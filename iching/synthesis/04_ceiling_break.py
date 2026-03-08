#!/usr/bin/env python3
"""
Probe 4: Breaking the 2/5 Ceiling

Tests whether 日辰 (daily branch, Z₁₂) can break the 2/5 ceiling
imposed by 旺相休囚死 alone. The ceiling: each season empowers exactly
2/5 elements, and 六親→element is a bijection, so at most 2/5 六親
types can be simultaneously strong.

日辰 operates on Z₁₂ (branch-level), not Z₅ (element-level).
Two branches of the same element can have different 沖/合 status.
Question: does the joint (season × day-branch) system raise the ceiling?

Also: 梅花 temporal distribution analysis.
"""

import sys
import importlib.util
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

# ─── Import infrastructure ───────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/
ICHING = ROOT / "iching"

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
from cycle_algebra import (
    NUM_HEX, TRIGRAM_ELEMENT, ELEMENTS, SHENG_MAP, KE_MAP,
    lower_trigram, upper_trigram, fmt6, bit, hugua,
)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p1 = _load("najia", ICHING / "huozhulin" / "01_najia_map.py")
p2 = _load("palace", ICHING / "huozhulin" / "02_palace_kernel.py")
p3 = _load("liuqin", ICHING / "huozhulin" / "03_liuqin.py")
p6 = _load("seasonal", ICHING / "huozhulin" / "06_seasonal.py")

# ─── Constants ────────────────────────────────────────────────────────────

BRANCH_NAMES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
BRANCH_ELEMENT = p1.BRANCH_ELEMENT  # branch_name → element

# Convert to index-based for convenience
BRANCH_ELEM_IDX = [BRANCH_ELEMENT[BRANCH_NAMES[i]] for i in range(12)]

SEASON_NAMES = p6.SEASON_NAMES
SEASON_ELEMENT = p6.SEASON_ELEMENT
SEASON_TABLE = p6.SEASON_TABLE
STRONG = p6.STRONG

LIUQIN_NAMES = p3.LIUQIN_NAMES
LIUQIN_SHORT = p3.LIUQIN_SHORT

# 沖 (clash): distance 6 in Z₁₂
BRANCH_CHONG = {i: (i + 6) % 12 for i in range(12)}

# 六合 (six combines)
BRANCH_HE_PAIRS = [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]
BRANCH_HE = {}
for a, b in BRANCH_HE_PAIRS:
    BRANCH_HE[a] = b
    BRANCH_HE[b] = a

# 先天八卦 numbering for 梅花 temporal mapping
# mod 8: result 0 → treated as 8 (坤)
XIANTIAN_ORDER = {
    1: 0b111, 2: 0b011, 3: 0b101, 4: 0b001,
    5: 0b110, 6: 0b010, 7: 0b100, 8: 0b000,
}

OUT_DIR = Path(__file__).resolve().parent


# ─── Data preparation ────────────────────────────────────────────────────

def build_hex_data():
    """Build hexagram data: palace, 六親 word, branch indices per line."""
    _, hex_info = p2.generate_palaces()
    records = []
    for h in range(NUM_HEX):
        info = hex_info[h]
        pe = info['palace_elem']
        word = p3.liuqin_word(h, pe)
        nj = p1.najia(h)
        # branch indices (0-11) for each line
        branch_idxs = [BRANCH_NAMES.index(b) for _, b in nj]
        line_elems = [BRANCH_ELEMENT[b] for _, b in nj]
        records.append({
            'hex': h, 'palace_elem': pe,
            'word': word,
            'branch_idxs': branch_idxs,
            'line_elems': line_elems,
            'basin': info['basin'],
            'depth': info['depth'],
        })
    return records


# ═══════════════════════════════════════════════════════════════════════════
# Part A: Element-level ceiling test
# ═══════════════════════════════════════════════════════════════════════════

