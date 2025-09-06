# Compound LLM Systems for Mimicking Knowledge Unlearning: A Detailed Analysis

## 1. Introduction

With the ever-growing complexity and deployment of large language models (LLMs) across diverse domains, the need for controlled and interpretable knowledge removal mechanisms has become paramount. Driven by legal imperatives (e.g., GDPR, California Consumer Privacy Act) and ethical considerations, the concept of knowledge unlearning is evolving from mere data removal to nuanced, context-adaptive strategies. Recent research has explored not only retraining or data purging but also more refined methods such as unlikelihood training and selective layer adjustments. This report examines the prospects for a Compound LLM System designed to mimic knowledge unlearning in large language models, drawing upon extensive learnings and multidisciplinary insights to outline both theoretical foundations and pragmatic approaches.

We investigate the design space of compound architectures—systems that encompass multiple, modular LLM components (e.g., specialized modules for retrieval, processing, unlearning) or employ a single LLM with engineered modular capabilities. Our analysis builds on methodologies from reinforcement learning, federated learning, differential privacy, and state-of-the-art unlearning techniques, while addressing both technical and evaluative challenges inherent to such multi-component frameworks.

## 2. Background and Related Work

### 2.1. Knowledge Unlearning in Machine Learning

Historically, knowledge unlearning has been addressed via mechanisms like post-hoc unlearning using unlikelihood training objectives or full retraining augmented with certifiable unlearning pipelines. For instance, approaches like the SCRUB algorithm have successfully balanced precision removal with maintained overall performance, and studies on logistic regression demonstrate trade-offs between approximation error and data expunction. The legal mandates for the 'right to be forgotten' have further motivated research into machine unlearning, leading to advanced pipelines that trigger full model retraining only when approximation errors become significant.

### 2.2. Modular and Compound Architectures

Concurrent research into modular reinforcement learning (RL) and multi-agent systems has shown that combining disparate components requires careful harmonization of reward scales. Studies indicate that Q-learning-based command arbitration, adaptive reward functions, and dynamic configuration via metareasoning are essential to ensure composability. Similarly, adapter architectures (e.g., MAD-X) and modular neural networks have been used effectively for tasks ranging from language translation to biomedical data processing, underscoring the potential benefits of splitting unlearning and data management tasks into distinct, specialized subsystems.

### 2.3. Evaluation Paradigms

Evaluation of unlearning strategies requires multi-dimensional benchmarks. The macro–meso–micro evaluation paradigm—originally proposed for Living Labs applications—proposes a three-layer analysis: global system performance (macro), inter-module interactions (meso), and granular, component-level performance (micro). In addition, integrated metrics such as PORT, which combines precision, recall, and ordering, have been shown to better correlate with human evaluation scores compared to traditional metrics such as BLEU. These insights provide a robust framework for assessing both the product and process of knowledge unlearning in complex LLM settings.

## 3. Architecting a Compound LLM System

### 3.1. Defining a Compound System

At its core, a compound LLM system is envisioned as an integrated ensemble of specialized modules, each assigned distinct roles such as:

- **Retrieval Module:** Responsible for sourcing relevant data and contextual cues, possibly integrating external databases, sensor inputs, or previous interactions.
- **Processing Module:** Handles the primary language understanding, generation, and transformation tasks in a manner similar to conventional LLM activities but with an eye on modular control.
- **Unlearning Module:** Specifically engineered to detect, isolate, and expunge outdated, erroneous, or legally problematic knowledge from the system’s parameters. This can be achieved through post-hoc token erasure, unlikelihood training adjustments, and targeted layer dropping.

Alternatively, the compound system could be a singular LLM engineered with modular capabilities that allow different internal pathways to be activated or suppressed based on the desired unlearning behavior. Techniques such as Sensitivity-Based Layer Dropping (SBLD) and selective activation recomputation are vital in this respect, as they dynamically reconfigure model complexity while reducing activation memory (with some studies showing up to 5× reduction) and cutting redundant computation by over 90%.

### 3.2. Modular Integration and Coordination

Drawing on insights from modular RL systems, the integration of independent LLM modules requires robust reward normalization and dynamic arbitration methods. For example, Q-learning-based command arbitration can reconcile disparate reward scales to ensure that the outcomes from different modules harmonize effectively. Advanced synchronization mechanisms, possibly leveraging metareasoning frameworks, can enable on-the-fly reconfiguration of modules to balance overall system utility against specialized unlearning objectives.

