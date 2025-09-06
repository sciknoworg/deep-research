# Retrieval-Augmented Deductive Reasoning (RADR) via Structural Decomposition of Legal Analysis

*Author: [assistant-generated] • Date: 2025-09-04*

---
## 1  Executive Summary
Retrieval-Augmented Deductive Reasoning (RADR) aims to combine the breadth of modern retrieval (dense semantic and symbolic) with the rigor of formal deductive and defeasible logic.  Drawing on three decades of legal-AI scholarship and recent breakthroughs in large language models (LLMs), SAT/SMT, neuro-symbolic integration, and regulatory governance (EU AI Act 2024/1689), this report synthesises the state of the art and lays out a design, evaluation and deployment blueprint for RADR.  Key findings:

1. Hybrid architectures (rule-based + case-based + neural) dominate production legal DSSs; proven migration paths (e.g., RuleML↔Drools, SweetProlog, LogicNets) avoid vendor lock-in while preserving explainability.
2. Symbolic systems still beat LLMs on hard statutory reasoning benchmarks (SARA 2024), yet GPT-class models fine-tuned on structured corpora (GDPR LegalDocML/LegalRuleML) reach SOTA on rule classification.  RADR must leverage both.
3. Vector databases such as **Weaviate** and neuro-symbolic transfer schemes (Deep Logic Models, Semantic-Based Regularisation, PRODEF) now offer scalable substrates for embedding-aware retrieval that can feed formal engines (Prolog, ASP, SMT) without lossy transformations.
4. New regulatory imperatives—Fundamental Rights Impact Assessments (FRIA), Article 27 EU AI Act—require quantitative bias, privacy and discrimination evidence.  Explainability fidelity and risk-metric coverage are therefore core evaluation axes alongside raw reasoning accuracy and runtime.
5. Best-of-breed solver choices are domain-dependent:  MathSAT 5 outperforms Z3 on bit-precise floating-point verification (SV-COMP 2023), while d-Prolog/DR-Prolog excel at defeasible normative reasoning.  RADR should offer a pluggable back-end abstraction.

---
## 2  Problem Statement and Motivation

Legal analysis is structurally decomposable into recurring subtasks—issue spotting, statutory rule extraction, precedent alignment, fact abstraction, argument assembly, norm conflict resolution and remedy calculation.  LLMs shine at broad, *surface-level* retrieval but falter on logically intensive steps (e.g., contrary-to-duty obligations, temporal norm change, institutional agency).  Conversely, symbolic systems deliver provably correct deductions but depend on brittle, labour-intensive knowledge bases and struggle with open-textured concepts.  RADR targets a middle path:

* Retrieve heterogeneous artefacts (statutes, regulations, contracts, case law, scholarly commentary) with high recall *and* semantic precision.
* Canonicalise and route the results into specialised deductive/defeasible engines able to explain, verify and—where needed—refute preliminary LLM answers.
* Deliver outputs that satisfy **both** practitioner usability (argument trees, citations, factor mappings) and regulatory duties (bias metrics, FRIA, audit trails).

---
## 3  Structural Decomposition of Legal Analysis (RADR Pipeline)

