# Final Report: Algorithm-Supported Programming for Intellectual, Mathematical, and Computational Intensive Code Generation

This report delves into recent advances in algorithm-supported programming, a domain that synergistically combines automated reasoning, formal verification, state-of-the-art machine learning, and domain-specific methodologies to generate highly optimized and correct code. The following sections outline comprehensive research learnings, integrating intellectual, mathematical, and computational advances into a cohesive synthesis framework.

---

## 1. Introduction

The growing complexity in high-performance computing, safety-critical systems, and advanced applications like cyber-physical systems demands innovative programming paradigms. Algorithm-supported programming shows promise by leveraging automated theorem proving, neural network verification, and modern high-level synthesis frameworks. This report synthesizes research findings that address three core emphases:

- **Intellectual and Mathematical Sophistication**: With techniques such as superoptimization, hybrid inductive-deductive synthesis, and higher-order reasoning, the research builds robust frameworks that generate code meeting rigorous mathematical specifications.
- **Computational Intensity**: Strategies for high-performance numerical methods, heterogeneous computing optimizations, and advanced task scheduling (e.g., HPC-DAG) are emphasized.
- **Integration of Conventional and Emerging Technologies**: Both formal verification tools (SMT/SMT extensions, Isabelle, Coq, and advanced theorem provers) and modern learning-driven frameworks (GNN-based optimizations, deep reinforcement learning, and counterexample-driven synthesis) have been consolidated in recent work.

This report, spanning over three pages of detailed analysis, discusses the advances, challenges, and future directions in algorithm-supported programming to guide practitioners and researchers in deploying and evolving these cutting-edge methodologies.

---

## 2. Bridging Productivity and Performance with Domain-Specific Languages and Auto-Tuning

A central innovation is the creation of **domain-specific embedded languages (DSELs)**. Systems such as those based on OptiML and Delite demonstrate that DSELs, when auto-tuned, can approach 80% of peak performance even on structured grid computations. This method not only improves developer productivity by abstracting details away from low-level optimizations but also retains efficiency in execution. In related work, high-level DSL transformations (e.g., Tangram) have been used to automatically generate GPU code with dynamic parallelism, achieving speedups up to 7.8x over hand-coded implementations.

### Key Learnings:

- **Auto-Tuned DSELs**: These languages bridge the performance gap by enabling structured problem-specific optimizations. The balance between productivity and low-level performance is critical for both scientific computing and real-time applications.
- **High-Level Synthesis (HLS) and DSLs**: Tools such as Spatial and HeteroCL significantly simplify code bases (reducing code lines by an order of magnitude) while incurring minimal performance penalties (as low as an 8% gap compared to custom RTL).

---

## 3. Formal Methods, Superoptimization, and Automated Theorem Proving

Another major research thrust is in formal methods and automated theorem proving to generate code that is succinct, provably correct, and minimal in instruction length. Tools such as the **Denali-2 superoptimizer** leverage E-graph matching combined with SAT reductions to generate machine code that has been mathematically verified for correctness. This is particularly significant in domains such as fixed-point and floating-point arithmetic, where the correctness of code is paramount.

### Notable Approaches:

- **Superoptimization with Automated Theorem Proving**: Techniques use theorem provers like Boyer-Moore and MetiTarski to rigorously optimize machine-level code. By reducing the verification problem to SAT, these systems offer both minimality and correctness.

- **CEGIS and Template-Free Synthesis**: The evolution of Counterexample-Guided Inductive Synthesis (CEGIS) into CEGIS(T) methods has shown remarkable efficiency improvements. CEGIS(T) leverages an optimized SAT encoding, incremental solving, and the elimination of manually provided syntax templates, offering considerable advantages in multi-instruction and complex constant benchmarks.

- **Higher-Order Reasoning Integration**: Projects like Matryoshka integrate higher-order reasoning into traditional SMT frameworks, extending the SMT-LIB standards to support richer constructs needed for cryptographic and safety-critical system verifications.

