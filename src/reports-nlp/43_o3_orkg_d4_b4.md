# Context-Aware Code Generation
Enhancing Contextual Understanding in Large-Language-Model (LLM) Toolchains for Production-Grade Software Engineering

**Prepared: 2025-09-05**  
*(All numbered bracket references map to the complete list of empirical “learnings” supplied by the customer; no external sources have been added.)*

---

## 1  Executive Summary
Large-language models have crossed the threshold of *syntactic* code generation competence (≥80 % pass@1 on HumanEval), yet they still stumble whenever the relevant information spans long ranges, multiple artefacts or heterogeneous modalities. Three converging research streams—(i) *architectural* tricks for longer/structured memories, (ii) *retrieval-augmented* and *slice-based* context selection, and (iii) *IDE/CI tooling* that injects dynamic or static signals during decoding—jointly suggest a path to production-quality, context-aware code generation.

We synthesise the entire evidence base (≈90 primary findings) into:  
• a design space taxonomy;  
• quantitative expectations for cost/benefit trade-offs;  
• candidate benchmarks, datasets and metrics;  
• seven under-explored yet high-leverage research bets.

---

## 2  Problem Statement & Motivation
1. **Prompt forgetfulness dominates failure modes** in robot-code generation and other embodied domains [L23].  
2. **Coverage gaps remain extreme**: Codex ⇒ >80 % HumanEval *vs* <2 % EvoSuite SF110 [L13 & L15 & L17 & L27].  
3. **Line/branch coverage in industrial systems is expensive**: 29 % regression-time overhead for only 59 % line coverage on 2 MLoC C/C++ [L1].

Hence *contextual grounding* must improve **both** (a) *quality* (compile/run correctness, maintainability, absence of smells) and (b) *efficiency* (GPU-hours, test+debug overhead, CI latency).

---

## 3  Design-Space Taxonomy for Contextual Grounding

### 3.1  Where Can Context Come From?
A. **Static artefacts inside the repository**  
   • neighbouring files, imports, type annotations [L34]  
   • API-usage graphs (UP-Miner [L42], LFM-OUPD [L41])  
   • slice-based dependency cones (KATANA dual slicing [L19 & L31]).

B. **Runtime signals**  
   • coverage feedback (HumanEval vs EvoSuite gap)  
   • on-the-fly performance probes (vscode-infer-performance [L29]).

C. **External corpora / retrieval memory**  
   • code-search indexes (ReACC, Relevance Transformer, SPoC BLEU 50.3 [L38]).  
   • domain-specific datasets (MIREA Python exercises [L6]; cross-project SonarQube 224 k warnings [L4 & L16]).

D. **Human/team norms & meta-data**  
   • six-axis context taxonomy inside MLSmellHound [L9 & L30].  
   • mined implicit social norms in commits [L36].

### 3.2  How Is Context Injected?
• **Expanded context windows**  
  – Rotary (RoPE) stretching to 128 k via YaRN [L28];  
  – ALiBi, sinusoidal vs implicit encodings [L26 & L53].  
• **Hierarchical memory** (multi-timescale prior extends LSTM horizon [L8 & L12]).  
• **Retrieval-Augmented Generation (RAG)** (ReACC, Monitor Guided Decoding [L38 & L35]).  
• **Dedicated modules**—Context Management Unit (CMU) in CoMArch [L6].  
• **Program-slice selection** for repair and by extension generation (KATANA dual slice [L19 & L31]).  
• **Parameter-Efficient Fine-Tuning (PEFT)** instead of giant prompts (LoRA success on code-*understanding* but lag on code-*generation* [L15] ⇒ open question).  
• **External monitors in-the-loop** (MGD static-analysis-guided decoding beats text-davinci-003 with 1.1 B params [L35]).

---

