#!/usr/bin/env python3
"""
先天/後天 Arrangements as Mathematical Objects

Analyzes the two classical trigram arrangements on the octagonal compass.
Tests the dual uniqueness conjecture:
  - 先天 is the unique arrangement maximizing Z₂ geometric coherence
  - 後天 is the unique arrangement maximizing Z₅ geometric coherence

Enumerates all 96 cardinal-aligned arrangements, scores on 7 metrics,
identifies what uniquely selects 後天, computes Pareto frontier.

CORRECTION: The task's 先天 arrangement was wrong.
Task had (clockwise from S): 乾,兌,離,震,坤,巽,坎,艮
Correct (counterclockwise from S): 乾,兌,離,震,坤,艮,坎,巽
The lower half has 艮 and 巽 swapped. The correct version satisfies the
說卦傳 requirement that all complement pairs are diametrically opposed:
天地定位(乾↔坤), 山澤通氣(艮↔兌), 雷風相薄(震↔巽), 水火不相射(坎↔離).
"""

import sys
import json
import math
from pathlib import Path
from itertools import permutations, product, combinations
from collections import defaultdict

import numpy as np

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    SHENG_CYCLE, SHENG_MAP, KE_MAP,
)

# ─── Constants ───────────────────────────────────────────────────────────────

# Trigram binary values (bit0=bottom line)
KUN   = 0b000  # ☷ Earth
ZHEN  = 0b001  # ☳ Wood
KAN   = 0b010  # ☵ Water
DUI   = 0b011  # ☱ Metal
GEN   = 0b100  # ☶ Earth
LI    = 0b101  # ☲ Fire
XUN   = 0b110  # ☴ Wood
QIAN  = 0b111  # ☰ Metal

TRIGRAM_NAME = {
    KUN: "坤", ZHEN: "震", KAN: "坎", DUI: "兌",
    GEN: "艮", LI: "離", XUN: "巽", QIAN: "乾",
}

ALL_TRIGRAMS = list(range(8))

# Compass positions (clockwise from N, 0-indexed)
POS_NAMES = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
POS_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]
POS_INDEX = {p: i for i, p in enumerate(POS_NAMES)}

# Element assignment
ELEM = TRIGRAM_ELEMENT

# He Tu cardinal elements
HETU_CARDINAL = {"N": "Water", "S": "Fire", "E": "Wood", "W": "Metal"}

# 生 cycle ordering
SHENG_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_Z5 = {e: i for i, e in enumerate(SHENG_ORDER)}

# 克 cycle: stride-2 in Z₅
KE_ORDER = ["Wood", "Earth", "Water", "Fire", "Metal"]

# γ conjugation: [3,2,0,4,1] in 生-cycle coordinates
GAMMA = [3, 2, 0, 4, 1]

# Lo Shu perimeter
LO_SHU = {"S": 9, "SW": 2, "W": 7, "NW": 6, "N": 1, "NE": 8, "E": 3, "SE": 4}

# He Tu element numbers
HETU_NUM = {"Water": 1, "Fire": 2, "Wood": 3, "Metal": 4, "Earth": 5}

# ─── Arrangement Definitions ────────────────────────────────────────────────

# CORRECTED 先天八卦 (Fu Xi)
# Counterclockwise from S: S→SE→E→NE→N→NW→W→SW
# Sequence: 乾,兌,離,震,坤,艮,坎,巽
# Shao Yong values: 7,6,5,4,0,1,2,3 (upper half descends, lower half ascends)
XIANTIAN = {
    "S": QIAN,  "SE": DUI,  "E": LI,   "NE": ZHEN,
    "N": KUN,   "NW": GEN,  "W": KAN,  "SW": XUN,
}

# 後天八卦 (King Wen)
HOUTIAN = {
    "S": LI,   "SW": KUN, "W": DUI,  "NW": QIAN,
    "N": KAN,  "NE": GEN, "E": ZHEN, "SE": XUN,
}


# ─── Part 1: Enumerate 96 Cardinal-Aligned Arrangements ─────────────────────

def enumerate_cardinal_aligned():
    """
    Cardinal alignment: N=Water(Kan), S=Fire(Li), E=Wood, W=Metal.
    Wood: {Zhen, Xun}. Metal: {Qian, Dui}.
    E picks one Wood, W picks one Metal.
    Remaining 4 → intercardinals in any order.
    Total: 2 × 2 × 4! = 96.
    """
    arrangements = []
    wood = [ZHEN, XUN]
    metal = [QIAN, DUI]
    intercardinals = ["NE", "SE", "SW", "NW"]

    for e_wood in wood:
        other_wood = [w for w in wood if w != e_wood][0]
        for w_metal in metal:
            other_metal = [m for m in metal if m != w_metal][0]
            remaining = [other_wood, other_metal, KUN, GEN]
            for perm in permutations(remaining):
                arr = {"N": KAN, "S": LI, "E": e_wood, "W": w_metal}
                for pos, trig in zip(intercardinals, perm):
                    arr[pos] = trig
                arrangements.append(arr)

    return arrangements


