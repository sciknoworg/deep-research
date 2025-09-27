# thesis-scripts/base.py
# Shared pipeline (loading, metrics extraction, aggregation, publication plots)
# Domain analyzers subclass this and implement domain-specific pieces only.

from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# Unified plotting helpers (we keep all plotting in a single module: plots.py)
from plots import (
    create_question_dashboard,
    save_scaling_heatmaps,
    create_parameter_effects_plot,
    create_quality_dimensions_plot,
    create_overall_quality_analysis,
)


# ------------------------------- Utilities -----------------------------------

def safe_div(num: float, den: float, default: float = 0.0) -> float:
    """Safe division that returns `default` when denominator ≤ 0."""
    return (num / den) if den > 0 else default


# ------------------------------- Configs -------------------------------------

@dataclass
class QualityWeights:
    """
    Linear weights for the six dimensions (kept compatible with older code).
    `taxonomic_or_specificity` is unused for Ecology but retained for API stability.
    """
    depth: float = 0.26
    breadth: float = 0.24
    rigor: float = 0.16
    innovation: float = 0.16
    domain_specific: float = 0.12
    info_density: float = 0.04
    taxonomic_or_specificity: float = 0.02  # unused in Ecology


@dataclass
class ScoringConfig:
    """
    Minimal knobs for the arithmetic-only scorer.
    - density_per_k_cap: sources-per-1k threshold at which InfoDensity saturates to 1.0
    - weights: QualityWeights used in the overall linear aggregate
    Legacy fields are kept for backward compatibility; they are not used here.
    """
    density_per_k_cap: float = 50.0
    weights: QualityWeights = QualityWeights()

    # Legacy / back-compat (unused)
    depth_agg: str = "arithmetic"
    breadth_agg: str = "arithmetic"
    density_tau: float = 14.0
    citations_tau: float = 12.0
    stats_rigor_tau: float = 4.0
    uncertainty_tau: float = 3.0


# ------------------------------ Base Analyzer --------------------------------

