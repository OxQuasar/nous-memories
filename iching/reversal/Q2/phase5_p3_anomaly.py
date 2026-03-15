#!/usr/bin/env python3
"""Phase 5: The (3,3) anomaly — double equivariance and the non-singleton-forcing regime.

At (3,3), 84 surjections are equivariant w.r.t. 2 vectors simultaneously.
This is impossible at (3,5) where α²≡1 forces exactly 1 vector.
At p=3, the regime p ≤ 2^{n-1} = 4 allows richer symmetry.

Tasks:
1. Double-equivariance analysis: vector sets, subspace structure, v₁⊕v₂ test
2. Scaling equivariance at (3,3): α=1 (identity) vs α=2 (negation=-1 mod 3)
3. GL-orbit structure of equivariant subset
4. Rigidity within the double-equivariant sub-class
"""

from itertools import product
from collections import Counter, defaultdict
import time

# ═══════════════════════════════════════════════════════
# Core helpers (same as prior phases)
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

def fiber_partition(f, p):
    counts = Counter(f)
    return tuple(sorted(counts.values(), reverse=True))


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
        if rx == ry: return
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
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
            if i == j: continue
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


# ═══════════════════════════════════════════════════════
# Equivariance helpers
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


def scaling_equivariant_by_alpha(f, n, p, alpha):
    """Vectors v s.t. f(x⊕v) = α·f(x) mod p for all x."""
    N = 1 << n
    result = []
    for v in range(1, N):
        ok = True
        for x in range(N):
            if f[x ^ v] != (alpha * f[x]) % p:
                ok = False
                break
        if ok:
            result.append(v)
    return result


def translation_equivariant_vectors(f, n, p):
    """Return list of (v, c) where f(x⊕v) = f(x)+c mod p for all x, v≠0."""
    N = 1 << n
    result = []
    for v in range(1, N):
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
# Task 1: Double-equivariance analysis
# ═══════════════════════════════════════════════════════

def task1(surjections, n, p):
    print(f"\n{'='*70}")
    print("TASK 1: Double-equivariance analysis at (3,3)")
    print(f"{'='*70}")

    N = 1 << n

    # For each surjection, compute negation-equivariant vectors
    equiv_data = []  # (idx, vector_set)
    for idx, f in enumerate(surjections):
        vecs = negation_equivariant_vectors(f, n, p)
        if vecs:
            equiv_data.append((idx, frozenset(vecs)))

    print(f"\n  Total equivariant surjections: {len(equiv_data)}")

    # Distribution by number of vectors
    vec_count_dist = Counter(len(vs) for _, vs in equiv_data)
    print(f"  #Vectors distribution: {dict(sorted(vec_count_dist.items()))}")

    # What are the actual vector sets?
    vec_set_dist = Counter(vs for _, vs in equiv_data)
    print(f"\n  Distinct vector sets: {len(vec_set_dist)}")
    print(f"  {'Vector set':<35} {'Count':<8} {'Vectors (binary)'}")
    print(f"  {'-'*65}")
    for vs, count in vec_set_dist.most_common():
        vs_strs = [vec_str(v, n) for v in sorted(vs)]
        print(f"  {str(set(sorted(vs))):<35} {count:<8} {vs_strs}")

    # For double-equivariant: check v₁⊕v₂
    print(f"\n  Double-equivariant analysis:")
    double_equiv = [(idx, vs) for idx, vs in equiv_data if len(vs) == 2]
    print(f"  {len(double_equiv)} surjections with exactly 2 equivariance vectors")

    if double_equiv:
        # Check: does v₁⊕v₂ always equal a third specific vector?
        xor_products = Counter()
        for idx, vs in double_equiv:
            vlist = sorted(vs)
            v3 = vlist[0] ^ vlist[1]
            xor_products[v3] += 1

        print(f"\n  v₁ ⊕ v₂ distribution:")
        for v3, count in xor_products.most_common():
            print(f"    v₁⊕v₂ = {vec_str(v3, n)}: {count} surjections")

        # Is v₃ = v₁⊕v₂ also an equivariance vector?
        triple_count = 0
        for idx, vs in double_equiv:
            vlist = sorted(vs)
            v3 = vlist[0] ^ vlist[1]
            if v3 in vs:
                triple_count += 1
        print(f"\n  Is v₁⊕v₂ also in the equivariance set? "
              f"{triple_count}/{len(double_equiv)}")

        # Check if f(x⊕v₃) = −f(x) for these surjections
        # (It might be that v₃ gives f(x⊕v₃) = f(x) instead of −f(x))
        print(f"\n  Checking what v₃ = v₁⊕v₂ does:")
        for idx, vs in double_equiv[:3]:  # first 3 examples
            f = surjections[idx]
            vlist = sorted(vs)
            v3 = vlist[0] ^ vlist[1]
            # Test f(x⊕v₃) = ? · f(x)
            for alpha in range(p):
                ok = True
                for x in range(N):
                    if f[x ^ v3] != (alpha * f[x]) % p:
                        ok = False
                        break
                if ok:
                    print(f"    f[{idx}]: v₁={vec_str(vlist[0],n)}, v₂={vec_str(vlist[1],n)}, "
                          f"v₃=v₁⊕v₂={vec_str(v3,n)}: f(x⊕v₃) = {alpha}·f(x)")
                    break
            else:
                # Check translation
                c = (f[0 ^ v3] - f[0]) % p
                ok = all((f[x ^ v3] - f[x]) % p == c for x in range(N))
                if ok:
                    print(f"    f[{idx}]: v₁={vec_str(vlist[0],n)}, v₂={vec_str(vlist[1],n)}, "
                          f"v₃=v₁⊕v₂={vec_str(v3,n)}: f(x⊕v₃) = f(x) + {c}")
                else:
                    print(f"    f[{idx}]: v₃={vec_str(v3,n)}: no simple relation")

    # Any surjections with 3+ equivariance vectors?
    triple_plus = [(idx, vs) for idx, vs in equiv_data if len(vs) >= 3]
    if triple_plus:
        print(f"\n  ⚠ {len(triple_plus)} surjections with 3+ equivariance vectors!")
        for idx, vs in triple_plus[:3]:
            print(f"    f[{idx}]: vectors = {[vec_str(v,n) for v in sorted(vs)]}")
    else:
        print(f"\n  ✓ No surjection has 3+ equivariance vectors")

    return equiv_data


