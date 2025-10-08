# Dialect-Aware Machine Translation with Prompted Lexicon Entries as Few-Shot Examples

**Status**                        2025-09-04  
**Author**                        LLM Research Assistant  
**Intended audience**    Experienced MT/NLP researchers & engineers  

---

## 1  Problem Statement and Scope

We want an MT system that, given a *standard-language* source sentence, produces a *dialectal* target whose lexis, morphology and idiomaticity faithfully reflect a chosen dialect.  
Distinct from typical MT, where source and target differ by language, here they differ primarily by **register and variety**.  
Our focus is Arabic because of:

* The deep diglossia between **Modern Standard Arabic (MSA)** and numerous regional dialects.
* Availability of three-way or learner dictionaries (Tharwa 2014; LDC/GU projects) that already encode cross-dialect mappings.

We keep the design *pair-agnostic* so it can later be transferred (e.g., Standard French→Québécois), but the initial concrete instantiation is:

```
Direction 1   MSA  →  Egyptian Arabic (EGY)
Direction 2   MSA  →  Moroccan Arabic (ARA-MA)     (optional phase-2)
```

### Why “prompted lexicon entries”?
Large decoder-only LMs already contain sizeable implicit knowledge of dialects.  Few-shot prompts that show **glossed, dialect-specific lexical correspondences** can steer generation without permanent parameter updates.  This avoids costly fine-tuning for every micro-dialect and supports last-minute terminology injection.


---

## 2  Landscape Review (Key Learnings Incorporated)

| # | Learning | Relevance to our plan |
|---|----------|----------------------|
|1 | **Tharwa (2014)**: 73 k 3-way MSA↔EGY↔EN lexicon | Ready-made seed for prompted examples & automatic constraint extraction. |
|2 | **LDC/GU learner dictionaries (1960s → LMF-XML)** for Moroccan, Syrian, Iraqi | Gives us dual orthography + IPA for future pronunciation-aware prompting. |
|3 | **BLEU/NIST correlate with human ratings on small fixed sets** (Coughlin 2003) | Confirms that for local experiments we can rely on automatic metrics *once* we also fix data size & domain. |
|4 | **Sentence-level dialect ID improves MT system selection** (+1 BLEU) | Motivate an *adaptive* inference pipeline: id-then-route or id-then-prompt. |
|5 | **Bootstrapping dialect tools from MSA** (BAMA-derived analyzers, Tunisian deverbal nouns) | We can reuse MSA morphological taggers to pre-annotate, then correct. |
|6 | **No documented Standard→Dialect MT with lexicon-guided prompting** | Opportunity for novelty; evaluation design must be bespoke. |
|7 | **Metric–quality decoupling** (BLEU misses dialect fidelity) | We will add COMET-DA and targeted probe sets (morphology, idiom, politeness). |
|8 | **Transformer chat MT with selective context + pseudo in-domain fine-tuning beats SOTA** | We can combine dynamic prompts (context) with lightweight LoRA fine-tuning. |
|9 | **Lexically constrained MT removes 46 % agreement errors** | Lexicon entries can be injected as *soft constraints* or *in-context* examples. |
|10| **Code-switching MT shows automatic metrics miss CSW errors** | Our dialect output may mix MSA/dialect; evaluation must capture CSW phenomena. |
|11| **Arabic→French SMT improvements via segmentation & LM** | Segmentation still matters—especially for Arabic, we must normalize MSA input. |
|12| **Pair-independent architecture (TAMTAM)** approaches commercial systems | We will keep the architecture modular: dialect layer sits atop general MT. |

---

## 3  System Architecture

```
                                ┌────────────────────────────┐
           Tharwa, LDC Lexicon  │  Dialect Lexicon Server    │
  ─────────>  (LMF-XML → JSON)  └─────────┬──────────────────┘
                                           │REST/GRPC
                                   plus    │
                                   Few-shot│Prompt builder
                                           ▼
          ┌─────────┐   prompt   ┌────────────────────────────┐
 MSA src →│Normalizer├──────────►│  Large Decoder-only LM     │
          └─────────┘            │  (e.g., GPT-4o-128K, φ-3)  │
                                 └─────────┬──────────────┬──┘
                                           │              │
                               Dialect ID   │   Soft constraints
                                           ▼              │
                                  Routing / Post-edit     │
                                           ▼              │
                                     Final Dialect Output ◄─oracle-level edit if cons. violated
```

