#!/usr/bin/env python3
"""
Probe 1: 納甲 as a map on Z₂⁶

Encodes the 納甲 system algebraically, verifies against worked examples,
and characterizes its structure (factoring, inner-bit blindness, element gap).
"""

import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "opposition-theory" / "phase4"))
from cycle_algebra import (
    NUM_HEX, TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENTS,
    SHENG_MAP, KE_MAP,
    lower_trigram, upper_trigram, fmt6, fmt3, bit,
    five_phase_relation,
)

# ─── 天干 (Heavenly Stems) ──────────────────────────────────────────────────

STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
STEM_ELEMENT = {
    "甲": "Wood", "乙": "Wood", "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth", "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water",
}

# ─── 地支 (Earthly Branches) ────────────────────────────────────────────────

BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_ELEMENT = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood",
    "辰": "Earth", "巳": "Fire",  "午": "Fire",  "未": "Earth",
    "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}

# Yang ascending: skip-one cycle through even branches
YANG_SEQ = [0, 2, 4, 6, 8, 10]   # 子寅辰午申戌
# Yin descending: skip-one cycle through odd branches (backwards)
YIN_SEQ  = [1, 11, 9, 7, 5, 3]   # 丑亥酉未巳卯

# ─── Trigram 納甲 Tables ────────────────────────────────────────────────────

# Stem: trigram → (lower_stem, upper_stem)
TRIGRAM_STEM = {
    0b111: ("甲", "壬"),  # 乾: splits by position
    0b000: ("乙", "癸"),  # 坤: splits by position
    0b001: ("庚", "庚"),  # 震
    0b110: ("辛", "辛"),  # 巽
    0b010: ("戊", "戊"),  # 坎
    0b101: ("己", "己"),  # 離
    0b100: ("丙", "丙"),  # 艮
    0b011: ("丁", "丁"),  # 兌
}

YANG_TRIGRAMS = {0b111, 0b001, 0b010, 0b100}  # 乾震坎艮
YIN_TRIGRAMS  = {0b000, 0b110, 0b101, 0b011}  # 坤巽離兌

# Branch start: (trigram, is_upper) → index into YANG_SEQ or YIN_SEQ
# 乾/坤 split by position (offset 3); others same for both positions
TRIGRAM_BRANCH_START = {
    (0b111, False): 0, (0b111, True): 3,  # 乾: 子.. / 午..
    (0b000, False): 3, (0b000, True): 0,  # 坤: 未.. / 丑..
    (0b001, False): 0, (0b001, True): 0,  # 震: 子..
    (0b110, False): 0, (0b110, True): 0,  # 巽: 丑..
    (0b010, False): 1, (0b010, True): 1,  # 坎: 寅..
    (0b101, False): 5, (0b101, True): 5,  # 離: 卯..
    (0b100, False): 2, (0b100, True): 2,  # 艮: 辰..
    (0b011, False): 4, (0b011, True): 4,  # 兌: 巳..
}


def najia(hex_val):
    """
    Compute 納甲 for a hexagram.

    Args:
        hex_val: 6-bit int (bit 0 = bottom line, bit 5 = top line)

    Returns:
        List of 6 (stem, branch) tuples, index 0 = bottom line.
    """
    lo = lower_trigram(hex_val)
    up = upper_trigram(hex_val)
    result = []

    for trig, is_upper in [(lo, False), (up, True)]:
        stem = TRIGRAM_STEM[trig][1 if is_upper else 0]
        seq = YANG_SEQ if trig in YANG_TRIGRAMS else YIN_SEQ
        start = TRIGRAM_BRANCH_START[(trig, is_upper)]

        for i in range(3):
            branch = BRANCHES[seq[(start + i) % 6]]
            result.append((stem, branch))

    return result


# ═══════════════════════════════════════════════════════════════════════════
# Verification
# ═══════════════════════════════════════════════════════════════════════════

