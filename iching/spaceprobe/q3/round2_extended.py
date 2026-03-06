#!/usr/bin/env python3
"""
Q3 Round 2: Extended Involution Analysis at n=6
================================================

Extends Round 1 (which found G=⟨σ₁,σ₂⟩≅V₄, structurally trivial) by
analyzing the mirror-pair XOR translation group and additional involutions.

Bit convention (same as Round 1):
  L1 = MSB = bit 5  (bottom line)
  L6 = LSB = bit 0  (top line)
  Integer = L1·32 + L2·16 + L3·8 + L4·4 + L5·2 + L6·1

Mirror-pair XOR masks:
  O (outer) = flip L1,L6 = 0b100001 = 33
  M (middle) = flip L2,L5 = 0b010010 = 18
  I (inner) = flip L3,L4 = 0b001100 = 12

Note: O⊕M⊕I = 63 = σ₁ (complement).

Additional involutions:
  σ₂ (reversal): reverse 6-bit string
  σ₄ (trigram swap): swap upper trigram (L1,L2,L3) ↔ lower trigram (L4,L5,L6)
  swap_LiLj: exchange bit positions i and j
"""

from io import StringIO
from sympy.combinatorics import Permutation, PermutationGroup

N = 64
BITS = 6

# ── Mirror-pair XOR mask values ────────────────────────────────────────────

MASK_O = 0b100001  # 33 — outer pair L1,L6
MASK_M = 0b010010  # 18 — middle pair L2,L5
MASK_I = 0b001100  # 12 — inner pair L3,L4

# ── Trigram names for orbit labeling ───────────────────────────────────────

TRIGRAM_NAMES = {  # keyed by value where bit0=bottom line, bit2=top line
    0b000: 'Kun', 0b001: 'Zhen', 0b010: 'Kan', 0b011: 'Dui',
    0b100: 'Gen', 0b101: 'Li',   0b110: 'Xun', 0b111: 'Qian',
}

# ── Bit operations ─────────────────────────────────────────────────────────

def reverse_bits(h):
    """σ₂: reverse 6-bit string."""
    result = 0
    for i in range(BITS):
        if h & (1 << i):
            result |= 1 << (BITS - 1 - i)
    return result

def trigram_swap(h):
    """σ₄: swap upper trigram (bits 5,4,3) ↔ lower trigram (bits 2,1,0)."""
    upper = (h >> 3) & 0b111
    lower = h & 0b111
    return (lower << 3) | upper

def swap_bits(h, i, j):
    """Swap bit positions i and j in h."""
    bi = (h >> i) & 1
    bj = (h >> j) & 1
    if bi != bj:
        h ^= (1 << i) | (1 << j)
    return h

def to_bin(h):
    return format(h, '06b')

def upper_trigram(h):
    """Bits 5,4,3 → upper trigram."""
    return (h >> 3) & 0b111

def lower_trigram(h):
    """Bits 2,1,0 → lower trigram."""
    return h & 0b111


# ── Build permutation lists ───────────────────────────────────────────────

def xor_perm(mask):
    """XOR translation by mask as permutation list."""
    return [h ^ mask for h in range(N)]

perm_O = xor_perm(MASK_O)
perm_M = xor_perm(MASK_M)
perm_I = xor_perm(MASK_I)
perm_sigma2 = [reverse_bits(h) for h in range(N)]
perm_sigma4 = [trigram_swap(h) for h in range(N)]

# Position swaps: swap_L1L6 = swap bits 5,0; swap_L2L5 = swap bits 4,1; swap_L3L4 = swap bits 3,2
perm_swap_L1L6 = [swap_bits(h, 5, 0) for h in range(N)]
perm_swap_L2L5 = [swap_bits(h, 4, 1) for h in range(N)]
perm_swap_L3L4 = [swap_bits(h, 3, 2) for h in range(N)]

# ── Sympy permutation objects ─────────────────────────────────────────────

p_O = Permutation(perm_O)
p_M = Permutation(perm_M)
p_I = Permutation(perm_I)
p_sigma2 = Permutation(perm_sigma2)
p_sigma4 = Permutation(perm_sigma4)
p_swap_L1L6 = Permutation(perm_swap_L1L6)
p_swap_L2L5 = Permutation(perm_swap_L2L5)
p_swap_L3L4 = Permutation(perm_swap_L3L4)


# ── Output capture ─────────────────────────────────────────────────────────