| Stage | Purpose | Recommended Techniques | Tooling Candidates |
|-------|---------|-------------------------|--------------------|
|¹ Query Normalisation & Embedding|Transform user query into symbolic + dense representations.|Prompt-engineering + OpenAI Function-calling; Ontology-guided term expansion (GDPRtEXT, SKOS).|GPT-4o, spaCy, Elastic BM25, Weaviate HNSW.|
|² Hybrid Retrieval|Parallel symbolic (citation nets, rule indices) and vector search.|Ikbals k-NN/LR weighting, BankXX multi-layer indices.|Weaviate + custom CBR index; FAISS; Graph-DB (Neo4j).|
|³ Result Typing & Structural Segmentation|Label retrieved artefacts as Rule / Fact / Analogy / Context.|Fine-tuned GPT-3 (Legal Rule Classification), ProbLog2 WMC segmentation.|OpenAI fine-tune, HuggingFace LoRA, SpaCy entityRuler.|
|⁴ Canonicalisation & Formalisation|Convert text snippets to formal representations.|LegalDocML/LegalRuleML; RuleML mapping; Jaist NN→FOL distillation.|SweetProlog, RuleML XSLT, JAIST pipeline.|
|⁵ Deductive / Defeasible Reasoning|Apply strict, defeasible, temporal & deontic logics.|d-Prolog, DR-Prolog, Rotolo et al. temporal DL; ASPMT→SMT.|d-Prolog, DR-Prolog, Clingo, Z3, MathSAT5.|
|⁶ Verification & Counter-Model Checking|Prove obligations, permissions, conflicts, exceptions; generate minimal counter-examples.|ESBMC FP verifier; SMT-based proof certificates; ASPIC+ argument attack graphs.|MathSAT5, ESBMC, ASPIC+ Workbench.|
|⁷ Explanation & FRIA Metrics|Render argument trees, precedence chains, bias & risk scores; prepare Annex III documentation.|Nearest-neighbour local explanations; CDD fairness metric; LogicNets proof viewer.|LogicNets, DR-Prolog proof API, custom Streamlit dashboard.|

### 3.1 Bridging Retrieval and Deduction
The cleavage between free-text retrieval and formal reasoning is bridged via *intermediate structural representations* (legal ontologies, factor graphs, rule fragments).  Proven loss-less converters (SweetProlog, RuleML 1.0 DTD) guarantee round-trip fidelity, while neuro-symbolic distillation (JAIST 2022) injects LLM-extracted latent concepts into Prolog/ASP without manual encoding.

---
## 4  Target Legal Domains & Document Types

RADR is **domain-agnostic by design**, yet early focus accelerates evaluation and dataset curation.  We recommend two complementary tracks:

1. **Statutory & Regulatory Reasoning**  
   • U.S. federal statutes (SARA benchmark continuity)  
   • EU acquis communautaire (GDPR, EU AI Act, Digital Services Act)  
   • Sectoral regulations (medical device directives, ESG disclosure rules)

2. **Contractual & Private-Law Instruments**  
   • Commercial contracts (LEDGAR, CaseHOLD)  
   • Data-processing agreements (DPA), standard contractual clauses  
   • Corporate policies subject to Annex III AI Act high-risk classification

These domains already enjoy machine-readable corpora (LegalRuleML, LegalDocML, GDPRtEXT, DAPRECO) and benchmark coverage (LexGLUE, LEXTREME), easing retrieval indexing and ground-truth generation.

---
## 5  Evaluation Framework

### 5.1 Core Metrics
1. **Reasoning Accuracy**  
   • Compliance with gold-standard answers on SARA, LexGLUE, LEXTREME.  
   • Formal proof check (SMT certificate validity).

2. **Explainability Fidelity**  
   • Exact match between generated argument tree and underlying proof steps.  
   • Survey-validated intelligibility (ECtHR argument-based XAI 97 % accuracy).  
   • Faithfulness gap ≤ 5 % vs ground-truth proof graph.

3. **Fairness & Fundamental Rights Impact**  
   • Conditional Demographic Disparity (CDD) on synthetic/real test pools.  
   • Documentation coverage vs EU AI Act Annex III check-list.

4. **Computational Efficiency & Green AI**  
   • Cost per 100 queries (CPU/GPU kWh, CO₂eq; cf. ICSE 2022 Green AI).  
   • Solver wall-time and memory (SV-COMP reporting style).

5. **Scalability & Portability**  
   • Throughput on 100 k-document corpora.  
   • Loss-less RuleML/Drools round-trip rate.

### 5.2 Benchmark Mix
• SARA (statutes)   • LexGLUE 7 tasks   • GDPR LRC   • ECtHR-A/B outcome & summarisation   • LEDGAR clause extraction   • Custom Annex III FRIA stress-tests.

Cost-sensitive instance selection (LIPIcs-CP 2021) will cut evaluation runtime by ≈70 % while preserving power rankings.

---
## 6  Integration with Existing Frameworks & Toolchains

