#!/usr/bin/env python3
"""Phase 4: Equivariance landscape across (3,p) and alternative GL-invariant properties.

Task A: Complete equivariance table at (3,3), (3,5), (3,7).
Task B: Test alternative GL-invariant properties at (3,5):
  1. Fiber-partition orbit counts (already known, tabulate)
  2. Affine equivariance: f(x⊕v) = α·f(x) for (v,α) pairs
  3. Translation equivariance: f(x⊕v) = f(x) + c for (v,c) pairs
"""

from itertools import product
from collections import Counter, defaultdict
import time

# ═══════════════════════════════════════════════════════
# F₂ helpers
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

def vec_str(v, n):
    return format(v, f'0{n}b')


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


def fiber_partition(f, p):
    counts = Counter(f)
    return tuple(sorted(counts.values(), reverse=True))


# ═══════════════════════════════════════════════════════
# Equivariance tests
# ═══════════════════════════════════════════════════════

def negation_equivariant_vectors(f, n, p):
    """Vectors v s.t. f(x⊕v) = −f(x) mod p for all x."""
    N = 1 << n
    result = []
    for v in range(1, N):
        ok = True
        for x in range(N):
            if (f[x] + f[x ^ v]) % p != 0:
                ok = False
                break
        if ok:
            result.append(v)
    return result


def scaling_equivariant_pairs(f, n, p):
    """Return list of (v, α) pairs where f(x⊕v) = α·f(x) mod p for all x.
    v ≠ 0, α ∈ {1,...,p-1} (α=0 excluded: would force f=0)."""
    N = 1 << n
    result = []
    for v in range(1, N):
        for alpha in range(1, p):
            ok = True
            for x in range(N):
                if f[x ^ v] != (alpha * f[x]) % p:
                    ok = False
                    break
            if ok:
                result.append((v, alpha))
    return result


def translation_equivariant_pairs(f, n, p):
    """Return list of (v, c) pairs where f(x⊕v) = f(x) + c mod p for all x.
    v ≠ 0, c ∈ {0,...,p-1}."""
    N = 1 << n
    result = []
    for v in range(1, N):
        # c is determined by any x: c = f(x⊕v) − f(x) mod p
        # Check if this c is consistent for all x
        c = (f[0 ^ v] - f[0]) % p
        ok = True
        for x in range(1, N):
            if (f[x ^ v] - f[x]) % p != c:
                ok = False
                break
        if ok:
            result.append((v, c))
    return result


# ═══════════════════════════════════════════════════════
# Task A: Equivariance table across (3,p)
# ═══════════════════════════════════════════════════════

