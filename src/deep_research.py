import asyncio, json, re
from typing import List, Dict, Any
import aiohttp
from ai.llms import query_llm

DATA_DIR = __import__('pathlib').Path(__file__).parent / 'data'

class ORKGClient:
    SEARCH = 'https://api.ask.orkg.org/index/search'
    PAPER  = 'https://api.orkg.org/papers'

    async def search(self, query: str, limit: int=5) -> List[Dict[str,Any]]:
        print(f"[ORKG-SEARCH] q={query}")
        async with aiohttp.ClientSession() as sess:
            async with sess.get(self.SEARCH, params={'query':query,'limit':limit}) as r:
                text = await r.text()
                if r.status!=200:
                    print(f"[ORKG-ERR] {r.status} {text}")
                    return []
                data = await r.json()
        if isinstance(data.get('data'), list):
            return data['data']
        return data.get('payload',{}).get('items',[])

    async def fetch_content(self, paper_id: str) -> str:
        url = f"{self.PAPER}/{paper_id}"
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as r:
                if r.status!=200: return ''
                return (await r.json()).get('abstract','')

class FirecrawlClient:
    BASE = 'https://api.firecrawl.com/search'
    KEY  = None
    async def search(self, query: str, limit:int=5)->List[Dict[str,Any]]:
        import requests
        r = requests.get(self.BASE, params={'key':self.KEY,'q':query,'limit':limit})
        if r.status_code!=200:
            print(f"[FC-ERR] {r.status_code} {r.text}")
            return []
        return r.json().get('results',[])

def extract_json(raw: str)->Dict[str,Any]:
    m = re.search(r'\{.*\}', raw, flags=re.DOTALL)
    if not m: raise ValueError("No JSON found")
    return json.loads(m.group(0))

def build_serp_prompt(topic: str, ctx: str, breadth:int)->str:
    return (
        "You are a focused research assistant generating concise search queries.\n"
        f"Topic: {topic}\nContext: {ctx}\n"
        f"Generate exactly {breadth} search queries.  "
        "- Include only user-affirmed aspects; ignore negatives.  "
        "- If none affirmed, return [\"{topic} overview\"].  "
        "Return *only* a JSON object {\"queries\":[...]}, no extra text.\n"
    )

def build_summary_prompt(abs_txt: str)->str:
    return (
        "Summarize the following abstract in one clear sentence.  "
        "Return only that sentence.\n\n"
        f"\"\"\"\n{abs_txt}\n\"\"\""
    )

async def deep_research(
    topic:        str,
    breadth:      int,
    depth:        int,
    questions:    List[str],
    answers:      List[str],
    model_name:   str,
    save_models:  int,
    use_firecrawl:bool
) -> Dict[str,List[str]]:
    client = FirecrawlClient() if use_firecrawl else ORKGClient()

    # build Q/A context
    ctx = topic
    if questions:
        qa = '; '.join(f"Q:{q} A:{a}" for q,a in zip(questions,answers))
        ctx = f"{topic} — {qa}"

    # 1) SERP queries
    sp = build_serp_prompt(topic,ctx,breadth)
    print(f"[SERP-PROMPT]\n{sp}")
    raw = await asyncio.get_event_loop().run_in_executor(
        None, query_llm, sp, model_name, save_models
    )
    print(f"[SERP-RAW]\n{raw}")
    try:
        data = extract_json(raw)
        queries = data.get('queries',[])
        assert isinstance(queries,list)
    except Exception as e:
        print(f"[SERP-ERR] {e}")
        queries = [f"{topic} overview"]

    print(f"[SERP] Qs={queries}")

    learnings, visited = [], []
    # 2) For each query do search+summaries
    for i,q in enumerate(queries,1):
        print(f"[SEARCH {i}/{len(queries)}] {q}")
        hits = await client.search(q, limit=breadth)
        if not hits:
            print(f"[SEARCH] no hits for {q}")
            continue

        for paper in hits[:breadth]:
            pid = paper.get('paperId') or paper.get('id')
            if not pid: continue
            visited.append(str(pid))

            abstract = paper.get('snippet','') if use_firecrawl else await client.fetch_content(str(pid))
            if not abstract: continue

            sp2 = build_summary_prompt(abstract)
            raw2 = await asyncio.get_event_loop().run_in_executor(
                None, query_llm, sp2, model_name, save_models
            )
            sent = raw2.strip().split('\n')[0]
            learnings.append(sent)
            print(f"[SUMMARY] {sent}")

    # 3) recurse
    if depth>1 and learnings:
        sub = await deep_research(
            topic=' '.join(learnings),
            breadth=breadth,
            depth=depth-1,
            questions=[],
            answers=[],
            model_name=model_name,
            save_models=save_models,
            use_firecrawl=use_firecrawl
        )
        learnings.extend(sub['learnings'])
        visited.extend(sub['visited_urls'])

    return {'learnings':learnings, 'visited_urls':visited}

async def write_final_report(
    topic:      str,
    questions:  List[str],
    answers:    List[str],
    learnings:  List[str],
    visited_urls:List[str],
    model_name: str,
    save_models:int
)->str:
    qa = ''
    if questions:
        qa = ' — ' + '; '.join(f"Q:{q} A:{a}" for q,a in zip(questions,answers))
    prompt = (
        f"Write a detailed report on '{topic}{qa}'.\n"
        f"Include these insights: {', '.join(learnings)}.\n"
        f"Sources: {', '.join(visited_urls)}.\n"
        "Return only the text of the report.\n"
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )

async def write_final_answer(
    topic:      str,
    questions:  List[str],
    answers:    List[str],
    learnings:  List[str],
    model_name: str,
    save_models:int
)->str:
    qa=''
    if questions:
        qa = ' — ' + '; '.join(f"Q:{q} A:{a}" for q,a in zip(questions,answers))
    prompt = (
        f"Provide a concise answer to '{topic}{qa}'.\n"
        f"Key findings: {', '.join(learnings)}.\n"
        "Return only the answer text.\n"
    )
    return await asyncio.get_event_loop().run_in_executor(
        None, query_llm, prompt, model_name, save_models
    )
