import json
from typing import List
from ai.llms import query_llm

def generate_feedback(
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
        "You are a helpful research assistant.  "
        f"The user’s topic is: “{topic}”.  "
        f"Generate exactly {num_questions} clarifying questions that will help me "
        "narrow my focus (for example: consumption patterns, cultural uses, technical methods).  "
        "Return only a JSON array of strings.  No extra text.\n\n"
        "Example format:\n"
        "[\"Question one?\", \"Question two?\", \"Question three?\"]"
    )

    try:
        raw = query_llm(prompt, model_name, save_models)
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
