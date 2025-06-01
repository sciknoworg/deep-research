import os
import sys
import asyncio
from typing import List, Dict, Optional, Callable
from collections import defaultdict
import aiohttp
from ai.llms import call_huggingface_on_cluster, wait_for_output_file
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

def build_prompt_generate_serp(query: str, num_queries: int, learnings: Optional[List[str]]) -> str:
    learnings_text = "\n".join(learnings) if learnings else ""
    return trim_prompt(
        f"Given the following prompt from the user, generate a list of SERP queries to research the topic. "
        f"Return a maximum of {num_queries} queries.\n\n<prompt>{query}</prompt>\n\n"
        f"{f'Here are some learnings from previous research: {learnings_text}' if learnings else ''}"
    )

def build_prompt_process_serp(query: str, contents_text: str, num_learnings: int, num_followups: int) -> str:
    return trim_prompt(
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

async def generate_serp_queries_cluster(query: str, num_queries: int = 3, learnings: Optional[List[str]] = None, model: str = "deepseek"):
    prompt = build_prompt_generate_serp(query, num_queries, learnings)
    call_huggingface_on_cluster(prompt, model_name=model, index=999)
    result = await wait_for_output_file(index=999)
    parsed = json.loads(result.get("response", "{}"))
    return parsed.get("queries", [])[:num_queries]

async def process_serp_result_cluster(query: str, result: Dict, model: str, num_learnings: int = 3, num_followups: int = 3):
    if "data" in result:
        contents = [
            trim_prompt(doc.get("markdown", ""), 25000)
            for doc in result.get("data", [])
            if doc.get("markdown")
        ]
    elif "payload" in result and "items" in result["payload"]:
        items = result["payload"]["items"][:10]
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

    contents_text = "\n".join(f"<content>\n{c}\n</content>" for c in contents)
    prompt = build_prompt_process_serp(query, contents_text, num_learnings, num_followups)

    call_huggingface_on_cluster(prompt, model_name=model, index=998)
    result = await wait_for_output_file(index=998)
    parsed = json.loads(result.get("response", "{}"))
    return parsed

async def write_final_report_cluster(prompt: str, learnings: list, visited_urls: list, model: str):
    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)
    full_prompt = trim_prompt(
        f"""Given the following prompt from the user, write a final report on the topic using the learnings from research. 
Make it as detailed as possible, aim for 3 or more pages, include ALL the learnings from research:

<prompt>{prompt}</prompt>

Here are all the learnings from previous research:

<learnings>
{learnings_string}
</learnings>"""
    )
    call_huggingface_on_cluster(full_prompt, model_name=model, index=997)
    result = await wait_for_output_file(index=997)
    parsed = json.loads(result.get("response", "{}"))
    urls_section = "\n\n## Sources\n\n" + "\n".join(f"- {url}" for url in visited_urls)
    return parsed.get("reportMarkdown", "") + urls_section

async def write_final_answer_cluster(prompt: str, learnings: list, model: str):
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
    call_huggingface_on_cluster(full_prompt, model_name=model, index=996)
    result = await wait_for_output_file(index=996)
    parsed = json.loads(result.get("response", "{}"))
    return parsed.get("exactAnswer", "")
