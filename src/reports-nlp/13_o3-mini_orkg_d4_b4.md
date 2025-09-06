# Final Report: Simulating Novice Coding (Mis-)Behaviors with Large Language Models

## 1. Introduction

The quest to simulate novice coding behaviors using large language models (LLMs) not only bridges the gap between generative artificial intelligence and human error diagnosis but also transforms pedagogical insights into practical engineering tools. This report consolidates extensive research, empirical learnings, and theoretical advances, spanning multiple disciplines including cognitive psychology, software engineering, and machine learning. The aim is to rigorously detail methods to simulate novice coding errors — from syntax mistakes to conceptual misunderstandings and erroneous debugging processes — and propose frameworks to diagnose, emulate, and ultimately remediate these misbehaviors.

## 2. Framing the Problem: Novice Coding Behaviors and Misbehaviors

The simulation of novice coding errors can be categorized into several distinct behaviors:

- **Syntax Errors**: Incorrect code structures that breakdown language grammar rules.
- **Conceptual Misunderstandings**: Misinterpretations of programming paradigms, leading to logical or semantic errors.
- **Debugging Strategies**: Inadequate or misapplied strategies when identifying and resolving issues.

These behaviors are not isolated phenomena; rather, they are intertwined with cognitive load, inherent biases (both from the developer and the AI system), and the nature of the programming task. The research literature advocates for a multifaceted approach, which integrates technical performance metrics, cognitive load assessments, and diagnostic rubrics derived from both human and algorithmic insights.

## 3. Comprehensive Research Learnings

A careful synthesis of recent studies and advancements provides a robust framework on which to build LLM-powered novice error simulations. The following subsections summarize the central research learnings:

### 3.1 Unified Performance Metrics and Code Quality Assessments

- **Composite Performance Metrics**: Several studies demonstrate that combining objective measures such as execution time and quality (e.g., cohesion, coupling via CKJM tools) yields high correlations with programmer seniority and self-assessed expertise. These combined metrics, when normalized (e.g., using Jadud’s error quotient calibrated via Kriging-based optimization), allow for precise evaluation and error detection.

- **Syntax-based Error Metrics**: The development and calibration of syntax-based metrics have highlighted the need for context-independent error quantification. Tools that harness normalized parameters are essential for extrapolating novice errors into scalable performance measures.

### 3.2 Advanced Prompt Engineering and Bias Detection

- **Bias in LLM-generated Code**: Advanced prompt engineering has been instrumental in detecting both socially-derived and cognitive biases. Studies leveraging models such as BERT, RoBERTa, and T5 have revealed anchoring and confirmation biases that influence code generation. Improved robustness can be achieved by refining prompt parameters and utilizing dual-phase architectures (such as proposer and ranker systems) to mitigate bias.

- **LLM Error Simulation**: Systematic methods using LLMs (e.g., Codex, GPT-4 type architectures) for simulating novice errors reveal patterns, especially a tendency to mimic high-frequency syntactic errors. Correcting these biases and designing diverse test prompts is essential for generating realistic error distributions.

### 3.3 Cognitive Load, Self-Assessment, and Psychometric Integration

- **Cognitive Load Measurement**: Studies borrowing from Morrison et al. and Raven’s Matrices underscore the importance of distinguishing intrinsic, extraneous, and, to some degree, germane loads. Integrating these assessments into LLM models can provide actionable feedback regarding the complexity of generated error patterns.

- **Psychometric Assessments**: Integration of psychometric data (including adaptations beyond traditional MBTI frameworks) with code-level metrics brings to light nuanced patterns on error generation and correction efficacy. This integration supports the formulation of personalized diagnostics—ensuring that simulated novice misbehaviors resemble real-world cognitive challenges.

### 3.4 Simulation Frameworks and Runtime Verification

- **Atomic Decomposition of Coding Tasks**: Utilizing frameworks that break down coding tasks into atomic elements (aided by the SOLO taxonomy) provides a granular view of novice mistakes. These models support detailed classification of errors at both syntax and semantic levels.

- **Runtime Verification Architectures**: Tools employing Logic-Labelled Finite-State Machines (LLFSMs) combined with assumption-based frameworks like NuRV and NUXMV, enable real-time error monitoring. Embedding these architectures allows LLM simulations to yield multi-step logic errors and detect cascading faults that are characteristic of novice debugging mishaps.