---

## 4. Hybrid Synthesis: Melding Deductive, Inductive, and Learning-Based Approaches

Recent research illustrates that solely relying on manual heuristics and traditional inductive logic programming is inadequate for complex synthesis tasks. Instead, a hybrid approach is emerging that combines deductive reasoning, inductive methods (including CEGIS), and learning-based techniques. The SCIDUCTION methodology exemplifies this synergy by integrating structural constraints, loop-free program synthesis, and switching logic synthesis for cyber-physical systems. This ensures that the codes not only meet functional requirements but are also resource-optimized and safe.

### Integrated Techniques:

- **SCIDUCTION**: This method uses counterexample guided inductive synthesis coupled with structural hypotheses to automatically generate optimal loop-free code and fixed-point arithmetic implementations. It directly addresses the non-intuitive aspects of code synthesis that traditional methods struggle with.

- **Code2Inv and GNN-Enhanced Verification**: Utilization of graph neural networks (GNNs) to directly map source code to its verification proofs via counterexample-based learning rewards has proven versatile. In multiple benchmarks, Code2Inv demonstrates enhanced scalability and adaptability to unseen programs. It also operates efficiently both as a Constrained Horn Clause solver and as a meta-solver in syntax-guided synthesis.

- **Hybrid AI approaches in Compiler Optimizations**: Several works have integrated deep reinforcement learning with traditional dynamic programming to optimize DNN execution and code synthesis. These approaches improve efficiency on heterogeneous systems, including ARM, RISC-V, NPUs, FPGAs, and ASICs, by reducing memory footprints and accelerating execution times.

---

## 5. Synthesis for Heterogeneous and Real-Time Systems

As applications increasingly run on heterogeneous systems, from GPUs to multi-core CPUs, the synthesis and scheduling of code require strategies that can handle diverse processing engines. The HPC-DAG framework is one such innovative solution that allows designers to specify multiple, alternative implementations for various processing engines, incorporating real-time task scheduling considerations and handling complications such as task preemption and memory bottlenecks.

### Advances in Real-Time and Heterogeneous Environments:

- **HPC-DAG Model**: It demands that software implementations be dynamically scheduled and task allocations be optimized using frameworks like ILP-based scheduling, ensuring that system performance is robust even under non-ideal preemption costs. This has been applied successfully on embedded, automotive, and avionic platforms.

- **Concurrent and Non-Intrusive Multiprocessing**: Tools such as AthenaMP demonstrate that leveraging OS-level process forking (utilizing mechanisms like copy-on-write) can yield dramatic memory reductions and affect scalability in real-world high-throughput systems (e.g., ATLAS production scenarios).

- **GNN-based Dependency Analysis in LLVM IR**: Systems such as GAHLS use graph neural network representations to optimize memory design space exploration, yielding performance improvements exceeding 14× compared to traditional HLS methodologies. This integration ensures rapid design space exploration without an onerous manual setup.

---

## 6. Advanced Synthesis for Safety-Critical and Energy-Constrained Domains

For areas like deep neural network inference, cryptographic verification, and cyber-physical systems, the accuracy of code and safety guarantees are of utmost importance. Recent work in neural network property verification has reformulated verification challenges as global optimization problems, using Bayesian techniques and feature-guided searches to maintain safety while ensuring performance. Parallelly, the integration of assume-guarantee contracts with abstraction methods has enhanced controller synthesis for distributed and multiperiodic systems.

### Detailed Innovations Include:

- **Verification of DNNs Using DeepSaucer**: Unified environments built on platforms such as Anaconda have enabled significant improvements in verification speed and code reuse, achieving order-of-magnitude speedups in safety-critical applications.

- **Co-design Approaches Combining Custom Hardware**: Integrating algorithmic innovations like low-precision quantization and structured matrix techniques with hardware accelerators (FPGAs, NPUs) has resulted in improved energy efficiency and throughput, which is critical in both mobile and server contexts.

