#!/usr/bin/env python3
"""
Z₅×Z₅ meta-space analysis: cell profiles, 互 flow, palace walks, pair geometry.

Loads atlas.json. Writes z5z5_cells.json.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from itertools import permutations

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "opposition-theory" / "phase4"))

from cycle_algebra import (
    ELEMENTS, TRIGRAM_ELEMENT, MASK_ALL,
    lower_trigram, upper_trigram, hugua, reverse6,
    kw_partner, is_palindrome6, generate_kw_pairs, fmt6,
)

ELEMENTS_SET = set(ELEMENTS)  # Wood, Fire, Earth, Metal, Water

# Complement permutation: Earth↔Metal, Fire↔Water, Wood↔Wood
COMP_PERM = {"Earth": "Metal", "Metal": "Earth", "Fire": "Water", "Water": "Fire", "Wood": "Wood"}


# ─── Load atlas ──────────────────────────────────────────────────────────────

def load_atlas():
    path = Path(__file__).parent / "atlas.json"
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ─── Part 1: Z₅×Z₅ cells ────────────────────────────────────────────────────

def build_cells(atlas):
    """Build 25-cell profile indexed by (lower_elem, upper_elem)."""
    cells = {}
    for lo_e in ELEMENTS:
        for up_e in ELEMENTS:
            cells[(lo_e, up_e)] = {
                "cell": [lo_e, up_e],
                "population": 0,
                "hexagrams": [],
                "surface_relation": None,
                "basin_distribution": Counter(),
                "depth_distribution": Counter(),
                "hu_cells_reachable": [],
                "palace_distribution": Counter(),
                "hu_attractor_distribution": Counter(),
            }

    for h in range(64):
        e = atlas[str(h)]
        key = tuple(e["surface_cell"])
        c = cells[key]
        c["population"] += 1
        c["hexagrams"].append(h)
        c["surface_relation"] = e["surface_relation"]
        c["basin_distribution"][e["basin"]] += 1
        c["depth_distribution"][e["depth"]] += 1
        c["hu_cells_reachable"].append(tuple(e["hu_cell"]))
        c["palace_distribution"][e["palace"]] += 1
        c["hu_attractor_distribution"][e["hu_attractor"]] += 1

    # Derive fields
    for key, c in cells.items():
        lo_e, up_e = key
        c["is_diagonal"] = (lo_e == up_e)
        c["complement_cell"] = [COMP_PERM[lo_e], COMP_PERM[up_e]]
        c["hu_cells_unique"] = [list(t) for t in sorted(set(c["hu_cells_reachable"]), key=str)]
        # Reverse cells: reverse swaps lower↔upper trigram, so cell (a,b) → (b,a)
        # But only for non-palindromic hexagrams; palindromes reverse to themselves
        rev_cells = []
        for h in c["hexagrams"]:
            r = atlas[str(h)]["reverse"]
            rev_cells.append(tuple(atlas[str(r)]["surface_cell"]))
        c["reverse_cells"] = [list(t) for t in sorted(set(rev_cells), key=str)]

    return cells


def serialize_cells(cells):
    """Convert cells dict to JSON-serializable list."""
    result = []
    for key in sorted(cells.keys(), key=lambda k: (ELEMENTS.index(k[0]), ELEMENTS.index(k[1]))):
        c = cells[key]
        result.append({
            "cell": c["cell"],
            "population": c["population"],
            "hexagrams": c["hexagrams"],
            "surface_relation": c["surface_relation"],
            "basin_distribution": dict(c["basin_distribution"]),
            "depth_distribution": {str(k): v for k, v in sorted(c["depth_distribution"].items())},
            "hu_cells_reachable": [list(x) for x in c["hu_cells_reachable"]],
            "hu_cells_unique": c["hu_cells_unique"],
            "palace_distribution": dict(c["palace_distribution"]),
            "hu_attractor_distribution": {str(k): v for k, v in c["hu_attractor_distribution"].items()},
            "is_diagonal": c["is_diagonal"],
            "complement_cell": c["complement_cell"],
            "reverse_cells": c["reverse_cells"],
        })
    return result


def print_cells(cells):
    print("=" * 70)
    print("PART 1: Z₅×Z₅ CELLS (25 cells)")
    print("=" * 70)

    # Population table
    print(f"\nPopulation table (lower \\ upper):")
    header = f"{'':>8s} " + " ".join(f"{e[:5]:>5s}" for e in ELEMENTS)
    print(header)
    for lo_e in ELEMENTS:
        row = " ".join(f"{cells[(lo_e, up_e)]['population']:>5d}" for up_e in ELEMENTS)
        print(f"{lo_e[:5]:>8s} {row}")

    pop_counts = Counter(c["population"] for c in cells.values())
    print(f"\nPopulation sizes: {dict(sorted(pop_counts.items()))}")

    # Diagonal vs off-diagonal
    diag = [c for c in cells.values() if c["is_diagonal"]]
    off = [c for c in cells.values() if not c["is_diagonal"]]
    print(f"Diagonal (5 cells): total {sum(c['population'] for c in diag)} hexagrams")
    print(f"Off-diagonal (20 cells): total {sum(c['population'] for c in off)} hexagrams")

    # Unique hu_cells per cell
    print(f"\nUnique hu_cells per surface cell:")
    for key in sorted(cells.keys(), key=lambda k: (ELEMENTS.index(k[0]), ELEMENTS.index(k[1]))):
        c = cells[key]
        n_hu = len(c["hu_cells_unique"])
        print(f"  ({key[0][:5]},{key[1][:5]}): {n_hu} hu targets  pop={c['population']}")

    single_target = sum(1 for c in cells.values() if len(c["hu_cells_unique"]) == 1)
    multi_target = 25 - single_target
    print(f"\nSingle-target cells: {single_target}/25, Multi-target: {multi_target}/25")


# ─── Part 2: 互 flow on Z₅×Z₅ ───────────────────────────────────────────────

def compute_hu_flow(cells, atlas):
    """Build the multi-valued 互 flow map on Z₅×Z₅."""
    flow = {}  # cell → Counter of target cells
    for key, c in cells.items():
        targets = Counter(tuple(hc) for hc in c["hu_cells_reachable"])
        flow[key] = targets

    # Attractor cells
    attractor_map = {}  # attractor hex_val → cell
    for att in [0, 63, 21, 42]:  # Kun, Qian, JiJi, WeiJi — known from atlas
        e = atlas[str(att)]
        attractor_map[att] = tuple(e["surface_cell"])

    # Per-cell convergence: attractor distribution
    convergence = {}
    for key, c in cells.items():
        convergence[key] = dict(c["hu_attractor_distribution"])

    # Set-valued orbits: from each cell, what cells are reachable by iterated 互?
    orbits = {}
    for key in cells:
        reachable = set()
        frontier = {key}
        while frontier:
            nxt = set()
            for cell in frontier:
                if cell in reachable:
                    continue
                reachable.add(cell)
                for target in flow.get(cell, {}):
                    if target not in reachable:
                        nxt.add(target)
            frontier = nxt
        orbits[key] = sorted(reachable, key=lambda c: (ELEMENTS.index(c[0]), ELEMENTS.index(c[1])))

    return flow, attractor_map, convergence, orbits


def print_hu_flow(flow, attractor_map, convergence, orbits):
    print("\n" + "=" * 70)
    print("PART 2: 互 FLOW ON Z₅×Z₅")
    print("=" * 70)

    print("\nAttractor cells:")
    for att, cell in sorted(attractor_map.items()):
        print(f"  hex {att} ({fmt6(att)}): cell {cell}")

    print(f"\n互 flow (multi-valued map):")
    for key in sorted(flow.keys(), key=lambda k: (ELEMENTS.index(k[0]), ELEMENTS.index(k[1]))):
        targets = flow[key]
        parts = ", ".join(f"({t[0][:2]},{t[1][:2]})×{n}" for t, n in sorted(targets.items(), key=lambda x: -x[1]))
        print(f"  ({key[0][:5]},{key[1][:5]}) → {parts}")

    # Orbit equivalence classes
    orbit_sets = {}
    for key, orb in orbits.items():
        orb_key = tuple(tuple(c) for c in orb)
        orbit_sets.setdefault(orb_key, []).append(key)

    print(f"\nOrbit equivalence classes ({len(orbit_sets)}):")
    for i, (orb_key, members) in enumerate(sorted(orbit_sets.items(), key=lambda x: -len(x[0]))):
        member_str = ", ".join(f"({m[0][:2]},{m[1][:2]})" for m in sorted(members, key=lambda c: (ELEMENTS.index(c[0]), ELEMENTS.index(c[1]))))
        print(f"  Class {i+1} ({len(orb_key)} cells reachable): {member_str}")


# ─── Part 3: Palace walk trajectories ────────────────────────────────────────

def compute_palace_walks(atlas):
    """Extract element-pair trajectories for each palace."""
    palaces = defaultdict(list)
    for h in range(64):
        e = atlas[str(h)]
        palaces[e["palace"]].append(e)

    walks = {}
    for palace, entries in palaces.items():
        entries.sort(key=lambda x: x["rank"])
        walks[palace] = {
            "palace_element": entries[0]["palace_element"],
            "element_trajectory": [tuple(e["surface_cell"]) for e in entries],
            "relation_trajectory": [e["surface_relation"] for e in entries],
            "basin_trajectory": [e["basin"] for e in entries],
            "depth_trajectory": [e["depth"] for e in entries],
            "liuqin_trajectory": [tuple(e["liuqin_word"]) for e in entries],
        }

    return walks


def test_z5_isomorphism(walks):
    """Test whether palace walks are related by Z₅ permutations (element relabelings)."""
    # Generate all 120 permutations of 5 elements
    elem_perms = list(permutations(ELEMENTS))
    palace_names = sorted(walks.keys())

    # For each pair of palaces, find permutations mapping one trajectory to the other
    equiv_classes = []
    assigned = set()

    for p in palace_names:
        if p in assigned:
            continue
        cls = [p]
        assigned.add(p)
        traj_p = walks[p]["element_trajectory"]  # list of (lo_e, up_e) tuples

        for q in palace_names:
            if q in assigned:
                continue
            traj_q = walks[q]["element_trajectory"]
            # Find permutation σ such that σ(traj_p) = traj_q
            for perm in elem_perms:
                sigma = dict(zip(ELEMENTS, perm))
                mapped = [(sigma[lo], sigma[up]) for lo, up in traj_p]
                if mapped == traj_q:
                    cls.append(q)
                    assigned.add(q)
                    break

        equiv_classes.append(cls)

    return equiv_classes


def print_palace_walks(walks, equiv_classes):
    print("\n" + "=" * 70)
    print("PART 3: PALACE WALK TRAJECTORIES")
    print("=" * 70)

    for palace in sorted(walks.keys()):
        w = walks[palace]
        elem_traj = [f"({lo[:2]},{up[:2]})" for lo, up in w["element_trajectory"]]
        rel_traj = w["relation_trajectory"]
        basin_traj = w["basin_trajectory"]
        depth_traj = w["depth_trajectory"]
        print(f"\n  {palace} ({w['palace_element']}):")
        print(f"    Element:  {' → '.join(elem_traj)}")
        print(f"    Relation: {' → '.join(rel_traj)}")
        print(f"    Basin:    {' → '.join(basin_traj)}")
        print(f"    Depth:    {' → '.join(map(str, depth_traj))}")

    print(f"\nZ₅ isomorphism test:")
    print(f"  Equivalence classes: {len(equiv_classes)}")
    for i, cls in enumerate(equiv_classes):
        print(f"  Class {i+1}: {cls}")

    if len(equiv_classes) == 1:
        print("  → All 8 palaces are isomorphic under Z₅ rotation!")
    else:
        print(f"  → {len(equiv_classes)} distinct walk patterns under Z₅.")

    # Check: is the relation trajectory the same for all palaces?
    # (Since surface_relation depends only on the element pair, isomorphic walks
    #  imply isomorphic relation trajectories iff the permutation preserves 生克)
    rel_trajectories = set()
    for w in walks.values():
        rel_trajectories.add(tuple(w["relation_trajectory"]))
    print(f"\n  Distinct relation trajectories: {len(rel_trajectories)}")
    for rt in sorted(rel_trajectories):
        palaces_with = [p for p, w in walks.items() if tuple(w["relation_trajectory"]) == rt]
        print(f"    {list(rt)}: {palaces_with}")

    # Basin trajectory
    basin_trajectories = set()
    for w in walks.values():
        basin_trajectories.add(tuple(w["basin_trajectory"]))
    print(f"\n  Distinct basin trajectories: {len(basin_trajectories)}")
    for bt in sorted(basin_trajectories):
        palaces_with = [p for p, w in walks.items() if tuple(w["basin_trajectory"]) == bt]
        print(f"    {list(bt)}: {palaces_with}")


# ─── Part 4: Complement/reverse pairs on Z₅×Z₅ ─────────────────────────────

def compute_pair_geometry(atlas):
    """Analyze complement and KW pairs in Z₅×Z₅."""
    # Complement pairs
    comp_pairs = []
    seen = set()
    for h in range(64):
        c = atlas[str(h)]["complement"]
        if h in seen or c in seen:
            continue
        seen.add(h); seen.add(c)
        cell_h = tuple(atlas[str(h)]["surface_cell"])
        cell_c = tuple(atlas[str(c)]["surface_cell"])
        comp_pairs.append({
            "hex_a": h, "hex_b": c,
            "cell_a": list(cell_h), "cell_b": list(cell_c),
            "same_cell": cell_h == cell_c,
        })

    # Verify anti-automorphism
    comp_anti_ok = True
    for pair in comp_pairs:
        ca, cb = tuple(pair["cell_a"]), tuple(pair["cell_b"])
        expected = (COMP_PERM[ca[0]], COMP_PERM[ca[1]])
        if cb != expected:
            comp_anti_ok = False
            print(f"  ANTI-AUTOMORPHISM FAIL: {ca} → {cb}, expected {expected}")

    # KW pairs (reversal or complement for palindromes)
    kw_pairs_data = []
    for a, b, ptype in generate_kw_pairs():
        cell_a = tuple(atlas[str(a)]["surface_cell"])
        cell_b = tuple(atlas[str(b)]["surface_cell"])
        kw_pairs_data.append({
            "hex_a": a, "hex_b": b, "pair_type": ptype,
            "cell_a": list(cell_a), "cell_b": list(cell_b),
            "same_cell": cell_a == cell_b,
        })

    # Reverse pattern: for non-palindromes, reverse swaps lower↔upper → (a,b) → (b,a)
    # For palindromes, reverse = self, so partner is complement → (a,b) → (π(a),π(b))
    rev_swap_count = 0
    for pair in kw_pairs_data:
        ca, cb = tuple(pair["cell_a"]), tuple(pair["cell_b"])
        if pair["pair_type"] == "reversal":
            # Expect cb = (ca[1], ca[0])
            if cb == (ca[1], ca[0]):
                rev_swap_count += 1

    return comp_pairs, comp_anti_ok, kw_pairs_data, rev_swap_count


def print_pair_geometry(comp_pairs, comp_anti_ok, kw_pairs, rev_swap_count):
    print("\n" + "=" * 70)
    print("PART 4: COMPLEMENT / REVERSE PAIRS ON Z₅×Z₅")
    print("=" * 70)

    # Complement
    comp_same = sum(1 for p in comp_pairs if p["same_cell"])
    print(f"\nComplement pairs: {len(comp_pairs)}")
    print(f"  Same cell: {comp_same}, Different cell: {len(comp_pairs) - comp_same}")
    print(f"  Anti-automorphism π(Earth↔Metal, Fire↔Water, Wood↔Wood): {'VERIFIED ✓' if comp_anti_ok else 'FAILED ✗'}")

    # Show cell pairings
    comp_cell_pairs = Counter()
    for p in comp_pairs:
        k = (tuple(p["cell_a"]), tuple(p["cell_b"]))
        comp_cell_pairs[k] += 1
    print(f"\n  Complement cell pairings ({len(comp_cell_pairs)} distinct):")
    for (ca, cb), cnt in sorted(comp_cell_pairs.items(), key=lambda x: -x[1]):
        print(f"    ({ca[0][:2]},{ca[1][:2]}) ↔ ({cb[0][:2]},{cb[1][:2]}): {cnt} pairs")

    # KW pairs
    kw_same = sum(1 for p in kw_pairs if p["same_cell"])
    n_rev = sum(1 for p in kw_pairs if p["pair_type"] == "reversal")
    n_pal = sum(1 for p in kw_pairs if p["pair_type"] == "palindromic")
    print(f"\nKW pairs: {len(kw_pairs)} ({n_rev} reversal, {n_pal} palindromic)")
    print(f"  Same cell: {kw_same}, Different cell: {len(kw_pairs) - kw_same}")

    # Reversal pattern
    print(f"\n  Reversal pairs where cell (a,b) → (b,a): {rev_swap_count}/{n_rev}")
    if rev_swap_count == n_rev:
        print("  → ALL reversal pairs swap lower↔upper element. ✓")

    # Palindromic pairs: partner is complement, so follows π
    pal_pairs = [p for p in kw_pairs if p["pair_type"] == "palindromic"]
    pal_anti_ok = all(
        tuple(p["cell_b"]) == (COMP_PERM[p["cell_a"][0]], COMP_PERM[p["cell_a"][1]])
        for p in pal_pairs
    )
    print(f"  Palindromic pairs follow complement π: {'YES ✓' if pal_anti_ok else 'NO ✗'}")

    # KW cell pairings
    kw_cell_pairs = Counter()
    for p in kw_pairs:
        ca, cb = tuple(p["cell_a"]), tuple(p["cell_b"])
        k = (min(ca, cb), max(ca, cb))
        kw_cell_pairs[k] += 1
    print(f"\n  KW cell pairings ({len(kw_cell_pairs)} distinct):")
    for (ca, cb), cnt in sorted(kw_cell_pairs.items(), key=lambda x: -x[1]):
        print(f"    ({ca[0][:2]},{ca[1][:2]}) ↔ ({cb[0][:2]},{cb[1][:2]}): {cnt} pairs")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    atlas = load_atlas()

    # Part 1
    cells = build_cells(atlas)
    print_cells(cells)

    # Part 2
    flow, attractor_map, convergence, orbits = compute_hu_flow(cells, atlas)
    print_hu_flow(flow, attractor_map, convergence, orbits)

    # Part 3
    walks = compute_palace_walks(atlas)
    equiv_classes = test_z5_isomorphism(walks)
    print_palace_walks(walks, equiv_classes)

    # Part 4
    comp_pairs, comp_anti_ok, kw_pairs, rev_swap_count = compute_pair_geometry(atlas)
    print_pair_geometry(comp_pairs, comp_anti_ok, kw_pairs, rev_swap_count)

    # ── Write JSON ──
    # Serialize flow
    flow_serial = {}
    for key, targets in flow.items():
        flow_serial[f"{key[0]},{key[1]}"] = {f"{t[0]},{t[1]}": n for t, n in targets.items()}

    orbits_serial = {f"{k[0]},{k[1]}": [list(c) for c in v] for k, v in orbits.items()}

    walks_serial = {}
    for palace, w in walks.items():
        walks_serial[palace] = {
            "palace_element": w["palace_element"],
            "element_trajectory": [list(t) for t in w["element_trajectory"]],
            "relation_trajectory": w["relation_trajectory"],
            "basin_trajectory": w["basin_trajectory"],
            "depth_trajectory": w["depth_trajectory"],
        }

    out = {
        "cells": serialize_cells(cells),
        "hu_flow": flow_serial,
        "attractor_cells": {str(k): list(v) for k, v in attractor_map.items()},
        "convergence": {f"{k[0]},{k[1]}": {str(a): n for a, n in v.items()} for k, v in convergence.items()},
        "orbits": orbits_serial,
        "palace_walks": walks_serial,
        "palace_z5_equivalence_classes": equiv_classes,
        "complement_pairs": comp_pairs,
        "complement_anti_automorphism_verified": comp_anti_ok,
        "kw_pairs": kw_pairs,
        "note_valence": "Valence (吉/凶) data not loaded — requires 爻辭 text extraction pipeline. Gap noted.",
    }

    out_path = Path(__file__).parent / "z5z5_cells.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
