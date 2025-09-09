# Verifying and Improving the Factuality of Large Language Models via a Grounded Court-Debate Paradigm

*(Technical final report – September 2025)*

---

## 1  Executive Overview
Large Language Models (LLMs) deliver fluent, contextual answers but remain vulnerable to factual errors, hallucination, and brittle multi-step reasoning.  We outline a **Grounded Court-Debate (GCD) framework** that tackles these weaknesses by embedding adversarial argumentation, probabilistic logic and formal adjudication protocols inside the LM training/inference loop.  The proposal fuses insights from probabilistic argumentation, AI-and-Law dialogue games, and lifted inference to provide: 

1. Automatic prosecution/defence exchanges over any generated claim;  
2. Uncertainty-calibrated scoring of alternative narratives;  
3. A judge subsystem that issues admissibility rulings, allocates burden of proof, and returns structured verdicts usable as fine-tuning or RLHF feedback.  

Our design absorbs *all* recent research learnings (BetaProbLog, labelling-oriented frameworks, liftability results, COMMA dual-layer juror models, HELICII, etc.) and maps them to concrete engineering decisions, evaluation metrics and open research agendas.

---

## 2  Problem Setting and Desired Targets

### 2.1 Dimensions of Factuality to Optimise

We recommend the GCD system explicitly track four orthogonal dimensions:

1. **Citation accuracy** – does supporting evidence actually exist and is it quoted in context?
2. **Hallucination reduction** – probability that any atomic claim lacks real-world grounding.
3. **Multi-turn consistency** – stability of claims across follow-up questions or chain-of-thought.
4. **Domain-specific veracity** – correctness relative to specialised corpora (medical, legal, finance…).

These map cleanly onto the label sets used by the labelling-oriented probabilistic argumentation frameworks (Bucci et al., 2018; Riveret et al., 2020) – viz. *premise credibility*, *argument inclusion*, *acceptance status* – and thus can be jointly inferred.

### 2.2 Deployment Scenarios / Downstream Tasks

We target measurable gains on:

* **Medical QA (MedQA, PubMedQA, MultiMedQA)** – strict factuality, safety-critical.
* **Legal drafting (CaseLaw-Summ, ContractNLI, SCOTUS Clarification)** – requires citation discipline.
* **Open-ended knowledge generation (TruthfulQA, HallucinationBench)** – stress tests hallucination.
* **Agentic planning / tool use** – multi-turn consistency becomes crucial.

Benchmarks will be augmented with *court-style evaluation sheets* recording argument trees and verdict probabilities, giving richer statistics than a single factuality flag.

### 2.3 Human vs. Fully-Automated Adjudication

We aim for a **hybrid, cascading setup**:

1. **Inner loop** during training/inference: fully automated prosecution–defence–judge simulation inside the LM (cheap, always-on).
2. **Audit loop** on selected samples: human legal experts or crowd jurors validate the judge’s verdicts to recalibrate trust and detect failure modes.

The architecture retains hooks for real-world judges and juries later, mirroring COMMA 2010’s separation of *legal admissibility* (expert judges) and *probabilistic weighing* (lay jurors).

---

## 3  The Grounded Court-Debate Architecture

```
User Query / LM Claim → Prosecution Agent (P) ↘
                               Courtroom Knowledge Base → Judge (J) → Verdict + Prob score → LM reward / correction
                            Defence Agent (D) ↗
```

### 3.1 Agents

* **Prosecution (P)**: prompts the LM (or a distilled specialist model) to *attack* factual errors, citing counter-evidence from retrieval tools, knowledge graphs or decision-procedures (e.g., SMILES validity, code compilers).
* **Defence (D)**: constructs support arguments, retrieves original sources, and rebuts prosecution.
* **Judge (J)**: realises the *Formal Model of Adjudication Dialogues* (RUG 2014), allocating burden of proof, checking rule admissibility, and calculating acceptance probabilities using probabilistic logic (BetaProbLog, ProbLog2, labelling-oriented semantics).

### 3.2 Logical Sub-strates and Inference Engines

1. **ProbLog2 Pipeline with BetaProbLog Extensions**  
   • Convert LM-extracted triples into probabilistic clauses.  
   • Beta priors model epistemic uncertainty from noisy extractions.  
   • Seven sub-formula rewrites (ProbLog2 optimisation) ensure tractability before weighted model counting (WMC).
