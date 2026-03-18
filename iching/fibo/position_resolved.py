#!/usr/bin/env python3
"""
Position-Resolved Opposition and Differentiation
==================================================
A: Complement opposition by line position (6 positions × 4 models)
B: d=1 differentiation by bit position (6 bits × 4 models)
C: 升↔无妄 per-position profile
D: Cross-model consistency
"""

import json
import numpy as np
from pathlib import Path
from itertools import combinations
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
SYNTH_PATH = ROOT / "synthesis" / "embeddings.npz"
Q1_DIR = ROOT / "reversal" / "Q1"

N_HEX = 64
N_LINES = 6
N_PERM = 10_000

MODEL_PATHS = {
    'bge-m3':      Q1_DIR / "embeddings_bge-m3.npz",
    'e5-large':    Q1_DIR / "embeddings_e5-large.npz",
    'labse':       Q1_DIR / "embeddings_labse.npz",
    'sikuroberta': Q1_DIR / "embeddings_sikuroberta.npz",
}
MODEL_ORDER = list(MODEL_PATHS.keys())

H_SHENG = 6    # 升, KW#46
H_WUWANG = 57  # 无妄, KW#25


def load_data():
    atlas = json.load(open(ATLAS_PATH))

    # Complement pairs (h_lo < h_hi)
    pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)
    assert len(pairs) == 32

    # Load all models
    models = {}
    for name, path in MODEL_PATHS.items():
        models[name] = np.load(path)['yaoci']

    return atlas, pairs, models


def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)


def cosine_dist(a, b):
    return 1.0 - cosine_sim(a, b)


