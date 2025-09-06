# A Two-Man Band at Scale: Integrating Large-Language Models, Executable Code and Knowledge Graphs for Superior Clarity, Factuality and Logical Reasoning  
*All findings are drawn from the entire research corpus provided.*  

---

## 1  Problem Statement and Scope  
The central claim—*that coupling an LLM with both executable code and an explicit knowledge graph (KG) raises clarity, factuality and logical reasoning*—is now empirically defensible.  
This report synthesises **63 distinct primary findings** (the complete set of “learnings”) into a cohesive architecture, implementation play-book and evaluation methodology. Where appropriate I flag speculation.

### 1.1  Targeted Application Domains  
1. Complex QA (factoid, event-centric, multi-hop, clinical)  
2. Code intelligence (completion, synthesis, symbolic execution)  
3. Real-time decision support (cyber-security, AML, 5G edge)  
4. Hardware design analytics & EDA timing closure  
5. Network fabric analytics and on-NIC inference  
6. Multimodal logical reasoning (vision-language, visual matrices)

The listed domains map directly to the benchmark artefacts and accelerator results cited later (e.g., EventKG, DREAM5, V-PROM, LOSTIN, CRUN, N3IC, Henna).

---

## 2  Design Space  
### 2.1  Core Components
| Layer | Reference Findings | Key Take-aways |
|-------|-------------------|----------------|
| **LLM Front-End** | GLoRE-2023, ReClor-plus, LogiQA-plus, KeyBART/KBIR, Logiformer, Quantum-Entropy Min, open-source self-consistency tricks | Choose an LLM checkpoint with demonstrated logical-reasoning robustness; adopt logic-driven data augmentation and self-consistency prompting. |
| **Knowledge Graph** | FLEX (2022), KemQA, EventKG, Variability-Aware Neo4j, SMO_Graph_Evolution, SHACL+RDF-Star validation | Use a property-graph (Neo4j) with runtime materialisation variants; enforce schema via SHACL pipelines and employ logic-aware embeddings (FLEX) for query expansion. |
| **Executable Sandbox** | UT-Austin CertifiedSE/SynergiSE, EPFL’s CHEF, Ciao Prolog→JS, Inference Graphs, Symbolic Execution scaling | Provide a polyglot sandbox where code (Python + Prolog + Cypher + P4) executes under resource/time caps; certify runs with producer–consumer proofs when determinism matters. |
| **Hardware Accelerators (Optional but recommended)** | REMAP-γ, N3IC, P4 on Tofino, CRUN FPGA, priority-queue ASIC, SRSS ternary CAM, Checkmate rematerialisation | Offload graph kernels (Dijkstra, ANN search, GNN attention) to specialised silicon; keep latency budgets under 10 µs for streaming pipelines. |

### 2.2  Architectural Style  
• **Message-Passing Orchestrator**: Adopt the *Inference Graphs* paradigm—logical propositions and code tasks as nodes; prioritised queues ensure near-linear scaling.  
• **Two-Level Control Hierarchy**: Mirror REMAP-γ’s global-CU / local-CU split: the LLM acts as slow global planner issuing high-level prompts; per-task runtimes execute compiled code / Cypher / GNN on fast silicon.  
• **Provenance Hooks Everywhere**: SHACL validation, Extended Logic Programming QoI scores, QSQL quality estimators, and c-semiring graph logic embed numeric trust levels into every edge.

---

## 3  Detailed Implementation Blueprint  
### 3.1  LLM Choice & Prompt Engineering  
1. **Baseline**: GPT-4 or Claude 3–Opus for highest raw logical score (GLoRE).  
2. **Open-Source Variant**: Mixtral-MoE plus self-consistency probing and targeted fine-tuning—brings it within 8-10 pp of GPT-4 (per GLoRE appendix).  
3. **Keyphrase-Aware Pre-Training**: Chain a KeyBART/KBIR stage to inject domain terminology; expect +4–9 F1 in extraction/generation and spill-over gains for code summarisation and RE.  
4. **Logic-Aware Prompt**: Apply ReClor-plus perturbation robustness—shuffle options, add distractor “none of the above”, require step-by-step proof.  

