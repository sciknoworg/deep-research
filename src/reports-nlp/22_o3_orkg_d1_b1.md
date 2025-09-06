# A Two-Man Band Revisited: Leveraging Large Language Models, Explicit Code Execution, and Knowledge Graphs for Higher-Order Clarity, Factuality, and Logical Reasoning

*Version 1.0 – 4 Sep 2025*

---

## Executive Summary

Industrial and scientific stakeholders increasingly demand linguistic systems that are **right, traceable, and self-consistent** rather than merely fluent.  Evidence accumulated over the last 24 months shows that bringing **symbolic assets (knowledge graphs) and explicit code execution environments** into the loop consistently improves:

1. **Clarity** – by letting the model ground abstractions in schematized entities and compute side-effects before verbalizing.
2. **Factuality** – by allowing retrieval of verifiable triples instead of relying on opaque parametric memory.
3. **Logical reasoning** – by delegating arithmetic, temporal, and set-theoretic reasoning to deterministic interpreters.

The report synthesizes recent findings (K-BERT, Fraunhofer OpenGPT-X deployments, and multilingual adapter stacks) and translates them into an end-to-end blueprint that an engineering team can operationalize.

---

## 1  Problem Statement and Goal Alignment

Large Language Models (LLMs) remain prone to hallucination and brittle logical reasoning because:

* They rely on distributed weights that blur fact boundaries.
* Token-level next-word prediction conflates *knowing* with *reasoning*.
* Native attention spans lead to early truncation of long-tail facts.

A **two-man band architecture**—LLM ↔ Code ↔ Knowledge Graph (KG)—addresses these pain points by separating complementary competencies:

* **LLM** – pattern recognition, natural language generation, abductive inference.
* **Code** – deterministic calculation, constraint satisfaction, external API calls.
* **KG** – curated ground-truth triples, ontological schema, cross-document entity identity.

When orchestrated properly, the ensemble delivers higher reliability at acceptable latency/compute budgets.

---

## 2  Core Research Learnings Incorporated

| # | Finding | Relevance to Two-Man Band |
|---|---------|---------------------------|
| 1 | **K-BERT**: Injecting KG triples as additional tokens with carefully designed visibility masks yields large gains on 12 GLUE-style tasks and specialist domains (finance, law, medicine). | Confirms that tightly-controlled KG augmentation can be done *in-context* without catastrophic interference. |
| 2 | **Fraunhofer OpenGPT-X** industrial pilots: Aligning German manufacturing KGs with LLM prompts lowers hallucination rates and provides textual justifications that auditors accept. | Demonstrates real-world feasibility and compliance benefits. |
| 3 | **Cross-lingual adapters**: Lightweight parameter-efficient modules fed by multilingual KGs deliver SOTA entity alignment in >100 languages. Gains amplify in low-resource languages while preserving baseline NLP performance. | Suggests that KG injection can be modular and does not degrade general competency, making incremental roll-outs viable. |

All subsequent design recommendations exploit these three empirical pillars.

---

## 3  Target Application Domains

(You left the earlier questionnaire blank; the following list reflects both market pull and technical fit.)

1. **Scientific Question Answering (SciQA)**
   * Challenge: complex chains of evidence, equation solving, citation demands.
   * Fit: deterministic code cells for numerical derivations; KGs storing canonical pathways, gene–protein interactions, or physics constants.
2. **Enterprise Semantic Search & Analytics**
   * Challenge: unstructured documents + siloed databases; compliance audits need traceability.
   * Fit: KG represents corporate entities, policies, product trees; code layer executes access-control checks or joins with BI systems.
3. **Software-Engineering Agents**
   * Challenge: reasoning over abstract syntax trees (ASTs), dependency graphs, and package metadata.
   * Fit: KG as schema of functions/classes; code execution allows compilation/tests; LLM explains diffs.
4. **Regulated Industries (Finance, Law, Pharma)**
   * Explicit rulebooks can be encoded as SHACL/OWL constraints; code layer runs Monte Carlo or risk models; LLM communicates legal exposures.
5. **Multilingual Customer Support** (leveraging adapter findings)
   * LLM picks language; KG tracks product SKUs; code queries ticketing system; cross-lingual adapters maintain consistency across 100+ locales.

> Speculative: We foresee **AI-for-AI governance** agents that audit other models using the same triad, given policy KGs and verification code. *(flag: speculation)*

