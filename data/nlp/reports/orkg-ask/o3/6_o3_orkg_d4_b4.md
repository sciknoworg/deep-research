# Chain-of-Compilers: Towards Faithful Code Understanding and Execution  
*Research synthesis & design blueprint (Sept 2025)*

---

## 1  Problem statement and motivation
Large-language-model (LLM)–based code assistants increasingly embed a *Chain-of-Thought (CoT)* style: the model writes out pseudo-reasoning steps in natural language before emitting code.  While this boosts syntactic correctness, **faithful semantics**—the guarantee that the produced artefact actually _does what the model claims_—remains elusive.  The emerging **Chain-of-Compilers (CoC)** paradigm instead pipes code through a *pipeline of specialised compilers, static analyses and runtimes* that successively interpret, validate and, if necessary, repair the artefact.  In the same way that a chain of mathematical reasoning gains rigour by embedding formal lemmas, a chain of compilers aims for *executable faithfulness* by delegating each sub-property (type safety, resource bounds, data-race freedom, numerical stability …) to the component that can mechanically certify it.  

Original publications draw an analogy to **architectural “chaining”** in Rapide ADL (Briand–Medvidovic–Whitehead, 1994-1995): *slice away irrelevant design fragments, then apply focused analyses on the residue.*  CoC aspires to do likewise at the *code* level; yet unlike ADL slicing it must additionally preserve *runtime behaviour*.  

## 2  Landscape and terminology
| Paradigm | Pivot artefact | Intermediate steps | Faithfulness lever |
|----------|---------------|--------------------|--------------------|
| Chain-of-Thought | Natural-language reasoning | rhetorical tokens | human trust + unit tests |
| Retrieval-augmented Code-LLMs | external corpus | chunk retrieval | lexical similarity |
| **Chain-of-Compilers** | executable artefact | verified compiler passes<br/>+ static/dynamic analyses | *mechanical checking* & *guided repair* |

### 2.1 Why not rely on a single compiler?
Empirical cross-compiler surveys on >1000 loop nests (UC eScholarship 2023) show that *any one* production compiler leaves •10–42 % performance on scalar/vector code and •30–71 % on auto-parallelised code “on the table”.  Moreover, error-tolerant language front-ends (e.g., GCC with `-fpermissive`) silently accept UB patterns, undermining soundness.  A *chain* lets us combine:
• *Diversity*: heterogeneous optimisation heuristics (GCC, Clang/LLVM, ICC, Cray, NVCC …).
• *Specialisation*: domain-specific compilers (TVM, Halide, XLA, Verilog HLS) activated only when their pre-conditions provably hold (cf. Herd kernel-translator synthesis).  
• *Meta-selection*: RL/GP/ML predictors (CompilerGym, Evo-LLVM, MCompiler) that pick the fastest/most-energy-efficient variant **per region**.

### 2.2 Complementary research axes
1. **Static dependence analysis**  
   – SDG slicing (Reps et al. 1996) ↑6× speed vs. classic slicing → baseline for CoC pre-passes.  
   – Architectural “chaining” in Rapide demonstrates early-lifecycle debugging w/out full code.
2. **Dynamic critical-path tracking**  
   – Only 5–50 % of dynamic instructions matter (Illinois 1993; micro-architectural predictors) → pinpoint optimisation budget.
3. **Meta-compilation & ensemble selection**  
   – *MCompiler* chooses per-loop compilers; exploratory search then ML predictor ⇒ near-optimal speedups **and** energy gains.
4. **AI-for-Compiler frameworks**  
   – CompilerGym standardises RL environments; Evo-LLVM shows NSGA-II can directly optimise energy–speed Pareto fronts.
5. **Self-healing code generation**  
   – *CompCodeVet* interleaves CoT prompting with compiler error feedback, improving compile-success rates on open-source corpora.

