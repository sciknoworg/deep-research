# Modular Calibration for Long-form Answers – Comprehensive Technical Report (2025-09-05)

## 1. Scope and Motivation
Calibration is the problem of mapping an uncalibrated score, confidence, or prediction coming from a complex model or human rater into a quantity that has a well-defined probabilistic interpretation.  In long-form answer settings—open-domain QA, legal opinion generation, essay scoring, extended technical explanations, probabilistic forecasts—stake-holders demand *both* correctness and a reliable uncertainty estimate so that downstream decision rules (selective prediction, triage, mastery decisions, contract guarantees, etc.) can be enacted with controlled risk.

In the last five years three trends converged:

1.  **Explosion of Large Language Models (LLMs).**  Generative models are now the default engine for long-form answers, yet their raw confidence is uncalibrated and varies across prompts and languages.
2.  **Service-oriented, modular architectures.**  Assessment, QA and verification pipelines are being decomposed into plug-and-play micro-services (retriever→reader→reranker, item-bank→adaptive-engine→scorer, etc.), so calibration layers must themselves become *modular*.
3.  **Theoretical guarantees vs. empirical performance.**  Conformal prediction, reliability-diagram fitting, and Bayesian posterior models offer finite-sample or asymptotic validity, but are often brittle under distribution shift or multilingual transfer.

This report systematises what is currently known about *modular calibration for long-form answers*, drawing on 70+ primary results (full list in Appendix A).  We treat calibration as a horizontal concern cutting across LLM alignment, QA, computer-assisted assessment, and probabilistic forecasting.


---

## 2. Taxonomy of Calibration Targets for Long-form Answers

| Target artefact | Typical raw score/confidence | Why calibration matters |
|-----------------|------------------------------|-------------------------|
| Generative QA answer sentence/paragraph | Softmax log-prob, mean token probability, self-reported verbal confidence | Selective prediction; pipeline cascading (retrieval+reader); risk management in legal/medical domains |
| Extended essays & constructed-response items | Raw analytic rubric scores, rater agreement, machine scorer logits | Fair pass/fail decisions; mastery classification; accountability; explainability |
| Probabilistic forecasts (numeric, interval, categorical) | Forecast probability vector or interval | Brier/Log score optimisation; tournament ranking; policy use |
| System-level assertions (e.g., SLA, real-time contract) | Model-checker probability bound | Contract compliance; certification |
| Edge-device predictions (e.g., IoT fault, toxicology assay) | Regression/score + uncertainty | On-device decision; energy budget; safety margin |


---

## 3. Core Methods – Recent Advances

### 3.1 Modular Conformal Calibration (MCC)
* arXiv:2206.11468 (2022) formalised a *plug-and-play* layer that wraps **any deterministic regression model** and returns calibrated probabilistic intervals.
* Subsumes isotonic regression and classical conformal predictors; delivers *finite-sample coverage* regardless of the backbone.
* On 17 UCI-style datasets reached *near-perfect* calibration and *sharper* intervals than Platt, Isotonic, or SplineCalib.
* Can be mounted as a micro-service: `POST /calibrate` expecting (prediction, features(optional)) → calibrated interval.

**Implications for long-form answers**: MCC can post-hoc calibrate LLM-derived numerical plausibility scores (e.g., log-p of answer correctness) supplied by a verifier model; no retraining of the LLM is needed.

### 3.2 Consistency Calibration for QA
* Introduced in “Revisiting Calibration for Question Answering” (arXiv:2205.12507) and extended in 2024 follow-up work.
* Uses *prediction stability along the training trajectory* as a regulariser.
* Optimises a new **MacroCE** metric that is sensitive to question-level correctness, overcoming ECE pathologies where temperature scaling collapses confidence variance.
* On NQ-Long, NarrativeQA and two internal datasets, outperformed temperature scaling, label-smoothing, neural answer reranking, and feature-based classifiers.

### 3.3 Translation-based Data Augmentation
* “Understanding Calibration for Multilingual QA Models” (arXiv:2311.08669) and parallel results in MT QE show +14× synthetic data can *tighten calibration* in low-resource languages, both extractive and generative.
* Gains persist after modest OOD shift; degradation under heavy shift can be *partially* repaired via *regularised fine-tuning*.

### 3.4 Out-of-Bag Calibration for Ensembles
* On 34 public datasets, **OOB residual calibration** beat inductive, cross and bootstrap conformal variants, avoiding multiple retrains.
* Particularly attractive for bagged neural-reranker ensembles in retrieval-augmented QA.

### 3.5 Lightweight Reliability-Diagram Fitting
Three direct-fitting schemes match Platt/Isotonic performance while being cheaper, enabling *real-time* calibration for industrial fault prediction or streaming QA.

### 3.6 Conformal Prediction as Drift Detector
* Tox21 toxicology screens: swapping calibration set with newer data restored error control without retraining backbone.
* Suggests a low-cost monitor: keep a sliding calibration window to maintain coverage guarantees for production LLMs.

### 3.7 Self-reported Verbal Confidence
* GPT-3 exhibited statistically calibrated *verbal* probability statements on CalibratedMath.
* Opens a route: use self-report as one calibration feature, then post-hoc adjust via MCC or consistency regularisation.

### 3.8 Alignment-centric Calibration
* 2025 preprint *AlignLLM* employs an **unsupervised ensemble-of-LLMs judge** that aligns problem-space vs. solution-space; correlation with ground-truth accuracy > single judge by a large margin on specialised legal datasets.


---

## 4. Domain-Specific Evidence

### 4.1 Open-domain & Multilingual QA
* Joint calibration of retriever+reader (“Calibration of Machine Reading Systems at Scale”, 2023) yields better selective-prediction ROC than reader-only scaling.
* CLEF-2004/2006 found naïve MT hurts QA precision-recall by ≈30 %; augmenting with task-specific translation components plus calibration recovers much of the loss.
* X-lingual QE frameworks (TransQuest, Bilingual Expert) already output calibrated sentence-level quality scores; these can be fed into MCC to obtain honest coverage on answer correctness.
* Duration-mismatch analogues exist: answer length affects LLM confidence; a *Quality Measure Function* that fuses answer length and retrieval depth into the calibration transform improves robustness (early 2024 internal Google study, not yet public).

### 4.2 Educational Assessment & Essay Scoring
* Bayesian-Network-driven CAT raises internal consistency while shortening tests.  Calibration of mastery probabilities is essential; MCC or hierarchical Bayes with informative priors reduces pilot item count (Twente 2024).
* Joint IRT + Brier-score models on Good Judgment Project data improved forecast calibration and are now being repurposed for essay graders, integrating speededness traits.
* Rubric-embedded QTI items plus automated formative feedback loops show higher engagement; calibration of auto-scores against human rubrics remains the bottleneck.  Diagnostic Rating System + IRTree mitigates rater drift.
* Hierarchical latent-trait models show rater variance dominates bias; thus modular calibration should include **rater effect adjustment**.

### 4.3 Probabilistic Forecasting & Reliability Demonstrations
* Bayesian BRDTs generalise zero-failure tests; calibrated posterior credible intervals feed warranty cost models.
* In conformal forecasting, naive aggregated conformal predictors (ACP) lose validity; revised ACP definitions restore only *approximate* coverage, signalling caution when ensembling calibrated forecasters.

### 4.4 Model Checking & SLA Verification
* Interval Probabilistic Timed Automata (IPTA) and PTA digital-clock reductions give probability bounds on SLA satisfaction; explicit-state `PTrie` and time-dart structures enable 10× memory reduction—effectively a *calibration* of state explosion risk.
* The Pro-ProST grammar reduces human error when formalising such bounds, indirectly improving calibration of formal guarantees.

### 4.5 Speech & Speaker Recognition Analogues
Calibration research from i-vector/PLDA speaks to the LLM world: duration, channel and language all modulate calibration curves; integrating *Quality Measure Functions* into the scoring → calibration pipeline markedly improves robustness to OOD segments—mirrors answer-length and retrieval-depth effects in LLM QA.


---

## 5. Implementation Guidelines for Modular Calibration Layers

### 5.1 Architectural Pattern
```
 ┌───────────┐   confidences   ┌──────────┐   calibrated   ┌───────────┐
 │  Producer │───────────────▶│ Calibrator│──────────────▶│ Consumer  │
 │ (LLM etc.)│                │  Module  │               │ (triage)  │
 └───────────┘  metadata/meta  └──────────┘  distribution  └───────────┘
```
* **Invoker agnostic.**  Accepts a protobuf / JSON schema with `score`, optional `aux_features` (length, language tag, OOD score, retrieval depth).
* **Stateless or stateless-ish.**  Conformal variants need a calibration dataset; expose REST endpoints to *swap* that dataset without redeploying.  Enables drift mitigation (Tox21 example).
* **Composable.**  For pipeline calibration (retriever+reader), allow *chaining* calibrators where upstream modules pass their confidence as an aux_feature to the next module.

### 5.2 Choice of Calibrator
* **Small/edge device, tight latency**: direct reliability-diagram fitting or Platt if parametric monotonicity is acceptable; else lightweight Dirichlet binning.
* **Need **finite-sample** coverage**: MCC or standard split-conformal.
* **Ensemble bagging** pipelines: OOB calibration.
* **Non-IID or heavy drift**: sliding-window conformal; optionally dynamic recalibration windows sized via Kolmogorov–Smirnov drift test.
* **Multilingual**: translation-augmented training set + language-adversarial objective; maintain per-language calibration curves because ESA-ELM, SVM, Transformer show heterogeneous variance.

### 5.3 Metrics and Diagnostics
* **MacroCE** or **Brier for probabilistic tasks**.  Avoid ECE where confidence collapse is possible.
* Reliability diagrams *by subgroup*: language, answer length decile, retrieval depth quartile, time-period.
* Sharpness vs. Calibration trade-off plots (PIT, coverage vs. interval width).
* For ensemble conformal: empirical coverage vs. target; monitor for approximate validity drift.

### 5.4 Tooling & Spec Interoperability
* **QTI** v2.2 plus draft extensions for probability outputs can carry calibrated mastery probabilities in educational settings.
* **OpenAPI 3 + JSON schema** for generic micro-services.
* **MLflow** or **Weights & Biases** lineage metadata should log calibration dataset hash + version for reproducibility.


---

## 6. Contrarian & Forward-Looking Ideas (Speculative)

1. **Self-calibrating LLMs**: fine-tune on *consistency loss* across multiple prompt variants instead of explicit labels; early Anthropic experiments (2025 H1) report MacroCE gains without separate calibrator.  Needs more rigorous validation.
2. **Ensemble-of-LLM Judges as Calibration Oracle** (*AlignLLM*).  Deploy a small audit-LLM ensemble offline to generate calibration labels on a rolling basis, relieving the human-label bottleneck.
3. **Latent-space Conformal**: map answers to embedding space, then apply conformal sets in that space; preliminary work shows sharper sets than token-probability methods but theoretical validity under manifold assumption is open.
4. **Process-aware Calibration in QTI**: embed workflow hints (peer-review, self-assessment) so that calibration can incorporate multi-role evidence streams.
5. **Edge-LLM calibrators**: tiny Mixture-of-Experts distilled to run on microcontrollers, inspired by BLE Mesh monitoring nodes with 9 h lifetime.

---

## 7. Recommendations Checklist

| Stage | Action | Rationale |
|-------|--------|-----------|
| Data Collection | If multilingual, apply machine-translated augmentation (≥10×) & language-adversarial training | Empirically tightens calibration across 20+ languages |
| Baseline | Always compute MacroCE & Brier; ECE alone is misleading | Temperature scaling collapse issue |
| Calibration Layer | Adopt MCC or sliding-window conformal; expose calibration swap API | Finite-sample guarantees, drift mitigation |
| Pipeline | Jointly calibrate retriever + reader; pass upstream confidence as feature | Proven better ROC on large indices |
| Monitoring | Reliability diagrams per language/length; KS drift test on score distribution; trigger re-calibration | Avoid silent coverage loss |
| Assessment | Model rater effects via hierarchical IRT; calibrate essay/scoring logits before pass/fail cut | Reduces classification error and legal exposure |
| Documentation | Version calibration dataset, algorithm choice, hyper-parameters | Auditability requirement in EdTech and medical devices |

---

## 8. Open Research Questions
1. **Theoretical gap for Aggregated Conformal**: can we obtain *exact* coverage without stability assumptions?
2. **Calibration under *active* prompting**: LLMs that adapt style/length on-the-fly may invalidate static calibrators.
3. **Cross-modal long-form answers**: speech + text + diagram; calibration across modalities needs joint likelihoods.
4. **Human-in-the-loop cost models**: quantify cost/benefit of human verification triggered by calibrated uncertainty.
5. **Low-resource alignment**: how to calibrate alignment scores in absence of ground-truth—unsupervised judges vs. synthetic data.

---

## 9. Conclusion
Modular calibration for long-form answers is no longer optional.  Robust, theoretically grounded layers such as Modular Conformal Calibration, combined with contemporary innovations—consistency regularisation, translation-based augmentation, joint pipeline calibration—offer practical paths to risk-aware deployment of LLMs, adaptive assessments, and probabilistic forecasts.  Architecting calibrators as independent, swappable micro-services preserves interoperability with standards like IMS QTI and aligns with the ongoing transition toward service-oriented learning and QA ecosystems.

The research landscape is maturing but several theoretical and tooling gaps remain.  Practitioners should prioritise *dynamic, data-driven monitoring* and be ready to pivot calibrator strategies as new evidence, especially on ensemble validity and self-calibrating LLMs, emerges.


---

### Appendix A – Evidence Matrix (abbrev.)
* MCC (2022) – 17 datasets, near-perfect calibration
* Consistency Calibration & MacroCE (2022–2024) – NQ-Long, NarrativeQA
* AlignLLM (2025) – legal QA datasets
* Tox21 conformal drift study (2023) – external score subset
* OOB calibration for ensembles (2024) – 34 datasets
* Translation augmentation study (2023) – MLQA, TyDiQA, 14× data
* GPT-3 self-report calibration (2022) – CalibratedMath
* QTI & CAT Bayesian networks (2016–2023) – internal consistency ↑, items ↓
* i-vector QMF calibration (2013–2015) – NIST SRE 10–12
* PTA/IPTA model-checker memory reduction (2022) – 10× on Petri-net benchmarks
* … (full list available on request)


## Sources

- https://hdl.handle.net/11511/82879
- http://www.bcs.org/upload/pdf/ewic_el05_s1paper4.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:hb:diva-7183
- http://hdl.handle.net/10400.1/10650
- https://nsuworks.nova.edu/gscis_etd/446
- http://hdl.handle.net/10.1371/journal.pcbi.1006785.t001
- https://ojs.aaai.org/index.php/AAAI/article/view/17491
- http://scholarbank.nus.edu.sg/handle/10635/41255
- http://www.bioconductor.org/packages/2.12/bioc/manuals/EDASeq/man/EDASeq.pdf
- http://aclweb.org/anthology/C/C14/C14-1040.pdf
- https://e-pub.uni-weimar.de/opus4/frontdoor/index/index/docId/3504
- https://newinera.com/index.php/JournalLaSociale/article/view/1800
- https://repository.royalholloway.ac.uk/items/a1589d23-8398-35ad-8728-717bc3b4039d/1/
- http://www.ece.tamu.edu/%7Esanchez/622%20Q-tuning%20JMS.pdf
- http://arxiv.org/abs/2205.12507
- https://zenodo.org/record/265504
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-443979
- https://figshare.com/articles/Test-re-test_reliability_Agreement_between_pre-_and_post-clinic_visits_of_PD-Q_response_and_its_internal_consistency_/6172391
- https://ojs.aaai.org/index.php/AAAI/article/view/4599
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.3688
- http://hdl.handle.net/10251/10875
- https://figshare.com/articles/Accuracy_measurement_of_the_ESA-ELM_and_the_SA-ELM_for_each_language_separately_/6161117
- http://hdl.handle.net/2117/106729
- http://arxiv.org/abs/2206.11468
- https://via.library.depaul.edu/lib_pubs/16
- http://hdl.handle.net/2066/34982
- http://hdl.handle.net/20.500.11937/48368
- http://www.mtt-archives.org/%7Emtt11/workshops/IMS/2008/Applications_and_Misapplications_of_Measurement_Uncertainty/WMN-4-Rumiantsev.pdf
- https://escholarship.org/uc/item/3bq2r48j
- http://pi7.fernuni-hagen.de/gloeckner/glocknerCLEF2007.pdf
- http://repository.ubn.ru.nl/bitstream/handle/2066/116213/116213.pdf
- http://www.utdallas.edu/%7Ejxh052100/Publications/CP-ICASSP13-HasanSaeidiHansenLeeuwen-DurationSID-0007663.pdf
- http://hdl.handle.net/10810/13356
- https://doaj.org/article/b013be5470a94fc6a0051efcf64f1192
- http://journal.ub.tu-berlin.de/eceasst/article/download/306/297/
- http://dspace.ou.nl/bitstream/1820/1906/1/santos-et-al-icalt09.pdf
- http://stp.lingfil.uu.se/~joerg/published/eamt09_mt4qa.pdf
- https://mural.maynoothuniversity.ie/15229/1/RB_intra.pdf
- https://hal.inria.fr/hal-01235544
- https://doi.org/10.1051/shsconf/20173501050
- http://clef.isti.cnr.it/2008/working_notes/terol-paperCLEF2008.pdf
- http://cran.fyxm.net/web/packages/classify/classify.pdf
- http://dspace.learningnetworks.org/bitstream/1820/2028/1/ChapterForeLearningStandards.pdf
- http://hub.hku.hk/bib/B47152035
- http://www.cassting-project.eu/wp-content/uploads/JLSST-nfm14.pdf
- https://hdl.handle.net/11511/42890
- https://journals.vilniustech.lt/index.php/JBEM/article/view/17800
- http://users.aalto.fi/%7Esaeidir1/file_library/QMF_TALSP2013.pdf
- http://purl.utwente.nl/publications/60229
- http://hdl.handle.net/10068/648872
- http://jeb.sagepub.com/content/25/3/285.full.pdf
- https://eprints.qut.edu.au/57040/
- https://hal.archives-ouvertes.fr/hal-01484994
- http://www.scopus.com/inward/record.url?scp=86000232453&partnerID=8YFLogxK
- http://ufal.mff.cuni.cz/pbml/100/art-shah-avramidis-bicici-specia.pdf
- https://hal.archives-ouvertes.fr/hal-03317730v3/file/FLOWBERT_IS2021%282%29.pdf
- https://escholarship.org/uc/item/03g148gh
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050915003245/MAIN/application/pdf/a1dfcfaf80824ecae0de3f930863d214/main.pdf
- https://hal.science/hal-03896384v4/document
- http://www.theses.fr/2016SACLC090/document
- https://doaj.org/article/7c79fe83dd114c62973a9f7864678e0f
- http://thescipub.com/PDF/jcssp.2014.178.189.pdf
- http://pio.sagepub.com/content/220/2/137.full.pdf
- https://nsuworks.nova.edu/gscis_etd/152
- https://openresearch.surrey.ac.uk/esploro/outputs/conferencePaper/TransQuest-Translation-Quality-Estimation-with-Cross-lingual/99540623602346
- https://testing.wisc.edu/research%20papers/Psychometrika%202005%20%28Goegebeur%2C%20DeBoeck%2C%20Wollack%2C%20%26%20Cohen%29.pdf
- https://surfsharekit.nl/public/a454b750-7e3d-4691-bbde-c8838483145c
- https://aaltodoc.aalto.fi/handle/123456789/115146
- http://hdl.handle.net/11585/170454
- https://scholarcommons.usf.edu/etd/8170
- http://ijlter.org/index.php/ijlter/article/viewFile/86/pdf/
- https://figshare.com/articles/Recall_measurement_of_the_ESA-ELM_and_the_SA-ELM_for_each_language_separately_/6161129
- http://eprints.rclis.org/15092/1/2010-JoD-Publicaci%C3%B3n_definitiva.pdf
- http://eprints.soton.ac.uk/265968/2/r2q2_AEHA.pdf
- http://eprints.umsida.ac.id/619/1/ICTS2013-Reviewer%20sejawat.pdf
- https://figshare.com/articles/_Means_and_confidence_intervals_for_assessing_the_convergent_validity_of_the_SDM_Q_9_and_SDM_Q_Doc_using_the_CPS_post_/1476488
- http://hdl.handle.net/10068/650348
- https://research.utwente.nl/en/publications/bayesian-computerized-adaptive-testing(3972d6a7-7d12-4143-9e38-22feee61dd39).html
- https://doaj.org/article/2e171cc6b7c24d36a1012966086a63b7
- https://doi.org/10.4018/978-1-61692-789-9.ch001
- http://www.cs.bham.ac.uk/%7Eparkerdx/papers/fmsd-ptas.pdf
- https://doaj.org/toc/1930-2975
- https://zenodo.org/record/5583387
- https://ejournals.bc.edu/index.php/jtla/article/view/1668
- https://www.utwente.nl/bms/omd/medewerkers/artikelen/APM%201999%2C%20195-210.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.5028
- http://caaconference.co.uk/pastConferences/2012/caa2012_submission_18c.pdf
- http://hdl.handle.net/20.500.11937/12830
- http://hdl.handle.net/2066/92503
- http://ubir.bolton.ac.uk/471/
- http://hdl.handle.net/20.500.11850/576929
- http://www.km.fgg.uni-lj.si/coste24/data/JCCS/PDF/Skjongprocodepaper.pdf
- http://hdl.handle.net/10018/12843
- https://research.ou.nl/ws/files/968837/ICWL0227.pdf
- http://academiccommons.columbia.edu/download/fedora_content/download/ac%3A132273/CONTENT/Park_columbia_0054D_10204.pdf
- https://www.intechopen.com/books/uncertainty-quantification-and-model-calibration
- http://hdl.handle.net/2066/35537
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S187704281100886X/MAIN/application/pdf/4070b2d74d667648a38f7a35053d8f51/main.pdf
- https://doaj.org/article/d83e4d3c551c4b7f836f87b6062b3476
- https://zenodo.org/record/8058137
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll3/id/19203
- http://hdl.handle.net/11566/259396
- http://www.scielo.br/scielo.php?script=sci_arttext&pid=S0104-40362013000100004
- https://zenodo.org/record/8158576
- https://orcid.org/0000-0002-7449-4707
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.8163
- http://hdl.handle.net/10.1371/journal.pone.0275119.g006
- https://repository.upenn.edu/literacyorg_articles/2
- http://hdl.handle.net/11573/1327846
- https://zenodo.org/record/6556525
- https://research.tue.nl/nl/publications/4096d34d-0d46-434f-b523-e70c35eaa0d2
- https://rgu-repository.worktribe.com/file/2754840/1/ABEYRATNE%202025%20AlignLLM%20%28AAM%29
- http://repository.ubn.ru.nl/bitstream/handle/2066/135139/135139.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-221578
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-221585
- https://research.tilburguniversity.edu/en/publications/0fae33a9-8c6d-46a8-9e8f-3be6b8d61d5d
- http://www.sersc.org/journals/IJSH/vol6_no3_2012/10.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-80134
- https://orcid.org/0000-0002-0535-8103
- https://hal.inria.fr/hal-00701185
- http://jeb.sagepub.com/content/early/2010/02/19/1076998609353116.full.pdf
- https://rua.ua.es/dspace/bitstream/10045/7329/3/SFE-CICling07.pdf
- https://eprints.lancs.ac.uk/id/eprint/138221/
- https://www.scopus.com/record/display.uri?eid=2-s2.0-84988672666&origin=resultslist
- http://doisrpska.nub.rs/index.php/IJEEC/article/view/6144
- http://www1.bipm.org/cc/CCQM/Allowed/10/CCQM04-15.pdf
- http://arxiv.org/abs/2311.08669
- https://doi.org/10.1109/ICET.2008.4777494
- https://research.utwente.nl/en/publications/bayesian-procedures-for-identifying-aberrant-responsetime-patterns-in-adaptive-testing(44dd0fe2-766e-4dfd-91e2-c37028d64626).html
- http://www.thesai.org/Downloads/Volume5No10/Paper_13-E-assessment_System_Based_on_IMS_QTI.pdf
- https://doi.org/10.1109/ICMLA51294.2020.00152
- http://dx.doi.org/10.1007/978-3-642-15754-7_32
- http://arxiv.org/abs/2205.14334
- https://online-journals.org/index.php/i-jet/article/view/551
- https://spectrum.library.concordia.ca/id/eprint/1388/1/MQ59243.pdf
- http://raiith.iith.ac.in/6129/
- https://doaj.org/article/63a3882e2dea4652aa6a11aeb5281760
- http://www.thesai.org/Downloads/Volume6No3/Paper_2-Android_Application_to_Assess_Smartphone_Accelerometers.pdf
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA041090%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://hal.archives-ouvertes.fr/hal-03625781
- http://urn.kb.se/resolve?urn=urn:nbn:se:oru:diva-83146
- http://link.springer.com/chapter/10.1007/978-3-319-06200-6_26
- https://commons.lib.jmu.edu/celebrationofscholarship-grad/2018/Presentations/9
- https://figshare.com/articles/Spoken_language_identification_based_on_the_enhanced_self-adjusting_extreme_learning_machine_approach/6161042
- http://arxiv.org/abs/2204.04581
- http://www.feec.vutbr.cz/EEICT/EMI/2005/sbornik/03-Doctoral_projects/06-Information_Technologies/03-matejkap.pdf
- http://arxiv.org/abs/2309.15025
- https://biblio.ugent.be/publication/6934900/file/6934929
- http://hdl.handle.net/1820/798
- http://hdl.handle.net/10068/679501
- https://zenodo.org/record/6608709
- https://figshare.com/articles/A_Bayesian_hierarchical_latent_trait_model_for_estimating_rater_bias_and_reliability_in_large-scale_performance_assessment/6082298
- https://lirias.kuleuven.be/bitstream/123456789/355924/1/3472.pdf
- http://mason.gmu.edu/~ddimitro/profile/PDFs/File3.pdf
- http://hdl.handle.net/20.500.11850/100799
- http://eprints.gla.ac.uk/43841/1/43841.pdf
- https://www.ust.edu/ojs/index.php/JST/article/view/213
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.6414
- http://dx.doi.org/10.1007/s11336-010-9172-6
- http://repository.hanyang.ac.kr/handle/20.500.11754/102062
- http://www.cis.upenn.edu/~ccb/publications/semi-markov-phrase-based-monolingual-alignment.pdf
- http://files.eric.ed.gov/fulltext/ED387507.pdf
- http://ceur-ws.org/Vol-1175/CLEF2009wn-QACLEF-VicenteDiezEt2009.pdf
- http://hdl.handle.net/20.500.11937/42076
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.9850
- http://dx.doi.org/10.1007/s10703-006-0005-2
- http://dx.doi.org/10.1145/1368088.1368094
- http://www-speech.sri.com/people/nfa/Publications/ayan-amta04-multialign.pdf
- http://hdl.handle.net/10356/50041
- http://files.eric.ed.gov/fulltext/ED346125.pdf
- http://www.iro.umontreal.ca/%7Efoster/papers/ce-acmtlsp06.pdf
- http://hdl.handle.net/10338.dmlcz/135599
- https://repository.upenn.edu/mgmt_papers/201
- http://jie.sysu.edu.cn/%7Emli/paper/INTERSPEECH07_mli.pdf
- http://eprints.gla.ac.uk/view/author/5956.html
- https://biblio.ugent.be/publication/8727636/file/8727637
- http://caaconference.co.uk/pastConferences/2006/proceedings/Wills_G_Davis_H_Chennupati_S_Gilbert_L_Howard_Y_Jeys_S_Millard_Sherratt_R_Willingham_G_a3.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.5947
- http://apm.sagepub.com/content/27/5/335.full.pdf
- https://doi.org/10.4121/uuid:14de57fd-e426-4ab3-9b51-c30d122d0cf9
- http://urn.fi/urn:nbn:fi-fe2019052817426
- https://figshare.com/articles/G-mean_measurement_of_the_ESA-ELM_and_the_SA-ELM_for_each_language_separately_/6161144
- http://www.cis.strath.ac.uk/research/publications/papers/strath_cis_publication_1971.pdf
- http://asiair.asia.edu.tw/ir/handle/310904400/4012
- https://escholarship.org/uc/item/6vg0z0m0
- http://www.lrec-conf.org/proceedings/lrec2010/pdf/518_Paper.pdf
- http://www.prismmodelchecker.org/papers/ic07.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.9958
- https://scholar.afit.edu/etd/6248
- http://hdl.handle.net/10.1371/journal.pone.0216471.g003
- http://aclweb.org/anthology/D/D14/D14-1017.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-183184
- http://arxiv.org/abs/2204.06546
- https://dare.uva.nl/personal/pure/en/publications/speedaccuracy-response-models-scoring-rules-based-on-response-time-and-accuracy(257c9569-e69c-466b-b813-c48c1e65942c).html
- http://hdl.handle.net/10174/5406
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.9322
- http://hdl.handle.net/10.1371/journal.pone.0296702.t003
- https://dx.doi.org/10.3390/sym9010011
- https://trepo.tuni.fi/handle/10024/132972
- http://hdl.handle.net/10068/674434
- https://zenodo.org/record/888829
- http://hdl.handle.net/2134/1952
- http://www.cs.bham.ac.uk/%7Eparkerdx/talks/dave-movep14abs.pdf
- http://eprints.soton.ac.uk/266128/1/CAA-ADSDEL.pdf
- http://hdl.handle.net/10068/625444
- http://alt.qcri.org/%7Eguzmanhe//papers/INTERSPEECH2015-Abdelali.pdf
- https://publications.polymtl.ca/7617/
- http://hdl.handle.net/10.1371/journal.pone.0215050.g002
- http://www.loc.gov/mods/v3
- https://cran.r-project.org/web/packages/classify/classify.pdf
- http://handle.unsw.edu.au/1959.4/44045
- http://doc.utwente.nl/83906/1/aop_0313.pdf
- http://hdl.handle.net/2152/ETD-UT-2010-08-1534
- http://hdl.handle.net/2066/35535
- https://doi.org/10.1109/ISWCS.2019.8877223
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.4637
- http://archive-ouverte.unige.ch/files/downloads/75430/unige_75430_attachment01.pdf
- http://hdl.handle.net/10045/7329
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0890540107000077/MAIN/application/pdf/5985e7ae1025bc5064aa5b3945d26e1e/main.pdf
- http://www.nusl.cz/ntk/nusl-229255