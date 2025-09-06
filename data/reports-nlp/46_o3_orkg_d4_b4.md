# Negative Questioning as an Alignment Lever to Reduce Hallucinations in Large Language Models

*Author — 2025-09-05*

---

## 1  Scope and Objectives  
The goal of this report is to provide a **comprehensive, technically detailed synthesis** of how *negative questioning*—i.e.
exposing a model to systematically adversarial, contradictory or otherwise counter-factual prompts—can be used to *align* large-scale neural networks and reduce hallucination rates.  
Because the user did not constrain the scope to theory **or** practice, nor to training **or** inference, we integrate *all* relevant evidence (2021-2024) that touches on negative supervision, hard-negative mining, contradiction learning, hallucination detection/evaluation, and hardware deployment.  
The document is intentionally exhaustive: every single learning item supplied is mapped to at least one section.

---

## 2  Conceptual Grounding: What Is “Negative Questioning”?

1. **Data-level Negatives:** inputs that should *not* be mapped to the positive class/answer (e.g.
false premises, adversarial distractors, conflicting demonstrations).  
2. **Prompt-level Negatives:** queries that intentionally contradict the model’s latent knowledge or memory (e.g.
AutoDebug’s chain-of-conflict prompts).  
3. **Policy-level Negatives:** demonstrations of failure trajectories or sub-optimal actions (IRLF, conflicting MaxEnt-IRL traces).  
4. **Relation-level Negatives:** explicit "A-is-not-related-to-B" signals that drive equivalence-class formation in humans (MTS 2015-2016).  

By *negative questioning* we collectively refer to techniques that **probe or train the model through such negatives** so that it (a) calibrates confidence, (b) suppresses internally generated spurious content, and (c) learns stronger discriminative boundaries.

---

## 3  Theoretical Foundations

### 3.1  Information Gain from Negatives
• `Error-Driven Compensating-Hypothesis loops` and the *Audit & Booster* cascade (CiteseerX 2003; Guo 2005) prove that iteratively re-examining mis‐labelled negatives can shrink the generalisation error from **O(ε)** to **O(ε²)**.  
• `SVM-Based Negative Data Mining` formalises a 1+k scheme that recovers information hidden in highly imbalanced negative sets.  
• `DOC3 (Deep One-Class Classification using Contradictions)` shows—via Empirical Rademacher Complexity bounds—that contradiction samples reduce hypothesis space capacity, directly paralleling alignment goals.

### 3.2  Entropy and Optimal Transport Perspectives
• `Entropy-regularised Optimal Transport` (Sinkhorn divergence) breaks the curse of dimensionality; selecting a large entropic weight acts analogously to injecting *soft* negatives that smooth the transport plan.  
• `Tsallis non-extensive entropy` unifies L2 regularisation and maximum entropy, suggesting that different *q* choices can weight negatives differently.

### 3.3  Behavioural-Cognitive Parallels
Human hallucination studies consistently identify **failure of inhibitory control** over episodic memory (auditory-verbal hallucinations, LSHS scale, rhesus LSD trials).  
Matching-to-Sample experiments (ABA 2015; Plazas & Villamil 2016) show that *explicit negative relations* are required for robust equivalence-class formation—mirroring the need for LLMs to see "X ≠ Y" evidence.

### 3.4  Inverse Reinforcement Learning (IRL) as Alignment Analogy
`IRLF (2022)` demonstrates that *failed* demonstrations accelerate convergence when successful demos ≤25 %.  
Multiple studies (TU-Delft conflicting demos; AAAI-23 misspecification) show that *contradictory* traces degrade classic MaxEnt IRL unless the optimisation explicitly models conflict—an important lesson for negative questioning pipelines: naïvely mixing conflict can hurt unless explicitly reasoned over.

---

## 4  Empirical Evidence that Negatives Reduce Hallucinations

