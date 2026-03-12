#!/usr/bin/env python3
"""
§I Static Profiles: Consolidate probes 01–04 + 納音 + 卦身 into atlas JSON.

Produces hzl_profiles.json with 64 entries — one per hexagram — containing:
  Palace, rank, 世/應, 納甲, 六親, 飛伏, 納音, 卦身, liuqin census.

Imports existing probe infrastructure; adds 納音 and 卦身 computations.
"""

import sys
import json
from pathlib import Path
from collections import Counter
import importlib.util

# ─── Imports from existing probes ──────────────────────────────────────────

def _load(name, filepath):
    s = importlib.util.spec_from_file_location(name, filepath)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

HERE = Path(__file__).resolve().parent
HZL = HERE.parent / "huozhulin"
PHASE4 = HERE.parent / "opposition-theory" / "phase4"

sys.path.insert(0, str(PHASE4))
from cycle_algebra import NUM_HEX, lower_trigram, upper_trigram, bit, fmt6

p1 = _load("p1", HZL / "01_najia_map.py")
p2 = _load("p2", HZL / "02_palace_kernel.py")
p3 = _load("p3", HZL / "03_liuqin.py")

najia        = p1.najia
STEMS        = p1.STEMS
BRANCHES     = p1.BRANCHES
BRANCH_ELEMENT = p1.BRANCH_ELEMENT
STEM_ELEMENT = p1.STEM_ELEMENT

generate_palaces = p2.generate_palaces
SHI_BY_RANK  = p2.SHI_BY_RANK
RANK_NAMES   = p2.RANK_NAMES

liuqin       = p3.liuqin
liuqin_word  = p3.liuqin_word
LIUQIN_NAMES = p3.LIUQIN_NAMES

# ─── 納音 (Nayin) ─────────────────────────────────────────────────────────

# 30 pairs of the 60 甲子 cycle, each sharing one 納音.
# Index = jiazi_ordinal // 2.
NAYIN_TABLE = [
    ("海中金", "Metal"),  ("爐中火", "Fire"),   ("大林木", "Wood"),
    ("路旁土", "Earth"),  ("劍鋒金", "Metal"),  ("山頭火", "Fire"),
    ("澗下水", "Water"),  ("城頭土", "Earth"),  ("白蠟金", "Metal"),
    ("楊柳木", "Wood"),   ("泉中水", "Water"),  ("屋上土", "Earth"),
    ("霹靂火", "Fire"),   ("松柏木", "Wood"),   ("長流水", "Water"),
    ("沙中金", "Metal"),  ("山下火", "Fire"),   ("平地木", "Wood"),
    ("壁上土", "Earth"),  ("金箔金", "Metal"),  ("覆燈火", "Fire"),
    ("天河水", "Water"),  ("大驛土", "Earth"),  ("釵釧金", "Metal"),
    ("桑柘木", "Wood"),   ("大溪水", "Water"),  ("沙中土", "Earth"),
    ("天上火", "Fire"),   ("石榴木", "Wood"),   ("大海水", "Water"),
]


