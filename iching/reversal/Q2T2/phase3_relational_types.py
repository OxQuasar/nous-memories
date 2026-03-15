#!/usr/bin/env python3
"""Phase 3: Algebraic type of each culture's relational structure.

Computes:
- Chinese 五行: dual Hamiltonian cycles on Z₅, automorphism group
- Indian Mahābhūta: chain poset on 5 elements
- Greek 4 elements: quality-square on F₂²
- Ifá: group structure on F₂⁴
"""

from itertools import permutations
from collections import Counter
from math import factorial


# ═══════════════════════════════════════════════════════
# Hamiltonian cycle enumeration on complete directed graph K_n
# ═══════════════════════════════════════════════════════

def enumerate_hamiltonian_cycles(n):
    """All directed Hamiltonian cycles on n vertices {0,...,n-1}.

    A directed Hamiltonian cycle visits every vertex exactly once
    and returns to start. Fix vertex 0 as start to avoid rotational
    duplicates. Then enumerate all permutations of {1,...,n-1}.
    Each gives a directed cycle 0 → perm[0] → perm[1] → ... → 0.

    Returns list of cycles as tuples of edges (stride sequences).
    """
    others = list(range(1, n))
    cycles = []
    for perm in permutations(others):
        cycle = (0,) + perm  # vertices in order
        # Represent as stride sequence: step[i] = (cycle[i+1] - cycle[i]) mod n
        strides = tuple((cycle[(i+1) % n] - cycle[i]) % n for i in range(n))
        cycles.append((cycle, strides))
    return cycles


def directed_to_undirected(cycles):
    """Group directed cycles into unordered pairs {C, C⁻¹}.
    Two cycles are reverses if one's stride sequence reversed and negated (mod n) gives the other."""
    n = len(cycles[0][1])
    seen = set()
    independent = []
    for cycle, strides in cycles:
        # Canonical: min of (strides, reverse_strides)
        # Reverse cycle: traverse backwards → strides become (-s_{n-1}, -s_{n-2}, ..., -s_0) mod n
        # But we also need to account for starting point rotation.
        # Actually, since we fixed start=0, the reverse of 0→a→b→...→0
        # is 0→...→b→a→0, which starting from 0 is a different permutation.
        # Simplest: use the edge set as canonical form.
        edges = frozenset((cycle[i], cycle[(i+1) % n]) for i in range(n))
        rev_edges = frozenset((cycle[(i+1) % n], cycle[i]) for i in range(n))
        if edges not in seen:
            seen.add(edges)
            seen.add(rev_edges)
            independent.append((cycle, strides))
    return independent


def is_constant_stride(strides, n):
    """Check if all strides are the same value mod n."""
    return len(set(strides)) == 1


# ═══════════════════════════════════════════════════════
# Chinese 五行 (Wuxing)
# ═══════════════════════════════════════════════════════

