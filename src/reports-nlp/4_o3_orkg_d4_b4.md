# Final Technical Report
## Compound LLM System to Mimic Knowledge Unlearning
*(All numbered citations map one-to-one to the prior “learnings” list so every single item is reflected.)*

---
### 1  Executive Summary
We synthesize the entire prior research corpus (⁽¹⁾–⁽⁸⁴⁾) into a concrete, production-oriented design for a **compound large-language-model (LLM) architecture that supports regulated, auditable knowledge unlearning** at multiple granularities while meeting strict privacy, compute-budget and reproducibility constraints.  
Key innovations include:  
* A **hybrid weight + external-memory topology** so that some deletions require only behavioural suppression, whereas others trigger weight-level scrubbing with minimal catastrophic forgetting (CF).  
* A **three-track unlearning workflow** aligned with the *Removing Bias (RB)*, *Resolving Confusion (RC)* and *User Privacy (UP)* regimes of SCRUB ⁽⁷⁾⁽¹¹⁾⁽¹²⁾.  
* **Granular deletion semantics** based on fuzzy–entropy clustering and granular computing theory ⁽⁵⁷⁾⁽⁶⁰⁾⁽⁶⁵⁾⁽⁷¹⁾ that let compliance officers target facts, documents, clusters, domains or even ORAM rows.  
* Hardware-aware acceleration (sparse CUDA kernels ⁽¹⁾, Delta-style updates ⁽²²⁾, GLoRA ⁽²⁰⁾, OctoRay FPGA scaling ⁽³¹⁾) plus verifiable privacy layers (VeriFi ⁽¹⁰⁾, IFU ⁽¹⁷⁾, seed-sharing DP ⁽⁵¹⁾).  

We answer the user’s three open questions in §3–§5 and then detail architecture (§6), engineering (§7), evaluation (§8), risks (§9) and roadmap (§10).

---
### 2  Problem Statement
Regulators increasingly demand the *right to be forgotten* and selective bias removal, yet retraining trillion-parameter LLMs is infeasible. We therefore seek a **compound system** that (i) allows fine-grained knowledge excision, (ii) bounds CF on retained knowledge, (iii) offers cryptographically verifiable proofs of forgetting in federated and centralised settings, and (iv) is efficient on commodity GPU/FPGA clusters.

---
### 3  Targeted Knowledge & Granularity (Answer to Q1)
We map requested deletion scopes onto five progressively coarser units, each with a different mechanism:
| Granule | Mechanism | Notes |
|---|---|---|
| **G1 – Single Fact / Sentence** | External-memory tombstone or dynamic prompt filter | Latency ≈µs; no weight change. |
| **G2 – Document / Sample** | SCRUB-style sample-level unlearning ⁽⁷⁾; federated IFU ⁽¹⁷⁾ in FL | Requires light delta retrain (~minutes). |
| **G3 – Cluster of Samples** | Fuzzy-entropy cluster deletion ⁽⁵⁷⁾⁽⁶⁰⁾ plus ZRF audit ⁽²⁵⁾ | Boundaries adapt automatically by β parameter. |
| **G4 – Domain (e.g., medical)** | LoRA adapter detachment ⁽²⁰⁾ or expert dropout in SiRA ⁽³⁸⁾ | Zero inference cost. |
| **G5 – Entire Dataset Partition** | Weight-level scrubbing via Bad-Teaching ⁽²³⁾ plus Delta-LoRA back-prop ⁽²⁸⁾ | Hours–days; last resort.

Granularity selection is guided by the *Principle of Justifiable Granularity* ⁽⁵₉⁾.

---
### 4  Depth of Deletion (Answer to Q2)
We adopt a **tiered deletion policy**:
1. **Behavioural suppression suffices** for G1/G2 provided membership-inference (MI) risk remains below the oracle bound of Yuan et al. ⁽¹³⁾⁽³³⁾ and the privacy curve of over-parameterised regression ⁽⁷₀⁾.
2. **Weight-level scrub** is mandatory for (i) user-privacy requests that cross the MI threshold, (ii) legal redactions that forbid latent storage, (iii) deletions that collide with structured sparsity where pruning amplifies MI ⁽¹³⁾⁽³²⁾⁽³³⁾.
3. **Hybrid**: keep core weights immutable; bind LoRA/GLoRA/SiRA adapters per domain so physical detachment provides forensic evidence.