| Cluster | Key Results |
|---------|-------------|
| **Contrastive & CL** | `MixCL (AAAI-23)` matches KB-enhanced baselines on Wizard-of-Wikipedia purely by *mining hard negatives*.  `MixCSE` and `Progressive Hard-Negative Masking` tighten mutual-information bounds, producing better textual similarity and downstream generalisation. |
| **Graph Space** | `CGC (ICDE-23)` synthesises label-flipped yet semantically close negatives to avoid false-negatives, outperforming prior graph representation methods.  `GGD (Monash 23)` shows O(1) BCE loss (no InfoNCE) trains in ≈0.18 s yet improves accuracy—negatives drive speed **and** quality. |
| **Language Pre-training** | `Language Model Pre-training on True Negatives` (AAAI-23/24) fixes false-negative gradients in ELECTRA, raising GLUE/SQuAD while improving robustness—a direct success story for negative-signal correction. |
| **Hallucination Benchmarks** | `HaloCheck`, `HaELM`, `FactCHD`, `Med-HALT` all confirm that hallucination detection is sensitive to **contradictory prompts** and can be measured automatically. |
| **Adversarial Prompting** | `AutoDebug (2310.12516)` crafts contradictory Q-A pairs that transfer across models, sharply amplifying hallucination surface area—validating negative questioning as a stress-test. |
| **Bias & Discrimination** | `Directional Pairwise Class Confusion Bias` widens bias analysis beyond social stereotypes, implying that negative questioning must consider class-level confusion.

---

## 5  Implementation Pathways

### 5.1  Training-Time Pipelines
1. **Negative Demonstration Injection:** Extend RLHF preference datasets with *explicit disagreement pairs*.  Use IRLF’s convex program for reward shaping to handle <25 % successes.  
2. **Contrastive Pre-training:**  
   a. SimCSE → MixCSE → MixCL style objectives.  
   b. Graph tasks: adopt GGD or CGC for O(1) loss and false-negative elimination.  
3. **Gradient Correction:** Integrate the *counter-false-negative* update rule (AAAI-24) into discriminative or dual-network setups (ELECTRA-style).  
4. **Curriculum & Progressive Masking:** Begin with easy negatives, then progressively unmask hardest negatives (Progressive Hard-Negative Masking), analogous to *anti‐catastrophic hallucination curricula*.

### 5.2  Inference-Time Guards
1. **Prompt-Level Negative Questioning:**  
   • Chain contradictory follow-ups à la AutoDebug.  
   • If answers disagree with ground truth or retrieval, downgrade confidence.  
2. **Multi-Agent Voting:** LLteaM style agent pool; predictions blocked when any detector flags hallucination.  Incorporate HaELM as local cheap LLM grader.  
3. **Audit & Booster‐Inspired Cascades:** First pass = primary LLM; second pass = auditor specialising in negatives; booster arbitrates.

### 5.3  Hardware Acceleration for Real-Time Filtering
• `Associative Memory ASICs` (VIPRAM, PRM) deliver 100 MHz pattern matching at ≤10 µs—enough to scan token streams for hallucination signatures on the fly.  
• `FPGA hls4ml` jet-substructure and auto-encoder anomaly circuits show sub-µs latency with minimal LUT usage; a blueprint for *on-device hallucination kernels*.  
• Clock-free spiking-inspired memories offer ultra-low-power alternatives.  

### 5.4  Data Infrastructure
• `GHTorrent on-demand` for up-to-date code bases (inc.
 hallucination-related code analysis).  
• `ClaimsKG`, `OpenGPT-X` pilot and `FactCHD` supply verifiable claims for negative-vs-positive grounding.  
• `figshare FPR curves` support operating-point tuning when negative questioning trades off FP vs FN.

---

## 6  Measurement & Benchmarking

1. **Domain-General:**  
   • `HaloCheck` (black-box, knowledge-free), `HaELM` (LLM-assisted, 95 % ChatGPT agreement).  
