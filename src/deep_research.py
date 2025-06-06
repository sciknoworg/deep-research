# deep_research.py

import os
import sys
import asyncio
from typing import List, Dict, Optional, Callable
from collections import defaultdict
import aiohttp
from ai.llms import _model_config_instance
from ai.prompt_utils import trim_prompt
import json

from prompt import system_prompt

from dotenv import load_dotenv
load_dotenv()

sys.stdout.reconfigure(encoding='utf-8')

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
            "scrapeOptions": {
                "formats": ["markdown"]
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/search", json=body, headers=headers
            ) as resp:
                print("resp.status")
                print(resp.status)                
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(
                        f"{resp.status}, message={repr(text)}, url='{str(resp.url)}'"
                    )

                return await resp.json()


class ORKGAskApp:
    def __init__(self, base_url: str = "https://api.ask.orkg.org/index"):
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        params = {"query": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/search", params=params) as resp:
                print("resp.status")
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"{resp.status}, message={repr(text)}, url='{str(resp.url)}'")
                return await resp.json()

FIRECRAWL = "firecrawl"
ORKG = "orkg"

def get_search_client(provider: str):
    if provider == ORKG:
        return ORKGAskApp()
    return FirecrawlApp(
        api_key=os.getenv("FIRECRAWL_KEY", ""),
        base_url=os.getenv("FIRECRAWL_BASE_URL", "https://api.firecrawl.dev/v1")
    )

search_client = get_search_client(os.getenv("RESEARCH_PROVIDER", "firecrawl"))

print(f"Search provider in use: {type(search_client).__name__}")

async def write_final_report(prompt: str, learnings: list, visited_urls: list) -> str:
    """Generate a final report in markdown format based on learnings."""

    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)

    #print("=====================")
    #print("learnings_string")
    #print(learnings_string)
    #print("=====================")

    full_prompt = trim_prompt(
        f"""Given the following prompt from the user, write a final report on the topic using the learnings from research. 
Make it as detailed as possible, aim for 3 or more pages, include ALL the learnings from research:

<prompt>{prompt}</prompt>

Here are all the learnings from previous research:

<learnings>
{learnings_string}
</learnings>"""
    )

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_report",
            "schema": {
                "type": "object",
                "properties": {
                    "reportMarkdown": {
                        "type": "string",
                        "description": "Final report on the topic in Markdown"
                    }
                },
                "required": ["reportMarkdown"]
            }
        }
    }

    completion = _model_config_instance.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": full_prompt}
        ],
        response_format=response_format
    )

    parsed = json.loads(completion.choices[0].message.content)
    urls_section = "\n\n## Sources\n\n" + "\n".join(f"- {url}" for url in visited_urls)
    return parsed["reportMarkdown"] + urls_section

async def write_final_answer(prompt: str, learnings: list) -> str:
    """Generate a short and concise final answer based on learnings."""

    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)

    full_prompt = trim_prompt(
        f"""Given the following prompt from the user, write a final answer on the topic using the learnings from research. 
Follow the format specified in the prompt. Do not yap or babble or include any other text than the answer besides the format specified in the prompt. 
Keep the answer as concise as possible—usually it should be just a few words or maximum a sentence. Try to follow the format specified in the prompt 
(for example, if the prompt is using LaTeX, the answer should be in LaTeX. If the prompt gives multiple answer choices, the answer should be one of the choices).

<prompt>{prompt}</prompt>

Here are all the learnings from research on the topic that you can use to help answer the prompt:

<learnings>
{learnings_string}
</learnings>"""
    )

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "final_answer",
            "schema": {
                "type": "object",
                "properties": {
                    "exactAnswer": {
                        "type": "string",
                        "description": "The final answer, concise and precise."
                    }
                },
                "required": ["exactAnswer"]
            }
        }
    }

    completion = _model_config_instance.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": full_prompt}
        ],
        response_format=response_format
    )

    parsed = json.loads(completion.choices[0].message.content)
    return parsed["exactAnswer"]

async def generate_serp_queries(query: str, num_queries: int = 3, learnings: Optional[List[str]] = None):

    learnings_text = "\n".join(learnings) if learnings else ""
    prompt = (
        f"Given the following prompt from the user, generate a list of SERP queries to research the topic. "
        f"Return a maximum of {num_queries} queries. \n\n<prompt>{query}</prompt>\n\n"
        f"{f'Here are some learnings from previous research: {learnings_text}' if learnings else ''}"
    )

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

    result = _model_config_instance.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt}
        ],
        response_format=schema
    )

    parsed = json.loads(result.choices[0].message.content)
    return parsed["queries"][:num_queries]


