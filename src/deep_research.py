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

# -----------------------------------------------------------------------------
# Feature flags (from .env)
# -----------------------------------------------------------------------------
def _env_flag(name: str, default: bool = False) -> bool:
    val = os.getenv(name, "").strip().lower()
    if not val:
        return default
    return val in ("1", "true", "yes", "on")

USE_SOURCE_RANKING = _env_flag("USE_SOURCE_RANKING", False)        # rank & prioritize before writing
SHOW_RANKING_SECTION = _env_flag("SHOW_RANKING_SECTION", False)    # append ranking list after References

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
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
    Build the numbered source catalog from URLs (AS-IS).
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

def _renumber_citations_in_text(md_body: str, mapping: Dict[int, int]) -> str:
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

def _sanitize_url(u: str) -> str:
    if not u:
        return u
    return u.strip().strip(".,);]")

# -----------------------------------------------------------------------------
# Citations / References (URLs only)
# -----------------------------------------------------------------------------
def _build_citations_bundle(
    report_md_raw: str,
    visited_urls: List[str],
    *,
    order_by: str = "numeric",   # "appearance" or "numeric"
    renumber: bool = True,
    sanitize_urls: bool = True,
) -> Dict:
    """
    Build final Markdown with a cleaned References section that includes ONLY actually cited sources.
    Fallback: if no citations in the text, list the full catalog.
    Returns a bundle with final_md, mapping, urls_list, etc.
    """
    # 1) Body only
    body = _strip_existing_references(report_md_raw or "").rstrip()

    # 2) Collect used citation numbers
    used_nums = _extract_citation_numbers_in_appearance_order(body)
    if order_by == "numeric":
        used_nums = sorted(used_nums)

    # 3) Optionally sanitize URLs
    urls_list = list(visited_urls or [])
    if sanitize_urls:
        urls_list = [_sanitize_url(u) for u in urls_list]

    # 4) If no citations in text → fallback to full catalog (as-is)
    if not used_nums:
        catalog_lines = [f"[{i}] {u}" for i, u in enumerate(urls_list, 1)]
        references = "\n\n## References\n\n" + "\n".join(catalog_lines) if urls_list else ""
        return {
            "final_md": body + references,
            "body": body,
            "references_lines": catalog_lines,
            "used_nums_original": [],
            "mapping": None,
            "urls_list": urls_list
        }

    # Keep only valid numbers that exist
    used_nums = [n for n in used_nums if 1 <= n <= len(urls_list)]

    # 5) Renumber or keep original
    mapping = None
    if renumber:
        # Map old -> new by chosen order (1..N)
        mapping = {old: new for new, old in enumerate(used_nums, 1)}
        body = _renumber_citations_in_text(body, mapping)
        ref_lines = [f"[{mapping[old]}] {urls_list[old-1]}" for old in used_nums]
    else:
        # Keep original numbers; list references in chosen order
        ref_lines = [f"[{old}] {urls_list[old-1]}" for old in used_nums]

    references = "\n\n## References\n\n" + "\n".join(ref_lines)
    return {
        "final_md": body + references,
        "body": body,
        "references_lines": ref_lines,
        "used_nums_original": used_nums,
        "mapping": mapping,
        "urls_list": urls_list
    }

def add_citations(
    report_md_raw: str,
    visited_urls: List[str],
    *,
    order_by: str = "numeric",   # "appearance" or "numeric"
    renumber: bool = True,
    sanitize_urls: bool = True,
) -> str:
    bundle = _build_citations_bundle(
        report_md_raw,
        visited_urls,
        order_by=order_by,
        renumber=renumber,
        sanitize_urls=sanitize_urls
    )
    return bundle["final_md"]

