# Final Report  
## Automatic Jailbreak Prompt Generation & Robustness Assessment for Large Language Models  
---  
### Prepared 05 Sep 2025  

**Author-note** – The user has not yet specified which of the three foci (attack generation, robustness measurement or defense design) is paramount, therefore this document treats *all three* dimensions in depth and adds implementation-level prescriptions.  

---
## 1. Executive Summary  
A decade of red-teaming research shows that *prompt-level* attacks remain the dominant alignment failure mode of deployed LLMs. 2023–2025 work introduced:  
* **Fully-automatic attack frameworks** (ReNeLLM, *Open Sesame!*, *Self-Deception*, Chain-of-Utterances) whose success rates exceed 60 % on GPT-4-class models and 90 % on open-source checkpoints;  
* **Compact, high-recall guardrails** (Mixture-of-Jailbreak-Experts – MoJE, RA-LLM, goal-prioritised inference) that reduce Attack-Success-Rate (ASR) on frontier models from ≈70 % to <10 % with negligible latency or training cost;  
* A **persistent dataset & evaluation gap** – no standard, CC-compliant jailbreak corpus exists; the community repurposes vulnerability, GUI-testing or code-generation sets, hampering reproducibility.  
The remainder of this report consolidates *every* research learning provided, maps them onto an end-to-end pipeline for automatic prompt generation and defense assessment, and finishes with concrete engineering recommendations.  

---
## 2. Attack Landscape 2023-2025  
### 2.1 Taxonomy of Automatic Jailbreak Methods  
| Class | Representative Works & Key Ideas | Reported Performance | Notes |
|-------|---------------------------------|----------------------|-------|
| **Gradient-free black-box** | *Open Sesame!* (Sept 2023) evolves a *single* adversarial suffix via a genetic algorithm; transfers across ChatGPT, GPT-4, Claude. | >90 % on GPT-3.5, 80 % on GPT-4 (no defence). | No weight/logit access; ideal stress-test. |
| **LLM-in-the-loop self-composition** | **ReNeLLM** (2024) reframes jailbreak as *Prompt Rewriting + Scenario Nesting* and lets an LLM recursively chain these ops. | Outperforms all prior manual/white-box attacks in both success rate and wall-clock. | Demonstrates that *capability ↑ ⇒ vulnerability ↑*. |
| **Conversation chain exploitation** | Chain-of-Utterances (RED-EVAL 2023) & six-month *in-the-wild* scrape (Li et al.) show two reusable templates achieving 0.99 ASR and evading defences >100 days. | 65–99 % on GPT-4/3.5. | Highlights need for longitudinal monitoring. |
| **Multi-lingual semantic tunnelling** | *Self-Deception* corpus (2 520 payloads, 6 languages) reported 86 % ASR on GPT-3.5, 67 % on GPT-4; later erratum questions exact numbers. | Multilingual risk persists; emphasises cross-lang evaluation. | |

### 2.2 Scaling & Transferability Observations  
1. Larger models (GPT-4) are **more vulnerable yet more steerable** – an empirical non-linearity later leveraged by goal-prioritisation defence.  
2. Black-box evolved suffixes (*Open Sesame!*) **transfer** across closed vs. open models, exposing architecture-agnostic weaknesses.  
3. **Temporal durability** – Li et al.’s scrape proves that once shared privately, a high-success prompt can persist >3 months before filters adapt.  

### 2.3 Gaps  
* **Dataset deficit**: No permissively licensed, standard jailbreak benchmark (PromptBench is small & non-CC).  
* **Evaluator bias**: Deception-detection studies show “investigator bias” – specialised raters over-label without ↑ accuracy. Equivalent risk exists for jailbreak labelling.  

---
## 3. Defence & Detection State of the Art  
### 3.1 Lightweight Input-Side Filters  
* **Mixture-of-Jailbreak-Experts (MoJE)** – AAAI AIES 2024, detects ≈90 % of attacks via *surface-level linguistic statistics*: perplexity, token-type ratio, function-word frequency, unseen-token flags.  
  * Tabular naïve classifiers ⇒ **constant-time inference**; near-zero latency, suitable for on-device or edge.  
  * Feature importance: perplexity + token-type ratio strongest, demonstrating deep semantics often unnecessary.  
