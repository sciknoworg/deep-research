# overall_quality_analysis.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def _ensure_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Add any missing score columns with zeros so plotting never crashes."""
    needed = [
        'config','depth_score','breadth_score','rigor_score','innovation_score',
        'gap_score','overall_quality'
    ]
    for c in needed:
        if c not in df.columns:
            if c == 'config':
                df[c] = 'd1_b1'
            else:
                df[c] = 0.0
    return df

def _bar(ax, xlabels, means, stds, title):
    xs = np.arange(len(xlabels))
    ax.bar(xs, means, yerr=stds, capsize=3)
    ax.set_xticks(xs); ax.set_xticklabels(xlabels, rotation=0)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel('Score (0..1)')
    ax.set_title(title)
    # annotate bars
    for x, y in zip(xs, means):
        ax.text(x, max(0.01, y)+0.01, f"{y:.2f}", ha='center', va='bottom', fontsize=8)

def create_overall_quality_analysis(all_results: dict, figures_dir: str):
    """
    Robust, domain-agnostic quality overview figure.
    - Works for Ecology *and* NLP.
    - Never assumes presence of domain-specific counters like 'geographic_regions'.
    - Plots 6 panels: depth, breadth, rigor, innovation, info-density, overall.
    """
    os.makedirs(figures_dir, exist_ok=True)
    combined = pd.concat(all_results.values(), ignore_index=True)
    combined = _ensure_cols(combined)

    cfgs = sorted(combined['config'].unique())
    def agg(col): 
        return (combined.groupby('config')[col].mean().reindex(cfgs).fillna(0.0),
                combined.groupby('config')[col].std().reindex(cfgs).fillna(0.0))

    depth_m, depth_s = agg('depth_score')
    breadth_m, breadth_s = agg('breadth_score')
    rigor_m, rigor_s = agg('rigor_score')
    innov_m, innov_s = agg('innovation_score')
    gap_m, gap_s = agg('gap_score')
    overall_m, overall_s = agg('overall_quality')

    fig = plt.figure(figsize=(14, 10))
    axes = [
        plt.subplot(2,3,1),
        plt.subplot(2,3,2),
        plt.subplot(2,3,3),
        plt.subplot(2,3,4),
        plt.subplot(2,3,5),
        plt.subplot(2,3,6),
    ]
    _bar(axes[0], cfgs, depth_m.values, depth_s.values, 'Research Depth Score')
    _bar(axes[1], cfgs, breadth_m.values, breadth_s.values, 'Research Breadth Score')
    _bar(axes[2], cfgs, rigor_m.values, rigor_s.values, 'Scientific Rigor Score')
    _bar(axes[3], cfgs, innov_m.values, innov_s.values, 'Innovation Score')
    _bar(axes[4], cfgs, gap_m.values, gap_s.values, 'Research Gap Score')
    _bar(axes[5], cfgs, overall_m.values, overall_s.values, 'Overall Quality Score')
    plt.suptitle('Research Quality Dimensions Analysis', fontsize=14, y=0.98)
    plt.tight_layout(rect=[0,0,1,0.96])
    out = os.path.join(figures_dir, 'quality_dimensions.png')
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # sanity ping in console if depth/breadth are basically zero
    tiny = []
    for name, m in [('depth', depth_m), ('breadth', breadth_m)]:
        if (m < 1e-3).all():
            tiny.append(name)
    if tiny:
        print(f"[WARN] The following scores are ~0 across all configs: {', '.join(tiny)}.\n"
              f"       Check vocabulary coverage or adjust coverage normalization.")
