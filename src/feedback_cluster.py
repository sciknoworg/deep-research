import json
import re
from typing import List
from pydantic import BaseModel, Field, ValidationError
from ai.llms import call_huggingface_on_cluster, wait_for_output_file
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

async def generate_feedback_cluster(query: str, model_name: str = "deepseek", index: int = 1, num_questions: int = 3) -> List[str]:
    system = system_prompt()
    prompt_text = (
        f"Given the following query from the user, ask some follow-up questions to clarify the research direction to inprove API Queries."
        f"Return a maximum of {num_questions} questions which can help you to specify the research direction."
        f"Make sure to ask questions that are specific and actionable and that will help you to understand the user's needs better. "
        f"Return the questions in a structured format as a JSON array with the key 'questions'. "
        f"Feel free to return less if the original query is clear: <query>{query}</query>"
    )

    full_prompt = f"System: {system}\nUser: {prompt_text}"

    try:
        call_huggingface_on_cluster(full_prompt, model_name=model_name, index=index)
        result = wait_for_output_file(index=index)
        content = result.get("response", "")

        try:
            parsed = json.loads(content)
            validated = FeedbackSchema(**parsed)
            return validated.questions[:num_questions]
        except (ValidationError, json.JSONDecodeError):
            print("Structured parsing failed, falling back to text extraction...")
            return extract_questions_fallback(content, num_questions)

    except Exception as e:
        print(f"[ClusterFeedback] Error: {e}")
        return []