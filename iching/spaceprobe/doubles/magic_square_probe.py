"""
Does the magic square enter necessarily?

Three probes:
1. How many ways to assign Lo Shu number pairs to S₄ blocks?
2. Is the polarity obtainable without number theory?
3. Is the magic square forced by geometric constraints?

Key setup:
- 3×3 magic square on {1,...,9}, center=5, magic constant=15
- Perimeter numbers: {1,2,3,4,6,7,8,9} assigned to 8 positions
- Diametrically opposite positions sum to 10
- These 4 pairs map to the 4 S₄ blocks
"""

from itertools import permutations, combinations
from collections import Counter, defaultdict

# ══════════════════════════════════════════════════════════════════════════════
# THE 3×3 MAGIC SQUARE
# ══════════════════════════════════════════════════════════════════════════════

# The essentially unique 3×3 magic square:
#   2 7 6
#   9 5 1
#   4 3 8
# 
# All 8 versions (rotations + reflections):
# Original:     2 7 6 / 9 5 1 / 4 3 8
# Rot 90:       4 9 2 / 3 5 7 / 8 1 6
# Rot 180:      8 3 4 / 1 5 9 / 6 7 2
# Rot 270:      6 1 8 / 7 5 3 / 2 9 4
# Reflect H:    6 7 2 / 1 5 9 / 8 3 4
# Reflect V:    4 3 8 / 9 5 1 / 2 7 6
# Reflect D1:   2 9 4 / 7 5 3 / 6 1 8
# Reflect D2:   8 1 6 / 3 5 7 / 4 9 2

# The perimeter positions (clockwise from top-left):
# TL, T, TR, R, BR, B, BL, L
# For the base square: 2, 7, 6, 1, 8, 3, 4, 9

# The diametrically opposite pairs on the perimeter:
# TL↔BR, T↔B, TR↔BL, R↔L
# For base: (2,8), (7,3), (6,4), (1,9) — all sum to 10. ✓

print("=" * 70)
print("THE 3×3 MAGIC SQUARE AND ITS CONSTRAINTS")
print("=" * 70)

# How constrained is the 3×3 magic square?
# Find ALL 3×3 magic squares on {1,...,9} with center 5.

def check_magic(grid):
    """Check if a 3×3 grid is a magic square with constant 15."""
    for r in range(3):
        if sum(grid[r]) != 15:
            return False
    for c in range(3):
        if sum(grid[r][c] for r in range(3)) != 15:
            return False
    if grid[0][0] + grid[1][1] + grid[2][2] != 15:
        return False
    if grid[0][2] + grid[1][1] + grid[2][0] != 15:
        return False
    return True

magic_squares = []
nums = [1, 2, 3, 4, 6, 7, 8, 9]  # perimeter numbers (center=5 forced)
for perm in permutations(nums):
    grid = [
        [perm[0], perm[1], perm[2]],
        [perm[3], 5, perm[4]],
        [perm[5], perm[6], perm[7]]
    ]
    if check_magic(grid):
        magic_squares.append(grid)

print(f"\n  Total 3×3 magic squares with center=5: {len(magic_squares)}")
print(f"  (Should be 8 = rotations × reflections of the unique square)")

# Show them
for i, g in enumerate(magic_squares):
    print(f"\n  Square {i+1}:")
    for row in g:
        print(f"    {row}")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 1: How many ways to assign number pairs to blocks?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"PROBE 1: NUMBER PAIR → BLOCK ASSIGNMENTS")
print(f"{'=' * 70}")

# The 4 sum-to-10 pairs: {1,9}, {2,8}, {3,7}, {4,6}
# The 4 S₄ blocks (abstract, labeled by their involution properties):
# Block structure is determined by the three involutions.
# The question: how many assignments of number pairs to blocks
# produce a valid Lo Shu (magic square on the octagon)?

# First: the number pairs are forced by sum-to-10.
pairs = [(1,9), (2,8), (3,7), (4,6)]
print(f"\n  Sum-to-10 pairs: {pairs}")

