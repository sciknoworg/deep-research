# Chain-of-State Iterative Code Generation via Large Language Models 

*An integrated research blueprint spanning LLM prompting, parameter-efficient fine-tuning, automated verification, CI/CD, and state-space analytics*

---

## 1. Executive Summary

Chain-of-state (CoS) prompting extends chain-of-thought by letting an LLM **materialise an explicit, mutable program state** (variables, files, API calls, DB rows, container images, CI artefacts, etc.) at each reasoning step. The LLM alternates between (i) *thought* tokens that decide what to do next and (ii) *state-edit* tokens that mutate the artefact under construction. This report synthesises ~100 distinct research findings (see Appendix A for mapping) into a *three-pillar plan*:

1. **Model Adaptation Layer** — leverage Parameter-Efficient Fine-Tuning (PEFT: LoRA, adapters, PALP) on open 2-to-9 B models (Llama-2/3-7B, Mistral-7B, Phi-3.5, Gemma-2–9 B). Combine *prompt-time* CoS scaffolding with *delta-tuned* weights that reward correct multi-step state manipulations.
2. **Automated Verification & Feedback Loop** — embed compositional model checkers (Storm 1.6.4, LTSmin, JPF Δ-execution) and lightweight runtime oracles (pytest, node-tap, selective mutation, DCI) to judge each intermediate state. Verification signals are fed back to the LLM either as additional context (`[FAIL step-id …]`) or as a reinforcement learning (RLHF / RLAIF) reward.
3. **Continuous Delivery Harness** — implement an Argo Workflows + ArgoCD-based pull pipeline on Kubernetes with autoscaling GitHub runners. The harness (a) executes generation/evaluation at scale, (b) mines empirical signals (latency, pass@k, cost, commit survivability), and (c) stores full state traces for offline state-space analytics.

The goal is **end-to-end reproducibility**: every generated codebase, state trace, verification artefact, and CI log is stored so that incremental re-runs reuse prior results and avoid quadratic explosion.

---

## 2. Background & Motivation

### 2.1 Why Chain-of-State?

Classic benchmarks (HumanEval, MBPP) are *stateless*: they measure single-function correctness and hence over-estimate LLM capability (Codex hits >80 % statement coverage there yet <2 % on real projects). Real-world tasks—full-stack apps, data pipelines, embedded firmware, microservices—require **mutable global state and long-horizon reasoning**. CoS explicitly surfaces that state in the prompt, allowing:

* **Fine-grained feedback**: verification oracles can point to the exact state step that broke.
* **Iterative repair**: the LLM need not regenerate from scratch; it patches the live artefact (cf. Lauterburg ’08 incremental exploration, Delta Execution JPF, Offline Delta Propagation for EMF).
* **Reusability**: previously explored states can be cached and skipped (Incremental SSE sped up 22/24 runs by median 42 %).

### 2.2 Terminology

```
[thought]   # English reasoning
[state]     # JSON/patch/SQL/file system diff
[oracle]    # external verifier result
```

A **CoS trace** is a sequence `(thought_i, state_i, oracle_i)`; success is `oracle_n = ✓`.

---

## 3. Related Work Synopsis

| Theme | Key Findings & Papers |
|-------|-----------------------|
| Scratch-pad prompting | ReAct, Program-Aided-RL; but no persistent external state. |
| PEFT for code | ICSE’24 *No More ICL?* → LoRA/adapters beat 32-shot ICL on 12-language unseen set while touching only ≈1-3 % params. |
| Incremental verification | Lauterburg ’08, Delta Execution, Offline DI delta propagation, LTSmin parallel CNDFS, Storm 1.6.4 Spot integration. |
| CI/CD research | Argo pull style fastest & safest; autoscaling runners robust; social impact (CI reduces PR discussion length). |
| Mutation & assertion amplification | Selective AV/Relational mutation (80 % effort cut, 83 % fault detection); DCI auto-amplification; OPi+ full-history mutation in CI. |
| Model-checking at scale | CADP Grid’5000, PReach 90 B states, BSP protocol models, parametric & multi-objective MC in Storm. |
| Datasets beyond HumanEval | CodeContests, SF110, SStuBs, Feature-Revision corpus, 400+ TACAS artefacts, CoqCryptoLine. |
| Formal refinement w/ LLM | Refine4LLM loop beats prior program-refinement baselines. |

