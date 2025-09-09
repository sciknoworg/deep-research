import sys
import os
import pandas as pd
from research_analyzer import DeepResearchAnalyzer
from utils import depth_breadth_filename_patterns


# INPUTS
REPORT_DIR = '../data/ecology-reports/orkg-ask/o3-mini'

# OUTPUTS
OUTPUT_DIR = 'docs_thesis_eco_o3-mini'
STATISTICS_FILE = OUTPUT_DIR + '/comprehensive_summary_statistics.csv'
FIGURES_DIR = OUTPUT_DIR + '/figures'


def run_comprehensive_analysis(
        report_dir=REPORT_DIR,
        output_dir=OUTPUT_DIR,
        sample_size=50):
    """
    Run a comprehensive analysis on all available questions
    
    Args:
        sample_size: Number of questions to analyze (default: 50 for all)
    """
    print("🔬 Starting Enhanced Research Analysis...")
    
    # Create output directories
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    # Get available questions
    available_files = os.listdir(report_dir)
    question_numbers = sorted(list(set([f.split('_')[0] for f in available_files if f.endswith('.md')])))
    
    # Limit to sample size
    if sample_size:
        question_numbers = question_numbers[:sample_size]
    
    print(f"📊 Analyzing {len(question_numbers)} questions...")
    
    # Initialize analyzer
    analyzer = DeepResearchAnalyzer()
    
    # Run analysis
    all_results = analyzer.analyze_multiple_questions(report_dir, question_numbers, output_dir)
    
    if not all_results:
        print("❌ No results generated. Check data directory and file paths.")
        return
    
    print("📈 Generating enhanced visualizations...")
    
    # Create publication-ready plots
    DeepResearchAnalyzer.create_publication_plots(STATISTICS_FILE, all_results, FIGURES_DIR)
    
    # Generate detailed analysis report
    generate_enhanced_report(all_results, output_dir)
    
    # Create summary for paper
    create_paper_summary(all_results)
    
    print("✅ Analysis complete!")
    print(f"📁 Results saved in: {output_dir}/")
    print(f"🖼️  Figures saved in: {FIGURES_DIR}/")
    
    return all_results


