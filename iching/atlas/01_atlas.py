#!/usr/bin/env python3
"""
Atlas Builder: assembles the complete per-hexagram profile → atlas.json

Imports from existing infrastructure:
  - cycle_algebra: trigram/element constants, bit ops, hugua, five_phase_relation
  - huozhulin/01_najia_map: najia, BRANCH_ELEMENT, BRANCHES, STEMS
  - huozhulin/02_palace_kernel: generate_palaces, basin, depth, ATTRACTORS, SHI_BY_RANK
  - huozhulin/03_liuqin: liuqin_word, liuqin, LIUQIN_NAMES
  - kingwen/sequence: KING_WEN
"""

import json
import sys
from pathlib import Path
from collections import Counter

# ─── Path setup ──────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ROOT / "kingwen"))

from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENTS,
    SHENG_MAP, KE_MAP,
    lower_trigram, upper_trigram, hugua, five_phase_relation,
    fmt6, bit, reverse6,
)

import importlib.util

def _load(name, filepath):
    s = importlib.util.spec_from_file_location(name, filepath)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

p1 = _load('p1', ROOT / 'huozhulin' / '01_najia_map.py')
p2 = _load('p2', ROOT / 'huozhulin' / '02_palace_kernel.py')
p3 = _load('p3', ROOT / 'huozhulin' / '03_liuqin.py')

from sequence import KING_WEN

najia         = p1.najia
BRANCH_ELEMENT = p1.BRANCH_ELEMENT
BRANCHES      = p1.BRANCHES
STEMS         = p1.STEMS

generate_palaces = p2.generate_palaces
basin         = p2.basin
depth         = p2.depth
ATTRACTORS    = p2.ATTRACTORS
SHI_BY_RANK   = p2.SHI_BY_RANK

liuqin_word   = p3.liuqin_word
liuqin        = p3.liuqin
LIUQIN_NAMES  = p3.LIUQIN_NAMES


# ─── King Wen lookup ─────────────────────────────────────────────────────────

def _build_kw_lookup():
    """Map hex_val → (kw_number, kw_name)."""
    lookup = {}
    for kw_num, name, binary_str in KING_WEN:
        val = sum(int(binary_str[i]) << i for i in range(6))
        lookup[val] = (kw_num, name)
    return lookup

KW_LOOKUP = _build_kw_lookup()


# ─── 納音 ────────────────────────────────────────────────────────────────────

NAYIN_TABLE = [
    ("Metal", "海中金"), ("Fire",  "爐中火"), ("Wood",  "大林木"), ("Earth", "路傍土"),
    ("Metal", "劍鋒金"), ("Fire",  "山頭火"), ("Water", "澗下水"), ("Earth", "城頭土"),
    ("Metal", "白蠟金"), ("Wood",  "楊柳木"), ("Water", "泉中水"), ("Earth", "屋上土"),
    ("Fire",  "霹靂火"), ("Wood",  "松柏木"), ("Water", "長流水"), ("Metal", "沙中金"),
    ("Fire",  "山下火"), ("Wood",  "平地木"), ("Earth", "壁上土"), ("Metal", "金箔金"),
    ("Fire",  "覆燈火"), ("Water", "天河水"), ("Earth", "大驛土"), ("Metal", "釵釧金"),
    ("Wood",  "桑柘木"), ("Water", "大溪水"), ("Earth", "沙中土"), ("Fire",  "天上火"),
    ("Wood",  "石榴木"), ("Water", "大海水"),
]

# Build the 60 甲子 cycle
JIAZI_CYCLE = [(STEMS[i % 10], BRANCHES[i % 12]) for i in range(60)]
JIAZI_INDEX = {pair: i for i, pair in enumerate(JIAZI_CYCLE)}


