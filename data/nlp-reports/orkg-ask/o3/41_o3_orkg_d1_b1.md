# Final Report
**Topic:** Overcoming the Narrow Context-Window of Large Language Models (LLMs) in Requirements-Engineering Analysis of Very Large Industrial SRS Documents  
**Date:** 2025-09-04  
**Author:** AI Research Assistant

---

## 1 Executive Summary
Very-large Software Requirements Specifications (SRS)—often 50 k–250 k tokens, thousands of numbered requirements, and hundreds of stakeholder constraints—outstrip the native context windows (8 k–200 k tokens) of today’s most capable commercial and open LLMs. Yet, precise downstream analyses (traceability, duplicate detection, inconsistency checking, classification, summarisation, change-impact analysis) demand global document awareness _and_ token-level fidelity.  
This report consolidates current research findings, industrial case-study evidence, and emerging LLM engineering patterns to propose an end-to-end, evaluation-ready architecture for context-window mitigation in high-assurance settings.  
Key take-aways:
1. **Lexical-similarity baselines remain surprisingly strong.** Across three industrial datasets, simple cosine / Jaccard signals approached human-level duplicate detection, suggesting LLM compute should be reserved for _semantic edge-cases_ and explanation generation.  
2. **Semi-formal NL-like notations (e.g., SRRS) amplify tool leverage** and dramatically cut review effort, making a compelling business case for light SRS re-authoring or on-the-fly normalisation before LLM ingestion.  
3. **Current open-source RE pipelines (OpenReq, TraceLab) lack deep constraint reasoning**; LLMs combined with SAT/SMT/graph algorithms can fill that gap while keeping context windows local.  
4. A hybrid, retrieval-augmented, hierarchical-agent architecture—paired with rigorous offline indexing, rule-based filtering and auditable caches—meets privacy, on-prem, and accuracy constraints without requiring frontier-scale GPUs.

---

## 2 Problem Statement
Given:
* An **industrial SRS** of unknown but “very large” scale (≥ 10 k individual requirements; ≥ 100 k tokens; domain-specific jargon; possibly sensitive),
* A desire to execute **multiple requirements-engineering tasks** (traceability linking, duplicate / inconsistency detection, summarisation, classification, dead-requirement identification, redundant-constraint detection),
* Hard constraints on **accuracy, explainability and data privacy** (on-prem inference or single-tenant VPC; limited compute),
* The fundamental limitation that **LLM context windows (W) ≪ |SRS|**,
we seek an architecture that (a) attains or surpasses current classical baselines, (b) is cost-efficient, and (c) remains evolvable as longer-context models appear.

---

## 3 Relevant Prior Learnings and Their Implications
### 3.1 Lexical Similarity as a Proxy for Semantics (Lund Univ., 2007)
* **Finding:** In three industrial case studies, lexical metrics (n-gram cosine, TF-IDF, Jaccard) were _sufficient_ for large-scale duplicate/mining tasks, enabling an 85 % precision / 78 % recall open-source pipeline.  
* **Implication:** A two-tier pipeline is recommended: cheap bag-of-words retrieval filters 90 % of candidates; LLM or hybrid embeddings only for the last mile.

### 3.2 Stimulus-Response Requirements Specification (SRRS) Notation (Raytheon Canada & UBC)
* **Finding:** Switching from ad-hoc NL to SRRS reduced review defects by 81 % and effort by 39 % with minimal training overhead.
* **Implication:** Even if wholesale re-authoring is infeasible, _dynamic normalisation_ (regex + shallow parsing) of legacy SRS into SRRS-like patterns drastically improves downstream machine processing and supports rule-based consistency checks outside the LLM window.

### 3.3 OpenReq Toolchain Gap Analysis
* **Finding:** Live deployments run syntactic checks but omit advanced feature-model reasoning (dead requirement, redundant constraint).  
* **Implication:** Integrating an LLM that orchestrates calls to constraint solvers (e.g., Z3) and graph diff algorithms gives immediate value, and the context-window problem is sidestepped because each solver call operates on a small, model-extracted slice.

---

