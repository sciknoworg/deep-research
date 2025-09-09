# Improving Code Models through Multi-Agent Debate

_Integrating self-play, argumentation theory, and static-analysis feedback to push functional correctness, security, and explainability of code-generation LLMs_

Date: 2025-09-04

## 1  Context and Motivation

Large language models (LLMs) for code (e.g., GPT-4o, Code Llama-70B, DeepSeek-Coder-33B) exhibit growing pass@k, yet still ship:

* logically wrong but syntactically valid programs,
* latent vulnerabilities (e.g., CWE-78, CWE-120) that unit tests rarely expose, and
* opaque reasoning traces that prevent rapid human review.

Multi-agent debate—letting two or more specialized agents critique, defend, and refine a candidate solution—has emerged as a promising lever to close these gaps. The approach generalizes DeepMind’s „self-consistent proofs“ for mathematics and the OpenAI „critic–coder“ chain to the code domain.

The goal of this report is to synthesize current evidence, map it onto code-specific requirements, and lay out a concrete research & engineering roadmap.

---

## 2  Key Learnings from Existing Literature

| # | Finding | Relevance to Debate for Code |
|---|---------|-----------------------------|
| L1 | **Self-play RL works beyond discrete actions:** kernel-regression search beat SOTA in digital curling. | Suggests we can treat „patch tokens“ or „tool-invocation parameters“ as continuous and still optimize via self-play. |
| L2 | **Sweetwater GC framework** (≈2007) provides repeatable metrics for computational-dialectic quality. | Supplies an evaluation harness and metrics (e.g., coherence, convergence) that can be reused for code-focused debate. |
| L3 | **Offline policy + self-supervised practice** lets robots set their own goals. | Analogous: code agents can propose self-tests or adversarial inputs to expose bugs. |
| L4/L6 | **CORE proposer–ranker** resolves >59 % of static-analysis findings with two LLMs. | Validates dual-role architectures; ranker cuts false positives—parallel to „judge“ in debate. |
| L5 | **Coevolutionary self-play stabilizes Rainbow-DQN** in Connect-Four. | Argues for population-based training of debating agents to avoid mode-collapse. |
| L7 | **Extended Dung argumentation** separates individual vs. collective acceptability via trust graphs. | Provides formal semantics for multi-agent code review; can model reliability of each agent. |
| L8 | **AAAI-19 communicating encoder-decoders** improved captioning via iterative voting. | Shows that token-level debate improves generative quality—directly portable to code. |
| L9 | **ASTxplainer** maps logits to AST nodes for explainability benchmarking. | Enables fine-grained tracking of which sub-tree each agent contests. |
| L10 | **Systematic review shows gap** between academic static-analysis research and industrial adoption. | Debate pipeline must integrate seamlessly with CI/CD to avoid same pitfall. |
| L11 | **SALLM security benchmark** replaces pass@k with vuln-centric metrics. | Provides domain-specific „judge“ signals for security-oriented debates. |
| L12 | **LLVM/Clang-plugin rules** can be authored quickly. | We can generate custom static rules „on the fly“ as debate topics. |

---

## 3  Dimensions of Improvement

1. **Functional correctness** – passing reference unit tests, but also self-generated stresses.
2. **Security & safety** – absence of common CWEs; sandbox fuzz runs.
3. **Efficiency** – asymptotic complexity and micro-benchmarks.
4. **Style & maintainability** – PEP-8 / Google Java Format; cyclomatic complexity.
5. **Explainability & traceability** – human-legible argument graph + ASTxplainer heat-map.

We will prioritize (1)–(3) because they most benefit from adversarial critique. Style can be tacked on with low marginal cost via lint checks.

---

## 4  Architectural Proposal

### 4.1  Roles and Responsibilities

1. **Proposer Agents (P₁…Pₙ)** – generate candidate patches or entire solutions.
2. **Critic Agents (C₁…Cₘ)** – perform targeted attacks: static-analysis, fuzz inputs, proof-obligation checks.
3. **Moderator / Judge (J)** – aggregates arguments using extended Dung semantics + trust weights updated via Elo-like rating.
4. **Meta-Planner (MP)** – decides when to spawn additional agents, adjusts budgets, and selects final answer.

