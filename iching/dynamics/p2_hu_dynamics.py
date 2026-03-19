"""
Probe 2: 互 Map Dynamics + Real-Eigenvalue Null Test

Part A: The 互 (nuclear hexagram) map as a discrete dynamical system on Z₂⁶.
Part B: Null test for the real-eigenvalue property of directed 五行 subgraph matrices.
"""

import json
import numpy as np
from scipy import stats
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]
GROUP_SIZES = {"比和": 14, "生": 24, "克": 26}

# ── Loading ────────────────────────────────────────────────────────

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def hamming(a, b):
    return bin(a ^ b).count('1')

def build_q6():
    A = np.zeros((64, 64), dtype=int)
    for i in range(64):
        for bit in range(6):
            A[i, i ^ (1 << bit)] = 1
    return A

# ── Part A: 互 Map Dynamics ───────────────────────────────────────

def hu_formula(h):
    """Compute hu(h) from bit formula as consistency check."""
    b = [(h >> i) & 1 for i in range(6)]
    # Nuclear lower = lines 2,3,4 → bits 1,2,3
    # Nuclear upper = lines 3,4,5 → bits 2,3,4
    return (b[1]) | (b[2] << 1) | (b[3] << 2) | (b[2] << 3) | (b[3] << 4) | (b[4] << 5)

def compute_orbits(atlas):
    """Compute full orbit structure of the 互 map."""
    hu_map = {}
    for h in range(64):
        hu_atlas = atlas[str(h)]["hu_hex"]
        hu_comp = hu_formula(h)
        assert hu_atlas == hu_comp, f"hu mismatch at {h}: atlas={hu_atlas}, formula={hu_comp}"
        hu_map[h] = hu_atlas

    orbits = {}
    for h in range(64):
        trajectory = [h]
        visited = {h}
        current = h
        while True:
            nxt = hu_map[current]
            if nxt in visited:
                # Found the cycle
                cycle_start = trajectory.index(nxt)
                transient = trajectory[:cycle_start]
                cycle = trajectory[cycle_start:]
                break
            visited.add(nxt)
            trajectory.append(nxt)
            current = nxt

        orbits[h] = {
            "trajectory": trajectory,
            "transient_length": len(transient),
            "cycle": cycle,
            "cycle_length": len(cycle),
            "attractor": atlas[str(h)]["hu_attractor"],
        }
    return hu_map, orbits

def basin_analysis(atlas, orbits):
    """Basin membership and bit-determination test."""
    basins = {}
    for h in range(64):
        att = orbits[h]["attractor"]
        basins.setdefault(att, []).append(h)

    # Verify bits 2,3 determine basin
    # hu²(h) = 21*b₂ + 42*b₃ where b₂ = bit 2, b₃ = bit 3
    BIT_BASIN = {(0, 0): 0, (1, 0): 21, (0, 1): 42, (1, 1): 63}
    mismatches = 0
    for h in range(64):
        b2 = (h >> 2) & 1
        b3 = (h >> 3) & 1
        predicted = BIT_BASIN[(b2, b3)]
        actual = orbits[h]["attractor"]
        if predicted != actual:
            mismatches += 1
    bits_23_exact = mismatches == 0

    return basins, bits_23_exact

def preimage_structure(hu_map):
    """In-degree of each hexagram in the functional graph."""
    in_degree = Counter(hu_map.values())
    # Fill zeros
    for h in range(64):
        if h not in in_degree:
            in_degree[h] = 0
    return dict(sorted(in_degree.items()))

def wuxing_cross_tab(atlas, basins):
    """Basin × 五行 type cross-tabulation."""
    def vertex_type(h):
        return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

    table = {}
    for att in sorted(basins.keys()):
        row = Counter(vertex_type(h) for h in basins[att])
        table[att] = {g: row.get(g, 0) for g in GROUP_NAMES}

    # Chi-square test
    observed = np.array([[table[att][g] for g in GROUP_NAMES]
                          for att in sorted(table.keys())])
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)

    return table, chi2, p_value, dof, expected

