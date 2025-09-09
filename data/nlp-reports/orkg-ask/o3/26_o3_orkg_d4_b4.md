# Algorithm-Supported Programming for Intellectual, Mathematical & Computational-Intensive Code Generation  
A Consolidated Report (2025-09-04)

---

## Executive Summary
Algorithm-supported programming (ASP) today spans an unusually wide design space: from **autotuning DSL compilers** such as Firedrake, through **SAT/SMT-based program synthesis**, to **LLM-powered pair programming** and **hardware/high-level synthesis (HLS)**.  
The attached research digest collects **>90 primary findings** (2011-2024) across scientific computing, cryptography, static analysis, cloud workflows, networking co-design and post-quantum security.  
Key messages:

1. **Domain-specific abstraction + automated lowering beats manual optimisation** for productivity while retaining 70–100 % of hand-tuned performance in most mature domains (finite-element FEM, FFT/NTT, image processing, lattice crypto).
2. **Encoding decisions dominate solver-centric pipelines** (CEGIS, MaxSAT, CSP→SAT); proper numeric or support encoding can shift instances from exponential to polynomial time.
3. **End-to-end reproducibility is becoming non-negotiable**: Zenodo-style immutable snapshots (e.g., Firedrake, Code4Bench, Franc) are now routinely cited and even pip-installable.
4. **Hardware/Network co-design is re-emerging**: GPU-Triggered Networking, XTQ and PsPIN style in-NIC RISC-V blocks eliminate CPU involvement and approach sub-µs launches at 400 Gb/s.
5. **LLM/Transformer models already solve ~50 % of routine coding tasks**, but require post-processing filters (FRANC) to raise compilability up to +46 % and remove 80 % of security smells.
6. The main open gaps are: (i) lack of evaluation on **2023+ accelerators** (NVIDIA H100, AMD MI300A), (ii) **maintenance/traceability metrics** in workflow studies, (iii) **multi-domain benchmark suites** that cover both symbolic and numeric ASP.

The remainder of this report organises the evidence, highlights trade-offs, and closes with design recommendations for the next generation of ASP frameworks.

---

## 1  Taxonomy of Algorithm-Supported Programming Approaches

| Category | Core Idea | Representative Artifacts | Key Advantages | Principal Limitations |
|----------|-----------|--------------------------|----------------|----------------------|
| AI-driven code generation | Pre-trained LLMs (CodeT5, AlphaCode, CodeGen), ML-guided superoptimisers | FRANC filter+repair, Edit Progress metric, Code4Bench | Rapid prototyping, language agnostic, improving with scale | Low uniqueness, over-use of loops & wide types, vulnerability injection, unpredictable perf |
| Formal algorithm synthesis | CEGIS(T), Sketch w/ Adaptive Concretisation, U-Automizer chains | Exponential speed-ups from better encodings, soundness guarantees | Solver fragility, scaling beyond ~100 LOC, theory plug-in complexity |
| Autotuning DSL compilers | Firedrake, Porcupine (HE kernels), BOAST+StarPU, hls4ml | Portable high perf, reproduceable snapshots, domain insight encoded | Needs investment per domain, kernel boundaries still memory-bound |
| Hardware-level HLS / DSL | Catapult C, LegUp, Spatial, RVC-CAL, CRYKET | 4–126 × SW speed-up, 2× simulation speed, 3-6× shorter dev time | Vendor lock-in, Fmax gap vs hand RTL, area blow-ups (up to +84 %) |
| Network / Device co-design | XTQ, GPU-TN, PsPIN, NaNet | Sub-µs launch, 26 ns packet latency, 3 µs GPU-to-GPU | ASIC cost, SW ecosystem immaturity |
| Static analysis & live verification | Modular abstract interpretation (CiaoPP), dynamic self-adaptation, SATT | Real-time CI feedback, precision tuning | Limited to languages with mature IRs |

---

## 2  Scientific-Computing Pipelines (FEM, FFT, NUFFT)

