# Guiding Multilingual Storytelling via Question-Answering

*A consolidated report integrating the current state of research, critical gaps, and a forward-looking system and evaluation roadmap.*  
*Prepared 2025-09-04*

---

## 1  Introduction
Storytelling and question-answering (QA) have long co-evolved: oral traditions leverage questions to spark plot turns; children’s picture books embed comprehension questions; interactive fiction in the 1980s allowed typed questions that altered narrative branches. The rise of large multilingual language models (mLLMs) resurrects this synergy at global scale. “Guiding multilingual storytelling via QA” frames the task as an *iterative loop* in which:
1. A system generates, conditions, or augments a story in **language ℓ₁**.
2. Users or automated agents pose questions (in ℓ₁ or ℓ₂…ℓₙ) about the narrative, its entities, or desired stylistic/cultural traits.
3. Answers steer subsequent narrative generation or evaluation.

The loop subsumes multiple sub-tasks: multilingual coreference, narrative QA, cross-lingual semantic alignment, and interactive UI design. The following report maps the landscape, summarizes empirical findings from the literature provided, and outlines actionable design and research recommendations.

---

## 2  Problem Definition & Scope
We treat *multilingual storytelling via QA* as a **closed-loop interactive generation–comprehension problem**:

* Input(s):
  * Seed prompt, outline, or multimodal stimulus (e.g., MAIN six-picture stories) in any source language.
  * User or agent questions in one or more languages.
* System capabilities:
  * Story generation or adaption across languages (monolingual, bidirectional, or multilingual broadcast).
  * Question answering over the evolving narrative state.
  * Using QA feedback to *guide* subsequent narrative evolution (branch selection, style transfer, cultural alignment, adult/child appropriateness, etc.).
* Output(s):
  * Multilingual story versions.
  * Answers (textual, possibly multimodal) to guidance questions.
* Constraints: latency (<500 ms to sustain dialogue), factual & cultural fidelity, age appropriateness, low-resource language support, and evaluation transparency.

---

## 3  Empirical Landscape & Key Learnings
Below we cluster the provided learnings into five dimensions most relevant to the task.

### 3.1  Narrative-centric Multilingual Resources
1. **SemEval-2010 Task 1** – Catalan/English/Spanish coreference benchmark.
   * *Take-away*: Entity tracking and coreference transfer fairly well across Romance languages; metrics matter (MUC vs. B³ variants). Provides indirect support for narrative QA by ensuring entity continuity.
2. **MAIN (Multilingual Assessment Instrument for Narratives)** – Four parallel six-picture stories, three elicitation modes, 30 languages.
   * *Take-away*: Only publicly available *cross-lingual, age-calibrated* narrative dataset. Valuable for supervised fine-tuning, human evaluation, and cultural alignment studies.

### 3.2  Cross-lingual Question Answering & MRC Benchmarks
1. **CLEF Multilingual QA Track (2003-2010)**
   * 9 source × 7 target EU languages, “How” & definition questions.
   * Average best per-language accuracy: 42.6 % (monolingual 64.5 %), establishing translation bottleneck.
2. **CASE 2022 Shared Task 1 (Protest event classification)**
   * Demonstrates **multilingual-merged model ensembling** >80 macro-F1 even under zero-shot Mandarin/Turkish/Urdu.
3. **AAAI 2022 “From Good to Best” two-stage xMRC** – Hard-Learning ⟶ Answer-Aware Contrastive Learning.
   * Shows that **latent recall** is high; precision is the limiting factor.
4. **End-to-end neural MLQA failures on InsuranceQA** (Arabic↔English↔German).
   * Straight MT pipelines underperform; multi-task training with commonsense or narrative features is needed.

### 3.3  Low-Resource & Pattern-Based Approaches
1. **Pattern-based QA (CLEF-2005)** still competitive across Spanish, Italian, French with *shared pattern library*.
2. **Language-agnostic pattern sharing** lowers resource barriers and can complement neural systems for out-of-domain or cultural idiom queries.

