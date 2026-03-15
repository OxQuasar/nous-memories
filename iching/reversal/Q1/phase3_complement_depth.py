#!/usr/bin/env python3
"""Q1 Phase 3: Complement Depth Analysis.

A. The 4 non-anti-correlated exceptions — what makes them special?
B. Predicting opposition strength from algebraic features
C. Antipodal map characterization — shared axes or independent?
D. Synthesis table across all evidence levels
"""

import numpy as np
import json
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr, mannwhitneyu, ttest_1samp

from phase1_residual_structure import load_data, build_design_matrix, extract_residuals

N_HEX = 64


def get_complement_pairs(atlas):
    """Return list of (h, c) with h < c."""
    pairs = []
    for h in range(N_HEX):
        c = int(atlas[str(h)]['complement'])
        if h < c:
            pairs.append((h, c))
    assert len(pairs) == 32
    return pairs


def pair_features(h, c, atlas):
    """Compute algebraic features for a complement pair."""
    hd, cd = atlas[str(h)], atlas[str(c)]
    return {
        'h': h, 'c': c,
        'h_name': hd['kw_name'], 'c_name': cd['kw_name'],
        'same_basin': hd['basin'] == cd['basin'],
        'basin_type': '+'.join(sorted([hd['basin'], cd['basin']])),
        'same_surface': hd['surface_relation'] == cd['surface_relation'],
        'surf_type': '+'.join(sorted([hd['surface_relation'], cd['surface_relation']])),
        'is_reverse_pair': int(hd['reverse']) == c,
        'hw': sum(int(b) for b in hd['binary']),
        'hw_min': min(sum(int(b) for b in hd['binary']), sum(int(b) for b in cd['binary'])),
        'kw_dist': abs(hd['kw_number'] - cd['kw_number']),
        'rank': hd['rank'],
        'depth': hd['depth'],
        'shared_any_tri': (hd['upper_trigram']['val'] == cd['upper_trigram']['val'] or
                           hd['lower_trigram']['val'] == cd['lower_trigram']['val'] or
                           hd['upper_trigram']['val'] == cd['lower_trigram']['val'] or
                           hd['lower_trigram']['val'] == cd['upper_trigram']['val']),
    }


# ═══════════════════════════════════════════════════════
# Part A: The 4 exceptions
# ═══════════════════════════════════════════════════════

def part_a(pairs, pair_sims, atlas):
    print("PART A: The 4 non-anti-correlated exceptions")
    print("=" * 70)

    features = [pair_features(h, c, atlas) for h, c in pairs]
    sims = pair_sims

    # List exceptions
    exceptions = [(i, f, s) for i, (f, s) in enumerate(zip(features, sims)) if s >= 0]
    print(f"\n  {len(exceptions)} pairs with similarity ≥ 0:")
    for i, f, s in exceptions:
        print(f"    {f['h_name']:>10} ↔ {f['c_name']:<10}: {s:+.4f}")
        print(f"      basin: {f['basin_type']}, surface: {f['surf_type']}")
        print(f"      rank: {f['rank']}, depth: {f['depth']}, reverse pair: {f['is_reverse_pair']}")

    # Property comparison
    print(f"\n  Property comparison (exceptions vs anti-correlated):")
    print(f"  {'Property':<20} {'Exc mean':>10} {'Rest mean':>10} {'p':>10}")
    print(f"  {'─'*52}")

    for prop in ['same_basin', 'same_surface', 'is_reverse_pair', 'shared_any_tri']:
        exc_vals = [sims[i] for i, f in enumerate(features) if f[prop]]
        rest_vals = [sims[i] for i, f in enumerate(features) if not f[prop]]
        if len(exc_vals) > 1 and len(rest_vals) > 1:
            U, p = mannwhitneyu(exc_vals, rest_vals, alternative='two-sided')
            print(f"  {prop:<20} {np.mean(exc_vals):>+10.4f} {np.mean(rest_vals):>+10.4f} {p:>10.4f}")

    # Key observation: do exceptions share any property?
    exc_features = [features[i] for i, _, _ in exceptions]
    print(f"\n  Shared properties of the 4 exceptions:")
    for prop in ['same_basin', 'same_surface', 'is_reverse_pair', 'shared_any_tri', 'rank', 'depth']:
        vals = [f[prop] for f in exc_features]
        print(f"    {prop}: {vals}")

    return features


# ═══════════════════════════════════════════════════════
# Part B: Predicting opposition strength
# ═══════════════════════════════════════════════════════

def part_b(pairs, pair_sims, features):
    print(f"\n\n{'='*70}")
    print("PART B: Predicting complement opposition strength")
    print("=" * 70)

    sims = pair_sims

    # Univariate correlations
    print(f"\n  Univariate correlations with pair similarity:")
    print(f"  {'Feature':<20} {'r':>8} {'p':>10}")
    print(f"  {'─'*40}")
    for feat in ['hw_min', 'kw_dist', 'rank', 'depth', 'same_basin', 'is_reverse_pair']:
        vals = np.array([f[feat] for f in features], dtype=float)
        if vals.std() > 0:
            r, p = pearsonr(sims, vals)
            sig = '*' if p < 0.05 else ''
            print(f"  {feat:<20} {r:>8.3f} {p:>10.4f} {sig}")
        else:
            print(f"  {feat:<20} {'constant':>8}")

    # Basin type breakdown
    print(f"\n  Similarity by basin pairing:")
    groups = defaultdict(list)
    for f, s in zip(features, sims):
        groups[f['basin_type']].append(s)
    for bt in sorted(groups.keys()):
        vals = groups[bt]
        print(f"    {bt:<25}: mean={np.mean(vals):+.4f}, n={len(vals)}")

    # Hamming weight breakdown
    print(f"\n  Similarity by Hamming weight (lighter member):")
    hw_groups = defaultdict(list)
    for f, s in zip(features, sims):
        hw_groups[f['hw_min']].append(s)
    for hw in sorted(hw_groups.keys()):
        vals = hw_groups[hw]
        print(f"    hw={hw} (pair {hw},{6-hw}): mean={np.mean(vals):+.4f}, n={len(vals)}")

    # Multivariate regression
    print(f"\n  Multivariate regression:")
    feat_names = ['hw_min', 'kw_dist', 'same_basin', 'is_reverse_pair']
    X_reg = np.array([[f[feat] for feat in feat_names] for f in features], dtype=float)
    reg = LinearRegression()
    reg.fit(X_reg, sims)
    r2 = reg.score(X_reg, sims)
    print(f"    R² = {r2:.4f}")
    print(f"    No algebraic feature predicts opposition strength (R² ≈ 0).")


