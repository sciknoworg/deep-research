# Resolving Ambiguous Translations via Language-Model Prompting

*(Compiled 2025-09-04)*

---

## 1. Executive Summary

Ambiguity remains one of the most stubborn obstacles to high-quality machine translation (MT).  Large Language Models (LLMs) give us an unprecedented control surface: **the prompt**.  By explicitly encoding disambiguation cues—as linguistic meta-information, task constraints, or interactive clarification steps—we can mitigate ambiguities that statistical and neural models have traditionally resolved only implicitly.

This report synthesises three decades of research on symbolic interlingua (Lexical-Conceptual Structure, Extended Case Structures), hybrid generation, lexically-constrained NMT, and the recent surge of LLM-based MT.  We map that body of work onto a **prompt-engineering research agenda** aimed at:

* (i) precisely *typing* the ambiguities we need to defeat;
* (ii) deciding *where* in the MT pipeline prompting adds the most value (pre-, intra- or post-generation);
* (iii) selecting language pairs and diagnostic benchmarks that expose the phenomenon; and
* (iv) distilling concrete experimental designs that combine symbolic representations, constrained decoding, and LLM reasoning.

---

## 2. Typology of Ambiguity and Their Relevance to Prompting

| Ambiguity Type | Long-standing Solutions | LLM-Prompt Opportunity |
|---------------|------------------------|------------------------|
| **Lexical / Word-sense** (polysemy: “bank”, “bat”) | WordNet-annotated corpora, sense inventory filtering, bilingual lexicon weighting | In-prompt examples that attach domain labels; interactive *few-shot sense selection*; explicit **LCS gloss** in the prompt (e.g. `CAUSE(AGT, GO(OBJ, TO(LOC)))`). |
| **Structural / Syntactic** (attachment, scope) | Statistical pre-reordering, syntax-based NMT, UNITRAN linking rules | Provide pseudo-code or bracketing in the prompt: `(NP[the man]) saw (PP[with the telescope])`; ask LLM to output both parse and translation for self-consistency. |
| **Thematic / Argument mapping** (divergent predicates) | Classic LCS mapping, θ-role templates | Prompt includes `AGENT=` / `PATIENT=` roles, letting LLM ground subject/object distinctions before generation. |
| **Coreference / Anaphora** | Winograd schemas, WinoMT | Supply discourse snippet in the prompt; request explicit antecedent resolution. |
| **Domain Terminology** (technical sense dominance) | Terminology constraints, glossary injection | Use **lexically constrained decoding**: pass target lemma list in prompt or as `must-use:` directive. |
| **Morphological Agreement** (rich-morph targets) | Post-edit rules, lemmas＋morph tags (Czech, Korean) | Prompt instructs LLM to *first* output lemmatised translation + morph features, *then* inflect. |

> Take-away: **Promptable information bands** (semantic roles, glosses, parses, terminology lists) neatly align with the symbolic layers pioneered in LCS-based MT.  Prompting can externalise what earlier systems encoded in feature structures.

---

## 3. Architectural Insertion Points for Prompting

```
          ┌───────────┐           ┌───────────┐
SRC text ─►  Baseline  ├─┬───────►│  Target    │
          │  MT (NMT) │ │        │  Text      │
          └───────────┘ │        └───────────┘
                        │
                        ▼
                Prompt-augmented
                 LLM module
```

1. **Post-edit / Disambiguation step (preferred)**  
   • Retain a strong NMT baseline for speed.  
   • Feed *translation + ambiguity cues* into LLM.  
   • Advantages: cheaper, easier evaluation—LLM only needs to fix errors.

2. **Inline guidance to decoder (constrained NMT)**  
   • Use LLM to generate lexical or structural constraints *before* decoding; pass them to an end-to-end constraints-aware NMT system (cf. English→Czech work that reduced agreement errors by 46 %).

3. **Full LLM translation from scratch**  
   • Simpler pipeline; competitive on high-resource pairs (GPT-4 ≅ Google).  
   • Still brittle on low-resource pairs (cf. AmericasNLP-2023).  
   • Heavy token cost for long documents; unclear domain-adaptation path.

> **Recommendation:** *Start with the post-edit setting*, gradually move constraints upstream once we quantify gains.

---

## 4. Candidate Language Pairs & Benchmarks

Priority is governed by: (i) rich morphology/divergence, (ii) tested diagnostic sets, (iii) data availability for automatic scores.

1. **English ↔ Czech**  
   • Agreement & free word order; existing lexically-constrained NMT literature.  
   • Benchmarks: CzEng test sets, Zboží (domain), WinoMT-CS.

