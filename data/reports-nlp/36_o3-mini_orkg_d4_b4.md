# Final Report on ManyChecks: Verifying Math Reasoning from Many Perspectives

This report presents an in‐depth analysis of the ManyChecks initiative—a framework oriented on the cross-verification of mathematical reasoning that encompasses both formal proofs and heuristic methods, as well as a rich integration of diverse techniques including symbolic, numerical, and machine learning-based approaches. Our discussion is structured into several segments: an overview of the initiative, a detailed breakdown of the underlying methodologies and paradigms, integration challenges and solutions, exemplary case studies, and future directions. The report draws on recent research developments and experimental validations, providing a comprehensive exploration that spans both theory and implementation.

---

## 1. Introduction

The ManyChecks concept is inspired by the need to verify mathematical reasoning and system correctness across multiple dimensions. Rather than being solely dedicated to verifying formal proofs using computer-assisted verification (e.g., via tools like Coq or Lean), ManyChecks is envisioned to embrace a broader scope that includes informal and heuristic reasoning. This includes:

- **Multi-perspective Consistency:** Validation that extends beyond proof verification by incorporating complementary checks from control-flow, data dependencies, resource assignments, and time constraints.
- **Methodological Diversity:** Harnessing symbolic, numerical, and machine learning based strategies to provide comprehensive coverage over correct reasoning.
- **Framework Versus Evaluative Study:** Serving concurrently as a toolkit for cross-verification of formal proofs as well as an evaluative study of existing multi-view verification methods.

This report organizes the state-of-the-art methods and best practices identified in recent research to provide a deeper context for ManyChecks.

---

## 2. Background and Motivations

### 2.1 The Need for Multi-Perspective Verification

Traditional verification methods often focus on a singular aspect of system correctness, such as control-flow, leaving critical attributes like data integrity, resource management, and timing properties to second order. Recent studies have demonstrated that:

- **Incremental, Modular, and Multi-View Approaches:** Transitioning from waterfall methodologies, modern techniques use incremental paradigms that capture natural language requirements (e.g., through Linear Temporal Logic) and translate them into formal properties for automated consistency checking.

- **Aggregation and ILP Techniques:** Approaches using aggregation functions coupled with integer linear programming have shown that a balanced multi-dimensional analysis yields greater diagnostic insights. Specifically, customizable cost functions quantitatively balance deviations across various perspectives.

- **Advanced Structural Grouping:** Nearly-linear runtime algorithms partition properties based on high-affinity groups (identical or near-identical cones of influence) to facilitate concurrent verification—a crucial requirement for large-scale systems.

### 2.2 Divergence Between Formal and Heuristic Methods

Unlike traditional static verification which relies heavily on formal proof systems (e.g., HOL Light at Intel, Isabelle/HOL, or Lean), ManyChecks also acknowledges the role of heuristic tools such as The Proofchecker. While formal methods guarantee correctness through rigorous proofs, heuristic approaches aim to offer automated guidance, counterexample generation, and adaptable feedback which have notable impacts in industrial applications—particularly when combined with machine learning-driven systems.

---

## 3. Methodologies and Paradigms

### 3.1 Integration of Multiple Verification Engines

ManyChecks integrates diverse verification components including:

- **Static Analyzers and Model Checkers:** For automated and offline verification of predefined proof obligations.
- **Interactive Theorem Provers:** Systems like Coq, Lean, and Isabelle/HOL provide interactive environments that allow for high-assurance proofs with features such as certified extraction (e.g., Coq 7.3’s new extraction mechanism).
- **SMT Solvers and Computer Algebra Systems (CAS):** Hybrid approaches that combine SAT solvers with algebraic methods (including Gröbner basis techniques) enable the verification of both Boolean and algebraic proofs. The STABLE solver represents one such integration, facilitating distinct Boolean and word-level reasoning.
- **Expert System-Guided Transformations:** Rule-based systems are employed to dynamically select transformation flows, reducing computational overhead considerably. These methods have been validated in contexts where industrial-scale problems demand exponential reductions in resource usage.

