"""
Thread 1: Bridge Mask Generator Basis

Questions:
- What is the rank of the 31 bridge masks over GF(2)?
- What is a minimal basis?
- Do the 23 unique masks form a subgroup, coset, or linear code?
- How does the bridge mask subspace relate to the standard generator subspace {O, M, I}?
"""

import sys
sys.path.insert(0, '/home/skipper/code/nous/kingwen')

import numpy as np
from collections import Counter
from sequence import KING_WEN, all_bits

DIMS = 6
M = np.array(all_bits())

GEN_BITS = {
    'O': (1, 0, 0, 0, 0, 1),
    'M': (0, 1, 0, 0, 1, 0),
    'I': (0, 0, 1, 1, 0, 0),
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])


# ─── Build bridge masks ────────────────────────────────────────────────────
bridge_masks = []
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    bridge_masks.append(xor)

unique_masks = sorted(set(bridge_masks))
all_masks = bridge_masks  # all 31, with repeats

print("=" * 70)
print("THREAD 1: BRIDGE MASK SUBSPACE ANALYSIS")
print("=" * 70)

# ─── 1. Rank of bridge mask matrix over GF(2) ─────────────────────────────
print("\n1. RANK OF BRIDGE MASK MATRIX OVER GF(2)")
print("-" * 50)

def gf2_rank(matrix):
    """Compute rank of binary matrix over GF(2) via row reduction."""
    mat = np.array(matrix, dtype=int) % 2
    rows, cols = mat.shape
    rank = 0
    pivot_cols = []
    for col in range(cols):
        # Find pivot row
        pivot_row = None
        for row in range(rank, rows):
            if mat[row, col] == 1:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        # Swap
        mat[[rank, pivot_row]] = mat[[pivot_row, rank]]
        pivot_cols.append(col)
        # Eliminate
        for row in range(rows):
            if row != rank and mat[row, col] == 1:
                mat[row] = (mat[row] + mat[rank]) % 2
        rank += 1
    return rank, mat[:rank], pivot_cols

def gf2_rref(matrix):
    """Full row reduction over GF(2), return reduced matrix and rank."""
    mat = np.array(matrix, dtype=int) % 2
    rows, cols = mat.shape
    rank = 0
    for col in range(cols):
        pivot_row = None
        for row in range(rank, rows):
            if mat[row, col] == 1:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        mat[[rank, pivot_row]] = mat[[pivot_row, rank]]
        for row in range(rows):
            if row != rank and mat[row, col] == 1:
                mat[row] = (mat[row] + mat[rank]) % 2
        rank += 1
    return mat[:rank], rank

# All 31 bridge masks (with repeats)
mat_all = np.array(all_masks, dtype=int)
rank_all, rref_all, pivots_all = gf2_rank(mat_all)
print(f"  All 31 bridge masks: rank = {rank_all} over GF(2)")

# 23 unique masks
mat_unique = np.array(unique_masks, dtype=int)
rank_unique, rref_unique, pivots_unique = gf2_rank(mat_unique)
print(f"  23 unique bridge masks: rank = {rank_unique} over GF(2)")

print(f"\n  Maximum possible rank in Z₂⁶: 6")
print(f"  Bridge mask space dimension: {rank_all}")
if rank_all == 6:
    print(f"  → Bridge masks SPAN the full 6-dimensional space!")
    print(f"  → Any element of Z₂⁶ can be reached by XOR-combining bridge masks")
else:
    print(f"  → Bridge masks span a {rank_all}-dimensional subspace")
    print(f"  → There are {6 - rank_all} 'blind' dimensions")

# ─── 2. Minimal basis ──────────────────────────────────────────────────────
print(f"\n2. MINIMAL BASIS (from RREF)")
print("-" * 50)

rref_result, final_rank = gf2_rref(mat_unique)
print(f"  Basis vectors (RREF of unique masks):")
for i in range(final_rank):
    vec = tuple(rref_result[i])
    print(f"    e{i+1}: {''.join(map(str, vec))}")

# Check if standard generators are in the span
print(f"\n  Standard generators vs bridge span:")
for name, gen in GEN_BITS.items():
    # Check if gen is in span: try to reduce [basis; gen]
    augmented = np.vstack([rref_result, [gen]])
    aug_rref, aug_rank = gf2_rref(augmented)
    in_span = (aug_rank == final_rank)
    print(f"    {name} = {''.join(map(str, gen))}:  {'IN span' if in_span else 'NOT in span'}")

# ─── 3. Subgroup / closure test ────────────────────────────────────────────
print(f"\n3. CLOSURE PROPERTIES OF UNIQUE BRIDGE MASKS")
print("-" * 50)

unique_set = set(unique_masks)
# Check closure under XOR (subgroup test for Z₂⁶)
closure_violations = 0
closure_products = set()
for i, a in enumerate(unique_masks):
    for j, b in enumerate(unique_masks):
        if i < j:
            product = tuple((a[d] ^ b[d]) for d in range(DIMS))
            closure_products.add(product)
            if product not in unique_set:
                closure_violations += 1

zero = (0,0,0,0,0,0)
has_identity = zero in unique_set
print(f"  Contains identity (000000): {has_identity}")
print(f"  Number of pairwise XORs: {len(closure_products)}")
print(f"  Pairwise XORs NOT in set: {closure_violations}")
print(f"  → {'CLOSED under XOR (subgroup)' if closure_violations == 0 and has_identity else 'NOT a subgroup'}")

# Generate full closure
generated = set(unique_masks)
changed = True
while changed:
    changed = False
    new = set()
    for a in list(generated):
        for b in list(generated):
            product = tuple((a[d] ^ b[d]) for d in range(DIMS))
            if product not in generated:
                new.add(product)
                changed = True
    generated |= new

