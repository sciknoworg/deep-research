# Autoprompting: Generating Diverse Few-Shot Examples for Any Application

*Prepared 4 Sept 2025*

---

## 1  Motivation and Scope  
Few-shot‐learning performance of large models hinges on **(i)** the *quality* of the demonstrations and **(ii)** their *diversity* relative to the test distribution.  Manual curation is brittle, expensive and slow to transfer across modalities.  We therefore study *autoprompting*: the fully automated generation, selection and optimisation of few-shot exemplars (text snippets, code fragments, vision-language triplets, etc.) under tight resource, privacy and latency constraints.

The report synthesises the latest evidence—spanning AutoML competitions, quality-diversity algorithms, differentiable prompting, frugal HPO and budget-aware meta-optimisation—to propose a unified, compute-bounded pipeline that can service *any* downstream task or architecture.

---

## 2  Problem Formulation  
Given:
* A pretrained backbone model **M** (LLM, VLM, code LM, etc.) with frozen weights.  
* A target task **T** specified by a small validation set \(D^{val}\) and evaluation metric \(\mathcal E\).

Goal:  Produce a *bundle* \(\mathcal B = \{(p_i, a_i)\}_{i=1}^k\) of *k* diverse prompt–answer pairs that, when prepended in-context, maximises \(\mathcal E(M, \mathcal B, D^{val})\) subject to

1. **Compute budget** \(C_{max}\) (FLOPs or wall-clock minutes).
2. **Privacy / data locality** (no raw data exfiltration; can require on-prem generation).
3. **Coverage constraints**: language set, protected attributes, edge cases.
4. **Explainability**: need to audit the generator.

This is a *constrained, multi-objective* optimisation in the spirit of AutoDL and CROP.

---

## 3  Prior Art and Key Learnings  
The table below positions each cited result against the four sub-problems of autoprompting:

| Contribution | Search / HPO | Diversity | Budget Awareness | Modality Agnostic |
|--------------|--------------|-----------|------------------|------------------|
|AutoDL/AutoCV (2019) | ✓ (any-time) | — | ✓ (20 min GPU) | ✓ (text/vision/speech)|
|Frugal Optimisation (FOC) | ✓ | — | ✓ (formal bounds) | ✓ |
|Quality-Divers. MAP-Elites | ✓ | ✓ | ✓ | ✓ |
|DART (ICLR ’22) | ✓ (gradient) | — | — | NLP but plug-and-play |
|tMOPSO | ✓ | — | ✓ (multi-budget Pareto) | ✓ |
|CROP | ✓ (resource split) | — | ✓ | ✓ |
|MultiTune | ✓ (adaptive fidelity) | — | ✓ | ✓ |
|Insertion-based Paraphraser | — | ✓ | — | Text |

**Main insights**
1. *Compute-bounded AutoML works*: AutoDL revealed that a strict 20-minute GPU cap does **not** preclude cross-modality generalisation when pipelines are designed to be any-time and early-stoppable.
2. *Budget must be a first-class citizen*: FOCHPO, tMOPSO, CROP and MultiTune all treat the FLOP envelope as an explicit variable, yielding graceful degradation when budgets shrink.
3. *Quality-diversity algorithms provide reusable primitives*: MAP-Elites style illuminations let us simultaneously *cover the extrema* (edge-cases) and *optimise for task loss*—critical for bias and robustness audits.
4. *Gradient-based prompt search scales to small LMs*: DART shows that back-prop over continuous prompt embeddings beats hand engineering without inference overhead, hinting at a differentiable subroutine inside our pipeline.
5. *Constraint-aware paraphrasers match autoregressive SOTA*: Insertion models can produce lexical-constrained variants cheaply, a key for privacy-preserving synthetic data.

---

## 4  Proposed Architecture  
```
┌──────────────┐    k0 random seeds   ┌────────────────┐   Pareto-front          ┌───────────────┐
│  Seed Pool   │──►(p,a)₀,…           │ Quality-Diversity│──► Bundle Selector ───►│Few-Shot Buffer│
└──────────────┘   (CROP split)      │  (MAP-Elites)  │   (tMOPSO + FOCHPO)     └───────────────┘
            ▲                           │   ↓ GradFine-Tune   ▲                   │
            │                           │  (DART / LoRA)      │                   │
            │  Insertion-based           └─────────────────────┘                   │
            │  paraphraser                                                          │
            └───────────────────────────────────────────────────────────────────────┘
```
Legend: colours indicate compute budgets dynamically reallocated via CROP; arrows are early-stoppable.

