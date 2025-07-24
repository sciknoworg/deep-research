import json
from typing import List
from ai.llms import query_llm_cluster
import json
import re
from typing import List
from pydantic import BaseModel, Field, ValidationError
from prompt import system_prompt

def generate_feedback_cluster(
    topic:         str,
    model_name:    str,
    save_models:   int = 0,
    num_questions: int = 3
) -> List[str]:
    """
    Ask the LLM for exactly `num_questions` clarifying follow-up questions,
    returned as a Python list of strings.
    """
    prompt = (
        f"You are a research assistant.\n"
        f"Given the research topic:\n\n"
        f"  \"{topic}\"\n\n"
        f"Generate EXACTLY {num_questions} concise, open-ended follow-up questions to clarify the user's intent.\n"
        f"Return ONLY a JSON array in the format:\n"
        f"[\"Question one?\", \"Question two?\", \"Question three?\"]"
    )

    try:
        raw = query_llm_cluster(prompt, model_name, save_models)
    except Exception as e:
        print(f"[FEEDBACK-ERROR] LLM call failed: {e!r}")
        raw = ""

    # 1) Versuch: JSON-Array extrahieren (non-greedy, erstes Array)
    m = re.search(r"\[\s*(?:\"[^\"]*\"\s*,\s*){"+str(num_questions-1)+r"\"[^\"]*\"\s*\]", raw, flags=re.S)
    if m:
        try:
            arr = json.loads(m.group(0))
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
                return arr[:num_questions]
        except json.JSONDecodeError:
            pass

    # 2) Fallback: jegliche JSON-Block-Extraktion
    m2 = re.search(r"\[.*?\]", raw, flags=re.S)
    if m2:
        try:
            arr2 = json.loads(m2.group(0))
            if isinstance(arr2, list) and all(isinstance(x, str) for x in arr2):
                return arr2[:num_questions]
        except json.JSONDecodeError:
            pass

    # 3) Linien-basiertes Extrahieren: jede Zeile mit '?'
    lines = []
    for ln in raw.splitlines():
        ln = ln.strip()
        # entferne führende Nummern/Bullets
        ln = re.sub(r"^[\-\*\d\.\)\s]+", "", ln)
        if ln.endswith("?"):
            lines.append(ln)
    # 4) Fallback: in-Text-Fragmenten mit '?' behandeln
    if len(lines) < num_questions:
        fragments = re.findall(r"([A-Z][^?]{10,}?\?)", raw)
        for frag in fragments:
            if frag not in lines:
                lines.append(frag.strip())
            if len(lines) >= num_questions:
                break

    # 5) Pad mit Platzhaltern, falls zu wenige gefunden
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
