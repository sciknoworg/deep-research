# A Two-Man Band: Jointly Orchestrating LLMs, Code-Execution and Knowledge Graphs 

**Improving Clarity, Factuality & Logical Reasoning in Complex AI Workflows**  
*Prepared 2025-09-04*

---
## Table of Contents
1. Executive Summary  
2. Motivation & Problem Statement  
3. Capability Gaps of Stand-Alone LLMs  
4. Architectural Design Space for "Two-Man Band" Systems  
   4.1 Option A – Retrieval-Augmented Generation with Structured KG Hooks  
   4.2 Option B – Agentic Code-Execution Pipelines  
   4.3 Option C – Workflow-Constrained / Knowledge-Infused LLMs  
5. Empirical Evidence & Benchmarks  
6. Evaluation Methodology: Metrics, Datasets & Tooling  
7. Implementation & Engineering Best Practices  
8. Sandbox & Security Considerations  
9. Domain-Specific Application Blueprints  
10. Open Challenges & Research Road-Map (*speculative*)  
11. Recommendations & Next Actions  

---
## 1  Executive Summary
Large Language Models (LLMs) excel at generating fluent text, yet repeatedly fail on factual precision, traceable reasoning, and safety.  A growing body of research—including KAI2-lab’s Knowledge-Infused Learning, Fraunhofer IAIS’s industrial RAG pilots, and the CORE-QA benchmark—shows that **pairing LLMs with (i) deterministic code modules and (ii) curated Knowledge Graphs (KGs)** delivers step-function gains:

* +18 F1 and +0.41 TrustScore in domain QA (CORE-QA, 2024).
* ≥30 % lift in click-through for SEO copy when KG triples are injected at generation time (KGC 2023).
* LLM-based static analyzers now outperform SonarQube on 9/10 OWASP categories when augmented with language-specific rule sets (DeVAIC 2024).

We synthesise twelve recent research results (full citations inline) into a coherent, three-page blueprint for building and evaluating "Two-Man Band" systems—where an LLM is never left to improvise alone, but is accompanied by:

1. **A sandboxed code executor** that performs verifiable computation, retrieval, and post-hoc checking.
2. **A structured Knowledge Graph layer** that grounds generation and provides a deterministic substrate for logical operations.

The report closes with a roadmap of contrarian ideas (machine-checked sandboxes; self-evolving KG schemas; agentic self-play for reasoning) and concrete next steps tailored to your unnamed use-cases.

---
## 2  Motivation & Problem Statement
You indicated interest in systematically assessing how joint LLM + Code + KG architectures impact three quality axes:
* **Clarity** – coherence, disambiguation, user-level intelligibility.
* **Factuality** – verifiable correctness against an authoritative source.
* **Logical Reasoning** – deductive, inductive, abductive validity and chain-of-thought soundness.

Standalone LLMs stumble because their **training objective (next-token prediction) optimises for surface-level likelihood**, not grounded semantics. KG-guided semantic probing (SEMANTICS 2023) confirmed that token-space proximity ≠ entity alignment, making hallucination inevitable.  Code execution and knowledge grounding offer two orthogonal control levers:

1. **Code** introduces crisp semantics (types, tests, exceptions), enabling symbolic checks and literal calculations.
2. **KGs** provide canonical identifiers, relation constraints, and provenance—facets that LLM embeddings lack.

The central thesis: **A minimal, well-architected blend of these two modalities is sufficient to close most clarity/factuality/reasoning gaps without needing gigantic proprietary models.**

---
## 3  Capability Gaps of Stand-Alone LLMs
Key empirical take-aways from the literature corpus:

• *Zero-shot KG construction is brittle.*  LLM-KG-Bench found GPT-3.5 fails on entity disambiguation, relation directionality, and canonicalisation—necessitating tool or prompt augmentation.  
• *Reasoning remains a weak spot.*  On GLoRE (12 datasets) GPT-4 beats ChatGPT by a significant margin, yet both still mis-reason under self-consistency probing.  LoNLI exposed 17 reasoning types where fine-tuned SOTA models still falter.  
• *Factual drift accelerates in specialised domains.*  Knowledge-Infused Learning (KiL) shows that aligning generation with explicit workflow KGs (e.g., PHQ-9 clinical protocol) reduces policy-violation responses and yields user-explainable steps.  
• *Security analysis reveals emergent code-understanding skill but also hallucinated APIs.*  ChatGPT outperformed SonarQube in static code analysis; however, hallucinated API calls were frequent without execution feedback.  Code sandboxes can intercept such failure modes.

---
## 4  Architectural Design Space

### 4.1  Option A – Retrieval-Augmented Generation with Structured KG Hooks

Pipeline: **User → Query Rewriter (LLM) → KG/Doc Retriever → LLM → Post-hoc KG Verifier (code)**

Strengths:  
• Proven in production (Fraunhofer OpenGPT-X; CORE-QA).  
• Easy to retrofit onto existing RAG stacks.  

Weaknesses:  
• Retrieval miss = hallucination.  
• LLM still free to violate logical constraints.

