# Final Report: Sampling Q&A for Eliminating Hallucinations and Enabling Instance Separation of Personal Facts in LLMs

This report presents a comprehensive investigation into the dual research objectives of (1) utilizing sampling Q&A techniques to eliminate hallucinations in large language models (LLMs) and (2) achieving robust instance separation of personal facts from non-personal content. Drawing on extensive interdisciplinary research—including clinical neuroimaging, dynamic post‐processing frameworks, and privacy-preserving machine learning—we synthesize a multi-layered strategy that spans both training-based adjustments and agile post‐processing interventions.

---

## 1. Introduction

Large language models have witnessed tremendous progress, yet they remain vulnerable to two persistent challenges: hallucinations (the generation of spurious or unverified outputs) and the inadvertent mixing of personal and non-personal data. Both issues have practical implications—from misinformation dissemination to privacy violations. Recent inquiries have focused on a promising approach referred to as "sampling Q&A," which, when properly applied, not only reduces hallucinations but also aids in the systematic isolation of personal facts. This report elaborates on this approach by defining the key concepts, reviewing analogous methodologies across diverse domains, and proposing integrated solutions.

### 1.1 Defining Key Concepts

- **Sampling Q&A:** The term can be interpreted in two main ways. It may involve a novel methodology to **select question–answer (Q&A) pairs dynamically during training and inference** that focuses on detecting and rapidly correcting hallucinations. Alternatively, it could also refer to a post‐processing technique that leverages model logit outputs and statistical evaluation methods to filter out spurious inaccuracies. Our approach advocates for a hybrid model, integrating both training modifications and dynamic post‐processing for real-time correction.

- **Instance Separation of Personal Facts:** This process involves isolating personal information from the broader knowledge encapsulated within an LLM. The goal is twofold: to minimize the leakage of private data and to ensure that personal facts are compartmentalized in a way that they do not contaminate general inferential outputs. Here, techniques that range from systematic sampling in qualitative research to embedding privacy metrics into cost functions all contribute to a robust separation framework.

---

## 2. Sampling Q&A to Mitigate Hallucinations

### 2.1 Theoretical Foundations and Rationale

Hallucinations in LLMs often arise due to an imbalance between robust long-term training and rapid inference dynamics. Several studies have demonstrated that dynamic post‐processing methods, such as the "A Stitch in Time Saves Nine" approach, can reduce hallucination rates dramatically—from nearly 47.5% to below 15%—by actively monitoring model logit outputs. The integration of sampling Q&A into the workflow harnesses methodologies from both training-based improvements and agile post-processing, ensuring that the model’s responses are continuously realigned with verified knowledge.

#### 2.1.1 Training-Based vs. Post‐Processing Interventions

- **Training-Based Approaches:** Fine-tuning on curated datasets (including Q&A pairs) can impose long-term robustness. However, these methods are often expensive, resource intensive, and subject to overfitting. Innovations such as prefix-tuning have emerged as alternatives, offering comparable accuracy while enhancing generalization and reducing latency benefits.

- **Post‐Processing Approaches:** Post-processing frameworks, exemplified by the HaELM method in vision-language models, enable rapid corrections after initial output generation. These methods are scalable and locally deployable, although they may yield transient benefits compared to deeply embedded training modifications. The integration of sampling Q&A techniques can serve as a corrective overlay, balancing immediacy with accuracy.

### 2.2 Dynamic Q&A Sampling Algorithm

One promising avenue involves **adaptive selective Q&A sampling algorithms**. Much like techniques seen in brain–computer interfaces (BCIs) for real-time state detection, these algorithms utilize lightweight predictive models (including RNNs and SVMs) to evaluate the veracity of ongoing responses. Key characteristics include:

- **Iterative Assessment:** Each generated answer is subjected to a Q&A sampling routine where auxiliary questions interrogate the core output, ensuring internal consistency and alignment with known facts.
- **Dynamic Feedback Loops:** Drawing inspiration from clinical cognitive training (e.g., adaptive feedback in digital therapeutics for auditory verbal hallucinations), the model updates its internal state in real time based on sampling outcomes.
- **Quantitative Benchmarks:** Utilizing metrics (e.g., recall rates around 88% and mitigation effectiveness near 57.6%) derived from multinational datasets helps threshold the sampling process, ensuring that only quality, non-hallucinatory outputs pass through.

