# src/sim_analyze.py
# Paper-parity heatmaps (ROUGE-L F1, BERTScore F1 [SciBERT], 1−WMD via WmdSimilarity)
# - Repo-relative paths (works from anywhere)
# - WMD uses precomputed SciBERT embeddings (KeyedVectors) + WmdSimilarity
# - BERTScore uses SciBERT with conservative 480-token chunking (avoids >512 issue)
# - ROUGE-L uses stemming
# - Strict 49×49 alignment (same indices across groups) with clear error if mismatch
# - Optional "core section" extraction to avoid Learnings/URLs noise
#
# Usage:
#   1) Edit the CONSTANTS below.
#   2) pip install: rouge-score bert-score gensim numpy pandas matplotlib torch transformers sentencepiece
#   3) Run: python -m src.sim_analyze

from __future__ import annotations
import os
import re
import math
import itertools
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from rouge_score import rouge_scorer
from bert_score import score as bert_score

import torch
from transformers import AutoTokenizer, AutoModel
from gensim.models import KeyedVectors
from gensim.similarities import WmdSimilarity

# =========================
# EDIT THESE CONSTANTS ONLY
# =========================

# Resolve repo root from this file location
REPO_ROOT = Path(__file__).resolve().parents[1]

# Input/Output
REPORTS_ROOT = REPO_ROOT / "data" / "reports-nlp"   # folder with *.md reports
OUT_DIR      = REPO_ROOT / "data" / "quant-nlp"     # output folder for CSV/PNGs

# Config ordering (rows/cols of the matrices)
MODELS   = ("o3", "o3-mini")
DEPTHS   = (1, 4)
BREADTHS = (1, 4)

# Engine filtering (paper used ORKG); set to () to allow all
ENGINE_WHITELIST = ("orkg",)
EXCLUDE_KEYWORDS = ("firecrawl",)  # exclude file keys containing any of these (case-insensitive)

# Paper-parity models/settings
SCIBERT_NAME     = "allenai/scibert_scivocab_uncased"
BERT_BATCH_SIZE  = 16          # affects speed/memory only, not the score
CHUNK_TOK_LEN    = 480         # conservative caps to avoid >512 after re-tokenization

# Precomputed SciBERT embeddings for WMD (gensim KeyedVectors)
SCIBERT_KV_PATH  = REPO_ROOT / "data" / "embeddings" / "scibert_tokens.kv"

# Strict 49×49 alignment across groups
STRICT_ENFORCE_SAME_INDICES = True
EXPECTED_COUNT = 49           # sanity guard; set to None to disable
CAP_WMD_TO_01  = True         # clip 1−WMD to [0,1] for nicer visuals

# Core-only scoring (extract synthesis between "Final Report" and "Visited URLs/References")
USE_CORE_SECTION = True
SECTION_START = [r"^\s*Final Report\s*:?\s*$", r"^\s*Final Answer\s*:?\s*$", r"^\s*Report\s*:?\s*$"]
SECTION_END   = [r"^\s*Visited URLs\s*:?\s*$", r"^\s*References\s*:?\s*$", r"^\s*Citations\s*:?\s*$",
                 r"^\s*Sources\s*:?\s*$", r"^\s*Learnings\s*:?\s*$",
                 r"^\s*Report has been saved", r"^\s*Answer has been saved"]

# Determinism/quietness
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
torch.set_num_threads(1)  # optional: keeps things tame on shared nodes

# =========================
# DO NOT EDIT BELOW
# =========================

FNAME_RE = re.compile(
    r"(?P<idx>\d+?)_(?P<model>[a-z0-9\-]+)_(?P<engine>[a-z]+)_d(?P<depth>\d+)_b(?P<breadth>\d+)\.md$",
    re.I,
)

