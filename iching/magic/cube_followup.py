#!/usr/bin/env python3
"""
Follow-up analyses on the most striking findings from probe 1a.
"""

import numpy as np
import random

# ── Setup (same as main script) ──
N_POL, N_LINE, N_ELEM = 2, 3, 5
H, P, Q = 0, 1, 2
WOOD, FIRE, EARTH, METAL, WATER = 0, 1, 2, 3, 4
LINE_NAMES = {H: 'H', P: 'P', Q: 'Q'}
ELEM_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}

MARKED = [
    (0, H, WOOD), (1, H, WOOD),
    (0, Q, WATER), (1, Q, FIRE),
    (0, P, METAL), (1, P, EARTH),
]

def cell_index(p, l, e):
    return p * (N_LINE * N_ELEM) + l * N_ELEM + e

print("=" * 60)
print("FOLLOW-UP 1: Z₅ negation — is it exact?")
print("=" * 60)
print()
print("The complement pairs satisfy f(comp) = -f(orig) mod 5 EXACTLY:")
print("  H: 0 ↔ 0  (negation: -0 ≡ 0 mod 5) ✓")
print("  P: 3 ↔ 2  (negation: -3 ≡ 2 mod 5) ✓")
print("  Q: 4 ↔ 1  (negation: -4 ≡ 1 mod 5) ✓")
print()
print("This is the complement equivariance f(x⊕111) = -f(x) mod 5.")
print("It's a defining property of the algebraic Z₅ assignment.")
print()

print("=" * 60)
print("FOLLOW-UP 2: Algebraic total = 15 (with frame)")
print("=" * 60)
print()
print("Under Algebraic Z₅:")
print("  6 marked cells: 0+0+4+1+3+2 = 10")
print("  Frame pair: Earth(2) + Metal(3) = 5")
print("  Total (all 8 trigrams): 10 + 5 = 15 = magic constant of 3×3 Lo Shu")
print()

# Verify: sum of 0,1,2,3,4 = 10, plus Wood double-counted → 10+0 = 10 for marked
# Actually all 8 trigrams: each element appears with multiplicity
# 坤→Earth(2), 震→Wood(0), 坎→Water(4), 兌→Metal(3), 
# 艮→Earth(2), 離→Fire(1), 巽→Wood(0), 乾→Metal(3)
all_8 = [2, 0, 4, 3, 2, 1, 0, 3]
print(f"All 8 trigram element values: {all_8}")
print(f"Sum = {sum(all_8)}")
print(f"= 2×Wood(0) + 1×Fire(1) + 2×Earth(2) + 2×Metal(3) + 1×Water(4)")
print(f"= 0 + 1 + 4 + 6 + 4 = 15")
print()
print("Cross-check: Under He Tu mod 5:")
hetu = {0: 3, 1: 2, 2: 0, 3: 4, 4: 1}
all_8_hetu = [hetu[e] for e in all_8]
print(f"  All 8 values: {all_8_hetu}, sum = {sum(all_8_hetu)}")
print()
print("Under Lo Shu (odds):")
loshu = {0: 3, 1: 9, 2: 5, 3: 7, 4: 1}
all_8_loshu = [loshu[e] for e in all_8]
print(f"  All 8 values: {all_8_loshu}, sum = {sum(all_8_loshu)}")
print()

print("=" * 60)
print("FOLLOW-UP 3: Sum mod 5 analysis of complement pairs")
print("=" * 60)
print()
print("Each Fano line's complement pair sums to 0 mod 5:")
print("  H: (0+0) mod 5 = 0")
print("  P: (3+2) mod 5 = 0")
print("  Q: (4+1) mod 5 = 0")
print()
print("This is forced by complement equivariance: f(x) + f(x⊕111) = f(x) + (-f(x)) = 0 mod 5")
print()

print("The three complement pair sums (in Z₅):")
print("  H: 0+0 = 0")
print("  P: 3+2 = 5")  
print("  Q: 4+1 = 5")
print("Absolute sums: 0, 5, 5")
print()

