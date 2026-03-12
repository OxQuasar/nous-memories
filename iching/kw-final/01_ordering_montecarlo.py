#!/usr/bin/env python3
"""
KW Sequence Ordering — Monte Carlo Comparison

What makes the King Wen pair ordering special among orderings
that satisfy the same hard constraints?

Hard constraints:
  1. Fixed endpoints: pair 0 = Qian/Kun (63,0), pair 31 = JiJi/WeiJi (42,21)
  2. Z₅×Z₅ anti-clustering: no two consecutive hexagrams share the same
     (lower_element, upper_element) pair

Metrics computed on 50,000 valid random orderings and compared to KW.
"""

import sys
import random
import json
from pathlib import Path
from collections import Counter

import numpy as np

# ─── Infrastructure imports ──────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(ROOT / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ROOT / "kingwen"))

from cycle_algebra import (
    lower_trigram, upper_trigram, TRIGRAM_ELEMENT,
    reverse6, hamming6, kw_partner, is_palindrome6,
    MASK_ALL, bit,
)
from sequence import KING_WEN

# ─── Constants ───────────────────────────────────────────────────────────────

NUM_PAIRS = 32
NUM_HEX = 64
N_MONTE_CARLO = 50_000
SEED = 42

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}

# ─── Hexagram utilities ──────────────────────────────────────────────────────

def kw_to_val(idx):
    """Convert KW sequence index (0-based) to integer hex value."""
    return int(KING_WEN[idx][2][::-1], 2)

def elem_pair(h):
    """(lower_element, upper_element) for hexagram integer h."""
    return (TRIGRAM_ELEMENT[lower_trigram(h)], TRIGRAM_ELEMENT[upper_trigram(h)])

def elem_pair_idx(h):
    """(lower_element_idx, upper_element_idx) for torus distance."""
    le, ue = elem_pair(h)
    return (ELEM_IDX[le], ELEM_IDX[ue])

def basin(h):
    """Basin from inner bits (lines 3,4 = bits 2,3)."""
    b2, b3 = bit(h, 2), bit(h, 3)
    if (b2, b3) == (0, 0): return "Kun"
    if (b2, b3) == (1, 1): return "Qian"
    return "KanLi"

def orbit_sig(h):
    """(L1⊕L6, L2⊕L5, L3⊕L4) — XOR signature of h with its reversal."""
    return (bit(h, 0) ^ bit(h, 5), bit(h, 1) ^ bit(h, 4), bit(h, 2) ^ bit(h, 3))

def torus_manhattan(h1, h2):
    """Manhattan distance on Z₅×Z₅ torus between element pairs."""
    r1, c1 = elem_pair_idx(h1)
    r2, c2 = elem_pair_idx(h2)
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    return min(dr, 5 - dr) + min(dc, 5 - dc)

# ─── Build KW pairs ─────────────────────────────────────────────────────────

def build_kw_pairs():
    """Extract 32 pairs in KW order with all attributes."""
    kw_vals = [kw_to_val(i) for i in range(NUM_HEX)]

    # Build value→pair_idx map for complement lookup
    val_to_pair = {}
    pairs = []
    for pi in range(NUM_PAIRS):
        h1 = kw_vals[2 * pi]
        h2 = kw_vals[2 * pi + 1]
        pairs.append({
            "pair_idx": pi,
            "h1": h1, "h2": h2,
            "h1_elem_pair": elem_pair(h1),
            "h2_elem_pair": elem_pair(h2),
            "basin": basin(h1),
            "orbit_sig": orbit_sig(h1),
            "kw_num1": KING_WEN[2 * pi][0],
            "kw_num2": KING_WEN[2 * pi + 1][0],
            "name1": KING_WEN[2 * pi][1],
            "name2": KING_WEN[2 * pi + 1][1],
        })
        val_to_pair[h1] = pi
        val_to_pair[h2] = pi

    # Add complement pair indices
    for p in pairs:
        comp_h1 = p["h1"] ^ MASK_ALL
        p["complement_pair_idx"] = val_to_pair[comp_h1]

    return pairs

# ─── Constraint checking ────────────────────────────────────────────────────