* **Prototype-Expert variants** (Mixture-of-Random-Prototype Experts) could further cut FLOPs w/out accuracy loss.  

### 3.2 Response-Side & Training-time Steering  
* **Goal-Prioritised Decoding / Training** (Tsinghua COAI 2023) – explicitly rank *safety > helpfulness*.  
  * *Inference-only*: ChatGPT ASR 66 %→2 %; Vicuna-33B 68 %→19 %.  
  * *Training-incorporated*: Llama-2-13B 71 %→6 %. Even w/o jailbreak data ASR halves (34 %).  
* **Robust-Alignment-LLM (RA-LLM)** – post-hoc “robust alignment check” wrapper; cuts ASR ≈100 %→10 % on open models.  

### 3.3 Ensemble & Statistical Approaches  
* **MoJE** outperforms neural guards (PromptBench/AutoDAN) at a *fraction* of compute.  
* **Analytical Bias-Reduction** for Gaussian quadratic experts (Canada NRC 2023) reduces over-confidence – transferrable to guardrail fusion.  
* Cross-domain evidence (malware ensembles, α-count schemes) shows heterogeneous detectors + tuned window length ↓ detection delay; suggests multi-expert guardrails for jailbreaks.  

### 3.4 Operational Considerations  
* Real-time constraints mirror telecom & datacenter findings:  
  * **Reference Latency Interpolation (RLI)**, **Lossy Difference Sketch (LDS)**: router-embedded, low overhead; analogy – LLM guardrails must be *compute-thrifty* like RLI for micro-second SLA workloads.  
  * LTE/5G handover algorithms (PBHA, REM-driven, PSO-optimised) show **dynamic thresholding** beats static policies – a design cue for adaptive safety thresholds.  
* **Edge deployment** lessons: lightweight ensembles beat heavier nets on IoT malware ↔ same trade-off favourable for on-device guardrails (phones, AR glasses).  

### 3.5 Known Limitations  
* Language coverage – intra-word code-switching (Dutch-Limburgish) & JSpeech corpus work show detection models must handle sub-token mixing.  
* Non-text modalities – phonetic / vision TBD fusion not yet applied to voice or image-prompt jailbreaks.  

---
## 4. Benchmarking & Datasets  
### 4.1 Existing Artefacts  
| Dataset / Tool | Size | Licence | Coverage | Notes |
|----------------|------|---------|----------|-------|
| **PromptBench / AutoDAN** | ≈10 k prompts | restrictive | text EN | Used by MoJE; lacks multilingual & voice. |
| **Self-Deception corpus** | 2 520 prompts | unclear | 6 languages | Erratum; still useful for multi-lang eval. |
| **Li et al. scrape** | 6 387 in-the-wild + 46 800 test prompts | research use | 13 scenarios | High realism; no CC licence. |
| **HARMFUL-QA, RED-EVAL** | 9.5 k safe + 7.3 k harmful conv.; 46 k queries | CC-BY-NC 4.0 | safety tasks | Indirectly useful for jailbreak eval. |

### 4.2 Licensing & Redistribution Constraints  
* *Red Hat JBoss EAP* guide under CC-BY-SA 3.0 but w/ waiver; *GitHub Project Dataset for License Analysis* helps identify CC-compliant text.  
* Lack of permissive corpora hinders sharing; need CC-BY-SA-4.0 or Apache-2.0-equivalent datasets.  

### 4.3 Proposal – Standardised **JailbreakBench-XL**  
1. Seed with public domain or CC-0 sources (e.g., Project Gutenberg) to avoid licence conflicts.  
2. Generate multilingual, multi-modal prompts via ReNeLLM.  
3. Annotate with MoJE + human triage to control investigator bias; use Signal-Detection-Theory mapping (Bader & Häussler) to convert continuous acceptability to binary labels.  
4. Publish on Zenodo with versioning like **CrossCodeBench** & **CIBench** for reproducibility.  

