import os
import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

from utils import (
    depth_breadth_filename_patterns,
    model_and_search_pattern,
    load_domain_vocab,   # ecology loader -> ecology_dictionaries.json
    topic                # "ecology" | "nlp"
)


from main_scaling_plot import create_main_scaling_plot
from optimization_analysis_plot import create_optimization_analysis_plot
from overall_quality_analysis import create_overall_quality_analysis
from parameter_effects_plot import create_parameter_effects_plot
from quality_dimensions_plot import create_quality_dimensions_plot

plt.style.use('seaborn-v0_8-whitegrid')

# ---------------------------
# Shared helpers
# ---------------------------

WORD_BOUNDARY = r'(?<![A-Za-z0-9_-]){term}(?![A-Za-z0-9_-])'

def unique_phrase_hits(text: str, vocab_terms) -> int:
    """
    Unique presence per vocab term/phrase with strict word boundaries (phrases supported).
    Counts coverage (0/1 per term), not frequency.
    """
    t = text.lower()
    hits = 0
    for term in vocab_terms:
        term_esc = re.escape(str(term).lower().strip())
        pattern = WORD_BOUNDARY.format(term=term_esc.replace(r'\ ', r'\s+'))
        if re.search(pattern, t, flags=re.IGNORECASE):
            hits += 1
    return hits

def safe_div(num: float, den: float, default: float = 0.0) -> float:
    return num / den if den > 0 else default

def hmean(values, weights):
    """Weighted harmonic mean on [0,1], penalizes imbalance strongly."""
    v = np.clip(np.array(values, dtype=float), 1e-6, 1.0)
    w = np.array(weights, dtype=float)
    return (w.sum()) / ((w / v).sum())

