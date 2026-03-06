#!/usr/bin/env python3
"""
Phase 2 Closure: n=3 Cross-Scale Test

Does the weight-preservation principle unify n=3 and n=6?

At n=6: reversal (weight-preserving) for size-4 orbits, complement (forced) for size-2.
At n=3: tradition uses complement for all pairs. Is this consistent?

Key question: does a weight-preserving pairing even EXIST at n=3?
"""

import math
from collections import Counter
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 3
NUM_STATES = 1 << N  # 8
NUM_PAIRS = NUM_STATES // 2  # 4
MASK_ALL = (1 << N) - 1  # 7 = 0b111

POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]

def _reverse(x):
    bits = format(x, f'0{N}b')
    return int(bits[::-1], 2)

REVERSE = [_reverse(x) for x in range(NUM_STATES)]
COMPLEMENT = [x ^ MASK_ALL for x in range(NUM_STATES)]
COMP_REV = [COMPLEMENT[REVERSE[x]] for x in range(NUM_STATES)]

def fmt(x):
    return format(x, f'0{N}b')


# ─── Enumerate all pairings ──────────────────────────────────────────────────

def enumerate_pairings():
    results = []
    def recurse(remaining, current):
        if not remaining:
            results.append(tuple(current))
            return
        first = remaining[0]
        rest = remaining[1:]
        for i in range(len(rest)):
            partner = rest[i]
            current.append((first, partner))
            recurse(rest[:i] + rest[i+1:], current)
            current.pop()
    recurse(list(range(NUM_STATES)), [])
    return results


# ─── Measures ─────────────────────────────────────────────────────────────────

def compute_measures(pairs):
    strength = sum(POPCOUNT[a ^ b] for a, b in pairs)

    masks = [a ^ b for a, b in pairs]
    mask_counts = Counter(masks)
    entropy = max(0.0, -sum((c/NUM_PAIRS) * math.log2(c/NUM_PAIRS)
                             for c in mask_counts.values()))

    weight_diffs = [abs(POPCOUNT[a] - POPCOUNT[b]) for a, b in pairs]
    total_dw = sum(weight_diffs)
    weight_tilt = total_dw / NUM_PAIRS

    wa = np.array([POPCOUNT[a] for a, b in pairs], dtype=float)
    wb = np.array([POPCOUNT[b] for a, b in pairs], dtype=float)
    if wa.std() == 0 or wb.std() == 0:
        weight_corr = 0.0
    else:
        weight_corr = float(np.corrcoef(wa, wb)[0, 1])

    return {
        'S': strength, 'D': round(entropy, 6),
        'WT': round(weight_tilt, 4), 'WC': round(weight_corr, 6),
        'total_dw': total_dw, 'masks': mask_counts,
    }


# ─── Equivariance ────────────────────────────────────────────────────────────