def part_a_element_ceiling():
    """For each (season, day_branch): count potentially promotable elements."""
    print("=" * 70)
    print("PART A: ELEMENT-LEVEL CEILING TEST")
    print("=" * 70)

    results = {}
    max_size = 0

    for season in SEASON_NAMES:
        se = SEASON_ELEMENT[season]
        wang = SEASON_TABLE[season]['旺']
        xiang = SEASON_TABLE[season]['相']
        strong_elems = {wang, xiang}

        for day_b in range(12):
            day_elem = BRANCH_ELEM_IDX[day_b]
            day_generates = SHENG_MAP[day_elem]

            # Potentially promotable: seasonally strong + day's element + day generates
            promotable = strong_elems | {day_elem, day_generates}
            size = len(promotable)
            max_size = max(max_size, size)
            results[(season, day_b)] = {
                'strong': strong_elems,
                'day_elem': day_elem,
                'day_gen': day_generates,
                'promotable': promotable,
                'size': size,
            }

    # Distribution
    size_dist = Counter(r['size'] for r in results.values())
    print(f"\n  Promotable element set sizes across 60 (season, day_branch) pairs:")
    for s in sorted(size_dist):
        print(f"    {s} elements: {size_dist[s]} pairs ({size_dist[s]/60:.0%})")
    print(f"\n  Maximum set size: {max_size}")

    # Detail: which pairs expand beyond 2?
    expansions = [(k, v) for k, v in results.items() if v['size'] > 2]
    if expansions:
        print(f"\n  Expansions beyond 2 ({len(expansions)} pairs):")
        for (season, day_b), v in sorted(expansions)[:12]:
            print(f"    {season:12s} + {BRANCH_NAMES[day_b]}({v['day_elem']:>5}): "
                  f"strong={v['strong']}, day_gen={v['day_gen']} → "
                  f"{v['promotable']} (size={v['size']})")
    else:
        print("\n  No expansions beyond 2 — day's element always overlaps seasonal 旺/相.")

    # Overlap analysis: how often does day_elem ∈ strong_elems?
    overlap_count = sum(1 for v in results.values() if v['day_elem'] in v['strong'])
    gen_overlap = sum(1 for v in results.values() if v['day_gen'] in v['strong'])
    print(f"\n  Day element ∈ seasonal 旺/相: {overlap_count}/60 ({overlap_count/60:.0%})")
    print(f"  Day generates ∈ seasonal 旺/相: {gen_overlap}/60 ({gen_overlap/60:.0%})")
    print(f"  Day element OUTSIDE seasonal 旺/相: {60-overlap_count}/60")

    return results, max_size


# ═══════════════════════════════════════════════════════════════════════════
# Part B: Hexagram-level active-type test
# ═══════════════════════════════════════════════════════════════════════════

def part_b_active_types(records):
    """For each (season, day_branch, hexagram): count distinct functionally active 六親 types."""
    print("\n" + "=" * 70)
    print("PART B: HEXAGRAM-LEVEL ACTIVE-TYPE TEST")
    print("=" * 70)

    max_active = 0
    active_dist = Counter()
    total = 0
    max_examples = []

    for season in SEASON_NAMES:
        for day_b in range(12):
            for rec in records:
                active_types = set()
                for i in range(6):
                    line_branch = rec['branch_idxs'][i]
                    line_elem = rec['line_elems'][i]
                    lq_type = rec['word'][i]

                    # Condition 1: seasonal strength
                    strength = p6.elem_strength(line_elem, season)
                    seasonally_active = strength in STRONG

                    # Condition 2: 暗動 — day branch clashes this line's branch
                    secretly_activated = BRANCH_CHONG[day_b] == line_branch

                    # Condition 3: 日辰生 — day's element generates this line's element
                    day_elem = BRANCH_ELEM_IDX[day_b]
                    day_supports = SHENG_MAP[day_elem] == line_elem

                    if seasonally_active or secretly_activated or day_supports:
                        active_types.add(lq_type)

                n_active = len(active_types)
                active_dist[n_active] += 1
                total += 1

                if n_active > max_active:
                    max_active = n_active
                    max_examples = [(season, day_b, rec['hex'], active_types)]
                elif n_active == max_active:
                    if len(max_examples) < 5:
                        max_examples.append((season, day_b, rec['hex'], active_types))

    print(f"\n  Total states: {total} (5 seasons × 12 branches × 64 hexagrams = {5*12*64})")
    print(f"\n  Active-type distribution:")
    for n in sorted(active_dist):
        print(f"    {n}/5 active types: {active_dist[n]:>5} ({active_dist[n]/total:.1%})")

    print(f"\n  MAXIMUM active types: {max_active}")
    if max_active > 2:
        print(f"  *** CEILING BROKEN — 日辰 EXPANDS BEYOND 2/5 ***")
    else:
        print(f"  Ceiling holds at 2/5.")

    if max_examples:
        print(f"\n  Examples at max ({max_active}):")
        for season, day_b, h, types in max_examples[:5]:
            type_str = ','.join(LIUQIN_SHORT[t] for t in sorted(types))
            print(f"    {season:12s} + {BRANCH_NAMES[day_b]}: hex={fmt6(h)} → {type_str}")

    return active_dist, max_active, total