### 3.3. Mimicking Knowledge Unlearning

The process of knowledge unlearning can be approached in two distinct but overlapping manners:

- **Simulation of Data Removal:** Mimicking the removal of outdated or erroneous data without completely reinitializing the model. This involves computational methods such as applying unlikelihood training objectives to selectively drop token sequences, as demonstrated in recent studies, ensuring that the system gradually forgets outdated information while preserving overall coherence.

- **Deliberate Induction of Forgetting:** Employing mechanisms that induce controlled forgetting by overwriting certain network weights or using teacher–student frameworks. This method is reminiscent of Hedberg’s overwriting model or Klein’s parenthetic model, in which the system either completely replaces old knowledge or partially retains it with reduced influence.

Techniques like snapshot learning—with weight averaging at learning rate minima and temperature tuning (optimal performance noted at T = 1.3)—illustrate how the training dynamics can be adjusted to both enhance model stability and facilitate selective unlearning. Additionally, dynamic confidence tagging and adaptive confidence neurons provide real-time estimates of decision confidence, which are crucial for monitoring the effectiveness of the unlearning process and for mitigating risks such as membership inference attacks.

## 4. Evaluation Metrics and Methodologies

### 4.1. Integrated Multi-Dimensional Metrics

Evaluating the unlearning process in compound LLM systems is particularly challenging due to the inherent dependencies between modules. Traditional metrics (e.g., perplexity, BLEU) have limited sensitivity when unlearning effects are subtle. Multi-dimensional approaches like PORT—which fuses precision, recall, and ordering—along with novel ranking metrics (e.g., ZRF, Normalized Winning Number) have shown promise. Moreover, embedding reliability indicators such as those derived from neuroimaging metrics (e.g., zALFF) combined with network-specific parameters (e.g., NVI on LFR networks) could enhance unlearning evaluations.

### 4.2. The Macro–Meso–Micro Framework

The macro–meso–micro evaluation framework offers a layered approach:

- **Macro:** Measures overall system coherence and large-scale performance, ensuring that the unlearning process does not degrade predictive performance or introduce systemic biases.

- **Meso:** Focuses on coordination between modules. For example, how well does the unlearning module’s output integrate with the processing module? Are changes in one sub-system causing side effects in another?

- **Micro:** Examines individual, token-level changes. This includes tracking the efficacy of unlearning at the level of specific sequences or weights and measuring the precision of targeted knowledge removal.

### 4.3. Quantitative Thresholds and Sensitivity Analysis

Establishing concrete thresholds is vital. Drawing parallels from domains such as business process mining and biomedical evaluations, thresholds for precision, recall, and overall effectiveness (e.g., recall thresholds of >0.70 when combined with acceptable precision levels) can be adapted to LLM unlearning evaluation. Sensitivity analysis using dynamic metrics, such as those observed in sensitivity-based layer dropping methods, ensures that the trade-off between computational efficiency and unlearning efficacy is continuously balanced.

## 5. Implementation Strategies and Advanced Techniques

### 5.1. Efficient Computational Strategies

Advanced methods like selective activation recomputation and sequence parallelism are integral to maintaining efficiency. Documented improvements—up to 29% performance increases and significant memory reductions—demonstrate the viability of deploying compound LLM systems on large-scale platforms, such as 530B parameter models on multi-GPU settings.

### 5.2. Privacy-Driven and Federated Approaches

In the context of legal and privacy obligations, integrating methods from differential privacy and federated learning is essential. Techniques such as temperature scaling have proven effective against membership inference attacks, while algorithms tuned for unlearning (e.g., SCRUB) have balanced forget quality with model utility. Federated unlearning paradigms—whereby localized model updates are reversed (e.g., via projected gradient descent) when specific client data must be expunged—offer promising avenues for distributed, privacy-preserving LLM deployments.

### 5.3. Dynamic Configuration and Metareasoning

The application of dynamic module configuration via metareasoning is an emerging area of focus. By integrating rich contextual representations, these strategies enable the compound system to adapt its internal hierarchies in real time, optimizing not only immediate performance metrics but also long-term model adaptability and compliance with evolving legal frameworks.

## 6. Trade-offs, Challenges, and Future Directions

### 6.1. Balancing Efficiency and Efficacy

