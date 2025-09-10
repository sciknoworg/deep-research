# FairPrompt: Enhancing Fairness in Multilingual Language Models through Culturally-Aware Prompting

*Comprehensive Technical Report – 2025-09-05*

---

## Table of Contents
1. Executive Summary  
2. Precise Problem Formulation  
3. Current State of Research  
   3.1 Theoretical Foundations of Fairness  
   3.2 Dataset & Benchmark Landscape  
   3.3 Mitigation Techniques in Multilingual LMs  
   3.4 Culture-Aware Prompting Evidence  
   3.5 Evaluation & Optimisation Tooling  
4. Proposed FairPrompt Framework  
   4.1 Fairness Objectives & Metrics  
   4.2 Data Assets & Pre-Processing  
   4.3 Prompt-Engineering Strategies  
   4.4 Model-Side Adaptation Modules  
   4.5 Multi-Objective Optimisation Loop  
   4.6 Auditing & Validation Protocol  
5. Experimental Roadmap & Milestones  
6. Open Challenges and Research Opportunities  
7. Conclusions  
8. Appendix A – Consolidated Learning Catalogue  

*(This report collapses more than 70 distinct research learnings into an integrated blueprint. Speculative elements are explicitly flagged.)*

---

## 1. Executive Summary
Multilingual large language models (mLLMs) systematically exhibit *culture-, language- and attribute-specific* biases. Empirical evidence: (i) GPT-4 has the highest rate of culturally inappropriate answers in non-English queries; (ii) state-of-the-art group-robust fine-tuning fails to eliminate demographic-parity and equalised-odds gaps in FairLex; (iii) LoRA debiasing, Social-Contact instruction tuning and culture-aware prompt heuristics each reduce measured bias by ≈30–40 % with negligible perplexity loss.

This report synthesises the literature and designs **FairPrompt**, an end-to-end framework that couples *culturally-aware prompt engineering* with *parameter-efficient adaptation* and *multi-objective Bayesian optimisation* to maximise utility while guaranteeing Rawls-style minima across languages, cultures and protected attributes. Key novelties:

• A prompt-composition grammar that mixes culturally-localised exemplars, continuous directional perturbations (Fair-CDA/CCPA) and Rawlsian Gini-centred hyper-volume search.  
• An expanded *FairLex-GEM* benchmark (≈90 datasets, 51 languages, 7 fairness metrics) plugged into GEMv2’s “living” infrastructure.  
• A dual-loop auditor: fast *ensemble-disagreement* error predictors for in-the-loop monitoring plus periodic human-calibrated evaluations for low-resource scripts.  
• A unified causal-observational fairness lens building on the theoretical equivalence of Counterfactual Fairness and Demographic Parity, allowing practitioners to pick either without loss of generality.

If executed, FairPrompt will deliver (speculative) **≥30 % fairness gain** over strong baselines on at least three cultural axes, while cutting inference latency in low-resource languages by ≈25 % via Cross-lingual Vocabulary Adaptation.

---

## 2. Precise Problem Formulation
We seek to **minimise representational and outcome-level harms** in mLLMs by *prompt-side interventions* that respect cultural context and scale to >50 languages. Formally, given an mLLM `f(·;θ)` and a prompt template `π_L,C` where `L` is language and `C` a cultural context manifold, learn a function `g` (prompt generator / adapter) and optionally adapter weights `Δθ` such that:

1. Utility `U(f∘g)` ≥ baseline utility `U₀` − ϵ  
2. For each protected attribute `A` and language `L`, chosen fairness metric `F` ≤ δ  
3. For each cultural scenario `C`, refusal / harmfulness rate `H` ≤ γ  
4. Inference cost `T` obeys budget `B` (e.g. ≤2× baseline).  

`F` may be Demographic Parity (DP), Equalised Odds (EO) or Rawlsian MinAcc. Equivalence results allow us to pick DP as a proxy for Counterfactual Fairness when causal DAGs are unknown.


---

