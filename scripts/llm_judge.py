import re
import json
import argparse
import sys
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Any

import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()


# ---- local imports from jude_core.py ----
try:
    from .judge_core import get_llm_caller, load_topic_dict, judge_metric  # type: ignore
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from judge_core import get_llm_caller, load_topic_dict, judge_metric  # type: ignore

# --------------------------------------------------------------------------

# =================== Load Constants ===================

METRICS = ["depth", "breadth", "rigor", "innovation", "gap"]
CONFIG_ORDER =["d1_b1", "d1_b4", "d4_b1", "d4_b4"]
BAR_FIGSIZE = (9, 4.5)
BATCH_FIGSIZE = (16, 12)
FILE_GLOB = "*.md"
MAX_FILES =  0
SAVE_PROMPTS = False

# =================== Core Helpers (Shared) ===================

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

def to_0_1(v: int) -> float:
    """Converts a 0-100 score to 0.0-1.0 float."""
    return round(max(0.0, min(100.0, float(v))) / 100.0, 6)

def parse_config_from_filename(stem: str) -> Tuple[int, int, str]:
    """Extracts the dX_bY pattern; defaults to d1_b1 if absent."""
    m = re.search(r"d(\d+)_b(\d+)", stem)
    if not m:
        return 1, 1, "d1_b1"
    d, b = int(m.group(1)), int(m.group(2))
    return d, b, f"d{d}_b{b}"

# =================== Single Report Mode Functions ===================

def save_scores_only_json(out_dir: Path, base: str, scores0_100: Dict[str, int], overall100: int) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / f"{base}_scores_only.json"
    obj = {**scores0_100, "overall_computed": overall100}
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return p

def save_repo_row_csv(out_dir: Path, base: str, config_str: str,
                      scores0_100: Dict[str, int], overall01: float) -> Path:
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
    vals01 = [to_0_1(scores0_100[m]) for m in METRICS]
    overall01 = float(np.mean(vals01))
    labels = [m.replace("_"," ") for m in METRICS] + ["overall quality"]
    values = vals01 + [overall01]

    fig = plt.figure(figsize=BAR_FIGSIZE)
    ax = plt.gca()
    xs = np.arange(len(labels))
    ax.bar(xs, values)
    ax.set_xticks(xs); ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05); ax.set_ylabel("Score (0..1)")
    ax.set_title(title)
    for i, v in enumerate(values):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    out = figures_dir / "quality_dimensions.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out

def run_single_report_mode(args: argparse.Namespace):
    """
    Main logic for scoring a single research report.
    """
    print(f"--- Running Single Report Mode for: {args.report} ---")

    report_path = Path(args.report).resolve()
    if not report_path.exists():
        sys.exit(f"Error: Report not found: {report_path}")
    out_dir = Path(args.out_dir).resolve()
    figures_dir = out_dir / "figures"
    prompts_dir = out_dir / "prompts"

    # Load report and dicts
    report_md = read_text(report_path)
    V = load_topic_dict(args.topic)

    # Caller
    call_llm, model_used, _ = get_llm_caller(args.model)

    # Score each metric
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
    
    # Console (scores only)
    print("\n--- Scores (0-100) ---")
    print(json.dumps({**scores0_100, "overall_computed": overall100}, indent=2, ensure_ascii=False))
    print(f"\nWrote JSON scores: {scores_json_path}")
    print(f"Wrote Repo CSV row: {row_csv}")
    
    if args.plot:
        title = f"{stem} — {args.topic} — LLMJ metric-wise ({model_used})"
        plot_path = plot_quality_bars(figures_dir, scores0_100, title)
        print(f"Wrote plot: {plot_path}")
    
    print(f"Wrote prompts: {prompts_dir}/<metric>.json")

# =================== Batch Report Mode Functions ===================

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

def find_reports(folder: Path, pattern: str) -> List[Path]:
    return sorted(folder.glob(pattern))

