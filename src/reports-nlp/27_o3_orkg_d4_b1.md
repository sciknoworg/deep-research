# Improving Code Models through Multi-Agent Debate – A Technical Blueprint

*Prepared 2025-09-04*

---

## Table of Contents
1. Executive Summary  
2. Problem Framing & Objectives  
3. Baselines, Constraints and Target Models  
4. Related Results & Theoretical Underpinnings  
5. Debate-Oriented System Architectures  
   * 5.1 Self-Play Debate (Turn-Based)  
   * 5.2 Adversarial Proxy Debate (Simultaneous)  
   * 5.3 “Vote-Revise-Vote” Token-Level Debate  
6. Training & Control Algorithms  
7. Evaluation Suite & Success Metrics  
8. Experimental Road-Map  
9. Anticipated Risks, Failure Modes & Mitigations  
10. Speculative Extensions & Contrarian Ideas  
11. Concluding Recommendations  
12. Appendix – Mapping Literature Learnings to Design Choices

---

## 1. Executive Summary
Large code language models (Code-LLMs) such as GPT-4-Code, CodeLlama and StarCoder achieve high pass-rates on curated benchmarks (e.g., **80 %+ on HumanEval**) yet collapse on industrial-scale testbeds (e.g., **< 2 % on Evosuite SF110**). Empirical evidence and theory both indicate that *single-agent decoding is the bottleneck*: capability cliffs, hallucinations and reasoning lapses emerge once the prompt or task exceeds the depth any single sample can explore.

Multi-agent debate is a promising remedy. By letting multiple model instances argue, critique, and reconcile competing partial solutions, we can **(i)** raise unit-test pass rates, **(ii)** suppress hallucinations through adversarial cross-examination, and **(iii)** externalize the chain-of-thought into an auditable transcript. This report distills the full body of prior research provided, proposes three concrete debate architectures, supplies training algorithms rooted in recent MARL theory, and delineates an experimental plan to validate gains on open-source and closed-source code models within reasonable compute budgets.

Key design levers include:
•  Pairwise ability self-classification to auto-schedule balanced debates.  
•  Two-stage heterogeneous voting to fuse diverse reasoning paths.  
•  Centralized-critic distillation to merge improvements back into a deployable single model.  
•  Evaluation on **both** synthetic and large-scale real test suites to avoid “illusion of competence.”

---

## 2. Problem Framing & Objectives
We operationalize *“improving code models via debate”* as optimizing three orthogonal metrics:
1. **Functional Correctness** – % unit tests passed across HumanEval, MBPP, CodeContests, SF110 and BigCode Bench.
2. **Hallucination Rate** – fraction of generated tokens not grounded in the problem specification, measured by static analyzers + manual adjudication.
3. **Transparency Score** – subjective utility of reasoning trace for a senior developer, rated on a 5-point scale (≥ 4 desired) and estimated with automated rubric classifiers.

Targets (stretch): +15 pp pass rate on SF110, 2× reduction in hallucinations, transparency ≥ 4.

Constraints accepted by stakeholder (if absent we assume default):
•  **Model Family** – start with *CodeLlama 70 B-Instruct* (open weights) for unrestricted modification; replicate on GPT-4-Code via API for external validity.  
•  **Compute** – ≤ 2 M GPU-hours for full project; real-time inference budget ≤ 5× baseline latency allowable for production.

---

## 3. Baselines, Constraints and Target Models
| Category | Baseline | Rationale |
|----------|----------|-----------|
| Decoding | Greedy / temperature 0.2 | industry default, single sample |
| Self-consistency | 5 interleaved samples + majority vote | light-weight ensemble baseline |
| Chain-of-Thought | Reflexion / ReAct prompting | shows gains but still single-agent |
| Peer-Review | Single-reviewer codex critique | limited diversity |
| Ensemble Voting | 5-way majority / logit-averaging | reference vs. debate |

For API-based models we respect usage TOS; critiques encoded in system & user messages only.

---

## 4. Related Results & Theoretical Underpinnings
This section maps each prior learning to debate design decisions (full mapping in Appendix).

1. **Pairwise LoA Self-Classification** – Agents can dynamically estimate their capability and request suitable opponents, avoiding both echo chambers (too weak) and steam-rolling (too strong). Expected to reduce compute by ~30 % relative to random pairing.
2. **Two-Stage Noisy Voting** – Heterogeneous ensembles converge to perfect decisions as size → ∞, while homogeneous ones saturate; thus, diversity (different checkpoints, temperatures, or even model families) is critical.
3. **Policy Distillation + Value Matching** – After debates generate better policies (i.e., solution traces), distillation merges knowledge back into a single deployable model, amortizing inference costs.
4. **Consensus Decentralized Actor-Critic** – Formal guarantee that sharing gradients / Q-values in a fully cooperative game causes no optimality loss; we can therefore train “debating agents” cooperatively without fear of convergence degradation.
5. **Boltzmann-Multiplication (BM) Ensembles** – Weighted multiplicative fusion often outperforms simple majority; we can import BM into token-level ensemble decisions inside debates.
6. **Overcooked Findings** – Centralized critics accelerate learning but do not ensure transfer to new partners; our design must build partner-robustness via explicit randomization and role-shuffling.
7. **Capability Cliffs** – Confirm the need for deeper reasoning iterations; debate is a tool to extend the cliff boundary.
8. **Vote-Revise-Vote in NLG** – Demonstrates practicality of iterative debate inside generation loop; we extend to code.

