# thesis-scripts/domains/nlp.py
# Minimal NLP analyzer placeholder to keep the pipeline shape identical to Ecology.
# Extend later with NLP dictionaries and scoring rules using the same pattern.

from __future__ import annotations
import json
import os

from base import BaseResearchAnalyzer, ScoringConfig


def _default_vocab_path(domain_name: str) -> str:
    """Try a few standard locations for '<domain>_dictionaries.json'."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, '..'))
    cwd = os.getcwd()
    fname = f'{domain_name}_dictionaries.json'
    for p in [
        os.path.join(repo_root, 'data', 'vocab', fname),
        os.path.join(repo_root, 'vocab', fname),
        os.path.join(cwd, 'data', 'vocab', fname),
        os.path.join(cwd, 'vocab', fname),
        os.path.join(cwd, fname),
    ]:
        if os.path.exists(p):
            return p
    return os.path.join(repo_root, 'vocab', fname)


class NLPAnalyzer(BaseResearchAnalyzer):
    def __init__(self, config: ScoringConfig | None = None):
        super().__init__(config=config)

    def build_vocab(self) -> dict:
        path = _default_vocab_path('nlp')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    # For now we keep metrics minimal so plots still render; fill in later.
    def domain_extract_metrics(self, content: str, metrics: dict):
        metrics['temporal_precision'] = 0.0

    def domain_calculate_quality_scores(self, m: dict):
        for k in ['depth_score','breadth_score','rigor_score','innovation_score',
                  'ecological_relevance','info_density','overall_quality']:
            m[k] = 0.0
