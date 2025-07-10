import json
from typing import List
from ai.llms import query_llm
from prompt_framework import make_json_array_prompt

def generate_feedback(
    topic: str,
    model_name: str,
    save_models: int = 0,
    num_questions: int = 3
) -> List[str]:
    prompt = ("You are a research assistant. Return EXACTLY ",
        f"{num_questions} concise follow-up questions for: {topic} ",
        "as a JSON array of strings to specify research direction. No returning of prompt or additional text."
    )
    raw = query_llm(prompt, model_name, save_models)
    try:
        qs = json.loads(raw)
        if isinstance(qs, list) and all(isinstance(q, str) for q in qs):
            return qs[:num_questions]
    except json.JSONDecodeError:
        pass
    # Fallback: extract lines containing a question mark
    lines = [l.strip() for l in raw.splitlines() if "?" in l]
    return lines[:num_questions]