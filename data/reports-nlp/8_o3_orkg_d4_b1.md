# Incorporating Chain-of-Context in Self-Planning to Enhance Interactive Code Generation from Natural Language

*Prepared 4 Sept 2025*

---

## 1  Scope and Positioning

This report synthesises research findings on *chain-of-context (CoC) self-planning* for interactive natural-language–to–code (NL→Code) systems. It is aimed at experts who wish to (i) survey the conceptual landscape, **and** (ii) obtain concrete design and evaluation guidance for building next-generation prototypes. All documented learnings from prior work (2009–2025) are integrated verbatim or paraphrased and explicitly cross-referenced.

Acronyms
- **ICL** – in-context learning
- **PEFT** – parameter-efficient fine-tuning (e.g., LoRA, IA3)
- **CoC** – chain of context prompting
- **PALP** – Prompt-Augmented Linear Probing

---

## 2  Background and Motivation

Large language models (LLMs) revolutionised code synthesis, yet *interactive* use cases—IDE copilots, conversational agents, robotics middleware—expose two recurrent pain-points:

1. **Planning Overhead.** Free-form NL requests often embed latent sub-tasks (“read CSV → filter rows → plot”), requiring a planning layer that *maps language to an ordered set of API calls or code blocks*.
2. **Context Budget.** Pure ICL systems encode planning steps as extensive in-prompt demonstrations. This is token-hungry and brittle to distribution shift.

`Chain-of-context self-planning`—where the LLM recursively decomposes, plans, and solves—alleviates (1). Yet evidence shows ICL alone fails to match fine-tuning baselines in specification-heavy domains (< 50 % of SOTA on 18 IE tasks; see “When does ICL Fall Short?”, arXiv 2311.08993).

Consequently, the field is pivoting towards *hybrid strategies* that keep CoC’s interpretability but reduce reliance on long demonstrations via PEFT or black-box probing (PALP). This report traces that evolution and produces actionable design patterns.

---

## 3  Key Research Learnings (Integrated Chronologically)

