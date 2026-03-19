"""
Probe 3: Composed Dynamics + Alternative Assignment Test

Part A: Alternative element assignments — 互 transition matrices
Part B: Composed dynamics (line-change × 互)
"""

import json
import numpy as np
from collections import Counter
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]

SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

ELEMENTS = ["Earth", "Wood", "Water", "Metal", "Fire"]

# ── Loading ────────────────────────────────────────────────────────

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def load_transitions():
    with open(ATLAS_DIR / "transitions.json") as f:
        return json.load(f)["bian_fan"]

def hu_formula(h):
    b = [(h >> i) & 1 for i in range(6)]
    return b[1] | (b[2] << 1) | (b[3] << 2) | (b[2] << 3) | (b[3] << 4) | (b[4] << 5)

def get_trigram_elements(atlas):
    elems = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            elems[t["val"]] = t["element"]
    return elems

def wuxing_group(e1, e2):
    if e1 == e2:
        return "比和"
    if SHENG[e1] == e2 or SHENG[e2] == e1:
        return "生"
    if KE[e1] == e2 or KE[e2] == e1:
        return "克"
    raise ValueError(f"No relation: {e1} ↔ {e2}")

def surface_group_from_map(h, elem_map):
    return wuxing_group(elem_map[h & 7], elem_map[(h >> 3) & 7])


# ══════════════════════════════════════════════════════════════════
# PART A: Alternative Assignments — 互 Transition Matrices
# ══════════════════════════════════════════════════════════════════

def generate_all_assignments():
    """
    Generate all distinct element assignments to trigrams, using the
    structural slot pattern: pair_A=(0,4), pair_B=(3,7), pair_C=(1,6),
    single_D=2, single_E=5.
    """
    seen_partitions = {}
    for perm in permutations(ELEMENTS):
        elem_map = {
            0: perm[0], 4: perm[0],
            3: perm[1], 7: perm[1],
            1: perm[2], 6: perm[2],
            2: perm[3],
            5: perm[4],
        }

        # Compute partition key
        groups = {g: frozenset(h for h in range(64) if surface_group_from_map(h, elem_map) == g)
                  for g in GROUP_NAMES}
        key = tuple(sorted(groups.items()))

        if key not in seen_partitions:
            seen_partitions[key] = {
                "perm": list(perm),
                "elem_map": dict(elem_map),
                "groups": {g: sorted(s) for g, s in groups.items()},
                "sizes": {g: len(s) for g, s in groups.items()},
            }

    return list(seen_partitions.values())

def compute_hu_transition_matrix(elem_map):
    """3×3 transition matrix under 互 for a given element assignment."""
    trans = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
    for h in range(64):
        src = surface_group_from_map(h, elem_map)
        dst = surface_group_from_map(hu_formula(h), elem_map)
        trans[(src, dst)] += 1
    return trans

