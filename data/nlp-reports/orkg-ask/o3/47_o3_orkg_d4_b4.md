# Verifying and Improving Factuality in Large Language Models through a **Grounded Court-Debate** Paradigm  
*Comprehensive Technical Report synthesising 120+ prior findings*  
(2025-09-05)

---

## 1 Motivation and Problem Statement  
Large Language Models (LLMs) outperform earlier NLP systems on reasoning‐style tasks, yet factual fidelity remains brittle.  TruthfulQA shows that the best open models still hallucinate on 42 % of adversarially-designed questions; scaling alone worsens the problem.  Meanwhile, legal practice offers a centuries-refined adversarial procedure whose explicit burdens of proof, evidentiary gating and third-party adjudication are specifically engineered to surface and correct factual error.  The core thesis of this report is therefore:

> *Embedding LLMs in a procedurally faithful, evidence-grounded “court debate” can both **diagnose** and **repair** factual defects more robustly than raw prompting or retrieval-only augmentation.*

To operationalise this thesis we analyse three orthogonal axes:

1. **Theoretical formulation** – formal dialogue systems, argumentation frameworks, burden-shifting rules.  
2. **Empirical evaluation** – datasets, unsupervised metrics, fact-checking corpora, risk-based performance targets.  
3. **Practical deployment** – multi-agent orchestration, retrieval at scale, latency/cost envelopes, IP compliance.

The remainder integrates *all* 71 domain-specific and 52 cross-domain research findings supplied, structuring them into an end-to-end solution blueprint.

---

## 2 Conceptual Foundations: Why “Legal-Grade Truth” ≠ Simple Accuracy

### 2.1 Formal vs Substantive Truth  
Legal scholarship documents a structural gap between factual reality and “formal legal truth”: evidentiary exclusions, varying standards (preponderance vs beyond reasonable doubt) and jury nullification decouple verdicts from objective ground truth.  Consequently, *metrics like TruthfulQA model the wrong notion of truth for court-style evaluation*.  A valid LLM benchmark must incorporate:
* **Process-Legitimacy** – did the agent respect burden allocations and admissibility rules?  
* **Error-Risk Management** – did the debate reduce Type I/II error probabilities given the stakes?  
* **Calibration under Uncertainty** – did the adjudicator obtain well-behaved probability estimates?

### 2.2 Formal Dialogue & Argumentation Frameworks (AFs)
* **Dung AFs & Attacks-on-Attacks** supply the minimal abstract semantics.  Modgil’s extensions and Baumann’s *splitting* technique provide scalability; Bipolar & Weighted ADFs add graded acceptance and meta-level values.  
* **ASPIC+** separates defeasible from strict inference, supports arbitrary priority orderings, and has been mapped onto real statutes and common-law rulings.  
* **Carneades → ADF compilation** shows how proof standards and cyclic evidentiary graphs can be encoded without semantic loss.  
* **Prakken & Sartor two-phase adjudication** plus the Groningen *Formal Model of Adjudication Dialogues* explicitly model (i) argumentation phase with burden allocation and (ii) decision phase with undercutting/priority arguments, thereby capturing the institutional logic of courts.  
* Logical vocabulary extensions—*confirmation*, *preclusion*, *reflection*—enable finer-grained evidentiary handling than vanilla attack/defeat.

### 2.3 Game-Theoretic & Behavioural Regularities  
Courts systematically favour more **extreme** presented models; the bias attenuates with richer evidence and stronger adjudicator discrimination.  Psychological experiments reveal an “anti-primacy” bias: first claimants are penalised with heavier proof burdens.  These effects motivate *multi-agent ensembles* and *evidence-amplified protocols* that counteract single-agent pathologies.

### 2.4 Cross-Lingual & Para-Linguistic Evidence Streams  
Empirical studies link **vocal arousal** and **lawyer voice features** to Justices’ votes (+1.1 pp outcome accuracy).  Conversation structure alone predicts 62–77 % of Supreme-Court outcomes.  Hence debate simulators should capture:
* turn order, reference chains, topic segmentation (CSseg beats LCseg);  
* acoustic/prosodic cues where available;  
* cross-lingual phenomena: dependency-length minimisation, information-density vs articulation-rate trade-off.

