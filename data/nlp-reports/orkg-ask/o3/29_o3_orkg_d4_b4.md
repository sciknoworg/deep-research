# Final Report: Toward a Prompt-Engineering Framework for Resolving Ambiguous Translations

Evelyn Cox – 5 Sep 2025  
(Internal Research Note)

---

## 1. Executive Summary
Resolving translation ambiguity with large language models (LLMs) is no longer a purely linguistic challenge; it is a systems problem that spans prompt design, latency/energy constraints, evaluation methodology, and human-in-the-loop (HITL) ergonomics.  
The 78 research results reviewed here (spanning MT, prosody, GNSS ambiguity, telescope control, pruning, bootstrapping, etc.) collectively suggest **five converging design principles**:

1. **Multi-view disambiguation beats mono-view** (Li 2004): bilingual, prosodic, discourse and risk-aware signals must be *explicitly combined* in prompts or auxiliary modules.
2. **Interactive decomposition** (Interactive-Chain Prompting 2023) yields higher accuracy and lower cognitive load than single-shot prompting, mirroring classic CAT/TransType2 findings.
3. **Latency, memory and energy are first-class constraints.** Modern compression (PET, P-VQ, Dynamic-HAT, Compressed Attention) and latency metrics (TL/ETL) enable on-device or streaming deployment without sacrificing quality.
4. **Evaluation must isolate ambiguity phenomena.** New test suites such as DiBiMT/MuCoW, plus latency-aware metrics and bootstrap confidence intervals, provide the statistical footing to measure real progress.
5. **Cross-domain control theory and ambiguity resolution offer transferrable algorithms** (Kalman/LQG vibration rejection, RTK integer ambiguities, hydrological ANN bootstrap intervals) that inspire risk-aware or multi-rate decoding for NLP.

Building on these, we recommend a modular framework that couples:  
(a) *interactive chain-of-thought prompting* for lexical/syntactic/pragmatic ambiguities;  
(b) *bilingual bootstrapping* with LLM-generated pseudo-labels for low-resource pairs;  
(c) *prosody-conditioned decoding* for speech inputs; and  
(d) *Lattice MBR* + *risk-aware rescoring* integrated directly into the decoder.  
An accompanying benchmark suite should log BLEU/COMET **with 95 % bootstrap CIs**, TL/ETL latency, and DiBiMT/MuCoW sense accuracy.

---

## 2. Problem Definition and Scope
The user (henceforth “client”) requests guidance on resolving ambiguous translations through LLM prompting. Three clarifications are still open:

* **Dimensions of ambiguity:** lexical sense, syntax, pragmatics, pronoun reference, cultural conventions, tone/formality.
* **Language scenario:** Should the solution be language-agnostic or target specific low-resource/high-typological-distance pairs?
* **Workflow:** Fully automated vs HITL, plus how to evaluate success.

Our response therefore covers **all** ambiguity dimensions, **both** high- and low-resource pairs, and **hybrid** workflows.  
Where research is seemingly off-topic (e.g., GNSS bias stability, telescope control), we extract transferable ideas (multi-rate Kalman control ⇔ multi-rate decoding; integer ambiguity ⇔ lexical ambiguity; etc.).

---

## 3. Typology of Ambiguity & Signals for Disambiguation

