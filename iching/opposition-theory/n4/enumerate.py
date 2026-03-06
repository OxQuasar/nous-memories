#!/usr/bin/env python3
"""
Opposition Theory — Phase 1: n=4 Exhaustive Pairing Enumeration & Measures

Enumerates all 2,027,025 pairings of 16 4-bit states into 8 unordered pairs.
Computes 5 opposition measures per pairing. Saves compressed results.

Measures:
  1. Opposition strength:  Σ popcount(a XOR b)
  2. Opposition diversity:  Shannon entropy of XOR mask distribution
  4a. Weight tilt:          mean |yang_count(a) - yang_count(b)|
  4b. Reversal symmetry:   count of pairs preserved under bit-reversal
  5. Weight complementarity: Pearson r of (yang_count(a), yang_count(b)), a < b
"""

import math
import time
import sys
from collections import Counter
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 4
NUM_STATES = 1 << N  # 16
NUM_PAIRS = NUM_STATES // 2  # 8
EXPECTED_PAIRINGS = 2_027_025  # 16! / (2^8 × 8!)

# Precompute tables
POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]
REVERSE = [0] * NUM_STATES
COMPLEMENT = [0] * NUM_STATES
for x in range(NUM_STATES):
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    REVERSE[x] = r
    COMPLEMENT[x] = x ^ ((1 << N) - 1)

HAMMING = [[0] * NUM_STATES for _ in range(NUM_STATES)]
for a in range(NUM_STATES):
    for b in range(NUM_STATES):
        HAMMING[a][b] = POPCOUNT[a ^ b]


# ─── Enumeration ──────────────────────────────────────────────────────────────

def enumerate_pairings():
    """
    Generate all pairings of {0..15} into 8 unordered pairs.
    Canonical: always pair the smallest unpaired element with each remaining.
    Returns flat numpy array: shape (N_pairings, 8, 2).
    """
    results = []

    def recurse(remaining, current):
        if not remaining:
            results.append(current[:])
            return
        first = remaining[0]
        rest = remaining[1:]
        for i in range(len(rest)):
            partner = rest[i]
            current.append((first, partner))
            new_remaining = rest[:i] + rest[i+1:]
            recurse(new_remaining, current)
            current.pop()

    recurse(list(range(NUM_STATES)), [])
    return results


# ─── Measures ─────────────────────────────────────────────────────────────────

def compute_measures(pairing):
    """Compute all measures for a single pairing (list of 8 (a,b) tuples, a < b)."""

    # 1. Opposition strength
    strength = 0
    masks = []
    yang_a = []
    yang_b = []
    reversal_preserved = 0

    for a, b in pairing:
        xor = a ^ b
        strength += POPCOUNT[xor]
        masks.append(xor)
        yang_a.append(POPCOUNT[a])
        yang_b.append(POPCOUNT[b])

    # 2. Opposition diversity (entropy of mask distribution)
    mask_counts = Counter(masks)
    entropy = 0.0
    for c in mask_counts.values():
        p = c / NUM_PAIRS
        entropy -= p * math.log2(p)
    entropy = max(0.0, entropy)  # clamp floating-point artifacts

    # 4a. Weight tilt: mean |yang_count(a) - yang_count(b)|
    abs_diffs = [abs(yang_a[i] - yang_b[i]) for i in range(NUM_PAIRS)]
    weight_tilt = sum(abs_diffs) / NUM_PAIRS

    # 4b. Reversal symmetry: pairs preserved (as sets) under reversal
    pair_set = set()
    for a, b in pairing:
        pair_set.add((min(a, b), max(a, b)))

    for a, b in pairing:
        ra, rb = REVERSE[a], REVERSE[b]
        rev_pair = (min(ra, rb), max(ra, rb))
        if rev_pair in pair_set:
            reversal_preserved += 1
    # Each preserved pair counted once (we iterate over original pairs)

    # 5. Weight complementarity: Pearson r
    wa = np.array(yang_a, dtype=np.float64)
    wb = np.array(yang_b, dtype=np.float64)
    std_a, std_b = wa.std(), wb.std()
    if std_a == 0 or std_b == 0:
        weight_corr = 0.0  # degenerate
    else:
        weight_corr = float(np.corrcoef(wa, wb)[0, 1])

    return strength, entropy, weight_tilt, reversal_preserved, weight_corr


# ─── Named pairings ──────────────────────────────────────────────────────────