def verify_examples():
    """Verify against 姤 and 遁 from example.md."""
    print("=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    cases = [
        ("姤 (天風姤)", 0b110 | (0b111 << 3), [
            ("辛", "丑"), ("辛", "亥"), ("辛", "酉"),
            ("壬", "午"), ("壬", "申"), ("壬", "戌"),
        ]),
        ("遁 (天山遁)", 0b100 | (0b111 << 3), [
            ("丙", "辰"), ("丙", "午"), ("丙", "申"),
            ("壬", "午"), ("壬", "申"), ("壬", "戌"),
        ]),
    ]

    all_ok = True
    for name, h, expected in cases:
        result = najia(h)
        ok = result == expected
        all_ok &= ok
        lo, up = lower_trigram(h), upper_trigram(h)
        print(f"\n  {name} = {fmt6(h)} (lo={TRIGRAM_NAMES[lo]}, up={TRIGRAM_NAMES[up]})")
        for i in range(5, -1, -1):
            s, b = result[i]
            es, eb = expected[i]
            mark = "✓" if (s, b) == (es, eb) else "✗"
            print(f"    L{i+1}: {s}{b} {mark}")
        print(f"  Match: {'✓' if ok else '✗ FAIL'}")

    return all_ok


# ═══════════════════════════════════════════════════════════════════════════
# Structural Tests
# ═══════════════════════════════════════════════════════════════════════════

def test_factoring():
    """Confirm 納甲 factors through trigram pair, with independent halves."""
    print("\n" + "=" * 60)
    print("FACTORING TEST")
    print("=" * 60)

    # Each upper/lower trigram's assignment should be invariant to the other half
    upper_by_trig, lower_by_trig = {}, {}
    for h in range(NUM_HEX):
        lo, up = lower_trigram(h), upper_trigram(h)
        nj = najia(h)
        lower_by_trig.setdefault(lo, set()).add(tuple(nj[:3]))
        upper_by_trig.setdefault(up, set()).add(tuple(nj[3:]))

    lo_indep = all(len(v) == 1 for v in lower_by_trig.values())
    up_indep = all(len(v) == 1 for v in upper_by_trig.values())

    print(f"\n  Lower half independent of upper trigram: {'✓' if lo_indep else '✗'}")
    print(f"  Upper half independent of lower trigram: {'✓' if up_indep else '✗'}")
    print(f"  → najia(h) = f_lower(lo(h)) ⊕ f_upper(up(h))  [fully decomposed]")

    # Position split: which trigrams differ between lower and upper?
    print("\n  Position-dependent trigrams:")
    for t in range(8):
        lo_lines = list(lower_by_trig.get(t, [set()]))[0] if t in lower_by_trig else None
        up_lines = list(upper_by_trig.get(t, [set()]))[0] if t in upper_by_trig else None
        if lo_lines and up_lines:
            same = lo_lines == up_lines
            print(f"    {TRIGRAM_NAMES[t]}: {'same in both positions' if same else 'DIFFERS by position'}")

    return lo_indep and up_indep


def test_inner_bit_blindness():
    """Quantify 納甲 variation grouped by inner vs outer bits."""
    print("\n" + "=" * 60)
    print("INNER-BIT BLINDNESS")
    print("=" * 60)

    # Group by inner 4 bits (b1..b4): 16 groups × 4 hexagrams
    inner_groups = {}
    for h in range(NUM_HEX):
        key = (bit(h, 1), bit(h, 2), bit(h, 3), bit(h, 4))
        inner_groups.setdefault(key, []).append(h)

    inner_variation = []
    for key, hexes in sorted(inner_groups.items()):
        najia_set = {tuple(tuple(p) for p in najia(h)) for h in hexes}
        inner_variation.append(len(najia_set))

    print(f"\n  Inner-bit groups (16 groups of 4):")
    print(f"    Distinct najia per group: min={min(inner_variation)}, max={max(inner_variation)}")
    print(f"    → Every group has {max(inner_variation)} distinct assignments (maximal variation)")

    # Per-line: which lines vary within inner-bit groups?
    print(f"\n  Per-line variation within inner-bit groups:")
    for pos in range(6):
        varies = sum(
            1 for hexes in inner_groups.values()
            if len({najia(h)[pos] for h in hexes}) > 1
        )
        trig_label = "lower" if pos < 3 else "upper"
        bit_label = f"b{pos}" + (" (outer)" if pos in (0, 5) else " (inner)")
        print(f"    L{pos+1} [{trig_label}, {bit_label}]: varies in {varies}/16 groups")

    # Group by outer 2 bits (b0, b5): 4 groups × 16 hexagrams
    print(f"\n  Outer-bit groups (4 groups of 16):")
    for b0 in range(2):
        for b5 in range(2):
            hexes = [h for h in range(NUM_HEX) if bit(h, 0) == b0 and bit(h, 5) == b5]
            najia_set = {tuple(tuple(p) for p in najia(h)) for h in hexes}
            print(f"    (b0={b0}, b5={b5}): {len(najia_set)} distinct out of 16")


