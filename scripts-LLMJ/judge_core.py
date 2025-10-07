import os
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

from prompts import system_prompt, build_user_prompt

# Adjustable, shared settings
EXAMPLES_TOPK = 12
TEMPORAL_EXAMPLES = [
    "within 2–5 years", "lag of ~6 months", "after 3 months", "before 12 weeks",
    "1998–2004", "June 2012", "every 2 weeks"
]
SEARCH_DICT_PATHS = [
    ".", "./vocab", "../", "../vocab", "vocab",
    "scripts-LLMJ", "./scripts-LLMJ", "./data/vocab", "../data/vocab"
]

# ---- Schema (strict JSON) ----------------------------------------------------

def metric_schema() -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "metric_score",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 100}},
                "required": ["score"],
                "additionalProperties": False
            }
        }
    }

# ---- Model caller---------------------

def get_llm_caller(preferred_model: str = None):
    """
    Returns: (call_fn, model_used, used_repo_wrapper: bool)
    call_fn(messages, response_format) -> completion

    Intentionally no 'temperature' or 'top_p', since some o-series models reject them.
    """
    model = (preferred_model or os.getenv("LLMJ_MODEL", "") or "").strip() or None
    try:
        # Try deep-research wrapper
        here = Path(__file__).resolve().parent
        root = here.parent
        src_path = root / "src"
        if src_path.exists():
            import sys
            sys.path.insert(0, str(src_path))
        from ai.llms import _model_config_instance as MCI  # type: ignore

        if preferred_model:
            os.environ["CUSTOM_MODEL"] = preferred_model  # wrapper typically respects this

        def _call(messages, response_format=None):
            if hasattr(MCI, "generate_completion"):
                try:
                    return MCI.generate_completion(messages, response_format=response_format)
                except TypeError:
                    return MCI.generate_completion(messages)
            cfg = MCI.get_model_config()
            params = dict(messages=messages, model=cfg.get("model"))
            if response_format and cfg.get("structured_outputs", False):
                params["response_format"] = response_format
            return cfg["client"].chat.completions.create(**params)

        try:
            cfg_try = MCI.get_model_config()
            model_used = cfg_try.get("model", os.getenv("CUSTOM_MODEL") or "unknown")
        except Exception:
            model_used = os.getenv("CUSTOM_MODEL") or "unknown"
        return _call, model_used, True

    except Exception:
        # Plain OpenAI fallback
        from openai import OpenAI
        client = OpenAI()
        model_fallback = model or "o4-mini"

        def _call(messages, response_format=None):
            params = dict(messages=messages, model=model_fallback)
            if response_format:
                params["response_format"] = response_format
            return client.chat.completions.create(**params)

        return _call, model_fallback, False

# ---- Dict loading & examples -------------------------------------------------

def find_dict_file(topic: str) -> Path:
    name = f"{topic}_dictionaries.json"
    candidates = [Path(name)] + [Path(p) / name for p in SEARCH_DICT_PATHS]
    here = Path(__file__).resolve().parent
    candidates += [here / name, here / "vocab" / name, here.parent / name, here.parent / "vocab" / name]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"Dictionary file '{name}' not found in: {', '.join(str(p) for p in candidates)}")

def load_topic_dict(topic: str) -> Dict[str, Any]:
    path = find_dict_file(topic)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def _take(xs: List[str], k: int) -> List[str]:
    return [x for x in (xs or []) if isinstance(x, str) and x.strip()][:max(0, k)]

def examples_from_dicts(topic: str, metric: str, V: Dict[str, Any], topk: int = EXAMPLES_TOPK) -> str:
    """
    Build a compact examples block from domain dictionaries + temporal cues (for depth).
    """
    t = (topic or "ecology").strip().lower()
    if t not in {"ecology", "nlp"}:
        t = "ecology"

    def join(name: str, keys: List[str]) -> str:
        vals: List[str] = []
        for k in keys:
            vals += V.get(k, []) or []
        vals = _take(vals, topk)
        return f"- {name}: " + ", ".join(vals) if vals else ""

    if t == "ecology":
        if metric == "depth":
            lines = [
                join("Mechanistic terms", ["mechanistic_terms"]),
                join("Causal connectors", ["causal_terms"]),
                "- Temporal cues (examples): " + ", ".join(TEMPORAL_EXAMPLES),
            ]
        elif metric == "breadth":
            lines = [
                join("Regions/biomes", ["regions"]),
                join("Interventions", ["interventions"]),
                join("Biodiversity dims", ["diversity_dimensions"]),
                join("Ecosystem services", ["ecosystem_services"]),
                join("Scale terms", ["scale_terms"]),
            ]
        elif metric == "rigor":
            lines = [
                join("Statistics/methods", ["stats_terms"]),
                join("Uncertainty/limits", ["uncertainty_terms"]),
            ]
        elif metric == "innovation":
            lines = [
                join("Novelty terms", ["innovation_terms"]),
                join("Speculative markers", ["speculation_terms"]),
            ]
        else:  # gap
            lines = [join("Gap keywords", ["gap_terms"])]
    else:  # NLP
        if metric == "depth":
            lines = [
                join("Causal connectors", ["causal_terms"]),
                join("Mechanistic", ["training_terms", "arch_terms", "ablation_terms"]),
                "- Temporal cues (examples): " + ", ".join(TEMPORAL_EXAMPLES),
            ]
        elif metric == "breadth":
            lines = [
                join("Tasks", ["tasks"]),
                join("Datasets/metrics", ["datasets", "eval_metrics"]),
                join("Languages/compute", ["languages", "compute_terms"]),
            ]
        elif metric == "rigor":
            lines = [
                join("Statistics/validation", ["stats_terms"]),
                join("Uncertainty/limits", ["uncertainty_terms"]),
            ]
        elif metric == "innovation":
            lines = [
                join("Novelty terms", ["innovation_terms"]),
                join("Speculative markers", ["speculation_terms"]),
            ]
        else:  # gap
            lines = [join("Gap keywords", ["gap_terms"])]

    return "\n".join([l for l in lines if l])

# ---- Judging (one metric) ----------------------------------------------------

def judge_metric(
    *,
    call_llm,
    model_used: str,
    topic: str,
    report_md: str,
    metric: str,
    V: Dict[str, Any],
    save_prompt_to: Path = None
) -> int:
    from prompts import build_user_prompt

    schema = metric_schema()
    examples_block = examples_from_dicts(topic, metric, V)
    sys_prompt = system_prompt()
    user_prompt = build_user_prompt(metric=metric, topic=topic, report_md=report_md, examples_block=examples_block)

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user",   "content": user_prompt},
    ]

    if save_prompt_to is not None:
        save_prompt_to.parent.mkdir(parents=True, exist_ok=True)
        save_payload = {
            "system": sys_prompt,
            "user": user_prompt,
            "metric": metric,
            "topic": topic,
            "model": model_used,
        }
        save_prompt_to.write_text(json.dumps(save_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    resp = call_llm(messages, response_format=schema)
    msg = resp.choices[0].message
    parsed = msg.parsed if hasattr(msg, "parsed") and msg.parsed else json.loads(msg.content)
    score = int(parsed.get("score", 0))
    return max(0, min(100, score))

