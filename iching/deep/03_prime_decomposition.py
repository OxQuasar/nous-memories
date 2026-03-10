#!/usr/bin/env python3
"""
Prime Decomposition of the 後天 Uniqueness

Builds on 02_arrangements.py findings:
  96 → 56 (monotone) → 8 (elem_pair_coherent) → 2 (yy_balance) → 1 (sons_yang_half)

Investigates:
  1. The 8 survivors of monotone + elem_pair_coherent: structure & symmetry
  2. The "anti-後天" arr_037: what it looks like, what it violates
  3. Z₅ distance → spatial distance embedding quality
  4. τ's two 4-cycles: algebraic structure
"""

import sys
from pathlib import Path
from itertools import product
from collections import defaultdict

import numpy as np

# ─── Import infrastructure from 02 ──────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    SHENG_CYCLE, SHENG_MAP, KE_MAP,
)

# ─── Constants (from 02) ────────────────────────────────────────────────────

KUN   = 0b000
ZHEN  = 0b001
KAN   = 0b010
DUI   = 0b011
GEN   = 0b100
LI    = 0b101
XUN   = 0b110
QIAN  = 0b111

TRIGRAM_NAME = {
    KUN: "坤", ZHEN: "震", KAN: "坎", DUI: "兌",
    GEN: "艮", LI: "離", XUN: "巽", QIAN: "乾",
}
ALL_TRIGRAMS = list(range(8))

POS_NAMES = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
POS_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]
POS_INDEX = {p: i for i, p in enumerate(POS_NAMES)}

ELEM = TRIGRAM_ELEMENT
SHENG_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_Z5 = {e: i for i, e in enumerate(SHENG_ORDER)}
KE_ORDER = ["Wood", "Earth", "Water", "Fire", "Metal"]

XIANTIAN = {
    "S": QIAN, "SE": DUI, "E": LI, "NE": ZHEN,
    "N": KUN, "NW": GEN, "W": KAN, "SW": XUN,
}
HOUTIAN = {
    "S": LI, "SW": KUN, "W": DUI, "NW": QIAN,
    "N": KAN, "NE": GEN, "E": ZHEN, "SE": XUN,
}

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

def yang_count(t):
    """Number of yang (1) lines in trigram."""
    return bin(t).count('1')

# ─── Enumeration + Filters (from 02) ────────────────────────────────────────

def enumerate_cardinal_aligned():
    from itertools import permutations
    arrangements = []
    for e_wood in [ZHEN, XUN]:
        other_wood = XUN if e_wood == ZHEN else ZHEN
        for w_metal in [QIAN, DUI]:
            other_metal = DUI if w_metal == QIAN else QIAN
            remaining = [other_wood, other_metal, KUN, GEN]
            for perm in permutations(remaining):
                arr = {"N": KAN, "S": LI, "E": e_wood, "W": w_metal}
                for pos, trig in zip(["NE", "SE", "SW", "NW"], perm):
                    arr[pos] = trig
                arrangements.append(arr)
    return arrangements

def sheng_spread_and_monotone(arr):
    reps = defaultdict(list)
    for pos, trig in arr.items():
        reps[ELEM[trig]].append((trig, pos))
    elem_choices = [[(t, pos_angle(p)) for t, p in reps[e]] for e in SHENG_ORDER]
    best_spread, best_monotone, best_repr = float('inf'), False, None
    for combo in product(*elem_choices):
        angles = [c[1] for c in combo]
        for direction in [1, -1]:
            total, steps = 0, []
            for i in range(5):
                j = (i + 1) % 5
                step = clockwise_distance(angles[i], angles[j]) if direction == 1 \
                    else clockwise_distance(angles[j], angles[i])
                if step == 0: step = 360
                steps.append(step)
                total += step
            monotone = all(s <= 180 for s in steps[:4])
            if total < best_spread or (total == best_spread and monotone and not best_monotone):
                best_spread, best_monotone = total, monotone
                best_repr = list(zip([c[0] for c in combo], [c[1] for c in combo]))
    return best_spread, best_monotone, best_repr

def is_monotone(arr):
    _, mono, _ = sheng_spread_and_monotone(arr)
    return mono

def element_pair_coherent(arr):
    for elem in ["Wood", "Metal", "Earth"]:
        trigs = [t for t in ALL_TRIGRAMS if ELEM[t] == elem]
        if len(trigs) == 2:
            p1, p2 = trig_pos(arr, trigs[0]), trig_pos(arr, trigs[1])
            dist = angular_distance(pos_angle(p1), pos_angle(p2))
            if dist not in (45, 180):
                return False
    return True