### 3.2 Multi-Perspective Conformance Checking

The multi-perspective approach considered in ManyChecks represents an evolution from earlier verification methodologies by:

- **Integrated Deviation Analysis:** Customizable cost functions are used to combine deviations measured in control-flow, data dependencies, and other critical dimensions. This integration reduces the biases inherent in traditional conformance checking methods that primarily emphasize control-flow.

- **Aggregative Calibration:** Techniques based on aggregation functions adjust deviation tolerances across multiple constraints. Comparative studies indicate that these methods may offer increased sensitivity and specificity relative to conventional techniques.

### 3.3 Machine Learning and Portfolio-Based Strategies

Modern verification is enriched by machine learning at several junctures:

- **Solver Selection:** Tools like Why3's Where4 utilize machine learning to predict the most optimal SMT solver for a given goal, thus accelerating the discharge of proof obligations.
- **Proof Strategy Learning:** Extensions to Meta-Interpretive Learning that integrate type systems have been shown to improve the learning of effective proof strategies, enhancing interactive theorem proving frameworks.
- **Semantic Feedback Loop:** Innovative systems incorporate cloud-scale data and semantic feedback to refine property partitions and structural grouping, mitigating state explosion challenges during verification.

---

## 4. Integration Challenges and Approaches

The design and deployment of ManyChecks face several integration challenges, which are actively being addressed:

### 4.1 Balancing Formal and Informal Verification

ManyChecks must reconcile the rigorous demands of formal proof verification with the agility offered by heuristic, informal reasoning methods. Key strategies include:

- **Distributed Verification Architectures:** Environments like the smart lean automation engine (SLAE–CPS) exploit cloud, IoT, and agent-based techniques to combine heterogeneous data sources.
- **Bi-Directional Interfaces:** Establishing lightweight, cloud-hosted systems that merge SMT, CAS, and interactive proof assistance (e.g., bi-directional communication interfaces between Lean and Mathematica) are paving the way for dynamic repositories of formalized mathematical knowledge.

### 4.2 Scalability and Concurrency

Verification in multi-core and distributed contexts introduces non-trivial challenges such as floating-point discrepancies and memory explosion. Advanced strategies include:

- **Dynamic Runtime Feedback:** Techniques that incorporate ExBLAS-based accuracy preservation and innovative data structures like Multiplicative Power Hybrid Decision Diagrams have achieved measurable performance improvements (e.g., overheads below 37.7% on 768-core systems).
- **Concurrent Property Partitioning:** Nearly-linear algorithms for grouping properties by high affinity allow for reusable verification efforts across nearly identical cones of influence, reducing overall resource usage.

### 4.3 Cross-Language and Cross-Tool Integration

One significant aspect of ManyChecks is the certification of verification tools themselves. Notable developments include:

- **Certification of Extraction Processes:** Advances in Coq, particularly the introduction of formally verified extraction mechanisms, guarantee that the translation of mathematical proofs to executable code preserves semantic integrity.
- **Modular Verification Pipelines:** Seamless integration of tools such as Test Case Generators, BDD/Boolean Gröbner basis methods, and interactive theorem provers within cohesive pipelines has become essential for industrial-scale verification.

---

## 5. Case Studies and Experimental Evidence

Recent experimental validations illustrate the effectiveness of the multi-perspective approach:

### 5.1 Industrial System Verification

Case studies in areas like train control systems have successfully employed translations between formal languages (e.g., LOTOS, Object-Z, and Z) to automate consistency checking within heterogeneous specification models. These studies demonstrate that:

- Aggregation-based conformance checking yields improved diagnostic accuracy.
- Customizable cost functions efficiently balance diverse deviations, mitigating the overemphasis on control-flow deviations.

### 5.2 High-Performance and Distributed Computational Environments

Verification tasks on HPC platforms have benefited significantly from semantic partitioning and structural grouping techniques:

- **Quantitative Frameworks in Cloud Trust:** Introducing a common quantitative feedback ontology enables the benchmarking and semantic reliability of cloud-based verification systems.
- **Performance Enhancements:** Experiments integrating hybrid SAT/BDD methods report up to a 5x reduction in CPU time and marked improvements in verification depth.

