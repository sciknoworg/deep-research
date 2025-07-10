import pandas as pd
from matplotlib import pyplot as plt

from scripts.utils import depth_breadth_filename_patterns


def create_quality_dimensions_plot(all_results, figures_dir):
    """
    Create a quality dimensions analysis plot
    """
    # Combine all results
    combined_df = pd.concat(all_results.values(), ignore_index=True)
    combined_df['config'] = combined_df.apply(lambda row: f"d{row['depth']}_b{row['breadth']}", axis=1)

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Research Quality Dimensions Analysis', fontsize=16, fontweight='bold')

    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

    # Quality dimensions to analyze
    quality_metrics = [
        ('depth_score', 'Research Depth Score'),
        ('breadth_score', 'Research Breadth Score'),
        ('rigor_score', 'Scientific Rigor Score'),
        ('innovation_score', 'Innovation Score'),
        ('info_density', 'Information Density'),
        ('overall_quality', 'Overall Quality Score')
    ]

    for i, (metric, title) in enumerate(quality_metrics):
        ax = axes[i // 3, i % 3]

        means = []
        stds = []
        for config in depth_breadth_filename_patterns:
            config_data = combined_df[combined_df['config'] == config]
            if len(config_data) > 0 and metric in config_data.columns:
                means.append(config_data[metric].mean())
                stds.append(config_data[metric].std())
            else:
                means.append(0)
                stds.append(0)

        bars = ax.bar(depth_breadth_filename_patterns, means, yerr=stds, capsize=5, color=colors, alpha=0.8)
        ax.set_title(title)
        ax.set_ylabel('Score (0-1)')
        ax.set_ylim(0, 1.1)

        # Add value labels
        for bar, mean in zip(bars, means):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{mean:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.tight_layout()
    output_path = f'{figures_dir}/quality_dimensions.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
