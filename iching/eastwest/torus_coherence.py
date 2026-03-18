#!/usr/bin/env python3
"""torus_coherence.py — Does the five-phase torus cell carry semantic information?

Four analyses:
1. Within-cell vs between-cell similarity
2. Which five-phase relation predicts similarity?
3. Torus distance vs semantic distance (correlation)
4. Variance decomposition: how much does the torus explain?
"""

import json
import numpy as np
from collections import Counter, defaultdict
from pathlib import Path
from itertools import combinations

# ════════════════════════════════════════════════════════════
# Constants
# ════════════════════════════════════════════════════════════

ATLAS_PATH = Path(__file__).parent.parent / "atlas" / "atlas.json"
EMBED_PATH = Path(__file__).parent.parent / "synthesis" / "embeddings.npz"

# 生-cycle ordering: Wood→Fire→Earth→Metal→Water
ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}

# Relation labels from atlas
REL_NAMES = {
    "比和": "same",
    "体生用": "lo→up (生)",
    "生体": "up→lo (被生)",
    "体克用": "lo→up (克)",
    "克体": "up→lo (被克)",
}

N_PERM = 10_000
RNG = np.random.default_rng(42)

# ════════════════════════════════════════════════════════════
# Data Loading
# ════════════════════════════════════════════════════════════

def load_data():
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)

    hex_data = {}
    for k, v in atlas.items():
        idx = int(k)
        hex_data[idx] = {
            "lower": ELEM_IDX[v["lower_trigram"]["element"]],
            "upper": ELEM_IDX[v["upper_trigram"]["element"]],
            "relation": v["surface_relation"],
            "cell": (ELEM_IDX[v["lower_trigram"]["element"]],
                     ELEM_IDX[v["upper_trigram"]["element"]]),
        }

    emb_data = np.load(EMBED_PATH)
    layers = {}
    for name in ["guaci", "tuan"]:
        d = emb_data[name]
        norms = np.linalg.norm(d, axis=1, keepdims=True)
        layers[name] = d / (norms + 1e-12)

    return hex_data, layers


# ════════════════════════════════════════════════════════════
# Utilities
# ════════════════════════════════════════════════════════════

def cosine_sim(a, b):
    return float(np.dot(a, b))  # already normalized


def torus_manhattan(cell_a, cell_b):
    dl = min(abs(cell_a[0] - cell_b[0]), 5 - abs(cell_a[0] - cell_b[0]))
    du = min(abs(cell_a[1] - cell_b[1]), 5 - abs(cell_a[1] - cell_b[1]))
    return dl + du


def all_pair_sims(emb):
    """Precompute all 2016 pairwise cosine similarities."""
    sims = {}
    for i in range(64):
        for j in range(i + 1, 64):
            sims[(i, j)] = cosine_sim(emb[i], emb[j])
    return sims


def pair_relation(hex_data, i, j):
    """Relation between the surface cells of hex i and hex j.
    This is the relation of i's cell, not the cross-hex relation."""
    return hex_data[i]["relation"], hex_data[j]["relation"]


# ════════════════════════════════════════════════════════════
# Analysis 1: Within-cell vs between-cell similarity
# ════════════════════════════════════════════════════════════