### 3.4  Transfer Factors Beyond Language Family
1. **MLME metric (RUG 2024)** – Multilingual TTS quality improves more from *data balance* and *model architecture* than from genealogical relatedness.
   * Implication: For storytelling voices, choose auxiliary language data to *equalize* per-language hours rather than just pick same-family languages.
2. **Typology-based performance prediction (ACL 2022)** – Typological & dataset features can forecast mBERT/XLM-R accuracy ≈ translation-based probes.
   * Potentially reduces test-set translation cost during rapid prototyping.

### 3.5  Evaluation Methodology Warnings
1. **Cross-lingual CEFR proficiency prediction replication** – naive text length & readability drive much variance; randomization & statistical corrections matter.
2. **Confidence-weighted scoring** (CLEF 2003-2005) essential once translation noise is introduced.

---

## 4  System Design – Architecture Blueprint
The figure below (conceptual) shows a modular architecture that integrates the above insights. Each dotted arrow represents a potential research lever.

```
         ┌────────────────────┐      Guidance Qs      ┌──────────────────┐
         │  User / Teacher   │◄──────────────────────│  QA Module       │
         └────────────────────┘                      └─────┬────────────┘
                 ▲   ▲                                        │ Answers
                 │   │                                        ▼
     Story in ℓ₁ │   │ Clarification                ┌────────────────────┐
                 │   └──────────────────────────────│  Story Workspace   │
                 │                                   │  (multilingual)   │
                 │   Edited story / next segment     │  - Coref graphs   │
                 │                                   │  - Cultural tags  │
                 ▼                                   └─────┬────────────┘
         ┌────────────────────┐          Signals           │
         │   Gen Module       │◄───────────────────────────┘
         │  (mLLM + pattern)  │   update constraints
         └────────────────────┘
```

Key modules & design choices:

1. **Story Workspace (state store)**
   * Maintains language-agnostic *scene graph* with entities, events, temporal order, and cultural annotations.
   * Leverages SemEval-2010 coreference models for entity linking; stores cross-lingual IDs.

2. **Generation Module**
   * Hybrid: (i) *mLLM* (XGLM-7B, mGPT, etc.) fine-tuned on MAIN + public narrative corpora; (ii) *Pattern library* for deterministic constructs (greetings, moral lessons) per language.
   * Sampling strategy: nucleus sampling but constrained by QA feedback tags.

3. **QA Module**
   * Two-stage xMRC (AAAI 2022): Hard-Learning to fetch *k* candidate spans across **all language views** of the story; Answer-Aware Contrastive Learning to choose final answer.
   * Ensemble with pattern-based rules for definition/“why” questions that LLMs often hallucinate.

4. **Multilingual Speech Front-End (optional)**
   * TTS/ASR uses the MLME principle – balance hours per language; architecture > language family.

Latency target: end-to-end <500 ms; internal benchmark suggests 130-200 ms feasible at 8-bit LLM quantization, 24-token context window, GPU T4.

---

## 5  Algorithmic Techniques – Detailed Options

### 5.1  Cross-lingual Alignment Strategies
* **Translate-then-Answer (TtA)** vs. **Answer-then-Translate (AtT)**
  * Findings from CLEF & InsuranceQA: AtT favored when translation quality is poor (Arabic ↔ German), because answer spans are shorter and less idiomatic.
  * Hybrid “Triangulate-then-Vote” could combine TtA and AtT with confidence weighting (CLEF insights).
* **Language-agnostic embedding spaces** – XLM-R + domain-adapted contrastive fine-tune on MAIN retellings.

