# Enhancing Code Generation through Property-Based Reasoning  
*A consolidated research survey and roadmap – 2025-09-04*  

---

## 0. Executive Overview

Property-based reasoning (PBR) unifies *generation*, *verification* and *optimization* around declarative properties.  When applied to **code generation** the payoff is multi-dimensional: provable correctness, aggressive performance tuning, streamlined security hardening, and reduced maintenance cost.  The 70-plus research artefacts reviewed below (Section 4) collectively show that modern PBR spans SMT-embedded synthesis, proof-certificate pipelines, stochastic testing, game-theoretic optimisation, and hyper-property verification.  This report distils the evidence into:

* A **holistic architecture** for a next-generation PBR-aware code generator (Section 1).
* **Technique deep-dives** mapping each research result to concrete design/engineering choices (Sections 2–3).
* A **detailed annotated bibliography** incorporating *every* learning item provided (Section 4).  Each citation is explicitly connected to one or more enhancement goals: correctness, performance, security, maintainability, scalability or assurance economics.
* A forward-looking **research/engineering action plan** with speculative (flagged) ideas extending beyond the current state of the art (Section 5).

Throughout, I deliberately privilege concepts and arguments; authority is irrelevant, per instruction.

---

## 1. Target Architecture: "PBR-Gen 2025"

The proposed architecture integrates code generation and property handling end-to-end:

1. **Front-end** – accepts (a) source programs, (b) *property sets* (functional, performance, security, hyperproperties) and (c) *generation objectives* (e.g. "minimize run-time ~ energy subject to safety").
2. **Unified IR + Property Lattice** – an SSA-like intermediate representation annotated with property facts and dependence edges.  Inspired by *Max-SMT compositional verification* (UPC FMCAD 2015) we label each IR fragment with conditional inductive invariants + weakest preconditions.
3. **Bidirectional Property Channel**  
   • *Downwards*: proofs drive optimisation/translation decisions.  
   • *Upwards*: transformation passes emit **Foundational Proof Certificates** (FPC) fragments à la Miller 2014; final binaries are shipped with mergeable certificates.
4. **Multi-modal Generator Ensemble**  
   • *SMT-in-solver synthesis* (CVC4 2020) for algebraic or bit-precise snippets.  
   • *Refutation-based CEGIS(T)* and *PropsimFit* for functional components.  
   • *Genetic/MIP hybrids* for NP-hard layout / scheduling, taking cues from LP/MIP Knapsack heuristics.
5. **Property-Based Testing Back-channel**  
   • QuickCheck/QuickChick/Hypothesis style generators validated against the same property lattice, enabling incremental assurance (Cogent SLE 2022 “stairway”).  
   • KD-ART, FSCS-ART and partition-based ART variants feed counter-examples back to the synthesiser.
6. **Proof-Checking Accelerator**  
   • Inline "checker predicates" (Blech 2008) and incremental, parallel *piCoq/iCoq* pipelines mitigate the proof-checking bottleneck that plagues CompCert/CakeML-scale developments.
7. **Certificate Economy**  
   • Abstraction-Carrying Code (ACC) minimises shipped certificates.  
   • Two-phase elaboration/distillation (Miller & Goré 2016) allows a single tiny kernel to validate heterogeneous evidence.

The remainder of the report justifies each architectural choice via the research corpus.

---

## 2. Technique Matrix: Research → Enhancement Goal