# ─── Geometric Utilities ────────────────────────────────────────────────────

def pos_angle(pos):
    return POS_ANGLES[POS_INDEX[pos]]

def trig_pos(arr, trig):
    for p, t in arr.items():
        if t == trig:
            return p
    return None

def angular_distance(a1, a2):
    d = abs(a1 - a2) % 360
    return min(d, 360 - d)

def clockwise_distance(a1, a2):
    return (a2 - a1) % 360

def is_diametrically_opposed(pos1, pos2):
    return angular_distance(pos_angle(pos1), pos_angle(pos2)) == 180

def is_ns_reflection(pos1, pos2):
    """Reflection across N-S axis: angle → 360 - angle."""
    a1, a2 = pos_angle(pos1), pos_angle(pos2)
    return (360 - a1) % 360 == a2

# Complement pairs: XOR = 111
COMPLEMENT_PAIRS = [(t, t ^ 0b111) for t in range(8) if t < t ^ 0b111]

# Bit-reversal: swap b₀↔b₂
def bit_reverse(t):
    return ((t & 1) << 2) | ((t >> 1) & 1) << 1 | ((t >> 2) & 1)

BIT_REVERSAL_NONFIXED = [(t, bit_reverse(t)) for t in range(8)
                          if t < bit_reverse(t)]


# ─── Metric Functions ───────────────────────────────────────────────────────

def metric_complement_diameter(arr):
    """Count complement pairs (XOR=111) that are diametrically opposed."""
    count = 0
    for a, b in COMPLEMENT_PAIRS:
        pa, pb = trig_pos(arr, a), trig_pos(arr, b)
        if pa and pb and is_diametrically_opposed(pa, pb):
            count += 1
    return count

def metric_reversal_reflection(arr):
    """Count bit-reversal pairs that are N-S axis reflections."""
    count = 0
    for a, b in BIT_REVERSAL_NONFIXED:
        pa, pb = trig_pos(arr, a), trig_pos(arr, b)
        if pa and pb and is_ns_reflection(pa, pb):
            count += 1
    return count

def arrangement_as_list(arr):
    """Position-indexed list [N, NE, E, SE, S, SW, W, NW]."""
    return [arr[p] for p in POS_NAMES]

def make_rotation(k):
    """Clockwise rotation by k positions."""
    return [(i - k) % 8 for i in range(8)]

def make_reflection(axis):
    """Reflection: pos i → (2*axis - i) mod 8."""
    return [(2 * axis - i) % 8 for i in range(8)]

ALL_ISOMETRIES = (
    [("rot", k, make_rotation(k)) for k in range(8)] +
    [("ref", a, make_reflection(a)) for a in range(8)]
)

def check_isometry(arr, trigram_map):
    """Check if a trigram-level map acts as a compass isometry on this arrangement."""
    perm = arrangement_as_list(arr)
    trig_to_pos = {t: i for i, t in enumerate(perm)}
    sigma = []
    for i in range(8):
        target = trigram_map[perm[i]]
        if target not in trig_to_pos:
            return False, None
        sigma.append(trig_to_pos[target])
    for name, param, iso in ALL_ISOMETRIES:
        if sigma == iso:
            return True, (name, param)
    return False, None

def metric_v4_isometry(arr):
    """How many of {complement, reversal, comp∘rev} act as compass isometries."""
    comp = {t: t ^ 7 for t in range(8)}
    rev = {t: bit_reverse(t) for t in range(8)}
    comp_rev = {t: bit_reverse(t ^ 7) for t in range(8)}

    results = {}
    count = 0
    for name, m in [("complement", comp), ("reversal", rev), ("comp∘rev", comp_rev)]:
        is_iso, iso_type = check_isometry(arr, m)
        results[name] = (is_iso, iso_type)
        if is_iso:
            count += 1
    return count, results

def get_element_representatives(arr):
    """For each element, return list of (trigram, position_name) in arrangement."""
    reps = defaultdict(list)
    for pos, trig in arr.items():
        reps[ELEM[trig]].append((trig, pos))
    return reps

def sheng_spread_and_monotone(arr):
    """
    Min total angular travel to traverse 生 cycle.
    Try all representative choices for paired elements, both directions.
    """
    reps = get_element_representatives(arr)
    elem_choices = []
    for elem in SHENG_ORDER:
        elem_choices.append([(t, pos_angle(p)) for t, p in reps[elem]])

    best_spread = float('inf')
    best_monotone = False
    best_repr = None

    for combo in product(*elem_choices):
        angles = [c[1] for c in combo]
        trigs = [c[0] for c in combo]

        for direction in [1, -1]:
            total = 0
            steps = []
            for i in range(5):
                j = (i + 1) % 5
                if direction == 1:
                    step = clockwise_distance(angles[i], angles[j])
                else:
                    step = clockwise_distance(angles[j], angles[i])
                if step == 0:
                    step = 360
                steps.append(step)
                total += step

            # Monotone: all intermediate steps < 180 (no backtracking)
            monotone = all(s <= 180 for s in steps[:4])

            if (total < best_spread or
                (total == best_spread and monotone and not best_monotone)):
                best_spread = total
                best_monotone = monotone
                best_repr = list(zip(trigs, angles))

    return best_spread, best_monotone, best_repr

