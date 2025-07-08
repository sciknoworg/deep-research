# File: src/feedback.py
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
    lines = content.strip().splitlines()
    questions = [
        re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        for line in lines
        if "?" in line
    ]
    return questions[:max_n]

def generate_feedback(
    query: str,
    model_name: str,
    save_models: int = 0,
    num_questions: int = 3,
    timeout: Optional[int] = 300
) -> List[str]:
    system = system_prompt()
    prompt_text = (
        f"{system}\n"
        f"Given the user's research topic, propose up to {num_questions} follow-up questions to clarify the direction: {query}"
    )
    # Submit the prompt as a cluster job
    idx = query_llm(prompt_text, model_name, save_models)

    # Wait for the SLURM output file
    data_dir = Path(__file__).parents[1] / 'data'
    out_file = data_dir / f'output_{idx}.json'
    elapsed = 0
    while not out_file.exists() and elapsed < timeout:
        time.sleep(1)
        elapsed += 1
    if not out_file.exists():
        raise TimeoutError(f"Feedback generation timed out after {timeout} seconds.")

    # Read the generated result
    with open(out_file, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    text = payload.get('choices', [{}])[0].get('text', '')

    # Try JSON parsing, otherwise fallback
    try:
        parsed = json.loads(text)
        validated = FeedbackSchema(**parsed)
        return validated.questions[:num_questions]
    except (ValidationError, json.JSONDecodeError):
        return extract_questions_fallback(text, num_questions)