# -----------------------------------------------------------------------------
# Optional: Paper ranking (LLM-only, based on URLs + learnings)
# -----------------------------------------------------------------------------
async def rank_papers(
    research_question: str,
    learnings: List[str],
    visited_urls: List[str],
    top_k: int = 12
) -> List[Dict]:
    urls = visited_urls or []
    if not urls:
        return []

    learnings_str = "\n".join(f"- {l}" for l in (learnings or []))
    catalog_lines = "\n".join(f"[{i}] {u}" for i, u in enumerate(urls, 1))
    k = min(top_k, len(urls))

    prompt = trim_prompt(f"""
You are ranking sources for usefulness to answer a research question.
You CANNOT browse. Base your judgement only on the URL cues (domain/path/doi),
and the provided learnings.

Research question:
{research_question}

Learnings:
{learnings_str}

Source catalog:
{catalog_lines}

Scoring (0-100):
- Topical fit (50)
- Likely credibility/rigor (25)
- Likely citability (15)
- Recency/relevance (10)

Return JSON: ranked: [{{index:int, url:string, score:number, reason:string}}], sorted DESC, limit {k}.
""")

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "paper_ranking",
            "schema": {
                "type": "object",
                "properties": {
                    "ranked": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "index": {"type": "integer"},
                                "url": {"type": "string"},
                                "score": {"type": "number"},
                                "reason": {"type": "string"}
                            },
                            "required": ["index", "score"]
                        }
                    }
                },
                "required": ["ranked"]
            }
        }
    }

    result = _model_config_instance.generate_completion(
        messages=[{"role": "system", "content": system_prompt()},
                  {"role": "user", "content": prompt}],
        response_format=schema
    )

    try:
        parsed = json.loads(result.choices[0].message.content)
        ranked = parsed.get("ranked", [])
        ranked = [r for r in ranked if isinstance(r.get("index"), int) and 1 <= r["index"] <= len(urls)][:k]
        for r in ranked:
            if not r.get("url"):
                r["url"] = urls[r["index"] - 1]
        ranked.sort(key=lambda x: x.get("score", 0), reverse=True)
        return ranked
    except Exception:
        return []

# -----------------------------------------------------------------------------
# Search clients
# -----------------------------------------------------------------------------
class FirecrawlApp:
    def __init__(self, api_key: str, base_url: str = "https://api.firecrawl.dev/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def search(self, query: str, timeout: int = 15000, limit: int = 10):
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"query": query, "limit": limit, "timeout": timeout, "scrapeOptions": {"formats": ["markdown"]}}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/search", json=body, headers=headers) as resp:
                print("resp.status"); print(resp.status)
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
                print("resp.status"); print(resp.status)
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

