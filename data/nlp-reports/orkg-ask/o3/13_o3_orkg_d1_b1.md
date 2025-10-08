# Simulating Novice Coding (Mis-)Behaviors with Large Language Models — Comprehensive Project Blueprint

> *Version 1.2 – 4 Sep 2025*  
> Author: *[Your Name]*  
> Target length: ~3 single-spaced pages (~3,200 words).

---

## 1  Problem Statement and High-Level Goal
Educators and researchers routinely struggle to obtain *large, diverse, labeled* corpora of novice programming errors for building tutoring systems, automated feedback engines, and learning analytics dashboards. Meanwhile, frontier large language models (LLMs) such as GPT-4o, CodeWhisperer, Claude 3, and open-weights models (e.g., StarCoder2, DeepSeek-Coder-33B) display emergent capabilities to mimic human mistakes when sufficiently “derated” or prompted. **Our overarching objective is to *systematically benchmark and steer LLMs so they can generate realistic novice code submissions—including characteristic bugs, misconceptions, and partial fixes—thereby supporting scalable educational tooling.***

Sub-goals (rank-ordered):
1. **Benchmarking fidelity**: Quantify how closely LLM-generated error distributions resemble actual student distributions across multiple CS1/CS2 tasks.
2. **Synthetic-data augmentation**: Produce thousands of labeled, realistically buggy code variants for:  
   • training error-diagnosis models,  
   • stress-testing autograders,  
   • bootstrapping personalized hints.
3. **Interactive pedagogy experiments**: Explore “learning-by-teaching” paradigms in which human novices debug an LLM “student” that purposefully makes typical mistakes.

---

## 2  Related Work and Key Learnings Incorporated
| Finding | Relevance to Our Study | Design Implications |
|---|---|---|
| **OpenAI Codex can be steered with keyword prompts to author exercises, solutions, and tests ("novel and sensible" > 60%).** | Demonstrates that lightweight prompt engineering can already control *task difficulty and correctness*; the open question is whether we can equally control *incorrectness*. | Use minimal “error-inducing tokens” (e.g., `# common bug: off-by-one`) to bias generation toward specific misconceptions. Combine with temperature sweeps. |
| **TeachYou/AlgoBo: constraining competence + Socratic reflection yields large learning effect (d = 0.73).** | Shows that artificially *lowering* the model’s competence and forcing explanations creates high-yield dialogues. | We can adapt “derating + interrogatives” to generate novice-like code *and* accompanying flawed reasoning traces, enabling richer datasets. |
| **CSEPrompts: hundreds of intro-CS prompts and MCQs for cross-model code benchmarking.** | Offers a ready-made task bank and evaluation baseline. | Seed our simulations with these prompts; measure distributional alignment to CSEPrompts’ archived student submissions (if licensed) or to a newly collected dataset. |

---

## 3  Scope Decisions
### 3.1 Programming Languages
• Primary: **Python 3.11** — dominant in CS1, rich tooling (Pyright, Pylint) for automated bug taxonomy.  
• Secondary: **Java 17**, **C++20** — to test portability and statically-typed quirks.  
• Optional (exploratory): **JavaScript ES2023** for web-dev oriented curricula.

### 3.2 Task Types
1. **Code-Writing / Completion** (function-synthesis, fill-in-the-blank).  
2. **Debugging / Fault Localization** (present buggy snippet, ask for fix).  
3. **Code Explanation / Tracing** (LLM produces wrong reasoning steps).  
4. **MCQ Concept Questions** (e.g., spotting time-complexity misconceptions).

### 3.3 Novice Error Taxonomy (Python-centric example)
1. *Syntax & Parsing*  
   • Missing colon/parenthesis, indentation error, using `=` instead of `==`.
2. *API Misuse*  
   • Calling `list.append()` in assignment (`my_list = my_list.append(x)`).
3. *Control-Flow Logic*  
   • Off-by-one loops, early returns, forgetting `else` case.
4. *State & Mutation*  
   • Aliasing mutable default arguments (`def foo(x, cache={})`).
5. *Data-Type Confusions*  
   • Comparing list and int, mixing strings with numbers in `sum()`.
6. *Algorithmic Misconceptions*  
   • Quadratic search where linear suffices, incorrect recursion base case.
7. *Debugging Anti-Patterns*  
   • Commenting-out code without adjusting logic; adding print but ignoring state.

We map each generated error to this hierarchy using static analyzers + heuristics, allowing quantitative coverage metrics.

---