### 3.5 Hybrid and Multi-Paradigm Approaches

- **Mixed Code Representations**: Empirical evidence suggests that combining token sequences with AST-based abstractions leads to improved error repair and generation outcomes. This dual-representation approach is crucial when simulating both surface-level syntax failures and deeper, conceptual missteps.

- **Integration of Automated Program Repair (APR)**: Hybrid systems that merge dense neural network classifiers with classical symbolic reasoning frameworks (such as SEQUENCER or DeepDelta) have demonstrated high repair rates, particularly when ranking the correct fix among potential candidates. This synergy improves the simulation of error identification and self-repair tactics in novice coding environments.

### 3.6 Ethical Considerations and System Scalability

- **Ethical Frameworks**: Research globally emphasizes robust ethical protocols (e.g., Jisc’s Code of Practice) to safeguard learner data handling, ensure fairness, and maintain algorithmic transparency. The integration of these frameworks is critical when employing LLMs for high-stakes educational applications.

- **Scalability and Distributed Architectures**: Distributed platforms that utilize serverless functions and microservices are essential to support dynamic resource allocation for analytics, as shown in systems like ATLAS (CERN) and MULE from Maynooth University. This architectural design must support real-time updates and adaptive learning mechanisms without compromising performance or ethical oversight.

## 4. LLMs as Simulation Engines for Novice Errors

The potential of LLMs in simulating coding mistakes is two-pronged: generating realistic error-laden code samples and diagnosing these errors against typical novice behavior profiles. Key applications include:

- **Error Generation**: Using LLMs in a controlled setting to generate code that contains a spectrum of errors—from simple syntactic inaccuracies to multi-step logical flaws—allows for the development of test suites for educational purposes. Novel simulation environments such as PyFiXV have shown that iterative cycles (Synthesize, Execute, Debug) improve the fidelity of simulated novice behaviors.

- **Error Diagnosis and Feedback**: By integrating runtime verification tools with neural network classifiers, systems can pinpoint and diagnose errors in a manner analogous to human tutors. The CORE architecture, for example, uses a dual LLM system to generate candidate revisions and systematically rank their feasibility against structured error metrics.

- **Adaptive Feedback and Incremental Learning**: Dynamic methods, such as anticipatory dynamic learning and online hyperparameter optimization, enable systems to adapt in real time to evolving error profiles. The integration of personalized, fine-grained feedback (augmented by survival analysis and incremental learning techniques) has been shown to significantly improve error resolution times and overall comprehension among novice programmers.

## 5. Proposed Integrated Framework and Future Directions

### 5.1 Proposed Architecture

We propose an integrated framework for simulating novice coding misbehaviors as follows:

1. **Data Ingestion and Preprocessing**: Collect multi-modal data sets (source code, error logs, code reviews) and preprocess them using techniques inspired by traditional tokenization and neural feature extraction (e.g., fastText, Word2Vec variants).

2. **Error Generation Module**: Leverage an LLM configured with advanced prompt-engineering strategies. This module integrates bias mitigation tools and contemporary error simulators (drawing on insights from Markov Logic-based approaches adapted from language error simulation) to generate realistic novice errors.

3. **Diagnostic Engine**: Employ runtime verification architectures (LLFSM-based and assumption-based methods) in tandem with dense neural classifiers to diagnose generated errors. Incorporate hybrid representations (AST and token sequence combinations) to yield diagnostic insights.

4. **Feedback and Repair Module**: Integrate automated program repair modules (such as DeepDelta or SEQUENCER) and adaptive feedback loops, calibrated by neural and statistical metrics (e.g., precision, recall, F1-score) to propose targeted revisions.

5. **Ethical Oversight and Scalability Layer**: Embed ethical evaluation protocols and distributed processing frameworks (leveraging microservices and serverless approaches) to ensure that data use and model updates remain transparent and fair.

### 5.2 Future Research Directions

- **Refining Free Parameter Calibration**: Further research is needed to systematically adjust free parameters in metrics (such as Jadud’s error quotient). Future work might integrate Kriging-based, Bayesian, and heuristic optimization frameworks.