## 4  Architectural Advances Enabling Longer, Richer Context
1. **Linear-time attention** (Performers FAVOR + [L22]) now scales to >100 k tokens on commodity GPUs—complementary to RoPE stretching.  
2. **Implicit position encodings** (causal Transformer without PE loses only 8 % [L26]), hinting at *context capacity being bottlenecked by retrieval, not positional math.*  
3. **Multi-stage Transformers for latency-critical code search** cut inference to 5 % of BERT while +0.17 Recall@1 [L40].  
4. **CMU + Meta-Policy layer** (CoMArch) treats context filtering as *first-class*, allowing plug-in slices, retrieval, docs, telemetry [L6].

*Take-away*: combine FAST attention *inside* the LM with SMART retrieval *outside* the LM.

---

## 5  Tooling & Workflow Integrations
• **IDE side-cars**  
  – MLSmellHound: per-file lint rewriting using six-axis context [L9 & L30].  
  – vscode-infer-performance: inline complexity feedback [L29].  
• **CI/CD pipelines**  
  – EvoSuite incremental search (96 % faster, +13.9 % coverage) [L48].  
  – Kiskadee: ML-ranked static warnings reduce false positives 5.2× [L10 & L24 & L32].
• **TDD loops**  
  – LLM4TDD dataset supports incremental code-gen/test iteration [L46].
• **Model ↔ repository feedback**  
  – Monitor-Guided Decoding (MGD) channels static checks into token selection [L35].

---

## 6  Datasets & Benchmarks for Evaluation

| Purpose | Candidate sets | Notes |
|---------|----------------|-------|
| **Algorithmic snippets** | HumanEval, CodeXGLUE | Saturated (>80 %); poor discriminant validity. |
| **API-rich OO code** | EvoSuite SF110, PragmaticCode | Reveals 78-point coverage gap [L13]. |
| **Bug-proneness prediction** | Apache HTTP, LaTeX2RTF slice-metric corpus [L11 & L47] | For measuring context-based risk ranking. |
| **Static-warning triage** | SonarQube 224 k warnings [L4] | 91 % accuracy ceiling with embeddings only—good baseline. |
| **Repair** | Codeflaws 3 902 real defects [L43]; KATANA dual-slice dataset | Use to assess context windows vs slice selection. |
| **Cross-task generalisation** | CrossCodeBench [L52] | Stress-test representation re-use. |
| **Education / small functions** | MIREA dataset, TaskTracker | Evaluate pedagogy-oriented generation. |
| **Embedded / IoT** | DSML4DT (DeviceTree) [L20 & L21 & L48] | Targets constrained hardware descriptions. |

We recommend reporting **pass@k, compile-rate, statement+branch coverage, bug-fix rate, false-positive reduction** and **developer SUS/USE scores**. *Per-dataset* maturity varies: e.g., MIREA is un-labelled for pass@k; DSML4DT logs developer time so can test productivity.

---

## 7  Cost–Benefit & Performance Considerations
• **Instrumentation overhead**: 29 % build-&-test time hit for coverage tracing on 2 MLOC [L1].  
• **LoRA/Adapter fine-tuning**: 50× cheaper vs full FT on multilingual tasks, but shows mixed results on code generation [L15 & L18].  
• **Linear attention** halves GPU memory ≥100 k tokens [L22]; YaRN shrinks training tokens 10× [L28].  
• **Context management as retrieval** → inference latency *drops* (multi-stage Transformer 20× faster than monolithic) [L40].

---

## 8  Lessons from Adjacent Domains (Contrarian Signals)
1. **Networked embedded systems**: Dual slicing parallels dual-program-slice energy savings in LoRa (ReDCoS: 38 % energy saved) [L60]—*selective context beats brute force*.
2. **Machine Translation**: Multilingual adapters & typological vectors (MAD-G [L18]) show that *parameterised context* generalises to unseen languages; analogous to unseen project codebases.
3. **Statistical physics of attention**: PAPA shows many attention weights are unused [L29]; focusing optimisation on *token-to-token interaction relevance* (ALTI [L39]) is likely more effective than ever-larger context windows.
4. **Refactoring economics**: ML-specific debt categories [L61] suggest LLMs need context of *lifecycle stage* to avoid generating brittle ML pipelines.

