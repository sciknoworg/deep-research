import sys
import os
import asyncio
import pandas as pd
from pathlib import Path

sys.path.append(".")

from main_experiments import main as run_experiment
from deep_research import TokenExpiredError


df = pd.read_excel("data/49-questions-nlp-numbered.xlsx")
questions = df["title"].tolist()

def run_batch_experiment(model, engine, depth, breadth, start=1, end=None):
    report_dir = Path("reports-nlp")
    report_dir.mkdir(exist_ok=True)

    model_name = "o3" if model == "o3" else "o3-mini"

    total_questions = questions[start-1:end] if end else questions[start-1:]

    for offset, question in enumerate(total_questions):
        i = start + offset
        report_path = report_dir / f"{i}_{model}_{engine}_d{depth}_b{breadth}.md"
        print(f"🔁 Frage {i}/49: {model} | {engine} | d={depth} b={breadth}")

        try:
            asyncio.run(run_experiment(
                initial_query=question,
                model_name=model_name,
                breadth=breadth,
                depth=depth,
                is_report=True,
                save_path=str(report_path),
                engine=engine
            ))
        except Exception as e:
            print(f"❌ Error at {i}: {e}")

        except TokenExpiredError as te:
            print(f"⚠️ Firecrawl-Token run out at: {i}: {te}")
            break

    print("✅ Batch finished")

if __name__ == "__main__":
    run_batch_experiment(
        model="o3-mini",             # "o3" or "o3-mini"
        engine="orkg",     # "firecrawl" or "orkg"
        depth=4,
        breadth=4,
        start=1,
        end=49

    )
