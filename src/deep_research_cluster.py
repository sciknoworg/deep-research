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
PROVIDER          = os.getenv('RESEARCH_PROVIDER', 'orkg').lower()
FULL_SEARCH       = os.getenv('FULL_SEARCH', '0') == '1'
MAX_CONTENT_CHARS = int(os.getenv('MAX_CONTENT_CHARS', '1000'))

# Initialize retrieval client
search_client = get_search_client(PROVIDER)

# Directory for logging raw data
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

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
    Recursive deep research using SLURM jobs with breadth-halving at each level:
      - breadth: number of queries at this level
      - depth: recursion depth remaining
      - FULL_SEARCH: if set, fetch full document metadata for summarization
      - MAX_CONTENT_CHARS: truncate full document content
    """
    # helper to parse JSON from LLM
    def extract_json(raw: str) -> Dict[str, Any]:
        m = re.search(r"\{.*\}\Z", raw, flags=re.DOTALL)
        if not m:
            raise ValueError('No JSON found')
        return json.loads(m.group(0))

    # build context
    context = topic
    if questions:
        context += ' — ' + '; '.join(f'Q:{q} A:{a}' for q,a in zip(questions,answers))

    # 1) generate EXACTLY breadth queries
    serp_prompt = trim_prompt(
        f"You are an expert search-query generator.\n"
        f"Topic: {topic}\n"
        f"Context: {context}\n"
        f"Generate EXACTLY {breadth} distinct scholarly search queries."
        " Output ONLY the JSON for the queries: {\"queries\":[…]}.\n"
        "Example: {\"queries\":[\"neptune atmosphere composition\",\"neptune orbital dynamics\"]}\n"
        "Return only the JSON array of queries, no extra text."
    )
    raw_q = query_llm_cluster(serp_prompt, model_name, save_models)
    try:
        queries = extract_json(raw_q).get('queries', [])
        if not isinstance(queries, list): raise ValueError
    except Exception:
        queries = []
    # pad/truncate
    if len(queries) < breadth:
        queries += [f'{topic} overview'] * (breadth - len(queries))
    else:
        queries = queries[:breadth]

    all_learnings: List[str] = []
    all_visited_urls: List[str] = []

    # 2) process each query and optionally recurse
    for q in queries:
        # fetch hits
        hits = await search_client.search(q, limit=breadth)
        # log raw hits
        uid = uuid.uuid4().hex
        (DATA_DIR / f'search_hits_{uid}.json').write_text(
            json.dumps(hits, ensure_ascii=False, indent=2), encoding='utf-8'
        )

        # this level's learnings and urls
        level_learnings: List[str] = []
        level_urls:     List[str] = []
        for item in hits[:breadth]:
            # extract URLs from payload
            urls = item.get('urls') or item.get('url') or []
            if isinstance(urls, str):
                urls = [urls]
            for link in urls:
                level_urls.append(link)

            # determine content source
            if FULL_SEARCH:
                pid = item.get('paperId') or item.get('id')
                if pid:
                    doc = await search_client.fetch_document(str(pid))
                    content = doc.get('abstract') or doc.get('full_text') or ''
                    if len(content) > MAX_CONTENT_CHARS:
                        content = content[:MAX_CONTENT_CHARS]
                else:
                    content = ''
            else:
                content = item.get('snippet') or item.get('abstract') or item.get('markdown') or ''
            if not content:
                continue

            # summarize
            sum_prompt = trim_prompt(
                "You are a concise summarization assistant.\n"
                "Summarize the content below in exactly one information-rich sentence, preserving entities and metrics. Return only that sentence.\n"
                f"Content:\n{content}"
            )
            raw_s = query_llm_cluster(sum_prompt, model_name, save_models)
            sent = raw_s.strip().splitlines()[0] if raw_s else ''
            if sent:
                level_learnings.append(sent)

        all_learnings.extend(level_learnings)
        all_visited_urls.extend(level_urls)

        # recurse if depth > 1
        if depth > 1 and level_learnings:
            sub = await deep_research(
                topic='; '.join(level_learnings),
                breadth=max(breadth//2, 1),
                depth=depth-1,
                questions=[],
                answers=[],
                model_name=model_name,
                save_models=save_models
            )
            all_learnings.extend(sub['learnings'])
            all_visited_urls.extend(sub['visited_urls'])

    return {'learnings': all_learnings, 'visited_urls': all_visited_urls}

async def write_final_report(
    topic:        str,
    questions:    List[str],
    answers:      List[str],
    learnings:    List[str],
    visited_urls: List[str],
    model_name:   str,
    save_models:  int,
) -> str:
    """
    Generate a structured Markdown report in 5 sections via separate prompts.
    """
    sections = ["Introduction","Methods","Results","Discussion","Conclusion"]
    report_parts = []
    for sec in sections:
        sec_prompt = trim_prompt(
            f"You are writing the {sec} section. Topic: {topic}."
            f" Key findings: {', '.join(learnings)}."
            " Cite sources inline. Return only Markdown for this section."
        )
        raw = query_llm_cluster(sec_prompt, model_name, save_models)
        md = raw.strip()
        if not md.startswith(f"## {sec}"):
            md = f"## {sec}\n\n" + md
        report_parts.append(md)
    report_md = "\n\n".join(report_parts)
    report_md += "\n\n## Sources\n" + "\n".join(f"- {u}" for u in visited_urls)
    return report_md

async def write_final_answer(
    topic:       str,
    questions:   List[str],
    answers:     List[str],
    learnings:   List[str],
    model_name:  str,
    save_models: int,
) -> str:
    prompt = trim_prompt(
        "You are an expert answer generator. Provide a concise answer based on research.\n"
        f"Question: {topic}. Insights: {', '.join(learnings)}.\n"
        "Return only the answer text."
    )
    return query_llm_cluster(prompt, model_name, save_models)
