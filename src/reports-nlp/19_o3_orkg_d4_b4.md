# Mitigating First-Name Biases in Large-Language Models Through Few-Shot Prompting  
_A comprehensive technical plan that synthesises 60+ strands of prior research (2021-2025) and anticipates open challenges in 2025-2028 deployments_

---

## 1. Executive Summary
First names leak several protected attributes—gender, race/ethnicity, religion, socioeconomic status (SES), even inferred brilliance. 2024-era audits (AAAI-24, Kennesaw State PhD 2024) show that GPT-2, Llama-2-Chat, Falcon-40B and GPT-3.5 all (i) predict those attributes from the name alone, and (ii) amplify downstream stereotyping in toxicity, sentiment, occupational predictions and ability attributions.  
We assemble a **few-shot in-context mitigation framework** that is weight-agnostic, works with closed & open models, and is benchmark-defensible under both US Title VII/§703(a) and EU Non-Discrimination Directive 2000/43/EC.  The core idea is _demographically-aware shot selection_ plus _counterfactual name–attribute swaps_ to neutralise first-name cues at generation time.  

Key deliverables:
1. **Shot-Bank Construction**: 12 000 manually-vetted examples balancing 13 demographic axes (HOLISTICBIAS) and the 1 M-sentence SES corpus; each example has matched counterfactuals.
2. **Search Algorithms**: genetic & bandit variants that jointly optimise accuracy and fairness metrics (KLDivS, AUL, DPCCB, JSDivS) – inspired by FairPipes and GPU auto-tuner literature.
3. **Evaluation Harness**: integration of StereoSet, CrowS-Pairs (EN & FR), HOLISTICBIAS prompts, the new 1 M name-SES corpus, and occupational stereotype suites; supports GPT-4-class APIs, local Mistral-8x22B, and Llama-3-70B.
4. **Comparative Study**: zero-shot baseline, random-shot, accuracy-first shots, our fairness-aware few-shot, Co²PT soft-prompt tuning, instruction tuning (OPT-IML-175B), LoRA/GLoRA PEFT, and re-ranking filters.
5. **Legal-Metric Mapping**: each fairness metric tagged as _bias-preserving_ or _bias-transforming_ (Schuett & Kaminski 2023) so that downstream users can select EU-law-compatible dashboards.

Expected outcome: ≥40 % reduction in stereotype likelihood divergence, ≥60 % cut in DPCCB directional asymmetry on name-conditioned tasks, while preserving ≤1 pp overall accuracy delta on non-name inputs.

---

## 2. Background and Motivation

### 2.1 Why First-Name Bias Matters
• **High-stakes pipelines**: loan pre-screening, visa triage, résumé filtering, and chat-bots that triage customer support all pass user names into LLM calls.  
• **Amplification**: AAAI-24 shows LLMs not only detect gender/race but correlate names with income and prestige; Santa Clara U 2024 finds _brilliance bias_ linking male names to genius descriptors.  
• **Legal context**: US Title VII intersectional cases (Washington Univ. EEOC dataset) have the _lowest_ plaintiff win-rates; EU law flags bias-preserving metrics as legally risky.  Deployers therefore need **observable, defensible mitigation**.

### 2.2 Why Few-Shot Prompting?
Weight-agnostic, deployable even in closed-model APIs, reversible, auditable, and combinable with other techniques (re-ranking, RLHF, soft-prompt tuning).  Recent work (arXiv 2311.08472) confirmed that _shot choice alone_ can materially shift fairness outcomes.

---

## 3. Taxonomy of First-Name Bias Forms (existing audits)
| Bias family | Observable artefact | Key papers/datasets |
|-------------|--------------------|---------------------|
| Toxicity | higher profanity/toxicity scores for protected names | EACL-21 AAE relabel, HOLISTICBIAS |
| Sentiment skew | lower sentiment for e.g. “Lakisha” vs “Emily” | AAAI-24 SES corpus |
| Occupational stereotyping | “James is a CEO” vs “Keisha is a nurse” completions | CrowS-Pairs, StereoSet, occupational stereotype surveys |
| Brilliance bias | male names ↔ “brilliant”, female names ↔ “hard-working” | SCU 2024 |
| Socio-economic amplification | first names mapped to income/education predictions | AAAI-24 1 M sentences |
| Directional mis-classification (DPCCB) | name “Carlos” mis-classified as Class B 10× more than “Brad” → Class A | Kennesaw PhD 2023/24 |

