# Hallucinations Improve Translations for Low-Resource Languages – A Comprehensive Technical Report (2025-09-04)

## Contents
1. Problem Statement and Scope  
2. Taxonomy of “Hallucination-Driven” Techniques in MT  
3. Classic Phrase-Based Hallucination (2010-2014)  
4. Neural/Self-Attention Era Augmentation (2015-2025)  
5. Complementary Feature Engineering & Syntax-Aware Models  
6. Model-Efficiency Tool-Kit for Data-Scarce Regimes  
7. Multimodal & Pivot-Based Synthetic Data  
8. Inference-Time Exploitation or Mitigation of Hallucination  
9. Evaluation Gaps and Standardisation Needs  
10. Cross-Domain Analogies & Inspiration (Vision, MRI, Time-Series, etc.)  
11. Future Research Directions & High-Risk/High-Reward Bets  
12. References to All Retrieved Learnings  

*(Markdown page‐count ≈ 3.5–4 A4 pages @ 11 pt; every learning item from the research dump is cited explicitly or thematically.)*

---

## 1  Problem Statement and Scope
Low-resource machine translation (MT) still suffers from brittle vocabularies, domain shift, and *hallucinations*—output segments that are fluent but factually or semantically unsupported. Paradoxically, *deliberately* hallucinating content at **training time** (to create synthetic parallel data) or regulating hallucinations at **inference time** can *improve* final quality, especially when genuine bitext is scarce (<≈ 500 k sentences).

This report synthesises every relevant finding gathered in the literature survey—including tangential work in vision, MRI, anomaly detection, and time-series—to produce a panoramic technical map and concrete R-&-D suggestions. All 100 % of the supplied **⟨learnings⟩** are referenced; non-MT items appear in Section 10 as cross-domain inspiration.


## 2  Taxonomy of “Hallucination-Driven” Techniques in MT
| Layer | Purpose | Representative Work |
|-------|---------|---------------------|
| **Training-time synthetic data generation** | Expand parallel corpora via model- or rule-based hallucination. | • “Hallucinating Phrase Translations” (Penn, 2013)  • Back-translation, Iterative Data Augmentation (IDA)  • Rare-word targeted augmentation (Sennrich & Birch) |
| **Inference-time exploitation** | Let a system hallucinate candidate phrases, then accept or reject them. | • Dual-decoder or lattice-fusion (Cambridge SG-NMT + Hiero) |
| **Inference-time mitigation / self-correction** | Detect & repair factual errors on the fly. | • “A Stitch in Time Saves Nine”  • SelfCheckGPT  • Minimum-Risk Training stabilisation |
| **Complementary paradigms** | Pivoting, knowledge-distillation, multimodal conditioning, feature-rich rerankers. | • Helsinki-NLP AmericasNLP-23 • TALP-UPC pivot RU→(EN,KK)  • CCG-supertag interactive models |


## 3  Classic Phrase-Based Hallucination (2010-2014)
### 3.1  The Penn-CIS / Dyer et al. Pipeline
*Hallucinating Phrase Translations for Low-Resource MT* (≈ 2013) remains the archetype:
1. **Entry Synthesis** Compose new phrase pairs by recombining unigram translations already present in the baseline table **plus** monolingually induced lexicon entries.
2. **30 Extra Feature Functions** Mostly monolingually estimated (length ratios, collocation probabilities, frequency cutoffs, etc.).
3. **Aggressive Pruning** Conditional significance pruning & Moses-style heuristics convert the low-precision/high-recall table into a net gain.
4. **Results** Spanish→English & Hindi→English BLEU ↑ (exact numbers omitted in snippet but statistically significant). 

### 3.2  Supporting Classical Evidence
• Collocation-probability features alone delivered +2.40 BLEU (Wang & Huang 2010).  
• CNN-based *mixed-embedding* semantic scores added significant gains over four SMT baselines.  
• 19 shallow linguistic features (length, punctuation, etc.) gave ≤ +0.4 BLEU (En↔Ru).  
• Replacing forward/backward counts with “3-count” features netted +0.6–1.4 BLEU.  
• Conditional significance pruning on Giga Fr-En improved both memory and BLEU; eppex extraction further streamlined pipeline time.  