- **Improved Multi-step Logic Simulation**: Although current LLMs can reliably simulate many novice behaviors, there is room to enhance multi-step logical error simulations. Combining symbolic logic (via formal verification methods) with dense vector representations could improve fidelity.

- **Adaptive, Real-Time Ethical Oversight**: As LLMs are deployed in dynamic and sensitive educational environments, frameworks for real-time ethical monitoring and bias correction—akin to anticipatory dynamic learning approaches—should be continuously refined.

- **Integration with Cognitive and Psychometric Evaluations**: Continued bridging between cognitive psychology and machine learning will refine our understanding of intrinsic versus extraneous cognitive load. Further development might explore real-time neurocognitive feedback loops to adjust simulation fidelity on the fly.

## 6. Conclusion

Simulating novice coding misbehaviors with large language models offers a promising frontier that fuses advanced AI techniques, rigorous performance metrics, and deep insights from educational psychology. By integrating comprehensive diagnostic tools, flexible hybrid architectures, and ethical oversight mechanisms, we can create systems that not only mimic human-like errors but also provide targeted, adaptive feedback to foster learning and reduce error repair costs. The integrated framework presented herein holds promise for both academic environments and large-scale deployments—paving the way for intelligent, self-correcting educational tools that mirror real-world coding challenges.

Moving forward, a multidisciplinary approach that bridges technical, cognitive, and ethical paradigms will be essential in tuning these systems for scalability, fairness, and practical impact in novice programming education.

---

*This report aggregates research learnings derived from a broad array of studies in machine learning, software engineering, and cognitive psychology. The integration of these findings offers comprehensive insights into how LLMs might be used to simulate, diagnose, and remediate novice coding mistakes effectively.*

## Sources

