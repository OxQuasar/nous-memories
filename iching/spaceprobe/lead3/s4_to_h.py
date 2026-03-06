"""
Does S₄'s block structure uniquely pick out H from the 7 order-4 subgroups of Z₂³?

The trigram space: 8 elements in 4 blocks of 2, acted on by S₄.
The hexagram space: doubled trigrams, three mirror pairs → Z₂³.
H = {id, O, MI, OMI} = {kernels where M=I}.

Question: what structural property of the S₄ block decomposition
singles out H among all order-4 subgroups of Z₂³?
"""

from itertools import combinations

# ══════════════════════════════════════════════════════════════════════════════
# Z₂³ and its subgroups
# ══════════════════════════════════════════════════════════════════════════════

# Elements of Z₂³ as 3-bit tuples (O, M, I)
Z2_3 = [(a,b,c) for a in range(2) for b in range(2) for c in range(2)]

# XOR operation
def xor3(a, b):
    return tuple(x^y for x,y in zip(a,b))

# All 7 order-4 subgroups of Z₂³ (= all 7 non-trivial elements, each generating
# a subgroup with id + that element + ... wait, Z₂³ is elementary abelian,
# every order-4 subgroup is Z₂×Z₂, isomorphic to choosing 2 generators)

# Order-4 subgroups of Z₂³: each is a 2-dimensional subspace.
# A subspace of dimension 2 in F₂³ is determined by its 3 non-identity elements
# (which form 3 pairs summing to 0, but in F₂ that means any 2 generate the third).
# Number of 2-dimensional subspaces of F₂³ = (2³-1)(2³-2)/((2²-1)(2²-2)) = 7*6/(3*2) = 7.

subgroups = []
id = (0,0,0)
nonzero = [e for e in Z2_3 if e != id]

for i, a in enumerate(nonzero):
    for b in nonzero[i+1:]:
        c = xor3(a, b)
        if c != id:
            sg = frozenset([id, a, b, c])
            if sg not in [frozenset(s) for s in subgroups]:
                subgroups.append(sorted(sg))