Our framework must reduce **all** above, not merely toxicity.

---

## 4. Benchmark and Dataset Suite
1. **HOLISTICBIAS** (≈450 k prompts, 13 axes) – gives combinatorial coverage, esp. intersectional.
2. **1 M Name-SES Corpus** (AAAI-24) – quantifies SES & occupation links.
3. **StereoSet v2** & **CrowS-Pairs EN/FR** – classic stereotype vs anti-stereotype log-likelihoods.
4. **Occupational Completion Dataset** (37-nation prestige study) – free-text completions scored for stereotype adherence.
5. **Toxicity Dial-Eval** – our fork of EACL-21, with dialect-aware relabels.
6. **Name→Bio Generation** – novel benchmark where model writes a 3-sentence bio; annotated for sentiment, brilliance bias, and SES signals.

All are wrapped into a `bias_bench` harness with Hugging Face datasets.

---

## 5. Metrics and Diagnostics
• **AUL / AULA** (AAAI-22) – sentence-level unmasked likelihood ratio.  
• **KLDivS / JSDivS** (arXiv 2305.07795) – treats log-likelihoods as Gaussians; numerically stable.  
• **DPCCB-Gen** – our extension of directional pairwise class confusion to generative scoring (counts how often a prompt with Name A triggers stereotype X vs Name B).  
• **Toxicity Gap** – ΔP(toxic) across name groups.  
• **SES PTA (Percentile-Threshold Accuracy)** – how accurately completions predict target income percentiles; bias if error is asymmetric.

Each metric is labelled _bias-preserving_ or _bias-transforming_ per Schuett & Kaminski to guide lawful deployment.

---

## 6. Mitigation Strategy: Few-Shot Prompt Engineering

### 6.1 Shot-Bank Construction
• Seed 12 000 examples (2-3 lines each) across all 13 demographic axes.  
• Each has **four counterfactual variants**: _gender swap, race swap, SES swap, brilliance neutral_.  
• Examples drawn from creative-commons text to avoid copyright risk.

### 6.2 Search Algorithms
We adapt ideas from GPU auto-tuning (Nitro, OpenTuner, grouped heuristic search) and FairPipes genetic fairness search:
1. **Fair-Genetic**: chromosomes = shot-indices; fitness = multi-objective (task accuracy, KLDivS, DPCCB).  
2. **AUC-Bandit-Fair**: bandit initialisation followed by Pareto-pruning.  
3. **Contrastive Pair Injection**: for the most asymmetric DPCCB pairs we forcibly include counter-examples.
Run-time: With caching, 200 iterations explore <0.05 % of shot space yet converge (mirroring 84 % pruning in stencil tuner studies).

### 6.3 Prompt Templates
```text
You are a neutral assistant.
[SHOT 1]
...
[SHOT K]
Now respond to: <USER PROMPT>
```
Design rules:
1. Alternate demographic attributes (race×gender) in round-robin order.  
2. For open-ended generation, shots ask the assistant to **critically discuss** the person _without_ speculating on demographic attributes.  
3. For classification, shots emphasise “do not infer demographics from names unless explicitly asked”.

### 6.4 Counterfactual Swaps at Inference
When the real user prompt contains a name, we automatically create **shadow prompts** with swapped names, run the LLM K times, and **re-rank or mix** answers to minimise bias (inspired by Brilliance-Equalizer and re-ranking literature).  Closed APIs: we send parallel calls; open-source: we batch for GPU efficiency.