2. **Domain-Specific:**  
   • `Med-HALT` (medical reasoning vs memory).  
   • `FactCHD` (conflict types: vanilla, multi-hop, set-operation).  
3. **Cross-Modal:**  
   • HaELM for vision-language hallucination.  
4. **Conflict Sensitivity:**  
   • IRL misspecification tests; measures how far demonstrations can deviate before reward recovery collapses.  
5. **Bias Overlays:**  
   • Directional pairwise class confusion metrics ensure negative questioning does **not** amplify unwanted bias.  
6. **Human Study Analogues:**  
   • False-alarm rates in AVH patients; LSD/DMT discrimination deficits can inspire psychometric-style hallucination probes.

---

## 7  Open Research Directions

A. **Unified Negative-Questioning Framework**  
Combine data-level, prompt-level and policy-level negatives in a *multi-objective* loss blending Sinkhorn divergence (for sample complexity) with InfoNCE/MixCL (for representation) and IRLF max-causal-entropy (for reward shaping).

B. **Automated Conflict Curriculum**  
Draw inspiration from progressive hard-negative masking *and* TU-Delft conflicting demo recovery to schedule contradiction strength during training.

C. **Hardware-Aware Alignment**  
Jointly co-design FPGA/ASIC accelerators with hallucination detectors so that safety checks run at generation time (<10 µs).  Use pattern-recognition mezzanine boards as drop-in safety coprocessors.

D. **Adaptive Bias Calibration**  
Leverage directional confusion bias to monitor when negative questioning inadvertently shifts model-class preference; integrate real-time bias metrics into the Audit stage.

E. **Multi-Exit Knowledge Distillation**  
Merge `OKDDip`, `MSKD`, and *group-leader* distillation with negative questioning so that early exits already reflect hallucination-aware logits.

F. **Contrarian KGs + Retrieval**  
Marry ClaimsKG/OpenGPT-X with contradiction querying: for every generated claim, retrieve *counter-evidence* and ask the model to self-refute; measure hallucination update via FactCHD.

G. **Psychological Plausibility**  
Explore hippocampus-style *inhibitory control* mechanisms (as in AVH studies) implemented through learnable gating or Tsallis-entropy regularisation.

---

## 8  Risk Assessment & Mitigations

| Risk | Origin | Mitigation |
|------|--------|-----------|
| *Over-regularisation* | Excess negatives collapse representation (Af-GCL shows augmentations may under-represent high-freq info). | Progressive masking, curriculum. |
| *Bias Amplification* | Directional class confusion; negative sampling skew. | Real-time bias dashboard, adjust sampling. |
| *Performance Regression on Updates* | LLteaM observed drastic drop after GPT-3.5 update. | CI pipeline that re-evaluates HaELM & HaloCheck after every model bump. |
| *Hardware Integration Bottlenecks* | Lat/throughput mismatch. | Use associative-memory pattern chips; ensure <10 µs budget. |

---

## 9  Actionable Checklist for Deployment

1. **Data Collection**  
   ☐ Mine conflict Q-A pairs via AutoDebug over ClaimsKG & FactCHD.  
   ☐ Label with HaELM local evaluator; store *both* positive & negative chains.
2. **Model Training**  
   ☐ Initialise ELECTRA-style dual network with gradient-correction for false-negatives.  
   ☐ Plug MixCL loss with progressive hard-negative masking.  
   ☐ Reward-fine-tune via IRLF variant with failed demos.  
   ☐ Distill into a single inference model (OKDDip stage 2).  
3. **Inference Guard**  
   ☐ Embed Audit-Booster cascade (primary LLM → HaELM scorer → booster).  
   ☐ On-device associative-memory FPGA filters per-token patterns.  
4. **Monitoring**  
   ☐ Run HaloCheck & Med-HALT nightly; track directional bias metric.  
   ☐ Auto-rollback if hallucination or bias KPIs spike.

---

