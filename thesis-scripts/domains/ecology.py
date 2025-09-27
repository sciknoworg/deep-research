# thesis-scripts/domains/ecology.py
# Ecology-specific analyzer: unique-hit coverage per dictionary + linear scoring.
# Important: InfoDensity uses ONLY the terminal Sources/References section
# (counted upstream in BaseResearchAnalyzer); we do not scan inline URLs.

from __future__ import annotations
import re
from typing import List, Dict

import numpy as np

from base import BaseResearchAnalyzer, ScoringConfig
from utils import load_domain_vocab  # expected to load ecology_dictionaries.json


# ------------------------- Tiny matching utilities ----------------------------

def _normalize_separators(s: str) -> str:
    """Replace common separators with spaces and collapse whitespace."""
    s = re.sub(r'[-–—_/]+', ' ', s)
    return re.sub(r'\s+', ' ', s.strip().lower())


def unique_phrase_hits(text: str, vocab_terms: List[str]) -> int:
    """
    Count unique presence (0/1 per vocab term/phrase) with tolerant matching:
      - case-insensitive
      - hyphen/underscore/slash tolerant
      - flexible whitespace between tokens (multi-word phrases)
      - simple plural tolerance on the last token (s|es)
    """
    if not vocab_terms:
        return 0
    t_norm = _normalize_separators(text)
    hits, seen = 0, set()

    for raw in vocab_terms:
        term = _normalize_separators(str(raw))
        if not term or term in seen:
            continue
        seen.add(term)

        tokens = [re.escape(tok) for tok in term.split()]
        if not tokens:
            continue
        core = tokens[0] if len(tokens) == 1 else r'\s+'.join(tokens[:-1]) + r'\s+' + tokens[-1]
        pattern = rf'(?<![A-Za-z0-9]){core}(?:s|es)?(?![A-Za-z0-9])'
        if re.search(pattern, t_norm, flags=re.IGNORECASE):
            hits += 1
    return hits


def unique_token_presence(text_lower: str, terms: List[str]) -> int:
    """Count unique presence for a short token list using fast substring checks."""
    if not terms:
        return 0
    tl = text_lower.lower()
    uniq = {t.strip().lower() for t in terms if t and t.strip()}
    return sum(1 for tok in uniq if tok in tl)


def ratio_coverage(hits: int, vocab_len: int) -> float:
    """Convert unique-hit count to a coverage ratio in [0,1]."""
    denom = max(1, int(vocab_len))
    return min(max(0.0, float(hits)) / denom, 1.0)


# ------------------------------ Ecology analyzer ------------------------------

