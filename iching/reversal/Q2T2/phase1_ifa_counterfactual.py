#!/usr/bin/env python3
"""Phase 1: Ifá counterfactual — complement-respecting surjections F₂⁴ → Z₅.

Question: If Ifá's F₂⁴ substrate had the I Ching's axioms
(complement equivariance + surjection to Z₅), what orbit landscape emerges?

Method:
  - F₂⁴ has 16 elements, 8 complement pairs (v = 0b1111 = 15)
  - Complement-respecting: f(x ⊕ v) = -f(x) mod 5
  - Choose f on one rep per pair → 5⁸ = 390,625 candidates, filter surjective
  - Symmetry group: Stab(1111) ≤ GL(4,F₂) × Aut(Z₅)
  - Orbit partition via union-find with generators
"""

from itertools import product
from collections import Counter
import time
import sys
sys.path.insert(0, '..')

# ═══════════════════════════════════════════════════════
# F₂ linear algebra (from Q2 phase2)
# ═══════════════════════════════════════════════════════

def mat_vec_f2(M, x, n):
    result = 0
    for i in range(n):
        parity = bin(M[i] & x).count('1') & 1
        result |= parity << (n - 1 - i)
    return result

def is_invertible_f2(rows, n):
    R = list(rows)
    for col in range(n):
        mask = 1 << (n - 1 - col)
        pivot = None
        for r in range(col, n):
            if R[r] & mask:
                pivot = r
                break
        if pivot is None:
            return False
        R[col], R[pivot] = R[pivot], R[col]
        for r in range(n):
            if r != col and R[r] & mask:
                R[r] ^= R[col]
    return True

def enumerate_gl_f2(n):
    N = 1 << n
    return [list(rows) for rows in product(range(N), repeat=n)
            if is_invertible_f2(list(rows), n)]


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

    def components(self):
        groups = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            groups.setdefault(r, []).append(i)
        return groups


# ═══════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════

N_BITS = 4
N_ELEMS = 16         # |F₂⁴|
COMP_VEC = 15        # 0b1111
P = 5                # target Z₅


def complement_pair_reps():
    """Choose one representative per complement pair {x, x⊕1111}.
    For each pair, take the element with smaller index."""
    reps = []
    seen = set()
    for x in range(N_ELEMS):
        if x not in seen:
            reps.append(x)
            seen.add(x)
            seen.add(x ^ COMP_VEC)
    return reps  # 8 representatives


def enumerate_comp_resp_surjections():
    """All complement-respecting surjections F₂⁴ → Z₅.

    For each representative x in a complement pair, assign f(x) ∈ {0..4}.
    Then f(x⊕v) = (-f(x)) mod 5.
    Filter for surjectivity.
    """
    reps = complement_pair_reps()
    assert len(reps) == 8

    surjections = []
    for vals in product(range(P), repeat=8):
        # Build full function
        f = [0] * N_ELEMS
        for i, x in enumerate(reps):
            f[x] = vals[i]
            f[x ^ COMP_VEC] = (-vals[i]) % P
        # Check surjectivity
        if len(set(f)) == P:
            surjections.append(tuple(f))
    return surjections


def stab_transvection_generators():
    """Transvections E_{ij} on F₂⁴ that fix the complement vector 1111.

    E_{ij}(x): if bit i of x is set, flip bit j of x.
    E_{ij}(1111): since bit i of 1111 is always 1, this flips bit j,
    giving 1111 ⊕ (1 << j). That equals 1111 only if... it never does
    for i≠j. Wait — let me reconsider.

    Actually, E_{ij}(x) = x ⊕ ((x >> bit_i) & 1) · e_j.
    With our convention, bit positions: bit 0 is LSB.

    For x = 1111 = 15: bit i is always 1, so E_{ij}(15) = 15 ⊕ (1 << j).
    This equals 15 iff 1 << j = 0, which is impossible.

    So NO single transvection fixes 1111! We need composite generators.

    Alternative: transvection I + e_i·e_j^T where e_i, e_j are basis vectors.
    Let's use the standard definition: T_{ij} adds row j to row i, i.e.,
    the matrix with 1s on diagonal and a 1 at position (i,j).

    T_{ij} applied to column vector v: v' = v, except v'_i = v_i + v_j (mod 2).

    For v = (1,1,1,1)^T: v'_i = 1 + 1 = 0 ≠ 1. So T_{ij}(1111) ≠ 1111.

    Hmm, so Stab(1111) contains NO transvections. We need to find actual
    generators of Stab(1111) differently.

    Let's enumerate Stab(1111) directly from GL(4,F₂).
    """
    pass  # Will use direct enumeration instead


