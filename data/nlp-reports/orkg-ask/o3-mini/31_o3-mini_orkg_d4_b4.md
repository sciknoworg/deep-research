# Automatic Jailbreak Prompt Generation for Large Language Models: An In-Depth Analysis

*Author: Expert Research Analyst*

*Date: 2025-09-05*

---

## Table of Contents

1. [Introduction](#introduction)
2. [Overview of Jailbreak Prompt Generation](#overview-of-jailbreak-prompt-generation)
3. [Empirical Findings and Vulnerability Analysis](#empirical-findings-and-vulnerability-analysis)
4. [Evaluation Metrics and Multi-Dimensional Criteria](#evaluation-metrics-and-multi-dimensional-criteria)
5. [Architectural and System-Level Considerations](#architectural-and-system-level-considerations)
6. [Defensive Approaches and Mitigation Strategies](#defensive-approaches-and-mitigation-strategies)
7. [Hybrid and Advanced Detection Mechanisms](#hybrid-and-advanced-detection-mechanisms)
8. [Additional Considerations and Future Directions](#additional-considerations-and-future-directions)
9. [Conclusion](#conclusion)

---

## Introduction

The evolution of Large Language Models (LLMs) has been paralleled by increasingly sophisticated techniques to both exploit and defend against vulnerabilities. One such critical area of study involves the automatic generation of jailbreak prompts, which aim to bypass the robust alignment and guardrails implemented in state-of-the-art LLMs, such as GPT-3.5, GPT-4, and open-source alternatives. This report provides a comprehensive analysis of the key findings from extensive research, highlighting empirical studies, evaluation metrics, system architectural choices, and both defensive and offensive methodologies related to jailbreak prompt generation.

## Overview of Jailbreak Prompt Generation

Automatic jailbreak prompt generation is centered on the identification and exploitation of vulnerabilities within LLM architectures. Adversaries leverage techniques such as prompt injection, privilege escalation, and scenario nesting. Recent large-scale empirical studies (e.g., the analysis of 6,387 jailbreak prompts collected over six months across four platforms) have demonstrated near-perfect attack success rates (up to 0.99) for specific prompts against models like ChatGPT and GPT-4. These prompts often persist in the wild for extended periods (over 100 days), evidencing both the durability and efficiency of these adversarial techniques.

The generation tactics include genetic algorithms for adversarial prompt optimization, prompt rewriting, and scenario nesting as exemplified in systems like ReNeLLM. In parallel, adversaries have expanded their domain into code-related vulnerabilities by adapting these strategies for static code analysis and trojan detection. This broadening of attack surfaces necessitates multi-pronged defense strategies.

## Empirical Findings and Vulnerability Analysis

Empirical work shows that automated techniques can rapidly generate universal adversarial jailbreak prompts with remarkable efficiency. Key insights include:

- **Near-Perfect Success Rates:** Empirical evidence demonstrates that some jailbreaking techniques achieve up to a 99% success rate on proprietary LLMs (e.g., ChatGPT, GPT-4) across multiple forbidden scenarios with high evaluation sample sizes.

- **Persistent Online Presence:** Certain prompt strategies endure in online forums and communities for over 100 days, making them a lasting threat.

- **Deep Vulnerability Coverage:** The heavy-tailed exploitation pattern observed in software security studies indicates that a small percentage of vulnerabilities (5–10%) account for the majority (over 90%) of successful attacks. This trend is reflected in LLMs, where a handful of sophisticated strategies cause disproportionate harm.

- **Trade-offs in Robustness:** Stronger LLMs inherently carry increased safety risks. However, these models are also more amenable to targeted defense mechanisms through advanced alignment and guardrail systems. Comparative research demonstrates that prompt-based attacks on models from the GPT-3 family are more susceptible than open-source models, which typically lack comprehensive safeguards.

- **Exploiting Alignment Loopholes:** Reverse engineering of semantic firewalls and self-deception techniques have achieved significant bypassing capabilities (86.2% success on GPT-3.5-Turbo and 67% on GPT-4) further stressing the importance of integrated defensive mechanisms.

## Evaluation Metrics and Multi-Dimensional Criteria

Assessing the efficacy and novelty of jailbreak prompts requires an evaluation framework that parallels metrics used in software security and risk management. The following metrics are central to this evaluation:

- **Code-Level Metrics and Attack Surface Quantification:** Adaptations of software vulnerability measures like AvgCyclomatic and CountDeclMethod can quantify architectural vulnerabilities. These metrics, when combined with traditional text mining methods (e.g., bag-of-words, word2vec, fastText embeddings), help to capture the complexity of adversarial prompts.

- **Success Likelihood and Operational Impact:** Multi-dimensional criteria that account for dynamic attack likelihood, potential real-world harm, and computational overhead are essential. Quantitative models, such as those adapted from IDS effectiveness and risk management frameworks (including mGQM and SLAM), enable holistic evaluations that not only consider the bypass success but also contextual harm.

- **Latency and Computational Overhead:** Evaluations using low-latency inference frameworks (e.g., InfAdapter) show that adaptive resource allocation can reduce service level objective (SLO) violations and operational costs. These metrics are crucial when considering the integration of additional statistical defenses like MoJE into high-throughput environments.

- **False Positives and Detection Accuracy:** Metrics from advanced interpretability techniques (LIME vs. SHAP) offer insights for quantifying feature importance and enable a deeper understanding of classifier decisions within vulnerability detection frameworks.

## Architectural and System-Level Considerations

System-level design choices strongly influence both the computational efficiency and the security posture of LLMs. Significant findings include:

- **Data Structures and Source Code Complexity:** Variations in data structures (e.g., DBM, CRDZone, CRDArray) and contrasting database implementations (MongoDB vs. PostgreSQL) significantly affect processing times and resource overhead. Optimal architectural trade-offs demand a holistic design philosophy.

- **Decentralized and Adaptive Control:** Advanced robust adaptive control frameworks, including those integrating System Level Synthesis, iterative LMI approaches, and decentralized optimization (using ADMM or column generation), are being examined for their capacity to manage variability, latency, and distributed computation. Techniques adapted from robust performance analysis in PLL networks have demonstrated principles that could be applied to LLM defense architectures.

- **Hardware and Resource Optimizations:** Emerging CPU inference techniques (pruning, quantization, and sparsity via frameworks like SparseML) alongside hardware accelerators (e.g., FPGA-based implementations) underline the potential for co-design strategies that balance latency reduction and computational cost. Such strategies are key when dynamic adversarial detection (using token-level gradient signals) is needed in real-time defenses.

## Defensive Approaches and Mitigation Strategies

Given the alarming success rates of jailbreak prompts, a multi-layered defense strategy is imperative. Several approaches stand out:

- **Guardrail Mechanisms:** Solutions like MoJE (Mixture of Jailbreak Experts) employ simple linguistic statistical methods that achieve a 90% detection rate with minimal computational overhead. When integrated with goal prioritization during training and inference, guardrails have reduced attack success rates markedly (e.g., from 66.4% to 2.0% for ChatGPT and from 71.0% to 6.6% for LLama2-13B).

- **Robust Alignment Frameworks:** RA-LLM represents a notable advance, integrating an alignment checking function atop an already aligned LLM. This can drop adversarial prompt success rates from nearly 100% to around 10% without incurring the costliness of extensive retraining.

- **Hybrid Prediction Models:** Integration of static software metrics with advanced NLP techniques (using ensemble methods such as random forest and BiLSTM) has enhanced vulnerability detection. Combining text mining with architectural metrics yields predictive models that can preemptively assess jailbreak risks.

- **Formal Methods and Verification:** The application of formal verification tools (e.g., ESBMC-AI) and methods such as Linear Temporal Logic and guarded command semantics is showing promise in rigorously verifying the robustness of LLM guardrails. These techniques provide guarantees on correctness even under complex adversarial conditions.

## Hybrid and Advanced Detection Mechanisms

Drawing on both traditional and novel approaches, several integrated methodologies show practical promise:

- **Fuzzing Frameworks and Genetic Algorithms:** GA-based black-box fuzzing frameworks like KameleonFuzz and FuzzLLM have demonstrated enhanced efficiency in uncovering vulnerabilities compared to undirected fuzzers. Evolutionary strategies, aided by dynamically adaptive fitness heuristics, have allowed for the intelligent generation of adversarial prompts that exploit deep execution paths.

- **Hybrid GA and Fuzzy Logic Methods:** Integrating fuzzy logic with hybrid GA approaches (as seen in the Genetic Fuzzimetric Technique) has shown that local minima traps can be avoided while significantly accelerating convergence. This dual approach improves both the quality and scalability of generated jailbreak prompts.

- **Interpretability and Explainability:** The incorporation of SHAP and LIME not only increases transparency in vulnerability detection models but also aids in refining guardrails by pinpointing the key features that adversaries exploit. This tracking of feature importance creates a feedback loop in continuously improving defensive mechanisms.

- **Integrated Multi-Agent and Game Theoretic Approaches:** Adversarial defense strategies are increasingly borrowing from the literature on security games and multi-agent coordination. By incorporating frameworks like Decentralized Markov Decision Processes (Dec-MDPs) with column generation, defenders can formulate mixed strategies that address uncertainty and coordination among heterogeneous adversary models.

## Additional Considerations and Future Directions

The defense against automated jailbreaking is a moving target. Looking to the future, research directions include:

- **Scalability in High-Throughput Environments:** Novel distributed optimization approaches and lightweight inference frameworks (like InfAdapter) may be integrated with guardrail systems to manage latency trade-offs without sacrificing detection accuracy.

- **Unified Risks and Performance Metrics:** Adapting quantitative security models used in mobile and software vulnerability contexts (for instance, mGQM and SLAM) to LLM platforms will offer better benchmarks that combine computational overhead, false positive rates, and contextual harm. This could guide the development of standardized metrics for LLM security assessments.

- **Real-Time Dynamic Adaptation:** Low-latency scheduling (using methods like ODIN and kernel bypass techniques) and improved hardware/software co-design must be leveraged to diminish the computational penalties incurred by real-time adversarial detection. This is essential as adversarial pressures continue to evolve.

- **Transferability and Cross-Domain Techniques:** The intersection between adversarial techniques in natural language and code-related attack vectors suggests that bridging methodologies across domains could yield more robust detection systems. Techniques honed in malware detection and static code analysis might be adapted for LLM defense, thereby broadening the scope of vulnerability coverage.

## Conclusion

The automatic generation of jailbreak prompts for LLMs remains a pressing challenge at the crossroads of natural language processing, security engineering, and systems design. Empirical evidence points to exceptionally high attack success rates using adversarial prompt strategies, while the persistence and evolution of these techniques necessitate a comprehensive, multi-dimensional defense strategy.

Key takeaways include:

- The critical need for multi-faceted evaluation frameworks that interweave text semantic analysis, traditional software metrics, and dynamic operational data.
- Architectural innovations and selective hardware/software co-design can play pivotal roles in mitigating latency and computational overhead in real-time detection systems.
- Hybrid defense strategies that leverage guardrails (MoJE), robust alignment (RA-LLM), formal verification, and game theory provide promising avenues to significantly reduce attack success rates.

Moving forward, it is essential that the research community continues to develop integrated, scalable, and adaptive defensive solutions. The evolution of adversaries through techniques such as prompt rewriting, gene-based fuzzing, and reverse engineering of semantic firewalls demands an equally agile and innovative response. A proactive, multifaceted defense model that combines insights from empirical analyses, advanced machine learning, and robust system architecture is our best path forward in ensuring secure and resilient deployment of LLM technologies.

---

*End of Report*

## Sources

- https://spectrum.library.concordia.ca/id/eprint/989972/
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-20119
- http://teamcore.usc.edu/papers/2014/ecai_main_decmdp_security_final.pdf
- http://teamcore.usc.edu/papers/2014/AAAISS14.pdf
- https://authors.library.caltech.edu/28108/1/CDS95-031.pdf
- https://research.vu.nl/en/publications/90f489a9-0924-4b3c-8233-7f83b0c8cafc
- http://aisel.aisnet.org/cgi/viewcontent.cgi?article%3D1656%26context%3Damcis2006
- https://ieeexplore.ieee.org/document/8066343
- http://sefcom.asu.edu/publications/riskmon-continuous-automated-codaspy2014.pdf
- https://repo.uum.edu.my/id/eprint/14176/
- http://hdl.handle.net/1814/75180
- http://infoscience.epfl.ch/record/278200
- http://ieeexplore.ieee.org/abstract/document/6335135/
- http://resolver.tudelft.nl/uuid:8660f6f6-248a-4c50-8127-e8f8b3aab582
- https://hal.inria.fr/hal-00976132
- https://hdl.handle.net/2123/23030
- https://figshare.com/articles/_Power_comparing_results_of_PLS_based_MLAS_PLS_MLAS_PCA_based_MLAS_PCA_MLAS_tagSNPs_based_MLAS_tagSNPs_MLAS_TSM_based_MLAS_using_F_test_FTSM_and_TSM_based_MLAS_using_Wald_test_WTSM_under_the_epistatic_model_/470952
- https://doaj.org/article/f06613cbe2084fe99475f455057da494
- https://doaj.org/article/2ed7b2c7ad0c4f03930eeda1b8b066b2
- http://hdl.handle.net/10.1371/journal.pone.0202145.g013
- http://max.berger.name/research/analysis_time_egee.pdf
- https://hdl.handle.net/10356/169803
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.4528
- https://scholarworks.sjsu.edu/etd_projects/545
- https://www.tdcommons.org/dpubs_series/6372
- http://repository.tue.nl/882646
- http://arxiv.org/abs/2205.10439
- http://hdl.handle.net/10316/101274
- https://hal-paris1.archives-ouvertes.fr/hal-03877517
- http://www.aaai.org/ocs/index.php/AAAI/AAAI11/paper/view/3574
- http://infoscience.epfl.ch/record/278914
- https://lirias.kuleuven.be/handle/123456789/430072
- http://www.mt-archive.info/HLT-EMNLP-2005-Moore.pdf
- http://hdl.handle.net/11577/2452575
- http://www.ai-lab.it/armando/pub/AIcomm2011-Carbone.pdf
- https://resolver.caltech.edu/CaltechAUTHORS:20190617-112254520
- http://collaboration.csc.ncsu.edu/laurie/Papers/p31-gegick.pdf
- https://hdl.handle.net/10657/18302
- http://resolver.tudelft.nl/uuid:f7f92564-a39f-478f-b9c2-503edb960cf6
- https://digitalcommons.lsu.edu/eecs_pubs/228
- https://ojs.aaai.org/index.php/AAAI/article/view/25119
- http://urn.fi/URN:NBN:fi:oulu-201601151058
- https://hdl.handle.net/2027.42/152459
- http://arxiv.org/abs/2308.03825
- http://hdl.handle.net/10217/67391
- https://doaj.org/article/a276d7694b804ad791d6b205ef02c13e
- https://doaj.org/article/e9eda0297500406da2503d1e1e757e64
- http://hdl.handle.net/20.500.12380/307923
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll3/id/572433
- https://rgu-repository.worktribe.com/file/2754840/1/ABEYRATNE%202025%20AlignLLM%20%28AAM%29
- http://ceur-ws.org/Vol-832/paper_12.pdf
- https://escholarship.org/uc/item/62428630
- https://ro.uow.edu.au/eispapers1/366
- https://www.repository.cam.ac.uk/handle/1810/300267
- https://escholarship.org/uc/item/3zk5x39s
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050913008685/MAIN/application/pdf/32d91533bb8a6d6d73357cea8cd43a89/main.pdf
- http://scholarbank.nus.edu.sg/handle/10635/72357
- http://www.ijcst.org/Volume5/Issue7/p2_5_7.pdf
- http://hdl.handle.net/10.1371/journal.pone.0202145.g005
- http://www.engr.colostate.edu/~hj/conferences/276.pdf
- https://elib.dlr.de/139117/
- http://publications.lib.chalmers.se/publication/248735-the-effect-of-dimensionality-reduction-on-software-vulnerability-prediction-models
- http://arxiv.org/abs/2205.01543
- http://hdl.handle.net/2027.42/152459
- https://hal.inria.fr/hal-00853728
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/112907
- http://hdl.handle.net/11574/192549
- http://hdl.handle.net/10.1184/r1/6604502.v1
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-206357
- http://dx.doi.org/10.3390/s25061666
- https://digitalcommons.montclair.edu/compusci-facpubs/592
- https://jurnal.idu.ac.id/index.php/DefenseJournal/article/view/19661
- http://www.mt-archive.info/MTS-2011-Duh.pdf
- http://hdl.handle.net/10945/68149
- https://ojs.aaai.org/index.php/AIES/article/view/31638
- https://hal.inria.fr/hal-01370368
- http://arxiv.org/abs/2309.01446
- http://web.cs.hacettepe.edu.tr/%7Essen/files/papers/EvoStar15.pdf
- http://hdl.handle.net/11365/1082824
- http://hdl.handle.net/10.1371/journal.pone.0271388.s003
- https://salford-repository.worktribe.com/file/1434086/1/11648104.pdf
- http://www.avantssar.eu/pdf/publications/aicom-carbone.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-978
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1072.1036
- https://doaj.org/article/4b5349da5178433c84d6cb0ba7e55d80
- https://hdl.handle.net/10356/148598
- http://arxiv.org/abs/2308.11521
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll3/id/547610
- https://research.utwente.nl/en/publications/256c0075-d13b-4c49-83f4-aaedfdb632fa
- http://hdl.handle.net/2144/21785
- https://doaj.org/article/2eb816136bff4a1ea4e1078a099c6014
- http://hdl.handle.net/10453/160769
- https://www.tdcommons.org/dpubs_series/2123
- http://cs.umd.edu/%7Ekartik/papers/1_vuln.pdf
- https://escholarship.org/uc/item/4nz902vt
- http://arxiv.org/abs/2205.14246
- https://openprairie.sdstate.edu/datascience_symposium/2022/posters/19
- http://dx.doi.org/10.26153/tsw/43861
- http://teamcore.usc.edu/papers/2014/Brown_GameSec2014.pdf
- http://arxiv.org/abs/2311.08268
- http://perso.telecom-paristech.fr/%7Erauzy/internship_formal-dpl.pdf
- https://zenodo.org/record/8296440
- https://www.open-access.bcu.ac.uk/16136/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.9423
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA457096%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.1452
- http://hdl.handle.net/11386/4776145
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.7754
- http://faculty.nps.edu/gbrown/docs/ics-2011-p0028-0049.pdf
- https://research.vu.nl/en/publications/2795d792-fe68-4bf4-a6c3-ae9cc73c5b50
- http://urn.kb.se/resolve?urn=urn:nbn:se:miun:diva-28099
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Doyle=3AJoseph=3A=3A.html
- https://doi.org/10.1098/rsta.2013.0277
- http://hdl.handle.net/11576/2629281
- https://cris.vtt.fi/en/publications/da7982a3-5184-499c-a8a5-33317f449462
- https://zenodo.org/record/7540216
- https://hdl.handle.net/10356/166097
- http://www.doria.fi/bitstream/handle/10024/85109/degerlund_fredrik.pdf%3Bjsessionid%3DA2196BA8743ED621F5148BE69D681679?sequence%3D4
- https://doaj.org/article/4d9edd94fe754044861af638bcac455e
- http://purl.utwente.nl/publications/100292
- http://digital.lib.uidaho.edu/cdm/ref/collection/etd/id/455
- https://ojs.aaai.org/index.php/AAAI/article/view/11767
- http://hdl.handle.net/2078.1/227296
- https://eprints.lancs.ac.uk/id/eprint/137428/
- http://arxiv.org/abs/2311.09096
- https://escholarship.org/uc/item/2g9542cn
- https://doaj.org/article/c6fa0d0da4994c66b4b82777959fe724
- https://drops.dagstuhl.de/opus/volltexte/2019/10541/
- https://doi.org/10.1109/ccnc49032.2021.9369620
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-177590
- http://www-i6.informatik.rwth-aachen.de/publications/download/812/LehnenPatrickHahnStefanGutaVlad-AndreiNeyHermann--HiddenConditionalRomFieldswithM-to-NAlignmentsforGrapheme-to-PhonemeConversion--2012.pdf
- https://hal.science/hal-00727280/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.7462
- https://hal.inria.fr/hal-00978844
- https://doaj.org/article/287d079cd5e545b9b31a5fa977933b49
- http://resolver.tudelft.nl/uuid:c5909991-f5c2-440f-b3f3-d62ac1ed678e
- http://hdl.handle.net/11562/435190
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Evaluating-Algorithmic-Risk-Assessment/99587022902346
- https://www.um.edu.mt/library/oar/handle/123456789/86001
- https://hal.archives-ouvertes.fr/hal-01162078
- https://orbilu.uni.lu/bitstream/10993/28628/1/EmpiricalAnalysisAPSEC16.pdf
- http://teamcore.usc.edu/manish/files/optmas10.pdf
- http://hdl.handle.net/10138/349975
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll3/id/302749
- https://digitalcommons.dartmouth.edu/cgi/viewcontent.cgi?article=1337&amp;context=cs_tr
- http://resolver.tudelft.nl/uuid:efc816c3-3a32-4325-a19a-aea15b3757e6
- https://hal.inria.fr/tel-02429815/document
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA576172%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/7989
- https://zenodo.org/record/8026525
- https://dx.doi.org/10.3390/s17030642
- http://www.ijcsns.com//April.2015-Volume.3-No.4//Article02.pdf
- https://stars.library.ucf.edu/scopus2015/1978
- https://www.repository.cam.ac.uk/handle/1810/279693
- https://aaltodoc.aalto.fi/handle/123456789/37192
- http://hdl.handle.net/2429/11014
- https://digitalcommons.kean.edu/keanpublications/683
- https://doaj.org/article/19f3f180736f4c98b6225e10c6b08ad1
- http://arxiv.org/abs/2309.05274
- https://doi.org/10.1007/978-3-642-28798-5_63
- http://arxiv.org/abs/2309.14348
- https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1021&amp;context=computer_sci_pub
- https://escholarship.org/uc/item/96x8f4m0
- http://arxiv.org/abs/2310.12321
- http://resolver.tudelft.nl/uuid:9fa2aecf-b62c-45f3-94ca-c9b300c11b50
- https://figshare.com/articles/GLM_analysis_of_change_in_PLT_counts_shows_best_model_is_useful_p_0033_R2_16_7_/6399434
- https://zenodo.org/record/7575800
- http://hdl.handle.net/10197/10606
- https://tigerprints.clemson.edu/cgi/viewcontent.cgi?article=4159&amp;context=all_dissertations
- http://www.mysmu.edu.sg/faculty/pradeepv/Papers/MAGS.pdf
- https://doaj.org/article/4c4cbf64f6e44a87badb5e389a085e45
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/67479
- http://hdl.handle.net/10.25384/sage.24546593.v1
- https://juser.fz-juelich.de/record/902918
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.6299
- http://hdl.handle.net/2286/R.I.53004
- https://stars.library.ucf.edu/scopus2000/6139
- http://teamcore.usc.edu/people/thanhhng/Papers/STEAM-H.pdf
- https://zenodo.org/record/4072812
- https://digitalcommons.sacredheart.edu/computersci_fac/181
- http://arxiv.org/abs/2204.03214
- https://doaj.org/article/221e69dfcdb24298a6a0578dcde69209
- http://www.nt.ntnu.no/users/skoge/prost/proceedings/ifac2005/Fullpapers/05177.pdf
- https://escholarship.org/uc/item/5w72v5s4
- http://urn.kb.se/resolve?urn=urn:nbn:se:hj:diva-54652
- http://ece.k-state.edu/sunflower_wiki/images/b/b3/Nakfi.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-55985
- http://research.ijcaonline.org/volume93/number18/pxc3896213.pdf
- http://arxiv.org/abs/2310.12505
- https://hal.telecom-paris.fr/hal-03788731/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.8704
- https://research.chalmers.se/en/publication/537626
- http://papers.nips.cc/paper/9571-powersgd-practical-low-rank-gradient-compression-for-distributed-optimization
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.2681
- http://arxiv.org/abs/2206.08255
- https://zenodo.org/record/6564230
- http://hdl.handle.net/10.1184/r1/22091651.v1
- http://www.loc.gov/mods/v3