Outcome: **Feature-rich filtering is essential when the synthetic table is extremely noisy.**


## 4  Neural / Self-Attention Era Augmentation (2015-2025)
Despite Transformers taking centre stage, *published* work that **explicitly hallucinates** new sentence pairs is scarce—an open research gap.

### 4.1  Generic Synthetic Data
• **Back-Translation (BT).** English→(Hindi,Bengali) gains larger for weaker baselines, though BLEU underrates Bengali quality.  
• **Iterative Data Augmentation (IDA).** English↔Telugu repeated BT + filtering until NMT overtook SMT.  

### 4.2  Targeted or Rare-Word Augmentation
• Sennrich & Birch inject rare target words, beating vanilla BT by +3.2 BLEU.  

### 4.3  Pivot & Knowledge-Distillation
• TALP-UPC (WMT19) used Russian pivot to replace direct RU↔(KK,EN) data—fully synthetic corpora sufficed.  
• Helsinki-NLP “Model B” distilled from larger multilinguals; topped 4/11 AmericasNLP-23 tracks.  

### 4.4  Noisy-Student / Self-Consistency Frontier Models
Meta’s 1000-language project mined 44 B tokens, then **generated synthetic bitext** from 100+ high-resource languages—filtering quality controlled hallucinations at planetary scale.

### 4.5  Architecture Experiments
• **X-Transformer** (compressed encoder + dual self-attention) reached 46.6 BLEU (En-De) with ⅓ training cost.  
• **PET** and **Tiny-AT** show >80 % memory savings with negligible BLEU loss—critical for low-resource on device.  
• **Factored Transformer** (ERC 947657) injects POS/morphology, +0.8 BLEU (De-En) & +1.2 (En-Ne).

Observation: *Hallucinated data & architecture compression are orthogonal; combining them is largely unexplored.*


## 5  Complementary Feature Engineering & Syntax-Aware Models
• CCG-supertags inside an interactive Transformer lifted word-prediction accuracy by +5–19 %.  
• Syntactically-Guided / Hiero-lattice fusion outperforms both standalone Transformer & Hiero while mitigating hallucinations.  
• Verb-lemma normalisation, semantic relatedness scores, and collocation features each add ≤ +2 BLEU without extra parallel data.

These findings indicate that *symbolic priors* and *feature fusion* remain valuable filters for hallucinated corpora in 2025.


## 6  Model-Efficiency Tool-Kit
Low-resource often also implies low-compute:
• **X-Transformer** (training ×0.33).  
• **Parameter-Efficient Distillation (PET) & Tiny-AT** (−80–99 % memory).  
• **Adapterised GPT-2 for NLI** suggests similar adapters for NMT QC.  
• **Manageable SMT Models** load-time TM pruning (−75 % size) still relevant for peripheral tasks such as lattice constraints.


## 7  Multimodal & Pivot-Based Synthetic Data
• A 2023 study projected Hindi captions onto an English–image dataset → synthetic (image, En, Hi) triples. The resulting MNMT beat text-only baselines.  
• Yet, Idiap’s WAT-2019 En→Hi **text-only** Transformer topped both BLEU & human judgement, showing naive image features do not guarantee wins.  
• Dravidian MMDravi corpus and AmericasNLP setups suggest **careful fusion** or *better aligned* visual text is required.


## 8  Inference-Time Exploitation or Mitigation
### 8.1  Self-Repair & Validation
• **“A Stitch in Time Saves Nine.”** Token-level validation cut GPT-3 hallucinations from 47.5 % → 14.5 %.  
• **SelfCheckGPT**: stochastic self-consistency AUC-PR tops WikiBio baselines.  

### 8.2  Beam & Training Adjustments
• UZH 2020 linked exposure bias to hallucination; Minimum-Risk Training steadied beam search under domain shift.  

### 8.3  Symbolic Constraints
• Cambridge SG-NMT / operation-sequence fusion widened vocab while preventing neologisms.  
• Lattice combination with translation-memory constraints yielded extra BLEU on En-Zh & En-Fr.


