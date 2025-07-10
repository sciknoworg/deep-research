SYSTEM_PROMPT = (
    "You are a research assistant. "
    "When asked, you must respond ONLY with valid JSON—"
    "an array of strings—and NOTHING else."
)

EXAMPLE_QA = (
    "Q: Impacts of urban heat islands on local climates\n"
    "A: [\n"
    '  "How does increased surface temperature affect urban air quality?",\n'
    '  "What mitigation strategies have proven effective in reducing heat islands?",\n'
    '  "How do green roofs influence local temperature and humidity?"\n'
    "]\n\n"
)

def make_json_array_prompt(
    question: str,
    n: int,
    include_example: bool = True
) -> str:
    """
    Returns a prompt that asks for exactly `n` items in a JSON array.
    - `question`: your core text, e.g. "Generate follow-up questions for: tides"
    - `n`: how many items you want
    - `include_example`: whether to prepend EXAMPLE_QA
    """
    parts = [SYSTEM_PROMPT, ""]
    if include_example:
        parts.append(EXAMPLE_QA)
    parts.append(f"Q: {question} (Return exactly {n} items)")
    parts.append("A:")
    return "\n".join(parts)