print(f"All {len(subgroups)} order-4 subgroups of Z₂³:")
names = {(0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
         (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'}

for i, sg in enumerate(subgroups):
    sg_names = [names[e] for e in sg]
    is_H = set(sg) == {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}
    tag = " ← H" if is_H else ""
    print(f"  {i+1}. {{{', '.join(sg_names)}}}{tag}")

# ══════════════════════════════════════════════════════════════════════════════
# The block structure
# ══════════════════════════════════════════════════════════════════════════════

# The 8 trigrams in 4 blocks of 2 (from the two-axiom characterization):
# Block 0: {Kan(010), Li(101)}     — ι₂ pair
# Block 1: {Kun(000), Gen(001)}    — ι₂ pair  
# Block 2: {Zhen(100), Dui(110)}   — ι₂ pair
# Block 3: {Xun(011), Qian(111)}   — ι₂ pair

BLOCKS = [
    (0b010, 0b101),  # Kan, Li
    (0b000, 0b001),  # Kun, Gen
    (0b100, 0b110),  # Zhen, Dui
    (0b011, 0b111),  # Xun, Qian
]

# The three involutions as permutations of the 8 trigrams:
# ι₁ (Fu Xi complement): XOR with 111
# ι₂ (KW/Lo Shu diametric): swap within each block
# ι₃ (He Tu): swap between blocks

print("\n" + "=" * 70)
print("BLOCK STRUCTURE")
print("=" * 70)

trig_names = {0b000: 'Kun', 0b001: 'Gen', 0b010: 'Kan', 0b011: 'Xun',
              0b100: 'Zhen', 0b101: 'Li', 0b110: 'Dui', 0b111: 'Qian'}

for i, (a, b) in enumerate(BLOCKS):
    print(f"  Block {i}: {{{trig_names[a]}({a:03b}), {trig_names[b]}({b:03b})}}")

# ══════════════════════════════════════════════════════════════════════════════
# How Z₂³ acts on blocks
# ══════════════════════════════════════════════════════════════════════════════

# Each element of Z₂³ is a mirror-pair operation on hexagrams.
# At the trigram level, it acts on the PAIR of trigrams (lower, upper).
# But we're asking about the BLOCK structure of individual trigrams.
#
# Actually, the connection is different. Let me think carefully.
#
# The hexagram h has lower trigram t_lo and upper trigram t_up.
# The mirror-pair kernel k = (O, M, I) tells us how t_lo and t_up relate:
#   O-bit = t_lo[0] ⊕ t_up[0]  (= L1 ⊕ L6)
#   M-bit = t_lo[1] ⊕ t_up[1]  (= L2 ⊕ L5) 
#   I-bit = t_lo[2] ⊕ t_up[2]  (= L3 ⊕ L4)
#
# So the kernel measures how the two trigrams differ, BIT BY BIT.
# The kernel (O, M, I) is the XOR of the two trigrams... but in a specific order.
# Actually: if h = (L1,L2,L3,L4,L5,L6), lower=(L1,L2,L3), upper=(L4,L5,L6)
# Then: kernel bit 0 = L1⊕L6 = lower[0]⊕upper[2]
#        kernel bit 1 = L2⊕L5 = lower[1]⊕upper[1]  
#        kernel bit 2 = L3⊕L4 = lower[2]⊕upper[0]
# So it's not just lower⊕upper, it's lower⊕reverse(upper).
#
# The question: when the KW pairing swaps a hexagram with its partner,
# what does that do to the blocks?

# Let me reframe. The S₄ acts on 4 blocks at n=3.
# At n=6, the hexagram is (t_lo, t_up) — a pair of trigrams.
# The mirror-pair operations (Z₂³) act on this pair.
# 
# Key insight: each mirror-pair operation can be decomposed into
# what it does to the BLOCK MEMBERSHIP of each trigram.
#
# For each element k of Z₂³, and each trigram t, define:
#   What block does t belong to?
#   What block does the "transformed" trigram belong to?
#
# But mirror-pair operations don't act on individual trigrams!
# They act on hexagrams = pairs of trigrams.
# 
# OK let me think about this differently.

print("\n" + "=" * 70)
print("BLOCK-LEVEL EFFECT OF EACH Z₂³ ELEMENT")
print("=" * 70)

# When we apply a mirror-pair operation k to hexagram (t_lo, t_up),
# we get a new hexagram whose trigrams may be in different blocks.
# But the operation isn't just XOR on each trigram independently.
#
# Mirror-pair operation k = (O, M, I) on hexagram (L1,...,L6):
#   L1' = L1 ⊕ O·(L1⊕L6_target)... no, this is getting confused.
#
# Let me be concrete. The KW partner of hexagram h is obtained by:
#   - If h is non-palindromic: reverse it (swap L1↔L6, L2↔L5, L3↔L4)
#   - If h is palindromic: complement it (flip all 6 bits)
#
# But mirror-pair operations are different. Let me re-derive.
# A mirror-pair XOR mask m = (m1,m2,m3,m4,m5,m6) is palindromic:
#   m = (a, b, c, c, b, a) where (a,b,c) is the kernel.
# Applying mask m to hexagram h gives h' = h ⊕ m.
# h' has: L1'=L1⊕a, L2'=L2⊕b, L3'=L3⊕c, L4'=L4⊕c, L5'=L5⊕b, L6'=L6⊕a
#
# Lower trigram of h: (L1, L2, L3)
# Lower trigram of h': (L1⊕a, L2⊕b, L3⊕c)
# Upper trigram of h: (L4, L5, L6) 
# Upper trigram of h': (L4⊕c, L5⊕b, L6⊕a)
#
# So: lower(h') = lower(h) ⊕ (a,b,c) = lower(h) ⊕ kernel
#     upper(h') = upper(h) ⊕ (c,b,a) = upper(h) ⊕ reverse(kernel)

print("  Mirror-pair kernel k = (O, M, I) acts on trigrams as:")
print("    lower → lower ⊕ (O, M, I)")
print("    upper → upper ⊕ (I, M, O)  [reversed kernel]")
print()

# So for each kernel k = (O,M,I):
# lower trigram gets XORed with k
# upper trigram gets XORed with reverse(k) = (I,M,O)

# Now: what does XORing a trigram with a fixed 3-bit mask do to its BLOCK membership?

def block_of(t):
    for i, (a, b) in enumerate(BLOCKS):
        if t == a or t == b:
            return i
    return -1

def within_block(t):
    """Which member of the block: 0 (first) or 1 (second)?"""
    for i, (a, b) in enumerate(BLOCKS):
        if t == a: return 0
        if t == b: return 1
    return -1

print("  Effect of each 3-bit XOR mask on block membership:")
print(f"  {'Mask':>5s}  {'Preserves blocks?':>18s}  {'Block permutation':>30s}")

for mask in range(8):
    mask_bits = ((mask>>2)&1, (mask>>1)&1, mask&1)
    mask_name = names.get(mask_bits, '?')
    
    # For each trigram, compute new block
    block_map = {}  # (block, position) → (block, position)
    preserves_blocks = True
    for t in range(8):
        t_new = t ^ mask
        b_old = block_of(t)
        b_new = block_of(t_new)
        w_old = within_block(t)
        w_new = within_block(t_new)
        block_map[(b_old, w_old)] = (b_new, w_new)
    
    # Check if it's a block permutation (both members of a block go to same block)
    for i in range(4):
        img_0 = block_map[(i, 0)][0]
        img_1 = block_map[(i, 1)][0]
        if img_0 != img_1:
            preserves_blocks = False
            break
    
    if preserves_blocks:
        perm = tuple(block_map[(i, 0)][0] for i in range(4))
        swaps = [block_map[(i, 0)][1] != 0 or block_map[(i, 1)][1] != 1 for i in range(4)]
        swap_str = "swaps:" + ''.join('S' if s else '.' for s in swaps)
        print(f"  {mask_name:>5s}  {'YES':>18s}  {str(perm):>20s}  {swap_str}")
    else:
        # Show what happens: blocks get scrambled
        print(f"  {mask_name:>5s}  {'NO (scrambles)':>18s}")

# ══════════════════════════════════════════════════════════════════════════════
# KEY TEST: For each Z₂³ element, what is the combined block effect?
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("COMBINED BLOCK EFFECT OF EACH MIRROR-PAIR OPERATION")
print("=" * 70)

print("  Each Z₂³ element k = (O,M,I) acts as:")
print("    lower trigram: XOR with (O,M,I)")
print("    upper trigram: XOR with (I,M,O)")
print()

for k in Z2_3:
    k_name = names[k]
    k_rev = (k[2], k[1], k[0])
    k_rev_int = k_rev[0]*4 + k_rev[1]*2 + k_rev[2]
    k_int = k[0]*4 + k[1]*2 + k[2]
    k_rev_name = names[k_rev]
    
    # Block effect on lower
    lo_block_perm = {}
    lo_within = {}
    for t in range(8):
        t_new = t ^ k_int
        b_old, b_new = block_of(t), block_of(t_new)
        w_old, w_new = within_block(t), within_block(t_new)
        lo_block_perm[b_old] = b_new
        lo_within[b_old] = (w_old != w_new)
    
    # Block effect on upper
    up_block_perm = {}
    up_within = {}
    for t in range(8):
        t_new = t ^ k_rev_int
        b_old, b_new = block_of(t), block_of(t_new)
        w_old, w_new = within_block(t), within_block(t_new)
        up_block_perm[b_old] = b_new
        up_within[b_old] = (w_old != w_new)
    
    lo_perm = tuple(lo_block_perm[i] for i in range(4))
    up_perm = tuple(up_block_perm[i] for i in range(4))
    same_perm = (lo_perm == up_perm)
    
    lo_any_swap = any(lo_within.values())
    up_any_swap = any(up_within.values())
    
    print(f"  {k_name:>3s}: lower mask={k}, upper mask={k_rev}")
    print(f"       lower blocks: {lo_perm}, swaps within: {lo_any_swap}")
    print(f"       upper blocks: {up_perm}, swaps within: {up_any_swap}")
    print(f"       SAME block permutation: {same_perm}")

# ══════════════════════════════════════════════════════════════════════════════
# THE ANSWER: Which subgroup preserves block-coherence?
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("WHICH Z₂³ ELEMENTS HAVE THE SAME BLOCK PERMUTATION ON BOTH TRIGRAMS?")
print("=" * 70)

coherent = []
for k in Z2_3:
    k_rev = (k[2], k[1], k[0])
    k_int = k[0]*4 + k[1]*2 + k[2]
    k_rev_int = k_rev[0]*4 + k_rev[1]*2 + k_rev[2]
    
    lo_perm = tuple(block_of(t ^ k_int) for t in [BLOCKS[i][0] for i in range(4)])
    up_perm = tuple(block_of(t ^ k_rev_int) for t in [BLOCKS[i][0] for i in range(4)])
    
    if lo_perm == up_perm:
        coherent.append(k)

coherent_names = [names[k] for k in coherent]
print(f"\n  Block-coherent elements: {{{', '.join(coherent_names)}}}")
is_H = set(coherent) == {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}
print(f"  This is H: {is_H}")

# Also check: which elements have SAME within-block effect?
print("\n  Also checking within-block consistency:")
fully_coherent = []
for k in Z2_3:
    k_rev = (k[2], k[1], k[0])
    k_int = k[0]*4 + k[1]*2 + k[2]
    k_rev_int = k_rev[0]*4 + k_rev[1]*2 + k_rev[2]
    
    consistent = True
    for i in range(4):
        a, b = BLOCKS[i]
        # lower trigram
        lo_a_new_block = block_of(a ^ k_int)
        lo_a_new_within = within_block(a ^ k_int)
        lo_b_new_block = block_of(b ^ k_int)
        lo_b_new_within = within_block(b ^ k_int)
        
        # upper trigram
        up_a_new_block = block_of(a ^ k_rev_int)
        up_a_new_within = within_block(a ^ k_rev_int)
        up_b_new_block = block_of(b ^ k_rev_int)
        up_b_new_within = within_block(b ^ k_rev_int)
        
        # Same block permutation AND same within-block effect
        if lo_a_new_block != up_a_new_block or (lo_a_new_within != within_block(a)) != (up_a_new_within != within_block(a)):
            consistent = False
            break
    
    if consistent:
        fully_coherent.append(k)

fully_coherent_names = [names[k] for k in fully_coherent]
print(f"  Fully coherent elements: {{{', '.join(fully_coherent_names)}}}")
