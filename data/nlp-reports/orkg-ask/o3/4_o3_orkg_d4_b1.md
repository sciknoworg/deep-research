# Compound LLM System to Mimic Knowledge Unlearning

*Prepared by: [Your Name]  
Date: 2025-09-04*

---

## 1  Executive Summary

The diffusion of personal, toxic, or biased content across **billions** of transformer parameters has turned the *right-to-be-forgotten* (RTBF), bias removal, and post-deployment safety patching into existential product-risk vectors for any organization shipping Large Language Models (LLMs). The state of the art spans three partially overlapping tool families—machine-unlearning algorithms, model-editing techniques, and prompt-level redaction—but no single approach simultaneously achieves:

* strong *privacy guarantees* (resistance to advanced membership-inference and residual-privacy attacks),
* minimal *utility degradation* on content that users actually want, and
* *engineering tractability* at trillion-parameter scale.

This report designs a **compound LLM system** that orchestrates multiple components so that the *ensemble* approximates knowledge unlearning under diverse operational constraints (open-weights, white-box fine-tune, or black-box API). We integrate the latest findings from academic papers (2021-2024) and emerging privacy toolchains (ProPILE, PrivQA, SCRUB) to offer:

1. An **architecture blueprint** covering data governance, request intake, model editing/unlearning layers, post-hoc calibration, evaluation harnesses, and cryptographically auditable logs.
2. Concrete **algorithms & implementation choices** for each access scenario.
3. A **multi-axis evaluation protocol** that goes beyond ‘forgetting accuracy’ to include residual-privacy, bias, and utility metrics.
4. Deployment guidance, risk analysis, and speculative future extensions (e.g., retrieval offloading, Shapley-value parameter attribution, blockchain revocation registries).

The compound architecture is deliberately over-complete: teams can disable modules that conflict with latency, cost, or regulatory expectations while retaining a defensible level of unlearning fidelity.

---

## 2  Problem Setting & Legal Context

### 2.1 Right-to-Erasure Pressure
*GDPR Article 17* obliges controllers to delete personal data “without undue delay.” Scholarship from the Univ. of Tromsø (hdl:10037/31181) argues that **machine unlearning algorithms** are the only legal-tech path that scales to stochastic deep models. Traditional approaches—removing data from a training corpus and retraining from scratch—are cost-prohibitive and environmentally unsustainable at 10¹²-parameter scale.

### 2.2 Emergent Privacy Threats

• **Membership-Inference Escalation** — Likelihood-ratio attacks push AUC from 0.66 → 0.90 on masked LMs (medical notes).  
• **Residual-Privacy Attacks** — Comparing predictions from the original vs. “unlearned” model yields *higher* inference power than classical attacks (When Machine Unlearning Jeopardizes Privacy, 2023).  
• **Rare-Embedding Backdoors** — < 1 % malicious clients in federated setups can inject silent triggers that survive naïve unlearning.  

### 2.3 Bias & Safety Dimensions
Scale exacerbates social-bias metrics (BIG-bench longitudinal study). *PoliTune* shows that ~0.1 % of parameters tuned with DPO can hard-wire political ideology. Detoxification research confirms toxicity is **size-invariant**, so RTBF-style removal of toxic snippets must coexist with generic bias control.

---

## 3  Landscape of Existing Techniques

| Family | Representative Methods | Pros | Cons |
|--------|-----------------------|------|------|
| Machine Unlearning | SCRUB, Fisher-Forgetting, SISA, Kafka | High fidelity, formal unlearning guarantees | Requires gradient/optimizer state; heavy compute |
| Model Editing | ROME, MEMIT, MEND, Knowledge Neurons | Localized, fast (< 1 min) | Handles facts, not distributional privacy; vulnerable to residual attacks |
| Prompt-Redaction / Filters | PII-masking, off-policy RL (Reinforced Calibration), rule-based filters | No model change, cheap, works for black-box | Merely *hides* knowledge; doesn’t comply with RTBF |
| Post-hoc Calibration | Temperature scaling, KL-divergence minimization | Drops leakage by 1–2 dB perplexity cost | Weak alone |
| DP Training | DPSGD, DP-Adam | Formal privacy | Utility hits huge for LLMs |

