# Guiding Multilingual Storytelling via Question-Answering

**Date:** 4 Sep 2025  
**Author:** Large-Scale Research Synthesis  
**Scope:** This report consolidates state-of-the-art research and adjacent findings relevant to using Question-Answering (QA) mechanisms to guide the generation, evaluation and interactive steering of *multilingual* narrative content. It covers methodology, datasets, system architecture, evaluation, gaps, and concrete design recommendations. All learnings provided by prior research excerpts are fully integrated.

---

## 1  Problem Setting

Story generation systems increasingly aim to (i) work across many languages and cultures, (ii) respect audience-specific discourse conventions, and (iii) support real-time or offline *guidance* through Question-Answering. “Guidance” denotes any pipeline in which answers to natural-language questions influence narrative creation or revision – e.g. ensuring factual consistency, enabling audience-driven branching, or providing diagnostics during offline story planning.

The user’s specific application parameters (education vs. entertainment, real-time vs. offline, language scope, etc.) are still open, so this report assumes a *generalised* setting and highlights where decisions affect architecture or evaluation.

---

## 2  Research Landscape

### 2.1  Multilingual QA Benchmarks & Transfer Techniques

| Year | Contribution | Relevance |
|------|--------------|-----------|
| **CLEF-2004 Multilingual QA track** | 50+ tasks, 9 source × 7 target languages, *single-exact-answer* metric. Surfaced scoring ambiguities for “definition” and “How” questions. | Reveals early pitfalls in evaluating cross-language QA: fine-grained answer types & culture-specific granularity matter. |
| **AAAI 2021 “Multilingual Transfer Learning for QA”** | Enlarges English training 14× with MT-generated silver data + language-adversarial objectives → SOTA zero-shot results on MLQA, TyDiQA. | Demonstrates scalable cross-lingual QA without per-language annotation. |
| **Icelandic DensePhrases pipeline (arXiv:2207.01918)** | MT-bootstrap → bilingual retriever/reader → monolingual transfer, no target-language labels. | Blueprint for rapidly adding *low-resource* languages to storytelling QA. |
| **DSTC-11 Track 4 (2023)** | Dialogue evaluation metrics stress-tested beyond English; most fail. | QA-guided dialogue storytelling must include robust multilingual evaluation metrics. |

### 2.2  Narrative-Centric Corpora & Instruments

• **University of Manchester “Visual Storytelling of Language Documentation” (USP 2020-21)**: 14 Zoom retellings of a baby-fish storyboard in 9 languages with aligned imagery + English translations. Valuable for grounding multimodal QA that bridges image panels and multilingual narration.  
• **Multilingual Assessment Instrument for Narratives (MAIN)**: Picture-based, >25 languages, three elicitation modes (Model, Retell, Tell), normative data on 550 children. Provides *macro-structure* (story grammar) and *micro-structure* (lexico-syntax) metrics that can double as reference targets when QA checks narrative completeness or cohesion.  
• **LF-SQuAD & LF-QUOREF** (2023): Long-form narrative QA benchmarks used to augment GPT-2/3 with dynamic knowledge graphs. Show viability of QA for *long-context* story comprehension.

### 2.3  Narrative Generation Frameworks Decoupling Content & Realisation

| Framework | Core Idea | Findings |
|-----------|----------|----------|
| “Where Story and Media Meet” (2013) | Separate **fabula** (event logic) from **medium logic** (linguistic realisation). | Enables dynamic PoV, emotional retellings; changing surface form shifts cross-cultural character perception. |
| **Expressive-Story Translator + Fabula Tales** (2018) | Rule-based surface realiser over abstract story graphs. | Reader studies confirm stylistic variation materially changes engagement. |
| **ITC-irst documentary engine** (2006) + **AGILE CAD/CAM manual generator** (2000) | Single language-independent representation; 70-80 % code reused across languages; referring expressions + sentence order handcrafted per locale. | Indicates that *story logic* can be language-agnostic while *realisation* must remain language- & culture-sensitive. |

### 2.4  Service-Oriented & Ontology-Driven QA

• **QALL-ME Framework** (repeated twice in literature): SOA architecture coupling multilingual question interpretation, spatiotemporal context, ontology mediation. Demo for cinema/tourism events shows plug-and-play domain portability, relevant for WIP prototypes requiring modular storyworld knowledge bases.  
• **Dynamic Document-Based Knowledge Graphs** (AAAI 2023): Out-of-context narrative questions routed through rolling knowledge graphs to expand LLM context window, producing higher accuracy on long stories.

### 2.5  Human Evaluation Insights

• English educational story generator (2019) scored 2.72/4 (grammar 2.52, dialogue 2.80) across 9 stories. Even *monolingual* quality lags: cross-cultural dialogue registers are harder.  
• CLEF & DSTC findings show existing automatic metrics misalign with human judgments, especially for multilingual dialogue/narrative QA.

---

## 3  Key Challenges for Multilingual QA-Guided Storytelling

