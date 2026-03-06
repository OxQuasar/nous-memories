#!/usr/bin/env python3
"""
Q3 Round 3: KW Pairing Verification and Closing Gaps
=====================================================

Bit convention (same as Rounds 1-2):
  L1 = MSB = bit 5  (bottom line), L6 = LSB = bit 0  (top line)
  O = 33, M = 18, I = 12. Complement = 63.
"""

import math
from io import StringIO
from collections import Counter
from sympy.combinatorics import Permutation, PermutationGroup

N = 64
BITS = 6
COMP = 63

MASK_O = 0b100001  # 33
MASK_M = 0b010010  # 18
MASK_I = 0b001100  # 12

TRIGRAM_NAMES = {  # keyed by value where bit0=bottom line, bit2=top line
    0b000: 'Kun', 0b001: 'Zhen', 0b010: 'Kan', 0b011: 'Dui',
    0b100: 'Gen', 0b101: 'Li',   0b110: 'Xun', 0b111: 'Qian',
}

# ── Bit operations ─────────────────────────────────────────────────────────

def reverse_bits(h):
    result = 0
    for i in range(BITS):
        if h & (1 << i):
            result |= 1 << (BITS - 1 - i)
    return result

def to_bin(h):
    return format(h, '06b')

def weight(h):
    return bin(h).count('1')

def hamming(a, b):
    return bin(a ^ b).count('1')

def upper_tri(h):
    return (h >> 3) & 0b111

def lower_tri(h):
    return h & 0b111

def mirror_residual(h):
    b = format(h, '06b')
    r0 = int(b[0]) ^ int(b[5])
    r1 = int(b[1]) ^ int(b[4])
    r2 = int(b[2]) ^ int(b[3])
    return (r0 << 2) | (r1 << 1) | r2

def swap_bits(h, i, j):
    bi = (h >> i) & 1
    bj = (h >> j) & 1
    if bi != bj:
        h ^= (1 << i) | (1 << j)
    return h

def pair_permute(h, pair_perm):
    pairs = [
        ((h >> 5) & 1, (h >> 0) & 1),
        ((h >> 4) & 1, (h >> 1) & 1),
        ((h >> 3) & 1, (h >> 2) & 1),
    ]
    new_pairs = [pairs[pair_perm[i]] for i in range(3)]
    result = 0
    result |= new_pairs[0][0] << 5 | new_pairs[0][1] << 0
    result |= new_pairs[1][0] << 4 | new_pairs[1][1] << 1
    result |= new_pairs[2][0] << 3 | new_pairs[2][1] << 2
    return result


# ── Permutation lists ──────────────────────────────────────────────────────

def xor_perm(mask):
    return [h ^ mask for h in range(N)]

perm_rev = [reverse_bits(h) for h in range(N)]
perm_comp = [h ^ COMP for h in range(N)]
perm_comp_rev = [reverse_bits(h) ^ COMP for h in range(N)]

perm_O = xor_perm(MASK_O)
perm_M = xor_perm(MASK_M)
perm_I = xor_perm(MASK_I)
perm_swap_L1L6 = [swap_bits(h, 5, 0) for h in range(N)]
perm_swap_L2L5 = [swap_bits(h, 4, 1) for h in range(N)]
perm_swap_L3L4 = [swap_bits(h, 3, 2) for h in range(N)]
perm_swap_OM = [pair_permute(h, [1, 0, 2]) for h in range(N)]
perm_cycle_OMI = [pair_permute(h, [2, 0, 1]) for h in range(N)]

# ── T-orbits ───────────────────────────────────────────────────────────────

T_MASKS = [0, MASK_O, MASK_M, MASK_I,
           MASK_O ^ MASK_M, MASK_O ^ MASK_I, MASK_M ^ MASK_I, COMP]

def t_orbit_of(h):
    return frozenset(h ^ m for m in T_MASKS)

# Build canonical T-orbits sorted by min element
_seen = set()
T_ORBITS = []  # list of frozensets, indexed 0..7
for h in range(N):
    orb = t_orbit_of(h)
    if orb not in _seen:
        _seen.add(orb)
        T_ORBITS.append(orb)