# ═══════════════════════════════════════════════════════════════════════════
# Part C: Spotlight dynamics
# ═══════════════════════════════════════════════════════════════════════════

def part_c_spotlight(elem_results, max_active, records):
    """Conditional analysis based on Part B result."""
    print("\n" + "=" * 70)
    print("PART C: SPOTLIGHT DYNAMICS")
    print("=" * 70)

    if max_active > 2:
        _part_c_broken(elem_results, records)
    else:
        _part_c_holds(elem_results)


def _part_c_broken(elem_results, records):
    """Analysis when ceiling is broken."""
    print("\n  Ceiling broken — analyzing expansion dynamics.\n")

    # For each season: how many elements reachable across 12 daily branches?
    for season in SEASON_NAMES:
        reachable = set()
        for day_b in range(12):
            reachable |= elem_results[(season, day_b)]['promotable']
        print(f"  {season:12s}: {len(reachable)} elements reachable across 12 branches")
        print(f"    {reachable}")

    # Autocorrelation: adjacent day-branches
    print("\n  Autocorrelation of promotable sets (adjacent day-branches):")
    for season in SEASON_NAMES:
        overlaps = []
        for day_b in range(12):
            next_b = (day_b + 1) % 12
            s1 = elem_results[(season, day_b)]['promotable']
            s2 = elem_results[(season, next_b)]['promotable']
            overlaps.append(len(s1 & s2) / len(s1 | s2))
        print(f"    {season:12s}: mean Jaccard = {np.mean(overlaps):.3f}")

    # Cycle basin conflict check
    print("\n  Cycle basin conflict resolution check:")
    print("  The Cycle basin has Fire↔Water permanently conflicted.")
    print("  Does 日辰 resolve the conflict for any (season, day_branch)?")
    fire_water_both_active = []
    for season in SEASON_NAMES:
        for day_b in range(12):
            p = elem_results[(season, day_b)]['promotable']
            if 'Fire' in p and 'Water' in p:
                fire_water_both_active.append((season, day_b))

    n = len(fire_water_both_active)
    print(f"  Both Fire AND Water promotable: {n}/60 pairs ({n/60:.0%})")
    if n > 0:
        print(f"  Examples: {fire_water_both_active[:6]}")


def _part_c_holds(elem_results):
    """Analysis when ceiling holds."""
    print("\n  Ceiling holds — analyzing WHY.")

    # Count (season, day_branch) pairs where day element is outside 旺/相
    outside = []
    for (season, day_b), v in sorted(elem_results.items()):
        if v['day_elem'] not in v['strong']:
            outside.append((season, day_b, v['day_elem'], v['strong']))

    print(f"\n  Day element OUTSIDE seasonal 旺/相: {len(outside)}/60 pairs")
    if outside:
        print(f"\n  These pairs introduce a third element:")
        for season, day_b, de, strong in outside[:12]:
            print(f"    {season:12s} + {BRANCH_NAMES[day_b]}({de:>5}): 旺/相={strong}")

        # But check: does the third element's generated element overlap?
        print(f"\n  When day is outside, does day_generates overlap with 旺/相?")
        gen_overlaps = 0
        for season, day_b, de, strong in outside:
            dg = SHENG_MAP[de]
            if dg in strong:
                gen_overlaps += 1
        print(f"    day_generates ∈ 旺/相: {gen_overlaps}/{len(outside)}")


