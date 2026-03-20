#!/usr/bin/env python3
"""
Q₃ Edge-Coloring Orbit Structure & Inverse Approach

Analyzes how the canonical Z₅ typing of Q₃ vertices induces edge 3-colorings
(比和/生/克), and how these transform under Aut(Q₃) = S₃ ⋉ (Z₂)³.
"""

from itertools import permutations, product, combinations
from collections import defaultdict

# ── Constants ──────────────────────────────────────────────────────────

VERTICES = list(range(8))  # 3-bit strings as ints 0..7
EDGES = [(u, v) for u in VERTICES for v in VERTICES if u < v and bin(u ^ v).count('1') == 1]
assert len(EDGES) == 12

# Canonical Z₅ typing: f(x⊕111) = -f(x) mod 5
# 000=2, 001=0, 010=4, 011=3, 100=2, 101=1, 110=0, 111=3
CANONICAL_F = {0b000: 2, 0b001: 0, 0b010: 4, 0b011: 3,
               0b100: 2, 0b101: 1, 0b110: 0, 0b111: 3}

Z5_NAMES = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}


def vertex_label(v):
    return f"{v:03b}"


def edge_type_z5(fa, fb):
    """Classify edge by Z₅ difference: 比和(0), 生(1,4), 克(2,3)."""
    d = (fa - fb) % 5
    if d == 0:
        return '比和'
    elif d in (1, 4):
        return '生'
    else:
        return '克'


def classify_edges(f):
    """Return tuple of edge types for all 12 edges (canonical edge order)."""
    return tuple(edge_type_z5(f[u], f[v]) for u, v in EDGES)


def edge_coloring_detail(f):
    """Return list of (u, v, type) for display."""
    return [(u, v, edge_type_z5(f[u], f[v])) for u, v in EDGES]


# ── Part 1: Aut(Q₃) orbit structure ───────────────────────────────────

def generate_aut_q3():
    """Generate all 48 automorphisms of Q₃ = S₃ ⋉ (Z₂)³.
    Each automorphism: permute bit positions, then XOR with a mask.
    Returns list of functions v → g(v)."""
    auts = []
    for perm in permutations(range(3)):  # 6 bit-position permutations
        for mask in range(8):            # 8 XOR masks
            def make_aut(p, m):
                def g(v):
                    bits = [(v >> i) & 1 for i in range(3)]
                    permuted = [bits[p[i]] for i in range(3)]
                    val = sum(permuted[i] << i for i in range(3))
                    return val ^ m
                return g
            auts.append(make_aut(perm, mask))
    assert len(auts) == 48
    return auts


def apply_automorphism(g, f):
    """Induced typing: f_g(v) = f(g⁻¹(v)).
    Since we have g forward, compute g⁻¹ by inverting the permutation."""
    # Build g as a lookup table, then invert
    g_table = {v: g(v) for v in VERTICES}
    g_inv = {g_table[v]: v for v in VERTICES}
    return {v: f[g_inv[v]] for v in VERTICES}


def connected_components(vertices, edges):
    """Find connected components in a subgraph."""
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    visited = set()
    components = []
    for v in vertices:
        if v not in visited and v in adj:
            comp = set()
            stack = [v]
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    comp.add(node)
                    stack.extend(adj[node] - visited)
            components.append(comp)
    return components


def is_path(vertices, edges):
    """Check if the subgraph on these vertices/edges is a simple path."""
    adj = defaultdict(set)
    for u, v in edges:
        if u in vertices and v in vertices:
            adj[u].add(v)
            adj[v].add(u)
    if not vertices:
        return False
    # Path: all degree ≤ 2, exactly 2 endpoints (degree 1), connected
    degrees = {v: len(adj[v]) for v in vertices}
    if any(d > 2 for d in degrees.values()):
        return False
    endpoints = [v for v, d in degrees.items() if d == 1]
    if len(endpoints) != 2:
        return False
    # Check connected
    visited = set()
    stack = [next(iter(vertices))]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(adj[node] - visited)
    return visited == vertices


