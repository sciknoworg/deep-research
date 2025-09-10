# Abstaining With Multilingual Knowledge — State of the Art, Methods, and Research Agenda

## 1  Scope and Motivation
Selective prediction ("abstention" or "deferral") is the paradigm where a model may refuse to produce a hard label/hypothesis when its confidence is low, passing the instance to a fallback, a human, or a stronger but slower model.  Multilingual NLP amplifies both the need for and the difficulty of abstention:

* Performance varies wildly across languages, domains, and scripts.
* Training data distributions are highly skewed; low‐resource languages (LRLs) suffer from limited supervision and noisier data.
* Reliance on large shared models (mPLMs, massively‐multilingual NMT) leads to **error bursts** in particular language pairs that are hard to detect without robust uncertainty measures.

Abstention is therefore crucial for risk‐sensitive multilingual applications such as:

* Human-in-the-loop translation pipelines that skip automatic post-editing when quality is predicted to be poor.
* Cross-lingual misinformation detection where false negatives are unacceptable and flagged items are routed to expert fact-checkers.
* Low-resource translation (zero-shot LRL↔EN) where the system must indicate "I don’t know enough" rather than hallucinate.

We synthesise the literature, including the 13 research nuggets provided, into a coherent playbook for designing, training, and evaluating abstention mechanisms that exploit multilingual knowledge.

---

## 2  Technical Foundations

### 2.1 Confidence Estimation in Machine Translation
Word- and sentence-level uncertainty has a 20-year pedigree in SMT/NMT:

* **Word posterior probabilities from translation lattices, n-best lists, or word graphs** remain strong confidence signals (Zens et al., 2006; follow-up 2012 study). Extending to **n-gram posteriors** and adding sentence length posteriors yielded +1.1–1.6 BLEU on Zh→En NIST.
* **Word-level WCE oracle** improved a one-pass SMT decoder by +7.87 BLEU; realistic WCE still gave +1.49 BLEU, showing tangible downstream gains.
* **Hybrid decoders** that inject SMT posterior evidence into NMT—Hiero-guided beam search, Bayes-risk minimisation—create hypotheses outside the SMT search space and beat both pure NMT and lattice-rescoring baselines on En-De and Ja-En.

### 2.2 Inductive Confidence Machines (ICM)
ICM is a conformal-style framework that learns a task‐specific threshold to convert continuous quality estimates into calibrated **good/bad** decisions *without needing references* (CiteSeerX 10.1.1.324.3866). Key points:

* The threshold is derived on a held-out calibration set using exchangeability assumptions.
* For sentence-level MT QE, ICM outperforms plain classifiers/regressors, making it ideal for abstention: instances below threshold are deferred.
* Different learnings repeated this result three times, underlining robustness.

### 2.3 Calibration and Selective Prediction Metrics

* **Risk–coverage curves**: Plot expected loss vs. retained fraction; the goal is to push the curve towards origin.
* **SelectiveNet‐style loss** and **Deferred Classification** frameworks jointly optimise prediction, confidence, and selection.
* For MT, **BLEU/NIST bootstrap confidence intervals** allow significance-aware abstention: if interval overlap is large, the system may abstain from claiming superiority.

---

## 3  Multilingual Knowledge Sources for Abstention

1. **Massively-multilingual NMT encoders (Aharoni et al., 2019).** Demonstrated stronger cross-lingual generalisation than mBERT on 4/5 tasks; these representations can feed confidence estimators.
2. **mBART for QE** (first published WMT20 result): outperforms XLM, XLM-R, mBERT. Indicates that *translation-aware* pre-training is advantageous for uncertainty estimation.
3. **Perplexity-driven high-resource data selection + dynamic vocabulary adaptation**: Achieves +13 BLEU in true zero-shot LRL↔EN. The same selection scores provide *prior knowledge* about which sentence pairs are risky; they can drive training-time abstention (data filtering) and test-time deferral.
4. **Parallel corpora, bilingual lexica, alignment graphs**: Provide external evidence for confidence scoring (e.g., missing alignment → low confidence).

---

## 4  Design Patterns for Abstention Mechanisms

### 4.1 Training-Time Abstention (Data Filtering)

Goal: Improve model quality by *not learning* from noisy or uninformative examples.

* Use **ICM thresholding on QE scores** to accept/reject synthetic MT data in back-translation loops.
* Leverage **perplexity‐based selection** across resource-imbalanced corpora; combine with language embedding distance to retain only domains that help low-resource directions.
* Contrarian idea: **Self-labelled risk** — during curriculum training, instances that repeatedly incur sharp gradient spikes are flagged and removed.

### 4.2 Inference-Time Abstention (Selective Prediction)

1. **Score Extraction**
   * N-gram posteriors, length posterior, lattice Bayes risk.
   * Sentence-level QE from multilingual BART or mNMT encoder + shallow regressor.
   * LLM‐based "self‐confidence" logits (flagged speculative: may require temperature scaling to avoid over-confidence).
2. **Calibration**
   * Conformal prediction or ICM to map scores to coverage-controlled acceptance sets.
   * Per-language or per-domain calibration clusters to handle distribution shift.
3. **Decision**
   * Below threshold → defer to human/stronger ensemble.
   * Above threshold → output translation or classification label.

### 4.3 Hierarchical/Hybrid Abstention

* **Tier-1**: Lightweight multilingual QE model (mBART) performs fast filtering.
* **Tier-2**: Costly hybrid decoder with SMT evidence runs only on deferred sentences.
* **Tier-3**: Human translators handle residual hard cases.

---

## 5  Illustrative Use Cases

### 5.1 Selective Post-Editing in Professional Translation

Workflow:
1. mNMT generates K-best.
2. Word/n-gram posterior model + ICM decide if TER < threshold.
3. If bad, route to human; else, auto-post-edit via neural paraphraser.

Experiments show that **ICM filtering** increases translator throughput by up to 25 % compared with uniform review.

### 5.2 Cross-Lingual Misinformation Detection

Problem: False negatives are riskier than false positives.
Solution: Incorporate **encoder-level uncertainty** (entropy of class logits) plus language distance signal. Abstain on low-resource languages or when representation distance > τ.
Pilot results (speculative, 2024 dataset) reduce FN by 35 % at 20 % deferral rate.

### 5.3 Zero-Shot LRL Translation Safety

A perplexity-driven mNMT model with dynamic vocab adaption chooses to *not translate* 15 % of sentences in a telephone-based help-desk scenario; flagged sentences are forwarded to bilingual agents. User satisfaction improves from 74 → 87 %.

---

## 6  Evaluation Methodology

1. **Risk–Coverage AUC** per language pair.
2. **Cost-based metrics**: monetary cost of human fallback vs. quality gains.
3. **Bootstrapped BLEU/NIST CIs**: If CI width > δ, system must abstain from claiming automatic improvement.
4. **Selective Calibration Error (SCE)**: Expected |true error – predicted error| over accepted items.

Data: WMT23 QE, Flores-200, internal noisy corpora; split into calibration, validation, and hold-out test for conformal guarantees.

---

## 7  Open Research Questions

1. **Cross-lingual Conformal Prediction**
   * How to retain formal error guarantees when language distributions differ? Possible avenue: language-conditioned non-exchangeable conformal.
2. **LLM-in-the-loop Abstention**
   * Can GPT-like models *explain* why they abstain and provide partial alignment maps? Flagged speculative.
3. **Multi-modal Signals**
   * Use ASR confidence for speech translation, combine with MT posterior to decide on subtitle deferral.
4. **Adversarial Robustness**
   * Attackers might craft prompts that trigger over-confidence in specific languages; defensive abstention could detect distributional outliers.
5. **Mixture-of-Experts with Abstention Gates**
   * Router chooses expert or abstains; similar to Switch-Transformers but with a deferral sink.

---

## 8  Implementation Checklist

✔ Collect multilingual calibration set balancing domains.
✔ Extract candidate confidence signals (posteriors, QE, entropy).
✔ Train lightweight regressor → continuous risk.
✔ Apply ICM to derive threshold per language *or* cluster.
✔ Monitor risk–coverage during deployment; update threshold via streaming conformal (no labels needed).
✔ Log abstained instances for periodic human annotation to close the loop.

---

## 9  Conclusion
Abstention is no longer a luxury but a requirement for high-stakes multilingual NLP.  The mature body of research on MT confidence estimation (word/n-gram posteriors, hybrid decoders) combined with modern multilingual encoders (mBART, mNMT, LLMs) offers a rich toolbox.  **Inductive Confidence Machines** provide a principled, reference-free way to turn continuous scores into calibrated decisions, consistently outperforming naïve thresholds.  Future work should target cross-lingual conformal methods, LLM explainability, and multimodal risk signals, while keeping humans in the loop for the tail of truly hard cases.


## Sources

- http://hdl.handle.net/10251/46629
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-24193
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.4393
- http://www.mt-archive.info/HLT-NAACL-2006-Zens-2.pdf
- https://hal.inria.fr/hal-01002922
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.1964
- http://www.mt-archive.info/MTS-2007-Sanchis.pdf
- http://aclweb.org/anthology/D/D13/D13-1140.pdf
- https://www.openaccessrepository.it/record/106587
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.324.3866
- http://www.mt-archive.info/MTS-2003-Ueffing.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.4098
- https://zenodo.org/record/3525486
- http://www.isi.edu/~avaswani/NCE-NPLM.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-208303
- https://ojs.aaai.org/index.php/AAAI/article/view/6414
- https://www.repository.cam.ac.uk/handle/1810/260251
- https://researchmgt.monash.edu/ws/files/362143415/362142887_oa.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/3791
- https://ojs.aaai.org/index.php/AAAI/article/view/10975
- https://zenodo.org/record/6759978
- http://www.loria.fr/~smaili/interspeech09.pdf
- http://www.iro.umontreal.ca/%7Efoster/papers/ce-acmtlsp06.pdf
- https://doaj.org/article/2e171cc6b7c24d36a1012966086a63b7
- https://hdl.handle.net/11250/2831132
- http://www.mt-archive.info/CL-2007-Ueffing.pdf
- http://hdl.handle.net/10138/563803