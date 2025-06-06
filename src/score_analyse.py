#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# Disable CUDA usage
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
torch.cuda.is_available    = lambda : False
torch.cuda.device_count    = lambda : 0
torch.cuda.current_device  = lambda : 0
torch.cuda.get_device_name = lambda idx=0: "cpu"

import glob
import argparse
import numpy as np
import csv
import matplotlib.pyplot as plt

# Scoring libraries
from sacrebleu import corpus_bleu            # BLEU
from nltk.translate.meteor_score import meteor_score  # METEOR
from rouge_score import rouge_scorer          # ROUGE-1 & ROUGE-L
from bert_score import score as bert_score    # BERTScore
from jiwer import wer                         # WER
from gensim.models import KeyedVectors        # WMD
from gensim.corpora.dictionary import Dictionary
from gensim.similarities import WmdSimilarity
import nltk
nltk.download('wordnet')
# Note: Moverscore import is deferred into its function to avoid CUDA errors

# ── USER-EDITABLE SECTION ───────────────────────────────────────────────────────
EXCLUDE_KEYWORDS    = ["firecrawl"]
REPORT_DIR_DEFAULT  = "../data/reports"
OUTPUT_DIR_DEFAULT  = "../data"
EMBEDDING_PATH      = "../embeddings/GoogleNews-vectors-negative300.bin.gz"
# ────────────────────────────────────────────────────────────────────────────────

def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Compute an aggregated pairwise‐average heatmap between groups of reports."
    )
    parser.add_argument(
        "--metric", "-m",
        choices=["BLEU", "ROUGE1", "ROUGEL", "METEOR", "BERT", "WER", "WMD", "MOVERSCORE"],
        required=True,
        help="Which metric to compute (only that one)."
    )
    parser.add_argument(
        "--reports", "-r",
        default=REPORT_DIR_DEFAULT,
        help=f"Directory containing Markdown reports (default: {REPORT_DIR_DEFAULT})"
    )
    parser.add_argument(
        "--output", "-o",
        default=OUTPUT_DIR_DEFAULT,
        help=f"Directory to write CSV and heatmap PNG (default: {OUTPUT_DIR_DEFAULT})"
    )
    parser.add_argument(
        "--exclude", "-e",
        nargs="*",
        default=EXCLUDE_KEYWORDS,
        help="List of keywords; any group whose key contains one of these (case-insensitive) is skipped."
    )
    return parser.parse_args()


def load_and_group_reports(report_dir, exclude_keywords):
    """
    1) Read all .md files from `report_dir`.
    2) Group them by filename pattern: <index>_<model>_<engine>_d<depth>_b<breadth>.md
       (group_key = f"{model}_{engine}_{depth}_{breadth}").
    3) Skip any group whose key contains a case-insensitive match of any exclude_keywords.
    Returns: { group_key: [ (filename, text), ... ], ... }.
    """
    pattern = os.path.join(report_dir, "*.md")
    paths = glob.glob(pattern)
    grouped = {}

    for path in paths:
        fname = os.path.basename(path)
        parts = fname[:-3].split("_")  # drop ".md", split by underscore
        if len(parts) >= 5:
            model   = parts[1]
            engine  = parts[2]
            depth   = parts[3]   # e.g. "d4"
            breadth = parts[4]   # e.g. "b1"
            group_key = f"{model}_{engine}_{depth}_{breadth}"
        else:
            group_key = "misc"

        # Exclude entire group if key contains any exclude keyword (case-insensitive)
        low = group_key.lower()
        if any(ex.lower() in low for ex in exclude_keywords):
            continue

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        grouped.setdefault(group_key, []).append((fname, text))

    return grouped


def build_index_to_text_map(docs):
    """
    Given a list of (filename, text) pairs for a single group,
    return a dict mapping `index` -> `text`, where `index` is the integer before the first underscore.
    Example: '1_o3_orkg_d1_b4.md'  -> index=1
    """
    idx_map = {}
    for fname, text in docs:
        # Split on underscore; the first part is the "index"
        parts = fname.split("_")
        try:
            idx = int(parts[0])
        except ValueError:
            # If filename doesn't start with a valid integer, skip it
            continue
        idx_map[idx] = text
    return idx_map


def average_metric_over_indices(idx_map_A, idx_map_B, metric_func):
    """
    Given two dicts: index->text for group A, and index->text for group B,
    apply `metric_func(text_A, text_B)` for every index that appears in both maps.
    Return the average of all pairwise scores.
    If no overlapping index, return NaN.
    """
    common_indices = sorted(set(idx_map_A.keys()) & set(idx_map_B.keys()))
    if not common_indices:
        return float("nan")

    scores = []
    for idx in common_indices:
        txtA = idx_map_A[idx]
        txtB = idx_map_B[idx]
        score = metric_func(txtA, txtB)
        scores.append(score)

    return float(np.mean(scores))