def verify_subgraph_structure(coloring):
    """Verify: 克=2×P₄, 生=2×P₃, 比和=2×K₂ for an edge coloring."""
    type_edges = defaultdict(list)
    for u, v, t in coloring:
        type_edges[t].append((u, v))

    results = {}
    for t, expected in [('克', '2×P₄'), ('生', '2×P₃'), ('比和', '2×K₂')]:
        edges = type_edges[t]
        verts = set()
        for u, v in edges:
            verts.add(u)
            verts.add(v)
        comps = connected_components(verts, edges)
        comp_details = []
        for comp in comps:
            comp_edges = [(u, v) for u, v in edges if u in comp and v in comp]
            comp_details.append((len(comp), len(comp_edges), is_path(comp, edges)))

        if t == '比和':
            ok = (len(comps) == 2 and
                  all(len(c) == 2 for c in comps) and
                  len(edges) == 2)
        elif t == '生':
            ok = (len(comps) == 2 and
                  sorted(len(c) for c in comps) == [3, 3] and
                  len(edges) == 4 and
                  all(cd[2] for cd in comp_details))
        elif t == '克':
            ok = (len(comps) == 2 and
                  sorted(len(c) for c in comps) == [4, 4] and
                  len(edges) == 6 and
                  all(cd[2] for cd in comp_details))
        else:
            ok = False

        results[t] = (ok, len(comps), comp_details, len(edges))
    return results


def swap_sheng_ke(coloring_tuple):
    """Swap 生↔克 in an edge coloring tuple."""
    swap = {'生': '克', '克': '生', '比和': '比和'}
    return tuple(swap[t] for t in coloring_tuple)


def part1():
    print("=" * 70)
    print("PART 1: Orbit structure under Aut(Q₃) = S₃ ⋉ (Z₂)³")
    print("=" * 70)

    # Verify canonical typing complement-equivariance
    print("\n── Canonical typing verification ──")
    for v in VERTICES:
        comp = v ^ 0b111
        assert (CANONICAL_F[v] + CANONICAL_F[comp]) % 5 == 0, \
            f"Equivariance fails for {vertex_label(v)}"
        print(f"  {vertex_label(v)}={CANONICAL_F[v]}({Z5_NAMES[CANONICAL_F[v]]}), "
              f"complement {vertex_label(comp)}={CANONICAL_F[comp]}({Z5_NAMES[CANONICAL_F[comp]]}), "
              f"sum mod 5 = {(CANONICAL_F[v]+CANONICAL_F[comp])%5}")

    # Generate automorphisms and induced colorings
    auts = generate_aut_q3()
    colorings = {}  # coloring_tuple → list of automorphism indices
    coloring_details = {}  # coloring_tuple → full detail list

    for i, g in enumerate(auts):
        f_g = apply_automorphism(g, CANONICAL_F)
        ct = classify_edges(f_g)
        if ct not in colorings:
            colorings[ct] = []
            coloring_details[ct] = edge_coloring_detail(f_g)
        colorings[ct].append(i)

    n_distinct = len(colorings)
    stabilizer_size = 48 // n_distinct

    print(f"\n── Orbit summary ──")
    print(f"  Total automorphisms: 48")
    print(f"  Distinct edge-coloring patterns: {n_distinct}")
    print(f"  Stabilizer size: {stabilizer_size}")
    print(f"  Orbit-stabilizer check: {n_distinct} × {stabilizer_size} = {n_distinct * stabilizer_size}")

    # Print each distinct pattern
    print(f"\n── All {n_distinct} distinct edge-coloring patterns ──")
    patterns = list(colorings.keys())
    for idx, ct in enumerate(patterns):
        detail = coloring_details[ct]
        counts = defaultdict(int)
        for t in ct:
            counts[t] += 1
        print(f"\n  Pattern {idx+1} (appears {len(colorings[ct])}× in orbit):")
        print(f"    Edge counts: 比和={counts['比和']}, 生={counts['生']}, 克={counts['克']}")
        for u, v, t in detail:
            print(f"      {vertex_label(u)}-{vertex_label(v)} [{t}]")

    # Check 生↔克 swap relationships
    print(f"\n── 生↔克 swap relationships ──")
    swap_groups = []
    assigned = set()
    for i, ct in enumerate(patterns):
        if i in assigned:
            continue
        swapped = swap_sheng_ke(ct)
        found_partner = False
        for j, ct2 in enumerate(patterns):
            if j != i and ct2 == swapped:
                swap_groups.append((i, j))
                assigned.add(i)
                assigned.add(j)
                found_partner = True
                break
        if not found_partner:
            if swapped == ct:
                swap_groups.append((i, 'self'))
                assigned.add(i)
            else:
                swap_groups.append((i, 'no_partner'))
                assigned.add(i)

    for sg in swap_groups:
        if sg[1] == 'self':
            print(f"  Pattern {sg[0]+1}: self-dual (生↔克 swap = itself)")
        elif sg[1] == 'no_partner':
            print(f"  Pattern {sg[0]+1}: NO PARTNER (生↔克 swap not in orbit)")
        else:
            print(f"  Patterns {sg[0]+1} ↔ {sg[1]+1}: 生↔克 swap pair")

    # Verify subgraph structure
    print(f"\n── Subgraph structure verification (克=2×P₄, 生=2×P₃, 比和=2×K₂) ──")
    all_ok = True
    for idx, ct in enumerate(patterns):
        detail = coloring_details[ct]
        results = verify_subgraph_structure(detail)
        pattern_ok = all(r[0] for r in results.values())
        all_ok = all_ok and pattern_ok
        status = "✓" if pattern_ok else "✗"
        print(f"  Pattern {idx+1}: {status}", end="")
        for t in ('比和', '生', '克'):
            ok, ncomp, comp_details, nedges = results[t]
            sizes = sorted([cd[0] for cd in comp_details], reverse=True)
            print(f"  {t}: {nedges} edges, {ncomp} comps {sizes}", end="")
        print()

    print(f"\n  All patterns satisfy structure: {'YES' if all_ok else 'NO'}")

    return patterns, colorings


