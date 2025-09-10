# Chain-of-State Iterative Code Generation with Large Language Models
*An integrative technical report synthesising prior results in state-space search, long-range sequence modelling, and incremental verification*

---

## 1 Motivation and Scope
Code-generation LLMs (e.g. CodeWhisperer, Gemini-Code, DeepSeek-Coder) increasingly rely on **iterative prompting loops**—“generate → test → criticise → regenerate”.  While effective, the loop treats each turn’s *latent search state* (partial hypotheses, test results, compiler traces, execution logs) as transient chat history rather than a **first-class structured object** that can be *explicitly searched, pruned, cached, and reused*.  We call approaches that capture and exploit such rich internal context **Chain-of-State (CoS) iterative generation**.

The objective of this report is to design a *research programme*—from algorithm to system—that:

1. Maximises end-to-end **code correctness** (primary goal),
2. Minimises **CPU/GPU wall-clock time** per solve (secondary goal), and
3. Progressively **eliminates manual intervention** (tertiary goal)

by exploiting *state-space search* techniques traditionally used in SMT decoders, model checkers and Petri-net analysis, but adapted to LLM-driven code synthesis.

Three pages of detail follow: Section 2 formalises the problem, Section 3 links prior art, Section 4 proposes an architecture, Section 5 outlines evaluation, Section 6 sketches future extensions.

---

## 2 Problem Formalisation
We model a session as a discrete-time Markov decision process  
\(\mathcal{M}=\langle S,A,T,R\rangle\) where

* **State s∈S** encodes (i) natural-language spec, (ii) working code draft, (iii) execution traces, (iv) previously pruned alternatives.
* **Action a∈A(s)** is an *LLM call* with a concrete prompt template plus decoding meta-parameters (temperature, top-p, n-best size, etc.).
* **Transition T(s,a,·)** is stochastic—sampling k candidates, executing tests, updating caches—yielding successor states.  
* **Reward R** is +1 when all tests pass, −λ per token or per wall-clock second otherwise.

Because the branching factor is exponential in beam size×test outcomes, *explicit* search is intractable without (a) powerful heuristics and (b) **state compression**.

---

## 3 Lessons from Existing Research (Mandatory Integrations)

### 3.1 Pointer-Based Left-State Minimisation (Machine Translation Decoders)
* Finding: *Moses/cdec/Joshua* report **3–6 % CPU savings** under fixed cube-pruning and **11 % with retuned pop-limits** by compressing left contexts [Learning 1].
* Implication: Represent the *dynamic prompt history* of an LLM call as a *pointer chain* with hash-consing; identical prefixes across hypotheses share memory and avoid re-embedding.

### 3.2 Gated State Space (GSS) Layers for Long-Range Sequences
* Finding: GSS trains faster than DSS, equals well-tuned Transformers on **GitHub code, arXiv-Math, English Books**, and displays **zero-shot length generalisation**; adding local attention yields extra gains [Learnings 2–5].
* Implication: Adopt a *hybrid GSS + local-attention* decoder as the backbone; longer prompt windows (≫32 k tokens) are feasible without quadratic cost, enabling **deep CoS histories**.

### 3.3 Incremental State-Space Exploration (Software Model Checking)
* Finding: Reusing explored states across program revisions accelerates **22/24 cases by 6.4–68.6 %** (median 42 %) with <5 % regressions [Learnings 8–11].
* Implication: Cache test-execution traces and AST diffs; when regenerating only the mutated region, *skip* re-executing unaffected tests—mirrors JPF’s incremental DFS.

### 3.4 Incremental Petri-Net State Construction
* Finding: Step-wise refinement mitigates state explosion for Coloured Petri Nets [Learnings 6–7].  
* Implication: View the code-generation dialogue as a coloured Petri net where tokens carry hypothesis metadata; incremental firing corresponds to partial regeneration.

### 3.5 Benchmarks & Baselines
* **One-Billion-Word** set a 67.6 perplexity baseline for LM innovation [Learning 6]—useful sanity check.
* **CodeSearchNet** (6 M functions, multi-lang) is the de-facto dataset for semantic code tasks [Learning 9].  We extend it with unit tests via *HumanEval-style auto-generation*.

---

## 4 Proposed Architecture

### 4.1 Macro View
```
┌──────────────────────────┐
│ Natural-Language Spec    │
└──────────┬───────────────┘
           ▼
┌──────────────────────────┐
│ State Encoder (GSS+Attn) │──hash──┐   (left-context pointer compression)
└──────────┬───────────────┘        │
           ▼                    ┌───▼────────┐
┌──────────────────────────┐    │ State-Bank │◄──reuse / dedup
│ Action Generator (LLM)   │    └────────────┘
└──────────┬───────────────┘        ▲
           ▼                    (incremental lookup)
┌──────────────────────────┐        │
│ Test & Execution Harness │────────┘
└──────────┬───────────────┘
           ▼
     reward / diagnostics
```

### 4.2 Key Components and Design Choices

1. **State Object**  
   ```python
   class CoSState:
       nl_spec: str           # immutable root
       code: AST              # current hypothesis
       logs: List[RunTrace]   # test results, compiler errors
       parents: Tuple[ptr]    # DAG of antecedent states (for reuse)
   ```

2. **Left-Context Compression** (cf. Moses pointer trick)  
   • Concatenate `nl_spec`+`code_fragment`+`logs` into a prompt template.  
   • Deduplicate via *rope* data structure; embed unique substrings once.

3. **Hybrid GSS Backbone**  
   • 32–128 k token receptive field with O(n) time.  
   • Local attention window = 2 k tokens for syntactic details.

