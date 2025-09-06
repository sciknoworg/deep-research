# “Look Before You Leap”: A Comprehensive Report on Defensive Prompting and System-Level Guardrails Against LLM Jailbreaking  
*Date of drafting ✧ 2025-09-04*  

---

## 1  Executive Summary  
Lee et al.’s “Look Before You Leap” (LBYL) paradigm proposes that an LLM **first** analyses the *intent* of the user’s instruction under a safe, capability-constrained context and **then**—only if the intent is judged benign—**leaps** into a second stage that executes the request.  
This report fulfils the following objectives simultaneously:

1. **Critical literature survey** of defensive-prompting and complementary guardrails.  
2. **Hands-on implementation guide** with prompt templates, model-checking pipelines and code-level hooks that cover public SaaS LLMs (e.g., ChatGPT), in-house-fine-tuned transformers and domain-specific enterprise models.  
3. **Experimental-design blueprint** that quantifies jailbreak resistance, integrating recent metrics, taxonomies and red-team protocols.  

Where appropriate, we integrate *all* cross-domain research learnings that can inform the design, verification or deployment of LBYL-style defences, including federated-learning hardening, model-checking advances, real-time FPGA anomaly filters, psychometric reliability theory, 5G URLLC latency constraints, sensor-fusion decision rules, PAC-Bayesian ensemble bounds, and more.  

---

## 2  Problem Landscape: Jailbreaks Remain a Moving Target  
• **In-the-wild evidence.** The 6-month “Do Anything Now” measurement study amassed 6 387 jailbreak prompts and produced a 46 800-item benchmark across 13 forbidden scenarios; two public payloads sustain 0.99 attack success on GPT-3.5 & GPT-4 after >100 days.  
• **Reverse-tunnel attacks.** The (later-contested) “Self-Deception” work reports 86.2 % / 67 % success on GPT-3.5 / GPT-4.  
• **Community migration.** Jailbreak communities are moving from open forums to private channels, decreasing the half-life of static blacklists or pattern-based filters.  

These data points underscore three design imperatives: (i) **layered defences** rather than single-point filters; (ii) **quantitative residual-risk modelling**; (iii) **rapid update loops** resilient to concept drift.

---

## 3  Conceptual Foundations  
### 3.1  LBYL Prompt-Loyal Analogy  
The *Prompt-Loyal Strategy* in context-oriented programming (Cardozo 2011) distinguishes between **prompt-loyal (deferred) activation** and **prompt (immediate) activation** of behavioural contexts. LBYL is the natural NLP analogue: the LLM withholds risky capabilities until a *guard* context finishes intent analysis.  

### 3.2  Jailbreak Detection as a Team-Monitoring Task  
Human-factors work (1972 “parallel vs. series” rules) shows that a *parallel* decision rule (k = 1 of n detectors must raise an alarm) maximises detection, whereas a *series* rule (all n must agree) eliminates false alarms but sacrifices sensitivity. LBYL can be parameterised analogously:  
* **Parallel LBYL** – any guard = block.  
* **Series LBYL** – all guards must approve = safe → risky execution.  
A *k-out-of-n* fusion rule allows tuning ROC operating points, with analytic error trade-offs documented in IEEE VTC-Spring-2015 and Bayesian-network sensor-voting work from Politecnico di Torino.

### 3.3  Residual-Risk Modelling  
The 2018 PAC-Bayesian ρ-bound for weighted majority votes affords a closed-form upper bound on ensemble risk using only first/second margins—lighter than full CTMC enumeration yet expressive enough to provide *mathematically rigorous* residual jailbreak probabilities for multilayer guardrails.

---

