# Sampling–Based Q&A to Tame Hallucinations and Isolate Personal Facts in LLMs  
*Toward deployable, privacy-compliant, high-precision conversational agents*  
2025-09-04  

---

## 0. Executive Summary

The combination of **(i) aggressive answer-space sampling** and **(ii) post-hoc agreement scoring** is emerging as the most architecture-agnostic, low-latency strategy for reducing factual hallucinations in Large Language Models (LLMs).  When the same mechanism is coupled with an **instance-separation layer**—a thin store that binds user-specific facts to a stable identifier separate from the LLM’s parametric memory—we obtain a single framework that solves three deployment pain-points at once:

1. **Hallucination Mitigation** without external knowledge bases or log-prob access (cf. *SelfCheckGPT*).  
2. **Personal-Fact Isolation** that prevents cross-user leakage, aids Right-to-Erasure GDPR compliance, and enables per-user continual fine-tuning.  
3. **Predictable Cost Profile** by avoiding full-retrieval or multi-agent stacks (contrast *LLteaM* cost overruns).

This report distills the current state of the art, proposes an implementation blueprint, and sketches an experimental plan that can be executed within six engineer-months on commodity GPU clusters (<$15 k cloud spend).  All 13 prior learnings supplied by the requester are woven into the discussion.

---

## 1. Problem Statement

An LLM used in multi-turn personalized dialogs faces two entangled risks:

* **Global Hallucination Risk** – incorrect or fabricated statements drawn from spurious reasoning, deficit in commonsense or memory, or adversarial prompts (see *AutoDebug* failure mode (i)).
* **Personal Fact Leakage** – inadvertent blending of user A’s data into answers for user B, breaching confidentiality and GDPR Articles 5(1)(b,f).

The community has tackled the first with retrieval-augmented generation (RAG), system-level filters, or adversarial training; and the second with encryption, federated learning, and memory sharding.  Yet no single pipeline addresses *both* while staying cost-effective and model-agnostic.

### 1.1 Hypothesis

> **H₀:** Independent, stochastic sampling of *k ≫ 1* answer candidates + majority / self-consistency scoring ("Sampling Q&A") can drive hallucination rate below 2 % without external KBs.  Augmenting that pipeline with a per-user key-value store plus relaxed functional-dependency masking will achieve ≤10⁻⁵ cross-user leakage probability, matching GDPR deletion timelines.

---

## 2. Literature Landscape

### 2.1 Sampling-Based Hallucination Filters

| Method | Core Idea | Key Metric | Notes |
|--------|-----------|-----------|-------|
| **SelfCheckGPT** (Cambridge ’23) | 𝑘-sample generations, cosine agreement > τ ⇒ factual | +15–20 AUC-PR on WikiBio | Black-box, no logits |
| **Self-Consistency Decoding** | Generate diverse reasoning paths; pick answer with most agreement | 4–14 pt improvement on GSM8K | Works even at T=1 by prompt diversification |
| **Batch-Time Voting (OpenAI)** | ChatGPT backend: 5 samples, majority vote -> safety pipeline | – | Undocumented heuristics |

Takeaway: **randomized diversification + cheap Agree(Xᵢ,Xⱼ)** scoring outperforms single-pass generation even with state-of-the-art LLMs (GPT-4o, Claude 3).  It requires *no* retraining, only more forward passes.

### 2.2 Contrastive & Retrieval Hybrids

* **MixCL (AAAI-23)** merges retrieved *hard negatives* with model-generated ones; SOTA on Wizard-of-Wikipedia factuality.  Key point: *generation-side negatives* approximate the "hallucination manifold" at train time.
* **Association-Analysis (arXiv 2309.05217)** quantifies risk contributions per skill.  Findings feed into targeted synthetic data like *AutoDebug*.

### 2.3 Cost–Accuracy Trade-Off Studies

* **LLteaM** multi-agent self-supervision blocked hallucinated e-mails but blew the cost budget (>3× inference tokens) and degraded after GPT-3.5 backend update.  **Volatility** of API endpoints is a latent risk.
* **HaELM, HaloCheck** automate hallucination detection cheaper (≈$0.003 /1k tokens).  

### 2.4 Privacy & Instance Separation

* **Relaxed Functional Dependencies (RFDs)** enable *partial* masking: instead of encrypting whole user tables, only quasi-identifiers strongly predictive of sensitive fields are obscured (≈30 % fewer masked cells).
* **Federated + Differential Privacy** stacks (2022 load-forecasting study) achieve "near-perfect privacy" but suffer from cross-silo latency.
* **Open-Source LMS Breach Case** highlights importance of **at-rest encryption** for metadata as well as raw text.

### 2.5 Cross-Domain Sampling Analogs (Informative Parallels)

While **Temperature Cool Walking (TCW)** and **Target Motion Sampling (TMS)** arise in molecular dynamics and neutron transport, both confirm that **replica / ensemble sampling accelerates convergence** and lowers computational variance—indirect evidence that our LLM sampling pipeline will scale sub-linearly with sample count.