### 3.1  Lexicon server
* Converts LMF-XML → flat JSON"); serves entries as `{"msa":"سيارة","egy":"عربية","pos":"N","root":"س ي ر"}`.  
* Supports **fuzzy lookup** to suggest near-surface MSA forms.  
* Emits *few-shot prompt lines*:
  "`MSA: سيارة  →  EGY: عربية`"

### 3.2  Prompt builder
Algorithm per source segment:
1. Run MSA segment through MADAMIRA to lemmatize & segment.  
2. Query lexicon; select **K≤10** high-salience pairs (rank by tf-idf in segment).  
3. Compose system prompt:

```
You are an expert translator. Given MSA, write the equivalent **Egyptian Arabic** sentence.
Use the following examples as guidance and preserve dialectal flavor.
Examples:
MSA: سيارة  →  EGY: عربية
MSA: ماذا تفعل؟ → EGY: بتعمل إيه؟
… K examples …
Sentence:
<msa_src>
Answer:
```

4. Optionally add *soft constraints* by repeating the expected Egyptian lemma inside square brackets to bias the LM.

### 3.3  Model & Training Strategy

Stage 0 (Off-the-shelf): Use GPT-4o-128K (or open φ-3) with **no param update**; rely solely on prompts.  
Stage 1 (Fine-tune): LoRA or QLoRA on 5–50 k parallel MSA→EGY lines (bootstrapped via back-translation + manual review).  
Stage 2 (Continual): For each new domain, run *pseudo in-domain fine-tuning* (NCIRL 2021 style) with small adapters.

**Speculation flag 🟡:** With good prompt design alone we may already reach >35 BLEU on informal test set; Stage 1 could add +2–3 BLEU and large gains in idiomaticity by locking in word order patterns.

### 3.4  Dialect Identification & Routing (optional)
Before translation, detect whether the input itself contains dialect.  If yes, either:
* Skip translation (identity), or
* Round-trip: dialect→MSA normalization → Lexicon-prompt → dialect.

This mirrors the +1 BLEU routing gain reported in ACL 2014.


---

## 4  Data Pipeline

1. **Raw corpora**  
   • OpenSubtitles (EGY portions)  
   • Egyptian Arabic TED (converted)  
   • Twitter 2013-18 (geofenced Egypt)  
   • 1960s Egyptian learner corpus (aligned glosses)  
2. **Cleaning & alignment**  
   • UTD-Mingea aligner with noisy channel (projects treat MSA→EGY as monotone ≈80 %).  
   • Remove sentences with high intra-segment code-switching to avoid confusing the base model.
3. **Annotation**  
   • POS, diacritization via ADAM (BAMA variant)  
   • Dialect tag (EGY)  
4. **Train / dev / test split** with *document-level* hashing to avoid leakage.  
5. **Test suites**: see §7.


---

## 5  Lexicon Construction & Expansion

| Step | Details |
|------|---------|
|Seed  | Tharwa 2014 (73 k items). POS, gender, number, root, pattern. |
|Merge | LDC Moroccan (24 k), Syrian (18 k), Iraqi (20 k) by lemma alignment. |
|Normalize | Map to *CODA* orthography for each dialect + Arabizi transliteration table. |
|Score | PMI between lexeme and dialect corpora; filter top 200 k for prompting. |
|Derivational expansion | Use pattern templates to auto-generate inflected forms (SAMA patterns). |
|Quality review | Crowdsource triage on Toloka; 3-way majority voting. |

Run time: one senior linguist-month + 300 crowd hours.


---

## 6  Prompt Engineering Experiments

| Variant | Description | Hypothesis |
|---------|-------------|-----------|
|`EX-k` | k explicit *example lines* (K=0…20) | More examples → diminishing returns after 8. |
|`SECTIONED` | Add sub-headers (Nouns, Verbs, Idioms) | Improves retrieval of multi-word idioms. |
|`CONSTR` | Lexical constraints `[عربية]` inline | Raises term accuracy but may reduce fluency. |
|`CHAIN` | Chain-of-thought: first write gloss table, then final sentence | Helps alignment of longer sentences. |
|`MIXED` | Mix MSA→EGY + EGY→MSA examples | Test interference vs. generalization. |

