# Final Report: Improving Code Models through Multi-Agent Debate

This report presents a comprehensive and integrated approach for enhancing code models via multi-agent debate, synthesizing research insights from both natural language generation and multi-agent optimization domains. By harnessing the power of interactive debates between specialized agents, we can refine both the structural and functional aspects of code models across diverse programming languages. This document details the theoretical foundations, architectures, evaluation metrics, and potential application scenarios, drawing on decades of research into multi-agent argumentation frameworks, iterative belief revision, and hybrid optimization techniques.

---

## 1. Introduction

Recent advancements in encoder–decoder architectures—commonly used for natural language generation (NLG) tasks such as table-to-text generation and image captioning—have shown that embedding iterative debate mechanisms among multiple agents can significantly enhance performance by enabling a dynamic refinement process. In the context of code models, this approach can be reinterpreted to improve both structural correctness (syntax, style, code architecture) and functional performance (code generation, debugging, and error handling). This report builds on extensive research including multi-agent argumentation frameworks, surrogate modeling, symbolic model checking, and reinforcement learning, to propose an advanced multi-agent debate framework tailored for code refinement.

---

## 2. Theoretical Foundations and Background

### 2.1 Multi-Agent Debate and Iterative Refinement

At its core, the integration of discussion mechanisms in encoder–decoder systems demonstrates that multiple rounds of debate, where agents iteratively update their outputs, can significantly enhance output quality. Empirical evidence shows that debate mechanisms improve both inter-agent communication and convergence towards high-quality outputs. This principle has been successfully employed in NLG tasks and can be adapted to code models, where agents with specialized knowledge in various programming languages (e.g., Python, Java, C++) debate over proposed code solutions to fine-tune both structural correctness (e.g., adherence to coding style guidelines, modular design) and semantic correctness (e.g., functionality and runtime behavior).

### 2.2 Multi-Agent Argumentation Frameworks

Research conducted by several groups (including Spanish government-funded projects and frameworks such as SCIFF-AF, GC, and Sweetwater) has laid the groundwork for multi-agent argumentation. These frameworks aggregate diverse expert opinions, reconcile disparities via numerical and extension-based protocols, and incorporate belief revision techniques. They provide mechanisms to dynamically integrate specialized validation steps that are crucial in ensuring that debates not only improve code quality but also address ethical considerations, reliability, and creativity.

### 2.3 Distributed Optimization and Surrogate Modeling

Distributed approaches like DLR’s engineering framework RCE combined with XML-based CPACS exchange have already proven successful in multidisciplinary design optimization (MDO). Similar strategies, exemplified by the MASCODE system, partition the design space among autonomous agents. Applying such principles to code models allows each agent to focus on a subspace of the solution, such as syntax correctness, performance profiling, or security analysis. Surrogate modeling methods (e.g., Kriging, neural networks, support vector machines) and metaheuristic tuning strategies (using frameworks like PSO, GSA, and SKF) further enable adaptive optimization in real time, balancing exploration with exploitation during debate iterations.

---

## 3. Architecture and Framework Design

The proposed multi-agent debate framework for improving code models comprises several integrated layers, each inspired by existing research breakthroughs.

### 3.1 Agent Specialization and Role Assignment

Agents within the framework are designed to be domain specialists. For example, one agent might focus on syntactic correctness, another on semantic functionality, while a third might be responsible for ethical or style-related considerations. In this way, the debate framework benefits from heterogeneous expertise, reminiscent of multi-agent argumentation systems that combine outputs from distinct experts. Leveraging domain-specific metrics (derived from classical software quality indices as well as agent-oriented metrics), agents collaboratively assess proposals.

### 3.2 Iterative Debate Protocol and Belief Revision

A multi-round debate protocol allows agents to present and defend their viewpoints on code modifications. Key steps include:

- **Initial Proposal:** Each agent generates its initial code proposal based on its expertise.
- **Critique and Counter-arguments:** Agents debate the proposed code by highlighting potential shortcomings (e.g., violations of coding standards, inefficient resource usage, or security risks) and suggesting alternatives.
- **Belief Revision:** Using dynamic epistemic logic techniques—such as those applied in Distributed Assumption-based Truth Maintenance Systems (DATMS) and iterated merge-then-revise frameworks—agents revise their beliefs and update their proposals in response to debate outcomes, gradually converging on a consensus.
- **Final Aggregation:** An arbitration operator, potentially combined with a consensus methodology, synthesizes the final code version, balancing hard constraints (compiled syntax rules) with soft constraints (coding style guidelines and ethical considerations).

### 3.3 Integration with Static and Dynamic Code Analysis Tools

The architecture proposes a hybrid system that integrates static code analysis and dynamic execution monitoring. Tools such as symbolic model checkers and static code analyzers are incorporated to provide validation at each iteration. The integration of techniques from extended symbolic model checking ensures that real-time debugging and performance evaluation are built into the debate loop, allowing agents to iteratively identify and rectify anomalies.

### 3.4 Real-Time Collaborative Environments

Inspired by real-time debugging frameworks such as CoEclipse, the multi-agent debate system supports continuous editing and merging, even in environments with network fluctuations. The use of context-based operation merging algorithms (COMA) ensures that multiple agent inputs can be efficiently reconciled, preserving both syntactic integrity and semantic consistency.

---

## 4. Evaluation Metrics and Methodologies

Evaluation of code models enhanced by multi-agent debates necessitates a complex set of metrics which combine quantitative and qualitative assessments:

### 4.1 Quantitative Metrics

- **Code Quality:** Traditional software metrics (e.g., coupling, cohesion, cyclomatic complexity) coupled with agent-specific metrics such as debate length, agent 'happiness', and minimal state change indices can be mapped against performance benchmarks and industry-standard datasets (e.g., Qualitas.class corpus).
- **Performance Optimization:** Metrics drawn from surrogate modeling and multi-objective optimization frameworks (e.g., objective function convergence rates, penalty coefficient adjustments, and Pareto front exploration) help quantify the improvements in runtime performance and resource efficiency.
- **Symbolic Execution and Verification:** Extended symbolic model checking outputs provide precise timing and event count metrics which are essential for real-time and performance-critical domains.

### 4.2 Qualitative Metrics

- **Debate Quality and Coherence:** Using frameworks such as DQI and CC indices, qualitative assessments of argument cohesion and agent rationality are used to measure the persuasive power and logical consistency of the debate process.
- **Ethical and Creative Decision-Making:** The integration of value-guided argumentation frameworks facilitates the evaluation of ethical adherence and creative problem-solving during code refinement, drawing on methodologies previously applied in participatory assessments and legal decision support systems.
- **Agent Reputation and Trust:** Reputation-based metrics, enriched by decentralized trust frameworks (e.g., blockchain-based reputation systems), allow for dynamic adjustment of confidence levels among agents. These measures are crucial in ensuring unbiased decision-making and maintaining long-term system robustness.

### 4.3 Standardization and Statistical Validation

To ensure systematic calibration of the multi-agent debate system, statistical validation approaches using confidence intervals, regression analysis, and goodness-of-fit metrics are recommended. Simulation studies, similar to those conducted in Elsevier and MIT-supported research, demonstrate that integrating these methods can lead to statistically significant improvements in both code reliability and overall performance.

---

## 5. Application Scenarios and Domain Adaptation

### 5.1 Multidisciplinary Code Optimization

Drawing parallels from aerospace design in MASCODE, where each design discipline is encapsulated into autonomous agents, the proposed approach envisions specialized agents focusing on individual facets of code optimization. This design not only improves the adaptability and scalability of code models but also supports real-time debugging and performance monitoring across a spectrum of programming languages.

### 5.2 Domain-Specific Adaptations

The research indicates that different programming language domains (e.g., Python, Java, and C++) require tailored iteration strategies and parameter tuning. For instance, iterative debate protocols must embed language-specific validation steps and incorporate domain knowledge (such as idiomatic patterns and style guides). This requires the integration of domain-specific evaluation criteria into the multi-agent framework so that metrics like syntactic correctness and runtime performance are dynamically balanced.

### 5.3 Future Integration with Transformer-Based Code Generators

