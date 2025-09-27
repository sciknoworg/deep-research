# research_analyzer.py
#
# Goal
# ----
# Provide a *simple and transparent* quality score for long-form research reports.
# The score is deliberately arithmetic (no harmonic means) and uses *unique-hit*
# coverage against domain dictionaries. Information Density is computed solely from
# the terminal Sources/References section (not inline links) to reflect curated
# evidence integration.
#
# Design in one page
# ------------------
# We compute six dimension scores in [0, 1], then combine them linearly:
#
#   Depth        = 0.4·mechanistic_cov + 0.3·causal_cov + 0.3·temporal_precision
#   Breadth      = 0.25·regions_cov + 0.25·interventions_cov + 0.25·diversity_cov
#                  + 0.15·services_cov + 0.10·scales_cov
#   Rigor        = 2/3·stats_cov + 1/3·uncertainty_cov
#   Innovation   = 0.4·speculative + 0.3·innovation_terms_cov + 0.3·gap_signal
#   Ecological   = 0.4·conservation_cov + 0.3·climate_cov + 0.3·complexity_cov
#   InfoDensity  = min( (sources_per_1k) / CAP , 1.0 )       (CAP = density_per_k_cap)
#
# Where each “_cov” is *ratio coverage* (unique hits divided by the length of the
# corresponding dictionary list). Unique-hit means: a dictionary entry contributes
# at most 1 to the hit count, regardless of frequency in the text.
#
# Key choices
# -----------
# - Arithmetic aggregation only (no harmonic or geometric means).
# - Count *unique* matches per dictionary item to avoid repetition gaming.
# - Separate the *raw* display metric `sources_per_1k` (can be > 1) from the
#   *normalized* `info_density` score (always in [0,1]).
# - Source counting is restricted to the terminal references section,
#   including Markdown links, bare URLs, and DOIs (normalized to doi.org).
#
# Architecture (numbered workflow overview)
# -----------------------------------------
# [0]  Imports, utilities, configs (shared).
# [1]  BaseResearchAnalyzer: batch orchestration (load → extract → score → visualize → summarize).
#      [1.1]  load_document(...)          — attach file, parse d/b tag
#      [1.2]  extract_metrics(...)        — common counts + sources_per_1k + call domain_extract_metrics
#      [1.3]  domain_calculate_quality_scores(...) (implemented in subclass)
#      [1.4]  _default_visualizations(...) per-question 3×3 dashboard
#      [1.5]  _save_summary(...)          — CSV for external plots
#      [1.6]  create_common_publication_plots(...) — call unchanged plot helpers
# [2]  EcologyAnalyzer: domain vocab, domain_extract_metrics (unique hits), scoring functions.
# [3]  NLPAnalyzer: mirrored implementation (comparable dimensions & weights).
# [4]  get_analyzer(...) factory.

import os
import re
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import (
    depth_breadth_filename_patterns,  # e.g. ["d1_b1", "d1_b4", "d4_b1", "d4_b4"]
    model_and_search_pattern,         # model/search tag embedded in filenames (e.g. "o3_orkg")
    load_domain_vocab,                # loads ecology_dictionaries.json
    topic                             # "ecology" | "nlp"
)

# External plotting helpers (left exactly as you had them)
from main_scaling_plot import create_main_scaling_plot
from optimization_analysis_plot import create_optimization_analysis_plot
from overall_quality_analysis import create_overall_quality_analysis
from parameter_effects_plot import create_parameter_effects_plot
from quality_dimensions_plot import create_quality_dimensions_plot

plt.style.use('seaborn-v0_8-whitegrid')


# ──────────────────────────────────────────────────────────────────────────────
# [0.1] Utility functions (matching, normalization, safe math)
# ──────────────────────────────────────────────────────────────────────────────

def _normalize_separators(s: str) -> str:
    """Normalize -, _, /, long dashes to spaces; collapse whitespace; lowercase."""
    s = re.sub(r'[-–—_/]+', ' ', s)
    return re.sub(r'\s+', ' ', s.strip().lower())