def check_anti_clustering(pair_ordering):
    """Check all 63 consecutive transitions for element-pair anti-clustering."""
    for k in range(len(pair_ordering) - 1):
        # Within pair: h1→h2 (always need to check)
        # Between pairs: h2[k]→h1[k+1]
        pass

    # Build full 64-hex sequence
    seq = []
    for p in pair_ordering:
        seq.extend([p["h1"], p["h2"]])

    for i in range(len(seq) - 1):
        if elem_pair(seq[i]) == elem_pair(seq[i + 1]):
            return False
    return True

# ─── Metric suite ───────────────────────────────────────────────────────────

ORBIT_COUNT = 8  # possible orbit signatures

def compute_metrics(pair_ordering):
    """Compute all metrics on a list of 32 pair dicts in sequence order."""
    n = len(pair_ordering)

    # Full hexagram sequence
    seq = []
    for p in pair_ordering:
        seq.extend([p["h1"], p["h2"]])

    # ── Basin metrics ──
    basins_seq = [basin(h) for h in seq]
    pair_basins = [p["basin"] for p in pair_ordering]

    # basin_clustering: fraction of 31 between-pair transitions sharing basin
    basin_same = sum(
        1 for k in range(n - 1)
        if pair_basins[k] == pair_basins[k + 1]
    )
    basin_clustering = basin_same / (n - 1)

    # basin_run_count and mean_length
    runs = 1
    run_len = 1
    run_lengths = []
    for i in range(1, len(basins_seq)):
        if basins_seq[i] == basins_seq[i - 1]:
            run_len += 1
        else:
            run_lengths.append(run_len)
            run_len = 1
            runs += 1
    run_lengths.append(run_len)

    # ── Bridge metrics (between pairs: h2[k] → h1[k+1]) ──
    bridge_hammings = [
        hamming6(pair_ordering[k]["h2"], pair_ordering[k + 1]["h1"])
        for k in range(n - 1)
    ]

    # ── Orbit metrics ──
    orbit_edges = set()
    for k in range(n - 1):
        src = pair_ordering[k]["orbit_sig"]
        dst = pair_ordering[k + 1]["orbit_sig"]
        orbit_edges.add((src, dst))

    # Count one-way edges
    oneway = 0
    connected_pairs = set()
    for src, dst in orbit_edges:
        if src != dst:
            pair_key = (min(src, dst), max(src, dst))
            connected_pairs.add(pair_key)
    for pair_key in connected_pairs:
        fwd = pair_key in orbit_edges or (pair_key[0], pair_key[1]) in orbit_edges
        rev = (pair_key[1], pair_key[0]) in orbit_edges
        if not (fwd and rev):
            oneway += 1

    # More careful one-way calculation
    directed_nonselfloops = {(s, d) for s, d in orbit_edges if s != d}
    undirected_pairs = set()
    for s, d in directed_nonselfloops:
        undirected_pairs.add((min(s, d), max(s, d)))
    oneway_count = 0
    for a, b in undirected_pairs:
        if not ((a, b) in directed_nonselfloops and (b, a) in directed_nonselfloops):
            oneway_count += 1
    oneway_frac = oneway_count / len(undirected_pairs) if undirected_pairs else 0

    # Max possible non-self directed edges for 8 orbits = 8*7 = 56
    orbit_unique_edges = len(directed_nonselfloops) / 56

    # ── Complement distance ──
    # For pairs whose complement is a different pair
    comp_distances = []
    for p in pair_ordering:
        ci = p["complement_pair_idx"]
        if ci != p["pair_idx"]:
            # Find position of this pair and its complement in the ordering
            pos_self = next(i for i, q in enumerate(pair_ordering) if q["pair_idx"] == p["pair_idx"])
            pos_comp = next(i for i, q in enumerate(pair_ordering) if q["pair_idx"] == ci)
            comp_distances.append(abs(pos_self - pos_comp))

    # Each complement orbit is counted twice (from each member), deduplicate by taking unique pairs
    comp_dist_unique = []
    seen_comp = set()
    for p in pair_ordering:
        ci = p["complement_pair_idx"]
        pi = p["pair_idx"]
        if ci != pi:
            key = (min(pi, ci), max(pi, ci))
            if key not in seen_comp:
                seen_comp.add(key)
                pos_self = next(i for i, q in enumerate(pair_ordering) if q["pair_idx"] == pi)
                pos_comp = next(i for i, q in enumerate(pair_ordering) if q["pair_idx"] == ci)
                comp_dist_unique.append(abs(pos_self - pos_comp))

    # ── Split-15 basin balance ──
    first_half_basins = Counter(pair_basins[:15])
    second_half_basins = Counter(pair_basins[15:])
    split15_imbalance = sum(
        abs(first_half_basins.get(b, 0) - second_half_basins.get(b, 0))
        for b in ["Kun", "Qian", "KanLi"]
    )

    # ── Yang lines in first half ──
    yang_first = sum(bin(h).count("1") for h in seq[:30])

    # ── Torus step mean ──
    torus_steps = [torus_manhattan(seq[i], seq[i + 1]) for i in range(63)]

    return {
        "basin_clustering": basin_clustering,
        "bridge_hamming_mean": np.mean(bridge_hammings),
        "bridge_hamming_max": max(bridge_hammings),
        "orbit_unique_edges": orbit_unique_edges,
        "orbit_oneway_frac": oneway_frac,
        "complement_distance_median": float(np.median(comp_dist_unique)) if comp_dist_unique else 0,
        "complement_distance_mean": float(np.mean(comp_dist_unique)) if comp_dist_unique else 0,
        "split15_basin_balance": split15_imbalance,
        "yang_total_first_half": yang_first,
        "basin_run_count": runs,
        "basin_run_mean_length": float(np.mean(run_lengths)),
        "torus_step_mean": float(np.mean(torus_steps)),
    }

