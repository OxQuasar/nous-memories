#!/usr/bin/env python3
"""
Torus graph structures: 變 neighborhood and 互 map on Z₅×Z₅.

1. 變 neighborhood per cell — reachable cells via single-bit flips
2. hu_graph — set-valued 互 map on the torus
3. 互 chain structure — paths to attractors

Outputs: stdout tables + torus_graphs.json
"""

import json
from pathlib import Path
from collections import defaultdict

# ─── Constants ───────────────────────────────────────────────────────────────

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
SINGLETON_ELEMENTS = {"Fire", "Water"}  # 1 trigram each → unique (b1,b2) in lower position
# Well-defined 互 requires: lower ∈ {Fire,Water} AND upper ∉ {Wood}
# Wood is the only element whose 2 trigrams differ in (b3,b4) — the interface bits for 互
UPPER_WELLDEF_ELEMENTS = {"Fire", "Water", "Earth", "Metal"}  # unique (b3,b4)
ALL_CELLS = [(a, b) for a in ELEMENTS for b in ELEMENTS]

SEPARATOR = "─" * 78


def cell_key(cell):
    """Canonical string key for a cell tuple/list."""
    return f"({cell[0]},{cell[1]})"


def load_json(name):
    path = Path(__file__).parent / name
    with open(path) as f:
        return json.load(f)


# ─── 1. 變 neighborhood ─────────────────────────────────────────────────────

def bian_neighborhood(atlas, transitions):
    """For each Z₅×Z₅ cell, compute the set of cells reachable via single-bit flip."""

    # Index: cell → list of hexagrams
    cell_hexagrams = defaultdict(list)
    for k, v in atlas.items():
        cell_hexagrams[tuple(v["surface_cell"])].append(int(k))

    # Index transitions by source hexagram
    bian_by_source = defaultdict(list)
    for t in transitions["bian_fan"]:
        bian_by_source[t["source"]].append(t)

    results = {}

    for cell in ALL_CELLS:
        hexes = sorted(cell_hexagrams.get(cell, []))
        if not hexes:
            continue

        # Per-hexagram reachable cells
        per_hex_targets = {}
        for h in hexes:
            targets = set()
            for t in bian_by_source[h]:
                targets.add(tuple(t["surface_cell_dst"]))
            per_hex_targets[h] = targets

        # Union (reachable from ANY hexagram in cell)
        union = set()
        for targets in per_hex_targets.values():
            union |= targets

        # Intersection (reachable from EVERY hexagram in cell)
        intersection = set.intersection(*per_hex_targets.values()) if per_hex_targets else set()

        # Cells reachable from some but not all
        partial = union - intersection

        results[cell] = {
            "hexagrams": hexes,
            "reachable": sorted(union),
            "universal": sorted(intersection),
            "partial": sorted(partial),
            "per_hexagram": {h: sorted(t) for h, t in per_hex_targets.items()},
        }

    return results


def print_bian_neighborhood(results, atlas):
    print(f"\n{SEPARATOR}")
    print("1. 變 NEIGHBORHOOD PER Z₅×Z₅ CELL")
    print(SEPARATOR)

    # Summary table
    print(f"\n{'Cell':17s} {'Pop':>3} {'Reach':>5} {'Univ':>4} {'Part':>4}  Reachable cells")
    print("─" * 90)

    total_reach = []
    for cell in ALL_CELLS:
        if cell not in results:
            continue
        r = results[cell]
        n_reach = len(r["reachable"])
        n_univ = len(r["universal"])
        n_part = len(r["partial"])
        total_reach.append(n_reach)

        reach_str = ", ".join(cell_key(c) for c in r["reachable"])
        print(f"{cell_key(cell):17s} {len(r['hexagrams']):3d} {n_reach:5d} {n_univ:4d} {n_part:4d}  {reach_str}")

    print(f"\nReachable cells: min={min(total_reach)}, max={max(total_reach)}, "
          f"mean={sum(total_reach)/len(total_reach):.1f}")

    # Detail: cells with within-cell variation (partial > 0)
    varied = [(c, r) for c, r in results.items() if r["partial"]]
    print(f"\nCells with within-cell variation (partial targets): {len(varied)}/25")
    for cell, r in sorted(varied, key=lambda x: -len(x[1]["partial"])):
        print(f"  {cell_key(cell)} (pop={len(r['hexagrams'])}): "
              f"{len(r['partial'])} partial targets")
        for h in r["hexagrams"]:
            name = atlas[str(h)]["kw_name"]
            targets_str = ", ".join(cell_key(c) for c in r["per_hexagram"][h])
            print(f"    {h:2d} {name:12s} → {targets_str}")


# ─── 2. hu_graph ─────────────────────────────────────────────────────────────

