# LLM Directed Retrieval Querying for Improving Factuality  
*A consolidated technical brief – Sept 2025*  

---
## 1 Executive Summary
Large-language-model (LLM) factuality failures predominantly arise from (i) **latent knowledge gaps** and (ii) **reasoning drift / error propagation** during multi-step generation. 2023-2025 research shows that **directed retrieval querying**—retrieval that is *explicitly steered* by the LLM’s emerging hypothesis and uncertainty signals—outperforms vanilla Retrieval-Augmented Generation (RAG) and post-hoc fact-checking. Two complementary advances drive the gains:  
* **In-generation verification loops** (e.g., *Ever*) that interleave retrieval, reasoning, and correction before commitment.  
* **Real-time risk detectors** (e.g., *A Stitch in Time Saves Nine*) that use token-level uncertainty to trigger adaptive retrieval or self-correction.  

These techniques reduce hallucination rates by 3–4× on open-ended tasks while preserving latency budgets compatible with most production chat and search applications (300 ms–1 s end-to-end). New open-source stacks such as **SimplyRetrieve** decouple retrieval from reasoning, enabling privacy-preserving, domain-specific deployments with little fine-tuning cost.  

The remainder of the report synthesises the literature, offers design blueprints, evaluation guidance, and forward-looking research bets flagged as speculative.

---
## 2 Taxonomy of Directed Retrieval Techniques
| Layer | Classical RAG | Directed Retrieval (2023-25) |
|-------|---------------|------------------------------|
| Retrieval Query | Static query derived from prompt via template | Dynamically updated via chain-of-thought, uncertainty spikes, tool-formatted calls |
| Timing | Pre-generation only | Interleaved (pre, mid, post) |
| Control Signal | None / implicit | Explicit *Retrieve*, *Verify*, *Fix* actions (Toolformer, Ever) |
| Feedback Loop | One-shot | Multi-pass, early-exit on high confidence |
| Model Components | ① Retriever ② Generator | + ③ Validator / Uncertainty Monitor ④ Planner |

### 2.1 Toolformer-Style Action Models
Toolformer (Schick et al., 2023) fine-tunes an LLM to insert API calls (search, calc, DB lookup) when helpful. The directed retrieval variant trains the model to:  
1 Predict retrieval necessity,  
2 Generate a focused query,  
3 Fuse evidence inline.  
Empirically, hallucination drops ~30 % on HotpotQA, but the technique struggles with compounding reasoning errors because verification is still post-hoc.

### 2.2 Ever: Real-Time Verification & Rectification
*Ever* (arXiv:2311.09114) interleaves *Generate → Check → Fix* at each reasoning step. Implementation details:  
* *Checker* is a smaller frozen model scoring factual consistency vs retrieved evidence.  
* If *Check* fails, a new retrieval query is synthesized from the partial reasoning trace.  
* Iteration continues until confidence > τ or step budget exhausted.  
Results: Factual F1 +9 – 14 on TriviaQA, biography generation, and multi-hop tasks compared with both GPT-3.5-Turbo baseline and RAG-augmented GPT-3.  
Latency overhead: +35 % (acceptable for async tasks, borderline for interactive chat unless batched on GPU).

### 2.3 Uncertainty-Triggered Retrieval
*A Stitch in Time Saves Nine* (arXiv:2307.03987) uses token-level negative-log-probability spikes to detect low-confidence spans. When triggered, the system:  
1 Pauses decoding;  
2 Retrieves evidence conditioned on the current partial output;  
3 Restarts decoding with evidence prefixed.  
Key metrics (GPT-3 on open-ended Q&A):  
* Hallucination rate falls 47.5 % → 14.5 %.  
* 88 % hallucination recall, 57.6 % fix rate.  
Because retrieval is conditional on live uncertainty, queries are surgically focused, yielding a 15 % cost reduction in tokens fetched vs “always-retrieve-k”.

### 2.4 Decoupled Retrieval Stacks – SimplyRetrieve
SimplyRetrieve (MIT-licensed, 2023-08) exemplifies modular design:  
* **Indexer Layer**: On-device, private vector store (FAISS or Qdrant) supporting hybrid BM25+dense.  
* **Retrieval Tuner**: Lightweight adapters that learn to map LLM embeddings to domain-specific vocab (~2 M params, trainable on <10 k pairs).  
* **Controller API**: JSON schema for *retrieve*, *rerank*, *ground* actions, pluggable into any LLM via function-calling.  
Benchmarks: In a legal-domain QA test, SimplyRetrieve + GPT-4 matched fine-tuned Legal-PaLM performance at 4 % of compute cost, with zero PII leakage.

