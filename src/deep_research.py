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
import traceback

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
        # ask explicitly for fields we use downstream
        params = {"query": query, "limit": limit, "fields": "title,abstract,urls"}
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

# ---- Robust parser: supports multiple SDK shapes + salvage JSON from string ----
def _parse_json_lenient(completion_obj) -> Dict:
    """
    Try common places where structured JSON may live, then salvage from string.
    Returns a dict (possibly empty).
    """
    try:
        content = completion_obj.choices[0].message.content
        if isinstance(content, str):
            try:
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                # salvage {...} from string
                start = content.find("{")
                end = content.rfind("}")
                if start != -1 and end != -1 and end > start:
                    try:
                        parsed = json.loads(content[start:end+1])
                        if isinstance(parsed, dict):
                            return parsed
                    except Exception:
                        pass
        # Some SDKs: parsed object right on the message
        parsed_attr = getattr(completion_obj.choices[0].message, "parsed", None)
        if isinstance(parsed_attr, dict):
            return parsed_attr
    except Exception:
        pass

    try:
        out_list = getattr(completion_obj, "output", [])
        if out_list:
            out0 = out_list[0].content[0]
            if hasattr(out0, "parsed") and isinstance(out0.parsed, dict):
                return out0.parsed
            if hasattr(out0, "text") and isinstance(out0.text, str):
                txt = out0.text
                try:
                    parsed = json.loads(txt)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    start = txt.find("{")
                    end = txt.rfind("}")
                    if start != -1 and end != -1 and end > start:
                        try:
                            parsed = json.loads(txt[start:end+1])
                            if isinstance(parsed, dict):
                                return parsed
                        except Exception:
                            pass
    except Exception:
        pass

    return {}

# Small helpers for ORKG extraction
def _extract_orkg_items(result: Dict) -> List[Dict]:
    payload = result.get("payload") or {}
    items = payload.get("items") or []
    return items[:10] if isinstance(items, list) else []

def _item_urls(item: Dict) -> List[str]:
    urls = item.get("urls") or []
    if not isinstance(urls, list):
        return []
    # Deduplicate while preserving order
    seen = set()
    out = []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out

async def write_final_report(prompt: str, learnings: list, visited_urls: list) -> str:
    """Generate a final report in markdown format based on learnings."""

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

    parsed = _parse_json_lenient(completion)
    urls_section = "\n\n## Sources\n\n" + "\n".join(f"- {url}" for url in visited_urls)
    return (parsed.get("reportMarkdown") or "") + urls_section

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

    parsed = _parse_json_lenient(completion)
    return parsed.get("exactAnswer", "")

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

    parsed = _parse_json_lenient(result)
    queries = parsed.get("queries", [])
    return queries[:num_queries] if isinstance(queries, list) else []

async def process_serp_result(
    query: str,
    result: Dict,
    num_learnings: int = 3,
    num_followups: int = 3
):
    # local helper to safely pick first URL from ORKG item
    def _first_url_safe(item: Dict) -> str:
        urls = _item_urls(item)
        return urls[0] if urls else ""

    # Step 1: Extract and trim content (keep original 25_000 limit)
    if "data" in result:  # Firecrawl response
        contents = [
            trim_prompt(doc.get("markdown", ""), 25000)
            for doc in result.get("data", [])
            if doc.get("markdown")
        ]
    elif "payload" in result and "items" in result["payload"]:  # ORKG Ask API
        items = (result["payload"].get("items") or [])[:10]  # only top 10, tolerate None
        contents = []
        for item in items:
            title = (item.get("title") or "Untitled").strip()
            abstract = (item.get("abstract") or "").strip()
            url = _first_url_safe(item)
            contents.append(
                trim_prompt(f"{title}\n{abstract}\n{url}", 25000)
            )
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
    try:
        completion = _model_config_instance.generate_completion(
            messages=[
                {"role": "system", "content": system_prompt()},
                {"role": "user", "content": prompt}
            ],
            response_format=response_format
        )
        parsed = _parse_json_lenient(completion)
    except Exception as e:
        print("[WARN] process_serp_result completion/parse failed:", e)
        traceback.print_exc()
        parsed = {}

    # Step 5: Normalize + Non-inventing fallback from content only
    learnings = parsed.get("learnings", [])
    followups = parsed.get("followUpQuestions", [])

    if not isinstance(learnings, list):
        learnings = []
    if not isinstance(followups, list):
        followups = []

    if not learnings:
        fallback = []
        for c in contents[:num_learnings]:
            # pick first non-empty, non-URL line from actual content
            for ln in c.splitlines():
                s = ln.strip()
                if s and not s.lower().startswith("http"):
                    fallback.append(s[:240])
                    break
        learnings = fallback

    if not followups:
        followups = [
            f"What are the key subtopics within '{query}'?",
            f"Which sources disagree on '{query}' and why?",
            f"What exact metrics or dates are reported for '{query}'?",
        ][:num_followups]

    return {"learnings": learnings, "followUpQuestions": followups}

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
    report({"totalQueries": len(serp_queries) if serp_queries else 0,
            "currentQuery": serp_queries[0]["query"] if serp_queries else None})

    async def run_query(serp_query):
        try:
            result = await search_client.search(serp_query["query"])
            if "data" in result:
                urls = [doc.get("url") for doc in result.get("data", []) if doc.get("url")]
            elif "payload" in result and "items" in result["payload"]:
                items = _extract_orkg_items(result)
                url_list = []
                for it in items:
                    url_list.extend(_item_urls(it))
                # dedupe while preserving order
                seen = set()
                urls = [u for u in url_list if (u not in seen and not seen.add(u))]
            else:
                urls = []

            follow = await process_serp_result(serp_query["query"], result, num_followups=breadth)
            new_learnings = follow.get("learnings", [])
            new_followups = follow.get("followUpQuestions", [])

            updated_learnings = learnings + new_learnings
            updated_urls = visited_urls + urls

            if depth - 1 > 0:
                report({"currentDepth": depth - 1, "completedQueries": progress["completedQueries"] + 1})
                next_query = f"Previous research goal: {serp_query['researchGoal']}\nFollow-up: {'; '.join(map(str, (new_followups or [])))}"
                return await deep_research(next_query, breadth=breadth//2 or 1, depth=depth-1,
                                           learnings=updated_learnings, visited_urls=updated_urls, on_progress=on_progress)
            else:
                report({"currentDepth": 0, "completedQueries": progress["completedQueries"] + 1})
                return {"learnings": updated_learnings, "visitedUrls": updated_urls}

        except Exception as e:
            print("[ERROR] run_query failed:", e)
            traceback.print_exc()
            return {"learnings": [], "visitedUrls": []}

    results = await asyncio.gather(*(run_query(q) for q in serp_queries))
    combined = defaultdict(set)

    # keep accumulated context from higher levels
    combined["learnings"].update(learnings)
    combined["visitedUrls"].update(visited_urls)

    for res in results:
        combined["learnings"].update(res.get("learnings", []))
        urls_from_res = res.get("visitedUrls") or res.get("VisitedUrls") or []
        combined["visitedUrls"].update(urls_from_res)

    return {"learnings": list(combined["learnings"]), "visitedUrls": list(combined["visitedUrls"])}