# ── Part 2: Inverse approach ──────────────────────────────────────────

def part2(part1_patterns):
    print("\n" + "=" * 70)
    print("PART 2: Inverse approach — constraint tightness")
    print("=" * 70)

    # Enumerate all F: {0,1}³ → Z₅ with complement equivariance + surjectivity
    # Complement pairs: {000,111}, {001,110}, {010,101}, {011,100}
    # Representatives: 000, 001, 010, 011
    REPS = [0b000, 0b001, 0b010, 0b011]
    COMPS = [r ^ 0b111 for r in REPS]

    valid_functions = []
    for vals in product(range(5), repeat=4):
        f = {}
        for i, r in enumerate(REPS):
            f[r] = vals[i]
            f[COMPS[i]] = (-vals[i]) % 5  # complement equivariance
        # Check surjectivity
        if len(set(f.values())) == 5:
            valid_functions.append(f)

    print(f"\n── Enumeration ──")
    print(f"  Total 5⁴ = 625 candidate assignments")
    print(f"  Valid (equivariant + surjective): {len(valid_functions)}")

    # Compute edge colorings
    coloring_to_functions = defaultdict(list)
    for f in valid_functions:
        ct = classify_edges(f)
        coloring_to_functions[ct].append(f)

    all_colorings = list(coloring_to_functions.keys())
    print(f"  Distinct edge-coloring patterns: {len(all_colorings)}")

    # Check overlap with Part 1
    part1_set = set(part1_patterns)
    part2_set = set(all_colorings)

    in_both = part1_set & part2_set
    only_part1 = part1_set - part2_set
    only_part2 = part2_set - part1_set

    print(f"\n── Overlap with Part 1 Aut(Q₃) orbit ──")
    print(f"  In both: {len(in_both)}")
    print(f"  Only in Aut(Q₃) orbit: {len(only_part1)}")
    print(f"  Only in equivariant+surjective: {len(only_part2)}")
    if only_part2:
        print(f"  ⚠ Extra patterns NOT reachable by Aut(Q₃):")
        for ct in only_part2:
            counts = defaultdict(int)
            for t in ct:
                counts[t] += 1
            funcs = coloring_to_functions[ct]
            print(f"    比和={counts['比和']}, 生={counts['生']}, 克={counts['克']}  ({len(funcs)} functions)")
            for f in funcs[:3]:  # show up to 3
                mapping = ", ".join(f"{vertex_label(v)}={f[v]}" for v in VERTICES)
                print(f"      {mapping}")
    else:
        print(f"  Every valid surjection is reachable by Aut(Q₃) — orbit is exhaustive.")

    every_in_part1 = (len(only_part2) == 0)
    print(f"\n  Aut(Q₃) orbit exhaustive: {'YES' if every_in_part1 else 'NO'}")

    # Minimal determining set
    print(f"\n── Minimal determining set ──")
    n_edges = len(EDGES)
    n_colorings = len(all_colorings)
    print(f"  Distinguishing {n_colorings} colorings across {n_edges} edges")

    # Precompute: for each coloring, its type on each edge
    color_vectors = []
    for ct in all_colorings:
        color_vectors.append(ct)

    found_min = None
    minimal_sets = []

    for size in range(1, n_edges + 1):
        for subset in combinations(range(n_edges), size):
            # Check if this subset distinguishes all colorings
            signatures = set()
            unique = True
            for cv in color_vectors:
                sig = tuple(cv[e] for e in subset)
                if sig in signatures:
                    unique = False
                    break
                signatures.add(sig)
            if unique:
                minimal_sets.append(subset)
        if minimal_sets:
            found_min = size
            break

    print(f"  Minimum determining set size: {found_min}")
    print(f"  Number of minimal determining sets: {len(minimal_sets)}")
    for s in minimal_sets:
        edge_names = [f"{vertex_label(EDGES[e][0])}-{vertex_label(EDGES[e][1])}" for e in s]
        print(f"    {edge_names}")

    # Show what each edge distinguishes
    if found_min and found_min <= 4:
        print(f"\n── Signature table for determining sets ──")
        for s in minimal_sets[:5]:  # show up to 5
            edge_names = [f"{vertex_label(EDGES[e][0])}-{vertex_label(EDGES[e][1])}" for e in s]
            print(f"\n  Edges: {edge_names}")
            for i, cv in enumerate(color_vectors):
                sig = tuple(cv[e] for e in s)
                print(f"    Coloring {i+1}: {sig}")

    return all_colorings, coloring_to_functions