def part_a(atlas):
    print("\n" + "═" * 70)
    print("PART A: ALTERNATIVE ELEMENT ASSIGNMENTS — 互 TRANSITION MATRICES")
    print("═" * 70)

    actual_elems = get_trigram_elements(atlas)
    assignments = generate_all_assignments()

    print(f"\n  Total distinct assignments: {len(assignments)}")

    results_a = []
    zero_cells_summary = []

    for i, asgn in enumerate(assignments):
        is_actual = (asgn["elem_map"] == {k: actual_elems[k] for k in range(8)})
        trans = compute_hu_transition_matrix(asgn["elem_map"])

        # Find zero cells
        zeros = [(a, b) for (a, b), v in trans.items() if v == 0]

        marker = " ← ACTUAL" if is_actual else ""
        print(f"\n  Assignment {i+1}{marker}: {asgn['perm']}")
        print(f"    Sizes: {asgn['sizes']}")
        print(f"    {'src→dst':>8} | {'比和':>5} {'生':>5} {'克':>5}")
        print(f"    {'-'*8}-+-{'-'*5}-{'-'*5}-{'-'*5}")
        for src in GROUP_NAMES:
            row = [trans[(src, dst)] for dst in GROUP_NAMES]
            print(f"    {src:>8} | {row[0]:>5} {row[1]:>5} {row[2]:>5}")
        print(f"    Zero cells: {zeros if zeros else 'NONE'}")

        results_a.append({
            "perm": asgn["perm"],
            "sizes": asgn["sizes"],
            "is_actual": is_actual,
            "transition_matrix": {f"{a}→{b}": v for (a, b), v in trans.items()},
            "zero_cells": [f"{a}→{b}" for a, b in zeros],
        })
        zero_cells_summary.append((i + 1, is_actual, zeros))

    print("\n  ── Summary: Zero Cells ──")
    for idx, is_actual, zeros in zero_cells_summary:
        marker = " ← ACTUAL" if is_actual else ""
        z_str = ", ".join(f"{a}→{b}" for a, b in zeros) if zeros else "none"
        print(f"    Assignment {idx}{marker}: {z_str}")

    all_have_zero = all(len(z) > 0 for _, _, z in zero_cells_summary)
    print(f"\n  All assignments have ≥1 zero cell: {all_have_zero}")

    return results_a


# ══════════════════════════════════════════════════════════════════
# PART B: Composed Dynamics (line-change × 互)
# ══════════════════════════════════════════════════════════════════

def build_composed_maps():
    """For each line k (0-5), build F_k(h) = hu(h XOR (1<<k))."""
    maps = {}
    for k in range(6):
        maps[k] = {}
        for h in range(64):
            flipped = h ^ (1 << k)
            maps[k][h] = hu_formula(flipped)
    return maps

def build_composed_adjacency(composed_maps):
    """64×64 adjacency with multiplicity (summing over all 6 lines)."""
    A = np.zeros((64, 64), dtype=int)
    for k in range(6):
        for h in range(64):
            A[h, composed_maps[k][h]] += 1
    return A

def compute_orbit(func_map, start):
    """Compute orbit of start under func_map until cycle found."""
    trajectory = [start]
    visited = {start: 0}
    current = start
    while True:
        nxt = func_map[current]
        if nxt in visited:
            cycle_start = visited[nxt]
            return {
                "trajectory": trajectory,
                "transient": trajectory[:cycle_start],
                "cycle": trajectory[cycle_start:],
                "transient_length": cycle_start,
                "cycle_length": len(trajectory) - cycle_start,
            }
        visited[nxt] = len(trajectory)
        trajectory.append(nxt)
        current = nxt