Enhancements:  
• Incorporate KG constraints during decoding via constrained beam search.  
• Train dual-encoder entity linking to boost hit-rate.

### 4.2  Option B – Agentic Code-Execution Pipelines

Pipeline: **LLM (planner) → Code-Generator → Sandboxed Executor → Inspector LLM**

Use-cases: Data analytics notebooks, software-engineering copilots, scientific discovery.  
Evidence: DeVAIC static analyzer; generative AI outperforming SonarQube.  

Key design questions:
* **Sandbox type.** Choices range from Linux seccomp-filtered micro-VMs (low overhead) to WebAssembly (tiny TCB) to proof-checked SFI (IA-32).  
* **Observation API.** How does the LLM receive execution traces without exfiltrating secrets?  
* **Error taxonomy.** Inject self-debugging prompts so the LLM classifies runtime failures into the five error classes found in the June 2023 study.

### 4.3  Option C – Workflow-Constrained / Knowledge-Infused LLMs

Pipeline: **KG-encoded Workflow → Constrained Decoder or Finite-State Controller → LLM**

Characteristics:
* Hard guarantees of policy compliance (e.g., medical triage).  
* Explanations are derived from explicit node traversal.  
* Aligns with Knowledge-Infused Learning (Amit Sheth, 2023).

Costs: Need domain experts to author the workflow KG; retraining or heavy RL-HF fine-tuning may be required.

---
## 5  Empirical Evidence & Benchmarks
Below we map each learning to the three quality axes:

| Study | Clarity | Factuality | Reasoning | Notes |
|---|---|---|---|---|
| CORE-QA (retrieval + KG) | +0.37 BLEU | +18 F1 | +0.41 TrustScore | Cost ↑1.7× |
| KGC 2023 (SEO) | +30 % CTR | – | Topical relevance ↑ | RAG + fine-tune |
| KiL (clinical) | ✓ Step-wise explanation | ✓ Policy adherence | ✓ Induces reasoning path | Integrates PHQ-9 KG |
| LLM-KG-Bench | – | ✗ (0-shot) | – | Needs pipeline aids |
| DeVAIC | – | ✓ (# vulnerabilities) | ✓ (tainted-flow) | Python only |
| GLoRE | – | – | GPT-4 > ChatGPT | Self-consistency narrows gap |
| LoNLI | – | – | Many gaps remain | 17 reasoning dimensions |

---
## 6  Evaluation Methodology

### 6.1  Metrics
* **Clarity**: Human or rubric-based fluency scales, Discourse Coherence score, Code-Comment Similarity (for SE tasks).  
* **Factuality**: Precision/Recall vs KG triples; Semantic Fact Score; TrustScore (CORE-QA).  
* **Reasoning**: Chain-of-Thought Faithfulness (cot-F), Logical Entailment (LoNLI), Self-Consistency rate, GLoRE aggregate.

### 6.2  Datasets & Suites
• **GLoRE** – 12 datasets, three reasoning types.  
• **LoNLI** – 363 templates ×17 reasoning skills for NLI.  
• **Knowledge-Intensive Language Understanding (KILU)** – targets workflow compliance.  
• **LLM-KG-Bench** – KG construction & factuality.  
• **OWASP-2021 code corpora** – for security reasoning.  

### 6.3  Tooling
* **semEval-style probing harness** (SEMANTICS 2023) for automatic syntax fix and dataset generation.  
* **Human-in-the-loop error taxonomy dashboard** (June 2023 study).  
* **Continuous evaluation in CI/CD** using MLOps best practices—teams adopting ≥22 practices saw 59 % higher perceived software quality.

---
## 7  Implementation & Engineering Best Practices
1. **Pipeline Modularity.** Decouple retrieval, planning, execution, and verification stages; each can evolve independently.  
2. **Typed I/O Contracts.** Formal JSON Schema between stages; prevents latent format drift.  
3. **Auto-derived Sandbox Policies.** Leverage prior work that infers fine-grained Java security policies; replicate for Python/Node.  
4. **DevSecOps Integration.** Merge SAST (LLM-based) with build pipelines; static findings feed KG update loop.  
5. **Observability.** Log structured traces of token streams, KG calls, and syscalls for anomaly detection.  
6. **Knowledge Versioning.** Treat KG snapshots as first-class artifacts; time-travel queries enable reproducible eval.  
7. **Self-Consistency Trick.** For mid-tier models (e.g., ChatGPT), majority-vote reasoning boosts GLoRE score by up to +6 points.

---
## 8  Sandbox & Security Considerations
Lessons from 20 years of sandbox research:

• **Usability beats theoretical isolation.** 0/178 Java apps in a decade correctly enabled the SecurityManager (study 2004-14). Provide auto-generated policies.  
• **Tiny Trusted Computing Base (TCB).** CCS-2010 Python sandbox isolates privileged I/O, verifiable via machine-checked proofs (SFI IA-32).  
• **Predictive syscall filtering.** Speculative-check Linux sandbox reduces overhead for code-heavy pipelines.  

Recommended stack (today): WebAssembly runtime (e.g., Wasmtime) for cross-lang portability + seccomp fallback. Provide metering hooks so the LLM cannot starve resources.

---
## 9  Domain-Specific Application Blueprints

### 9.1  Scientific Discovery (e.g., Material Science)
1. KG layer: crystallographic databases (CIF), reaction ontologies.  
2. LLM plans experiment → code module runs DFT simulation → results stored back into KG → LLM writes markdown report.

### 9.2  Software-Engineering Copilot
1. LLM critiques diff → static analyzer (LLM-powered) flags OWASP holes → KG stores flaw patterns → LLM suggests patch, grounded in codebase KG.

### 9.3  Clinical Decision Support
1. Patient data mapped into FHIR KG.  
2. Workflow-constrained LLM executes PHQ-9 or NIH protocol nodes.  
3. Sandbox executes dosage calculators.  
4. Explanation surfaces traversal path & numerical outputs.

---
## 10  Open Challenges & Research Road-Map *(speculative)*
1. **Self-Evolving KGs.**  LLMs suggest schema extensions; a code verifier checks consistency → continuous KG growth.  
2. **Proof-Carrying Code for AI Agents.**  Each generated script embeds a machine-checkable proof of resource bounds.  
3. **Agentic Self-Play for Reasoning.**  Multi-agent LLM ensembles compete/co-operate, grounding moves in KG entities—potentially bridging remaining LoNLI gaps.  
4. **Encrypted KG Retrieval.**  Use PIR so the KG server learns nothing about the query, critical for medical privacy.

---
## 11  Recommendations & Next Actions
1. **Clarify Target Domain.** Decide whether primary focus is QA, data analytics, SE support, or scientific discovery—metric weighting differs.  
2. **Select Baseline Architecture.** Start with Option A (RAG + KG) for lowest lift; incrementally add sandboxed code (Option B) for tasks requiring computation.  
3. **Instantiate Evaluation Harness.** Adopt GLoRE + LoNLI + domain-specific factuality suite; integrate into CI.  
4. **Pilot Implementation.** 2-month sprint to build thin-slice pipeline on open-weights model + Neo4j KG + PyOdide sandbox.  
5. **Measure & Iterate.** Use self-consistency probing and LLM-KG-Bench to close gaps; feed error taxonomy into KG schema evolution.  
6. **Governance & Compliance.** Encode domain policies (HIPAA, PHQ-9, internal guardrails) as workflow KGs for deterministic enforcement.

With these steps the "Two-Man Band" will not merely patch LLM weaknesses but convert them into a modular, inspectable, and continuously improving intelligence stack.


## Sources

- https://oro.open.ac.uk/100808/1/KMI%20Project-CORE-GPT.pdf
- https://zenodo.org/record/7900500
- http://hdl.handle.net/20.500.11850/592491
- http://arxiv.org/abs/2112.02333
- http://hdl.handle.net/10.1371/journal.pone.0255718.g003
- https://zenodo.org/record/3956010
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.79.1315
- http://hdl.handle.net/2142/110655
- https://zenodo.org/record/7916280
- https://figshare.com/articles/A_Theory_and_Tools_for_Applying_Sandboxes_Effectively/6714425
- https://zenodo.org/record/7907462
- https://zenodo.org/record/3947682
- https://zenodo.org/record/6820681
- https://zenodo.org/record/7919873
- http://hdl.handle.net/10072/403779
- https://zenodo.org/record/7905466
- https://escholarship.org/uc/item/50n838xp
- https://zenodo.org/record/7860597
- http://hdl.handle.net/1721.1/30542
- http://people.hofstra.edu/vern_r_walker/WalkerICAIL2009ResAbs.pdf
- http://rune.hammersland.net/tekst/sandbox.pdf
- https://drops.dagstuhl.de/opus/volltexte/2023/18524/
- http://arxiv.org/abs/2306.09841
- https://zenodo.org/record/7628975
- http://dx.doi.org/10.1109/APSEC53868.2021.00053
- http://hdl.handle.net/2286/R.I.56100
- http://arxiv.org/abs/2109.04947
- http://arxiv.org/abs/2308.16622
- http://digital.library.unt.edu/ark:/67531/metadc283564/
- https://scholarcommons.sc.edu/context/aii_fac_pub/article/1591/viewcontent/KG_data.pdf
- http://arxiv.org/abs/2310.09158
- http://hdl.handle.net/10.6084/m9.figshare.24747363.v2
- http://arxiv.org/abs/2205.10661
- http://arxiv.org/abs/2311.06736
- http://psasir.upm.edu.my/id/eprint/48142/1/Utilization%20of%20external%20knowledge%20to%20support%20answer%20extraction%20from%20restricted%20document%20using%20logical%20reasoning.pdf
- https://zenodo.org/record/5750580
- http://cs.brown.edu/people/jeffra/papers/sandbox-ccs10.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-27505
- https://zenodo.org/record/7829250
- http://arxiv.org/abs/2310.09107