# ── Summary ───────────────────────────────────────────────────────────

def summary(part1_patterns, part1_colorings, part2_colorings, part2_map):
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    p1_n = len(part1_patterns)
    p2_n = len(part2_colorings)
    p1_set = set(part1_patterns)
    p2_set = set(part2_colorings)

    print(f"""
  Q₃ vertices: 8, edges: 12
  Aut(Q₃) = S₃ ⋉ (Z₂)³, order 48

  Part 1 — Aut(Q₃) orbit of canonical typing:
    Distinct edge-colorings: {p1_n}
    Stabilizer size: {48 // p1_n}
    All satisfy 克=2×P₄, 生=2×P₃, 比和=2×K₂: YES

  Part 2 — All equivariant+surjective typings:
    Valid functions: {sum(len(v) for v in part2_map.values())}
    Distinct edge-colorings: {p2_n}
    Aut(Q₃) orbit is exhaustive: {'YES' if p2_set <= p1_set else 'NO'}
    Extra beyond Aut(Q₃): {len(p2_set - p1_set)}

  Edge-coloring counts per type (all patterns):""")

    for i, ct in enumerate(part2_colorings):
        counts = defaultdict(int)
        for t in ct:
            counts[t] += 1
        n_funcs = len(part2_map[ct])
        print(f"    Pattern {i+1}: 比和={counts['比和']} 生={counts['生']} 克={counts['克']}  ({n_funcs} functions)")


if __name__ == '__main__':
    part1_patterns, part1_colorings = part1()
    part2_colorings, part2_map = part2(part1_patterns)
    summary(part1_patterns, part1_colorings, part2_colorings, part2_map)
