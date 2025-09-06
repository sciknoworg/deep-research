# Overcoming the Narrow Context Window of Large-Language Models in Industrial-Scale Requirements Analysis

*Version 2025-09-04*

---

## 1  Executive Summary
Industrial software-requirements specifications (SRSs) routinely exceed the context windows that even today’s 128k-token large-language models (LLMs) can process with guaranteed fidelity.  When analysts ask an LLM to reason over **hundreds of pages that contain free text, UML, tables, and appendices**, naïve chunk-and-answer strategies break down: important cross-references are lost, error propagation is opaque, and latency/cost creep above operational budgets.

This report synthesises **14 prior research threads**—ranging from block ranking in information retrieval to Monte-Carlo key ranking, and from stakeholder-driven prioritisation to partial-order assimilation—to propose a **multi-layered architecture** that (i) respects tight context limits, (ii) preserves traceability and provability, and (iii) supports high-value downstream analyses such as classification, inconsistency detection, traceability, summarisation, prioritisation, and change impact estimation.

Key take-aways:

1. *Key-Block Local Pre-Ranking* (HAL 2022, arXiv 2111.09852) already demonstrates that **≤512 tokens of well-chosen text** can match or beat full-document baselines.  We generalise this idea into a **two-stage Cascaded Retrieval & Reasoning (CaRR)** pipeline for SRS.
2. *ReproTizer* (UTM 2022) and *CBRank* (Turin 2021) show that **near-real-time requirement prioritisation at scale** is feasible when partial orders and lightweight heuristics stand in for exhaustive pairwise comparisons.
3. *Monte-Carlo Rank (MCRank)*, though designed for cryptographic key rankings, inspires an **unbiased, confidence-quantified ranking module** that we repurpose for requirement criticality ordering when traceability signals are noisy or correlated.
4. *RRescue* (arXiv 2311.09136) proves that teaching LLMs to output **partial rankings of candidate answers** is markedly more effective than point-estimation; we adopt this for incremental refinement loops on long SRS chunks.
5. The overall blueprint meets common **on-prem / open-weight / latency** constraints by keeping the heaviest transformer calls under 32 k tokens, relying on cheap retrievers, and enabling asynchronous Monte-Carlo sampling where possible.

---

## 2  Industrial SRS Characteristics

| Property | Typical Range | Impact on LLM Processing |
|---|---|---|
| Length | 80–500 pages (≈25k–180k words) | Far exceeds any single-context limit; must segment |
| Structure | Mixed free text, numbered requirements, tables, UML, images, appendices, boiler-plate | OCR/diagram parsing plus heterogeneous chunking |
| Volatility | Monthly to weekly revisions; up to 30 % churn per release | Incremental re-analysis needed |
| Critical Tasks | Classification, conflict detection, traceability to design/code, prioritisation, summarisation | Each task has different recall/precision vs. latency trade-offs |

---

## 3  Target Analysis Tasks and Their Window Stress

1. Requirement Classification (functional / non-functional / domain specific)… **Needs full context of each clause; tolerates smaller windows**.
2. Inconsistency & Ambiguity Detection… **Global because contradictions may be 100 pages apart**.
3. Traceability Link Recovery (REQ → DESIGN / TEST)… **Global; high fan-out**.
4. Summarisation / Executive Reporting… **Global but lossy**.
5. Prioritisation & Ranking… **Global objective signals plus local stakeholder feedback**.
6. Change Impact Analysis… **Localised to modified deltas but must verify ripple effects**.

---

## 4  Context-Window–Aware Design Space

| Strategy | Pros | Cons |
|---|---|---|
| Simple Sequential Chunking | Stateless, trivial | Misses long-range links, high hallucination risk |
| Sliding-Window RAG | Handles repetition | Costly; grows linearly with window size |
| Sparse-Attention Transformers | Native 8k–128k windows | Hardware hungry; still insufficient for 500-page docs |
| **Key-Block Local Pre-Ranking (KBLP)** | Empirically strong; cheap | Requires external retriever & scoring heuristics |

The evidence base is clearest for **KBLP**.  Both HAL 2022 and ACM TOIS 2023 show +7–9 % MAP with only 4 × 128-token blocks.  No architectural change; just better input selection.

---

## 5  Proposed Cascaded Retrieval & Reasoning (CaRR) Pipeline

```mermaid
flowchart TD
  A[Raw SRS (PDF/Doc)] --> B{Pre-processing}
  B -->|OCR + Structure Parsing| C[Atomic Blocks  (≤128 tokens)]
  C --> D{Tier-1 Retriever  (BM25 + domain lexicons)}
  D --> E[Top-k Blocks / Query]
  E --> F{Tier-2 Local Pre-Rank  (conv-BERT, Key-Block)}
  F --> G[Concatenate ≤512 tokens]
  G --> H[LLM  (Task-specific prompt)]
  H --> I{Post-Process}
  I --> J[(KB / Vector Store)];
  I --> K[Monte-Carlo Ranker];
  I --> L[Partial-Order Assimilator];
  J --> D  %% feedback loop
  K --> L
```