# ─── Optimized metrics for Monte Carlo (avoid repeated dict lookups) ────────

def compute_metrics_fast(ordering_indices, pairs_data):
    """Fast metric computation using precomputed arrays.
    ordering_indices: list of pair indices in sequence order.
    pairs_data: precomputed pair data dict.
    """
    n = len(ordering_indices)
    pd = pairs_data

    # Build full sequence using precomputed values
    seq_h1 = [pd["h1"][i] for i in ordering_indices]
    seq_h2 = [pd["h2"][i] for i in ordering_indices]

    # Full 64-hex sequence
    seq = []
    for i in range(n):
        seq.append(seq_h1[i])
        seq.append(seq_h2[i])

    # ── Basin metrics ──
    pair_basins = [pd["basin_id"][i] for i in ordering_indices]
    hex_basins = []
    for i in range(n):
        hex_basins.append(pd["h1_basin_id"][ordering_indices[i]])
        hex_basins.append(pd["h2_basin_id"][ordering_indices[i]])

    basin_same = sum(1 for k in range(n - 1) if pair_basins[k] == pair_basins[k + 1])
    basin_clustering = basin_same / (n - 1)

    # Basin runs
    runs = 1
    run_len = 1
    run_lengths = []
    for i in range(1, len(hex_basins)):
        if hex_basins[i] == hex_basins[i - 1]:
            run_len += 1
        else:
            run_lengths.append(run_len)
            run_len = 1
            runs += 1
    run_lengths.append(run_len)

    # ── Bridge Hamming ──
    bridge_hammings = [
        pd["hamming_cache"][(seq_h2[k], seq_h1[k + 1])]
        for k in range(n - 1)
    ]

    # ── Orbit edges ──
    orbit_sigs = [pd["orbit_sig_id"][i] for i in ordering_indices]
    orbit_edges = set()
    for k in range(n - 1):
        orbit_edges.add((orbit_sigs[k], orbit_sigs[k + 1]))

    directed_nonselfloops = {(s, d) for s, d in orbit_edges if s != d}
    undirected_pairs = set()
    for s, d in directed_nonselfloops:
        undirected_pairs.add((min(s, d), max(s, d)))
    oneway_count = 0
    for a, b in undirected_pairs:
        if not ((a, b) in directed_nonselfloops and (b, a) in directed_nonselfloops):
            oneway_count += 1
    oneway_frac = oneway_count / len(undirected_pairs) if undirected_pairs else 0
    orbit_unique_edges = len(directed_nonselfloops) / 56

    # ── Complement distance ──
    # Build position map
    pos_map = {ordering_indices[i]: i for i in range(n)}
    comp_dist_unique = []
    seen = set()
    for i in range(n):
        pi = ordering_indices[i]
        ci = pd["complement_pair_idx"][pi]
        if ci != pi:
            key = (min(pi, ci), max(pi, ci))
            if key not in seen:
                seen.add(key)
                comp_dist_unique.append(abs(pos_map[pi] - pos_map[ci]))

    # ── Split-15 basin balance ──
    first_half = Counter(pair_basins[:15])
    second_half = Counter(pair_basins[15:])
    split15_imbalance = sum(
        abs(first_half.get(b, 0) - second_half.get(b, 0))
        for b in range(3)  # 0=Kun, 1=Qian, 2=KanLi
    )

    # ── Yang lines in first half (first 30 hexagrams) ──
    yang_first = sum(pd["yang_count"][h] for h in seq[:30])

    # ── Torus step mean ──
    torus_sum = sum(pd["torus_cache"][(seq[i], seq[i + 1])] for i in range(63))

    return {
        "basin_clustering": basin_clustering,
        "bridge_hamming_mean": np.mean(bridge_hammings),
        "bridge_hamming_max": max(bridge_hammings),
        "orbit_unique_edges": orbit_unique_edges,
        "orbit_oneway_frac": oneway_frac,
        "complement_distance_median": float(np.median(comp_dist_unique)) if comp_dist_unique else 0,
        "complement_distance_mean": float(np.mean(comp_dist_unique)) if comp_dist_unique else 0,
        "split15_basin_balance": split15_imbalance,
        "yang_total_first_half": yang_first,
        "basin_run_count": runs,
        "basin_run_mean_length": float(np.mean(run_lengths)),
        "torus_step_mean": torus_sum / 63,
    }