| Layer | Integration Candidates | Rationale |
|-------|------------------------|-----------|
|Retrieval|Weaviate, Elastic, GPT-4o RAG toolkit|Combine vector and keyword indices; Weaviate supports hybrid queries and external ML pipelines.|
|Neuro-Symbolic Bridge|JAIST NN→FOL distillation, Deep Logic Models, Semantic-Based Regularisation|Converts LLM latent knowledge into logic rules; supports back-prop constraints if future joint learning desired.|
|Rule Exchange|RuleML 1.0, LegalRuleML, SweetProlog|Round-trip serialisation, guarantees compliance with Semantic-Web standards.|
|Defeasible Reasoning|d-Prolog, DR-Prolog, Rotolo temporal DL|Handles norm hierarchies, exceptions, temporal change, contrary-to-duty.|
|Assertion & Example Reasoning|Inference Graphs, MIX taxonomy|Supports hybrid deductive + analogical reasoning needed for precedent alignment.|
|Formal Verification|ESBMC 7.3 (MathSAT 5), Z3, ASPSMT2SMT|Model-check formal encodings, ensure soundness, generate counter-models.|
|XAI/UX|LogicNets, Streamlit, ASPIC+ Workbench|Render proofs, factor hierarchies, bias reports, FRIA dashboards.|

---
## 7  Reference Implementation Blueprint

```mermaid
graph LR
A[User Query]
A --> B1[Symbolic Expansion]
A --> B2[Embedding Vector]
B1 --> C[Hybrid Search Broker]
B2 --> C
C --> D1[Symbolic Results]
C --> D2[Vector Hits]
D1 & D2 --> E[Result Typing / Segmentation]
E --> F[Canonicalisation (RuleML, FOL, DL)]
F --> G[Deductive / Defeasible Engine]
G --> H1[Proof Graph]
G --> H2[Counter-Models]
H1 & H2 --> I[Explanation Renderer + FRIA Metrics]
I --> J[Human-Facing Output (Docx / HTML / JSON)]
```

*Deployment stack*:  Python micro-services with gRPC; Weaviate for retrieval; Prolog (SWI) + d-Prolog meta-interpreter; MathSAT5 via PySMT; Streamlit front-end.

---
## 8  Research & Development Roadmap

| Phase | Duration | Milestones |
|-------|----------|------------|
|0 Preparation|Q4-2025|Corpus acquisition (GDPRtEXT, DAPRECO, SARA, LexGLUE); standing CI/CD with cost-aware sampling harness.|
|1 MVP|Q1-2026|Hybrid search broker + Prolog canonicaliser; pass ≥70 % of SARA subset; basic argument tree export.|
|2 Neuro-Symbolic Upgrade|Q2-2026|LLM distillation to FOL; 5-point accuracy lift; integrate vector-symbolic architecture (VSA) for edge inference.|
|3 FRIA Compliance Pack|Q3-2026|CDD bias reports; Annex III evidence generator; obtain external audit sign-off.|
|4 Scalability & Green AI|Q4-2026|Throughput ≥200 queries/min; CO₂eq per query < 0.5 g; incorporate DISPO style OR-parallelism in Prolog back-end.|
|5 Full Product|2027|Multi-domain release (statute + contracts); user-configurable logic modules; pluggable solver/distributed retrieval.|

---
## 9  Risk & Mitigation Analysis

1. **Bias & Discrimination** – Use CDD metric; differential privacy noise; human-in-the-loop audits.
2. **Explainability Gaps** – Enforce proof certificate logging; perform fidelity spot-checks; fallback to symbolic subsystem for contested outputs.
3. **Regulatory Drift** – Continuous mapping to evolving EU AI Act delegates; automated update watch on EUR-LEX; rule-patch diffing via RuleML.
4. **Scalability Bottlenecks** – Adopt DISPO OR-parallelism; Bounded-model checking pre-pass (Dartagnan style) to shrink solver search.
5. **Knowledge Base Staleness** – Leverage LYNX curation platform; schedule nightly SPARQL delta harvests; automated integrity constraints.

---
## 10  Contrarian/Speculative Opportunities
*(Flagged as forward-looking, high-uncertainty)*

