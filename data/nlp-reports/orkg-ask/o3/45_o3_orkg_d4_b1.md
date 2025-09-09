# Final Report – Modular Calibration for Long-form Answers

*Prepared 2025-09-04*

---

## 1 Executive summary
Long-form answer generation systems—whether built on large language models (LLMs), retrieval-augmented generation (RAG), program-of-thought toolchains, or domain-specific simulation pipelines—need *calibrated confidence* if we wish to:
• estimate answer‐level reliability; • compose multi-module workflows where later steps can react to earlier uncertainty; • meet audit or regulatory thresholds; and • enable human-in-the-loop (HITL) intervention only when genuinely necessary.  

The academic calibration literature, however, has been dominated by *scalar* prediction tasks (classification or real-valued regression).  Recent breakthroughs—particularly **Modular Conformal Calibration (MCC, arXiv 2206.11468)**—demonstrate that *wrappers* can endow *any* point-prediction model with prediction intervals that enjoy finite-sample coverage guarantees.  The question before us is how to transplant those ideas into *structured* or *long-form* answer settings.

Key take-aways from the research survey:
1. MCC unifies isotonic regression, temperature/Platt scaling, and conformal intervals, and delivers near-perfect calibration **and** sharper intervals across 17 public regression data sets.
2. Finite-sample guarantees hold even if the base learner is misspecified; i.e., calibration is *modular* and *model-agnostic*.
3. Ensembling (“aggregated conformal predictors”) complicates validity; the naïve ensemble forfeits guarantees unless extra assumptions hold.  Approximate validity can be restored, but only partially.
4. Temporal or covariate shift breaks conformal validity; refreshing the calibration split with in-distribution samples restores error rates but widens intervals.
5. Fine-grained observational data (e.g., hourly smart-meter readings) materially improve calibration efficiency in energy-model settings—suggesting that *data granularity* matters as much as algorithm choice.
6. Surrogate-accelerated Bayesian calibration pipelines (e.g., polynomial chaos expansion + PCA for heat-transfer models) show how calibration modules can piggy-back on *fast emulators* to meet real-time constraints.

The rest of the report maps these findings onto long-form answer generation and proposes a concrete *Modular Calibration Stack (MCS)* that decouples *segment-level* uncertainty estimation from *answer-level* aggregation while preserving rigorous coverage guarantees.

---

## 2 Problem framing

### 2.1 Why “long-form” ≠ scalar regression
A long-form answer A can be viewed as an ordered tuple of K atomic segments (s₁, …, s_K).  Each segment may originate from an LLM token stream, a retrieval snippet, a symbolic proof step, or an external simulation.

We desire
P(A is correct | x) ≈ γ
for some target γ (e.g., 95 % coverage) while providing *localized* credibility measures so that downstream modules (citation checker, refutation engine, human reviewer) can act selectively.

Naïve token-level probabilities emitted by autoregressive LLMs are notoriously *mis-calibrated*: they reflect next-token likelihood under the model’s learned distribution, not correctness in the world.  Aggregating them into segment- or answer-level confidence via simple heuristics (geometric mean, logit averaging) inherits that mis-calibration.

We therefore need a *wrapper* that:
1. requires no changes to the base model;
2. yields *finite-sample* guarantees under mild assumptions;
3. supports incremental deployment (retrofit onto existing systems);
4. is compatible with streaming or real-time generation; and
5. handles distribution drift, ensembles, and domain constraints.

This is precisely the design space where MCC-style ideas thrive.

---

## 3 Key research insights and their implications

| Research finding | Implication for long-form answers |
|---|---|
| MCC provides model-agnostic, finite-sample calibrated prediction intervals. | We can wrap any confidence source (token probabilities, RAG retrieval scores, reasoning tool logits) with a conformal–isotonic recalibrator to output segment-level coverage intervals. |
| Near-perfect calibration with sharper (narrower) intervals than temp-scaling or classic conformal. | Sharper intervals mean fewer false negatives (rejecting good answers) **and** fewer false positives (accepting bad ones); critical for HITL efficiency. |
| Ensemble conformal predictors lose validity; approximate fixes exist but need assumptions. | If we ensemble multiple LLMs or use mixture-of-experts routing, we must either (i) calibrate each expert individually and then union their intervals, or (ii) use theoretically sound aggregated conformal methods with explicit trade-off awareness. |
| Distributional drift ruins validity; recalibrating on fresh data restores it at the cost of wider intervals. | Long-form answer systems deployed in dynamic domains (news, finance) need *rolling calibration windows*; we must budget for interval widening or invest in active-learning to gather labeled calibration data. |
| Finer-grained data improves calibration efficiency. | Collect auxiliary signals (e.g., token-level log-prob trajectories, SERP ranking scores, citation graph stats) rather than only final correctness labels to tighten intervals. |
| Surrogate-accelerated Bayesian calibration can meet real-time constraints. | We can pre-train lightweight emulators of the calibration function to avoid heavy runtime conformal computations. |

