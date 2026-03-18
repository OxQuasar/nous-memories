#!/usr/bin/env python3
"""
Corrected Residual Extraction + d=2 Retest + Reversal Opposition
=================================================================
Part 1: Residualize at 384 (line-level), THEN average to centroids.
        Retest d1/d2 vs complement opposition.
Part 2: Reversal opposition in residual space.
"""

import sys
import json
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy.stats import spearmanr

# Import phase1 functions for correct residualization
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "reversal" / "Q1"))
from phase1_residual_structure import load_data as _load_phase1, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
N_PERM = 10_000
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']


def popcount(x):
    return bin(x).count('1')


def cosine_sim(a, b):
    d = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)
    return d


def cosine_dist(a, b):
    return 1.0 - cosine_sim(a, b)


def d1_neighbors(h):
    return [h ^ (1 << k) for k in range(6)]


def d2_neighbors(h):
    return [h ^ (1 << j) ^ (1 << k) for j, k in combinations(range(6), 2)]


# ── Data loading ─────────────────────────────────────────────

def load_all():
    atlas = json.load(open(ATLAS_PATH))

    # Phase1 meta + design matrix (384 lines, shared across models)
    _, meta, _ = _load_phase1()
    X, feat_names = build_design_matrix(meta)

    # Complement pairs
    comp_pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            comp_pairs.append(pair)
            seen.add(pair)

    # KW pairs
    kw_to_hex = {v['kw_number']: int(k) for k, v in atlas.items() if k.isdigit()}
    kw_pairs = [(kw_to_hex[2*i - 1], kw_to_hex[2*i]) for i in range(1, 33)]

    return atlas, X, comp_pairs, kw_pairs, kw_to_hex


