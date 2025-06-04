import sys
import os
import asyncio
import pandas as pd
from pathlib import Path

sys.path.append(".")

from main_experiments import main as run_experiment
from deep_research import TokenExpiredError

df = pd.read_excel("data/55-questions-ecology-clean.xlsx")
questions = df["Your research question."].tolist()

def run_batch_experiment(model, engine, depth, breadth, start=1, end=None):
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    model_name = "o3" if model == "o3" else "o3-mini"

    total_questions = questions[start-1:end] if end else questions[start-1:]

    for offset, question in enumerate(total_questions):
        i = start + offset
        report_path = report_dir / f"{i}_{model}_{engine}_d{depth}_b{breadth}.md"
        print(f"🔁 Frage {i}/50: {model} | {engine} | d={depth} b={breadth}")

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
            print(f"❌ Fehler bei Frage {i}: {e}")

        except TokenExpiredError as te:
            print(f"⚠️ Firecrawl-Token abgelaufen bei Frage {i}: {te}")
            print("↪ Batch wird hier abgebrochen, damit der Token gewechselt werden kann.")
            break

    print("✅ Batch abgeschlossen.")

if __name__ == "__main__":
    run_batch_experiment(
        model="o3",             # "o3" or "o3-mini"
        engine="firecrawl",     # "firecrawl" or "orkg"
        depth=4,
        breadth=1,
        start=6,
        end=50
    )