def extract_core(text: str) -> str:
    """Extract the core synthesis between SECTION_START and SECTION_END markers."""
    if not USE_CORE_SECTION:
        return text
    lines = text.splitlines()
    # start
    s = 0
    for i, ln in enumerate(lines):
        if any(re.search(p, ln, flags=re.I) for p in SECTION_START):
            s = i + 1
            break
    # end
    e = len(lines)
    for j in range(s, len(lines)):
        if any(re.search(p, lines[j], flags=re.I) for p in SECTION_END):
            e = j
            break
    core = "\n".join(lines[s:e]).strip()
    return core if core else text.strip()

def load_reports(root: Path) -> Dict[Tuple[str,int,int,str], Dict[int,str]]:
    """
    Scan *.md and group by (model, depth, breadth, engine)
    Returns: groups[(model, depth, breadth, engine)] -> { idx -> core_text }
    """
    groups: Dict[Tuple[str,int,int,str], Dict[int,str]] = defaultdict(dict)
    for p in root.rglob("*.md"):
        m = FNAME_RE.match(p.name)
        if not m:
            continue
        idx     = int(m.group("idx"))
        model   = m.group("model").lower()
        engine  = m.group("engine").lower()
        depth   = int(m.group("depth"))
        breadth = int(m.group("breadth"))

        if ENGINE_WHITELIST and engine not in ENGINE_WHITELIST:
            continue

        key_str = f"{model}_{engine}_d{depth}_b{breadth}".lower()
        if any(ex.lower() in key_str for ex in EXCLUDE_KEYWORDS):
            continue

        raw  = p.read_text(encoding="utf-8", errors="ignore")
        core = extract_core(raw)
        groups[(model, depth, breadth, engine)][idx] = core
    return groups

def index_set(d: Dict[int,str]) -> Set[int]:
    return set(d.keys())

def require_same_index_set(groups: Dict[Tuple[str,int,int,str], Dict[int,str]],
                           keys: List[Tuple[str,int,int,str]]) -> List[int]:
    """Use the first key as reference; enforce EXACT same indices for all groups."""
    ref_key = keys[0]
    ref_idx = index_set(groups[ref_key])
    if EXPECTED_COUNT is not None and len(ref_idx) != EXPECTED_COUNT:
        raise ValueError(f"[strict] Reference {ref_key} has {len(ref_idx)} items; expected {EXPECTED_COUNT}.")
    for k in keys[1:]:
        k_idx = index_set(groups[k])
        missing = sorted(ref_idx - k_idx)
        extra   = sorted(k_idx - ref_idx)
        if missing or extra:
            msg = [f"[strict] Index set mismatch for {k} vs ref {ref_key}:"]
            if missing: msg.append(f"  Missing: {missing}")
            if extra:   msg.append(f"  Extra:   {extra}")
            raise ValueError("\n".join(msg))
        if EXPECTED_COUNT is not None and len(k_idx) != EXPECTED_COUNT:
            raise ValueError(f"[strict] Group {k} has {len(k_idx)} items; expected {EXPECTED_COUNT}.")
    return sorted(ref_idx)

# ---------- ROUGE-L F1 ----------
def rougeL_f1(pairs: List[Tuple[int,str,str]]) -> float:
    if not pairs: return float("nan")
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    vals = []
    for _, a, b in pairs:
        # Note: metric is symmetric enough; we follow score_analyse style: ref=b, cand=a
        vals.append(scorer.score(b, a)["rougeL"].fmeasure)
    return float(np.mean(vals)) if vals else float("nan")

# ---------- BERTScore F1 (SciBERT + conservative chunking) ----------
_scibert_tok = AutoTokenizer.from_pretrained(SCIBERT_NAME)

def chunk_text_to_len(text: str, tok=_scibert_tok, max_wp_len: int = CHUNK_TOK_LEN) -> List[str]:
    """
    Chunk by SciBERT WordPiece with conservative cap (default 480).
    This leaves headroom so that bert_score's re-tokenization never exceeds 512 incl. specials.
    """
    wp_ids = tok.encode(text, add_special_tokens=False)
    chunks = []
    for i in range(0, len(wp_ids), max_wp_len):
        sub = wp_ids[i:i+max_wp_len]
        if not sub:
            continue
        chunks.append(tok.decode(sub, skip_special_tokens=True))
    return chunks or [""]

