#!/usr/bin/env python3
"""
Complete distance profile: ρ(d_k_diff, comp_opp) for k=1..5

Extends R235/R236 to full Hamming distance spectrum.
Tests whether d=2 anti-coupling is specific or part of monotonic gradient.
Includes complement symmetry tests at two levels.
"""

import sys
import json
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "reversal" / "Q1"))
from phase1_residual_structure import load_data as _load_phase1, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']

# ── Helpers ──────────────────────────────────────────────────────────

def cosine_dist(a, b):
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

def dk_neighbors(h, k):
    """All hexagrams at Hamming distance exactly k from h."""
    return [x for x in range(N_HEX) if bin(h ^ x).count('1') == k]

def sig_marker(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "** "
    if p < 0.05:  return "*  "
    return "   "

# ── Data loading ─────────────────────────────────────────────────────

def load_all():
    atlas = json.load(open(ATLAS_PATH))
    _, meta, _ = _load_phase1()
    X, _ = build_design_matrix(meta)
    return atlas, X

def compute_residual_centroids(model_name, X):
    emb = np.load(Q1_DIR / f"embeddings_{model_name}.npz")['yaoci']
    resid, r2, _ = extract_residuals(emb, X)
    cents = np.array([resid[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    return cents, r2

# ── Main computation ─────────────────────────────────────────────────

def main():
    atlas, X = load_all()

    # Precompute neighbor lists for k=1..5
    neighbors = {}
    for k in range(1, 6):
        neighbors[k] = {h: dk_neighbors(h, k) for h in range(N_HEX)}
        n_neigh = len(neighbors[k][0])
        print(f"  d={k}: {n_neigh} neighbors per hexagram")

    # Verify: C(6,1)=6, C(6,2)=15, C(6,3)=20, C(6,4)=15, C(6,5)=6
    print()

    # ══════════════════════════════════════════════════════════════════
    # PART 1: Full distance profile
    # ══════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 1: ρ(d_k_diff, comp_opp) for k=1..5, all models")
    print("=" * 80)
    print()

    # Store results for later analysis
    all_results = {}

    for mname in MODEL_ORDER:
        cents, r2 = compute_residual_centroids(mname, X)

        # Compute d_k_diff for each k and comp_opp
        dk_diff = {}
        for k in range(1, 6):
            dk_diff[k] = np.array([
                np.mean([cosine_dist(cents[h], cents[n]) for n in neighbors[k][h]])
                for h in range(N_HEX)
            ])

        comp_opp = np.array([
            cosine_dist(cents[h], cents[atlas[str(h)]['complement']])
            for h in range(N_HEX)
        ])

        # Spearman correlations
        rhos = {}
        for k in range(1, 6):
            rho, p = spearmanr(dk_diff[k], comp_opp)
            rhos[k] = (rho, p)

        all_results[mname] = {
            'r2': r2, 'rhos': rhos, 'dk_diff': dk_diff,
            'comp_opp': comp_opp, 'cents': cents
        }

        print(f"  {mname} (R²={r2:.4f}):")
        for k in range(1, 6):
            rho, p = rhos[k]
            print(f"    ρ(d{k}_diff, comp_opp) = {rho:+.4f}  p={p:.4f} {sig_marker(p)}")
        print()

    # Summary table
    print("  SUMMARY TABLE:")
    header = f"  {'Model':14s} |"
    for k in range(1, 6):
        header += f" {'d='+str(k):>10s}"
    print(header)
    print("  " + "-" * 72)

    for mname in MODEL_ORDER:
        row = f"  {mname:14s} |"
        for k in range(1, 6):
            rho, p = all_results[mname]['rhos'][k]
            row += f" {rho:+.3f}{sig_marker(p)}"
        print(row)

    # Count significance
    print()
    print("  Significant (p<0.05) count per distance:")
    for k in range(1, 6):
        n_sig = sum(1 for m in MODEL_ORDER if all_results[m]['rhos'][k][1] < 0.05)
        print(f"    d={k}: {n_sig}/4 models")

    # ══════════════════════════════════════════════════════════════════
    # PART 2: Profile shape analysis
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("PART 2: Profile shape — monotonic vs d=2 specific vs complement-symmetric")
    print("=" * 80)
    print()

    for mname in MODEL_ORDER:
        rhos = all_results[mname]['rhos']
        profile = [rhos[k][0] for k in range(1, 6)]

        # Test monotonicity: is |ρ(k+1)| > |ρ(k)| for all k?
        abs_profile = [abs(r) for r in profile]
        monotonic = all(abs_profile[i+1] >= abs_profile[i] for i in range(4))

        # Peak location
        peak_k = abs_profile.index(max(abs_profile)) + 1

        # Complement symmetry: compare ρ(k) vs ρ(6-k)
        sym_pairs = [(1, 5), (2, 4)]

        print(f"  {mname}:")
        print(f"    |ρ| profile: {['%.3f' % r for r in abs_profile]}")
        print(f"    Monotonic increasing: {monotonic}")
        print(f"    Peak at d={peak_k}")
        for k1, k2 in sym_pairs:
            print(f"    ρ(d{k1}) vs ρ(d{k2}): {rhos[k1][0]:+.4f} vs {rhos[k2][0]:+.4f}  "
                  f"(diff = {abs(rhos[k1][0] - rhos[k2][0]):.4f})")
        print()

    # ══════════════════════════════════════════════════════════════════
    # PART 3: Complement symmetry — per-hexagram level
    # ══════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 3: Per-hexagram complement symmetry")
    print("  Test: ρ(d_k_diff(h), d_{6-k}_diff(σ(h))) across 64 hexagrams")
    print("  Structural prediction: σ(N_k(h)) = N_{6-k}(σ(h))")
    print("=" * 80)
    print()

    # First verify the structural prediction algebraically
    print("  Algebraic verification: σ(N_k(h)) = N_{6-k}(σ(h))?")
    violations = 0
    for h in range(N_HEX):
        comp_h = 63 ^ h
        for k in range(1, 6):
            nk = set(neighbors[k][h])
            comp_nk = {63 ^ x for x in nk}
            n6mk_comp = set(neighbors[6 - k][comp_h])
            if comp_nk != n6mk_comp:
                violations += 1
    print(f"    Violations: {violations} (should be 0)")
    print()

    # Now test in embedding space
    print("  Per-hexagram tests:")
    header = f"  {'Model':14s} |"
    for k in range(1, 4):  # k=1,2,3 (3 is self-paired with 3)
        k2 = 6 - k
        header += f" ρ(d{k},d{k2}) "
    print(header)
    print("  " + "-" * 60)

    for mname in MODEL_ORDER:
        dk_diff = all_results[mname]['dk_diff']
        row = f"  {mname:14s} |"

        for k in range(1, 4):
            k2 = 6 - k
            # d_k_diff(h) vs d_{6-k}_diff(σ(h))
            vals_a = np.array([dk_diff[k][h] for h in range(N_HEX)])
            vals_b = np.array([dk_diff[k2][63 ^ h] for h in range(N_HEX)])
            rho, p = spearmanr(vals_a, vals_b)
            row += f"  {rho:+.3f}{sig_marker(p)}"
        print(row)

    # Also: d_k_diff(h) vs d_k_diff(σ(h)) — same-distance complement symmetry
    print()
    print("  Same-distance complement symmetry: ρ(d_k_diff(h), d_k_diff(σ(h)))")
    header = f"  {'Model':14s} |"
    for k in range(1, 6):
        header += f"  d={k:1d}   "
    print(header)
    print("  " + "-" * 72)

    for mname in MODEL_ORDER:
        dk_diff = all_results[mname]['dk_diff']
        row = f"  {mname:14s} |"
        for k in range(1, 6):
            vals_h = np.array([dk_diff[k][h] for h in range(N_HEX)])
            vals_c = np.array([dk_diff[k][63 ^ h] for h in range(N_HEX)])
            rho, p = spearmanr(vals_h, vals_c)
            row += f" {rho:+.3f}{sig_marker(p)}"
        print(row)

    # ══════════════════════════════════════════════════════════════════
    # PART 4: Raw statistics for each distance
    # ══════════════════════════════════════════════════════════════════
    print()
    print("=" * 80)
    print("PART 4: Descriptive statistics of d_k_diff vectors")
    print("=" * 80)
    print()

    for mname in MODEL_ORDER:
        dk_diff = all_results[mname]['dk_diff']
        comp_opp = all_results[mname]['comp_opp']
        print(f"  {mname}:")
        print(f"    {'k':>3s}  {'mean':>8s}  {'std':>8s}  {'min':>8s}  {'max':>8s}  {'cv':>8s}")
        for k in range(1, 6):
            v = dk_diff[k]
            print(f"    d={k}  {v.mean():.5f}  {v.std():.5f}  {v.min():.5f}  {v.max():.5f}  {v.std()/v.mean():.5f}")
        v = comp_opp
        print(f"    comp {v.mean():.5f}  {v.std():.5f}  {v.min():.5f}  {v.max():.5f}  {v.std()/v.mean():.5f}")
        print()

    # ══════════════════════════════════════════════════════════════════
    # PART 5: Inter-distance correlations
    # ══════════════════════════════════════════════════════════════════
    print("=" * 80)
    print("PART 5: Inter-distance correlations ρ(d_j_diff, d_k_diff)")
    print("  Tests whether d_k_diff vectors are redundant or independent")
    print("=" * 80)
    print()

    for mname in MODEL_ORDER:
        dk_diff = all_results[mname]['dk_diff']
        print(f"  {mname}:")
        header = "      "
        for k in range(1, 6):
            header += f"  d={k:1d}  "
        print(header)
        for j in range(1, 6):
            row = f"    d={j}"
            for k in range(1, 6):
                if k <= j:
                    row += "       "
                else:
                    rho, _ = spearmanr(dk_diff[j], dk_diff[k])
                    row += f" {rho:+.3f} "
            print(row)
        print()


if __name__ == "__main__":
    main()
