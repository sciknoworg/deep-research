import os
import sys
import asyncio
import json
import re
from typing import List, Dict, Any
from collections import defaultdict
import aiohttp

from ai.llms import query_llm
from ai.prompt_utils import trim_prompt
from prompt import system_prompt

# Ensure UTF-8 console output
sys.stdout.reconfigure(encoding='utf-8')

# --- Clients ---
class FirecrawlApp:
    """Client for the Firecrawl API."""
    BASE_URL = os.getenv('FIRECRAWL_BASE_URL', 'https://api.firecrawl.dev/v1')
    API_KEY  = os.getenv('FIRECRAWL_KEY', '')

    async def search(self, query: str, limit: int = 5, timeout: int = 15000) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/search"
        headers = {"Authorization": f"Bearer {self.API_KEY}", "Content-Type": "application/json"}
        body = {"query": query, "limit": limit, "timeout": timeout, "scrapeOptions": {"formats": ["markdown"]}}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as resp:
                resp.raise_for_status()
                data = await resp.json()
        return data.get('data', [])

class ORKGAskApp:
    """Client for the ORKG Ask API."""
    BASE_URL = 'https://api.ask.orkg.org/index'

    async def search(self, query: str, limit: int = 5, timeout: int = 15000) -> List[Dict[str, Any]]:
        url = f"{self.BASE_URL}/search"
        params = {"query": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=timeout/1000) as resp:
                print("[ORKG] resp.status", resp.status)
                resp.raise_for_status()
                data = await resp.json()
        # ORKG returns either 'data' or 'payload.items'
        return data.get('data', []) or data.get('payload', {}).get('items', [])

    async def fetch_content(self, paper_id: str) -> str:
        """Fetch abstract content for a paper ID."""
        url = f"https://api.orkg.org/papers/{paper_id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        return ''
                    doc = await resp.json()
                    return doc.get('abstract', '') or ''
        except Exception:
            return ''

# Select client based on flag
def get_search_client(use_firecrawl: bool):
    return FirecrawlApp() if use_firecrawl else ORKGAskApp()

# --- JSON extraction ---
def extract_json(raw: str) -> Dict[str, Any]:
    m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not m:
        raise ValueError("No JSON found in LLM response")
    return json.loads(m.group(0))

# --- SERP query generation ---
async def generate_serp_queries(
    topic: str,
    breadth: int,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    model_name: str,
    save_models: int
) -> List[str]:
    # Build context with Q&A and previous learnings
    ctx = topic
    if questions:
        qa = '; '.join(f"Q:{q} A:{a}" for q,a in zip(questions, answers))
        ctx = f"{topic} — {qa}"
    learn_ctx = '\n'.join(learnings)
    prompt = trim_prompt(
        f"""
You are a focused research assistant generating concise search queries.
Topic: {topic}
Context: {ctx}
Generate exactly {breadth} search queries. Include only user-affirmed aspects; ignore negatives.
Previous learnings:
{learn_ctx}
Return *only* a JSON object {{"queries":[...]}} with no extra text.
"""
    )
    raw = query_llm(prompt, model_name, save_models)
    try:
        data = extract_json(raw)
        qs = data.get('queries', [])
        if isinstance(qs, list) and qs:
            return qs[:breadth]
    except Exception:
        print(f"[SERP-ERR] failed to parse JSON from: {raw}")
    return [f"{topic} overview"]

# --- SERP result summarization ---
async def process_serp_result(
    query: str,
    items: List[Dict[str, Any]],
    model_name: str,
    save_models: int,
    num_learnings: int = 3,
    num_followups: int = 3
) -> Dict[str, Any]:
    orkg = ORKGAskApp()
    blocks = []
    visited = []
    # Collect text blocks
    for it in items[:num_learnings]:
        txt = it.get('snippet') or it.get('abstract', '')
        if not txt:
            pid = it.get('paperId') or it.get('id')
            if pid:
                txt = await orkg.fetch_content(str(pid))
        if txt:
            blocks.append(trim_prompt(txt, 25000))
        url = (it.get('urls') or it.get('url') or '')
        if url:
            visited.append(url[0] if isinstance(url, list) else url)
    print(f"Ran {query}, found {len(blocks)} contents")
    if not blocks:
        return {'learnings': [], 'followUpQuestions': [], 'visited': visited}
    contents_text = '\n'.join(f"<content>\n{b}\n</content>" for b in blocks)
    prompt = trim_prompt(
        f"""
Given the following contents from a search for <query>{query}</query>, generate up to {num_learnings} concise learning sentences and up to {num_followups} follow-up questions.
Return ONLY a JSON object matching:
{{"learnings":[string,...],"followUpQuestions":[string,...]}}

<contents>
{contents_text}
</contents>
"""
    )
    raw = query_llm(prompt, model_name, save_models)
    try:
        data = extract_json(raw)
        return {'learnings': data.get('learnings', []), 'followUpQuestions': data.get('followUpQuestions', []), 'visited': visited}
    except Exception:
        print(f"[SUMMARY-ERR] invalid JSON from LLM: {raw}")
        return {'learnings': [], 'followUpQuestions': [], 'visited': visited}

# --- Deep research orchestration ---
async def deep_research(
    topic: str,
    breadth: int,
    depth: int,
    questions: List[str],
    answers: List[str],
    model_name: str,
    save_models: int,
    use_firecrawl: bool = False
) -> Dict[str, Any]:
    client = get_search_client(use_firecrawl)
    fallback = get_search_client(not use_firecrawl)
    all_learnings: List[str] = []
    visited_urls: List[str] = []
    for level in range(depth):
        prompt_topic = topic if level == 0 else '; '.join(all_learnings)
        queries = await generate_serp_queries(prompt_topic, breadth, questions, answers, all_learnings, model_name, save_models)
        # Clear QA after first level
        questions, answers = [], []
        for q in queries:
            print(f"[SEARCH {level+1}/{depth}] {q}")
            items = await client.search(q, limit=breadth)
            if not items:
                items = await fallback.search(q, limit=breadth)
            summary = await process_serp_result(q, items, model_name, save_models, breadth, breadth)
            all_learnings.extend(summary['learnings'])
            visited_urls.extend(summary['visited'])
    return {'learnings': all_learnings, 'visited_urls': visited_urls}

# --- Final report and answer ---
async def write_final_report(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    visited_urls: List[str],
    model_name: str,
    save_models: int
) -> str:
    qa_block = ''
    if questions:
        qa_block = ' — ' + '; '.join(f"Q:{q} A:{a}" for q,a in zip(questions, answers))
    learn_str = '\n'.join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""
Given the following user prompt, write a detailed Markdown report (3+ pages) including ALL the learnings:
<prompt>{topic}{qa_block}</prompt>

<learnings>
{learn_str}
</learnings>
"""
    )
    raw = query_llm(full_prompt, model_name, save_models)
    parsed = extract_json(raw)
    report_md = parsed.get('reportMarkdown', '')
    report_md += "\n\n## Sources\n" + '\n'.join(f"- {u}" for u in visited_urls)
    return report_md

async def write_final_answer(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    model_name: str,
    save_models: int
) -> str:
    qa_block = ''
    if questions:
        qa_block = ' — ' + '; '.join(f"Q:{q} A:{a}" for q,a in zip(questions, answers))
    learn_str = '\n'.join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""
Given the following user prompt, write a concise final answer using the learnings:
<prompt>{topic}{qa_block}</prompt>

<learnings>
{learn_str}
</learnings>
"""
    )
    raw = query_llm(full_prompt, model_name, save_models)
    parsed = extract_json(raw)
    return parsed.get('exactAnswer', '')