def analyze_wuxing():
    print("=" * 70)
    print("CHINESE 五行 (Wuxing) — Z₅ with dual cycles")
    print("=" * 70)

    n = 5
    elements = {0: "Wood", 1: "Fire", 2: "Earth", 3: "Metal", 4: "Water"}

    # 生 cycle: stride +1 (W→F→E→M→Wa→W)
    sheng = tuple(range(n))  # 0,1,2,3,4
    sheng_strides = tuple(1 for _ in range(n))
    print(f"\n  生 (generation) cycle: {' → '.join(elements[i] for i in sheng)} → {elements[0]}")
    print(f"  Stride: +1 mod 5")

    # 克 cycle: stride +2 (W→E→Wa→F→M→W = 0→2→4→1→3→0)
    ke = tuple((2 * i) % n for i in range(n))  # 0,2,4,1,3
    ke_strides = tuple(2 for _ in range(n))
    print(f"\n  克 (conquest) cycle: {' → '.join(elements[i] for i in ke)} → {elements[0]}")
    print(f"  Stride: +2 mod 5")

    # Enumerate ALL directed Hamiltonian cycles on 5 vertices
    all_cycles = enumerate_hamiltonian_cycles(n)
    print(f"\n  Total directed Hamiltonian cycles (fixed start): {len(all_cycles)}")
    # This should be (n-1)! = 24

    # Group into undirected pairs
    independent = directed_to_undirected(all_cycles)
    print(f"  Independent (up to reversal): {len(independent)}")
    # Should be 24/2 = 12

    # Classify by stride pattern
    constant_stride_cycles = [(c, s) for c, s in all_cycles if is_constant_stride(s, n)]
    print(f"\n  Constant-stride cycles:")
    for cycle, strides in constant_stride_cycles:
        stride = strides[0]
        print(f"    Stride +{stride}: {' → '.join(elements[i] for i in cycle)} → {elements[0]}")

    # Strides 1 and 4 are reverses (4 = -1 mod 5)
    # Strides 2 and 3 are reverses (3 = -2 mod 5)
    print(f"\n  Constant-stride analysis:")
    print(f"    Strides {1} and {n-1} are reverse of each other (+1 ↔ -1)")
    print(f"    Strides {2} and {n-2} are reverse of each other (+2 ↔ -2)")
    print(f"    → 2 independent constant-stride cycles: 生 (stride 1) and 克 (stride 2)")
    print(f"    → These are the ONLY Hamiltonian cycles with algebraic (constant-stride) structure")

    # Non-constant-stride cycles
    non_constant = [(c, s) for c, s in all_cycles if not is_constant_stride(s, n)]
    print(f"\n  Non-constant-stride (irregular) cycles: {len(non_constant)}")
    print(f"  These lack algebraic uniformity — they're 'accidental' Hamiltonian cycles.")

    # Automorphism group: permutations of Z₅ preserving both cycles
    print(f"\n  Automorphism group (preserving both 生 and 克):")
    print(f"    生 is stride +1, 克 is stride +2.")
    print(f"    A permutation σ preserves stride-s cycle iff σ(x+s) = σ(x)+s mod 5")
    print(f"    i.e., σ is an affine map x ↦ ax+b with a·s ≡ s mod 5 for both s=1,2")
    print(f"    a·1 ≡ 1 and a·2 ≡ 2 → a ≡ 1 → σ(x) = x+b")
    print(f"    Translations Z₅, order 5")

    # Wait — preserving the DIRECTED cycle means σ maps edges to edges.
    # If σ(x) = ax+b, then edge (x, x+s) maps to (ax+b, a(x+s)+b) = (ax+b, ax+b+as).
    # For this to be an edge of the stride-s cycle, we need as ≡ s mod 5.
    # For s=1: a ≡ 1. For s=2: 2a ≡ 2, so a ≡ 1. So Aut = {x↦x+b} ≅ Z₅.
    # But if we allow reversal of ONE cycle, we get more.

    # Actually the question is about preserving both cycles SIMULTANEOUSLY.
    # As undirected: stride-1 undirected = stride-{1,4}, stride-2 undirected = stride-{2,3}.
    # σ preserves undirected stride-1 cycle: a·1 ∈ {1,4} mod 5, so a ∈ {1,4}.
    # σ preserves undirected stride-2 cycle: a·2 ∈ {2,3} mod 5, so 2a ∈ {2,3}, a ∈ {1,4}.
    # So a ∈ {1,4}, b ∈ Z₅. |Aut| = 2 × 5 = 10 (dihedral of the pentagon).

    # But for DIRECTED cycles: a must satisfy a·1 ≡ 1, so a=1. |Aut| = 5.
    # For directed-or-reverse: a ∈ {1,4}. With a=4: 生↦生⁻¹ and 克↦克⁻¹. |Aut| = 10.

    print(f"    As DIRECTED cycles: |Aut| = 5 (translations)")
    print(f"    As UNDIRECTED cycles: |Aut| = 10 (dihedral group of pentagon)")

    return {
        'elements': 5,
        'substrate': 'Z₅',
        'total_directed_ham': len(all_cycles),
        'independent_ham': len(independent),
        'constant_stride': len(constant_stride_cycles),
        'independent_constant_stride': 2,
        'aut_directed': 5,
        'aut_undirected': 10,
        'relational_type': 'Dual Hamiltonian cycles (生/克) on Z₅',
    }


# ═══════════════════════════════════════════════════════
# Indian Mahābhūta
# ═══════════════════════════════════════════════════════

def analyze_mahabhuta():
    print(f"\n{'='*70}")
    print("INDIAN MAHĀBHŪTA — Linear order on 5 elements")
    print("=" * 70)

    elements = {1: "Ākāśa", 2: "Vāyu", 3: "Agni", 4: "Āpas", 5: "Pṛthvī"}

    print(f"\n  Emanation order: {' > '.join(elements[i] for i in range(1, 6))}")
    print(f"  Structure: total order (chain poset P₅)")
    print(f"  No cyclic structure — emanation is a directed path, not a cycle")

    # Automorphism of a total order: only identity
    print(f"\n  Automorphism group:")
    print(f"    A permutation preserving a total order must be the identity.")
    print(f"    |Aut(P₅)| = 1")

    # Hamiltonian cycles
    print(f"\n  Hamiltonian cycles: 0")
    print(f"    A chain poset has a single Hamiltonian PATH but no cycle.")
    print(f"    The path is the order itself: 1→2→3→4→5.")
    print(f"    To close it as a cycle would need edge 5→1, which doesn't exist.")

    return {
        'elements': 5,
        'substrate': 'P₅ (chain poset)',
        'total_directed_ham': 0,
        'independent_ham': 0,
        'constant_stride': 0,
        'independent_constant_stride': 0,
        'aut_directed': 1,
        'aut_undirected': 1,
        'relational_type': 'Total order (chain poset)',
    }