def jiazi_ordinal(stem_idx, branch_idx):
    """Position in the 60 甲子 cycle from stem and branch indices.

    Uses CRT: k ≡ stem_idx (mod 10), k ≡ branch_idx (mod 12).
    Requires same parity (always true in valid stem-branch pairs).
    """
    t = (-(branch_idx - stem_idx) // 2) % 6
    return (stem_idx + 10 * t) % 60


def nayin(stem, branch):
    """Return (name, element) for a stem-branch pair's 納音."""
    si = STEMS.index(stem)
    bi = BRANCHES.index(branch)
    pair_idx = jiazi_ordinal(si, bi) // 2
    name, elem = NAYIN_TABLE[pair_idx]
    return name, elem


# ─── 卦身 (Guashen) ───────────────────────────────────────────────────────

# 「陽世則從子月起，陰世還當午月生」
# Yang 世: count from 子 (idx 0) forward by (shi - 1)
# Yin 世:  count from 午 (idx 6) forward by (shi - 1)

def guashen(hex_val, shi_line):
    """Compute 卦身 branch from the 世 line's yin/yang and position.

    Returns: (branch_char, element, line_number_or_None)
    """
    shi_bit = bit(hex_val, shi_line - 1)  # 0 = yin, 1 = yang
    start = 0 if shi_bit == 1 else 6
    gs_idx = (start + shi_line - 1) % 12
    gs_branch = BRANCHES[gs_idx]
    gs_element = BRANCH_ELEMENT[gs_branch]

    # Find which line (if any) has this branch
    nj = najia(hex_val)
    gs_line = None
    for i, (_, b) in enumerate(nj):
        if b == gs_branch:
            gs_line = i + 1
            break

    return gs_branch, gs_element, gs_line


# ─── Profile Builder ──────────────────────────────────────────────────────

def build_profiles():
    """Build 64 static profile entries."""
    _, hex_info = generate_palaces()

    # Load hexagram names from existing atlas
    atlas_path = HERE.parent / "atlas" / "atlas.json"
    atlas = json.loads(atlas_path.read_text())

    profiles = []
    for h in range(NUM_HEX):
        info = hex_info[h]
        pe = info["palace_elem"]
        root = info["root"]
        shi = info["shi"]
        ying = info["ying"]

        # 納甲
        nj = najia(h)
        root_nj = najia(root)

        # 六親 words
        vis_word = liuqin_word(h, pe)

        # Build lines
        lines = []
        for pos in range(6):
            stem, branch = nj[pos]
            elem = BRANCH_ELEMENT[branch]
            lq = vis_word[pos]

            # 飛伏: palace root's corresponding line
            ff_stem, ff_branch = root_nj[pos]
            ff_elem = BRANCH_ELEMENT[ff_branch]
            ff_lq = liuqin(ff_elem, pe)

            # 納音
            ny_name, ny_elem = nayin(stem, branch)

            lines.append({
                "position": pos + 1,
                "stem": stem,
                "branch": branch,
                "element": elem,
                "liuqin": lq,
                "feifu_branch": ff_branch,
                "feifu_element": ff_elem,
                "feifu_liuqin": ff_lq,
                "nayin_name": ny_name,
                "nayin_element": ny_elem,
            })

        # 六親 census
        census = Counter(vis_word)
        missing = sorted(set(LIUQIN_NAMES) - set(vis_word))

        # 卦身
        gs_branch, gs_element, gs_line = guashen(h, shi)

        # Name from atlas
        name = atlas[str(h)].get("kw_name", f"hex_{h}")

        profiles.append({
            "hex_val": h,
            "hex_binary": format(h, "06b"),
            "name": name,
            "palace": info["palace"],
            "palace_element": pe,
            "palace_rank": info["rank"],
            "rank_name": info["rank_name"],
            "shi_line": shi,
            "ying_line": ying,
            "guashen_branch": gs_branch,
            "guashen_element": gs_element,
            "guashen_line": gs_line,
            "lines": lines,
            "liuqin_census": dict(census),
            "missing_liuqin": missing,
        })

    return profiles


# ─── Verification ─────────────────────────────────────────────────────────

def verify(profiles):
    """Verify against worked examples from example.md."""
    print("=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    by_val = {p["hex_val"]: p for p in profiles}
    atlas_path = HERE.parent / "atlas" / "atlas.json"
    atlas = json.loads(atlas_path.read_text())
    all_ok = True

    # ── 姤 (0b111110 = 62) ──
    gou = by_val[62]
    print(f"\n  姤 ({gou['hex_binary']}): {gou['palace']} {gou['rank_name']}")
    assert gou["palace"] == "Qian ☰", f"Palace mismatch: {gou['palace']}"
    assert gou["palace_rank"] == 1, f"Rank mismatch: {gou['palace_rank']}"
    assert gou["shi_line"] == 1, f"Shi mismatch: {gou['shi_line']}"

    # Check 六親
    expected_lq = ["父母", "子孫", "兄弟", "官鬼", "兄弟", "父母"]
    actual_lq = [l["liuqin"] for l in gou["lines"]]
    lq_ok = actual_lq == expected_lq
    print(f"  六親: {actual_lq} {'✓' if lq_ok else '✗'}")
    all_ok &= lq_ok

    # Check 納甲
    expected_nj = [("辛", "丑"), ("辛", "亥"), ("辛", "酉"),
                   ("壬", "午"), ("壬", "申"), ("壬", "戌")]
    actual_nj = [(l["stem"], l["branch"]) for l in gou["lines"]]
    nj_ok = actual_nj == expected_nj
    print(f"  納甲: {actual_nj} {'✓' if nj_ok else '✗'}")
    all_ok &= nj_ok

    # Check missing = {妻財}
    miss_ok = gou["missing_liuqin"] == ["妻財"]
    print(f"  Missing: {gou['missing_liuqin']} {'✓' if miss_ok else '✗'}")
    all_ok &= miss_ok

    # Check nayin: 壬申 → 劍鋒金 (line 5)
    l5_ny = gou["lines"][4]  # 0-indexed
    ny_ok = l5_ny["nayin_name"] == "劍鋒金" and l5_ny["nayin_element"] == "Metal"
    print(f"  L5 納音: {l5_ny['nayin_name']} ({l5_ny['nayin_element']}) {'✓' if ny_ok else '✗'}")
    all_ok &= ny_ok

    # Check guashen: 世=L1, L1 is yin → from 午 + 0 = 午 → L4 has 午
    gs_ok = gou["guashen_branch"] == "午" and gou["guashen_line"] == 4
    print(f"  卦身: {gou['guashen_branch']} at L{gou['guashen_line']} {'✓' if gs_ok else '✗'}")
    all_ok &= gs_ok

    # ── Cross-validate nayin against existing atlas ──
    print(f"\n  Cross-validating 納音 against atlas.json...")
    nayin_mismatches = 0
    for h in range(NUM_HEX):
        p = by_val[h]
        a = atlas[str(h)]
        for pos in range(6):
            p_ny = p["lines"][pos]
            a_ny = a["nayin"][pos]
            if p_ny["nayin_name"] != a_ny["name"] or p_ny["nayin_element"] != a_ny["element"]:
                nayin_mismatches += 1
                if nayin_mismatches <= 3:
                    print(f"    MISMATCH hex {h} L{pos+1}: "
                          f"computed={p_ny['nayin_name']}/{p_ny['nayin_element']} "
                          f"atlas={a_ny['name']}/{a_ny['element']}")

    ny_cross_ok = nayin_mismatches == 0
    print(f"  納音 cross-validation: {384 - nayin_mismatches}/384 match "
          f"{'✓' if ny_cross_ok else f'✗ ({nayin_mismatches} mismatches)'}")
    all_ok &= ny_cross_ok

    # ── 遁 (0b111100 = 60) ──
    dun = by_val[60]
    print(f"\n  遁 ({dun['hex_binary']}): {dun['palace']} {dun['rank_name']}")

    # Expected from example.md: 丙辰, 丙午, 丙申, 壬午, 壬申, 壬戌
    expected_dun_nj = [("丙", "辰"), ("丙", "午"), ("丙", "申"),
                       ("壬", "午"), ("壬", "申"), ("壬", "戌")]
    actual_dun_nj = [(l["stem"], l["branch"]) for l in dun["lines"]]
    dun_nj_ok = actual_dun_nj == expected_dun_nj
    print(f"  納甲: {'✓' if dun_nj_ok else '✗'}")
    all_ok &= dun_nj_ok

    # Expected 六親 from example.md
    expected_dun_lq = ["父母", "官鬼", "兄弟", "官鬼", "兄弟", "父母"]
    actual_dun_lq = [l["liuqin"] for l in dun["lines"]]
    dun_lq_ok = actual_dun_lq == expected_dun_lq
    print(f"  六親: {'✓' if dun_lq_ok else '✗'}")
    all_ok &= dun_lq_ok

    # 丙午 納音 = 天河水
    l2_ny = dun["lines"][1]
    dun_ny_ok = l2_ny["nayin_name"] == "天河水"
    print(f"  L2 納音: {l2_ny['nayin_name']} {'✓' if dun_ny_ok else '✗'}")
    all_ok &= dun_ny_ok

    return all_ok


# ─── Summary Statistics ───────────────────────────────────────────────────

def print_summary(profiles):
    """Print summary statistics."""
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    # Palace distribution
    palace_counts = Counter(p["palace"] for p in profiles)
    print(f"\n  Palaces: {len(palace_counts)} (8 × 8 = {sum(palace_counts.values())})")

    # 六親 coverage
    miss_counts = Counter(len(p["missing_liuqin"]) for p in profiles)
    print(f"\n  Missing 六親 distribution:")
    for n in sorted(miss_counts):
        print(f"    {n} missing: {miss_counts[n]} hexagrams")

    # 卦身 distribution
    gs_on_line = sum(1 for p in profiles if p["guashen_line"] is not None)
    gs_not = 64 - gs_on_line
    print(f"\n  卦身 falls on a line: {gs_on_line}/64")
    print(f"  卦身 falls on no line: {gs_not}/64")

    # Which lines host 卦身
    gs_line_dist = Counter(p["guashen_line"] for p in profiles if p["guashen_line"])
    print(f"  卦身 line distribution:")
    for ln in sorted(gs_line_dist):
        print(f"    L{ln}: {gs_line_dist[ln]}")

    # 卦身 element distribution
    gs_elem_dist = Counter(p["guashen_element"] for p in profiles)
    print(f"\n  卦身 element distribution:")
    for elem, cnt in gs_elem_dist.most_common():
        print(f"    {elem}: {cnt}")

    # 卦身 × 世 line relationship
    print(f"\n  卦身 = 世 line's branch?")
    gs_is_shi = sum(1 for p in profiles if p["guashen_line"] == p["shi_line"])
    print(f"    Same line: {gs_is_shi}/64")

    # 納音 element distribution across 384 positions
    ny_elem_dist = Counter()
    for p in profiles:
        for l in p["lines"]:
            ny_elem_dist[l["nayin_element"]] += 1
    print(f"\n  納音 element distribution (384 positions):")
    for elem, cnt in ny_elem_dist.most_common():
        print(f"    {elem}: {cnt}")

    # Distinct 納音 names used
    ny_names = set()
    for p in profiles:
        for l in p["lines"]:
            ny_names.add(l["nayin_name"])
    print(f"\n  Distinct 納音 names: {len(ny_names)}/30")

    # 飛伏 completeness
    ff_complete = 0
    for p in profiles:
        vis_types = set(l["liuqin"] for l in p["lines"])
        hid_types = set(l["feifu_liuqin"] for l in p["lines"])
        if vis_types | hid_types == set(LIUQIN_NAMES):
            ff_complete += 1
    print(f"\n  飛伏 completeness (vis ∪ hid = all 5): {ff_complete}/64")


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    profiles = build_profiles()

    ok = verify(profiles)
    if not ok:
        print("\n*** VERIFICATION FAILED ***")
        return

    print_summary(profiles)

    # Write output
    out_path = HERE / "hzl_profiles.json"
    out_path.write_text(json.dumps(profiles, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote {len(profiles)} profiles to {out_path}")


if __name__ == "__main__":
    main()
