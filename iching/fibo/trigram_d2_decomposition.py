#!/usr/bin/env python3
"""
Trigram Decomposition of the d=2 Anti-Coupling (R236)
======================================================
Decomposes the 15 d=2 neighbors into within-lower (3), within-upper (3),
and cross-trigram (9), then tests which component drives the anti-coupling
with complement opposition.

Bit convention (verified):
  bits 0-2 = lower trigram
  bits 3-5 = upper trigram
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

LOWER_BITS = {0, 1, 2}
UPPER_BITS = {3, 4, 5}


def cosine_dist(a, b):
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)


def classify_d2_neighbors():
    """Precompute d=2 neighbor classification for all 64 hexagrams.
    Returns dict: h → {'within_lower': [...], 'within_upper': [...], 'cross': [...]}
    """
    all_bit_pairs = list(combinations(range(6), 2))
    # Classify each bit pair
    within_lower_pairs = [(i, j) for i, j in all_bit_pairs if {i, j} <= LOWER_BITS]
    within_upper_pairs = [(i, j) for i, j in all_bit_pairs if {i, j} <= UPPER_BITS]
    cross_pairs = [(i, j) for i, j in all_bit_pairs
                   if not ({i, j} <= LOWER_BITS) and not ({i, j} <= UPPER_BITS)]

    assert len(within_lower_pairs) == 3, f"Got {len(within_lower_pairs)}"
    assert len(within_upper_pairs) == 3, f"Got {len(within_upper_pairs)}"
    assert len(cross_pairs) == 9, f"Got {len(cross_pairs)}"

    result = {}
    for h in range(N_HEX):
        result[h] = {
            'within_lower': [h ^ (1 << i) ^ (1 << j) for i, j in within_lower_pairs],
            'within_upper': [h ^ (1 << i) ^ (1 << j) for i, j in within_upper_pairs],
            'cross':        [h ^ (1 << i) ^ (1 << j) for i, j in cross_pairs],
        }
    return result


def compute_residual_centroids(model_name, X):
    emb = np.load(Q1_DIR / f"embeddings_{model_name}.npz")['yaoci']
    resid, r2, _ = extract_residuals(emb, X)
    cents = np.array([resid[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])
    return cents, r2


def main():
    atlas = json.load(open(ATLAS_PATH))
    _, meta, _ = _load_phase1()
    X, _ = build_design_matrix(meta)

    d2_map = classify_d2_neighbors()

    # ── Step 1: Verify bit convention ──
    print("=" * 80)
    print("STEP 1: BIT CONVENTION VERIFICATION")
    print("=" * 80)
    print()
    for h_idx in [1, 8, 7, 56]:
        d = atlas[str(h_idx)]
        print(f"  hex {h_idx:2d} ({d['binary']}): lower={d['lower_trigram']['name']}({d['lower_trigram']['val']}), "
              f"upper={d['upper_trigram']['name']}({d['upper_trigram']['val']})")
    print("  → bits 0-2 = lower trigram, bits 3-5 = upper trigram ✓")
    print()

    # ── Step 2: Verify neighbor counts ──
    print("=" * 80)
    print("STEP 2: NEIGHBOR CLASSIFICATION VERIFICATION")
    print("=" * 80)
    print()
    h_test = 21  # 010101
    nb = d2_map[h_test]
    print(f"  hex {h_test} ({atlas[str(h_test)]['binary']}):")
    print(f"    within_lower (3): {nb['within_lower']} → {[format(n,'06b') for n in nb['within_lower']]}")
    print(f"    within_upper (3): {nb['within_upper']} → {[format(n,'06b') for n in nb['within_upper']]}")
    print(f"    cross        (9): {nb['cross']}")
    all_nb = set(nb['within_lower'] + nb['within_upper'] + nb['cross'])
    assert len(all_nb) == 15, f"Got {len(all_nb)} unique neighbors"
    # Verify all are d=2
    for n in all_nb:
        assert bin(h_test ^ n).count('1') == 2
    print(f"    Total: {len(all_nb)} unique d=2 neighbors ✓")
    print()

    # ── Steps 3-4: Per-model computation ──
    print("=" * 80)
    print("STEPS 3-4: COMPONENT CORRELATIONS WITH COMPLEMENT OPPOSITION")
    print("=" * 80)
    print()

    all_model_results = {}

    for mname in MODEL_ORDER:
        cents, r2 = compute_residual_centroids(mname, X)

        d2_wl = np.zeros(N_HEX)
        d2_wu = np.zeros(N_HEX)
        d2_cr = np.zeros(N_HEX)
        d2_all = np.zeros(N_HEX)
        comp_opp = np.zeros(N_HEX)

        for h in range(N_HEX):
            nb = d2_map[h]
            d2_wl[h] = np.mean([cosine_dist(cents[h], cents[n]) for n in nb['within_lower']])
            d2_wu[h] = np.mean([cosine_dist(cents[h], cents[n]) for n in nb['within_upper']])
            d2_cr[h] = np.mean([cosine_dist(cents[h], cents[n]) for n in nb['cross']])
            d2_all[h] = np.mean([cosine_dist(cents[h], cents[n])
                                  for n in nb['within_lower'] + nb['within_upper'] + nb['cross']])
            comp_opp[h] = cosine_dist(cents[h], cents[atlas[str(h)]['complement']])

        # Correlations
        rho_wl, p_wl = spearmanr(d2_wl, comp_opp)
        rho_wu, p_wu = spearmanr(d2_wu, comp_opp)
        rho_cr, p_cr = spearmanr(d2_cr, comp_opp)
        rho_all, p_all = spearmanr(d2_all, comp_opp)

        all_model_results[mname] = {
            'r2': r2, 'rho_wl': rho_wl, 'p_wl': p_wl,
            'rho_wu': rho_wu, 'p_wu': p_wu,
            'rho_cr': rho_cr, 'p_cr': p_cr,
            'rho_all': rho_all, 'p_all': p_all,
            'd2_wl': d2_wl, 'd2_wu': d2_wu, 'd2_cr': d2_cr,
            'd2_all': d2_all, 'comp_opp': comp_opp,
        }

        sig = lambda p: "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""

        print(f"  {mname} (R²={r2:.4f}):")
        print(f"    {'Component':20s} | {'ρ':>8s} {'p':>8s} | {'mean':>8s} {'std':>8s}")
        print(f"    {'-'*60}")
        for label, rho, p, arr in [
            ("d2_within_lower", rho_wl, p_wl, d2_wl),
            ("d2_within_upper", rho_wu, p_wu, d2_wu),
            ("d2_cross", rho_cr, p_cr, d2_cr),
            ("d2_all (R236)", rho_all, p_all, d2_all),
            ("comp_opp", None, None, comp_opp),
        ]:
            if rho is not None:
                print(f"    {label:20s} | {rho:+8.4f} {p:7.4f}{sig(p):>3s} | {arr.mean():8.4f} {arr.std():8.4f}")
            else:
                print(f"    {label:20s} | {'—':>8s} {'—':>8s}    | {arr.mean():8.4f} {arr.std():8.4f}")
        print()

    # ── Step 5: Trigram imbalance ──
    print("=" * 80)
    print("STEP 5: TRIGRAM IMBALANCE")
    print("  |d2_within_lower − d2_within_upper| vs comp_opp")
    print("=" * 80)
    print()

    for mname in MODEL_ORDER:
        r = all_model_results[mname]
        imbalance = np.abs(r['d2_wl'] - r['d2_wu'])
        rho_imb, p_imb = spearmanr(imbalance, r['comp_opp'])
        sig_str = "***" if p_imb < 0.001 else "**" if p_imb < 0.01 else "*" if p_imb < 0.05 else ""
        print(f"  {mname:14s}: ρ = {rho_imb:+.4f} (p = {p_imb:.4f}) {sig_str}  "
              f"imbalance mean={imbalance.mean():.4f}, std={imbalance.std():.4f}")

    print()

    # ── Step 6: Cross-model summary ──
    print("=" * 80)
    print("STEP 6: CROSS-MODEL SUMMARY")
    print("=" * 80)
    print()

    components = [
        ("d2_within_lower", 'rho_wl', 'p_wl'),
        ("d2_within_upper", 'rho_wu', 'p_wu'),
        ("d2_cross",        'rho_cr', 'p_cr'),
        ("d2_all (R236)",   'rho_all', 'p_all'),
    ]

    sig = lambda p: "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""

    hdr = f"  {'Component':20s}"
    for m in MODEL_ORDER:
        hdr += f" | {m:>14s}"
    hdr += " | sig≥3?"
    print(hdr)
    print("  " + "-" * (22 + 17 * len(MODEL_ORDER) + 10))

    for label, rho_key, p_key in components:
        row = f"  {label:20s}"
        n_sig = 0
        for m in MODEL_ORDER:
            r = all_model_results[m]
            rho_val = r[rho_key]
            p_val = r[p_key]
            s = sig(p_val)
            if p_val < 0.05:
                n_sig += 1
            row += f" | {rho_val:+.3f}{s:>4s} p={p_val:.3f}"
        flag = " ◄ YES" if n_sig >= 3 else f"   ({n_sig}/4)"
        row += f" | {flag}"
        print(row)

    # Imbalance row
    row = f"  {'trigram_imbalance':20s}"
    n_sig_imb = 0
    for m in MODEL_ORDER:
        r = all_model_results[m]
        imb = np.abs(r['d2_wl'] - r['d2_wu'])
        rho_i, p_i = spearmanr(imb, r['comp_opp'])
        s = sig(p_i)
        if p_i < 0.05:
            n_sig_imb += 1
        row += f" | {rho_i:+.3f}{s:>4s} p={p_i:.3f}"
    flag = " ◄ YES" if n_sig_imb >= 3 else f"   ({n_sig_imb}/4)"
    row += f" | {flag}"
    print(row)

    print()

    # ── Verdict ──
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()

    # Determine which component(s) are significant
    component_sig = {}
    for label, rho_key, p_key in components:
        n = sum(1 for m in MODEL_ORDER if all_model_results[m][p_key] < 0.05)
        component_sig[label] = n

    # Compare magnitudes
    mean_rhos = {}
    for label, rho_key, _ in components:
        mean_rhos[label] = np.mean([all_model_results[m][rho_key] for m in MODEL_ORDER])

    print("  Mean ρ across models:")
    for label in mean_rhos:
        print(f"    {label:20s}: {mean_rhos[label]:+.4f}  (sig in {component_sig[label]}/4)")
    print()

    # Strongest component
    strongest = min(mean_rhos, key=mean_rhos.get)  # most negative = strongest anti-coupling
    weakest = max(mean_rhos, key=mean_rhos.get)

    print(f"  Strongest component: {strongest} (mean ρ = {mean_rhos[strongest]:+.4f})")
    print(f"  Weakest component:   {weakest} (mean ρ = {mean_rhos[weakest]:+.4f})")
    print()

    # Determine hypothesis
    wl_mean = mean_rhos["d2_within_lower"]
    wu_mean = mean_rhos["d2_within_upper"]
    cr_mean = mean_rhos["d2_cross"]
    within_mean = (wl_mean + wu_mean) / 2

    ratio = abs(cr_mean) / abs(within_mean) if abs(within_mean) > 1e-6 else float('inf')

    if ratio > 1.5:
        print(f"  HYPOTHESIS: INTERACTION-DRIVEN")
        print(f"    Cross-trigram component ({cr_mean:+.4f}) dominates within-trigram ({within_mean:+.4f})")
        print(f"    Ratio: {ratio:.2f}×")
    elif ratio < 0.67:
        print(f"  HYPOTHESIS: TRIGRAM-DEPENDENT")
        print(f"    Within-trigram component ({within_mean:+.4f}) dominates cross-trigram ({cr_mean:+.4f})")
    else:
        print(f"  HYPOTHESIS: DISTRIBUTED")
        print(f"    All components contribute similarly (ratio = {ratio:.2f})")
        print(f"    The anti-coupling is a holistic property, not trigram-specific")


if __name__ == "__main__":
    main()
