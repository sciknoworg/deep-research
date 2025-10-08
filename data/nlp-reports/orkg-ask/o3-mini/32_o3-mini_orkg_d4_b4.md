# Final Report: LLM Directed Retrieval Querying for Improving Factuality

## 1. Introduction

The rapidly evolving domain of large language models (LLMs) has always been accompanied by challenges related to factual consistency and hallucination mitigation. This report presents an integrated evaluation of methods that direct retrieval queries in order to improve the factuality of LLM outputs. Our analysis synthesizes literature and experimental research on techniques ranging from word sense disambiguation and dynamic query augmentation to adversarial testing and reinforcement learning. The primary goal is to establish a comprehensive framework that not only reduces hallucinations in generative responses but also enhances retrieval precision in tasks that depend on external evidence.

## 2. Problem Definition and Objectives

Improving factuality in LLM outputs involves two interrelated goals:

- **Mitigating Hallucinations:** Reducing the generation of content that appears plausible but is factually incorrect. This involves addressing elements such as commonsense memorization errors, relational reasoning deficiencies, and overconfidence in generated outputs.

- **Enhancing Retrieval Precision:** Optimizing search and retrieval tasks so that outputs are corroborated by authoritative sources. This encompasses dynamic query adjustments, semantic enrichment, and the integration of static and dynamic retrieval augmentations that respond to LLM feedback.

The overall objective is to design systems that utilize directed retrieval querying to constrain and validate LLM outputs, ensuring that the generative process aligns with verifiable external content.

## 3. Methodologies and Integrated Approaches

Research has demonstrated multiple methodologies for addressing the issues of factuality and retrieval precision:

### 3.1. Query Expansion and Word Sense Disambiguation

Integrating word sense disambiguation with query expansion techniques is a foundational strategy. Approaches that employ corpus co-occurrence graphs and possibilistic networks have effectively resolved lexical ambiguities. Empirical evaluations on datasets like ROMANSEVAL and CLEF-2003 indicate that disambiguation can significantly improve both recall and precision metrics. This provides a key leverage point for retrieval systems to avoid conflicting evidence and ensure that ambiguous terms do not lead to erroneous information pairing.

### 3.2. Dynamic Query Algorithm Enhancements

A core dimension is the use of dynamic query adjustment algorithms. Several studies have demonstrated how machine learning models such as multi-layer perceptrons (MLPs) and recurrent neural networks can integrate with real-time systems—for instance, in healthcare risk prediction systems like DETECT (AUROC ~0.86). The ability to adjust queries dynamically based on live feedback not only modulates retrieval relevance but also mitigates the risk of hallucinations by constantly re-aligning model outputs with updated external data.

### 3.3. Retrieval Augmentation and Factual Boundary Delineation

Retrieval augmentation has emerged as a cornerstone in reducing factual inconsistencies observed in LLM outputs. Research (e.g., RUCAIBox and Med-HALT benchmarks) has emphasized that augmenting LLMs with external validated sources enhances both priori and posteriori judgment. Practically, models such as ChatGPT, LLaMA-2, and Atlas have shown marked improvement in error rates (up to 58% reduction in certain categories) when supplemented with retrieval outputs.

### 3.4. Reinforcement Learning & Adaptive Feedback Mechanisms

Combining reinforcement learning with traditional retrieval augmentation has offered additional pathways to improve factuality. Dynamic ranking optimization, employing frameworks like Markov Decision Processes (MDPs), Multi-Armed Bandits, and two-level interactive ranking architectures, allow systems to learn from both explicit and implicit user feedback. This dynamic adaptation responds in real time to user interactions, thereby mitigating trade-offs between diverse result sets and result depth.

Simultaneously, hybrid approaches that integrate RL-based relevance feedback with traditional techniques ensure that the retrieval system can overcome sparse or noisy input, as well as adjust rapidly to domain-specific challenges.

### 3.5. Adversarial Training and Constrained Attack Frameworks

Advanced adversarial training methods, including calibrated adversarial training and multi-objective constrained attacks, have been employed to further test and refine the factual consistency of LLM outputs. By incorporating both linear and non-linear constraints, adversarial frameworks—such as unified constrained attack systems—can generate feasible adversarial examples with high success rates. This is essential for rigorous debugging of LLMs, where prompt chaining (as used in AutoDebug) reveals vulnerabilities in commonsense reasoning and relational memory.

