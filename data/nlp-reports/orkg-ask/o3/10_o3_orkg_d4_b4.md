# Cross-Culture Self-Debiasing through Cross-Lingual Interactions among Large Language Models

*Final technical scoping report (2025-09-04)*

---

## 1 Motivation and Problem Statement

Large Language Models (LLMs) inherit and occasionally amplify societal biases present in their training data.  These biases manifest heterogeneously across cultures and languages – e.g. region-specific gender stereotypes in CLIP **[Aequitas 2023]**, stronger religious stereotypes than gender stereotypes in multilingual bias probing **[arXiv 2311.09090]**, or language-dependent adjective stereotypes in the 250 k-politician corpus.  A single-language debiasing pass therefore cannot guarantee equitable behaviour once the model is redeployed in another linguistic or cultural context.  

Recent work shows that (i) cross-lingual **evaluation** is feasible without hand annotation (MBE score, NAACL 2022) and (ii) *interaction-based* techniques such as Social-Contact Debiasing (SCD) can slash measured social biases by ≈40 % in a single epoch.  In parallel, multi-agent reasoning frameworks (ReConcile, AlignLLM, noisy-voting theory) demonstrate that heterogeneous model collectives reliably outperform isolated models and reduce self-evaluation bias.  Collectively, these findings suggest a new research direction: **cross-culture self-debiasing**, in which multiple LLM agents speaking different languages critique and refine each other’s outputs until bias metrics converge to acceptable levels in every language domain.

This report synthesises the relevant literature, proposes a concrete multi-agent, cross-lingual debiasing pipeline, and enumerates datasets, metrics, verification methods and experimental design choices required to build a *replicable* debiasing benchmark.

---

## 2 Conceptual Framework

### 2.1 Bias axes and cultural embedding

We adopt the multidimensional view recommended by “You Reap What You Sow” (2022): evaluate **beyond gender** to include political ideology, religion, socioeconomic status, disability, and cultural stereotypes.  Intersectional research shows multilevel regression best captures spatio-temporal inequalities.  Therefore, our evaluation stack will log **(language, culture, bias-axis, context)** tuples and support hierarchical modelling.

### 2.2 Cross-lingual transfer and shared representations

mBERT lottery-ticket pruning revealed a language-neutral sub-network largely responsible for zero-shot transfer.  UDify, Cambridge/IARPA layered augmentation and shared-hidden-layer ASR studies confirm that parameter-level sharing can propagate improvements to low-resource languages.  Conversely, bias can *also* propagate along these shared layers.  Structured sparsity (Aalto/FCAI) and vocabulary-independent hidden-layer augmentation provide knobs to localise or suppress bias propagation.

### 2.3 Interaction-based and reinforcement debiasing

• Social Contact Debiasing (108 k prompts, 1 epoch) → ↓40 % social bias.

• Reinforced Calibration uses RL with classifier-based rewards to trim political biases without full retraining.

• TrufLL eliminates exposure bias by dynamically truncating the action space.

All three are *data-light* and compatible with API-only models; they just require a reward or critique signal, which a partner LLM in another language can supply.

### 2.4 Multi-agent error correction and verification

Noisy-voting theory guarantees asymptotic zero error for sufficiently diverse agents.  ReConcile’s 3-agent conference improved GPT-4 by +10 pp.  AlignLLM demonstrates that ensemble, alignment-based grading correlates better with ground truth than single-model self-judging.  

Formal underpinnings: Multi-Agent Protocol → PROMELA + SPIN; Event-B + TLA yields convergence proofs; ASM encodes MAPE-K feedback loops; RepNet-MDP models reputation-driven policy adaptation.  These techniques can provide **machine-checkable guarantees** that the debiasing dialogue terminates and monotonically reduces bias metrics.

---

## 3 State of the Art in Cross-Cultural Bias Evaluation

