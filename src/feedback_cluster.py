import json
import re
from typing import List
from pydantic import BaseModel, Field, ValidationError
from prompt import system_prompt
from ai.llms import call_huggingface_on_cluster, wait_for_output_file
from ai.prompt_utils import trim_prompt

class FeedbackSchema(BaseModel):
    questions: List[str] = Field(...)

def extract_questions_fallback(content: str, max_n: int = 3) -> List[str]:
    lines = content.strip().splitlines()
    questions = [
        re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        for line in lines if "?" in line
    ]
    return questions[:max_n]

def generate_feedback_cluster(query: str, model_name: str, num_questions: int = 3) -> List[str]:
    system = system_prompt()
    prompt_text = trim_prompt(
        f"""{system}\n\nGiven the following query from the user, ask some follow-up questions 
        to clarify the research direction. Return a maximum of {num_questions} questions, 
        but feel free to return less if the original query is clear: <query>{query}</query>"""
    )

    try:
        call_huggingface_on_cluster(prompt_text, model_name=model_name, index=995)
        result = await wait_for_output_file(index=995)
        content = result.get("response", "")

        if isinstance(content, dict):
            validated = FeedbackSchema(**content)
            return validated.questions[:num_questions]

        try:
            parsed = json.loads(content)
            validated = FeedbackSchema(**parsed)
            return validated.questions[:num_questions]
        except (ValidationError, json.JSONDecodeError) as e:
            print("Structured parsing failed:", e)

        print("Falling back to text extraction...")
        return extract_questions_fallback(content, num_questions)

    except Exception as e:
        print(f"Cluster feedback error: {e}")
        return []
