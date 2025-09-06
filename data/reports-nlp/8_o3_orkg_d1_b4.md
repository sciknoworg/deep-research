# Incorporating Chain-of-Context (CoC) into Self-Planning Pipelines for Interactive NL-to-Code Generation  
*Comprehensive technical report & research proposal — 4 Sep 2025*

---

## 1  Problem Statement & Research Focus
Large Language Models (LLMs) already yield impressive one-shot code snippets from natural-language (NL) prompts.  Yet **interactive generation** — iterative dialogue between the developer and the model inside an IDE — still suffers from: 
1. *Plan brittleness*: coherent multi-step intent decomposition is rarely surfaced to the user, making corrections expensive.  
2. *Context evaporation*: transient dialogue history, file system state, and runtime traces are only loosely exploited.  
3. *Poor cross-task generalisation*: models excel on templated benchmarks but degrade badly on unseen domains or tasks.

We hypothesise that explicitly fusing **Self-Planning (SP)** with an extended **Chain-of-Context (CoC)** mechanism addresses all three pain points.  The research angles that follow emphasise **architectural design** and **rigorous, human-in-the-loop evaluation**, while treating IDE integration as an engineering deliverable informed by those findings.

> Clarified priorities (answers to the follow-up questions):  
> • **Primary angle**: Architecture of SP + CoC and empirical protocols.  
> • **Target stack**: Python, TypeScript/JavaScript (web), Rust (systems), SQL (data).  Granularities: function-level *and* project-level (multi-file).  
> • **Data**: We will reuse CrossCodeBench, MultiPL-E, LLM4TDD, API-Bench, plus new human-in-the-loop traces we plan to collect.  Baselines: vanilla GPT-4-Turbo, Contextor, and Self-Planning Code Generation (SP-Code, 2023).

## 2  Landscape Review — Key Empirical Learnings 
Below we map the 12 curated learnings to concrete design/evaluation implications.

| ID | Finding | Implication for our project |
|----|---------|----------------------------|
| L1 | **CrossCodeBench**: unified cross-task protocol | Use as backbone to test generalisation of SP + CoC across code-centric tasks (gen, translate, summarize…). |
| L2 | **SP-Code**: two-phase planning → stepwise generation, SOTA gains | Adopt as baseline; lift to interactive regime & enrich with CoC retrieval. |
| L3 | **SPT-Code**: unsupervised code-semantics pre-training wins | Pre-train CoC retriever on structure-recovery & masked spans to better match code semantics. |
| L4 | **MultiPL-E**: 18-language NL-to-code test suite | Evaluate multilingual transfer; ensures that CoC reasoning transcends Python. |
| L5 | **API-Bench** & **LLM4TDD**: fine-grained traces | Leverage API-aware & TDD traces as demonstration contexts inside CoC. |
| L6 | **ThoughtSource**: unified CoT datasets | Borrow prompt patterns for CoC retrieval diversity. |
| L7 | Formal HMI IDE studies | Adapt their safety-critical usability metrics to assess interactive generator error coverage. |
| L8 | **Auto-CoT**: diversity of reasoning beats manual prompts | Programmatically sample diverse context chains. |
| L9 | Eight hand-crafted CoTs boost GSM8K | Inject a small curated seed of high-quality code CoCs. |
| L10 | **UMARA** instrumentation | Instrument our IDE plugin to log fine-grained user interactions for evaluation. |
| L11 | **Contextor**: bidirectional decoder | Consider hybridising Contextor decoding with SP stepwise execution. |
| L12 | KTH 40-criteria framework | Adopt for holistic comparison of generated code across quality attributes. |

## 3  Conceptual Architecture
### 3.1  Pipeline Overview
```
NL Intent  →  (1) Self-Planner  →  Ordered Step Plan
           ↘  (2) Chain-of-Context Retriever  →  Context Pack (K=8)
Plan + CoC  →  (3) Stepwise Code Generator (Contextor-style)  →  Draft code
 IDE loop  ←─────────────  (4) Critique & Repair Agent  ──────→  Final code
```
1. **Self-Planner**: In-context few-shot planner (finetuned on LLM4TDD & curated reasoning traces) decomposes intent into an *ordered list of sub-goals* tagged with expected artefacts (functions, tests, configs).  
2. **CoC Retriever**: For each sub-goal, it fetches **synthetic chains** (code, tests, docs, runtime errors, commit diffs) from an index built on CrossCodeBench + our live project.  Retrieval scoring mixes dense semantic similarity (SPT-Code embeddings) and structural overlap (AST sketch hashing).  
3. **Stepwise Generator**: A bidirectional decoder à la Contextor consumes `(sub-goal, CoC chunk)` pairs; scheduled sampling mitigates leakage between left-to-right and right-to-left passes.  
4. **Critique & Repair Agent**: Runs test suites, static analysis (Clippy, ESLint, MyPy), and formal checks (if specs present) — then emits patch suggestions.  User can accept, modify, or re-prompt; all interactions are logged via UMARA hooks.

