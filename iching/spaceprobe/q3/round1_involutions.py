"""
Q3 Round 1: Hexagram Involution Structure
==========================================

Analyzes three involutions on the 64 hexagrams (6-bit strings):
  σ₁ (complement): h → h XOR 63
  σ₂ (reversal):   h → reverse bit string
  σ₃ (comp∘rev):   h → complement(reversal(h))

Bit convention:
  L1 = MSB = bit 5  (bottom line of hexagram)
  L6 = LSB = bit 0  (top line of hexagram)

  So hexagram integer = L1*32 + L2*16 + L3*8 + L4*4 + L5*2 + L6*1

  reversal(h) reverses L1↔L6, L2↔L5, L3↔L4, i.e. reverses the 6-bit string.
"""

import sys
from io import StringIO
from sympy.combinatorics import Permutation, PermutationGroup

N = 64
BITS = 6
ALL_ONES = (1 << BITS) - 1  # 63


# ── Operations ──────────────────────────────────────────────────────────────

def complement(h):
    """σ₁: flip all bits."""
    return h ^ ALL_ONES

def reverse_bits(h):
    """σ₂: reverse the 6-bit string (L1↔L6, L2↔L5, L3↔L4)."""
    result = 0
    for i in range(BITS):
        if h & (1 << i):
            result |= 1 << (BITS - 1 - i)
    return result

def comp_rev(h):
    """σ₃ = σ₁∘σ₂: complement of reversal."""
    return complement(reverse_bits(h))

def to_bin(h):
    """6-bit binary string representation."""
    return format(h, '06b')


# ── Build permutations as lists ─────────────────────────────────────────────

sigma1 = [complement(h) for h in range(N)]
sigma2 = [reverse_bits(h) for h in range(N)]
sigma3 = [comp_rev(h) for h in range(N)]

# Verify σ₃ = σ₁∘σ₂ (apply σ₂ first, then σ₁)
sigma1_of_sigma2 = [sigma1[sigma2[h]] for h in range(N)]
sigma2_of_sigma1 = [sigma2[sigma1[h]] for h in range(N)]


# ── Helpers ─────────────────────────────────────────────────────────────────

def fixed_points(perm):
    return [h for h in range(N) if perm[h] == h]

def two_cycles(perm):
    """Unordered pairs {h, σ(h)} where h ≠ σ(h), each pair listed once."""
    pairs = set()
    for h in range(N):
        if perm[h] != h:
            pairs.add(frozenset((h, perm[h])))
    return pairs

def cycle_structure(perm):
    """Return dict: cycle_length → count."""
    visited = [False] * N
    structure = {}
    for start in range(N):
        if visited[start]:
            continue
        length = 0
        h = start
        while not visited[h]:
            visited[h] = True
            h = perm[h]
            length += 1
        structure[length] = structure.get(length, 0) + 1
    return structure

def perm_order(perm):
    """Smallest k where perm^k = identity."""
    current = list(perm)
    for k in range(1, N + 1):
        if all(current[i] == i for i in range(N)):
            return k
        current = [perm[current[i]] for i in range(N)]
    return None  # shouldn't happen for small groups


# ── Output capture ──────────────────────────────────────────────────────────

out = StringIO()

def pr(*args, **kwargs):
    print(*args, **kwargs)
    print(*args, **kwargs, file=out)


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 1: Fixed points and cycle structure
# ═══════════════════════════════════════════════════════════════════════════

pr("=" * 72)
pr("SECTION 1: Fixed Points and Cycle Structure")
pr("=" * 72)

