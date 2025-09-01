import asyncio
from pathlib import Path

from ai.llms import ModelConfig
from feedback import generate_feedback
from deep_research import deep_research, write_final_report

# ==== Configuration ==========================================================
TOPIC = "tidal forces north german sea" 
CONFIGS = [(1, 1),(2, 2),(3, 3),(4, 4),(10, 5)] 
OUT_DIR = Path("test_data")
# ============================================================================

async def run_once(topic: str, breadth: int, depth: int, model_cfg: dict) -> Path:

    try:
        questions = generate_feedback(
            query=topic,
            client=model_cfg["client"],
            model_name=model_cfg["model"]
        )
    except Exception:
        questions = []

    qa_block_lines = [f"Q: {q} - A: " for q in questions]
    combined_query = (
        f"Initial Query: {topic}\n"
        f"Follow-up Questions and Answers:\n"
        + "\n".join(qa_block_lines)
    )

    print(f"\n--- Running breadth={breadth}, depth={depth} ---")
    res = await deep_research(query=combined_query, breadth=breadth, depth=depth)
    learnings = res.get("learnings", [])
    visited_urls = res.get("visitedUrls", [])

    print(f"Learnings: {len(learnings)} | Sources collected: {len(visited_urls)}")

    report_md = await write_final_report(
        prompt=combined_query,
        learnings=learnings,
        visited_urls=visited_urls
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"report_b{breadth}_d{depth}.md"
    out_path.write_text(report_md, encoding="utf-8")
    print(f"Saved: {out_path}")
    return out_path

async def main():
    cfg = ModelConfig().get_model_config()
    print("Using model:", cfg["model"])

    for b, d in CONFIGS:
        try:
            await run_once(TOPIC, b, d, cfg)
        except Exception as e:
            print(f"[WARN] Run b={b}, d={d} failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