T_ORBITS.sort(key=lambda o: min(o))

# Residual for each orbit
ORBIT_RESIDUAL = [mirror_residual(min(orb)) for orb in T_ORBITS]

# Macro-orbit assignment: A=res000, B=res111, C=res_wt1, D=res_wt2
def macro_orbit_label(res):
    w = bin(res).count('1')
    if res == 0: return 'A'
    if res == 7: return 'B'
    if w == 1:   return 'C'
    return 'D'

# ── KW partner function ───────────────────────────────────────────────────

def kw_partner(h):
    r = reverse_bits(h)
    if r == h:
        return h ^ COMP
    return r

perm_kw = [kw_partner(h) for h in range(N)]


# ── Output capture ─────────────────────────────────────────────────────────

out = StringIO()

def pr(*args, **kwargs):
    print(*args, **kwargs)
    print(*args, **kwargs, file=out)


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: Enumerate the 9 Equivariant Pairings
# ═══════════════════════════════════════════════════════════════════════════

pr("=" * 72)
pr("PART 1: The 9 Equivariant Pairings")
pr("=" * 72)

# The 3 involution operations applied per-element
OPS = {
    'rev':     lambda h: reverse_bits(h),
    'comp':    lambda h: h ^ COMP,
    'comp_rev': lambda h: reverse_bits(h) ^ COMP,
}

# Macro-orbits A (res=000) and B (res=111) are forced.
# For A: rev(h)=h (palindromes), so only comp works.
# For B: rev(h)=comp(h) (anti-palindromes), so rev=comp; only 1 distinct pairing.
# Macro-orbits C (res wt=1, 3 T-orbits) and D (res wt=2, 3 T-orbits) have 3 choices each.

# Under equivariance, within a macro-orbit all T-orbits must use the same operation.
# So: 1 × 1 × 3 × 3 = 9 pairings.

OP_NAMES = ['rev', 'comp', 'comp_rev']

pr(f"\nFor each of 9 pairings: operation for macro-orbit C, operation for macro-orbit D.")
pr(f"Macro-orbits A and B always use complement (forced).\n")

pairing_table = []

for c_op_name in OP_NAMES:
    for d_op_name in OP_NAMES:
        c_op = OPS[c_op_name]
        d_op = OPS[d_op_name]

        # Build the 32 pairs
        pairs = []
        paired = set()
        for h in range(N):
            if h in paired:
                continue
            res = mirror_residual(h)
            label = macro_orbit_label(res)

            if label == 'A' or label == 'B':
                partner = h ^ COMP  # forced complement
            elif label == 'C':
                partner = c_op(h)
            else:  # D
                partner = d_op(h)

            assert partner != h or label in ('A', 'B'), \
                f"Fixed point: h={h}, label={label}, op_C={c_op_name}, op_D={d_op_name}"
            pairs.append((h, partner))
            paired.add(h)
            paired.add(partner)

        # Verify perfect matching
        all_elements = set()
        for a, b in pairs:
            all_elements.add(a)
            all_elements.add(b)
        assert len(all_elements) == 64 and len(pairs) == 32

        # Compute measures
        wt_sum = sum(abs(weight(a) - weight(b)) for a, b in pairs)
        wt = wt_sum / 32.0

        s = sum(hamming(a, b) for a, b in pairs)

        # Mask diversity: entropy of XOR mask multiset
        xor_masks = [a ^ b for a, b in pairs]
        mask_counts = Counter(xor_masks)
        total = len(xor_masks)
        entropy = -sum((c / total) * math.log2(c / total) for c in mask_counts.values())
        entropy = abs(entropy)  # avoid -0.0
        n_distinct_masks = len(mask_counts)

        pairing_table.append({
            'c_op': c_op_name, 'd_op': d_op_name,
            'pairs': pairs, 'WT': wt, 'S': s, 'D': entropy,
            'n_masks': n_distinct_masks, 'xor_masks': mask_counts,
        })