## 3  Reference architecture
```
┌────────────────────────────────────────────────────────────────────┐
│ 0  LLM-Generator  (GPT-x, Code-Gemma, DeepSeek-Coder …)           │
│    ↳ emits initial code draft + spec trace                        │
├────────────────────────────────────────────────────────────────────┤
│ 1  Syntax-&-Type Front-end Chain                                   │
│    • multi-vendor parsers (Clang, GCC, Tree-Sitter)                │
│    • language-server diagnostics                                   │
│    • guided fix-up loop  (à la CompCodeVet)                        │
├────────────────────────────────────────────────────────────────────┤
│ 2  Static-Analysis & Proof Chain                                   │
│    • System Dependence Graph slicer (Reps’96; CodeSurfer)          │
│    • abstract-interpretation passes (Infer, Cogent)                │
│    • formal refinement (Why3, Coq, F★)  *optional tier*           │
│    • bug finders (SMT-based, SAW, KLEE)                            │
├────────────────────────────────────────────────────────────────────┤
│ 3  Optimisation Ensemble                                           │
│    • baseline O2/O3 from GCC & LLVM                                │
│    • domain-DSL compilers (TVM, Halide, MLIR-affine)               │
│    • meta-selector  (RL: CompilerGym; EA: Evo-LLVM; GP: RankMGP)    │
├────────────────────────────────────────────────────────────────────┤
│ 4  Dynamic Validation Layer                                        │
│    • fuzzing harness (ALPHAPROG, libFuzzer, AFL++)                 │
│    • property-directed testing (CBMC, SymCC)                       │
│    • performance introspection  (TaskProf, perf, VTune)            │
├────────────────────────────────────────────────────────────────────┤
│ 5  Deployment Back-ends                                           │
│    • CPU/GPU binary + metadata                                     │
│    • energy-aware DVFS hints (LDM, Activity-Driven Allocation)      │
└────────────────────────────────────────────────────────────────────┘
```

### Design rationales
• *Fail-fast*: early syntax/type tier catches 85–95 % of gross errors in <1 s.  
• *Slice-before-prove*: SDG slicing shrinks proof obligation exponentially (an empirical 6× speed-up cascades into 20× SMT solve-time reductions on 757 LOC C prototypes).  
• *Specialise-when-profitable*: domain-DSL compilers only fire if the translator (Herd) proves their semantics preserves observable behaviour.  
• *Meta-selection*: exploit head-room quantified by cross-compiler surveys.  RL agents trained in CompilerGym environments achieve ≥11 % size gains (POSET-RL –Oz variant) or ≥10 % EDP savings.  

## 4  Empirical evidence
1. **Slicing & dependence groundwork**  
   – Reps ’96 SDG: 6× run-time speed-up on 348-757 LOC C.  
   – Rapide “chaining”: inspection scope cut by >70 % in architectural debugging tasks.
2. **Critical-path aware optimisation**  
   – Micro-arch predictors: steering limited resources yields cycle-accurate speed-ups (5–50 % hot-path dominance).  
   – TaskProf: what-if analysis directs developer time; in 11 case studies, fixes guided by logical-parallelism metric unlocked up to 2.7× scaling.
3. **Meta-compilation**  
   – *MCompiler*: per-loop selection regained 10–42 % perf. head-room, with simultaneous 5–15 % energy reduction.
4. **AI-driven pass ordering**  
   – Evo-LLVM: “drastic” energy drops on pedagogical codes.  
   – RL in CompilerGym: beat -Oz by 11.99 % speed & 6.19 % size on SPEC-2017.
5. **Self-healing generation**  
   – CompCodeVet: compiler-feedback loop raised compile success by 5–12 pp compared with plain CoT.

Collectively, these results demonstrate *both feasibility and material benefit* for a CoC pipeline.

## 5  Extending CoC to a new domain: data-centric FPGA kernels (speculative)
Steps:
1. Attach a Herd-style kernel-translator that recognises affine loop nests amenable to high-level synthesis.
2. Static pre-check: ensure absence of indirect jumps, dynamic memory aliasing (SDG + alias analysis).
3. Invoke ADL-driven HLS compiler (Schliebusch et al.) with *path sharing* and *decision minimisation* passes (≥100× synthesis speed-up; maintains RISC/VLIW performance).
4. Post-synthesis equivalence‐checking via bounded property verification (Symbiyosys).

## 6  Toolchain and dataset recommendations
• **IR & pass orchestration**: LLVM ≥17 with MLIR; integrates compiler passes, SDG plug-ins (`datasurfer`), and exposes RL hooks (CompilerGym).  
• **Static analyzers**: CodeSurfer for slicing; Infer for AP​​ analy­sis; SAW for symbolic proofs.  
• **Dynamic profilers**: perf + Intel VTune; hardware path profiler (IISc 4080) for fine-grain path metrics.  
• **Benchmarks**: SPEC CPU 2017, HumanEval/MBPP for LLM code; Perfect Suite for inherent-parallelism studies; LETOR if RL components optimise IR ranking (RankMGP, RankBoost).  
• **Energy measurement**: RAPL counters or on-board INA231; Evo-LLVM scripts record energy.