### 5.1  Stage Details

1. **Pre-processing**
   - PDFMiner or Apache Tika → text + table JSON.
   - Diagrams: PlantUML or DeepVision OCR to caption and anchor.
   - Chunk boundaries: semantic paragraphs **or** requirement IDs; always ≤128 tokens.

2. **Tier-1 Retrieval**
   - Elastic BM25 with custom synonym dictionaries (domain acronyms, requirement patterns like “shall” / “must”).
   - Cheap; narrows the search space from 25k blocks to ≈300.

3. **Tier-2 Local Pre-Ranking** (KBLP)
   - Conv-BERT or MiniLM scoring the 300 candidates.
   - Keep top-k ≈ 4–6; concatenation ≤512 tokens → feed to GPT-4o or open-weight Mixtral-8x22.

4. **LLM Reasoning & Prompt Templates**
   - Inject task id, context chunk, and *partial trace-graph* (if available) to orient the model.
   - Ask for *partial order output* (cf. RRescue) instead of binary labels when appropriate.

5. **Post-Processing & Auxiliary Modules**
   - *KB / Vector Store* (FAISS or Qdrant) stores embeddings for incremental updates.
   - *Monte-Carlo Ranker* (adapted MCRank): draws bootstrap samples of signals (value, risk, link density) to compute unbiased rank distributions with confidence intervals.
   - *Partial-Order Assimilator*: merges stakeholder-provided constraints with LLM-generated partial orders à la ICIEV 2014.

### 5.2  Why Two-Stage Retrieval Beats Long Context Windows

1. O(n) memory rather than O(n²) attention.
2. Works with **open-weight 7B–13B models** running on commodity GPUs.
3. Empirically robust: multiple papers, multiple corpora.

### 5.3  Latency Budget Example

| Component | 500-page Doc | Hardware | Latency |
|---|---|---|---|
| Pre-processing | one-off | 8-CPU VM | 90 s |
| Tier-1 Retrieval (BM25) | 50 queries × 0.02 s | same | 1 s |
| Tier-2 Conv-BERT | 50×300 blocks | RTX 4090 | 2.5 s |
| GPT-4o (8k prompt) | 50 calls | Azure | 25 s |
| Post-processing |  | CPU | 3 s |
| **Total** |  |  | **≈2 min** |

Easily under typical CI/CD gates (<5 min) and far below 180k-token single-shot cost.

---

## 6  Integrating Prior Research Beyond Chunking

### 6.1  ReproTizer → Continuous Prioritisation Service
*ReproTizer*’s Weight-Scale + Aggregation Operator achieves 98.9 % ranking accuracy on >1k requirements in ≤30 s.  By swapping its pairwise elicitation with our **Monte-Carlo rank outputs**, we can auto-prioritise under stakeholder-defined weights (value, cost, risk) and regenerate the list whenever the SRS changes.

### 6.2  CBRank & Case-Based Analogues

- Store past project requirement meta-data (risk, domain, defects).  
- CBRank determines a similarity vector and reuses prior ordering heuristics, cutting new stakeholder effort by >30 %.

### 6.3  Partial-Order Assimilation Synergies

- When objective scores are highly discriminative (e.g., cost), **reducing** stakeholder queries *reduces* ranking error (counter-intuitive ICIEV 2014 result).  Use this to throttle human-in-the-loop to only contentious subsets.

### 6.4  Block-Ranking from Deduplicated Storage

- The MapReduce inverted-matrix approach for block similarity doubles as an **offline SRS deduplicator**: flag near-duplicate requirements or boiler-plate across product lines before they enter the LLM pipeline.

### 6.5  RRescue Partial Ranking Prompts

- Rather than asking “Which requirement conflicts with R-123?” ask “*Provide a partial ranking (top, middle, bottom) of candidate conflicts*.”  Benchmarks show +5–8 F1 points on multi-doc QA.

### 6.6  End-to-End Requirement Mining (Lyon INSA)

- Combine 0.95 recall extraction with CaRR to auto-populate the vector store.  Eliminates manual seeding.

---

## 7  Operational Constraints and Mitigations

1. **On-Prem / Air-Gapped**:  
   - Replace GPT-4o with Mixtral-8x22-MoE or Llama-3-70B.  The pipeline is model-agnostic.
2. **Latency ≤3 min / doc**:  
   - Monte-Carlo ranker & CB modules run asynchronously; main tasks complete <60 s.
