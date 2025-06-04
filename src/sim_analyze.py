import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Find all Markdown reports in /mnt/data (or adjust path if needed)
report_dir = "reports"
pattern = os.path.join(report_dir, "*.md")
paths = glob.glob(pattern)

# 2. Parse filenames into groups and load their contents
#    Expected filename format: "<index>_<model>_<engine>_d<depth>_b<breadth>.md"
grouped = {}
for path in paths:
    fname = os.path.basename(path)
    parts = fname[:-3].split("_")  # drop ".md" and split
    if len(parts) >= 5:
        model   = parts[1]
        engine  = parts[2]
        depth   = parts[3]  # e.g. "d4"
        breadth = parts[4]  # e.g. "b1"
        group_key = f"{model}_{engine}_{depth}_{breadth}"
    else:
        group_key = "misc"

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Append (filename, content) to the appropriate group
    grouped.setdefault(group_key, []).append((fname, text))

# 3. Ensure output folder exists
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# 4. For each group that has ≥2 documents, compute TF–IDF + cosine similarity and save a heatmap
for group_key, items in grouped.items():
    docs  = [content for _, content in items]
    names = [name for name, _ in items]
    n     = len(docs)

    if n < 2:
        continue  # skip groups with fewer than two reports

    # Compute TF–IDF vectors of all documents in this group
    vec   = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf = vec.fit_transform(docs)

    # Compute pairwise cosine-similarity matrix
    sim = cosine_similarity(tfidf)

    # Plot heatmap (but do not show)
    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(sim, cmap="viridis")
    fig.colorbar(cax)

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(names, rotation=90, fontsize=8)
    ax.set_yticklabels(names, fontsize=8)
    ax.set_title(f"Similarity for group {group_key}")

    plt.tight_layout()

    # Save to "data/sim_<group_key>.png"
    out_path = os.path.join(output_dir, f"heat_{group_key}.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)

    print(f"Heatmap für '{group_key}' gespeichert in: {out_path}")
