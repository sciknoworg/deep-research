# Negative Questioning for Alignment Models to Reduce Hallucinations

## 1  Executive Summary
Negative questioning (NQ) is the deliberate use of *polarity-reversing* prompts, counter-factual queries and adversarially constructed hard negatives to surface, quantify and finally attenuate hallucinations produced by large language, vision–language and domain-specific generative models.  
This report synthesises findings from (i) contrastive‐learning literature (e.g. MixCSE, hard-negative curricula), (ii) recent hallucination benchmarks (Med-HALT, HaELM), (iii) psycholinguistic evidence on how humans process negative questions, and (iv) a seemingly orthogonal but instructive body of work on *biological* hallucinations and neuromodulation (rTMS in schizophrenia). The latter provides an analogue: parameter-sensitive interventions can shrink hallucination sub-space yet show heterogeneous response patterns predictable by structural biomarkers. 

Key take-aways:
* Treat NQ as **both a training signal and an evaluation probe**.  
* Hard-negative sampling (Li et al.; MixCSE) materially improves discriminative precision—an effect we can generalise to factuality tasks.  
* Benchmarking resources now exist (Med-HALT, HaELM) to measure hallucination suppression at scale and in high-risk regimes such as medicine.  
* Psycholinguistic evidence (ULB, Tilburg/Utrecht) suggests human cognition initially entertains *both* polarities, then pragmatically settles on the affirmative state; models may mirror or exaggerate this bias, offering a template for *contrastive reward shaping*.  
* Neuromodulation studies remind us that **dose, frequency and target selection** matter; by analogy, gradient magnitude, curriculum pacing and prompt selection are decisive hyper-parameters for NQ efficacy.  

We close with a concrete multi-phase roadmap: (a) dataset generation with structured NQs, (b) contrastive-policy fine-tuning, (c) multimodal evaluation with HaELM/Med-HALT and (d) biomarker-inspired latent state diagnostics.

---

## 2  Conceptual Foundations

### 2.1  Definition of Negative Questioning (NQ)
We adopt **NQ** as an umbrella term covering three granularity levels:
1. **Prompt-level polarity flips** – “What are the side-effects of tramadol?” → “What are *not* side-effects of tramadol?”
2. **Training-time hard negatives** – Explicitly label *false yet plausible* continuations and incorporate them in contrastive or RL objectives.
3. **Adversarial evaluation queries** – Post-training probes designed to elicit hallucinations by conflicting with retrieved evidence.

### 2.2  Human Processing of Negative Questions
Eye-tracking evidence (ULB 2020; Tilburg & Utrecht 2016-17) shows that listeners temporarily represent *both* the positive and negative proposition when faced with a negative question, then bias toward the positive hypothesis. This two-stage dynamic parallels model behaviour: LLMs generate a superposition of candidate continuations before sampling. Implication: **Contrastive objectives that hold both polarities in memory then suppress the incorrect one are cognitively-plausible and empirically validated**.

---

## 3  State of the Art in Hallucination Control

### 3.1  Hard-Negative Contrastive Learning
* **Li et al. (Hard Negative Entities, EMNLP 2022)**: Explicit hard negatives improve entity set expansion; reproduced successfully, confirming transferability of the technique.  
* **MixCSE (AAAI 2022)**: Dynamically mix hard negatives with randomly sampled negatives; yields SOTA sentence embeddings without labelled data—suggests a scalable recipe.

### 3.2  Current Medical Benchmarks
* **Med-HALT (EMNLP 2023)**: Multilingual, reasoning versus memory sub-tasks; reveals open-source models (Llama-2, MPT, Falcon) underperform GPT-3.5/Davinci-003 → high safety risk.  
* **HaELM (2023)**: LLM-driven hallucination metric for VLMs—95 % agreement with ChatGPT, locally deployable.

### 3.3  Prompt-time Guardrails
* Retrieval-augmented generation (RAG) with *false premise detector*—yet suffers from exposure bias.  
* Post-hoc filtering via fact-checkers.

**Limitation**: Pure generation guardrails often fail under distribution shift; thus NQ is proposed as a *training-level alignment* instrument rather than a brittle inference-time patch.

---

## 4  Integrating Negative Questioning into Alignment Pipelines

