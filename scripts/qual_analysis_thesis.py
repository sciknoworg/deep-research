import os
import pandas as pd

from research_analyzer import EcologyAnalyzer, NLPAnalyzer
from utils import depth_breadth_filename_patterns, topic, model_and_search_pattern

REPORT_DIR = '../data/nlp-reports/orkg-ask/o3'
OUTPUT_DIR = f'docs_thesis_{topic}_{model_and_search_pattern}'
FIGURES_DIR = os.path.join(OUTPUT_DIR, 'figures')
STATISTICS_FILE = os.path.join(OUTPUT_DIR, 'comprehensive_summary_statistics.csv')


def _get_analyzer():
    """Wählt den passenden Analyzer je nach utils.topic ('ecology' | 'nlp')."""
    if str(topic).lower() == 'nlp':
        return NLPAnalyzer()
    return EcologyAnalyzer()


def run_comprehensive_analysis(report_dir=REPORT_DIR, output_dir=OUTPUT_DIR, sample_size=50):
    """
    Läuft die komplette Auswertung (laden -> analysieren -> Plots -> Reports).
    """
    print("🔬 Starting Enhanced Research Analysis...")

    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

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

    print("📝 Writing enhanced report and paper summary...")
    generate_enhanced_report(all_results, output_dir)
    create_paper_summary(all_results, output_dir)

    print("✅ Analysis complete!")
    print(f"📁 Results saved in: {output_dir}/")
    print(f"🖼️ Figures saved in: {FIGURES_DIR}/")
    return all_results