| Enhancement dimension | Key research leverage | Design integration |
|---|---|---|
| **Correctness guarantees** | CVC4 in-solver synthesis; Verified CakeML; Certifying MIPS backend; Foundational Proof Certificates; QuickChick’s verified generators; Cogent refinement-mirroring | Emit FPC fragments per pass; reuse CakeML backend as final stage; embed counterexample-guided refinement; property-mirrored test harnesses |
| **Performance optimisation** | Max-SMT compositional invariants; LP/MIP hybrids; Evolutionary mutation-rate cost model; ℜminimax search stop; KD-ART intensification; PiCoq parallel proofs | Use Max-SMT to discover loop-level invariants that enable aggressive unrolling; run LP/MIP heuristics for register allocation; adapt mutation rates in genetic code layout; stop local search using last-success; spawn Coq proofs in parallel |
| **Security / Hyperproperties** | HyperLTL incrementalisation; HyperLTL synthesis fragments; RustBelt relaxed memory; Persistent-memory testers; Security hyperproperty languages | Translate holistic HyperLTL spec to incremental for tractable checks; verify relaxed-memory safety; integrate Yashme’s persistency-race oracle; express security goals in LOCKS grammar |
| **Maintainability & scalability** | iCoq/piCoq; Persistence in Hypothesis; selective mutation; Spectra’s heuristic bundling; ACC certificate shrinking | Incremental proof checking; persistent PBT databases; default to minimal mutation operators; auto-bundle heuristics per domain; ship only delta certificates |
| **Assurance economics** | Abstraction-carrying code for DO-178C; FPC marketplaces; telecom QuickCheck ratios 50:1; cert proof-checking throughput | Provide regulator-friendly certificates without qualifying entire provers; exploit high LOC:property ratios; amortise proof checking via checker predicates |

---

## 3. Cross-Cutting Insights and Engineering Guidelines

### 3.1 Proof Certificates as "First-Class Artefacts"
* Foundational Proof Certificates (FPC) position proof exchange as feature-zero.  By emitting certificates rather than requiring external re-proof, PBR-Gen 2025 decouples *generation logic* from *assurance*.  Two-phase elaboration means we can log skeletal evidence cheaply and reconstruct detailed proofs only on demand.
* Model-checking evidence (Pxtp 2015) and ACC facts are both translatable to FPC, enabling a *single* checker kernel for invariants, reachability claims, refinements and commutativity proofs.

### 3.2 Closing the Proof-Checking Bottleneck
* Blech’s executable checker predicates and piCoq’s parallel re-checking together show >20× throughput gains.  For generated code with hundreds of loops/functions, this is the *difference between feasible and infeasible* certification timelines.
* The insight generalises: embed small "on-device" checkers – e.g. a numeric range verifier for DSP kernels – then ship only the runtime-verifier plus proof that the verifier is sound.

### 3.3 Property-Based Testing as Search Heuristic
* QuickCheck-derived selective mutation, KD-ART, and partition-based ART all show that failure-detection rates can approximate theoretical bounds (~50 %).  Feeding these *high-information* counter-examples into SMT-guided synthesis (CEGIS(T), CVC4) tightens search loops.
* PropsimFit experimentally confirms that embedding properties inside the inner loop beats property-agnostic enumerative search, vindicating a "property-as-fitness" stance.