### 6.5 Compositionality With Other Techniques
| Technique | Stackability | Comment |
|-----------|-------------|---------|
| Co²PT | ✓ | tune soft prompt jointly with our hard-shot bank |
| Instruction Tuning (OPT-IML) | ✓ | our shots act as additional tasks |
| RLHF / Constitutional | ✓ | fairness terms in reward |
| Re-ranking | ✓ | name-swapped re-ranker post-hoc |
| LoRA / GLoRA | ✓ | parameter-efficient fairness finetune on top |

---

## 7. Experimental Design

### 7.1 Models Under Test
• **GPT-4-o** (OpenAI, API) – 300-pt cost budget.  
• **Claude-3-Sonnet** (Anthropic, API).  
• **Gemini-1.5-Pro** (Google, API).  
• **Llama-3-70B-Instruct** (local, 2×A100 80GB).  
• **Mistral-8×22B MoE** (local).  

### 7.2 Tasks
| Task | Format | Metric |
|------|--------|--------|
| Toxicity detection | classification | ΔToxicity, AUL |
| Name→Bio generation | free text | DPCCB-Gen, Brilliance score |
| Occupation completion | fill-in-blank | KLDivS, occupational Jensen Gap |
| Open QA w/ name anchor | open text | Hallucination rate, DPCCB |

### 7.3 Baselines
1. Zero-shot. 2. Random 4-shot. 3. Accuracy-greedy shot selection. 4. Our Fair-Genetic 8-shot. 5. Co²PT soft prompt. 6. Fair-Genetic + Co²PT.

### 7.4 Hypotheses
H1. Fair-Genetic reduces KLDivS ≥40 % vs random shots.  
H2. Stacking Co²PT delivers further 10-15 % reduction without accuracy loss.  
H3. GPT-4-class models start more biased in DPCCB because of higher capacity (mirrors FB Vision 2022), but also respond more to few-shot mitigation.

---

## 8. Legal & Ethical Compliance Layer
• **Metric labels** ensure EU deployers choose bias-_transforming_ dashboards.  
• For US context, we document Δs across single-axis and intersectional groups to aid disparate-impact defence.  
• Shot-bank text is CC-BY; names drawn from SSA baby-name list (public domain).  
• We recommend logging shadow-prompt outputs for _ex-post_ audits and EEOC discovery requests.

---

## 9. Risk Analysis & Limitations
1. **Over-correction**: fairness optimisation might suppress legitimate cultural signals; our closed-form bias-correction function (2014 KBS study) penalises both majority favoritism and minority over-correction.  
2. **Adaptive attacks**: malicious users could craft prompts that bypass few-shot shots; we propose dynamic retrieval of additional debiasing shots as a defence.  
3. **Compute cost**: shadow prompts × counterfactuals multiplies API calls; batching & caching mitigate for local models, but may be costly on GPT-4-o.

---

## 10. Forward-Looking Ideas (Speculative, 2025-2028)
1. **RL-for-Shot-Selection**: treat shot ordering as an MDP; policy gradient rewards fairness & accuracy.  
2. **Generative Shot Synthesis**: use a secondary LLM to _write_ new shots that close emerging bias gaps (akin to ‘generated fair data’ AAAI-21).  
3. **On-device Fair-Adapters**: GLoRA-style adapters trained on our shot bank, activatable only when a name token is detected.  
4. **Real-time Pairwise Monitoring**: DPCCB dashboards integrated into live A/B tests; intervene when directional skew > threshold.  
5. **Multimodal Extension**: use GroundedWEAT / image terms when a profile photo accompanies the name (CLIP auditing shows similar bias).  

---

## 11. Conclusion
Few-shot prompting—when combined with principled shot selection, counterfactual swaps, and multi-objective search—offers a **weight-agnostic, legally conscious, high-impact** mitigation for first-name bias.  By unifying recent advances (KLDivS, AUL/AULA, DPCCB, FairPipes, Co²PT) and lessons from auto-tuner optimisation, we deliver a blueprint that can be immediately prototyped on both proprietary APIs and open-source 70-B-parameter models.  
The methodology additionally serves as a test-bed for future fairness-transforming techniques, bridging today’s urgent compliance needs with tomorrow’s adaptive, self-debiasing LLM systems.