1. **Cross-Language Semantics & Pragmalinguistics**  
   − Literal equivalence rarely preserves cultural implicature, e.g., Japanese indirectness vs. German directness in answering “why” questions.  
   − QA guidance must thus map to *culture-specific narrative acts* (e.g., moral, epilogue, formulaic openings).
2. **Long-Form Context Windows**  
   − Modern LLMs truncate contexts; dynamic knowledge graphs or retrieval-augmented generation (RAG) are mandatory for novels, transmedia scripts.
3. **Evaluation Granularity**  
   − Need metrics beyond exact answer span: *narrative entailment*, *thematic coverage*, *affective coherence*.
4. **Data Scarcity in Low-Resource Languages**  
   − MAIN covers 25+ languages, but many are still missing; automatic MT-bootstrapping similar to the Icelandic pipeline can fill gaps.
5. **Multimodality**  
   − Storyboards, comics, or games require QA that references both images and text (cf. Manchester baby-fish dataset). Alignment is non-trivial.
6. **Real-Time vs. Offline**  
   − Interactive co-creation imposes latency constraints; offline planning allows heavier reasoning (graph search, global coherence scoring).

---

## 4  Reference Architecture (Generalised)

```
+------------------+      +-------------------+     +------------------+
|  User / Audience | <--> | Multilingual QA    | <-> | Story State &     |
|  (questions)     |      | Layer (Retriever, |     | Knowledge Graph  |
+------------------+      | Reader, Arbiter)  |     +------------------+
                                  ^                        |
                                  |                        v
                           +--------------+         +---------------+
                           | Narrative    | <-----> | Language-     |
                           | Planner      |         | specific NLG  |
                           +--------------+         +---------------+
                                      ^
                                      |
                                +-----------+
                                | Assets    |  (MAIN pictures, baby-fish
                                | & Corpora |   dataset, custom domain)
                                +-----------+
```

Component notes:

• **Multilingual QA Layer**  
  − Retriever: dense or hybrid; can exploit MT-expanded corpora (AAAI 2021) for low-resource languages.  
  − Reader: span extraction or generative; augment with *arbitration objective* to enforce language-invariant embeddings.  
  − Arbiter: judges answer *type* (definition, causal, affect) following CLEF-derived fine-grained taxonomy.

• **Story State & Knowledge Graph**  
  − Maintains fabula events, character arcs, factual world model; dynamic updates à la AAAI 2023 graphs.

• **Narrative Planner**  
  − Controls story progression. Questions answered by QA can trigger plan repairs (e.g., “Where is the antagonist now?” ⇒ missing location yields subplot insertion).

• **Language-Specific NLG**  
  − Realisers per language, reusing 70-80 % shared code; culture-bound templates for referring expressions, viewpoint, dialogue registers.

• **Evaluation Loop**  
  − Automatic metrics (BLEU-like + narrative entailment) *and* MAIN-style human annotation to close the gap uncovered by DSTC-11.


---

## 5  Evaluation Framework

1. **Automatic QA Accuracy**  
   − Use MLQA, TyDiQA for baseline; extend with long-form benchmarks (LF-SQuAD/QUOREF) adapted to target languages.  
   − Score span overlap *and* answer-type agreement (cf. CLEF ambiguity lessons).
2. **Narrative Quality**  
   − Macro-structure: story grammar elements (setting, initiating event, attempts, outcome, moral) using MAIN coding.  
   − Micro-structure: clause complexity, discourse markers, culturally appropriate speech acts.
3. **Human Ratings**  
   − Grammar & Dialogue (replicating 2019 study) but per language, using native speaker panels.
4. **User Engagement**  
   − Real-time settings: click-throughs, dwell time, retelling frequency.  
   − Offline: Likert scales on coherence, novelty, enjoyment.
5. **Cross-Cultural Perception Shift**  
   − Controlled A/B tests of stylistic variations (PoV, direct vs. indirect speech) as in Fabula Tales studies.

---

## 6  Design Recommendations & Unsolicited Suggestions

1. **Adopt a Fabula/Medium Split Early**  
   − Keeps localisation costs predictable; dovetails with per-locale NLG modules.
2. **Leverage MT-Bootstrapped Silver QA Pairs**  
   − For each new language, translate a curated English narrative QA corpus; fine-tune bilingual retriever/reader before freezing to monolingual.
3. **Hybrid Retrieval for Long Contexts**  
   − Combine sliding-window attention with knowledge-graph retrieval to circumvent LLM context limits.
4. **QA-Driven Consistency Checks**  
   − Periodically auto-query the story graph (“Who currently owns the magic key?”). Discrepancies trigger planner repairs.
5. **MAIN-Aligned Picture Sequences for Younger Audiences**  
   − Use MAIN’s picture stories to auto-generate age-appropriate QA pairs; ideal for educational tools.
6. **Model Answer-Type Uncertainty Explicitly**  
   − Following CLEF’s observed ambiguities, train a classifier to tag answers (definition, causality, emotional state) and threshold differently per type.
7. **Evaluation Metric Ensemble**  
   − Blend multilingual BERTScore, COMET-Kiwi (for semantics), and novel *Narrative Entailment Score* trained on LF-SQuAD.
