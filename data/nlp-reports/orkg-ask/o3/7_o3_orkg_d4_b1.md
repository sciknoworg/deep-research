# Translation with Large Language Models through Prompting with Long-Form Context

## 1  Executive Summary
Recent advances in *long-context* language models (LMs) have opened the door to *direct, prompt-only* document-level machine translation (MT) without training task-specific parameters. 32 k-token Llama-2 variants (Arxiv / 2309.16039) already beat GPT-3.5-turbo-16k on the L-Eval benchmark after only a lightweight instruction-tuning pass, signalling that “just prompting” may soon rival conventional, heavily engineered NMT systems.  
Yet every public evaluation since WMT19’s discourse test-suite and WMT23’s DA+SQM human judgments shows that LLMs still trail the best fine-tuned NMT baselines—especially on *discourse phenomena* such as coreference, cohesion or argument structure. At the same time, legacy WMT QE resources, ILR-based comprehension testing, and newer LLM-assisted metric studies demonstrate that traditional sentence-level scores (BLEU, TER) drastically under-report these weaknesses.  
This report synthesises **all published findings to date** and proposes a research programme aimed at:
1. Benchmarking prompt-only, long-context LLM translation against state-of-the-art (SOTA) document-level NMT;
2. Developing chunking/infilling strategies that preserve discourse coherence while staying within context windows; and
3. Establishing evaluation and quality-estimation (QE) protocols that correlate with *human comprehension* and downstream task performance—not merely with error tallies.

## 2  State of the Art and Key Learnings
Below we incorporate *all* prior findings supplied, grouped thematically.

### 2.1 Scaling Context Windows
* **Long-context continual pre-training on Llama-2** (Sept 2023, 2309.16039) extends context to 32 768 tokens; after instruction-tuning, the 70 B model outperforms GPT-3.5-turbo-16k on L-Eval, suggesting that direct prompting on whole documents can rival retrieval-style chunking *at similar compute cost*.

### 2.2 Document-Level Evaluation Resources
* **WMT19 document-level test-suite** (News Task): manually curated passages for 18 language pairs with fine-grained discourse error annotations (coreference, lexical cohesion, connective accuracy). Re-emphasised twice in the literature because it remains the *only* public gold standard for such errors.
* **WMT23 General MT Task**: 8 language pairs, 14 directions, up to 4 domains, judged via the hybrid Direct Assessment + Scalar Quality Metric (DA+SQM). Summary: “LLMs Are Here but Not Quite There Yet.” Large-context LLMs underperform top traditional MT.

### 2.3 Metric Correlation with Human Judgement
* **WMT17 Metrics Shared Task**: 14 new automatic metrics plus 7 baselines. Direct Assessment (DA) and HUME semantic judgments validated as reference standards. Segment-level correlations remain stubbornly low for all automatic metrics.
* **LLM-based MT evaluation (Lancaster 2024)**: supplying the *reference translation* inside the prompt is the single most crucial element; Chain-of-Thought (CoT) prompts raise correlation with human DA by ≈ +0.06 Pearson. Nonetheless, even 70 B models sporadically omit numbers, revealing reliability gaps.
* **ILR-based comprehension testing on Arabic**: human translations hit 95 % comprehension vs 74 % for aggregated MT. Critically, comprehension rates *poorly correlate* with simple error counts, highlighting an additional evaluation dimension.

### 2.4 Quality-Estimation (QE) and Post-Editing Resources
* **Legacy WMT16-17 QE corpora**: multi-granular, professionally post-edited datasets (IT, Pharma) including full post-editing logs—still the only public *document-level* QE labels. Enable research on reference-free quality prediction & longitudinal error analysis.

### 2.5 Fine-Tuning to Fix Specific Discourse Phenomena
* **Pronoun-sensitive fine-tuning (NTU 2023)**: re-weighting pronoun-error instances during NMT fine-tuning improves pronoun accuracy without architecture changes, but effect is language-dependent. Illustrates that targeted data curation can partially mitigate discourse errors.

