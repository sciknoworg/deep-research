import json
import re
from typing import List
from pydantic import BaseModel, Field, ValidationError
from ai.llms import call_huggingface_on_cluster, wait_for_output_file
from ai.prompt_utils import trim_prompt
from prompt import system_prompt

class FeedbackSchema(BaseModel):
    questions: List[str] = Field(...)

def extract_questions_fallback(content: str, max_n: int = 3) -> List[str]:
    lines = content.strip().splitlines()
    questions = [
        re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        for line in lines if "?" in line
    ]
    return questions[:max_n]

async def generate_feedback_cluster(query: str, model_name: str, index: int = 1, num_questions: int = 3) -> List[str]:
    system = system_prompt()
    prompt_text = trim_prompt(
        f"""Given the following query from the user, ask some follow-up questions to clarify the research direction. 
Return a maximum of {num_questions} questions, but feel free to return less if the original query is clear:

<query>{query}</query>"""
    )

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "feedback_response",
            "schema": {
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["questions"],
                "additionalProperties": False
            }
        }
    }

    try:
        prompt_full = f"System: {system}\nUser: {prompt_text}"
        result = await call_huggingface_on_cluster(prompt_full, model=model_name, index=index)

        try:
            parsed = json.loads(result)
            validated = FeedbackSchema(**parsed)
            return validated.questions[:num_questions]
        except (ValidationError, json.JSONDecodeError):
            print("Structured parsing failed, falling back to text extraction...")

        return extract_questions_fallback(result, num_questions)

    except Exception as e:
        print(f"[FeedbackCluster] Error: {e}")
        return []