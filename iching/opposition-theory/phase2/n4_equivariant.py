#!/usr/bin/env python3
"""
Phase 2: n=4 Equivariant Pairing Analysis

Identifies all 117 Z₂²-equivariant pairings, computes their measures,
and characterizes the structural landscape.

Key questions:
  1. Do equivariant pairings pair only within orbits, or across?
  2. What is the S×D distribution among the 117?
  3. Is KW unique within the equivariant family?
"""

import math
import sys
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 4
NUM_STATES = 1 << N  # 16
NUM_PAIRS = NUM_STATES // 2  # 8
MASK_ALL = (1 << N) - 1

POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]

def _reverse(x):
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    return r

REVERSE = [_reverse(x) for x in range(NUM_STATES)]
COMPLEMENT = [x ^ MASK_ALL for x in range(NUM_STATES)]
COMP_REV = [COMPLEMENT[REVERSE[x]] for x in range(NUM_STATES)]

def fmt(x):
    return format(x, f'0{N}b')


# ─── Orbit computation ───────────────────────────────────────────────────────

def compute_orbits():
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]})
        orbits.append(orbit)
        visited.update(orbit)
    return orbits


# ─── Enumeration ──────────────────────────────────────────────────────────────

def enumerate_all_pairings():
    """Generate all perfect matchings of {0..15} into 8 pairs."""
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


def is_equivariant(pairs, op):
    """Check if applying op to both members of every pair yields another pair."""
    pair_set = {(min(a,b), max(a,b)) for a,b in pairs}
    for a, b in pairs:
        oa, ob = op[a], op[b]
        if (min(oa,ob), max(oa,ob)) not in pair_set:
            return False
    return True


def is_fully_equivariant(pairs):
    return (is_equivariant(pairs, COMPLEMENT) and
            is_equivariant(pairs, REVERSE) and
            is_equivariant(pairs, COMP_REV))


# ─── Measures ─────────────────────────────────────────────────────────────────

def compute_measures(pairs):
    """Returns (strength, diversity, weight_tilt, weight_corr)."""
    strength = sum(POPCOUNT[a ^ b] for a, b in pairs)

    masks = [a ^ b for a, b in pairs]
    mask_counts = Counter(masks)
    entropy = max(0.0, -sum((c/NUM_PAIRS) * math.log2(c/NUM_PAIRS)
                             for c in mask_counts.values()))

    abs_diffs = [abs(POPCOUNT[a] - POPCOUNT[b]) for a, b in pairs]
    weight_tilt = sum(abs_diffs) / NUM_PAIRS

    wa = np.array([POPCOUNT[a] for a, b in pairs], dtype=float)
    wb = np.array([POPCOUNT[b] for a, b in pairs], dtype=float)
    if wa.std() == 0 or wb.std() == 0:
        weight_corr = 0.0
    else:
        weight_corr = float(np.corrcoef(wa, wb)[0, 1])

    return strength, round(entropy, 6), round(weight_tilt, 4), round(weight_corr, 6), mask_counts


# ─── Structural analysis ─────────────────────────────────────────────────────

def classify_pair(a, b):
    """Classify a pair by which group operation maps a→b."""
    ops = []
    if COMPLEMENT[a] == b or COMPLEMENT[b] == a:
        ops.append('comp')
    if REVERSE[a] == b or REVERSE[b] == a:
        ops.append('rev')
    if COMP_REV[a] == b or COMP_REV[b] == a:
        ops.append('comp_rev')
    return '+'.join(ops) if ops else 'none'


def orbit_of(x):
    return tuple(sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]}))