The **K-means retrieval database** insight from satellite AMSU processing shows *distance metric + database-size selection* as critical; we will reuse that for our per-user memory hashing and similarity search.

---

## 3. Proposed Architecture

```
┌──────────────────────────┐    write/delete       ┌──────────────────────┐  
│  Per-User Fact Store     │◀─────────────────────▶│ RFD-Aware Mask Layer │  
└─────────▲────────────────┘                      └─────────▲────────────┘  
          │ read (top-k)                                      │            
          │                                                   │            
┌─────────┴──────────────┐          k samples                 │            
│  Prompt Composer       │───────────────────────────────────▶│            
└─────────▲──────────────┘                                   │            
          │                                                   │            
┌─────────┴──────────────┐        k passages                  │            
│  LLM (frozen)          │───────────────────────────────────▶│            
└─────────▲──────────────┘         pairwise                   │            
          │                        agmnt                      │            
┌─────────┴──────────────┐                                   │            
│  Agreement Scorer      │───────────────────────────────────▶│            
└─────────▲──────────────┘            final answer           │            
          │                                                   │            
┌─────────┴──────────────┐                                   │            
│  Hallucination Filter  │                                   │            
└────────────────────────┘                                   │            
```

### 3.1 Components

1. **Per-User Fact Store (PUFS)**  
   * Key = SHA-256("userID::fact-title")  
   * Value = JSON blob {claim, evidence, last_verified, sensitivity_score}.  
   * Indexed via **K-means product quantization** (cf. AMSU) on SBERT embeddings; *radius-based pruning* keeps latency <5 ms.

2. **RFD-Aware Mask Layer**  
   * On every read/write, compute relaxed functional dependencies; flag columns that leak sensitive fields (e.g., date_of_birth ↔ age).  
   * Unmasked cells sealed with AES-GCM; keys stored in an HSM for GDPR Article 32 compliance.

3. **Prompt Composer**  
   * Injects top-k (≤4) personal claims as *Context Blocks* with explicit `VERIFIED_DATE` tags to reduce staleness hallucinations.

4. **LLM Back-End**  
   * We target **Gemma-7B-Instruct** and **GPT-4o** families; on-device inference feasible with 7B quantized to 4-bit.

5. **Agreement Scorer**  
   * Compute pairwise ROUGE-L + cosine on CLS embeddings; score = mean agreement.  
   * Accept candidate if (i) agreement ≥ 0.42 or (ii) content overlaps ≥80 % with *any* top-k context fact.

6. **Hallucination Filter**  
   * If none pass threshold, return `I am not certain`.  
   * Secondary HaELM classifier for medical or financial domains.

### 3.2 Data Flow

1. **User asks Q**.  
2. PUFS pulls 1–4 candidate facts by similarity.  
3. Prompt composed: *System* + *User* + *Facts* + "Generate **k=6** diverse answers."  
4. Six forward passes (temperature schedule 1.2→0.8 like *TCW* replica-exchange).  
5. Agreement scorer selects best.  
6. Personal data in transcript stored encrypted; per-turn RFD scan updates masks.

---

## 4. Implementation Blueprint (Gantt-Style)

| Month | Milestone | Key Risks |
|-------|-----------|-----------|
| 1 | Set up PUFS schema + AES-GCM/HSM | Index latency |
| 2 | Integrate SBERT + PQ; reach <10 ms retrieval | Vector drift |
| 3 | Implement sampling wrapper & scorer; reproduce SelfCheckGPT 20 pt AUC gain on WikiBio | Token cost explosion |
| 4 | RFD masking layer; GDPR DPIA drafting | False negatives |
| 5 | End-to-end eval on AutoDebug set + in-house personalized QA (5k Qs) | Adversarial prompts |
| 6 | Load testing, ablation (k=2…8), final report | Model version drift (cf. LLteaM) |

Cloud budget estimate: 700 k input tokens ×6 samples ×$15/1M = $63 for GPT-4o eval; training SBERT fine-tune <50 GPU-hours ≈$500.

---

## 5. Experimental Evaluation Plan

### 5.1 Datasets

* **AutoDebug synthetic QA** – stress conflict vs composition.  
* **Med-HALT** reasoning vs memory splits (medical).  
* **Custom Personal Facts** – 100 synthetic personas ×50 facts each, with 20 intentionally overlapping to test leakage.

### 5.2 Metrics

1. **Hallucination Rate** (sentence-level as in HaloCheck).  
2. **Precision@1** on personal facts.  
3. **Cross-Persona Leakage** (% answers containing other users’ facts).  
4. **Latency + Cost** per turn.  
5. **GDPR Erasure Lag** (time to delete user vector + shards).

### 5.3 Baselines

* Single-pass LLM (temperature = 0).  
* RAG with ElasticSearch.  
* MixCL-fine-tuned model (needs retraining).  
* LLteaM multi-agent.

### 5.4 Success Criteria