One of the major challenges lies in balancing the efficiency gains from techniques such as sensitivity-based layer dropping with the need to retain performance integrity post-unlearning. While strategies like snapshot learning and summation-based methods significantly reduce the cost relative to complete retraining, they may also introduce approximation errors that must be carefully monitored using combined metrics.

### 6.2. Regulatory Compliance and Ethical Considerations

The implementation of unlearning mechanisms is not solely a technical issue but also a legal and ethical one. Integrating legal compliance into the technical design—using established thresholds and evaluation frameworks—is a necessity. Future research should continue to explore how unlearning architectures can be standardized to support compliance mandates while preserving model utility.

### 6.3. Integrative and Interdisciplinary Innovations

Drawing from multiple fields—machine translation, neuroimaging, and modular RL frameworks—the next generation of compound LLM systems will likely incorporate hybrid approaches. These might marry neural unlearning with symbolic or ontology-based knowledge management, utilize dynamic confidence measures to control unlearning in real time, or employ teacher–student frameworks to guide selective forgetting.

### 6.4. Potential for Emergent Techniques

There is scope for exploring contrarian and non-traditional methodologies, such as dynamic precision selection in LSTM networks and the integration of extended BiRNN confidence estimators for unlearning validation. These novel approaches, though speculative, promise to further refine the balance between computational overhead and unlearning fidelity.

## 7. Conclusion

The landscape of knowledge unlearning in large language models is rapidly evolving, with compound LLM systems offering a promising framework for balancing modular specialization with overall coherence. By leveraging a blend of sophisticated modular architectures, dynamic evaluation frameworks (such as the macro–meso–micro paradigm), and advanced computational techniques, it is possible to design systems that meet the dual challenge of robust unlearning and sustained model performance.

Future work should continue to integrate insights from parallel domains, standardizing evaluation methods and exploring innovative unlearning paradigms. With tailored methods that span from federated unlearning to sensitivity-based dynamic configurations, compound LLM systems are poised to become essential platforms for managing the lifecycle of knowledge in artificial intelligence, ensuring that models can adapt and evolve in response to both technological progress and rigorous legal and ethical standards.

---

*This report synthesizes lessons from diverse research areas including reinforcement learning, federated learning, differential privacy, and advanced model evaluation techniques, and provides a comprehensive blueprint for deploying compound LLM architectures with effective knowledge unlearning capabilities.*

## Sources