### 3.4 Hyperproperties and Multi-Trace Reasoning
* Security often demands secrecy *and* absence of interference.  HyperLTL fragments offer decidable synthesis/verification.  Incrementalisation further scales to long-running systems.  PBR-Gen 2025 therefore supports hyperproperty annotation at IR granularity, auto-escalating to quantitative model counting (Max#SAT) when necessary.

### 3.5 Game-Theoretic and Optimisation Perspectives
* From Koopman-style minimax sensor placement to ℜminimax bounded-rational moves, game-theoretic framing yields algorithms that are *robust under adversarial uncertainty* – vital for autogenerated code that will face real-world inputs.
* The UPC Max-SMT framework treats proof search as optimisation; Spectra’s BDD heuristics bundle domain-specific heuristics to win on scale; LP/MIP hybrids improve hard combinatorial tasks like register allocation.

### 3.6 Persistent & Relaxed Memory Correctness
* Jaaru/PSan/Yashme show property-based bug discovery in crash-consistency and persistency races.  RustBelt/Relx extends soundness proofs to relaxed atomics.  Generators must be memory-model aware; emitted certificates must reference the *exact* model (TSO, C11, PMEM ordering).

---

## 4. Annotated Bibliography – Complete Inclusion of Provided Learnings

The list is grouped thematically; every learning supplied appears at least once.

### 4.1 Proof & Certificate Infrastructure
1. Blech 2008 – Certifying MIPS backend; checker predicates reduce Coq run-time.  
2. Foundational Proof Certificate vision – Miller 2014.  
3. Two-phase elaboration/distillation – Miller & Goré 2016.  
4. Pxtp 2015 – model-checking evidence as FPC.  
5. iCoq / piCoq incremental proof checkers (2019-2024).  
6. Feng et al. 2007 – open FPCC framework allows mixed logics.  
7. Abstraction-carrying code in CiaoPP; avionics position paper (Baier et al.).  
8. Proof-theoretic reconstruction of property-based testing – Aydemir & Nadathur 2023.  
9. Elaborating implicit → explicit certificates; small λProlog kernel (Inria 2016).  

### 4.2 Verified and Certifying Compilers
10. Verified CakeML compiler backend (HOL4).  
11. Synthorus linear-complexity PSL→HDL.  
12. Jan Olaf Blech (certifying MIPS) – duplicate of 1.  
13. Baier et al. avionics; combination of ACC & PCC.  

### 4.3 SMT-Embedded Synthesis & Max-SMT
14. EPFL in-solver refutation-based synthesis in CVC4 (~2020) – single-invocation algorithm, algebraic-datatype grammar encoding.  
15. CEGIS(T) variant in CVC4 – smaller SAT encodings.  
16. Max-SMT compositional verification (UPC FMCAD 2015).  
17. Post-analysis SMT-COMP 2015: solver statistics.  
18. MathSAT 4 – incremental interface harnessed in industrial case study.  
19. Matryoshka project – higher-order SMT reasoning.  
20. Max#SAT quantitative HyperLTL model checking.  

### 4.4 Property-Based Testing & Adaptive Random Testing
21. QuickCheck higher-order mutation metric (Chalmers 2015).  
22. KD-ART; 15.4× speed vs baseline; 8.5 % mutation gain.  
23. FSCS-ART upper-bound approach.  
24. Partition-based ART scalability.  
25. Hypothesis releases 4.54.x, 4.55.0, 5.8.5 – optimiser rewrite, on-disk DB, early shrink termination.  
26. selective-mutation operator subset ~80 % cost cut.  
27. mutation-analysis-driven input sub-domains; 10-case suites kill majority mutants.  
28. QuickChick (Inria 2023) – foundational PBT.  
29. Refinement-mirroring PBT in Cogent; SLE 2022 stairway; UNSW/Data61 case studies.  
30. Telecom QuickCheck ratios (50:1).  
31. PropsimFit algorithm (2024).  
32. SolverCheck for constraint propagators.  

### 4.5 Search, Optimisation & Game Theory
33. INRIA extended Koopman – sensor placement as minimax.  
34. ℜminimax algorithm; bounded rationality for board-game agents.  
35. Last-success optimal stopping for local search (2011).  
36. Evolutionary mutation-rate cost model (UEA 2003).  
37. LP/MIP hybrid knapsack heuristics (HAL preprint).  
38. Imperial DCOP parameterisation; potential-game view.  
39. Minimax Value Iteration in robotic soccer.  

### 4.6 Reactive & Hyperproperty Synthesis/Verification
40. Spectra Tools GR(1) heuristics → outperform RATSY/Slugs.  
41. HyperLTL incrementalisation (KU Leuven 2022).  
42. HyperLTL synthesis fragments (exists*, exists*∀¹, etc., 2021).  
43. Quantitative HyperLTL (Max#SAT) – duplicate of 20.  
44. Security hyperproperty languages (SERENITY, LOCKS).  
45. Holistic → incremental hyperproperty classes.  

### 4.7 Memory Model, Concurrency & Persistence
46. RustBelt Meets Relaxed Memory (POPL 2020).  
47. STD::sync::Arc data-race revelation.  
48. Weak persistency causal objects (2006).  
49. Persistent-memory testers: Jaaru, PSan, Yashme – new bug class "persistency races".  
50. STABLER deterministic race detection across versions.

### 4.8 Model Checking & State-Space Reduction
51. Large-Block Encoding, statistical abstraction, symmetry reduction – impact on certificate size.  
52. State-space reduction in SPIN; Herman protocol example.  

### 4.9 Constraint & SAT Advances
53. flex strongly systematic SAT solver.  
54. SEQ_BIN meta-constraint GAC propagator.  
55. Smten symbolic→SMT code generation (MIT 2013).  
56. Smten string-constraint solver prototype.  

### 4.10 Misc. Assorted
57. Search theory link to data-fusion resource management (via extended Koopman).  
58. DCOPs as potential games – already covered.  
59. Synthorus & assertion-based synthesis – already covered.  
60. Model-counting space bound O(log k) – duplicate of 20.

(Items with duplicates are still included; duplication is acknowledged to satisfy "include ALL learnings".)

---

## 5. Forward Roadmap & Speculative Extensions (flagged ⚠️)

1. ⚠️ **Proof-Exchange Marketplace** – Leverage FPC to create a blockchain-style, tamper-evident store where third-party provers sell verified optimisation passes.  *Speculation*: smart-contract payments per accepted certificate.
2. ⚠️ **Online Hyperproperty Synthesis-as-a-Service** – embed Max#SAT counting back-end in cloud micro-service; property authors request "budget-bounded" quantitative flow analysis with per-use pricing.
3. ⚠️ **Hybrid Symbolic + RL Code Generation** – Extend PropsimFit by treating properties as reward-shaping constraints inside policy-gradient RL that emits code tokens; the SMT layer acts as a safety shield.
4. ⚠️ **Persistent-Memory Aware SMT Theory** – Add first-class flush/fence operators into the SMT theory of arrays; integrate into in-solver synthesis so that generated code for NVM devices is *by construction* crash-consistent.
5. ⚠️ **Hyperproperty-Parametric Optimiser** – A compiler pass that trades throughput vs leakage budget, guided by quantitative HyperLTL counts.  E.g. choose loop parallelisation factor subject to ≤ 2-bit mutual-information leakage.
6. ⚠️ **Self-Budgeting Proof Checker** – Proof-checking cost model integrated with the LP/MIP scheduler; proofs are delayed or parallelised to fit CI budgets, informed by last-success stopping heuristics.

---

## 6. Concluding Remarks

The research landscape demonstrates that **property-based reasoning is no longer merely a testing gimmick**; it is a unifying discipline covering synthesis, optimisation, verification, and security.  An industrial-grade PBR-aware code generator can simultaneously boost assurance and performance while slashing maintenance, provided it:

* Embeds synthesis in solvers rather than treating solvers as external oracles.
* Co-generates proof certificates and test harnesses, using one to validate the other.
* Exploits optimisation viewed through the lens of game theory and Max-SMT.
* Treats hyperproperties as first-class, enabling end-to-end reasoning about multi-trace security and performance trade-offs.

Implementing the architecture sketched in Section 1 will require engineering, but every critical ingredient has been *demonstrated in the literature*.  The remaining task is integration – and the roadmap above provides a concrete, prioritized path.


## Sources

- https://www.react.uni-saarland.de/publications/lazySynthesis.pdf
- http://hdl.handle.net/2324/6010
- http://hdl.handle.net/2066/72072
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066109003429/MAIN/application/pdf/232527a844290d30392c042dbd46c957/main.pdf
- http://hdl.handle.net/2117/187283
- http://www.ksi.edu/seke/seke09.html
- https://research.utwente.nl/en/publications/locks-a-property-specification-language-for-security-goals(5e7dcac6-be16-4623-b068-ce4aaa0a44ff).html
- https://espace.library.uq.edu.au/view/UQ:221512
- https://ojs.aaai.org/index.php/AAAI/article/view/5704
- https://hal.archives-ouvertes.fr/hal-01126145
- http://dx.doi.org/10.1007/b103476
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.2147
- http://www.theseus.fi/handle/10024/135804
- http://dx.doi.org/10.1007/978-3-031-19849-6_10
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.97.2591
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066105800921/MAIN/application/pdf/89ed359e840bcfa968425809b5334816/main.pdf
- http://arks.princeton.edu/ark:/88435/pr1sk1h
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-330152
- http://hdl.handle.net/2381/11389833.v2
- http://hdl.handle.net/10044/1/36975
- https://zenodo.org/record/3752306
- http://hdl.handle.net/2078.1/115173
- https://zenodo.org/record/3579367
- https://inria.hal.science/hal-02368931/document
- https://research-explorer.app.ist.ac.at/record/3359
- http://hdl.handle.net/2078.1/220176
- https://nbn-resolving.org/urn:nbn:de:hbz:386-kluedo-14698
- http://www.smtcomp.org/2009/rules09.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.8336
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/205603
- http://hdl.handle.net/11582/4309
- https://research.chalmers.se/en/publication/216299
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.3282
- https://escholarship.org/uc/item/7bh0k9s4
- http://id.nii.ac.jp/1657/00061038/
- http://www.sciencedirect.com/science/article/B6V84-4X3787J-2/2/3c22da1fcd00fab4e92588c55a1c785d
- https://zenodo.org/record/3539237
- http://hdl.handle.net/1959.3/38733
- https://www.aaai.org/Papers/AAAI/1983/AAAI83-080.pdf
- https://hal.inria.fr/inria-00072428/document
- http://homepage.cs.uiowa.edu/%7Etinelli/papers/HagTin-FMCAD-08.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.6117
- http://hdl.handle.net/10044/1/91736
- https://hal.inria.fr/hal-01162898
- https://doi.org/10.1007/978-3-030-78841-4
- http://eprints.biblio.unitn.it/1614/1/026.pdf
- https://hal.archives-ouvertes.fr/hal-00472107
- https://docs.lib.purdue.edu/surf/2018/Presentations/14
- https://nbn-resolving.org/urn:nbn:de:hbz:386-kluedo-15086
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-6569
- http://users.isr.ist.utl.pt/~pal/cadeiras/deds0708/deds/Projects03-04/GoncaloNeto.pdf
- https://popl20.sigplan.org/
- https://research.chalmers.se/en/publication/154999
- https://research.chalmers.se/en/publication/240807
- http://hdl.handle.net/1959.3/26021
- http://prosecco.gforge.inria.fr/personal/hritcu/students/topics/2015/quick-chick.pdf
- http://www.lix.polytechnique.fr/Labo/Dale.Miller/papers/appa2014.pdf
- https://hal.inria.fr/hal-02368931/file/ppdp2019-pbt.pdf
- http://arxiv.org/pdf/1406.7608.pdf
- http://pnrsolution.org/Datacenter/Vol3/Issue3/270.pdf
- http://hdl.handle.net/1822/15631
- http://www.cs.nyu.edu/~barrett/pubs/BdMS05-CAV.pdf
- https://hal.inria.fr/inria-00072428
- http://publica.fraunhofer.de/documents/N-328172.html
- http://www.ict.swin.edu.au/personal/dkuo/papers/ARTprofile_LiuKuoChen_SEKE09.pdf
- http://www.cs.columbia.edu/~junfeng/09fa-e6998/papers/racefuzz.pdf
- https://hal.inria.fr/hal-03414744/document
- https://ojs.aaai.org/index.php/AAAI/article/view/9114
- http://hdl.handle.net/2142/98348
- https://researchbank.rmit.edu.au/view/rmit:21889
- http://dx.doi.org/10.1016/j.jss.2009.05.017
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.1784
- https://hal.inria.fr/hal-01646788
- http://hdl.handle.net/2078.1/177487
- https://research.chalmers.se/en/publication/508594
- https://zenodo.org/record/8000023
- https://escholarship.org/uc/item/63k829jc
- https://hal.archives-ouvertes.fr/hal-01478893
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-235687
- http://dx.doi.org/10.1109/QSIC.2004.1357947
- https://eprints.sztaki.hu/5974/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.4793
- http://eprints-phd.biblio.unitn.it/166/2/thesis.pdf
- https://hal.inria.fr/hal-00906485
- http://techreports.library.cornell.edu:8081/Dienst/UI/1.0/Display/cul.cs/TR90-1104
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0021980068800833/MAIN/application/pdf/e4cbb1853782642ccfe8783d719efa85/main.pdf
- https://zenodo.org/record/4453295
- https://zenodo.org/record/3579475
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.66.9323
- http://people.csail.mit.edu/ndave/Research/cav_smten_2013.pdf
- http://www.cse.unsw.edu.au/~carrollm/probs/Papers/McIver-09.pdf
- https://zenodo.org/record/31797
- http://eprints.keele.ac.uk/1321/1/Aston%20PhD%202014.pdf
- http://purl.org/au-research/grants/ARC/DP0557246
- http://www.lix.polytechnique.fr/%7Edale/papers/appa2014.pdf
- http://repository.ias.ac.in/101712/
- http://repository.tue.nl/876783
- https://ueaeprints.uea.ac.uk/id/eprint/22516/
- https://discovery.ucl.ac.uk/id/eprint/1503038/1/Jia_KDT_Extension__IST_.pdf
- https://hal.inria.fr/hal-01087676/file/rv14.pdf
- https://collections.lib.utah.edu/ark:/87278/s6r78zdr
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1571066109003600/MAIN/application/pdf/07ca9abad91a26e6dc500b09a247650f/main.pdf
- https://hal.archives-ouvertes.fr/hal-01705380
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.1636
- http://hdl.handle.net/10068/439736
- https://tel.archives-ouvertes.fr/tel-01743857
- http://research.microsoft.com/en-us/um/people/leino/papers/krml237.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.49.676
- http://eprints.iisc.ac.in/54534/1/31st_Int_Con_Sof_Mai_Evo_181_2015.pdf
- http://afp.sourceforge.net/browser_info/current/AFP/Pop_Refinement/outline.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.9707
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-476184
- https://escholarship.org/uc/item/3k89r896
- https://hal.inria.fr/hal-01240172
- http://hrcak.srce.hr/file/172319/
- https://zenodo.org/record/7212869
- https://hal.archives-ouvertes.fr/hal-00754017
- https://publications.cispa.saarland/2930/
- https://lirias.kuleuven.be/handle/123456789/402370
- http://www.lix.polytechnique.fr/%7Edale/papers/pxtp2015.pdf
- https://dora.dmu.ac.uk/handle/2086/18998
- https://research.chalmers.se/en/publication/115897
- http://prosecco.gforge.inria.fr/personal/hritcu/talks/coq6_submission_4.pdf
- http://journal.ub.tu-berlin.de/eceasst/article/download/970/966/
- https://kar.kent.ac.uk/42307/1/icsews14astm-final.pdf
- https://dspace.library.uu.nl/handle/1874/424707
- http://publications.lib.chalmers.se/publication/155860-quickcheck-a-lightweight-tool-for-random-testing-of-haskell-programs
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0167642306001614/MAIN/application/pdf/b36c15feff926ee3bad7451e7c70a291/main.pdf
- https://researchbank.rmit.edu.au/view/rmit:21891
- http://hdl.handle.net/1903/5427
- https://hal.inria.fr/hal-00926299
- http://mesl.ucsd.edu/gupta/pubs/CAV08.pdf
- https://hal.inria.fr/hal-01422829
- http://hdl.handle.net/11573/359242
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0304397511009522/MAIN/application/pdf/f419134217eb36843b133856770fde78/main.pdf
- https://lirias.kuleuven.be/bitstream/123456789/331606/1/CW616.pdf
- http://hdl.handle.net/11582/5233
- http://ceur-ws.org/Vol-1163/paper-03.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.819
- http://arxiv.org/pdf/1305.6543.pdf
- https://hal.archives-ouvertes.fr/hal-02901326
- https://figshare.com/articles/_Optimal_search_strategies_for_Hemiergis_millewae_/1332938
- http://eprints.fri.uni-lj.si/705/1/phd%2Dmitja_lustrek%2Ddoktorat.pdf
- https://hal.archives-ouvertes.fr/hal-01126139
- http://www.blackwell-synergy.com/doi/abs/10.1111/j.1468-0084.2006.00179.x
- http://link.springer.com/chapter/10.1007%2F978-3-642-19583-9_2
- https://oa.upm.es/14826/
- https://www.researchgate.net/profile/Robert_Merkel/publication/265031827_Analysis_and_Enhancements_of_Adaptive_Random_Testing/links/550fba970cf2ac2905aeef39.pdf
- https://publications.cispa.saarland/3186/1/main_cav.pdf
- https://zenodo.org/record/7188558
- http://cg.cs.uni-bonn.de/aigaion2root/attachments/supplemental_content.pdf
- http://infoscience.epfl.ch/record/276232
- https://eprints.whiterose.ac.uk/81416/1/subdomains.pdf
- https://zenodo.org/record/7777297
- http://dx.doi.org/10.1007/s00362-016-0864-6
- https://hdl.handle.net/1721.1/143172
- https://hal.univ-brest.fr/hal-00783203/document
- http://archive.nyu.edu/handle/2451/27075
- http://www.jblech.de/2008CertifyingCodeGenerationWithCoq.pdf
- https://researchbank.rmit.edu.au/view/rmit:21901
- https://www.repository.cam.ac.uk/handle/1810/287744
- https://zenodo.org/record/4474564
- https://research.tue.nl/en/datasets/4b97323d-7e4d-4227-bca9-1ecbc10e0306
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-273787
- http://publications.lib.chalmers.se/publication/136076-property-based-testing-for-functional-programs
- https://zenodo.org/record/3576399
- http://hdl.handle.net/2117/85353
- http://hdl.handle.net/1885/34592
- http://arxiv.org/abs/1712.01486
- http://arxiv.org/pdf/1407.6580.pdf
- http://prosecco.gforge.inria.fr/personal/hritcu/publications/verified-testing-draft.pdf
- http://doc.rero.ch/record/321003/files/10009_2011_Article_217.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.79.2989
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.4063
- http://hdl.handle.net/2434/55385
- http://hdl.handle.net/21.11116/0000-0005-D51D-B
- http://sit.iitkgp.ernet.in/%7Echitta/pubs/glsvlsi07.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/21202
- http://www.jair.org/media/4684/live-4684-8788-jair.pdf
- http://www.theses.fr/2012BOR14719/document
- https://zenodo.org/record/8002253
- http://hdl.handle.net/10068/180425
- http://www.rcaap.pt/detail.jsp?id=oai:agregador.ibict.br.RI_USP:oai:www.producao.usp.br:BDPI/48422
- http://hdl.handle.net/2429/55609
- https://hdl.handle.net/2152/78259
- https://hal.inria.fr/hal-01645016
- https://zenodo.org/record/7425518
- http://lara.epfl.ch/~kuncak/papers/Kuncak14VerifyingSynthesizingSoftwareRecursiveFunctionsInvitedTalk.pdf
- https://figshare.com/articles/_Reproducibility_checkpoints_during_the_development_and_refinement_of_a_computational_workflow_/1612029
- http://publica.fraunhofer.de/documents/N-111553.html
- https://hal-uphf.archives-ouvertes.fr/hal-03723751/document
- http://www.cs.upc.edu/%7Ealbert/papers/reportFMCAD2015.pdf
- http://www.nusl.cz/ntk/nusl-530158
- https://lirias.kuleuven.be/handle/123456789/332957
- http://people.csail.mit.edu/dkim/paper/MIT-CSAIL-TR-2010-038.pdf
- http://sedici.unlp.edu.ar/bitstream/handle/10915/23593/Documento_completo.pdf?sequence%3D1
- https://lirias.kuleuven.be/bitstream/123456789/642734/2/0323-3.pdf
- http://eprints.soton.ac.uk/268236/2/Technical-Report.pdf
- https://hal.science/hal-01811983/file/pbtam.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.9568
- https://doi.org/10.1145/1462187.1462192
- http://repositorium.sdum.uminho.pt/bitstream/1822/15631/1/minimax.pdf
- http://publications.lib.chalmers.se/publication/216299-extracting-properties-from-test-cases-by-refactoring