def compute_stab_generators(gl4):
    """Find Stab(1111) ≤ GL(4,F₂) and extract generators.

    Strategy: filter GL(4,F₂) for matrices fixing 1111,
    then use a small generating set.
    """
    stab = [A for A in gl4 if mat_vec_f2(A, COMP_VEC, N_BITS) == COMP_VEC]
    print(f"  |Stab(1111)| = {len(stab)} (expected 20160/15 = 1344)")

    # Extract domain permutations induced by Stab elements
    perms = []
    for A in stab:
        perm = [mat_vec_f2(A, x, N_BITS) for x in range(N_ELEMS)]
        perms.append(perm)

    # Find generators via incremental closure test:
    # Add matrices one at a time, check if group grows
    generators = []
    generated = {tuple(range(N_ELEMS))}  # identity permutation

    for perm in perms:
        perm_t = tuple(perm)
        if perm_t in generated:
            continue
        generators.append(perm)
        # Expand group with this generator
        queue = [perm_t]
        new_elements = {perm_t}
        while queue:
            current = queue.pop()
            for g in list(generated) | new_elements:
                # compose current ∘ g and g ∘ current
                for a, b in [(current, g), (g, current)]:
                    composed = tuple(a[b[x]] for x in range(N_ELEMS))
                    if composed not in generated and composed not in new_elements:
                        new_elements.add(composed)
                        queue.append(composed)
        generated |= new_elements
        if len(generated) == len(stab):
            break

    print(f"  Generators found: {len(generators)} (group size: {len(generated)})")
    return generators, stab


def compute_stab_generator_perms(gl4):
    """More efficient: find a few generators of Stab(1111) by random selection,
    verify they generate the full group."""
    stab_perms = []
    for A in gl4:
        if mat_vec_f2(A, COMP_VEC, N_BITS) == COMP_VEC:
            perm = tuple(mat_vec_f2(A, x, N_BITS) for x in range(N_ELEMS))
            stab_perms.append(perm)

    stab_set = set(stab_perms)
    print(f"  |Stab(1111)| = {len(stab_set)} (expected 1344)")

    # Find generators: pick elements, close under composition, stop when full
    identity = tuple(range(N_ELEMS))
    generators = []
    generated = {identity}

    for perm in stab_perms:
        if perm in generated:
            continue
        generators.append(perm)
        # BFS expand
        frontier = [perm]
        while frontier:
            next_frontier = []
            for f in frontier:
                for g in generators:
                    for composed in [tuple(f[g[x]] for x in range(N_ELEMS)),
                                     tuple(g[f[x]] for x in range(N_ELEMS))]:
                        if composed not in generated:
                            generated.add(composed)
                            next_frontier.append(composed)
            frontier = next_frontier
        if len(generated) == len(stab_set):
            break

    print(f"  Generators: {len(generators)}, closure size: {len(generated)}")
    assert len(generated) == len(stab_set), "Generator closure doesn't match Stab!"
    return generators


def fiber_partition(f, p):
    """Fiber partition of f: sizes of preimages, sorted descending."""
    counts = Counter(f)
    return tuple(sorted(counts.values(), reverse=True))


