import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import depth_breadth_filename_patterns


def create_main_scaling_plot(statistics_file, figures_dir):
    """
    Create the main scaling effects plot (sources, words, efficiency)
    """
    df = pd.read_csv(statistics_file, index_col=0)
    source_means = [df.loc[config, 'source_count_mean'] for config in depth_breadth_filename_patterns]
    source_stds = [df.loc[config, 'source_count_std'] for config in depth_breadth_filename_patterns]
    word_means = [df.loc[config, 'word_count_mean'] for config in depth_breadth_filename_patterns]

    title = "Deep Research Parameter Effects: Quantitative Analysis"

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # 1. Source count scaling
    ax1 = axes[0]
    bars = ax1.bar(
        depth_breadth_filename_patterns,
        source_means,
        yerr=source_stds,
        capsize=5,
        color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'], alpha=0.8
    )
    ax1.set_ylabel('Number of Sources')
    ax1.set_title('Source Utilization by Configuration')
    ax1.set_ylim(0, max(source_means) * 1.2)

    # Add value labels on bars
    for bar, mean in zip(bars, source_means):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(source_means) * 0.02,
                 f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')

    # 2. Word count scaling
    ax2 = axes[1]
    bars2 = ax2.bar(
        depth_breadth_filename_patterns, word_means,
        color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'], alpha=0.8
    )
    ax2.set_ylabel('Word Count')
    ax2.set_title('Content Length by Configuration')

    for bar, mean in zip(bars2, word_means):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(word_means) * 0.01,
                 f'{mean:.0f}', ha='center', va='bottom', fontweight='bold')

    # 3. Efficiency ratio
    ax3 = axes[2]
    efficiency = np.array(source_means) / (np.array(word_means) / 1000)
    bars3 = ax3.bar(
        depth_breadth_filename_patterns, efficiency,
        color=['#3498db', '#2ecc71', '#f39c12', '#e74c3c'], alpha=0.8
    )
    ax3.set_ylabel('Sources per 1000 Words')
    ax3.set_title('Information Density')

    for bar, eff in zip(bars3, efficiency):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + max(efficiency) * 0.02,
                 f'{eff:.1f}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    output_path = f'{figures_dir}/main_scaling_effects.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()