### 2.1  Finite-Element Method (FEM)
* **Firedrake stack** (UFL → TSFC → COFFEE → Loopy → PETSc).  
  – Published Zenodo DOIs (e.g., 10.5281/zenodo.7143572) freeze every dependency, enabling byte-identical reproduction.  
  – Weak-form DSL (UFL) lets scientists describe a PDE in ≈10 lines; backend auto-generates CPU, GPU or heterogeneous kernels.  
  – Indirect memory access, not FP peak, is the bottleneck (FrontFlow/blue on K-computer). Cache/bandwidth tuning delivers larger gains than flop tuning.
* **Auto-tuning evidence**: BOAST + StarPU gave 1.9–5.7× across four many-core chips; dynamic schedulers match hand-tuned code.
* **Research gap**: no data on NVIDIA H100 or MI300A; an open benchmark could measure skewness-mesh kernels on Hopper GPUs.

### 2.2  Transforms (FFT, NTT, NUFFT)
* **Vilnius Univ. 2021**: Verilog best Fmax; LegUp shrank logic & dev time (6×).  
* **GPU NUFFT** (2007 – 2015): 5× over CPU; good candidate for tensor-core exploitation.  
* **FPGA NTT generators**: parameterised DSLs now achieve 28–48× speed-ups and 1.57 M NTT/s (Kyber).  
* **Key lesson** — generator + autotune allows **switchable in-place vs MDC datapaths** for FFT/NTT, letting designers hit specific fclk or BRAM targets.

---

## 3  Cryptography & Post-Quantum

1. **RVC-CAL Crypto Tools Library (CTL)**: emits C/C++/Java/LLVM/VHDL; SHA-256 matches handwritten; 4-adic hash trees 3× on quad-core.
2. **Lattice-crypto accelerators**: open-source Artix-7 design delivers 40–100× faster keygen and constant-time CDT sampler with 1.67–235 × better area-delay.
3. **VHDL Kyber core**: fastest NTT (322 cycles @ 637 MHz) with <30 DSPs. Indication that sub-µs PQC is feasible for HF trading/edge.
4. **CRYKET & GUIs**: provide Rapid design-space exploration without HDL expertise, even for cryptanalytic hardware.
5. **Homomorphic-Encryption DSL** (Porcupine) shows program synthesis can discover vector layouts missed by LLVM; synergy with hardware NTT suggests an integrated HE stack is within reach.

---

## 4  SAT/SMT & Search-Based Synthesis

* **Encoding sensitivity**: Binary vs unary vs mixed integer encoding can change SAT runtime by orders of magnitude; auxiliary clauses may act as poly-time preprocessing (exponential separation proof).
* **CEGIS(T)** upstream in CVC4: smaller SAT, incremental solving, wins benchmarks with non-trivial constants.  
* **Adaptive Concretisation for Sketch**: Exploits hill-climbing to ground high-influence unknowns; parallelises naturally.
* **Hyper-resolution** automatically derives faster support encoding from naive binary CSP encodings.

Implication: **auto-selecting or auto-synthesising encodings** should be a first-class feature of ASP frameworks that rely on solvers.

---

## 5  LLM-Driven Programming Assistance

* **AlphaCode**: low lexical overlap (cos 0.26) with 31 k human Codeforces answers; nested loops & wide types hurt efficiency.
* **CodeT5** surpasses SOTA on code-revision tasks by up to 39 %; new **Edit Progress (EP)** metric changes ranking.
* **FRANC pipeline**: Static Filter (+9–46 % compilability), Quality Ranker (+0.0763 NDCG) and Repair (up to 80 % vulnerable fix) in ≤2 s.
* **Compile-time Template Morphing**: Clang plugin swaps monomorphisation ↔ dynamic dispatch to cut code size.

Overall: **pairing LLMs with lightweight static analysis & repair closes ¾ of production-readiness gaps**.

---

## 6  Hardware/Network Co-Design & Offload