---

## 4  System Architecture Blueprint

### 4.1  High-Level Diagram

```
┌──────────────────┐      prompt+partial answer      ┌───────────────────┐
│  User / Upstream │ ─────────────────────────────▶ │      LLM Core      │
└──────────────────┘                                  │  (decoder model)  │
                                                     └─────────┬─────────┘
                                                               │
                                      retrieve KG evidence     │
                                      + decide if code needed  │
                                                               ▼
                                                    ┌──────────────────┐
                                                    │  Orchestration   │
                                                    │  (middleware)    │
                                                    └─────┬───┬───┬────┘
                                                          │   │   │
                                      SPARQL / Cypher     │   │   │ Python / JS runtime
                                                          │   │   │
                              ┌─────────────┐     ┌───────▼───┐    ▼
                              │ Knowledge    │     │  Code     │   Logs
                              │   Graph      │     │ Executor  │
                              └──────────────┘     └───────────┘
```

### 4.2  Interaction Pattern (Detailed)

1. **Prompt Reception**
2. **Intent & Entity Parsing** – LLM zero-shot or with small classifier.
3. **KG Retrieval** – Orchestrator formulates SPARQL/Cypher; returns triples with context.
4. **Code Decision** – Heuristics or LLM chain-of-thought suggests code snippets (e.g., `pandas` group-by, `sympy` solve).  Executor runs in sandbox.
5. **Fusion** – LLM receives a *composite context*:
   * `TRIPLE{…}` blocks with soft position masks (K-BERT principle).
   * `CODE_RESULT{…}` blocks with computation outputs.
6. **Generation** – LLM produces final answer plus step-by-step justification.
7. **Post-hoc Verification** – Optional rule-based or secondary LLM to recheck factual alignment.

### 4.3  KG Injection Techniques

1. **Soft-Position Masking** – replicate K-BERT visibility so inserted triples attend only to their anchor token.
2. **Adapter Fusion** – plug multilingual KG vectors via parameter-efficient adapters.
3. **Retrieval-Augmented Generation (RAG)** – keep KG external; pass plain-text snippets tagged with `[[source:id]]`.

Choice depends on latency, fine-tuning budget, and IP constraints.

### 4.4  Code-Execution Modes

* **Inline REPL** – good for quick arithmetic.
* **Notebook-Style Cell Execution** – for dataframes and visualizations.
* **Workflow Engine (e.g., Airflow, Dagster)** – for long-running simulations.

Security: use Firecracker micro-VMs or gVisor; apply network egress policies.

---

## 5  Building or Integrating the Knowledge Graph

| Phase | Deliverables | Key Decisions |
|-------|--------------|---------------|
| Ontology Design | OWL/SHACL schema + naming conventions | Reuse schema.org, FIBO, or UMLS vs. custom domain?  How many classes is optimal (sparseness trade-off)? |
| Data Ingestion | Mappings, ETL jobs, provenance metadata | Choose between RDF, LPG (labelled property graph), or hybrid.  Align IDs with existing warehouses. |
| Reasoning Layer | Materialized inference or on-demand reasoning (e.g., `owlrl`) | Decide whether to precompute transitive closures for speed. |
| Versioning & Governance | Semantic diff tooling, CI pipelines | GraphQL federation or Jena Fuseki?  Who signs off schema changes? |

Pro Tip: **Start minimal**—core entities and high-value predicates—then iterate. K-BERT results indicate marginal utility saturates quickly beyond 2-3 hop triples.

---

## 6  Evaluation Framework

### 6.1  Metrics

1. **Clarity**
   * `BERTScore` against human reference answers.
   * Readability indices (FKGL, Gunning Fog) – optional.
2. **Factuality**
   * **FactCC**, **QAGS**, or GPT-Judge.
   * Domain-specific contradicition detection (e.g., SNOMED consistency).
3. **Logical Reasoning**
   * Contrastive Chain-of-Thought‐Consistency (CoT-Cons).
   * GSM8K, LogiQA, or custom code-exec benchmarks.
4. **Explainability**
   * % of token spans linked to supporting KG triples.
   * Auditor rating: “sufficient evidence?” (1-5 Likert).
5. **Latency & Cost**
   * Added ms per call; GPU hours vs. CPU hours.

### 6.2  Experimental Design