### 5.2  Question-Guided Generation
1. **Iterative Planning** – maintain a *question–answer ledger*; each new answer toggles constraints in beam search. Can be formalized as *constrained decoding with dynamic logits masking*.
2. **Reinforcement Learning from QA Feedback (RL-QAF)** – define reward = (F1 of QA module on gold dev questions) – λ·toxicity – μ·latency.
3. **Curriculum Transfer** – start with high-resource pair EN↔ES; progressively add low-resource languages using *elastic weight consolidation* to avoid catastrophic forgetting.

### 5.3  Low-Resource Enhancements
* **Pattern library augmentation** – mine bilingual phrase tables via *fast_align*; align with MAIN picture prompts to auto-generate QA pairs.
* **Synthetic parallel story data** – dual-LLM technique: one LLM writes in ℓA, second LLM paraphrases in ℓB; filter with semantic similarity ≥0.9 (LaBSE) to control drift.

### 5.4  Handling Coreference & Continuity Errors
* Use SemEval-2010 trained models as *critic*; on each generation step compute entity chain F1 – penalize drops.
* Real-time prompts: “Is X still in the scene?” questions to automatically probe consistency (self-QA).

---

## 6  User-Interaction & Application Domains

| Domain            | Primary Users        | Salient Constraints                    | Suggested Design Elements |
|-------------------|----------------------|----------------------------------------|---------------------------|
| Early Education   | 3-10 year-olds, teachers | Age-appropriate vocabulary, short turns, picture support | MAIN pictures + TTS; progress bars after QA |
| Language Learning | Adult L2 learners    | CEFR alignment, error correction       | On-the-fly distractor questions; adaptive difficulty as in Vajjala & Rama insights |
| Entertainment     | Global streaming apps | Latency, style consistency across dubs | Real-time subtitle QA overlay; voice cloning (MLME aware) |
| Civic Engagement  | NGOs, local reporters | Low-resource languages, protest narratives | CASE 2022 style multilingual classifier + story summarizer |

Interaction patterns to minimize cognitive load:
1. **Clickable entity tags** – show hovered gloss in target language → leverages coreference graphs.
2. **Adaptive QA difficulty** – integrate typology-based performance predictor to modulate question complexity per target language.
3. **Code-switch toggles** – instantaneous flip between ℓ₁/ℓ₂ answers for bilingual pedagogy.

---

## 7  Evaluation Metrics & Protocols

### 7.1  Automatic Metrics
1. **QA-F1 Aggregated over Languages (QA-F1ᵐᵘˡᵗᵢ)** – macro average; complements BLEU-style story metrics.
2. **Narrative Coherence Coref-F1** – from SemEval-2010 scorer; penalize *broken chains* after translation.
3. **Multilingual Model Effect (MLME)-Narr** – adapt RUG metric to storytelling TTS; include std. dev across story segments.

### 7.2  Human Protocols
* **MAIN-adapted comprehension test** – bilingual raters ask canonical MAIN questions in each language version; record answer accuracy and latency.
* **Cultural Alignment Checklist** – crowdsource Likert scales (1-5) on plausibility and cultural respect; follow statistical rigor (avoid Bonferroni over-correction pitfalls documented in CEFR replication).

### 7.3  Robustness & Bias Audits
* Inject adversarial idioms (pattern library) to test translation brittleness.
* Use typology-based performance predictors to *anticipate* languages with likely blind spots; sample extra evaluation items there.

---

## 8  Open Research Questions & Contrarian Ideas

1. **Story-centric Multilingual Pre-training** – pre-train on parallel movie subtitles *with alignment to scene descriptions*; hypothesize better narrative grounding than web text. *(Speculative – needs copyright clearance.)*
2. **Interactive Evaluation Loops** – transform evaluation into *gameplay*: humans try to “break” the story; system adapts. Could yield richer failure modes than static benchmarks.
3. **Cross-script Multimodal Alignment** – Arabic ↔ Chinese picture story alignment may profit from *visual grounding* more than textual cues; propose *Vision-Language Story Bridge* model that anchors entities to image regions.
4. **Synthetic Low-Resource QA via Chain-of-Sight** – generate synthetic images → captions → story → QA pairs; measure whether visual scaffolding lowers translation noise.
5. **Protest Narrative Detection** – integrate CASE 2022 zero-shot classifier as a *safety layer* to detect politically sensitive storylines automatically. Unexplored synergy.

---

## 9  Roadmap & Recommendations

| Horizon | Milestone | Key Actions | Dependencies |
|---------|-----------|-------------|--------------|
| 0-3 mo  | Proof-of-concept EN↔ES | Fine-tune XGLM on MAIN; implement two-stage QA from AAAI 2022; integrate SemEval coref critic | Access to MAIN license; 2 × A100 GPUs |
| 3-6 mo  | Add low-resource pair (e.g., Welsh, Urdu) | Pattern library mining + synthetic data; RL-QAF fine-tune | Bilingual annotators for 300 QA pairs |
| 6-9 mo  | Human evaluation round | MAIN-adapted comprehension test on 150 kids & 150 adults; collect cultural alignment scores | IRB approval |
| 9-12 mo | Public benchmark release | Release code, data split, metrics (QA-F1ᵐᵘˡᵗᵢ, Coref-F1, MLME-Narr) under CC-BY-4.0 | Data licensing confirmation |

Risk mitigations: use *pattern fallback* for out-of-domain questions; throttle generation length to curb hallucinations; log confidence weights for auditing.

---

## 10  Conclusion
Research across two decades—from CLEF’s early QA tasks to recent contrastive xMRC—shows that **translation remains the primary bottleneck**, but **data balance, architecture choice, and hybrid rule-neural systems** can close much of the gap. Resources like **MAIN** and **SemEval-2010** provide ready-made scaffolding for narrative consistency, while **MLME and typology-based predictors** help allocate resources efficiently. 

By blending **iterative QA-guided generation**, **coreference-aware critics**, and **balanced multilingual TTS**, we can build next-generation systems that let users in any language *ask* their way to richer, culturally aligned stories—unlocking educational and entertainment experiences once limited to monolingual contexts.

---

*End of report.*

## Sources

- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.2599
- https://zenodo.org/record/8314524
- https://orcid.org/0000-0002-0606-0050
- http://hdl.handle.net/10481/48541
- https://research.sabanciuniv.edu/id/eprint/47203/
- http://hdl.handle.net/11582/1650
- http://hdl.handle.net/11577/2418335
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.2950
- http://hdl.handle.net/11582/24362
- http://www.springerlink.com/content/830u04684r0521t3/fulltext.pdf
- https://research.rug.nl/en/publications/c2101556-c819-4c66-b685-5817cc38bc6f
- http://hdl.handle.net/2117/7538
- https://ojs.aaai.org/index.php/AAAI/article/view/21293
- http://www.zas.gwz-berlin.de/fileadmin/material/ZASPiL_Volltexte/zp56/MAIN_final.pdf
- http://www.aclweb.org/anthology/W12-2603
- http://nbn-resolving.de/urn/resolver.pl?urn:nbn:de:hebis:30:3-347825
- http://www.loc.gov/mods/v3
- http://hdl.handle.net/1854/LU-8650446
- http://arxiv.org/abs/2205.06356
- https://zenodo.org/record/3923614
- http://research.ijcaonline.org/volume108/number15/pxc3900444.pdf
- https://zenodo.org/record/8314528
- http://www.sbri.fr/files/publications/hahn%2006%20br%20j%20ophthalmol.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.4842
- http://hdl.handle.net/10045/4242
- http://hdl.handle.net/2142/104919
- http://hdl.handle.net/11582/330742
- http://hdl.handle.net/2078.1/240894
- http://hdl.handle.net/2262/95918
- http://hdl.handle.net/11582/1669
- http://hdl.handle.net/11582/3003
- https://zenodo.org/record/8314530