| Ambiguity Dimension | Key Cues & Prior Work | Integration into Prompt / System |
|---------------------|-----------------------|----------------------------------|
| Lexical Sense | WordNet+syntax selector (63.89 % accuracy Tagalog study), DiBiMT, MuCoW, Li 2004 bilingual bootstrapping | Explicit *“sense inventory”* in the prompt; bilingual co-training to refine gloss selection; few-shot GlossGPT style exemplars |
| Syntactic Structure | Prosodic phrase boundaries (Verbmobil 2000, 94 % detection; MEG 2023 shows neural facilitation), boundary-conditioned parsing | Inject boundary tags `<PB/>` into prompt; pre-process ASR lattice with prosody; enable incremental partial decoding |
| Pragmatics & Speech Act | Verbmobil’s 5-layer constraint stack; KANT controlled language | Add role/context descriptors; enforce domain ontologies in system prompts |
| Discourse & Coreference | Interactive chain prompting step 3 (“clarify pronouns”); streaming ETL penalizes re-writes | Prompt sub-task to resolve antecedents; enforce *erasure-time-lag* limits to discourage late repairs |
| Cultural Form & Tone | TAP studies: induction/deduction/abduction cycles; think-aloud improved uncertainty management | Ask the LLM to propose multiple tone variants, score with *formality* rubric |
| Latency-induced Ambiguity | Simultaneous interpretation EVS/TTS (3.66 s / 5.34 s) | Coupled pseudo-look-ahead + duration-scaled TTS; prompt includes *“anticipate continuation”* directive |

---

## 4. Algorithmic Building Blocks

### 4.1 Interactive-Chain Prompting (ICP)
Eight Q&A turns decompose the sentence, resolving each micro-ambiguity. Empirically outperforms single-shot even when correct context is provided (arXiv 2301.10309).  
**Augmentation:** Insert *prosody* and *risk* sub-steps: (i) ask for prosodic phrase segmentation, (ii) ask for confidence-weighted alternative glosses; feed these into risk-aware decoding (Section 4.4).

### 4.2 Bilingual Bootstrapping + LLM Rationales
Li 2004 showed parallel co-training beats monolingual self-training. No work yet combines this with LLM-style rationales (SERP gap). Proposal: 
(1) use chain-of-thought to generate pseudo-labels + rationales in both languages; (2) exchange them across paired classifiers; (3) re-prompt LLM with *“consider peer rationale, critique and revise”*. This mirrors **multi-agent debate** but grounded in bilingual data.

### 4.3 Prosody-Aware Decoding
Verbmobil boundary detection (91.7 % phrase, 82.5 % accent) and 2023 MEG findings confirm prosody helps syntactic disambiguation. A multi-head fusion block (UW thesis 2020) already improved parsing. We embed word-level prosody tokens—`<F0_UP>`, `<PAUSE_250ms>`—in the source prompt, allowing the LLM to adjust syntactic expectations. For streaming S2ST we reuse the *pseudo-look-ahead + duration-scaled TTS* trick (−0.5 s latency, preserves BLEU).

### 4.4 Risk-Aware (Lattice) Minimum Bayes Risk Decoding in Prompting Era
LMBR within neural decoding (Sapienza/Helsinki) still delivers BLEU gains. We extend: treat each LLM-generated alternative as a *weighted finite-state transducer* (WFST) arc (learning: “weighted sets of alternatives outperform 1-best”). Risk weights combine:
* lexical sense distribution (DiBiMT prior),  
* prosody-conditioned syntactic likelihood,  
* streaming penalty (ETL),
* user correction cost (TransType2 latency-quality curve).

Search is **multi-rate**: coarse outer loop at phrase level, fine inner loop at token level—direct analogy to multirate Kalman/LQG vibration rejection (Gemini/Keck) that upsamples low-rate measurements for fast control while maintaining global stability.

### 4.5 Compression & Deployment Constraints
Interactive systems must keep <200 ms response (TransType2) and sometimes run on edge devices (Jetson Nano; Lancaster Letz Translate). Combine:
* **PET** weight sharing (−81 % mem, −45 % time) + **Compressed Attention** (1.42× speed-up) + **P-VQ** (−74 % FLOPs).  
* **Dynamic-HAT** allows runtime latency/quality trade-off (<1 s switch).  
* **Optimal sparsity law** guides n:m pruning without large retraining.

These maintain quality (≤0.5 BLEU loss) which is within the **±0.27 BLEU noise band** estimated by bootstrap CI studies (CESTA, “Tangled up in BLEU”).

---

## 5. Evaluation & Benchmarking

