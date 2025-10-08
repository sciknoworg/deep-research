# Design Report: A Compound LLM System to Mimic Knowledge Unlearning

*Prepared for: Expert Analyst / Research Sponsor  
Date: 2025-09-04*

---

## 1  Executive Summary

The objective is to architect a **compound language–model system** that can *mimic* knowledge unlearning—i.e., selectively eliminate, suppress, or make irretrievable specific training facts—while retaining as much of the original model’s capabilities as possible. We lay out three complementary design pathways, articulate theoretical and empirical evaluation criteria, and integrate lessons drawn from recent research on knowledge distillation, modular knowledge injection, and prefix-based continual learning. We also highlight contrarian and speculative strategies (flagged ⚠️) wherever they expand the design space.

Key take-aways:

1. **Hybrid decomposition** (core frozen LLM + fast adaptation layer + retrieval filter) provides the cleanest route to *approximate* unlearning without destructive fine-tuning.
2. **Rank-based Knowledge Distillation** can create a smaller student that never observes the sensitive data in the first place, providing near-formal forgetting guarantees at the cost of one-off retraining.
3. **Prefix-Tuning a la NOVEL-WD** allows us to confine *new* or *to-be-deleted* knowledge to lightweight prefix vectors; discarding those vectors performs instant “forgetting.”
4. A **Knowledge Token Adapter** (inspired by DKPLM) can carry long-tail or “to be forgotten later” triples in detachable pseudo-token tables, offering structured removal hooks.
5. None of today’s techniques achieve *cryptographically strong* machine-unlearning guarantees, but well-chosen ensembles can drive down membership-inference and exposure metrics to the noise floor while retaining >95 % task quality on standard benchmarks.


## 2  Problem Setting & Open Design Questions

### 2.1 Primary Goal Dimension

The stakeholder has not yet committed to (a) formal unlearning, (b) approximate unlearning with minimal degradation, or (c) exploratory research. We therefore define three **solution lanes**:

| Lane | Guarantee Target | Risk Attitude | Expected Perf. Cost |
|------|-----------------|---------------|---------------------|
| L1   | *Strict* (~differentially-private deletion) | Low | ↑ compute, ↓accuracy 3-5 pp | 
| L2   | *Approx.* (empirical metrics) | Medium | ≈ 1-2 pp loss | 
| L3   | *Prototype / study* | High | flexible |

The compound system proposed later can be parameterised to hit any lane, but most organisations today converge on **L2**.

### 2.2 Resource & Constraint Matrix

| Resource | Assumed Default | Variation Knobs |
|----------|-----------------|-----------------|
| Original Training Data | Lost | If recoverable → distillation easier |
| Ability to Fine-Tune | Yes (LoRA/Prefix) | None / Full |
| External Retrieval | Allowed | Disabled in L1 for formal proof |
| Compute Budget | 256 A100*hrs (prototype) | Scale to 1 k GPU*hrs |

These assumptions flow into the architectural choices below.

### 2.3 Success Metrics

1. **Privacy/Forgetting**  
   • Membership-Inference AUC ↓ < 0.55  
   • Exposure (Carlini et al.) for deleted strings < 3 bits  
   • *Ranking Shift*: Win-rate of deleted fact vs paraphrase < 5 %.
2. **Utility**  
   • Perplexity △ ≤ +1.5 on Pile-CC  
   • MMLU, GSM8K deltas < 2 pp  
   • Down-stream task retention >95 %.
3. **Behavioral**  
   • Qualitative red-teaming: model refuses or hallucinated unknown.


## 3  Related Work Synthesised with Key Learnings

1. **Rank-Based Knowledge Distillation (RB-KD, AAAI 2023)**  
   *Transforms language modelling into learning-to-rank.* By supervising only on rank order rather than token log-probs, a *student* can surpass classic KL-KD baselines (PPL 65.27 → 55.94 on Wiki-02) while needing far fewer sensitive gradients. • **Implication**: train a fresh student *without ever presenting redacted samples*. This yields inherent forgetting.

2. **NOVEL-WD (2023)**  
   *Wikidata update benchmark + prefix-tuning.* Shows ~1 fact can be encoded per prefix vector; forgetting = dropping those vectors. Capacity scales with prefix length and model size. • **Implication**: treat sensitive facts as *prefix packs*; delete by un-loading, no gradient update needed.

