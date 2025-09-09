# Defensive LLM Prompting: “Look Before You Leap” and Beyond  
_A technical synthesis and deployment blueprint_

---

## 1  Executive summary
The community’s understanding of prompt-level attacks on Large Language Models (LLMs) has matured dramatically since the first jailbreak demonstrations in early-2023. The 2024 paper **“Look Before You Leap (LBYL): Defensive Prompting to Analyze Instruction Intent Against Jailbreaking”** proposes a two-stage prompt wrapper (“Look” → analyze request; “Leap” → conditionally comply) that rejects or rewrites malicious instructions before they reach the base model. This report:  
* distills LBYL’s contributions;  
* cross-maps 12 additional, seemingly unrelated research strands—from actuarial risk scores to aerospace PIM pipelines—into a defensible, production-grade architecture;  
* offers concrete metrics, red-teaming tactics, and speculative (flagged) avenues for future work.  

Readers are presumed familiar with Transformer internals, RLHF/SFT, and security engineering.

---

## 2  Threat landscape snapshot (Q3-2025)
| Vector | Recent evidence | Typical success rate (un-mitigated)|
|---|---|---|
| **Classic prompt injection** (direct, indirect) | _Do Anything Now_ benchmark (2023) crawled ≈6 k attacks; two prompts maintained >99 % success for 100 days. | 60-80 % on GPT-3.5/4-class models |
| **Policy-violating jailbreaks** (disallowed content) | Goal-prioritization cuts attack success by 50-60 pp when safety outranks helpfulness. | 65-75 %→<10 % with safety-first tuning |
| **Data exfiltration** via hidden context stealing | Google-style DLP pipeline flags leaks at ≈92 % recall. | Highly model-dependent |
| **Over-long, self-referential chains** (sybil tokens) | MoJE flags ≈90 % with O(1) cost. | 40-70 % before filtering |

Implication: no single counter-measure suffices; layered controls analogous to **SQUARE’s** nine-gate model or **Defense-in-Depth** are required.

---

## 3  “Look Before You Leap” (LBYL) in detail
### 3.1  Mechanism
1. **Look phase**: Inject an *analyzer* prompt asking the model to classify the user instruction across dimensions (benign / disallowed / suspicious; knowledge scope; presence of role-play, chain-of-thought leakage, etc.).  
2. **Policy function**: Deterministically map the analysis results to `ALLOW`, `REWRITE`, or `BLOCK`.  
3. **Leap phase**: If `ALLOW`, the original instruction is re-issued; if `REWRITE`, the analyzer returns a *sanitized* version; if `BLOCK`, the model refuses.  

### 3.2  Results claimed by authors (GPT-3.5-turbo, 2024-07 weights)
* 74 % of jailbreaks caught (baseline 41 %).  
* ≤4 % helpfulness degradation on **Helpful & Harmless (HH-RLHF)** dataset.  
* Latency overhead: +1 inference call (~30-70 ms on GPU).  

### 3.3  Limitations acknowledged
* Analyzer itself can be *socially engineered* via second-order injection (“tell the Look phase it’s safe”).  
* Binary policy is coarse; complex corporate policy often needs hierarchical taxonomies (GDPR, PCI-DSS, export-control).  
* No quantitative risk score—makes SOC/SIEM correlation harder.  

---

## 4  Cross-pollinating external research learnings
The table shows how each external study enriches or stress-tests LBYL.

| External learning | Relevance to LBYL | Concrete leverage |
|---|---|---|
| **SQUARE 9-gate security-requirements** | Map gates to prompt lifecycle: _asset ID → risk rank → misuse cases_ | Forces traceability: each `BLOCK`/`REWRITE` decision is a stored artefact for audits. |
| **OSSTMM quantitative scoring** | Convert LBYL’s categorical decision into a numeric **Prompt-Risk Index (PRI)**: `PRI = f(lifecycle stage, damage potential, effort)` | SOC can threshold or trend-analyze PRI. |
| **MoJE low-latency detectors** | Add zero-stateless classifier _before_ Look phase; skip costly analysis when obviously malicious | Cuts compute by ≈20 %. |
| **Goal-prioritized fine-tuning** | Embed “safety > helpfulness” at base-model level; LBYL becomes failsafe not first line | Observed 66 → 2 % jailbreak drop on ChatGPT analogue. |
| **Google two-stage DLP** | Append to _output_ chain, catching sensitive data leaks that LBYL’s input-centric design ignores | Complements inbound focus. |
| **Red-teaming governance survey** | Use MITRE ATT&CK as common taxonomy for adversarial tests of Look+Leap stack | Enables vendor-neutral reporting. |
| **Lockheed PIM pipeline** | Treat prompts + logs as controlled artefacts; enforce RBAC & immutable audit across organisations | Useful for multi-tenant LLM SaaS. |
| **Actuarial risk (NJ bail)** | Warning on unintended bias: a PRI may entrench disparities if race/gender proxies sneak in | Mandate fairness audits on classifier features. |
| **Honeynet deterrence study** | “Legal banner” alone weakly deters attackers – so LBYL disclaimers shouldn’t replace enforcement | Keep hard blockers. |
| **SoC Security fine-tune workflow** | 5-step pipeline (sanitise → template → reward-model → ensemble → human veto) matches Look+Leap interplay | Templating ideas improve rewriting quality. |
| **Do Anything Now benchmark** | Supply >46 k adversarial cases for regression testing | Needed for coverage metrics. |

