import asyncio
import os
from pathlib import Path

from deep_research import deep_research, write_final_report, write_final_answer
from feedback import generate_feedback
from ai.llms import ModelConfig

async def main():
    # Pick model (optional override)
    model_input = input("Enter an OpenAI model to use (press Enter to use default 'o3-mini'): ").strip()
    if model_input:
        os.environ["CUSTOM_MODEL"] = model_input

    # Initialize model (ensures OpenAI client setup)
    config = ModelConfig()
    model_config = config.get_model_config()
    print("Using model:", model_config["model"])

    # Research input
    initial_query = input("What would you like to research? ").strip()

    # Breadth
    try:
        breadth = int(input("Enter research breadth (recommended 2–10, default 4): ") or 4)
    except ValueError:
        breadth = 4

    # Depth
    try:
        depth = int(input("Enter research depth (recommended 1–5, default 2): ") or 2)
    except ValueError:
        depth = 2

    # Report or answer
    report_type = input("Do you want to generate a long report or a specific answer? (report/answer, default report): ").strip().lower()
    is_report = report_type != "answer"

    combined_query = initial_query

    if is_report:
        print("\nCreating research plan...")
        follow_up_questions = generate_feedback(
            query=initial_query,
            client=model_config["client"],
            model_name=model_config["model"]
        ) or []

        if follow_up_questions:
            print("\nTo better understand your research needs, please answer these follow-up questions:")
            answers = []
            for q in follow_up_questions:
                a = input(f"\n{q}\nYour answer: ")
                answers.append(a)

            qa_lines = [f"- Q: {q}\n  A: {a}" for q, a in zip(follow_up_questions, answers)]
            combined_query = (
                f"Initial Query: {initial_query}\n\n"
                f"Follow-up Questions and Answers:\n" + "\n".join(qa_lines)
            )

    print("\nStarting research...\n")
    result = await deep_research(query=combined_query, breadth=breadth, depth=depth)

    learnings = result.get("learnings", [])
    visited_urls = result.get("visitedUrls", [])
    source_cards = result.get("sourceCards", [])   # <-- NEW: pass this to write_final_report

    if learnings:
        print("\n\nLearnings:\n")
        print("\n".join(learnings))
    else:
        print("\n\nLearnings: (none)")

    print(f"\n\nVisited URLs ({len(visited_urls)}):\n")
    if visited_urls:
        print("\n".join(visited_urls))
    else:
        print("(none)")

    if is_report:
        print("\nWriting final report...")
        report = await write_final_report(
            prompt=combined_query,
            learnings=learnings,
            visited_urls=visited_urls,
            source_cards=source_cards   # <-- IMPORTANT for formatted references via ORKG metadata
        )
        Path("report.md").write_text(report, encoding="utf-8")
        print("\n\nFinal Report:\n\n" + report)
        print("\nReport has been saved to report.md")
    else:
        print("\nGenerating final answer...")
        answer = await write_final_answer(prompt=combined_query, learnings=learnings)
        Path("answer.md").write_text(answer, encoding="utf-8")
        print("\n\nFinal Answer:\n\n" + answer)
        print("\nAnswer has been saved to answer.md")

if __name__ == "__main__":
    asyncio.run(main())