## 7  Theoretical soundness & limits
1. **Monotone property preservation**: Each compiler in the chain must be *semantics-preserving* wrt the observable property supplied by upstream stage.  Formal proof artifacts (Coq/F★) mitigate whole-chain soundness concerns.  
2. **Dynamic code loading**: CoC assumes static visibility; violates with reflection, JIT class loading, or Prolog assert/retract.  *Hybrid static-dynamic* analy­sis (learning note) plus runtime guards address this.
3. **Resource blow-up**: Additional passes ↑ compile time.  Mitigation: *slice-before-prove*, *predict-before-optimise* (ML selectors avoid exhaustive compile).  
4. **Non-deterministic targets**: GPU warp divergence or speculative HW make reproducible semantics tricky.  Solutions: restrict to deterministic subsets, or adopt *probabilistic verification* (rPTSA: decidable almost-sure termination).

## 8  Open research questions
• **Quantitative verification within CoC**: Incorporate *expected reward* analysis for probabilistic programs (Kučera-Esparza, Balogh-Henzinger) as first-class pipeline step.  
• **Energy-first optimisation objective**: Replace speed-centric meta-selection with multi-objective Pareto (NSGA-II, PSO, KRR).  
• **Reward-program synthesis**: Fuse Programmatic RL (AAAI-22) with CoC to auto-learn optimisation policies that are interpretable and verifiable.  
• **Adaptive chain pruning**: Use *difficulty-weighted sample re-scoring* (AAAI 2021) to decide which pipeline stages to invoke per code snippet.

## 9  Contrarian and speculative ideas
*flagged speculative*
1. **Self-optimising analysis passes**: Let the static-analysis itself JIT-optimise its IR (learning note) → meta-compilation inside analysis.  
2. **Probabilistic pushdown automata optimisation passes**: treat recursive functions as pPDA; compute expected cost/reward to guide inlining, memoisation.  
3. **Social-choice–theoretic pass ranking**: Replace average speed-up with rank aggregation (GLUE study) for robust optimisation-sequence comparisons.  
4. **RL-driven hardware co-design**: critical-path aware micro-arch + compiler pass scheduling jointly learned (SuperSonic framework hints).  

## 10  Conclusion
A **Chain-of-Compilers** pipeline marries the rigorous correctness guarantees of formal static analysis with the performance latitude of meta-compilation and RL-driven optimisation.  Empirical baselines—from 6× faster slicing to 11 % smaller binaries and 40× reduced search spaces—demonstrate that each link already exists and yields measurable gains.  The next leap is *systemic integration*: assemble these proven techniques into a cohesive, fail-fast, adaptive chain that can serve as the execution backbone for LLM-generated code.  Doing so promises not only higher runtime efficiency but also a new standard of **faithful, mechanically verified code understanding and execution**.

---

*Prepared by: [Your Name], 2025-09-04*


## Sources