---
## 5. Implementation Blueprint  
### 5.1 System Architecture  
```
┌───────────────────────────────────────────────────────────┐
│ 1  Attack Generator (AG)                                 │
│   • ReNeLLM self-chaining                                │
│   • Open Sesame GA suffix evolution                      │
│   • Multi-lingual Scenario Templates (Self-Deception)    │
└──────┬────────────────────────────────────────────────────┘
       │ prompts
┌──────▼────────────────────────────────────────────────────┐
│ 2  Target Executor (TE)                                  │
│   • Batch API to GPT-4o, Claude-3, Llama-3 70B-Instruct   │
│   • Collect raw responses + logits (when avail.)         │
└──────┬────────────────────────────────────────────────────┘
       │ responses
┌──────▼────────────────────────────────────────────────────┐
│ 3  Guardrail Layer (GL)                                  │
│   • Input-side: MoJE, RA-LLM, Prototype-Experts          │
│   • Response-side: Goal-Prioritised Decoding             │
│   • Adaptive Threshold Scheduler (PSO-style)             │
└──────┬────────────────────────────────────────────────────┘
       │ verdicts + metrics
┌──────▼────────────────────────────────────────────────────┐
│ 4  Evaluator & Profiler (EP)                             │
│   • ASR, Precision/Recall, Latency (RLI-style sampling)  │
│   • Cost modelling (FLOPs, $/1 k tokens)                 │
│   • Investigator-bias correction (SDT)                   │
└───────────────────────────────────────────────────────────┘
```

### 5.2 Key Engineering Choices  
* **Latency sampling** – embed RLI-like extrapolation in GL to log per-prompt overhead without high-resolution timers.  
* **Dynamic safety level** – replicate adaptive RSS handover: PSO tunes MoJE threshold based on real-time ASR drift.  
* **Cross-modal extensibility** – TBD fusion shows KLA can combine vision & text detectors; architect GL to accept pluggable experts.  

### 5.3 Resource Prediction & Scheduling  
* Markov-chain mobility prediction analogy: pre-compute “risk trajectory” of session; raise guardrail strength when prompt-flow exceeds 3.4 Mb (finding from adaptive security-level selection study).  
* Workload auto-tuning (LANCET) principles – sample a subset of prompts to measure 99th-percentile guardrail latency w/ ≤10 µs precision.  

---
## 6. Open Research Directions  
1. **Universal + Explainable Guardrail** – fuse MoJE stats with small PCFG-based syntactic detectors to surface *why* a prompt is flagged.  
2. **Temporal Robustness** – integrate continuous scraping (Li et al.) + genetic evolution (Open Sesame!) to emulate attacker adaptation; evaluate guardrail half-life.  
3. **Cross-Language & Code-Switching** – extend MoJE features w/ sub-token segmenter from Dutch–Limburgish study; validate on JSpeech for spoken prompts.  
4. **Multi-Objective Optimisation** – trade-off safety vs. helpfulness vs. latency via weighted Kullback–Leibler Average similar to TBD vision fusion.  
5. **Bias & Validity Audits** – apply fit–validity–fairness principles (PSA audit) to jailbreak detectors; mitigate investigator bias through blinded evaluation.  
6. **Edge & On-Device** – port MoJE to WASM for mobile; pair with low-power ANN scheduler from adaptive security-level selection to save battery when traffic <3 Mb.  

---
## 7. Ethical & Policy Considerations  
* **Threat Model Clarity** – distinguish researcher red-team vs. malicious public use; enforce dual-use review.  
* **Dataset Licensing** – leverage GitHub Licence Analysis to ensure redistribution legality; prefer CC-0/GPL-compatible text.  
* **Transparency vs. Security** – publish guardrail *architecture* (MoJE) but not evolved adversarial suffixes (Open Sesame!) to avoid proliferation.  
* **Evaluation Fairness** – borrow Signal-Detection-Theory mapping to avoid over-penalising benign creative prompts.  

---
## 8. Conclusions & Recommendations  
1. **Adopt ReNeLLM + Open Sesame** for internal stress-testing; they collectively cover white-box, black-box and transfer attacks.  
2. **Deploy MoJE front-end + Goal-Prioritised decoding** as default safety stack; expect ASR <10 % with <1 ms overhead per prompt.  
3. **Launch JailbreakBench-XL** under CC-BY-SA-4.0 to fill dataset gap; reuse licensing pipeline of CrossCodeBench.  
4. **Continuously tune thresholds** via PSO-style optimiser driven by live ASR statistics, mirroring telecom dynamic handover.  
5. **Audit guardrails** against multilingual & voice prompts; integrate sub-token code-switching detector.  
6. **Publish latency & cost metrics** using RLI-like sampling to foster reproducibility.  

