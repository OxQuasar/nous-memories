#!/usr/bin/env python3
"""
flat_uniformity.py — Flat-direction pattern analysis across all 240 surjections

For each complement-equivariant surjection F₂³ → Z₅:
  - Compute the derivative spectrum for all 7 nonzero directions
  - Identify "flat" directions (max derivative count ≤ 2)
  - Classify surjections by their flat-direction pattern

Then analyze:
  - How many distinct flat-direction patterns exist?
  - How do the 240 surjections partition across patterns?
  - What is the orbit structure under Stab(111) × Aut(Z₅)?
  - What is the stabilizer for each pattern?
  - Detailed analysis of the IC pattern {001, 101, 111}
"""

import json
from pathlib import Path
from collections import Counter, defaultdict
from itertools import product as iterproduct

HERE = Path(__file__).resolve().parent
OUT_PATH = HERE / "flat_uniformity_results.json"

P = 5
IC = [2, 0, 4, 3, 2, 1, 0, 3]

def fmt(x): return format(x, '03b')
def popcount(x): return bin(x).count('1')


# ═══════════════════════════════════════════════════════════════════
# F₂ linear algebra
# ═══════════════════════════════════════════════════════════════════

def mat_vec_f2(A, v, n=3):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result


def mat_det_f2(A):
    a, b, c = A[0]; d, e, f_ = A[1]; g, h, k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1


def mat_inv_f2(A, n=3):
    M = [A[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]:
                pivot = row
                break
        if pivot is None:
            return None
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        for row in range(n):
            if row != col and M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(2 * n)]
    return [M[i][n:] for i in range(n)]


def mat_to_str(A, n=3):
    return '[' + ','.join(''.join(str(A[i][j]) for j in range(n)) for i in range(n)) + ']'


def compute_stab():
    stab = []
    for row0 in range(1, 8):
        for row1 in range(1, 8):
            for row2 in range(1, 8):
                A = [[(row0 >> j) & 1 for j in range(3)],
                     [(row1 >> j) & 1 for j in range(3)],
                     [(row2 >> j) & 1 for j in range(3)]]
                if mat_det_f2(A) and mat_vec_f2(A, 7) == 7:
                    stab.append(A)
    return stab


# ═══════════════════════════════════════════════════════════════════
# Enumerate all 240 complement-equivariant surjections
# ═══════════════════════════════════════════════════════════════════

def enumerate_surjections():
    """
    Complement-equivariant: f(x⊕111) = -f(x) mod 5.
    So f is determined by values on {000, 001, 010, 011} (representatives of
    complement pairs). f(000) + f(111) = 0 mod 5, etc.
    Surjective onto Z₅.
    """
    pairs = [(0, 7), (1, 6), (2, 5), (3, 4)]
    surjections = []
    for assignment in iterproduct(range(P), repeat=len(pairs)):
        fmap = {}
        for i, (rep, partner) in enumerate(pairs):
            fmap[rep] = assignment[i]
            fmap[partner] = (-assignment[i]) % P
        if len(set(fmap.values())) == P:
            surjections.append(tuple(fmap[x] for x in range(8)))
    return surjections


# ═══════════════════════════════════════════════════════════════════
# Derivative analysis
# ═══════════════════════════════════════════════════════════════════

def compute_derivative_spectrum(f):
    """For each nonzero direction a, compute derivative distribution over Z₅."""
    spectrum = {}
    for a in range(1, 8):
        counts = [0] * P
        for x in range(8):
            d = (f[x ^ a] - f[x]) % P
            counts[d] += 1
        spectrum[a] = tuple(counts)
    return spectrum


def flat_directions(f):
    """Return frozenset of directions a where max derivative count ≤ 2."""
    spec = compute_derivative_spectrum(f)
    return frozenset(a for a in range(1, 8) if max(spec[a]) <= 2)


# ═══════════════════════════════════════════════════════════════════
# Group actions
# ═══════════════════════════════════════════════════════════════════

def apply_action(f, A_inv, tau):
    """Apply (A, τ) to surjection f: g(x) = τ · f(A⁻¹ x)."""
    return tuple((tau * f[mat_vec_f2(A_inv, x)]) % P for x in range(8))


def transform_flat_pattern(pattern, A):
    """Transform a set of flat directions under A ∈ GL(3,F₂).
    Direction a maps to A·a."""
    return frozenset(mat_vec_f2(A, a) for a in pattern)


# ═══════════════════════════════════════════════════════════════════
# Main computation
# ═══════════════════════════════════════════════════════════════════