print("=" * 60)
print("FOLLOW-UP 4: Permutation matrix structure")
print("=" * 60)
print()
print("Each polarity slice is a permutation matrix (3 lines → 3 distinct elements):")
print()
print("Positive: H→Wood(0), P→Metal(3), Q→Water(4)")
print("  These are {0, 3, 4} = the non-identity non-unit elements minus {1, 2}")
print("  In Z₅: {0, 3, 4} = {0, -2, -1}")
print()
print("Negative: H→Wood(0), P→Earth(2), Q→Fire(1)")
print("  These are {0, 1, 2}")
print("  In Z₅: {0, 1, 2}")
print()
print("The negative slice uses {0, 1, 2} and the positive uses {0, -1, -2} = {0, 3, 4}.")
print("This is EXACTLY Z₅ negation acting on the positive slice!")
print("  neg(0) = 0, neg(3) = 2, neg(4) = 1")
print("  Positive: H→0, P→3, Q→4")
print("  Negative: H→0, P→2, Q→1 ← negation of positive!")
print()

print("=" * 60)
print("FOLLOW-UP 5: The polarity slices as Z₅ permutations")
print("=" * 60)
print()
print("Viewing each polarity slice as a function Line → Z₅:")
print()
print("σ₊: H↦0, P↦3, Q↦4")
print("σ₋: H↦0, P↦2, Q↦1  (= -σ₊ mod 5)")
print()
print("Is σ₊ an affine map? If lines are numbered H=0, P=1, Q=2:")
print("  σ₊(0)=0, σ₊(1)=3, σ₊(2)=4")
print("  Differences: σ₊(1)-σ₊(0) = 3, σ₊(2)-σ₊(1) = 1")
print("  Not linear (would need constant stride). Not affine on Z₃→Z₅.")
print()
print("But in Z₅ arithmetic: {0, 3, 4} are {0, -2, -1}.")
print("If we map H↦0, P↦-2, Q↦-1:")
print("  This is NOT arithmetic progression in any obvious way.")
print()

# Check if it becomes affine under different line orderings
from itertools import permutations as perms
print("Check all line orderings for affine structure σ(l) = al + b mod 5:")
for perm in perms([0, 1, 2]):
    line_vals = [0, 3, 4]  # σ₊ values
    mapped = [(perm[i], line_vals[i]) for i in range(3)]
    mapped.sort()
    x = [m[0] for m in mapped]
    y = [m[1] for m in mapped]
    # Check: y = ax + b mod 5?
    for a in range(5):
        for b in range(5):
            if all((a * x[i] + b) % 5 == y[i] for i in range(3)):
                perm_names = [LINE_NAMES[i] for i in [H, P, Q]]
                reord = [perm_names[perm[i]] for i in range(3)]
                print(f"  Line order ({','.join(str(p) for p in perm)}): "
                      f"σ₊ = {a}l + {b} mod 5")
print()

print("=" * 60)
print("FOLLOW-UP 6: Exact count of line-magic permutations")
print("=" * 60)
print()
print("From the null distribution: P(line variance = 0) ≈ 0.03%")
print("That's about 1 in 3300 random permutations.")
print()
# More precise count
random.seed(123)
N = 1_000_000
count_line_magic = 0
count_elem_magic = 0
count_both = 0
for _ in range(N):
    perm = list(range(1, 31))
    random.shuffle(perm)
    e_sums = [0] * 5
    l_sums = [0] * 3
    for p in range(2):
        for l in range(3):
            for e in range(5):
                v = perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    if all(s == 155 for s in l_sums):
        count_line_magic += 1
    if all(s == 93 for s in e_sums):
        count_elem_magic += 1
    if all(s == 155 for s in l_sums) and all(s == 93 for s in e_sums):
        count_both += 1

print(f"In {N:,} random permutations:")
print(f"  Line-magic (all 155): {count_line_magic} ({count_line_magic/N*100:.4f}%)")
print(f"  Element-magic (all 93): {count_elem_magic} ({count_elem_magic/N*100:.4f}%)")
print(f"  Both: {count_both} ({count_both/N*100:.6f}%)")
print()