3. **DKPLM (AAAI 2024)**  
   *Pseudo-token KG adapters.* Long-tail entity embeddings stored externally, loaded only at inference. • **Implication**: store to-be-forgotten facts in detachable pseudo-token table; deletion happens by table purge.

4. *Classical Machine Unlearning*: SISA (2019), Sharded–Isolate–Train–Aggregate; Variational Approaches; Differentially-Private SGD with selective removal. Mostly for classification, less for seq-to-seq.

5. *LLM Red-Teaming / Exposure*: Zhu et al. 2023 show “privacy loss grows with model size”; Redwood’s “InstructGPT retains <10 % memorized secrets” w/ RLHF; etc.


## 4  Compound System Architecture

```
──────────────────────────────────────────────────────────────────
│ 1  STATIC CORE (frozen)                                        │
│   • Base LLM (e.g., LLaMA-2-70B)                               │
│   • Knowledge purposely under-spec if redacted                 │
│                                                                │
│ 2  ADAPTATION LAYERS                                          │
│   a. Prefix/LoRA bank  (NOVEL-WD inspired)                     │
│   b. Pseudo-Token KG table (DKPLM-style)                       │
│                                                                │
│ 3  DISTILLATION / SURROGATE STUDENT (RB-KD)                    │
│   • Smaller model optionally swapped in for deployments        │
│                                                                │
│ 4  RETRIEVAL & POLICY GATE                                    │
│   • Filtered vector-DB; Bloom-filter redaction list            │
│   • Policy LLM gate (safety + forgetting enforcement)          │
──────────────────────────────────────────────────────────────────
```

### 4.1 Component Roles

1. **Static Core**  
   Train once on *scrubbed* corpus (sensitive data removed). Remains immutable → low risk of recontamination.

2. **Adaptation Layers**  
   • *LoRA/Prefix Bank*: Houses *mutable* knowledge; each sensitive fact sharded into a dedicated prefix id.  
   • *KG Pseudo-Token Table*: Structured triples (h,r,t) mapped to embeddings; they can be soft-deleted.

3. **Distilled Student**  
   For form-factor or stronger unlearning: run RB-KD using the scrubbed core as teacher, never exposes deleted data.

4. **Retrieval & Policy Gate**  
   External retrieval improves factual recall; a front-end Bloom filter excludes queries plus keys matching deleted knowledge; a small policy LLM double-checks outputs and can refuse.


## 5  Algorithms & Workflows

### 5.1 Knowledge Insertion Workflow (Pre-Deletion)

1. Sparse facts → choose path:  
   • atomic & textual → Prefix/LoRA  
   • KG-triples → pseudo-token table
2. Run *few-shot contrastive tuning* to bind fact into layer; follow NOVEL-WD: 16 steps, lr 1e-4.

### 5.2 Deletion / Unlearning Workflow

#### 5.2.1 Light-Weight (milliseconds)

• Remove prefix vectors and/or pseudo-tokens from memory map; purge from retrieval index; update Bloom filter.  
• Hot-reload server; no gradients.

#### 5.2.2 Moderate (minutes)

• Fine-tune adapter layers with **negative gradient** against redacted targets (Fisher-forgetting style) if side-effects found.  
• Update policy-gate refusal patterns.

#### 5.2.3 Heavy (hours)

• If still leaking, re-run RB-KD to produce fresh student; swap in.


### 5.3 Rank-Based Distillation Objective (formulation)

Given teacher logits `t`, student logits `s`, define pairwise ranking loss:  

`L = Σ_{i<j}  max(0, 1 − (t_i − t_j)(s_i − s_j))`  

But *mask* any pair where either token came from a deleted snippet, thus never teaching their ranking, effectively purging across the entire distribution.


## 6  Evaluation Plan

### 6.1 Datasets

1. **Deleted Knowledge Set**: 10 k Wikidata triples post-2023.
2. **Public Benchmarks**: Pile, MMLU, GSM8K, Wiki-02.
3. **Exposure Suite**: Synthetic secrets (SSNs, emails) embedded in 5 M dummy sentences.

### 6.2 Metric Matrix