### 5.1 Quality Metrics
* **BLEU/COMET** with 1,500 bootstrap resamples → 95 % CIs (Dryad 2020 code).  
* **Sense accuracy**: DiBiMT leaderboard & MuCoW contrastive sets.  
* **Discourse/coherence**: ACT metric, MQM ‘Ambiguity/Sense’ tags.  
* **Prosody impact**: phrase-boundary detection AUPRC; ACT or BLEU delta on spoken-language sets.

### 5.2 Latency Metrics
* **Time-Lag (TL)** and **Erasure-Time-Lag (ETL)** (Google 2023) for online systems.  
* EVS/TTS analogue for human interpreters to compare automated vs human lag.

### 5.3 Statistical Rigor
Bootstrap intervals shrink with corpus size and #refs; CESTA shows a subset of sentences often suffices, reducing eval cost. Pairwise thresholding controls Type I/II errors.

### 5.4 Test Data
Combine:  
* DiBiMT & MuCoW for WSD,  
* hardEN/42D challenge for rare senses,  
* new four-language free-word-order benchmark (learning set),  
* Zenodo 8286649 ChatGPT/Google outputs for head-to-head baselines.

---

## 6. Proposed Framework Architecture
```
┌─────────────────────────────────────────┐
│ 1) ASR / Text Input                    │
│    + Prosody Tags (optional)           │
└─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ 2) Interactive-Chain Prompting Module  │
│    • Q1: Segment & tag prosody         │
│    • Q2: List lexical senses + probs   │
│    • Q3: Clarify pronouns              │
│    • Q4: Check tone/formality          │
│    • Q5: Produce draft translation     │
│    • Q6–7: Risk critique & revise      │
│    • Q8: Final translation             │
└─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ 3) Risk-Aware LMBR Decoder            │
│    • Inputs: WFST alternatives, priors │
│    • Multi-rate beam search            │
│    • Output: n-best with risk scores   │
└─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ 4) HITL Review Panel (optional)        │
│    • UI latency <200 ms                │
│    • TransType2 keystroke hooks        │
│    • Edits fed back as new few-shots   │
└─────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ 5) Streaming Output / TTS              │
│    • Pseudo-look-ahead to cut delay    │
│    • Duration-scaled synthesis         │
└─────────────────────────────────────────┘
```
Compression blocks (PET, Dynamic-HAT, P-VQ) encapsulate the LLM to meet edge deployment budgets.

---

## 7. Cross-Domain Analogies & Lessons
* **GNSS integer ambiguity ↔ lexical ambiguity**: Stable inter-system biases over ≥1 yr allow aggressive cut-offs while preserving resolution success (80 % above 50°). Analogous strategy: cache high-confidence sense mappings per domain to prune future search.
* **Kalman/LQG multirate control** (telescope tip/tilt): Up-sampling slow but accurate signals resembles combining low-rate human feedback with high-rate automatic prompting.
* **Hydrological bootstrap failures** warn that BCa intervals break when the model is misspecified—same for BLEU CIs if reference domain shifts; hence maintain domain-matched dev sets.
* **Voltage down-scaling in LDPC decoders** demonstrates *adaptive fidelity*; Dynamic-HAT mirrors this by selecting SubTransformers on the fly.
* **Psychometric giftedness testing (MHBT-S)** reminds that reliability & validity are distinct; same applies to MT metrics—hence ACT/MQM adoption.

---

## 8. Recommendations & Roadmap (6 Months)

| Month | Milestone | Deliverables |
|-------|-----------|--------------|
| 1 | Finalize ambiguity taxonomy & prompt templates | Prompt library with placeholders + rationale examples |
| 2 | Integrate prosody tagger & Compressed Attention LLM | 1st working prototype, TL/ETL logger |
| 3 | Implement WFST risk decoder + bilingual bootstrapping loop | Side-by-side eval on MuCoW, DiBiMT, ChatGPT baseline |
| 4 | Launch HITL UI (TransType2-style) | Keystroke latency & micro-bleu logging |
| 5 | Edge compression (PET+P-VQ) and Dynamic-HAT toggling | Jetson Nano benchmark, power profiling |
| 6 | Full evaluation with bootstrap CIs, ACT, MQM annotations | Technical report, open-sourced toolkit, submission to DiBiMT leaderboard |