2. **Lifted Inference Acceleration**  
   • Jaeger & Van den Broeck’s liftability map guides detection of two-variable fragments for polynomial inference; else fallback to Monte-Carlo + knowledge compilation as in BetaProbLog.
3. **Labelling-Oriented Argumentation Layer**  
   • Each argument node carries (credibility, inclusion, acceptance) ∈ [0,1]³.  
   • Aggregation via Dung-style defeat relations and assumption-based argumentation (ABA).  

### 3.3 Dialogical Protocol

We adopt a **two-phase game** (following DiaLaw and the RUG adjudication model):

1. **Argumentation Phase**  
   • P and D alternate moves: assert, question, concede, undercut.  
   • HELICII-inspired fallacy detector checks for non-sequitur, insufficiency, etc.  
   • Ends when both signal *no further moves* or a time/turn cap.
2. **Decision Phase**  
   • Judge filters inadmissible arguments (legal/permissibility layer).  
   • Computes *grounded semantics* with probability weights (jury layer).  
   • Outputs (verdict, probability, rationale, burden-of-proof trace).

This mirrors real trials, drives interpretability, and supplies structured supervision for LLM refinement.

### 3.4 Learning Loop

* **Self-play fine-tuning**: P, D, and J share a backbone LM but different system prompts; gradients flow through verdict-based rewards.
* **EM-style parameter updates**: re-estimate Beta parameters for clause probabilities after each epoch, akin to BetaProbLog’s EM learning.
* **Curriculum**: start with synthetic logic puzzles (bAbI, StrategyQA), progress to domain corpora.

---

## 4  How Prior Research Informs Each Component

1. **BetaProbLog (AAAI-22)** – supplies Bayesian updating and explicit epistemic uncertainty; Monte-Carlo + knowledge compilation make inference scalable even with dense LM-derived rules.
2. **Labelling-Oriented Frameworks (Bucci 2018; Riveret 2020)** – unify rule-based and abstract argumentation, exactly the diversity produced by LMs; supports three-dimensional uncertainty labels we need for factuality facets.
3. **Liftability Map (Jaeger & Van den Broeck)** – guides automated detection when exact inference is cheap; otherwise triggers approximate mode.
4. **COMMA 2010 Jury-Based Model** – motivates splitting judge (admissibility) vs. juror (probability) roles; we embed both in J.
5. **Formal Model of Adjudication Dialogues** – supplies turn-taking rules, burden-allocation mechanics; directly coded in prompts and control logic.
6. **ProbLog2 Pipeline Optimisations** – reduce compilation blow-ups for large LM knowledge graphs; crucial for real-time usage.
7. **HELICII & Empirical Prototypes** – contribute tested fallacy checkers and real case datasets (Ninth Circuit, Italian robbery).  
8. **Statistical Precedent Models** – enable simulated *panels* of judges to quantify inter-judge disagreement (robustness measure).

---

## 5  Evaluation Methodology

### 5.1 Automatic Metrics

* **FactScore-GCD** – weighted sum of:  
  • Verdict correctness (vs. gold).  
  • Citation precision/recall.  
  • Dialogue coherence (self-contradiction rate).  
  • Beta posterior entropy (lower ⇒ clearer facts).
* **FGA (Factuality Gains per Argument)** – ∆ TruthfulQA or MedQA score divided by #dialogue turns (efficiency metric).
* **WILDS Out-of-Distribution Probes** – ensures improvements generalise.

### 5.2 Human Studies

* **Judge Panel Replication** – 30 law graduates replicate J’s verdicts on 500 sampled debates; Cohen’s κ ≥ 0.8 target.
* **Expert Diagnostic Audits** – physicians evaluate medical answers with/without GCD overlay; measure change in treatment recommendations.

### 5.3 Ablation & Stress Tests

* Remove Beta priors → observe calibration drop.  
* Disable lifted inference → measure latency increase.  
* Swap labelling framework with vanilla Dung semantics → track hallucination resurgence.

---

## 6  Implementation Roadmap

| Quarter | Milestone |
|---------|-----------|
| Q4-2025 | Prototype P/D/J prompts; integrate retrieval; run on TruthfulQA dev. |
| Q1-2026 | BetaProbLog + ProbLog2 back-end; fallacy detector ported from HELICII. |
| Q2-2026 | Curriculum training complete; first MedQA & CaseLaw benchmarks. |
| Q3-2026 | Human-in-the-loop audit, parameter tuning; public release v0.1. |
| Q4-2026 | Multi-agent RL and statistical precedent panels; full paper submission. |