def _default_vocab_path(domain_name: str) -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(here, '..'))
    cwd = os.getcwd()

    fname = f'{domain_name}_dictionaries.json'
    candidates = [
        os.path.join(here, 'data', 'vocab', fname),
        os.path.join(repo_root, 'data', 'vocab', fname),
        os.path.join(here, 'vocab', fname),
        os.path.join(repo_root, 'vocab', fname),
        os.path.join(cwd, 'data', 'vocab', fname),
        os.path.join(cwd, 'vocab', fname),
        os.path.join(cwd, fname),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p

    return os.path.join(repo_root, 'vocab', fname)


# ---------------------------
# Base class
# ---------------------------

@dataclass
class QualityWeights:
    depth: float = 0.22
    breadth: float = 0.20
    rigor: float = 0.18
    innovation: float = 0.15
    domain_specific: float = 0.12  # Ecology: ecological relevance; NLP: reproducibility/safety
    info_density: float = 0.08
    taxonomic_or_specificity: float = 0.05  # Ecology: taxonomic; NLP: reporting specificity


class BaseResearchAnalyzer:
    """
    Base with shared IO & skeleton. Subclasses must implement:
      - build_vocab()
      - domain_extract_metrics(content, metrics)
      - domain_calculate_quality_scores(metrics_dict)
      - domain_publication_plots(statistics_file, all_results, figures_dir)
    """
    def __init__(self):
        self.documents = {}
        self.metrics = {}
        self.vocab = self.build_vocab()
        self.weights = self.domain_weights()

    # ---- to override in subclasses ----
    def build_vocab(self):
        raise NotImplementedError

    def domain_weights(self) -> QualityWeights:
        return QualityWeights()

    def domain_extract_metrics(self, content: str, metrics: dict):
        raise NotImplementedError

    def domain_calculate_quality_scores(self, metrics_dict: dict):
        raise NotImplementedError

    def domain_publication_plots(self, statistics_file, all_results, figures_dir):
        """
        Subclasses can override. If not, the base provides a generic, domain-agnostic
        plot set via create_common_publication_plots (same filenames across domains).
        """
        self.create_common_publication_plots(statistics_file, all_results, figures_dir)

    # ---- shared extraction ----
    def load_document(self, filename, content):
        m = re.search(r'd(\d+)_b(\d+)', filename)
        if not m:
            return
        depth = int(m.group(1)); breadth = int(m.group(2))
        key = f"d{depth}_b{breadth}"
        self.documents[key] = {
            'filename': filename,
            'depth': depth,
            'breadth': breadth,
            'content': content
        }

    def extract_source_count(self, content):
        # Exclude typical reference headers to avoid double counting pasted lists
        body = re.split(r'\n#+\s*(references|bibliography|works cited)\b', content, flags=re.IGNORECASE)[0]
        urls = re.findall(r'https?://[^\s\)]+', body)
        return len(set(urls))

    def extract_temporal_precision(self, content):
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
        sc = sum(len(re.findall(p, content.lower())) for p in specific_patterns)
        vc = sum(content.lower().count(t) for t in vague_terms)
        return sc / max(1, sc + vc)

    def extract_metrics(self):
        for key, doc in self.documents.items():
            content = doc['content']; cl = content.lower()
            metrics = {}
            metrics['word_count'] = len(content.split())
            metrics['char_count'] = len(content)
            metrics['source_count'] = self.extract_source_count(content)
            metrics['section_count'] = len(content.split('\n## '))
            metrics['formal_citations'] = len(re.findall(r'\([^)]*\d{4}[^)]*\)', content))
            metrics['percentage_values'] = len(re.findall(r'\d+\.?\d*\s*%', content))

            # Delegate to subclass (domain-specific blocks)
            self.domain_extract_metrics(content, metrics)
            self.metrics[key] = metrics

    # ---- pipeline glue ----
    def analyze_multiple_questions(self, report_dir, question_numbers, output_dir) -> dict:
        os.makedirs(output_dir, exist_ok=True)
        all_results = {}

        for question_num in question_numbers:
            self.documents = {}
            self.metrics = {}

            loaded = 0
            for config in depth_breadth_filename_patterns:
                filename = f"{question_num}_{model_and_search_pattern}_{config}.md"
                try:
                    with open(os.path.join(report_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.load_document(filename, content)
                    loaded += 1
                except FileNotFoundError:
                    print(f"[WARN] File not found: {filename}")

            if loaded == 0:
                continue

            self.extract_metrics()
            for k in list(self.metrics.keys()):
                self.domain_calculate_quality_scores(self.metrics[k])

            os.makedirs(os.path.join(output_dir, "plot_per_question"), exist_ok=True)
            fig, df = self._default_visualizations(pd.DataFrame(self.metrics).T)
            fig.savefig(os.path.join(output_dir, f"plot_per_question/question_{question_num}_analysis.png"),
                        dpi=300, bbox_inches='tight')
            plt.close(fig)

            df['config'] = [f"d{self.documents[k]['depth']}_b{self.documents[k]['breadth']}" for k in df.index]
            df['question'] = question_num
            all_results[question_num] = df

            print(f"[OK] Analyzed question {question_num} with {loaded} documents")

        if all_results:
            self._save_comprehensive_summary_statistics(all_results, output_dir)
        return all_results

    @staticmethod
    def _save_comprehensive_summary_statistics(all_results, output_dir):
        """
        Save per-config summary stats + include sample sizes to detect imbalance.
        """
        combined_df = pd.concat(all_results.values(), ignore_index=True)

        # Aggregate numeric columns by mean/std/min/max
        agg_spec = {}
        for col in combined_df.columns:
            if col in ('config','question'):
                continue
            if np.issubdtype(combined_df[col].dtype, np.number):
                agg_spec[col] = ['mean','std','min','max']

        summary = combined_df.groupby('config').agg(agg_spec).round(3)
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]

        # Add per-config sample sizes to avoid misinterpretation when coverage is uneven
        counts = combined_df.groupby('config').size().rename('n_docs')
        summary = pd.concat([counts, summary], axis=1)

        os.makedirs(output_dir, exist_ok=True)
        summary.to_csv(os.path.join(output_dir, "comprehensive_summary_statistics.csv"))

    def _default_visualizations(self, df: pd.DataFrame):
        """
        Common core panels for both domains:
          (1) Word Count heatmap
          (2) Source Count heatmap
          (3) Overall Quality bar
          (4) First available dimension bar (depth/breadth/rigor/innovation)
        """
        for col in ['word_count','source_count']:
            if col not in df.columns:
                df[col] = 0
        df['depth'] = [int(k.split('_')[0][1:]) for k in df.index]
        df['breadth'] = [int(k.split('_')[1][1:]) for k in df.index]

        fig = plt.figure(figsize=(16, 12))

        ax1 = plt.subplot(2, 2, 1)
        hm1 = df.pivot_table(index='depth', columns='breadth', values='word_count', aggfunc='mean')
        sns.heatmap(hm1, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax1)
        ax1.set_title('Word Count by Depth & Breadth')

        ax2 = plt.subplot(2, 2, 2)
        hm2 = df.pivot_table(index='depth', columns='breadth', values='source_count', aggfunc='mean')
        sns.heatmap(hm2, annot=True, fmt='.0f', cmap='Blues', ax=ax2)
        ax2.set_title('Sources by Depth & Breadth')

        ax3 = plt.subplot(2, 2, 3)
        y = df.get('overall_quality', pd.Series([0]*len(df), index=df.index))
        ax3.bar(df.index, y)
        ax3.set_title('Overall Quality')
        ax3.tick_params(axis='x', rotation=45)

        ax4 = plt.subplot(2, 2, 4)
        for candidate in ['depth_score','breadth_score','rigor_score','innovation_score']:
            if candidate in df.columns:
                ax4.bar(df.index, df[candidate])
                ax4.set_title(candidate.replace('_',' ').title())
                ax4.tick_params(axis='x', rotation=45)
                break

        plt.tight_layout()
        return fig, df

    # -------- Common, domain-agnostic publication plots (SAME filenames across domains) --------
    def create_common_publication_plots(self, statistics_file, all_results, figures_dir):
        """
        Produce the 4 key figures with the SAME filenames used in the Ecology paper modules:
          - main_scaling_effects.png
          - parameter_effects.png
          - quality_dimensions.png
          - optimization_analysis.png
        Ensures comparability for Ecology and NLP outputs.
        """
        os.makedirs(figures_dir, exist_ok=True)
        df = pd.concat(all_results.values(), ignore_index=True)

        # Ensure expected columns exist
        for col in ['word_count', 'source_count', 'depth_score', 'breadth_score',
                    'rigor_score', 'innovation_score', 'overall_quality']:
            if col not in df.columns:
                df[col] = 0.0
        if 'config' not in df.columns:
            df['config'] = 'd1_b1'
        df['depth'] = df['config'].str.extract(r'd(\d+)').astype(int)
        df['breadth'] = df['config'].str.extract(r'b(\d+)').astype(int)

        # 1) Main scaling plot
        plt.figure(figsize=(10,4))
        plt.subplot(1,2,1)
        sns.heatmap(df.pivot_table(index='depth', columns='breadth', values='word_count', aggfunc='mean'),
                    annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('Word Count by Depth & Breadth')
        plt.subplot(1,2,2)
        sns.heatmap(df.pivot_table(index='depth', columns='breadth', values='source_count', aggfunc='mean'),
                    annot=True, fmt='.0f', cmap='Blues')
        plt.title('Sources by Depth & Breadth')
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'main_scaling_effects.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 2) Parameter effects (Δ in source_count)
        def pct_change(a, b):
            return (b - a) / a * 100 if a > 0 else 0.0
        depth1 = df[df['depth']==1]['source_count'].mean()
        depth4 = df[df['depth']==4]['source_count'].mean()
        breadth1 = df[df['breadth']==1]['source_count'].mean()
        breadth4 = df[df['breadth']==4]['source_count'].mean()

        plt.figure(figsize=(6,4))
        plt.bar(['Depth 1→4','Breadth 1→4'],
                [pct_change(depth1, depth4), pct_change(breadth1, breadth4)])
        plt.ylabel('% change in sources')
        plt.title('Parameter Effects on Source Utilization')
        plt.savefig(os.path.join(figures_dir, 'parameter_effects.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 3) Quality dimensions (stacked)
        dims = ['depth_score','breadth_score','rigor_score','innovation_score']
        df_mean = df.groupby('config')[dims].mean()
        plt.figure(figsize=(8,5))
        bottom = np.zeros(len(df_mean))
        for d in dims:
            plt.bar(df_mean.index, df_mean[d].values, bottom=bottom, label=d)
            bottom = bottom + df_mean[d].values
        plt.xticks(rotation=30)
        plt.title('Quality Dimensions')
        plt.legend()
        plt.savefig(os.path.join(figures_dir, 'quality_dimensions.png'), dpi=300, bbox_inches='tight')
        plt.close()

        # 4) Optimization (Overall quality vs source_count)
        cost = df.groupby('config')['source_count'].mean()
        quality = df.groupby('config')['overall_quality'].mean()
        plt.figure(figsize=(6,5))
        plt.scatter(cost, quality)
        for cfg in quality.index:
            plt.annotate(cfg, (cost[cfg], quality[cfg]))
        plt.xlabel('Avg sources (cost proxy)')
        plt.ylabel('Overall quality')
        plt.title('Quality vs Cost')
        plt.savefig(os.path.join(figures_dir, 'optimization_analysis.png'), dpi=300, bbox_inches='tight')
        plt.close()


# ---------------------------
# Ecology Analyzer
# ---------------------------

class EcologyAnalyzer(BaseResearchAnalyzer):
    """Ecology domain using coverage + harmonic-depth (paper-aligned)."""

    def build_vocab(self):
        return load_domain_vocab()

    def domain_extract_metrics(self, content: str, metrics: dict):
        cl = content.lower()
        V = self.vocab

        # Coverage blocks
        metrics['mechanistic_detail']   = unique_phrase_hits(content, V['mechanistic_terms'])
        metrics['causal_explanations']  = unique_phrase_hits(content, V['causal_terms'])
        metrics['geographic_regions']   = unique_phrase_hits(content, V['regions'])
        metrics['intervention_types']   = unique_phrase_hits(content, V['interventions'])
        metrics['diversity_dimensions'] = unique_phrase_hits(content, V['diversity_dimensions'])
        metrics['ecosystem_services']   = unique_phrase_hits(content, V['ecosystem_services'])
        metrics['spatial_scales']       = unique_phrase_hits(content, V['scale_terms'])

        # Temporal
        metrics['temporal_precision']  = self.extract_temporal_precision(content)
        metrics['temporal_references'] = len(re.findall(r'\d+[\s-]+(?:yr|year|decade)', content))

        # Rigor / Policy / etc.
        metrics['research_gaps'] = cl.count('research gap') + cl.count('knowledge gap') + cl.count('data gap')
        metrics['speculative_ideas'] = cl.count('speculative') + cl.count('flagged') + cl.count('hypothetical')
        metrics['uncertainty_acknowledgment'] = cl.count('uncertain') + cl.count('unclear') + cl.count('unknown')
        metrics['hypothesis_testing'] = cl.count('hypothesis') + cl.count('test') + cl.count('experiment')
        metrics['tradeoff_mentions']  = cl.count('trade-off') + cl.count('tradeoff') + cl.count('balance')
        metrics['statistical_rigor']  = sum(cl.count(t) for t in V['stats_terms'])
        metrics['policy_mentions']    = cl.count('policy') + cl.count('subsidy') + cl.count('regulation')

        # Innovation indicators 
        metrics['innovation_indicators'] = sum(cl.count(t) for t in V.get('innovation_terms', []))

        # Taxonomy — improved: count UNIQUE taxa to avoid saturation by repetition
        taxon_patterns = [
            r'\b[A-Z][a-z]+ [a-z]+\b',          # Genus species
            r'\b[A-Z]\. [a-z]+\b',              # G. species
            r'\b[A-Z][a-z]+ (sp\.|spp\.)\b',    # Genus sp./spp.
        ]
        unique_taxa = set()
        for p in taxon_patterns:
            unique_taxa.update(re.findall(p, content))
        metrics['taxonomic_specificity'] = len(unique_taxa)

        # Ecological relevance terms
        metrics['conservation_focus']    = sum(cl.count(t) for t in V['conservation_terms'])
        metrics['climate_relevance']     = sum(cl.count(t) for t in V['climate_terms'])
        metrics['ecological_complexity'] = sum(cl.count(t) for t in V['complexity_terms'])

    def domain_calculate_quality_scores(self, m: dict):
        V = self.vocab
        wc = m['word_count']
        denom = {
            'mech': max(1, len(V['mechanistic_terms'])),
            'causal': max(1, len(V['causal_terms'])),
            'regions': max(1, len(V['regions'])),
            'interventions': max(1, len(V['interventions'])),
            'diversity': max(1, len(V['diversity_dimensions'])),
            'services': max(1, len(V['ecosystem_services'])),
            'scales': max(1, len(V['scale_terms'])),
        }

        # Depth: harmonic mean of mechanistic coverage, causal coverage, temporal precision
        mech_cov = safe_div(m['mechanistic_detail'],  denom['mech'])
        caus_cov = safe_div(m['causal_explanations'], denom['causal'])
        temp_prec = float(m.get('temporal_precision', 0.0))
        depth = hmean([mech_cov, caus_cov, temp_prec], [0.4, 0.3, 0.3])

        # Breadth: improved — harmonic mean to penalize imbalance across components
        b_parts = np.array([
            safe_div(m['geographic_regions'],   denom['regions']),
            safe_div(m['intervention_types'],   denom['interventions']),
            safe_div(m['diversity_dimensions'], denom['diversity']),
            safe_div(m['ecosystem_services'],   denom['services']),
            safe_div(m['spatial_scales'],       denom['scales']),
        ], dtype=float)
        b_weights = np.array([0.25, 0.25, 0.25, 0.15, 0.10], dtype=float)
        breadth = hmean(b_parts, b_weights)

        # Rigor
        rigor = (
            min(m.get('statistical_rigor', 0)/5.0,  1.0) * 0.4 +
            min(m.get('formal_citations', 0)/20.0,  1.0) * 0.4 +
            min(m.get('uncertainty_acknowledgment', 0)/5.0, 1.0) * 0.2
        )

        # Innovation
        innovation = (
            min(m.get('speculative_ideas', 0)/3.0,      1.0) * 0.4 +
            min(m.get('innovation_indicators', 0)/3.0,  1.0) * 0.3 +
            min(m.get('research_gaps', 0)/3.0,          1.0) * 0.3
        )

        # Info density: improved — smooth saturating curve (avoid early 1.0 plateau)
        info_per_k = safe_div(m['source_count'], wc/1000.0)
        info_density = 1.0 - np.exp(-info_per_k / 40.0)  # gradually approaches 1.0

        # Taxonomic specificity: improved ceiling to avoid trivial saturation
        taxonomic = min(m.get('taxonomic_specificity', 0) / 40.0, 1.0)

        # Ecological relevance
        ecological = (
            min(m.get('conservation_focus', 0)/8.0, 1.0) * 0.4 +
            min(m.get('climate_relevance', 0)/6.0, 1.0) * 0.3 +
            min(m.get('ecological_complexity', 0)/5.0, 1.0) * 0.3
        )

        w = self.domain_weights()
        overall = (
            depth*w.depth + breadth*w.breadth + rigor*w.rigor + innovation*w.innovation +
            ecological*w.domain_specific + info_density*w.info_density + taxonomic*w.taxonomic_or_specificity
        )

        m.update({
            'depth_score': depth,
            'breadth_score': breadth,
            'rigor_score': rigor,
            'innovation_score': innovation,
            'ecological_relevance': ecological,
            'info_density': info_density,
            'taxonomic_score': taxonomic,
            'overall_quality': overall
        })

    def domain_publication_plots(self, statistics_file, all_results, figures_dir):
        """
        Ecology keeps the paper-specific plots AND (implicitly) remains comparable to NLP,
        since filenames are the same. (NLP uses the base common plots with same filenames.)
        """
        create_main_scaling_plot(statistics_file, figures_dir)
        create_parameter_effects_plot(statistics_file, figures_dir)
        create_optimization_analysis_plot(all_results, figures_dir)
        create_quality_dimensions_plot(all_results, figures_dir)
        create_overall_quality_analysis(all_results, figures_dir)


# ---------------------------
# NLP Analyzer
# ---------------------------

class NLPAnalyzer(BaseResearchAnalyzer):
    """NLP domain with external JSON vocab and comparable plots."""

    def build_vocab(self):
        path = _default_vocab_path('nlp')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def domain_weights(self) -> QualityWeights:
        # Slightly higher rigor & domain-specific (repro/safety) for NLP,
        # slightly lower weight on "specificity" proxy.
        return QualityWeights(
            depth=0.22, breadth=0.20, rigor=0.22, innovation=0.14,
            domain_specific=0.12, info_density=0.06, taxonomic_or_specificity=0.04
        )

    def domain_extract_metrics(self, content: str, metrics: dict):
        cl = content.lower(); V = self.vocab
        metrics['nlp_tasks_cov']    = unique_phrase_hits(content, V['tasks'])
        metrics['nlp_datasets_cov'] = unique_phrase_hits(content, V['datasets'])
        metrics['nlp_langs_cov']    = unique_phrase_hits(content, V['languages'])
        metrics['nlp_eval_cov']     = unique_phrase_hits(content, V['eval_metrics'])

        metrics['nlp_arch_detail']  = unique_phrase_hits(content, V['arch_terms'])
        metrics['nlp_train_detail'] = unique_phrase_hits(content, V['training_terms'])
        metrics['nlp_ablation']     = unique_phrase_hits(content, V['ablation_terms'])

        metrics['nlp_rigor_stats']  = sum(cl.count(t) for t in V['rigor_stats'])
        metrics['nlp_repro']        = unique_phrase_hits(content, V['repro_terms'])
        metrics['nlp_safety']       = unique_phrase_hits(content, V['safety_terms'])
        metrics['nlp_reporting']    = unique_phrase_hits(content, V['compute_terms'])

        # No temporal precision emphasis in typical NLP reports
        metrics['temporal_precision'] = 0.0

    def domain_calculate_quality_scores(self, m: dict):
        V = self.vocab; wc = m['word_count']
        denom = {
            'tasks':     max(1, len(V['tasks'])),
            'datasets':  max(1, len(V['datasets'])),
            'langs':     max(1, len(V['languages'])),
            'eval':      max(1, len(V['eval_metrics'])),
            'arch':      max(1, len(V['arch_terms'])),
            'train':     max(1, len(V['training_terms'])),
            'ablation':  max(1, len(V['ablation_terms'])),
        }

        arch_cov  = safe_div(m['nlp_arch_detail'],  denom['arch'])
        train_cov = safe_div(m['nlp_train_detail'], denom['train'])
        abl_cov   = safe_div(m['nlp_ablation'],     denom['ablation'])
        depth = hmean([arch_cov, train_cov, abl_cov], [0.4, 0.4, 0.2])

        breadth = (
            safe_div(m['nlp_tasks_cov'],    denom['tasks'])    * 0.30 +
            safe_div(m['nlp_datasets_cov'], denom['datasets']) * 0.30 +
            safe_div(m['nlp_langs_cov'],    denom['langs'])    * 0.20 +
            safe_div(m['nlp_eval_cov'],     denom['eval'])     * 0.20
        )

        rigor = (
            min(m.get('nlp_rigor_stats', 0) / 5.0, 1.0) * 0.7 +
            min(m.get('formal_citations', 0) / 20.0, 1.0) * 0.3
        )

        innovation = (
            min(m.get('percentage_values', 0) / 15.0, 1.0) * 0.15 +
            min(m.get('nlp_ablation', 0) / 3.0, 1.0)       * 0.25 +
            min(safe_div(m.get('source_count',0), wc/1000.0) / 30.0, 1.0) * 0.10 +
            min(arch_cov,  1.0) * 0.25 +
            min(train_cov, 1.0) * 0.25
        )

        domain_specific = (
            min(m.get('nlp_repro',  0) / 6.0, 1.0) * 0.6 +
            min(m.get('nlp_safety', 0) / 6.0, 1.0) * 0.4
        )

        info_density = min(safe_div(m['source_count'], wc/1000.0)/40.0, 1.0)
        reporting_specificity = min(m.get('nlp_reporting', 0) / 10.0, 1.0)

        w = self.domain_weights()
        overall = (
            depth*w.depth + breadth*w.breadth + rigor*w.rigor + innovation*w.innovation +
            domain_specific*w.domain_specific + info_density*w.info_density +
            reporting_specificity*w.taxonomic_or_specificity
        )

        m.update({
            'depth_score': depth,
            'breadth_score': breadth,
            'rigor_score': rigor,
            'innovation_score': innovation,
            'repro_safety_score': domain_specific,
            'info_density': info_density,
            'reporting_specificity': reporting_specificity,
            'overall_quality': overall
        })

    def domain_publication_plots(self, statistics_file, all_results, figures_dir):
        """
        NLP produces the SAME 4 key figures (same filenames) via the common generator,
        ensuring comparability with Ecology outputs.
        """
        self.create_common_publication_plots(statistics_file, all_results, figures_dir)


# ---------------------------
# Analyzer selector / alias for pipeline compatibility
# ---------------------------

def get_analyzer():
    if str(topic).lower().strip() == 'nlp':
        return NLPAnalyzer()
    # default
    return EcologyAnalyzer()

# Backward compatibility for existing pipelines:
DeepResearchAnalyzer = NLPAnalyzer if str(topic).lower().strip() == 'nlp' else EcologyAnalyzer
