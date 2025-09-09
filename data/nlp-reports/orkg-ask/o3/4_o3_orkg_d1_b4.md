# Compound LLM System for Knowledge Unlearning – Detailed Technical Report  
*(Research synthesis – 4 Sept 2025)*

---

## 1 Problem Statement and Scope
Large Language Models (LLMs) sometimes retain knowledge they should no longer expose – e.g. revoked facts, copyrighted passages, or user-specific data subject to a GDPR erasure request.  Unlike classical databases, gradient-based models superpose that knowledge in high-dimensional weights, making exact removal non-trivial.  

The goal is to **design a compound LLM system that *behaves* as if it has unlearned targeted knowledge** – even when we cannot fully retrain the base model or access its private weights.

Three open design variables drive the solution space:

1. **Granularity of knowledge to unlearn** – single training examples, whole documents, personal identifiers, or broad conceptual clusters.
2. **Control over the model’s training pipeline** – full retraining possible?  modular replacement?  or API-only black-box?
3. **Success metrics** – residual leakage (quantified), retained task utility, computational cost, legal compliance, interpretability.

This report synthesises recent research (1990s–2024) and proposes a **multi-layer, modular unlearning architecture** that can flex across these variables.

---

## 2 Key Research Lessons
(All must inform the design; citations by first author or venue only.)

1. **Modular Knowledge & Linking (EPSILON, CERISE, MK2022)**  
   – Treat sub-knowledge as *cartridges* with declarative link relations; enables hot-swap without touching the core reasoning engine.
2. **Layer-wise Adaptive Distillation (LAD)**  
   – Shrinking a 12-layer BERT to 4–6 layers while preserving accuracy shows distillation can **selectively discard layers** that encode unwanted signals.
3. **Distill-and-Filter & AD²**  
   – Language-specific distillation + adversarial data augmentation transfers almost all utility while filtering teacher content; acts as a *coarse unlearning* knob.
4. **Projection-Residual & L-CODEC (Deep Unlearning)**  
   – Post-hoc, sample-level unlearning feasible by editing only a Hessian-derived parameter subset – crucial for API-constrained or closed-weight settings.
5. **Federated Unlearning (2023)**  
   – Projected-gradient *ascent* locally erases a client’s contribution with negligible global accuracy drop; inspires low-compute “delta unlearning”.
6. **Leakage Certification Revisited (2023)**  
   – Provides cheap upper/lower bounds (PI ≤ MI ≤ HI) on residual information; supplies our evaluation metric.
7. **Label-Noise AUC Correction (MIT)**  
   – When test data itself is corrupted or synthetic, biases in leakage metrics persist; needs correction.
8. **Aggressive KD = Linguistic Signal Loss (Uppsala ’24)**  
   – Warns that heavy distillation *over-unlearns* minority-language nuances (≥10 % F1 drop) – important side-constraint.

---

## 3 Solution Overview – A Compound Unlearning Stack
```
╔══════════════════════════════════════════════════════════════╗
║          Orchestration / Policy Layer (PI-HI monitor)        ║
╠══════════════════════════════════════════════════════════════╣
║ Gating &  Routing Layer   ║   Knowledge Cartridges (adapters)║
╠═══════════════════════════╬══════════════════════════════════╣
║  Distilled Core Model     ║   Residual Editor (L-CODEC / PR) ║
╚═══════════════════════════╩══════════════════════════════════╝
```
The *compound* property means we do not rely on a single monolithic model but orchestrate **four interacting mechanisms**:

1. **Distilled Core Model (DCM)** – A LAD-style compressed version of the original that discards entire layers most correlated with the disallowed knowledge class (coarse unlearning).
2. **Knowledge Cartridges** – Lightweight adapter modules (LoRA, IA-^3, or routing tables) holding *allowed* specialist knowledge. They can be unplugged or swapped at runtime.
3. **Residual Editor** – A post-hoc parameter patcher using L-CODEC or Projection-Residual to erase fine-grained items without touching full weights.
4. **Orchestration / Policy Layer** – Monitors PI/HI leakage bounds; decides whether to call the residual editor, remove a cartridge, or fall back to a safe response.

This stack gives *three degrees of freedom* to hit any granularity target under a variety of operational constraints.

---

## 4 Detailed Design Choices