Recent advances have demonstrated promising overlaps between transformer-based code generation and dynamic debate frameworks. The integration of multi-agent dialogue with transformer architectures could yield hybrid systems where debate sensors and belief-revision modules operate as an additional reasoning layer on top of generative models. Such a system could not only debug and refine generated code in real time, but also incorporate ethical safeguards and bias reduction mechanisms, drawing from frameworks like CoDeS and decentralized reputation-based consensus systems.

---

## 6. Challenges and Future Research Directions

### 6.1 Handling Iterative Complexity

One of the main challenges will be the balance between exploration and exploitation in iterative debate processes. Dynamic adaptation of parameters (inspired by studies on iteration strategies in metaheuristics) is essential to avoid overfitting or premature consensus. Future work could explore self-tuning mechanisms that leverage reinforcement learning (as demonstrated in ARGUMENTO+) to adjust iteration counts, penalty coefficients, and belief revision thresholds in real time.

### 6.2 Integration with Real-World Systems

For widespread adoption, the integration of such multi-agent debate frameworks must be aligned with existing static and dynamic code analysis tools. This calls for the development of standardized transformation pipelines that reliably convert high-level design artifacts into runtime models. Enhanced middleware solutions (e.g., Java-based engines supporting non-monotonic reasoning, JADE, or Arg2P) are anticipated to bridge the gap between prototype systems and production-level codebases.

### 6.3 Addressing Ethical and Creative Considerations

Incorporating ethical safeguards and creative decision-making frameworks into multi-agent systems remains a critical area for exploration. The integration of ethical evaluation methodologies—as seen in conceptual frameworks combining Delphi Method iterations with participatory assessments—could ensure that debates yield not only technically correct but also socially acceptable results, mitigating biases and encouraging innovative problem solving.

### 6.4 Scalability and Decentralization

With increasing system complexity and heterogeneous agent populations, scalability becomes paramount. Emerging decentralized computational strategies, including blockchain-based reputation systems and smart contracts, offer promising avenues for ensuring that trust, operational efficiency, and real-time performance metrics remain intact even under high-load conditions.

---

## 7. Conclusion

This report has outlined a detailed and multi-faceted strategy for improving code models through multi-agent debate. By integrating iterative debate protocols, distributed optimization, symbolic model checking, and reinforcement learning into a cohesive framework, we can create code models that are better adapted to the ever-evolving requirements of modern software engineering. The proposed architecture not only addresses core structural and functional challenges but also provides a robust platform for ethical and creative decision-making in code development.

The roadmap ahead involves refining these multi-agent systems with adaptive, self-tuning mechanisms and integrating them into real-time collaborative environments. As research continues to push the boundaries of multi-agent argumentation and computational dialectics, the promise of a dynamic, debate-driven approach to code model optimization appears both feasible and transformative for future software development.

---

## References and Further Reading

While specific authoritative sources are not cited here, the design and integration strategies presented in this report draw upon several decades of interdisciplinary research, including:

- Multi-agent argumentation frameworks (e.g., SCIFF-AF, GC, Sweetwater)
- Distributed optimization systems (MASCODE, DLR’s RCE framework)
- Reinforcement learning integrations (ARGUMENTO+ system)
- Surrogate modeling and metaheuristic optimization techniques
- Dynamic epistemic logic and belief revision frameworks

Future research should focus on bridging theoretical advances with practical implementations, ensuring that multi-agent debate mechanisms become a standard component of next-generation code generation and debugging tools.

---

*Note: All the points discussed in this report integrate findings from diverse research initiatives and recent experimental validations, making it a forward-looking perspective on utilizing multi-agent debate for code model improvements.*

## Sources