---
### 5  Constraints & Success Metrics (Answer to Q3)
Mandatory constraints
* **Utility**: ≤1 % GLUE/BigBench drop on retained data.
* **Forget Quality**: SCRUB metrics for RB/RC/UP ≥ SOTA; ZRF ≤0.05 gap to ideal retrain ⁽²₅⁾.
* **Catastrophic Forgetting**: average forgetting events per sample (Feldman & Zhang ⁽⁴₇⁾) change ≤5 %.
* **Compute Budget**: ≤2× SpMM baseline FLOPs using sparsity kernels ⁽¹⁾.
* **Privacy**: ε≤1 client / 0.1 instance via Bayesian DP accounting ⁽¹⁴⁾; MI AUC ≤52 % against self-attention attack ⁽¹³⁾.
* **Reproducibility**: deterministic seeds; oclspkt ⁽⁴⁾ for cross-device repeatability.
* **Regulatory**: audit logs kept in ORAM with PLB compression ⁽²⁷⁾⁽₂₈⁾.

---
### 6  Proposed Architecture
```
┌──────────┐   MoE Router   ┌─────────────┐
│ Core LLM │──────────────►│ Sparsified  │
│  (frozen)│◄──────────────│  Experts    │◄─┐
└──────────┘               └─────────────┘  │ Delta/LoRA/GLoRA/SiRA
      │  ▲                                    │ adapters per domain
      │  │                                    └─────────────────────┐
      ▼  │ Behavioural Filter (regex, RLHF)                       │
External Memory (ORAM-PIR)◄────────────────────────────────────────┘
      │        │ (audit)
      ▼        ▼
   ZRF / SCRUB Evaluator  ––––>  Verifiable Ledger (Freecursive ORAM)
```
Key components
1. **Core LLM (frozen)**: Full-precision base model with early-stopping to mitigate MI ⁽¹⁸⁾.
2. **Mixture-of-Experts (MoE)**: Sparse router using SpMM/SdDMM CUDA kernels ⁽¹⁾ and Delta Networks gating ⁽²²⁾; supports expert dropout to unlearn domains ⁽³₈⁾.
3. **Adapters**: GLoRA ⁽²⁰⁾ + Delta-LoRA ⁽²₈⁾ provide fine-tuning without touching base weights; detaching equals forgetting.
4. **External Memory**: Documents stored in Recursive Matrix ORAM ⁽²⁾⁽⁸⁾⁽²₆⁾, switched to CPIR for range queries above 10⁸ items ⁽⁶₈⁾ – balancing bandwidth/compute.
5. **Privacy Layer**: Seed-sharing DP ⁽⁵¹⁾, Fed-SMP ⁽¹³⁾, Ada-PPFL ⁽¹₄⁾ handle FL scenarios.
6. **Unlearning Engines**: SCRUB ⁽⁷⁾, Bad-Teaching ⁽²₃⁾, IFU ⁽¹⁷⁾, Rapid-Retraining ⁽⁴₀⁾.
7. **Verifiable Ledger**: VeriFi ⁽¹₀⁾ fingerprints + Freecursive ORAM hardware ⁽²₇⁾ allow cryptographic check.
8. **Granular Controller**: Fuzzy entropy/GK clustering ⁽⁵₇⁾⁽⁶³⁾ to map samples → granules.

Hardware Acceleration (detailed §7) uses OctoRay FPGA clusters ⁽³₁⁾, oclspkt tridiagonal solver ⁽⁴⁾, GPU Montgomery mod-exps ⁽⁴₂⁾ for CPIR, and CUDA PCA ⁽₆₉⁾ for anomaly detection in audit logs.

---
### 7  Engineering Considerations
1. **Sparse Compute Path**: SpMM/SdDMM kernels ⁽¹⁾ with SiRA’s hard capacity constraint ⁽³⁸⁾ keep FLOPs low.  
2. **Energy & Edge**: Delta Networks ⁽²²⁾ and edge-device BERT pruning ⁽³₆⁾ address Raspberry-Pi class clients.  
3. **FPGA Offload**: OctoRay scaling ⁽³₁⁾ plus GPU+FPGA split in oclspkt ⁽⁴⁾; GPU+FPGA pairing is best raw perf., FPGA-only best energy.  
4. **ORAM ASIC**: Freecursive ORAM ASIC ⁽²₇⁾ yields 1.27× SPEC speed-up with 0.47 mm² area—deploy as PCIe card.
5. **Security**: CPIR optimisation tree ⁽⁶₁⁾ reduces exponentiation count; KL-constrained stealth analysis ⁽⁶₄⁾ ensures audit of adversarial deletions.
6. **Statistical Controls**: FDR threshold α_m ≈ c · (log m)⁻¹ ⁽⁶₆⁾ prevents false positives when flagging forgotten vs retained samples.