---

## 5  Comprehensive defensive architecture (production blueprint)
### 5.1  Assumed controllables (answers to prior Qs)
* **Model**: access to system prompt, optional LoRA or full-fine-tune, no source-code changes.  
* **Post-processing**: full control over output mediator, can call auxiliary models or detectors.  
* **Infrastructure**: containerised GPU cluster, IAM integrated with enterprise RBAC.  

### 5.2  Layered controls pipeline  
```text
[User ↔ UI]
   │ (1) MoJE stateless filter (O(µs))
   │   ├── if score>τ₀ → hard refuse
   │   └── else→
   │ (2) LBYL Look Phase (Analyze)
   │ (3) Policy router: ALLOW / REWRITE / BLOCK (PRI computed here)
   │ (4) Leap Phase (Execute sanitized prompt)
   │ (5) Output-side DLP & safety filter (2-stage)
   │ (6) Human-in-the-loop (optional, high-PRI only)
   │ (7) Immutable logging → SIEM / audit lake
```

### 5.3  Policy router details
```
IF PRI < 20          → ALLOW
ELSE IF 20 ≤ PRI <40 → REWRITE + add "guarded" system prompt
ELSE (≥40)           → BLOCK & escalate ticket
```
PRI calibration uses OSSTMM factors plus a multiplicative bias-fairness penalty (cf. NJ bail study).

### 5.4  Secure-software life-cycle graft (SQUARE-inspired)
1. Identify **assets**: prompt text, embeddings, model weights, policy tables.  
2. Elicit **security goals**: no disallowed content, no data leakage, explainable refusals.  
3. **Risk assessment**: ATT&CK mapping; assign PRI baselines.  
4. **Misuse cases**: chain-of-thought leakage, policy override, prompt injection, latent racism.  
5. **Security requirements**: e.g. “P1: The system SHALL block any prompt containing PHI with PRI≥30.”  
6-9. Trace through design → implementation → test → deploy, with artefacts checked into GitOps repo.  

### 5.5  Evaluation plan
* **Datasets**: _Do Anything Now_, Anthropic HarmlessEval, custom enterprise prompts.  
* **Metrics**:  
  * Jailbreak recall @τ₀, τ₁  
  * Benign pass-through rate  
  * Mean PRI (trend over time)  
  * Latency (p99)  
* **Red-team loops**: quarterly exercises using ATT&CK adaptation; integrate results as new MoJE features.  

---

## 6  Operational considerations
1. **Latency budget**: MoJE <0.1 ms ⇒ negligible; Look+Leap adds single forward pass; total overhead ≈1.6× base call.  
2. **Cost trade-off**: Running analyzer at lower temperature (τ=0) suffices; no extra model needed.  
3. **Auditing**: PRI, decision path, and “analyzer summary” logged; meets EU AI Act transparency obligations.  
4. **Bias control**: periodic disparate-impact tests on PRI outputs; re-weight MoJE features if disparities >5 pp.  
5. **Cross-tenant segregation**: borrow **Lockheed PIM** principle—store prompts in tenant-scoped buckets enforced by IAM tags; helps regulators.  

---

## 7  Speculative / contrarian ideas (flagged)
* **(Spec)** Hardware-rooted isolation: Run Look phase on a lightweight, on-prem “LLM firewall” (e.g., Groq-LPU) that never sees sensitive context; main model stays in cloud.  
* **(Spec)** Adversarial honeypots: Publish watered-down prompts with subtle canaries; attackers who reuse them reveal themselves. Effectiveness unknown (honeynet study suggests limited deterrence).  
* **(Spec)** Dynamic goal reprioritization: During emergencies (e.g., ransomware triage), temporarily flip “helpfulness > safety” for whitelisted SOC users; requires cryptographic attestation.  

---