---

## 3 Grounding Sources and Corpus Strategy

### 3.1 Domain-Specific Corpora Outperform Scaling  
Zero-shot GPT-4 on LEDGAR trails *tiny* legal-tuned models by up to 26.8 pp F₁.  MULTILEGALPILE-trained variants top LexGLUE.  **Lesson**: allocate budget to *grounding*, not only parameter count.

Key corpora/assets:  
* **MULTILEGALPILE** (24 languages, 689 GB) – licensing permits redistribution.  
* **CASELAW4** (350 k labelled appellate opinions).  
* **ClassActionPrediction** benchmark (raw complaints).  
* **Legal TRUTHS** IE pipeline (95.6 % in-sample F₁) for fact triples.  
* **Political-Debate Fact-Checking** (Zenodo 7490224) & Wikipedia Claim-Evidence corpus – supply out-of-domain factuality testbeds.

### 3.2 IP & TDM Compliance  
Directive 2019/790/EU arts 3–4:  
* Art. 3 unwaivable for research bodies.  
* Art. 4 opt-outable for commercial actors; model weight redistribution of opt-out works infringes copyright.  
Directive 2019/770 (Digital Content) transposition in Estonia is pending; draft LOA amendments may extend liability periods—relevant for long-term model service obligations.  
**Risk-mitigation**: maintain provenance metadata; restrict commercial checkpoints to “lawfully accessed, opt-in” sub-corpora.

### 3.3 Automatic Corpus Normalisation  
Cross-language comparability benefits from *syllable-level information-density balancing* rather than raw word counts; apply this when mixing multilingual case-law to avoid skewed frequency statistics.

---

## 4 Architecting a **Grounded Court-Debate** LLM System

### 4.1 Agent Roles & Protocol
```
      Claimant-Agent  ↔  Respondent-Agent
                \\   (Argument Phase)   //
                Judge-Agent (neutral)
                         ↓
                Decision Phase Output
```

1. **Argument Phase**  
   * Each side issues **strict** (provable) or **defeasible** (prima-facie) claims.  
   * Claims must cite *retrieved evidence* with Legal TRUTHS-format fact triples.  
   * Burden allocation follows Prakken-Sartor rules; explicit *meta-dialogue* allowed to dispute burdens or admissibility.  
2. **Decision Phase**  
   * Judge constructs an AF/ADF graph, applies preferred + grounded semantics; *attacks on attacks* capture preclusion/reflection.  
   * Probability calibration applied via similarity-aligned ensemble of judges (AlignLLM) to dampen single-model variance.

### 4.2 Retrieval & Evidence Layer  
* **Retrieval-Augmented Generation**: internal RAG pipeline enforces chain-of-thought *with source citation*.  Performance varies by language & claim type; fallback indicator triggers *Debate Amplification*.  
* **Mobile-Agent IR** pushes code to data when bandwidth-limited; bounded P2P caches cut backend load by 33–70 %.  
* **Legal-domain IE** populates a *Ground Truth Knowledge Store* (GTKS) with 91 %+ precision.

### 4.3 Scalable Orchestration & QoS  
Latency target: **p99 < 200 ms** end-to-end for user queries.  Pipeline components:
* **PerfIso** co-locates batch fine-tuning with inference, lifting off-peak utilisation from 21 → 66 % across 90 k nodes while holding p99.  
* **Firmament** scheduler + **MetaNet** meta-selector assign pods to GPUs/CPUs; GPU offload slashes ranking latency 8.8×.  
* **Cheetah** MPI layer accelerates collective broadcasts by 93 %.  
* **Dovetailing & Parallel-A
*** accelerate AF reasoning and search-based evidence ranking.  
* **Vivaldi/GNP** latency coordinates guide nearest retrieval node selection.

### 4.4 Debate Segmentation & Management  
* Apply **CSseg** for topic drift and argument chain detection; adaptive weights optimise WindowDiff.  
* DiaLaw procedural constraints ensure realistic timing: who can introduce evidence when.  
* Automated *speaker-turn dynamics* injection: order, self/other continuity, moderator cues.

