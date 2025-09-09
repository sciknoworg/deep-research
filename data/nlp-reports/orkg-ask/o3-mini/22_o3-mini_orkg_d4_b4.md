# Final Report: A Two-Man Band – Integrating LLMs, Code, and Knowledge Graphs for Enhanced Clarity, Factuality, and Logical Reasoning

This report presents a comprehensive analysis of the synergistic integration of Large Language Models (LLMs), code-driven systems, and knowledge graphs. Drawing on extensive research findings from diverse academic and industrial case studies, we explore how these components interact to improve logical reasoning, factual accuracy, and overall clarity across applications. The interdisciplinary approach is encapsulated in the metaphorical notion of a “Two-Man Band,” emphasizing the complementary roles that tightly integrated systems can play in addressing complex, real-world challenges.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Component Roles and Interactions](#component-roles-and-interactions)
   - [LLMs](#llms)
   - [Code and Computational Infrastructures](#code-and-computational-infrastructures)
   - [Knowledge Graphs](#knowledge-graphs)
3. [Technological Underpinnings and Hybrid Approaches](#technological-underpinnings-and-hybrid-approaches)
4. [Application Domains and Real-World Scenarios](#application-domains-and-real-world-scenarios)
5. [Evaluation Metrics and Methodological Considerations](#evaluation-metrics-and-methodological-considerations)
6. [Advanced Techniques and Emerging Trends](#advanced-techniques-and-emerging-trends)
7. [Case Studies and Benchmarking Frameworks](#case-studies-and-benchmarking-frameworks)
8. [Discussion, Limitations, and Future Research](#discussion-limitations-and-future-research)
9. [Conclusion](#conclusion)

---

## Introduction

The integration of LLMs with code components and knowledge graphs represents a significant evolution in computational systems that aim to enhance clarity, improve factuality, and foster robust logical reasoning. This multi-faceted approach blends symbolic reasoning with neural methods, leading to more reliable handling of diverse datasets and enhanced interpretability of system outputs. Recent research underscores the impact of combining these paradigms, whether in the domain of legal information retrieval, healthcare data management, or eCommerce consumer behavior analysis.

This report collates the learnings from multiple research studies ranging from knowledge graph completion and link prediction to neuro-symbolic architectures and declarative programming methods. We provide a detailed discussion on how to systemically fuse these components to bolster system performance across evaluative benchmarks like Mean Reciprocal Rank (MRR), Hits@N, as well as qualitative stakeholder feedback.

---

## Component Roles and Interactions

### LLMs

**Role and Utility**: LLMs are at the core of natural language understanding tasks. They excel in generating text, extracting facts, and providing logical continuations to unknown inputs. In the integrated framework:

- **Factuality Enhancement**: They extract facts and context, assisting in error correction and dataset generation (as evidenced by zero-shot KG construction in systems like LLM-KG-Bench).
- **Adaptability**: By leveraging adaptive prompt engineering, LLMs can overcome input-length constraints while facilitating a smooth transition between few-shot in-context learning and full fine-tuning.
- **Multi-Modal Interactions**: Their integration with code allows for dynamic interfacing with knowledge graphs, ensuring the production of grounded outputs.

### Code and Computational Infrastructures

**Role and Utility**: Code plays multiple roles in this ecosystem—from orchestrating the underlying data pipelines to implementing real-time performance optimizations. Its primary functions include:

- **Automated Maintenance and Feedback Loops**: Advanced code systems manage reinforcement learning (RL) loops and reward shaping, integrating qualitative human feedback and real-time computational signals (e.g., MP-MODA framework and RLHF approaches).
- **Declarative and Imperative Synergy**: By leveraging declarative paradigms (e.g., extended Datalog, KDDlog), the code simplifies complex query handling over large-scale knowledge graphs. Studies involving logic programming have shown significant gains in scalability on both multicore and distributed platforms.
- **Optimization and Sampling**: Automated surrogate modeling and adaptive sampling strategies ensure efficient hyperparameter optimization—a critical factor in reducing computational overhead and enhancing real-world responsiveness.

### Knowledge Graphs

**Role and Utility**: Knowledge Graphs (KGs) provide a semantic structure that encapsulates domain-specific knowledge. They serve as both a repository and an enrichment mechanism for LLM outputs:

- **Semantic Enrichment & Ontological Reasoning**: KGs encode complex relational information and support distributed data fusion. Projects like Amazon Neptune-based legal management systems showcase how KGs integrate data from diverse sources for enhanced search and retrieval operations.
- **Scalability and Heterogeneity**: With proven efficacy across data sources like Linked MDB, DBpedia, and industry-specific datasets, KGs are a cornerstone of FAIR data infrastructures and enterprise knowledge management solutions.
- **Hybrid Matching and Instance Alignment**: Algorithms such as SiGMa and hybrid approaches incorporating discriminative features ensure that large-scale entity matching is both accurate and computationally efficient.

---

## Technological Underpinnings and Hybrid Approaches

In advancing this integrated system, numerous hybrid approaches have emerged:

- **Graph-Based Semantic Methods**: These include rule-based aggregations, GAN-driven zero-shot relational learning, and reinforcement learning-driven frameworks that combine neural and symbolic inputs. Hybrid systems that integrate neuro-fuzzy networks have shown improved predictive performance over traditional time series methods.

- **Declarative and Constraint Programming**: Extensions to logic-based languages (DeAL, KDDlog) enable efficient query processing and recursive data retrieval. Research has demonstrated their superior performance over conventional systems like Apache Spark, particularly in high-data-volume scenarios.

- **Hybrid Prompt Engineering**: Innovations such as Prompt-Augmented Linear Probing (PALP) merge adaptive prompt methods with linear probing techniques, effectively bridging the gap between in-context learning and full fine-tuning while scaling across multi-dimensional evaluation metrics.

- **Dual Architectures in Graph-LLM Integration**: Techniques demonstrated in recent arXiv papers (e.g., arXiv:2310.05499) reinforce LLM reasoning with explicit, structural graph knowledge. This cross-domain strategy minimizes hallucinations and promotes high logical fidelity in generated outputs.

---

## Application Domains and Real-World Scenarios

The envisioned system applies across a number of domains, validated through empirical studies and industrial benchmarks:

- **Legal and Regulatory Domains**: Deployments in legal management systems (e.g., Amazon Neptune-based implementations) have successfully integrated data from varied sources (laws, court data, third-party legal inputs) and demonstrated high performance in query latency and throughput.

- **Healthcare and FAIR Data Infrastructures**: Knowledge graphs support semantic interoperability initiatives, such as those reported in the German NFDI working group, ensuring that complex clinical datasets are both FAIR and scalable.

- **Industry 4.0 and Cyber-Physical Systems**: Modular KG architectures based on RAMI 4.0 guidelines improve bottom-up contextualization and top-down abstraction in manufacturing, enhancing automated decision-making processes.

- **eCommerce and Neuromarketing**: Integration of domain-specific KGs with LLMs, augmented with neurosymbolic reasoning, has led to superior performance in forecasting consumer behavior and refining review rating predictions.

- **Digital Twins and Geospatial Data**: The Universal Digital Twin approach leverages dynamic KGs to simulate and integrate cross-domain data streams, relevant for applications in energy decarbonization and urban planning.

---

## Evaluation Metrics and Methodological Considerations

To quantify improvements in clarity, factuality, and logical reasoning, multiple evaluative frameworks are utilized:

- **Quantitative Metrics**: Benchmarks such as MRR, Hits@N, and F1-scores (observed in instance matching tasks) provide rigorous performance evaluations. Automated systems like LLM-KG-Bench offer RESTful and rule-based metrics to track syntax error correction and fact extraction in KG generation.

- **Qualitative Analyses**: Incorporating multi-objective frameworks, such as MORAL and user-driven evaluation schemes, provides insights into stakeholder satisfaction and systemic usability—integrating both numerical and human-feedback data.

- **Hybrid Reward Mechanisms**: Advanced RL frameworks combine potential-based advice with real-time human feedback. Studies, notably from the University of Washington using the FRESH framework, have demonstrated how reward shaping accelerates policy learning and enhances output credibility.

- **Declarative Evaluations**: Declarative languages and multi-paradigm programming paradigms further allow for systematic comparisons across diverse architectures, ensuring that both static and dynamic properties (e.g., scalability and semantic enrichment) are consistently measured.

---

## Advanced Techniques and Emerging Trends

Several advanced methodologies and emerging trends are pushing the boundaries of integrated LLM-KG systems:

- **Neurosymbolic Architectures**: The fusion of enterprise knowledge graphs with fine-tuned LLMs via ontological reasoning has been shown to reduce hallucinations and increase domain fidelity. This approach is further enhanced by integrating business-specific definitions directly into training routines.

- **Adaptive Sampling and Hyperparameter Tuning**: Adaptive sampling strategies in surrogate modeling have led to significant improvements in both accuracy and computational efficiency, as evidenced in spatial data and cybersecurity applications.

- **Modularization and Declarative Query Extensions**: Integrating modular KG approaches (e.g., through the use of specialized ontologies like DiCon and ifcOWL/BOT for BIM) provides robust methods to navigate heterogeneous data sources. Declarative systems like Deductive Application Language (DeAL) have outperformed distributed platforms in controlled benchmarks.

- **Feedback Automation and Composite Loss Functions**: Employing composite loss functions that balance quantitative metrics with qualitative human feedback has allowed systems to fine-tune reward functions dynamically, a critical advancement in hybrid RL and multi-criteria decision-making systems.

- **Syntactic and Semantic Optimization**: Techniques integrating classical methods like the Orthogonal Procrustes Analysis in KG embedding have reduced training time dramatically while decreasing the carbon footprint, emphasizing the importance of revisiting established models under modern computational conditions.

---

## Case Studies and Benchmarking Frameworks

Empirical case studies illustrate concrete benefits and challenges in real-world implementations:

- **Amazon Neptune and Legal Management Systems**: Real-world tests using EU Publications Office RDF datasets have benchmarked successive Neptune versions, demonstrating improvements in data loading, query response times, and update operations. Legal applications show that the fusion of automated and human-curated data can streamline search capabilities and support complex legal workflows.

- **LLM-KG-Bench Framework**: Presented at SEMANTICS 2023, this framework systematically evaluates LLM performance on knowledge graph tasks. It employs both automated evaluation and statistical visualization techniques to track performance on syntax correction, fact extraction, and dataset generation.

- **Industry-Specific Instance Matching**: Studies comparing holistic and pair-wise matching approaches (e.g., the VMI system and SiGMa) show significant speedups and improved precision. Such hybrid matching strategies have reduced computational complexity from quadratic to linear, offering scalable alignment across diverse KG datasets.

- **Enterprise Knowledge Graph (EKG) Use Cases**: In sectors ranging from healthcare to digital manufacturing, enterprise KGs provide a semantic backbone for linked data. These systems benefit from modular design and active preference elicitation frameworks that align multiple stakeholder needs while performing dynamic optimizations.

---

## Discussion, Limitations, and Future Research

The integration of LLMs, code, and knowledge graphs is promising, yet not without its challenges. Key discussion points include:

- **Scalability and Heterogeneity**: Integrating diverse data sources, ranging from legal documents to consumer data, requires robust frameworks that can handle scale and complexity. Future research should focus on optimization algorithms that merge local and global similarity measures while ensuring computational efficiency.

- **Domain-Specific Adaptation**: While generic models provide a baseline, domain-specific fine-tuning through enterprise knowledge graph integration and adaptive prompt engineering is critical. Emerging neurosymbolic architectures need to be assessed further on domain-specific benchmarks, particularly in dynamically changing industrial settings.

- **Evaluation Framework Standardization**: There is a pressing need for standardized evaluation metrics, especially in instance matching across heterogeneous knowledge graphs. Although frameworks like LLM-KG-Bench present promising methodologies, further work is required to balance quantitative and qualitative evaluation methods.

- **Integration of Declarative and Procedural Methods**: Bridging the gap between declarative programming paradigms and neural-based approaches remains a significant research endeavor. Initiatives that combine logic programming, constraint programming, and deep RL reward mechanisms are likely to produce more robust, adaptable systems in the near future.

- **Feedback and Adaptive Learning**: Incorporating continuous user feedback through automated systems (e.g., composite loss functions and reinforcement learning frameworks) is essential for maintaining system accuracy. Directions for future research include enhancing real-time adjustments and integrating multi-modal feedback mechanisms.

---

## Conclusion

The multi-dimensional integration of LLMs, code, and knowledge graphs represents a cutting-edge frontier for achieving enhanced clarity, improved factuality, and deeper logical reasoning. By uniting the generative strengths of LLMs with the structured, scalable nature of knowledge graphs and the precision offered by orchestrated code systems, the envisioned two-man band approach delivers a holistic solution for complex problem-solving. This interdisciplinary synergy, validated through benchmarks like LLM-KG-Bench and real-world deployments on platforms such as Amazon Neptune, underscores the significant potential of hybrid systems. 

Going forward, continuous improvements in adaptive sampling, multi-objective evaluation frameworks, and neurosymbolic architectures will further refine these integrations. Future research should target standardization of evaluation methods and explore deeper interactivity between automated feedback and declarative reasoning to drive the next generation of high-fidelity, scalable knowledge systems.

---

This report has synthesized learnings across a spectrum of advanced research areas, providing both a detailed roadmap for current implementations and a foundation for future explorations in the realm of integrated LLM, Code, and Knowledge Graph systems.

## Sources

- http://hdl.handle.net/1773/48178
- https://orcid.org/0000-0002-0606-0050
- https://www.scopus.com/inward/record.uri?eid=2-s2.0-84912544587&doi=10.1109%2fFUZZ-IEEE.2014.6891829&partnerID=40&md5=8048da1cace556e05435ee216837c830
- https://zenodo.org/record/3523969
- http://www.ict.csiro.au/staff/nathalie.colineau/publications/Paris-Colineau-Wilkinson-NLGeval2007.pdf
- https://hal-emse.ccsd.cnrs.fr/emse-04138834
- https://hal.science/hal-03132794v2/file/benchmark-v2.pdf
- http://www.cscjournals.org/csc/manuscript/Journals/IJBRM/volume2/Issue1/IJBRM-33.pdf
- http://liris.cnrs.fr/Documents/Liris-3382.pdf
- https://zenodo.org/record/7750212
- https://www.i3s.unice.fr/jfpc_2021/
- http://arxiv.org/pdf/1207.4525.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-206118
- http://hdl.handle.net/10.1371/journal.pone.0292126.g004
- https://zenodo.org/record/7919873
- https://dspace.kpfu.ru/xmlui/handle/net/162375
- https://pub.uni-bielefeld.de/record/1992597
- https://lirias.kuleuven.be/bitstream/123456789/325258/2/Postprint%202013-Monte-Carlo%20based%20uncertainty%20analysis%20-%20Sampling%20efficiency%20and%20sampling%20convergence.pdf
- http://dx.doi.org/10.2139/ssrn.2878950
- https://zenodo.org/record/6517844
- https://research.vu.nl/en/publications/922fa661-059e-43ed-bb88-dc10e0d02881
- http://hdl.handle.net/2077/62454
- https://zenodo.org/record/3596522
- https://hal.science/hal-00491560
- https://zenodo.org/record/3813905
- https://zenodo.org/record/8151856
- https://escholarship.org/uc/item/9qb0c0zx
- https://ojs.aaai.org/index.php/AAAI/article/view/7690
- https://zenodo.org/record/6522651
- https://figshare.com/articles/Benchmark_for_47M_DBpedia_based_dataset_on_4_triple_stores/5808333
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.433.4365
- http://hdl.handle.net/2117/91415
- https://escholarship.org/uc/item/86m762fq
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.3824
- http://publica.fraunhofer.de/documents/N-422396.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.6414
- https://zenodo.org/record/7447274
- http://publica.fraunhofer.de/documents/2004948776.html
- https://lirias.kuleuven.be/bitstream/123456789/528415/1/iclp%202015%20luc.pdf
- http://arxiv.org/abs/2311.06503
- http://hdl.handle.net/20.500.12566/938
- http://digital.library.unt.edu/ark:/67531/metadc283564/
- https://madoc.bib.uni-mannheim.de/61522/
- http://arxiv.org/abs/2204.09805
- https://zenodo.org/record/7916281
- http://hdl.handle.net/11390/860154
- https://zenodo.org/record/8186168
- http://people.oregonstate.edu/%7Ejudahk/pubs/AdviceInRL.pdf
- http://www.iaeme.com/MasterAdmin/UploadFolder/NEUROMARKETING+EXPLORING+THE+BRAIN+FOR+MEASURING+CONSUMER+BEHAVIOR/NEUROMARKETING+EXPLORING+THE+BRAIN+FOR+MEASURING+CONSUMER+BEHAVIOR.pdf
- https://doi.org/10.1016/j.jocs.2022.101603
- https://zenodo.org/record/5872552
- http://keg.cs.tsinghua.edu.cn/jietang/publications/KBS13-Li-et-al-large-instance.pdf
- https://digitalcommons.unl.edu/dissertations/AAI3258768
- http://arxiv.org/abs/2203.07490
- http://www.pds.ewi.tudelft.nl/~iosup/benchmarking-graph-proc14icpe-vision.pdf
- https://hal.archives-ouvertes.fr/hal-00517126
- http://arxiv.org/abs/2310.05499
- http://eprints.utm.my/id/eprint/87352/
- http://dx.doi.org/10.1016/j.procs.2015.08.446
- https://zenodo.org/record/4644577
- http://arxiv.org/abs/2309.02033
- https://research-explorer.ista.ac.at/record/18113
- https://hal.archives-ouvertes.fr/hal-01501276
- https://hdl.handle.net/10216/128959
- https://corescholar.libraries.wright.edu/etd_all/1954
- http://epm.sagepub.com/content/70/2/199.full.pdf
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-00200721
- http://anale.spiruharet.ro/economics/article/view/1250
- https://doi.org/10.1080/095373203000136024
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:0898122192901377/MAIN/application/pdf/e0fdd070dcf224c2a62f15473ae7eddd/main.pdf
- https://hec.hal.science/hal-03885355
- http://publica.fraunhofer.de/documents/N-481414.html
- http://publications.jrc.ec.europa.eu/repository/handle/JRC64877
- http://hdl.handle.net/2117/370674
- http://dx.doi.org/10.4230/TGDK.1.1.13
- http://hdl.handle.net/2066/76092
- https://ojs.aaai.org/index.php/AAAI/article/view/6012
- https://escholarship.org/uc/item/8pq2q37r
- https://juser.fz-juelich.de/record/820837
- https://zenodo.org/record/7804789
- https://zenodo.org/record/4912131
- http://repository.readscheme.org/ftp/papers/bristol/peralta-thesis.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-6622357234668258372
- http://arxiv.org/abs/2308.16622
- http://edoc.hu-berlin.de/18452/20718
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.6853
- https://hal-lirmm.ccsd.cnrs.fr/tel-01110342
- https://madoc.bib.uni-mannheim.de/61042
- https://zenodo.org/record/8254171
- https://hal.archives-ouvertes.fr/hal-01534282
- https://research.vu.nl/en/publications/c19efcd4-c636-40ba-9545-500610e03f20
- https://zenodo.org/record/6631971
- http://hdl.handle.net/20.500.11937/68747
- https://doaj.org/article/94aa4862cb6e44429dc2222443b6930c
- https://ojs.aaai.org/index.php/AAAI/article/view/6392
- http://debs2016.org
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.89.9358
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-338176
- https://research.vu.nl/en/publications/9b06bcfe-e27d-4e6c-92bc-b21669efdacb
- https://orcid.org/0000-0003-4386-8195
- https://zenodo.org/record/4268930
- https://zenodo.org/record/4720282
- http://cds.cern.ch/record/1041014
- http://ceur-ws.org/Vol-431/om2008_Tpaper4.pdf
- https://ict.csiro.au/staff/Cecile.Paris/distribution/inlg2006-Paris-final.pdf
- https://zenodo.org/record/8171405
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.9847
- http://hdl.handle.net/11858/00-001M-0000-0014-B7AB-E
- https://ueaeprints.uea.ac.uk/id/eprint/3616/
- https://zenodo.org/record/6538201
- http://hdl.handle.net/10945/66068
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.772
- http://hdl.handle.net/11567/237108
- https://doaj.org/article/357ae8efb8124b17a368a76fc4c24731
- http://eprints.utm.my/id/eprint/95366/
- https://repozitorij.efzg.unizg.hr/islandora/object/efzg:9266/datastream/PDF
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Bretones_Cassoli=3ABeatriz=3A=3A.html
- https://lup.lub.lu.se/record/8b3959ca-0fe2-41ca-a237-3246765b0daf
- https://zenodo.org/record/1256409
- http://webpages.iust.ac.ir/amiri/papers/A
- https://aaltodoc.aalto.fi/handle/123456789/109204
- https://zenodo.org/record/7921645
- https://hal.archives-ouvertes.fr/hal-01500750
- http://ceur-ws.org/Vol-1335/wflp2014_tutorial.pdf
- https://doaj.org/article/58980410f10242649309b2842497af63
- https://escholarship.org/uc/item/1jr9k84v
- https://zenodo.org/record/6517842
- http://hdl.handle.net/10197/9889
- https://anale.spiruharet.ro/economics/article/view/1250
- https://hal.science/hal-01534282
- https://zenodo.org/record/8118389
- https://hdl.handle.net/1721.1/136715
- https://doaj.org/article/4bf711266c5e4c0e86fb5bac4a897885
- https://zenodo.org/record/7829250
- https://zenodo.org/record/7228955
- https://ir.cwi.nl/pub/22257
- https://research.wur.nl/en/publications/utilizing-mobile-fnirs-to-investigate-neural-correlates-of-the-ta
- https://hal-emse.ccsd.cnrs.fr/emse-03109122
- http://hdl.handle.net/10.1184/r1/6576578.v1
- https://research.tue.nl/en/publications/d0550ce5-f019-431e-a7a4-a047c5935f7e
- http://publications.jrc.ec.europa.eu/repository/handle/JRC98050
- https://hal.archives-ouvertes.fr/hal-01356072
- http://etd.adm.unipi.it/theses/available/etd-08052021-191720/
- https://zenodo.org/record/2621996
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.7179
- http://www.journals.elsevier.com/pattern-recognition-letters/
- http://hdl.handle.net/10779/DRO/DU:20808886.v1
- http://www.ec.tuwien.ac.at/%7Eivona/papers/AdaptiveResourceConfiguration.pdf
- https://doaj.org/toc/1690-4524
- https://ageconsearch.umn.edu/record/59183/files/Weaver1.pdf
- https://www.tandfonline.com/doi/abs/10.1080/10454446.2014.1000445?journalCode=wfpm20 10.1080/10454446.2014.1000445
- http://www.utupub.fi/handle/10024/125668
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.6591
- https://hal.science/hal-01356072/document
- http://resolver.tudelft.nl/uuid:f80e69f0-716d-423a-8124-b834984b7fc5
- https://dspace.library.uu.nl/handle/1874/415008
- https://drops.dagstuhl.de/opus/volltexte/2022/16000/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.97.8979
- https://infocom2021.ieee-infocom.org/workshop-computer-and-networking-experimental-research-using-testbeds
- http://arxiv.org/abs/2209.09593
- https://ojs.aaai.org/index.php/AAAI/article/view/26495
- https://www.repository.cam.ac.uk/handle/1810/327763
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-16141
- http://hdl.handle.net/20.500.11897/412458
- http://ipcsit.com/vol5/85-ICCCM2011-C052.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.3830
- https://doaj.org/article/c7f321e7011e449d962e58d2f60e1e90
- http://hdl.handle.net/11573/1340442
- https://commons.allard.ubc.ca/theses/86
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Wirth=3AChristian=3A=3A.html
- https://hal.inria.fr/hal-03770004/document
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=44828
- https://aisel.aisnet.org/pacis2008/234
- https://lirias.kuleuven.be/handle/123456789/315320
- https://zenodo.org/record/7907584
- https://primo.bib.uni-mannheim.de/primo-explore/openurl?vid=MAN_UB&institution=MAN&url_ctx_val=&url_ctx_fmt=null&isSerivcesPage=true&sid=madocurl_ver=Z39.88-2004&rft_id=62491&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Adc&rft.title=Supervised+knowledge+aggregation+for+knowledge+graph+completion&rft.book_title=The+semantic+web%3A++19th+International+Conference%2C+ESWC+2022%2C+Hersonissos%2C+Crete%2C+Greece%2C+May+29-June+2%2C+2022+%3A+proceedings&rft.auinit=P&rft.aulast=Betz&rft.auinit=M&rft.aulast=Christian&rft.auinit=S&rft.aulast=Heiner&rft.editor=Groth%2C+Paul&rft.subject=004+Informatik&rft.division=30460&rft.publisher=Springer&rft.contributor=Groth%2C+Paul&rft.date=2022&rft.publication=Lecture+Notes+in+Computer+Science&rft.pagerange=74-92&rft.place_of_pub=Berlin+%5Bu.a.%5D&rft.type=Konferenzver%C3%B6ffentlichung&rft.relation=https%3A%2F%2Fmadoc.bib.uni-mannheim.de%2F62491%2F&rft.eprint_status=archive&rft.issn=0302-9743&rft.isbn=978-3-031-06980-2
- https://constellation.uqac.ca/id/eprint/6001/1/cpe.5746.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.4266
- http://hdl.handle.net/10400.22/20264
- https://zenodo.org/record/7696672
- https://orcid.org/0000-0003-2762-0050
- https://zenodo.org/record/7779522
- https://research.tilburguniversity.edu/en/publications/ea98daa9-081d-4a58-bbd0-ba12912ec9aa
- https://escholarship.org/uc/item/8sd320nz
- https://zenodo.org/record/7919405
- http://publications.jrc.ec.europa.eu/repository/handle/JRC6141
- https://zenodo.org/record/8250646
- http://hdl.handle.net/1721.1/99835
- https://doi.org/10.1177/13563890231204664
- https://hal.archives-ouvertes.fr/hal-03613558/file/A%20Methodology%20to%20Build%20Decision%20Analysis%20Tools.pdf
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/1147_Paper.pdf
- https://hal.archives-ouvertes.fr/hal-01437628
- https://lirias.kuleuven.be/handle/123456789/564497
- https://zenodo.org/record/6547684
- https://zenodo.org/record/7907462
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050915025818/MAIN/application/pdf/01a1503c504f78961cebfb8eca6b6df6/main.pdf
- https://hdl.handle.net/11311/1257038
- https://zenodo.org/record/6517834
- https://research.vu.nl/en/publications/f4c2294d-2bb6-422b-b192-e86078f68a6d
- https://doaj.org/article/e5a9c119590f42c8b5c9a6a0e7651375
- http://hdl.handle.net/11573/396709
- https://eprints.gla.ac.uk/272120/1/272120.pdf
- http://purl.utwente.nl/publications/62199
- https://research.vu.nl/en/publications/0d1e1de5-bed3-4ce4-b8a4-0761fd96e0c8
- http://www.loc.gov/mods/v3
- http://hdl.handle.net/1807/102319