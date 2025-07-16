# File: src/deep_research_api.py

import os
import sys
import asyncio
import json
from typing import List, Dict, Optional, Callable
from collections import defaultdict
import aiohttp

from ai.prompt_utils import trim_prompt
from ai.llms import _model_config_instance
from prompt import system_prompt

sys.stdout.reconfigure(encoding='utf-8')


# —— paper retrieval clients —— #

class FirecrawlApp:
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "query": query,
            "limit": limit,
            "timeout": timeout,
            "scrapeOptions": {"formats": ["markdown"]}
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/search", json=body, headers=headers) as resp:
                print("resp.status", resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"{resp.status}, message={repr(text)}, url='{resp.url}'")
                return await resp.json()


class ORKGAskApp:
    def __init__(self, base_url: str = "https://api.ask.orkg.org/index"):
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        params = {"query": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/search", params=params) as resp:
                print("resp.status", resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"{resp.status}, message={repr(text)}, url='{resp.url}'")
                return await resp.json()


FIRECRAWL = "firecrawl"
ORKG      = "orkg"

def get_search_client(provider: str):
    if provider == ORKG:
        return ORKGAskApp()
    return FirecrawlApp(
        api_key=os.getenv("FIRECRAWL_KEY", ""),
        base_url=os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev/v1")
    )

search_client = get_search_client(os.getenv("RESEARCH_PROVIDER", "firecrawl"))
print(f"Search provider in use: {type(search_client).__name__}")


# —— generate SERP queries —— #

async def generate_serp_queries(
    query: str,
    num_queries: int = 3,
    learnings: Optional[List[str]] = None
) -> List[Dict[str, str]]:
    learnings_text = "\n".join(learnings) if learnings else ""
    prompt = (
        f"Given the following prompt from the user, generate a list of SERP queries to research the topic. "
        f"Return a maximum of {num_queries} queries.\n\n<prompt>{query}</prompt>\n\n"
        f"{f'Here are some learnings from previous research: {learnings_text}' if learnings else ''}"
    )

    response_format = {
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
                                "query":        {"type": "string"},
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

    completion = _model_config_instance.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user",   "content": prompt}
        ],
        response_format=response_format
    )
    parsed = json.loads(completion.choices[0].message.content)
    return parsed["queries"][:num_queries]


# —— process SERP result into learnings & follow-ups —— #

async def process_serp_result(
    query: str,
    result: Dict,
    num_learnings: int = 3,
    num_followups: int = 3
) -> Dict[str, List[str]]:
    # 1) collect raw contents
    if "data" in result:
        docs = result["data"]
        contents = [
            trim_prompt(doc["markdown"], 25000)
            for doc in docs if doc.get("markdown")
        ]
    elif "payload" in result and "items" in result["payload"]:
        items = result["payload"]["items"][:10]
        contents = [
            trim_prompt(
                f"{item.get('title','')}\n{item.get('abstract','')}\n{item.get('urls',[''])[0]}",
                25000
            )
            for item in items if item.get("title") or item.get("abstract")
        ]
    else:
        contents = []

    print(f"Ran {query}, found {len(contents)} contents")

    # 2) build schema‐driven summary prompt
    contents_blob = "\n".join(f"<content>\n{c}\n</content>" for c in contents)
    prompt = trim_prompt(
        f"""Given these contents from a SERP search for <query>{query}</query>,
generate up to {num_learnings} unique, concise learnings, and up to {num_followups} follow-up questions.

<contents>
{contents_blob}
</contents>"""
    )

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "serp_result_summary",
            "schema": {
                "type": "object",
                "properties": {
                    "learnings":         {"type": "array", "items": {"type": "string"}},
                    "followUpQuestions": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["learnings", "followUpQuestions"]
            }
        }
    }

    comp = _model_config_instance.generate_completion(
        messages=[
            {"role": "system",  "content": system_prompt()},
            {"role": "user",    "content": prompt}
        ],
        response_format=response_format
    )
    return json.loads(comp.choices[0].message.content)


# —— recursive deep research —— #

async def deep_research(
    query:      str,
    breadth:    int,
    depth:      int,
    learnings:  List[str] = None,
    visited:    List[str] = None,
    on_progress: Optional[Callable] = None
) -> Dict[str, List[str]]:
    learnings = learnings or []
    visited   = visited   or []

    serp_qs = await generate_serp_queries(query, breadth, learnings)
    for i, sq in enumerate(serp_qs, 1):
        print(f"[{i}/{len(serp_qs)}] Searching: {sq['query']}")
        res = await search_client.search(sq["query"])
        summary = await process_serp_result(
            sq["query"], res,
            num_learnings=breadth,
            num_followups=breadth
        )
        learnings.extend(summary["learnings"])
        visited.extend(res.get("urls", []))

        if depth > 1 and summary["followUpQuestions"]:
            follow_text = "; ".join(summary["followUpQuestions"])
            sub = await deep_research(
                follow_text, breadth // 2, depth - 1,
                learnings, visited, on_progress
            )
            learnings.extend(sub["learnings"])
            visited.extend(sub["visitedUrls"])

    return {"learnings": learnings, "visitedUrls": visited}


# —— final report & answer writers —— #

async def write_final_report(
    prompt:      str,
    learnings:   List[str],
    visited_urls: List[str]
) -> str:
    learnings_blob = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""Given the user's prompt below, write a detailed report (3+ pages) using ALL the learnings.

<prompt>{prompt}</prompt>

<learnings>
{learnings_blob}
</learnings>"""
    )
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_report",
            "schema": {
                "type":"object",
                "properties":{
                    "reportMarkdown":{
                        "type":"string",
                        "description":"Detailed report in Markdown"
                    }
                },
                "required":["reportMarkdown"]
            }
        }
    }
    comp = _model_config_instance.generate_completion(
        messages=[
            {"role":"system","content":system_prompt()},
            {"role":"user","content":full_prompt}
        ],
        response_format=response_format
    )
    parsed = json.loads(comp.choices[0].message.content)
    sources = "\n\n## Sources\n\n" + "\n".join(f"- {u}" for u in visited_urls)
    return parsed["reportMarkdown"] + sources


async def write_final_answer(
    prompt:    str,
    learnings: List[str]
) -> str:
    learnings_blob = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""Given the user's prompt below, write a concise answer using the learnings.

<prompt>{prompt}</prompt>

<learnings>
{learnings_blob}
</learnings>"""
    )
    response_format = {
        "type":"json_schema",
        "json_schema":{
            "name":"final_answer",
            "schema":{
                "type":"object",
                "properties":{
                    "exactAnswer":{
                        "type":"string",
                        "description":"Concise final answer"
                    }
                },
                "required":["exactAnswer"]
            }
        }
    }
    comp = _model_config_instance.generate_completion(
        messages=[
            {"role":"system","content":system_prompt()},
            {"role":"user","content":full_prompt}
        ],
        response_format=response_format
    )
    parsed = json.loads(comp.choices[0].message.content)
    return parsed["exactAnswer"]