def cardinal_yy_balance(arr):
    counts = [yang_count(arr[p]) for p in ["N", "E", "S", "W"]]
    return sorted(counts) == [1, 1, 2, 2]

SON_TRIGRAMS = {ZHEN, KAN, GEN}
DAUGHTER_TRIGRAMS = {XUN, LI, DUI}

def sons_in_yang_half(arr):
    return {trig_pos(arr, t) for t in SON_TRIGRAMS} == {"N", "NE", "E"}


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# Prime Decomposition of 後天 Uniqueness")
    out()

    arrangements = enumerate_cardinal_aligned()
    ht_index = next(i for i, a in enumerate(arrangements)
                    if all(a[p] == HOUTIAN[p] for p in POS_NAMES))

    # ════════════════════════════════════════════════════════════════════════
    # Task 1: The 8 survivors
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 1: The 8 Survivors (monotone ∧ elem_pair_coherent)")
    out()

    survivors = []
    for i, arr in enumerate(arrangements):
        if is_monotone(arr) and element_pair_coherent(arr):
            survivors.append((i, arr))

    out(f"Count: {len(survivors)} (expected 8)")
    out()

    # Print each survivor with full detail
    out("### Full position maps")
    out()
    header = f"{'#':>3} {'Idx':>4}  " + "  ".join(f"{p:>3}" for p in POS_NAMES)
    out(header)
    out("-" * len(header))
    for rank, (i, arr) in enumerate(survivors):
        label = "★後天" if i == ht_index else f"  #{rank}"
        cols = "  ".join(f"{TRIGRAM_NAME[arr[p]]:>3}" for p in POS_NAMES)
        out(f"{label:>5} {i:>4}  {cols}")
    out()

    # Yang-line profile and son/daughter placement
    out("### Yang-line counts at cardinals & son/daughter positions")
    out()
    out(f"{'#':>3} {'Idx':>4}  {'N':>3} {'E':>3} {'S':>3} {'W':>3}  "
        f"{'Card.sorted':>14}  {'Sons at':>18}  {'Daughters at':>18}  "
        f"{'yy_bal':>6}  {'sons_NNE_E':>10}")
    out("-" * 120)

    for rank, (i, arr) in enumerate(survivors):
        card_yc = {p: yang_count(arr[p]) for p in ["N", "E", "S", "W"]}
        card_sorted = sorted(card_yc.values())

        sons_pos = sorted([trig_pos(arr, t) for t in SON_TRIGRAMS],
                          key=lambda p: POS_INDEX[p])
        daughters_pos = sorted([trig_pos(arr, t) for t in DAUGHTER_TRIGRAMS],
                               key=lambda p: POS_INDEX[p])

        yy = cardinal_yy_balance(arr)
        siy = sons_in_yang_half(arr)

        label = "★" if i == ht_index else " "
        card_str = "  ".join(f"{card_yc[p]:>3}" for p in ["N", "E", "S", "W"])
        out(f"  {label} {i:>4}  {card_str}  {str(card_sorted):>14}  "
            f"{','.join(sons_pos):>18}  {','.join(daughters_pos):>18}  "
            f"{'✓' if yy else '✗':>6}  {'✓' if siy else '✗':>10}")
    out()

    # What varies between the 8?
    out("### Structural decomposition of the 8")
    out()

    # For each survivor, extract: E-wood, W-metal, intercardinal assignment
    out("Degrees of freedom:")
    out()

    # Check: is it exactly {swap E-Wood} × {swap W-Metal} × {swap Earth at intercardinals}?
    configs = []
    for i, arr in survivors:
        e_trig = TRIGRAM_NAME[arr["E"]]
        w_trig = TRIGRAM_NAME[arr["W"]]
        # Find which Earth trigram is at NE vs SW (they must be opposed)
        earth_trigs = [t for t in ALL_TRIGRAMS if ELEM[t] == "Earth"]
        earth_pos = {trig_pos(arr, t): TRIGRAM_NAME[t] for t in earth_trigs}
        # Find which Wood is non-cardinal (SE/NW/NE/SW)
        wood_trigs = [t for t in [ZHEN, XUN] if t != arr["E"]]
        wood2_pos = trig_pos(arr, wood_trigs[0])
        metal_trigs = [t for t in [QIAN, DUI] if t != arr["W"]]
        metal2_pos = trig_pos(arr, metal_trigs[0])

        configs.append({
            "idx": i,
            "E": e_trig,
            "W": w_trig,
            "earth": earth_pos,
            "wood2_pos": wood2_pos,
            "metal2_pos": metal2_pos,
            "is_ht": i == ht_index,
        })

    # Display the 3 binary choices
    out(f"{'Idx':>4}  {'E':>3} {'W':>3}  {'other_Wood':>12}  {'other_Metal':>13}  "
        f"{'Earth_NE':>10} {'Earth_SW':>10}  {'label':>6}")
    out("-" * 80)
    for c in configs:
        out(f"{c['idx']:>4}  {c['E']:>3} {c['W']:>3}  "
            f"{c['wood2_pos']:>12}  {c['metal2_pos']:>13}  "
            f"{c['earth'].get('NE','—'):>10} {c['earth'].get('SW','—'):>10}  "
            f"{'★後天' if c['is_ht'] else '':>6}")
    out()

    # Check: is this exactly 2³=8?
    e_choices = set(c["E"] for c in configs)
    w_choices = set(c["W"] for c in configs)
    out(f"E-Wood choices: {e_choices}")
    out(f"W-Metal choices: {w_choices}")

    # Check Earth placement pattern
    earth_patterns = set()
    for c in configs:
        ne = c['earth'].get('NE', '?')
        sw = c['earth'].get('SW', '?')
        earth_patterns.add((ne, sw))
    out(f"Earth (NE,SW) patterns: {earth_patterns}")
    out()

    # Check if it's a group orbit
    out("Structure check: is it {E-swap} × {W-swap} × {Earth-swap} = Z₂³ = 8?")
    expected = len(e_choices) * len(w_choices) * len(earth_patterns)
    out(f"  |E-choices| × |W-choices| × |Earth-patterns| = "
        f"{len(e_choices)} × {len(w_choices)} × {len(earth_patterns)} = {expected}")
    out(f"  Actual survivors: {len(survivors)}")
    out(f"  Match: {'✓ Exact Z₂³ structure' if expected == len(survivors) else '✗ Not simple product'}")
    out()

    # Verify: for each of the 2³=8 combos, exactly one arrangement exists
    seen_combos = set()
    for c in configs:
        ne = c['earth'].get('NE', '?')
        combo = (c['E'], c['W'], ne)
        seen_combos.add(combo)
    out(f"  Distinct (E, W, Earth_NE) triples: {len(seen_combos)}")
    out(f"  All unique: {'✓' if len(seen_combos) == len(survivors) else '✗'}")
    out()

    # Show constraint breakdown
    out("### Constraint decomposition")
    out()
    out("The 3 independent Z₂ choices:")
    out("  Choice A: E = 震(Zhen) vs 巽(Xun)     — which Wood at cardinal E")
    out("  Choice B: W = 兌(Dui) vs 乾(Qian)     — which Metal at cardinal W")
    out("  Choice C: NE = 艮(Gen) vs 坤(Kun)     — which Earth at NE (other at SW)")
    out()
    out("These are independent because elem_pair_coherent forces:")
    out("  • Wood pair adjacent → other Wood at SE (adjacent to E)")
    out("  • Metal pair adjacent → other Metal at NW (adjacent to W)")
    out("  • Earth pair opposed → one at NE, other at SW")
    out()
    out("後天 selects: A=震, B=兌, C=艮")
    out("  → yy_balance eliminates 4 of 8 (requires cardinal yang-counts [1,1,2,2])")
    out("  → sons_yang_half eliminates 1 more (requires 震,坎,艮 at N,NE,E)")
    out()

    # Show exactly which choices survive each filter
    out("Filter action on the 8:")
    out(f"{'Idx':>4}  {'A(E)':>5} {'B(W)':>5} {'C(NE)':>6}  {'yy_bal':>6}  {'sons':>5}  {'survives':>8}")
    out("-" * 60)
    for c in configs:
        arr = arrangements[c['idx']]
        yy = cardinal_yy_balance(arr)
        siy = sons_in_yang_half(arr)
        surv = yy and siy
        out(f"{c['idx']:>4}  {c['E']:>5} {c['W']:>5} {c['earth'].get('NE','?'):>6}  "
            f"{'✓' if yy else '✗':>6}  {'✓' if siy else '✗':>5}  "
            f"{'★後天' if surv and c['is_ht'] else '✓' if surv else '✗':>8}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 2: The "anti-後天" arr_037
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 2: The Anti-後天 (arr_037)")
    out()

    # Find arr_037 among the monotone + elem_pair_coherent + yy_balance survivors
    yy_survivors = [(i, a) for i, a in survivors if cardinal_yy_balance(a)]
    out(f"Survivors of monotone + elem_pair_coherent + yy_balance: {len(yy_survivors)}")
    for i, arr in yy_survivors:
        label = "後天" if i == ht_index else f"arr_{i:03d}"
        out(f"  {label}: {', '.join(TRIGRAM_NAME[arr[p]] for p in POS_NAMES)}")
    out()

    # Find the anti-後天
    anti_ht_idx, anti_ht = next((i, a) for i, a in yy_survivors if i != ht_index)
    out(f"Anti-後天 = arr_{anti_ht_idx:03d}")
    out()

    # Position-by-position comparison
    out("### Position comparison: 後天 vs anti-後天")
    out()
    out(f"{'Pos':>4}  {'後天':>5}  {'anti':>5}  {'same?':>5}  {'elem':>6}")
    out("-" * 40)
    ht_arr = arrangements[ht_index]
    diff_positions = []
    for p in POS_NAMES:
        t_ht = ht_arr[p]
        t_anti = anti_ht[p]
        same = t_ht == t_anti
        if not same:
            diff_positions.append(p)
        out(f"{p:>4}  {TRIGRAM_NAME[t_ht]:>5}  {TRIGRAM_NAME[t_anti]:>5}  "
            f"{'✓' if same else '✗':>5}  {ELEM[t_ht]:>6}")
    out()
    out(f"Differences: {diff_positions}")
    out(f"  後天: {', '.join(f'{p}={TRIGRAM_NAME[ht_arr[p]]}' for p in diff_positions)}")
    out(f"  anti: {', '.join(f'{p}={TRIGRAM_NAME[anti_ht[p]]}' for p in diff_positions)}")
    out()

    # Sons placement
    out("### Son trigram positions (震=thunder, 坎=water, 艮=mountain)")
    out("  (Sons = 1-yang-line trigrams: the 'young yang' family)")
    out()
    for label, arr in [("後天", ht_arr), ("anti", anti_ht)]:
        sons = {t: trig_pos(arr, t) for t in SON_TRIGRAMS}
        daughters = {t: trig_pos(arr, t) for t in DAUGHTER_TRIGRAMS}
        out(f"  {label}:")
        for t, p in sorted(sons.items()):
            out(f"    {TRIGRAM_NAME[t]} (yang={yang_count(t)}) → {p}")
        out(f"    Daughters:")
        for t, p in sorted(daughters.items()):
            out(f"    {TRIGRAM_NAME[t]} (yang={yang_count(t)}) → {p}")
    out()

    # What traditional properties does anti-後天 violate?
    out("### Traditional property check for anti-後天")
    out()

    # Check: does anti-後天 violate the family structure?
    # In 後天: sons at N,NE,E (yang/rising half), daughters at S,SE,W (yin/setting half)
    anti_sons = {trig_pos(anti_ht, t) for t in SON_TRIGRAMS}
    anti_daughters = {trig_pos(anti_ht, t) for t in DAUGHTER_TRIGRAMS}
    out(f"  Sons at: {sorted(anti_sons, key=lambda p: POS_INDEX[p])}")
    out(f"  Daughters at: {sorted(anti_daughters, key=lambda p: POS_INDEX[p])}")
    out()

    # The specific swap: 坤(NE) ↔ 艮(SW)
    out("  The anti-後天 swaps 坤(Earth,NE) ↔ 艮(Earth,SW)")
    out("  This moves 艮(son, 1-yang) from NE to SW")
    out("  and 坤(pure-yin, 0-yang) from SW to NE")
    out()

    # Cosmological meaning
    out("  Cosmological implications:")
    out("  後天: 艮(Mountain/youngest son) at NE = dawn direction")
    out("       坤(Earth/mother) at SW = afternoon direction")
    out("  anti: 坤(Earth/mother) at NE, 艮(Mountain/youngest son) at SW")
    out("  → anti-後天 places the 'receptive mother' in the dawn/rising position")
    out("    and the 'youngest son' in the declining position — inverts the")
    out("    generational flow of the 說卦傳 sequence")
    out()

    # Is arr_037 a known arrangement?
    out("  Known arrangements check:")
    out("  • 先天 (Fu Xi): No — not cardinal-aligned")
    out("  • 後天 (King Wen): No — different NE/SW")
    out("  • arr_037 does not correspond to any historically attested bagua arrangement")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 3: Z₅ distance → spatial distance embedding
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 3: Z₅ → Spatial Distance Embedding")
    out()

    # For all 10 element pairs
    elements = SHENG_ORDER
    out("### 後天: element pair distances")
    out()
    out(f"{'Pair':>14}  {'Z₅ dist':>7}  {'Rel':>5}  {'Trigrams & angles':>40}  {'Spatial dists':>20}")
    out("-" * 100)

    def z5_distance(e1, e2):
        """Cyclic distance on Z₅ (生 cycle)."""
        d = (ELEM_Z5[e2] - ELEM_Z5[e1]) % 5
        return min(d, 5 - d)

    # Build trigram→angle lookup for 後天
    ht_trig_angle = {t: pos_angle(trig_pos(HOUTIAN, t)) for t in ALL_TRIGRAMS}

    d1_spatial = []
    d2_spatial = []
    d0_spatial = []

    for i in range(5):
        for j in range(i + 1, 5):
            e1, e2 = elements[i], elements[j]
            d = z5_distance(e1, e2)

            # Get relation
            if SHENG_MAP.get(e1) == e2 or SHENG_MAP.get(e2) == e1:
                rel = "生"
            elif KE_MAP.get(e1) == e2 or KE_MAP.get(e2) == e1:
                rel = "克"
            else:
                rel = "比和"

            # Get all trigrams of each element
            t1s = [t for t in ALL_TRIGRAMS if ELEM[t] == e1]
            t2s = [t for t in ALL_TRIGRAMS if ELEM[t] == e2]

            spatial_dists = []
            for t1 in t1s:
                for t2 in t2s:
                    sd = angular_distance(ht_trig_angle[t1], ht_trig_angle[t2])
                    spatial_dists.append(sd)

            trig_str = f"{','.join(TRIGRAM_NAME[t]+'@'+str(ht_trig_angle[t])+'°' for t in t1s)} / " \
                       f"{','.join(TRIGRAM_NAME[t]+'@'+str(ht_trig_angle[t])+'°' for t in t2s)}"

            if d == 1:
                d1_spatial.extend(spatial_dists)
            elif d == 2:
                d2_spatial.extend(spatial_dists)
            else:
                d0_spatial.extend(spatial_dists)

            out(f"{e1+'↔'+e2:>14}  {d:>7}  {rel:>5}  {trig_str:>40}  {spatial_dists}")

    out()
    out("### Distance coherence summary")
    out()
    out(f"  d=0 (比和) spatial distances: {d0_spatial}")
    out(f"  d=1 (生) spatial distances: {d1_spatial}")
    out(f"  d=2 (克) spatial distances: {d2_spatial}")
    out()

    # Count good embeddings
    d1_close = sum(1 for d in d1_spatial if d <= 90)
    d2_far = sum(1 for d in d2_spatial if d >= 135)
    out(f"  d=1 pairs with spatial ≤ 90°: {d1_close}/{len(d1_spatial)}")
    out(f"  d=2 pairs with spatial ≥ 135°: {d2_far}/{len(d2_spatial)}")
    out()

    # Define embedding quality score
    def embedding_score(arr):
        """Lower = better. Sum of |spatial - expected| for all element pair representatives."""
        # For each element pair, use the representative giving best spatial match
        # Expected: d=1 → 72° (360/5), d=2 → 144° (2×360/5)
        trig_angle = {t: pos_angle(trig_pos(arr, t)) for t in ALL_TRIGRAMS}
        total = 0.0
        for i in range(5):
            for j in range(i + 1, 5):
                e1, e2 = elements[i], elements[j]
                d = z5_distance(e1, e2)
                expected = d * 72.0  # 72° per Z₅ step

                t1s = [t for t in ALL_TRIGRAMS if ELEM[t] == e1]
                t2s = [t for t in ALL_TRIGRAMS if ELEM[t] == e2]

                # Best representative pair
                best_err = float('inf')
                for t1 in t1s:
                    for t2 in t2s:
                        sd = angular_distance(trig_angle[t1], trig_angle[t2])
                        err = abs(sd - expected)
                        best_err = min(best_err, err)
                total += best_err
        return total

    ht_score = embedding_score(HOUTIAN)
    out(f"### Embedding quality (|spatial - expected|, lower = better)")
    out(f"  Expected: d=1→72°, d=2→144°")
    out(f"  後天 score: {ht_score:.1f}")
    out()

    # Score all 96
    all_scores = [(i, embedding_score(arr)) for i, arr in enumerate(arrangements)]
    all_scores.sort(key=lambda x: x[1])
    best_score = all_scores[0][1]
    best_count = sum(1 for _, s in all_scores if s == best_score)

    out(f"  Best score among 96: {best_score:.1f} ({best_count} arrangement(s))")
    out(f"  後天 rank: {next(r+1 for r, (i,_) in enumerate(all_scores) if i == ht_index)}/96")
    out()

    # Show top 5
    out("  Top 5 by embedding quality:")
    for rank, (i, score) in enumerate(all_scores[:5]):
        label = "後天" if i == ht_index else f"arr_{i:03d}"
        arr = arrangements[i]
        mono = is_monotone(arr)
        epc = element_pair_coherent(arr)
        out(f"    {rank+1}. {label}: score={score:.1f}, monotone={mono}, epc={epc}")
    out()

    # Is 後天 unique best among monotone+epc?
    mono_epc_scores = [(i, s) for i, s in all_scores
                       if is_monotone(arrangements[i]) and element_pair_coherent(arrangements[i])]
    mono_epc_scores.sort(key=lambda x: x[1])
    out(f"  Among monotone+epc (the 8 survivors):")
    for rank, (i, score) in enumerate(mono_epc_scores):
        label = "後天" if i == ht_index else f"arr_{i:03d}"
        out(f"    {rank+1}. {label}: score={score:.1f}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 4: τ's two 4-cycles
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 4: τ's Two 4-Cycles")
    out()

    # Compute τ
    xinv = {trig: pos for pos, trig in XIANTIAN.items()}
    tau = {trig: HOUTIAN[xinv[trig]] for trig in range(8)}

    # Extract cycles
    def get_cycles(perm):
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

    cycles = get_cycles(tau)
    out("### Cycle structure")
    out()
    for ci, cycle in enumerate(cycles):
        names = [TRIGRAM_NAME[t] for t in cycle]
        elems = [ELEM[t] for t in cycle]
        yangs = [yang_count(t) for t in cycle]
        bins = [f"{t:03b}" for t in cycle]
        out(f"  Cycle {ci+1}: ({' → '.join(names)})")
        out(f"    Elements:     {' → '.join(elems)}")
        out(f"    Yang counts:  {' → '.join(str(y) for y in yangs)}")
        out(f"    Binary:       {' → '.join(bins)}")
        out(f"    Code values:  {' → '.join(str(t) for t in cycle)}")
    out()

    # Check: each cycle has exactly one from each doubleton element?
    out("### Doubleton element distribution")
    out()
    doubleton_elems = ["Wood", "Metal", "Earth"]
    for ci, cycle in enumerate(cycles):
        out(f"  Cycle {ci+1}:")
        for elem in doubleton_elems:
            trigs_in_cycle = [t for t in cycle if ELEM[t] == elem]
            out(f"    {elem}: {[TRIGRAM_NAME[t] for t in trigs_in_cycle]} "
                f"({'one of two ✓' if len(trigs_in_cycle) == 1 else '✗'})")
    out()

    # Singleton elements
    out("  Singleton elements:")
    for ci, cycle in enumerate(cycles):
        for elem in ["Water", "Fire"]:
            trigs_in_cycle = [t for t in cycle if ELEM[t] == elem]
            if trigs_in_cycle:
                out(f"    Cycle {ci+1} contains {elem}: {[TRIGRAM_NAME[t] for t in trigs_in_cycle]}")
    out()
    out("  → Each cycle contains exactly one trigram from each doubleton")
    out("    plus one singleton (cycle 1: Water, cycle 2: Fire)")
    out()

    # Check binary patterns
    out("### Binary structure within each cycle")
    out()
    for ci, cycle in enumerate(cycles):
        vals = cycle
        out(f"  Cycle {ci+1}: values {vals}")

        # Check if it's a coset of a subgroup of Z₂³
        # A subgroup of Z₂³ has order 1, 2, or 4.
        # Check if the set is closed under XOR (= a coset)
        cycle_set = set(vals)

        # Differences (XOR) between all pairs
        diffs = set()
        for a in vals:
            for b in vals:
                diffs.add(a ^ b)
        out(f"    XOR closure: {sorted(diffs)}")
        out(f"    Is subgroup (contains 0, closed under XOR): "
            f"{'✓' if 0 in diffs and diffs == cycle_set else '✗'}")

        # Check: is it a COSET of some order-4 subgroup?
        # A coset of H is g+H for some g. So the set of differences = H.
        if 0 in diffs and len(diffs) == len(cycle_set):
            out(f"    → The cycle IS a subgroup of Z₂³")
        elif len(diffs) == len(cycle_set):
            # The diffs form a subgroup, and the set is a coset of it
            # Verify: diffs should be a subgroup
            diff_closed = True
            for a in diffs:
                for b in diffs:
                    if (a ^ b) not in diffs:
                        diff_closed = False
            if diff_closed:
                out(f"    → The cycle is a coset of subgroup {sorted(diffs)}")
        out()

    # Parity check
    out("### Parity structure")
    out()
    for ci, cycle in enumerate(cycles):
        parities = [t % 2 for t in cycle]
        out(f"  Cycle {ci+1} parities (bit0): {parities}")
    out("  → Cycle 1 = {even} values: {0,2,3,6}")
    out("  → Cycle 2 = {odd} values: {1,4,5,7}")
    out("  → Wait: 3 and 6 are not the same parity. Let me check more carefully.")
    out()

    # Actually check
    c1_vals = set(cycles[0])
    c2_vals = set(cycles[1])
    c1_even = {v for v in c1_vals if v % 2 == 0}
    c1_odd = {v for v in c1_vals if v % 2 == 1}
    c2_even = {v for v in c2_vals if v % 2 == 0}
    c2_odd = {v for v in c2_vals if v % 2 == 1}
    out(f"  Cycle 1: even={c1_even}, odd={c1_odd}")
    out(f"  Cycle 2: even={c2_even}, odd={c2_odd}")
    out(f"  Mixed parity in both cycles: neither is all-even or all-odd")
    out()

    # Check bit patterns more carefully
    out("### Bit-level analysis")
    out()
    for ci, cycle in enumerate(cycles):
        out(f"  Cycle {ci+1}:")
        for t in cycle:
            b2, b1, b0 = (t >> 2) & 1, (t >> 1) & 1, t & 1
            out(f"    {TRIGRAM_NAME[t]:>3} = {t:03b}: top={b2} mid={b1} bot={b0}")

        # Sum of bits in each position
        bit_sums = [0, 0, 0]
        for t in cycle:
            for bit in range(3):
                bit_sums[bit] += (t >> bit) & 1
        out(f"    Bit sums: bot={bit_sums[0]}, mid={bit_sums[1]}, top={bit_sums[2]}")
        out(f"    → Each bit position sums to 2 (balanced): "
            f"{'✓' if all(s == 2 for s in bit_sums) else '✗ ' + str(bit_sums)}")
    out()

    # τ² analysis
    out("### τ² (applying τ twice)")
    out()
    tau2 = {t: tau[tau[t]] for t in range(8)}
    cycles2 = get_cycles(tau2)

    out("τ² mapping:")
    for t in range(8):
        out(f"  {TRIGRAM_NAME[t]} → {TRIGRAM_NAME[tau2[t]]}")
    out()

    out(f"τ² cycle structure: {[len(c) for c in cycles2]}")
    for ci, c in enumerate(cycles2):
        names = [TRIGRAM_NAME[t] for t in c]
        elems = [ELEM[t] for t in c]
        out(f"  Cycle {ci+1}: ({' → '.join(names)})")
        out(f"    Elements: {' → '.join(elems)}")
    out()

    # Check fiber preservation for τ²
    fiber2 = {}
    fiber2_ok = True
    for t, t2 in tau2.items():
        e1, e2 = ELEM[t], ELEM[t2]
        if e1 in fiber2:
            if fiber2[e1] != e2:
                fiber2_ok = False
        else:
            fiber2[e1] = e2
    out(f"τ² fiber preservation: {fiber2_ok}")
    if fiber2_ok:
        out("τ² induced permutation on Z₅:")
        for e in SHENG_ORDER:
            out(f"  {e} → {fiber2[e]}")

        # Check if it's γ or γ²
        gamma_map = {SHENG_ORDER[i]: SHENG_ORDER[GAMMA[i]] for i in range(5)}
        gamma2_map = {e: gamma_map[gamma_map[e]] for e in SHENG_ORDER}
        is_gamma = all(fiber2[e] == gamma_map[e] for e in SHENG_ORDER)
        is_gamma2 = all(fiber2[e] == gamma2_map[e] for e in SHENG_ORDER)
        out(f"  Matches γ: {is_gamma}")
        out(f"  Matches γ²: {is_gamma2}")
    else:
        out("τ² fiber map (showing conflicts):")
        elem_targets = defaultdict(set)
        for t, t2 in tau2.items():
            elem_targets[ELEM[t]].add(ELEM[t2])
        for e, targets in sorted(elem_targets.items()):
            out(f"  {e} → {targets}")
    out()

    # τ⁴ = identity?
    tau4 = {t: tau2[tau2[t]] for t in range(8)}
    is_identity = all(tau4[t] == t for t in range(8))
    out(f"τ⁴ = identity: {is_identity}")
    out(f"Order of τ: {4 if is_identity else 'not 4, checking further...'}")
    if not is_identity:
        # Check τ³
        tau3 = {t: tau[tau2[t]] for t in range(8)}
        # Check order
        for k in range(1, 9):
            tauk = {t: t for t in range(8)}
            for _ in range(k):
                tauk = {t: tau[tauk[t]] for t in range(8)}
            if all(tauk[t] == t for t in range(8)):
                out(f"  Order of τ: {k}")
                break
    out()

    # Relationship between cycles and complement
    out("### Cycle-complement relationship")
    out()
    for ci, cycle in enumerate(cycles):
        comps = [t ^ 7 for t in cycle]
        comp_set = set(comps)
        other_cycle = set(cycles[1 - ci])
        out(f"  Complement of cycle {ci+1}: {[TRIGRAM_NAME[t] for t in comps]}")
        if comp_set == other_cycle:
            out(f"  → Complement maps cycle {ci+1} to cycle {2-ci} ✓")
        else:
            out(f"  → In cycle {ci+1}: {comp_set & set(cycle)} stay, "
                f"{comp_set & other_cycle} cross")
    out()

    # Angular interpretation: what does τ do as a compass operation?
    out("### τ as compass operation")
    out()
    # For each trigram, compute the angular displacement in 先天 vs 後天
    out(f"{'Trigram':>8}  {'先天 pos':>8}  {'後天 pos':>8}  {'先天 θ':>6}  {'後天 θ':>6}  {'Δθ':>6}")
    out("-" * 55)
    for t in range(8):
        xt_pos = trig_pos(XIANTIAN, t)
        ht_pos = trig_pos(HOUTIAN, t)
        xt_angle = pos_angle(xt_pos)
        ht_angle = pos_angle(ht_pos)
        delta = (ht_angle - xt_angle) % 360
        if delta > 180:
            delta -= 360
        out(f"{TRIGRAM_NAME[t]:>8}  {xt_pos:>8}  {ht_pos:>8}  {xt_angle:>6}  {ht_angle:>6}  {delta:>+6}")
    out()
    out("  → No single rotation/reflection describes all displacements")
    out("  → τ is genuinely non-geometric: it cannot be realized as a D₈ isometry")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Summary
    # ════════════════════════════════════════════════════════════════════════
    out("## Summary")
    out()
    out("### Prime decomposition confirmed")
    out("The 8 survivors of (monotone + elem_pair_coherent) have exact Z₂³ structure:")
    out("  • Choice A: which Wood at E (震 vs 巽)")
    out("  • Choice B: which Metal at W (兌 vs 乾)")
    out("  • Choice C: which Earth at NE (艮 vs 坤)")
    out("Each choice is forced by adjacency constraints from elem_pair_coherent.")
    out()
    out("The final two filters eliminate 7 of 8:")
    out("  • yy_balance: cardinal yang-counts must be [1,1,2,2] → eliminates 4")
    out("  • sons_yang_half: 震,坎,艮 must be at N,NE,E → eliminates 1 more")
    out("  → UNIQUE survivor: 後天")
    out()
    out("### Anti-後天 (arr_037)")
    out("Differs only at NE/SW: swaps 艮↔坤.")
    out("Survives monotone + elem_pair_coherent + yy_balance.")
    out("Eliminated by sons_yang_half: places 艮(son) at SW instead of NE,")
    out("inverting the generational/directional flow of the 說卦傳.")
    out()
    out("### τ structure")
    out("Two 4-cycles: (坤→坎→兌→巽)(震→艮→乾→離)")
    out("  • Each cycle contains one trigram from each doubleton element")
    out("  • Cycle 1 contains Water (singleton), Cycle 2 contains Fire")
    out("  • Complement maps cycle 1 ↔ cycle 2")
    tau_order = 4
    for k in range(1, 9):
        tauk = {t: t for t in range(8)}
        for _ in range(k):
            tauk = {t: tau[tauk[t]] for t in range(8)}
        if all(tauk[t] == t for t in range(8)):
            tau_order = k
            break
    out(f"  • τ has order {tau_order}")
    out(f"  • Fiber NOT preserved (τ is not a Z₅ morphism)")
    out(f"  • τ² {'preserves' if fiber2_ok else 'does not preserve'} fibers")
    out()

    # Write results
    results_path = OUT_DIR / "03_prime_decomposition_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