### 4.5 Factuality-Repair Loop  
1. Judge detects low-confidence fact nodes (TruthfulQA style).  
2. Triggers *evidence amplification* – retrieve additional documents, possibly ask external SMEs or micro-task crowd.  
3. Re-enter mini-debate focused on disputed node.  
4. Update ADF acceptance degrees; if stable within ε tolerance, finalise.

---

## 5 Evaluation Protocols

### 5.1 Datasets & Tasks  
| Layer | Dataset | Purpose |
|-------|---------|---------|
| Raw factuality | TruthfulQA, political-debate fact-checking | Hallucination baseline |
| Legal QA | LEDGAR, ClassActionPrediction, CASELAW4 | Domain grounding |
| Debate process | Oyez audio, 100-Minute Debate (CSseg), DiaLaw logs | Procedural fidelity |

### 5.2 Metrics  
1. **Accuracy** – but computed per-claim *post adjudication*, not raw generation.  
2. **Process-Legitimacy Index (PLI)** – composite: (a) burden compliance, (b) admissibility compliance, (c) argument graph completeness.  
3. **Calibrated Brier/Log-loss** – judged by AlignLLM collective.  
4. **Weighted Accuracy-Diversity (WAD)** – harmonic mean used for ensemble outputs.  
5. **Tail-Risk Latency SLA** – <200 ms p99 across 100 k queries.

### 5.3 Variance-Stabilised Ensemble Judging  
*Similarity-Aligned Ensemble Metrics* (Abeyratne 2025) shrink 95  % CIs vs single-judge LLMs, leveraging MT-Metrics ensemble style embeddings.  AlignLLM’s dual space (problem ↔ solution) further boosts Spearman ρ by >0.15.

### 5.4 Error-Risk Tuning  
Dynamic significance levels (Empirical Methods for the Law) trade false-positive vs false-negative cost depending on downstream application (e.g., medical advice vs trivia).

---

## 6 Contrarian & Cross-Domain Insights

* **Dependency-Length Minimisation** and **Menzerath-Altmann** laws suggest that LLM outputs could be regularised for *syntactic efficiency*—potentially serving as an ancillary plausibility cue during adjudication.  
* **Universal negative correlation** between information density and articulation rate implies that *speech-to-text* modules feeding the debate should normalise for tempo or risk biasing language-specific confidence scores.  
* **Similarity-aligned ensembles** from influenza forecasting and structural biology generalise to legal QA—pointing to cross-domain robustness of the alignment trick.  
* **Variance-tracking** from ex aequo et bono jurisprudence hints that once inter-judge dispersion falls below τ ≈ 2 pp, further human review yields diminishing returns; we can hard-stop the debate.

---

## 7 Roadmap and Open Research Questions

| Stage | Milestone | Dependencies | Risk |
|-------|-----------|--------------|------|
| M0 | Assemble GTKS with provenanced corpora | Legal TRUTHS, MULTILEGALPILE | IP compliance |
| M3 | Implement 3-agent debate prototype on 1,000 cases | DiaLaw constraints | Latency |
| M6 | Integrate AlignLLM collective judging; run against TruthfulQA & LEDGAR | Ensemble infra | Cost |
| M9 | Deploy PerfIso-isolated cluster, <200 ms p99 | Firmament, GPU vertical scaling | Tail spikes |
| M12 | Submit empirical paper comparing Debate vs RAG w/o debate | – | – |

**Open Questions**  
1. *Weighted ADFs* vs *Conditional ADFs*: which better model graded fact uncertainty?  
2. Can **speaker acoustic features** be synthesised (text-to-speech) to test the effect of voice on adjudicator perception?  
3. How to exploit **Hamiltonian-CBS** multi-goal path finding for evidence retrieval ordering?  
4. Will **opt-out terminologies** in Art. 4 be published in a machine-readable register and can they seed automatic exclusion filters?

---

