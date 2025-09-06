# Translation with LLMs through Prompting with Long-Form Context  
*(Comprehensive technical report synthesising 2023-2025 research findings)*  

---

## 0. Executive Summary
Large-language-model (LLM) translation has reached near-human parity **in narrow sub-languages** (e.g.
controlled avalanche bulletins) and on **high-resource pairs**; however accuracy degrades for low-resource
pairs, legally asymmetric terminology, streaming use-cases and very long documents. 55 % of users can no
longer distinguish catalogue-generated from human text in production systems, yet mixed-method corpus
studies still expose persistent deficiencies in discourse coherence, coreference, domain terminology and
latency stability.

Breakthroughs since 2023 derive less from bigger models and more from **prompt engineering, retrieval and
constraint injection**:

* Chain-of-Thought (CoT) and three-stage prompt-chaining pipelines lift quality by >10 BLEU / F1; small
  open-source models can beat GPT-3.5 zero-shot on 100-page Swiss legal filings.
* Pivot prompting (source→high-resource pivot→target) recovers most of the gap on distant/low-resource
  pairs at ≈2× token cost.
* Embedding **lemmatised positive constraints** in the input eliminates 46 % agreement errors in
  EN→CS; stemmed negative constraints drastically reduce forbidden-term evasion.
* **Translator↔Reflector two-agent prompting** raises BLEU/COMET on EN→TH and other low-resource
  settings.

On the evaluation side, the **Time-Lag / Erasure-Time-Lag (TL/ETL)** metrics family now quantifies
per-token responsiveness *and* output stability in streaming APIs, while accuracy metrics have expanded
with ACT (connective adequacy), TINE, tunable TER-Plus and discourse-cohesion scores that correlate +3–5 %
more strongly with human judgements than BLEU/COMET alone.

Infrastructure matters: single-node benchmarks find Apache **Pulsar** gives the lowest average
end-to-end latency, Kafka the highest throughput but worst latency, Redis Streams the most variance.
Micro-architectural cache effects can otherwise under-estimate worst-case lag.

Legal-domain projects (UN, EU, WTO, Swiss and Belgian ministries) demonstrate that **terminology
management—not raw model accuracy—is the current bottleneck**. New cloud TMS prototypes (e.g.,
Belgium’s TermWise) mine bilingual corpora, surface context-sensitive variants and map workflows to EN
15038 quality criteria.

The report formulates **12 actionable recommendations** covering model selection, prompt design, domain
terminology, streaming latency, metric dashboards and amortisation of development cost.

---

## 1. Current Landscape of Long-Form LLM Translation

### 1.1 High-resource vs Low-resource Performance
* GPT-4 five-shot translation matches Google Translate on high-resource pairs; it **lags on low-resource
  pairs** unless pivot prompting is applied (Zenodo 8286649; arXiv 2301.08745).
* Zero-shot + 5-shot in the “Chat-GPT MT” corpus confirm competitiveness only for
  high-resource languages; performance on low-resource pairs remains the primary weakness.
* A two-agent English→Thai *translator–reflector* workflow (Typhoon LLM + Claude 3.5) outperforms single-pass GPT-3.5 Turbo, indicating that self-critique prompts can fill the low-resource gap.

### 1.2 Domain-specific Success Stories
* **Swiss Avalanche Bulletin**: fully automated German→FR/IT/EN phrase-catalogue MT (2012-)
  reached 55 % machine/human recognition rate and indistinguishable quality ratings, cutting daily costs
  enough to amortise development within *a few years* while keeping forecasters’ workload flat.
* **TransLI** (Canada) uses SMT plus mandatory human post-editing for EN↔FR court judgements, already
  adopted by multiple government departments.
* **ModernMT** surpassed DeepL on an *atto costitutivo* (company law) EN metrics: BLEU 29.14 vs 27.02, accuracy/terminology error 8.43 % vs 9.22 %.

### 1.3 Persistent Pain Points
* Low-resource pairs; domain-specific polysemy and legal asymmetry (“prima facie evidence”, “tort”,
  “magistrates’ court”) drive accuracy down and inconsistency up by up to 30 %.
* Coreference across sentences and compounds (Nordwand→Wand) is mishandled unless explicitly
  constrained.
* Long-sentence degradation: Croatian→EN error rates climb with sentence length to ~40 tokens then
  plateau, suggesting chunking may still be beneficial even with 128k–200k context windows.

