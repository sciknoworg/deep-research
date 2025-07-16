import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine mode: use HF (cluster batch) or API
USE_CLUSTER = os.getenv('USE_CLUSTER', '1') == '1'

# Ensure data directory exists
DATA_DIR = Path(os.getenv('DATA_DIR_PATH', Path(__file__).parent.parent / 'data'))
DATA_DIR.mkdir(parents=True, exist_ok=True)

if USE_CLUSTER:
    from deep_research_cluster import deep_research, write_final_report, write_final_answer
    from feedback import generate_feedback_cluster
    MODEL      = os.getenv('HF_MODEL')
    SAVE_MODELS= int(os.getenv('SAVE_MODELS','0'))
else:
    from deep_research_api import deep_research, write_final_report, write_final_answer
    from feedback import generate_feedback
    from ai.llms import OpenAIClient
    MODEL      = os.getenv('OPENAI_MODEL')
    SAVE_MODELS= int(os.getenv('SAVE_MODELS','0'))
    API_CLIENT  = OpenAIClient(os.getenv('OPENAI_KEY'))

async def main():
    # Interactive inputs
    breadth = int(input("Number of search queries (default 4): ") or 4)
    depth   = int(input("Recursion depth (1–5, default 2): ") or 2)
    topic   = input("What topic to research? ").strip()
    mode    = input("Report or answer? (r/a, default r): ").strip().lower()
    qa_mode = (mode != 'a')

    if qa_mode:
    # Generate follow-up questions
        print("\nGenerating follow-up questions…")
        if USE_CLUSTER:
            questions = generate_feedback_cluster(topic, model_name=os.getenv('HF_MODEL'), save_models=int(os.getenv('SAVE_MODELS', '0')))
        else:
            questions = generate_feedback(topic, API_CLIENT, MODEL)
        answers = []
        for q in questions:
            a = input(f"{q}\nAnswer: ").strip()
            answers.append(a)

    print("Starting deep research…")
    # Execute research
    if USE_CLUSTER:
        result = await deep_research(
            topic, breadth, depth,
            questions, answers,
            model_name=os.getenv('HF_MODEL'),
            save_models=int(os.getenv('SAVE_MODELS', '0'))
        )
    else:
        result = await deep_research(
            topic, breadth, depth,
            questions, answers,
            os.getenv('OPENAI_MODEL'),
            save_models=int(os.getenv('SAVE_MODELS', '0')),
            api_key=os.getenv('OPENAI_KEY'),
            provider=os.getenv('RESEARCH_PROVIDER', 'orkg')
        )

    print("Learnings:")
    for ln in result.get('learnings', []):
        print(" -", ln)

    # Generate and save report or answer
    if qa_mode:
        if USE_CLUSTER:
            output = await write_final_report(
                topic, questions, answers,
                result.get('learnings', []), result.get('visited_urls', []),
                model_name=os.getenv('HF_MODEL'),
                save_models=int(os.getenv('SAVE_MODELS', '0'))
            )
        else:
            output = await write_final_report(
                topic, questions, answers,
                result.get('learnings', []), result.get('visited_urls', []),
                api_key=os.getenv('OPENAI_KEY')
            )
        suffix = 'report'
    else:
        if USE_CLUSTER:
            output = await write_final_answer(
                topic, questions, answers,
                result.get('learnings', []),
                model_name=os.getenv('HF_MODEL'),
                save_models=int(os.getenv('SAVE_MODELS', '0'))
            )
        else:
            output = await write_final_answer(
                topic, questions, answers,
                result.get('learnings', []),
                api_key=os.getenv('OPENAI_KEY')
            )
        suffix = 'answer'

    path = DATA_DIR / f"{topic.replace(' ','_')}_{suffix}.md"
    path.write_text(output, encoding='utf-8')
    print(f"Saved {suffix} to {path}")

if __name__ == '__main__':
    asyncio.run(main())