#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# CPU only
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import glob
import numpy as np
import csv
import matplotlib.pyplot as plt
import torch
import nltk
from transformers import AutoTokenizer, AutoModel
from gensim.models import KeyedVectors
from gensim.similarities import WmdSimilarity

nltk.download('wordnet', quiet=True)

# ── SETTINGS ───────────────────────────────────────────────────────────────────
REPORT_DIR    = "../data/reports"
OUTPUT_DIR    = "../data/paper_results"
SCIBERT_MODEL = "allenai/scibert_scivocab_uncased"
EXCLUDE_KEYS  = []  # alle Engines zulassen
# ────────────────────────────────────────────────────────────────────────────────

def load_and_group_reports(report_dir, exclude_keywords=None):
    if exclude_keywords is None:
        exclude_keywords=[]
    grouped={}
    for path in sorted(glob.glob(os.path.join(report_dir,"*.md"))):
        fname=os.path.basename(path)
        parts=fname[:-3].split("_")
        if len(parts)>=5:
            key=f"{parts[1]}_{parts[2]}_{parts[3]}_{parts[4]}"
        else:
            key="misc"
        if any(ex.lower() in key.lower() for ex in exclude_keywords): continue
        with open(path,encoding="utf-8") as f:
            txt=f.read()
        grouped.setdefault(key,[]).append((fname,txt))
    return grouped

def build_index_map(docs):
    m={}
    for fname,txt in docs:
        try:
            idx=int(fname.split("_")[0])
            m[idx]=txt
        except: pass
    return m

def average_wmd(mapA,mapB,w2v):
    ids=sorted(set(mapA)&set(mapB))
    if not ids: return np.nan,0
    scores=[]
    for i in ids:
        A=[t for t in mapA[i].lower().split() if t.isalpha()]
        B=[t for t in mapB[i].lower().split() if t.isalpha()]
        sim=WmdSimilarity([B],w2v,num_best=1)
        cos=sim[A][0][1] if sim[A] else 0.0
        scores.append(1.0-cos)
    return float(np.mean(scores)),len(ids)

def build_scibert_kv(model_name):
    tok=AutoTokenizer.from_pretrained(model_name)
    mdl=AutoModel.from_pretrained(model_name).eval()
    emb=mdl.get_input_embeddings().weight.detach().cpu().numpy()
    kv=KeyedVectors(vector_size=emb.shape[1])
    inv_vocab=[w for w,i in sorted(tok.vocab.items(),key=lambda x:x[1])]
    kv.add_vectors(inv_vocab,emb)
    return kv

def save_csv(mat,cnt,keys,base):
    os.makedirs(os.path.dirname(base),exist_ok=True)
    with open(base+"_matrix.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow([""]+keys)
        for i,k in enumerate(keys):
            w.writerow([k]+[("" if np.isnan(mat[i,j]) else f"{mat[i,j]:.6f}") for j in range(len(keys))])
    with open(base+"_counts.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow([""]+keys)
        for i,k in enumerate(keys):
            w.writerow([k]+[(""+str(cnt[i,j]) if cnt[i,j]>0 else "") for j in range(len(keys))])

def plot_heatmap(mat,keys,title,out,vmin=0,vmax=1):
    N=len(keys)
    fig,ax=plt.subplots(figsize=(max(6,N*0.3),max(5,N*0.3)))
    c=ax.imshow(mat,cmap="viridis_r",vmin=vmin,vmax=vmax,interpolation="nearest")
    fig.colorbar(c,ax=ax)
    ax.set_xticks(np.arange(N));ax.set_yticks(np.arange(N))
    ax.set_xticklabels(keys,rotation=90,fontsize=6)
    ax.set_yticklabels(keys,fontsize=6)
    ax.set_title(title)
    plt.tight_layout();plt.savefig(out,dpi=300);plt.close()

def sort_by_model(keys):
    return sorted(keys,key=lambda k:(k.split("_")[0],k))
def sort_by_depth(keys):
    order={"d1_b1":0,"d1_b4":1,"d4_b1":2,"d4_b4":3}
    def fn(k):
        suf="_".join(k.split("_")[2:4])
        return (order.get(suf,99),k)
    return sorted(keys,key=fn)
def sort_by_engine(keys):
    return sorted(keys,key=lambda k:(0 if "_firecrawl_" in k else 1,k))

def main():
    grouped=load_and_group_reports(REPORT_DIR,EXCLUDE_KEYS)
    idx_map={k:build_index_map(v) for k,v in grouped.items()}
    keys=sorted(idx_map)
    orkg=[k for k in keys if "_orkg_" in k]
    fire=[k for k in keys if "_firecrawl_" in k]

    print("Loading SciBERT…")
    kv=build_scibert_kv(SCIBERT_MODEL)

    # RQ1: ORKG, sortiert nach Model
    for label, sorter in [("by_model",sort_by_model(orkg)),
                          ("by_depth",sort_by_depth(orkg)),
                          ("by_engine",sort_by_engine(orkg))]:
        ks=sorter
        N=len(ks)
        M=np.full((N,N),np.nan);C=np.zeros((N,N),int)
        for i,a in enumerate(ks):
            for j,b in enumerate(ks):
                m,c=average_wmd(idx_map[a],idx_map[b],kv)
                if c>0: M[i,j]=m; C[i,j]=c
        base=os.path.join(OUTPUT_DIR,f"rq1_orkg_wmd_{label}")
        save_csv(M,C,ks,base)
        plot_heatmap(M,ks,f"RQ1 ORKG WMD ({label})",base+"_heatmap.png")

    # RQ3: ORKG vs FireCrawl
    pairs=[]
    for a in orkg:
        mdl,_,d,b=a.split("_")
        fc=f"{mdl}_firecrawl_{d}_{b}"
        if fc in fire: pairs+=[a,fc]
    if pairs:
        ks=[]
        for x in pairs:
            if x not in ks: ks.append(x)
        N=len(ks)
        M=np.full((N,N),np.nan);C=np.zeros((N,N),int)
        for i,a in enumerate(ks):
            for j,b in enumerate(ks):
                m,c=average_wmd(idx_map[a],idx_map[b],kv)
                if c>0: M[i,j]=m; C[i,j]=c
        base=os.path.join(OUTPUT_DIR,"rq3_orkg_vs_fc_wmd")
        save_csv(M,C,ks,base)
        plot_heatmap(M,ks,"RQ3 ORKG vs FireCrawl WMD",base+"_heatmap.png")

    print("Fertig. Ergebnisse in",OUTPUT_DIR)

if __name__=="__main__":
    main()