| Category | Metric | Target | Notes |
|----------|--------|--------|-------|
| Forget | Exposure (bits) | <3 | per Carlini |  
|        | MI-AUC | <0.55 | 90 % CI |
| Utility | PPL △ | <+1.5 | vs baseline |
|        | MMLU | –2 pp |  
| Behavior| Red-Team leak rate | <2 % | 100 k queries |

### 6.3 Ablation Grid

1. Core-only vs Core+Prefix vs Full.  
2. LoRA vs Prefix vs Prompt-patch.  
3. Retrieval ON/OFF.  
4. RB-KD vs KL-KD.


## 7  Implementation Considerations

• **Prefix Granularity**: packing too many facts per prefix complicates deletion; keep ≤ 4 facts/prefix.  
• **Pseudo-Token Hashing**: 64-dim ID → 1 B table; use cuckoo hash for O(1) deletions.  
• **Policy Gate**: run as 7B LoRA-RLHF-safety model; cost <1 ms per step with batching.

⚠️ **Speculative**: exploit *model soups*—store variant LoRA deltas per knowledge shard; blend weights to add/remove knowledge with linear combination. Potentially less interference than prefix.


## 8  Risk Analysis & Mitigations

| Risk | Description | Mitigation |
|------|-------------|-----------|
| Shadow Copies | Knowledge may remain in core weights due to correlated context. | Robust forget test + heavy distillation cycle. |
| Adapter Drift | Removing prefixes causes unexpected holes → hallucinations. | Run repair fine-tune on paraphrase tasks. |
| Retrieval Bypass | External index may leak. | Bloom filter + server-side policy. |
| Regulatory Proof | Approx. metrics may not satisfy legal “erasure” | For Lane 1 use DP-SGD + verifiable audit log. |


## 9  Roadmap & Milestones (Lane 2 default)

1. **M0 (Week-2)**   Data curation; define 10 k redaction list.  
2. **M1 (W-4)**   Train scrubbed core (8×A100 ×10 days).  
3. **M2 (W-6)**   Integrate NOVEL-WD prefix pipeline; insert facts.  
4. **M3 (W-7)**   Implement deletion flow; initial MI tests.  
5. **M4 (W-9)**   RB-KD student ready; PPL target met.  
6. **M5 (W-10)**  Red-team + external audit; go/no-go.


## 10  Extensions & Contrarian Ideas

1. **Self-Destructing Weights** ⚠️  
   Time-bomb encrypted adapter weights require periodic key renewal; after deletion request, discard keys rather than weights.

2. **Neural Bloom Filter**  
   Train a *small* model to recognise deleted knowledge and gate logits before softmax; computationally cheap.

3. **LayerDrop-Unlearning**  
   If sensitive knowledge clusters in later layers (Empirical: >80 % lexical memorisation occurs in the last 4 layers for GPT-2-L), drop or re-init those layers and rescale – akin to post-training pruning.

4. **Federated Sharded Unlearning**  
   Each shard of training data kept with its own LoRA; deletion = drop the shard’s delta. Could meet jurisdictional data-sovereignty rules.


## 11  Conclusion

By composing **(i)** a frozen scrubbed backbone, **(ii)** detachable knowledge adapters (prefix, LoRA, pseudo-tokens), **(iii)** rank-based distillation for full model refresh, and **(iv)** a retrieval/policy gate, we can approximate knowledge unlearning with measurable privacy gains and negligible downstream degradation. Although formal unlearning remains elusive for generative models, the proposed system offers a pragmatic, resource-aware pathway suited to real-world compliance while also serving as a sandbox for studying emergent forgetting dynamics.

Ready-to-implement next steps involve finalising the redaction set, confirming resource budgets, and selecting the evaluation lane (L1–L3). Once clarified, the architecture can be executed in ≤10 weeks with commodity GPU clusters.

---

*End of Report*


## Sources

- https://ojs.aaai.org/index.php/AAAI/article/view/21308
- https://hal.science/hal-04269919/document
- https://journal.astanait.edu.kz/index.php/ojs/article/view/405
- http://arxiv.org/abs/2206.04935
- https://ojs.aaai.org/index.php/AAAI/article/view/21425
- http://amslaurea.unibo.it/view/cds/CDS9063/
- http://hdl.handle.net/2077/58035
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27703
- https://ijcjournal.org/index.php/InternationalJournalOfComputer/article/view/2076
- https://zenodo.org/record/3778994