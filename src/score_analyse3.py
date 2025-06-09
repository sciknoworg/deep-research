import os
os.environ["CUDA_VISIBLE_DEVICES"] = "" 

import glob
import numpy as np
import matplotlib.pyplot as plt
import csv

from bert_score import score as bert_score
from gensim.models import KeyedVectors
from gensim.similarities import WmdSimilarity
import nltk
nltk.download('wordnet', quiet=True)

# ── Settings ────────────────────────────────────────────────────────────────
REPORT_DIR     = "../data/reports"
OUTPUT_DIR     = "../data/paper_results/rq3_subset"
EMBEDDING_PATH = "../embeddings/GoogleNews-vectors-negative300.bin.gz"
MODELS   = ["o3-mini", "o3"]
ENGINES  = ["orkg", "firecrawl"]
SUFFIXES = ["d1_b4", "d4_b1"]
# ────────────────────────────────────────────────────────────────────────────────

def load_grouped():
    grouped = {}
    for path in glob.glob(os.path.join(REPORT_DIR, "*.md")):
        name = os.path.basename(path)[:-3]
        parts = name.split("_")
        if len(parts) < 5:
            continue
        idx, model, engine, depth, breadth = parts
        key = f"{model}_{engine}_{depth}_{breadth}"
        if model in MODELS and engine in ENGINES and f"{depth}_{breadth}" in SUFFIXES:
            grouped.setdefault(key, []).append((int(idx), open(path, encoding="utf-8").read()))
    return grouped

def map_by_idx(docs):
    return {i: t for i,t in docs}

def avg_and_count(A, B, fn):
    common = sorted(set(A) & set(B))
    print(f"   Overlap {len(common)} docs")
    if not common:
        return np.nan, 0
    scores = [fn(A[i], B[i]) for i in common]
    return float(np.mean(scores)), len(common)

def make_wmd(model):
    def tok(s): return [w for w in s.lower().split() if w.isalpha()]
    def f(a,b):
        tA, tB = tok(a), tok(b)
        index = WmdSimilarity([tB], model, num_best=1)
        sim = index[tA]
        return 1 - sim[0][1] if sim else 1.0
    return f

def bert_f1(a,b):
    P,R,F = bert_score([a],[b],
                       model_type="bert-base-uncased",
                       num_layers=9,
                       verbose=False,
                       rescale_with_baseline=True,
                       lang="en")
    return F.item()

def save_csv(mat, cnt, labels, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/{name}_matrix.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow([""]+labels)
        for i,l in enumerate(labels):
            w.writerow([l] + [f"{mat[i,j]:.4f}" for j in range(len(labels))])
    with open(f"{OUTPUT_DIR}/{name}_counts.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow([""]+labels)
        for i,l in enumerate(labels):
            w.writerow([l] + [str(cnt[i,j]) for j in range(len(labels))])

def plot(mat, labels, title, name, vmin, vmax):
    plt.figure(figsize=(max(6,len(labels)*0.4), max(5,len(labels)*0.4)))
    plt.imshow(mat, cmap="viridis_r", vmin=vmin, vmax=vmax, interpolation="nearest")
    plt.colorbar()
    plt.xticks(range(len(labels)), labels, rotation=90, fontsize=8)
    plt.yticks(range(len(labels)), labels, fontsize=8)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/{name}_heatmap.png", dpi=300)
    plt.close()

def main():
    grouped = load_grouped()
    labels = sorted(grouped.keys())
    print("Selected 8 groups:")
    for l in labels: print(" ",l)
    maps = [map_by_idx(grouped[k]) for k in labels]

    # Embeddings laden
    print("Loading Word2Vec for WMD…")
    w2v = KeyedVectors.load_word2vec_format(EMBEDDING_PATH, binary=True)
    wmd = make_wmd(w2v)

    N = len(labels)
    bert_mat = np.zeros((N,N))
    wmd_mat  = np.zeros((N,N))
    cnt_mat  = np.zeros((N,N),int)

    print("\n=== RQ3 subset pairwise ===")
    for i,ki in enumerate(labels):
        print(f"Row {i+1}/{N}: {ki}")
        for j,kj in enumerate(labels):
            print(f" {ki:30} vs {kj:30}", end="")
            b,c = avg_and_count(maps[i], maps[j], bert_f1)
            w,_ = avg_and_count(maps[i], maps[j], wmd)
            bert_mat[i,j], wmd_mat[i,j], cnt_mat[i,j] = b, w, c

    save_csv(bert_mat, cnt_mat, labels, "rq3_bert")
    plot(bert_mat, labels, "RQ3 BERT-F1 subset", "rq3_bert", 0, 1)

    save_csv(wmd_mat, cnt_mat, labels, "rq3_wmd")
    plot(wmd_mat, labels, "RQ3 WMD subset", "rq3_wmd", 0, 1)

    print("\nDone. Outputs in", OUTPUT_DIR)

if __name__=="__main__":
    main()