---

## 2. Empirical Findings on Quality and Consistency

### 2.1 Blind-User & Corpus Studies
* Blind surveys (n≈?) show users recognise catalogue MT only 55 % of the time, rating quality 
  statistically equal to human translations within this sub-language.
* Mixed-method lexicometric + acceptability audits across EU/UN/WTO find that **terminological
  consistency and adequacy co-vary with translator thematic expertise and institutional process
  conditions**.
* Diachronic corpora 2005-2019 prove that legal-system asymmetry drives both accuracy drops and
  intertextual variation.

### 2.2 Discourse & Coreference Benchmarks
* **BWB novel corpus** (15 095 aligned entity mentions, four discourse dimensions) shows current MT
  diverges sharply from human latent discourse.
* Document-level cohesion modelling (lexical-chain probability) yields statistically significant BLEU gains,
  and lexical-cohesion metrics lift system–human correlation by 3–5 %.
* Accuracy of Connective Translation (ACT) stays within 2 % of human judgements while exposing
  discourse-level errors missed by BLEU/NIST.

### 2.3 Constraint-based Improvements
* Embedding lemmatised **positive constraints** in EN→CS translation reduces agreement errors from 46 %
  to ≈0 % without BLEU loss (End-to-End Lexically Constrained MT 2024).
* Using stemmed **negative constraints** during training curbs forbidden-term evasion.
* Alignment-guided constrained decoding (EAM-Output) adds +2.53 BLEU on Vi-En news.

---

## 3. Prompt Engineering & Retrieval Techniques for Long Context

| Technique | Evidence Δ | Token-Cost | Notes |
|-----------|-----------|-----------|-------|
| Chain-of-Thought (CoT) | Largest accuracy jump for ≥13 b models (Lancaster 2024) | +10–15 % | Smaller models plateau |
| Three-stage prompt-chaining (summary→retrieval→few-shot) | >+10 micro-F1 over ChatGPT-3.5 zero-shot (SwissText 2023) | Moderate | Beats larger LLMs |
| Pivot prompting | Parity on distant pairs; ≈2× cost | +100 % | Eliminates most hallucinations |
| Translator–Reflector | +BLEU / COMET on EN→TH | +50 % | Adds self-critique pass |
| Coreference/compound reminder tags | +readability, correctness in DE →EN | negligible | Works in SMT & LLMs |

Retrieval sources have expanded: DGT-TM (231 pairs), DGT-UD 1.0 (2 B words), SwissAdmin (6–8 M words/language), PARM dense retrievers (LegalBERT_doc/para) for statute matching. Dense+BM25+FiD retrieval in MultiDoc2Dial lifts both F1 and SacreBLEU by >10 points, underlining benefits for dialogue and long-form tasks.

---

## 4. Latency, Streaming & Infrastructure

### 4.1 Metrics Evolution
* **Time-Lag (TL)** timestamps first emission; **Erasure Time-Lag (ETL)** marks final token stability.
  ETL therefore captures correction churn and better reflects perceived latency.
* TL/ETL dashboards enable fair comparison across GPT-4-Turbo-128k and Claude-3-200k streaming modes.

### 4.2 Systems Benchmarks
* Apache **Pulsar** = lowest average latency; **Kafka** = highest throughput but worst latency; **Redis
  Streams** competitive latency but high variance.
* Cache-aware timing analysis shows ignoring CPU cache effects under-estimates worst-case lag, risking
  buffer under-provisioning in real-time MT pipelines.
* Flink join operators increase stage latency 4.5×; latency variance propagates downstream.

### 4.3 Human Analogy
Simultaneous interpreting Ear-Voice Span (3.66 s) and Tail-to-Tail Span (5.34 s) mirror
machine TL/ETL trade-offs—extended lags reduce accuracy.

---

## 5. Terminology Management: The Bottleneck

Institutional translators often ignore IATE/UNTERM due to relevance gaps. Projects addressing this:

* **Belgium FPS Justice**: TermWise cloud TMS + context-extraction prototypes; mines bilingual legal
  corpora; aligns with EN 15038; surfaces *archetypal phraseological contexts* during CAT usage.
* **ITE-MateCat/SFI** project: XML or cache model injection of domain terminology adds up to +15 BLEU.
* **Docent + bilingual word-vector constraints**: ≈+0.6 ULC on technical texts.

