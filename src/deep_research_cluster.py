import os
import asyncio
import json
import uuid
import re
from typing import List, Dict, Any
from pathlib import Path

from ai.llms import query_llm_cluster
from paper_retrieval import get_search_client

# Environment-configurable flags
PROVIDER          = os.getenv('RESEARCH_PROVIDER', 'orkg').lower()
FULL_SEARCH       = os.getenv('FULL_SEARCH', '0') == '1'
MAX_CONTENT_CHARS = int(os.getenv('MAX_CONTENT_CHARS', '1000'))

# Initialize retrieval client
search_client = get_search_client(PROVIDER)

# Directory for logging raw data
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)


def extract_queries(raw: str) -> List[str]:
    """
    Extract a list of queries from various raw LLM outputs.
    Supports:
      1) Direct JSON array
      2) JSON object with "queries" field
      3) Inline JSON array in text
      4) Numbered list ("1.")
      5) Semicolon-separated strings
    """
    text = raw.strip()
    # 1) Direct JSON array
    try:
        arr = json.loads(text)
        if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
            return arr
    except:
        pass
    # 2) JSON object with "queries"
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and isinstance(obj.get('queries'), list):
            return [str(x) for x in obj['queries'] if isinstance(x, str)]
    except:
        pass
    # 3) Inline JSON array
    m = re.search(r"\[[^\]]*\]", text)
    if m:
        try:
            arr = json.loads(m.group(0))
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
                return arr
        except:
            pass
    # 4) Numbered list
    lines = text.splitlines()
    qs = []
    for ln in lines:
        m2 = re.match(r"^\s*\d+[\.)]\s*(.+)$", ln)
        if m2:
            qs.append(m2.group(1).strip())
    if qs:
        return qs
    # 5) Semicolon-separated
    if ';' in text:
        parts = [p.strip() for p in text.split(';') if p.strip()]
        if parts:
            return parts
    # fallback empty
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
    Recursive deep research:
      - breadth: number of queries per level
      - depth: recursion levels
    Returns dict with 'learnings' and 'visited_urls'.
    """
    # Build context
    context = topic
    if questions:
        context += ' — ' + '; '.join(f'Q:{q} A:{a}' for q, a in zip(questions, answers))

    # 1) Generate queries
    prompt_q = (
        f"You are an academic search-query generator. Topic: {topic}."
        f"Context: {context}. Generate EXACTLY {breadth} concise scholarly queries."
        "Return only the list of queries as an array or numbered list."
        "Format: [\"query1\",\"query2\",…]."
    )
    raw_q = query_llm_cluster(prompt_q, model_name, save_models)
    queries = extract_queries(raw_q)
    # pad/truncate
    if len(queries) < breadth:
        queries += [f"{topic} overview"] * (breadth - len(queries))
    queries = queries[:breadth]
    print(f"[SERP] Level(breadth={breadth}, depth={depth}) queries: {queries}")

    all_learnings: List[str] = []
    all_urls:      List[str] = []

    # 2) Fetch hits and summarize
    for q in queries:
        hits = await search_client.search(q, limit=breadth)
        # log raw
        uid = uuid.uuid4().hex
        (DATA_DIR / f"hits_{uid}.json").write_text(json.dumps(hits, ensure_ascii=False, indent=2))
        for item in hits[:breadth]:
            # collect URLs
            urls = item.get('urls') or item.get('url') or []
            if isinstance(urls, str): urls = [urls]
            all_urls.extend(urls)
            # get content
            if FULL_SEARCH:
                pid = item.get('paperId') or item.get('id')
                doc = await getattr(search_client, 'fetch_document', lambda x: {})(pid)
                content = doc.get('abstract', '') or doc.get('full_text', '')
            else:
                content = item.get('snippet') or item.get('abstract') or item.get('markdown') or ''
            content = content[:MAX_CONTENT_CHARS]
            if not content: continue
            # summarize
            prompt_s = (
                "You are a concise summarization assistant. "
                "Summarize in ONE information-rich sentence preserving entities and metrics. "
                f"Content: {content}"
            )
            raw_s = query_llm_cluster(prompt_s, model_name, save_models)
            sent = raw_s.strip().splitlines()[0] if raw_s else ''
            if sent:
                all_learnings.append(sent)

    # 3) Recurse
    if depth > 1 and all_learnings:
        next_b = max(breadth // 2, 1)
        next_topic = '; '.join(all_learnings[:breadth])
        sub = await deep_research(next_topic, next_b, depth-1, [], [], model_name, save_models)
        all_learnings.extend(sub['learnings'])
        all_urls.extend(sub['visited_urls'])

    return {'learnings': all_learnings, 'visited_urls': all_urls}

async def write_final_report(
    topic:       str,
    questions:   List[str],
    answers:     List[str],
    learnings:   List[str],
    visited_urls:List[str],
    model_name:  str,
    save_models: int,
) -> str:
    """
    Build a 5-section Markdown report using learnings and numbered sources.
    """
    print(f"[REPORT] {topic} | Qs: {questions} | As: {answers}")
    print(f"[REPORT] Findings: {learnings}")
    # prepare sources
    src_md = '\n'.join(f"[{i+1}] {u}" for i,u in enumerate(visited_urls))
    parts = []
    for sec in ["Introduction","Methods","Results","Discussion","Conclusion"]:
        print(f"[REPORT] Section: {sec}")
        prompt_sec = (
            f"Write the {sec} section for '{topic}' using these findings as bullets:\n" +
            '\n'.join(f"- {f}" for f in learnings) +
            f"\nNumbered sources:\n{src_md}\n"
            "Return only Markdown for this section starting with '## {sec}'."
        )
        raw = query_llm_cluster(prompt_sec, model_name, save_models).strip()
        md = raw if raw.startswith(f"## {sec}") else f"## {sec}\n\n" + raw
        parts.append(md)
    report = '\n\n'.join(parts)
    report += "\n\n## Sources\n" + '\n'.join(f"{i+1}. {u}" for i,u in enumerate(visited_urls))
    return report

async def write_final_answer(
    topic:       str,
    questions:   List[str],
    answers:     List[str],
    learnings:   List[str],
    model_name:  str,
    save_models: int,
) -> str:
    print(f"[ANSWER] {topic}")
    prompt_ans = (
        f"Provide a concise answer to '{topic}' based on these insights:\n" +
        '\n'.join(f"- {f}" for f in learnings) +
        "\nReturn only the answer text."
    )
    return query_llm_cluster(prompt_ans, model_name, save_models)