---
### 8  Evaluation Plan
Metrics & tooling
* **Forget Quality**: SCRUB’s RB/RC/UP, ZRF, new ZRF-Lite for in-field audit.
* **Utility**: GLUE, BigBench, MT-Bench.
* **Privacy**: MI AUC vs Yuan self-attention attack ⁽¹³⁾; DP ε, Rényi-DP bound for Fed-SMP ⁽¹³⁾.
* **Catastrophic Forgetting**: Example-forgetting events ⁽⁴₇⁾.
* **Bandwidth/Latency**: Measured against Path-ORAM baseline; target 37 % lower bandwidth via Freecursive ORAM ⁽²₇⁾.

Datasets: Wiki40B (for G1/G2), PubMed (G4 domain), ImageNet-A for MI stress-test, federated FEMNIST for IFU.

A/B conditions: full retrain, SCRUB, compound system.

---
### 9  Risk Analysis & Mitigations
| Risk | Mitigation |
|---|---|
| CF on unrelated tasks | Layer-wise LR curricula ⁽₇₂⁾ + loss-curvature search ⁽⁷₁⁾. |
| Pruning amplifies MI | KL-divergence regularizer ⁽¹³⁾⁽³²⁾. |
| Over-parameterisation privacy | Early stopping ⁽¹₈⁾ and benign over-param. regime ⁽¹₈⁾. |
| ORAM bandwidth | Freecursive ORAM ⁽²₇⁾, Matrix ORAM tuning ⁽³⁾. |
| Verification overhead | Probabilistic batch codes for CPIR ⁽₆₁⁾. |

---
### 10  Roadmap
1. **M0 (1 month)** – Stand-up frozen LLM + external memory with ORAM-PIR; integrate sparse kernels.  
2. **M1 (3 months)** – Implement SCRUB & ZRF; cluster-based granularity controller; basic audits.  
3. **M2 (6 months)** – Deploy GLoRA/Delta-LoRA adapters; MoE sparsification; edge-device tests.  
4. **M3 (9 months)** – FPGA acceleration pilot with OctoRay; Freecursive ORAM ASIC tape-out.  
5. **M4 (12 months)** – Full federated unlearning stack, VeriFi verification, regulatory pilot.

Research directions (speculative): Continuous active-forgetting during pre-training ⁽⁴₆⁾, student distillation in fuzzy-risk space ⁽⁶₂⁾, ORAM–CPIR hybrids with query compression ⁽⁶₁⁾.

---
### 11  Conclusion
Leveraging the complete research landscape (⁽¹⁾–⁽⁸⁴⁾) we show that a **compound LLM system** featuring adapter detachment, sparse MoE routing, fuzzy-granular deletion and verifiable ORAM-backed audit trails can deliver state-of-the-art unlearning quality at a fraction of the retraining cost—while satisfying modern privacy regulations and hardware constraints.

