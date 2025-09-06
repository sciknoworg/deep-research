# Tree-of-Thought Prompting for Challenging Mathematical Proofs: A Comprehensive Exploration

## Abstract

This report presents an exhaustive review of tree-of-thought prompting applied to challenging mathematical proofs. It synthesizes research insights from automated learning in proof planning, human-oriented interactive systems, cognitive modeling, and neuro‐symbolic frameworks. The report discusses theoretical frameworks, algorithmic enhancements, and experimental validations that underscore the potential of tree-of-thought strategies for both automated theorem proving and enhanced human-in-the-loop exploratory proof processes. The integration of such methods into existing systems and the prospects for future development are also explored in detail.

---

## 1. Introduction

Mathematical proofs, especially those involving combinatorial, algebraic, infinitary, or other complex reasoning tasks, demand not only rigor but also dynamic exploration of multiple reasoning pathways. Tree-of-thought prompting represents an emerging strategy that systematically expands on traditional chain-of-thought methods by structuring proofs as branching, multi-step decision trees. This report delves into this approach by integrating diverse research insights and technical advances into a unified framework aimed at challenging mathematical proofs.

### 1.1 Motivation

Traditional proof planning systems have historically been augmented using rule-based and heuristic methods. However, recent advances in machine learning, reinforcement learning (RL), meta-level inference, and human cognitive modeling have ushered in new paradigms. The tree-of-thought framework promises to not only explore multiple reasoning trajectories but also operate as a meta-planner that dynamically manages trade-offs between computational overhead and decision accuracy.

### 1.2 Scope and Focus

The primary focus of this report is to synthesize prior learnings and propose a roadmap for incorporating tree-of-thought prompting into both automated theorem proving and human-guided exploratory proof systems. We address:

- **Target Proof Domains:** Exploring combinatorial, algebraic, and infinitary proofs amongst others.
- **Underlying Reasoning Processes:** Investigating the meta-reasoning and self-correction mechanisms, such as self-consistency decoding and metareasoning.
- **Integration Strategies:** Addressing how these methods can be incorporated both into automated theorem provers (e.g., HERBY, THEO, Ωmega) and into human-involved interactive proof environments.

---

## 2. Background: Automated Learning in Proof Planning

### 2.1 The Evolution of Proof Planning Systems

Automated learning in proof planning has evolved from static rule-based systems to hybrid frameworks that combine symbolic reasoning with machine learning. For instance, the CALCULEMUS community has demonstrated dynamic invocation of external theorem provers and computer algebra systems. These developments lay the groundwork for tree-of-thought strategies that benefit from data-driven heuristic triggers and dynamic tactic selection.

### 2.2 Hybrid Reasoning Frameworks

Recent research has developed hybrid frameworks that integrate symbolic assertions with direct semantic representations of examples using a resolution calculus. These frameworks address processing complexity and offer both soundness and completeness. They act as precursors to tree-of-thought prompting by framing ideas around the hierarchical decision-making process where multiple branches of proof can be evaluated concurrently.

### 2.3 Performance Profile Trees and Dyadic Decision Trees

Incorporation of performance profile trees and optimal dyadic decision trees into interactive systems has showcased robust data-driven deliberation control. Experiments in domains outside of pure theorem proving (e.g., collision-avoidance tasks) emphasize the need to balance between search depth and computational cost—a key consideration in tree-of-thought prompting.

---

## 3. Integrating Human-Oriented Interactive Systems

### 3.1 Meta-Information and Dynamic Reconstruction

Systems such as GETFOL and MetaPRL capture detailed meta-level data regarding proof states, conjectures, and tactic sequences. Encoding these branching thought processes as structured metadata supports both replay of successful proof paths and dynamic strategy adaptation. Such meta-information is pivotal when tree-of-thought methods are to be integrated into interactive proof environments where users navigate, expand, and transform proof trees.

### 3.2 Cognitive Load and Behavioral Data

Empirical studies employing eye-tracking and mouse-based exploration indices give insights into cognitive load during problem solving. Trees that adapt using cognitive feedback help in forming adaptive user interfaces in real-time proof systems. For instance, balancing fixation duration data with decision-making steps can fine-tune when a tree-search should terminate or branch further.

### 3.3 Digital Storytelling and the Role of Pedagogy