# ═══════════════════════════════════════════════════════
# Greek 4 Elements (Aristotle)
# ═══════════════════════════════════════════════════════

def analyze_greek():
    print(f"\n{'='*70}")
    print("GREEK 4 ELEMENTS (Aristotle) — Quality square on F₂²")
    print("=" * 70)

    # Encode as F₂²: bit 1 = hot(1)/cold(0), bit 0 = dry(1)/wet(0)
    elements = {
        0b11: "Fire  (H,D)",
        0b10: "Air   (H,W)",
        0b00: "Water (C,W)",
        0b01: "Earth (C,D)",
    }

    print(f"\n  Encoding (hot/cold × dry/wet):")
    for v, name in sorted(elements.items()):
        print(f"    {v:02b} = {name}")

    # Transformation cycle: change one quality at a time
    # Fire(11) → Air(10) → Water(00) → Earth(01) → Fire(11)
    cycle = [0b11, 0b10, 0b00, 0b01]
    print(f"\n  Transformation cycle: {' → '.join(elements[v] for v in cycle)} → {elements[cycle[0]]}")
    print(f"  Each step changes exactly one quality (Hamming distance 1)")

    # Verify Hamming distance 1 between consecutive
    for i in range(4):
        d = bin(cycle[i] ^ cycle[(i+1) % 4]).count('1')
        print(f"    {elements[cycle[i]]} → {elements[cycle[(i+1)%4]]}: Hamming distance = {d}")

    # Enumerate ALL directed Hamiltonian cycles on 4 vertices
    n = 4
    all_cycles = enumerate_hamiltonian_cycles(n)
    print(f"\n  Total directed Hamiltonian cycles on {n} vertices (fixed start): {len(all_cycles)}")
    # (n-1)! = 6

    independent = directed_to_undirected(all_cycles)
    print(f"  Independent (up to reversal): {len(independent)}")
    # 6/2 = 3

    # List them
    labels = {0: "F", 1: "A", 2: "W", 3: "E"}  # Using Aristotle's square
    for i, (cycle_v, strides) in enumerate(all_cycles):
        print(f"    Directed cycle {i+1}: {' → '.join(str(v) for v in cycle_v)} → 0  strides={strides}")

    # Which are the Hamming-distance-1 cycles on F₂²?
    # On F₂², the Hamming-distance-1 graph is the 4-cycle (square):
    # 00-01-11-10-00 and its reverse
    print(f"\n  Hamming-distance-1 cycles on F₂²:")
    ham1_cycles = []
    for cycle_v, strides in all_cycles:
        is_ham1 = all(bin(cycle_v[i] ^ cycle_v[(i+1)%n]).count('1') == 1 for i in range(n))
        if is_ham1:
            ham1_cycles.append((cycle_v, strides))
            print(f"    {' → '.join(f'{v:02b}' for v in cycle_v)} → {cycle_v[0]:02b}")
    print(f"  Count: {len(ham1_cycles)} directed ({len(ham1_cycles)//2} undirected)")

    # Automorphism group of the square (4-cycle graph)
    print(f"\n  Automorphism group:")
    print(f"    The directed 4-cycle (as a directed graph): Aut = Z₄ (rotations)")
    print(f"    The undirected 4-cycle (square): Aut = D₄ (dihedral), |D₄| = 8")
    print(f"    As Aristotle's quality square (F₂² structure): Aut ≅ Z₂ × Z₂")
    print(f"    (flip hot/cold and/or flip dry/wet independently)")

    return {
        'elements': 4,
        'substrate': 'F₂² (quality square)',
        'total_directed_ham': len(all_cycles),
        'independent_ham': len(independent),
        'constant_stride': 0,  # Not cyclic group, N/A
        'independent_constant_stride': 0,
        'aut_directed': 4,
        'aut_undirected': 8,
        'relational_type': 'Single Hamiltonian cycle on F₂² (quality adjacency)',
    }


# ═══════════════════════════════════════════════════════
# Ifá (F₂⁴ group structure)
# ═══════════════════════════════════════════════════════

