#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch LLM-as-a-Judge over ONE selected folder (your chosen domain+model).

Typical folder structure (examples)
-----------------------------------
deep-research/
  data/
    ecology-reports/
      orkg-ask/
        o3/
          1_o3_orkg_d1_b1.md
          ...
        o3-mini/
          ...
    nlp-reports/
      orkg-ask/
        o3/
        o3-mini/

What this script does
---------------------
- You point it at ONE folder, e.g.:  ../data/ecology-reports/orkg-ask/o3
- It runs 5 separate rubric calls per report (depth, breadth, rigor, innovation, gap),
  using strict JSON outputs (0..100 integers).
- It writes per-report outputs (scores JSON, repo_compatible CSV row, prompts per metric),
  and group-level CSV + summary JSON + group plot.

Model & Domain
--------------
- You choose the domain and the model in the SETTINGS below or via CLI flags.
- If you leave --topic unspecified, it tries to infer it from the folder path.

Run
---
python scripts-LLMJ/judge_folder_select.py \
  --folder ../data/ecology-reports/orkg-ask/o3 \
  --out_dir scripts-LLMJ/out-batch \
  --topic ecology \
  --model o4-mini \
  --max_files 0

Notes
-----
- No temperature/top_p parameters (compatible with o-series structured outputs).
- Prompts are saved for audit under: <out_dir>/<topic>/<group>/<engine>/prompts/<report_stem>/<metric>.json
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

# ---- local imports (judge_core provides: model caller, dict loading, judge_metric) ----
try:
    from .judge_core import get_llm_caller, load_topic_dict, judge_metric
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from judge_core import get_llm_caller, load_topic_dict, judge_metric  # type: ignore


# ====================== Settings (editable, overridable via CLI) ======================
SETTINGS = {
    "FOLDER": "../data/ecology-reports/orkg-ask/o3",  # folder to process
    "OUT_DIR": "scripts-LLMJ/out-batch",
    "TOPIC": None,                 # "ecology" | "nlp" | None (infer from folder path)
    "MODEL": "o4-mini",            # good for strict, structured judging
    "FILE_GLOB": "*.md",           # which files inside the folder to process
    "MAX_FILES": 0,                # 0 = no cap
    "MAKE_PLOT": True,
    "BAR_FIGSIZE": (9, 4.5),
}

METRICS = ["depth", "breadth", "rigor", "innovation", "gap"]


# ====================== Helpers ======================
def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def detect_topic_from_path(folder: Path) -> str | None:
    parts = [s.lower() for s in folder.parts]
    # look for 'ecology-reports' or 'nlp-reports' markers
    if any("ecology-reports" in s or "ecology" in s for s in parts):
        return "ecology"
    if any("nlp-reports" in s or "nlp" in s for s in parts):
        return "nlp"
    return None

def detect_engine_from_path(folder: Path) -> str:
    # last directory name is usually 'o3' or 'o3-mini'
    name = folder.name.lower()
    if "o3-mini" in name or "o3mini" in name or "o3_mini" in name:
        return "o3-mini"
    if name == "o3" or "o3" in name:
        return "o3"
    return name  # fallback (kept for traceability)

def detect_group_from_path(folder: Path) -> str:
    # parent name (e.g., 'orkg-ask') acts as group id if available
    return folder.parent.name

def to_0_1(v: int) -> float:
    return round(max(0.0, min(100.0, float(v))) / 100.0, 6)

def parse_config_from_filename(stem: str) -> Tuple[int, int, str]:
    m = re.search(r"d(\d+)_b(\d+)", stem)
    if not m:
        return 1, 1, "d1_b1"
    d, b = int(m.group(1)), int(m.group(2))
    return d, b, f"d{d}_b{b}"

def find_reports(folder: Path, file_glob: str) -> List[Path]:
    return sorted(folder.rglob(file_glob))


