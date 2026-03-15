#!/usr/bin/env python3
"""Phase 3: Internal structure of GL-orbits at (3,5).

Tasks:
1. For each complement-touching GL-orbit: test equivariance w.r.t. all 7 nonzero vectors.
   Verify that surjections in each orbit are equivariant w.r.t. exactly one vector each,
   and all 7 vectors appear equally.

2. For non-complement-touching orbits: compute fiber partitions, report distribution.

3. Check if any surjections have fiber partition {2,2,2,1,1} but are NOT equivariant
   w.r.t. any nonzero vector.

4. Count distinct fiber partitions at (3,3), (3,5), (3,7) to explain non-monotonicity.
"""

from itertools import product
from collections import Counter, defaultdict
import time

# ═══════════════════════════════════════════════════════
# F₂ linear algebra (from phase2)
# ═══════════════════════════════════════════════════════

def mat_vec_f2(M, x, n):
    result = 0
    for i in range(n):
        bits = M[i] & x
        parity = bin(bits).count('1') & 1
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

_gl_cache = {}
def get_gl(n):
    if n not in _gl_cache:
        _gl_cache[n] = enumerate_gl_f2(n)
    return _gl_cache[n]


# ═══════════════════════════════════════════════════════
# Union-Find
# ═══════════════════════════════════════════════════════

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


def primitive_root(p):
    for g in range(2, p):
        if len({pow(g, k, p) for k in range(1, p)}) == p - 1:
            return g


def transvection_perms(n):
    N = 1 << n
    perms = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            perm = [x ^ (((x >> i) & 1) << j) for x in range(N)]
            perms.append(perm)
    return perms


def enumerate_surjections(n, p):
    N = 1 << n
    return [vals for vals in product(range(p), repeat=N) if len(set(vals)) == p]


def build_orbit_partition(n, p, surjections):
    """Partition surjections into orbits under GL(n,F₂) × Aut(Z_p)."""
    N = 1 << n
    surj_idx = {s: i for i, s in enumerate(surjections)}
    uf = UnionFind(len(surjections))

    perms = transvection_perms(n)
    for perm in perms:
        for idx in range(len(surjections)):
            f = surjections[idx]
            g = tuple(f[perm[x]] for x in range(N))
            j = surj_idx.get(g)
            if j is not None:
                uf.union(idx, j)

    alpha = primitive_root(p)
    for idx in range(len(surjections)):
        f = surjections[idx]
        g = tuple((alpha * v) % p for v in f)
        j = surj_idx.get(g)
        if j is not None:
            uf.union(idx, j)

    return uf


# ═══════════════════════════════════════════════════════
# Equivariance and fiber analysis
# ═══════════════════════════════════════════════════════

def equivariant_vectors(f, n, p):
    """Return set of nonzero vectors v ∈ F₂ⁿ such that f(x⊕v) = −f(x) mod p for all x."""
    N = 1 << n
    result = []
    for v in range(1, N):  # all nonzero vectors
        ok = True
        for x in range(N):
            if (f[x] + f[x ^ v]) % p != 0:
                ok = False
                break
        if ok:
            result.append(v)
    return result


def fiber_partition(f, p):
    """Return sorted tuple of fiber sizes: how many domain elements map to each value."""
    counts = Counter(f)
    return tuple(sorted(counts.values(), reverse=True))


def vec_str(v, n):
    """Binary string for vector."""
    return format(v, f'0{n}b')


# ═══════════════════════════════════════════════════════
# Task 1: Equivariance analysis of complement-touching orbits
# ═══════════════════════════════════════════════════════