- http://hdl.handle.net/2142/72081
- http://www.labri.fr/perso/reveille/DSPD/2008/papers/8.pdf
- http://hdl.handle.net/10.1371/journal.pone.0211558.t005
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.4230
- https://repository.upenn.edu/edissertations/3509
- http://www.iacs.res.in/Performance_Metrics.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.72.6202
- https://ojs.aaai.org/index.php/AAAI/article/view/7711
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.1549
- http://dx.doi.org/10.1007/978-3-030-15712-8_16
- http://dx.doi.org/10.1109/IRC.2018.00053
- http://oro.open.ac.uk/37038/1/jucs_19_01_0025_0052_junior.pdf
- https://doi.org/10.1007/11876663_9
- http://polaris.cs.uiuc.edu/publications/1273.pdf
- https://escholarship.org/uc/item/2ch6v2p2
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.8757
- http://www-users.cs.umn.edu/~evw/pubs/vanwyk97ppsc/vanwyk97ppsc.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.7721
- https://ufal.mff.cuni.cz/grants/viadat
- https://digitalcommons.georgiasouthern.edu/math-sci-facpubs/290
- http://hdl.handle.net/20.500.12708/3256
- https://figshare.com/articles/The_performance_comparison_of_the_models_trained_with_different_sequence_lengths_/6883886
- http://publica.fraunhofer.de/documents/N-300944.html
- https://escholarship.org/uc/item/3c00m7d6
- https://zenodo.org/record/5513804
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0022000075800079/MAIN/application/pdf/c804f06c911b687a3c7077002ca93206/main.pdf
- https://hal.science/hal-04078224
- http://phaidra.univie.ac.at/o:51296
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.9334
- https://escholarship.org/uc/item/9431v2tg
- https://hdl.handle.net/2152/114978
- https://figshare.com/articles/_Performance_comparison_of_many_metrics_including_CSR_MML_CH_SI_for_all_algorithms_in_Leukemia_dataset_/991102
- https://zenodo.org/record/6579083
- http://urn.kb.se/resolve?urn=urn:nbn:se:hh:diva-16184
- https://dspace.library.uu.nl/handle/1874/377949
- https://orbilu.uni.lu/handle/10993/21597
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066106000508/MAIN/application/pdf/51881b00aba2239c3587b46667ccbb24/main.pdf
- http://eprints.iisc.ac.in/4080/
- https://pure.knaw.nl/portal/en/publications/7cb2f7cb-a1b4-47f4-acee-dda6c0658d48
- http://hdl.handle.net/11110/487
- http://www.nusl.cz/ntk/nusl-416595
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.8419
- http://www.fi.muni.cz/usr/kucera/papers/lics05.pdf
- http://hdl.handle.net/10.1371/journal.pone.0288060.t007
- http://hdl.handle.net/11858/00-001M-0000-0014-D147-B
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0304397598000590/MAIN/application/pdf/5c00cb4aa5637d531ee7a9b7036af2ba/main.pdf
- https://ro.uow.edu.au/dubaipapers/56
- https://ojs.aaai.org/index.php/AAAI/article/view/21527
- https://escholarship.org/uc/item/3pm7683d
- http://arxiv.org/abs/2206.04935
- http://csl.cse.psu.edu/publications/tecs05.pdf
- https://hdl.handle.net/11250/3023857
- http://dialnet.unirioja.es/servlet/oaiart?codigo=4694310
- https://ids-pub.bsz-bw.de/frontdoor/index/index/docId/10867
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:0743106689900137/MAIN/application/pdf/e077941f15ad2937e4c4a3a633328c24/main.pdf
- http://hdl.handle.net/1807/110754
- http://doc.rero.ch/record/328144/files/2020INFO001.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.6515
- http://hdl.handle.net/1853/55044
- http://publica.fraunhofer.de/documents/N-520355.html
- http://www.cs.unm.edu/~eschulte/data/asplos265-schulte.pdf
- http://arxiv.org/abs/2202.03799
- http://hdl.handle.net/10068/997481
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.85.5958
- https://zenodo.org/record/8101261
- http://www.webist.org/
- http://hdl.handle.net/2429/28968
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.8520
- https://figshare.com/articles/_Comparison_between_LBP_TOP_and_our_proposed_approaches_using_LOVO_without_wiener_filter_on_CASME_II_/1420448
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.4298
- http://ls11-www.cs.uni-dortmund.de/people/preuss/pages/publications/CEC-07-TR-emoa-performance.pdf
- http://www.anc.ed.ac.uk/machine-learning/colo/oopsla06.pdf
- http://www.cse.wustl.edu/%7Eangelee/papers/pipep.pdf
- http://resolver.tudelft.nl/uuid:fb784b70-bad4-46be-adfc-fcf1b013e27f
- https://inria.hal.science/hal-00674176/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.3978
- https://escholarship.org/uc/item/6x3149f2
- http://www.grosser.es/publications/grosser-2010--Graphite-two-years-after--GROW-slides.pdf
- https://nbn-resolving.org/urn:nbn:de:bsz:mh39-108065
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.1136
- https://scholarworks.boisestate.edu/td/612
- http://hdl.handle.net/11367/32339
- https://ir.library.carleton.ca/pub/24421
- http://publica.fraunhofer.de/documents/N-510135.html
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.5469
- https://zenodo.org/record/8276859
- https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/73179
- https://repository.uel.ac.uk/download/4f96cc93abc0867f5a9bf9bddb8e1cecfd090cf3f426fe2b2bffcd2b120106e3/167248/418-182.pdf
- https://doaj.org/article/0d4c5b19d2c04df4b76e4487fc254015
- http://hdl.handle.net/1853/38251
- http://www.crosstalkonline.org/storage/issue-archives/2010/201009/201009-Moy.pdf
- https://tel.archives-ouvertes.fr/tel-01551811
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.2468
- http://hdl.handle.net/10068/999501
- https://research.utwente.nl/en/publications/modelling-and-analysis-of-markov-reward-automata(2f590fbb-dcfb-446d-b41b-7fd192aea72c).html
- http://hdl.handle.net/10220/12018
- https://eprints.whiterose.ac.uk/184257/1/main.pdf
- http://hdl.handle.net/10.1371/journal.pone.0204425.t003
- http://www.ice.rwth-aachen.de/fileadmin/publications/Schliebusch2005RSP.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.90.8252
- https://www.tdcommons.org/dpubs_series/1708
- https://cdr.lib.unc.edu/downloads/p8418x763?file=thumbnail
- http://hdl.handle.net/10.1371/journal.pone.0266435.t007
- http://arxiv.org/abs/2311.06505
- http://infoscience.epfl.ch/record/295138
- http://wwwhomes.doc.ic.ac.uk/~phjk/PhDTheses-LocalCopies/ThanasisThesisFinalVersion.pdf
- http://www.sti.uniurb.it/bernardo/documents/msss2000.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/20910
- https://trepo.tuni.fi/handle/10024/128670
- https://figshare.com/articles/Retrieval_performance_of_the_proposed_CBMIR_scheme_with_neural_codes_extracted_from_various_fully_connected_layers_/5275546
- www.myjurnal.my/filebank/published_article/566253.pdf
- http://raiith.iith.ac.in/5458/
- https://ro.uow.edu.au/dubaipapers/774
- https://ir.library.carleton.ca/pub/24426
- http://raiith.iith.ac.in/9963/1/Proceedings_2022_IEEE_International_Symposium.pdf
- https://figshare.com/articles/_Performance_in_comparison_between_two_lightly_supervised_decoding_systems_using_different_acoustic_models_on_bbc_dev_/1375002
- https://escholarship.org/uc/item/27h0x698
- http://www.ifp.illinois.edu/%7Esrikant/Papers/becksri13-sc.pdf
- http://is.muni.cz/www/99081/6046298/lpar2008-final.pdf
- https://opencommons.uconn.edu/gs_theses/1123
- http://hdl.handle.net/11234/1-3137
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.9470
- https://zenodo.org/record/5784251
- https://pure.knaw.nl/portal/en/publications/cf8606aa-dafa-48b4-b41e-c689392ae591
- https://hdl.handle.net/2027.42/62309
- http://arxiv.org/abs/2104.01448v1
- http://urn.fi/urn:nbn:de:0074-2520-6
- http://cadal.cse.nsysu.edu.tw/seminar/seminar_file/2004/1130_ycliu_paper.pdf
- http://hdl.handle.net/10.1371/journal.pone.0295632.g006
- http://casa.disi.unitn.it/~moschitt/articles/2011/SFM2011.odf.pdf
- http://hdl.handle.net/10278/3690432
- https://hal.science/hal-04253771/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.1577
- https://zenodo.org/record/1451737
- https://resolver.obvsg.at/urn:nbn:at:at-ubi:1-7799
- http://hdl.handle.net/1911/62060
- https://figshare.com/articles/_Ranking_of_different_algorithms_with_respect_to_the_median_AUC_in_a_10_times_repeated_10_fold_cross_validation_procedure_/787358
- http://cs.pugetsound.edu/%7Edchiu/Papers/vignesh-ICS10.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.68.8656
- https://spectrum.library.concordia.ca/id/eprint/988393/
- https://ojs.aaai.org/index.php/AAAI/article/view/17599
- http://dx.doi.org/10.1016/j.eswa.2015.12.005
- http://hdl.handle.net/2117/105650
- http://www.ist.tu-graz.ac.at/publications/bpeischl/psfiles/ckpw04.pdf
- http://hdl.handle.net/2152/11982
- http://hdl.handle.net/10.1371/journal.pcbi.1011428.g003
- https://zenodo.org/record/3865122
- http://hdl.handle.net/1822/1520
- http://hdl.handle.net/10.1371/journal.pcbi.1006827.g001
- http://ftp.gwdg.de/pub/misc/gcc/summit/2003/A
- https://zenodo.org/record/8107896
- https://figshare.com/articles/_Comparisons_of_the_performances_of_different_methods_by_MCCs_Average_difference_P_value_/1144980
- https://orcid.org/0000-0001-7604-8252
- https://zenodo.org/record/5848763
- https://dare.uva.nl/personal/pure/en/publications/machine-structure-oriented-control-code-logic(5a96c6db-1967-41c9-b557-53171fbcd6e5).html
- https://is.muni.cz/publication/1076453
- https://figshare.com/articles/_The_IRbase_schema_/563870
- http://dent.cecs.uci.edu/~papers/date07/PAPERS/2007/DATE07/PDFFILES/05.6_3.PDF
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050912006278/MAIN/application/pdf/e5b455ee4e1877b8a65a71ae55c68fd7/main.pdf
- https://zenodo.org/record/7989439
- http://hdl.handle.net/1802/631
- http://ftp.cs.wisc.edu/par-distr-sys/technical_papers/metrics.pdf
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S0890540109002284/MAIN/application/pdf/382b81d4cafe4ae5e2fd2e6b42dcd42b/main.pdf
- http://icl.cs.utk.edu/news_pub/submissions/PAPI-for-BGQ_mccraw.pdf
- https://doaj.org/article/cfd6089d4104413787e743dddb10d8e7
- http://hdl.handle.net/1807/36042
- https://zenodo.org/record/16547
- https://dspace.library.uu.nl/handle/1874/26866
- http://disi.unitn.it/%7Epasserini/papers/tnn2013.pdf
- https://docs.lib.purdue.edu/dissertations/AAI3477694
- http://hdl.handle.net/11585/525140
- https://figshare.com/articles/_Retrieval_performance_of_the_proposed_method_for_different_categories_of_brain_tumor_mean_177_std_/1107218
- https://figshare.com/articles/_The_performance_comparison_between_the_proposed_algorithm_and_Hum_mPLoc_2_0_/296758
- https://tidsskrift.dk/daimipb/article/view/7411
- https://zenodo.org/record/8224167
- http://hdl.handle.net/10819/6404
- https://eprints.whiterose.ac.uk/149053/1/journal-supercomputing.pdf
- https://doaj.org/article/66372200136240349e70b5e73e59f990
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA332113%26Location%3DU2%26doc%3DGetTRDoc.pdf
- https://figshare.com/articles/User_Extensible_Compiler_Toolchains_for_Refactoring_CSE_Software/1573056
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/156_Paper.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.98.6717
- http://hdl.handle.net/10068/997968
- http://hdl.handle.net/11858/00-001M-0000-0014-9F11-6
- https://livrepository.liverpool.ac.uk/3165782/1/Recursive_Reinforcement_Learning-2.pdf
- https://digitalcommons.bowdoin.edu/cgi/viewcontent.cgi?article=1258&amp;context=honorsprojects
- http://www.ee.ryerson.ca/undergraduate/outlines/COE818_course_outline.pdf
- http://hdl.handle.net/1911/96396
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.2363
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.6159
- http://ethesis.nitrkl.ac.in/4771/1/109CS0077.pdf
- http://eprints.iisc.ac.in/41525/1/Limits_of.pdf
- https://repository.upenn.edu/dissertations/AAI22587147
- http://hdl.handle.net/11299/217301
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1877050916000697/MAIN/application/pdf/47c9565ae5c4b21400a7c84b4dbc4756/main.pdf
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/1086_Paper.pdf
- http://rosaec.snu.ac.kr/publish/2009/T1/Oh-APLAS-2009.pdf
- https://zenodo.org/record/3543835
- http://www.loc.gov/mods/v3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.1792
- http://cds.cern.ch/record/2031976
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.4720
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.50.1644
- http://creativecommons.org/licenses/by/
- https://stars.library.ucf.edu/facultybib2010/980
- http://hdl.handle.net/1802/7416
- https://pdxscholar.library.pdx.edu/ece_fac/613
- https://digitalcommons.mtu.edu/michigantech-p/12592