def unique_phrase_hits(text: str, vocab_terms: List[str]) -> int:
    """
    Unique-hit matching for phrases (0/1 per vocab entry).
    Rules: case-insensitive; separator-tolerant; flexible spaces; optional plural on last token.
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
    """Unique presence for short token lists via simple substring tests."""
    if not terms:
        return 0
    tl = text_lower.lower()
    uniq = {t.strip().lower() for t in terms if t and t.strip()}
    return sum(1 for tok in uniq if tok in tl)


def safe_div(num: float, den: float, default: float = 0.0) -> float:
    """Safe division; returns `default` when denominator ≤ 0."""
    return (num / den) if den > 0 else default


def ratio_coverage(hits: int, vocab_len: int) -> float:
    """Coverage = unique hits / dictionary size, clamped to [0,1]."""
    denom = max(1, int(vocab_len))
    return min(max(0.0, float(hits)) / denom, 1.0)


def _default_vocab_path(domain_name: str) -> str:
    """Fallback locator for '<domain>_dictionaries.json' (used by NLPAnalyzer only)."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, '..'))
    cwd = os.getcwd()
    fname = f'{domain_name}_dictionaries.json'
    for p in [
        os.path.join(here, 'data', 'vocab', fname),
        os.path.join(repo_root, 'data', 'vocab', fname),
        os.path.join(here, 'vocab', fname),
        os.path.join(repo_root, 'vocab', fname),
        os.path.join(cwd, 'data', 'vocab', fname),
        os.path.join(cwd, 'vocab', fname),
        os.path.join(cwd, fname),
    ]:
        if os.path.exists(p):
            return p
    return os.path.join(repo_root, 'vocab', fname)


# ──────────────────────────────────────────────────────────────────────────────
# [0.2] Config objects (weights & scoring settings)
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class QualityWeights:
    """
    Weights for the six dimensions (sum ~ 1.0).
    """
    depth: float = 0.26
    breadth: float = 0.24
    rigor: float = 0.16
    innovation: float = 0.16
    domain_specific: float = 0.12
    info_density: float = 0.06
    taxonomic_or_specificity: float = 0.00  # kept for API stability


@dataclass
class ScoringConfig:
    """
    Minimal knobs for the arithmetic-only scorer.
    density_per_k_cap: cap for InfoDensity score (sources per 1k → [0,1]).
    """
    density_per_k_cap: float = 50.0
    weights: QualityWeights = QualityWeights()

    # Back-compat (unused here)
    depth_agg: str = "arithmetic"
    breadth_agg: str = "arithmetic"
    density_tau: float = 14.0
    citations_tau: float = 12.0
    stats_rigor_tau: float = 4.0
    uncertainty_tau: float = 3.0


# ──────────────────────────────────────────────────────────────────────────────
# [1] Base class: batch orchestration
# ──────────────────────────────────────────────────────────────────────────────

