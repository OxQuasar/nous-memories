#!/usr/bin/env python3
"""
Cross-scale test at n=5: Does KW-style occupy a distinctive position?

n=5: 32 states, 16 pairs, 2 mirror pairs {L1↔L5, L2↔L4}, center L3.
- Palindromes: L1=L5 and L2=L4, L3 free → 2³ = 8 palindromes
- Odd n → no complement-fixed, no comp∘rev-fixed points
"""

import math
import time
from collections import Counter
from itertools import permutations
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 5
NUM_STATES = 1 << N   # 32
NUM_PAIRS = NUM_STATES // 2  # 16
MASK_ALL = (1 << N) - 1

POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]

def _reverse(x):
    bits = format(x, f'0{N}b')
    return int(bits[::-1], 2)

REVERSE = [_reverse(x) for x in range(NUM_STATES)]
COMPLEMENT = [x ^ MASK_ALL for x in range(NUM_STATES)]
COMP_REV = [COMPLEMENT[REVERSE[x]] for x in range(NUM_STATES)]

PALINDROMES = [x for x in range(NUM_STATES) if REVERSE[x] == x]
PALINDROME_SET = set(PALINDROMES)
CR_FIXED = [x for x in range(NUM_STATES) if COMP_REV[x] == x]
COMP_FIXED = [x for x in range(NUM_STATES) if COMPLEMENT[x] == x]

def fmt(x):
    return format(x, f'0{N}b')


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


# ─── Z₂² orbit structure ─────────────────────────────────────────────────────

def compute_z2_orbits():
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]})
        orbits.append(orbit)
        visited.update(orbit)
    return orbits


# ─── KW-style pairing ────────────────────────────────────────────────────────