def _ensure_depth_breadth_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Extrahiert depth & breadth aus 'config', falls nicht vorhanden."""
    if 'depth' not in df.columns and 'config' in df.columns:
        df['depth'] = df['config'].str.extract(r'd(\d+)').astype(int)
    if 'breadth' not in df.columns and 'config' in df.columns:
        df['breadth'] = df['config'].str.extract(r'b(\d+)').astype(int)
    return df


def generate_enhanced_report(all_results: dict, output_dir: str):
    """
    Ausführlicher Markdown-Report mit Konfig-Vergleich, Key Findings
    und Domain-Abschnitten (Ecology oder NLP).
    """
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df = _ensure_depth_breadth_cols(combined_df)

    lines = []
    lines.append("# Enhanced Deep Research Quality Analysis")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"**Domain:** {topic}  •  **Model/Search tag:** {model_and_search_pattern}")
    lines.append("")

    # Overview
    total_docs = len(combined_df)
    total_questions = len(all_results)
    lines.append("## Overview")
    lines.append(f"- Total documents analyzed: **{total_docs}**")
    lines.append(f"- Questions analyzed: **{total_questions}**")
    lines.append(f"- Configurations per question: **{len(depth_breadth_filename_patterns)}** (" +
                 ", ".join(depth_breadth_filename_patterns) + ")")
    lines.append("")

    # Configuration Performance
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

        if 'geographic_regions' in cdf:       lines.append(f"- 🌍 Geographic regions: {cdf['geographic_regions'].mean():.1f}")
        if 'mechanistic_detail' in cdf:       lines.append(f"- 🔬 Mechanistic detail: {cdf['mechanistic_detail'].mean():.1f}")
        if 'diversity_dimensions' in cdf:     lines.append(f"- 🌿 Diversity dimensions: {cdf['diversity_dimensions'].mean():.1f}")
        if 'ecosystem_services' in cdf:       lines.append(f"- 🏞️ Ecosystem services: {cdf['ecosystem_services'].mean():.1f}")
        if 'spatial_scales' in cdf:           lines.append(f"- 📏 Spatial scales: {cdf['spatial_scales'].mean():.1f}")
        if 'conservation_focus' in cdf:       lines.append(f"- 🛡️ Conservation focus: {cdf['conservation_focus'].mean():.1f}")
        if 'climate_relevance' in cdf:        lines.append(f"- 🌡️ Climate relevance: {cdf['climate_relevance'].mean():.1f}")

        if 'nlp_tasks_cov' in cdf:            lines.append(f"- 🔤 Tasks coverage: {cdf['nlp_tasks_cov'].mean():.1f}")
        if 'nlp_datasets_cov' in cdf:         lines.append(f"- 🧪 Datasets coverage: {cdf['nlp_datasets_cov'].mean():.1f}")
        if 'nlp_langs_cov' in cdf:            lines.append(f"- 🌐 Languages coverage: {cdf['nlp_langs_cov'].mean():.1f}")
        if 'nlp_eval_cov' in cdf:             lines.append(f"- 🧮 Eval metrics coverage: {cdf['nlp_eval_cov'].mean():.1f}")
        if 'nlp_arch_detail' in cdf:          lines.append(f"- 🧩 Architecture detail: {cdf['nlp_arch_detail'].mean():.1f}")
        if 'nlp_train_detail' in cdf:         lines.append(f"- 🏗️ Training detail: {cdf['nlp_train_detail'].mean():.1f}")
        if 'nlp_ablation' in cdf:             lines.append(f"- ✂️ Ablations (coverage): {cdf['nlp_ablation'].mean():.1f}")
        if 'nlp_repro' in cdf:                lines.append(f"- ♻️ Reproducibility (signals): {cdf['nlp_repro'].mean():.1f}")
        if 'nlp_safety' in cdf:               lines.append(f"- 🛡️ Safety (signals): {cdf['nlp_safety'].mean():.1f}")

        lines.append(f"- ⭐ Overall quality: {_a('overall_quality')}")
        lines.append(f"- 🎯 Research depth: {_a('depth_score')}")
        lines.append(f"- 🌐 Research breadth: {_a('breadth_score')}")
        lines.append(f"- 🔬 Scientific rigor: {_a('rigor_score')}")
        lines.append(f"- 💡 Innovation: {_a('innovation_score')}")
        if 'ecological_relevance' in cdf:     lines.append(f"- 🌿 Ecological relevance: {_a('ecological_relevance')}")
        if 'info_density' in cdf:             lines.append(f"- 📊 Information density: {_a('info_density')}")
        if 'taxonomic_score' in cdf:          lines.append(f"- 🧬 Taxonomic specificity: {_a('taxonomic_score')}")
        if 'repro_safety_score' in cdf:       lines.append(f"- ♻️🛡️ Repro & Safety: {_a('repro_safety_score')}")
        if 'reporting_specificity' in cdf:    lines.append(f"- 🧾 Reporting specificity: {_a('reporting_specificity')}")

    lines.append("\n## 🔍 Key Findings")
    if {'source_count','word_count','config'}.issubset(combined_df.columns):
        d1b1_sources = combined_df[combined_df['config'] == 'd1_b1']['source_count'].mean()
        d4b4_sources = combined_df[combined_df['config'] == 'd4_b4']['source_count'].mean()
        d1b1_words = combined_df[combined_df['config'] == 'd1_b1']['word_count'].mean()
        d4b4_words = combined_df[combined_df['config'] == 'd4_b4']['word_count'].mean()
        scaling_factor = (d4b4_sources / d1b1_sources) if d1b1_sources > 0 else 0
        word_scaling = (d4b4_words / d1b1_words) if d1b1_words > 0 else 0
        lines.append(f"1. 📈 **Source Scaling**: d4_b4 uses {scaling_factor:.1f}× more sources than d1_b1")
        lines.append(f"2. 📝 **Content Scaling**: d4_b4 has {word_scaling:.1f}× more words than d1_b1")

        depth_1_avg = combined_df[combined_df['depth'] == 1]['source_count'].mean()
        depth_4_avg = combined_df[combined_df['depth'] == 4]['source_count'].mean()
        breadth_1_avg = combined_df[combined_df['breadth'] == 1]['source_count'].mean()
        breadth_4_avg = combined_df[combined_df['breadth'] == 4]['source_count'].mean()
        pct = lambda a, b: ((b - a) / a * 100) if a > 0 else 0
        lines.append(f"3. 🔄 **Depth Effect**: +{pct(depth_1_avg, depth_4_avg):.0f}% in source utilization")
        lines.append(f"4. 🌐 **Breadth Effect**: +{pct(breadth_1_avg, breadth_4_avg):.0f}% in source utilization")

    if topic == 'ecology':
        ecology_metrics = ['ecosystem_services','conservation_focus','climate_relevance','ecological_complexity','spatial_scales']
        available = [m for m in ecology_metrics if m in combined_df.columns]
        if available:
            lines.append("\n## 🌿 Ecology-Specific Insights")
            for metric in available:
                best_cfg = combined_df.groupby('config')[metric].mean().idxmax()
                best_val = combined_df.groupby('config')[metric].mean().max()
                lines.append(f"- **{metric.replace('_',' ').title()}** best in {best_cfg} ({best_val:.1f})")
    else:
        nlp_metrics = ['nlp_tasks_cov','nlp_datasets_cov','nlp_langs_cov','nlp_eval_cov','nlp_arch_detail','nlp_train_detail','nlp_ablation','nlp_repro','nlp_safety']
        available = [m for m in nlp_metrics if m in combined_df.columns]
        if available:
            lines.append("\n## 🤖 NLP-Specific Insights")
            for metric in available:
                best_cfg = combined_df.groupby('config')[metric].mean().idxmax()
                best_val = combined_df.groupby('config')[metric].mean().max()
                lines.append(f"- **{metric.replace('_',' ').title()}** best in {best_cfg} ({best_val:.1f})")

    lines.append("\n## 🔬 Methodological Notes")
    lines.append("- Multi-dimensional scoring (Depth, Breadth, Rigor, Innovation, Domain-specific, Info density, Specificity)")
    if topic == 'ecology':
        lines.append("- Domain-specific = ecological relevance (conservation, climate, complexity).")
    else:
        lines.append("- Domain-specific = reproducibility & safety signals.")

    with open(os.path.join(output_dir, 'enhanced_analysis_report.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def create_paper_summary(all_results: dict, output_dir: str):
    """Kurze Zusammenfassung für den Paper-Abschnitt."""
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df = _ensure_depth_breadth_cols(combined_df)

    lines = []
    lines.append("# Summary for Paper - Qualitative Results Section")
    lines.append("=" * 60)
    lines.append(f"**Domain:** {topic}  •  **Model/Search tag:** {model_and_search_pattern}")
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
            lines.append(f"- **Source scaling (d4_b4 / d1_b1)**: {source_ratio:.1f}×")
            lines.append(f"- **Word scaling (d4_b4 / d1_b1)**: {word_ratio:.1f}×")


    if 'overall_quality' in combined_df.columns:
        q_by_cfg = combined_df.groupby('config')['overall_quality'].mean()
        best_cfg = q_by_cfg.idxmax()
        q_range = q_by_cfg.max() - q_by_cfg.min()
        lines.append("")
        lines.append(f"- **Highest quality configuration**: {best_cfg} ({q_by_cfg[best_cfg]:.3f})")
        lines.append(f"- **Quality range across configurations**: {q_range:.3f}")
        if 'source_count' in combined_df.columns:
            eff = combined_df.groupby('config').apply(
                lambda x: x['overall_quality'].mean() / x['source_count'].mean() if x['source_count'].mean() > 0 else 0
            )
            most_efficient = eff.idxmax()
            lines.append(f"- **Most efficient configuration**: {most_efficient} ({eff[most_efficient]:.4f} quality/source)")

    with open(os.path.join(output_dir, 'paper_summary.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    results = run_comprehensive_analysis(sample_size=50)

    print("\n🎉 Enhanced analysis complete!")
    print("Generated files:")
    print(" - enhanced_analysis_report.md")
    print(" - paper_summary.md")
    print(" - figures/main_scaling_effects.png")
    print(" - figures/parameter_effects.png")
    print(" - figures/quality_dimensions.png")
    print(" - figures/optimization_analysis.png")
    print(" - comprehensive_summary_statistics.csv")
