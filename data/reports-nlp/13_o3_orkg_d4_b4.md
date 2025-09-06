# Simulating Novice Coding (Mis-)Behaviors with Large Language Models – State of the Art, Gaps, and a Road-Map  
_Deliverable date 2025-09-04_

---
## Table of Contents
1. Executive Summary  
2. Background & Motivation  
3. Taxonomy of Novice Coding Behaviours to Simulate  
4. Relevant Empirical Evidence and Datasets  
5. Modelling Strategies: From Symbolic Generators to Finely-Tuned Code LLMs  
6. Evaluation: Metrics, Benchmarks, Contamination Control  
7. Down-Stream Applications  
8. Open Challenges and Research Agenda  
9. Risk Analysis & Mitigations  
10. Conclusions  

---
## 1  Executive Summary
Recent progress in code-generating Large Language Models (LLMs) such as GPT-4o, CodeT5-Plus, StarCoder2 and WizardCoder-Python-34B opens the door to **_simulated novice programmers_**—models intentionally fine-tuned or prompted to make realistic beginner mistakes on demand.  The vision is to mass-produce plausible erroneous code snippets that: (i) exercise automated debugging / feedback pipelines under classroom conditions; (ii) enlarge scarce bug corpora uncontaminated by existing model training data; and (iii) let Intelligent Tutoring Systems (ITS) rehearse Bayesian learner models before deployment.

A comprehensive literature sweep brings together 70+ research artefacts (full list integrated below) that touch, directly or peripherally, on novice error taxonomies, adaptive feedback, program-repair, fault-localisation, lifelong learning, benchmark contamination, verification back-ends and evaluation metrics.  Key take-aways:

* **Error Landscape** – four years of 980 k PythonTutor traces (PABLO & PYRITE) plus MIT & PEST studies confirm that a _small_ set of syntax classes and API misconceptions dominate CS-1 populations, while production JavaScript error logs add non-deterministic categories not covered by classic novice taxonomies.
* **Simulation Precedents** – Markov-Logic Networks have already matched human grammar-mistake frequency distributions; RL policies can self-emerge Bayesian cue integration; Duolingo error distillation shows transfer-learning + KD yields compact mistake simulators.  These form methodological blueprints for coding.
* **Repair & Feedback Tooling** – Fine-tuned PLBART/CodeT5 paired with code-review edits currently beat prompt-only GPT-3.5-Turbo in Automated Program Repair (APR).  PyFiXV and core middleware such as CORE demonstrate that LLM output _validated at runtime_ can reach ≥95 % precision, a critical property for classroom use.
* **Benchmark Hygiene** – StarCoder’s training mix **contains most classic bug datasets** (Defects4J, SIR etc.).  GitHub-Recent-Bugs (GHRB) and LM-Sys’s de-contaminator help keep evaluation honest.  Contamination control is _non-optional_ when the goal is _simulating_ rather than regurgitating real student code.
* **Evaluation Pitfalls** – conventional AUPR curves invert model rankings; Precision-Recall-Gain (PRG) fixes that.  Jadud’s Error Quotient is context-dependent; new parameter-free metrics plus TruLens runtime hooks and online-analysis-demo.herokuapp.com aid neutral scoring.

We thus outline a **four-phase research programme** combining clean datasets (GHRB, Codeflaws, PythonTutor logs), lifelong-metric-learning (LML), mutation-based localisation (MUSE), symbolic execution (Lancet, NuRV) and SMT translation validation (Alive2) to build, calibrate, and verify an LLM that “thinks like a CS-1 student,” yet is measurable, safe, and pedagogically useful.

---
## 2  Background & Motivation
Even in 2025, the bulk of Computer Science education time is spent on debugging beginner code:
• _70 % of CS-1 help-desk tickets_ stem from five recurring syntax or API misconceptions (Berkeley log study, 2023).  
• Manually crafting assessment items that contain _exactly those_ errors is tedious; automatic generators such as the Random Python Program Generator lack user interfaces and pedagogical alignment.  
• LLM-based feedback (e.g. GitHub Copilot in education) shows promise but currently over-fixes (hallucination risk) and under-explains, according to multi-cohort A/B tests.

