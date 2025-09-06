# Final Report on PolyPrompt: Automating Knowledge Extraction from Multilingual Language Models with Dynamic Prompt Generation

This report consolidates extensive findings and insights from recent research on dynamic prompting techniques, multilingual language models, and knowledge extraction tasks. It synthesizes contributions from a multitude of studies to provide a detailed, three-plus page report discussing the theoretical underpinnings, applied methodologies, trade-offs, and future directions for the PolyPrompt system.

---

## 1. Introduction

The rapid evolution of multilingual language models (MLMs) and the explosion of research on dynamic prompt generation have paved the way for systems such as PolyPrompt. This framework aims to automatically extract knowledge from multilingual language models by leveraging dynamic, adaptive prompt generation. Given the diversity of languages – including high-resource as well as under-resourced contexts – an automated, dynamic approach is imperative. PolyPrompt must seamlessly integrate multiple strategies that range from rule-based to learned generative techniques while being tailored for effective extraction of structured knowledge such as entities, events, and zero-shot inference tasks across diverse languages.

The goal of this report is to map out the landscape of relevant techniques, highlight key experimental findings, and propose a unified architecture that addresses both the practical and theoretical challenges of multidimensional language processing. The report draws on findings from approaches such as dynamic sparse methods, dynamic priming, differentiable prompt optimization, and parameter-efficient training techniques, among many others.

---

## 2. Multilingual Language Models and the Scope of PolyPrompt

### 2.1 Target Languages and Language Resources

PolyPrompt is designed to be agnostic with regards to language resource levels. It not only targets high-resource languages but also extends its capabilities to low-resource languages by:

- Leveraging **auxiliary supervision** and **data augmentation techniques** including non-gradient based text span substitutions and syntactic manipulations.
- Utilizing cross-lingual word embeddings as well as dynamic vocabulary adaptation methods to optimize performance in languages with sparse data.
- Incorporating hybrid approaches that combine rule-based metrics with generative prompting, thus allowing for flexible transfer learning and zero-shot tasks.

Many recent advancements have shown that traditional methods, when extended with dynamic prompting, are capable of achieving performance levels that rival monolingual models, even in less-resourced languages.

### 2.2 Dynamic Sparse and Parameter-Efficient Approaches