class EcologyAnalyzer(BaseResearchAnalyzer):
    """
    Ecology domain: ratio-coverage scores with arithmetic-only aggregation.
    - All coverage values are unique-hit ratios against actual dictionary sizes.
    - InfoDensity is derived upstream from the *terminal Sources section only*.
    - Temporal precision is computed in the base class and used here.
    """

    def __init__(self, config: ScoringConfig | None = None):
        super().__init__(config=config)

    # ----- vocab -----
    def build_vocab(self) -> dict:
        """Load ecology dictionaries via utils.load_domain_vocab()."""
        return load_domain_vocab()

    # ----- raw signals -----
    def domain_extract_metrics(self, content: str, metrics: dict):
        """
        Extract raw signals for dimension scoring. All dictionary-based signals
        use unique-hit counts to emphasize coverage rather than repetition.
        """
        V = self.vocab
        cl = content.lower()

        # Mechanistic & causal
        metrics['mechanistic_hits']   = unique_phrase_hits(content, V.get('mechanistic_terms', []))
        metrics['causal_hits']        = unique_phrase_hits(content, V.get('causal_terms', []))

        # Breadth dictionaries
        metrics['region_hits']        = unique_phrase_hits(content, V.get('regions', []))
        metrics['intervention_hits']  = unique_phrase_hits(content, V.get('interventions', []))
        metrics['diversity_hits']     = unique_phrase_hits(content, V.get('diversity_dimensions', []))
        metrics['services_hits']      = unique_phrase_hits(content, V.get('ecosystem_services', []))
        metrics['scales_hits']        = unique_phrase_hits(content, V.get('scale_terms', []))

        # Temporal precision (computed in base class)
        metrics['temporal_precision'] = float(self._temporal_precision(content))

        # Rigor (no citation counts): stats lexicon + uncertainty tokens
        metrics['stats_hits'] = unique_phrase_hits(content, V.get('stats_terms', []))
        metrics['uncertainty_hits'] = unique_token_presence(
            cl, V.get('uncertainty_terms', ['uncertain','unclear','unknown'])
        )

        # Innovation: speculative markers, innovation lexicon, and explicit gaps
        metrics['gap_hits'] = unique_token_presence(
            cl, V.get('gap_terms', ['research gap','knowledge gap','data gap'])
        )
        metrics['speculative_hits'] = unique_token_presence(
            cl, V.get('speculative_terms', ['speculative','hypothetical','flagged'])
        )
        metrics['innovation_term_hits'] = unique_phrase_hits(content, V.get('innovation_terms', []))

        # Domain alignment
        metrics['conservation_hits'] = unique_phrase_hits(content, V.get('conservation_terms', []))
        metrics['climate_hits']      = unique_phrase_hits(content, V.get('climate_terms', []))
        metrics['complexity_hits']   = unique_phrase_hits(content, V.get('complexity_terms', []))

    # ----- helpers -----
    def _cov(self, hits: int, vocab_key: str) -> float:
        vocab_len = len(self.vocab.get(vocab_key, []))
        return ratio_coverage(hits, vocab_len or 1)

    def _score_depth(self, m: dict) -> float:
        mech = self._cov(m.get('mechanistic_hits', 0), 'mechanistic_terms')
        caus = self._cov(m.get('causal_hits', 0), 'causal_terms')
        temp = float(m.get('temporal_precision', 0.0))
        m['depth_mechanistic_cov'] = mech
        m['depth_causal_cov'] = caus
        m['depth_temp_precision'] = temp
        return float(np.average([mech, caus, temp], weights=[0.4, 0.3, 0.3]))

    def _score_breadth(self, m: dict) -> float:
        region = self._cov(m.get('region_hits', 0), 'regions')
        interv = self._cov(m.get('intervention_hits', 0), 'interventions')
        divers = self._cov(m.get('diversity_hits', 0), 'diversity_dimensions')
        serv   = self._cov(m.get('services_hits', 0), 'ecosystem_services')
        scale  = self._cov(m.get('scales_hits', 0), 'scale_terms')
        m['breadth_regions_cov'] = region
        m['breadth_interventions_cov'] = interv
        m['breadth_diversity_cov'] = divers
        m['breadth_services_cov'] = serv
        m['breadth_scales_cov'] = scale
        return float(np.average([region, interv, divers, serv, scale],
                                weights=[0.25, 0.25, 0.25, 0.15, 0.10]))

    def _score_rigor(self, m: dict) -> float:
        stats = self._cov(m.get('stats_hits', 0), 'stats_terms')
        unc   = ratio_coverage(
            m.get('uncertainty_hits', 0),
            len(self.vocab.get('uncertainty_terms', ['uncertain','unclear','unknown'])) or 1
        )
        m['rigor_stats_cov'] = stats
        m['rigor_uncertainty_cov'] = unc
        return float(np.average([stats, unc], weights=[2/3, 1/3]))

    def _score_innovation(self, m: dict) -> float:
        spec  = min(m.get('speculative_hits', 0) / 3.0, 1.0)
        iterm = self._cov(m.get('innovation_term_hits', 0), 'innovation_terms')
        gaps  = min(m.get('gap_hits', 0) / 3.0, 1.0)
        m['innovation_speculative'] = spec
        m['innovation_terms_cov']   = iterm
        m['innovation_gaps']        = gaps
        return float(np.average([spec, iterm, gaps], weights=[0.4, 0.3, 0.3]))

    def _score_info_density(self, m: dict) -> float:
        """Normalize raw sources_per_1k to [0,1] using a simple cap."""
        cap = max(1e-9, self.config.density_per_k_cap)
        return min(float(m.get('sources_per_1k', 0.0)) / cap, 1.0)

    def _score_ecological(self, m: dict) -> float:
        cons = self._cov(m.get('conservation_hits', 0), 'conservation_terms')
        clim = self._cov(m.get('climate_hits', 0),      'climate_terms')
        comp = self._cov(m.get('complexity_hits', 0),   'complexity_terms')
        m['ecology_conservation_cov'] = cons
        m['ecology_climate_cov']      = clim
        m['ecology_complexity_cov']   = comp
        return float(np.average([cons, clim, comp], weights=[0.4, 0.3, 0.3]))

    # ----- scoring entrypoint -----
    def domain_calculate_quality_scores(self, m: dict):
        """
        Compute six dimension scores and the overall linear aggregate.
        All scores are clipped to [0,1] for plot compatibility.
        """
        w = self.weights

        depth = self._score_depth(m)
        breadth = self._score_breadth(m)
        rigor = self._score_rigor(m)
        innovation = self._score_innovation(m)
        info_density = self._score_info_density(m)
        ecological = self._score_ecological(m)

        overall = (
            depth*w.depth + breadth*w.breadth + rigor*w.rigor + innovation*w.innovation +
            ecological*w.domain_specific + info_density*w.info_density
        )

        clip = lambda x: float(np.clip(x, 0.0, 1.0))
        m.update({
            'depth_score': clip(depth),
            'breadth_score': clip(breadth),
            'rigor_score': clip(rigor),
            'innovation_score': clip(innovation),
            'ecological_relevance': clip(ecological),
            'info_density': clip(info_density),
            'overall_quality': clip(overall),
        })