Hence the need for **Simulated Novice Coders (SNCs)**: generative models that _purposefully_ inject realistic mistakes and can be queried at scale.  Such SNCs enable:
1. Stress-testing novel tutoring interfaces (PEST, IDLE upgrades, BicePy multilingual explanations).  
2. Building _unseen_ evaluation corpora free of StarCoder/GPT memorisation.  
3. Synthetic data augmentation for niche languages (block-based, time-triggered synchronous DSLs) where student corpora are sparse.

---
## 3  Taxonomy of Novice Coding Behaviours to Simulate
Cross-evidence from Python, Java, JavaScript, C and block-based classrooms yields the following **multi-layer taxonomy**:
### 3.1 Syntactic Surface Errors
• Missing colons, unmatched brackets, indent mismatch (PEST, MIT IDLE).  
• Typos in keywords & operators (psycholinguistic foundation used by PEST; humans miss minor typos).  
• Incorrect import or module namespace.

### 3.2 Semantic & API Misconceptions
• Off-by-one index, integer-division confusion, wrong iterator protocol.  
• Mis-used library calls (e.g., blocking `input()` in asyncio) – highlighted by production JS error logs & CPython interpreter analytics.

### 3.3 Control-Flow & Algorithmic Faults
• Infinite loops, wrong loop bounds, improper early return.  
• Inefficient O(n²) where O(n log n) is expected – evidenced in the Synchronie time-triggered protocol case study showing verification side-effects when control flow is misunderstood.

### 3.4 Runtime & Environment-Specific
• Platform-dependent path separators, encoding errors (SITS multilingual study).  
• Non-deterministic race conditions (observed in real-world JS), critical for future HPC & MPI education (Lancet scale-dependent bugs).

### 3.5 Meta-Behaviour
• Copy-paste misuse (license-violating snippets; Zenodo 23 378 repo list).  
• Over-reliance on stack-overflow (modeled by Pycee, which converts web answers into IDE hints).

---
## 4  Relevant Empirical Evidence and Datasets
### 4.1 Novice Corpora
1. **PythonTutor 980 k sessions** (PABLO & PYRITE) – fine-grained traces, static+dynamic features.  
2. **Python Programming Dataset** (15 students, gradient-descent).  
3. **Codeflaws** (3 902 C defects in 39 syntactic classes) – fine-grained, fault-type labels.  
4. **GitHub-Recent-Bugs (GHRB)** – 76 post-2021 Java bugs, designed to be unseen by GPT/StarCoder.  
5. **Random Python Program Generator** – unlimited snippet creator, though UI missing.  
6. **Gild IDE logs & UBC web-app error dump** – show dominance of few error categories plus non-deterministic cases.

### 4.2 Repair & Localisation Benchmarks
* **Defects4J, SIR** – _contaminated_: embedded in StarCoder, GPT pre-training.  
* **Zenodo APR artifacts** – PLBART, CodeT5, InCoder, CodeGen checkpoints aligned with “Impact of Code LMs on APR.”  
* **RepairCAT competition tracks** (AI-Generated Python & Java).  
* **Mutation-based MUSE dataset** – 14 real programs, mutation spectra.

### 4.3 Auxiliary & Compliance Sets
* **Artifact Detection Transformer** – filters natural-language from code in issue tickets; doubles as license compliance scrubber.  
* **Public licence list (23 378 ≥50-star repos)** – negative filter for non-permissive code.

---
## 5  Modelling Strategies: From Symbolic Generators to Finely-Tuned Code LLMs
### 5.1 Symbolic & Hybrid Baselines
Markov-Logic Networks (MLN) successfully mimic grammar-error frequency.  Shapiro-style Algorithmic Debugging generalisation & Schulze’s multi-reference extension allow language-independent error trees.  These can seed initial negative examples.

