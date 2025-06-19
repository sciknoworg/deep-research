#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import glob
import numpy as np
import csv
import matplotlib.pyplot as plt
from bert_score import score as bert_score
import nltk
nltk.download('wordnet', quiet=True)

# ── EINSTELLUNGEN ────────────────────────────────────────────────────────────────
REPORT_DIR = "../data/reports"
OUTPUT_DIR = "../data/paper_results"
# Wir verwenden SciBERT für BERTScore
SCIBERT = "allenai/scibert_scivocab_uncased"
EXCLUDE = ["firecrawl"]  # FireCrawl-Gruppen ignorieren
# ────────────────────────────────────────────────────────────────────────────────

def load_and_group(report_dir, exclude_keys):
    grouped = {}
    for p in sorted(glob.glob(os.path.join(report_dir, "*.md"))):
        fn = os.path.basename(p)
        parts = fn[:-3].split("_")
        if len(parts) < 5:
            continue
        key = f"{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}"
        if any(ex in key.lower() for ex in exclude_keys):
            continue
        with open(p, encoding="utf-8") as f:
            text = f.read()
        grouped.setdefault(key, []).append((fn, text))
    return grouped

def pick_longest(docs):
    # als Repräsentant pro Gruppe den längsten Report
    return max(docs, key=lambda x: len(x[1]))[1]

def bleu_pair(a,b): return bert_score  # unused placeholder

def bert_pair(txtA, txtB):
    P,R,F = bert_score([txtA],[txtB],
                       model_type="microsoft/deberta-xlarge-mnli",
                       num_layers=12,
                       verbose=False,
                       rescale_with_baseline=True,
                       lang="en")
    return F.item()

def average_over(groups, keys, metric):
    N = len(keys)
    M = np.zeros((N,N),dtype=float)
    for i,ki in enumerate(keys):
        for j,kj in enumerate(keys):
            score = metric(groups[ki], groups[kj])
            M[i,j] = score
        print(f"Reihe {i+1}/{N} fertig")
    return M

def save_and_plot(mat, keys, title, basename, vmin=0, vmax=1):
    os.makedirs(os.path.dirname(basename), exist_ok=True)
    # CSV
    with open(basename+"_matrix.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow([""]+keys)
        for i,k in enumerate(keys):
            w.writerow([k]+[f"{mat[i,j]:.6f}" for j in range(len(keys))])
    # Plot
    fig,ax=plt.subplots(figsize=(6,6))
    cax=ax.imshow(mat,cmap="viridis_r",vmin=vmin,vmax=vmax)
    fig.colorbar(cax,ax=ax)
    ax.set_xticks(np.arange(len(keys))); ax.set_xticklabels(keys,rotation=90,fontsize=6)
    ax.set_yticks(np.arange(len(keys))); ax.set_yticklabels(keys,fontsize=6)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(basename+"_heatmap.png",dpi=300)
    plt.close()

def main():
    # 1) Daten laden & gruppieren
    grouped = load_and_group(REPORT_DIR, EXCLUDE)
    # nur ORKG-Gruppen
    orkg = sorted([k for k in grouped if "_orkg_" in k])
    # jeweils längsten Report je Gruppe extrahieren
    reps = {k: pick_longest(grouped[k]) for k in orkg}

    # 2) RQ1: o3-mini vs o3 über **alle** depth/breadth
    #    → sortiere nach Model-Präfix
    rq1_keys = sorted(orkg, key=lambda k: k.split("_")[0])
    rq1_mat = average_over(reps, rq1_keys, bert_pair)
    save_and_plot(rq1_mat, rq1_keys,
                  "RQ1: SciBERTScore ORKG (o3-mini vs o3)",
                  os.path.join(OUTPUT_DIR,"rq1_orkg_scibert_by_model"))

    # 3) RQ2: alle depth/breadth-Kombinationen innerhalb jedes Modells
    #    → sortiere nach Tiefe–Breite
    order = {"d1_b1":0,"d1_b4":1,"d4_b1":2,"d4_b4":3}
    rq2_keys = sorted(orkg,
                      key=lambda k: (order.get("_".join(k.split("_")[2:4]),99), k))
    rq2_mat = average_over(reps, rq2_keys, bert_pair)
    save_and_plot(rq2_mat, rq2_keys,
                  "RQ2: SciBERTScore ORKG (depth–breadth)",
                  os.path.join(OUTPUT_DIR,"rq2_orkg_scibert_by_depth"))

    print("Fertig! Ergebnisse liegen in", OUTPUT_DIR)

if __name__=="__main__":
    main()
