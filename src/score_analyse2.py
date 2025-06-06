#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# Force CPU‐only
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
torch.cuda.is_available    = lambda : False
torch.cuda.device_count    = lambda : 0
torch.cuda.current_device  = lambda : 0
torch.cuda.get_device_name = lambda idx=0: "cpu"

import glob
import numpy as np
import csv
import matplotlib.pyplot as plt

from bert_score import score as bert_score       # CPU BERTScore
from gensim.models import KeyedVectors           # Word2Vec (GoogleNews)
from gensim.similarities import WmdSimilarity
import nltk
nltk.download('wordnet', quiet=True)

# ── SETTINGS ───────────────────────────────────────────────────────────────────
REPORT_DIR     = "../data/reports"
OUTPUT_DIR     = "../data/paper_results"
EMBEDDING_PATH = "../embeddings/GoogleNews-vectors-negative300.bin.gz"
EXCLUDE_KEYS   = []   # leave empty so ORKG & FireCrawl both appear for RQ3
# ─────────────────────────────────────────────────────────────────────────────

def load_and_group_reports(report_dir, exclude_keywords=None):
    """
    1) Read all “*.md” in report_dir
    2) Group by "<model>_<engine>_<depth>_<breadth>"
    3) Skip any group whose key contains a substring in exclude_keywords
    Returns: { group_key: [ (filename, text), … ], … }
    """
    if exclude_keywords is None:
        exclude_keywords = []
    pattern = os.path.join(report_dir, "*.md")
    paths = sorted(glob.glob(pattern))
    grouped = {}
    for path in paths:
        fname = os.path.basename(path)
        parts = fname[:-3].split("_")
        if len(parts) >= 5:
            model, engine, depth, breadth = parts[1], parts[2], parts[3], parts[4]
            key = f"{model}_{engine}_{depth}_{breadth}"
        else:
            key = "misc"
        if any(ex.lower() in key.lower() for ex in exclude_keywords):
            continue
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        grouped.setdefault(key, []).append((fname, txt))
    return grouped

def build_index_to_text_map(docs):
    """
    From [(filename, text), …], return { index: text },
    where index = integer before first “_” in filename.
    E.g. “1_o3_orkg_d1_b4.md” → 1 → text.
    """
    idx_map = {}
    for fname, txt in docs:
        parts = fname.split("_")
        try:
            idx = int(parts[0])
        except ValueError:
            continue
        idx_map[idx] = txt
    return idx_map

def average_metric_over_indices(mapA, mapB, metric_func):
    """
    For every index in both mapA and mapB, compute metric_func(textA, textB).
    Return (mean_score, count). If no overlap, (nan, 0).
    """
    common = sorted(set(mapA.keys()) & set(mapB.keys()))
    if not common:
        return (float("nan"), 0)
    scores = [metric_func(mapA[i], mapB[i]) for i in common]
    return (float(np.mean(scores)), len(common))

def wmd_text_pair_factory(w2v_model):
    """
    Return f(A,B) = Word Mover’s Distance = 1 – cos_sim (via WmdSimilarity).
    Output ∈ [0..1], lower = more similar.
    """
    def doc_to_tokens(s):
        return [tok for tok in s.lower().split() if tok.isalpha()]
    def f(textA, textB):
        toksA = doc_to_tokens(textA)
        toksB = doc_to_tokens(textB)
        index = WmdSimilarity([toksB], w2v_model, num_best=1)
        sims  = index[toksA]  # yields [(0, cos_sim)]
        if not sims:
            return 1.0
        _, cos = sims[0]
        return max(0.0, 1.0 - cos)
    return f

def bert_text_pair(textA, textB):
    """
    Compute BERTScore‐F1 (bert-base-uncased) on CPU. Return ∈ [0..1].
    """
    P, R, F1 = bert_score(
        [textA], [textB],
        model_type="bert-base-uncased",
        num_layers=9,
        verbose=False,
        rescale_with_baseline=True,
        lang="en"
    )
    return F1.item()