print("=" * 60)
print("FOLLOW-UP 7: Element-magic existence proof by construction")
print("=" * 60)
print()
print("Each element slice has 6 cells (2 polarities × 3 lines).")
print("We need 5 groups of 6 cells (by element), each summing to 93.")
print("This is a partition of {1,...,30} into 5 groups of 6 with equal sums.")
print()
# Constructive: just assign numbers such that each group of 6 sums to 93
# Pair 1+30, 2+29, ..., 15+16 (each pair sums to 31)
# We need 5 groups of 6. Each group can have 3 pairs: 3×31 = 93. ✓
print("Construction: pair numbers as (k, 31-k) for k=1..15. Each pair sums to 31.")
print("Assign 3 pairs to each element slice: 3 × 31 = 93. ✓")
print()
print("Example element-magic assignment:")
pairs = [(k, 31-k) for k in range(1, 16)]
for e in range(5):
    group_pairs = pairs[e*3:(e+1)*3]
    group = [x for pair in group_pairs for x in pair]
    print(f"  {ELEM_NAMES[e]}: {group} → sum = {sum(group)}")
print()
print("This proves element-magic numberings exist trivially.")
print("The constraint is mild: any partition into equal-sized groups with equal sums works.")

print()
print("=" * 60)
print("FOLLOW-UP 8: Doubly-magic feasibility")
print("=" * 60)
print()
print("For doubly-magic, we need element slices = 93 AND line slices = 155.")
print("Element slices: 5 groups of 6 cells, each summing to 93.")
print("Line slices: 3 groups of 10 cells, each summing to 155.")
print()
print("These are not independent: each cell belongs to exactly one element slice")
print("and one line slice. The intersection of element e and line l is a 2-cell")
print("(polarity 0 and 1) pair.")
print()
print("Let S(l,e) = sum of the 2 cells in (line l, element e).")
print("Then: Σ_l S(l,e) = 93 for each e (element constraint)")
print("      Σ_e S(l,e) = 155 for each l (line constraint)")
print()
print("This is a 3×5 matrix with row sums = 155 and column sums = 93.")
print("Total = 465. Row sum = 155 (×3 = 465). Column sum = 93 (×5 = 465). ✓")
print()
print("The existence of such a matrix is trivially satisfied (e.g., S(l,e) = 31 for all).")
print("The further constraint is that the 30 values are a permutation of 1..30.")
print()

# Do a more intensive search for doubly-magic
print("Intensive doubly-magic search (2M steps)...")
random.seed(999)
best = float('inf')
best_perm = None
perm = list(range(1, 31))
random.shuffle(perm)
restarts = 0
for trial in range(2_000_000):
    if trial % 200_000 == 0 and trial > 0:
        if best > 0:
            restarts += 1
            perm = list(range(1, 31))
            random.shuffle(perm)
    
    i, j = random.sample(range(30), 2)
    perm[i], perm[j] = perm[j], perm[i]
    
    e_sums = [0] * 5
    l_sums = [0] * 3
    for p in range(2):
        for l in range(3):
            for e in range(5):
                v = perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    
    cost = sum((s - 93)**2 for s in e_sums) + sum((s - 155)**2 for s in l_sums)
    if cost < best:
        best = cost
        best_perm = perm.copy()
        if cost == 0:
            break
    else:
        perm[i], perm[j] = perm[j], perm[i]

if best == 0:
    print(f"FOUND doubly-magic numbering after restarts={restarts}!")
    e_sums = [0]*5; l_sums = [0]*3
    for p in range(2):
        for l in range(3):
            for e in range(5):
                v = best_perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    print(f"  Element sums: {e_sums}")
    print(f"  Line sums: {l_sums}")
    # Show the assignment
    print("\n  Full assignment:")
    print(f"  {'':8s}", end='')
    for e in range(5):
        print(f"  {ELEM_NAMES[e]:>6s}", end='')
    print()
    for p in range(2):
        for l in range(3):
            label = f"{'pos' if p==0 else 'neg'} {LINE_NAMES[l]}"
            print(f"  {label:8s}", end='')
            for e in range(5):
                print(f"  {best_perm[cell_index(p, l, e)]:6d}", end='')
            print()
else:
    print(f"Best cost after 2M steps: {best}")
    e_sums = [0]*5; l_sums = [0]*3
    for p in range(2):
        for l in range(3):
            for e in range(5):
                v = best_perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    print(f"  Element sums: {e_sums}")
    print(f"  Line sums: {l_sums}")