def compute_residual_centroids(model_name, X):
    """Load embeddings, residualize at 384 lines, average to 64 centroids."""
    emb = np.load(Q1_DIR / f"embeddings_{model_name}.npz")['yaoci']
    resid, r2, _ = extract_residuals(emb, X)
    cents = np.array([resid[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    return cents, r2


# ══════════════════════════════════════════════════════════════
# PART 1: Corrected d=1/d=2 vs Complement Opposition
# ══════════════════════════════════════════════════════════════

def part1(atlas, X, comp_pairs):
    print("=" * 80)
    print("PART 1: CORRECTED RESIDUAL EXTRACTION + d=1/d=2 RETEST")
    print("  Residualize at 384 lines (R² ≈ 11%), then average to 64 centroids")
    print("=" * 80)
    print()

    results = {}
    for mname in MODEL_ORDER:
        cents, r2 = compute_residual_centroids(mname, X)

        d1_diff = np.zeros(N_HEX)
        d2_diff = np.zeros(N_HEX)
        comp_opp = np.zeros(N_HEX)

        for h in range(N_HEX):
            d1_diff[h] = np.mean([cosine_dist(cents[h], cents[n]) for n in d1_neighbors(h)])
            d2_diff[h] = np.mean([cosine_dist(cents[h], cents[n]) for n in d2_neighbors(h)])
            comp_opp[h] = cosine_dist(cents[h], cents[atlas[str(h)]['complement']])

        rho1, p1 = spearmanr(d1_diff, comp_opp)
        rho2, p2 = spearmanr(d2_diff, comp_opp)

        # Complement symmetry
        d1_h = np.array([d1_diff[h1] for h1, h2 in comp_pairs])
        d1_c = np.array([d1_diff[h2] for h1, h2 in comp_pairs])
        rho_sym, _ = spearmanr(d1_h, d1_c)

        results[mname] = {
            'r2': r2, 'rho1': rho1, 'p1': p1, 'rho2': rho2, 'p2': p2,
            'rho_sym': rho_sym, 'cents': cents,
            'd1_diff': d1_diff, 'd2_diff': d2_diff, 'comp_opp': comp_opp,
        }

        sig1 = "***" if p1 < 0.001 else "**" if p1 < 0.01 else "*" if p1 < 0.05 else ""
        sig2 = "***" if p2 < 0.001 else "**" if p2 < 0.01 else "*" if p2 < 0.05 else ""

        print(f"  {mname}:  R²={r2:.4f}")
        print(f"    ρ(d1_diff, comp_opp) = {rho1:+.4f} (p={p1:.4f}) {sig1}")
        print(f"    ρ(d2_diff, comp_opp) = {rho2:+.4f} (p={p2:.4f}) {sig2}")
        print(f"    d1 complement symmetry: ρ = {rho_sym:+.4f}")
        print(f"    d1_diff: mean={d1_diff.mean():.4f}, std={d1_diff.std():.4f}")
        print(f"    d2_diff: mean={d2_diff.mean():.4f}, std={d2_diff.std():.4f}")
        print(f"    comp_opp: mean={comp_opp.mean():.4f}, std={comp_opp.std():.4f}")
        print()

    # Summary table
    print("  CROSS-MODEL SUMMARY (Part 1):")
    print(f"  {'Model':14s} | {'R²':>6s} | {'ρ(d1,co)':>9s} {'p':>7s} | {'ρ(d2,co)':>9s} {'p':>7s} | {'ρ_sym':>6s}")
    print("  " + "-" * 70)
    n_sig_d1 = 0
    n_sig_d2 = 0
    for mname in MODEL_ORDER:
        r = results[mname]
        s1 = "***" if r['p1'] < 0.001 else "**" if r['p1'] < 0.01 else "*" if r['p1'] < 0.05 else ""
        s2 = "***" if r['p2'] < 0.001 else "**" if r['p2'] < 0.01 else "*" if r['p2'] < 0.05 else ""
        if r['p1'] < 0.05: n_sig_d1 += 1
        if r['p2'] < 0.05: n_sig_d2 += 1
        print(f"  {mname:14s} | {r['r2']:.4f} | {r['rho1']:+9.4f} {r['p1']:6.4f}{s1:>3s} | "
              f"{r['rho2']:+9.4f} {r['p2']:6.4f}{s2:>3s} | {r['rho_sym']:+6.3f}")
    print(f"\n  d1 sig: {n_sig_d1}/4, d2 sig: {n_sig_d2}/4")
    print()

    return results


# ══════════════════════════════════════════════════════════════
# PART 2: Reversal Opposition in Residual Space
# ══════════════════════════════════════════════════════════════

def classify_kw_pairs(atlas, kw_pairs):
    """Classify 32 KW pairs into palindrome-complement, anti-palindrome, pure-reversal."""
    palindrome = []      # both self-reverse → paired by complement
    anti_palindrome = []  # rev(h) == comp(h) for both
    pure_reversal = []    # paired by reversal

    for h1, h2 in kw_pairs:
        r1 = atlas[str(h1)]['reverse']
        r2 = atlas[str(h2)]['reverse']
        c1 = atlas[str(h1)]['complement']
        c2 = atlas[str(h2)]['complement']

        if r1 == h1 and r2 == h2:
            palindrome.append((h1, h2))
        elif r1 == c1 and r2 == c2:
            anti_palindrome.append((h1, h2))
        else:
            pure_reversal.append((h1, h2))

    return palindrome, anti_palindrome, pure_reversal


def part2(atlas, X, kw_pairs, comp_pairs, part1_results):
    print("=" * 80)
    print("PART 2: REVERSAL OPPOSITION IN RESIDUAL SPACE")
    print("=" * 80)
    print()

    palindrome, anti_palindrome, pure_reversal = classify_kw_pairs(atlas, kw_pairs)

    print(f"  2a. KW PAIR CLASSIFICATION:")
    print(f"    Palindrome-complement: {len(palindrome)} pairs")
    print(f"    Anti-palindrome:       {len(anti_palindrome)} pairs")
    print(f"    Pure-reversal:         {len(pure_reversal)} pairs")
    print(f"    Total:                 {len(kw_pairs)} pairs")
    print()

    # Hamming distances for pure-reversal
    pr_hamming = {}
    for h1, h2 in pure_reversal:
        d = popcount(h1 ^ h2)
        pr_hamming.setdefault(d, []).append((h1, h2))

    print("    Pure-reversal Hamming distances:")
    for d in sorted(pr_hamming):
        print(f"      d={d}: {len(pr_hamming[d])} pairs")
    print()

    # Non-palindrome-complement pairs: complement pairs excluding palindrome hexagrams
    palindrome_hexes = set()
    for h1, h2 in palindrome:
        palindrome_hexes.add(h1)
        palindrome_hexes.add(h2)
    non_pal_comp = [(h1, h2) for h1, h2 in comp_pairs
                    if h1 not in palindrome_hexes and h2 not in palindrome_hexes]
    print(f"    Non-palindrome complement pairs: {len(non_pal_comp)}")
    print()

    # Run for each model
    for mname in MODEL_ORDER:
        cents = part1_results[mname]['cents']

        print(f"  --- {mname} ---")
        print()

        # 2b. Group statistics
        groups = {
            'pure-reversal': pure_reversal,
            'non-pal-complement': non_pal_comp,
            'anti-palindrome': anti_palindrome,
            'palindrome-complement': palindrome,
        }

        print(f"    2b. GROUP STATISTICS (residual cosine similarity):")
        print(f"    {'Group':25s} | {'n':>3s} | {'mean':>7s} {'std':>7s} {'min':>7s} {'max':>7s}")
        print("    " + "-" * 60)

        group_sims = {}
        for gname, gpairs in groups.items():
            sims = np.array([cosine_sim(cents[h1], cents[h2]) for h1, h2 in gpairs])
            group_sims[gname] = sims
            print(f"    {gname:25s} | {len(sims):3d} | {sims.mean():+7.4f} {sims.std():7.4f} "
                  f"{sims.min():+7.4f} {sims.max():+7.4f}")
        print()

        # 2c. Permutation test for pure-reversal
        pr_sims = group_sims['pure-reversal']
        observed_mean = pr_sims.mean()

        # Null: random pairing of the 48 non-palindrome hexagrams
        non_pal_hexes = sorted(set(h for pair in pure_reversal for h in pair))
        assert len(non_pal_hexes) == 48, f"Expected 48, got {len(non_pal_hexes)}"

        rng = np.random.default_rng(42)
        null_means = np.zeros(N_PERM)
        for t in range(N_PERM):
            perm = rng.permutation(non_pal_hexes)
            null_sims = [cosine_sim(cents[perm[2*i]], cents[perm[2*i+1]]) for i in range(24)]
            null_means[t] = np.mean(null_sims)

        # Two-sided p-value
        p_above = np.mean(null_means >= observed_mean)
        p_below = np.mean(null_means <= observed_mean)
        p_two = 2 * min(p_above, p_below)
        p_two = min(p_two, 1.0)

        print(f"    2c. PERMUTATION TEST (pure-reversal, 10K null):")
        print(f"      Observed mean cos: {observed_mean:+.4f}")
        print(f"      Null mean ± std:   {null_means.mean():+.4f} ± {null_means.std():.4f}")
        print(f"      Null range:        [{null_means.min():+.4f}, {null_means.max():+.4f}]")
        print(f"      p (two-sided):     {p_two:.4f}")
        if p_two < 0.05:
            direction = "more similar" if observed_mean > null_means.mean() else "more opposed"
            print(f"      ◄ SIGNIFICANT: reversal pairs are {direction} than random")
        else:
            print(f"      Not significant")
        print()

        # 2d. R159 profile comparison
        # Full Hamming spectrum (all 2016 pairs)
        all_pairs = [(h1, h2) for h1 in range(N_HEX) for h2 in range(h1+1, N_HEX)]
        spectrum = {}
        for h1, h2 in all_pairs:
            d = popcount(h1 ^ h2)
            spectrum.setdefault(d, []).append(cosine_sim(cents[h1], cents[h2]))

        print(f"    2d. R159 PROFILE COMPARISON:")
        print(f"    {'d':>4s} | {'all-pairs mean':>14s} | {'PR subset mean':>14s} {'n_PR':>5s} | {'deviation':>10s}")
        print("    " + "-" * 60)

        for d in sorted(pr_hamming):
            all_mean = np.mean(spectrum[d])
            pr_subset = [cosine_sim(cents[h1], cents[h2]) for h1, h2 in pr_hamming[d]]
            pr_mean = np.mean(pr_subset)
            dev = pr_mean - all_mean
            print(f"    {d:4d} | {all_mean:+14.4f} | {pr_mean:+14.4f} {len(pr_subset):5d} | {dev:+10.4f}")

        print()

    # ── Cross-model summary for Part 2 ──
    print("=" * 80)
    print("PART 2 CROSS-MODEL SUMMARY")
    print("=" * 80)
    print()

    print(f"  {'Model':14s} | {'PR mean cos':>11s} {'null mean':>10s} {'p':>7s} | {'PR-comp':>8s} {'NPC-comp':>9s}")
    print("  " + "-" * 70)

    for mname in MODEL_ORDER:
        cents = part1_results[mname]['cents']

        pr_sims = np.array([cosine_sim(cents[h1], cents[h2]) for h1, h2 in pure_reversal])
        npc_sims = np.array([cosine_sim(cents[h1], cents[h2]) for h1, h2 in non_pal_comp])

        non_pal_hexes = sorted(set(h for pair in pure_reversal for h in pair))
        rng = np.random.default_rng(42)
        null_means = np.zeros(N_PERM)
        for t in range(N_PERM):
            perm = rng.permutation(non_pal_hexes)
            null_sims = [cosine_sim(cents[perm[2*i]], cents[perm[2*i+1]]) for i in range(24)]
            null_means[t] = np.mean(null_sims)

        p_two = 2 * min(np.mean(null_means >= pr_sims.mean()),
                        np.mean(null_means <= pr_sims.mean()))
        p_two = min(p_two, 1.0)

        sig = "***" if p_two < 0.001 else "**" if p_two < 0.01 else "*" if p_two < 0.05 else ""
        print(f"  {mname:14s} | {pr_sims.mean():+11.4f} {null_means.mean():+10.4f} {p_two:6.4f}{sig:>3s} | "
              f"{pr_sims.mean():+8.4f} {npc_sims.mean():+9.4f}")

    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    atlas, X, comp_pairs, kw_pairs, kw_to_hex = load_all()

    p1_results = part1(atlas, X, comp_pairs)
    part2(atlas, X, kw_pairs, comp_pairs, p1_results)

    # Final verdict
    print("=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)
    print()
    print("  Part 1: Does the d=2 anti-coupling survive correct residualization?")
    print("  Part 2: Do KW reversal pairs show thematic structure beyond random?")


if __name__ == "__main__":
    main()