Digital Interactive Storytelling in Mathematics (DIST-M) and dialogical frameworks highlight the benefit of narrative and collaborative interactions in enhancing mathematical proof construction. Embedding tree-of-thought strategies in educational settings leverages guided exploration and structured peer feedback to maintain engagement and sensitize students to both symbolic and embodied reasoning.

---

## 4. Enhancing Automated Theorem Proving Through Tree-of-Thought Methods

### 4.1 Incorporating PoT and Self-Consistency Decoding

The Program of Thoughts (PoT) approach differentiates reasoning from computation by delegating calculations to an external executor. Experiments indicate an average 12% performance improvement over traditional chain-of-thought methods. Further integration with self-consistency decoding reduces hallucinations and enhances the logical coherence of proofs.

### 4.2 RL, MCTS, and Policy Gradient Approaches

Reinforcement Learning (RL) and Monte Carlo Tree Search (MCTS) pitfalls and successes have been studied extensively, as seen in TreeLine and PerfRL. Policy gradient methods, including Proximal Policy Optimization (PPO), modify the exploration strategy during tree search to optimize both reward functions and state-representations. This directly addresses trade-offs between proof search time and decision accuracy in complex combinatorial settings.

### 4.3 Applications in Non-Ground Reasoning

Automated provers such as HERBY, THEO, and Ωmega require modifications in their underlying logic calculi to incorporate non-ground reasoning and meta-level control. Tree-of-thought strategies necessitate extensions to existing inference rules, such as integrating open-loop control and performance profile trees, whereby stopping conditions are evaluated in tandem with semantic progress metrics.

---

## 5. Hybrid Architectures: From Neuro‐Symbolic Integration to Parallel Systems

### 5.1 Neuro‐Symbolic Systems and Tall’s Three-World Framework

Recent integrations of neuro‐symbolic architectures, which combine neural perception with symbolic logic, align with Tall’s three-world framework. By operationalizing embodied, symbolic, and conceptual representations, tree-of-thought methods can leverage both concrete computations and higher-level abstractions. This dual representation is essential when constructing proofs that involve both numerical and symbolic components.

### 5.2 ML4PG and Data-Driven Tactic Selection

Projects like ML4PG demonstrate the effective clustering of proof statistics such as goal shapes and tactic sequences. Data-mining techniques applied in these contexts provide evidence that a tree-of-thought framework could dynamically select and sequence tactics based on contextual clues as gleaned from historical proof data and real-time metareasoning outputs.

### 5.3 FPGA, Edge Computing, and Hardware/Software Co-Design

Recent research on FPGA edge computing (e.g., modifications to Intel Arria 10 GX and frameworks like ARTICo3) show that dynamic reprogrammability can support low-latency, high-throughput decision making. Such hardware innovations allow for the standalone execution of tree search algorithms, balancing computational efficiency with decision accuracy. When coupled with tree-of-thought methods, these systems can achieve near constant inference times even while navigating large decision trees.

---

## 6. Cognitive Insights and Empirical Studies

### 6.1 Eye-Movement and Microcognitive Monitoring

Studies utilizing eye-movement tracking underline the microcognitive processes underlying calculational reasoning and theorem proving. Integrating these findings into adaptive tree-of-thought systems can allow for real-time adjustments in reasoning strategies based on cognitive overload indicators, such as fixation duration and pupil diameter measurements.

### 6.2 Pedagogical Interventions and Collaborative Thinking

Longitudinal studies and randomized controlled experiments on higher-order cognitive strategy training illustrate the importance of tailored questioning and limit-confirming examples. These pedagogical interventions are essential to transition students from empirical, intuitive reasoning to formal proof construction. Tree-of-thought methods may act as a scaffolding platform that integrates expert-generated meta-data to guide student proof exploration.

### 6.3 Multi-Register Representations and Symbol Sense

Integrating verbal, algebraic, and anticipatory representations is crucial for developing a robust symbolic sense in mathematics. Research into hybrid representations has shown benefits in both early algebraic training and advanced proof systems. Tree-based representations naturally lend themselves to this multi-register paradigm, where each branch can represent distinct cognitive modalities used during proof construction.

---

## 7. Comparative Analysis and Trade-Offs

### 7.1 Speed–Accuracy Trade-Offs in Tree Search

