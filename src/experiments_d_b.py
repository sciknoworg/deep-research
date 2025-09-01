from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Iterable, Tuple, Union

from main_experiments import main as run_one


QUESTION: str = "Weather in North Germany Over the Last 100 Years"  

# You can write:
#   MODELS = "o3"            # single model (string)  
#   MODELS = ("o3",)         # single model (tuple)   
#   MODELS = ("o3", "o3-mini")   # multiple models    
MODELS = "o3"

# You can write:
#   DEPTHS = 3               # single value 
#   DEPTHS = (1, 2, 3)       # explicit set 
#   DEPTHS = (1, 5)          # expands to 1,2,3,4,5 
DEPTHS = 5

# Same rules as DEPTHS:
BREADTHS = 10

ENGINE = "orkg"                   # "orkg" or "firecrawl"
OUTPUT_DIR = "../data/reports-db" # relative to this file
SKIP_EXISTING = True              # do not rerun if output file already exists

# ======================

def _sanitize(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-._" else "_" for c in s)

def _as_tuple_one(x: Union[str, int, Iterable]) -> Tuple:
    """Coerce a possibly scalar value into a tuple with 1+ items."""
    if isinstance(x, tuple):
        return x
    if isinstance(x, list):
        return tuple(x)
    if isinstance(x, str):
        return (x.strip(),) if x.strip() else tuple()
    if isinstance(x, int):
        return (x,)
    try:
        return tuple(x)  # type: ignore
    except TypeError:
        return (x,)

def _expand_numeric_grid(x: Union[int, Tuple[int, ...]]) -> Tuple[int, ...]:
    """
    Expand a numeric grid spec:
      - int          -> (int,)
      - (a, b)       -> inclusive range a..b (if b > a)
      - (a, b, ...)  -> returned as-is
    """
    t = _as_tuple_one(x)
    if len(t) == 1 and isinstance(t[0], int):
        return (int(t[0]),)
    if len(t) == 2 and all(isinstance(v, int) for v in t) and t[1] > t[0]:
        start, end = int(t[0]), int(t[1])
        return tuple(range(start, end + 1))
    # validate ints
    vals = tuple(int(v) for v in t)
    return vals

async def run() -> None:
    base_dir = Path(__file__).resolve().parent
    out_dir = (base_dir / OUTPUT_DIR).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    models = _as_tuple_one(MODELS)
    if not models:
        print("No models configured (MODELS is empty). Aborting.")
        return

    depths = _expand_numeric_grid(DEPTHS)
    breadths = _expand_numeric_grid(BREADTHS)

    question = (QUESTION or "").strip() or input("Enter your research question: ").strip()
    if not question:
        print("No question provided. Aborting.")
        return

    print(f"\nQuestion: {question}")
    print(f"Engine:   {ENGINE}")
    print(f"Models:   {models}")
    print(f"Depths:   {depths}")
    print(f"Breadths: {breadths}\n")

    for model in models:
        if not model:
            continue
        for depth in depths:
            for breadth in breadths:
                filename = f"{_sanitize(model)}_{ENGINE}_d{depth}_b{breadth}.md"
                save_path = out_dir / filename

                if SKIP_EXISTING and save_path.exists():
                    print(f"↷ Skip existing: {save_path.name}")
                    continue

                print(f"→ Running: model={model} | engine={ENGINE} | d={depth} | b={breadth}")
                try:
                    await run_one(
                        initial_query=question,
                        model_name=str(model),
                        breadth=int(breadth),
                        depth=int(depth),
                        is_report=True,
                        save_path=str(save_path),
                        engine=ENGINE,
                    )
                    print(f"  ✓ Saved: {save_path}")
                except Exception as e:
                    print(f"  ✗ Failed (model={model}, d={depth}, b={breadth}): {e}")

    print("\n✅ Done.")

if __name__ == "__main__":
    asyncio.run(run())