def wuxing_transition_matrix(atlas, hu_map):
    """3×3 transition matrix between 五行 types under the 互 map."""
    def vtype(h):
        return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

    trans = {(a, b): 0 for a in GROUP_NAMES for b in GROUP_NAMES}
    for h in range(64):
        src_type = vtype(h)
        dst_type = vtype(hu_map[h])
        trans[(src_type, dst_type)] += 1

    return trans

def contraction_analysis(hu_map):
    """Contraction ratio d(hu(x),hu(y))/d(x,y) by starting distance."""
    by_dist = {d: [] for d in range(1, 7)}

    for x in range(64):
        for y in range(x + 1, 64):
            d_xy = hamming(x, y)
            d_hu = hamming(hu_map[x], hu_map[y])
            by_dist[d_xy].append(d_hu / d_xy)

    result = {}
    for d in range(1, 7):
        ratios = by_dist[d]
        result[d] = {
            "n_pairs": len(ratios),
            "mean_ratio": float(np.mean(ratios)),
            "std_ratio": float(np.std(ratios)),
            "min_ratio": float(np.min(ratios)),
            "max_ratio": float(np.max(ratios)),
        }
    return result

def contraction_by_type(atlas, hu_map):
    """Contraction ratio broken down by 五行 type pair."""
    def vtype(h):
        return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

    by_type = {}
    for x in range(64):
        for y in range(x + 1, 64):
            tx, ty = vtype(x), vtype(y)
            pair = tuple(sorted([tx, ty]))
            d_xy = hamming(x, y)
            d_hu = hamming(hu_map[x], hu_map[y])
            by_type.setdefault(pair, []).append(d_hu / d_xy)

    result = {}
    for pair, ratios in sorted(by_type.items()):
        result[str(pair)] = {
            "n_pairs": len(ratios),
            "mean_ratio": float(np.mean(ratios)),
            "std_ratio": float(np.std(ratios)),
        }
    return result

def distance_to_attractor(atlas, orbits):
    """Hamming distance to attractors by 五行 type."""
    ATTRACTORS = [0, 21, 42, 63]
    def vtype(h):
        return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

    results = {g: {"nearest": [], "own": []} for g in GROUP_NAMES}
    for h in range(64):
        g = vtype(h)
        nearest = min(hamming(h, a) for a in ATTRACTORS)
        own_att = orbits[h]["attractor"]
        own_dist = hamming(h, own_att)
        results[g]["nearest"].append(nearest)
        results[g]["own"].append(own_dist)

    summary = {}
    for g in GROUP_NAMES:
        summary[g] = {
            "mean_nearest": float(np.mean(results[g]["nearest"])),
            "mean_own": float(np.mean(results[g]["own"])),
            "nearest_dist": dict(Counter(results[g]["nearest"])),
            "own_dist": dict(Counter(results[g]["own"])),
        }
    return summary

def distance_to_specific_attractors(atlas, orbits):
    """Which attractor does each 五行 type converge to?"""
    def vtype(h):
        return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

    table = {}
    for g in GROUP_NAMES:
        table[g] = Counter()
    for h in range(64):
        g = vtype(h)
        att = orbits[h]["attractor"]
        table[g][att] += 1

    return table

# ── Part B: Real-Eigenvalue Null Test ──────────────────────────────

def check_all_real(matrices):
    """Check if all eigenvalues of all matrices are real."""
    for A in matrices:
        eigvals = np.linalg.eigvals(A.astype(float))
        if np.max(np.abs(np.imag(eigvals))) > 1e-10:
            return False
    return True

def real_eigenvalue_null_test(A_q6, n_trials=1000):
    """Random partition null test for real eigenvalues."""
    np.random.seed(42)
    sizes = [14, 24, 26]  # 比和, 生, 克
    n_all_real = 0

    for _ in range(n_trials):
        perm = np.random.permutation(64)
        groups = [set(perm[:14]), set(perm[14:38]), set(perm[38:])]

        matrices = []
        for group in groups:
            P = np.zeros((64, 64), dtype=int)
            for h in group:
                P[h, h] = 1
            matrices.append(P @ A_q6)

        if check_all_real(matrices):
            n_all_real += 1

    return n_all_real, n_trials