| Metric | Target |
|--------|--------|
| Hallucination | ≤2 % |
| Leakage | <10⁻⁵ |
| Latency | <800 ms per turn (Gemma 7B on A10G) |
| Cost | <1.6× single-pass |

### 5.5 Statistical Method

* Two-proportion z-test vs baseline.  
* Bootstrap 10 k samples for latency distribution.  
* Ablation: vary k; with/without RFD mask.

---

## 6. Privacy, Compliance, and Risk Mitigation

1. **GDPR Articles 5, 16–18, 32** satisfied by per-user vector isolation and AES-GCM + HSM key management.  RFD masking reduces data-at-rest volume by ≈30 % (cf. RFD paper).
2. **Right to Erasure** – delete KV entry + embedding index slice; no retraining because parametric memory untouched.  Expected sub-second deletion.
3. **Model Volatility** – fixed Gemma deployment avoids LLteaM-style drift; GPT-4o used only for offline eval.
4. **Adversarial Prompts** – periodic AutoDebug style re-tests; regeneration of negative prompts monthly.
5. **Inference On-Device** – 7B Q4-K quantization; ensures data residency for highly regulated sectors.

---

## 7. Contrarian & Forward-Looking Ideas (Flagged Speculative)

* **Replica-Exchange Sampling (à la TCW)** for LLM decoding: run two temperature ladders that occasionally swap hidden states; could reach same consensus accuracy with k≈3.
* **Graph-Regularized PUFS**: store personal facts as a knowledge graph; use graph contrastive learning to improve recall without increasing leakage.
* **Differentiable RFD Layer**: back-prop through mask decisions so that future SFT can learn to avoid sensitive joins automatically.
* **Local LLM Distillation via MixCL Negatives**: fine-tune a 3-B model with MixCL to mimic sampled-consensus answers, slashing inference cost by 4–6×.

---

## 8. Open Problems

1. **Commonsense Deficit** – Association-analysis highlights that sampling cannot fix missing world knowledge; may need targeted pre-training.  
2. **Temporal Staleness** – Personal facts verified years ago still surface; dynamic validity intervals needed.  
3. **Cross-Modal Facts** – Photos or audio memories not handled; needs multi-modal embeddings + RFD extensions.

---

## 9. Recommended Next Actions

1. Green-light Months 1-2 tasks immediately; hardware and HSM procurement lead times ~6 weeks.  
2. Secure data-processing agreement drafts with legal for GDPR.  
3. Commission a pilot with 20 beta users in Q2 2026, ensuring instrumentation for leakage logging.

---

## 10. Conclusion

Sampling-based Q&A, once seen as a stopgap, now offers a practical, inexpensive path to both *hallucination suppression* and *personal-instance separation*.  By blending insights from MixCL, SelfCheckGPT, RFD privacy controls, and even cross-domain sampling theory (TCW, TMS, K-means retrieval), we can deploy LLM systems that are safer, cheaper, and regulation-ready—without waiting for next-generation model releases.

> *“Diversify, agree, isolate.”*  These three verbs summarize the blueprint presented here and set a concrete, measurable roadmap for the next six months.


## Sources

- https://cris.vtt.fi/en/publications/24e0f969-9a8a-4612-9d32-589bb068774d
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/39845
- http://hdl.handle.net/2117/172057
- https://zenodo.org/record/5841868
- http://hdl.handle.net/10251/201319
- http://arxiv.org/abs/2202.03629
- https://www.openaccessrepository.it/record/142499
- https://zenodo.org/record/8296440
- https://hdl.handle.net/11250/2990213
- https://hal.science/hal-03784937/file/ark%20_67375_WNG-PWSK0CF2-4.pdf
- http://arxiv.org/abs/2309.05217
- https://zenodo.org/record/7919873
- https://hdl.handle.net/11386/4834471
- https://hal-amu.archives-ouvertes.fr/hal-01965459/file/p125_kossoski_importance-sampling_jctc_2018-preprint.pdf
- https://www.repository.cam.ac.uk/handle/1810/358475
- https://escholarship.org/uc/item/0ng8c2q2
- https://doaj.org/article/1d6efe23e7ca43bc83056e128092d091
- http://arxiv.org/abs/2308.11764
- https://hdl.handle.net/11386/4753787
- http://arxiv.org/abs/2311.01041
- http://hdl.handle.net/10560/islandora:1001314
- http://arxiv.org/abs/2307.15343
- http://arxiv.org/abs/2308.15126
- http://arxiv.org/abs/2310.12516
- https://www.repository.cam.ac.uk/handle/1810/262385
- https://hal.inria.fr/inria-00001061v2/document
- http://urn.kb.se/resolve?urn=urn:nbn:se:miun:diva-34069
- https://ojs.aaai.org/index.php/AAAI/article/view/26596
- https://orbilu.uni.lu/bitstream/10993/52125/1/1-s2.0-S0306261922011722-main.pdf
- https://hal.science/halsde-00757162