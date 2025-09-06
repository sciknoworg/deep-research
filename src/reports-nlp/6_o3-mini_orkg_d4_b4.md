# Chain-of-Compilers: Towards Faithful Code Understanding and Execution

## 1. Introduction

Over the past decade, the compiler community has seen a sustained push towards harnessing machine learning, formal verification, and dynamic validation techniques to reimagine how compilers understand and execute code. The Chain-of-Compilers paradigm represents an emergent framework where a sequence of transformation passes—ranging from high-level semantic abstraction to low-level machine code generation—is tightly integrated with advanced optimization strategies. This report synthesizes extensive research findings to outline a vision for a compiler chain that achieves faithful code understanding and execution while managing performance, energy efficiency, and verification precision.

In this report, we detail the rationale behind a chain-of-compilers approach, review potential evaluation metrics, and explore how intermediate representation (IR) transformations, semantic preservation, and machine learning integration can drive next-generation compiler architectures. The discussion builds on interdisciplinary insights from energy-aware frameworks, formal method integration, interactive iterative compilation, and dynamic validation, making a comprehensive case for a multi-disciplinary approach that leverages both static and dynamic verification strategies.

## 2. The Chain-of-Compilers Paradigm and Its Implications

The term "Chain-of-Compilers" connotes a modular yet integrated approach to the compilation process. Traditional monolithic compilers often provide limited visibility into individual transformation stages, placing constraints on both optimization and verification capabilities. By contrast, a chain-of-compilers structure divides the compilation process into well-defined, interoperable stages:

- **Front-End Processing and Semantic Analysis:** Emphasis on sophisticated IR generation that captures both syntactic and semantic nuances. This stage sets the foundation for ensuring that subsequent optimizations preserve the high-level intent of the original source code.

- **Intermediate Representation Transformation:** Each compiler pass is engineered to maintain strict semantic equivalence. The integration of machine learning models—ranging from probabilistic methods to deep reinforcement learning (DRL)—aids in selecting optimal passes, predicting performance trade-offs, and ensuring energy-aware execution.

- **Back-End Code Generation:** Here, architectural and platform-specific optimizations are incorporated. The work includes tightly controlling energy consumption, optimizing memory usage, and ensuring that verified transformations (e.g., via formal methods such as Coq proofs) are preserved.

This modular architecture not only offers granular control over the optimization search space but also provides hooks for integrating iterative and interactive improvement strategies. By externalizing high-level decision processes (as seen in the Interactive Compilation Interface (ICI) developments for compilers like PathScale EKOPath and GCC), the chain-of-compilers framework can leverage external ML-driven heuristics to tune the classifiers effectively.

## 3. Intermediate Representations and Semantic Preservation

A critical requirement for any modern compiler chain is the preservation of semantics across transformation passes. Research on intermediate representations has taken two prominent directions:

1. **IR Transformation Mechanisms:** Advances in designing concise and verifiable IR models ensure that transformations are not only correct but also amenable to formal methods. For instance, projects like Vellvm utilize Coq to mechanize the semantics of LLVM IR, guaranteeing memory safety and preservation of operational semantics during SSA-based transformations.

2. **Integration with Machine Learning:** To navigate the NP-hard optimization spaces, machine learning approaches (e.g., transfer learning, deep reinforcement learning, and probabilistic models) are increasingly embedded in the IR transformation process. These models analyze program features and predict the best sequence of optimizations. With empirical evidence showing speedups upwards of 10–17% in frameworks such as Milepost GCC and MCompiler, such approaches significantly shrink the traditionally massive search spaces.

These two lines of development—formal verification and ML-guided transformation—are not mutually exclusive. Instead, they are complementary in that ML can suggest candidate transformations while formal methods ensure their soundness. This paradigm is particularly crucial in heterogeneous environments where compiler passes must work over a range of architectures, from multicore CPUs to reconfigurable fabrics for neural machine translation systems.

## 4. Evaluation Metrics and Benchmarks for Faithful Code Understanding

Assessing the faithfulness of code understanding and execution requires a careful blend of static and dynamic methodologies. Researchers have proposed several evaluation frameworks:

