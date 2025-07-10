import pandas as pd
import os
from matplotlib import pyplot as plt

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import depth_breadth_filename_patterns


def create_parameter_effects_plot(statistics_file, figures_dir):
    """
    Create an individual parameter effects plot.
    """
    df = pd.read_csv(statistics_file, index_col=0)
    source_means = [df.loc[config, 'source_count_mean'] for config in depth_breadth_filename_patterns]

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    fig.suptitle('Individual Parameter Effects on Source Utilization', fontsize=14, fontweight='bold')

    depth_1_avg = (source_means[0] + source_means[1]) / 2  # d1 average
    depth_4_avg = (source_means[2] + source_means[3]) / 2  # d4 average
    breadth_1_avg = (source_means[0] + source_means[2]) / 2  # b1 average
    breadth_4_avg = (source_means[1] + source_means[3]) / 2  # b4 average

    effects = [depth_1_avg, depth_4_avg, breadth_1_avg, breadth_4_avg]
    labels = ['Depth 1', 'Depth 4', 'Breadth 1', 'Breadth 4']
    colors = ['#3498db', '#3498db', '#2ecc71', '#2ecc71']

    bars = ax.bar(labels, effects, color=colors, alpha=0.8)
    ax.set_ylabel('Average Sources')
    ax.set_title('Individual Parameter Effects')
    ax.tick_params(axis='x', rotation=45)

    # Add value labels
    for bar, effect in zip(bars, effects):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{effect:.1f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    output_path = f'{figures_dir}/parameter_effects.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