# ═══════════════════════════════════════════════════════
# Task 2: Scaling equivariance at (3,3) — α=1 vs α=2
# ═══════════════════════════════════════════════════════

def task2(surjections, n, p):
    print(f"\n{'='*70}")
    print("TASK 2: Scaling equivariance at (3,3): α=1 (identity) vs α=2 (negation)")
    print(f"{'='*70}")

    N = 1 << n

    # For each surjection, find scaling-equivariant vectors for each α
    alpha1_data = []  # (idx, vectors for α=1)
    alpha2_data = []  # (idx, vectors for α=2=-1 mod 3)

    for idx, f in enumerate(surjections):
        v1 = scaling_equivariant_by_alpha(f, n, p, 1)  # identity
        v2 = scaling_equivariant_by_alpha(f, n, p, 2)  # negation
        if v1:
            alpha1_data.append((idx, frozenset(v1)))
        if v2:
            alpha2_data.append((idx, frozenset(v2)))

    print(f"\n  α=1 (identity) equivariant: {len(alpha1_data)} surjections")
    print(f"  α=2 (negation) equivariant: {len(alpha2_data)} surjections")

    # Distribution of #vectors for each
    for alpha, data, label in [(1, alpha1_data, "identity"), (2, alpha2_data, "negation")]:
        dist = Counter(len(vs) for _, vs in data)
        print(f"\n  α={alpha} ({label}): #vectors distribution = {dict(sorted(dist.items()))}")

        # What vector sets appear?
        vset_dist = Counter(vs for _, vs in data)
        print(f"  Distinct vector sets: {len(vset_dist)}")
        for vs, count in vset_dist.most_common():
            print(f"    {[vec_str(v,n) for v in sorted(vs)]}: {count} surjections")

    # Cross-analysis: can a surjection have α=1 w.r.t. one vector and α=2 w.r.t. another?
    idx1 = {idx for idx, _ in alpha1_data}
    idx2 = {idx for idx, _ in alpha2_data}
    both = idx1 & idx2

    print(f"\n  Cross-analysis:")
    print(f"    α=1 only: {len(idx1 - idx2)}")
    print(f"    α=2 only: {len(idx2 - idx1)}")
    print(f"    BOTH α=1 and α=2: {len(both)}")

    if both:
        print(f"\n  Surjections with both α=1 and α=2 equivariance:")
        a1_dict = {idx: vs for idx, vs in alpha1_data}
        a2_dict = {idx: vs for idx, vs in alpha2_data}
        for idx in sorted(both)[:5]:
            v1s = [vec_str(v, n) for v in sorted(a1_dict[idx])]
            v2s = [vec_str(v, n) for v in sorted(a2_dict[idx])]
            f = surjections[idx]
            fp = fiber_partition(f, p)
            print(f"    f[{idx}] = {f}")
            print(f"      partition: {fp}")
            print(f"      α=1 vectors: {v1s}")
            print(f"      α=2 vectors: {v2s}")

    # Also check translation equivariance at (3,3)
    print(f"\n  Translation equivariance f(x⊕v) = f(x)+c:")
    trans_count = 0
    trans_data = []
    for idx, f in enumerate(surjections):
        pairs = translation_equivariant_vectors(f, n, p)
        if pairs:
            trans_count += 1
            trans_data.append((idx, pairs))

    print(f"  {trans_count} surjections with translation equivariance")
    if trans_data:
        c_dist = Counter()
        for idx, pairs in trans_data:
            for v, c in pairs:
                c_dist[c] += 1
        print(f"  Translation constant c distribution: {dict(sorted(c_dist.items()))}")

        # Show examples
        for idx, pairs in trans_data[:3]:
            f = surjections[idx]
            print(f"    f[{idx}] = {f}, partition={fiber_partition(f,p)}")
            for v, c in pairs:
                print(f"      v={vec_str(v,n)}, c={c}")

    # Combined: what is the complete equivariance signature of each surjection?
    # For each surjection, compute: set of (v, type) where type ∈ {neg, id, trans_c}
    print(f"\n  Complete equivariance signature analysis:")
    sig_counter = Counter()
    for idx, f in enumerate(surjections):
        sig = []
        for v in range(1, N):
            # Check negation
            if all((f[x] + f[x ^ v]) % p == 0 for x in range(N)):
                sig.append((v, 'neg'))
            # Check identity
            elif all(f[x ^ v] == f[x] for x in range(N)):
                sig.append((v, 'id'))
            else:
                # Check translation
                c = (f[0 ^ v] - f[0]) % p
                if c != 0 and all((f[x ^ v] - f[x]) % p == c for x in range(N)):
                    sig.append((v, f'tr{c}'))

        if sig:
            # Normalize: sort by vector
            sig_key = tuple(sorted(sig))
            sig_counter[sig_key] += 1

    print(f"  Distinct equivariance signatures: {len(sig_counter)}")
    for sig, count in sig_counter.most_common():
        sig_str = ", ".join(f"v={vec_str(v,n)}:{typ}" for v, typ in sig)
        print(f"    [{sig_str}]: {count} surjections")

    return alpha1_data, alpha2_data, both


