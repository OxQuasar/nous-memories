#!/usr/bin/env python3
"""
變 Fan: 384-state single-bit perturbation table.

For each (hex_val, line) pair, computes H' = hex_val ⊕ (1 << (line-1))
and records structural changes between source and destination.

Reads: atlas.json
Writes: transitions.json
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "opposition-theory" / "phase4"))

from cycle_algebra import (
    TRIGRAM_NAMES, TRIGRAM_ELEMENT,
    lower_trigram, upper_trigram, five_phase_relation,
    tiyong_relation, tiyong_trigrams,
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def trig_info(val):
    return {"val": val, "name": TRIGRAM_NAMES[val], "element": TRIGRAM_ELEMENT[val]}


# ─── Build bian fan ──────────────────────────────────────────────────────────

def build_bian_fan(atlas):
    entries = []

    for h in range(64):
        src = atlas[str(h)]
        for line in range(1, 7):
            dst_val = h ^ (1 << (line - 1))
            dst = atlas[str(dst_val)]

            # 體/用
            ti_trig, yong_trig = tiyong_trigrams(h, line)
            ty_rel = tiyong_relation(h, line)

            # Boundary bits
            flips_b2 = (line == 3)
            flips_b3 = (line == 4)

            # 六親 word comparison
            lq_src = src["liuqin_word"]
            lq_dst = dst["liuqin_word"]
            lq_changed = sum(1 for a, b in zip(lq_src, lq_dst) if a != b)

            entries.append({
                "source":           h,
                "line":             line,
                "destination":      dst_val,
                "ti_trigram":       trig_info(ti_trig),
                "yong_trigram":     trig_info(yong_trig),
                "tiyong_relation":  ty_rel,
                "basin_src":        src["basin"],
                "basin_dst":        dst["basin"],
                "basin_crosses":    src["basin"] != dst["basin"],
                "depth_src":        src["depth"],
                "depth_dst":        dst["depth"],
                "depth_delta":      dst["depth"] - src["depth"],
                "palace_src":       src["palace"],
                "palace_dst":       dst["palace"],
                "palace_crosses":   src["palace"] != dst["palace"],
                "surface_cell_src": src["surface_cell"],
                "surface_cell_dst": dst["surface_cell"],
                "surface_relation_src":       src["surface_relation"],
                "surface_relation_dst":       dst["surface_relation"],
                "surface_relation_preserved": src["surface_relation"] == dst["surface_relation"],
                "hu_cell_src":      src["hu_cell"],
                "hu_cell_dst":      dst["hu_cell"],
                "i_component_src":  src["i_component"],
                "i_component_dst":  dst["i_component"],
                "i_component_changes": src["i_component"] != dst["i_component"],
                "flips_b2":         flips_b2,
                "flips_b3":         flips_b3,
                "flips_boundary_bit": flips_b2 or flips_b3,
                "liuqin_word_src":  lq_src,
                "liuqin_word_dst":  lq_dst,
                "liuqin_positions_changed": lq_changed,
            })

    return entries


# ─── Summary ──────────────────────────────────────────────────────────────────

LINE_GROUPS = {"outer": [1, 6], "shell": [2, 5], "boundary": [3, 4]}


def print_summary(fan):
    n = len(fan)
    print(f"Total states: {n}")

    # ── Basin crossing by line ──
    print(f"\nBasin-crossing rate by line:")
    for line in range(1, 7):
        states = [e for e in fan if e["line"] == line]
        crosses = sum(1 for e in states if e["basin_crosses"])
        print(f"  L{line}: {crosses}/{len(states)} = {crosses/len(states):.3f}")

    print(f"\nBasin-crossing by layer:")
    for layer, lines in LINE_GROUPS.items():
        states = [e for e in fan if e["line"] in lines]
        crosses = sum(1 for e in states if e["basin_crosses"])
        print(f"  {layer:10s} (L{','.join(map(str,lines))}): "
              f"{crosses}/{len(states)} = {crosses/len(states):.3f}")

    # ── Surface relation preservation by line ──
    print(f"\nSurface relation preservation rate by line:")
    for line in range(1, 7):
        states = [e for e in fan if e["line"] == line]
        preserved = sum(1 for e in states if e["surface_relation_preserved"])
        print(f"  L{line}: {preserved}/{len(states)} = {preserved/len(states):.3f}")

    # ── i_component change rate by line ──
    print(f"\ni_component change rate by line:")
    for line in range(1, 7):
        states = [e for e in fan if e["line"] == line]
        changes = sum(1 for e in states if e["i_component_changes"])
        print(f"  L{line}: {changes}/{len(states)} = {changes/len(states):.3f}")

    # ── 體/用 relation distribution ──
    ty_dist = Counter(e["tiyong_relation"] for e in fan)
    print(f"\n體/用 relation distribution:")
    for rel, cnt in sorted(ty_dist.items(), key=lambda x: -x[1]):
        print(f"  {rel}: {cnt} ({cnt/n:.3f})")

    # ── Palace crossing by line ──
    print(f"\nPalace-crossing rate by line:")
    for line in range(1, 7):
        states = [e for e in fan if e["line"] == line]
        crosses = sum(1 for e in states if e["palace_crosses"])
        print(f"  L{line}: {crosses}/{len(states)} = {crosses/len(states):.3f}")

    # ── 六親 word disruption by line ──
    print(f"\n六親 word disruption (mean positions changed) by line:")
    for line in range(1, 7):
        states = [e for e in fan if e["line"] == line]
        mean_changed = sum(e["liuqin_positions_changed"] for e in states) / len(states)
        print(f"  L{line}: {mean_changed:.2f}")

    # ── Boundary leakage ──
    boundary = sum(1 for e in fan if e["flips_boundary_bit"])
    print(f"\nBoundary states (flip b2 or b3): {boundary}/{n} = {boundary/n:.3f}")

    # ── Depth delta distribution ──
    dd_dist = Counter(e["depth_delta"] for e in fan)
    print(f"\nDepth delta distribution:")
    for d, cnt in sorted(dd_dist.items()):
        print(f"  {d:+d}: {cnt}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    atlas_path = Path(__file__).parent / "atlas.json"
    with open(atlas_path, encoding='utf-8') as f:
        atlas = json.load(f)

    fan = build_bian_fan(atlas)
    print_summary(fan)

    out_path = Path(__file__).parent / "transitions.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({"bian_fan": fan}, f, ensure_ascii=False, indent=2)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