# The magic square places these 8 numbers on 8 positions of the octagon.
# The octagon has 4 diametrically opposite position pairs.
# Each position pair gets a number pair.
# 
# Given the 8 magic squares, extract the octagonal arrangements:

octagon_arrangements = []
for g in magic_squares:
    # Perimeter clockwise: TL, T, TR, R, BR, B, BL, L
    oct = [g[0][0], g[0][1], g[0][2], g[1][2], g[2][2], g[2][1], g[2][0], g[1][0]]
    # Diametric pairs: (pos 0, pos 4), (pos 1, pos 5), (pos 2, pos 6), (pos 3, pos 7)
    diametric = [tuple(sorted([oct[i], oct[i+4]])) for i in range(4)]
    octagon_arrangements.append({
        'octagon': oct,
        'diametric_pairs': diametric,
        'pair_set': frozenset(tuple(sorted(d)) for d in diametric)
    })

# All arrangements should have the same pair set (since sum-to-10 is forced)
pair_sets = set(a['pair_set'] for a in octagon_arrangements)
print(f"\n  Distinct diametric pair sets across 8 squares: {len(pair_sets)}")
for ps in pair_sets:
    print(f"    {sorted(ps)}")

# How many distinct orderings of pairs around the octagon?
distinct_orderings = set()
for a in octagon_arrangements:
    # Normalize: the 4 diametric pairs in octagonal order
    ordering = tuple(a['diametric_pairs'])
    distinct_orderings.add(ordering)

print(f"\n  Distinct pair orderings around octagon: {len(distinct_orderings)}")
for o in sorted(distinct_orderings):
    print(f"    {o}")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 2: What does the octagonal ordering constrain?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"PROBE 2: OCTAGONAL ADJACENCY CONSTRAINTS")
print(f"{'=' * 70}")

# In the magic square, the octagon has adjacency structure:
# Corners (TL,TR,BL,BR) are connected diagonally through center.
# Edges (T,R,B,L) are connected through rows/columns.
# 
# The magic square constraint (rows/cols/diags = 15) means:
# Each pair of adjacent positions on the octagon, together with the
# center (5) or the third position in the same line, sums to 15.
#
# But the key constraint for BLOCK ASSIGNMENT is:
# which pairs are ADJACENT on the octagon?
# This determines which blocks are "neighbors" in the geometric sense.

print(f"\n  Octagonal adjacency (for base square 2 7 6 / 9 5 1 / 4 3 8):")
base_oct = [2, 7, 6, 1, 8, 3, 4, 9]
for i in range(8):
    j = (i + 1) % 8
    print(f"    {base_oct[i]} — {base_oct[j]}  "
          f"(pairs: {tuple(sorted([base_oct[i], base_oct[(i+4)%8]]))}"
          f" adj {tuple(sorted([base_oct[j], base_oct[(j+4)%8]]))})")

# Which diametric pairs are adjacent?
base_pairs = [(2,8), (3,7), (4,6), (1,9)]  # in octagonal order for base
# Wait, let me recompute:
# Position 0(TL)=2, Position 4(BR)=8 → pair (2,8)
# Position 1(T)=7,  Position 5(B)=3  → pair (3,7)
# Position 2(TR)=6, Position 6(BL)=4 → pair (4,6)
# Position 3(R)=1,  Position 7(L)=9  → pair (1,9)
# Adjacent pairs on octagon: (2,8)-(3,7)-(4,6)-(1,9)-(2,8)-...
# So it's a cycle of 4 pairs.

print(f"\n  Diametric pair cycle (adjacency on octagon):")
pair_order = [(2,8), (3,7), (4,6), (1,9)]
for i in range(4):
    j = (i+1) % 4
    print(f"    {pair_order[i]} — {pair_order[j]}")

# The 4 pairs form a 4-cycle. How many distinct 4-cycles exist?
# With 4 elements, there are 3 distinct cycle orderings:
#   (A-B-C-D), (A-B-D-C), (A-C-B-D)
# Each has 8 equivalent forms (4 rotations × 2 directions).
# So 4!/8 = 3 distinct circular orderings.

