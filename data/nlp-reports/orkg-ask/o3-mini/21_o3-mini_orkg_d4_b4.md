# Final Report: Chain-of-State Iterative Code Generation via Large Language Models

## 1. Introduction

Over the last several years the integration of large language models (LLMs) into code generation architectures has evolved from a simplistic chain-of-thought style into sophisticated chain-of-state iterative approaches. Such methods incorporate iterative optimization loops, state minimization techniques, and dynamic prompt engineering that together create a robust framework when applied to the domain of code generation. This report surveys recent learnings from research, including both theoretical advances and empirical evaluations across multiple domains—from compiler theory to real-time code optimization on heterogeneous hardware. In the subsequent sections, we explore how iterative techniques, adaptive thresholding, reinforcement learning, and architectural innovations (e.g., gated state spaces and pre-gated Mixture-of-Experts) have contributed to creating efficient, robust, and semantically reliable code generation protocols.

## 2. Background and Theoretical Underpinnings

### 2.1. Chain-of-Thought vs. Chain-of-State

Early explorations into LLM-enabled code generation predominantly used chain-of-thought prompting. However, limitations became apparent when addressing dynamic error correction, semantic decoupling, and iterative optimization. In contrast, the chain-of-state paradigm focuses on maintaining and updating an explicit internal representation (or state) as the code generation process evolves. This approach allows for:

- **Robust corrective feedback**: Minimizing error propagation by dynamically incorporating previous state information.
- **Adaptive optimization**: Facilitating fine-tuning via reinforcement learning-based strategies and parameter-efficient (PETuning) techniques.
- **Interfacing with traditional compiler techniques**: Enabling state minimization, speculative execution, and iterative parameter tuning.

### 2.2. Iterative Optimization in Code Generation

In the iterative framework, code is developed and refined over multiple loops. Empirical evidence, as seen in studies involving KDataSets and various compilers like GCC and ICC, illustrates that tailored, program-specific optimization sequences can achieve speedup improvements sometimes up to 3.75x, reaching at least 83% of the ideal speedup. By integrating iterative parameter tuning with robust error metrics and state reduction strategies, a chain-of-state approach provides a strong foundation for next-generation code generators.

## 3. Architectural Innovations and Algorithmic Strategies

### 3.1. Iterative Parameter Tuning and Reinforcement Learning

Recent research demonstrates the power of combining prompt engineering with reinforcement learning (RL) enhancements. These RL-based approaches adapt prompt responses dynamically under distributional shifts, allowing for:

- **Dynamic fine-tuning and state correction**: As seen in experiments with GPT-4 based models, integrating reinforcement learning can adaptively control response reliability and mitigate code errors.
- **Parameterized optimization sequences**: Techniques like PETuning and iterative language model estimation have demonstrated that minor tuning adjustments yield improvements in both stability and algorithmic performance.

### 3.2. Adaptive Thresholding and Energy-Aware Optimizations

Adaptive thresholding strategies have garnered attention especially in settings where resource constraints and error management are critical. Studies focusing on IoT and embedded applications suggest that:

- **Class-dependent confidence measures**: Early-stopping mechanisms and energy-based scoring systems allow for dynamic adaptation to simpler inputs, reducing overhead and mitigating errors.
- **Adaptive differential and fixed-length coding schemes**: These allow controlled trade-offs between coding resolution and robustness, ensuring reliable transmissions under variable channel conditions (e.g., with modulation schemes adjusted for SNR thresholds).

### 3.3. Gated State Spaces (GSS) and Mixture-of-Experts (MoE) Architectures

Gated State Space models and pre-gated Mixture-of-Experts architectures are two techniques that have revolutionized the iterative state updating process:

- **Gated State Spaces (GSS)**: GSS models have been shown to improve autoregressive sequence prediction and enable zero-shot generalization to longer inputs. They are particularly efficient on TPUs and can be integrated with self-attention mechanisms to handle local dependencies.
- **Pre-gated Mixture-of-Experts (MoE)**: These architectures reduce computational overhead by pre-selecting experts using a lightweight gating function. They offer a scalable solution, as shown by models that match dense model performance while using substantially less compute. Importantly, these methods also decouple semantic quality from token-based complexity, which is essential in achieving robust semantic code synthesis.

