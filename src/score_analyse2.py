#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import csv
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoTokenizer
from bert_score import BERTScorer

# ── SETTINGS ────────────────────────────────────────────────────────────────
REPORT_DIR   = "../data/reports"
OUTPUT_DIR   = "../data/paper_results"
SCIBERT      = "allenai/scibert_scivocab_uncased"
EXCLUDE      = ["firecrawl"]
CHUNK_TOKS   = 510
# ─────────────────────────────────────────────────────────────────────────────

# load reports
def load_reports(path, exclude):
    groups = {}
    for fn in sorted(glob.glob(os.path.join(path, "*.md"))):
        key = "_".join(os.path.basename(fn)[:-3].split("_")[1:5])
        if any(e in key for e in exclude): continue
        idx = int(os.path.basename(fn).split("_")[0])
        with open(fn, encoding='utf-8') as f:
            groups.setdefault(key, {})[idx] = f.read()
    return groups

groups = load_reports(REPORT_DIR, EXCLUDE)
orkg_keys = sorted(k for k in groups if "orkg" in k)
print("→ ORKG groups:", orkg_keys)

# init
scorer = BERTScorer(model_type=SCIBERT, lang='en', idf=False, rescale_with_baseline=False)
tokenizer = AutoTokenizer.from_pretrained(SCIBERT)

def preprocess_chunk(text):
    ids = tokenizer.encode(text, add_special_tokens=False)
    if len(ids) > CHUNK_TOKS:
        ids = ids[:CHUNK_TOKS]
    return tokenizer.decode(ids, skip_special_tokens=True)

def chunk_text(text):
    ids = tokenizer.encode(text, add_special_tokens=False)
    return [preprocess_chunk(tokenizer.decode(ids[i:i+CHUNK_TOKS], skip_special_tokens=True))
            for i in range(0, len(ids), CHUNK_TOKS)]

# heatmap
def pairwise_heatmap(keys, sort_fn, title, outname):
    ordered = sorted(keys, key=sort_fn); N=len(ordered)
    M = np.zeros((N,N))
    for i,a in enumerate(ordered):
        for j,b in enumerate(ordered):
            vals=[]
            for k in set(groups[a])&set(groups[b]):
                ca=chunk_text(groups[a][k]); cb=chunk_text(groups[b][k])
                for sa,sb in zip(ca,cb):
                    _,_,F1=scorer.score([sa],[sb])
                    vals.append(F1[0].item())
            M[i,j] = np.mean(vals) if vals else np.nan
        print(f"{title} row {i+1}/{N} done")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # save CSV
    with open(os.path.join(OUTPUT_DIR,f"{outname}.csv"),'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow([""]+ordered)
        for r,key in enumerate(ordered): w.writerow([key]+[f"{M[r,c]:.4f}" for c in range(N)])
    # plot
    fig,ax=plt.subplots(figsize=(6,6)); c=ax.imshow(M,cmap='viridis_r',vmin=0,vmax=1)
    fig.colorbar(c,ax=ax)
    ax.set_xticks(range(N)); ax.set_xticklabels(ordered,rotation=90,fontsize=6)
    ax.set_yticks(range(N)); ax.set_yticklabels(ordered,fontsize=6)
    ax.set_title(title)
    fig.tight_layout(); fig.savefig(os.path.join(OUTPUT_DIR,f"{outname}_heatmap.png"),dpi=300)
    plt.close(fig)

pairwise_heatmap(orkg_keys, lambda k:k.split("_")[0], "RQ1: SciBERT BERTScore F1 (by model)", "rq1_bertscore_by_model")
order_map = {"d1_b1":0,"d1_b4":1,"d4_b1":2,"d4_b4":3}
pairwise_heatmap(orkg_keys, lambda k:(order_map["_".join(k.split("_")[2:4])],k),
                 "RQ2: SciBERT BERTScore F1 (by depth/breadth)","rq2_bertscore_by_depth")
print("Done — outputs at", OUTPUT_DIR)
