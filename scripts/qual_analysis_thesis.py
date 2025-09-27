"""
qual_analysis_thesis.py

Purpose
-------
Batch-run the simplified, arithmetic-only quality scoring (see research_analyzer.py)
over a directory of markdown reports (grouped by question and depth/breadth config),
then emit:

- Publication-ready figures (scaling, parameter effects, quality decomposition, cost-quality).
- A concise Markdown report that summarizes per-configuration stats.
- A short paper-summary file with key numbers per configuration.
- A CSV with comprehensive summary statistics (consumed by your plot helpers).

What this file DOES NOT do
--------------------------
- It does not define the scoring logic (that lives in research_analyzer.py).
- It does not add citations/taxonomy/harmonic aggregation (the scorer excludes them).
- It does not alter your existing plotting modules — we call them unchanged.

Where to tweak
--------------
- REPORT_DIR to point to ecology or nlp runs (utils.topic decides the Analyzer class).
- _get_analyzer() to adjust weights or the density_per_k_cap if needed.
"""

import os
import pandas as pd

from research_analyzer import (
    EcologyAnalyzer, NLPAnalyzer, ScoringConfig, QualityWeights, get_analyzer
)
from utils import depth_breadth_filename_patterns, topic, model_and_search_pattern

# Publication figures are provided by research_analyzer's plotting helpers (unchanged)
from research_analyzer import (
    create_main_scaling_plot, create_parameter_effects_plot,
    create_optimization_analysis_plot, create_quality_dimensions_plot,
    create_overall_quality_analysis
)

# ----- CHANGE THIS PATH when switching between domains -----
# NOTE: utils.topic controls which Analyzer class is instantiated,
# but REPORT_DIR must still point to the directory containing the generated .md files.
# Example for NLP:
REPORT_DIR = '../data/nlp-reports/orkg-ask/o3-mini'
# Example for Ecology:
# REPORT_DIR = '../data/ecology-reports/orkg-ask/o3'

# Outputs (documents and figures) go under a topic- and model-tagged directory.
OUTPUT_DIR = f'docs_thesis_{topic}_{model_and_search_pattern}'
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
STATISTICS_FILE = os.path.join(OUTPUT_DIR, 'comprehensive_summary_statistics.csv')


def _get_analyzer():
    """
    Build an Analyzer configured for the simplified arithmetic-only score:
      - No citations, no taxonomy, no harmonic aggregation.
      - Only 'density_per_k_cap' (for InfoDensity) and 'weights' matter here.

    density_per_k_cap
      Number of sources per 1k words that saturates the Information Density score to 1.0.
      Example: 50 => 50 sources per 1k words produces info_density = 1.0.

    Weights
      Keep them stable unless you have evidence to change them.
    """
    cfg = ScoringConfig(
        density_per_k_cap=50.0,  # sources per 1k words needed for info_density = 1.0
        weights=QualityWeights(
            depth=0.26,
            breadth=0.24,
            rigor=0.16,
            innovation=0.16,
            domain_specific=0.12,
            # Slightly reward sourcing in the overall score; raw display still shows sources_per_1k
            info_density=0.06,
            taxonomic_or_specificity=0.00
        )
    )

    if str(topic).lower() == 'nlp':
        return NLPAnalyzer(config=cfg)
    return EcologyAnalyzer(config=cfg)