4. **Search / Control Strategy**
   *Beam-of-Beams*:
   - Outer beam over *high-level actions* (rewrite-module, add-test, refactor-loop).  
   - Inner beam over *low-level token completions* controlling the LLM sampler.
   - Cube-pruning style scoring: `score = λ₁·pass_rate − λ₂·#tokens − λ₃·latency`.

5. **Incremental Execution Harness**  
   • Use `pytest --lf` (“last-failed”) to rerun only failing tests.  
   • Memoise `(code_hash, input)`→`output` pairs; identical file→skip execution.

6. **State-Bank (Persistent KV)**  
   • Key = SHA-256 of serialised `CoSState`.  
   • Value = (embedding, perplexity, pass-vec, wall-clock).  
   • Eviction by *reward-adjusted LRU*.

7. **IDE / CI Integration**  
   • VSCode plugin surfaces alternative beams, colour-annotates diff vs baseline.  
   • GitHub Action uses same State-Bank to warm-start PR checks.

---

## 5 Evaluation Protocol

### 5.1 Datasets
1. **CodeSearchNet-Extended**: 1000 random functions per language with synthetic unit tests.  
2. **LeetCode-Hard (2025 snapshot)**: 300 tasks unseen during pre-training.  
3. **Smart-Contracts (SB-SC-Bench)**: 120 Solidity bugs + echidna fuzz tests.

### 5.2 Baselines
* Plain ChatGPT-4o zero-shot.  
* ReAct (Chen & Bubeck 2023).  
* ToolFormer-style API calling.  
* Ours w/o state compression, w/o incremental exec, etc.

### 5.3 Metrics
| Category | Metric | Target | Note |
|----------|--------|--------|------|
| Correctness | Unit-test pass rate | +7 pp over ReAct | primary |
| Efficiency | Median wall-clock / task | −25 % vs ReAct | secondary |
| Token Usage | #tokens per solved task | −20 % | tertiary |
| Compute | TPU-v5 time / training step | ≤1.0× Transformer | GSS claim |

### 5.4 Ablation Grid
1. Beam sizes ∈ {1,4,8}.  
2. Pointer-compression on/off.  
3. Incremental harness on/off.  
4. GSS vs vanilla Transformer.

### 5.5 Statistical Tests
* Wilcoxon signed-rank over paired tasks (α = 0.01).  
* Bootstrap CI (1 k reps) on pass-rate deltas.

---

## 6 Speculative Extensions (flagged as high-uncertainty)

1. **Reinforcement Learning from Incremental Feedback (RLiF)**:  Reward dense intermediate “distance-to-passing”; train a policy head to propose high-value actions, bypassing random beam exploration.
2. **Petri-Net Coverage Heuristic**:  Treat each AST node as a “place”, generation steps as transitions; guide exploration toward uncovered places → diversity.
3. **Neural-Guided Pop-Limit Tuning**:  Predict optimal cube-pruning pop-limit per task (analogy to Moses 11 % speedup).
4. **Cross-Repo State Reuse in CI/CD**:  Share State-Bank across microservices; if two repos import the same library version, reuse compilation & test traces.
5. **Federated State-Banks**:  Privacy-preserving swap of hashed embeddings among organisations, accelerating convergence while keeping code local.

---

## 7 Conclusions
Leveraging **state-space research from SMT, Petri nets and model checking**, plus **GSS hybrid LLM architectures**, we outline a comprehensive Chain-of-State code-generation framework that:

* Cuts search cost via *pointer-based left-state minimisation* (3–11 % CPU analogy),
* Handles **long prompt histories** efficiently with *GSS + local attention*,
* Reuses execution artefacts to replicate **42 % median speed-ups** from incremental model checking,
* Benchmarks on **CodeSearchNet-Extended, LeetCode-Hard, and smart contracts**, and
* Offers an *end-to-end path* to higher correctness with less human effort.

Future work includes RL fine-tuning, Petri-net-guided diversity, and federated State-Banks.  Collectively, these steps push iterative LLM coding closer to *industrial-grade autonomous programming*.


## Sources

- http://www.mt-archive.info/IWSLT-2011-Federico.pdf
- https://hal.archives-ouvertes.fr/hal-01450658
- http://www.mt-archive.info/IWSLT-2011-Heafield.pdf
- http://scholarbank.nus.edu.sg/handle/10635/43181
- http://faculty.salisbury.edu/~stlauterburg/publications/lauterburg-icse08.pdf
- https://www.open-access.bcu.ac.uk/16136/
- https://scholarworks.umass.edu/dissertations/AAI3193914
- https://zenodo.org/record/7908468
- http://people.csail.mit.edu/jrg/2008/paul-interspeech08.pdf
- https://research.tue.nl/en/publications/26b78994-a469-4be7-b769-2c3bdab51f4a
- https://asimod.informatik.tu-muenchen.de/2005/abstracts/Esparza_05.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.3256
- http://static.googleusercontent.com/media/research.google.com/en/us/pubs/archive/41880.pdf
- https://ojs.aaai.org/index.php/SOCS/article/view/18189
- http://hdl.handle.net/2142/81835
- http://berlin.csie.ntnu.edu.tw/Berlin_Research/Talks/20071018-NTNU-LVCSR.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.4619
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.51.33
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.2492
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.4806
- https://doaj.org/toc/1932-6203
- http://hdl.handle.net/2440/29485
- https://zenodo.org/record/8012171
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.4271
- http://www.cs.york.ac.uk/rts/docs/SIGDA-Compendium-1994-2004/papers/1999/date99/pdffiles/09c_3.pdf
- http://hdl.handle.net/10.1371/journal.pcbi.1006316.g004
- http://hdl.handle.net/2142/11386
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.1073
- https://ojs.aaai.org/index.php/AAAI/article/view/4555
- https://spectrum.library.concordia.ca/id/eprint/988393/
- http://arxiv.org/abs/2206.13947