Corpus evidence: intratextual consistency correlates chiefly with document length and series context; legal
asymmetry drives *intertextual* variation. Therefore any long-form LLM workflow must track both term
frequency within the document and precedent translations across a corpus.

---

## 6. Evaluation Benchmarks & Metrics

1. **BLEU / COMET** remain baseline but plateau for document-level nuance.
2. **ACT, TINE, tunable TER-Plus** add connective and semantic-role granularity.
3. **Discourse cohesion / coreference preservation** metrics narrow the gap by another 3–5 %.
4. TL/ETL provide latency + stability axes absent from traditional accuracy scores.
5. **User perception**: 55 % recognition rate under controlled studies still functions as an
   external UX benchmark.

Public datasets now span literary (Jules Verne multilingual corpus, 11 versions, 3 400 proper names), legal
(Swiss Legal Benchmark, SwissAdmin, DGT-UD, BWB), technical (TermWise corpora) and dialogue (MultiDoc2Dial).

---

## 7. Recommendations

### 7.1 Model & Prompt Selection
1. High-resource pair: GPT-4-Turbo-128k with CoT + 3-shot; low-latency needs ⇒ use wait-k decoding at k≈3;
   monitor ETL < 1 s.
2. Low-resource or legally asymmetric: **pivot prompting** (source→EN→target) *or* two-agent
   Translator–Reflector pipeline; add domain term constraints.
3. Compound-rich languages (DE, NL): inject coreference reminders or compound alignment tags.

### 7.2 Terminology Workflow
4. Deploy TermWise-like TMS: mine DGT-TM, SwissAdmin and internal memories; expose ranked context during
   prompt construction or CAT post-edit.
5. Embed lemmatised **positive constraints** for must-use terms; use stemmed **negative constraints** for
   forbidden terms.
6. Track term frequency intra- & inter-document; raise QA flags when consistency diverges >5 %.

### 7.3 Retrieval-Augmented Generation
7. For >5k-token documents, chunk into ≤40-token overlaps; run DPR/BM25 retrieval from DGT-UD +
   LegalBERT_para; feed top-k exemplars into the prompt (SwissText strategy).

### 7.4 Streaming Infrastructure & SLAs
8. Choose Pulsar if ≤200 ms token-lag is hard SLA; Kafka only when throughput >200 MB/s trumps latency.
9. Instrument TL/ETL at per-token granularity; incorporate cache-aware profilers.

### 7.5 Evaluation Stack
10. Use BLEU+COMET+ACT+discourse cohesion for accuracy; TL/ETL for latency; user A/B with
    55 % recognition target.
11. Apply mixed-method audits (lexicometric counts + qualitative acceptability) quarterly to monitor term
    adequacy and process conditions.

### 7.6 ROI & Cost Control
12. Experiences from the avalanche bulletin and controlled-language MT show complete cost recovery
    within years; similar gains are projected if streaming LLM translation replaces human first drafts for
    high-volume yet formulaic legal documents.

---

## 8. Roadmap & Speculative Outlook (flagged *speculative*)

*speculative* 2025-2027 trends:
* Context windows will expand beyond 1 M tokens; nevertheless **chunk-and-retrieve** will remain
  economical due to quadratic cost scaling.
* Legal-domain agents will negotiate terminology in multi-agent settings, combining TermWise signals with
  live legislative DBs to auto-draft bilingual statutes.
* TL/ETL will evolve into user-perceived “Interaction Latency Index” integrating eye-tracking & cognitive
  load, mirroring psycholinguistic EVS/TTS.
* Hybrid neural-symbolic terminological constraints may guarantee court-grade fidelity, catalysing
  regulatory change akin to pending European Patent Convention amendments.

---

## 9. Checklist for Immediate Implementation

- [ ] Define source-target pairs & domains; gather domain corpora (SwissAdmin, DGT-UD, TermWise, etc.).
- [ ] Choose model tier (GPT-4-Turbo or open-source 13-70 b) based on latency/price/quality trade-off.
- [ ] Implement retrieval + CoT prompt chain; add pivot prompting fallback.
- [ ] Inject positive/negative lexical constraints & compound coreference tags.
- [ ] Stand up Pulsar-backed streaming API; instrument TL/ETL.
- [ ] Deploy TMS with bilingual context mining; connect to CAT and LLM prompt generation.
- [ ] Establish metric dashboard (BLEU, COMET, ACT, cohesion, TL/ETL, cost/1k tokens).

