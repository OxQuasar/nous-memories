#!/usr/bin/env python3
"""
Probe 8e: Algebraic analysis of 納甲 under complement.

Tests whether the complement involution σ (hex → 63-hex) induces
a consistent Z₅ transformation on 納甲 branch-element assignments,
extending the known trigram-level complement-Z₅ result to the
line-level 火珠林 system.
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "huozhulin"))
sys.path.insert(0, str(BASE / "opposition-theory" / "phase4"))

from cycle_algebra import (
    NUM_HEX, TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENTS,
    ELEMENT_ZH, SHENG_MAP, KE_MAP, MASK_ALL,
    lower_trigram, upper_trigram, fmt6, fmt3,
    five_phase_relation,
)

# Import from 01_najia_map.py (numeric prefix requires importlib)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "najia_map", BASE / "huozhulin" / "01_najia_map.py")
najia_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(najia_mod)

najia = najia_mod.najia
BRANCH_ELEMENT = najia_mod.BRANCH_ELEMENT
BRANCHES = najia_mod.BRANCHES
STEMS = najia_mod.STEMS
STEM_ELEMENT = najia_mod.STEM_ELEMENT
TRIGRAM_STEM = najia_mod.TRIGRAM_STEM
TRIGRAM_BRANCH_START = najia_mod.TRIGRAM_BRANCH_START
YANG_SEQ = najia_mod.YANG_SEQ
YIN_SEQ = najia_mod.YIN_SEQ
YANG_TRIGRAMS = najia_mod.YANG_TRIGRAMS
YIN_TRIGRAMS = najia_mod.YIN_TRIGRAMS

# ─── Z₅ encoding ──────────────────────────────────────────────────────────

ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}  # Wood=0 Fire=1 Earth=2 Metal=3 Water=4

def z5_diff(e1, e2):
    """Signed difference in Z₅: (idx(e2) - idx(e1)) mod 5."""
    return (ELEM_IDX[e2] - ELEM_IDX[e1]) % 5

def z5_neg(e):
    """Negation in Z₅: -idx(e) mod 5."""
    return ELEMENTS[(-ELEM_IDX[e]) % 5]

# ─── Trigram helpers ───────────────────────────────────────────────────────

TRIG_COMPLEMENT = {t: t ^ 0b111 for t in range(8)}

TRIGRAM_ZH = {
    0b111: "乾", 0b000: "坤", 0b001: "震", 0b110: "巽",
    0b010: "坎", 0b101: "離", 0b100: "艮", 0b011: "兌",
}

def trigram_najia_elements(trig, is_upper):
    """Get 3 branch elements for a trigram in given position."""
    # Build a dummy hexagram with this trigram in the desired position
    if is_upper:
        h = 0b000 | (trig << 3)  # pair with 坤 lower
    else:
        h = trig | (0b000 << 3)  # pair with 坤 upper
    nj = najia(h)
    if is_upper:
        return [(s, b, BRANCH_ELEMENT[b]) for s, b in nj[3:]]
    else:
        return [(s, b, BRANCH_ELEMENT[b]) for s, b in nj[:3]]


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: Characterize 納甲 as a map
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("PART 1: 納甲 TRIGRAM-LEVEL MAP")
print("=" * 70)

print("\nFor each trigram: stem, branches, and elements (lower / upper):\n")
print(f"{'Trig':>6s}  {'Pos':>5s}  {'Stem':>4s}  {'L1→L3 branches':>18s}  {'Elements':>20s}  {'TrigElem':>8s}")
print("─" * 80)

for t in range(8):
    te = TRIGRAM_ELEMENT[t]
    for is_upper in [False, True]:
        pos = "upper" if is_upper else "lower"
        lines = trigram_najia_elements(t, is_upper)
        stem = TRIGRAM_STEM[t][1 if is_upper else 0]
        branches = " ".join(b for _, b, _ in lines)
        elements = " ".join(ELEMENT_ZH[e] for _, _, e in lines)
        print(f"{TRIGRAM_ZH[t]:>6s}  {pos:>5s}  {stem:>4s}  {branches:>18s}  {elements:>20s}  {ELEMENT_ZH[te]:>8s}")

# Check: do lower and upper give same elements?
print("\nPosition invariance check:")
for t in range(8):
    lo_elems = [e for _, _, e in trigram_najia_elements(t, False)]
    up_elems = [e for _, _, e in trigram_najia_elements(t, True)]
    same = lo_elems == up_elems
    print(f"  {TRIGRAM_ZH[t]}: {'same' if same else 'DIFFERS'}"
          f"  lower={[ELEMENT_ZH[e] for e in lo_elems]}  upper={[ELEMENT_ZH[e] for e in up_elems]}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: Complement behavior at trigram level
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 2: COMPLEMENT BEHAVIOR (TRIGRAM LEVEL)")
print("=" * 70)

# First verify trigram-element complement-Z₅
print("\nTrigram-element complement check (known: σ = -id on Z₅):")
for t in range(4):  # 4 complement pairs
    tc = t ^ 0b111
    e1 = TRIGRAM_ELEMENT[t]
    e2 = TRIGRAM_ELEMENT[tc]
    neg_e1 = z5_neg(e1)
    ok = "✓" if e2 == neg_e1 else "✗"
    diff = z5_diff(e1, e2)
    print(f"  {TRIGRAM_ZH[t]}({ELEMENT_ZH[e1]}) ↔ {TRIGRAM_ZH[tc]}({ELEMENT_ZH[e2]})"
          f"  Z₅ diff={diff}  -id→{ELEMENT_ZH[neg_e1]}  {ok}")

# Now check 納甲 branch elements under complement
print("\n納甲 branch-element complement analysis:")
print("(Using lower position for both; upper shown separately if different)\n")

COMPLEMENT_PAIRS = [(0b111, 0b000), (0b001, 0b110), (0b010, 0b101), (0b100, 0b011)]

for t, tc in COMPLEMENT_PAIRS:
    print(f"  {TRIGRAM_ZH[t]} ↔ {TRIGRAM_ZH[tc]}:")
    for is_upper in [False, True]:
        pos = "upper" if is_upper else "lower"
        lines_t = trigram_najia_elements(t, is_upper)
        lines_tc = trigram_najia_elements(tc, is_upper)
        diffs = []
        for i in range(3):
            e1 = lines_t[i][2]
            e2 = lines_tc[i][2]
            d = z5_diff(e1, e2)
            diffs.append(d)
        consistent = len(set(diffs)) == 1
        elems_t = [ELEMENT_ZH[e] for _, _, e in lines_t]
        elems_tc = [ELEMENT_ZH[e] for _, _, e in lines_tc]
        print(f"    {pos:5s}: {elems_t} ↔ {elems_tc}  Z₅ diffs={diffs}  {'consistent' if consistent else 'INCONSISTENT'}")

# Global consistency check: is there a single Z₅ translation across all trigram pairs?
print("\nGlobal consistency: is σ a single Z₅ element across all lines?")
all_diffs = set()
for t, tc in COMPLEMENT_PAIRS:
    for is_upper in [False, True]:
        lines_t = trigram_najia_elements(t, is_upper)
        lines_tc = trigram_najia_elements(tc, is_upper)
        for i in range(3):
            d = z5_diff(lines_t[i][2], lines_tc[i][2])
            all_diffs.add(d)

if len(all_diffs) == 1:
    d = all_diffs.pop()
    print(f"  ✓ YES: σ acts as Z₅ translation by {d} (= {'−id' if d == 0 else f'+{d}'})")
else:
    print(f"  ✗ NO: σ produces multiple Z₅ shifts: {sorted(all_diffs)}")
    print("  The 納甲 branch-element map does NOT respect complement-Z₅ at the line level.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: Hexagram-level complement analysis
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 3: HEXAGRAM-LEVEL COMPLEMENT ANALYSIS")
print("=" * 70)

# For all 32 complement pairs
hex_results = []
consistent_count = 0
inconsistent_count = 0
diff_pattern_dist = Counter()

for h in range(32):
    hc = h ^ MASK_ALL
    nj_h = najia(h)
    nj_hc = najia(hc)

    elems_h = [BRANCH_ELEMENT[b] for _, b in nj_h]
    elems_hc = [BRANCH_ELEMENT[b] for _, b in nj_hc]

    diffs = [z5_diff(elems_h[i], elems_hc[i]) for i in range(6)]
    diff_tuple = tuple(diffs)
    diff_pattern_dist[diff_tuple] += 1

    consistent = len(set(diffs)) == 1
    if consistent:
        consistent_count += 1
    else:
        inconsistent_count += 1

    hex_results.append({
        'h': h, 'hc': hc,
        'elems_h': elems_h, 'elems_hc': elems_hc,
        'diffs': diffs, 'consistent': consistent,
    })

print(f"\n32 complement pairs:")
print(f"  Consistent (single Z₅ shift across 6 lines): {consistent_count}")
print(f"  Inconsistent (mixed shifts): {inconsistent_count}")

print(f"\nZ₅ diff patterns (lower3 | upper3):")
for pattern, count in sorted(diff_pattern_dist.items(), key=lambda x: -x[1]):
    lo_p = list(pattern[:3])
    up_p = list(pattern[3:])
    n_unique = len(set(pattern))
    print(f"  {lo_p}|{up_p}  ×{count}  {'(uniform)' if n_unique == 1 else ''}")

# Show a few examples
print("\nSample pairs:")
for r in hex_results[:6]:
    h, hc = r['h'], r['hc']
    lo_h, up_h = lower_trigram(h), upper_trigram(h)
    lo_hc, up_hc = lower_trigram(hc), upper_trigram(hc)
    eh = [ELEMENT_ZH[e] for e in r['elems_h']]
    ehc = [ELEMENT_ZH[e] for e in r['elems_hc']]
    tag = "consistent" if r['consistent'] else "MIXED"
    print(f"  {fmt6(h)} ({TRIGRAM_ZH[lo_h]}|{TRIGRAM_ZH[up_h]}) elems={eh}")
    print(f"  {fmt6(hc)} ({TRIGRAM_ZH[lo_hc]}|{TRIGRAM_ZH[up_hc]}) elems={ehc}")
    print(f"    diffs={r['diffs']}  [{tag}]")
    print()

# Analyze the inconsistency structure
print("Inconsistency analysis:")
print("  For inconsistent pairs, does the lower half have one shift and upper another?")
split_consistent = 0
for r in hex_results:
    if not r['consistent']:
        lo_diffs = set(r['diffs'][:3])
        up_diffs = set(r['diffs'][3:])
        if len(lo_diffs) == 1 and len(up_diffs) == 1:
            split_consistent += 1

print(f"  Pairs where lower is uniform AND upper is uniform (but different): "
      f"{split_consistent}/{inconsistent_count}")

# Identify the 2 consistent pairs
print(f"\nThe {consistent_count} consistent hexagram pairs:")
for r in hex_results:
    if r['consistent']:
        h, hc = r['h'], r['hc']
        lo_h, up_h = lower_trigram(h), upper_trigram(h)
        lo_hc, up_hc = lower_trigram(hc), upper_trigram(hc)
        shift = r['diffs'][0]
        print(f"  {fmt6(h)} ({TRIGRAM_ZH[lo_h]}|{TRIGRAM_ZH[up_h]}) ↔ "
              f"{fmt6(hc)} ({TRIGRAM_ZH[lo_hc]}|{TRIGRAM_ZH[up_hc]})  "
              f"uniform Z₅ shift = +{shift}")

# Which trigram complement pairs produce per-half consistency?
print("\nPer-half consistency of the 4 trigram complement pairs:")
for t, tc in COMPLEMENT_PAIRS:
    for is_upper in [False, True]:
        lines_t = trigram_najia_elements(t, is_upper)
        lines_tc = trigram_najia_elements(tc, is_upper)
        diffs = [z5_diff(lines_t[i][2], lines_tc[i][2]) for i in range(3)]
        pos = "upper" if is_upper else "lower"
        ok = "✓ uniform" if len(set(diffs)) == 1 else "✗ mixed"
        print(f"  {TRIGRAM_ZH[t]}↔{TRIGRAM_ZH[tc]} {pos:5s}: Z₅ diffs={diffs}  {ok}")

# Why does 艮↔兌 work? Show branch-ring analysis
print("\nMechanism: branch-ring Z₁₂ → Z₅ projection")
print("  Yang ascending even branches → Z₅:")
yang_z5 = [ELEM_IDX[BRANCH_ELEMENT[BRANCHES[i]]] for i in YANG_SEQ]
print(f"    Branches: {[BRANCHES[i] for i in YANG_SEQ]}")
print(f"    Elements: {[ELEMENT_ZH[BRANCH_ELEMENT[BRANCHES[i]]] for i in YANG_SEQ]}")
print(f"    Z₅:       {yang_z5}")
print(f"    Steps:     {[(yang_z5[i+1]-yang_z5[i])%5 for i in range(5)]}")

print("  Yin descending odd branches → Z₅:")
yin_z5 = [ELEM_IDX[BRANCH_ELEMENT[BRANCHES[i]]] for i in YIN_SEQ]
print(f"    Branches: {[BRANCHES[i] for i in YIN_SEQ]}")
print(f"    Elements: {[ELEMENT_ZH[BRANCH_ELEMENT[BRANCHES[i]]] for i in YIN_SEQ]}")
print(f"    Z₅:       {yin_z5}")
print(f"    Steps:     {[(yin_z5[i+1]-yin_z5[i])%5 for i in range(5)]}")

print("\n  Non-constant steps → Z₁₂ arithmetic ≠ Z₅ arithmetic.")
print("  Root cause: Earth fiber has 4 branches (丑辰未戌) vs 2 for others.")
print("  This non-uniformity breaks the Z₁₂ → Z₅ projection's linearity.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: Compare with trigram-level element assignment
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 4: LINE-LEVEL vs TRIGRAM-LEVEL ELEMENTS")
print("=" * 70)

print("\nBranch elements vs trigram element for each trigram (lower position):\n")
print(f"{'Trig':>6s}  {'TrigElem':>8s}  {'L1':>6s}  {'L2':>6s}  {'L3':>6s}  {'Relations':>24s}")
print("─" * 70)

for t in range(8):
    te = TRIGRAM_ELEMENT[t]
    lines = trigram_najia_elements(t, False)
    elems = [e for _, _, e in lines]
    rels = []
    for e in elems:
        if e == te:
            rels.append("比和")
        else:
            rels.append(five_phase_relation(te, e))
    print(f"{TRIGRAM_ZH[t]:>6s}  {ELEMENT_ZH[te]:>8s}  "
          f"{'  '.join(f'{ELEMENT_ZH[e]:>6s}' for e in elems)}  "
          f"{', '.join(rels)}")

# What's the relationship pattern? Check if it's a cyclic shift in 生/克
print("\nRelation pattern analysis:")
print("  For yang trigrams (ascending branches), the 3 line elements cycle")
print("  through positions in the 生 cycle starting from a specific point.")
print("  For yin trigrams (descending branches), similarly.\n")

for t in range(8):
    te = TRIGRAM_ELEMENT[t]
    is_yang = t in YANG_TRIGRAMS
    # Show the branch sequence and their Z₅ indices
    lines = trigram_najia_elements(t, False)
    elems = [e for _, _, e in lines]
    idxs = [ELEM_IDX[e] for e in elems]
    steps = [(idxs[i+1] - idxs[i]) % 5 for i in range(2)]
    polarity = "yang" if is_yang else "yin"
    print(f"  {TRIGRAM_ZH[t]} ({polarity}): {[ELEMENT_ZH[e] for e in elems]}  "
          f"Z₅={idxs}  steps={steps}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: Fibers and homomorphism check
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 5: FIBERS AND ALGEBRAIC STRUCTURE")
print("=" * 70)

# Group 12 branches by element
print("\n地支 → 五行 fiber sizes:")
branch_fibers = defaultdict(list)
for b in BRANCHES:
    branch_fibers[BRANCH_ELEMENT[b]].append(b)

for elem in ELEMENTS:
    branches = branch_fibers[elem]
    print(f"  {ELEMENT_ZH[elem]:>2s}: {branches}  (size {len(branches)})")

print(f"\nFiber sizes: {[len(branch_fibers[e]) for e in ELEMENTS]}")
print("  Non-uniform: Earth has 4, others have 2.")
print("  Total: 4+2+2+2+2 = 12 ✓")

# Homomorphism check: is 納甲 a group homomorphism Z₈ × Z₃ → Z₅?
print("\nHomomorphism check: 納甲 as Z₈ × Z₃ → Z₅")
print("  Z₈ = trigram (binary), Z₃ = line position (0,1,2), Z₅ = element")
print()

# For a homomorphism φ: Z₈ × Z₃ → Z₅, we need:
# φ(t1 + t2, p1 + p2) = φ(t1, p1) + φ(t2, p2)
# Test: does φ(t, p) = a·t + b·p (mod 5) for some a, b?
# (Where t is trigram value 0-7, p is position 0-2)

# Build the actual map
najia_map = {}  # (trigram, position, is_upper) → element
for t in range(8):
    for is_upper in [False, True]:
        lines = trigram_najia_elements(t, is_upper)
        for p in range(3):
            najia_map[(t, p, is_upper)] = ELEM_IDX[lines[p][2]]

# Test linearity for lower position only
print("  Testing linearity for lower position:")
is_linear = True
# If linear: φ(t, p) = a·t + b·p mod 5
# Try all (a, b) in Z₅ × Z₅
best_fit = (0, 0, 0)
for a in range(5):
    for b in range(5):
        matches = 0
        for t in range(8):
            for p in range(3):
                predicted = (a * t + b * p) % 5
                actual = najia_map[(t, p, False)]
                if predicted == actual:
                    matches += 1
        if matches > best_fit[2]:
            best_fit = (a, b, matches)

total_cells = 8 * 3
print(f"  Best linear fit: a={best_fit[0]}, b={best_fit[1]}, "
      f"matches={best_fit[2]}/{total_cells}")
print(f"  {'Linear!' if best_fit[2] == total_cells else 'NOT linear.'}")

# Check what structure it IS
print("\n  Actual element map (lower position, Z₅ indices):")
print(f"  {'Trig':>4s}  {'p=0':>3s}  {'p=1':>3s}  {'p=2':>3s}  {'step01':>6s}  {'step12':>6s}")
for t in range(8):
    vals = [najia_map[(t, p, False)] for p in range(3)]
    s01 = (vals[1] - vals[0]) % 5
    s12 = (vals[2] - vals[1]) % 5
    print(f"  {t:>4d}  {vals[0]:>3d}  {vals[1]:>3d}  {vals[2]:>3d}  {s01:>6d}  {s12:>6d}")

# Check if steps are constant per polarity
yang_steps = set()
yin_steps = set()
for t in range(8):
    vals = [najia_map[(t, p, False)] for p in range(3)]
    s01 = (vals[1] - vals[0]) % 5
    s12 = (vals[2] - vals[1]) % 5
    if t in YANG_TRIGRAMS:
        yang_steps.add((s01, s12))
    else:
        yin_steps.add((s01, s12))

print(f"\n  Yang trigram step patterns: {yang_steps}")
print(f"  Yin trigram step patterns: {yin_steps}")

yang_constant = len(yang_steps) == 1
yin_constant = len(yin_steps) == 1
if yang_constant and yin_constant:
    ys = yang_steps.pop()
    yi = yin_steps.pop()
    print(f"\n  Yang: constant step {ys[0]} between lines (Z₅ arithmetic progression)")
    print(f"  Yin: constant step {yi[0]} between lines (Z₅ arithmetic progression)")
    if ys[0] == (5 - yi[0]) % 5:
        print(f"  Yang step + Yin step = {ys[0]}+{yi[0]} = {(ys[0]+yi[0])%5} (mod 5)")
        print(f"  → Yin step = negation of Yang step in Z₅!")
elif yang_constant:
    print(f"  Yang has constant step, Yin does not")
elif yin_constant:
    print(f"  Yin has constant step, Yang does not")
else:
    print(f"  Neither has constant step — not arithmetic progressions")

# Final characterization
print("\n" + "─" * 70)
print("ALGEBRAIC CHARACTERIZATION:")
print("─" * 70)
print("""
  納甲 = (trigram_lookup, polarity_step):
    1. Trigram identity → starting branch (via TRIGRAM_BRANCH_START table)
    2. Polarity (yang/yin) → step direction (+2/-2 in branch index)
    3. 3 branches per trigram = arithmetic progression in Z₁₂ (branch ring)
    4. Branch → element via the non-uniform 地支→五行 fiber map

  The map is:
    (trigram, line_pos) → branch_start[trigram] + polarity_sign × 2 × line_pos  (mod 12)
    → then project branch → element via the fixed 地支→五行 map

  NOT a group homomorphism because:
    - The starting points (trigram → branch_start) are a table lookup, not linear
    - The 地支→五行 projection is non-uniform (Earth fiber = 4, others = 2)
    - 12 is not divisible by 5, so the Z₁₂ → Z₅ projection is not a homomorphism

  It IS a composition of:
    (Z₂³ × Z₃) → Z₁₂ → Z₅
    where the first map is affine (start + step × pos) per trigram,
    and the second map is the fixed branch→element projection.