print(f"\n  Full closure (generated subgroup): {len(generated)} elements")
print(f"  Expected from rank {final_rank}: {2**final_rank} elements")

# What's in the closure that's not in the original set?
extra = generated - unique_set
if extra:
    print(f"  Elements in closure but not original masks ({len(extra)}):")
    for e in sorted(extra):
        print(f"    {''.join(map(str, e))}")

# ─── 4. Compare to standard generator subspace ─────────────────────────────
print(f"\n4. BRIDGE SPACE vs GENERATOR SPACE")
print("-" * 50)

# Generate full standard subgroup (Z₂³ embedded in Z₂⁶)
std_gens = list(GEN_BITS.values())
std_group = set()
std_group.add((0,0,0,0,0,0))
for g in std_gens:
    new_group = set()
    for elem in std_group:
        product = tuple((elem[d] ^ g[d]) for d in range(DIMS))
        new_group.add(product)
    std_group |= new_group

print(f"  Standard generator group size: {len(std_group)} (Z₂³)")
print(f"  Standard group elements:")
for e in sorted(std_group):
    print(f"    {''.join(map(str, e))}")

print(f"\n  Bridge masks IN standard group: {len(unique_set & std_group)}")
print(f"  Bridge masks NOT in standard group: {len(unique_set - std_group)}")

# Intersection
intersection = unique_set & std_group
if intersection:
    print(f"  Intersection: {sorted(intersection)}")

# Coset analysis: are the non-standard masks in a single coset?
non_std = unique_set - std_group
if non_std:
    # Pick any non-standard mask, XOR all non-std with it → check if result is in std_group
    ref = sorted(non_std)[0]
    coset_check = set()
    for ns in non_std:
        shifted = tuple((ns[d] ^ ref[d]) for d in range(DIMS))
        coset_check.add(shifted)
    in_std = coset_check & std_group
    print(f"\n  Coset analysis (shift non-std by {ref}):")
    print(f"    Shifted elements in std group: {len(in_std)}/{len(non_std)}")
    if len(in_std) == len(non_std):
        print(f"    → Non-standard masks form a SINGLE COSET of the standard group")
    else:
        print(f"    → Non-standard masks are NOT a single coset")
        # How many cosets do they span?
        remaining = set(non_std)
        cosets = []
        while remaining:
            ref = sorted(remaining)[0]
            coset = set()
            for elem in std_group:
                shifted = tuple((ref[d] ^ elem[d]) for d in range(DIMS))
                coset.add(shifted)
            cosets.append((ref, coset & remaining))
            remaining -= coset
        print(f"    → Spans {len(cosets)} cosets of the standard group")
        for ref, members in cosets:
            print(f"      Coset via {''.join(map(str, ref))}: "
                  f"{', '.join(''.join(map(str, m)) for m in sorted(members))}")

# ─── 5. Which elements of Z₂⁶ are NOT bridge masks? ────────────────────────
print(f"\n5. MISSING ELEMENTS")
print("-" * 50)

all_z2_6 = set()
for i in range(64):
    elem = tuple((i >> d) & 1 for d in range(DIMS))
    all_z2_6.add(elem)

# Actually build them properly (bit 0 = position 0)
all_z2_6 = set()
for i in range(64):
    elem = tuple((i >> (5-d)) & 1 for d in range(DIMS))
    all_z2_6.add(elem)

missing_from_unique = all_z2_6 - unique_set
print(f"  Total elements in Z₂⁶: {len(all_z2_6)}")
print(f"  Unique bridge masks: {len(unique_set)}")
print(f"  Missing from bridge masks: {len(missing_from_unique)}")

# Group missing by Hamming weight
from collections import defaultdict
missing_by_weight = defaultdict(list)
for m in sorted(missing_from_unique):
    w = sum(m)
    missing_by_weight[w].append(m)

print(f"\n  Missing elements by Hamming weight:")
for w in sorted(missing_by_weight):
    elems = missing_by_weight[w]
    print(f"    Weight {w}: {len(elems)} elements")
    for e in elems:
        # Check if in standard group
        in_std = "  (std)" if e in std_group else ""
        print(f"      {''.join(map(str, e))}{in_std}")

# ─── 6. Bridge mask weight distribution ────────────────────────────────────
print(f"\n6. BRIDGE MASK WEIGHT DISTRIBUTION")
print("-" * 50)

weight_dist = Counter(sum(m) for m in unique_masks)
print(f"  Unique mask weights: {dict(sorted(weight_dist.items()))}")
weight_dist_all = Counter(sum(m) for m in all_masks)
print(f"  All 31 mask weights:  {dict(sorted(weight_dist_all.items()))}")

# Weight distribution of all Z₂⁶
z2_weight = Counter(sum(e) for e in all_z2_6)
print(f"  Z₂⁶ weight distribution: {dict(sorted(z2_weight.items()))}")

# Compare: bridge masks are biased toward which weights?
print(f"\n  Coverage by weight:")
all_by_weight = defaultdict(set)
for e in all_z2_6:
    all_by_weight[sum(e)].add(e)
bridge_by_weight = defaultdict(set)
for m in unique_masks:
    bridge_by_weight[sum(m)].add(m)

for w in range(7):
    total = len(all_by_weight[w])
    used = len(bridge_by_weight.get(w, set()))
    print(f"    Weight {w}: {used}/{total} ({100*used/total:.0f}%)")

print(f"\n{'=' * 70}")
print("THREAD 1 COMPLETE")
print("=" * 70)