for name, perm in [("σ₁ (complement)", sigma1),
                    ("σ₂ (reversal)", sigma2),
                    ("σ₃ (comp∘rev)", sigma3)]:
    fp = fixed_points(perm)
    pairs = two_cycles(perm)
    cs = cycle_structure(perm)

    pr(f"\n{name}:")
    pr(f"  Order: {perm_order(perm)}")
    pr(f"  Cycle structure: {dict(sorted(cs.items()))}")
    pr(f"  Fixed points: {len(fp)}")
    if fp:
        pr(f"    {', '.join(f'{h}={to_bin(h)}' for h in fp)}")
    else:
        pr(f"    (none)")
    pr(f"  2-cycles: {len(pairs)}")
    pr(f"  Verify: {len(fp)} + 2×{len(pairs)} = {len(fp) + 2*len(pairs)}"
       f" {'✓' if len(fp) + 2*len(pairs) == 64 else '✗'}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 2: Pair-set overlaps
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("SECTION 2: Pair-Set Overlaps")
pr("=" * 72)

pairs1 = two_cycles(sigma1)
pairs2 = two_cycles(sigma2)
pairs3 = two_cycles(sigma3)

for (name_a, pa), (name_b, pb) in [
    (("σ₁", pairs1), ("σ₂", pairs2)),
    (("σ₁", pairs1), ("σ₃", pairs3)),
    (("σ₂", pairs2), ("σ₃", pairs3)),
]:
    shared = pa & pb
    pr(f"\n|pairs({name_a}) ∩ pairs({name_b})| = {len(shared)}")
    if shared:
        for pair in sorted(shared, key=lambda p: min(p)):
            a, b = sorted(pair)
            pr(f"  {{{a}={to_bin(a)}, {b}={to_bin(b)}}}")
    else:
        pr("  (no shared pairs)")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 3: Products and Composition Orders
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("SECTION 3: Products and Composition Orders")
pr("=" * 72)

pr(f"\nσ₁∘σ₂ == σ₃? {sigma1_of_sigma2 == sigma3}")
pr(f"σ₂∘σ₁ == σ₃? {sigma2_of_sigma1 == sigma3}")
pr(f"σ₁∘σ₂ == σ₂∘σ₁ (commute)? {sigma1_of_sigma2 == sigma2_of_sigma1}")

products = {
    "σ₁∘σ₂": sigma1_of_sigma2,
    "σ₁∘σ₃": [sigma1[sigma3[h]] for h in range(N)],
    "σ₂∘σ₃": [sigma2[sigma3[h]] for h in range(N)],
}

for name, perm in products.items():
    cs = cycle_structure(perm)
    order = perm_order(perm)
    pr(f"\n{name}:")
    pr(f"  Order: {order}")
    pr(f"  Cycle structure: {dict(sorted(cs.items()))}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 4: Generated Group G = ⟨σ₁, σ₂⟩
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("SECTION 4: Generated Group G = ⟨σ₁, σ₂⟩")
pr("=" * 72)

# Build sympy Permutation objects
p_sigma1 = Permutation(sigma1)
p_sigma2 = Permutation(sigma2)
p_sigma3 = Permutation(sigma3)

G = PermutationGroup(p_sigma1, p_sigma2)

pr(f"\n|G| = {G.order()}")
pr(f"G is abelian: {G.is_abelian}")
pr(f"G is solvable: {G.is_solvable}")
pr(f"G is nilpotent: {G.is_nilpotent}")

# Generators info
pr(f"\nGenerator orders:")
pr(f"  σ₁ order: {p_sigma1.order()}")
pr(f"  σ₂ order: {p_sigma2.order()}")
pr(f"  σ₃ order: {p_sigma3.order()}")

# Center
center = G.center()
pr(f"\nCenter Z(G):")
pr(f"  |Z(G)| = {center.order()}")
if center.order() <= 16:
    pr(f"  Elements: {[list(g.array_form) for g in center.elements]}")

# Derived subgroup
derived = G.derived_subgroup()
pr(f"\nDerived subgroup [G,G]:")
pr(f"  |[G,G]| = {derived.order()}")

pr(f"\nAbelianization G/[G,G]:")
pr(f"  |G/[G,G]| = {G.order() // derived.order()}")

# Enumerate all elements if tractable
g_order = G.order()
if g_order <= 64:
    pr(f"\nAll {g_order} elements of G (as permutations):")
    elements = list(G.elements)
    for i, elem in enumerate(sorted(elements, key=lambda p: p.order())):
        cs = {}
        for cycle in elem.cyclic_form:
            l = len(cycle)
            cs[l] = cs.get(l, 0) + 1
        # Count fixed points
        moved = sum(len(c) for c in elem.cyclic_form)
        fp_count = N - moved
        if fp_count > 0:
            cs[1] = fp_count
        pr(f"  g{i}: order={elem.order()}, cycle type={dict(sorted(cs.items()))}")

    # Check known small group isomorphisms
    pr(f"\nGroup identification:")
    if g_order == 4:
        if G.is_abelian:
            # Z₄ or Z₂×Z₂ (Klein four)?
            orders = sorted([g.order() for g in elements])
            if max(orders) == 2:
                pr(f"  G ≅ Z₂ × Z₂ (Klein four-group V₄)")
            else:
                pr(f"  G ≅ Z₄")
        else:
            pr(f"  G is non-abelian of order 4 (impossible)")
    elif g_order == 2:
        pr(f"  G ≅ Z₂")
    elif g_order == 1:
        pr(f"  G ≅ {{e}} (trivial)")
    elif g_order == 8:
        if G.is_abelian:
            pr(f"  G is abelian of order 8")
            orders = sorted([g.order() for g in elements])
            pr(f"  Element orders: {orders}")
        else:
            pr(f"  G is non-abelian of order 8 (D₄ or Q₈)")
    elif g_order == 6:
        if G.is_abelian:
            pr(f"  G ≅ Z₆")
        else:
            pr(f"  G ≅ S₃")
    else:
        pr(f"  Order {g_order} — check structure manually")
        orders = sorted([g.order() for g in elements])
        pr(f"  Element orders: {orders}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 5: Block Systems and Subgroup Lattice
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("SECTION 5: Block Systems and Subgroup Lattice")
pr("=" * 72)

# Orbits first
orbits = G.orbits()
pr(f"\nOrbits of G on {{0,...,63}}: {len(orbits)} orbits")
orbit_sizes = sorted([len(o) for o in orbits], reverse=True)
pr(f"Orbit sizes: {orbit_sizes}")

# G ≅ V₄ = Z₂×Z₂ has exactly 3 proper nontrivial subgroups, each ≅ Z₂
# These are ⟨σ₁⟩, ⟨σ₂⟩, ⟨σ₃⟩
pr(f"\nSubgroup lattice of V₄:")
pr(f"  {{e}} < ⟨σ₁⟩ ≅ Z₂")
pr(f"  {{e}} < ⟨σ₂⟩ ≅ Z₂")
pr(f"  {{e}} < ⟨σ₃⟩ ≅ Z₂")
pr(f"  All three < G ≅ V₄")

# Each Z₂ subgroup partitions {0..63} into its own orbit structure
# These give natural "block-like" decompositions
pr(f"\nOrbit decompositions by subgroup:")

for name, perm in [("⟨σ₁⟩ (complement)", sigma1),
                    ("⟨σ₂⟩ (reversal)", sigma2),
                    ("⟨σ₃⟩ (comp∘rev)", sigma3)]:
    # Orbits of this Z₂ subgroup
    visited = [False] * N
    sub_orbits = []
    for h in range(N):
        if visited[h]:
            continue
        orb = {h}
        visited[h] = True
        img = perm[h]
        if not visited[img]:
            orb.add(img)
            visited[img] = True
        sub_orbits.append(sorted(orb))

    sizes = sorted([len(o) for o in sub_orbits], reverse=True)
    pr(f"\n  {name}:")
    pr(f"    Orbits: {len(sub_orbits)} (sizes: {len([s for s in sizes if s==2])} pairs + {len([s for s in sizes if s==1])} fixed)")

# The G-orbits are intersections of the three Z₂ orbit structures
# Size-4 orbits: h is in no fixed-point set
# Size-2 orbits: h is fixed by exactly one of σ₂, σ₃ (can't be fixed by σ₁)
pr(f"\nOrbit size analysis:")
fp2 = set(fixed_points(sigma2))
fp3 = set(fixed_points(sigma3))

size2_orbits = [sorted(o) for o in orbits if len(o) == 2]
size4_orbits = [sorted(o) for o in orbits if len(o) == 4]

pr(f"  Size-2 orbits ({len(size2_orbits)}):")
for orb in sorted(size2_orbits, key=lambda o: o[0]):
    h = orb[0]
    in_fp2 = h in fp2
    in_fp3 = h in fp3
    pr(f"    {{{', '.join(f'{x}={to_bin(x)}' for x in orb)}}}"
       f"  — fixed by: {'σ₂' if in_fp2 else ''}{'σ₃' if in_fp3 else ''}")

pr(f"\n  Size-4 orbits ({len(size4_orbits)}):")
for orb in sorted(size4_orbits, key=lambda o: o[0]):
    # Show the orbit structure: which element maps to which under each σ
    h = orb[0]
    pr(f"    {{{', '.join(f'{x}={to_bin(x)}' for x in orb)}}}")

# Partition of orbits by stabilizer type
pr(f"\nStabilizer analysis:")
pr(f"  Size-2 orbits have stabilizer ≅ Z₂ (index 2 in V₄)")
pr(f"  Size-4 orbits have trivial stabilizer (free V₄ action)")
pr(f"  Check: 8×2 + 12×4 = {8*2 + 12*4}")

# Relationship to complement pairs
pr(f"\nComplement pairs and reversal pairs:")
pr(f"  σ₁ produces 32 complement pairs (always, no fixed points)")
pr(f"  σ₂ produces 28 reversal pairs + 8 palindromes")
pr(f"  The 8 size-2 orbits ARE the 8 complement pairs whose elements")
pr(f"  are individually fixed by σ₂ or σ₃:")
for orb in sorted(size2_orbits, key=lambda o: o[0]):
    a, b = orb
    is_palindrome_a = sigma2[a] == a
    is_palindrome_b = sigma2[b] == b
    is_antipal_a = sigma3[a] == a
    is_antipal_b = sigma3[b] == b
    pr(f"    {{{a}={to_bin(a)}, {b}={to_bin(b)}}}: "
       f"{'both palindromes' if is_palindrome_a and is_palindrome_b else ''}"
       f"{'both anti-palindromes' if is_antipal_a and is_antipal_b else ''}"
       f"{'mixed' if (is_palindrome_a != is_palindrome_b) else ''}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 6: Orbit Structure (detailed)
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("SECTION 6: Orbit Structure (Detailed)")
pr("=" * 72)

pr(f"\nTotal orbits: {len(orbits)}")
pr(f"Orbit size distribution: {dict(sorted(((s, orbit_sizes.count(s)) for s in set(orbit_sizes)), reverse=True))}")

for i, orbit in enumerate(sorted(orbits, key=lambda o: (len(o), min(o)))):
    orbit_sorted = sorted(orbit)
    binary_reps = [to_bin(h) for h in orbit_sorted]

    pr(f"\nOrbit {i+1} (size {len(orbit_sorted)}):")
    pr(f"  Elements: {', '.join(f'{h}({to_bin(h)})' for h in orbit_sorted)}")

    # What does each generator do within this orbit?
    pr(f"  σ₁ action: {', '.join(f'{h}→{sigma1[h]}' for h in orbit_sorted)}")
    pr(f"  σ₂ action: {', '.join(f'{h}→{sigma2[h]}' for h in orbit_sorted)}")

    # Characterize: are elements related by complement, reversal, or both?
    # Check hamming weights
    weights = [bin(h).count('1') for h in orbit_sorted]
    pr(f"  Yang counts: {weights}")


# ═══════════════════════════════════════════════════════════════════════════
# SECTION 7: Summary
# ═══════════════════════════════════════════════════════════════════════════

pr("\n" + "=" * 72)
pr("SECTION 7: Summary")
pr("=" * 72)

pr(f"""
Key findings:
- σ₁ (complement): order {p_sigma1.order()}, {len(fixed_points(sigma1))} fixed points, {len(two_cycles(sigma1))} pairs
- σ₂ (reversal):   order {p_sigma2.order()}, {len(fixed_points(sigma2))} fixed points, {len(two_cycles(sigma2))} pairs
- σ₃ (comp∘rev):   order {p_sigma3.order()}, {len(fixed_points(sigma3))} fixed points, {len(two_cycles(sigma3))} pairs
- σ₁ and σ₂ commute: {sigma1_of_sigma2 == sigma2_of_sigma1}
- G = ⟨σ₁, σ₂⟩ has order {G.order()}, abelian: {G.is_abelian}
- Number of orbits: {len(orbits)}
- Orbit sizes: {orbit_sizes}
""")


# ── Save raw output ─────────────────────────────────────────────────────────

output_path = "memories/iching/spaceprobe/q3/round1_raw_output.txt"
with open(output_path, 'w') as f:
    f.write(out.getvalue())

print(f"\nRaw output saved to {output_path}")
print(f"Formatted results in memories/iching/spaceprobe/q3/round1_results.md")