### 4.1 Seed Pool Initialisation  
* Use constrained-random or order-free insertion models to draft *k₀ ≫ k* candidate (prompt, answer) pairs, optionally conditioned on keywords, APIs or vision patches.
* Apply **CROP**: allocate \(ϕ · C_{max}\) to seeding vs. \((1-ϕ)\) to main search, where \(ϕ\) is optimised on-line.

### 4.2 Quality-Diversity Core (QD-MAP)  
*Behaviour space*: choose latent descriptors that matter for downstream fairness—e.g., language, sentiment polarity, token length, protected attributes—so that MAP-Elites bins can surface diverse niches.
*Objective*: each individual is evaluated on *aggregated meta-metric* \(M = \alpha · E + (1-\alpha) · \text{Robustness}\) (weight \(\alpha\) set via tMOPSO).
*Any-time property*: QD algorithm can be interrupted at any moment, yielding a valid elite archive—a direct fit to AutoDL-style scoring.

### 4.3 Gradient Fine-Tuning (Optional)  
For text-only tasks under looser privacy rules, back-prop through **DART-style continuous prompts** or lightweight LoRA-adapters for the backbone.  This step is selective: invoked only for the top-\(m\) elites to stay within \(C_{max}\).

### 4.4 Bundle Selection under Multi-Budget Uncertainty  
We rarely know the *inference-time* context window or acceptable latency ahead of deployment.  Using **tMOPSO**, we produce *Pareto fronts* of bundles each optimised for a *different* test-time shot budget \(k\in{1,2,…,32}\).  At serve time the appropriate bundle is chosen on-the-fly.

---

## 5  Handling Practical Constraints

### 5.1 Compute  
* MultiTune auto-discovers fidelity schedules, e.g., **image resolution** for VLM prompts or **sequence length** for LLM prompts, reducing wasted FLOPs.
* Frugal optimisation guarantees sub-linear *cost* regret: if a run must be aborted, current best is near-optimal.

### 5.2 Data Privacy  
* Generate seeds with *privacy-abstracted* descriptors (keywords, class labels) instead of raw client text/images.
* Perform all gradient steps with **differentially private (DP-SGD)** or **rewind-and-prune** techniques; release only continuous embeddings, not real data.

### 5.3 Multilingual & Cross-Modality  
* Behaviour descriptors include language tag and modality flag to enforce coverage.  MAP-Elites “illumination” finds at least one elite per language-modality bin.
* Insertion-based generators natively support hard lexical constraints, enabling *code-switching* prompts.

### 5.4 Alignment with Backbone Architectures  
* The pipeline is **model-agnostic**: for PaLM-type LLMs we use text tokens; for CLIP we treat image patches + caption tokens as a joint tensor (cf. AutoDL uniform-tensor trick).  Continuous prompts can be LoRA-tuned even on vision transformers.

---

## 6  Evaluation Methodology
1. **Any-time AULC (Area Under Learning Curve)**: mirror AutoDL scoring—submit a *time-stamped stream* of candidate bundles; reward early gains.
2. **Robustness Stress-Suite**: adversarially perturbed validation sets (spelling variants, JPEG artefacts) to quantify over-specialisation.
3. **Bias & Coverage Audits**: measure performance gaps across MAP-Elites bins; a flat profile is desirable.
4. **Cost-Adjusted Score**: \(S = E / \log(1+\text{FLOPs})\) to discourage brute force.

---

## 7  Practical Playbook for Deployment
Step | Action | Tools / Hints
-----|--------|-----------
1 | *Define constraints*: max wall-clock, disallowed data flows, target languages | Document contract
2 | *Allocate budget*: run CROP to split between seed gen and optim | CROP lib
3 | *Seed generation*: call insertion-based paraphraser with control keywords; synthesise low-res image patches for VLM | open-source `insertion-gen`
4 | *QD search*: start MAP-Elites; log elites every 30 s (any-time) | `qdpy`, `evogym`
5 | *Adaptive fidelity*: wrap objectives with MultiTune to downsample tokens / images early | MultiTune API
6 | *Pareto bundling*: open tMOPSO in `budget_space = {1,…,32}`; export bundle ↔ budget map | `tmopso-py`
7 | *Fine-tune (optional)*: DART continuous prompts on top-m elites | LoRA + FP-16
8 | *Validation & freeze*: run Bias+Robustness suite; pick bundle meeting policy thresholds | Custom scripts
9 | *Serve*: at inference choose bundle ≤ available context window | lightweight router