| Aspect | Key results & gaps |
|---|---|
| Gender bias metrics | MCAS (multimodal, prompt-free), MBE (8 languages, zero annotation) | Need expansion to more axes and non-Indo-Euro families |
| Multimodal audits | Transnational-feminist CLIP audit shows region-specific bias correlating with UN indices | LLM–image interaction remains largely untested |
| Bias axes breadth | Socioeconomic, religion, disability datasets still scarce; politician corpus covers only gender | Urgent need for *multi-axis, multi-lingual* benchmark |
| Evaluation reliability | Bootstrap CIs, permutation tests, “Tangled up in BLEU” reveal small test sets inflate false-positive gains; sentence-level human agreement is nonlinear | Plan for ≥1 000 eval sentences/language, multi-reference, CI reporting |
| Low-resource coverage | WALS & MasakhaNER over-represent core-area African traits; typological skew distorts benchmarks | Adopt triadic Focus–Neighbor–Benchmark sampling and feature-frequency reweighting |
| Human vs automatic | TRECVid, MT-Summit 2003 data show high corpus-level metric correlation only when test sets are large | Combine automatic metrics (MBE, COMET-KIWI) with targeted human adversarial audits |

---

## 4 Proposed Research Programme

### 4.1 Objectives

1. **Benchmark** existing multilingual LLMs on bias across ≥10 language families.
2. **Design** a cross-lingual, multi-agent self-debiasing protocol that iteratively reduces bias without sacrificing utility.
3. **Provide** formal termination & bias-monotonicity proofs using SPIN and Event-B.
4. **Release** open-source datasets, evaluation scripts, and trained checkpoints.

### 4.2 Language and Culture Scope

We select languages along two axes:

• **High-resource Indo-European**: English, Spanish, Russian, Portuguese (EU & African varieties).  
• **Typologically distant / low-resource**: Sudanese Arabic (Zenodo 7426918), Hausa (Chadic), Wolof (Atlantic), Finnish (Uralic), Tamil (Dravidian), Indonesian (Austronesian).  

Family coverage exploits Bayesian phylogenies supplying baseline cultural change rates (Austronesian, Bantu, Indo-European) for temporal grounding.  A triadic Focus–Neighbor–Benchmark design mitigates contact/reconstruction confounds.

### 4.3 Bias Dimensions

1. **Gender and Sexual Orientation** – MCAS, DisCo-EXT, politician corpus.  
2. **Religion** – Social Bias Probing set; region-specific terrorist stereotype probes.  
3. **Political Ideology** – Reinforced Calibration test prompts; GPT-3 partisan tilt corpus.  
4. **Socioeconomic Status** – 1 M-sentence Socioeconomic Bias corpus.  
5. **Disability & Health** – newly crafted prompts intersecting with TSST stress vocabulary.  
6. **Culture-Specific Stereotypes** – e.g., “click consonants→primitive” for Niger-Congo; “high-pitched unstressed syllable→stressed” auditory stereotype from N325 ERP study.

### 4.4 System Architecture

```
┌─────────────────────────────┐        ┌────────────────────────┐
│  LLM-A  (e.g., Open-weight) │◀──────▶│  LLM-B (API-only)      │
└─────────────────────────────┘  CRIT  └────────────────────────┘
        ▲          ▲                       ▲        ▲
        │  round-table ReConcile-style     │        │
        ▼          ▼                       ▼        ▼
┌──────────────────────────────┐   SCORE ┌────────────────────────┐
│  Bias-Metric Ensemble        │────────▶│  RL Debiaser / SCD     │
│  (MBE, MCAS, classifier)     │         └────────────────────────┘
└──────────────────────────────┘
```