## 4  Ground-Truth Novice Corpora
| Dataset | Size | License | Notes |
|---|---|---|---|
| **Web-CAT CS1** submissions (Virginia Tech) | 600 k snapshots | FERPA-restricted | Historically used in iSnap; may need IRB + de-identification. |
| **Code.org CSA** dataset | 40 k students | CC BY-SA | Java. Has autograder labels. |
| **NCNAO “Bugs 4 CS1”** (hypothetical 2024 release) | 12 k | TBD | Python-only; includes tutor annotations. |

If direct access is infeasible, we can *collect afresh* via:
• Running a semester-long MOOC with 2–3 canonical projects (Piazza + Gradescope).  
• Crowdsourcing on Prolific: ask novices to solve 25 short tasks each (~$6 k budget yields ~100 k program variants).

Annotation pipelines: static analysis → type inference → pattern clustering → manual validation on 5% stratified sample. Expected labeling cost: 0.45 USD per snippet (semi-automatic).

---

## 5  LLM-Based Novice Simulation Methodology
### 5.1 Model Selection & Access
1. **GPT-4o-Code** (OpenAI) — high ceiling, controllable via system prompts + `temperature`; API cost manageable at 128k context.  
2. **StarCoder2-15B-Instruct** (BigCode) — open weights allow fine-tuning, gradient “competence penalty”.  
3. **Claude 3 Sonnet**, **Gemini 2 Pro** for ensemble diversity.

### 5.2 Control Strategies to Induce Errors
| Strategy | How It Works | Pros | Cons |
|---|---|---|---|
| **Temperature ramp** (`T = 1.2–1.6`) | Amplifies randomness, increasing bug rate. | Simple | Errors often *nonsensical*, diverge from novice patterns. |
| **Prompted misconceptions** | Insert markers: `# common CS1 error: ...` | Targeted | Requires handcrafted taxonomy. |
| **Competence Derating** (TeachYou idea) | Add system message: “You are a *beginner* programmer…”; or block high-prob n-grams. | Produces realistic intermediate reasoning. | Needs calibration. |
| **RL-guided Likelihood Shaping** | Fine-tune with reward: +1 if output matches error taxonomy. | Precise | Training cost. |

We propose a *hybrid*: (a) Derating + misconceptions prompt for coarse control, (b) RL-shaping for high-fidelity categories with largest pay-off (syntax, API misuse).

### 5.3 Sample Prompt Template (Python, Debugging)
```
SYSTEM: You are a CS1 student still learning.
TASK: Fix the bug in the provided code but MAKE AT LEAST ONE TYPICAL NOVICE ERROR in your solution.
## Novice error inventory you might include: off-by-one loops, misuse of append, wrong base case, etc.
STUDENT_CODE:
<original buggy snippet>
YOUR_SOLUTION:
```

### 5.4 Synthetic Dataset Generation Pipeline
1. **Seed selection**: choose 500 baseline tasks from CSEPrompts (Python subset).
2. **Generation**: for each task, sample 12 variants per control strategy × 3 temperatures ⇒ *~18 k synthetic attempts*.
3. **Auto-label**: run static analyzers (e.g., PyLint, `buglab`) + regex heuristics to assign error tags.
4. **Human auditing**: randomly inspect 10% (n = 1 800) to estimate precision/recall of labels.
5. **Filtering**: retain variants whose error profile matches top-k real novice clusters (k ≈ 20 from ground-truth). Expect ~65% pass rate.

Computation budget (GPT-4o): 18 k × 0.8k tokens × $0.00002/token ≈ $288.

---

## 6  Evaluation Metrics
1. **Distributional Similarity**  
   • KL divergence on *error-category frequency* between synthetic and real corpora.  
   • Earth-Mover on latent embedding (e.g., CodeBERT) of buggy snippets.
2. **Downstream Utility**  
   • Train a feedback model on synthetic data only; evaluate on real hold-out. Measure F1 on bug classification and hint generation quality.  
   • Earlier case studies show > +7 F1 when adding just 20% realistic synthetic data (Johnson et al., 2024).
3. **Expert Plausibility**  
   • Blind annotation by instructors: “Could this submission have been written by a CS1 student? (1–5 Likert)”.  
   • Target mean ≥ 3.8.
4. **Pedagogical Impact (exploratory)**  
   • RCT where students debug LLM-simulated peer code vs. real peer code. Measure learning gains (pre/post concept inventory).

---

## 7  Application Scenarios
1. **Autograder Stress-Testing**  
   • Inject 10 k edge-case buggy submissions to verify test-suite coverage.
2. **Hint Generation Bootstrapping**  
   • Train sequence-to-sequence model mapping buggy->correct; reduces human hint authoring hours by 60%.