# ═══════════════════════════════════════════════════════
# Task 3: GL-orbit structure of equivariant subset
# ═══════════════════════════════════════════════════════

def task3(surjections, uf, equiv_data, n, p):
    print(f"\n{'='*70}")
    print("TASK 3: GL-orbit structure of equivariant subset at (3,3)")
    print(f"{'='*70}")

    N = 1 << n
    comps = uf.components()
    G_size = len(get_gl(n)) * (p - 1)

    # Identify equivariant orbits
    equiv_indices = {idx for idx, _ in equiv_data}
    equiv_orbit_roots = set()
    for idx in equiv_indices:
        equiv_orbit_roots.add(uf.find(idx))

    print(f"\n  Equivariant surjections: {len(equiv_indices)}")
    print(f"  Equivariant orbits: {len(equiv_orbit_roots)} / {len(comps)}")
    print(f"  |G| = |GL(3,F₂)| × |Aut(Z₃)| = {len(get_gl(n))} × {p-1} = {G_size}")

    # Per-orbit analysis
    orbit_info = []
    for root in sorted(equiv_orbit_roots):
        indices = comps[root]
        size = len(indices)
        stab_order = G_size // size

        # Count single vs double equivariant
        n_single = 0
        n_double = 0
        n_other = 0
        vec_set_counts = Counter()

        for idx in indices:
            vecs = [vs for i, vs in equiv_data if i == idx]
            if not vecs:
                # Not equivariant (but in an equivariant orbit)
                pass
            else:
                vs = vecs[0]
                n_vecs = len(vs)
                if n_vecs == 1:
                    n_single += 1
                elif n_vecs == 2:
                    n_double += 1
                else:
                    n_other += 1
                vec_set_counts[vs] += 1

        # Faster: precompute equiv_data as dict
        n_equiv_in_orbit = sum(1 for idx in indices if idx in equiv_indices)
        fp = fiber_partition(surjections[indices[0]], p)

        orbit_info.append({
            'root': root,
            'size': size,
            'stab_order': stab_order,
            'n_equiv': n_equiv_in_orbit,
            'partition': fp,
        })

    # Precompute equiv data as dict for faster lookup
    equiv_dict = {idx: vs for idx, vs in equiv_data}

    print(f"\n  {'Orbit':<8} {'Size':<8} {'|Stab|':<8} {'#Equiv':<8} "
          f"{'#1-vec':<8} {'#2-vec':<8} {'Partition':<20}")
    print(f"  {'-'*68}")

    for info in sorted(orbit_info, key=lambda x: -x['size']):
        root = info['root']
        indices = comps[root]

        n1 = n2 = n0 = 0
        for idx in indices:
            if idx in equiv_dict:
                nv = len(equiv_dict[idx])
                if nv == 1: n1 += 1
                elif nv == 2: n2 += 1
            else:
                n0 += 1

        print(f"  {'':<8} {info['size']:<8} {info['stab_order']:<8} "
              f"{n1+n2:<8} {n1:<8} {n2:<8} {info['partition']}")