def make_complement_pairing():
    """Pair each state with its bitwise complement."""
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        c = COMPLEMENT[x]
        pairs.append((min(x, c), max(x, c)))
        seen.update((x, c))
    return tuple(sorted(pairs))


def make_comprev_pairing():
    """Pair each state with complement(reverse(x)).
    Returns None if the operation has fixed points (invalid pairing)."""
    fixed = [x for x in range(NUM_STATES) if COMPLEMENT[REVERSE[x]] == x]
    if fixed:
        return None
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        cr = COMPLEMENT[REVERSE[x]]
        pairs.append((min(x, cr), max(x, cr)))
        seen.update((x, cr))
    return tuple(sorted(pairs))


def make_kw_style_pairing():
    """Reversal for non-palindromes, complement for palindromes."""
    pairs = []
    seen = set()
    palindromes = {x for x in range(NUM_STATES) if REVERSE[x] == x}
    for x in range(NUM_STATES):
        if x in seen:
            continue
        partner = COMPLEMENT[x] if x in palindromes else REVERSE[x]
        pairs.append((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    return tuple(sorted(pairs))


def format_bin(x):
    return format(x, f'0{N}b')


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent

    print("=" * 70)
    print("n=4 EXHAUSTIVE PAIRING ENUMERATION")
    print("=" * 70)

    # ── Enumerate ──
    print(f"\nEnumerating all pairings of {NUM_STATES} states into {NUM_PAIRS} pairs...")
    t0 = time.time()
    pairings = enumerate_pairings()
    t_enum = time.time() - t0
    print(f"  Found {len(pairings):,} pairings (expected {EXPECTED_PAIRINGS:,})")
    print(f"  Time: {t_enum:.2f}s")
    assert len(pairings) == EXPECTED_PAIRINGS, f"Count mismatch!"

    # ── Identify named pairings ──
    comp_pair = make_complement_pairing()
    kw_pair = make_kw_style_pairing()

    named = {
        'complement': comp_pair,
        'kw_style': kw_pair,
    }

    print("\nNamed pairings:")
    for name, p in named.items():
        print(f"  {name}:")
        for a, b in p:
            print(f"    {format_bin(a)} ↔ {format_bin(b)}  XOR={format_bin(a^b)} dist={HAMMING[a][b]}")
    print(f"\n  comp_rev: INVALID (4 fixed points under comp∘rev)")
    print(f"  reversal: INVALID (4 palindromes are fixed under reversal)")

    # ── Compute measures ──
    print(f"\nComputing measures for {len(pairings):,} pairings...")
    t0 = time.time()

    # Pre-allocate arrays
    strengths = np.empty(EXPECTED_PAIRINGS, dtype=np.int32)
    diversities = np.empty(EXPECTED_PAIRINGS, dtype=np.float64)
    weight_tilts = np.empty(EXPECTED_PAIRINGS, dtype=np.float64)
    reversal_syms = np.empty(EXPECTED_PAIRINGS, dtype=np.int32)
    weight_corrs = np.empty(EXPECTED_PAIRINGS, dtype=np.float64)

    named_indices = {name: None for name in named}

    for idx, pairing in enumerate(pairings):
        s, d, wt, rs, wc = compute_measures(pairing)
        strengths[idx] = s
        diversities[idx] = d
        weight_tilts[idx] = wt
        reversal_syms[idx] = rs
        weight_corrs[idx] = wc

        # Check if this is a named pairing
        key = tuple(sorted(pairing))
        for name, npair in named.items():
            if key == npair:
                named_indices[name] = idx

        if (idx + 1) % 500_000 == 0:
            elapsed = time.time() - t0
            rate = (idx + 1) / elapsed
            eta = (EXPECTED_PAIRINGS - idx - 1) / rate
            print(f"  {idx+1:>10,} / {EXPECTED_PAIRINGS:,} ({100*(idx+1)/EXPECTED_PAIRINGS:.1f}%)  "
                  f"{rate:.0f}/s  ETA {eta:.0f}s")

    t_comp = time.time() - t0
    print(f"  Computation time: {t_comp:.1f}s")

    # ── Summary statistics ──
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)

    measures = [
        ("Strength", strengths),
        ("Diversity", diversities),
        ("Weight Tilt", weight_tilts),
        ("Reversal Symmetry", reversal_syms),
        ("Weight Correlation", weight_corrs),
    ]

    for name, arr in measures:
        print(f"\n{name}:")
        print(f"  range: [{np.min(arr):.4f}, {np.max(arr):.4f}]")
        print(f"  mean:  {np.mean(arr):.4f}  std: {np.std(arr):.4f}")
        if arr.dtype in (np.int32, np.int64):
            vals, counts = np.unique(arr, return_counts=True)
            for v, c in zip(vals, counts):
                print(f"    {v:>3}: {c:>8,} ({100*c/len(arr):5.2f}%)")

    # ── Named pairing scores ──
    print("\n" + "=" * 70)
    print("NAMED PAIRING SCORES")
    print("=" * 70)

    for name, idx in named_indices.items():
        if idx is not None:
            print(f"\n  {name} (index {idx}):")
            print(f"    Strength:          {strengths[idx]}")
            print(f"    Diversity:         {diversities[idx]:.6f}")
            print(f"    Weight Tilt:       {weight_tilts[idx]:.4f}")
            print(f"    Reversal Symmetry: {reversal_syms[idx]}")
            print(f"    Weight Correlation:{weight_corrs[idx]:.6f}")
        else:
            print(f"\n  {name}: NOT FOUND in enumeration")

    # ── Correlations ──
    print("\n" + "=" * 70)
    print("INTER-MEASURE CORRELATIONS")
    print("=" * 70)

    mnames = ["Strength", "Diversity", "WeightTilt", "RevSym", "WeightCorr"]
    arrays = [strengths.astype(float), diversities, weight_tilts,
              reversal_syms.astype(float), weight_corrs]
    for i in range(len(mnames)):
        for j in range(i+1, len(mnames)):
            r = np.corrcoef(arrays[i], arrays[j])[0, 1]
            print(f"  {mnames[i]:>12} ↔ {mnames[j]:<12}: r = {r:+.4f}")

    # ── Strength distribution detail ──
    print("\n" + "=" * 70)
    print("STRENGTH DISTRIBUTION")
    print("=" * 70)
    vals, counts = np.unique(strengths, return_counts=True)
    for v, c in zip(vals, counts):
        bar = '█' * max(1, int(60 * c / counts.max()))
        print(f"  S={v:2d}: {c:>8,} {bar}")

    # ── Diversity at extremes ──
    max_s = np.max(strengths)
    mask = strengths == max_s
    print(f"\n  At max strength ({max_s}): "
          f"diversity in [{np.min(diversities[mask]):.4f}, {np.max(diversities[mask]):.4f}], "
          f"n={np.sum(mask):,}")
    min_s = np.min(strengths)
    mask = strengths == min_s
    print(f"  At min strength ({min_s}): "
          f"diversity in [{np.min(diversities[mask]):.4f}, {np.max(diversities[mask]):.4f}], "
          f"n={np.sum(mask):,}")

    max_d = np.max(diversities)
    mask = diversities == max_d
    print(f"\n  At max diversity ({max_d:.4f}): "
          f"strength in [{np.min(strengths[mask])}, {np.max(strengths[mask])}], "
          f"n={np.sum(mask):,}")

    # ── Save compressed results ──
    save_path = out_dir / 'measures.npz'
    np.savez_compressed(save_path,
        strengths=strengths,
        diversities=diversities,
        weight_tilts=weight_tilts,
        reversal_syms=reversal_syms,
        weight_corrs=weight_corrs,
    )
    print(f"\nResults saved to {save_path}")
    print(f"File size: {save_path.stat().st_size / 1024:.1f} KB")

    # Save named pairing indices
    import json
    meta = {
        'total_pairings': EXPECTED_PAIRINGS,
        'named_indices': {k: int(v) if v is not None else None for k, v in named_indices.items()},
        'named_pairings': {
            name: [(format_bin(a), format_bin(b)) for a, b in p]
            for name, p in named.items()
        },
        'invalid_pairings': {
            'comp_rev': 'comp∘rev has 4 fixed points (0011, 0101, 1010, 1100)',
            'reversal': 'reversal has 4 fixed points (palindromes: 0000, 0110, 1001, 1111)',
        },
    }
    meta_path = out_dir / 'meta.json'
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"Metadata saved to {meta_path}")

    print(f"\nNote: Measure 3 (Sequential variety) skipped — requires a sequence, "
          f"not just a pairing.\n  No canonical n=4 sequence exists. May revisit if "
          f"one emerges from analysis.")


if __name__ == '__main__':
    main()