Metrics collected: COMET-DA, Dialect-BLEU, Idiom-Hit@k (custom), runtime.


---

## 7  Evaluation Design

### 7.1  Automatic metrics
* **BLEU-detok** (for comparability).  
* **COMET-DA-22** – finetuned on dialect human judgments.  
* **TER** for post-edit distance.  
* **LexAcc**: percentage of gold dialect lexical items present (weighted by importance).  
* **CSW-F1**: code-switch detection precision/recall (as in Vietnamese study).

### 7.2  Phenomenon-specific test suites
1. **Idiomaticity**: 500 MSA idioms with one canonical EGY equivalent; measure hit rate.  
2. **Morpho-agreement**: 1 k synthetic sentences covering gender/number; evaluate via automatic morphological analyzer.  
3. **Register & politeness**: 300 minimal pairs; human rank order.  
4. **Out-of-domain**: Newswire MSA, to check robustness.

### 7.3  Human evaluation
* 3 bilingual annotators, 5-point Likert on *fluency*, *dialect fidelity*, *semantic adequacy*.  
* Use TrueSkill to combine ranks; 1000-sentence sample gives ±0.1 accuracy at 95 % CI.

**Note:** Coughlin 2003 showed one reference might suffice, but we include two to catch variability.


---

## 8  Experimental Roadmap & Expected Results (speculative)

| Phase | Core experiment | Expectation | Risk |
|-------|-----------------|-------------|------|
|P0 | Off-the-shelf GPT-4o + 0-shot | Baseline BLEU≈27, COMET-DA≈0.62 | Dialect drift toward MSA. |
|P1 | +5 example lines | +5 BLEU, +0.06 COMET; LexAcc↑20 % | Prompt length hits 8 k tokens. |
|P2 | +lexical constraints | LexAcc↑10 %; idiom hit↑15 % | Fluency –0.5 Likert. |
|P3 | LoRA fine-tune (50 k pairs) | +2 BLEU, COMET +0.03, fluency recovers | Catastrophic forgetting of rare patterns. |
|P4 | Dialect-ID routing | +0.7 BLEU on mixed input | Mis-ID leads to jarring outputs. |

**Overall goal:** reach **BLEU ≥35, COMET-DA ≥0.72, human adequacy≥4.2/5** on internal blind set.


---

## 9  Contrarian & Emerging Ideas

* **Decoder fusion (Shallow fusion)**: Fuse a small Egyptian LM (trained on 50 M tokens) during decoding of the base LLM, analogous to domain LM fusion in speech.  
  *Could yield better word order with marginal compute.*
* **Multimodal prompts**: Provide the LM with IPA or audio snippets of dialectal pronunciation to bias toward colloquial orthography.
* **Retrieval-augmented generation**: At inference, retrieve parallel MSA→EGY sentence pairs from a vector DB (FAISS) and inject as demonstrations.  
  NCIRL 2021 shows retrieval + fine-tune > fine-tune alone.
* **Edit-based MT (Levenshtein Transformer)**: Predict *edit ops* that transform MSA into EGY; might require less data and guarantee strong lexical copying.
* **Graph-based lexicon propagation**: Use graph neural networks over the LMF lexicon to predict likely EGY equivalents for unseen MSA lemmas; feed predictions as constraints.

---

## 10  Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
|Prompt overflow with long source | Truncation of examples → quality loss | Dynamic K selection, compress examples via tags. |
|Dialect intra-speaker variation (e.g., Cairene vs. Upper Egyptian) | Inconsistent output | Add dialect-subtag; fine-tune separate adapters. |
|Resource license incompatibility (Tharwa vs. LDC) | Legal blockage | Use OpenTharwa subset; sign LDC research license. |
|Crowd annotator bias toward MSA | Inflated scores | Add dialect proficiency screening + gold checks. |

---

## 11  Engineering Effort Estimate

| Work package | Lead | Weeks |
|--------------|------|-------|
|Lexicon ETL + API | NLP eng | 2 |
|Prompt builder + constraint injector | ML eng | 2 |
|Data alignment & cleaning | RA | 3 |
|Model fine-tuning infra (LoRA) | ML eng | 1 |
|Evaluation harness (COMET-DA, probes) | Researcher | 2 |
|Human eval UI + annotators | PM | 1 |
|Analysis + write-up | Researcher | 1 |
|**Total** | | **~12 person-weeks** |