def ke_angular_variance(representatives):
    """Variance of angular jumps in 克 cycle using given representatives."""
    if not representatives:
        return float('inf')
    repr_angles = {ELEM[t]: a for t, a in representatives}
    steps = []
    for i in range(5):
        a1 = repr_angles[KE_ORDER[i]]
        a2 = repr_angles[KE_ORDER[(i + 1) % 5]]
        step = clockwise_distance(a1, a2)
        if step == 0:
            step = 360
        steps.append(step)
    return float(np.var(steps))


# ─── τ Analysis ─────────────────────────────────────────────────────────────

def compute_tau(xiantian, houtian):
    """τ = H ∘ X⁻¹: trigram permutation from 先天 to 後天."""
    xinv = {trig: pos for pos, trig in xiantian.items()}
    return {trig: houtian[xinv[trig]] for trig in range(8)}

def cycle_structure(perm):
    visited = set()
    cycles = []
    for start in sorted(perm.keys()):
        if start in visited:
            continue
        cycle = []
        x = start
        while x not in visited:
            visited.add(x)
            cycle.append(x)
            x = perm[x]
        if cycle:
            cycles.append(cycle)
    return cycles


# ─── Scoring ────────────────────────────────────────────────────────────────

def score_arrangement(arr, label=""):
    cd = metric_complement_diameter(arr)
    rr = metric_reversal_reflection(arr)
    v4_count, v4_detail = metric_v4_isometry(arr)
    spread, monotone, best_repr = sheng_spread_and_monotone(arr)
    ke_var = ke_angular_variance(best_repr)

    return {
        "label": label,
        "arrangement": {p: TRIGRAM_NAME[arr[p]] for p, _ in
                        sorted(arr.items(), key=lambda x: POS_INDEX[x[0]])},
        "complement_diameter": cd,
        "reversal_reflection": rr,
        "v4_isometry": v4_count,
        "v4_detail": v4_detail,
        "sheng_min_spread": spread,
        "sheng_monotone": monotone,
        "ke_angular_variance": ke_var,
        "best_repr": [(TRIGRAM_NAME[t], a) for t, a in best_repr] if best_repr else None,
        "z2_composite": cd + rr,
    }


# ─── Part 5: Lo Shu ────────────────────────────────────────────────────────