## 3. Current State of Research
### 3.1 Theoretical Foundations
• **Equivalence of CF & DP** – Any classifier satisfying Counterfactual Fairness (CF) necessarily satisfies Demographic Parity; conversely a DP model can be transformed into a CF-compliant one (AAAI-23).  
• **Identifiability Bottleneck** – Most causal fairness notions are not identifiable unless the full DAG or specific d-separation hold. Partial-DAG algorithms can still enforce fairness when sensitive attributes have no ancestors.  
• **Rawlsian Fairness in mLLM Selection** – Maximin selection over languages produces Pareto-efficient trade-offs without harming high-resource language accuracy.  
• **Strategic Manipulation Aware Fairness** – Optimising for statistical TPR gaps can *increase* feature-editing burden on minorities; direct cost-disparity minimisation alleviates this.

### 3.2 Dataset & Benchmark Landscape
• **FairLex** – Legal-domain fairness benchmark: 4 jurisdictions, 5 languages, 5 sensitive attributes; reveals persistent DP & EO gaps. Race & SES still missing.  
• **GEMv2** – 40 datasets, 51 languages, modular “living” evaluation harness; ideal host for new fairness metrics.  
• **CIVICS** – 2 000+ culturally loaded prompts across five social domains; refusal rate spikes in English.  
• **CLEF Microblog Cultural Contextualisation** – Microblog + event metadata for cultural retrieval.  
• **Cross-lingual Bias Resources** – French CrowS-Pairs, 1 M-sentence socioeconomic bias corpus, Indian-language DisCo, etc.  
• **Legal Corpus Assets** – Fusion-Jena German Legal NER, Figshare “Justice_data”, Bristol “Judgments as Bulk Data”, U Pittsburgh drug-stop opinions.

*Pitfall*: naive translation to low-resource languages introduces polarity shifts and new bias (Urdu sentiment study).

### 3.3 Mitigation Techniques in Multilingual LMs
• **Parameter-Efficient Debiasing** – LoRA; cuts normalized stereotype score by 4.12 pts; bias aligns with perplexity not size.  
• **Social Contact Debiasing (SCD)** – One-epoch instruction tuning on 108 k “contact” prompts → 40 % bias reduction across 13 axes.  
• **Fair-CDA** – Continuous & Directional augmentation; 86 % relative fairness gain on Adult while preserving accuracy.  
• **CCPA** – Continuous Prompt Augmentation + contrastive loss; stronger than standard CFA baselines.  
• **Reinforced Calibration** – RL with bias-aware rewards debiases politically-sensitive generations.  
• **Cross-lingual Bias Projection** – Projects bias directions through embedding spaces, eliminating gender & race bias in languages lacking probes.  
• **Rawlsian Hyper-parameter Optimisation** – Treat fairness metrics as first-class objectives; Pareto tuning drops disparity by >30 % at <2 % accuracy cost.  
• **Cross-lingual Vocabulary Adaptation (CVA)** – Up to 271 % faster generation; maintains accuracy when pre-training is balanced.

### 3.4 Culture-Aware Prompting Evidence
• Additional diverse pre-training *or* lightweight culture-aware prompts lowered culturally inappropriate answer rate by 28 % (Thanksgiving study).  
• CIVICS shows refusal spikes specifically for English wording, revealing language-culture interaction.  
• Ensemble disagreement scoring predicts true error 13.8 % better than silver labels → enables automatic fairness auditing in live prompts.  

### 3.5 Evaluation & Optimisation Tooling
• **LLM-based Evaluators** – Over-score outputs, esp. for non-Latin scripts; require language-specific calibration sets.  
• **LITMUS Predictor** – Estimates zero-shot language accuracy, suggests minimal extra labels to satisfy Rawls minima.  
• **Pareto-Front-Centre Acquisition** – Faster multi-objective Bayesian optimisation focusing on the geometric centre of the Pareto set.

---

## 4. Proposed FairPrompt Framework
### 4.1 Fairness Objectives & Metrics
Mandatory metrics:  
1. **Demographic Parity Gap (DPG)** – primary operational proxy for CF.  
2. **Equalised Odds Gap (EOG)** – secondary classification fairness.  
3. **Representational Bias (RB)** – e.g. cosine distance between sensitive-direction embeddings.  
4. **Rawlsian MinAcc (RMA)** – minimum per-language utility.  
5. **Gini-Coefficient of Accuracy (GCA)** – distributional equity across languages.  
6. **Directional Pairwise Class-Confusion Bias (DPCB)** – catches label-level favoritism.  
7. **Refusal-Harm Rate (RHR)** – culture-specific harmfulness.

