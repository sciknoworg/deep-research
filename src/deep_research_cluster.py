import os
import asyncio
import json
import uuid
import re
from typing import List, Dict, Any
from pathlib import Path

from ai.llms import query_llm_cluster
from paper_retrieval import get_search_client
from ai.prompt_utils import trim_prompt
from prompt import system_prompt

# Environment-configurable flags
PROVIDER = os.getenv('RESEARCH_PROVIDER', 'orkg').lower()
FULL_SEARCH = os.getenv('FULL_SEARCH', '0') == '1'
MAX_CONTENT_CHARS = int(os.getenv('MAX_CONTENT_CHARS', '1000'))

# Initialize retrieval client
search_client = get_search_client(PROVIDER)

# Directory for logging raw data
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

async def deep_research(
    topic: str,
    breadth: int,
    depth: int,
    questions: List[str],
    answers: List[str],
    model_name: str,
    save_models: int,
) -> Dict[str, Any]:
    """
    Perform recursive research with breadth-first query generation and summarization.
    Level 1: generate `breadth` queries.
    Level >1: after summarizing all level learnings, recurse once with breadth//2.
    Returns a dict with 'learnings' and 'visited_urls'.
    """
    def extract_json(raw: str) -> Dict[str, Any]:
        m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not m:
            raise ValueError("No JSON found in LLM output")
        return json.loads(m.group(0))

    # Build prompt context
    context = topic
    if questions:
        qa_pairs = '; '.join(f"Q:{q} A:{a}" for q, a in zip(questions, answers))
        context += f" — {qa_pairs}"

    # 1) Generate queries for this level
    serp_prompt = trim_prompt(f"""
You are an expert academic search-query generator.
Topic: {topic}
Context: {context}
Generate EXACTLY {breadth} concise, scholarly search queries focused on methods, properties, or applications.
Return ONLY THE QUERIES IN FORMAT: {{"queries":[...]}}\n.
Nothing besides the queries should be output.
Example:
{{"queries":["neptune atmosphere composition","neptune orbital dynamics"]}}
"""
    )
    raw_q = query_llm_cluster(serp_prompt, model_name, save_models)
    try:
        queries = extract_json(raw_q)['queries']
    except Exception:
        queries = []
    # pad or truncate to breadth
    if len(queries) < breadth:
        queries += [f"{topic} overview"] * (breadth - len(queries))
    else:
        queries = queries[:breadth]
    print(f"[SERP] Level(breadth={breadth}, depth={depth}) queries: {queries}")

    all_learnings: List[str] = []
    all_urls: List[str] = []

    # 2) Summarize hits for each query
    for q in queries:
        hits = await search_client.search(q, limit=breadth)
        # log raw
        uid = uuid.uuid4().hex
        (DATA_DIR / f"search_hits_{uid}.json").write_text(json.dumps(hits, ensure_ascii=False, indent=2), encoding='utf-8')
        for item in hits[:breadth]:
            # collect URLs
            urls = item.get('urls') or item.get('url') or []
            if isinstance(urls, str):
                urls = [urls]
            all_urls.extend(urls)
            # choose content
            if FULL_SEARCH and (pid := item.get('paperId') or item.get('id')):
                doc = await getattr(search_client, 'fetch_document', lambda x: {})(pid)
                content = doc.get('abstract') or doc.get('full_text', '')
                content = content[:MAX_CONTENT_CHARS]
            else:
                content = item.get('snippet') or item.get('abstract') or item.get('markdown') or ''
            if not content:
                continue
            # summarization
            summary_prompt = trim_prompt(f"""
You are an academic summarization assistant.
Given a text snippet from a research abstract or result, produce exactly one concise, information-rich sentence capturing the core finding or insight, preserving entities, metrics, and dates.
Return only the sentence.
Content:
{content}
"""
            )
            raw_s = query_llm_cluster(summary_prompt, model_name, save_models)
            sent = raw_s.strip().splitlines()[0] if raw_s else ''
            if sent:
                all_learnings.append(sent)

    # 3) Recurse once with aggregated learnings
    if depth > 1 and all_learnings:
        next_breadth = max(breadth // 2, 1)
        aggregated = '; '.join(all_learnings[:breadth])
        sub = await deep_research(
            topic=aggregated,
            breadth=next_breadth,
            depth=depth - 1,
            questions=[],
            answers=[],
            model_name=model_name,
            save_models=save_models,
        )
        all_learnings.extend(sub['learnings'])
        all_urls.extend(sub['visited_urls'])

    return {'learnings': all_learnings, 'visited_urls': all_urls}

async def write_final_report(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    visited_urls: List[str],
    model_name: str,
    save_models: int,
) -> str:
    """
    Generate a structured Markdown report: Introduction, Methods, Results, Discussion, Conclusion.
    Each section is requested separately to keep prompts within token limits.
    """
    print(f"[REPORT] Generating report for topic: {topic}")
    if questions:
        print(f"[REPORT] Questions: {questions}")
        print(f"[REPORT] Answers: {answers}")
    print("[REPORT] Key findings:")
    for idx, l in enumerate(learnings, 1):
        print(f"  {idx}. {l}")

    report_sections = []
    for sec in ["Introduction", "Methods", "Results", "Discussion", "Conclusion"]:
        print(f"[REPORT] Generating section: {sec}")
        section_prompt = trim_prompt(f"""
You are a scholarly report writer.
Write the **{sec}** section for a research report on '{topic}'.
Use the following key findings as bullet points:
{chr(10).join(f'- {l}' for l in learnings)}
Include inline citations [1], [2], etc., corresponding to the numbered sources below.
Return only the Markdown text for this section, starting with '## {sec}'.
"""
        )
        raw_sec = query_llm_cluster(section_prompt, model_name, save_models)
        md = raw_sec.strip()
        if not md.startswith(f"## {sec}"):
            md = f"## {sec}\n\n{md}"
        report_sections.append(md)

    report_md = "\n\n".join(report_sections)
    report_md += "\n\n## Sources\n"
    for i, url in enumerate(visited_urls, 1):
        report_md += f"{i}. {url}\n"
    return report_md

async def write_final_answer(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    model_name: str,
    save_models: int,
) -> str:
    print(f"[ANSWER] Generating concise answer for topic: {topic}")
    answer_prompt = trim_prompt(f"""
You are an expert answer generator.
Question: {topic}
Insights:
{chr(10).join(f'- {l}' for l in learnings)}
Provide a concise, precise answer based on these insights. Return only the answer text.
"""
    )
    return query_llm_cluster(answer_prompt, model_name, save_models)