• Edge-deployable Vector-Symbolic Architecture (VSA) chips could run the retrieval facet on-device, lowering latency for courtroom/field use.

• SAT-based proof logging + blockchain anchoring offers tamper-evident audit trails, addressing Article 10 AI Act data governance.

• Generative argument mining via **LLM-to-ASP** translation may produce *counter-factual* precedents useful for policy simulation and legislative drafting.

---
## 11  Conclusion
Retrieval-Augmented Deductive Reasoning stands poised to reconcile the scalability of neural retrieval with the fidelity of symbolic legal reasoning.  By grounding the pipeline in open standards (RuleML, LegalRuleML), leveraging best-in-class solvers (MathSAT5, d-Prolog) and meeting stringent new regulatory duties (FRIA, bias metrics), RADR can deliver practical, trustworthy decision-support that outperforms either paradigm alone.  A staged roadmap, robust evaluation harness and pluggable architecture will de-risk development while leaving room for emerging neuro-symbolic innovations.

---
### Appendix A  Key References (Chronological)
• DISPO OR-parallel Prolog VM (FLAIRS 1999).  • RuleML 1.0 specification (2013).  • SweetProlog ontology round-trip (2004).  • DR-Prolog Tool Suite (AAAI 2005).  • ProbLog2 Weighted MC (2015).  • Rotolo et al. temporal defeasible logic (2013-2020).  • LYNX Legal KG (2017-2021).  • LexGLUE benchmark (2021).  • JAIST neural-symbolic distillation (2022).  • SV-COMP 2023 ESBMC-MathSAT FP victory.  • SARA statutory reasoning dataset (2024).  • EU AI Act Regulation 2024/1689.

---
*End of Report*

## Sources

