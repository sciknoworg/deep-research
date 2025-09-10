# Dialect-Aware Machine Translation with Prompted Lexicon Entries as Examples  
*A design and research blueprint*  
**Date:** 2025-09-04  

---

## 1. Problem Framing
Modern MT systems routinely ignore dialectal variation, collapsing regional, socio-linguistic, and register differences into a single “standard” variety. For high-variance languages (Arabic diglossia, Chinese topolects, Indo-Aryan spectra, African-American English, etc.) this leads to degraded intelligibility, loss of identity cues, and mis-translations of lexicalised cultural items.  

The goal is **dialect-aware MT (DA-MT)** that can:
1. Detect the dialect of an input segment.
2. Exploit dialect-specific lexicons supplied *on-the-fly* as few-shot exemplars (“prompted lexicon entries”).
3. Translate into a target variety while obeying user constraints (morphology, terminology, style).  

We assume flexibility in architecture: both (i) large language models used in an in-context **prompt engineering** regime, and (ii) conventional Transformer-based NMT enhanced with control signals or constraints.  

---

## 2. Take-aways from Prior Work
The three cited findings give concrete levers:

| Finding | Mechanism | Transferable Lessons for DA-MT |
|---------|-----------|--------------------------------|
| **P14-2125** – Sentence-level dialect ID switching among 4 Arabic MT engines ⬆︎ BLEU +1.0 (vs best single) | Light-weight classifier + system selection | (i) Dialect ID is low-hanging fruit; (ii) modular, engine-per-dialect architecture outperforms monolithic training when resources are skewed. |
| **Lexicalised CCG “supertag” injection** in interactive NMT ⬆︎ WPA +5.65 % (Fr-En), +19.1 % (Hi-En) | Syntax-aware source annotation | Explicit linguistic tags alter decoder search to match human expectations; can lower post-edit effort in a constrained setup. |
| **Lemma-level user constraints** (En→Cs) removed 46 % of inflection errors | Constraints encoded inline, then forced during decoding | Morphologically rich targets benefit from lexical specification *and* morphological freedom; inline constraints do not degrade general quality. |

Implications:
1. **Switching matters** – even a +1 BLEU is non-trivial on strong baselines.
2. **Fine-grained linguistic tags** synergise with interactive workflows; dialectal cues are an analogous “tag”.
3. **Constraint injection works** – essential for lexicon fidelity.

---

## 3. Architectural Space
### 3.1 Prompt-Engineering with Frontier LLMs  
Pros: zero/low-shot coverage of dialects, rapid iteration, no training.  
Cons: latency, hallucinations, opacity of constraint satisfaction, licensing.

Basic recipe:
```
[System] You are a dialect-aware translator …
[Few-shot] <dialectal src 1> → <target 1>
           <glossary entry “جُوز” = “walnut”> …
[User] <new source segment>
```
We can **prepend a dialect code** (e.g. `<ms_egy>`) and inject lexicon pairs as demonstrations.  

### 3.2 Transformer-based Constrained NMT  
Pros: deterministic, tractable to fine-tune, can run locally/edge, supports hard lexical constraints.  
Cons: Need of parallel data; updating model for new dialects is costly.

Techniques:
1. **Inline constraint tokens** (Hasler et al.) – works for morphology-rich languages.
2. **Vocabulary gating** – restrict softmax to lexicon translations.
3. **Factorised inputs** – add dialect ID, supertags, lemma.

### 3.3 Hybrid & Retrieval-Augmented  
A retrieval layer surfaces dialect-specific parallel snippets or lexicon entries; the MT model (LLM or NMT) conditions on them.  

---

## 4. Proposed End-to-End System
### 4.1 Pipeline Overview
1. **Dialect Identification**  
   • Pre-classifier at sentence or segment level (fasttext, adapter, or LLM zero-shot).  
   • Output: probability distribution over dialects.  
2. **Resource Routing**  
   • If **LLM mode**: assemble a prompt with:   
     – ISO-style dialect tag (e.g. `ar_EGY`),   
     – top-k lexicon entries relevant to the source,   
     – 1-2 parallel exemplars from retrieval memory.  
   • If **NMT mode**: choose dialect-specialised decoder or load dialect embeddings.  
3. **Constraint & Syntax Injection**  
   • For NMT:   
     – Prefix `<lex=walnut#جوز>` inline tokens.   
     – Insert supertag sequence on source side (`<NP/NP>` etc.) to lower post-edit.  
4. **Decoding & Post-Editing Interface**  
   • Interactive suggestions with forced constraints (e.g. SGD-beam search with hard spans).  
   • UI highlights lexicon hits + dialectal markers.  
5. **Feedback Loop**  
   • Accepted post-edits join the retrieval memory and fine-tune incrementally.  

### 4.2 Component Details
• **Dialect Tags as Supertags Analogy**: Tagging *itself* influences decoder; we can embed `<dialect|egyptian>` tokens analogous to CCG tags, leveraging the +2.65‒+6.55 WPA gains observed.  