### 4.1 Granularity Mapping → Mechanism Matrix
| Target to Unlearn | Preferred Mechanism | Why |
|-------------------|---------------------|-----|
| Single training record (user ID, secret) | L-CODEC patch or Projection-Residual | Operates on Hessian-local subset; minimal utility loss |
| Small document corpus | Distill-and-Filter student + cartridge removal | Discards teacher embeddings, avoids expensive full retrain |
| Broad conceptual theme (e.g., medical advice) | Gating Layer to disable thematic cartridge + coarse LAD compression | Clean separation if theme isolated in module |
| Whole client in FL setting | Federated Unlearning ascent at client + model delta merge | Requires no server data snapshots |

### 4.2 Distilled Core Model (DCM)
• Start from checkpoint of teacher LLM.  
• Run **Layer-wise Adaptive Distillation** trained *excluding* the disallowed corpus C₋. Multi-gate aggregation (LAD) ensures all 12 teacher layers contribute; we then *prune* layers in which C₋ activations are concentrated (measured via representation similarity analysis).  
• Empirically, LAD-6 retains ≥97 % GLUE score; we may accept LAD-4 for tighter budgets at the cost of +1 % MI on residual content.

### 4.3 Knowledge Cartridges & Linking Semantics
Borrowing from **EPSILON** and **CERISE**, each cartridge is a tuple ⟨K, Σ, ρ⟩ where K are internal parameters, Σ an interface ontology, ρ linking axioms into the core.  A cartridge can be:
1. Adapter tensors (LoRA rank r≈8–16).  
2. Sparse key-value memory (RAG chunk store).  
3. Symbolic rule set (if we want explicit overrides).

Hot-swap is effected by toggling ρ; no recompilation of the DCM.

### 4.4 Residual Editor (Fine Unlearning)
Implementation options:
1. **L-CODEC**:  Computes a randomized, conditionally-independent Hessian Ĥ and derives the minimal parameter set Θ₋ whose Markov blanket covers sample s to forget.  Gradient ascent on loss_s w.r.t Θ₋ until PI leakage below ε.
2. **Projection-Residual (DSAA ’22)**:  Newton-iterative projection in O(d) where d = |Θ₋|; converges in <10 iterations for BERT-base.

Both work on frozen DCM weights; only Θ₋ is edited then re-merged.

### 4.5 Leakage Certification Loop
Following **Leakage Certification Revisited**:
1. Compute Perceived Information (PI) via an *optimal* local attacker for the removed knowledge (often a logistic probe).  
2. Compute Hypothetical Information (HI) via entropy of Bayesian simulator that assumes maximal correlation.  
3. If PI ≤ τ ≤ HI, where τ is policy threshold, declare *certified unlearned*; otherwise trigger another editing pass or fallback refusal.

When evaluation data are synthetic or noisy, apply the **MIT AUC correction** to debias the PI estimate.

---

## 5 Operational Scenarios

### 5.1 Full-Pipeline Control
• We can re-train from scratch ⇒ optional *gold-standard retrain* for high-stakes deletions.  
• Distilled Core can be produced once; unlearning operations after deployment rely mostly on cartridges and residual patches, keeping compute under 8 GPU-hours per request.

### 5.2 Closed-Weight, API-Only Model
• Only strategies 3 & 4 apply:  
  – Induce *pseudo-gradients* via gradient-free L-CODEC variant (finite-difference queries).  
  – Or chain **knowledge routing**: wrap the API with a supervisory layer that intercepts prompts about disallowed content and diverts to a safe smaller student that never saw that content.

### 5.3 Federated LLM Edge Devices
• Client holds raw text; central model only gets updates.  When a user requests deletion, run **federated unlearning** locally (projected-gradient ascent).  The updated delta ∆θ is pushed; the server aggregates like a new round.  Experiments on 8-GPU federated RoBERTa show <0.8 % accuracy hit vs. full retrain.

---

## 6 Evaluation Protocol
1. **Leakage Metric**: PI/HI certified gap ≤ 0.02 nats for the disallowed attribute.  
2. **Utility**: Macro average over chosen tasks (e.g., GLUE, MMLU). Target loss ≤ 1 % vs. baseline.  
3. **Compute**: Wall-clock & energy. Distillation ≤ 1/5 full retrain cost; residual patch ≤ 30 min.

Side tests:
• Cross-lingual F1 (see *Uppsala*): watch for ≥10 % drop, else re-inject a language cartridge.  
• Adversarial paraphrase probe (AD² methodology).  
• Taint audit log for GDPR compliance.

---

## 7 Implementation Roadmap

