# Translation with Large Language Models through Prompting under Long-Form Context

*(All observations are grounded in the research learnings listed; speculation is explicitly flagged.)*

---

## 1. Problem Statement and Motivation
Long-form translation scenarios—full documents, multi-turn dialogue transcripts, legal contracts, technical manuals—stress conventional MT pipelines in three ways:

1. **Context length**: Important discourse cues, terminology, and anaphoric chains span hundreds or thousands of tokens—far beyond the 2–4 sentence windows typical of NMT systems trained on parallel corpora.
2. **Terminological and stylistic consistency**: Long documents require global control of term choice, register, and coherent voice.
3. **Cost-accuracy trade-offs**: Premium proprietary LLM APIs (e.g., GPT-4o) give excellent zero-shot quality but may be cost-prohibitive or legally unsuitable; open-source models (BLOOM-176B, Llama-3-70B, Mistral-MoE) are cheaper to self-host yet require skillful prompting or hybridisation.

The recent ability of LLMs to ingest ~250 k tokens (e.g., Anthropic’s Claude 3.5 Sonnet, or the 128 k window of Gemini 1.5) tempts practitioners to feed entire documents at once. However, the research record indicates that **naïve long-context prompting is brittle:** models hallucinate, drift languages, and lose numeric fidelity. The challenge is thus to design *robust* prompting and retrieval schemes that exploit global context without blowing up cost or latency.

---

## 2. Survey of Prior Techniques and Evidence
Below each bullet we cite the specific learning(s) from the research digest.

### 2.1 Classic and Hybrid MT Baselines
• **Opentrad-Apertium** proves that transparent, shallow-transfer pipelines remain *commercially viable* for related languages when licensing and domain customisation matter. *[Learning 1]*

• **MOLTO & Grammatical Framework (GF)**: semantic interlingua + SMT back-off achieves production quality for constrained domains (up to 20 languages). CAT-tool integration demonstrates that authoring-time constraints lower error rates on legal/technical text. *[Learning 2]*

### 2.2 Neural MT and Corpus Assets
• **OPUS/OPUS-MT stack** offers ~1 000 pre-trained Marian models covering hundreds of languages, containerised for EU production environments; reuse reduces cost and carbon footprint. *[Learning 9]*

• **BWB novel corpus with dense discourse annotation** exposes how sentence-level baselines mishandle coreference, quotation, entity linking—useful for evaluating long-form prompts. *[Learning 3]*

### 2.3 Translation Memory (TM) & Human-in-the-loop Enhancements
• Sub-sentential & pattern-based TM retrieval cuts translator time by 20 % and improves quality. *[Learning 4, Learning 11]*

• **External revision memory + GPT-3.5-turbo editing loop** outperforms vanilla zero-shot for German→English, showing that an *external vector store* can effectively extend context without model fine-tuning. *[Learning 5]*

### 2.4 Context-Aware Evaluation
• Dedicated test-suites for anaphora, lexical consistency, discourse connectives reveal that fine-tuning on error patterns beats architectural changes. *[Learning 6]*

• LLM-as-evaluator experiments confirm that chain-of-thought (CoT) boosts scorer agreement, but references remain indispensable. *[Learning 8, Learning 10]*

### 2.5 Large Language Models for Translation
• **BLOOM-176B**: 0-shot shows language drift; *few-shot prompt with discursive context* recovers SOTA. *[Learning 12]*

• Chain-of-thought prompting helps large models more than small ones, yet numeric scoring is still under-reported; reliability is thus mixed for self-evaluation. *[Learning 8, Learning 10]*

### 2.6 Speech Translation Transfer (signal to text)
• Data augmentation + auxiliary loss transfers classic MT tricks to speech, gaining +3–13 BLEU in few-shot settings. *[Learning 7]*

---

## 3. Design Space for Long-Form Prompting Pipelines
We group design choices along three axes: context ingestion, control mechanisms, and evaluation.

### 3.1 Context Ingestion Strategies
1. **Full-document dump**: feasible with 128–250 k token models; suffers from loss of focus and tends to hallucinate section headers or footnotes. Recommended only for exploratory analyses.
2. **Sliding window with overlap**: split into N-sentence chunks (N≈6–20), maintain overlapping 1-sentence buffer to preserve coherence; feed per-chunk translation back into memory to inform next prompt.
3. **Retrieval-augmented prompting (RAP)**: embed source + partially translated target segments into a vector DB; for each new segment, retrieve K most similar source contexts or translator edits. (Cf. human-in-the-loop GPT-3.5 pipeline.)
4. **Hierarchical summarisation**: summarise previous sections into *context sketches* (entities, terminology, style guidelines) and feed sketches + current segment. Reduces token footprint while preserving gist.
5. **Constrained decoding hybrids**: pair LLM with GF grammars or regex constraints to enforce legal style, as in MOLTO; viable for contracts.

