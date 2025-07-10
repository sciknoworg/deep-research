import argparse, asyncio, os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
from feedback import generate_feedback
from deep_research import deep_research, write_final_report, write_final_answer

DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

SAVE_MODELS = int(os.getenv('SAVE_MODELS','1'))
USE_FIRECRAWL_DEFAULT = os.getenv('USE_FIRECRAWL_DEFAULT','0')=='1'

def parse_args():
    p = argparse.ArgumentParser(description="Deep Research CLI")
    p.add_argument('--model', type=str, required=True,
                   help='HuggingFace model (e.g. zephyr-7b-beta)')
    return p.parse_args()

async def main():
    args = parse_args()
    model = args.model

    breadth = input("Number of search queries (breadth, default 4): ").strip()
    breadth = int(breadth) if breadth.isdigit() else 4

    depth = input("Recursion depth (1–5, default 2): ").strip()
    depth = int(depth) if depth.isdigit() else 2

    choice = input("Search provider (o=ORKG, f=Firecrawl, default o): ").strip().lower()
    use_fc = (choice=='f') or USE_FIRECRAWL_DEFAULT

    topic = input("What topic to research? ").strip()
    mode  = input("Report or answer? (r/a, default r): ").strip().lower()
    is_rep = (mode!='a')

    questions, answers = [], []
    if is_rep:
        print("\nGenerating follow-up questions…")
        questions = generate_feedback(topic, model, SAVE_MODELS)
        for q in questions:
            a = input(f"{q}\nAnswer: ").strip()
            answers.append(a)

    print("\nStarting deep research…")
    result = await deep_research(
        topic=topic,
        breadth=breadth,
        depth=depth,
        questions=questions,
        answers=answers,
        model_name=model,
        save_models=SAVE_MODELS,
        use_firecrawl=use_fc
    )

    print("\nLearnings:")
    for ln in result['learnings']:
        print(" -", ln)

    stem = topic.replace(' ','_')
    if is_rep:
        out = await write_final_report(
            topic, questions, answers,
            result['learnings'], result['visited_urls'],
            model, SAVE_MODELS
        )
        path = DATA_DIR / f"{stem}_report.md"
        path.write_text(out, encoding='utf-8')
        print(f"\nReport saved to {path}")
    else:
        out = await write_final_answer(
            topic, questions, answers,
            result['learnings'], model, SAVE_MODELS
        )
        path = DATA_DIR / f"{stem}_answer.md"
        path.write_text(out, encoding='utf-8')
        print(f"\nAnswer saved to {path}")

if __name__ == '__main__':
    asyncio.run(main())