def main():
    print("=" * 72)
    print("  FLAT-DIRECTION UNIFORMITY ANALYSIS")
    print("=" * 72)
    print()

    # Step 1: Enumerate surjections and compute flat patterns
    surjections = enumerate_surjections()
    print(f"  Total complement-equivariant surjections: {len(surjections)}")

    ic_tuple = tuple(IC)
    assert ic_tuple in surjections, "IC not found in surjection list"

    # Compute flat-direction pattern for each surjection
    pattern_map = {}  # surjection → flat pattern (frozenset)
    pattern_groups = defaultdict(list)  # pattern → list of surjections

    for f in surjections:
        pat = flat_directions(f)
        pattern_map[f] = pat
        pattern_groups[pat].append(f)

    print(f"  Distinct flat-direction patterns: {len(pattern_groups)}")
    print()

    # Step 2: Display patterns
    print(f"  {'Pattern':>25}  {'Size':>4}  {'Directions'}")
    print("  " + "-" * 55)
    for pat in sorted(pattern_groups.keys(), key=lambda p: (-len(p), sorted(p))):
        dirs = ", ".join(fmt(a) for a in sorted(pat))
        size = len(pattern_groups[pat])
        marker = " ← IC" if ic_tuple in pattern_groups[pat] else ""
        print(f"  {{{dirs}}}  {size:>4}{marker}")

    # Verify: total = 240
    total = sum(len(g) for g in pattern_groups.values())
    print(f"\n  Total surjections accounted for: {total}")

    # Check if all patterns have same size
    sizes = [len(g) for g in pattern_groups.values()]
    if len(set(sizes)) == 1:
        print(f"  All patterns have equal size: {sizes[0]} ✓")
    else:
        print(f"  Pattern sizes vary: {Counter(sizes)}")

    # Step 3: Group action analysis
    print()
    print("=" * 72)
    print("  GROUP ACTION ON FLAT-DIRECTION PATTERNS")
    print("=" * 72)
    print()

    stab = compute_stab()
    stab_invs = [mat_inv_f2(A) for A in stab]
    print(f"  |Stab(111)| = {len(stab)}, |Aut(Z₅)| = {P-1}")
    print(f"  |G| = |Stab(111)| × |Aut(Z₅)| = {len(stab) * (P-1)}")
    print()

    # For each surjection, apply all group elements and check pattern preservation
    # More efficient: work at the pattern level
    # A ∈ Stab(111) acts on directions: a ↦ A·a
    # τ ∈ Aut(Z₅) doesn't change directions (it scales values, not inputs)
    # So flat-direction patterns transform only under Stab(111)

    # Verify: τ preserves flat patterns
    print("  Verifying: Aut(Z₅) preserves flat-direction patterns...")
    tau_preserves = True
    for f in surjections[:50]:  # spot check
        pat_f = pattern_map[f]
        for tau in range(1, P):
            g = tuple((tau * f[x]) % P for x in range(8))
            pat_g = flat_directions(g)
            if pat_g != pat_f:
                tau_preserves = False
                break
        if not tau_preserves:
            break

    if tau_preserves:
        # Full check
        for f in surjections:
            pat_f = pattern_map[f]
            for tau in range(1, P):
                g = tuple((tau * f[x]) % P for x in range(8))
                pat_g = flat_directions(g)
                if pat_g != pat_f:
                    tau_preserves = False
                    break
            if not tau_preserves:
                break

    print(f"  Aut(Z₅) preserves flat patterns: {'✓' if tau_preserves else '✗'}")
    print()

    # Compute orbits of patterns under Stab(111) action on directions
    pattern_list = list(pattern_groups.keys())
    pattern_orbits = []  # list of sets of patterns
    visited = set()

    for pat in pattern_list:
        if pat in visited:
            continue
        orbit = set()
        queue = [pat]
        while queue:
            p = queue.pop()
            if p in visited:
                continue
            visited.add(p)
            orbit.add(p)
            # Apply all A ∈ Stab(111) to the pattern
            for A in stab:
                transformed = transform_flat_pattern(p, A)
                if transformed not in visited:
                    queue.append(transformed)
        pattern_orbits.append(orbit)

    print(f"  Orbits of flat-direction patterns under Stab(111):")
    print(f"  Number of orbits: {len(pattern_orbits)}")
    for i, orbit in enumerate(pattern_orbits):
        sizes_in_orbit = [len(pattern_groups[p]) for p in orbit]
        total_surj = sum(sizes_in_orbit)
        sample = sorted(orbit, key=lambda p: sorted(p))[0]
        dirs = ", ".join(fmt(a) for a in sorted(sample))
        ic_in = any(ic_tuple in pattern_groups[p] for p in orbit)
        print(f"    Orbit {i}: {len(orbit)} patterns, {total_surj} surjections"
              f"  (sample: {{{dirs}}})"
              f"{'  ← contains IC' if ic_in else ''}")

    print()

    # Stabilizer analysis for each pattern
    print("  Stabilizer analysis (for each pattern, which g ∈ Stab(111) fix it):")
    stab_sizes = {}
    for pat in pattern_list:
        stabilizer = []
        for i, A in enumerate(stab):
            if transform_flat_pattern(pat, A) == pat:
                stabilizer.append(i)
        stab_sizes[pat] = len(stabilizer)

    # Display
    print(f"\n  {'Pattern':>30}  {'Surj':>4}  {'|Stab_pat|':>10}  {'|Orbit|':>7}")
    print("  " + "-" * 60)
    for pat in sorted(pattern_groups.keys(), key=lambda p: (-len(p), sorted(p))):
        dirs = ", ".join(fmt(a) for a in sorted(pat))
        n_surj = len(pattern_groups[pat])
        ss = stab_sizes[pat]
        orbit_size = len(stab) // ss  # orbit-stabilizer theorem
        marker = " ← IC" if ic_tuple in pattern_groups[pat] else ""
        print(f"  {{{dirs}:>27}}  {n_surj:>4}  {ss:>10}  {orbit_size:>7}{marker}")

    # Verify orbit-stabilizer theorem
    print()
    print("  Orbit-stabilizer check: |orbit| × |stab| should = 24 for each pattern")
    ost_ok = True
    for pat in pattern_list:
        # Find orbit size for this pattern
        for orbit in pattern_orbits:
            if pat in orbit:
                if len(orbit) * stab_sizes[pat] != len(stab):
                    ost_ok = False
                    print(f"    FAIL: pattern {sorted(pat)}: |orbit|={len(orbit)}, |stab|={stab_sizes[pat]}")
                break
    if ost_ok:
        print(f"  Orbit-stabilizer theorem: ✓ (all patterns satisfy |orbit|×|stab|=24)")

    # Step 4: Orbit structure under full group G = Stab(111) × Aut(Z₅) on surjections
    print()
    print("=" * 72)
    print("  ORBIT STRUCTURE ON SURJECTIONS")
    print("=" * 72)
    print()

    # Use union-find on surjections
    surj_set = set(surjections)
    parent = {s: s for s in surjections}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for s in surjections:
        for A_inv in stab_invs:
            for tau in range(1, P):
                t = apply_action(s, A_inv, tau)
                if t in surj_set:
                    union(s, t)

    orbit_map = defaultdict(list)
    for s in surjections:
        orbit_map[find(s)].append(s)

    surj_orbits = sorted(orbit_map.values(), key=lambda o: (-len(o), sorted(o)[0]))
    print(f"  Orbits under Stab(111) × Aut(Z₅): {len(surj_orbits)}")
    for i, orb in enumerate(surj_orbits):
        pat = pattern_map[orb[0]]
        # Check: all surjections in same orbit have patterns in same pattern orbit
        pats_in_orb = set(pattern_map[f] for f in orb)
        n_pats = len(pats_in_orb)
        dirs = ", ".join(fmt(a) for a in sorted(pat))
        ic_in = ic_tuple in orb
        print(f"    Orbit {i}: {len(orb)} surjections, {n_pats} flat-direction patterns"
              f"  (sample: {{{dirs}}})"
              f"{'  ← contains IC' if ic_in else ''}")

    # Orbits under Stab(111) alone (τ=1 only)
    print()
    parent2 = {s: s for s in surjections}

    def find2(x):
        while parent2[x] != x:
            parent2[x] = parent2[parent2[x]]
            x = parent2[x]
        return x

    def union2(a, b):
        ra, rb = find2(a), find2(b)
        if ra != rb:
            parent2[ra] = rb

    for s in surjections:
        for A_inv in stab_invs:
            t = apply_action(s, A_inv, 1)  # τ=1 only
            if t in surj_set:
                union2(s, t)

    orbit_map2 = defaultdict(list)
    for s in surjections:
        orbit_map2[find2(s)].append(s)

    surj_orbits2 = sorted(orbit_map2.values(), key=lambda o: (-len(o), sorted(o)[0]))
    print(f"  Orbits under Stab(111) alone: {len(surj_orbits2)}")
    for i, orb in enumerate(surj_orbits2):
        pat = pattern_map[orb[0]]
        pats_in_orb = set(pattern_map[f] for f in orb)
        dirs = ", ".join(fmt(a) for a in sorted(pat))
        ic_in = ic_tuple in orb
        print(f"    Orbit {i}: {len(orb)} surjections, {len(pats_in_orb)} patterns"
              f"  (sample: {{{dirs}}})"
              f"{'  ← contains IC' if ic_in else ''}")

    # Step 5: Deep dive on IC pattern {001, 101, 111}
    print()
    print("=" * 72)
    print("  IC PATTERN {001, 101, 111}: DETAILED ANALYSIS")
    print("=" * 72)
    print()

    ic_pat = pattern_map[ic_tuple]
    ic_group = pattern_groups[ic_pat]
    print(f"  IC flat-direction pattern: {{{', '.join(fmt(a) for a in sorted(ic_pat))}}}")
    print(f"  Surjections with this pattern: {len(ic_group)}")
    print()

    # List all 16 surjections
    print(f"  All surjections with IC pattern:")
    print(f"  {'f(000..111)':>15}  {'f values':>15}  {'Fibers (element → count)':>30}")
    for f in sorted(ic_group):
        fibers = Counter(f)
        fiber_str = " ".join(f"{v}:{c}" for v, c in sorted(fibers.items()))
        print(f"  {str(list(f)):>15}  {fiber_str:>30}")

    # Stabilizer subgroup for the IC pattern
    print()
    ic_stab_indices = []
    for i, A in enumerate(stab):
        if transform_flat_pattern(ic_pat, A) == ic_pat:
            ic_stab_indices.append(i)

    print(f"  Stabilizer of IC pattern in Stab(111): order {len(ic_stab_indices)}")
    print(f"  Stabilizer elements:")
    for i in ic_stab_indices:
        A = stab[i]
        print(f"    {mat_to_str(A)}")

    # Check: does the stabilizer fix 111? (it should, being in Stab(111))
    # More interesting: what subgroup of S₄ is this?
    # Compute orders of stabilizer elements
    orders = []
    for i in ic_stab_indices:
        A = stab[i]
        current = [[1 if r == c else 0 for c in range(3)] for r in range(3)]
        for k in range(1, 50):
            current = [[sum(current[r][m] & A[m][c] for m in range(3)) % 2
                        for c in range(3)] for r in range(3)]
            if all(current[r][c] == (1 if r == c else 0) for r in range(3) for c in range(3)):
                orders.append(k)
                break
    print(f"  Element orders: {sorted(Counter(orders).items())}")

    # Eigenvalue analysis: which directions are special?
    print()
    print(f"  Eigenvalue check for IC surjection:")
    for a in range(1, 8):
        # Check D_a f = c·f for some c
        found = False
        for c in range(P):
            if all((IC[x ^ a] - IC[x]) % P == (c * IC[x]) % P for x in range(8)):
                print(f"    D_{{{fmt(a)}}} f = {c}·f  ✓  (flat: {a in ic_pat})")
                found = True
                break
        if not found:
            spec = compute_derivative_spectrum(ic_tuple)[a]
            print(f"    D_{{{fmt(a)}}} f: no eigenvalue  (spectrum: {spec}, max={max(spec)}, flat: {a in ic_pat})")

    # Structural characterization of flat directions
    print()
    print(f"  Structural analysis of flat directions {{001, 101, 111}}:")
    flat_dirs = sorted(ic_pat)
    print(f"    001 ⊕ 101 = {fmt(1 ^ 5)} = 100")
    print(f"    001 ⊕ 111 = {fmt(1 ^ 7)} = 110")
    print(f"    101 ⊕ 111 = {fmt(5 ^ 7)} = 010")
    print(f"    Fano lines through these:")
    # Fano lines in PG(2,2): {a,b,a⊕b}
    fano_lines = []
    for a in range(1, 8):
        for b in range(a + 1, 8):
            c = a ^ b
            if c > b:
                fano_lines.append(frozenset([a, b, c]))
    fano_lines = list(set(fano_lines))
    for line in sorted(fano_lines, key=lambda l: sorted(l)):
        dirs = sorted(line)
        in_flat = sum(1 for d in dirs if d in ic_pat)
        print(f"    {{{', '.join(fmt(d) for d in dirs)}}}: {in_flat}/3 flat")

    # Save results
    results = {
        "total_surjections": len(surjections),
        "distinct_patterns": len(pattern_groups),
        "pattern_details": [
            {
                "directions": sorted(pat),
                "directions_str": [fmt(a) for a in sorted(pat)],
                "n_surjections": len(pattern_groups[pat]),
                "stabilizer_size": stab_sizes[pat],
                "contains_ic": ic_tuple in pattern_groups[pat],
            }
            for pat in sorted(pattern_groups.keys(), key=lambda p: (-len(p), sorted(p)))
        ],
        "pattern_orbits_stab111": len(pattern_orbits),
        "surjection_orbits_full_group": len(surj_orbits),
        "surjection_orbits_stab_only": len(surj_orbits2),
        "aut_preserves_patterns": tau_preserves,
        "ic_pattern": {
            "directions": sorted(ic_pat),
            "n_surjections": len(ic_group),
            "stabilizer_order": len(ic_stab_indices),
        },
    }

    with open(OUT_PATH, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n\nResults saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