def alternative_assignments_test(A_q6, atlas):
    """
    Test alternative complement-pair assignments.

    The 8 trigrams form 4 complement pairs: (0,7), (1,6), (2,5), (3,4).
    Elements: {Earth, Wood, Water, Fire, Metal}.
    Current assignment: 0,4→Earth; 1,6→Wood; 2→Water; 5→Fire; 3,7→Metal.

    Note: the complement pairs map to: (Earth,Metal), (Wood,Wood), (Water,Fire), (Earth,Metal).
    Actually: trigram elements are: 0=Earth, 1=Wood, 2=Water, 3=Metal, 4=Earth, 5=Fire, 6=Wood, 7=Metal.
    Complement pairs: (0→Earth, 7→Metal), (1→Wood, 6→Wood), (2→Water, 5→Fire), (3→Metal, 4→Earth).

    The actual assignment has a specific pattern of which elements go to which trigrams.
    Alternative assignments permute the 5 elements across the same structural positions.
    """
    # Get the actual trigram elements
    trigram_elements = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            trigram_elements[t["val"]] = t["element"]

    # The 五行 relation between two elements
    SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
    KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}

    def get_group(e1, e2):
        if e1 == e2:
            return "比和"
        if SHENG[e1] == e2 or SHENG[e2] == e1:
            return "生"
        return "克"

    def surface_group(h, elem_map):
        lower_elem = elem_map[h & 7]
        upper_elem = elem_map[(h >> 3) & 7]
        return get_group(lower_elem, upper_elem)

    # Generate alternative element assignments by permuting elements
    # The actual assignment: [Earth, Wood, Water, Metal, Earth, Fire, Wood, Metal]
    # Alternative: permute the 5 elements
    from itertools import permutations

    elements = ["Earth", "Wood", "Water", "Metal", "Fire"]
    actual_map = trigram_elements.copy()

    # The structure is: pairs (0,4)=same element, (3,7)=same element, (1,6)=same element
    # Single: 2, 5
    # Current: pair(0,4)=Earth, pair(3,7)=Metal, pair(1,6)=Wood, single(2)=Water, single(5)=Fire

    # We can permute elements while preserving the structural constraint that
    # complement pairs get specific elements. The actual constraint from the
    # 五行 surjection is more complex, but let's just test random permutations
    # of the 5 elements applied to the same structural slots.

    # Test: for each permutation of 5 elements, assign to structural slots
    # Slots: [pair_A, pair_B, pair_C, single_D, single_E]
    # Actual: pair_A=Earth(0,4), pair_B=Metal(3,7), pair_C=Wood(1,6), single_D=Water(2), single_E=Fire(5)
    # Alternative: permute which element goes where

    results = []
    tested_partitions = set()

    for perm in permutations(elements):
        elem_map = {
            0: perm[0], 4: perm[0],  # pair A
            3: perm[1], 7: perm[1],  # pair B
            1: perm[2], 6: perm[2],  # pair C
            2: perm[3],              # single D
            5: perm[4],              # single E
        }

        # Compute partition
        groups_hex = {g: set() for g in GROUP_NAMES}
        for h in range(64):
            groups_hex[surface_group(h, elem_map)].add(h)

        partition_key = tuple(sorted(
            tuple(sorted(groups_hex[g])) for g in GROUP_NAMES
        ))
        if partition_key in tested_partitions:
            continue
        tested_partitions.add(partition_key)

        sizes = {g: len(groups_hex[g]) for g in GROUP_NAMES}

        # Build directed matrices
        matrices = []
        for g in GROUP_NAMES:
            P = np.zeros((64, 64), dtype=int)
            for h in groups_hex[g]:
                P[h, h] = 1
            matrices.append(P @ A_q6)

        all_real = check_all_real(matrices)
        is_actual = (elem_map == actual_map)

        results.append({
            "perm": list(perm),
            "sizes": sizes,
            "all_real": bool(all_real),
            "is_actual": is_actual,
        })

    return results


# ── Main ───────────────────────────────────────────────────────────