def analysis_1(hex_data, layers):
    print("=" * 72)
    print("ANALYSIS 1: Within-cell vs between-cell similarity")
    print("=" * 72)

    # Group hexagrams by cell
    cell_members = defaultdict(list)
    for idx, hd in hex_data.items():
        cell_members[hd["cell"]].append(idx)

    cell_sizes = {c: len(m) for c, m in cell_members.items()}
    print(f"\n  25 cells: {sum(1 for s in cell_sizes.values() if s >= 2)} with ≥2 hexagrams")
    print(f"  Size distribution: {Counter(cell_sizes.values())}")

    for layer_name, emb in layers.items():
        print(f"\n  ── {layer_name} ──")
        print("  " + "─" * 50)

        sims = all_pair_sims(emb)

        # Within-cell similarities
        within_sims = []
        for cell, members in cell_members.items():
            if len(members) < 2:
                continue
            for i, j in combinations(members, 2):
                a, b = min(i, j), max(i, j)
                within_sims.append(sims[(a, b)])

        # Between-cell similarities
        between_sims = []
        for (i, j), s in sims.items():
            if hex_data[i]["cell"] != hex_data[j]["cell"]:
                between_sims.append(s)

        mean_within = np.mean(within_sims)
        mean_between = np.mean(between_sims)
        delta = mean_within - mean_between

        print(f"  Within-cell:  mean = {mean_within:.4f}  (n = {len(within_sims)})")
        print(f"  Between-cell: mean = {mean_between:.4f}  (n = {len(between_sims)})")
        print(f"  Δ (within − between) = {delta:.4f}")

        # Null model: permute cell labels
        null_deltas = []
        hex_indices = list(range(64))
        for _ in range(N_PERM):
            perm = RNG.permutation(hex_indices)
            # Permuted cell assignment
            perm_cells = {idx: hex_data[perm[idx]]["cell"] for idx in range(64)}
            w, b = [], []
            for (i, j), s in sims.items():
                if perm_cells[i] == perm_cells[j]:
                    w.append(s)
                else:
                    b.append(s)
            if w:
                null_deltas.append(np.mean(w) - np.mean(b))
            else:
                null_deltas.append(0)

        null_deltas = np.array(null_deltas)
        pctile = np.mean(null_deltas <= delta)

        print(f"\n  Null Δ: {np.mean(null_deltas):.4f} ± {np.std(null_deltas):.4f}")
        print(f"  True Δ: {delta:.4f}  (percentile: {100 * pctile:.1f}%)")

        # Per-cell breakdown
        print(f"\n  Per-cell mean similarity (cells with ≥2 hexagrams):")
        print(f"  {'Cell':<20} {'Size':>4} {'Mean sim':>10}")
        print("  " + "-" * 38)
        cell_means = []
        for cell in sorted(cell_members.keys()):
            members = cell_members[cell]
            if len(members) < 2:
                continue
            csims = [sims[(min(i, j), max(i, j))]
                     for i, j in combinations(members, 2)]
            m = np.mean(csims)
            cell_means.append((cell, len(members), m))
        cell_means.sort(key=lambda x: -x[2])
        for cell, sz, m in cell_means:
            lo, up = cell
            print(f"  ({ELEMENTS[lo]:>5},{ELEMENTS[up]:>5})  {sz:>4}  {m:>10.4f}")


# ════════════════════════════════════════════════════════════
# Analysis 2: Which five-phase relation predicts similarity?
# ════════════════════════════════════════════════════════════

def analysis_2(hex_data, layers):
    print("\n" + "=" * 72)
    print("ANALYSIS 2: Five-phase relation vs similarity")
    print("=" * 72)

    # Classify each hexagram PAIR by the relation between their cells
    # For two hexagrams with cells (l1,u1) and (l2,u2), there's no
    # single "relation" — that concept is per-hexagram (lower vs upper).
    # Instead, group by: do the two hexagrams share the same relation type?

    # Actually, the more useful analysis: group hexagrams by their OWN
    # surface relation, then check within-group similarity.
    rel_members = defaultdict(list)
    for idx, hd in hex_data.items():
        rel_members[hd["relation"]].append(idx)

    for layer_name, emb in layers.items():
        print(f"\n  ── {layer_name} ──")
        print("  " + "─" * 50)

        sims = all_pair_sims(emb)
        grand_mean = np.mean(list(sims.values()))

        print(f"  Grand mean pairwise sim: {grand_mean:.4f}")
        print(f"\n  {'Relation':<12} {'Name':<14} {'n':>3} {'Within mean':>12}"
              f" {'vs grand':>10}")
        print("  " + "-" * 55)

        rel_results = {}
        for rel in ["比和", "体生用", "生体", "体克用", "克体"]:
            members = rel_members[rel]
            n = len(members)
            if n < 2:
                continue
            within = [sims[(min(i, j), max(i, j))]
                      for i, j in combinations(members, 2)]
            m = np.mean(within)
            delta = m - grand_mean
            rel_results[rel] = (m, delta, n)
            sign = "+" if delta > 0 else ""
            print(f"  {rel:<12} {REL_NAMES[rel]:<14} {n:>3}"
                  f" {m:>12.4f} {sign}{delta:>9.4f}")

        # Cross-relation: mean similarity between hexagrams of different relations
        print(f"\n  Cross-relation mean similarities:")
        rels = ["比和", "体生用", "生体", "体克用", "克体"]
        print(f"  {'':>12}", end="")
        for r2 in rels:
            print(f" {r2:>8}", end="")
        print()
        for r1 in rels:
            print(f"  {r1:<12}", end="")
            for r2 in rels:
                m1 = rel_members[r1]
                m2 = rel_members[r2]
                if r1 == r2:
                    cross = [sims[(min(i, j), max(i, j))]
                             for i, j in combinations(m1, 2)]
                else:
                    cross = [sims[(min(i, j), max(i, j))]
                             for i in m1 for j in m2 if i != j]
                print(f" {np.mean(cross):>8.4f}", end="")
            print()

        # Null model: permute relation labels
        null_bihe_means = []
        for _ in range(N_PERM):
            perm = RNG.permutation(64)
            perm_rel = {idx: hex_data[perm[idx]]["relation"] for idx in range(64)}
            bihe_members = [idx for idx in range(64) if perm_rel[idx] == "比和"]
            if len(bihe_members) >= 2:
                w = [sims[(min(i, j), max(i, j))]
                     for i, j in combinations(bihe_members, 2)]
                null_bihe_means.append(np.mean(w))

        null_bihe_means = np.array(null_bihe_means)
        bihe_mean = rel_results["比和"][0]
        pctile = np.mean(null_bihe_means <= bihe_mean)
        print(f"\n  比和 (same) null mean: {np.mean(null_bihe_means):.4f}"
              f" ± {np.std(null_bihe_means):.4f}")
        print(f"  比和 true mean: {bihe_mean:.4f}"
              f"  (percentile: {100 * pctile:.1f}%)")