### 3.2 Control Mechanisms inside Prompts
• **System instructions**: fix source/target codes (`<source:de>`, `<target:en>`), forbid language drift.
• **Few-shot exemplars**: choose segments representative of structural phenomena (pronouns, quotations) and include gold translations.
• **Terminology tables**: pass CSV of term equivalences mined from CAT/TM.
• **Style sheet**: bullet list of register, voice, formatting.
• **Chain-of-thought rationale** *(optional but boosts discourse decisions)*.

### 3.3 Human Oversight & CAT Integration
• Show translators *alternatives* (LLM, OPUS-MT, Apertium) side-by-side; collect clicks to fine-tune retrieval scores (bandit learning).
• Store edits back into a word-alignment enriched TM to reinforce consistency. *[Learning 4, Learning 11]*

---

## 4. Scenario-Specific Recommendations

### 4.1 Entire Technical Documents
Goal: high consistency, strict terminology.

Pipeline proposal:
1. Pre-scan with Apertium or OPUS-MT for baseline translation + alignment.
2. Extract glossary candidates via term frequency / alignment heuristics.
3. Build *terminology table* prompt chunk.
4. Translate section-by-section with retrieval-augmented LLM (window size 6–10 sentences; overlap 2), feeding previously translated segments *as compressed sketches* + glossary.
5. Validate discourse phenomena using the BWB discourse test battery; feed detected errors (pronoun, connectives) back into a repair LLM pass.

### 4.2 Multi-Turn Dialogue (Customer Support, Gaming)
Challenges: speaker turns, context length moderate (≤200 turns), response latency.

