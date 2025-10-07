import re
import json
import argparse
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt

from judge_core import (
    get_llm_caller, load_topic_dict, judge_metric, EXAMPLES_TOPK,
)

# ---------- Adjustable CLI defaults ----------
DEFAULT_REPORT = "../data/ecology-reports/orkg-ask/o3/8_o3_orkg_d4_b4.md"
DEFAULT_TOPIC  = "ecology"         # "ecology" | "nlp"
DEFAULT_OUT    = "out"
DEFAULT_MODEL  = "o4-mini"         # solid for strict structured scoring
MAKE_PLOT      = True
BAR_FIGSIZE    = (9, 4.5)

METRICS = ["depth", "breadth", "rigor", "innovation", "gap"]


# ---------- Small helpers ----------
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def parse_config_from_filename(stem: str) -> Tuple[int, int, str]:
    m = re.search(r"d(\d+)_b(\d+)", stem)
    if not m:
        return 1, 1, "d1_b1"
    d, b = int(m.group(1)), int(m.group(2))
    return d, b, f"d{d}_b{b}"

def to_0_1(v: int) -> float:
    return round(max(0.0, min(100.0, float(v))) / 100.0, 6)


# ---------- Outputs ----------
def save_scores_only_json(out_dir: Path, base: str, scores0_100: Dict[str, int], overall100: int) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{base}_scores_only.json"
    obj = {**scores0_100, "overall_computed": overall100}
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return p

def save_repo_row_csv(out_dir: Path, base: str, config_str: str,
                      scores0_100: Dict[str, int], overall01: float) -> Path:
    import csv
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{base}_repo_compatible_row.csv"
    row = {
        "config": config_str,
        "depth_score": to_0_1(scores0_100["depth"]),
        "breadth_score": to_0_1(scores0_100["breadth"]),
        "rigor_score": to_0_1(scores0_100["rigor"]),
        "innovation_score": to_0_1(scores0_100["innovation"]),
        "gap_score": to_0_1(scores0_100["gap"]),
        "overall_quality": round(overall01, 6),
    }
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader(); w.writerow(row)
    return p

def plot_quality_bars(figures_dir: Path, scores0_100: Dict[str, int], title: str) -> Path:
    figures_dir.mkdir(parents=True, exist_ok=True)
    vals01 = [
        to_0_1(scores0_100["depth"]),
        to_0_1(scores0_100["breadth"]),
        to_0_1(scores0_100["rigor"]),
        to_0_1(scores0_100["innovation"]),
        to_0_1(scores0_100["gap"]),
    ]
    overall01 = float(np.mean(vals01))
    labels = ["depth_score","breadth_score","rigor_score","innovation_score","gap_score","overall_quality"]
    values = vals01 + [overall01]

    fig = plt.figure(figsize=BAR_FIGSIZE)
    ax = plt.gca()
    xs = np.arange(len(labels))
    ax.bar(xs, values)
    ax.set_xticks(xs); ax.set_xticklabels([l.replace("_"," ") for l in labels])
    ax.set_ylim(0, 1.05); ax.set_ylabel("Score (0..1)")
    ax.set_title(title)
    for i, v in enumerate(values):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    out = figures_dir / "quality_dimensions.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=DEFAULT_REPORT, help="Path to a single DeepResearch .md report")
    ap.add_argument("--topic",  default=DEFAULT_TOPIC,  choices=["ecology","nlp"], help="Domain (ecology|nlp)")
    ap.add_argument("--out_dir",default=DEFAULT_OUT,    help="Output directory for JSON/CSV/plots")
    ap.add_argument("--model",  default=DEFAULT_MODEL,  help="OpenAI model (e.g., o4-mini).")
    ap.add_argument("--no_plot", action="store_true",   help="Skip plotting")
    args = ap.parse_args()

    report_path = Path(args.report).resolve()
    assert report_path.exists(), f"Report not found: {report_path}"
    out_dir = Path(args.out_dir).resolve()
    figures_dir = out_dir / "figures"
    prompts_dir = out_dir / "prompts"

    # Load report and dicts
    report_md = read_text(report_path)
    V = load_topic_dict(args.topic)

    # Caller
    call_llm, model_used, used_wrapper = get_llm_caller(args.model)

    # Score each metric (and save the exact prompt to disk for audit)
    scores0_100: Dict[str, int] = {}
    for m in METRICS:
        prompt_path = prompts_dir / f"{m}.json"
        score = judge_metric(
            call_llm=call_llm,
            model_used=model_used,
            topic=args.topic,
            report_md=report_md,
            metric=m,
            V=V,
            save_prompt_to=prompt_path
        )
        scores0_100[m] = score

    # Overall (local)
    vals01 = [to_0_1(scores0_100[m]) for m in METRICS]
    overall01 = float(np.mean(vals01)) if vals01 else 0.0
    overall100 = int(round(overall01 * 100.0))

    # Outputs
    stem = report_path.stem
    _d, _b, config_str = parse_config_from_filename(stem)
    scores_json_path = save_scores_only_json(out_dir, stem, scores0_100, overall100)
    row_csv = save_repo_row_csv(out_dir, stem, config_str, scores0_100, overall01)
    if not args.no_plot and MAKE_PLOT:
        title = f"{stem} — {args.topic} — LLMJ metric-wise ({model_used})"
        plot_quality_bars(figures_dir, scores0_100, title)

    # Console (scores only)
    print(json.dumps({**scores0_100, "overall_computed": overall100}, ensure_ascii=False))
    print(f"Wrote: {scores_json_path}")
    print(f"Wrote: {row_csv}")
    if not args.no_plot and MAKE_PLOT:
        print(f"Wrote: {figures_dir / 'quality_dimensions.png'}")
    print(f"Wrote prompts: {prompts_dir}/<metric>.json")


if __name__ == "__main__":
    main()