# ════════════════════════════════════════════════════════════
# Analysis 3: Torus distance vs semantic distance
# ════════════════════════════════════════════════════════════

def analysis_3(hex_data, layers):
    print("\n" + "=" * 72)
    print("ANALYSIS 3: Torus distance vs semantic similarity")
    print("=" * 72)

    # Compute torus distances for all pairs
    torus_dists = {}
    for i in range(64):
        for j in range(i + 1, 64):
            torus_dists[(i, j)] = torus_manhattan(
                hex_data[i]["cell"], hex_data[j]["cell"])

    # Distribution of torus distances
    dist_counts = Counter(torus_dists.values())
    print(f"\n  Torus Manhattan distance distribution (2016 pairs):")
    for d in sorted(dist_counts):
        print(f"    d={d}: {dist_counts[d]} pairs")

    for layer_name, emb in layers.items():
        print(f"\n  ── {layer_name} ──")
        print("  " + "─" * 50)

        sims = all_pair_sims(emb)

        # Mean similarity at each torus distance
        dist_sims = defaultdict(list)
        for (i, j), d in torus_dists.items():
            dist_sims[d].append(sims[(i, j)])

        print(f"\n  {'Torus d':>8} {'n pairs':>8} {'Mean sim':>10} {'Std':>8}")
        print("  " + "-" * 38)
        for d in sorted(dist_sims):
            vals = dist_sims[d]
            print(f"  {d:>8} {len(vals):>8} {np.mean(vals):>10.4f}"
                  f" {np.std(vals):>8.4f}")

        # Spearman correlation: torus distance vs cosine similarity
        all_d = []
        all_s = []
        for (i, j) in sims:
            all_d.append(torus_dists[(i, j)])
            all_s.append(sims[(i, j)])
        all_d = np.array(all_d)
        all_s = np.array(all_s)

        # Spearman ρ (rank correlation)
        from scipy.stats import spearmanr
        rho, p_val = spearmanr(all_d, all_s)
        print(f"\n  Spearman ρ(torus_dist, cosine_sim) = {rho:.4f}"
              f"  (p = {p_val:.2e})")

        # Compare with Hamming distance correlation
        all_hd = np.array([bin(i ^ j).count("1") for i, j in sims])
        rho_hd, p_hd = spearmanr(all_hd, all_s)
        print(f"  Spearman ρ(hamming_dist, cosine_sim) = {rho_hd:.4f}"
              f"  (p = {p_hd:.2e})")

        # Null model for torus correlation
        null_rhos = []
        hex_indices = list(range(64))
        for _ in range(N_PERM):
            perm = RNG.permutation(hex_indices)
            perm_cells = {idx: hex_data[perm[idx]]["cell"] for idx in range(64)}
            perm_dists = [torus_manhattan(perm_cells[i], perm_cells[j])
                          for i, j in sims]
            r, _ = spearmanr(perm_dists, all_s)
            null_rhos.append(r)

        null_rhos = np.array(null_rhos)
        # For negative correlation, check what fraction is MORE negative
        pctile = np.mean(null_rhos <= rho)
        print(f"\n  Null ρ: {np.mean(null_rhos):.4f} ± {np.std(null_rhos):.4f}")
        print(f"  True ρ: {rho:.4f}  (percentile: {100 * pctile:.1f}%)")