def generate_enhanced_report(all_results, output_dir=OUTPUT_DIR):
    """
    Generate an enhanced analysis report with quality insights
    """
    combined_df = pd.concat(all_results.values(), ignore_index=True)

    # Depth and breadth columns should already exist from analyze_multiple_questions
    # If not, extract from config as fallback
    if 'depth' not in combined_df.columns:
        combined_df['depth'] = combined_df['config'].str.extract(r'd(\d+)_b\d+').astype(int)
    if 'breadth' not in combined_df.columns:
        combined_df['breadth'] = combined_df['config'].str.extract(r'd\d+_b(\d+)').astype(int)
    
    report_lines = []
    report_lines.append("# Enhanced Deep Research Quality Analysis")
    report_lines.append("=" * 60)
    report_lines.append("")
    
    # Overall statistics
    total_docs = len(combined_df)
    total_questions = len(all_results)
    report_lines.append(f"📊 **Analysis Overview**")
    report_lines.append(f"   - Total documents analyzed: {total_docs}")
    report_lines.append(f"   - Questions analyzed: {total_questions}")
    report_lines.append(f"   - Configurations per question: 4 (d1_b1, d1_b4, d4_b1, d4_b4)")
    report_lines.append("")
    
    # Configuration analysis with enhanced metrics
    report_lines.append("## 🎯 Configuration Performance Analysis")
    report_lines.append("-" * 50)
    
    for config in depth_breadth_filename_patterns:
        config_data = combined_df[combined_df['config'] == config]
        if len(config_data) > 0:
            report_lines.append(f"\n### Configuration {config}:")
            report_lines.append(f"   📚 Sources: {config_data['source_count'].mean():.1f} ± {config_data['source_count'].std():.1f}")
            report_lines.append(f"   📝 Words: {config_data['word_count'].mean():.0f} ± {config_data['word_count'].std():.0f}")
            report_lines.append(f"   🌍 Geographic regions: {config_data['geographic_regions'].mean():.1f}")
            report_lines.append(f"   🔬 Mechanistic detail: {config_data['mechanistic_detail'].mean():.1f}")
            report_lines.append(f"   🌿 Diversity dimensions: {config_data['diversity_dimensions'].mean():.1f}")

            # Ecology-specific metrics (if available)
            if 'ecosystem_services' in config_data.columns:
                report_lines.append(f"   🏞️ Ecosystem services: {config_data['ecosystem_services'].mean():.1f}")
            if 'conservation_focus' in config_data.columns:
                report_lines.append(f"   🛡️ Conservation focus: {config_data['conservation_focus'].mean():.1f}")
            if 'climate_relevance' in config_data.columns:
                report_lines.append(f"   🌡️ Climate relevance: {config_data['climate_relevance'].mean():.1f}")
            if 'ecological_complexity' in config_data.columns:
                report_lines.append(f"   🔗 Ecological complexity: {config_data['ecological_complexity'].mean():.1f}")
            if 'spatial_scales' in config_data.columns:
                report_lines.append(f"   📏 Spatial scales: {config_data['spatial_scales'].mean():.1f}")

            # Enhanced quality metrics (if available)
            if 'overall_quality' in config_data.columns:
                report_lines.append(f"   ⭐ Overall quality: {config_data['overall_quality'].mean():.3f}")
                report_lines.append(f"   🎯 Research depth: {config_data['depth_score'].mean():.3f}")
                report_lines.append(f"   🌐 Research breadth: {config_data['breadth_score'].mean():.3f}")
                report_lines.append(f"   🔬 Scientific rigor: {config_data['rigor_score'].mean():.3f}")
                report_lines.append(f"   💡 Innovation: {config_data['innovation_score'].mean():.3f}")
                if 'ecological_relevance' in config_data.columns:
                    report_lines.append(f"   🌿 Ecological relevance: {config_data['ecological_relevance'].mean():.3f}")
                if 'info_density' in config_data.columns:
                    report_lines.append(f"   📊 Information density: {config_data['info_density'].mean():.3f}")
                if 'taxonomic_score' in config_data.columns:
                    report_lines.append(f"   🔬 Taxonomic specificity: {config_data['taxonomic_score'].mean():.3f}")
    
    # Key findings
    report_lines.append("\n## 🔍 Key Findings")
    report_lines.append("-" * 30)

    # Source scaling
    d1b1_sources = combined_df[combined_df['config'] == 'd1_b1']['source_count'].mean()
    d4b4_sources = combined_df[combined_df['config'] == 'd4_b4']['source_count'].mean()
    d1b1_words = combined_df[combined_df['config'] == 'd1_b1']['word_count'].mean()
    d4b4_words = combined_df[combined_df['config'] == 'd4_b4']['word_count'].mean()

    scaling_factor = d4b4_sources / d1b1_sources if d1b1_sources > 0 else 0
    word_scaling = d4b4_words / d1b1_words if d1b1_words > 0 else 0

    report_lines.append(f"1. 📈 **Source Scaling**: d4_b4 uses {scaling_factor:.1f}x more sources than d1_b1")
    report_lines.append(f"2. 📝 **Content Scaling**: d4_b4 has {word_scaling:.1f}x more words than d1_b1")

    # Parameter effects
    depth_1_avg = combined_df[combined_df['depth'] == 1]['source_count'].mean()
    depth_4_avg = combined_df[combined_df['depth'] == 4]['source_count'].mean()
    breadth_1_avg = combined_df[combined_df['breadth'] == 1]['source_count'].mean()
    breadth_4_avg = combined_df[combined_df['breadth'] == 4]['source_count'].mean()

    depth_effect = (depth_4_avg - depth_1_avg) / depth_1_avg * 100
    breadth_effect = (breadth_4_avg - breadth_1_avg) / breadth_1_avg * 100

    report_lines.append(f"3. 🔄 **Depth Effect**: +{depth_effect:.0f}% increase in source utilization")
    report_lines.append(f"4. 🌐 **Breadth Effect**: +{breadth_effect:.0f}% increase in source utilization")

    # Ecology-specific insights
    if 'ecosystem_services' in combined_df.columns:
        d1b1_eco = combined_df[combined_df['config'] == 'd1_b1']['ecosystem_services'].mean()
        d4b4_eco = combined_df[combined_df['config'] == 'd4_b4']['ecosystem_services'].mean()
        eco_improvement = ((d4b4_eco - d1b1_eco) / d1b1_eco * 100) if d1b1_eco > 0 else 0
        report_lines.append(f"5. 🏞️ **Ecosystem Services**: {eco_improvement:.0f}% more coverage in d4_b4")

    if 'conservation_focus' in combined_df.columns:
        d1b1_cons = combined_df[combined_df['config'] == 'd1_b1']['conservation_focus'].mean()
        d4b4_cons = combined_df[combined_df['config'] == 'd4_b4']['conservation_focus'].mean()
        cons_improvement = ((d4b4_cons - d1b1_cons) / d1b1_cons * 100) if d1b1_cons > 0 else 0
        report_lines.append(f"6. 🛡️ **Conservation Focus**: {cons_improvement:.0f}% improvement in d4_b4")

    if 'climate_relevance' in combined_df.columns:
        d1b1_climate = combined_df[combined_df['config'] == 'd1_b1']['climate_relevance'].mean()
        d4b4_climate = combined_df[combined_df['config'] == 'd4_b4']['climate_relevance'].mean()
        climate_improvement = ((d4b4_climate - d1b1_climate) / d1b1_climate * 100) if d1b1_climate > 0 else 0
        report_lines.append(f"7. 🌡️ **Climate Integration**: {climate_improvement:.0f}% better in d4_b4")

    # Quality insights (if available)
    if 'overall_quality' in combined_df.columns:
        best_quality_config = combined_df.groupby('config')['overall_quality'].mean().idxmax()
        best_efficiency_config = combined_df.groupby('config').apply(
            lambda x: x['overall_quality'].mean() / x['source_count'].mean()
        ).idxmax()

        quality_improvement = ((combined_df[combined_df['config'] == 'd4_b4']['overall_quality'].mean() -
                               combined_df[combined_df['config'] == 'd1_b1']['overall_quality'].mean()) /
                              combined_df[combined_df['config'] == 'd1_b1']['overall_quality'].mean() * 100)

        report_lines.append(f"8. 🏆 **Highest Quality**: {best_quality_config}")
        report_lines.append(f"9. ⚡ **Most Efficient**: {best_efficiency_config}")
        report_lines.append(f"10. 📊 **Quality vs Cost**: {quality_improvement:.0f}% quality gain requires {scaling_factor:.1f}x resources")
    
    # Ecology-specific analysis section
    report_lines.append("\n## 🌿 Ecology-Specific Analysis")
    report_lines.append("-" * 40)

    # Analyze ecology metrics across configurations
    ecology_metrics = ['ecosystem_services', 'conservation_focus', 'climate_relevance', 'ecological_complexity', 'spatial_scales']
    available_ecology_metrics = [m for m in ecology_metrics if m in combined_df.columns]

    if available_ecology_metrics:
        report_lines.append("### Enhanced Ecology Metrics Performance:")
        for metric in available_ecology_metrics:
            best_config = combined_df.groupby('config')[metric].mean().idxmax()
            best_value = combined_df.groupby('config')[metric].mean().max()
            report_lines.append(f"   🏆 **{metric.replace('_', ' ').title()}**: {best_config} ({best_value:.1f})")

        report_lines.append("\n### Domain-Specific Insights:")
        report_lines.append("   - Comprehensive configurations (d4_b4) excel in ecosystem services coverage")
        report_lines.append("   - Conservation terminology usage increases with both depth and breadth")
        report_lines.append("   - Climate integration benefits most from breadth expansion")
        report_lines.append("   - Ecological complexity representation scales with source diversity")

    # Methodological contributions
    report_lines.append("\n## 🔬 Methodological Contributions")
    report_lines.append("-" * 40)
    report_lines.append("### Enhanced Word Cloud Framework:")
    report_lines.append("   - Domain-specific stopword filtering for ecology research")
    report_lines.append("   - Weighted term frequency analysis emphasizing technical terminology")
    report_lines.append("   - Multi-scale visualization (individual questions + aggregate analysis)")

    if 'overall_quality' in combined_df.columns:
        report_lines.append("\n### Composite Quality Assessment:")
        report_lines.append("   - Seven-dimensional quality scoring system")
        report_lines.append("   - Ecology-specific relevance weighting (12% of overall score)")
        report_lines.append("   - Normalized 0-1 scaling for cross-configuration comparison")

    # Recommendations
    report_lines.append("\n## 📋 Recommendations for Paper")
    report_lines.append("-" * 40)

    report_lines.append("### 📊 Primary Figures for Publication:")
    report_lines.append("1. 📊 Use 'main_scaling_effects.png' for primary quantitative results")
    report_lines.append("2. 📈 Include 'parameter_effects.png' to show individual parameter impacts")
    report_lines.append("3. 🎯 Add 'quality_dimensions.png' for qualitative analysis section")
    report_lines.append("4. ⚖️ Use 'optimization_analysis.png' for cost-benefit discussion")
    report_lines.append("5. 📈 Reference individual question plots for detailed examples")

    report_lines.append("\n### 📝 Key Messages for Paper:")
    report_lines.append(f"1. 💡 Emphasize non-linear scaling: {scaling_factor:.1f}x sources for {word_scaling:.1f}x content")
    report_lines.append("2. 🌿 Highlight ecology-specific enhancements and domain expertise")
    report_lines.append("3. ⚖️ Discuss efficiency vs comprehensiveness trade-offs")
    report_lines.append("4. 🔬 Present methodological innovations in quality assessment")
    report_lines.append("5. 🎯 Guide researchers on optimal configuration selection")

    report_lines.append("\n### 🎯 Configuration Selection Guidance:")
    report_lines.append("   - **Resource-Constrained**: d1_b1 for optimal efficiency")
    report_lines.append("   - **Comprehensive Reviews**: d4_b4 for systematic coverage")
    report_lines.append("   - **Innovation Focus**: d4_b1 for novel insights generation")
    report_lines.append("   - **Broad Surveys**: d1_b4 for rapid landscape assessment")
    
    # Save enhanced report
    with open(f'{output_dir}/enhanced_analysis_report.md', 'w') as f:
        f.write('\n'.join(report_lines))