# ═══════════════════════════════════════════════════════════════════════════
# Part D: 梅花 temporal distribution
# ═══════════════════════════════════════════════════════════════════════════

def part_d_meihua():
    """梅花 先天起卦 temporal distribution analysis."""
    print("\n" + "=" * 70)
    print("PART D: 梅花 TEMPORAL DISTRIBUTION")
    print("=" * 70)

    def xiantian_trig(n):
        """Map modular result (1-8) to trigram binary value."""
        r = n % 8
        if r == 0:
            r = 8
        return XIANTIAN_ORDER[r]

    # Sample: year branch = 1 (丑), 12 months × 30 days × 12 hours
    year_branch = 1
    hex_counter = Counter()
    upper_counter = Counter()
    lower_counter = Counter()
    dongyao_counter = Counter()
    hour_hex = defaultdict(Counter)  # hour → hex distribution

    for month in range(1, 13):
        for day in range(1, 31):
            for hour in range(12):
                total = year_branch + month + day
                upper_trig = xiantian_trig(total)
                lower_trig = xiantian_trig(total + hour)
                dong_raw = (total + hour) % 6
                dong = dong_raw if dong_raw != 0 else 6  # 1-6

                hex_val = lower_trig | (upper_trig << 3)
                hex_counter[hex_val] += 1
                upper_counter[upper_trig] += 1
                lower_counter[lower_trig] += 1
                dongyao_counter[dong] += 1
                hour_hex[hour][hex_val] += 1

    total_states = 12 * 30 * 12  # = 4320
    n_distinct = len(hex_counter)

    print(f"\n  Sample: year_branch={year_branch}, 12 months × 30 days × 12 hours = {total_states}")
    print(f"\n  Distinct hexagrams accessed: {n_distinct}/64 ({n_distinct/64:.0%})")

    # Frequency distribution
    freq_dist = Counter(hex_counter.values())
    print(f"\n  Hexagram frequency distribution:")
    for freq in sorted(freq_dist):
        print(f"    appears {freq:>3}×: {freq_dist[freq]} hexagrams")

    # Most/least common
    most = hex_counter.most_common(5)
    print(f"\n  Most common:")
    for h, c in most:
        print(f"    {fmt6(h)}: {c} ({c/total_states:.1%})")

    least = hex_counter.most_common()[-5:]
    print(f"  Least common:")
    for h, c in reversed(least):
        print(f"    {fmt6(h)}: {c} ({c/total_states:.1%})")

    # Trigram distributions
    print(f"\n  Upper trigram distribution:")
    for t in sorted(upper_counter):
        from cycle_algebra import TRIGRAM_NAMES
        print(f"    {TRIGRAM_NAMES[t]:10s} ({fmt6(t)[:3]}): {upper_counter[t]}")

    print(f"\n  動爻 distribution:")
    for d in sorted(dongyao_counter):
        print(f"    line {d}: {dongyao_counter[d]} ({dongyao_counter[d]/total_states:.1%})")

    # Basin distribution by hour
    _, hex_info = p2.generate_palaces()
    print(f"\n  Basin distribution by hour (2-hour blocks):")
    print(f"  {'Hour':>4} | {'Kun':>5} {'Qian':>5} {'Cycle':>6} | distinct hex")
    print(f"  {'─'*4}─┼─{'─'*5}─{'─'*5}─{'─'*6}─┼─{'─'*12}")
    for hour in range(12):
        basin_count = Counter()
        for h, c in hour_hex[hour].items():
            basin_count[hex_info[h]['basin']] += c
        n_h = len(hour_hex[hour])
        print(f"  {hour:>4} | {basin_count.get('Kun',0):>5} {basin_count.get('Qian',0):>5} "
              f"{basin_count.get('Cycle',0):>6} | {n_h}")

    # Does 梅花 inherit the 2/5 ceiling?
    print(f"\n  2/5 ceiling in 梅花:")
    print(f"  梅花 uses seasonal strength (旺相休囚死) but NOT 日辰 branch mechanisms.")
    print(f"  Therefore 梅花 inherits the 2/5 ceiling identically:")
    print(f"  - 六親→element bijection ✓")
    print(f"  - Each season: exactly 2 elements 旺/相 ✓")
    print(f"  - Maximum simultaneously strong 六親 types: 2/5 ✓")

    # Uniformity test
    expected = total_states / 64
    chi2 = sum((hex_counter.get(h, 0) - expected) ** 2 / expected for h in range(64))
    print(f"\n  Uniformity: χ² = {chi2:.1f} (df=63, expected={expected:.1f})")
    print(f"  Distribution is {'non-uniform' if chi2 > 100 else 'approximately uniform'}")

    return hex_counter, total_states, n_distinct


