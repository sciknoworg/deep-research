
# Architecture (workflow)
# -----------------------
# [0]  Imports, utilities, configs
# [1]  BaseResearchAnalyzer (shared pipeline)
# [2]  EcologyAnalyzer  (signals + scoring)
# [3]  NLPAnalyzer      (signals + scoring, mirrored)
# [4]  get_analyzer()   (factory)


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
    depth_breadth_filename_patterns,   # e.g. ["d1_b1", "d1_b4", "d4_b1", "d4_b4"]
    model_and_search_pattern,          # e.g. "o3" | "o3-mini"
    load_domain_vocab,                 # loads vocab/<domain>_dictionaries.json
    topic                              # "ecology" | "nlp"
)

# External plotting helpers (unchanged)
from main_scaling_plot import create_main_scaling_plot
from optimization_analysis_plot import create_optimization_analysis_plot
from overall_quality_analysis import create_overall_quality_analysis
from parameter_effects_plot import create_parameter_effects_plot
from quality_dimensions_plot import create_quality_dimensions_plot

plt.style.use('seaborn-v0_8-whitegrid')


# ──────────────────────────────────────────────────────────────────────────────
# [0.1] Utility functions
# ──────────────────────────────────────────────────────────────────────────────

def _normalize_separators(s: str) -> str:
    s = re.sub(r'[-–—_/]+', ' ', s)
    return re.sub(r'\s+', ' ', s.strip().lower())


def unique_phrase_hits(text: str, vocab_terms: List[str]) -> int:
    """Unique-hit matching for phrases (0/1 je Vokabeleintrag), sep-tolerant & case-insensitive."""
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
    return (num / den) if den > 0 else default


def ratio_coverage(hits: int, vocab_len: int) -> float:
    denom = max(1, int(vocab_len))
    return min(max(0.0, float(hits)) / denom, 1.0)


def _default_vocab_path(domain_name: str) -> str:
    """Fallback locator for '<domain>_dictionaries.json' (only used if utils.load_domain_vocab is overridden)."""
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
# [0.2] Config objects (composite weights live in vocab; config only for density cap)
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class QualityWeights:
    """
    Composite weights for the five dimensions in the overall score.
    (We load final values from vocab["weights"]["alpha"].)
    """
    depth: float = 0.29
    breadth: float = 0.27
    rigor: float = 0.19
    innovation: float = 0.19
    gap: float = 0.06

    def normalize(self):
        s = self.depth + self.breadth + self.rigor + self.innovation + self.gap
        if s <= 0:
            return
        self.depth /= s; self.breadth /= s; self.rigor /= s; self.innovation /= s; self.gap /= s


@dataclass
class ScoringConfig:
    """
    density_per_k_cap: cap for InfoDensity score (sources per 1k → [0,1]).
    """
    density_per_k_cap: float = 50.0
    weights: Optional[QualityWeights] = None  # final α come from vocab unless overridden


# ──────────────────────────────────────────────────────────────────────────────
# [1] Base class: batch orchestration
# ──────────────────────────────────────────────────────────────────────────────