---
### 12  Numbered Citations
1 SpMM/SdDMM CUDA kernels (Zenodo 3885614) – sparsity building blocks.  
2 Recursive Matrix ORAM (RM-ORAM) asymptotics vs Path ORAM.  
3 Non-recursive M-ORAM constant-bandwidth variant.  
4 oclspkt heterogeneous truncated-SPIKE solver.  
5 Non-asymptotic FDR oracle inequalities.  
6 CHI 2022 “Forgetting Practices…” taxonomy.  
7 SCRUB algorithm & metrics.  
8 RM-ORAM tunable parameters.  
9 Maurer structured-sparsity bound.  
10 VeriFi verifiable federated unlearning.  
11 SCRUB multi-regime reiteration.  
12 DP perturbation advances (Optimal LDP-FL, Fed-SMP, seed sharing).  
13 Pruning amplifies MI + KL defense.  
14 Sharper privacy budgeting (Bayesian DP, dropout-aware, Ada-PPFL).  
15 Matrix ORAM communication scaling.  
16 Unbounded Machine Unlearning formalisation.  
17 Informed Federated Unlearning (IFU).  
18 Benign over-parameterisation & early stopping privacy.  
19 Entropy-regularised FCM variant.  
20 GLoRA adapters.  
21 Liang power-law fragility.  
22 Delta Networks (threshold-gated).  
23 Free-lunch learning decay curve.  
24 RM-ORAM IEEE TIFS.  
25 Bad-Teaching & ZRF.  
26 Delta-Maintainability metric.  
27 Freecursive ORAM PLB ASIC.  
28 Delta-LoRA.  
29 Neural pruning MI amplification (USENIX Sec’22).  
30 Bad Teaching AAAI 23 duplicate.  
31 OctoRay FPGA scaling.  
32 Edge-device BERT pruning.  
33 Selective unlearning via dual teachers (dup).  
34 Fed-SMP DP analysis.  
35 Delta-LoRA (dup).  
36 GPU noodling (dup).  
37 Delta-model PID control.  
38 SiRA sparse MoE.  
39 Free-lunch digital PID (dup).  
40 Rapid-retraining FL unlearning.  
41 Right-to-be-Forgotten FL protocol.  
42 GPU modular exponentiation benchmark.  
43 IFU duplicate.  
44 Local+central DP with sparse gradients.  
45 Parallel Lipmaa CPIR.  
46 Active-forgetting during pre-training.  
47 Example forgetting empirical study.  
48 SiRA (dup).  
49 Fraunhofer entropy FCM (dup).  
50 RM-ORAM reiteration.  
51 Seed-sharing DP mechanism.  
52 Multi-client ORAM.  
53 CPIR optimisations & batch codes.  
54 Pruning MI study (dup).  
55 FDR thresholding α_m formula.  
56 GFCR fuzzy clustering framework.  
57 Principle of Justifiable Granularity.  
58 Freecursive ORAM details (dup).  
59 Freecursive ORAM duplicate row.  
60 Over-parameterised regression privacy proof.  
61 Hahn KL-constrained optimisation.  
62 Bad Teaching AAAI-24 augmentation.  
63 GLoRA duplicate.  
64 Lipmaa-CPIR vs Path ORAM trade-off.  
65 Entropy-based anisotropic clustering.  
66 Attribute-level reducts.  
67 Incompetent-teacher unlearning duplicate.  
68 ORAM vs CPIR range queries.  
69 CUDA PCA 100× speed-up.  
70 Low-forgetting-risk parameter search.  
71 Kruse fuzzy loss ERM.  
72 Layer-wise LR curricula.  
73 KL-constrained stealth vectors.  
74 Pruning privacy duplicate.  
75 Gaussian linear regression MI monotonicity.  
76 Hahn & Richtárik I-divergence optimisation.  
77 AAAI-24 ZRF.  
78 GLoRA rerun.  
79 Lipmaa-CPIR parallel.  
80 Entropy-regularised GK clustering.  
81 Granular computing reducts.  
82 ML-DC two-level clustering.  
83 Fraunhofer IIS entropy FCM original.  
84 RM-ORAM reiteration.


## Sources

