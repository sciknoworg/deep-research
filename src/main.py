import argparse
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from feedback import generate_feedback
from deep_research import deep_research, write_final_report, write_final_answer

SAVE_MODELS       = int(os.getenv('SAVE_MODELS', '1'))
USE_FIRECRAWL_DEF = os.getenv('USE_FIRECRAWL_DEFAULT', '0') == '1'

def parse_args():
    p = argparse.ArgumentParser(description='Deep Research CLI')
    p.add_argument('--model', type=str, required=True,
                   help='HF model name or local path')
    return p.parse_args()

async def main():
    args       = parse_args()
    model_name = args.model

    # 1) Interaktive Abfrage von Breadth & Depth
    breadth = input("Number of search queries (breadth, default 4): ").strip()
    breadth = int(breadth) if breadth.isdigit() else 4

    depth = input("Recursion depth levels (1–5, default 2): ").strip()
    depth = int(depth) if depth.isdigit() else 2

    # 2) Such-Provider
    choice = input("Search provider (o=ORKG, f=Firecrawl, default o): ").strip().lower()
    use_fc = (choice == 'f') or USE_FIRECRAWL_DEF

    # 3) Initial-Query
    topic = input("What topic to research? ").strip()

    # 4) Follow-up-Fragen (nur bei Reports)
    is_report = True
    ans_mode  = input("Generate report or answer? (r/a, default r): ").strip().lower()
    if ans_mode == 'a':
        is_report = False

    questions, answers = [], []
    if is_report:
        print("\nGenerating follow-up questions…")
        questions = generate_feedback(topic, model_name, SAVE_MODELS)
        for q in questions:
            a = input(f"{q}\nAnswer: ")
            answers.append(a)

    # 5) Deep-Research-Workflow
    print("\nStarting deep research…")
    result = await deep_research(
        topic=topic,
        breadth=breadth,
        depth=depth,
        questions=questions,
        answers=answers,
        model_name=model_name,
        save_models=SAVE_MODELS,
        use_firecrawl=use_fc
    )

    learnings = result.get('learnings', [])
    print("\nLearnings:\n" + "\n".join(learnings))

    # 6) Final Report/Answer schreiben
    out_dir = Path(os.getenv('DATA_DIR_PATH', Path(__file__).parent.parent / 'data'))
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = topic.replace(' ', '_')

    if is_report:
        report = await write_final_report(
            topic, questions, answers, learnings, result.get('visited', []),
            model_name, SAVE_MODELS
        )
        path = out_dir / f"{fname}_report.md"
        path.write_text(report, encoding='utf-8')
        print(f"\nReport saved to: {path}")
    else:
        answer = await write_final_answer(
            topic, questions, answers, learnings,
            model_name, SAVE_MODELS
        )
        path = out_dir / f"{fname}_answer.md"
        path.write_text(answer, encoding='utf-8')
        print(f"\nAnswer saved to: {path}")

if __name__ == '__main__':
    asyncio.run(main())