import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── USER EDITABLE ─────────────────────────────────────────────────────────────
# Any keyword in this list will cause its matching group to be excluded from the heatmap.
EXCLUDE_KEYWORDS = ["firecrawl"]
# ────────────────────────────────────────────────────────────────────────────────

def main():
    # 1
    report_dir = "../data/reports"
    pattern = os.path.join(report_dir, "*.md")
    paths = glob.glob(pattern)
    print(f"Found {len(paths)} total Markdown files in '{report_dir}'.\n")

    # 2 import via filename
    #    Filename format assumed: "<index>_<model>_<engine>_d<depth>_b<breadth>.md"
    grouped = {}
    for path in paths:
        fname = os.path.basename(path)
        parts = fname[:-3].split("_")  
        if len(parts) >= 5:
            model   = parts[1]
            engine  = parts[2]
            depth   = parts[3]   
            breadth = parts[4]   
            group_key = f"{model}_{engine}_{depth}_{breadth}"
        else:
            group_key = "misc"

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        grouped.setdefault(group_key, []).append(text)

    print("Groups before exclusion:")
    for key, docs in grouped.items():
        print(f"  • {key}: {len(docs)} document(s)")
    print()

    # 3 filter
    filtered_grouped = {}
    for key, docs in grouped.items():
        lowercase_key = key.lower()
        if any(keyword.lower() in lowercase_key for keyword in EXCLUDE_KEYWORDS):
            print(f"Excluding group '{key}' (matches exclude keyword).")
            continue
        filtered_grouped[key] = docs

    print("\nGroups after exclusion:")
    for key, docs in filtered_grouped.items():
        print(f"  • {key}: {len(docs)} document(s)")
    print()

    # 4 exit if empty
    all_docs = [doc for docs in filtered_grouped.values() for doc in docs]
    if not all_docs:
        print("No files remain after exclusion. Exiting.")
        return

    # 5 Build a single TF–IDF space 
    print(f"Building TF–IDF vectorizer over {len(all_docs)} document(s)...")
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    vectorizer.fit(all_docs)
    vocab_size = len(vectorizer.vocabulary_)
    print(f"  → Vocabulary size (max_features): {vocab_size}\n")

    # 6 For each group, compute its "centroid" TF–IDF vector
    centroids = {}
    for key, docs in filtered_grouped.items():
        tfidf_matrix = vectorizer.transform(docs)    
        centroid_matrix = tfidf_matrix.mean(axis=0)     
        centroid_array = np.asarray(centroid_matrix).ravel()  
        centroids[key] = centroid_array

        print(f"Computed centroid for group '{key}':")
        print(f"  - Number of docs in group: {len(docs)}")
        print(f"  - Centroid vector dimension: {centroid_array.shape[0]}\n")

    # 7 Build a sorted list of group_keys and compute an n×n similarity matrix
    group_keys = sorted(centroids.keys())
    n = len(group_keys)
    print(f"Computing pairwise similarities among {n} group centroid(s)...\n")

    sim_matrix = np.zeros((n, n))
    for i, key_i in enumerate(group_keys):
        for j, key_j in enumerate(group_keys):
            vec_i = centroids[key_i].reshape(1, -1)
            vec_j = centroids[key_j].reshape(1, -1)
            score = cosine_similarity(vec_i, vec_j)[0, 0]
            sim_matrix[i, j] = score
            print(f"Similarity('{key_i}', '{key_j}') = {score:.4f}")
        print()

    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "group_centroid_similarity.csv")
    print(f"Writing similarity matrix to: {csv_path}")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([""] + group_keys)
        for i, key_i in enumerate(group_keys):
            row = [key_i] + [f"{sim_matrix[i, j]:.6f}" for j in range(n)]
            writer.writerow(row)
    print("CSV file written.\n")

    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.matshow(sim_matrix, cmap="viridis")
    fig.colorbar(cax)

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(group_keys, rotation=90, fontsize=8)
    ax.set_yticklabels(group_keys, fontsize=8)
    ax.set_title("Average Similarity Between Groups")

    plt.tight_layout()

    heatmap_path = os.path.join(output_dir, "group_centroid_similarity.png")
    print(f"Saving heatmap image to: {heatmap_path}\n")
    fig.savefig(heatmap_path, dpi=300)
    plt.close(fig)

    print("Done.")

if __name__ == "__main__":
    main()