# ═══════════════════════════════════════════════════════════════════════════
# Part E: Interpretation — interaction through 日辰?
# ═══════════════════════════════════════════════════════════════════════════

def part_e_interpretation(max_active, active_dist, total):
    """Connect ceiling analysis back to the orthogonality wall."""
    print("\n" + "=" * 70)
    print("PART E: INTERPRETATION — SHELL vs CORE INTERACTION")
    print("=" * 70)

    print(f"""
  The orthogonality wall (Probe 2):
    - 火珠林 operational structure (六親, 旺相) reads the SHELL (trigram pair)
    - 凶 signal lives in CORE (basin/depth, inner 4 bits)
    - These are algebraically orthogonal projections of Z₂⁶

  The 2/5 ceiling (Probe 6):
    - 六親→element is a bijection (5 types → 5 distinct elements)
    - Each season empowers exactly 2 elements → at most 2 types strong
    - This lives entirely in the SHELL projection

  日辰 operates on Z₁₂ (branches), not Z₅ (elements).
  Question: does 日辰 create a bridge between shell and core?

  Answer: {'YES — ceiling broken to ' + str(max_active) + '/5'
           if max_active > 2
           else 'PARTIAL — ceiling expands but through a DIFFERENT mechanism'}

  日辰's mechanisms (沖/暗動, 生) can activate lines that seasons cannot.
  But this activation operates on BRANCH IDENTITY, not on element identity.
  The branch→element map (Z₁₂ → Z₅) is many-to-one (12→5), so branch-level
  operations can discriminate lines that element-level operations cannot.

  Maximum active types achieved: {max_active}/5 across {total} states.
""")

    # Distribution of active types
    print(f"  Active-type distribution summary:")
    cumulative = 0
    for n in sorted(active_dist):
        cumulative += active_dist[n]
        print(f"    ≥{n} types: {total - cumulative + active_dist[n]:>6} states "
              f"({(total - cumulative + active_dist[n])/total:.1%})")

    # Key question: does the expansion touch the core?
    print(f"""
  Does 日辰 bridge the orthogonality wall?
  No. 日辰 operates on branches assigned by 納甲, which reads trigram pairs
  (shell). The branches are shell-level data. 沖 (Z₁₂ distance 6) and
  生 (element generation) are both shell→shell operations.
  日辰 increases the resolution within the shell (Z₅ → Z₁₂) but
  does not create cross-talk with the core (inner bits / basin / depth).

  The 2/5 ceiling and the orthogonality wall are INDEPENDENT constraints:
  - 2/5 ceiling: limits simultaneous activation (element-level)
  - Orthogonality wall: prevents shell from seeing core (information-level)
  日辰 softens the first but cannot touch the second.
""")


# ═══════════════════════════════════════════════════════════════════════════
# Write results
# ═══════════════════════════════════════════════════════════════════════════