By integrating lightweight statistical guardrails with adaptive scheduling and comprehensive benchmarking, practitioners can dramatically shrink the attack surface of both closed and open LLMs while keeping cost and latency within production budgets.


## Sources

- http://hdl.handle.net/11386/4652991
- http://purl.utwente.nl/publications/102942
- https://figshare.com/articles/Code_for_the_Common_Redstart_case_study/5849868
- http://arxiv.org/abs/2108.13161
- http://www.ist-intermon.org/overview/ips_2004/ips2004_030.pdf
- https://zenodo.org/record/5228822
- https://digitalcommons.carleton.edu/comps/3620
- http://caia.swin.edu.au/reports/
- http://digital.library.unt.edu/ark:/67531/metadc407740/
- http://journals.itb.ac.id/index.php/jictra/article/download/846/523/
- http://eprints.usq.edu.au/46108/
- https://zenodo.org/record/8283005
- http://hdl.handle.net/10018/1240172
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-2950
- http://hdl.handle.net/10138/564129
- http://arxiv.org/abs/2308.09662
- https://www.e3s-conferences.org/10.1051/e3sconf/202343001182/pdf
- http://hdl.handle.net/11582/322998
- http://arxiv.org/abs/2205.11166
- http://infoscience.epfl.ch/record/268172
- http://hdl.handle.net/10.6084/m9.figshare.24792507.v1
- https://eprints.whiterose.ac.uk/170423/1/Manuscript_Final.pdf
- http://arxiv.org/abs/2309.14976
- https://figshare.com/articles/_Performances_of_different_text_detection_methods_evaluated_on_texts_of_different_languages_/764753
- http://hdl.handle.net/11567/1083642
- http://hdl.handle.net/10.1371/journal.pone.0291750.t007
- http://cran.at.r-project.org/web/packages/Causata/Causata.pdf
- https://zenodo.org/record/6577817
- https://zenodo.org/record/4682056
- https://hal.inria.fr/hal-02331295
- https://hal.inria.fr/inria-00413347/document/
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA486996%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://resolver.tudelft.nl/uuid:6fca25b4-2105-433f-a9a1-365116d99214
- http://hdl.handle.net/10045/117457
- https://figshare.com/articles/The_dataset_of_six_open_source_Java_projects/951967
- http://urn.kb.se/resolve?urn=urn:nbn:se:kau:diva-76707
- http://dx.doi.org/10.15480/882.2422
- http://hdl.handle.net/2066/44538
- https://cris.maastrichtuniversity.nl/ws/files/6271690/a5573.pdf
- https://zenodo.org/record/2556151
- https://access.redhat.com/documentation/en-US/JBoss_Enterprise_Application_Platform/4.3/pdf/Server_Configuration_Guide/JBoss_Enterprise_Application_Platform-4.3-Server_Configuration_Guide-en-US.pdf
- https://figshare.com/articles/Overview_of_the_proposed_methodology_for_evaluating_signal_detection_methods_/6654104
- http://eprints.utm.my/id/eprint/102671/1/ArfahAhmadHasbollahPSKE2020.pdf.pdf
- https://zenodo.org/record/8226079
- https://ojs.aaai.org/index.php/AAAI/article/view/26599
- https://bibliotekanauki.pl/articles/226002
- https://zenodo.org/record/7847805
- https://hdl.handle.net/11250/3022462
- https://zenodo.org/record/3608212
- http://hdl.handle.net/2066/135159
- https://norma.ncirl.ie/4301/
- http://ijret.org/Volumes/V02/I14/IJRET_110214018.pdf
- http://cds.cern.ch/record/1443929
- http://purl.utwente.nl/publications/100292
- https://eprints.lancs.ac.uk/id/eprint/179211/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.109
- http://arxiv.org/abs/2309.14348
- https://al-kindipublisher.com/index.php/jcsts/article/view/6568
- http://ubicc.org/files/pdf/ubic232volume3_232.pdf
- http://www.ling.gu.se/~rj/statmetRJ.pdf
- https://zenodo.org/record/6338011
- http://hdl.handle.net/11591/445420
- http://hdl.handle.net/10945/49347
- https://figshare.com/articles/Distribution_of_minimization_criteria_in_trial_participants_included_in_the_primary_endpoint_analysis_by_trial_arm_supported_telemonitoring_compared_to_usual_care_/3887754
- https://zenodo.org/record/8096871
- https://ojs.aaai.org/index.php/AIES/article/view/31664
- http://datacite.org/schema/kernel-4
- https://figshare.com/articles/ICPE_2018_Artifact_-_Measuring_Network_Latency_Variation_Impacts_to_High_Performance_Computing_Application_Performance/6894338
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-8566
- https://figshare.com/articles/MOESM7_of_Can_human_experts_predict_solubility_better_than_computers_/5701318
- https://hal.inria.fr/hal-03540072
- https://eprint.iacr.org/2023/1561
- https://kar.kent.ac.uk/109494/1/EICC2025-AAM.pdf
- http://hdl.handle.net/2078.1/187334
- http://hdl.handle.net/2066/166336
- https://doaj.org/article/1bb439cd1f5946b69889f0012a45fd52
- http://arxiv.org/abs/2205.10625
- https://doaj.org/article/486dd7830ede472cb25d71dc62747b40
- http://hdl.handle.net/10871/126487
- http://berlin.csie.ntnu.edu.tw/Courses/2004F-SpeechRecognition/Slides/SP2004F_Lecture06_Language%20Modeling.pdf
- http://hdl.handle.net/2066/133918
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:92434
- https://zenodo.org/record/7321934
- https://nrl.northumbria.ac.uk/id/eprint/49657/1/FINAL%20VERSION_TII.pdf
- https://surrey.eprints-hosting.org/850355/1/JSPEECH.pdf
- http://wrap.warwick.ac.uk/171107/1/WRAP-Attention-based-adversarial-robust-distillation-radio-classifications-low-power-IoT-22.pdf
- https://zenodo.org/record/7597922
- https://digitalcommons.wpi.edu/mqp-all/7305
- http://eprints.nottingham.ac.uk/36358/
- http://hdl.handle.net/10.1371/journal.pone.0285333.g002
- https://calhoun.nps.edu/bitstream/handle/10945/36732/defending_critical_infrastructure.pdf%3Bjsessionid%3D709FF8E5F07BF8B0C85FA1B50A1DE683?sequence%3D3
- http://arxiv.org/abs/2311.09096
- http://hdl.handle.net/10.6084/m9.figshare.22153901.v1
- http://real.mtak.hu/172978/
- https://research.vu.nl/en/publications/0815706a-a0e7-4edb-9300-84d2bd772154
- https://figshare.com/articles/_Scaling_outcomes_for_loading_rate_/169410
- https://access.redhat.com/documentation/en-US/JBoss_Enterprise_Application_Platform/6.1/pdf/Security_Guide/JBoss_Enterprise_Application_Platform-6.1-Security_Guide-en-US.pdf
- https://orbilu.uni.lu/handle/10993/18548
- http://arxiv.org/abs/2308.03825
- https://zenodo.org/record/8285326
- http://creativecommons.org/licenses/by-nc-nd/4.0
- https://figshare.com/articles/Data_set_of_Android_permissions/5986708
- https://docs.lib.purdue.edu/dissertations/AAI3544236
- http://hdl.handle.net/10.1371/journal.pone.0203794.t008
- www.myjurnal.my/filebank/published_article/63546JTEC_5.pdf
- http://arxiv.org/abs/2308.12833
- https://doaj.org/article/f01ef51f289a461fbda6d1da92d6df28
- https://doaj.org/article/c7169fb08cb5480baa8cc6e5f352a854
- http://dssm.unipa.it/CRAN/web/packages/rrcovNA/rrcovNA.pdf
- https://publisher.uthm.edu.my/ojs/index.php/ijie/article/view/9061
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1875389214002454/MAIN/application/pdf/718ce459f5c8faaae16ef20433647734/main.pdf
- https://trepo.tuni.fi//handle/123456789/22276
- https://zenodo.org/record/6556525
- http://paper.ijcsns.org/07_book/200807/20080730.pdf
- https://figshare.com/articles/Performance_Comparison_of_PSOGO_Senti_and_the_GSM_GA_based_Approaches_1_/2671246
- http://hdl.handle.net/10453/127498
- https://zenodo.org/record/3663390
- http://www.bth.se/fou/forskinfo.nsf/6753b78eb2944e0ac1256608004f0535/28b9a40a6111b0d5c12572f7002aaf3b?OpenDocument
- http://publica.fraunhofer.de/documents/N-543590.html
- http://ijrcct.org/index.php/ojs/article/view/425/pdf/
- https://figshare.com/articles/Zebra_finch_analyses/4097727
- https://rgu-repository.worktribe.com/file/2072071/1/SENANAYAKE%202023%20Labelled%20vulnerability%20%28LINK%20ONLY%29
- http://arxiv.org/abs/2311.08268
- http://hdl.handle.net/11582/3938
- https://doaj.org/article/2ed7b2c7ad0c4f03930eeda1b8b066b2
- https://zenodo.org/record/4180893
- http://hdl.handle.net/10138/337001
- http://hdl.handle.net/10.1371/journal.pone.0203794.t009
- https://scholarship.law.vanderbilt.edu/faculty-publications/887
- http://dx.doi.org/10.1109/COMST.2020.2988293
- https://zenodo.org/record/7227476
- https://doaj.org/article/3a98719f5ea94ed8af495b5f1f8610df
- http://www.hoajonline.com/journals/pdf/2050-1323-3-1.pdf
- https://zenodo.org/record/8014643
- https://doaj.org/article/dcb8f54cbc304eb3aff0b6c1c8c44618
- https://surrey.eprints-hosting.org/807434/17/Mobility%20Prediction%20for%20Handover%20Management%20in%20Cellular%20Networks%20with%20Control%20Data%20Separation_Camera_Ready.pdf
- https://cris.maastrichtuniversity.nl/en/publications/97284781-58c1-47f3-ba68-3ddbd1e7f871
- https://doaj.org/article/d39673f5c7d4411183d13ace9ae6e9d4
- https://zenodo.org/record/6347648
- https://ojs.aaai.org/index.php/AIES/article/view/31638
- http://urn.kb.se/resolve?urn=urn:nbn:se:hj:diva-17960
- http://hdl.handle.net/10.6084/m9.figshare.24607614.v1
- http://ccc.inaoep.mx/%7Evillasen/index_archivos/cursoTATII/ClasificacionIntervenciones/Balakrishna-StatistiscalLM+for+VoiceSystems.pdf?origin%3Dpublication_detail
- http://dx.doi.org/10.1109/ICC.2015.7248939
- https://figshare.com/articles/MOESM1_of_Real-time_topic-aware_influence_maximization_using_preprocessing/4675171
- https://figshare.com/articles/Distribution_of_accuracy_for_binary_and_multi-class_classifier_in_generalisation_evaluation_/3871596
- http://hdl.handle.net/10.5281/zenodo.2547512
- https://archive-ouverte.unige.ch/unige:3475
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050916000995/MAIN/application/pdf/024dc6d88c78f05b4cc3804843e29ff1/main.pdf
- http://www.scopus.com/inward/record.url?scp=85053628175&partnerID=8YFLogxK
- http://collaboration.csc.ncsu.edu/laurie/Papers/p31-gegick.pdf
- https://zenodo.org/record/1343499
- https://escholarship.org/uc/item/8551n5mz
- https://orbilu.uni.lu/handle/10993/57833
- http://hdl.handle.net/11386/4776145
- https://zenodo.org/record/8095785
- https://www.ijitr.com/index.php/ojs/article/view/2372
- http://hdl.handle.net/2134/20310984.v1
- https://hal.science/hal-03703712/document
- https://zenodo.org/record/7688700
- http://jurnal.unprimdn.ac.id/index.php/JUTIKOMP/article/view/4281
- http://arxiv.org/abs/2206.02982
- https://zenodo.org/record/4554591
- http://hdl.handle.net/10453/136339
- https://zenodo.org/record/3648686
- http://hdl.handle.net/10.1371/journal.pone.0285333.t004
- http://www.nusl.cz/ntk/nusl-503239
- http://hdl.handle.net/10.1371/journal.pone.0208450.g001
- https://hal.science/hal-01705734/document
- https://zenodo.org/record/21500
- https://figshare.com/articles/Comparison_of_detection_rate_using_3_Methods_on_KITTI_and_DETRAC_datasets_/5956984
- http://arxiv.org/abs/2309.01446
- https://researchbank.rmit.edu.au/view/rmit:54038
- https://hal.science/hal-01812121
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.6691
- https://zenodo.org/record/7054326
- https://doaj.org/article/617f8ed7e46e4bc29c92a62eae9ad6b9
- http://hdl.handle.net/10.1371/journal.pone.0291750.t006
- https://figshare.com/articles/_Latency_to_reach_the_wood_shavings_area_for_tests_for_which_birds_were_successful_across_eight_tests_with_increasing_water_runway_length_and_depth_for_the_three_food_treatments_for_a_means_177_SE_estimated_from_LMM_on_log_scale_and_b_back_transformed_to_/1120034
- http://arxiv.org/abs/2308.11521
- https://eprints.ugd.edu.mk/16527/
- http://digitalcommons.utep.edu/cgi/viewcontent.cgi?article%3D1008%26context%3Dchristian_meissner
- http://acl.ldc.upenn.edu/acl2002/DEMOS/pdfs/DEMO011.pdf
- https://zenodo.org/record/3469193
- https://zenodo.org/record/4896447
- https://figshare.com/articles/The_random_variables_extracted_from_natural_language_sentences_elicited_from_experts_/4236632
- https://hal.science/hal-03277333/document
- https://lirias.kuleuven.be/handle/123456789/288444
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066106000296/MAIN/application/pdf/2dba4c4452a2c56854acb3472f4b392d/main.pdf
- https://figshare.com/articles/The_accuracy_and_running_time_of_different_generations_in_GA_/4242575
- https://zenodo.org/record/4617258
- https://nrc-publications.canada.ca/eng/view/accepted/?id=8a1144bd-69c8-49fe-9ae2-8ef86f388615
- http://hdl.handle.net/11584/47370
- https://zenodo.org/record/7056331
- https://hal.archives-ouvertes.fr/hal-01112905
- http://arxiv.org/abs/2202.02851
- http://elektro.studentjournal.ub.ac.id/index.php/teub/article/view/1303
- https://zenodo.org/record/5139187
- http://hdl.handle.net/2066/146300
- https://figshare.com/articles/_Running_time_comparison_for_our_algorithm_LTE_with_other_state_of_the_art_local_community_detection_algorithms_/413229
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Evaluating-Algorithmic-Risk-Assessment/99587022902346
- http://hdl.handle.net/1822/52754
- http://hdl.handle.net/10.1371/journal.pone.0212342.t001
- http://hdl.handle.net/2099.1/21093
- https://zenodo.org/record/7893288
- http://nickduffield.net/download/papers/ToN_RLI.pdf
- https://journal.austms.org.au/ojs/index.php/ANZIAMJ/article/view/2440
- https://aaltodoc.aalto.fi/handle/123456789/40155
- https://hdl.handle.net/11250/3048652
- https://www.ijitr.com/index.php/ojs/article/view/2462
- http://hdl.handle.net/1854/LU-8560423
- https://www.repository.cam.ac.uk/handle/1810/274144
- https://napier-repository.worktribe.com/file/2894905/1/Ensemble%20learning-based%20IDS%20for%20sensors%20telemetry%20data%20in%20IoT%20networks
- https://figshare.com/articles/_Relative_distribution_of_POS_in_the_IceMorph_dictionary_GOLD_and_EXPERT_/1107674
- https://doaj.org/toc/1690-4524
- http://hdl.handle.net/2066/43224
- http://hdl.handle.net/2117/14288
- https://pub.uni-bielefeld.de/record/2969258