### 4.2 Data Assets & Pre-Processing
• **Core Benchmarks** – FairLex-GEM fusion (add FairLex to GEMv2); CIVICS; CrowS-Pairs-FR; Socioeconomic Bias Benchmark; CLEF microblogs.  
• **Legal Augmentations** – Fusion-Jena NER, German compound gold alignments, PANACEA glossary for synonym swaps.  
• **Low-Resource Bootstraps** – Citizen-science translations (LanguageARC, Irish Twitter) + synthetic SCD prompts.  
• **Pre-Processing** – Culture tagging, language-specific tokeniser adaptation, compound-aware masking (German), script-aware vocabulary refresh (Script-Language-Label work). *Speculative*: add LBSN proxies for culture clusters.

### 4.3 Prompt-Engineering Strategies
1. **Cultural Localisation Layer** – Replace Anglo-centric examples with locally authentic scenarios (food, festivals, legal references).  
2. **Continuous Directional Perturbation (Fair-CDA / CCPA)** – Generate attribute-interpolated prompt variants to expose model to demographic axis.  
3. **Soft Counterfactual Prompts** – Ask model to answer “as if the user were …” but evaluate only under DP (equivalence theorem).  
4. **Dynamic Prompt Selection via Ensemble Disagreement** – If predicted error > τ, back-off to a longer culturally enriched template.  
5. **Prompt Campaign Optimisation** – Multi-objective Bayesian search (Pareto-front-centre) over template parameters {language register, role descriptor, example count, style markers}.  
6. **Refusal Mitigation** – For sensitive topics, prepend contact-style instructions (SCD) shown to lower bias without raising refusal.

### 4.4 Model-Side Adaptation Modules
• **Adapter Stack** – LoRA or MAD-G adapters per language family.  
• **SCD Instruction Tuning** – One-epoch fine-tuning on synthetic contact prompts.  
• **CVA Decoders** – Language-specific vocabulary remapping for latency reduction.  
• **Reinforced Calibration** – Small RLHF stage with fairness-aware reward (DPG penalty + utility bonus).  
• **Rawlsian Model Selection** – Among mBERT / XLM-R / distilled monolingual students.

### 4.5 Multi-Objective Optimisation Loop
Repeated until convergence or budget `B`:
1. Sample prompt hyper-parameters with Pareto-front-centre acquisition.  
2. Generate predictions on validation slice.  
3. Estimate utility & bias via calibrated LLM evaluator + ensemble disagreement proxy.  
4. Update Gaussian-process surrogates for objectives {U, DPG, EOG, RHR, latency}.  
5. Periodically adapt LoRA/SCD weights if bias plateaus.

### 4.6 Auditing & Validation Protocol
• **Fast Loop** – Automatic auditing with ensemble disagreement + calibrated evaluator.  
• **Slow Loop** – Native-speaker human review on low-resource languages every 2 weeks; sample via stratified harvesting to maximise surrogate uncertainty reduction.  
• **Causal Stress Tests** – Inject synthetic confounding variables leveraging DCEVAE / VACA to ensure DPG⇒CF equivalence holds in practice.  
• **Manipulation Cost Audit** – Compute feature-editing cost disparity as per strategic manipulation literature.

---

## 5. Experimental Roadmap & Milestones
| Phase | Duration | Deliverables |
|------|----------|--------------|
| 0. Setup | 2 w | Data ingestion, adapter baselines, evaluation harness |
| 1. Prompt Grammar & Localisation | 3 w | 1 000 templates across 10 language families |
| 2. Mitigation Sweep | 4 w | LoRA, SCD, Fair-CDA, CCPA comparisons |
| 3. Bayesian Optimisation | 3 w | Pareto-front-centre search integration |
| 4. Comprehensive Audit | 4 w | Human-calibrated scores, manipulation cost study |
| 5. Ablation & Causal Tests | 2 w | CF vs DP empirical validation |
| 6. Release v1.0 | — | FairPrompt toolkit + extended FairLex-GEM benchmark |