# -----------------------------------------------------------------------------
# Final report (ranking optional; references are URLs only)
# -----------------------------------------------------------------------------
async def write_final_report(prompt: str, learnings: list, visited_urls: list) -> str:
    """
    - (optional) ranks sources & guides prioritization if USE_SOURCE_RANKING
    - writes report (LLM)
    - builds numeric, renumbered citations (URLs only, sanitized)
    - (optional) appends "Source Usefulness Ranking" after References if SHOW_RANKING_SECTION
    """
    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in (learnings or []))
    sources_block, urls_list = _build_sources_block(visited_urls)
    n_sources = len(urls_list)

    ranked = []
    priority_block = "[none]"
    if USE_SOURCE_RANKING and visited_urls:
        ranked = await rank_papers(prompt, learnings or [], visited_urls, top_k=min(12, len(visited_urls)))
        if ranked:
            lines = []
            for r in ranked:
                idx = r["index"]
                score = int(round(r.get("score", 0)))
                reason = (r.get("reason") or "").strip()
                url = visited_urls[idx - 1]
                lines.append(f"[{idx}] (score {score}) {url} — {reason}")
            priority_block = "\n".join(lines)

    prioritization_text = ""
    if USE_SOURCE_RANKING:
        prioritization_text = (
            f"Prioritization:\n"
            f"- Prefer the 'PRIORITY SOURCES' (by usefulness ranking) for most of your citations when possible.\n"
            f"- When multiple sources support a claim, choose from the top-ranked set first.\n\n"
            f"=== PRIORITY SOURCES (indices refer to the catalog) ===\n"
            f"{priority_block}\n\n"
        )

    full_prompt = trim_prompt(
        f"""
You are writing a scholarly report. You MUST ONLY cite from the sources listed below.

Citation style (strict):
- Use numeric citations [n] from the catalog only (1..{n_sources}); [n,m] for multiple.
- No bare URLs/footnotes in the text; only [n].
- If a claim cannot be sourced, write [citation needed].

{prioritization_text}
Given the following prompt from the user, write a final report on the topic using the learnings from research.

=== RESEARCH QUESTION ===
{prompt}

=== LEARNINGS ===
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
                    "reportMarkdown": {"type": "string"}
                },
                "required": ["reportMarkdown"]
            }
        }
    }

    completion = _model_config_instance.generate_completion(
        messages=[{"role": "system", "content": system_prompt()},
                  {"role": "user", "content": full_prompt}],
        response_format=response_format
    )

    parsed = json.loads(completion.choices[0].message.content)
    report_md_raw = parsed["reportMarkdown"].rstrip()

    # Build citations + formatted URL references
    bundle = _build_citations_bundle(
        report_md_raw,
        visited_urls,
        order_by="numeric",
        renumber=True,
        sanitize_urls=True
    )

    final_md = bundle["final_md"]
    mapping = bundle["mapping"] or {}
    urls_out = bundle["urls_list"]

    # Optional: Ranking section after References, showing mapped citation numbers
    if USE_SOURCE_RANKING and SHOW_RANKING_SECTION and ranked:
        rank_lines = []
        for r in ranked:
            old_idx = r["index"]
            score = int(round(r.get("score", 0)))
            reason = (r.get("reason") or "").strip()
            mapped = mapping.get(old_idx)
            tag = f"[{mapped}]" if mapped is not None else "[not cited]"
            url = urls_out[old_idx - 1] if 1 <= old_idx <= len(urls_out) else r.get("url", "")
            rank_lines.append(f"{tag} (score {score}) {url} — {reason}")
        final_md += "\n\n## Source Usefulness Ranking (top)\n\n" + "\n".join(rank_lines)

    return final_md

# -----------------------------------------------------------------------------
# Short final answer (unchanged)
# -----------------------------------------------------------------------------
async def write_final_answer(prompt: str, learnings: list) -> str:
    """Generate a short and concise final answer based on learnings."""
    learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in (learnings or []))

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

# -----------------------------------------------------------------------------
# SERP query generator
# -----------------------------------------------------------------------------
async def generate_serp_queries(query: str, num_queries: int = 3, learnings: Optional[List[str]] = None):
    learnings_text = "\n".join(learnings) if learnings else ""
    prompt = (
        f"Given the following prompt, generate up to {num_queries} SERP queries to research the topic.\n"
        f"<prompt>{query}</prompt>\n\n"
        f"{f'Here are learnings from previous research: {learnings_text}' if learnings else ''}"
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
        messages=[{"role": "system", "content": system_prompt()},
                  {"role": "user", "content": prompt}],
        response_format=schema
    )

    parsed = json.loads(result.choices[0].message.content)
    return parsed["queries"][:num_queries]

# -----------------------------------------------------------------------------
# SERP result processing
# -----------------------------------------------------------------------------
async def process_serp_result(query: str, result: Dict, num_learnings: int = 3, num_followups: int = 3):
    contents = []
    # Firecrawl style
    if "data" in result:
        for doc in result.get("data", []):
            if doc.get("markdown"):
                contents.append(trim_prompt(doc.get("markdown", ""), 25000))
    # ORKG classic
    elif "payload" in result and "items" in result["payload"]:
        items = result["payload"]["items"][:10]
        for item in items:
            url = None
            if isinstance(item.get("urls"), list) and item["urls"]:
                url = item["urls"][0]
            elif isinstance(item.get("urls"), str):
                url = item["urls"]
            elif item.get("url"):
                url = item["url"]
            block = f"{item.get('title','')}\n{item.get('abstract','')}\n{url or ''}"
            if item.get("title") or item.get("abstract"):
                contents.append(trim_prompt(block, 25000))
    # Fallbacks for API variants
    elif "payload" in result or "items" in result:
        items = []
        pl = result.get("payload")
        if isinstance(pl, dict) and isinstance(pl.get("items"), list):
            items = pl["items"][:10]
        elif isinstance(pl, list):
            items = pl[:10]
        elif isinstance(result.get("items"), list):
            items = result["items"][:10]
        for item in items:
            url = None
            if isinstance(item.get("urls"), list) and item["urls"]:
                url = item["urls"][0]
            elif isinstance(item.get("urls"), str):
                url = item["urls"]
            elif item.get("url"):
                url = item["url"]
            block = f"{item.get('title','')}\n{item.get('abstract','')}\n{url or ''}"
            if block.strip():
                contents.append(trim_prompt(block, 25000))

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
                    "learnings": {"type": "array", "items": {"type": "string"}},
                    "followUpQuestions": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["learnings", "followUpQuestions"]
            }
        }
    }

    completion = _model_config_instance.generate_completion(
        messages=[{"role": "system", "content": system_prompt()},
                  {"role": "user", "content": prompt}],
        response_format=response_format
    )

    parsed = json.loads(completion.choices[0].message.content)
    return parsed

# -----------------------------------------------------------------------------
# Main workflow – robust recursion (merge child results; breadth never 0)
# -----------------------------------------------------------------------------
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

            # Extract URLs in order, light dedup
            urls = []
            if "data" in result:  # Firecrawl
                docs = result.get("data", [])
                for doc in docs:
                    u = doc.get("url")
                    if u:
                        urls.append(u)
                urls = _uniq_preserve(urls)
            elif "payload" in result and "items" in result["payload"]:  # ORKG
                items = result["payload"]["items"][:10]
                for item in items:
                    u = None
                    if isinstance(item.get("urls"), list) and item["urls"]:
                        u = item["urls"][0]
                    elif isinstance(item.get("urls"), str):
                        u = item["urls"]
                    elif item.get("url"):
                        u = item["url"]
                    if u:
                        urls.append(u)
                urls = _uniq_preserve([u for u in urls if u])
            else:
                # other API variants
                items = []
                pl = result.get("payload")
                if isinstance(pl, dict) and isinstance(pl.get("items"), list):
                    items = pl["items"][:10]
                elif isinstance(pl, list):
                    items = pl[:10]
                elif isinstance(result.get("items"), list):
                    items = result["items"][:10]
                for item in items:
                    u = None
                    if isinstance(item.get("urls"), list) and item["urls"]:
                        u = item["urls"][0]
                    elif isinstance(item.get("urls"), str):
                        u = item["urls"]
                    elif item.get("url"):
                        u = item["url"]
                    if u:
                        urls.append(u)
                urls = _uniq_preserve([u for u in urls if u])

            follow = await process_serp_result(serp_query["query"], result, num_learnings=3, num_followups=breadth)
            new_learnings = follow.get("learnings", [])
            new_followups = follow.get("followUpQuestions", [])

            updated_learnings = _uniq_preserve(learnings + new_learnings)
            updated_urls = _uniq_preserve(visited_urls + urls)

            if depth - 1 > 0:
                # recurse with breadth never dropping to 0
                next_query = f"Previous research goal: {serp_query['researchGoal']}\nFollow-up: {'; '.join(new_followups)}"
                child = await deep_research(
                    next_query,
                    breadth=max(1, breadth // 2),
                    depth=depth - 1,
                    learnings=updated_learnings,
                    visited_urls=updated_urls,
                    on_progress=on_progress
                )
                # MERGE child results (do NOT overwrite!)
                merged_learnings = _uniq_preserve(updated_learnings + child.get("learnings", []))
                merged_urls = _uniq_preserve(updated_urls + child.get("visitedUrls", []))

                report({"currentDepth": depth - 1, "completedQueries": progress["completedQueries"] + 1})
                return {"learnings": merged_learnings, "visitedUrls": merged_urls}
            else:
                report({"currentDepth": 0, "completedQueries": progress["completedQueries"] + 1})
                return {"learnings": updated_learnings, "visitedUrls": updated_urls}
        except Exception:
            return {"learnings": [], "visitedUrls": []}

    results = await asyncio.gather(*(run_query(q) for q in serp_queries)) if serp_queries else []

    all_learnings = []
    all_urls = []
    for res in results:
        all_learnings.extend(res.get("learnings", []))
        all_urls.extend(res.get("visitedUrls", []))

    all_learnings = _uniq_preserve(all_learnings)
    all_urls = _uniq_preserve(all_urls)

    return {"learnings": all_learnings, "visitedUrls": all_urls}
