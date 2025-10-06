

"""
qual_analysis_thesis.py

Batch-run the arithmetic-only quality scoring (research_analyzer.py)
over a directory of markdown reports grouped by question and d/b config.

Outputs
-------
- figures/main_scaling_effects.png
- figures/parameter_effects.png
- figures/quality_dimensions.png
- figures/optimization_analysis.png
- comprehensive_summary_statistics.csv
- enhanced_analysis_report.md
- paper_summary.md
"""

import os
import pandas as pd

from research_analyzer import (
    EcologyAnalyzer, NLPAnalyzer, ScoringConfig, get_analyzer
)
from utils import depth_breadth_filename_patterns, topic, model_and_search_pattern

# Publication figures come from helper modules imported inside research_analyzer
from research_analyzer import (
    create_main_scaling_plot, create_parameter_effects_plot,
    create_optimization_analysis_plot, create_quality_dimensions_plot,
    create_overall_quality_analysis
)

_model_root = 'o3-mini' if 'o3-mini' in str(model_and_search_pattern) else 'o3'
REPORT_DIR = f'../data/{topic}-reports/orkg-ask/{_model_root}'

# Optional suffix to label multiple runs on same config (e.g., "_wtestA")
OUTPUT_SUFFIX = "_main"  # <-- set e.g. "_alphaA" or "_debug1"

OUTPUT_DIR = f"docs_thesis_{topic}_{model_and_search_pattern}{OUTPUT_SUFFIX}"
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
STATISTICS_FILE = os.path.join(OUTPUT_DIR, 'comprehensive_summary_statistics.csv')


def _get_analyzer():
    """
    Analyzer with density cap only. Composite weights & part-weights come from vocab JSON.
    """
    cfg = ScoringConfig(
        density_per_k_cap=50.0,   # InfoDensity cap (stored but not in overall)
        weights=None               # <- tell analyzer to use vocab["weights"]["alpha"]
    )
    return get_analyzer(cfg)


def run_comprehensive_analysis(report_dir=REPORT_DIR, output_dir=OUTPUT_DIR, sample_size=50):
    print("🔬 Starting Research Quality Analysis...")

    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Discover questions: filenames "<QID>_<modeltag>_dX_bY.md"
    available_files = [f for f in os.listdir(report_dir) if f.endswith('.md')]
    question_numbers = sorted(list({f.split('_')[0] for f in available_files}))
    if sample_size:
        question_numbers = question_numbers[:sample_size]

    print(f"📊 Analyzing {len(question_numbers)} questions...")

    analyzer = _get_analyzer()
    all_results = analyzer.analyze_multiple_questions(report_dir, question_numbers, output_dir)
    if not all_results:
        print("❌ No results generated. Check data directory and file paths.")
        return

    print("📈 Generating publication-ready figures...")
    analyzer.domain_publication_plots(STATISTICS_FILE, all_results, FIGURES_DIR)

    print("📝 Writing reports...")
    generate_enhanced_report(all_results, output_dir)
    create_paper_summary(all_results, output_dir)

    print("✅ Analysis complete!")
    print(f"📁 Results: {output_dir}/")
    print(f"🖼️ Figures: {FIGURES_DIR}/")
    return all_results


def _ensure_depth_breadth_cols(df: pd.DataFrame) -> pd.DataFrame:
    if 'depth' not in df.columns and 'config' in df.columns:
        df['depth'] = df['config'].str.extract(r'd(\d+)').astype(int)
    if 'breadth' not in df.columns and 'config' in df.columns:
        df['breadth'] = df['config'].str.extract(r'b(\d+)').astype(int)
    return df