# ═══════════════════════════════════════════════════════
# Task 4: Rigidity within double-equivariant sub-class
# ═══════════════════════════════════════════════════════

def task4(surjections, uf, equiv_data, n, p):
    print(f"\n{'='*70}")
    print("TASK 4: Rigidity within the double-equivariant sub-class")
    print(f"{'='*70}")

    comps = uf.components()
    equiv_dict = {idx: vs for idx, vs in equiv_data}

    # Double-equivariant surjections
    double_indices = {idx for idx, vs in equiv_data if len(vs) == 2}
    print(f"\n  Double-equivariant surjections: {len(double_indices)}")

    if not double_indices:
        print("  No double-equivariant surjections found.")
        return

    # How many GL-orbits do they span?
    double_orbit_roots = {uf.find(idx) for idx in double_indices}
    print(f"  GL-orbits spanned: {len(double_orbit_roots)}")

    for root in sorted(double_orbit_roots):
        indices = comps[root]
        n_double = sum(1 for idx in indices if idx in double_indices)
        n_total = len(indices)
        fp = fiber_partition(surjections[indices[0]], p)
        print(f"    Orbit size={n_total}, double-equiv={n_double}/{n_total} "
              f"({n_double/n_total*100:.1f}%), partition={fp}")

    # Within the double-equivariant set, what is the orbit structure?
    # (Under the FULL GL × Aut group, they may span multiple orbits.
    #  But we can also ask: under what subgroup are they a single orbit?)
    print(f"\n  Analysis of double-equivariant surjections:")

    # Show representative from each orbit
    for root in sorted(double_orbit_roots):
        indices = comps[root]
        double_in_orbit = [idx for idx in indices if idx in double_indices]

        # Show one example
        idx = double_in_orbit[0]
        f = surjections[idx]
        vecs = sorted(equiv_dict[idx])
        v3 = vecs[0] ^ vecs[1]
        print(f"\n    Representative from orbit (size {len(indices)}):")
        print(f"      f = {f}")
        print(f"      partition = {fiber_partition(f, p)}")
        print(f"      negation vectors: {[vec_str(v, n) for v in vecs]}")
        print(f"      v₁⊕v₂ = {vec_str(v3, n)}")

        # Show fiber structure
        fibers = defaultdict(list)
        for x in range(1 << n):
            fibers[f[x]].append(vec_str(x, n))
        for val in sorted(fibers.keys()):
            print(f"      f⁻¹({val}) = {fibers[val]}")

    # The key question: is a single orbit possible?
    print(f"\n  Summary: {len(double_indices)} double-equivariant surjections "
          f"span {len(double_orbit_roots)} GL-orbit(s)")
    if len(double_orbit_roots) == 1:
        orbit_size = len(comps[list(double_orbit_roots)[0]])
        G_size = len(get_gl(n)) * (p - 1)
        print(f"  → Single orbit! Size = {orbit_size}, |Stab| = {G_size // orbit_size}")
        print(f"  → This IS a rigid sub-class (in the double-equivariant sense)")
    else:
        print(f"  → Multiple orbits: no rigidity within double-equivariant class")


