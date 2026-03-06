#!/usr/bin/env python3
"""
Phase 2 Closure: Equivariant Landscape Under the Full Stabilizer

The KW pairing's stabilizer in B₆ has order 384.
How many pairings are equivariant under this full group?
If the answer is small, the characterization simplifies dramatically.
"""

import math
import time
from collections import Counter
from itertools import permutations
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


# ─── Build the 384-element stabilizer ────────────────────────────────────────

def apply_b6(x, perm, flip_mask):
    result = 0
    for out_pos in range(N):
        in_pos = perm[out_pos]
        bit = (x >> in_pos) & 1
        result |= bit << out_pos
    return result ^ flip_mask


def make_kw_pairing():
    palindrome_set = {x for x in range(NUM_STATES) if REVERSE[x] == x}
    pairs = set()
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        partner = COMPLEMENT[x] if x in palindrome_set else REVERSE[x]
        pairs.add((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    return frozenset(pairs)


def build_stabilizer():
    """Find all B₆ elements preserving KW. Returns list of permutation tables."""
    kw = make_kw_pairing()
    stabilizer = []

    for perm in permutations(range(N)):
        for flip_int in range(1 << N):
            sigma = [apply_b6(x, perm, flip_int) for x in range(NUM_STATES)]
            # Check if sigma preserves KW
            ok = True
            for a, b in kw:
                sa, sb = sigma[a], sigma[b]
                if (min(sa, sb), max(sa, sb)) not in kw:
                    ok = False
                    break
            if ok:
                stabilizer.append(sigma)

    return stabilizer


# ─── Orbit computation ───────────────────────────────────────────────────────

def compute_state_orbits(group):
    """Orbits of {0,...,63} under the group action."""
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = set()
        for sigma in group:
            orbit.add(sigma[x])
        orbits.append(sorted(orbit))
        visited |= orbit
    return orbits


def compute_pair_orbits(group):
    """Orbits of unordered pairs {a,b} under g·{a,b} = {g(a), g(b)}."""
    visited = set()
    pair_orbits = []

    for a in range(NUM_STATES):
        for b in range(a + 1, NUM_STATES):
            if (a, b) in visited:
                continue
            orbit = set()
            for sigma in group:
                sa, sb = sigma[a], sigma[b]
                orbit.add((min(sa, sb), max(sa, sb)))
            pair_orbits.append(frozenset(orbit))
            visited |= orbit

    return pair_orbits


# ─── Exact cover solver (bitset) ─────────────────────────────────────────────

def solve_exact_cover(pair_orbits_valid, orbit_masks, orbit_npairs):
    """Find all ways to select pair-orbits covering all 64 states exactly once."""
    n_valid = len(orbit_masks)

    state_to_vorbits = [[] for _ in range(NUM_STATES)]
    for vi in range(n_valid):
        mask = orbit_masks[vi]
        for s in range(NUM_STATES):
            if mask & (1 << s):
                state_to_vorbits[s].append(vi)

    ALL_BITS = (1 << NUM_STATES) - 1
    solutions = []

    def backtrack(remaining, chosen, pairs_so_far):
        if remaining == 0:
            if pairs_so_far == NUM_PAIRS:
                solutions.append(chosen[:])
            return
        if pairs_so_far >= NUM_PAIRS:
            return

        # MRV: find state with fewest covering options
        best_state = -1
        best_count = 999
        s = remaining
        while s:
            bit = s & (-s)
            state = bit.bit_length() - 1
            count = sum(1 for vi in state_to_vorbits[state]
                        if (orbit_masks[vi] & remaining) == orbit_masks[vi])
            if count < best_count:
                best_count = count
                best_state = state
                if count <= 1:
                    break
            s ^= bit

        if best_count == 0:
            return

        for vi in state_to_vorbits[best_state]:
            m = orbit_masks[vi]
            if (m & remaining) == m:
                chosen.append(vi)
                backtrack(remaining ^ m, chosen, pairs_so_far + orbit_npairs[vi])
                chosen.pop()

    backtrack(ALL_BITS, [], 0)
    return solutions


# ─── Measures ─────────────────────────────────────────────────────────────────

def compute_measures(pairs):
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

    return strength, round(entropy, 6), round(weight_tilt, 4), round(weight_corr, 6)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("EQUIVARIANT LANDSCAPE UNDER FULL 384-ELEMENT STABILIZER")
    pr("=" * 70)

    # ── Build stabilizer ──
    pr(f"\nBuilding stabilizer...")
    t0 = time.time()
    group = build_stabilizer()
    pr(f"  |Stab| = {len(group)} ({time.time()-t0:.1f}s)")

    kw_pairs = make_kw_pairing()

    # ── Step 1: State orbits ──
    pr(f"\n## Step 1: State Orbits Under 384-Element Group")

    state_orbits = compute_state_orbits(group)
    pr(f"\n  Number of orbits: {len(state_orbits)}")

    size_dist = Counter(len(o) for o in state_orbits)
    pr(f"  Size distribution: {dict(sorted(size_dist.items()))}")

    for i, orb in enumerate(state_orbits):
        weights = [POPCOUNT[x] for x in orb]
        weight_dist = Counter(weights)
        pr(f"  O{i:2d} (size {len(orb):2d}): "
           f"weights={dict(sorted(weight_dist.items()))}, "
           f"states=[{', '.join(fmt(x) for x in orb[:8])}"
           f"{'...' if len(orb) > 8 else ''}]")

    # Compare with Z₂² orbits
    pr(f"\n  Comparison with Z₂² (4 elements):")
    visited = set()
    z2_orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]})
        z2_orbits.append(orbit)
        visited.update(orbit)
    pr(f"    Z₂² orbits: {len(z2_orbits)} (sizes: {dict(Counter(len(o) for o in z2_orbits))})")
    pr(f"    Full stabilizer orbits: {len(state_orbits)} (sizes: {dict(sorted(size_dist.items()))})")

    # ── Step 2: Pair orbits ──
    pr(f"\n## Step 2: Pair Orbits Under 384-Element Group")

    t0 = time.time()
    pair_orbits = compute_pair_orbits(group)
    pr(f"\n  Total pair-orbits: {len(pair_orbits)} ({time.time()-t0:.1f}s)")

    po_sizes = Counter(len(po) for po in pair_orbits)
    pr(f"  Size distribution: {dict(sorted(po_sizes.items()))}")

    # Filter valid (no internal state overlap)
    valid_po = []
    valid_masks = []
    valid_npairs = []
    for po in pair_orbits:
        mask = 0
        valid = True
        for a, b in po:
            bit_a = 1 << a
            bit_b = 1 << b
            if mask & (bit_a | bit_b):
                valid = False
                break
            mask |= bit_a | bit_b
        if valid:
            valid_po.append(po)
            valid_masks.append(mask)
            valid_npairs.append(len(po))

    pr(f"  Valid (no internal overlap): {len(valid_po)} / {len(pair_orbits)}")
    pr(f"  Valid pair-orbit sizes: {dict(sorted(Counter(len(po) for po in valid_po).items()))}")

    # Show details
    for i, po in enumerate(valid_po):
        states = set()
        for a, b in po:
            states.add(a)
            states.add(b)
        s_contrib = sum(POPCOUNT[a ^ b] for a, b in po)
        masks = set(a ^ b for a, b in po)
        pr(f"    PO{i:2d}: {len(po):3d} pairs, {len(states):3d} states, "
           f"S_contrib={s_contrib:3d}, masks={sorted(fmt(m) for m in masks)}")

    # ── Step 3: Enumerate equivariant pairings ──
    pr(f"\n## Step 3: Enumerate Equivariant Pairings")

    t0 = time.time()
    solutions = solve_exact_cover(valid_po, valid_masks, valid_npairs)
    elapsed = time.time() - t0
    pr(f"\n  Solutions found: {len(solutions)} ({elapsed:.2f}s)")

    # Convert to actual pairings
    pairings = []
    for sol in solutions:
        pairs = []
        for idx in sol:
            pairs.extend(valid_po[idx])
        pairings.append(sorted(pairs))

    # Verify uniqueness
    pairing_set = set(tuple(p) for p in pairings)
    pr(f"  Distinct pairings: {len(pairing_set)}")

    # ── Step 4: Analyze each ──
    pr(f"\n## Step 4: Measures for Each Equivariant Pairing")

    kw_tuple = tuple(sorted(kw_pairs))

    comp_pairs_list = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        c = COMPLEMENT[x]
        comp_pairs_list.append((min(x, c), max(x, c)))
        seen.update((x, c))
    comp_tuple = tuple(sorted(comp_pairs_list))

    for i, p in enumerate(pairings):
        s, d, wt, wc = compute_measures(p)
        pt = tuple(p)
        tag = ""
        if pt == kw_tuple:
            tag = " ← KW"
        if pt == comp_tuple:
            tag = " ← COMPLEMENT"

        pr(f"\n  Pairing {i+1}:{tag}")
        pr(f"    S={s}, D={d:.6f}, WT={wt:.4f}, WC={wc:+.6f}")

        # Pair-orbit decomposition
        pr(f"    Pair-orbits used: {[idx for idx in solutions[i]]}")

        # Show pair types
        type_counts = Counter()
        for a, b in p:
            if COMPLEMENT[a] == b or COMPLEMENT[b] == a:
                type_counts['comp'] += 1
            elif REVERSE[a] == b or REVERSE[b] == a:
                type_counts['rev'] += 1
            elif COMP_REV[a] == b or COMP_REV[b] == a:
                type_counts['cr'] += 1
            else:
                type_counts['other'] += 1
        pr(f"    Pair types: {dict(type_counts)}")

        # Mask distribution
        mask_counts = Counter(a ^ b for a, b in p)
        distinct_masks = len(mask_counts)
        pr(f"    Distinct masks: {distinct_masks}")
        for m, c in sorted(mask_counts.items(), key=lambda x: -x[1]):
            pr(f"      {fmt(m)} (dist={POPCOUNT[m]}): ×{c}")

    # ── Verify equivariance ──
    pr(f"\n## Verification")
    for i, p in enumerate(pairings):
        pair_set = {(min(a,b), max(a,b)) for a,b in p}
        ok = True
        for sigma in group:
            for a, b in p:
                sa, sb = sigma[a], sigma[b]
                if (min(sa,sb), max(sa,sb)) not in pair_set:
                    ok = False
                    break
            if not ok:
                break
        pr(f"  Pairing {i+1}: equivariant under all 384 elements: {ok}")

    # ── Summary ──
    pr(f"\n{'='*70}")
    pr("SUMMARY")
    pr(f"{'='*70}")

    pr(f"\n  State orbits under full stabilizer: {len(state_orbits)}")
    pr(f"  Pair-orbits (valid): {len(valid_po)}")
    pr(f"  Equivariant pairings: {len(pairings)}")

    if len(pairings) == 1:
        pr(f"\n  KW IS THE UNIQUE PAIRING INVARIANT UNDER THE MIRROR-PAIR SYMMETRY GROUP.")
        pr(f"  No lexicographic characterization needed — symmetry alone determines KW.")
    elif len(pairings) == 2:
        pr(f"\n  EXACTLY TWO pairings respect the full mirror-pair symmetry:")
        for i, p in enumerate(pairings):
            pt = tuple(p)
            s, d, wt, wc = compute_measures(p)
            tag = "KW" if pt == kw_tuple else ("COMPLEMENT" if pt == comp_tuple else "UNKNOWN")
            pr(f"    {tag}: S={s}, D={d:.6f}, WT={wt:.4f}")
        pr(f"\n  The characterization reduces to:")
        pr(f"  'Two pairings respect mirror-pair symmetry: complement (max strength)")
        pr(f"   and KW (weight-preserving). The tradition uses complement at n=3, KW at n=6.'")
    else:
        pr(f"\n  {len(pairings)} pairings respect the full mirror-pair symmetry.")
        pr(f"  The lexicographic characterization retains its role within this smaller space.")

    # ── Save ──
    md_path = out_dir / 'full_stabilizer_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