### 3.6. Neural Re-ranking and Hybrid Models

Another salient approach in evidence validation involves neural re-ranking techniques. Reinforcement learning-based rankers (e.g., the R3 system) and hybrid rank fusion methods like QLFusion have proven useful in re-prioritizing candidate documents based on semantic alignment and contextual integrity. This helps in maintaining factual consistency, especially when combined with classical IR methods (e.g., BM25, TF-IDF). The dual-phase pipeline integrating retrieval augmentation with neural re-ranking supports both immediate factual checks and prolonged evaluation through a feedback loop.

## 4. Evaluation Frameworks and Metrics

Robust evaluation frameworks are crucial for quantifying improvements in factuality. Several benchmarks have been proposed to gauge hallucination risks and retrieval efficacy:

### 4.1. Benchmarking with Med-HALT and HaELM

Systems such as Med-HALT provide structured evaluations based on both reasoning- and memory-based tests across different models. HaELM, on the other hand, emphasizes cost-effectiveness, reproducibility, and privacy. These frameworks incorporate engineered non-convex constraints (e.g., pixel-level adaptations in image domains) and calibrated semantic similarity metrics.

### 4.2. Risk-Sensitive Metrics and GLM-Based Evaluations

The application of Generalized Linear Models (GLMs) relaxes traditional linearity assumptions in IR evaluations, facilitating robust, non-linear assessments. Risk-sensitive metrics, such as the TRisk measure, and cumulative gain-based indicators have been pivotal in highlighting statistically significant discrepancies between retrieval approaches. Such metrics not only assess system performance but also quantify the reduction in overconfidence and hallucination rates in LLM outputs.

### 4.3. User-Centered and Context-Aware Measurement

Dynamic retrieval systems now integrate measures such as Normalized Task Completion Time (NT) and Normalized User Effectiveness (NUE) to capture the multifaceted nature of user satisfaction. Moreover, advanced techniques incorporate both explicit feedback (through questionnaires or satisfaction scores) and implicit signals (click behavior, sentiment analysis) to iteratively refine query outputs. This continuous feedback loop ensures that retrieval systems remain aligned with user expectations regarding factuality and trustworthiness.

## 5. Domain-Specific Considerations

Factual consistency improvements must account not only for general open-domain tasks but also for high-stakes domains such as healthcare, finance, and legal applications:

### 5.1. Healthcare Applications

In healthcare settings where errors can have severe consequences, dual-phase pipelines are being developed that combine dynamic query adjustments with adversarial testing frameworks, as seen in projects like DynAIRx. These pipelines incorporate domain-specific benchmarks, ensuring that outputs are cross-validated against multiple sources (e.g., EHR data, laboratory test results) and tailored retrieval augmentation strategies. Techniques such as high-dimensional propensity score (HDPS) methods and automated data-adaptive analytics further ensure robust confounder adjustments.

### 5.2. Financial and Legal Queries

Models specially fine-tuned for finance (e.g., ConFIRM with >90% accuracy) or legal QA demonstrate that specialized datasets dramatically enhance factual reliability. The integration of domain-specific query expansion methods, coupled with targeted adversarial retraining, ensures that retrieval outputs are both precise and contextually relevant. The emphasis on domain-specific approaches indicates that a one-size-fits-all model may be less effective than an architecture that adapts parameters based on field-specific data.

## 6. Discussion and Future Directions

### 6.1. Refining Dynamic Retrieval Systems

The research indicates that static retrieval methods are increasingly less effective compared to dynamic augmentation strategies that adapt to real-time user inputs and domain constraints. Future systems are likely to benefit from end-to-end pipelines that integrate reinforcement learning, adversarial testing, and real-time feedback loops. These systems should be designed with modular components (such as a Generator, Validator, and Optimizer) that directly link queries to authoritative, vetted online sources.

### 6.2. Integrating Hybrid Models

The blend of generative retrieval frameworks with neural re-ranking models represents a promising frontier. Future research should explore hybrid architectures that not only improve retrieval efficiency (as outlined by cost-aware cascade ranking and per-query dynamic cutoff predictions) but also ensure comprehensive factual checks. The synergy between retrieval and generative models could lead to systems that are robust even in low-feedback and adversarial scenarios.

