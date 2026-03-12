#!/usr/bin/env python3
"""
01_mh_states: Generate all 384 梅花 (hexagram × 動爻) states.

Each state captures the full interpretive coordinates:
  本卦 体/用, 互卦 体互/用互, 變卦 用-side, and the 4-step relation vector.

乾坤无互 exception: hex 0 (坤) and 63 (乾) have self-referential 互.
  Rule: use 互 of the 變卦 instead → 動爻-dependent 互 for these 12 states.

Output: mh_states.json (384 entries)
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "opposition-theory" / "phase4"))
from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    lower_trigram, upper_trigram,
    hugua, biangua, five_phase_relation,
)

HERE = Path(__file__).resolve().parent
ATLAS_DIR = HERE.parent / "atlas"

QIANKUN = {0, 63}  # 坤, 乾 — self-referential 互

# ─── Helpers ────────────────────────────────────────────────────────────────

def ti_yong_side(line):
    """Return (ti_pos, yong_pos) given moving line (1-indexed).
    Moving line in lower (1-3) → 用=lower, 體=upper.
    Moving line in upper (4-6) → 用=upper, 體=lower."""
    if line <= 3:
        return "upper", "lower"
    return "lower", "upper"


def trigram_by_pos(hex_val, pos):
    """Extract trigram value by position name."""
    return upper_trigram(hex_val) if pos == "upper" else lower_trigram(hex_val)


def hu_trigrams(hex_val, line):
    """Return (hu_lower, hu_upper, is_qiankun_exception) for the 互 source.
    For 乾/坤: routes through 變卦."""
    if hex_val in QIANKUN:
        bian = biangua(hex_val, line)
        hu = hugua(bian)
        return lower_trigram(hu), upper_trigram(hu), True
    hu = hugua(hex_val)
    return lower_trigram(hu), upper_trigram(hu), False


# ─── State computation ─────────────────────────────────────────────────────

def compute_state(hex_val, line):
    ti_pos, yong_pos = ti_yong_side(line)

    # 本卦 体/用
    ti_trig = trigram_by_pos(hex_val, ti_pos)
    yong_trig = trigram_by_pos(hex_val, yong_pos)
    ti_elem = TRIGRAM_ELEMENT[ti_trig]
    yong_elem = TRIGRAM_ELEMENT[yong_trig]
    ben_rel = five_phase_relation(ti_elem, yong_elem)

    # 互卦
    hu_lo, hu_up, qk_exc = hu_trigrams(hex_val, line)
    hu_lower_elem = TRIGRAM_ELEMENT[hu_lo]
    hu_upper_elem = TRIGRAM_ELEMENT[hu_up]

    # 互 on 體's side vs 用's side
    ti_hu_trig = hu_up if ti_pos == "upper" else hu_lo
    yong_hu_trig = hu_lo if ti_pos == "upper" else hu_up
    ti_hu_elem = TRIGRAM_ELEMENT[ti_hu_trig]
    yong_hu_elem = TRIGRAM_ELEMENT[yong_hu_trig]
    ti_hu_rel = five_phase_relation(ti_elem, ti_hu_elem)
    yong_hu_rel = five_phase_relation(ti_elem, yong_hu_elem)

    # 變卦
    bian = biangua(hex_val, line)
    bian_yong_trig = trigram_by_pos(bian, yong_pos)
    bian_yong_elem = TRIGRAM_ELEMENT[bian_yong_trig]
    bian_rel = five_phase_relation(ti_elem, bian_yong_elem)

    # 互 source hex (for diagnostics)
    hu_source = biangua(hex_val, line) if hex_val in QIANKUN else hex_val
    hu_hex = hugua(hu_source)

    return {
        "hex_val": hex_val,
        "line": line,
        "ti_pos": ti_pos,
        "ti_trigram": ti_trig,
        "yong_trigram": yong_trig,
        "ti_element": ti_elem,
        "yong_element": yong_elem,
        "ben_relation": ben_rel,
        "hu_hex": hu_hex,
        "hu_lower_trigram": hu_lo,
        "hu_upper_trigram": hu_up,
        "hu_lower_element": hu_lower_elem,
        "hu_upper_element": hu_upper_elem,
        "ti_hu_trigram": ti_hu_trig,
        "yong_hu_trigram": yong_hu_trig,
        "ti_hu_element": ti_hu_elem,
        "yong_hu_element": yong_hu_elem,
        "ti_hu_relation": ti_hu_rel,
        "yong_hu_relation": yong_hu_rel,
        "bian_hex": bian,
        "bian_yong_trigram": bian_yong_trig,
        "bian_yong_element": bian_yong_elem,
        "bian_relation": bian_rel,
        "relation_vector": [ben_rel, ti_hu_rel, yong_hu_rel, bian_rel],
        "qiankun_exception": qk_exc,
    }


def compute_all_states():
    return [compute_state(h, l) for h in range(64) for l in range(1, 7)]


# ─── Validation ─────────────────────────────────────────────────────────────

def validate_against_transitions(states):
    """Cross-check ti/yong trigrams and ben_relation against transitions.json."""
    with open(ATLAS_DIR / "transitions.json") as f:
        trans = json.load(f)

    by_key = {}
    for entry in trans["bian_fan"]:
        by_key[(entry["source"], entry["line"])] = entry

    mismatches = []
    for s in states:
        key = (s["hex_val"], s["line"])
        t = by_key[key]
        if s["ti_trigram"] != t["ti_trigram"]["val"]:
            mismatches.append((key, "ti_trigram", s["ti_trigram"], t["ti_trigram"]["val"]))
        if s["yong_trigram"] != t["yong_trigram"]["val"]:
            mismatches.append((key, "yong_trigram", s["yong_trigram"], t["yong_trigram"]["val"]))
        if s["ben_relation"] != t["tiyong_relation"]:
            mismatches.append((key, "ben_relation", s["ben_relation"], t["tiyong_relation"]))
        if s["bian_hex"] != t["destination"]:
            mismatches.append((key, "bian_hex", s["bian_hex"], t["destination"]))

    return mismatches


def validate_against_atlas(states):
    """Cross-check hu data against atlas.json for non-乾坤 hexagrams."""
    with open(ATLAS_DIR / "atlas.json") as f:
        atlas = json.load(f)

    mismatches = []
    for s in states:
        if s["qiankun_exception"]:
            continue
        a = atlas[str(s["hex_val"])]
        if s["hu_lower_trigram"] != a["hu_lower_trigram"]["val"]:
            mismatches.append((s["hex_val"], "hu_lower", s["hu_lower_trigram"], a["hu_lower_trigram"]["val"]))
        if s["hu_upper_trigram"] != a["hu_upper_trigram"]["val"]:
            mismatches.append((s["hex_val"], "hu_upper", s["hu_upper_trigram"], a["hu_upper_trigram"]["val"]))

    return mismatches


# ─── Summary ────────────────────────────────────────────────────────────────

def print_summary(states):
    print(f"Total states: {len(states)}")

    # Distinct (ti, yong) element pairs
    pairs = set((s["ti_element"], s["yong_element"]) for s in states)
    print(f"Distinct (ti_element, yong_element) pairs: {len(pairs)}")
    for ti, yo in sorted(pairs):
        count = sum(1 for s in states if s["ti_element"] == ti and s["yong_element"] == yo)
        print(f"  {ti:6s} / {yo:6s}: {count}")

    # 乾坤 exception details
    print(f"\n乾坤 exception states: {sum(1 for s in states if s['qiankun_exception'])}")
    for s in states:
        if s["qiankun_exception"]:
            print(f"  hex {s['hex_val']:2d} line {s['line']}: "
                  f"bian={s['bian_hex']:2d}, hu(bian)={s['hu_hex']:2d}, "
                  f"hu_lo={TRIGRAM_NAMES[s['hu_lower_trigram']]}({s['hu_lower_element']}), "
                  f"hu_up={TRIGRAM_NAMES[s['hu_upper_trigram']]}({s['hu_upper_element']})")

    # ben_relation distribution
    print(f"\nben_relation distribution:")
    for rel, cnt in Counter(s["ben_relation"] for s in states).most_common():
        print(f"  {rel}: {cnt}")

    # Relation vector distribution (top 10)
    vec_counts = Counter(tuple(s["relation_vector"]) for s in states)
    print(f"\nRelation vector distribution (top 10 of {len(vec_counts)} distinct):")
    for vec, cnt in vec_counts.most_common(10):
        print(f"  [{', '.join(vec)}]: {cnt}")

    # Per-position relation distribution in the vector
    print(f"\nPer-position distribution in relation_vector:")
    labels = ["ben", "ti_hu", "yong_hu", "bian"]
    for i, label in enumerate(labels):
        dist = Counter(s["relation_vector"][i] for s in states)
        parts = ", ".join(f"{r}: {c}" for r, c in dist.most_common())
        print(f"  {label:7s}: {parts}")


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    states = compute_all_states()

    # Validate
    print("Validating against transitions.json...")
    mm1 = validate_against_transitions(states)
    if mm1:
        print(f"  MISMATCHES: {mm1}")
    else:
        print("  ✓ All ti/yong/ben/bian match")

    print("Validating hu data against atlas.json...")
    mm2 = validate_against_atlas(states)
    if mm2:
        print(f"  MISMATCHES: {mm2}")
    else:
        print("  ✓ All hu trigrams match (non-乾坤)")

    print()
    print_summary(states)

    # Write output
    out_path = HERE / "mh_states.json"
    with open(out_path, "w") as f:
        json.dump(states, f, ensure_ascii=False, indent=2)
    print(f"\nWritten to {out_path}")


if __name__ == "__main__":
    main()