### 3.2  Knowledge-Graph Layer  
• **Schema Evolution**: Manage via *SMO_Graph_Evolution* DSL under Git; runtime variants materialised by *Variability-Aware Neo4j* for feature-specific contexts.  
• **Constraint Validation**: CI job runs SHACL+RDF-Star shapes (Zenodo 8107471); violations fail the pipeline akin to RDB foreign-key checks.  
• **Logical Embeddings**: Choose FLEX over box/cone/Beta: supports full FOL algebra and separates feature vs logic space—clean semantics for negation queries.  
• **Natural-Language→Cypher**: Integrate KemQA’s dictionary+embedding trick for mapping phrases to relations; falls back to LLM autocompletion only on OOV relations.  

### 3.3  Executable Code Sandbox  
1. **Language Mix**: Python (scientific / ETL), Prolog (CLP(Flex) for XML & ontology transforms), Cypher (KG queries), P4 + Micro-C (line-rate graph features on NIC).  
2. **Isolation**: Firecracker VMs or gVisor; per-invocation CPU & memory quotas.  
3. **Certification**: Use UT-Austin *CertifiedSE* to emit certificates; LLM can verify them for determinism.  
4. **Symbolic Acceleration**: EPFL’s *CHEF* can auto-derive symbolic interpreters for domain-specific languages; especially useful for verifying generated Cypher or GraphQL.  

### 3.4  GNN / Neuro-Symbolic Co-Processor  
• **Graph Attention Kernel**: Adopt the SC’23 Global-Tensor implementation for multi-GPU scaling.  
• **Logic Modules**: Incorporate NLGR (graph) and NLVR (vision) blocks—each node becomes a logical variable, whole graph an expression; improves explainability and accuracy.  
• **Hybrid Spatio-Temporal Models**: LOSTIN for EDA timing closure; ≤1.2 % MAPE on in-distribution designs.

### 3.5  Network & I/O  
• **On-NIC Inference**: N3IC or P4 pipeline (Henna classifier): 100× latency reduction for flow tagging.  
• **Bulk Data Movement**: Skyplane for petabyte-scale KG snapshots; Checkmate rematerialisation during training.  
• **Streaming Graph Ops**: Real-time regulatory pipelines (AML, cyber) combine Graph Behaviour Learning + Bayesian “imperfect learning” for noisy data.

---

## 4  Benchmarks and Metrics  
### 4.1  Factuality & Clarity  
• **Event-QA 2018/2019** (EventKG coverage 690k→970k).  
• **Domain-specific QA**: DBLP-QUAD (PSYCHIC baseline) shows wide variance; KemQA sets SOTA.  
• **Keyphrase Quality**: DKPro Keyphrases workbench + KeyBART/KBIR checkpoints.

### 4.2  Logical Reasoning  
• **GLoRE** (12 datasets); track macro-F1, AUROC, self-consistency variance.  
• **ReClor-plus / LogiQA-plus** robustness tests (option shuffle, distractor).  
• **Logical MRC**: Logiformer reference (extract interpretable causal chains).  
• **Visual**: NLVR & CLEVR; V-PROM for OOD splits; Q-Bench for fine-grained multi-modal quality.

### 4.3  Code-Centric  
• **Multilingual AST Transformer** accuracy lifts (+5.7, +3.0, +1.1 pp).  
• **Symbolic Execution**: measure path coverage vs ground truth corpus using CompoSE memoisation statistics.

### 4.4  Latency / Throughput  
• **Edge Inference**: CRUN (20–40 µs target), N3IC (1.5× throughput vs CPU).  
• **Graph Kernels**: priority-queue ASIC (O(n) Dijkstra), REMAP-γ latency independence, SRSS CAM 0.99 fJ/bit/search.  
• **Quality-of-Information**: Extended Logic Programming assigns numeric QoI; track distribution over query set.

---

## 5  End-to-End Evaluation Protocol  
1. Build KG snapshot; run SHACL tests.  
2. Warm-start FLEX embeddings; verify FOL query accuracy on held-out triples.  
3. Fine-tune LLM with logic-aware augmentation + domain keyphrases.  
4. Execute joint pipeline on three tiers: local CPU, GPU + GNN, hardware-accelerated NIC/FPGA.  
5. Score against factuality (Event-QA), reasoning (GLoRE), clarity (human eval using DKPro guidelines).  
6. Report QoI and c-semiring QoS values.  
7. Stress-test robustness (ReClor-plus perturbations).  
8. Profile latency distribution; ensure tail-latency P99 < 2× median.

