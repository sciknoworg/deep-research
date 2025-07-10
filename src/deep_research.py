import asyncio
import json
import re
import os
import aiohttp
import requests
from typing import List, Dict
from ai.llms import query_llm
from prompt_framework import make_json_array_prompt

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
        self.api_key   = api_key or os.getenv('FIRECRAWL_API_KEY')
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
    breadth: int,
    depth:   int,
    questions: List[str],
    answers:   List[str],
    model_name: str,
    save_models: int,
    use_firecrawl: bool
) -> Dict[str, List[str]]:
    client = FirecrawlApp() if use_firecrawl else ORKGAskApp()
    # Combine Q&A for context
    combined = topic
    if questions:
        qa = '; '.join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"{topic} — {qa}"

    # 1) Generate search queries
    prompt_q = ("You are a research assistant. Return exactly ",
         f"{breadth} concise search queries for this context: {combined}",
        "as a JSON array of strings. These are used to improve API search results. Do NOT return innitial prompt or additional text besides the queries.",
    )
    raw_q = await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt_q, model_name, save_models
    )
    try:
        queries = json.loads(raw_q)
        if not isinstance(queries, list):
            raise ValueError
    except Exception:
        queries = [l.strip() for l in raw_q.splitlines() if l.strip()]

    learnings, visited = [], []

    # 2) Fetch & summarize
    for q in queries:
        res     = await client.search(q)
        items   = res.get('data') or res.get('results') or []
        for item in items:
            pid = item.get('paperId') or item.get('id')
            visited.append(str(pid))
            if use_firecrawl:
                abstract = item.get('snippet', '')
            else:
                abstract = await ORKGAskApp().fetch_content(str(pid))

            sum_prompt = (
                f"Extract the key finding from this abstract as a single sentence: “{abstract}”. "
                "Return only that sentence."
            )
            summary = await asyncio.get_event_loop().run_in_executor(
                None, query_llm, sum_prompt, model_name, save_models
            )
            learnings.append(summary)

    # 3) Depth recursion
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
    answers:   List[str],
    learnings: List[str],
    visited:   List[str],
    model_name: str,
    save_models: int
) -> str:
    combined = topic
    if questions:
        qa = '; '.join(f"Q: {q} A: {a}" for q,a in zip(questions,answers))
        combined = f"{topic} — {qa}"
    prompt = (
        f"Write a comprehensive report based on “{combined}”. "
        f"Learnings: {'; '.join(learnings)}. "
        f"Sources: {'; '.join(visited)}. "
        "Return only the report content; no explanations."
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )

async def write_final_answer(
    topic: str,
    questions: List[str],
    answers:   List[str],
    learnings: List[str],
    model_name: str,
    save_models: int
) -> str:
    combined = topic
    if questions:
        qa = '; '.join(f"Q: {q} A: {a}" for q,a in zip(questions,answers))
        combined = f"{topic} — {qa}"
    prompt = (
        f"Answer concisely based on “{combined}”. "
        f"Key findings: {'; '.join(learnings)}. "
        "Return only the answer; no chain-of-thought."
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )