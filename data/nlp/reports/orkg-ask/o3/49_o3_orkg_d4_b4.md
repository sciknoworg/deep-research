# Abstaining With Multilingual Knowledge – A Comprehensive Technical Report  
*(all numbered bullets refer to the 78 distinct research learnings supplied; duplicates are collapsed but credited)*

---

## 1  Problem Statement and Motivation  
Selective prediction – a model’s ability to **abstain** (i.e. refuse to return a decision) when its risk of error is high – is rapidly becoming a first-class safety requirement across multilingual NLP use-cases: cross-lingual QA (§4.1), speech-to-speech translation (§4.2), toxicity filtering (§4.3), medical triage, and even low-level language identification.  
Multilingual abstention is hard because:  
• uncertainty must be **calibrated jointly across dozens or hundreds of languages** whose training data sizes, writing systems and typological features differ by orders of magnitude (L13, L26, L51).  
• annotation disagreement is itself language- and culture-dependent (L47, L52, L57).  
• errors may originate in any stage of a cascade (ASR → MT → QA retrieval, etc.), so abstention signals must be **fused across heterogeneous modules** (L8, L28, L30, L45).  
We therefore survey theoretical foundations, metrics, algorithms and deployment practices, drawing not only from core NLP but also from bio-informatics, nuclear engineering and metrology, where sophisticated UQ has long been mandatory (L17, L24, L31, L61).

---

## 2  Theoretical Foundations of Selective Prediction

### 2.1 Risk–Coverage Analysis and the Reject Option  
The formal backbone is the **selective-prediction risk–coverage curve**.  Area-based summaries such as AUACC (L40) extend the well-known ROC-AUC framework (L29, L39, L76) to incorporate an explicit *coverage* axis.  Key properties:
• Threshold-free and class-imbalance-robust (L29).  
• Statistically consistent unlike raw accuracy (L39).  
Comparably, protein–DNA binding predictors now publish **wAUC across spatial cut-offs** (L1) – an instructive analogue for multilingual systems that must satisfy varying risk tolerances in different locales.

### 2.2 Calibration  
Abstention hinges on probability calibration.  Temperature scaling minimizes Expected Calibration Error (ECE) but flattens the confidence distribution; **MacroCE + consistency calibration** (L46) preserve separation between easy and hard instances.  A *global calibration metric* for language identification (L20, L36) analytically ties all binary sub-tasks together – a template for multilingual abstention across hundreds of languages.

### 2.3 Uncertainty Quantification (UQ)  
• **Ensemble disagreement** is an inexpensive, empirically tight proxy for error (L35, L48).  
• Full Deep Ensembles offer gold-standard epistemic UQ but are compute-heavy; **Mixture-Density distillation** (L38) retains outlier detection while meeting real-time constraints.  
• A 2023 subsampling study (L42) shows data uncertainty dominates model uncertainty, cautioning against over-investing in model-centric approaches alone.  
• Cross-domain: MLMC (L24, L50, L64, L77) and Total Monte Carlo (L27, L63) demonstrate how hierarchical variance-reduction and correlated sampling slash cost by >10× in neutron transport; the same control-variate ideas inform **multi-granularity dropout** or **layerwise ensembling** in very large LLMs.

---

## 3  Evaluation Metrics: Lessons Across Disciplines

| Domain | Metric Innovation | Adaptation to Multilingual Abstention |
|---|---|---|
| Protein binding (L1) | weighted AUC over distance cut-offs | Multi-dialect wAUC over risk cut-offs per language/dialect |
| Clinical biomarkers (L25) | ROC-AUC with CI | Add language-stratified CIs when auditing fairness |
| Survival analysis (L11) | Time-dependent AP<sub>t₀</sub> | Track coverage vs. time in streaming SLT |
| Imaging (L12) | Weighted ROC-AUC across dimensionality | Report AUC vs. context window size in multilingual QA |
| Deep ROC Analysis (L58) | Decomposition by risk group | Inspect coverage buckets per language family |

Software such as **Stata cvAUROC** (L7) or **PredictABEL** (L45) can be repurposed into evaluation harnesses; open-source MLMC tool-chains ease CI estimation under label noise.

---

## 4  Algorithmic Building Blocks and Case Studies

### 4.1 Multilingual Question Answering  
• **Icelandic DensePhrases** bootstrapped from machine-translated trivia (L4, L21, L22) attains competitive open-domain QA without any native data, but missing-attribution detection (L42) reveals that up to 50 % of answers lack support – an ideal trigger for abstention.  
• Automatic MT-based data augmentation (L43) lowers ECE by 35 %, improving answerability prediction without retraining.  
• **QAssist** (L44) shows that calibrated multi-source retrieval can hit 96 % recall in requirements engineering – evidence that *retriever–reader discrepancy* is a potent abstention cue.  

### 4.2 Speech-to-Speech Translation Pipelines  
A new 2 643-utterance SLT corpus (L3, L16) plus WCE fusion (L28) proves that ASR posteriors and MT features are complementary.  Second-pass graph rescoring (L30) adds >2 BLEU and gives word-level triage labels {good, ASR_error, MT_error}.  Token-level abstention can thus be exposed to the UI, reducing user re-typing (L40).

### 4.3 Toxicity and Content Moderation  
• Platform-tailored lexica – Twitch valence embeddings (L2) – boost F1 by 31 %.  
• Hybrid monolingual + multilingual fusion yields 95 % less added toxicity when coupled with **Meta’s MinTox** inference filter (L31, L14).  
• Dialect-aware relabeling (L19, L47, L59) outperforms model-only debiasing; weighting annotators (GLAD/Dawid–Skene) restores minority-perceived toxicity accuracy (L47, L52, L57).  
• A multimodal Russian toxic-memes dataset (L34) extends abstention to vision–language.

### 4.4 Machine Translation Evaluation and Quality Estimation  
Referential Translation Machines (L10, L23, L33) and **AfriCOMET** (L6, L18, L79) achieve language-independent QE with no MT system internals.  RoCS-MT (L60) and Ringer et al. (L55) reveal fragility to UGC noise – elevating abstention thresholds for noisy inputs.  **Stupid Backoff** LM smoothing (L41, L78) or high-resource cognate transfer (L56) improve baseline MT, thus reducing downstream abstention rate.

### 4.5 Language Identification and Open-Set Rejection  
Replacing raw acoustic scores with lattice-based confidence (L37) slices error by up to 37 % and enables **unknown-language rejection**; the global-calibration trick (L20) then harmonises thresholds across 100+ languages.

---

## 5  Cross-Pollination From Other Scientific Domains

1. **Protein bio-informatics**: wAUC thinking translates to *risk-granular*, language-conditioned curves.  
2. **Nuclear engineering**: Direct-perturbation vs. stochastic-sampling duality (L17, L63) suggests *local vs. global* sensitivity analysis of multilingual models (e.g. layer-wise perturbations vs. full parameter sampling).  
3. **Micro-flow metrology**: Bayesian propagation prevents non-physical negative intervals near detection limits (L61); likewise abstention logits should remain inside [0,1] under heavy label noise.  
4. **CFD MLMC** (L24, L50, L77) demonstrates that hierarchical approximations can amortise the cost of language-specific calibration runs.

---

## 6  Design Guidelines for a Production-Grade Multilingual Abstention Layer

### 6.1 Signal Generation
• Combine *intrinsic* confidences (softmax, margin) with *extrinsic* signals: ensemble disagreement (L35), self-consistency (L46), retriever–reader agreement (QA), ASR vs. MT alignment (L28).  
• Fuse via lightweight meta-learners (SVM late fusion L8; Bayesian ridge L10), or distill into a single Mixture Density head (L38) for low latency.

### 6.2 Calibration and Metric Tracking
• Optimise *global* calibration (L20) but audit per-language slices with Deep ROC Analysis (L58).  
• Report AUACC + language-stratified CIs (L7, L25).  wAUC over dialect strata mimics protein-binding best practice (L1).  
• Track ECE and coverage buckets continuously; degrade gracefully via MinTox (L31) or coverage-aware reply frameworks.

### 6.3 Data Strategy
• Leverage MT-based augmentation for low-resource languages (L43), plus cognate-transfer (L56) and typology-aware parameter sharing (L72).  
• Use **LITMUS Predictor** (L60, L71) to decide which languages to label next.  
• Aggregate labels with annotator-aware weighting (L47).  Maintain minority-opinion distributions to prevent blind spots.  

### 6.4 Robustness
• Inject character-level noise (L55, L60) and run RoCS-MT stress tests; tune abstention thresholds to maintain constant risk.  
• Monitor cross-modal drift (vision–language memes, L34).  
• For LLM evaluators, keep a human-calibrated reference set per script (L51, L62) – LLM scoring biases otherwise inflate coverage dangerously.

---

## 7  Future Research Directions (speculative)

1. **Multi-Level Abstention**: Mirror MLMC – coarse, cheap language-family detectors gate expensive fine-grained models. 2× cheaper? (*flagged speculative*).  
2. **Dynamic Prompt Harmonizers**: Extend the “harmonizer” risk model (L71) to route queries between agents of differing language competencies, yielding higher attributable answer rates.  
3. **Coverage-Aware Debiasing**: Jointly optimise toxicity fairness and abstention via Pareto-front search, inspired by skip-gram event-prediction re-ranking (L5) and multi-objective CFD sampling.  
4. **Cross-Domain Metric Transfer**: Adapt clinical time-dependent AP<sub>t₀</sub> (L11) to *session-long* dialogue safety monitoring.  
5. **Physically Plausible Calibration**: Import micro-flow Bayesian intervals (L61) to enforce monotone likelihood-ratio constraints on confidence scores under extreme low-data regimes.

---

## 8  Conclusion
Selective abstention in multilingual NLP is no longer optional.  A decade of work on confidence estimation (L8, L10, L28, L38, L45) and three decades of ROC-based evaluation (L29, L39, L76) give us the mathematical machinery; cross-lingual innovations (L6, L13, L31, L41) provide the linguistic coverage; and external scientific domains supply proven UQ tooling (L17, L24, L61).  By systematically integrating these learnings, organisations can build systems that **speak hundreds of languages yet know when to remain silent**—safely, fairly and with quantified guarantees.  

---

### Complete Learning Reference Index
1 wAUC Protein, 2 Twitch Lexicon, 3/16 SLT-WCE Corpus, 4/21 Icelandic QA MT-bootstrapping, 5 Skip-gram Event Prediction, 6/18/79 AfriCOMET, 7 cvAUROC, 8 SVM Fusion WCE, 9/32 CLEF06 MT-QA, 10/23/33 RTM QE, 11 AP<sub>t₀</sub>, 12 MCI Imaging AUC, 13 Typology-based Perf-Pred, 14 Hybrid Toxic Pipeline, 15 Br-PT Toxic Corpus, 17/63 Nuclear UQ, 19/47/59 Dialect-Aware Relabel, 20/36 Global Calibration LID, 22 Cross-Lingual DensePhrases, 24/50/64/77 MLMC, 25 tPA ROC, 26 Multilingual Bias Metric, 27 TMC-CS, 28 SLT WCE Fusion, 29 Seminal ROC-AUC, 30 Second-Pass SLT, 31 MinTox, 34 Toxic Memes Dataset, 35/48 Ensemble Disagreement, 37 Lattice-LID Confidence, 38 MDN Distillation, 39/76 AUC Consistency, 40 Word-Graph WCE, 41/78 Stupid Backoff, 42 Missing-Attr QA, 43 MT-Aug Calibration, 44 QAssist, 45 PredictABEL & Prob Ensemble, 46 MacroCE, 51/62 LLM Eval Bias, 52/57 Annotator Weighting, 55 German QA Noise, 56 Cognate Transfer, 58 Deep ROC Analysis, 60/71 LITMUS & Harmonizer, 61 Bayesian Metrology, 72 Typology-Sharing Parser.


## Sources

- http://aclweb.org/anthology/D/D15/D15-1182.pdf
- http://qa.iis.sinica.edu.tw/iasl/webpdf/paper-2008-exploring_shallow_answer_ranking_features_in_cross-lingual_and_monolingual_factoid_question_answering.pdf
- https://www.repository.cam.ac.uk/handle/1810/316387
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-wbrov7hjmum23
- http://d-scholarship.pitt.edu/43419/1/Taehee_Dissertation_Paper_v2.pdf
- https://eprints.lancs.ac.uk/id/eprint/210065/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.7774
- https://zuscholars.zu.ac.ae/works/7100
- http://urn.kb.se/resolve?urn=urn:nbn:se:miun:diva-42317
- https://doaj.org/article/a74aa9b751f34ba9a347e032653f4f77
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1042.946
- http://hdl.handle.net/10.1371/journal.pone.0212844.t012
- http://www.cerilliant.com/activities_events/tiaft
- https://hal.inria.fr/hal-01002931
- https://figshare.com/articles/_Evaluation_process_of_a_new_prediction_model_/1295050
- https://espace.library.uq.edu.au/view/UQ:4f8dab4
- http://arxiv.org/abs/2205.12390
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-24193
- http://summit.sfu.ca/item/15505
- http://arxiv.org/abs/2307.01503
- http://hdl.handle.net/10.1371/journal.pcbi.1006376.g008
- http://clair.si.umich.edu/clair/HLT-NAACL03/shorts/pdf/hlt_naacl_03_shortpaper_301.pdf
- https://zenodo.org/record/3712029
- http://arxiv.org/abs/2205.12507
- http://hdl.handle.net/1765/25522
- https://figshare.com/articles/_Comparison_of_various_prediction_methods_in_terms_of_the_area_under_the_ROC_curve_AUC_/854911
- http://hdl.handle.net/10.1371/journal.pone.0212844.t013
- http://tubiblio.ulb.tu-darmstadt.de/136782/
- http://nlp.uned.es/MLQA06/papers/ligozat.pdf
- http://www.isca-speech.org/archive/interspeech_2010/i10_1942.html
- http://research-information.bristol.ac.uk/files/14031372/ukci03n.pdf
- https://www.aclweb.org/anthology/2020.findings-emnlp.269/
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D2330%26context%3Dcompsci
- http://www.mt-archive.info/EAMT-2005-Ueffing.pdf
- http://pan.oxfordjournals.org/content/16/2/153.full.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-208303
- http://hdl.handle.net/10.1371/journal.pone.0209002.g003
- https://figshare.com/articles/Screening_performance_of_risk_prediction_or_scoring_models_/4827502
- http://hdl.handle.net/11582/1749
- https://datacompass.lshtm.ac.uk/id/eprint/400/
- http://hdl.handle.net/11025/45010
- http://hdl.handle.net/10.1371/journal.pone.0292888.g001
- https://figshare.com/articles/_Receiver_operating_characteristic_ROC_curve_plots_for_TG_AUC_predicting_diabetes_risk_/1641646
- http://www.loria.fr/~smaili/interspeech09.pdf
- https://hal.inria.fr/inria-00333843
- https://zenodo.org/record/2597291
- http://doras.dcu.ie/19107/
- http://hdl.handle.net/1853/66502
- https://www.openaccessrepository.it/record/106587
- http://edschofield.com/publications/schofield03language.pdf
- http://hdl.handle.net/10.1184/r1/6473816.v1
- https://figshare.com/articles/_Classification_performance_measures_of_final_prediction_model_at_different_risk_thresholds_/1607959
- http://hdl.handle.net/1946/39966
- http://hdl.handle.net/10.1371/journal.pone.0272796.g005
- http://www.mt-archive.info/MTS-2003-Ueffing.pdf
- http://arxiv.org/abs/2205.06424
- https://zenodo.org/record/8082258
- https://hal-supelec.archives-ouvertes.fr/hal-00321714/file/paper_132_BIOTECHNO_2008.pdf
- http://hdl.handle.net/10.1371/journal.pone.0200397.t003
- http://research.ijcaonline.org/volume108/number15/pxc3900444.pdf
- http://arxiv.org/abs/2207.01918
- https://figshare.com/articles/_Sensitivity_specificity_accuracy_and_the_area_under_the_curve_for_a_receiver_operating_characteristic_curve_ROC_AUC_for_control_and_MCI_classification_/346804
- http://www.eurasip.org/Proceedings/Ext/SPECOM2006/papers/084.pdf
- https://eprints.whiterose.ac.uk/169793/7/2020.aacl-main.91.pdf
- http://hdl.handle.net/11582/331001
- http://hdl.handle.net/2066/147122
- http://hdl.handle.net/11582/329886
- https://figshare.com/articles/Prediction_accuracues_using_diffusion_based_fuctional_profiles_and_annotation_based_functional_profiles_quantified_by_AUC-ROC_/5650393
- http://infoscience.epfl.ch/record/286915
- http://hdl.handle.net/2117/367737
- http://hdl.handle.net/10.1371/journal.pone.0210575.t005
- http://hdl.handle.net/11582/3974
- https://figshare.com/articles/_General_accuracy_distribution_based_on_wAUC_/1626615
- http://www.mt-archive.info/CL-2007-Ueffing.pdf
- http://www.mt-archive.info/EMNLP-2009-Nakov.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.5028
- https://doaj.org/article/5d15f4a4b1f54c99aba477b05ccebb2a
- http://hdl.handle.net/11582/2967
- http://www.mt-archive.info/MTS-2007-Sanchis.pdf
- http://arxiv.org/abs/2311.06532
- http://hdl.handle.net/1946/39414
- https://hal.science/hal-04124948
- https://pub.h-brs.de/frontdoor/index/index/docId/8893
- https://figshare.com/articles/Prediction_performance_/6006227
- http://hdl.handle.net/1959.14/1280832
- https://doi.org/10.1051/epjconf/201921103002
- https://hdl.handle.net/20.500.12259/53784
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.4393
- https://doaj.org/article/e89c241cc81644cab89a16173c0cb41d
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.5075
- http://hdl.handle.net/10.1371/journal.pone.0202312.t004
- https://figshare.com/articles/_Prediction_performance_of_10_fold_cross_validation_based_on_different_encoding_methods_/294999
- https://zenodo.org/record/1292841
- http://arxiv.org/abs/2302.07372
- https://zenodo.org/record/884044
- https://research.rug.nl/en/publications/6af86526-142f-4f32-bbbb-3497743a3ede
- https://repository.upenn.edu/cis_reports/878
- https://hal.science/hal-04300824
- https://figshare.com/articles/_ROC_curves_for_different_point_cut_offs_for_the_proposed_survey_tool_/985987
- http://gtts.ehu.es/gtts/NT/fulltext/PenagarikanoInterspeech2012a.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/21736
- https://rua.ua.es/dspace/bitstream/10045/7329/3/SFE-CICling07.pdf
- https://www.epj-n.org/10.1051/epjn/2020003/pdf
- https://www.repository.cam.ac.uk/handle/1810/315111
- https://hal.archives-ouvertes.fr/hal-01807054
- http://hdl.handle.net/10.1371/journal.pone.0205916.t005
- http://arxiv.org/abs/2311.08669
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.2599
- https://zenodo.org/record/3578008
- http://arxiv.org/abs/2309.05619
- https://research.rug.nl/en/publications/c2101556-c819-4c66-b685-5817cc38bc6f
- http://hdl.handle.net/10.1371/journal.pone.0210450.g002
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.8.130
- https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=1354&amp;context=usf_patents
- https://doi.org/10.1051/snamc/201403404
- https://zenodo.org/record/7925667
- https://zenodo.org/record/5770267
- https://zenodo.org/record/3991352
- https://hal.science/hal-03812319/document
- https://hal.science/hal-03228823v2/document
- https://lirias.kuleuven.be/bitstream/123456789/325258/2/Postprint%202013-Monte-Carlo%20based%20uncertainty%20analysis%20-%20Sampling%20efficiency%20and%20sampling%20convergence.pdf
- https://hal.archives-ouvertes.fr/hal-02021878/file/IS07.pdf
- https://zenodo.org/record/6960790
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.4737
- https://zenodo.org/record/7188178
- http://hdl.handle.net/1773/48884
- http://stp.lingfil.uu.se/~nivre/statmet/brandt.pdf
- http://hdl.handle.net/10.1371/journal.pone.0207741.t001
- http://jech.bmj.com/content/58/8/718.full.pdf
- http://arxiv.org/abs/2310.05069
- http://arxiv.org/abs/2205.06356
- https://figshare.com/articles/_Statistics_of_the_prediction_performances_/302300
- https://publications.aston.ac.uk/id/eprint/46332/1/2311.09828v3.pdf
- https://dx.doi.org/10.1016/j.neucom.2021.02.023
- http://www.mt-archive.info/IWSLT-2005-Gimenez.pdf
- https://figshare.com/articles/_Area_under_the_curve_AUC_for_cross_validation_ROC_curves_of_the_method_Zulkifley_et_al_/1264743
- http://cdn.intechopen.com/pdfs-wm/5879.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-339229
- http://hdl.handle.net/10481/48541
- http://www.asru2015.org/
- https://digitalcommons.kennesaw.edu/context/dataphd_etd/article/1017/viewcontent/Sayenju_PhD_Dissertation.pdf
- http://hdl.handle.net/2117/27387
- http://dspace.mit.edu/bitstream/handle/1721.1/86510/46895107-MIT.pdf%3Bjsessionid%3D005FEFBD380FDDDE5E34A82BF4005D5A?sequence%3D2
- http://www.iai.uni-sb.de/carl/papers/lrec.pdf
- http://hdl.handle.net/1946/39430
- http://www.iro.umontreal.ca/%7Efoster/papers/ce-acmtlsp06.pdf
- http://hdl.handle.net/10068/647870
- http://hdl.handle.net/10150/595756
- http://apps.carleton.edu/people/cussery/assets/ussery.NELS_40.pdf
- https://figshare.com/articles/_Comparison_of_the_prediction_accuracy_measured_by_AUC_on_ten_real_world_networks_/1167289
- https://escholarship.org/uc/item/5z00b5m9
- https://figshare.com/articles/_ROC_curve_for_tissue_plasminogen_activator_antigen_tPA_Ag_/1393695
- https://digitalcommons.kean.edu/keanpublications/1727
- http://hdl.handle.net/2429/65247
- http://arxiv.org/abs/2306.16564
- https://research.chalmers.se/en/publication/200356
- http://www.aclweb.org/anthology/W/W14/W14-3339.pdf
- https://research.hva.nl/en/publications/889b7d24-eac9-4086-ab59-1a54de88644d
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.4098
- https://nrc-publications.canada.ca/fra/voir/objet/?id=78f288f5-8987-4130-8eed-b0f2e395859a
- https://hal.archives-ouvertes.fr/hal-01110393
- https://figshare.com/articles/_Sensitivity_specificity_accuracy_and_the_area_under_the_curve_for_a_receiver_operating_characteristic_curve_ROC_AUC_for_Control_MCIna_and_MCIa_classification_/347096
- https://figshare.com/articles/_Predictive_accuracies_AUC_Kappa_and_TSS_of_Larix_principis_rupprechtii_/1340277
- https://figshare.com/articles/_Accuracy_classification_for_different_ranges_of_AUC_for_the_diagnostic_test_/1450634
- http://hdl.handle.net/1773/47617
- https://escholarship.org/uc/item/1hc811c0
- http://hdl.handle.net/10397/12837
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.4505
- http://arxiv.org/abs/2210.15452
- https://zenodo.org/record/5156186
- https://lirias.kuleuven.be/handle/123456789/343305
- http://arxiv.org/abs/2311.08298
- http://arxiv.org/abs/2204.06487
- http://infoscience.epfl.ch/record/205275
- https://ojs.aaai.org/index.php/AAAI/article/view/26528
- https://zenodo.org/record/8306439
- http://www.map.meteoswiss.ch/map-doc/NL15/marsigli.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.1126
- https://zenodo.org/record/7525010
- https://ojs.aaai.org/index.php/AAAI/article/view/26574
- http://nbn-resolving.de/urn:nbn:de:bsz:352-0-365898
- http://arxiv.org/abs/2205.12456
- https://figshare.com/articles/Apparent_and_cross-validated_area-under-the-curve_AUC_statistics_for_four_super_learner_risk_prediction_tools_as_well_as_for_each_of_the_component_algorithms_methods_considered_in_the_implementation_of_the_super_learner_/5801250
- http://hdl.handle.net/11356/1187
- https://serval.unil.ch/notice/serval:BIB_59398FF92BA0
- http://hdl.handle.net/10536/DRO/DU:30047368
- https://www.repository.cam.ac.uk/handle/1810/298857
- https://etheses.whiterose.ac.uk/14284/1/thesis.pdf
- https://orcid.org/0000-0001-5736-5930
- http://hdl.handle.net/10.1371/journal.pone.0212844.t014
- http://dx.doi.org/10.1145/1777432.1777439
- http://hdl.handle.net/1969.1/186559
- http://www.computing.dcu.ie/%7Eebicici/publications/2014/RTMforQE.pdf
- https://zenodo.org/record/5230386
- http://arxiv.org/abs/2309.07462
- http://www.loc.gov/mods/v3
- https://hal.archives-ouvertes.fr/hal-02095256
- http://hdl.handle.net/2429/56150
- http://hdl.handle.net/10.1371/journal.pone.0212844.t015
- https://www.scipedia.com/public/Pons_Prats_Bugeda_2019a
- http://resolver.tudelft.nl/uuid:43f84e8d-71f7-4379-84a6-b6cac86253e5
- http://arxiv.org/abs/2305.14332
- http://hdl.handle.net/10045/7329
- https://hal.archives-ouvertes.fr/hal-01840808
- http://hdl.handle.net/2078.1/240894
- https://hal.archives-ouvertes.fr/hal-00953773