1. **Dialogue Engine**: MAP-specified protocol where each LLM returns *answer, uncertainty, self-critique*.  Confidence-weighted vote (CLWA family) selects a canonical answer.  
2. **Critique Phase**: Agents exchange bilingual critiques; populous evidence shows late-fusion majority voting boosts WSD by +2.84 %, suggesting simple majority is sufficient but we add confidence weights.  
3. **Reward Phase**: Bias-Metric Ensemble scores current answer per language.  Reinforced Calibration back-propagates bias penalties; SCD injects contact prompts targeted at the worst axis.
4. **Verification**: SPIN proves protocol termination; Event-B proves that global bias score is non-increasing per iteration.  Alignment with noisy-voting theory ensures asymptotic correctness.
5. **Multimodal Add-on**: CLIP-based image generation tested via MCAS to ensure text-to-image coherence does not reintroduce bias.

### 4.5 Datasets and Data Management

| Resource | Rationale |
| --- | --- |
| Zenodo 7426918 Sudanese Arabic speech | Low-resource dialect to test ASR + text bias |
| African Portuguese 3 M-word corpus | Cross-variety Portuguese stereotypes |
| Helsinki 500 GB multilingual NMT benchmark | Parallel data for automatic back-translation of prompts |
| Socioeconomic Bias 1 M corpus | Non-gender axis |
| Politician 250 k corpus | Fine-grained gender bias metrics |
| CLIP audit prompt set | Multimodal check |
| TSST scenario texts | Health/disability stereotype prompts |

Data splits respect **bootstrap CI requirements**: ≥1 000 sentences per (language, bias-axis) ensures 95 % CI <0.6 BLEU/NIST.

### 4.6 Evaluation Protocols

• **Automatic metrics**: MBE (gender), classifier-based religion/politics scores, COMET-KIWI for semantic preservation, MCAS for multimodal.  
• **Human evaluation**: Balanced, cross-culture annotator pools; adversarial stress tests modelled after TSST-G to elicit potentially biased behaviour under stress.
• **Statistical rigour**: Bootstrap CIs, permutation tests for metric gains; correlation stabilisation threshold n≈250 (Schönbrodt & Perugini) dictates minimum annotation sample size.
• **Significance reporting**: EMNLP-2014 permutation test to compare correlations; CI width shrink achieved via doubled references where feasible.

### 4.7 Formal Verification

1. **MAP → PROMELA**: prove liveness & absence of deadlock in agent dialogue.
2. **Event-B refinement**: model bias-score variable; prove invariant *bias_total_next ≤ bias_total*.
3. **ASM meta-property**: show MAPE-K loop does not interfere across language-specific sub-loops.

### 4.8 Milestones

| Month | Deliverable |
| --- | --- |
| 0–3 | Data acquisition & triadic sampling; baseline bias measurement |
| 4–6 | MAP-based dialogue engine + SPIN verification |
| 7–9 | Integrate Reinforced Calibration + SCD; first debiasing runs |
| 10–12 | Multimodal MCAS extension; Event-B proofs; public release v1 |
| 13–15 | Large-scale human + automatic evaluation; ablation studies |
| 16–18 | Final benchmarks, paper submission, model & script open-sourcing |

---

## 5 Anticipated Challenges and Mitigations

1. **API rate-limits** – Mitigation: open-weight fallback models, request batching.
2. **Evaluation disagreement** – Use hybrid automatic-human pipeline; apply perceptual threshold analysis from LREC-2010 to flag unstable cases.
3. **Dataset representativeness** – WALS skew addressed via feature reweighting and core-area under-sampling.
4. **Language coverage gaps** – Leverage Cambridge/IARPA hidden-layer augmentation and mBERT lottery-ticket sub-networks for zero-shot.
5. **Reintroduction of bias via multimodal channels** – MCAS monitoring each iteration.
6. **Formal model scalability** – Use compositional verification (ASM decomposition) and confidence-weighted abstraction.

---

## 6 Expected Contributions

• First *formalised* multi-agent, cross-lingual debiasing protocol with machine-checked guarantees.  
• Comprehensive 10-language, 6-axis bias benchmark with statistically robust evaluation.  
• Demonstration that interaction-based methods (SCD + Reinforced Calibration) generalise across cultures and modalities.  
• Open-source toolchain integrating SPIN, Event-B and bias metrics for reproducible ML assurance.  
• Empirical evidence on sample-size thresholds for bias metrics in multilingual settings, extending BLEU/NIST CI literature to bias evaluation.

