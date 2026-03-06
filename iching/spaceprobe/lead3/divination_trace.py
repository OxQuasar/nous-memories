"""
Lead 3: Operational probe — trace Meihua divination through all coordinate systems.

Question: What's invariant along the 本→互→变 path across coordinate systems?

The Meihua evaluation circuit:
  本卦 (original hexagram) + moving line
  → 互卦 (nuclear hexagram) — erase outer lines, double inner
  → 变卦 (changed hexagram) — flip the moving line

Each step produces a hexagram. Each hexagram has:
  - Binary representation (Z₂⁶)
  - Trigram decomposition (lower + upper, each in Z₂³)
  - Five-phase assignment (via trigram→element mapping)
  - Lo Shu numbers (via KW circle position)
  - Mirror-pair decomposition (kernel + orbit)
  - KW pairing relationship

For each of 384 states (64 hex × 6 lines), trace all three hexagrams
through every coordinate system and look for invariants.

Key hypothesis: The M-I lock (H-subgroup from sequence investigation)
treats inner core as unit, outer as free. The 互卦 operation literally
erases outer and doubles inner. Are these the same structural feature?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from cycle_algebra import (
    NUM_HEX, MASK_ALL, MASK3, N,
    lower_trigram, upper_trigram, hugua, biangua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    five_phase_relation, tiyong_relation, tiyong_trigrams,
    hugua_tiyong_relation, kw_partner, reverse6, is_palindrome6,
    hamming6, hamming3, popcount, bit, fmt6, fmt3,
)

# ══════════════════════════════════════════════════════════════════════════════
# COORDINATE SYSTEMS
# ══════════════════════════════════════════════════════════════════════════════

# Lo Shu numbers (trigram → Lo Shu position on KW Later Heaven circle)
TRIGRAM_LOSHU = {
    0b010: 1,  # Kan N
    0b000: 2,  # Kun SW
    0b100: 3,  # Zhen E
    0b011: 4,  # Xun SE
    0b111: 6,  # Qian NW
    0b110: 7,  # Dui W
    0b001: 8,  # Gen NE
    0b101: 9,  # Li S
}

# Directions
TRIGRAM_DIRECTION = {
    0b010: "N",  0b000: "SW", 0b100: "E",  0b011: "SE",
    0b111: "NW", 0b110: "W",  0b001: "NE", 0b101: "S",
}

# Polarity partition
P_PLUS  = {0b010, 0b100, 0b110, 0b101}  # Kan, Zhen, Dui, Li (Lo Shu odd)
P_MINUS = {0b000, 0b001, 0b111, 0b011}  # Kun, Gen, Qian, Xun (Lo Shu even)

# Three involutions (ι₁=Fu Xi complement, ι₂=KW/Lo Shu diametric, ι₃=He Tu)
def iota1(t): return t ^ 0b111  # complement
def iota2(t):  # Lo Shu pairs summing to 10
    pairs = {0b010: 0b101, 0b101: 0b010,  # Kan↔Li (1↔9)
             0b000: 0b001, 0b001: 0b000,  # Kun↔Gen (2↔8)
             0b100: 0b110, 0b110: 0b100,  # Zhen↔Dui (3↔7)
             0b011: 0b111, 0b111: 0b011}  # Xun↔Qian (4↔6)
    return pairs[t]
def iota3(t):  # He Tu: Lo Shu numbers differ by 5
    pairs = {0b010: 0b111, 0b111: 0b010,  # Kan↔Qian (1↔6)
             0b000: 0b110, 0b110: 0b000,  # Kun↔Dui (2↔7)
             0b100: 0b001, 0b001: 0b100,  # Zhen↔Gen (3↔8)
             0b011: 0b101, 0b101: 0b011}  # Xun↔Li (4↔9)
    return pairs[t]

# Mirror-pair decomposition for hexagrams
def mirror_kernel(h):
    """3-bit kernel: palindromic part of the XOR mask between mirror pairs."""
    bits = [(h >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

def yang_count(h):
    return popcount(h)

def weight_tilt(h):
    """Weight difference between upper and lower trigrams."""
    return popcount(upper_trigram(h)) - popcount(lower_trigram(h))


# ══════════════════════════════════════════════════════════════════════════════
# COMPLETE STATE TRACE
# ══════════════════════════════════════════════════════════════════════════════

def trace_state(h, line):
    """Trace one divination state through all coordinate systems."""
    bg = biangua(h, line)
    hg = hugua(h)

    # Which trigram is 体, which is 用
    lo, up = lower_trigram(h), upper_trigram(h)
    if line <= 3:
        ti_trig, yong_trig = up, lo
        ti_pos = "upper"
    else:
        ti_trig, yong_trig = lo, up
        ti_pos = "lower"

    # 互卦 trigrams (体 position inherited)
    hg_lo, hg_up = lower_trigram(hg), upper_trigram(hg)
    if line <= 3:
        hu_ti, hu_yong = hg_up, hg_lo
    else:
        hu_ti, hu_yong = hg_lo, hg_up

    # 变卦 trigrams
    bg_lo, bg_up = lower_trigram(bg), upper_trigram(bg)
    if line <= 3:
        bian_ti, bian_yong = bg_up, bg_lo
    else:
        bian_ti, bian_yong = bg_lo, bg_up

    return {
        'hex': h, 'line': line,
        # Three hexagrams
        'ben': h, 'hu': hg, 'bian': bg,
        # Trigram decompositions
        'ben_lo': lo, 'ben_up': up,
        'hu_lo': hg_lo, 'hu_up': hg_up,
        'bian_lo': bg_lo, 'bian_up': bg_up,
        # 体/用
        'ti_pos': ti_pos,
        'ben_ti': ti_trig, 'ben_yong': yong_trig,
        'hu_ti': hu_ti, 'hu_yong': hu_yong,
        'bian_ti': bian_ti, 'bian_yong': bian_yong,
        # Five-phase relations
        'rel_ben': five_phase_relation(TRIGRAM_ELEMENT[ti_trig], TRIGRAM_ELEMENT[yong_trig]),
        'rel_hu': five_phase_relation(TRIGRAM_ELEMENT[hu_ti], TRIGRAM_ELEMENT[hu_yong]),
        'rel_bian': five_phase_relation(TRIGRAM_ELEMENT[bian_ti], TRIGRAM_ELEMENT[bian_yong]),
        # Elements
        'ben_ti_elem': TRIGRAM_ELEMENT[ti_trig],
        'ben_yong_elem': TRIGRAM_ELEMENT[yong_trig],
        'hu_ti_elem': TRIGRAM_ELEMENT[hu_ti],
        'hu_yong_elem': TRIGRAM_ELEMENT[hu_yong],
        'bian_ti_elem': TRIGRAM_ELEMENT[bian_ti],
        'bian_yong_elem': TRIGRAM_ELEMENT[bian_yong],
        # Lo Shu
        'ben_ti_loshu': TRIGRAM_LOSHU[ti_trig],
        'ben_yong_loshu': TRIGRAM_LOSHU[yong_trig],
        'hu_ti_loshu': TRIGRAM_LOSHU[hu_ti],
        'hu_yong_loshu': TRIGRAM_LOSHU[hu_yong],
        'bian_ti_loshu': TRIGRAM_LOSHU[bian_ti],
        'bian_yong_loshu': TRIGRAM_LOSHU[bian_yong],
        # Yang counts
        'ben_yang': yang_count(h),
        'hu_yang': yang_count(hg),
        'bian_yang': yang_count(bg),
        # Weight tilts
        'ben_tilt': weight_tilt(h),
        'hu_tilt': weight_tilt(hg),
        'bian_tilt': weight_tilt(bg),
        # KW partners
        'ben_partner': kw_partner(h),
        'hu_partner': kw_partner(hg),
        'bian_partner': kw_partner(bg),
    }


def all_states():
    return [trace_state(h, line) for h in range(NUM_HEX) for line in range(1, 7)]


# ══════════════════════════════════════════════════════════════════════════════
# INVARIANT TESTS
# ══════════════════════════════════════════════════════════════════════════════

def test_invariants(states):
    print("=" * 70)
    print("INVARIANT ANALYSIS: 本→互→变 PATH")
    print(f"({len(states)} states: 64 hexagrams × 6 moving lines)")
    print("=" * 70)

    # ── 1. 体 trigram preservation ──
    print("\n" + "─" * 70)
    print("1. 体 TRIGRAM PRESERVATION")
    print("─" * 70)

    # Does the 体 trigram stay the same across 本→互→变?
    ti_preserved_hu = sum(1 for s in states if s['ben_ti'] == s['hu_ti'])
    ti_preserved_bian = sum(1 for s in states if s['ben_ti'] == s['bian_ti'])
    ti_all_same = sum(1 for s in states if s['ben_ti'] == s['hu_ti'] == s['bian_ti'])

    print(f"  体 same in 本 and 互: {ti_preserved_hu}/{len(states)} ({100*ti_preserved_hu/len(states):.1f}%)")
    print(f"  体 same in 本 and 变: {ti_preserved_bian}/{len(states)} ({100*ti_preserved_bian/len(states):.1f}%)")
    print(f"  体 same in all three: {ti_all_same}/{len(states)} ({100*ti_all_same/len(states):.1f}%)")

    # When is 体 preserved in 互?
    # 互 erases outer (L1,L6), doubles inner (L3,L4).
    # If 体=upper: 互's upper = upper_nuclear = (L3,L4,L5). Different from upper=(L4,L5,L6) unless L3=L6.
    # If 体=lower: 互's lower = lower_nuclear = (L2,L3,L4). Different from lower=(L1,L2,L3) unless L1=L4.
    print("\n  When 体 is preserved in 互卦:")
    for pos in ["upper", "lower"]:
        preserved = [s for s in states if s['ti_pos'] == pos and s['ben_ti'] == s['hu_ti']]
        total = [s for s in states if s['ti_pos'] == pos]
        print(f"    体={pos}: {len(preserved)}/{len(total)} ({100*len(preserved)/len(total):.1f}%)")
        if preserved:
            # What's the condition?
            for s in preserved[:3]:
                h = s['hex']
                bits = [(h >> i) & 1 for i in range(6)]
                print(f"      hex={fmt6(h)} line={s['line']} "
                      f"lower={fmt3(s['ben_lo'])} upper={fmt3(s['ben_up'])} "
                      f"hu_lo={fmt3(s['hu_lo'])} hu_up={fmt3(s['hu_up'])}")

    # When is 体 preserved in 变?
    # 变 flips one bit. If moving line is in 用 trigram (by definition), 体 is unchanged.
    # Wait — 体 is the trigram NOT containing the moving line. So 变 flips a bit in 用.
    # Therefore 体 is ALWAYS preserved in 变!
    print(f"\n  体 preserved in 变卦: {ti_preserved_bian}/{len(states)}")
    print(f"  (Expected: 384/384 — moving line is always in 用, never in 体)")

    # ── 2. 体 element preservation ──
    print("\n" + "─" * 70)
    print("2. 体 ELEMENT PRESERVATION")
    print("─" * 70)

    elem_preserved_hu = sum(1 for s in states if s['ben_ti_elem'] == s['hu_ti_elem'])
    elem_preserved_bian = sum(1 for s in states if s['ben_ti_elem'] == s['bian_ti_elem'])
    elem_all_same = sum(1 for s in states if s['ben_ti_elem'] == s['hu_ti_elem'] == s['bian_ti_elem'])

    print(f"  体 element same in 本 and 互: {elem_preserved_hu}/{len(states)} ({100*elem_preserved_hu/len(states):.1f}%)")
    print(f"  体 element same in 本 and 变: {elem_preserved_bian}/{len(states)} ({100*elem_preserved_bian/len(states):.1f}%)")
    print(f"  体 element same in all three: {elem_all_same}/{len(states)} ({100*elem_all_same/len(states):.1f}%)")

    # ── 3. Lo Shu number relationships ──
    print("\n" + "─" * 70)
    print("3. LO SHU NUMBER RELATIONSHIPS")
    print("─" * 70)

    # Lo Shu sum of 体+用 across three stages
    loshu_sums = defaultdict(list)
    for s in states:
        loshu_sums['ben'].append(s['ben_ti_loshu'] + s['ben_yong_loshu'])
        loshu_sums['hu'].append(s['hu_ti_loshu'] + s['hu_yong_loshu'])
        loshu_sums['bian'].append(s['bian_ti_loshu'] + s['bian_yong_loshu'])

    for stage in ['ben', 'hu', 'bian']:
        sums = loshu_sums[stage]
        print(f"  {stage} Lo Shu (体+用) sum: mean={np.mean(sums):.2f}, std={np.std(sums):.2f}")

    # Lo Shu sum preserved across stages?
    sum_preserved_hu = sum(1 for i in range(len(states))
                          if loshu_sums['ben'][i] == loshu_sums['hu'][i])
    sum_preserved_bian = sum(1 for i in range(len(states))
                           if loshu_sums['ben'][i] == loshu_sums['bian'][i])
    print(f"\n  Lo Shu sum preserved 本→互: {sum_preserved_hu}/{len(states)}")
    print(f"  Lo Shu sum preserved 本→变: {sum_preserved_bian}/{len(states)}")

    # Lo Shu difference |体-用|
    loshu_diffs = defaultdict(list)
    for s in states:
        loshu_diffs['ben'].append(abs(s['ben_ti_loshu'] - s['ben_yong_loshu']))
        loshu_diffs['hu'].append(abs(s['hu_ti_loshu'] - s['hu_yong_loshu']))
        loshu_diffs['bian'].append(abs(s['bian_ti_loshu'] - s['bian_yong_loshu']))

    for stage in ['ben', 'hu', 'bian']:
        diffs = loshu_diffs[stage]
        print(f"  {stage} Lo Shu |体−用|: mean={np.mean(diffs):.2f}, std={np.std(diffs):.2f}")

    # ── 4. Yang count trajectory ──
    print("\n" + "─" * 70)
    print("4. YANG COUNT TRAJECTORY (本→互→变)")
    print("─" * 70)

    yang_deltas_hu = [s['hu_yang'] - s['ben_yang'] for s in states]
    yang_deltas_bian = [s['bian_yang'] - s['ben_yang'] for s in states]

    print(f"  Δyang (本→互): mean={np.mean(yang_deltas_hu):.3f}, std={np.std(yang_deltas_hu):.3f}")
    print(f"  Δyang (本→变): always {set(yang_deltas_bian)}")  # should be {-1, +1}

    # 互 yang count: does it contract toward center?
    ben_devs = [abs(s['ben_yang'] - 3) for s in states]
    hu_devs = [abs(s['hu_yang'] - 3) for s in states]
    contracts = sum(1 for i in range(len(states)) if hu_devs[i] < ben_devs[i])
    expands = sum(1 for i in range(len(states)) if hu_devs[i] > ben_devs[i])
    same = sum(1 for i in range(len(states)) if hu_devs[i] == ben_devs[i])
    print(f"\n  互 yang deviation from 3 vs 本:")
    print(f"    Contracts: {contracts}/{len(states)} ({100*contracts/len(states):.1f}%)")
    print(f"    Expands: {expands}/{len(states)} ({100*expands/len(states):.1f}%)")
    print(f"    Same: {same}/{len(states)} ({100*same/len(states):.1f}%)")

    # ── 5. Five-phase relation trajectory ──
    print("\n" + "─" * 70)
    print("5. FIVE-PHASE RELATION TRAJECTORY")
    print("─" * 70)

    rel_names = ["比和", "生体", "克体", "体生用", "体克用"]

    # Distribution at each stage
    for stage_key, stage_name in [('rel_ben', '本'), ('rel_hu', '互'), ('rel_bian', '变')]:
        counts = Counter(s[stage_key] for s in states)
        print(f"\n  {stage_name}: ", end="")
        for r in rel_names:
            print(f"{r}={counts.get(r, 0)} ", end="")
        print()

    # Relation preserved across stages
    rel_preserved_all = sum(1 for s in states if s['rel_ben'] == s['rel_hu'] == s['rel_bian'])
    rel_none_same = sum(1 for s in states if len(set([s['rel_ben'], s['rel_hu'], s['rel_bian']])) == 3)
    print(f"\n  All three same: {rel_preserved_all}/{len(states)} ({100*rel_preserved_all/len(states):.1f}%)")
    print(f"  All three different: {rel_none_same}/{len(states)} ({100*rel_none_same/len(states):.1f}%)")

    # Transition matrix: 本→互
    print(f"\n  Transition matrix 本→互:")
    trans_ben_hu = Counter((s['rel_ben'], s['rel_hu']) for s in states)
    print(f"  {'':>8s}", end="")
    for r in rel_names:
        print(f"  {r:>6s}", end="")
    print()
    for r1 in rel_names:
        print(f"  {r1:>8s}", end="")
        row_total = sum(trans_ben_hu.get((r1, r2), 0) for r2 in rel_names)
        for r2 in rel_names:
            c = trans_ben_hu.get((r1, r2), 0)
            pct = 100*c/row_total if row_total else 0
            print(f"  {c:4d}({pct:2.0f})", end="")
        print(f"  [{row_total}]")

    # ── 6. Weight tilt trajectory ──
    print("\n" + "─" * 70)
    print("6. WEIGHT TILT TRAJECTORY (upper_yang - lower_yang)")
    print("─" * 70)

    tilt_deltas_hu = [s['hu_tilt'] - s['ben_tilt'] for s in states]
    print(f"  Δtilt (本→互): mean={np.mean(tilt_deltas_hu):.3f}, std={np.std(tilt_deltas_hu):.3f}")
    print(f"  Tilt preserved 本→互: {sum(1 for d in tilt_deltas_hu if d == 0)}/{len(states)}")

    # ── 7. M-I LOCK CONNECTION ──
    print("\n" + "─" * 70)
    print("7. M-I LOCK AND 互卦: THE STRUCTURAL CONNECTION")
    print("─" * 70)

    # The H-subgroup {id, O, MI, OMI} = transformations where M-bit = I-bit.
    # O = flip outer pair (L1↔L6), M = flip middle (L2↔L5), I = flip inner (L3↔L4).
    # 互卦 erases O (L1,L6), preserves M(L2,L5) at reduced weight, doubles I(L3,L4).
    #
    # Key test: when the KW bridge kernel is in H (M-bit = I-bit),
    # what does that mean for the 互卦 of consecutive hexagrams?

    # For every pair of consecutive hexagrams in KW sequence:
    from sequence import KING_WEN, bits as kw_bits

    kw_hex = []
    for i in range(64):
        b = [int(c) for c in KING_WEN[i][2]]
        val = sum(b[j] << j for j in range(6))
        kw_hex.append(val)

    # Bridge kernels
    print("\n  Bridge kernel and 互卦 relationship:")
    h_count = 0
    non_h_count = 0
    hu_same_in_h = 0
    hu_same_not_h = 0

    H_SUBGROUP = {(0,0,0), (1,0,1), (0,1,1), (1,1,0)}  # {id, O, MI, OMI} kernels
    # Wait: kernel = (L1^L6, L2^L5, L3^L4) for the XOR mask.
    # id = (0,0,0), O = (1,0,0), M = (0,1,0), I = (0,0,1)
    # OM = (1,1,0), OI = (1,0,1), MI = (0,1,1), OMI = (1,1,1)
    # H = {id, O, MI, OMI} means M-bit = I-bit.
    # id: M=0, I=0 ✓. O: M=0, I=0 ✓. MI: M=1, I=1 ✓. OMI: M=1, I=1 ✓.
    H_SUBGROUP = {k for k in [(a,b,c) for a in range(2) for b in range(2) for c in range(2)]
                  if k[1] == k[2]}

    for i in range(63):
        h1, h2 = kw_hex[i], kw_hex[i+1]
        xor = h1 ^ h2
        kernel = (bit(xor, 0) ^ bit(xor, 5),
                  bit(xor, 1) ^ bit(xor, 4),
                  bit(xor, 2) ^ bit(xor, 3))

        hu1, hu2 = hugua(h1), hugua(h2)
        hu_same = (hu1 == hu2)

        in_h = kernel in H_SUBGROUP
        if in_h:
            h_count += 1
            if hu_same: hu_same_in_h += 1
        else:
            non_h_count += 1
            if hu_same: hu_same_not_h += 1

    print(f"  H-subgroup bridges: {h_count}/63")
    print(f"    互卦 same for both: {hu_same_in_h}/{h_count} ({100*hu_same_in_h/h_count:.0f}%)")
    print(f"  Non-H bridges: {non_h_count}/63")
    print(f"    互卦 same for both: {hu_same_not_h}/{non_h_count} ({100*hu_same_not_h/non_h_count:.0f}%)")
    print(f"\n  Interpretation: H bridges (M-I locked) should be MORE likely to")
    print(f"  preserve 互卦, because the inner core changes in lockstep.")

    # More precise: what does 互卦 see of each kernel type?
    print(f"\n  互卦 Hamming distance by bridge kernel type:")
    kernel_hu_dist = defaultdict(list)
    kernel_names = {
        (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
        (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
    }
    for i in range(63):
        h1, h2 = kw_hex[i], kw_hex[i+1]
        xor = h1 ^ h2
        kernel = (bit(xor, 0) ^ bit(xor, 5),
                  bit(xor, 1) ^ bit(xor, 4),
                  bit(xor, 2) ^ bit(xor, 3))
        hu_dist = hamming6(hugua(h1), hugua(h2))
        kernel_hu_dist[kernel].append(hu_dist)

    for k in sorted(kernel_names.keys()):
        dists = kernel_hu_dist.get(k, [])
        name = kernel_names[k]
        in_h = "H" if k in H_SUBGROUP else " "
        if dists:
            print(f"    {name:>3s} [{in_h}]: mean 互 distance = {np.mean(dists):.2f}, "
                  f"n={len(dists)}, values={dists}")

    # ── 8. Involution preservation ──
    print("\n" + "─" * 70)
    print("8. INVOLUTION PRESERVATION THROUGH 互卦")
    print("─" * 70)

    # Does 互卦 preserve the three involutions ι₁, ι₂, ι₃?
    # For each trigram pair (ti, yong) in 本, check whether the corresponding
    # pair in 互 maintains the same involution relationship.

    for iota_name, iota_fn in [("ι₁ (Fu Xi)", iota1), ("ι₂ (Lo Shu)", iota2), ("ι₃ (He Tu)", iota3)]:
        # Check: if ben_ti and ben_yong are ι-paired, are hu_ti and hu_yong also ι-paired?
        paired_ben = sum(1 for s in states if iota_fn(s['ben_ti']) == s['ben_yong'])
        paired_hu_when_ben = sum(1 for s in states
                                 if iota_fn(s['ben_ti']) == s['ben_yong']
                                 and iota_fn(s['hu_ti']) == s['hu_yong'])
        total_paired = paired_ben if paired_ben > 0 else 1
        print(f"  {iota_name}:")
        print(f"    本 体/用 are ι-paired: {paired_ben}/{len(states)}")
        if paired_ben > 0:
            print(f"    Of those, 互 体/用 also ι-paired: {paired_hu_when_ben}/{paired_ben} "
                  f"({100*paired_hu_when_ben/paired_ben:.1f}%)")

    # ── 9. Polarity preservation ──
    print("\n" + "─" * 70)
    print("9. POLARITY (P₊/P₋) TRAJECTORY")
    print("─" * 70)

    def polarity(t):
        return "+" if t in P_PLUS else "-"

    # Pattern of 体 polarity across stages
    pol_patterns = Counter()
    for s in states:
        pat = (polarity(s['ben_ti']), polarity(s['hu_ti']), polarity(s['bian_ti']))
        pol_patterns[pat] += 1

    print(f"\n  体 polarity pattern (本,互,变):")
    for pat, count in sorted(pol_patterns.items(), key=lambda x: -x[1]):
        print(f"    {pat}: {count}/{len(states)} ({100*count/len(states):.1f}%)")

    # Is polarity preserved?
    pol_all_same = sum(1 for s in states
                       if polarity(s['ben_ti']) == polarity(s['hu_ti']) == polarity(s['bian_ti']))
    print(f"\n  体 polarity preserved across all three: {pol_all_same}/{len(states)} ({100*pol_all_same/len(states):.1f}%)")

    # ── 10. KW pairing preservation ──
    print("\n" + "─" * 70)
    print("10. KW PAIRING: DOES 互卦 PRESERVE PARTNERS?")
    print("─" * 70)

    # hugua(h) and hugua(kw_partner(h)): are they KW partners?
    partner_preserved = 0
    partner_same = 0
    for h in range(NUM_HEX):
        p = kw_partner(h)
        hu_h = hugua(h)
        hu_p = hugua(p)
        if hu_h == hu_p:
            partner_same += 1
        elif kw_partner(hu_h) == hu_p:
            partner_preserved += 1

    print(f"  互(h) = 互(partner(h)): {partner_same}/64 ({100*partner_same/64:.1f}%)")
    print(f"  互(h) and 互(partner(h)) are KW partners: {partner_preserved}/64 ({100*partner_preserved/64:.1f}%)")
    print(f"  Neither: {64 - partner_same - partner_preserved}/64")

    # ── 11. The 互卦 as projection onto M∪I ──
    print("\n" + "─" * 70)
    print("11. 互卦 AS PROJECTION: WHAT INFORMATION SURVIVES?")
    print("─" * 70)

    # 互卦 = f(L2,L3,L4,L5) — depends on 4 bits, outputs 6 bits (but with structure)
    # The 64 hexagrams map to how many distinct 互卦 values?
    hu_values = set(hugua(h) for h in range(NUM_HEX))
    print(f"  Distinct 互卦 values: {len(hu_values)}/64")

    # Fiber sizes
    fibers = defaultdict(list)
    for h in range(NUM_HEX):
        fibers[hugua(h)].append(h)
    fiber_sizes = Counter(len(f) for f in fibers.values())
    print(f"  Fiber sizes: {dict(fiber_sizes)}")

    # What's lost: the outer pair (L1, L6). What's preserved: inner 4 bits.
    # But with doubling of L3, L4.
    # The information content is 4 bits (L2,L3,L4,L5) → 2⁴ = 16 distinct outputs.
    print(f"  Information: 6 bits → 4 bits (L2,L3,L4,L5). Loss = outer pair (L1,L6).")

    # What structural features are determined by the inner 4 bits?
    # Mirror kernel = (L1^L6, L2^L5, L3^L4): 互 preserves M-bit and I-bit, erases O-bit.
    print(f"\n  Mirror kernel fate under 互卦:")
    print(f"    O-bit (L1⊕L6): ERASED (both lines deleted)")
    print(f"    M-bit (L2⊕L5): PRESERVED (both lines kept)")
    print(f"    I-bit (L3⊕L4): PRESERVED and DOUBLED (appears twice in output)")

    # Verify: for each hexagram, check that 互卦 kernel has O-bit determined by M and I
    for h in range(NUM_HEX):
        hg = hugua(h)
        h_kernel = mirror_kernel(h)
        hg_kernel = mirror_kernel(hg)
        # 互卦 kernel: O-bit of 互卦 = L2(互)⊕L5(互) = L2(本)⊕L5(本) = M-bit(本)
        # Wait: 互 = (L2, L3, L4, L3, L4, L5). So 互's L1=L2(本), 互's L6=L5(本).
        # 互 kernel O-bit = 互L1 ⊕ 互L6 = L2(本) ⊕ L5(本) = M-bit(本).
        # 互 kernel M-bit = 互L2 ⊕ 互L5 = L3(本) ⊕ L4(本) = I-bit(本).
        # 互 kernel I-bit = 互L3 ⊕ 互L4 = L4(本) ⊕ L3(本) = I-bit(本).
        assert hg_kernel[0] == h_kernel[1], f"O(互) should = M(本): hex {h}"
        assert hg_kernel[1] == h_kernel[2], f"M(互) should = I(本): hex {h}"
        assert hg_kernel[2] == h_kernel[2], f"I(互) should = I(本): hex {h}"

    print(f"\n  Verified (64/64): 互卦 kernel = (M, I, I) where M,I are from 本卦")
    print(f"  The O-bit is replaced by M-bit. The M-bit is replaced by I-bit.")
    print(f"  This is a DOWNWARD SHIFT: O→M→I→I (outer info → middle → inner → inner)")
    print(f"\n  H-subgroup connection: H = {{kernels where M=I}}.")
    print(f"  互卦 kernel has M-bit = I-bit ALWAYS (both equal to 本's I-bit).")
    print(f"  ∴ Every 互卦 has its kernel in H. The 互卦 operation projects into H.")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    states = all_states()
    test_invariants(states)