class BaseResearchAnalyzer:
    """
    Shared end-to-end flow:
      1) load_document(filename, text)    — parse depth/breadth from filename.
      2) extract_metrics()                — counts + domain raw signals.
      3) domain_calculate_quality_scores  — dimension scores + overall.
      4) create_question_dashboard        — compact per-question panel (no empty plots).
      5) create_common_publication_plots  — standardized figures (heatmaps, effects, etc).
    """

    def __init__(self, config: Optional[ScoringConfig] = None):
        self.config = config if config is not None else ScoringConfig()
        self.vocab = self.build_vocab()
        self.weights = self.config.weights
        self.documents: Dict[str, dict] = {}
        self.metrics: Dict[str, dict] = {}

    # ----- Subclass API -----
    def build_vocab(self) -> dict:
        raise NotImplementedError

    def domain_weights(self) -> QualityWeights:
        return self.weights

    def domain_extract_metrics(self, content: str, metrics: dict):
        raise NotImplementedError

    def domain_calculate_quality_scores(self, metrics: dict):
        raise NotImplementedError

    def domain_publication_plots(self, statistics_file: str, all_results: Dict[str, pd.DataFrame], figures_dir: str):
        # Default: the common publication bundle
        self.create_common_publication_plots(statistics_file, all_results, figures_dir)

    # ----- I/O & Helpers -----
    def load_document(self, filename: str, content: str) -> None:
        """
        Attach a report to the batch. We expect filenames to end in "..._dX_bY.md".
        """
        m = re.search(r'd(\d+)_b(\d+)', filename)
        if not m:
            return
        depth, breadth = int(m.group(1)), int(m.group(2))
        key = f"d{depth}_b{breadth}"
        self.documents[key] = dict(filename=filename, depth=depth, breadth=breadth, content=content)

    # ---- Source counting: ONLY in the terminal Sources/References section ----
    def _find_sources_section(self, content: str) -> str:
        """
        Return the substring that belongs to the trailing Sources/References section.
        Header match is case-insensitive and supports levels '#..######'.
        """
        header_re = re.compile(r'(?im)^\s*#{1,6}\s*(sources|references|bibliography|works\s+cited)\s*$')
        m = header_re.search(content)
        if not m:
            return ""
        start = m.end()
        next_header_re = re.compile(r'(?im)^\s*#{1,6}\s+\S+.*$')
        m2 = next_header_re.search(content, pos=start)
        end = m2.start() if m2 else len(content)
        return content[start:end]

    def _extract_source_count(self, content: str) -> int:
        """
        Count *unique* sources only from the terminal Sources/References/Bibliography block.
        We support:
          - Markdown link targets: [text](https://...)
          - Bare URLs:             https://...
          - DOIs:                  10.XXXX/... (normalized to https://doi.org/<doi>)
        """
        section = self._find_sources_section(content)
        if not section:
            return 0

        urls = set()

        # 1) Markdown targets: (...)[(URL)]
        for u in re.findall(r'\((https?://[^\s)]+)\)', section):
            urls.add(u.strip().rstrip('.,;:)'))

        # 2) Bare URLs
        for u in re.findall(r'https?://[^\s)]+', section):
            urls.add(u.strip().rstrip('.,;:)'))

        # 3) DOIs normalized to doi.org
        doi_pat = re.compile(r'\b10\.\d{4,9}/\S+\b', re.IGNORECASE)
        for doi in doi_pat.findall(section):
            doi_clean = doi.strip().rstrip('.,;:)')
            urls.add(f'https://doi.org/{doi_clean}')

        return len(urls)

    def _temporal_precision(self, content: str) -> float:
        """
        Temporal precision: specific / (specific + vague)
        - Specific: absolute dates, numeric durations, month+day, year ranges.
        - Vague: vague temporal adjectives/adverbs (e.g., "long-term", "historically").
        """
        specific_patterns = [
            r'\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*(?:yr|year|month|week|day|hour|decade|century)',
            r'(?:within|after|before)\s+\d+\s+(?:yr|year|month|week|day)',
            r'(?:every|each)\s+\d+\s+(?:yr|year|month|week|day)',
            r'\d{4}(?:\s*[-–]\s*\d{4})?(?:\s+(?:AD|BC|CE|BCE))?',
            r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}',
        ]
        vague_terms = [
            'recently','historically','traditionally','formerly','previously',
            'short-term','long-term','medium-term','near-term',
            'early','late','mid-','recent','ancient','modern',
            'soon','eventually','ultimately','initially','finally',
            'temporary','permanent','occasional','frequent','rare'
        ]
        cl = content.lower()
        specific = sum(len(re.findall(p, cl)) for p in specific_patterns)
        vague = sum(cl.count(t) for t in vague_terms)
        return safe_div(specific, specific + vague, default=0.0)

    # ----- Pipeline -----
    def extract_metrics(self) -> None:
        """
        Build self.metrics for each loaded document (keyed by 'dX_bY').
        """
        for key, doc in self.documents.items():
            content = doc['content']
            word_count = len(content.split())
            source_count = self._extract_source_count(content)

            metrics = dict(
                word_count=word_count,
                char_count=len(content),
                source_count=source_count,
                section_count=len(content.split('\n## ')),
                # raw display metric (can exceed 1.0)
                sources_per_1k=safe_div(source_count, (word_count / 1000.0), default=0.0),
            )

            # Domain hooks (unique-hit coverages, temporal, etc.)
            self.domain_extract_metrics(content, metrics)
            self.metrics[key] = metrics

    def analyze_multiple_questions(self, report_dir: str, question_numbers: List[str], output_dir: str) -> dict:
        """
        Load all files for each question that match "*_d<b>_b<d>.md", compute metrics
        and scores, save a per-question dashboard, and return a dict of DataFrames.
        """
        os.makedirs(output_dir, exist_ok=True)
        all_results: Dict[str, pd.DataFrame] = {}

        for q in question_numbers:
            self.documents.clear(); self.metrics.clear()
            loaded = 0

            # Accept any filename that starts with "<Q>_" and ends in "_dX_bY.md"
            for fname in os.listdir(report_dir):
                if not fname.startswith(f"{q}_"):
                    continue
                if re.search(r'd\d+_b\d+\.md$', fname):
                    with open(os.path.join(report_dir, fname), 'r', encoding='utf-8') as f:
                        self.load_document(fname, f.read())
                    loaded += 1

            if not loaded:
                print(f"[WARN] No files found for question {q} in {report_dir}")
                continue

            # raw → metrics → scores
            self.extract_metrics()
            for k in list(self.metrics.keys()):
                self.domain_calculate_quality_scores(self.metrics[k])

            # Per-question dashboard (no empty subplots)
            df = pd.DataFrame(self.metrics).T
            fig = create_question_dashboard(df)
            os.makedirs(os.path.join(output_dir, "plot_per_question"), exist_ok=True)
            fig.savefig(os.path.join(output_dir, f"plot_per_question/question_{q}_analysis.png"),
                        dpi=300, bbox_inches='tight')
            import matplotlib.pyplot as plt
            plt.close(fig)

            # Attach config + question for aggregation
            df['config'] = [f"d{self.documents[k]['depth']}_b{self.documents[k]['breadth']}" for k in df.index]
            df['question'] = q
            all_results[q] = df
            print(f"[OK] Analyzed question {q} with {loaded} documents")

        if all_results:
            self._save_summary(all_results, output_dir)
        return all_results

    @staticmethod
    def _save_summary(all_results: Dict[str, pd.DataFrame], output_dir: str) -> None:
        """
        Save a compact CSV with per-configuration statistics across all questions.
        This file is the single source of truth for figure helpers (if needed).
        """
        combined = pd.concat(all_results.values(), ignore_index=True)

        # Clip score-like columns to [0,1] for consistent plotting ranges
        score_cols = [
            'depth_score','breadth_score','rigor_score','innovation_score',
            'ecological_relevance','info_density','overall_quality',
            'breadth_regions_cov','breadth_interventions_cov','breadth_diversity_cov',
            'breadth_services_cov','breadth_scales_cov',
            'depth_mechanistic_cov','depth_causal_cov','depth_temp_precision',
            'rigor_stats_cov','rigor_uncertainty_cov'
        ]
        for c in score_cols:
            if c in combined.columns:
                combined[c] = combined[c].astype(float).clip(0.0, 1.0)

        # Aggregate mean/std/min/max per numeric column by config
        agg_spec = {
            c: ['mean','std','min','max']
            for c in combined.columns
            if c not in ('config','question') and np.issubdtype(combined[c].dtype, np.number)
        }
        summary = combined.groupby('config').agg(agg_spec).round(3)
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        summary = pd.concat([combined.groupby('config').size().rename('n_docs'), summary], axis=1)

        os.makedirs(output_dir, exist_ok=True)
        summary.to_csv(os.path.join(output_dir, "comprehensive_summary_statistics.csv"))

    # ----- Publication figures -----
    def create_common_publication_plots(self, statistics_file: str, all_results: Dict[str, pd.DataFrame], figures_dir: str):
        os.makedirs(figures_dir, exist_ok=True)
        # (1) Scaling heatmaps (words, sources, sources/1k)
        save_scaling_heatmaps(all_results, figures_dir)
        # (2) Parameter effects + (compat) optimization figure
        create_parameter_effects_plot(all_results, figures_dir)
        # (3) Dimension bars
        create_quality_dimensions_plot(all_results, figures_dir)
        # (4) 3×3 overview (no empty axes; Avg Research Quality scaled to 0–4)
        create_overall_quality_analysis(all_results, figures_dir)
