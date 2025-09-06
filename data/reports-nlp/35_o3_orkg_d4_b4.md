# Dialect-Aware Machine Translation with Prompted Lexicon Entries as Examples

## 1. Scope and Objectives
The goal is to design, train, and evaluate a **dialect-aware MT (DA-MT) system** that reliably preserves dialectal signals (lexical, morpho-syntactic, phonological where relevant) while maintaining translation adequacy and fluency.  The defining characteristic is **lexicon-prompt conditioning**: at inference time, the user (or an upstream retrieval module) injects exemplar lexical mappings—`<dialect-term, standard-term>` or vice-versa—that the system must honor and generalize from within the local context.  This combines the strengths of

* dynamic, context-dependent lexicons (Carpuat & Wu 2008; UFAL 2024),
* light-weight parameter-efficient adaptation (adapters, CPG), and
* lexically‐constrained or retrieval-augmented decoding.

Although the conceptual framework is language-agnostic, we prioritise two concrete scenarios that stress distinct dimensions of dialectal variation and resource availability:

1. **MSA ↔ North-Levantine Arabic (NLA)**  
   *Large structural distance, diglossic continuum, low-resource parallel data but new 120 k-sentence UFAL corpus.*
2. **Standard U.S. English ↔ African-American Vernacular English (AAVE)**  
   *High lexical overlap, salient morpho-syntactic and phonological features, plentiful raw monolingual data but scarce parallel corpora.*

Both pairs benefit from prompted lexicons: Arabic for dialect-specific lemmas & morphology; AAVE for tense/aspect markers (BIN/DONE), zero copula, negative concord, orthographic cues, etc.

---
## 2. Architectural Design Space
### 2.1 Baseline Backbone
* **Pre-trained multilingual Transformer or LLM** (e.g., NLLB-200, Llama 3-70B, or GPT-4o via API).
* **Frozen core + adapters** (Houlsby or LoRA style) to keep compute footprint low and allow dialect-specific plug-ins.
* **Contextual Parameter Generation (CPG)** to synthesise *on-the-fly* adapter weights from a task embedding that encodes both **(i)** language pair and **(ii)** injected lexicon keys.  MIT 2024 M.Eng thesis shows largest gains for low-resource MT without adding base parameters.

### 2.2 Prompt & Lexicon Conditioning
1. **Retrieval layer** selects the *k* most similar sentence pairs from an indexed dialect parallel corpus (UFAL NLA 1.0, PADIC, MPCA, Twitter AAVE–SAE, etc.).
2. **Prompt template**:
   ```
   # Dialect⇄Standard lexicon examples
   - <hlkoh>, <your father>  # Levantine example
   - <done finish>, <perfective have finished>  # AAVE example
   Translate:  «SOURCE SENTENCE»
   ```
3. Use **Finite-State Constrained Decoding** («Neural MT with Terminology Constraints») so that any span labelled as a terminology constraint is *forced* into the output.  We thus avoid hallucination and misalignment.
4. Combine with **dialect tag prompting** (WMT-21 “similar-language” results: +3–5 BLEU).

### 2.3 Dynamic Vocabulary / Search
* **Gumbel-Greedy Decoding** (AAAI) to make search differentiable and permit future end-to-end fine-tuning *with* the constraint mechanism in the loop.
* **Hiero Lattice guidance** (EPSRC EP/L027623/1) for syntax-aware vocabulary pruning at test time—keeps search tractable even if we fuse retrieval candidates.
* Optionally add **Rush et al. Optimal Beam Search** for MAP-certificate decoding.

### 2.4 Multitask & Cross-modal Synergy
* **POS tagging auxiliary task** (bi-LSTM encoder) has doubled BLEU for dialect→MSA directions in prior work.
* Plug-in **ASR–MT synergy** when we work with spoken dialect input (26.6 % WER reduction earlier): a single encoder feeding both tasks with adapters.
* **Ontology-mapping agents** (DSSim/JADE) can mediate lexicon negotiation when multiple human or bot users supply divergent glossaries.