### 4.1  Data Curation Strategy
1. **Polarity-paired corpora**: Construct `{positive, negative}` question pairs with shared evidential context (e.g. SNOMED triples, Wikipedia citations).
2. **Adversarial rewriters**: Use a *white-box* LLM to mutate answer segments into near-miss false claims.
3. **Curriculum shaping**: Begin with strongly differentiated pairs → gradually shrink lexical distance, analogous to increasing rTMS frequency.

### 4.2  Algorithmic Techniques
1. **Contrastive Reward Modelling (CRM-NQ)**  
   *Objective*: Maximise log-odds that model prefers truthful to hallucinated answer given a negative-question pair.  
   *Implementation*: Use MixCSE recipe; treat truthful answer as anchor, hallucinated answer as hard negative.
2. **Reinforcement Learning from Negative Questions (RLNQ)**  
   *Reward*: +1 if model provides *consistent* answers across polarity flips; penalise factually divergent or logically inconsistent continuations.
3. **Latent Consistency Regulariser**  
   Encourage cosine alignment between hidden states of `{Q+, A+}` and `{¬Q, A+}`; empirically lowers hallucination rate (speculative—needs testing).

### 4.3  Evaluation Framework
* Run cross-domain tests: general (TruthfulQA), medical (Med-HALT), multimodal (HaELM).  
* Track *delta-hallucination* when toggling question polarity; large swings indicate unreliability.

---

## 5  Cross-Disciplinary Lessons from Neuro-Modulation Studies

While rTMS/clozapine trials in schizophrenia target *biological* hallucinations, several insights map surprisingly well to alignment:

| Neuro finding | Alignment Analogy | Actionable Takeaway |
|--------------|-------------------|---------------------|
| **NNT = 9** for auditory hallucinations despite null overall PANSS | Hallucination reduction may appear small in aggregate metrics (BLEU, perplexity) yet large in tail-risk safety | Measure *hallucination-specific utility*, not only average perplexity. |
| **Dose × frequency critical** (1 Hz × 30 vs cTBS × 10) | Curriculum length, gradient update frequency and negative-sampling rate are decisive | Tune negative-sample ratio as a hyper-parameter. |
| **Structural MRI predictor (85 % BAC)** identifies responders | Latent-state probes (e.g. probing heads, attention entropy) might predict which prompts induce hallucination | Build *prompt-state biomarkers* to gate high-risk generations. |
| **Left arcuate fasciculus integrity linked to benefit** | Analogous to *parameter sub-space* where model stores factual memory | Use *low-rank adapters* targeted at knowledge-dense layers for NQ fine-tuning. |

---

## 6  Proposed Research Agenda (12 months)

### Phase 1  Dataset & Instrumentation (Months 0-2)
* Mine polarity-paired Q/A from Wikipedia, biomedical QA, StackExchange.  
* Generate adversarial hallucinations via rule sets plus GPT-4 sampling.  
* Instrument HaELM/Med-HALT into continuous evaluation pipeline.

### Phase 2  Baseline Re-Implementation (Months 2-4)
* Reproduce Li et al. hard-negative objective on entity-expansion tasks.  
* Port objective to factual QA (closed-book subset of Natural Questions).

### Phase 3  Contrastive Fine-Tuning (Months 4-7)
* Experiment grid: negative ratio {5, 10, 20 %}, curriculum slope {linear, cosine}, loss {NT-Xent, InfoLOOB}.  
* Measure hallucination delta on Med-HALT.

### Phase 4  RLNQ & Consistency Regularisation (Months 7-9)
* Implement PPO-style RL with polarity consistency reward.  
* Add latent-state regulariser; evaluate with attention entropy diagnostics.

### Phase 5  Multimodal Extension (Months 9-12)
* Fine-tune MiniGPT-4 on HaELM with CRM-NQ objective.  
* Analyze modality-specific failure cases (image hallucinations vs text).

Deliverables: open-source checkpoints, scripts for dataset generation, live leaderboard, ablation study report.

---

## 7  Contrarian & Speculative Ideas

1. **Zero-Shot Neuro-Symbolic Introspection** *(speculative)*  
   Equip model with a *self-query* head that answers “Is this claim entailed by retrieved evidence?”; train the head with NQ contrastive loss.
2. **Gradient-Surgery on Hallucination Sub-Space**  
   Use low-rank adaptation vectors aligned with high-hallucination prompts; orthogonally project standard LM gradients to avoid catastrophic forgetting.
