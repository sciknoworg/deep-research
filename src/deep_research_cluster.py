import os
import sys
import asyncio
import json
from typing import List, Dict, Optional, Callable
from collections import defaultdict
import aiohttp

from dotenv import load_dotenv
from ai.prompt_utils import trim_prompt
from ai.llms import call_huggingface_on_cluster, wait_for_output_file
from prompt import system_prompt

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

FIRECRAWL = "firecrawl"
ORKG = "orkg"

class FirecrawlApp:
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {
            "query": query, "limit": limit, "timeout": timeout,
            "scrapeOptions": {"formats": ["markdown"]}
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/search", json=body, headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(f"{resp.status}, {await resp.text()}")
                return await resp.json()

class ORKGAskApp:
    def __init__(self, base_url: str = "https://api.ask.orkg.org/index"):
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        params = {"query": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/search", params=params) as resp:
                if resp.status != 200:
                    raise Exception(f"{resp.status}, {await resp.text()}")
                return await resp.json()

def get_search_client(provider: str):
    if provider == ORKG:
        return ORKGAskApp()
    return FirecrawlApp(api_key=os.getenv("FIRECRAWL_KEY", ""))

search_client = get_search_client(os.getenv("RESEARCH_PROVIDER", "firecrawl"))

async def call_indexed(prompt: str, schema: dict, model: str, index: int):
    call_huggingface_on_cluster(prompt, model_name=model, index=index)
    result = await wait_for_output_file(index=index)
    return json.loads(result.get("response", "{}"))

async def write_final_report(prompt: str, learnings: list, visited_urls: list, model: str = "deepseek", index: int = 3) -> str:
    prompt_text = trim_prompt(f"""{system_prompt()}
Given the following prompt from the user, write a final report using ALL learnings:
<prompt>{prompt}</prompt>
<learnings>{chr(10).join(f'<learning>{l}</learning>' for l in learnings)}</learnings>""")
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_report",
            "schema": {
                "type": "object",
                "properties": {"reportMarkdown": {"type": "string"}},
                "required": ["reportMarkdown"]
            }
        }
    }
    parsed = await call_indexed(prompt_text, schema, model, index)
    urls_section = "\n\n## Sources\n\n" + "\n".join(f"- {url}" for url in visited_urls)
    return parsed.get("reportMarkdown", "") + urls_section

async def write_final_answer(prompt: str, learnings: list, model: str = "deepseek", index: int = 4) -> str:
    prompt_text = trim_prompt(f"""{system_prompt()}
Based on the following prompt and learnings, give a short final answer:
<prompt>{prompt}</prompt>
<learnings>{chr(10).join(f'<learning>{l}</learning>' for l in learnings)}</learnings>""")
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_answer",
            "schema": {
                "type": "object",
                "properties": {"exactAnswer": {"type": "string"}},
                "required": ["exactAnswer"]
            }
        }
    }
    parsed = await call_indexed(prompt_text, schema, model, index)
    return parsed.get("exactAnswer", "")

async def generate_serp_queries(prompt: str, learnings: Optional[List[str]], num_queries: int, model: str, index: int = 2):
    learnings_text = "\n".join(learnings or [])
    query_prompt = trim_prompt(f"""{system_prompt()}
Generate up to {num_queries} research SERP queries for this:
<prompt>{prompt}</prompt>
<learnings>{learnings_text}</learnings>""")
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "serp_queries",
            "schema": {
                "type": "object",
                "properties": {
                    "queries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "researchGoal": {"type": "string"}
                            },
                            "required": ["query", "researchGoal"]
                        }
                    }
                },
                "required": ["queries"]
            }
        }
    }
    parsed = await call_indexed(query_prompt, schema, model, index)
    return parsed["queries"][:num_queries]

async def process_serp_result(query: str, result: Dict, model: str, index: int, num_learnings: int = 3, num_followups: int = 3):
    if "data" in result:
        contents = [trim_prompt(doc.get("markdown", ""), 25000) for doc in result["data"] if doc.get("markdown")]
    elif "payload" in result:
        items = result["payload"].get("items", [])
        contents = [trim_prompt(f"{i.get('title', '')}\n{i.get('abstract', '')}", 25000) for i in items]
    else:
        contents = []

    contents_block = "\n".join(f"<content>\n{c}\n</content>" for c in contents)
    summarization_prompt = trim_prompt(f"""{system_prompt()}
Summarize {query} from:
{contents_block}""")
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "serp_summary",
            "schema": {
                "type": "object",
                "properties": {
                    "learnings": {"type": "array", "items": {"type": "string"}},
                    "followUpQuestions": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["learnings", "followUpQuestions"]
            }
        }
    }
    parsed = await call_indexed(summarization_prompt, schema, model, index)
    return parsed

async def deep_research(prompt: str, breadth: int, depth: int, model: str, learnings=None, visited_urls=None, index: int = 2):
    learnings = learnings or []
    visited_urls = visited_urls or []
    queries = await generate_serp_queries(prompt, learnings, breadth, model, index=index)

    async def recurse(query: str, depth: int, goal: str):
        result = await search_client.search(query)
        urls = list({doc.get("url") for doc in result.get("data", []) if doc.get("url")})
        summary = await process_serp_result(query, result, model, index=index+1)
        new_learnings = summary["learnings"]
        new_followups = summary["followUpQuestions"]
        updated_learnings = learnings + new_learnings
        updated_urls = visited_urls + urls
        if depth > 1:
            next_query = f"{goal}\nFollow-up: {'; '.join(new_followups)}"
            return await deep_research(next_query, breadth // 2, depth - 1, model, updated_learnings, updated_urls, index=index+2)
        return {"learnings": updated_learnings, "visitedUrls": updated_urls}

    results = await asyncio.gather(*(recurse(q["query"], depth, q["researchGoal"]) for q in queries))
    final_learnings = set().union(*(r["learnings"] for r in results))
    final_urls = set().union(*(r["visitedUrls"] for r in results))
    return {"learnings": list(final_learnings), "visitedUrls": list(final_urls)}
