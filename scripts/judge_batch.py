from __future__ import annotations
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

# ---- local imports from your core (no sampling params) ----
try:
    from .judge_core import get_llm_caller, load_topic_dict, judge_metric  # type: ignore
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from judge_core import get_llm_caller, load_topic_dict, judge_metric  # type: ignore


# ================= User-adjustable defaults (overridable via CLI) =================
SETTINGS = {
    "FOLDER": "../data/ecology-reports/orkg-ask/o3-mini",
    "OUT_DIR": "LLMJ-5-mini-ecology-o3-mini",
    "TOPIC": None,            # "ecology" | "nlp" | None (infer from path)
    "MODEL": "gpt-5-mini-2025-08-07",
    "FILE_GLOB": "*.md",      # only top-level; adjust to "**/*.md" if you need recursion
    "MAX_FILES": 0,           # 0 = no cap
    "SAVE_PROMPTS": False,    # store system+user prompt JSON per metric under each question folder
    "FIGSIZE": (16, 12),      # 6-panel figure size (like your screenshot)
}

# Five metrics = five separate LLM calls
METRICS = ["depth", "breadth", "rigor", "innovation", "gap"]

# Fixed order of the four configs required in all six panels
CONFIG_ORDER = ["d1_b1", "d1_b4", "d4_b1", "d4_b4"]


# ================= Small helpers =================
def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def detect_topic_from_path(folder: Path) -> str | None:
    parts = [s.lower() for s in folder.parts]
    if any("ecology" in s for s in parts): return "ecology"
    if any("nlp" in s for s in parts): return "nlp"
    return None

def detect_engine_from_path(folder: Path) -> str:
    name = folder.name.lower()
    if "o3-mini" in name or "o3mini" in name or "o3_mini" in name: return "o3-mini"
    if "o3" in name: return "o3"
    return name

def to_0_1(v: int) -> float:
    return round(max(0.0, min(100.0, float(v))) / 100.0, 6)

def parse_config_from_filename(stem: str) -> Tuple[int, int, str]:
    """
    Extracts the dX_bY pattern; defaults to d1_b1 if absent.
    Returns (d, b, "dX_bY").
    """
    m = re.search(r"d(\d+)_b(\d+)", stem)
    if not m:
        return 1, 1, "d1_b1"
    d, b = int(m.group(1)), int(m.group(2))
    return d, b, f"d{d}_b{b}"

def find_reports(folder: Path, pattern: str) -> List[Path]:
    """
    Returns top-level matches (use folder.rglob if you want recursive).
    """
    return sorted(folder.glob(pattern))


# ================= Per-question & batch I/O =================
def write_question_csv(q_dir: Path, report_path: Path,
                       scores0_100: Dict[str, int], overall01: float) -> Path:
    """
    Writes exactly ONE CSV for the question:
    - normalized 0..1 scores (for plotting)
    - raw 0..100 scores (for auditing)
    - config and report path
    """
    import csv
    q_dir.mkdir(parents=True, exist_ok=True)
    csv_path = q_dir / "scores.csv"

    _d, _b, cfg = parse_config_from_filename(report_path.stem)
    row = {
        "report_stem": report_path.stem,
        "config": cfg,
        "depth": to_0_1(scores0_100["depth"]),
        "breadth": to_0_1(scores0_100["breadth"]),
        "rigor": to_0_1(scores0_100["rigor"]),
        "innovation": to_0_1(scores0_100["innovation"]),
        "gap": to_0_1(scores0_100["gap"]),
        "overall": round(overall01, 6),
        "depth_raw": scores0_100["depth"],
        "breadth_raw": scores0_100["breadth"],
        "rigor_raw": scores0_100["rigor"],
        "innovation_raw": scores0_100["innovation"],
        "gap_raw": scores0_100["gap"],
        "overall_raw": int(round(overall01 * 100.0)),
        "report_path": str(report_path),
    }
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader(); w.writerow(row)
    return csv_path