# ════════════════════════════════════════════════════════════
# Analysis 4: Variance decomposition
# ════════════════════════════════════════════════════════════

def analysis_4(hex_data, layers):
    print("\n" + "=" * 72)
    print("ANALYSIS 4: Variance decomposition — what does the torus explain?")
    print("=" * 72)

    # Group hexagrams by cell
    cell_members = defaultdict(list)
    for idx, hd in hex_data.items():
        cell_members[hd["cell"]].append(idx)

    # Group by complement pair
    comp_members = defaultdict(list)
    for idx in range(64):
        comp = idx ^ 63
        pair_key = (min(idx, comp), max(idx, comp))
        comp_members[pair_key].append(idx)

    for layer_name, emb in layers.items():
        print(f"\n  ── {layer_name} ──")
        print("  " + "─" * 50)

        sims = all_pair_sims(emb)
        all_sims_arr = np.array(list(sims.values()))
        grand_mean = np.mean(all_sims_arr)
        ss_total = np.sum((all_sims_arr - grand_mean) ** 2)

        # R² for torus cell partition
        # SS_between = Σ_groups n_g * (mean_g - grand_mean)²
        # But here "groups" are pairs grouped by (cell_i, cell_j)
        # Easier: group pairs by whether same-cell or not, then by cell pair
        cell_pair_groups = defaultdict(list)
        for (i, j), s in sims.items():
            ci = hex_data[i]["cell"]
            cj = hex_data[j]["cell"]
            key = (min(ci, cj), max(ci, cj))
            cell_pair_groups[key].append(s)

        ss_between_cell = 0
        for key, group_sims in cell_pair_groups.items():
            group_mean = np.mean(group_sims)
            ss_between_cell += len(group_sims) * (group_mean - grand_mean) ** 2
        r2_cell = ss_between_cell / ss_total

        # R² for torus distance (as categorical: d=0,1,2,3,4,5)
        dist_groups = defaultdict(list)
        for (i, j), s in sims.items():
            d = torus_manhattan(hex_data[i]["cell"], hex_data[j]["cell"])
            dist_groups[d].append(s)

        ss_between_dist = 0
        for d, group_sims in dist_groups.items():
            group_mean = np.mean(group_sims)
            ss_between_dist += len(group_sims) * (group_mean - grand_mean) ** 2
        r2_dist = ss_between_dist / ss_total

        # R² for Hamming distance (as categorical: d=1,...,6)
        hd_groups = defaultdict(list)
        for (i, j), s in sims.items():
            d = bin(i ^ j).count("1")
            hd_groups[d].append(s)

        ss_between_hd = 0
        for d, group_sims in hd_groups.items():
            group_mean = np.mean(group_sims)
            ss_between_hd += len(group_sims) * (group_mean - grand_mean) ** 2
        r2_hd = ss_between_hd / ss_total

        # R² for complement pair membership (same pair or not)
        comp_groups = defaultdict(list)
        for (i, j), s in sims.items():
            same_pair = (j == i ^ 63)
            comp_groups[same_pair].append(s)

        ss_between_comp = 0
        for key, group_sims in comp_groups.items():
            group_mean = np.mean(group_sims)
            ss_between_comp += len(group_sims) * (group_mean - grand_mean) ** 2
        r2_comp = ss_between_comp / ss_total

        # R² for surface relation
        rel_groups = defaultdict(list)
        for (i, j), s in sims.items():
            # Use the relation of hex i (it's a per-hex property)
            # Actually, for pair-level analysis, combine both
            ri = hex_data[i]["relation"]
            rj = hex_data[j]["relation"]
            key = (min(ri, rj), max(ri, rj))
            rel_groups[key].append(s)

        ss_between_rel = 0
        for key, group_sims in rel_groups.items():
            group_mean = np.mean(group_sims)
            ss_between_rel += len(group_sims) * (group_mean - grand_mean) ** 2
        r2_rel = ss_between_rel / ss_total

        print(f"\n  R² decomposition (fraction of similarity variance explained):")
        print(f"  {'Predictor':<30} {'R²':>8} {'# groups':>10}")
        print("  " + "-" * 52)
        print(f"  {'Torus cell pair (lo×up, lo×up)':<30} {r2_cell:>8.4f}"
              f" {len(cell_pair_groups):>10}")
        print(f"  {'Torus Manhattan distance':<30} {r2_dist:>8.4f}"
              f" {len(dist_groups):>10}")
        print(f"  {'Hamming distance':<30} {r2_hd:>8.4f}"
              f" {len(hd_groups):>10}")
        print(f"  {'Complement pair membership':<30} {r2_comp:>8.4f}"
              f" {len(comp_groups):>10}")
        print(f"  {'Surface relation pair':<30} {r2_rel:>8.4f}"
              f" {len(rel_groups):>10}")

        # Null model: R² for random partitions with same cell sizes
        cell_size_list = sorted(cell_members.values(), key=len)
        null_r2s = []
        for _ in range(N_PERM):
            perm = RNG.permutation(64)
            perm_cells = {}
            idx = 0
            for cell, members in cell_members.items():
                for m in members:
                    perm_cells[perm[idx]] = cell
                    idx += 1

            perm_cell_pair_groups = defaultdict(list)
            for (i, j), s in sims.items():
                ci = perm_cells[i]
                cj = perm_cells[j]
                key = (min(ci, cj), max(ci, cj))
                perm_cell_pair_groups[key].append(s)

            ss_b = sum(len(gs) * (np.mean(gs) - grand_mean) ** 2
                       for gs in perm_cell_pair_groups.values())
            null_r2s.append(ss_b / ss_total)

        null_r2s = np.array(null_r2s)
        pctile = np.mean(null_r2s <= r2_cell)

        print(f"\n  Null R² (random partition, same sizes):"
              f" {np.mean(null_r2s):.4f} ± {np.std(null_r2s):.4f}")
        print(f"  True R² (torus cell pair): {r2_cell:.4f}"
              f"  (percentile: {100 * pctile:.1f}%)")