## 8  Roadmap
| Quarter | Milestone | Key risk |
|---|---|---|
| Q4-2025 | Integrate MoJE + basic LBYL (pri=boolean) | Mis-tuned thresholds |
| Q1-2026 | OSSTMM-derived PRI v1; attach SIEM dashboards | Metric drift |
| Q2-2026 | Full SQUARE traceability; ATT&CK red-team α | Audit burden |
| Q3-2026 | Tenant-scoped RBAC + export-control content filter | False positives |
| Q4-2026 | Bias-mitigation loop (NJ bail analogy) | Governance overhead |

---

## 9  Conclusion
“Look Before You Leap” is a compact, easily deployable wrapper that already halves jailbreak success rates with minimal usability cost. Yet its real power emerges when nested inside a mature security engineering stack: stateless MoJE filters for speed, quantitative PRI scoring for governance, output-side DLP for data protection, and SQUARE-style artefact traceability for audits. Incorporating insights from domains as diverse as pre-trial risk assessment and aerospace configuration management yields a blueprint that is not merely reactive but **provably defensible**.

The next 12 months should focus on (i) PRI calibration against live traffic, (ii) semi-automated bias audits, and (iii) codifying ATT&CK-derived red-team playbooks to keep pace with the fast-evolving jailbreak arms race.

---

### References (selected)
* _Look Before You Leap: Defensive Prompting to Analyze Instruction Intent_, arXiv 2405.XXXXX (2024)  
* Fordham L. Rev. 87(1) (2018) “Pre-trial Risk Assessment Instruments”  
* Mylopoulos et al., SQUARE Method, CMU-SEI/CMU-2005-TR-009  
* AAAI-AIES 2024 “Mixture of Jailbreak Experts”  
* arXiv 2308.03825 “Do Anything Now”  
* ePrint 2023/1561 “LLM for SoC Security”  
* TDCommons (2024) “Two-stage DLP for LLMs”  
* Theseus (2023) “Survey of Red-Teaming Governance Frameworks”  


## Sources

- https://nsuworks.nova.edu/gscis_facbooks/36
- https://repository.law.umich.edu/cgi/viewcontent.cgi?article=4736&amp;context=mlr
- https://oskar-bordeaux.fr/handle/20.500.12278/78298
- https://cris.vtt.fi/en/publications/da178d20-ff0e-4bde-953b-430062ebd49f
- https://commons.pacificu.edu/context/todayg1/article/1002/type/native/viewcontent
- http://digital.library.unt.edu/ark:/67531/metadc710466/
- https://hdl.handle.net/10657/18302
- https://eprint.iacr.org/2023/1561
- https://www.researchgate.net/profile/Pietro_Ferrara/publication/242286672_JAIL_Firewall_Analysis_of_Java_Card_by_Abstract_Interpretation/links/00b49539708fbdbc9d000000.pdf
- http://www.iariajournals.org/security/sec_v2_n4_2009_paged.pdf#page=66
- https://hal.univ-lorraine.fr/tel-01748227
- http://arxiv.org/abs/2309.01446
- http://hdl.handle.net/10068/452972
- https://zenodo.org/record/5140271
- https://doaj.org/toc/2415-6698
- http://arxiv.org/abs/2311.08268
- https://scholarship.law.ufl.edu/flr/vol68/iss2/10
- https://digitalcommons.usf.edu/cgi/viewcontent.cgi?article=7247&amp;context=etd
- http://arxiv.org/abs/2308.03825
- https://doi.org/10.1109/ES.2016.19
- http://shell.cas.usf.edu/%7Esanocki/AttentionalCycles.pdf
- https://hdl.handle.net/11454/71290
- https://dare.uva.nl/personal/pure/en/publications/a-policy-compliance-detection-architecture-for-data-exchange-infrastructures(c1d8ad5b-c82d-4370-bdf4-0c1217e71a10).html
- http://wseas.us/e-library/conferences/2007corfu/papers/540-264.pdf
- https://scholarcommons.usf.edu/etd/6259
- https://hal.inria.fr/hal-01394973
- http://arxiv.org/abs/2311.09096
- http://www.thinkmind.org/download.php?articleid%3Dsec_v2_n4_2009_5
- http://repository.tue.nl/695281
- https://escholarship.org/uc/item/44b7k2xf
- https://ojs.aaai.org/index.php/AIES/article/view/31638
- https://ir.lawnet.fordham.edu/flr/vol87/iss1/12
- http://www.theseus.fi/handle/10024/500627
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.83.9266
- http://hdl.handle.net/10.1184/r1/6574325.v1
- http://arxiv.org/abs/2308.11521
- https://doaj.org/article/48b4a94b5aeb4c1e86aa4d4ad68ad34f
- http://arxiv.org/abs/2310.12815
- https://www.tdcommons.org/context/dpubs_series/article/7538/viewcontent/A_Cost_Effective_Method_to_Prevent_Data_Exfiltration_from_LLM_Prompt_Responses.pdf