""")


# ═══════════════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ═══════════════════════════════════════════════════════════════════════════

results = []
w = results.append

w("# Probe 8e: 納甲 Under Complement\n")
w("> Algebraic analysis of whether the complement involution σ extends")
w("> from trigram-level to line-level 納甲 element assignments.\n")
w("---\n")

w("## Part 1: 納甲 as a Trigram-Level Map\n")
w("The 納甲 system factors through trigrams: each line's assignment depends only on")
w("which trigram it belongs to and its position (lower/upper) in the hexagram.\n")
w("| Trigram | Position | Stem | Branches | Elements | Trig Elem |")
w("|---------|----------|------|----------|----------|-----------|")
for t in range(8):
    te = TRIGRAM_ELEMENT[t]
    for is_upper in [False, True]:
        pos = "upper" if is_upper else "lower"
        lines = trigram_najia_elements(t, is_upper)
        stem = TRIGRAM_STEM[t][1 if is_upper else 0]
        branches = " ".join(b for _, b, _ in lines)
        elements = " ".join(ELEMENT_ZH[e] for _, _, e in lines)
        w(f"| {TRIGRAM_ZH[t]} | {pos} | {stem} | {branches} | {elements} | {ELEMENT_ZH[te]} |")

w("\n**Position invariance:** Only 乾 and 坤 differ between lower and upper position.")
w("All other trigrams are position-invariant in their branch-element assignments.\n")

w("## Part 2: Complement at Trigram Level\n")
w("At the trigram-element level, complement is known to induce -id on Z₅:")
w("  Wood↔Wood, Fire↔Water, Earth↔Metal (verified for all 4 complement pairs).\n")
w("**Key question:** Does this extend to the 3-line 納甲 branch-element assignments?\n")

for t, tc in COMPLEMENT_PAIRS:
    for is_upper in [False, True]:
        lines_t = trigram_najia_elements(t, is_upper)
        lines_tc = trigram_najia_elements(tc, is_upper)
        diffs = [z5_diff(lines_t[i][2], lines_tc[i][2]) for i in range(3)]
        pos = "upper" if is_upper else "lower"
        consistent = len(set(diffs)) == 1
        elems_t = [ELEMENT_ZH[e] for _, _, e in lines_t]
        elems_tc = [ELEMENT_ZH[e] for _, _, e in lines_tc]
        w(f"- {TRIGRAM_ZH[t]}↔{TRIGRAM_ZH[tc]} ({pos}): {elems_t} ↔ {elems_tc}  "
          f"Z₅ diffs={diffs}  {'✓' if consistent else '✗'}")

w(f"\n**Result:** σ produces Z₅ shifts {sorted(all_diffs)} across all lines.")
if len(all_diffs) == 1:
    w("The complement-Z₅ structure **extends** to 納甲 branch-level elements.\n")
else:
    w("The complement-Z₅ structure does **NOT** extend uniformly to 納甲 branch-level.\n")

w("## Part 3: Hexagram-Level Complement\n")
w(f"Of 32 complement pairs:")
w(f"- **{consistent_count}** have a single uniform Z₅ shift across all 6 lines")
w(f"- **{inconsistent_count}** have mixed shifts\n")

if inconsistent_count > 0:
    w(f"Of the {inconsistent_count} inconsistent pairs:")
    w(f"- **{split_consistent}** have uniform shift within each half (lower vs upper)")
    w(f"  but different shifts between halves.\n")

w("### Z₅ diff pattern distribution\n")
w("| Pattern (lower|upper) | Count | Uniform? |")
w("|----------------------|------:|----------|")
for pattern, count in sorted(diff_pattern_dist.items(), key=lambda x: -x[1]):
    lo_p = list(pattern[:3])
    up_p = list(pattern[3:])
    uniform = "✓" if len(set(pattern)) == 1 else ""
    w(f"| {lo_p}\\|{up_p} | {count} | {uniform} |")

w("\n## Part 4: Line-Level vs Trigram-Level Elements\n")
w("Each trigram's 3 branch elements form an arithmetic progression in Z₁₂ (branch ring),")
w("projected to Z₅ via the 地支→五行 map.\n")

yang_steps_recalc = set()
yin_steps_recalc = set()
for t in range(8):
    vals = [najia_map[(t, p, False)] for p in range(3)]
    s = (vals[1] - vals[0]) % 5
    if t in YANG_TRIGRAMS:
        yang_steps_recalc.add(s)
    else:
        yin_steps_recalc.add(s)

if len(yang_steps_recalc) == 1 and len(yin_steps_recalc) == 1:
    ys = yang_steps_recalc.pop()
    yi = yin_steps_recalc.pop()
    w(f"**Yang trigrams:** Z₅ step = +{ys} per line")
    w(f"**Yin trigrams:** Z₅ step = +{yi} per line")
    w(f"Yang + Yin steps = {(ys+yi)%5} (mod 5) → "
      f"{'negation pair in Z₅' if (ys+yi)%5 == 0 else 'not negation'}\n")

w("## Part 5: Algebraic Structure\n")
w("**地支 → 五行 fiber sizes:** Earth=4, Wood=2, Fire=2, Metal=2, Water=2\n")
w("**Not a group homomorphism** from Z₈ × Z₃ → Z₅ because:")
w("- Starting points are a table lookup (not linear in trigram index)")
w("- The Z₁₂ → Z₅ projection is non-homomorphic (12 ∤ 5)")
w(f"- Best linear approximation matches only {best_fit[2]}/{total_cells} cells\n")
w("**Actual structure:** composition of an affine map and a fixed projection:")
w("```")
w("(trigram, line_pos) → start[trigram] + polarity × 2 × pos  (mod 12)  →  element")
w("         Z₂³ × Z₃        affine per trigram on Z₁₂               Z₁₂ → Z₅")
w("```\n")

w("## Synthesis\n")
if len(all_diffs) > 1:
    w("The complement-Z₅ involution, which operates cleanly at the trigram-element")
    w("level (as -id on Z₅), does **not** extend uniformly to the 納甲 branch-element")
    w("level. The inconsistency arises because:")
    w("1. Complement swaps yang↔yin polarity, reversing the branch stepping direction")
    w("2. The branch→element projection (Z₁₂ → Z₅) is non-linear")
    w("3. Reversing direction in Z₁₂ does not commute with projection to Z₅\n")
    w("This confirms the structural boundary between the trigram-level algebra")
    w("(where complement-Z₅ operates) and the 火珠林 line-level system")
    w("(where 納甲 introduces a non-algebraic table lookup that breaks the symmetry).\n")
    w("### Why it breaks: the Earth fiber")
    w("")
    w("The Z₁₂ branch ring maps to Z₅ elements via 地支→五行. This projection is")
    w("non-uniform: Earth has 4 branches (丑辰未戌) while all others have 2.")
    w("Yang/yin sequences step by ±2 in Z₁₂ (arithmetic progressions), but the")
    w(f"Z₁₂ → Z₅ projection converts these to non-constant Z₅ step sequences:")
    yang_z5_loc = [ELEM_IDX[BRANCH_ELEMENT[BRANCHES[i]]] for i in YANG_SEQ]
    yin_z5_loc = [ELEM_IDX[BRANCH_ELEMENT[BRANCHES[i]]] for i in YIN_SEQ]
    yang_steps = [(yang_z5_loc[i+1]-yang_z5_loc[i])%5 for i in range(5)]
    yin_steps = [(yin_z5_loc[i+1]-yin_z5_loc[i])%5 for i in range(5)]
    w(f"- Yang Z₅ steps: {yang_steps}")
    w(f"- Yin Z₅ steps: {yin_steps}\n")
    w("Non-constant steps mean that shifting the starting point in Z₁₂ (as complement does)")
    w("changes the Z₅ step pattern seen by a 3-line window. Only 艮↔兌 avoids this")
    w("because their specific starting-point offsets happen to sample windows with")
    w("identical Z₅ step sequences.\n")
    w("### Factoring structure of the inconsistency\n")
    w(f"{split_consistent}/{inconsistent_count} inconsistent pairs maintain per-half consistency")
    w("(uniform Z₅ shift within each half, different shifts between halves).")
    w("This follows from 納甲 factoring: complement acts independently on each trigram half.")
    w("The two halves receive different Z₅ shifts when their trigram complement pairs differ")
    w("(which is true for all hexagrams where lower and upper trigrams are from different")
    w("complement families).\n")
    w(f"Only 2/32 pairs achieve full 6-line consistency:")
    for r in hex_results:
        if r['consistent']:
            h = r['h']
            lo, up = lower_trigram(h), upper_trigram(h)
            hc = r['hc']
            lo_c, up_c = lower_trigram(hc), upper_trigram(hc)
            w(f"- {fmt6(h)} ({TRIGRAM_ZH[lo]}|{TRIGRAM_ZH[up]}) ↔ "
              f"{fmt6(hc)} ({TRIGRAM_ZH[lo_c]}|{TRIGRAM_ZH[up_c]}): uniform shift +{r['diffs'][0]}")
    w("")
else:
    w("The complement-Z₅ involution extends cleanly to the 納甲 branch-element level.")
    w("This unifies the trigram-level and line-level algebraic structures.\n")

out_path = Path(__file__).resolve().parent / "probe_8e_results.md"
out_path.write_text("\n".join(results))
print(f"\n{'='*70}")
print(f"Results saved to {out_path}")
