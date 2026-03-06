#!/usr/bin/env python3
"""
Choice point 1: Alternative generating decompositions of the traditional S₄.

Questions:
1. What are all minimal generating sets of this S₄?
2. Can 2 FPF involutions generate S₄, or is 3 the minimum?
3. What 2-element generating sets exist, by cycle type?
"""

from itertools import combinations
from collections import Counter

# ═══════════════════════════════════════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════════════════════════════════════

def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))

def perm_order(p):
    x = p
    for k in range(1, len(p) + 1):
        if all(x[i] == i for i in range(len(p))):
            return k
        x = compose(p, x)
    return len(p)

def generate_group(generators, n=8):
    identity = tuple(range(n))
    group = {identity}
    frontier = set(generators)
    while frontier:
        for g in frontier:
            group.add(g)
        nf = set()
        for g in list(group):
            for gen in generators:
                for prod in [compose(g, gen), compose(gen, g)]:
                    if prod not in group:
                        nf.add(prod)
        frontier = nf
    return group

def cycle_type(p):
    """Cycle type of a permutation, as sorted tuple of cycle lengths."""
    seen = set()
    cycles = []
    for i in range(len(p)):
        if i in seen:
            continue
        length = 0
        j = i
        while j not in seen:
            seen.add(j)
            j = p[j]
            length += 1
        cycles.append(length)
    return tuple(sorted(cycles, reverse=True))

def is_fpf_involution(p):
    return all(p[i] != i and p[p[i]] == i for i in range(len(p)))

NAMES = {0: "Kun", 1: "Gen", 2: "Kan", 3: "Xun",
         4: "Zhen", 5: "Li", 6: "Dui", 7: "Qian"}

# ═══════════════════════════════════════════════════════════════════════════
# Build the traditional S₄
# ═══════════════════════════════════════════════════════════════════════════

# ι₁ (complement): x ↦ x ⊕ 111
IOTA1 = tuple(x ^ 0b111 for x in range(8))

# ι₂ (KW diameters): Kun↔Gen, Kan↔Li, Xun↔Qian, Zhen↔Dui
IOTA2 = [0] * 8
for a, b in [(0, 1), (2, 5), (3, 7), (4, 6)]:
    IOTA2[a] = b; IOTA2[b] = a
IOTA2 = tuple(IOTA2)

# ι₃ (He Tu): Kan↔Qian, Kun↔Dui, Zhen↔Gen, Xun↔Li
IOTA3 = [0] * 8
for a, b in [(2, 7), (0, 6), (4, 1), (3, 5)]:
    IOTA3[a] = b; IOTA3[b] = a
IOTA3 = tuple(IOTA3)

G = generate_group({IOTA1, IOTA2, IOTA3})
assert len(G) == 24, f"Expected S₄ (order 24), got order {len(G)}"

G_list = sorted(G)
IDENTITY = tuple(range(8))