def write_question_csv(q_dir: Path, report_path: Path,
                       scores0_100: Dict[str, int], overall01: float) -> Path:
    q_dir.mkdir(parents=True, exist_ok=True)
    csv_path = q_dir / "scores.csv"

    _d, _b, cfg = parse_config_from_filename(report_path.stem)
    row = {
        "report_stem": report_path.stem,
        "config": cfg,
        "depth": to_0_1(scores0_100["depth"]), "breadth": to_0_1(scores0_100["breadth"]),
        "rigor": to_0_1(scores0_100["rigor"]), "innovation": to_0_1(scores0_100["innovation"]),
        "gap": to_0_1(scores0_100["gap"]), "overall": round(overall01, 6),
        "depth_raw": scores0_100["depth"], "breadth_raw": scores0_100["breadth"],
        "rigor_raw": scores0_100["rigor"], "innovation_raw": scores0_100["innovation"],
        "gap_raw": scores0_100["gap"], "overall_raw": int(round(overall01 * 100.0)),
        "report_path": str(report_path),
    }
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader(); w.writerow(row)
    return csv_path

def save_batch_reports_csv(out_dir: Path, rows: List[Dict[str, str | float]]) -> Path:
    p = out_dir / "batch_reports.csv"
    if not rows:
        p.write_text("", encoding="utf-8")
        return p
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    return p

def aggregate_by_config(rows: List[Dict[str, str | float]]) -> List[Dict[str, float | str | int]]:
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
        row: Dict[str, float | str | int] = {"config": cfg, "n_docs": len(items)}
        for k in ["depth", "breadth", "rigor", "innovation", "gap", "overall"]:
            m, s = mean_std(col(k))
            row[f"{k}_mean"] = round(m, 6)
            row[f"{k}_std"]  = round(s, 6)
        out.append(row)
    return out

def save_batch_summary_csv(out_dir: Path, summary_rows: List[Dict[str, float | str | int]]) -> Path:
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
    if not summary_rows:
        return out_dir / "quality_dimensions.png"

    by_cfg = {r["config"]: r for r in summary_rows}
    cfgs = CONFIG_ORDER

    def take_means_stds(name: str):
        means = [float(by_cfg.get(cfg, {}).get(f"{name}_mean", 0.0)) for cfg in cfgs]
        stds  = [float(by_cfg.get(cfg, {}).get(f"{name}_std", 0.0)) for cfg in cfgs]
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
        # stds are calculated as sample standard deviation. For error bars, typically Standard Error of the Mean (SEM) is used.
        # Since 'ddof=0' (population std) was used, let's just use it as the error bar for now.
        # To calculate SEM, you'd need the count of reports 'n_docs'
        n_docs = [int(by_cfg.get(cfg, {}).get("n_docs", 0)) for cfg in cfgs]
        sems = [s / np.sqrt(n) if n > 0 else 0.0 for s, n in zip(stds, n_docs)]

        ax.bar(xs, means, yerr=sems, capsize=5) # Using SEM for error bars
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