---

## 7 Speculative Extensions (flagged)

*Speculative*: Integrate physiological stress signals (TSST-G inspired heart-rate, audio prosody) into the agent feedback loop, allowing the system to detect when a user is stressed and dynamically adjust debiasing aggressiveness; explore cultural variance in stress-cue interpretation using N325 ERP cue-reweighting findings.

---

## 8 Key References to Prior Learnings (non-exhaustive)

1. Multilingual Bias Evaluation (MBE) — *arXiv 2205.00551*  
2. MCAS gender image metric — *2024 pre-print*  
3. Social Contact Debiasing — *arXiv 2023*  
4. Reinforced Calibration — *AAAI 2021*  
5. ReConcile multi-agent conference — *arXiv 2309.13007*  
6. Lottery-Ticket mBERT analysis — *ACL 2022*  
7. Formal MAS verification (MAP→SPIN, Event-B+TLA) — *HAL 03159079*  
8. Bootstrap CI guidance — *Koehn et al.; Zhang & Vogel 2004*  
9. WALS skew & triadic sampling — *Focus-Neighbor-Benchmark, 2023*  
10. Transnational-feminist CLIP audit — *Aequitas 2023*

---

### Appendix A Bias-Metric Ensemble Definition

```
BiasScore = w1·MBE_gender + w2·Cls_religion + w3·Cls_politics \
          + w4·SocioEcon + w5·Disability + w6·MBE_language_var
Weights wi are tuned via constrained optimisation s.t. \sum wi = 1 and
corr(BiasScore, human_harm_rating) is maximised on dev set.
```

### Appendix B Event-B Invariant Sketch

```
INV1:  Bias_Total ∈ ℝ ∧ Bias_Total ≥ 0
INV2:  ∀iteration. Bias_Total_next ≤ Bias_Total
THM:   The system terminates when Bias_Total ≤ ε (ε tunable)
```

---

> This report integrates **all prior learnings** into a unified, cross-cultural self-debiasing research blueprint, balancing empirical methodology with formal verification to ensure both effectiveness and trustworthiness of the resulting multilingual LLM systems.

## Sources