• **Morphology Handling on Target**: Use lemma constraints (`jít` vs `šel`) then let the model inflect; prior work removed >40 % errors.  

• **System Selection Heuristic**: If dialect probability `p(d_i)` > θ, route to engine `E_i`; else fallback to best MSA/standard engine with constraint tokens.  

---

## 5. Data & Resource Strategy
1. **Parallel Corpora**  
   • Crawl regional social media, lyrics, subtitles.  
   • Use *data augmentation* by back-translating monolingual dialect corpora.  
2. **Lexicon Construction**  
   • Crowd-source dialectal term pairs (Walnut ↔ جوز).  
   • Exploit Wiktionary, dialect dictionaries, cross-dialect word alignments.  
3. **Alignment Heuristics**  
   • Character n-gram similarity for cognates (esp. Arabic dialects) to auto-bootstrap lexicon.  

---

## 6. Evaluation Framework
### 6.1 Automatic Metrics
• **BLEU / COMET** on pooled dev/test per dialect.  
• **Dialectal Fidelity Score (DFS)** – percentage of dialect-specific lexical items preserved.  
• **Constraint Success Rate (CSR)** – were forced terms realised *exactly*?  

### 6.2 Human Studies
• **Crowd-sourced dialect speakers** rate naturalness (Likert 1-5).  
• **Post-edit Effort (WPA)** replicating the supertag study; target ≤ −10 % vs baseline.  
• **Contrastive minimum-pair test suite**: e.g. `جوز` (walnut) vs `زوج` (husband) contrast in Egyptian vs MSA.  

### 6.3 Statistical Validation
Randomised blocked design; bootstrap confidence bands; *Holm-Bonferroni* for multiple metrics.  

---

## 7. Implementation Road-map (18-Month)
| Phase | Milestones | Notes |
|-------|------------|-------|
| **0-3 m** | Prototype dialect classifier; gather 500 lexicon pairs; wrap GPT-4 prompt demo | Fast validation of concept |
| **3-6 m** | Build dialect-specific sub-corpora; fine-tune 4 small NMT models; implement constraint tokeniser | Use open NLLB initialisation |
| **6-9 m** | Multi-engine switcher; behaviour testing; DFS metric tool | Expect +1 BLEU vs single model |
| **9-12 m** | Syntax/supertag augmentation; interactive Post-edit UI; measure WPA | Target ≥ 5 % WPA reduction |
| **12-15 m** | Retrieval-augmented prompting; dynamic lexicon injection | Evaluate latency and CSR |
| **15-18 m** | Large-scale human evaluation; rollout in pilot localisation pipeline | Collect feedback for v2 |

---

## 8. Risks & Mitigations
1. **Sparse Dialect Data** – Mitigate via back-translation, synthetic paraphrasing, few-shot LLM generalisation.
2. **Constraint Violations by LLM** – Use post-hoc regex verifiers and re-prompt; consider Constrained-Decoding wrapper.
3. **Classifier Mis-Routing** – Ensemble dialect ID; confidence threshold for fallback.
4. **User Trust** – Transparent highlighting, editing affordances; log provenance of lexicon usage.

---

## 9. Future & Speculative Directions
• **Diffusion-based Decoders** for fine-grained control signals (flagged *speculative*).  
• **Meta-Learning**: train a control transformer that outputs dialect-aware prompts for any downstream LLM.  
• **Federated Fine-tuning on Translator Edits** to respect data privacy.  
• **Code-mixed Inputs**: exploit joint segmentation + tagging to handle intra-utterance shifts.  

---

## 10. Summary Bullet Points
1. Prior work shows clear benefits from (i) dialect switching (+1 BLEU), (ii) syntax tag injection (−20 % post-edit), (iii) morphological lemma constraints (eliminate half of inflection errors).  
2. Combine these techniques in a modular DA-MT pipeline that supports both LLM prompts and traditional NMT.  
3. Central components: dialect ID, lexicon-based constraint injection, optional supertags, retrieval-augmented prompts.  
4. Evaluation must balance BLEU/COMET with dialect fidelity and human post-edit effort.  
5. An 18-month staged plan reaches pilot deployment while gathering data for next-generation models.

---

*Prepared by: Expert Research Assistant*

## Sources

- http://folk.uio.no/plison/pdfs/projects/fripro2013.pdf
- http://www.aaai.org/Papers/Symposia/Spring/1993/SS-93-02/SS93-02-007.pdf
- http://faculty.washington.edu/fxia/papers_from_penn/iccc96.pdf
- http://hdl.handle.net/11346/BIBLIO@id=2165773603281921920
- https://hdl.handle.net/10356/165027
- http://repository.nkfust.edu.tw/ir/handle/987654321/15684
- https://zenodo.org/record/1340038
- https://orcid.org/0000-0001-5736-5930
- http://aclweb.org/anthology/P/P14/P14-2125.pdf
- http://dx.doi.org/10.1145/2518130