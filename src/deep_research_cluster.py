import os
import asyncio
import json
import uuid
import re
from typing import List, Dict, Any
from pathlib import Path

from ai.llms import query_llm_cluster
from paper_retrieval import get_search_client

# Environment‐configurable flags
PROVIDER        = os.getenv("RESEARCH_PROVIDER", "orkg").lower()
FULL_SEARCH     = os.getenv("FULL_SEARCH", "0") == "1"
MAX_CONTENT_CHARS = int(os.getenv("MAX_CONTENT_CHARS", "1000"))

# Retrieval client
search_client = get_search_client(PROVIDER)

# Directory for logging raw hits
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def _extract_queries(raw: str) -> List[str]:
    """
    Try in order:
    1) parse a bare JSON array
    2) find a JSON array snippet [...]
    3) find JSON {"queries":[...]}
    4) fallback: numbered list
    5) fallback: semicolon‐delimited
    """
    r = raw.strip()
    # 1) bare array
    if r.startswith("["):
        try:
            arr = json.loads(r)
            if all(isinstance(q, str) for q in arr):
                return arr
        except:
            pass
    # 2) array inside text
    m = re.search(r"\[.*\]", r, flags=re.DOTALL)
    if m:
        try:
            arr = json.loads(m.group(0))
            if all(isinstance(q, str) for q in arr):
                return arr
        except:
            pass
    # 3) object with queries
    m2 = re.search(r"\{.*\}", r, flags=re.DOTALL)
    if m2:
        try:
            obj = json.loads(m2.group(0))
            if isinstance(obj, dict) and isinstance(obj.get("queries"), list):
                return [str(q) for q in obj["queries"]]
        except:
            pass
    # 4) numbered list
    lines = r.splitlines()
    qs = []
    for line in lines:
        m3 = re.match(r"^\s*\d+[\.\)]?\s*(.+)$", line)
        if m3:
            qs.append(m3.group(1).strip())
    if qs:
        return qs
    # 5) semicolon‐delimited
    if ";" in r:
        parts = [p.strip() for p in r.split(";") if len(p.strip()) > 3]
        if parts:
            return parts
    return []


async def deep_research(
    topic:       str,
    breadth:     int,
    depth:       int,
    questions:   List[str],
    answers:     List[str],
    model_name:  str,
    save_models: int,
) -> Dict[str, Any]:
    """
    Recursive breadth‐first research:
    - Level 1: generate `breadth` queries
    - Summarize each hit
    - If depth>1, recurse once with half breadth
    Returns {'learnings': [...], 'visited_urls': [...]}
    """
    # 1) Build context string
    context = topic
    if questions:
        pairs = "; ".join(f"Q:{q} A:{a}" for q, a in zip(questions, answers))
        context += f" — {pairs}"

    # 2) Generate exactly `breadth` search queries
    serp_prompt = (
        f"You are an expert academic search‐query generator.\n"
        f"Topic: {topic}\n"
        f"Context: {context}\n"
        f"Generate EXACTLY {breadth} concise, scholarly search queries relevant to this research.\n"
        f"Return ONLY a JSON array of strings, e.g. [\"query1\",\"query2\",…]."
    )
    raw_q = query_llm_cluster(serp_prompt, model_name, save_models)
    queries = _extract_queries(raw_q)
    # pad/truncate
    if len(queries) < breadth:
        queries += [f"{topic} overview"] * (breadth - len(queries))
    queries = queries[:breadth]
    print(f"[SERP] Level(breadth={breadth}, depth={depth}) queries: {queries}")

    learnings:  List[str] = []
    visited_urls: List[str] = []

    # 3) Fetch & summarize each query
    for q in queries:
        hits = await search_client.search(q, limit=breadth)
        # log raw hits for debugging
        uid = uuid.uuid4().hex
        (DATA_DIR / f"search_hits_{uid}.json").write_text(
            json.dumps(hits, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        # iterate top‐`breadth` hits
        for item in hits[:breadth]:
            # collect URL(s)
            urls = item.get("urls") or item.get("url") or []
            if isinstance(urls, str):
                urls = [urls]
            visited_urls.extend(urls)

            # pick content
            if FULL_SEARCH and (pid := item.get("paperId") or item.get("id")):
                doc = await getattr(search_client, "fetch_document", lambda x: {})(pid)
                content = doc.get("abstract", "") or doc.get("full_text", "")
            else:
                content = item.get("snippet") or item.get("abstract") or item.get("markdown") or ""
            content = content[:MAX_CONTENT_CHARS]
            if not content:
                continue

            # summarization prompt
            sum_prompt = (
                "You are an academic summarization assistant.\n"
                "Given this snippet, return exactly ONE concise, information‐rich sentence "
                "that captures its core insight (preserving entities, metrics, dates).\n"
                f"Snippet:\n{content}"
            )
            raw_s = query_llm_cluster(sum_prompt, model_name, save_models)
            sent = raw_s.strip().splitlines()[0]
            if sent:
                learnings.append(sent)

    # 4) Recurse if needed
    if depth > 1 and learnings:
        next_b = max(breadth // 2, 1)
        aggregate = "; ".join(learnings[:breadth])
        sub = await deep_research(
            topic=aggregate,
            breadth=next_b,
            depth=depth - 1,
            questions=[],
            answers=[],
            model_name=model_name,
            save_models=save_models,
        )
        learnings.extend(sub["learnings"])
        visited_urls.extend(sub["visited_urls"])

    return {"learnings": learnings, "visited_urls": visited_urls}


async def write_final_report(
    topic:       str,
    questions:   List[str],
    answers:     List[str],
    learnings:   List[str],
    visited_urls:List[str],
    model_name:  str,
    save_models: int,
) -> str:
    print(f"[REPORT] Generating report for topic: {topic}")
    if questions:
        print(f"[REPORT] Questions: {questions}")
        print(f"[REPORT] Answers: {answers}")
    print("[REPORT] Key findings:")
    for i, l in enumerate(learnings, 1):
        print(f"  {i}. {l}")

    sections = []
    for sec in ["Introduction", "Methods", "Results", "Discussion", "Conclusion"]:
        print(f"[REPORT] Section: {sec}")
        sec_prompt = (
            "You are a scholarly report writer.\n"
            f"Write the **{sec}** section for a report on '{topic}'.\n"
            "Use the following key findings as bullet points:\n" +
            "\n".join(f"- {l}" for l in learnings) + "\n"
            "Include inline citations [1], [2], etc., matching the numbered sources below.\n"
            f"Return only markdown text, starting with '## {sec}'."
        )
        raw_sec = query_llm_cluster(sec_prompt, model_name, save_models).strip()
        if not raw_sec.startswith(f"## {sec}"):
            raw_sec = f"## {sec}\n\n{raw_sec}"
        sections.append(raw_sec)

    report_md = "\n\n".join(sections)
    report_md += "\n\n## Sources\n"
    for i, url in enumerate(visited_urls, 1):
        report_md += f"{i}. {url}\n"
    return report_md


async def write_final_answer(
    topic:       str,
    questions:   List[str],
    answers:     List[str],
    learnings:   List[str],
    model_name:  str,
    save_models: int,
) -> str:
    print(f"[ANSWER] Generating concise answer for topic: {topic}")
    ans_prompt = (
        "You are an expert answer generator.\n"
        f"Question: {topic}\n"
        "Insights:\n" + "\n".join(f"- {l}" for l in learnings) + "\n"
        "Provide a concise, precise answer based on these insights. Return only the answer text."
    )
    return query_llm_cluster(ans_prompt, model_name, save_models)