## 10  Concluding Remarks
Negative questioning is not a silver bullet, but **every strand of evidence—from SVMs to IRL to human cognition—converges on the thesis that *structured contradictions* accelerate learning, sharpen decision boundaries, and can dramatically suppress hallucination-like errors**.  
The research ecosystem now offers:
• Rigorous theory (ERC bounds, Sinkhorn sample-complexity, IRL misspecification).  
• Scalable practice (MixCL, gradient-corrected ELECTRA, OKDDip distillation).  
• Repeatable evaluation (HaELM, HaloCheck, FactCHD, Med-HALT).  
The next frontier lies in **tight end-to-end integration**—from dataset curation to hardware coprocessors—such that negative questioning becomes a *first-class citizen* of LLM alignment pipelines rather than an after-the-fact patch.


## Sources

- https://hal.science/hal-03617746
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.5785
- http://arxiv.org/abs/2308.15126
- https://figshare.com/articles/_Reversal_learning_and_set_shifting_in_the_ASST_task_/841147
- http://hdl.handle.net/10.3389/fpsyg.2022.1017865.s001
- https://zenodo.org/record/3741842
- http://opensiuc.lib.siu.edu/cgi/viewcontent.cgi?article%3D1316%26context%3Dtpr
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-179593
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/49/e9/fnbeh-09-00060.PMC4357306.pdf
- https://lirias.kuleuven.be/handle/123456789/356241
- https://zenodo.org/record/5523918
- http://arxiv.org/abs/2308.11764
- http://140.118.1.157/cht/BPM/BPM
- http://hdl.handle.net/11384/79835
- https://dialnet.unirioja.es/servlet/oaiart?codigo=5679133
- http://www.loria.fr/%7Eignatcla/pmwiki/pub/papers/RohRR12.pdf
- http://hdl.handle.net/10.1371/journal.pone.0276729.s005
- http://arxiv.org/abs/2307.15343
- https://research.rug.nl/en/publications/bced5917-f3b4-457e-9e7b-914f2628606f
- http://doi.org/10.15027/28510
- http://hdl.handle.net/10255/dryad.126971
- https://dx.doi.org/10.3390/e16073552
- http://cds.cern.ch/record/1273162
- https://repository.urosario.edu.co/handle/10336/22905
- http://scholarworks.csun.edu/xmlui/handle/10211.2/286
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.6232
- https://zenodo.org/record/8229448
- http://www.thinkmind.org/download.php?articleid%3Dap2ps_2011_2_10_30063
- http://arxiv.org/abs/2203.12821
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S014976341300225X/MAIN/application/pdf/54191c0910bdb5b2990e657f180a0670/main.pdf
- https://hdl.handle.net/10356/158301
- http://cds.cern.ch/record/1414218
- https://zenodo.org/record/4487154
- http://www.cs.iastate.edu/~yetianc/cs573/files/CS573_ProjectReport_YetianChen.pdf
- http://arxiv.org/abs/2205.10536
- https://zenodo.org/record/3696079
- http://hdl.handle.net/10.1371/journal.pone.0206283.t005
- http://hdl.handle.net/10.1371/journal.pone.0280387.g003
- https://hal.science/hal-03617766
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/45/b9/sbu011.PMC4141312.pdf
- http://seab.envmed.rochester.edu/jeab/articles/1997/jeab-68-02-0143.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050915015239/MAIN/application/pdf/3765dc98b9c3fe7b85279081bbd0cd1b/main.pdf
- https://doaj.org/article/126ac529d038468ca46586397374f5a0
- http://arxiv.org/abs/2206.01535
- https://zenodo.org/record/3973431
- http://old.scielo.br/scielo.php?script=sci_arttext&pid=S1807-03022006000200011
- http://hdl.handle.net/10356/66506
- http://hdl.handle.net/11588/896159
- http://cds.cern.ch/record/2287313
- https://publications.aston.ac.uk/id/eprint/40898/1/1_s2.0_S0272735817300946_main.pdf
- https://hal.archives-ouvertes.fr/hal-03014858
- https://zenodo.org/record/7919873
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1045%26context%3Drobotics
- https://journals.linguisticsociety.org/proceedings/index.php/BLS/article/view/1432
- http://arxiv.org/abs/2204.04874
- http://arxiv.org/abs/2205.16004
- http://cds.cern.ch/record/2306350
- https://hal.archives-ouvertes.fr/hal-02404153/file/ClaimsKG_A_knowledge_graph_of_annotated_claims.pdf
- https://zenodo.org/record/7585083
- http://arxiv.org/abs/2008.07284
- https://figshare.com/articles/_False_positive_rate_of_anti_DENV_IgM_ELISA_Venture_Technologies_Sdn_Bhd_in_DENV_negatives_and_challenge_panel_specimens_/1207680
- http://cds.cern.ch/record/2093540
- http://etd.adm.unipi.it/theses/available/etd-06242014-055001/
- http://sifaka.cs.uiuc.edu/course/ds/kldir.pdf
- http://www.um.es/analesps/v26/v26_1/06-26_1.pdf
- http://hdl.handle.net/10.1371/journal.pone.0272127.t004
- https://theses.hal.science/tel-01956591
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2022-03849%22
- www.duo.uio.no:10852/74707
- https://research.chalmers.se/en/publication/189640
- http://hdl.handle.net/10560/1675
- http://arxiv.org/abs/2207.00148
- http://ieeexplore.ieee.org/xpl/conferences.jsp
- http://hdl.handle.net/10379/12911
- https://doaj.org/article/a10526f255b846b6841836c93a30ca18
- http://hdl.handle.net/10.1371/journal.pcbi.1010480.t002
- https://zenodo.org/record/8296440
- https://figshare.com/articles/_Positive_avoidance_8211_negative_approach_inconsistent_pattern_/1002755
- https://figshare.com/articles/_Number_of_samples_contained_in_positive_negative_test_set_used_for_performance_evaluation_of_MLLE_with_different_distance_metrics_on_different_IRMA_category_/877894
- https://repositorio.konradlorenz.edu.co/handle/001/1147
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050915005402/MAIN/application/pdf/67ee4e992009f308a121784460a2c5c8/main.pdf
- https://escholarship.org/uc/item/3bk48019
- http://cds.cern.ch/record/2289503
- https://zenodo.org/record/4723171
- http://hdl.handle.net/10.1371/journal.pone.0215357.g008
- https://doaj.org/toc/1932-6203
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.432.6314
- https://figshare.com/articles/_Negative_patterning_and_simple_discrimination_paradigms_/760855
- https://figshare.com/articles/_False_positive_rate_of_anti_DENV_IgM_rapid_diagnostic_tests_in_DENV_negatives_and_challenge_panel_specimens_/1207686
- http://hdl.handle.net/10.36227/techrxiv.21203096.v1
- https://figshare.com/articles/_Positive_approach_negative_avoidance_consistent_pattern_/1002754
- https://ojs.aaai.org/index.php/AAAI/article/view/26596
- https://aisel.aisnet.org/pacis2018/254
- https://escholarship.org/uc/item/25g6573w
- http://arxiv.org/abs/2203.13457
- http://ebooks.ien.bg.ac.rs/1724/1/milovanovic%20et%20al.pdf
- https://figshare.com/articles/_Weighted_classification_score_for_the_full_range_of_thresholds_using_different_trade_offs_between_false_negative_and_false_positive_cases_/1607955
- http://hdl.handle.net/11568/538956
- http://tesi.cab.unipd.it/65910/1/Franceschetto_Giacomo.pdf
- http://hdl.handle.net/2108/292936
- https://zenodo.org/record/5817082
- https://scholarworks.gsu.edu/cs_diss/8
- https://ir.cwi.nl/pub/22257
- http://repository.tue.nl/772222
- https://ojs.aaai.org/index.php/AAAI/article/view/21428
- http://jphyscol.journaldephysique.org/10.1051/jphyscol:1986506/pdf
- http://hdl.handle.net/10.25384/sage.7212356.v1
- http://dx.doi.org/10.1163/22134468-20191163
- https://spectrum.library.concordia.ca/id/eprint/28/1/MM68780.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26639
- https://zenodo.org/record/6407084
- http://cds.cern.ch/record/2266416
- http://www.nusl.cz/ntk/nusl-239090
- http://arxiv.org/abs/2309.05217
- https://zenodo.org/record/825515
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.3927
- http://resolver.tudelft.nl/uuid:edcf1a42-416c-4969-a625-898f2c28418b
- https://ojs.aaai.org/index.php/AAAI/article/view/17141
- https://research.rug.nl/en/publications/8e18419a-ed43-4be6-a0ca-7d55eb0d57df
- https://docs.lib.purdue.edu/purc/2019/Posters/16
- http://hdl.handle.net/
- https://zenodo.org/record/8123311
- http://www.mcs.anl.gov/~balaji/pubs/2013/icpads/icpads13.gpu-perf.pdf
- http://hdl.handle.net/1773/45788
- https://figshare.com/articles/_Number_of_positive_and_negative_instances_in_testing_and_training_dataset_/1027279
- http://sci2s.ugr.es/keel/pdf/specific/congreso/guo_on_2008.pdf
- http://arxiv.org/abs/2202.03629
- https://cris.maastrichtuniversity.nl/en/publications/5e6e1948-039d-4db1-b981-5e06e50b0977
- https://doaj.org/article/ff732616bb6f4f3f95909dd5a2372c42
- http://arxiv.org/abs/2205.11332
- https://zenodo.org/record/4732421
- http://hdl.handle.net/20.500.11794/68251
- http://hdl.handle.net/10251/201319
- http://arxiv.org/abs/2310.12516
- http://cds.cern.ch/record/2779339
- https://opensiuc.lib.siu.edu/theses/2267
- https://doaj.org/article/aad678e5c42e4a1f89ce8a94a9fa9a2a
- http://hdl.handle.net/10.1371/journal.pone.0295678.g002
- https://ojs.aaai.org/index.php/AAAI/article/view/26319
- https://bioling.psychopen.eu/index.php/bioling/article/view/13153
- http://hdl.handle.net/10.1371/journal.pone.0296171.g004
- http://hdl.handle.net/11025/29516
- https://dare.uva.nl/personal/pure/en/publications/do-language-models-understand-anything(7c218577-ba24-43ac-86d7-575bd25c12cd).html
- http://arxiv.org/abs/2310.12086
- https://doi.org/10.1016/j.schres.2006.03.008
- https://scholarworks.unist.ac.kr/handle/201301/54969
- http://cvi.asm.org/content/early/2008/06/18/CVI.00157-08.full.pdf
- http://hdl.handle.net/2152/27822
- https://ojs.aaai.org/index.php/AAAI/article/view/12108
- https://orbi.uliege.be/handle/2268/237187
- http://hdl.handle.net/1959.14/302383
- https://zenodo.org/record/555999
- http://scholarbank.nus.edu.sg/handle/10635/40794
- https://digitalcommons.kennesaw.edu/context/dataphd_etd/article/1017/viewcontent/Sayenju_PhD_Dissertation.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17234
- http://raiith.iith.ac.in/2551/1/iWML_2016_paper_25.pdf
- https://orbi.uliege.be/handle/2268/291548
- https://hal.archives-ouvertes.fr/hal-02440364/document
- https://figshare.com/articles/Houben_Open_Practices_Disclosure_Supplemental_material_for__Lateral_Eye_Movements_Increase_False_Memory_Rates/6270362
- https://zenodo.org/record/6577777
- https://hdl.handle.net/1721.1/128237
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.3489
- https://zenodo.org/record/7570475
- http://www.mathematik.uni-kl.de/uploads/tx_sibibtex/poisson_parameter_revised_01.pdf
- https://figshare.com/articles/_Schematic_of_the_Induced_Roelofs_Effect_/633014
- http://featureselection.asu.edu/fsdm10/fsdm10.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26766
- http://resolver.tudelft.nl/uuid:8a452b02-0237-4131-b47d-92244c9916b1
- http://dspace.library.uu.nl/handle/1874/338442
- http://dx.doi.org/10.1007/978-3-642-21090-7
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.9726
- https://figshare.com/articles/_Number_of_samples_contained_in_positive_negative_test_set_used_for_performance_evaluation_of_different_dimensionality_reduction_methods_on_different_IRMA_category_/877898
- https://research.monash.edu/en/publications/9ba9317f-e650-42d7-aa3d-568444538440
- http://scholarbank.nus.edu.sg/handle/10635/41603
- http://www.eecs.berkeley.edu/%7Ecarreira/papers/iccv2013.pdf
- http://arxiv.org/abs/2105.07636
- https://zenodo.org/record/7011631
- https://figshare.com/articles/Mean_false_positives_per_minute_for_all_activity_monitors_during_the_non-stepping_prescribed_activities_/4554571
- http://hdl.handle.net/11566/70876
- http://hdl.handle.net/1959.13/24467
- https://e-space.mmu.ac.uk/30028/1/stirling%2Band%2Bshon.pdf
- http://dro.deakin.edu.au/eserv/DU%3A30039519/zhang-anunified-2007.pdf
- http://hdl.handle.net/10.1371/journal.pcbi.1006267.g008
- https://hrcak.srce.hr/78374
- https://orbi.uliege.be/handle/2268/4326
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/a3/ce/2190-8567-2-2.PMC3365869.pdf
- https://tel.archives-ouvertes.fr/tel-02458044/document
- http://hdl.handle.net/1853/53167
- http://malgen.googlecode.com/files/malstone-TR-09-01.pdf
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll40/id/480290
- https://ojs.aaai.org/index.php/AAAI/article/view/5746
- http://hdl.handle.net/20.500.11850/508888
- https://elib.dlr.de/47496/
- https://figshare.com/articles/_The_number_of_false_targets_identified_from_Mock_Mock_comparisons_after_AD_or_Median_normalization_/174339
- https://figshare.com/articles/_The_false_positive_rate_for_the_four_networks_and_estimation_methods_/1532927
- https://figshare.com/articles/Precision_recall_and_F_measure_results_from_adaptive_thresholds_on_MSRA_1000_/2767105
- https://figshare.com/articles/_Estimating_the_statistical_power_of_the_test_for_the_presence_of_spatial_correlations_in_RGC_dipole_angles_/912967
- http://www.cin.ufpe.br/%7Ecompint/aulas-IAS/kdd-112/material/Artigos_MSc+CIn/2009_IEEE_IRI_Integration+and+Knowledge+Reuse+Environment.pdf?origin%3Dpublication_detail
- http://hdl.handle.net/2142/99421
- http://www.ee.usyd.edu.au/people/philip.leong/UserFiles/File/theses/chang12.pdf
- https://hal.science/hal-01199905
- https://research-portal.st-andrews.ac.uk/en/researchoutput/automatic-opencl-device-characterization(4e9aedaa-9287-46d5-891e-0f381b17a4ba).html
- https://figshare.com/articles/_False_negative_errors_against_synapse_size_and_perforation_/1073704
- https://napier-repository.worktribe.com/file/3503113/1/An%20Entity%20Ontology-Based%20Knowledge%20Graph%20Embedding%20Approach%20To%20News%20Credibility%20Assessment%20%28Accepted%20Version%29
- http://arxiv.org/abs/2205.15308
- http://hdl.handle.net/11568/177755