---

## 4 Proposed Modular Calibration Stack (MCS)

### 4.1 Overview
```
                ┌───────────────────────────────────────────┐
                │   Base generator(s) (LLM / RAG / tools)  │
                └───────────┬──────────────────────────────┘
                            │ per-segment raw scores
                ┌───────────▼──────────────────────────────┐
                │ Segment-level Conformal Recalibrator     │  (MCC core)
                └───────────┬──────────────────────────────┘
                            │ calibrated intervals + point est.
                ┌───────────▼──────────────────────────────┐
                │ Interval Aggregator (Answer-level)       │
                │  • union / intersection logic            │
                │  • error-budget allocator                │
                └───────────┬──────────────────────────────┘
                            │ answer credibility score + expl.
                ┌───────────▼──────────────────────────────┐
                │ Decision Layer (HITL / auto-publish)     │
                └───────────────────────────────────────────┘
```
*Calibrator and aggregator are modular and hot-swappable.*

### 4.2 Algorithmic details
1. **Conformal score definition**.  For each segment s_i we need a non-conformity score α_i.  Options:
   • 1 – p_i where p_i is the LLM’s token-level correctness probability aggregated via dynamic programming;  
   • A regression model predicting binary correctness from features (retrieval overlap, contradiction flags, tool verdicts).  
   The MCC recipe plugs in *any* α_i.

2. **Calibration data**.  Collect a set {(x_j, α_j)} of recent segments with ground-truth correctness labels (manual audits, automated proofs).  Under IID, MCC guarantees (1 – δ) coverage for any δ.

3. **Isotonic + conformal hybrid**.  MCC first fits an isotonic regression to map raw scores to empirical cumulative distribution; then applies split-conformal to obtain data-driven quantiles q_δ.  The calibrated interval for a new segment is [0, q_δ].

4. **Answer-level aggregation**.  Let E_i be the event “segment i is wrong”.  If we want answer-level coverage ≤ δ, a simple (though pessimistic) union bound sets per-segment δ_i = δ/K.  Tighter aggregation (Bonferroni-Holm, Bayesian network factorization, dependency-aware conformal) can reduce over-conservatism.  We recommend *adaptive error budgeting*: allocate higher δ_i to low-impact sections (boilerplate) and lower δ_i to critical facts.

5. **Drift handling**.  Maintain a sliding calibration window (e.g., last N=5000 audited segments).  Use **change-point detectors** on α distribution; if KL-divergence exceeds τ, trigger recalibration.

6. **Ensemble integration**.  For mixture-of-experts LLMs, compute separate α_i^m for each expert m and apply *aggregated conformal prediction with overlap penalty* per (Angelopoulos & Bates 2023).  Acceptable only if base experts satisfy exchangeability assumptions; else fall back to worst-case union.

7. **Runtime acceleration**.  Train a *surrogate calibrator* g_φ(•) (e.g., two-layer MLP) on (raw α, calibrated interval width) pairs.  At runtime call g_φ to approximate q_δ; fall back to MCC when g_φ’s uncertainty (MC-dropout) crosses a threshold.

### 4.3 Interpretability hooks
Because isotonic calibration is monotonic and piece-wise constant, we can surface *breakpoints* to domain users: “Segments with LLM confidence below 0.72 historically required manual review 90 % of the time.”  Sharper intervals help compliance teams argue that the system’s ‘guardrails’ are quantitatively defensible.

---

## 5 Addressing domain-specific constraints

| Constraint | Calibration accommodation |
|---|---|
| Real-time (<200 ms) budgeting | Pre-compute isotonic step function; O(log n) lookup.  Use surrogate accelerators. |
| Medical legal compliance (high recall) | Set δ aggressively low (e.g., 0.01).  Use hierarchical error budgeting: facts → citations → overall narrative. |
| Interpretability | Expose calibration plots, empirical coverage metrics, and per-segment interval widths in audit dashboard. |
| Low-label regime | Leverage *semi-supervised MCC*: use unlabeled segments with *self-consistency* checks as pseudo-labels, but flag as speculative. |
| Data privacy (PII) | Perform calibration locally; store only α scores, not raw text; hash linking. |

