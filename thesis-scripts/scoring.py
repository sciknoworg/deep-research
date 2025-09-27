from dataclasses import dataclass
from typing import Dict
import numpy as np

__all__ = [
    "QualityWeights",
    "ScoringConfig",
    "safe_div",
    "ratio_coverage",
    "score_depth",
    "score_breadth",
    "score_rigor",
    "score_innovation",
    "score_domain_triple",
    "score_info_density",
    "linear_overall",
]

@dataclass
class QualityWeights:
    """Linear weights for aggregating the six dimensions."""
    depth: float = 0.26
    breadth: float = 0.24
    rigor: float = 0.16
    innovation: float = 0.16
    domain_specific: float = 0.12
    info_density: float = 0.04
    # kept for API stability (unused here)
    taxonomic_or_specificity: float = 0.02


@dataclass
class ScoringConfig:
    """
    Minimal knobs for the arithmetic-only scorer.

    density_per_k_cap : sources per 1k at which InfoDensity saturates to 1.0.
    """
    density_per_k_cap: float = 50.0
    weights: QualityWeights = QualityWeights()


def safe_div(num: float, den: float, default: float = 0.0) -> float:
    return (num / den) if den > 0 else default


def ratio_coverage(hits: int, vocab_len: int) -> float:
    denom = max(1, int(vocab_len))
    val = float(hits) / denom
    return float(min(max(0.0, val), 1.0))


def score_depth(mech: float, caus: float, temp: float) -> float:
    return float(np.average([mech, caus, temp], weights=[0.4, 0.3, 0.3]))


def score_breadth(reg: float, inter: float, div: float, serv: float, scale: float) -> float:
    return float(np.average([reg, inter, div, serv, scale],
                            weights=[0.25, 0.25, 0.25, 0.15, 0.10]))


def score_rigor(stats: float, unc: float) -> float:
    return float(np.average([stats, unc], weights=[2/3, 1/3]))


def score_innovation(spec: float, novelty: float, gaps: float) -> float:
    return float(np.average([spec, novelty, gaps], weights=[0.4, 0.3, 0.3]))


def score_domain_triple(a: float, b: float, c: float) -> float:
    # used for (conservation, climate, complexity) or any domain triple
    return float(np.average([a, b, c], weights=[0.4, 0.3, 0.3]))


def score_info_density(sources_per_1k: float, cap: float) -> float:
    cap = max(1e-9, float(cap))
    return float(min(max(0.0, sources_per_1k / cap), 1.0))


def linear_overall(scores: Dict[str, float], w: QualityWeights) -> float:
    """
    scores keys: depth, breadth, rigor, innovation, domain_specific, info_density
    """
    overall = (
        scores.get("depth", 0.0) * w.depth +
        scores.get("breadth", 0.0) * w.breadth +
        scores.get("rigor", 0.0) * w.rigor +
        scores.get("innovation", 0.0) * w.innovation +
        scores.get("domain_specific", 0.0) * w.domain_specific +
        scores.get("info_density", 0.0) * w.info_density
    )
    return float(np.clip(overall, 0.0, 1.0))
