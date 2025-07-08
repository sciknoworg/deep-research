import argparse
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from feedback import generate_feedback
from deep_research import deep_research, write_final_report, write_final_answer

# Flag to save models locally (1=save, 0=don't save)
SAVE_MODELS = 1
# Default search provider fallback (False=ORKG, True=Firecrawl)
USE_FIRECRAWL_DEFAULT = False

def parse_args():
    parser = argparse.ArgumentParser(description='Deep Research CLI')
    parser.add_argument('--model',    type=str, required=True, help='Huggingface model name or local path')
    parser.add_argument('--breadth',  type=int, default=4, help='Search breadth (2–10)')
    parser.add_argument('--depth',    type=int, default=2, help='Search depth (1–5)')
    parser.add_argument('--answer',   action='store_true', help='Generate concise answer instead of report')
    return parser.parse_args()

async def main():
    args = parse_args()
    model_name   = args.model
    breadth      = args.breadth
    depth        = args.depth
    is_report    = not args.answer
    use_fc_input = input("Choose search provider: ORKG or Firecrawl? (o/f, default o): ").strip().lower()
    use_firecrawl = (use_fc_input == 'f') or USE_FIRECRAWL_DEFAULT
    topic        = input('What topic would you like to research? ').strip()

    questions, answers = [], []
    if is_report:
        print('Generating follow-up questions...')
        questions = generate_feedback(topic, model_name, SAVE_MODELS)
        for q in questions:
            answers.append(input(f"{q}\nAnswer: "))

    print('Starting deep research...')
    result = await deep_research(
        topic,
        breadth,
        depth,
        questions,
        answers,
        model_name=model_name,
        save_models=SAVE_MODELS,
        use_firecrawl=use_firecrawl
    )
    learnings = result.get('learnings', [])
    print('Learnings:\n' + '\n'.join(learnings))

    out_dir = Path(os.getenv('DATA_DIR_PATH', Path(__file__).parent.parent / 'data'))
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = topic.replace(' ', '_')
    if is_report:
        report = await write_final_report(topic, questions, answers, learnings, result.get('visited', []), model_name=model_name, save_models=SAVE_MODELS)
        path = out_dir / f"{fname}_report.md"
        path.write_text(report, encoding='utf-8')
        print(f'Report saved to: {path}')
    else:
        answer = await write_final_answer(topic, questions, answers, learnings, model_name=model_name, save_models=SAVE_MODELS)
        path = out_dir / f"{fname}_answer.md"
        path.write_text(answer, encoding='utf-8')
        print(f'Answer saved to: {path}')

if __name__ == '__main__':
    asyncio.run(main())