def run_comprehensive_analysis(report_dir=REPORT_DIR, output_dir=OUTPUT_DIR, sample_size=50):
    """
    End-to-end runner:

      1) Scan `report_dir` for .md files and extract question IDs from filenames
         of the form "<QID>_<modeltag>_dX_bY.md".
      2) For each question, try to load all depth/breadth configs (e.g., d1_b1, d4_b4).
      3) Use the Analyzer to parse raw signals and compute scores.
      4) Save quick per-question panels and aggregate figures.
      5) Generate Markdown reports and a summary CSV.

    Returns
    -------
    dict
        Mapping: {question_id -> DataFrame of per-config metrics+scores}.
    """
    print("🔬 Starting Research Quality Analysis...")

    # Make sure folders exist (safe if they already do).
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # Extract question numbers from filenames "<QID>_<modeltag>_dX_bY.md"
    available_files = [f for f in os.listdir(report_dir) if f.endswith('.md')]
    question_numbers = sorted(list({f.split('_')[0] for f in available_files}))

    # Optional downsample to speed up trial runs (e.g., sample_size=10)
    if sample_size:
        question_numbers = question_numbers[:sample_size]

    print(f"📊 Analyzing {len(question_numbers)} questions...")

    analyzer = _get_analyzer()
    all_results = analyzer.analyze_multiple_questions(report_dir, question_numbers, output_dir)
    if not all_results:
        print("❌ No results generated. Check data directory and file paths.")
        return

    # Call the Analyzer's domain-specific figure bundle (filenames are standardized).
    print("📈 Generating publication-ready figures...")
    analyzer.domain_publication_plots(STATISTICS_FILE, all_results, FIGURES_DIR)

    # Lightweight Markdown summaries: "enhanced_analysis_report.md" + "paper_summary.md"
    print("📝 Writing reports...")
    generate_enhanced_report(all_results, output_dir)
    create_paper_summary(all_results, output_dir)

    print("✅ Analysis complete!")
    print(f"📁 Results: {output_dir}/")
    print(f"🖼️ Figures: {FIGURES_DIR}/")
    return all_results