1. **GPU-Issued RDMA** (Fraunhofer): raw idea works but serialized WR generation dominates; offload only pays after protocol simplification.
2. **XTQ / GPU-TN / PsPIN**: sub-µs kernel launches, 26 ns per packet, 400 Gb/s in 22 nm → feasible today.
3. **NaNet FPGA NIC**: 34 Gbps APElink, deterministic 2.5 Gbps; CERN NA62 / KM3NeT used in production.
4. **RIBOSOME**: hybrid on-switch/off-host buffering; stateful 300 Gb/s firewalls on single x86.
5. **PCIe P2P host bypass**: 10 Gb/s from commodity GPUs shows a low-cost path for mid-tier systems.

Take-away: **Networking stack must be considered a first-class target for code generation**, especially for HPC & ML inference.

---

## 7  Tooling, Workflows & Reproducibility

* **Immutable Zenodo snapshots** (Firedrake, Code4Bench, Franc, V-FIT) make experiments pip-installable.  
* **Lifecycle management on K8s**: no agreed criteria; Operator Framework best measured but evaluation misses maintainability; SATT metric & KTH scoreboard fill gap.
* **Modular incremental analysis (CiaoPP) and LEAP profiler** offer real-time feedback in CI/CD.
* **Decision-tree FPGA classifier pipelines** demonstrate sub-100 ns latency; QuickScorer SoC variant keeps latency constant w.r.t tree count.

---

## 8  Cross-Cutting Trade-offs & Design Patterns

1. **Productivity ↔ Performance ↔ Portability**:  
   – HLS: 6× dev-time reduction vs hand RTL, but −10–30 % Fmax.  
   – DSL compilers: near-par perf, maximal portability, moderate domain effort.  
   – LLMs: minutes of effort, variable perf, portability only via post-processing.
2. **Vendor lock-in**: Catapult C proprietary types; mitigation is IR-level open standards (MLIR dialects, RVC-CAL).
3. **Memory bandwidth vs FLOPs**: FEM, HE, decision-tree pipelines all memory-bound; focusing on layout & BRAM re-org gives larger wins than ALU optimisation.
4. **Energy vs Latency**: FPGA samplers and on-chip decision trees offer 10–50 % energy savings and deterministic sub-µs latency—key for edge and satellite.

---

## 9  Recommendations for Designing a New ASP Framework

1. **Multi-Level IR Stack** adopting MLIR-style extensible dialects:  
   – High-level domain language (e.g., weak-form PDE, cryptographic primitive, SAT encoding)  
   – Mid-level autotuning IR (configurable blocking, vec layout)  
   – Low-level target (CUDA PTX, VHDL, P4)  
2. **Auto-encoding selector** that:  
   – Benchmarks binary/unary/mixed encodings on sample instances  
   – Learns a decision model (tree/NN) → picks encoding per problem.  
3. **Built-in Reproducibility**: automatic Zenodo/OCI artifact export with DOI, lock file & conda/pip environment YAML.
4. **Integrated Post-Processor for LLM blocks**: embed FRANC style filter-repair pipeline as default ingestion path for user-authored or AI-authored snippets.
5. **Hardware/Network-aware Scheduler**: exploit XTQ or PsPIN when available; fall back to PCIe P2P; store perf metadata and use decision-tree learning for future runs.
6. **Benchmark Harness** covering:  
   – FEM kernels (Firedrake snapshots)  
   – PQC (Kyber, qTESLA NTT)  
   – SAT-encoding problems (V-FIT, Code4Bench)  
   – LLM-generated code (SOEVAL, Codeforces)  
   – Networking micro-benchmarks (GPU-TN, NaNet).
7. **Contrarian idea — speculative**: host a **public “Encoding Futures Market”** where researchers submit new encodings or lowering passes, staked on gas-less crypto tokens; framework auto-benchmarks and rewards net speed-ups. *(Flagged as speculative)*

---

## 10  Open Research Directions