- **Static Analysis Metrics:** These include false alarm rates, verification scope sizes, and the rigor of separation logic-inspired invariants. Studies have shown that improvements in static analysis (e.g., shortening validation scopes after bug fixes) correlate with improved code safety and maintainability.

- **Dynamic Validation Methods:** Validation frameworks such as the Safety-Progress (SP) model have been adapted to runtime verification strategies. Tools like j-VETO and j-POST validate non-deterministic behaviors while accounting for concurrency safety. Metrics such as enforcement window efficiencies and short-circuiting validation speed-ups are crucial for timely detection of critical errors.

- **Formal Verification Benchmarks:** Projects like CompCert and Verasco provide a baseline for rigor while ensuring competitive performance with non-verified counterparts. The integration of SMT-based techniques (e.g., Alive2 for LLVM’s memory model) serves as rigorous benchmarks for translation validation.

The synergy of these evaluation metrics enables the construction of an optimization and verification chain that is robust even in dynamically evolving environments such as cloud-native architectures and microservices ecosystems. By combining static guarantees with dynamic validations, the chain-of-compilers framework can cater both to predictable execution and adaptive performance in real time.

## 5. Energy Awareness and Hardware Adaptability

Energy-aware compilation frameworks such as EAC have leveraged cycle-accurate energy models to assess consumption within tight error margins (around 6%). This focus becomes increasingly important as energy efficiency and thermal constraints become central to both server and embedded system design.

By integrating energy-performance trade-off strategies within the compiler chain, the following is achieved:

- **Energy-Efficient IR Transformations:** Optimizations can be prioritized not only based on execution speed but also energy consumption metrics. Empirical data (e.g., on AMD Ryzen architectures) indicate that tuning compiler flags can deliver significant energy savings while maintaining competitive performance.

- **Hardware-Specific Calibration:** Advanced compilers are increasingly using metrics like CPU utilization, cache behavior, and memory bandwidth to fine-tune back-end optimizations. Joint architecture-compiler design space explorations have shown promise in mitigating false-sharing and cache contention, particularly in multicore and distributed systems.

- **Convergence of ML and Physical Metrics:** ML-enhanced strategies can predict optimal paths for both performance and energy efficiency. Controlled experiments using transfer learning and deep reinforcement learning techniques have yielded execution-time gains of 11–17% across benchmarks such as MiBench and Berkeley DB.

## 6. Interactive and Iterative Compiler Architectures

One of the most innovative strands converging in the chain-of-compilers concept is the iterative and interactive compilation framework. Tools like the ICI have shown that exposing high-level decision processes to external heuristics enables fine-grained adjustments, reducing the overall search space. This fine control permits real-time compiler adjustments for code regions at the loop or instruction level, paving the way for:

- **Loop-Level and Instruction-Level Adjustments:** Empirical studies have demonstrated that exposing these granular optimization decisions can result in speedups from 23% to nearly 43% in hybrid compilation modes.

- **Meta-Optimization Strategies:** Iterative approaches have leveraged predictive dynamic analysis and statistical heuristics to adaptively tune compiler passes, thus significantly reducing compile time while ensuring rigorous semantic preservation.

- **Dynamic Reconfiguration:** For heterogeneous and multi-threaded environments, iterative compilation provides the adaptive engine needed to continuously update optimization strategies in response to runtime behaviors, thereby improving both energy efficiency and overall execution throughput.

## 7. Machine Learning Integration in Compiler Optimizations

Machine learning has dramatically reshaped compiler designs by replacing static, expert-tuned heuristics with models that can learn from program features. This integration presents multiple advantages:

- **Search Space Reduction:** Deep reinforcement learning models, as seen in frameworks like SuperSonic, can dramatically reduce exploration time. In some scenarios, search times were shortened by up to an order of magnitude. These improvements are particularly significant for phase-ordering challenges, where the selection and sequencing of optimizations are NP-hard problems.

- **Transfer Learning and DRL Techniques:** These have proven effective in adapting learned strategies across diverse codebases, mitigating issues associated with negative transfer. The combination of probabilistic models and elegant cross-domain embedding techniques permits the compiler chain to generalize well even in unseen code patterns.

- **Empirical Successes:** Several studies, notably within Milepost GCC, have reported improvements in execution times (11% decreases on MiBench for ARC processors) and further gains in real-world applications like Berkeley DB. Such outcomes underscore the effectiveness of ML in dynamically guiding the compilation pipeline.