# ════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════

def print_summary():
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print("""
  1. WITHIN-CELL VS BETWEEN-CELL
     guaci: within-cell LOWER than between (3.5th pctile) — anti-signal.
     tuan:  no difference (54th pctile).
     Hexagrams sharing a torus cell are NOT more semantically similar.

  2. FIVE-PHASE RELATIONS
     体生用 (lo generates up) has highest similarity in guaci (+0.030).
     But 比和 (same element) shows no significant effect (80th, 52nd pctile).
     No relation type robustly predicts semantic similarity.

  3. TORUS DISTANCE VS SIMILARITY
     guaci: ρ = 0.007, no correlation.
     tuan:  ρ = -0.061, p = 0.006, 0.1st pctile — WEAK negative correlation.
     Close torus cells are slightly more similar in tuan, but effect is tiny.
     Compare: Hamming ρ = -0.073 in tuan — slightly stronger than torus.

  4. VARIANCE DECOMPOSITION
     guaci: torus cell pair R² = 0.257 (null: 0.249) — NO signal (58th pctile).
     tuan:  torus cell pair R² = 0.375 (null: 0.270) — SIGNAL (99th pctile).
     The torus cell explains ~10% more variance than random grouping in tuan.
     But: 321 cell-pair groups for 2016 observations — fine-grained.
     Torus Manhattan distance R² ≈ 0.005 — negligible.
     Hamming distance R² ≈ 0.007 — similarly negligible.

  OVERALL:
     The five-phase torus carries WEAK semantic information, detectable
     only in the tuan (judgment) layer. The effect is real (p ≈ 0.01)
     but small (ρ ≈ -0.06, R² uplift ≈ 0.10).

     Compared to:
     - KW sequence smoothness: p < 0.0001 (much stronger)
     - Binary Hamming: comparable weak effect (ρ ≈ -0.07)
     - Complement pairing: negligible

     The torus cell is a mid-resolution predictor: it captures some of
     the thematic organization via the five-phase element assignment to
     trigrams, but the signal is weak and inconsistent across text layers.
     The five-phase relation labels (生/克/比和) do NOT robustly predict
     semantic similarity between hexagrams.
""")


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    hex_data, layers = load_data()
    analysis_1(hex_data, layers)
    analysis_2(hex_data, layers)
    analysis_3(hex_data, layers)
    analysis_4(hex_data, layers)
    print_summary()