2. **English ↔ Korean**  
   • Historical LCS work (UMIACS-TR-95-16) provides leveragable templates.  
   • Datasets: AIHub EK corpus; WinoMT-KO (community port).  
   • Ambiguities: honorifics, aspect markers.

3. **Spanish ↔ Chinese**  
   • Lexogen evaluation; strong structural divergence.  
   • Data: UN Parallel, WMT-20 zh-es.

4. **Low-resource Indigenous pairs (e.g., Shipibo-Konibo ↔ English)**  
   • Highlights LLM limits; AmericasNLP-2023 has curated test sets.  
   • Evaluate zero-shot vs. LLM-hinted translation.

5. **English → German (control)**  
   • High-resource baseline; synthetic disambiguation corpora exist (MuST-SHE for gender).

Evaluation metrics:

* Standard: BLEU, COMET-22, chrF++
* Ambiguity-focused: WinoMT accuracy, MT-Eval-ANA (anaphora subset), ADIST (agreement distance), targeted contrastive pairs (MuST-SHE gender tags)

---

## 5. Prompt Engineering Recipes

### 5.1 Symbolic-Infused Prompts (LCS & θ-roles)

```
You are a translation specialist. Translate the sentence, then
output (a) disambiguated LCS, (b) final target text.
SRC: "The scientist shot the star."
Expect LCS template: CAUSE(AGENT:scientist, GO(OBJ: star, EVENT:photo))
```

*Rationale*: For homographs like *shot*, forcing the model to commit to an LCS predicate (`photo` vs `fire-gun`) front-loads sense selection.

### 5.2 Parse-then-generate Self-Consistency

```
TASK: produce JSON with fields {"parse", "translation"}.
Ensure the PP attachment in parse is consistent with translation.
SRC: "I saw the man with the telescope."
```

*Rationale*: Structural ambiguity is surfaced in a machine-checkable form.  Inconsistencies can be caught automatically.

### 5.3 Constraint-driven Domain Terminology

```
Translate. Must include target terms: {"processor"=“procesador”, "cache"=“caché”}.
SRC: "The new processor has a larger cache."
```

Leverages end-to-end lexically constrained decoding research; ensures term fidelity.

### 5.4 Iterative Clarification Loop *(speculative)*

1. Prompt LLM to ask ONE clarification question if ambiguity is detected (score < τ).  
2. User/NMT pipeline answers automatically using glossaries or metadata.  
3. Model proceeds with confident translation.

Flagged as speculative because interaction cost in production is still under-explored.

---

## 6. How Classic Research Guides Modern Prompting

| Classic Insight | Modern Leverage in Prompting |
|-----------------|-----------------------------|
| **UNITRAN’s 7 divergences + linking rules** systematically map predicate-argument mismatch. | Encode linking rule outcomes (e.g., target VO word order) as *structured hints* in prompt to prevent LLM from hallucinating source order. |
| **UMIACS Korean–English interlingua pipeline** integrated aspect and morphology via semantic hierarchies. | Pass aspectual tags (`PROG`, `COMPL`) and morphological slots (`honorific`, `formality`) in prompt to drive correct Korean TL morphology. |
| **Generation-Heavy Hybrid MT’s over-generation pruned by n-gram** shows we can produce many target hypotheses then rank. | Use LLM to over-generate (`n` candidates) *and* return self-scoring logits; pick highest by COMET rescoring. |
| **Lexogen’s reusable linearizer** proved decoupling semantics from surface order works across languages. | Prompt LLM with *abstract semantic graph* and request language-specific linearization, falling back to learned linearization if abstract representation is correct. |
| **Lexically constrained NMT eliminates agreement errors** by lemma constraints. | In prompt, supply *lemma list + morph tags*; LLM does agreement-aware inflection. |

---

## 7. Experimental Design

### 7.1 Baseline Systems

* NMT: Fairseq Transformer-Big (English→Czech, WMT-23 data).  
* LLM: GPT-4o, Mistral-8x7B-Instruct (open-weight).  
* Constrained decoder: Dynamic Beam Edition of Post-2018 lexically-constrained algorithm.

### 7.2 Conditions

A. **No Prompt** (pure baseline)  
B. **Post-edit LLM** (translate-then-fix)  
C. **Constraints via LLM → Constrained NMT**  
D. **Full LLM (few-shot)**  
E. **Full LLM + Symbolic prompt (LCS, parse)**

### 7.3 Test Suites

* Generic test set (newstest-2023).  
* Diagnostic suites:  
  – 200 WinoMT‐CS sentences  
  – 150 structural ambiguity pairs (PP-attach)  
  – 100 domain-term sentences (IT hardware)  
* Manual error annotation following Multidimensional Quality Metrics (MQM) subset.

### 7.4 Success Criteria

