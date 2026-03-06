#!/usr/bin/env python3
"""
Opposition Theory — Phase 1: Pareto Frontier Analysis

Loads measures from enumerate.py output, computes Pareto frontier,
generates scatter plots and analysis report.

Objectives (all maximize):
  1. Strength ↑
  2. Diversity ↑
  5. Weight Correlation: we include |weight_corr| ↑ (extremity, not sign)
  4a. Weight Tilt: context-dependent — test both directions
  4b. Reversal Symmetry ↑

Primary Pareto: strength × diversity × |weight_corr| (3D)
Extended: add reversal_symmetry and weight_tilt if non-degenerate
"""

import json
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not available, skipping plots")


OUT_DIR = Path(__file__).parent


# ─── Load data ────────────────────────────────────────────────────────────────

def load_data():
    data = np.load(OUT_DIR / 'measures.npz')
    meta = json.load(open(OUT_DIR / 'meta.json'))
    return data, meta


# ─── Pareto computation ──────────────────────────────────────────────────────

def pareto_frontier_unique(points):
    """
    Compute Pareto frontier for points where all objectives are to be maximized.
    points: (N, D) array.
    Returns mask of non-dominated points.

    Strategy: group by unique profiles (expect many duplicates),
    compute Pareto on unique set, then expand back.
    """
    N, D = points.shape

    # Find unique rows
    unique, inverse = np.unique(points, axis=0, return_inverse=True)
    U = len(unique)
    print(f"  Unique measure profiles: {U:,} (from {N:,} pairings)")

    # Pareto on unique set — O(U²) which is manageable for U << N
    dominated = np.zeros(U, dtype=bool)
    # Sort by first objective descending for early termination
    order = np.argsort(-unique[:, 0])
    unique_sorted = unique[order]

    for i in range(U):
        if dominated[order[i]]:
            continue
        for j in range(U):
            if i == j or dominated[order[j]]:
                continue
            # Does order[i] dominate order[j]?
            ui, uj = order[i], order[j]
            if np.all(unique[ui] >= unique[uj]) and np.any(unique[ui] > unique[uj]):
                dominated[uj] = True

    # Map back
    pareto_mask = ~dominated[inverse]
    return pareto_mask, unique, inverse, ~dominated


# ─── Plot helpers ─────────────────────────────────────────────────────────────

def scatter_2d(x, y, xlabel, ylabel, title, named_points, pareto_mask, filename):
    """2D scatter with named pairings and Pareto frontier marked."""
    if not HAS_MPL:
        return

    fig, ax = plt.subplots(figsize=(10, 8))

    # Background: all points (sample if too many)
    n = len(x)
    if n > 50000:
        idx = np.random.choice(n, 50000, replace=False)
        ax.scatter(x[idx], y[idx], s=1, alpha=0.1, c='gray', label=f'Sample (50k/{n:,})')
    else:
        ax.scatter(x, y, s=1, alpha=0.2, c='gray', label=f'All ({n:,})')

    # Pareto points
    px, py = x[pareto_mask], y[pareto_mask]
    ax.scatter(px, py, s=15, alpha=0.6, c='blue', zorder=3, label=f'Pareto ({np.sum(pareto_mask):,})')

    # Named pairings
    colors = {'complement': 'red', 'kw_style': 'orange'}
    markers = {'complement': 'D', 'kw_style': '^'}
    for name, idx in named_points.items():
        if idx is not None:
            ax.scatter(x[idx], y[idx], s=200, c=colors.get(name, 'black'),
                      marker=markers.get(name, 'o'), zorder=5,
                      edgecolors='black', linewidth=1.5, label=name)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_DIR / filename, dpi=150)
    plt.close(fig)
    print(f"  Saved {filename}")