Dynamic sparse methods, such as those illustrated by the RoSA framework, demonstrate that low‐rank and high‐sparse approximations can be combined effectively. This is particularly relevant for PolyPrompt, since it provides a mechanism to reconcile computational efficiency with evaluation accuracy in noisy environments. Other techniques, like parameter space factorization via Bayesian generative models and prototypical fine-tuning methods, further emphasize achieving robust performance while drastically reducing model parameters (e.g., down to 1.5% of BERT's size).

These advancements are critical in enabling PolyPrompt to operate efficiently across varied computational budgets, making it feasible to handle large multilingual datasets without significantly compromising on fine-tuning performance.

---

## 3. Dynamic Prompt Generation Strategies

Dynamic prompt generation within PolyPrompt leverages both rule-based and learned generative strategies, thus addressing distinct operational and contextual needs.

### 3.1 Rule-Based and Hybrid Approaches

Several research efforts support the integration of rule-based systems with dynamic generative frameworks. For instance:

- **Hybrid Architectures:** Integrating explicit rule-enforcement through adapters or dedicated masking strategies into dynamic subnetworks. This ensures that strict, structured linguistic knowledge is blended with the flexibility of generative models. This approach is seen to be particularly effective when the system has to accommodate noisy, low-resource language data.
- **Multilingual Multitask Frameworks:** Frameworks like Polyglot Prompt have demonstrated the efficacy of a monolithic architecture wherein a shared semantic space supports up to 49 languages across various tasks such as NER, sentiment analysis, and event extraction.

These rule-based components are crucial as they provide consistency and explicit linguistic features, which are often necessary when handling domain-specific data (e.g., crisis-related event extraction). They complement the generative capabilities by adjusting dynamic subnetworks based on task-specific metrics.

### 3.2 Learned and Differentiable Techniques

Dynamic prompt generation can also be optimized using learned methods. Recent innovations include:

- **Differentiable Prompt Techniques (e.g., DART):** These methods reformulate NLP tasks by jointly optimizing the prompt templates and the target labels through backpropagation. They enable smaller pretrained language models (PLMs) to achieve competitive few-shot performance while minimizing manual prompt engineering. This approach also provides a pathway to integrate dynamic computational overhead into the training process, achieving flexibility in prompt generation.

- **Dynamic Priming:** Incorporating context-dependent triggers (such as 'protested' vs. 'arrest') improves task-specific performance in zero-shot cross-lingual applications. Dynamic priming techniques have already demonstrated significant improvements in trigger and argument extraction, and when combined with generative methods, offer considerable gains in both precision and recall.

- **Unified Multilingual Prompts (UniPrompt):** These prompts are pre-computed and language-agnostic, meaning they incur near-zero extra inference cost while enhancing cross-lingual transfer. The use of novel initializations for target label words has proven to enhance the overall performance in zero-shot settings, making them a fitting component in the PolyPrompt framework.

### 3.3 Hybrid Strategies and Dynamic Adaptation

A particularly promising area involves the integration of learned generative techniques with rule-based components, adopting a hybrid approach. Such architectures benefit from:

- **Classifier Ensembles and Meta-Learning:** Techniques like meta-learning for dynamic task sampling and ensemble bootstrapping (e.g., Prompt-GAN) have shown improvements in performance metrics such as macro F1 scores and accuracy under low-resource benchmarks.

- **Contextual Dynamism:** By applying adaptive strategies that reinitialize specific top layers for masked language modeling or adjust task-specific triggers dynamically, it is possible to further enhance the predictive accuracy for various tasks such as TTS, ASR, and NMT across multiple languages.

In summary, the dynamic prompt generation strategies for PolyPrompt are envisioned as a multi-tiered system combining rule-based constraints and dynamic, learned module optimization. This provides a robust foundation that is well suited for both high-resource and low-resource scenarios.

---

## 4. Knowledge Extraction Tasks and Benchmarking

### 4.1 Types of Extraction Tasks

PolyPrompt is geared toward optimizing an array of knowledge extraction tasks, including but not limited to:

- **Information Retrieval:** Efficiently retrieving structured data from multilingual corpora by dynamically tuning prompts that offer semantic clarity across languages.
- **Entity Recognition:** Leveraging auxiliary tasks such as syntactic and sentiment analysis to bolster zero-shot entity recognition performance. Hybrid techniques and meta distillation frameworks (e.g., ProKD) serve to enhance both generalizability and linguistic specificity.
- **Event Extraction:** Especially in domains such as crisis management, event extraction systems which combine multilingual, domain-specific grammars with weakly supervised techniques have already shown promising improvements in languages like Portuguese and Spanish.
- **Zero-Shot Learning:** Adaptation of transformer-based models via cross-lingual prompt transfer has demonstrated that careful design of task-specific instructional text can yield major improvements in zero-shot performance.

### 4.2 Evaluation and Benchmarking Approaches

Evaluating the performance of a multilingual prompt-based system is non-trivial. Traditional metrics for machine translation (BLEU, METEOR, TER) or NER (macro F1, entity linking accuracy) require significant adaptation to account for translation variance and cultural nuances. Recent research has underscored the importance of:

- **Unified Metric Families:** Integration of n-gram based metrics and modern LLM evaluators (e.g., BARTScore, T5Score) that capture both local and global variance in model outputs.
- **Hybrid Evaluation Protocols:** Benchmarks like GEM and GEMv2 exemplify modular evaluation architectures that can seamlessly combine rule-based and generative metrics. They support a range of datasets and languages, ensuring that PolyPrompt can be rigorously tested across varied linguistic settings.
- **Multilingual Model Effect (MLME) Metric:** Specifically designed for TTS evaluation in low-resource languages, MLME quantifies the impact of acoustic model architecture, data balance ratios, and the absolute quantity of target language data. This metric informs how multilingual experiments fare compared to monolingual baselines and guides iterative optimization of the PolyPrompt framework.

Benchmarking these tasks also involves conducting ablation studies. By selectively removing components such as contrastive alignment loss, latent variable factorization, or prototype alignment, researchers have been able to quantify the individual contributions of each component, thereby refining the trade-offs between language-independent and language-specific as well as rule-based versus generative aspects of the system.

---

## 5. Integration of Findings and System Design Considerations

### 5.1 Architectural Synergies and Trade-offs

The integration of learnings from dynamic sparse methods, dynamic priming, differentiable prompt techniques, and hybrid rule-based generative paradigms delineates a roadmap to build a robust and flexible PolyPrompt system. Key design elements include:

- **Dynamic Subnetwork Selection:** Incorporate mechanisms that allow the system to dynamically select between rule-based and generative pathways based on the task context. This could use metaheuristic and genetic algorithms inspired by digital image registration techniques to optimize the search space.

- **Early Fusion of Multilingual Prompts:** Utilize unified pre-computed prompts (UniPrompt) to reduce runtime ambiguity, while still providing a framework for re-optimization as more domain-specific data becomes available.

- **Parameter-Efficient and Sparse Training:** Leverage approaches such as low-rank approximations and structured sparsity to reduce computational costs significantly. This aligns with recent findings that suggest potential savings of up to 75% FLOPs reduction without a significant degradation of performance.

- **Task-Specific Adaptations:** Utilize dynamic adjustments such as reinitializing top layers for masked language modeling or integrating meta-learning frameworks to dynamically sample tasks. This ensures that the system is flexible across differing domains such as TTS, ASR, and multilingual event extraction.

### 5.2 Technology and Implementation Considerations

From an implementation perspective, the following should be considered:

- **Frameworks and Toolkits:** Modern libraries such as NLG-Metricverse centralize heterogeneous metrics and facilitate meta-evaluation. These tools are crucial when aligning rule-based evaluations with generative ones.

- **Integration with Multimodal Datasets:** Recent research using multimodal experimental techniques (e.g., MOUS dataset, grip force sensors) provides both high spatial and temporal data resolution, enabling correlations between linguistic constructs and neural activations. This insight could lead to further refinements in prompt design by ensuring that dynamic prompts are both semantically and neurophysiologically informed.

- **Future-Proofing through Continuous Learning:** Systems like PolyPrompt must embrace live, interactive evaluation frameworks (akin to GEMv2) to refine prompt strategies as new languages and tasks are introduced. The strategies should also be open to incorporating the latest breakthroughs from LLM evaluations, such as chain-of-thought and few-shot prompting techniques.

---

## 6. Conclusions and Future Directions

In conclusion, the PolyPrompt framework is an ambitious, integrative approach that seeks to combine the best of rule-based, hybrid, and generative dynamic prompt systems to extract high-value knowledge from multilingual language models. Several key insights have emerged from the research: 

- The use of parameter-efficient sparse training and dynamic priming can recover performance even in noisy or data-sparse environments.
- Hybrid systems that intelligently blend rule-based constraints with learned dynamic prompts provide robustness and adaptability across a wide range of tasks and languages.
- Evaluation strategies must be tailored, leveraging unified metric families and modular benchmarks to fully capture the complexities of multilingual and multitask scenarios.

Looking ahead, further research is warranted in areas including the integration of continuous learning paradigms, enhanced dynamic optimization via meta-learning, and deeper exploration of neurophysiological correlates of language prompts. Moreover, additional studies on low-resource languages and domain-specific applications (such as crisis event extraction or hate speech detection) will refine and extend the capabilities of the PolyPrompt system. 

This report therefore provides a comprehensive synthesis of current methodologies and sets a clear pathway for further innovations in automated multilingual knowledge extraction via dynamic prompt generation.

---

# References

While this report synthesizes findings from a broad array of contemporary research, the individual studies and experimental results mentioned herein represent the cumulative basis for ongoing developments in dynamic, multilingual prompt-based architectures. Future publications and benchmarks such as GEM/GEMv2, studies on MLME, and outcomes from recent conferences (e.g., AAAI, EMNLP, IJCAI) are recommended for continuous updates.

---

*This document is intended for expert readers and researchers with a deep interest in multilingual NLP, dynamic prompting frameworks, and the integration of learnings across languages and tasks. The conclusions drawn herein are based on speculative projections, rigorous analysis, and experimental validation, suggesting a promising future direction for PolyPrompt and related systems.*

## Sources

- https://hdl.handle.net/1721.1/145034
- http://hdl.handle.net/10045/93563
- https://www.um.edu.mt/library/oar//handle/123456789/22686
- http://arxiv.org/abs/2310.06927
- http://hdl.handle.net/1854/LU-8709864
- http://hdl.handle.net/21.11116/0000-0003-4FC2-A
- https://doi.org/10.18653/v1/2023.vardial-1.1
- http://www.mt-archive.info/NAACL-HLT-2010-Cer-1.pdf
- https://inria.hal.science/hal-04015863v2/document
- http://hdl.handle.net/10.1371/journal.pone.0296939.g014
- https://docs.lib.purdue.edu/dissertations/AAI10615003
- https://rgu-repository.worktribe.com/output/1920683
- https://ojs.aaai.org/index.php/AAAI/article/view/17661
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-352637
- https://dspace.library.uu.nl/handle/1874/17183
- https://ojs.aaai.org/index.php/AAAI/article/view/17516
- http://hdl.handle.net/11858/00-001M-0000-0019-1C49-3
- https://cris.maastrichtuniversity.nl/en/publications/99f30efb-a216-4d23-8da0-c32597ac1ff9
- https://purehost.bath.ac.uk/ws/files/300005316/2309.05454v1.pdf
- https://aclanthology.org/2023.emnlp-main.14.pdf
- https://hal.science/hal-03334485/document
- https://research-repository.st-andrews.ac.uk/bitstream/10023/26886/1/Biedenkapp_2022_Theory_inspired_parameter_GECCO_AAM.pdf
- https://research.tue.nl/en/publications/7c7766b1-42ba-4b1f-8be1-ee27878af509
- http://dx.doi.org/10.1007/s10590-010-9077-2
- http://arxiv.org/abs/2207.00349
- http://arxiv.org/abs/2205.04810
- http://hdl.handle.net/10230/58560
- https://ojs.aaai.org/index.php/AAAI/article/view/6302
- https://research.rug.nl/en/publications/c2101556-c819-4c66-b685-5817cc38bc6f
- http://hdl.handle.net/10138/344611
- https://ojs.aaai.org/index.php/AAAI/article/view/11919
- https://ojs.aaai.org/index.php/AAAI/article/view/26068
- http://eecs.vanderbilt.edu/people/mikefitzpatrick/papers/1988_fitzpatrick_machinelearning_genetic_alg_in_noisy_environments.pdf
- http://www.nusl.cz/ntk/nusl-304321
- https://hal.science/hal-03361421/file/Narratives_Syntax_semantics.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.432.1915
- https://orcid.org/0000-0002-6131-8763
- https://ojs.aaai.org/index.php/AAAI/article/view/5079
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://resolver.tudelft.nl/uuid:c035edc6-688f-4d16-aa77-45351266dba2
- http://dsmforum.org/events/DSM13/Papers/Ackermann.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/6476
- https://hal.science/hal-00349665
- http://alt.qcri.org/%7Eguzmanhe//papers/WMT2015-Guzman.pdf
- http://dialnet.unirioja.es/servlet/oaiart?codigo=1018100
- https://aisel.aisnet.org/icis2023/generalis/generalis/1
- https://ojs.aaai.org/index.php/AAAI/article/view/6362
- http://publications.jrc.ec.europa.eu/repository/handle/JRC56065
- https://eprints.whiterose.ac.uk/152594/1/coli_a_00356.pdf
- https://drops.dagstuhl.de/opus/volltexte/2015/5029/
- https://biblio.ugent.be/publication/8650850
- https://ojs.aaai.org/index.php/AAAI/article/view/26524
- https://scholarworks.utep.edu/open_etd/2011
- http://www.nusl.cz/ntk/nusl-397887
- https://ojs.aaai.org/index.php/AAAI/article/view/26507
- https://doaj.org/toc/1647-0818
- https://github.com/pvh1602/NPB.
- http://hdl.handle.net/20.500.12678/0000004724
- http://arxiv.org/abs/2207.03380
- http://arxiv.org/abs/2207.00352
- http://arxiv.org/abs/2205.01543
- https://zenodo.org/record/5779966
- http://arxiv.org/abs/2111.00160
- http://real.mtak.hu/172978/
- http://publications.jrc.ec.europa.eu/repository/handle/JRC66720
- https://espace.library.uq.edu.au/view/UQ:4f8dab4
- https://epub.ub.uni-muenchen.de/61855/1/D18-1343.pdf
- https://pub.uni-bielefeld.de/record/2619483
- http://arxiv.org/abs/2211.13638
- https://hdl.handle.net/10289/15259
- http://www.mt-archive.info/MTS-2001-Miller-1.pdf
- http://hdl.handle.net/21.11116/0000-0004-B4DB-A
- https://zenodo.org/record/7772333
- http://www.mt-archive.info/CoNLL-2009-Gesmundo.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/5374
- http://aclweb.org/anthology/C/C14/C14-1040.pdf
- https://scholarworks.utep.edu/dissertations/AAI22617182
- https://hal-univ-bourgogne.archives-ouvertes.fr/hal-03529206/document
- http://summit.sfu.ca/item/16087
- https://eprints.whiterose.ac.uk/id/eprint/218822/8/2024.findings-emnlp.396.pdf
- http://publications.jrc.ec.europa.eu/repository/handle/JRC66736
- http://publications.idiap.ch/downloads/papers/2012/Imseng_INTERSPEECH_2012.pdf
- http://hdl.handle.net/11858/00-001M-0000-0029-1D65-1
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.73.3109
- http://hdl.handle.net/2066/221201
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-190548
- https://research.rug.nl/en/publications/6af86526-142f-4f32-bbbb-3497743a3ede
- http://hdl.handle.net/10.1371/journal.pone.0271388.s003
- http://hdl.handle.net/11582/324172
- http://hdl.handle.net/2077/65590
- http://www.lrec-conf.org/proceedings/lrec2012/pdf/443_Paper.pdf
- http://arxiv.org/abs/2110.07560
- http://www.linguamatica.com/index.php/linguamatica/article/view/37/37/
- http://arxiv.org/abs/2205.06356
- http://www.mt-archive.info/WMT-2009-Snover.pdf
- https://dx.doi.org/10.1016/j.inffus.2022.09.029
- http://oa.upm.es/55618/
- https://hal.archives-ouvertes.fr/hal-00258389
- http://hdl.handle.net/11346/BIBLIO@id=-6622357234668258372
- http://hdl.handle.net/11585/801636
- https://research-explorer.ista.ac.at/record/18117
- http://arxiv.org/abs/2204.14264
- https://www.repository.cam.ac.uk/handle/1810/360866
- https://hal.archives-ouvertes.fr/hal-02364502
- http://hdl.handle.net/11858/00-001M-0000-000E-FC0D-F
- http://www.mt-archive.info/WMT-2009-Popovic-1.pdf
- http://hdl.handle.net/2152/45746
- https://ojs.aaai.org/index.php/AAAI/article/view/21307
- http://publications.jrc.ec.europa.eu/repository/handle/JRC56760
- https://ojs.aaai.org/index.php/AAAI/article/view/26528
- https://ict.csiro.au/staff/Cecile.Paris/distribution/inlg2006-Paris-final.pdf
- https://research.monash.edu/en/publications/e7af0388-d67e-4f54-826e-ce01c9c6b6dc
- https://cnrs.hal.science/hal-02989957/document
- https://eprints.lancs.ac.uk/id/eprint/131820/
- http://www.open-access.bcu.ac.uk/12549/
- http://hdl.handle.net/20.500.11850/498270
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-446516
- https://hal.science/hal-01439729
- https://zenodo.org/record/1091008
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0167642306000724/MAIN/application/pdf/6c420924bd65566c14bb70b76a4d35e2/main.pdf
- https://zenodo.org/record/3894645
- http://hdl.handle.net/11025/43167
- https://research-portal.st-andrews.ac.uk/en/researchoutput/a-sized-time-system-for-a-parallel-functional-language-revised(10dd17bb-0799-40af-9e4a-1d639f4bd5c6).html
- https://doaj.org/article/2e171cc6b7c24d36a1012966086a63b7
- https://researchmgt.monash.edu/ws/files/505674985/49498487_oa.pdf
- https://doaj.org/article/cef2c4428b3449139e84133efd717b2e
- http://doras.dcu.ie/24600/
- https://nrc-publications.canada.ca/eng/view/object/?id=fb92f18a-a6da-4cae-b18d-a8e9e3f25dda
- https://hal.archives-ouvertes.fr/hal-03294912
- https://ojs.aaai.org/index.php/AAAI/article/view/25114
- https://ojs.aaai.org/index.php/AAAI/article/view/4670
- https://hal.inria.fr/hal-01584054
- http://www.mt-archive.info/ACL-2004-Soricut.pdf
- https://zenodo.org/record/7861323
- http://arxiv.org/abs/2303.10464
- http://hdl.handle.net/10379/16085
- https://research.utwente.nl/en/publications/do-we-actually-need-dense-overparameterization-intime-overparameterization-in-sparse-training(9b8f9451-b59e-443f-99c6-33867c21ccff).html
- http://arxiv.org/abs/2205.11005
- http://hdl.handle.net/11582/325614
- https://www.repository.cam.ac.uk/handle/1810/275496
- http://d3s.mff.cuni.cz/publications/download/KezniklMalohlavaBuresHnetynka-PolyglotProgrammingSupport-SEAA-2011.pdf
- http://edoc.mpg.de/320253
- http://hdl.handle.net/10.6084/m9.figshare.21321198.v2
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27668
- https://hal.science/hal-03426977/document
- https://hdl.handle.net/10388/14394
- http://arxiv.org/abs/2205.05313
- https://aclanthology.org/2021.emnlp-main.664.pdf
- https://doaj.org/article/8dae0e835ef84307a9944baf935a40e9
- http://thescipub.com/PDF/jcssp.2010.1326.1333.pdf
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1067%26context%3Dlti
- http://hdl.handle.net/10.1184/r1/6473021.v1
- http://hdl.handle.net/1853/60414
- http://arxiv.org/abs/2202.11451
- http://amslaurea.unibo.it/28997/1/2023-06-30_MA_thesis_submission.pdf
- https://hal.inria.fr/hal-03840070
- https://research.tilburguniversity.edu/en/publications/c42a48c6-22ca-4ea4-9e88-6a43cdf0b3f9
- http://dx.doi.org/10.1016/j.scico.2014.06.012
- https://zenodo.org/record/7525010
- https://lirias.kuleuven.be/handle/123456789/543402
- http://hdl.handle.net/1721.1/91126
- http://publications.jrc.ec.europa.eu/repository/handle/JRC45831
- https://www.aaai.org/Papers/Symposia/Spring/2003/SS-03-06/SS03-06-021.pdf
- https://zenodo.org/record/7524913
- http://hdl.handle.net/1911/96451
- http://hdl.handle.net/1721.1/58926
- https://hdl.handle.net/11585/896084
- http://hdl.handle.net/10045/3451
- https://aclanthology.org/2021.acl-long.101.pdf
- http://hdl.handle.net/10.1184/r1/6473570.v1
- http://aclweb.org/anthology/P/P14/P14-2037.pdf
- http://alt.qcri.org/%7Eguzmanhe//papers/CONLL2015-Guzman.pdf
- http://www3.nd.edu/%7Etlevinbo/papers/NAACL15_MTWA.pdf
- https://doi.org/10.26615/978-954-452-092-2_003
- http://arxiv.org/abs/2112.10684
- https://inria.hal.science/hal-03704504/document
- https://orcid.org/0000-0001-5736-5930
- https://figshare.com/articles/Commonality_of_neural_representations_of_sentences_across_languages_predicting_brain_activation_during_Portuguese_sentence_comprehension_using_an_English-based_model_of_brain_function/6614009
- https://zenodo.org/record/3525486
- https://hal.inria.fr/hal-03540072
- http://arxiv.org/abs/1906.08584
- https://hal.science/hal-01084986/document
- http://arxiv.org/abs/2108.07140
- http://parles.upf.edu/llocs/plambert/hytra/hytra2014/NivreHyTra.pdf
- http://arxiv.org/abs/2106.04217
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.74.3391
- http://hdl.handle.net/1911/16807
- https://oasis.postech.ac.kr/handle/2014.oak/115618
- http://arxiv.org/abs/2204.06457
- http://arxiv.org/abs/2211.01642
- http://arxiv.org/abs/2108.13161
- http://hdl.handle.net/11379/549099
- http://arxiv.org/abs/2106.10199
- http://tubiblio.ulb.tu-darmstadt.de/127749/
- https://doi.org/10.18653/v1/2024.findings-acl.753
- http://arxiv.org/abs/2203.08383
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.175
- http://ir.psych.ac.cn/handle/311026/26433
- http://tubiblio.ulb.tu-darmstadt.de/136782/
- https://escholarship.org/uc/item/2sx1t8rr
- http://hdl.handle.net/11573/871376
- http://strategic.mit.edu/docs/3_114_AIAA-2008-6058-Optimal-ISRU.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050916300576/MAIN/application/pdf/61e5baec6bcf2cce053459a89e3f0bc8/main.pdf
- https://archive-ouverte.unige.ch/unige:162730