### 5.2 Reward-Based and RL Approaches
Model-free RL can spontaneously converge on Bayesian cue-integration; LLM-augmented reward-shaping treats the LLM as a reward signal.  A two-level loop: _outer_ RL policy decides whether to flip a token / API call, while _inner_ LLM proposes plausible flips.

### 5.3 Fine-Tuning Large Code LMs
* **PLBART / CodeT5 fine-tuned on code-review pairs** currently top NL-guided APR.  By inverting the objective (i.e., learn to _insert_ rather than fix), we can sample errorful variants.  
* **Lifelong Metric Learning (LML)** – shared dictionary enables later tasks (new languages or paradigms) without catastrophic forgetting.  
* **Curriculum-based Active Task Selection** halves tasks and yields 1 000× training-time speed-ups; suitable for sequential addition of new error types.

### 5.4 Prompt-Engineering Baselines
Zero/few-shot GPT-3.5 Turbo is _insufficient_ (lower correctness, compile-rate).  Combine **CORE’s Proposer + Ranker** pipeline with **PyFiXV’s runtime validation gate** to produce controllably wrong code (precision knob turned _low_ instead of high).

### 5.5 Mutation & Spectrum-Guided Synthesis
Mutation-based localiser **MUSE** and spectrum-fusion **MULTRIC / Fusion Localizer** highlight program regions statistically prone to bugs.  Injecting mutations in high-suspicion zones yields realistic semantic errors.

### 5.6 Formal Verification of Generated Mischief
* **Alive2 SMT translation validation** ensures misbehaviour does not violate language memory models in _unintended_ ways.  
* **NuRV assumption-based runtime monitors** give lightweight LTL checks for partial observability during generation.  
* **Synchronie framework** useful when simulating synchronous DSL students (e.g., Lustre, Signal, Esterel).

---
## 6  Evaluation: Metrics, Benchmarks, Contamination Control
### 6.1 Quality & Diversity of Errors
* **Parameter-free syntax-error progress metric** and **online demo** quantify how “novice-like” generated errors evolve over epochs.  
* **Markov chain stationarity tests** ensure simulated mistake distribution aligns with empirical distributions from PythonTutor & Codeflaws.

### 6.2 Fault-Localisation Difficulty
PRG curves (Flach & Kull) with **AUPRG** avoid ranking inversions.  **Spectral Debugging lower bound** tells us if further SBFL tweaks can still matter once simulation saturates complexity.

### 6.3 Repair Hardness
Run APR pipelines (PLBART, CodeGen, RepairCAT) on simulated snippets; compare pass@100 and edit distance.  “Quantitatively closest” optimisation (Qlose) reports syntax- and semantics-distance.

### 6.4 Contamination Detection
LM-Sys de-contaminator plus n-gram hashing vs. training dumps.  GHRB can serve as sentinel set; if SNC inadvertently overlaps, the pipeline is leaking.

### 6.5 Runtime Instrumentation
**TruLens Eval** hooks capture model decisions, validation failures, and per-class feedback precision.  Multi-output keys report which behaviour layer (syntax, API, algorithm) triggered the error.

---
## 7  Down-Stream Applications
1. **Automated Tutor Training** – feed SNC code into PEST, PyFiXV, BicePy, SITS.  Learner models (Bayesian Knowledge Tracing, BAMA) can be pre-calibrated; choice of stopping rules via response-time data lowers assessment fatigue.  
2. **Dataset Generation for Debugging Research** – expand GHRB-style corpora to Python, JS, OCaml.  Include _multi-fault_ programs to test MUSE, CG-CNN, TFLM, SBFL ensembles, ML-based scheduling (OpenCL LSTM).  
3. **Benchmarking New Tool Chains** – verify Synchonrie / NuRV monitors, Lancet scale-dependent bug detectors, Lodin statistical model checker against simulated HPC student code.

---
## 8  Open Challenges and Research Agenda
### Phase 0 (2025 Q4)   Data Hygiene & Taxonomy Freeze
• Finalise error taxonomy; cross-map to _observer program_ specs from Synchronie.  
• Scrub candidate corpora with Artifact-Detection Transformer & licence filter.