out = StringIO()

def pr(*args, **kwargs):
    print(*args, **kwargs)
    print(*args, **kwargs, file=out)

def compute_orbits_from_perm_list(generators):
    """Compute orbits using union-find on permutation lists."""
    parent = list(range(N))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[a] = b
    for perm in generators:
        for h in range(N):
            union(h, perm[h])
    orbits = {}
    for h in range(N):
        r = find(h)
        orbits.setdefault(r, set()).add(h)
    return list(orbits.values())


# ═══════════════════════════════════════════════════════════════════════════
# PART 1: Mirror-pair translation group T = ⟨O, M, I⟩
# ═══════════════════════════════════════════════════════════════════════════

pr("=" * 72)
pr("PART 1: Mirror-pair Translation Group T = ⟨O, M, I⟩")
pr("=" * 72)

T = PermutationGroup(p_O, p_M, p_I)
pr(f"\n|T| = {T.order()}")
pr(f"T is abelian: {T.is_abelian}")

# Verify T ≅ Z₂³
elem_orders = sorted([g.order() for g in T.elements])
pr(f"Element orders: {elem_orders}")
pr(f"All order ≤ 2: {all(o <= 2 for o in elem_orders)}")
pr(f"T ≅ Z₂³: {T.order() == 8 and T.is_abelian and all(o <= 2 for o in elem_orders)}")

# List the 7 nonzero masks
pr(f"\nThe 7 nonzero XOR masks in T:")
masks = [MASK_O, MASK_M, MASK_I,
         MASK_O ^ MASK_M, MASK_O ^ MASK_I, MASK_M ^ MASK_I,
         MASK_O ^ MASK_M ^ MASK_I]
mask_names = ['O', 'M', 'I', 'O⊕M', 'O⊕I', 'M⊕I', 'O⊕M⊕I']
for name, mask in zip(mask_names, masks):
    pr(f"  {name:8s} = {to_bin(mask)} = {mask}")

pr(f"\nO⊕M⊕I = {MASK_O ^ MASK_M ^ MASK_I} = σ₁ (complement)? "
   f"{'✓' if MASK_O ^ MASK_M ^ MASK_I == 63 else '✗'}")

# Orbits of T
t_orbits = T.orbits()
t_orbits_sorted = sorted(t_orbits, key=lambda o: min(o))
pr(f"\nOrbits of T on {{0,...,63}}: {len(t_orbits_sorted)} orbits")
orbit_sizes = sorted([len(o) for o in t_orbits_sorted])
pr(f"Orbit sizes: {orbit_sizes}")
pr(f"All size 8 (T acts freely): {all(s == 8 for s in orbit_sizes)}")

# The subgroup of Z₂⁶ generated by {O,M,I}
subgroup_elems = {0, MASK_O, MASK_M, MASK_I,
                  MASK_O ^ MASK_M, MASK_O ^ MASK_I, MASK_M ^ MASK_I,
                  MASK_O ^ MASK_M ^ MASK_I}
pr(f"\nT as subgroup of Z₂⁶: {sorted(subgroup_elems)}")
pr(f"  = {{0, O, M, I, OM, OI, MI, OMI}} = {{0, 33, 18, 12, 51, 45, 30, 63}}")

# List the 8 orbits and identify with trigrams
pr(f"\nThe 8 T-orbits (cosets of T in Z₂⁶):")
orbit_reps = {}  # rep → orbit set
orbit_to_idx = {}  # frozenset → index
for i, orb in enumerate(t_orbits_sorted):
    rep = min(orb)
    orbit_reps[rep] = orb
    orbit_to_idx[frozenset(orb)] = i
    elements_str = ', '.join(f'{h}({to_bin(h)})' for h in sorted(orb))
    pr(f"  Orbit {i}: rep={rep}({to_bin(rep)}): {elements_str}")

# Identify orbits with trigrams via residual structure
pr(f"\nOrbit-trigram identification:")
pr(f"  Each orbit is a coset h + T in Z₂⁶.")
pr(f"  The coset is determined by the 'residual' bits not affected by T.")
pr(f"  T acts on mirror pairs: {{L1,L6}}, {{L2,L5}}, {{L3,L4}}.")
pr(f"  Within each pair, T can flip both bits simultaneously.")
pr(f"  The residual = the XOR within each pair: L1⊕L6, L2⊕L5, L3⊕L4.")

