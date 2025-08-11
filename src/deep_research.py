# deep_research.py

import os
import sys
import asyncio
from typing import List, Dict, Optional, Callable
import aiohttp
import json
import re
from ai.llms import _model_config_instance
from ai.prompt_utils import trim_prompt
from prompt import system_prompt
from dotenv import load_dotenv

load_dotenv()

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------
# Helpers
# ---------------------------------------

def _uniq_preserve(seq):
    """Deduplicate while preserving original order."""
    seen = set()
    out = []
    for x in seq:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out

def _build_sources_block(urls: List[str]):
    """
    Build the numbered source catalog from URLs (AS-IS, no normalization).
    Returns: (sources_block_str, urls_list_as_is)
    """
    urls_list = urls or []
    lines = [f"[{i}] {u}" for i, u in enumerate(urls_list, 1)]
    return "\n".join(lines), urls_list

def _strip_existing_references(md: str) -> str:
    """
    Remove any trailing '## References' section to avoid parsing [n] from it.
    Case-insensitive, matches '## References' or deeper headings.
    """
    if not md:
        return md
    m = re.search(r'(?im)^#{2,}\s*references?\b.*$', md)
    return md[:m.start()] if m else md

def _extract_citation_numbers_in_appearance_order(md_body: str) -> List[int]:
    """Return distinct citation numbers in the order they first appear (e.g., [17], then [40], ...)."""
    seen = set()
    order = []
    for m in re.finditer(r"\[([0-9,\s]+)\]", md_body):
        for token in m.group(1).split(","):
            t = token.strip()
            if t.isdigit():
                n = int(t)
                if n not in seen:
                    seen.add(n)
                    order.append(n)
    return order

def _renumber_citations_in_text(md_body: str, mapping: dict[int, int]) -> str:
    """Replace [old] (and lists) with [new] per mapping, preserving commas/spaces."""
    def repl(m):
        parts = []
        for token in m.group(1).split(","):
            raw = token
            t = token.strip()
            if t.isdigit():
                newn = mapping.get(int(t))
                parts.append(str(newn) if newn is not None else t)
            else:
                parts.append(raw)
        return "[" + ", ".join(p.strip() for p in parts) + "]"
    return re.sub(r"\[([0-9,\s]+)\]", repl, md_body)

# --- OPTIONAL: ultra-light URL sanitizer (on by default in add_citations below) ---
def _sanitize_url(u: str) -> str:
    if not u:
        return u
    return u.strip().strip(".,);]")

# ---------------------------------------
# One-shot public API: add_citations
# ---------------------------------------

def add_citations(
    report_md_raw: str,
    visited_urls: List[str],
    *,
    order_by: str = "numeric",   # "numeric" (default) or "appearance"
    renumber: bool = True,        # True = remap in-text to [1..N] in chosen order
    sanitize_urls: bool = True,   # True = trim trivial trailing punctuation
) -> str:
    """
    Build a References section aligned with in-text [n] citations.

    Steps:
      - remove any existing '## References' section from the model output
      - parse [n] citations only from the body
      - build catalog from visited_urls (as-is)
      - create '## References' with only actually cited sources (fallback: full catalog if none cited)
      - optionally renumber in-text citations to [1..N] by selected ordering
    """
    # 1) Body only
    body = _strip_existing_references(report_md_raw or "").rstrip()

    # 2) Collect used citation numbers
    used_nums = _extract_citation_numbers_in_appearance_order(body)
    if order_by == "numeric":
        used_nums = sorted(used_nums)

    # 3) Optional URL sanitize
    urls_list = list(visited_urls or [])
    if sanitize_urls:
        urls_list = [_sanitize_url(u) for u in urls_list]

    # 4) Build output
    if not used_nums:
        # No citations in text → fallback to full catalog (as-is)
        catalog_lines = [f"[{i}] {u}" for i, u in enumerate(urls_list, 1)]
        references = "\n\n## References\n\n" + "\n".join(catalog_lines) if urls_list else ""
        return body + references

    # Filter to only cited numbers that exist
    used_nums = [n for n in used_nums if 1 <= n <= len(urls_list)]

    if renumber:
        # Map old -> new by selected order (1..N), rewrite text and references
        mapping = {old: new for new, old in enumerate(used_nums, 1)}
        body = _renumber_citations_in_text(body, mapping)
        ref_lines = [f"[{mapping[old]}] {urls_list[old-1]}" for old in used_nums]
    else:
        # Keep original numbers; list references in chosen order
        ref_lines = [f"[{old}] {urls_list[old-1]}" for old in used_nums]

    references = "\n\n## References\n\n" + "\n".join(ref_lines)
    return body + references

# ---------------------------------------
# Search clients
# ---------------------------------------

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
                print("resp.status")
                print(resp.status)
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"{resp.status}, message={repr(text)}, url='{str(resp.url)}'")
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

# ---------------------------------------
# Final report
# ---------------------------------------