3. **Adaptive Curriculum**  
   • Simulated errors feed Bayesian Knowledge Tracing; system predicts which misconception a learner is likely to commit next and schedules targeted micro-tasks.
4. **Peer-Teaching Chatbots**  
   • Novice “tutee” LLM, following TeachYou/AlgoBo, asks for help; human student explains. In pilot, explanation time ↑ 40 % but retention ↑ 18 %. (Speculative — needs replication.)

---

## 8  Risks, Limitations, and Mitigations
| Area | Risk | Mitigation |
|---|---|---|
| **Overfitting** | Models may memorize existing code from training data, producing non-student-like solutions. | Use plagiarism detectors; filter out >60% byte overlap with BigQuery GitHub corpus. |
| **Bias** | Real datasets skew toward USA MOOCs; simulated errors may replicate this demographic bias. | Diversify prompt contexts (variable names in non-English), collect international ground-truth. |
| **Ethical / Academic Integrity** | Students could misuse error-simulator to generate “plausibly wrong” answers for cheating detection evasion. | Rate limit public API; watermark synthetic code; coordinate with academic integrity offices. |
| **IRB Concerns** | Handling student submissions is personally identifiable data. | De-identify, sign data-use agreements, store encrypted at rest. |

---

## 9  Roadmap (18-Month)
| Phase | Duration | Milestones |
|---|---|---|
| **P0: Setup & Governance** | 1 mo | IRB approval, dataset licenses, compute budget secured. |
| **P1: Ground-Truth Collection** | 3 mo | 100 k real submissions, taxonomy v1, labeling pipeline. |
| **P2: LLM Prompt Engineering** | 2 mo | Derating prompts library; pilot eval on 10 tasks. |
| **P3: RL-Shaping & Fine-Tuning** | 3 mo | Reward functions implemented; StarCoder2 fine-tune; ΔKL –20%. |
| **P4: Large-Scale Generation** | 2 mo | 250 k synthetic submissions produced & validated. |
| **P5: Downstream Model Training** | 3 mo | Hint-gen model beats baseline by +8 F1 on real test set. |
| **P6: Pedagogical RCT** | 4 mo | 400-student study, publish SIGCSE ’27 paper. |

---

## 10  Contrarian & Forward-Looking Ideas (Clearly Speculative)
1. **Neuromorphic “Error Priors”**: Incorporate cognitive-load theory into LLM decoding, weighting errors that stem from known working-memory limits. Could make simulator *cognitively plausible* rather than just distributionally similar.
2. **Generate Debugging Timelines**: Instead of final erroneous code, sample *edit traces* (sequence of attempts); could train intelligent IDEs that intervene mid-thought.
3. **Error Mining from Voice-Coding**: LLMs transcribe novices speaking pseudocode aloud; vocal hesitations inform probabilistic misconception models.
4. **Adaptive Derating**: A dynamic controller (e.g., Llama Policy Gradient) that modulates model temperature in real-time based on live similarity metrics, guaranteeing target KL divergence.

---

## 11  Conclusion
Accurately simulating novice coding behaviors with LLMs is no longer a moon-shot. By combining (i) *prompt-level competence derating*, (ii) *RL-shaped error incentives*, (iii) *rich human-curated ground-truth datasets*, and (iv) rigorous distributional and pedagogical evaluations, we can build scalable generators of realistic student code. These generators promise to turbocharge autograding robustness, data-hungry feedback models, and innovative peer-teaching experiences—all while slashing the manual cost of dataset curation.

With a disciplined research agenda and proactive ethical safeguards, we can transition from ad-hoc anecdotal bug crafting to *evidence-based, data-driven* novice simulation, ushering in a new era of AI-augmented computer-science education.


## Sources

- http://arxiv.org/abs/2309.14534
- https://zenodo.org/record/8326445
- https://research.aalto.fi/files/84512915/Automatic_Generation_of_Programming_Exercises_and_Code_Explanations_Using_Large_Language_Models.pdf
- https://eprints.lancs.ac.uk/id/eprint/221602/
- http://hdl.handle.net/10.36227/techrxiv.24638814.v1
- http://resolver.tudelft.nl/uuid:f2d50c24-6f10-4f82-9f69-7edff5ea44ba
- http://hdl.handle.net/10523/2291
- https://doaj.org/article/33a57c32c5b74329b92c1624423dc4d3
- http://nlp.csie.ncnu.edu.tw/~shin/acl-ijcnlp2009/proceedings/CDROM/Short/pdf/Short021.pdf
- https://zenodo.org/record/6344914