from typing import Dict, List


RUBRIC_LABELS = {
    "depth": (
        "The Research Depth rubric evaluates how well the report traces mechanistic/causal chains, employs multi-step reasoning, and specifies the temporal scope of claims."
    ),
    "breadth": (
        "The Research Breadth rubric evaluates the diversity of evidence across contexts (regions/biomes/tasks), methods or interventions, and scales."
    ),
    "rigor": (
        "The Scientific Rigor rubric evaluates the clarity of methods and statistics and the handling of uncertainty and limitations."
    ),
    "innovation": (
        "The Innovation rubric evaluates the novelty of contributions, whether speculation is explicitly flagged, and the presence of testable, actionable ideas."
    ),
    "gap": (
        "The Research Gap rubric evaluates how clearly, concretely, and actionably the report identifies gaps or next steps."
    ),
}



HIGH_SIGNALS = {
    "depth": [
        "Explicit multi-step mechanisms (driver → mediator → outcome) with causal connectors.",
        "Temporal specificity (lags, durations, windows) tied to effects.",
        "Assumptions/boundary conditions for mechanistic links are stated.",
    ],
    "breadth": [
        "Multiple contexts (regions/taxa/tasks) and/or multiple methods/interventions.",
        "Touches multiple scales (e.g., local→regional or individual→ecosystem).",
        "Triangulates evidence across datasets/sources.",
    ],
    "rigor": [
        "Concrete statistics and methodological clarity.",
        "Acknowledges uncertainty, limitations, and potential biases.",
        "Reproducibility signals when relevant (data/code/baselines).",
    ],
    "innovation": [
        "Novel synthesis or angle vs prior work.",
        "Speculation is clearly flagged and bounded.",
        "Proposes testable, concrete next steps.",
    ],
    "gap": [
        "Explicit, operational gaps (what is missing, where, and why).",
        "Links gaps to decisions/consequences; proposes steps to close.",
        "Avoids vague platitudes.",
    ],
}

LOW_SIGNALS = {
    "depth": [
        "Vague 'X affects Y' without pathway.",
        "No causal connectors or temporal qualifiers.",
        "Single-step claims; mediators/moderators ignored.",
    ],
    "breadth": [
        "Single context/method; no comparison or generalization.",
        "No discussion of scale or transfer.",
        "Ignores relevant diversity dimensions.",
    ],
    "rigor": [
        "Claims without statistics or methodological details.",
        "No uncertainty/limitations.",
        "No reproducibility signals when relevant.",
    ],
    "innovation": [
        "'More research is needed' without specifics.",
        "Speculation presented as fact.",
        "No differentiation from prior work.",
    ],
    "gap": [
        "Vague 'gaps' without scope/operationalization.",
        "No path to close the gap.",
        "Contradictory or unsupported gap statements.",
    ],
}


# ---- System prompt -----------------------------------------------------------

def system_prompt() -> str:
    """
    System prompt used for every metric. Keep it concise and strict, aligned with YESciEval-style judging.
    """
    return (
        "You are a careful, consistent scientific evaluator. "
        "Follow the rubric strictly; judge only evidence present in the input report text. "
        "Be conservative and precise. Use the full 0–100 integer range (fine granularity such as 53 or 67 is allowed). "
        "Do not invent content; do not rely on external knowledge. "
        "Return only JSON that matches the specified schema; no explanations."
    )


# ---- User prompt (5 sections) -----------------------------------------------

def _bullets(lines: List[str]) -> str:
    return "\n".join([f"- {s}" for s in lines])

def build_user_prompt(
    *,
    metric: str,
    topic: str,
    report_md: str,
    examples_block: str
) -> str:
    """
    Build the user prompt with exactly five sections: Context, Task Description, Task Instructions,
    Input format, Output format. Metric is one of {'depth','breadth','rigor','innovation','gap'}.
    """
    topic = (topic or "ecology").strip().lower()
    if topic not in {"ecology", "nlp"}:
        topic = "ecology"

    domain_note = (
        "Domain: ECOLOGY — emphasize ecological mechanisms, multi-scale context, and conservation/climate relevance."
        if topic == "ecology" else
        "Domain: NLP — emphasize task framing, datasets/baselines, error/limitations, and reproducibility."
    )

    rubric_text = RUBRIC_LABELS[metric]
    high_blk = _bullets(HIGH_SIGNALS[metric])
    low_blk  = _bullets(LOW_SIGNALS[metric])

    return f"""\
Context
- The dimension is analogous to our quantitative context for '{metric}'.
- {domain_note}

Task Description
- Evaluate this rubric:
  {rubric_text}
- Produce a single integer score in [0, 100].

Task Instructions
- Use only evidence present in the report text; do not hallucinate or use external knowledge.
- Strictness: 50 is "partially addressed". Adjust precisely up/down; do not round to multiples of 5/10.
- High-signal indicators include:
{high_blk}
- Indicators for high-signals (non-exhaustive; presence not required):
{examples_block}
- Also think about more keywords that could fit the high-signal indicators.

- Low-signal indicators include:
{low_blk}

- Granularity policy:
  - 90–100 only if evidence is comprehensive across the high-signal bullets.
  - 0–10 if evidence is absent or directly contradicted.
  - If borderline between two integers, choose the more precise (e.g., 53 rather than 55).

- Strictness policy:
  - Really think if your are not sure; be conservative and precise.
  - You are a Judge, don't be too soft.
  - Don't be overly optimistic.


Input format
[REPORT_START]
{report_md}
[REPORT_END]

Output format
- Return ONLY a strict JSON object: {{"score": <integer 0..100>}}. No additional keys or text.
"""