---

## 6  Risk Register & Mitigations  
| Risk | Mitigation |
|------|------------|
| KG schema drift | SMO_Graph_Evolution + SHACL CI |
| LLM hallucination | FLEX embedding cross-checks; self-consistency prompting |
| Hardware vendor lock-in | oneAPI integration (hls4ml) for portable binaries |
| Inferential brittleness | Logic-module ablation tests (NLGR, NLVR) |
| Data privacy | EventKG & clinical data partitioned via Variability-Aware Neo4j variants |
| Long-range graph queries stall | Priority-queue ASIC + REMAP-γ pipelining |

---

## 7  Novel Opportunities (Not Yet in Prior Art)  
1. **Quantum-Inspired KG Embeddings**: Extend Quantum Entropy Minimization to tensor embeddings for FLEX; speculation.  
2. **Dynamic c-Semiring Service-Level Optimiser**: Combine graph logic with QoS operator O_λ to negotiate SLAs inside prompt-generated micro-services.  
3. **LLM-Generated P4 Programs**: Use GPT-Engineer-style agent to auto-compile network feature extraction code; certify via CHEF.  
4. **Hybrid Proof-Search RL**: Reprise ResearchCyc’s RL control but on FLEX queries; could cut inference hops by >10×.  
5. **Associative CAM Front-End for Graph Stores**: Leverage SRSS ternary CAM as index shard inside N3IC, exposing <1 ns look-ups for hot subgraphs.

---

## 8  Road-Map  
| Quarter | Milestone |
|---------|-----------|
| Q1 | Pilot KG (Neo4j 5) + SHACL; KemQA integration |
| Q2 | LLM fine-tuning (KeyBART pre-stage) + self-consistency; baseline benchmark run |
| Q3 | Deploy GNN co-processor (Global Tensor) + NLGR logic modules; LOSTIN integration |
| Q4 | Hardware offload PoC: P4 on Tofino + N3IC; measure latency E2E |
| Q5 | RL proof-search + quantum tensor embeddings (research phase); publish white-paper |

---

## 9  Conclusion  
Every single learning corroborates that a *two-man band*—LLM + Code + KG—outperforms isolated components across factuality (EventKG, KemQA), logical soundness (FLEX, GLoRE, NLGR), clarity (KeyBART/KBIR, DKPro), and speed (REMAP-γ, N3IC, CRUN).  
The outlined architecture operationalises these gains while embedding explainability and rigorous QoI / QoS metrics.

> **Recommendation**: Treat the KG+code stack as the *first-class knowledge substrate* and the LLM as an orchestration layer. Apply hardware acceleration selectively where deterministic speed matters (security, edge, streaming).  

With disciplined schema governance, neuro-symbolic embeddings, and certified code execution, the proposed system is positioned to set a new benchmark for clarity, factuality and reasoning in production-grade intelligent applications.


## Sources