### 2.3 Implementation Considerations

Implementing sampling Q&A involves several technical challenges:

- **Latency and Scalability:** Analogous to real-time embedded systems that achieve latencies as low as 1.46 ms on dedicated hardware, the sampling module must be optimized to support rapid evaluation without significant processing overhead.
- **Integration with Existing Pipelines:** Hybrid models must seamlessly integrate internal training modifications with post-processing filters. Adaptive frameworks inspired by dynamic noise injection strategies allow for efficient resource management.
- **Evaluation Metrics:** Hierarchical hybrid statistical models that combine trigram frameworks with sub-word feature analysis offer a path towards unified evaluation, ensuring that the sampled responses adhere to predefined standards of factual accuracy.

---

## 3. Instance Separation of Personal Facts

### 3.1 Privacy Concerns and the Need for Instance Separation

The leakage of personal facts poses significant ethical and regulatory challenges. Importantly, isolated personal information may inadvertently amplify biases or serve as a conduit for identity exposure. To mitigate these risks, research has increasingly focused on techniques that explicitly separate personal facts from general outputs.

### 3.2 Methodologies for Instance Separation

Several cross-disciplinary strategies have emerged:

#### 3.2.1 Linguistic Frameworks and Semantic Parsing

- **Systemic Functional Linguistics (SFL):** By parsing texts through pronominal and determination systems, SFL-based methods can differentiate interpersonal distance and isolate nuanced personal information. Hierarchical systemic representations allow for a degree of granularity that is crucial for separating sensitive data.
- **Hybrid Language Models:** Approaches using hierarchical attention-based models (HAMs) and transformer architectures (e.g., PRIDE) have shown superior performance by integrating zero-shot learning techniques and discriminative rerankers. These methods are capable of inferring implicit demographic details from dialogue, an essential component in identifying personal facts.

#### 3.2.2 Embedding Privacy Metrics into Model Cost Functions

- **Privacy-Preserving Cost Functions:** Embedding formal privacy metrics—such as Kullback–Leibler divergence, Fisher information, and mutual information—directly into the training loss functions allows the model to quantify and manage potential privacy violations. Such methods provide a controlled balance between performance and privacy preservation.
- **Differential Privacy Adjustments:** Emerging techniques like the personalized sample Laplace mechanism allow for the injection of calibrated noise, ensuring that the sensitivity of personal data is appropriately masked during both training and inference.

#### 3.2.3 Multi-Party and Distributed Data Architectures

- **Hybrid Anonymization Approaches:** Frameworks that leverage k-anonymity, l-diversity, and cryptographic techniques on multi-party data architectures enable the model to process sensitive information without full exposure of individual records. These approaches draw an analogy with decentralized frameworks used in smart grid metering and have shown promise in safeguarding data in digital health applications.
- **Instance-Based Data Partitioning:** By partitioning personal facts into discrete instances, each stored and processed separately, systems can further reduce the risk of information leakage. The key is to achieve accurate segmentation while maintaining robust inference performance.

### 3.3 Integration with Sampling Q&A

The coupling of instance separation with sampling Q&A methods enhances both accuracy and privacy. For instance:

- **Dual-Stage Processing:** Initially, sampling Q&A mechanisms interrogate baseline output for factual consistency. In a subsequent stage, detected personal content is flagged and processed using instance separation techniques. This two-tiered approach minimizes both hallucination and accidental personal data coupling.
- **Context-Sensitive Inference:** The use of contextual models that leverage both sub-word and sentence-level features (a strategy borrowed from hierarchical hybrid statistical models) ensures that personal and non-personal facts are correctly identified and routed through separate processing pipelines.

---

## 4. Integration of Approaches and Practical Considerations

This section provides a roadmap for integrating sampling Q&A and instance separation into a unified LLM framework. While the methodologies are distinct, their synergy is critical for achieving robust and privacy-aware systems.

### 4.1 A Unified Framework

Integrating the strategies outlined earlier, the following blueprint is proposed:

1. **Initial Output Generation:** The LLM generates a preliminary answer which may contain both verified and potentially hallucinatory information.

2. **Dynamic Q&A Sampling Module:** A lightweight, on-the-fly sampling mechanism queries the model with targeted questions. This module employs Bayesian committee models and Kalman filter-inspired controllers to detect inconsistencies, rapidly flagging potential inaccuracies.

3. **Privacy Filtering Layer:** Once the system identifies personal data, an embedded privacy filter (utilizing dynamic noise injection techniques and advanced anonymization schemes) segregates these data points into an isolated instance layer.

4. **Post‐Processing Adjustment:** Finally, a post‐processing step—similar to the HaELM framework—applies corrective adjustments to both the hallucination-related inaccuracies and the borderline cases of personal fact leakage.

### 4.2 Challenges and Trade-Offs

Several challenges remain:

- **Computational Overhead:** The addition of both a dynamic sampling module and a privacy filtering layer introduces extra latency. Optimizations must be pursued, potentially by tailoring embedded hardware solutions or leveraging efficient adaptive clustering methods from BCI research.

- **Scalability:** With models deployed in diverse real-time settings, ensuring that the sampling and instance separation modules scale without compromising response times is critical. Techniques used in adaptive signal processing and real-time spectral clustering might offer solutions.

- **Evaluation and Metrics:** Consistent, rigorous evaluation frameworks are needed. The integration of metrics from both hallucination detection (e.g., recall rates, DET curves) and privacy protection (e.g., differential privacy guarantees) is essential to validate system performance.

- **Ethical and Regulatory Concerns:** Implementing comprehensive personal fact separation necessitates a robust dialogue between AI practitioners, legal experts, and domain specialists. Transparent evaluation metrics and traceable processing pipelines will be indispensable.

---

## 5. Future Directions and Recommendations

Based on our integrated review, several avenues for future research and system improvement emerge:

- **Enhanced Closed-Loop Feedback:** Emulate dynamic neuromodulatory techniques (such as rTMS parameters adjusted based on neuroimaging feedback) to develop a closed-loop system that continuously optimizes both factual accuracy and privacy preservation.

- **Hybrid Training and Post‐Processing Models:** Further research could focus on establishing hybrid frameworks that natively incorporate dynamic Q&A sampling during fine-tuning, thus reducing the reliance on post-processing corrections over time.

- **Advanced Benchmarking:** Develop multidimensional benchmarks that factor in both hallucination elimination and personal fact isolation. This may include constructing datasets that specifically highlight the presence of sensitive information and the propensity for hallucination.

- **Cross-Domain Applications:** Techniques from digital mental health, where Experience Sampling Methods (ESM) and dynamic cognitive training have been successfully applied, can inspire further modifications to the Q&A sampling strategy, making it more attuned to the ephemeral nuances of human communication.

- **Privacy-Aware Adaptive Learning:** Incorporate state-of-the-art privacy preserving machine learning techniques (e.g., adaptive differential privacy schemes) directly into the language model's parameters.

---

## 6. Conclusion

In summary, the integration of sampling Q&A methodologies and instance separation of personal facts presents a promising pathway for resolving two persistent challenges in LLMs: hallucination reduction and privacy protection. By leveraging dynamic sampling techniques inspired by real-time neuromodulation and adaptive signal processing, together with sophisticated privacy-preserving filters, it is possible to engineer systems that are both accurate and ethically resilient.

The proposed unified framework combines processing stages—from rapid Q&A sampling to nuanced instance separation—while addressing computational, scalability, and ethical challenges. Future research should advance these techniques through fine-tuning, hybrid models, and robust evaluation metrics that reflect both technical performance and human-centric requirements.

This report synthesizes learnings from multiple domains including neuroscience, deep learning, digital therapeutic approaches, and privacy engineering, offering a roadmap for deploying next-generation LLMs that not only minimize hallucinations but also rigorously enshrine personal data into separable, secure instances.

---

## References and Analogous Research

Although this report synthesizes research findings from a variety of domains without citing specific authors, parallel works have outlined strategies in areas such as:

