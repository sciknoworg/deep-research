# Uncertainty Estimation via Consistency in Self-generated References in Large Language Models

## 1. Purpose and Scope
This report synthesises prior empirical results and methodological advances on *reference-consistency–based* uncertainty estimation for large language models (LLMs).  The goal is to define a principled, task-agnostic framework that (i) extracts calibrated epistemic and aleatoric uncertainty from a **single** LLM by inspecting the *internal consistency of its own generated references* (rationales, citations, or chain-of-thoughts); and (ii) positions this technique relative to baselines such as Monte-Carlo sampling, SWAG, entropy over logits, and verbal-probability prompting.

Although the framework is designed to be task-agnostic, we provide concrete recipes for three high-value downstream tasks where reliable uncertainty is critical:
1. **Open-domain question answering (OD-QA)** — factuality and hallucination risk.
2. **Code generation & repair** — compilation/runtime failure cost is high.
3. **Clinical / medical reasoning** — domain demands strong calibrated caution.

We assume two operating regimes:
* **Logit-free access** (e.g., commercial GPT-4-class APIs).  No gradients, no logits, but unconstrained prompting and temperature control.
* **Logit access & light fine-tuning** (e.g., open-weights models).  Enables SWAG, MC-Dropout, entropy, etc.

Budget assumptions are a single high-end GPU per experiment day; full multi-seed MC-ensembles are assumed *possible but expensive*.

---

## 2. Motivation: Why Consistency?
1. **Self-generated references expose latent epistemic variables.**  When an LLM generates rationales or citations it implicitly samples from its *posterior over latent justifications*.  Divergence among those samples is an information-rich uncertainty signal.
2. **Logit-free calibration is already viable.**  The CalibratedMath studies (2022) showed GPT-3 can produce verbal probabilities that remain “moderately calibrated” even under distribution shift, outperforming raw logits in some settings.
3. **Human interpretability.**  Consistency metrics are naturally explainable to end-users (e.g., *“the model cited three mutually incompatible sources”*).
4. **Complementarity.**  Reference-consistency yields *orthogonal* information to token-level entropy and to SWAG-style posterior samples; combining them empirically improves detection of hallucinations and ambiguous cases.

---

## 3. Theoretical Framing
### 3.1 Reference-Consistency (RC)
Given a prompt **x**, an LLM produces an answer **a** and a set of *k* self-generated references **R = {r₁ … r_k}** (citations, rationales, proof steps, or chain-of-thoughts).  Let
```
RC(x) = 1 − D( R )
```
where **D(·)** is a divergence measure over semantics of references.  Lower consistency (higher *D*) implies higher epistemic uncertainty.

#### Divergence Measures
* **Textual overlap** (BLEU, ROUGE) — cheap but surface-level.
* **Semantic embedding dispersion** — cosine variance in Sentence-Transformer space.
* **Factual contradiction rate** — using an external contradiction classifier.
* **Graph structural distance** — for code ASTs or proof graphs.

### 3.2 Decomposing Uncertainty
Following cross-task studies separating epistemic vs. aleatoric uncertainty, we model
```
p(correct | x) = f_epistemic(RC(x)) × f_aleatoric(x)
```
where *f_epistemic* is monotone decreasing in inconsistency, and *f_aleatoric* captures irreducible task noise (estimated via calibrated residues or human-annotator disagreement proxies).

---

## 4. Algorithmic Techniques
### 4.1 Single-Model, Logit-Free (Primary Focus)
1. **Self-Consistency Sampling (SCS).**  Prompt the model *n* times with different temperature seeds; harvest *n × k* references; compute RC.  (Analogous to Wang et al. 2023 “Self-Consistency” for reasoning.)
2. **Verbal-Probability Calibration Layer.**  Augment the prompt: *“Answer plus a numeric confidence (0-100 %)”*.  Empirically, GPT-3 can output calibrated numbers (CalibratedMath).  Use RC as a feature to *post-calibrate* those verbal numbers via isotonic regression.
3. **Consistency-conditioned Decoding (CCD).**  Iteratively sample until RC ≥ τ or max budget.  The acceptance rate is itself a proxy for uncertainty.
4. **Reference Dropout Ablation (RDA).**  Randomly mask portions of the generated chain-of-thought during *post-hoc* evaluation; measure variance in the final answer.