def run_phase1():
    print("Phase 1: Ifá Counterfactual — F₂⁴ → Z₅ with complement equivariance")
    print("=" * 70)

    # ── Step 1: Enumerate complement-respecting surjections ──
    print("\nStep 1: Enumerate complement-respecting surjections")
    t0 = time.time()
    surjections = enumerate_comp_resp_surjections()
    t1 = time.time()
    print(f"  Total: {len(surjections)} (from 5⁸ = {5**8} candidates) [{t1-t0:.1f}s]")

    # ── Step 2: Validate complement-respecting property ──
    print("\nStep 2: Validation")
    for f in surjections[:10]:
        for x in range(N_ELEMS):
            assert (f[x] + f[x ^ COMP_VEC]) % P == 0, f"Complement violation at {x}"
        assert len(set(f)) == P, "Not surjective"
    print("  ✓ Complement-respecting and surjective (spot-checked)")

    # Verify: what's the complement pair structure?
    reps = complement_pair_reps()
    print(f"  Complement pairs ({len(reps)}):")
    for x in reps:
        print(f"    {x:04b} ↔ {x^COMP_VEC:04b}")

    # ── Step 3: Compute Stab(1111) ──
    print("\nStep 3: Compute Stab(1111) ≤ GL(4,F₂)")
    t0 = time.time()
    gl4 = enumerate_gl_f2(N_BITS)
    t_gl = time.time() - t0
    print(f"  |GL(4,F₂)| = {len(gl4)} [{t_gl:.1f}s]")

    t0 = time.time()
    generators = compute_stab_generator_perms(gl4)
    t_stab = time.time() - t0
    print(f"  [{t_stab:.1f}s]")

    # ── Step 4: Union-find orbit partition ──
    print("\nStep 4: Orbit partition under Stab(1111) × Aut(Z₅)")
    t0 = time.time()

    surj_idx = {s: i for i, s in enumerate(surjections)}
    uf = UnionFind(len(surjections))

    # Apply Stab(1111) generators
    # Action: A ∈ GL sends f ↦ f ∘ A⁻¹. If perm = A on domain,
    # then (f ∘ A⁻¹)(y) = f(A⁻¹(y)).
    for gen in generators:
        inv_gen = [0] * N_ELEMS
        for x in range(N_ELEMS):
            inv_gen[gen[x]] = x
        for idx in range(len(surjections)):
            f = surjections[idx]
            g = tuple(f[inv_gen[y]] for y in range(N_ELEMS))
            j = surj_idx.get(g)
            if j is not None:
                uf.union(idx, j)

    # Apply Aut(Z₅) generator: multiply by 2 (primitive root mod 5)
    alpha = 2  # 2 is a primitive root mod 5: 2,4,3,1
    for idx in range(len(surjections)):
        f = surjections[idx]
        g = tuple((alpha * v) % P for v in f)
        j = surj_idx.get(g)
        if j is not None:
            uf.union(idx, j)

    t_uf = time.time() - t0
    comps = uf.components()
    n_orbits = len(comps)
    orbit_sizes = sorted([len(v) for v in comps.values()], reverse=True)

    print(f"  Orbits: {n_orbits} [{t_uf:.1f}s]")
    print(f"  Orbit sizes: {orbit_sizes}")
    print(f"  Size distribution: {dict(Counter(orbit_sizes))}")

    # ── Step 5: Fiber partitions per orbit ──
    print("\nStep 5: Fiber partitions per orbit")
    orbit_fibers = []
    for root, indices in sorted(comps.items(), key=lambda x: -len(x[1])):
        # All surjections in an orbit have the same fiber partition
        rep_f = surjections[indices[0]]
        fp = fiber_partition(rep_f, P)
        orbit_fibers.append((len(indices), fp))

        # Verify all members have same fiber partition
        for idx in indices[:20]:  # spot check
            assert fiber_partition(surjections[idx], P) == fp

    orbit_fibers.sort(key=lambda x: (-x[0], x[1]))

    print(f"\n  {'Orbit#':<8} {'Size':<10} {'Fiber partition':<30} {'Sum':<6}")
    print(f"  {'-'*54}")
    for i, (size, fp) in enumerate(orbit_fibers):
        print(f"  {i+1:<8} {size:<10} {str(fp):<30} {sum(fp):<6}")

    # ── Step 6: Comparison with (3,5) baseline ──
    print(f"\n{'='*70}")
    print("COMPARISON WITH (3,5) BASELINE")
    print(f"{'='*70}")

    print(f"\n  (3,5) I Ching:")
    print(f"    Complement-respecting surjections: 240")
    print(f"    Orbits: 5")
    print(f"    Fiber types: {{2,2,2,1,1}} and {{4,1,1,1,1}}")
    print(f"    Characteristic: 2-singleton partition = the I Ching's actual structure")

    print(f"\n  (4,5) Ifá counterfactual:")
    print(f"    Complement-respecting surjections: {len(surjections)}")
    print(f"    Orbits: {n_orbits}")

    # Check for {2,2,2,1,1}-type partitions (proportionally scaled)
    # At (4,5): 16 elements, 5 values → average fiber size 3.2
    iching_type = any(fp.count(1) == 2 for _, fp in orbit_fibers)
    print(f"    Any orbit with exactly 2 singleton fibers: {iching_type}")

    # Detailed fiber type analysis
    fiber_types = Counter(fp for _, fp in orbit_fibers)
    print(f"\n  Fiber partition types (across all orbits):")
    for fp, count in fiber_types.most_common():
        print(f"    {fp}: {count} orbit(s)")

    # ── Step 7: Deeper analysis ──
    print(f"\n{'='*70}")
    print("STRUCTURAL ANALYSIS")
    print(f"{'='*70}")

    # How many fibers of each size appear?
    print(f"\n  Fiber size frequency across all orbit types:")
    all_fiber_sizes = []
    for fp, count in fiber_types.items():
        for size in fp:
            all_fiber_sizes.extend([size] * count)
    for size, cnt in sorted(Counter(all_fiber_sizes).items()):
        print(f"    Size {size}: appears in {cnt} orbit type(s)")

    # Verify total: each surjection maps 16 elements to 5 values
    for f in surjections[:10]:
        assert sum(Counter(f).values()) == 16

    print(f"\n  Key metrics:")
    print(f"    |F₂⁴| = {N_ELEMS}, |Z₅| = {P}")
    print(f"    Complement pairs: {N_ELEMS // 2}")
    print(f"    Average fiber size: {N_ELEMS / P:.1f}")
    print(f"    |Stab(1111)| = 1344")
    print(f"    |Aut(Z₅)| = 4")
    print(f"    |Stab × Aut| = {1344 * 4}")
    print(f"    Naive orbit estimate: {len(surjections)} / {1344*4} = {len(surjections)/(1344*4):.1f}")
    print(f"    Actual orbits: {n_orbits}")

    return {
        'surjection_count': len(surjections),
        'orbit_count': n_orbits,
        'orbit_sizes': orbit_sizes,
        'orbit_fibers': orbit_fibers,
        'fiber_types': fiber_types,
    }


if __name__ == '__main__':
    results = run_phase1()