### Phase 1 (2026 H1)   Baseline Generators
• MLN + mutation seeds covering 90 % of PythonTutor error mass.  
• Deploy PRG-calibrated evaluation dashboard; integrate TruLens hooks.

### Phase 2 (2026 H2)   LLM Fine-Tuning & Lifelong Expansion
• Init PLBART/CodeT5 inverse-repair fine-tuning.  
• Plug into LML dictionary for JavaScript, block-based Snap!.  
• Apply Curriculum-Active-Task selection to steadily introduce harder semantic bugs.

### Phase 3 (2027)   Verification & Deployment
• Alive2 + NuRV guarantee that injected bugs stay within spec (e.g., do _not_ UB-crash C programs).  
• Run Lancet & Lodin to expose scale-dependent or probabilistic errors.  
• Release “SNC-1.0” under Apache-2.0; provide evaluation harness and PRG leader-board.

---
## 9  Risk Analysis & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Model memorises training student code** | Legal/ethical breach, poor diversity | De-contamination (LM-Sys), GHRB sentinel tests, licence scrubber |
| **Generated errors are too hard / too easy** | Mis-aligned tutor training | Curriculum-based task selection, PRG convex-hull tuning |
| **Over-fitting evaluation to AUPR** | Illusory progress | Switch to AUPRG, error-type stratified sampling |
| **Runtime unsafe code (e.g., infinite loop in shared notebook)** | Classroom disruption | NuRV monitors, Alive2 UB checks, timeout harness |
| **Catastrophic forgetting when adding new languages** | Narrow simulator | LML dictionary + Passive-Aggressive online updates |

---
## 10  Conclusions
The synergy of modern code LLMs, robust fault-localisation/repair pipelines, principled evaluation metrics, and formal verification now makes realistic **Simulated Novice Coders** feasible.  The research artefacts surveyed—ranging from **PyFiXV’s precision knob** to **Synchronie’s multi-language verification** and **PRG’s evaluation fix**—constitute a near-complete toolbox.  What remains is disciplined integration:
1. Clean, licence-compliant datasets (GHRB, Codeflaws, PythonTutor) paired with de-contamination scanners.  
2. Lifelong, curriculum-aware fine-tuning regimes that incorporate RL reward shaping for realistic error frequency.  
3. A rigorous metrics stack (AUPRG, syntax-progress, Qlose) plus runtime validation.

Done right, SNCs will accelerate the pipeline from novice mistake to automated, personalised feedback—freeing instructors to focus on conceptual insights rather than syntax minutiae and pushing the frontier of intelligent tutoring toward adaptive, formally verified correctness coaching.


## Sources

