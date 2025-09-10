# Step-wise Uncertainty Estimation in Chain-of-Thought Reasoning

*Prepared 2025-09-04*

---

## 1 Problem framing and objectives
Chain-of-thought (CoT) prompting exposes a model’s intermediate reasoning instead of only its final answer.  While CoT greatly boosts accuracy and interpretability, it also surfaces an unmet need: **reliably quantifying the model’s uncertainty _at every intermediate step_**, not just on the final answer.  Such *step-wise* or *token-level* uncertainty signals can then be used for

* dynamic search control (e.g., prune low-confidence thought branches in Tree-of-Thoughts),
* selective generation or early exit,
* human-in-the-loop verification,
* safety guarantees in decision-making pipelines, and
* curriculum-style self-training where the model learns more from low-certainty steps.

Because the user left the clarifying questions blank, we treat the scope as **maximally broad**: we want both new algorithms and evaluation recipes that cover training-time integration, inference-time/post-hoc techniques, and application to multiple downstream tasks.  Specifically we will:
1. Catalogue existing mechanisms for step-wise uncertainty in language models.
2. Compare their calibration behaviour, compute cost and ease of deployment.
3. Propose novel research directions and contrarian ideas beyond the current literature.

Throughout we distinguish
* **Granularity**: token-level, “thought” (natural-language span) level, or whole tree path.
* **Uncertainty type**: epistemic (model uncertainty) vs. aleatoric (data/label noise).
* **Integration locus**: weight-space (Bayesian training), activation-space (dropout masks), output-space (verbalised probabilities), or search-space (uncertain nodes in ToT).

---

## 2 Taxonomy of techniques

### 2.1 Dropout-based Monte-Carlo ensembling

| Variant | Key idea | Strengths | Weaknesses |
| --- | --- | --- | --- |
| **Standard MC-Dropout** (Gal & Ghahramani 2016) | Sample Bernoulli masks at inference | Zero retraining cost; easy to retrofit | Requires many forward passes; vanilla masks poorly calibrated on NLP |
| **Controlled Dropout** (arXiv 2205.03109) | Limit the number of unique masks, reuse across timesteps | Lower variance estimate with fewer samples; >10× faster | Needs code-level change to transformer blocks |
| **Concrete Dropout** (Gal et al. 2017) | Learn per-layer dropout rate via differentiable Concrete distribution | Removes grid-search; yields better calibration | Requires finetuning; heavier regularisation may hurt perplexity |
| **Variational/Bayesian RNN Dropout** | One shared mask across all timesteps of an RNN cell | Theoretically grounded as GP approximation | Less relevant now that LSTMs are eclipsed by transformers |
| **Inference-only “dropout injection”** | Activate dropout *post-hoc* and rescale logits | Requires no retraining; calibration close to embedded dropout | Needs a per-task scale factor, non-Bayesian heuristic |
| **Tree of Uncertain Thoughts (TouT) 2023** | Attach MC-Dropout uncertainty to every node in ToT search | Beats vanilla ToT and CoT on planning games | Currently limited to small reasoning trees; sampling cost scales with branching factor |

### 2.2 Weight-space posterior sampling

* **SWAG (Stochastic Weight Averaging-Gaussian)**: collect weight snapshots during training, fit a low-rank Gaussian posterior, then sample new weights at inference.  On NLI it tightened Expected Calibration Error (ECE) by ≈40 % and correlated with human annotation disagreement—evidence that weight-space epistemic uncertainty aligns with semantic ambiguity.
* **Potential for step-wise reasoning**: every sampled weight vector can generate a full chain-of-thought; the variance across trajectories yields a confidence band per step.

### 2.3 Output-space verbal confidence

LLMs can be prompted or fine-tuned to emit natural-language confidences (e.g. “90 % sure”).  On *CalibratedMath* these verbal reports are *better calibrated than softmax logits* and degrade gracefully under distribution shift.  This is attractive because it needs only one forward pass, but it blurs epistemic vs. aleatoric uncertainty and currently lacks granularity below the final answer.

### 2.4 Search-space uncertainty

Tree-of-Thoughts (ToT) introduced breadth-first reasoning but chose branch scores ad-hoc (e.g., log-probs of node text).  **Tree of Uncertain Thoughts (TouT)** replaces that with *MC-Dropout variance* per node, improving solution rates on Game-of-24 and Mini-Crosswords.  This shows that *intermediate* uncertainty can guide exploration effectively.

---

## 3 Evaluation metrics and benchmarks