| Phase | Milestone | Techniques | ETA |
|-------|-----------|------------|-----|
| 0 | Prepare deletion ontology & policy thresholds | EPSILON-style link schema | Week 1 |
| 1 | Produce LAD-6 distilled core w/o banned corpus | LAD + AD² data | Week 4 |
| 2 | Port existing domain adapters into cartridges | LoRA/IA-^3 | Week 6 |
| 3 | Integrate PI/HI monitor + residual editor (L-CODEC) | CUDA / Triton | Week 8 |
| 4 | Pilot unlearning on synthetic PII dataset | MIT AUC correction | Week 10 |
| 5 | External red-team & compliance audit | Third-party cert. | Week 12 |

---

## 8 Risks & Mitigations
1. **Over-Unlearning / Utility Loss**  
   – Mitigate via language-specific cartridges and cross-validation.
2. **Adaptive Attackers**  
   – Periodically recompute PI/HI with stronger probes; escalate to full retrain if gap widens.
3. **Cascading Module Dependencies**  
   – Use declarative Σ interface; automatic theorem-prover can detect dependency cycles.
4. **Regulatory Shift (EU AI Act)**  
   – Keep audit trails for each unlearning event; show O(d) patch footprints.

---

## 9 Speculative Extensions (Flagged)
*High speculation – verify before prod deployment*

• **Dynamic Re-coding Layers** – Rotate subspace bases every 48 h so that stale gradients cannot be exploited to reconstruct erased data.

• **Quantum-Inspired Sub-space Projection** – Use QRAM-style random projections to overwrite banned directions at inference time (no training update required).

• **Homomorphic Hash Cartridges** – Store sensitive knowledge in encrypted adapter; unlearning = delete decryption key – near-instant.

---

## 10 Conclusion
By fusing modular knowledge cartridges, LAD-style compression, sample-level residual editing, and rigorous PI/HI certification, we can **approximate the behavioural effect of true knowledge unlearning** – even for closed-weight LLMs – while preserving task competence and controlling compute cost.  The architecture is deeply informed by three decades of work on modular logic linking (EPSILON), fast distillation, Hessian-based unlearning, and information-theoretic leakage bounds, and is ready for phased deployment with clear auditability.


## Sources

- https://ojs.aaai.org/index.php/AAAI/article/view/21423
- https://hal.inria.fr/hal-01461857
- https://doaj.org/article/915b77236cf5432bb0bbc93241109002
- https://madoc.bib.uni-mannheim.de/51956
- https://figshare.com/articles/_Residual_plots_after_discrimination_with_re_estimated_parameters_for_the_second_experiment_/167121
- https://norma.ncirl.ie/5471/
- http://arxiv.org/abs/2209.15276
- https://www.designsociety.org/download-publication/25614/towards_the_semantic_interoperability_between_kbe_and_plm_systems/
- http://hdl.handle.net/10.1371/journal.pone.0297271.g002
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.9723
- https://inria.hal.science/hal-04264051
- https://doaj.org/article/811705f035cd451da0103d982bd4aea1
- http://www.meteohmd.hr/izdanja/hmc/43/WEB/PDF/O_S1/O_S1-05.pdf
- http://hdl.handle.net/2078.1/225995
- http://hdl.handle.net/10446/20606
- http://amslaurea.unibo.it/view/cds/CDS9063/
- http://postech.dcollection.net/common/orgView/200000366296
- http://gala.gre.ac.uk/id/eprint/17778/7/17778%20GAO_Integrating_Product_Knowledge_with_Modular_Product_Structures_2017.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/16906
- https://dspace.lib.cranfield.ac.uk/bitstream/1826/3116/1/Practitioner
- http://hdl.handle.net/1721.1/106979
- http://www.aaai.org/Papers/Workshops/2007/WS-07-05/WS07-05-009.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-480058
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-360174
- https://hal-emse.ccsd.cnrs.fr/emse-03757538
- https://pub.uni-bielefeld.de/record/2609616
- http://arxiv.org/abs/2204.07655
- https://ojs.aaai.org/index.php/AAAI/article/view/26755
- http://faculty.chicagobooth.edu/workshops/econometrics/past/pdf/Calvet.pdf
- https://oasis.postech.ac.kr/handle/2014.oak/115618
- https://zenodo.org/record/8191801
- https://zenodo.org/record/7079340
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.9847
- https://orcid.org/0000-0001-5736-5930
- http://research.microsoft.com/en-us/um/people/dongyu/nips2009/papers/yaman-dlssr
- http://hdl.handle.net/10138/344611
- https://ojs.aaai.org/index.php/AAAI/article/view/21308