def centroids(emb):
    """(384, d) → (64, d)."""
    return np.array([emb[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])


# ══════════════════════════════════════════════════════════════
# PART A: Position-Resolved Complement Opposition
# ══════════════════════════════════════════════════════════════

def part_a(models, pairs):
    print("=" * 80)
    print("PART A: POSITION-RESOLVED COMPLEMENT OPPOSITION")
    print("  Mean cosine similarity between complement pairs at each line position")
    print("=" * 80)
    print()

    # profiles[model] = [mean_cos_L1, ..., mean_cos_L6]
    profiles = {}

    hdr = f"{'Position':>10s}"
    for m in MODEL_ORDER:
        hdr += f" | {m:>12s}"
    print(hdr)
    print("-" * len(hdr))

    for k in range(1, 7):
        row = f"{'L' + str(k):>10s}"
        for m in MODEL_ORDER:
            emb = models[m]
            # Extract position k for all hexagrams
            pos_emb = emb[k-1::6]  # indices k-1, k-1+6, k-1+12, ... → 64 embeddings
            assert pos_emb.shape[0] == N_HEX

            cos_vals = [cosine_sim(pos_emb[h1], pos_emb[h2]) for h1, h2 in pairs]
            mean_cos = np.mean(cos_vals)
            profiles.setdefault(m, []).append(mean_cos)
            row += f" | {mean_cos:12.4f}"
        print(row)

    # Range per model
    print()
    row = f"{'Range':>10s}"
    for m in MODEL_ORDER:
        r = max(profiles[m]) - min(profiles[m])
        row += f" | {r:12.4f}"
    print(row)

    # Argmax/argmin
    row_max = f"{'Argmax':>10s}"
    row_min = f"{'Argmin':>10s}"
    for m in MODEL_ORDER:
        row_max += f" | {'L' + str(np.argmax(profiles[m]) + 1):>12s}"
        row_min += f" | {'L' + str(np.argmin(profiles[m]) + 1):>12s}"
    print(row_max)
    print(row_min)
    print()

    return profiles


# ══════════════════════════════════════════════════════════════
# PART B: Position-Resolved d=1 Differentiation
# ══════════════════════════════════════════════════════════════

def part_b(models, pairs):
    print("=" * 80)
    print("PART B: d=1 DIFFERENTIATION BY BIT POSITION")
    print("  Mean cosine distance between centroid(h) and centroid(h XOR bit_j)")
    print("=" * 80)
    print()

    # Precompute centroids per model
    cents = {m: centroids(models[m]) for m in MODEL_ORDER}

    # Precompute null distribution (shared across bit positions)
    # Null: random pairings of 64 hexagrams into 32 pairs
    rng = np.random.default_rng(42)
    null_dists = {m: [] for m in MODEL_ORDER}
    for _ in range(N_PERM):
        perm = rng.permutation(N_HEX)
        random_pairs = [(perm[2*i], perm[2*i+1]) for i in range(32)]
        for m in MODEL_ORDER:
            c = cents[m]
            dists = [cosine_dist(c[a], c[b]) for a, b in random_pairs]
            null_dists[m].append(np.mean(dists))
    for m in MODEL_ORDER:
        null_dists[m] = np.array(null_dists[m])

    # Actual d=1 distances
    diff_profiles = {}

    hdr = f"{'Bit pos':>10s}"
    for m in MODEL_ORDER:
        hdr += f" | {'dist':>7s} {'p':>7s}"
    print(hdr)
    print("-" * len(hdr))

    for j in range(1, 7):
        bit_mask = 1 << (j - 1)
        row = f"{'flip L' + str(j):>10s}"

        for m in MODEL_ORDER:
            c = cents[m]
            # 32 unique pairs: h < h XOR mask
            d1_pairs = []
            for h in range(N_HEX):
                h2 = h ^ bit_mask
                if h < h2:
                    d1_pairs.append((h, h2))
            assert len(d1_pairs) == 32

            dists = [cosine_dist(c[a], c[b]) for a, b in d1_pairs]
            actual_mean = np.mean(dists)
            diff_profiles.setdefault(m, []).append(actual_mean)

            p_val = (np.sum(null_dists[m] >= actual_mean) + 1) / (N_PERM + 1)
            row += f" | {actual_mean:7.4f} {p_val:7.4f}"

        print(row)

    print()

    # Null distribution summary
    print("  Null distribution (random pairing mean cosine distance):")
    for m in MODEL_ORDER:
        nd = null_dists[m]
        print(f"    {m:14s}: mean={nd.mean():.4f}, std={nd.std():.4f}, "
              f"[{nd.min():.4f}, {nd.max():.4f}]")
    print()

    return diff_profiles


# ══════════════════════════════════════════════════════════════
# PART C: 升↔无妄 Per-Position
# ══════════════════════════════════════════════════════════════

def part_c(models, pairs):
    print("=" * 80)
    print("PART C: 升↔无妄 PER-POSITION PROFILE")
    print(f"  升 = hex {H_SHENG} (KW#46), 无妄 = hex {H_WUWANG} (KW#25)")
    print("=" * 80)
    print()

    # Find pair index
    sw_pair = (min(H_SHENG, H_WUWANG), max(H_SHENG, H_WUWANG))
    sw_idx = pairs.index(sw_pair)

    for m in MODEL_ORDER:
        emb = models[m]
        print(f"  {m}:")
        print(f"  {'Position':>10s} | {'cos(升,无妄)':>12s} | {'rank':>6s} | {'mean (32)':>10s} {'std':>8s}")
        print("  " + "-" * 55)

        for k in range(1, 7):
            pos_emb = emb[k-1::6]
            e_sheng = pos_emb[H_SHENG]
            e_wuwang = pos_emb[H_WUWANG]
            sw_cos = cosine_sim(e_sheng, e_wuwang)

            # All 32 pair cosines at this position
            all_cos = [cosine_sim(pos_emb[h1], pos_emb[h2]) for h1, h2 in pairs]
            # Rank 1 = lowest cosine (most opposed)
            sorted_idx = np.argsort(all_cos)
            rank = sorted_idx.tolist().index(sw_idx) + 1

            print(f"  {'L' + str(k):>10s} | {sw_cos:12.4f} | {rank:4d}/32 | "
                  f"{np.mean(all_cos):10.4f} {np.std(all_cos):8.4f}")

        print()


# ══════════════════════════════════════════════════════════════
# PART D: Cross-Model Consistency
# ══════════════════════════════════════════════════════════════

def part_d(a_profiles, b_profiles, models):
    print("=" * 80)
    print("PART D: CROSS-MODEL CONSISTENCY")
    print("=" * 80)
    print()

    model_pairs = list(combinations(MODEL_ORDER, 2))

    # Part A consistency
    print("  Part A (opposition profile) cross-model Spearman ρ:")
    rhos_a = []
    for m1, m2 in model_pairs:
        rho, p = spearmanr(a_profiles[m1], a_profiles[m2])
        rhos_a.append(rho)
        sig = " *" if p < 0.05 else ""
        print(f"    {m1:14s} × {m2:14s}: ρ={rho:+.4f} (p={p:.4f}){sig}")
    print(f"    Mean ρ: {np.mean(rhos_a):+.4f}")
    print()

    # Part B consistency
    print("  Part B (differentiation profile) cross-model Spearman ρ:")
    rhos_b = []
    for m1, m2 in model_pairs:
        rho, p = spearmanr(b_profiles[m1], b_profiles[m2])
        rhos_b.append(rho)
        sig = " *" if p < 0.05 else ""
        print(f"    {m1:14s} × {m2:14s}: ρ={rho:+.4f} (p={p:.4f}){sig}")
    print(f"    Mean ρ: {np.mean(rhos_b):+.4f}")
    print()

    # A vs B correlation per model
    print("  Opposition profile (A) vs Differentiation profile (B) per model:")
    print("  (Do positions with stronger opposition also show stronger differentiation?)")
    print()
    for m in MODEL_ORDER:
        # A profile: higher cos → less opposition. Negate for "opposition strength".
        opp_strength = [-x for x in a_profiles[m]]
        diff_strength = b_profiles[m]
        rho, p = spearmanr(opp_strength, diff_strength)
        print(f"    {m:14s}: ρ(opposition, differentiation) = {rho:+.4f} (p={p:.4f})")
    print()


# ══════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════

def summary(a_profiles, b_profiles):
    print("=" * 80)
    print("SUMMARY ASSESSMENT")
    print("=" * 80)
    print()

    # Q1: Opposition flat or concentrated?
    print("  Q1: Is complement opposition flat or position-dependent?")
    ranges = {m: max(a_profiles[m]) - min(a_profiles[m]) for m in MODEL_ORDER}
    mean_range = np.mean(list(ranges.values()))
    mean_mean = np.mean([np.mean(a_profiles[m]) for m in MODEL_ORDER])
    cv = mean_range / mean_mean * 100
    print(f"      Mean range across models: {mean_range:.4f}")
    print(f"      As % of mean cosine: {cv:.1f}%")
    if cv < 5:
        print(f"      → FLAT: opposition is holistic, not position-concentrated")
    elif cv < 15:
        print(f"      → MILD variation: some positional modulation")
    else:
        print(f"      → STRONG variation: opposition is position-dependent")
    print()

    # Q2: Differentiation flat or concentrated?
    print("  Q2: Is d=1 differentiation flat or bit-position-dependent?")
    d_ranges = {m: max(b_profiles[m]) - min(b_profiles[m]) for m in MODEL_ORDER}
    d_mean_range = np.mean(list(d_ranges.values()))
    d_mean_mean = np.mean([np.mean(b_profiles[m]) for m in MODEL_ORDER])
    d_cv = d_mean_range / d_mean_mean * 100
    print(f"      Mean range across models: {d_mean_range:.4f}")
    print(f"      As % of mean distance: {d_cv:.1f}%")
    if d_cv < 10:
        print(f"      → FLAT: all bit flips produce similar differentiation")
    elif d_cv < 30:
        print(f"      → MILD variation: some bit positions differentiate more")
    else:
        print(f"      → STRONG variation: differentiation is bit-position-dependent")
    print()

    # Q3: A-B correlation already handled in part_d
    print("  Q3: A-B correlation printed in Part D above.")
    print()

    # Q4: 升↔无妄
    print("  Q4: 升↔无妄 anomaly assessment — see Part C ranks.")
    print("      If ranks cluster near 16/32 (median) → uniformly unremarkable.")
    print("      If ranks cluster at extremes → positionally anomalous.")
    print()


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

def main():
    atlas, pairs, models = load_data()

    a_profiles = part_a(models, pairs)
    b_profiles = part_b(models, pairs)
    part_c(models, pairs)
    part_d(a_profiles, b_profiles, models)
    summary(a_profiles, b_profiles)


if __name__ == "__main__":
    main()
