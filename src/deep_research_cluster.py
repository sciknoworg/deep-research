import os
import sys
import asyncio
import json
import time
import tempfile
import subprocess
import uuid
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
        body = {"query": query, "limit": limit, "timeout": timeout, "scrapeOptions": {"formats": ["markdown"]}}
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

async def call_llm_via_cluster(prompt: str, model: str = "deepseek", index: Optional[int] = None) -> str:
    index = call_huggingface_on_cluster(prompt, model_name=model, index=index)
    result = await asyncio.to_thread(wait_for_output_file, index=index)
    return result.get("response", "")

async def generate_cluster_completion(prompt: str, response_format: dict, model: str = "deepseek") -> dict:
    result = await call_llm_via_cluster(prompt, model=model)
    return json.loads(result)

async def write_final_report(prompt: str, learnings: list, visited_urls: list, model: str = "deepseek") -> str:
    learnings_text = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""Given the following prompt from the user, write a final report on the topic using the learnings from research. \
Make it as detailed as possible, aim for 3 or more pages, include ALL the learnings from research:

<prompt>{prompt}</prompt>

<learnings>
{learnings_text}
</learnings>"""
    )
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_report",
            "schema": {
                "type": "object",
                "properties": {
                    "reportMarkdown": {"type": "string"}
                },
                "required": ["reportMarkdown"]
            }
        }
    }
    parsed = await generate_cluster_completion(full_prompt, schema, model=model)
    urls_section = "\n\n## Sources\n\n" + "\n".join(f"- {url}" for url in visited_urls)
    return parsed["reportMarkdown"] + urls_section

async def write_final_answer(prompt: str, learnings: list, model: str = "deepseek") -> str:
    learnings_text = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""Given the following prompt from the user, write a final answer on the topic using the learnings from research. \
Follow the format specified in the prompt. Be concise and precise.

<prompt>{prompt}</prompt>

<learnings>
{learnings_text}
</learnings>"""
    )
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_answer",
            "schema": {
                "type": "object",
                "properties": {
                    "exactAnswer": {"type": "string"}
                },
                "required": ["exactAnswer"]
            }
        }
    }
    parsed = await generate_cluster_completion(full_prompt, schema, model=model)
    return parsed["exactAnswer"]

async def generate_serp_queries(prompt: str, num_queries: int = 3, learnings: Optional[List[str]] = None) -> List[Dict]:
    learnings_text = "\n".join(learnings or [])
    query_prompt = trim_prompt(f"""Given the user prompt and learnings, generate {num_queries} useful research SERP queries.
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
    parsed = await generate_cluster_completion(query_prompt, schema)
    return parsed["queries"][:num_queries]

async def process_serp_result(query: str, result: dict, num_learnings: int = 3, num_followups: int = 3):
    if "data" in result:
        contents = [trim_prompt(doc.get("markdown", ""), 25000) for doc in result["data"] if doc.get("markdown")]
    elif "payload" in result:
        items = result["payload"].get("items", [])
        contents = [trim_prompt(f"{i.get('title', '')}\n{i.get('abstract', '')}", 25000) for i in items]
    else:
        contents = []

    contents_block = "\n".join(f"<content>\n{c}\n</content>" for c in contents)
    summarization_prompt = trim_prompt(f"""Extract {num_learnings} key learnings and {num_followups} follow-up questions from:
<query>{query}</query>
<contents>{contents_block}</contents>""")
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
    parsed = await generate_cluster_completion(summarization_prompt, schema)
    return parsed

async def deep_research(prompt: str, breadth: int = 3, depth: int = 2, model: str = "deepseek", learnings=None, visited_urls=None) -> Dict:
    learnings = learnings or []
    visited_urls = visited_urls or []
    queries = await generate_serp_queries(prompt, num_queries=breadth, learnings=learnings)
    
    async def recurse(query: str, depth: int, research_goal: str):
        result = await search_client.search(query)
        if "data" in result:
            urls = list({d.get("url") for d in result["data"] if d.get("url")})
        elif "payload" in result:
            urls = list({i.get("urls", [None])[0] for i in result["payload"].get("items", []) if i.get("urls")})
        else:
            urls = []
        summary = await process_serp_result(query, result, num_learnings=breadth, num_followups=breadth)
        new_learnings = summary["learnings"]
        follow_ups = summary["followUpQuestions"]
        updated_learnings = learnings + new_learnings
        updated_urls = visited_urls + urls
        if depth > 1:
            next_query = f"{research_goal}\nFollow-up: {'; '.join(follow_ups)}"
            return await deep_research(next_query, breadth=breadth//2, depth=depth-1, model=model, learnings=updated_learnings, visited_urls=updated_urls)
        return {"learnings": updated_learnings, "visitedUrls": updated_urls}

    all_results = await asyncio.gather(*(recurse(q["query"], depth, q["researchGoal"]) for q in queries))
    all_learnings, all_urls = set(), set()
    for r in all_results:
        all_learnings.update(r["learnings"])
        all_urls.update(r["visitedUrls"])
    return {"learnings": list(all_learnings), "visitedUrls": list(all_urls)}