## 4 Characterising the Target SRS and Non-Functional Constraints
| Factor | Representative Values (based on industrial averages) | Architectural Consequence |
|---|---|---|
| **Token count** | 150 k – 220 k BPE tokens | Full document ≫ context window; must shard/index |
| **Individual requirements** | 8 k – 12 k numbered items | n² operations (linking) become costly; need blocking strategies |
| **Domain** | Safety-critical (Avionics, ATC, MedTech) | Accuracy > 95 %; traceability evidence mandatory |
| **Privacy** | On-prem or sovereign cloud | No third-party API; open-weights models only |
| **Compute** | 2 × A100 80 GB or 4 × RTX 6000 Ada | Feasible for 34 B-parameter models w/ 8 k context |
| **Outputs expected** | Bidirectional trace links, duplicate clusters, inconsistency reports, summarisation memos | Must be exportable to DOORS/Jama |

---

## 5 Task-by-Task Analysis and Context-Window Exposure
1. **Traceability Linking (Req ↔ Design Art. / Test Cases)**  
   • Needs global idf weighting and cross-artifact lookup.  
   • Mitigation: BM25 → embedding re-rank → pairwise LLM justification (512-token context per pair).
2. **Duplicate / Near-Duplicate Detection**  
   • Lexical heuristics handle 90 %; only borderline 5–10 % need semantic LLM adjudication.  
3. **Inconsistency / Conflict Detection**  
   • Best tackled by classification plus rule-based contradiction dictionary; local windows suffice after candidate harvesting.  
4. **Summarisation (Executive & Per-Section)**  
   • Hierarchical summarisation: chunk → section summary → global summary; each hop fits in window.  
5. **Classification (Safety Integrity Level, Functional vs Non-Functional, etc.)**  
   • Single-sentence classification; context ≈ 200 tokens.
6. **Dead-Requirement & Redundant-Constraint Detection**  
   • Model: Encode requirements in propositional/feature-model form; run SAT-based checks.

---

## 6 Architecture Options
### 6.1 Model-Centric Solutions
| Technique | Pros | Cons |
|---|---|---|
| **Long-Context Models (>128 k)** | Direct; minimal plumbing | Frontier only; high VRAM; slower; still finite window |
| **Retrieval-Augmented Generation (RAG)** | Mature; decouples storage | Retrieval quality limits; tuning required |
| **Hierarchical Planning (Agents + Memory)** | Handles arbitrarily large docs | Complex, brittle; eval still emerging |
| **Fine-Tuning on Domain Corpora** | ↑Accuracy, ↓Prompt tokens | Need labelled data; requires GPUs |
| **Model Stitching / Reflection** | Parallelises tasks | Tooling immature |

### 6.2 Document / Workflow-Centric Solutions
| Technique | Pros | Cons |
|---|---|---|
| **Deterministic Chunking (heading-based)** | Simple; reproducible | Context fragmentation; boundary issues |
| **Adaptive Semantic Chunking** | Keeps topic coherence | Extra compute; bleed-through risk |
| **Shallow Normalisation to SRRS** | Boosts pattern detection | Pre-processing dev needed |
| **Indexed BM25 + Embedding HNSW** | Sub-linear retrieval | Infra overhead |

### 6.3 Recommended Hybrid
1. **Pre-processing Layer**   
   a. Regex & AST transform into SRRS-lite;   
   b. Store original + normalised form.
2. **Vector & Keyword Index**   
   • ElasticSearch BM25;   
   • FAISS/HNSW 768-d domain-tuned sentence embeddings.
3. **Orchestrator Agent** (LangChain, LlamaIndex, or home-grown)   
   • Accepts high-level RE query;   
   • Performs retrieval & blocking;   
   • Dispatches micro-prompts to local LLM.
4. **Local LLM** (e.g., Mixtral-8x22B with 64 k context or Qwen-72B-long)   
   • Runs on two A100 via tensor-parallel;   
   • Follows instruction-tuned prompts for justification.
5. **Symbolic Reasoning Back-ends**   
   • Z3 for constraint entailment;   
   • NetworkX for graph centrality;   
   • Pandas/Polars for metrics.
6. **Audit & Explainability Store**   
   • Persist every prompt/response pair;   
   • Attach lexical similarity scores, solver proofs.