# ====================== Per-report & Group I/O ======================
def write_report_outputs(
    group_dir: Path,
    report_path: Path,
    scores0_100: Dict[str, int],
    overall01: float,
):
    """Save per-report: scores JSON and repo-compatible CSV row."""
    group_dir.mkdir(parents=True, exist_ok=True)

    # JSON (scores only)
    js = group_dir / f"{report_path.stem}_scores_only.json"
    obj = {**scores0_100, "overall_computed": int(round(overall01 * 100.0))}
    js.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")

    # CSV row (0..1)
    import csv
    row_csv = group_dir / f"{report_path.stem}_repo_compatible_row.csv"
    _d, _b, config_str = parse_config_from_filename(report_path.stem)
    row = {
        "config": config_str,
        "depth_score": to_0_1(scores0_100["depth"]),
        "breadth_score": to_0_1(scores0_100["breadth"]),
        "rigor_score": to_0_1(scores0_100["rigor"]),
        "innovation_score": to_0_1(scores0_100["innovation"]),
        "gap_score": to_0_1(scores0_100["gap"]),
        "overall_quality": round(overall01, 6),
        "report_path": str(report_path),
    }
    with row_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader(); w.writerow(row)

def save_group_csv(group_dir: Path, topic: str, model: str, engine: str, group: str, rows: List[Dict[str, float | str]]) -> Path:
    import csv
    group_dir.mkdir(parents=True, exist_ok=True)
    p = group_dir / f"group_scores_{topic}_{group}_{engine}_{model}.csv"
    if not rows:
        p.write_text("", encoding="utf-8")
        return p
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    return p

def save_group_summary_and_plot(group_dir: Path, topic: str, model: str, engine: str, group: str, rows: List[Dict[str, float | str]], make_plot: bool, figsize: tuple):
    group_dir.mkdir(parents=True, exist_ok=True)
    scores = {k: [] for k in ["depth_score","breadth_score","rigor_score","innovation_score","gap_score","overall_quality"]}
    for r in rows:
        for k in scores:
            scores[k].append(float(r[k]))

    def _mean_std(xs: List[float]) -> Tuple[float, float]:
        if not xs: return 0.0, 0.0
        a = np.array(xs, dtype=float)
        return float(a.mean()), float(a.std(ddof=0))

    summary = {"topic": topic, "model": model, "engine": engine, "group": group, "n_docs": len(rows)}
    means = {}
    stds  = {}
    for k, xs in scores.items():
        m, s = _mean_std(xs)
        means[k] = round(m, 6)
        stds[k]  = round(s, 6)
    summary["means"] = means
    summary["stds"]  = stds

    sj = group_dir / f"group_summary_{topic}_{group}_{engine}_{model}.json"
    sj.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    if make_plot:
        labels = ["depth_score","breadth_score","rigor_score","innovation_score","gap_score","overall_quality"]
        values = [means[k] for k in labels]
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=figsize)
        ax = plt.gca()
        xs = np.arange(len(labels))
        ax.bar(xs, values)
        ax.set_xticks(xs); ax.set_xticklabels([l.replace("_"," ") for l in labels])
        ax.set_ylim(0, 1.05); ax.set_ylabel("Mean score (0..1)")
        ax.set_title(f"{topic} — {group} — {engine} (n={len(rows)})")
        for i, v in enumerate(values):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
        out_fig = group_dir / f"quality_dimensions_group_{topic}_{group}_{engine}_{model}.png"
        fig.tight_layout()
        fig.savefig(out_fig, dpi=200, bbox_inches="tight")
        plt.close(fig)

    return sj

def append_group_row(
    rows: List[Dict[str, float | str]],
    topic: str,
    model: str,
    engine: str,
    group: str,
    report_path: Path,
    scores0_100: Dict[str, int],
    overall01: float
):
    _d, _b, config_str = parse_config_from_filename(report_path.stem)
    rows.append({
        "topic": topic,
        "model": model,
        "engine": engine,
        "group": group,
        "config": config_str,
        "report_stem": report_path.stem,
        "report_path": str(report_path),
        "depth_score": to_0_1(scores0_100["depth"]),
        "breadth_score": to_0_1(scores0_100["breadth"]),
        "rigor_score": to_0_1(scores0_100["rigor"]),
        "innovation_score": to_0_1(scores0_100["innovation"]),
        "gap_score": to_0_1(scores0_100["gap"]),
        "overall_quality": round(overall01, 6),
    })