def generate_enhanced_report(all_results: dict, output_dir: str):
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df = _ensure_depth_breadth_cols(combined_df)

    lines = []
    lines.append("# Research Quality Analysis (Arithmetic)")
    lines.append("=" * 60)
    lines.append(f"**Domain:** {topic}  •  **Model/Search tag:** {model_and_search_pattern}{OUTPUT_SUFFIX}")
    lines.append("")

    total_docs = len(combined_df)
    total_questions = len(all_results)
    lines.append("## Overview")
    lines.append(f"- Total documents analyzed: **{total_docs}**")
    lines.append(f"- Questions analyzed: **{total_questions}**")
    lines.append(f"- Configurations per question: **{len(depth_breadth_filename_patterns)}** (" +
                 ", ".join(depth_breadth_filename_patterns) + ")")
    lines.append("")

    lines.append("## Configuration Performance")
    for config in depth_breadth_filename_patterns:
        cdf = combined_df[combined_df['config'] == config]
        if len(cdf) == 0:
            continue

        lines.append(f"\n### {config}")

        def _m(name):
            return f"{cdf[name].mean():.1f} ± {cdf[name].std():.1f}" if name in cdf.columns else "n/a"

        def _a(name):
            return f"{cdf[name].mean():.3f}" if name in cdf.columns else "n/a"

        lines.append(f"- 📚 Sources: {_m('source_count')}")
        lines.append(f"- 📝 Words: {cdf['word_count'].mean():.0f} ± {cdf['word_count'].std():.0f}")

        for col, label in [
            ('breadth_regions_cov', "🌍 Regions coverage"),
            ('breadth_interventions_cov', "🧪 Interventions coverage"),
            ('breadth_diversity_cov', "🌿 Diversity coverage"),
            ('breadth_services_cov', "🏞️ Services coverage"),
            ('breadth_scales_cov', "📏 Scales coverage"),
            ('breadth_tasks_cov', "🧭 Tasks coverage"),
            ('breadth_datasets_cov', "🗃️ Datasets coverage"),
            ('breadth_languages_cov', "🗣️ Languages coverage"),
            ('breadth_metrics_cov', "📊 Eval metrics coverage"),
            ('breadth_compute_cov', "🖥️ Compute terms coverage"),
            ('depth_mechanistic_cov', "🔬 Mechanistic coverage"),
            ('depth_causal_cov', "🔗 Causal coverage"),
            ('depth_temp_precision', "⏱️ Temporal precision"),
            ('rigor_stats_cov', "📐 Stats rigor coverage"),
            ('rigor_uncertainty_cov', "❓ Uncertainty coverage"),
            ('innovation_speculative', "💭 Speculative signals"),
            ('innovation_terms_cov', "💡 Innovation terms coverage"),
            ('gap_score', "🧩 Gap score"),
        ]:
            if col in cdf:
                lines.append(f"- {label}: {cdf[col].mean():.2f}")

        lines.append(f"- ⭐ Overall quality: {_a('overall_quality')}")
        lines.append(f"- 🎯 Depth: {_a('depth_score')}")
        lines.append(f"- 🌐 Breadth: {_a('breadth_score')}")
        lines.append(f"- 🔬 Rigor: {_a('rigor_score')}")
        lines.append(f"- 💡 Innovation: {_a('innovation_score')}")
        lines.append(f"- 🧩 Gaps: {_a('gap_score')}")
        if 'info_density' in cdf:
            lines.append(f"- 📊 Info density: {_a('info_density')}")

    lines.append("\n## 🔍 Key Findings")
    if {'source_count','word_count','config'}.issubset(combined_df.columns):
        d1b1_sources = combined_df[combined_df['config'] == 'd1_b1']['source_count'].mean()
        d4b4_sources = combined_df[combined_df['config'] == 'd4_b4']['source_count'].mean()
        d1b1_words   = combined_df[combined_df['config'] == 'd1_b1']['word_count'].mean()
        d4b4_words   = combined_df[combined_df['config'] == 'd4_b4']['word_count'].mean()
        scaling_factor = (d4b4_sources / d1b1_sources) if d1b1_sources > 0 else 0
        word_scaling   = (d4b4_words / d1b1_words) if d1b1_words > 0 else 0
        lines.append(f"1. 📈 Source scaling: d4_b4 uses {scaling_factor:.1f}× more sources than d1_b1.")
        lines.append(f"2. 📝 Content scaling: d4_b4 has {word_scaling:.1f}× more words than d1_b1.")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'enhanced_analysis_report.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def create_paper_summary(all_results: dict, output_dir: str):
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df = _ensure_depth_breadth_cols(combined_df)

    lines = []
    lines.append("# Paper Summary — Qualitative Results")
    lines.append("=" * 60)
    lines.append(f"**Domain:** {topic}  •  **Model/Search tag:** {model_and_search_pattern}{OUTPUT_SUFFIX}")
    lines.append("")

    lines.append("## Key Statistics per Configuration")
    for config in depth_breadth_filename_patterns:
        cdf = combined_df[combined_df['config'] == config]
        if len(cdf) == 0:
            continue
        src_m = cdf['source_count'].mean() if 'source_count' in cdf else float('nan')
        src_s = cdf['source_count'].std() if 'source_count' in cdf else float('nan')
        w_m = cdf['word_count'].mean() if 'word_count' in cdf else float('nan')
        lines.append(f"- **{config}**: {src_m:.1f} ± {src_s:.1f} sources, {w_m:.0f} words")

    if {'source_count','word_count','config'}.issubset(combined_df.columns):
        d1b1 = combined_df[combined_df['config'] == 'd1_b1']
        d4b4 = combined_df[combined_df['config'] == 'd4_b4']
        if len(d1b1) > 0 and len(d4b4) > 0:
            source_ratio = d4b4['source_count'].mean() / d1b1['source_count'].mean() if d1b1['source_count'].mean() > 0 else 0
            word_ratio = d4b4['word_count'].mean() / d1b1['word_count'].mean() if d1b1['word_count'].mean() > 0 else 0
            lines.append("")
            lines.append(f"- Source scaling (d4_b4 / d1_b1): {source_ratio:.1f}×")
            lines.append(f"- Word scaling (d4_b4 / d1_b1): {word_ratio:.1f}×")

    if 'overall_quality' in combined_df.columns:
        q_by_cfg = combined_df.groupby('config')['overall_quality'].mean()
        best_cfg = q_by_cfg.idxmax()
        q_range = q_by_cfg.max() - q_by_cfg.min()
        lines.append("")
        lines.append(f"- Highest quality configuration: {best_cfg} ({q_by_cfg[best_cfg]:.3f})")
        lines.append(f"- Quality range across configurations: {q_range:.3f}")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'paper_summary.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    results = run_comprehensive_analysis(sample_size=50)

    print("\n🎉 Done!")
    print("Generated files:")
    print(" - enhanced_analysis_report.md")
    print(" - paper_summary.md")
    print(" - figures/main_scaling_effects.png")
    print(" - figures/parameter_effects.png")
    print(" - figures/quality_dimensions.png")
    print(" - figures/optimization_analysis.png")
    print(" - comprehensive_summary_statistics.csv")