## 8. Formal Verification and Dynamic Validation: Bridging the Gap

Ensuring that every compiler pass preserves the intended semantics is arguably the most challenging aspect of compiler design. A promising solution involves combining formal verification with dynamic validation techniques to establish a robust, end-to-end assurance framework:

- **Mechanized Proofs and SMT Integration:** Formal methods, as implemented in Vellvm (using Coq) and Alive2, validate memory models and transformation passes at scale. These mechanized proofs ensure that even low-level compiler optimizations maintain semantic integrity, with concrete benefits such as the early detection of subtle bugs in memory optimization strategies.

- **Unified Verification Frameworks:** Projects like the Aartifact infrastructure and StaRVOOrS have begun integrating static proofs with runtime checks. This unified approach, which juxtaposes static analysis with dynamic enforcement (e.g., through j-VETO and j-POST for Java), presents a scalable method to continuously monitor and validate software behavior across various execution environments.

- **Hybrid Solutions in Cloud and Concurrency Settings:** Advanced verification frameworks now accommodate both finite and infinite state systems, employing dynamic measurements of validation scopes and coupling them with formal guarantees. Techniques like short-circuiting invariant checkers have demonstrated efficacy in reducing runtime overhead while ensuring strict adherence to safety properties.

## 9. Challenges, Opportunities, and Future Directions

While the chain-of-compilers framework shows impressive promise, several key challenges remain:

- **Scalability:** As compilers evolve to address heterogeneous, cloud-native, and microservices-driven infrastructures, scaling verification and optimization techniques remains a open problem. Research into distributed and cloud-based verification methods is underway to address the state explosion problem and ensure that formal methods are applicable at industrial scale.

- **Integration of Disparate IR Paradigms:** Reconciling traditional IR models with emerging representations tailored for neural machine translation systems and reconfigurable fabrics remains a critical area of ongoing research. Bridging this gap is expected to not only preserve semantic fidelity but also to create bridges between disparate computing paradigms.

- **Balancing Static and Dynamic Verification:** Determining the optimal mix of static guarantees and dynamic validations is essential for systems that operate in real time. Further research is needed on adaptive deoptimization strategies and hybrid verification frameworks that can dynamically adjust the balance between performance overhead and assurance rigour.

- **Advanced ML Integration:** Future directions include the continued development of DRL and meta-optimization frameworks that dynamically adapt to evolving code patterns. Furthermore, techniques like translation memories as adaptive prompts hold promise for maintaining semantic fidelity without the need for exhaustive retraining.

## 10. Conclusion

The chain-of-compilers approach offers a compelling vision for the future of compilation: one that marries the formal rigor of mechanized verification with the adaptive efficiency of machine learning optimizations. By integrating advanced IR transformation techniques, energy-aware strategies, and iterative, interactive compilation architectures, the proposed framework aims to achieve a high level of faithfulness in both code understanding and execution.

The wide-ranging research efforts—from energy-aware models and dynamic validation methods to DRL-enhanced optimizations and formal verification frameworks—underscore the feasibility and potential of a unified, verifiable, and efficient compilation process. Moving forward, the integration of these methodologies is expected to lead to compilers that not only optimize code more effectively but also offer unprecedented assurances of semantic correctness and energy efficiency, pivotal for modern, heterogeneous computing environments.

This multi-disciplinary synthesis sets the stage for continued exploration and refinement of the chain-of-compilers framework. As systems evolve and hardware boundaries expand, the union of machine learning, formal method integration, and iterative interactive compilation promises to redefine the limits of both code performance and trust, ensuring that compilers remain adaptive, robust, and faithfully aligned with real-world execution demands.

---

*End of Report*

## Sources