def nayin(stem, branch):
    """Return (element, name) for a 干支 pair via the 納音 table."""
    idx = JIAZI_INDEX.get((stem, branch))
    if idx is None:
        return None  # invalid pair (stem/branch parity mismatch)
    return NAYIN_TABLE[idx // 2]


# ─── 互 depth / attractor ────────────────────────────────────────────────────

def hu_chain(h):
    """Iterate 互 until fixed point or 2-cycle. Return (depth, attractor)."""
    seen = [h]
    for step in range(1, 20):
        nxt = hugua(seen[-1])
        if nxt == seen[-1]:
            return step - 1 if h != nxt else 0, nxt  # fixed point
        if len(seen) >= 2 and nxt == seen[-2]:
            # 2-cycle: attractor is the pair
            return step - 2, seen[-2]  # depth to first entry into cycle
        seen.append(nxt)
    raise RuntimeError(f"No convergence for {h}")


# ─── i_component ──────────────────────────────────────────────────────────────

def i_component(h):
    """Inner parity: bit(h,2) ^ bit(h,3). Separates fixed-point (0) from cycle (1)."""
    return bit(h, 2) ^ bit(h, 3)


# ─── Trigram info helper ──────────────────────────────────────────────────────

def trig_info(val):
    return {"val": val, "name": TRIGRAM_NAMES[val], "element": TRIGRAM_ELEMENT[val]}


# ─── Surface relation ────────────────────────────────────────────────────────

def surface_relation(h):
    """Five-phase relation between lower (体) and upper (用) trigram elements."""
    lo_e = TRIGRAM_ELEMENT[lower_trigram(h)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(h)]
    return five_phase_relation(lo_e, up_e)


# ─── Build atlas ─────────────────────────────────────────────────────────────

def build_atlas():
    _, hex_info = generate_palaces()

    atlas = {}
    for h in range(NUM_HEX):
        info = hex_info[h]
        kw_num, kw_name = KW_LOOKUP[h]

        lo = lower_trigram(h)
        up = upper_trigram(h)

        # 互卦
        hu = hugua(h)
        hu_lo = lower_trigram(hu)
        hu_up = upper_trigram(hu)
        hu_lo_e = TRIGRAM_ELEMENT[hu_lo]
        hu_up_e = TRIGRAM_ELEMENT[hu_up]
        hu_rel = five_phase_relation(hu_lo_e, hu_up_e)

        # 互 depth / attractor
        hd, ha = hu_chain(h)

        # 納甲
        nj = najia(h)
        najia_list = [
            {"stem": s, "branch": b, "branch_element": BRANCH_ELEMENT[b]}
            for s, b in nj
        ]

        # 納音
        nayin_list = []
        for s, b in nj:
            ny = nayin(s, b)
            if ny:
                nayin_list.append({"element": ny[0], "name": ny[1]})
            else:
                nayin_list.append(None)

        # 六親
        pe = info['palace_elem']
        lq_word = liuqin_word(h, pe)
        lq_present = sorted(set(lq_word))
        lq_missing = sorted(set(LIUQIN_NAMES) - set(lq_word))

        # complement / reverse / rev_comp
        comp = h ^ MASK_ALL
        rev = reverse6(h)
        rev_comp = reverse6(comp)

        # 世 / 應
        shi = SHI_BY_RANK[info['rank']]
        ying = shi + 3
        if ying > 6:
            ying -= 6

        entry = {
            "hex_val":         h,
            "binary":          fmt6(h),
            "kw_number":       kw_num,
            "kw_name":         kw_name,
            "lower_trigram":   trig_info(lo),
            "upper_trigram":   trig_info(up),
            "surface_relation": surface_relation(h),
            "surface_cell":    [TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up]],
            "hu_hex":          hu,
            "hu_lower_trigram": trig_info(hu_lo),
            "hu_upper_trigram": trig_info(hu_up),
            "hu_relation":     hu_rel,
            "hu_cell":         [hu_lo_e, hu_up_e],
            "hu_depth":        hd,
            "hu_attractor":    ha,
            "palace":          info['palace'],
            "palace_element":  pe,
            "rank":            info['rank'],
            "rank_name":       info['rank_name'],
            "shi":             shi,
            "ying":            ying,
            "basin":           info['basin'],
            "depth":           info['depth'],
            "inner_val":       p2.inner_val(h),
            "i_component":     i_component(h),
            "najia":           najia_list,
            "liuqin_word":     list(lq_word),
            "liuqin_present":  lq_present,
            "liuqin_missing":  lq_missing,
            "nayin":           nayin_list,
            "complement":      comp,
            "reverse":         rev,
            "rev_comp":        rev_comp,
        }
        atlas[str(h)] = entry

    return atlas


# ─── Summary statistics ──────────────────────────────────────────────────────

def print_summary(atlas):
    entries = list(atlas.values())
    n = len(entries)
    print(f"Total hexagrams: {n}")

    # Basin distribution
    basin_dist = Counter(e["basin"] for e in entries)
    print(f"\nBasin distribution:")
    for b, c in sorted(basin_dist.items()):
        print(f"  {b}: {c}")

    # Surface relation distribution
    rel_dist = Counter(e["surface_relation"] for e in entries)
    print(f"\nSurface relation distribution:")
    for r, c in sorted(rel_dist.items(), key=lambda x: -x[1]):
        print(f"  {r}: {c}")

    # 六親 unique words
    unique_words = set(tuple(e["liuqin_word"]) for e in entries)
    print(f"\n六親 unique words: {len(unique_words)}")

    # Missing type distribution
    missing_count_dist = Counter(len(e["liuqin_missing"]) for e in entries)
    print(f"\nMissing type count distribution:")
    for mc, cnt in sorted(missing_count_dist.items()):
        print(f"  {mc} missing: {cnt} hexagrams")

    # Which types are most commonly missing
    type_missing = Counter()
    for e in entries:
        for m in e["liuqin_missing"]:
            type_missing[m] += 1
    print(f"\nType missing frequency:")
    for t, c in sorted(type_missing.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    # Complement verification
    errors = 0
    for e in entries:
        h = e["hex_val"]
        c = e["complement"]
        if h ^ c != MASK_ALL:
            print(f"  ERROR: {h} ^ {c} != {MASK_ALL}")
            errors += 1
    print(f"\nComplement pairs: {n // 2} pairs, {errors} errors")

    # 互 attractor distribution
    att_dist = Counter(e["hu_attractor"] for e in entries)
    print(f"\n互 attractor distribution:")
    for a, c in sorted(att_dist.items()):
        print(f"  {fmt6(a)} ({KW_LOOKUP[a][1]}): {c} hexagrams")

    # 互 depth distribution
    hd_dist = Counter(e["hu_depth"] for e in entries)
    print(f"\n互 depth distribution:")
    for d, c in sorted(hd_dist.items()):
        print(f"  depth {d}: {c}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    atlas = build_atlas()
    print_summary(atlas)

    out_path = Path(__file__).parent / "atlas.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(atlas, f, ensure_ascii=False, indent=2)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
