#!/usr/bin/env python3
"""
d=1 Differentiation vs Complement Opposition Unification Test
===============================================================
Are complement opposition (R156, d=6) and near-neighbor differentiation
(R159, d=1) aspects of a single design principle?

All computations use RESIDUAL embeddings (algebraic signal regressed out).
"""

import json
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy.stats import spearmanr
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']


def popcount(x):
    return bin(x).count('1')


def cosine_dist(a, b):
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)


def ols_residualize(y, x):
    """Residualize y on x via OLS."""
    X = np.column_stack([np.asarray(x, dtype=float), np.ones(len(x))])
    beta = np.linalg.lstsq(X, np.asarray(y, dtype=float), rcond=None)[0]
    return y - X @ beta


# ── Residual computation ────────────────────────────────────

def build_centroid_design_matrix(atlas):
    """Build algebraic design matrix for 64 hexagram centroids.
    Excludes line_pos (not applicable to centroids)."""
    meta = []
    for h in range(N_HEX):
        d = atlas[str(h)]
        meta.append({
            'basin': d['basin'],
            'surface_relation': d['surface_relation'],
            'palace': d['palace'],
            'palace_element': d['palace_element'],
            'rank': d['rank'],
            'depth': d['depth'],
            'i_component': d['i_component'],
            'inner_val': d['inner_val'],
            'hu_depth': d['hu_depth'],
            'shi': d['shi'],
            'ying': d['ying'],
        })

    cat_names = ['basin', 'surface_relation', 'palace', 'palace_element', 'rank']
    cat_arrays = []
    for cn in cat_names:
        vals = np.array([[m[cn]] for m in meta])
        enc = OneHotEncoder(sparse_output=False, drop='first')
        cat_arrays.append(enc.fit_transform(vals))

    num_names = ['depth', 'i_component', 'inner_val', 'hu_depth', 'shi', 'ying']
    num_array = np.array([[m[n] for n in num_names] for m in meta], dtype=float)

    X = np.hstack(cat_arrays + [num_array])
    return X