* +2 COMET over baseline, **and**
* ≥85 % accuracy on targeted ambiguity suites, **and**
* <1.5 ×  baseline latency for post-edit scenario.

---

## 8. Evaluation & Diagnostics

1. **Automatic**: BLEU, COMET-Kiwi, chrF++.  
2. **Contrastive**: accuracy on minimal pairs (`bank₁` vs `bank₂`).  
3. **Explanation accuracy** (symbolic prompts): parse correctness, LCS template validity.  
4. **Human typological error profiling**: following Dorr’s divergence taxonomy to see which are reduced.  
5. **A/B incremental cost analysis** (token & GPU minutes per sentence).

---

## 9. Contrarian / Forward-Looking Ideas

* **Prompt-time Meta-Learning**: Fine-tune a small policy model that chooses which *type of prompt* (sense-gloss, parse, constraint) to apply per sentence, maximising expected disambiguation benefit vs cost.
* **Zero-shot LCS induction**: Ask the LLM to *invent* an LCS-like representation for unseen languages—then store & reuse as an interlingua. *(Highly speculative.)*
* **Hybrid symbolic–neural interactive editing**: Use UNITRAN to propose disambiguated interlingua; have LLM *critique* and patch it before generation.
* **Dynamic curriculum**: Feed ambiguous training pairs where baseline failed, letting LLM explanations guide synthetic data augmentation for the NMT model.

---

## 10. Roadmap & Resourcing

| Phase | Duration | Milestones |
|-------|----------|------------|
| 0. Infrastructure | 2 wks | Integrate OpenAI + local open-LLM endpoints; implement constraint emitter. |
| 1. Pilot (EN-CS) | 4 wks | Run conditions A–E on 3 k sentences; produce error clustering. |
| 2. Extension (EN-KO) | 6 wks | Import UMIACS θ-role templates; evaluate honorific & aspect errors. |
| 3. Low-Resource (Shipibo) | 4 wks | Test zero-shot vs prompt-aided LLM; gather AmericasNLP metrics. |
| 4. Productisation | 8 wks | Optimise latency, cost; choose best prompt strategy per domain. |

Team: 1 MT researcher, 1 prompt engineer, 0.5 linguistic annotator, 2 GPU nodes (A100).

---

## 11. Conclusion

Prompting is not a silver bullet, but it finally lets us *exposed the hidden layers* that symbolic MT toiled over—LCS roles, syntactic trees, semantic classes—and offer them as **high-level instructions** to an extremely competent yet error-prone language model.  Leveraging thirty years of insights on divergence, case structures and constraint-based generation gives us a principled scaffold on which to build prompt-time disambiguation.  Systematic experiments across Czech, Korean, Chinese-Spanish and low-resource pairs will tell us whether this promise translates (pun intended) into measurable gains and deployable workflows.

If successful, the result will be a **modular, explainable, and far more controllable** MT pipeline—one that combines the precision of symbolic interlingua with the fluent power of modern LLMs.


## Sources

- http://hdl.handle.net/1721.1/6016
- http://www.mt-archive.info/Coling-1986-Nomura.pdf
- http://hdl.handle.net/10068/509098
- http://www.mt-archive.info/Coling-1992-Mitamura.pdf
- http://hdl.handle.net/1903/1202
- http://www.lingviko.net/feng/forum-fzw.pdf
- http://www.mt-archive.info/CL-1994-Dorr.pdf
- http://hdl.handle.net/11346/BIBLIO@id=2165773603281921920
- http://works.bepress.com/barbara_kwasnik/3/download/
- http://liantze.penguinattack.org/files/publications/LLT-PhD-thesis.pdf
- http://hdl.handle.net/1721.1/6018
- http://www.mt-archive.info/LREC-2008-Monson.pdf
- http://hdl.handle.net/1903/696
- https://zenodo.org/record/8286649
- http://www.mt-archive.info/ACL-1990-Dorr.pdf
- https://animorepository.dlsu.edu.ph/etd_bachelors/14209
- http://hdl.handle.net/2013/ULB-DIPOT:oai:dipot.ulb.ac.be:2013/235098
- http://www.aaai.org/Papers/Symposia/Spring/1993/SS-93-02/SS93-02-007.pdf
- https://zenodo.org/record/1340038
- http://hdl.handle.net/10.1184/r1/6623216.v1
- http://ict.usc.edu/pubs/Hybrid%20Natural%20Language%20Generation%20from%20Lexical%20%20Conceptual%20Structures.pdf
- https://pub.uni-bielefeld.de/record/2901767
- http://hdl.handle.net/10138/563803
- http://hdl.handle.net/11582/325888
- http://hdl.handle.net/20.500.12678/0000004631
- http://hdl.handle.net/1721.1/6482