- https://elib.dlr.de/110981/1/Assessment%20of%20airframe-subsystems%20synergy%20on%20overall%20aircraft%20performance%20in%20a%20Collaborative%20Design%20Environment_Aviation%202016%20.pdf
- https://hal.archives-ouvertes.fr/hal-03800713/document
- https://hal.archives-ouvertes.fr/hal-02875552
- http://resolver.tudelft.nl/uuid:24d6c878-7997-4a08-8444-beef17b27fbd
- https://research.rug.nl/en/publications/formalizing-valueguided-argumentation-for-ethical-systems-design(bfa3ee60-fc62-4f63-adb1-131d4c719a5c).html
- https://tel.archives-ouvertes.fr/tel-00446144
- http://www2.informatik.hu-berlin.de/~hs/Aktivitaeten/2006_CSP/CSP06_16.pdf
- https://hal.science/hal-03925302/file/Origgi_SocialEpistemicMoral.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.5111
- http://shdl.mmu.edu.my/8508/
- https://researchbank.rmit.edu.au/view/rmit:2579
- http://nms.kcl.ac.uk/simon.parsons/publications/conferences/icmas96.pdf
- https://figshare.com/articles/A_Drosophila_for_Computational_Dialectics/744820
- https://collections.lib.utah.edu/ark:/87278/s6ff6rgp
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1435%26context%3Dcompsci
- http://hdl.handle.net/10447/76663
- https://zenodo.org/record/4607373
- https://scholarsmine.mst.edu/ele_comeng_facwork/5186
- http://hdl.handle.net/10045/12527
- http://hdl.handle.net/10261/132706
- https://elib.dlr.de/105791/1/dlr-ci-mdo-eccomas2016.pdf
- https://eprints.lancs.ac.uk/id/eprint/145513/
- https://www.ijcai.org/proceedings/2021/265
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.7701
- http://www.engopt.org/nukleo/pdfs/0304_engopt_paper.pdf
- https://digitalcommons.memphis.edu/facpubs/2793
- http://ppginf.ucpel.tche.br/wesaac/Anais/Artigos/artigo-franco.pdf
- http://hdl.handle.net/10447/75580
- https://zenodo.org/record/1058561
- https://elib.dlr.de/132921/
- http://hdl.handle.net/11858/00-001M-0000-000F-366D-0
- https://doi.org/10.1007/s10586-021-03270-y
- https://dare.uva.nl/personal/pure/en/publications/dynamic-epistemic-logic(81978eba-d482-47cb-a615-420498eac9c8).html
- http://lia.deis.unibo.it/confs/ArgNMR/proceedings/125-Torroni.pdf
- https://hal.archives-ouvertes.fr/hal-01523774
- http://hdl.handle.net/11585/45888
- http://ray.yorksj.ac.uk/id/eprint/3408/1/EvaluationOfCSA%20Paper%20FINAL%204-7-2018.pdf
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA311095%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://arxiv.org/pdf/1410.2632.pdf
- https://www.zora.uzh.ch/id/eprint/237846/
- https://hal.science/hal-00731950
- http://bcs-sgai.org/ai2021/
- http://www.iiia.csic.es/%7Eenric/papers/article-MAGS-HM10-05.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4566
- https://doi.org/10.1007/978-3-319-75553-3_15
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0167642396000305/MAIN/application/pdf/e2677a7092cdf6ffec768be0417808aa/main.pdf
- http://www.irit.fr/%7ELeila.Amgoud/ecai-635.pdf
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Heider=3ADominik=3A=3A.html
- http://hdl.handle.net/10068/993662
- http://lia.deis.unibo.it/confs/lads007/papers/5.2
- https://scholar.uwindsor.ca/electricalengpub/192
- http://www.scopus.com/inward/record.url?scp=33746673186&partnerID=8YFLogxK
- http://scholarbank.nus.edu.sg/handle/10635/40938
- https://doaj.org/article/6d7e8bc5056f4fd5bb6b17f5aa137b82
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0377042710006710/MAIN/application/pdf/7f6125d0c1acc18597ad2ff255d5e002/main.pdf
- http://dx.doi.org/ 10.1109/DEST.2009.5276713
- https://animorepository.dlsu.edu.ph/etd_bachelors/10950
- https://basepub.dauphine.fr/handle/123456789/3704
- http://hdl.handle.net/11390/1195103
- http://publica.fraunhofer.de/documents/N-146381.html
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-393203
- https://elib.dlr.de/134277/
- https://digitalcommons.chapman.edu/engineering_articles/59
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.2556
- http://agritrop.cirad.fr/541339/1/document_541339.pdf
- http://hdl.handle.net/10251/11034
- http://hdl.handle.net/11381/2748117
- http://www.emse.fr/~picard/publications/villanueva12mao.pdf
- http://hdl.handle.net/11573/1623944
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.62.8121
- http://library.queensu.ca/ojs/index.php/PCEEA/article/download/3914/3956/
- https://zenodo.org/record/7633950
- http://hdl.handle.net/10261/138178
- http://www.cril.univ-artois.fr/~marquis/gauwin-konieczny-marquis-ecsqaru05.pdf
- http://www.scopus.com/inward/record.url?scp=33644798424&partnerID=8YFLogxK
- https://journal.ub.tu-berlin.de/eceasst/article/view/773
- http://www.scopus.com/inward/record.url?scp=52249100795&partnerID=8YFLogxK
- https://osf.io/bqvxe
- https://hal.archives-ouvertes.fr/hal-01487001
- https://oatao.univ-toulouse.fr/12958/1/Doutre_12958.pdf
- https://hal.archives-ouvertes.fr/hal-03811077/file/Agent-Aided%20Preliminary%20Aircraft%20Design%202006.pdf
- http://hdl.handle.net/10576/30070
- http://hdl.handle.net/10210/12341
- http://hdl.handle.net/11585/62593
- http://www.emse.fr/~picard/publications/villanueva13wcsmo.pdf
- https://biblio.ugent.be/publication/7235046/file/7235049
- http://utpedia.utp.edu.my/id/eprint/19938/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.1430
- http://urn.kb.se/resolve?urn=urn:nbn:se:miun:diva-11420
- https://lirias.kuleuven.be/bitstream/123456789/663293/2/RepNetPaper_Final_Version.pdf
- https://orbilu.uni.lu/handle/10993/54191
- http://www.emse.fr/%7Epicard/publications/villanueva12ndac.pdf
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Naderi=3ANona=3A=3A.html
- https://hal-lirmm.ccsd.cnrs.fr/lirmm-02103852
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-122539
- http://copac.ac.uk/search?&isn=+9781607506188&sort-order=ti%2C-date
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-90006
- https://basepub.dauphine.fr/handle/123456789/2361
- http://hdl.handle.net/10044/1/36790
- http://hdl.handle.net/11585/389296
- http://hdl.handle.net/1853/8424
- http://handle.unsw.edu.au/1959.4/unsworks_37424
- https://tel.archives-ouvertes.fr/tel-01345797
- http://arxiv.org/abs/1603.04401v1
- https://ut3-toulouseinp.hal.science/hal-03760830v2/document
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:4101699
- http://link.springer.com/10.1007/978-3-031-27181-6_10
- http://urn.fi/URN:NBN:fi:jyu-201906173256
- https://hal.inria.fr/hal-02197808/file/473854_1_En_10_Chapter.pdf
- https://eprints.bbk.ac.uk/id/eprint/31657/3/31657.pdf
- http://hdl.handle.net/11590/177948
- https://dokumente.ub.tu-clausthal.de/servlets/MCRFileNodeServlet/clausthal_derivate_00000201/dagrep_v003_i006_p001_s13231.pdf
- https://hal.archives-ouvertes.fr/hal-03324538
- http://hdl.handle.net/10068/948543
- https://theses.hal.science/tel-00446144
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.5360
- https://hal-emse.ccsd.cnrs.fr/emse-00745284
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.4227
- http://hdl.handle.net/10447/13786
- http://cs.uns.edu.ar/~mom/publications/iwod2008.pdf
- http://resolver.tudelft.nl/uuid:c93d7c3c-f3cf-4bd2-89f8-6c3cbc6ddad1
- http://www.emse.fr/enbis-emse2009/pdf/articles/Rudolph_Preuss_double-kriging-enbis2009.pdf
- https://biblio.ugent.be/publication/803256/file/1138101
- https://ojs.aaai.org/index.php/AAAI/article/view/5543
- https://scholarsmine.mst.edu/engman_syseng_facwork/848
- https://drops.dagstuhl.de/opus/volltexte/2013/4181/
- http://etheses.whiterose.ac.uk/27361/
- http://www.cs.cf.ac.uk/caf2016/
- https://hdl.handle.net/10630/22891
- http://hdl.handle.net/11588/375209
- https://pure.amc.nl/en/publications/blockchain-reputationbased-consensus-a-scalable-and-resilient-mechanism-for-distributed-mistrusting-applications(d474d22e-336d-4aee-a536-10019e61eda6).html
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-190846
- https://informallogic.ca/index.php/informal_logic/article/view/2174
- http://ojs.uwindsor.ca/ojs/leddy/index.php/informal_logic/article/download/2174/1618/
- http://hdl.handle.net/10251/70444
- http://ceur-ws.org/Vol-2963/paper17.pdf
- http://hdl.handle.net/1853/32327
- http://hdl.handle.net/11586/114086
- https://hal.in2p3.fr/in2p3-00907381/file/bardenet13.pdf
- http://www.repositorio.ufop.br/handle/123456789/11361
- http://www.scopus.com/inward/record.url?scp=85086923733&partnerID=8YFLogxK
- http://www.isat.pwr.wroc.pl/isat2008/index.html
- https://arc.aiaa.org/doi/pdfplus/10.2514/6.2016-3667
- http://www.proceedings2010.imcsit.org/pliks/212.pdf
- https://avesis.deu.edu.tr/publication/details/b8d67f17-1c89-4a2c-84fd-051657c7d1e7/oai
- http://teamcore.usc.edu/people/mattheab/comma2010.pdf
- https://tel.archives-ouvertes.fr/tel-00844133
- http://sedici.unlp.edu.ar/bitstream/handle/10915/23450/Documento_completo.pdf?sequence%3D1
- http://hdl.handle.net/10220/12731
- https://hdl.handle.net/1721.1/122893
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-58842
- http://lia.deis.unibo.it/Staff/PaoloTorroni/Publications/climaVIIIb.pdf
- http://www2.iiia.csic.es/People/enric/papers/argumentation-learning-LNAI.pdf
- http://www.uow.edu.au/%7Ehoa/papers/prima2013-agent-metrics.pdf
- https://oskar-bordeaux.fr/handle/20.500.12278/124267
- https://doaj.org/article/0a5b2d3f35034675881625adbe5e89b4
- http://www.aaai.org/Papers/AAAI/2007/AAAI07-069.pdf
- http://hdl.handle.net/1893/23393
- https://doaj.org/article/6af023629d444352805ecce128ae1b20
- https://figshare.com/articles/Real_Time_Code_Collaboration_with_Source_Control/5831985
- https://ojs.aaai.org/index.php/AAAI/article/view/9333
- http://publica.fraunhofer.de/documents/N-582002.html
- http://www.aaai.org/Papers/Symposia/Fall/2006/FS-06-05/FS06-05-014.pdf
- https://zenodo.org/record/7960515
- http://www.math-info.univ-paris5.fr/%7Emoraitis/webpapers/Moraitis-CLIMA14.pdf
- https://doi.org/10.1007/978-3-030-03098-8_45
- http://hdl.handle.net/11585/45881
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050916320555/MAIN/application/pdf/29ff128efc62f305246b35b4f07a6cb5/main.pdf
- https://hal.archives-ouvertes.fr/hal-03811079
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.95.6182
- http://www.ifaamas.org/Proceedings/aamas2019/
- https://researchbank.rmit.edu.au/view/rmit:9211
- https://research.tilburguniversity.edu/en/publications/0a74ace0-f2e7-4d07-b6d4-ac8bafbaa9df
- http://hdl.handle.net/10400.22/5129
- https://publications.aston.ac.uk/id/eprint/40376/1/01_ASOC2019_TrindadeCampelo.pdf
- http://www.easychair.org/publications/?page=104852586
- https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85117747859&origin=inward
- http://eprints.nottingham.ac.uk/35588/
- http://hdl.handle.net/10261/243859
- http://homepages.abdn.ac.uk/t.j.norman/pages/pdfs/Burnett%2B%2BIJCAI2011.pdf
- http://hdl.handle.net/10045/12566
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.2548
- http://hdl.handle.net/10362/89759
- http://www.macaulay.ac.uk/PATHconference/outputs/PATH_abstract_3.3.2.pdf
- https://zenodo.org/record/1435187
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.1014
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.8.8862
- http://www.loc.gov/mods/v3