async def process_serp_result(
    query: str,
    result: Dict,
    num_learnings: int = 3,
    num_followups: int = 3
):
    # Step 1: Extract and trim content
    if "data" in result:  # Firecrawl response
        contents = [
            trim_prompt(doc.get("markdown", ""), 25000)
            for doc in result.get("data", [])
            if doc.get("markdown")
        ]
    elif "payload" in result and "items" in result["payload"]:  # ORKG Ask API
        items = result["payload"]["items"][:10]  # only top 10
        contents = [
            trim_prompt(
                f"{item.get('title', '')}\n{item.get('abstract', '')}\n{item.get('urls', [''])[0]}",
                25000
            )
            for item in items
            if item.get("title") or item.get("abstract")
        ]
    else:
        contents = []
    print(f"Ran {query}, found {len(contents)} contents")

    # Step 2: Build formatted prompt
    contents_text = "\n".join(
        f"<content>\n{c}\n</content>" for c in contents
    )

    prompt = trim_prompt(
        f"""Given the following contents from a SERP search for the query <query>{query}</query>, 
generate a list of learnings from the contents. Return a maximum of {num_learnings} learnings, 
but feel free to return less if the contents are clear. Make sure each learning is unique and not 
similar to each other. The learnings should be concise and to the point, as detailed and information 
dense as possible. Make sure to include any entities like people, places, companies, products, things, 
etc in the learnings, as well as any exact metrics, numbers, or dates. The learnings will be used 
to research the topic further.

Also return a list of follow-up questions to research the topic further. 
Return a maximum of {num_followups} follow-up questions, but fewer is okay if the content is narrow.

<contents>
{contents_text}
</contents>"""
    )

    # Step 3: Prepare schema for structured output
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "serp_result_summary",
            "schema": {
                "type": "object",
                "properties": {
                    "learnings": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": f"List of learnings, max of {num_learnings}"
                    },
                    "followUpQuestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": f"List of follow-up questions, max of {num_followups}"
                    }
                },
                "required": ["learnings", "followUpQuestions"]
            }
        }
    }

    # Step 4: Make completion request
    completion = _model_config_instance.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt}
        ],
        response_format=response_format
    )

    # Step 5: Parse and return the result
    parsed = json.loads(completion.choices[0].message.content)
    #print(f"Created {len(parsed['learnings'])} learnings")
    return parsed

async def deep_research(query: str, breadth: int, depth: int, learnings=None, visited_urls=None, on_progress: Optional[Callable] = None):
    learnings = learnings or []
    visited_urls = visited_urls or []
    progress = {
        "currentDepth": depth,
        "totalDepth": depth,
        "currentBreadth": breadth,
        "totalBreadth": breadth,
        "totalQueries": 0,
        "completedQueries": 0,
        "currentQuery": None
    }

    def report(update):
        progress.update(update)
        if on_progress:
            on_progress(progress)

    serp_queries = await generate_serp_queries(query, breadth, learnings)
    report({"totalQueries": len(serp_queries), "currentQuery": serp_queries[0]["query"]})

    async def run_query(serp_query):
        #print("serp_query")
        #print(serp_query)
        try:
            result = await search_client.search(serp_query["query"])
            #print("============================")
            #print("result")
            #print("payload" in result)
            #print(result)
            #print("============================")
            if "data" in result:
                urls = list({doc.get("url") for doc in result.get("data", []) if doc.get("url")})
            elif "payload" in result and "items" in result["payload"]:
                #print(result)
                items = result["payload"]["items"][:10]  # Only the top 10 used in summarization
                urls = list({item.get("urls", [None])[0] for item in items if item.get("urls")})
                #print("============================")
                #print(urls)
                #print("============================")
            else:
                urls = []
            #print("============================")
            #print(serp_query["query"])
            #print("============================")
            follow = await process_serp_result(serp_query["query"], result, num_followups=breadth)
            new_learnings = follow["learnings"]
            new_followups = follow["followUpQuestions"]

            updated_learnings = learnings + new_learnings
            updated_urls = visited_urls + urls

            if depth - 1 > 0:
                report({"currentDepth": depth - 1, "completedQueries": progress["completedQueries"] + 1})
                next_query = f"Previous research goal: {serp_query['researchGoal']}\nFollow-up: {'; '.join(new_followups)}"
                return await deep_research(next_query, breadth=breadth//2, depth=depth-1, learnings=updated_learnings, visited_urls=updated_urls, on_progress=on_progress)
            else:
                report({"currentDepth": 0, "completedQueries": progress["completedQueries"] + 1})
                return {"learnings": updated_learnings, "visitedUrls": updated_urls}
        except Exception as e:
            return {"learnings": [], "visitedUrls": []}

    results = await asyncio.gather(*(run_query(q) for q in serp_queries))
    combined = defaultdict(set)
    for res in results:
        combined["learnings"].update(res["learnings"])
        combined["visitedUrls"].update(res["visitedUrls"])
    return {"learnings": list(combined["learnings"]), "visitedUrls": list(combined["visitedUrls"])}