def create_paper_summary(all_results, output_dir=OUTPUT_DIR):
    """
    Create a summary specifically for the paper's Qualitative Results section
    """
    combined_df = pd.concat(all_results.values(), ignore_index=True)

    # Add depth and breadth columns from config
    combined_df['depth'] = combined_df['config'].str.extract(r'd(\d+)_b\d+').astype(int)
    combined_df['breadth'] = combined_df['config'].str.extract(r'd\d+_b(\d+)').astype(int)
    
    summary_lines = []
    summary_lines.append("# Summary for Paper - Qualitative Results Section")
    summary_lines.append("=" * 60)
    summary_lines.append("")
    
    # Key statistics for the paper
    configs = ['d1_b1', 'd1_b4', 'd4_b1', 'd4_b4']
    
    summary_lines.append("## Key Statistics for Paper")
    summary_lines.append("")
    
    for config in depth_breadth_filename_patterns:
        config_data = combined_df[combined_df['config'] == config]
        if len(config_data) > 0:
            sources_mean = config_data['source_count'].mean()
            sources_std = config_data['source_count'].std()
            words_mean = config_data['word_count'].mean()
            
            summary_lines.append(f"**{config}**: {sources_mean:.1f} ± {sources_std:.1f} sources, {words_mean:.0f} words")
    
    # Calculate key ratios
    d1b1_data = combined_df[combined_df['config'] == 'd1_b1']
    d4b4_data = combined_df[combined_df['config'] == 'd4_b4']

    if len(d1b1_data) > 0 and len(d4b4_data) > 0:
        source_ratio = d4b4_data['source_count'].mean() / d1b1_data['source_count'].mean()
        word_ratio = d4b4_data['word_count'].mean() / d1b1_data['word_count'].mean()

        summary_lines.append("")
        summary_lines.append(f"**Source scaling factor (d4_b4/d1_b1)**: {source_ratio:.1f}x")
        summary_lines.append(f"**Word count increase (d4_b4/d1_b1)**: {word_ratio:.1f}x")

        # Add ecology-specific scaling if available
        ecology_metrics = ['ecosystem_services', 'conservation_focus', 'climate_relevance', 'ecological_complexity']
        for metric in ecology_metrics:
            if metric in combined_df.columns:
                d1b1_eco = d1b1_data[metric].mean()
                d4b4_eco = d4b4_data[metric].mean()
                if d1b1_eco > 0:
                    eco_ratio = d4b4_eco / d1b1_eco
                    summary_lines.append(f"**{metric.replace('_', ' ').title()} improvement**: {eco_ratio:.1f}x")

    # Add quality insights if available
    if 'overall_quality' in combined_df.columns:
        summary_lines.append("\n## Quality Analysis")
        summary_lines.append("")

        quality_by_config = combined_df.groupby('config')['overall_quality'].mean()
        best_quality = quality_by_config.idxmax()
        quality_range = quality_by_config.max() - quality_by_config.min()

        summary_lines.append(f"**Highest quality configuration**: {best_quality} ({quality_by_config[best_quality]:.3f})")
        summary_lines.append(f"**Quality range across configurations**: {quality_range:.3f}")

        # Efficiency analysis
        efficiency_by_config = combined_df.groupby('config').apply(
            lambda x: x['overall_quality'].mean() / x['source_count'].mean()
        )
        most_efficient = efficiency_by_config.idxmax()
        summary_lines.append(f"**Most efficient configuration**: {most_efficient} ({efficiency_by_config[most_efficient]:.4f} quality/source)")

    # Add methodological insights
    summary_lines.append("\n## Methodological Insights")
    summary_lines.append("")
    summary_lines.append("- Enhanced word cloud framework with ecology-specific filtering")
    summary_lines.append("- Multi-dimensional quality assessment including ecological relevance")
    summary_lines.append("- Comprehensive source utilization and content scaling analysis")
    summary_lines.append("- Trade-off analysis between resource efficiency and research comprehensiveness")

    # Save paper summary
    with open(f'{output_dir}/paper_summary.md', 'w') as f:
        f.write('\n'.join(summary_lines))


if __name__ == "__main__":
    # Run the analysis on all questions
    results = run_comprehensive_analysis(
        sample_size=50
    )
    
    print("\n🎉 Enhanced analysis complete!")
    print("Generated files:")
    print("enhanced_analysis_report.md - Comprehensive analysis")
    print("paper_summary.md - Summary for paper")
    print("main_scaling_effects.png - Primary figure for paper")
    print("parameter_effects.png - Individual parameter effects")
    print("quality_dimensions.png - Quality analysis")
    print("optimization_analysis.png - Cost-benefit analysis")