Success KPIs (speculative targets):  
• DPG and EOG ≤ 0.05 on ≥80 % of language-attribute pairs.  
• Rawls MinAcc ≥ 95 % of high-resource baseline.  
• RHR ↓ 25 % vs vanilla prompts on CIVICS.  
• Inference latency ↓ 20 % in low-resource scripts via CVA.

---

## 6. Open Challenges & Research Opportunities
1. **DAG Uncertainty** – Without full causal graphs, DP⇔CF equivalence may fail under hidden confounding; PDAG approaches warrant deeper study.  
2. **Evaluation Calibration at Scale** – Need cost-effective native-speaker judgments for >100 languages; explore active-learning selection.  
3. **Intersectional Metrics** – Current datasets still miss race in FairLex; leveraging “Judgments as Bulk Data” and U Pittsburgh corpora could fill the gap.  
4. **Typological Extremes** – Embedding alignment breaks down for distant pairs; incorporate script-aware adapter re-initialisation.  
5. **Real-Time Fairness Guarantees** – Explore conformal prediction techniques to provide on-the-fly fairness confidence intervals.

---

## 7. Conclusions
The literature demonstrates that fairness in multilingual LMs is *achievable* yet *fragile*. Prompt-side interventions alone can yield ≥28 % bias reduction, but combining them with lightweight model adaptation and principled optimisation delivers substantially larger gains. Leveraging the equivalence between Demographic Parity and Counterfactual Fairness simplifies metric choice, while Rawlsian and Gini criteria guarantee equitable performance distribution.

**FairPrompt** operationalises these insights into a reproducible framework that (i) unifies culturally-aware prompting, (ii) augments with continuous perturbations, (iii) employs parameter-efficient debiasing and (iv) rigorously audits via multi-objective Bayesian optimisation and human-in-the-loop validation. The result is a scalable pathway toward fairer, culturally competent multilingual language technologies.

---

## 8. Appendix A – Consolidated Learning Catalogue
*(Each bullet maps to a source learning; numbers refer to original list ordering where given.)*

1. CF⇔DP equivalence; ranking-preserving baselines beat CF algorithms.  
2. FairLex benchmark – multilingual legal fairness.  
3. Fair-CDA perturbation augmentation (86 % fairness gain).  
4. GEMv2 “living” NLG benchmark (51 languages).  
5. FairLex lacks race & SES coverage.  
6. Robustness to unobserved confounding (additive noise, DCEVAE, VACA).  
7. CLEF Microblog culture datasets.  
8. Bias in legal word embeddings.  
9. English-culture dominance gradient across GPT models; −28 % via culture-aware prompting.  
10. Parameter-efficient debiasing (LoRA, SCD).  
11. Translation-induced sentiment drift (EN→Urdu).  
12. Rawlsian max-min model selection.  
13. Strategic manipulation cost optimisation.  
14. French CrowS-Pairs, socioeconomic bias datasets.  
15. Fusion-Jena German Legal NER.  
16. U Pittsburgh drug-stop opinions corpus.  
17. LLM evaluator over-scoring & need for calibration.  
18. LITMUS Predictor for zero-shot accuracy.  
19. German Legal NER augmented datasets.  
20. Socioeconomic Bias Benchmark (1 M sentences).  
21. CIVICS dataset.  
22. Fairness-aware HPO frameworks.  
23. Gini-based inclusion metric across Indian languages.  
24. Language-technology coverage 3 % statistic.  
25. Unsupervised cross-lingual DNN phone tokenisers.  
26. Bristol “Judgments as Bulk Data”.  
27. Ensemble disagreement scoring.  
28. GPT-3.5 evaluator bias.  
29. Gold standard German compound alignments.  
30. Script-Language-Label discrepancy mitigation.  
31. Indian-language DisCo benchmark.  
32. Legal corpora missing demographic annotations.  
33. Cross-lingual intermediate ASR training.  
34. Multispeech OLR robust ASR ensemble.  
35. Perplexity–bias correlation in LLaMA/OPT.  
36. Monolingual student model distillation.  
37. Participatory cultural mapping via LBSN.  
38. CVA inference-speed gains.  
39. Bias-projection through embedding spaces.  
40. AAAI-21 linguistic fairness Rawlsian study.  
41. AIES-24 stereotype detection in legal embeddings.  
42. Causal fairness risk scoring on German Credit.  
43. CCPA two-stage debiaser.  
44. Hidden-graph counterfactual fairness (PDAG).  
45. Double-Kriging ParEGO extension.  
46. Remaining items folded where redundant with above.