def analyze_element_gap():
    """Compare branch elements to trigram elements across all 384 states."""
    print("\n" + "=" * 60)
    print("BRANCH vs TRIGRAM ELEMENTS")
    print("=" * 60)

    relation_counter = Counter()
    mismatch_counts = []

    for h in range(NUM_HEX):
        lo, up = lower_trigram(h), upper_trigram(h)
        nj = najia(h)
        mismatches = 0

        for pos in range(6):
            _, branch = nj[pos]
            be = BRANCH_ELEMENT[branch]
            te = TRIGRAM_ELEMENT[lo if pos < 3 else up]

            rel = "比和" if be == te else five_phase_relation(te, be)
            relation_counter[rel] += 1
            if be != te:
                mismatches += 1

        mismatch_counts.append(mismatches)

    mismatch_dist = Counter(mismatch_counts)
    total = sum(relation_counter.values())

    print(f"\n  Relation distribution (384 states):")
    for rel, cnt in sorted(relation_counter.items(), key=lambda x: -x[1]):
        print(f"    {rel:>6}: {cnt:>3} ({cnt/total:.4f})")

    print(f"\n  Mismatches per hexagram:")
    for n in sorted(mismatch_dist):
        print(f"    {n}/6 lines mismatch: {mismatch_dist[n]} hexagrams")

    # Show element spread for each trigram
    print(f"\n  Branch element spread per trigram:")
    for t in range(8):
        # Get branches when used as lower trigram
        nj_lower = najia(t)[:3]  # trigram t as lower, upper=000
        elems = [BRANCH_ELEMENT[b] for _, b in nj_lower]
        te = TRIGRAM_ELEMENT[t]
        matches = sum(1 for e in elems if e == te)
        print(f"    {TRIGRAM_NAMES[t]} ({te}): branches={[BRANCH_ELEMENT[b] for _,b in nj_lower]}, "
              f"match={matches}/3")

    return mismatch_dist, relation_counter


# ═══════════════════════════════════════════════════════════════════════════
# Findings
# ═══════════════════════════════════════════════════════════════════════════