def main():
    print("=" * 70)
    print("CHOICE POINT 1: GENERATING DECOMPOSITIONS OF THE TRADITIONAL S₄")
    print("=" * 70)

    # ───────────────────────────────────────────────────────────────────
    # Classify all 24 elements by cycle type
    # ───────────────────────────────────────────────────────────────────
    print("\n--- Element classification ---")
    type_counts = Counter()
    type_elements = {}
    for g in G_list:
        ct = cycle_type(g)
        type_counts[ct] += 1
        type_elements.setdefault(ct, []).append(g)

    print(f"{'Cycle type':>20s}  {'Count':>5s}  {'Order':>5s}  FPF?")
    print("-" * 55)
    for ct in sorted(type_counts):
        g = type_elements[ct][0]
        fpf = all(g[i] != i for i in range(8))
        print(f"  {str(ct):>20s}  {type_counts[ct]:>5d}  "
              f"{perm_order(g):>5d}  {'yes' if fpf else 'no'}")

    # Count FPF involutions in G
    fpf_in_G = [g for g in G_list if is_fpf_involution(g)]
    print(f"\nFPF involutions in G: {len(fpf_in_G)}")

    # ───────────────────────────────────────────────────────────────────
    # 2-element generating sets
    # ───────────────────────────────────────────────────────────────────
    print("\n--- 2-element generating sets ---")
    non_id = [g for g in G_list if g != IDENTITY]
    two_gen_sets = []

    for g, h in combinations(non_id, 2):
        grp = generate_group({g, h})
        if len(grp) == 24:
            two_gen_sets.append((g, h))

    print(f"Total 2-element generating sets: {len(two_gen_sets)}")

    # Classify by cycle type pair
    pair_type_counts = Counter()
    for g, h in two_gen_sets:
        key = tuple(sorted([cycle_type(g), cycle_type(h)]))
        pair_type_counts[key] += 1

    print(f"\nBy cycle type pair:")
    print(f"  {'Type pair':>40s}  {'Count':>5s}")
    print("-" * 50)
    for key in sorted(pair_type_counts):
        print(f"  {str(key):>40s}  {pair_type_counts[key]:>5d}")

    # ───────────────────────────────────────────────────────────────────
    # FPF-involution generating sets
    # ───────────────────────────────────────────────────────────────────
    print("\n--- FPF involution generating sets ---")

    # Size 2: pairs of FPF involutions generating S₄
    fpf_2gen = []
    for g, h in combinations(fpf_in_G, 2):
        grp = generate_group({g, h})
        if len(grp) == 24:
            fpf_2gen.append((g, h))

    print(f"FPF involution pairs generating S₄: {len(fpf_2gen)}")

    if fpf_2gen:
        print("  → 2 FPF involutions CAN generate S₄")
        # Show product orders for these pairs
        prod_orders = Counter()
        for g, h in fpf_2gen:
            prod_orders[perm_order(compose(g, h))] += 1
        print(f"  Product orders: {dict(sorted(prod_orders.items()))}")
    else:
        print("  → 2 FPF involutions CANNOT generate S₄; minimum is 3")

    # Size 3: triples of FPF involutions generating S₄
    fpf_3gen = []
    for triple in combinations(fpf_in_G, 3):
        grp = generate_group(set(triple))
        if len(grp) == 24:
            fpf_3gen.append(triple)

    print(f"FPF involution triples generating S₄: {len(fpf_3gen)}")

    # How many are minimal (no proper subset generates)?
    fpf_3gen_minimal = []
    for triple in fpf_3gen:
        is_minimal = True
        for pair in combinations(triple, 2):
            grp = generate_group(set(pair))
            if len(grp) == 24:
                is_minimal = False
                break
        if is_minimal:
            fpf_3gen_minimal.append(triple)

    print(f"Of those, minimal (no sub-pair generates): {len(fpf_3gen_minimal)}")

    # ───────────────────────────────────────────────────────────────────
    # All minimal generating sets (any size)
    # ───────────────────────────────────────────────────────────────────
    print("\n--- All minimal generating sets ---")

    # Size 1: single elements generating S₄?
    one_gen = [g for g in non_id if len(generate_group({g})) == 24]
    print(f"Size 1: {len(one_gen)} (impossible: max cyclic order in S₄ is 4)")

    # Size 2 minimal: already found two_gen_sets; check minimality
    # All size-2 sets are minimal by definition (size-1 can't generate)
    print(f"Size 2: {len(two_gen_sets)} (all minimal)")

    # Size 3 minimal FPF-only (already computed)
    print(f"Size 3 (FPF-only, minimal): {len(fpf_3gen_minimal)}")

    # ───────────────────────────────────────────────────────────────────
    # Traditional triple: what makes it special?
    # ───────────────────────────────────────────────────────────────────
    print("\n--- The traditional triple ---")
    print(f"ι₁ type: {cycle_type(IOTA1)}, FPF: {is_fpf_involution(IOTA1)}")
    print(f"ι₂ type: {cycle_type(IOTA2)}, FPF: {is_fpf_involution(IOTA2)}")
    print(f"ι₃ type: {cycle_type(IOTA3)}, FPF: {is_fpf_involution(IOTA3)}")

    # Check if traditional triple is among minimal FPF triples
    trad_set = frozenset([IOTA1, IOTA2, IOTA3])
    # Can any pair of the traditional triple generate?
    for name_pair, pair in [("ι₁,ι₂", (IOTA1, IOTA2)),
                             ("ι₁,ι₃", (IOTA1, IOTA3)),
                             ("ι₂,ι₃", (IOTA2, IOTA3))]:
        grp = generate_group(set(pair))
        print(f"  ⟨{name_pair}⟩ order: {len(grp)}")

    # ───────────────────────────────────────────────────────────────────
    # Summary
    # ───────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    can_2_fpf = len(fpf_2gen) > 0
    print(f"""
Element types in this S₄:
  {dict(sorted(type_counts.items()))}
  FPF involutions: {len(fpf_in_G)} of 24 elements

Generating sets:
  2-element (any type): {len(two_gen_sets)}
  2-element (both FPF): {len(fpf_2gen)}
  3-element FPF-only minimal: {len(fpf_3gen_minimal)}

Can 2 FPF involutions generate S₄? {can_2_fpf}
""")
    if can_2_fpf:
        print("""→ The "three FPF involutions" framing is NOT forced by "generate S₄
  using only FPF involutions." Two suffice. Using three is a CHOICE
  that provides extra structure (the V₄ subgroup, the overlap pattern).
  The third involution is redundant for generation but essential for
  the axiom system.""")
    else:
        print("""→ The "three FPF involutions" framing IS the minimum for generating
  S₄ from FPF involutions alone. It's forced, not chosen.""")


if __name__ == '__main__':
    main()