---

### Concluding Remark
Research confirms that **prompt-centric, retrieval-augmented, constraint-aware workflows** can unlock
near-human translation quality for long documents—*provided* that latency, terminology and discourse are
explicitly engineered. The next competitive edge will not stem from larger generic LLMs but from
integration of domain-specific corpora, fine-grained latency metrics and real-time terminology systems.


## Sources

- http://catalogue.bnf.fr/ark:/12148/cb41930931j
- http://hdl.handle.net/10593/21240
- https://zenodo.org/record/6838828
- https://pub.uni-bielefeld.de/record/2017683
- https://ojs.aaai.org/index.php/AAAI/article/view/17496
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1042.946
- http://home.rcs.ei.tum.de/~samarjit/psfiles/cache_aware_journal.pdf
- http://bvh.hypotheses.org/6681
- http://hdl.handle.net/2440/70696
- http://www.hakusuisha.co.jp/book/b243686.html
- http://personal.cityu.edu.hk/~ctckit/papers/2011NLPKE_manuscript_FINAL.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-55985
- http://hdl.handle.net/11346/BIBLIO@id=2165773603281921920
- http://resolver.tudelft.nl/uuid:6bb284a6-9b9d-4136-ac5c-7d039e8216bb
- http://hdl.handle.net/2117/28516
- http://ceur-ws.org/Vol-2957/
- http://www.mt-archive.info/ACL-2009-Xiong-1.pdf
- http://www.comp.nus.edu.sg/%7Etancl/publications/c2013/EMNLP2013.pdf
- http://resolver.tudelft.nl/uuid:427b434d-6e9b-4fd9-81d8-49a265cd90ac
- http://scholarbank.nus.edu.sg/handle/10635/41960
- https://bibliotekanauki.pl/articles/451588
- https://figshare.com/articles/_Comparison_of_mean_CPU_time_on_the_Extended_Yale_B_database_with_different_corruption_levels_/673808
- http://catalogue.bnf.fr/ark:/12148/cb41930352v
- https://doi.org/10.1093/grurint/ikad099
- http://hdl.handle.net/1959.14/112691
- http://hdl.handle.net/20.500.11897/411574
- http://hdl.handle.net/10356/78898
- http://hdl.handle.net/11250/2404147
- http://nthur.lib.nthu.edu.tw/dspace/handle/987654321/13891
- http://arxiv.org/abs/2308.04138
- https://zenodo.org/record/8139254
- http://dmtf.org/sites/default/files/standards/documents/DSP0198_1.0.0.pdf
- http://alt.qcri.org/semeval2014/cdrom/pdf/SemEval123.pdf
- http://catalogue.bnf.fr/ark:/12148/cb41916083b
- https://doaj.org/article/79c1524018b64eafbc371a039e6054b6
- http://hdl.handle.net/11346/BIBLIO@id=-2597061875789547516
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1429%26context%3Disr
- https://library.oapen.org/bitstream/20.500.12657/46390/14/9780429264894_oachapter7.pdf
- http://hdl.handle.net/10.1371/journal.pone.0288453.s003
- https://zenodo.org/record/8286649
- https://www.earticle.net/Article/A117684
- http://hdl.handle.net/2078.1/149776
- https://library.oapen.org/handle/20.500.12657/46391
- http://darhiv.ffzg.unizg.hr/id/eprint/4574/1/Sabljak-diplomski.pdf
- https://dialnet.unirioja.es/servlet/oaiart?codigo=6707821
- http://hdl.handle.net/11380/612592
- https://iaflporto2017.com
- http://cscanada.net/index.php/hess/article/view/13164
- https://zenodo.org/record/8139264
- https://archive-ouverte.unige.ch/unige:166012
- https://openrepository.ru/article?id=327109
- http://hdl.handle.net/10379/14924
- http://aclweb.org/anthology/D/D13/D13-1163.pdf
- http://amslaurea.unibo.it/view/cds/CDS9174/
- https://repozitorij.ffzg.unizg.hr/islandora/object/ffzg:5057/datastream/PDF
- https://www.doria.fi/handle/10024/177865
- https://content.sciendo.com/view/journals/cl/43/1/article-p17.xml
- https://biblio.ugent.be/publication/8753671/file/8753672
- http://catalogue.bnf.fr/ark:/12148/cb41917314k
- https://www.persee.fr/doc/rga_0035-1121_1925_num_13_2_4930
- http://hdl.handle.net/11577/2271302
- https://archive-ouverte.unige.ch/unige:157860
- http://clg.wlv.ac.uk/papers/wmt-2011-rios.pdf
- http://scholarbank.nus.edu.sg/handle/10635/40347
- http://dspace.mit.edu/handle/1721.1/16322
- http://resolver.tudelft.nl/uuid:6f3d02a3-f836-426b-9fc9-b7914b961811
- http://www.tao2015.org/research/03_TaoCat_HeylenSteursKockaert_bis.pdf
- http://www.matthen.com/research/papers/The_Third_Dialog_State_Tracking_Challenge.pdf
- http://www.nusl.cz/ntk/nusl-281198
- https://portal.research.lu.se/ws/files/5892565/1894906.pdf
- https://figshare.com/articles/_Estimation_of_transcriptional_time_lag_/754316
- https://hdl.handle.net/1721.1/145034
- http://folk.uio.no/plison/pdfs/projects/fripro2013.pdf
- https://openrepository.ru/article?id=257792
- http://www.comm.utoronto.ca/%7Eakhisti/JSAC_InPress.pdf
- http://real.mtak.hu/172978/
- http://www.mt-archive.info/AMTA-2006-Owczarzak.pdf
- http://catalogue.bnf.fr/ark:/12148/cb419284389
- https://hildok.bsz-bw.de/frontdoor/index/index/docId/248
- https://zenodo.org/record/8238853
- http://www.hutchinsweb.me.uk/HasMTimproved.pdf
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://cemadoc.irstea.fr/cemoa/PUB00001963
- https://zenodo.org/record/5529712
- https://ueaeprints.uea.ac.uk/id/eprint/82501/
- http://chinelectrodoc.hypotheses.org/9841
- http://infoscience.epfl.ch/record/291528
- http://www.ticontre.org/ojs/index.php/t3/issue/view/4
- https://zenodo.org/record/8105098
- https://lirias.kuleuven.be/handle/123456789/329197
- http://gallica.bnf.fr/ark:/12148/cb327327315/date
- http://www.mt-archive.info/LREC-2004-Carl.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.97.4810
- http://cemadoc.irstea.fr/cemoa/PUB00001616
- http://hdl.handle.net/10447/39626
- https://zenodo.org/record/7474115
- http://www.nusl.cz/ntk/nusl-403442
- https://archive-ouverte.unige.ch/unige:100814
- https://figshare.com/articles/Execution_times_over_many_support_Apriori_AprioriTID_and_ITDApriori_on_T10_4D100K_dataset_/5803698
- http://www.nusl.cz/ntk/nusl-387899
- https://zenodo.org/record/5608412
- https://archive-ouverte.unige.ch/unige:43275
- http://www.aclweb.org/anthology/W/W09/W09-3502.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.91.3641
- http://hdl.handle.net/11582/3938
- http://hdl.handle.net/11346/BIBLIO@id=5635146769111164891
- http://aclweb.org/anthology/D/D13/D13-1053.pdf
- https://scholarbank.nus.edu.sg/handle/10635/229626
- http://catalogue.bnf.fr/ark:/12148/cb41914666x
- https://hal-insu.archives-ouvertes.fr/insu-02305942/document
- http://publications.jrc.ec.europa.eu/repository/handle/JRC67292
- http://dx.doi.org/10.7764/onomazein.33.15
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.2267
- https://biblio.ugent.be/publication/8661091
- https://library.oapen.org/handle/20.500.12657/46388
- https://lirias.kuleuven.be/bitstream/123456789/448810/3/Heylen_Bond_DeHertog_Vulic_Kockaert_Steurs_2014pres_TermWise_TKE.pdf
- https://zenodo.org/record/4110680
- http://hdl.handle.net/10068/405693
- http://catalogue.bnf.fr/ark:/12148/cb419283846
- http://hdl.handle.net/2066/203149
- http://www.lrec-conf.org/proceedings/lrec2004/pdf/34.pdf
- http://hdl.handle.net/10.36227/techrxiv.24486214.v1
- https://doaj.org/article/96a9c6b731374382ade9f1ecd064e32c
- http://urn.kb.se/resolve?urn=urn:nbn:se:mdh:diva-48744
- https://archive-ouverte.unige.ch/unige:152278
- http://hdl.handle.net/10045/76047
- http://wwwling.arts.kuleuven.be/qlvl/prints/Heylen_Bond_DeHertog_Vulic_Kockaert_2014abs_TermWise_CAT_tool_LREC.pdf
- https://yareta.unige.ch/archives/ee4db33f-47dc-480e-a433-5692d425690b
- http://arxiv.org/abs/2301.08745
- http://nbn-resolving.de/urn:nbn:de:bsz:93-opus-ds-97844
- https://www.zora.uzh.ch/id/eprint/98540/
- http://catalogue.bnf.fr/ark:/12148/cb41929180h
- https://mural.maynoothuniversity.ie/2205/
- http://hdl.handle.net/10068/651781
- https://www.open-access.bcu.ac.uk/16138/
- http://repository.cmu.edu/cgi/viewcontent.cgi?article%3D1310%26context%3Dcompsci
- https://zenodo.org/record/3555183
- http://www.mt-archive.info/WMT-2009-Snover.pdf
- https://zenodo.org/record/1291930
- https://arbor.bfh.ch/19713/
- http://english.um.edu.my/anuvaada/main.html
- https://hal.archives-ouvertes.fr/hal-01155041
- http://www.mt-archive.info/EAMT-2011-Gavrila.pdf
- http://hdl.handle.net/11701/37323
- https://ojs.aaai.org/index.php/AAAI/article/view/17536
- http://hdl.handle.net/2027/umn.31951d02977984b
- https://mustikka.uta.fi/corpora
- https://hal.archives-ouvertes.fr/hal-00461615/document/
- https://www.tdcommons.org/cgi/viewcontent.cgi?article=6275&amp;context=dpubs_series
- https://hal.archives-ouvertes.fr/hal-01838532
- http://www.mt-archive.info/MTS-2009-Farzindar.pdf
- http://hdl.handle.net/2072/434013
- https://bibliotekanauki.pl/articles/1943276
- https://archive-ouverte.unige.ch/unige:154232
- https://hdl.handle.net/11584/343795
- http://arc.lib.montana.edu/snow-science/objects/ISSW_P-048.pdf
- http://tubiblio.ulb.tu-darmstadt.de/51521/
- http://calenda.org/359302
- http://hdl.handle.net/1773/48053
- https://doaj.org/article/f4351b8c66d04ed4965ed696e8c9c403
- https://archive-ouverte.unige.ch/unige:146556
- http://www-i6.informatik.rwth-aachen.de/~bender/papers/eamt05.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.2846
- http://publications.idiap.ch/downloads/papers/2013/Hajlaoui_CICLING-2013_2013.pdf
- https://doaj.org/toc/2084-1965
- https://dspace.library.uu.nl/handle/1874/391212
- http://scholarbank.nus.edu.sg/handle/10635/40943
- https://zenodo.org/record/5772042
- https://www.usenix.org/legacy/events/vee06/full_papers/p175-sridhar.pdf
- https://zenodo.org/record/8016844
- https://zenodo.org/record/4110683
- https://hal.archives-ouvertes.fr/hal-01030777
- http://carnetsjapon.hypotheses.org/3621
- https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/Consistency-in-terminological-choice-Holy-Grail/99516737502346
- http://pqdtopen.proquest.com/#viewpdf?dispub=10643063
- http://etd.adm.unipi.it/theses/available/etd-04122023-101720/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.4660
- https://doaj.org/article/ccd6c74b9ff94d0984e16e91719622c6
- https://archive-ouverte.unige.ch/unige:38811
- https://library.oapen.org/bitstream/20.500.12657/46389/1/9780429264894_oaintroduction.pdf
- https://orcid.org/0000-0001-5736-5930
- http://hdl.handle.net/20.500.11850/626756
- https://zenodo.org/record/5779380
- https://research.rug.nl/en/publications/72bcb7f4-db6f-4bb2-ae89-643a612d8c73
- https://research.vu.nl/en/publications/1141c362-e9eb-46e8-b198-dca33d4fafbd
- https://zenodo.org/record/7022491
- http://hdl.handle.net/11356/1197
- https://lirias.kuleuven.be/handle/123456789/656784
- http://aclweb.org/anthology/D/D14/D14-1060.pdf