## 4  Survey of Defensive Techniques  
| Layer | Representative Work | Key Properties | Limitations |
|-------|--------------------|---------------|-------------|
| **Input-side linguistic filter** | **MoJE** (Mixture of Jailbreak Experts, AAAI AIES 2024) | ~90 % jailbreak block, negligible compute; naïve tabular statistics | Requires continual retraining for linguistic drift |
| **Prompt engineering / LBYL** | Original LBYL paper; Prompt-Loyal delayed activation | No model retrain; interpretable; composable | Still prompt-injectable; can leak instructions in chain-of-thought |
| **Content policy classifiers** | OpenAI & Anthropic policy nets | Low latency; centralised updates | Proprietary; black-box; bias concerns |
| **Contextual ICL immunisation** | RSA & Attention-Ratio metrics (arXiv 2310.00313) correlate embedding drift with robustness | Could auto-adapt prompts | Requires expensive representation probes |
| **Output-side DLP** | TDCommons #7538 two-stage DLP redactor | Stops data exfiltration | Only post-hoc; no intent inference |
| **Tree-ensemble fuzzing** | FATE (2024) adapts grey-box fuzzing to ML | Finds edge-case adversarials | Presently non-text models |
| **Federated guardrail learning** | SAFELearn, FedScale datasets | Privacy-preserving, scalable | Communication overhead |

---

## 5  End-to-End Architectural Blueprint  
```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1  User Prompt                                                        │
└─────────────────────────────────────────────────────────────────────────┘
             │
             ▼  (A) Linguistic Front-End  ≈ 0.1 ms latency @ 82 Mbps FPGA
     ┌──────────────────┐
     │ MoJE   (FPGA     │  ← optional HW acceleration via LDPC-style
     │ + KL-divergence) │     pipeline (§7)
     └──────────────────┘
             │ pass if benign
             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2  LBYL Guard Context                                                 │
│    – Parses intent                                                    │
│    – Verifies policy (§6)                                             │
└─────────────────────────────────────────────────────────────────────────┘
             │ approve
             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3  Capability-Enabled Execution                                       │
└─────────────────────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4  Output DLP / Redaction (TDCommons #7538)                            │
└─────────────────────────────────────────────────────────────────────────┘
             │
             ▼  deliver
```

### 5.1  Hardware note  
The (3, 6) LDPC FPGA core (82 Mbps) and the real-time KL-divergence monitor (sub-µs) show that lightweight statistical guardrails can be off-loaded to FPGA/ASIC near the LLM inference servers, satisfying **URLLC-grade latency** (0.5 ms) for safety-critical chatbots in industrial automation.

---

## 6  Implementation Guide  
### 6.1  Prompt Templates  
```text
<system>
You are an AI regulated under policy POL-2025-01-SAFE.
Stage-1 (Intent Analysis):
 – Summarise the user’s request in ≤30 words.
 – Classify intent using tags: {benign, questionable, disallowed}.
 – Cite policy paragraph for questionable/disallowed classes.
 – Output ONLY: {tag}:{summary}
</system>
<assistant>READY</assistant>
<user>{USER_PROMPT}</user>
```
The Stage-2 prompt is injected **only** if Stage-1 produced `benign:`. Prompt-loyal delayed activation ensures no capability leakage occurs if the user tries prompt-injection in Stage-1.

### 6.2  Code Hooks  
```python
result = llm(stage1_prompt)
if result.startswith('benign:'):
    stage2 = make_capability_prompt(original_user_prompt)
    answer = llm(stage2)
    answer = dlp_filter(answer)   # TDCommons #7538
else:
    answer = refusal_template(result)
```

### 6.3  Federated-Learning Option  
Enterprises with privacy constraints can train MoJE-style linguistic filters via **FedMalDE** or **FL-ADS**: semi-supervised aggregation plus vertical/horizontal FL improves F1 and handles non-IID departmental data. SAFELearn’s dropout-tolerant secure aggregation allows 500 clients per <0.5 s round.

---

## 7  Quantitative Evaluation Methodology  
1. **Benchmarks.** Combine LLMSecEval 1.2, the 46 800-item “Do Anything Now” set, and TrickyBugs for code-generation corner cases.  
2. **Attack Taxonomy.** Adopt the three-layer schema (Threat → Measure → Residual) from arXiv 2308.12833.  
3. **Metrics.**  
   • `Attack Success Rate (ASR)`  
   • `Benign Answer Rate (BAR)`  
   • `Guardrail Latency` (target ≤ 10 ms control-plane, 0.5 ms user-plane per 3GPP URLLC).  
   • `∆Embedding` and `Attention-Ratio` drift for ICL robustness (ρ≈0.62 correlation with performance).  
   • `Cronbach α` for inter-rater reliability when human red-team labels are needed; plateau >0.80 after ≈10 evaluations per prompt (TeamQ study).  