8. **Dialogue Register Modules**  
   − Use linguistic resources (e.g., Japanese keigo templates, Spanish t-v distinction) to patch the grammar/dialogue gap seen in 2019 human study.
9. **Exploit QALL-ME for Ontology Mediation**  
   − Story-domain ontologies (characters, settings, timelines) can plug into QALL-ME’s SOA so questions like “Which battles occurred near Riverrun?” route seamlessly.
10. **Future-Proof via Modality Expansion** *(speculative)*  
    − Plan for image-grounded QA (Manchester dataset) and audio prosody control, anticipating 2026-2027 multimodal generation APIs.

---

## 7  Open Research Questions

1. **Cultural Pragmatics Modeling**: Can we jointly embed QA answers and narrative utterances in a space that captures politeness, indirectness, honorifics?  
2. **Narrative Entailment Benchmarks**: Need multilingual corpora where story-specific logical entailments are labelled (e.g., causal chains across translations).  
3. **Real-Time Latency vs. Coherence Trade-off**: How to schedule deep QA checks without stalling interactive co-creation sessions?  
4. **Metric Alignment**: What surrogate automatic metric best predicts MAIN-style human judgments across languages?  
5. **Cross-Media Consistency**: For transmedia franchises, how to keep QA-derived story facts consistent across novel, comic, game dialogue?

---

## 8  Roadmap (12-Month, Aggressive)

| Month | Milestone |
|-------|-----------|
| 0-1 | Scope languages (≥ 3 high-resource, 2 low-resource). Collect MAIN & Manchester datasets; set up QALL-ME instance. |
| 2-3 | MT-bootstrap silver QA pairs for low-resource languages. Train multilingual retriever/reader with adversarial + arbitration objectives. |
| 4-5 | Build language-independent story planner; integrate dynamic knowledge graph. |
| 6-7 | Develop per-language NLG modules; implement dialogue register templates. |
| 8 | Implement QA-triggered consistency checks in planner. |
| 9 | Internal evaluation: automatic + 20-person human panel using MAIN scheme. |
| 10-11 | Pilot interactive demo (education or game) with real-time QA steering. Collect user engagement analytics. |
| 12 | Public release of benchmark, code, and evaluation report; iterate on metric alignment study.

---

## 9  Conclusion

The convergence of multilingual QA advances (CLEF legacy through AAAI 2021 transfer learning), decoupled narrative generation pipelines, and ontology-driven architectures (QALL-ME) makes QA-guided multilingual storytelling technically feasible today. The main bottlenecks have shifted from core QA accuracy to (i) culturally nuanced realisation, (ii) long-context management, and (iii) trustworthy evaluation. By embracing a fabula/medium split, leveraging MT-bootstrapped QA data, and embedding MAIN-style human evaluation early, practitioners can deliver interactive or offline storytelling systems that scale to many languages while maintaining narrative coherence and cultural resonance.

*(End of Report)*

## Sources

- http://clef.isti.cnr.it/2008/working_notes/terol-paperCLEF2008.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/17491
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.43.1585
- https://archive-ouverte.unige.ch/unige:55056
- http://hdl.handle.net/10481/48541
- http://hdl.handle.net/11590/364042
- http://tanev.dir.bg/MultilingualLibraries.pdf
- http://www.rug.nl/science-and-society/centre-for-information-technology/research/hpcv/publications/scientific_publications/bouma-clef2006.pdf
- http://tubiblio.ulb.tu-darmstadt.de/93222/
- https://hal.inria.fr/hal-01005381
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.61.2599
- https://ojs.aaai.org/index.php/AIIDE/article/view/21981
- http://arxiv.org/abs/2306.12794
- https://eprints.whiterose.ac.uk/182092/3/01427237211064695.pdf
- http://hdl.handle.net/11381/2840988
- http://hdl.handle.net/11582/43583
- https://animorepository.dlsu.edu.ph/cgi/viewcontent.cgi?article=12773&amp;context=etd_masteral
- https://doi.org/10.1007/978-3-319-77842-6_10
- http://hdl.handle.net/11582/2536
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-447027
- http://hdl.handle.net/10045/87149
- http://stp.lingfil.uu.se/~joerg/published/eamt09_mt4qa.pdf
- http://publica.fraunhofer.de/documents/N-31573.html
- http://arxiv.org/abs/2207.01918
- http://nbn-resolving.de/urn/resolver.pl?urn:nbn:de:hebis:30:3-347825
- https://research.rug.nl/en/publications/f974de16-ce6a-4a07-b14b-aa82624e2edf
- http://hdl.handle.net/2142/104919
- http://hdl.handle.net/2072/405531
- http://www.loc.gov/mods/v3
- https://ojs.aaai.org/index.php/AAAI/article/view/21286
- https://dspace.library.uu.nl/handle/1874/414719
- https://zenodo.org/record/6940046
- http://hdl.handle.net/11582/2038
- https://escholarship.org/uc/item/0mf0f4js
- https://zenodo.org/record/5137399
- https://hal.archives-ouvertes.fr/hal-00456700
- http://www.qristal.fr/pub/Cross