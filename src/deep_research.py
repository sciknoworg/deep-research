import asyncio, json
from typing import List, Dict
from ai.llms import query_llm
import aiohttp, os

# ORKG client
class ORKGAskApp:
    def __init__(self): self.base='https://api.ask.orkg.org/index'
    async def search(self,q,limit=10):
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{self.base}/search",params={'query':q,'limit':limit}) as r:
                return await r.json()
    async def fetch_content(self,pid):
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.orkg.org/papers/{pid}") as r:
                return (await r.json()).get('abstract','')

search_client = ORKGAskApp()

async def deep_research(topic:str,breadth=4,depth=2,questions=None,answers=None)->Dict:
    questions=questions or []
    answers=answers or []
    combined = topic if not questions else 'Initial: '+topic+'\n'+ '\n'.join([f"Q:{q} A:{a}" for q,a in zip(questions,answers)])
    # 1. generate queries
    prompt = f"Return EXACTLY {breadth} search queries as a JSON array for topic: '{combined}'"
    raw = query_llm(prompt)
    try: queries=json.loads(raw)
    except: queries=[l.strip() for l in raw.splitlines() if l.strip()]
    learnings=[]; visited=[]
    # 2. fetch and summarize
    for q in queries:
        res=await search_client.search(q)
        for e in res.get('data',res.get('results',res)):
            pid=e.get('paperId') or e.get('id')
            if not pid: continue
            visited.append(pid)
            abs=await search_client.fetch_content(pid)
            summary=query_llm(f"Summarize abstract: {abs}")
            learnings.append(summary)
    # 3. recurse
    if depth>1 and learnings:
        sub=await deep_research(' '.join(learnings),breadth,depth-1,questions,answers)
        learnings+=sub['learnings']; visited+=sub['visited']
    return {'learnings':learnings,'visited':visited,'queries':queries}

async def write_final_report(combined,learnings,visited)->str:
    prompt = (
        f"Write comprehensive report. Prompt: {combined}. "
        f"Learnings: {'; '.join(learnings)}. Sources: {'; '.join(visited)}"
    )
    return query_llm(prompt)

async def write_final_answer(combined,learnings)->str:
    prompt = (
        f"Answer concisely. Prompt: {combined}. Key findings: {'; '.join(learnings)}"
    )
    return query_llm(prompt)