4. **Statistical Model Checking.** Use MRMC (reward-bounded CSL) or the BSCC-short-circuit LTL algorithm to verify that expected residual jailbreaks < ε. Reinforcement-learning SMC scales to models beyond symbolic limits.  
5. **Ensemble Risk Bound.** PAC-Bayesian ρ-bound supplies a closed-form residual risk upper bound for MoJE + LBYL + DLP stack.

---

## 8  Cross-Domain Analogues & Learnings  
| Cross-Domain Insight | Transfer to LBYL / Guardrails |
|----------------------|--------------------------------|
| **Grey-box fuzzing of tree ensembles (FATE)** finds adversarials by mutating thresholds; analogous threshold search can stress-test MoJE feature splits. |
| **Model Drifts** detected by DetAIL pipeline (AAAI 2024) via continuous ∆KL triggers suggest an auto-retrain flag for linguistic filters facing evolving jailbreak lingo. |
| **Incremental LSDD change detector** gives analytic false-positive bounds; reuse for live monitoring of prompt distribution shifts. |
| **Markov chain adaptive attackers** (energy-saving eavesdroppers) remind us that attackers optimise too; defender simulations must therefore incorporate adaptive adversaries (role4All + MAL attack graphs). |
| **EnterpriseLang threat-modelling DSLs** can embed LBYL nodes into holistic attack paths and compute business impact if guardrails fail. |
| **Ethereum-based Fed-Learning aggregator** removes poisoning vectors; same smart-contract ledger can vouch for guardrail policy provenance. |
| **LDTTL timing-recovery analog**: replacing a hard limiter with a linear device lowered jitter; similarly, soft probabilistic refusal policies may lower false-positive “jitter” compared to hard keyword filters. |
| **Sensor fusion k-out-n optimisation** parallels multi-guard stacks; algorithms minimise global error without exhaustive search. |
| **5G Cat-M1 ns-3 stack** achieving <1 ms latency shows feasibility of edge-deployed guardrails in OT/ICS chatbots that need URLLC-like performance. |
| **KL-divergence FPGA monitor on 10 MHz streams** proves hardware viability for real-time text-stream anomaly detection. |
| **Legal scholarship on actuarial guardrails** warns of bias entrenchment; guardrail decisions should be logged à-la secure audit (IPFS + hash chain) for due-process transparency. |

---

## 9  Experimental Plan (Prototype)  
1. **Dataset split**: 70 % training / 15 % validation / 15 % test, stratified by jailbreak family.  
2. **Baselines**: raw GPT-4, GPT-4+policy-net, LBYL-only, MoJE-only.  
3. **Proposed**: MoJE➜LBYL➜DLP (`parallel` fusion) vs. MoJE∧LBYL∧DLP (`series`).  
4. **Evaluation harness**:  
   • `fedscale` runtime for federated MoJE variants.  
   • `FATE` style mutator to auto-generate unseen jailbreaks.  
5. **SMC target property**: *P*≤0.05 [◇ (successful_jailbreak within 1 interaction)].  
6. **Termination criterion**: stop if the 95 % CI for ASR is below 0.05 or after 1 000 red-team episodes.

---

## 10  Risk, Bias & Governance  
• **Bias amplification**: As Fordham Law Rev. notes for actuarial systems, opaque statistical guardrails risk entrenching demographic bias. Transparency logs plus periodic fairness audits using Domain-aware mutators mitigate this.  
• **Reproducibility**: The “Self-Deception” errata highlight the need for open-sourced attack scripts and data; store all artifacts in a MAL-compatible, IPFS-pinned repository.  
• **Privacy**: Secure aggregation (SAFELearn) and smart-contract attestations protect proprietary policy data.  
• **Latency budgets**: Edge deployments must meet 0.5 ms user-plane constraint—validated via FPGA accelerators.  

---

## 11  Future Directions & High-Uncertainty Speculation (flagged 🔮)  
🔮 **Capsule-Net Guardrails.** FedMalDE’s subgraph-aggregated capsule networks could capture higher-order prompt syntax, potentially lifting MoJE’s ceiling beyond 90 %.  
🔮 **(1+1) Evolutionary Search Co-Design.** FATE’s coverage-free evolutionary search may jointly evolve prompts *and* guard policy parameters, closing the attacker–defender loop.  
🔮 **Real-Time Attack-Path Re-wiring.** Combining enterpriseLang attack graphs with live LLM telemetry could allow model-checking of **dynamic** security postures every few seconds.  
🔮 **Multi-Modal Jailbreaks.** Extend linguistic detectors to code, image or RF modality; FPGA KL-divergence monitors already support high-rate RF stream anomaly screening.  