* **Accelerator Frontiers**: Evaluate ASP-generated FEM & NTT kernels on Hopper (H100) tensor cores & AMD MI300A CPU+GPU; explore if sparsity engines help indirect FEM access.
* **SAT-to-GPU**: Port CEGIS(T) or Adaptive Concretisation to run inside PsPIN or GPU-TN environment for micro-second reactive synthesis.
* **LLM × Formal Synthesis**: Train code-gen models on the *trace* of formal synthesis steps, producing debuggable rationales, not just final code.
* **Unified DSL for Network + Compute**: Extend UFL-style weak forms with message-passing operators targeting XTQ-enabled NICs.
* **Edge-Satellite ASIC frameworks**: Leverage XPP wavelet reconfigurability + SCCC-X to auto-compile compression/codec pipelines for radiation-tolerant FPGAs.

---

## 11  Conclusion
The collected evidence paints an optimistic picture: **algorithm-supported programming is no longer an exotic research topic but a practical necessity** for any domain where intellectual, mathematical and computational complexity collide.  
By fusing DSLs, formal synthesis, machine-learning guidance, hardware generation and rigorous reproducibility, we can now generate code **faster than we can manually write specifications**, while still retaining or even exceeding hand-tuned performance in many workloads.  
The next milestone is **holistic integration**—a single framework that treats encoding choice, autotuning, hardware mapping, network offload, and LLM post-processing as co-equal passes in a unified compilation pipeline.  
Such a system would let experts express only the *what*, leaving the *how* to an ever-improving stack of search, learning, and domain insight.


## Sources