# ====================== Main run ======================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder",  default=SETTINGS["FOLDER"],   help="Folder that contains the reports to process")
    ap.add_argument("--out_dir", default=SETTINGS["OUT_DIR"],  help="Output root directory")
    ap.add_argument("--topic",   default=SETTINGS["TOPIC"],    help="Domain: ecology|nlp (if omitted, infer from folder path)")
    ap.add_argument("--model",   default=SETTINGS["MODEL"],    help="OpenAI model, e.g. o4-mini")
    ap.add_argument("--file_glob", default=SETTINGS["FILE_GLOB"], help="Glob for files inside folder (default: *.md)")
    ap.add_argument("--max_files", type=int, default=SETTINGS["MAX_FILES"], help="Max files to process (0 = no cap)")
    ap.add_argument("--no_plot", action="store_true", help="Skip group plot")
    args = ap.parse_args()

    folder = Path(args.folder).resolve()
    assert folder.exists() and folder.is_dir(), f"Folder not found: {folder}"

    topic = (args.topic or "").strip().lower()
    if not topic:
        inferred = detect_topic_from_path(folder)
        if inferred is None:
            raise SystemExit("Cannot infer topic from folder path. Pass --topic ecology|nlp.")
        topic = inferred
    assert topic in {"ecology","nlp"}, "--topic must be 'ecology' or 'nlp'"

    engine = detect_engine_from_path(folder)
    group  = detect_group_from_path(folder)

    out_root = Path(args.out_dir).resolve()
    group_dir = out_root / topic / group / engine
    prompts_root = group_dir / "prompts"
    group_dir.mkdir(parents=True, exist_ok=True)
    prompts_root.mkdir(parents=True, exist_ok=True)

    # Collect files
    files = find_reports(folder, args.file_glob)
    if args.max_files > 0:
        files = files[: args.max_files]
    if not files:
        print(f"No files found under {folder} with pattern {args.file_glob}.")
        return

    # Load dicts and model caller
    V = load_topic_dict(topic)
    call_llm, model_used, used_wrapper = get_llm_caller(args.model)

    rows: List[Dict[str, float | str]] = []

    for report_path in files:
        report_md = read_text(report_path)

        # score all metrics, saving prompt payloads
        scores0_100: Dict[str, int] = {}
        for m in METRICS:
            prompt_path = prompts_root / report_path.stem / f"{m}.json"
            score = judge_metric(
                call_llm=call_llm,
                model_used=model_used,
                topic=topic,
                report_md=report_md,
                metric=m,
                V=V,
                save_prompt_to=prompt_path
            )
            scores0_100[m] = score

        vals01 = [to_0_1(scores0_100[m]) for m in METRICS]
        overall01 = float(np.mean(vals01)) if vals01 else 0.0

        # per-report outputs
        write_report_outputs(group_dir, report_path, scores0_100, overall01)
        # add to group table
        append_group_row(rows, topic, model_used, engine, group, report_path, scores0_100, overall01)

        print(f"Scored: {report_path.name}  →  "
              f"D:{scores0_100['depth']:3d} B:{scores0_100['breadth']:3d} "
              f"R:{scores0_100['rigor']:3d} I:{scores0_100['innovation']:3d} "
              f"G:{scores0_100['gap']:3d}  (overall~{overall01:.2f})")

    # Group outputs
    csv_path = save_group_csv(group_dir, topic, model_used, engine, group, rows)
    summary_path = save_group_summary_and_plot(group_dir, topic, model_used, engine, group, rows, not args.no_plot and SETTINGS["MAKE_PLOT"], SETTINGS["BAR_FIGSIZE"])

    print("\nGroup done.")
    print("  Group CSV:   ", csv_path)
    print("  Group summary:", summary_path)
    if not args.no_plot and SETTINGS["MAKE_PLOT"]:
        print("  Group plot:   ", group_dir / f"quality_dimensions_group_{topic}_{group}_{engine}_{model_used}.png")
    print("  Prompts saved under:", prompts_root)


if __name__ == "__main__":
    main()
