#!/usr/bin/env python3
"""
Consolidate all Block 1 results into an updated z5z5_cells.json.

Merges data from:
  - z5z5_cells.json (existing)
  - atlas.json (reverse indices)
  - cross_network_results.json (complement, 五行 classes, 六親 collisions)
  - torus_graphs.json (變 neighborhood, 互 graph)
  - valence_torus.json (per-cell valence rates)

Converts cells from list to dict keyed by "(Element,Element)" for O(1) lookup.
Adds global reverse indices by basin, palace, surface_relation.
"""

import json
from pathlib import Path
from collections import defaultdict

DIR = Path(__file__).parent
ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]


def load(name):
    with open(DIR / name) as f:
        return json.load(f)


def cell_key(cell):
    """Canonical key from list/tuple."""
    return f"({cell[0]},{cell[1]})"


def main():
    # ─── Load all sources ────────────────────────────────────────────────
    existing = load("z5z5_cells.json")
    atlas = load("atlas.json")
    cross = load("cross_network_results.json")
    torus = load("torus_graphs.json")
    valence = load("valence_torus.json")

    # ─── Convert existing cells list → dict keyed by cell_key ────────────
    cells = {}
    for c in existing["cells"]:
        key = cell_key(c["cell"])
        cells[key] = c

    # ─── 1. Hex names (readability) ──────────────────────────────────────
    for key, c in cells.items():
        c["hex_names"] = [atlas[str(h)]["kw_name"] for h in c["hexagrams"]]

    # ─── 2. Valence rates ────────────────────────────────────────────────
    for key, c in cells.items():
        v = valence["per_cell"].get(key, {})
        c["valence"] = {
            "auspicious": v.get("auspicious", 0),
            "ausp_rate": v.get("auspicious_rate", 0),
            "inauspicious": v.get("inauspicious", 0),
            "inausp_rate": v.get("inauspicious_rate", 0),
            "no_blame": v.get("no_blame", 0),
            "regret": v.get("regret", 0),
            "difficulty": v.get("difficulty", 0),
            "danger": v.get("danger", 0),
        }

    # ─── 3. 變 neighborhood ──────────────────────────────────────────────
    for key, c in cells.items():
        bn = torus["bian_neighborhood"].get(key, {})
        c["bian_reachable"] = [cell_key(r) for r in bn.get("reachable", [])]
        c["bian_universal"] = [cell_key(r) for r in bn.get("universal", [])]
        c["bian_partial"] = [cell_key(r) for r in bn.get("partial", [])]

    # ─── 4. 互 graph ────────────────────────────────────────────────────
    for key, c in cells.items():
        hg = torus["hu_graph"].get(key, {})
        c["hu_targets"] = hg.get("targets", [])
        c["hu_well_defined"] = hg.get("well_defined", False)

    # ─── 5. Complement cell (already exists, normalize to key) ───────────
    for key, c in cells.items():
        if "complement_cell" in c:
            c["complement_cell"] = cell_key(c["complement_cell"])

    # ─── Build reverse indices ───────────────────────────────────────────
    by_basin = defaultdict(list)
    by_palace = defaultdict(list)
    by_relation = defaultdict(list)

    for h in range(64):
        entry = atlas[str(h)]
        by_basin[entry["basin"]].append(h)
        by_palace[entry["palace"]].append(h)
        by_relation[entry["surface_relation"]].append(h)

    # Sort all lists
    for d in [by_basin, by_palace, by_relation]:
        for k in d:
            d[k].sort()

    # ─── 五行 equivalent pairs (non-singleton only) ─────────────────────
    wuxing_pairs = []
    for profile_key, hex_ids in cross["wuxing_classes_full"].items():
        if len(hex_ids) > 1:
            names = [atlas[str(h)]["kw_name"] for h in hex_ids]
            wuxing_pairs.append({
                "profile": profile_key,
                "hex_ids": hex_ids,
                "hex_names": names,
            })

    # ─── Assemble output ─────────────────────────────────────────────────
    output = {
        "cells": cells,
        "reverse_indices": {
            "by_basin": dict(by_basin),
            "by_palace": dict(by_palace),
            "by_relation": dict(by_relation),
        },
        "liuqin_collisions": cross["liuqin_collisions"],
        "wuxing_equivalent_pairs": wuxing_pairs,
        # Preserve existing top-level data
        "hu_flow": existing.get("hu_flow"),
        "attractor_cells": existing.get("attractor_cells"),
        "convergence": existing.get("convergence"),
        "orbits": existing.get("orbits"),
        "palace_walks": existing.get("palace_walks"),
        "palace_z5_equivalence_classes": existing.get("palace_z5_equivalence_classes"),
        "complement_anti_automorphism": cross["complement_pi"],
        "complement_pi_errors": cross["complement_pi_errors"],
        "valence_summary": {
            "core_bridge": valence["core_bridge"],
            "shell_bridge": valence["shell_bridge"],
            "spatial_residual": valence["spatial_residual"],
        },
    }

    # Remove None values from preserved keys
    output = {k: v for k, v in output.items() if v is not None}

    # ─── Verification ────────────────────────────────────────────────────
    errors = []

    # 1. All hex IDs valid and each appears in exactly one cell
    all_hex_ids = []
    for key, c in cells.items():
        for h in c["hexagrams"]:
            if h < 0 or h > 63:
                errors.append(f"Invalid hex_id {h} in cell {key}")
            all_hex_ids.append(h)

    if len(all_hex_ids) != 64:
        errors.append(f"Total hexagrams in cells: {len(all_hex_ids)}, expected 64")
    if len(set(all_hex_ids)) != 64:
        errors.append(f"Unique hexagrams: {len(set(all_hex_ids))}, expected 64")

    # 2. Population sums to 64
    total_pop = sum(c["population"] for c in cells.values())
    if total_pop != 64:
        errors.append(f"Population sum: {total_pop}, expected 64")

    # 3. Basin indices partition all 64
    basin_all = []
    for ids in by_basin.values():
        basin_all.extend(ids)
    if sorted(basin_all) != list(range(64)):
        errors.append("Basin indices don't partition 0–63")

    # 4. Palace indices partition all 64
    palace_all = []
    for ids in by_palace.values():
        palace_all.extend(ids)
    if sorted(palace_all) != list(range(64)):
        errors.append("Palace indices don't partition 0–63")

    # 5. Relation indices partition all 64
    rel_all = []
    for ids in by_relation.values():
        rel_all.extend(ids)
    if sorted(rel_all) != list(range(64)):
        errors.append("Relation indices don't partition 0–63")

    # 6. Every cell has valence data
    for key, c in cells.items():
        if "valence" not in c:
            errors.append(f"Missing valence for cell {key}")

    # 7. 變 neighborhood present for all cells
    for key, c in cells.items():
        if "bian_reachable" not in c:
            errors.append(f"Missing bian_reachable for cell {key}")

    # 8. Hex names match population
    for key, c in cells.items():
        if len(c["hex_names"]) != c["population"]:
            errors.append(f"hex_names length mismatch in cell {key}")

    # Print verification
    print(f"{'═' * 60}")
    print("VERIFICATION SUMMARY")
    print(f"{'═' * 60}")
    print(f"Cells: {len(cells)}")
    print(f"Total hexagrams: {len(all_hex_ids)} (unique: {len(set(all_hex_ids))})")
    print(f"Population sum: {total_pop}")
    print(f"Basins: {list(by_basin.keys())} → {[len(v) for v in by_basin.values()]} = {sum(len(v) for v in by_basin.values())}")
    print(f"Palaces: {len(by_palace)} palaces → {sum(len(v) for v in by_palace.values())}")
    print(f"Relations: {list(by_relation.keys())} → {[len(v) for v in by_relation.values()]} = {sum(len(v) for v in by_relation.values())}")
    print(f"六親 collisions: {len(cross['liuqin_collisions'])}")
    print(f"五行 equivalent pairs: {len(wuxing_pairs)}")
    print()

    # Cell-level summary
    print(f"{'Cell':17s} {'Pop':>3} {'Hex IDs':20s} {'Basins':20s} {'凶%':>5} {'吉%':>5} {'變':>3} {'互':>3} {'WD':>3}")
    print("─" * 85)
    for key in [cell_key((a,b)) for a in ELEMENTS for b in ELEMENTS]:
        c = cells[key]
        basins = c["basin_distribution"]
        basin_str = " ".join(f"{b[0]}:{v}" for b,v in sorted(basins.items()))
        v = c["valence"]
        wd = "✓" if c.get("hu_well_defined") else " "
        print(f"{key:17s} {c['population']:3d} {str(c['hexagrams'])[:20]:20s} {basin_str:20s} "
              f"{v['inausp_rate']:4.0%} {v['ausp_rate']:4.0%} {len(c['bian_reachable']):3d} "
              f"{len(c['hu_targets']):3d}  {wd}")

    print()
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("ALL CHECKS PASSED ✓")

    # ─── Write ───────────────────────────────────────────────────────────
    out_path = DIR / "z5z5_cells.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
