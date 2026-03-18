#!/usr/bin/env python3
"""
Thread A: Partial Spearman correlations — is d=3's sign flip independent or echo of d=2?
Thread B: Permutation test — is d=2 coupling specific to text-vertex assignment?
"""

import sys
import json
import numpy as np
from pathlib import Path
from scipy.stats import spearmanr, rankdata, t as t_dist

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "reversal" / "Q1"))
from phase1_residual_structure import load_data as _load_phase1, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']
N_PERM = 1000

def cosine_dist(a, b):
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)

def dk_neighbors(h, k):
    return [x for x in range(N_HEX) if bin(h ^ x).count('1') == k]

def sig_marker(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "** "
    if p < 0.05:  return "*  "
    return "   "

def partial_spearman(x, y, z):
    """Rank-based partial Spearman ρ(X, Y | Z) with t-test p-value."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    # Regress ranks on control
    rz_centered = rz - rz.mean()
    beta_x = np.dot(rx, rz_centered) / np.dot(rz_centered, rz_centered)
    beta_y = np.dot(ry, rz_centered) / np.dot(rz_centered, rz_centered)
    res_x = rx - beta_x * rz_centered - rx.mean()
    res_y = ry - beta_y * rz_centered - ry.mean()
    rho = np.dot(res_x, res_y) / (np.linalg.norm(res_x) * np.linalg.norm(res_y) + 1e-12)
    # t-test: df = n - 3
    n = len(x)
    df = n - 3
    t_val = rho * np.sqrt(df) / np.sqrt(1 - rho**2 + 1e-12)
    p_val = 2 * t_dist.sf(abs(t_val), df)
    return rho, p_val

# ── Data loading ─────────────────────────────────────────────────────

def load_and_compute():
    atlas = json.load(open(ATLAS_PATH))
    _, meta, _ = _load_phase1()
    X, _ = build_design_matrix(meta)

    # Precompute neighbor lists
    neighbors = {k: {h: dk_neighbors(h, k) for h in range(N_HEX)} for k in range(1, 6)}

    results = {}
    for mname in MODEL_ORDER:
        emb = np.load(Q1_DIR / f"embeddings_{mname}.npz")['yaoci']
        resid, r2, _ = extract_residuals(emb, X)
        cents = np.array([resid[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])

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

        results[mname] = {'cents': cents, 'dk_diff': dk_diff, 'comp_opp': comp_opp, 'r2': r2}

    return results, neighbors

# ══════════════════════════════════════════════════════════════════════
# THREAD A: Partial correlations
# ══════════════════════════════════════════════════════════════════════

def thread_a(results):
    print("=" * 80)
    print("THREAD A: Partial Spearman correlations")
    print("=" * 80)

    # A1: ρ(d_k, comp_opp | d2) for k=1,3,4,5
    print("\n  A1: ρ(d_k_diff, comp_opp | d2_diff) — controlling for d=2")
    print(f"  {'Model':14s} | {'d=1':>10s} {'d=3':>10s} {'d=4':>10s} {'d=5':>10s}")
    print("  " + "-" * 58)

    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        co = results[mname]['comp_opp']
        row = f"  {mname:14s} |"
        for k in [1, 3, 4, 5]:
            rho, p = partial_spearman(dk[k], co, dk[2])
            row += f" {rho:+.3f}{sig_marker(p)}"
        print(row)

    # A2: ρ(d2, comp_opp | d3) — does d=2 survive controlling for d=3?
    print(f"\n  A2: ρ(d2_diff, comp_opp | d3_diff) — does d=2 survive controlling for d=3?")
    print(f"  {'Model':14s} | {'partial ρ':>10s} {'p':>8s}")
    print("  " + "-" * 35)

    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        co = results[mname]['comp_opp']
        rho, p = partial_spearman(dk[2], co, dk[3])
        print(f"  {mname:14s} | {rho:+10.4f} {p:8.4f} {sig_marker(p)}")

    # A3: ρ(d2, comp_opp | d4) — is the d2/d4 anticorrelation confounding?
    print(f"\n  A3: ρ(d2_diff, comp_opp | d4_diff) — controlling for d=4")
    print(f"  {'Model':14s} | {'partial ρ':>10s} {'p':>8s}")
    print("  " + "-" * 35)

    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        co = results[mname]['comp_opp']
        rho, p = partial_spearman(dk[2], co, dk[4])
        print(f"  {mname:14s} | {rho:+10.4f} {p:8.4f} {sig_marker(p)}")

    # A4: Full partial table — every pair controlling for every other
    print(f"\n  A4: Bivariate vs partial ρ comparison")
    print(f"  {'Model':14s} | {'k':>2s} | {'bivariate':>10s} | {'| d2':>10s} | {'| d3':>10s} | {'| d2,d3':>10s}")
    print("  " + "-" * 70)

    for mname in MODEL_ORDER:
        dk = results[mname]['dk_diff']
        co = results[mname]['comp_opp']
        for k in range(1, 6):
            rho_biv, p_biv = spearmanr(dk[k], co)

            if k == 2:
                rho_cd2, p_cd2 = rho_biv, p_biv  # can't control for self
                rho_cd3, p_cd3 = partial_spearman(dk[k], co, dk[3])
                # Control for both d3
                r2_str = f"     —    "
                r3_str = f"{rho_cd3:+.3f}{sig_marker(p_cd3)}"
                r23_str = f"     —    "
            elif k == 3:
                rho_cd2, p_cd2 = partial_spearman(dk[k], co, dk[2])
                rho_cd3, p_cd3 = rho_biv, p_biv
                r2_str = f"{rho_cd2:+.3f}{sig_marker(p_cd2)}"
                r3_str = f"     —    "
                r23_str = f"     —    "
            else:
                rho_cd2, p_cd2 = partial_spearman(dk[k], co, dk[2])
                rho_cd3, p_cd3 = partial_spearman(dk[k], co, dk[3])
                # Multiple control: regress on both d2 and d3
                rz = np.column_stack([rankdata(dk[2]), rankdata(dk[3])])
                rx = rankdata(dk[k])
                ry = rankdata(co)
                rz_c = rz - rz.mean(axis=0)
                # OLS residuals
                beta_x = np.linalg.lstsq(rz_c, rx - rx.mean(), rcond=None)[0]
                beta_y = np.linalg.lstsq(rz_c, ry - ry.mean(), rcond=None)[0]
                res_x = rx - rx.mean() - rz_c @ beta_x
                res_y = ry - ry.mean() - rz_c @ beta_y
                rho_both = np.dot(res_x, res_y) / (np.linalg.norm(res_x) * np.linalg.norm(res_y) + 1e-12)
                df = N_HEX - 4
                t_val = rho_both * np.sqrt(df) / np.sqrt(1 - rho_both**2 + 1e-12)
                p_both = 2 * t_dist.sf(abs(t_val), df)
                r2_str = f"{rho_cd2:+.3f}{sig_marker(p_cd2)}"
                r3_str = f"{rho_cd3:+.3f}{sig_marker(p_cd3)}"
                r23_str = f"{rho_both:+.3f}{sig_marker(p_both)}"

            if k in [2, 3]:
                print(f"  {mname:14s} | d={k} | {rho_biv:+.3f}{sig_marker(p_biv)} | {r2_str} | {r3_str} | {r23_str}")
            else:
                print(f"  {mname:14s} | d={k} | {rho_biv:+.3f}{sig_marker(p_biv)} | {r2_str} | {r3_str} | {r23_str}")
        print("  " + "-" * 70)


# ══════════════════════════════════════════════════════════════════════
# THREAD B: Permutation test
# ══════════════════════════════════════════════════════════════════════

def thread_b(results, neighbors):
    print()
    print("=" * 80)
    print("THREAD B: Permutation test — is coupling specific to text-vertex assignment?")
    print(f"  {N_PERM} random permutations of centroid-to-vertex mapping")
    print("=" * 80)

    rng = np.random.default_rng(42)

    for mname in MODEL_ORDER:
        cents = results[mname]['cents']
        actual_rhos = {}

        # Actual ρ values (already computed, but recompute for consistency)
        for k in range(1, 6):
            actual_rhos[k], _ = spearmanr(results[mname]['dk_diff'][k], results[mname]['comp_opp'])

        # Null distribution
        null_rhos = {k: np.zeros(N_PERM) for k in range(1, 6)}

        for t in range(N_PERM):
            perm = rng.permutation(N_HEX)
            # perm[v] = which original centroid sits at vertex v
            perm_cents = cents[perm]

            for k in range(1, 6):
                dk_diff_perm = np.array([
                    np.mean([cosine_dist(perm_cents[h], perm_cents[n]) for n in neighbors[k][h]])
                    for h in range(N_HEX)
                ])
                comp_opp_perm = np.array([
                    cosine_dist(perm_cents[h], perm_cents[h ^ 63])
                    for h in range(N_HEX)
                ])
                null_rhos[k][t], _ = spearmanr(dk_diff_perm, comp_opp_perm)

        # Report
        print(f"\n  {mname}:")
        print(f"    {'k':>3s} | {'actual ρ':>9s} | {'null mean':>9s} {'null std':>9s} | {'percentile':>10s} {'p-value':>8s}")
        print("    " + "-" * 60)

        for k in range(1, 6):
            actual = actual_rhos[k]
            null_mean = null_rhos[k].mean()
            null_std = null_rhos[k].std()
            # One-sided p-value (how often is null ≤ actual for negative ρ)
            pctl = np.mean(null_rhos[k] <= actual) * 100
            # Two-sided p-value
            p_two = 2 * min(np.mean(null_rhos[k] <= actual), np.mean(null_rhos[k] >= actual))
            p_two = min(p_two, 1.0)
            print(f"    d={k} | {actual:+9.4f} | {null_mean:+9.4f} {null_std:9.4f} | {pctl:9.1f}% {p_two:7.4f} {sig_marker(p_two)}")

    # Cross-model summary
    print("\n  CROSS-MODEL SUMMARY (permutation two-sided p-values):")
    print(f"  {'Model':14s} |", end="")
    for k in range(1, 6):
        print(f" {'d='+str(k):>8s}", end="")
    print()
    print("  " + "-" * 60)

    for mname in MODEL_ORDER:
        cents = results[mname]['cents']
        actual_rhos = {}
        for k in range(1, 6):
            actual_rhos[k], _ = spearmanr(results[mname]['dk_diff'][k], results[mname]['comp_opp'])

        # Recompute null (use same seed for consistency)
        rng2 = np.random.default_rng(42)
        null_rhos = {k: np.zeros(N_PERM) for k in range(1, 6)}
        for t in range(N_PERM):
            perm = rng2.permutation(N_HEX)
            perm_cents = cents[perm]
            for k in range(1, 6):
                dk_diff_perm = np.array([
                    np.mean([cosine_dist(perm_cents[h], perm_cents[n]) for n in neighbors[k][h]])
                    for h in range(N_HEX)
                ])
                comp_opp_perm = np.array([
                    cosine_dist(perm_cents[h], perm_cents[h ^ 63])
                    for h in range(N_HEX)
                ])
                null_rhos[k][t], _ = spearmanr(dk_diff_perm, comp_opp_perm)

        row = f"  {mname:14s} |"
        for k in range(1, 6):
            p_two = 2 * min(np.mean(null_rhos[k] <= actual_rhos[k]),
                           np.mean(null_rhos[k] >= actual_rhos[k]))
            p_two = min(p_two, 1.0)
            row += f" {p_two:7.4f}{sig_marker(p_two)[:1]}"
        print(row)


# ══════════════════════════════════════════════════════════════════════

def main():
    results, neighbors = load_and_compute()
    thread_a(results)
    thread_b(results, neighbors)

if __name__ == "__main__":
    main()
