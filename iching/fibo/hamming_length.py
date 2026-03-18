#!/usr/bin/env python3
"""
Text Length × Hamming V-Shape Connection
==========================================
Tests whether R159 (Hamming-thematic anti-correlation) and R219 (text length
as sole cross-model opposition axis) are connected.

Stage A: Does text-length difference show a V-shape across Hamming distance?
Stage B: Does R159 survive after controlling for text length?
         (Uses both raw and residual embeddings, Pearson and Spearman)

Note: R159 used RESIDUAL embeddings (algebraic signal regressed out) and
PEARSON correlation, finding r ≈ -0.10 to -0.17.
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from scipy.stats import spearmanr, pearsonr
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
TEXTS = ROOT.parent / "texts" / "iching"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
N_YAOCI = 384
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']


def popcount(x):
    return bin(x).count('1')


def cosine_dist(a, b):
    return 1.0 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)


def load_data():
    atlas = json.load(open(ATLAS_PATH))
    hex_to_kw = {int(k): v['kw_number'] for k, v in atlas.items() if k.isdigit()}

    yaoci_data = json.load(open(TEXTS / "yaoci.json"))['entries']
    guaci_data = json.load(open(TEXTS / "guaci.json"))['entries']
    yaoci_by_kw = {e['number']: e for e in yaoci_data}
    guaci_by_kw = {e['number']: e for e in guaci_data}

    yaoci_len = np.zeros(N_HEX)
    guaci_len = np.zeros(N_HEX)
    for h in range(N_HEX):
        kw = hex_to_kw[h]
        yaoci_len[h] = sum(len(line['text']) for line in yaoci_by_kw[kw]['lines'])
        guaci_len[h] = len(guaci_by_kw[kw]['text'])

    # All 2016 pairs
    pairs = [(h1, h2) for h1 in range(N_HEX) for h2 in range(h1 + 1, N_HEX)]
    assert len(pairs) == 2016

    hamming = np.array([popcount(h1 ^ h2) for h1, h2 in pairs])
    delta_yaoci = np.array([abs(yaoci_len[h1] - yaoci_len[h2]) for h1, h2 in pairs])
    delta_guaci = np.array([abs(guaci_len[h1] - guaci_len[h2]) for h1, h2 in pairs])

    # Load embeddings
    models = {}
    for name in MODEL_ORDER:
        models[name] = np.load(Q1_DIR / f"embeddings_{name}.npz")['yaoci']

    return atlas, pairs, hamming, delta_yaoci, delta_guaci, yaoci_len, guaci_len, models


def build_design_matrix(atlas):
    """Build algebraic design matrix for residualization (per yaoci, 384 rows).
    Matches phase1_residual_structure.py methodology."""
    meta = []
    for h in range(N_HEX):
        d = atlas[str(h)]
        for line in range(6):
            meta.append({
                'line_pos': line,
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

    # Categorical features
    cat_names = ['line_pos', 'basin', 'surface_relation', 'palace', 'palace_element', 'rank']
    cat_arrays = []
    for cn in cat_names:
        vals = np.array([[m[cn]] for m in meta])
        enc = OneHotEncoder(sparse_output=False, drop='first')
        cat_arrays.append(enc.fit_transform(vals))

    # Numeric features
    num_names = ['depth', 'i_component', 'inner_val', 'hu_depth', 'shi', 'ying']
    num_array = np.array([[m[n] for n in num_names] for m in meta], dtype=float)

    X = np.hstack(cat_arrays + [num_array])
    return X


def extract_residuals(yaoci_emb, X):
    """Regress out algebraic signal, return residual embeddings."""
    reg = LinearRegression()
    reg.fit(X, yaoci_emb)
    predicted = reg.predict(X)
    residual = yaoci_emb - predicted
    # R²
    ss_res = np.sum(residual ** 2)
    ss_tot = np.sum((yaoci_emb - yaoci_emb.mean(axis=0)) ** 2)
    r2 = 1 - ss_res / ss_tot
    return residual, r2


def compute_centroids(emb):
    """(384, d) → (64, d)."""
    return np.array([emb[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])


def ols_residualize(y, x):
    """OLS residualize y on x."""
    X = np.column_stack([x, np.ones(len(x))])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return y - X @ beta


# ══════════════════════════════════════════════════════════════
# STAGE A: Text-Length V-Shape Test
# ══════════════════════════════════════════════════════════════

def stage_a(hamming, delta_yaoci, delta_guaci):
    print("=" * 80)
    print("STAGE A: TEXT-LENGTH V-SHAPE TEST")
    print("  Does |Δ text_length| follow the Hamming V-shape?")
    print("=" * 80)
    print()

    for label, delta in [("yaoci", delta_yaoci), ("guaci", delta_guaci)]:
        print(f"  {label}:")
        print(f"  {'d':>4s} | {'n pairs':>8s} | {'mean |Δlen|':>12s} {'std':>8s} | {'median':>8s}")
        print("  " + "-" * 50)

        by_d = defaultdict(list)
        for i in range(len(hamming)):
            by_d[hamming[i]].append(delta[i])

        means = []
        for d in range(1, 7):
            vals = np.array(by_d[d])
            means.append(np.mean(vals))
            print(f"  {d:4d} | {len(vals):8d} | {np.mean(vals):12.2f} {np.std(vals):8.2f} | {np.median(vals):8.1f}")

        v_peak = (means[0] + means[5]) / 2
        v_trough = (means[2] + means[3]) / 2
        print()
        print(f"    Peak avg (d=1,6): {v_peak:.2f}")
        print(f"    Trough avg (d=3,4): {v_trough:.2f}")
        ratio = v_peak / v_trough if v_trough > 0 else float('inf')
        print(f"    Ratio peak/trough: {ratio:.3f}")
        if ratio > 1.10:
            print(f"    → V-SHAPE PRESENT ({(ratio-1)*100:.0f}% elevation)")
        else:
            print(f"    → NO V-SHAPE (flat: ratio < 1.10)")

        rho, p = spearmanr(hamming, delta)
        print(f"    ρ(d, |Δlen|) = {rho:+.4f} (p={p:.4f})")
        print()


# ══════════════════════════════════════════════════════════════
# STAGE B: Hamming-Thematic Correlation & Partial Correlation
# ══════════════════════════════════════════════════════════════

def stage_b(atlas, pairs, hamming, delta_yaoci, models):
    print("=" * 80)
    print("STAGE B: HAMMING-THEMATIC CORRELATION (RAW + RESIDUAL)")
    print("  R159 used residual embeddings + Pearson. We test both.")
    print("=" * 80)
    print()

    hamming_f = hamming.astype(float)
    delta_f = delta_yaoci.astype(float)

    # Build design matrix (shared across models)
    X = build_design_matrix(atlas)

    # Exclude complement pairs (d=6) for the "excl comp" measure
    non_comp_mask = hamming_f < 6
    n_nc = non_comp_mask.sum()

    # ── B1: Raw embeddings ──
    print("  B1: RAW EMBEDDINGS")
    print(f"  {'Model':14s} | {'r (all)':>8s} {'p':>9s} | {'r (excl d=6)':>13s} {'p':>9s} | {'ρ (all)':>8s} {'p':>9s}")
    print("  " + "-" * 80)

    raw_results = {}
    for mname in MODEL_ORDER:
        cents = compute_centroids(models[mname])
        tdist = np.array([cosine_dist(cents[h1], cents[h2]) for h1, h2 in pairs])

        r_all, p_all = pearsonr(hamming_f, tdist)
        r_nc, p_nc = pearsonr(hamming_f[non_comp_mask], tdist[non_comp_mask])
        rho_all, prho = spearmanr(hamming_f, tdist)

        sig_all = "***" if p_all < 0.001 else ""
        sig_nc = "***" if p_nc < 0.001 else ""
        sig_rho = "***" if prho < 0.001 else ""

        print(f"  {mname:14s} | {r_all:+8.4f} {p_all:8.2e}{sig_all:>3s} | "
              f"{r_nc:+13.4f} {p_nc:8.2e}{sig_nc:>3s} | {rho_all:+8.4f} {prho:8.2e}{sig_rho:>3s}")
        raw_results[mname] = (r_all, r_nc, rho_all, tdist)

    print()

    # ── B2: Residual embeddings ──
    print("  B2: RESIDUAL EMBEDDINGS (algebraic signal regressed out)")
    print(f"  {'Model':14s} | {'R²_alg':>7s} | {'r (all)':>8s} {'p':>9s} | {'r (excl d=6)':>13s} {'p':>9s}")
    print("  " + "-" * 70)

    resid_results = {}
    for mname in MODEL_ORDER:
        resid, r2 = extract_residuals(models[mname], X)
        cents_r = compute_centroids(resid)
        tdist_r = np.array([cosine_dist(cents_r[h1], cents_r[h2]) for h1, h2 in pairs])

        r_all, p_all = pearsonr(hamming_f, tdist_r)
        r_nc, p_nc = pearsonr(hamming_f[non_comp_mask], tdist_r[non_comp_mask])

        sig_all = "***" if p_all < 0.001 else "**" if p_all < 0.01 else "*" if p_all < 0.05 else ""
        sig_nc = "***" if p_nc < 0.001 else "**" if p_nc < 0.01 else "*" if p_nc < 0.05 else ""

        print(f"  {mname:14s} | {r2:7.3f} | {r_all:+8.4f} {p_all:8.2e}{sig_all:>3s} | "
              f"{r_nc:+13.4f} {p_nc:8.2e}{sig_nc:>3s}")
        resid_results[mname] = (r2, r_all, r_nc, tdist_r)

    print()

    # ── B3: V-shape spectra ──
    print("  B3: HAMMING SPECTRA (mean thematic distance by d)")
    print()

    for tag, results_dict, use_resid in [("RAW", raw_results, False), ("RESIDUAL", resid_results, True)]:
        print(f"    {tag}:")
        print(f"    {'Model':14s} | {'d=1':>8s} {'d=2':>8s} {'d=3':>8s} {'d=4':>8s} {'d=5':>8s} {'d=6':>8s}")
        print("    " + "-" * 70)

        for mname in MODEL_ORDER:
            tdist = results_dict[mname][-1]
            by_d = defaultdict(list)
            for i in range(len(hamming)):
                by_d[hamming[i]].append(tdist[i])
            means = [np.mean(by_d[d]) for d in range(1, 7)]
            # Normalize by overall mean for comparison
            overall_mean = np.mean(tdist)
            ratios = [m / overall_mean for m in means]
            print(f"    {mname:14s} | {' '.join(f'{r:8.4f}' for r in ratios)}  (×mean)")

        print()

    # ── B4: Partial correlation (controlling for text length) ──
    print("  B4: PARTIAL CORRELATION (control: |Δ yaoci_length|)")
    print()

    for tag, results_dict in [("RAW", raw_results), ("RESIDUAL", resid_results)]:
        print(f"    {tag} embeddings:")
        print(f"    {'Model':14s} | {'r':>8s} {'p':>9s} | {'r|Δlen':>8s} {'p':>9s} | {'reduction':>10s}")
        print("    " + "-" * 60)

        for mname in MODEL_ORDER:
            tdist = results_dict[mname][-1]

            # Raw Pearson
            r_raw, p_raw = pearsonr(hamming_f, tdist)

            # Partial: residualize both on delta_length
            resid_h = ols_residualize(hamming_f, delta_f)
            resid_t = ols_residualize(tdist, delta_f)
            r_partial, p_partial = pearsonr(resid_h, resid_t)

            if abs(r_raw) > 1e-10:
                red = (abs(r_raw) - abs(r_partial)) / abs(r_raw) * 100
            else:
                red = 0.0

            sig_r = "***" if p_raw < 0.001 else "**" if p_raw < 0.01 else "*" if p_raw < 0.05 else ""
            sig_p = "***" if p_partial < 0.001 else "**" if p_partial < 0.01 else "*" if p_partial < 0.05 else ""

            print(f"    {mname:14s} | {r_raw:+8.4f} {p_raw:8.2e}{sig_r:>3s} | "
                  f"{r_partial:+8.4f} {p_partial:8.2e}{sig_p:>3s} | {red:+9.1f}%")

        print()

    # ── Auxiliary correlations ──
    print("  AUXILIARY CORRELATIONS:")
    rho_dlen_ham, p_dlen_ham = spearmanr(hamming_f, delta_f)
    print(f"    ρ(hamming_d, |Δ yaoci_len|) = {rho_dlen_ham:+.4f} (p={p_dlen_ham:.4f})")

    for mname in MODEL_ORDER:
        tdist = raw_results[mname][-1]
        rho_dlen_t, p_dlen_t = spearmanr(delta_f, tdist)
        print(f"    ρ(|Δlen|, raw_thematic_dist) [{mname}] = {rho_dlen_t:+.4f} (p={p_dlen_t:.2e})")

    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    atlas, pairs, hamming, delta_yaoci, delta_guaci, yaoci_len, guaci_len, models = load_data()

    stage_a(hamming, delta_yaoci, delta_guaci)
    stage_b(atlas, pairs, hamming, delta_yaoci, models)

    # Verdict
    print("=" * 80)
    print("VERDICT")
    print("=" * 80)
    print()
    print("  Q1: Does |Δ text_length| show a V-shape across Hamming distance?")
    print("  Q2: Does the Hamming-thematic anti-correlation (R159) survive")
    print("      after controlling for text length?")
    print("  Q3: Are R159 and R219 independent or connected?")


if __name__ == "__main__":
    main()
