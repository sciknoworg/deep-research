import asyncio
import os
from pathlib import Path
import json
import tempfile
from deep_research import deep_research, write_final_report, write_final_answer
from feedback import generate_feedback
from ai.llms import call_huggingface_on_cluster

def write_to_input_file(data: dict):
    Path("data").mkdir(exist_ok=True)
    Path("data/input.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

async def wait_for_output_file(timeout=600):
    output_file = Path("data/output.json")
    for _ in range(timeout):
        if output_file.exists():
            return json.loads(output_file.read_text(encoding="utf-8"))
        await asyncio.sleep(1)
    raise TimeoutError("Timeout waiting for output.json")

async def main():
    model_input = input("Enter a model to run on the cluster (default: deepseek): ").strip() or "deepseek"
    initial_query = input("What would you like to research? ").strip()

    try:
        breadth = int(input("Enter research breadth (recommended 2–10, default 4): ") or 4)
    except ValueError:
        breadth = 4

    try:
        depth = int(input("Enter research depth (recommended 1–5, default 2): ") or 2)
    except ValueError:
        depth = 2

    report_type = input("Do you want to generate a long report or a specific answer? (report/answer, default report): ").strip().lower()
    is_report = report_type != "answer"

    combined_query = initial_query
    conversation = ["Initial Query: " + initial_query]

    if is_report:
        for i in range(3):
            print("\nGenerating follow-up question...")
            write_to_input_file({
                "type": "followup",
                "query": "\n".join(conversation),
                "model": model_input
            })
            call_huggingface_on_cluster(prompt="\n".join(conversation), model_name=model_input)
            followup_result = await wait_for_output_file()

            follow_up_questions = followup_result.get("questions", [])
            if not follow_up_questions:
                break
            follow_up_question = follow_up_questions[0]
            print(f"\n{follow_up_question}")
            answer = input("Your answer: ")
            conversation.append(f"Q: {follow_up_question}\nA: {answer}")

        combined_query = "\n".join(conversation)
        Path("data/conversation_log.json").write_text(json.dumps(conversation, indent=2), encoding="utf-8")

    print("\nStarting research...\n")
    result = await deep_research(query=combined_query, breadth=breadth, depth=depth)
    learnings = result["learnings"]
    visited_urls = result["visitedUrls"]

    print("\n\nLearnings:\n\n" + "\n".join(learnings))
    print(f"\n\nVisited URLs ({len(visited_urls)}):\n\n" + "\n".join(visited_urls))

    if is_report:
        print("Writing final report...")
        report = await write_final_report(prompt=combined_query, learnings=learnings, visited_urls=visited_urls)
        Path("report.md").write_text(report, encoding="utf-8")
        print("\n\nFinal Report:\n\n" + report)
        print("\nReport has been saved to report.md")
    else:
        print("Generating final answer...")
        answer = await write_final_answer(prompt=combined_query, learnings=learnings)
        Path("answer.md").write_text(answer, encoding="utf-8")
        print("\n\nFinal Answer:\n\n" + answer)
        print("\nAnswer has been saved to answer.md")

if __name__ == "__main__":
    asyncio.run(main())