- https://espace.library.uq.edu.au/view/UQ:72b8dfb
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/61590
- http://airccj.org/CSCP/vol4/csit42503.pdf
- http://hdl.handle.net/10119/4651
- https://zenodo.org/record/5162546
- https://eprints.whiterose.ac.uk/178919/1/2110.00976v1.pdf
- http://hdl.handle.net/1721.1/3545
- https://ir.cwi.nl/pub/29447
- http://oa.upm.es/55403/
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1571066105806620/MAIN/application/pdf/cc76a04ec85041b81deaeaefb4181337/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.3359
- http://handle.westernsydney.edu.au:8081/1959.7/uws:47646
- http://hdl.handle.net/11343/39621
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.131
- http://www.cs.rutgers.edu/%7Emccarty/research/rj90.pdf
- http://hdl.handle.net/11585/881319
- https://www.cai.sk/ojs/index.php/cai/article/view/630
- https://zenodo.org/record/3587674
- https://hdl.handle.net/11582/341507
- http://www.theses.fr/2013GREND001/document
- http://www.unibuc.ro/prof/vlada_m/docs/2011/apr/11_15_47_49Probleme_prolog.pdf
- https://scholarship.law.nd.edu/law_books/1235/thumbnail.jpg
- https://resolver.caltech.edu/CaltechAUTHORS:20161006-130031306
- https://ebooks.iospress.nl/volumearticle/58848
- http://eprints.uthm.edu.my/9756/
- http://dx.doi.org/10.1016/j.artint.2023.103861
- https://figshare.com/articles/GDPR_tool_for_handling_Data-Subject_rights_requests/5853180
- https://www.repository.law.indiana.edu/ilj/vol84/iss3/1
- https://figshare.com/articles/_Comparison_of_runtime_at_different_percentages_of_the_corpus_in_the_study_case_/1058691
- https://www.utupub.fi/handle/10024/154606
- https://elibrary.law.psu.edu/pslr_symposia/2020/tech/3
- http://hdl.handle.net/11590/338479
- https://ojs.victoria.ac.nz/wfes/article/view/8419
- http://www.smtcomp.org/2009/rules09.pdf
- https://lirias.kuleuven.be/bitstream/123456789/502578/1/thesis_final_dimitar_shterionov.pdf
- http://hdl.handle.net/11590/338448
- https://zenodo.org/record/5850115
- https://orbilu.uni.lu/handle/10993/57759
- http://hdl.handle.net/11586/12441
- http://lst.nectec.or.th/marut/papers/ICSEC2013_Review_Rule_Language_IE_CR.pdf
- https://nrc-publications.canada.ca/eng/view/accepted/?id=5c7d558c-c2f3-4b6a-a2d5-3673f53c3230
- https://oa.upm.es/14497/
- https://orbilu.uni.lu/handle/10993/45489
- http://peace.eas.asu.edu/joolee/papers/aspmt-system-jelia.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.9188
- https://hec.hal.science/hal-03885355
- https://zenodo.org/record/8139254
- https://doi.org/10.1145/3594536.3595129
- https://zenodo.org/record/6518245
- http://hdl.handle.net/2429/42045
- https://zenodo.org/record/6014327
- https://digitalcommons.wcl.american.edu/pub_disc_presentations/115
- https://www.researchgate.net/profile/Antonis_Bikakis2/publication/221238888_The_DR-Prolog_Tool_Suite_for_Defeasible_Reasoning_and_Proof_Explanation_in_the_Semantic_Web/links/00b7d517bfd9c4757b000000.pdf?origin%3Dpublication_detail
- http://jhir.library.jhu.edu/handle/1774.2/67855
- https://openaccess.city.ac.uk/id/eprint/299/2/Neurons_and_Symbols.pdf
- http://opac.fitk.uinjkt.ac.id//index.php?p=show_detail&id=9988
- http://hdl.handle.net/10197/10526
- https://hdl.handle.net/1814/16057
- https://hal.archives-ouvertes.fr/hal-02397050/document
- https://zenodo.org/record/8375183
- http://mindmodeling.org/cogsci2012/papers/0311/paper0311.pdf
- http://hdl.handle.net/2445/123425
- https://authors.library.caltech.edu/26676/1/postscript.ps
- https://ir.lawnet.fordham.edu/iplj/vol30/iss1/3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.432.4615
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA211444%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://www.aaai.org/ocs/index.php/SSS/SSS15/paper/viewFile/10281/10029%26sa%3DU%26ved%3D0CAQQFjAAahUKEwjd3tPQqPvGAhWCVhQKHacjCJQ%26client%3Dinternal-uds-cse%26usg%3DAFQjCNF4wF1u_JS20P9rQfT25aSsc26HMg/
- http://hdl.handle.net/10278/3742943
- https://hal.inria.fr/hal-01187003
- http://hdl.handle.net/11568/190551
- http://hdl.handle.net/20.500.11794/38195
- https://www.itenrecht.nl/dossiers
- http://www.ieccr.net/2013/ietict/
- http://cds.cern.ch/record/2115349
- https://figshare.com/articles/_Performance_comparison_of_several_algorithms_on_the_DREAM4_in_silico_multifactorial_dataset_/973778
- http://www.aaai.org/Papers/AAAI/1994/AAAI94-084.pdf
- http://hdl.handle.net/10.1371/journal.pone.0201455.t001
- https://ejournals.lib.auth.gr/infolawj/article/view/10462
- http://www.cs.nyu.edu/~barrett/pubs/BdMS05-CAV.pdf
- http://hdl.handle.net/10138/311162
- http://dx.doi.org/10.48550/arXiv.2301.13126
- http://menzies.us/pdf/05fsscocomo.pdf
- http://hdl.handle.net/1814/56124
- https://hal-cnrs.archives-ouvertes.fr/hal-03800492/file/LIPIcs-CP-2021-43.pdf
- https://brill.com/edcollbook/title/62134
- https://zenodo.org/record/7627783
- https://researchbank.rmit.edu.au/view/rmit:37980
- https://zenodo.org/record/8239725
- http://hdl.handle.net/2066/84486
- http://hdl.handle.net/10.1371/journal.pcbi.1010493.s002
- https://orbilu.uni.lu/handle/10993/52162
- https://zenodo.org/record/5666728
- http://orbilu.uni.lu/handle/10993/39701
- https://doaj.org/toc/1932-6203
- https://scholarship.law.ufl.edu/context/ftr/article/1288/viewcontent/lauren_2C_2BFTR_02.Lawsky.pdf
- https://www.um.edu.mt/library/oar//handle/123456789/22368
- https://biblio.ugent.be/publication/8708154/file/8708155
- http://hdl.handle.net/10.6084/m9.figshare.21228650.v1
- http://cemadoc.irstea.fr/cemoa/PUB00002083
- http://researchonline.federation.edu.au/vital/access/HandleResolver/1959.17/44208
- https://ojs.aaai.org/index.php/AIES/article/view/31648
- http://cds.cern.ch/record/1314888
- https://zenodo.org/record/8233714
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.5679
- http://upcommons.upc.edu/bitstream/handle/2117/2684/doc1.pdf%3Bjsessionid%3D1FAA26E31A09F34CE4C5199D83E5B0B6?sequence%3D1
- http://resolver.tudelft.nl/uuid:7c918897-b994-4ed9-9680-2ddd1e6dabeb
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.9323
- http://www.aaai.org/Papers/FLAIRS/1999/FLAIRS99-050.pdf
- https://biblio.ugent.be/publication/01H4SYNE382AKENHDHGFE8AHNY/file/01H4SZ0QN1DATYD77HC9N5F8ZH
- https://scholarship.law.nd.edu/law_books/111
- https://zenodo.org/record/5532997
- http://eprints.binus.ac.id/24324/1/2003-1-20020-IF%20abstrak.pdf
- http://www.icc.qmul.ac.uk/gar/index.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.8732
- http://hdl.handle.net/10068/47683
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.459
- http://hdl.handle.net/10150/106135
- http://hdl.handle.net/10536/DRO/DU:30085286
- https://research.vu.nl/en/publications/16ec1c82-3812-4a8f-b073-b869a213333d
- http://publikace.k.utb.cz/handle/10563/1010790
- https://repository.law.umich.edu/mjgl/vol16/iss2/2
- http://www.cse.buffalo.edu/%7Eshapiro/Papers/schsha14.pdf
- https://figshare.com/articles/Binary_SVM_and_AdaBoost_classifier_performance_for_average_ERP_data_using_identical_input_features_/3116101
- http://ojs.academypublisher.com/index.php/jetwi/article/download/0204343353/2338/
- https://hal.inria.fr/inria-00108034
- http://www.springer.com/series/7899
- https://shs.hal.science/halshs-02552395
- https://doaj.org/article/e6ab6a942ab8464e8be9707c2b9ff1ef
- http://hdl.handle.net/10447/103267
- https://hal.archives-ouvertes.fr/hal-03679650
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.7838
- https://repository.law.umich.edu/cgi/viewcontent.cgi?article=1324&amp;context=book_chapters
- https://figshare.com/articles/GDPRtEXT_-_GDPR_as_a_Linked_Data_Resource/6893066
- http://hdl.handle.net/11372/LRT-1408
- https://doaj.org/toc/1558-7223
- https://ojs.aaai.org/index.php/AIES/article/view/31700
- http://www.theseus.fi/handle/10024/158328
- http://xyuan.myweb.cs.uwindsor.ca/references/LawExpertSystem09.pdf
- https://orca.cardiff.ac.uk/id/eprint/2051/1/a_simple_rule_induction_algorithm.pdf
- http://hdl.handle.net/11583/2503716
- https://hal.archives-ouvertes.fr/hal-02141770
- https://zenodo.org/record/6259048
- https://zenodo.org/record/3946085
- https://orbilu.uni.lu/bitstream/10993/40980/1/msp201906.article.pdf
- https://figshare.com/articles/Micro-averaged_performance_comparison_of_PhenoNorm_against_other_normsalisation_approaches_applied_to_the_NCBI_disease_corpus_/3841539
- https://livrepository.liverpool.ac.uk/3186206/1/JURIX_2024___ECHR_Judgment_Paper.pdf
- https://doaj.org/article/725c0a889f3044d7921c5369a133fa64
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:184993
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.6025
- https://hal.science/hal-03674949
- http://hal.inria.fr/docs/00/87/86/77/PDF/improving_case-based.pdf
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-01894744/file/hecham-8-demo.pdf
- https://escholarship.org/uc/item/6607r8tt
- http://hdl.handle.net/2066/92331
- http://link.springer.com/chapter/10.1007%2F978-3-642-19583-9_2
- https://hdl.handle.net/11585/841429
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.5639
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.3800
- https://doi.org/10.1007/978-3-319-70145-5_14
- https://doaj.org/article/a8e52d03c3cb43dcb9dc4646ef63ca2b
- https://hdl.handle.net/1813/73144
- http://www.aaai.org/Papers/AAAI/2005/SA05-006.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.3709
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.4260
- http://hdl.handle.net/11585/153269
- http://hdl.handle.net/11380/608954
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.3057
- http://ceur-ws.org/Vol-2690/COUrT-paper1.pdf
- http://hdl.handle.net/11585/63495
- https://hal.archives-ouvertes.fr/hal-01332051
- http://vuir.vu.edu.au/10684/
- https://pure.hud.ac.uk/en/publications/legal-representation-and-reasoning-in-practice-a-critical-compari
- http://hdl.handle.net/11585/841694
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.7492
- http://hdl.handle.net/10068/623583
- http://vuir.vu.edu.au/10652/
- https://eprints.qut.edu.au/71067/
- http://www.thesai.org/Downloads/Volume6No12/Paper_1-Introducing_a_Method_for_Modeling_Knowledge_Bases_in_Expert_Systems.pdf
- https://zenodo.org/record/4066438
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-212183
- https://orca.cardiff.ac.uk/id/eprint/175868/1/SPIE_2024_VSA_Paper_1.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-273787
- https://research.vu.nl/en/publications/b324c489-cc7c-404a-8db7-0f02dab314dd
- http://doi.org/10.1080/13600834.1993.9965670
- http://hdl.handle.net/10.1371/journal.pone.0291750.t008
- https://drops.dagstuhl.de/opus/volltexte/2010/2800/
- https://aisel.aisnet.org/wi2023/77
- http://iccd.et.tudelft.nl/Proceedings/2007/Papers/3.3.1.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17522
- http://hdl.handle.net/2072/434984
- https://www.aaai.org/Papers/Workshops/1994/WS-94-01/WS94-01-030.pdf
- https://nrc-publications.canada.ca/eng/view/object/?id=0ee36c35-f3c3-420e-8c70-4f8031604018
- https://zenodo.org/record/4720282
- https://doi.org/10.1016/j.jval.2024.10.1835
- http://digital.library.wisc.edu/1793/60584
- https://hal.archives-ouvertes.fr/hal-01863729
- https://cris.maastrichtuniversity.nl/ws/files/72539184/waddington_1999_testing_the_limits_of_the_EC_treaty.pdf
- http://www.helsinki.fi/~pietarin/publications/Defeasible
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.8957
- https://espace.library.uq.edu.au/view/UQ:278467/progress.pl
- https://doaj.org/article/eee3692d2e744f85883012cbdcb0c291
- https://figshare.com/articles/_Comparison_of_compression_performance_of_SRComp_to_gzip_bzip2_BEETL_and_SCALCE_/877760
- http://arxiv.org/pdf/1011.5332.pdf
- https://dspace.library.uu.nl/handle/1874/420552
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.4001
- https://figshare.com/articles/_The_performance_of_SCMLFP_and_the_compared_SVM_based_methods_on_the_dataset_consisting_of_269_luciferases_and_216_FPs_/1026466
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.5682
- https://figshare.com/articles/Population_demographics_and_clinical_characteristics_based_on_collateral_grades_/5485318
- http://www.loc.gov/mods/v3
- https://philpapers.org/rec/MEASL
- http://publica.fraunhofer.de/documents/N-74175.html
- http://hdl.handle.net/10609/73125
- http://hdl.handle.net/11585/708837
- http://hdl.handle.net/10150/105191
- https://search.gesis.org/research_data/ZA6790?lang=de