def histogram_2d(x, y, xlabel, ylabel, title, named_points, filename):
    """2D hexbin density plot."""
    if not HAS_MPL:
        return

    fig, ax = plt.subplots(figsize=(10, 8))
    hb = ax.hexbin(x, y, gridsize=40, cmap='Blues', mincnt=1)
    fig.colorbar(hb, ax=ax, label='Count')

    colors = {'complement': 'red', 'kw_style': 'orange'}
    markers = {'complement': 'D', 'kw_style': '^'}
    for name, idx in named_points.items():
        if idx is not None:
            ax.scatter(x[idx], y[idx], s=200, c=colors.get(name, 'black'),
                      marker=markers.get(name, 'o'), zorder=5,
                      edgecolors='black', linewidth=1.5, label=name)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='best', fontsize=9)

    fig.tight_layout()
    fig.savefig(OUT_DIR / filename, dpi=150)
    plt.close(fig)
    print(f"  Saved {filename}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("n=4 PARETO FRONTIER ANALYSIS")
    print("=" * 70)

    data, meta = load_data()
    S = data['strengths'].astype(float)
    D = data['diversities']
    WT = data['weight_tilts']
    RS = data['reversal_syms'].astype(float)
    WC = data['weight_corrs']
    N = len(S)

    named = meta['named_indices']

    # ── Check for degenerate measures ──
    print("\n## Degeneracy Check")
    measures = {'Strength': S, 'Diversity': D, 'Weight Tilt': WT,
                'Reversal Sym': RS, 'Weight Corr': WC}
    for name, arr in measures.items():
        uvals = np.unique(arr)
        rng = arr.max() - arr.min()
        cv = arr.std() / abs(arr.mean()) if arr.mean() != 0 else float('inf')
        print(f"  {name:>15}: {len(uvals):>6} unique values, "
              f"range [{arr.min():.4f}, {arr.max():.4f}], CV={cv:.4f}")
        if len(uvals) <= 2:
            print(f"    *** NEAR-DEGENERATE — only {len(uvals)} distinct values")

    # ── Primary Pareto: Strength × Diversity × |Weight Corr| ──
    print("\n## Primary Pareto: Strength × Diversity × |Weight Corr|")
    print("  (all maximized)")

    points_3d = np.column_stack([S, D, np.abs(WC)])
    pareto_mask_3d, unique_3d, inv_3d, upareto_3d = pareto_frontier_unique(points_3d)
    n_pareto_3d = np.sum(pareto_mask_3d)
    print(f"  Pareto frontier size: {n_pareto_3d:,} / {N:,} "
          f"({100*n_pareto_3d/N:.2f}%)")

    for name, idx in named.items():
        if idx is not None:
            on_pareto = pareto_mask_3d[idx]
            print(f"  {name:>15} on Pareto: {on_pareto}  "
                  f"(S={S[idx]:.0f}, D={D[idx]:.4f}, |WC|={abs(WC[idx]):.4f})")

    # ── Extended Pareto: add non-degenerate measures ──
    # Check if Weight Tilt and Reversal Sym add discrimination
    print("\n## Extended Pareto: + Reversal Symmetry + (neg) Weight Tilt")
    # Weight tilt: lower might be "better" (balanced), so maximize -WT
    points_5d = np.column_stack([S, D, np.abs(WC), RS, -WT])
    pareto_mask_5d, unique_5d, inv_5d, upareto_5d = pareto_frontier_unique(points_5d)
    n_pareto_5d = np.sum(pareto_mask_5d)
    print(f"  Pareto frontier size: {n_pareto_5d:,} / {N:,} "
          f"({100*n_pareto_5d/N:.2f}%)")

    for name, idx in named.items():
        if idx is not None:
            on_pareto = pareto_mask_5d[idx]
            print(f"  {name:>15} on Pareto: {on_pareto}")

    # ── Alternative: Strength × Diversity only ──
    print("\n## 2D Pareto: Strength × Diversity")
    points_2d = np.column_stack([S, D])
    pareto_mask_2d, unique_2d, inv_2d, upareto_2d = pareto_frontier_unique(points_2d)
    n_pareto_2d = np.sum(pareto_mask_2d)
    print(f"  Pareto frontier size: {n_pareto_2d:,} / {N:,}")

    # List the 2D Pareto-optimal unique profiles
    pareto_profiles_2d = unique_2d[upareto_2d]
    order = np.argsort(-pareto_profiles_2d[:, 0])
    print(f"\n  2D Pareto frontier profiles (Strength, Diversity):")
    for i in order:
        s, d = pareto_profiles_2d[i]
        count = np.sum((S == s) & (D == d))
        print(f"    S={s:5.0f}  D={d:.6f}  (n={count:,})")

    for name, idx in named.items():
        if idx is not None:
            print(f"  {name:>15} on 2D Pareto: {pareto_mask_2d[idx]}")

    # ── Detailed Pareto frontier inspection ──
    print("\n## Pareto Frontier Details (3D)")

    # Group Pareto points by strength
    pareto_idx = np.where(pareto_mask_3d)[0]
    by_strength = {}
    for i in pareto_idx:
        s = int(S[i])
        if s not in by_strength:
            by_strength[s] = []
        by_strength[s].append(i)

    for s in sorted(by_strength.keys(), reverse=True):
        indices = by_strength[s]
        d_vals = D[indices]
        wc_vals = np.abs(WC[indices])
        print(f"\n  Strength={s}: {len(indices):,} pairings on frontier")
        print(f"    Diversity: [{d_vals.min():.4f}, {d_vals.max():.4f}]")
        print(f"    |WC|:     [{wc_vals.min():.4f}, {wc_vals.max():.4f}]")

    # ── Strength-Diversity trade-off detail ──
    print("\n## Strength-Diversity Trade-off")
    str_vals = np.unique(S).astype(int)
    for sv in sorted(str_vals, reverse=True):
        mask = S == sv
        dvs = D[mask]
        print(f"  S={sv:2d}: n={mask.sum():>8,}  "
              f"D=[{dvs.min():.4f}, {dvs.max():.4f}]  "
              f"mean_D={dvs.mean():.4f}")

    # ── Plots ──
    print("\n## Generating Plots")

    # 1. Strength vs Diversity scatter
    scatter_2d(S, D, 'Opposition Strength', 'Opposition Diversity (entropy)',
               'n=4: Strength vs Diversity (2M pairings)',
               named, pareto_mask_2d, 'strength_vs_diversity.png')

    # 2. Strength vs Weight Correlation
    scatter_2d(S, WC, 'Opposition Strength', 'Weight Complementarity (Pearson r)',
               'n=4: Strength vs Weight Complementarity',
               named, pareto_mask_3d, 'strength_vs_weight_corr.png')

    # 3. Density plots
    histogram_2d(S, D, 'Opposition Strength', 'Opposition Diversity',
                 'n=4: Pairing Density (Strength × Diversity)',
                 named, 'density_strength_diversity.png')

    # 4. Diversity vs Weight Correlation
    scatter_2d(D, WC, 'Opposition Diversity', 'Weight Complementarity',
               'n=4: Diversity vs Weight Complementarity',
               named, pareto_mask_3d, 'diversity_vs_weight_corr.png')

    # 5. Strength vs Reversal Symmetry
    scatter_2d(S, RS, 'Opposition Strength', 'Reversal Symmetry (pairs preserved)',
               'n=4: Strength vs Reversal Symmetry',
               named, pareto_mask_3d, 'strength_vs_rev_sym.png')

    print("\nDone.")


if __name__ == '__main__':
    main()