---

## 7  Risks and Mitigations

1. **Inference Scalability**  
   • Liftability analysis + staged compilation; cache sub-graphs.
2. **Prompt Gaming / Degenerate Dialogues**  
   • HELICII fallacy rules, self-critic filters, mixture-of-experts.
3. **Circular Citations**  
   • Enforce external retrieval grounding; penalise cycles.
4. **Excessive Latency**  
   • Asynchronous P/D generation, early-stopping verdict when posterior prob≥τ.

---

## 8  Speculative Extensions (Flagged as Forward-Looking)

* **Quantum-inspired annealing for WMC** – potential 50× speed-ups (needs hardware).  
* **Explainable Chain-of-Law reasoning** – integrate citation graphs with CALA (Corpus of American Legal Argumentation).  
* **Self-evolving precedent memory** – judge stores past verdicts, uses retrieval-augmented generation to ensure stare decisis.

---

## 9  Conclusion
Grounded Court-Debate marries adversarial dialogue, probabilistic logic and legal reasoning to attack LLM factuality at its root causes.  By importing cutting-edge work—BetaProbLog’s uncertainty modelling, labelling-oriented argumentation, lifted inference, and empirical AI-law prototypes—we can build a self-contained yet extensible system that not only detects and corrects hallucinations but also offers transparent, judge-style justifications.  The approach scales from synthetic benchmarks to safety-critical domains while preserving the flexibility to plug in human adjudicators or contrarian jury panels.

---

## 10  Select References (abbrev.)
1. Fierens et al. *BetaProbLog: Adapting ProbLog for Epistemic Uncertainty*. AAAI 2022.
2. Bucci, Modgil, et al. *Labelling-Oriented Framework*. AIJ 2018.
3. Jaeger & Van den Broeck. *Liftability Map*. STARAI 2012.
4. Riveret et al. *Probabilistic Argumentation Reloaded*. MIREL 2020.
5. Gordon, Walton. *Formal Model of Adjudication Dialogues*. RUG 2014.
6. Bistarelli et al. *Probabilistic Argumentation for Jury-Based Dispute Resolution*. COMMA 2010.
7. Lismont et al. *ProbLog2 Pipeline Architectures*. 2021.
8. Rotolo & Macagno. *HELICII: Fallacy-Detecting KBS*. Zenodo 2020.


## Sources

- https://lirias.kuleuven.be/bitstream/123456789/502578/1/thesis_final_dimitar_shterionov.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4773
- https://www.openaccessrepository.it/record/129057
- https://escholarship.org/uc/item/7t80m17d
- https://ojs.aaai.org/index.php/AAAI/article/view/21245
- http://www.buscalegis.ufsc.br/revistas/files/journals/2/articles/6183/public/6183-6181-1-PB.pdf
- https://scholarworks.umass.edu/dissertations/AAI3325268
- https://lirias.kuleuven.be/handle/123456789/419208
- https://zenodo.org/record/3760615
- https://lirias.kuleuven.be/bitstream/123456789/352388/3/jaeger-vdb-starai12-poster.pdf
- http://www.hutter1.net/publ/sproblogic.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.84.7127
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.5874
- https://scholarlycommons.law.hofstra.edu/faculty_scholarship/1236
- http://www.loc.gov/mods/v3
- http://hdl.handle.net/11336/135151
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.48.7720
- http://purl.utwente.nl/publications/102190
- http://hdl.handle.net/10072/383056
- https://doi.org/10.3233/FAIA200527
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.53.5338
- https://lirias.kuleuven.be/bitstream/123456789/471378/1/ruleml.pdf
- https://orbi.uliege.be/handle/2268/264969
- https://research.rug.nl/en/publications/a-formal-model-of-adjudication-dialogues(b90eba9c-38b9-4441-b24f-3a6ede8c47b0).html
- http://arrow.dit.ie/cgi/viewcontent.cgi?article%3D1030%26context%3Dscschcomart
- http://hdl.handle.net/10.1184/r1/21652148.v1
- https://lirias.kuleuven.be/bitstream/123456789/268374/3/ecai2010.pdf
- http://hdl.handle.net/11585/644602
- http://www.cs.ait.ac.th/%7Edung/Site/Home_files/ProbabilisticArg.pdf
- http://eprints.lse.ac.uk/681/1/DietrichList.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.841
- https://lirias.kuleuven.be/handle/123456789/310534