async def write_final_report(prompt: str, learnings: list, visited_urls: list) -> str:
    """
    Generate the report via LLM (with citation style instructions) and then call add_citations()
    to set a consistent References section (only used sources, or full catalog as fallback).
    """
    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)

    # Catalog (only for the prompt display; add_citations will rebuild independently)
    sources_block, urls_list = _build_sources_block(visited_urls)
    n_sources = len(urls_list)

    full_prompt = trim_prompt(
        f"""
You are writing a scholarly report. You MUST ONLY cite from the sources listed below.

Citation style (important):
- After every claim requiring evidence, place citations as [n] or [n,m] according to the numbered catalog below.
- DO NOT invent sources and DO NOT use numbers outside 1..{n_sources}.
- No bare URLs in the text. No footnote format. Only square brackets [ ].
- If something cannot be sourced, explicitly write [citation needed].

Structure:
1) Introduction (brief, contextual)
2) Main body (precise, fact-based; insert [n] wherever a source backs a statement)
3) Conclusion (short)

Material:
=== RESEARCH QUESTION ===
{prompt}

=== LEARNINGS (condensed) ===
{learnings_string}

=== SOURCES (numbered catalog) ===
{sources_block}

Task:
Produce the report in Markdown. At the end, append a
## References
section containing EXACTLY the above catalog 1..{n_sources} in identical order and formatting.
"""
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
    report_md_raw = parsed["reportMarkdown"].rstrip()

    # Single call that does everything: strip existing refs, parse [n] from body, build final refs
    # NOTE: now using numeric ordering + renumber + sanitization, as requested
    return add_citations(
        report_md_raw,
        visited_urls,
        order_by="numeric",   # numeric ordering
        renumber=True,        # rewrite in-text to [1..N] in numeric order
        sanitize_urls=True    # trim trivial trailing punctuation on URLs
    )

# ---------------------------------------
# Short final answer (unchanged)
# ---------------------------------------

async def write_final_answer(prompt: str, learnings: list) -> str:
    """Generate a short and concise final answer based on learnings."""
    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)

    full_prompt = trim_prompt(
        f"""Given the following prompt from the user, write a final answer on the topic using the learnings from research. 
Follow the format specified in the prompt. Keep it concise — usually just a few words or one sentence.

<prompt>{prompt}</prompt>

Here are all the learnings from research that you can use:

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

# ---------------------------------------
# SERP query generator (unchanged)
# ---------------------------------------

async def generate_serp_queries(query: str, num_queries: int = 3, learnings: Optional[List[str]] = None):
    learnings_text = "\n".join(learnings) if learnings else ""
    prompt = (
        f"Given the following prompt, generate up to {num_queries} SERP queries to research the topic.\n"
        f"<prompt>{query}</prompt>\n\n"
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

# ---------------------------------------
# SERP result processing (unchanged)
# ---------------------------------------

async def process_serp_result(query: str, result: Dict, num_learnings: int = 3, num_followups: int = 3):
    if "data" in result:  # Firecrawl response
        contents = [
            trim_prompt(doc.get("markdown", ""), 25000)
            for doc in result.get("data", [])
            if doc.get("markdown")
        ]
    elif "payload" in result and "items" in result["payload"]:  # ORKG Ask API
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
    prompt = trim_prompt(
        f"""Given the following contents from a SERP search for the query <query>{query}</query>, 
generate up to {num_learnings} unique, detailed learnings and up to {num_followups} follow-up questions.

<contents>
{contents_text}
</contents>"""
    )

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "serp_result_summary",
            "schema": {
                "type": "object",
                "properties": {
                    "learnings": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "followUpQuestions": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["learnings", "followUpQuestions"]
            }
        }
    }

    completion = _model_config_instance.generate_completion(
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt}
        ],
        response_format=response_format
    )

    parsed = json.loads(completion.choices[0].message.content)
    return parsed

# ---------------------------------------
# Main workflow – URLs in order, no sets
# ---------------------------------------

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
    if serp_queries:
        report({"totalQueries": len(serp_queries), "currentQuery": serp_queries[0]["query"]})
    else:
        report({"totalQueries": 0, "currentQuery": None})

    async def run_query(serp_query):
        try:
            result = await search_client.search(serp_query["query"])

            # Extract URLs in order, then light dedup to avoid exact repeats
            if "data" in result:
                urls_raw = [doc.get("url") for doc in result.get("data", []) if doc.get("url")]
                urls = _uniq_preserve(urls_raw)
            elif "payload" in result and "items" in result["payload"]:
                items = result["payload"]["items"][:10]
                urls_raw = [(item.get("urls") or [None])[0] for item in items if item.get("urls")]
                urls = _uniq_preserve(urls_raw)
            else:
                urls = []

            follow = await process_serp_result(serp_query["query"], result, num_followups=breadth)
            new_learnings = follow["learnings"]
            new_followups = follow["followUpQuestions"]

            updated_learnings = _uniq_preserve(learnings + new_learnings)
            updated_urls = _uniq_preserve(visited_urls + urls)

            if depth - 1 > 0:
                report({"currentDepth": depth - 1, "completedQueries": progress["completedQueries"] + 1})
                next_query = f"Previous research goal: {serp_query['researchGoal']}\nFollow-up: {'; '.join(new_followups)}"
                return await deep_research(
                    next_query,
                    breadth=breadth//2,
                    depth=depth-1,
                    learnings=updated_learnings,
                    visited_urls=updated_urls,
                    on_progress=on_progress
                )
            else:
                report({"currentDepth": 0, "completedQueries": progress["completedQueries"] + 1})
                return {"learnings": updated_learnings, "visitedUrls": updated_urls}
        except Exception:
            return {"learnings": [], "visitedUrls": []}

    results = await asyncio.gather(*(run_query(q) for q in serp_queries)) if serp_queries else []

    all_learnings = []
    all_urls = []
    for res in results:
        all_learnings.extend(res["learnings"])
        all_urls.extend(res["visitedUrls"])

    all_learnings = _uniq_preserve(all_learnings)
    all_urls = _uniq_preserve(all_urls)

    return {"learnings": all_learnings, "visitedUrls": all_urls}
