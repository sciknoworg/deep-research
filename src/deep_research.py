import asyncio
import json
import re
import os
import aiohttp
import requests
from typing import List, Dict
from ai.llms import query_llm

class ORKGAskApp:
    def __init__(self):
        self.base_url = 'https://api.ask.orkg.org/index'

    async def search(self, query: str, limit: int = 10) -> Dict:
        params = {'query': query, 'limit': limit}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/search", params=params) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def fetch_content(self, paper_id: str) -> str:
        url = f"https://api.orkg.org/papers/{paper_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get('abstract', '')

class FirecrawlApp:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        self.base_url = 'https://api.firecrawl.com/search'

    async def search(self, query: str, limit: int = 10) -> Dict:
        params = {'key': self.api_key, 'q': query, 'limit': limit}
        def _sync_search():
            r = requests.get(self.base_url, params=params)
            r.raise_for_status()
            return r.json()
        return await asyncio.get_event_loop().run_in_executor(None, _sync_search)

async def deep_research(
    topic: str,
    breadth: int = 4,
    depth: int = 2,
    questions: List[str] = None,
    answers: List[str] = None,
    model_name: str = None,
    save_models: int = 0,
    use_firecrawl: bool = False
) -> Dict[str, List[str]]:
    if use_firecrawl:
        search_client = FirecrawlApp()
    else:
        search_client = ORKGAskApp()

    questions = questions or []
    answers = answers or []
    combined = topic
    if questions:
        qa_block = '; '.join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"Initial: {topic} — {qa_block}"

    prompt = (
        f"Context for query generation: {combined}. Generate exactly {breadth} concise search queries." 
        " Return only a JSON array of query strings."
    )
    raw = await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )
    m = re.search(r"\[.*?\]", raw, flags=re.S)
    if m:
        try:
            raw_arr = json.loads(m.group(0))
        except json.JSONDecodeError:
            raw_arr = []
    else:
        raw_arr = [line.strip() for line in raw.splitlines() if line.strip()]

    serp_queries = []
    for item in raw_arr:
        if isinstance(item, str):
            serp_queries.append(item)
        elif isinstance(item, dict) and 'query' in item:
            serp_queries.append(item['query'])
        else:
            serp_queries.append(str(item))

    learnings = []
    visited = []

    for q in serp_queries:
        res = await search_client.search(q)
        entries = res.get('data') or res.get('results') or []
        for entry in entries:
            pid = entry.get('paperId') or entry.get('id')
            vid = str(pid)
            visited.append(vid)
            abstract = await (search_client.fetch_content if not use_firecrawl else (lambda x: entry.get('snippet', '')))(vid)
            summary_prompt = f"Summarize: {abstract}"
            summary = await asyncio.get_event_loop().run_in_executor(
                None, query_llm, summary_prompt, model_name, save_models
            )
            learnings.append(summary)

    if depth > 1 and learnings:
        sub = await deep_research(
            ' '.join(learnings), breadth, depth - 1, [], [],
            model_name, save_models, use_firecrawl
        )
        learnings.extend(sub.get('learnings', []))
        visited.extend(sub.get('visited', []))

    return {'learnings': learnings, 'visited': visited}

async def write_final_report(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    visited: List[str],
    model_name: str = None,
    save_models: int = 0
) -> str:
    combined = topic
    if questions:
        qa_block = '; '.join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"Initial: {topic} — {qa_block}"
    prompt = (
        f"Write a comprehensive report based on '{combined}'. "
        f"Learnings: {'; '.join(learnings)}. "
        f"Sources: {'; '.join(visited)}"
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )

async def write_final_answer(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    model_name: str = None,
    save_models: int = 0
) -> str:
    combined = topic
    if questions:
        qa_block = '; '.join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"Initial: {topic} — {qa_block}"
    prompt = (
        f"Answer concisely based on '{combined}'. "
        f"Key findings: {'; '.join(learnings)}"
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )