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
# Env
# ---------------------------------------

def _env_true(val: Optional[str], default: bool = True) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "on", "y"}

USE_SOURCE_RANKING = _env_true(os.getenv("USE_SOURCE_RANKING"), default=False)
SHOW_RANKING_SECTION = _env_true(os.getenv("SHOW_RANKING_SECTION"), default=False)

# Allow more learnings per SERP without changing signatures elsewhere
MAX_LEARNINGS_PER_QUERY = int(os.getenv("MAX_LEARNINGS_PER_QUERY", "6"))

# Module-level store for optional per-learning URL hints (aligned to final learnings)
_LAST_SUPPORTING_URLS: List[List[str]] = []

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
    """Build numbered source catalog from URLs (AS-IS)."""
    urls_list = urls or []
    lines = [f"[{i}] {u}" for i, u in enumerate(urls_list, 1)]
    return "\n".join(lines), urls_list

def _strip_existing_references(md: str) -> str:
    """Remove any trailing '## References' section so we only parse [n] from body."""
    if not md:
        return md
    m = re.search(r'(?im)^#{2,}\s*references?\b.*$', md)
    return md[:m.start()] if m else md

def _extract_citation_numbers_in_appearance_order(md_body: str) -> List[int]:
    """Return distinct citation numbers in order of first appearance."""
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

def _compact_learnings_for_context(learnings: List[str], k: int = 30, max_chars: int = 4000) -> str:
    """
    Build a compact, high-signal subset of learnings for query planning.
    Heuristics only (no extra LLM calls): prefer entries with digits/proper nouns.
    """
    if not learnings:
        return ""
    uniq = []
    seen = set()
    for s in learnings:
        s = (s or "").strip()
        if not s or s in seen:
            continue
        seen.add(s); uniq.append(s)
    scored = sorted(
        uniq,
        key=lambda x: (any(c.isdigit() for c in x), sum(t.istitle() for t in x.split())),
        reverse=True
    )
    out_lines, total = [], 0
    for s in (scored[:k] if len(scored) > k else scored):
        if total + len(s) + 2 > max_chars:
            break
        out_lines.append(f"- {s}")
        total += len(s) + 2
    return "\n".join(out_lines)

def _hinted_learnings(learnings: List[str], supporting_urls: Optional[List[List[str]]], urls_list: List[str]) -> str:
    """
    Render learnings with optional <hints>[n]</hints> based on supporting_urls,
    where supporting_urls[i] contains 0..2 URLs for learnings[i].
    """
    lines = []
    for i, L in enumerate(learnings):
        hints = []
        if supporting_urls and i < len(supporting_urls):
            for u in (supporting_urls[i] or [])[:2]:
                try:
                    idx = urls_list.index(u) + 1
                    hints.append(f"[{idx}]")
                except ValueError:
                    pass
        if hints:
            lines.append(f"<learning>\n{L}\n<hints>{' '.join(hints)}</hints>\n</learning>")
        else:
            lines.append(f"<learning>\n{L}\n</learning>")
    return "\n".join(lines)

# ---------------------------------------
# Citations builder
# ---------------------------------------

def _build_citations_bundle(
    report_md_raw: str,
    visited_urls: List[str],
    *,
    order_by: str = "numeric",   # "numeric" or "appearance"
    renumber: bool = True,
    sanitize_urls: bool = False
) -> Dict:
    """
    Build '## References' from actually used [n] in body.
    If none used: fallback to full catalog.
    """
    body = _strip_existing_references(report_md_raw or "").rstrip()

    used_nums = _extract_citation_numbers_in_appearance_order(body)
    if order_by == "numeric":
        used_nums = sorted(used_nums)

    urls_list = list(visited_urls or [])

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

    used_nums = [n for n in used_nums if 1 <= n <= len(urls_list)]

    mapping: Optional[Dict[int, int]] = None
    if renumber:
        mapping = {old: new for new, old in enumerate(used_nums, 1)}
        body = _renumber_citations_in_text(body, mapping)
        ref_lines = [f"[{mapping[old]}] {urls_list[old-1]}" for old in used_nums]
    else:
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
    order_by: str = "numeric",
    renumber: bool = True,
    sanitize_urls: bool = False
) -> str:
    bundle = _build_citations_bundle(
        report_md_raw,
        visited_urls,
        order_by=order_by,
        renumber=renumber,
        sanitize_urls=sanitize_urls
    )
    return bundle["final_md"]

# ---------------------------------------
# Optional: Paper Ranking (no influence on writer prompt)
# ---------------------------------------

async def rank_papers(
    research_question: str,
    learnings: List[str],
    visited_urls: List[str],
) -> List[Dict]:
    urls = visited_urls or []
    if not urls:
        return []

    learnings_str = "\n".join(f"- {l}" for l in (learnings or []))
    catalog_lines = "\n".join(f"[{i}] {u}" for i, u in enumerate(urls, 1))
    k = len(urls)

    prompt = trim_prompt(f"""
You are ranking sources for usefulness to answer a research question.
Base your judgement only on URL cues and the provided learnings (no browsing).

Research question:
{research_question}

Learnings:
{learnings_str}

Source catalog:
{catalog_lines}

Return JSON 'ranked': array of objects with fields
- index (1-based), url, score (0..100), reason (1–2 sentences).
Sort by score DESC. Limit {k}.
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
        messages=[
            {"role": "system", "content": system_prompt()},
            {"role": "user", "content": prompt}
        ],
        response_format=schema
    )

    try:
        parsed = json.loads(result.choices[0].message.content)
        ranked = parsed.get("ranked", [])
        ranked = [
            r for r in ranked
            if isinstance(r.get("index"), int) and 1 <= r["index"] <= len(urls)
        ][:k]
        for r in ranked:
            if not r.get("url"):
                r["url"] = urls[r["index"] - 1]
        ranked.sort(key=lambda x: x.get("score", 0), reverse=True)
        return ranked
    except Exception:
        return []

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

def _make_client():
    """Resolve provider from ENV at call time (still ENV-controlled, more robust)."""
    provider = os.getenv("RESEARCH_PROVIDER", "firecrawl")
    client = get_search_client(provider)
    print(f"Search provider in use: {type(client).__name__}")
    return client

# ---------------------------------------
# Final report (+ citation)
# ---------------------------------------

async def write_final_report(prompt: str, learnings: list, visited_urls: list) -> str:
    """
    Report writer with (1) sources placed early, (2) optional [n] hints per learning,
    (3) same return contract as before.
    """
    sources_block, urls_list = _build_sources_block(visited_urls)
    n_sources = len(urls_list)

    # Render learnings; if we have stored hints, surface them
    global _LAST_SUPPORTING_URLS
    try:
        learnings_string = _hinted_learnings(learnings, _LAST_SUPPORTING_URLS, urls_list)
    except Exception:
        learnings_string = "\n".join(f"<learning>\n{l}\n</learning>" for l in learnings)

    full_prompt = trim_prompt(
        f"""
You are writing a scholarly report grounded in the numbered catalog BELOW (placed early to avoid context loss).

=== SOURCES (numbered catalog — cite only from here) ===
{sources_block}

Length & Coverage
- Write at least three full pages of substantive, fact-dense text (no filler).
- Weave in as many LEARNINGS as are relevant; synthesize and paraphrase clearly.

Citation Playbook (VERY IMPORTANT)
- Cite ONLY from the numbered catalog (1..{n_sources}) using square brackets [n] or [n,m].
- Aim for ≥1 citation in EVERY paragraph with nontrivial facts; target ≥ min(6, {n_sources}) distinct sources overall.
- If a learning contains <hints>[n]</hints>, strongly prefer those [n] unless they are clearly suboptimal.
- Spread citations across distinct high-quality sources; avoid repeating the same source in adjacent paragraphs unless necessary.
- Place citations immediately after the supported sentence (not only at paragraph end).
- If nothing fits, write [citation needed] (rare).

Sectioning
1) Introduction (include at least one citation)
2) Main body with multiple subsections (engineering/science/policy etc.) — keep citing
3) Conclusion (succinct; include at least one citation)

=== RESEARCH QUESTION ===
{prompt}

=== LEARNINGS (use and weave in as many as relevant) ===
{learnings_string}

Task
- Produce the report in Markdown.
- At the end, append **## References** listing ONLY the sources actually cited in the body, using the SAME catalog numbers.
- Do not include your reasoning or an outline; think silently.
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

    final_md = add_citations(
        report_md_raw,
        visited_urls,
        order_by="numeric",
        renumber=True,
        sanitize_urls=False
    )

    if SHOW_RANKING_SECTION and USE_SOURCE_RANKING and visited_urls:
        ranked = await rank_papers(prompt, learnings, visited_urls)
        if ranked:
            lines = []
            for r in ranked:
                idx = r.get("index")
                score = int(round(r.get("score", 0)))
                reason = (r.get("reason") or "").strip()
                url = visited_urls[idx - 1] if idx and 1 <= idx <= len(visited_urls) else (r.get("url") or "")
                lines.append(f"[{idx}] (score {score}) {url} — {reason}")
            final_md += "\n\n## Source Usefulness Ranking\n\n" + "\n".join(lines)

    return final_md

# ---------------------------------------
# Short final answer
# ---------------------------------------

async def write_final_answer(prompt: str, learnings: list) -> str:
    """Short final answer, repo-style."""
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
# SERP query generator
# ---------------------------------------

async def generate_serp_queries(query: str, num_queries: int = 3, learnings: Optional[List[str]] = None):
    """
    Generate diverse SERP queries. 'learnings' may be a list (legacy) or a compact string.
    """
    num_queries = max(1, int(num_queries) if isinstance(num_queries, int) else 1)

    if isinstance(learnings, list):
        learnings_text = "\n".join(learnings) if learnings else ""
    elif isinstance(learnings, str):
        learnings_text = learnings
    else:
        learnings_text = ""
    context_line = f"Context (compact, high-signal):\n{learnings_text}" if learnings_text else ""

    prompt = (
        "Given the following prompt, generate up to "
        f"{num_queries} diverse SERP queries that maximize credible, citable coverage.\n\n"
        f"<prompt>{query}</prompt>\n\n"
        "Guidelines:\n"
        "- Mix angles: core technical/science, policy/legal, standards/agency guidance, industry/whitepaper.\n"
        "- Prefer authoritative domains (e.g., .gov, .edu, .int, standards bodies) and use operators when helpful "
        "(site:, filetype:pdf, \"report\", \"whitepaper\", \"standard\", \"guideline\").\n"
        "- Include synonyms/aliases and canonical program/instrument names to broaden recall.\n"
        "- At least one query MUST target primary literature (journals) and one MUST target policy/standards.\n"
        "- Avoid near-duplicates; cover distinct facets.\n"
        f"{context_line}\n"
        "Return concise queries with a clear researchGoal for each."
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
    return parsed.get("queries", [])[:num_queries] or []

# ---------------------------------------
# SERP result processing
# ---------------------------------------

async def process_serp_result(query: str, result: Dict, num_learnings: int = 3, num_followups: int = 3):
    """
    Distill SERP content into factual learnings + follow-up questions.
    Additionally try to surface supporting URLs for each learning (if applicable).
    """
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
                f"{item.get('title', '')}\n{item.get('abstract', '')}\n{(item.get('urls') or [''])[0] if item.get('urls') else ''}",
                25000
            )
            for item in items
            if item.get("title") or item.get("abstract")
        ]
    else:
        contents = []

    print(f"Ran {query}, found {len(contents)} contents")

    # Collect candidate URLs for hinting later
    candidate_urls = []
    if "data" in result:
        candidate_urls = [d.get("url") for d in result.get("data", []) if d.get("url")]
    elif "payload" in result and "items" in result["payload"]:
        for it in result["payload"]["items"][:10]:
            if isinstance(it.get("urls"), list) and it["urls"]:
                candidate_urls.append(it["urls"][0])
            elif it.get("url"):
                candidate_urls.append(it["url"])
    candidate_urls = [u for u in candidate_urls if u]

    contents_text = "\n".join(f"<content>\n{c}\n</content>" for c in contents)
    prompt = trim_prompt(
        f"""You are distilling SERP content into **evidence-ready** learnings.

Return:
- up to {num_learnings} learnings: each a self-contained, falsifiable factual statement that could be cited verbatim in a report.
  * Include concrete entities, dates, metrics, instrument/mission names, report IDs, standard numbers, treaty/article names when present.
  * One claim per learning; avoid overlaps.
- up to {num_followups} follow-up questions that would deepen coverage.
- For each learning, list 1–2 supportingUrls **taken from the candidate URL list** (if applicable).

Candidate URLs:
{chr(10).join(candidate_urls)}

Strictly use only details present in the content; no fabrication.

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
                    "followUpQuestions": {"type": "array", "items": {"type": "string"}},
                    "supportingUrls": { "type": "array", "items": { "type": "array", "items": {"type":"string"} } }
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
    # Ensure optional field presence
    if "supportingUrls" not in parsed or not isinstance(parsed.get("supportingUrls"), list):
        parsed["supportingUrls"] = []
    return parsed

# ---------------------------------------
# Main workflow
# ---------------------------------------

async def deep_research(query: str, breadth: int, depth: int, learnings=None, visited_urls=None, on_progress: Optional[Callable] = None,
                        _support_collector: Optional[List[List[str]]] = None, _raw_learnings_collector: Optional[List[str]] = None):
    """
    Recursive exploration as before.
    Improvements:
      - Query planning uses a compact, high-signal subset of learnings (less drift).
      - Optional per-learning URL hints collected across the whole run (module-level store).
    """
    # IMPORTANT: one global declaration at the top of the function
    global _LAST_SUPPORTING_URLS
    client = _make_client()

    learnings = learnings or []
    visited_urls = visited_urls or []
    if _support_collector is None:
        _support_collector = []
    if _raw_learnings_collector is None:
        _raw_learnings_collector = []

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

    # Ensure >=1 queries requested; pass compact context (not the whole learnings list)
    compact_context = _compact_learnings_for_context(learnings, k=30, max_chars=4000)
    serp_queries = await generate_serp_queries(query, max(1, breadth), compact_context if compact_context else None)

    if serp_queries:
        report({"totalQueries": len(serp_queries), "currentQuery": serp_queries[0]["query"]})
    else:
        _LAST_SUPPORTING_URLS = [[] for _ in learnings]
        return {
            "learnings": _uniq_preserve(learnings),
            "visitedUrls": _uniq_preserve(visited_urls)
        }

    async def run_query(serp_query):
        try:
            result = await client.search(serp_query["query"])

            if "data" in result:
                urls_raw = [doc.get("url") for doc in result.get("data", []) if doc.get("url")]
                urls = _uniq_preserve(urls_raw)
            elif "payload" in result and "items" in result["payload"]:
                items = result["payload"]["items"][:10]
                urls_raw = []
                for item in items:
                    if isinstance(item.get("urls"), list) and item["urls"]:
                        urls_raw.append(item["urls"][0])
                    elif isinstance(item.get("urls"), str):
                        urls_raw.append(item["urls"])
                    elif item.get("url"):
                        urls_raw.append(item["url"])
                urls = _uniq_preserve([u for u in urls_raw if u])
            else:
                urls = []

            follow = await process_serp_result(
                serp_query["query"],
                result,
                num_learnings=MAX_LEARNINGS_PER_QUERY,
                num_followups=breadth
            )
            new_learnings = follow.get("learnings", []) or []
            new_followups = follow.get("followUpQuestions", []) or []
            supp = follow.get("supportingUrls", []) or []

            # Align supportingUrls to learnings length
            new_support_lists: List[List[str]] = []
            for i in range(len(new_learnings)):
                new_support_lists.append(supp[i] if i < len(supp) and isinstance(supp[i], list) else [])

            # Collect raw learnings + support for global hinting (before dedupe)
            _raw_learnings_collector.extend(new_learnings)
            _support_collector.extend(new_support_lists)

            updated_learnings = _uniq_preserve(learnings + new_learnings)
            updated_urls = _uniq_preserve(visited_urls + urls)

            if depth - 1 > 0:
                report({"currentDepth": depth - 1, "completedQueries": progress["completedQueries"] + 1})
                next_query = (
                    f"Root question (do not drift): {query}\n"
                    f"Research goal for this branch: {serp_query.get('researchGoal','')}\n"
                    f"Follow-ups to pursue: {'; '.join(new_followups[:max(1, breadth)])}"
                )
                next_breadth = max(1, breadth // 2)  # keep your original decay
                return await deep_research(
                    next_query,
                    breadth=next_breadth,
                    depth=depth-1,
                    learnings=updated_learnings,
                    visited_urls=updated_urls,
                    on_progress=on_progress,
                    _support_collector=_support_collector,
                    _raw_learnings_collector=_raw_learnings_collector
                )
            else:
                report({"currentDepth": 0, "completedQueries": progress["completedQueries"] + 1})
                return {"learnings": updated_learnings, "visitedUrls": updated_urls}
        except Exception:
            return {"learnings": [], "visitedUrls": []}

    results = await asyncio.gather(*(run_query(q) for q in serp_queries)) if serp_queries else []

    # Merge results (learned facts & URLs) from all branches
    all_learnings = list(learnings)   # start with incoming ones
    all_urls = list(visited_urls)

    for res in results:
        all_learnings.extend(res.get("learnings", []))
        all_urls.extend(res.get("visitedUrls", []))

    # Deduplicate final outputs
    all_urls = _uniq_preserve(all_urls)

    # Build final learning list (unique) but keep hint mapping consistent:
    # Map first occurrence in raw collector to hints; initial incoming learnings get empty hints.
    raw_list = list(_raw_learnings_collector)
    raw_support = list(_support_collector)

    unique_from_raw = _uniq_preserve(raw_list)
    final_learnings = _uniq_preserve(list(learnings) + unique_from_raw)

    # Build mapping from learning -> first support seen in raw_list
    first_support_map: Dict[str, List[str]] = {}
    for idx, L in enumerate(raw_list):
        if L not in first_support_map:
            first_support_map[L] = raw_support[idx] if idx < len(raw_support) else []

    # Compose final hints aligned to final_learnings
    final_support: List[List[str]] = []
    incoming_set = set(learnings)
    for L in final_learnings:
        if L in incoming_set:
            final_support.append([])
        else:
            final_support.append(first_support_map.get(L, []))

    # Store hints module-wide for writer to consume later
    _LAST_SUPPORTING_URLS = final_support

    return {"learnings": final_learnings, "visitedUrls": all_urls}