---

## 6 Open challenges & contrarian ideas
1. **Beyond exchangeability**.  Long-form answers exhibit *serial dependence* (earlier segments influence later ones).  Conformal methods assume IID or exchangeability.  *Mondrian conformal* on discourse structure or *online conformal* with martingale tests could relax this but need fresh theory.
2. **Coverage vs. utility trade-off**.  Wider intervals guarantee safety but may trigger excessive escalations.  Active sampling of ‘hard’ segments for labeling can shrink intervals quickly.
3. **Counterfactual calibration**.  Use causal language models to generate counter-answers; calibrate on the *set* of plausible answers to bound epistemic uncertainty.
4. Speculative: **functional calibration** where the unit is not a scalar α but an *explanation graph*; run MCC on graph embedding distances.

---

## 7 Implementation roadmap
1. MVP (2 weeks):
   • Log LLM token-level log-probs and simple features.  
   • Label 5k segments via crowd review.  
   • Fit isotonic + conformal; benchmark empirical coverage.  
2. Phase 2 (1 month):
   • Integrate answer-level aggregator and HITL routing.  
   • Deploy sliding-window recalibration with drift detector.  
3. Phase 3 (quarter):
   • Advanced aggregation (Bonferroni-Holm).  
   • Surrogate accelerator.  
   • Domain-specific dashboards; compliance reporting.  
4. Phase 4 (R&D):  serial-dependence conformal, counterfactual calibration.

---

## 8 Recommendations
1. Adopt MCC as the default segment-level calibrator; empirical evidence shows sharper, valid intervals compared with temperature scaling or raw logits.
2. Start with conservative answer-level union bound; iterate towards dependency-aware budgeting as confidence in system grows.
3. Invest in data labeling pipelines—coverage guarantees are only as good as calibration data freshness under drift.
4. If ensembling LLMs, calibrate each expert individually; do **not** rely on naïve averaging of probabilities.
5. Log fine-grained signals and use them for richer α definitions; this low-hanging fruit often beats exotic algorithm tweaks.

---

## 9 Conclusion
Modular Conformal Calibration, though born in scalar regression, offers a principled, *plug-and-play* pathway to calibrated long-form answer generation.  By decomposing answers into segments, applying MCC for segment-level coverage, and thoughtfully aggregating intervals, we can deliver quantitative reliability guarantees that survive base-model misspecification, distribution drift, and real-time constraints.  The proposed Modular Calibration Stack operationalizes these ideas today, while leaving open research avenues—serial dependence, functional calibration—to push reliability even further.


## Sources

- http://urn.kb.se/resolve?urn=urn:nbn:se:oru:diva-83146
- https://zenodo.org/record/7756062
- http://hdl.handle.net/10068/678287
- http://hdl.handle.net/10068/654167
- https://zenodo.org/record/7352194
- http://dx.doi.org/10.1007/978-3-319-17091-6_24
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-443979
- https://doi.org/10.4121/uuid:44c32783-15d0-4dbd-af8a-78b97be3de49
- https://eldorado.tu-dortmund.de:443/bitstream/2003/4870/1/tr14-04.pdf
- http://raiith.iith.ac.in/6129/
- http://arxiv.org/abs/2206.11468
- http://hdl.handle.net/10255/dryad.192363
- https://hal.archives-ouvertes.fr/hal-00953786
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-221578
- http://hdl.handle.net/Calibration
- http://infoscience.epfl.ch/record/222443
- http://digital.library.unt.edu/ark:/67531/metadc682450/
- http://digital.library.unt.edu/ark:/67531/metadc685362/
- https://hdl.handle.net/1721.1/128133
- http://digital.library.unt.edu/ark:/67531/metadc671335/
- http://hdl.handle.net/20.500.11850/387699
- https://zenodo.org/record/4742171
- http://dx.doi.org/10.17877/DE290R-5308
- https://doi.org/10.4121/uuid:14de57fd-e426-4ab3-9b51-c30d122d0cf9
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-475196
- http://doisrpska.nub.rs/index.php/IJEEC/article/view/6144
- https://hal.inria.fr/hal-01459631
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-221585