---
## 3. Data Assets and Preparation
### 3.1 Parallel Corpora
| Pair | Corpus | Size | Notes |
|------|--------|------|-------|
| MSA ↔ NLA | UFAL Parallel NLA 1.0 | 120 600 | 6 side multiparallel; movie subtitles |
| 〃 | PADIC | 6 × 6 400 | Useful for Maghrebi/NLA transfer |
| 〃 | MPCA | 2 000 | High-quality, 6 dialects + En |
| SAE ↔ AAVE | Twitter-style corp (~70 k) | Noise, mined via dialect ID |
| 〃 | “Paraphrase-like” back-translated set | 250 k synthetic | Built via style transfer + filtering |
| general | NLLB 1.7 B pool | pivot pre-training |

Data pipeline:
1. **Semi-supervised dialect classification** (linear-SVM 89.1 %, ensemble +5 %) to *filter* noisy web data and label it by dialect.
2. **Instance weighting** (VSM adaptation): propagate lexicon frequency into phrase pair weights.
3. **Morphology normalisation** (MADAMIRA, 3arrib) for Arabic to maximise overlap across dialect & MSA orthography.
4. **Back-translation & Triangular MT** (WMT-21) for synthetic parallel expansion.

### 3.2 Lexicon Resources
* **LMF-XML dialect dictionaries** (Moroccan, Syrian, Iraqi).
* **Pilot MWE lexicons** for four Latin-American Spanish dialects – architectural template for AAVE multiword markers.
* **User-provided glossaries** aggregated in a vector DB with fast k-NN retrieval.

---
## 4. Evaluation Framework
### 4.1 Automatic Metrics
* **AL-BLEU** for Arabic directions (strongest correlation with human scores in EMNLP-14 study).
* **COMET-22** (or COMET-Kiwi variant for endangered languages) for overall adequacy.
* **TermCat** to measure terminology adherence w.r.t. injected lexicon.
* **Dia-BLEU** (speculative) – BLEU variant weighting dialectal features.
* Track **brevity penalty pathologies** (Stahlberg & Byrne 2021) — specifically problematic with constraint decoding.

### 4.2 Human Judgments
* **Dialect fidelity**: crowdsource to *in-dialect* speakers; use Likert + error typology (morphology, lexeme choice, code-mixing).
* **Fluency/Adequacy**: standard MQM or Direct Assessment.
* Link to **MEANT** optimisation results to ensure semantic-frame coverage.
* Inter-rater metrics: Fleiss-κ, Kendall-τ (EnSiMaS precedent).

### 4.3 Downstream Tasks
* **ASR WER** for spoken translation pipeline.
* **Information-extraction F1** from translated text (e.g., named entities in AAVE tweets).
* **Dialect-ID perturbation**: feed MT output into a dialect classifier; we target ∆accuracy < 2 % to show dialectal cues survive translation.

---
## 5. Experimental Road-Map
1. **Baseline reproduction**: fine-tune NLLB-200 on UFAL-NLA with AL-BLEU dev tuning.
2. **Adapter insertion**: freeze backbone; insert 256-d LoRA (2.3 % params) – measure ∆BLEU/COMET.
3. **Add lexicon-prompt**: supply 5 pairs per sentence, evaluate TermCat gains.
4. **Constraint decoding** vs **soft prompt** ablation.
5. **CPG dynamic adapter**: replace static adapter with CPG; expect +1–2 BLEU on truly low-resource subsets.
6. **POS multitask**: share encoder, add POS loss, compare.
7. **Back-translation expansion**: +synthetic 250 k; check if gains survive with constraint decoder.
8. **Human evaluation sprint**: 500 sentences, 3 raters, MQM.
9. **ASR-MT joint** (optional): integrate LibriSpeech fine-tuned acoustic encoder.
10. **AAVE domain transfer**: replicate steps 1–8 with English<→AAVE; rely heavily on synthetic parallel data.

---
## 6. Risk Analysis and Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Lexicon conflict with training statistics | Hallucinated or duplicated spans | Constraint decoder with finite-state mask; penalise duplicate n-grams |
| Data sparsity (AAVE) | Over-regularisation to SAE | Use retrieval prompts + Dialect-ID filtering; iterative back-translation |
| Brevity bias under constraints | Empty or too short outputs | Minimum-length constraint (Stahlberg & Byrne), Optimal Beam Search |
| Evaluation mismatch | BLEU penalises dialect synonyms | Use AL-BLEU / TermCat / human eval |
| Sociolinguistic stance errors | Offensiveness, register mismatch | Include dialect speakers in eval loop; style detectors |

