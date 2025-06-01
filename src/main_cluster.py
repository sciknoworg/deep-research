import asyncio
import os
import sys
from feedback_cluster import generate_feedback_cluster
from ai.llms import call_huggingface_on_cluster, wait_for_output_file
from ai.prompt_utils import trim_prompt
from deep_research_cluster import deep_research, write_final_report, write_final_answer

MODEL_MAP = {
    "deepseek": "deepseek-ai/deepseek-llm-7b-chat",
    "mistral": "mistralai/Mistral-7B-Instruct-v0.2",
    "zephyr": "HuggingFaceH4/zephyr-7b-beta"
}

async def main():
    model_input = input("Enter a model to run on the cluster (default: deepseek): ").strip().lower() or "deepseek"
    model_key = MODEL_MAP.get(model_input, MODEL_MAP["deepseek"])

    initial_query = input("What would you like to research? ").strip()
    breadth = int(input("Enter research breadth (recommended 2–10, default 4): ") or 4)
    depth = int(input("Enter research depth (recommended 1–5, default 2): ") or 2)
    mode = input("Do you want to generate a long report or a specific answer? (report/answer, default report): ").strip().lower() or "report"

    print("\nGenerating follow-up questions...")
    follow_up_questions = await generate_feedback_cluster(initial_query, model_key)
    print("\nTo better understand your research needs, please answer these follow-up questions:")
    answers = []
    for q in follow_up_questions:
        a = input(f"\n{q}\nYour answer: ")
        answers.append(a)

    follow_ups = '\n'.join([f"Q: {q}\nA: {a}" for q, a in zip(follow_up_questions, answers)])
    combined_query = f"""Initial Query: {initial_query}\nFollow-up Questions and Answers:\n{follow_ups}"""

    print("\nStarting research...")
    result = await deep_research(combined_query, breadth, depth, model=model_key)

    print("\nResearch complete. Generating final output...")
    if mode == "answer":
        output = await write_final_answer(initial_query, result["learnings"], model=model_key)
    else:
        output = await write_final_report(initial_query, result["learnings"], result["visitedUrls"], model=model_key)

    print("\n=== FINAL OUTPUT ===\n")
    print(output)

if __name__ == "__main__":
    asyncio.run(main())