Expected engineering effort: ≈2 person-weeks to script once; afterwards, per-task autoprompting is one-command.

---

## 8  Opportunities & Contrarian Ideas
1. **Zero-Cost Uncertainty Estimation**: compute *proxy diversity* via cosine novelty during seed generation, skipping expensive evaluation passes.
2. **Edge-device Co-Optimisation**: jointly optimise *prompt length* and *quantisation scheme* of the backbone so that the pair fits mobile VRAM.
3. **Neural Compression of Prompt Bundles**: store bundles as latent codes in a tiny VAE; decompress on-device to sidestep context-window limits.
4. **Adaptive Shot Count at Test-time** *(speculative)*: use early-exit confidence to decide whether to read further exemplars, amortising latency.
5. **Federated Autoprompting**: run QD search locally on data silos; use *control improvisation* to release only loss-augmented descriptors, preserving IP.

---

## 9  Conclusion  
The collective evidence from AutoDL, differentiable prompting and budget-aware meta-optimisation shows that *fully automated, compute-bounded autoprompting* across modalities is not only feasible but competitive with human curation.  A unified pipeline combining constrained-random seeding, quality-diversity illumination, gradient fine-tuning and Pareto bundling yields robust, bias-aware and privacy-compatible few-shot exemplar sets under strict FLOP envelopes.

Future work should explore end-to-end differentiable approximations of the QD layer and tighter integration with DP mechanisms, unlocking autoprompting for regulated industries.


## Sources

- https://cos.bibl.th-koeln.de/frontdoor/index/index/docId/11
- https://hal.science/hal-01906226/file/AutoDL_challenge_design_and_beta_tests_____towards_Automatic_Deep_Learning.pdf
- https://zenodo.org/record/4281275
- http://hdl.handle.net/10536/DRO/DU:30117272
- http://arxiv.org/abs/2211.02227
- https://hal.archives-ouvertes.fr/hal-02265053/document
- https://digital.library.unt.edu/ark:/67531/metadc928732/
- https://ujm.hal.science/ujm-04165556
- http://hdl.handle.net/11586/319892
- http://arxiv.org/pdf/1006.4645.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.6272
- http://hdl.handle.net/10453/131494
- http://hdl.handle.net/10722/218962
- http://tiger.cs.tsinghua.edu.cn/Students/kongzq/pubs/cscwd09.pdf
- https://hal.inria.fr/hal-03159795/document
- http://resolver.tudelft.nl/uuid:2c5f0b4d-966d-4eb1-a26a-ca0893afb8aa
- https://hal.archives-ouvertes.fr/hal-00922135
- https://cris.maastrichtuniversity.nl/en/publications/8ed288ab-0a88-4b1c-83bd-dd063e90fb3b
- https://zenodo.org/record/6525661
- https://hal.archives-ouvertes.fr/hal-00904008/file/paper.pdf
- http://digital.lib.uidaho.edu/cdm/ref/collection/etd/id/1757
- http://hdl.handle.net/2043/30472
- https://ojs.aaai.org/index.php/AAAI/article/view/17239
- http://arxiv.org/abs/2108.13161
- http://hdl.handle.net/10.1371/journal.pone.0272167.t001
- https://docs.lib.purdue.edu/dissertations/AAI3592575
- https://elib.dlr.de/132578/
- http://cs.boisestate.edu/~uh/Publication/rtas04.pdf
- http://creativecommons.org/licenses/by-nc-nd/3.0/us/
- http://resolver.tudelft.nl/uuid:4ad6c3bf-6a66-4666-8700-aecd06b4407d
- https://hal.archives-ouvertes.fr/hal-02386805/document
- http://www.cs.sfu.ca/~anoop/papers/pdf/multi_metric_tune.pdf
- https://hal-ujm.archives-ouvertes.fr/ujm-03267869/document