### --- Metric‐specific wrapper functions (operate on two raw strings) ---

def bleu_text_pair(text_A, text_B):
    """
    Compute BLEU between text_A (hyp) and text_B (ref). Returns a float in [0..100].
    """
    hyp  = [text_A]
    refs = [[text_B]]
    return corpus_bleu(hyp, refs, force=True).score


def meteor_text_pair(text_A, text_B):
    """
    Compute METEOR: tokenize by whitespace, then call nltk’s meteor_score.
    Returns float in [0..100].
    """
    tokens_ref = text_B.split()
    tokens_hyp = text_A.split()
    return meteor_score([tokens_ref], tokens_hyp) * 100.0


def rouge1_text_pair(text_A, text_B):
    """
    Compute ROUGE-1 F1 for (A vs. B). Returns float in [0..1].
    """
    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
    scores = scorer.score(text_B, text_A)
    return scores["rouge1"].fmeasure


def rougel_text_pair(text_A, text_B):
    """
    Compute ROUGE-L F1 for (A vs. B). Returns float in [0..1].
    """
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(text_B, text_A)
    return scores["rougeL"].fmeasure


def bert_text_pair(text_A, text_B):
    """
    Compute BERTScore F1 for (A vs. B). Returns float in [0..1].
    """
    P, R, F1 = bert_score(
        [text_A], [text_B],
        #model_type="microsoft/deberta-xlarge-mnli",
        model_type="bert-base-uncased",
        num_layers=9,
        verbose=False,
        rescale_with_baseline=True,
        lang="en"
    )
    return F1.item()


def wer_text_pair(text_A, text_B):
    """
    Compute WER (word-error‐rate) between (A vs. B). Returns float >=0.
    """
    return wer(text_B, text_A)


def wmd_text_pair_factory(w2v_model):
    """
    Returns a function f(A,B) that computes Word Mover’s Distance between A and B
    using the provided gensim KeyedVectors model. Internally, uses gensim's WmdSimilarity
    to get a cosine‐similarity score, then does 1 - sim to produce a “distance.”
    """
    
def wmd_text_pair_factory(w2v_model):
    """
    Returns a function f(A, B) that computes Word Mover’s Distance between A and B
    using gensim’s WmdSimilarity (no dictionary= keyword).
    """
    def doc_to_tokens(txt):
        return [tok for tok in txt.lower().split() if tok.isalpha()]

    def f(text_A, text_B):
        # Tokenize both strings:
        toksA = doc_to_tokens(text_A)
        toksB = doc_to_tokens(text_B)

        # Build a tiny corpus consisting of B only:
        index = WmdSimilarity(
            [toksB],      # our “reference corpus” is just one document
            w2v_model,
            num_best=1
        )
        sims = index[toksA]    # returns [(0, cosine_sim)]
        if not sims:
            return 1.0
        _, cosine_sim = sims[0]
        return max(0.0, 1.0 - cosine_sim)
    return f


def moverscore_text_pair(text_A, text_B):
    """
    Compute MoverScore(A vs. B) on CPU only.
    """
    from moverscore import get_idf_dict, word_mover_score

    idf_dict = get_idf_dict([text_A, text_B])
    # Pass device="cpu" so that it never tries to move the model to CUDA
    return word_mover_score(
        [text_B],
        [text_A],
        idf_dict,
        stop_words=[],
        device="cpu"
    )