### 5.3 Floating-Point and Parallel Numerical Verification

Challenges in the verification of parallel numerical programs are addressed by coupling symbolic execution with model checking. Notably, comparisons with sequential specifications demonstrate that:

- Structured path condition analysis not only constrains the search space but also significantly enhances the verification of floating-point computations on heterogeneous HPC architectures.

---

## 6. Future Directions and Research Opportunities

Several promising avenues emerge from the synthesis of current research and the ManyChecks framework:

### 6.1 Extended Integration of Heuristic and Formal Strategies

- **Enhanced Expert System Capabilities:** Future work should explore adaptive, rule-based transformations that more seamlessly convert informal textbook proofs into formal sequences. This will involve deeper integration of heuristic decision-making components alongside rigorous formal methods.
- **Unified Verification Standards:** There is scope for developing standard protocols that facilitate the interoperability of a diverse range of verification tools—from interactive theorem provers to automated counterexample generators.

### 6.2 Advancing Scalability and Automation

- **Dynamic Verification Architectures:** Research should focus on building lightweight, distributed verification environments that leverage both cloud computing and multi-core systems. The use of semantic partitioning and novel high-affinity grouping algorithms will be central to these advances.
- **Portfolio-Based and Machine Learning-Guided Solvers:** Further refinement of solver selection models, based on syntactic and statistical analysis of proof obligations, is expected to reduce verification time significantly across industrial-scale applications.

### 6.3 Bridging the Gap between Formal Specifications and Operational Realities

- **Cross-Domain Verification:** It is imperative that methodologies evolve to better relate enterprise-level (informal) specifications with rigorous computational viewpoints. The use of frameworks like RM-ODP provides a solid foundation for this integration, but additional studies are needed to reconcile disparate specification styles effectively.
- **Certifiable Proof Artifacts:** Ensuring that verification tools themselves are certified (e.g., through proof-carrying code or formally verified extraction processes) will become a cornerstone in high-assurance, industrial contexts.

---

## 7. Conclusions

The ManyChecks initiative represents a robust, multi-faceted approach to verifying mathematical reasoning. By integrating formal, heuristic, and aggregated methods, it offers a path towards a more accurate and scalable verification environment capable of addressing both traditional proof obligations and the complex challenges posed by industrial applications. The research landscape—with its advances in modular verification paradigms, machine learning integration, and high-performance distributed systems—provides a rich ecosystem for further exploration and enhancement of the ManyChecks framework.

In summary, ManyChecks is not just a singular toolkit but an evolving paradigm that encapsulates a broad spectrum of verification strategies. Its development promises enhanced diagnostic accuracy, reduced resource consumption, and improved cross-verification capabilities—paving the way for future innovations in both theoretical and applied domains of mathematical and system verification.

---

## References

*While this report synthesizes results from multiple research projects and empirical studies (e.g., ProM, Why3, SLAE–CPS, Coq 7.3 extraction, and hybrid SAT/BDD approaches), further details on experimental configurations, datasets, and specific performance metrics are available in the referenced publications and technical reports in the field of formal verification and model checking.*


*This report has considered all learnings from recent research to provide a comprehensive evaluation of the ManyChecks methodology. Future efforts are expected to refine these approaches further and adapt them to emerging technological challenges in verification and validation.*


## Sources