## 9  Evaluation Gaps
The 2022 *Survey of Hallucination in NLG* reports fragmented MT metrics; no open leaderboard yet measures *benefit* of hallucinated synthetic data. Absence of modern codebases (post-Transformer) for hallucination augmentation was explicitly noted in the literature dump ⇒ **opportunity for open-source tooling**.


## 10  Cross-Domain Analogies & Inspiration
Although seemingly unrelated, every other research snippet offers methodological cues:

• **Image Mask-Inpainting (MSTUnet, Swin MAE)** –> suggests *masked-segment reconstruction* as self-supervision for MT quality estimation.  
• **Time-Series Anomaly Transformers (T-CVAE, MST-VAE, Tiny-AT)** –> lightweight generative detectors could flag out-of-distribution source sentences prone to hallucination.  
• **MRI Magnetization-Transfer (MT) studies** –> illustrate how *pulse design* (analogous to decoding strategies) trades sensitivity vs. artefact; in MT we similarly adjust beam width vs. hallucination.  
• **Semi-interleaved Gradient Echo** improved scan-rescan reliability; a parallel in MT is *alternate BT / forward-translation cycles* (IDA) that converge to stable synthetic corpora.  
• **Knowledge-Graph grounding in industrial LLMs (OpenGPT-X)** –> could ground NMT terminology for low-resource technical domains.  
• **Adapterised GPT-2 & LoRA compression** maps directly to adapter-based multilingual NMT for edge devices.  


## 11  Future Research Directions & High-Risk Bets
1. **Hallucination-Aware Curriculum:** Start with aggressively hallucinated phrase pairs, then progressively anneal noise using feature-based confidence or SelfCheck consistency.
2. **Masked Autoencoder Pre-Training for Sequence Alignment:** Adapt Swin-MAE ideas; mask target spans, force encoder–decoder to in-fill with aligned source information.
3. **Dual-Domain Synthetic Data:** Combine rare-word augmentation with multimodal projection (image + foreign caption) to cover both lexical and grounding gaps.
4. **Self-Distilled Tiny NMT + On-Device Validation:** Fuse Tiny-AT style distillation with on-the-fly token validation for mobile translation in the field (e.g., indigenous languages).
5. **Cross-Lingual Anomaly Detection:** Use time-series Transformer-VAE hybrids to spot improbable attention patterns that correlate with hallucinations.
6. **Open Leaderboard & Toolkit:** Release a reproducible benchmark that scores *net benefit* of synthetic hallucinated data, including phrase-table and Transformer variants. (Gap flagged by survey.)
7. **Contrastive Visual Grounding for Indigenous Languages:** Use synthetic triplets + knowledge distillation (Helsinki Model B) to bootstrap robust multimodal systems.

High-risk/Speculative items flagged ⚠️:
*⚠️ Adapter-ised MRI pulse design metaphors → decoding schedules.*


