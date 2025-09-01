import asyncio
import os
from pathlib import Path

from deep_research import deep_research, write_final_report, write_final_answer
from feedback import generate_feedback
from ai.llms import ModelConfig

async def main(initial_query, model_name="o3-mini", breadth=4, depth=2, is_report=True, save_path="report.md", engine="orkg"):

    os.environ["CUSTOM_MODEL"] = model_name
    os.environ["RESEARCH_PROVIDER"] = engine

    config = ModelConfig()
    model_config = config.get_model_config()

    print("Using model:", model_config['model'])

    combined_query = initial_query

    if is_report:
        print("\nCreating research plan...")
        follow_up_questions = generate_feedback(query=initial_query, client=model_config['client'], model_name=model_config['model'])

        print("\nTo better understand your research needs, please answer these follow-up questions:")
        answers = ["", "", ""] 

        qa_block = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(follow_up_questions, answers)])
        combined_query = f"""
                        Initial Query: {initial_query}
                        Follow-up Questions and Answers:
                        {qa_block}
                        """

    print("\nStarting research...\n")
    result = await deep_research(query=combined_query, breadth=breadth, depth=depth)
    learnings = result["learnings"]
    visited_urls = result["visitedUrls"]

    print("\n\nLearnings:\n\n" + "\n".join(learnings))
    print(f"\n\nVisited URLs ({len(visited_urls)}):\n\n" + "\n".join(visited_urls))

    if is_report:
        print("Writing final report...")
        report = await write_final_report(prompt=combined_query, learnings=learnings, visited_urls=visited_urls)
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        Path(save_path).write_text(report, encoding="utf-8")
        print("\n\nFinal Report:\n\n" + report)
        print(f"\nReport has been saved to {save_path}")
    else:
        print("Generating final answer...")
        answer = await write_final_answer(prompt=combined_query, learnings=learnings)
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        Path(save_path).write_text(answer, encoding="utf-8")
        print("\n\nFinal Answer:\n\n" + answer)
        print(f"\nAnswer has been saved to {save_path}")