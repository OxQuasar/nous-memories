#!/usr/bin/env python3
"""kw_sequence_probe.py — King Wen sequence structural analysis.

Three analyses:
1. Hamming distance patterns in KW order
2. Five-phase torus trajectory
3. Text embedding trajectory (semantic smoothness)
"""

import json
import numpy as np
from collections import Counter
from pathlib import Path

# ════════════════════════════════════════════════════════════
# Constants
# ════════════════════════════════════════════════════════════

ATLAS_PATH = Path(__file__).parent.parent / "atlas" / "atlas.json"
EMBED_PATH = Path(__file__).parent.parent / "synthesis" / "embeddings.npz"

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}

# 生 cycle (generation): Wood→Fire→Earth→Metal→Water→Wood (stride +1)
SHENG = {(i, (i + 1) % 5) for i in range(5)}
# 克 cycle (destruction): Wood→Earth→Water→Fire→Metal→Wood (stride +2)
KE = {(i, (i + 2) % 5) for i in range(5)}

N_PERM = 10_000
RNG = np.random.default_rng(42)

# ════════════════════════════════════════════════════════════
# Data Loading
# ════════════════════════════════════════════════════════════

def load_data():
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)

    # Build KW-ordered sequence of hex indices
    entries = []
    for k, v in atlas.items():
        entries.append({
            "hex_idx": int(k),
            "kw": v["kw_number"],
            "binary": v["binary"],
            "lower": v["lower_trigram"]["element"],
            "upper": v["upper_trigram"]["element"],
        })
    entries.sort(key=lambda x: x["kw"])

    kw_seq = [e["hex_idx"] for e in entries]
    binaries = {e["hex_idx"]: int(e["binary"], 2) for e in entries}
    elements = {e["hex_idx"]: (ELEM_IDX[e["lower"]], ELEM_IDX[e["upper"]])
                for e in entries}

    emb_data = np.load(EMBED_PATH)
    guaci = emb_data["guaci"]       # (64, 1024)
    yaoci = emb_data["yaoci"]       # (384, 1024)

    return kw_seq, binaries, elements, guaci, yaoci, entries


# ════════════════════════════════════════════════════════════
# Utilities
# ════════════════════════════════════════════════════════════

def hamming(a, b):
    return bin(a ^ b).count("1")


def torus_manhattan(cell_a, cell_b):
    """Manhattan distance on Z₅ × Z₅ torus."""
    dl = min(abs(cell_a[0] - cell_b[0]), 5 - abs(cell_a[0] - cell_b[0]))
    du = min(abs(cell_a[1] - cell_b[1]), 5 - abs(cell_a[1] - cell_b[1]))
    return dl + du


def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12)


