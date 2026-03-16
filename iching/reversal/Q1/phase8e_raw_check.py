#!/usr/bin/env python3
"""Phase 8e: Check if anti-clustering in 8d is a residual-space artifact.

Runs the same algebraic grouping tests on RAW (not residual) difference vectors.
If anti-clustering disappears → artifact of orthogonal complement projection.
If it persists → genuine property of the texts.
"""

import numpy as np
import json
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

from phase1_residual_structure import load_data, build_design_matrix, extract_residuals
from phase8_trigram_decomposition import (
    load_atlas, load_embeddings, get_complement_pairs, get_pair_trigram_types,
    compute_diff_vectors, grouping_test, wuxing_relation, tri_pair_type,
    N_HEX
)

def main():
    print("Phase 8e: Raw vs Residual Anti-Clustering Check")
    print("=" * 70)

    atlas = load_atlas()
    _, meta, _ = load_data()
    pairs = get_complement_pairs(atlas)
    pair_types = get_pair_trigram_types(atlas, pairs)

    yaoci = load_embeddings('bge-m3')

    # Raw centroids
    raw_centroids = np.array([yaoci[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    raw_diff = compute_diff_vectors(raw_centroids, pairs)

    # Residual centroids (for comparison)
    X, _ = build_design_matrix(meta)
    residual, _, _ = extract_residuals(yaoci, X)
    res_centroids = np.array([residual[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    res_diff = compute_diff_vectors(res_centroids, pairs)

    # Build labels
    lower_labels = [lt for lt, ut in pair_types]
    upper_labels = [ut for lt, ut in pair_types]

    wuxing_lower_labels = []
    wuxing_upper_labels = []
    basin_labels = []
    for h, c in pairs:
        sc_h = atlas[str(h)]['surface_cell']
        sc_c = atlas[str(c)]['surface_cell']
        wuxing_lower_labels.append(wuxing_relation(sc_h[0], sc_c[0]))
        wuxing_upper_labels.append(wuxing_relation(sc_h[1], sc_c[1]))
        b1 = atlas[str(h)]['basin']
        b2 = atlas[str(c)]['basin']
        basin_labels.append('same' if b1 == b2 else 'different')

    groupings = [
        ('fano_lower', lower_labels, "Lower trigram pair type"),
        ('fano_upper', upper_labels, "Upper trigram pair type"),
        ('wuxing_lower', wuxing_lower_labels, "五行 lower-element"),
        ('wuxing_upper', wuxing_upper_labels, "五行 upper-element"),
        ('basin', basin_labels, "Basin (same vs diff)"),
    ]

    # Run on both raw and residual
    print("\n  Comparison: RAW vs RESIDUAL difference vectors")
    print(f"  {'Grouping':<22} {'RAW gap':>10} {'RAW p':>8} {'RES gap':>10} {'RES p':>8}")
    print(f"  {'-'*60}")

    for key, labels, name in groupings:
        print(f"\n  === {name} ===")
        print(f"  RAW centroids:")
        r_raw = grouping_test(raw_diff, labels, f"RAW {name}")
        print(f"  RESIDUAL centroids:")
        r_res = grouping_test(res_diff, labels, f"RES {name}")

    # Summary table
    print(f"\n\n{'='*70}")
    print("SUMMARY TABLE")
    print(f"{'='*70}")
    print(f"\n  {'Grouping':<22} {'RAW gap':>10} {'RAW p':>8}   {'RES gap':>10} {'RES p':>8}")
    print(f"  {'-'*62}")

    for key, labels, name in groupings:
        # Re-run without printing (quick — use precomputed cos_mat)
        from phase8_trigram_decomposition import RNG as _rng
        # Just compute the gaps without permutation for the summary
        # (permutation already done above)
        norms_raw = np.linalg.norm(raw_diff, axis=1, keepdims=True)
        unit_raw = raw_diff / norms_raw
        cos_raw = unit_raw @ unit_raw.T

        norms_res = np.linalg.norm(res_diff, axis=1, keepdims=True)
        unit_res = res_diff / norms_res
        cos_res = unit_res @ unit_res.T

        groups = defaultdict(list)
        for i, g in enumerate(labels):
            groups[g].append(i)

        w_raw, b_raw, w_res, b_res = [], [], [], []
        for g, indices in groups.items():
            for i, j in combinations(indices, 2):
                w_raw.append(cos_raw[i, j])
                w_res.append(cos_res[i, j])
        for i in range(32):
            for j in range(i+1, 32):
                if labels[i] != labels[j]:
                    b_raw.append(cos_raw[i, j])
                    b_res.append(cos_res[i, j])

        gap_raw = np.mean(w_raw) - np.mean(b_raw) if w_raw else 0
        gap_res = np.mean(w_res) - np.mean(b_res) if w_res else 0
        print(f"  {name:<22} {gap_raw:>+10.4f} {'':>8}   {gap_res:>+10.4f} {'':>8}")

    print(f"\n  If RAW gaps are near zero or positive while RES gaps are negative:")
    print(f"  → Anti-clustering is a residual-space artifact")
    print(f"  If both show similar negative gaps:")
    print(f"  → Anti-clustering is a genuine text property")


if __name__ == '__main__':
    main()