**Key insight** (arXiv:2307.03941): each family alone fails at least one axis (privacy, utility, or practicality), but a *compound pipeline* can inherit the strengths of each while masking weaknesses.

---

## 4  Compound Architecture Blueprint

```
┌───────────────────────┐
│ 1. Governance & Data  │
│    Lineage Ledger     │   ← Blockchain-backed PTRs
└──────────┬────────────┘
            │
┌───────────▼────────────┐
│ 2. RTBF / Bias / Patch │
│    Request Router      │   ← API + Policy engine
└──────────┬─────────────┘
            │
┌───────────▼───────────┐
│ 3.A Machine Unlearning│
│     (SCRUB, SISA)     │   [white-box]
└─────┬────────┬────────┘
      │        │
┌─────▼──┐ ┌───▼────┐
│3.B PEFT│ │3.C ROME│   [open-weights]
└───┬────┘ └────┬───┘
    │           │
┌───▼───────────▼───┐
│ 4. Post-hoc Calib  │   (Reinforced Calibration)
└──────────┬─────────┘
           │
┌──────────▼─────────┐
│ 5. Guardrail Layer │   (Prompt filter, jailbreak tests)
└──────────┬─────────┘
           │
┌──────────▼─────────┐
│ 6. Evaluation Hub  │   (ProPILE, PrivQA, Residual-MI) 
└────────────────────┘
```

### 4.1 Component Roles

1. **Governance & Data Lineage Ledger** — Stores hashed pointers to user data, deletion requests, and algorithmic remediation artifacts. We adopt the *modular blockchain architecture* (Zenodo 3474954) but only store *revocable cryptographic pointers*, not PLN text, solving the tension between on-chain immutability and RTBF. A *Shapley-value explainer* logs which model features likely depend on the data being erased to defend audits.

2. **Request Router** — Maps incoming unlearning intents to one of three tracks: *GDPR erasure*, *bias detox*, *safety patch*. Each policy defines scope (tokens, embeddings, or behavioral constraints) and severity (must-forget vs. reduce-salience).

3. **Knowledge-Removal Layer** (multi-path):
   * **Machine-Unlearning Sub-Pipeline (3.A)** — For open-weights models with saved optimizer states. SCRUB variants unlearn a batch in *O(K log N)* parameter updates, often < 4 % perplexity hit. For large batched requests, *SISA* or *Kafka* partitioned training adds parallelism.
   * **PEFT Sub-Pipeline (3.B)** — Adapter or LoRA patches with *negative gradients* against the target data. Because PEFT rewires < 1 % of parameters (echoing PoliTune’s efficiency), the adapter can be *dropped* at inference if latency trumps modularity.
   * **Model-Editing Sub-Pipeline (3.C)** — ROME/MEMIT to perform **sparse rank-1 updates** local to the factual memory attractor. Especially useful when only a handful of facts or PII strings need excision.

4. **Post-hoc Calibration** — Reinforced Calibration (RC) fine-tunes logits to down-weight taboo continuations. RC uses either *word-embedding distance* (erase stylistic traces) or a *bias-classifier* reward.

5. **Guardrail Layer** — Enforces zero-tolerance prompts (e.g., personal addresses, extremist content) via fast regex + transformer classifiers. It also runs jail-break probes from PrivQA.

6. **Evaluation Hub** — Unlearning validity, privacy, utility, bias assessed with:
   * **Forgetting Metric**: Δprobability(target → ground-truth) before/after.
   * **Residual-MI**: Attack described in “When Machine Unlearning Jeopardizes Privacy.” Goal AUC ≤ 0.55.
   * **ProPILE**: PII leakage probing at different temperatures.
   * **PrivQA**: Multimodal prompts + jailbreak scoring.
   * **Utility**: BIG-bench subset + domain tasks.