---

## 4. System Architecture Proposal

### 4.1 High-Level Diagram

```
┌──────────┐   prompts   ┌───────────────┐   patches   ┌─────────────┐
│  LLM +   │───────────▶│   CoS Agent    │───────────▶│  Code Base  │
│  PEFT    │◀───────────│(state manager) │◀───────────│ (git repo)  │
└──────────┘   signal    └──────┬────────┘   events    └─────┬───────┘
                               ▼                          ▼
                          ┌─────────┐                ┌────────────┐
                          │ Oracle  │ test / MC      │ CI Runner  │
                          │  Farm   │──────────────▶ │  (Argo)    │
                          └─────────┘  verdict        └────────────┘
```

* **CoS Agent** stores the *authoritative* state as a Git repo plus an in-memory cache of structured artefacts (AST, IR, DB schema…).
* **Oracle Farm** is a heterogeneous pool: pytest + coverage, Storm model checker invocations, mutation analysis, runtime property monitors.
* **CI Runner Harness** triggers Argo Workflows inside a pull-style pipeline; logs are persisted in MinIO / S3.

### 4.2 Data-flow & Caching Strategies

1. **State Snapshotting** — every `state_i` is a *Git commit* labelled with `<run-id, step-i>`.
2. **Incremental Verification Re-use** — each oracle maintains a cache keyed by `(tool-version, commit-hash, config-hash)`. Lauterburg ’08 & Delta Execution show 6×–126× reuse speed-ups.
3. **Delta-based Fine-Tuning** — failed traces are distilled into `(prompt, correct_patch)` pairs. Via LoRA we periodically update the base model with only 0.1-2 % new parameters.

### 4.3 Security & Compliance

* Pull pipeline keeps kube-configs in-cluster; push pipelines do not (Umeå study).
* Use ChoEn (Bologna) for BPMN→Ethereum translation if decentralised compliance proofs are needed.
* AES-CTR/GCM constant-time libraries (~7.6 cycles/byte) are recommended for encryption of artefact caches.

---

## 5. Dataset & Benchmark Suite

| Category | Dataset | Rationale |
|----------|---------|-----------|
| Stateless baseline | HumanEval+/MBPP | sanity check & comparability. |
| Stateful algorithmic | SF110, CodeContests | richer heap & I/O. |
| Real project histories | 500-repo mining, LISA 1.1 M revs, Feature-Revision corpus, SStuBs, OPi+ mutation traces | test long-horizon CoS repair. |
| Formal models | 400 TACAS artefacts, i-Protocol livelock, Storm/JANI parametric models | stress formal oracle pipeline. |
| Proof corpora | CoqCryptoLine, CompCert QuickChick | evaluate CoS in proof repair domain. |

For each, we pre-compute *ground-truth oracles* (unit tests, model properties, proof goals). All artefacts live in a *monorepo* to enable cross-dataset caching.

---

## 6. Model Adaptation Plan

1. **Base checkpoint selection** — choose 7-9 B open-weights Llama-3-8B-Instruct + Mistral-7B. They have strong code pre-training and fit on a single A100/80 GB with 4-bit QLoRA.
2. **Prompt Engineering** —
```
You are CoS-GPT. Maintain a JSON object `state`. After thinking, output either
 1. <patch> … </patch>   # git-style unified diff
 2. <stop />             # when tests pass
```
3. **Instruction SFT** — seed with ∼5 k synthetic CoS traces: generate a small buggy repo, record human-written multi-step fixes, log oracles.
4. **LoRA Fine-Tuning** — 8-rank adapters on Wq, Vq, out-proj; α=32; dropout 0.05. The 2024 comparative PEFT study showed negligible loss.
5. **PALP Linear-Head** — for languages or domains lacking enough SFT data (e.g., COBOL), freeze base model, train a linear probe on prompt embeddings to choose high-level CoS actions.