def task1_equivariance(surjections, uf, n, p):
    print(f"\n{'='*70}")
    print("TASK 1: Equivariance vectors in complement-touching GL-orbits")
    print(f"{'='*70}")

    N = 1 << n
    ones = N - 1

    # Identify complement-respecting surjections (w.r.t. 111)
    def is_comp_resp_111(f):
        for x in range(N // 2):
            if (f[x] + f[x ^ ones]) % p != 0:
                return False
        return True

    comp_flags = [is_comp_resp_111(f) for f in surjections]

    # Get orbits
    comps = uf.components()
    orbit_list = []
    for root, indices in comps.items():
        n_comp = sum(1 for i in indices if comp_flags[i])
        orbit_list.append((len(indices), n_comp, indices))
    orbit_list.sort(key=lambda x: (-x[0], -x[1]))

    # Complement-touching orbits
    comp_orbits = [(size, n_comp, indices) for size, n_comp, indices in orbit_list if n_comp > 0]

    print(f"\n  {len(comp_orbits)} complement-touching orbits found\n")

    for oi, (size, n_comp, indices) in enumerate(comp_orbits):
        print(f"  Orbit {oi+1}: size={size}, comp-resp(111)={n_comp}")

        # For EVERY surjection in this orbit, find equivariant vectors
        eq_counts = Counter()  # how many surjections have each # of equivariant vectors
        vec_counts = Counter()  # how many surjections are equivariant w.r.t. each vector

        for idx in indices:
            f = surjections[idx]
            vecs = equivariant_vectors(f, n, p)
            eq_counts[len(vecs)] += 1
            for v in vecs:
                vec_counts[v] += 1

        print(f"    # equivariant vectors per surjection: {dict(eq_counts)}")
        print(f"    Vector usage (how many surjections are equiv w.r.t. each v):")
        for v in sorted(vec_counts.keys()):
            print(f"      v={vec_str(v, n)}: {vec_counts[v]} surjections "
                  f"({vec_counts[v]/size*100:.1f}%)")

        # Check: does each surjection have exactly 1 equivariant vector?
        if set(eq_counts.keys()) == {1}:
            print(f"    ✓ Every surjection equivariant w.r.t. exactly 1 vector")
        elif set(eq_counts.keys()) == {0}:
            print(f"    ✗ No surjection has any equivariant vector!")
        else:
            print(f"    Mixed: some have {min(eq_counts.keys())}, "
                  f"some have {max(eq_counts.keys())}")

        # Check: all 7 vectors appear equally?
        if len(vec_counts) == N - 1:
            vals = list(vec_counts.values())
            if len(set(vals)) == 1:
                print(f"    ✓ All {N-1} nonzero vectors appear equally ({vals[0]} each)")
            else:
                print(f"    All {N-1} vectors present but unequal: "
                      f"{dict(Counter(vals))}")
        else:
            print(f"    Only {len(vec_counts)}/{N-1} vectors present")
        print()


# ═══════════════════════════════════════════════════════
# Task 2: Fiber partitions of non-complement-touching orbits
# ═══════════════════════════════════════════════════════

def task2_fiber_partitions(surjections, uf, n, p):
    print(f"\n{'='*70}")
    print("TASK 2: Fiber partitions of non-complement-touching orbits")
    print(f"{'='*70}")

    N = 1 << n
    ones = N - 1

    def is_comp_resp_111(f):
        for x in range(N // 2):
            if (f[x] + f[x ^ ones]) % p != 0:
                return False
        return True

    comp_flags = [is_comp_resp_111(f) for f in surjections]

    comps = uf.components()
    orbit_list = []
    for root, indices in comps.items():
        n_comp = sum(1 for i in indices if comp_flags[i])
        orbit_list.append((len(indices), n_comp, indices))

    # Non-complement-touching orbits
    non_comp_orbits = [(size, indices) for size, n_comp, indices in orbit_list if n_comp == 0]

    print(f"\n  {len(non_comp_orbits)} non-complement-touching orbits")

    # For each orbit, compute fiber partition of one representative
    # (fiber partition is invariant under GL × Aut action? 
    #  GL permutes domain → preserves fiber sizes. Aut permutes codomain → preserves fiber sizes.
    #  So yes, fiber partition is an orbit invariant.)
    partition_to_orbits = defaultdict(list)
    for size, indices in non_comp_orbits:
        rep = surjections[indices[0]]
        fp = fiber_partition(rep, p)
        partition_to_orbits[fp].append(size)

    print(f"\n  Distinct fiber partitions: {len(partition_to_orbits)}\n")
    print(f"  {'Partition':<25} {'#Orbits':<10} {'Orbit sizes':<30}")
    print(f"  {'-'*65}")
    for fp in sorted(partition_to_orbits.keys(), key=lambda x: (-x[0], -len(x))):
        orbits = partition_to_orbits[fp]
        size_dist = dict(Counter(orbits))
        print(f"  {str(fp):<25} {len(orbits):<10} {size_dist}")

    return partition_to_orbits


# ═══════════════════════════════════════════════════════
# Task 3: {2,2,2,1,1} partition without equivariance
# ═══════════════════════════════════════════════════════

def task3_partition_without_equivariance(surjections, uf, n, p):
    print(f"\n{'='*70}")
    print("TASK 3: Surjections with partition {2,2,2,1,1} but no equivariance")
    print(f"{'='*70}")

    N = 1 << n
    target_partition = (2, 2, 2, 1, 1)

    # Find all surjections with this partition
    matching = []
    for idx, f in enumerate(surjections):
        if fiber_partition(f, p) == target_partition:
            matching.append(idx)

    print(f"\n  Surjections with partition {target_partition}: {len(matching)}")

    # For each, check equivariance w.r.t. any vector
    has_equiv = 0
    no_equiv = 0
    equiv_vec_counts = Counter()  # number of equivariant vectors

    for idx in matching:
        f = surjections[idx]
        vecs = equivariant_vectors(f, n, p)
        equiv_vec_counts[len(vecs)] += 1
        if vecs:
            has_equiv += 1
        else:
            no_equiv += 1

    print(f"  With equivariance (≥1 vector): {has_equiv}")
    print(f"  Without equivariance (0 vectors): {no_equiv}")
    print(f"  Distribution of #equiv vectors: {dict(equiv_vec_counts)}")

    if no_equiv > 0:
        print(f"\n  ⚠ {no_equiv} surjections have partition {target_partition} "
              f"but NO equivariant vector!")
        # Show an example
        for idx in matching:
            f = surjections[idx]
            if not equivariant_vectors(f, n, p):
                print(f"    Example: f = {f}")
                # Show the fiber structure
                fibers = defaultdict(list)
                for x in range(N):
                    fibers[f[x]].append(vec_str(x, n))
                for val in sorted(fibers.keys()):
                    print(f"      f⁻¹({val}) = {fibers[val]}")
                # Check what structure the size-2 fibers have
                pairs = [(val, fibers[val]) for val in fibers if len(fibers[val]) == 2]
                print(f"    Size-2 fibers:")
                for val, elems in pairs:
                    x1 = int(elems[0], 2)
                    x2 = int(elems[1], 2)
                    diff = x1 ^ x2
                    print(f"      f⁻¹({val}) = {elems}, XOR diff = {vec_str(diff, n)}")
                break
    else:
        print(f"\n  ✓ Every surjection with partition {target_partition} has ≥1 equivariant vector.")
        print(f"    The partition {target_partition} FORCES equivariance (at (3,5)).")


# ═══════════════════════════════════════════════════════
# Task 4: Fiber partition count vs orbit count
# ═══════════════════════════════════════════════════════

def task4_partition_diversity(cases):
    """Count distinct fiber partitions at each (n,p) and correlate with orbit counts."""
    print(f"\n{'='*70}")
    print("TASK 4: Fiber partition diversity and orbit count non-monotonicity")
    print(f"{'='*70}")

    # Orbit counts from Phase 2 (Burnside)
    # Recompute just the partition counts, not full orbits
    from math import comb

    def surjection_count_ie(N, p):
        return sum((-1)**k * comb(p, k) * (p - k)**N for k in range(p + 1))

    # For orbit counts, use known values from Phase 2
    known_orbits = {(3, 3): 63, (3, 5): 245, (3, 7): 142}

    results = {}
    for n, p in cases:
        N = 1 << n
        t0 = time.time()

        # Enumerate surjections and compute partition distribution
        surj_count = surjection_count_ie(N, p)
        print(f"\n  (n={n}, p={p}): {surj_count} surjections")

        partition_counts = Counter()
        for f in product(range(p), repeat=N):
            if len(set(f)) == p:
                fp = fiber_partition(f, p)
                partition_counts[fp] += 1

        elapsed = time.time() - t0
        n_partitions = len(partition_counts)
        orbits = known_orbits.get((n, p), "?")

        print(f"    Distinct fiber partitions: {n_partitions}")
        print(f"    GL-orbits: {orbits}")
        print(f"    [{elapsed:.1f}s]")

        print(f"    Partition distribution:")
        for fp in sorted(partition_counts.keys(), key=lambda x: -partition_counts[x]):
            print(f"      {str(fp):<25} {partition_counts[fp]:>8} surjections "
                  f"({partition_counts[fp]/surj_count*100:.1f}%)")

        results[(n, p)] = {
            'n_partitions': n_partitions,
            'orbits': orbits,
            'partition_counts': partition_counts,
            'surj_count': surj_count
        }

    # Summary comparison
    print(f"\n  {'─'*50}")
    print(f"  {'(n,p)':<10} {'#Partitions':<15} {'#Orbits':<10} {'Ratio':<10}")
    print(f"  {'─'*50}")
    for n, p in cases:
        r = results[(n, p)]
        ratio = r['orbits'] / r['n_partitions'] if isinstance(r['orbits'], int) else "?"
        print(f"  ({n},{p}){'':<5} {r['n_partitions']:<15} {str(r['orbits']):<10} "
              f"{ratio if isinstance(ratio, str) else f'{ratio:.1f}':<10}")

    return results


# ═══════════════════════════════════════════════════════
# Also: broader equivariance analysis for ALL orbits
# ═══════════════════════════════════════════════════════

def task2b_equivariance_in_all_orbits(surjections, uf, n, p):
    """For each orbit: what fraction of surjections has at least one equivariant vector?"""
    print(f"\n{'='*70}")
    print("TASK 2b: Equivariance presence across ALL orbits")
    print(f"{'='*70}")

    N = 1 << n
    comps = uf.components()

    # For each orbit, check a few representatives for equivariance
    # (Equivariance w.r.t. some vector is NOT necessarily an orbit invariant under GL × Aut,
    #  because GL moves vectors around. But within an orbit, if one surjection has
    #  equivariance w.r.t. v, then another surjection (obtained by applying A)
    #  has equivariance w.r.t. Av. So having-any-equivariance IS an orbit invariant.)

    has_equiv_count = 0
    no_equiv_count = 0

    for root, indices in comps.items():
        # Check representative
        f = surjections[indices[0]]
        vecs = equivariant_vectors(f, n, p)
        if vecs:
            has_equiv_count += 1
        else:
            no_equiv_count += 1

    print(f"\n  Total orbits: {has_equiv_count + no_equiv_count}")
    print(f"  Orbits with equivariance (any vector): {has_equiv_count}")
    print(f"  Orbits without any equivariance: {no_equiv_count}")

    # Also check: among orbits WITH equivariance, how many equivariant vectors
    # does each orbit's surjections have?
    print(f"\n  Detail for orbits WITH equivariance:")
    eq_orbit_data = []
    for root, indices in comps.items():
        f = surjections[indices[0]]
        vecs = equivariant_vectors(f, n, p)
        if vecs:
            fp = fiber_partition(f, p)
            eq_orbit_data.append((len(indices), len(vecs), fp))

    eq_orbit_data.sort(key=lambda x: (-x[0], -x[1]))
    print(f"  {'Size':<8} {'#EqVecs':<10} {'Partition':<25}")
    print(f"  {'-'*43}")
    for size, n_vecs, fp in eq_orbit_data:
        print(f"  {size:<8} {n_vecs:<10} {fp}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    n, p = 3, 5
    N = 1 << n

    print("Phase 3: Internal structure of GL-orbits at (3,5)")
    print("=" * 70)

    # Enumerate surjections
    t0 = time.time()
    surjections = enumerate_surjections(n, p)
    print(f"Enumerated {len(surjections)} surjections [{time.time()-t0:.1f}s]")

    # Build orbit partition
    t0 = time.time()
    uf = build_orbit_partition(n, p, surjections)
    comps = uf.components()
    print(f"Built {len(comps)} orbits [{time.time()-t0:.1f}s]")

    # Task 1: Equivariance in complement-touching orbits
    task1_equivariance(surjections, uf, n, p)

    # Task 2: Fiber partitions of non-complement-touching orbits
    partition_data = task2_fiber_partitions(surjections, uf, n, p)

    # Task 2b: Broader equivariance analysis
    task2b_equivariance_in_all_orbits(surjections, uf, n, p)

    # Task 3: Partition {2,2,2,1,1} without equivariance
    task3_partition_without_equivariance(surjections, uf, n, p)

    # Task 4: Partition diversity
    task4_results = task4_partition_diversity([(3, 3), (3, 5), (3, 7)])

    # ═══════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════
    print(f"\n\n{'='*70}")
    print("SUMMARY OF FINDINGS")
    print(f"{'='*70}")
    print("""
Key questions answered:
1. Do complement-touching orbit surjections have equivariance w.r.t. exactly 1 vector?
2. What fiber partitions exist in the non-complement-touching orbits?
3. Does partition {2,2,2,1,1} force equivariance?
4. Does partition diversity explain the non-monotone orbit count in p?
""")