### 3.2  Why Chain-of-Context, not just Chain-of-Thought?
*Chain-of-Thought* exposes *reasoning steps* in **tokens**.  *Chain-of-Context* generalises this to **arbitrary artefacts** that may condition generation: prior commits, StackOverflow snippets, API docs, test diffs, telemetry, etc.  It recognises that code generation in the wild is rarely a pure reasoning problem; *context assimilation* is equally critical.

### 3.3  Key Design Choices & Novel Contributions
1. **CoC diversity optimiser**: Inspired by Auto-CoT, we sample candidate contexts by maximising *pairwise dissimilarity* in structural & lexical space while keeping high sub-goal similarity, using Determinantal Point Processes (DPPs).  
2. **Adapter fusion** for multilinguality: Fine-tune lightweight adapters per language using MultiPL-E, then fuse with parameter-efficient FiLM layers during decoding.  
3. **Safety-critical interaction mode**: When the project’s `critical = true` flag is set (e.g., medical device firmware), the generator must pass additional PVSio-web model checks before suggesting code; the user is alerted if proof obligations fail.  
4. **Cross-task meta-training**: Using CrossCodeBench, we alternate tasks each batch, encouraging representations that transfer among generation, summarisation, and translation.

## 4  Experimental Protocols
### 4.1  Quantitative Benchmarks
• **Static offline**: HumanEval, MBPP, and MultiPL-E (*pass@k*, compilation rate).  
• **Cross-task**: CrossCodeBench *Generalisation score* (G-score).  
• **API-Aware**: API-Bench completion F1.  
• **TDD**: LLM4TDD *iteration reduction* (Δ iterations to green tests).

### 4.2  Interactive, Human-in-the-Loop Metrics
Using the UMARA-instrumented VS Code plugin we collect:  
1. **Task Completion Time (TCT)**: wall-clock to merge PR.  
2. **Intervention Count (IC)**: manual edits per generated LOC.  
3. **Exploration Depth (ED)**: max chain length of back-and-forth revisions.  
4. **Subjective NASA-TLX & SUS**: fatigue and usability.  
5. **Safety Coverage (SC)**: proportion of model-induced errors caught before merge (leveraging formal IDE work, learning L7).

### 4.3  Baselines
• GPT-4-Turbo (direct generation, no planning).  
• Self-Planning Code Generation (SP-Code, 2023).  
• Contextor (bidirectional decoding without planning).  
• Single-turn Codex.  
Ablations: (i) CoC diversity off; (ii) planner off; (iii) critique agent off.

### 4.4  Statistical Analysis
Mixed-effects models treat *participant* as random effect and *system variant* as fixed; Holm-Bonferroni controls family-wise error across 20+ metrics.  Use 95 % CIs; report Cliff’s Δ for non-normal metrics.

## 5  Implementation Plan
### 5.1  Data Pipeline
1. Ingest raw datasets (CrossCodeBench, MultiPL-E, etc.)  
2. Normalise to a shared JSON schema (task, prompt, ground-truth, meta).  
3. Index artefacts into FAISS & AST-SSD *dual* vector stores to serve CoC retrieval.  
4. Collect new *Interactive CoC Traces* (ICT-25K) via internal dog-fooding sprints.  Store diff-n-test sequences at each keystroke.

### 5.2  Model Training
• Base LM: 7-B parameter code-optimised Transformer (open-sourced) or GPT-4 via API for pilot phase.  
• Stage A: Unsupervised SPT-Code tasks for 10 epochs on The Pile-of-Code.  
• Stage B: Cross-task meta-fine-tuning (CrossCodeBench, ThoughtSource, API-Bench).  
• Stage C: RLHF with interaction logs; reward function = weighted sum of TCT ↓, IC ↓, SC ↑.