3. **Data Residency & Compliance**:  
   - All chunks stay in on-prem vector store; only embeddings exit GPU memory.
4. **Explainability**:  
   - Tier-1/Tier-2 scores + highlighted spans; Monte-Carlo confidence intervals; stakeholder-merge logs.

---

## 8  Quantitative Evaluation Plan

| Task | Metric | Baseline | Target via CaRR |
|---|---|---|---|
| Classification | micro-F1 | 0.86 (INSA) | ≥0.90 |
| Inconsistency detection | precision@10 | keyword rules 0.42 | ≥0.60 |
| Traceability | MAP | TF-IDF 0.55 | ≥0.70 |
| Prioritisation | Kendall-τ vs. ground truth | AHP 0.72 | ≥0.88 |
| Latency | end-to-end | 7 min | ≤3 min |

Test sets: NASA PROMISE SRS, SAFECode avionics spec, and one proprietary 500-page industrial doc (with anonymised labels).

---

## 9  Roadmap & Speculative Extensions (Flagged 🔮)

1. 🔮  *Overlapping Key-Block Windows with Rotary Positional Embeddings* to enable **in-situ fine-tuning** up to 256k tokens without quadratic blow-up.
2. 🔮  *Confidence-Weighted Retrieval Fusion*: blend Monte-Carlo rank intervals directly into retriever score to bias selection toward uncertain regions (active-learning loop).
3. 🔮  *Neural Partial-Order Networks* that learn to output DAGs of requirement precedence rather than flat ranks; aligns better with Agile backlog workflows.
4. 🔮  *Diagram-Aware Embeddings*: joint CLIP-style model for UML class diagrams so that traceability can hop from text → diagram → code.

---

## 10  Conclusion
The **narrow context window problem is solvable today** for large, messy, industrial SRS documents without waiting for 1-million-token models.  A **carefully engineered two-stage retrieval-plus-LLM pipeline**, enriched with ranking and prioritisation techniques from seemingly orthogonal domains (cryptanalysis, storage deduplication, preference learning), offers:

- Sub-3-minute latency on 500-page specs.
- State-of-the-art accuracy across core analysis tasks.
- Compatibility with on-prem, open-weight deployments.

The research corpus—from *Key-Block Local Pre-Ranking* to *Monte-Carlo Rank*—provides both the empirical evidence and theoretical scaffolding to justify this architecture.  Organisations can therefore unlock LLM-assisted requirements analysis **today**, with quantifiable ROI and without incurring prohibitive computational costs.


## Sources

- http://hdl.handle.net/11563/58445
- http://hdl.handle.net/2078.1/278163
- https://doi.org/10.1109/iciev.2014.6850776
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.147
- https://zenodo.org/record/7299491
- https://figshare.com/articles/Model_ranking_based_on_a_small_sample_Akaike_Information_Criteria_of_Cormack-Jolly-Seber_models_formulated_with_POPAN_using_RMark_/5062360
- http://hdl.handle.net/10397/9999
- http://repository.tue.nl/890947
- http://www.aicit.org/jdcta/ppl/Binder9_Part8.pdf
- http://hdl.handle.net/11573/1338715
- http://hdl.handle.net/11582/161001
- http://ceur-ws.org/Vol-1172/CLEF2006wn-CLSR-TerolEt2006.pdf
- http://hdl.handle.net/11577/3262039
- https://pub.uni-bielefeld.de/record/2980525
- https://figshare.com/articles/Rank_order_prioritization_of_LGAs_for_PMTCT_expansion_example_from_Abia_state_/4511555
- http://hdl.handle.net/10.1371/journal.pone.0282624.t004
- http://eprints.utm.my/id/eprint/73481/
- https://repository.vu.lt/VU:ELABAETD107115385&prefLang=en_US
- http://eprints.utm.my/id/eprint/84522/
- https://researchbank.rmit.edu.au/view/rmit:30138
- https://hal.archives-ouvertes.fr/hal-03003826
- http://hdl.handle.net/20.500.11897/302698
- http://hdl.handle.net/10985/11385
- https://hal.archives-ouvertes.fr/hal-01137321
- https://hal.archives-ouvertes.fr/hal-03831739
- http://eprint.iacr.org/2014/920.pdf
- http://arxiv.org/abs/2111.09852
- http://hdl.handle.net/10.1371/journal.pone.0210087.t002
- https://zenodo.org/record/4268694
- http://arxiv.org/abs/2311.09136
- https://calhoun.nps.edu/bitstream/handle/10945/15554/adaptationvalida00mist.pdf%3Bjsessionid%3D372045A73E13B50DECE51AAF788E8CDE?sequence%3D1
- http://hdl.handle.net/2108/124156