### 6.3. Enhanced Adversarial Strategies

While adversarial training and testing have clearly demonstrated their value, there remains substantial room for improvement. Refinements in constrained attack methodologies, including the imposition of both linear and non-linear constraints, will be critical as LLMs continue to scale. Future adversarial protocols might consider leveraging latent-space perturbation strategies and FGSM-inspired adjustments to localize decision boundary vulnerabilities with greater precision.

### 6.4. Trust Cues and User-Centered Adaptation

The incorporation of trust cues—such as certainty highlighting, reference links, and social feedback—is critical to fostering user trust. As retrieval systems become more interactive, the use of transparent markers that indicate the confidence level of model outputs becomes paramount. Ongoing research into dynamic relevance feedback mechanisms (including pilot runs for selectivity estimation) will likely yield even more user-adaptive systems that balance factual accuracy with responsiveness.

### 6.5. Beyond Conventional Wisdom: Speculative and Contrarian Ideas

There remain innovative avenues worth exploring, such as:

- **Latent Q-A Memory Indexing:** Building on QA-memory indexing to store atomic Q-A pairs may further enhance compositional reasoning in multi-hop queries, thus bridging the gap between high-coverage passage retrieval and structured knowledge bases.

- **Graph-Based Iterative Unsupervised Methods:** Techniques that utilize graph structures (e.g., STEP approaches) to refine retrieval augmentation can potentially lower annotation costs and provide more robust evidence re-ranking.

- **Novel Hybrid RL Models:** Combining sample-efficient RL approaches with minimal user data could revolutionize retrieval paradigms in low-resource settings, albeit at the cost of higher computational overhead.

- **Integration with Private, Localized Knowledge Bases:** Tools like SimplyRetrieve exemplify the trend toward segregated retrieval and generation pipelines, thereby enhancing performance and data privacy. This model could be a blueprint for industries requiring strict confidentiality while relying on up-to-date factual information.

## 7. Conclusion

This report has provided a detailed exploration into the use of directed retrieval querying for enhancing factuality in LLM outputs. The integration of word sense disambiguation, dynamic query adjustment, adversarial training, and hybrid ranking methods collectively holds promise for reducing hallucinations and improving precision in retrieval-based tasks. Importantly, the convergence of retrieval augmentation with modern evaluation frameworks such as Med-HALT and HaELM provides a robust foundation for future work.

Moving forward, further research should focus on fine-tuning these integrated frameworks with domain-specific data and continued user-centered adaptations. The potential exists for these approaches to be applied across diverse sectors—ranging from healthcare to finance—ensuring that LLMs not only generate coherent text but do so with verifiable, factual integrity.

By continually iterating on these methodologies and embracing novel, contrarian approaches, the next generation of LLM retrieval systems is poised to become both highly effective and transparent, significantly advancing the state of factual consistency in AI-generated content.

## Sources