def task_a():
    print(f"{'='*70}")
    print("TASK A: Negation-equivariance table across (3,p)")
    print(f"{'='*70}")

    n = 3
    results = {}

    for p in [3, 5, 7]:
        print(f"\n  Computing (n={n}, p={p})...")
        t0 = time.time()

        surjections = enumerate_surjections(n, p)
        t_enum = time.time() - t0
        print(f"    {len(surjections)} surjections [{t_enum:.1f}s]")

        t0 = time.time()
        uf = build_orbit_partition(n, p, surjections)
        comps = uf.components()
        t_uf = time.time() - t0
        print(f"    {len(comps)} orbits [{t_uf:.1f}s]")

        # Test negation equivariance for each surjection
        t0 = time.time()
        equiv_flags = []
        for f in surjections:
            vecs = negation_equivariant_vectors(f, n, p)
            equiv_flags.append(len(vecs))
        t_eq = time.time() - t0

        total_equiv = sum(1 for e in equiv_flags if e > 0)
        print(f"    Equivariant: {total_equiv} / {len(surjections)} "
              f"({total_equiv/len(surjections)*100:.2f}%) [{t_eq:.1f}s]")

        # Distribution of #equiv vectors per surjection
        vec_dist = Counter(equiv_flags)
        print(f"    #Equiv vectors distribution: {dict(vec_dist)}")

        # How many GL-orbits do the equivariant surjections span?
        equiv_orbit_roots = set()
        for idx, e in enumerate(equiv_flags):
            if e > 0:
                equiv_orbit_roots.add(uf.find(idx))
        n_equiv_orbits = len(equiv_orbit_roots)

        # Orbit sizes for equivariant orbits
        equiv_orbit_sizes = sorted(
            [len(comps[r]) for r in equiv_orbit_roots], reverse=True)

        print(f"    Equivariant orbits: {n_equiv_orbits} / {len(comps)}")
        print(f"    Equivariant orbit sizes: {equiv_orbit_sizes}")

        results[p] = {
            'total': len(surjections),
            'equiv': total_equiv,
            'frac': total_equiv / len(surjections),
            'equiv_orbits': n_equiv_orbits,
            'total_orbits': len(comps),
            'equiv_orbit_sizes': equiv_orbit_sizes,
            'vec_dist': dict(vec_dist),
        }

    # Summary table
    print(f"\n  {'─'*65}")
    print(f"  {'(n,p)':<8} {'total':<10} {'equivariant':<12} {'frac':<8} "
          f"{'eq orbits':<12} {'total orbits':<12}")
    print(f"  {'─'*65}")
    for p in [3, 5, 7]:
        r = results[p]
        print(f"  (3,{p}){'':<3} {r['total']:<10} {r['equiv']:<12} "
              f"{r['frac']*100:.2f}%{'':<2} {r['equiv_orbits']:<12} "
              f"{r['total_orbits']:<12}")

    # The 1/7 structure: equiv/total should equal
    # complement_respecting × 7 / total = 7 × (complement count) / total
    print(f"\n  Verification: equivariant count = 7 × complement-respecting count?")
    for p in [3, 5, 7]:
        r = results[p]
        # Complement-respecting = equiv/7 (since each equivariant surjection
        # is equivariant w.r.t. exactly 1 vector, and GL distributes equally)
        comp_resp = r['equiv'] // 7
        print(f"    (3,{p}): {r['equiv']} / 7 = {comp_resp} complement-respecting")

    return results


# ═══════════════════════════════════════════════════════
# Task B: Alternative GL-invariant properties at (3,5)
# ═══════════════════════════════════════════════════════