def run_batch_report_mode(args: argparse.Namespace):
    """
    Main logic for scoring a batch of research reports.
    """
    print(f"--- Running Batch Report Mode for: {args.folder} ---")

    in_folder = Path(args.folder).resolve()
    if not in_folder.exists() or not in_folder.is_dir():
        sys.exit(f"Error: Folder not found: {in_folder}")
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    topic = (args.topic or "").strip().lower()
    if not topic:
        topic = detect_topic_from_path(in_folder) or ""
    if topic not in {"ecology", "nlp"}:
        sys.exit("Error: Please pass --topic ecology|nlp (or make it inferable from path).")

    engine = detect_engine_from_path(in_folder)

    # Load dictionaries & model caller
    V = load_topic_dict(topic)
    call_llm, model_used, _ = get_llm_caller(args.model)

    files = find_reports(in_folder, args.file_glob)
    if not files:
        sys.exit(f"Error: No files under {in_folder} matching {args.file_glob}")
    
    if args.max_files > 0:
        files = files[: args.max_files]

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
            "report_stem": report_path.stem, "config": cfg,
            "depth": to_0_1(scores0_100["depth"]), "breadth": to_0_1(scores0_100["breadth"]),
            "rigor": to_0_1(scores0_100["rigor"]), "innovation": to_0_1(scores0_100["innovation"]),
            "gap": to_0_1(scores0_100["gap"]), "overall": round(overall01, 6),
            "report_path": str(report_path),
        })

        print(f"[OK] {report_path.name}  →  "
              f"D:{scores0_100['depth']:3d}  B:{scores0_100['breadth']:3d}  "
              f"R:{scores0_100['rigor']:3d}  I:{scores0_100['innovation']:3d}  "
              f"G:{scores0_100['gap']:3d}   (overall~{overall01:.2f})   -> {q_csv.name}")

    # Batch CSV with one row per question
    batch_csv = save_batch_reports_csv(out_dir, batch_rows)

    # Config-level summary (fixed 4-config order) + figure
    summary_rows = aggregate_by_config(batch_rows)
    summary_csv = save_batch_summary_csv(out_dir, summary_rows)
    title = f"Research Quality Dimensions Analysis — {topic} / {engine} (n={len(batch_rows)})"
    
    if args.plot:
        fig_path = plot_group_6panels(out_dir, summary_rows, title, figsize=BATCH_FIGSIZE)
        print("\nBatch complete.")
        print("  batch_reports.csv        :", batch_csv)
        print("  batch_config_summary.csv :", summary_csv)
        print("  quality_dimensions.png   :", fig_path)
    else:
        print("\nBatch complete (no plot requested).")
        print("  batch_reports.csv        :", batch_csv)
        print("  batch_config_summary.csv :", summary_csv)


# =================== Main Execution Control ===================

def main():
    ap = argparse.ArgumentParser(
        description="Unified script for scoring single or batch research reports.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # --- Mode Selection ---
    ap.add_argument(
        "--run-batch",
        action="store_true",
        help="Run in batch mode (requires --folder)."
    )

    # --- Common Arguments ---
    ap.add_argument("--topic", default="ecology", choices=["ecology", "nlp"],
                    help="Domain (ecology|nlp)")
    ap.add_argument("--out_dir", default="Test_out",
                    help="Output directory for JSON/CSV/plots")
    ap.add_argument("--model", default="o4-mini",
                    help="OpenAI model (e.g., o3-mini).")
    ap.add_argument("--no-plot", dest="plot", action="store_false",
                    help="Skip plotting")
    ap.set_defaults(plot=True)

    # --- Single Mode Argument ---
    ap.add_argument("--report", default=None,
                    help="Path to a single DeepResearch .md report (REQUIRED for single mode)")

    # --- Batch Mode Arguments ---
    ap.add_argument("--folder", default=None,
                    help="Folder containing reports (*.md) for batch mode (REQUIRED for batch mode)")
    ap.add_argument("--file_glob", default="*.md",
                    help="File glob (default: *.md), only used in batch mode.")
    ap.add_argument("--max_files", type=int, default=0,
                    help="Max files to process (0 = all), only used in batch mode.")
    ap.add_argument("--save_prompts", action="store_true",
                    help="Store prompts per question, only used in batch mode.")

    args = ap.parse_args()

    # ================= ARGUMENT VALIDATION =====================

    if args.run_batch:
        # --- Batch Mode ---
        if args.folder is None:
            ap.error("Batch mode requires --folder. Example: --run-batch --folder path/to/reports")

        if args.report is not None:
            print("Warning: --report ignored because --run-batch is enabled.")

        run_batch_report_mode(args)
        return

    # --- Single File Mode ---
    if args.report is None:
        ap.error("Single-report mode requires --report. Example: --report path/to/file.md")

    run_single_report_mode(args)


if __name__ == "__main__":
    main()
