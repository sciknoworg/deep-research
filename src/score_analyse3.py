#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, glob, csv
import numpy as np
import matplotlib.pyplot as plt
import nltk

import torch
from transformers import AutoTokenizer, AutoModel
from rouge_score import rouge_scorer
from nltk.tokenize import sent_tokenize
from gensim.models import KeyedVectors
from gensim.similarities import WmdSimilarity

nltk.download('punkt_tab')

# ── EINSTELLUNGEN ────────────────────────────────────────────────────────────────
REPORT_DIR = "../data/reports"
OUTPUT_DIR = "../data/paper_results"
EXCLUDE    = ["firecrawl"]               # FireCrawl-Gruppen ignorieren
SCIBERT    = "allenai/scibert_scivocab_uncased"
# ────────────────────────────────────────────────────────────────────────────────

def load_reports(report_dir, exclude):
    groups = {}
    for path in glob.glob(os.path.join(report_dir, "*.md")):
        fn = os.path.basename(path)
        parts = fn[:-3].split("_")
        if len(parts) < 5: continue
        idx, model, engine, depth, breadth = parts[:5]
        key = f"{model}_{engine}_{depth}_{breadth}"
        if any(ex in key for ex in exclude): continue
        text = open(path, encoding="utf-8").read()
        groups.setdefault(key, {})[int(idx)] = text
    return groups

def build_scibert_model(name):
    tok = AutoTokenizer.from_pretrained(name)
    mdl = AutoModel.from_pretrained(name).eval().to("cpu")
    return tok, mdl

def embed_text(text, tokenizer, model):
    # Sentence-split und mean-pooling über Token-Embeddings
    sents = sent_tokenize(text)
    all_emb = []
    for s in sents:
        tokens = tokenizer(s, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            out = model(**tokens)
        # mean over token embeddings (exclude padding)
        emb = out.last_hidden_state.mean(dim=1).squeeze(0).cpu().numpy()
        all_emb.append(emb)
    return np.stack(all_emb)  # shape (n_sents, dim)

def avg_bert_sim(a, b, tokenizer, model):
    eA = embed_text(a, tokenizer, model)
    eB = embed_text(b, tokenizer, model)
    # cos sim matrix
    sim = (eA @ eB.T) / (np.linalg.norm(eA, axis=1)[:,None] * np.linalg.norm(eB, axis=1)[None,:] + 1e-8)
    # average of diagonal of min(n,n)
    n = min(sim.shape)
    return float(np.mean(np.diag(sim[:n,:n])))

def rouge_pair(a, b, scorer):
    sc = scorer.score(b, a)
    return sc["rouge1"].fmeasure, sc["rougeL"].fmeasure

def build_wmd(kv):
    def f(a, b):
        toksA = [w for w in a.lower().split() if w in kv]
        toksB = [w for w in b.lower().split() if w in kv]
        index = WmdSimilarity([toksB], kv, num_best=1)
        sims = index[toksA]
        return 1.0 - sims[0][1] if sims else 1.0
    return f

def compute_matrix(keys, data, tokenizer, model, kv):
    N = len(keys)
    M_bert = np.zeros((N,N))
    M_r1   = np.zeros((N,N))
    M_rL   = np.zeros((N,N))
    M_wmd  = np.zeros((N,N))
    rouge  = rouge_scorer.RougeScorer(["rouge1","rougeL"], use_stemmer=True)
    wmd_fn = build_wmd(kv)

    for i,ka in enumerate(keys):
        for j,kb in enumerate(keys):
            idxs = set(data[ka]) & set(data[kb])
            b, r1, rL, w = [], [], [], []
            for idx in idxs:
                A, B = data[ka][idx], data[kb][idx]
                b.append(avg_bert_sim(A, B, tokenizer, model))
                x1, xL = rouge_pair(A, B, rouge)
                r1.append(x1); rL.append(xL)
                w.append(wmd_fn(A, B))
            M_bert[i,j] = np.mean(b)
            M_r1[i,j]   = np.mean(r1)
            M_rL[i,j]   = np.mean(rL)
            M_wmd[i,j]  = np.mean(w)
        print(f"Row {i+1}/{N} done")
    return M_bert, M_r1, M_rL, M_wmd

def plot_save(mat, keys, title, fname, vmin=0, vmax=1):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # CSV
    with open(f"{OUTPUT_DIR}/{fname}.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow([""]+keys)
        for i,k in enumerate(keys):
            w.writerow([k]+[f"{mat[i,j]:.4f}" for j in range(len(keys))])
    # Heatmap
    fig,ax=plt.subplots(figsize=(6,6))
    cax=ax.imshow(mat,cmap="viridis_r",vmin=vmin,vmax=vmax)
    fig.colorbar(cax,ax=ax)
    ax.set_xticks(range(len(keys))); ax.set_xticklabels(keys,rotation=90,fontsize=6)
    ax.set_yticks(range(len(keys))); ax.set_yticklabels(keys,fontsize=6)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{fname}.png",dpi=300)
    plt.close()

def main():
    data = load_reports(REPORT_DIR, EXCLUDE)
    keys = sorted(data.keys())
    print("Groups:", keys)

    # SciBERT laden
    print("Loading SciBERT…")
    tok, mdl = build_scibert_model(SCIBERT)

    # SciBERT-Vektoren für WMD
    print("Building KeyedVectors from SciBERT embeddings…")
    emb = mdl.get_input_embeddings().weight.detach().cpu().numpy()
    kv = KeyedVectors(vector_size=emb.shape[1])
    inv = [w for w,i in sorted(tok.vocab.items(), key=lambda x:x[1])]
    kv.add_vectors(inv, emb)

    # Matrix berechnen
    B, R1, RL, W = compute_matrix(keys, data, tok, mdl, kv)

    # RQ1: sort by model prefix
    s1 = sorted(keys, key=lambda k: k.split("_")[0])
    idx1 = [keys.index(k) for k in s1]
    for mat,name,ttl in [
      (B,  "rq1_bert_by_model",   "RQ1: SciBERT‐Sim by model"),
      (R1, "rq1_rouge1_by_model", "RQ1: ROUGE‐1 by model"),
      (RL, "rq1_rougel_by_model", "RQ1: ROUGE‐L by model"),
      (W,  "rq1_wmd_by_model",    "RQ1: WMD by model")
    ]:
        m = mat[np.ix_(idx1,idx1)]
        plot_save(m, s1, ttl, name)

    # RQ2: sort by depth–breadth
    order = {"d1_b1":0,"d1_b4":1,"d4_b1":2,"d4_b4":3}
    s2 = sorted(keys, key=lambda k:(order["_".join(k.split("_")[2:4])],k))
    idx2 = [keys.index(k) for k in s2]
    for mat,name,ttl in [
      (B,  "rq2_bert_by_depth",   "RQ2: SciBERT‐Sim by depth"),
      (R1, "rq2_rouge1_by_depth", "RQ2: ROUGE‐1 by depth"),
      (RL, "rq2_rougel_by_depth", "RQ2: ROUGE‐L by depth"),
      (W,  "rq2_wmd_by_depth",    "RQ2: WMD by depth")
    ]:
        m = mat[np.ix_(idx2,idx2)]
        plot_save(m, s2, ttl, name)

    print("Done — outputs in", OUTPUT_DIR)

if __name__=="__main__":
    main()
