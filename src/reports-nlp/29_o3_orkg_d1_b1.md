# Final Report: Prompt-Engineering Strategies for Resolving Ambiguous Translations in Neural MT

*Prepared 2025-09-04*

---

## 1  Problem Statement and Scope
Ambiguity—lexical, syntactic, or pragmatic—remains the single largest source of major errors in otherwise fluent neural machine translation (NMT). Recent advances in large language models (LLMs) make it feasible to *inject transient context or linguistic hints at inference time* (a.k.a. prompt engineering) rather than retraining a full model.  
The original query asks how to resolve ambiguous translations via language-model prompting. Although the follow-up questionnaire (language pair, ambiguity type, metrics) was left blank, we intentionally design a *general framework* that:  
* works for any high-resource language pair (illustrated with English↔French and Hindi→English);  
* addresses **all three** major ambiguity classes (lexical sense, syntactic attachment/scope, and culturally loaded idioms);  
* supports both source→target and bidirectional workflows;  
* evaluates with automatic metrics (BLEU, COMET) **plus** targeted human sense-accuracy judgment.

## 2  Key Empirical Learnings
We incorporate **all** prior findings supplied:

| ID | Finding | Implication for Prompt Design |
|----|---------|------------------------------|
| L-1 | *Document-level context* injected as a lightweight prompt into a **sentence-trained** MT model (University of Pisa 2023) boosts BLEU and removes many lexical ambiguities **at negligible training cost**. | Provide surrounding sentences/section abstracts as an *auxiliary prefix* (or separate channel) during inference. |
| L-2 | Adding *explicit syntactic supertags* to the source prompt in a Transformer-based interactive MT system yields +2.65 BLEU (Fr→En) and +6.55 points word-prediction accuracy (Hi→En). | Encode fine-grained syntactic cues (e.g., CCG or STAG tags) directly in the prompt to steer disambiguation of attachment and argument structure. |
| L-3 | Legacy interlingua MT (KANT, 1991) shows that **rule-based disambiguation before generation** reduces competing parses. | Deploy a lightweight *pre-prompt filter* that heuristically prunes senses/structures before LLM prompting—acts as a quality-control gate especially for COMET-oriented optimization. |

These three ingredients—(i) document-level context, (ii) syntactic supertags, (iii) rule-based filtering—constitute mutually reinforcing stages in a modern prompting pipeline.

## 3  Proposed Multi-Stage Prompting Pipeline
```
┌────────────────────┐   ┌────────────────────┐   ┌──────────────────┐   ┌──────────────┐
│1  Pre-filter &     │→ │2  Source Rewriter   │→ │3  Core MT Model  │→ │4  Post-LLM    │
│   Sense Pruner     │  │   (Supertags + Ctx) │  │   (frozen)       │  │   QA/Rerank   │
└────────────────────┘   └────────────────────┘   └──────────────────┘   └──────────────┘
```
1. **Pre-filter (Rule-Based / KB-Aided)**  
   • Tokenize & POS-tag.  
   • Consult bilingual lexicon or WordNet to *enumerate* possible senses.  
   • If >1 plausible sense → insert *disambiguation markers* (e.g., `〈SENSE=financial-bank〉`).
2. **Source-side Rewriter with Supertags & Context**  
   • Fetch ±2 sentences of document context; compress via extractive summarizer if long.  
   • Run CCG or SRL tagger → append tags as inline markers:  
     > `[NP/finance] bank [VP took] [NP/loan]`  
   • Resulting augmented source becomes the *prompt* for step 3.
3. **Core MT Engine** (frozen sentence-trained Transformer or mid-size LLM).  
   • No retraining; rely on attention to pick disambiguated sense.  
4. **Post-LLM Reranker / ChatGPT-style Agent**  
   • Generate *n* hypotheses.  
   • Use a separate LLM with chain-of-thought justification prompt:  
     "Which hypothesis is most consistent with *〈context〉*? Provide rationale then output 1/2/3."

### Why a Pipeline?
*Stage separation* enables independent error analysis and A/B testing—mirrors the KANT finding (L-3) that early pruning prevents downstream mistakes.  
The Pisa (L-1) result suggests we can inject document context *cheaply*; supertags (L-2) further steer syntax when semantics alone is insufficient.

## 4  Concrete Prompt Templates
Below we give sample templates for English→French; adapt accordingly.

### 4.1  Document-Context + Supertag Prompt
```text
### Task: Translate the SOURCE sentence into French.
### Document context (2 preceding, 1 following):
[1] The central bank left rates unchanged.  
[2] Analysts expected a hike.  
[+1] Markets opened slightly higher on Monday.
### Source (with supertags):
[NP/FINANCE] bank [VP/PAST] left [NP/PL] rates unchanged .
### Translation:
```

### 4.2  Post-Generation Reranker Prompt
```text
You are an expert bilingual editor. Below are three candidate translations and the relevant context. 
Pick the best candidate; justify briefly under 'Reasoning:' then output the candidate number only under 'Choice:'.

Context (English): The central bank ... Markets opened ...
Candidate 1 (French): ...
Candidate 2 (French): ...
Candidate 3 (French): ...
```

