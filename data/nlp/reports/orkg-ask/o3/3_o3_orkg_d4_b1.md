# Probabilistic Opinion Pooling for Open-Domain Question Answering (OD-QA)
*State of the art, design space, and a research agenda*

---

## 1. Motivation
Open-domain QA systems must marshal heterogeneous evidence (web passages, tables, images, model memory) and often rely on *ensembles* of retrievers, rerankers and readers.  Production deployments therefore face three long-standing problems:

1. How to turn **many imperfect probability forecasts** ("opinions")—coming from different sub-models, decoding strategies, or evidence pieces—into a single **well-calibrated answer distribution**.
2. How to **trade off compute vs. robustness**: naïvely adding more ensemble members yields diminishing returns and higher cost.
3. How to remain **robust to conflicting or out-of-distribution (OOD) evidence** retrieved from the open web.

Probabilistic *opinion pooling* gives a mathematically principled toolbox for (1), while *diversity-aware ensembling* addresses (2) and (3).  The two strands have rarely been combined in NLP; doing so is timely because recent findings in vision/forecasting (summarised in the Learnings) reveal novel regularisers, pooling rules and calibration hacks that can carry over to OD-QA.

---

## 2. Theoretical foundations of pooling
### 2.1 Classic pools
Let \(\{p_i(y)\}_{i=1}^M\) be expert/agent/ model posteriors over answer variable \(y\).

| Pool | Formula | Key property |
|------|---------|--------------|
| Linear (mixture) | \(p_{\text{lin}}(y)=\sum_i w_i p_i(y)\) | Externally Bayesian iff all experts use same prior; preserves *unanimity*. |
| Logarithmic (product) | \(p_{\text{log}}(y) \propto \prod_i p_i(y)^{w_i}\) | Commutes with Bayes updates; incentivises independent evidence; suffers from *pathology* when any \(p_i(y)=0\). |
| Harmonic | \(p_{\text{harm}}(y) \propto (\sum_i w_i/p_i(y))^{-1}\) | Heavy-tails; rarely used in ML but useful for lower-bounding probabilities. |
| Rényi-α mixture (Storkey et al., 2014) | \(p_{\alpha}(y) \propto \Big(\sum_i w_i p_i(y)^{1-\alpha}\Big)^{\frac1{1-\alpha}}\) | Interpolates smoothly: α→0 linear, α→∞ log pool; maximum-entropy under bias α. |

Finding *weights* \(w_i\) is itself a learning problem (equal vs. performance-based, hedging, Bayesian model averaging, stacking).  Empirically, **post-calibration can blur theoretical gaps**: the large 11 k-stock study on Beta-mixture calibration (Econometrics 2016) found that once forecasts were calibrated, linear, harmonic and log pools became “almost statistically indistinguishable”.  Still, different pools interact differently with mis-calibration (see §3).

### 2.2 Pooling versus decision layers in OD-QA
A modern OD-QA architecture typically exposes three aggregation junctions:

1. **Retriever union**: BM25, DPR, Contriever and dense-sparse hybrids each output recall-oriented scores per passage.  Pool here can increase recall.
2. **Reranker ensemble**: MonoT5, ColBERT‐v2, RePlug produce passage-level relevance probabilities.  Pool here steers evidence ranking.
3. **Reader / generator ensemble**: extractive span heads, generative LMs with different prompts/temperatures, or step-retrieval CoT decoders.  Pool here decides the final answer string and its confidence.

Because each layer’s *failure mode* differs—retrievers are under-confident but diverse; readers are over-confident and correlated—**hybrid pools** (e.g., linear at retrieval, logarithmic at reading) often outperform one-size-fits-all.

---

## 3. Calibration, diversity, and aggregation level
### 3.1 Logit- vs. probability-space pooling
The DLR 2023 study reports a striking asymmetry:

* For **under-confident** MC-Dropout ensembles on CIFAR-10, *logit averaging* cut Expected Calibration Error (ECE) from 12.0 % to 5.4 %.
* For **over-confident** MMCD on MNIST, the same trick *raised* mean false-positive confidence from 51 % to 95 %.

Take-away: **Choose pooling domain adaptively**.  In OD-QA readers tend to be over-confident, whereas retrievers/rerankers act under-confident.  We therefore recommend:

```
if ECE > threshold and avg-confidence < 70%:   # under-confident regime
    pool_logits()
else:                                           # over-confident
    pool_probs()   # or apply temperature scaling then pool
```

### 3.2 Diversity as an explicit regulariser

• arXiv:2201.10908 (Jan 2022) introduces an **OOD-sample diversity regulariser** that keeps ensembles calibrated while requiring ≈50 % fewer members; gains in top-1 accuracy and AUROC were concurrent.  The trick is to maximise *pairwise KL divergence* on synthetically generated OOD samples.

