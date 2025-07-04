import asyncio
import os
from pathlib import Path
from feedback import generate_feedback
from deep_research import deep_research, write_final_report, write_final_answer
from ai.llms import ModelConfig, MODEL_ALIASES

async def main():
    # Initialize and select model
    config = ModelConfig()
    model_config = config.get_model_config()
    print("Available model aliases:", ", ".join(MODEL_ALIASES.keys()))
    alias = input(f"Choose alias (default '{os.getenv('DEFAULT_MODEL_ALIAS', 'zephyr')}'): ").strip()
    if alias:
        os.environ['DEFAULT_MODEL_ALIAS'] = alias
        config = ModelConfig()
        model_config = config.get_model_config()
    print("Using model:", model_config['model'])

    # Research inputs
    topic = input("What would you like to research? ").strip()
    breadth = int(input("Enter breadth (2–10, default 4): ") or 4)
    depth = int(input("Enter depth (1–5, default 2): ") or 2)
    is_report = input("Report or answer? (report/answer, default report): ").strip().lower() != "answer"

    # Feedback stage
    combined_query = topic
    if is_report:
        print("Generating feedback questions...")
        questions = await generate_feedback(topic)
        answers = []
        for q in questions:
            ans = input(f"{q}Answer: ")
            answers.append(ans)
        follow_ups = "".join([f"Q: {q}A: {a}" for q, a in zip(questions, answers)])
        combined_query = f"Initial: {topic}{follow_ups}"

    # Deep research stage
    print("Running deep research...")
    result = await deep_research(query=combined_query, breadth=breadth, depth=depth)
    learnings = result.get('learnings', [])
    visited_urls = result.get('visitedUrls', [])

    print("Learnings:" + "".join(learnings))

    # Save outputs
    data_dir = Path(os.getenv('DATA_DIR_PATH', Path(__file__).parent.parent / 'data'))
    data_dir.mkdir(parents=True, exist_ok=True)
    filename = topic.replace(' ', '_')
    if is_report:
        report = await write_final_report(prompt=combined_query, learnings=learnings, visited_urls=visited_urls)
        path = data_dir / f"{filename}_report.md"
        path.write_text(report, encoding='utf-8')
        print(f"Report saved to {path}")
    else:
        answer = await write_final_answer(prompt=combined_query, learnings=learnings)
        path = data_dir / f"{filename}_answer.md"
        path.write_text(answer, encoding='utf-8')
        print(f"Answer saved to {path}")

if __name__ == "__main__":
    asyncio.run(main())