---

## 9  Proposed Target Configuration (answers to the three outstanding product-scoping questions)
Q1  **Languages/domains.**  
• Primary: **Python 3.11** (data science, scripting) & **Java 17** (enterprise back-end, Android) because we have *complementary* benchmarks (HumanEval, EvoSuite, PragmaticCode, SonarQube) and contrasting object-orientation gaps.  
• Secondary: **DeviceTree DSL** for embedded, leveraging DSML4DT to measure productivity.  
• Frameworks: Django, Spring Boot, LoRa Mac drivers, ROS2 robotics.

Q2  **Focus areas.**  
(a) *60 % Architectural*: Retrieval-augmented decoders, CMU, YaRN-expanded windows, Performer attention.  
(b) *40 % Tooling*: VSCode+MGD plug-in, MLSmellHound adaptive lints, Kiskadee warning ranking.

Q3  **Success metrics.**  
1. **pass@k (k≤10) & compile-rate** on HumanEval + EvoSuite.  
2. **Fixed-bug@k** on Codeflaws & Defects4J.  
3. **delta-coverage / delta-false-positive** in CI (instrumentation overhead recorded).  
4. **Developer SUS & NASA-TLX** via DSML4DT-style surveys.  
5. **Energy-per-solution** on embedded targets (LoRa/DeviceTree).

---

## 10  Seven High-Leverage Research Bets
1. **Context Slicing for Generation** —generalise KATANA’s dual slices from repair to *forward* code generation; evaluate vs sliding windows.
2. **Monitor-Guided Decoding at Scale** —extend MGD beyond type checks to SonarQube rule set (160 rules [L4]).
3. **Adaptive Context Taxonomy** —plug MLSmellHound’s six axes directly into CMU selection heuristics.
4. **Linear-Attention RAG Hybrid** —combine Performer inner loop with multi-stage retrieval outer loop; hypothesise ≥2× speedup, no accuracy loss. *(Speculative)*
5. **Energy-Aware Decoding** —borrow LoRa BER/energy models [L56] to include *energy per token* constraint in beam-search scoring—critical for on-board generation in drones/IoT. *(Speculative)*
6. **Slice-Ranked Static Warnings to Drive Prompting** —use Kiskadee’s ranking to prioritise context lines fed into the prompt, reducing token budget.
7. **Cross-Task Adapter Fusion** —train LoRA layers jointly on generation + warning triage so that the same Δ-weights serve both compile-time & run-time tasks.

---

## 11  Implementation Roadmap (12 Months)
| Quarter | Milestones |
|---------|------------|
| Q1 | Baselining: fine-tune open-source 7B model with YaRN 64 k; ingest ReACC retrieval index; port HumanEval+EvoSuite harness. |
| Q2 | Build CMU prototype (static slices + retrieval); integrate MGD static monitors; run ablation on coverage/correctness. |
| Q3 | IDE plug-in: MLSmellHound + Kiskadee ranking + inline MGD; deploy to 3 pilot teams; collect SUS/TLX. |
| Q4 | Energy-aware decoding for embedded; cross-task LoRA fusion; final benchmark sweep; write SIGSOFT/EMNLP papers. |

---

## 12  Risk Register & Mitigations
• **Prompt token explosion** → use dual-slice + ranking; fallback to Performer + ALiBi.  
• **Adapter lag on generation** → investigate hybrid: LoRA for *under-standing* subsystems, full FT for decoder layers only.  
• **Coverage instrumentation overhead** → adopt selective probe toggling; cache executive summary of slices [L62].

---