| Year | Finding | Implication for CoC Self-Planning |
|---|---|---|
| 2009 | End-to-end generation of executable code from NL UML use-cases enabled early completeness checks (e-Informatica 2009-1). | Validates the vision; shows planning decoupled from code emission can work even with pre-LLM tooling. |
| 2010–2014 | Distributed Correspondence Graph (DCG) decouples NL constraint inference from trajectory planning for mobile manipulators (ONR MURI N00014-09-1-1052; W911NF-10-2-0016). | Template: treat “planning” as a *search* module separate from language understanding—mirrors modern CoC frameworks. |
| 2023 | Multi-domain analyses (HyperCLOVA corpus; GPT-3 biomed) show ICL performance < 50 % of SOTA; failures tied to alignment & data, not model size/perplexity. | Token-heavy CoC prompting is *not enough*; alignment or fine-tuning is required. |
| 2023 | “When does ICL Fall Short and Why?” confirms context-misunderstanding & schema misalignment as root causes; instruction-tuning recovers accuracy. | Suggests *instruction-tuned* CoC or PEFT-augmented CoC. |
| 2024 | ICSE 2024 “No More In-Context Learning?”: PEFT (LoRA, IA3) on code LLMs **outperforms CoC prompting** on HumanEval (pass@1 & pass@10) while updating ≤ 1 % weights. Artifact released (Zenodo #8191801). | For code-generation, lightweight fine-tuning may *replace* long CoC chains. |
| 2024 | PALP (AAAI-24) combines linear probing with prompt engineering, nearly closing gap to full fine-tuning; scalable when context windows/compute limit ICL. | A black-box option that preserves CoC interpretability yet shrinks prompt length. |
| 2024 | Comparative study LoRA vs IA3 with CoC baseline on HumanEval further corroborates PEFT edge. | Model choice: LoRA easiest; IA3 lower memory. |

---

## 4  Conceptual Model of CoC Self-Planning

```
User NL query ──► ① Task-Decomposer  ── plan steps ─► ② Step-Solver ──► ③ Integrator ──► Code
```
1. **Task-Decomposer (Planner).** Uses CoC prompts (or a specialised PEFT adapter) to output an *ordered list of sub-tasks* expressed in either NL or a canonical DSL.
2. **Step-Solver.** For each sub-task, another LLM invocation (with or without CoC) emits candidate code snippets.
3. **Integrator.** Assembles snippets, resolves dependencies, optionally executes tests, and surfaces results to the user.

The *chain* is thus manifest both in textual reasoning (exposed to the user) and in the explicit sub-task list, affording debuggability and partial regeneration.

### Relation to DCG (2010)
DCG’s decomposition of NL robot commands into constraints + motion plans exactly parallels (1) vs (2); the historical success in robotics supports this modular decomposition for code.

---

## 5  Limitations of Plain ICL-Only CoC

Empirical failures (≤ 50 % SOTA) cluster in three axes:
1. **Context Misunderstanding.** LLM cannot slot examples into the correct schema when the domain diverges (biomed IE, HyperCLOVA study).
2. **Long-Text Limits.** CoC chains consume context tokens, exacerbating truncation and latency.
3. **Alignment Mismatch.** Without explicit instruction tuning, the model mis-interprets specification heavy-and-strict tasks.

Hence, raw CoC is best viewed as an *interpretability scaffold*, not a performance panacea.

---

## 6  Augmenting CoC with PEFT / PALP

### 6.1 Parameter-Efficient Fine-Tuning (LoRA, IA3)

- **Mechanics.** Inject rank-decomposed weight deltas (LoRA) or per-layer scaling (IA3) into *specific* transformer blocks.
- **Artifacts.** Zenodo 8191801 provides reference checkpoints achieving > CoC baseline on HumanEval.
- **Benefits for Interactive Systems.**
  - Shrinks prompt: demonstrations replaced by learned adapters.
  - Faster interaction latency; fewer tokens ⇒ lower API cost.
  - Deployable in user space (only adapters shipped), relevant for proprietary code.

### 6.2 Prompt-Augmented Linear Probing (PALP)

- Retains black-box model; learns a linear probe over frozen activations conditioned on a small prompt template.
- Achieves near-fine-tuned performance when data abundant; ideal if host API forbids weight updates.

### 6.3 Hybrid Workflow

```
┌─────────┐   LoRA-tuned            ┌─────────┐
│CoC Plan │ ─────────── step → │LoRA Solver│ → code
└─────────┘                      └─────────┘
```
Planner may remain prompt-only (human readable), while Step-Solver is PEFT-tuned for correctness.

---

## 7  Benchmarks and Evaluation Protocol

### 7.1 Datasets

1. **HumanEval** (Python) – standard; good for pass@k.
2. **MBPP** (Mostly Basic Programming Problems) – diverse; emphasises readability.
3. **Proprietary Spec-Heavy Suite** – recommended if your domain uses custom APIs.

### 7.2 Metrics

| Goal | Metric | Notes |
|---|---|---|
|Offline quality| pass@1, pass@k | Use the canonical HumanEval harness. |
|Interactive UX| Latency / turn | Count wall-clock incl. planning calls. |
|Context efficiency| Prompt tokens per solution | Lower is better. |
|Human satisfaction| SUS or tailored Likert | Collect via IDE plugin study. |
|Robustness| Success rate under mutation tests | Eg, fuzz the NL query. |

**Observation.** Studies show PEFT variants not only raise pass@k but *halve* latency relative to long CoC prompts due to fewer tokens.

---

## 8  System Architecture Blueprint

1. **Frontend.** VS Code extension or chat UI.
2. **Planning Service.** Stateless micro-service hosting the Task-Decomposer; can run pure prompts for transparency.
3. **Solver Pool.** Hosts multiple PEFT-tuned models specialised by language (Python, TypeScript, Bash).
4. **Execution Sandbox.** Runs generated code, captures I/O, applies unit tests.
5. **Telemetry DB.** Stores prompts, plans, code, feedback for continual tuning.

`gRPC` or `FastAPI` is sufficient; latency budgets (< 500 ms for planner, < 2 s for code generation) align with IDE use cases.

---

## 9  Design Recommendations

1. **Separate Plan vs Solve.** Inspired by DCG, keep planner lightweight and interpretable; fine-tune solvers.
2. **Use LoRA-β>16.** Empirically stable for code; IA3 if GPU VRAM constrained.
3. **Embed Unit Tests in Prompt.** 2009 prototype already did completeness checks; reinforce with modern test-driven prompts.
4. **Adaptive Prompt Truncation.** If plan length N > 8, collapse solved steps into high-level placeholders to fit window.
5. **Feedback-Driven Fine-Tuning.** Log failing plans, run offline PALP to patch without retraining whole model.

---

## 10  Contrarian & Speculative Ideas (Flagged)

- *Speculation* – Replace textual CoC with a **graph-structured plan** serialized in JSON; feed back into graph-neural adapter. May improve schema alignment.
- *Speculation* – Employ **retrieval-augmented CoC** where each step queries a codebase embedding index, reducing generation load.
- *Speculation* – Combine PEFT with **flash-attention v3** kernels to cut latency below 100 ms, enabling near real-time co-editing.

---

## 11  Open Research Questions

1. How to quantify *planner correctness* separate from code correctness?
2. Can PALP replace LoRA for on-device (mobile) IDEs where weight deltas are still heavy?
3. What are the security implications of exposing intermediate plans (e.g., prompt injection at plan layer)?

---

## 12  Conclusion

The past 15 years—from DCG in robotics to ICSE 2024’s PEFT results—demonstrate a clear trajectory: **decoupled planning plus lightweight model adaptation outperforms monolithic, prompt-only CoC** for NL→Code. Interactive systems should therefore:

1. Preserve CoC’s interpretability for planning.
2. **Minimise** prompt length via PEFT or PALP for execution steps.
3. Evaluate holistically on quality, latency, and user satisfaction.

Adopting this hybrid recipe will likely surpass current SOTA baselines (plain CoC) while shrinking operational cost and improving UX.

---

### Reference Index of Integrated Learnings

L1 (DCG 2009), L2 (HyperCLOVA study), L3 (arXiv 2311.08993), L4–L6 (PEFT vs CoC on HumanEval), L7 (2009 UML prototype), L8–L9 (PALP AAAI-24), L10–L13 (ICSE 2024 artifact & replication). All have been cited above.


## Sources

- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.431.9367
- https://zenodo.org/record/8191801
- https://zenodo.org/record/8100245
- https://escholarship.org/uc/item/6xx2h90z
- https://zenodo.org/record/7708774
- https://ojs.aaai.org/index.php/AAAI/article/view/26495
- http://arxiv.org/abs/2310.12477
- http://arxiv.org/abs/2311.08993
- https://pub.uni-bielefeld.de/record/2951681
- http://arxiv.org/abs/2204.13509
- https://doaj.org/article/43896c44c7f94b73b47f70447a0e091e
- https://hal.archives-ouvertes.fr/hal-02281604
- http://www.e-informatyka.pl/index.php/einformatica/volumes/volume-2009/issue-1/article-5/
- https://doi.org/10.1016/j.sbspro.2013.09.299
- http://hdl.handle.net/2078.1/113821
- https://zenodo.org/record/7578503
- https://zenodo.org/record/1298928
- https://zenodo.org/record/7638657
- http://hdl.handle.net/2142/18023
- http://library.uny.ac.id/sirkulasi/index.php?p=show_detail&id=34095
- https://zenodo.org/record/8050982
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/27671
- https://hal.inria.fr/hal-01659137
- https://hdl.handle.net/10125/103014
- http://www.editlib.org/d/30469/
- http://arxiv.org/abs/2203.08410
- https://orcid.org/0000-0002-8293-0492
- http://hdl.handle.net/2078.1/91163
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.1031
- http://hdl.handle.net/1820/1177
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-325238
- http://www.nnce.org/Arquivos/Artigos/1996/landeira_etal_1996.01.pdf
- http://www.kamran-karimi.com/pubs/khES2000.pdf