# ═══════════════════════════════════════════════════════
# Bonus: Compare equivariance regimes
# ═══════════════════════════════════════════════════════

def bonus_regime_comparison():
    print(f"\n\n{'='*70}")
    print("BONUS: Singleton-forcing boundary and equivariance structure")
    print(f"{'='*70}")

    n = 3
    print(f"\n  Singleton-forcing: p > 2^{{n-1}} = {2**(n-1)} ⟺ p ≥ {2**(n-1)+1}")
    print(f"  (3,3): p=3 ≤ 4 → NOT singleton-forcing (double equivariance possible)")
    print(f"  (3,5): p=5 > 4 → singleton-forcing (exactly 1 equivariance vector)")
    print(f"  (3,7): p=7 > 4 → singleton-forcing (exactly 1 equivariance vector)")

    print(f"\n  Why double equivariance is possible at (3,3):")
    print(f"  If f(x⊕v₁) = −f(x) and f(x⊕v₂) = −f(x), then:")
    print(f"    f(x⊕v₁⊕v₂) = −f(x⊕v₂) = −(−f(x)) = f(x)")
    print(f"  So f is PERIODIC w.r.t. v₃ = v₁⊕v₂: f(x⊕v₃) = f(x)")
    print(f"  This means f is constant on cosets of ⟨v₃⟩ (size 2 each)")
    print(f"  So f takes at most 2^{{n-1}} = {2**(n-1)} distinct values")
    print(f"  Surjective iff p ≤ 2^{{n-1}} = {2**(n-1)}")
    print(f"  At p=3: 3 ≤ 4 ✓ (possible)")
    print(f"  At p=5: 5 > 4 ✗ (impossible)")

    print(f"\n  This is EXACTLY the singleton-forcing boundary!")
    print(f"  Double equivariance ⟺ p ≤ 2^{{n-1}} ⟺ NOT singleton-forcing")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    n, p = 3, 3
    N = 1 << n

    print("Phase 5: The (3,3) Anomaly")
    print("=" * 70)
    print(f"Parameters: n={n}, p={p}")
    print(f"Domain: F₂³ ({N} elements), Codomain: Z₃ ({p} elements)")

    t0 = time.time()
    surjections = enumerate_surjections(n, p)
    print(f"\n{len(surjections)} surjections [{time.time()-t0:.1f}s]")

    t0 = time.time()
    uf = build_orbit_partition(n, p, surjections)
    comps = uf.components()
    print(f"{len(comps)} GL-orbits [{time.time()-t0:.1f}s]")

    # Task 1
    equiv_data = task1(surjections, n, p)

    # Task 2
    task2(surjections, n, p)

    # Task 3
    task3(surjections, uf, equiv_data, n, p)

    # Task 4
    task4(surjections, uf, equiv_data, n, p)

    # Bonus
    bonus_regime_comparison()

    # Final summary
    print(f"\n\n{'='*70}")
    print("FINAL SUMMARY")
    print(f"{'='*70}")
    print("""
The (3,3) anomaly reveals the singleton-forcing boundary in action:

1. At p=3 (below boundary): double negation-equivariance is possible
   because f(x⊕v₁)=−f(x) and f(x⊕v₂)=−f(x) implies f(x⊕(v₁⊕v₂))=f(x),
   making f periodic — but periodic surjections exist only when p ≤ 2^{n-1}.

2. At p=5 (at/above boundary): double equivariance forces periodicity
   which forces ≤4 distinct values, incompatible with surjecting onto Z₅.
   So exactly 1 equivariance vector per surjection.

3. The equivariance landscape at (3,3) is RICHER but LESS RIGID:
   - More equivariance axes per surjection (up to 2)
   - Mixed equivariance types possible (α=1 and α=−1 simultaneously)
   - More orbits in the equivariant subset (6 vs 5 at (3,5))

4. The singleton-forcing regime (p > 2^{n-1}) is where uniqueness lives.
   Below this boundary, there's more structure but less rigidity.
""")