# Across all 8 magic squares, how many distinct circular orderings?
def normalize_cycle(cycle):
    """Normalize a circular ordering to canonical form."""
    # Try all rotations and both directions, pick lexicographic minimum
    n = len(cycle)
    candidates = []
    for start in range(n):
        # Forward
        candidates.append(tuple(cycle[(start + i) % n] for i in range(n)))
        # Backward
        candidates.append(tuple(cycle[(start - i) % n] for i in range(n)))
    return min(candidates)

cycles = set()
for a in octagon_arrangements:
    dp = a['diametric_pairs']
    cycle = normalize_cycle(dp)
    cycles.add(cycle)

print(f"\n  Distinct pair cycles across 8 magic squares: {len(cycles)}")
for c in sorted(cycles):
    print(f"    {c}")
    # Parity pattern
    parities = ['odd' if (p[0] % 2 == 1) else 'even' for p in c]
    print(f"    Parity: {parities}")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 3: Is the parity pattern forced by the cycle?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"PROBE 3: PARITY PATTERN IN THE CYCLE")
print(f"{'=' * 70}")

# The pairs: (1,9)=odd, (2,8)=even, (3,7)=odd, (4,6)=even
# The magic square forces a specific cycle order.
# What's the parity pattern of the cycle?

for c in sorted(cycles):
    parities = tuple('O' if (p[0] % 2 == 1) else 'E' for p in c)
    print(f"  Cycle {c}: parity = {parities}")
    # Is it alternating?
    alternating = all(parities[i] != parities[(i+1)%4] for i in range(4))
    print(f"  Alternating: {alternating}")

# If the parity alternates (O-E-O-E), then adjacent blocks always
# have opposite parity. This means the 2+2 parity split is also
# a GEOMETRIC property: P₊ = non-adjacent pair of positions,
# P₋ = the other non-adjacent pair.

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 4: Could we get polarity without the magic square?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"PROBE 4: POLARITY WITHOUT THE MAGIC SQUARE")
print(f"{'=' * 70}")

# The involution structure alone gives Aut = Z₂.
# The Z₂ automorphism swaps 2 of the 4 blocks.
# It creates 3 possible 2+2 splits, of which one is aut-invariant.
# The polarity is one of the other two (the swapped pair).
#
# Could we get the polarity from the INVOLUTION STRUCTURE + Z₂³ alone?
# We showed ι₂ is not affine on Z₂³. So Z₂³ sees the difference.

# The non-trivial automorphism maps:
# Block 0↔0 (with Kan↔Li swap), Block 1↔2, Block 3↔3 (with Xun↔Qian swap)
# So it fixes {blocks 0,3} as a set and swaps {block 1, block 2}.
# The aut-invariant split is {0,3} vs {1,2}.
# The swapped pair is {0,1} vs {2,3} ↔ {0,2} vs {1,3}.
# Traditional polarity is {0,2} vs {1,3}.

# Now: in Z₂³ terms:
# Block 0 = {010, 101} (Kan, Li) — complement pair, distance 3
# Block 1 = {000, 001} (Kun, Gen) — adjacent, distance 1
# Block 2 = {100, 110} (Zhen, Dui) — adjacent, distance 1
# Block 3 = {011, 111} (Xun, Qian) — adjacent, distance 1

# Block 0 is SPECIAL in Z₂³: it's the only complement pair (distance 3).
# Blocks 1,2,3 are all distance-1 pairs.

print(f"  Block Hamming distances in Z₂³:")
BLOCKS = [(2, 5), (0, 1), (4, 6), (3, 7)]
for i, (a, b) in enumerate(BLOCKS):
    d = bin(a ^ b).count('1')
    print(f"    Block {i} {{{a:03b},{b:03b}}}: distance {d}")

# Block 0 is distinguished. The aut fixes it. Can we use this?
# The aut also fixes block 3. So {0,3} are the "fixed" blocks.
# Are 0 and 3 also distinguished in Z₂³?