Stretch goal: explore **GlossGPT + bilingual bootstrapping** fusion; conceptually yields self-improving sense inventory.

---

## 9. Risks & Mitigations
1. **LLM hallucination of senses** – use risk decoder + HITL verification; compare to WSTE classifier for alarms.  
2. **Latency blow-ups in low-connectivity settings** – on-device compression, offline fallback to P-VQ student model.  
3. **Metric mis-alignment** – dual reporting BLEU/COMET *and* sense-level metrics; bootstrap to detect non-significant deltas.  
4. **Data privacy** – edge inference avoids cloud calls; prompt stripping of PII before logging.

---

## 10. Conclusion
By synthesizing decades of MT, prosody, risk modeling, compression, and even satellite ambiguity research, we can architect a **holistic, prompt-centric translation system** that explicitly tackles ambiguity while respecting human latency and device constraints.  
The proposed ICP + LMBR + bootstrapping framework is technically feasible with open-source components, aligns with current evaluation best practice, and leaves room for speculative gains (multi-agent bilingual rationale exchange) that the literature has not yet exploited.

> *“Treating ambiguity as weighted sets of alternatives rather than single hypotheses yields higher BLEU.”* — this insight from spoken-language MT three decades ago now finds its natural partner in modern LLM prompting. Implemented correctly, it promises a **step-change in translation reliability** across both high- and low-resource languages.


## Sources

