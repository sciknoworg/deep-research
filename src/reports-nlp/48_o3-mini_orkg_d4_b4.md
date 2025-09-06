# Final Report: Ensemble of LLMs Attack Safety Classifiers – A Comprehensive Analysis

*Date: September 5, 2025*

---

## Abstract

This report presents an exhaustive investigation into the use of ensemble strategies by large language models (LLMs) to attack safety classifiers, as well as an evaluation of the robustness of current safety classifiers in the face of ensemble-based attacks. We explore techniques ranging from hybrid ensemble methods to formal logic-based threat specifications, and we analyze both theoretical frameworks and empirical experiments. Drawing insights from recent research that integrates adaptive importance weighting, dynamic thresholding, gradient dispersion, and secure/insecure set partitioning, this document provides a multi-dimensional view into adversarial attack strategies and defense measures. Our analysis synthesizes findings from over forty distinct learnings to offer a coherent roadmap for both offensive and defensive strategies, highlighting avenues for improvement in system scalability, computational efficiency, and cross-domain applicability.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement and Objectives](#problem-statement-and-objectives)
3. [Technical Background and Methodologies](#technical-background-and-methodologies)
   - [Ensemble Attack Techniques](#ensemble-attack-techniques)
   - [Adversarial Training and Optimizations](#adversarial-training-and-optimizations)
   - [Statistical and Formal Frameworks](#statistical-and-formal-frameworks)
4. [Empirical Findings and Benchmarking](#empirical-findings-and-benchmarking)
5. [Trade-offs, Challenges, and System Complexity](#trade-offs-challenges-and-system-complexity)
6. [Future Research Directions and Recommendations](#future-research-directions-and-recommendations)
7. [Conclusion](#conclusion)

---

## 1. Introduction

Recent advancements in large language models (LLMs) have brought robust capabilities in natural language generation and understanding. However, as LLMs become integrated into safety-critical applications, so too does the potential for adversarial exploitation. Safety classifiers are deployed to prevent harmful outcomes from adversarial content or poisoned inputs. This report investigates two inter-related aspects:

- The use of ensembles of LLMs to generate adversarial examples that bypass safety classifiers.
- The resilience and robustness of safety classifiers when attacked by ensemble-based mechanisms.

Adversarial approaches have evolved beyond single-model attacks with methods such as gradient dispersion, secure/insecure set frameworks, and automated ensemble attacks (e.g., AutoAE). The deployment of hybrid ensemble methods leverages diversified model responses to craft more potent adversarial sequences. At the same time, defenders have increasingly relied on techniques that combine formal logic, adaptive training, and optimized multiobjective frameworks to bolster safety measures. Our goal is to synthesize these emerging strategies and offer actionable insights.

---

## 2. Problem Statement and Objectives

### Primary Objectives

- **Investigate Ensemble Based Attack Strategies:** To examine how ensembles of LLMs can collaborate to generate adversarial examples that effectively bypass safety classifiers. Emphasis is given on exploring the technical underpinnings and potential vulnerabilities of current defense measures.

- **Evaluate the Robustness of Safety Classifiers:** Determine the effectiveness of current safety classification frameworks when subjected to complex adversarial ensembles. This includes analyzing the interplay between ensemble diversity, dynamic thresholding, and secure/insecure set approaches.

### Questions Addressed

1. **Attack Strategy Exploration vs. Robustness Evaluation:** The analysis includes both theoretical techniques (e.g., secure set partitioning, gradient dispersion) for ensemble attacks and empirical evaluations of system behavior under these threats.

2. **Technical Methods vs. Overall System Behavior:** Detailed technical methods of constructing attack ensembles, such as automated iterative refinements (AutoAE) and diverse adversarial training (e.g., iGAT), are reviewed along with system-level responses.

3. **Theoretical and Empirical Combination:** Our exploration combines rigorous theoretical frameworks (e.g., formal logic threat specification and multiobjective bilevel optimization) with large-scale empirical experiments validated on benchmarks like ImageNet-Patch, CIFAR datasets, and specialised security datasets (e.g., CICIDS2017).

---

## 3. Technical Background and Methodologies

### Ensemble Attack Techniques

Recent advancements have centered around **hybrid ensemble methods**. These combine *adaptive importance weighting*, dynamic threshold adjustments, and symbolic threat modeling (using Petri nets and causality theory) to improve adversarial performance. Key highlights include:

- **Adaptive PGD and Dynamic Thresholding:** Some ensemble techniques outperform classic adversarial training under non-uniform attack conditions by dynamically adjusting thresholds. However, reliance on such methods may obscure true underlying vulnerabilities and contribute to computational inefficiencies.

- **Secure/ Insecure Set Frameworks:** The notion of partitioning model responses into secure (robust) and insecure (vulnerable) sets has led to nearly perfect detection in some settings. This method aids in reducing the transferability of adversarial examples among ensemble members.

- **Gradient Dispersion and Coordinated Training:** Techniques that intentionally disperse gradients within ensemble architectures (as seen in iGAT) provide significant boosts in adversarial robustness. Empirically, improvements of up to 52% on complex image benchmarks have been observed by targeting high-level feature representations.

- **Automated Construction of Attack Ensembles (AutoAE):** AutoAE stands out by iterating to add effective base attackers in a systematic and provable manner. It achieves near-optimal robustness evaluation across multiple defenses (e.g., 45 defenses in RobustBench) while incurring the cost of iterative computation.

### Adversarial Training and Optimizations

Modern optimization approaches have dramatically reduced the computational burden and enhanced the effectiveness of attacks:

- **Frank-Wolfe and STARS Algorithms:** The utilization of pioneering optimization techniques, such as variants of the Frank-Wolfe framework and Sequential TArget Ranking Selection (STARS) methods, assists in managing query complexities and speeding up convergence. These methods achieve linear convergence properties, substantially reducing runtime.

- **Multiobjective Bilevel Optimization for Data Poisoning:** Through dynamically learned hyperparameters, including ℓ₁ regularization and adaptive strategies, this approach fine-tunes control over the interplay between typical and adversarial distributions. Such strategies help mitigate overly pessimistic robustness assessments by leveraging real-time feedback loops.

- **Composite Adversarial Attack (CAA) Frameworks:** Involving multi-objective optimization over a search space of multiple base attackers (e.g., using NSGA-II), CAA frameworks have been shown to outperform state-of-the-art methods such as AutoAttack by designing rapid and effective ensemble-based attack sequences.

### Statistical and Formal Frameworks

Statistical analysis and formal logic offer complementary views on adversarial threat modeling:

- **ECDF-Based Statistical Measures:** The application of empirical cumulative distribution function (ECDF) measures—such as Kolmogorov-Smirnov, Kuiper, Anderson-Darling, and Wasserstein distances—facilitates quantitative correlations between classifier decision boundaries and anomalous inputs. These have been validated across synthetic datasets (e.g., XOR, Spiral) and realistic security benchmarks (like CICIDS2017).

- **Formal Logical Threat Specifications:** Using first-order and modal logics, researchers are now specifying threat properties that are technology-agnostic. This allows for a systematic pre-deployment sizing of risk, such that designed defenses remain congruent with abstract security properties defined by system architects.

- **Bayesian Information Criterion (BIC)-based Mixture Models:** These unsupervised frameworks detect and remove poisoned samples from the training process, thereby increasing robustness. They provide a way to handle adversarial and noisy data even when clean validation sets are unavailable.

---

## 4. Empirical Findings and Benchmarking

### Benchmark Datasets and Industrial Pilot Studies

Robust benchmarking has been done on datasets such as ImageNet-Patch, CIFAR-10/100, MNIST, and specialized datasets like CICIDS2017. The following distinct outcomes were found:

- **ImageNet-Patch and Physical Domain Validation:** Evaluations on ImageNet-Patch highlight reproducible frameworks that assess both attack efficacy and runtime efficiency, reinforcing the importance of physical validations beyond simulated environments.

- **Empirical Gains on CIFAR and MNIST:** Ensemble approaches like iGAT and hybrid methods (e.g., Adven) have reported robustness improvements of up to 17% on CIFAR datasets, with some techniques achieving more than 91% defense against specific attacks, such as PGD.

- **Industrial Studies at Ericsson Finland:** Agile software development models enhanced with risk-driven security metrics have improved early-phase visibility of security effectiveness. Despite sophistication in visualization and risk estimation, challenges remain with evidence collection in the early stages of product development.

### Comparative Evaluation of Defense Strategies

Multiple ensemble methods have been comparatively assessed to balance computational overhead with robust performance:

- **Bagging and Randomized Ensembles:** Traditional bagging methods, which reduce outlier impacts through bootstrap resampling, have shown promise in mitigating poisoning in tasks like spam filtering and intrusion detection. Randomized defenses provide efficiency benefits but are generally more susceptible to sophisticated, adaptive attacks.

- **Hybrid Architectures and Ensembling Loss Approaches:** Combining ensemble loss mechanisms that exploit mutual information among members have yielded improvements in performance (for example, boosting accuracy in side-channel attacks by up to 6.8% and reducing brute-force operations considerably).

- **Latent Space Attacks:** Innovations such as ADSAttack, which work at the latent space level using affiliated networks and edge-detection, have improved stealth and transferability of adversarial examples compared to dense pixel space modifications.

---

## 5. Trade-offs, Challenges, and System Complexity

### Computational Overhead vs. Robustness

Many ensemble-based defense and attack strategies incur a substantial computational cost. Methods such as AutoAE deliver near-optimal adversarial evaluation but require iterative computation cycles that increase latency. Key trade-offs include:

- **Dynamic Threshold Adaptation:** Adjusting secure/insecure set thresholds introduces additional computational overhead and may hamper convergence speed, posing a challenge for real-time safety systems.

- **Model Complexity and Interpretability:** Increased ensemble complexity, especially when combining symbolic, statistical, and neural methods, risks reduced interpretability. This is critical in safety-critical environments where explanations for decisions must be clear.

### Robustness in LLM Scale Deployments

Large language models inherently possess sequential and contextual complexities that challenge traditional ensemble defenses:

- **Transferability in Transformer Architectures:** Empirical studies indicate that adversarial examples in Transformer-based setups exhibit up to 25.7% higher transferability. Adapting secure/insecure frameworks to token-level operations and integrating gradient regularization into self-attention layers are promising directions.

- **Balancing Statistical Rigor with Real-Time Adaptability:** As seen in ECDF-based methods and formal logical specifications, the need to reconcile high-level statistical insights with operational constraints remains a significant open problem in scaling these methods to LLM architectures.

---

## 6. Future Research Directions and Recommendations

### Integrating Multi-Modal and Cross-Domain Approaches

- **Hybrid Explainable AI:** Future work could examine fusion techniques that integrate interpretable gradient dispersion with formal threat specification. By merging sensor data and textual context, one could design explainable defenses that are both robust and transparent.

- **Hardware-Aware Optimization:** Emerging accelerator-centric architectures, such as FPGA-based systems with RRAM devices, provide an opportunity to integrate robustness measures directly into hardware. This might reduce latency and energy cost during ensemble training and adversarial evaluations.

### Refining Ensemble Construction and Hyperparameter Tuning

- **Automated and Adaptive Construction Strategies:** Continued refinement of automated ensemble methods like AutoAE is vital. Extending the methodology to variations under ℓ₁ norm constraints and dynamically selecting attackers may yield further reductions in query complexity and improved evaluation consistency.

- **Advanced Secure/Insecure Set Mechanisms:** Enhancing secure/insecure partition criteria at both token and higher-level feature representations in Transformer architectures can be an area of significant innovation. Dynamic weight adjustments based on real-time feedback will likely be essential to mitigate adversarial transferability.

### Novel Optimization and Statistical Techniques

- **Multiobjective Bilevel Optimization Enhancements:** The adaptation of bilevel optimization frameworks with adaptive hyperparameter selection (e.g., leveraging ℓ₁ or mixed-norm regularization) should be explored. These methods would ideally balance computational resource distribution, risk evaluation, and model stability.

- **Distributed Meta-Heuristic Frameworks:** Leveraging parallel and distributed optimization techniques, including evolutionary algorithms tailored for heterogeneous platforms (CPU, GPU, FPGA), is a promising research path. This could reconcile the difficulty balance between optimality and resource consumption when scaling ensemble frameworks.

### Broader Application and System-Level Integration

- **Cross-domain Applicability:** The approach of utilizing bagging, ensembling loss, and formal threat specifications in adversarial scenarios with LLMs should be evaluated and adapted for other safety-critical domains (e.g., cybersecurity, smart grid systems).

- **Risk-Driven Hierarchical Models:** Integrating risk-driven hierarchical metrics, as demonstrated in industrial pilot studies, is recommended to enable early detection of vulnerabilities. These systems should be built to fuse top-down risk assessments with bottom-up monitoring data.

---

## 7. Conclusion

The investigation into ensemble-based attacks on safety classifiers reveals both the potent threat posed by such techniques and the promising defense strategies arising from recent research. The integration of adaptive weighting, secure/insecure set frameworks, gradient dispersion, and automated ensemble construction methods offer nearly state-of-the-art performance in adversarial robustness evaluations. However, these advances come with challenges including substantial computational overhead, increased system complexity, and nuanced trade-offs in interpretability.

Future work must address these challenges by developing more integrated, hardware-aware, and explainable solutions that dynamically balance efficiency and security. By synthesizing insights from both theoretical and empirical lenses, this report provides a detailed roadmap for researchers and practitioners seeking to enhance LLM safety classifiers in an environment where adversarial ensemble attacks are increasingly sophisticated.

---

*This report compiles and integrates over forty independent research learnings from cutting-edge adversarial machine learning, providing a detailed reference for ongoing research in ensemble LLM attacks and safety classifier robustness.*

## Sources

- https://publications.cispa.saarland/3526/
- https://doi.org/10.1109/INFOCOMWKSHPS54753.2022.9798325
- https://zenodo.org/record/5505817
- http://publica.fraunhofer.de/documents/N-422824.html
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-21533
- http://hdl.handle.net/11588/876849
- http://www.nusl.cz/ntk/nusl-448078
- https://digitalcommons.memphis.edu/facpubs/2518
- http://arxiv.org/abs/2310.11597
- http://www.cs.qub.ac.uk/%7Ew.liu/KSEM15-252.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4061
- http://etd.adm.unipi.it/theses/available/etd-10162021-103039/
- http://arxiv.org/abs/2105.13530
- http://arxiv.org/pdf/1401.8255.pdf
- http://arxiv.org/abs/2206.04568
- http://pralab.diee.unica.it/sites/default/files/biggio11-mcs.pdf
- https://hdl.handle.net/10356/169803
- https://escholarship.org/uc/item/7rx3k2ck
- https://ojs.aaai.org/index.php/AAAI/article/view/26797
- http://hdl.handle.net/11584/26921
- https://espace.library.uq.edu.au/view/UQ:a86e160
- https://zenodo.org/record/1082947
- https://hdl.handle.net/10356/148567
- http://aaaipress.org/Papers/Workshops/2007/WS-07-05/WS07-05-008.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/25118
- https://hal.science/hal-03353850
- http://faculty.nps.edu/mcarlyle/docs/allocatingcapacity.pdf
- https://escholarship.org/uc/item/1ws1z7k4
- https://hdl.handle.net/11584/321558
- http://resolver.tudelft.nl/uuid:0a1fbc80-ff9a-4590-a7db-ce59799e1c31
- http://hdl.handle.net/10278/3681515
- https://ro.uow.edu.au/eispapers1/3042
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-123546
- http://publica.fraunhofer.de/documents/N-303960.html
- https://doi.org/10.17352/tcsit.000017
- http://hdl.handle.net/11567/1083648
- http://www.iariajournals.org/security/sec_v2_n4_2009_paged.pdf#page=66
- http://hdl.handle.net/11584/104528
- http://hdl.handle.net/11568/136158
- http://pqdtopen.proquest.com/#viewpdf?dispub=27994576
- http://hdl.handle.net/2134/21325092.v1
- https://escholarship.org/uc/item/6tp72870
- https://hdl.handle.net/10356/136863
- http://arxiv.org/abs/2203.07341
- http://arxiv.org/abs/2310.18477
- https://hdl.handle.net/10356/137938
- http://hdl.handle.net/2142/110269
- https://ojs.aaai.org/index.php/AAAI/article/view/26722
- http://hdl.handle.net/11379/551393
- http://www.dicom.uninsubria.it/%7Esabrina.sicari/public/documents/conference/2008_expert.pdf
- https://hal.inria.fr/hal-00978637
- https://norma.ncirl.ie/955/
- https://lirias.kuleuven.be/handle/123456789/167605
- https://link.springer.com/chapter/10.1007/978-3-030-72236-4_13
- http://hdl.handle.net/10.25394/pgs.21585801.v1
- http://hdl.handle.net/10044/1/104225
- http://digital.library.unt.edu/ark:/67531/metadc693390/
- http://resolver.tudelft.nl/uuid:ca0c16eb-2021-4095-a928-337e3dce3997
- https://escholarship.org/uc/item/5sm046wj
- https://escholarship.org/uc/item/70x7h2mk
- https://hdl.handle.net/11584/357302
- https://cea.hal.science/cea-04292759/document
- https://research.sabanciuniv.edu/id/eprint/47219/
- https://dx.doi.org/10.1109/ICCD50377.2020.00056
- https://ojs.aaai.org/index.php/AAAI/article/view/17075
- https://ir.cwi.nl/pub/25192
- https://zenodo.org/record/8006754
- http://infoscience.epfl.ch/record/281094
- https://ojs.aaai.org/index.php/AAAI/article/view/26064
- https://doaj.org/article/b8ef98441c4745989e91d49b544fb021
- https://ojs.aaai.org/index.php/AAAI/article/view/17869
- https://doaj.org/article/c10569972ae043bb9bc9bedf23b358e4
- https://hal.inria.fr/hal-03806425
- https://doi.org/10.1007/978-3-030-58920-2_13
- https://doaj.org/article/b129691a6be54bd598b9f264bdaa02e3
- https://doi.org/10.1109/IJCNN54540.2023.10191889
- http://www2.docm.mmu.ac.uk/STAFF/M.Muyeba/ThreatNet_EMS2008.pdf
- https://doaj.org/article/8879abd584ca43ff964e09b9fdbb3d00
- http://hdl.handle.net/11584/105029
- http://teamcore.usc.edu/papers/2014/Brown_GameSec2014.pdf
- https://hal.archives-ouvertes.fr/hal-03916842/file/2102.10875.pdf
- https://openreview.net/forum?id=PAfnMGXief
- http://dx.doi.org/10.1109/Metrisec.2011.19
- https://discovery.ucl.ac.uk/id/eprint/10132359/
- https://hal.science/hal-02892188/document
- http://hdl.handle.net/11336/114217
- http://orbilu.uni.lu/handle/10993/53045
- http://lyle.smu.edu/%7Emitch/ftp_dir/pubs/jmvl15b.pdf
- http://hdl.handle.net/1773/39901
- https://doaj.org/article/357ae8efb8124b17a368a76fc4c24731
- https://hdl.handle.net/11582/340287
- https://ojs.aaai.org/index.php/AAAI/article/view/26758
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/6449
- http://resolver.tudelft.nl/uuid:4e479a22-f4bc-4319-9cb6-877770596773
- http://hdl.handle.net/2142/104943
- https://hdl.handle.net/10356/166036
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.2169
- http://hdl.handle.net/11591/442611
- https://serval.unil.ch/notice/serval:BIB_CC23329E7FF6
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-193599
- https://espace.library.uq.edu.au/view/UQ:820f318
- https://zenodo.org/record/4840798
- https://www.open-access.bcu.ac.uk/16198/2/research%20paper.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/16955
- https://doaj.org/article/7b93adf29cfb4975b70c64124a8cca42
- https://ojs.aaai.org/index.php/AAAI/article/view/5887
- http://hdl.handle.net/10230/47626
- https://eprints.whiterose.ac.uk/194593/1/SETP_TSG_22_accepted%20%281%29.pdf
- https://doaj.org/article/cde2e25a91594a97af456244d7a58156
- https://hal.archives-ouvertes.fr/hal-03827382/document
- https://ojs.aaai.org/index.php/AAAI/article/view/26738
- http://hdl.handle.net/20.500.11754/67767
- http://hdl.handle.net/2142/104039
- https://ojs.aaai.org/index.php/AAAI/article/view/16843
- https://cris.vtt.fi/en/publications/23388f13-a98e-4104-afc9-28dd5b1156d3
- https://hdl.handle.net/11584/344200
- https://ojs.aaai.org/index.php/AAAI/article/view/17292
- https://tches.iacr.org/index.php/TCHES/article/view/8968
- https://hal.inria.fr/hal-01567601
- http://arxiv.org/abs/2206.07314
- http://arxiv.org/abs/2103.03530
- http://resolver.tudelft.nl/uuid:a2f01150-67ea-484b-ae94-04a2f4c95d9b
- http://raiith.iith.ac.in/6057/
- https://docs.lib.purdue.edu/dissertations/AAI3113762
- https://hdl.handle.net/11573/1671306
- https://ojs.aaai.org/index.php/AAAI/article/view/17050
- https://doi.org/10.3390/fi12110180
- http://pralab.diee.unica.it/sites/default/files/biggio11-smc.pdf
- https://cris.vtt.fi/en/publications/61fd763a-31cf-45e8-af7e-88395c5a428b
- http://arxiv.org/abs/2206.06737
- https://research.tue.nl/en/publications/f9fe56cc-dc5c-4122-8fe7-7f871e3cc6cb
- https://cris.vtt.fi/en/publications/cd1416de-0dd6-4408-850e-f67ea2d29048
- https://hal.archives-ouvertes.fr/hal-02892188/document
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-19847
- https://www.neliti.com/publications/426503/reinforced-cost-effective-architecture-for-fault-tolerance-mechanism-through-met
- http://hdl.handle.net/1773/48151
- http://resolver.tudelft.nl/uuid:a25715d5-f301-4027-9e6e-ec59cef1c73f
- http://hdl.handle.net/11250/253097
- https://digital.library.unt.edu/ark:/67531/metadc896490/
- https://digitalcommons.odu.edu/ece_etds/229
- http://hdl.handle.net/2117/166417
- https://ojs.aaai.org/index.php/AAAI/article/view/5753
- http://hdl.handle.net/1854/LU-8663504
- https://zenodo.org/record/8050866
- https://hal.inria.fr/hal-03772929/file/512058_1_En_14_Chapter.pdf
- https://digitalcommons.unl.edu/dissertations/AAI30488606
- https://hal.inria.fr/hal-03360526
- http://www.loc.gov/mods/v3
- https://cris.vtt.fi/en/publications/c92d5d74-6dd8-4bd5-8014-0179e7d91895