def _ensure_depth_breadth_cols(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure 'depth' and 'breadth' columns are present in the combined results DataFrame.
    We infer them from the 'config' strings like 'd4_b1' if they are missing.
    This is helpful for grouping/pivoting in the reporting functions.
    """
    if 'depth' not in df.columns and 'config' in df.columns:
        df['depth'] = df['config'].str.extract(r'd(\d+)').astype(int)
    if 'breadth' not in df.columns and 'config' in df.columns:
        df['breadth'] = df['config'].str.extract(r'b(\d+)').astype(int)
    return df


def generate_enhanced_report(all_results: dict, output_dir: str):
    """
    Create a concise Markdown report that:
      - Summarizes per-configuration performance across all questions.
      - Prints means (and std) for basic counts.
      - Prints the average sub-dimension coverages (if present).
      - Lists key scaling effects (depth/breadth).
    """
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df = _ensure_depth_breadth_cols(combined_df)

    lines = []
    lines.append("# Research Quality Analysis (Simplified, Arithmetic)")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"**Domain:** {topic}  •  **Model/Search tag:** {model_and_search_pattern}")
    lines.append("")

    # --- Overview (counts) ---
    total_docs = len(combined_df)
    total_questions = len(all_results)
    lines.append("## Overview")
    lines.append(f"- Total documents analyzed: **{total_docs}**")
    lines.append(f"- Questions analyzed: **{total_questions}**")
    lines.append(f"- Configurations per question: **{len(depth_breadth_filename_patterns)}** (" +
                 ", ".join(depth_breadth_filename_patterns) + ")")
    lines.append("")

    # --- Configuration performance blocks ---
    lines.append("## Configuration Performance")
    for config in depth_breadth_filename_patterns:
        cdf = combined_df[combined_df['config'] == config]
        if len(cdf) == 0:
            continue

        lines.append(f"\n### {config}")

        def _m(name):
            """Mean ± std for raw counts (sources/words)."""
            return f"{cdf[name].mean():.1f} ± {cdf[name].std():.1f}" if name in cdf.columns else "n/a"

        def _a(name):
            """Mean only for scores/coverages (already in [0,1])."""
            return f"{cdf[name].mean():.3f}" if name in cdf.columns else "n/a"

        # basic size/sourcing
        lines.append(f"- 📚 Sources: {_m('source_count')}")
        lines.append(f"- 📝 Words: {cdf['word_count'].mean():.0f} ± {cdf['word_count'].std():.0f}")

        # ecology breadth sub-dimensions (printed if present)
        for col, label in [
            ('breadth_regions_cov', "🌍 Regions coverage"),
            ('breadth_interventions_cov', "🧪 Interventions coverage"),
            ('breadth_diversity_cov', "🌿 Diversity coverage"),
            ('breadth_services_cov', "🏞️ Services coverage"),
            ('breadth_scales_cov', "📏 Scales coverage"),
            ('depth_mechanistic_cov', "🔬 Mechanistic coverage"),
            ('depth_causal_cov', "🔗 Causal coverage"),
            ('depth_temp_precision', "⏱️ Temporal precision"),
            ('rigor_stats_cov', "📐 Stats rigor coverage"),
            ('rigor_uncertainty_cov', "❓ Uncertainty coverage"),
            ('innovation_speculative', "💭 Speculative signals"),
            ('innovation_terms_cov', "💡 Innovation terms coverage"),
            ('innovation_gaps', "🧩 Research gaps (signals)"),
            ('ecology_conservation_cov', "🛡️ Conservation coverage"),
            ('ecology_climate_cov', "🌡️ Climate coverage"),
            ('ecology_complexity_cov', "🧠 Complexity coverage"),
            # nlp breadth/domain (if present)
            ('breadth_tasks_cov', "🧭 Tasks coverage"),
            ('breadth_datasets_cov', "🗃️ Datasets coverage"),
            ('breadth_languages_cov', "🗣️ Languages coverage"),
            ('breadth_metrics_cov', "📊 Eval metrics coverage"),
            ('breadth_compute_cov', "🖥️ Compute terms coverage"),
            ('nlp_repro_cov', "🔁 Reproducibility coverage"),
            ('nlp_safety_cov', "⚠️ Safety coverage"),
            ('nlp_compute_cov', "🖥️ Compute (domain) coverage"),
        ]:
            if col in cdf:
                lines.append(f"- {label}: {cdf[col].mean():.2f}")

        # aggregate scores (all in [0,1])
        lines.append(f"- ⭐ Overall quality: {_a('overall_quality')}")
        lines.append(f"- 🎯 Depth: {_a('depth_score')}")
        lines.append(f"- 🌐 Breadth: {_a('breadth_score')}")
        lines.append(f"- 🔬 Rigor: {_a('rigor_score')}")
        lines.append(f"- 💡 Innovation: {_a('innovation_score')}")
        if 'ecological_relevance' in cdf:      lines.append(f"- 🧭 Domain alignment: {_a('ecological_relevance')}")
        if 'info_density' in cdf:              lines.append(f"- 📊 Info density: {_a('info_density')}")

    # --- Key Findings (simple deltas) ---
    lines.append("\n## 🔍 Key Findings")
    if {'source_count','word_count','config'}.issubset(combined_df.columns):
        d1b1_sources = combined_df[combined_df['config'] == 'd1_b1']['source_count'].mean()
        d4b4_sources = combined_df[combined_df['config'] == 'd4_b4']['source_count'].mean()
        d1b1_words   = combined_df[combined_df['config'] == 'd1_b1']['word_count'].mean()
        d4b4_words   = combined_df[combined_df['config'] == 'd4_b4']['word_count'].mean()
        scaling_factor = (d4b4_sources / d1b1_sources) if d1b1_sources > 0 else 0
        word_scaling   = (d4b4_words / d1b1_words) if d1b1_words > 0 else 0
        lines.append(f"1. 📈 **Source scaling**: d4_b4 uses {scaling_factor:.1f}× more sources than d1_b1.")
        lines.append(f"2. 📝 **Content scaling**: d4_b4 has {word_scaling:.1f}× more words than d1_b1.")

        depth_1_avg = combined_df[combined_df['depth'] == 1]['source_count'].mean()
        depth_4_avg = combined_df[combined_df['depth'] == 4]['source_count'].mean()
        breadth_1_avg = combined_df[combined_df['breadth'] == 1]['source_count'].mean()
        breadth_4_avg = combined_df[combined_df['breadth'] == 4]['source_count'].mean()
        pct = lambda a, b: ((b - a) / a * 100) if a > 0 else 0
        lines.append(f"3. 🔄 **Depth effect**: +{pct(depth_1_avg, depth_4_avg):.0f}% sources.")
        lines.append(f"4. 🌐 **Breadth effect**: +{pct(breadth_1_avg, breadth_4_avg):.0f}% sources.")

    # --- Domain notes ---
    if str(topic).lower() == 'ecology':
        lines.append("\n## 🌿 Ecology-Specific Notes")
        lines.append("- Coverage uses unique-hit ratio vs. dictionary size (no frequency inflation).")
        lines.append("- Rigor excludes citations; focuses on stats lexicon & uncertainty signals.")
        lines.append("- No taxonomy enters the score; prevents correlation with depth/breadth.")
    else:
        lines.append("\n## 🤖 NLP Notes")
        lines.append("- Identical aggregation, weights, and density cap as in Ecology for comparability.")
        lines.append("- Depth uses architecture/training/ablation as mechanistic proxies; Breadth swaps to tasks/datasets/languages/metrics/compute.")
        lines.append("- Domain alignment maps to reproducibility/safety/compute; stored under the same key used by the plotters.")

    # --- Methods summary ---
    lines.append("\n## 🔬 Methodological Notes")
    lines.append("- Arithmetic aggregation only; no harmonic means.")
    lines.append("- Dimensions: Depth, Breadth, Rigor, Innovation, Domain alignment, Info density.")
    lines.append("- Coverage = unique term hits / dictionary size (clipped to [0,1]).")
    lines.append("- CSV also includes the raw `sources_per_1k` used by your density panels.")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'enhanced_analysis_report.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def create_paper_summary(all_results: dict, output_dir: str):
    """
    Produce a compact Markdown summary for the paper:
      - One block of key stats per configuration (sources ± std, words).
      - Scale ratios (d4_b4 / d1_b1).
      - Which config has the highest overall quality, the range, and "quality per source".
    """
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df = _ensure_depth_breadth_cols(combined_df)

    lines = []
    lines.append("# Paper Summary — Qualitative Results")
    lines.append("=" * 60)
    lines.append(f"**Domain:** {topic}  •  **Model/Search tag:** {model_and_search_pattern}")
    lines.append("")

    # Per-configuration headline stats
    lines.append("## Key Statistics per Configuration")
    for config in depth_breadth_filename_patterns:
        cdf = combined_df[combined_df['config'] == config]
        if len(cdf) == 0:
            continue
        src_m = cdf['source_count'].mean() if 'source_count' in cdf else float('nan')
        src_s = cdf['source_count'].std() if 'source_count' in cdf else float('nan')
        w_m = cdf['word_count'].mean() if 'word_count' in cdf else float('nan')
        lines.append(f"- **{config}**: {src_m:.1f} ± {src_s:.1f} sources, {w_m:.0f} words")

    # Simple scale ratios for figure captions
    if {'source_count','word_count','config'}.issubset(combined_df.columns):
        d1b1 = combined_df[combined_df['config'] == 'd1_b1']
        d4b4 = combined_df[combined_df['config'] == 'd4_b4']
        if len(d1b1) > 0 and len(d4b4) > 0:
            source_ratio = d4b4['source_count'].mean() / d1b1['source_count'].mean() if d1b1['source_count'].mean() > 0 else 0
            word_ratio = d4b4['word_count'].mean() / d1b1['word_count'].mean() if d1b1['word_count'].mean() > 0 else 0
            lines.append("")
            lines.append(f"- **Source scaling (d4_b4 / d1_b1)**: {source_ratio:.1f}×")
            lines.append(f"- **Word scaling (d4_b4 / d1_b1)**: {word_ratio:.1f}×")

    # Best average quality and spread across configurations
    if 'overall_quality' in combined_df.columns:
        q_by_cfg = combined_df.groupby('config')['overall_quality'].mean()
        best_cfg = q_by_cfg.idxmax()
        q_range = q_by_cfg.max() - q_by_cfg.min()
        lines.append("")
        lines.append(f"- **Highest quality configuration**: {best_cfg} ({q_by_cfg[best_cfg]:.3f})")
        lines.append(f"- **Quality range across configurations**: {q_range:.3f}")

        # Light "efficiency" proxy: quality per average source
        if 'source_count' in combined_df.columns:
            eff = combined_df.groupby('config').apply(
                lambda x: x['overall_quality'].mean() / (x['source_count'].mean() if x['source_count'].mean() > 0 else 1.0)
            )
            most_efficient = eff.idxmax()
            lines.append(f"- **Most efficient configuration**: {most_efficient} ({eff[most_efficient]:.4f} quality/source)")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'paper_summary.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    # Set sample_size=0 to process ALL questions found in REPORT_DIR.
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