---

*End of Report*

## Sources

- http://hdl.handle.net/11567/1086642
- https://hal.archives-ouvertes.fr/hal-03782735
- https://ojs.aaai.org/index.php/AAAI/article/view/16990
- https://hal.science/hal-03636725/file/Goeuriot_22195.pdf
- http://d-scholarship.pitt.edu/42292/
- https://zenodo.org/record/3893649
- http://hdl.handle.net/10.1371/journal.pone.0205872.t004
- https://zenodo.org/record/8107519
- http://hdl.handle.net/1854/LU-8769631
- https://scholarworks.umass.edu/context/fishpassage_conference/article/2198/type/native/viewcontent
- https://publiscologne.th-koeln.de/frontdoor/index/index/docId/1531
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1042.946
- http://arxiv.org/abs/2305.13862
- https://ojs.aaai.org/index.php/AAAI/article/view/21461
- https://hal.inria.fr/inria-00100687
- https://pub.uni-bielefeld.de/record/2965286
- http://repository.ubn.ru.nl/bitstream/handle/2066/43095/43095.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26706
- http://arxiv.org/abs/2310.12481
- http://hdl.handle.net/10.1371/journal.pone.0216922.t002
- https://zenodo.org/record/6992392
- http://arxiv.org/abs/2307.01503
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-395946
- http://publications.idiap.ch/downloads/papers/2013/Szaszak_COGINFOCOM2013_2013.pdf
- https://hal.science/hal-01913223
- http://arxiv.org/abs/2305.08283
- https://openrepository.ru/article?id=189238
- http://arxiv.org/abs/2204.07661
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.4325
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Pfeiffer=3AJonas=3A=3A.html
- https://www.zora.uzh.ch/id/eprint/207976/
- https://eprints.qut.edu.au/99589/
- https://hal.archives-ouvertes.fr/hal-03792475
- http://orcid.org/0000-0003-1835-9225
- http://hdl.handle.net/2066/178645
- https://zenodo.org/record/6956603
- http://hdl.handle.net/1903/23771
- https://bibliotekanauki.pl/articles/103899
- https://corescholar.libraries.wright.edu/management/53
- https://ojs.aaai.org/index.php/AAAI/article/view/6325
- https://ojs.aaai.org/index.php/aimagazine/article/view/2240
- https://digitalcommons.law.seattleu.edu/faculty/890
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D2330%26context%3Dcompsci
- http://hdl.handle.net/10.6084/m9.figshare.21103021.v1
- https://zenodo.org/record/7603208
- http://www.mt-archive.info/EAMT-2000-Nuebel.pdf
- http://hdl.handle.net/2117/128025
- http://hdl.handle.net/10068/547626
- http://hdl.handle.net/11582/1749
- http://journals.rudn.ru/linguistics/article/view/20613/16692
- https://zenodo.org/record/4081365
- http://scholarbank.nus.edu.sg/handle/10635/40041
- http://dx.doi.org/10.1109/BigData50022.2020.9378308
- http://arxiv.org/abs/2310.18458
- https://inria.hal.science/inria-00100687
- http://cl.naist.jp/%7Ekevinduh/papers/duh12multiobj.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17744
- http://hdl.handle.net/2066/155748
- http://www.lingref.com/cpp/wccfl/26/paper1695.pdf
- http://mirlab.org/conference_papers/International_Conference/ICASSP%201997/pdf/author/ic971383.pdf
- http://hdl.handle.net/10084/127003
- https://figshare.com/articles/_Aggregation_of_data_by_language_family_area_and_country_/1487489
- https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/26327
- https://zenodo.org/record/6956874
- https://ojs.aaai.org/index.php/AIES/article/view/31710
- https://ecollections.law.fiu.edu/diaz-cruz-pamphlets/219
- https://hal.inrae.fr/hal-02734591
- http://www.nusl.cz/ntk/nusl-304321
- https://hal.archives-ouvertes.fr/hal-02964972
- http://hdl.handle.net/2066/37920
- https://doi.org/10.1051/shsconf/202317102017
- http://hdl.handle.net/2066/104451
- https://hal.inria.fr/hal-03911551
- https://intellrobot.com/article/view/5055
- http://scholar.sun.ac.za/bitstream/handle/10019.1/6840/gortz_linguistic_2011.pdf%3Bjsessionid%3DA7CA6ED96673758A53EE44D70D0B0156?sequence%3D1
- https://hdl.handle.net/2152/119143
- http://arxiv.org/abs/2207.01056
- https://hal.archives-ouvertes.fr/hal-01346717
- https://www.open-access.bcu.ac.uk/16136/
- http://www.corpus4u.org/forum/upload/forum/2005092023174960.pdf
- https://qmro.qmul.ac.uk/xmlui/handle/123456789/73098
- http://hdl.handle.net/11567/1086652
- https://pub.uni-bielefeld.de/record/2965712
- http://arxiv.org/abs/2307.01595
- http://hdl.handle.net/20.500.11850/637766
- https://hdl.handle.net/10216/128959
- https://openresearch.surrey.ac.uk/esploro/outputs/conferencePresentation/When-Worlds-Collide-Integrating-Different-Counterfactual/99513642702346
- http://arxiv.org/abs/2203.05900
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:110989
- http://dx.doi.org/10.1177/0003122414562600
- https://pub.uni-bielefeld.de/record/2980967
- https://zenodo.org/record/5532997
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-106986
- http://arxiv.org/abs/2205.13972
- http://hdl.handle.net/10230/19960
- https://www.repository.cam.ac.uk/handle/1810/296683
- https://www.giappichelli.it/algorithmic-conflict-resolution-e-book
- https://research-information.bris.ac.uk/en/publications/1aaa7f12-dfdf-4b2e-8c79-0f8d69c3c8b7
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0885230814001016/MAIN/application/pdf/7c087210ed4577379a141a0c7c718a2f/main.pdf
- https://hal.archives-ouvertes.fr/hal-01309586
- http://arxiv.org/abs/2205.12676
- https://archive-ouverte.unige.ch/unige:38209
- https://ojs.aaai.org/index.php/AAAI/article/view/21736
- https://hal.archives-ouvertes.fr/hal-01822151
- https://ojs.aaai.org/index.php/AIES/article/view/31616
- https://figshare.com/articles/_Mean_scores_for_participants_evaluation_of_the_fairness_of_offers_made_by_attractive_and_less_attractive_proposers_of_the_same_or_the_opposite_sex_Standard_deviations_are_in_parentheses_/989472
- https://hal.inria.fr/hal-03629677
- https://ojs.aaai.org/index.php/AAAI/article/view/26691
- https://rgu-repository.worktribe.com/output/1920683
- http://hdl.handle.net/20.500.11897/459329
- https://zenodo.org/record/6322643
- http://arxiv.org/abs/2309.05619
- https://zenodo.org/record/3964153
- https://research.rug.nl/en/publications/c2101556-c819-4c66-b685-5817cc38bc6f
- http://hdl.handle.net/2381/1406
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-23520
- https://eprints.whiterose.ac.uk/id/eprint/218822/8/2024.findings-emnlp.396.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.3684
- https://hal.science/hal-03812319/document
- https://hal.science/hal-03228823v2/document
- https://eprints.ums.edu.my/id/eprint/33456/1/Comparison%20analysis%20between%20linear%20and%20nonlinear%20models%20to%20predict%20language%20proficiency%20in%20proportion%20to%20language%20learning%20strategy.ABSTRACT.pdf
- https://hdl.handle.net/1813/110502
- https://hal.archives-ouvertes.fr/hal-02347125
- http://www.nusl.cz/ntk/nusl-305131
- http://hdl.handle.net/2066/72676
- http://arxiv.org/abs/2205.10842
- http://hdl.handle.net/10125/74490
- http://opac-caknur.fah.uinjkt.ac.id//index.php?p=show_detail&id=17094
- https://zenodo.org/record/5877746
- http://hdl.handle.net/10.1371/journal.pone.0207741.t001
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.6740
- http://arxiv.org/abs/2205.06356
- https://www.zora.uzh.ch/id/eprint/162622/
- https://ojs.aaai.org/index.php/AIES/article/view/31715
- https://doaj.org/article/8ecb423081884b9ab9ee01a76279ee5e
- https://hal.science/hal-02614855
- https://doaj.org/article/98942ae6df6644309fe317e97b1de1d1
- https://zenodo.org/record/6635194
- https://digitalcommons.kennesaw.edu/context/dataphd_etd/article/1017/viewcontent/Sayenju_PhD_Dissertation.pdf
- http://loic.barrault.free.fr/articles/Barrault-EUROSPEECH2005.pdf
- https://www.persee.fr/doc/ridc_0035-3337_1977_num_29_2_16960
- http://hdl.handle.net/10.6084/m9.figshare.8063186.v2
- https://eprints.whiterose.ac.uk/116618/17/1-s2.0-S0885230816302935-main.pdf
- http://arxiv.org/abs/2311.09090
- http://hdl.handle.net/10.1184/r1/6473039.v1
- https://hal.science/hal-03466171
- http://arxiv.org/abs/2205.12677
- https://hal.science/hal-03091428
- http://lexicometrica.univ-paris3.fr/numspeciaux/special8/Mult1-2013.pdf
- http://hdl.handle.net/20.500.11897/437943
- https://escholarship.org/uc/item/5z00b5m9
- http://www.aclweb.org/anthology/W/W14/W14-3339.pdf
- https://hal.science/hal-03767640
- http://hdl.handle.net/11346/BIBLIO@id=-6622357234668258372
- http://arxiv.org/abs/2310.12560
- https://zenodo.org/record/7890715
- https://zenodo.org/record/4274906
- https://hal.science/hal-04421595/document
- http://dx.doi.or/10.1177/0003122414562600
- http://hdl.handle.net/2117/102165
- https://escholarship.org/uc/item/0441n1tt
- https://figshare.com/articles/Justice_data/1162516
- http://hdl.handle.net/2117/361757
- https://madoc.bib.uni-mannheim.de/52168/
- http://hdl.handle.net/1773/27514
- http://hdl.handle.net/2077/65590
- https://ojs.aaai.org/index.php/AAAI/article/view/5434
- https://lirias.kuleuven.be/handle/123456789/466833
- https://ojs.aaai.org/index.php/AAAI/article/view/26528
- https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/30002
- https://ojs.aaai.org/index.php/AAAI/article/view/17512
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.1126
- https://zenodo.org/record/5168433
- https://inria.hal.science/hal-04355882
- https://zenodo.org/record/3813515
- http://journals.tc-library.org/templates/about/editable/pdf/Wagner
- http://hdl.handle.net/1721.1/58926
- http://www.nusl.cz/ntk/nusl-472415
- https://publications.rwth-aachen.de/record/59767
- https://ojs.aaai.org/index.php/AAAI/article/view/20789
- https://hal.science/hal-01883336/document
- http://hdl.handle.net/1842/3838
- https://ojs.aaai.org/index.php/AAAI/article/view/17505
- https://orcid.org/0000-0001-5736-5930
- http://www.computing.dcu.ie/%7Eebicici/publications/2014/RTMforQE.pdf
- http://hdl.handle.net/2066/91907
- https://ojs.aaai.org/index.php/AAAI/article/view/26183
- https://www.aaai.org/Papers/Symposia/Spring/2004/SS-04-05/SS04-05-001.pdf
- http://www.loc.gov/mods/v3
- http://arxiv.org/abs/2309.07462
- https://hal.archives-ouvertes.fr/hal-03626753/file/EDBT_2022___Masked_Language_Models_as_Stereotype_Detectors_.pdf
- https://hal.inria.fr/hal-03693686
- https://eprints.ucm.es/id/eprint/57348/1/Cid-L%C3%B3pez-Linguistic%20multi-criteria.pdf
- http://arxiv.org/abs/2205.12586
- http://www.openarchives.org/OAI/2.0/oai_dc/
- https://zenodo.org/record/7600568
- https://zenodo.org/record/8112817
- https://zenodo.org/record/22983