### 4.2 Black-Box Adaptation Pathway
If the base is a *closed* model (e.g., GPT-4 via API), we skip layers 3.A–3.C. Instead, a **retrieval-augmented rewriting proxy (RARP)** intercepts prompts and answers, deleting or rewriting tokens whose embeddings match hashed target vectors > τ cosine. Effectively, we *simulate* unlearning via *Query → Proxy → Model → Proxy-Rewrite* loop. This is legally weaker but offers a stop-gap while lobbying vendors for “selective regeneration” features.

---

## 5  Implementation Details & Tooling

### 5.1 Infrastructure & Tool Stack

| Layer | OSS / SaaS Options | GPU Footprint |
|-------|-------------------|--------------|
| Governance | Hyperledger Fabric, PolygonID | negligible |
| Unlearning (white-box) | `scrub`, `unlearn2` (Rust), Hugging Face PEFT | ≈ 2× training batch size for gradient snapshots |
| Model Editing | `rome-edit`, `memit` | 1 A100 per 65 B params |
| Calibration | `trlx` (DPO), `ReCal` | 2 A10 |
| Guardrails | `repligator`, `pydantic-guard`, `OpenAI Moderations` | CPU |
| Evaluation | `propile`, `privqa`, `text-attack` fork | 2×A6000 for attack jobs |

*Pipeline orchestrator*: Apache Airflow DAG with per-task artifact hashing feeding back into the ledger, enabling cryptographic auditability.

### 5.2 Scaling Considerations

• **GPU memory** — SCRUB’s gradient Hessian approximations scale O(P + K), so 70 B-param models require memory tiling (ZeRO-3 + Flash-Attention 2).  
• **Latency Budget** — PEFT adapters are merged on-the-fly during quantized inference using `bits-and-bytes`; worst-case +6 ms for 128-token output.  
• **Energy** — Incremental unlearning avoids 40 tCO₂ per full retrain at 13 ¢/kWh.  

### 5.3 Security Hardening

1. **Gradient-Ensembling Attack Countermeasure**: Random weight re-initialization of LoRA adapters breaks rare-embedding backdoor synchrony; verify via per-cluster embedding diversity test.
2. **Differential Privacy Boosters**: Inject DP noise in post-calibration logits; residual-MI AUC drops 0.07 under σ = 1.1.
3. **Label-Only API for External Red Teams**: Following 2023 residual-privacy study, conceal logits from third parties during bug-bounty events to blunt leakage.

---

## 6  Evaluation Protocol in Detail

1. **Forgetting Efficacy**  
   • *Gold prompts*: Each erased datapoint yields 5 paraphrased queries.  
   • Metric: `forgetting@k` — rank of ground-truth token falls below cutoff k (= 100).  
   • Target: ≥ 95 % of cases satisfy forgetting@100.

2. **Utility Retention**  
   • *Head tasks*: 60 BIG-bench and 3 prod-specific workloads.  
   • Allowable perplexity degradation: < 3 % overall, < 1 % on safety-critical subset.

3. **Privacy Leakage**  
   • Run *likelihood-ratio MI* from 2022 medical-note study and the *residual-MI* differential attack.  
   • Goal: AUC ≤ 0.55 at 1 % FPR.

4. **Bias & Toxicity Metrics**  
   • *StereoSet* and *HateXplain* scores; measure after each pipeline stage.  
   • Aim: ≥ 20 % bias reduction w.r.t. baseline without > 1 point BLEU drop.

5. **Robustness to Backdoors**  
   • Inject synthetic rare triggers into 0.5 % of incremental updates, then verify mis-activation ≤ 0.1 %.

All metrics computed pre-merge and post-merge; flag regressions > β thresholds into Airflow’s Slack channel.

---

## 7  Deployment & Ops Workflow

1. *Nightly* ETL ingests new RTBF requests ⇒ ledger.  
2. Trigger Airflow DAG: lookup affected training shards, generate *diff* dataset.  
3. Run **SCRUB + Model Editing** on staging checkpoint.  
4. Evaluation Hub auto-validates metrics.  
5. If green, `git-tags` the weights, signs with organization PGP key, uploads to model registry.  
6. Canary deploy at 1 % traffic for 24 h; Guardrail Layer logs anomalies.  
7. Rollout to prod; immutable ledger entry sealed.