def compute_residual_centroids(yaoci_emb, atlas):
    """Compute 64 residual centroids from 384 yaoci embeddings.
    1. Average 6 lines per hexagram → 64 raw centroids
    2. Regress out algebraic coordinates → 64 residual centroids
    Returns (residual_centroids, raw_centroids, r2).
    """
    raw_cents = np.array([yaoci_emb[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    X = build_centroid_design_matrix(atlas)

    reg = LinearRegression()
    reg.fit(X, raw_cents)
    predicted = reg.predict(X)
    residual = raw_cents - predicted

    ss_res = np.sum(residual ** 2)
    ss_tot = np.sum((raw_cents - raw_cents.mean(axis=0)) ** 2)
    r2 = 1.0 - ss_res / ss_tot

    return residual, raw_cents, r2


# ── Neighbor computation ────────────────────────────────────

def d1_neighbors(h):
    """Return 6 Hamming-distance-1 neighbors."""
    return [h ^ (1 << k) for k in range(6)]


def d2_neighbors(h):
    """Return 15 Hamming-distance-2 neighbors."""
    return [h ^ (1 << j) ^ (1 << k) for j, k in combinations(range(6), 2)]


# ── Main computation ────────────────────────────────────────

def run_model(mname, atlas):
    emb = np.load(Q1_DIR / f"embeddings_{mname}.npz")['yaoci']
    resid_cents, raw_cents, r2 = compute_residual_centroids(emb, atlas)

    # Per-hexagram metrics
    d1_diff = np.zeros(N_HEX)
    d2_diff = np.zeros(N_HEX)
    comp_opp = np.zeros(N_HEX)
    ham_wt = np.zeros(N_HEX)

    for h in range(N_HEX):
        # d=1 differentiation
        d1n = d1_neighbors(h)
        d1_diff[h] = np.mean([cosine_dist(resid_cents[h], resid_cents[n]) for n in d1n])

        # d=2 differentiation
        d2n = d2_neighbors(h)
        d2_diff[h] = np.mean([cosine_dist(resid_cents[h], resid_cents[n]) for n in d2n])

        # Complement opposition
        comp_h = atlas[str(h)]['complement']
        comp_opp[h] = cosine_dist(resid_cents[h], resid_cents[comp_h])

        # Hamming weight
        ham_wt[h] = popcount(h)

    return {
        'd1_diff': d1_diff,
        'd2_diff': d2_diff,
        'comp_opp': comp_opp,
        'ham_wt': ham_wt,
        'r2_alg': r2,
        'resid_cents': resid_cents,
    }


def main():
    atlas = json.load(open(ATLAS_PATH))

    # Complement pairs
    pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)

    all_results = {}

    for mname in MODEL_ORDER:
        print(f"{'='*70}")
        print(f"Model: {mname}")
        print(f"{'='*70}")

        res = run_model(mname, atlas)
        all_results[mname] = res

        d1 = res['d1_diff']
        d2 = res['d2_diff']
        co = res['comp_opp']
        hw = res['ham_wt']

        print(f"  Algebraic R² (centroid regression): {res['r2_alg']:.4f}")
        print()

        # Step 3: Main test
        rho_d1_co, p_d1_co = spearmanr(d1, co)
        # Partial: control for Hamming weight
        resid_d1 = ols_residualize(d1, hw)
        resid_co = ols_residualize(co, hw)
        rho_partial, p_partial = spearmanr(resid_d1, resid_co)

        print(f"  Step 3 — Main test:")
        print(f"    d1_diff vs comp_opp:   ρ = {rho_d1_co:+.4f} (p = {p_d1_co:.4f})")
        print(f"    Partial (|ham_wt):     ρ = {rho_partial:+.4f} (p = {p_partial:.4f})")
        print()

        # Step 4: Monotonicity check
        rho_d2_co, p_d2_co = spearmanr(d2, co)
        print(f"  Step 4 — Monotonicity:")
        print(f"    d2_diff vs comp_opp:   ρ = {rho_d2_co:+.4f} (p = {p_d2_co:.4f})")
        print(f"    d1 vs d2 comparison:   |ρ_d1| = {abs(rho_d1_co):.4f}, |ρ_d2| = {abs(rho_d2_co):.4f}")
        if abs(rho_d1_co) > abs(rho_d2_co) + 0.05:
            print(f"    → d=1 SPECIFIC (d1 stronger than d2)")
        elif abs(rho_d2_co) > abs(rho_d1_co) + 0.05:
            print(f"    → d=2 STRONGER (unexpected)")
        else:
            print(f"    → SIMILAR magnitude (monotonic gradient)")
        print()

        # Step 5: Confound diagnostic
        d1_h = np.array([d1[h1] for h1, h2 in pairs])
        d1_c = np.array([d1[h2] for h1, h2 in pairs])
        rho_sym, p_sym = spearmanr(d1_h, d1_c)
        print(f"  Step 5 — Complement symmetry:")
        print(f"    ρ(d1_diff(h), d1_diff(σ(h))): ρ = {rho_sym:+.4f} (p = {p_sym:.4f})")
        if rho_sym > 0.5:
            print(f"    ◄ HIGH symmetry — effective n ≈ 32, not 64")
        elif rho_sym > 0.3:
            print(f"    Moderate symmetry — some effective n reduction")
        else:
            print(f"    Low symmetry — 64 hexagrams are reasonably independent")
        print()

        # Distribution stats
        print(f"  Distributions:")
        for name, arr in [("d1_diff", d1), ("d2_diff", d2), ("comp_opp", co)]:
            print(f"    {name:10s}: mean={arr.mean():.4f}, std={arr.std():.4f}, "
                  f"min={arr.min():.4f}, max={arr.max():.4f}")
        print()

    # ── Cross-model summary ──
    print("=" * 70)
    print("CROSS-MODEL SUMMARY")
    print("=" * 70)
    print()

    print(f"  {'Model':14s} | {'R²_alg':>7s} | {'ρ(d1,co)':>9s} {'p':>8s} | {'ρ partial':>10s} {'p':>8s} | {'ρ(d2,co)':>9s} {'p':>8s} | {'ρ_sym':>6s}")
    print("  " + "-" * 90)

    n_sig = 0
    for mname in MODEL_ORDER:
        res = all_results[mname]
        d1, d2, co, hw = res['d1_diff'], res['d2_diff'], res['comp_opp'], res['ham_wt']

        rho1, p1 = spearmanr(d1, co)
        resid_d1 = ols_residualize(d1, hw)
        resid_co = ols_residualize(co, hw)
        rhop, pp = spearmanr(resid_d1, resid_co)
        rho2, p2 = spearmanr(d2, co)

        d1_h = np.array([d1[h1] for h1, h2 in pairs])
        d1_c = np.array([d1[h2] for h1, h2 in pairs])
        rho_s, _ = spearmanr(d1_h, d1_c)

        sig1 = "***" if p1 < 0.001 else "**" if p1 < 0.01 else "*" if p1 < 0.05 else ""
        sigp = "***" if pp < 0.001 else "**" if pp < 0.01 else "*" if pp < 0.05 else ""
        sig2 = "***" if p2 < 0.001 else "**" if p2 < 0.01 else "*" if p2 < 0.05 else ""

        if p1 < 0.05:
            n_sig += 1

        print(f"  {mname:14s} | {res['r2_alg']:7.4f} | {rho1:+9.4f} {p1:7.4f}{sig1:>3s} | "
              f"{rhop:+10.4f} {pp:7.4f}{sigp:>3s} | {rho2:+9.4f} {p2:7.4f}{sig2:>3s} | {rho_s:+6.3f}")

    print()
    print(f"  Significant (p<0.05) in {n_sig}/4 models")
    print()

    # ── Verdict ──
    print("=" * 70)
    print("VERDICT")
    print("=" * 70)
    print()

    # Collect main rhos
    main_rhos = []
    for mname in MODEL_ORDER:
        res = all_results[mname]
        rho, _ = spearmanr(res['d1_diff'], res['comp_opp'])
        main_rhos.append(rho)

    mean_rho = np.mean(main_rhos)
    all_same_sign = all(r > 0 for r in main_rhos) or all(r < 0 for r in main_rhos)

    if n_sig >= 3 and all_same_sign:
        if mean_rho > 0:
            print("  UNIFIED: d=1 differentiation and complement opposition are")
            print("  positively coupled. Hexagrams that are more thematically")
            print("  distinct from their neighbors are also more opposed to their")
            print("  complements. The V-shape is one coherent design principle.")
        else:
            print("  ANTI-UNIFIED: d=1 differentiation and complement opposition")
            print("  are negatively coupled (unexpected).")
    elif n_sig >= 2:
        print("  TENTATIVE: partial coupling between d=1 differentiation and")
        print("  complement opposition. Not fully cross-model robust.")
    else:
        print("  INDEPENDENT: d=1 differentiation and complement opposition")
        print("  are not correlated. The V-shape peaks arise from separate mechanisms.")

    print(f"\n  Mean ρ(d1_diff, comp_opp) across models: {mean_rho:+.4f}")
    print(f"  All same sign: {all_same_sign}")


if __name__ == "__main__":
    main()