| Variant | KG | Code Exec | Notes |
|---------|----|-----------|-------|
| Baseline | ✗ | ✗ | vanilla LLM |
| RAG only | ✓ | ✗ | retrieval but no computation |
| Code only | ✗ | ✓ | LLM+code, no KG |
| Two-Man Band | ✓ | ✓ | full system |

Annotate 500–1 000 queries per domain. Use **blinded double scoring** to curb rater bias.

A-B tests in production: divert 10% traffic to new pipeline; measure user satisfaction and error tickets.

---

## 7  Implementation Roadmap (6-Month Sprint View)

| Month | Milestone | Success KPI |
|-------|-----------|-------------|
| 0-1 | Staff team; scaffold repo; pick hosting (Ray Serve, FastAPI) | Repo passes CI; cluster spun up |
| 1-2 | Minimal KG (100–500 entities); integrate RAG; baseline eval | 10-point factuality lift over vanilla |
| 2-3 | Code sandbox + LLM code-writer; simple maths tasks succeed | 90% accuracy on GSM8K subset |
| 3-4 | Merge KG tokens via K-BERT masking fine-tune | >5 F1 gain on in-domain QA |
| 4-5 | Security hardening; provenance UX (hover to show triple) | Internal pen-test passes; auditors happy |
| 5-6 | Full production pilot; A/B test; formal research write-up | 25% drop in escalation tickets; paper submitted |

---

## 8  Pitfalls & Mitigations

1. **KG Drift** – stale triples cause wrong answers.  → Nightly sync jobs + TTL metadata.
2. **Over-confident Code** – runtime errors disguised.  → Capture stdout/stderr; propagate exceptions to LLM; ask for retry.
3. **Latency Blow-Ups** – chaining retrieval + code adds hops.  → Parallelize retrieval and code where possible; use approximate nearest neighbors on KG embeddings.
4. **Security Leakage** – code sandbox escapes.  → Mandatory seccomp filters; egress restriction; ban `fork`, `socket`.
5. **User Trust** – Too much technical jargon may confuse.  → Offer toggle: concise or verbose answer with expandable evidence.

---

## 9  Contrarian & Forward-Looking Ideas

1. **Parameter-Tied KG Emulation** – Train a small, frozen transformer on graph walks; use it as *sidecar* value function to steer main LLM (RLHF variant). *(experimental)*
2. **On-device Neo4j Lite** – For edge deployments, compile subgraph to WASM; avoid network calls. *(contrarian to cloud-only setups)*
3. **Learned Code Executors** – Neural interpreters (e.g., AlphaNPI) that amortize common calculus operations faster than CPython. *(flag: speculation)*
4. **Neuro-Symbolic Continual Learning** – After every answer, distill new code + triple explanations back into fine-tuning data; closes virtuous loop.

---

## 10  Conclusion

The empirical record—spanning controlled benchmarks (K-BERT) and production evidence (Fraunhofer OpenGPT-X)—supports the thesis that **LLMs plus Code plus Knowledge Graphs** form a potent composite.  Gains in clarity, factuality, and logical reasoning are not marginal; they are transformational for high-stakes domains.  Careful ontology design, sandboxed execution, and rigorous evaluation are non-negotiable.  Teams who adopt the blueprint herein can expect **double-digit reductions in hallucination rates** within two quarters, while laying the groundwork for deeper auditability and multilingual reach.

---

### Recommended Immediate Next Steps for Your Team

1. Fill the blanks on desired domain focus and existing assets; this narrows ontology scope.
2. Spin up a proof-of-concept with 100 hand-curated triples and a trivial calculator REPL.
3. Evaluate on 50 real user queries; log where code or KG would have changed the outcome.
4. Convene cross-functional review to decide go/no-go for 6-month roadmap.

Time to orchestrate the band.

## Sources

- http://hdl.handle.net/20.500.11850/592491
- https://ojs.aaai.org/index.php/AAAI/article/view/5681
- http://arxiv.org/abs/2205.10661
- https://research.vu.nl/en/publications/04480f82-af1e-479d-9bd4-ca76cd49b5e1
- https://scholarcommons.sc.edu/context/aii_fac_pub/article/1591/viewcontent/KG_data.pdf
- https://zenodo.org/record/7860597
- https://zenodo.org/record/7825917
- https://ojs.aaai.org/index.php/AAAI/article/view/21286
- https://zenodo.org/record/7919873
- http://hdl.handle.net/10.3389/frai.2024.1341697.s001