- http://aspectos.org/papers/nelson-reflection-2001.pdf
- https://doi.org/10.4236/wjet.2020.81008
- http://clip.dia.fi.upm.es/Conferences/Colognet/ITCLS-2003/AcceptedPapers/Andrei.pdf
- https://doi.org/10.1016/S0167-9260(97)00018-7
- http://hdl.handle.net/10161/9813
- https://hal.archives-ouvertes.fr/hal-00128124
- https://zenodo.org/record/5907927
- http://www.theses.fr/2017NANT3026/document
- http://blog.freearrow.com/wp-content/uploads/2012/01/prelim.pdf
- https://mural.maynoothuniversity.ie/8770/
- http://resolver.tudelft.nl/uuid:7192bb13-2b22-4f2f-afaf-3554ca3df5a6
- https://zenodo.org/record/1327798
- http://hdl.handle.net/2440/108008
- https://dx.doi.org/10.3390/s17071500
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.8532
- https://drops.dagstuhl.de/opus/volltexte/2023/18802/
- https://research.tue.nl/nl/publications/the-multiperspective-process-explorer(7bfd5e20-4a5b-4525-8e8d-d2feaea23d57).html
- http://dx.doi.org/10.14279/tuj.eceasst.77.1111.1055
- http://nbn-resolving.de/urn:nbn:de:bsz:352-286431
- http://www.doc.ic.ac.uk/%7Eshm/Papers/typemilproof.pdf
- https://repository.upenn.edu/cis_papers/266
- https://hal.archives-ouvertes.fr/hal-02427795/document
- https://eprints.lancs.ac.uk/id/eprint/137465/
- http://kar.kent.ac.uk/30829/1/odpsiBoitenDerrickv3.pdf
- http://eprints-phd.biblio.unitn.it/1177/1/main.pdf
- http://hdl.handle.net/1721.1/6068
- http://arxiv.org/pdf/1403.6085.pdf
- http://hdl.handle.net/2144/11405
- https://scholarcommons.sc.edu/aii_fac_pub/142
- http://www.cs.le.ac.uk/people/tg75/arw13.pdf
- http://hdl.handle.net/10.1184/r1/6492902.v1
- http://fm.csl.sri.com/UV10/submissions/uv2010_submission_9.pdf
- https://tel.archives-ouvertes.fr/tel-01798332
- https://doi.org/10.1145/2429069.2429085
- http://www.michaelbeeson.com/research/papers/ProofAndComputation.pdf
- http://hdl.handle.net/11582/1958
- https://hdl.handle.net/2454/40483
- http://arxiv.org/abs/1301.7462
- http://www.elsevier.com/wps/find/journaldescription.cws_home/621920/description#description
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.322
- https://journals.lib.washington.edu/index.php/acro/article/view/15389
- http://hdl.handle.net/11582/2092
- http://mural.maynoothuniversity.ie/8217/1/JP-Predicting-2016.pdf
- http://repository.tue.nl/691069
- https://hal.inria.fr/hal-01824815
- https://doi.org/10.4204/EPTCS.118.2
- http://www.ccs.neu.edu/home/wahl/Publications/lrwy12.pdf
- https://journals.lib.washington.edu/index.php/acro/article/view/15397
- http://www.dbpia.co.kr/Article/NODE06602422
- https://surface.syr.edu/eecs_etd/224
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.2755
- http://hdl.handle.net/11582/479
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.527
- http://prosecco.gforge.inria.fr/personal/hritcu/students/topics/2015/quick-chick.pdf
- http://bpmcenter.org/wp-content/uploads/reports/2014/BPM-14-07.pdf
- https://figshare.com/articles/Theorem_Proving_in_Lean/6492902
- https://hal.inria.fr/hal-01088692/file/article.pdf
- https://hal.science/hal-00150914/document
- http://knowledge.uchicago.edu/record/1788/files/Bonakdarpour_uchicago_0330D_14677.pdf
- http://www.ai-lab.it/armando/pub/frocos09.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.6526
- https://research.tue.nl/en/publications/84293ae5-3718-4856-bca5-b3f69be155f0
- https://doaj.org/article/c8584d1fbaa74e6bb47141c7e3b3b204
- http://arieg.bitbucket.org/pdf/gurfinkel_cv.pdf
- http://www.cs.york.ac.uk/rts/docs/DAC-1964-2005/papers/2005/dac05/pdffiles/p779.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.62.9912
- http://arxiv.org/pdf/1405.5003.pdf
- https://zenodo.org/record/7313584
- https://hal.archives-ouvertes.fr/hal-01126146
- http://hdl.handle.net/10.1184/r1/6622046.v1
- https://hdl.handle.net/11511/56061
- https://hal.inria.fr/inria-00189670v3/document
- https://lirias.kuleuven.be/bitstream/123456789/642734/2/0323-3.pdf
- https://publications.rwth-aachen.de/search?p=id:%22RWTH-CONV-123475%22
- http://eprints-phd.biblio.unitn.it/166/2/thesis.pdf
- https://journal.ub.tu-berlin.de/eceasst/article/view/773
- http://publica.fraunhofer.de/documents/N-311251.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.2564
- http://eprints.iisc.ac.in/6411/1/a_floating.pdf
- https://doi.org/10.1007/978-3-642-40176-3_10
- http://www.cse.yorku.ca/~jonathan/students/GaoThesis.pdf
- https://doi.org/10.4236/jtts.2021.111003
- https://scholarworks.umass.edu/dissertations/AAI3078679
- http://hdl.handle.net/2117/99938
- https://research.utwente.nl/en/publications/verifythis--verification-competition-with-a-human-factor(48c34e97-2257-4126-bee8-0528424e319c).html
- https://eprints.lancs.ac.uk/id/eprint/52274/
- https://research.utwente.nl/en/publications/verification-of-program-parallelization(e36589ce-aad3-4ad5-95fd-9fbd0626542b).html
- http://ix.cs.uoregon.edu/~michal/Classes/04u/fsv/readings/Biere-BMC.pdf
- http://ntur.lib.ntu.edu.tw/bitstream/246246/7994/1/922213E002104.pdf
- http://hdl.handle.net/2434/236481
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.6305
- https://zenodo.org/record/5905601
- https://research.tue.nl/en/publications/881a9179-7839-4fea-b2bd-8667310342aa
- http://hdl.handle.net/10393/7536
- https://www.matec-conferences.org/10.1051/matecconf/202134302011/pdf
- http://vstte17.lri.fr/
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-61892
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.6745
- http://software.imdea.org/~julian/docs/Samborski.Forlese.2008.SEFM.pdf
- https://corescholar.libraries.wright.edu/knoesis/576/
- http://publica.fraunhofer.de/documents/N-180311.html
- http://hdl.handle.net/2117/113246
- http://homepage.cs.uiowa.edu/%7Etinelli/papers/StuEtAl-FMSD-13.pdf
- http://hdl.handle.net/11567/532614
- https://hal.inria.fr/hal-03592675v2/file/main.pdf
- https://pms.cs.ru.nl/iris-diglib/src/getContent.php?id%3D2012-Lensink-ProofPrograms
- https://hal.inria.fr/hal-01802488
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.4790
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.12
- https://researchbank.rmit.edu.au/view/rmit:21889
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.2499
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-301330
- https://eprints.lancs.ac.uk/id/eprint/21028/
- https://zenodo.org/record/6329773
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.2631
- https://lib.dr.iastate.edu/cgi/viewcontent.cgi?article=1048&amp;context=aere_conf
- http://www.unirioja.es/cu/joheras/papers/mlipgii.pdf
- https://zenodo.org/record/4071675
- http://www4.in.tum.de/%7Eschaetz/papers/SchaetzHuberFM99.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0167642398000173/MAIN/application/pdf/6d42e5ecf0b15dc713ce526ac5da18e1/main.pdf
- http://porto.polito.it/2654254/
- http://hdl.handle.net/10.1184/r1/6608804.v1
- http://hdl.handle.net/10044/1/24437
- https://www.zora.uzh.ch/id/eprint/116533/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.9178
- https://zenodo.org/record/7100208
- https://hal.archives-ouvertes.fr/hal-01111193
- http://handle.uws.edu.au:8081/1959.7/44720
- http://hdl.handle.net/11583/1397883
- http://publica.fraunhofer.de/documents/N-244770.html
- https://orcid.org/0000-0002-1900-3901
- https://hal.inria.fr/hal-00639977
- http://hdl.handle.net/2144/3789
- http://hdl.handle.net/2434/264140
- http://hdl.handle.net/1822/35225
- https://research.tue.nl/nl/publications/f5387f12-882d-470e-a0a2-e2a00ca9f841
- http://kar.kent.ac.uk/21276/1/cvc_results.pdf
- https://hdl.handle.net/1721.1/128880.2
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.79.2989
- http://hdl.handle.net/10.1184/r1/6602861.v1
- http://hdl.handle.net/2429/32572
- http://leodemoura.github.io/files/lean_cade25.pdf
- https://hdl.handle.net/2027.42/175663
- https://www.deeds.informatik.tu-darmstadt.de/fileadmin/user_upload/GROUP_DEEDS/Peter/SOSP11-wip.pdf
- http://hdl.handle.net/10.1184/r1/6591176.v1
- https://zenodo.org/record/5493554
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.6105
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.8309
- https://zenodo.org/record/7928649
- http://hdl.handle.net/10536/DRO/DU:30042192
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.3244
- http://ai.eecs.umich.edu/people/rounds/HSCC/83.pdf
- https://mdpi.com/books/pdfview/book/2657
- https://kar.kent.ac.uk/21731/1/a_formal_framework_for_viewpoint_1_bowman.pdf
- http://www-soc.lip6.fr/~cecile/558_10931370_Chapter_9.pdf
- http://fm.csl.sri.com/UV10/submissions/uv2010_submission_18.pdf
- https://works.bepress.com/jeffrey_keisler/16
- http://www.scopus.com/inward/record.url?scp=85086267241&partnerID=8YFLogxK
- https://research.vu.nl/en/publications/97981d68-6901-48e5-bc6b-cebd72acb68e
- http://hdl.handle.net/10.1184/r1/6587147.v1
- http://ul.qucosa.de/api/qucosa%3A15779/attachment/ATT-0/
- https://hal.archives-ouvertes.fr/hal-00150914/document
- http://hdl.handle.net/1822/66208
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1040.6791
- https://zenodo.org/record/4246174
- https://zenodo.org/record/6999824
- http://hdl.handle.net/1885/218107
- https://www.zora.uzh.ch/id/eprint/103106/1/35.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.97.7981
- https://research.utwente.nl/en/publications/generating-and-solving-symbolic-parity-games(728ff805-ee8a-4674-8277-ce08ba35b143).html
- https://hal.science/hal-00949355v4/file/superaccumulator.pdf
- http://www.easychair.org/publications/?page=504984429
- http://hdl.handle.net/11568/1116818
- https://scholarworks.umass.edu/cs_faculty_pubs/421
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.84.3567
- http://publica.fraunhofer.de/documents/N-96217.html
- https://kar.kent.ac.uk/17284/1/viewpoints_and_consistency%3A_translating_derrick.pdf
- https://research.utwente.nl/en/publications/a-rigorous-approach-to-relate-enterprise-and-computational-viewpoints(26d3db09-9c78-45c5-b782-b3e4e2d43917).html
- http://hdl.handle.net/2066/230789
- https://doi.org/10.1007/3-540-49519-3_18
- https://hal.univ-lorraine.fr/tel-03203922/file/DDOC_T_2021_0023_EL_OURAOUI.pdf
- http://edoc.mpg.de/618673
- http://www.scopus.com/inward/record.url?scp=85053603425&partnerID=8YFLogxK
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1570868305000753/MAIN/application/pdf/8f2c0b7ce5d45a03be169037bfd310d7/main.pdf
- https://research.tue.nl/en/publications/d59f37f8-763e-42d3-b6c9-a3fec8f88b9b
- http://hdl.handle.net/10400.22/7065
- http://laser.cs.umass.edu/techreports/05-15.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.7559
- https://hal.inria.fr/hal-03656144/file/MANUSCRIPT.pdf
- https://orcid.org/0000-0001-5622-1775
- https://zenodo.org/record/5667545
- http://dx.doi.org/10.1016/j.jlamp.2023.100941
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.1128
- https://hal.inria.fr/hal-00762330/file/paper-ieee.pdf
- http://www.loc.gov/mods/v3
- https://research.vu.nl/en/publications/66658ce0-7c0b-4dac-8c53-0a1356f5b003