def task_b():
    print(f"\n\n{'='*70}")
    print("TASK B: Alternative GL-invariant properties at (3,5)")
    print(f"{'='*70}")

    n, p = 3, 5
    N = 1 << n

    print(f"\n  Enumerating surjections...")
    surjections = enumerate_surjections(n, p)
    print(f"  {len(surjections)} surjections")

    print(f"  Building orbit partition...")
    uf = build_orbit_partition(n, p, surjections)
    comps = uf.components()
    print(f"  {len(comps)} orbits")

    # ── B1: Fiber partition orbit counts ──
    print(f"\n  {'─'*60}")
    print(f"  B1: Orbit counts by fiber partition")
    print(f"  {'─'*60}")

    partition_orbits = defaultdict(set)
    partition_surj_count = Counter()
    for idx, f in enumerate(surjections):
        fp = fiber_partition(f, p)
        partition_surj_count[fp] += 1
        partition_orbits[fp].add(uf.find(idx))

    for fp in sorted(partition_orbits.keys(), key=lambda x: -partition_surj_count[x]):
        n_orb = len(partition_orbits[fp])
        n_surj = partition_surj_count[fp]
        print(f"    {str(fp):<25} {n_surj:>6} surjections, {n_orb:>3} orbits")

    # ── B2: Affine equivariance (scaling) ──
    print(f"\n  {'─'*60}")
    print(f"  B2: Scaling equivariance f(x⊕v) = α·f(x)")
    print(f"  {'─'*60}")
    print(f"  Testing all (v, α) pairs: v ∈ F₂³\\{{0}}, α ∈ {{1,2,3,4}}")
    print(f"  Note: α=4≡−1 mod 5 is the complement/negation case")
    print()

    t0 = time.time()
    # For each surjection, find all (v, α) pairs
    # Track by α value
    alpha_surj_sets = defaultdict(set)     # α → set of surjection indices
    pair_counts = Counter()                 # (v,α) → count of surjections
    n_vecs_per_alpha = defaultdict(Counter) # α → distribution of #vecs per surj

    for idx, f in enumerate(surjections):
        pairs = scaling_equivariant_pairs(f, n, p)
        seen_alphas = set()
        for v, alpha in pairs:
            alpha_surj_sets[alpha].add(idx)
            pair_counts[(v, alpha)] += 1
            seen_alphas.add(alpha)
        for alpha in range(1, p):
            n_vecs = sum(1 for v, a in pairs if a == alpha)
            n_vecs_per_alpha[alpha][n_vecs] += 1

    elapsed = time.time() - t0
    print(f"  [{elapsed:.1f}s]")

    # Report by α
    print(f"\n  Per-α summary:")
    print(f"  {'α':<5} {'α mod p':<10} {'#surj with ≥1':<15} {'fraction':<10} "
          f"{'#vecs distribution'}")
    print(f"  {'─'*70}")
    for alpha in range(1, p):
        n_with = len(alpha_surj_sets[alpha])
        frac = n_with / len(surjections)
        # What is α in terms of negation?
        label = ""
        if alpha == 1:
            label = "(identity)"
        elif alpha == p - 1:
            label = "(negation = −1)"
        else:
            label = f"(order {next(k for k in range(1, p) if pow(alpha, k, p) == 1)})"
        dist = dict(sorted(n_vecs_per_alpha[alpha].items()))
        nonzero_dist = {k: v for k, v in dist.items() if k > 0}
        print(f"  {alpha:<5} {label:<18} {n_with:<15} {frac*100:.2f}%{'':<4} "
              f"{nonzero_dist if nonzero_dist else '—'}")

    # Orbits spanned by each α
    print(f"\n  GL-orbits spanned by surjections with each α:")
    for alpha in range(1, p):
        orbit_roots = {uf.find(idx) for idx in alpha_surj_sets[alpha]}
        if orbit_roots:
            orbit_sizes = sorted([len(comps[r]) for r in orbit_roots], reverse=True)
            print(f"    α={alpha}: {len(orbit_roots)} orbits, sizes={orbit_sizes}")
        else:
            print(f"    α={alpha}: 0 orbits")

    # Key comparison: is α=−1 special?
    print(f"\n  Is α=−1 (negation) special?")
    for alpha in range(1, p):
        n_with = len(alpha_surj_sets[alpha])
        print(f"    α={alpha}: {n_with} surjections "
              f"({n_with/len(surjections)*100:.2f}%)")

    # ── B3: Translation equivariance ──
    print(f"\n  {'─'*60}")
    print(f"  B3: Translation equivariance f(x⊕v) = f(x) + c")
    print(f"  {'─'*60}")
    print(f"  Testing all v ∈ F₂³\\{{0}}")
    print()

    t0 = time.time()
    trans_surj_set = set()  # surjections with any translation equivariance
    c_counts = Counter()    # c value → count

    for idx, f in enumerate(surjections):
        pairs = translation_equivariant_pairs(f, n, p)
        if pairs:
            trans_surj_set.add(idx)
            for v, c in pairs:
                c_counts[c] += 1

    elapsed = time.time() - t0
    n_trans = len(trans_surj_set)
    print(f"  Surjections with translation equivariance: {n_trans} / {len(surjections)} "
          f"({n_trans/len(surjections)*100:.2f}%) [{elapsed:.1f}s]")

    # Orbits
    trans_orbit_roots = {uf.find(idx) for idx in trans_surj_set}
    trans_orbit_sizes = sorted([len(comps[r]) for r in trans_orbit_roots], reverse=True)
    print(f"  GL-orbits spanned: {len(trans_orbit_roots)}")
    print(f"  Orbit sizes: {trans_orbit_sizes}")

    # c distribution
    print(f"  Translation constant c distribution:")
    for c in sorted(c_counts.keys()):
        print(f"    c={c}: {c_counts[c]} (v,surj) pairs")

    # Check overlap with scaling equivariance
    neg_set = alpha_surj_sets.get(p - 1, set())
    overlap = trans_surj_set & neg_set
    print(f"\n  Overlap with negation equivariance: {len(overlap)}")
    print(f"  Translation-only (no negation): {len(trans_surj_set - neg_set)}")
    print(f"  Negation-only (no translation): {len(neg_set - trans_surj_set)}")

    # Any surjection with BOTH translation AND scaling equivariance?
    any_scaling = set()
    for alpha_set in alpha_surj_sets.values():
        any_scaling |= alpha_set
    both = trans_surj_set & any_scaling
    print(f"  Has both translation AND scaling: {len(both)}")

    # ── Grand comparison ──
    print(f"\n\n  {'='*60}")
    print(f"  GRAND COMPARISON: GL-invariant properties at (3,5)")
    print(f"  {'='*60}")

    print(f"\n  {'Property':<35} {'#Surj':<10} {'%':<8} {'#Orbits':<10}")
    print(f"  {'─'*63}")
    print(f"  {'All surjections':<35} {len(surjections):<10} {'100%':<8} "
          f"{len(comps):<10}")
    for fp in sorted(partition_orbits.keys(), key=lambda x: -partition_surj_count[x]):
        n_orb = len(partition_orbits[fp])
        n_surj = partition_surj_count[fp]
        print(f"  {'  partition=' + str(fp):<35} {n_surj:<10} "
              f"{n_surj/len(surjections)*100:.1f}%{'':<2} {n_orb:<10}")

    for alpha in range(1, p):
        n_with = len(alpha_surj_sets[alpha])
        if n_with == 0:
            continue
        orbit_roots = {uf.find(idx) for idx in alpha_surj_sets[alpha]}
        label = f"scaling α={alpha}"
        if alpha == p - 1:
            label += " (negation)"
        elif alpha == 1:
            label += " (identity)"
        print(f"  {'  ' + label:<35} {n_with:<10} "
              f"{n_with/len(surjections)*100:.2f}%{'':<1} {len(orbit_roots):<10}")

    neg_n = len(neg_set)
    neg_orbits = len({uf.find(idx) for idx in neg_set})
    print(f"  {'  negation (any v)':<35} {neg_n:<10} "
          f"{neg_n/len(surjections)*100:.2f}%{'':<1} {neg_orbits:<10}")

    print(f"  {'  translation (any v,c)':<35} {n_trans:<10} "
          f"{n_trans/len(surjections)*100:.2f}%{'':<1} {len(trans_orbit_roots):<10}")

    # Verdict
    print(f"\n  VERDICT:")
    # Check if negation is uniquely thin
    scaling_counts = {alpha: len(alpha_surj_sets[alpha]) for alpha in range(1, p)}
    nonzero_scaling = {a: c for a, c in scaling_counts.items() if c > 0}
    if len(nonzero_scaling) == 1 and (p - 1) in nonzero_scaling:
        print(f"  → Only α=−1 (negation) produces scaling-equivariant surjections.")
        print(f"  → Negation IS distinguished among all automorphisms.")
    elif all(c == scaling_counts.get(p - 1, 0) for c in nonzero_scaling.values()):
        print(f"  → All α values produce the SAME number of equivariant surjections.")
        print(f"  → Negation is NOT distinguished; the equivariance structure is α-uniform.")
    else:
        print(f"  → Different α values produce different counts:")
        for a, c in sorted(nonzero_scaling.items()):
            print(f"       α={a}: {c}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Phase 4: Equivariance Landscape")
    print("=" * 70)

    task_a_results = task_a()
    task_b()