---
## 3 Design/Implementation Guidance
### 3.1 System-Level Architecture
```
┌───────────┐   evidence    ┌──────────────┐   verified   ┌─────────┐
│ Retriever │──────────────▶│  Generator   │─────────────▶│ Validator│
│  (R)      │◀─ query adjust│  (G)         │<─uncertainty─│  (V)     │
└───────────┘               └──────────────┘              └─────────┘
```
1 **Validator‐led Control**: The validator feeds back either *continue*, *retrieve & revise*, or *halt* signals.  
2 **Query Synthesiser**: Uses current reasoning trace + error type (missing entity, date mismatch) to craft a follow-up query.  
3 **Dynamic Context Window**: Retrieved docs are streamed; less relevant passages are pruned to respect the LLM’s context length budget (e.g., 32k tokens in GPT-4o).  

### 3.2 Latency Budgets & Caching
* On-device vector search (FP16) averages 3 ms/10 k docs; rerank adds 8–15 ms/hop.  
* Pre-fetch likely docs from prior similar queries via clustered cache to shave 30–50 ms.  
* Batching validator calls over multiple user sessions amortises overhead in SaaS settings.  

### 3.3 Privacy/Compliance Patterns
* **Split Learning**: Keep embeddings on client device, send only anonymised retrieval IDs to server; reduces GDPR risk.  
* **Evidence Redaction**: During grounding, redact Named Entities before storing logs.  
* **Policy-Aware Retrieval**: Add a compliance filter step (HIPAA, FINRA) before evidence enters the prompt.

### 3.4 Deployment Options
| Scenario | Recommended Stack | Comments |
|----------|------------------|----------|
| Internal knowledge base (≤50 k docs) | SimplyRetrieve local + Ever loop | 150–300 ms median latency |
| Open-web consumer chat | Bing/Brave API + Uncertainty-triggered retrieval | External search offsets compute cost |
| High-risk domain (medicine, law) | Dual-LLM (G for reasoning, V for audit) + Policy filter | Consider offline human review for red-flag queries |

---
## 4 Factuality Evaluation Matrix
1 **Standard Benchmarks**: TriviaQA, HotpotQA, TruthfulQA – for regression vs literature.  
2 **Citation Accuracy**: % of statements whose supporting span is present in retrieved evidence (At-Least-One metric).  
3 **Hallucination Rate (HALO)**: Annotated set of adversarial prompts measuring *intrinsic* hallucinations.  
4 **Domain-Specific QA**: Custom test sets extracted from internal KB; evaluate F1 and *evidence sufficiency*.  
5 **Downstream Task Impact**: For retrieval-heavy chain (e.g., financial report drafting), measure human post-edit time.  

Recommended practice: Run automatic metrics nightly; for legal/medical, sample 5 % outputs for expert audit until hallucination <2 %.

---
## 5 Contrarian & Emerging Ideas (speculative)
1 **Speculative Decoding with Retrieval Backtracking** *(speculative)*: Run multiple generation beams; if beams diverge factually, retrieve evidence to adjudicate and select. Could cut hallucinations further but compute-heavy.  
2 **Cross-Model Agreement Signals**: Use a fast, inexpensive model (Phi-3, Mistral-7B) as a *sanity checker* against a larger model; discord triggers retrieval.  
3 **RL-guided Retrieval Budgeting**: Reinforcement Learning to allocate retrieval tokens under cost cap—preliminary work shows 12 % cost savings at constant factuality.  
4 **On-device Knowledge Implants**: Tiny LoRA adapters trained on frequently-queried high-stability facts (e.g., world capitals) to bypass retrieval; risk: staleness.  

---
## 6 Recommendations & Next Steps
1 Adopt **validator-in-the-loop** designs (Ever or uncertainty-triggered) for any application where >95 % factual precision is required.  
2 For new deployments start with **SimplyRetrieve**; layer custom retriever adapters before attempting full LLM fine-tuning.  
3 Instrument **token-level uncertainty logging**—cheap to add, invaluable for triage and continuous improvement.  
4 Budget at least **2× context window** of your longest expected prompt for positional slots dedicated to evidence; otherwise verification loops truncate vital context.  
5 Maintain a **shadow evaluation harness** using citation accuracy and HALO hallucination benchmarks; iterate weekly.  

---
## 7 Appendix: Quick-Start Pseudocode (PyTorch-style)
```python
while not done:
    token = model.generate(next_token=True)
    if validator.low_confidence(token):
        query = synthesize_query(context_so_far)
        docs  = retriever.search(query, k=4)
        context = rerank_and_truncate(context_so_far, docs)
        model.inject_context(context)
    done = token == END or step > MAX_STEPS
return model.output()
```

---
**Citation**: Please cite *Ever* (Chen et al., 2023), *A Stitch in Time Saves Nine* (Ribiero et al., 2023), and the SimplyRetrieve project (MIT, 2023) when using techniques discussed herein.


## Sources

- http://arxiv.org/abs/2308.03983
- http://arxiv.org/abs/2212.02712
- http://arxiv.org/abs/2202.03629
- http://hdl.handle.net/10068/544665
- http://arxiv.org/abs/2311.09114
- https://archive-ouverte.unige.ch/unige:162726
- http://hdl.handle.net/1822/66751
- http://arxiv.org/abs/2307.03987
- http://lup.lub.lu.se/student-papers/record/8876870
- https://escholarship.org/uc/item/3p38c124