def write_findings(mismatch_dist, relation_counter):
    """Generate findings markdown."""
    lines = []
    w = lines.append

    w("# Probe 1: 納甲 as a Map on Z₂⁶\n")

    # ── Verification ──
    w("## 1. Verification\n")
    w("Implementation matches both worked examples exactly:\n")

    for name, h, positions in [
        ("姤 (天風姤) — 巽 lower, 乾 upper",
         0b110 | (0b111 << 3),
         ["初六", "九二", "九三", "九四", "九五", "上六"]),
        ("遁 (天山遁) — 艮 lower, 乾 upper",
         0b100 | (0b111 << 3),
         ["初六", "六二", "九三", "九四", "九五", "上九"]),
    ]:
        w(f"**{name}:**")
        w("```")
        nj = najia(h)
        for i in range(5, -1, -1):
            s, b = nj[i]
            w(f"  {positions[i]}  {s}{b}  {BRANCH_ELEMENT[b]}")
        w("```\n")

    # ── Factoring ──
    w("## 2. Factoring Structure\n")
    w("**納甲 factors completely through the trigram pair** as two independent functions:\n")
    w("```")
    w("najia(h) = ( f_lower(lower_trig(h)), f_upper(upper_trig(h)) )")
    w("```\n")
    w("The upper half's assignment depends only on the upper trigram,")
    w("the lower half only on the lower trigram. No cross-trigram interaction.\n")
    w("**Position split:** Only 乾 and 坤 assign different stems/branches")
    w("depending on whether they occupy the lower or upper position.")
    w("The other 6 trigrams are position-invariant.\n")

    # ── Inner-bit blindness ──
    w("## 3. Inner-Bit Blindness\n")
    w("納甲 reads the 3+3 trigram split (bits [0:3] and [3:6]).")
    w("It accesses every bit, but only through trigram membership.\n")
    w("It is **completely blind** to features depending on the inner")
    w("4-bit window (bits 1–4):\n")
    w("- 互卦 (nuclear hexagram)")
    w("- Basin membership and convergence depth")
    w("- Kernel decomposition (O, M, I components)\n")
    w("Within each inner-bit group (4 hexagrams sharing bits 1–4),")
    w("all 4 get **maximally different** 納甲 assignments.\n")
    w("**納甲 and 互卦 decompose Z₂⁶ along orthogonal axes.**\n")

    # ── Element gap ──
    w("## 4. Branch vs Trigram Elements\n")
    total = sum(relation_counter.values())
    w("Across 384 (hexagram, line) states:\n")
    w("| Relation | Count | Fraction |")
    w("|----------|------:|----------|")
    for rel, cnt in sorted(relation_counter.items(), key=lambda x: -x[1]):
        w(f"| {rel} | {cnt} | {cnt/total:.4f} |")
    w("")

    same = relation_counter.get("比和", 0)
    w(f"Only **{same}/{total} = {same/total:.1%}** of positions have matching branch")
    w(f"and trigram elements. The branch layer carries independent 五行 information.\n")

    w("### Mismatch count per hexagram\n")
    w("| Mismatches | Count |")
    w("|----------:|------:|")
    for n in sorted(mismatch_dist):
        w(f"| {n}/6 | {mismatch_dist[n]} |")
    w("")

    # Element spread per trigram
    w("### Branch element spread per trigram\n")
    w("| Trigram | Element | Branch elements (3 lines) | Matches |")
    w("|---------|---------|---------------------------|---------|")
    for t in range(8):
        nj = najia(t)[:3]  # t as lower, paired with 坤(000) as upper
        elems = [BRANCH_ELEMENT[b] for _, b in nj]
        te = TRIGRAM_ELEMENT[t]
        matches = sum(1 for e in elems if e == te)
        w(f"| {TRIGRAM_NAMES[t]} | {te} | {', '.join(elems)} | {matches}/3 |")
    w("")
    w("Each trigram's branches span multiple elements — typically 2–3 distinct")
    w("elements across its 3 lines, usually different from the trigram element.\n")

    # ── Algebraic characterization ──
    w("## 5. Algebraic Characterization\n")
    w("```")
    w("Z₂⁶ ──split──→ Z₂³ × Z₂³ ──lookup──→ (Stem × Branch)³ × (Stem × Branch)³")
    w("  h              (lo, up)               6 labeled lines")
    w("```\n")
    w("The first step (trigram extraction) is linear. The second (stem/branch assignment)")
    w("is a table lookup with no algebraic structure beyond the cyclic branch progressions")
    w("(arithmetic mod 12, step ±2).\n")
    w("The starting points per trigram are specific to the 納甲 tradition —")
    w("they encode a particular correspondence between the 8 trigrams and the")
    w("12 branches that has no obvious group-theoretic origin.\n")

    # ── Key insight ──
    w("## 6. Key Insight\n")
    w("**納甲 and the 互卦/kernel framework are algebraically orthogonal.**\n")
    w("| System | Reads | Blind to |")
    w("|--------|-------|----------|")
    w("| 納甲 | Trigram pair (shell) | Nuclear structure, basin, kernel |")
    w("| 互/kernel | Inner 4-bit window (core) | Trigram identity, outer bits |")
    w("")
    w("火珠林 accesses information 梅花 discards (individual trigram identity, 6-node resolution).")
    w("梅花 accesses information 火珠林 ignores (nuclear convergence, basin dynamics).")
    w("They are **complementary projections** of the same Z₂⁶ space.\n")

    out = Path(__file__).parent / "01_findings.md"
    out.write_text("\n".join(lines))
    print(f"\nFindings → {out}")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    if not verify_examples():
        print("\n*** VERIFICATION FAILED ***")
        return

    test_factoring()
    test_inner_bit_blindness()
    md, rc = analyze_element_gap()
    write_findings(md, rc)


if __name__ == "__main__":
    main()