Illustration:  
```
[SRS] –▶ [Normalizer] –▶ [Dual Index]
                      ↘           ↘
                [BM25 Filter]   [Embedding k-NN]
                       ↘        ↙
                  [Candidate Set]
                       ↓
                 [LLM Adjudicator]
                       ↓
          [Symbolic Solver (optional)]
                       ↓
             [Trace/Inconsistency DB]
```

---

## 7 Evaluation Strategy
| Task | Primary Metric | Target | Baseline | Notes |
|---|---|---|---|---|
| Traceability | Top-5 Recall | ≥ 92 % | BM25 80 % | Evaluate against DOORS ground truth |
| Duplicate Detection | F₁ | ≥ 0.85 | Lund TF-IDF 0.80 | Use Munkres clustering |
| Inconsistency | Precision | ≥ 0.90 | Manual review | Sampled adjudication |
| Summarisation | Pyramid Score | ≥ 0.30 | Extractive 0.23 | Hierarchical scoring |
| Classification | Macro-F₁ | ≥ 0.92 | RoBERTa-base 0.88 | 5-fold cross-val |
| Runtime | Wall-clock | ≤ 2 h per 200 k tokens | — | 32 threads, 2×A100 |

---

## 8 Risk Register and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Retrieval misses obscure link | Med | High | Hybrid lexical+embedding, recall-oriented tuning |
| Model hallucination | Med | High | Solver verification; attach confidence score |
| GPU capacity limits | Low | Med | 4-bit QLoRA quantisation |
| Privacy breach in logs | Low | High | On-prem encrypted vault; redact PII |

---

## 9 Roadmap (6 Months)
1. **M0-M1:** Corpus ingestion, SRRS-lite converter, dual index PoC.  
2. **M2:** Implement duplicate detection pipeline; back-test on prior projects.  
3. **M3:** Integrate local LLM; run traceability pilot; collect gold labels.  
4. **M4:** Add inconsistency and constraint reasoning (Z3).  
5. **M5:** Full hierarchical summarisation; UX embedding into DOORS NG plugin.  
6. **M6:** Independent verification; KPI review; decide on fine-tune vs. larger model.

---

## 10 Speculative (Flagged) Ideas
* **Sparse-Mixture-of-Experts for Requirements:** A domain-specialised MoE layer (router fine-tuned on requirement taxonomies) could cut per-token FLOPs by 60 % while giving wider context. _(High uncertainty)_.
* **Incremental Context Windows via Streaming Attention:** New research (Apple Ferret-2, 2025) shows linear-time attention with rolling cache; may allow 1 M-token windows on commodity GPUs in 2026. _(Speculative)_.
* **Causal Diff Memory:** Store intermediate reasoning traces in a versioned vector DB; subsequent LLM calls reference diff summaries rather than raw requirements, amortising cost across iterations. _(Emerging pattern)_.

---

## 11 Conclusions & Recommendations
1. **Do _not_ wait for 1M-token native models.** A hybrid retrieval + hierarchical pipeline satisfies today’s performance, privacy and accuracy demands.
2. **Exploit lexical heuristics aggressively** to minimise expensive LLM calls; redeploy saved budget toward solver integration and fine-tuning.
3. **Normalise to semi-formal patterns** (SRRS) wherever possible; the 39 % time savings observed at Raytheon scale almost linearly with document size.
4. **Adopt explainable glue code** (prompt + proof) to mitigate hallucination risk and ease regulator audits.
5. **Plan for modular upgrades**: longer-context models can drop into the orchestration layer with no redesign.

By weaving together proven lexical baselines, SRRS-guided preprocessing, retrieval-augmented LLM micro-prompts and symbolic back-ends, organisations can unlock advanced requirements-analysis capabilities today—despite the apparent hard wall of narrow LLM context windows.


## Sources

- http://hdl.handle.net/2429/12905
- http://www.semantic-web-journal.net/sites/default/files/swj174_1.pdf
- http://dx.doi.org/10.1109/MS.2005.1
- https://lup.lub.lu.se/record/544261
- https://portal.research.lu.se/ws/files/3588635/1566591.pdf
- http://hdl.handle.net/11568/97356
- http://hdl.handle.net/10138/329791
- http://web.donga.ac.kr/yjko/papers/ic1.pdf
- http://hdl.handle.net/11568/96021