- Dynamic post‐processing for error correction (e.g., using model logits for real-time detection).
- Privacy-preserving cost function design (embedding KL divergence, mutual information metrics).
- Adaptive signal processing in brain–computer interfaces to manage nonstationarity.
- Digital therapeutics in computational psychiatry (e.g., the Temstem app and experience sampling methodologies).

Further cross-disciplinary work is recommended to refine these approaches and validate their efficacy in practical, large-scale deployments.

---

By integrating these diverse approaches, the community can move towards developing LLMs that not only generate more reliable outputs but do so in a manner that respects and preserves individual privacy—a necessary evolution in the age of pervasive AI.

*End of Report*

## Sources

- https://www.repository.cam.ac.uk/handle/1810/276415
- https://research.rug.nl/en/publications/8a853126-a7d4-4d3d-a7e3-8313cf41f139
- https://ejurnalmalahayati.ac.id/index.php/MAHESA/article/view/11177
- http://hdl.handle.net/10400.4/2175
- https://doaj.org/toc/1932-6203
- http://arxiv.org/abs/2205.11206
- http://hdl.handle.net/10.1184/r1/6473528.v1
- http://hdl.handle.net/10150/663026
- http://fampra.oxfordjournals.org/content/13/6/522.full.pdf
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27687
- https://hdl.handle.net/11370/e00f2584-9906-4128-ba66-d143f9de3de3
- https://hal.sorbonne-universite.fr/hal-02125141/file/document.pdf
- http://dx.doi.org/10.18725/OPARU-33785
- http://arxiv.org/pdf/1202.3461.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0920996413000637/MAIN/application/pdf/f71834b53a076ca1ae346090467546aa/main.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1035.9227
- http://eprints-phd.biblio.unitn.it/1881/3/Thesis_Firoj_Alam.pdf
- https://research.sabanciuniv.edu/id/eprint/41205/1/10357179_Torkamani_Azar__Mastaneh.pdf
- http://arxiv.org/abs/2112.03254
- https://escholarship.org/uc/item/2094c6pt
- https://ojs.aaai.org/index.php/AAAI/article/view/6518
- http://ieeexplore.ieee.org/document/7410511/
- https://zenodo.org/record/5871834
- http://ijnngt.org/upload/journal5/paper4.pdf
- http://hdl.handle.net/10.1371/journal.pone.0207714.g001
- https://scholarexchange.furman.edu/scjas/2022/all/88
- http://people.cs.pitt.edu/~forbesk/papers/spcomm11.pdf
- http://arxiv.org/abs/2308.15126
- https://research.rug.nl/en/publications/92816b6d-532d-471c-abf4-47a828797700
- https://research-repository.st-andrews.ac.uk/bitstream/10023/4783/1/insel2013neuroscibehaviourrev2438.pdf
- http://www.managementmarketing.ro/pdf/articole/72.pdf
- https://research.rug.nl/en/publications/df456073-536a-41b3-bfdc-8108a34965e3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.431.8529
- https://publications.inschool.id/index.php/icash/article/view/716
- https://cea.hal.science/cea-01883271/document
- http://www.lrec-conf.org/proceedings/lrec2002/pdf/50.pdf
- https://doaj.org/article/5294c3daac9d4a61b811f3b09808603e
- http://hdl.handle.net/2262/93721
- https://espace.library.uq.edu.au/view/UQ:82344
- https://research.rug.nl/en/publications/e00f2584-9906-4128-ba66-d143f9de3de3
- https://nsuworks.nova.edu/tqrc/eleventh/day1/2
- https://nbn-resolving.org/urn:nbn:de:gbv:27-dbt-20221216-092407-006
- https://boris.unibe.ch/69085/
- http://hdl.handle.net/10356/78845
- http://hdl.handle.net/10044/1/46109
- http://arxiv.org/abs/2211.15324
- https://doi.org/10.1093/schbul/sby103
- https://scholarcommons.usf.edu/etd/5394
- https://orca.cardiff.ac.uk/id/eprint/136049/1/Santamaria.%20Towards%20a%20personalized%20multi-domain.pub.pdf
- http://arxiv.org/abs/2211.03698
- https://hdl.handle.net/10356/146327
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.9354
- http://mitras.ece.illinois.edu/research/2014/HWMD_HICONS2014_draft.pdf
- https://figshare.com/articles/Comparison_of_different_speech_separation_models_with_respect_to_methodology_used_/6006164
- http://purl.tuc.gr/dl/dias/1C94DA49-2645-4D31-BDDB-260D98E52C8B
- https://juser.fz-juelich.de/record/889307
- https://repository.essex.ac.uk/32181/
- http://ezproxy.uws.edu.au/login?url=http://doi.org/10.1177/0081175012460852
- https://doi.org/10.1080/21642850.2022.2119144
- http://arxiv.org/abs/2307.03987
- https://serval.unil.ch/notice/serval:BIB_51D2849DE969
- http://arxiv.org/abs/2210.15042
- http://arxiv.org/abs/2209.09619
- https://hal.archives-ouvertes.fr/hal-01375948
- http://pqdtopen.proquest.com/#viewpdf?dispub=27834758
- https://doaj.org/article/f6a40d6618e1474fb2872ca911d0cba8
- https://doi.org/10.1109/NER.2015.7146548
- https://research.rug.nl/en/publications/effectiveness-of-cognitive-therapy-with-coping-training-for-persistent-auditory-hallucinations(2285d499-f893-4805-bf5a-fdb4a606f43e).html
- http://hdl.handle.net/1807/89264
- https://research.gold.ac.uk/id/eprint/26340/1/sr.pdf
- https://hdl.handle.net/10356/153057
- http://journals.sfu.ca/jmde/index.php/jmde_1/article/download/266/254/
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050915003981/MAIN/application/pdf/5db723f436b452ac53b3fe7d2b44c0db/main.pdf
- http://bmjopen.bmj.com/content/8/3/e020537.full.pdf
- http://arxiv.org/abs/2311.01463
- https://research.gold.ac.uk/id/eprint/24700/1/esm.final.pdf
- http://hdl.handle.net/21.11116/0000-000B-3FE1-1
- http://www.scopus.com/inward/record.url?scp=85160926453&partnerID=8YFLogxK
- http://hdl.handle.net/10453/132790
- https://hdl.handle.net/1820/e48b5a52-2c2b-43d1-8bb0-66b6102a24b4
- https://doaj.org/article/42f4feac1f244430834da16f5d886664
- https://eprints.gla.ac.uk/318945/1/318945.pdf
- https://doaj.org/article/947d8d0900a74589b67dff277aee3c92
- http://methodos.hypotheses.org/1795
- https://doaj.org/article/400b609441b14c7abb99aa419f20a394
- https://digitalcommons.usf.edu/usf_patents/1287
- https://hal-supelec.archives-ouvertes.fr/hal-00778752
- https://doaj.org/toc/2213-1582
- http://resolver.tudelft.nl/uuid:dae7367d-4758-474d-b2e7-85aedf6ec867
- http://arxiv.org/abs/2309.05217
- https://research.rug.nl/en/publications/8e2ecc8c-2a2d-4b6b-91d9-6ee5a6e77de2
- https://hdl.handle.net/1813/111942
- http://hdl.handle.net/10068/998449
- https://www.repository.cam.ac.uk/handle/1810/287951
- https://publikationen.bibliothek.kit.edu/1000136239
- http://hdl.handle.net/10150/662571
- https://zenodo.org/record/7068726
- https://zenodo.org/record/5888356
- http://surveypractice.org/index.php/SurveyPractice/article/download/43/pdf/
- http://hdl.handle.net/10453/12715
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0896627311009342/MAIN/application/pdf/6288e91292fd9294ebc23aefcdbed8fd/main.pdf
- https://hal.archives-ouvertes.fr/hal-02318237/document
- https://doaj.org/article/8cb72703527645d59856e0049c33c7f7
- https://doaj.org/article/6b979acc2eca411085947f956bc62310
- https://cronfa.swan.ac.uk/Record/cronfa59258
- https://doi.org/10.1034/j.1600-0447.2003.00102.x
- http://hdl.handle.net/10.1371/journal.pgph.0002817.t001
- https://doaj.org/article/9b599c1baaaa41ffac3636e54e95db0e
- https://escholarship.umassmed.edu/gsn_pp/117
- http://www.scopus.com/inward/record.url?scp=84916627980&partnerID=8YFLogxK
- http://hdl.handle.net/2434/780827
- https://doi.org/10.1080/14737167.2019.1632194
- http://hdl.handle.net/10453/152651
- https://doi.org/10.5445/IR/1000122802
- http://hdl.handle.net/10.26174/thesis.lboro.14974833.v1
- https://escholarship.org/uc/item/2hp7g04z
- http://arrow.monash.edu.au/hdl/1959.1/930546
- http://hdl.handle.net/2262/86116
- https://dspace.library.uu.nl/handle/1874/410666
- https://hdl.handle.net/1871.1/731fceb3-bf78-4492-b000-8187586525fb
- http://d-scholarship.pitt.edu/28101/1/Johnson_Geoffrey_dissert_6_2016.pdf
- https://doaj.org/article/3520cd1b215441d1b05516840336d61f
- https://ddd.uab.cat/record/204148
- https://www.zora.uzh.ch/id/eprint/219915/
- http://hdl.handle.net/1959.13/923866
- https://commons.clarku.edu/faculty_psychology/372
- https://doaj.org/article/2da2507b312047bca867e2b172c6ebf6
- https://scholarcommons.sc.edu/aii_fac_pub/583
- http://hdl.handle.net/10.1371/journal.pone.0202473.t002
- http://www.loc.gov/mods/v3
- http://www.wseas.us/e-library/conferences/brazil2004/papers/470-266.pdf
- http://arxiv.org/abs/2307.15343
- http://hdl.handle.net/11573/1352746
- http://hdl.handle.net/2066/91354
- http://cercor.oxfordjournals.org/content/17/11/2733.full.pdf
- http://repository.poltekkes-smg.ac.id//index.php?p=show_detail&id=17616
- http://hdl.handle.net/10.1371/journal.pone.0202473.t003
- http://dx.doi.org/10.1038/tp.2012.114
- http://hdl.handle.net/11582/312127
- https://zenodo.org/record/2563163
- https://strathprints.strath.ac.uk/65152/1/Pratt_Hall_Springer_2018_Biomarkers_in_neuropsychiatry.pdf
- http://hdl.handle.net/1928/10343
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:37067841
- http://hdl.handle.net/1959.14/45403
- http://resolver.tudelft.nl/uuid:c8069976-ffd6-47fa-a28c-5c66dab991c6
- http://hdl.handle.net/21.11116/0000-000A-3C9E-2
- http://hdl.handle.net/11380/1264940
- https://dare.uva.nl/personal/pure/en/publications/time-to-get-personal-the-impact-of-researchers-choices-on-the-selection-of-treatment-targets-using-the-experience-sampling-methodology(5959d884-889c-46d1-8cbf-70abd2b2670b).html
- http://hdl.handle.net/11582/328152
- https://hal.science/hal-03812319/document
- http://hdl.handle.net/10.1371/journal.pone.0206236.g002
- https://www.era.lib.ed.ac.uk/bitstream/handle/1842/3980/Brockmann2009.pdf%3Bjsessionid%3DF51F6963D123345817DC11F4FDB7F023?sequence%3D1
- https://research.rug.nl/en/publications/5fc5ac7e-3e65-4528-be98-584827c1912d
- https://doaj.org/article/e9573bbc909645c4b3eff357a2468a80
- http://hdl.handle.net/1842/3980
- http://hdl.handle.net/1842/1080
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0920996412000357/MAIN/application/pdf/113ccd2d1af2ff4ccc1910ee52deb3a3/main.pdf
- https://research.rug.nl/en/publications/2285d499-f893-4805-bf5a-fdb4a606f43e
- https://hal.archives-ouvertes.fr/hal-03767722
- http://resolver.tudelft.nl/uuid:cfd1595d-290b-4a8d-a704-00af8e243596
- http://eprints.usq.edu.au/39997/
- http://hdl.handle.net/10316/47464
- https://hdl.handle.net/11352/4671
- https://doaj.org/article/eace3bec06224498b64c4979b5839868
- http://infoscience.epfl.ch/record/87379
- http://wing.comp.nus.edu.sg/~antho/W/W13/W13-4009.pdf
- https://doaj.org/toc/1875-6883
- https://research.rug.nl/en/publications/414692cd-7a7b-4e39-813b-b14a7b2949e3
- https://research.rug.nl/en/publications/training-switching-focus-with-a-mobileapplication-by-a-patient-suffering-from-avh-a-case-report(20ea038a-38f8-4df1-bd2b-0ac17098913e).html
- https://dspace.library.uu.nl/handle/1874/362415
- https://doi.org/10.13094/SMIF-2019-00014
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll127/id/5641
- http://creativecommons.org/licenses/by-nc-sa/2.0/uk/
- http://hdl.handle.net/10447/98221
- http://d-scholarship.pitt.edu/22918/
- https://research.vu.nl/en/publications/3a3337c8-dcc2-46b3-b892-b3a2fe8df9d3
- http://hdl.handle.net/10068/950224
- http://hdl.handle.net/10.36227/techrxiv.24227851.v1
- https://doi.org/10.7748/nr2004.07.12.1.47.c5930
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.7217
- https://ueaeprints.uea.ac.uk/id/eprint/64586/
- https://doaj.org/article/0a001b43dc6f4f81ba3722b94def5d18
- http://pqdtopen.proquest.com/#viewpdf?dispub=3401733
- https://doi.org/10.1080/21520704.2016.1205698
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0149763413000821/MAIN/application/pdf/6430464cbcbe8ccae18c10fb1aaaf37d/main.pdf
- http://disi.unitn.it/moschitti/articles/2011/TALP2011-din.pdf
- http://d-scholarship.pitt.edu/22561/
- https://eprints.ucm.es/id/eprint/57348/1/Cid-L%C3%B3pez-Linguistic%20multi-criteria.pdf
- http://hdl.handle.net/10.1184/r1/6473081.v1
- https://digitalcommons.aaru.edu.jo/cgi/viewcontent.cgi?article=1497&amp;context=amis
- http://hdl.handle.net/1807/70247
- http://ezproxy.uws.edu.au/login?url=http://onlinelibrary.wiley.com/doi/10.1111/jan.12163/pdf
- https://research.rug.nl/en/publications/90a03c24-b22d-4cbf-86ce-eb8c053c368f
- https://doaj.org/article/eec95b1fdcdd40d99f990e272069a997
- http://arodes.hes-so.ch/record/870
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1116%26context%3Dlti
- https://hdl.handle.net/1956/23544
- http://hdl.handle.net/10.1184/r1/6473078.v1
- http://arxiv.org/abs/2203.09424
- https://doaj.org/article/8ececf13360c475aaae8ac6df5adceec
- http://hdl.handle.net/10044/1/99427
- http://hdl.handle.net/2142/38387
- http://nrs.harvard.edu/urn-3:HUL.InstRepos:37298276
- https://escholarship.org/uc/item/2g47n9jk
- http://hdl.handle.net/1773/48052
- https://doaj.org/toc/2071-1050
- https://escholarship.org/uc/item/57q0t1jf
- http://www.umiacs.umd.edu/%7Ejbg/docs/jbg-mlslda-2010.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.3376
- http://dx.doi.org/10.1016/j.cose.2011.12.003
- https://doi.org/10.1093/schbul/sby171
- http://arxiv.org/abs/2110.08501
- http://repository-tnmgrmu.ac.in/6324/1/410211711dharmaraj.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.283
- https://ojs.aaai.org/index.php/AAAI/article/view/17590
- https://eprints.lancs.ac.uk/id/eprint/172566/
- http://hdl.handle.net/10807/159526
- https://ojs.aaai.org/index.php/AAAI/article/view/9821
- http://hoschl.cz/files/4552_cz_klirova_rtms_eanp.pdf
- http://www.iiia.csic.es/~vtorra/publications/unrestricted/confEUROFUSE.1999.188.pdf
- http://eprints.utm.my/id/eprint/76551/
- http://www.speech.kth.se/~annah/courses/speech/annah_termpaper_05.pdf