• The classic **Diversity Regularised Ensemble Pruning (DREP, 2012)** formalises pair-wise diversity as a capacity regulariser; **WAD (Zeng 2014)** further shows that a harmonic mean of accuracy and diversity beats accuracy-only selection on 80 % of UCI tasks.

Implication for OD-QA: retrieval ensembles with heavy weight sharing (e.g., multi-head adapters) can be pruned/regularised using OOD queries (nonsense strings, random word bags) to cut GPU RAM in half while maintaining recall and calibration.

---

## 4. Design space for pooling in QA
### 4.1 Weighting schemes
1. **Equal weights**: surprisingly hard to beat when ‘calibration questions’ are scarce (Classical Model literature).
2. **Performance-weighted**: use held-out calibration set; improves composite score but not Statistical Accuracy—so only if your validation set matches test domain.
3. **Bayesian model averaging**: treat each model’s log-marginal likelihood as weight; expensive but principled.
4. **Meta-learnt gating (stacking)**: small MLP takes per-expert features (entropy, retrieval score, OOD score) and outputs weights; can approximate any pool form.

### 4.2 When to prefer which canonical pool?
| Concern | Recommended pool | Rationale |
|---------|------------------|-----------|
| Heterogeneous evidence, correlated mistakes | Linear or small-α Rényi | Softly averages, avoids zero-probability domination. |
| Independent models w/ identical priors | Log pool or α→∞ | Theoretically Bayes-optimal under independence. |
| Need for *spiky* distribution (single answer surface form) | Log pool on **calibrated** probs | Encourages consensus. |
| Safety-critical (want hedging) | Harmonic or temperature-scaled linear | Heavy tails, penalises over-confidence. |

---

## 5. Practical recipe for an OD-QA pipeline
Below is a *reference architecture* that integrates the findings.

1. **Retrieval**
   • Models: BM25, Contriever, Cohere-Embed, T5-SS.
   • Scoring: convert raw scores to probabilities via softmax-temperature τᵣ.
   • Pool: *linear* with equal weights (diverse evidence desirable).
   • Calibration: isotonic regression on NQ-Train queries.

2. **Reranking**
   • Models: ColBERT-v2, monoT5-3B, SPLADE-Max.
   • Diversity regulariser: apply OOD KL penalty as in arXiv:2201.10908 on synthetic junk queries to prune to 3 models.
   • Pool: *Rényi α=0.3* (mildly super-linear to sharpen yet hedge).

3. **Reader / Generator**
   • Models: Fusion-in-Decoder 65M, Llama-2-13B-QA, ReAct-augmented Llama-2 pointer.
   • Logit or prob?  Measure ECE on dev set.  Typically FiD is under-confident (→logit), Llama-2 is over-confident (→prob).
   • Pool: adaptive per-question scheme:
     – If top-2 model posteriors within 0.15 → *log pool* (need decisive answer).
     – Else → *α=0.5 Rényi* to keep alternatives alive.

4. **Uncertainty post-processing**
   • Apply *Beta-mixture calibration*—shown to homogenise differences between pool types.
   • Compute answer-level ECE and Brier.

5. **Rejection / abstention**
   • Threshold on calibrated probability; use OOD AUROC from diversity-regularised readers to set risk-targeted cutoff.

---

## 6. Datasets & metrics

| Layer | Datasets for calibration & diversity | Metrics |
|-------|--------------------------------------|---------|
| Retrieval | BEIR multi-domain, MS-MARCO dev, *junk-query* synthetic set (for OOD) | Recall@k, nDCG@10, ECE (passage relevance) |
| Reader | NQ-Open, TriviaQA, WebQuestionsSP, HotpotQA | F1, EM, answer ECE, Negative Log-Likelihood (NLL) |
| End-to-end | KILT leaderboard tasks | Calibrated F1, selective-risk curves, OOD AUROC |

---

## 7. Experimental agenda
1. **Ablate pooling rules**: linear vs. log vs. α=0.5 vs. learned gating on identical readers; measure ECE, NLL.
2. **Vary aggregation domain**: logits vs. probs; include temperature scaling.
3. **Diversity regularisation sweep**: λ ∈ {0,0.1,0.5,1.0} on OOD KL; evaluate compute vs. robustness curve.
4. **Expert weighting vs. equal**: use 5-fold CV performance weights; test for over-fitting.
5. **Per-question adaptive α**: train regressor mapping (entropy, retrieval depth, evidence disagreement) → optimal α.

---