def save_batch_reports_csv(out_dir: Path, rows: List[Dict[str, str | float]]) -> Path:
    """
    One row per report (0..1 scores + config + path).
    """
    import csv
    p = out_dir / "batch_reports.csv"
    if not rows:
        p.write_text("", encoding="utf-8")
        return p
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    return p


def aggregate_by_config(rows: List[Dict[str, str | float]]) -> List[Dict[str, float | str | int]]:
    """
    Aggregates to config-level mean/std with a FIXED four-config order.
    Missing configs are included with n=0 and zeros for means/stds (keeps panel axes stable).
    """
    from collections import defaultdict
    bucket: Dict[str, List[Dict[str, float]]] = defaultdict(list)
    for r in rows:
        cfg = str(r["config"])
        bucket[cfg].append(r)  # type: ignore

    def mean_std(values: List[float]) -> Tuple[float, float]:
        if not values: return 0.0, 0.0
        a = np.array(values, dtype=float)
        return float(a.mean()), float(a.std(ddof=0))

    out: List[Dict[str, float | str | int]] = []
    for cfg in CONFIG_ORDER:
        items = bucket.get(cfg, [])
        def col(k: str) -> List[float]:
            return [float(x[k]) for x in items]
        row = {"config": cfg, "n_docs": len(items)}
        for k in ["depth", "breadth", "rigor", "innovation", "gap", "overall"]:
            m, s = mean_std(col(k))
            row[f"{k}_mean"] = round(m, 6)
            row[f"{k}_std"]  = round(s, 6)
        out.append(row)
    return out


def save_batch_summary_csv(out_dir: Path, summary_rows: List[Dict[str, float | str | int]]) -> Path:
    """
    Writes config-level mean/std table in fixed order.
    """
    import csv
    p = out_dir / "batch_config_summary.csv"
    if not summary_rows:
        p.write_text("", encoding="utf-8")
        return p
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        w.writeheader(); w.writerows(summary_rows)
    return p