# Compute residual for each hexagram
def mirror_residual(h):
    """3-bit residual: (L1⊕L6, L2⊕L5, L3⊕L4)."""
    b = format(h, '06b')
    r0 = int(b[0]) ^ int(b[5])  # L1⊕L6
    r1 = int(b[1]) ^ int(b[4])  # L2⊕L5
    r2 = int(b[2]) ^ int(b[3])  # L3⊕L4
    return (r0 << 2) | (r1 << 1) | r2

pr(f"\n  Orbit residuals:")
for i, orb in enumerate(t_orbits_sorted):
    residuals = set(mirror_residual(h) for h in orb)
    assert len(residuals) == 1, f"Orbit {i} has multiple residuals!"
    r = residuals.pop()
    pr(f"    Orbit {i}: residual = {format(r, '03b')} ({r})")

# Check: is the residual the same as one of the trigrams?
pr(f"\n  The residual (L1⊕L6, L2⊕L5, L3⊕L4) encodes whether each mirror")
pr(f"  pair is 'same' (0) or 'different' (1). This is exactly the signature")
pr(f"  of the hexagram under the OMI decomposition.")
pr(f"  Palindromes have residual 000 (all pairs same).")
pr(f"  Anti-palindromes have residual 111 (all pairs different).")

# Alternative: check if orbits correspond to upper or lower trigram
pr(f"\n  Do orbits correspond to upper trigram?")
for i, orb in enumerate(t_orbits_sorted):
    uppers = set(upper_trigram(h) for h in orb)
    lowers = set(lower_trigram(h) for h in orb)
    pr(f"    Orbit {i}: upper trigrams = {sorted(uppers)}, "
       f"lower trigrams = {sorted(lowers)}")