def is_equivariant(pairs, op):
    pair_set = {(min(a,b), max(a,b)) for a,b in pairs}
    for a, b in pairs:
        oa, ob = op[a], op[b]
        if (min(oa,ob), max(oa,ob)) not in pair_set:
            return False
    return True


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("n=3 CROSS-SCALE ANALYSIS")
    pr("=" * 70)

    # ── 1. Z₂² orbit structure ──
    pr(f"\n## 1. Z₂² Orbit Structure at n=3")

    pr(f"\n  All 8 states:")
    for x in range(NUM_STATES):
        pr(f"    {fmt(x)}: w={POPCOUNT[x]}, rev={fmt(REVERSE[x])}, "
           f"comp={fmt(COMPLEMENT[x])}, cr={fmt(COMP_REV[x])}")

    # Orbits
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]})
        orbits.append(orbit)
        visited.update(orbit)

    pr(f"\n  Orbits under Z₂²:")
    for i, orb in enumerate(orbits):
        ws = [POPCOUNT[x] for x in orb]
        pr(f"    O{i} (size {len(orb)}): {[fmt(x) for x in orb]}  weights: {ws}")

    size_dist = Counter(len(o) for o in orbits)
    pr(f"\n  Orbit sizes: {dict(size_dist)}")

    # Fixed points
    palindromes = [x for x in range(NUM_STATES) if REVERSE[x] == x]
    cr_fixed = [x for x in range(NUM_STATES) if COMP_REV[x] == x]
    comp_fixed = [x for x in range(NUM_STATES) if COMPLEMENT[x] == x]

    pr(f"\n  Palindromes (rev-fixed): {len(palindromes)} — {[fmt(x) for x in palindromes]}")
    pr(f"  Comp∘rev-fixed: {len(cr_fixed)} — {[fmt(x) for x in cr_fixed]}")
    pr(f"  Complement-fixed: {len(comp_fixed)} — {[fmt(x) for x in comp_fixed]}")

    # n=3 is ODD — complement CAN have a fixed point if N is odd?
    # comp(x) = x means x ^ 111 = x, which means 111 = 0. No. So no complement-fixed points.
    # But at odd n, palindromes: rev(abc) = cba = abc means a=c. So palindromes have form a b a.
    # Count: 2 choices for a, 2 for b = 4 palindromes.

    # Classify orbits
    size2 = [o for o in orbits if len(o) == 2]
    size4 = [o for o in orbits if len(o) == 4]

    pr(f"\n  Size-2 orbits: {len(size2)}")
    for o in size2:
        a = o[0]
        is_pal = REVERSE[a] == a or REVERSE[o[1]] == o[1]
        is_cr = COMP_REV[a] == a or COMP_REV[o[1]] == o[1]
        pr(f"    {[fmt(x) for x in o]}  palindrome={is_pal}  cr-fixed={is_cr}")

    pr(f"\n  Size-4 orbits: {len(size4)}")
    for o in size4:
        pr(f"    {[fmt(x) for x in o]}")

    # ── 2. Can reversal produce a valid pairing? ──
    pr(f"\n## 2. Can Reversal Produce a Valid Pairing?")

    pr(f"\n  Reversal has {len(palindromes)} fixed points (palindromes).")
    if len(palindromes) > 0:
        pr(f"  Since palindromes map to themselves under reversal,")
        pr(f"  reversal alone CANNOT produce a complete pairing.")
    else:
        pr(f"  No fixed points — reversal can produce a complete pairing.")

    # What about comp∘rev?
    pr(f"\n  Comp∘rev has {len(cr_fixed)} fixed points.")
    if len(cr_fixed) > 0:
        pr(f"  Comp∘rev alone CANNOT produce a complete pairing.")
    else:
        pr(f"  No fixed points — comp∘rev can produce a complete pairing.")

    # What about complement?
    pr(f"\n  Complement has {len(comp_fixed)} fixed points.")
    pr(f"  Complement CAN produce a complete pairing.")

    # ── 3. Enumerate all 105 pairings ──
    pr(f"\n## 3. All {7*5*3*1} Pairings Enumerated")

    all_pairings = enumerate_pairings()
    pr(f"\n  Total pairings: {len(all_pairings)} (expected {7*5*3*1})")

    results = []
    for p in all_pairings:
        m = compute_measures(p)
        eq_comp = is_equivariant(p, COMPLEMENT)
        eq_rev = is_equivariant(p, REVERSE)
        eq_cr = is_equivariant(p, COMP_REV)
        eq_all = eq_comp and eq_rev and eq_cr
        m['eq_comp'] = eq_comp
        m['eq_rev'] = eq_rev
        m['eq_cr'] = eq_cr
        m['eq_all'] = eq_all
        m['pairing'] = p
        results.append(m)

    # ── 4. Equivariant pairings ──
    pr(f"\n## 4. Equivariant Pairings")

    eq_full = [r for r in results if r['eq_all']]
    eq_comp_only = [r for r in results if r['eq_comp']]
    eq_rev_only = [r for r in results if r['eq_rev']]
    eq_cr_only = [r for r in results if r['eq_cr']]

    pr(f"\n  Equivariant under complement: {len(eq_comp_only)}")
    pr(f"  Equivariant under reversal: {len(eq_rev_only)}")
    pr(f"  Equivariant under comp∘rev: {len(eq_cr_only)}")
    pr(f"  Fully Z₂²-equivariant (all three): {len(eq_full)}")

    if eq_full:
        pr(f"\n  All fully equivariant pairings:")
        for r in eq_full:
            pairs_str = ', '.join(f'{fmt(a)}↔{fmt(b)}' for a,b in r['pairing'])
            pr(f"    [{pairs_str}]")
            pr(f"      S={r['S']}, D={r['D']:.4f}, total_Δw={r['total_dw']}, "
               f"WC={r['WC']:+.4f}")
            pr(f"      masks: {dict((fmt(k),v) for k,v in r['masks'].items())}")

    # ── 5. Weight preservation analysis ──
    pr(f"\n## 5. Weight Preservation Analysis")

    # Among ALL 105 pairings
    total_dws = [r['total_dw'] for r in results]
    min_dw = min(total_dws)
    max_dw = max(total_dws)

    pr(f"\n  Total |Δw| across all pairings:")
    pr(f"    Range: [{min_dw}, {max_dw}]")
    dw_dist = Counter(total_dws)
    for dw in sorted(dw_dist):
        pr(f"    Δw={dw}: {dw_dist[dw]} pairings")

    zero_dw = [r for r in results if r['total_dw'] == 0]
    pr(f"\n  Pairings with total Δw = 0 (perfect weight preservation): {len(zero_dw)}")

    if zero_dw:
        pr(f"  Weight-preserving pairings:")
        for r in zero_dw:
            pairs_str = ', '.join(f'{fmt(a)}↔{fmt(b)}' for a,b in r['pairing'])
            pr(f"    [{pairs_str}]  S={r['S']}, D={r['D']:.4f}")
    else:
        pr(f"  NO weight-preserving pairing exists at n=3!")

        # Why? At n=3, weight distribution:
        # w=0: 1 state (000)
        # w=1: 3 states (001, 010, 100)
        # w=2: 3 states (011, 101, 110)
        # w=3: 1 state (111)
        weight_dist = Counter(POPCOUNT[x] for x in range(NUM_STATES))
        pr(f"\n  Weight distribution: {dict(sorted(weight_dist.items()))}")
        pr(f"  For Δw=0, each pair must have equal weight.")
        pr(f"  w=0: 1 state (odd count — cannot pair among themselves)")
        pr(f"  w=3: 1 state (odd count — cannot pair among themselves)")
        pr(f"  Since w=0 and w=3 each have 1 state, they MUST pair with")
        pr(f"  different-weight partners. Perfect weight preservation is impossible.")

    # Min Δw pairings
    min_dw_pairings = [r for r in results if r['total_dw'] == min_dw]
    pr(f"\n  Minimum Δw pairings (total_Δw = {min_dw}): {len(min_dw_pairings)}")
    for r in min_dw_pairings[:10]:
        pairs_str = ', '.join(f'{fmt(a)}(w={POPCOUNT[a]})↔{fmt(b)}(w={POPCOUNT[b]})' for a,b in r['pairing'])
        pr(f"    [{pairs_str}]")
        pr(f"      S={r['S']}, D={r['D']:.4f}, eq_all={r['eq_all']}")

    # ── 6. Equivariant + minimum weight disruption ──
    pr(f"\n## 6. Equivariance + Weight Preservation")

    if eq_full:
        eq_dws = [(r['total_dw'], r) for r in eq_full]
        min_eq_dw = min(dw for dw, _ in eq_dws)
        pr(f"\n  Min total_Δw among equivariant pairings: {min_eq_dw}")

        best_eq = [r for dw, r in eq_dws if dw == min_eq_dw]
        pr(f"  Equivariant pairings achieving min Δw: {len(best_eq)}")
        for r in best_eq:
            pairs_str = ', '.join(f'{fmt(a)}↔{fmt(b)}' for a,b in r['pairing'])
            pr(f"    [{pairs_str}]")
            pr(f"      S={r['S']}, D={r['D']:.4f}, total_Δw={r['total_dw']}")

        # Is it complement?
        comp_pairing = []
        seen = set()
        for x in range(NUM_STATES):
            if x in seen: continue
            c = COMPLEMENT[x]
            comp_pairing.append((min(x,c), max(x,c)))
            seen.update((x,c))
        comp_pairing = tuple(sorted(comp_pairing))

        for r in eq_full:
            if tuple(sorted(r['pairing'])) == comp_pairing:
                pr(f"\n  Complement pairing is fully equivariant: True")
                pr(f"    S={r['S']}, total_Δw={r['total_dw']}")
                break

    # ── 7. The unified principle ──
    pr(f"\n## 7. Cross-Scale Consistency Check")

    pr(f"""
  THE UNIFIED PRINCIPLE:
    Maximize weight preservation, subject to equivariance.
    Within that, maximize strength.

  AT n=6:
    - 12 size-4 orbits: reversal (weight-preserving) is available → use it
    - 8 size-2 orbits: forced to complement (weight disruption unavoidable
      for palindrome orbits, zero for cr-fixed orbits)
    - Among all-reversal: KW uniquely maximizes S
    → KW is the unique solution

  AT n=3:""")

    if not zero_dw:
        pr(f"    - NO weight-preserving pairing exists at all")
        pr(f"      (w=0 and w=3 have odd counts → forced cross-weight pairing)")
        pr(f"    - Weight preservation is vacuously maximized by any pairing")
        pr(f"    - Among equivariant pairings: {len(eq_full)} exist")
        if eq_full:
            min_eq_dw = min(r['total_dw'] for r in eq_full)
            best_s_eq = max(r['S'] for r in eq_full if r['total_dw'] == min_eq_dw)
            best = [r for r in eq_full if r['total_dw'] == min_eq_dw and r['S'] == best_s_eq]
            pr(f"    - Min Δw among equivariant: {min_eq_dw}")
            pr(f"    - Max S at min Δw among equivariant: {best_s_eq}")
            pr(f"    - Number achieving both: {len(best)}")

            is_comp = any(tuple(sorted(r['pairing'])) == comp_pairing for r in best)
            pr(f"    - Is complement the unique such pairing? {is_comp and len(best) == 1}")
    else:
        pr(f"    - Weight-preserving pairings exist: {len(zero_dw)}")

    # ── 8. Alternative: n=3 as degenerate case ──
    pr(f"\n## 8. Structural Comparison Across Scales")

    pr(f"""
  Scale decomposition:
  
  n=3: 4 orbits (2 size-2, 0 size-4)
    - ALL orbits are size-2 (palindrome or cr-fixed)
    - No size-4 orbits exist → no reversal/comp/cr choice at all
    - Every orbit is forced to self-match (complement)
    - The principle "use reversal for size-4 orbits" is vacuously satisfied
    
  n=4: 6 orbits (4 size-2, 2 size-4)
    - 2 size-4 orbits admit the rev/comp/cr choice
    - KW-style: reversal for both → S=24 (unique S-max in all-rev)
    
  n=6: 20 orbits (8 size-2, 12 size-4)  
    - 12 size-4 orbits admit the rev/comp/cr choice
    - KW: reversal for all 12 → S=120 (unique S-max in all-rev)""")

    # Count orbits at each scale
    for n_test in [3, 4, 5, 6]:
        ns = 1 << n_test
        mask = (1 << n_test) - 1

        def rev_n(x):
            bits = format(x, f'0{n_test}b')
            return int(bits[::-1], 2)

        rev_t = [rev_n(x) for x in range(ns)]
        comp_t = [x ^ mask for x in range(ns)]
        cr_t = [comp_t[rev_t[x]] for x in range(ns)]

        vis = set()
        orbs = []
        for x in range(ns):
            if x in vis: continue
            orb = sorted({x, comp_t[x], rev_t[x], cr_t[x]})
            orbs.append(orb)
            vis.update(orb)

        s2 = sum(1 for o in orbs if len(o) == 2)
        s4 = sum(1 for o in orbs if len(o) == 4)
        pals = sum(1 for x in range(ns) if rev_t[x] == x)
        crfix = sum(1 for x in range(ns) if cr_t[x] == x)
        pr(f"\n  n={n_test}: {len(orbs)} orbits ({s2} size-2, {s4} size-4), "
           f"{pals} palindromes, {crfix} cr-fixed")

    pr(f"""
  PATTERN: At odd n (3, 5), there are NO comp∘rev-fixed points
  (because comp_rev(x)=x means rev(x)=comp(x), requiring w(x)=N-w(x),
  so w=N/2 which is impossible at odd N).
  
  At even n (4, 6), comp∘rev-fixed points exist (w = N/2 is achievable).
  
  At n=3: 4 palindromes, 0 cr-fixed → 2 palindrome orbits, 0 cr-fixed orbits.
  All 4 remaining states form 1 size-4 orbit.
  Wait — let me recount...""")

    # Actually recount carefully for n=3
    pr(f"\n  n=3 recount:")
    pr(f"    Palindromes: {[fmt(x) for x in palindromes]} ({len(palindromes)} states)")
    pr(f"    CR-fixed: {[fmt(x) for x in cr_fixed]} ({len(cr_fixed)} states)")
    pr(f"    Size-2 orbits: {len(size2)}")
    pr(f"    Size-4 orbits: {len(size4)}")
    if size4:
        for o in size4:
            pr(f"      {[fmt(x) for x in o]}")
            x = o[0]
            opts = {}
            cx, rx, crx = COMPLEMENT[x], REVERSE[x], COMP_REV[x]

            # Three intra-orbit pairings
            for label, p1, p2 in [
                ('comp', (min(x,cx),max(x,cx)), (min(rx,crx),max(rx,crx))),
                ('rev', (min(x,rx),max(x,rx)), (min(cx,crx),max(cx,crx))),
                ('cr', (min(x,crx),max(x,crx)), (min(cx,rx),max(cx,rx))),
            ]:
                s_val = POPCOUNT[p1[0]^p1[1]] + POPCOUNT[p2[0]^p2[1]]
                dw1 = abs(POPCOUNT[p1[0]] - POPCOUNT[p1[1]])
                dw2 = abs(POPCOUNT[p2[0]] - POPCOUNT[p2[1]])
                m1 = fmt(p1[0] ^ p1[1])
                m2 = fmt(p2[0] ^ p2[1])
                pr(f"        {label}: {fmt(p1[0])}↔{fmt(p1[1])}, {fmt(p2[0])}↔{fmt(p2[1])}  "
                   f"S={s_val}, Δw=[{dw1},{dw2}], masks=[{m1},{m2}]")

    # ── Summary ──
    pr(f"\n{'='*70}")
    pr("SUMMARY")
    pr(f"{'='*70}")

    pr(f"""
  1. n=3 has {len(orbits)} orbits: {len(size2)} size-2, {len(size4)} size-4
  2. {len(palindromes)} palindromes, {len(cr_fixed)} cr-fixed points
  3. Perfect weight preservation is {'impossible' if not zero_dw else 'possible'} at n=3
     {'(odd weight classes w=0,w=3 have 1 state each)' if not zero_dw else ''}
  4. Fully equivariant pairings: {len(eq_full)}
  5. Complement is {'the unique' if len(eq_full)==1 else 'one of the'} fully equivariant pairing{'s' if len(eq_full)>1 else ''}
""")

    if size4:
        pr(f"  6. n=3 HAS a size-4 orbit: the non-palindromic states")
        pr(f"     Within this orbit, reversal gives Δw=0 (weight-preserving)")
        pr(f"     Complement gives Δw>0")
        pr(f"     The principle 'use reversal for size-4 orbits' IS applicable")
        pr(f"     But the size-2 orbits force complement (which contributes Δw>0)")

        # Check: does the pairing that uses rev for size-4 + comp for size-2 exist?
        # And is it equivariant?
        # Size-2 orbits: self-match (complement)
        # Size-4 orbit: use reversal
        kw_style_pairs = []
        # size-2 orbits
        for o in size2:
            a, b = o
            kw_style_pairs.append((min(a,b), max(a,b)))
        # size-4 orbit: reversal
        if size4:
            x = size4[0][0]
            rx = REVERSE[x]
            cx = COMPLEMENT[x]
            crx = COMP_REV[x]
            kw_style_pairs.append((min(x,rx), max(x,rx)))
            kw_style_pairs.append((min(cx,crx), max(cx,crx)))

        kw_style = tuple(sorted(kw_style_pairs))
        pr(f"\n     'KW-style' at n=3 (rev for size-4, comp for size-2):")
        for a,b in kw_style:
            pr(f"       {fmt(a)}↔{fmt(b)}  Δw={abs(POPCOUNT[a]-POPCOUNT[b])}")

        # Find it in results
        for r in results:
            if tuple(sorted(r['pairing'])) == kw_style:
                pr(f"       S={r['S']}, D={r['D']:.4f}, total_Δw={r['total_dw']}")
                pr(f"       Equivariant: {r['eq_all']}")
                pr(f"       Equivariant under comp: {r['eq_comp']}")
                pr(f"       Equivariant under rev: {r['eq_rev']}")
                pr(f"       Equivariant under cr: {r['eq_cr']}")
                break

        # Compare with complement pairing
        pr(f"\n     Complement pairing at n=3:")
        for a,b in comp_pairing:
            pr(f"       {fmt(a)}↔{fmt(b)}  Δw={abs(POPCOUNT[a]-POPCOUNT[b])}")
        for r in results:
            if tuple(sorted(r['pairing'])) == comp_pairing:
                pr(f"       S={r['S']}, D={r['D']:.4f}, total_Δw={r['total_dw']}")
                pr(f"       Equivariant: {r['eq_all']}")
                break

        # The key comparison
        pr(f"\n     THE CROSS-SCALE TEST:")
        pr(f"     At n=3, the 'KW-style' (rev for size-4, comp for size-2)")
        pr(f"     and the 'complement' (comp for everything) are DIFFERENT pairings.")
        pr(f"     Tradition chose COMPLEMENT, not KW-style.")
        pr(f"     Is complement consistent with the weight-preservation principle?")

        # Count Δw for each
        kw_dw = sum(abs(POPCOUNT[a]-POPCOUNT[b]) for a,b in kw_style)
        comp_dw = sum(abs(POPCOUNT[a]-POPCOUNT[b]) for a,b in comp_pairing)
        pr(f"\n     KW-style total Δw: {kw_dw}")
        pr(f"     Complement total Δw: {comp_dw}")

        if kw_dw < comp_dw:
            pr(f"\n     KW-style has LESS weight disruption than complement!")
            pr(f"     But tradition chose complement anyway.")
            pr(f"     This means the n=3 tradition does NOT follow the weight-preservation principle.")
            pr(f"     However: is KW-style equivariant?")
        elif kw_dw == comp_dw:
            pr(f"\n     Both have EQUAL weight disruption.")
            pr(f"     The principle doesn't distinguish them at n=3.")
        else:
            pr(f"\n     Complement has LESS weight disruption!")

    # ── Save ──
    md_path = out_dir / 'cross_scale_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