def precompute_pairs_data(pairs):
    """Precompute all per-pair data for fast metric computation."""
    BASIN_MAP = {"Kun": 0, "Qian": 1, "KanLi": 2}

    pd = {
        "h1": {}, "h2": {},
        "basin_id": {}, "h1_basin_id": {}, "h2_basin_id": {},
        "orbit_sig_id": {},
        "complement_pair_idx": {},
        "yang_count": {},
        "hamming_cache": {},
        "torus_cache": {},
    }

    # Orbit sig → integer ID
    orbit_sig_map = {}
    orbit_counter = 0

    all_h1 = set()
    all_h2 = set()

    for p in pairs:
        pi = p["pair_idx"]
        pd["h1"][pi] = p["h1"]
        pd["h2"][pi] = p["h2"]
        pd["basin_id"][pi] = BASIN_MAP[p["basin"]]
        pd["h1_basin_id"][pi] = BASIN_MAP[basin(p["h1"])]
        pd["h2_basin_id"][pi] = BASIN_MAP[basin(p["h2"])]
        pd["complement_pair_idx"][pi] = p["complement_pair_idx"]

        osig = p["orbit_sig"]
        if osig not in orbit_sig_map:
            orbit_sig_map[osig] = orbit_counter
            orbit_counter += 1
        pd["orbit_sig_id"][pi] = orbit_sig_map[osig]

        all_h1.add(p["h1"])
        all_h2.add(p["h2"])

    # Yang count for all hexagrams
    for h in range(NUM_HEX):
        pd["yang_count"][h] = bin(h).count("1")

    # Hamming cache for all bridge transitions (h2 → h1)
    all_hexes = all_h1 | all_h2
    for a in all_h2:
        for b in all_h1:
            pd["hamming_cache"][(a, b)] = hamming6(a, b)

    # Torus cache for all consecutive hex transitions
    for a in range(NUM_HEX):
        for b in range(NUM_HEX):
            pd["torus_cache"][(a, b)] = torus_manhattan(a, b)

    return pd

# ─── Mawangdui sequence ─────────────────────────────────────────────────────

# Mawangdui upper trigram order: Qian, Kun, Gen, Dui, Kan, Li, Zhen, Xun
# Lower trigram cycles in same order within each group
MWD_UPPER_ORDER = [0b111, 0b000, 0b100, 0b011, 0b010, 0b101, 0b001, 0b110]
MWD_LOWER_ORDER = [0b111, 0b000, 0b100, 0b011, 0b010, 0b101, 0b001, 0b110]

def build_mawangdui_sequence():
    """Reconstruct Mawangdui sequence: 64 hexagrams in MWD order."""
    seq = []
    for upper in MWD_UPPER_ORDER:
        for lower in MWD_LOWER_ORDER:
            h = lower | (upper << 3)
            seq.append(h)
    return seq