pr(f"\n  Neither upper nor lower trigram is constant within a T-orbit.")
pr(f"  This is expected: O flips both L1 and L6, crossing the")
pr(f"  upper/lower boundary. T acts on mirror pairs, not on trigrams.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 2: G_ext = ⟨O, M, I, σ₂⟩
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 2: G_ext = ⟨O, M, I, σ₂⟩")
pr("=" * 72)

# Check: does σ₂ commute with O, M, I?
pr(f"\nCommutation check (σ₂ with mask generators):")
for name, p_mask, perm_mask in [("O", p_O, perm_O), ("M", p_M, perm_M), ("I", p_I, perm_I)]:
    # σ₂ ∘ mask ∘ σ₂⁻¹ should equal mask (since σ₂²=id, σ₂⁻¹=σ₂)
    conjugate = [perm_sigma2[perm_mask[perm_sigma2[h]]] for h in range(N)]
    commutes = (conjugate == perm_mask)
    if not commutes:
        # What does the conjugate equal?
        conj_mask = None
        for m_name, m_val in zip(mask_names, masks):
            if conjugate == xor_perm(m_val):
                conj_mask = m_name
                break
        pr(f"  σ₂∘{name}∘σ₂ = {conj_mask or 'unknown'} (does NOT commute)")
    else:
        pr(f"  σ₂∘{name}∘σ₂ = {name} ✓ (commutes)")

G_ext = PermutationGroup(p_O, p_M, p_I, p_sigma2)
pr(f"\n|G_ext| = {G_ext.order()}")
pr(f"G_ext is abelian: {G_ext.is_abelian}")
pr(f"G_ext is solvable: {G_ext.is_solvable}")

# Check if G_ext = T × ⟨σ₂⟩
pr(f"\nExpected |T × ⟨σ₂⟩| = |T| × |⟨σ₂⟩| = 8 × 2 = 16")
pr(f"Actual |G_ext| = {G_ext.order()}")
is_direct_product = (G_ext.order() == 16 and G_ext.is_abelian)
pr(f"G_ext = T × ⟨σ₂⟩ ≅ Z₂⁴: {is_direct_product}")

# Orbits
g_ext_orbits = G_ext.orbits()
g_ext_orbits_sorted = sorted(g_ext_orbits, key=lambda o: min(o))
pr(f"\nOrbits of G_ext on {{0,...,63}}: {len(g_ext_orbits_sorted)} orbits")
g_ext_sizes = sorted([len(o) for o in g_ext_orbits_sorted])
pr(f"Orbit sizes: {g_ext_sizes}")

# Does σ₂ respect T-orbits?
pr(f"\nDoes σ₂ map each T-orbit to itself?")
sigma2_preserves_all = True
for i, orb in enumerate(t_orbits_sorted):
    # Apply σ₂ to each element, check if result stays in same T-orbit
    images = set(perm_sigma2[h] for h in orb)
    preserved = (images == orb)
    if not preserved:
        # Find which orbit the images land in
        for j, orb2 in enumerate(t_orbits_sorted):
            if images <= orb2:
                pr(f"  Orbit {i} → Orbit {j} (NOT preserved)")
                sigma2_preserves_all = False
                break
    else:
        pr(f"  Orbit {i} → Orbit {i} ✓")
pr(f"σ₂ preserves all T-orbits: {sigma2_preserves_all}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 3: Action on 8 T-orbits (quotient action)
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 3: Action on 8 T-orbits (quotient)")
pr("=" * 72)

if sigma2_preserves_all:
    pr(f"\nσ₂ acts trivially on T-orbits (fixes each orbit).")
    pr(f"T acts regularly on itself (transitive on each orbit).")
    pr(f"The quotient action of G_ext on the 8 orbits is trivial.")
    pr(f"This is the key structural difference from n=3:")
    pr(f"  At n=3, the additional involutions acted NONTRIVIALLY on blocks.")
    pr(f"  At n=6, σ₂ acts trivially because reversal commutes with all")
    pr(f"  mirror-pair masks. We need a different generator.")


# ═══════════════════════════════════════════════════════════════════════════
# PART 4: Upper/lower trigram swap σ₄
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 4: Trigram Swap σ₄")
pr("=" * 72)

pr(f"\nσ₄: swap upper (L1,L2,L3) ↔ lower (L4,L5,L6)")
pr(f"σ₄ order: {p_sigma4.order()}")

# Fixed points
fp_sigma4 = [h for h in range(N) if perm_sigma4[h] == h]
pr(f"Fixed points: {len(fp_sigma4)}")
pr(f"  (hexagrams where upper = lower trigram)")
for h in fp_sigma4:
    u, l = upper_trigram(h), lower_trigram(h)
    pr(f"  {h}({to_bin(h)}): upper={TRIGRAM_NAMES[u]}, lower={TRIGRAM_NAMES[l]}")

# Cycle structure
from collections import Counter
visited = [False] * N
cycles = []
for start in range(N):
    if visited[start]:
        continue
    cycle = []
    h = start
    while not visited[h]:
        visited[h] = True
        cycle.append(h)
        h = perm_sigma4[h]
    cycles.append(len(cycle))
cs = Counter(cycles)
pr(f"Cycle structure: {dict(sorted(cs.items()))}")

# Does σ₄ normalize T?
pr(f"\nConjugation: σ₄ on T generators:")
for name, perm_mask in [("O", perm_O), ("M", perm_M), ("I", perm_I)]:
    conjugate = [perm_sigma4[perm_mask[perm_sigma4[h]]] for h in range(N)]
    found = None
    for m_name, m_val in zip(mask_names, masks):
        if conjugate == xor_perm(m_val):
            found = m_name
            break
    if conjugate == list(range(N)):
        found = "identity"
    pr(f"  σ₄∘{name}∘σ₄ = {found or 'unknown'}")

pr(f"\n  σ₄ acts on {{O,M,I}} as: O ↔ I, M ↔ M")
pr(f"  This is the transposition (O I) fixing M.")
pr(f"  σ₄ normalizes T but permutes its generators.")

# Does σ₄ commute with σ₂?
conj_sigma2 = [perm_sigma4[perm_sigma2[perm_sigma4[h]]] for h in range(N)]
pr(f"\nσ₄ commutes with σ₂: {conj_sigma2 == perm_sigma2}")

# What is σ₄∘σ₂?
sigma4_sigma2 = [perm_sigma4[perm_sigma2[h]] for h in range(N)]
sigma2_sigma4 = [perm_sigma2[perm_sigma4[h]] for h in range(N)]
pr(f"σ₄∘σ₂ == σ₂∘σ₄: {sigma4_sigma2 == sigma2_sigma4}")

# Check if σ₄∘σ₂ = σ₂∘σ₄ or if their product is interesting
p_sigma4_sigma2 = Permutation(sigma4_sigma2)
pr(f"ord(σ₄∘σ₂) = {p_sigma4_sigma2.order()}")

# How σ₄ permutes the 8 T-orbits
pr(f"\nσ₄ action on T-orbits:")
sigma4_orbit_perm = []
for i, orb in enumerate(t_orbits_sorted):
    images = set(perm_sigma4[h] for h in orb)
    for j, orb2 in enumerate(t_orbits_sorted):
        if images == orb2:
            sigma4_orbit_perm.append(j)
            break
    res_src = mirror_residual(min(orb))
    res_dst = mirror_residual(min(images))
    pr(f"  Orbit {i} (res={format(res_src,'03b')}) → Orbit {sigma4_orbit_perm[-1]} "
       f"(res={format(res_dst,'03b')})")

pr(f"\nσ₄ orbit permutation: {sigma4_orbit_perm}")
# Identify this permutation
p_sigma4_on_orbits = Permutation(sigma4_orbit_perm)
pr(f"Order on orbits: {p_sigma4_on_orbits.order()}")
pr(f"Cyclic form on orbits: {p_sigma4_on_orbits.cyclic_form}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 5: G_full = ⟨O, M, I, σ₂, σ₄⟩
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 5: G_full = ⟨O, M, I, σ₂, σ₄⟩")
pr("=" * 72)

G_full = PermutationGroup(p_O, p_M, p_I, p_sigma2, p_sigma4)
pr(f"\n|G_full| = {G_full.order()}")
pr(f"G_full is abelian: {G_full.is_abelian}")
pr(f"G_full is solvable: {G_full.is_solvable}")
pr(f"G_full is nilpotent: {G_full.is_nilpotent}")

# Orbits
g_full_orbits = G_full.orbits()
g_full_orbits_sorted = sorted(g_full_orbits, key=lambda o: min(o))
pr(f"\nOrbits on {{0,...,63}}: {len(g_full_orbits_sorted)} orbits")
pr(f"Orbit sizes: {sorted([len(o) for o in g_full_orbits_sorted])}")

for i, orb in enumerate(g_full_orbits_sorted):
    pr(f"  Orbit {i} (size {len(orb)}): {sorted(orb)[:8]}{'...' if len(orb)>8 else ''}")

# Center, derived subgroup
center_full = G_full.center()
pr(f"\n|Z(G_full)| = {center_full.order()}")

derived_full = G_full.derived_subgroup()
pr(f"|[G_full, G_full]| = {derived_full.order()}")
pr(f"|G_full/[G_full,G_full]| = {G_full.order() // derived_full.order()}")

# Identify the group
g_order = G_full.order()
pr(f"\nGroup identification (order {g_order}):")
if g_order <= 128:
    orders_count = Counter(g.order() for g in G_full.elements)
    pr(f"  Element order distribution: {dict(sorted(orders_count.items()))}")

# Quotient action on T-orbits
pr(f"\nQuotient action of G_full on the 8 T-orbits:")

# σ₂ on orbits (already known to be trivial if sigma2_preserves_all)
sigma2_orbit_perm = []
for i, orb in enumerate(t_orbits_sorted):
    images = set(perm_sigma2[h] for h in orb)
    for j, orb2 in enumerate(t_orbits_sorted):
        if images == orb2:
            sigma2_orbit_perm.append(j)
            break
pr(f"  σ₂ on orbits: {sigma2_orbit_perm} (trivial: {sigma2_orbit_perm == list(range(8))})")
pr(f"  σ₄ on orbits: {sigma4_orbit_perm}")

# Build the quotient group on orbits
p_s2_orbits = Permutation(sigma2_orbit_perm)
p_s4_orbits = Permutation(sigma4_orbit_perm)
G_quotient = PermutationGroup(p_s2_orbits, p_s4_orbits)
pr(f"\n  Quotient group on orbits:")
pr(f"  |G_quotient| = {G_quotient.order()}")
pr(f"  G_quotient is abelian: {G_quotient.is_abelian}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 6: The 384-element mirror-pair partition group
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 6: Mirror-pair Partition Group G_384")
pr("=" * 72)

pr(f"""
The 384-element group from the opposition theory is (Z₂ ≀ S₃) × Z₂³,
the stabilizer of the mirror-pair partition in B₆ (hyperoctahedral group).

Its generators in B₆ (signed permutations of 6 coordinates):
  - Z₂³ = pair-value flips: O, M, I (XOR masks)
  - Z₂³ = within-pair position swaps: swap L1↔L6, swap L2↔L5, swap L3↔L4
  - S₃ = permutations of the 3 mirror pairs AS UNITS

The within-pair swaps and XOR masks all commute (both act independently
on each mirror pair). These give Z₂⁶ (order 64). The S₃ factor permutes
the 3 pairs, giving the wreath product structure.
""")

# Build pair permutations (S₃ on the 3 mirror pairs)
# Pair labeling: pair_O = {L1,L6} = {bit5,bit0}, pair_M = {L2,L5} = {bit4,bit1},
#                pair_I = {L3,L4} = {bit3,bit2}

def pair_permute(h, pair_perm):
    """Apply a permutation of the 3 mirror pairs.
    pair_perm maps pair index → pair index.
    Pair 0 = O = {bit5, bit0}, Pair 1 = M = {bit4, bit1}, Pair 2 = I = {bit3, bit2}.
    """
    # Extract the two bits from each pair
    pairs = [
        ((h >> 5) & 1, (h >> 0) & 1),  # pair O: (bit5, bit0) = (L1, L6)
        ((h >> 4) & 1, (h >> 1) & 1),  # pair M: (bit4, bit1) = (L2, L5)
        ((h >> 3) & 1, (h >> 2) & 1),  # pair I: (bit3, bit2) = (L3, L4)
    ]
    # Apply permutation: new pair at position i gets old pair at pair_perm[i]
    new_pairs = [pairs[pair_perm[i]] for i in range(3)]
    # Reconstruct hexagram
    result = 0
    result |= new_pairs[0][0] << 5 | new_pairs[0][1] << 0  # pair O positions
    result |= new_pairs[1][0] << 4 | new_pairs[1][1] << 1  # pair M positions
    result |= new_pairs[2][0] << 3 | new_pairs[2][1] << 2  # pair I positions
    return result

# S₃ is generated by two elements: (0 1) and (0 1 2)
# Transposition: swap pairs O↔M (leaving I fixed)
perm_swap_OM = [pair_permute(h, [1, 0, 2]) for h in range(N)]
# 3-cycle: O→M→I→O
perm_cycle_OMI = [pair_permute(h, [2, 0, 1]) for h in range(N)]

p_swap_OM = Permutation(perm_swap_OM)
p_cycle_OMI = Permutation(perm_cycle_OMI)

pr(f"S₃ generators on mirror pairs:")
pr(f"  swap_OM (O↔M, I fixed) order: {p_swap_OM.order()}")
pr(f"  cycle_OMI (O→M→I→O) order: {p_cycle_OMI.order()}")

# Verify σ₄ is the pair transposition O↔I
perm_swap_OI = [pair_permute(h, [2, 1, 0]) for h in range(N)]
pr(f"\n  σ₄ == pair_swap O↔I? {perm_swap_OI == perm_sigma4}")

# Verify conjugation: swap_OM should map O→M, M→O, I→I
pr(f"\nConjugation by swap_OM:")
for mask_name, perm_mask in [("O", perm_O), ("M", perm_M), ("I", perm_I)]:
    conjugate = [perm_swap_OM[perm_mask[perm_swap_OM[h]]] for h in range(N)]
    found = None
    for mn, mv in zip(mask_names, masks):
        if conjugate == xor_perm(mv):
            found = mn
            break
    pr(f"  swap_OM ∘ {mask_name} ∘ swap_OM = {found}")

pr(f"\nConjugation by cycle_OMI:")
# cycle_OMI has order 3, so inverse = cycle^2
inv_cycle = [perm_cycle_OMI[perm_cycle_OMI[h]] for h in range(N)]
for mask_name, perm_mask in [("O", perm_O), ("M", perm_M), ("I", perm_I)]:
    conjugate = [perm_cycle_OMI[perm_mask[inv_cycle[h]]] for h in range(N)]
    found = None
    for mn, mv in zip(mask_names, masks):
        if conjugate == xor_perm(mv):
            found = mn
            break
    pr(f"  cycle_OMI ∘ {mask_name} ∘ cycle_OMI⁻¹ = {found}")

# Build the full 384-element group
pr(f"\nBuilding G_384 = ⟨O, M, I, swap_L1L6, swap_L2L5, swap_L3L4, swap_OM, cycle_OMI⟩")
G_384 = PermutationGroup(p_O, p_M, p_I,
                          p_swap_L1L6, p_swap_L2L5, p_swap_L3L4,
                          p_swap_OM, p_cycle_OMI)
pr(f"|G_384| = {G_384.order()}")
pr(f"Expected 384: {G_384.order() == 384}")
pr(f"G_384 is abelian: {G_384.is_abelian}")
pr(f"G_384 is solvable: {G_384.is_solvable}")

# Also try just ⟨O, M, I, swap_OM, cycle_OMI⟩ (without position swaps)
G_wreath_only = PermutationGroup(p_O, p_M, p_I, p_swap_OM, p_cycle_OMI)
pr(f"\n|⟨O, M, I, swap_OM, cycle_OMI⟩| (T ⋊ S₃, no pos swaps) = {G_wreath_only.order()}")
pr(f"Expected Z₂³ ⋊ S₃ = Z₂ ≀ S₃ = 48: {G_wreath_only.order() == 48}")

# And just ⟨swap_L1L6, swap_L2L5, swap_L3L4, swap_OM, cycle_OMI⟩ (no XOR masks)
G_pos_only = PermutationGroup(p_swap_L1L6, p_swap_L2L5, p_swap_L3L4, p_swap_OM, p_cycle_OMI)
pr(f"|⟨swaps, S₃_pairs⟩| (position ops only) = {G_pos_only.order()}")

# Check: is σ₂ in G_384?
pr(f"\nσ₂ ∈ G_384? {G_384.contains(p_sigma2)}")
pr(f"σ₄ ∈ G_384? {G_384.contains(p_sigma4)}")

# Orbits and center
center_384 = G_384.center()
pr(f"\n|Z(G_384)| = {center_384.order()}")

derived_384 = G_384.derived_subgroup()
pr(f"|[G_384, G_384]| = {derived_384.order()}")
pr(f"|G_384/[G_384,G_384]| = {G_384.order() // derived_384.order()}")

# Orbit-level action
pr(f"\nAction of S₃ pair-permutations on T-orbits:")
swap_OM_orbit_perm = []
for i, orb in enumerate(t_orbits_sorted):
    images = frozenset(perm_swap_OM[h] for h in orb)
    for j, orb2 in enumerate(t_orbits_sorted):
        if images == frozenset(orb2):
            swap_OM_orbit_perm.append(j)
            break
pr(f"  swap_OM on orbits: {swap_OM_orbit_perm}")

cycle_OMI_orbit_perm = []
for i, orb in enumerate(t_orbits_sorted):
    images = frozenset(perm_cycle_OMI[h] for h in orb)
    for j, orb2 in enumerate(t_orbits_sorted):
        if images == frozenset(orb2):
            cycle_OMI_orbit_perm.append(j)
            break
pr(f"  cycle_OMI on orbits: {cycle_OMI_orbit_perm}")

# Build quotient group on 8 T-orbits from all generators
swap_L1L6_orbit_perm = []
for i, orb in enumerate(t_orbits_sorted):
    images = frozenset(perm_swap_L1L6[h] for h in orb)
    for j, orb2 in enumerate(t_orbits_sorted):
        if images == frozenset(orb2):
            swap_L1L6_orbit_perm.append(j)
            break
pr(f"  swap_L1L6 on orbits: {swap_L1L6_orbit_perm}")

pr(f"\n  Residual-level interpretation:")
for i, orb in enumerate(t_orbits_sorted):
    res = mirror_residual(min(orb))
    pr(f"    Orbit {i}: residual {format(res, '03b')}")

# Build quotient group
p_swOM_orb = Permutation(swap_OM_orbit_perm)
p_cyOMI_orb = Permutation(cycle_OMI_orbit_perm)
p_swL1L6_orb = Permutation(swap_L1L6_orbit_perm)

G_quotient_384 = PermutationGroup(p_swOM_orb, p_cyOMI_orb, p_swL1L6_orb)
pr(f"\n  Quotient group (G_384 on 8 T-orbits):")
pr(f"  |G_quotient| = {G_quotient_384.order()}")
pr(f"  Is it S₃? {G_quotient_384.order() == 6 and not G_quotient_384.is_abelian}")


# ═══════════════════════════════════════════════════════════════════════════
# PART 7: The 4 macro-orbits under G_384
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 7: Macro-orbits under G_384 (expected: 4 orbits)")
pr("=" * 72)

macro_orbits = G_384.orbits()
macro_orbits_sorted = sorted(macro_orbits, key=lambda o: (len(o), min(o)))
pr(f"\nOrbits of G_384: {len(macro_orbits_sorted)}")
pr(f"Orbit sizes: {sorted([len(o) for o in macro_orbits_sorted])}")

for i, orb in enumerate(macro_orbits_sorted):
    orb_sorted = sorted(orb)
    weights = sorted(set(bin(h).count('1') for h in orb))
    pr(f"\n  Macro-orbit {i} (size {len(orb)}):")
    pr(f"    Elements: {orb_sorted}")
    pr(f"    Binary: {', '.join(to_bin(h) for h in orb_sorted)}")
    pr(f"    Yang count range: {weights}")

    # Classify palindromes/anti-palindromes
    n_pal = sum(1 for h in orb if perm_sigma2[h] == h)
    n_antipal = sum(1 for h in orb if h ^ 63 == perm_sigma2[h])  # σ₃ fixed
    pr(f"    Palindromes: {n_pal}, Anti-palindromes: {n_antipal}")

    # Residuals present
    residuals = sorted(set(mirror_residual(h) for h in orb))
    pr(f"    Residuals: {[format(r,'03b') for r in residuals]}")

# How do T-orbits distribute across macro-orbits?
pr(f"\nT-orbit → macro-orbit mapping:")
for i, t_orb in enumerate(t_orbits_sorted):
    rep = min(t_orb)
    for j, m_orb in enumerate(macro_orbits_sorted):
        if rep in m_orb:
            res = mirror_residual(rep)
            pr(f"  T-orbit {i} (res={format(res,'03b')}) → macro-orbit {j} (size {len(m_orb)})")
            break


# ═══════════════════════════════════════════════════════════════════════════
# PART 8: Summary & Comparison with n=3
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("PART 8: Summary & Cross-Scale Comparison")
pr("=" * 72)

pr(f"""
=== Group hierarchy at n=6 ===

  T = ⟨O, M, I⟩ ≅ Z₂³           |T| = {T.order()}
    Acts by XOR on mirror pairs
    8 orbits of size 8 (free action)
    Orbits indexed by residual (L1⊕L6, L2⊕L5, L3⊕L4) ∈ Z₂³

  G_ext = ⟨T, σ₂⟩ ≅ Z₂⁴          |G_ext| = {G_ext.order()}
    σ₂ commutes with T (direct product)
    σ₂ fixes all T-orbits → trivial quotient action

  G_full = ⟨T, σ₂, σ₄⟩            |G_full| = {G_full.order()}
    σ₄ normalizes T, permuting O↔I
    σ₄ acts nontrivially on T-orbits

  G_384 = full mirror-pair group    |G_384| = {G_384.order()}
    = (Z₂ ≀ S₃) × Z₂³
    Adds S₃ pair-permutations + within-pair swaps
    {len(macro_orbits_sorted)} macro-orbits (sizes {sorted([len(o) for o in macro_orbits_sorted])})

=== Structural parallel with n=3 ===

  n=3: Z₂³ acting on itself (8 trigrams) = regular representation
    - 1 orbit (the whole set)
    - The 3 masks ι₁, ι₂, ι₃ ARE the generators of Z₂³
    - Block system: 4 blocks of 2 → S₄ action
    - S₄ came from the CHOICE of masks + additional structure

  n=6: Z₂³ (via mirror-pair masks) acting on Z₂⁶
    - T = ⟨O,M,I⟩ ≅ Z₂³ as a SUBGROUP of Z₂⁶ (index 8)
    - 8 orbits of size 8 (cosets Z₂⁶/T)
    - The 8 cosets ARE a copy of Z₂³ (indexed by residual)
    - The residual (L1⊕L6, L2⊕L5, L3⊕L4) is the trigram-level signature
    - S₃ pair permutations act on residuals, merging T-orbits into macro-orbits

  Bridge: The quotient Z₂⁶/⟨O,M,I⟩ ≅ Z₂³ IS the trigram-signature space.
    Each hexagram maps to a 3-bit "signature" = its mirror-pair residual.
    The mirror-pair translation group erases the distinction between
    hexagrams that differ only in mirror-pair values.
    The S₃ pair permutations then act on this Z₂³ quotient.
""")

# ── Save raw output ────────────────────────────────────────────────────────

output_path = "memories/iching/spaceprobe/q3/round2_raw_output.txt"
with open(output_path, 'w') as f:
    f.write(out.getvalue())

print(f"\nRaw output saved to {output_path}")
print(f"Formatted results in memories/iching/spaceprobe/q3/round2_results.md")