---
## 7. Answers to Design Questions
**Q1: Prioritised language-dialect pairs**  
• Primary: Modern Standard Arabic ↔ North-Levantine Arabic (and Maghrebi + Egyptian in transfer studies).  
• Secondary: Standard American English ↔ African-American Vernacular English.  
Rationale: (i) strong community demand, (ii) newly available parallel corpora, (iii) complementary typological challenges.

**Q2: Model strategy**  
Start from a **pre-trained multilingual Transformer/LLM** (NLLB-200 or Llama-3) and add **parameter-efficient adapters + CPG**; no full retraining from scratch.  Lexicon prompts and finite-state constraint decoding enforce terminology at inference.  A multi-agent wrapper (MaSMT/JADE) orchestrates retrieval, ontology mapping, and evaluation agents.

**Q3: Evaluation focus**  
Triple emphasis:  
1. **Automatic metrics** tuned for dialect and terminology (AL-BLEU, COMET, TermCat).  
2. **Human judgment of dialect fidelity** (speaker-in-the-loop MQM).  
3. **Downstream impact** on ASR WER and information-extraction accuracy.  
Benchmarks: UFAL NLA test split, PADIC dev, MPCA test, and a curated 5 k AAVE sentence set with gold SAE paraphrases.

---
## 8. Future & Contrarian Ideas
* **Differentiable Retrieval**: merge k-NN search into the gradient path (speculative) using Gumbel soft selection.
* **Swarm MT**: extend EnSiMaS idea—multiple mini-decoders vote, each seeded with a different lexicon subset, plus dynamic ontology mapping.
* **Dialect-aware speech synthesis** post-MT for full duplex conversational agents; leverage vowel-normalisation findings (Lobanov algorithm vs Bark scaling).
* **Ethical Dialect Obfuscation Toggle** allowing users to *reduce* dialect signal (privacy) or *enhance* it (solidarity).
* **Real-time adaptive prompts** using speaker embeddings from ASR to bias lexicon retrieval by sociophonetic similarity.

---
## 9. Conclusion
Recent advances—dynamic adapters (CPG), finite-state constrained decoding, dialect-tag prompting, and new multiparallel corpora—make **dialect-aware, lexicon-prompted MT** technically and economically viable.  By combining these strands within a parameter-efficient architecture and evaluating with dialect-sensitive metrics and human feedback, we can deliver translations that *both* respect community linguistic identity and meet professional adequacy standards.

> *Speculative elements flagged above; all other recommendations are grounded in published empirical results from the literature overview.*

## Sources