def build_mawangdui_pairs():
    """Apply KW pairing rule to Mawangdui sequence to get pairs."""
    mwd_seq = build_mawangdui_sequence()

    # Group into consecutive pairs
    paired = set()
    pairs = []
    pair_idx = 0
    for h in mwd_seq:
        if h in paired:
            continue
        partner = kw_partner(h)
        pairs.append({
            "pair_idx": pair_idx,
            "h1": h, "h2": partner,
            "h1_elem_pair": elem_pair(h),
            "h2_elem_pair": elem_pair(partner),
            "basin": basin(h),
            "orbit_sig": orbit_sig(h),
        })
        paired.add(h)
        paired.add(partner)
        pair_idx += 1

    # Add complement pair indices
    val_to_pair = {}
    for p in pairs:
        val_to_pair[p["h1"]] = p["pair_idx"]
        val_to_pair[p["h2"]] = p["pair_idx"]
    for p in pairs:
        comp_h1 = p["h1"] ^ MASK_ALL
        p["complement_pair_idx"] = val_to_pair[comp_h1]

    return pairs

# ─── Monte Carlo generation ─────────────────────────────────────────────────

def check_anti_clustering_fast(ordering_indices, pd):
    """Fast anti-clustering check using precomputed element pairs."""
    seq = []
    for i in ordering_indices:
        seq.append(pd["h1_elem_pair"][i])
        seq.append(pd["h2_elem_pair"][i])
    for i in range(len(seq) - 1):
        if seq[i] == seq[i + 1]:
            return False
    return True

def precompute_elem_pairs(pairs):
    """Precompute element pairs for fast constraint checking."""
    pd = {"h1_elem_pair": {}, "h2_elem_pair": {}}
    for p in pairs:
        pi = p["pair_idx"]
        pd["h1_elem_pair"][pi] = elem_pair(p["h1"])
        pd["h2_elem_pair"][pi] = elem_pair(p["h2"])
    return pd

def generate_valid_orderings(pairs, n_target, seed=SEED):
    """Generate n_target valid orderings via rejection sampling."""
    random.seed(seed)

    ep_data = precompute_elem_pairs(pairs)
    middle_indices = list(range(1, NUM_PAIRS - 1))  # pairs 1-30

    valid_orderings = []
    attempts = 0

    while len(valid_orderings) < n_target:
        random.shuffle(middle_indices)
        ordering = [0] + list(middle_indices) + [NUM_PAIRS - 1]
        attempts += 1

        if check_anti_clustering_fast(ordering, ep_data):
            valid_orderings.append(ordering[:])

        if attempts % 10000 == 0:
            rate = len(valid_orderings) / attempts
            print(f"  {len(valid_orderings)}/{n_target} valid after {attempts} attempts ({rate*100:.1f}%)")

    rate = len(valid_orderings) / attempts
    print(f"  Final: {len(valid_orderings)} valid from {attempts} attempts ({rate*100:.2f}%)")
    return valid_orderings, attempts, rate

# ─── Output formatting ──────────────────────────────────────────────────────

METRIC_NAMES = [
    "basin_clustering",
    "bridge_hamming_mean",
    "bridge_hamming_max",
    "orbit_unique_edges",
    "orbit_oneway_frac",
    "complement_distance_median",
    "complement_distance_mean",
    "split15_basin_balance",
    "yang_total_first_half",
    "basin_run_count",
    "basin_run_mean_length",
    "torus_step_mean",
]