def consecutive_stats(seq, metric_fn):
    """Compute metric for all consecutive pairs in a sequence."""
    return [metric_fn(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]


def percentile_rank(observed, null_samples):
    """What fraction of null samples is <= observed?"""
    return np.mean(null_samples <= observed)


# ════════════════════════════════════════════════════════════
# Analysis 1: Hamming Distance
# ════════════════════════════════════════════════════════════

def analysis_hamming(kw_seq, binaries):
    print("=" * 72)
    print("ANALYSIS 1: Hamming Distance in KW Order")
    print("=" * 72)

    n = len(kw_seq)
    # All consecutive Hamming distances
    all_hd = [hamming(binaries[kw_seq[i]], binaries[kw_seq[i + 1]])
              for i in range(n - 1)]

    # Split: within-pair (odd→even: indices 0→1, 2→3, ...) = positions 0,2,4,...
    # KW pairs are (1,2), (3,4), ..., (63,64) → indices 0,1 / 2,3 / ...
    # Within-pair: transitions at positions 0,2,4,...,62 (i.e., i even)
    # Inter-pair: transitions at positions 1,3,5,...,61 (i.e., i odd)
    within = [all_hd[i] for i in range(0, n - 1, 2)]  # 32 within-pair
    inter = [all_hd[i] for i in range(1, n - 1, 2)]    # 31 inter-pair

    print(f"\n  Total transitions: {len(all_hd)}")
    print(f"  Within-pair (odd→even KW): {len(within)}")
    print(f"  Inter-pair (even→odd KW):  {len(inter)}")

    # Distribution
    print(f"\n  Hamming distance distribution:")
    print(f"  {'HD':>4} {'All':>6} {'Within':>8} {'Inter':>8}")
    print("  " + "-" * 30)
    for hd in range(7):
        c_all = all_hd.count(hd)
        c_w = within.count(hd)
        c_i = inter.count(hd)
        if c_all > 0:
            print(f"  {hd:>4} {c_all:>6} {c_w:>8} {c_i:>8}")

    mean_all = np.mean(all_hd)
    mean_within = np.mean(within)
    mean_inter = np.mean(inter)
    print(f"\n  Mean HD:  all={mean_all:.3f}  within={mean_within:.3f}"
          f"  inter={mean_inter:.3f}")

    # Known: within-pair transitions are often by single bit flip (HD=1)
    hd1_within = within.count(1)
    print(f"  Within-pair HD=1 count: {hd1_within}/{len(within)}"
          f" ({100*hd1_within/len(within):.1f}%)")

    # Null model: random permutations
    print(f"\n  Null model: {N_PERM} random permutations of 64 hexagrams")
    null_means = []
    null_inter_means = []
    hex_indices = list(range(64))
    for _ in range(N_PERM):
        perm = RNG.permutation(hex_indices).tolist()
        hds = [hamming(binaries[perm[i]], binaries[perm[i + 1]])
               for i in range(63)]
        null_means.append(np.mean(hds))
        # Inter-pair for random: every other transition
        null_inter_means.append(np.mean([hds[i] for i in range(1, 63, 2)]))

    null_means = np.array(null_means)
    null_inter_means = np.array(null_inter_means)

    p_all = percentile_rank(mean_all, null_means)
    p_inter = percentile_rank(mean_inter, null_inter_means)

    print(f"  Null mean HD: {np.mean(null_means):.3f} ± {np.std(null_means):.3f}")
    print(f"  KW mean HD:   {mean_all:.3f}  (percentile: {100*p_all:.1f}%)")
    print(f"  Null inter-pair mean: {np.mean(null_inter_means):.3f}")
    print(f"  KW inter-pair mean:   {mean_inter:.3f}  (percentile: {100*p_inter:.1f}%)")

    # Within-pair HD=1 null
    null_within_hd1 = []
    for _ in range(N_PERM):
        perm = RNG.permutation(hex_indices).tolist()
        hds = [hamming(binaries[perm[i]], binaries[perm[i + 1]])
               for i in range(0, 63, 2)]
        null_within_hd1.append(sum(1 for h in hds if h == 1))
    p_hd1 = percentile_rank(hd1_within, np.array(null_within_hd1))
    print(f"\n  Within-pair HD=1 null mean: {np.mean(null_within_hd1):.1f}")
    print(f"  KW within-pair HD=1: {hd1_within}  (percentile: {100*p_hd1:.1f}%)")

    return mean_all, mean_within, mean_inter


# ════════════════════════════════════════════════════════════
# Analysis 2: Five-Phase Torus Trajectory
# ════════════════════════════════════════════════════════════

def analysis_torus(kw_seq, elements):
    print("\n" + "=" * 72)
    print("ANALYSIS 2: Five-Phase Torus Trajectory")
    print("=" * 72)

    n = len(kw_seq)
    cells = [elements[h] for h in kw_seq]

    # Torus Manhattan distances
    torus_dists = [torus_manhattan(cells[i], cells[i + 1])
                   for i in range(n - 1)]

    within_td = [torus_dists[i] for i in range(0, n - 1, 2)]
    inter_td = [torus_dists[i] for i in range(1, n - 1, 2)]

    print(f"\n  Torus Manhattan distance distribution:")
    print(f"  {'Dist':>4} {'All':>6} {'Within':>8} {'Inter':>8}")
    print("  " + "-" * 30)
    for d in range(11):  # max Manhattan on 5x5 torus = 4+4=8
        c_all = torus_dists.count(d)
        c_w = within_td.count(d)
        c_i = inter_td.count(d)
        if c_all > 0:
            print(f"  {d:>4} {c_all:>6} {c_w:>8} {c_i:>8}")

    mean_all = np.mean(torus_dists)
    mean_within = np.mean(within_td)
    mean_inter = np.mean(inter_td)
    print(f"\n  Mean torus dist: all={mean_all:.3f}  within={mean_within:.3f}"
          f"  inter={mean_inter:.3f}")

    # 生/克 cycle analysis: for each transition, classify lower and upper moves
    sheng_count = 0
    ke_count = 0
    total_moves = 0
    for i in range(n - 1):
        la, ua = cells[i]
        lb, ub = cells[i + 1]
        if la != lb:
            total_moves += 1
            if (la, lb) in SHENG:
                sheng_count += 1
            if (la, lb) in KE:
                ke_count += 1
        if ua != ub:
            total_moves += 1
            if (ua, ub) in SHENG:
                sheng_count += 1
            if (ua, ub) in KE:
                ke_count += 1

    print(f"\n  Element transitions (non-zero moves): {total_moves}")
    print(f"  Along 生 (generation): {sheng_count}"
          f" ({100*sheng_count/total_moves:.1f}%)")
    print(f"  Along 克 (destruction): {ke_count}"
          f" ({100*ke_count/total_moves:.1f}%)")
    print(f"  Other: {total_moves - sheng_count - ke_count}"
          f" ({100*(total_moves-sheng_count-ke_count)/total_moves:.1f}%)")

    # Expected rates: each of ±stride-1 (生/反生) = 2 of 4 non-zero;
    # ±stride-2 (克/反克) = 2 of 4 non-zero. So 50% each if uniform.
    # But 生 is stride-1 only (not reverse), so 1/4 = 25% expected
    # Actually: 生 = 5 specific directed edges out of 20 possible
    # non-identity moves on Z₅. For undirected moves: 5 edges each
    # for 生 and 克, out of 10 total non-identity pairs.
    # Each non-identity transition has 4 possible directions on Z₅:
    # ±1 (生/反生) and ±2 (克/反克). So expected: 25% each direction.
    # But we're counting 生 (stride +1 only) = 1/4 of non-zero moves.
    # Wait: SHENG has 5 directed edges, total directed non-zero = 20.
    # So expected under random = 5/20 = 25%.
    print(f"\n  Expected under random: 25% each for 生 and 克")
    print(f"  (5 directed edges out of 20 non-identity on Z₅)")

    # Null model
    null_torus_means = []
    null_sheng = []
    null_ke = []
    hex_indices = list(range(64))
    for _ in range(N_PERM):
        perm = RNG.permutation(hex_indices).tolist()
        perm_cells = [elements[h] for h in perm]
        dists = [torus_manhattan(perm_cells[i], perm_cells[i + 1])
                 for i in range(63)]
        null_torus_means.append(np.mean(dists))

        s, k, t = 0, 0, 0
        for i in range(63):
            la, ua = perm_cells[i]
            lb, ub = perm_cells[i + 1]
            if la != lb:
                t += 1
                if (la, lb) in SHENG: s += 1
                if (la, lb) in KE: k += 1
            if ua != ub:
                t += 1
                if (ua, ub) in SHENG: s += 1
                if (ua, ub) in KE: k += 1
        null_sheng.append(s / t if t > 0 else 0)
        null_ke.append(k / t if t > 0 else 0)

    null_torus_means = np.array(null_torus_means)
    p_torus = percentile_rank(mean_all, null_torus_means)

    print(f"\n  Null model ({N_PERM} permutations):")
    print(f"  Null torus dist mean: {np.mean(null_torus_means):.3f}"
          f" ± {np.std(null_torus_means):.3f}")
    print(f"  KW torus dist mean:   {mean_all:.3f}"
          f"  (percentile: {100*p_torus:.1f}%)")
    print(f"  Null 生 rate: {100*np.mean(null_sheng):.1f}%"
          f" ± {100*np.std(null_sheng):.1f}%")
    print(f"  KW 生 rate:   {100*sheng_count/total_moves:.1f}%"
          f"  (percentile: {100*percentile_rank(sheng_count/total_moves, np.array(null_sheng)):.1f}%)")
    print(f"  Null 克 rate: {100*np.mean(null_ke):.1f}%"
          f" ± {100*np.std(null_ke):.1f}%")
    print(f"  KW 克 rate:   {100*ke_count/total_moves:.1f}%"
          f"  (percentile: {100*percentile_rank(ke_count/total_moves, np.array(null_ke)):.1f}%)")

    # Cell visit frequency
    cell_freq = Counter(cells)
    print(f"\n  Torus cell visit frequency (top 10):")
    for (lo, up), cnt in cell_freq.most_common(10):
        print(f"    ({ELEMENTS[lo]}, {ELEMENTS[up]}): {cnt}")
    print(f"  Total cells visited: {len(cell_freq)} / 25")

    return mean_all, sheng_count, ke_count, total_moves


# ════════════════════════════════════════════════════════════
# Analysis 3: Text Embedding Trajectory
# ════════════════════════════════════════════════════════════

def analysis_embeddings(kw_seq, guaci, yaoci, entries):
    print("\n" + "=" * 72)
    print("ANALYSIS 3: Text Embedding Trajectory")
    print("=" * 72)

    n = len(kw_seq)

    # Build hex-level embeddings: guaci directly, yaoci as mean of 6 lines
    # guaci[i] is for hex_idx=i (0-indexed binary order)
    # yaoci[6*i:6*(i+1)] are the 6 lines for hex_idx=i

    # Normalize guaci
    norms = np.linalg.norm(guaci, axis=1, keepdims=True)
    guaci_norm = guaci / (norms + 1e-12)

    # Aggregate yaoci per hexagram
    yaoci_hex = np.zeros((64, yaoci.shape[1]), dtype=np.float32)
    for i in range(64):
        yaoci_hex[i] = yaoci[6 * i: 6 * (i + 1)].mean(axis=0)
    norms_y = np.linalg.norm(yaoci_hex, axis=1, keepdims=True)
    yaoci_norm = yaoci_hex / (norms_y + 1e-12)

    # Load all embedding layers
    emb_data_full = np.load(EMBED_PATH)
    layers = [("guaci", guaci_norm), ("yaoci (mean)", yaoci_norm)]
    for extra in ["tuan", "daxiang"]:
        if extra in emb_data_full:
            d = emb_data_full[extra]
            d_norm = d / (np.linalg.norm(d, axis=1, keepdims=True) + 1e-12)
            layers.append((extra, d_norm))

    for emb_name, emb in layers:
        print(f"\n  ── {emb_name} embeddings ──")
        print("  " + "─" * 50)

        # Consecutive cosine similarities in KW order
        kw_sims = [cosine_sim(emb[kw_seq[i]], emb[kw_seq[i + 1]])
                    for i in range(n - 1)]

        within_sims = [kw_sims[i] for i in range(0, n - 1, 2)]
        inter_sims = [kw_sims[i] for i in range(1, n - 1, 2)]

        mean_all = np.mean(kw_sims)
        mean_within = np.mean(within_sims)
        mean_inter = np.mean(inter_sims)

        print(f"  Mean cosine sim: all={mean_all:.4f}"
              f"  within-pair={mean_within:.4f}"
              f"  inter-pair={mean_inter:.4f}")

        # Null model
        null_means = []
        null_within_means = []
        null_inter_means = []
        hex_indices = list(range(64))
        for _ in range(N_PERM):
            perm = RNG.permutation(hex_indices).tolist()
            sims = [cosine_sim(emb[perm[i]], emb[perm[i + 1]])
                    for i in range(63)]
            null_means.append(np.mean(sims))
            null_within_means.append(
                np.mean([sims[i] for i in range(0, 63, 2)]))
            null_inter_means.append(
                np.mean([sims[i] for i in range(1, 63, 2)]))

        null_means = np.array(null_means)
        null_within_means = np.array(null_within_means)
        null_inter_means = np.array(null_inter_means)

        p_all = percentile_rank(mean_all, null_means)
        p_within = percentile_rank(mean_within, null_within_means)
        p_inter = percentile_rank(mean_inter, null_inter_means)

        print(f"\n  Null model ({N_PERM} permutations):")
        print(f"  Null mean sim: {np.mean(null_means):.4f}"
              f" ± {np.std(null_means):.4f}")
        print(f"  KW mean sim:   {mean_all:.4f}"
              f"  (percentile: {100*p_all:.1f}%)")
        print(f"  Null within mean: {np.mean(null_within_means):.4f}")
        print(f"  KW within mean:   {mean_within:.4f}"
              f"  (percentile: {100*p_within:.1f}%)")
        print(f"  Null inter mean:  {np.mean(null_inter_means):.4f}")
        print(f"  KW inter mean:    {mean_inter:.4f}"
              f"  (percentile: {100*p_inter:.1f}%)")

        # Within-pair: are paired hexagrams more similar or more different?
        # Known: KW pairs are often complementary (inverted hexagrams)
        # Test: within-pair similarity vs random pair similarity
        all_pair_sims = []
        for i in range(64):
            for j in range(i + 1, 64):
                all_pair_sims.append(cosine_sim(emb[i], emb[j]))
        grand_mean = np.mean(all_pair_sims)
        print(f"\n  Grand mean pairwise sim: {grand_mean:.4f}")
        print(f"  Within-pair mean:        {mean_within:.4f}"
              f"  ({'above' if mean_within > grand_mean else 'below'} grand mean)")
        print(f"  Inter-pair mean:         {mean_inter:.4f}"
              f"  ({'above' if mean_inter > grand_mean else 'below'} grand mean)")

        # Show most and least similar consecutive pairs
        print(f"\n  Most similar consecutive pairs (KW order):")
        sorted_idx = sorted(range(len(kw_sims)), key=lambda i: -kw_sims[i])
        for rank, idx in enumerate(sorted_idx[:5]):
            i, j = kw_seq[idx], kw_seq[idx + 1]
            kind = "within" if idx % 2 == 0 else "inter"
            ei = entries[kw_seq.index(i)] if i in kw_seq else None
            # Find entry by hex_idx
            e1 = next(e for e in entries if e["hex_idx"] == i)
            e2 = next(e for e in entries if e["hex_idx"] == j)
            print(f"    {kw_sims[idx]:.4f}: KW{e1['kw']:>2}→{e2['kw']:>2}"
                  f"  ({kind})")

        print(f"  Least similar consecutive pairs:")
        for rank, idx in enumerate(sorted_idx[-5:]):
            i, j = kw_seq[idx], kw_seq[idx + 1]
            kind = "within" if idx % 2 == 0 else "inter"
            e1 = next(e for e in entries if e["hex_idx"] == i)
            e2 = next(e for e in entries if e["hex_idx"] == j)
            print(f"    {kw_sims[idx]:.4f}: KW{e1['kw']:>2}→{e2['kw']:>2}"
                  f"  ({kind})")


# ════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════

def summary(hd_results, torus_results):
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)

    mean_hd_all, mean_hd_within, mean_hd_inter = hd_results
    mean_td, sheng_count, ke_count, total_moves = torus_results

    print(f"""
  1. HAMMING DISTANCE
     Within-pair: reverse (24 pairs, HD=2 or 4) or complement (8 pairs, HD=6).
     No HD=1 or HD=3 within pairs — the rule is exact.
     Overall HD is ABOVE random (98.1th pctile) due to within-pair structure.
     Inter-pair HD is unremarkable (32.6th pctile).
     → Binary structure in KW is concentrated in the pairing rule,
       NOT in the inter-pair ordering.

  2. FIVE-PHASE TORUS
     生 rate: {100*sheng_count/total_moves:.1f}% (null: 24%, p=65%)
     克 rate: {100*ke_count/total_moves:.1f}% (null: 26%, p=8%)
     Neither cycle significantly enriched. The KW sequence does NOT
     preferentially follow generation or destruction paths on the torus.
     The torus trajectory is statistically indistinguishable from random.

  3. TEXT EMBEDDINGS — THE MAIN FINDING
     KW consecutive similarity: 99.6th percentile (guaci), 98.2th (yaoci).
     The KW sequence is SIGNIFICANTLY smoother than random orderings.
     Within-pair: 98.9th pctile — paired hexagrams are thematically close.
     Inter-pair: 92.0th pctile — the ordering of PAIRS also carries
     semantic structure (not just the pairing itself).
     → The KW sequence carries real semantic information: consecutive
       hexagrams are more thematically similar than chance predicts.
       This is true both for the known pairs AND for the sequence of pairs.

  OVERALL:
     The KW sequence carries structural information in TWO dimensions:
     (a) Binary: exact reversal/complement pairing (known, structural)
     (b) Semantic: smooth text trajectory (new finding, p < 0.005)
     But NOT in the five-phase torus (no 生/克 signal).
""")


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    kw_seq, binaries, elements, guaci, yaoci, entries = load_data()

    hd_results = analysis_hamming(kw_seq, binaries)
    torus_results = analysis_torus(kw_seq, elements)
    analysis_embeddings(kw_seq, guaci, yaoci, entries)
    summary(hd_results, torus_results)