### 3.1 Metrics
* **Negative Log-Likelihood (NLL)**: gold standard probabilistic score; penalises over-confident errors.
* **Expected Calibration Error (ECE)** or **Token-ECE**: bucketised gap between confidence and empirical accuracy at each step.
* **Brier Score / Decomposition**: separates calibration loss, refinement, and resolution—helpful to isolate epistemic vs. aleatoric components.
* **Area under Confidence-Accuracy Curve (AUC-CAC)**: holistic view for downstream decision thresholds.
* **Structural scores for trees**: e.g. probability mass assigned to the solved branch vs. distractor branches.

### 3.2 Datasets and tasks
1. **ThoughtSource** (15 CoT datasets) gives breadth across domains.
2. **CalibratedMath** (SyLin 2022): gold labels for both answer correctness and numeric confidence → direct calibration check.
3. **Game-of-24, Mini-Crosswords**: planning tasks with natural search trees; uncertainty influences solver efficiency.
4. **BIG-Bench Hard** (subset): multi-step reasoning but few existing uncertainty baselines—ripe for new benchmarks.

*Recommendation*: use a multi-task battery combining (1) maths (highly structured), (2) open-domain QA (noisy labels → aleatoric), and (3) planning games (tree search demands step-wise signals).

---

## 4 Integration loci and design choices

### 4.1 Training-time Bayesianisation

a) **Concrete Dropout finetune** on a mid-sized OpenAI or open-weights model.  Learn per-layer dropout rate while prompting CoT style examples; keeps inference cost low (one forward pass if we rely on verbal confidence) or moderate (10–20 MC passes).

b) **Full SWAG sweep**: continue training a task-adapted model with SWA trajectory, then fit Gaussian.  Each sample yields a *whole* model; costs are one forward pass per sample but each pass is deterministic, enabling embarrassingly parallel evaluation.

Advantage: deeper Bayesian grounding, better out-of-distribution performance.  Disadvantage: heavyweight; multiple million-parameter models in memory.

### 4.2 Inference-time stochasticity only

The simplest pipeline: take an off-the-shelf GPT-J / Llama-2, toggle dropout `p = 0.1` at each transformer feed-forward layer during generation, and draw *K* (≈30) trajectories.  Compute per-token entropy or variance.  **Controlled Dropout** can cut K to 4–8 without losing calibration, saving GPU hours.

### 4.3 Search-time uncertainty control

Plug either source of uncertainty into Tree-of-Thought search heuristics: prune branches whose **upper confidence bound** (UCB) falls below a threshold, or conversely expand high-variance nodes to gather information (active search).  Preliminary TouT results show >10 % solution-rate gain at equal compute.

### 4.4 Post-hoc calibration layers

After collecting raw stepwise probabilities we can re-map them with:
* **Temperature scaling** (tuned on validation set) per step index.
* **Dirichlet calibration** jointly over steps to enforce monotonic uncertainty reduction.
* **Isotonic regression** when we do *not* trust parametric assumptions.

---

## 5 Experimental blueprint

1. **Models**: Llama-2-7B (open) and GPT-3.5-turbo (API).  For opened-weights we test (i) vanilla, (ii) Concrete-Dropout finetuned, (iii) SWAG.
2. **Generation modes**: CoT greedy, CoT temperature 0.7, ToT (breadth 2, depth 4), TouT (same search, using MC-Dropout variance as node score).
3. **Uncertainty extraction**: (a) token logit variance across 32 MC samples; (b) explicit “X % confidence” verbal token parsed via regex; (c) hybrid ensemble + verbal (averaged).
4. **Metrics**: Token-ECE, Brier, final-answer NLL, compute cost (GPU-hours), tree nodes evaluated.
5. **Ablations**: sample count K, dropout rate p, presence/absence of Controlled-Dropout mask pooling, SWAG rank.
6. **Downstream decision tasks**: selective question answering (answer only if step-4 confidence > τ); game-of-24 solver with branch budget ≤ 40.

---

## 6 Novel directions & contrarian ideas

### 6.1 Hierarchical Dropout for hierarchical reasoning
Use **two dropout temperatures**: high p on earlier layers for coarse diversity, lower p on later layers for fine-grained calibration.  Mimics coarse-to-fine reasoning, may yield richer step-wise variance without exploding sample count.

### 6.2 Step-indexed SWAG (speculative)
Re-interpret each reasoning step as conditioning on additional evidence; run a *particle filter in weight space*: after emitting step t, importance-sample weight vectors that explain the partial chain best.  This could capture epistemic shrinkage as reasoning unfolds.  Flagged as high-risk research.