---

## 12  Conclusion  
Defensive prompting via “Look Before You Leap” is *necessary but not sufficient.*  
A *layered* architecture—MoJE linguistic filter → LBYL intent gate → output-side DLP—bounded by PAC-Bayesian risk estimates and verified through state-of-the-art statistical model checking, provides quantifiable, latency-compatible protection while remaining adaptable via federated learning and drift detectors.  

Cross-pollinating insights from federated-learning security, model-checking advances, FPGA anomaly detection, sensor-fusion decision theory and legal-procedural safeguards enriches both the *science* and the *engineering* of LLM defence. Implementation templates and experimental protocols presented here aim to expedite production-grade deployments that can stand up to rapidly evolving jailbreak techniques.


## Sources

- http://dergipark.ulakbim.gov.tr/jcer/article/download/5000039226/5000038092/
- https://www.zora.uzh.ch/id/eprint/217434/1/1-s2.0-S1389128621005582-main.pdf
- http://scholarsmine.mst.edu/cgi/viewcontent.cgi?article%3D5761%26context%3Dmasters_theses
- https://research.utwente.nl/en/publications/the-ins-and-outs-of-the-probabilistic-model-checker-mrmc(eaa683f2-d054-4e88-9417-16bdcc1fde3a).html
- https://hal.science/hal-03610715/file/FinalVersion.pdf
- https://doaj.org/article/acc8f273668744e2be6dd5c7bef5ef43
- http://hdl.handle.net/2134/25736757.v1
- http://ece.k-state.edu/sunflower_wiki/images/b/b3/Nakfi.pdf
- https://digitalcommons.trinity.edu/compsci_faculty/16
- https://zenodo.org/record/5625651
- http://hdl.handle.net/11568/92132
- https://digitalcommons.wayne.edu/jmasm/vol6/iss1/27
- https://scholarcommons.usf.edu/etd/6259
- https://lirias.kuleuven.be/handle/123456789/545857
- http://resolver.tudelft.nl/uuid:d61cc5f6-4af8-49e8-9ee8-9171cacec449
- https://hal.science/hal-01774837/document
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-423621
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-308473
- http://hdl.handle.net/2097/7082
- https://hal.inria.fr/tel-01242619/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.57.7885
- http://hdl.handle.net/10255/dryad.126971
- https://epublications.regis.edu/facultypubs/725
- https://figshare.com/articles/_Estimation_performance_of_individual_parameters_/1429537
- http://soft.vub.ac.be/%7Encardozo/docs/papers/2011/cardozo11cop.pdf
- http://hdl.handle.net/10.1371/journal.pone.0291750.t007
- https://ojs.aaai.org/index.php/AAAI/article/view/20903
- http://whc13.bol.ucla.edu/FusionSensorNetwork.pdf
- https://digitalcommons.mtu.edu/michigantech-p/16155
- http://hdl.handle.net/2142/102456
- http://resolver.tudelft.nl/uuid:d1178bef-05ab-4f63-895e-dd582d581612
- https://trepo.tuni.fi/handle/10024/215694
- https://ieeexplore.ieee.org/document/8705874
- http://www.cs.bham.ac.uk/%7Eparkerdx/papers/sfm07.pdf
- http://hdl.handle.net/10.1371/journal.pone.0273588.g007
- https://figshare.com/articles/_Internal_consistency_reliability_coefficients_Cronbach_s_945_for_all_themes_of_the_TeamQ_instrument_/1239950
- http://hdl.handle.net/2078.1/88957
- https://hal.archives-ouvertes.fr/hal-01199905/document
- http://hdl.handle.net/2078.1/154801
- http://hdl.handle.net/10.1371/journal.pone.0271388.t004
- http://hdl.handle.net/10453/118165
- https://hdl.handle.net/1721.1/122969
- https://hdl.handle.net/11386/4825134
- https://doi.org/10.1109/INFOCOMWKSHPS54753.2022.9798325
- http://www.ee.kth.se/php/modules/publications/reports/2009/IR-EE-ICS_2009_012.pdf
- http://www.itu.dk/people/fbio/vmcai2013.pdf
- http://hdl.handle.net/2440/75217
- http://eprints.gla.ac.uk/40103/
- https://trepo.tuni.fi/handle/10024/129856
- http://hdl.handle.net/10138/304679
- http://hdl.handle.net/11584/313634
- https://animorepository.dlsu.edu.ph/etd_bachelors/11124
- https://zenodo.org/record/7575800
- https://doi.org/10.1049/cps2.70001
- http://digital.library.unt.edu/ark:/67531/metadc11003/
- http://tmo.jpl.nasa.gov/progress_report/42-162/162G.pdf
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S1571066105001878/MAIN/application/pdf/ac4ab4760529bf50ba534ebd45011205/main.pdf
- http://docs.rwu.edu/cgi/viewcontent.cgi?article%3D1027%26context%3Dsjs_fp
- https://zenodo.org/record/5547824
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/9624
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-284445
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-259297
- http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n3963.pdf
- http://hdl.handle.net/1854/LU-837921
- http://hdl.handle.net/10.1371/journal.pone.0273588.g006
- http://hdl.handle.net/2078.1/227296
- https://www.icesi.edu.co/revistas/index.php/sistemas_telematica/article/view/927
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-259298
- http://urn.kb.se/resolve?urn=urn:nbn:se:bth-27597
- https://ojs.aaai.org/index.php/AAAI/article/view/26872
- http://resolver.tudelft.nl/uuid:a5537af8-2146-45fe-89b1-48114e034b2c
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-297942
- https://scidar.kg.ac.rs/handle/123456789/9072
- http://hdl.handle.net/10.1371/journal.pone.0278092.t002
- https://figshare.com/articles/_Performance_evaluation_metrics_of_the_secretomics_based_methods_compared_to_other_SCL_predictors_/264510
- http://afp.sourceforge.net/browser_info/current/AFP/Markov_Models/document.pdf
- https://digitalcommons.montclair.edu/compusci-facpubs/299
- https://figshare.com/articles/_Reliability_Cronbach_8217_s_945_for_Emotional_State_Trait_and_Criminality_Ratings_for_the_Controlled_and_Naturalistic_Photos_by_Gender_/298439
- https://www.open-access.bcu.ac.uk/16136/
- http://arxiv.org/abs/2204.13256
- http://hdl.handle.net/10.1371/journal.pone.0214249.t001
- http://www.open-access.bcu.ac.uk/6077/
- https://hal.archives-ouvertes.fr/hal-01543282
- https://ir.lawnet.fordham.edu/flr/vol87/iss1/12
- http://hdl.handle.net/11568/193327
- http://stat-athens.aueb.gr/~esi/proceedings/18/pdf/435-440.pdf
- https://ueaeprints.uea.ac.uk/id/eprint/87317/
- http://research.ijcaonline.org/volume93/number16/pxc3896072.pdf
- http://www8.cs.umu.se/~thomash/reports/BehaviorRecognitionforLearningfromDemonstration.pdf
- http://hdl.handle.net/10576/37225
- http://hdl.handle.net/10068/536475
- http://hdl.handle.net/10.1371/journal.pone.0271388.t005
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.3616
- http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?punumber=6221021
- http://krex.k-state.edu/dspace/bitstream/handle/2097/7077/JonathanHoag2010.pdf%3Bjsessionid%3D5D4E818DC2B5F9A87A86B6482C28630E?sequence%3D1
- https://hal.archives-ouvertes.fr/hal-03779486
- http://hdl.handle.net/2142/81718
- https://www.ijcnis.org/index.php/ijcnis/article/view/2515
- https://s3.amazonaws.com/prod-ucs-content-store-us-east/content/pii:S157106610405248X/MAIN/application/pdf/6aed3466db77d9e5cb1f3edaec0b096a/main.pdf
- http://www.nt.ntnu.no/users/skoge/prost/proceedings/ecc-2013/data/papers/0112.pdf
- https://hal.archives-ouvertes.fr/hal-02461502
- http://arxiv.org/abs/2308.03825
- http://arxiv.org/abs/2308.12833
- http://creativecommons.org/licenses/by-nc-nd/4.0
- http://localhost:8080/xmlui/handle/123456789/19565
- https://escholarship.org/uc/item/9rh9p8mn
- https://repository.law.umich.edu/cgi/viewcontent.cgi?article=4736&amp;context=mlr
- http://cds.cern.ch/record/2729154
- https://zenodo.org/record/8123647
- http://hdl.handle.net/20.500.11875/553
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-308821
- http://dx.doi.org/10.1109/MECO52532.2021.9460304
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/3865
- https://hdl.handle.net/10356/164399
- http://tubiblio.ulb.tu-darmstadt.de/view/person/Egert=3ARolf=3A=3A.html
- http://hdl.handle.net/10547/623049
- http://hfs.sagepub.com/content/14/4/309.full.pdf
- http://hdl.handle.net/10.1184/r1/6609887.v1
- https://figshare.com/articles/_Observed_reliability_levels_945_for_teams_with_a_different_number_of_completed_TeamQ_evaluations_/1239954
- https://repozitorij.ffos.hr/islandora/object/ffos:2620/datastream/FILE0
- http://www.nusl.cz/ntk/nusl-442354
- http://eprints.utm.my/id/eprint/91947/
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-511287
- https://eprints.umm.ac.id/101730/3/Pratama%20Akbi%20Nastiti%20-%20Machine%20Learning%20Klasifikasi%20Na%C3%AFve%20Bayes%20Pearson%20Product-Moment%20Correlation%20Klasifikasi.pdf
- https://hal.science/hal-04208787
- http://ijcsit.com/docs/Volume+5/vol5issue02/ijcsit20140502102.pdf
- http://www.comp.nus.edu.sg/~abhik/pdf/padl04.pdf
- http://hdl.handle.net/2078.1/91163
- http://sfxit.ugent.be/sfx_local?sid=bellow&atitle=Evidence%20for%20a%20hierarchical%20structure%20underlying%20avoidance%20behavior&issn=0097-7403&volume=35&issue=1&spage=123&date=2009&svc.fulltext=yes
- https://figshare.com/articles/_The_Shock_Avoidance_Behavioural_paradigm_with_self_initiated_A_and_externally_triggered_B_conditions_/1513531
- http://cqpi.engr.wisc.edu/system/files/neworleans.pdf
- https://scholarbank.nus.edu.sg/handle/10635/191903
- https://openresearch.surrey.ac.uk/view/delivery/44SUR_INST/12139171110002346/13140256120002346
- https://zenodo.org/record/4727605
- https://reunir.unir.net/handle/123456789/10388
- https://hdl.handle.net/1959.7/uws:66523
- https://eprints.lancs.ac.uk/id/eprint/204514/
- https://lirias.kuleuven.be/handle/123456789/466070
- https://pub.uni-bielefeld.de/record/2281511
- http://resolver.tudelft.nl/uuid:abfa9cc8-75ba-4dd0-84ed-3ce674445c0d
- https://ojs.aaai.org/index.php/AIES/article/view/31638
- http://hdl.handle.net/10255/dryad.192596
- http://hdl.handle.net/2117/13039
- https://eprints.uny.ac.id/78606/
- https://www.tdcommons.org/context/dpubs_series/article/7538/viewcontent/A_Cost_Effective_Method_to_Prevent_Data_Exfiltration_from_LLM_Prompt_Responses.pdf
- http://hdl.handle.net/10.1371/journal.pone.0270154.g002
- https://zenodo.org/record/192828
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Detection-and-Management-of-Concept-Drift/99511553902346
- http://publica.fraunhofer.de/documents/N-226207.html
- http://hdl.handle.net/10871/128696
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:227934
- http://hdl.handle.net/10068/335782
- https://doi.org/10.1109/RCIS.2009.5089274
- https://www.researchgate.net/profile/Pietro_Ferrara/publication/242286672_JAIL_Firewall_Analysis_of_Java_Card_by_Abstract_Interpretation/links/00b49539708fbdbc9d000000.pdf
- https://doi.org/10.1109/MNET.2018.8329617
- https://zenodo.org/record/47976
- https://hal.inria.fr/hal-01088193/file/main.pdf
- https://zenodo.org/record/7977256
- https://opus.hs-offenburg.de/frontdoor/index/index/docId/3268
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.82.731
- https://doi.org/10.1007/978-3-662-49674-9_7
- https://aaltodoc.aalto.fi/handle/123456789/110701
- https://zenodo.org/record/7750212
- https://figshare.com/articles/_An_illustration_of_temporal_learning_via_anticipatory_drops_in_the_response_threshold_/864727
- http://hdl.handle.net/2117/87446
- https://doaj.org/article/4196f21aa07044878d09417f690b2793
- http://arks.princeton.edu/ark:/88435/pr1qf2q
- http://collaboration.csc.ncsu.edu/laurie/Papers/p31-gegick.pdf
- http://hdl.handle.net/10251/183050
- https://zenodo.org/record/4374309
- https://pub.uni-bielefeld.de/record/2966088
- http://hdl.handle.net/10084/110972
- https://hdl.handle.net/10356/148598
- https://research-explorer.app.ist.ac.at/record/1234
- http://hdl.handle.net/2066/157666
- http://hdl.handle.net/2117/86278
- http://www.thinkmind.org/download.php?articleid%3Dsec_v7_n34_2014_7
- http://www.infosec.aueb.gr/Publications/SECRYPT-2015%20Automated%20exploits%20Site.pdf
- http://dx.doi.org/10.1109/VTCSpring.2015.7145982
- http://hdl.handle.net/10.1371/journal.pone.0210597.g003
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.433.3947
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-33104
- https://doi.org/10.1007/s11276-021-02553-x
- www.springer.com.
- https://publish.tntech.edu/index.php/PSRCI/article/view/527
- http://hdl.handle.net/2144/2137
- http://arxiv.org/abs/2105.11367
- http://www.nnce.org/Arquivos/Artigos/1996/landeira_etal_1996.01.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-302372
- http://eprints.utem.edu.my/id/eprint/25470/
- https://zenodo.org/record/8014233
- http://hdl.handle.net/10.1371/journal.pone.0291750.t006
- http://urn.kb.se/resolve?urn=urn:nbn:se:lnu:diva-75204
- http://arxiv.org/abs/2308.11521
- http://irep.iium.edu.my/5641/1/vol501p4.htm
- http://hdl.handle.net/10.5061/dryad.jc14081/3
- https://doi.org/10.1109/ISABEL.2009.5373614
- http://cds.cern.ch/record/2649532
- http://sim.sagepub.com/content/79/9/515.full.pdf
- https://pub.uni-bielefeld.de/record/2980429
- http://hdl.handle.net/11591/365039
- https://orbilu.uni.lu/handle/10993/44927
- https://figshare.com/articles/_Number_of_completed_TeamQ_evaluations_needed_to_obtain_reliable_theme_scores_based_on_generalizability_analysis_/1239953
- http://urn.kb.se/resolve?urn=urn:nbn:se:ltu:diva-42011
- http://eprint.iacr.org/2015/097.pdf
- http://resolver.tudelft.nl/uuid:5b6a753e-bbbb-4b4f-b4b8-9a7a1ac838bb
- https://digital.library.unt.edu/ark:/67531/metadc935096/
- https://hal.science/hal-01169228
- http://delab.csd.auth.gr/%7Ekatsaros/Secrypt-2015.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-294123
- http://falbu.50webs.com/articole/icassp2002.pdf
- http://purl.utwente.nl/publications/58974
- https://opensiuc.lib.siu.edu/ece_articles/26
- http://hdl.handle.net/10.1371/journal.pone.0205285.g002
- https://hal-ensta-bretagne.archives-ouvertes.fr/hal-02123046
- http://www.nusl.cz/ntk/nusl-400908
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-425193
- http://hdl.handle.net/10.6084/m9.figshare.24602307.v1
- http://www.loc.gov/mods/v3
- https://figshare.com/articles/Diagram_of_the_LSSM_for_human_recognition_/4772917
- http://nbn-resolving.de/urn:nbn:de:bsz:352-2-16l0jts3wgeoz5
- http://arxiv.org/abs/2310.00313
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-476260
- http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-102884
- http://dx.doi.org/10.1145/3286490.3286559