Empirical analyses of tree-based search methods, including performance profile trees and dyadic decision trees, emphasize a notable speed–accuracy trade-off in reasoning systems. Deeper and more targeted searches tend to improve accuracy at the cost of increased computational time. Balancing these trade-offs is central to optimizing tree-of-thought methods, especially in dynamic environments where time is a critical factor.

### 7.2 Benchmarking and Quantitative Metrics

Current benchmarking platforms, such as IOHprofiler, set fixed-probability measures and Pareto layer analyses for capturing search trade-offs. While direct quantitative metrics for tree-of-thought versus traditional semantic tree methods remain underexplored, experimental evidence using datasets like GSM, AQuA, FinQA, and Coq projects confirms that leveraging tree-of-thought architectures can yield measurable performance improvements.

### 7.3 Algorithmic Adjustments and Deep Inference

Modifying deep inference with tailored interaction-depth schemes shows potential for reducing non-determinism and deriving exponentially shorter analytic proofs. Integrating these adjustments within a tree-of-thought framework allows proof systems to decouple reasoning from computation, thus fostering more streamlined, consistent deductive pathways.

---

## 8. Future Directions and Open Challenges

### 8.1 Integrating Metareasoning and Self-reflection

Incorporating metareasoning strategies— as highlighted by GETFOL and MetaPRL—can allow systems to reconfigure their search paradigms based on real-time assessments of partial proofs. Future work should focus on establishing normative criteria for meta-level tactic updating and dynamic re-planning, ensuring that tree-of-thought frameworks are not only adaptive but also self-reflective.

### 8.2 Extending Frameworks into Automated Environments

While interactive systems such as Theorema and Lambda-clam have demonstrated the benefits of manipulable proof trees, extending these benefits into fully automated theorem provers remains a critical challenge. Key research directions include modifying existing logic calculi (e.g., Model Evolution Calculus, DPLL-based methods) to more seamlessly integrate dynamic branch tracking and external computation delegations.

### 8.3 Leveraging Cross-Disciplinary Cognitive and Hardware Advances

Explorations in neuro-symbolic integration, advanced FPGA-based accelerations, and embedded cognitive data are promising areas that merit further exploration. The convergence of hardware/software co-design, eye-tracking metrics, and deep algorithmic modifications provides a rich interdisciplinary research landscape poised to revolutionize proof planning.

### 8.4 Speculative Extensions: Beyond Traditional Frameworks

Speculatively, future tree-of-thought systems might integrate dynamically reconfigurable reinforcement learning agents with introspective revision mechanisms to mimic human-like hypothesis testing and error correction. These adaptive systems could potentially extend the boundaries of current AI proof systems, making them more resilient to fallacies and more capable of generating novel, hybrid reasoning strategies.

---

## 9. Conclusion

Tree-of-thought prompting presents a transformative approach to tackling challenging mathematical proofs. By bridging machine learning, automated theorem proving, and cognitive insights, these systems offer a pathway to more robust, transparent, and adaptive proof strategies. The integration of hybrid methods, multi-modal representations, reinforcement learning techniques, and dynamic piecewise reasoning not only enhances the accuracy of automated proofs but also enriches human-in-the-loop exploratory processes.

The future of mathematical proof construction lies in systems that can strategically navigate complex decision spaces, dynamically balance computation with accuracy, and harness cognitive and pedagogical insights for enriched learning and discovery. Our examination underscores the need for interdisciplinary research and innovative algorithmic designs that collectively push the boundaries of what is achievable in automated formal reasoning.

---

## References

While this report synthesizes insights from multiple research studies and community-driven explorations (e.g., CALCULEMUS, ML4PG, Theorema, HERBY, and MetaPRL among others), the ideas are presented integratively to elucidate pathways for future work in tree-of-thought prompting for challenging mathematical proofs.

*Note: This report incorporates data and trends reported in diverse studies, underscoring prospective paths and exploratory research in this evolving domain.*

## Sources