---

## 7. Automated Verification Layer

### 7.1 Static & Symbolic

* **Storm 1.6.4** for LTL/steady-state/expected-reward properties; parametric via storm-pars if unbounded int arrays appear.
* **LTSmin CNDFS** for multi-core liveness; shorter counter-examples aid prompt feedback.
* **Java PathFinder + Delta Execution** for object-oriented subjects; 1.06×–126× speed-ups expected.
* **Model-Based Testing** — integrate Testing Automata (single-pass liveness, stuttering-insensitive) to cut double searches.

### 7.2 Dynamic & Mutation-based

* **Selective Mutation (AV & Relational ops)** — 80 % effort cut vs full set, still 83 % fault exposure.
* **DCI Assertion Amplification** — auto-generates new asserts around modified lines; succeeded in 15 % of commits with coverage.
* **OPi+ Continuous Mutation** — run on each CoS patch to give real-time “mutation score” feedback.

### 7.3 Proof Repair Oracles

Leverage **iCoq / piCoq** to regression-check Coq proofs in parallel; 10×-28× speed-ups keep them CI-friendly.

---

## 8. CI/CD & Infrastructure Blueprint

| Layer | Technology | Justification |
|-------|------------|---------------|
| Cluster | k8s on managed cloud (GKE/EKS) | proven autoscaling runner pattern. |
| Pipeline | Argo Workflows + ArgoCD (pull) | fastest & most fault-tolerant; secures kube-config. |
| Runners | GitHub Actions self-hosted in cluster; Linköping study shows autoscaling best robustness. |
| Storage | MinIO S3 + CephFS | versioned, encrypted via constant-time AES GCM. |
| Observability | Prometheus, Grafana, Loki | pipeline latency, oracle runtime, GPU utilisation. |
| Cost control | Vertical Pod Autoscaler + Storm’s JSON export to track analysis time. |

*Bulk-Synchronous Parallel* state-space tasks run as Argo DAG nodes with per-tool sidecars.

---

## 9. Experimental Protocol

### 9.1 Metrics

* **pass@k** (k ∈ {1,5,10}) — test oracles.
* **oracle-latency** — median runtime per state.
* **repair-depth** — # CoS steps until success.
* **resource cost** — GPU hours + CPU core-seconds.
* **human-effort proxy** — # manual reviews on failing traces.
* **CI social signals** — PR comment length (post-CI integration tends to shrink).

### 9.2 Ablations

1. Prompt-only vs Prompt + LoRA (expect LoRA > PALP > ICL).
2. Stateless vs Stateful tasks (highlight CoS gains on the latter).
3. Verification reuse ON/OFF (quantify Delta Execution/Incremental SSE speed-ups).
4. Mutation oracle inclusion ON/OFF (measure added fault detection).

### 9.3 Statistical Power

* ≥50 tasks × 5 seeds ⇒ 250 runs per condition.
* Accept 95 % CI width ≤ ±3 % on pass@k.
* Use blocked bootstrap by dataset to handle heterogeneity.

---

## 10. Scalability & Performance Tactics

* **Compositional reductions** (Storm, logic-based spec layer) shrink large reward models.
* **BSP state construction** specialised for security protocols outperforms generic BSP; adopt for i-Protocol, Pastry traces.
* **State compression** — LTSmin symbolic BDD + Sylvan for 48 core scaling.
* **Disk-backed sparse matrices** (PARSECS) for >100 M states.
* **Cache invalidation policy** — LRU per-tool, but keep hot states around release spikes (GitHub mining shows activity spikes near releases).

---

## 11. Risk Register & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| GPU supply shortage | medium | high | QLoRA / 4-bit; fall back to PALP (CPU-friendly). |
| Oracle false positives (mutation survivability) | medium | medium | Triangulate across oracles; require consensus ≥2. |
| State-space explosion | high | high | Incremental reuse + compositional reduction + specialised BSP. |
| CI cost overrun | medium | high | Vertical Pod Autoscaler; LoRA reduces iteration time. |
| Security breach (push credentials) | low | high | Pull pipeline only; secret management via Vault. |