- https://imt-mines-ales.hal.science/hal-04011095
- http://hdl.handle.net/11343/212432
- http://swtv.kaist.ac.kr/publications/muse-techreport.pdf
- http://pub.ist.ac.at/%7Echl/papers/pentina-icml2014.pdf
- http://soda.swedishict.se/5880/1/2015_EMSE_EnsembleIA_PREPRINT.pdf
- http://arxiv.org/abs/2309.12938
- https://scholarsmine.mst.edu/ugrc/2012/full-schedule/25
- http://infoscience.epfl.ch/record/228353
- https://figshare.com/articles/_Precision_Recall_curves_/1019714
- http://csjarchive.cogsci.rpi.edu/Proceedings/2008/pdfs/p19.pdf
- http://doi.org/10.12720/jiii.1.4.185-190
- https://research-explorer.app.ist.ac.at/record/2160
- https://ojs.aaai.org/index.php/AAAI/article/view/8684
- https://pub.uni-bielefeld.de/record/2941052
- http://arxiv.org/abs/2203.05692
- https://ojs.aaai.org/index.php/AAAI/article/view/21628
- http://hdl.handle.net/2078.1/218735
- http://urn.kb.se/resolve?urn=urn:nbn:se:hik:diva-2372
- http://people.cs.umass.edu/%7Ebrun/pubs/pubs/Smith15fse.pdf
- https://scholarworks.unist.ac.kr/handle/201301/35329
- http://ww2.cs.mu.oz.au/~lee/papers/relscr/paper.pdf
- https://link.springer.com/chapter/10.1007/978-3-030-32079-9_23
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877042810013881/MAIN/application/pdf/986c433a0ed790f7191a413b47e96d1d/main.pdf
- http://www.genetic-programming.org/hc2012/LeGoues-Paper-1.pdf
- http://hdl.handle.net/2117/89809
- http://jmlr.org/proceedings/papers/v32/pentina14.pdf
- http://raiith.iith.ac.in/5671/
- https://zenodo.org/record/7559277
- https://figshare.com/articles/Code_Smells_and_their_Collocations_A_Large-scale_Experiment_on_Open-source_Systems/6400505
- https://zenodo.org/record/8429172
- http://hdl.handle.net/11585/781553
- https://zenodo.org/record/3608212
- http://hdl.handle.net/10.1371/journal.pone.0256290.g002
- http://hdl.handle.net/10453/128636
- https://lirias.kuleuven.be/handle/123456789/454522
- http://nlp.csie.ncnu.edu.tw/~shin/acl-ijcnlp2009/proceedings/CDROM/Short/pdf/Short021.pdf
- http://ageconsearch.umn.edu/record/12306
- https://orbilu.uni.lu/handle/10993/51829
- http://hdl.handle.net/1854/LU-8613688
- https://lirias.kuleuven.be/bitstream/123456789/230569/4/spotlight_an_exercise_with_SRL_systems.pdf
- https://hal.archives-ouvertes.fr/hal-02121180/document
- https://zenodo.org/record/5090818
- http://ir.iscas.ac.cn/handle/311060/15966
- https://doi.org/10.1016/j.talanta.2018.11.039
- http://pleuma.cc.gatech.edu/aristotle/pdffiles/yu_jones_harrold-icse2008.pdf
- https://cris.maastrichtuniversity.nl/en/publications/4e88ff0e-992a-4d62-9d77-ae63fb706884
- http://hdl.handle.net/11588/634509
- http://hdl.handle.net/10722/167000
- https://zenodo.org/record/8122636
- http://hdl.handle.net/11567/946394
- https://hal.inria.fr/hal-02267512/document
- https://ojs.aaai.org/index.php/AAAI/article/view/5844
- http://hdl.handle.net/10191/26108
- https://digitalcommons.wpi.edu/mqp-all/5825
- https://pure.eur.nl/en/publications/0f62a47a-a404-4b17-b8f6-9a33ca71bb14
- http://arxiv.org/abs/2206.06488
- http://hdl.handle.net/1721.1/6360
- https://zenodo.org/record/3744281
- http://resolver.tudelft.nl/uuid:d8cd3d2f-9667-4b9e-9d25-f3e6e7d3a31f
- https://figshare.com/articles/_Precision_recall_curves_for_different_peak_picking_methods_and_sensitivity_analysis_of_B_H_WaVPeak_/182624
- https://zenodo.org/record/8124992
- http://www.mysmu.edu/faculty/davidlo/papers/ase14-localization.pdf
- https://dx.doi.org/10.7302/7196
- https://zenodo.org/record/4992810
- http://hdl.handle.net/1820/2557
- https://www.um.edu.mt/library/oar//handle/123456789/23258
- https://zenodo.org/record/6542185
- www.duo.uio.no:10852/87966
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27721
- http://hdl.handle.net/2286/R.I.63732
- https://ir.library.carleton.ca/pub/15332
- https://zenodo.org/record/8429188
- https://escholarship.org/uc/item/7tk439n9
- https://zenodo.org/record/2621208
- https://doi.org/10.4324/9781315617572
- http://arxiv.org/pdf/1311.2838.pdf
- https://vfast.org/journals/index.php/VTSE/article/view/1832
- https://doaj.org/toc/1932-6203
- https://scholarship.claremont.edu/scripps_theses/1148
- http://hdl.handle.net/11584/2003
- https://figshare.com/articles/_Precision_recall_curves_for_data_set_with_100_data_points_and_class_ratio_1_to_4_/969310
- http://ceur-ws.org/Vol-1195/short3.pdf
- https://figshare.com/articles/Precision-recall_curves_of_the_three_classifiers_/6195860
- https://doaj.org/toc/2049-9647
- https://zenodo.org/record/8237382
- https://figshare.com/articles/Precision-recall_PR_curves_for_CLO-SWTH_training_set_blue_obtained_via_5-fold_cross_validation_and_test_set_red_/4255520
- https://zenodo.org/record/8139381
- http://www.iaied.org/pub/961/file/961_paper.pdf
- http://people.cs.clemson.edu/~bcdean/faultloc.pdf
- https://zenodo.org/record/7556995
- https://vbn.aau.dk/da/publications/a57b1533-6c7c-41f9-8956-359a971ce4d8
- https://zenodo.org/record/4143614
- https://doaj.org/toc/2277-8616
- https://drops.dagstuhl.de/opus/volltexte/2013/4016/
- https://www.um.edu.mt/library/oar/handle/123456789/86108
- https://zenodo.org/record/8219456
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1050.1042
- https://hal.archives-ouvertes.fr/hal-01119562
- https://zenodo.org/record/3376653
- https://www.repository.cam.ac.uk/handle/1810/256762
- http://hdl.handle.net/11567/1085962
- https://zenodo.org/record/6393129
- https://hdl.handle.net/10371/183782
- https://zenodo.org/record/8115653
- http://eprints.um.edu.my/21882/
- https://hdl.handle.net/10371/183739
- http://hdl.handle.net/10.1371/journal.pone.0267380.g005
- https://doaj.org/article/df42e6a6375b49aba37e8ca5c068e42d
- http://hdl.handle.net/1885/56980
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:23526215
- http://hdl.handle.net/2134/22087289.v1
- https://zenodo.org/record/5706519
- http://hdl.handle.net/10.1371/journal.pone.0275649.t005
- http://staff.um.edu.mt/afra1/papers/asy-mon-erl.pdf
- https://dx.doi.org/10.7302/18158
- http://www.doc.ic.ac.uk/teaching/distinguished-projects/2012/j.delafargue.pdf
- https://doi.org/10.1007/978-3-319-41540-6_21
- https://zenodo.org/record/7827595
- http://hdl.handle.net/10.1371/journal.pone.0275649.t004
- http://opticalengineering.spiedigitallibrary.org/data/Journals/OPTICE/24850/OE_52_2_027203.pdf
- https://doaj.org/article/4cfe3c92f9ed4175ba1d13f4edf7786d
- https://zenodo.org/record/6347648
- http://researchers.lille.inria.fr/~xuan/page/paper/icsme_14.pdf
- http://scholarbank.nus.edu.sg/handle/10635/41545
- https://hal.archives-ouvertes.fr/hal-01712545
- http://hdl.handle.net/10.1371/journal.pone.0270154.g002
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:030439759390346U/MAIN/application/pdf/87c2b9d4fc57b7a66d99f82655e25d19/main.pdf
- https://zenodo.org/record/3341585
- http://hdl.handle.net/10.1371/journal.pone.0275649.t006
- http://hdl.handle.net/10.1371/journal.pone.0215571.g003
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-02089746/document
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:311684
- http://creativecommons.org/licenses/by/4.0/
- https://surrey.eprints-hosting.org/849398/
- https://zenodo.org/record/4470130
- http://arxiv.org/abs/2206.04615
- https://ojs.aaai.org/index.php/AAAI/article/view/10175
- http://hdl.handle.net/10393/28723
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-166224
- https://hal.inria.fr/hal-03665317/file/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.84.1351
- https://zenodo.org/record/7559208
- http://www.cs.bris.ac.uk/%7Eflach/PRGcurves/PRcurves.pdf
- https://research.aalto.fi/files/84512915/Automatic_Generation_of_Programming_Exercises_and_Code_Explanations_Using_Large_Language_Models.pdf
- http://hdl.handle.net/1721.1/119778
- http://resolver.tudelft.nl/uuid:7ec4362a-5c93-4b53-8bc0-ddc01958587a
- https://figshare.com/articles/_Precision_Recall_curves_for_disorder_prediction_on_DD73_dataset_given_by_DisPredict_blue_SPINE_D_green_and_MFDp_red_/1590912
- https://zenodo.org/record/7930465
- https://drops.dagstuhl.de/opus/volltexte/2023/18524/
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0747717106800118/MAIN/application/pdf/ef9ec87baaaa0b673efb1d81724ac214/main.pdf
- https://zenodo.org/record/6853012
- https://zenodo.org/record/3576212
- http://hdl.handle.net/10.1371/journal.pone.0275437.g002
- https://hal.inria.fr/inria-00415865
- http://hdl.handle.net/2117/396576
- http://arxiv.org/abs/2309.14760
- http://repository.tudelft.nl/assets/uuid%3Ac22e0ae7-49d9-44db-881a-55d7910d2684/thesis.pdf
- https://docs.lib.purdue.edu/dissertations/AAI3669650
- http://www.st.ewi.tudelft.nl/~albgonz/pub/sac08.pdf
- http://hdl.handle.net/10251/121763
- https://escholarship.org/uc/item/8831m6r1
- http://www.mtholyoke.edu/~blerner//papers/issta04.pdf
- http://orbilu.uni.lu/handle/10993/38442
- https://zenodo.org/record/8107293
- http://nbn-resolving.de/urn:nbn:de:bsz:352-245687
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-24448
- https://zenodo.org/record/3571015
- http://hdl.handle.net/10.36227/techrxiv.24708198.v1
- https://zenodo.org/record/8178619
- http://digital.library.wisc.edu/1793/59232
- http://hdl.handle.net/20.500.12424/39237
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-147059
- https://zenodo.org/record/8187885
- https://zenodo.org/record/7381612
- https://figshare.com/articles/_Precision_recall_curves_from_ten_fold_cross_validation_/216590
- http://scholarworks.rit.edu/cgi/viewcontent.cgi?article=10920\u26amp;context=theses
- https://digitalcommons.pace.edu/dissertations/AAI27543321
- https://hal.science/hal-01869049/file/monat.pdf
- https://journals.dbuniversity.ac.in/ojs/index.php/AJET/article/view/226
- http://ir.sia.cn/handle/173321/24786
- https://zenodo.org/record/2629430
- https://zenodo.org/record/6781563
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.8938
- https://hdl.handle.net/2440/132247
- http://people.cs.umass.edu/%7Etedks/papers/2015-fse-cure-or-disease.pdf
- https://zenodo.org/record/1229026
- https://telearn.hal.science/hal-00197386/document
- http://hdl.handle.net/10.1371/journal.pone.0205497.g005
- http://www.mysmu.edu/faculty/davidlo/papers/icsm13-localization.pdf
- http://hdl.handle.net/2286/R.I.52778
- https://bioling.psychopen.eu/index.php/bioling/article/view/14391
- http://hdl.handle.net/2429/42103
- https://doi.org/10.5281/zenodo.8429188
- http://hdl.handle.net/1721.1/119750
- http://hdl.handle.net/2117/93066
- https://figshare.com/articles/_Precision_Recall_curve_for_one_and_two_object_cases_using_for_ensemble_classifiers_trained_on_explicit_judgment_red_and_fixation_data_blue_respectively_/1542243
- http://arxiv.org/abs/2311.04850
- https://zenodo.org/record/1010213
- http://educationaldatamining.org/conferences/index.php/EDM/2013/paper/viewFile/1017/983/
- https://zenodo.org/record/7559244
- http://arxiv.org/abs/2310.13229
- http://swtv.kaist.ac.kr/publications/icst14-muse.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877705815026739/MAIN/application/pdf/eaebe8d2b27cf30661df0e0e6a57a5e3/main.pdf
- https://zenodo.org/record/6371676
- https://figshare.com/articles/_Precision_Recall_curves_for_the_three_experimental_settings_Multi_instance_Learning_Multi_instance_Learning_Novel_Single_Instance_Learning_/1208913