### 3.4. In-Place Dynamic Code Generation and Compiler Integration

Systems like VCODE have demonstrated that an in-place dynamic code generation approach (originally developed for architectures such as MIPS, SPARC, and Alpha) can generate machine code with remarkable efficiency—incurring only 6–10 instructions overhead per generated instruction. Key techniques include:

- **Elimination of intermediate representations**: This leads to significant performance gains, as well as an ability to exploit hardware-specific features in GPU and multi-core settings (usage of warp shuffle, dynamic parallelism, atomic operations).
- **Integration with traditional compiler optimizations**: Techniques such as Boolean function optimization, state equivalence merging, and speculative code motion (driven by insights from compiler theory) allow for fine-grained control over code efficiency and error minimization.

## 4. Empirical Evaluations, Benchmarks, and Comparative Analyses

### 4.1. Benchmarking Iterative Optimization Strategies

Large-scale benchmark studies—such as the KDataSets evaluation spanning 1000 datasets and 32 programs—have provided key insights into the potential speedups that can be achieved. These studies show:

- **Substantial performance improvements**: Targeted parameter tuning can yield speedup improvements up to 3.75x compared with conventional settings (e.g., -O3 optimization in GCC).
- **Quantitative error metrics**: Empirical analyses indicate that error propagation can be mitigated by iterative approaches that adjust parameters based on real-time performance feedback.

### 4.2. Multi-Paradigm and Domain-Specific Benchmarks

Frameworks such as MultiPL-E and VerilogEval extend traditional benchmarks by incorporating multiple programming languages (up to 18) and domain-specific tasks (like hardware description language generation). These benchmarks illustrate:

- **Cross-language performance differences**: Evaluating models like Codex, InCoder, and GPT-NeoX across diverse programming paradigms provides valuable insights into how chain-of-state methods can be tailored to meet language-specific requirements.
- **Semantic validation and feedback loops**: Systems that incorporate simulation-based testing (as in VerilogEval for checking HDL code) ensure that generated code meets functional correctness standards in practical hardware design contexts.

### 4.3. Integration of ML-Driven Compiler Techniques

Modern research has begun integrating compiler optimization techniques within the LLM code generation pipeline. By employing methods such as phase ordering, ML-guided empirical model tuning, and state minimization in finite state machines (FSMs), these integrated frameworks achieve improvements such as:

- **Up to 17% improvement in execution time and code size optimization**: During the compilation process.
- **Reduced CPU time by up to 11%**: Through enhanced state encoding and hypothesis recombination in iterative workflows.

### 4.4. Energy Efficiency and Resource Management

Adaptive resource allocation, driven by a synthesis of dynamic voltage-frequency scaling (DVFS) and distributed resource allocation (DRA), has yielded energy per instruction (EPI) reductions of nearly 17.9% and overall energy efficiency improvements of approximately 55%. This level of integration is crucial in scenarios that involve cloud-native scaling, IoT tasks, and heterogeneous multi-core systems.

## 5. Advanced Topics and Emerging Trends

### 5.1. Decentralized and Adaptive Runtime Scheduling

Modern embedded systems are increasingly adopting decentralized dynamic scheduling paradigms (akin to the COAST enhancements) that integrate runtime code generation with energy-efficient task classification. This architecture supports:

- **Dynamic re-optimization**: Continually adapting scheduling policies to balance resource utilization and performance.
- **Decentralized OS-level strategies**: Allowing live code updates and minimizing downtime with in-place code generation linked to adaptive thresholding strategies.

### 5.2. Speculative Execution and Parallelization

Speculative execution methods, including conditional speculation and multi-threading strategies, have shown promise in reducing FSM state explosion and improving parallel execution efficiency. Using techniques such as thread prediction and checkpointing, these methods can deliver:

- **Up to 17.7% reduction in dynamic energy consumption**: By proactively predicting code paths and mitigating mis-speculation overhead.
- **Throughput improvements**: On average around 50% when applying speculative parallelization strategies in multi-core environments.

### 5.3. Robust Differentiation in State Chain Coding