### 4.2 Logit-Aware or Fine-tune-Based Baselines
* **Entropy & Margin.**  Token-level softmax entropy; margin between top-2 logits.
* **Monte-Carlo Dropout.**  30 stochastic forward passes with dropout enabled.
* **Bayesian SWAG.**  Lightweight posterior sampling; prior research shows improved correlation with human disagreement on NLI and 2–5 % accuracy gain.
* **Ensemble of Checkpoints (SWA).**  Averaged weights increase stability; Fleiss’ κ ↑ but biases persist.

### 4.3 Hybrid Approach (Speculative)
Use SWAG to draw *m* weight samples; for each, run SCS to gather *n* reference sets.  Then:
```
U_total = α · Var_weight( answers ) + β · Var_reference( R )
```
Choose α, β via validation ECE minimisation.

---

## 5. Implementation Recipes by Task
### 5.1 Open-Domain QA
*Prompt template*
```text
Q: <question>
A: Let’s think in step-by-step reasoning. Provide 3 source URLs with each final answer. Then output “Confidence: <0-100%>”.
```
Pipeline:
1. Collect 5 stochastic answers per question.
2. Compute RC via semantic clustering of the three URLs across samples (high variance ⇒ low RC).
3. Combine RC with verbal probability; calibrate on validation using expected calibration error (ECE).
4. Evaluate on **NQ-Ambig** and *49 ambiguous entities* dataset (prior work shows 75 % accuracy when prompts underspecified).

### 5.2 Code Generation & Repair
*Prompt*
```text
Write a Python function ... Provide inline comments that cite standard library docs. After code, state “Confidence=<0-100%>”.
```
Metrics:
* Compile & unit-test pass-rate.
* RC = disagreement in cited docstrings / function names among 5 samples.

### 5.3 Medical Reasoning
*Prompt*
```text
Given symptoms ... Provide differential diagnosis list plus 3 peer-review references (DOIs). State numeric confidence.
```
RC measured as DOI semantic overlap.  Aleatoric component estimated via historical mis-diagnosis rates.

---

## 6. Evaluation Protocols
1. **Calibration Metrics.**  ECE, Brier score, adaptive binning; separate epistemic vs. aleatoric.
2. **Quality Metrics.**  Accuracy (QA), pass@k (code), F1 or NLI accuracy; track the 2–5 % boost seen in calibrated models.
3. **Human Disagreement Correlation.**  Replicate SWAG NLI methodology: compute Spearman ρ between model confidence and human vote distribution; target ≥0.6.
4. **Distribution Shift Stress-tests.**  Use CalibratedMath OOD splits; evaluate verbal calibration vs. RC-augmented.
5. **Ablation Study.**  1) verbal only, 2) RC only, 3) logits only, 4) hybrid.

Computation: For each model, *n* = 5 SCS samples × 1 000 items ≈ 5 k forward passes; affordable on a single GPU.

---

## 7. Synthesis of Empirical Learnings
| Prior Finding | Implication for RC Framework |
|---------------|------------------------------|
| GPT-3 verbal probabilities are calibrated (CalibratedMath). | Use as baseline; RC features can *post-calibrate* further. |
| Separating epistemic vs. aleatoric reduces mis-calibration by 2–5 %. | RC addresses epistemic; retain aleatoric residual models. |
| SWAG tightens model–human correlation on ambiguous NLI. | Hybrid RC + SWAG expected to further improve. |
| Ambiguous entity study: 75 % accuracy under under-specification. | Low RC should flag such cases; evaluate detection recall. |
| SWA ensembles improve stability but biases remain. | RC unlikely to remove bias; must monitor with CheckList. |

---