![architecture](https://fake-uri/arch.svg)

### 4.2  Interaction Protocol (Inference-Time)

```
Step 0: Task T (prompt, spec) enters.
Step 1: P₁ drafts code C⁰.
Step 2: For k = 1…K debate rounds:
    2a. Each Critic Ci produces critique Δi,k = {bug, vuln, inefficiency,…}.
    2b. Judge ranks critiques → Score_i,k; updates trust.
    2c. Proposers patch C^{k} → C^{k+1} addressing top-scored issues.
Step 3: Final C^{K} emitted + argument log.
```

### 4.3  Training-Time Self-Play Loop

Instead of purely inference-time, we embed the above inside RLHF / RLAIF:

* **Reward** = weighted blend of (unit-test pass rate, SALLM security score, Judge coherence score, efficiency delta).
* **Population-based training (PBT):** Coevolve multiple proposer/critic pairs; periodically swap weights / hyperparams as in L5.
* **Curriculum:** Start with toy k-atas, gradually increase to real-world GitHub issues.

---

## 5  Evaluation Design

### 5.1  Benchmarks

* **HumanEval+** (functional correctness)
* **SALLM** (security)
* **Megahit-Efficiency** (synthetic big-O tasks, 2024 dataset)
* **ASTxplainer** (explainability delta compared to baseline)

### 5.2  Metrics

1. pass@k (k≤10) & pass@budget (seconds)
2. vuln@k (fraction of completions free of CWE hits)
3. _Debate Convergence_ – #rounds until score stabilizes ≤ ε
4. _Argument Coverage_ – % AST nodes touched by critiques (proxy for thoroughness)

### 5.3  Ablation Grid

| Factor | Values |
|--------|--------|
| #Proposers | 1,2,4 |
| #Critics | 0,1,2,4 |
| Judge Mode | rule-based, LLM, graph-based (Dung+) |
| Training | zero-shot, RLHF only, RLHF+PBT |
| Static-analysis tools | None, Bandit, Semgrep, LLVM-plugin |

---

## 6  Implementation Notes

### 6.1  Model Footprints and Budget

* Base models: 7B-33B parameter open-weights (DeepSeek-Coder) fine-tuned via LoRA to keep memory ≤48 GB/ GPU.
* Debate at inference time adds ~1.8× token cost per round. With K=3, expect 5.4× baseline; batch decode with speculative sampling to stay within 60 s latency for <300-line tasks.

### 6.2  Toolchain Integration

* **Unit tests** – PyTest harness auto-generated if absent; cached Docker images.
* **Static analyzers** – Bandit, Semgrep; dynamic load of LLVM rules (L12) compiled on the fly.
* **Sandbox** – gVisor for untrusted code; coverage-guided fuzzing via Python-Atheris.

### 6.3  Data

* 140 k Github issues w/ accepted PRs (MIT-licensed) → instruction-response pairs.
* Augment with synthetic vuln seeds from SALLM.

### 6.4  Trust Graph Initialization

* Begin with uniform weights; update after each task: agent’s trust += α·(is_correct − expected).
* Decay towards mean to prevent „tyrant“ domination.

---

## 7  Contrarian & Speculative Extensions  ⚠️

1. **Continuous-Action Debate** (L1): Treat the diff-embedding space as continuous and run gradient-guided search between Critic and Proposer—a hybrid of code gradient descent (compare AlphaCode2 „edit tree“).
2. **On-device Micro-benchmarks**: Critics gather runtime profiles (e.g., perf counters) to argue „your patch regresses cache misses by 30 %“.
3. **Reflexive Trust**: Let agents negotiate their own trust scores, akin to „social calibration“ models—speculative, risk of collusion.
4. **Adversarial Code-Style Attacks**: An agent purposely proposes style-compliant but insecure code to test Judge robustness.
5. **Explainable Debates via ASTxplainer**: Visual panel shows node-level heat-maps per argument; might increase reviewer adoption (untested).

---

## 8  Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Token-cost Explosion | Latency & $$ | adaptive early-exit when Judge variance < τ. |
| Collusion between agents | Wrong code accepted | randomized role assignment every session; differential trust decay. |
| Static analyzer false positives (L10) hamper debate | wasted cycles | weight critic evidence by historical precision (à la CORE). |
| Security eval sandbox escapes | CI pipeline breach | gVisor + firecracker VMs; time/memory caps. |

---

## 9  Roadmap (T0 = project start)

| Phase | Duration | Milestones |
|-------|----------|-----------|
| P0 – Prototype | 6 weeks | single Proposer + Critic + rule-based Judge on HumanEval; measure convergence. |
| P1 – Integration | 8 weeks | add SALLM harness, LLVM plugin generation; begin RLHF fine-tune. |
| P2 – Population | 10 weeks | coevolution training, trust-graph judge, Sweetwater metrics. |
| P3 – Productization | 12 weeks | CI plugin, VSCode extension w/ debate visualization; user study. |

Total ≈ 36 weeks to beta.

---

## 10  Recommendations

1. **Start narrow**: Python & Java—rich analyzer ecosystem + match CORE stats; defer C/C++ until sandbox story is solid.
2. **Invest in Judge Quality**: Empirically LLM-judges outperform static heuristics; fine-tune a 13B „debate-evaluator“ on argument/outcome pairs.
3. **Leverage Cheap Critics**: Static analyzers/fuzzers cost CPU not GPU; run them massively in parallel.
4. **Publish Intermediate Artifacts**: Argument graphs + code patches form a novel dataset valuable to research community, creating a positive feedback loop.
5. **Align Incentives**: Reward agents not only for being right but for being persuasive yet truthful—use soft-truth metrics from epistemic-trust extensions (L7).

---

## 11  Conclusion

The synthesis of self-play reinforcement learning, computational argumentation, and modern static-analysis tooling provides a realistic path to **substantially improve functional correctness, security, and explainability** of code-generation LLMs. Multi-agent debate is not a silver bullet, but the evidence (L1–L12) indicates that a carefully engineered pipeline can yield step-change gains while remaining cost-effective and integrable into existing developer workflows.

Investing in the outlined roadmap positions us to deliver the first „trustworthy-by-design“ code LLM—a key differentiator in an increasingly crowded market.


## Sources

- http://arxiv.org/abs/2310.12357
- https://hal.inria.fr/hal-03159815
- https://tel.archives-ouvertes.fr/tel-01345797
- http://arxiv.org/abs/2309.12938
- http://hdl.handle.net/11379/157480
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.431.1633
- http://arxiv.org/abs/2308.13062
- https://hal.science/hal-03348492
- http://hdl.handle.net/2117/121655
- http://hdl.handle.net/1721.1/103745
- http://lia.deis.unibo.it/Staff/PaoloTorroni/Publications/climaVIIIb.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-12871
- https://researchbank.rmit.edu.au/view/rmit:2550
- http://www.scopus.com/inward/record.url?scp=24144432342&partnerID=8YFLogxK
- http://hdl.handle.net/10453/157968
- https://scholar.smu.edu/datasciencereview/vol5/iss2/12
- http://paginas.fe.up.pt/%7Eei05021/TQSO%20-%20An%20overview%20on%20the%20Static%20Code%20Analysis%20approach%20in%20Software%20Development.pdf
- http://cds.cern.ch/record/2305318
- http://hdl.handle.net/10.36227/techrxiv.24708198.v1
- http://arxiv.org/abs/2311.00889
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-128625
- http://scholarworks.csun.edu//handle/10211.2/286
- https://ojs.aaai.org/index.php/AAAI/article/view/4566
- https://escholarship.org/uc/item/99w7d1hz
- http://hdl.handle.net/10251/11034
- https://repository.vu.lt/VU:ELABAETD23254963&prefLang=en_US
- https://zenodo.org/record/7898305
- http://hdl.handle.net/10831/77109
- https://scholarworks.unist.ac.kr/handle/201301/32723
- http://handle.westernsydney.edu.au:8081/1959.7/uws:51781
- http://hdl.handle.net/1911/96396
- http://arxiv.org/abs/2308.03873
- https://basepub.dauphine.fr/handle/123456789/3704
- http://www.scopus.com/inward/record.url?scp=33644798424&partnerID=8YFLogxK
- https://orbilu.uni.lu/handle/10993/54191
- http://hdl.handle.net/11383/2101537
- http://leenissen.dk/rl/Steffen_Nissen_Thesis2007_Print.pdf