3. **sMRI-Inspired Layer Pruning** *(highly speculative)*  
   Remove or dampen layers analogous to low-integrity tracts in neuro studies, i.e., layers whose activations correlate with hallucination metrics.

---

## 8  Risk Analysis & Mitigations

| Risk | Example | Mitigation |
|------|---------|-----------|
| Over-regularisation → knowledge loss | Model refuses benign queries | Monitor F1 on open-book QA; introduce *selective* NQ penalties. |
| Adversarial over-fitting | Model memorises dataset artefacts | Use diverse NQ generation, hold-out domains. |
| Evaluation leakage | HaELM prompts seen during tuning | Strict data split, continuous addition of unseen probes. |

---

## 9  Implementation Roadmap for a Production System
1. **Offline**: Fine-tune base model with CRM-NQ objective.  
2. **Edge Safety Layer**: Deploy real-time NQ probes on sampled outputs; if inconsistency > τ, trigger retrieval fallback.  
3. **Telemetry**: Log latent-state biomarkers; feed into drift detection.  
4. **Periodic Re-alignment**: Weekly RLNQ refresh using newly logged queries.

---

## 10  Conclusion
Negative questioning offers a principled, empirically grounded path to shrink hallucination propensity in generative models. The approach aligns with human cognitive processing, leverages proven hard-negative contrastive methods, and can be evaluated with modern benchmarks like Med-HALT and HaELM. Cross-disciplinary insights from neuromodulation underscore the importance of parameter tuning, responder stratification and biomarker development. A structured 12-month agenda can operationalise these insights into safer, more reliable AI systems.


## Sources

- https://dspace.library.uu.nl/handle/1874/351319
- http://schizophreniabulletin.oxfordjournals.org/content/early/2011/11/17/schbul.sbr154.full.pdf
- http://arxiv.org/abs/2308.15126
- http://orcid.org/0000-0003-2873-8667
- https://figshare.com/articles/_Activations_for_the_contrast_reward_anticipation_versus_no_outcome_for_healthy_controls_gt_schizophrenia_patients_/1349891
- http://arxiv.org/abs/2202.09662
- http://arxiv.org/abs/2309.05217
- https://research.tilburguniversity.edu/en/publications/43231a4a-c5e6-4264-9168-d4682327f0ec
- https://archive-ouverte.unige.ch/unige:98031
- https://ojs.aaai.org/index.php/AAAI/article/view/21428
- http://dx.doi.org/10.1038/s41398-024-02903-1
- https://zenodo.org/record/7641552
- https://hal.science/hal-03862836/document
- https://hal.sorbonne-universite.fr/hal-02125141/file/document.pdf
- http://arxiv.org/abs/2307.15343
- https://archive-ouverte.unige.ch/unige:74220
- http://hdl.handle.net/1807/103056
- https://ojs.aaai.org/index.php/AAAI/article/view/26539
- http://www.loc.gov/mods/v3
- http://edoc.mdc-berlin.de/16808/
- https://dare.uva.nl/personal/pure/en/publications/positive-and-negative-polar-questions-in-discourse(dda1c07a-e3ce-4297-a4e7-1b580962dad0).html
- https://espace.library.uq.edu.au/view/UQ:718b439
- https://hdl.handle.net/11370/79631b43-bd9d-46f9-8097-162dc02923cd
- http://hdl.handle.net/10261/74483
- https://eprints.umm.ac.id/90754/1/Similarity%20-%20Karisma%20Zulfany%20yuniardi%20Latipun%20-%20Negative%20reinforcement%20reward%20behavior%20therapy%20schizophrenia.pdf
- http://dspace.library.uu.nl/handle/1874/338442
- http://www.rcaap.pt/detail.jsp?id=oai:agregador.ibict.br.RI_USP:oai:www.producao.usp.br:BDPI/21196
- http://arxiv.org/abs/2202.03629
- https://zenodo.org/record/7585083
- http://hdl.handle.net/10.3389/fpsyg.2023.937656.s002
- http://www.theses.fr/2018NANT2010/document
- http://www.theses.fr/2020PA080039/document
- http://orcid.org/0000-0002-2072-9216
- http://hdl.handle.net/10.3389/fpsyg.2023.937656.s001
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/333699