print(f"\n  Z₂³ properties of each block:")
for i, (a, b) in enumerate(BLOCKS):
    xor = a ^ b
    center = (a + b) // 2 if a ^ b == (1 << (a^b).bit_length() - 1) else None
    # Popcount sum
    pc_sum = bin(a).count('1') + bin(b).count('1')
    # Is either member the identity (000)?
    has_id = (a == 0 or b == 0)
    # Is either member the all-ones (111)?
    has_all = (a == 7 or b == 7)
    print(f"    Block {i} {{{a:03b},{b:03b}}}: XOR={xor:03b}, "
          f"yang_sum={pc_sum}, has_id={has_id}, has_all={has_all}")

# Block 0: XOR=111 (complement), yang_sum=3
# Block 1: XOR=001, yang_sum=1, has_id=True (000=Kun)
# Block 2: XOR=010, yang_sum=3
# Block 3: XOR=100, yang_sum=5, has_all=True (111=Qian)

# So blocks 1 and 3 contain the extremes (Kun=000, Qian=111).
# Block 0 is the complement pair.
# Block 2 is the "ordinary" block.

# Can Z₂³ distinguish the traditional polarity {0,2} vs {1,3}?
# {0,2}: the complement pair + the ordinary pair
# {1,3}: the identity-containing + the all-ones-containing

print(f"\n  Traditional polarity in Z₂³ terms:")
print(f"    P₊ = blocks {{0,2}} = complement pair + ordinary pair")
print(f"    P₋ = blocks {{1,3}} = identity(000) block + all-ones(111) block")
print(f"    P₋ contains the EXTREMES (Kun=000, Qian=111)")
print(f"    P₊ contains neither extreme")

# Is this the Z₂³ predicate? P₊ = {blocks without extremes}?
# Block 0 has the complement pair (010,101) — neither is 000 or 111
# Block 2 has (100,110) — neither is 000 or 111
# So P₊ = blocks that don't contain 000 or 111.
# P₋ = blocks that contain 000 or 111.

print(f"\n  Predicate: P₋ = blocks containing an extreme (000 or 111)")
print(f"  Block 0: {'YES' if 0 in (2,5) or 7 in (2,5) else 'NO'} → {'P₋' if 0 in (2,5) or 7 in (2,5) else 'P₊'}")
print(f"  Block 1: {'YES' if 0 in (0,1) or 7 in (0,1) else 'NO'} → {'P₋' if 0 in (0,1) or 7 in (0,1) else 'P₊'}")
print(f"  Block 2: {'YES' if 0 in (4,6) or 7 in (4,6) else 'NO'} → {'P₋' if 0 in (4,6) or 7 in (4,6) else 'P₊'}")
print(f"  Block 3: {'YES' if 0 in (3,7) or 7 in (3,7) else 'NO'} → {'P₋' if 0 in (3,7) or 7 in (3,7) else 'P₊'}")

print(f"\n  ✓ P₋ = {{blocks containing Kun(000) or Qian(111)}}")
print(f"  ✓ P₊ = {{blocks without binary extremes}}")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 5: Is this Z₂³ predicate robust?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"PROBE 5: ROBUSTNESS OF THE Z₂³ PREDICATE")
print(f"{'=' * 70}")

# The predicate "contains 000 or 111" uses the Z₂³ structure.
# But the BLOCK ASSIGNMENT depends on which S₄ we chose.
# The traditional S₄ puts Kun(000) and Qian(111) in different blocks.
# Is this forced, or contingent on the specific representation?

# In Rep A: the blocks are {Kan,Li}, {Kun,Gen}, {Zhen,Dui}, {Xun,Qian}
# 000(Kun) is in block 1, 111(Qian) is in block 3. Different blocks.
# ι₁ (complement) maps 000↔111, and these are in different blocks.
# Since ι₁ maps between blocks (not within), this is necessary.

# Actually: ι₁ = complement = XOR 111. 
# ι₁ maps each block to some other block (it's a block permutation).
# 000 and 111 are ι₁-paired. Since ι₁ maps BETWEEN blocks (no shared
# pairs with ι₂ except Kan↔Li), 000 and 111 must be in different blocks.
# (Unless they're in the shared pair's block — but that's {Kan,Li}={010,101}.)