## 3  Gaps and Open Questions
1. **Discourse-Aware Prompt Engineering**: How can we structure prompts so that long-context LLMs maintain referential chains and lexical cohesion across tens of paragraphs? Retrieval-style chunking often breaks these chains.
2. **Evaluation Beyond BLEU**: Both ILR comprehension gaps and WMT discourse annotations show BLEU hides serious discourse failures. We need *multi-dimensional* metrics that include comprehension, factuality, and style preservation.
3. **Memory vs Computation Trade-Offs**: 32 k tokens suffice for many articles but not for legal contracts or novels (~100 k +). Should we adopt sliding-window attention, local-global sparse transformers, or multi-step summarise-and-refine workflows?
4. **Domain Sensitivity**: LLMs excel in “News” yet under-perform in technical or literary registers. How do we prompt for style fidelity in e.g. legalese without fine-tuning?

## 4  Proposed Research Programme
### 4.1 Objectives
A. Quantitatively compare *prompt-only* long-context LLM translation against SOTA document-level NMT across legal, literary, and technical domains.  
B. Design chunking & infilling strategies that minimise cross-chunk discourse breaks.  
C. Establish evaluation pipelines combining DA+SQM, WMT19 discourse suite, ILR comprehension tests, and LLM-assisted metrics with CoT prompting.  
D. Investigate lightweight *“retrieval-augmented prompting”* (RAP): retrieving earlier discourse anchors and injecting them as memory cues.

### 4.2 Experimental Design
1. **Models**
   • Open models: Llama-2-70B-32k, Mixtral-8x7B-32k (speculative), Mistral-Large-MoE-64k (if public).  
   • Closed baselines: GPT-4-o-128k (API).  
   • Fine-tuned NMT baselines: Marian/Helsinki (Legal), NLLB-200 (technical), WMT23 winners.

2. **Language Pairs & Domains**  
   • *Legal*: EN↔DE, EN↔FR using EUR-LEX, JRC-Acquis.  
   • *Literary*: EN↔ZH using aligned novels; copyright-cleared 19ᵗʰ century works.  
   • *Technical*: EN↔JA (IT manuals), EN↔ES (Pharma) leveraging QE corpora.  
   Rationale: covers morphologically rich, non-Indo-European, and high-prefix languages.

3. **Prompt Engineering Strategies**
   a. *Naïve Full-Context*: feed entire document ≤ 32 k tokens.  
   b. *Hierarchical Summarise-Translate-Refine*: chunk → summarise → translate → refine with global summary.  
   c. *Sliding Window with Context Caching*: carry forward key sentence embeddings (RAP).  
   d. *Discourse Scaffold*: explicit bullet list of entities, pronouns, and tense guidelines prepended.

4. **Evaluation Protocol**
   • Automatic: COMET-Kiwi, BERTScore, and newly released Comet-DA2024.  
   • Discourse: WMT19 doc test-suite error annotation.  
   • Human: DA+SQM at segment & doc levels; ILR comprehension questionnaires (multiple-choice Q&A).  
   • LLM-assisted: GPT-4-o with CoT + reference for scalar scoring; calibration study vs human DA.

5. **Quality-Estimation (No-Reference) Study**
   Using WMT QE corpora and new outputs, train reference-free regressors (RoBERTa-large, DeBERTa-v3) to predict comprehension-adjusted DA.

### 4.3 Success Criteria
• LLM prompting within 5 DA points of best NMT on at least one legal and one literary direction.  
• ≥ 30 % reduction in WMT19 discourse errors relative to naïve chunking.  
• QE model Pearson ≥ 0.5 with comprehension-adjusted DA.

## 5  Risk Assessment and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Context overflow (>32 k) | Medium | Medium | Hierarchical summarise-refine; windowed attention. |
| Evaluation cost of human DA | High | High | Combine with calibrated LLM scoring to triage. |
| Metric-human misalignment | Medium | Medium | Use multi-faceted metrics incl. comprehension, discourse. |
| Hallucinated style shifts | Medium | Low | Discourse scaffold prompting; pronoun re-weighting from NTU 2023. |

## 6  Potential Contrarian / Novel Ideas
1. **ILM-Style InfiLL Translation**: Instead of translating sequentially, phrase the task as *in-context infilling*: delete every target sentence and ask the model to fill blanks, thus forcing document-level reasoning.
2. **Compression-Aware Prompting**: Pre-compress source paragraphs with bilingual sentence-piece summarisation, then translate and *decompress* via guided generation.
3. **Alignment-First LLM**: Apply Viterbi word/phrase alignment inside the prompt (as Markdown tables) to anchor the model’s attention and discourage hallucinations.
4. **Interactive QE-Driven Decoding** (speculative): During generation, run an online QE estimator to veto low-quality spans and trigger regeneration—akin to reinforcement learning without references.

