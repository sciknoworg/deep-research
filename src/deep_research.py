# File: src/deep_research.py
import asyncio
import json
import re
from typing import List, Dict
import aiohttp
from ai.llms import query_llm

# ORKG client for paper search and fetch
class ORKGAskApp:
    def __init__(self):
        self.base_url = "https://api.ask.orkg.org/index"

    async def search(self, query: str, limit: int = 10) -> Dict:
        params = {"query": query, "limit": limit}
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

search_client = ORKGAskApp()

async def deep_research(
    topic: str,
    breadth: int = 4,
    depth: int = 2,
    questions: List[str] = None,
    answers: List[str] = None
) -> Dict[str, List[str]]:
    """
    Perform recursive research:
      1) Generate search queries via LLM
      2) Fetch and summarize ORKG papers
      3) Recurse for deeper levels
    Returns a dict with 'learnings' and 'visited'.
    """
    questions = questions or []
    answers = answers or []

        # Combine topic and Q&A for context
    combined = topic
    if questions:
        qa_block = "; ".join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"Initial: {topic} — {qa_block}"

    # 1) Generate search queries
    # Clean context to avoid duplication
    combined_ctx = combined.replace(" — ", "")

    prompt = (
        "Context for query generation:"
        f"{combined_ctx}"
        f"Now, generate exactly {breadth} concise search queries that would find relevant academic papers on ORKG. "
        "Return only a JSON array of query strings; do not include any explanations or numbering."
    )
    raw = await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, None
    )

    # Extract JSON array
    m = re.search(r"\[.*?\]", raw, flags=re.S)
    if m:
        try:
            raw_arr = json.loads(m.group(0))
        except json.JSONDecodeError:
            raw_arr = []
    else:
        raw_arr = [line.strip() for line in raw.splitlines() if line.strip()]

    # Normalize to list of strings
    serp_queries: List[str] = []
    for item in raw_arr:
        if isinstance(item, str):
            serp_queries.append(item)
        elif isinstance(item, dict) and 'query' in item:
            serp_queries.append(item['query'])
        else:
            serp_queries.append(str(item))

    learnings: List[str] = []
    visited: List[str] = []

    # 2) Fetch and summarize each paper
    for q in serp_queries:
        res = await search_client.search(q)
        entries = res.get('data') or res.get('results') or []
        for entry in entries:
            pid = entry.get('paperId') or entry.get('id') or entry
            vid = str(pid)
            visited.append(vid)
            abstract = await search_client.fetch_content(vid)
            # Summarize abstract via LLM
            summary = await asyncio.get_event_loop().run_in_executor(
                None, query_llm, f"Summarize abstract: {abstract}", None
            )
            learnings.append(summary)

    # 3) Recurse deeper if needed
    if depth > 1 and learnings:
        sub = await deep_research(' '.join(learnings), breadth, depth - 1)
        learnings.extend(sub.get('learnings', []))
        visited.extend(sub.get('visited', []))

    return {'learnings': learnings, 'visited': visited}

async def write_final_report(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str],
    visited: List[str]
) -> str:
    """
    Compile a comprehensive report via LLM.
    """
    combined = topic
    if questions:
        qa_block = "; ".join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"Initial: {topic} — {qa_block}"
    prompt = (
        f"Write a comprehensive report based on '{combined}'. "
        f"Learnings: {'; '.join(learnings)}. "
        f"Sources: {'; '.join(visited)}"
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, None
    )

async def write_final_answer(
    topic: str,
    questions: List[str],
    answers: List[str],
    learnings: List[str]
) -> str:
    """
    Compile a concise answer via LLM.
    """
    combined = topic
    if questions:
        qa_block = "; ".join(f"Q: {q} A: {a}" for q, a in zip(questions, answers))
        combined = f"Initial: {topic} — {qa_block}"
    prompt = (
        f"Answer concisely based on '{combined}'. "
        f"Key findings: {'; '.join(learnings)}"
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, None
    )