- http://www.ijetsp.info/article/IJETSPV1I103.pdf
- http://hdl.handle.net/2299/18216
- http://publica.fraunhofer.de/documents/N-374955.html
- http://etd.adm.unipi.it/theses/available/etd-07022023-182035/
- https://doaj.org/article/fbdba590a9b443f7bc3485f385d4b062
- https://zenodo.org/record/8211917
- https://research.sabanciuniv.edu/id/eprint/40596/1/DATE_09116470.pdf
- http://hdl.handle.net/10.5061/dryad.1s1m8r7/11
- http://resolver.tudelft.nl/uuid:3992a2cc-7002-44ed-8e58-f45027a81993
- https://zenodo.org/record/1189453
- http://hdl.handle.net/1773/47421
- http://hdl.handle.net/10379/15276
- https://trepo.tuni.fi/handle/10024/129009
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Arzt=3ASteven=3A=3A.html
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-65869
- http://hdl.handle.net/2440/109378
- http://hdl.handle.net/2152/71508
- https://figshare.com/articles/_Performance_comparison_among_various_types_of_sequence_features_and_methods_for_the_across_germline_prediction_using_10_fold_cross_validation_/183488
- http://scholarbank.nus.edu.sg/handle/10635/41016
- https://zenodo.org/record/7244986
- https://publications.rwth-aachen.de/search?p=id:%22RWTH-2017-04256%22
- https://zenodo.org/record/1217552
- http://dx.doi.org/10.26153/tsw/42134
- http://tel.archives-ouvertes.fr/docs/00/74/47/68/ANNEX/texfiles/ESANN2011_Poster/poster.pdf
- https://zenodo.org/record/7153109
- http://upcommons.upc.edu/e-prints/bitstream/2117/25882/1/Cristal.pdf
- https://arodes.hes-so.ch/record/8071/files/published%20version.pdf
- https://zenodo.org/record/7113252
- https://espace.library.uq.edu.au/view/UQ:51096b6
- http://publica.fraunhofer.de/documents/N-330349.html
- https://zenodo.org/record/1064234
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Mitschke=3ARalf=3A=3A.html
- http://etd.lib.metu.edu.tr/upload/3/12610279/index.pdf
- https://oa.upm.es/68446/
- http://hdl.handle.net/1721.1/6501
- https://zenodo.org/record/4694370
- http://hdl.handle.net/11585/870466
- http://hdl.handle.net/2117/25882
- https://zenodo.org/record/7559277
- https://joiv.org/index.php/joiv/article/view/1259
- https://figshare.com/articles/_Performance_comparison_of_many_metrics_including_CSR_MML_CH_SI_for_all_algorithms_in_Leukemia_dataset_/991102
- https://ph.pollub.pl/index.php/jcsi/article/view/2097
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1045.1928
- http://hdl.handle.net/2142/42340
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877705812003372/MAIN/application/pdf/12f5a1730d8eeda2f7d85cca494d8864/main.pdf
- http://cucis.ece.northwestern.edu/projects/DMS/publications/NarHon07A.pdf
- http://publica.fraunhofer.de/documents/N-330356.html
- https://zenodo.org/record/7988142
- http://www.cs.toronto.edu/%7Efbacchus/csc2512/Lectures/2012Readings/Skallah_Empirical_Study_SAT_Solvers.pdf
- https://hal.archives-ouvertes.fr/hal-00502751
- https://rhul.elsevierpure.com/en/publications/29a00205-25da-49c6-bcdf-8984ddf82bc9
- https://docs.lib.purdue.edu/surf/2018/Presentations/14
- http://www.lrec-conf.org/proceedings/lrec2008/pdf/907_paper.pdf
- http://hdl.handle.net/11346/BIBLIO@id=8321152982565999288
- http://cds.cern.ch/record/2137560
- https://zenodo.org/record/7110999
- https://zenodo.org/record/5090818
- http://summit.sfu.ca/item/16679
- http://jauu.net/var/print-queue/integrated-network-interfaces-for-high-bandwidth-tcp-ip.pdf
- https://doaj.org/article/004b4074f4ed4b4abe66e3589ee6b971
- http://hdl.handle.net/2134/14711
- https://doi.org/10.1007/978-3-030-65474-0
- http://hdl.handle.net/11311/1214622
- http://monarch.qucosa.de/api/qucosa%3A17446/attachment/ATT-2/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.8310
- http://www.o3bnetworks.com/wp-content/uploads/2015/02/COMTECH-CDM-625-EN-US-Lettre-Print-Ready.pdf
- https://doaj.org/article/1fce6aee022a457a8f668ea5050d0157
- https://zenodo.org/record/806916
- http://scholarbank.nus.edu.sg/handle/10635/38960
- http://publica.fraunhofer.de/documents/N-520355.html
- https://hdl.handle.net/1721.1/134045
- http://www.mysmu.edu/faculty/davidlo/papers/ase14-localization.pdf
- https://figshare.com/articles/_Performance_of_compared_methods_on_two_evaluation_metrics_/1167013
- http://digital.library.unt.edu/ark:/67531/metadc740533/
- https://depositonce.tu-berlin.de/handle/11303/13881
- www.duo.uio.no:10852/87966
- http://gray.cs.ua.edu/pubs/ferosh-jacob-thesis-2013.pdf
- http://www.nusl.cz/ntk/nusl-220742
- http://commons.lib.niu.edu/handle/10843/14932
- http://hdl.handle.net/1721.1/30433
- http://eprints.utm.my/id/eprint/61835/
- https://hal.inria.fr/hal-00869652
- http://eprint.iacr.org/2014/254.pdf
- https://zenodo.org/record/3369483
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.1901
- https://zenodo.org/record/6820681
- https://inria.hal.science/hal-01655456
- https://zenodo.org/record/819449
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.6703
- http://cds.cern.ch/record/1709601
- https://commons.erau.edu/adfsl/2015/tuesday/6
- https://figshare.com/articles/_The_decision_tree_for_the_classification_of_bedtime_rest_and_activity_accelerometer_recordings_/997186
- https://zenodo.org/record/4701708
- https://zenodo.org/record/4315393
- http://hdl.handle.net/2142/91549
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-187108
- http://bib-pubdb1.desy.de//record/291332/files/16.pdf
- http://publica.fraunhofer.de/documents/N-264055.html
- http://publica.fraunhofer.de/documents/N-382693.html
- https://zenodo.org/record/7245111
- http://iopscience.iop.org/1748-0221/10/04/C04011/pdf/1748-0221_10_04_C04011.pdf
- https://repository.vu.lt/VU:ELABAETD23254963&prefLang=en_US
- http://hdl.handle.net/11392/2341252
- http://www.disp.duke.edu/%7Enikos/reprints/C-024-GPU-FFT-HPEC07.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.90.8252
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-177136
- https://juser.fz-juelich.de/record/838390
- https://hal.science/hal-00549145/document
- https://hal.science/hal-01257303/document
- http://www.nusl.cz/ntk/nusl-235581
- http://www.nusl.cz/ntk/nusl-72087
- https://biblio.ugent.be/publication/1339511/file/1339558
- http://dx.doi.org/10.1016/j.vlsi.2013.09.001
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.88.1803
- http://www.mecs-press.org/ijitcs/ijitcs-v6-n9/IJITCS-V6-N9-4.pdf
- http://lup.lub.lu.se/student-papers/record/8978722
- https://doaj.org/article/70ce101b0d3f419db49bfe896bf2239e
- http://hdl.handle.net/10945/4601
- http://hdl.handle.net/11588/575030
- https://zenodo.org/record/3956281
- http://charm.cs.illinois.edu/newPapers/09-06/paper.pdf
- http://arxiv.org/pdf/1210.4400.pdf
- http://cds.cern.ch/record/1629759
- https://gdr-secu-jn2022.sciencesconf.org/
- https://doi.org/10.1109/NetSoft54395.2022.9844090
- http://resolver.tudelft.nl/uuid:fd77a839-c33d-4ec4-a700-59fc4c6a6ce7
- http://hdl.handle.net/1807/67970
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.88.9625
- http://resolver.tudelft.nl/uuid:3ca2419f-660f-4ea1-9e37-1fed1203364a
- http://www.nusl.cz/ntk/nusl-340863
- https://doaj.org/article/df42e6a6375b49aba37e8ca5c068e42d
- http://hdl.handle.net/11585/38452
- http://www.nusl.cz/ntk/nusl-385960
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Secure-computing-with-the-MPEG-RVC/99512706202346
- http://publica.fraunhofer.de/documents/N-418172.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.650.8883
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA445190%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://pqdtopen.proquest.com/#viewpdf?dispub=1516795
- http://www.massey.ac.nz/~dpplayne/Papers/cstn-125.pdf
- https://lirias.kuleuven.be/bitstream/123456789/436316/1/EDA_crypto_TFP2012.pdf
- https://ph.pollub.pl/index.php/jcsi/article/view/2595
- https://figshare.com/articles/Cepstral_based_i-vector_reference_system_i-vector_based_on_MFCC-SDC_features_performance_average_EER_of_all_language_clusters_/5299336
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-447812
- http://www.mathematik.tu-dortmund.de/lsiii/cms/papers/Moeller2012.pdf
- https://zenodo.org/record/7153137
- https://escholarship.org/uc/item/7dj862k9
- http://hdl.handle.net/10.1371/journal.pone.0212833.g005
- http://commons.lib.niu.edu/handle/10843/14695
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-80404
- https://hal.inria.fr/inria-00422143
- http://cds.cern.ch/record/2293722
- http://parse.ele.tue.nl/system/attachments/40/original/hendriks2012.pdf
- https://zenodo.org/record/5838454
- http://dspace.mit.edu/bitstream/handle/1721.1/88083/MIT-CSAIL-TR-2014-014.pdf%3Bjsessionid%3DCAFBEBBDBC2DC29EA989E3AC9FB88DF7?sequence%3D1
- http://www.nusl.cz/ntk/nusl-511925
- http://www.st.ewi.tudelft.nl/~peterz/papers/AGZA_SAC08.pdf
- https://oatao.univ-toulouse.fr/29383/1/Aguilar_Melchor_29383.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-91351
- http://www.cs.utoronto.ca/~ahertel/WebPageFiles/Papers/Formalizing
- http://hdl.handle.net/1853/32479
- https://doaj.org/article/0412ff468dd948fa876c2b688797dafd
- https://zenodo.org/record/8124296
- http://hdl.handle.net/11588/428471
- https://orcid.org/0000-0001-7604-8252
- https://archive-ouverte.unige.ch/unige:3445
- https://doaj.org/toc/2100-014X
- https://zenodo.org/record/7559208
- http://resolver.tudelft.nl/uuid:50562fb5-f04c-472c-b935-c3928765f24d
- https://zenodo.org/record/6950729
- https://repository.vu.lt/VU:ELABAETD107116280&prefLang=en_US
- http://hdl.handle.net/2117/327883
- https://zenodo.org/record/7546044
- https://www.esaim-proc.org/10.1051/proc/201863152/pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.8561
- https://www.esaim-proc.org
- http://cs.sookmyung.ac.kr/~chang/lecture/popa/bacon.pdf
- http://hdl.handle.net/11577/2468996
- https://figshare.com/articles/_Prediction_performance_for_different_ratios_of_positive_to_negative_sets_based_on_binary_encoding_/294583
- https://inria.hal.science/hal-03131759
- https://zenodo.org/record/2582968
- https://zenodo.org/record/1217550
- https://eprints.lincoln.ac.uk/id/eprint/57087/1/DSD2023_paper_2376%20_final.pdf
- http://cccp.eecs.umich.edu/papers/samadi-taco14.pdf
- http://hdl.handle.net/11568/1067213
- https://silm-workshop.inria.fr/
- http://hdl.handle.net/10251/97658
- https://hdl.handle.net/10356/166197
- https://biblio.ugent.be/publication/7047860/file/8039284
- https://zenodo.org/record/7855363
- http://arxiv.org/abs/2207.09152
- https://zenodo.org/record/4632609
- https://zenodo.org/record/3627379
- https://www.ajol.info/index.php/jorind/article/view/92596
- http://publica.fraunhofer.de/documents/N-219620.html
- http://www.nusl.cz/ntk/nusl-227352
- http://hdl.handle.net/10.6084/m9.figshare.7430282.v1
- https://hal.science/hal-01740903
- http://hdl.handle.net/2078.1/268338
- https://zenodo.org/record/819448
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.7044
- https://zenodo.org/record/6856744
- http://www.nusl.cz/ntk/nusl-416279
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066109000681/MAIN/application/pdf/3b88faebf5d8df880f28d174ad0d44b3/main.pdf
- http://www.eecg.utoronto.ca/~gulak/papers/Feygin94.pdf
- https://hal.inria.fr/hal-01909325/file/CEMRACS.pdf
- https://zenodo.org/record/46094
- https://zenodo.org/record/4084275
- https://centaur.reading.ac.uk/105223/9/hess-26-2939-2022.pdf
- http://hdl.handle.net/11012/200945
- http://hdl.handle.net/11336/150230
- https://e-space.mmu.ac.uk/view/creators/=D6zer=3AEmre=3A=3A.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.3085
- http://hdl.handle.net/10.5281/zenodo.2582968
- https://research.tue.nl/en/publications/ec1f2f35-91af-47bb-9249-d9b64bf2327b
- https://epublications.marquette.edu/mscs_fac/366
- https://zenodo.org/record/49284
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.7859
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0743106690900387/MAIN/application/pdf/cc437d564339ed185f76602985fbaf22/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.6332
- https://avesis.deu.edu.tr/publication/details/f442bc47-fd2d-41b5-a357-c19c59e7cfda/oai
- https://collections.lib.utah.edu/ark:/87278/s6cg1rbq
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-197297
- https://zenodo.org/record/7974809
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S187705091300570X/MAIN/application/pdf/07cc0fe9bbe47567cb43f81240b70b8b/main.pdf
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/1998/date98/pdffiles/poster13.pdf
- http://hal.inria.fr/docs/00/71/73/32/PDF/Template-5.pdf
- https://digitalcommons.wpi.edu/mqp-all/6346
- https://figshare.com/articles/Criteria_for_the_comparison_of_SA-conf_and_other_software_dedicated_to_the_structural_variability_analysis_and_quantification_of_a_set_of_MTCs_/5322601
- https://zenodo.org/record/7559244
- http://hdl.handle.net/1807/29464
- http://hdl.handle.net/10068/49450
- https://tches.iacr.org/index.php/TCHES/article/view/8591
- https://zenodo.org/record/4904024
- http://hdl.handle.net/2429/69355
- http://hdl.handle.net/10261/134458