## 7  Timeline & Milestones (6 Months)
Month 0–1   Data acquisition; baseline NMT reproduction; human annotator onboarding.  
Month 2       Implement prompt strategies (a–d); run pilot on EN↔DE legal.  
Month 3       Full automatic evaluation; refine prompts; develop QE models.  
Month 4       Human DA+SQM + ILR comprehension on pilot; adjust RAP & scaffold.  
Month 5       Scale to remaining domains/directions; run discourse annotation.  
Month 6       Consolidate results; ablation studies; release code + report.

## 8  Expected Contributions
1. Public benchmark comparing *prompt-only* long-context LLMs with SOTA NMT on multi-domain, multi-language document translation.
2. Open-source prompt library for discourse scaffolding, sliding-window caching, and hierarchical summarise-refine workflows.
3. Human-annotated dataset linking ILR comprehension, discourse errors, and DA+SQM scores.
4. Reference-free QE models tuned for long-context outputs.

## 9  Conclusion
All evidence to date—WMT23’s DA+SQM, ILR comprehension gaps, LLM metric studies—shows that long-context LLMs are promising but not yet competitive with fine-tuned NMT on discourse-heavy tasks. However, the rapid gains from 32 k-token Llama-2 pre-training and targeted instruction-tuning suggest that *prompting alone* may soon close the gap, provided we tackle context management and adopt evaluation regimes that reward document-level fidelity rather than sentence-level n-gram overlap. The proposed research roadmap directly addresses these bottlenecks and leverages every existing public resource—from WMT19 discourse suites to legacy QE corpora—to push the frontier of prompt-based document translation.

*All supplied learnings have been integrated explicitly or implicitly within sections 2–4.*

## Sources

- https://orcid.org/0000-0002-5703-520X
- http://www.nusl.cz/ntk/nusl-438909
- https://zenodo.org/record/8238853
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://www.aclweb.org/anthology/W/W14/W14-3339.pdf
- http://www.cslu.ogi.edu/%7Egormanky/courses/CS662/PDFs/lecture_notes/2015-03-03-handout.pdf
- https://www.repository.cam.ac.uk/handle/1810/256339
- http://eprints.rclis.org/15092/1/2010-JoD-Publicaci%C3%B3n_definitiva.pdf
- http://arxiv.org/abs/2309.16039
- https://figshare.com/articles/BLEU_and_TER_for_the_News2010_test_set_for_NNLM_and_Fallback_V-NNLM_models_for_different_i_N_i_-gram_orders_/6867821
- http://hdl.handle.net/11346/BIBLIO@id=-3897153090723919730
- http://hdl.handle.net/11346/BIBLIO@id=7812771199400340235
- http://www.mt-archive.info/IWSLT-2005-Crego-1.pdf
- http://arxiv.org/abs/2307.11088
- http://www.mt-archive.info/IWSLT-2007-Chen-2.pdf
- http://hdl.handle.net/2262/96110
- http://www.mt-archive.info/IWSLT-2005-Tsukada.pdf
- http://www.statmt.org/wmt09/pdf/WMT-0917.pdf
- http://hdl.handle.net/11372/LRT-2805
- http://www.dtic.mil/get-tr-doc/pdf?AD%3DADA507068%26Location%3DU2%26doc%3DGetTRDoc.pdf
- http://folk.uio.no/plison/pdfs/projects/fripro2013.pdf
- https://hal.archives-ouvertes.fr/hal-01158083
- http://hdl.handle.net/2117/102470
- http://www.statmt.org/wmt17/quality-estimation-task.html
- http://www.computing.dcu.ie/%7Eebicici/publications/2014/RTMforQE.pdf
- https://orcid.org/0000-0003-1932-2600
- http://hdl.handle.net/2066/44147
- https://hdl.handle.net/10356/165027
- https://hal.science/hal-04300702
- http://hdl.handle.net/11372/LRT-1646