- http://dx.doi.org/10.26153/tsw/9733
- https://hdl.handle.net/10356/136964
- https://www.aclweb.org/anthology/2020.eamt-1.25/
- https://orbilu.uni.lu/handle/10993/43342
- http://repository.ias.ac.in/101025/
- https://hal.inria.fr/tel-01237164/file/HDR-Erven-Rohou.pdf
- http://repository.tue.nl/646335
- https://tidsskrift.dk/daimipb/article/view/6944
- http://cms.brookes.ac.uk/staff/HongZhu/Publications/swvv3.pdf
- https://hal.inria.fr/inria-00436029
- http://hdl.handle.net/2286/R.I.52121
- https://publikationen.bibliothek.kit.edu/1000025470
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1743%26context%3Dcis_papers
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.3800
- https://doi.org/10.1007/s11219-011-9169-0
- https://hal.inria.fr/hal-01141135
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.8391
- http://www.wseas.us/e-library/conferences/2006bucharest/papers/518-198.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.5368
- http://people.cs.uchicago.edu/%7Etga/pubs/stc-ccgrid14-doct-final.pdf
- https://escholarship.org/uc/item/27h0x698
- https://hal.inria.fr/hal-01097677
- http://dspace.mit.edu/bitstream/handle/1721.1/100386/932082841-MIT.pdf?sequence%3D1
- https://hal.inria.fr/hal-00708821
- http://hdl.handle.net/2262/96391
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1050.3547
- https://hdl.handle.net/2123/28809
- https://theses.hal.science/tel-03511998
- https://hal.inria.fr/inria-00551067
- https://doaj.org/article/182d97d8a7554d4cb8f6914113d88116
- http://hdl.handle.net/1773/48890
- https://hal.archives-ouvertes.fr/tel-02395522
- http://hdl.handle.net/10068/1022106
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.7557
- https://ph.pollub.pl/index.php/jcsi/article/view/2693
- https://tel.archives-ouvertes.fr/tel-00420478
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-148321
- https://hal.inria.fr/hal-00685276
- http://hdl.handle.net/10261/220048
- https://hdl.handle.net/10371/183782
- https://hal.inria.fr/inria-00538772/document
- http://hdl.handle.net/20.500.12380/307923
- http://eprints.iisc.ac.in/10584/1/82.pdf
- https://calhoun.nps.edu/bitstream/handle/10945/15771/investigationofb00smed.pdf%3Bjsessionid%3D341B673A80E154B6D5F061E83E85D3C4?sequence%3D1
- https://escholarship.org/uc/item/3c00m7d6
- https://www.zora.uzh.ch/id/eprint/208888/
- https://eprints.whiterose.ac.uk/184257/1/main.pdf
- https://hal.archives-ouvertes.fr/hal-01265437
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-16184
- https://hal.inria.fr/tel-03371774/document
- https://hal.inria.fr/hal-00903724
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1597%26context%3Dcis_papers
- https://works.bepress.com/eliot_moss/6
- http://publications.lib.chalmers.se/publication/246520-starvoors-episode-ii-strengthen-and-distribute-the-force
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.5569
- http://hdl.handle.net/2117/122685
- https://escholarship.org/uc/item/9431v2tg
- https://research.utwente.nl/en/publications/a-broader-view-on-verification(45deb128-2d83-4ba0-a995-822989004482).html
- https://zenodo.org/record/5572610
- http://hdl.handle.net/20.500.11850/550162
- http://cs-people.bu.edu/lapets/resource/topi2013-integdep.pdf
- http://csl.cse.psu.edu/publications/tecs05.pdf
- http://www.labri.fr/perso/reveille/DSPD/2008/papers/8.pdf
- http://digitool.Library.McGill.CA:80/R/?func=dbin-jump-full&object_id=145639
- https://digitalcommons.bowdoin.edu/cgi/viewcontent.cgi?article=1258&amp;context=honorsprojects
- http://dspace.mit.edu/bitstream/handle/1721.1/37902/132792993-MIT.pdf%3Bjsessionid%3D4A29FE156B7F8DA41D8B174A3AAD5907?sequence%3D2
- http://cadal.cse.nsysu.edu.tw/seminar/seminar_file/2004/1130_ycliu_paper.pdf
- https://research-portal.st-andrews.ac.uk/en/researchoutput/milepost-gcc-machine-learning-based-research-compiler(1042e5a5-7e9b-4503-a58f-9ece794fd4d1).html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.4637
- http://apt.cs.manchester.ac.uk/ftp/pub/apt/papers/ZhaoHorsnellRogersDinnKirkhamWatson_EuroPar07.pdf
- http://hdl.handle.net/10.1184/r1/7798226.v1
- https://drops.dagstuhl.de/opus/volltexte/2014/4820/
- https://ojs.aaai.org/index.php/AAAI/article/view/26585
- http://repository.ias.ac.in/101712/
- https://zenodo.org/record/5563375
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-48680
- http://www.cs.uni-salzburg.at/%7Emaigner/cv-martin_aigner.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.805
- http://hdl.handle.net/20.500.11850/506990
- http://dx.doi.org/10.1145/1869542.1869568
- https://hal.inria.fr/hal-01344110/file/paper063.pdf
- https://escholarship.org/uc/item/50x3k7xn
- https://publications.rwth-aachen.de/search?p=id:%22RWTH-CONV-123475%22
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.1427
- http://oa.upm.es/52831/
- http://hdl.handle.net/1807/81068
- http://www.aaai.org/Papers/Symposia/Spring/2009/SS-09-01/SS09-01-020.pdf
- http://real.mtak.hu/66928/1/pollack.5.2010.2.7.pdf
- https://nbn-resolving.org/urn:nbn:de:hbz:386-kluedo-63678
- http://hdl.handle.net/10679/2257
- http://hdl.handle.net/2434/236481
- https://hal.inria.fr/hal-01242094
- http://udspace.udel.edu/handle/19716/13442
- https://biblio.ugent.be/publication/1104904/file/1104910
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.76.7586
- https://hal.inria.fr/hal-01183129/document
- https://docs.lib.purdue.edu/dissertations/AAI3075736
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.5266
- http://hdl.handle.net/11299/217356
- http://repository.tudelft.nl/assets/uuid%3Ad2ebe038-fc1e-47b4-a708-e043e9d3ca74/thesis-final.pdf
- https://hal.inria.fr/inria-00128507
- http://hdl.handle.net/11567/532614
- http://kameken.clique.jp/Lectures/Lectures2013/Compiler2013/a26-stanier.pdf
- https://research.chalmers.se/en/publication/168912
- http://hdl.handle.net/1773/6891
- https://ojs.aaai.org/index.php/AAAI/article/view/9983
- http://hdl.handle.net/10657/683
- https://escholarship.org/uc/item/4kn8s2hk
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.64.8769
- https://hal.inria.fr/inria-00613575/document
- https://repository.upenn.edu/edissertations/825
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.440
- https://lib.dr.iastate.edu/cgi/viewcontent.cgi?article=1048&amp;context=aere_conf
- https://drops.dagstuhl.de/opus/volltexte/2017/7258/
- https://cris.vtt.fi/en/publications/d3bd028e-f870-4b19-9e23-ef24ecb9f012
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.8227
- https://hal.inria.fr/hal-01078386
- http://hdl.handle.net/11299/217301
- http://static.googleusercontent.com/media/research.google.com/en/us/pubs/archive/41874.pdf
- http://hdl.handle.net/1721.1/100386
- https://www.cs.purdue.edu/homes/suresh/502-Fall2008/papers/kelsey-compilation.pdf
- https://repository.upenn.edu/cis_papers/560
- http://publications.lib.chalmers.se/records/fulltext/168912/local_168912.pdf
- http://www.elsman.com/pdf/optimiser.pdf
- https://hdl.handle.net/1842/39298
- https://hal.inria.fr/hal-01256324
- https://hdl.handle.net/10356/149382
- http://www.cs.berkeley.edu/~fateman/264/papers/copperman.pdf
- http://hdl.handle.net/10.6084/m9.figshare.7763435.v2
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.4886
- http://hdl.handle.net/10945/29588
- http://cristal.inria.fr/~xleroy/publi/Verasco-architecture.pdf
- https://hal.inria.fr/hal-01588422
- http://thescipub.com/PDF/jcssp.2013.749.756.pdf
- http://digital.library.unt.edu/ark:/67531/metadc31002/
- https://repository.upenn.edu/cis_papers/705
- http://pqdtopen.proquest.com/#viewpdf?dispub=3521816
- http://resolver.tudelft.nl/uuid:16ee713c-0651-425f-accb-b8398f09e751
- http://hdl.handle.net/10261/189116
- http://hdl.handle.net/10261/132424
- https://hal-mines-paristech.archives-ouvertes.fr/hal-01526469
- http://dx.doi.org/10.1007/978-3-030-03421-4_1
- http://www.alia4j.org/alia4j-debugging/pdf/aosd304r-yin.pdf
- https://research.utwente.nl/en/publications/a-finegrained-debugger-for-aspectoriented-programming(e1cd5dd2-5de5-4ddc-ad94-d27cf77907aa).html
- https://repository.upenn.edu/dissertations/AAI3592852
- http://www.lsi-cad.com/logic-synthesis/
- http://hdl.handle.net/2142/23164
- https://escholarship.org/uc/item/2h54t3gt
- https://ojs.aaai.org/index.php/AAAI/article/view/10975
- https://biblio.ugent.be/publication/3138993/file/3139035
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.461
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.1053
- http://dx.doi.org/10.1007/s10766-010-0161-2
- https://www.scopus.com/record/display.uri?eid=2-s2.0-84940394110&origin=resultslist&sort=cp-f&src=s&st1=Exploiting+model+profiles+in+requirements+verification+of+cloud+systems&st2=&sid=F2D0AD6DE303B7CC33E6392538AEFFBC.wsnAw8kcdt7IPYLO0V48gA%3a1171&sot=b&sdt=b&sl=86&s=TITLE-ABS-KEY%28Exploiting+model+profiles+in+requirements+verification+of+cloud+systems%29&relpos=0&citeCnt=2&searchTerm=
- http://hdl.handle.net/1911/15935
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-104894
- http://alfa.di.uminho.pt/~danieladacruz/CORTACompilerPaperFinal.pdf
- http://hdl.handle.net/11311/1076751
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-128950
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.1661
- https://ace-design.github.io/devops-at-models/
- https://kar.kent.ac.uk/63812/1/icooolps17-chari-et-al-a-mop-for-optimizing-run-time-variability.pdf
- http://publica.fraunhofer.de/documents/N-300901.html
- https://oa.upm.es/70113/
- https://ojs.aaai.org/index.php/AAAI/article/view/6344
- https://doi.org/10.1145/3378678.3391882
- https://hdl.handle.net/1969.1/189051
- https://hal.archives-ouvertes.fr/hal-02424317/file/esop2020.pdf
- http://www.csc.kth.se/%7Edilian/Papers/facs14.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.4074
- http://hdl.handle.net/1911/96403
- http://dx.doi.org/10.1007/11946441_3
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S157106610700504X/MAIN/application/pdf/0e31253d09ac7e882948b632a02cdafb/main.pdf
- http://purl.utwente.nl/publications/85425
- https://digitalcommons.mtu.edu/michigantech-p/12470
- https://hal.science/hal-03917754/file/camlboot.pdf
- http://eprints.iisc.ac.in/50843/1/sci_com_pro_98_645_2015.pdf
- http://subs.emis.de/LNI/Proceedings/Proceedings110/gi-proc-110-048.pdf
- http://hdl.handle.net/10068/998313
- http://oa.upm.es/52861/
- http://resolver.tudelft.nl/uuid:15f4b654-31a3-4485-b270-ea9e4ded2c2f
- https://orcid.org/0000-0001-7604-8252
- https://ojs.aaai.org/index.php/AAAI/article/view/6339
- https://collections.lib.utah.edu/ark:/87278/s63799x3
- http://cds.cern.ch/record/1530554
- http://hdl.handle.net/10400.22/7065
- http://hdl.handle.net/11311/1062745
- http://arxiv.org/pdf/1111.4737.pdf
- http://doc.rero.ch/record/328144/files/2020INFO001.pdf
- https://research.utwente.nl/en/publications/validating-specifications-of-dynamic-systems-using-automated-reasoning-techniques(531be4e1-37a7-46c9-9ac6-3108cdb73f2b).html
- https://zenodo.org/record/7628219
- http://hdl.handle.net/10068/998415
- https://hal.inria.fr/hal-01185812
- https://www.um.edu.mt/library/oar//handle/123456789/24150
- http://www.scarpaz.com/2100-papers/01191546.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/11248
- http://www.loc.gov/mods/v3
- https://hal.archives-ouvertes.fr/hal-01304898