- http://www.mt-archive.info/ACL-2010-He.pdf
- https://www.ksp.kit.edu/9783866447899
- http://hdl.handle.net/2066/167405
- http://hdl.handle.net/10.1371/journal.pone.0201520.t004
- http://www.mt-archive.info/NAACL-HLT-2010-Cer-1.pdf
- http://hdl.handle.net/10447/223410
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-16628
- http://arxiv.org/abs/2307.11254
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.5688
- https://figshare.com/articles/_Changes_in_magnitude_of_ALFF_calculated_at_different_frequency_bands_/1440555
- https://pro-ve-2021.sciencesconf.org/
- http://hdl.handle.net/11380/1268738
- http://arxiv.org/abs/2207.00099
- http://hdl.handle.net/10.1371/journal.pcbi.1006518.g002
- https://figshare.com/articles/New_Paradigms_and_Optimality_Guarantees_in_Statistical_Learning_and_Estimation/6720836
- https://hal.science/hal-03613558/file/A%20Methodology%20to%20Build%20Decision%20Analysis%20Tools.pdf
- http://hdl.handle.net/10560/islandora:1001314
- http://astro.temple.edu/~tua95067/djuric2013bigdata.pdf
- http://hdl.handle.net/11858/00-001M-0000-002B-3120-2
- http://arxiv.org/pdf/1209.2784.pdf
- https://hal.archives-ouvertes.fr/hal-00623642
- https://ojs.aaai.org/index.php/AAAI/article/view/5776
- https://doaj.org/article/bbda5f1cdf314cc593d4166ec4252762
- http://hdl.handle.net/11346/BIBLIO@id=-2764416092873062069
- https://lirias.kuleuven.be/handle/123456789/650533
- https://escholarship.org/uc/item/8cv4b2qp
- https://hal.science/hal-03389126/file/From%20Multimodal%20to%20Unimodal%20Attention%20in%20Transformers%20using%20Knowledge%20Distillation.pdf
- https://nrc-publications.canada.ca/eng/view/object/?id=376a485b-e4c4-4ffe-bc8a-cfae93085e10
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.862
- http://urn.fi/urn:nbn:fi-fe202101181977
- https://figshare.com/articles/_Evaluation_of_different_methods_on_LFR_benchmark_networks_/1361881
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.1793
- http://hdl.handle.net/10.1184/r1/6587174.v1
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0004370209000897/MAIN/application/pdf/728614198e4b1f30c5e586e33fb85f1a/main.pdf
- https://orbilu.uni.lu/handle/10993/57581
- http://arxiv.org/abs/2205.13891
- https://hal.science/hal-03798824/file/Pinte_Abstract-Poster_rtFIN2022.pdf
- http://resolver.tudelft.nl/uuid:6be8ea7b-2a87-45d9-aaa8-c82ff28d56c2
- https://aisel.aisnet.org/amcis2017/InformationSystems/Presentations/14
- http://hdl.handle.net/10453/22253
- https://avesis.deu.edu.tr/publication/details/01f7d0dd-4dad-4fa9-a090-384fdc53c24d/oai
- https://zenodo.org/record/8092059
- http://hdl.handle.net/2429/67623
- https://scholar.barrowneuro.org/neurology/504
- http://www.scopus.com/inward/record.url?scp=85139387457&partnerID=8YFLogxK
- https://digitalcommons.law.yale.edu/fss_papers/5141
- https://figshare.com/articles/_Performance_Metrics_/1231852
- http://www.nusl.cz/ntk/nusl-304321
- http://ir.sia.cn/handle/173321/26773
- https://figshare.com/articles/_Comparison_between_the_group_mean_zALFF_map_and_the_zALFF_reliability_map_using_a_three_session_dataset_RS1_RS2_and_RS3_from_10_subjects_/1440545
- http://faculty.ksu.edu.sa/ghazy/Documents/Emp
- https://www.repository.cam.ac.uk/handle/1810/315104
- https://inria.hal.science/hal-04168694/file/pinte-caroline-empenn.pdf
- http://wing.comp.nus.edu.sg/~antho/P/P13/P13-2067.pdf
- https://research-explorer.ista.ac.at/record/18062
- http://hdl.handle.net/10.25394/pgs.24279787.v1
- http://resolver.tudelft.nl/uuid:f1b187b2-638f-45f9-88c8-ce3bf548295c
- https://figshare.com/articles/_Comparison_of_learning_rates_in_the_later_stage_of_training_/309953
- https://figshare.com/articles/Proposed_method_evaluation_based_on_precision-_recall_and_F_sub_1_sub_-measure_metrics_/5883829
- https://eprints.whiterose.ac.uk/152594/1/coli_a_00356.pdf
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D2330%26context%3Dcompsci
- http://hdl.handle.net/10.36227/techrxiv.24708198.v1
- http://www.dbs.ifi.lmu.de/%7Eschubert/papers/PAKDD2007.pdf
- https://www.journal.iaingorontalo.ac.id/index.php/tjmpi/article/view/2911
- http://arxiv.org/abs/2308.16474
- https://ojs.aaai.org/index.php/AAAI/article/view/26321
- https://scholar.barrowneuro.org/neurology/506
- http://hdl.handle.net/1807/106253
- http://hdl.handle.net/10068/601406
- https://hal.science/hal-03740118/file/conference_101719.pdf
- http://www.iro.umontreal.ca/~sahraouh/qaoose/papers/Klemola.pdf
- http://arxiv.org/abs/2203.13167
- http://arxiv.org/abs/2205.05256
- http://www.cns.atr.jp/cnb/papers/pdf/Schweeighofer2003nn.pdf
- https://escholarship.org/uc/item/50n838xp
- https://figshare.com/articles/_Word_frequency_distributions_with_ZM_parameter_approximations_for_selected_languages_/1451662
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27703
- http://arxiv.org/abs/2306.03604
- http://ijr.sagepub.com/content/27/3-4/505.full.pdf
- https://hal.science/hal-03541009
- http://alarcos.esi.uclm.es/per/rpdelcastillo/publicaciones/internacionales/ESEM11.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.2320
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.8949
- http://arxiv.org/abs/2208.10836
- http://www.mt-archive.info/MTS-2003-Turian.pdf
- https://eprints.qut.edu.au/10788/
- https://doaj.org/article/bfe5448ccfc141ecb2e01a278b3f1985
- https://publications.cispa.saarland/3489/
- https://hal.archives-ouvertes.fr/hal-03251437
- http://arxiv.org/abs/2308.03945
- http://etd.adm.unipi.it/theses/available/etd-03092023-161823/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.88.1722
- https://zenodo.org/record/7996194
- http://www.ece.rutgers.edu/%7Easarwate/pdfs/ChaudhuriMS11erm.pdf
- https://cris.maastrichtuniversity.nl/en/publications/9e2b4ca4-a26f-476e-896a-057436db6a7d
- http://www.ewdw.com/PUBLICATIONS/Whittaker_ASJ2004.pdf
- http://hdl.handle.net/10018/6249
- https://nrc-publications.canada.ca/eng/view/fulltext/?id=e873a590-859e-4c30-a39f-3201fd3696b0
- http://arxiv.org/abs/2209.00939
- https://dare.uva.nl/personal/pure/en/publications/nbla-a-neurometric-test-battery-for-learning-disabledattention-deficit-disordered-children(4d6ad476-d4ec-438c-b9ca-d981f6132523).html
- https://doaj.org/toc/1875-919X
- http://resolver.tudelft.nl/uuid:fb784b70-bad4-46be-adfc-fcf1b013e27f
- http://www.hf.faa.gov/docs/508/docs/gmugrant/papers/Effectev.pdf
- http://repository.tue.nl/799368
- https://stars.library.ucf.edu/scopus2010/2687
- https://push-zb.helmholtz-muenchen.de/frontdoor.php?source_opus=57113
- https://doi.org/10.18653/v1/2020.acl-main.448.
- https://hal.science/hal-01997659/document
- http://www.theseus.fi/handle/10024/754099
- http://arxiv.org/abs/2309.14322
- http://www.iro.umontreal.ca/%7Efoster/papers/ce-acmtlsp06.pdf
- https://rdw.rowan.edu/etd/1268
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877042815023125/MAIN/application/pdf/e7a3c684ad94be77c3d4425f20b8818c/main.pdf
- https://philpapers.org/rec/GOEBIB
- https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00040464/SMABS2004_PaperSession_Hartig.mp4
- https://eprints.qut.edu.au/10604/
- http://mt-archive.info/LREC-2002-Dabbadie-2.pdf
- http://people.csail.mit.edu/jrg/2008/paul-emnlp08.pdf
- https://ojs.aaai.org/index.php/AIES/article/view/31716
- http://www.theseus.fi/handle/10024/500387
- http://arxiv.org/abs/2210.01504
- http://hdl.handle.net/10576/35609
- https://ojs.aaai.org/index.php/AAAI/article/view/4428
- https://zenodo.org/record/8331261
- https://ojs.aaai.org/index.php/AAAI/article/view/26528
- https://zenodo.org/record/7434406
- http://repository.tue.nl/906980
- https://doaj.org/article/6e1c7175cf924ad9833048c35a05e6d6
- http://hdl.handle.net/Main
- https://ojs.aaai.org/index.php/AAAI/article/view/8926
- https://ojs.aaai.org/index.php/AIES/article/view/31697
- https://seer.lcc.ufmg.br/index.php/jidm/article/download/221/163/
- https://ieeexplore.ieee.org/abstract/document/6916165
- https://eprints.lancs.ac.uk/id/eprint/211935/
- http://arxiv.org/abs/2207.07061
- https://ir.law.fsu.edu/lr/vol47/iss3/3
- http://arxiv.org/abs/2111.11124
- https://pubs.cs.uct.ac.za/id/eprint/579/
- https://nrc-publications.canada.ca/fra/voir/objet/?id=bcff7104-cfbc-4372-800b-d5b77c040066
- http://matjournals.in/index.php/JOCSES/article/view/5179
- http://ccsenet.org/journal/index.php/mas/article/download/2647/2450/
- https://hdl.handle.net/10356/151686
- https://cris.maastrichtuniversity.nl/en/publications/484fa120-e1e3-43aa-b58f-a91e890b46e1
- https://hdl.handle.net/10371/186868
- https://hdl.handle.net/11379/564860
- https://doaj.org/article/9cbeff002bba4a81ad937f95b9e9c3e1
- http://arxiv.org/abs/2205.14336
- https://ojs.aaai.org/index.php/AIES/article/view/31705
- https://doi.org/10.1109/TIFS.2021.3050603.
- http://hdl.handle.net/11582/312127
- http://hdl.handle.net/1807/110754
- http://www.niu.edu/user/tj0dgw1/pdf/learning/lukowiak
- http://hdl.handle.net/10.26434/chemrxiv.8058464.v1
- http://hdl.handle.net/10356/66920
- https://zenodo.org/record/4554990
- https://ojs.aaai.org/index.php/AAAI/article/view/25879
- https://www.scopus.com/inward/record.uri?eid=2-s2.0-84939815790&doi=10.1109%2fTSG.2014.2387848&partnerID=40&md5=2d6486a9f2c7cd33f7dde5a2737e24bf
- http://arxiv.org/abs/2202.07178
- http://hdl.handle.net/10018/6452
- http://www.dsmforum.org/events/DSM10/Papers/Tolvanen.pdf
- https://hal.inria.fr/hal-02387468/file/Active_block_matrix_completion_with_adaptive_confidence_sets.pdf
- https://escholarship.org/uc/item/5z00b5m9
- http://www.mt-archive.info/ACL-2007-Albrecht-2.pdf
- http://hdl.handle.net/10125/79686
- https://research.tue.nl/en/publications/e9ec1a83-22ce-4abf-9245-1541f297788f
- https://escholarship.org/uc/item/1j9178fr
- http://hdl.handle.net/10018/1427
- https://researchrepository.murdoch.edu.au/id/eprint/53990/
- https://hal.archives-ouvertes.fr/hal-02311104
- http://hdl.handle.net/1853/38251
- http://dx.doi.org/10.1109/MC.2022.3160276
- https://zenodo.org/record/5568797
- https://scholar.smu.edu/smulr/vol75/iss3/2
- https://hdl.handle.net/11250/2781110
- https://repository.law.umich.edu/book_chapters/6
- http://www.scopus.com/inward/record.url?scp=85038856554&partnerID=8YFLogxK
- http://edoc.hu-berlin.de/18452/24345
- https://zenodo.org/record/8154387
- https://doaj.org/toc/2415-6698
- http://hdl.handle.net/1773/36724
- http://hdl.handle.net/10018/6492
- http://hdl.handle.net/10138/345489
- https://hal.archives-ouvertes.fr/hal-00784858
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA460991%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://hdl.handle.net/10.1184/r1/6468992.v1
- http://arxiv.org/abs/2310.12442
- http://rise.cs.drexel.edu/~sunny/papers/wicsa09.pdf
- https://hal.in2p3.fr/in2p3-00726760/document
- https://ojs.aaai.org/index.php/AAAI/article/view/26008
- http://hdl.handle.net/2142/97890
- http://dx.doi.org/10.26153/tsw/42587
- https://eprints.lancs.ac.uk/id/eprint/224982/
- http://arxiv.org/abs/2205.05198
- http://www.mt-archive.info/LREC-2008-Babych-2.pdf
- https://figshare.com/articles/Properties_Being_Considered_for_Any_Assessment_Method/4007415
- https://figshare.com/articles/The_i_NVI_i_comparison_on_undirected_and_unweighted_small_LFR_benchmark_networks_with_large_average_degree_/3941616
- http://www.therightrequirement.com/pubs/1990-5/Determining
- http://hdl.handle.net/10362/33863
- http://arodes.hes-so.ch/record/4074
- https://ojs.aaai.org/index.php/AAAI/article/view/5965
- http://dx.doi.org/10.1016/j.jlp.2011.12.013
- https://eprints.qut.edu.au/13765/
- http://hdl.handle.net/2117/344816
- http://www.stat.columbia.edu/%7Emadigan/PAPERS/ldbma27.pdf
- http://arxiv.org/abs/2202.07304
- http://www.cs.columbia.edu/%7Ejunfeng/papers/unlearning-sp15.pdf
- https://www.repository.cam.ac.uk/handle/1810/279181
- https://zenodo.org/record/3515044
- http://ir.sia.cn/handle/173321/26639
- http://arxiv.org/abs/2309.12578
- http://hdl.handle.net/2134/22087289.v1
- https://digitalcommons.tacoma.uw.edu/context/tactalks/article/1014/type/native/viewcontent
- https://nrl.northumbria.ac.uk/id/eprint/47724/1/Privacy_and_Utility_aware_Recommendationswith_Local_Differential_Privacy_V5_0%20%281%29.pdf
- http://arxiv.org/pdf/1207.3520.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.1658
- http://lup.lub.lu.se/student-papers/record/1764310
- http://www.loc.gov/mods/v3
- https://ojs.aaai.org/index.php/AAAI/article/view/16900