def hu_graph(atlas):
    """Set-valued 互 map on Z₅×Z₅ cells."""
    cell_hexagrams = defaultdict(list)
    for k, v in atlas.items():
        cell_hexagrams[tuple(v["surface_cell"])].append(int(k))

    results = {}
    for cell in ALL_CELLS:
        hexes = sorted(cell_hexagrams.get(cell, []))
        if not hexes:
            continue

        hu_targets = set()
        per_hex = {}
        for h in hexes:
            hu_cell = tuple(atlas[str(h)]["hu_cell"])
            hu_targets.add(hu_cell)
            per_hex[h] = hu_cell

        well_defined = len(hu_targets) == 1
        # Predicted: lower singleton AND upper not Wood
        predicted_wd = (cell[0] in SINGLETON_ELEMENTS and cell[1] in UPPER_WELLDEF_ELEMENTS)

        results[cell] = {
            "hexagrams": hexes,
            "targets": sorted(hu_targets),
            "well_defined": well_defined,
            "predicted_well_defined": predicted_wd,
            "per_hexagram": per_hex,
        }

    return results


def print_hu_graph(results, atlas):
    print(f"\n{SEPARATOR}")
    print("2. 互 MAP ON Z₅×Z₅ (HU_GRAPH)")
    print(SEPARATOR)

    # Verify: well-defined iff contains singleton element
    wd_cells = [c for c, r in results.items() if r["well_defined"]]
    pred_cells = [c for c, r in results.items() if r["predicted_well_defined"]]

    print(f"\nWell-defined cells: {len(wd_cells)}")
    print(f"Predicted (lower∈{{Fire,Water}}, upper∉{{Wood}}): {len(pred_cells)}")
    print(f"Match: {'YES' if set(wd_cells) == set(pred_cells) else 'NO'}")
    print(f"  Lower must be Fire/Water: unique (b1,b2) interface bits")
    print(f"  Upper must not be Wood: only element with 2 distinct (b3,b4) values")

    print(f"\n{'Cell':17s} {'Pop':>3} {'#Tgt':>4} {'WD':>3}  Targets")
    print("─" * 78)

    for cell in ALL_CELLS:
        if cell not in results:
            continue
        r = results[cell]
        wd = "✓" if r["well_defined"] else " "
        tgt_str = ", ".join(cell_key(c) for c in r["targets"])
        print(f"{cell_key(cell):17s} {len(r['hexagrams']):3d} {len(r['targets']):4d}   {wd}   {tgt_str}")

    # Multi-target detail
    multi = [(c, r) for c, r in results.items() if not r["well_defined"]]
    print(f"\nMulti-target cells ({len(multi)}):")
    for cell, r in sorted(multi, key=lambda x: -len(x[1]["targets"])):
        print(f"  {cell_key(cell)} → {len(r['targets'])} targets:")
        for h, hu in sorted(r["per_hexagram"].items()):
            name = atlas[str(h)]["kw_name"]
            print(f"    {h:2d} {name:12s} → {cell_key(hu)}")


# ─── 3. 互 chain structure ──────────────────────────────────────────────────

def hu_chains(atlas, hu_results):
    """Follow 互 chains from well-defined cells; document attractor reachability for all."""

    # Build cell → hu_cell map for well-defined cells
    cell_map = {}
    for cell, r in hu_results.items():
        if r["well_defined"]:
            cell_map[cell] = r["targets"][0]

    # Follow chains from well-defined cells
    chains = []
    for start in sorted(cell_map.keys()):
        path = [start]
        current = start
        visited = {start}
        while True:
            nxt = cell_map.get(current)
            if nxt is None:
                # Hit a multi-target cell — chain ends (set-valued)
                path.append(("multi", current))
                break
            if nxt in visited:
                # Cycle/fixed point
                path.append(nxt)
                break
            visited.add(nxt)
            path.append(nxt)
            current = nxt

        chains.append({
            "start": start,
            "path": path,
            "length": len(path) - 1,
        })

    # For multi-target cells: which attractors are reachable?
    # (Follow each hexagram's individual 互 chain)
    multi_reach = {}
    for cell, r in hu_results.items():
        if r["well_defined"]:
            continue
        attractors = set()
        for h in r["hexagrams"]:
            att = atlas[str(h)]["hu_attractor"]
            att_cell = tuple(atlas[str(att)]["surface_cell"])
            attractors.add(att_cell)
        multi_reach[cell] = {
            "reachable_attractors": sorted(attractors),
            "hexagram_attractors": {
                h: tuple(atlas[str(atlas[str(h)]["hu_attractor"])]["surface_cell"])
                for h in r["hexagrams"]
            },
        }

    return chains, multi_reach