def plot_group_6panels(out_dir: Path,
                       summary_rows: List[Dict[str, float | str | int]],
                       title: str,
                       figsize=(16, 12)) -> Path:
    """
    Creates the 6-panel figure. Each panel shows the same fixed four configs
    (d1_b1, d1_b4, d4_b1, d4_b4) as bars with mean (0..1) and std error bars.
    """
    if not summary_rows:
        return out_dir / "quality_dimensions.png"

    # Map summary rows by config for fast lookup
    by_cfg = {r["config"]: r for r in summary_rows}
    cfgs = CONFIG_ORDER  # fixed order

    def take_means_stds(name: str):
        means = [float(by_cfg[cfg][f"{name}_mean"]) if cfg in by_cfg else 0.0 for cfg in cfgs]
        stds  = [float(by_cfg[cfg][f"{name}_std"])  if cfg in by_cfg else 0.0 for cfg in cfgs]
        return means, stds

    dims = ["depth", "breadth", "rigor", "innovation", "gap", "overall"]
    titles = [
        "Research Depth Score", "Research Breadth Score", "Scientific Rigor Score",
        "Innovation Score", "Research Gap Score", "Overall Quality Score"
    ]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.ravel()

    for i, (dim, dim_title) in enumerate(zip(dims, titles)):
        ax = axes[i]
        means, stds = take_means_stds(dim)
        xs = np.arange(len(cfgs))
        ax.bar(xs, means, yerr=stds, capsize=5)
        ax.set_title(dim_title)
        ax.set_xticks(xs); ax.set_xticklabels(cfgs)
        ax.set_ylim(0.0, 1.05); ax.set_ylabel("Score (0..1)")
        for j, v in enumerate(means):
            ax.text(j, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=9)

    fig.suptitle(title, fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    out = out_dir / "quality_dimensions.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ================= Main =================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", default=SETTINGS["FOLDER"], help="Folder with reports (*.md)")
    ap.add_argument("--out_dir", default=SETTINGS["OUT_DIR"], help="Output root folder")
    ap.add_argument("--topic", default=SETTINGS["TOPIC"], help="ecology|nlp; if omitted, inferred from path")
    ap.add_argument("--model", default=SETTINGS["MODEL"], help="Model name (e.g., o4-mini)")
    ap.add_argument("--file_glob", default=SETTINGS["FILE_GLOB"], help="File glob (default: *.md)")
    ap.add_argument("--max_files", type=int, default=SETTINGS["MAX_FILES"], help="Max files to process (0 = all)")
    ap.add_argument("--save_prompts", action="store_true", default=SETTINGS["SAVE_PROMPTS"], help="Store prompts per question")
    args = ap.parse_args()

    in_folder = Path(args.folder).resolve()
    assert in_folder.exists() and in_folder.is_dir(), f"Folder not found: {in_folder}"
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    topic = (args.topic or "").strip().lower()
    if not topic:
        topic = detect_topic_from_path(in_folder) or ""
    assert topic in {"ecology", "nlp"}, "Please pass --topic ecology|nlp (or make it inferable from path)."

    engine = detect_engine_from_path(in_folder)

    # Load dictionaries & model caller
    V = load_topic_dict(topic)
    call_llm, model_used, _ = get_llm_caller(args.model)

    files = find_reports(in_folder, args.file_glob)
    if args.max_files > 0:
        files = files[: args.max_files]
    assert files, f"No files under {in_folder} matching {args.file_glob}"

    batch_rows: List[Dict[str, str | float]] = []

    for report_path in files:
        report_md = read_text(report_path)

        # Per-question folder (flat structure)
        q_dir = out_dir / report_path.stem
        q_dir.mkdir(parents=True, exist_ok=True)
        prompts_dir = q_dir / "prompts"
        if args.save_prompts:
            prompts_dir.mkdir(parents=True, exist_ok=True)

        # Score each metric with a separate call
        scores0_100: Dict[str, int] = {}
        for m in METRICS:
            save_prompt_to = (prompts_dir / f"{m}.json") if args.save_prompts else None
            score = judge_metric(
                call_llm=call_llm,
                model_used=model_used,
                topic=topic,
                report_md=report_md,
                metric=m,
                V=V,
                save_prompt_to=save_prompt_to
            )
            scores0_100[m] = score

        # Local overall (mean of normalized)
        vals01 = [to_0_1(scores0_100[m]) for m in METRICS]
        overall01 = float(np.mean(vals01)) if vals01 else 0.0

        # Write the single-question CSV
        q_csv = write_question_csv(q_dir, report_path, scores0_100, overall01)

        # Add 0..1 scores to batch table
        _d, _b, cfg = parse_config_from_filename(report_path.stem)
        batch_rows.append({
            "report_stem": report_path.stem,
            "config": cfg,
            "depth": to_0_1(scores0_100["depth"]),
            "breadth": to_0_1(scores0_100["breadth"]),
            "rigor": to_0_1(scores0_100["rigor"]),
            "innovation": to_0_1(scores0_100["innovation"]),
            "gap": to_0_1(scores0_100["gap"]),
            "overall": round(overall01, 6),
            "report_path": str(report_path),
        })

        print(f"[OK] {report_path.name}  →  "
              f"D:{scores0_100['depth']:3d}  B:{scores0_100['breadth']:3d}  "
              f"R:{scores0_100['rigor']:3d}  I:{scores0_100['innovation']:3d}  "
              f"G:{scores0_100['gap']:3d}   (overall~{overall01:.2f})   -> {q_csv}")

    # Batch CSV with one row per question
    batch_csv = save_batch_reports_csv(out_dir, batch_rows)

    # Config-level summary (fixed 4-config order) + figure
    summary_rows = aggregate_by_config(batch_rows)
    summary_csv = save_batch_summary_csv(out_dir, summary_rows)
    title = f"Research Quality Dimensions Analysis — {topic} / {engine} (n={len(batch_rows)})"
    fig_path = plot_group_6panels(out_dir, summary_rows, title, figsize=SETTINGS["FIGSIZE"])

    print("\nBatch complete.")
    print("  batch_reports.csv        :", batch_csv)
    print("  batch_config_summary.csv :", summary_csv)
    print("  quality_dimensions.png   :", fig_path)


if __name__ == "__main__":
    main()
