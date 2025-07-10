import pandas as pd
from matplotlib import pyplot as plt

from scripts.utils import depth_breadth_filename_patterns


def create_overall_quality_analysis(all_results, figures_dir):
    """
    Create aggregate analysis across multiple questions
    """
    # Combine all dataframes
    combined_df = pd.concat(all_results.values(), ignore_index=True)

    # Create aggregate visualizations
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    fig.suptitle('Aggregate Analysis Across All Questions', fontsize=16)

    # 1. Source count distribution by configuration
    ax1 = axes[0, 0]

    # Create a configuration column for easier filtering
    combined_df['config'] = combined_df.apply(lambda row: f"d{row['depth']}_b{row['breadth']}", axis=1)

    source_means = [combined_df[combined_df['config'] == config]['source_count'].mean()
                    for config in depth_breadth_filename_patterns]
    source_stds = [combined_df[combined_df['config'] == config]['source_count'].std()
                   for config in depth_breadth_filename_patterns]
    ax1.bar(depth_breadth_filename_patterns, source_means, yerr=source_stds, capsize=5,
            color=['lightblue', 'lightgreen', 'orange', 'red'])
    ax1.set_title('Average Source Count by Configuration')
    ax1.set_ylabel('Number of Sources')

    # 2. Word count distribution
    ax2 = axes[0, 1]
    word_means = [combined_df[combined_df['config'] == config]['word_count'].mean()
                  for config in depth_breadth_filename_patterns]
    word_stds = [combined_df[combined_df['config'] == config]['word_count'].std()
                 for config in depth_breadth_filename_patterns]
    ax2.bar(depth_breadth_filename_patterns, word_means, yerr=word_stds, capsize=5,
            color=['lightblue', 'lightgreen', 'orange', 'red'])
    ax2.set_title('Average Word Count by Configuration')
    ax2.set_ylabel('Word Count')

    # 3. Geographic coverage
    ax3 = axes[0, 2]
    geo_means = [combined_df[combined_df['config'] == config]['geographic_regions'].mean()
                 for config in depth_breadth_filename_patterns]
    ax3.bar(depth_breadth_filename_patterns, geo_means, color=['lightblue', 'lightgreen', 'orange', 'red'])
    ax3.set_title('Average Geographic Regions by Configuration')
    ax3.set_ylabel('Number of Regions')

    # 4. Mechanistic detail
    ax4 = axes[1, 0]
    mech_means = [combined_df[combined_df['config'] == config]['mechanistic_detail'].mean()
                  for config in depth_breadth_filename_patterns]
    ax4.bar(depth_breadth_filename_patterns, mech_means, color=['lightblue', 'lightgreen', 'orange', 'red'])
    ax4.set_title('Average Mechanistic Detail by Configuration')
    ax4.set_ylabel('Mechanistic Detail Score')

    # 5. Quality indicators
    ax5 = axes[1, 1]
    quality_means = [(combined_df[combined_df['config'] == config]['research_gaps'] +
                      combined_df[combined_df['config'] == config]['speculative_ideas'] +
                      combined_df[combined_df['config'] == config]['tradeoff_mentions']).mean()
                     for config in depth_breadth_filename_patterns]
    ax5.bar(depth_breadth_filename_patterns, quality_means, color=['lightblue', 'lightgreen', 'orange', 'red'])
    ax5.set_title('Average Research Quality Score by Configuration')
    ax5.set_ylabel('Quality Score')

    # 7. Depth vs Breadth effects
    ax7 = axes[2, 0]
    depth_effect = combined_df.groupby('depth')['source_count'].mean()
    breadth_effect = combined_df.groupby('breadth')['source_count'].mean()
    x = ['Depth 1', 'Depth 4', 'Breadth 1', 'Breadth 4']
    y = [depth_effect[1], depth_effect[4], breadth_effect[1], breadth_effect[4]]
    colors = ['blue', 'blue', 'green', 'green']
    ax7.bar(x, y, color=colors, alpha=0.7)
    ax7.set_title('Depth vs Breadth Effects on Source Count')
    ax7.set_ylabel('Average Source Count')
    ax7.tick_params(axis='x', rotation=45)

    # 9. Scaling effects
    ax9 = axes[2, 2]
    # Calculate scaling factor (d4_b4 vs d1_b1)
    scaling_factors = []
    questions = []
    for q_num, df in all_results.items():
        if 'd1_b1' in df.index and 'd4_b4' in df.index:
            d1b1_sources = df.loc['d1_b1', 'source_count']
            d4b4_sources = df.loc['d4_b4', 'source_count']
            if d1b1_sources > 0:
                scaling_factors.append(d4b4_sources / d1b1_sources)
                questions.append(f'Q{q_num}')

    if scaling_factors:
        ax9.bar(questions, scaling_factors, color='purple', alpha=0.7)
        ax9.set_title('Source Scaling Factor (d4_b4 / d1_b1)')
        ax9.set_ylabel('Scaling Factor')
        ax9.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    output_path = f'{figures_dir}/overall_quality_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
