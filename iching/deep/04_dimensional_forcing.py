#!/usr/bin/env python3
"""
Dimensional Forcing: Why 3 Lines?

Tests the conjecture: n=3 is the unique dimension where every surjective
complement=negation partition Z₂ⁿ → Z₅ has singleton fibers.

Framework:
  Complement pairs {x, x̄} in Z₂ⁿ map to Z₅ destinations:
    - Both to 0 (Wood, self-conjugate under negation in Z₅)
    - One to 1, other to 4 (Fire/Water: 1+4 ≡ 0 mod 5)
    - One to 2, other to 3 (Earth/Metal: 2+3 ≡ 0 mod 5)

  With k₀ pairs → {0}, k₁ pairs → {1,4}, k₂ pairs → {2,3}:
    Fiber sizes: |0|=2k₀, |1|=k₁, |4|=k₁, |2|=k₂, |3|=k₂
    Surjective requires k₀ ≥ 1, k₁ ≥ 1, k₂ ≥ 1
    Singletons exist iff min(k₁, k₂) = 1

Also explores hexagram dimension (互 convergence for general n).
"""

import sys
from math import comb
from pathlib import Path
from itertools import product
from collections import Counter, defaultdict

OUT_DIR = Path(__file__).resolve().parent


def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# Dimensional Forcing: Why 3 Lines?")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 1: Dimensional forcing theorem for n=1..8
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 1: Dimensional Forcing Theorem (n=1..8)")
    out()
    out("For Z₂ⁿ with complement=negation partitions into Z₅:")
    out("  2^(n-1) complement pairs distributed as (k₀, k₁, k₂)")
    out("  Fiber sizes: |Wood|=2k₀, |Fire|=|Water|=k₁, |Earth|=|Metal|=k₂")
    out("  Surjective: k₀≥1, k₁≥1, k₂≥1")
    out("  Singleton: min(k₁,k₂)=1")
    out()

    out(f"{'n':>3}  {'2^(n-1)':>7}  {'surj shapes':>11}  {'w/ singl':>9}  "
        f"{'w/o singl':>10}  {'ALL singl?':>10}  {'min fiber':>9}")
    out("-" * 75)

    unique_n = None
    results_by_n = {}

    for n in range(1, 9):
        pairs = 2 ** (n - 1)

        surjective = []
        for k0 in range(1, pairs + 1):
            for k1 in range(1, pairs - k0 + 1):
                k2 = pairs - k0 - k1
                if k2 >= 1:
                    surjective.append((k0, k1, k2))

        with_singleton = [(k0, k1, k2) for k0, k1, k2 in surjective
                          if min(k1, k2) == 1]
        without_singleton = [(k0, k1, k2) for k0, k1, k2 in surjective
                             if min(k1, k2) > 1]

        all_singleton = len(without_singleton) == 0 and len(surjective) > 0

        # Min fiber size across all surjective
        min_fiber = float('inf')
        for k0, k1, k2 in surjective:
            fibers = [2 * k0, k1, k1, k2, k2]
            min_fiber = min(min_fiber, min(fibers))
        if not surjective:
            min_fiber = 0

        results_by_n[n] = {
            "pairs": pairs,
            "surjective": surjective,
            "with_singleton": with_singleton,
            "without_singleton": without_singleton,
            "all_singleton": all_singleton,
            "min_fiber": min_fiber,
        }

        marker = " ←←←" if all_singleton else ""
        out(f"{n:>3}  {pairs:>7}  {len(surjective):>11}  {len(with_singleton):>9}  "
            f"{len(without_singleton):>10}  {'YES' if all_singleton else 'no':>10}  "
            f"{min_fiber:>9}{marker}")

        if all_singleton and unique_n is None:
            unique_n = n

    out()

    # Check uniqueness
    all_forced = [n for n in range(1, 9) if results_by_n[n]["all_singleton"]]
    out(f"Dimensions where ALL surjective partitions have singletons: {all_forced}")
    out()

    if len(all_forced) == 1 and all_forced[0] == 3:
        out("★ CONFIRMED: n=3 is the UNIQUE dimension (among 1..8) where every")
        out("  surjective complement=negation partition Z₂ⁿ → Z₅ has singleton fibers.")
    elif 3 in all_forced and len(all_forced) > 1:
        out(f"  n=3 has the singleton property, but so do: {[x for x in all_forced if x != 3]}")
    else:
        out(f"  SURPRISE: n=3 does NOT have the universal singleton property!")
    out()

    # Show why n=3 is forced
    out("### Why n=3 is forced")
    out()
    out("For n=3: 2^(n-1) = 4 complement pairs")
    out("  k₀ + k₁ + k₂ = 4, all ≥ 1")
    out("  Surjective partition shapes:")
    for k0, k1, k2 in results_by_n[3]["surjective"]:
        fibers = [2 * k0, k1, k1, k2, k2]
        has_s = min(k1, k2) == 1
        out(f"    ({k0},{k1},{k2}) → fibers {fibers} "
            f"{'singleton ✓' if has_s else 'NO singleton'}")
    out()
    out("  With k₀+k₁+k₂=4 and all ≥ 1: max(k₁,k₂) ≤ 4-1-1 = 2")
    out("  If min(k₁,k₂) ≥ 2, then k₁+k₂ ≥ 4, so k₀ ≤ 0 → contradiction.")
    out("  Therefore min(k₁,k₂) = 1 always. QED.")
    out()

    # Show why n=4 breaks
    out("### Why n=4 breaks")
    out()
    out("For n=4: 2^(n-1) = 8 complement pairs")
    out("  First partition without singletons:")
    for k0, k1, k2 in results_by_n[4]["without_singleton"][:3]:
        fibers = [2 * k0, k1, k1, k2, k2]
        out(f"    ({k0},{k1},{k2}) → fibers {fibers}")
    out()
    out("  (k₁=2, k₂=2) is possible because k₀=8-2-2=4 ≥ 1. No singletons.")
    out()

    # Show why n=2 fails
    out("### Why n=2 fails (different reason)")
    out()
    if results_by_n[2]["surjective"]:
        out("For n=2: 2^(n-1) = 2 complement pairs")
        out("  k₀+k₁+k₂ = 2, all ≥ 1 → impossible! (sum ≥ 3)")
        out("  No surjective partitions exist at all.")
    else:
        out("For n=2: 2^(n-1) = 2 complement pairs")
        out("  k₀+k₁+k₂ = 2 with all ≥ 1 → impossible (need ≥ 3)")
        out("  NO surjective partitions exist. The Z₂/Z₅ bridge cannot be built.")
    out()

    out("### Boundary analysis")
    out()
    out("  n=1: 1 pair, cannot reach 3 destinations → no surjection")
    out("  n=2: 2 pairs, need 3 destinations → still impossible")
    out("  n=3: 4 pairs, 3 destinations → surjection forced to have singletons ★")
    out("  n=4: 8 pairs, 3 destinations → room for non-singleton partitions")
    out("  n≥4: always have non-singleton partitions (slack grows)")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 2: Concrete assignments for n=3
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 2: Concrete Assignments for n=3")
    out()

    # The 4 complement pairs in Z₂³
    comp_pairs = []
    seen = set()
    for x in range(8):
        xbar = x ^ 7
        pair = (min(x, xbar), max(x, xbar))
        if pair not in seen:
            seen.add(pair)
            comp_pairs.append(pair)

    out(f"Complement pairs in Z₂³: {comp_pairs}")
    out(f"  = {{(000,111), (001,110), (010,101), (011,100)}}")
    out()

    # For each surjective partition shape, count concrete assignments
    out("### Partition shapes and concrete assignment counts")
    out()

    # Destinations: 0 = {x,x̄} both to Wood
    #               1 = one to Fire(1), other to Water(4)
    #               2 = one to Earth(2), other to Metal(3)
    # For dest 0: the pair maps to (0,0) — 1 way
    # For dest 1: which of {x, x̄} goes to 1 vs 4 — 2 ways
    # For dest 2: which of {x, x̄} goes to 2 vs 3 — 2 ways

    total_assignments = 0
    out(f"{'Shape':>12}  {'Fibers':>20}  {'Pair combos':>12}  {'Orientations':>12}  "
        f"{'Total':>6}  {'Type':>6}")
    out("-" * 80)

    for k0, k1, k2 in results_by_n[3]["surjective"]:
        # Choose which pairs go to each destination
        # C(4, k0) * C(4-k0, k1) ways to assign pairs to destinations
        pair_combos = comb(4, k0) * comb(4 - k0, k1)  # k2 is forced

        # For each pair in dest 1 or 2: 2 orientations
        orientations = 2 ** k1 * 2 ** k2

        total = pair_combos * orientations
        total_assignments += total

        # Identify traditional type
        fibers = sorted([2 * k0, k1, k1, k2, k2], reverse=True)
        if fibers == [4, 1, 1, 1, 1]:
            ttype = "A"
        elif fibers == [2, 2, 2, 1, 1]:
            ttype = "B/C"
        else:
            ttype = "?"

        out(f"  ({k0},{k1},{k2})  {str([2*k0,k1,k1,k2,k2]):>20}  "
            f"{pair_combos:>12}  {orientations:>12}  {total:>6}  {ttype:>6}")

    out(f"\n  Total concrete assignments: {total_assignments}")
    out()

    # Cross-check with R32 = (8! / 32) from iteration 1
    # The 32 automorphisms of Z₅ under complement=negation
    # Actually, let me just enumerate directly
    out("### Direct enumeration verification")
    out()

    # Enumerate all f: Z₂³ → Z₅ satisfying complement=negation
    valid_assignments = []
    for dest in product(range(3), repeat=4):
        # dest[i] = destination of complement pair i
        # 0 → both to Wood, 1 → Fire/Water split, 2 → Earth/Metal split
        k0 = dest.count(0)
        k1 = dest.count(1)
        k2 = dest.count(2)
        if k0 < 1 or k1 < 1 or k2 < 1:
            continue  # not surjective

        # For each pair in dest 1 or 2, choose orientation
        n_orient = 2 ** (k1 + k2)
        for orient_bits in range(n_orient):
            # Build the assignment
            f = {}
            bit_idx = 0
            for pair_idx, (x, xbar) in enumerate(comp_pairs):
                d = dest[pair_idx]
                if d == 0:
                    f[x] = 0
                    f[xbar] = 0
                elif d == 1:
                    bit = (orient_bits >> bit_idx) & 1
                    bit_idx += 1
                    if bit == 0:
                        f[x] = 1
                        f[xbar] = 4
                    else:
                        f[x] = 4
                        f[xbar] = 1
                elif d == 2:
                    bit = (orient_bits >> bit_idx) & 1
                    bit_idx += 1
                    if bit == 0:
                        f[x] = 2
                        f[xbar] = 3
                    else:
                        f[x] = 3
                        f[xbar] = 2

            # Verify complement=negation
            ok = all(f[x ^ 7] == (5 - f[x]) % 5 for x in range(8))
            if ok:
                valid_assignments.append(dict(f))

    out(f"  Direct enumeration: {len(valid_assignments)} valid assignments")
    out(f"  Matches combinatorial count: {len(valid_assignments) == total_assignments}")
    out()

    # Classify by fiber shape
    shape_counts = Counter()
    for f in valid_assignments:
        fibers = tuple(sorted(Counter(f.values()).values(), reverse=True))
        shape_counts[fibers] += 1

    out("  Fiber shape distribution:")
    for shape, count in sorted(shape_counts.items()):
        has_single = 1 in shape
        out(f"    {shape}: {count} assignments {'(has singleton ✓)' if has_single else '(NO singleton!)'}")
    out()

    # Verify ALL have singletons
    all_have_singleton = all(1 in shape for shape in shape_counts)
    out(f"  ALL assignments have singletons: {all_have_singleton}")
    out()

    # Identify the traditional assignment
    out("### Traditional assignment identification")
    out()
    # Traditional: Qian(111)→Metal(3), Dui(011)→Metal(3), Li(101)→Fire(1),
    #   Zhen(001)→Wood(0), Xun(110)→Wood(0), Kan(010)→Water(4),
    #   Gen(100)→Earth(2), Kun(000)→Earth(2)
    trad = {0b111: 3, 0b011: 3, 0b101: 1, 0b001: 0,
            0b110: 0, 0b010: 4, 0b100: 2, 0b000: 2}

    # Verify complement=negation
    trad_ok = all(trad[x ^ 7] == (5 - trad[x]) % 5 for x in range(8))
    out(f"  Traditional assignment satisfies complement=negation: {trad_ok}")

    # Find its fiber shape
    trad_fibers = tuple(sorted(Counter(trad.values()).values(), reverse=True))
    out(f"  Traditional fiber shape: {trad_fibers}")
    out(f"  Traditional assignment is type: "
        f"{'A (4,1,1,1,1)' if trad_fibers == (4,1,1,1,1) else 'B/C (2,2,2,1,1)' if trad_fibers == (2,2,2,1,1) else 'other'}")
    out()

    # Which pair destinations?
    out("  Traditional pair destinations:")
    for x, xbar in comp_pairs:
        fx, fxbar = trad[x], trad[xbar]
        if fx == fxbar == 0:
            dest = "both→Wood (type 0)"
        elif set([fx, fxbar]) == {1, 4}:
            dest = f"{fx},{fxbar} → Fire/Water split (type 1)"
        elif set([fx, fxbar]) == {2, 3}:
            dest = f"{fx},{fxbar} → Earth/Metal split (type 2)"
        else:
            dest = f"ERROR: {fx},{fxbar}"
        out(f"    ({x:03b},{xbar:03b}): {dest}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 3: n=4 partition space
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 3: n=4 Partition Space")
    out()

    r4 = results_by_n[4]
    out(f"n=4: 2^3 = 8 complement pairs")
    out(f"  Surjective partition shapes: {len(r4['surjective'])}")
    out(f"  With singletons: {len(r4['with_singleton'])}")
    out(f"  Without singletons: {len(r4['without_singleton'])}")
    out(f"  Fraction with singletons: {len(r4['with_singleton'])}/{len(r4['surjective'])} "
        f"= {len(r4['with_singleton'])/len(r4['surjective']):.3f}")
    out()

    out("  All surjective shapes:")
    out(f"  {'Shape':>12}  {'Fibers':>25}  {'Singleton?':>10}  {'Min fiber':>9}")
    out("  " + "-" * 65)
    for k0, k1, k2 in r4["surjective"]:
        fibers = sorted([2 * k0, k1, k1, k2, k2], reverse=True)
        has_s = min(k1, k2) == 1
        mf = min(fibers)
        out(f"  ({k0:>2},{k1:>2},{k2:>2})  {str(fibers):>25}  "
            f"{'✓' if has_s else '✗':>10}  {mf:>9}")
    out()

    # Count concrete assignments for n=4
    out("  Concrete assignment counts by shape:")
    n4_total = 0
    for k0, k1, k2 in r4["surjective"]:
        pair_combos = comb(8, k0) * comb(8 - k0, k1)
        orientations = 2 ** (k1 + k2)
        total = pair_combos * orientations
        n4_total += total
        fibers = sorted([2 * k0, k1, k1, k2, k2], reverse=True)
        out(f"    ({k0},{k1},{k2}) [{fibers}]: "
            f"C(8,{k0})×C({8-k0},{k1}) × 2^{k1+k2} = {total}")
    out(f"  Total concrete assignments for n=4: {n4_total}")
    out()

    # Min fiber size
    out(f"  Minimum fiber size across all surjective partitions: {r4['min_fiber']}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 4: Precise theorem statement
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 4: Theorem Statement")
    out()
    out("**Theorem (Dimensional Forcing).** Let f: Z₂ⁿ → Z₅ be a surjection")
    out("satisfying f(x̄) = -f(x) mod 5 for all x ∈ Z₂ⁿ (where x̄ = x ⊕ 1ⁿ).")
    out("Then:")
    out("  (a) Such f exists if and only if n ≥ 3.")
    out("  (b) For n = 3, every such f has at least two singleton fibers.")
    out("  (c) For n ≥ 4, there exist such f with no singleton fibers.")
    out()
    out("*Proof.*")
    out("  There are 2^(n-1) complement pairs. Each pair maps to one of 3")
    out("  destination types: self-conjugate (0), or one of two split types (1,2).")
    out("  Let (k₀,k₁,k₂) be the counts. Surjectivity requires k₀,k₁,k₂ ≥ 1.")
    out()
    out("  (a) k₀+k₁+k₂ = 2^(n-1) ≥ 3 iff n ≥ 3. For n≤2, 2^(n-1) ≤ 2 < 3.")
    out()
    out("  (b) For n=3: k₀+k₁+k₂ = 4 with all ≥ 1.")
    out("      Suppose min(k₁,k₂) ≥ 2. Then k₁+k₂ ≥ 4, so k₀ ≤ 0. Contradiction.")
    out("      Therefore min(k₁,k₂) = 1, giving fiber size 1 (a singleton).")
    out("      The paired element with k=1 produces two singleton fibers (at")
    out("      positions i and 5-i in Z₅).")
    out()
    out("  (c) For n=4: (k₀,k₁,k₂) = (4,2,2) gives all fibers ≥ 2. □")
    out()
    out("**Corollary.** The Z₂/Z₅ bridge — the existence of an injective point")
    out("in the quotient map f: Z₂ⁿ → Z₅ with complement=negation — is")
    out("structurally guaranteed if and only if n = 3.")
    out()
    out("**Interpretation.** The trigram having 3 lines is not a design choice")
    out("but a structural necessity: it is the unique dimension where the")
    out("Z₂-Z₅ bridge is forced to create singleton fibers, which are the")
    out("injection points that make the quotient map invertible on two fibers.")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 5: Hexagram dimension (互 convergence)
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 5: Hexagram Dimension (互 Convergence)")
    out()
    out("For 2n-line figures (Z₂^{2n}), the 互 analog extracts inner lines")
    out("and repackages them. We test convergence for n=2,3,4.")
    out()

    # For the actual I Ching (n=3, 6-line hexagrams):
    # 互 takes lines 2,3,4,5 (0-indexed: lines 1,2,3,4) and forms:
    #   lower trigram = lines 2,3,4 (original lines 1,2,3)
    #   upper trigram = lines 3,4,5 (original lines 2,3,4)
    # In our bit encoding (bit0=line1):
    #   For hexagram h (6 bits, bit0=line1):
    #     inner_lower = (h >> 1) & 0b111   (lines 2,3,4)
    #     inner_upper = (h >> 2) & 0b111   (lines 3,4,5)
    #     hu_hex = inner_lower | (inner_upper << 3)

    out("### n=3: Standard 互 (6-line hexagrams)")
    out()

    def hu_6(h):
        """互 transform for 6-line hexagrams."""
        inner_lower = (h >> 1) & 0b111
        inner_upper = (h >> 2) & 0b111
        return inner_lower | (inner_upper << 3)

    # Compute convergence
    orbit_lengths = []
    fixed_points = []
    cycle_2 = []

    for h in range(64):
        seen = [h]
        x = h
        for step in range(20):
            x = hu_6(x)
            if x in seen:
                cycle_start = seen.index(x)
                prefix = cycle_start
                cycle_len = len(seen) - cycle_start
                orbit_lengths.append((h, prefix, cycle_len))
                if cycle_len == 1:
                    fixed_points.append(x)
                elif cycle_len == 2:
                    cycle_2.append(x)
                break
            seen.append(x)

    fp_set = set(fixed_points)
    out(f"  Total hexagrams: 64")
    out(f"  Fixed points of 互: {len(fp_set)}")
    out(f"    Values: {sorted(fp_set)}")

    # Show fixed points as trigram pairs
    out(f"    As upper/lower trigrams:")
    for h in sorted(fp_set):
        lower = h & 0b111
        upper = (h >> 3) & 0b111
        out(f"      {h:06b} = ({upper:03b}/{lower:03b})")
    out()

    # Convergence depth distribution
    depth_dist = Counter()
    for h, prefix, cycle_len in orbit_lengths:
        depth_dist[prefix] += 1

    out(f"  Convergence depth distribution (steps to reach cycle):")
    for d in sorted(depth_dist):
        out(f"    depth {d}: {depth_dist[d]} hexagrams")
    out()

    max_depth = max(prefix for _, prefix, _ in orbit_lengths)
    out(f"  Maximum convergence depth: {max_depth}")

    # Cycle length distribution
    cycle_dist = Counter()
    for _, _, cycle_len in orbit_lengths:
        cycle_dist[cycle_len] += 1
    out(f"  Cycle length distribution:")
    for cl in sorted(cycle_dist):
        out(f"    cycle length {cl}: {cycle_dist[cl]} hexagrams")
    out()

    # ─── n=2: 4-line figures ──
    out("### n=2: 4-line figures (Z₂⁴)")
    out()
    out("  For 4-line figures, 互 extracts inner 2 lines (lines 2,3)")
    out("  and must form a new 4-line figure. Following the pattern:")
    out("    lower 'digram' = lines 2,3 → new lines 1,2")
    out("    upper 'digram' = lines 2,3 → new lines 3,4")
    out("  This means 互(h) = inner | (inner << 2) where inner = (h>>1) & 0b11")
    out()

    def hu_4(h):
        """互 analog for 4-line figures."""
        inner = (h >> 1) & 0b11  # lines 2,3
        return inner | (inner << 2)  # duplicate as lower and upper

    fp4 = set()
    depths_4 = []
    for h in range(16):
        seen = [h]
        x = h
        for step in range(20):
            x = hu_4(x)
            if x in seen:
                cycle_start = seen.index(x)
                depths_4.append((h, cycle_start, len(seen) - cycle_start))
                if len(seen) - cycle_start == 1:
                    fp4.add(x)
                break
            seen.append(x)

    out(f"  Total 4-line figures: 16")
    out(f"  Fixed points: {len(fp4)} → {sorted(fp4)}")
    out(f"    As binary: {[f'{h:04b}' for h in sorted(fp4)]}")

    depth_dist4 = Counter(d for _, d, _ in depths_4)
    out(f"  Convergence depths: {dict(sorted(depth_dist4.items()))}")
    max_d4 = max(d for _, d, _ in depths_4)
    out(f"  Max depth: {max_d4}")
    out()

    # ─── n=4: 8-line figures ──
    out("### n=4: 8-line figures (Z₂⁸)")
    out()
    out("  For 8-line figures, 互 extracts inner 6 lines (lines 2-7)")
    out("  Lower 4-gram = lines 2,3,4,5 → bits 0-3")
    out("  Upper 4-gram = lines 3,4,5,6 → bits 4-7")
    out("  But this gives an 8-line figure only if we treat")
    out("  lines 2-5 as lower half and lines 3-6 as upper half.")
    out()

    def hu_8(h):
        """互 analog for 8-line figures."""
        # Extract inner 6 lines (lines 2-7, i.e., bits 1-6)
        # Lower tetrad: lines 2,3,4,5 = bits 1,2,3,4
        lower = (h >> 1) & 0xF
        # Upper tetrad: lines 3,4,5,6 = bits 2,3,4,5
        upper = (h >> 2) & 0xF
        return lower | (upper << 4)

    fp8 = set()
    depths_8 = []
    for h in range(256):
        seen = [h]
        x = h
        for step in range(30):
            x = hu_8(x)
            if x in seen:
                cycle_start = seen.index(x)
                depths_8.append((h, cycle_start, len(seen) - cycle_start))
                if len(seen) - cycle_start == 1:
                    fp8.add(x)
                break
            seen.append(x)

    out(f"  Total 8-line figures: 256")
    out(f"  Fixed points: {len(fp8)}")

    depth_dist8 = Counter(d for _, d, _ in depths_8)
    out(f"  Convergence depths: {dict(sorted(depth_dist8.items()))}")
    max_d8 = max(d for _, d, _ in depths_8)
    out(f"  Max depth: {max_d8}")

    cycle_dist8 = Counter(cl for _, _, cl in depths_8)
    out(f"  Cycle lengths: {dict(sorted(cycle_dist8.items()))}")
    out()

    # ─── Comparison table ──
    out("### Comparison: 互 convergence by dimension")
    out()
    out(f"{'n':>3}  {'2n lines':>8}  {'|Z₂^{2n}|':>10}  {'Fixed pts':>9}  "
        f"{'Max depth':>9}  {'Cycle lens':>15}")
    out("-" * 65)

    results_hu = [
        (2, 4, 16, len(fp4), max_d4, dict(sorted(Counter(cl for _, _, cl in depths_4).items()))),
        (3, 6, 64, len(fp_set), max_depth, dict(sorted(cycle_dist.items()))),
        (4, 8, 256, len(fp8), max_d8, dict(sorted(cycle_dist8.items()))),
    ]
    for n, lines, total, fp, md, cl in results_hu:
        out(f"{n:>3}  {lines:>8}  {total:>10}  {fp:>9}  {md:>9}  {str(cl):>15}")
    out()

    # Check: is n=3 special?
    out("### Is n=3 distinguished for 互 convergence?")
    out()

    # For n=3: all orbits converge to fixed points (cycle len = 1)?
    all_fp_6 = all(cl == 1 for _, _, cl in orbit_lengths)
    all_fp_4 = all(cl == 1 for _, _, cl in depths_4)
    all_fp_8 = all(cl == 1 for _, _, cl in depths_8)

    out(f"  n=2 (4 lines): all converge to fixed points? {all_fp_4}")
    out(f"  n=3 (6 lines): all converge to fixed points? {all_fp_6}")
    out(f"  n=4 (8 lines): all converge to fixed points? {all_fp_8}")
    out()

    if all_fp_6 and not all_fp_8:
        out("  ★ n=3 is the largest n where all 互 orbits converge to fixed points")
    out()

    # Check max cycle length by dimension
    max_cycle_4 = max(cl for _, _, cl in depths_4)
    max_cycle_6 = max(cl for _, _, cl in orbit_lengths)
    max_cycle_8 = max(cl for _, _, cl in depths_8)
    out(f"  Max cycle length by dimension:")
    out(f"    n=2: max cycle = {max_cycle_4} → all cycles divide 2: "
        f"{'✓' if max_cycle_4 <= 2 else '✗'}")
    out(f"    n=3: max cycle = {max_cycle_6} → all cycles divide 2: "
        f"{'✓' if max_cycle_6 <= 2 else '✗'}")
    out(f"    n=4: max cycle = {max_cycle_8} → all cycles divide 2: "
        f"{'✓' if max_cycle_8 <= 2 else '✗'}")
    out()
    if max_cycle_4 <= 2 and max_cycle_6 <= 2 and max_cycle_8 > 2:
        out("  ★ n=3 is the largest n where 互² is the identity on eventual cycles.")
        out("    At n=4, 互 introduces 3-cycles — a qualitative change in dynamics.")
    elif max_cycle_6 <= 2 and max_cycle_8 > 2:
        out("  ★ n≤3: 互² = identity on cycles. n=4: 3-cycles appear.")
    out()

    # Fixed point fraction
    for n, lines, total, fp, md, cl in results_hu:
        out(f"  n={n}: {fp}/{total} = {fp/total:.3f} fixed point ratio")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Summary
    # ════════════════════════════════════════════════════════════════════════
    out("## Summary")
    out()
    out("### Dimensional forcing: n=3 is uniquely forced")
    out("  • n ≤ 2: No surjective complement=negation partition exists")
    out("  • n = 3: Every surjection has singletons (pigeonhole on 4 pairs)")
    out("  • n ≥ 4: Non-singleton surjections exist (enough slack)")
    out("  → The 3-line trigram is the unique bridge dimension")
    out()
    out("### Concrete count for n=3")
    out(f"  Total valid assignments: {len(valid_assignments)}")
    out(f"  Fiber shapes: {dict(shape_counts)}")
    out(f"  ALL have singletons: {all_have_singleton}")
    out()
    out("### 互 convergence")
    out(f"  n=2 (4 lines): max cycle {max_cycle_4}, max depth {max_d4}, {len(fp4)} fixed pts")
    out(f"  n=3 (6 lines): max cycle {max_cycle_6}, max depth {max_depth}, {len(fp_set)} fixed pts")
    out(f"  n=4 (8 lines): max cycle {max_cycle_8}, max depth {max_d8}, {len(fp8)} fixed pts")
    out(f"  → n=4 introduces 3-cycles: 互² ≠ identity on eventual cycle")
    out()

    # Write results
    results_path = OUT_DIR / "04_dimensional_forcing_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