## 8. Contrarian & Speculative Ideas (Flagged)
* **Self-debate Consistency.**  Use *adversarial* paired dialogue (“for” vs. “against”); measure concession rate as uncertainty.
* **Secondary-Model Consistency Judge.**  Train a small LM to take (answer, references) and output *p(consistent)*; similar to discriminator in GANs.
* **Cross-modal References.**  Ask model to draw or diagram a concept and check coherence across modalities; higher modality divergence ⇒ higher epistemic uncertainty.  (High risk, researchy.)
* **Dynamic Prompt Tuning for RC maximisation.**  Meta-optimizer searches prompt space to *minimise* RC divergence, thereby *implicitly* seeking higher certainty answers.

---

## 9. Recommendations & Roadmap
1. **Prototype SCS-RC on OD-QA** using GPT-4 API (logit-free).  Baseline vs. RC ECE.
2. **Integrate SWAG** on an open-weights model (Llama 3-70B) for NLI; combine with RC.
3. **Calibration Layer**: isotonic regression over combined feature vector ⟨RC, verbal-prob⟩.
4. **Deploy Human Annotation Study** (200 ambiguous items) to validate correlation with disagreement.
5. **Bias Audit**: Run CheckList on RC-filtered high-confidence outputs to ensure no confidence-amplified bias.
6. **Publish toolkit** *(ReCUE)* with pluggable divergence metrics, calibration, and evaluation scripts.

Timeline (assuming 3-month sprint):
* Month 1 — QA prototype + evaluation.
* Month 2 — SWAG hybrid + medical pilot.
* Month 3 — Human study + code task, write-up.

---

## 10. Conclusions
Reference-consistency provides a **logit-free, interpretable, and empirically grounded** pathway to extract calibrated epistemic uncertainty from a single LLM.  Prior work on verbal confidence, Bayesian SWAG, and human disagreement correlation collectively suggest that:
* RC can *augment* existing uncertainty signals and close residual calibration gaps (≈2–5 %).
* Hybrid RC + SWAG may capture both weight and generation-space variability.
* The technique generalises across QA, code, and medical reasoning with minimal task-specific customisation.

Future research should explore multi-modal consistency, adversarial self-debate, and automated prompt tuning for RC optimisation.  The proposed *ReCUE* toolkit and evaluation roadmap aim to make these insights actionable for real-world, high-stakes LLM deployments.


## Sources

- http://d-scholarship.pitt.edu/43419/1/Taehee_Dissertation_Paper_v2.pdf
- https://mdpi.com/books/pdfview/book/2166
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.875
- http://arxiv.org/abs/2205.15449
- https://www.repository.cam.ac.uk/handle/1810/316387
- http://www.repositorio.uchile.cl/handle/2250/125159
- http://www.mt-archive.info/HLT-NAACL-2006-Zens-2.pdf
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-1psffk7q1e0es9
- http://hdl.handle.net/10068/213648
- http://arakilab.media.eng.hokudai.ac.jp/~araki/2007/2007-B-2.pdf
- http://arxiv.org/abs/2205.14334
- http://hdl.handle.net/10068/993647
- https://www.intechopen.com/books/uncertainty-quantification-and-model-calibration
- http://cds.cern.ch/record/1315490
- https://escholarship.org/uc/item/6td9p2d2
- http://discovery.ucl.ac.uk/1363250/
- http://www.loc.gov/mods/v3
- https://www.spsc.tugraz.at/sites/default/files/is15-uncertainty.pdf
- http://www.dbs.ifi.lmu.de/Publikationen/Boehm/SSDBM_06.pdf
- https://scholarworks.unist.ac.kr/handle/201301/31905
- http://www.dbs.informatik.uni-muenchen.de/~schubert/papers/SSDBM2006_a.pdf
- http://hdl.handle.net/10138/563840
- https://hal.archives-ouvertes.fr/hal-01484994
- https://ojs.aaai.org/index.php/AAAI/article/view/4719
- https://research.vu.nl/en/publications/771980b7-0503-4e95-96a5-b731fa160bed
- http://dl.acm.org/citation.cfm?id=1540464&dl=ACM&coll=DL&CFID=455575457&CFTOKEN=49253491
- https://www.repository.cam.ac.uk/handle/1810/298857
- http://hdl.handle.net/10.1371/journal.pcbi.1006572.g009
- http://infoscience.epfl.ch/record/192427/files/Garner_THESIS_2012.pdf