def print_hu_chains(chains, multi_reach, atlas, hu_results):
    print(f"\n{SEPARATOR}")
    print("3. 互 CHAIN STRUCTURE")
    print(SEPARATOR)

    print(f"\nChains from well-defined cells ({len(chains)}):")
    for ch in chains:
        path_strs = []
        for step in ch["path"]:
            if isinstance(step, tuple) and step[0] == "multi":
                path_strs.append(f"{cell_key(step[1])}[multi]")
            else:
                path_strs.append(cell_key(step))
        print(f"  {' → '.join(path_strs)}  (len={ch['length']})")

    print(f"\nMulti-target cells → reachable attractors ({len(multi_reach)}):")

    # Identify the 4 attractor cells
    all_att = set()
    for mr in multi_reach.values():
        for a in mr["reachable_attractors"]:
            all_att.add(a)
    for ch in chains:
        last = ch["path"][-1]
        if not (isinstance(last, tuple) and last[0] == "multi"):
            all_att.add(last)

    print(f"  Attractor cells: {sorted(cell_key(a) for a in all_att)}")

    for cell in sorted(multi_reach.keys()):
        mr = multi_reach[cell]
        att_str = ", ".join(cell_key(a) for a in mr["reachable_attractors"])
        print(f"  {cell_key(cell)} → attractors: {att_str}")
        for h, att in sorted(mr["hexagram_attractors"].items()):
            name = atlas[str(h)]["kw_name"]
            print(f"    {h:2d} {name:12s} → {cell_key(att)}")


# ─── Serialize ───────────────────────────────────────────────────────────────

def serialize_results(bian_results, hu_results, chains, multi_reach):
    """Convert tuple keys to strings for JSON serialization."""

    def ser_cell_list(cells):
        return [list(c) if not (isinstance(c, tuple) and c[0] == "multi") else ["multi", list(c[1])]
                for c in cells]

    bian_out = {}
    for cell, r in sorted(bian_results.items()):
        bian_out[cell_key(cell)] = {
            "hexagrams": r["hexagrams"],
            "reachable": [list(c) for c in r["reachable"]],
            "universal": [list(c) for c in r["universal"]],
            "partial": [list(c) for c in r["partial"]],
        }

    hu_out = {}
    for cell, r in sorted(hu_results.items()):
        hu_out[cell_key(cell)] = {
            "hexagrams": r["hexagrams"],
            "targets": [list(c) for c in r["targets"]],
            "well_defined": r["well_defined"],
            "predicted_well_defined": r["predicted_well_defined"],
        }

    chains_out = []
    for ch in chains:
        chains_out.append({
            "start": list(ch["start"]),
            "path": ser_cell_list(ch["path"]),
            "length": ch["length"],
        })

    multi_out = {}
    for cell, mr in sorted(multi_reach.items()):
        multi_out[cell_key(cell)] = {
            "reachable_attractors": [list(a) for a in mr["reachable_attractors"]],
        }

    return {
        "bian_neighborhood": bian_out,
        "hu_graph": hu_out,
        "hu_chains": chains_out,
        "hu_multi_attractors": multi_out,
    }


# ─── Summary ─────────────────────────────────────────────────────────────────

def print_summary(bian_results, hu_results, chains, multi_reach):
    wd = sum(1 for r in hu_results.values() if r["well_defined"])
    reach_counts = [len(r["reachable"]) for r in bian_results.values()]

    match = all(
        r["well_defined"] == r["predicted_well_defined"]
        for r in hu_results.values()
    )

    print(f"\n{'═' * 78}")
    print("SUMMARY")
    print(f"{'═' * 78}")
    print(f"""
變 neighborhood:
  25 cells on Z₅×Z₅, each with 1-4 hexagrams
  Reachable cells per source: {min(reach_counts)}–{max(reach_counts)} (mean {sum(reach_counts)/len(reach_counts):.1f})
  Every cell can reach multiple targets — 變 explores the full torus
  Within-cell variation: {sum(1 for r in bian_results.values() if r['partial'])}/25 cells have partial targets
    (some destinations reachable from some hexagrams but not all in the cell)

互 graph on torus:
  Well-defined (unique target): {wd}/25 cells
  Multi-target: {25 - wd}/25 cells
  Well-defined ↔ lower∈{{Fire,Water}} ∧ upper∉{{Wood}}: {'CONFIRMED' if match else 'MISMATCH'}
    Lower must fix (b1,b2): only Fire(101) and Water(010) have 1 trigram
    Upper must fix (b3,b4): all except Wood — Wood's 2 trigrams give distinct (b3,b4)

互 chains:
  {len(chains)} chains from well-defined cells
  {len(multi_reach)} multi-target cells with mixed attractor reachability
""")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    atlas = load_json("atlas.json")
    transitions = load_json("transitions.json")

    bian_res = bian_neighborhood(atlas, transitions)
    hu_res = hu_graph(atlas)
    ch, multi = hu_chains(atlas, hu_res)

    print_bian_neighborhood(bian_res, atlas)
    print_hu_graph(hu_res, atlas)
    print_hu_chains(ch, multi, atlas, hu_res)
    print_summary(bian_res, hu_res, ch, multi)

    # Save
    out = serialize_results(bian_res, hu_res, ch, multi)
    out_path = Path(__file__).parent / "torus_graphs.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