Robust differential chain coding schemes leverage the combination of relative and absolute vectors to prevent error propagation without incurring additional bandwidth costs or forward error correction overhead. These strategies are vital in domains that range from multimedia transmission to secure communications (including post-quantum cryptography), and they suggest that integrating such robust coding into LLM-driven code generation can improve overall error resilience.

### 5.4. Interactive Error Correction and Feedback Loops

Emerging research in interactive error-correcting protocols shows that adaptive adjustments in speaker roles and dynamic error feedback can extend error tolerance significantly (with improvements noted from 1/4 to adaptive bounds such as 2/7 and even 2/3 in different contexts). Embedding such strategies in chain-of-state methods would allow code generation systems to be more robust against adversarial inputs and variant edge cases.

## 6. Future Directions and Open Research Questions

### 6.1. Novel Prompting Strategies and Architectural Hybrids

Future research may investigate combining chain-of-thought with chain-of-state paradigms—hybrid models that leverage both a narrative understanding of problem statements and a continuously updated internal state. Additionally, integrating meta-object protocols and lightweight metamodelling languages could provide configurable semantic validation mechanisms for low-resource languages.

### 6.2. Integration with Heterogeneous Hardware Platforms

As systems become increasingly heterogeneous (utilizing multi-core GPUs, FPGAs, and specialized accelerators), further work is needed to optimize in-place code generation methods to leverage domain-specific hardware features. The interplay between hardware-assisted dynamic parallelism, resource allocation, and real-time scheduling remains an open area of exploration.

### 6.3. Enhanced Empirical Benchmarks and Metrics

It is imperative that next-generation benchmarks extend beyond token-based natural language metrics. Future evaluation frameworks should incorporate semantic quality measures and runtime error correction metrics that decouple token complexity from true code understanding—drawing on insights from modular language implementations and comprehensive multi-paradigm suites.

### 6.4. Resource-Bounded and Adaptive Learning

Focusing on energy-constrained environments, research into energy-bounded learning and adaptive, class-dependent thresholding strategies is expected to grow. Such techniques, by aligning energy scores with input probability densities and incorporating random network distillation-based feedback loops, promise enhanced robustness under resource constraints and non-stationary operating conditions.

## 7. Conclusion

Chain-of-state iterative code generation represents a paradigm shift in the field of automated code synthesis using large language models. By merging insights from compiler theory, iterative optimization, dynamic state management, and reinforcement learning, this framework offers a robust alternative to traditional chain-of-thought approaches. Engineering benefits include significant performance speed-ups, energy efficiency improvements, and enhanced error resilience.

The extensive research learnings outlined in this report—ranging from gated state spaces and pre-gated MoE architectures to interactive error correction protocols and decentralized runtime scheduling—provide a roadmap for future investigations. These methodologies not only demonstrate immediate practical benefits but also pave the way for iterative system designs that can dynamically adapt to both semantic requirements and evolving hardware landscapes.

As the field continues to evolve, integrating diverse benchmarks and exploring hybrid prompt strategies will be critical. The potential to leverage heterogeneous architectures and interactive state optimization heralds a new era for code generation systems—one in which iterative chain-of-state methodologies push the boundaries of computational efficiency, correctness, and robustness in automated programming.

---

*This report integrates learnings from a wide spectrum of modern research and anticipates future trends that merge traditional compiler optimization with cutting-edge LLM technologies. Continued interdisciplinary research will be crucial in realizing the full potential of chain-of-state iterative code generation.*

## Sources

