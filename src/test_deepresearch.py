import asyncio
from deep_research import deep_research, write_final_answer, write_final_report

def test_deep_research_pipeline():
    # Basic test prompt
    test_query = "What are the main applications of AI in ecological monitoring?"

    # Parameters for breadth and depth of the research tree
    breadth = 2
    depth = 1

    async def run_pipeline():
        print("Running deep research...")
        result = await deep_research(
            query=test_query,
            breadth=breadth,
            depth=depth,
            learnings=[],
            visited_urls=[],  # ✅ Corrected name
        )

        learnings = result["learnings"]
        urls = result["visitedUrls"]

        print("\nLearnings:")
        for l in learnings:
            print(f"- {l}")

        print("\nVisited URLs:")
        for url in urls:
            print(f"- {url}")

        assert isinstance(learnings, list) and len(learnings) > 0, "No learnings returned"
        assert isinstance(urls, list), "Visited URLs should be a list"

        print("\nGenerating final report...")
        report = await write_final_report(
            prompt=test_query,
            learnings=learnings,
            visited_urls=urls,
        )
        assert isinstance(report, str) and len(report) > 0, "Empty report generated"
        print("\nReport generated successfully.")

        print("\nGenerating final answer...")
        answer = await write_final_answer(
            prompt=test_query,
            learnings=learnings,
        )
        assert isinstance(answer, str) and len(answer) > 0, "Empty answer generated"
        print(f"\nFinal Answer: {answer}")

    # Run the async pipeline
    asyncio.run(run_pipeline())

if __name__ == "__main__":
    test_deep_research_pipeline()