def save_matrix_and_counts(matrix, counts, labels, basepath, fmt="%.6f"):
    """
    Save two CSVs:
      - basepath + "_matrix.csv"  (mean scores)
      - basepath + "_counts.csv"  (# of shared indices)
    Both have header row & first column = labels.
    """
    os.makedirs(os.path.dirname(basepath), exist_ok=True)
    mat_path = basepath + "_matrix.csv"
    cnt_path = basepath + "_counts.csv"
    # Write matrix
    with open(mat_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([""] + labels)
        for i, lab in enumerate(labels):
            row = [lab]
            for j in range(len(labels)):
                val = matrix[i, j]
                row.append("" if np.isnan(val) else fmt % val)
            w.writerow(row)
    print(f"CSV written: {mat_path}")
    # Write counts
    with open(cnt_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([""] + labels)
        for i, lab in enumerate(labels):
            row = [lab]
            for j in range(len(labels)):
                c = counts[i, j]
                row.append(str(c) if c != 0 else "")
            w.writerow(row)
    print(f"CSV written: {cnt_path}")

def plot_heatmap(matrix, labels, title, outpath, vmin=None, vmax=None):
    """
    Draw & save a square heatmap (imshow) with cmap="viridis_r" 
    so darker = more similar (BERT high, WMD low). NaN cells remain white.
    """
    N = len(labels)
    fig, ax = plt.subplots(figsize=(max(6, N*0.4), max(5, N*0.4)))
    cax = ax.imshow(matrix, cmap="viridis_r", vmin=vmin, vmax=vmax, interpolation="nearest")
    fig.colorbar(cax, ax=ax)
    ax.set_xticks(np.arange(N))
    ax.set_yticks(np.arange(N))
    ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_title(title)
    plt.tight_layout()
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    fig.savefig(outpath, dpi=300)
    plt.close(fig)
    print(f"Heatmap saved: {outpath}")

def sort_keys_by_model(keys):
    """
    Sort “o3-mini_…” before “o3_…”
    """
    return sorted(keys, key=lambda k: (k.split("_")[0], k))

def sort_keys_by_depth_breadth(keys):
    """
    Sort by suffix “d#_b#” in order d1_b1, d1_b4, d4_b1, d4_b4; unknown last.
    """
    order = {"d1_b1": 0, "d1_b4": 1, "d4_b1": 2, "d4_b4": 3}
    def keyfn(k):
        parts = k.split("_")
        if len(parts) < 4:
            return (99, k)
        suffix = parts[2] + "_" + parts[3]
        return (order.get(suffix, 99), k)
    return sorted(keys, key=keyfn)

def sort_keys_by_engine(keys):
    """
    Put FireCrawl first, then ORKG, within each lex order.
    """
    def keyfn(k):
        engine = k.split("_")[1]
        return (0 if engine == "firecrawl" else 1, k)
    return sorted(keys, key=keyfn)

def main():
    # 1) Load & group all .md reports
    grouped = load_and_group_reports(REPORT_DIR, exclude_keywords=EXCLUDE_KEYS)
    if not grouped:
        print("No groups found—exiting.")
        return

    # Create map: group_key → { index: text }
    group_idx_map = {k: build_index_to_text_map(v) for k, v in grouped.items()}
    all_keys      = sorted(group_idx_map.keys())
    print("All groups:")
    for k in all_keys:
        print("  -", k)
    print()

    # 2) ORKG‐only keys
    orkg_keys = [k for k in all_keys if "_orkg_" in k]
    if orkg_keys:
        # 3) Load Word2Vec once & build WMD function
        print("Loading Word2Vec (GoogleNews) for WMD …")
        w2v_model = KeyedVectors.load_word2vec_format(EMBEDDING_PATH, binary=True)
        wmd_func  = wmd_text_pair_factory(w2v_model)

        N = len(orkg_keys)
        # Initialize full ORKG matrices
        bert_mat_all    = np.full((N, N), np.nan, dtype=float)
        bert_counts_all = np.zeros((N, N), dtype=int)
        wmd_mat_all     = np.full((N, N), np.nan, dtype=float)
        wmd_counts_all  = np.zeros((N, N), dtype=int)

        print("\n=== Computing full ORKG matrices (BERT & WMD) … ===")
        for i, key_i in enumerate(orkg_keys):
            map_i = group_idx_map[key_i]
            for j, key_j in enumerate(orkg_keys):
                map_j = group_idx_map[key_j]
                # BERT
                avg_b, cnt_b = average_metric_over_indices(map_i, map_j, bert_text_pair)
                # WMD
                avg_w, cnt_w = average_metric_over_indices(map_i, map_j, wmd_func)
                if cnt_b > 0:
                    bert_mat_all[i, j]    = avg_b
                    bert_counts_all[i, j] = cnt_b
                if cnt_w > 0:
                    wmd_mat_all[i, j]     = avg_w
                    wmd_counts_all[i, j]  = cnt_w
            print(f"Done row {i+1}/{N} (full ORKG)")

        # 4) Produce three sorted views from the same full matrices
        sorts = [
            ("by_model",        sort_keys_by_model(orkg_keys)),
            ("by_depthbreadth", sort_keys_by_depth_breadth(orkg_keys)),
            ("by_engine",       sort_keys_by_engine(orkg_keys))
        ]
        for label, sorted_keys in sorts:
            idx_map = {k: orkg_keys.index(k) for k in orkg_keys}
            indices = [idx_map[k] for k in sorted_keys]

            # Reorder full matrices according to indices
            bert_mat_sorted    = bert_mat_all[np.ix_(indices, indices)]
            bert_counts_sorted = bert_counts_all[np.ix_(indices, indices)]
            wmd_mat_sorted     = wmd_mat_all[np.ix_(indices, indices)]
            wmd_counts_sorted  = wmd_counts_all[np.ix_(indices, indices)]

            print(f"\n--- Saving ORKG sorted {label} ---")
            base_b = os.path.join(OUTPUT_DIR, f"orkg_bertscore_{label}")
            save_matrix_and_counts(bert_mat_sorted, bert_counts_sorted, sorted_keys, base_b)
            plot_heatmap(
                bert_mat_sorted, sorted_keys,
                title=f"ORKG BERTScore‐F1 ({label})",
                outpath=base_b + "_heatmap.png",
                vmin=0.0, vmax=1.0
            )

            base_w = os.path.join(OUTPUT_DIR, f"orkg_wmd_{label}")
            save_matrix_and_counts(wmd_mat_sorted, wmd_counts_sorted, sorted_keys, base_w)
            plot_heatmap(
                wmd_mat_sorted, sorted_keys,
                title=f"ORKG WMD Distance ({label})",
                outpath=base_w + "_heatmap.png",
                vmin=0.0, vmax=1.0
            )
    else:
        print("No ORKG groups found—skipping ORKG portion.")

    # 5) RQ3: ORKG vs FireCrawl pairs
    fire_keys = [k for k in all_keys if "_firecrawl_" in k]
    pairs = []
    for ok in orkg_keys:
        parts = ok.split("_")
        if len(parts) < 4:
            continue
        model, engine, depth, breadth = parts[0], parts[1], parts[2], parts[3]
        fc_candidate = f"{model}_firecrawl_{depth}_{breadth}"
        if fc_candidate in fire_keys:
            pairs.append((model, depth, breadth, ok, fc_candidate))

    if pairs:
        combo_keys = []
        for (model, depth, breadth, ok, fc) in sorted(pairs, key=lambda x: (x[0], x[1], x[2])):
            combo_keys.append(ok)
            combo_keys.append(fc)

        N2 = len(combo_keys)
        bert_mat2    = np.full((N2, N2), np.nan, dtype=float)
        bert_counts2 = np.zeros((N2, N2), dtype=int)
        wmd_mat2     = np.full((N2, N2), np.nan, dtype=float)
        wmd_counts2  = np.zeros((N2, N2), dtype=int)

        print("\n=== Computing RQ3 block (ORKG vs FireCrawl) … ===")
        for i, k_i in enumerate(combo_keys):
            map_i = group_idx_map[k_i]
            parts_i = k_i.split("_")
            model_i, engine_i, depth_i, breadth_i = parts_i[0], parts_i[1], parts_i[2], parts_i[3]
            for j, k_j in enumerate(combo_keys):
                map_j = group_idx_map[k_j]
                parts_j = k_j.split("_")
                model_j, engine_j, depth_j, breadth_j = parts_j[0], parts_j[1], parts_j[2], parts_j[3]

                if i == j:
                    avg_b, cnt_b = average_metric_over_indices(map_i, map_j, bert_text_pair)
                    avg_w, cnt_w = average_metric_over_indices(map_i, map_j, wmd_func)
                    if cnt_b > 0:
                        bert_mat2[i, j]    = avg_b
                        bert_counts2[i, j] = cnt_b
                    if cnt_w > 0:
                        wmd_mat2[i, j]     = avg_w
                        wmd_counts2[i, j]  = cnt_w
                elif (model_i == model_j and depth_i == depth_j and breadth_i == breadth_j and engine_i != engine_j):
                    avg_b, cnt_b = average_metric_over_indices(map_i, map_j, bert_text_pair)
                    avg_w, cnt_w = average_metric_over_indices(map_i, map_j, wmd_func)
                    if cnt_b > 0:
                        bert_mat2[i, j]    = avg_b
                        bert_counts2[i, j] = cnt_b
                    if cnt_w > 0:
                        wmd_mat2[i, j]     = avg_w
                        wmd_counts2[i, j]  = cnt_w
            print(f"RQ3 row {i+1}/{N2} done")

        # Save & plot RQ3
        base_b2 = os.path.join(OUTPUT_DIR, "rq3_bertscore_orc_fx")
        save_matrix_and_counts(bert_mat2, bert_counts2, combo_keys, base_b2)
        plot_heatmap(
            bert_mat2, combo_keys,
            title="RQ3: ORKG vs FireCrawl BERTScore",
            outpath=base_b2 + "_heatmap.png",
            vmin=0.0, vmax=1.0
        )

        base_w2 = os.path.join(OUTPUT_DIR, "rq3_wmd_orc_fx")
        save_matrix_and_counts(wmd_mat2, wmd_counts2, combo_keys, base_w2)
        plot_heatmap(
            wmd_mat2, combo_keys,
            title="RQ3: ORKG vs FireCrawl WMD",
            outpath=base_w2 + "_heatmap.png",
            vmin=0.0, vmax=1.0
        )
    else:
        print("No FireCrawl–ORKG matching pairs found—skipping RQ3.")

    print("\nAll done. Outputs in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