def bertscore_f1(pairs: List[Tuple[int,str,str]],
                 model_type: str = SCIBERT_NAME,
                 batch_size: int = BERT_BATCH_SIZE) -> float:
    if not pairs: return float("nan")
    # Aggregate chunk pairs across all documents and score in one (batched) call
    cands_all: List[str] = []
    refs_all:  List[str] = []
    for _, a, b in pairs:
        a_chunks = chunk_text_to_len(a)
        b_chunks = chunk_text_to_len(b)
        n = min(len(a_chunks), len(b_chunks))
        if n <= 0:
            continue
        cands_all.extend(a_chunks[:n])
        refs_all.extend(b_chunks[:n])
    if not cands_all:
        return float("nan")
    _, _, F1 = bert_score(cands_all, refs_all,
                          model_type=model_type, lang="en",
                          rescale_with_baseline=False, batch_size=batch_size)
    return float(F1.mean().item())

# ---------- SciBERT KeyedVectors (precompute & cache) ----------
def build_or_load_scibert_kv(kv_path: Path, model_name: str) -> KeyedVectors:
    kv_path = Path(kv_path)
    if kv_path.exists():
        return KeyedVectors.load(str(kv_path), mmap="r")

    # ensure parent dir exists
    kv_path.parent.mkdir(parents=True, exist_ok=True)

    # extract SciBERT input embeddings
    tok = AutoTokenizer.from_pretrained(model_name)
    mdl = AutoModel.from_pretrained(model_name).eval().to("cpu")
    with torch.no_grad():
        emb = mdl.get_input_embeddings().weight.detach().cpu().numpy()  # (vocab, dim)
    # tokens sorted by ID
    vocab_items = sorted(tok.get_vocab().items(), key=lambda x: x[1])
    tokens = [w for w, _ in vocab_items]

    kv = KeyedVectors(vector_size=emb.shape[1])
    kv.add_vectors(tokens, emb)
    kv.fill_norms()  # speed up WMD
    kv.save(str(kv_path))
    return kv

_scibert_tok2 = AutoTokenizer.from_pretrained(SCIBERT_NAME)

def tokenize_scibert(text: str) -> List[str]:
    # Use SciBERT's own tokenizer → tokens exist in KV
    return _scibert_tok2.tokenize(text)

# ---------- WMD via WmdSimilarity on SciBERT KV ----------
def wmd_similarity_wmdsim(pairs: List[Tuple[int,str,str]], kv: KeyedVectors) -> float:
    if not pairs: return float("nan")
    sims = []
    for _, a, b in pairs:
        ta = tokenize_scibert(a)
        tb = tokenize_scibert(b)
        # Build a tiny index with the reference doc (tb)
        index = WmdSimilarity([tb], kv, num_best=1)
        res = index[ta]  # list of (doc_id, distance)
        if not res:
            dist = float("inf")
        else:
            _, dist = res[0]
        if math.isinf(dist) or math.isnan(dist):
            dist = 2.0  # treat invalid as large distance
        sim = 1.0 - dist
        sims.append(max(0.0, min(1.0, sim)) if CAP_WMD_TO_01 else sim)
    return float(np.mean(sims)) if sims else float("nan")

# ---------- Matrix & plotting ----------
def to_matrix(keys: List[Tuple[str,int,int,str]],
              scores: Dict[Tuple[Tuple[str,int,int,str], Tuple[str,int,int,str]], float]) -> np.ndarray:
    M = np.full((len(keys), len(keys)), np.nan, dtype=float)
    for i, k1 in enumerate(keys):
        for j, k2 in enumerate(keys):
            M[i, j] = scores.get((k1, k2), float("nan"))
    return M

