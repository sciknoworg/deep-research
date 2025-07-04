import json
import asyncio
import re

async def generate_feedback(query: str) -> list:
    """
    Generates follow-up feedback questions using the LLM.
    """
    prompt = (
        f"Given the initial research query: '{query}', generate 3 concise follow-up questions to clarify the research intent. "
        "Ensure the output is either a JSON array of strings or a numbered list."
    )
    # Import the cluster LLM client
    from ai.llms import query_llm

    # Execute LLM call for feedback questions
    response_text = await asyncio.get_event_loop().run_in_executor(
        None,
        query_llm,
        prompt,
    )

    questions = []
    # Attempt JSON parse
    try:
        data = json.loads(response_text)
        if isinstance(data, list):
            questions = [str(q).strip() for q in data]
    except json.JSONDecodeError:
        pass

    # Fallback: parse numbered or bulleted lists
    if not questions:
        for line in response_text.splitlines():
            match = re.match(r"^\s*(?:\d+|[-*])\W*(.*)$", line)
            if match:
                text = match.group(1).strip().strip('"')
                if text:
                    questions.append(text)

    # Final fallback: semicolon-separated
    if not questions and ';' in response_text:
        questions = [p.strip() for p in response_text.split(';') if p.strip()]

    return questions

# Synchronous wrapper for legacy usage
def generate_feedback_sync(query: str) -> list:
    return asyncio.get_event_loop().run_until_complete(generate_feedback(query))