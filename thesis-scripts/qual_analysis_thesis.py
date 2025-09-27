import os
import re
import argparse
import pandas as pd

from research_analyzer import ResearchBatchRunner


def _infer_questions_from_dir(report_dir: str):
    """
    Fällt zurück, wenn keine explizite Fragenliste angegeben ist:
    extrahiert Q-IDs aus Dateinamen wie '<QID>_..._d?_b?.md'.
    """
    qids = set()
    for fn in os.listdir(report_dir):
        if not fn.endswith('.md'):
            continue
        m = re.match(r'(\d+)_.*_d\d+_b\d+\.md$', fn)
        if m:
            qids.add(m.group(1))
    return sorted(qids, key=lambda x: int(x))


def main():
    ap = argparse.ArgumentParser(description="Qualitative report scoring & figures")
    ap.add_argument("--reports", type=str, required=True,
                    help="Directory with generated markdown reports (per question)")
    ap.add_argument("--out", type=str, required=True,
                    help="Output directory for CSV and figures")
    ap.add_argument("--questions", type=str, default=None,
                    help="Optional: CSV/TXT with a 'question' column or one QID per line")
    args = ap.parse_args()

    # Fragenliste laden/ableiten
    if args.questions and os.path.isfile(args.questions):
        if args.questions.endswith('.csv'):
            qdf = pd.read_csv(args.questions)
            if 'question' in qdf.columns:
                questions = [str(x) for x in qdf['question'].dropna().astype(int).tolist()]
            else:
                questions = [str(x) for x in qdf.iloc[:,0].dropna().astype(int).tolist()]
        else:
            with open(args.questions, 'r', encoding='utf-8') as f:
                questions = [line.strip() for line in f if line.strip()]
    else:
        questions = _infer_questions_from_dir(args.reports)

    if not questions:
        raise SystemExit("No questions found. Provide --questions or ensure filenames match '<QID>_..._d?_b?.md'.")

    print(f"[INFO] analyzing {len(questions)} questions")
    runner = ResearchBatchRunner()
    all_results = runner.analyze_multiple_questions(args.reports, questions, args.out)

    if not all_results:
        raise SystemExit("No results produced (check report file names/paths).")

    stats_csv = os.path.join(args.out, "comprehensive_summary_statistics.csv")
    if not os.path.isfile(stats_csv):
        # falls analyze_multiple_questions bereits geschrieben hat, übernehmen wir es
        stats_csv = runner._save_summary(all_results, args.out)

    figs_dir = os.path.join(args.out, "figures")
    runner.create_publication_plots(stats_csv, all_results, figs_dir)

    print(f"[DONE] CSV: {stats_csv}")
    print(f"[DONE] Figures saved under: {figs_dir}")


if __name__ == "__main__":
    main()