Compute: single 8×A100 node for LoRA (<24 h), inference on 1×A100.

---

## 12  Future Extensions

1. **Bidirectional Standard↔Dialect**: Add EGY→MSA to serve GEC/correction tasks.  
2. **Other dialects**: Moroccan, Levantine, Gulf via same pipeline; just swap lexicon.  
3. **Cross-dialect bridging**: MSA→EGY then EGY→MSA→Maghrebi to produce synthetic corpora for low-resource Maghrebi.  
4. **Standard French→Québécois**: Demonstrate language independence; needs new lexicon (BDLP + fr-CA phrase table).  
5. **Interactive CAT tool**: Expose lexicon constraints via UI; translator can pin terms in real time.

---

## 13  Conclusion

The proposed pipeline leverages *prompted lexicon entries* as few-shot demonstrations to steer powerful decoder-only LMs toward dialect-faithful output, filling a clear gap in Standard→Dialect MT research.  Existing resources—Tharwa, LDC learner dictionaries, MSA-derived analyzers—provide an unusually rich starting point.  By coupling adaptive prompt engineering with lightweight parameter-efficient tuning, and evaluating using dialect-specific metrics beyond BLEU, we expect to achieve significant improvements in lexical fidelity and idiomaticity over baseline LLM translation.

If successful, the methodology generalizes to any standard/dialect pair, opens new avenues for *register-controlled generation* and establishes a reproducible benchmark others can build upon.

---

*All speculative numbers are flagged; actual gains depend on prompt/model choice and data noise.*


## Sources

- http://hdl.handle.net/10125/44864
- http://hdl.handle.net/11582/266819
- http://www.mt-archive.info/MTS-2001-White-2.pdf
- https://hal.inria.fr/hal-01066989
- http://www.lrec-conf.org/proceedings/lrec2004/pdf/611.pdf
- https://doaj.org/toc/1972-1293
- http://www-i6.informatik.rwth-aachen.de/PostScript/InterneArbeiten/Hasan+Isbihani+Ney_CreatingALarge-ScaleArabicToFrenchStatisticalMachineTranslationSystem_LREC_2006.pdf
- https://hal.archives-ouvertes.fr/hal-00479949
- https://hal.archives-ouvertes.fr/hal-01297415
- http://www.eamt.org/events/summitVIII/papers/pinkham.pdf
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.46.7485
- https://hal.science/hal-02869839
- http://www.lrec-conf.org/proceedings/lrec2014/pdf/1161_Paper.pdf
- https://zenodo.org/record/8115780
- http://orcid.org/0000-0002-5503-0341
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.81.8967
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.71.3539
- http://liantze.penguinattack.org/files/publications/LLT-PhD-thesis.pdf
- https://orcid.org/0000-0001-5736-5930
- https://pub.uni-bielefeld.de/record/1897888
- http://www.mt-archive.info/IWSLT-2008-Shen.pdf
- http://www.lrec-conf.org/proceedings/lrec2012/pdf/461_Paper.pdf
- http://www.theses.fr/2012BESA1011/document
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.5708
- http://anthology.aclweb.org/W/W14/W14-5311.pdf
- http://www.mt-archive.info/MTS-2001-White-1.pdf
- http://aclweb.org/anthology/P/P14/P14-2125.pdf
- https://hdl.handle.net/10356/165027
- http://www.mt-archive.info/LREC-2008-Hasan.pdf
- https://hal.archives-ouvertes.fr/hal-00959228
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.99.3040
- https://zenodo.org/record/6760024
- http://etd.adm.unipi.it/theses/available/etd-04122023-101720/
- http://www.cslu.ogi.edu/%7Egormanky/courses/CS662/PDFs/lecture_notes/2015-03-03-handout.pdf
- https://norma.ncirl.ie/5081/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.4660
- http://www.mt-archive.info/MTS-2003-Coughlin.pdf
- http://hdl.handle.net/11346/BIBLIO@id=2165773603281921920
- https://aclanthology.org/2023.findings-acl.893.pdf
- http://www.mt-archive.info/TMI-1995-Levin.pdf