# Print table
pr(f"{'#':>2} {'C_op':>10} {'D_op':>10} {'S':>5} {'WT':>7} {'D(bits)':>8} {'#masks':>6}")
pr("-" * 55)
for i, row in enumerate(pairing_table):
    pr(f"{i+1:>2} {row['c_op']:>10} {row['d_op']:>10} "
       f"{row['S']:>5} {row['WT']:>7.3f} {row['D']:>8.3f} {row['n_masks']:>6}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: The Actual King Wen Pairing
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 2: The Actual King Wen Pairing")
pr("=" * 72)

kw_pairs = []
kw_paired = set()
for h in range(N):
    if h in kw_paired:
        continue
    p = kw_partner(h)
    kw_pairs.append((h, p))
    kw_paired.add(h)
    kw_paired.add(p)

assert len(kw_pairs) == 32

pr(f"\nKW pairs (32 total):")
pr(f"{'h':>6} {'partner':>8} {'XOR':>6} {'Δw':>4} {'H':>3} {'res':>5} {'orbit':>6} {'op':>10}")
pr("-" * 55)

kw_xor_masks = Counter()
for a, b in sorted(kw_pairs, key=lambda p: p[0]):
    mask = a ^ b
    kw_xor_masks[mask] += 1
    dw = abs(weight(a) - weight(b))
    h_dist = hamming(a, b)
    res = mirror_residual(a)
    label = macro_orbit_label(res)
    op = 'rev' if b == reverse_bits(a) else ('comp' if b == a ^ COMP else 'comp_rev')
    pr(f"{to_bin(a):>6} {to_bin(b):>8} {to_bin(mask):>6} {dw:>4} {h_dist:>3} "
       f"{format(res,'03b'):>5} {label:>6} {op:>10}")

# KW measures
kw_wt = sum(abs(weight(a) - weight(b)) for a, b in kw_pairs) / 32.0
kw_s = sum(hamming(a, b) for a, b in kw_pairs)
kw_total = len(kw_pairs)
kw_entropy = -sum((c / kw_total) * math.log2(c / kw_total) for c in kw_xor_masks.values())

pr(f"\nKW measures: S={kw_s}, WT={kw_wt:.3f}, D={kw_entropy:.3f}")
pr(f"Distinct XOR masks: {len(kw_xor_masks)}")
pr(f"Mask distribution: {dict(sorted(((to_bin(m), c) for m, c in kw_xor_masks.items())))}")

# Match against the 9 pairings
pr(f"\nMatching KW against the 9 equivariant pairings:")
kw_pair_set = set(frozenset(p) for p in kw_pairs)
for i, row in enumerate(pairing_table):
    row_pair_set = set(frozenset(p) for p in row['pairs'])
    if row_pair_set == kw_pair_set:
        pr(f"  KW matches pairing #{i+1}: C={row['c_op']}, D={row['d_op']} ✓")
        break
else:
    pr(f"  KW does NOT match any of the 9 pairings!")


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: Is the KW Pairing a Group Element of G₃₈₄?
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 3: KW Pairing as Group Element")
pr("=" * 72)

# Build G_384
p_O = Permutation(perm_O)
p_M = Permutation(perm_M)
p_I = Permutation(perm_I)
p_swap_L1L6 = Permutation(perm_swap_L1L6)
p_swap_L2L5 = Permutation(perm_swap_L2L5)
p_swap_L3L4 = Permutation(perm_swap_L3L4)
p_swap_OM = Permutation(perm_swap_OM)
p_cycle_OMI = Permutation(perm_cycle_OMI)
p_rev = Permutation(perm_rev)

G_384 = PermutationGroup(p_O, p_M, p_I,
                          p_swap_L1L6, p_swap_L2L5, p_swap_L3L4,
                          p_swap_OM, p_cycle_OMI)

p_kw = Permutation(perm_kw)
pr(f"\nKW permutation order: {p_kw.order()}")

# Cycle structure
cs = Counter()
for cycle in p_kw.cyclic_form:
    cs[len(cycle)] += 1
fp_count = N - sum(len(c) for c in p_kw.cyclic_form)
if fp_count > 0:
    cs[1] = fp_count
pr(f"Cycle structure: {dict(sorted(cs.items()))}")
pr(f"Fixed points: {fp_count}")
pr(f"2-cycles: {cs.get(2, 0)}")

pr(f"\nKW ∈ G_384? {G_384.contains(p_kw)}")

pr(f"\nExplanation:")
pr(f"  The KW pairing applies reversal on non-palindromes and complement on")
pr(f"  palindromes. A group element must apply a SINGLE algebraic operation")
pr(f"  uniformly. The KW hybrid uses different operations on different orbits,")
pr(f"  so it cannot be a group element unless the two operations happen to")
pr(f"  coincide on the relevant orbits (they don't — reversal and complement")
pr(f"  are distinct permutations).")

# Check: are the three pure involutions in G_384?
pr(f"\nPure involutions in G_384:")
p_comp = Permutation(perm_comp)
p_comp_rev = Permutation(perm_comp_rev)
pr(f"  σ₁ (complement) ∈ G_384? {G_384.contains(p_comp)}")
pr(f"  σ₂ (reversal) ∈ G_384? {G_384.contains(p_rev)}")
pr(f"  σ₃ (comp∘rev) ∈ G_384? {G_384.contains(p_comp_rev)}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: Palindromes and Anti-palindromes
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 4: Palindromes and Anti-palindromes")
pr("=" * 72)

palindromes = [h for h in range(N) if reverse_bits(h) == h]
anti_palindromes = [h for h in range(N) if reverse_bits(h) == h ^ COMP]

pr(f"\n8 Palindromes (rev(h) = h, all mirror pairs 'same'):")
pr(f"{'Binary':>8} {'Dec':>4} {'w':>3} {'Upper':>6} {'Lower':>6}")
pr("-" * 35)
for h in palindromes:
    u, l = upper_tri(h), lower_tri(h)
    pr(f"{to_bin(h):>8} {h:>4} {weight(h):>3} {TRIGRAM_NAMES[u]:>6} {TRIGRAM_NAMES[l]:>6}")

pr(f"\n8 Anti-palindromes (rev(h) = comp(h), all mirror pairs 'different'):")
pr(f"{'Binary':>8} {'Dec':>4} {'w':>3} {'Upper':>6} {'Lower':>6}")
pr("-" * 35)
for h in anti_palindromes:
    u, l = upper_tri(h), lower_tri(h)
    pr(f"{to_bin(h):>8} {h:>4} {weight(h):>3} {TRIGRAM_NAMES[u]:>6} {TRIGRAM_NAMES[l]:>6}")

# KW pairs among these
pr(f"\nKW pairs among palindromes (forced complement):")
for h in palindromes:
    p = kw_partner(h)
    if h < p:
        pr(f"  {to_bin(h)} ↔ {to_bin(p)}  "
           f"({TRIGRAM_NAMES[upper_tri(h)]}/{TRIGRAM_NAMES[lower_tri(h)]} ↔ "
           f"{TRIGRAM_NAMES[upper_tri(p)]}/{TRIGRAM_NAMES[lower_tri(p)]})")

pr(f"\nKW pairs among anti-palindromes (rev=comp, so KW uses reversal=complement):")
for h in anti_palindromes:
    p = kw_partner(h)
    if h < p:
        pr(f"  {to_bin(h)} ↔ {to_bin(p)}  "
           f"({TRIGRAM_NAMES[upper_tri(h)]}/{TRIGRAM_NAMES[lower_tri(h)]} ↔ "
           f"{TRIGRAM_NAMES[upper_tri(p)]}/{TRIGRAM_NAMES[lower_tri(p)]})")


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: Kernel of G₃₈₄ → S₃
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 5: Kernel of G₃₈₄ → S₃ (quotient action)")
pr("=" * 72)

# The kernel should be the elements that fix all T-orbits.
# This is ⟨O, M, I, swap_L1L6, swap_L2L5, swap_L3L4⟩ = Z₂⁶ (order 64).
K = PermutationGroup(p_O, p_M, p_I, p_swap_L1L6, p_swap_L2L5, p_swap_L3L4)

pr(f"\nK = ⟨O, M, I, swap_L1L6, swap_L2L5, swap_L3L4⟩")
pr(f"|K| = {K.order()}")
pr(f"Expected 384/6 = 64: {K.order() == 384 // 6}")
pr(f"K is abelian: {K.is_abelian}")
pr(f"K ≅ Z₂⁶: {K.order() == 64 and K.is_abelian and all(g.order() <= 2 for g in K.elements)}")

# Verify K is normal in G_384
pr(f"K ◁ G_384 (normal): {K.is_normal(G_384)}")

# Verify the S₃ generators are NOT in K
pr(f"\nswap_OM ∈ K? {K.contains(p_swap_OM)}")
pr(f"cycle_OMI ∈ K? {K.contains(p_cycle_OMI)}")

# Verify K preserves all T-orbits
pr(f"\nVerify K preserves all T-orbits:")
k_preserves = True
for g in K.elements:
    g_list = list(g.array_form)
    for orb in T_ORBITS:
        images = frozenset(g_list[h] for h in orb)
        if images != orb:
            k_preserves = False
            break
    if not k_preserves:
        break
pr(f"  All elements of K preserve all T-orbits: {k_preserves}")

# The quotient G_384/K ≅ S₃
pr(f"\n|G_384/K| = {G_384.order() // K.order()} (should be 6 = |S₃|)")

# What does K look like structurally?
pr(f"\nK structure:")
pr(f"  K = T × ⟨swaps⟩ where:")
pr(f"  T = ⟨O, M, I⟩ ≅ Z₂³ (pair-value flips)")
pr(f"  ⟨swaps⟩ = ⟨swap_L1L6, swap_L2L5, swap_L3L4⟩ ≅ Z₂³ (within-pair position swaps)")
pr(f"  K ≅ Z₂³ × Z₂³ ≅ Z₂⁶ (order 64)")

# Verify K = T × swaps (direct product, not just semidirect)
T_group = PermutationGroup(p_O, p_M, p_I)
Swaps_group = PermutationGroup(p_swap_L1L6, p_swap_L2L5, p_swap_L3L4)
pr(f"\n  |T| = {T_group.order()}, |Swaps| = {Swaps_group.order()}")
pr(f"  |T| × |Swaps| = {T_group.order() * Swaps_group.order()} = |K|? "
   f"{T_group.order() * Swaps_group.order() == K.order()}")

# Check T and Swaps commute
all_commute = True
for t_gen, t_name in [(perm_O, 'O'), (perm_M, 'M'), (perm_I, 'I')]:
    for s_gen, s_name in [(perm_swap_L1L6, 'sL1L6'), (perm_swap_L2L5, 'sL2L5'), (perm_swap_L3L4, 'sL3L4')]:
        ts = [t_gen[s_gen[h]] for h in range(N)]
        st = [s_gen[t_gen[h]] for h in range(N)]
        if ts != st:
            all_commute = False
            pr(f"  {t_name} and {s_name} do NOT commute!")
pr(f"  T and Swaps commute: {all_commute} → K = T × Swaps (direct product)")


# ═══════════════════════════════════════════════════════════════════════════
# PART 6: Summary Comparison Table
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 6: Summary — n=3 vs n=6")
pr("=" * 72)

# Find which pairing is KW
kw_idx = None
for i, row in enumerate(pairing_table):
    row_pair_set = set(frozenset(p) for p in row['pairs'])
    if row_pair_set == kw_pair_set:
        kw_idx = i
        break

kw_row = pairing_table[kw_idx] if kw_idx is not None else None

pr(f"""
| Property                    | n=3                     | n=6                              |
|-----------------------------|-------------------------|----------------------------------|
| State space                 | Z₂³ (8 elements)        | Z₂⁶ (64 elements)               |
| Translation group T         | Z₂³ (full, regular rep) | Z₂³ (subgroup, index 8)         |
| T-orbits                    | 1 (whole space)         | 8 (size 8 each)                  |
| Quotient Z/T                | trivial                 | Z₂³ (residual space)             |
| Ambient symmetry group      | ...                     | G₃₈₄ = (Z₂≀S₃)×Z₂³             |
| Quotient action             | S₄ on 4 blocks          | S₃ on 8 orbits → 4 macro-orbits |
| Macro-orbits                | 4 blocks of 2           | 4 orbits (8, 8, 24, 24)         |
| Kernel of quotient map      | ...                     | K ≅ Z₂⁶ (order 64)              |
| Equivariant pairings        | 9 (under Z₂²)          | 9 (under G₃₈₄)                  |
| Traditional pairing         | complement (ι₁)         | rev + comp hybrid (KW)           |
| Trad. pairing ∈ group?      | Yes (ι₁ ∈ Z₂³)         | No (KW ∉ G₃₈₄)                 |
| KW pairing: C_op / D_op    | —                       | rev / rev                        |
| KW S (opposition strength)  | —                       | {kw_row['S'] if kw_row else '?':>32} |
| KW WT (weight tilt)         | —                       | {f"{kw_row['WT']:.3f}" if kw_row else '?':>32} |
| KW D (mask diversity, bits) | —                       | {f"{kw_row['D']:.3f}" if kw_row else '?':>32} |
""")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: The 9 Pairings — Detailed View
# ═══════════════════════════════════════════════════════════════════════════

pr("=" * 72)
pr("PART 7: Detailed View of All 9 Pairings")
pr("=" * 72)

pr(f"\n{'#':>2} {'C_op':>10} {'D_op':>10} {'S':>5} {'WT':>7} {'D':>7} {'#masks':>6} {'KW?':>4}")
pr("-" * 58)
for i, row in enumerate(pairing_table):
    is_kw = '✓' if i == kw_idx else ''
    pr(f"{i+1:>2} {row['c_op']:>10} {row['d_op']:>10} "
       f"{row['S']:>5} {row['WT']:>7.3f} {row['D']:>7.3f} {row['n_masks']:>6} {is_kw:>4}")

# Highlight extremes
s_values = [r['S'] for r in pairing_table]
wt_values = [r['WT'] for r in pairing_table]
d_values = [r['D'] for r in pairing_table]

pr(f"\nExtremes:")
pr(f"  Max S (opposition strength): {max(s_values)} "
   f"(pairing #{s_values.index(max(s_values))+1})")
pr(f"  Min S: {min(s_values)} "
   f"(pairing #{s_values.index(min(s_values))+1})")
pr(f"  Min WT (weight tilt): {min(wt_values):.3f} "
   f"(pairing #{wt_values.index(min(wt_values))+1})")
pr(f"  Max D (diversity): {max(d_values):.3f} "
   f"(pairing #{d_values.index(max(d_values))+1})")

if kw_idx is not None:
    pr(f"\n  KW (pairing #{kw_idx+1}): S={kw_row['S']}, WT={kw_row['WT']:.3f}, "
       f"D={kw_row['D']:.3f}")
    pr(f"  KW has min WT? {kw_row['WT'] == min(wt_values)}")
    pr(f"  KW has max S? {kw_row['S'] == max(s_values)}")

# Mask vocabulary for KW
pr(f"\nKW mask vocabulary:")
for mask, count in sorted(kw_xor_masks.items(), key=lambda x: x[0]):
    # Identify which OMI combination
    for mn, mv in zip(['O', 'M', 'I', 'O⊕M', 'O⊕I', 'M⊕I', 'O⊕M⊕I'],
                      [MASK_O, MASK_M, MASK_I, MASK_O^MASK_M, MASK_O^MASK_I,
                       MASK_M^MASK_I, COMP]):
        if mask == mv:
            pr(f"  {to_bin(mask)} = {mn:8s}: {count} pairs")
            break
    else:
        pr(f"  {to_bin(mask)} = ???     : {count} pairs")


# ── Save ───────────────────────────────────────────────────────────────────

raw_path = "memories/iching/spaceprobe/q3/round3_raw_output.txt"
with open(raw_path, 'w') as f:
    f.write(out.getvalue())

print(f"\nRaw output saved to {raw_path}")