class BaseResearchAnalyzer:
    """
    Shared I/O & pipeline. Subclasses implement domain-specific extraction + scoring.
    """

    def __init__(self, config: Optional[ScoringConfig] = None):
        self.config = config if config is not None else ScoringConfig()
        self.vocab = self.build_vocab()  # MUST load from vocab/<domain>_dictionaries.json
        # Load composite α from vocab (fallback to config or defaults)
        self.weights = self._load_composite_weights_from_vocab(self.vocab.get("weights", {}), self.config.weights)
        self.part_w = self._load_part_weights_from_vocab(self.vocab.get("weights", {}))
        self.documents: Dict[str, dict] = {}
        self.metrics: Dict[str, dict] = {}

    # ----- subclass API -----
    def build_vocab(self) -> dict:
        raise NotImplementedError

    def domain_extract_metrics(self, content: str, metrics: dict):
        raise NotImplementedError

    def domain_calculate_quality_scores(self, metrics: dict):
        raise NotImplementedError

    def domain_publication_plots(self, statistics_file, all_results, figures_dir):
        self.create_common_publication_plots(statistics_file, all_results, figures_dir)

    # ----- weights from vocab -----
    def _load_composite_weights_from_vocab(self, wblock: dict, override: Optional[QualityWeights]) -> QualityWeights:
        if override is not None:
            override.normalize()
            return override
        alpha = (wblock or {}).get("alpha", {}) or {}
        qw = QualityWeights(
            depth=float(alpha.get("depth", 0.29)),
            breadth=float(alpha.get("breadth", 0.27)),
            rigor=float(alpha.get("rigor", 0.19)),
            innovation=float(alpha.get("innov", 0.19)),
            gap=float(alpha.get("gap", 0.06)),
        )
        qw.normalize()
        return qw

    def _load_part_weights_from_vocab(self, wblock: dict) -> dict:
        # Provide sane fallbacks if any block is missing; otherwise use vocab-provided values.
        def _norm(d: dict, defaults: dict) -> dict:
            base = dict(defaults)
            base.update(d or {})
            s = sum(base.values()) or 1.0
            return {k: v / s for k, v in base.items()}

        return {
            "depth": _norm((wblock or {}).get("depth", {}),
                           {"mech": 0.40, "causal": 0.30, "temp": 0.30}),
            "breadth_ecology": _norm((wblock or {}).get("breadth", {}),
                                     {"regions": 0.25, "interventions": 0.25, "biodiversity": 0.25, "services": 0.15, "scale": 0.10}),
            "breadth_nlp": _norm((wblock or {}).get("breadth", {}),
                                 {"tasks": 0.25, "datasets": 0.25, "metrics": 0.25, "languages": 0.15, "setting": 0.10}),
            "rigor": _norm((wblock or {}).get("rigor", {}),
                           {"stats": 2/3, "uncert": 1/3}),
            "innovation": _norm((wblock or {}).get("innovation", {}),
                                {"spec": 0.50, "novel": 0.50})
        }

    # ----- shared helpers -----
    def load_document(self, filename: str, content: str) -> None:
        m = re.search(r'd(\d+)_b(\d+)', filename)
        if not m:
            return
        depth, breadth = int(m.group(1)), int(m.group(2))
        key = f"d{depth}_b{breadth}"
        self.documents[key] = dict(filename=filename, depth=depth, breadth=breadth, content=content)

    # Limit source counting to terminal references section
    def _find_sources_section(self, content: str) -> str:
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
            self.domain_extract_metrics(content, metrics)  # populate hits, etc.
            self.metrics[key] = metrics

    def analyze_multiple_questions(self, report_dir: str, question_numbers: List[str], output_dir: str) -> dict:
        os.makedirs(output_dir, exist_ok=True)
        all_results: Dict[str, pd.DataFrame] = {}

        for q in question_numbers:
            self.documents.clear(); self.metrics.clear()
            loaded = 0
            for cfg in depth_breadth_filename_patterns:
                fname = f"{q}_{model_and_search_pattern}_{cfg}.md"
                try:
                    with open(os.path.join(report_dir, fname), 'r', encoding='utf-8') as f:
                        self.load_document(fname, f.read())
                    loaded += 1
                except FileNotFoundError:
                    print(f"[WARN] File not found: {fname}")
            if not loaded:
                continue

            self.extract_metrics()
            for k in list(self.metrics.keys()):
                self.domain_calculate_quality_scores(self.metrics[k])

            os.makedirs(os.path.join(output_dir, "plot_per_question"), exist_ok=True)
            fig, df = self._default_visualizations(pd.DataFrame(self.metrics).T)
            fig.savefig(os.path.join(output_dir, f"plot_per_question/question_{q}_analysis.png"),
                        dpi=300, bbox_inches='tight')
            plt.close(fig)

            df['config'] = [f"d{self.documents[k]['depth']}_b{self.documents[k]['breadth']}" for k in df.index]
            df['question'] = q
            all_results[q] = df
            print(f"[OK] Analyzed question {q} with {loaded} documents")

        if all_results:
            self._save_summary(all_results, output_dir)
        return all_results

    @staticmethod
    def _save_summary(all_results: Dict[str, pd.DataFrame], output_dir: str) -> None:
        combined = pd.concat(all_results.values(), ignore_index=True)

        # Clamp score-like columns. Domain-alignment removed; include gap_score.
        score_cols = [
            'depth_score','breadth_score','rigor_score','innovation_score','gap_score',
            'info_density','overall_quality',
            'breadth_regions_cov','breadth_interventions_cov','breadth_diversity_cov',
            'breadth_services_cov','breadth_scales_cov',
            'depth_mechanistic_cov','depth_causal_cov','depth_temp_precision',
            'rigor_stats_cov','rigor_uncertainty_cov',
            # NLP breadth (if present)
            'breadth_tasks_cov','breadth_datasets_cov','breadth_languages_cov',
            'breadth_metrics_cov','breadth_compute_cov'
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
        defaults = {
            'word_count': 0, 'source_count': 0, 'sources_per_1k': 0.0,
            'overall_quality': np.nan,
            'depth_score': np.nan, 'breadth_score': np.nan,
            'rigor_score': np.nan, 'innovation_score': np.nan, 'gap_score': np.nan,
            'info_density': np.nan
        }
        for k, v in defaults.items():
            if k not in df.columns:
                df[k] = v

        df['depth'] = [int(k.split('_')[0][1:]) for k in df.index]
        df['breadth'] = [int(k.split('_')[1][1:]) for k in df.index]

        fig, axes = plt.subplots(3, 3, figsize=(18, 14))
        axes = axes.flatten()

        def _heat(ax, col, title, cmap, fmt='.0f'):
            try:
                pv = df.pivot_table(index='depth', columns='breadth', values=col, aggfunc='mean')
                sns.heatmap(pv, annot=True, fmt=fmt, cmap=cmap, ax=ax)
                ax.set_title(title)
            except Exception:
                ax.set_axis_off()

        def _bar(ax, series, title, ylim=(0, 1), fmt='.2f', draw_max_line=None):
            y = series.fillna(0)
            ax.bar(series.index, y); ax.set_title(title)
            ax.tick_params(axis='x', rotation=45); ax.set_ylim(*ylim)
            for i, v in enumerate(y):
                ax.text(i, v, format(float(v), fmt), ha='center', va='bottom', fontsize=8)
            if draw_max_line is not None:
                ax.axhline(draw_max_line, linestyle='--', linewidth=1.2, alpha=0.7, color='k')

        _heat(axes[0], 'word_count', 'Word Count by Depth & Breadth', 'YlOrRd', '.0f')
        _heat(axes[1], 'source_count', 'Sources by Depth & Breadth', 'Blues', '.0f')
        _heat(axes[2], 'sources_per_1k', 'Sources per 1k by Depth & Breadth', 'Greens', '.2f')

        idx_order = list(df.index)
        overall_scaled = (df.loc[idx_order, 'overall_quality'] * 4.0).fillna(0.0)
        _bar(axes[3], overall_scaled, 'Average Research Quality (0–4 scale)', (0, 4.1), '.2f', draw_max_line=4.0)
        _bar(axes[4], df.loc[idx_order, 'depth_score'], 'Depth Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[5], df.loc[idx_order, 'breadth_score'], 'Breadth Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[6], df.loc[idx_order, 'rigor_score'], 'Rigor Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[7], df.loc[idx_order, 'innovation_score'], 'Innovation Score (0–1)', (0, 1.0), '.2f')
        _bar(axes[8], df.loc[idx_order, 'gap_score'], 'Gap Score (0–1)', (0, 1.0), '.2f')

        plt.tight_layout()
        return fig, df

    def create_common_publication_plots(self, statistics_file, all_results, figures_dir):
        os.makedirs(figures_dir, exist_ok=True)
        df = pd.concat(all_results.values(), ignore_index=True)
        for col in ['word_count', 'source_count', 'sources_per_1k',
                    'depth_score', 'breadth_score', 'rigor_score',
                    'innovation_score', 'gap_score', 'overall_quality']:
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
# [2] Ecology analyzer
# ──────────────────────────────────────────────────────────────────────────────

class EcologyAnalyzer(BaseResearchAnalyzer):
    """Ecology: ratio-coverage per dict + temporal precision, arithmetic aggregation."""

    def build_vocab(self) -> dict:
        return load_domain_vocab()

    def domain_extract_metrics(self, content: str, metrics: dict):
        V = self.vocab
        cl = content.lower()

        # Coverage hits
        metrics['mechanistic_hits']   = unique_phrase_hits(content, V.get('mechanistic_terms', []))
        metrics['causal_hits']        = unique_phrase_hits(content, V.get('causal_terms', []))
        metrics['region_hits']        = unique_phrase_hits(content, V.get('regions', []))
        metrics['intervention_hits']  = unique_phrase_hits(content, V.get('interventions', []))
        metrics['diversity_hits']     = unique_phrase_hits(content, V.get('diversity_dimensions', []))
        metrics['services_hits']      = unique_phrase_hits(content, V.get('ecosystem_services', []))
        metrics['scales_hits']        = unique_phrase_hits(content, V.get('scale_terms', []))

        # Temporal precision
        metrics['temporal_precision'] = self._temporal_precision(content)

        # Rigor
        metrics['stats_hits'] = unique_phrase_hits(content, V.get('stats_terms', []))
        metrics['uncertainty_hits'] = unique_token_presence(cl, V.get('uncertainty_terms', []))

        # Innovation + Gap
        metrics['speculative_hits']      = unique_token_presence(cl, V.get('speculation_terms', []))
        metrics['innovation_term_hits']  = unique_phrase_hits(content, V.get('innovation_terms', []))
        metrics['gap_hits']              = unique_token_presence(cl, V.get('gap_terms', []))

    # ----- scoring helpers -----
    def _cov(self, hits: int, vocab_key: str) -> float:
        vocab_len = len(self.vocab.get(vocab_key, []))
        return ratio_coverage(hits, vocab_len or 1)

    def _score_depth(self, m: dict) -> float:
        pw = self.part_w["depth"]
        mech = self._cov(m.get('mechanistic_hits', 0), 'mechanistic_terms')
        caus = self._cov(m.get('causal_hits', 0), 'causal_terms')
        temp = float(m.get('temporal_precision', 0.0))
        m['depth_mechanistic_cov'] = mech
        m['depth_causal_cov'] = caus
        m['depth_temp_precision'] = temp
        return float(mech*pw['mech'] + caus*pw['causal'] + temp*pw['temp'])

    def _score_breadth(self, m: dict) -> float:
        pw = self.part_w["breadth_ecology"]
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
        return float(region*pw['regions'] + interv*pw['interventions'] +
                     divers*pw['biodiversity'] + serv*pw['services'] + scale*pw['scale'])

    def _score_rigor(self, m: dict) -> float:
        pw = self.part_w["rigor"]
        stats = self._cov(m.get('stats_hits', 0), 'stats_terms')
        unc   = ratio_coverage(m.get('uncertainty_hits', 0), len(self.vocab.get('uncertainty_terms', [])) or 1)
        m['rigor_stats_cov'] = stats
        m['rigor_uncertainty_cov'] = unc
        return float(stats*pw['stats'] + unc*pw['uncert'])

    def _score_innovation(self, m: dict) -> float:
        pw = self.part_w["innovation"]
        spec  = min(m.get('speculative_hits', 0) / 3.0, 1.0)  # conservative cap
        iterm = self._cov(m.get('innovation_term_hits', 0), 'innovation_terms')
        m['innovation_speculative'] = spec
        m['innovation_terms_cov']   = iterm
        return float(spec*pw['spec'] + iterm*pw['novel'])

    def _score_gap(self, m: dict) -> float:
        gap = ratio_coverage(m.get('gap_hits', 0), len(self.vocab.get('gap_terms', [])) or 1)
        m['gap_score'] = gap
        return float(gap)

    def _score_info_density(self, m: dict) -> float:
        cap = max(1e-9, self.config.density_per_k_cap)
        return min(float(m.get('sources_per_1k', 0.0)) / cap, 1.0)

    def domain_calculate_quality_scores(self, m: dict):
        a = self.weights
        depth      = self._score_depth(m)
        breadth    = self._score_breadth(m)
        rigor      = self._score_rigor(m)
        innov      = self._score_innovation(m)
        gap        = self._score_gap(m)
        info_dens  = self._score_info_density(m)  # stored only

        def _c(x): return float(np.clip(x, 0.0, 1.0))
        overall = (depth*a.depth + breadth*a.breadth + rigor*a.rigor + innov*a.innovation + gap*a.gap)

        m.update({
            'depth_score': _c(depth),
            'breadth_score': _c(breadth),
            'rigor_score': _c(rigor),
            'innovation_score': _c(innov),
            'gap_score': _c(gap),
            'info_density': _c(info_dens),
            'overall_quality': _c(overall)
        })


# ──────────────────────────────────────────────────────────────────────────────
# [3] NLP analyzer (mirrored)
# ──────────────────────────────────────────────────────────────────────────────

class NLPAnalyzer(BaseResearchAnalyzer):
    """NLP: mirrored scoring; Breadth facets/tasks; Depth via arch+training+ablation proxies."""

    def build_vocab(self) -> dict:
        # If your utils.load_domain_vocab switches by topic, you can reuse it;
        # else, fall back to reading vocab/nlp_dictionaries.json via helper above.
        try:
            return load_domain_vocab()
        except Exception:
            path = _default_vocab_path('nlp')
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)

    def domain_extract_metrics(self, content: str, metrics: dict):
        V = self.vocab
        cl = content.lower()

        # Depth: mechanistic_nlp = arch ∪ training ∪ ablation
        mech_terms = (V.get('arch_terms', []) or []) + (V.get('training_terms', []) or []) + (V.get('ablation_terms', []) or [])
        metrics['mechanistic_hits'] = unique_phrase_hits(content, mech_terms)
        metrics['causal_hits']      = unique_phrase_hits(content, V.get('causal_terms', []))
        metrics['temporal_precision'] = self._temporal_precision(content)

        # Breadth facets
        metrics['task_hits']      = unique_phrase_hits(content, V.get('tasks', []))
        metrics['dataset_hits']   = unique_phrase_hits(content, V.get('datasets', []))
        metrics['language_hits']  = unique_phrase_hits(content, V.get('languages', []))
        metrics['metric_hits']    = unique_phrase_hits(content, V.get('eval_metrics', []))
        metrics['compute_hits']   = unique_phrase_hits(content, V.get('compute_terms', []))

        # Rigor
        stats_list = V.get('rigor_stats', V.get('stats_terms', []))
        metrics['stats_hits'] = unique_phrase_hits(content, stats_list)
        metrics['uncertainty_hits'] = unique_token_presence(cl, V.get('uncertainty_terms', []))

        # Innovation + Gap
        metrics['speculative_hits']      = unique_token_presence(cl, V.get('speculation_terms', []))
        metrics['innovation_term_hits']  = unique_phrase_hits(content, V.get('innovation_terms', []))
        metrics['gap_hits']              = unique_token_presence(cl, V.get('gap_terms', []))

    def _cov_list(self, hits: int, vocab_list: list) -> float:
        return ratio_coverage(hits, len(vocab_list) or 1)

    def _score_depth(self, m: dict) -> float:
        pw = self.part_w["depth"]
        V = self.vocab
        mech_terms = (V.get('arch_terms', []) or []) + (V.get('training_terms', []) or []) + (V.get('ablation_terms', []) or [])
        mech = self._cov_list(m.get('mechanistic_hits', 0), mech_terms)
        caus = self._cov_list(m.get('causal_hits', 0), V.get('causal_terms', []))
        temp = float(m.get('temporal_precision', 0.0))
        m['depth_mechanistic_cov'] = mech
        m['depth_causal_cov'] = caus
        m['depth_temp_precision'] = temp
        return float(mech*pw['mech'] + caus*pw['causal'] + temp*pw['temp'])

    def _score_breadth(self, m: dict) -> float:
        pw = self.part_w["breadth_nlp"]
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
        return float(task*pw['tasks'] + dset*pw['datasets'] + lang*pw['languages'] +
                     metr*pw['metrics'] + comp*pw['setting'])  # "setting" maps to compute proxy

    def _score_rigor(self, m: dict) -> float:
        pw = self.part_w["rigor"]
        V = self.vocab
        stats_list = V.get('rigor_stats', V.get('stats_terms', []))
        stats = self._cov_list(m.get('stats_hits', 0), stats_list)
        unc   = ratio_coverage(m.get('uncertainty_hits', 0), len(V.get('uncertainty_terms', [])) or 1)
        m['rigor_stats_cov'] = stats
        m['rigor_uncertainty_cov'] = unc
        return float(stats*pw['stats'] + unc*pw['uncert'])

    def _score_innovation(self, m: dict) -> float:
        pw = self.part_w["innovation"]
        iterm = self._cov_list(m.get('innovation_term_hits', 0), self.vocab.get('innovation_terms', []))
        spec  = min(m.get('speculative_hits', 0) / 3.0, 1.0)
        m['innovation_terms_cov']   = iterm
        m['innovation_speculative'] = spec
        return float(spec*pw['spec'] + iterm*pw['novel'])

    def _score_gap(self, m: dict) -> float:
        gap = ratio_coverage(m.get('gap_hits', 0), len(self.vocab.get('gap_terms', [])) or 1)
        m['gap_score'] = gap
        return float(gap)

    def _score_info_density(self, m: dict) -> float:
        cap = max(1e-9, self.config.density_per_k_cap)
        return min(float(m.get('sources_per_1k', 0.0)) / cap, 1.0)

    def domain_calculate_quality_scores(self, m: dict):
        a = self.weights
        depth   = self._score_depth(m)
        breadth = self._score_breadth(m)
        rigor   = self._score_rigor(m)
        innov   = self._score_innovation(m)
        gap     = self._score_gap(m)
        info_d  = self._score_info_density(m)

        def _c(x): return float(np.clip(x, 0.0, 1.0))
        overall = (depth*a.depth + breadth*a.breadth + rigor*a.rigor + innov*a.innovation + gap*a.gap)

        m.update({
            'depth_score': _c(depth),
            'breadth_score': _c(breadth),
            'rigor_score': _c(rigor),
            'innovation_score': _c(innov),
            'gap_score': _c(gap),
            'info_density': _c(info_d),
            'overall_quality': _c(overall)
        })


# ──────────────────────────────────────────────────────────────────────────────
# [4] Analyzer selector (factory)
# ──────────────────────────────────────────────────────────────────────────────

def get_analyzer(custom_config: Optional[ScoringConfig] = None):
    """Select analyzer by utils.topic (keeps runners simple)."""
    if str(topic).lower().strip() == 'nlp':
        return NLPAnalyzer(config=custom_config)
    return EcologyAnalyzer(config=custom_config)
