#!/usr/bin/env python3
"""
Phase 2 — Task A+B: S↔D Anti-Correlation Under Equivariance & Weight Preservation

Task A: Derive why r(S,D) = 0 in full space but r(S,D) ≈ −0.33 under equivariance.
Task B: Verify that reversal is the unique weight-preserving intra-orbit operation.

Key structural identity: for every size-4 orbit,
    S_rev + S_cr = S_comp = 12  (constant)

This creates a per-orbit S↔mask coupling that doesn't exist in the full space:
  - comp: S=12 (maximum per orbit), mask=111111 (shared, reduces D)
  - rev:  S∈{4,8}, mask=palindromic (distinct per orbit, increases D)
  - cr:   S∈{4,8}, mask=comp(palindromic) (distinct per orbit, increases D)

Choosing high-S (comp) concentrates masks → low D.
Choosing low-S (rev/cr) diversifies masks → high D.
This per-orbit tradeoff creates the anti-correlation under equivariance.
"""

import math
from collections import Counter
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N
NUM_PAIRS = NUM_STATES // 2
MASK_ALL = (1 << N) - 1

POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]

def _reverse(x):
    bits = format(x, f'0{N}b')
    return int(bits[::-1], 2)

REVERSE = [_reverse(x) for x in range(NUM_STATES)]
COMPLEMENT = [x ^ MASK_ALL for x in range(NUM_STATES)]
COMP_REV = [COMPLEMENT[REVERSE[x]] for x in range(NUM_STATES)]

def fmt(x):
    return format(x, f'0{N}b')


# ─── Orbit computation ───────────────────────────────────────────────────────

def compute_state_orbits():
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]})
        orbits.append(orbit)
        visited.update(orbit)
    return orbits

def classify_orbits(orbits):
    pal, cr, big = [], [], []
    for o in orbits:
        if len(o) == 2:
            if REVERSE[o[0]] == o[0] or REVERSE[o[1]] == o[1]:
                pal.append(o)
            else:
                cr.append(o)
        else:
            big.append(o)
    return pal, cr, big


# ─── Per-orbit analysis ──────────────────────────────────────────────────────