def main():
    atlas = load_atlas()
    A_q6 = build_q6()

    print("=" * 70)
    print("PROBE 2: 互 Map Dynamics + Real-Eigenvalue Null Test")
    print("=" * 70)

    # ══════════════════════════════════════════════════════════════
    # PART A: 互 Map Dynamics
    # ══════════════════════════════════════════════════════════════
    print("\n" + "═" * 70)
    print("PART A: 互 MAP AS DISCRETE DYNAMICAL SYSTEM")
    print("═" * 70)

    hu_map, orbits = compute_orbits(atlas)

    # ── A1: Orbit structure ────────────────────────────────────────
    print("\n── A1. Orbit Structure ──")

    max_transient = max(o["transient_length"] for o in orbits.values())
    print(f"  Max transient length: {max_transient}")

    transient_dist = Counter(o["transient_length"] for o in orbits.values())
    print(f"  Transient length distribution: {dict(sorted(transient_dist.items()))}")

    cycle_lengths = Counter(o["cycle_length"] for o in orbits.values())
    print(f"  Cycle length distribution: {dict(sorted(cycle_lengths.items()))}")

    attractors = sorted(set(o["attractor"] for o in orbits.values()))
    print(f"  Attractors: {attractors}")
    for att in attractors:
        cycle = orbits[att]["cycle"]
        print(f"    {att} ({format(att, '06b')}): cycle = {cycle}")

    # Show image of hu
    image = sorted(set(hu_map.values()))
    print(f"\n  Image of hu: {image} (size {len(image)})")
    image2 = sorted(set(hu_map[hu_map[h]] for h in range(64)))
    print(f"  Image of hu²: {image2} (size {len(image2)})")

    # ── A2: Algebraic explanation ──────────────────────────────────
    print("\n── A2. Algebraic Structure ──")
    print("  hu²(h) = 21·b₂ + 42·b₃  where b₂ = bit 2, b₃ = bit 3 of h")
    print("  Basin determined exactly by (bit2, bit3):")
    print("    (0,0) → 0,  (1,0) → 21,  (0,1) → 42,  (1,1) → 63")

    # Verify
    for h in range(64):
        b2, b3 = (h >> 2) & 1, (h >> 3) & 1
        assert hu_map[hu_map[h]] == 21 * b2 + 42 * b3

    print("  ✓ Verified for all 64 hexagrams")

    # ── A3: Basin structure ────────────────────────────────────────
    print("\n── A3. Basin Structure ──")
    basins, bits_23_exact = basin_analysis(atlas, orbits)
    print(f"  Bits 2,3 determine basin exactly: {bits_23_exact}")

    for att in sorted(basins.keys()):
        members = sorted(basins[att])
        print(f"\n  Basin of {att} ({format(att, '06b')}): size {len(members)}")
        print(f"    Members: {members}")
        # Show bit pattern
        b2_vals = set((h >> 2) & 1 for h in members)
        b3_vals = set((h >> 3) & 1 for h in members)
        print(f"    All have bit2={b2_vals}, bit3={b3_vals}")

    # ── A4: Preimage structure ─────────────────────────────────────
    print("\n── A4. Preimage Structure (in-degree) ──")
    in_deg = preimage_structure(hu_map)
    in_deg_dist = Counter(in_deg.values())
    print(f"  In-degree distribution: {dict(sorted(in_deg_dist.items()))}")
    print(f"  Hexagrams with in-degree > 0 (= image): {sum(1 for d in in_deg.values() if d > 0)}")

    # Show in-degrees of attractors and image elements
    print("\n  In-degrees of image elements:")
    for h in sorted(set(hu_map.values())):
        print(f"    hex {h:2d} ({format(h, '06b')}): in-degree = {in_deg[h]}")

    # ── A5: Basin × 五行 cross-tabulation ──────────────────────────
    print("\n── A5. Basin × 五行 Cross-Tabulation ──")
    table, chi2, p_value, dof, expected = wuxing_cross_tab(atlas, basins)

    print(f"\n  {'Basin':>8} | {'比和':>5} {'生':>5} {'克':>5} | Total")
    print(f"  {'-'*8}-+-{'-'*5}-{'-'*5}-{'-'*5}-+------")
    for att in sorted(table.keys()):
        row = table[att]
        total = sum(row.values())
        print(f"  {att:>8} | {row['比和']:>5} {row['生']:>5} {row['克']:>5} | {total:>5}")
    totals = {g: sum(table[att][g] for att in table) for g in GROUP_NAMES}
    print(f"  {'Total':>8} | {totals['比和']:>5} {totals['生']:>5} {totals['克']:>5} | {sum(totals.values()):>5}")

    print(f"\n  Chi-square: {chi2:.4f}, p-value: {p_value:.6f}, dof: {dof}")
    print(f"  Expected under independence:")
    for i, att in enumerate(sorted(table.keys())):
        print(f"    {att}: {expected[i]}")

    # ── A6: 五行 type along trajectories ───────────────────────────
    print("\n── A6. 五行 Transition Matrix Under 互 Map ──")
    trans = wuxing_transition_matrix(atlas, hu_map)

    print(f"\n  {'src\\dst':>8} | {'比和':>5} {'生':>5} {'克':>5}")
    print(f"  {'-'*8}-+-{'-'*5}-{'-'*5}-{'-'*5}")
    for src in GROUP_NAMES:
        row = [trans[(src, dst)] for dst in GROUP_NAMES]
        print(f"  {src:>8} | {row[0]:>5} {row[1]:>5} {row[2]:>5}")

    # Specific questions about 生 trajectories
    print(f"\n  生→生 transitions: {trans[('生', '生')]}")
    print(f"  生→比和 transitions: {trans[('生', '比和')]}")
    print(f"  生→克 transitions: {trans[('生', '克')]}")

    # Show trajectories with 五行 type sequences
    print("\n  Example trajectories (first 10 of each type):")
    def vtype(h):
        return RELATION_GROUPS[atlas[str(h)]["surface_relation"]]

    for g in GROUP_NAMES:
        hexes = [h for h in range(64) if vtype(h) == g][:5]
        for h in hexes:
            traj = orbits[h]["trajectory"]
            types = [vtype(t) for t in traj]
            traj_str = " → ".join(f"{t}({tp})" for t, tp in zip(traj, types))
            print(f"    {traj_str}")

    # ── A7: Contraction analysis ───────────────────────────────────
    print("\n── A7. Contraction Analysis ──")
    contraction = contraction_analysis(hu_map)

    print(f"\n  {'Dist':>5} | {'N pairs':>8} | {'Mean ratio':>10} | {'Std':>6} | {'Min':>6} | {'Max':>6}")
    print(f"  {'-'*5}-+-{'-'*8}-+-{'-'*10}-+-{'-'*6}-+-{'-'*6}-+-{'-'*6}")
    for d in range(1, 7):
        r = contraction[d]
        print(f"  {d:>5} | {r['n_pairs']:>8} | {r['mean_ratio']:>10.4f} | {r['std_ratio']:>6.4f} | {r['min_ratio']:>6.3f} | {r['max_ratio']:>6.3f}")

    print("\n  Contraction by 五行 type pair:")
    cont_type = contraction_by_type(atlas, hu_map)
    for pair, r in cont_type.items():
        print(f"    {pair}: mean={r['mean_ratio']:.4f} ± {r['std_ratio']:.4f} (n={r['n_pairs']})")

    # ── A8: Distance to attractor ──────────────────────────────────
    print("\n── A8. Hamming Distance to Attractor by 五行 Type ──")
    dist_summary = distance_to_attractor(atlas, orbits)

    print(f"\n  {'Type':>5} | {'Mean nearest':>13} | {'Mean own':>10}")
    print(f"  {'-'*5}-+-{'-'*13}-+-{'-'*10}")
    for g in GROUP_NAMES:
        s = dist_summary[g]
        print(f"  {g:>5} | {s['mean_nearest']:>13.4f} | {s['mean_own']:>10.4f}")

    print("\n  Distribution of distances to nearest attractor:")
    for g in GROUP_NAMES:
        print(f"    {g}: {dict(sorted(dist_summary[g]['nearest_dist'].items()))}")

    print("\n  Distribution of distances to own attractor:")
    for g in GROUP_NAMES:
        print(f"    {g}: {dict(sorted(dist_summary[g]['own_dist'].items()))}")

    # Attractor affinity: which attractor does each type converge to?
    print("\n  Attractor affinity (which basin each type falls in):")
    att_affinity = distance_to_specific_attractors(atlas, orbits)
    for g in GROUP_NAMES:
        print(f"    {g}: {dict(sorted(att_affinity[g].items()))}")

    # ══════════════════════════════════════════════════════════════
    # PART B: Real-Eigenvalue Null Test
    # ══════════════════════════════════════════════════════════════
    print("\n" + "═" * 70)
    print("PART B: REAL-EIGENVALUE NULL TEST")
    print("═" * 70)

    # ── B1: Random partition test ──────────────────────────────────
    print("\n── B1. Random Partition Test (1000 trials) ──")
    print("  Partitioning 64 vertices into groups of sizes {14, 24, 26}")
    print("  Testing: P_g × A_Q₆ has all real eigenvalues for all 3 groups?")

    n_real, n_trials = real_eigenvalue_null_test(A_q6, n_trials=1000)
    frac = n_real / n_trials
    print(f"\n  Result: {n_real}/{n_trials} trials had all-real eigenvalues = {frac:.1%}")
    if frac > 0.9:
        print("  → Real eigenvalues are GENERIC to the partition structure")
    elif frac < 0.1:
        print("  → Real eigenvalues are SPECIFIC to the 五行 coloring")
    else:
        print(f"  → Intermediate: neither fully generic nor fully specific")

    # ── B2: Alternative 五行 assignments ───────────────────────────
    print("\n── B2. Alternative 五行 Assignments ──")
    print("  Testing all distinct partitions from permuting 5 elements")
    print("  across 3 complement-pair slots + 2 single slots")

    alt_results = alternative_assignments_test(A_q6, atlas)
    n_total = len(alt_results)
    n_real_alt = sum(1 for r in alt_results if r["all_real"])
    print(f"\n  Distinct partitions tested: {n_total}")
    print(f"  All-real eigenvalues: {n_real_alt}/{n_total}")

    for r in alt_results:
        marker = " ← ACTUAL" if r["is_actual"] else ""
        real_str = "✓ real" if r["all_real"] else "✗ complex"
        print(f"    {r['perm']}: sizes={r['sizes']}, {real_str}{marker}")

    # ── Save results ───────────────────────────────────────────────
    json_results = {
        "part_a": {
            "hu_map": hu_map,
            "orbit_structure": {
                str(h): {
                    "trajectory": orbits[h]["trajectory"],
                    "transient_length": orbits[h]["transient_length"],
                    "cycle_length": orbits[h]["cycle_length"],
                    "attractor": orbits[h]["attractor"],
                }
                for h in range(64)
            },
            "max_transient": max_transient,
            "transient_distribution": dict(sorted(transient_dist.items())),
            "image_size": len(image),
            "basins": {str(k): sorted(v) for k, v in basins.items()},
            "basin_sizes": {str(k): len(v) for k, v in basins.items()},
            "bits_23_determine_basin": bits_23_exact,
            "in_degree_distribution": dict(sorted(in_deg_dist.items())),
            "basin_wuxing_table": {str(k): v for k, v in table.items()},
            "basin_wuxing_chi2": chi2,
            "basin_wuxing_pvalue": p_value,
            "wuxing_transition_matrix": {f"{a}→{b}": c for (a, b), c in trans.items()},
            "contraction_by_distance": contraction,
            "contraction_by_type": cont_type,
            "distance_to_attractor": dist_summary,
            "attractor_affinity": {g: dict(sorted(v.items())) for g, v in att_affinity.items()},
        },
        "part_b": {
            "random_partition": {
                "n_real": n_real,
                "n_trials": n_trials,
                "fraction": frac,
            },
            "alternative_assignments": {
                "n_distinct": n_total,
                "n_all_real": n_real_alt,
                "details": alt_results,
            },
        },
    }

    out_path = HERE / "p2_results.json"
    with open(out_path, "w") as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