- **Template-Driven Synthesis in Constrained Environments**: Approaches that still leverage structural templates—where user-provided invariants and pre-/postconditions guide SAT/SMT solving—continue to provide practical pathways for automated reasoning, ensuring tractability amidst expansive design search spaces.

---

## 7. Future Directions and Open Challenges

While the research thus far has produced impressive gains, several challenges remain:

1. **Scalability of Verification Overheads**: Although methods like incremental SAT solving and reuse of learned clauses (as seen in CEGIS(T)) offer performance improvements, detailed industrial-scale metrics on memory consumption and long-term maintainability are still sparse. Future work should focus on quantifying these overheads in large-scale deployments.

2. **Integration Across Heterogeneous Platforms**: The migration of synthesis frameworks to ARM/RISC-V and other heterogeneous multi-core environments requires deeper research into concurrency, performance metric prediction (e.g., GNN-based models for HLS), and dynamic scheduling algorithms.

3. **Advanced Representations and Higher-Order Reasoning**: Efforts such as extending SMT-LIB standards and enhancing higher-order reasoners like Isabelle must continue to adapt to the increasing complexity of cryptographic and safety-critical applications.

4. **Exploiting Hybrid AI Methods**: With promising results already seen in Code2Inv and similar systems, further research is warranted to explore meta-learning frameworks that combine inductive, deductive, and learning-based approaches to create robust, self-improving synthesis systems.

5. **Quantitative Synthesis Standards**: Defining stable metrics (e.g., verification time, resource utilization, and fault tolerance) will be essential to evaluate and compare emerging synthesis techniques effectively.

---

## 8. Conclusion

Algorithm-supported programming stands at the intersection of automated reasoning, machine learning, and systems engineering. With integrated approaches such as auto-tuned DSLs, superoptimization driven by SAT/SMT solvers, hybrid synthesis that combines deductive and inductive reasoning, and advanced verification frameworks, the field is well-positioned to address the complex challenges of modern code generation. Despite remaining challenges in scalability and integration, these methodologies already show significant promise in improving computational performance, safety, and resource efficiency.

Moving forward, a proactive research agenda that addresses integration across heterogeneous platforms, refines quantitative performance metrics, and further hybridizes AI with formal synthesis is needed to fully exploit the capabilities of algorithm-supported programming. Researchers and practitioners must continue to innovate at the interface of theory and practice, ensuring that future systems not only meet but exceed the stringent demands of safety-critical and computationally intensive environments.

---

This report has consolidated and detailed multiple research learnings, providing a comprehensive view into current and future trends in algorithm-supported programming. By acknowledging both the impressive strides already made and the challenges that lie ahead, it aims to serve as a reference for further investigation and effective implementation in industrial and academic settings.

## Sources