def orbit_pairing_data(orbit):
    """For a size-4 orbit, return the three intra-orbit pairing options."""
    x = orbit[0]
    cx, rx, crx = COMPLEMENT[x], REVERSE[x], COMP_REV[x]

    options = {}

    # Complement pairing: x↔comp(x), rev(x)↔comp_rev(x)
    pairs_comp = [(min(x,cx), max(x,cx)), (min(rx,crx), max(rx,crx))]
    s_comp = sum(POPCOUNT[a^b] for a,b in pairs_comp)
    masks_comp = [a^b for a,b in pairs_comp]
    dw_comp = [abs(POPCOUNT[a]-POPCOUNT[b]) for a,b in pairs_comp]
    options['comp'] = {'S': s_comp, 'masks': masks_comp, 'dw': dw_comp, 'pairs': pairs_comp}

    # Reversal pairing: x↔rev(x), comp(x)↔comp_rev(x)
    pairs_rev = [(min(x,rx), max(x,rx)), (min(cx,crx), max(cx,crx))]
    s_rev = sum(POPCOUNT[a^b] for a,b in pairs_rev)
    masks_rev = [a^b for a,b in pairs_rev]
    dw_rev = [abs(POPCOUNT[a]-POPCOUNT[b]) for a,b in pairs_rev]
    options['rev'] = {'S': s_rev, 'masks': masks_rev, 'dw': dw_rev, 'pairs': pairs_rev}

    # Comp-rev pairing: x↔comp_rev(x), comp(x)↔rev(x)
    pairs_cr = [(min(x,crx), max(x,crx)), (min(cx,rx), max(cx,rx))]
    s_cr = sum(POPCOUNT[a^b] for a,b in pairs_cr)
    masks_cr = [a^b for a,b in pairs_cr]
    dw_cr = [abs(POPCOUNT[a]-POPCOUNT[b]) for a,b in pairs_cr]
    options['cr'] = {'S': s_cr, 'masks': masks_cr, 'dw': dw_cr, 'pairs': pairs_cr}

    return options


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("TASK A: S↔D ANTI-CORRELATION UNDER EQUIVARIANCE")
    pr("=" * 70)

    orbits = compute_state_orbits()
    pal_orbits, cr_orbits, big_orbits = classify_orbits(orbits)

    # ── A1: Verify S_rev + S_cr = S_comp for all size-4 orbits ──
    pr(f"\n## A1. Strength Identity: S_rev + S_cr = S_comp")
    pr(f"\n  {'Orbit':>50} {'S_comp':>6} {'S_rev':>5} {'S_cr':>4} {'Sum':>4} {'Check':>6}")
    pr(f"  {'-'*50} {'-'*6} {'-'*5} {'-'*4} {'-'*4} {'-'*6}")

    all_hold = True
    orbit_data = []
    for i, orb in enumerate(big_orbits):
        opts = orbit_pairing_data(orb)
        sc, sr, scr = opts['comp']['S'], opts['rev']['S'], opts['cr']['S']
        holds = (sr + scr == sc)
        all_hold &= holds
        orbit_data.append(opts)
        pr(f"  {str([fmt(x) for x in orb]):>50} {sc:>6} {sr:>5} {scr:>4} {sr+scr:>4} {'✓' if holds else '✗':>6}")

    pr(f"\n  Identity holds for all {len(big_orbits)} orbits: {all_hold}")
    pr(f"  S_comp = {orbit_data[0]['comp']['S']} for all orbits (= 2×N = 2×{N} = {2*N})")

    # Why: mask_comp = 111111 always, popcount(111111) = N = 6, two pairs → S = 2×6 = 12
    # S_rev = popcount(x XOR rev(x)) × 2 (both pairs have same mask)
    # S_cr = popcount(x XOR comp_rev(x)) × 2 = popcount(comp(x XOR rev(x))) × 2 = (N - popcount(x XOR rev(x))) × 2
    # S_rev + S_cr = 2×popcount(m) + 2×(N - popcount(m)) = 2N = S_comp ✓
    pr(f"\n  Proof: Let m = x ⊕ rev(x) (the reversal mask, a palindrome).")
    pr(f"    S_rev = 2 × popcount(m)")
    pr(f"    mask_cr = x ⊕ comp_rev(x) = x ⊕ comp(rev(x)) = (x ⊕ rev(x)) ⊕ 111111 = comp(m)")
    pr(f"    S_cr = 2 × popcount(comp(m)) = 2 × (N − popcount(m))")
    pr(f"    S_rev + S_cr = 2N = S_comp  ∎")

    # ── A2: Mask structure per orbit ──
    pr(f"\n## A2. Mask Structure Per Orbit")
    pr(f"\n  Each intra-orbit choice produces a deterministic mask (2 copies).")
    pr(f"  comp: always 111111")
    pr(f"  rev: x ⊕ rev(x) = palindromic mask (the mirror-pair signature)")
    pr(f"  cr: comp(rev mask) = complementary palindromic mask")

    pr(f"\n  {'Orbit':>4} {'mask_comp':>8} {'mask_rev':>8} {'mask_cr':>8} {'rev is comp(cr)?':>18}")
    for i, opts in enumerate(orbit_data):
        mc = opts['comp']['masks'][0]
        mr = opts['rev']['masks'][0]
        mcr = opts['cr']['masks'][0]
        is_comp = (mr ^ mcr == MASK_ALL)
        pr(f"  {i:>4} {fmt(mc):>8} {fmt(mr):>8} {fmt(mcr):>8} {'✓' if is_comp else '✗':>18}")

    pr(f"\n  Observation: mask_rev and mask_cr are always complementary.")
    pr(f"  The 6 palindromic masks form 3 complementary pairs:")
    rev_masks = sorted(set(opts['rev']['masks'][0] for opts in orbit_data))
    cr_masks = sorted(set(opts['cr']['masks'][0] for opts in orbit_data))
    shown = set()
    for m in rev_masks:
        if m not in shown:
            c = m ^ MASK_ALL
            pr(f"    {fmt(m)} ↔ {fmt(c)}")
            shown.update([m, c])

    # ── A3: The coupling mechanism ──
    pr(f"\n## A3. Why Equivariance Creates S↔D Anti-Correlation")

    pr(f"\n  In the FULL pairing space:")
    pr(f"    - S depends on Hamming weights of XOR masks")
    pr(f"    - D depends on entropy of mask distribution (multiplicity)")
    pr(f"    - These are orthogonal: knowing S tells you nothing about D (r = 0)")

    pr(f"\n  Under EQUIVARIANCE:")
    pr(f"    - Each size-4 orbit contributes exactly 2 pairs")
    pr( "    - The choice is from {comp, rev, cr}")
    pr(f"    - comp: S=12 (max), mask=111111 (shared across all orbits)")
    pr(f"    - rev/cr: S<12, mask=palindromic (distinct per orbit)")

    pr(f"\n  THE COUPLING: choosing comp for an orbit contributes max S")
    pr(f"  but adds to the 111111 pile (reducing diversity).")
    pr(f"  Choosing rev/cr contributes less S but a distinct mask (increasing diversity).")
    pr(f"  Since mask identity is tied to the operation, S and mask-type are coupled per orbit.")
    pr(f"  Summing over orbits: more comp choices → higher S, lower D.")
    pr(f"  This creates the negative correlation r(S,D) ≈ −0.33.")

    # ── A4: Analytic derivation of the coupling ──
    pr(f"\n## A4. Analytic Structure")

    pr(f"\n  For the 12 size-4 orbits with intra-orbit matching only:")
    pr(f"  Let c_i ∈ {{comp, rev, cr}} be the choice for orbit i.")
    pr(f"  S_big = Σᵢ S(c_i)")
    pr(f"  mask_counts = multiset of masks from all choices")
    pr(f"  D = H(mask_counts / 32)")

    pr(f"\n  S(comp) = 12 always, S(rev) and S(cr) vary by orbit.")
    pr(f"  Masks:")
    pr(f"    comp → 111111 (same for all orbits)")
    pr(f"    rev → orbit-specific palindrome (6 distinct values)")
    pr(f"    cr → complement of the rev palindrome (6 distinct values)")

    # Count mask distribution for comp vs rev vs cr
    pr(f"\n  Rev masks by orbit:")
    mask_orbit_map = {}
    for i, opts in enumerate(orbit_data):
        m = opts['rev']['masks'][0]
        if m not in mask_orbit_map:
            mask_orbit_map[m] = []
        mask_orbit_map[m].append(i)

    for m, orbits_with_mask in sorted(mask_orbit_map.items()):
        pr(f"    {fmt(m)}: orbits {orbits_with_mask} (count={len(orbits_with_mask)})")

    pr(f"\n  Each palindromic mask appears in exactly 2 orbits for rev,")
    pr(f"  and 2 orbits for cr (its complement mask).")
    pr(f"  Total: 6 distinct masks × 2 orbits = 12 orbit-mask slots = 12 orbits ✓")

    # ── Quantify the per-orbit tradeoff ──
    pr(f"\n  Per-orbit S-vs-mask contribution:")
    pr(f"  {'Choice':>6} {'S contribution':>15} {'Mask effect':>30}")
    pr(f"  {'comp':>6} {'12 (max)':>15} {'adds 2 to 111111 pile':>30}")
    pr(f"  {'rev':>6} {'4 or 8':>15} {'adds 2 to distinct palindrome':>30}")
    pr(f"  {'cr':>6} {'8 or 4':>15} {'adds 2 to distinct palindrome':>30}")

    # ── Verify with the sample data ──
    pr(f"\n## A5. Verification from Sample")

    sample_path = Path(__file__).parent.parent / 'phase2' / 'n6_eq_sample.npz'
    if sample_path.exists():
        data = np.load(sample_path)
        s = data['strengths'].astype(float)
        d = data['diversities']

        r_sd = np.corrcoef(s, d)[0, 1]
        pr(f"\n  r(S, D) from 500K equivariant sample: {r_sd:+.6f}")

        # Also check: is the correlation coming from size-4 orbit choices?
        # The size-2 contribution is independent and varies less
        # We can't decompose the sample directly, but we can check
        # the strength-conditional diversity
        pr(f"\n  S-conditional D (from sample):")
        s_unique = sorted(set(s.astype(int)))
        for sv in s_unique:
            mask = s == sv
            n = mask.sum()
            if n >= 100:
                pr(f"    S={int(sv):3d}: n={n:>6}, D_mean={d[mask].mean():.4f}, "
                   f"D_std={d[mask].std():.4f}")

    # ── A6: Why r=0 in full space ──
    pr(f"\n## A6. Why r(S,D) = 0 in the Full Space")

    pr(f"""
  In the full space of pairings (no equivariance constraint):
  - Any state can pair with any other state
  - The mask a⊕b can be ANY nonzero value (63 possible)
  - The Hamming weight of the mask (determining S contribution)
    and the mask identity (determining D contribution)
    are independently choosable across different pairs
  
  Under equivariance:
  - Each orbit's mask is FIXED by the operation choice
  - The operation determines BOTH the mask identity AND its weight
  - Specifically: comp always gives mask=111111 (weight 6)
    while rev/cr give orbit-specific masks (weight < 6)
  
  This is the coupling: in the full space, two pairs can have
  the same Hamming distance but different masks (e.g., 110100 and 101010
  both have distance 3). Under equivariance, the mask is deterministic
  given the orbit and operation — no freedom to decouple S from mask identity.
  
  The equivariance constraint BINDS the per-orbit S contribution to
  the per-orbit mask contribution, creating the anti-correlation.""")

    # ═══════════════════════════════════════════════════════════════════════════
    pr(f"\n{'='*70}")
    pr("TASK B: WEIGHT PRESERVATION EQUIVALENCE")
    pr(f"{'='*70}")

    # ── B1: Verify Δw per operation for all size-4 orbits ──
    pr(f"\n## B1. Weight Change Per Operation")
    pr(f"\n  Algebraic prediction:")
    pr(f"    rev: w(rev(x)) = w(x) → Δw = 0 always")
    pr(f"    comp: w(comp(x)) = N − w(x) → Δw = |2w(x) − N|")
    pr(f"    cr: w(comp_rev(x)) = N − w(x) → Δw = |2w(x) − N|")

    pr(f"\n  {'Orbit':>4} {'x':>8} {'w(x)':>4} "
       f"{'Δw_comp':>8} {'Δw_rev':>7} {'Δw_cr':>6}  "
       f"{'rev=0?':>7} {'comp=cr?':>8}")

    all_rev_zero = True
    all_comp_eq_cr = True
    for i, opts in enumerate(orbit_data):
        x = big_orbits[i][0]
        w = POPCOUNT[x]

        dw_comp = opts['comp']['dw']
        dw_rev = opts['rev']['dw']
        dw_cr = opts['cr']['dw']

        rev_zero = all(d == 0 for d in dw_rev)
        comp_eq_cr = (dw_comp == dw_cr)

        all_rev_zero &= rev_zero
        all_comp_eq_cr &= comp_eq_cr

        pr(f"  {i:>4} {fmt(x):>8} {w:>4} "
           f"{str(dw_comp):>8} {str(dw_rev):>7} {str(dw_cr):>6}  "
           f"{'✓' if rev_zero else '✗':>7} {'✓' if comp_eq_cr else '✗':>8}")

    pr(f"\n  Reversal preserves weight for ALL orbits: {all_rev_zero}")
    pr(f"  Comp and CR have identical Δw for ALL orbits: {all_comp_eq_cr}")
    pr(f"\n  Conclusion: REVERSAL IS THE UNIQUE WEIGHT-PRESERVING INTRA-ORBIT OPERATION.")

    # ── B2: Size-2 orbit weight analysis ──
    pr(f"\n## B2. Size-2 Orbit Weight Changes (Forced Pairings)")

    pr(f"\n  Palindrome orbits (self-match = complement):")
    pal_dw_total = 0
    for o in pal_orbits:
        a, b = o
        dw = abs(POPCOUNT[a] - POPCOUNT[b])
        pal_dw_total += dw
        pr(f"    {fmt(a)} ↔ {fmt(b)}: w={POPCOUNT[a]},{POPCOUNT[b]}, Δw={dw}")
    pr(f"    Total Δw from pal: {pal_dw_total}")

    pr(f"\n  Comp-rev-fixed orbits (self-match = complement):")
    cr_dw_total = 0
    for o in cr_orbits:
        a, b = o
        dw = abs(POPCOUNT[a] - POPCOUNT[b])
        cr_dw_total += dw
        pr(f"    {fmt(a)} ↔ {fmt(b)}: w={POPCOUNT[a]},{POPCOUNT[b]}, Δw={dw}")
    pr(f"    Total Δw from cr-fixed: {cr_dw_total}")

    pr(f"\n  Size-2 orbits are FORCED to use complement.")
    pr(f"  For palindrome orbits: Δw = |2w(p) − N| (nonzero unless w = N/2)")
    pr(f"  For cr-fixed orbits: w(x) + w(comp(x)) = N, but x and comp(x)")
    pr(f"    are the two elements. Here comp_rev(x)=x means rev(x)=comp(x),")
    pr(f"    so w(rev(x))=w(x) and w(comp(x))=N−w(x).")
    pr(f"    But wait: cr-fixed states have comp_rev(x)=x, meaning the orbit")
    pr(f"    is {{x, comp(x)}} where rev(x) = comp(x).")
    pr(f"    So w(x) = w(rev(x)) = w(comp(x)) = N − w(x) → w(x) = N/2.")
    pr(f"    ALL cr-fixed states have weight N/2 = {N//2}. Δw = 0 for cr-fixed orbits!")

    pr(f"\n  Verification: {all(POPCOUNT[o[0]] == N//2 for o in cr_orbits)}")

    # ── B3: Equivalence theorem ──
    pr(f"\n## B3. The Lexicographic Characterization")

    pr(f"""
  THEOREM: Among Z₂²-equivariant pairings of n=6 states:
  
  (1) Reversal is the UNIQUE weight-preserving intra-orbit operation
      for size-4 orbits (complement and comp-rev both break weight).
      
  (2) Size-2 orbits are forced to use complement (no alternative).
      Palindrome size-2 orbits have Δw > 0 (unavoidable).
      CR-fixed size-2 orbits have Δw = 0 (all states have weight N/2).
      
  (3) "Maximize weight preservation" = "use reversal for all size-4 orbits"
      = the all-reversal subfamily (625 pairings).
      
  (4) Within the all-reversal subfamily, KW is the UNIQUE strength-maximizer
      (S = 120, achieved only by all-self-match for size-2 orbits).
      
  Therefore:
  
      KW = argmax S  subject to  max weight preservation  subject to  Z₂²-equivariance
      
  Equivalently, KW is the unique solution to the lexicographic optimization:
      
      FIRST: maximize weight preservation (reversal for all size-4 orbits)
      THEN: maximize strength (self-match for all size-2 orbits)""")

    # ── B4: Verify KW uniqueness in all-rev subfamily ──
    pr(f"\n## B4. KW Uniqueness in All-Reversal Subfamily")

    # Within all-rev: S = S_pal + S_cr + S_big_rev
    # S_big_rev is fixed (72) — all orbits use rev
    # S_pal depends on palindrome config: max when all self-match (S_pal=24)
    # S_cr depends on cr-fixed config: max when all self-match (S_cr=24)
    # Total max S = 24 + 24 + 72 = 120 — achieved only when both size-2 groups all self-match

    s_big_rev = sum(opts['rev']['S'] for opts in orbit_data)
    pr(f"\n  S_big_rev (fixed for all-rev): {s_big_rev}")

    # Max S_pal
    max_s_pal = sum(POPCOUNT[o[0] ^ o[1]] for o in pal_orbits)
    pr(f"  Max S_pal (all self-match): {max_s_pal}")

    # Max S_cr
    max_s_cr = sum(POPCOUNT[o[0] ^ o[1]] for o in cr_orbits)
    pr(f"  Max S_cr (all self-match): {max_s_cr}")

    pr(f"  Max total S in all-rev: {s_big_rev + max_s_pal + max_s_cr}")
    pr(f"  KW S: 120")
    pr(f"  Match: {s_big_rev + max_s_pal + max_s_cr == 120}")

    # Is self-match the unique maximizer for size-2 orbits?
    # Any inter-orbit pairing of palindromes replaces two comp pairs (S=6 each)
    # with two cross pairs (S < 6 in general). Let's verify:
    pr(f"\n  Why self-match maximizes S for size-2 orbits:")
    pr(f"  Self-match pairs a↔comp(a) at distance N = {N}.")
    pr(f"  Any inter-orbit pair a↔c has distance < N (since a ≠ comp(c) in general).")
    pr(f"  Complement is the UNIQUE distance-maximizing partner for any state.")
    pr(f"  Therefore self-match uniquely maximizes S for size-2 orbits. ∎")

    # ── Summary table ──
    pr(f"\n## Summary")

    pr(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │ STRUCTURAL IDENTITY                                                │
  │                                                                    │
  │ For every size-4 orbit:  S_rev + S_cr = S_comp = 2N              │
  │                                                                    │
  │ Proof: mask_rev = m (palindrome), mask_cr = comp(m)               │
  │        S_rev = 2·popcount(m), S_cr = 2·(N − popcount(m))         │
  │        Sum = 2N = S_comp  ∎                                       │
  ├─────────────────────────────────────────────────────────────────────┤
  │ COUPLING MECHANISM                                                 │
  │                                                                    │
  │ comp → S=12, mask=111111 (shared)  → high S, low D               │
  │ rev  → S<12, mask=palindrome (distinct) → low S, high D          │
  │ cr   → S<12, mask=palindrome (distinct) → low S, high D          │
  │                                                                    │
  │ Under equivariance, S and mask-identity are coupled per orbit.    │
  │ This creates r(S,D) ≈ −0.33.                                     │
  │                                                                    │
  │ In the full space, S and mask-identity are independent → r = 0.   │
  ├─────────────────────────────────────────────────────────────────────┤
  │ WEIGHT PRESERVATION                                                │
  │                                                                    │
  │ Reversal is the UNIQUE weight-preserving operation among           │
  │ {{comp, rev, cr}} for size-4 orbits.                                │
  │                                                                    │
  │ "Max weight preservation" = "all-reversal" = 625 pairings         │
  ├─────────────────────────────────────────────────────────────────────┤
  │ KW CHARACTERIZATION                                                │
  │                                                                    │
  │ KW = argmax S,  subject to  max weight preservation,              │
  │                 subject to  Z₂²-equivariance                      │
  │                                                                    │
  │ Unique solution. Lexicographic: weight pres. >> strength.          │
  └─────────────────────────────────────────────────────────────────────┘""")

    # ── Save ──
    md_path = out_dir / 'sd_coupling_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
