import json
import re
import time
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from prompt import system_prompt
from ai.llms import query_llm

class FeedbackSchema(BaseModel):
    questions: List[str] = Field(...)

def extract_questions_fallback(content: str, max_n: int = 3) -> List[str]:
    return [re.sub(r"^[\-\*\d\.\)\s]+", "", l).strip() for l in content.splitlines() if "?" in l][:max_n]

def generate_feedback(query: str, model_name: str, save_models: int=0, num_questions: int=3, timeout: int=300) -> List[str]:
    sys=sys_prompt = system_prompt()
    prompt = f"{sys}\nPropose up to {num_questions} follow-up questions: {query}"
    txt = query_llm(prompt, model_name, save_models)
    try:
        data=json.loads(txt)
        return FeedbackSchema(**data).questions[:num_questions]
    except:
        return extract_questions_fallback(txt, num_questions)