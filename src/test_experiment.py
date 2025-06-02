import asyncio
from main_experiments import main as run_experiment

if __name__ == "__main__":
    # Beispiel-Frage
    test_question = "How does mowing maintain grasslands?"

    # Parameter für das Experiment
    model = "o3"                  # oder "o3-mini"
    engine = "orkg"              # oder "orkg"
    depth = 1
    breadth = 1
    output_path = "reports/test_run.md"

    # Experiment starten
    asyncio.run(run_experiment(
        initial_query=test_question,
        model_name=model,
        breadth=breadth,
        depth=depth,
        is_report=True,
        save_path=output_path,
        engine=engine
    ))