def save_csv(matrix: np.ndarray, labels: list, filepath: str, fmt="%.6f"):
    """
    Write a square matrix to a CSV file, with row & column headers given by `labels`.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow([""] + labels)
        for i, lab in enumerate(labels):
            row = [lab] + [fmt % matrix[i, j] for j in range(matrix.shape[1])]
            writer.writerow(row)
    print(f"CSV written: {filepath}")


def plot_heatmap(matrix: np.ndarray, labels: list, title: str, outpath: str, vmin=None, vmax=None):
    """
    Draw a heatmap for the given square matrix and save as PNG.
    - vmin/vmax can fix the color scale range (optional).
    """
    n = len(labels)
    fig, ax = plt.subplots(figsize=(max(6, n*0.5), max(5, n*0.5)))
    cax = ax.matshow(matrix, cmap="viridis_r", vmin=vmin, vmax=vmax)
    fig.colorbar(cax)

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_title(title)
    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    fig.savefig(outpath, dpi=300)
    plt.close(fig)
    print(f"Heatmap saved: {outpath}")


def main():
    args = parse_args()

    # 1) Load and group all reports
    grouped = load_and_group_reports(args.reports, args.exclude)
    if not grouped:
        print("No groups remain after exclusion. Exiting.")
        return

    # Build a dict: group_key -> ( index -> text ) 
    group_to_idx_map = {}
    for gk, docs in grouped.items():
        group_to_idx_map[gk] = build_index_to_text_map(docs)

    group_keys = sorted(group_to_idx_map.keys())
    N = len(group_keys)

    print(f"Available groups ({N}):")
    for k in group_keys:
        print("  -", k)
    print()

    # 2) Decide which metric we're computing
    metric = args.metric.upper()
    metric_func = None
    wmd_factory = None

    if metric == "BLEU":
        metric_func = bleu_text_pair
        vmin, vmax = 0, 100
        out_csv = os.path.join(args.output, "bleu_matrix.csv")
        out_png = os.path.join(args.output, "bleu_heatmap.png")
        plot_title = "BLEU (0–100)"

    elif metric == "METEOR":
        metric_func = meteor_text_pair
        vmin, vmax = 0, 100
        out_csv = os.path.join(args.output, "meteor_matrix.csv")
        out_png = os.path.join(args.output, "meteor_heatmap.png")
        plot_title = "METEOR (0–100)"

    elif metric == "ROUGE1":
        metric_func = rouge1_text_pair
        vmin, vmax = 0, 1
        out_csv = os.path.join(args.output, "rouge1_matrix.csv")
        out_png = os.path.join(args.output, "rouge1_heatmap.png")
        plot_title = "ROUGE-1 F1 (0–1)"

    elif metric == "ROUGEL":
        metric_func = rougel_text_pair
        vmin, vmax = 0, 1
        out_csv = os.path.join(args.output, "rougel_matrix.csv")
        out_png = os.path.join(args.output, "rougel_heatmap.png")
        plot_title = "ROUGE-L F1 (0–1)"

    elif metric == "BERT":
        metric_func = bert_text_pair
        vmin, vmax = 0, 1
        out_csv = os.path.join(args.output, "bertscore_matrix.csv")
        out_png = os.path.join(args.output, "bertscore_heatmap.png")
        plot_title = "BERTScore F1 (0–1)"

    elif metric == "WER":
        metric_func = wer_text_pair
        # Clamp color scale to [0,1], though WER can exceed 1
        vmin, vmax = 0, 1
        out_csv = os.path.join(args.output, "wer_matrix.csv")
        out_png = os.path.join(args.output, "wer_heatmap.png")
        plot_title = "WER (0–∞, clamped 0–1)"

    elif metric == "WMD":
        # Build a factory function once we load embeddings
        try:
            print("Loading Word2Vec embeddings for WMD (this can take a moment)…")
            w2v_model = KeyedVectors.load_word2vec_format(EMBEDDING_PATH, binary=True)
            metric_func = wmd_text_pair_factory(w2v_model)
            vmin, vmax = None, None
            out_csv = os.path.join(args.output, "wmd_matrix.csv")
            out_png = os.path.join(args.output, "wmd_heatmap.png")
            plot_title = "WMD Distance"
        except Exception as ex:
            print("Error loading embeddings or preparing WMD:", ex)
            return

    elif metric == "MOVERSCORE":
        metric_func = moverscore_text_pair
        vmin, vmax = 0, 1
        out_csv = os.path.join(args.output, "moverscore_matrix.csv")
        out_png = os.path.join(args.output, "moverscore_heatmap.png")
        plot_title = "MoverScore (0–1)"

    else:
        print(f"Unknown metric: {metric}. Exiting.")
        return

    # 3) Build an N×N matrix of “average‐over‐indices” scores
    matrix = np.zeros((N, N), dtype=float)

    for i in range(N):
        key_i = group_keys[i]
        idx_map_i = group_to_idx_map[key_i]

        for j in range(N):
            key_j = group_keys[j]
            idx_map_j = group_to_idx_map[key_j]

            avg_score = average_metric_over_indices(idx_map_i, idx_map_j, metric_func)
            matrix[i, j] = avg_score

        print(f"{metric}: processed row {i+1}/{N}")

    # 4) Save CSV + plot heatmap
    save_csv(matrix, group_keys, out_csv, fmt="%.6f")
    plot_heatmap(matrix, group_keys, plot_title, out_png, vmin=vmin, vmax=vmax)

    print("\nAll done. Outputs in:", args.output)


if __name__ == "__main__":
    main()
