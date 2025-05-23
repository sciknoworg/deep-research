import json
import re
from typing import List
from pydantic import BaseModel, Field, ValidationError
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

def generate_feedback(query: str, client, model_name: str, num_questions: int = 3) -> List[str]:
    system = system_prompt()
    prompt_text = (
        f"Given the following query from the user, ask some follow-up questions "
        f"to clarify the research direction. Return a maximum of {num_questions} questions, "
        f"but feel free to return less if the original query is clear: <query>{query}</query>"
    )

    response_format = {
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
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt_text}
            ],
            response_format=response_format,
            max_completion_tokens=1000
        )

        content = response.choices[0].message.content

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
        print(f"API error: {e}")
        return []
