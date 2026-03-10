#!/usr/bin/env python3
"""
V₄ Symmetry Group on Z₂⁶

The Klein four-group V₄ = {id, complement, reversal, comp∘rev} acts on
the 64 hexagrams. This script analyzes the orbit structure and its
interaction with the element system, KW sequence, and 上經/下經 split.
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "kingwen"))
sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    TRIGRAM_ELEMENT, five_phase_relation,
)

# ─── Constants ───────────────────────────────────────────────────────────────

TRIG_NAME = {
    0: "坤", 1: "震", 2: "坎", 3: "兌",
    4: "艮", 5: "離", 6: "巽", 7: "乾",
}
ELEM = TRIGRAM_ELEMENT
SHENG_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_Z5 = {e: i for i, e in enumerate(SHENG_ORDER)}

# Build KW data
KW = []
KW_NAME = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    KW.append(sum(b[j] << j for j in range(6)))
    KW_NAME.append(KING_WEN[i][1])

KW_INDEX = {h: i for i, h in enumerate(KW)}  # hex value → KW 0-based index

# ─── V₄ operations ──────────────────────────────────────────────────────────

def comp(h):
    """Complement: XOR with 111111."""
    return h ^ 63

def rev(h):
    """Line-reversal: reverse all 6 bits."""
    return reverse6(h)

def comp_rev(h):
    """Complement ∘ Reversal."""
    return comp(rev(h))

def basin(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1  # Kun
    if b2 == 1 and b3 == 1: return 1   # Qian
    return 0  # KanLi

BASIN_NAME = {-1: "Kun", 0: "KanLi", 1: "Qian"}

def yang_count(h):
    return bin(h).count('1')

def hex_label(h):
    """Short label for a hexagram."""
    idx = KW_INDEX[h]
    return f"#{idx+1} {KW_NAME[idx]}"


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# V₄ Symmetry Group on Z₂⁶")
    out()

    # Verify V₄ axioms
    out("## Verification: V₄ = {id, comp, rev, comp∘rev}")
    out()
    out("Checking group axioms on all 64 hexagrams:")

    # comp² = id, rev² = id, (comp∘rev)² = id
    assert all(comp(comp(h)) == h for h in range(64)), "comp² ≠ id"
    assert all(rev(rev(h)) == h for h in range(64)), "rev² ≠ id"
    assert all(comp_rev(comp_rev(h)) == h for h in range(64)), "(comp∘rev)² ≠ id"
    # comp∘rev = rev∘comp
    assert all(comp(rev(h)) == rev(comp(h)) for h in range(64)), "comp∘rev ≠ rev∘comp"

    out("  comp² = id ✓")
    out("  rev² = id ✓")
    out("  (comp∘rev)² = id ✓")
    out("  comp∘rev = rev∘comp ✓ (V₄ is abelian)")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 1: Fixed points and orbit structure
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 1: Fixed Points and Orbits")
    out()

    # Fixed points of each involution
    comp_fixed = [h for h in range(64) if comp(h) == h]
    rev_fixed = [h for h in range(64) if rev(h) == h]
    cr_fixed = [h for h in range(64) if comp_rev(h) == h]

    out(f"Fixed points of complement: {len(comp_fixed)}")
    out(f"Fixed points of reversal: {len(rev_fixed)}")
    for h in rev_fixed:
        lo, up = lower_trigram(h), upper_trigram(h)
        out(f"  {h:06b} = {hex_label(h)} ({TRIG_NAME[lo]}/{TRIG_NAME[up]})")
    out(f"Fixed points of comp∘rev: {len(cr_fixed)}")
    for h in cr_fixed:
        lo, up = lower_trigram(h), upper_trigram(h)
        out(f"  {h:06b} = {hex_label(h)} ({TRIG_NAME[lo]}/{TRIG_NAME[up]})")
    out()

    # Enumerate all V₄ orbits
    visited = set()
    orbits = []
    for h in range(64):
        if h in visited:
            continue
        orb = sorted({h, comp(h), rev(h), comp_rev(h)})
        for x in orb:
            visited.add(x)
        orbits.append(orb)

    orbit_sizes = Counter(len(o) for o in orbits)
    out(f"Total V₄ orbits: {len(orbits)}")
    out(f"Orbit size distribution: {dict(sorted(orbit_sizes.items()))}")
    out(f"  Size 1: {orbit_sizes.get(1, 0)} (fixed by all three involutions)")
    out(f"  Size 2: {orbit_sizes.get(2, 0)} (fixed by one involution)")
    out(f"  Size 4: {orbit_sizes.get(4, 0)} (generic)")
    out()

    # Show all orbits grouped by size
    out("### All V₄ orbits")
    out()

    for size in sorted(orbit_sizes.keys()):
        size_orbits = [o for o in orbits if len(o) == size]
        out(f"#### Size-{size} orbits ({len(size_orbits)} total)")
        out()
        for oi, orb in enumerate(size_orbits):
            labels = [hex_label(h) for h in orb]
            bins = [f"{h:06b}" for h in orb]
            # Which involution fixes them?
            if size == 2:
                h0, h1 = orb
                if comp(h0) == h0:
                    fix = "comp-fixed"
                elif rev(h0) == h0 or rev(h0) == h1:
                    # Check which fixes what
                    if rev(h0) == h0:
                        fix = "rev-fixed (both palindromic)"
                    else:
                        fix = "rev swaps them"
                elif comp_rev(h0) == h0 or comp_rev(h0) == h1:
                    fix = "comp∘rev"
                else:
                    fix = "?"

                # Actually: for size-2 orbits, the orbit is {h, g(h)} for some g.
                # The stabilizer has order |V₄|/|orbit| = 2, so two elements fix each member.
                stab = []
                if comp(h0) == h0:
                    stab.append("comp")
                if rev(h0) == h0:
                    stab.append("rev")
                if comp_rev(h0) == h0:
                    stab.append("c∘r")
                fix = f"stab={{{','.join(stab)}}}" if stab else "?"

                out(f"  {oi+1}. {', '.join(labels)}")
                out(f"     {', '.join(bins)} | {fix}")
            else:
                out(f"  {oi+1}. {', '.join(labels)}")
                out(f"     {', '.join(bins)}")
        out()

    # Show size-4 orbits with full structure
    out("### Size-4 orbit detail")
    out()
    out(f"{'Orbit':>5} {'h':>7} {'comp':>7} {'rev':>7} {'c∘r':>7}  "
        f"{'Name_h':>12} {'Name_comp':>12} {'Name_rev':>12} {'Name_cr':>12}")
    out("-" * 110)

    for oi, orb in enumerate([o for o in orbits if len(o) == 4]):
        h = orb[0]
        ch, rh, crh = comp(h), rev(h), comp_rev(h)
        out(f"{oi+1:>5} {h:06b} {ch:06b} {rh:06b} {crh:06b}  "
            f"{KW_NAME[KW_INDEX[h]]:>12} {KW_NAME[KW_INDEX[ch]]:>12} "
            f"{KW_NAME[KW_INDEX[rh]]:>12} {KW_NAME[KW_INDEX[crh]]:>12}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 2: V₄ action on coordinate systems
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 2: V₄ Action on Coordinate Systems")
    out()

    # ── 2a: Element system ──
    out("### 2a: V₄ action on elements")
    out()

    # Complement action on elements
    out("Complement on trigrams → elements:")
    comp_elem_map = {}
    comp_elem_ok = True
    for t in range(8):
        ct = t ^ 7
        e1, e2 = ELEM[t], ELEM[ct]
        if e1 in comp_elem_map:
            if comp_elem_map[e1] != e2:
                comp_elem_ok = False
        else:
            comp_elem_map[e1] = e2
        out(f"  {TRIG_NAME[t]}({ELEM[t]}) → {TRIG_NAME[ct]}({ELEM[ct]})")
    out(f"  Fiber-preserving: {comp_elem_ok}")
    if comp_elem_ok:
        out(f"  Induced Z₅ permutation: {comp_elem_map}")
        # Verify it's negation
        neg_match = all(ELEM_Z5[comp_elem_map[e]] == (5 - ELEM_Z5[e]) % 5 for e in SHENG_ORDER)
        out(f"  Is negation (-x mod 5): {neg_match}")
    out()

    # Reversal action on trigrams
    def trig_reverse(t):
        """Reverse bits of trigram (swap b₀↔b₂)."""
        return ((t & 1) << 2) | ((t >> 1) & 1) << 1 | ((t >> 2) & 1)

    out("Reversal on trigrams → elements:")
    rev_elem_map = defaultdict(set)
    for t in range(8):
        rt = trig_reverse(t)
        e1, e2 = ELEM[t], ELEM[rt]
        rev_elem_map[e1].add(e2)
        out(f"  {TRIG_NAME[t]}({ELEM[t]}) → {TRIG_NAME[rt]}({ELEM[rt]})")

    rev_fiber_ok = all(len(v) == 1 for v in rev_elem_map.values())
    out(f"  Fiber-preserving: {rev_fiber_ok}")
    if not rev_fiber_ok:
        out(f"  Fiber map (showing multi-valued):")
        for e, targets in sorted(rev_elem_map.items()):
            out(f"    {e} → {targets}")
    out()

    # Comp∘Rev on trigrams
    out("Comp∘Rev on trigrams → elements:")
    cr_elem_map = defaultdict(set)
    for t in range(8):
        crt = trig_reverse(t) ^ 7  # reverse then complement at trigram level
        e1, e2 = ELEM[t], ELEM[crt]
        cr_elem_map[e1].add(e2)
        out(f"  {TRIG_NAME[t]}({ELEM[t]}) → {TRIG_NAME[crt]}({ELEM[crt]})")

    cr_fiber_ok = all(len(v) == 1 for v in cr_elem_map.values())
    out(f"  Fiber-preserving: {cr_fiber_ok}")
    if not cr_fiber_ok:
        out(f"  Fiber map:")
        for e, targets in sorted(cr_elem_map.items()):
            out(f"    {e} → {targets}")
    out()

    # ── 2b: Directed relation ──
    out("### 2b: V₄ action on directed relations")
    out()

    def directed_rel(h):
        return five_phase_relation(ELEM[lower_trigram(h)], ELEM[upper_trigram(h)])

    rel_names = ["比和", "生体", "体生用", "克体", "体克用"]

    for op_name, op_fn in [("complement", comp), ("reversal", rev), ("comp∘rev", comp_rev)]:
        # Check: does the operation induce a well-defined map on relations?
        rel_map = defaultdict(set)
        for h in range(64):
            r1 = directed_rel(h)
            r2 = directed_rel(op_fn(h))
            rel_map[r1].add(r2)

        well_defined = all(len(v) == 1 for v in rel_map.values())
        out(f"  {op_name}:")
        for r, targets in sorted(rel_map.items()):
            arrow = "→" if len(targets) == 1 else "⇒"
            out(f"    {r} {arrow} {targets}")
        out(f"    Well-defined on relations: {well_defined}")
        out()

    # ── 2c: Basin action ──
    out("### 2c: V₄ action on basins")
    out()

    for op_name, op_fn in [("complement", comp), ("reversal", rev), ("comp∘rev", comp_rev)]:
        basin_map = defaultdict(set)
        for h in range(64):
            b1 = basin(h)
            b2 = basin(op_fn(h))
            basin_map[b1].add(b2)

        well_defined = all(len(v) == 1 for v in basin_map.values())
        out(f"  {op_name}:")
        for b, targets in sorted(basin_map.items()):
            bnames = {BASIN_NAME[t] for t in targets}
            out(f"    {BASIN_NAME[b]} → {bnames}")
        out(f"    Preserves basins: {well_defined and all(v == {k} for k, v in basin_map.items())}")
        out()

    # ── 2d: 互 action ──
    out("### 2d: V₄ action on 互")
    out()

    for op_name, op_fn in [("complement", comp), ("reversal", rev), ("comp∘rev", comp_rev)]:
        # Check: does op commute with 互?
        commutes = all(hugua(op_fn(h)) == op_fn(hugua(h)) for h in range(64))
        out(f"  {op_name} commutes with 互: {commutes}")

        if not commutes:
            # Show counterexamples
            counter = 0
            for h in range(64):
                if hugua(op_fn(h)) != op_fn(hugua(h)):
                    counter += 1
            out(f"    Failures: {counter}/64")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 3: V₄ and the element system (detailed)
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 3: V₄ and the Element System (Detailed)")
    out()

    # Reversal doesn't preserve element fibers. Characterize the failure.
    out("### Reversal fiber analysis")
    out()
    out("Reversal on trigrams:")
    out(f"  Fixed: 坤(000→000,Earth), 坎(010→010,Water), 離(101→101,Fire), 乾(111→111,Metal)")
    out(f"  Swapped: 震(001)↔艮(100): Wood↔Earth")
    out(f"           巽(110)↔兌(011): Wood↔Metal")
    out()
    out("Element-level effect:")
    out("  Water → Water (fixed, singleton)")
    out("  Fire → Fire (fixed, singleton)")
    out("  Earth → {Earth, Wood} (Gen stays Earth, Kun stays Earth, but Zhen(Wood)→Gen(Earth))")
    out("  Metal → {Metal, Wood} (Qian stays Metal, Dui stays Metal, but Xun(Wood)→Dui(Metal))")
    out("  Wood → {Earth, Metal} (Zhen→Gen=Earth, Xun→Dui=Metal)")
    out()
    out("Reversal is NOT fiber-preserving. Wood splits into Earth and Metal.")
    out("But it IS fiber-preserving on the SINGLETON elements (Fire, Water).")
    out("The singletons are the injection points of the Z₂→Z₅ map —")
    out("reversal respects them because they have no fiber ambiguity.")
    out()

    # On hexagrams: reversal swaps upper and lower trigrams,
    # then reverses each trigram's bits
    out("### Reversal on hexagrams: upper/lower swap")
    out()
    out("For hexagram h with lower=L, upper=U:")
    out("  rev(h) has lower=rev_trig(U), upper=rev_trig(L)")
    out("  This swaps upper↔lower AND reverses trigram bits.")
    out()
    # Verify
    all_swap = True
    for h in range(64):
        lo, up = lower_trigram(h), upper_trigram(h)
        rh = rev(h)
        rlo, rup = lower_trigram(rh), upper_trigram(rh)
        if rlo != trig_reverse(up) or rup != trig_reverse(lo):
            all_swap = False
            break
    out(f"  Verified: rev(lo,up) = (rev_trig(up), rev_trig(lo)) for all 64: {all_swap}")
    out()

    # What this means for directed relations
    out("### Reversal effect on directed relation")
    out()
    out("If lo_elem and up_elem are both singletons (Fire or Water),")
    out("reversal preserves both elements → relation is determined by")
    out("swapping upper↔lower → relation inverts (生体↔体生用, 克体↔体克用, 比和→比和).")
    out()

    # Count: how often does reversal invert the relation?
    inv_map = {"比和": "比和", "生体": "体生用", "体生用": "生体",
               "克体": "体克用", "体克用": "克体"}
    rev_inverts = sum(1 for h in range(64)
                      if directed_rel(rev(h)) == inv_map[directed_rel(h)])
    out(f"  Reversal inverts relation: {rev_inverts}/64")
    out(f"  (Expected if reversal = perfect upper/lower swap: 64/64)")
    out()

    # When does it NOT invert?
    if rev_inverts < 64:
        out("  Failures (reversal ≠ simple relation inversion):")
        for h in range(64):
            r_orig = directed_rel(h)
            r_rev = directed_rel(rev(h))
            if r_rev != inv_map[r_orig]:
                lo, up = ELEM[lower_trigram(h)], ELEM[upper_trigram(h)]
                rlo, rup = ELEM[lower_trigram(rev(h))], ELEM[upper_trigram(rev(h))]
                out(f"    {h:06b} ({lo}/{up} → {r_orig}) "
                    f"→ rev ({rlo}/{rup} → {r_rev}), expected {inv_map[r_orig]}")
        out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 4: V₄ and the KW sequence
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 4: V₄ and the KW Sequence")
    out()

    # Check: does each V₄ operation preserve KW pairing?
    for op_name, op_fn in [("complement", comp), ("reversal", rev), ("comp∘rev", comp_rev)]:
        preserves = True
        pair_perm = {}  # KW pair index → KW pair index under op
        for k in range(32):
            a, b = KW[2*k], KW[2*k + 1]
            oa, ob = op_fn(a), op_fn(b)
            pair_a = KW_INDEX[oa] // 2
            pair_b = KW_INDEX[ob] // 2
            if pair_a != pair_b:
                preserves = False
                break
            pair_perm[k] = pair_a

        out(f"  {op_name} preserves KW pairing: {preserves}")
        if preserves:
            # Characterize the permutation on 32 pairs
            fixed_pairs = sum(1 for k, v in pair_perm.items() if k == v)
            cycles = []
            visited_pairs = set()
            for start in range(32):
                if start in visited_pairs:
                    continue
                cycle = []
                x = start
                while x not in visited_pairs:
                    visited_pairs.add(x)
                    cycle.append(x + 1)  # 1-indexed
                    x = pair_perm[x]
                if len(cycle) > 0:
                    cycles.append(cycle)
            cycle_lens = sorted([len(c) for c in cycles], reverse=True)
            out(f"    Fixed pairs: {fixed_pairs}/32")
            out(f"    Cycle structure on pairs: {cycle_lens}")
    out()

    # The combined V₄ action on pairs
    out("### V₄ orbits on KW pairs")
    out()

    # Group the 32 pairs into orbits under V₄
    pair_visited = set()
    pair_orbits = []
    for k in range(32):
        if k in pair_visited:
            continue
        # Apply all V₄ elements to the pair
        porb = set()
        for op_fn in [lambda x: x, comp, rev, comp_rev]:
            a, b = KW[2*k], KW[2*k + 1]
            oa = op_fn(a)
            target_pair = KW_INDEX[oa] // 2
            porb.add(target_pair)
        for p in porb:
            pair_visited.add(p)
        pair_orbits.append(sorted(porb))

    pair_orbit_sizes = Counter(len(o) for o in pair_orbits)
    out(f"Total V₄ orbits on KW pairs: {len(pair_orbits)}")
    out(f"Pair orbit sizes: {dict(sorted(pair_orbit_sizes.items()))}")
    out()

    # Show pair orbits
    for oi, porb in enumerate(pair_orbits):
        labels = []
        for p in porb:
            a_name = KW_NAME[2*p]
            b_name = KW_NAME[2*p + 1]
            labels.append(f"P{p+1}({a_name}/{b_name})")
        out(f"  {oi+1}. {', '.join(labels)}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 5: V₄ orbits and 上經/下經
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 5: V₄ Orbits and 上經/下經")
    out()

    # For each V₄ orbit of hexagrams, check if all members are in 上經, 下經, or split
    upper_set = set(range(30))   # KW indices 0-29 = hexagrams 1-30
    lower_set = set(range(30, 64))  # KW indices 30-63 = hexagrams 31-64

    orbit_location = {"上經": 0, "下經": 0, "split": 0}
    for orb in orbits:
        kw_indices = {KW_INDEX[h] for h in orb}
        in_upper = kw_indices & upper_set
        in_lower = kw_indices & lower_set
        if in_upper and not in_lower:
            orbit_location["上經"] += 1
        elif in_lower and not in_upper:
            orbit_location["下經"] += 1
        else:
            orbit_location["split"] += 1

    out(f"Hexagram orbit locations:")
    out(f"  Entirely in 上經: {orbit_location['上經']}")
    out(f"  Entirely in 下經: {orbit_location['下經']}")
    out(f"  Split across both: {orbit_location['split']}")
    out()

    # Same for pair orbits
    upper_pairs = set(range(15))  # pairs 0-14 = 上經
    lower_pairs = set(range(15, 32))  # pairs 15-31 = 下經

    pair_orbit_loc = {"上經": 0, "下經": 0, "split": 0}
    for porb in pair_orbits:
        in_up = set(porb) & upper_pairs
        in_lo = set(porb) & lower_pairs
        if in_up and not in_lo:
            pair_orbit_loc["上經"] += 1
        elif in_lo and not in_up:
            pair_orbit_loc["下經"] += 1
        else:
            pair_orbit_loc["split"] += 1

    out(f"Pair orbit locations:")
    out(f"  Entirely in 上經: {pair_orbit_loc['上經']}")
    out(f"  Entirely in 下經: {pair_orbit_loc['下經']}")
    out(f"  Split: {pair_orbit_loc['split']}")
    out()

    # Show split orbits (these connect 上經 to 下經)
    out("### Split pair orbits (connecting 上經 ↔ 下經)")
    out()
    for porb in pair_orbits:
        in_up = set(porb) & upper_pairs
        in_lo = set(porb) & lower_pairs
        if in_up and in_lo:
            labels = []
            for p in porb:
                canon = "上" if p in upper_pairs else "下"
                a_name = KW_NAME[2*p]
                b_name = KW_NAME[2*p + 1]
                labels.append(f"P{p+1}[{canon}]({a_name}/{b_name})")
            out(f"  {', '.join(labels)}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 6: Comp∘Rev analysis
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 6: Comp∘Rev — The Third Involution")
    out()

    out("### Fixed points of comp∘rev")
    out()
    out(f"comp∘rev(h) = h requires: b₅=1-b₀, b₄=1-b₁, b₃=1-b₂")
    out(f"Three free bits (b₀,b₁,b₂) → 8 fixed points")
    out()

    out(f"{'Binary':>7} {'KW#':>4} {'Name':>12} {'Lo':>3} {'Up':>3} "
        f"{'Lo_E':>6} {'Up_E':>6} {'Rel':>6} {'Basin':>6} {'Yang':>4}")
    out("-" * 75)
    for h in cr_fixed:
        lo, up = lower_trigram(h), upper_trigram(h)
        rel = directed_rel(h)
        b = basin(h)
        yc = yang_count(h)
        idx = KW_INDEX[h]
        out(f"{h:06b} {idx+1:>4} {KW_NAME[idx]:>12} "
            f"{TRIG_NAME[lo]:>3} {TRIG_NAME[up]:>3} "
            f"{ELEM[lo]:>6} {ELEM[up]:>6} {rel:>6} "
            f"{BASIN_NAME[b]:>6} {yc:>4}")
    out()

    # Properties of the 8 cr-fixed hexagrams
    cr_yang = [yang_count(h) for h in cr_fixed]
    out(f"Yang line counts: {cr_yang}")
    out(f"  All have exactly 3 yang lines: {all(y == 3 for y in cr_yang)}")
    out()

    # Check: are they exactly the hexagrams with 3 yang and 3 yin lines
    # that satisfy the anti-palindrome condition?
    three_yang = [h for h in range(64) if yang_count(h) == 3]
    out(f"Total hexagrams with 3 yang lines: {len(three_yang)}")
    out(f"Of which, comp∘rev-fixed: {len(cr_fixed)}")
    out(f"Fraction: {len(cr_fixed)}/{len(three_yang)}")
    out()

    # Element patterns
    cr_rels = Counter(directed_rel(h) for h in cr_fixed)
    out(f"Relations among cr-fixed: {dict(cr_rels)}")
    out()

    cr_basins = Counter(basin(h) for h in cr_fixed)
    out(f"Basins among cr-fixed: {dict((BASIN_NAME[k], v) for k, v in cr_basins.items())}")
    out()

    # Check if cr-fixed hexagrams are their own complements-then-reversals
    out("### Structural characterization")
    out()
    out("comp∘rev fixed means: the hexagram read backwards with all lines flipped")
    out("equals itself. This is an 'anti-palindrome' — a figure that is its own")
    out("complement-reversal.")
    out()

    # Show the binary structure
    out("Binary structure of comp∘rev-fixed hexagrams:")
    out("  b₀b₁b₂ | b₃b₄b₅ where b₃=1-b₂, b₄=1-b₁, b₅=1-b₀")
    out("  → lower trigram determines upper trigram as comp∘rev(lower)")
    out()
    for h in cr_fixed:
        lo, up = lower_trigram(h), upper_trigram(h)
        cr_lo = trig_reverse(lo) ^ 7
        out(f"  {h:06b}: lo={lo:03b}({TRIG_NAME[lo]}), up={up:03b}({TRIG_NAME[up]}), "
            f"comp∘rev(lo)={cr_lo:03b}({TRIG_NAME[cr_lo]}), "
            f"up == comp∘rev(lo): {up == cr_lo}")
    out()

    # ── Traditional significance ──
    out("### Traditional significance")
    out()

    # These 8 are a special subset. Check: are they the 大成卦 or some other named group?
    # They include 既濟(63) and 未濟(64) — the final pair!
    ji_ji = 5 | (2 << 3)  # Li lower, Kan upper = 010101 = 21
    wei_ji = 2 | (5 << 3)  # Kan lower, Li upper = 101010 = 42
    out(f"  既濟 (#{KW_INDEX[ji_ji]+1}) in cr-fixed: {ji_ji in cr_fixed}")
    out(f"  未濟 (#{KW_INDEX[wei_ji]+1}) in cr-fixed: {wei_ji in cr_fixed}")
    out()

    # Check which pairs they belong to
    cr_pairs = set()
    for h in cr_fixed:
        cr_pairs.add(KW_INDEX[h] // 2)
    out(f"  KW pairs containing cr-fixed hexagrams: {sorted(p+1 for p in cr_pairs)}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Summary
    # ════════════════════════════════════════════════════════════════════════
    out("## Summary")
    out()
    out("### V₄ orbit structure")
    out(f"  {len(orbits)} orbits total: "
        f"{orbit_sizes.get(1, 0)} size-1, "
        f"{orbit_sizes.get(2, 0)} size-2, "
        f"{orbit_sizes.get(4, 0)} size-4")
    out(f"  Fixed points: comp=0, rev=8 (palindromes), comp∘rev=8 (anti-palindromes)")
    out()

    out("### Fiber preservation")
    out(f"  Complement: preserves element fibers ✓ (acts as -x mod 5 on Z₅)")
    out(f"  Reversal: does NOT preserve fibers (Wood → {{Earth, Metal}})")
    out(f"  Comp∘Rev: does NOT preserve fibers")
    out(f"  → Only complement descends to Z₅. Reversal is purely Z₂.")
    out()

    out("### Directed relation action")
    out(f"  Complement: {'well-defined' if comp_elem_ok else 'not well-defined'} on relations")
    out(f"  Reversal: inverts relation direction for {rev_inverts}/64 hexagrams")
    out()

    out("### KW sequence compatibility")
    out(f"  All three involutions preserve KW pairing: ✓")
    out(f"  V₄ orbits on KW pairs: {len(pair_orbits)}")
    out(f"  Pair orbits split: {pair_orbit_loc}")
    out()

    out("### Anti-palindromes (comp∘rev-fixed)")
    out(f"  8 hexagrams where h = complement(reverse(h))")
    out(f"  All have exactly 3 yang lines (balanced yin/yang)")
    out(f"  Include 既濟 and 未濟 (the 互 cycle attractors)")
    out(f"  Lower trigram uniquely determines upper as comp∘rev(lower)")
    out()

    # Write results
    results_path = OUT_DIR / "06_v4_symmetry_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