- https://hal-mines-paristech.archives-ouvertes.fr/hal-00618122
- http://groups.csail.mit.edu/tds/papers/Ghaffari/STOC14-interactive_protocol1.pdf
- http://arodes.hes-so.ch/record/5955
- https://lirias.kuleuven.be/bitstream/123456789/369163/1/paper.pdf
- https://authors.library.caltech.edu/25083/1/OSTfocs05.pdf
- https://hal.inria.fr/hal-01397196
- http://arxiv.org/abs/2308.12066
- http://arxiv.org/abs/2308.11696
- http://arxiv.org/abs/2112.11226
- http://hdl.handle.net/10023/25744
- https://doaj.org/toc/1932-6203
- https://research.aalto.fi/files/84512915/Automatic_Generation_of_Programming_Exercises_and_Code_Explanations_Using_Large_Language_Models.pdf
- https://rgu-repository.worktribe.com/output/1920683
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.8756
- https://hdl.handle.net/11311/1254605
- http://www.lisha.ufsc.br/pub/Gracioli_HotSWUp_2008.pdf
- https://hal.archives-ouvertes.fr/hal-01575352
- https://research.chalmers.se/en/publication/deaa2a2a-fca0-493f-b0da-99bf82a83bb1
- http://camars.kaist.ac.kr/~maeng/cs710/esd07/software-synthesis.pdf
- http://creativecommons.org/licenses/by-nc-nd/4.0
- https://eprint.iacr.org/2013/160
- http://arxiv.org/abs/2202.12662
- https://doaj.org/article/c3a4487f6e3848579f535176604b45e5
- https://drops.dagstuhl.de/opus/volltexte/2023/18524/
- https://resolver.caltech.edu/CaltechAUTHORS:20090831-141451771
- https://ieeexplore.ieee.org/document/9488770
- https://zenodo.org/record/6672752
- https://research.rug.nl/en/publications/c9bb0824-d63c-433a-a8b6-9b3059499ade
- http://hdl.handle.net/11582/1507
- http://upcommons.upc.edu/bitstream/handle/2117/10039/Ranjan.pdf%3Bjsessionid%3DA3026D87A77F5F9FBD5452BA36A4DC35?sequence%3D1
- https://ojs.aaai.org/index.php/AAAI/article/view/6397
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.7.9271
- http://euler.ecs.umass.edu/research/raks-isvlsi-2014.pdf
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/1999/date99/pdffiles/09c_3.pdf
- https://doaj.org/article/de66238ca697460091a3b3690707a228
- https://journal.austms.org.au/ojs/index.php/ANZIAMJ/article/view/7817
- https://inria.hal.science/hal-03084824
- http://arxiv.org/abs/2202.07962
- http://arxiv.org/abs/2308.01240
- https://zenodo.org/record/6363556
- https://doaj.org/article/277fd8e1273d4c35801f2fe75442e1ce
- http://urn.kb.se/resolve?urn=urn:nbn:se:ri:diva-23520
- https://hal.inria.fr/hal-00685276
- http://hdl.handle.net/11585/677163
- http://dx.doi.org/10.1109/ISIT.2005.1523745
- https://doi.org/10.1209/0295-5075/85/28005
- http://repository.tue.nl/887496
- http://hdl.handle.net/11346/BIBLIO@id=2988035754545580332
- https://hal.laas.fr/hal-03763258/file/DRL-AIoTS.pdf
- https://www.aaai.org/Papers/AAAI/2006/AAAI06-063.pdf
- https://digitalcommons.njit.edu/dissertations/1067
- http://wing.comp.nus.edu.sg/~antho/P/P13/P13-2067.pdf
- http://resolver.tudelft.nl/uuid:6d119eba-76e2-4ebd-8dc7-17f865c2d0cb
- https://dx.doi.org/10.3390/computers7020025
- https://hal.archives-ouvertes.fr/hal-01529162
- https://research.tilburguniversity.edu/en/publications/1a75d890-29d6-4081-bf11-3a309b1a74bb
- http://arxiv.org/abs/2208.08227
- https://hal.inria.fr/hal-01637518
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/1995/dac95/pdffiles/35_1.pdf
- http://hdl.handle.net/1911/96341
- http://arxiv.org/abs/2304.07575
- http://www.cs.york.ac.uk/rts/docs/DAC-1964-2006/PAPERS/2000/DAC00_396.PDF
- https://hal.inria.fr/hal-01095116
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.2492
- https://doaj.org/article/18d71b999a5b4fe38de56f7dc2d841af
- https://www.researchgate.net/profile/Alberto_Sangiovanni-Vincentelli/publication/232651546_Synthesis_of_Software_Programs_for_Embedded_Control_Application/links/00b4952bb498b080b9000000.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.5267
- https://hdl.handle.net/1721.1/144767
- https://eprints.lancs.ac.uk/id/eprint/146947/
- https://research.tue.nl/en/publications/2bb83aa4-c160-4d42-8896-f62a55a8cc71
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.5264
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.1453
- http://arxiv.org/pdf/0911.3456.pdf
- http://arxiv.org/abs/2206.13947
- https://hal-cea.archives-ouvertes.fr/cea-03534312/file/jlpea-1142703-english.pdf
- https://research-explorer.ista.ac.at/record/18113
- https://escholarship.org/uc/item/50n838xp
- http://oar.sci-gaia.eu/record/117
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.84.467
- http://www.es.ele.tue.nl/~oana/publications/esr-2007.pdf
- https://hdl.handle.net/11420/52445
- http://cs.stanford.edu/%7Epliang/papers/semantic-parsing-intro.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.7.7781
- http://people.csail.mit.edu/madhu/papers/2013/interactive-conf.pdf
- https://doaj.org/article/19efda4800a24e0789a4eb091d41e86a
- http://www.date-conference.com/proceedings/PAPERS/2010/DATE10/PDFFILES/IP4_05.PDF
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.2778
- http://hdl.handle.net/10356/3254
- https://hdl.handle.net/2027.42/135921
- https://researchrepository.wvu.edu/etd/6457
- https://escholarship.org/uc/item/2ch6v2p2
- http://hdl.handle.net/11346/BIBLIO@id=-6622357234668258372
- https://doi.org/10.1109/MS.2010.119
- https://ieeexplore.ieee.org/document/9744560
- https://biblio.ugent.be/publication/1104904/file/1104910
- http://arxiv.org/abs/2207.07706
- http://udspace.udel.edu/handle/19716/13442
- https://zenodo.org/record/6344914
- https://orbilu.uni.lu/bitstream/10993/36136/1/tuna2.pdf
- http://hdl.handle.net/1802/6278
- https://hal.inria.fr/inria-00475919/file/iterative.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.8440
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.9154
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-90006
- http://arxiv.org/abs/2309.07544
- http://www.mt-archive.info/IWSLT-2011-Heafield.pdf
- http://eprints.iisc.ac.in/27090/1/45.pdf
- https://escholarship.org/uc/item/24j5w1rx
- http://cds.cern.ch/record/1518703
- http://hdl.handle.net/1853/59838
- http://hdl.handle.net/11585/781553
- https://zenodo.org/record/8191801
- https://hal.laas.fr/hal-03428530/file/TaskOffloading-ns3-gym.pdf
- https://docs.lib.purdue.edu/dissertations/AAI10181549
- https://ieeexplore.ieee.org/document/9285951
- http://hdl.handle.net/10.26686/wgtn.17068217.v1
- https://eprints.lancs.ac.uk/id/eprint/137601/
- https://escholarship.org/uc/item/1dx6s0pw
- http://hdl.handle.net/2324/6344
- https://doi.org/10.1002/cpe.2872
- http://www.idi.ntnu.no/grupper/su/bibliography/pdf/2006/Beyer2006percomw.pdf
- http://hdl.handle.net/2376/16338
- http://arxiv.org/pdf/1305.3733.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.70
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.8769
- http://hdl.handle.net/2429/59552
- https://tud.qucosa.de/id/qucosa%3A85463
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0167642306000724/MAIN/application/pdf/6c420924bd65566c14bb70b76a4d35e2/main.pdf
- https://escholarship.org/uc/item/9b2584zz
- https://hal.inria.fr/hal-03084824
- http://d-scholarship.pitt.edu/9054/1/zhao_etdPitt2006.pdf
- https://orbilu.uni.lu/bitstream/10993/36135/1/icsme3.pdf
- http://hdl.handle.net/11585/800233
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.4471
- https://hdl.handle.net/1887/4572
- https://zenodo.org/record/8011320
- http://ieeexplore.ieee.org/search/srchabstract.jsp?tp=&arnumber=4145110&queryText%3DMicroarchitecture+sensitive+empirical+models+for+compiler+optimizations%26openedRefinements%3D*%26searchField%3DSearch+All
- https://hal.inria.fr/inria-00001106/document
- https://hal.inria.fr/inria-00073343
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.8583
- http://hdl.handle.net/1807/109195
- http://hdl.handle.net/1959.13/1333280
- https://escholarship.org/uc/item/1h96n0n1
- http://tubiblio.ulb.tu-darmstadt.de/133999/
- http://paper.ijcsns.org/07_book/201206/20120605.pdf
- http://www.comp.nus.edu.sg/%7Etulika/ISIC14.pdf
- http://arxiv.org/abs/2309.04586
- https://research.monash.edu/en/publications/ed432453-5dc1-4111-a5c0-47c8b9c8f4a1
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.7796
- http://pp.info.uni-karlsruhe.de/uploads/folien/lochbihler11ded.pdf
- http://hdl.handle.net/2440/18605
- http://ufal.mff.cuni.cz/conll2009-st/results/papers/19_conll09st.pdf
- https://tches.iacr.org/index.php/TCHES/article/view/7340
- http://srl.cs.jhu.edu/courses/600.439/engler96vcode.pdf
- https://discovery.ucl.ac.uk/id/eprint/10100294/1/Developments_in_channel_coding.pdf
- http://tud.qucosa.de/api/qucosa%3A28598/attachment/ATT-2/
- https://doaj.org/article/0d4c5b19d2c04df4b76e4487fc254015
- https://eccc.weizmann.ac.il/report/2021/051/
- https://hal.inria.fr/inria-00495666
- https://escholarship.org/uc/item/5pf93714
- http://rmod.lille.inria.fr/archives/papers/Brun14a-IWST-Benzo.pdf
- http://arxiv.org/abs/2209.09593
- https://biblio.ugent.be/publication/3138993/file/3139035
- https://hal.science/hal-03466171
- http://hdl.handle.net/2434/175564
- https://research.tue.nl/en/publications/035d88fe-051b-4a51-aa4b-c1a28ce6591d
- http://dx.doi.org/10.1007/s10766-010-0161-2
- https://hal.archives-ouvertes.fr/hal-01450658
- http://arxiv.org/abs/2112.10684
- https://ijcjournal.org/index.php/InternationalJournalOfComputer/article/view/2076
- https://escholarship.org/uc/item/0m39x48j
- http://hdl.handle.net/11311/1076751
- http://hdl.handle.net/2434/387056
- http://people.csail.mit.edu/jrg/2008/paul-interspeech08.pdf
- https://cronfa.swan.ac.uk/Record/cronfa26941
- https://doaj.org/article/6af023629d444352805ecce128ae1b20
- http://hdl.handle.net/10292/18885
- http://hdl.handle.net/11250/2608932
- http://monarch.qucosa.de/api/qucosa%3A20213/attachment/ATT-2/
- http://www.mt-archive.info/IWSLT-2011-Federico.pdf
- https://openresearch.surrey.ac.uk/view/delivery/44SUR_INST/12148259190002346/13149080000002346
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.6630
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.1073
- https://escholarship.org/uc/item/6dp3v46b
- https://zenodo.org/record/8091247
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.7289
- http://hdl.handle.net/2142/81609
- http://oro.open.ac.uk/24694/1/paper4.pdf
- https://parasol.tamu.edu/publications/download.php?file_id=401
- http://ieeexplore.ieee.org/document/7740545/
- http://eprints.iisc.ac.in/44835/
- http://hdl.handle.net/2152/ETD-UT-2011-08-3987
- https://zenodo.org/record/8089824
- http://resolver.tudelft.nl/uuid:a2310b6a-3dbe-4d83-a0f2-fb6a9a104e50
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.6930
- http://hdl.handle.net/1903/4491
- http://arxiv.org/abs/2206.04615
- http://www.scopus.com/inward/record.url?eid=2-s2.0-80052666222&partnerID=40&md5=4ce2dd8a1c3e9d532aa3ce8f6a4c3ea5
- https://escholarship.org/uc/item/5w72v5s4
- http://hdl.handle.net/2142/110412
- https://zenodo.org/record/1193984
- https://escholarship.org/uc/item/3kr0p102
- http://www.cs.utexas.edu/users/ml/papers/quirk.acl15.pdf
- http://hdl.handle.net/10356/2522
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/1996/iccad96/pdffiles/11a_1.pdf
- http://hdl.handle.net/2142/108570
- http://www.loc.gov/mods/v3
- http://www.aaai.org/ocs/index.php/DC/DC10/paper/viewFile/1648/2392/