---

## 12. Future & Speculative Directions

* **Refine4LLM Integration** — formal refinement laws as *thought prompts* → may teach the LLM provably correct transformation sequences.
* **Choreographic CI** — generate the entire Argo workflow via the reversible choreography language (Zenodo 2019) for automatic flaky-test isolation.
* **Smart-contract Enforcement** — compile BPMN choreographies of the pipeline into Ethereum smart contracts (ChoEn) for tamper-evident compliance.
* **Speech-based CoS** — a warm-up pre-training step enables speech LMs to perform ICL; research whether spoken natural-language planning benefits CoS tools.
* **Hardware acceleration** — bitsliced AES/GCM primitives for encrypted caches; offload model-checking BDD operations to GPU (Sylvan-CUDA prototype, speculative).

---

## 13. Conclusion

Chain-of-state code generation is **ripe for industrial-grade evaluation**. By marrying PEFT-adapted LLMs with incremental verification, mutation analysis, and a Kubernetes-native CI harness, we can measure—and systematically improve—an LLM’s ability to *think, act, verify, and repair over long horizons*. The architecture explicitly tackles state-space explosion, CI cost, and security, leveraging dozens of empirical findings: pull pipelines excel, selective mutation is cheap yet potent, LoRA beats ICL at a fraction of GPU usage, and state caching yields double-digit speed-ups.

If executed as laid out, the project will deliver:

1. A **public benchmark suite** covering stateless and stateful tasks with ground-truth oracles.
2. A **reproducible pipeline** whose every component—from LLM adapters to TACAS models—is open-sourced and version-pinned.
3. Quantitative evidence on how CoS + PEFT + verification closes the gap between prototype demos and production-quality code generation.

---

### Appendix A. Traceability Matrix (Learning → Section)

(Only the first few shown for brevity; full 100-item mapping attached in repository.)

| Learning bullet | Where applied |
|-----------------|--------------|
| GitHub release spikes | §7 cache policy |
| Logic-based spec layer | §7.1 compositional reduction |
| Lauterburg Incremental SSE | §4.2, §9.2 |
| Argo pull vs push | §4.3, §8 |
| DCI | §7.2 |
| Offline DI delta propagation | §4.2 |
| 2024 PEFT study | §6 |
| Storm 1.6.4 Spot | §7.1 |
| BSP specialised | §10 |
| Selective mutation | §7.2 |
| Codex coverage gap | §2.1, §5 |
| … | … |


## Sources