- https://youtu.be/ydp96LQOYE0?t=1029
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877042815001962/MAIN/application/pdf/e19274e47a51831e8e00dbe3e8dd5e61/main.pdf
- http://philsci-archive.pitt.edu/19681/
- https://resolver.caltech.edu/CaltechAUTHORS:20141021-080525961
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.6311
- https://discovery.ucl.ac.uk/id/eprint/10117328/1/1912.10824v1.pdf
- https://doi.org/10.13016/jbi5-wwmc
- http://cds.cern.ch/record/2006148
- https://digitalcommons.usf.edu/context/books/article/1141/type/native/viewcontent
- https://hal.science/hal-03288846
- https://dl.acm.org/doi/10.1145/3531073.3534493
- https://inria.hal.science/hal-01900891/file/hapop2018.pdf
- https://discovery.ucl.ac.uk/id/eprint/10038400/1/Barber_7120-thinking-fast-and-slow-with-deep-learning-and-tree-search.pdf
- https://escholarship.org/uc/item/8tm550mr
- https://hal.inria.fr/hal-00937009
- https://www.intechopen.com/books/9963
- https://dx.doi.org/10.1109/CDC.2015.7402937
- http://andrius.velykis.lt/publications/FreitasJVW14.pdf
- https://hira.hope.ac.uk/id/eprint/4021/
- http://hdl.handle.net/11591/427819
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0747717185710127/MAIN/application/pdf/99048a27c7ee27ae055919c3fdff5906/main.pdf
- http://amslaurea.unibo.it/view/cds/CDS8614/
- https://research.vu.nl/en/publications/48791af1-c3f8-4fb6-82bd-02f76cb66688
- http://www.doc.ic.ac.uk/%7Eshm/Papers/typemilproof.pdf
- https://hdl.handle.net/2027.42/171438
- http://hdl.handle.net/10.1371/journal.pcbi.1006827
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27701
- http://www.aaai.org/Papers/Symposia/Spring/2006/SS-06-02/SS06-02-013.pdf
- https://hdl.handle.net/10067/2015970151162165141
- http://hdl.handle.net/11585/781387
- https://doi.org/10.1007/978-3-319-43473-5
- https://doi.org/10.1007/978-981-16-1361-6_9
- http://hdl.handle.net/10.1371/journal.pone.0277862.t007
- http://ir.uiowa.edu/cgi/viewcontent.cgi?article%3D1546%26context%3Detd
- http://urn.fi/urn:nbn:fi-fe2020120198829
- https://scholarship.claremont.edu/hmc_theses/224
- https://hdl.handle.net/10877/9856
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0747717197901759/MAIN/application/pdf/f6fc3db01566ee901a0ad8f0aefbb53e/main.pdf
- http://techreports.library.cornell.edu:8081/Dienst/UI/1.0/Display/cul.cs/TR99-1733
- https://zenodo.org/record/8124296
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.8027
- http://profs.sci.univr.it/~bonacina/analysis.html
- http://hdl.handle.net/2142/101086
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-220364
- http://hdl.handle.net/1885/66281
- http://hdl.handle.net/10044/1/13999
- http://www.michaelbeeson.com/research/papers/ProofAndComputation.pdf
- http://dx.doi.org/10.1007/BFb0000056
- https://doaj.org/article/3dff8440bddb4c299f2ade1f819b2d7f
- https://zenodo.org/record/4570733
- https://hal.archives-ouvertes.fr/hal-03745430/file/TWG25_08_Gregorio.pdf
- http://hdl.handle.net/10044/1/104353
- http://arxiv.org/abs/2210.01240
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.3165
- https://zenodo.org/record/7765283
- http://dx.doi.org/10.1007/978-3-319-30526-4_12
- http://homepages.lboro.ac.uk/~mamji/files/pme2006.pdf
- http://hdl.handle.net/20.500.12380/307923
- http://arxiv.org/pdf/1003.4802.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0004370207001968/MAIN/application/pdf/741bd783ea0fbfd5b784fa49506f7beb/main.pdf
- http://publikationen.ub.uni-frankfurt.de/files/59160/SSRN-id3872711.pdf
- https://www.aaai.org/Papers/AAAI/2004/AAAI04-012.pdf
- http://econ.haifa.ac.il/%7Eadmiller/Benchmarking.pdf
- https://zenodo.org/record/8121219
- http://arxiv.org/abs/2211.12588
- http://eprints.usm.my/36838/
- https://research.tue.nl/nl/publications/f031337a-ba93-497b-90ba-eaa10769b39c
- http://publications.lib.chalmers.se/records/fulltext/155931.pdf
- http://timrickard.com/Papers/Rickard2004.pdf
- http://hdl.handle.net/11380/641242
- https://hdl.handle.net/2152/121237
- http://hdl.handle.net/10068/997942
- https://doi.org/10.4204/EPTCS.118.2
- https://hal.archives-ouvertes.fr/hal-00484666
- http://hdl.handle.net/11311/1204072
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.2620
- https://doaj.org/article/d0bb5f719be242cca47643fda60fd51e
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.8676
- http://www.cs.vu.nl/~tbosse/papers/ICCM07-interpret-final.pdf
- http://hdl.handle.net/1773/43349
- http://hdl.rutgers.edu/1782.1/rucore10001500001.ETD.000067517
- https://scholarsbank.uoregon.edu/xmlui/handle/1794/27079
- https://biblio.ugent.be/publication/6935979/file/6935980
- http://hdl.handle.net/10315/32339
- https://discovery.ucl.ac.uk/id/eprint/10118849/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.9122
- http://www.biokids.umich.edu/papers/songerkelceygotwalsaera4.09.pdf
- https://digitalcommons.cwu.edu/math/93
- https://hal.inria.fr/inria-00332718
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.7908
- https://hal.archives-ouvertes.fr/hal-01280547
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.5022
- http://arxiv.org/abs/2201.09104
- https://doaj.org/article/cfd6089d4104413787e743dddb10d8e7
- http://www.iro.umontreal.ca/~sahraouh/qaoose/papers/Klemola.pdf
- http://hdl.handle.net/10447/512105
- http://hdl.handle.net/2078.1/266164
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0004370299000764/MAIN/application/pdf/1e7b645c919d4205f421bd5224a2060c/main.pdf
- http://www.scopus.com/inward/record.url?scp=78650348033&partnerID=8YFLogxK
- http://hdl.handle.net/11562/20905
- https://hal.inria.fr/hal-02273713
- http://statmath.wu.ac.at/~zeileis/papers/GfKl-2004a.pdf
- https://doaj.org/article/c8584d1fbaa74e6bb47141c7e3b3b204
- http://domino.mpi-inf.mpg.de/internet/reports.nsf/NumberView/94-233
- http://www.ischool.drexel.edu/faculty/mkhoo/docs/11_drk12.pdf
- http://hdl.handle.net/11380/596156
- http://hdl.handle.net/1959.14/1117011
- http://hdl.handle.net/2066/175341
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.8416
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.116
- https://philpapers.org/rec/MIRUTF
- https://hdl.handle.net/1721.1/139305
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1663%26context%3Dcis_reports
- http://www.coli.uni-saarland.de/publikationen/softcopies/Schulte:1997:PCI.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.6952
- http://hdl.handle.net/11386/4783683
- http://cogprints.org/319/1/computation.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.2313
- http://hdl.handle.net/10150/186576
- https://ojs.aaai.org/index.php/SOCS/article/view/18179
- https://hal.inria.fr/hal-01840583
- http://www.easy-hub.org/hub/workshops/um2005/doc/Bednarik.pdf
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1699%26context%3Dcis_reports
- https://scholarcommons.scu.edu/cseng_senior/228
- http://hdl.handle.net/11591/456797
- http://eprints.gla.ac.uk/view/author/10424.html
- http://page.mi.fu-berlin.de/cbenzmueller/papers/W6.pdf
- www.cerme12.org
- http://funes.uniandes.edu.co/24013/1/Healy2000Blurring.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066104002853/MAIN/application/pdf/c54e0d98420a3874cc6ecb288030baa0/main.pdf
- http://nbn-resolving.de/urn:nbn:de:bsz:352-0-399762
- http://hdl.handle.net/1842/8115
- http://ethanfast.com/resources/deduceit-paper.pdf
- http://hdl.handle.net/2060/20000109821
- http://hdl.handle.net/11571/129844
- https://kluedo.ub.uni-kl.de/frontdoor/index/index/docId/350
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0743106684900281/MAIN/application/pdf/c904d650b6f281f0ef060542048a4a4b/main.pdf
- https://doaj.org/article/9a601605c8ff47bda37b160de8661602
- http://hdl.handle.net/11386/4727074
- http://profs.sci.univr.it/~bonacina
- http://publica.fraunhofer.de/documents/N-59430.html
- https://hal.science/hal-04303153/document
- http://repository.uin-malang.ac.id/1740/7/1740.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.8424
- https://philpapers.org/rec/VENFTO
- http://www.sato.kuis.kyoto-u.ac.jp/~masahiko/papers/nf.pdf
- http://hdl.handle.net/2027.42/63536
- http://hdl.handle.net/11368/2301426
- https://hal.sorbonne-universite.fr/hal-02179607
- http://hdl.handle.net/11584/326550
- http://hdl.handle.net/11577/2611844
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877042810021622/MAIN/application/pdf/43c233ae8f967cdaba53ab54123d4cc0/main.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/21333
- http://hdl.handle.net/10230/55354
- http://arxiv.org/abs/2203.04857
- http://arxiv.org/pdf/1212.2287.pdf
- http://hdl.handle.net/11562/243780
- http://proceedings.mlr.press/v97/yang19a.html
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0195669807001783/MAIN/application/pdf/d2eea7d828614dcd090c7ccfcf6bfd88/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.7840
- http://arxiv.org/abs/2206.06965
- http://arxiv.org/abs/2311.01460
- http://pqdtopen.proquest.com/#viewpdf?dispub=28089396
- http://www.cl.cam.ac.uk/~lp15/papers/Arith/SNC2014-invited.pdf
- http://hdl.handle.net/11577/2686882
- https://hdl.handle.net/11573/1698263
- https://hal.archives-ouvertes.fr/hal-02423496/document
- http://w3.isis.vanderbilt.edu/publications/archive/Scott_JM_9_11_2004_A_HW_SW_Co.pdf
- https://nbn-resolving.org/urn:nbn:de:hbz:386-kluedo-3149
- https://zenodo.org/record/8136722
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.5576
- http://edoc.ub.uni-muenchen.de/12990/1/Eugster_Manuel_J_A.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.1830
- https://hal.inria.fr/inria-00075450
- http://www.scopus.com/home.url)
- http://dx.doi.org/10.22028/D291-25745
- http://www.scopus.com/inward/record.url?scp=84866392001&partnerID=8YFLogxK
- https://hal.archives-ouvertes.fr/hal-01865647/document
- http://homepages.warwick.ac.uk/staff/David.Tall/pdfs/dot2006g-mejia-tall.pdf
- https://www.inf.ed.ac.uk/publications/online/0954.pdf
- http://hdl.handle.net/2286/R.I.53286
- https://www.aaai.org/Papers/AAAI/1999/AAAI99-041.pdf
- http://hdl.handle.net/11571/261103
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.84.5360
- http://hdl.handle.net/11858/00-001M-0000-0023-CF13-D
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1660%26context%3Dcis_reports
- http://arxiv.org/abs/2201.11903
- https://doaj.org/article/135561a611ec4c30b64490accbdd1264
- https://hal.archives-ouvertes.fr/hal-01289344
- https://lmcs.episciences.org/1089
- http://hdl.rutgers.edu/1782.2/rucore10001600001.ETD.000051358
- https://escholarship.org/uc/item/6607r8tt
- http://ir.uiowa.edu/cgi/viewcontent.cgi?article%3D5471%26context%3Detd
- http://zaguan.unizar.es/record/89558
- http://techreports.library.cornell.edu:8081/Dienst/UI/1.0/Display/cul.cs/TR98-1680
- https://doaj.org/article/14fee03e4983400b993bcb0bd2c0e395
- http://hdl.handle.net/11386/4747463
- http://dx.doi.org/10.22028/D291-40440
- http://dx.doi.org/10.22028/D291-40245
- https://doaj.org/article/95e81689a501453cab804bdcf5c4ccd7
- http://www.florisbex.com/papers/lpr11.pdf
- https://hal.inria.fr/inria-00098603
- http://staff.computing.dundee.ac.uk/katya/ML4PG/ML4PG.pdf
- https://zenodo.org/record/8118487
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27706
- https://www.researchgate.net/profile/Vasily_Moshnyaga/publication/224086710_Algorithm_Optimizations_for_Low-Complexity_Eye_Tracking/links/09e4150da7b8f74f17000000.pdf
- https://doaj.org/toc/1424-8220
- http://publica.fraunhofer.de/documents/N-34883.html
- https://orbilu.uni.lu/handle/10993/54472