### 5.3  IDE Extension
A VS Code plugin exposes CoC visualisation (graph of retrieved artefacts), step plan sidebar, one-click rerank.  Telemetry respects GDPR; opt-in study consent.

## 6  Risk Analysis & Mitigations
1. **Context leakage → hallucinated code**.  *Mitigation*: AST sketch regularisation and retrieval gating (confidence > τ).  
2. **Latency overhead** from retrieval + bidirectional decoding.  *Mitigation*: cache CoC vectors; async plan computation.  
3. **Evaluation fatigue** in human studies.  *Mitigation*: micro-tasks ≤ 20 min; monetary bonus tied to code quality, not speed.  
4. **Bias in dataset selection** (over-representation of Python).  *Mitigation*: strict stratified sampling from MultiPL-E.

## 7  Expected Contributions
1. Formal definition and open dataset of **Chain-of-Context traces** for code generation.  
2. Architectural blueprint combining self-planning + CoC + bidirectional decoding.  
3. Empirical evidence of improved cross-task generalisation and interactive usability.  
4. Public VS Code plugin and UMARA-compatible telemetry layer.  
5. Holistic evaluation framework mapping to ISO/IEC 25010 attributes.

## 8  Speculative Extensions (Flagged 🔮)
🔮 *Neural‐symbolic planner*: replace LLM planner with SAT-guided search over API preconditions.

🔮 *Self-healing datasets*: failed CoC retrievals feed back into index, creating a closed-loop memory akin to vector KV-cache at project scope.

🔮 *On-device diffusion LLM for UI code*: generate HTML/CSS screenshots conditioned on CoC for instant UI previews.

## 9  Timeline & Milestones (12 months)
1–2 m  Dataset normalisation & CoC index  
3–4 m  Prototype retriever + planner; offline benchmarks  
5–6 m  Interactive plugin α release; small-N user study  
7–9 m  RLHF & multilingual expansion; large-N study  
10–12 m  Paper submission (ICSE 26) & open-source release

## 10  Conclusion
By marrying the structured decomposition of **Self-Planning** with a rich, diversity-controlled **Chain-of-Context** substrate, we target a step-change in *interactive* NL-to-code tooling.  Leveraging cross-task meta-training, formal usability instrumentation, and multilingual adapters, the project promises not only higher offline accuracy but demonstrable productivity gains in real IDE workflows.


## Sources

- https://zenodo.org/record/8254171
- http://arxiv.org/abs/2210.01240
- https://doaj.org/article/cfd6089d4104413787e743dddb10d8e7
- http://www.coli.uni-saarland.de/~koller/papers/experiences-08.pdf
- https://zenodo.org/record/8199390
- http://arxiv.org/abs/2210.03493
- http://hdl.handle.net/1773/45166
- http://arxiv.org/abs/2309.15402
- http://www.e-informatyka.pl/index.php/einformatica/volumes/volume-2009/issue-1/article-5/
- http://hdl.handle.net/10.6084/m9.figshare.24768660.v1
- http://arxiv.org/abs/2311.09214
- http://hdl.handle.net/10.26180/5ce3c9e5e0625
- http://arxiv.org/abs/2303.06689
- https://zenodo.org/record/4736810
- http://arxiv.org/abs/2201.01549
- https://zenodo.org/record/7220521
- https://escholarship.org/uc/item/3qq6w5kx
- https://zenodo.org/record/7321934
- http://www.cs.toronto.edu/%7Ecmaddis/pubs/nsc.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-177136
- https://eprints.bbk.ac.uk/id/eprint/55303/1/jss24.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-6622357234668258372
- http://hdl.handle.net/10.6084/m9.figshare.7804127.v1
- http://arxiv.org/abs/2201.11903
- http://hdl.handle.net/11311/734566
- https://drops.dagstuhl.de/opus/volltexte/2021/14233/
- http://arxiv.org/abs/2311.09193
- http://hdl.handle.net/10536/DRO/DU:30164722
- https://zenodo.org/record/8199538
- https://inria.hal.science/hal-04099649/document
- https://zenodo.org/record/5704197
- https://hal.archives-ouvertes.fr/hal-03663642/file/Testing%20Interactive%20Software.pdf
- http://eprints.cs.vt.edu/archive/00000207/
- https://hal.archives-ouvertes.fr/hal-01757338
- http://hdl.handle.net/11250/137364
- https://hal.archives-ouvertes.fr/hal-03612380
- http://hdl.handle.net/11390/870050
- http://arxiv.org/abs/2208.08227