- http://bvasiles.github.io/papers/era14.pdf
- https://hal.science/hal-03185848
- http://hdl.handle.net/2381/12547244.v2
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.1073
- http://repository.tue.nl/893366
- https://hal.inria.fr/hal-00730668
- https://zenodo.org/record/7865692
- http://www.ylies.fr/wp-content/uploads/2015/07/crv15.pdf
- https://zenodo.org/record/8286531
- https://openresearch.surrey.ac.uk/esploro/outputs/doctoral/Distributed-Choreography-A-Framework-to-Support/99512446002346
- http://www.cs.york.ac.uk/rts/docs/EMSOFT-2004-2005/docs05/p343.pdf
- http://urn.fi/URN:NBN:fi:oulu-201805091678
- https://research.utwente.nl/en/publications/concurrent-algorithms-and-data-structures-for-model-checking(b6e8a1c5-9ba1-4f85-83d0-df645ad42b1f).html
- https://zenodo.org/record/3263870
- http://www.wseas.us/e-library/conferences/austria2004/papers/482-327.pdf
- http://arxiv.org/abs/2205.06381
- https://ueaeprints.uea.ac.uk/id/eprint/73712/
- https://zenodo.org/record/7874637
- http://www.lrec-conf.org/proceedings/lrec2004/pdf/3.pdf
- http://arxiv.org/abs/2205.11166
- https://hdl.handle.net/11566/321231
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Toward-efficient-protocol-design-through-protocol/99511757202346
- https://research.utwente.nl/en/publications/testing-timed-automata(d8de401a-f259-4656-ba6a-b430ef80017d).html
- http://hdl.handle.net/2286/R.I.56100
- http://homes.cs.washington.edu/%7Emernst/pubs/oo-test-gen-tr056.pdf
- https://zenodo.org/record/4021127
- https://aaltodoc.aalto.fi/handle/123456789/38991
- http://www.cs.umd.edu/~atif/zeller.pdf
- https://ir.library.carleton.ca/pub/16063
- http://arxiv.org/abs/2212.10873
- https://zenodo.org/record/1432789
- https://zenodo.org/record/8191801
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.9830
- https://biblio.ugent.be/publication/944052/file/1139601
- https://zenodo.org/record/7559277
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.9977
- http://hdl.handle.net/2381/43725
- https://hal.inria.fr/hal-01882413/file/rv18-invited.pdf
- https://doi.org/10.1109/EASe.2011.16
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066104804110/MAIN/application/pdf/9187722eb620c8017590ddcb8481e679/main.pdf
- https://zenodo.org/record/7509474
- http://sdiwc.net/digital-library/web-admin/upload-pdf/00001653.pdf
- http://faculty.salisbury.edu/~stlauterburg/publications/lauterburg-icse08.pdf
- https://zenodo.org/record/8201529
- http://arxiv.org/abs/2310.12477
- https://research.tue.nl/nl/publications/e399a742-7cd0-4c21-9463-99afbe9ee5af
- https://hdl.handle.net/1721.1/122047
- http://repository.tue.nl/880711
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.4310
- http://hdl.handle.net/2117/174561
- http://urn.kb.se/resolve?urn=urn:nbn:se:his:diva-6569
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Lochau=3AMalte=3A=3A.html
- http://hdl.handle.net/2066/113779
- https://zenodo.org/record/7881403
- https://doaj.org/toc/1875-9203
- https://ir.library.carleton.ca/pub/22392
- https://www.doria.fi/handle/10024/187916
- http://classes.soe.ucsc.edu/cmps203/Fall05/sample-kristal-final.pdf
- http://groups.csail.mit.edu/tds/papers/Gawlick/journal.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-108379
- http://hdl.handle.net/10356/78364
- https://research.sabanciuniv.edu/id/eprint/42658/1/Yang2021_Article_WhereWereTheRepairIngredientsF.pdf
- https://ir.cwi.nl/pub/21858
- http://hdl.handle.net/10.1371/journal.pone.0288060.t007
- https://hal.archives-ouvertes.fr/hal-00745201
- http://oai.cwi.nl/oai/asset/21227/21227B.pdf
- http://people.csail.mit.edu/jrg/2008/paul-interspeech08.pdf
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/165652
- https://ojs.aaai.org/index.php/AAAI/article/view/26495
- http://eprints.iisc.ac.in/8611/
- https://pub.uni-bielefeld.de/download/2919994/2919995
- https://zenodo.org/record/1288600
- https://hal.inria.fr/hal-01367307/file/NPZ12a.pdf
- http://www.theseus.fi/handle/10024/502189
- https://zenodo.org/record/2606632
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.6923
- https://hdl.handle.net/2152/119143
- http://www.macesystems.org/papers/MaceMC_TR.pdf
- http://repository.tue.nl/916246
- https://figshare.com/articles/Code_Coverage_and_Continuous_Integration/6465047
- http://www.cs.gmu.edu/~offutt/rsrch/papers/SDL-CProteum-ICST2014.pdf
- http://hdl.handle.net/11585/66616
- http://resolver.tudelft.nl/uuid:562de17a-2a9d-479d-b7a2-d85b37e9543a
- http://hdl.handle.net/10344/4012
- https://hdl.handle.net/10072/435175
- https://www.open-access.bcu.ac.uk/16136/
- https://zenodo.org/record/6363556
- http://hdl.handle.net/2117/372818
- https://hal.inria.fr/hal-03592675v2/file/main.pdf
- https://hal.inria.fr/hal-00664236/document
- https://eprints.lancs.ac.uk/id/eprint/186158/
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S0304397599001346/MAIN/application/pdf/a3a8ffd11ce66e65753ceb7613b78783/main.pdf
- http://hdl.handle.net/11573/526001
- http://www.ylies.fr/wp-content/uploads/2011/09/rv14-2.pdf
- https://hal.archives-ouvertes.fr/hal-01701443
- http://hdl.handle.net/2078.1/264383
- http://hdl.handle.net/20.500.11850/498126
- https://zenodo.org/record/7765625
- https://elib.dlr.de/92693/
- http://pleuma.cc.gatech.edu/aristotle/pdffiles/p130-harrold.pdf
- https://hal.archives-ouvertes.fr/hal-01851813
- https://zenodo.org/record/4017717
- http://hdl.handle.net/10.1184/r1/6603527.v1
- https://zenodo.org/record/7875338
- http://disi.unitn.it/~bielova/papers/BIEL-MASS-SIAH-FCS_ARSPA_WITS08.pdf
- http://resolver.tudelft.nl/uuid:c085d5a9-7a11-49bd-a5d2-7d2eeec2e28e
- https://zenodo.org/record/4555199
- http://hdl.handle.net/2142/75450
- https://inria.hal.science/hal-01900195
- http://onlinelibrary.wiley.com/doi/10.1002/9781119131151.ch2/summary
- https://zenodo.org/record/4298643
- http://www.mate.tue.nl/mate/pdfs/9577.pdf
- http://ejournal.uika-bogor.ac.id/index.php/INOVA-TIF/article/view/8345
- https://calico.org/calico-conference/calico-2018
- http://arxiv.org/abs/2311.08993
- https://hal.inria.fr/hal-00806788
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.9707
- http://hdl.handle.net/20.500.11850/585331
- https://zenodo.org/record/7309036
- http://hdl.handle.net/1911/104217
- https://inria.hal.science/hal-03121735
- http://es.cs.uni-kl.de/publications/datarsg/ARSS97.pdf
- https://zenodo.org/record/1183244
- https://hal.inria.fr/hal-01432931
- https://shmpublisher.com/index.php/joscex/article/view/274
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-142506
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.2492
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Steinh=F6fel=3ADominic=3A=3A.html
- http://prosecco.gforge.inria.fr/personal/hritcu/talks/coq6_submission_4.pdf
- https://tel.archives-ouvertes.fr/tel-00766757
- http://hdl.handle.net/10.6084/m9.figshare.16847098.v1
- http://www.sersc.org/journals/IJMUE/vol9_no7_2014/34.pdf
- https://aisel.aisnet.org/iceb2017/14
- https://zenodo.org/record/7343828
- http://repository.tue.nl/780734
- https://zenodo.org/record/4727934
- http://hdl.handle.net/10.5281/zenodo.1413666
- https://research.utwente.nl/en/publications/distributed-diskbased-solution-of-very-large-markov-chains(2e956f97-5212-4459-9104-78a0cee3d827).html
- https://www.zora.uzh.ch/id/eprint/140446/1/alexandru-panichella-gall_code-analysis_saner17.pdf
- https://ir.library.oregonstate.edu/concern/graduate_thesis_or_dissertations/9p290g400
- http://www.ime.usp.br/%7Eemilio/publications/2014_orchor.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.92.9028
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.3872
- http://urn.kb.se/resolve?urn=urn:nbn:se:umu:diva-197216
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.1918
- http://www.theseus.fi/handle/10024/786622
- http://hdl.handle.net/2429/52670
- https://zenodo.org/record/1140261
- https://hal.inria.fr/hal-03586813
- http://resolver.tudelft.nl/uuid:ce135a31-972f-4f96-bfbb-28b813045e1b
- https://zenodo.org/record/6653291
- https://zenodo.org/record/887578
- http://fias.uni-frankfurt.de/fileadmin/fias/luecke/Publications/LCCC-BornscheinEtAl-Abstract.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.65.6972
- https://zenodo.org/record/7119067
- http://arxiv.org/abs/2206.04615
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-186054
- https://zenodo.org/record/7559208
- https://doi.org/10.7916/D81261TG
- http://hdl.handle.net/2078.1/226341
- https://zenodo.org/record/8078999
- http://ifipwg213.org/sites/flosshub.org/files/ICSME2014ERA.pdf
- https://hal.inria.fr/hal-01294167v2/file/coco-experimental-setup.pdf
- http://www.nusl.cz/ntk/nusl-300109
- https://doi.org/10.1051/e3sconf/20187313009
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.8432
- https://hal-mines-paristech.archives-ouvertes.fr/hal-02434236/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.6765
- http://www.cin.ufpe.br/~damorim/publications/tse2008.pdf
- https://research.tue.nl/en/publications/b89c7fef-6f75-44f9-86af-c568c9eb03b8
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-19313
- https://hal.science/hal-01803008
- https://repository.upenn.edu/dissertations/AAI8307327
- https://hdl.handle.net/10356/166197
- https://digitalcommons.unl.edu/computerscidiss/110
- https://zenodo.org/record/4661935
- https://zenodo.org/record/7578503
- https://digitalcommons.fiu.edu/dissertations/AAI3395789
- https://zenodo.org/record/4288652
- https://hal.science/hal-01888538/document
- http://prosecco.gforge.inria.fr/personal/hritcu/publications/verified-testing-draft.pdf
- https://zenodo.org/record/4606679
- https://www.um.edu.mt/library/oar/handle/123456789/91281
- https://ir.library.carleton.ca/pub/8234
- http://www.nusl.cz/ntk/nusl-448316
- https://www.interscience.in/cgi/viewcontent.cgi?article=1154&amp;context=ijcsi
- https://www.st.cs.uni-saarland.de/publications/files/fraser-issta-2010.pdf
- https://hdl.handle.net/2152/78259
- http://msr.uwaterloo.ca/papers/Ying.pdf
- https://zenodo.org/record/5845075
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.55.8315
- http://collaboration.csc.ncsu.edu/laurie/Papers/Mutation2007.pdf
- http://pp.info.uni-karlsruhe.de/uploads/folien/lochbihler11ded.pdf
- http://arxiv.org/pdf/1402.6478.pdf
- https://zenodo.org/record/6673741
- https://zenodo.org/record/5593568
- http://hdl.handle.net/2117/344391
- http://hdl.handle.net/11586/115495
- http://hdl.handle.net/2434/714671
- https://openresearch.surrey.ac.uk/esploro/outputs/conferencePresentation/Using-Formal-Verification-Methods-and-Tools/99514619102346
- http://hdl.handle.net/2440/29485
- https://hal.inria.fr/hal-01629288
- http://eprints.eemcs.utwente.nl/15288/01/Tre96-CTIT96-26.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.97.9710
- https://hal.archives-ouvertes.fr/hal-01198918/document
- https://figshare.com/articles/Artefact_containing_model_checker_Storm_binary_as_presented_in_the_TACAS_2018_paper_Multi-Cost_Bounded_Reachability_in_MDP_/5907349
- https://zenodo.org/record/7746646
- http://neo.lcc.uma.es/staff/francis/pdf/ChicanoAlba08scal.pdf
- http://www.loc.gov/mods/v3
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1571066113000418/MAIN/application/pdf/2b419d6b09043413d8a63baee5b68048/main.pdf
- https://zenodo.org/record/7559244
- https://zenodo.org/record/5522820
- http://resolver.tudelft.nl/uuid:c7b2c5b7-cb3d-436d-a4ec-ac4e3c0cc719
- http://eprints.eemcs.utwente.nl/6494/01/276_Tre96.pdf
- http://eden.dei.uc.pt/~pmarques/nomeacao/papers/mendes2008.pdf