- https://epublications.marquette.edu/theses/1588
- http://speed.pub.ro/speed3/wp-content/uploads/2013/02/2011_ASRU_v11.pdf
- http://hdl.handle.net/10722/100250
- http://www.mt-archive.info/IWSLT-2008-Zens.pdf
- http://hdl.handle.net/10545/625192
- https://hal.science/hal-03547539
- http://hdl.handle.net/10356/45350
- https://halshs.archives-ouvertes.fr/halshs-01533094
- https://figshare.com/articles/A_Human_Judgment_Corpus_and_a_Metric_for_Arabic_MT_Evaluation/6287699
- http://aracapag.hypotheses.org/221
- http://hdl.handle.net/11858/00-001M-0000-0012-80A6-A
- http://projectile.sv.cmu.edu/research/public/talks/speechTranslation/otherPaper/eurospeech2003-cgabpcm.pdf
- http://hdl.handle.net/10.1184/r1/6373130.v1
- https://orcid.org/0000-0002-0606-0050
- https://hal.inria.fr/hal-01066989
- http://www.mt-archive.info/LREC-2008-Carpuat.pdf
- http://anthology.aclweb.org/W/W14/W14-5313.pdf
- https://scholarworks.umass.edu/aae_delv/3
- http://wing.comp.nus.edu.sg/~antho/P/P13/P13-2067.pdf
- https://dclu.langston.edu/mccabe_theses/43
- http://jls.sagepub.com/content/28/4/408.full.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.99.3415
- https://hdl.handle.net/10292/13201
- http://www.isi.edu/~avaswani/NCE-NPLM.pdf
- http://bcmi.sjtu.edu.cn/%7Epaclic29/proceedings/PACLIC29-1004.47.pdf
- http://airccj.org/CSCP/vol5/csit53311.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.2290
- http://hdl.handle.net/10.1371/journal.pone.0288060.t006
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.52.5472
- https://hal.archives-ouvertes.fr/hal-01137318/file/Zied_12353.pdf
- https://www.repository.cam.ac.uk/handle/1810/315098
- https://www.repository.cam.ac.uk/handle/1810/260251
- http://arxiv.org/abs/2205.15599
- https://doi.org/10.21437/Interspeech.2022-592
- http://hdl.handle.net/2117/89809
- https://zenodo.org/record/5533224
- https://www.ajol.info/index.php/lex/article/view/51427
- http://hdl.handle.net/11346/BIBLIO@id=-362859195066522129
- https://www.ajol.info/index.php/salas/article/view/104691
- https://ojs.aaai.org/index.php/AAAI/article/view/12016
- http://dl.lib.mrt.ac.lk/handle/123/11847
- http://recipp.ipp.pt///bitstream/10400.22/5172/1/A_AlexandraAlbuquerque_2010.pdf
- https://dare.uva.nl/personal/pure/en/publications/whats-in-a-domain(dc7e1ea5-ea60-4a33-beac-92967bf27aec).html
- http://www.thesai.org/Downloads/Volume6No11/Paper_28-Comparative_Study_Between_METEOR_and_BLEU_Methods.pdf
- http://www.lrec-conf.org/proceedings/lrec2010/pdf/777_Paper.pdf
- http://www.mt-archive.info/LREC-2008-Babych-1.pdf
- http://d-scholarship.pitt.edu/8131/1/Alorifi_thesis_7_15_08.pdf
- http://hdl.handle.net/1959.14/1187591
- http://hdl.handle.net/1959.14/1058267
- http://www.jatit.org/volumes/Vol53No1/6Vol53No1.pdf
- http://wing.comp.nus.edu.sg/~antho/W/W11/W11-3202.pdf
- https://zenodo.org/record/3383006
- http://www.mt-archive.info/CL-1996-Mani.pdf
- http://cslt.riit.tsinghua.edu.cn/~fzheng/PAPERS/2000/0010E_ICSLP_REDUCING_WJ(ZF).pdf
- http://www.murieltranslations.com/articles/terminology/term_mgmt_and_mt.pdf
- http://hdl.handle.net/1721.1/89999
- http://hdl.handle.net/2066/60926
- https://figshare.com/articles/Domain_and_Dialect_Adaptation_for_Machine_Translation_into_Egyptian_Arabic/6373139
- http://hdl.handle.net/10068/561288
- http://aclweb.org/anthology/D/D15/D15-1254.pdf
- https://hal.archives-ouvertes.fr/hal-01718858
- http://hdl.handle.net/11346/BIBLIO@id=-4855833202634207349
- http://www.nusl.cz/ntk/nusl-304321
- http://hdl.handle.net/2142/69824
- https://hal.science/hal-03435996/file/Springer_Lecture_Notes_in_Computer_Science__4_.pdf
- https://biblio.ugent.be/publication/8761020/file/8761026
- https://repository.upenn.edu/pwpl/vol18/iss2/16
- https://doaj.org/article/6be72491772a43e799c47ae8611a6e50
- https://zenodo.org/record/4394718
- http://clg.wlv.ac.uk/papers/wmt-2011-rios.pdf
- https://zenodo.org/record/3364893
- https://halshs.archives-ouvertes.fr/halshs-00645202
- https://hal.inria.fr/hal-02422914
- http://www.cs.uu.nl/groups/IS/archive/rogier/eykijis.pdf
- http://hdl.handle.net/1903/983
- http://hdl.handle.net/11582/3404
- https://nrc-publications.canada.ca/fra/voir/objet/?id=12888ba7-31e7-4056-bf81-1201d55c15d2
- http://hdl.handle.net/2437/156229
- http://cds.cern.ch/record/1503761
- https://hal.inria.fr/hal-03272258/document
- http://www.maia.ub.edu/%7Emaite/papers/autonomic-orgs-2008-camera-ready.pdf
- https://doaj.org/article/1a9e5b0a365f4d5eade46da63eff736a
- http://hdl.handle.net/1959.14/143202
- https://hal.archives-ouvertes.fr/hal-01581038
- http://www.hathitrust.org/access_use#pd-us-google.
- http://arxiv.org/abs/2205.03983
- https://animorepository.dlsu.edu.ph/faculty_research/2552
- http://dx.doi.org/10.1109/ACCESS.2021.3132488
- http://folk.uio.no/plison/pdfs/projects/fripro2013.pdf
- https://hdl.handle.net/1721.1/145034
- http://dl.lib.mrt.ac.lk/handle/123/11832
- http://www.mt-archive.info/NAACL-HLT-2009-Hasan.pdf
- https://doaj.org/article/a90d69b049df4cb3b706d2bc2d8b3975
- http://hdl.handle.net/11346/BIBLIO@id=-4751090298931679179
- http://www-i6.informatik.rwth-aachen.de/PostScript/InterneArbeiten/Khadivi_AutomaticTextDictation_in_CAT_EUROSPEECH2005.pdf
- https://hal.archives-ouvertes.fr/hal-01557405
- https://nrc-publications.canada.ca/eng/view/accepted/?id=d1f017c8-aab2-4739-88a6-53999a36d713
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.7456
- http://hdl.handle.net/10251/46629
- http://dx.doi.org/10.1109/EEE.2005.116
- https://doaj.org/article/c1068ee5db2c4b84acb6382829dcc5c5
- http://www.irit.fr/dynamo/uploads/publis_dynamo/sellami_keod_09.pdf
- http://www.lrec-conf.org/proceedings/lrec2008/pdf/217_paper.pdf
- http://dx.doi.org/10.1145/2518130
- http://drum.lib.umd.edu/bitstream/handle/1903/2148/umi-umd-2127.pdf%3Bjsessionid%3D5E1F8BFB60378BC5A9F327548E8180B3?sequence%3D1
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://doi:10.4018/978-1-7998-3479-3.ch060
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/523_Paper.pdf
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/120458
- http://hdl.handle.net/10292/11398
- http://dx.doi.org/10.17613/p0sp-yj29
- http://scholarbank.nus.edu.sg/handle/10635/77949
- https://pub.uni-bielefeld.de/record/1857752
- https://dke.maastrichtuniversity.nl/nico.roos/wp-content/uploads/2015/07/WRV02AAMAS.pdf
- http://dl.lib.mrt.ac.lk/handle/123/13112
- http://hdl.handle.net/10125/5045
- https://journals.linguisticsociety.org/proceedings/index.php/BLS/article/view/1237
- http://www.mt-archive.info/ACL-SMT-2008-Agarwal.pdf
- http://hdl.handle.net/10356/78408
- http://hdl.handle.net/11582/330742
- http://bcmi.sjtu.edu.cn/%7Epaclic29/proceedings/PACLIC29-2041.221.pdf
- https://lirias.kuleuven.be/bitstream/123456789/523782/1//4004_final.pdf
- http://hdl.handle.net/11582/3938
- http://cocoon.huma-num.fr/exist/crdo/meta/crdo-NRU_M31_NUM_CL
- https://dx.doi.org/10.1016/j.apacoust.2022.108976
- http://summit.sfu.ca/item/9759
- http://dl.lib.uom.lk/handle/123/16916
- https://openresearch-repository.anu.edu.au/bitstream/1885/282436/3/billington21_interspeech.pdf.jpg
- http://journals.cambridge.org/abstract_S0025100309990247
- http://alt.qcri.org/%7Eguzmanhe//papers/IWSLT2013-Sajjad.pdf
- https://epublications.marquette.edu/spaud_fac/61
- http://www.sociolinguistics.uottawa.ca/shanapoplack/francais/pubs/articles/PoplackVanHerkHarvie2001.pdf
- http://hdl.handle.net/10068/336350
- http://commons.lib.niu.edu/handle/10843/14858
- http://www.nusl.cz/ntk/nusl-508955
- https://doaj.org/article/6f65df3c5ab641dfa60bd2cdb551bd22
- https://repository.upenn.edu/pwpl/vol20/iss2/16
- http://opar.unior.it/337/1/Mixed_up_with_Machine_Translation_FINAL_preview.pdf
- http://hdl.handle.net/10523/984
- http://arabic.emi.ac.ma/alelm/?q=Resources
- http://alt.qcri.org/%7Eguzmanhe//papers/NIST2015-Sajjad.pdf
- http://hdl.handle.net/2027.42/83314
- http://hdl.handle.net/2027.42/83344
- https://zenodo.org/record/3726804
- https://hal.archives-ouvertes.fr/hal-03294912
- http://www.ida.liu.se/~sarst/SLTC_2010_Bremin_et_al.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.70.3500
- http://cs.uef.fi/sipu/pub/IS140382.pdf
- https://emitter.pens.ac.id/index.php/emitter/article/view/812
- http://hdl.handle.net/10251/49157
- http://repository.upenn.edu/cgi/viewcontent.cgi?article%3D1821%26context%3Dpwpl
- https://doi.org/10.21437/Interspeech.2021-2167.
- https://figshare.com/articles/DNN_phoneme_classification_frame_accuracy_and_language_recognition_performance_average_EER_of_all_language_clusters_/5299342
- http://hdl.handle.net/10068/447393
- http://purl.umn.edu/139944
- http://hdl.handle.net/10092/13213
- https://doi.org/10.1215/00031283-80-4-366
- http://doras.dcu.ie/24493/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.47.4876
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.6.4344
- https://doaj.org/article/efab47705211400f878eb8e3370ce9c1
- http://hdl.handle.net/2117/104733
- http://www.mt-archive.info/MTMarathon-2010-Heafield.pdf
- https://www.neliti.com/publications/361816/perbandingan-bahasa-antara-modern-standard-arabic-dengan-aksen-lebanon
- https://etd.ohiolink.edu/%21etd.send_file?accession%3Dohiou1020776535%26disposition%3Dinline
- https://ojs.aaai.org/index.php/AAAI/article/view/17485
- http://bcmi.sjtu.edu.cn/%7Epaclic29/proceedings/PACLIC29-2032.40.pdf
- https://zenodo.org/record/55708
- http://anthology.aclweb.org/W/W14/W14-3627.pdf
- https://research-portal.st-andrews.ac.uk/en/researchoutput/automatic-classification-of-human-translation-and-machine-translation(777591c5-314d-4ecb-be42-2d2ae1d834bc).html
- www.springer.com.
- http://journals.library.mun.ca/ojs/index.php/LA/article/download/1394/1026/
- https://hal.archives-ouvertes.fr/hal-00819590
- https://hal.archives-ouvertes.fr/hal-01505049
- https://doaj.org/toc/1972-1293
- http://www.lrec-conf.org/proceedings/lrec2008/pdf/403_paper.pdf
- http://www.mt-archive.info/LREC-2008-Itagaki.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-4101501886257704446
- https://doaj.org/article/7006cc74002e41b2bc84f1fa337e1052
- http://hdl.handle.net/10379/14891
- https://hal.archives-ouvertes.fr/hal-03798550
- http://doras.dcu.ie/23860/
- http://www.ajol.info/index.php/lex/article/download/51427/40081/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.77.450
- http://dl.lib.mrt.ac.lk/handle/123/13110
- http://aclweb.org/anthology/D/D13/D13-1022.pdf
- https://www.zora.uzh.ch/id/eprint/150769/1/Volk__Parallel_Corpora_Term_Extraction_MT_v01.pdf
- http://hdl.handle.net/10.1371/journal.pone.0288060.t001
- https://zenodo.org/record/8320370
- http://www.lrec-conf.org/proceedings/lrec2012/pdf/461_Paper.pdf
- https://hdl.handle.net/10292/11398
- http://hdl.handle.net/10.1184/r1/6287699.v1
- http://learningtotalk.org/sites/learningtotalk.org/files/ChungEtAl2010JKSSS.pdf
- http://emnlp2014.org/papers/pdf/EMNLP2014026.pdf
- https://digitalcommons.hope.edu/curcp_12/171
- https://digitalcollections.sit.edu/sandanona/spring2009/wedmay27/3
- http://mt-archive.info/MTS-2007-Moore.pdf
- http://dl.lib.mrt.ac.lk/handle/123/8409
- www.myjurnal.my/filebank/published_article/6471621.pdf
- https://zenodo.org/record/2529727
- https://hal.archives-ouvertes.fr/hal-03263105
- http://etd.adm.unipi.it/theses/available/etd-04122023-101720/
- https://orcid.org/0000-0001-5736-5930
- https://www.repository.cam.ac.uk/handle/1810/324365
- http://handle.unsw.edu.au/1959.4/44045
- http://arxiv.org/abs/2202.07856
- http://dl.lib.mrt.ac.lk/handle/123/11845
- http://people.ischool.berkeley.edu/~nakov/selected_papers_list/IWSLT13_SMT_EN2AR.pdf
- http://hdl.handle.net/10068/416624
- http://repository.essex.ac.uk/11692/
- http://mt-archive.info/LREC-2002-Kubler.pdf