def analyze_ifa():
    print(f"\n{'='*70}")
    print("IFÁ — F₂⁴ with group structure and seniority ordering")
    print("=" * 70)

    n = 4
    N = 1 << n

    print(f"\n  |F₂⁴| = {N} elements")
    print(f"  Group operation: XOR (bitwise addition mod 2)")
    print(f"  Automorphism group of (F₂⁴, +): GL(4, F₂)")

    # GL(4,F₂) order
    gl_order = 1
    for i in range(4):
        gl_order *= (2**4 - 2**i)
    print(f"  |GL(4, F₂)| = {gl_order}")

    print(f"\n  Relational structure: SENIORITY ORDERING ONLY")
    print(f"    No surjection to a codomain (no 生/克-type dynamics)")
    print(f"    No quality-based adjacency (no Aristotelian square)")
    print(f"    The 16 odù are ordered by cultural/divinatory significance")

    print(f"\n  Structural comparison:")
    print(f"    China: F₂³ → Z₅ (binary → pentadic, with two cycles)")
    print(f"    Ifá:   F₂⁴ → ∅  (binary only, no codomain)")
    print(f"    Ifá discovered the DOMAIN (binary encoding) but not the CODOMAIN (cyclic structure)")

    # Hamiltonian cycles on F₂⁴ as a graph? Not meaningful without a relation.
    print(f"\n  Hamiltonian cycles: N/A")
    print(f"    F₂⁴ as a group has no canonical directed graph structure.")
    print(f"    The Cayley graph depends on generator choice.")

    return {
        'elements': 16,
        'substrate': 'F₂⁴ (vector space)',
        'total_directed_ham': 'N/A',
        'independent_ham': 'N/A',
        'constant_stride': 'N/A',
        'independent_constant_stride': 'N/A',
        'aut_directed': gl_order,
        'aut_undirected': gl_order,
        'relational_type': 'Seniority ordering (no cyclic dynamics)',
    }


# ═══════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════

def print_summary(results):
    print(f"\n\n{'='*70}")
    print("CROSS-CULTURAL COMPARISON TABLE")
    print(f"{'='*70}")

    headers = ["System", "|Elem|", "Substrate", "Dir Ham", "Indep Ham",
               "|Aut(rel)|", "Relational Type"]
    widths = [12, 7, 18, 9, 10, 12, 45]

    header_line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
    print(f"\n  {header_line}")
    print(f"  {'─'*sum(widths)}")

    names = ["Wuxing", "Mahābhūta", "Greek", "Ifá"]
    for name, r in zip(names, results):
        row = [
            name,
            str(r['elements']),
            r['substrate'],
            str(r['total_directed_ham']),
            str(r['independent_ham']),
            str(r['aut_directed']),
            r['relational_type'],
        ]
        print(f"  {'  '.join(v.ljust(w) for v, w in zip(row, widths))}")

    print(f"\n  Key observations:")
    print(f"    1. Only Wuxing has DUAL independent cycles (生 and 克)")
    print(f"    2. Greek system has a SINGLE cycle (quality adjacency)")
    print(f"    3. Indian system is ACYCLIC (pure emanation hierarchy)")
    print(f"    4. Ifá has the largest domain but NO codomain dynamics")
    print(f"    5. Binary encoding appears in ≥2 traditions (I Ching, Ifá)")
    print(f"    6. Five-fold classification appears in 3 traditions (China, India, Greece+1)")
    print(f"       but with fundamentally different algebraic structures")

    # Deeper analysis: what makes Wuxing unique
    print(f"\n  What makes 五行 algebraically unique:")
    print(f"    - The ONLY system where the relational structure is a PAIR of")
    print(f"      Hamiltonian cycles with constant stride on a cyclic group")
    print(f"    - Strides 1 and 2 are the only generators of Z₅* acting on Z₅")
    print(f"    - This gives 生 and 克 independent algebraic meaning:")
    print(f"      生 = addition by generator, 克 = addition by the other generator")
    print(f"    - On Z₅, there are exactly 2 independent constant-stride cycles")
    print(f"      (strides 1,2; with 3,4 being their reverses)")
    print(f"    - The dual-cycle structure is therefore MAXIMAL for p=5")


if __name__ == '__main__':
    print("Phase 3: Cross-Cultural Relational Structure Types")
    print("=" * 70)

    r_wuxing = analyze_wuxing()
    r_mahabhuta = analyze_mahabhuta()
    r_greek = analyze_greek()
    r_ifa = analyze_ifa()

    print_summary([r_wuxing, r_mahabhuta, r_greek, r_ifa])
