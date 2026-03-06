#!/usr/bin/env python3
"""
Opposition Theory — Phase 1: n=4 Structural Analysis

Computes:
- Z₂² orbit structure under {id, complement, reversal, comp∘rev}
- Palindromes, complement-fixed points
- Named pairings and their measures
- Equivariance analysis: which pairings are preserved under each group element
"""

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 4
NUM_STATES = 1 << N

POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]

def reverse_bits(x):
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    return r

def complement(x):
    return x ^ ((1 << N) - 1)

def comp_rev(x):
    return complement(reverse_bits(x))

REVERSE = [reverse_bits(x) for x in range(NUM_STATES)]
COMPLEMENT = [complement(x) for x in range(NUM_STATES)]
COMP_REV = [comp_rev(x) for x in range(NUM_STATES)]

def fmt(x):
    return format(x, f'0{N}b')


# ─── Orbit computation ───────────────────────────────────────────────────────

def compute_orbits():
    """Orbits under Z₂² = {id, complement, reversal, comp∘rev}."""
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = {x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]}
        orbits.append(sorted(orbit))
        visited |= orbit
    return orbits


# ─── Fixed points ─────────────────────────────────────────────────────────────

def find_fixed_points():
    palindromes = [x for x in range(NUM_STATES) if REVERSE[x] == x]
    comp_fixed = [x for x in range(NUM_STATES) if COMPLEMENT[x] == x]
    comprev_fixed = [x for x in range(NUM_STATES) if COMP_REV[x] == x]
    return palindromes, comp_fixed, comprev_fixed


# ─── Named pairings ──────────────────────────────────────────────────────────

def make_pairing(op):
    """Make a pairing by applying operation op: each x paired with op(x).
    Returns sorted tuple of pairs, or None if invalid (fixed points exist)."""
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        y = op(x)
        if y == x:
            return None  # Fixed point — not a valid pairing
        pairs.append((min(x, y), max(x, y)))
        seen.update((x, y))
    return tuple(sorted(pairs))


def make_kw_style():
    """Reversal for non-palindromes, complement for palindromes."""
    palindromes = {x for x in range(NUM_STATES) if REVERSE[x] == x}
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        y = COMPLEMENT[x] if x in palindromes else REVERSE[x]
        pairs.append((min(x, y), max(x, y)))
        seen.update((x, y))
    return tuple(sorted(pairs))


# ─── Measures ─────────────────────────────────────────────────────────────────

def pairing_measures(pairs):
    """Compute all 5 measures for a pairing."""
    strength = sum(POPCOUNT[a ^ b] for a, b in pairs)

    masks = [a ^ b for a, b in pairs]
    mask_counts = Counter(masks)
    entropy = max(0.0, -sum((c/8) * math.log2(c/8) for c in mask_counts.values()))

    abs_diffs = [abs(POPCOUNT[a] - POPCOUNT[b]) for a, b in pairs]
    weight_tilt = sum(abs_diffs) / 8

    pair_set = {(min(a,b), max(a,b)) for a,b in pairs}
    rev_sym = sum(1 for a,b in pairs if (min(REVERSE[a],REVERSE[b]), max(REVERSE[a],REVERSE[b])) in pair_set)

    wa = np.array([POPCOUNT[a] for a,b in pairs], dtype=float)
    wb = np.array([POPCOUNT[b] for a,b in pairs], dtype=float)
    if wa.std() == 0 or wb.std() == 0:
        wcorr = 0.0
    else:
        wcorr = float(np.corrcoef(wa, wb)[0, 1])

    return {
        'strength': strength,
        'diversity': round(entropy, 6),
        'weight_tilt': round(weight_tilt, 4),
        'reversal_symmetry': rev_sym,
        'weight_corr': round(wcorr, 6),
        'masks': mask_counts,
    }


# ─── Equivariance ────────────────────────────────────────────────────────────

def is_equivariant(pairs, op_table):
    """Check if applying op to both members of every pair yields another pair in the pairing."""
    pair_set = {(min(a,b), max(a,b)) for a,b in pairs}
    for a, b in pairs:
        oa, ob = op_table[a], op_table[b]
        if (min(oa,ob), max(oa,ob)) not in pair_set:
            return False
    return True


