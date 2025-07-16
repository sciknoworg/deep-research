import json
from typing import List
from ai.llms import query_llm_cluster
import json
import re
from typing import List
from pydantic import BaseModel, Field, ValidationError
from prompt import system_prompt

def generate_feedback_cluster(
    topic:        str,
    model_name:   str,
    save_models:  int = 0,
    num_questions:int = 3
) -> List[str]:
    """
    Ask the LLM for exactly `num_questions` clarifying follow-up questions,
    returned as a Python list of strings.
    """
    prompt = (
        "You are a helpful research assistant.\n"
        "Generate EXACTLY 3 clarifying QUESTIONS to narrow the research focus from the User on \n"
        f"TOPIC: {topic}\n"
        "(e.g. Ask about: geography, species, uses). "
        "Return only a JSON array of strings of the Questions, no extra text.\n\n"
        "Example format:\n"
        "[\"Question one?\", \"Question two?\", \"Question three?\"]\n"
    )

    try:
        raw = query_llm_cluster(prompt, model_name, save_models)
    except Exception as e:
        print(f"[FEEDBACK-ERROR] LLM call failed: {e}")
        raw = ""

    # Try to pull out a JSON array
    start = raw.find('[')
    end   = raw.rfind(']')
    if start != -1 and end != -1:
        try:
            arr = json.loads(raw[start:end+1])
            if isinstance(arr, list) and all(isinstance(x,str) for x in arr):
                return arr[:num_questions]
        except json.JSONDecodeError:
            pass

    # Fallback: any line ending in '?'
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip().endswith('?')]
    # Pad if needed
    while len(lines) < num_questions:
        lines.append(f"(No question generated #{len(lines)+1})")
    return lines[:num_questions]

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