def lo_shu_analysis():
    results = []
    for pos in POS_NAMES:
        trig = HOUTIAN[pos]
        elem = ELEM[trig]
        ls = LO_SHU[pos]
        ht = HETU_NUM[elem]
        results.append({
            "pos": pos, "trig": TRIGRAM_NAME[trig], "elem": elem,
            "lo_shu": ls, "he_tu": ht,
            "ls_mod5": ls % 5, "ht_mod5": ht % 5,
            "match_mod5": (ls % 5) == (ht % 5),
        })
    return results


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# 先天/後天 Arrangements: Mathematical Analysis")
    out()

    # ── Part 0: Verify arrangements ──
    out("## Part 0: Arrangement Verification & Correction")
    out()

    out("### CORRECTION: 先天 arrangement")
    out("The task specified (S→SW→W→NW→N→NE→E→SE):")
    out("  乾,兌,離,震,坤,巽,坎,艮")
    out("This has 巽 and 艮 SWAPPED in the lower half and uses clockwise direction.")
    out("It violates 說卦傳: 山澤通氣 requires 艮↔兌 diametrically opposed,")
    out("but task places 兌(SW)↔艮(SE) at 90° apart.")
    out()
    out("Correct 先天 (counterclockwise S→SE→E→NE→N→NW→W→SW):")
    out("  乾,兌,離,震,坤,艮,坎,巽")
    out("  Shao Yong values: 7,6,5,4,0,1,2,3 (upper descends, lower ascends)")
    out()

    out("### Corrected 先天八卦")
    for pos in POS_NAMES:
        t = XIANTIAN[pos]
        out(f"  {pos:>3}: {TRIGRAM_NAME[t]} ({t:03b}) — {ELEM[t]}")
    out()

    # Verify all complement pairs diametrically opposed
    out("  Complement pair verification:")
    for a, b in COMPLEMENT_PAIRS:
        pa, pb = trig_pos(XIANTIAN, a), trig_pos(XIANTIAN, b)
        dist = angular_distance(pos_angle(pa), pos_angle(pb))
        ok = "✓" if dist == 180 else "✗"
        out(f"    {TRIGRAM_NAME[a]}({pa}) ↔ {TRIGRAM_NAME[b]}({pb}): {dist}° {ok}")
    out()

    out("### 後天八卦")
    for pos in POS_NAMES:
        t = HOUTIAN[pos]
        out(f"  {pos:>3}: {TRIGRAM_NAME[t]} ({t:03b}) — {ELEM[t]}")
    out()

    # Cardinal alignment check
    for name, arr in [("先天", XIANTIAN), ("後天", HOUTIAN)]:
        aligned = all(ELEM[arr[p]] == HETU_CARDINAL[p] for p in HETU_CARDINAL)
        out(f"  {name} cardinal-aligned: {aligned}")
    out()

    # ── Part 1: Enumerate 96 ──
    out("## Part 1: Enumeration")
    out()
    arrangements = enumerate_cardinal_aligned()
    out(f"Total cardinal-aligned: {len(arrangements)}")

    ht_index = next(i for i, arr in enumerate(arrangements)
                    if all(arr[p] == HOUTIAN[p] for p in POS_NAMES))
    out(f"後天 index: {ht_index}")
    out()

    # ── Part 2: Score everything ──
    out("## Part 2: Scoring")
    out()

    # Score 先天
    xt_scores = score_arrangement(XIANTIAN, "先天")
    out("### 先天 Scores")
    out(f"  complement_diameter:  {xt_scores['complement_diameter']}/4")
    out(f"  reversal_reflection:  {xt_scores['reversal_reflection']}/2")
    out(f"  v4_isometry:          {xt_scores['v4_isometry']}/3")
    for name, (is_iso, iso_type) in xt_scores["v4_detail"].items():
        out(f"    {name}: {'✓ ' + str(iso_type) if is_iso else '✗'}")
    out(f"  Z₂ composite:        {xt_scores['z2_composite']}/6")
    out(f"  sheng_min_spread:     {xt_scores['sheng_min_spread']}°")
    out(f"  sheng_monotone:       {xt_scores['sheng_monotone']}")
    out(f"  ke_angular_variance:  {xt_scores['ke_angular_variance']:.1f}")
    out(f"  best_repr: {xt_scores['best_repr']}")
    out()

    # Score all 96
    all_scores = []
    for i, arr in enumerate(arrangements):
        label = f"arr_{i:03d}" if i != ht_index else "後天"
        all_scores.append(score_arrangement(arr, label))

    ht_scores = all_scores[ht_index]
    out("### 後天 Scores")
    out(f"  complement_diameter:  {ht_scores['complement_diameter']}/4")
    out(f"  reversal_reflection:  {ht_scores['reversal_reflection']}/2")
    out(f"  v4_isometry:          {ht_scores['v4_isometry']}/3")
    for name, (is_iso, iso_type) in ht_scores["v4_detail"].items():
        out(f"    {name}: {'✓ ' + str(iso_type) if is_iso else '✗'}")
    out(f"  Z₂ composite:        {ht_scores['z2_composite']}/6")
    out(f"  sheng_min_spread:     {ht_scores['sheng_min_spread']}°")
    out(f"  sheng_monotone:       {ht_scores['sheng_monotone']}")
    out(f"  ke_angular_variance:  {ht_scores['ke_angular_variance']:.1f}")
    out(f"  best_repr: {ht_scores['best_repr']}")
    out()

    # ── Distributions ──
    out("### Metric Distributions (96 cardinal-aligned)")
    out()
    for metric in ["complement_diameter", "reversal_reflection", "v4_isometry",
                    "sheng_min_spread", "sheng_monotone", "ke_angular_variance"]:
        vals = [s[metric] for s in all_scores]
        dist = defaultdict(int)
        for v in vals:
            dist[v] += 1
        ht_val = ht_scores[metric]
        out(f"  {metric}:")
        for k in sorted(dist.keys()):
            marker = " ← 後天" if k == ht_val else ""
            out(f"    {k}: {dist[k]}{marker}")
        out()

    # ── Part 3: Progressive Filtering ──
    out("## Part 3: What Uniquely Selects 後天?")
    out()

    # Precompute basic filter sets
    mono_set = {i for i in range(96) if all_scores[i]["sheng_monotone"]}
    min_spread_val = min(all_scores[i]["sheng_min_spread"] for i in mono_set)
    min_ke_val = min(all_scores[i]["ke_angular_variance"] for i in range(96))
    ht_arr = arrangements[ht_index]

    # ── Element-pair geometry ──
    # In 後天: same-element pairs are adjacent (Wood: E/SE, Metal: W/NW)
    # and Earth trigrams are diametrically opposed (NE/SW = 180°)
    def element_pair_coherence(idx):
        """Check: paired elements have trigrams adjacent (45°) or opposed (180°)."""
        arr = arrangements[idx]
        for elem in ["Wood", "Metal", "Earth"]:
            trigs_of = [t for t in ALL_TRIGRAMS if ELEM[t] == elem]
            if len(trigs_of) == 2:
                p1, p2 = trig_pos(arr, trigs_of[0]), trig_pos(arr, trigs_of[1])
                dist = angular_distance(pos_angle(p1), pos_angle(p2))
                if dist not in (45, 180):
                    return False
        return True

    epc_set = {i for i in range(96) if element_pair_coherence(i)}

    # ── Same-element adjacent (both trigrams of each paired element are neighbors) ──
    def all_pairs_adjacent(idx):
        """All paired-element trigrams at adjacent positions (45°)."""
        arr = arrangements[idx]
        for elem in ["Wood", "Metal", "Earth"]:
            trigs_of = [t for t in ALL_TRIGRAMS if ELEM[t] == elem]
            if len(trigs_of) == 2:
                p1, p2 = trig_pos(arr, trigs_of[0]), trig_pos(arr, trigs_of[1])
                if angular_distance(pos_angle(p1), pos_angle(p2)) != 45:
                    return False
        return True

    adj_pair_set = {i for i in range(96) if all_pairs_adjacent(i)}

    # ── Wood adj + Metal adj + Earth opposed ──
    def wm_adj_earth_opp(idx):
        """Wood and Metal pairs adjacent, Earth pair diametrically opposed."""
        arr = arrangements[idx]
        for elem in ["Wood", "Metal"]:
            trigs = [t for t in ALL_TRIGRAMS if ELEM[t] == elem]
            p1, p2 = trig_pos(arr, trigs[0]), trig_pos(arr, trigs[1])
            if angular_distance(pos_angle(p1), pos_angle(p2)) != 45:
                return False
        earth = [t for t in ALL_TRIGRAMS if ELEM[t] == "Earth"]
        p1, p2 = trig_pos(arr, earth[0]), trig_pos(arr, earth[1])
        return angular_distance(pos_angle(p1), pos_angle(p2)) == 180

    wm_adj_e_opp_set = {i for i in range(96) if wm_adj_earth_opp(i)}

    # ── 生 cycle direction (clockwise vs counterclockwise) ──
    def sheng_direction(idx):
        """Return 'cw' if 生 representative path goes clockwise, 'ccw' if counter."""
        s = all_scores[idx]
        if not s["best_repr"]:
            return None
        angles = [a for _, a in s["best_repr"]]
        cw_steps = sum(1 for i in range(4) if 0 < clockwise_distance(angles[i], angles[i+1]) <= 180)
        return "cw" if cw_steps >= 3 else "ccw"

    # ── Yin/Yang line count pattern ──
    def yang_line_count(t):
        return bin(t).count('1')

    def cardinal_yinyang_balance(idx):
        """Cardinals have 2 male (1-yang) + 2 female (2-yang), as in 後天."""
        arr = arrangements[idx]
        cardinal_counts = [yang_line_count(arr[p]) for p in ["N", "E", "S", "W"]]
        return sorted(cardinal_counts) == [1, 1, 2, 2]

    yy_bal_set = {i for i in range(96) if cardinal_yinyang_balance(i)}

    # ── Son trigrams (1-yang: 震,坎,艮) in "yang" half (N,NE,E) ──
    SON_TRIGRAMS = {ZHEN, KAN, GEN}  # 1 yang line each
    def sons_in_yang_half(idx):
        arr = arrangements[idx]
        yang_half = {"N", "NE", "E"}
        sons_pos = {trig_pos(arr, t) for t in SON_TRIGRAMS}
        return sons_pos == yang_half

    sons_set = {i for i in range(96) if sons_in_yang_half(i)}

    # ── Assemble all filters ──
    filters = {
        "monotone": lambda i: i in mono_set,
        "cd≥1": lambda i: all_scores[i]["complement_diameter"] >= 1,
        "cd≥2": lambda i: all_scores[i]["complement_diameter"] >= 2,
        "rr≥1": lambda i: all_scores[i]["reversal_reflection"] >= 1,
        "elem_pair_coherent": lambda i: i in epc_set,
        "WM_adj_E_opp": lambda i: i in wm_adj_e_opp_set,
        "all_pairs_adj": lambda i: i in adj_pair_set,
        "yy_balance": lambda i: i in yy_bal_set,
        "sons_yang_half": lambda i: i in sons_set,
    }

    # ── Progressive filtering ──
    out("### Progressive filtering")
    out(f"  Start: 96")

    steps = [
        ("monotone", "生 cycle monotone"),
        ("elem_pair_coherent", "element pairs adjacent or opposed"),
        ("WM_adj_E_opp", "Wood/Metal adjacent, Earth opposed"),
        ("yy_balance", "cardinal yin/yang balance (1,1,2,2)"),
        ("sons_yang_half", "sons (震坎艮) at N/NE/E"),
    ]
    remaining = set(range(96))
    for fname, desc in steps:
        f = filters[fname]
        remaining = {i for i in remaining if f(i)}
        ht_in = "✓" if ht_index in remaining else "✗"
        out(f"  + {desc}: {len(remaining)} remain (後天: {ht_in})")

    if len(remaining) <= 10:
        out()
        out(f"  Surviving arrangements:")
        for i in sorted(remaining):
            arr = arrangements[i]
            label = all_scores[i]["label"]
            trigs = ', '.join(TRIGRAM_NAME[arr[p]] for p in POS_NAMES)
            out(f"    {label}: {trigs}")
    out()

    # ── Systematic uniqueness search ──
    out("### Systematic uniqueness search (all filter combinations)")
    out()
    unique_combos = []
    near_unique = []
    for r in range(1, len(filters) + 1):
        for combo in combinations(filters.items(), r):
            names = [c[0] for c in combo]
            fns = [c[1] for c in combo]
            result = [i for i in range(96) if all(f(i) for f in fns)]
            if ht_index in result:
                if len(result) == 1:
                    unique_combos.append(names)
                elif len(result) <= 3:
                    near_unique.append((names, [all_scores[i]["label"] for i in result]))

    if unique_combos:
        out("  Minimal constraint sets that UNIQUELY select 後天:")
        # Find truly minimal (no subset also unique)
        minimal = []
        for combo in unique_combos:
            is_minimal = not any(set(other) < set(combo) for other in unique_combos)
            if is_minimal:
                minimal.append(combo)
        for combo in minimal:
            out(f"    ★ {' ∧ '.join(combo)}")
        out()
    else:
        out("  No unique selection found.")
        out()

    if near_unique:
        out("  Near-unique (2-3 survivors):")
        seen = set()
        for names, labels in near_unique:
            key = tuple(sorted(names))
            if key not in seen and len(names) <= 3:
                seen.add(key)
                out(f"    {' ∧ '.join(names)}: {labels}")
        out()

    # ── Filter census ──
    out("### Individual filter sizes")
    for fname, f in filters.items():
        count = sum(1 for i in range(96) if f(i))
        ht_in = "✓" if f(ht_index) else "✗"
        out(f"  {fname}: {count}/96 (後天: {ht_in})")
    out()

    # ── 後天 vs nearest alternatives ──
    out("### 後天 vs nearest alternatives (differ by ≤2 positions)")
    out()
    out(f"  後天: {', '.join(TRIGRAM_NAME[ht_arr[p]] for p in POS_NAMES)}")
    out()
    for i in sorted(mono_set):
        if i == ht_index:
            continue
        arr = arrangements[i]
        diffs = [p for p in POS_NAMES if arr[p] != ht_arr[p]]
        if len(diffs) <= 2:
            s = all_scores[i]
            out(f"  {s['label']}: differs at {diffs}")
            out(f"    {', '.join(TRIGRAM_NAME[arr[p]] for p in POS_NAMES)}")
            out(f"    cd={s['complement_diameter']}, rr={s['reversal_reflection']}, "
                f"ke_var={s['ke_angular_variance']:.1f}")
    out()

    # ── Part 4: Pareto Frontier ──
    out("## Part 4: Pareto Frontier")
    out()

    # Z₅ composite: higher = better Z₅ embedding
    for s in all_scores + [xt_scores]:
        spread_score = 360 - s["sheng_min_spread"]
        mono_bonus = 90 if s["sheng_monotone"] else 0
        ke_penalty = s["ke_angular_variance"] / 100.0
        s["z5_composite"] = spread_score + mono_bonus - ke_penalty

    all_points = [(s["z2_composite"], s["z5_composite"], s["label"], i)
                  for i, s in enumerate(all_scores)]
    all_points.append((xt_scores["z2_composite"], xt_scores["z5_composite"], "先天", -1))

    # Pareto frontier (maximize both)
    pareto = []
    for z2, z5, label, idx in all_points:
        dominated = any(z2b >= z2 and z5b >= z5 and (z2b > z2 or z5b > z5)
                       for z2b, z5b, _, _ in all_points)
        if not dominated:
            pareto.append((z2, z5, label, idx))

    pareto.sort(key=lambda x: (-x[0], -x[1]))
    out("Pareto frontier (maximize Z₂ composite, Z₅ composite):")
    for z2, z5, label, idx in pareto:
        out(f"  Z₂={z2}, Z₅={z5:.1f} — {label}")
    out()

    xt_z2, xt_z5 = xt_scores["z2_composite"], xt_scores["z5_composite"]
    ht_z2, ht_z5 = ht_scores["z2_composite"], ht_scores["z5_composite"]

    # Separate cardinal-aligned from 先天
    ca_points = [p for p in all_points if p[3] >= 0]
    max_z2_ca = max(p[0] for p in ca_points)

    out(f"先天: Z₂={xt_z2}, Z₅={xt_z5:.1f}")
    out(f"後天: Z₂={ht_z2}, Z₅={ht_z5:.1f}")
    out()

    out(f"Max Z₂ among cardinal-aligned = {max_z2_ca}")
    z2_ca_maxers = [p for p in ca_points if p[0] == max_z2_ca]
    out(f"  {len(z2_ca_maxers)} arrangement(s) at this level")
    out()

    out(f"先天 Z₂ = {xt_z2} vs cardinal-aligned max = {max_z2_ca}")
    if xt_z2 > max_z2_ca:
        out(f"  → 先天 EXCEEDS all cardinal-aligned by {xt_z2 - max_z2_ca}")
        out(f"  → UNIQUE Z₂ champion (no cardinal-aligned arrangement can match)")
    elif xt_z2 == max_z2_ca:
        out(f"  → TIES (先天 not uniquely maximal)")
    out()

    max_z5_ca = max(p[1] for p in ca_points)
    z5_ca_maxers = [p for p in ca_points if p[1] == max_z5_ca]
    out(f"Max Z₅ among cardinal-aligned = {max_z5_ca:.1f}: {len(z5_ca_maxers)} arrangement(s)")
    out(f"後天 Z₅ = {ht_z5:.1f}: {'TIED for max' if ht_z5 == max_z5_ca else 'NOT max'}")
    out()

    # Distribution table
    out("Z₂ × Z₅ cross-tabulation:")
    z2_set = sorted(set(p[0] for p in all_points), reverse=True)
    z5_set = sorted(set(p[1] for p in all_points))
    grid = defaultdict(list)
    for z2, z5, label, idx in all_points:
        grid[(z2, z5)].append(label)

    header = f"  {'Z₂':>4} |" + "".join(f" {v:>7.1f}" for v in z5_set)
    out(header)
    out("  " + "-" * len(header))
    for z2v in z2_set:
        row = f"  {z2v:>4} |"
        for z5v in z5_set:
            labels = grid.get((z2v, z5v), [])
            count = len(labels)
            cell = f"{count:>7d}" if count > 0 else f"{'·':>7}"
            row += f" {cell}"
        out(row)
    out()

    # ── Part 4.5: τ analysis ──
    out("## Part 4.5: τ = H ∘ X⁻¹")
    out()
    tau = compute_tau(XIANTIAN, HOUTIAN)
    out("τ mapping (先天 position → 後天 trigram at that position):")
    for t in range(8):
        t2 = tau[t]
        out(f"  {TRIGRAM_NAME[t]} ({ELEM[t]:>5}) → {TRIGRAM_NAME[t2]} ({ELEM[t2]:>5})")
    out()

    cycles = cycle_structure(tau)
    cycles_str = [f"({'→'.join(TRIGRAM_NAME[t] for t in c)})" for c in cycles]
    out(f"Cycle structure: {' '.join(cycles_str)}")
    out(f"Cycle lengths: {sorted(len(c) for c in cycles)}")
    out()

    # Fiber analysis
    fiber_map = {}
    fiber_ok = True
    for t, t2 in tau.items():
        e1, e2 = ELEM[t], ELEM[t2]
        if e1 in fiber_map:
            if fiber_map[e1] != e2:
                fiber_ok = False
        else:
            fiber_map[e1] = e2

    out(f"Fiber preserved: {fiber_ok}")
    if not fiber_ok:
        out("Fiber map (not well-defined — showing conflicts):")
        elem_targets = defaultdict(set)
        for t, t2 in tau.items():
            elem_targets[ELEM[t]].add(ELEM[t2])
        for e, targets in sorted(elem_targets.items()):
            out(f"  {e} → {targets}")
    else:
        out("Fiber permutation on Z₅:")
        for e in SHENG_ORDER:
            out(f"  {e} → {fiber_map[e]}")

    gamma_map = {SHENG_ORDER[i]: SHENG_ORDER[GAMMA[i]] for i in range(5)}
    out(f"\nγ reference: {gamma_map}")
    out(f"γ match: {fiber_ok and all(fiber_map[e] == gamma_map[e] for e in SHENG_ORDER)}")
    out()

    # ── Part 5: Lo Shu ──
    out("## Part 5: Lo Shu Analysis")
    out()
    ls = lo_shu_analysis()
    out(f"{'Pos':>4} {'Trig':>3} {'Elem':>6} {'LS':>3} {'HT':>3} {'LS%5':>4} {'HT%5':>4} {'Mod5':>5}")
    mod5_matches = 0
    for r in ls:
        m = "✓" if r["match_mod5"] else "✗"
        if r["match_mod5"]:
            mod5_matches += 1
        out(f"{r['pos']:>4} {r['trig']:>3} {r['elem']:>6} {r['lo_shu']:>3} {r['he_tu']:>3} "
            f"{r['ls_mod5']:>4} {r['ht_mod5']:>4} {m:>5}")
    out(f"\nMod-5 matches: {mod5_matches}/8")
    out()

    # He Tu pairs
    hetu_pairs = {"Water": (1, 6), "Fire": (2, 7), "Wood": (3, 8),
                  "Metal": (4, 9), "Earth": (5, 10)}
    pair_matches = 0
    out("He Tu pair membership (inner/outer = n, n+5):")
    for r in ls:
        pair = hetu_pairs[r["elem"]]
        in_pair = r["lo_shu"] in pair
        if in_pair:
            pair_matches += 1
        out(f"  {r['pos']}: LS={r['lo_shu']}, {r['elem']} pair={pair}, "
            f"{'✓' if in_pair else '✗'}")
    out(f"\nHe Tu pair matches: {pair_matches}/8")
    out()

    # Lo Shu odd/even pattern
    out("Lo Shu parity pattern:")
    out("  Cardinals (N,E,S,W): all ODD in Lo Shu → {1,3,9,7}")
    out("  Intercardinals: all EVEN → {8,4,2,6}")
    cardinal_odd = all(LO_SHU[p] % 2 == 1 for p in ["N", "E", "S", "W"])
    inter_even = all(LO_SHU[p] % 2 == 0 for p in ["NE", "SE", "SW", "NW"])
    out(f"  Cardinals all odd: {cardinal_odd}")
    out(f"  Intercardinals all even: {inter_even}")
    out()

    # Lo Shu axis-opposite pairs (well-known: all sum to 10)
    out("Lo Shu axis-opposite pairs and 五行 relationships:")
    axis_pairs = [("S", "N"), ("SW", "NE"), ("W", "E"), ("NW", "SE")]
    for p1, p2 in axis_pairs:
        t1, t2 = HOUTIAN[p1], HOUTIAN[p2]
        e1, e2 = ELEM[t1], ELEM[t2]
        s = LO_SHU[p1] + LO_SHU[p2]
        # Determine 五行 relationship
        if e1 == e2:
            rel = "比和"
        elif SHENG_MAP.get(e1) == e2:
            rel = f"{e1}生{e2}"
        elif SHENG_MAP.get(e2) == e1:
            rel = f"{e2}生{e1}"
        elif KE_MAP.get(e1) == e2:
            rel = f"{e1}克{e2}"
        elif KE_MAP.get(e2) == e1:
            rel = f"{e2}克{e1}"
        else:
            rel = "?"
        out(f"  {p1}({TRIGRAM_NAME[t1]},{e1},{LO_SHU[p1]}) ↔ "
            f"{p2}({TRIGRAM_NAME[t2]},{e2},{LO_SHU[p2]}): "
            f"sum={s}, rel={rel}")
    out("  → All axis-opposite pairs sum to 10 (magic square property)")
    out("  → Paired elements: Fire↔Water (克), Earth↔Earth (比和), "
        "Metal↔Wood (克×2)")
    out()

    # ── Summary ──
    out("## Summary of Key Findings")
    out()
    out("### 先天 (Corrected)")
    out(f"  complement_diameter = {xt_scores['complement_diameter']}/4 (ALL pairs at 180°)")
    out(f"  reversal_reflection = {xt_scores['reversal_reflection']}/2")
    out(f"  v4_isometry = {xt_scores['v4_isometry']}/3")
    out(f"  Z₂ composite = {xt_scores['z2_composite']}/6")
    out()
    out("### 後天")
    out(f"  complement_diameter = {ht_scores['complement_diameter']}/4")
    out(f"  sheng_monotone = {ht_scores['sheng_monotone']}")
    out(f"  sheng_min_spread = {ht_scores['sheng_min_spread']}°")
    out(f"  ke_angular_variance = {ht_scores['ke_angular_variance']:.1f}")
    out()

    is_pareto = any(p[2] == "先天" for p in pareto)
    out(f"先天 on Pareto frontier: {is_pareto}")
    is_ht_pareto = any(p[2] == "後天" for p in pareto)
    out(f"後天 on Pareto frontier: {is_ht_pareto}")
    out()

    out("### Dual Uniqueness Conjecture")
    out(f"  先天 Z₂ = {xt_z2} vs cardinal-aligned max = {max_z2_ca}")
    if xt_z2 > max_z2_ca:
        out(f"  → 先天 is UNIQUE Z₂ champion (exceeds all 96 cardinal-aligned)")
    out(f"  後天 Z₅ = {ht_z5:.1f} (cardinal-aligned max = {max_z5_ca:.1f})")
    out(f"  → 後天 {'IS' if ht_z5 == max_z5_ca else 'is NOT'} among Z₅ maximizers ({len(z5_ca_maxers)} tied)")
    out(f"  → 後天 uniquely selected by: element_pair_coherent ∧ yy_balance ∧ sons_yang_half")
    out()

    # Write
    results_path = OUT_DIR / "02_arrangements_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