## 8. Contrarian & forward-looking ideas (flagged speculative)
*Chain-of-Thought as opinions* (S): treat each self-consistent CoT trace as an “expert”, then pool end-answers using α-adaptive Rényi; may capture diverse reasoning modes.

*GFlowNet-driven pooling* (S): frame answer generation as sampling from a flow network where each edge weight is an expert’s log-prob; training GFlowNets to match ground-truth yields a new *learned pooling operator*.

*Graph neural pooling over evidence* (S): nodes are evidence passages; edges carry inter-passage contradiction signals; run Belief Propagation to converge to marginal answer probabilities—equivalent to iterative log-pool with structured sparsity.

---

## 9. Implementation considerations
• **Weight-sharing**: use parameter-efficient LoRA adapters per reader; diversity arises via random initialisation & OOD regulariser, halving VRAM vs. full copies (confirmed by arXiv:2201.10908 vision results, expected to translate).

• **Calibration storage**: save isotonic/Beta-mixture maps as PyTorch tensors; <1 MB.

• **Latency**: linear + log pools are O(M|y|).  α-Rényi adds a single power op; negligible.  Gating MLP (~4 k params) also cheap.

• **Fail-safes**: detect zero probabilities before log pool; add ε=1e-9.

---

## 10. Key take-aways
1. **One pool does not fit all**: choose rule and aggregation level based on each component’s confidence regime.
2. **Calibration first, pool second**: post-calibration equalises many theoretical differences; skipping it leads to fragile log pools.
3. **Diversity is a free lunch—up to a point**: OOD-based regularisers and DREP/WAD pruning keep robustness while halving ensemble size.
4. **Adaptive α-Rényi pooling** offers a smooth knob between hedging and consensus, ideal for dynamically varying OD-QA conditions.

---

## 11. Recommended next steps
1. Build a *calibration probe* for each model (10-line PyTorch) and store ECE / NLL on dev set.
2. Implement α-Rényi pooling (2-line wrapper around `torch.pow`).
3. Generate 50 k synthetic junk queries to train OOD diversity regulariser for retriever and reader.
4. Run the experimental agenda over NQ-Open; iterate.
5. Integrate selective-risk curves into dashboard so product managers can set confidence thresholds post-deployment.

---

> **Bottom line**: By marrying *calibrated probabilistic opinion pooling* with *diversity-aware, compute-efficient ensembling*, OD-QA systems can deliver sharper answers, honest uncertainties, and lower serving cost—all without inventing new base architectures.


## Sources

- https://escholarship.org/uc/item/3kb142r2
- https://bibliotekanauki.pl/articles/375851
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.2549
- http://dx.doi.org/10.1109/ACCESS.2019.2949059
- https://figshare.com/articles/_The_initial_configuration_of_the_system_in_the_absence_of_social_influence_/841882
- http://hdl.handle.net/2066/100978
- https://dx.doi.org/10.3390/econometrics4010017
- http://arxiv.org/abs/2205.12507
- http://www.nusl.cz/ntk/nusl-200712
- http://cs.nju.edu.cn/yuy/%28S%285d4gahbn4pg3mx45ltokpf3i%29%29/GetFile.aspx?File%3Dpapers/ecml12-divprune.pdf
- https://cris.maastrichtuniversity.nl/en/publications/41b00ad2-a1d2-4a7f-b5c4-27b3467cebb3
- http://www1.ccls.columbia.edu/~dutta/iicai.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/20877
- https://doaj.org/toc/1930-2975
- http://hdl.handle.net/11583/2734222
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/d2/25/TSWJ2014-961747.PMC3925515.pdf
- https://doaj.org/toc/1537-744X
- http://bigml.cs.tsinghua.edu.cn/%7Edmpi-icml2014-workshop/static/Storkey_Zhu_Hu_A_Continuum_from_Mixtures_to_Products_Aggregation_under_Bias.pdf
- https://elib.dlr.de/188833/
- http://hdl.handle.net/10044/1/88397
- http://e.bangor.ac.uk/5816/
- http://arxiv.org/abs/2201.10908
- https://figshare.com/articles/The_ensemble_method_matches_or_beats_the_best_component_overall_consistently_improves_log_score_across_all_times_and_for_some_sets_of_components_can_provide_significant_improvements_in_both_log_score_and_mean_absolute_error_/6553343
- https://philpapers.org/rec/DIEPOP
- http://hdl.handle.net/1854/LU-8708723
- https://biblio.ugent.be/publication/01GYF8C0SFYGC9Q1EYT4QFTFZC/file/01GYF8HG3HJB0SZSQ65FXHZ9SS
- http://www.merl.com/publications/docs/TR2014-034.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.93.2608