- http://journal.iis.sinica.edu.tw/paper/1/120729-2.pdf?cd%3D59363EF5C73728C51
- http://hdl.handle.net/10068/520252
- https://doaj.org/article/18611d725f374aad8059332943856ac8
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-1k37ubu2f2p1k9
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.1732
- http://hdl.handle.net/10.1184/r1/6604934.v1
- https://www.idref.fr/187385661
- https://hal.science/hal-03984522/file/10.1515_lingty-2022-0005-1.pdf
- http://pubman.mpdl.mpg.de/pubman/item/escidoc%3A2044827/component/escidoc%3A2044941/Roberts_2014.pdf
- http://files.eric.ed.gov/fulltext/ED276294.pdf
- https://ir.library.carleton.ca/pub/9602
- http://archive-ouverte.unige.ch/files/downloads/3460/unige_3460_attachment01.pdf
- http://arxiv.org/abs/2012.15375
- http://hdl.handle.net/2086/8969
- https://halshs.archives-ouvertes.fr/halshs-03507171
- http://arxiv.org/abs/2307.01503
- http://homepages.inf.ed.ac.uk/aghoshal/pubs/icassp13-multiling.pdf
- https://arbitrer.fib.unand.ac.id/index.php/arbitrer/article/view/208
- http://hdl.handle.net/11380/742378
- http://hdl.handle.net/2434/373596
- https://figshare.com/articles/Prevalence_of_low_cognitive_and_language_scores_on_the_INTER-NDA_2SD_and_BSID-III_70_Sensitivity_specificity_and_agreement_between_scales_Cohen_s_kappa_/5935315
- https://soundideas.pugetsound.edu/context/thecommons/article/1082/viewcontent/Political_Bias_The_Commons_Draft__6_.pdf
- https://hal-emse.ccsd.cnrs.fr/emse-00745284
- http://skennoch.net/MB_2004_tr.pdf
- https://figshare.com/articles/An_Investigation_on_Initialization_Schemes_for_Multilayer_Perceptron_Training_Using_Multilingual_Data_and_Their_Effect_on_ASR_Performance/6473039
- https://ojs.aaai.org/index.php/AAAI/article/view/17504
- http://hdl.handle.net/2440/17854
- https://figshare.com/articles/_TransNewGuinea_org_An_Online_Database_of_New_Guinea_Languages_/1585942
- https://hal.archives-ouvertes.fr/hal-03159079
- http://proceedings.eldoc.ub.rug.nl/HOME/bnaic/2004/pt1/abstracts/
- https://norma.ncirl.ie/3240/
- https://hal.science/hal-03348492
- https://digitalcommons.mtu.edu/mobiletext/3
- https://doaj.org/article/b6d53b78ae1646d3aca9778da51c97a9
- https://zenodo.org/record/3988998
- http://192.38.112.111/pdf-reprints/Linder_JoB_2012.pdf
- http://www.lrec-conf.org/proceedings/lrec2010/pdf/87_Paper.pdf
- https://ojs.aaai.org/index.php/AIES/article/view/31758
- https://doi.org/10.1016/j.psyneuen.2010.08.004
- https://espace.library.uq.edu.au/view/UQ:205385/s4083658_PHD_Abstract.pdf
- http://hdl.handle.net/123456789/5100
- https://zenodo.org/record/5552686
- https://figshare.com/articles/Pearson_Correlation_Scores_for_Individual_Sample_Groups_Between_NanoString_and_Microarray_p-value_0_001_/3950204
- https://doi.org/10.7910/DVN/2CEYWV
- https://inria.hal.science/hal-03161685
- https://figshare.com/articles/_Comparing_the_false_discovery_rate_fdr_adjusted_obtained_from_an_analysis_of_both_datasets_using_Pearson_correlation_and_using_partial_correlation_and_the_performance_of_their_predictions_in_light_of_the_results_from_the_24_validation_experiments_/709086
- http://hdl.handle.net/11858/00-001M-0000-0028-F42F-C
- https://doaj.org/toc/2405-8807
- https://www.repository.cam.ac.uk/handle/1810/361774
- http://hdl.handle.net/1807/69108
- http://www.upo.es/eps/divina/Publications/aisbVogtDivina.pdf
- https://hdl.handle.net/1959.7/uws:67720
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0888613X96001211/MAIN/application/pdf/bb20d494c741af19a56b61818f1e1932/main.pdf
- https://figshare.com/articles/_The_untransformed_cytokine_levels_pg_ml_measured_in_supernatants_after_24_hours_LPS_stimulation_from_the_healthy_individuals_included_in_this_genome_wide_association_study_/724217
- https://shs.hal.science/halshs-01544597/file/Miller%2027%2004%202017.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17744
- https://zenodo.org/record/1255790
- https://figshare.com/articles/_Awakening_response_in_offspring_and_partners_/353935
- http://www.nusl.cz/ntk/nusl-397887
- http://arxiv.org/abs/2104.07505
- https://figshare.com/articles/Separate_Spheres_Model_of_Gendered_Inequality/1598239
- http://www.casos.cs.cmu.edu/publications/papers/2012ExtractingSocio-culturalNetworks.pdf
- https://hal.inria.fr/hal-03350962/file/adelani_TACL2021.pdf
- http://hdl.handle.net/10.1371/journal.pone.0202789.t006
- http://hdl.handle.net/10.1371/journal.pntd.0010772.s006
- http://www.cslu.ogi.edu/%7Egormanky/courses/CS662/PDFs/lecture_notes/2015-03-03-handout.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/16749
- http://www.clul.ul.pt/equipa/lpereira/variedades_lrec.pdf
- http://dx.doi.org/10.1002/asi.21674
- http://hdl.handle.net/10138/567205
- https://hal.archives-ouvertes.fr/hal-03348492
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050916300576/MAIN/application/pdf/61e5baec6bcf2cce053459a89e3f0bc8/main.pdf
- https://doaj.org/toc/1563-5147
- http://www.david-reitter.com/pub/xu2015evaluation-alignment.pdf
- http://hdl.handle.net/10119/9568
- http://hdl.handle.net/10.6084/m9.figshare.7577987.v1
- http://hdl.handle.net/10119/15434
- https://eprints.ucm.es/id/eprint/59458/1/perez_asurmendi%2Cchiclana_AGOP13.pdf
- http://hdl.handle.net/10.1371/journal.pntd.0010772.s005
- https://ojs.aaai.org/index.php/AAAI/article/view/4631
- http://hdl.handle.net/2434/253216
- http://arxiv.org/abs/2205.00551
- https://hdl.handle.net/20.500.12587/2127
- http://hdl.handle.net/11567/822803
- https://doi.org/10.18653/v1/2020.acl-main.448.
- https://www.persee.fr/doc/aflin_2033-8732_1994_num_11_1_951
- https://hal.inria.fr/hal-03769124/document
- https://zenodo.org/record/7426918
- http://hdl.handle.net/10068/474181
- http://nbn-resolving.de/urn:nbn:de:bvb:19-epub-17968-2
- https://figshare.com/articles/Aggregate_prediction_accuracy_of_re-weighted_algorithms_for_each_ethnic_group_/6951854
- http://hdl.handle.net/10197/12456
- https://figshare.com/articles/_Size_range_of_L1_in_the_human_reference_genome_/852082
- http://maple.cs.umbc.edu/papers/DemocraticApproximationOfLexicographicPreferenceModels.pdf
- https://www.persee.fr/doc/aflin_2033-8732_2015_num_21_1_1044
- https://pub.uni-bielefeld.de/record/2958104
- http://hdl.handle.net/10068/623105
- https://research.tilburguniversity.edu/en/publications/ff874b34-44b9-4d1b-985e-05201d8d37cb
- https://figshare.com/articles/Descriptive_statistics_of_stress_and_cognitive_control_and_their_correlations_/5785125
- https://doi.org10.1016/j.csi.2021.103513
- https://espace.library.uq.edu.au/view/UQ:6f7215f
- http://hdl.handle.net/2066/159577
- http://www.mt-archive.info/MTS-2003-Coughlin.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.4393
- https://hal.archives-ouvertes.fr/hal-00417433
- https://figshare.com/articles/_Correlation_of_scores_with_B_scores_/930283
- http://www.cc.gatech.edu/%7Esimpkins/publications/simpkins2010integrating.pdf
- https://researchmgt.monash.edu/ws/files/488804447/464752463_oa.pdf
- http://arxiv.org/abs/2309.13007
- https://figshare.com/articles/_Analysis_of_FSH_in_control_premanifest_and_stage_II_III_HD_cohorts_/1562970
- https://figshare.com/articles/_Regional_association_plots_showing_8211_log10_p_values_against_base_pair_position_for_Hispanic_HP_women_considering_grade_0_vs_1_8211_3_analyses_/1596141
- https://zenodo.org/record/7502548
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.5075
- https://halshs.archives-ouvertes.fr/halshs-02178112
- http://www.mt-archive.info/NAACL-HLT-2010-Cer-1.pdf
- https://archive-ouverte.unige.ch/unige:157858
- https://rgu-repository.worktribe.com/file/2754840/1/ABEYRATNE%202025%20AlignLLM%20%28AAM%29
- https://research.vumc.nl/en/publications/1cedf2f8-f7c6-490e-accb-07e484e6b615
- https://ojs.aaai.org/index.php/AIES/article/view/31616
- http://ceit.aut.ac.ir/~dehghan/Paper/Conference/ITS2004.pdf
- https://zenodo.org/record/8242092
- http://communication.oxfordre.com/view/10.1093/acrefore/9780190228613.001.0001/acrefore-9780190228613-e-470
- https://figshare.com/articles/Multiple_regression_analysis_predicting_Asian_American_representation_at_the_PhD_level_/3095806
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-383951
- http://www.mt-archive.info/ACL-SMT-2008-Agarwal.pdf
- http://hdl.handle.net/20.500.11910/6778
- https://doaj.org/toc/2460-6952
- https://hdl.handle.net/10356/84707
- http://hdl.handle.net/11576/2637811
- http://msurj.mcgill.ca/vol8/iss1/Goff2013.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.5708
- http://hdl.handle.net/
- https://halshs.archives-ouvertes.fr/halshs-01357537
- http://www.nrcresearchpress.com/doi/abs/10.1139/apnm-2017-0551
- https://hal.archives-ouvertes.fr/hal-00953648
- https://zenodo.org/record/6322643
- http://hdl.handle.net/10068/541548
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1570868305000972/MAIN/application/pdf/a28c6219a96531c844cb548edd13d058/main.pdf
- http://hdl.handle.net/10.1371/journal.pone.0210450.g002
- http://javnost-thepublic.org/article/2014/2/4/
- https://research.rug.nl/en/publications/c2101556-c819-4c66-b685-5817cc38bc6f
- https://shs.hal.science/halshs-00150438/file/millerBergen.pdf
- https://figshare.com/articles/Pearson_correlation_coefficients_and_p-values_for_ADOS_compared_against_regional_rs-BOLD_Z-score_/5730582
- http://dx.doi.org/10.26153/tsw/46055
- https://halshs.archives-ouvertes.fr/halshs-01487214
- http://hdl.handle.net/2066/91348
- https://doras.dcu.ie/29035/1/Gender%20Bias%20in%20Multimodal%20Models%20-%20A%20Transnational%20Feminist%20Approach%20Considering%20Geographical%20Region%20and%20Culture.pdf
- https://hal.science/hal-03812319/document
- https://www.aaai.org/Papers/Workshops/2008/WS-08-07/WS08-07-019.pdf
- https://repo.uum.edu.my/id/eprint/17626/1/ISAMSR%202015%2087-92.pdf
- http://hdl.handle.net/10045/76022
- https://doras.dcu.ie/29470/
- https://figshare.com/articles/Multilevel_regression_models_of_ethnic_diversity_cross-group_friendship_and_generalized_trust_predicting_anti-immigrant_sentiments_/4985027
- https://hal-amu.archives-ouvertes.fr/hal-01796289/document
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:120519
- https://figshare.com/articles/_Correlations_between_Spontaneous_Counterfactual_Generation_Test_and_cognitive_tests_in_HD_patients_/1447322
- http://aff.sagepub.com/content/26/4/395.full.pdf
- http://hdl.handle.net/2440/77360
- https://ojs.aaai.org/index.php/AIES/article/view/31715
- https://insight.cumbria.ac.uk/id/eprint/7322/1/%282022%2C%20December%29%20Intersectionality%20Literature%20Review_Final%20Report.pdf
- https://figshare.com/articles/Results_of_multiple_regression_analyses_predicting_level_of_participation_for_females_number_of_female_participants_by_economic_classification_EC_and_GDP_95_confidence_intervals_for_i_b_i_in_parentheses_/4310447
- https://digitalcommons.kennesaw.edu/context/dataphd_etd/article/1017/viewcontent/Sayenju_PhD_Dissertation.pdf
- http://www.lirmm.fr/~cerri/TEACHING
- https://researchbank.rmit.edu.au/view/rmit:35147
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.9850
- http://hdl.handle.net/2117/105451
- http://arxiv.org/abs/2311.09090
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.7637
- https://escholarship.org/uc/item/5z00b5m9
- http://eprints.imtlucca.it/1571/1/sac2013.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.8967
- https://doaj.org/article/e34578a91bbd405c9da8dc6b647b8c2b
- http://www.oxfordbibliographies.com/view/document/obo-9780199846733/obo-9780199846733-0030.xml.
- http://arxiv.org/abs/2309.04997
- http://email.eva.mpg.de/~gueldema/pdf/AfricanMacro-areasH.pdf
- https://orcid.org/0000-0002-0504-5844
- https://zenodo.org/record/7890715
- http://hdl.handle.net/11581/362798
- http://emnlp2014.org/papers/pdf/EMNLP2014020.pdf
- https://ir.cwi.nl/pub/27296
- https://figshare.com/articles/ThetaW_in_5Kb_interval_in_Africa_an_Middle_East_and_Zscores_outliers_in_Africa_and_Middle_East/1341967
- http://edepot.wur.nl/358275
- http://essuir.sumdu.edu.ua/handle/123456789/11189
- https://www.repository.cam.ac.uk/handle/1810/279181
- https://orcid.org/0000-0002-5275-4192
- http://hdl.handle.net/10138/327794
- https://hal.science/hal-03150686/file/IJCAI.pdf
- https://figshare.com/articles/_The_distribution_of_Noradrenaline_response_to_the_Trier_Social_Stress_Test_among_individuals_/1504545
- https://lirias.kuleuven.be/handle/123456789/543402
- http://hdl.handle.net/11568/94539
- https://figshare.com/articles/_Cortisol_levels_956_g_dl_units_in_adolescents_with_excess_weight_and_adolescents_with_normal_weight_before_and_after_exposure_to_the_Trier_Social_Stress_Task_TSST_/1387409
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/35/14/pone.0099841.PMC4063756.pdf
- https://figshare.com/articles/_Cultural_phylogenetic_results_for_Austronesian_Bantu_and_Indo_European_language_families_/326165
- https://ojs.aaai.org/index.php/AAAI/article/view/26528
- https://eprints.lancs.ac.uk/id/eprint/161023/
- https://figshare.com/articles/_Cultural_variation_in_the_main_finding_/1336908
- https://cris.vtt.fi/en/publications/8dca1f6b-9b92-45d8-b70a-9c6b27890d38
- http://hdl.handle.net/Scatterplots
- https://elischolar.library.yale.edu/ymtdl/1833
- http://arxiv.org/abs/2205.12672
- https://trepo.tuni.fi/handle/10024/213123
- http://edoc.hu-berlin.de/18452/14062
- https://doi.org/10.18653/v1/2022.naacl-srw.19
- https://researchonline.jcu.edu.au/16611/2/16611_Aikhenvald_2011_Book_Cover.jpg
- https://ojs.aaai.org/index.php/AAAI/article/view/26129
- http://urn.kb.se/resolve?urn=urn:nbn:se:oru:diva-20328
- http://www.ifaamas.org/Proceedings/aamas2019/pdfs/p1761.pdf
- http://tubdok.tub.tuhh.de/handle/11420/1565
- https://digitalcommons.winthrop.edu/sewsa/2016/fullschedule/171
- https://orcid.org/0000-0002-9786-8716
- https://figshare.com/articles/_Evening_cortisol_in_offspring_and_partners_/354061
- http://kheafield.com/professional/thesis.pdf
- http://hdl.handle.net/10.1371/journal.pone.0202697.t004
- https://lirias.kuleuven.be/bitstream/123456789/663293/2/RepNetPaper_Final_Version.pdf
- https://halshs.archives-ouvertes.fr/halshs-01681143
- https://doaj.org/toc/1809-452X
- http://www.nusl.cz/ntk/nusl-534105
- http://hdl.handle.net/20.500.11937/62218
- https://doaj.org/article/8b9e1e44157f4ef3916644b2d1676186
- http://cardinalscholar.bsu.edu/handle/handle/178406
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-70252
- https://figshare.com/articles/_Phylogenetic_informative_sequence_variations_/285071
- http://hdl.handle.net/2117/102176