- http://hdl.handle.net/10044/1/51686
- https://research-explorer.app.ist.ac.at/record/3359
- https://hdl.handle.net/1721.1/138590
- http://cds.cern.ch/record/2006148
- https://mural.maynoothuniversity.ie/15157/
- https://mural.maynoothuniversity.ie/8770/
- http://purl.utwente.nl/publications/92343
- https://hal.inria.fr/hal-01388984
- http://www.fp7-save.eu/papers/EUC2016.pdf
- http://hdl.handle.net/2060/20030064036
- http://hdl.handle.net/1773/41705
- http://www.theses.fr/2019SACLC076/document
- http://hdl.handle.net/10356/76135
- https://collections.lib.utah.edu/ark:/87278/s6ff6rgp
- http://hal.in2p3.fr/in2p3-00537763
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.2337
- http://arxiv.org/abs/2205.06773
- https://ojs.aaai.org/index.php/AAAI/article/view/7652
- http://www.nicta.com.au/pub?doc=7246
- https://zenodo.org/record/6501606
- https://escholarship.org/uc/item/27h0x698
- https://biblio.ugent.be/publication/1077747/file/1077748
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0747717199903462/MAIN/application/pdf/b1e6ae9c9ed89475e1c2b4c2a1fc7b5c/main.pdf
- https://escholarship.org/uc/item/3h97c8wb
- https://escholarship.org/uc/item/0zx0p6wr
- http://resolver.tudelft.nl/uuid:3efc8aae-e31f-47a4-a92c-b9da05917ada
- http://research.microsoft.com/en-us/um/people/nswamy/papers/calibrating-program-synthesis.pdf
- https://dare.uva.nl/personal/pure/en/publications/quantifying-resource-use-in-computations(8838573f-a986-4aff-a664-fd3d856e564c).html
- https://research.utwente.nl/en/publications/d3fada36-4fa4-4ae6-805a-9e47dc80ef0c
- http://cds.cern.ch/record/2002910
- http://ir.uiowa.edu/cgi/viewcontent.cgi?article%3D1546%26context%3Detd
- https://hdl.handle.net/1721.1/143375
- https://research.vu.nl/en/publications/0b0e24bf-54f2-4766-91d9-1dde55b8b4ac
- http://summit.sfu.ca/item/12093
- http://arxiv.org/abs/2205.09702
- http://domino.mpi-inf.mpg.de/internet/reports.nsf/NumberView/94-218
- http://hdl.handle.net/1885/66281
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.3887
- https://computerresearch.org/index.php/computer/article/view/572
- https://digitalcollection.zhaw.ch/handle/11475/16215
- http://hdl.handle.net/2066/103766
- http://hdl.handle.net/1842/4691
- http://arxiv.org/abs/1712.01486
- https://mural.maynoothuniversity.ie/17475/1/RosemaryMonahanVerify2021.pdf
- https://research.aalto.fi/files/75821278/ICCC_2021_paper_37.pdf
- https://resolver.caltech.edu/CaltechAUTHORS:20170404-101550871
- http://hdl.handle.net/20.500.11850/458523
- https://aisel.aisnet.org/isd2014/proceedings2021/methodologies/2
- https://hal.science/hal-01358210/document
- http://www.csee.umbc.edu/%7Etsimo1/papers/files/simon_mcgalliard_multicore_2009.pdf
- http://hdl.handle.net/11858/00-001M-0000-0014-ABEC-A
- http://www.cs.uni-paderborn.de/uploads/tx_sibibtex/programmsFromProofsSE_01.pdf
- https://repository.upenn.edu/edissertations/3788
- http://arxiv.org/abs/2201.08455
- https://hal.inria.fr/hal-00661320
- http://homepage.lnu.se/staff/saplaa/papers/peppher_parco_2011p.pdf
- http://www.nicta.com.au/pub?doc=8105
- http://www.vpri.org/pdf/M2013004_agere.pdf
- http://hdl.handle.net/2429/8990
- https://drops.dagstuhl.de/opus/volltexte/2017/8281/
- http://www.theses.fr/2016SACLS285/document
- https://research.chalmers.se/en/publication/250828
- http://vlsicad.ucsd.edu/Publications/Conferences/112/c112.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.5706
- https://doaj.org/article/685cf01b165944089044a2a264e11a08
- https://hal.inria.fr/hal-02359588
- http://hdl.handle.net/1903/10416
- https://hdl.handle.net/1721.1/144767
- https://eprints.whiterose.ac.uk/110313/1/roscoe.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0747717185800109/MAIN/application/pdf/8043bfa25812f5069ca4a6ab8fa223a7/main.pdf
- https://doi.org/10.21979/N9/GZJ0PW
- https://zenodo.org/record/4429098
- https://juser.fz-juelich.de/search?p=id:%22FZJ-2020-00366%22
- https://hdl.handle.net/2152/115338
- http://hdl.handle.net/2099.1/12514
- http://w3.isis.vanderbilt.edu/publications/archive/scott_j_9_0_1998_model_inte.pdf
- https://zenodo.org/record/6820681
- https://tud.qucosa.de/id/qucosa%3A74884
- http://hal.inria.fr/docs/00/10/58/94/PDF/paper.pdf
- https://mural.maynoothuniversity.ie/8217/
- https://biblio.ugent.be/publication/1339511/file/1339558
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.62.9912
- http://hdl.handle.net/11380/1253758
- http://www.lifl.fr/%7Ebenatita/paper/MOSIM2012.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-22220
- http://hdl.handle.net/1807/103150
- http://dissertations.umi.com/cornellgrad:12023
- https://lirias.kuleuven.be/bitstream/123456789/642734/2/0323-3.pdf
- http://eprints-phd.biblio.unitn.it/166/2/thesis.pdf
- http://hdl.handle.net/11311/964955
- http://hdl.handle.net/10044/1/82639
- http://hdl.handle.net/11311/666039
- http://link.springer.com/chapter/10.1007%2F978-3-642-19583-9_2
- http://hdl.handle.net/2142/22956
- https://digitalcommons.usu.edu/ece_facpub/230
- https://zenodo.org/record/3976706
- https://hal.archives-ouvertes.fr/hal-01995376
- http://edoc.mpg.de/519767
- http://hdl.handle.net/10447/462057
- https://escholarship.org/uc/item/6ng0q1n8
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.6339
- https://hal-ens-lyon.archives-ouvertes.fr/ensl-01252342
- https://zenodo.org/record/1239843
- http://compilers.cs.txstate.edu/papers/diss.pdf
- https://research.tue.nl/en/publications/d3882c9b-31cd-4389-9662-07714f251fdd
- https://inria.hal.science/hal-00944513
- http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20010084145.pdf
- https://escholarship.org/uc/item/421154mt
- https://doi.org/10.1016/j.micpro.2013.08.006
- http://ppl.stanford.edu/papers/ppopp20-chafi.pdf
- http://cds.cern.ch/record/2242909
- https://escholarship.org/uc/item/9p6896qr
- http://fileadmin.cs.lth.se/cs/Personal/Calle_Lejdfors/web.pdf
- https://hdl.handle.net/1842/38446
- http://www.wseas.us/e-library/conferences/spain2002/papers/443-150.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.4254
- http://www-users.cs.umn.edu/~evw/pubs/vanwyk00amast/vanwyk00amast.pdf
- https://hdl.handle.net/2027.42/140897
- http://dx.doi.org/10.1007/978-3-662-48899-7_43
- https://hdl.handle.net/1887/4961
- https://escholarship.org/uc/item/3k89r896
- http://hal.in2p3.fr/in2p3-00657498
- http://dx.doi.org/10.1109/SEAA.2019.00031
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.9911
- https://digitalcollection.zhaw.ch/handle/11475/3278
- http://hdl.handle.net/2027.42/86537
- http://www.cs.york.ac.uk/rts/partes04/final/01_binns.pdf
- https://zenodo.org/record/3764836
- https://hal-cea.archives-ouvertes.fr/cea-01834979
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.7.2047
- https://research.tue.nl/nl/publications/39aefe7f-d879-435a-ac3d-ebeb9daa557a
- https://zenodo.org/record/3503967
- http://hdl.handle.net/11311/1069657
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.73.5949
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.3646
- http://hdl.handle.net/11858/00-001M-0000-0014-ABDC-E
- http://hdl.handle.net/11585/586773
- https://research.chalmers.se/en/publication/236486
- http://drum.lib.umd.edu/bitstream/handle/1903/10416/Srivastava_umd_0117E_11263.pdf%3Bjsessionid%3D83E6FAF9C978F0DFDC8A8B73FB21F73E?sequence%3D1
- https://escholarship.org/uc/item/7c48g766
- http://dx.doi.org/10.26153/tsw/42134
- http://hdl.handle.net/11311/1032177
- http://hdl.handle.net/11568/941592
- https://hdl.handle.net/1842/39298
- http://hdl.handle.net/11858/00-001M-0000-000F-3664-2
- http://arxiv.org/abs/2201.06848
- https://scholarworks.unist.ac.kr/handle/201301/53066
- http://publica.fraunhofer.de/documents/N-487921.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.8454
- http://academiccommons.columbia.edu/download/fedora_content/download/ac:141302/CONTENT/cucs-259-87.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.906
- https://hal.inria.fr/hal-01215992
- https://escholarship.org/uc/item/7dj862k9
- http://arxiv.org/pdf/1402.6478.pdf
- https://juser.fz-juelich.de/record/872819
- https://doaj.org/article/9cbdeac6ef6944b8b19bc658f4a68fc6
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.648.8285
- https://doi.org/10.1051/shsconf/202316302021
- https://depositonce.tu-berlin.de/handle/11303/13881
- http://hdl.handle.net/1887/18622
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/2003/dac03/pdffiles/30_4.pdf
- https://www.aaai.org/Papers/AAAI/1984/AAAI84-004.pdf
- https://hal.inria.fr/hal-03887202/file/paper.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.4654
- https://hdl.handle.net/11380/1294545
- http://eprints.iisc.ac.in/39096/1/Computer.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.4356
- https://zenodo.org/record/3568332
- https://www.repository.cam.ac.uk/handle/1810/334823
- https://ojs.aaai.org/index.php/AAAI/article/view/7711
- https://hdl.handle.net/2152/78259
- http://purl.utwente.nl/publications/71138
- http://hdl.handle.net/11311/964213
- http://arxiv.org/pdf/1201.0979.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-8381563302276154902
- http://hdl.handle.net/11311/1194317
- http://aclweb.org/anthology/P/P14/P14-1012.pdf
- http://iwi.eldoc.ub.rug.nl/root/2006/LNCSAvgeriou/
- http://arxiv.org/abs/2204.13103
- https://zenodo.org/record/808888
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.88.9625
- http://eprints.cs.vt.edu/archive/00000803/
- http://eprints.adm.unipi.it/1938/
- https://corescholar.libraries.wright.edu/cecs_syllabi/1172
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.9651
- https://www.researchgate.net/profile/Roberto_Bruttomesso/publication/251706829_The_MathSAT_4_SMT_Solver_%28Tool_Paper%29/links/0046352cfa2df1c388000000.pdf
- https://ro.uow.edu.au/eispapers1/2325
- http://cds.cern.ch/record/2269119
- https://orbilu.uni.lu/handle/10993/10301
- https://hdl.handle.net/1721.1/134932
- https://hal.univ-lorraine.fr/tel-03203922/file/DDOC_T_2021_0023_EL_OURAOUI.pdf
- https://scholarcommons.scu.edu/cseng_mstr/29
- https://doi.org/10.1007/s10817-024-09709-2
- http://digital.library.unt.edu/ark:/67531/metadc838297/
- https://escholarship.org/uc/item/921805kz
- http://hal.archives-ouvertes.fr/docs/00/08/94/16/PDF/maalej_2004icm.pdf
- http://www.csie.ntu.edu.tw/%7Ehtlin/paper/doc/pakdd14interactive.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26606
- http://hdl.handle.net/2142/110412
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.7847
- https://escholarship.org/uc/item/3421b3h6
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.89.1028
- http://www.cs.berkeley.edu/~bodik/dagstuhl-2011_files/SATSMT-Dagstuhl-Aug8-12-2011-part2.pdf
- http://www.cse.chalmers.se/%7Ejoels/writing/multidev.pdf
- http://hdl.handle.net/11576/2673238
- https://repository.upenn.edu/dissertations/AAI28028527
- https://www.repository.cam.ac.uk/handle/1810/329963
- http://doc.rero.ch/record/329701/files/2020INFO016.pdf
- http://cds.cern.ch/record/2222298
- http://dx.doi.org/10.1109/MM.2011.67
- http://hdl.handle.net/2142/108570
- http://www.loc.gov/mods/v3
- http://www.eecs.berkeley.edu/~nishant/papers/Crowdsolving.pdf