def write_results(elem_results, max_elem_size, active_dist, max_active, total,
                  hex_counter, meihua_total, meihua_distinct):
    lines = []
    w = lines.append

    w("# Probe 4: Breaking the 2/5 Ceiling\n")

    # ── Part A ──
    w("## Part A: Element-Level Ceiling Test\n")
    w("For each (season, day_branch) pair (5 × 12 = 60), compute the set of")
    w("'potentially promotable' elements: {旺, 相} ∪ {day_element, day_generates}.\n")

    size_dist = Counter(r['size'] for r in elem_results.values())
    w("| Set size | Count | Fraction |")
    w("|----------|-------|----------|")
    for s in sorted(size_dist):
        w(f"| {s} | {size_dist[s]} | {size_dist[s]/60:.0%} |")
    w("")
    w(f"**Maximum set size: {max_elem_size}**\n")

    outside = sum(1 for v in elem_results.values() if v['day_elem'] not in v['strong'])
    w(f"Day element outside seasonal 旺/相: {outside}/60 pairs ({outside/60:.0%}).\n")

    if max_elem_size > 2:
        w("日辰's element can introduce elements beyond the seasonal 旺/相 pair.")
        w("The element-level ceiling can be exceeded when the day's element")
        w("differs from both 旺 and 相.\n")
    else:
        w("Day's element always overlaps with seasonal 旺/相 — no element-level expansion.\n")

    # ── Part B ──
    w("## Part B: Hexagram-Level Active-Type Test (Definitive)\n")
    w("For each (season, day_branch, hexagram) triple (5 × 12 × 64 = 3840):")
    w("A line is **functionally active** if ANY of:")
    w("- Its element is 旺 or 相 in this season")
    w("- The day branch 沖's this line's branch (暗動)")
    w("- The day branch's element 生 this line's element\n")
    w("Count distinct 六親 types with ≥1 active line.\n")

    w("| Active types | States | Fraction |")
    w("|-------------|--------|----------|")
    for n in sorted(active_dist):
        w(f"| {n}/5 | {active_dist[n]} | {active_dist[n]/total:.1%} |")
    w("")

    if max_active > 2:
        w(f"**CEILING BROKEN: maximum {max_active}/5 active types.**\n")
        w("日辰's branch-level mechanisms (沖/暗動, 日辰生) can activate 六親 types")
        w("whose elements are seasonally weak. The branch→element map (Z₁₂ → Z₅)")
        w("is many-to-one, so branch-level operations reach elements that the")
        w("season alone does not empower.\n")
    else:
        w("**Ceiling holds at 2/5.** 日辰 operates within the same element space.\n")

    # ── Part C ──
    w("## Part C: Spotlight Dynamics\n")

    if max_active > 2:
        # Reachability
        for season in SEASON_NAMES:
            reachable = set()
            for day_b in range(12):
                reachable |= elem_results[(season, day_b)]['promotable']
            w(f"- {season}: {len(reachable)} elements reachable across 12 branches: {reachable}")
        w("")

        # Fire-Water conflict
        fw_count = sum(1 for v in elem_results.values()
                       if 'Fire' in v['promotable'] and 'Water' in v['promotable'])
        w(f"**Cycle basin conflict resolution:** Both Fire AND Water promotable in "
          f"{fw_count}/60 pairs ({fw_count/60:.0%}).")
        if fw_count > 0:
            w("日辰 can simultaneously promote both Fire and Water elements,")
            w("partially resolving the Cycle basin's permanent internal conflict.\n")
        else:
            w("Fire and Water never simultaneously promotable — conflict persists.\n")
    else:
        w("Ceiling holds. The day branch's element falls within the seasonal 旺/相")
        w("set often enough that no net expansion occurs.\n")

    # ── Part D ──
    w("## Part D: 梅花 Temporal Distribution\n")
    w(f"Sample: year_branch=1, 12 months × 30 days × 12 hours = {meihua_total} time points.\n")
    w(f"**Distinct hexagrams accessed: {meihua_distinct}/64 ({meihua_distinct/64:.0%})**\n")

    # Frequency summary
    freq_dist = Counter(hex_counter.values())
    w("| Frequency | # Hexagrams |")
    w("|-----------|-------------|")
    for freq in sorted(freq_dist):
        w(f"| {freq}× | {freq_dist[freq]} |")
    w("")

    expected = meihua_total / 64
    chi2 = sum((hex_counter.get(h, 0) - expected) ** 2 / expected for h in range(64))
    w(f"χ² = {chi2:.1f} (df=63, expected per hex = {expected:.1f})")
    w(f"Distribution is {'**non-uniform**' if chi2 > 100 else '**approximately uniform**'}.\n")

    w("**2/5 ceiling in 梅花:** 梅花 uses seasonal strength (旺相休囚死) but does NOT")
    w("employ 日辰 branch mechanisms (沖, 暗動, 日辰生). Therefore:")
    w("- 六親→element bijection applies ✓")
    w("- Each season empowers exactly 2/5 elements ✓")
    w("- **梅花 inherits the 2/5 ceiling identically** ✓\n")

    # ── Part E ──
    w("## Part E: Connection to the Orthogonality Wall\n")

    w("### The two constraints\n")
    w("1. **2/5 ceiling** (element-level): limits simultaneous activation")
    w("2. **Orthogonality wall** (information-level): shell cannot see core\n")

    w("### 日辰's effect on each\n")
    w(f"- **2/5 ceiling**: {'BROKEN by 日辰 (expanded to ' + str(max_active) + '/5)'  if max_active > 2 else 'NOT broken — holds at 2/5'}")
    w("- **Orthogonality wall**: UNTOUCHED — 日辰 operates on branches from 納甲,")
    w("  which reads trigram pairs (shell). No cross-talk with basin/depth (core).\n")

    w("### Why 日辰 cannot bridge the wall\n")
    w("日辰 increases resolution within the shell (Z₅ → Z₁₂). The branch-level")
    w("mechanisms (沖/暗動, 六合, 日辰生/克) all operate on data assigned by 納甲,")
    w("which factors through the trigram pair decomposition. 納甲 is inner-bit blind")
    w("(Probe 1): it reads (lower_trig, upper_trig), not (b₁,b₂,b₃,b₄).")
    w("Therefore 日辰's operations, however rich in Z₁₂, remain in the shell's")
    w("image. No temporal mechanism in 火珠林 creates a channel to the core.\n")

    w("### Structural summary\n")
    w("```")
    w("             Z₂⁶")
    w("            /    \\")
    w("     Shell (trig pair)    Core (inner bits)")
    w("       ↓                    ↓")
    w("   納甲 → branches       互卦 → basins")
    w("       ↓                    ↓")
    w("   六親 × 旺相 × 日辰     凶 / depth")
    w("       ↓                    ↓")
    w("   2/5 ceiling            convergence")
    w("   (softened by 日辰)     (unreachable)")
    w("```\n")
    w("The 2/5 ceiling lives in the left branch. 凶 lives in the right branch.")
    w("日辰 can push the ceiling higher within the left branch, but the wall")
    w("between left and right is structural — it's the orthogonality of")
    w("trigram-pair vs inner-window decompositions of Z₂⁶.\n")

    out = OUT_DIR / "probe4_results.md"
    out.write_text("\n".join(lines))
    print(f"\n  Results → {out}")
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    records = build_hex_data()

    # Part A
    elem_results, max_elem_size = part_a_element_ceiling()

    # Part B
    active_dist, max_active, total = part_b_active_types(records)

    # Part C
    part_c_spotlight(elem_results, max_active, records)

    # Part D
    hex_counter, meihua_total, meihua_distinct = part_d_meihua()

    # Part E
    part_e_interpretation(max_active, active_dist, total)

    # Write results
    write_results(elem_results, max_elem_size, active_dist, max_active, total,
                  hex_counter, meihua_total, meihua_distinct)


if __name__ == "__main__":
    main()