- http://hdl.handle.net/Bootstrap
- http://www.mt-archive.info/CL-2004-Li.pdf
- https://escholarship.org/uc/item/4h03k92b
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.1732
- https://nrc-publications.canada.ca/eng/view/accepted/?id=f2a4386f-564f-44d4-9c01-c437390b8bb3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.44.7361
- https://zenodo.org/record/8291850
- https://zenodo.org/record/7829222
- http://publications.idiap.ch/downloads/papers/2013/Hajlaoui_ACL-WMT-13_2013.pdf
- http://archive-ouverte.unige.ch/files/downloads/3460/unige_3460_attachment01.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17572
- https://zenodo.org/record/3476394
- https://archive-ouverte.unige.ch/unige:3460
- https://figshare.com/articles/_Top_10_4_test_combinations_ranked_according_to_sum_of_sensitivity_and_specificity_compared_to_a_120_minute_global_neuropsychological_battery_/215550
- https://nrc-publications.canada.ca/eng/view/object/?id=e92c5cc5-4ec5-43bf-8419-5372ceb0ca95
- http://arxiv.org/abs/2202.06387
- https://zenodo.org/record/8091292
- https://hdl.handle.net/11250/2831132
- http://hdl.handle.net/2027/wu.89006085633
- http://interspeech2015.org/
- https://zenodo.org/record/7481721
- http://personalpages.manchester.ac.uk/staff/harold.somers/ebmtvstm_ijt.pdf
- http://hdl.handle.net/20.500.11794/15728
- http://hdl.handle.net/10.1371/journal.pone.0288060.t006
- http://edoc.mpg.de/322800
- https://arodes.hes-so.ch/record/12331/files/Popescu_2023_simplified_training.pdf
- http://hdl.handle.net/11858/00-001M-0000-0013-75AC-2
- https://www.repository.cam.ac.uk/handle/1810/260251
- http://hdl.handle.net/10138/305137
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1490%26context%3Dpwpl
- http://arxiv.org/abs/2310.08908
- http://hdl.handle.net/2117/89809
- http://hdl.handle.net/10068/149726
- http://hdl.handle.net/10.1371/journal.pone.0205392.t001
- http://www.mtdbest.iki.rssi.ru/pdf/qmtd_iscta07.pdf
- https://haab-digital.klassik-stiftung.de/viewer/resolver?urn=urn:nbn:de:gbv:32-1-10000365092
- https://imt-atlantique.hal.science/hal-04184072/document
- https://zenodo.org/record/7829233
- http://hdl.handle.net/11346/BIBLIO@id=-2597061875789547516
- http://www.mt-archive.info/EMNLP-2008-Sanchis-Trilles.pdf
- https://zenodo.org/record/5704449
- http://catalogue.bnf.fr/ark:/12148/cb419179387
- https://repository.upenn.edu/dissertations/AAI9628034
- https://zenodo.org/record/8286649
- http://www.mt-archive.info/ACL-2009-Li-1.pdf
- https://cronfa.swan.ac.uk/Record/cronfa68937
- https://zenodo.org/record/8170714
- https://bibliotekanauki.pl/articles/176415
- http://www.ias.ac.in/sadhana/Pdf2009Jun/381.pdf
- https://www.earticle.net/Article/A117684
- http://hdl.handle.net/2066/75109
- https://nrc-publications.canada.ca/fra/voir/objet/?id=eb32e642-68db-4632-aca4-c4921bb8592f
- https://zenodo.org/record/8141321
- https://www.sfsic.org/evenements-sfsic/congres-sfsic/congres-sfsic-metz-2016-temps-temporalites-et-information-communication/
- http://publica.fraunhofer.de/documents/N-46294.html
- https://hal.inria.fr/hal-03780006/document
- http://www.cslu.ogi.edu/%7Egormanky/courses/CS662/PDFs/lecture_notes/2015-03-03-handout.pdf
- http://hdl.handle.net/10251/103640
- http://hdl.handle.net/1885/83063
- https://zenodo.org/record/6523631
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.7485
- http://hdl.handle.net/10.6084/m9.figshare.24921090.v1
- https://www.scopus.com/inward/record.uri?eid=2-s2.0-34547325221&doi=10.1109/ICPPW.2006.35&partnerID=40&md5=65cbf9b05409b04a145ceff3904ba679
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll123/id/61441
- http://www.imeko.org/publications/tc1-tc7-2008/IMEKO-TC1-TC7-2008-015.pdf
- https://isca-speech.org/archive/pdfs/interspeech_2022/liu22u_interspeech.pdf
- http://www.nusl.cz/ntk/nusl-304321
- http://hdl.handle.net/11471/908.10.9080
- https://doaj.org/article/1635d185bebf4ceda1ed71b5beba511d
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.99.8435
- http://hrmars.com/hrmars_papers/Constructivism_Translation_Training_in_Translation_Process_Workshops_The_effect_of_Think-aloud_Protocols_in_increasing_Student_Uncertainty_Management.pdf
- https://doi.org/10.1051/ao4elt/201005002
- http://edoc.mpg.de/559092
- https://www.aclweb.org/anthology/2020.lrec-1.452.pdf
- http://arxiv.org/abs/2301.10309
- https://zenodo.org/record/6625312
- http://hdl.handle.net/20.500.11794/9688
- http://hdl.handle.net/2066/86073
- http://hdl.handle.net/2072/405531
- https://doi.org/10.18653/v1/2020.acl-main.448.
- https://ojs.aaai.org/index.php/AAAI/article/view/17688
- http://hdl.handle.net/20.500.11794/33267
- http://publikationen.ub.uni-frankfurt.de/frontdoor/index/index/docId/74534
- https://figshare.com/articles/_Estimation_of_transcriptional_time_lag_/754316
- http://www.hathitrust.org/access_use#pd-us-google.
- http://dutangc.free.fr/pub/stat/boot.pdf
- https://nbn-resolving.de/urn:nbn:de:hbz:061:1-381883
- http://folk.uio.no/plison/pdfs/projects/fripro2013.pdf
- http://hdl.handle.net/20.500.11937/21282
- http://www5.informatik.uni-erlangen.de/Forschung/Publikationen/2000/Batliner00-TPM.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/4487
- https://zenodo.org/record/7948696
- http://hdl.handle.net/1842/1280
- https://zenodo.org/record/7321964
- http://hdl.handle.net/123456789/14955
- http://www.mt-archive.info/AMTA-2006-Pytlik.pdf
- http://arxiv.org/abs/2202.05148
- http://aclweb.org/anthology/E/E14/E14-4011.pdf
- https://opus.hs-osnabrueck.de/frontdoor/index/index/docId/3739
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.69.4393
- https://archive-ouverte.unige.ch/unige:3461
- https://zenodo.org/record/3474282
- https://pub.uni-bielefeld.de/record/2963992
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/120458
- http://catalogue.bnf.fr/ark:/12148/cb419291210
- http://www.research.ed.ac.uk/portal/files/7507896/P00_1028.pdf
- http://hdl.handle.net/11573/1640533
- http://www.mt-archive.info/NAACL-HLT-2010-Cer-1.pdf
- https://rio.tamiu.edu/psych_comm_facpubs/1
- http://hdl.handle.net/10255/dryad.206247
- https://portal.research.lu.se/ws/files/6182329/624435.pdf
- https://www.zora.uzh.ch/id/eprint/224506/1/2022.aacl_main.83.pdf
- http://hdl.handle.net/20.500.12678/0000004631
- https://zenodo.org/record/7474115
- https://zenodo.org/record/6800975
- https://hal.archives-ouvertes.fr/hal-00632782
- http://hdl.handle.net/10356/78408
- http://urn.kb.se/resolve?urn=urn:nbn:se:liu:diva-197946
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.5708
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.90.8451
- http://www.scholink.org/ojs/index.php/sll/article/view/3306
- http://hdl.handle.net/1773/46782
- http://arxiv.org/abs/2205.11277
- http://hdl.handle.net/11471/908.10.9082
- http://www.mt-archive.info/LREC-2008-Monson.pdf
- http://www.ai.soc.i.kyoto-u.ac.jp/publications/thesis/M_H19_tanaka-rie.pdf
- https://elib.dlr.de/130969/
- https://elib.dlr.de/19554/
- http://summit.sfu.ca/item/9913
- http://hdl.handle.net/11573/1553733
- http://purl.tuc.gr/dl/dias/0C32C1C4-3C4F-4B80-8BEE-E7FEF0FA128D
- http://arxiv.org/abs/2209.07617
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.2267
- https://zenodo.org/record/3991352
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.229
- https://zenodo.org/record/7242501
- https://www.persee.fr/doc/jhydr_0000-0001_2014_act_36_1_2342
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.94.6245
- http://hdl.handle.net/10045/76022
- http://www.mt-archive.info/ACL-2007-Rosti.pdf
- http://hdl.handle.net/10.36227/techrxiv.24486214.v1
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.6024
- https://zenodo.org/record/3981352
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/58698
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.7626
- http://www.lrec-conf.org/proceedings/lrec2002/pdf/136.pdf
- https://doaj.org/article/03487a8a756e4848b97196bf1e81cfa0
- https://repository.rudn.ru/records/article/record/72491/
- http://hdl.handle.net/2027/njp.32101074363779
- http://hdl.handle.net/20.500.11937/84265
- http://www.nusl.cz/ntk/nusl-461323
- http://www.mt-archive.info/MTS-2009-Xiong-1.pdf
- http://hdl.handle.net/10251/83641
- http://hdl.handle.net/11346/BIBLIO@id=-4769769869536062865
- http://hdl.handle.net/2027/uc1.$b304775
- https://animorepository.dlsu.edu.ph/etd_masteral/3306
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.5429
- https://ojs.aaai.org/index.php/AAAI/article/view/9983
- http://hdl.handle.net/1903/17152
- http://hdl.handle.net/10447/59647
- http://hdl.handle.net/11346/BIBLIO@id=-8641281304745265785
- http://www.mt-archive.info/Coling-1988-Zajac.pdf
- http://hdl.handle.net/1842/1225
- https://ojs.aaai.org/index.php/AAAI/article/view/11929
- http://www.lingref.com/cpp/slrf/2012/paper3095.pdf
- http://arxiv.org/abs/2205.06644
- https://publications.rwth-aachen.de/search?p=id:%22RWTH-2019-06230%22
- https://zenodo.org/record/7474099
- http://psydok.sulb.uni-saarland.de/doku/lic_ohne_pod.php
- https://www.tdcommons.org/cgi/viewcontent.cgi?article=6275&amp;context=dpubs_series
- https://doaj.org/article/811705f035cd451da0103d982bd4aea1
- https://eprints.lancs.ac.uk/id/eprint/210068/
- http://arxiv.org/pdf/1407.7895.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.86.5452
- https://zenodo.org/record/7085587
- https://zenodo.org/record/5759541
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.4980
- http://cl.sd.tmu.ac.jp/%7Ekomachi/papers/dthesis-mamoruk.pdf
- http://www.mt-archive.info/NAACL-HLT-2007-Shieber.pdf
- http://www.hathitrust.org/access_use#pd-google.
- http://www-i6.informatik.rwth-aachen.de/~bender/papers/eamt05.pdf
- https://dx.doi.org/10.3390/w10020166
- https://research-explorer.ista.ac.at/record/18062
- http://aclweb.org/anthology/D/D13/D13-1022.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/26528
- https://benjamins.com/#home
- http://hdl.handle.net/1903/11217
- http://www.cs.umd.edu/~ynhu/publications/eacl2014_rnn_mtu.pdf
- http://hdl.handle.net/11562/391067
- http://aclweb.org/anthology/D/D14/D14-1023.pdf
- http://hdl.handle.net/10.1371/journal.pone.0288060.t001
- http://hdl.handle.net/10068/116431
- https://zenodo.org/record/8190372
- https://zenodo.org/record/8058248
- http://www.ion.org/publications/abstract.cfm?jp=p&articleID=13394
- https://scholarworks.sjsu.edu/etd_projects/1324
- http://research.microsoft.com/pubs/145627/eamt-05.pdf
- http://dspace.stir.ac.uk/bitstream/1893/23468/1/Xiaojun%20ZhangActive%20Interactive%20Protocol%20in%20CAT%20System.pdf
- http://hdl.handle.net/10.1184/r1/6623216.v1
- http://scholarbank.nus.edu.sg/handle/10635/145605
- https://www.repository.cam.ac.uk/handle/1810/287962
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.54.7465
- http://www.mt-archive.info/MTS-1999-Cowie.pdf
- http://hdl.handle.net/10220/12393
- http://pqdtopen.proquest.com/#viewpdf?dispub=10643063
- https://hal.science/hal-03735046
- https://pub.uni-bielefeld.de/record/2943661
- http://aclweb.org/anthology/E/E14/E14-1003.pdf
- https://bells.uib.no/index.php/bells/article/view/49
- https://orcid.org/0000-0001-5736-5930
- https://doaj.org/article/e9a4f3ed1b6d45ce82ab0174a3ed544c
- http://doras.dcu.ie/15278/
- https://escholarship.org/uc/item/35q268p3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.431.7131
- http://hdl.handle.net/10068/116159
- http://www.mt-archive.info/Coling-1990-Brown.pdf
- http://www.mt-archive.info/EACL-1989-Kitano.pdf
- http://www.loc.gov/mods/v3
- http://arxiv.org/abs/2202.07856
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.451
- https://zenodo.org/record/8008727
- https://hal.archives-ouvertes.fr/hal-02097707
- https://biblio.ugent.be/publication/3054587/file/3054596
- http://hdl.handle.net/11025/21578