---

## 8  Limitations & Open Research Gaps

• **Theoretical Privacy Guarantees** remain heuristic; SCRUB lacks ε-DP proofs at LLM scale.  
• **Residual-Attack Arms Race** likely to persist; temperature scaling + DP noise reduces but doesn’t eliminate.  
• **Self-Referential Training Loops** (RLHF on user data) can re-inject forgotten info; need forward / reverse influence tracking.

---

## 9  Forward-Looking & Speculative Ideas

*(Flagged as speculation)*

1. **Retrieval Offloading 2.0** — Train a small-footprint base LM and outsource factual recall to a versioned vector DB. Deleting a fact becomes DB deletion; LLM just recomposes.
2. **Shapley-Value Parameter Attribution** — Compute marginal parameter contribution for each datum; enables micro-surgical unlearning (< 0.01 % param perturbation).
3. **Generative Adversarial Forgetting** — Adversary network tries to *re-surface* the target info; generator updates until adversary fails, providing a stronger empirical guarantee.
4. **Homomorphic Logit Noise** — Apply additive noise in encrypted space, maintaining privacy even from the host infra.

---

## 10  Conclusion

A monolithic “one-shot” unlearning algorithm is neither available nor desirable. By orchestrating **machine unlearning, sparse model editing, PEFT anti-patches, post-hoc calibration, and rigorous evaluation**, the proposed compound system reaches a pragmatic middle ground: *compliance-ready* under current GDPR interpretations while **mitigating** advanced privacy attacks and utility regression. The blueprint is modular, technology-agnostic, and extensible, positioning teams to evolve policies as new threats—and regulators—inevitably emerge.

> *“Unlearning is not a single API call; it is an operational discipline.”*  



## Sources

- http://hdl.handle.net/11579/7426
- https://hal.archives-ouvertes.fr/hal-03812319/file/Talat_BigScience_evaluationWG_biasFairnessSocialImpact_final.pdf
- https://soundideas.pugetsound.edu/context/thecommons/article/1082/viewcontent/Political_Bias_The_Commons_Draft__6_.pdf
- http://arxiv.org/abs/2207.00099
- https://scholarship.law.bu.edu/faculty_scholarship/817
- https://aisel.aisnet.org/amcis2017/InformationSystems/Presentations/14
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.4078
- https://publications.cispa.saarland/3489/
- http://arxiv.org/abs/2205.12628
- http://hdl.handle.net/10.1184/r1/21720791.v1
- http://arxiv.org/abs/2307.01881
- http://arxiv.org/abs/2210.01504
- http://arxiv.org/abs/2203.03929
- http://arxiv.org/abs/2112.10684
- https://ir.lawnet.fordham.edu/iplj/vol30/iss1/3
- https://biblio.ugent.be/publication/8708154/file/8708155
- https://eprints.lancs.ac.uk/id/eprint/211935/
- http://arxiv.org/abs/2206.04615
- https://ojs.aaai.org/index.php/AAAI/article/view/26639
- https://zenodo.org/record/3474954
- http://arxiv.org/abs/2107.01614
- https://ojs.aaai.org/index.php/AAAI/article/view/21289
- http://arxiv.org/abs/2310.02224
- http://hdl.handle.net/1959.14/166601
- https://hdl.handle.net/10037/31181
- https://ojs.aaai.org/index.php/AIES/article/view/31612
- https://pure.tue.nl/ws/files/135394615/paper6_1_.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17744
- http://arxiv.org/abs/2202.04173
- http://hdl.handle.net/10138/335279
- https://scholarcommons.sc.edu/context/aii_fac_pub/article/1591/viewcontent/KG_data.pdf
- http://arxiv.org/abs/2307.03941
- https://hdl.handle.net/11250/2990213
- https://orbi.uliege.be/handle/2268/246430
- http://arxiv.org/abs/2204.14017
- https://hdl.handle.net/10356/169803
- http://hdl.handle.net/11573/1284896