## 8 Conclusion  
Combining retrieval-augmented generation with **procedure-faithful court debate** delivers a principled avenue for raising LLM factual reliability.  Abstract-dialectical tools supply formal semantics, ensemble judging tackles evaluation variance, and proven performance-isolation plus accelerator-centric scheduling keeps the system within real-time cost envelopes.  Policy compliance and multilingual grounding remain non-trivial but tractable.  The outlined architecture thus represents a concrete, end-to-end research and engineering agenda that leverages the full spectrum of existing scholarship—ranging from legal IP nuance to high-performance systems design—to close the factuality gap in next-generation language models.


## Sources

- https://lawecommons.luc.edu/cgi/viewcontent.cgi?article=1653&amp;context=facpubs
- https://zenodo.org/record/7490224
- https://zenodo.org/record/1475514
- https://zenodo.org/record/1240746
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.988
- https://zenodo.org/record/7727057
- http://coitweb.uncc.edu/~anraja/PAPERS/AAAISS04.pdf
- https://hal-emse.ccsd.cnrs.fr/emse-01575624
- https://zenodo.org/record/3801114
- https://chicagounbound.uchicago.edu/cjil/vol18/iss1/3
- http://hdl.handle.net/11336/76482
- https://eprints.lancs.ac.uk/id/eprint/204581/
- http://www.ijcsit.com/docs/Volume%206/vol6issue03/ijcsit2015060306.pdf
- http://homepage.univie.ac.at/wolfgang.dvorak/files/argcomp_resem_slides.pdf
- http://hdl.handle.net/11582/331008
- http://publications.ut-capitole.fr/28406/1/Attorney_Voice_and_the_US_Supreme_Court.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-190434
- http://hdl.handle.net/11582/322998
- http://repository.urosario.edu.co/handle/10336/19089
- http://hdl.handle.net/21.11116/0000-0002-D4AD-C
- http://publica.fraunhofer.de/documents/PX-25525.html
- http://hdl.handle.net/11336/152318
- https://digitalcommons.unomaha.edu/studentwork/2189
- http://scholarworks.csun.edu/xmlui/handle/10211.2/286
- http://irs.ub.rug.nl/ppn/318907720
- http://hdl.handle.net/11144/1491
- http://hdl.handle.net/10447/567283
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1069.2244
- http://infoscience.epfl.ch/record/274328
- https://research.utwente.nl/en/publications/burden-of-proof-in-legal-dialogue-games(5dd8ad34-1f9f-4c17-bb00-e7f7076a4b48).html
- https://scholarlycommons.law.cwsl.edu/fs/190
- http://hdl.handle.net/10453/30830
- https://ojs.aaai.org/index.php/SOCS/article/view/18151
- http://warse.org/pdfs/2014/ijacst02312014.pdf
- http://hdl.handle.net/10.1371/journal.pone.0256133.g004
- http://hdl.handle.net/10779/cqu.24502381.v1
- http://hdl.handle.net/2078.1/204444
- http://infoscience.epfl.ch/record/278200
- http://hdl.handle.net/10278/3704213
- https://orca.cardiff.ac.uk/id/eprint/120619/1/understanding_adfs.pdf
- https://www.repository.cam.ac.uk/handle/1810/264317
- http://geoff-morrison.net/documents/Morrison,
- https://ojs.aaai.org/index.php/AAAI/article/view/11545
- https://hal.archives-ouvertes.fr/hal-02875552
- https://cris.maastrichtuniversity.nl/en/publications/71038652-3825-49ec-ba92-ec97d29bdd5e
- https://zenodo.org/record/2710864
- https://discovery.dundee.ac.uk/en/publications/e42c11a5-8a3e-4ab8-be97-612ed5aa570f
- https://scholarship.law.cornell.edu/facpub/1186
- http://hdl.handle.net/21.11116/0000-0005-885E-9
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-385195
- http://hdl.handle.net/2429/54722
- https://pure.rug.nl/ws/files/203338503/2021.wnut_1.55.pdf
- http://dx.doi.org/10.18653/v1/2022.nllp-1.3
- https://hal.inria.fr/hal-00650313/document
- http://works.bepress.com/cgi/viewcontent.cgi?article%3D1001%26context%3Destelle_derclaye
- https://digitalcommons.law.byu.edu/lawreview/vol2017/iss6/5
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.75.4958
- http://dx.doi.org/10.48550/arXiv.2306.02069
- https://chicagounbound.uchicago.edu/jle/vol59/iss3/2
- https://zenodo.org/record/5060206
- http://www.lrec-conf.org/proceedings/lrec2004/pdf/363.pdf
- https://hdl.handle.net/10356/82564
- https://lawdigitalcommons.bc.edu/darter_materials/44
- https://scholarworks.unist.ac.kr/handle/201301/35431
- https://archive-ouverte.unige.ch/unige:97526
- https://ojs.aaai.org/index.php/SOCS/article/view/18577
- http://publications.ut-capitole.fr/28407/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.74.9495
- http://hdl.handle.net/10.1371/journal.pone.0216922.g001
- https://digitalcommons.schulichlaw.dal.ca/scholarly_works/463
- http://web.engr.illinois.edu/%7Eshu17/pdf/hu2015dcoss.pdf
- http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6826508
- http://journals.tubitak.gov.tr/elektrik/issues/elk-14-22-5/elk-22-5-21-1210-105.pdf
- http://nima.eeg.uminho.pt/uploads/EEG161107NIMA14.pdf
- http://www.nusl.cz/ntk/nusl-218001
- http://hdl.handle.net/11565/3825304
- http://intranet.csc.liv.ac.uk/research/techreports/tr2015/ulcs-15-002.pdf
- https://www.idref.fr/241586631
- https://doaj.org/toc/2310-1202
- https://doi.org/10.7910/DVN/J5TU3H
- https://hal.archives-ouvertes.fr/hal-02473494
- https://escholarship.org/uc/item/7t80m17d
- http://hdl.handle.net/21.11116/0000-0000-2BED-6
- https://figshare.com/articles/_a_Word_frequency_per_million_across_Dutch_English_French_German_and_Spanish_/259386
- http://idir.uta.edu/%7Enaeemul/file/factchecking-cikm15-hassan-cameraready.pdf
- http://hdl.handle.net/2066/101551
- https://digitalcommons.law.seattleu.edu/sulr/vol2/iss1/3
- https://hdl.handle.net/10356/88377
- http://hdl.handle.net/10018/22597
- http://hdl.handle.net/1903/9999
- https://hal.archives-ouvertes.fr/hal-02976607
- http://hdl.handle.net/11585/772595
- http://egov.ufsc.br/portal/sites/default/files/anexos/5738-5730-1-PB.pdf
- http://www.tandfonline.com/doi/abs/10.1080/13546780701739782
- http://liber2014.lnb.lv/liber-award/
- https://figshare.com/articles/_Similarity_with_the_gold_standard_model_/699687
- https://animorepository.dlsu.edu.ph/faculty_research/3208
- https://doi.org/10.7910/DVN/JFU71R
- http://hdl.handle.net/11385/210695
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/d2/25/TSWJ2014-961747.PMC3925515.pdf
- http://www.ece.iastate.edu/%7Ezambreno/pdf/AwaRov14A.pdf
- https://zenodo.org/record/5082012
- https://hal.science/hal-01634461/file/kes2017.pdf
- http://www.dougwalton.ca/papers
- https://hal.archives-ouvertes.fr/hal-01291101
- http://www.aclweb.org/anthology/W/W14/W14-1305.pdf
- https://research.rug.nl/en/publications/d8650611-fb8a-4404-918d-b430f7313d28
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/34/49/TSWJ2014-492387.PMC4177094.pdf
- http://hdl.handle.net/10393/26514
- https://ijece.iaescore.com/index.php/IJECE/article/view/29967
- http://ul.qucosa.de/api/qucosa%3A17204/attachment/ATT-0/
- http://hdl.handle.net/2262/89952
- https://zenodo.org/record/8105098
- https://research.vu.nl/en/publications/c172f0ee-3377-4d9a-b753-be3b25e3dbc3
- https://zenodo.org/record/7541425
- http://files.eric.ed.gov/fulltext/ED376518.pdf
- https://rgu-repository.worktribe.com/file/2754840/1/ABEYRATNE%202025%20AlignLLM%20%28AAM%29
- https://doaj.org/article/12aafbdc74524c4eba9c3d2a9ef71979
- http://discovery.ucl.ac.uk/17308/1/17308.pdf
- https://madoc.bib.uni-mannheim.de/34929
- https://biblio.ugent.be/publication/8752443
- https://aaai-2022.virtualchair.net/poster_aaai7429
- http://sedici.unlp.edu.ar/handle/10915/21164
- https://lawecommons.luc.edu/luclj/vol48/iss1/3
- http://publications.ut-capitole.fr/31263/
- http://arxiv.org/abs/2205.10640
- http://hdl.handle.net/2027/mdp.39015077946690
- https://ir.cwi.nl/pub/28029
- http://hdl.handle.net/20.500.12708/19570
- http://hdl.handle.net/1822/2004
- https://ojs.aaai.org/index.php/AAAI/article/view/17472
- https://ojs.aaai.org/index.php/AAAI/article/view/11035
- https://rgu-repository.worktribe.com/file/2754880/1/ABEYRATNE%202025%20Unsupervised%20similarity-aligned%20%28LINK%20ONLY%29
- http://hdl.handle.net/11582/3938
- https://pub.uni-bielefeld.de/record/2527686
- https://hal.archives-ouvertes.fr/hal-01133692
- http://publications.ut-capitole.fr/31268/
- https://scholarship.law.umn.edu/lawineq/vol4/iss1/5
- https://dare.uva.nl/personal/pure/en/publications/futuretdm-is-mapping-the-legal-barriers-to-tdm-in-europe(a1448bba-d3d2-4f32-9438-744d198396cc).html
- https://doaj.org/toc/1537-744X
- http://hdl.handle.net/10068/956222
- https://figshare.com/articles/_Overview_of_ensemble_comparison_methods_implemented_in_ENCORE_/1586458
- https://nbn-resolving.org/urn:nbn:de:hebis:30:3-692110
- https://doi.org/10.5128/erya16.04
- https://ojs.aaai.org/index.php/SOCS/article/view/18560
- http://hdl.handle.net/2027/pur1.32754077529737
- http://hdl.handle.net/10.3389/frai.2024.1341697.s001
- https://aaltodoc.aalto.fi/handle/123456789/35238
- https://hdl.handle.net/1887/3198962
- https://scholarship.law.duke.edu/faculty_scholarship/2094
- http://hdl.handle.net/11568/1014169
- http://hdl.handle.net/10.1371/journal.pone.0256133.s004
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/1048_Paper.pdf
- http://hdl.handle.net/1854/LU-8756347
- http://urn.kb.se/resolve?urn=urn:nbn:se:su:diva-195372
- http://hdl.handle.net/2027/mdp.39015069665092
- https://research.rug.nl/en/publications/a-formal-model-of-adjudication-dialogues(b90eba9c-38b9-4441-b24f-3a6ede8c47b0).html
- http://nbn-resolving.de/urn:nbn:de:bsz:93-opus-ds-97844
- http://www.dcs.bbk.ac.uk/ida2017/
- http://hdl.handle.net/11585/89750
- http://hdl.handle.net/20.500.12678/0000004257
- http://hdl.handle.net/2066/112645
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.74.4055
- https://scholarlycommons.law.hofstra.edu/hlr/vol46/iss3/9
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.80.2301
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.45.2780
- http://arxiv.org/abs/2311.08890
- https://figshare.com/articles/_Three_types_of_similarity_judgment_tasks_scaled_with_metric_and_non_metric_MDS_/942017
- https://hal.inria.fr/hal-00689745
- http://www.polisci.umn.edu/%7Etjohnson/MyPapers/Johnsonetal2006.pdf?issueId%3D01%26jid%3DPSR%26volumeId%3D100
- http://www.dcs.kcl.ac.uk/staff/smodgil/tafa13_submission_24.pdf
- https://jlc.law.pitt.edu/ojs/jlc/article/view/132
- https://digitalcommons.law.ggu.edu/ggulrev/vol22/iss2/7
- http://sedici.unlp.edu.ar/bitstream/handle/10915/31737/Documento_completo.pdf?sequence%3D1
- https://hal.inria.fr/hal-01183129/document
- https://hal.inria.fr/hal-03119732/document
- http://www.informatik.uni-leipzig.de/%7Eellmau/publications/2012/FAIA245-0505.pdf
- http://publica.fraunhofer.de/documents/N-582002.html
- http://ul.qucosa.de/api/qucosa%3A16720/attachment/ATT-0/
- https://cug.org/5-publications/proceedings_attendee_lists/CUG11CD/pages/1-program/final_program/Thursday/16C-Graham-Paper.pdf
- http://sfxit.ugent.be/sfx_local?sid=bellow&atitle=Abstract%20argumentation%20and%20explanation%20applied%20to%20scientific%20debates&issn=0039-7857&volume=190&issue=12&spage=2195&date=2013&svc.fulltext=yes
- https://figshare.com/articles/Justice_data/1162516
- http://hdl.handle.net/10161/9957
- https://zenodo.org/record/3264762
- https://open.library.ubc.ca/media/download/pdf/24/1.0165790/1/
- http://digitalcommons.linfield.edu/symposium/2018/all/81
- http://www.dcs.kcl.ac.uk/staff/smodgil/ICAILcameraReady.pdf
- https://digitalcommons.ursinus.edu/pol_hon/8
- https://doaj.org/article/323a755c0f0e469d89410f64af96cce6
- https://doi.org/10.1136/bmj.b3128
- http://www.cs.montana.edu/mwittie/publications/Yaw15CGP.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.87.287
- https://zenodo.org/record/4972158
- https://www.jipitec.eu/issues/jipitec-12-2-2021/5295
- https://figshare.com/articles/_Similarity_metrics_between_CDC_8217_s_ILI_and_4_machine_learning_ensemble_methods_for_last_week_top_this_week_second_next_week_third_and_two_weeks_from_now_bottom_for_the_time_period_Aug_2013_8212_Feb_2015_/1589066
- https://scholar.uwindsor.ca/ossaarchive/OSSA2/papersandcommentaries/8
- https://eprints.ucm.es/id/eprint/42844/1/GWpilot%20Enabling%20multi-level%20scheduling-preprint.pdf
- https://hal-auf.archives-ouvertes.fr/hal-01358358
- https://ojs.aaai.org/index.php/ICWSM/article/view/14698
- https://zenodo.org/record/1075897
- http://hdl.handle.net/11577/2436351
- https://orcid.org/0000-0002-9786-8716
- https://eprints.gla.ac.uk/273387/1/273387.pdf
- https://figshare.com/articles/_Correlations_based_on_condition_level_similarity_matrices_formed_by_averaging_subject_level_matrices_for_the_subjects_belonging_to_each_condition_/1598616
- http://www.loc.gov/mods/v3
- http://publica.fraunhofer.de/documents/N-169351.html
- https://ojs.aaai.org/index.php/AAAI/article/view/10492
- http://hdl.handle.net/2108/259095
- http://cdn.intechopen.com/pdfs/35703.pdf
- https://hal.archives-ouvertes.fr/hal-01523774
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.63.841
- http://www.aaai.org/Papers/AAAI/2007/AAAI07-347.pdf
- http://arxiv.org/abs/2211.00582
- https://research.utwente.nl/en/publications/search-result-caching-in-peertopeer-information-retrieval-networks(790b0c9d-2cf0-4168-b888-afb2fe3d8abf).html
- https://hdl.handle.net/10356/156705
- https://ojs.aaai.org/index.php/SOCS/article/view/27278
- https://repository.law.uic.edu/cgi/viewcontent.cgi?article=1125&amp;context=jitpl
- http://hdl.handle.net/10.1371/journal.pone.0256133.g005
- http://hdl.handle.net/11858/00-001M-0000-0013-1689-E
- http://arxiv.org/abs/2109.07958