def make_kw_style():
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        partner = COMPLEMENT[x] if x in PALINDROME_SET else REVERSE[x]
        pairs.append((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    return sorted(pairs)


# ─── B_N operations ──────────────────────────────────────────────────────────

def apply_bn(x, perm, flip_mask):
    result = 0
    for out_pos in range(N):
        in_pos = perm[out_pos]
        bit = (x >> in_pos) & 1
        result |= bit << out_pos
    return result ^ flip_mask


def build_stabilizer(target_pairs):
    """Find all B_N elements preserving a pairing."""
    target_set = frozenset(target_pairs)
    stabilizer = []
    for perm in permutations(range(N)):
        for flip_int in range(1 << N):
            sigma = [apply_bn(x, perm, flip_int) for x in range(NUM_STATES)]
            ok = True
            for a, b in target_set:
                sa, sb = sigma[a], sigma[b]
                if (min(sa, sb), max(sa, sb)) not in target_set:
                    ok = False
                    break
            if ok:
                stabilizer.append(sigma)
    return stabilizer


def compute_state_orbits(group):
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


def solve_exact_cover(valid_po, orbit_masks, orbit_npairs):
    """Find all equivariant perfect matchings."""
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


def random_pairing(rng):
    perm = rng.permutation(NUM_STATES)
    a = perm[0::2]
    b = perm[1::2]
    pairs = [(min(x, y), max(x, y)) for x, y in zip(a, b)]
    return pairs


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr(f"n={N} CROSS-SCALE ANALYSIS")
    pr("=" * 70)

    # ── Fixed points ──
    pr(f"\n## Fixed Points")
    pr(f"  Palindromes (rev-fixed): {len(PALINDROMES)}")
    for p in PALINDROMES:
        pr(f"    {fmt(p)}  w={POPCOUNT[p]}  comp={fmt(COMPLEMENT[p])}")
    pr(f"  Comp∘rev-fixed: {len(CR_FIXED)}")
    for x in CR_FIXED:
        pr(f"    {fmt(x)}  w={POPCOUNT[x]}")
    pr(f"  Complement-fixed: {len(COMP_FIXED)}")

    # ── Z₂² orbits ──
    pr(f"\n## Z₂² Orbit Structure")
    z2_orbits = compute_z2_orbits()
    size_dist = Counter(len(o) for o in z2_orbits)
    pr(f"  Total orbits: {len(z2_orbits)}")
    pr(f"  Size distribution: {dict(sorted(size_dist.items()))}")

    for i, orb in enumerate(z2_orbits):
        weights = [POPCOUNT[x] for x in orb]
        pr(f"    O{i:2d} (size {len(orb)}): "
           f"{', '.join(fmt(x) for x in orb)}  weights={weights}")

    n_size2 = sum(1 for o in z2_orbits if len(o) == 2)
    n_size4 = sum(1 for o in z2_orbits if len(o) == 4)
    pr(f"\n  Size-2 orbits: {n_size2}")
    pr(f"  Size-4 orbits: {n_size4}")

    # ── KW-style pairing ──
    pr(f"\n## KW-Style Pairing")
    kw_pairs = make_kw_style()
    pr(f"  Rule: reversal for non-palindromes, complement for palindromes")

    for a, b in kw_pairs:
        xor = a ^ b
        ptype = "comp" if COMPLEMENT[a] == b else "rev"
        pr(f"    {fmt(a)} ↔ {fmt(b)}  XOR={fmt(xor)} dist={POPCOUNT[xor]} "
           f"Δw={abs(POPCOUNT[a]-POPCOUNT[b])} [{ptype}]")

    kw_s, kw_d, kw_wt, kw_wc = compute_measures(kw_pairs)
    pr(f"\n  Measures:")
    pr(f"    Strength:    {kw_s}")
    pr(f"    Diversity:   {kw_d:.6f}")
    pr(f"    Weight Tilt: {kw_wt:.4f}")
    pr(f"    Weight Corr: {kw_wc:+.6f}")

    # Mask distribution
    mask_counts = Counter(a ^ b for a, b in kw_pairs)
    pr(f"    Distinct masks: {len(mask_counts)}")
    for m, c in sorted(mask_counts.items(), key=lambda x: -x[1]):
        pr(f"      {fmt(m)} (dist={POPCOUNT[m]}): ×{c}")

    # Max possible S (complement)
    comp_pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        c = COMPLEMENT[x]
        comp_pairs.append((min(x, c), max(x, c)))
        seen.update((x, c))
    comp_s = sum(POPCOUNT[a ^ b] for a, b in comp_pairs)
    pr(f"\n  Complement S = {comp_s} (maximum)")
    pr(f"  KW-style S = {kw_s} ({100*kw_s/comp_s:.1f}% of max)")
    pr(f"  S cost of weight preservation: {100*(1-kw_s/comp_s):.1f}%")

    # ── Mirror-pair partition group ──
    pr(f"\n## Mirror-Pair Partition Group (Stabilizer in B_{N})")
    pr(f"  |B_{N}| = 2^{N} × {N}! = {(1<<N) * math.factorial(N)}")
    pr(f"  Mirror pairs at n={N}: {{L1↔L5, L2↔L4}}, center L3")

    t0 = time.time()
    kw_fset = frozenset((min(a,b), max(a,b)) for a,b in kw_pairs)
    stab = build_stabilizer(kw_pairs)
    pr(f"  |Stab_B{N}(KW-style)| = {len(stab)} ({time.time()-t0:.1f}s)")

    # Expected: S₂ (permute 2 mirror pairs) × (Z₂)² (swap within pairs) × Z₂ (flip center)
    # × (Z₂)² (flip mirror pair values) × Z₂ (flip center value)
    # = 2 × 4 × 2 × 4 × 2 = 128? Let's see what we get.
    pr(f"  Expected structure: permute 2 mirror pairs (S₂) × swap within (Z₂²) × center (Z₂)")
    pr(f"                    × flip mirror pair values (Z₂²) × flip center value (Z₂)")
    pr(f"  Expected order: 2 × 4 × 2 × 4 × 2 = 128")

    # ── State orbits under stabilizer ──
    pr(f"\n## State Orbits Under Full Stabilizer")
    state_orbits = compute_state_orbits(stab)
    so_sizes = Counter(len(o) for o in state_orbits)
    pr(f"  Number of orbits: {len(state_orbits)}")
    pr(f"  Size distribution: {dict(sorted(so_sizes.items()))}")

    for i, orb in enumerate(state_orbits):
        weights = Counter(POPCOUNT[x] for x in orb)
        pr(f"    SO{i:2d} (size {len(orb):2d}): "
           f"weights={dict(sorted(weights.items()))}, "
           f"states=[{', '.join(fmt(x) for x in orb[:8])}"
           f"{'...' if len(orb) > 8 else ''}]")

    # ── Pair orbits + enumeration ──
    pr(f"\n## Equivariant Pairings Under Full Stabilizer")
    t0 = time.time()
    pair_orbits = compute_pair_orbits(stab)
    pr(f"  Total pair-orbits: {len(pair_orbits)} ({time.time()-t0:.1f}s)")

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
            valid_po.append(sorted(po))
            valid_masks.append(mask)
            valid_npairs.append(len(po))

    pr(f"  Valid pair-orbits (no internal overlap): {len(valid_po)}")
    for i, po in enumerate(valid_po):
        s_contrib = sum(POPCOUNT[a ^ b] for a, b in po)
        masks = set(a ^ b for a, b in po)
        wt_contrib = sum(abs(POPCOUNT[a] - POPCOUNT[b]) for a, b in po) / len(po)
        pr(f"    VPO{i:2d}: {len(po):2d} pairs, "
           f"S_contrib={s_contrib:3d}, WT={wt_contrib:.2f}, "
           f"masks={sorted(fmt(m) for m in masks)}")

    t0 = time.time()
    solutions = solve_exact_cover(valid_po, valid_masks, valid_npairs)
    pr(f"\n  Equivariant pairings: {len(solutions)} ({time.time()-t0:.2f}s)")

    # Analyze each
    kw_tuple = tuple(sorted(kw_pairs))
    comp_tuple = tuple(sorted(comp_pairs))

    eq_pairings = []
    for sol in solutions:
        pairs = []
        for idx in sol:
            pairs.extend(valid_po[idx])
        pairs = sorted(pairs)
        eq_pairings.append(pairs)

    for i, p in enumerate(eq_pairings):
        s, d, wt, wc = compute_measures(p)
        pt = tuple(p)
        tag = ""
        if pt == kw_tuple:
            tag = " ← KW-STYLE"
        if pt == comp_tuple:
            tag = " ← COMPLEMENT"

        type_counts = Counter()
        for a, b in p:
            if COMPLEMENT[a] == b:
                type_counts['comp'] += 1
            elif REVERSE[a] == b or REVERSE[b] == a:
                type_counts['rev'] += 1
            elif COMP_REV[a] == b or COMP_REV[b] == a:
                type_counts['cr'] += 1
            else:
                type_counts['other'] += 1

        pr(f"\n  Pairing {i+1}:{tag}")
        pr(f"    S={s}, D={d:.6f}, WT={wt:.4f}, WC={wc:+.6f}")
        pr(f"    Types: {dict(type_counts)}")
        masks = Counter(a ^ b for a, b in p)
        pr(f"    Distinct masks: {len(masks)}")

    # ── Random sample ──
    SAMPLE_SIZE = 50_000
    pr(f"\n## Random Sample ({SAMPLE_SIZE:,} pairings)")

    rng = np.random.default_rng(42)
    t0 = time.time()
    r_strengths = np.empty(SAMPLE_SIZE, dtype=np.int32)
    r_diversities = np.empty(SAMPLE_SIZE, dtype=np.float64)
    r_wt = np.empty(SAMPLE_SIZE, dtype=np.float64)
    r_wc = np.empty(SAMPLE_SIZE, dtype=np.float64)

    for i in range(SAMPLE_SIZE):
        rp = random_pairing(rng)
        s, d, wt, wc = compute_measures(rp)
        r_strengths[i] = s
        r_diversities[i] = d
        r_wt[i] = wt
        r_wc[i] = wc

    pr(f"  Sampling time: {time.time()-t0:.1f}s")

    pr(f"\n  Sample statistics:")
    for name, arr in [("Strength", r_strengths), ("Diversity", r_diversities),
                      ("Weight Tilt", r_wt), ("Weight Corr", r_wc)]:
        pr(f"    {name}: mean={arr.mean():.4f}, std={arr.std():.4f}, "
           f"range=[{arr.min():.4f}, {arr.max():.4f}]")

    pr(f"\n  KW-style percentiles:")
    for name, kv, arr in [
        ("Strength", kw_s, r_strengths),
        ("Diversity", kw_d, r_diversities),
        ("Weight Tilt", kw_wt, r_wt),
        ("Weight Corr", kw_wc, r_wc),
    ]:
        pct = 100 * np.mean(arr <= kv)
        pr(f"    {name:<15}: KW={kv:>10.4f}  percentile={pct:.2f}%")

    # Also complement percentiles
    comp_s, comp_d, comp_wt, comp_wc = compute_measures(comp_pairs)
    pr(f"\n  Complement percentiles:")
    for name, cv, arr in [
        ("Strength", comp_s, r_strengths),
        ("Diversity", comp_d, r_diversities),
        ("Weight Tilt", comp_wt, r_wt),
    ]:
        pct = 100 * np.mean(arr <= cv)
        pr(f"    {name:<15}: Comp={cv:>10.4f}  percentile={pct:.2f}%")

    # ── Cross-scale comparison table ──
    pr(f"\n## Cross-Scale Comparison")
    pr(f"  {'n':>3} {'States':>6} {'|S₂ orbs|':>9} {'|Stab|':>6} "
       f"{'#Eq pairings':>12} {'KW S%max':>8} {'KW S%ile':>8} "
       f"{'KW WT':>6}")

    # n=3 data (from previous analysis)
    pr(f"  {'3':>3} {'8':>6} {'3':>9} {'?':>6} "
       f"{'9':>12} {'83.3%':>8} {'~99%':>8} "
       f"{'1.00':>6}")

    # n=4 data
    pr(f"  {'4':>3} {'16':>6} {'6':>9} {'?':>6} "
       f"{'117':>12} {'75%':>8} {'~75%':>8} "
       f"{'?':>6}")

    # n=5 data
    kw_pct_s = 100 * np.mean(r_strengths <= kw_s)
    pr(f"  {'5':>3} {NUM_STATES:>6} {len(z2_orbits):>9} {len(stab):>6} "
       f"{len(solutions):>12} {100*kw_s/comp_s:>7.1f}% {kw_pct_s:>7.2f}% "
       f"{kw_wt:>6.2f}")

    # n=6 data
    pr(f"  {'6':>3} {'64':>6} {'20':>9} {'384':>6} "
       f"{'9':>12} {'62.5%':>8} {'99.98%':>8} "
       f"{'0.38':>6}")

    # ── Summary ──
    pr(f"\n{'='*70}")
    pr("SUMMARY")
    pr(f"{'='*70}")

    pr(f"\n  n=5 orbit structure: {n_size2} size-2 + {n_size4} size-4 orbits")
    pr(f"  Mirror-pair stabilizer: |Stab| = {len(stab)}")
    pr(f"  Equivariant pairings: {len(solutions)}")
    pr(f"  KW-style: S={kw_s}, WT={kw_wt:.4f}, S-percentile={kw_pct_s:.2f}%")

    if kw_pct_s > 99:
        pr(f"\n  n=5 looks like n=6: KW-style is extreme → transition before n=6")
    elif kw_pct_s > 90:
        pr(f"\n  n=5 is intermediate: KW-style is notable but not extreme")
    else:
        pr(f"\n  n=5 looks like n=4: KW-style is mediocre → n=6 is a sharp threshold")

    # ── Save ──
    md_path = out_dir / 'cross_scale_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