def format_results(kw_metrics, mwd_metrics, null_metrics, acceptance_rate, n_attempts,
                   pairs, comp_map):
    """Format results as markdown."""
    lines = []
    w = lines.append

    w("# KW Sequence Ordering — Monte Carlo Comparison\n")
    w(f"**Monte Carlo samples:** {N_MONTE_CARLO:,} valid orderings")
    w(f"**Acceptance rate:** {acceptance_rate*100:.2f}% ({n_attempts:,} total attempts)")
    w(f"**Constraints:** Fixed endpoints (Qian/Kun at 0, JiJi/WeiJi at 31) + Z₅×Z₅ anti-clustering\n")

    # ── Metric comparison table ──
    w("## Metric Comparison\n")
    w("| Metric | KW | MWD | Null Mean | Null Std | KW %ile | KW z-score | Flag |")
    w("|--------|-----|-----|-----------|----------|---------|------------|------|")

    discriminating = []
    for m in METRIC_NAMES:
        kw_val = kw_metrics[m]
        mwd_val = mwd_metrics[m]
        null_vals = np.array(null_metrics[m])
        null_mean = np.mean(null_vals)
        null_std = np.std(null_vals)
        # Mid-rank percentile: P(X < val) + 0.5 * P(X == val)
        below = np.sum(null_vals < kw_val)
        equal = np.sum(null_vals == kw_val)
        pct = 100.0 * (below + 0.5 * equal) / len(null_vals)
        zscore = (kw_val - null_mean) / null_std if null_std > 0 else 0

        flag = ""
        if pct < 1 or pct > 99:
            flag = "★ DISCRIMINATING"
            discriminating.append((m, kw_val, pct, zscore))
        elif pct < 5 or pct > 95:
            flag = "• Notable"

        w(f"| {m} | {kw_val:.4f} | {mwd_val:.4f} | {null_mean:.4f} | {null_std:.4f} | {pct:.1f}% | {zscore:+.2f} | {flag} |")

    w("")

    # ── Complement pair map ──
    w("## Complement Pair Map\n")

    self_comp = []
    comp_orbits = []
    seen = set()

    for p in pairs:
        pi = p["pair_idx"]
        ci = p["complement_pair_idx"]
        if pi == ci:
            self_comp.append(p)
        else:
            key = (min(pi, ci), max(pi, ci))
            if key not in seen:
                seen.add(key)
                comp_orbits.append((pi, ci, abs(pi - ci)))

    w(f"### Self-complementary pairs ({len(self_comp)})\n")
    w("| Pair # | h1 | h2 | Basin |")
    w("|--------|----|----|-------|")
    for p in self_comp:
        w(f"| {p['pair_idx']} | {p['h1']} ({p['name1']}) | {p['h2']} ({p['name2']}) | {p['basin']} |")
    w("")

    w(f"### Complement orbits ({len(comp_orbits)} pairs)\n")
    w("| Pair A | Pair B | Distance |")
    w("|--------|--------|----------|")
    for pi, ci, dist in sorted(comp_orbits, key=lambda x: x[2]):
        pa = pairs[pi]
        pb = pairs[ci]
        w(f"| {pi} ({pa.get('name1','')}/{pa.get('name2','')}) | {ci} ({pb.get('name1','')}/{pb.get('name2','')}) | {dist} |")
    w("")

    # ── Basin verification ──
    w("## Basin Pairing Verification\n")
    basin_mismatches = []
    for p in pairs:
        b1 = basin(p["h1"])
        b2 = basin(p["h2"])
        if b1 != b2:
            basin_mismatches.append((p["pair_idx"], p["h1"], p["h2"], b1, b2))
    if basin_mismatches:
        w(f"**{len(basin_mismatches)} pairs have mismatched basins** (palindromic complement pairs):\n")
        w("| Pair # | h1 | h2 | Basin(h1) | Basin(h2) |")
        w("|--------|----|----|-----------|-----------|")
        for pi, h1, h2, b1, b2 in basin_mismatches:
            w(f"| {pi} | {h1} | {h2} | {b1} | {b2} |")
        w("\nBasin is computed from h1 of each pair.\n")
    else:
        w("All pairs share the same basin between h1 and h2.\n")

    # ── Summary ──
    w("## Summary\n")
    if discriminating:
        w("### Discriminating dimensions (KW percentile < 1% or > 99%):\n")
        for m, val, pct, zs in discriminating:
            direction = "unusually HIGH" if pct > 50 else "unusually LOW"
            w(f"- **{m}** = {val:.4f} (percentile {pct:.1f}%, z={zs:+.2f}) — {direction}")
        w("")
    else:
        w("No metrics fall below 1st or above 99th percentile.\n")

    w("### Interpretation\n")
    w("These metrics test whether the KW pair *ordering* is special,")
    w("given that the pairing rule and anti-clustering constraint are already satisfied.")
    w("Discriminating metrics point to additional structure beyond the known constraints.\n")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("KW SEQUENCE ORDERING — MONTE CARLO COMPARISON")
    print("=" * 70)

    # ── Build KW pairs ──
    print("\n1. Building KW pairs...")
    pairs = build_kw_pairs()
    print(f"   {len(pairs)} pairs built")

    # Verify constraint
    assert check_anti_clustering(pairs), "KW sequence violates anti-clustering!"
    print("   Anti-clustering constraint verified ✓")

    # ── Compute KW metrics ──
    print("\n2. Computing KW metrics...")
    kw_metrics = compute_metrics(pairs)
    for m in METRIC_NAMES:
        print(f"   {m}: {kw_metrics[m]:.4f}")

    # ── Build Mawangdui pairs ──
    print("\n3. Building Mawangdui pairs...")
    mwd_pairs = build_mawangdui_pairs()
    print(f"   {len(mwd_pairs)} pairs built")
    mwd_metrics = compute_metrics(mwd_pairs)
    print("   Mawangdui metrics computed (note: reconstructed sequence)")

    # ── Precompute for fast Monte Carlo ──
    print("\n4. Precomputing data structures...")
    pd = precompute_pairs_data(pairs)

    # Verify fast metrics match slow metrics
    kw_ordering = list(range(NUM_PAIRS))
    kw_metrics_fast = compute_metrics_fast(kw_ordering, pd)
    for m in METRIC_NAMES:
        assert abs(kw_metrics[m] - kw_metrics_fast[m]) < 1e-10, \
            f"Fast/slow mismatch on {m}: {kw_metrics[m]} vs {kw_metrics_fast[m]}"
    print("   Fast metrics verified ✓")

    # ── Monte Carlo ──
    print(f"\n5. Generating {N_MONTE_CARLO:,} valid orderings...")
    valid_orderings, n_attempts, acceptance_rate = generate_valid_orderings(pairs, N_MONTE_CARLO)

    print(f"\n6. Computing metrics for {N_MONTE_CARLO:,} orderings...")
    null_metrics = {m: [] for m in METRIC_NAMES}
    for idx, ordering in enumerate(valid_orderings):
        metrics = compute_metrics_fast(ordering, pd)
        for m in METRIC_NAMES:
            null_metrics[m].append(metrics[m])
        if (idx + 1) % 10000 == 0:
            print(f"   {idx + 1:,}/{N_MONTE_CARLO:,}")

    # ── Save null distributions for downstream analysis ──
    print("\n7. Saving null distributions...")
    save_data = {f"null_{m}": np.array(null_metrics[m]) for m in METRIC_NAMES}
    save_data["kw_metrics"] = np.array([kw_metrics[m] for m in METRIC_NAMES])
    save_data["metric_names"] = np.array(METRIC_NAMES)
    npz_path = SCRIPT_DIR / "01_null_distributions.npz"
    np.savez_compressed(npz_path, **save_data)
    print(f"   Saved to {npz_path}")

    # ── Format and write results ──
    print("\n8. Writing results...")
    comp_map = {}
    for p in pairs:
        comp_map[p["pair_idx"]] = p["complement_pair_idx"]

    md = format_results(kw_metrics, mwd_metrics, null_metrics, acceptance_rate,
                        n_attempts, pairs, comp_map)

    out_path = SCRIPT_DIR / "01_ordering_results.md"
    out_path.write_text(md)
    print(f"   Results written to {out_path}")

    # Print summary to stdout
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Acceptance rate: {acceptance_rate*100:.2f}%")
    print(f"\n{'Metric':<30} {'KW':>8} {'%ile':>8} {'z':>8}")
    print("-" * 58)
    for m in METRIC_NAMES:
        null_vals = np.array(null_metrics[m])
        below = np.sum(null_vals < kw_metrics[m])
        equal = np.sum(null_vals == kw_metrics[m])
        pct = 100.0 * (below + 0.5 * equal) / len(null_vals)
        zs = (kw_metrics[m] - np.mean(null_vals)) / np.std(null_vals) if np.std(null_vals) > 0 else 0
        flag = " ★" if pct < 1 or pct > 99 else " •" if pct < 5 or pct > 95 else ""
        print(f"{m:<30} {kw_metrics[m]:>8.4f} {pct:>7.1f}% {zs:>+7.2f}{flag}")


if __name__ == "__main__":
    main()