- http://arxiv.org/abs/2305.10235
- http://www.diku.dk/%7Ec.lioma/publications/ictir2009a.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/3812
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.73.9441
- https://researchbank.rmit.edu.au/view/rmit:17589
- https://scholarworks.utep.edu/dissertations/AAI1564656
- http://ir.ii.uam.es/%7Ealejandro/2007/s2/trabajo_eit2_abk.pdf
- http://www.nusl.cz/ntk/nusl-448078
- https://dare.uva.nl/personal/pure/en/publications/reinforcement-learning-to-rank(0813c7ef-5dcc-43e3-81fd-6a8bde7f4bde).html
- https://doi.org/10.1145/3295750.3298957
- https://digitalcommons.lsu.edu/vetmed_pubs/11
- http://hdl.handle.net/2078.1/278584
- http://www.eti.pg.gda.pl/katedry/kiw/pracownicy/Adam.Kaczmarek/C2_046_Kaczmarek.pdf
- http://oro.open.ac.uk/40779/1/ir0883p-zhangAemb.pdf
- http://hdl.handle.net/1721.1/119758
- https://researchbank.rmit.edu.au/view/rmit:18879
- http://arxiv.org/abs/2308.15126
- https://hdl.handle.net/1721.1/139041
- http://oro.open.ac.uk/44130/1/p871-li.pdf
- http://www.www2015.it/documents/proceedings/proceedings/p1177.pdf
- http://hdl.handle.net/2142/608
- http://arxiv.org/abs/2311.08401
- https://hal.archives-ouvertes.fr/hal-01883078/file/gan_for_testing.pdf
- http://arxiv.org/abs/2311.09136
- https://doi.org/10.1016/j.schres.2006.03.008
- https://zenodo.org/record/3268359
- http://emnlp2014.org/papers/pdf/EMNLP2014156.pdf
- http://staffwww.dcs.shef.ac.uk/people/R.Gaizauskas/research/papers/ecir04.pdf
- https://zenodo.org/record/7073494
- https://researchbank.rmit.edu.au/view/rmit:44756
- http://hdl.handle.net/11577/3402961
- https://publications.cispa.saarland/3142/
- https://researchbank.rmit.edu.au/view/rmit:48605
- http://hdl.handle.net/11025/39669
- https://dare.uva.nl/personal/pure/en/publications/learning-to-rank-for-information-retrieval-from-user-interactions(0a68588c-f8eb-491c-ba3c-e2f578e5636f).html
- http://ejournals.bc.edu/ojs/index.php/ital/article/view/3334
- https://doaj.org/article/8a294d437d884f07b9066bf8a36b09dc
- https://works.bepress.com/andrew_mccallum/68
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/6444
- http://cseweb.ucsd.edu/%7Egary/pubs/info-retrieval-1999.pdf
- http://www.cecs.uci.edu/%7Epapers/icme05/defevent/papers/cr1557.pdf
- https://zenodo.org/record/8186168
- https://repub.eur.nl/pub/135742
- http://berlin.csie.ntnu.edu.tw/Courses/Information%20Retrieval%20and%20Extraction/2012S_Lectures/IR2012S-Lecture04-Benchmark%20Collections.pdf
- https://www.microsoft.com/en-us/research/wp-content/uploads/2014/06/dyno-sigmod2014.pdf
- https://works.bepress.com/james_allan/5
- http://hdl.handle.net/10150/658717
- https://elib.dlr.de/83107/
- http://www.repository.uhblibrary.co.uk/id/eprint/5458/
- https://works.bepress.com/houbing_song/318
- https://ojs.aaai.org/index.php/AAAI/article/view/26483
- http://arxiv.org/abs/2307.03987
- https://researchbank.rmit.edu.au/view/rmit:18615
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/66278
- http://hdl.handle.net/2066/79177
- http://hdl.handle.net/10150/667278
- http://arxiv.org/abs/2311.01477
- https://pure.tue.nl/ws/files/192475963/1_s2.0_S1361841521001870_main.pdf
- https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=2188&amp;context=open_etd
- http://hdl.handle.net/2142/104003
- https://orbilu.uni.lu/handle/10993/29385
- http://arxiv.org/abs/2311.01463
- http://arxiv.org/abs/2202.08417
- http://arxiv.org/abs/2311.09114
- https://doi.org/10.1007/978-3-030-42835-8_8.
- https://zenodo.org/record/8191875
- http://resolver.tudelft.nl/uuid:aa87a2ad-ed2b-4e7d-91e8-73fe17879d6d
- https://hdl.handle.net/11577/3493282
- http://arxiv.org/abs/2308.03983
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.4260
- https://hal.archives-ouvertes.fr/hal-03103810v2/file/TLDKS.pdf
- https://hal.archives-ouvertes.fr/hal-03230715
- http://hdl.handle.net/10722/180707
- http://resolver.tudelft.nl/uuid:52636871-f8c1-45a7-9ccf-452f90c3784f
- http://d-scholarship.pitt.edu/12451/
- https://escholarship.org/uc/item/5bm9g2n1
- http://doras.dcu.ie/16391/
- http://arxiv.org/abs/2309.05217
- https://eprints.gla.ac.uk/221500/7/221500.pdf
- https://hdl.handle.net/2027.42/171361
- http://vislab.ucr.edu/PUBLICATIONS/pubs/Journal+and+Conference+Papers/after10-1-1997/Conference/2003/Reinforcement+Learning+for+Combining03.pdf
- http://linkinghub.elsevier.com/retrieve/pii/S0002-9297(15)00365-1
- http://ir.iscas.ac.cn/handle/311060/16295
- https://resolver.caltech.edu/CaltechAUTHORS:20140910-134106609
- http://arxiv.org/abs/2310.12516
- http://www.cs.cornell.edu/~karthik/Publications/PDF/raman_etal_11b.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-3992
- https://research.tue.nl/nl/publications/f4bca7c8-2a43-474e-8bd5-e1b3545446dd
- https://libkey.io/libraries/1712/10.1259/bjro.20220023
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.3910
- https://www.repository.cam.ac.uk/handle/1810/358475
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.73.1927
- http://hdl.handle.net/2066/161646
- http://lear.inrialpes.fr/people/triggs/events/iccv03/cdrom/iccv03/0510_yin.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/6876
- http://oro.open.ac.uk/38255/1/submission%282%29.pdf
- https://hal.archives-ouvertes.fr/hal-01845532
- https://ojs.aaai.org/index.php/AAAI/article/view/17568
- https://research.vu.nl/en/publications/c19efcd4-c636-40ba-9545-500610e03f20
- https://ojs.aaai.org/index.php/AAAI/article/view/17803
- http://arxiv.org/abs/2112.01156
- https://zenodo.org/record/4727091
- http://www.ee.columbia.edu/~graham/papers/huangDRCMPE08.pdf
- http://techreports.library.cornell.edu:8081/Dienst/UI/1.0/Display/cul.cs/TR83-570
- https://doaj.org/toc/2229-6956
- http://eprints.usq.edu.au/34527/
- http://www.ijera.com/papers/Vol3_issue5/DT35682686.pdf
- http://www.umiacs.umd.edu/%7Eninggao/pub/11/fully.pdf
- http://orbilu.uni.lu/handle/10993/53045
- http://research.ijcaonline.org/volume105/number8/pxc3899646.pdf
- http://arxiv.org/abs/2207.03073
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.1112
- http://dspace.library.iitb.ac.in/xmlui/handle/100/25257
- http://ilps.science.uva.nl/sites/ilps.science.uva.nl/files/irfc2011-l2r.pdf
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA449013%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://eprints.rclis.org/32943/1/Open-%20vs.%20Restricted-Domain%20QA%20Systems%20in%20the%20Biomedical%20Field.pdf
- http://users.mct.open.ac.uk/ss24382/papers/qairstoyanchev-song-lahti-camera.pdf
- http://hdl.handle.net/10.1371/journal.pone.0273281.g003
- http://hdl.handle.net/10150/657832
- http://hdl.handle.net/2142/10991
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.5016
- https://hdl.handle.net/1721.1/139227
- http://hdl.handle.net/10722/82739
- http://www.loc.gov/mods/v3
- http://ir.ncnu.edu.tw:8080/handle/310010000/14871
- http://arxiv.org/abs/2205.09393
- http://arxiv.org/abs/2307.15343
- https://trepo.tuni.fi/handle/10024/65718
- http://hdl.handle.net/10566/1062
- https://papers.nips.cc/paper/2020/hash/c4fac8fb3c9e17a2f4553a001f631975-Abstract.html
- https://zenodo.org/record/6359843
- http://dx.doi.org/10.1016/S2589-7500(20)30024-8
- http://tubiblio.ulb.tu-darmstadt.de/view/person/K=FCgler=3ADavid=3A=3A.html
- https://researchbank.rmit.edu.au/view/rmit:18929
- https://vfast.org/journals/index.php/VTSE/article/view/496
- https://resolver.caltech.edu/CaltechAUTHORS:20140910-105428880
- https://escholarship.org/uc/item/3dx2f8kq
- http://hdl.handle.net/10722/224244
- https://lirias.kuleuven.be/handle/123456789/199408
- http://arxiv.org/abs/2310.12558
- https://scholarworks.umass.edu/dissertations/AAI3152722
- http://hdl.handle.net/10523/4453
- http://www.ime.usp.br/%7Ejmsinger/MAE5705/Alencar%26Singer%26Rocha2012BiomJournal.pdf
- http://www.nusl.cz/ntk/nusl-383263
- https://discovery.ucl.ac.uk/id/eprint/1503918/
- http://arxiv.org/abs/2310.13001
- http://techreports.library.cornell.edu:8081/Dienst/UI/1.0/Display/cul.cs/TR69-39
- http://clef.isti.cnr.it/2009/working_notes/kuersten-videoclef-paperCLEF2009.pdf
- http://udspace.udel.edu/handle/19716/23622
- http://hdl.handle.net/10.1184/r1/6473774.v1
- https://eprints.whiterose.ac.uk/id/eprint/80506/1/acse%20research%20report%20614.pdf
- https://hal.inria.fr/hal-03893496
- http://dl2015.image.ntua.gr/
- http://hdl.handle.net/10.1184/r1/6473021.v1
- https://escholarship.org/uc/item/21p8270f
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/8b/47/sap-25-05-319.PMC4054568.pdf
- https://hildok.bsz-bw.de/frontdoor/index/index/docId/12
- http://pages.cs.wisc.edu/~andrzeje/publications/kdd-2011-poster.pdf
- http://ir.sia.cn/handle/173321/29856
- https://researchonline.lshtm.ac.uk/id/eprint/4664727/1/2021_EPH_PhD_Tazare_J.pdf
- http://dx.doi.org/10.1080/03610918.2012.683924
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA512698%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://jptam.org/index.php/jptam/article/view/3241
- http://arxiv.org/pdf/1108.2754.pdf
- https://researchbank.rmit.edu.au/view/rmit:44354
- https://zenodo.org/record/4792375
- http://arxiv.org/abs/2311.01307
- https://figshare.com/articles/_Relative_risk_of_hallucinations_illusions_estimated_as_odds_ratios_ORs_using_a_multi_variable_regression_model_/922287
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.2023
- http://repository.essex.ac.uk/14724/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.7239
- http://hdl.handle.net/10251/201319
- http://hdl.handle.net/10278/3724417
- https://digitalcommons.aaru.edu.jo/amis/vol11/iss5/26
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.4651
- http://ciir-publications.cs.umass.edu/pub/web/getpdf.php?id=1153
- http://resolver.tudelft.nl/uuid:8e38bc8b-6bff-4794-a27a-93ce6a95ee53
- http://hdl.handle.net/1721.1/5978
- https://e-space.mmu.ac.uk/23157/
- https://pure.eur.nl/en/publications/d2e1b011-0337-4513-b722-5316cc1c0e6e
- http://hdl.handle.net/11571/1341075
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.661
- http://people.bu.edu/ellisrp/EllisPapers/2009_EllisMookim_R2paper.pdf
- http://arxiv.org/abs/2307.11019
- https://dare.uva.nl/personal/pure/en/publications/balancing-speed-and-quality-in-online-learning-to-rank-for-information-retrieval(519d43f8-6f6f-4573-80b2-0320aaf9f4cf).html
- http://hdl.handle.net/20.500.11850/460345
- https://research.tue.nl/en/publications/f9fe56cc-dc5c-4122-8fe7-7f871e3cc6cb
- http://www.acad.ro/sectii2002/proceedings/doc2008-3/12-Ion.pdf
- http://edoc.mdc-berlin.de/19317/
- https://hal.archives-ouvertes.fr/hal-02353400/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.8153
- https://doi.org/10.17605/OSF.IO/N3YZ5
- http://hdl.handle.net/11571/1361534
- https://doaj.org/article/697838f5e4fc4433915bd5f542704bc7
- https://zenodo.org/record/3373529
- http://hdl.handle.net/2142/11349
- http://arxiv.org/abs/2203.17274
- http://ceur-ws.org/Vol-1172/CLEF2006wn-CLSR-TerolEt2006.pdf
- http://livrepository.liverpool.ac.uk/3176648/1/2205.08589.pdf
- https://eprints.lancs.ac.uk/id/eprint/124801/
- https://ojs.aaai.org/index.php/AAAI/article/view/12053
- https://hal.archives-ouvertes.fr/hal-01990465
- http://arxiv.org/abs/2204.04581
- http://repository.nkfust.edu.tw/ir/handle/987654321/14862
- https://doaj.org/article/e3c2d6baf26c4d6a9cbcbd159038b3c5
- https://eprints.whiterose.ac.uk/3777/1/petrelid1.pdf
- https://researchbank.rmit.edu.au/view/rmit:39108
- https://discovery.ucl.ac.uk/id/eprint/10181256/
- http://arxiv.org/abs/2310.12443