### 6.3 Diffusion-based CoT sampling (contrarian)
View each chain-of-thought as a trajectory through latent space; run a small diffusion model that gradually *denoises* an uncertain plan into a concrete answer, giving a natural estimate of uncertainty via the variance schedule.  Unexplored but parallels diffusion-LM work.

### 6.4 Calibration-aware reward models for RLHF
Most RLHF pipelines optimise for helpfulness but ignore calibration.  Add a term that penalises mis-calibrated verbal confidences at each step.  This could teach the model an *intrinsic sense* of uncertainty rather than bolted-on sampling.

### 6.5 Program-analysis alignment
If we compile CoT into a formal program (e.g., Chain-of-Thought-to-Python), we can run symbolic execution to *verify* steps.  Uncertainty then collapses for verified steps, isolating epistemic mass on the un-verifiable parts.  Hybrid neuro-symbolic idea.

---

## 7 Recommendations

1. **Start cheap**: implement inference-time MC-Dropout with Controlled-Dropout on an open model; gather 32 samples; compute token-level ECE on ThoughtSource.
2. **Parallel path**: finetune Concrete Dropout rates on a subset for better OOD calibration; evaluate compute/accuracy trade-off.
3. **Integrate with search**: wrap both pipelines in TouT; measure branch budgets.
4. **Add verbal confidence** as a baseline—one forward pass, virtually no cost, surprisingly strong.
5. **Iterate on calibration layers**: temperature-scale per step index; publish ablation plots.
6. **Publish a benchmark**: extend ThoughtSource with per-step gold “is this step correct?” annotations on 5 key tasks; this fills a current gap.

---

## 8 Take-home messages

* Multiple lightweight tricks (Controlled-Dropout, verbal confidences) already *materially improve* step-wise uncertainty without retraining.
* Weight-space methods (SWAG) promise deeper epistemic grounding but need engineering to scale to 7 B+ parameters.
* The community lacks standardised step-wise calibration metrics; adopting Token-ECE and Brier decompositions is low-hanging fruit.
* **Uncertainty-aware search (TouT)** is currently the most effective demonstration of *using* step uncertainty for performance gains; pushing it to harder tasks is the next milestone.

---

> *Speculative but high-impact*: Coupling SWAG-style weight posterior sampling with program-verification loops could give both calibrated probabilities and correctness certificates—a path toward rigorous AI safety arguments.


## Sources

- http://d-scholarship.pitt.edu/43419/1/Taehee_Dissertation_Paper_v2.pdf
- https://www.repository.cam.ac.uk/handle/1810/316387
- http://arxiv.org/abs/2210.15452
- http://arxiv.org/abs/2205.03109
- http://www.cs.utoronto.ca/%7Ehinton/absps/JMLRdropout.pdf
- http://arxiv.org/abs/2205.14334
- https://www.hal.inserm.fr/inserm-02141610
- https://www.intechopen.com/books/uncertainty-quantification-and-model-calibration
- https://figshare.com/articles/_Accuracy_of_probability_estimates_and_confidence_/1450251
- http://www.igb.uci.edu/%7Epfbaldi/download/download.inc.php?pid%3D317
- http://repository.cshl.edu/id/eprint/32785/
- https://scholarship.claremont.edu/jhm/vol11/iss2/31
- https://mindmodeling.org/cogsci2015/papers/0452/index.html
- http://resolver.tudelft.nl/uuid:e2bc20fc-3284-4ce1-ad0f-7564aa3b9d1a
- http://hdl.handle.net/10453/123817
- http://hdl.handle.net/11336/85015
- http://arxiv.org/abs/2311.08298
- http://hdl.handle.net/10138/563840
- https://doaj.org/article/cfd6089d4104413787e743dddb10d8e7
- https://ojs.aaai.org/index.php/AAAI/article/view/4719
- https://zenodo.org/record/1422804
- http://nlp.stanford.edu/~sidaw/home/_media/papers:fastdropouttalk.pdf
- http://arxiv.org/abs/2309.07694
- https://ore.exeter.ac.uk/repository/bitstream/handle/10871/11586/computing_with_confidence_2006.pdf%3Bjsessionid%3DB4852405172EC40A0BE400519DB4753D?sequence%3D2
- https://escholarship.org/uc/item/3qq6w5kx
- http://www.sigdial.org/workshops/workshop5/proceedings/pdf/raymond.pdf
- https://doaj.org/article/abe11eb02f2a479e8ed4c93ad9b77551
- https://hdl.handle.net/11584/380063