def analyze_inter_orbit(pairs, orbits):
    """Check if any pair crosses orbit boundaries."""
    orbit_map = {}
    for orb in orbits:
        for x in orb:
            orbit_map[x] = tuple(orb)
    
    intra = 0
    inter = 0
    inter_details = []
    for a, b in pairs:
        if orbit_map[a] == orbit_map[b]:
            intra += 1
        else:
            inter += 1
            inter_details.append((a, b, orbit_map[a], orbit_map[b]))
    return intra, inter, inter_details


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("PHASE 2: n=4 EQUIVARIANT PAIRING ANALYSIS")
    pr("=" * 70)

    orbits = compute_orbits()
    pr(f"\nOrbits ({len(orbits)}):")
    for i, orb in enumerate(orbits):
        pr(f"  O{i}: size {len(orb)} — {', '.join(fmt(x) for x in orb)}")

    # Classify orbits
    size2_orbits = [o for o in orbits if len(o) == 2]
    size4_orbits = [o for o in orbits if len(o) == 4]
    pr(f"\n  Size-2 orbits: {len(size2_orbits)}")
    pr(f"  Size-4 orbits: {len(size4_orbits)}")

    # ── Enumerate all pairings, filter equivariant ──
    pr(f"\nEnumerating all pairings...")
    t0 = time.time()
    all_pairings = enumerate_all_pairings()
    pr(f"  Total: {len(all_pairings):,} ({time.time()-t0:.1f}s)")

    pr(f"\nFiltering for full Z₂²-equivariance...")
    t0 = time.time()
    eq_pairings = [p for p in all_pairings if is_fully_equivariant(p)]
    pr(f"  Found: {len(eq_pairings)} ({time.time()-t0:.1f}s)")

    # ── Q1: Do any pair across orbits? ──
    pr(f"\n{'='*70}")
    pr("Q1: INTRA-ORBIT vs INTER-ORBIT PAIRING")
    pr(f"{'='*70}")

    has_inter = 0
    max_inter = 0
    for pairing in eq_pairings:
        intra, inter, details = analyze_inter_orbit(pairing, orbits)
        if inter > 0:
            has_inter += 1
            max_inter = max(max_inter, inter)

    pr(f"\n  Pairings with inter-orbit pairs: {has_inter} / {len(eq_pairings)}")
    pr(f"  Max inter-orbit pairs in any pairing: {max_inter}")

    if has_inter > 0:
        pr(f"\n  Inter-orbit pairing IS possible among equivariant pairings.")
        pr(f"  This explains why count (117) exceeds per-orbit product (9).")
        
        # Show a few examples
        pr(f"\n  Examples of inter-orbit equivariant pairings:")
        shown = 0
        for pairing in eq_pairings:
            intra, inter, details = analyze_inter_orbit(pairing, orbits)
            if inter > 0 and shown < 3:
                pr(f"\n  Pairing (inter={inter}):")
                for a, b in pairing:
                    oa, ob = orbit_of(a), orbit_of(b)
                    tag = "INTER" if oa != ob else "intra"
                    pr(f"    {fmt(a)} ↔ {fmt(b)}  [{tag}]  "
                       f"type={classify_pair(a,b)}")
                shown += 1
    else:
        pr(f"\n  All equivariant pairings pair within orbits.")

    # ── Detailed orbit pairing structure ──
    pr(f"\n{'='*70}")
    pr("ORBIT PAIRING PATTERNS")
    pr(f"{'='*70}")

    # For each equivariant pairing, record which orbits are paired together
    orbit_map = {}
    for orb in orbits:
        for x in orb:
            orbit_map[x] = tuple(orb)

    orbit_pairing_patterns = Counter()
    for pairing in eq_pairings:
        # For each pair, record (orbit_of_a, orbit_of_b) canonically
        orbit_pairs = []
        for a, b in pairing:
            oa, ob = orbit_map[a], orbit_map[b]
            orbit_pairs.append(tuple(sorted([oa, ob])))
        orbit_pairing_patterns[tuple(sorted(orbit_pairs))] += 1

    pr(f"\n  Distinct orbit-level pairing patterns: {len(orbit_pairing_patterns)}")
    for pattern, count in orbit_pairing_patterns.most_common():
        # Summarize: how many intra vs inter orbit pairings
        intra = sum(1 for oa, ob in pattern if oa == ob)
        inter = sum(1 for oa, ob in pattern if oa != ob)
        pr(f"    count={count}: {intra} intra-orbit + {inter} inter-orbit pairs")

    # ── Q2: Measures for all 117 ──
    pr(f"\n{'='*70}")
    pr("Q2: MEASURES FOR ALL EQUIVARIANT PAIRINGS")
    pr(f"{'='*70}")

    results = []
    for pairing in eq_pairings:
        s, d, wt, wc, masks = compute_measures(pairing)
        results.append({
            'pairing': pairing,
            'S': s, 'D': d, 'WT': wt, 'WC': wc,
            'masks': masks,
        })

    strengths = [r['S'] for r in results]
    diversities = [r['D'] for r in results]
    weight_corrs = [r['WC'] for r in results]

    # S distribution
    pr(f"\n  Strength distribution:")
    s_counts = Counter(strengths)
    for s_val in sorted(s_counts):
        pr(f"    S={s_val:2d}: {s_counts[s_val]:>3} pairings")

    # D distribution
    pr(f"\n  Diversity distribution:")
    d_counts = Counter(diversities)
    for d_val in sorted(d_counts):
        pr(f"    D={d_val:.6f}: {d_counts[d_val]:>3} pairings")

    # S×D cross-tabulation
    pr(f"\n  S × D cross-tabulation:")
    sd_counts = Counter((r['S'], r['D']) for r in results)
    pr(f"    {'S':>4}  {'D':>10}  {'count':>5}")
    for (s, d) in sorted(sd_counts):
        pr(f"    {s:>4}  {d:>10.6f}  {sd_counts[(s,d)]:>5}")

    # ── Q3: Does S uniquely identify KW/complement? ──
    pr(f"\n{'='*70}")
    pr("Q3: UNIQUENESS ANALYSIS")
    pr(f"{'='*70}")

    # KW-style pairing
    kw_pairs = []
    seen = set()
    palindromes = {x for x in range(NUM_STATES) if REVERSE[x] == x}
    for x in range(NUM_STATES):
        if x in seen:
            continue
        partner = COMPLEMENT[x] if x in palindromes else REVERSE[x]
        kw_pairs.append((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    kw_pairing = tuple(sorted(kw_pairs))

    comp_pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        c = COMPLEMENT[x]
        comp_pairs.append((min(x, c), max(x, c)))
        seen.update((x, c))
    comp_pairing = tuple(sorted(comp_pairs))

    # Find KW and complement in equivariant set
    kw_found = False
    comp_found = False
    for r in results:
        p_sorted = tuple(sorted(r['pairing']))
        if p_sorted == kw_pairing:
            kw_found = True
            kw_r = r
        if p_sorted == comp_pairing:
            comp_found = True
            comp_r = r

    pr(f"\n  KW-style found in equivariant set: {kw_found}")
    if kw_found:
        pr(f"    S={kw_r['S']}, D={kw_r['D']}, WT={kw_r['WT']}, WC={kw_r['WC']}")
    pr(f"  Complement found in equivariant set: {comp_found}")
    if comp_found:
        pr(f"    S={comp_r['S']}, D={comp_r['D']}, WT={comp_r['WT']}, WC={comp_r['WC']}")

    # Max S
    max_s = max(strengths)
    max_s_pairings = [r for r in results if r['S'] == max_s]
    pr(f"\n  Max S among equivariant: {max_s}")
    pr(f"    Count at max S: {len(max_s_pairings)}")
    pr(f"    Is complement the unique S-maximizer? "
       f"{len(max_s_pairings) == 1 and comp_found}")

    # Second-highest S
    second_s = sorted(set(strengths), reverse=True)[1] if len(set(strengths)) > 1 else None
    if second_s is not None:
        second_s_pairings = [r for r in results if r['S'] == second_s]
        pr(f"\n  Second-highest S: {second_s}")
        pr(f"    Count: {len(second_s_pairings)}")
        # Check if KW is among them
        kw_in_second = any(tuple(sorted(r['pairing'])) == kw_pairing
                          for r in second_s_pairings)
        pr(f"    KW among them: {kw_in_second}")

    # Max D at each S level among equivariant
    pr(f"\n  Max D at each S level (equivariant only):")
    for s_val in sorted(set(strengths), reverse=True):
        ds_at_s = [r['D'] for r in results if r['S'] == s_val]
        pr(f"    S={s_val:2d}: max D = {max(ds_at_s):.6f}, "
           f"min D = {min(ds_at_s):.6f}, n={len(ds_at_s)}")

    # ── Pareto analysis within equivariant set ──
    pr(f"\n  2D Pareto frontier (max S, max D) within equivariant set:")
    pareto = []
    for r in results:
        dominated = False
        for r2 in results:
            if (r2['S'] > r['S'] and r2['D'] >= r['D']) or \
               (r2['S'] >= r['S'] and r2['D'] > r['D']):
                dominated = True
                break
        if not dominated:
            pareto.append(r)
    pareto.sort(key=lambda r: -r['S'])
    for r in pareto:
        p_sorted = tuple(sorted(r['pairing']))
        is_kw = " ← KW" if p_sorted == kw_pairing else ""
        is_comp = " ← COMP" if p_sorted == comp_pairing else ""
        pr(f"    S={r['S']}, D={r['D']:.6f}{is_kw}{is_comp}")

    # ── Q4: Structural classification ──
    pr(f"\n{'='*70}")
    pr("Q4: STRUCTURAL CLASSIFICATION")
    pr(f"{'='*70}")

    # For each equivariant pairing, classify each pair
    structure_types = Counter()
    for r in results:
        pair_types = tuple(sorted(classify_pair(a, b) for a, b in r['pairing']))
        structure_types[pair_types] += 1

    pr(f"\n  Distinct pair-type signatures: {len(structure_types)}")
    for sig, count in structure_types.most_common():
        type_counts = Counter(sig)
        summary = ', '.join(f'{t}:{c}' for t, c in sorted(type_counts.items()))
        pr(f"    n={count:>3}: {summary}")

    # ── Size-2 orbit pairing freedom ──
    pr(f"\n{'='*70}")
    pr("ANALYSIS: SIZE-2 ORBIT PAIRING FREEDOM")
    pr(f"{'='*70}")

    # The 4 size-2 orbits are: {0000,1111}, {0011,1100}, {0101,1010}, {0110,1001}
    # Within each, the two elements are complements.
    # But could we pair across? E.g., 0011↔0101 and 1100↔1010?
    # Check: comp maps (0011,0101)→(1100,1010) — need (1100,1010) to also be a pair.
    # If we pair 0011↔0101 and 1100↔1010, then comp maps both correctly. ✓
    # rev maps 0011↔1100 and 0101↔1010 — but 0011 is paired with 0101, not 1100.
    # Need: rev(0011)=1100, rev(0101)=1010 → pair (1100,1010) — that IS in our set. ✓
    # comp∘rev maps 0011→comp(1100)=0011 (fixed!), and 0101→comp(1010)=0101 (fixed!)
    # So comp_rev(0011)=0011 and comp_rev(0101)=0101 → pair (0011,0101) → (0011,0101). ✓
    # So this cross-orbit pairing IS equivariant!

    pr(f"\n  Size-2 orbits contain states from the complement-pair relationship.")
    pr(f"  But equivariant cross-pairing between size-2 orbits is possible")
    pr(f"  when reversal maps one orbit to another.")
    pr(f"\n  Size-2 orbit reversal relationships:")
    for orb in size2_orbits:
        rev_orb = tuple(sorted({REVERSE[x] for x in orb}))
        cr_orb = tuple(sorted({COMP_REV[x] for x in orb}))
        pr(f"    {[fmt(x) for x in orb]} → rev:{[fmt(x) for x in rev_orb]}, "
           f"cr:{[fmt(x) for x in cr_orb]}")

    # Map out the action of each group element on size-2 orbits
    orb_tuples = [tuple(o) for o in size2_orbits]
    pr(f"\n  Group action on size-2 orbits:")
    for ot in orb_tuples:
        rev_ot = tuple(sorted({REVERSE[x] for x in ot}))
        comp_ot = tuple(sorted({COMPLEMENT[x] for x in ot}))
        cr_ot = tuple(sorted({COMP_REV[x] for x in ot}))
        pr(f"    {[fmt(x) for x in ot]}: "
           f"rev→{[fmt(x) for x in rev_ot]}, "
           f"comp→{[fmt(x) for x in comp_ot]}, "
           f"cr→{[fmt(x) for x in cr_ot]}")

    # ── Summary ──
    pr(f"\n{'='*70}")
    pr("SUMMARY")
    pr(f"{'='*70}")

    pr(f"\n  Total Z₂²-equivariant pairings at n=4: {len(eq_pairings)}")
    pr(f"  Inter-orbit pairing possible: {'Yes' if has_inter else 'No'}")
    pr(f"  Unique S-maximizer (complement): {len(max_s_pairings) == 1}")
    if kw_found:
        pr(f"  KW: S={kw_r['S']}, D={kw_r['D']}")
        kw_s_rank = sum(1 for s in strengths if s > kw_r['S']) + 1
        kw_d_rank = sum(1 for d in diversities if d > kw_r['D']) + 1
        pr(f"  KW S-rank among equivariant: {kw_s_rank}/{len(eq_pairings)}")
        pr(f"  KW D-rank among equivariant: {kw_d_rank}/{len(eq_pairings)}")
    pr(f"  Pareto frontier size: {len(pareto)}")

    # ── Save results ──
    md_path = out_dir / 'n4_equivariant_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