- https://hdl.handle.net/10292/1515
- http://hdl.handle.net/11585/709279
- https://zenodo.org/record/8122636
- http://moss.csc.ncsu.edu/%7Emueller/ftp/pub/mueller/papers/corr13.pdf
- https://digitalcommons.csbsju.edu/honors_theses/176
- http://dx.doi.org/10.1016/j.infsof.2020.106368
- http://www.dcs.bbk.ac.uk/~dell/teaching/cc/paper/sigmod12/p793-lin.pdf
- https://zenodo.org/record/6946565
- https://zenodo.org/record/5907927
- https://research.tue.nl/en/publications/339201e9-500a-4243-9113-5c967d033b9e
- http://arxiv.org/abs/2309.14345
- http://www6.in.tum.de/Main/Publications/Gagliolo2006a.pdf
- http://hdl.handle.net/10525/680
- http://www.ics.teikyo-u.ac.jp/~hiro/proj/asmjudge1/icce99.pdf
- https://hdl.handle.net/11420/49859
- http://knowledge.uchicago.edu/record/2735/files/Ding_uchicago_0330D_15553.pdf
- http://publica.fraunhofer.de/documents/N-188309.html
- http://dx.doi.org/10.1109/APSEC.2011.44
- http://hdl.handle.net/10.1184/r1/6469991.v1
- https://escholarship.org/uc/item/1p0851z6
- https://www.repository.cam.ac.uk/handle/1810/302349
- http://www.lta.disco.unimib.it/lta/uploads/papers/Whalen-FITE-FOSER-2010.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1571066105805778/MAIN/application/pdf/20cb4b53944a584f2756009f1b95d843/main.pdf
- https://doi.org/10.7298/X4J96499
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1050.1042
- http://hdl.handle.net/2160/657
- http://arxiv.org/pdf/1307.4394.pdf
- https://hal.science/hal-01640097/document
- http://hdl.handle.net/20.500.12207/502
- https://hal.inria.fr/hal-01976747/document
- https://www.erts2022.org/,
- https://zenodo.org/record/7147519
- https://tigerprints.clemson.edu/grads_symposium/118
- https://cedar.wwu.edu/grad_conf/poster_presentations/poster_presentations/24
- http://arxiv.org/abs/2202.12299
- https://escholarship.org/uc/item/62m217kx
- https://doaj.org/article/d502a213a3cc4323bb0745fdf7cdd284
- https://docs.lib.purdue.edu/dissertations/AAI30504013
- https://www.repository.cam.ac.uk/handle/1810/294984
- http://hdl.handle.net/10.1184/r1/9989393.v1
- https://elib.dlr.de/132578/
- https://aisel.aisnet.org/cgi/viewcontent.cgi?article=1000&amp;context=sais2004
- https://openresearch.surrey.ac.uk/view/delivery/44SUR_INST/12138413410002346/13140605050002346
- https://researchbank.rmit.edu.au/view/rmit:8793
- https://pure.hud.ac.uk/en/publications/6da46168-4930-414f-be7a-68f68bad93ee
- https://www.duo.uio.no/bitstream/handle/10852/48583/1/PhD-Bergersen.pdf
- http://hdl.handle.net/11581/226471
- https://eprints.lancs.ac.uk/id/eprint/169350/
- http://arxiv.org/abs/2203.07983
- https://doaj.org/article/88cf7750206b4f1381a10545f3c29716
- https://www.repository.cam.ac.uk/handle/1810/287795
- https://collections.lib.utah.edu/ark:/87278/s66b17qh
- https://www.repository.cam.ac.uk/handle/1810/279104
- http://arxiv.org/abs/2206.06960
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066107001910/MAIN/application/pdf/d5e179ab65b895b720179a99be8f651f/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.1206
- https://zenodo.org/record/5151947
- https://drops.dagstuhl.de/opus/volltexte/2010/2619/
- https://kluedo.ub.uni-kl.de/files/1105/sfb501_22.pdf
- http://hdl.handle.net/10292/16708
- http://hdl.handle.net/1773/49314
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.5420
- https://dare.uva.nl/personal/pure/en/publications/the-learning-analytics-architectural-lifecycle(c722c3f9-45f2-46f8-9e5a-7328b0d73296).html
- http://arxiv.org/abs/2309.12938
- https://inria.hal.science/hal-00696590/document
- https://zenodo.org/record/6802730
- https://scholarworks.utep.edu/cgi/viewcontent.cgi?article=1049&amp;context=open_etd
- https://fisherpub.sjf.edu/math_facpub/16
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.8300
- https://zenodo.org/record/7620095
- https://orcid.org/0000-0002-2721-0898
- http://www.nusl.cz/ntk/nusl-236750
- http://www.iro.umontreal.ca/~sahraouh/qaoose/papers/Klemola.pdf
- http://hdl.handle.net/1853/56343
- http://hdl.handle.net/11380/1247332
- https://doi.org/10.1051/itmconf/20225001003
- https://escholarship.org/uc/item/50n838xp
- https://doaj.org/article/6e4b63aaed6d4f008f26a5427030f49e
- https://escholarship.org/uc/item/09r411mq
- http://hdl.handle.net/11581/456452
- http://www.theseus.fi/handle/10024/347872
- https://hal.archives-ouvertes.fr/hal-02473300/file/accurateai_HAL.pdf
- http://arxiv.org/abs/2110.14081
- https://docs.lib.purdue.edu/context/idcpres/article/1004/type/native/viewcontent
- https://research.tue.nl/nl/publications/exploration-strategies-performance-and-error-consequences-when-learning-a-complex-computer-program(64ed54a6-b017-4f9e-b654-514f9848ebb4).html
- https://orbilu.uni.lu/bitstream/10993/45073/1/thesis.pdf
- http://www.optimization-online.org/DB_FILE/2009/03/2259.pdf
- https://doi.org/10.1145/2543882.2543884
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:72837
- https://escholarship.org/uc/item/0441n1tt
- http://summit.sfu.ca/item/8292
- http://hdl.handle.net/11299/217418
- https://zenodo.org/record/5605708
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-21932
- http://resolver.tudelft.nl/uuid:f2d50c24-6f10-4f82-9f69-7edff5ea44ba
- http://repository.tue.nl/798474
- https://hdl.handle.net/11511/56280
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.2224
- http://www.cs.jhu.edu/%7Eyarowsky/acl2000/sigdat/hung.pdf
- https://zenodo.org/record/8115653
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-9467
- http://springerlink.com/content/0302-9743/copyright/2005/
- https://espace.library.uq.edu.au/view/UQ:a874a19
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.7327
- https://hdl.handle.net/1805/31396
- www.duo.uio.no:10852/87966
- https://aisel.aisnet.org/siged2018/25
- https://ojs.aaai.org/index.php/AAAI/article/view/10633
- http://hdl.handle.net/10314/2412
- https://doi.org/10.1145/3696443.3708959
- https://figshare.com/articles/Psychopy_ext_A_framework_for_streamlining_research_workflow_in_neuroscience_and_psychology_/6356719
- http://web.me.iastate.edu/soumiks/pdf/Conference/bigdata15_conf.pdf
- https://scholarbank.nus.edu.sg/handle/10635/232249
- https://zenodo.org/record/8296440
- https://repository.uwtsd.ac.uk/id/eprint/1249/
- http://hdl.handle.net/20.500.11937/19941
- https://source.sheridancollege.ca/context/ctl_publ/article/1004/type/native/viewcontent
- http://hdl.handle.net/2142/34253
- https://archium.ateneo.edu/theses-dissertations/264
- https://hal.inria.fr/hal-00853727
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Doyle=3AJoseph=3A=3A.html
- http://hdl.handle.net/10072/383221
- https://research.utwente.nl/en/publications/d87a6dc6-8af2-4c4f-8d4c-f119e7201a2c
- http://hdl.handle.net/11567/932340
- https://zenodo.org/record/7030145
- http://irep.iium.edu.my/97680/7/97680_Source%20code%20plagiarism%20detection.pdf
- http://arxiv.org/abs/2307.04492
- http://dx.doi.org/10.1016/S0167-9260(98)00013-3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.5678
- http://144.124.16.251/ltt/RESEARCH/strategies.pdf
- https://ieeexplore.ieee.org/abstract/document/9251049
- http://hdl.handle.net/2429/80146
- https://dare.uva.nl/personal/pure/en/publications/taming-technical-bias-in-machine-learning-pipelines(06902f9d-224a-4f3f-8c52-33496fe8bd56).html
- http://www.win.tue.nl/%7Easerebre/ICSME2015ERAPaloma.pdf
- https://doi.org/10.1007/s10703-023-00416-z
- https://tel.archives-ouvertes.fr/tel-00809048
- http://hal-onera.archives-ouvertes.fr/docs/00/52/08/08/PDF/SYSTOL36final.pdf
- https://scholarworks.umass.edu/cgi/viewcontent.cgi?article=3693&amp;context=dissertations_2
- https://pure.eur.nl/en/publications/0f62a47a-a404-4b17-b8f6-9a33ca71bb14
- https://escholarship.org/uc/item/42r093p5
- http://resolver.tudelft.nl/uuid:cff6cd3b-a587-42f2-a3ce-e735aebf87ce
- http://hdl.handle.net/2429/80538
- https://zenodo.org/record/6951481
- http://hdl.handle.net/2117/396576
- http://arxiv.org/abs/2304.01358
- https://digitalcommons.csbsju.edu/honors_theses/14
- https://zenodo.org/record/8011320
- http://oro.open.ac.uk/47792/1/Beyond%20justice%20final.docx
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-192649
- https://scholarsbank.uoregon.edu/xmlui/handle/1794/24785
- http://hdl.handle.net/11583/2955739
- http://www.thesai.org/Downloads/Volume5No11/Paper_16-A_Code_Level_Based_Programmer_Assessment_and_Selection.pdf?height%3D100%%26iframe%3Dtrue%26width%3D100%
- http://dx.doi.org/10.1145/3517133
- http://arxiv.org/abs/2205.12702
- https://ieeexplore.ieee.org/abstract/document/4556964/
- http://hdl.handle.net/11336/152508
- http://cds.cern.ch/record/2627020
- http://hdl.handle.net/10523/2291
- https://surrey.eprints-hosting.org/124486/2/SRI_deposit_agreement.pdf
- http://depts.washington.edu/pettt/papers/reviews/lori.pdf
- http://doi.acm.org/10.1145/3174781.3174784
- https://hdl.handle.net/2152/120742
- http://nlp.csie.ncnu.edu.tw/~shin/acl-ijcnlp2009/proceedings/CDROM/Short/pdf/Short021.pdf
- http://publica.fraunhofer.de/documents/N-266669.html
- https://doi.org/10.1007/s10994-022-06262-0
- http://jhir.library.jhu.edu/handle/1774.2/67617
- https://zenodo.org/record/8026525
- https://digitalcommons.lsu.edu/gradschool_disstheses/5455
- https://digitalcommons.kennesaw.edu/context/dataphd_etd/article/1017/viewcontent/Sayenju_PhD_Dissertation.pdf
- https://trepo.tuni.fi/handle/10024/97660
- https://norma.ncirl.ie/5222/
- http://dx.doi.org/10.21608/jocc.2023.307054
- http://arxiv.org/abs/2309.05227
- http://folk.uio.no/gunnab/publications/Bergersen_et_al.2011%28preprint%29.pdf
- https://doi.org/10.11606/D.3.2016.tde-12072016-084728
- http://proquest.umi.com/pqdweb?did=1604490061&Fmt=7&clientId=58634&RQT=309&VName=PQD
- http://arodes.hes-so.ch/record/9490
- http://arxiv.org/abs/2310.12357
- http://cardinalscholar.bsu.edu/handle/handle/185678
- https://www.repository.cam.ac.uk/handle/1810/295220
- http://hdl.handle.net/1959.13/1347183
- http://dl.acm.org/citation.cfm?doid=2593735.2593737
- https://digitalcollection.zhaw.ch/handle/11475/11161
- https://digitalcommons.montclair.edu/compusci-facpubs/218
- https://hal-upec-upem.archives-ouvertes.fr/hal-01794807
- http://hdl.handle.net/10453/128636
- https://usir.salford.ac.uk/id/eprint/1770/1/ewic_fa96_paper14.pdf
- https://scholarworks.utep.edu/dissertations/AAI13857380
- http://hdl.handle.net/10453/132088
- http://encore.tut.ac.za/iii/cpro/DigitalItemViewPage.external?sp=1001990
- http://gmarceau.qc.ca/papers/Marceau-2010-Measuring-Effectiveness.pdf
- https://escholarship.org/uc/item/9kx2k801
- https://dx.doi.org/10.3390/fi8020026
- http://staff.scm.uws.edu.au/~yan/papers/current/hase09.pdf
- https://aisel.aisnet.org/cgi/viewcontent.cgi?article=1842&amp;context=amcis1998
- http://dx.doi.org/10.26153/tsw/43893
- http://arxiv.org/abs/2212.06008
- https://zenodo.org/record/4314413
- http://www.cs.utah.edu/formal_verification/Gauss/Pages/grt/publications/ppopp14-s3fp.pdf
- https://msdl.uantwerpen.be/conferences/MDEbug/
- https://hal.science/hal-03401683
- https://zenodo.org/record/7555648
- https://www.sciencedirect.com/science/article/pii/S2666557321000318
- https://doaj.org/article/48fc7dcb1c964241b36dcd4fdba31fa7
- http://hdl.handle.net/20.500.11937/3314
- http://hdl.handle.net/20.500.11937/75878
- https://repository.alt.ac.uk/2361/1/PrivateconsultationonCodeofPracticeforLearningAnalytics.pdf
- https://bioling.psychopen.eu/index.php/bioling/article/view/14391
- http://arxiv.org/abs/2206.04615
- https://zenodo.org/record/4134097
- https://doi.org/10.3217/jucs-025-13-1668
- https://eduq.info/xmlui/handle/11515/37712
- https://mural.maynoothuniversity.ie/15662/1/NatalieCulliganThesisPrint.pdf
- http://arxiv.org/abs/2211.13899
- https://ueaeprints.uea.ac.uk/id/eprint/51431/
- http://hdl.handle.net/10292/1515
- https://zenodo.org/record/8131690
- https://cris.maastrichtuniversity.nl/en/publications/621c105c-15d8-4168-97bb-d3740a3ba038
- http://www.scopus.com/inward/record.url?scp=85091452842&partnerID=8YFLogxK
- http://hdl.handle.net/2142/101231
- http://sefm17.fbk.eu/
- http://strathprints.strath.ac.uk/32280/1/10.1.1.105.1767_1_.pdf
- https://digitalcommons.kennesaw.edu/facpubs/1414
- http://upcommons.upc.edu/bitstream/handle/2117/14830/2ndwoss_Micsik.pdf%3Bjsessionid%3D32980FE1A10BFE4AAE5FB099E78435A4?sequence%3D1
- https://arrow.tudublin.ie/scschcomart/59
- http://hdl.handle.net/10230/47267
- https://ojs.aaai.org/index.php/AAAI/article/view/9821