---

## 5. Debate-Oriented System Architectures
### 5.1 Self-Play Debate (Turn-Based)
•  Two copies of the same base model (possibly at different temperatures) alternate *roles* (“Proposer”, “Skeptic”).  
•  Round 0: Proposer emits an initial solution sketch + unit tests.  
•  Round k (>0): Skeptic runs tests, points out failures, proposes patches; roles swap.  
•  Terminate after *K=4* rounds or when tests pass.  
•  Final answer = last passing code; trace archived.

Advantages: Simplicity, no extra training required initially.  
Pitfalls: Potential collusion (identical weights) ⇒ inject dropout or checkpoint diversity.

### 5.2 Adversarial Proxy Debate (Simultaneous)
•  Use two heterogeneous models (e.g., CodeLlama 70 B vs. StarCoder 16 B, or same model at T=0 vs. T=1).  
•  Both independently propose full solutions + rationale.  
•  A separate “Adjudicator” model (smaller, cost-efficient) applies two-stage noisy voting + static analysis to pick winner.  
•  Pairwise LoA estimator selects opponent mixes adaptively.

### 5.3 “Vote-Revise-Vote” Token-Level Debate
•  Ensemble of *N=5* lightweight copies decode **synchronously**.  
•  At each time-step *t*:  
  1. All agents emit token logits.  
  2. BM fusion produces consensus token cₜ.  
  3. Agents receive consensus, internally rescore; agents with low log-prob(cₜ) inject critiques in a side channel.  
  4. Critiques can trigger roll-back & re-decoding before committing cₜ.  
•  Provides fine-grained control, highest transparency, but demands custom decoding infra.

We recommend a phased rollout: start with 5.1 for quick wins, migrate to 5.2 for robustness, and explore 5.3 once infra is mature.

---

## 6. Training & Control Algorithms
1. **Static Zero-Shot Phase** – Run debate without extra training to establish baseline uplift; collect traces and outcomes.
2. **Debate-Fine-Tuning Phase**  
   • Successful transcripts (high test pass + low hallucination) are distilled back into the base model via next-token supervised fine-tuning.  
   • Loss = CE(logits, target) + λ·DIVERSE where DIVERSE penalizes redundant reasoning to preserve heterogeneity.  
   • Value Matching: also regress pass/fail signal as scalar “value” head to allow RL fine-tuning.
3. **Reinforcement Phase**  
   • Model plays both roles in turn-based debate, reward = +1 if final answer passes tests, −0.2 per hallucination flag, +0.05 per unique rationale token.  
   • Consensus actor-critic with decentralized updates (per AAAI’24) enables parallel training across 128 GPU workers with minimal communication.

Compute sketch (CodeLlama 70 B):  
• Fine-tune 20k debate transcripts ≈ 400 k tokens each → 8 B tokens ≈ 1.5 M GPU-hours at 200 t/s/A100.  
• RL phase 50 k games × 4 rounds × 400 tokens ≈ 80 M tokens, negligible extra cost.

---

## 7. Evaluation Suite & Success Metrics
1. **Primary Benchmarks** – HumanEval, MBPP, CodeContests, LeetCode-Hard subset, SF110, BigCode Bench.
2. **Hidden Proprietary Suite** – 500 production bugs from partner company; ensures external validity.
3. **Stress-Hallucination Tasks** – Ill-posed specs, ambiguous requirements. Measure hallucination ratio.
4. **Transparency Audits** – Senior engineers score debate transcripts on (i) clarity, (ii) utility, (iii) noise. Automated BERT classifier trained on 3 k human labels replicates scoring for scale.

Statistical testing: *Clopper–Pearson* 95 % CIs on pass rates; *paired bootstrap* for hallucination.

Deployment guard-rail: any regression > 1 pp on hallucination triggers rollback.

---

## 8. Experimental Road-Map
| Month | Milestone | Deliverable |
|-------|-----------|-------------|
| 0–1 | Infra | Debate orchestrator scripts, unit-test harness, logging DB |
| 1–2 | Zero-Shot Debates | 10 k samples, baseline lifts; internal report |
| 2–4 | Fine-Tuning Phase | Distilled checkpoint v1; offline eval |
| 4–5 | RL Phase | Checkpoint v2; ablation on voting vs. BM vs. majority |
| 5–6 | Token-Level Debate POC | Throughput analysis, early metrics |
| 6 | Public Tech Report & Open-Sourcing (if policy allows) |

---