class BaseResearchAnalyzer:
    """
    Shared I/O & pipeline for any domain.

    Lifecycle:
      analyze_multiple_questions(...)
        ├─ [1.1] load_document(...) per file
        ├─ [1.2] extract_metrics() → common counts & sources_per_1k → [2] domain_extract_metrics(...)
        ├─ [1.3] domain_calculate_quality_scores(...) per doc
        ├─ [1.4] _default_visualizations(...) (per-question 3×3)
        ├─ [1.5] _save_summary(...) CSV for external plotting
        └─ [1.6] create_common_publication_plots(...)
    """

    def __init__(self, config: Optional[ScoringConfig] = None):
        self.config = config if config is not None else ScoringConfig()
        self.vocab = self.build_vocab()
        self.weights = self.config.weights or self.domain_weights()
        self.documents: Dict[str, dict] = {}
        self.metrics: Dict[str, dict] = {}

    # ----- subclass API -----
    def build_vocab(self) -> dict:
        raise NotImplementedError

    def domain_weights(self) -> QualityWeights:
        return QualityWeights()

    def domain_extract_metrics(self, content: str, metrics: dict):
        raise NotImplementedError

    def domain_calculate_quality_scores(self, metrics: dict):
        raise NotImplementedError

    def domain_publication_plots(self, statistics_file, all_results, figures_dir):
        """Default: call common bundle; subclasses may override."""
        self.create_common_publication_plots(statistics_file, all_results, figures_dir)

    # ----- shared helpers -----
    def load_document(self, filename: str, content: str) -> None:
        # [1.1] Attach file; parse d/b tags from filename "..._d<depth>_b<breadth>.md"
        m = re.search(r'd(\d+)_b(\d+)', filename)
        if not m:
            return
        depth, breadth = int(m.group(1)), int(m.group(2))
        key = f"d{depth}_b{breadth}"
        self.documents[key] = dict(filename=filename, depth=depth, breadth=breadth, content=content)

    # ----- sources counting restricted to terminal references section -----

    def _find_sources_section(self, content: str) -> str:
        """Locate the LAST '## Sources/References/Bibliography/Works cited' section."""
        header_re = re.compile(r'(?im)^\s*#{1,6}\s*(sources|references|bibliography|works\s+cited)\s*$')
        matches = list(header_re.finditer(content))
        if not matches:
            return ""
        start = matches[-1].end()
        next_header_re = re.compile(r'(?im)^\s*#{1,6}\s+\S+.*$')
        m2 = next_header_re.search(content, pos=start)
        end = m2.start() if m2 else len(content)
        return content[start:end]

    def _normalize_url(self, u: str) -> str:
        """Normalize and lightly sanitize URLs/DOIs for deduplication."""
        u = u.strip().rstrip(').,;:]')
        if re.match(r'(?i)^doi:\s*10\.\d{4,9}/\S+$', u):
            u = re.sub(r'(?i)^doi:\s*', 'https://doi.org/', u)
        elif re.match(r'^10\.\d{4,9}/\S+$', u):
            u = 'https://doi.org/' + u
        u = re.sub(r'^https?://(www\.)?', 'https://', u)
        u = re.sub(r'(\?|&)utm_[^=&]+=[^&]+', '', u)
        u = re.sub(r'(\?|&)ref=[^&]+', '', u)
        return u

    def _extract_source_count(self, content: str) -> int:
        """
        Count unique sources **only** from the terminal references section.
        Supports: Markdown link targets, bare URLs, and DOIs.
        """
        section = self._find_sources_section(content)
        if not section:
            return 0
        urls = set()
        for u in re.findall(r'\((https?://[^\s)]+)\)', section):
            urls.add(self._normalize_url(u))
        for u in re.findall(r'https?://[^\s)]+', section):
            urls.add(self._normalize_url(u))
        for doi in re.findall(r'(?i)\b(?:doi:\s*)?10\.\d{4,9}/\S+\b', section):
            urls.add(self._normalize_url(doi))
        return len(urls)

    def _temporal_precision(self, content: str) -> float:
        """Temporal precision = specific / (specific + vague)."""
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

    # ----- pipeline -----
    def extract_metrics(self) -> None:
        """
        [1.2] For each loaded doc, compute common counts and sources_per_1k,
              then delegate to [2] domain_extract_metrics for dictionary hits.
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
                sources_per_1k=safe_div(source_count, (word_count / 1000.0), default=0.0),
            )
            self.domain_extract_metrics(content, metrics)  # [2]
            self.metrics[key] = metrics

    def analyze_multiple_questions(self, report_dir: str, question_numbers: List[str], output_dir: str) -> dict:
        """
        [1] Main entrypoint: discover files, extract metrics, score, visualize, summarize.
        """
        os.makedirs(output_dir, exist_ok=True)
        all_results: Dict[str, pd.DataFrame] = {}

        for q in question_numbers:
            self.documents.clear(); self.metrics.clear()
            loaded = 0
            for cfg in depth_breadth_filename_patterns:
                fname = f"{q}_{model_and_search_pattern}_{cfg}.md"
                try:
                    with open(os.path.join(report_dir, fname), 'r', encoding='utf-8') as f:
                        self.load_document(fname, f.read())  # [1.1]
                    loaded += 1
                except FileNotFoundError:
                    print(f"[WARN] File not found: {fname}")
            if not loaded:
                continue

            self.extract_metrics()  # [1.2]
            for k in list(self.metrics.keys()):
                self.domain_calculate_quality_scores(self.metrics[k])  # [1.3]

            os.makedirs(os.path.join(output_dir, "plot_per_question"), exist_ok=True)
            fig, df = self._default_visualizations(pd.DataFrame(self.metrics).T)  # [1.4]
            fig.savefig(os.path.join(output_dir, f"plot_per_question/question_{q}_analysis.png"),
                        dpi=300, bbox_inches='tight')
            plt.close(fig)

            df['config'] = [f"d{self.documents[k]['depth']}_b{self.documents[k]['breadth']}" for k in df.index]
            df['question'] = q
            all_results[q] = df
            print(f"[OK] Analyzed question {q} with {loaded} documents")

        if all_results:
            self._save_summary(all_results, output_dir)  # [1.5]
        return all_results

    @staticmethod
    def _save_summary(all_results: Dict[str, pd.DataFrame], output_dir: str) -> None:
        """
        [1.5] Build compact CSV with per-config stats; clamp all score-like cols to [0,1].
        """
        combined = pd.concat(all_results.values(), ignore_index=True)

        score_cols = [
            'depth_score','breadth_score','rigor_score','innovation_score',
            'ecological_relevance','info_density','overall_quality',
            'breadth_regions_cov','breadth_interventions_cov','breadth_diversity_cov',
            'breadth_services_cov','breadth_scales_cov',
            'depth_mechanistic_cov','depth_causal_cov','depth_temp_precision',
            'rigor_stats_cov','rigor_uncertainty_cov',
            # NLP breadth/domain (will be absent in ecology; we guard below)
            'breadth_tasks_cov','breadth_datasets_cov','breadth_languages_cov',
            'breadth_metrics_cov','breadth_compute_cov',
            'nlp_repro_cov','nlp_safety_cov','nlp_compute_cov'
        ]
        for c in score_cols:
            if c in combined.columns:
                combined[c] = combined[c].astype(float).clip(0.0, 1.0)

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

    def _default_visualizations(self, df: pd.DataFrame) -> Tuple[plt.Figure, pd.DataFrame]:
        """
        [1.4] Per-question 3×3 dashboard: heatmaps (counts), bars (scores).
        Robust fallbacks ensure no empty panels.
        """
        defaults = {
            'word_count': 0, 'source_count': 0, 'sources_per_1k': 0.0,
            'overall_quality': np.nan,
            'depth_score': np.nan, 'breadth_score': np.nan,
            'rigor_score': np.nan, 'innovation_score': np.nan,
            'ecological_relevance': np.nan, 'info_density': np.nan
        }
        for k, v in defaults.items():
            if k not in df.columns:
                df[k] = v

        df['depth'] = [int(k.split('_')[0][1:]) for k in df.index]
        df['breadth'] = [int(k.split('_')[1][1:]) for k in df.index]

        fig, axes = plt.subplots(3, 3, figsize=(18, 14))
        axes = axes.flatten()

        def _heatmap_or_bar(ax, col, title, cmap, fmt_heat='.0f', fmt_bar='.0f'):
            try:
                pv = df.pivot_table(index='depth', columns='breadth', values=col, aggfunc='mean')
                if pv.size and not pv.isna().all().all() and pv.shape[0] > 0 and pv.shape[1] > 0:
                    sns.heatmap(pv, annot=True, fmt=fmt_heat, cmap=cmap, ax=ax)
                    ax.set_title(title)
                    return
            except Exception:
                pass
            series = df[col]
            if series.isna().all():
                series = series.fillna(0.0)
            ax.bar(df.index, series); ax.set_title(f"{title} (by config)")
            ax.tick_params(axis='x', rotation=45)
            for i, v in enumerate(series):
                try:
                    ax.text(i, v, format(v, fmt_bar), ha='center', va='bottom', fontsize=8)
                except Exception:
                    continue

        def _bar(ax, series, title, ylim=(0, 1), fmt='.2f', draw_max_line=None):
            y = series.fillna(0)
            ax.bar(series.index, y); ax.set_title(title)
            ax.tick_params(axis='x', rotation=45); ax.set_ylim(*ylim)
            for i, v in enumerate(y):
                ax.text(i, v, format(float(v), fmt), ha='center', va='bottom', fontsize=8)
            if draw_max_line is not None:
                ax.axhline(draw_max_line, linestyle='--', linewidth=1.2, alpha=0.7, color='k')
                ax.text(0.02, draw_max_line + (ylim[1]-ylim[0])*0.02, "max",
                        transform=ax.get_yaxis_transform(), fontsize=9, color='k')

        _heatmap_or_bar(axes[0], 'word_count', 'Word Count by Depth & Breadth', 'YlOrRd', '.0f', '.0f')
        _heatmap_or_bar(axes[1], 'source_count', 'Sources by Depth & Breadth', 'Blues', '.0f', '.0f')
        _heatmap_or_bar(axes[2], 'sources_per_1k', 'Sources per 1k by Depth & Breadth', 'Greens', '.2f', '.2f')

        idx_order = list(df.index)
        overall_scaled = (df.loc[idx_order, 'overall_quality'] * 4.0).fillna(0.0)
        _bar(axes[3], overall_scaled, 'Average Research Quality (0–4 scale)', (0, 4.1), '.2f', draw_max_line=4.0)
        _bar(axes[4], df.loc[idx_order, 'depth_score'], 'Depth Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[5], df.loc[idx_order, 'breadth_score'], 'Breadth Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[6], df.loc[idx_order, 'rigor_score'], 'Rigor Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[7], df.loc[idx_order, 'innovation_score'], 'Innovation Score (0–1)', (0, 1.0), '.2f')

        last_series = df.loc[idx_order, 'ecological_relevance']
        last_title = 'Domain Alignment (0–1)'  # works for ecology & NLP; same key used
        if last_series.isna().all():
            last_series = df.loc[idx_order, 'info_density']
            last_title = 'Information Density (0–1)'
        _bar(axes[8], last_series, last_title, (0, 1.0), '.2f')

        plt.tight_layout()
        return fig, df

    def create_common_publication_plots(self, statistics_file, all_results, figures_dir):
        """
        [1.6] Domain-agnostic bundle of standardized figures + heatmaps.
        """
        os.makedirs(figures_dir, exist_ok=True)
        df = pd.concat(all_results.values(), ignore_index=True)

        for col in ['word_count', 'source_count', 'sources_per_1k',
                    'depth_score', 'breadth_score', 'rigor_score',
                    'innovation_score', 'overall_quality']:
            if col not in df.columns:
                df[col] = 0.0
        if 'config' not in df.columns:
            df['config'] = 'd1_b1'
        df['depth'] = df['config'].str.extract(r'd(\d+)').astype(int)
        df['breadth'] = df['config'].str.extract(r'b(\d+)').astype(int)

        plt.figure(figsize=(15, 4.5))
        plt.subplot(1, 3, 1)
        sns.heatmap(df.pivot_table(index='depth', columns='breadth', values='word_count', aggfunc='mean'),
                    annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('Word Count by Depth & Breadth')

        plt.subplot(1, 3, 2)
        sns.heatmap(df.pivot_table(index='depth', columns='breadth', values='source_count', aggfunc='mean'),
                    annot=True, fmt='.0f', cmap='Blues')
        plt.title('Sources by Depth & Breadth')

        plt.subplot(1, 3, 3)
        sns.heatmap(df.pivot_table(index='depth', columns='breadth', values='sources_per_1k', aggfunc='mean'),
                    annot=True, fmt='.2f', cmap='Greens')
        plt.title('Sources per 1k by Depth & Breadth')

        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'main_scaling_effects.png'), dpi=300, bbox_inches='tight')
        plt.close()

        create_parameter_effects_plot(statistics_file, figures_dir)
        create_optimization_analysis_plot(all_results, figures_dir)
        create_quality_dimensions_plot(all_results, figures_dir)
        create_overall_quality_analysis(all_results, figures_dir)


# ──────────────────────────────────────────────────────────────────────────────
# [2] Ecology analyzer (domain vocab, signals, scoring)
# ──────────────────────────────────────────────────────────────────────────────

class EcologyAnalyzer(BaseResearchAnalyzer):
    """
    Ecology domain: ratio-coverage scores with arithmetic-only aggregation.
    - Coverage = unique-hit ratios against dictionary sizes.
    - Temporal precision from base class.
    """

    def build_vocab(self) -> dict:
        # [2.0] Load ecology dictionaries (via utils).
        return load_domain_vocab()

    def domain_extract_metrics(self, content: str, metrics: dict):
        """
        [2.1] Extract raw domain signals (unique-hit counts + temporal precision).
        """
        V = self.vocab
        cl = content.lower()

        # Coverage (unique presence per dictionary entry)
        metrics['mechanistic_hits']   = unique_phrase_hits(content, V.get('mechanistic_terms', []))
        metrics['causal_hits']        = unique_phrase_hits(content, V.get('causal_terms', []))
        metrics['region_hits']        = unique_phrase_hits(content, V.get('regions', []))
        metrics['intervention_hits']  = unique_phrase_hits(content, V.get('interventions', []))
        metrics['diversity_hits']     = unique_phrase_hits(content, V.get('diversity_dimensions', []))
        metrics['services_hits']      = unique_phrase_hits(content, V.get('ecosystem_services', []))
        metrics['scales_hits']        = unique_phrase_hits(content, V.get('scale_terms', []))

        # Temporal precision
        metrics['temporal_precision'] = self._temporal_precision(content)

        # Rigor: stats lexicon + uncertainty language
        metrics['stats_hits'] = unique_phrase_hits(content, V.get('stats_terms', []))
        metrics['uncertainty_hits'] = unique_token_presence(
            cl, V.get('uncertainty_terms', ['uncertain','unclear','unknown'])
        )

        # Innovation: speculative markers, innovation lexicon, explicit gaps
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

    # ----- scoring helpers -----
    def _cov(self, hits: int, vocab_key: str) -> float:
        """[2.2] Convert unique-hit count to coverage ratio using actual dict size."""
        vocab_len = len(self.vocab.get(vocab_key, []))
        return ratio_coverage(hits, vocab_len or 1)

    def _score_depth(self, m: dict) -> float:
        """[2.3] Depth = 0.4·mechanistic + 0.3·causal + 0.3·temporal_precision."""
        mech = self._cov(m.get('mechanistic_hits', 0), 'mechanistic_terms')
        caus = self._cov(m.get('causal_hits', 0), 'causal_terms')
        temp = float(m.get('temporal_precision', 0.0))
        m['depth_mechanistic_cov'] = mech
        m['depth_causal_cov'] = caus
        m['depth_temp_precision'] = temp
        return float(np.average([mech, caus, temp], weights=[0.4, 0.3, 0.3]))

    def _score_breadth(self, m: dict) -> float:
        """[2.4] Breadth mix: regions, interventions, diversity, services, scales."""
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
        """[2.5] Rigor = (2/3)·stats_cov + (1/3)·uncertainty_cov."""
        stats = self._cov(m.get('stats_hits', 0), 'stats_terms')
        unc   = ratio_coverage(
            m.get('uncertainty_hits', 0),
            len(self.vocab.get('uncertainty_terms', ['uncertain','unclear','unknown'])) or 1
        )
        m['rigor_stats_cov'] = stats
        m['rigor_uncertainty_cov'] = unc
        return float(np.average([stats, unc], weights=[2/3, 1/3]))

    def _score_innovation(self, m: dict) -> float:
        """[2.6] Innovation mix with simple 3-count caps for speculative and gaps."""
        spec  = min(m.get('speculative_hits', 0) / 3.0, 1.0)
        iterm = self._cov(m.get('innovation_term_hits', 0), 'innovation_terms')
        gaps  = min(m.get('gap_hits', 0) / 3.0, 1.0)
        m['innovation_speculative'] = spec
        m['innovation_terms_cov']   = iterm
        m['innovation_gaps']        = gaps
        return float(np.average([spec, iterm, gaps], weights=[0.4, 0.3, 0.3]))

    def _score_info_density(self, m: dict) -> float:
        """[2.7] InfoDensity score = min(sources_per_1k / cap, 1)."""
        cap = max(1e-9, self.config.density_per_k_cap)
        return min(float(m.get('sources_per_1k', 0.0)) / cap, 1.0)

    def _score_ecological(self, m: dict) -> float:
        """[2.8] Ecological relevance = 0.4·conservation + 0.3·climate + 0.3·complexity."""
        cons = self._cov(m.get('conservation_hits', 0), 'conservation_terms')
        clim = self._cov(m.get('climate_hits', 0),      'climate_terms')
        comp = self._cov(m.get('complexity_hits', 0),   'complexity_terms')
        m['ecology_conservation_cov'] = cons
        m['ecology_climate_cov'] = clim
        m['ecology_complexity_cov'] = comp
        return float(np.average([cons, clim, comp], weights=[0.4, 0.3, 0.3]))

    def domain_calculate_quality_scores(self, m: dict):
        """
        [2.9] Compute six dimension scores and the overall linear aggregate.
        Clamp everything to [0,1] for downstream consumers.
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

        def _clip01(x): return float(np.clip(x, 0.0, 1.0))
        m.update({
            'depth_score': _clip01(depth),
            'breadth_score': _clip01(breadth),
            'rigor_score': _clip01(rigor),
            'innovation_score': _clip01(innovation),
            'ecological_relevance': _clip01(ecological),
            'info_density': _clip01(info_density),
            'overall_quality': _clip01(overall)
        })


