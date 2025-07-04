import os
import sys
import asyncio
from typing import List, Dict
import aiohttp
import json
from ai.llms import query_llm, ModelConfig
from dotenv import load_dotenv

# Load env and ensure UTF-8 output
load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

# Cluster LLM client
_model_cfg = ModelConfig()
_llm_client = _model_cfg.client
_llm_model = _model_cfg.model

# Search clients
class FirecrawlApp:
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"query": query, "limit": limit, "timeout": timeout, "scrapeOptions": {"formats": ["markdown"]}}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/search", json=body, headers=headers) as resp:
                resp.raise_for_status()
                return await resp.json()

class ORKGAskApp:
    def __init__(self, base_url: str = "https://api.ask.orkg.org/index"):
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        params = {"query": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/search", params=params) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def fetch_content(self, paper_id: str) -> str:
        # Fetch abstract from ORKG Graph API
        graph_url = f"https://api.orkg.org/papers/{paper_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(graph_url) as resp:
                resp.raise_for_status()
                data = await resp.json()
        return data.get('abstract', '')

# Instantiate search client based on provider
provider = os.getenv("RESEARCH_PROVIDER", "orkg").lower()
search_client = ORKGAskApp() if provider == "orkg" else FirecrawlApp(api_key=os.getenv("FIRECRAWL_KEY", ""))

# Prompt builders

def build_serp_prompt(query: str, breadth: int, learnings: List[str]) -> str:
    # Use initial line only
    first_line = query.split("\n")[0].replace("Initial:", "").strip()
    learn_text = "; ".join(learnings) if learnings else ""
    # Instruction for LLM
    return (
        f"Generate {breadth} search queries as a JSON array of strings. "
        f"Return only the JSON array without any extra commentary. "
        f"Query: {first_line}. Learnings: {learn_text}"
    )


def build_summary_prompt(source: str, content: str) -> str:
    return f"Summarize the abstract for {source}: {content}"


def build_report_prompt(prompt: str, learnings: List[str], visited: List[str]) -> str:
    return (
        f"Write a comprehensive report. Prompt: {prompt}. "
        f"Learnings: {'; '.join(learnings)}. "
        f"Sources: {'; '.join(visited)}"
    )


def build_answer_prompt(prompt: str, learnings: List[str]) -> str:
    return f"Answer concisely. Question: {prompt}. Key findings: {'; '.join(learnings)}"

# Generate SERP queries
def extract_json_array(text: str) -> List[str]:
    try:
        return json.loads(text)
    except:
        # find first [...] block
        import re
        m = re.search(r"\[.*\]", text)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                pass
    return []

async def generate_serp_queries(query: str, breadth: int, learnings: List[str]) -> List[str]:
    prompt = build_serp_prompt(query, breadth, learnings)
    raw = await asyncio.get_event_loop().run_in_executor(None, _llm_client, prompt, _llm_model)
    arr = extract_json_array(raw)
    # ensure type
    return [q.strip() for q in arr if isinstance(q, str)]

# Summarization step
async def generate_summary(source: str, content: str) -> str:
    prompt = build_summary_prompt(source, content)
    return await asyncio.get_event_loop().run_in_executor(None, _llm_client, prompt, _llm_model)

# Recursive deep research
async def deep_research(query: str, breadth: int = 4, depth: int = 2) -> Dict[str, List[str]]:
    learnings: List[str] = []
    visited: List[str] = []

    # 1) SERP queries
    serp = await generate_serp_queries(query, breadth, learnings)

    # 2) Retrieve and summarize
    for q in serp:
        res = await search_client.search(q)
        entries = res.get('data') or res.get('results') or res
        ids = [e.get('paperId') or e.get('id') or e for e in entries]
        visited.extend(ids)
        for pid in ids:
            content = await search_client.fetch_content(pid) if hasattr(search_client, 'fetch_content') else ''
            summary = await generate_summary(pid, content)
            learnings.append(summary)

    # 3) Recurse
    if depth > 1 and learnings:
        sub = await deep_research(' '.join(learnings), breadth, depth - 1)
        learnings.extend(sub['learnings'])
        visited.extend(sub['visitedUrls'])

    return {"learnings": learnings, "visitedUrls": visited}

# Final report and answer
def write_final_report(prompt: str, learnings: List[str], visited_urls: List[str]) -> str:
    rep = build_report_prompt(prompt, learnings, visited_urls)
    return query_llm(rep, _llm_model)

async def write_final_answer(prompt: str, learnings: List[str]) -> str:
    ans = build_answer_prompt(prompt, learnings)
    return await asyncio.get_event_loop().run_in_executor(None, _llm_client, ans, _llm_model)