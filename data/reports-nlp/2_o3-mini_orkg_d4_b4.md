# Final Report on Autoprompting: Generating Diverse Few-Shot Examples for Any Application

## Table of Contents

1. [Introduction](#introduction)
2. [Theoretical Foundations and Multi-Fidelity Approaches](#theoretical-foundations)
3. [Feedback-Driven and Iterative Example Generation](#feedback-driven-generation)
4. [Hybrid Strategies and Adaptive Architectures](#hybrid-strategies)
5. [Evaluation Frameworks and Comprehensive Metrics](#evaluation-frameworks)
6. [Case Studies, Practical Implementations, and Industrial Insights](#case-studies)
7. [Future Directions and Concluding Remarks](#conclusion)

---

## 1. Introduction

Autoprompting is emerging as a critical methodology in generating diverse, few-shot examples that can be adapted for myriad applications across domains such as natural language processing, computer vision, and multi-modal learning systems. The concept centers on synthesizing a small set of examples that are not only representative of the underlying task but also sufficiently diverse to cover a wide array of potential queries, thereby improving robustness and generalization. This report provides a detailed assessment of autoprompting, drawing on a vast body of research that spans derivative‐free optimization, iterative feedback, hybrid algorithmic strategies, and dynamic evaluation frameworks.

Key motivations for this approach include:

- **Data Sparsity:** In real-world scenarios, especially in few-shot learning settings, annotated data is limited. Autoprompting aims to bridge this gap by generating relevant, diversified data points.
- **Adaptability:** The techniques discussed enable prompt generation to be refined dynamically, facilitating both theoretical consistency and pragmatic applicability.
- **Evaluation Rigor:** A dual focus on qualitative and quantitative performance metrics ensures that both fidelity and diversity are directly optimized.

---

## 2. Theoretical Foundations and Multi-Fidelity Approaches

### 2.1 Derivative-Free Optimization via Transfer Series Expansion (TSE)

A central theme in recent literature is the use of **Multi-Fidelity Evaluation** combined with **Transfer Series Expansion (TSE)**. TSE leverages a large number of low-fidelity evaluations—potentially drawn from smaller datasets or down-scaled tasks—and then corrects these evaluations through a linear combination of base predictors. This method is especially useful in hyperparameter tuning in AutoML scenarios where the cost of high-fidelity evaluations is prohibitive. The advantages of TSE include:

- **Acceleration of Hyper-Parameter Tuning:** By harnessing lower-order approximations and applying corrections, tuning processes become derivative‐free and computationally efficient.
- **Scalability Across Tasks:** TSE’s ability to correct for bias in low-fidelity models makes it applicable when designing autoprompting pipelines that must function across heterogeneous data environments.

### 2.2 Theoretical Runtime Analyses and Adaptive Strategies

The incorporation of theoretical runtime analyses, such as those employing fuzzy logic controllers and one-step variation techniques, offers rigorous insights into population management in high-dimensional search spaces. These methods underscore the importance of adaptive parameter control and dynamic diversity enhancement. Such approaches ensure:

- **Balanced Exploration and Exploitation:** Adaptive mutation schemes and natural evolution strategies provide mechanisms to avoid premature convergence while exploring the solution space.
- **Convergence Guarantees:** Through mathematical rigor, these methods pave the way for optimizing multi-objective functions, ensuring timely discovery of robust prompt examples.

---

## 3. Feedback-Driven and Iterative Example Generation

### 3.1 Iterative Refinement Through Dynamic Feedback Loops

Empirical research shows that incorporating iterative feedback is crucial to generating diverse and high-fidelity examples. For instance, systems utilizing iterative, feedback-driven generation in Excel and domain-independent programming environments have demonstrated the following benefits:

- **Dynamic Adjustment:** User-guided example synthesis allows the system to learn from its mistakes and adjust generation strategies in real-time.
- **Enhanced Relevance:** By continuously integrating user feedback and adaptive signals, the generated prompts remain contextually rich and representative of the target application domains.

### 3.2 Proactive Adaptation and Prompt Consistency Regularization

Recent studies have showcased methods involving prompt consistency regularization where multiple natural language prompts are administered along with unlabeled data. These strategies improve zero-shot performance by ensuring that the system’s responses remain coherent across different context injections. The integration of fine-tuning with transfer learning further bolsters sample quality, resulting in notable accuracy improvements in both text and visual domains.

---

## 4. Hybrid Strategies and Adaptive Architectures

### 4.1 Hybrid Ensemble and HyperPrompt Strategies

A number of hybrid approaches are now dominating the landscape by merging domain-specific tactics with robust adaptive models:

- **Prompt-Augmented Linear Probing (PALP):** PALP combines the simplicity of linear probing with the structural strengths of in-context learning. This method significantly narrows the performance gap between few-shot learning and full fine-tuning, making it highly attractive in environments with limited data.

- **HyperPrompt via HyperNetworks:** This paradigm utilizes hypernetworks to generate task-specific hyper-prompts while adding only marginal overhead (e.g., 0.14% additional parameters). Results on benchmarks such as GLUE and SuperGLUE validate its efficacy, suggesting promising applications across multi-modal tasks.

### 4.2 Dynamic Composition and AutoML Integration

Beyond hypernetwork-driven approaches, adaptive evolutionary frameworks (e.g., derandomised self‐adaptive mutation schemes and natural evolution strategies) highlight the potential of dynamically adjusting prompt generation strategies. These frameworks are designed to:

- **Support Multi-Objective Optimization:** By balancing contradictory objectives (e.g., model sparsity versus classification accuracy), it is possible to generate a wide array of prompt examples that are both diverse and high fidelity.
- **Integrate into AutoML Pipelines:** AutoML frameworks are rapidly evolving to incorporate dynamic evaluations and online adaptation strategies, ensuring that autoprompting systems can adjust on-the-fly to non-stationary data environments and concept drift.

### 4.3 Middleware and Distributed Architectures

The deployment of context-aware middleware and plugin-based architectures (such as those used in Eclipse or Mesos frameworks) has opened up new avenues for integrating autoprompting modules with existing software systems. These architectures facilitate:

- **Real-Time Adaptation:** Dynamic resource scaling and decentralized decision-making enable systems to maintain high operational robustness, even under changing conditions.
- **Cross-Domain Applicability:** The design principles emerging from IoT systems, mobile pervasive frameworks, and adaptive smart home architectures demonstrate that autoprompting systems can be tailored to a wide range of application domains.

---

## 5. Evaluation Frameworks and Comprehensive Metrics

### 5.1 Dual Metrics and Domain-Agnostic Assessment

Comprehensive performance evaluation in autoprompting goes beyond single-metric assessments. Effective frameworks incorporate:

- **Dual Evaluation Metrics:** These include both qualitative aspects such as fault detection capability and quantitative measures like test execution times. Such metrics were successfully applied in domains ranging from behavioral response tests to automated oracles.

- **Three-Dimensional Evaluation Models:** A domain-agnostic framework defined by α-Precision, β-Recall, and Authenticity has been proposed. This structure unifies classical statistical divergence measures with binary classification at sample level, ensuring that fidelity, diversity, and generalization are all fairly evaluated.

### 5.2 Performance Monitoring and Adaptive Profiling

Advanced profiling and performance monitoring tools, like input-sensitive profiling methods and auto-profiling techniques seen in OSCAR-P, are critical. Their benefits include:

- **Uncovering Asymptotic Bottlenecks:** Tools that aggregate performance costs relative to input sizes using statistical curve fitting are crucial for identifying workload-dependent inefficiencies.
- **Integration with AutoML-like Pipelines:** Such profiling methods can be adapted to autoprompting systems, facilitating both theoretical evaluation and real-world performance measurement through dynamic test scenarios.

### 5.3 Quantitative and Qualitative Synergy

Benchmarks that compare both infrastructure-level and application-level metrics (ranging from CPU overhead, runtime behavior, to error codes and APM metrics) reveal that a composite evaluation framework is essential. Approaches that have merged strategies—like perturbation-based regularizers in prompt tuning—demonstrate measurable improvements in test accuracy and stability (e.g., +2.34% on FewGLUE), thereby serving as a blueprint for further system enhancements in autoprompting.

---

## 6. Case Studies, Practical Implementations, and Industrial Insights

### 6.1 Industrial Deployments and Real-World Testing

Industrial case studies, such as those undertaken by Tobii Technology for Tobii Studio, exemplify how extended automated testing scripts can capture non-functional properties like long-term CPU performance, hardware stress, and runtime behavior. These case studies provide a practical lens for evaluating autoprompting systems in operational conditions.

### 6.2 AutoML and Dynamic Reconfiguration

Systems like AutoPrognosis, AutoGOAL, and extended Auto-Sklearn pipelines have set precedents by dynamically reconfiguring models with online adaptation strategies. In particular, the integration of concept drift detectors, asynchronous genetic programing, and successive halving methods offers valuable lessons for ensuring that autoprompting systems remain effective even in evolving data contexts.

### 6.3 Domain-Specific Evaluations and Cross-Modal Tasks

Research in cross-modal tasks (e.g., text-to-3D synthesis using Score Distillation Sampling) has shifted evaluation metrics from singular fidelity measures toward hybrid approaches that encompass both perceptual fidelity and categorical diversity. Such case studies reinforce the need for autoprompting systems that can seamlessly integrate diverse data modalities, thereby making them highly versatile across different application sectors.

---

## 7. Future Directions and Concluding Remarks

### 7.1 Evolving Architectures and Anticipated Research Trends

As we look forward, several emerging trends are likely to shape the future of autoprompting:

- **Deeper Integration with Reinforcement Learning (RL):** Distributed RL techniques, particularly those applied to sensor networks and mobile systems, will likely be integrated more deeply into autoprompting, enabling real-time, decentralized decision-making that improves prompt diversity and quality.
- **Refinement of Hybrid Approaches:** Combining hypernetwork-driven methods with perturbation-based regularizers and hybrid ensemble strategies will be essential in creating systems that are both robust and adaptable. Efforts reminiscent of HyperPrompt and Structured Prompt Tuning indicate promising avenues.
- **Standardization of Evaluation Frameworks:** With frameworks emerging that reconcile the differences between structural continuity, contextual fidelity, and dynamic adaptation, future research will focus on standardizing unified metrics. These metrics will likely incorporate elements from domain-agnostic evaluation (α-Precision, β-Recall, Authenticity) to cross-modal, application-specific assessments.

### 7.2 Summative Perspective

In summary, the research accumulated over recent studies provides a robust foundation for designing autoprompting systems that can generate diverse few-shot examples across any application domain. By harnessing methods such as multi-fidelity evaluations with TSE, iterative example generation driven by dynamic feedback, and hybrid adaptive strategies, we are poised to bridge critical gaps in data sparsity and model adaptability.

The dual emphasis on theoretical rigor and practical responsiveness ensures that autoprompting is not only theoretically sound but also practically viable. Additionally, advanced profiling and comprehensive test automation frameworks offer promising avenues for future improvements and standardizations that can further refine these techniques.

---

## Concluding Remarks

Autoprompting represents a significant step forward in the realm of few-shot learning and automated data generation. Its inherent synergy of adaptive strategies, feedback loops, and hybrid evaluation frameworks equips it to handle the multi-faceted challenges of modern AI deployments—from high-dimensional optimization scenarios to domain-specific implementations and dynamic operational environments.

As the field continues to evolve, it is essential that we harness both the theoretical and empirical insights presented here, driving innovations that are both efficient and versatile. The integration of these diverse methodologies will not only yield robust, dynamic autoprompting systems but also pave the way for future cross-disciplinary breakthroughs in automated machine learning and beyond.

---

*This report has synthesized key findings from a broad spectrum of research efforts. It is intended to provide an in-depth, reference-rich overview of autoprompting and serves as a guide for further exploration and implementation in advanced, data-driven applications.*

## Sources

- http://arodes.hes-so.ch/record/5955
- http://arxiv.org/abs/2204.00998
- https://repository.upenn.edu/cgi/viewcontent.cgi?article=1006&amp;context=cps_machine_programming
- https://zenodo.org/record/1055895
- http://arxiv.org/pdf/1303.7093.pdf
- https://eprints.lancs.ac.uk/id/eprint/59907/
- https://madoc.bib.uni-mannheim.de/39016
- https://pub.uni-bielefeld.de/record/2979703
- https://zenodo.org/record/4680185
- https://cris.maastrichtuniversity.nl/en/publications/02f1de1b-695d-4fe5-b1f8-2e661b74bfaf
- https://research.utwente.nl/en/publications/axiomatic-testing-of-structure-metrics(1707aa09-a59a-43f6-80b9-4b50e183f443).html
- http://hdl.handle.net/10.26180/15154956.v1
- https://hdl.handle.net/1721.1/143854
- https://www.tdcommons.org/dpubs_series/1024
- http://arxiv.org/abs/2208.02532
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.6407
- http://library.oapen.org/handle/20.500.12657/23012
- https://hdl.handle.net/2152/119143
- http://hdl.handle.net/10356/42370
- http://hdl.handle.net/10289/2587
- https://hdl.handle.net/1721.1/139640.2
- http://arxiv.org/abs/2205.10370
- https://ph.pollub.pl/index.php/jcsi/article/view/2097
- http://dspace.wul.waseda.ac.jp/dspace/bitstream/2065/10666/1/sadoku-018.pdf
- https://orcid.org/0000-0002-7231-7643
- https://doi.org/10.24355/dbbs.084-202102191146-0
- https://discovery.ucl.ac.uk/id/eprint/10099087/19/Zhang_ML_Testing_Survey_arXiv.pdf
- http://sciforum.net/conference/MOL2NET-1/paper/3318/download/pdf/
- https://scholarworks.wm.edu/aspubs/820
- http://mosfet.isu.edu/classes/Neural
- https://hal.science/hal-04269868
- https://media.suub.uni-bremen.de/handle/elib/5042
- http://hdl.handle.net/11385/192635
- http://hdl.handle.net/11858/00-001M-0000-0013-C901-8
- https://lirias.kuleuven.be/bitstream/123456789/229976/1/Context-Aware%20Adaptation%20in%20an%20Ecology%20of%20Applications.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.7768
- https://www.repository.cam.ac.uk/handle/1810/284899
- https://cris.vtt.fi/en/publications/8ae75f8f-e045-475e-9b15-bf857135dcfc
- https://doaj.org/article/bf4e3406757c4d5681b31f83d0f0a83a
- http://arxiv.org/abs/2206.10210
- http://vixra.org/pdf/1405.0079v1.pdf
- https://nbn-resolving.org/urn:nbn:de:hbz:832-cos-777
- http://hdl.handle.net/2434/714671
- http://arxiv.org/abs/2205.12309
- http://www.lirmm.fr/~bessiere/stock/cp14-adaptive.pdf
- https://zenodo.org/record/1310586
- https://drops.dagstuhl.de/opus/volltexte/2010/2618/
- http://journal.ub.tu-berlin.de/eceasst/article/viewFile/131/129/
- http://hdl.handle.net/11380/979774
- https://zenodo.org/record/7043866
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.5377
- http://zaguan.unizar.es/record/69730
- http://arxiv.org/pdf/1107.4390.pdf
- https://researchbank.rmit.edu.au/view/rmit:56140
- https://lirias.kuleuven.be/bitstream/123456789/564497/1//seel16-034_Paper.pdf
- http://axel22.github.io/resources/docs/icadiwt_atga.pdf
- http://repository.tue.nl/753879
- http://web.engr.oregonstate.edu/%7Ektumer/publications/files/tumer-colby_aamas13.pdf
- https://dspace.kpfu.ru/xmlui/handle/net/170213
- https://doi.org/10.1109/ICCISci.2019.8716478
- https://escholarship.org/uc/item/6k7685q5
- https://zenodo.org/record/5055130
- http://arxiv.org/abs/2203.08304
- https://www.msu.edu/~pennock5/research/papers/IEEE-TEC11_IndirectEncodingAcrossRegularity.pdf
- http://hdl.handle.net/11562/20905
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.96.2518
- https://hdl.handle.net/11311/1256298
- http://dl.acm.org/citation.cfm?id=2576768
- https://zenodo.org/record/1313577
- http://eprints.fri.uni-lj.si/1413/1/Budal1.pdf
- http://www.aaai.org/ojs/index.php/aimagazine/article/download/93/92/
- http://repository.tue.nl/914620
- http://eprints.eemcs.utwente.nl/15288/01/Tre96-CTIT96-26.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-2863
- https://doi.org/10.26083/tuprints-00021651
- http://arxiv.org/abs/2203.01311
- http://handle.uws.edu.au:8081/1959.7/556956
- http://hdl.handle.net/2078.1/5515
- https://hal.archives-ouvertes.fr/hal-03452804/file/2104.08313.pdf
- http://d-scholarship.pitt.edu/44340/1/PTP_for_Thesis_final.pdf
- https://dx.doi.org/10.3390/info7020035
- http://hdl.handle.net/2160/38775
- https://hal.archives-ouvertes.fr/hal-01689997
- http://journal.ibsu.edu.ge/index.php/jtst/article/download/494/418/
- https://hdl.handle.net/1721.1/124252
- http://hdl.handle.net/10453/17677
- https://hal-univ-artois.archives-ouvertes.fr/hal-03300954
- https://univ-pau.hal.science/hal-01910019
- https://orca.cardiff.ac.uk/id/eprint/92466/1/effectiveness-automated-configuration.pdf
- http://staffwww.dcs.shef.ac.uk/people/A.Simons/research/papers/benchmark.pdf
- http://hdl.handle.net/10068/183115
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-146018
- http://hdl.handle.net/11573/579990
- http://coyotepapers.sbs.arizona.edu/CPXV/briner_mccarthy_mcnamara-pg1-17.pdf
- https://hdl.handle.net/10356/169609
- https://escholarship.org/uc/item/6tr2h9rb
- http://urn.kb.se/resolve?urn=urn:nbn:se:kau:diva-95645
- http://arxiv.org/abs/2201.09750
- http://eprints.hud.ac.uk/id/eprint/28670/1/effectiveness-automated-configuration.pdf
- http://repository.wit.ie/44/1/vdm2005k-mmns.pdf
- https://dare.uva.nl/personal/pure/en/publications/hyperlearn-a-distributed-approach-for-representation-learning-in-datasets-with-many-modalities(3c4994fc-fd39-42d7-a954-09ac61b17e79).html
- http://doc.rero.ch/record/333618/files/Riccio_ese_2020.pdf
- https://hal.archives-ouvertes.fr/hal-01906197
- https://stars.library.ucf.edu/scopus2010/6202
- http://hdl.handle.net/21.11116/0000-0000-7A96-E
- https://ojs.aaai.org/index.php/AAAI/article/view/25283
- https://hal.archives-ouvertes.fr/hal-00372138v2/document
- https://kluedo.ub.uni-kl.de/files/995/no_series_244.pdf
- http://hdl.handle.net/2440/118732
- https://hal.inria.fr/hal-01966962/file/drift-wkpICML2018.pdf
- http://hdl.handle.net/1871/11254
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-54269
- http://arxiv.org/abs/2211.02227
- http://hdl.handle.net/2078.1/67684
- https://zenodo.org/record/832468
- http://hdl.handle.net/11585/680810
- http://arxiv.org/abs/2203.00759
- http://arxiv.org/abs/2205.00049
- http://link.springer.com.gate6.inist.fr/article/10.1007%2Fs12243-012-0307-x
- http://urn.kb.se/resolve?urn=urn:nbn:se:miun:diva-13919
- http://hdl.handle.net/11250/2353451
- https://pure.tue.nl/ws/files/192514029/Adaptation_Strategies_for_Automated_Machine_Learning_on_Evolving_Data.pdf
- https://doaj.org/toc/2409-0026
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1571066107004896/MAIN/application/pdf/f6fa15edf2c8c3f1c5b889e63bde01fc/main.pdf
- https://etheses.whiterose.ac.uk/23098/2/ECO%20Thesis%20-%20Theoretical%20and%20Empirical%20Evaluation%20of%20Diversity-preserving%20Mechanisms%20in%20Evolutionary%20Algorithms.pdf
- https://stars.library.ucf.edu/scopus2010/2434
- http://arxiv.org/abs/2201.03916
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.7407
- http://hdl.handle.net/10.1371/journal.pdig.0000179.g001
- https://scholarworks.unist.ac.kr/handle/201301/53607
- http://hdl.handle.net/10068/154431
- https://escholarship.org/uc/item/3ch1d199
- https://doaj.org/article/50dc5ba7158a49b5a1271f1a8ebbfe82
- http://hdl.handle.net/10068/998035
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.74.5926
- http://www.ucl.ac.uk/%7Eucberal/ECTA2011.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.9201
- http://www6.in.tum.de/Main/Publications/wierstra2008c.pdf
- http://lup.lub.lu.se/student-papers/record/8923515
- https://ojs.aaai.org/index.php/SOCS/article/view/18588
- http://hdl.handle.net/11012/203382
- https://zenodo.org/record/60904
- http://hdl.handle.net/2117/346900
- http://hdl.handle.net/11385/192567
- http://tubiblio.ulb.tu-darmstadt.de/133999/
- http://hdl.handle.net/1893/28000
- https://discovery.ucl.ac.uk/id/eprint/10105016/
- http://hdl.handle.net/2434/49529
- http://arizona.openrepository.com/arizona/bitstream/10150/219531/1/IJCSN-2012-1-1-3.pdf
- http://scholarbank.nus.edu.sg/handle/10635/69750
- http://resolver.tudelft.nl/uuid:ef0529dd-1506-4e53-8aba-c9d20909125b
- http://arxiv.org/abs/2205.02918
- http://hdl.handle.net/2117/8870
- http://homepages.rpi.edu/~bonisp/NASA-course/fuzz05fredfinalv9.pdf
- http://resolver.tudelft.nl/uuid:1307aef3-331a-4814-8126-09ee0eae1359
- https://ojs.aaai.org/index.php/AAAI/article/view/25496
- http://nbn-resolving.de/urn:nbn:de:bsz:352-0-370172
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.89.3255
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.7737
- http://ai.stanford.edu/%7Eronnyk/c45ap.pdf
- https://doi.org/10.1007/s10994-022-06262-0
- http://www2.ic.uff.br/%7Eboeres/slides_AP/papers2012_2/AutonomicLoadFrameworkp91-barna.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.7207
- https://hal.archives-ouvertes.fr/hal-01286229
- http://www.thinkmind.org/download.php?articleid%3Dambient_2012_1_40_70045
- http://dx.doi.org/10.1145/1383559.1383585
- https://lirias.kuleuven.be/bitstream/123456789/203446/1/131-394-1-PB.pdf
- http://irep.iium.edu.my/119961/
- https://madoc.bib.uni-mannheim.de/62029/
- http://www.epics-project.eu/publications/2013_keller_srcs.pdf
- http://hdl.handle.net/11250/262478
- https://research.vu.nl/en/publications/cb261b84-0e80-403f-a9c6-8bc7ddf9295d
- https://escholarship.org/uc/item/2163j1c4
- http://www.nusl.cz/ntk/nusl-72087
- http://deal.ing.unisannio.it/perflab/assets/papers/CISIS2010.pdf
- https://hal.archives-ouvertes.fr/hal-01416457
- http://www.scopus.com/home.url)
- https://ojs.aaai.org/index.php/AAAI/article/view/26495
- http://hdl.handle.net/20.500.11850/541761
- https://zenodo.org/record/7234162
- http://hdl.handle.net/11573/1562600
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-14430
- http://hdl.handle.net/10045/110741
- https://ojs.aaai.org/index.php/AAAI/article/view/4272
- https://research.tue.nl/nl/publications/fd9419e4-2ac3-426e-8095-d01e869f4dba
- http://theis.io/media/publications/1511.01844v1.pdf
- http://hdl.handle.net/10150/195456
- http://publica.fraunhofer.de/documents/N-462107.html
- http://doi.acm.org/http://dx.doi.org/10.1145/2491411.2491434
- https://hal.archives-ouvertes.fr/hal-03449789
- http://hdl.handle.net/2134/19341863.v1
- http://publica.fraunhofer.de/documents/N-254246.html
- http://users.ecs.soton.ac.uk/dem/workshops/htsw2003/submissions/htsw03-falkovych.pdf
- http://arxiv.org/abs/2102.08921
- http://d3s.mff.cuni.cz/publications/download/2014-isola-performance.pdf
- http://web.ist.utl.pt/tiago.guerreiro/mmi/mmf/files/ICMI07_mmf_v1.1_CameraReady.pdf
- https://nbn-resolving.org/urn:nbn:de:gbv:084-2022012109310
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.2707
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-17626
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-10940
- http://arxiv.org/abs/2212.10873
- https://dx.doi.org/10.1109/CDC.2012.6426402
- https://hal.inria.fr/hal-00980839/document
- https://hal.inria.fr/hal-01155533/file/es-overview-2015.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1571066109004022/MAIN/application/pdf/ed6a8f7ff35f3c1fedec869ea52361eb/main.pdf
- http://arxiv.org/abs/2107.12322
- http://hdl.handle.net/2142/45868
- http://scholarbank.nus.edu.sg/handle/10635/69146
- http://article.sciencepublishinggroup.com/pdf/10.11648.j.ajsea.20150401.12.pdf
- http://dspace.mit.edu/bitstream/handle/1721.1/88083/MIT-CSAIL-TR-2014-014.pdf%3Bjsessionid%3DCAFBEBBDBC2DC29EA989E3AC9FB88DF7?sequence%3D1
- https://stars.library.ucf.edu/scopus2010/7677
- https://ojs.aaai.org/index.php/AAAI/article/view/21572
- https://escholarship.org/uc/item/0844s56f
- http://www.st.ewi.tudelft.nl/%7Earie/papers/artosc/TUD-SERG-2010-028.pdf
- http://sfbci.uni-dortmund.de/Publications/Reference/Downloads/_Rud020300D.pdf
- https://zenodo.org/record/8014324
- https://ijece.iaescore.com/index.php/IJECE/article/view/34522
- https://ojs.aaai.org/index.php/AAAI/article/view/17289
- http://eprints.gla.ac.uk/view/journal_volume/International_Journal_of_Intelligent_Systems.html