## 13  Conclusion
Evidence from 30+ datasets and 40+ empirical studies indicates that *structured context management*—not just bigger models—drives the next quality leap in code generation. Marrying retrieval, program slicing, static/dynamic monitors and adaptive context taxonomies within an extensible CMU unlocks (i) higher correctness on complex OO tasks, (ii) lower cognitive load inside IDEs, and (iii) better cost/energy envelopes for CI and embedded targets. The proposed roadmap operationalises these insights and positions the project to publish competitive results within a year while simultaneously shipping developer-visible productivity gains.


## Sources

- http://hdl.handle.net/11268/7935
- https://hal.inria.fr/hal-01677142
- http://www.theseus.fi/handle/10024/509953
- http://hdl.handle.net/10344/3380
- https://zenodo.org/record/5228822
- http://arxiv.org/abs/2205.15544
- https://zenodo.org/record/8128447
- http://hdl.handle.net/10255/dryad.132750
- http://hdl.handle.net/11250/2479193
- http://hdl.handle.net/11568/1054222
- https://zenodo.org/record/5885654
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S016764231000078X/MAIN/application/pdf/c453cbdfd75c06eacd586719f0498dfd/main.pdf
- http://people.engr.ncsu.edu/sesmith5/publications/HW06_ISSRE.pdf
- https://zenodo.org/record/5704197
- http://www.seas.upenn.edu/%7Eepavlick/papers/language_demographics_mturk.pdf
- http://alexandria.tue.nl/repository/books/253159.pdf
- https://figshare.com/articles/Dataset_for_survey_of_industry-academia_collaboration_in_software_engineering_phase_1_/6491743
- https://zenodo.org/record/1251317
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Pfeiffer=3AJonas=3A=3A.html
- http://hdl.handle.net/20.500.11897/262476
- https://figshare.com/articles/Data_and_code/6070283
- https://zenodo.org/record/836858
- https://dare.uva.nl/personal/pure/en/publications/english-intermediatetask-training-improves-zeroshot-crosslingual-transfer-too(bb96e7f6-05a6-4b17-839c-37d3674246a0).html
- https://escholarship.org/uc/item/47x1t79s
- https://zenodo.org/record/5993801
- http://taoxie.cs.illinois.edu/publications/ase10-warning.pdf
- https://scholarworks.unist.ac.kr/handle/201301/35329
- http://hdl.handle.net/1843/JCES-AREGGR
- https://aisel.aisnet.org/cgi/viewcontent.cgi?article=1003&amp;context=confirm2010
- https://zenodo.org/record/3547639
- https://zenodo.org/record/8191801
- https://spectrum.library.concordia.ca/id/eprint/8951/
- http://hdl.handle.net/2117/347326
- https://hal.inria.fr/hal-00746814
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.7752
- https://figshare.com/articles/code_zip/5925178
- https://ojs.aaai.org/index.php/AAAI/article/view/6480
- https://research.vu.nl/en/publications/f7a1f567-96d8-4889-a032-18245a5e9a8d
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-424272
- https://hal.archives-ouvertes.fr/hal-00619863/file/hal.pdf
- http://journal.ub.tu-berlin.de/eceasst/article/download/396/367/
- http://dx.doi.org/10.1109/MC.2022.3160276
- https://hal.archives-ouvertes.fr/hal-02538535/document
- http://hdl.handle.net/11585/781553
- https://zenodo.org/record/3708904
- https://ids-pub.bsz-bw.de/frontdoor/index/index/docId/8001
- http://hdl.handle.net/10.1371/journal.pone.0256152.t001
- http://hdl.handle.net/11588/819287
- https://digitalcommons.unl.edu/dissertations/AAI3450111
- http://www.stringology.org/cgi-bin/getfile.cgi?c%3D-%26n%3D10%26t%3Dpdf%26y%3D2010
- http://arxiv.org/abs/2205.10504
- www.myjurnal.my/filebank/published_article/65205JTEC_24.pdf
- http://resolver.tudelft.nl/uuid:02720548-effa-4707-af99-718667c91ae3
- https://ojs.aaai.org/index.php/AAAI/article/view/21587
- http://web.engr.oregonstate.edu/~alex/icse14.pdf
- http://hdl.handle.net/11386/4716472
- https://www.zora.uzh.ch/id/eprint/111051/
- https://figshare.com/articles/_CPU_seconds_versus_reduced_dimensionalities_on_four_datasets_/882942
- http://dyuthi.cusat.ac.in/purl/3889
- http://tubiblio.ulb.tu-darmstadt.de/133999/
- http://www.nusl.cz/ntk/nusl-415948
- http://repository.tue.nl/662907
- http://repositorio.unicamp.br/jspui/handle/REPOSIP/91996
- http://resolver.tudelft.nl/uuid:7b1ae1e0-d598-479b-adb1-8dfd545f7c2d
- http://www.cise.ufl.edu/%7Esahni/papers/p.pdf
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Murphy-Hill=3AEmerson=3A=3A.html
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-14904
- http://hdl.handle.net/10.1371/journal.pone.0216922.g001
- https://zenodo.org/record/8050982
- https://madoc.bib.uni-mannheim.de/60102/
- http://datacite.org/schema/kernel-4
- http://hdl.handle.net/10.6084/m9.figshare.23821830.v2
- http://hdl.handle.net/2429/66724
- https://zenodo.org/record/8274618
- http://hdl.handle.net/2117/79981
- http://publica.fraunhofer.de/documents/N-520355.html
- https://zenodo.org/record/7118615
- https://zenodo.org/record/7614189
- http://hdl.handle.net/10.1371/journal.pone.0291946.t005
- https://zenodo.org/record/7998099
- http://subs.emis.de/LNI/Proceedings/Proceedings215/571.pdf
- http://hdl.handle.net/11582/331001
- https://zenodo.org/record/3841257
- https://hal.univ-grenoble-alpes.fr/hal-02933799
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27721
- http://dx.doi.org/10.1002/smr.1841
- http://arxiv.org/abs/2205.03286
- http://people.engr.ncsu.edu/sesmith5/publications/HW08_ESEM.pdf
- http://hdl.handle.net/11336/59494
- https://zenodo.org/record/7861337
- https://hal.inria.fr/hal-01875492
- https://www.open-access.bcu.ac.uk/16136/
- https://spectrum.library.concordia.ca/id/eprint/7853/
- https://zenodo.org/record/7857872
- https://zenodo.org/record/7875623
- https://zenodo.org/record/7321934
- https://figshare.com/articles/_Standard_deviation_of_the_estimated_latency_produced_by_the_different_methods_/1439001
- http://hdl.handle.net/10.1371/journal.pone.0292582.g002
- https://oa.upm.es/70462/
- https://zenodo.org/record/841984
- https://zenodo.org/record/3559986
- https://docs.lib.purdue.edu/dissertations/AAI10608065
- http://scholarbank.nus.edu.sg/handle/10635/39029
- https://figshare.com/articles/Dataset_for_Industry-academia_collaboration_in_software_engineering_an_analysis_of_multiple_research_projects/4509092
- https://figshare.com/articles/_Sequencing_success_sequence_quality_and_barcode_recovery_of_six_regions_/1276722
- http://arxiv.org/abs/2202.10447
- http://dx.doi.org/10.26153/tsw/43665
- https://lirias.kuleuven.be/handle/123456789/627430
- https://figshare.com/articles/_Top_negation_context_features_in_a_multi_corpus_model_by_chi_square_value_and_feature_rank_in_domain_specific_models_/1239309
- https://hal.archives-ouvertes.fr/hal-01851813
- https://hal-univ-rennes1.archives-ouvertes.fr/hal-01904637
- http://dl.acm.org/citation.cfm?doid=2043910.2043916
- https://figshare.com/articles/Footprint_of_data_structures_as_function_of_number_of_points_/5604103
- https://research.utwente.nl/en/publications/conceptual-language-models-for-contextaware-text-retrieval(97c1e906-111c-4624-8ea3-9002b6d3d351).html
- http://arxiv.org/abs/2205.12654
- http://arxiv.org/abs/2211.03495
- http://sei.pku.edu.cn/%7Ezhanglu/Download/ICSME14-301.pdf
- https://figshare.com/articles/_Results_for_development_time_/317338
- http://hdl.handle.net/10012/18197
- https://zenodo.org/record/7875338
- https://orbilu.uni.lu/handle/10993/21458
- https://zenodo.org/record/7875395
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-162013
- https://research.hanze.nl/nl/activities/b2900f8d-c8c3-4bb1-99a8-9bccb104f4c4
- https://doi.org/10.1109/RE59067.2024.00022
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-279489
- http://arxiv.org/abs/2203.02094
- http://resolver.tudelft.nl/uuid:5c5a84ea-9729-4893-99fa-1d5116c136dd
- https://zenodo.org/record/4296613
- http://hdl.handle.net/10523/2101
- http://hdl.handle.net/2429/83363
- https://hal.archives-ouvertes.fr/hal-01822151
- https://scholarworks.umass.edu/cgi/viewcontent.cgi?article=3693&amp;context=dissertations_2
- http://resolver.tudelft.nl/uuid:b70d083a-7557-4d8e-9828-b9a7408c72dc
- https://orbilu.uni.lu/handle/10993/21460
- https://zenodo.org/record/7646968
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.5133
- http://pat.keldysh.ru/~roman/doc/Romanenko%2CSestoft-1998-April--Moscow.ML.owner%27s.manual%2C.version.1.43.pdf
- https://hal.science/hal-04311790/file/Evaluating_self_attention_interpretability_through_human_grounded_experimental_protocol___Springer_xAI.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/6795
- http://hdl.handle.net/20.500.11897/423975
- https://doi.org/10.11606/D.45.2018.tde-20082018-170140
- https://figshare.com/articles/DS1_Relative_cell_counts_and_normalized_growth_rate_inhibition_values_across_technical_replicates/6032324
- https://ojs.aaai.org/index.php/AAAI/article/view/5341
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-41105
- http://ict-2018.org/
- http://arxiv.org/abs/2309.00071
- https://zenodo.org/record/8153849
- https://doi.org/10.1007/978-3-319-41540-6_21
- https://escholarship.org/uc/item/6d62c22g
- http://www.scopus.com/record/display.url?eid=2-s2.0-67650480233&origin=inward
- http://hdl.handle.net/10388/8530
- https://figshare.com/articles/_Standard_deviation_of_the_estimated_response_duration_produced_by_the_different_methods_/1439002
- http://hdl.handle.net/10.6084/m9.figshare.24768660.v1
- http://hdl.handle.net/10255/dryad.74487
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.1310
- https://hal.inria.fr/hal-01659137
- https://ro.uow.edu.au/eispapers/5024
- https://hal.science/hal-03519372/file/Theoretical_Performance_of_LoRa_System_in_Multi_Path_and_Interference_Channels.pdf
- https://zenodo.org/record/2532867
- https://hal.archives-ouvertes.fr/hal-00680688
- https://zenodo.org/record/3973301
- https://doi.org/10.1109/AICCSA.2018.8612819
- http://arxiv.org/abs/2212.05901
- http://hdl.handle.net/10.6084/m9.figshare.22149854.v1
- http://arxiv.org/abs/2306.10763
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.470
- https://figshare.com/articles/P4ML_Evaluation_Results_Apr2018/6319844
- https://zenodo.org/record/7559208
- http://etd.iisc.ernet.in/abstracts/4765/G21067-Abs.pdf
- https://zenodo.org/record/8267719
- https://doaj.org/article/bbcf3cdf0c6f4e2db61568aab23f4034
- https://hal.archives-ouvertes.fr/hal-03545897
- https://figshare.com/articles/_Performance_of_DNA_barcodes_in_sequence_recovery_and_species_identification_success_/1184766
- http://www.elsnet.org/mt2010/probst.pdf
- https://zenodo.org/record/32434
- https://zenodo.org/record/7313115
- https://e-space.mmu.ac.uk/628837/
- http://rosaec.snu.ac.kr/publish/2009/T1/KiLeBaYiWu-APSEC-2009.pdf
- http://hdl.handle.net/10061/12733
- http://hdl.handle.net/2117/396576
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0890540107000399/MAIN/application/pdf/3a30fa53726e7930ef776972deebc81e/main.pdf
- http://hdl.handle.net/2117/394210
- https://digitalcommons.pace.edu/dissertations/AAI3235024
- https://zenodo.org/record/7799972
- https://figshare.com/articles/The_evaluation_times_and_computation_time_on_70_DNME_models_for_three_algorithms_100SNP_markers_/3131047
- http://www.evosuite.org/wp-content/papercite-data/pdf/qsic11.pdf
- http://www.uow.edu.au/%7Ehoa/papers/icse-nier-preprint.pdf
- https://figshare.com/articles/_Mobile_phone_data_and_causality_trees_/367642
- http://arxiv.org/abs/1906.08584
- https://hdl.handle.net/10371/185665
- http://hdl.handle.net/10.36227/techrxiv.21960170.v2
- http://arxiv.org/abs/2203.04212
- https://academicworks.cuny.edu/context/hc_pubs/article/1865/filename/1/type/additional/viewcontent/refactoring_categories.csv
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.3784
- http://hdl.handle.net/10138/327849
- http://hdl.handle.net/10138/327794
- http://arxiv.org/abs/2201.03327
- https://corescholar.libraries.wright.edu/knoesis/700
- http://hdl.handle.net/1773/48053
- http://www.mirlab.org/conference_papers/International_Conference/ICSLP
- https://digitalcommons.unl.edu/cseconfwork/128
- https://figshare.com/articles/Evaluation_results_on_the_development_portion_of_the_Protein_Coreference_Dataset_/3094516
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-142408
- https://research.chalmers.se/en/publication/501018
- https://escholarship.org/uc/item/7gv0d5pv
- https://ojs.aaai.org/index.php/AAAI/article/view/17512
- https://research.rug.nl/en/publications/06a9e7bf-8f53-4881-9e1c-c6307a9be16a
- https://zenodo.org/record/7553738
- https://doaj.org/toc/1530-8677
- http://www.sciencedirect.com/science/article/pii/S0045790616301744
- http://hdl.handle.net/10255/dryad.147846
- http://arxiv.org/abs/2203.16634
- http://resolver.tudelft.nl/uuid:60ac83aa-bd59-412a-a3d5-e7aed16eb65a
- http://resolver.tudelft.nl/uuid:7dca4164-d299-46a4-8ffe-7ab6057ed4d5
- https://resolver.obvsg.at/urn:nbn:at:at-ubk:1-21988
- http://u.cs.biu.ac.il/%7Etomi/Postscripts/damfixed1.pdf
- http://arxiv.org/pdf/1101.4101.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-3358
- http://www.loc.gov/mods/v3
- http://hdl.handle.net/10679/2253
- https://doaj.org/article/f0f5c2fb8279451cb4488f7178c10dde
- https://digitalcommons.kean.edu/keanpublications/468
- https://arrow.tudublin.ie/scschcomart/99
- https://zenodo.org/record/7559244
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.8183
- https://eprints.whiterose.ac.uk/86827/1/art%253A10.1007%252Fs10664-013-9299-z.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-131815
- https://ojs.aaai.org/index.php/AAAI/article/view/21330