def part_b(atlas, composed_maps):
    print("\n" + "═" * 70)
    print("PART B: COMPOSED DYNAMICS (line-change × 互)")
    print("═" * 70)

    actual_elems = get_trigram_elements(atlas)
    results_b = {}

    # ── B1: Composed adjacency ─────────────────────────────────────
    print("\n── B1. Composed Map h → hu(flip(h, k)) ──")

    A = build_composed_adjacency(composed_maps)

    # Out-degree: always 6 (by construction)
    in_deg = A.sum(axis=0)
    in_deg_dist = dict(sorted(Counter(in_deg.tolist()).items()))
    print(f"  In-degree distribution: {in_deg_dist}")

    # Distinct targets per hexagram
    distinct_per_hex = []
    for h in range(64):
        targets = set(composed_maps[k][h] for k in range(6))
        distinct_per_hex.append(len(targets))
    distinct_dist = dict(sorted(Counter(distinct_per_hex).items()))
    print(f"  Distinct targets per hexagram: {distinct_dist}")

    # Image of composed map
    all_targets = set()
    for k in range(6):
        for h in range(64):
            all_targets.add(composed_maps[k][h])
    print(f"  Total reachable states: {len(all_targets)} (互 alone: 16)")

    # Per-line images
    for k in range(6):
        img = set(composed_maps[k][h] for h in range(64))
        print(f"    Line {k+1} (bit {k}): image size = {len(img)}")

    results_b["b1"] = {
        "in_degree_distribution": in_deg_dist,
        "distinct_targets_distribution": distinct_dist,
        "total_reachable": len(all_targets),
        "per_line_image_sizes": {k + 1: len(set(composed_maps[k][h] for h in range(64))) for k in range(6)},
    }

    # ── B2: Hinge test ─────────────────────────────────────────────
    print("\n── B2. Hinge Test ──")
    print("  Lines 3,4 (bits 2,3) are the 'hinge' — the only bits surviving iterated 互")

    # For each line k, analyze the composed map F_k(h) = hu(h XOR (1<<k))
    # F_k bit formula:
    # h XOR (1<<k) flips bit k. Then hu extracts (b1,b2,b3,b2,b3,b4).
    # So F_k(h) depends on which bits of h are used after the flip.

    print("\n  Per-line output distribution (how 64 hexagrams distribute across targets):")
    hinge_data = {}
    for k in range(6):
        targets = [composed_maps[k][h] for h in range(64)]
        target_counts = Counter(targets)
        n_targets = len(target_counts)
        max_count = max(target_counts.values())
        min_count = min(target_counts.values())
        entropy = -sum((c / 64) * np.log2(c / 64) for c in target_counts.values())

        line_type = "HINGE" if k in [2, 3] else "outer"
        print(f"    Line {k+1} (bit {k}) [{line_type}]: {n_targets} targets, "
              f"counts range [{min_count}, {max_count}], entropy = {entropy:.3f}")

        hinge_data[k + 1] = {
            "n_targets": n_targets,
            "max_count": max_count,
            "min_count": min_count,
            "entropy": float(entropy),
            "is_hinge": k in [2, 3],
        }

    # How outputs distribute across the 16 互-image elements
    hu_image = set(hu_formula(h) for h in range(64))
    print(f"\n  Distribution across 互-image elements:")
    for k in range(6):
        targets = [composed_maps[k][h] for h in range(64)]
        in_hu_image = sum(1 for t in targets if t in hu_image)
        outside = 64 - in_hu_image
        line_type = "HINGE" if k in [2, 3] else "outer"
        print(f"    Line {k+1} [{line_type}]: {in_hu_image}/64 land in 互-image, {outside} outside")

    results_b["b2"] = hinge_data

    # ── B3: Markov chain ───────────────────────────────────────────
    print("\n── B3. Markov Chain: Random-Line-Then-互 ──")

    M = A.astype(float) / 6.0  # Row-stochastic transition matrix

    # Eigenvalues
    eigvals = np.linalg.eigvals(M)
    eigvals_sorted = sorted(eigvals, key=lambda x: -abs(x))
    real_eigs = sorted([v.real for v in eigvals if abs(v.imag) < 1e-10], reverse=True)

    print(f"  Top 5 eigenvalues (by magnitude): {[f'{v:.6f}' for v in eigvals_sorted[:5]]}")
    print(f"  Spectral gap (1 - |λ₂|): {1 - abs(eigvals_sorted[1]):.6f}")

    # Stationary distribution: left eigenvector for eigenvalue 1
    # For a row-stochastic matrix, stationary = left eigenvector of eigenvalue 1
    # Equivalently: right eigenvector of M^T for eigenvalue 1
    eigvals_T, eigvecs_T = np.linalg.eig(M.T)
    idx = np.argmin(np.abs(eigvals_T - 1.0))
    pi = eigvecs_T[:, idx].real
    pi = pi / pi.sum()  # Normalize

    print(f"  Stationary distribution range: [{pi.min():.6f}, {pi.max():.6f}]")
    print(f"  Uniform would be {1/64:.6f}")
    print(f"  Max/min ratio: {pi.max()/pi.min():.4f}")

    # Top/bottom hexagrams
    sorted_hex = sorted(range(64), key=lambda h: -pi[h])
    print(f"\n  Top 10 most-visited:")
    for h in sorted_hex[:10]:
        sr = RELATION_GROUPS[atlas[str(h)]["surface_relation"]]
        hu = hu_formula(h)
        print(f"    hex {h:2d} ({format(h, '06b')}): π={pi[h]:.6f}, sr={sr}, hu={hu}")

    print(f"\n  Bottom 10 least-visited:")
    for h in sorted_hex[-10:]:
        sr = RELATION_GROUPS[atlas[str(h)]["surface_relation"]]
        hu = hu_formula(h)
        print(f"    hex {h:2d} ({format(h, '06b')}): π={pi[h]:.6f}, sr={sr}, hu={hu}")

    # Check for absorbing states
    absorbing = [h for h in range(64) if M[h, h] == 1.0]
    print(f"\n  Absorbing states: {absorbing if absorbing else 'none'}")

    # Periodicity check
    n_real_1 = sum(1 for v in eigvals if abs(abs(v) - 1.0) < 1e-10)
    print(f"  Eigenvalues with |λ| = 1: {n_real_1}")

    # Mixing time estimate
    spectral_gap = 1 - abs(eigvals_sorted[1])
    if spectral_gap > 0:
        mixing_time = 1 / spectral_gap
        print(f"  Estimated mixing time (1/gap): {mixing_time:.2f}")

    # Stationary by 五行 type
    pi_by_type = {g: 0.0 for g in GROUP_NAMES}
    for h in range(64):
        g = RELATION_GROUPS[atlas[str(h)]["surface_relation"]]
        pi_by_type[g] += pi[h]
    print(f"\n  Stationary mass by 五行 type:")
    for g in GROUP_NAMES:
        n_hex = sum(1 for h in range(64) if RELATION_GROUPS[atlas[str(h)]["surface_relation"]] == g)
        print(f"    {g}: π_total = {pi_by_type[g]:.6f} (uniform would be {n_hex/64:.6f})")

    results_b["b3"] = {
        "spectral_gap": float(spectral_gap),
        "mixing_time": float(1 / spectral_gap) if spectral_gap > 0 else None,
        "stationary_distribution": {str(h): float(pi[h]) for h in range(64)},
        "pi_range": [float(pi.min()), float(pi.max())],
        "top_10": [{"hex": int(h), "pi": float(pi[h])} for h in sorted_hex[:10]],
        "bottom_10": [{"hex": int(h), "pi": float(pi[h])} for h in sorted_hex[-10:]],
        "absorbing_states": absorbing,
        "stationary_by_type": pi_by_type,
    }

    # ── B4: 五行 flow in composed dynamics ─────────────────────────
    print("\n── B4. 五行 Flow in Composed Dynamics ──")

    # Overall transition matrix (all 384 composed transitions)
    trans_all = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
    for k in range(6):
        for h in range(64):
            src = RELATION_GROUPS[atlas[str(h)]["surface_relation"]]
            dst_hex = composed_maps[k][h]
            dst = RELATION_GROUPS[atlas[str(dst_hex)]["surface_relation"]]
            trans_all[(src, dst)] += 1

    print(f"\n  Overall composed 五行 transition (384 transitions):")
    print(f"    {'src→dst':>8} | {'比和':>5} {'生':>5} {'克':>5}")
    print(f"    {'-'*8}-+-{'-'*5}-{'-'*5}-{'-'*5}")
    for src in GROUP_NAMES:
        row = [trans_all[(src, dst)] for dst in GROUP_NAMES]
        print(f"    {src:>8} | {row[0]:>5} {row[1]:>5} {row[2]:>5}")

    # Compare to 互-only (from P2)
    trans_hu = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
    for h in range(64):
        src = RELATION_GROUPS[atlas[str(h)]["surface_relation"]]
        dst = RELATION_GROUPS[atlas[str(hu_formula(h))]["surface_relation"]]
        trans_hu[(src, dst)] += 1

    zero_in_hu = [(a, b) for (a, b), v in trans_hu.items() if v == 0]
    zero_in_composed = [(a, b) for (a, b), v in trans_all.items() if v == 0]
    print(f"\n  克→生 in 互-only: {trans_hu[('克', '生')]}")
    print(f"  克→生 in composed: {trans_all[('克', '生')]}")
    print(f"  Zero cells in 互-only: {zero_in_hu}")
    print(f"  Zero cells in composed: {zero_in_composed if zero_in_composed else 'NONE'}")

    # Per-line breakdown
    print(f"\n  Per-line 五行 transitions:")
    trans_per_line = {}
    for k in range(6):
        trans_k = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
        for h in range(64):
            src = RELATION_GROUPS[atlas[str(h)]["surface_relation"]]
            dst = RELATION_GROUPS[atlas[str(composed_maps[k][h])]["surface_relation"]]
            trans_k[(src, dst)] += 1
        trans_per_line[k] = trans_k

        line_type = "HINGE" if k in [2, 3] else "outer"
        zeros_k = [(a, b) for (a, b), v in trans_k.items() if v == 0]
        ke_sheng = trans_k[("克", "生")]
        print(f"    Line {k+1} [{line_type}]: 克→生 = {ke_sheng}, zeros = "
              f"{[f'{a}→{b}' for a,b in zeros_k] if zeros_k else 'none'}")

    # Full per-line tables for hinge vs outer
    print(f"\n  Hinge lines (3,4) combined:")
    trans_hinge = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
    for k in [2, 3]:
        for (a, b), v in trans_per_line[k].items():
            trans_hinge[(a, b)] += v
    print(f"    {'src→dst':>8} | {'比和':>5} {'生':>5} {'克':>5}")
    print(f"    {'-'*8}-+-{'-'*5}-{'-'*5}-{'-'*5}")
    for src in GROUP_NAMES:
        row = [trans_hinge[(src, dst)] for dst in GROUP_NAMES]
        print(f"    {src:>8} | {row[0]:>5} {row[1]:>5} {row[2]:>5}")

    print(f"\n  Outer lines (1,2,5,6) combined:")
    trans_outer = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
    for k in [0, 1, 4, 5]:
        for (a, b), v in trans_per_line[k].items():
            trans_outer[(a, b)] += v
    print(f"    {'src→dst':>8} | {'比和':>5} {'生':>5} {'克':>5}")
    print(f"    {'-'*8}-+-{'-'*5}-{'-'*5}-{'-'*5}")
    for src in GROUP_NAMES:
        row = [trans_outer[(src, dst)] for dst in GROUP_NAMES]
        print(f"    {src:>8} | {row[0]:>5} {row[1]:>5} {row[2]:>5}")

    results_b["b4"] = {
        "overall_transition": {f"{a}→{b}": v for (a, b), v in trans_all.items()},
        "ke_sheng_survives": trans_all[("克", "生")] == 0,
        "per_line_ke_sheng": {k + 1: trans_per_line[k][("克", "生")] for k in range(6)},
        "hinge_transition": {f"{a}→{b}": v for (a, b), v in trans_hinge.items()},
        "outer_transition": {f"{a}→{b}": v for (a, b), v in trans_outer.items()},
    }

    # ── B5: Fixed points and cycles ────────────────────────────────
    print("\n── B5. Fixed Points and Cycles of Deterministic Maps ──")

    fp_data = {}
    for k in range(6):
        fm = composed_maps[k]
        fixed = [h for h in range(64) if fm[h] == h]
        two_cycles = []
        seen = set()
        for h in range(64):
            if h not in seen and fm[fm[h]] == h and fm[h] != h:
                two_cycles.append((h, fm[h]))
                seen.add(h)
                seen.add(fm[h])

        line_type = "HINGE" if k in [2, 3] else "outer"
        print(f"\n  Line {k+1} (F_{k+1}) [{line_type}]:")
        print(f"    Fixed points ({len(fixed)}): {fixed}")
        print(f"    2-cycles ({len(two_cycles)}): {two_cycles[:10]}{'...' if len(two_cycles) > 10 else ''}")

        fp_data[k + 1] = {
            "fixed_points": fixed,
            "n_fixed": len(fixed),
            "two_cycles": [list(c) for c in two_cycles],
            "n_two_cycles": len(two_cycles),
        }

    results_b["b5"] = fp_data

    # ── B6: Full orbit structure ───────────────────────────────────
    print("\n── B6. Orbit Structure of Deterministic Maps ──")

    orbit_data = {}
    for k in range(6):
        fm = composed_maps[k]

        orbits = {}
        for h in range(64):
            orbits[h] = compute_orbit(fm, h)

        max_trans = max(o["transient_length"] for o in orbits.values())
        trans_dist = dict(sorted(Counter(o["transient_length"] for o in orbits.values()).items()))
        cycle_lens = Counter(o["cycle_length"] for o in orbits.values())

        # Attractor structure: find all distinct cycles
        cycles = set()
        for o in orbits.values():
            cycles.add(tuple(o["cycle"]))
        cycles = sorted(cycles)

        # Basin sizes
        basin_sizes = []
        for cycle in cycles:
            cycle_set = set(cycle)
            basin = [h for h in range(64) if set(orbits[h]["cycle"]) == cycle_set]
            basin_sizes.append(len(basin))

        on_attractor = sum(1 for o in orbits.values() if o["transient_length"] == 0)

        line_type = "HINGE" if k in [2, 3] else "outer"
        print(f"\n  Line {k+1} (F_{k+1}) [{line_type}]:")
        print(f"    Max transient: {max_trans}")
        print(f"    Transient distribution: {trans_dist}")
        print(f"    Cycle lengths: {dict(sorted(cycle_lens.items()))}")
        print(f"    Number of attractors: {len(cycles)}")
        print(f"    Basin sizes: {sorted(basin_sizes, reverse=True)}")
        print(f"    Hexagrams on attractors: {on_attractor}/64")

        # Show cycles
        for i, cycle in enumerate(cycles):
            types = [RELATION_GROUPS[atlas[str(h)]["surface_relation"]] for h in cycle]
            if len(cycle) <= 8:
                cycle_str = " → ".join(f"{h}({t})" for h, t in zip(cycle, types))
            else:
                cycle_str = f"[length {len(cycle)}]"
            basin = [h for h in range(64) if set(orbits[h]["cycle"]) == set(cycle)]
            print(f"      Cycle {i+1}: {cycle_str} (basin size {len(basin)})")

        orbit_data[k + 1] = {
            "max_transient": max_trans,
            "transient_distribution": trans_dist,
            "cycle_lengths": dict(sorted(cycle_lens.items())),
            "n_attractors": len(cycles),
            "basin_sizes": sorted(basin_sizes, reverse=True),
            "on_attractor": on_attractor,
            "cycles": [list(c) for c in cycles],
        }

    results_b["b6"] = orbit_data

    return results_b


# ── Main ───────────────────────────────────────────────────────────

def main():
    atlas = load_atlas()

    print("=" * 70)
    print("PROBE 3: Composed Dynamics + Alternative Assignment Test")
    print("=" * 70)

    results_a = part_a(atlas)

    composed_maps = build_composed_maps()
    results_b = part_b(atlas, composed_maps)

    # Save
    json_results = {
        "part_a": results_a,
        "part_b": results_b,
    }

    out_path = HERE / "p3_results.json"
    with open(out_path, "w") as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