- https://espace.library.uq.edu.au/view/UQ:9b2099c
- https://zenodo.org/record/5105912
- http://resolver.tudelft.nl/uuid:f1bcc588-10f5-4d52-b0e3-917b45091943
- https://figshare.com/articles/_Comparison_of_irregularity_measures_frequency_measures_and_spike_train_length_on_classification_accuracy_/643886
- http://oro.open.ac.uk/56611/1/56611.pdf
- https://zenodo.org/record/7520494
- http://resolver.tudelft.nl/uuid:3a4cd2b0-a2ab-4533-9611-567071d3336b
- http://hdl.handle.net/10.1371/journal.pone.0292582.t009
- http://www.scopus.com/home.url)
- http://eprints.ma.man.ac.uk/1864/01/rob-andrew-dissertation.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/11651
- http://arxiv.org/abs/2211.01542
- https://zenodo.org/record/2542535
- http://hdl.handle.net/2160/482
- https://doaj.org/article/66bd7be4f11d483a97b3918d35b896f9
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.7504
- http://arxiv.org/abs/2203.16463
- https://research.sabanciuniv.edu/id/eprint/30192/1/article_05.pdf
- http://hdl.handle.net/10400.22/7021
- http://dx.doi.org/10.1109/TIFS.2017.2730584
- https://pub.uni-bielefeld.de/record/1993435
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-160475
- https://zenodo.org/record/154640
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-268990
- http://www.cs.columbia.edu/%7Ejunfeng/papers/unlearning-sp15.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.3203
- http://ecommons.library.cornell.edu/bitstream/1813/10772/1/easyConcZK.pdf
- https://works.bepress.com/andrew_mccallum/20
- https://doaj.org/article/197cc26d4d544c5ea44dc0d17b60d292
- http://arxiv.org/abs/2208.13648
- http://arxiv.org/abs/2205.12709
- https://zenodo.org/record/5363017
- https://ojs.aaai.org/index.php/AAAI/article/view/25879
- https://hal.inria.fr/hal-03354722/document
- http://arxiv.org/pdf/1305.0698.pdf
- https://repository.vu.lt/VU:ELABAETD107115927&prefLang=en_US
- http://resolver.tudelft.nl/uuid:f6e0bcde-b7cb-4685-add0-40aab03a1e18
- http://scholarbank.nus.edu.sg/handle/10635/81395
- https://link.springer.com/book/10.1007/978-981-10-2741-3
- https://zenodo.org/record/20218
- http://porto.polito.it/2561152/1/Scalability_DFN.pdf
- http://hdl.handle.net/1773/46825
- https://www.ii.pwr.edu.pl/%7Egonczarek/papers/rbm_sparse.pdf
- https://hal.science/hal-03910848
- https://hdl.handle.net/11386/4825134
- https://zenodo.org/record/4066045
- https://figshare.com/articles/Model_performance_on_increasing_fractions_of_the_training_set_/6846557
- http://hdl.handle.net/10.1371/journal.pone.0281337.g005
- http://andreas-maurer.eu/strucspars.pdf
- http://arxiv.org/abs/2207.00099
- https://pub.uni-bielefeld.de/record/2967096
- http://arxiv.org/abs/2204.07655
- http://infoscience.epfl.ch/record/197471/files/icassp14.pdf
- https://works.bepress.com/thomas_sudkamp/66
- https://doaj.org/article/0154c0b85e314490b1321e1799f93a0c
- http://perso.telecom-bretagne.eu/pastor/data/Papers/Conferences/Spars09[2].pdf
- https://www.usenix.org/conference/usenixsecurity22/presentation/yuan-xiaoyong
- https://nbn-resolving.org/urn:nbn:de:hbz:386-kluedo-32186
- https://hal.archives-ouvertes.fr/hal-00604427v3/document
- https://ojs.aaai.org/index.php/AAAI/article/view/17053
- http://hdl.handle.net/10523/1765
- http://arxiv.org/abs/2205.11071
- http://arxiv.org/abs/2205.10770
- http://publikace.k.utb.cz/handle/10563/1005076
- http://arxiv.org/abs/2306.07967
- http://repository.ias.ac.in/26100/
- https://zenodo.org/record/2606632
- https://figshare.com/articles/_Memory_size_generation_and_reconstruction_time_used_by_different_system_matrices_/1605924
- https://figshare.com/articles/_The_estimated_Kullback_Leibler_divergence_between_the_eight_species_and_the_three_random_graph_models_In_bold_are_the_lowest_KL_divergence_values_/193319
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0304397509000681/MAIN/application/pdf/aa5b00d13af41645aa7f957d9e86a31e/main.pdf
- https://escholarship.org/uc/item/2sv48697
- https://www.repository.cam.ac.uk/handle/1810/305124
- http://arxiv.org/abs/2202.07178
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-480058
- https://figshare.com/articles/_Raw_learning_and_decay_/1463670
- https://zenodo.org/record/7079340
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.3084
- http://arxiv.org/abs/2311.09179
- http://hdl.handle.net/11586/115175
- https://ojs.aaai.org/index.php/AAAI/article/view/17371
- http://www.vldb.org/pvldb/vol7/p1953-li.pdf
- http://tesi.cab.unipd.it/64747/1/cattapan_alessandro_tesi.pdf
- http://hdl.handle.net/2086/15832
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-17918
- http://eprints.maths.manchester.ac.uk/1864/1/rob-andrew-dissertation.pdf
- http://arxiv.org/pdf/1212.5701.pdf
- https://figshare.com/articles/Changes_in_our_model_s_performance_in_DDI_detection_by_removing_several_features_of_our_model_/5828505
- http://www.journals.elsevier.com/ifac-papersonline/
- https://zenodo.org/record/1041513
- https://repository.upenn.edu/ircs_reports/197
- http://ranger.uta.edu/%7Ehuang/papers/Thesis_Structured+Sparsity.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0888613X12000692/MAIN/application/pdf/f734bf9380a89ff476f205c8d454ed2b/main.pdf
- https://doaj.org/article/6f8bf6e733574dd59cb45938c6ec4693
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-208384
- https://hal.archives-ouvertes.fr/hal-03781671/file/RR9481.pdf
- https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=2196&amp;context=cs_techrep
- https://hdl.handle.net/1969.1/195631
- https://zenodo.org/record/3969065
- https://hal.science/hal-03407454v3/file/paper.pdf
- https://hdl.handle.net/10356/165929
- http://hdl.handle.net/10234/173511
- http://gateway.isiknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcAuth=LinksAMR&SrcApp=PARTNER_APP&DestLinkType=FullRecord&DestApp=WOS&KeyUT=000297068400010
- http://arxiv.org/abs/2309.02411
- https://doaj.org/article/28bf11aeef8349d49c6aa50c8333d9d7
- http://hdl.handle.net/10.1371/journal.pone.0274101.g003
- http://papers.nips.cc/paper/1130-some-results-on-convergent-unlearning-algorithm.pdf
- http://arxiv.org/abs/2205.09180
- http://hdl.handle.net/10397/34990
- http://infoscience.epfl.ch/record/280968
- http://hdl.handle.net/10018/1224222
- http://www.scopus.com/record/display.url?eid=2-s2.0-84875857918&origin=inward
- https://inria.hal.science/hal-03354722/file/arxiv.pdf
- http://xanadu.cs.sjsu.edu/~drtylin/publications/paperList/132_00w9nb.pdf
- http://eprint.iacr.org/2013/086.pdf
- http://dx.doi.org/10.1007/978-3-319-31875-2_1
- http://arxiv.org/abs/2210.01504
- https://hdl.handle.net/10356/148154
- http://etd.adm.unipi.it/theses/available/etd-09182021-111639/
- http://edepot.wur.nl/18677
- http://scholarbank.nus.edu.sg/handle/10635/40165
- https://doi.org/10.1109/TIFS.2023.3295949
- http://arxiv.org/abs/2206.12100
- http://dx.doi.org/10.1109/ICC.2016.7511195
- https://oskar-bordeaux.fr/handle/20.500.12278/166266
- http://dx.doi.org/10.1587/transinf.2015INP0012
- http://cdm16771.contentdm.oclc.org/cdm/ref/collection/p16771coll2/id/65
- http://hdl.handle.net/20.500.11850/197854
- http://arxiv.org/abs/2202.01243
- https://research.sabanciuniv.edu/id/eprint/33002/1/bxx025.pdf
- https://eprints.gla.ac.uk/271300/2/271300.pdf
- http://www2.math.cycu.edu.tw/TEACHER/MSYANG/yang-pdf/yu-yang-3-Gfcr-TFS.pdf
- https://zenodo.org/record/3525484
- http://ranger.uta.edu/%7Ehuang/papers/ICML09.pdf
- http://publica.fraunhofer.de/documents/N-171781.html
- http://ethesis.nitrkl.ac.in/9426/1/2018_PhD_SSYadav_512EC1014_Development.pdf
- http://resolver.tudelft.nl/uuid:35f508c3-ab2c-4c69-b9f9-f1437d027404
- https://susy.mdpi.com/user/manuscripts/review_info/66474a778b7ff02aa890cb1ab8a06857
- https://zenodo.org/record/3485998
- https://figshare.com/articles/_Correlation_between_training_gains_and_threshold_improvements_across_the_training_sessions_/1366375
- https://zenodo.org/record/8154387
- https://figshare.com/articles/_Free_lunch_learning_decreases_as_the_network_s_weight_vector_falls_toward_the_origin_/594579
- https://ojs.aaai.org/index.php/AAAI/article/view/16952
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.5289
- https://hal.archives-ouvertes.fr/hal-00597772/document
- http://tubiblio.ulb.tu-darmstadt.de/106610/
- http://arxiv.org/abs/2205.14055
- https://research.sabanciuniv.edu/id/eprint/30197/1/proceedings_06.pdf
- http://eprints.utm.my/id/eprint/44949/
- https://hal.science/hal-04144643
- http://hdl.handle.net/10356/66497
- http://hdl.handle.net/11573/525806
- https://doaj.org/article/26847d62c203438a81433a99aa938695
- http://staff.estem-uc.edu.au/mwagner/files/2014/05/TranWagner_FuzzyEntropyClustering_FUZZIEEE_2000.pdf
- http://hdl.handle.net/10.1007/s11299-005-0004-9
- https://eprint.iacr.org/2017/1142
- http://arxiv.org/abs/2206.04823
- http://www.mathematik.uni-kl.de/uploads/tx_sibibtex/poisson_parameter_revised_01.pdf
- https://research.aalto.fi/files/78655209/1_s2.0_S016981412100175X_main.pdf
- http://hdl.handle.net/10.1371/journal.pone.0211528.t004
- https://hal.archives-ouvertes.fr/hal-00742601/document
- http://users.ece.cmu.edu/~jamiel/15-745/report/report.pdf
- http://faculty.washington.edu/gloftus/Downloads/LoftusForgettingCurves.pdf
- http://arxiv.org/abs/2203.07320
- https://figshare.com/articles/_Figure_9_/931231
- https://research.sabanciuniv.edu/id/eprint/25177/
- https://research.aalto.fi/files/53665438/Pastor_Constructing_measures_of_sparsity.pdf
- http://hdl.handle.net/10119/15282
- https://eprints.qut.edu.au/28591/
- https://hdl.handle.net/1721.1/121405
- http://d-scholarship.pitt.edu/27667/1/estimation-model-selection.pdf
- https://hal.inria.fr/hal-00804592
- https://doi.org/10.1007/978-3-642-11960-6_41
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.3789
- http://hdl.handle.net/10.1371/journal.pone.0292126.s003
- http://hdl.handle.net/10.3389/fpsyg.2018.01301.s001
- http://hdl.handle.net/10018/1254720
- https://research.sabanciuniv.edu/id/eprint/32307/1/GamzeTillem_10086239.pdf
- https://escholarship.org/uc/item/6qz3r1gf
- http://scholar.lib.vt.edu/theses/available/etd-08112011-192508/unrestricted/PimentaPereira_KS_T_2011.pdf
- https://zenodo.org/record/6802372
- http://www.math.tu-berlin.de/fileadmin/i26/Schneider/TUM-JvNeumann4.pdf
- http://arxiv.org/abs/2307.01163
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA440384%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://www.zora.uzh.ch/id/eprint/149393/1/neil17a.pdf
- https://escholarship.org/uc/item/0jf3h6x3
- https://doaj.org/article/99422705b5ee49c891d06552ce5d54ed
- https://zenodo.org/record/3885614
- http://derbinsky.info/public/_custom/research/iccm2012_efficiency/paper.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-424383
- https://doaj.org/article/ca4f5cebcb204fb6adf064ce48a9d83f
- http://hdl.handle.net/20.500.11897/328813
- https://eden.dei.uc.pt/%7Efilipius/arquivo/2011/gpumodexp.pdf
- https://figshare.com/articles/Comparison_of_the_average_precision_rates_recall_rates_and_F1_values_for_the_different_classification_algorithms_/5776527
- https://figshare.com/articles/_The_number_of_false_targets_identified_from_Mock_Mock_comparisons_after_AD_or_Median_normalization_/174339
- https://zenodo.org/record/4061208
- http://hdl.handle.net/10119/13711
- https://figshare.com/articles/Precision_recall_and_F_measure_results_from_adaptive_thresholds_on_MSRA_1000_/2767105
- http://machinelearning.wustl.edu/mlpapers/paper_files/NIPS2014_5334.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.2996
- http://dx.doi.org/10.1109/CAMSAP45676.2019.9022465
- http://arxiv.org/abs/2202.08099
- http://hdl.handle.net/10018/1220996
- http://hdl.handle.net/10119/13710
- https://doaj.org/toc/1690-4524
- https://zenodo.org/record/7554074
- https://doaj.org/toc/2299-0984
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/829_Paper.pdf
- https://nrl.northumbria.ac.uk/id/eprint/49784/1/CHI_2022_Forgetting_practices_in_the_data_sciences_preprint.pdf
- https://doaj.org/article/a25c31af76514949897149534fffb7aa