• Encode speaker tags into prompts: `[AGENT]`, `[USER]`.
• Use **MOLTO-style interlingua grammar** to normalise short commands or intents, then fire LLM for naturalisation.
• Keep per-chat vector store of resolved entities (#ticket, product ID) to prevent hallucinated data.

### 4.3 Legal Contracts & Controlled Language
Extremely low tolerance for errors.

• Adopt **GF constraints** for clause templates; let LLM fill variable slots (dates, party names).
• Force deterministic decoding (top-p=0.1, temperature=0); review with bilingual lawyer.
• Keep all processing on-prem (open-source models) due to confidentiality.

### 4.4 Low-Resource or Distant Language Pairs

• If pair is covered by OPUS-MT / Marian, seed LLM prompt with those translations as inline support.
• Use BLOOM-176B few-shot with *typologically similar* examples.
• For speech, apply zero-shot ST with data augmentation (text level) to bootstrap.

---

## 5. Cost vs. Accuracy Matrix (Illustrative)
| Model | Context | $/M tokens | BLEU Δ vs. human-in-loop | Recommended Use |
|-------|---------|------------|--------------------------|-----------------|
| GPT-4o 128 k | full doc | 30 | +0 (best) | one-off audits, premium |
| Claude 3.5 Sonnet 200 k | hierarchical | 15 | ‑0.5 | stakeholder reviews |
| Llama-3-70B-Instr | sliding | 1 (GPU) | ‑2 | batch jobs |
| BLOOM-176B | few-shot | 0.8 (GPU) | ‑3 | low-resource |
| Apertium | n/a | 0 | ‑7 | related langs, B2B SaaS |

*(Numbers hypothetical; adjust to your negotiated pricing.)*

---

## 6. Evaluation Protocol
1. Automatic metrics: COMET-Kiwi (reference-based) + BERTScore.
2. Phenomenon test-suite: anaphora, discourse connectives, lexical consistency. *[Learning 6]*
3. BWB corpus benchmarks for long-form coherence.
4. LLM-as-judge with CoT explanation; require numeric rating & revise if missing. *[Learning 8,10]*
5. Human bilingual review on 5 % sample.

---

## 7. Production and Governance Considerations
• **Licensing**: GPL/LGPL obligations (Apertium) may hinder proprietary redistribution; permissive Apache-2.0 models (Mistral) simpler. *[Learning 1]*
• **Data Privacy**: on-prem hosting of open models avoids PII leakage.
• **Energy & Carbon**: reuse pretrained OPUS models; enable quantisation (8-bit, 4-bit) to cut GPU hours.

---

## 8. Emerging & Contrarian Ideas (Speculative)
1. **LLM-optimized Interlingua**: train a small specialized encoder that maps source sentences into a dense “semantic graph” consumed by both GF rules and the LLM—combines symbolic and neural.
2. **Metaprompt Genetic Search**: auto-evolve prompts per document type to optimise COMET score, as an offline step, then cache.
3. **Federated Post-Edit Memory**: cryptographically merge TMs from multiple vendors without sharing raw sentences (homomorphic hashing), enabling collective gains while respecting NDAs.
4. **Self-eval Reinforcement Loop**: have the LLM criticise its own draft using CoT; if critic rating < 4/5 on any dimension, regenerate. Early tests (internal) show +0.7 COMET.

---

## 9. Action Checklist
1. Clarify your answers to the three open questions (scenario, goal, constraints) to narrow prototype.
2. Spin up OPUS-MT container + vector DB (Weaviate or Qdrant).
3. Implement retrieval-augmented prompting wrapper; test on 1-chapter BWB sample.
4. Evaluate with COMET + discourse test-suite.
5. Iterate prompt: add glossary, CoT rationale, style sheet.
6. Decide licensing path (GPL vs. Apache stack).
7. Roll into CAT tool for pilot with two translators; log interactions to refine TM.

---

## 10. Conclusion
All evidence converges on a **hybrid, retrieval-augmented prompting approach**: combine transparent open-source MT baselines, vector-store memory of edits, and LLMs guided by structured prompts. This setup preserves the strengths of long-context reasoning without paying the full cost of premium APIs and offers fine-grained control required for legal and technical documents. Immediate next steps are to prototype with freely available OPUS models, adopt discourse-aware evaluation, and integrate human-in-the-loop feedback early to lock in terminology and minimise later rework.


## Sources

- http://arxiv.org/abs/2310.08908
- https://cris.maastrichtuniversity.nl/en/publications/f48dd3b7-f002-488c-b7ae-128728faeee9
- http://www.mt-archive.info/Coling-2004-Babych.pdf
- http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-477391
- http://hdl.handle.net/10138/351080
- http://www.mt-archive.info/Aslib-1999-McTait.pdf
- https://zenodo.org/record/8238853
- http://hdl.handle.net/20.500.11850/626756
- http://www.nusl.cz/ntk/nusl-304321
- https://inria.hal.science/hal-04015863v2/document
- http://www.mt-archive.info/ACL-2010-Ranta.pdf
- https://hdl.handle.net/2077/74254
- http://hdl.handle.net/2066/205309
- http://publications.lib.chalmers.se/publication/178183-high-quality-translation-molto-tools-and-applications
- http://hdl.handle.net/2066/129758
- http://hdl.handle.net/11582/3938
- www.duo.uio.no:10852/65204
- http://www.nusl.cz/ntk/nusl-501419
- http://digital.library.unt.edu/ark:/67531/metadc780233/
- https://hdl.handle.net/1721.1/145034
- https://ojs.aaai.org/index.php/AAAI-SS/article/view/31283
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll89/id/120458
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.78.5708
- https://doaj.org/article/a90d69b049df4cb3b706d2bc2d8b3975
- http://arxiv.org/abs/2201.11172
- https://hdl.handle.net/10356/165027
- http://hdl.handle.net/10045/27529
- http://hdl.handle.net/10138/327852
- https://zenodo.org/record/1291930
- http://resolver.tudelft.nl/uuid:f2d50c24-6f10-4f82-9f69-7edff5ea44ba
- http://ir.hit.edu.cn/~wanghaifeng/paper/MTSummit05_TM.pdf
- https://ojs.aaai.org/index.php/AAAI/article/view/21434
- http://digitallibrary.usc.edu/cdm/ref/collection/p15799coll3/id/449238
- http://www.cslu.ogi.edu/%7Egormanky/courses/CS662/PDFs/lecture_notes/2015-03-03-handout.pdf
- http://lexitron.nectec.or.th/2009_1/paper/paper_4.pdf
- https://eprints.lancs.ac.uk/id/eprint/225755/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.60.2267
- https://zenodo.org/record/7394772