print(f"  000(Kun) and 111(Qian) are ι₁-paired (complements).")
print(f"  ι₁ permutes blocks, so they must be in different blocks.")
print(f"  The Kan↔Li block is the overlap block — it gets {{010,101}}.")
print(f"  So 000 and 111 go to two of the remaining 3 blocks.")
print(f"  They CANNOT be in the same block (ι₁ maps between blocks).")
print(f"  So exactly 2 blocks contain an extreme. This is forced.")

# But is the PARTITION {blocks with extremes} vs {blocks without} 
# the same as the traditional polarity across ALL valid S₄ representations?

# In Rep A: {blocks with extremes} = {1,3}, {without} = {0,2}
# This gives P₋ = {Kun,Gen,Xun,Qian}, P₊ = {Kan,Li,Zhen,Dui}
# Which matches the traditional polarity!

# But this depends on the specific block assignment.
# If we permuted which blocks get which trigrams, the predicate would change.
# However, the S₄ is determined up to the 24-element conjugacy class.
# And within that class, 000 and 111 always end up in different non-overlap blocks.

print(f"\n  The predicate 'block contains a binary extreme' is:")
print(f"  - Independent of the magic square")
print(f"  - Derived purely from Z₂³ + S₄ block structure")
print(f"  - Forced: 000 and 111 are ι₁-paired, hence in different blocks")
print(f"  - The 2+2 split it produces matches the traditional polarity")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 6: Verify the alternating parity pattern
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print(f"PROBE 6: MAGIC SQUARE PARITY ALTERNATION")
print(f"{'=' * 70}")

# Even if Z₂³ can provide the polarity, does the magic square add anything?
# Check: in the octagonal cycle, are odd and even pairs always alternating?

for c in sorted(cycles):
    parities = [p[0] % 2 for p in c]  # 1=odd pair, 0=even pair
    alternating = all(parities[i] != parities[(i+1)%4] for i in range(4))
    print(f"  Cycle: {c}")
    print(f"  Parities: {''.join('O' if p else 'E' for p in parities)}")
    print(f"  Alternating: {alternating}")

print(f"""
  The magic square forces alternating parity around the octagon.
  This means P₊ and P₋ blocks alternate geometrically.
  
  This is CONSISTENT with the Z₂³ predicate but ADDS geometric information:
  not just which blocks are P₊/P₋, but how they're arranged spatially.
""")

# ══════════════════════════════════════════════════════════════════════════════
# CONCLUSION
# ══════════════════════════════════════════════════════════════════════════════

print(f"{'=' * 70}")
print(f"CONCLUSION")
print(f"{'=' * 70}")

print(f"""
  THE POLARITY IS DERIVABLE WITHOUT THE MAGIC SQUARE.

  The Z₂³ predicate: P₋ = {{blocks containing a binary extreme (000 or 111)}}
  
  This is forced by:
  1. Z₂³ structure identifies 000 and 111 as extremes
  2. ι₁ (complement) pairs 000↔111
  3. ι₁ maps between blocks (not within) — so 000 and 111 are in different blocks
  4. The overlap block is {{Kan,Li}} = {{010,101}} — no extremes
  5. Exactly 2 of the remaining 3 blocks contain an extreme
  6. The 2+2 split matches the traditional polarity

  The magic square AGREES with this but is not NEEDED for it.
  The magic square adds GEOMETRIC arrangement (alternating parity on octagon)
  but the polarity partition itself is derivable from Z₂³ + S₄ alone.

  REVISED MINIMAL INPUT SET:
  1. Binary lines (yin/yang) → Z₂³
  2. FPF involutions → block structure → S₄
  3. Commutation → Rep A
  4. Outer-pair erasure → 互 → H
  + The polarity is FORCED by the interaction of inputs 1 and 2.
    No additional input needed.

  The magic square is a COORDINATE SYSTEM that realizes the polarity
  in number-theoretic terms, but the polarity exists independently of it.
""")