def count_equivariant_pairings():
    """Count pairings equivariant under each group element by loading all pairings."""
    # We need the enumeration — check if measures.npz exists, otherwise
    # just check named pairings
    pass  # Will be done after enumeration in enumerate.py


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("n=4 STRUCTURAL ANALYSIS")
    pr("=" * 70)

    # ── Orbits ──
    orbits = compute_orbits()
    pr(f"\n## Z₂² Orbit Structure")
    pr(f"\nGroup: {{id, complement, reversal, comp∘rev}} acting on {{0,...,15}}")
    pr(f"Total orbits: {len(orbits)}")

    size_dist = Counter(len(o) for o in orbits)
    pr(f"Orbit sizes: {dict(size_dist)}")

    pr(f"\nAll orbits:")
    for i, orbit in enumerate(orbits):
        strs = [fmt(x) for x in orbit]
        weights = [POPCOUNT[x] for x in orbit]
        pr(f"  Orbit {i+1:2d} (size {len(orbit)}): {', '.join(strs)}  "
           f"weights: {weights}")

    # ── Fixed points ──
    palindromes, comp_fixed, comprev_fixed = find_fixed_points()

    pr(f"\n## Fixed Points")
    pr(f"\nPalindromes (reversal-fixed): {len(palindromes)}")
    for p in palindromes:
        pr(f"  {fmt(p)}  (weight {POPCOUNT[p]}, complement = {fmt(COMPLEMENT[p])})")

    pr(f"\nComplement-fixed: {len(comp_fixed)}")
    if comp_fixed:
        for x in comp_fixed:
            pr(f"  {fmt(x)}")
    else:
        pr(f"  (none — complement has no fixed points at even n)")

    pr(f"\nComp∘rev-fixed: {len(comprev_fixed)}")
    if comprev_fixed:
        for x in comprev_fixed:
            pr(f"  {fmt(x)}")
    else:
        pr(f"  (none)")

    # ── Palindrome structure ──
    pr(f"\n## Palindrome Analysis")
    pr(f"\nPalindromes at n=4 have form L1 L2 L2 L1 (L2↔L3 and L1↔L4 match).")
    pr(f"So 2² = 4 palindromes. They form 2 complement pairs:")
    pal_pairs = []
    seen = set()
    for p in palindromes:
        if p in seen:
            continue
        c = COMPLEMENT[p]
        pal_pairs.append((min(p,c), max(p,c)))
        seen.update((p, c))
    for a, b in pal_pairs:
        pr(f"  {fmt(a)} ↔ {fmt(b)}  (dist {POPCOUNT[a^b]})")

    pr(f"\nNon-palindromes: {NUM_STATES - len(palindromes)} states forming "
       f"{(NUM_STATES - len(palindromes))//2} reversal pairs")

    # ── Named pairings ──
    pr(f"\n## Named Pairings")

    comp_pair = make_pairing(lambda x: COMPLEMENT[x])
    rev_pair = make_pairing(lambda x: REVERSE[x])
    cr_pair = make_pairing(lambda x: COMP_REV[x])
    kw_pair = make_kw_style()

    rev_fixed = [fmt(x) for x in range(NUM_STATES) if REVERSE[x] == x]
    cr_fixed = [fmt(x) for x in range(NUM_STATES) if COMP_REV[x] == x]

    named = [
        ("Complement", comp_pair, None),
        ("Reversal", rev_pair,
         f"4 palindromes are fixed under reversal ({', '.join(rev_fixed)})"),
        ("Comp∘Rev", cr_pair,
         f"4 anti-palindromes are fixed under comp∘rev ({', '.join(cr_fixed)})"),
        ("KW-style (rev + comp for palindromes)", kw_pair, None),
    ]

    for name, pair, invalid_reason in named:
        pr(f"\n### {name}")
        if pair is None:
            pr(f"  INVALID — {invalid_reason}")
            continue

        pr(f"  Pairs:")
        for a, b in pair:
            pr(f"    {fmt(a)} ↔ {fmt(b)}  XOR={fmt(a^b)} dist={POPCOUNT[a^b]} "
               f"Δw={abs(POPCOUNT[a]-POPCOUNT[b])}")

        m = pairing_measures(pair)
        pr(f"  Measures:")
        pr(f"    Strength:          {m['strength']}")
        pr(f"    Diversity:         {m['diversity']:.6f}")
        pr(f"    Weight Tilt:       {m['weight_tilt']:.4f}")
        pr(f"    Reversal Symmetry: {m['reversal_symmetry']}/8")
        pr(f"    Weight Correlation:{m['weight_corr']:+.6f}")
        pr(f"    Mask distribution: {dict((fmt(k), v) for k,v in sorted(m['masks'].items()))}")

    # ── Equivariance check for named pairings ──
    pr(f"\n## Equivariance of Named Pairings")
    pr(f"\nA pairing is equivariant under g if applying g to both members of every")
    pr(f"pair produces another pair in the same pairing.")

    ops = [
        ("complement", COMPLEMENT),
        ("reversal", REVERSE),
        ("comp∘rev", COMP_REV),
    ]

    for name, pair, _ in named:
        if pair is None:
            continue
        pr(f"\n  {name}:")
        for op_name, op_table in ops:
            eq = is_equivariant(pair, op_table)
            pr(f"    equivariant under {op_name}: {eq}")

    # ── Check if comp∘rev is same as reversal or complement ──
    pr(f"\n## Relationships Between Named Pairings")
    if comp_pair and cr_pair:
        pr(f"  Complement == Comp∘Rev? {comp_pair == cr_pair}")
    if kw_pair and comp_pair:
        pr(f"  KW-style == Complement? {kw_pair == comp_pair}")
    if kw_pair and cr_pair:
        pr(f"  KW-style == Comp∘Rev?   {kw_pair == cr_pair}")

    # ── Equivariant pairing counting (full enumeration) ──
    pr(f"\n## Equivariant Pairing Counts")
    pr(f"\nCounting pairings equivariant under each group element requires")
    pr(f"checking all 2,027,025 pairings. Running enumeration...")

    from enumerate import enumerate_pairings
    import time
    t0 = time.time()
    pairings = enumerate_pairings()
    t1 = time.time()
    pr(f"  Enumeration: {t1-t0:.1f}s")

    eq_counts = {op_name: 0 for op_name, _ in ops}
    eq_all = 0  # equivariant under all three
    for pairing in pairings:
        results = {}
        for op_name, op_table in ops:
            results[op_name] = is_equivariant(pairing, op_table)
            if results[op_name]:
                eq_counts[op_name] += 1
        if all(results.values()):
            eq_all += 1

    pr(f"\n  Equivariant counts (out of {len(pairings):,}):")
    for op_name in eq_counts:
        pr(f"    under {op_name:>10}: {eq_counts[op_name]:>6,}")
    pr(f"    under all three:  {eq_all:>6,}")

    # ── Save structure.md ──
    md_path = out_dir / 'structure.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