## 9. Anticipated Risks, Failure Modes & Mitigations
1. **Debate Collusion / Mode Collapse**  
   • Inject stochasticity, checkpoint diversity, or explicit disagreement loss.
2. **Compute Blow-Up**  
   • Auto-shutoff when LoA mismatch > 2 σ; heuristics to end debate early on test-pass.
3. **Over-fitting to Benchmarks**  
   • Hold-out secret suite; adversarial example generation.
4. **Opaque Transcripts**  
   • Require structured JSON rationales; use summarizer agent to post-process.

---

## 10. Speculative Extensions & Contrarian Ideas
*High speculation flagged.*
1. **On-Device Micro-Debate** – Distill debate logic into a single model that simulates multiple personas internally (similar to Mixture-of-Experts with routing conditioned on internal disagreement signal). Could run on laptop GPUs.
2. **Neuro-Symbolic Skeptic** – Replace one debating agent with an SMT solver that tries to refute code correctness. Hybrid increases rigor, at cost of limited language.
3. **Curriculum of Disagreement** – Intentionally feed slightly incorrect unit tests to force deeper debate cycles, analogous to adversarial training.
4. **Liquid Democracy-Style Delegation** – Agents dynamically delegate votes to more competent peers based on LoA trust scores, achieving logarithmic debate depth (untested).

---

## 11. Concluding Recommendations
1. Start with *turn-based self-play debate* on CodeLlama 70 B; expected immediate +5–7 pp on HumanEval.
2. **Prioritize heterogeneity** – different temperature seeds, checkpoints, or even model families; theory predicts unbounded gains with diversity.
3. Build **pairwise LoA estimator** early – it is orthogonal and will save compute across all phases.
4. After collecting 10–20 k high-quality transcripts, launch *policy distillation + value matching* to fold improvements back into a single checkpoint, amortizing inference cost.
5. Don’t skip hallucination metrics; adversarial debate can paradoxically increase confident wrong answers if adjudication is weak.

If executed, we project (probabilistic):  
• +15 pp on SF110, 95 % CI ±3 pp.  
• Hallucination ↓ by 45 % ±10 %.  
• Transparency score 4.2 / 5.

---

## 12. Appendix – Mapping Literature Learnings to Design Choices
| Learning | System Lever |
|----------|--------------|
| Pairwise LoA self-classification | Opponent scheduling, compute saving |
| Two-stage noisy voting | Adjudicator aggregation, token-level BM |
| Policy distillation + value matching | Converge to single deployable model |
| CodeLLM benchmark gap (HumanEval vs. SF110) | Motivation for deeper debate cycles |
| Consensus decentralized actor-critic | RL phase scalability |
| Boltzmann-multiplication ensemble | Token-level fusion |
| Overcooked centralized critic speed-vs-generalization | Caution: we need heterogeneity + randomization for partner robustness |
| Capability cliffs @ 3 kyu | Target for debate to extend |
| Vote-Revise-Vote NLG gains | Blueprint for 5.3 architecture |

---

*End of Report*

## Sources

- https://ojs.aaai.org/index.php/AAAI/article/view/26385
- https://hdl.handle.net/1721.1/137155
- https://tel.archives-ouvertes.fr/tel-01345797
- http://arxiv.org/abs/2205.10607
- https://hal-centralesupelec.archives-ouvertes.fr/hal-02649822
- http://repository.essex.ac.uk/19034/1/PacmanGhosts2016Competition.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/20887
- http://arxiv.org/abs/2309.12732
- http://ojs.uwindsor.ca/ojs/leddy/index.php/informal_logic/article/download/2174/1618/
- http://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/ensemble_RL_final.pdf
- https://zenodo.org/record/7875623
- http://www.scopus.com/inward/record.url?scp=33746673186&partnerID=8YFLogxK
- https://zenodo.org/record/6402300
- http://www.springerlink.com/content/fulltext.pdf?id=doi:10.1140/epjb/s10051-021-00259-9
- https://hal.inria.fr/hal-01821677
- https://ojs.aaai.org/index.php/AAAI/article/view/6216
- https://repository.uantwerpen.be/docstore/d:irua:20874
- http://www.wseas.us/e-library/transactions/computers/2008/28-458.pdf
- http://www.loc.gov/mods/v3
- https://hdl.handle.net/10072/433512
- https://hal.science/hal-04277513/document
- http://hdl.handle.net/10.36227/techrxiv.24486214.v1
- http://hdl.handle.net/10.1184/r1/6604934.v1
- http://www.nusl.cz/ntk/nusl-448493
- http://www.scopus.com/inward/record.url?scp=33644798424&partnerID=8YFLogxK
- https://digital.library.unt.edu/ark:/67531/metadc893370/
- https://ojs.aaai.org/index.php/AAAI/article/view/4566
- https://openreview.net/pdf?id=xy_2w3J3kH
- http://resolver.tudelft.nl/uuid:e801ead9-60be-44b4-85ee-829c93322763