# ──────────────────────────────────────────────────────────────────────────────
# [3] NLP analyzer (domain vocab, signals, scoring — mirrored to ecology)
# ──────────────────────────────────────────────────────────────────────────────

# Conservative, explicit defaults
_DEFAULT_CAUSAL = [
    "because","due to","caused by","results in","leads to","triggers","induces",
    "therefore","consequently","as a result","hence","thus","accordingly","owing to","through","via","by means of"
]
_DEFAULT_UNCERT = ["uncertain","unclear","unknown"]
_DEFAULT_SPECULATIVE = ["speculative","hypothetical","flagged"]
_DEFAULT_GAPS = ["research gap","knowledge gap","data gap"]
_DEFAULT_INNOV = ["novel","innovative","breakthrough","pioneering","cutting-edge",
                  "emerging","frontier","state-of-the-art","advanced","experimental",
                  "proof-of-concept","first","unprecedented"]


class NLPAnalyzer(BaseResearchAnalyzer):
    """
    NLP domain: same scoring schema and weights as Ecology for comparability.

    Depth = Mechanistic (arch+training+ablation) + Causal + Temporal precision
    Breadth = Tasks + Datasets + Languages + Eval metrics + Compute
    Rigor = Stats + Uncertainty
    Innovation = Speculative + Innovation lexicon + Gaps (with small caps)
    Domain Alignment (mapped to 'ecological_relevance' key) = Reproducibility + Safety + Compute
    InfoDensity = sources/1k with cap L=50
    """

    def build_vocab(self) -> dict:
        path = _default_vocab_path('nlp')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def domain_weights(self) -> QualityWeights:
        # identical to Ecology so that Q is directly comparable
        return QualityWeights(
            depth=0.26, breadth=0.24, rigor=0.16, innovation=0.16,
            domain_specific=0.12, info_density=0.06, taxonomic_or_specificity=0.00
        )

    def domain_extract_metrics(self, content: str, metrics: dict):
        V = self.vocab
        cl = content.lower()

        # Depth: mechanistic_nlp = arch ∪ training ∪ ablation
        mech_terms = (V.get('arch_terms', []) or []) + (V.get('training_terms', []) or []) + (V.get('ablation_terms', []) or [])
        metrics['mechanistic_hits'] = unique_phrase_hits(content, mech_terms)

        causal_terms = V.get('causal_terms', _DEFAULT_CAUSAL)
        metrics['causal_hits'] = unique_phrase_hits(content, causal_terms)

        metrics['temporal_precision'] = self._temporal_precision(content)

        # Breadth: tasks, datasets, languages, eval_metrics, compute
        metrics['task_hits']      = unique_phrase_hits(content, V.get('tasks', []))
        metrics['dataset_hits']   = unique_phrase_hits(content, V.get('datasets', []))
        metrics['language_hits']  = unique_phrase_hits(content, V.get('languages', []))
        metrics['metric_hits']    = unique_phrase_hits(content, V.get('eval_metrics', []))
        metrics['compute_hits']   = unique_phrase_hits(content, V.get('compute_terms', []))

        # Rigor: Stats + Uncertainty (duplizierte, kleine, präzise Liste)
        stats_list = V.get('rigor_stats', V.get('stats_terms', []))
        metrics['stats_hits'] = unique_phrase_hits(content, stats_list)
        metrics['uncertainty_hits'] = unique_token_presence(cl, V.get('uncertainty_terms', _DEFAULT_UNCERT))

        # Innovation
        metrics['speculative_hits']      = unique_token_presence(cl, V.get('speculative_terms', _DEFAULT_SPECULATIVE))
        metrics['innovation_term_hits']  = unique_phrase_hits(content, V.get('innovation_terms', _DEFAULT_INNOV))
        metrics['gap_hits']              = unique_token_presence(cl, V.get('gap_terms', _DEFAULT_GAPS))

        # Domain-Alignment (NLP): Repro + Safety + Compute
        metrics['repro_hits']   = unique_phrase_hits(content, V.get('repro_terms', []))
        metrics['safety_hits']  = unique_phrase_hits(content, V.get('safety_terms', []))
        metrics['comp_hits_da'] = unique_phrase_hits(content, V.get('compute_terms', []))

    # ---- Scoring helpers (mirrored) ----
    def _cov_list(self, hits: int, vocab_list: list) -> float:
        return ratio_coverage(hits, len(vocab_list) or 1)

    def _score_depth(self, m: dict) -> float:
        V = self.vocab
        mech_terms = (V.get('arch_terms', []) or []) + (V.get('training_terms', []) or []) + (V.get('ablation_terms', []) or [])
        mech = self._cov_list(m.get('mechanistic_hits', 0), mech_terms)
        caus = self._cov_list(m.get('causal_hits', 0), V.get('causal_terms', _DEFAULT_CAUSAL))
        temp = float(m.get('temporal_precision', 0.0))
        m['depth_mechanistic_cov'] = mech
        m['depth_causal_cov'] = caus
        m['depth_temp_precision'] = temp
        return float(np.average([mech, caus, temp], weights=[0.4, 0.3, 0.3]))

    def _score_breadth(self, m: dict) -> float:
        V = self.vocab
        task   = self._cov_list(m.get('task_hits', 0),     V.get('tasks', []))
        dset   = self._cov_list(m.get('dataset_hits', 0),  V.get('datasets', []))
        lang   = self._cov_list(m.get('language_hits', 0), V.get('languages', []))
        metr   = self._cov_list(m.get('metric_hits', 0),   V.get('eval_metrics', []))
        comp   = self._cov_list(m.get('compute_hits', 0),  V.get('compute_terms', []))
        m['breadth_tasks_cov']     = task
        m['breadth_datasets_cov']  = dset
        m['breadth_languages_cov'] = lang
        m['breadth_metrics_cov']   = metr
        m['breadth_compute_cov']   = comp
        return float(np.average([task, dset, lang, metr, comp],
                                weights=[0.25, 0.25, 0.25, 0.15, 0.10]))

    def _score_rigor(self, m: dict) -> float:
        V = self.vocab
        stats_list = V.get('rigor_stats', V.get('stats_terms', []))
        stats = self._cov_list(m.get('stats_hits', 0), stats_list)
        unc   = ratio_coverage(m.get('uncertainty_hits', 0), len(V.get('uncertainty_terms', _DEFAULT_UNCERT)) or 1)
        m['rigor_stats_cov'] = stats
        m['rigor_uncertainty_cov'] = unc
        return float(np.average([stats, unc], weights=[2/3, 1/3]))

    def _score_innovation(self, m: dict) -> float:
        spec  = min(m.get('speculative_hits', 0) / 3.0, 1.0)
        iterm = self._cov_list(m.get('innovation_term_hits', 0), self.vocab.get('innovation_terms', _DEFAULT_INNOV))
        gaps  = min(m.get('gap_hits', 0) / 3.0, 1.0)
        m['innovation_speculative'] = spec
        m['innovation_terms_cov']   = iterm
        m['innovation_gaps']        = gaps
        return float(np.average([spec, iterm, gaps], weights=[0.4, 0.3, 0.3]))

    def _score_info_density(self, m: dict) -> float:
        cap = max(1e-9, self.config.density_per_k_cap)   # L=50 as in Ecology
        return min(float(m.get('sources_per_1k', 0.0)) / cap, 1.0)

    def _score_domain(self, m: dict) -> float:
        V = self.vocab
        repro = self._cov_list(m.get('repro_hits', 0),   V.get('repro_terms', []))
        safety= self._cov_list(m.get('safety_hits', 0),  V.get('safety_terms', []))
        comp  = self._cov_list(m.get('comp_hits_da', 0), V.get('compute_terms', []))
        m['nlp_repro_cov']  = repro
        m['nlp_safety_cov'] = safety
        m['nlp_compute_cov']= comp
        return float(np.average([repro, safety, comp], weights=[0.4, 0.3, 0.3]))

    def domain_calculate_quality_scores(self, m: dict):
        w = self.weights
        depth        = self._score_depth(m)
        breadth      = self._score_breadth(m)
        rigor        = self._score_rigor(m)
        innovation   = self._score_innovation(m)
        density      = self._score_info_density(m)
        domain_align = self._score_domain(m)

        overall = (depth*w.depth + breadth*w.breadth + rigor*w.rigor +
                   innovation*w.innovation + domain_align*w.domain_specific +
                   density*w.info_density)

        def _clip01(x): return float(np.clip(x, 0.0, 1.0))
        m.update({
            'depth_score': _clip01(depth),
            'breadth_score': _clip01(breadth),
            'rigor_score': _clip01(rigor),
            'innovation_score': _clip01(innovation),
            # keep the same downstream key for domain alignment (works in plots)
            'ecological_relevance': _clip01(domain_align),
            'info_density': _clip01(density),
            'overall_quality': _clip01(overall)
        })


# ──────────────────────────────────────────────────────────────────────────────
# [4] Analyzer selector (factory)
# ──────────────────────────────────────────────────────────────────────────────

def get_analyzer(custom_config: Optional[ScoringConfig] = None):
    """Return analyzer for current utils.topic (keeps runners simple)."""
    if str(topic).lower().strip() == 'nlp':
        return NLPAnalyzer(config=custom_config)
    return EcologyAnalyzer(config=custom_config)

# Backwards-compatible alias
DeepResearchAnalyzer = NLPAnalyzer if str(topic).lower().strip() == 'nlp' else EcologyAnalyzer