## 5  Evaluation Design
### 5.1  Datasets
• **MuSe, ContraWSD, and OpenSubtitles AmbiSet** for lexical sense.  
• **CRITT-TED** for discourse-level pronoun and ellipsis.  
• **Hi→En Health-Subdomain** to replicate L-2.

### 5.2  Metrics
1. **General Quality**: BLEU, TER, COMET-20 for each system variant.  
2. **Ambiguity-Focused**:  
   • *WSD Accuracy*: percentage of tokens whose word-sense tag matches manual gold.  
   • *Attachment Accuracy*: proportion of PP-attachment decisions judged correct by syntactic annotators.  
3. **Human Adequacy/Fluency** (5-point Likert) on 200 sampled sentences.  
4. **Effort-Sensitive**: Keystroke-Mouse-Action (KMA) delta in a simulated post-editing study.

### 5.3  Ablations
• Base MT (no prompt) —> +Context —> +Supertags —> +Pre-filter —> +Rerank.  
• Each increment measured to estimate marginal gain (cf. L-1 & L-2).

## 6  Anticipated Results (Projected)
| Variant | BLEU (En→Fr) | WSD Acc. | Post-edit KMA | Comment |
|---------|--------------|----------|---------------|---------|
| Baseline | 32.4 | 80.1% | 100% | – |
| +Context | 33.8 | 85.7% | 93% | Mirrors Pisa 2023 (L-1). |
| +Supertags | 34.7 | 88.2% | 88% | Parallels 2.65 BLEU gain (L-2). |
| +Pre-filter | 34.9 | 89.1% | 87% | Small but significant; legacy KANT (L-3). |
| +Rerank | **35.4** | **91.9%** | **82%** | Best COMET; human eval ↑.

## 7  Risk & Mitigation
1. **Prompt Length Limits** – Truncate context with neural summarizer; empirically ≤1,024 tokens works on GPT-4o.
2. **Tagging Noise** – Use confidence-weighted tags; if p(tag)<0.8 drop it.
3. **Hallucination** – Post-reranker penalizes hypotheses containing out-of-context named entities.
4. **Domain Drift** – Maintain per-domain pre-filter rule sets; fallback to generic WSD model.

## 8  Contrarian / Forward-Looking Ideas
*High speculation flagged* 🔮
1. **Sense-aware Retrieval-Augmented MT**: Index bilingual corpora by BabelNet synset; at inference, retrieve parallel examples sharing sense id and embed them in the prompt (few-shot with sense homogeneity).  
2. **Constraint-Programming Decoder**: Use a SAT/SMT solver to forbid output tokens incompatible with pre-filter senses (hard constraint vs soft re-ranking).  
3. **RLHF-Tuned Reranker**: Reinforcement-learning fine-tune the post-LLM agent on human WSD rewards, decoupling it from BLEU orientation.  
4. **Bidirectional Round-Trip Verification**: Translate source→target and back; if meaning diverges, invoke an *adaptive sense-clarification prompt* asking the LLM to choose a different sense.

## 9  Implementation Timeline
| Month | Milestone |
|-------|-----------|
| 1 | Build corpus & gold ambiguity annotations; integrate rule-based filter. |
| 2 | Implement context-injection wrapper; reproduce Pisa 2023 results. |
| 3 | Add CCG/STAG tagger & supertag prompt; run ablation. |
| 4 | Develop LLM reranker with chain-of-thought; human eval round 1. |
| 5 | Integrate speculative retrieval-augmented prototype; stress test. |
| 6 | Full human evaluation, write paper for ACL 2026.

## 10  Conclusion
Leveraging *prompt-time* interventions is a cost-effective path to disambiguating NMT without retraining the main engine. Empirical evidence (Pisa 2023, supertag study, and KANT legacy insights) collectively suggests that stacking (i) document context, (ii) fine-grained syntactic cues, and (iii) pre-filtering yields additive gains in both automatic scores and human judgments.  
The proposed pipeline generalizes across language pairs, captures lexical and syntactic ambiguity, and remains modular for future plug-ins such as retrieval-augmented prompts or RL-grounded rerankers.  
Next steps include scaling to low-resource languages and quantifying gains under strict latency budgets for real-time interactive translation.

---
*End of Report*

## Sources

- http://folk.uio.no/plison/pdfs/projects/fripro2013.pdf
- http://hdl.handle.net/1959.14/156247
- http://etd.adm.unipi.it/theses/available/etd-04122023-101720/
- http://www.cslu.ogi.edu/%7Egormanky/courses/CS662/PDFs/lecture_notes/2015-03-03-handout.pdf
- http://doras.dcu.ie/22664/
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.56.6024
- https://hdl.handle.net/10356/165027
- https://orcid.org/0000-0001-5736-5930
- http://dx.doi.org/10.1145/2518130
- http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.67.451