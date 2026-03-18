#!/usr/bin/env python3
"""
Centroid Geometry Artifact Check & Conditional Follow-ups
==========================================================
Check 1: Does text length correlate with distance-to-centroid-mean?
         (If yes → text-length probe may be an embedding artifact)
Check 2: Do complement pairs have more asymmetric text lengths than random pairs?
Check 3: (Conditional) Does negation retain signal after partialing out text length?
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent          # memories/iching
TEXTS = ROOT.parent / "texts" / "iching"
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"
SYNTH_DIR = ROOT / "synthesis"

N_HEX = 64
N_LINES = 6
N_PERM = 10_000
MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']

# ── Reuse data loading from semantic_probes ──────────────────

def load_atlas():
    atlas = json.load(open(ATLAS_PATH))
    hex_to_kw = {int(k): v['kw_number'] for k, v in atlas.items() if k.isdigit()}
    return atlas, hex_to_kw

def load_complement_pairs(atlas):
    pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)
    assert len(pairs) == 32
    return pairs

def load_texts_by_hex(hex_to_kw):
    yaoci_data = json.load(open(TEXTS / "yaoci.json"))['entries']
    guaci_data = json.load(open(TEXTS / "guaci.json"))['entries']
    yaoci_by_kw = {e['number']: e for e in yaoci_data}
    guaci_by_kw = {e['number']: e for e in guaci_data}

    yaoci_texts, guaci_texts = {}, {}
    for h in range(N_HEX):
        kw = hex_to_kw[h]
        yaoci_texts[h] = [line['text'] for line in yaoci_by_kw[kw]['lines']]
        guaci_texts[h] = guaci_by_kw[kw]['text']
    return yaoci_texts, guaci_texts

def load_embeddings():
    models = {}
    for name in MODEL_ORDER:
        data = np.load(Q1_DIR / f"embeddings_{name}.npz")
        models[name] = {'yaoci': data['yaoci']}
    synth = np.load(SYNTH_DIR / "embeddings.npz")
    models['bge-m3']['guaci'] = synth['guaci']
    return models

def compute_centroids(yaoci_emb):
    return np.array([yaoci_emb[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])

def count_tokens(text, tokens):
    return sum(text.count(tok) for tok in tokens)

def probe_r2(centroids, scores, pairs):
    scores = np.array(scores, dtype=float)
    if np.std(scores) < 1e-10:
        return 0.0, np.zeros(len(pairs))

    scores_centered = scores - scores.mean()
    denom = np.sum(scores_centered ** 2)
    beta = centroids.T @ scores_centered / denom
    probe_dir = beta / np.linalg.norm(beta)

    diffs = np.array([centroids[h1] - centroids[h2] for h1, h2 in pairs])
    projections = diffs @ probe_dir

    total_var = np.sum(diffs ** 2)
    probe_var = np.sum(projections ** 2)
    return probe_var / total_var, projections

def permutation_test(centroids, scores, pairs, n_perm=N_PERM):
    r2_actual, projections = probe_r2(centroids, scores, pairs)
    rng = np.random.default_rng(42)
    scores_arr = np.array(scores)
    n_ge = sum(
        1 for _ in range(n_perm)
        if probe_r2(centroids, rng.permutation(scores_arr), pairs)[0] >= r2_actual
    )
    return r2_actual, (n_ge + 1) / (n_perm + 1), projections


# ══════════════════════════════════════════════════════════════
# CHECK 1: Centroid Geometry Artifact
# ══════════════════════════════════════════════════════════════

def check1(models, yaoci_texts, guaci_texts):
    print("=" * 80)
    print("CHECK 1: CENTROID GEOMETRY ARTIFACT")
    print("  Does text length correlate with distance-to-global-mean?")
    print("  (Negative ρ → longer texts → centroid closer to mean → artifact)")
    print("=" * 80)
    print()

    # Yaoci text lengths per hexagram
    yaoci_lengths = [sum(len(line) for line in yaoci_texts[h]) for h in range(N_HEX)]
    guaci_lengths = [len(guaci_texts[h]) for h in range(N_HEX)]

    print(f"  Yaoci lengths: min={min(yaoci_lengths)}, max={max(yaoci_lengths)}, "
          f"mean={np.mean(yaoci_lengths):.1f}, std={np.std(yaoci_lengths):.1f}")
    print(f"  Guaci lengths: min={min(guaci_lengths)}, max={max(guaci_lengths)}, "
          f"mean={np.mean(guaci_lengths):.1f}, std={np.std(guaci_lengths):.1f}")
    print()

    print("  YAOCI (centroid = mean of 6 line embeddings per hexagram):")
    print(f"  {'Model':14s} | {'ρ(len, dist)':>12s} {'p':>10s} | {'ρ(len, norm)':>12s} {'p':>10s} | Interpretation")
    print("  " + "-" * 85)

    yaoci_results = {}
    for mname in MODEL_ORDER:
        centroids = compute_centroids(models[mname]['yaoci'])
        global_mean = centroids.mean(axis=0)

        # Distance to global mean (Euclidean)
        dists = np.linalg.norm(centroids - global_mean, axis=1)

        # Also check centroid norm (in case embeddings aren't centered)
        norms = np.linalg.norm(centroids, axis=1)

        rho_dist, p_dist = spearmanr(yaoci_lengths, dists)
        rho_norm, p_norm = spearmanr(yaoci_lengths, norms)

        interp = ""
        if abs(rho_dist) > 0.3 and p_dist < 0.05:
            interp = "◄ ARTIFACT RISK" if rho_dist < 0 else "◄ POSITIVE (unexpected)"
        else:
            interp = "Clean"

        print(f"  {mname:14s} | {rho_dist:+12.4f} {p_dist:10.4f} | {rho_norm:+12.4f} {p_norm:10.4f} | {interp}")
        yaoci_results[mname] = (rho_dist, p_dist)

    print()

    # Guaci (only bge-m3 has guaci embeddings)
    print("  GUACI (single embedding per hexagram):")
    print(f"  {'Model':14s} | {'ρ(len, dist)':>12s} {'p':>10s} | {'ρ(len, norm)':>12s} {'p':>10s} | Interpretation")
    print("  " + "-" * 85)

    guaci_results = {}
    if 'guaci' in models['bge-m3']:
        mname = 'bge-m3'
        centroids = models[mname]['guaci']
        global_mean = centroids.mean(axis=0)
        dists = np.linalg.norm(centroids - global_mean, axis=1)
        norms = np.linalg.norm(centroids, axis=1)

        rho_dist, p_dist = spearmanr(guaci_lengths, dists)
        rho_norm, p_norm = spearmanr(guaci_lengths, norms)

        interp = ""
        if abs(rho_dist) > 0.3 and p_dist < 0.05:
            interp = "◄ ARTIFACT RISK" if rho_dist < 0 else "◄ POSITIVE (unexpected)"
        else:
            interp = "Clean"

        print(f"  {mname:14s} | {rho_dist:+12.4f} {p_dist:10.4f} | {rho_norm:+12.4f} {p_norm:10.4f} | {interp}")
        guaci_results[mname] = (rho_dist, p_dist)

    print()

    # Additional diagnostic: for each model, show distance distribution stats
    print("  DISTANCE DISTRIBUTION (yaoci centroids to global mean):")
    print(f"  {'Model':14s} | {'min':>8s} {'median':>8s} {'max':>8s} {'std':>8s} | {'emb dim':>7s}")
    print("  " + "-" * 65)
    for mname in MODEL_ORDER:
        centroids = compute_centroids(models[mname]['yaoci'])
        global_mean = centroids.mean(axis=0)
        dists = np.linalg.norm(centroids - global_mean, axis=1)
        d = centroids.shape[1]
        print(f"  {mname:14s} | {dists.min():8.4f} {np.median(dists):8.4f} {dists.max():8.4f} {dists.std():8.4f} | {d:7d}")
    print()

    # Scatter data for the strongest correlation
    worst_model = min(yaoci_results, key=lambda m: yaoci_results[m][0])
    rho_worst, p_worst = yaoci_results[worst_model]
    print(f"  Strongest negative: {worst_model} ρ={rho_worst:+.4f} (p={p_worst:.4f})")
    print()

    return yaoci_results, guaci_results


# ══════════════════════════════════════════════════════════════
# CHECK 2: Complement Text-Length Asymmetry
# ══════════════════════════════════════════════════════════════

def check2(pairs, yaoci_texts, guaci_texts):
    print("=" * 80)
    print("CHECK 2: COMPLEMENT TEXT-LENGTH ASYMMETRY")
    print("  Do complement pairs have more asymmetric text lengths than random pairs?")
    print("=" * 80)
    print()

    for layer_name, get_length in [
        ("yaoci", lambda h: sum(len(line) for line in yaoci_texts[h])),
        ("guaci", lambda h: len(guaci_texts[h])),
    ]:
        lengths = np.array([get_length(h) for h in range(N_HEX)])

        # Actual complement asymmetry
        actual_diffs = np.array([abs(lengths[h1] - lengths[h2]) for h1, h2 in pairs])
        actual_mean = actual_diffs.mean()
        actual_max = actual_diffs.max()

        # Null: random pairings
        rng = np.random.default_rng(42)
        null_means = []
        for _ in range(N_PERM):
            perm = rng.permutation(N_HEX)
            null_pairs = [(perm[2*i], perm[2*i+1]) for i in range(32)]
            null_diffs = [abs(lengths[a] - lengths[b]) for a, b in null_pairs]
            null_means.append(np.mean(null_diffs))

        null_means = np.array(null_means)
        percentile = np.mean(null_means <= actual_mean) * 100
        p_val = np.mean(null_means >= actual_mean)

        print(f"  {layer_name}:")
        print(f"    Actual mean |Δlength| across 32 complement pairs: {actual_mean:.1f}")
        print(f"    Null mean |Δlength| (10K random pairings): {null_means.mean():.1f} ± {null_means.std():.1f}")
        print(f"    Percentile of actual: {percentile:.1f}%")
        print(f"    p-value (actual ≥ null): {p_val:.4f}")
        if p_val < 0.05:
            print(f"    ◄ COMPLEMENT PAIRS ARE MORE ASYMMETRIC than random")
        elif percentile < 50:
            print(f"    Complement pairs are LESS asymmetric than random (no concern)")
        else:
            print(f"    No significant asymmetry (within normal range)")
        print()

        # Show the 5 most asymmetric complement pairs
        pair_diffs = sorted(zip(pairs, actual_diffs), key=lambda x: -x[1])
        atlas = json.load(open(ATLAS_PATH))
        print(f"    Most asymmetric complement pairs ({layer_name}):")
        for (h1, h2), d in pair_diffs[:5]:
            n1 = atlas[str(h1)]['kw_name']
            n2 = atlas[str(h2)]['kw_name']
            print(f"      {n1:10s}({lengths[h1]:3d}) ↔ {n2:10s}({lengths[h2]:3d}): |Δ|={d:.0f}")
        print()


# ══════════════════════════════════════════════════════════════
# CHECK 3: Negation Partial Correlation (conditional)
# ══════════════════════════════════════════════════════════════

def check3(models, yaoci_texts, guaci_texts, pairs):
    print("=" * 80)
    print("CHECK 3: NEGATION AFTER PARTIALING OUT TEXT LENGTH")
    print("  Does negation retain complement-opposition signal after")
    print("  residualizing on text length?")
    print("=" * 80)
    print()

    NEGATION_TOKENS = ['不', '勿', '無', '非']

    for layer_name in ['yaoci', 'guaci']:
        print(f"  --- {layer_name} ---")

        if layer_name == 'yaoci':
            neg_scores = []
            length_scores = []
            for h in range(N_HEX):
                text = ''.join(yaoci_texts[h])
                neg_scores.append(count_tokens(text, NEGATION_TOKENS))
                length_scores.append(sum(len(line) for line in yaoci_texts[h]))
            model_list = MODEL_ORDER
        else:
            neg_scores = []
            length_scores = []
            for h in range(N_HEX):
                neg_scores.append(count_tokens(guaci_texts[h], NEGATION_TOKENS))
                length_scores.append(len(guaci_texts[h]))
            model_list = ['bge-m3'] if 'guaci' in models.get('bge-m3', {}) else []

        neg_scores = np.array(neg_scores, dtype=float)
        length_scores = np.array(length_scores, dtype=float)

        # Correlation between negation and text length
        rho_nl, p_nl = spearmanr(neg_scores, length_scores)
        print(f"    ρ(negation, text_length) = {rho_nl:.3f} (p={p_nl:.4f})")

        # Residualize negation on text length via OLS
        X = length_scores.reshape(-1, 1)
        X_aug = np.column_stack([X, np.ones(N_HEX)])
        beta_ols = np.linalg.lstsq(X_aug, neg_scores, rcond=None)[0]
        neg_residual = neg_scores - X_aug @ beta_ols

        print(f"    Residual negation: mean={neg_residual.mean():.4f} (≈0), "
              f"std={neg_residual.std():.3f}")
        print()

        # Run probe test with residualized negation
        for mname in model_list:
            if layer_name == 'yaoci':
                centroids = compute_centroids(models[mname]['yaoci'])
            else:
                centroids = models[mname]['guaci']

            # Raw negation probe
            r2_raw, p_raw, _ = permutation_test(centroids, neg_scores, pairs)
            # Residualized negation probe
            r2_resid, p_resid, _ = permutation_test(centroids, neg_residual, pairs)
            # Raw text length for comparison
            r2_len, p_len, _ = permutation_test(centroids, length_scores, pairs)

            sig_raw = "***" if p_raw < 0.01 else "*" if p_raw < 0.05 else ""
            sig_resid = "***" if p_resid < 0.01 else "*" if p_resid < 0.05 else ""
            sig_len = "***" if p_len < 0.01 else "*" if p_len < 0.05 else ""

            print(f"    {mname:14s}:")
            print(f"      Text length:        R²={r2_len:.4f}, p={p_len:.4f} {sig_len}")
            print(f"      Raw negation:       R²={r2_raw:.4f}, p={p_raw:.4f} {sig_raw}")
            print(f"      Resid. negation:    R²={r2_resid:.4f}, p={p_resid:.4f} {sig_resid}")

            if p_resid < 0.05:
                print(f"      → Negation RETAINS signal after controlling for text length")
            else:
                print(f"      → Negation signal ABSORBED by text length")
            print()

    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    atlas, hex_to_kw = load_atlas()
    pairs = load_complement_pairs(atlas)
    yaoci_texts, guaci_texts = load_texts_by_hex(hex_to_kw)
    models = load_embeddings()

    # Check 1
    yaoci_artifact, guaci_artifact = check1(models, yaoci_texts, guaci_texts)

    # Check 2
    check2(pairs, yaoci_texts, guaci_texts)

    # Decide on Check 3
    # Check 1 verdict: artifact if any model shows ρ < -0.3 with p < 0.05
    any_artifact = any(
        rho < -0.3 and p < 0.05
        for rho, p in yaoci_artifact.values()
    )

    if any_artifact:
        print("=" * 80)
        print("CHECK 3: SKIPPED")
        print("  Check 1 found artifact risk (strong ρ < -0.3).")
        print("  Text-length probe may reflect centroid geometry, not semantic content.")
        print("  Negation partial correlation is moot if the base signal is artifactual.")
        print("=" * 80)
    else:
        print("  Check 1 clean (no strong artifact). Proceeding to Check 3...")
        print()
        check3(models, yaoci_texts, guaci_texts, pairs)

    # Final verdict
    print("=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)
    print()

    any_neg_artifact = any(rho < -0.3 and p < 0.05 for rho, p in yaoci_artifact.values())
    any_pos = any(rho > 0.3 and p < 0.05 for rho, p in yaoci_artifact.values())

    if any_neg_artifact:
        print("  TEXT LENGTH PROBE: LIKELY ARTIFACT")
        print("  Longer texts produce centroids closer to the global mean,")
        print("  making complement difference vectors systematically larger/smaller")
        print("  based on text length rather than semantic content.")
    elif any_pos:
        print("  TEXT LENGTH PROBE: UNEXPECTED POSITIVE CORRELATION")
        print("  Longer texts have centroids FURTHER from the mean.")
        print("  Needs further investigation.")
    else:
        print("  TEXT LENGTH PROBE: NO CENTROID GEOMETRY ARTIFACT DETECTED")
        print("  Text length is uncorrelated with distance-to-mean.")
        print("  The probe R² reflects genuine semantic alignment, not embedding geometry.")


if __name__ == "__main__":
    main()