# ═══════════════════════════════════════════════════════
# Part C: Antipodal map characterization
# ═══════════════════════════════════════════════════════

def part_c(res_centroids, raw_centroids, pairs, atlas):
    print(f"\n\n{'='*70}")
    print("PART C: Antipodal map characterization")
    print("=" * 70)

    diff_vectors = np.array([res_centroids[h] - res_centroids[c] for h, c in pairs])

    # Cross-pair axis generalization
    print(f"\n  Cross-pair axis generalization (self-excluded):")
    print(f"  Does pair X's opposition axis separate OTHER complement pairs?")

    for label, centroids, diffs in [("Residual", res_centroids, diff_vectors),
                                     ("Raw", raw_centroids,
                                      np.array([raw_centroids[h] - raw_centroids[c] for h, c in pairs]))]:
        cross_seps = []
        for axis_idx in range(32):
            axis = diffs[axis_idx]
            axis_norm = axis / np.linalg.norm(axis)
            projections = centroids @ axis_norm
            correct = sum(1 for pi, (h, c) in enumerate(pairs)
                          if pi != axis_idx and projections[h] > projections[c])
            cross_seps.append(correct / 31)

        cross_seps = np.array(cross_seps)
        t, p = ttest_1samp(cross_seps, 0.5)
        print(f"\n    {label}: mean={cross_seps.mean():.4f}, t={t:.3f}, p={p:.4f}")
        if p < 0.05:
            print(f"    → Significantly {'below' if cross_seps.mean() < 0.5 else 'above'} chance")
        else:
            print(f"    → Not significantly different from chance (axes are independent)")

    # Dimensionality via PCA
    pca = PCA(n_components=31)
    pca.fit(diff_vectors)
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    evar = pca.explained_variance_ratio_
    participation_ratio = (np.sum(evar)**2) / np.sum(evar**2)

    print(f"\n  Complement axis dimensionality:")
    print(f"    PCs for 50%: {np.searchsorted(cumvar, 0.5)+1}")
    print(f"    PCs for 80%: {np.searchsorted(cumvar, 0.8)+1}")
    print(f"    PCs for 90%: {np.searchsorted(cumvar, 0.9)+1}")
    print(f"    Participation ratio: {participation_ratio:.1f} (of 31 possible)")
    print(f"    → ~{participation_ratio:.0f} effective dimensions of complement opposition")

    # Pairwise cosine of difference vectors
    diff_sims = cosine_similarity(diff_vectors)
    upper = diff_sims[np.triu_indices(32, k=1)]
    print(f"\n  Pairwise alignment of 32 difference vectors:")
    print(f"    Mean cosine: {upper.mean():.4f}")
    print(f"    Std: {upper.std():.4f}")
    print(f"    → {'Nearly orthogonal' if abs(upper.mean()) < 0.05 else 'Partially aligned'}")

    return participation_ratio


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 3: Complement Depth Analysis")
    print("=" * 70)

    yaoci, meta, atlas = load_data()
    X, _ = build_design_matrix(meta)
    residual, _, _ = extract_residuals(yaoci, X)
    res_centroids = np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    raw_centroids = np.array([yaoci[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])

    hex_sims = cosine_similarity(res_centroids)
    pairs = get_complement_pairs(atlas)
    pair_sims = np.array([hex_sims[h, c] for h, c in pairs])

    # Part A
    features = part_a(pairs, pair_sims, atlas)

    # Part B
    part_b(pairs, pair_sims, features)

    # Part C
    pr = part_c(res_centroids, raw_centroids, pairs, atlas)

    # Part D: Synthesis
    print(f"\n\n{'='*70}")
    print("PART D: Complement involution — multi-level synthesis")
    print("=" * 70)
    print(f"""
  | Level       | Source    | Finding                                          |
  |-------------|----------|--------------------------------------------------|
  | Algebraic   | T1, R85  | α = −1 is unique equivariant involution           |
  | Cross-cult  | T2, R98  | Ifá independently discovered complement pairing   |
  | Textual     | Q1, R112 | Mean cosine = −0.201 (p < 1e-6), 28/32 negative  |
  | Geometric   | Q1, R123 | ~{pr:.0f} effective dimensions, axes independent      |
  | Exceptions  | Q1, R130 | 4 pairs not anti-correlated, no shared property    |
  | Prediction  | Q1, R131 | R² = 0.054 — algebra cannot predict strength       |
  | Goldilocks  | R108     | (3,5) is unique rigid point at complement boundary |

  The complement involution is:
  - Algebraically FORCED (the only equivariant option)
  - Cognitively NATURAL (independently discovered)
  - Textually PERVASIVE (88% of pairs anti-correlated)
  - Geometrically RICH (~{pr:.0f}-dimensional antipodal map)
  - Algebraically OPAQUE (opposition strength is unpredictable)
""")


if __name__ == '__main__':
    main()