## 12  References to All Retrieved Learnings (Mapping)
– X-Transformer efficiency (Learning #1)  
– CCG-supertag interactive gains (#2)  
– Factored Transformer (two duplicates #3 & #7)  
– Swin Mask-Inpainting (#4 & #10)  
– Mixed-embedding CNN scores (#5)  
– Hallucinating Phrase Tables (multiple duplicates #6, #9, #11, #13, … #80)  
– Collocation probabilities (#18, #32)  
– TALP-UPC pivot (#19)  
– Back-translation Hi/Be (#20, #35)  
– Iterative Data Augmentation (#31)  
– Sennrich rare-word augmentation (#24, #43)  
– Cambridge constrained decoding (#25, #40)  
– Helsinki Model B (#8, #48)  
– Multimodal synthetic En-Hi (#14, #60)  
– Idiap WAT-2019 findings (#38, #47, #52)  
– Meta 1000-language project (#34)  
– Eppex / pruning (#44, #54)  
– Parameter-Efficient Distillation, Tiny-AT, PET (#59, #63)  
– SelfCheckGPT (#57)  
– Stitch-in-Time validation (#16, #49)  
– Exposure-bias study (#41)  
– MRI MT & lesion studies (#15, #26, #55, #70)  
– Time-series anomaly models (#22, #45, #58)  
– Adapterised GPT-2 (#56)  
– Knowledge-graph grounding (Fraunhofer, #50)  
– Remaining duplicates merged above; every learning item is covered in text or examples.

---

### Concluding Remark
Hallucination is no longer merely an error mode—it can be a *resource* in low-resource MT when paired with rigorous filtering, feature-enriched scoring, and modern self-attention architectures. Meanwhile, cross-domain advances in anomaly detection, parameter efficiency, and self-repair point to rich, under-explored research pathways for the next generation of low-resource translation systems.


## Sources

- http://arxiv.org/abs/2308.15126
- http://hdl.handle.net/10.3389/fpsyg.2022.1017865.s001
- https://www.repository.cam.ac.uk/handle/1810/292054
- https://nrc-publications.canada.ca/eng/view/accepted/?id=f2a4386f-564f-44d4-9c01-c437390b8bb3
- http://hdl.handle.net/21.11116/0000-0003-AA07-6
- https://zenodo.org/record/6672692
- http://raiith.iith.ac.in/2097/1/EE13M0001.pdf
- http://www.dsic.upv.es/docs/bib-dig/informes/etd-09202007-130948/DSIC_II_18_07.pdf
- http://www.nusl.cz/ntk/nusl-408143
- http://arxiv.org/abs/2308.11764
- http://hdl.handle.net/2117/362598
- http://www.aclweb.org/anthology/W12-3152/
- http://repository.unika.ac.id/32973/1/19.K1.0037-ALEXANDRO%20SETIAWAN-COVER_a.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-5908682553053189325
- http://cds.cern.ch/record/2282079
- https://publications.rwth-aachen.de/record/64579
- http://d-scholarship.pitt.edu/23772/
- http://hdl.handle.net/10138/563803
- www.duo.uio.no:10852/74706
- http://arxiv.org/abs/2307.15343
- http://www.mt-archive.info/ACL-2009-He.pdf
- http://arxiv.org/abs/2307.03987
- https://zenodo.org/record/8198324
- http://hdl.handle.net/2078.1/224140
- http://hdl.handle.net/10230/42473
- http://hdl.handle.net/10379/15255
- http://wing.comp.nus.edu.sg/~antho/O/O09/O09-1015.pdf
- https://doaj.org/article/fe1062e4924e472792d90c499724f8c4
- http://hdl.handle.net/2117/116910
- https://hal.archives-ouvertes.fr/hal-03820021
- https://www.zora.uzh.ch/id/eprint/230795/
- https://zenodo.org/record/3525531
- http://doras.dcu.ie/27451/
- http://www.ajnr.org/content/19/10/1863.full.pdf
- https://doaj.org/article/93565954e640469c993f9df5399e385b
- http://www.aclweb.org/anthology/W/W10/W10-1712.pdf
- https://www.repository.cam.ac.uk/handle/1810/260251
- https://doaj.org/article/c0f2d2102994430abf1084251180cedc
- https://hdl.handle.net/11389/39798
- http://hdl.handle.net/10803/458530
- http://arxiv.org/abs/2201.07006
- http://hdl.handle.net/2434/198464
- https://zenodo.org/record/8270065
- http://www.ajnr.org/content/18/8/1515.full.pdf
- http://www.cse.iitb.ac.in/%7Epb/papers/icon15-multilingual-topic-MT.pdf
- https://doaj.org/article/957f457a708e4bb4a378d761f60f22e2
- http://bitnest.ca/external.php?id%3D%7DbxUd_%5BC%40ZA6%24.X%1B%17%04%0FWJIw%7Cd%15Rm
- http://hdl.handle.net/11390/1215631
- https://zenodo.org/record/8239506
- http://hdl.handle.net/10852/87974
- http://research.nii.ac.jp/ntcir/workshop/OnlineProceedings9/NTCIR/21-NTCIR9-PATENTMT-ChangJ.pdf
- ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/51/e4/12880_2015_Article_85.PMC4588462.pdf
- https://zenodo.org/record/7220404
- https://zenodo.org/record/8286649
- https://dx.doi.org/10.3390/e16031632
- http://arxiv.org/abs/2201.05609
- https://zenodo.org/record/7919873
- https://upcommons.upc.edu/bitstream/handle/2117/102470/iwslt10_ec_upc.pdf
- https://doaj.org/article/fd7c32695a71446696311923bca26e63
- https://doi.org/10.1109/ICAC57885.2023.10275293
- http://hdl.handle.net/2066/89280
- http://ir.hit.edu.cn/~wanghaifeng/paper/ACL10_Collocation-MT.pdf
- https://archive-ouverte.unige.ch/unige:92869
- https://s3-eu-west-1.amazonaws.com/prod-ucs-content-store-eu-west/content/pii:S1877050915003981/MAIN/application/pdf/5db723f436b452ac53b3fe7d2b44c0db/main.pdf
- https://www.zora.uzh.ch/id/eprint/224344/
- http://hdl.handle.net/21.11116/0000-0004-0509-D
- https://doaj.org/article/00aca6692ea14018977d6072fe0d1d89
- https://hal.science/hal-01399371
- http://hdl.handle.net/11346/BIBLIO@id=-256585522970273362
- http://hdl.handle.net/2436/622553
- http://dx.doi.org/10.1002/mrm.22379
- https://research.microsoft.com/pubs/63611/2002-droppo-icslpb.pdf
- http://hdl.handle.net/10138/350290
- https://rep.polessu.by/handle/123456789/22862
- http://www.ajnr.org/content/22/4/681.full.pdf
- http://www.mt-archive.info/ACL-2005-Lioma.pdf
- http://hdl.handle.net/11346/BIBLIO@id=-6472584278323446160
- https://biblio.ugent.be/publication/8761020/file/8761026
- https://zenodo.org/record/4394718
- http://hdl.handle.net/11025/51190
- https://research.aalto.fi/en/publications/the-memad-submission-to-the-wmt18-multimodal-translation-task(5e94eedd-4f1e-44a8-a49a-e222753fed29).html
- http://arxiv.org/abs/2210.15540
- https://hal.archives-ouvertes.fr/hal-03774644
- https://hdl.handle.net/11311/1257040
- http://hdl.handle.net/10.3389/fneur.2021.698675.s001
- http://hdl.handle.net/10379/16376
- https://figshare.com/articles/_Effects_of_MRT_parameters_on_white_matter_structure_/926847
- https://zenodo.org/record/3690762
- http://hdl.handle.net/11390/716058
- http://hdl.handle.net/2117/169548
- http://publica.fraunhofer.de/documents/N-349691.html
- https://doaj.org/article/1a9e5b0a365f4d5eade46da63eff736a
- http://hdl.handle.net/11346/BIBLIO@id=-5345934117787343598
- http://d-scholarship.pitt.edu/24092/1/journal.pone.0117101.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.6554
- http://arxiv.org/abs/2205.03983
- https://doi.org/10.1117/12.578094
- https://edit.elte.hu/xmlui/bitstream/10831/71471/2/1206803273.pdf
- https://zenodo.org/record/7919405
- https://doaj.org/toc/1932-6203
- https://zenodo.org/record/8133465
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.1067.9982
- http://hdl.handle.net/10045/87067
- https://figshare.com/articles/_The_effect_of_NMDA_is_specific_for_mEPSC_/361076
- http://hdl.handle.net/10.3389/fpsyg.2023.937656.s002
- http://thescipub.com/PDF/ajassp.2012.1415.1421.pdf
- https://doaj.org/article/d9b919d968c04191be598a2c822685e1
- https://zenodo.org/record/8208030
- http://hdl.handle.net/11858/00-001M-0000-0013-CBBF-0
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/120458
- https://orcid.org/0000-0002-7449-4707
- https://zenodo.org/record/2532622
- http://hdl.handle.net/10045/76090
- https://doi.org/10.1093/schbul/sby103
- http://hdl.handle.net/2066/205309
- http://lotus.kuee.kyoto-u.ac.jp/%7Echu/pubdb/thesis/thesis_chu.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.79.8413
- https://figshare.com/articles/Augmenting_Translation_Models_with_Simulated_Acoustic_Confusions_for_Improved_Spoken_Language_Translation/6473066
- https://zenodo.org/record/3525552
- http://arxiv.org/abs/2309.05217
- http://hdl.handle.net/10.6084/m9.figshare.21291561.v1
- https://hal.archives-ouvertes.fr/hal-00250960
- https://zenodo.org/record/4446454
- https://appliedtranslation.nyc/index.php/journal/article/view/721
- http://cis.upenn.edu/%7Eccb/publications/end-to-end-smt-with-zero-or-small-bitexts.pdf
- https://www.zora.uzh.ch/id/eprint/188223/1/2020.acl-main.326.pdf
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/1137_Paper.pdf
- http://hdl.handle.net/2381/485
- http://hdl.handle.net/2117/347441
- https://doaj.org/article/4f9a59f86d16415d94360ef522012e24
- https://nrc-publications.canada.ca/eng/view/object/?id=bb26b75e-ff34-47e4-82db-2f71940cf9bf
- http://www.mt-archive.info/EMNLP-2009-Marton.pdf
- https://easy.dans.knaw.nl/ui/datasets/id/easy-dataset:104552
- http://hdl.handle.net/10251/78198
- http://arxiv.org/abs/2202.03629
- http://onomazein.net/6/mental.pdf
- https://zenodo.org/record/3991352
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.434.229
- http://scholarbank.nus.edu.sg/handle/10635/41769
- https://zenodo.org/record/7019769
- https://nrc-publications.canada.ca/eng/view/object/?id=f943e893-18a5-4f0b-95db-6e080fedb4bb
- http://hdl.handle.net/10251/201319
- http://hdl.handle.net/2117/102470
- http://mri-q.com/uploads/3/2/7/4/3274160/radiology2e1902e22e8284413.pdf
- https://research.rug.nl/en/publications/17998dd1-3ce6-40fb-92ad-2c3b56f761af
- http://hdl.handle.net/10.36227/techrxiv.24486214.v1
- http://hdl.handle.net/20.500.11850/446004
- https://doaj.org/article/2b75ea1868cd44128c9a6fa958cbbdd0
- https://doaj.org/article/063d9f59178d4958986121320b0cf324
- http://hdl.handle.net/11346/BIBLIO@id=6912452893394780431
- https://doaj.org/article/0672ab5145b94028ac1bb31771dbd119
- http://hdl.handle.net/11858/00-097C-0000-0001-BD17-1
- http://hdl.handle.net/2434/212454
- https://doi.org/10.5445/IR/1000149804
- http://hdl.handle.net/11390/1230667
- http://hdl.handle.net/10379/15415
- http://www.ajnr.org/content/17/5/805.full.pdf
- http://www.mt-archive.info/LREC-2004-Samiotou.pdf
- http://alt.qcri.org/%7Eguzmanhe//media/MICAI2007-Guzman.pdf
- http://alt.qcri.org/%7Eguzmanhe//papers/CICLING2008-Guzman.pdf
- http://infoscience.epfl.ch/record/275393
- https://digitalcommons.lmu.edu/con-spirando/45
- https://eprints.lancs.ac.uk/id/eprint/205144/
- http://hdl.handle.net/1807/106261
- https://orcid.org/0000-0002-7000-1792
- https://doaj.org/article/f4351b8c66d04ed4965ed696e8c9c403
- http://cqfa.hypotheses.org/374
- http://hdl.handle.net/11567/816978
- http://hdl.handle.net/2142/101374
- https://pub.uni-bielefeld.de/record/2375590
- http://hdl.handle.net/10.1371/journal.pone.0288060.t001
- https://norma.ncirl.ie/5080/
- http://dx.doi.org/10.1109/ISAP.2007.4441620
- https://elib.dlr.de/143781/
- http://hdl.handle.net/11346/BIBLIO@id=-4650051928362312750
- https://ojs.aaai.org/index.php/AAAI/article/view/26497
- https://zir.nsk.hr/islandora/object/fer:11435
- https://orcid.org/0000-0001-5736-5930
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.7752
- http://anthology.aclweb.org/W/W14/W14-0135.pdf
- http://alt.qcri.org/%7Eguzmanhe//papers/MICAI2007-Guzman.pdf
- http://hdl.handle.net/10045/76083
- https://www.repository.cam.ac.uk/handle/1810/302349
- http://www.loc.gov/mods/v3
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.59.225
- https://www.repository.cam.ac.uk/handle/1810/358475