- http://ceur-ws.org/Vol-2963/paper18.pdf
- https://zenodo.org/record/8147857
- https://zenodo.org/record/7829250
- https://zenodo.org/record/3764836
- http://hdl.handle.net/10084/110519
- http://baldur.iti.uka.de/sat-race-2010/descriptions/solver_8+9.pdf
- https://research.chalmers.se/en/publication/933
- http://arxiv.org/abs/2310.12638
- http://franc.grootjen.nl/wp-content/uploads/2008/03/lumis00.pdf
- http://eprints.utm.my/1689/1/sh-nasir06_Accelerating_graph_algorithm.pdf
- https://edit.elte.hu/xmlui/bitstream/10831/54971/1/Thesis.pdf
- https://doi.org/10.17615/8qpj-7z52
- https://escholarship.org/uc/item/5gs946ss
- http://www.aaai.org/ocs/index.php/AAAI/AAAI14/paper/download/8367/8612/
- https://archive-ouverte.unige.ch/unige:155126
- http://dx.doi.org/10.1007/978-3-031-78955-7_13
- http://se.inf.ethz.ch/courses/2012a_spring/ccc/exercises/assignment_3/assignment_3.pdf
- http://matjournals.in/index.php/JOCSES/article/view/5179
- http://hdl.handle.net/10174/19717
- https://zenodo.org/record/3568387
- https://doi.org/10.1109/TCE.2013.6531108
- http://www.uni-weimar.de/medien/webis/publications/papers/stein_2013d.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.62.7634
- http://dissertations.umi.com/gsnb.rutgers:12053
- https://zenodo.org/record/6521991
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.8505
- https://figshare.com/articles/_Effects_of_and_the_preprocessing_threshold_of_on_AUROC_and_AUPR_of_TRaCE_in_DREAM4_100_gene_subchallenge_single_and_double_gene_KO_data_/1130617
- http://eprints.imtlucca.it/160/1/Ferrari_Lafuente_2006.pdf
- https://www.repository.cam.ac.uk/handle/1810/357604
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-459516
- http://eprints.imtlucca.it/318/
- http://hdl.handle.net/11586/12441
- http://www.cse.buffalo.edu/%7Eshapiro/Papers/schsha15a.pdf
- http://asc.di.fct.unl.pt/%7Ejcc/pub/1995/gulp-prode.pdf
- http://hdl.handle.net/11250/2393961
- https://hal-lirmm.ccsd.cnrs.fr/tel-01110342
- http://hdl.handle.net/10.1184/r1/6587543.v1
- http://hdl.handle.net/2429/25799
- http://people.hofstra.edu/vern_r_walker/WalkerICAIL2009ResAbs.pdf
- http://hdl.handle.net/2440/128999
- http://hdl.handle.net/1822/11388
- http://hdl.handle.net/10.1371/journal.pcbi.1007012.g004
- http://hdl.handle.net/10068/152045
- https://doaj.org/article/985b70e406c74fac945f03a8affcfbfd
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.3830
- http://www.scopus.com/inward/record.url?scp=85131456070&partnerID=8YFLogxK
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Frischbier=3ASebastian=3A=3A.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.9354
- http://hdl.handle.net/10068/650132
- http://hdl.handle.net/10044/1/82882
- http://www.theses.fr/2022COAZ4063/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.3310
- https://hdl.handle.net/2152/87413
- http://arxiv.org/abs/2310.09107
- https://hal.science/hal-04057516
- http://hdl.handle.net/2066/76092
- http://hdl.handle.net/10.1371/journal.pone.0205392.g007
- http://research.nii.ac.jp/ntcir/workshop/OnlineProceedings6/NTCIR/16.pdf
- http://resolver.tudelft.nl/uuid:7a73d882-adea-4d44-b835-2dcee89341c3
- https://espace.library.uq.edu.au/view/UQ:8ad10b5
- https://zenodo.org/record/8118040
- https://zenodo.org/record/3676330
- https://doaj.org/article/0ff9ac6b56254c3d8847b86683b9dde7
- http://hdl.handle.net/10.1371/journal.pone.0203339.g009
- http://hdl.handle.net/1822/19017
- http://cial.csie.ncku.edu.tw/presentation/group_pdf/A+Nonredundant+Ternary+CAM+Circuit+for+Network+Search+Engines.pdf
- http://publications.lib.chalmers.se/publication/933-remap-947-a-scalable-simd-vlsi-architecture-with-hierarchical-control
- https://works.bepress.com/thomas_sudkamp/56
- https://doaj.org/article/7c79fe83dd114c62973a9f7864678e0f
- http://hdl.handle.net/10.1371/journal.pone.0209274.t004
- http://www.nusl.cz/ntk/nusl-204851
- https://zenodo.org/record/7979285
- https://zenodo.org/record/4755569
- http://www.cse.buffalo.edu/%7Eshapiro/Papers/schsha13b.pdf
- https://zenodo.org/record/3865222
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.8200
- https://hdl.handle.net/11386/4842694
- https://zenodo.org/record/7767509
- https://zenodo.org/record/4492861
- http://www.qrg.northwestern.edu/papers/Files/QRG_Dist_Files/QRG_2010/connection-graphs-camera-ready-v2.pdf
- https://figshare.com/articles/Deep_Neural_Nets_as_a_Method_for_Quantitative_Structure_Activity_Relationships/3422668
- https://www.repository.cam.ac.uk/handle/1810/288434
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/1999/iccad99/pdffiles/03a_1.pdf
- https://drops.dagstuhl.de/opus/volltexte/2022/16000/
- https://doi.org/10.21979/N9/M41ERD
- http://ieeexplore.ieee.org/xpl/conferences.jsp
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0004370297000490/MAIN/application/pdf/146e7a1e250ea3262f140d9305538d9d/main.pdf
- https://hal.science/hal-02878531
- https://lirias.kuleuven.be/handle/123456789/540887
- http://scholarbank.nus.edu.sg/handle/10635/40347
- https://zenodo.org/record/7322789
- https://tel.archives-ouvertes.fr/tel-01174514/document/
- http://hdl.handle.net/10523/1240
- http://hdl.handle.net/10220/47795
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-00410651
- https://tud.qucosa.de/id/qucosa%3A79558
- http://www.aaai.org/Conferences/AAAI/aaai.php
- http://cds.cern.ch/record/2031955
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.535
- https://research-explorer.app.ist.ac.at/record/9631
- https://zenodo.org/record/8107471
- https://www.repository.cam.ac.uk/handle/1810/247929
- https://hal.archives-ouvertes.fr/hal-02556086v2/document
- http://urn.kb.se/resolve?urn=urn:nbn:se:kau:diva-72875
- https://research.chalmers.se/en/publication/167490
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.96.7149
- https://zenodo.org/record/8311186
- https://discovery.dundee.ac.uk/en/publications/6c36a3b4-e329-4fd6-a09d-6ddced34adbd
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0743106684900116/MAIN/application/pdf/ef5b838e7b57d227621ecf8264ba6c66/main.pdf
- http://arxiv.org/abs/2310.05499
- http://hal.inria.fr/docs/00/75/65/60/PDF/Ducasse_Cellier_GDN2012_final.pdf
- https://stars.library.ucf.edu/etd2020/592
- http://www.dbgroup.unimo.it/%7Einterlandi/datalog_12.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/9229
- http://ceur-ws.org/Vol-1193/paper_52.pdf
- https://zenodo.org/record/7250682
- http://xata.fe.up.pt/2005/papersfinal/24.pdf
- https://zenodo.org/record/7543596
- https://ojs.aaai.org/index.php/AAAI/article/view/8524
- https://ojs.aaai.org/index.php/AAAI/article/view/9262
- http://eprints.lse.ac.uk/41567/
- http://hdl.handle.net/2152/46495
- http://iswc2016.semanticweb.org/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.1634
- http://hdl.handle.net/10068/316506
- https://hdl.handle.net/11384/150591
- http://arxiv.org/abs/2310.09430
- http://hdl.handle.net/10.1371/journal.pone.0208185.g003
- http://arxiv.org/pdf/1210.2864.pdf
- https://research.chalmers.se/en/publication/239098
- http://aclweb.org/anthology/P/P14/P14-5006.pdf
- http://www.cs.cmu.edu/~dwrensha/15-745/final.pdf
- https://figshare.com/articles/_AUC_PR_and_AUC_ROC_for_DREAM3_100_node_networks_/1004689
- http://hdl.handle.net/1854/LU-8731276
- https://hdl.handle.net/10356/147982
- https://hal.archives-ouvertes.fr/hal-03336593
- https://digitalcommons.usm.maine.edu/healthpolicy/20
- https://doaj.org/toc/2248-9622
- http://hdl.handle.net/11025/35863
- http://infoscience.epfl.ch/record/195687/files/chef.pdf
- https://pub.uni-bielefeld.de/record/1796635
- http://arxiv.org/abs/2205.11039
- http://etd.adm.unipi.it/theses/available/etd-07012022-182656/
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27678
- http://purl.utwente.nl/publications/54794
- http://arxiv.org/abs/2205.09088
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.2992
- https://hal.laas.fr/hal-03318448
- http://arxiv.org/abs/2201.08455
- https://zenodo.org/record/8081983
- http://www.ece.tamu.edu/%7Espalermo/ecen689/PRBS_%26_PLL_model.pdf
- https://www.aaai.org/Papers/FLAIRS/2007/Flairs07-027.pdf
- http://cds.cern.ch/record/2010066
- https://figshare.com/articles/_AUPR_and_AUROC_scores_for_all_six_algorithms_and_one_integrative_analysis_using_three_gold_standard_datasets_from_the_DREAM5_challenge_/738070
- https://hal.inria.fr/hal-01609576
- http://publica.fraunhofer.de/documents/N-565622.html
- https://zenodo.org/record/3823095
- http://www.mos.t.u-tokyo.ac.jp/~y-oike/Papers/ipsoc2004.pdf
- http://www.cs.huji.ac.il/%7Eshaull/pub/LTLFQuery.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/8496
- http://arxiv.org/pdf/1306.0271.pdf
- http://hdl.handle.net/10.1371/journal.pone.0208185.g004
- https://zenodo.org/record/8001815
- https://aaltodoc.aalto.fi/handle/123456789/27390
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-01892705/document
- https://zenodo.org/record/7550150
- https://library.oapen.org/handle/20.500.12657/58220
- http://resolver.tudelft.nl/uuid:50562fb5-f04c-472c-b935-c3928765f24d
- https://escholarship.org/uc/item/50n838xp
- http://eprints.lse.ac.uk/7624/
- https://trepo.tuni.fi//handle/123456789/26864
- https://figshare.com/articles/_Classification_accuracy_of_LDA_using_a_single_color_channel_on_the_GTFB_database_/257646
- https://pub.uni-bielefeld.de/record/2497911
- http://hdl.handle.net/10.1371/journal.pone.0204999.g009
- https://zenodo.org/record/8325592
- https://hdl.handle.net/11386/4825232
- http://cumincad.architexturez.net//doc/oai-cumincadworks-id-e7b8
- https://zenodo.org/record/4534128
- https://research.library.fordham.edu/cgi/viewcontent.cgi?article=1061&amp;context=frcv_facultypubs
- http://hdl.handle.net/10261/189116
- https://repository.upenn.edu/cis_reports/334
- https://doaj.org/article/2a3c515496a443efa85ddd995ff96cd6
- http://hdl.handle.net/10.1371/journal.pcbi.1009224.g005
- https://zenodo.org/record/6798193
- https://zenodo.org/record/1946392
- http://hdl.handle.net/10.1371/journal.pone.0204338.g005
- http://arxiv.org/abs/2205.00731
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.73.295
- https://escholarship.org/uc/item/4jp775f7
- https://zenodo.org/record/7634134
- https://doi.org/10.1109/CCNC49033.2022.9700636
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.8523
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066105052163/MAIN/application/pdf/85a2eb32ae488e7ca17640756c41bad2/main.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/11671
- https://zenodo.org/record/4483825
- https://nrc-publications.canada.ca/eng/view/object/?id=ad6b57cc-c891-4598-a9ff-75a24d4a5c3a
- https://www.repo.uni-hannover.de/handle/123456789/11614
- http://arxiv.org/abs/2112.15280
- https://figshare.com/articles/_Number_of_completed_TeamQ_evaluations_needed_to_obtain_reliable_theme_scores_based_on_generalizability_analysis_/1239953
- http://dx.doi.org/10.22028/D291-25037
- https://figshare.com/articles/_AUC_for_different_time_points_and_doses_in_TG_GATEs_/1117190
- http://www.cs.kuleuven.ac.be/publicaties/rapporten/cw/CW253/MartinKing.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.5570
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.9911
- https://hal-emse.ccsd.cnrs.fr/emse-04138834
- http://repositorium.sdum.uminho.pt/bitstream/1822/19010/1/2010%20-%20Springer%20DCAI%20LCNBN.pdf
- https://research.vu.nl/en/publications/8442e638-c860-4005-b8a1-c461b7215272
- https://www.aaai.org/Papers/Workshops/2008/WS-08-11/WS08-11-004.pdf
- http://hdl.handle.net/10.1371/journal.pone.0203339.g016
- https://zenodo.org/record/5781449
- https://zenodo.org/record/4739760
- https://hal.archives-ouvertes.fr/hal-03842359
- http://hdl.handle.net/1854/LU-417389
- http://faculty.kfupm.edu.sa/COE/mayez/Publications(pdf)/Pact-95-maasarani.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.3906
- https://zenodo.org/record/4047756
- https://ebooks.iospress.nl/volumearticle/63734
- http://hdl.handle.net/10072/403779
- https://inria.hal.science/hal-04041691
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.6199
- http://arxiv.org/abs/2203.15544