def plot_heatmap(M: np.ndarray, keys: List[Tuple[str,int,int,str]], title: str, out_png: Path):
    labels = [f"{m}\nd{d}b{b}" for (m, d, b, _e) in keys]
    fig, ax = plt.subplots(figsize=(max(8, len(keys)*0.9), max(6, len(keys)*0.7)))
    im = ax.imshow(M, aspect="auto")
    ax.set_xticks(range(len(keys))); ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks(range(len(keys))); ax.set_yticklabels(labels)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.ax.set_ylabel("score", rotation=90)
    ax.set_title(title)
    fig.tight_layout(); fig.savefig(out_png, dpi=200); plt.close(fig)

def main():
    reports_root = Path(REPORTS_ROOT)
    out = Path(OUT_DIR); out.mkdir(parents=True, exist_ok=True)

    print(f"Scanning: {reports_root}")
    groups = load_reports(reports_root)
    if not groups:
        raise SystemExit("No reports found after filtering. Check REPORTS_ROOT / ENGINE_WHITELIST / EXCLUDE_KEYWORDS.")

    # Assemble desired order: model → depth → breadth
    keys: List[Tuple[str,int,int,str]] = []
    for m in MODELS:
        mk = m.lower()
        for d in DEPTHS:
            for b in BREADTHS:
                found = [k for k in groups.keys() if k[0] == mk and k[1] == d and k[2] == b]
                if not found:
                    continue
                # prefer whitelisted engine if multiple exist
                found.sort(key=lambda x: (0 if (not ENGINE_WHITELIST or x[3] in ENGINE_WHITELIST) else 1))
                keys.append(found[0])

    if not keys:
        raise SystemExit("No matching (model,depth,breadth) groups found. Check MODELS/DEPTHS/BREADTHS and filenames.")

    # Strict 49×49 enforcement
    if STRICT_ENFORCE_SAME_INDICES:
        ref_idx = require_same_index_set(groups, keys)
        print(f"[strict] Using reference {len(ref_idx)} indices.")
    else:
        # fall back to intersection (not recommended for paper parity)
        ref_idx = None

    print("Loading/Building SciBERT KeyedVectors for WMD …")
    kv = build_or_load_scibert_kv(SCIBERT_KV_PATH, SCIBERT_NAME)

    print("Computing pairwise …")
    rouge_scores: Dict[Tuple[Tuple[str,int,int,str], Tuple[str,int,int,str]], float] = {}
    bert_scores:  Dict[Tuple[Tuple[str,int,int,str], Tuple[str,int,int,str]], float] = {}
    wmd_scores:   Dict[Tuple[Tuple[str,int,int,str], Tuple[str,int,int,str]], float] = {}

    for k1 in keys:
        for k2 in keys:
            if STRICT_ENFORCE_SAME_INDICES:
                pairs = [(i, groups[k1][i], groups[k2][i]) for i in ref_idx]
            else:
                inter = sorted(set(groups[k1]) & set(groups[k2]))
                pairs = [(i, groups[k1][i], groups[k2][i]) for i in inter]

            rouge_scores[(k1, k2)] = rougeL_f1(pairs)
            bert_scores[(k1, k2)]  = bertscore_f1(pairs)
            wmd_scores[(k1, k2)]   = wmd_similarity_wmdsim(pairs, kv)

    # Matrices + CSV
    R = to_matrix(keys, rouge_scores)
    B = to_matrix(keys, bert_scores)
    W = to_matrix(keys, wmd_scores)

    pd.DataFrame(R, index=keys, columns=keys).to_csv(out / "rougeL_matrix.csv")
    pd.DataFrame(B, index=keys, columns=keys).to_csv(out / "bertscore_matrix.csv")
    pd.DataFrame(W, index=keys, columns=keys).to_csv(out / "wmd_matrix.csv")

    # Heatmaps
    plot_heatmap(R, keys, "ROUGE-L F1 (higher = more similar)", out / "rougeL_heatmap.png")
    plot_heatmap(B, keys, f"BERTScore F1 ({SCIBERT_NAME})", out / "bertscore_heatmap.png")
    plot_heatmap(W, keys, "1 − WMD (higher = more similar)", out / "wmd_heatmap.png")

    print(f"Done → {out.resolve()}")

if __name__ == "__main__":
    main()