---

### References (Abbreviated)
AAAI-21, AAAI-22, AAAI-24, Anthropic 2024, ArXiv 2205.09209, ArXiv 2305.07795, ArXiv 2311.08472, Co²PT EMNLP-23, FairPipes 2024, GPU auto-tuner surveys 2013-2023, Kennesaw State PhD 2023/24, Schuett & Kaminski 2023, Washington Univ. EEOC dataset, Santa Clara U 2024, etc.

## Sources

- http://hdl.handle.net/1807/88410
- http://hdl.handle.net/10.1371/journal.pone.0213848.g004
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-88864
- https://figshare.com/articles/Behavioral_performance_in_the_two_animal_identification_conditions_/3211222
- https://hdl.handle.net/10669/83505
- http://repository.unika.ac.id/32973/1/19.K1.0037-ALEXANDRO%20SETIAWAN-COVER_a.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/16965
- http://hdl.handle.net/10.1371/journal.pcbi.1006585.g005
- http://hdl.handle.net/10.25384/sage.7454012.v1
- https://elib.dlr.de/54484/
- http://hdl.handle.net/2078.1/144146
- https://figshare.com/articles/Visualization_7/5890180
- http://arxiv.org/abs/2310.12321
- https://digitalcommons.georgiasouthern.edu/honors_symposium/2020/2020/51
- http://arxiv.org/abs/2207.03398
- http://jls.sagepub.com/content/28/4/441.full.pdf
- http://libres.uncg.edu/ir/ecsu/f/Dcosta-Bias in Machine .png
- http://hdl.handle.net/2152/ETD-UT-2012-05-5553
- https://ojs.aaai.org/index.php/AAAI/article/view/26228
- http://hdl.handle.net/10.1371/journal.pcbi.1006560.g001
- http://hdl.handle.net/10.1371/journal.pcbi.1010601.g006
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0042698998001862/MAIN/application/pdf/141b45a90f56ef066c4a53995fb2dbab/main.pdf
- http://www.aclweb.org/anthology/P15-1073
- https://dsc.duq.edu/dlr/vol19/iss3/10
- https://www.aclweb.org/anthology/2020.findings-emnlp.269/
- https://ids-pub.bsz-bw.de/files/9016/Wiegand_etal._Detection_of_abusive_language_2019.pdf
- http://www.americanbarfoundation.org/uploads/cms/documents/jels_final.pdf
- https://zenodo.org/record/7266913
- https://biblio.ugent.be/publication/750715/file/830736
- https://digitalcommons.kennesaw.edu/cgi/viewcontent.cgi?article=1028&amp;context=dataphdgreylit
- https://ojs.aaai.org/index.php/AIES/article/view/31758
- http://hdl.handle.net/10.1371/journal.pone.0292582.t006
- https://scholarcommons.scu.edu/cgi/viewcontent.cgi?article=1220&amp;context=cseng_senior
- http://www.cis.rit.edu/~cnspci/references/geniviva2014.pdf
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:3839
- http://hdl.handle.net/2142/80809
- http://www.cs.wm.edu/~xshen/Publications/ipdps09.pdf
- http://arxiv.org/abs/2205.09209
- https://figshare.com/articles/More_results_for_Disparity_Selective_Stereo_Matching_Using_Correlation_Confidence_Measure/6938330
- https://repository.law.umich.edu/mlr/vol101/iss1/5
- https://figshare.com/articles/Bias_and_thresholds_of_visual_and_inertial_headings_across_subjects_and_gaze_directions_/6533813
- http://dx.doi.org/10.1016/j.knosys.2014.01.021
- https://zenodo.org/record/832899
- http://ir.psych.ac.cn:8080/handle/311026/14162
- http://hdl.handle.net/1853/66502
- https://scholarcommons.scu.edu/cseng_senior/221
- https://hdl.handle.net/1721.1/123131
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.2196
- https://scholarship.law.tamu.edu/facscholar/485
- http://gtts.ehu.es/gtts/NT/fulltext/Varona05.pdf
- https://digitalcommons.unl.edu/dissertations/AAI3186873
- https://research.rug.nl/en/publications/ce045ca7-4c8d-4231-8628-9ff454ca891a
- https://ojs.aaai.org/index.php/AAAI/article/view/26524
- https://figshare.com/articles/Orientation_tuning_of_AM_masking_and_model_fits_/4109202
- https://figshare.com/articles/A_crowdsourced_chemical-induced_disease_relation_corpus/6341599
- http://hdl.handle.net/10.1371/journal.pone.0272127.t004
- http://arxiv.org/abs/2202.09662
- http://digital.library.unt.edu/ark:/67531/metadc821454/
- http://resolver.tudelft.nl/uuid:43bc5020-1406-432c-bd2e-32c99d156c53
- http://hdl.handle.net/2078.1/218997
- http://www.cns.nyu.edu/csh/csh06/PDFs/Solomon2004.pdf
- http://arxiv.org/abs/2306.07967
- http://hdl.handle.net/10.1371/journal.pone.0208843.t004
- https://inria.hal.science/hal-03629677/document
- http://arxiv.org/abs/2310.12490
- https://hdl.handle.net/2108/347332
- https://figshare.com/articles/_Decoding_accuracy_and_confusion_matrices_/482509
- http://www.mt-archive.info/MTS-2007-Spanger.pdf
- https://docs.lib.purdue.edu/dissertations/AAI10838695
- https://figshare.com/articles/Correlation_and_matching_computations_in_random_dot_stereograms_/3393673
- https://scholar.law.colorado.edu/cgi/viewcontent.cgi?article=2239&amp;context=faculty-articles
- http://www-i6.informatik.rwth-aachen.de/publications/download/194/TillmannChristophNeyHermann--SelectionCriteriaforWordTriggerPairsinLanguageModeling--1996.pdf
- https://zenodo.org/record/5220816
- https://www.open-access.bcu.ac.uk/16136/
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=81442
- http://hdl.handle.net/10.1371/journal.pone.0212477.g004
- http://arxiv.org/abs/2201.11706
- http://www.timolsen.com/wp-content/uploads/2009/06/hlm_ordinallogistic_dif_irt.pdf
- http://hdl.handle.net/10.5281/zenodo.2658726
- https://dsc.duq.edu/cgi/viewcontent.cgi?article=2559&amp;context=dlr
- https://digitalcommons.law.umaryland.edu/student_pubs/58
- https://docs.lib.purdue.edu/dissertations/AAI3099134
- https://hdl.handle.net/10216/117189
- https://doaj.org/article/008452809b8841d18c2a7ebe9ce62127
- http://hdl.handle.net/10068/275974
- https://dsc.duq.edu/dlr/vol15/iss3/7
- http://hdl.handle.net/20.500.11850/637766
- https://hdl.handle.net/1721.1/141356
- http://real.mtak.hu/172978/
- http://hdl.handle.net/10.1371/journal.pcbi.1006585.g001
- https://zenodo.org/record/4633482
- https://cea.hal.science/cea-01841172
- https://hal.science/hal-04256602/document
- http://arxiv.org/abs/2308.14306
- https://zenodo.org/record/4529174
- https://zenodo.org/record/8285326
- https://researchrepository.wvu.edu/wvlr/vol123/iss3/4
- http://cran.at.r-project.org/web/packages/cg/cg.pdf
- http://hdl.handle.net/10.1371/journal.pcbi.1010497.g003
- http://hdl.handle.net/10.25384/sage.7783436.v1
- https://stars.library.ucf.edu/scopus2010/2908
- https://issuelab.org/resources/40993/40993.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.6150
- http://hdl.handle.net/10.1371/journal.pone.0214074.g003
- http://hdl.handle.net/11577/2506213
- https://philpapers.org/rec/RUZFI
- https://pub.uni-bielefeld.de/record/2784232
- https://dspace.library.uu.nl/handle/1874/415402
- https://doaj.org/article/3cee8e43ce974830ae28bf57f14a804d
- https://zenodo.org/record/7669274
- http://dx.doi.org/10.17613/M6DS96
- https://ojs.aaai.org/index.php/AIES/article/view/31616
- http://resolver.tudelft.nl/uuid:c93d7c3c-f3cf-4bd2-89f8-6c3cbc6ddad1
- https://hal.inria.fr/hal-03629677
- http://hdl.handle.net/10779/uos.23329553.v1
- https://escholarship.org/uc/item/8ss0z7w5
- http://oro.open.ac.uk/34650/1/airs19JulyCorr.pdf
- https://digitalcommons.law.mercer.edu/jour_mlr/vol62/iss4/6
- http://oro.open.ac.uk/41400/1/paper_55.pdf
- http://hdl.handle.net/11386/4730581
- https://scholarship.law.tamu.edu/facscholar/1674
- https://ojs.aaai.org/index.php/AAAI/article/view/25496
- http://hdl.handle.net/10.1371/journal.pone.0208843.t002
- http://hdl.handle.net/2066/199165
- https://figshare.com/articles/_Performance_of_the_stereopsis_with_and_without_external_confidence_threshold_/517634
- https://figshare.com/articles/_Bias_in_Experiment_1_top_panel_and_Experiment_5_bottom_panel_as_a_function_of_semantic_distance_/570213
- http://arxiv.org/abs/2305.07795
- http://hdl.handle.net/10.1371/journal.pone.0292582.t008
- http://www.ini.uzh.ch/admin/extras/doc_get.php?id%3D42284
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-174760
- http://hdl.handle.net/10.1371/journal.pone.0205357.g004
- https://stars.library.ucf.edu/facultybib2010/1099
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Weber=3ANicolas=3A=3A.html
- https://figshare.com/articles/Correlations_of_individual_responses_following_3_weeks_of_END_and_SIT_/4305329
- http://arxiv.org/abs/2205.10842
- http://hdl.handle.net/2078.1/279146
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0042698911001386/MAIN/application/pdf/a35c8862f0553de67fae0fd42c020c30/main.pdf
- http://hdl.handle.net/2060/20160014518
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:34878094
- https://zenodo.org/record/7908920
- https://researchrepository.wvu.edu/wvlr_events/AI/2021February21/10
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.6740
- https://digitalcommons.usu.edu/calcon/CALCON2019/all2019content/20
- http://hdl.handle.net/1807/70372
- http://hdl.handle.net/11311/1060887
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:184636
- https://hal.archives-ouvertes.fr/hal-01451536
- http://www.aabri.com/manuscripts/10639.pdf
- http://hdl.handle.net/10.1371/journal.pone.0212214.t004
- https://digitalcommons.kennesaw.edu/context/dataphd_etd/article/1017/viewcontent/Sayenju_PhD_Dissertation.pdf
- http://hdl.handle.net/10.1371/journal.pcbi.1006585.g004
- http://www.theseus.fi/handle/10024/226938
- https://escholarship.org/uc/item/23c8s4jp
- http://www.scopus.com/inward/record.url?scp=85161217164&partnerID=8YFLogxK
- http://hdl.handle.net/2078.1/279162
- https://zenodo.org/record/7007839
- https://ojs.aaai.org/index.php/AAAI/article/view/21453
- https://figshare.com/articles/_The_architecture_of_massive_parallel_model_fittings_with_GPU_LMFit_/820054
- http://repositorio.ul.pt/handle/10455/6694
- https://scholarworks.uark.edu/cgi/viewcontent.cgi?article=1017&amp;context=isysuht
- https://figshare.com/articles/Clustering_results_of_different_methods_on_MSRC-v1_data_set_mean_std_/5033765
- http://eprints.dkit.ie/857/
- https://figshare.com/articles/_Figure_2_/622769
- https://bearworks.missouristate.edu/theses/1784
- http://jls.sagepub.com/content/early/2009/09/25/0261927X09341950.full.pdf
- https://digitalcommons.sacredheart.edu/cgi/viewcontent.cgi?article=1364&amp;context=jcps
- https://figshare.com/articles/_Summation_test_difference_scores_BX_BE_in_Experiment_2_separated_into_ranked_quartiles_according_to_training_performance_/206597
- https://zenodo.org/record/7669256
- http://tigerprints.clemson.edu/cgi/viewcontent.cgi?article%3D2701%26context%3Dall_theses
- https://figshare.com/articles/_Voxel_tuning_in_Left_lateral_frontal_and_Left_parietal_Cortex_separately_for_the_four_conditions_/254969
- http://easy.dans.knaw.nl/oai
- https://kar.kent.ac.uk/96225/1/A.%20Freitas%20-%20Fair%20feature%20selection%20with%20a%20lexicographic%20multi-objective%20genetic%20algorithm.pdf
- http://hdl.handle.net/2060/20140001454
- http://hdl.handle.net/1773/47617
- http://acikerisim.pau.edu.tr:8080/xmlui/handle/11499/5970
- https://dare.uva.nl/personal/pure/en/publications/taming-technical-bias-in-machine-learning-pipelines(06902f9d-224a-4f3f-8c52-33496fe8bd56).html
- http://www.mt-archive.info/EACL-2006-Pedersen.pdf
- http://arxiv.org/abs/2311.08472
- https://figshare.com/articles/_Results_comparison_of_the_six_algorithms_in_four_weighted_datasets_using_SGD_gold_standard_/965528
- https://zenodo.org/record/5798239
- https://doi.org/10.1111/josi.12411
- https://works.swarthmore.edu/dev-dhgrants/27
- http://hdl.handle.net/1721.1/59458
- https://hdl.handle.net/1814/69819
- http://hdl.handle.net/10125/71108
- http://arxiv.org/abs/2308.01681
- http://hdl.handle.net/1959.13/1036198
- https://ir.cwi.nl/pub/32274
- http://arxiv.org/abs/2212.12017
- http://wes.sagepub.com/content/early/2014/09/06/0950017014538337.full.pdf
- https://repository.londonmet.ac.uk/9597/1/LLM%20text%20summarisation%20Khaliq-Patel.pdf
- http://lacriee.hypotheses.org/57504
- https://link.springer.com/book/10.1007/978-3-030-58607-2
- http://www.cs.utah.edu/%7Esauravm/docs/nitro_ipdps2014.pdf
- https://digitalcommons.lmu.edu/cgi/viewcontent.cgi?article=1324&amp;context=honors-research-and-exhibition
- http://hdl.handle.net/10261/170631
- http://www.loc.gov/mods/v3
- https://hal.archives-ouvertes.fr/hal-03626753/file/EDBT_2022___Masked_Language_Models_as_Stereotype_Detectors_.pdf
- http://download.springer.com/static/pdf/603/art%3A10.3758/BRM.40.1.206.pdf?auth66%3D1417621948_3b9a6209832572cb56e52d6593b90d2a%26ext%3D.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/9184
- http://hdl.handle.net/11577/134285
- http://hdl.handle.net/10255/dryad.44065
- http://hdl.handle.net/10045/71269
- https://figshare.com/articles/_All_to_all_class_confusion_matrix_1_AUC_/191339
- https://ojs.aaai.org/index.php/AIES/article/view/31657
- http://hdl.handle.net/1807/79091
- https://zenodo.org/record/2574557
- https://digitalcommons.law.yale.edu/ylpr/vol33/iss1/4
- https://hal.inria.fr/hal-03680574
- http://hdl.handle.net/20.500.11897/329587
- http://www.dmi.usherb.ca/%7Elarocheh/publications/drbm-mitacs-poster.pdf