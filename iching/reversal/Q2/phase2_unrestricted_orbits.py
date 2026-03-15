#!/usr/bin/env python3
"""Phase 2: Unrestricted surjection orbits under GL(n,F₂) × Aut(Z_p).

Parameters: (n,p) ∈ {(2,3), (3,3), (3,5), (3,7), (4,3), (4,5)}.
Methods:
  - Burnside's lemma for all cases (exact orbit count)
  - Union-find for small cases (orbit size distribution)
  - Complement analysis for (3,5)
"""

from itertools import product
from collections import Counter
from math import comb
import time

# ═══════════════════════════════════════════════════════
# F₂ linear algebra (matrices as lists of row-bitmasks)
# ═══════════════════════════════════════════════════════

def mat_vec_f2(M, x, n):
    """Apply n×n F₂ matrix M (list of row-ints) to vector x (int). Returns int."""
    result = 0
    for i in range(n):
        # Dot product of row i with x
        bits = M[i] & x
        parity = bin(bits).count('1') & 1
        result |= parity << (n - 1 - i)
    return result

def is_invertible_f2(rows, n):
    """Check invertibility via Gaussian elimination mod 2."""
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
    """All invertible n×n F₂ matrices."""
    N = 1 << n
    return [list(rows) for rows in product(range(N), repeat=n)
            if is_invertible_f2(list(rows), n)]

# Precompute and cache GL
_gl_cache = {}
def get_gl(n):
    if n not in _gl_cache:
        _gl_cache[n] = enumerate_gl_f2(n)
    return _gl_cache[n]

# Expected GL orders for validation
GL_ORDERS = {2: 6, 3: 168, 4: 20160}


# ═══════════════════════════════════════════════════════
# Burnside's Lemma (works for all cases)
# ═══════════════════════════════════════════════════════

def surjection_count_ie(N, p):
    """Standard inclusion-exclusion: |surj(N,p)|."""
    return sum((-1)**k * comb(p, k) * (p - k)**N for k in range(p + 1))

def ord_mod(a, p):
    """Multiplicative order of a in (Z/pZ)*."""
    for k in range(1, p):
        if pow(a, k, p) == 1:
            return k


def burnside_orbits(n, p):
    """Count orbits of surjections F₂ⁿ → Z_p under GL(n,F₂) × Aut(Z_p).
    
    For each (A, α):
    - Decompose A into cycles of lengths k₁,...,k_m on F₂ⁿ.
    - Cycle c is "free" if α^{k_c} ≡ 1 (mod p), else "forced" (value = 0).
    - A free cycle with representative value v covers the coset v·⟨α⟩ in Z_p*.
      d = ord(α), c = (p-1)/d cosets.
    - If m_forced > 0 (0 auto-covered): need all c cosets from free cycles.
      fix = Σ_{j=0}^c (-1)^j C(c,j) (1 + (c-j)d)^{m_free}
    - If m_forced = 0: need 0 + all c cosets from free cycles.
      fix = Σ_{j=0}^c (-1)^j C(c,j) [(1+(c-j)d)^{m_free} - ((c-j)d)^{m_free}]
    """
    N = 1 << n
    gl = get_gl(n)
    auts = list(range(1, p))
    G_size = len(gl) * len(auts)
    
    # Precompute cycle lengths for each A
    A_cycles = []
    for A in gl:
        visited = [False] * N
        lengths = []
        for start in range(N):
            if visited[start]:
                continue
            k = 0
            x = start
            while not visited[x]:
                visited[x] = True
                x = mat_vec_f2(A, x, n)
                k += 1
            lengths.append(k)
        A_cycles.append(lengths)
    
    # Cache ord_mod
    ord_cache = {alpha: ord_mod(alpha, p) for alpha in auts}
    
    total_fix = 0
    for lengths in A_cycles:
        for alpha in auts:
            m_free = sum(1 for k in lengths if pow(alpha, k, p) == 1)
            m_forced = len(lengths) - m_free
            
            d = ord_cache[alpha]
            c = (p - 1) // d  # number of cosets of ⟨α⟩ in Z_p*
            
            if m_forced > 0:
                # 0 auto-covered; need all c cosets from free cycles
                # Each free cycle: v=0 (1 way, no coset) or v∈coset_i (d ways)
                fix = sum((-1)**j * comb(c, j) * (1 + (c - j) * d)**m_free
                          for j in range(c + 1))
            else:
                # Need {0} + all c cosets
                fix = sum((-1)**j * comb(c, j) *
                          ((1 + (c - j) * d)**m_free - ((c - j) * d)**m_free)
                          for j in range(c + 1))
            total_fix += fix
    
    orbit_count = total_fix // G_size
    remainder = total_fix % G_size
    return orbit_count, total_fix, G_size, remainder


# ═══════════════════════════════════════════════════════
# Union-Find (orbit sizes for small cases)
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
    """Smallest primitive root mod p."""
    for g in range(2, p):
        if len({pow(g, k, p) for k in range(1, p)}) == p - 1:
            return g
    raise ValueError(f"No primitive root for p={p}")


def transvection_perms(n):
    """Permutations on F₂ⁿ induced by transvections E_{ij} (i≠j).
    E_{ij}(x): if bit i set, flip bit j."""
    N = 1 << n
    perms = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            perm = [x ^ (((x >> i) & 1) << j) for x in range(N)]
            perms.append(perm)
    return perms


def uf_orbits(n, p, surjections=None, return_uf=False):
    """Orbit partition via union-find with group generators.
    Returns (orbit_count, orbit_sizes_sorted, [uf if requested])."""
    N = 1 << n
    
    if surjections is None:
        surjections = enumerate_surjections(n, p)
    
    surj_idx = {s: i for i, s in enumerate(surjections)}
    uf = UnionFind(len(surjections))
    
    # GL generators: transvections
    perms = transvection_perms(n)
    
    for perm in perms:
        for idx in range(len(surjections)):
            f = surjections[idx]
            g = tuple(f[perm[x]] for x in range(N))
            j = surj_idx.get(g)
            if j is not None:
                uf.union(idx, j)
    
    # Aut generator: primitive root
    alpha = primitive_root(p)
    for idx in range(len(surjections)):
        f = surjections[idx]
        g = tuple((alpha * v) % p for v in f)
        j = surj_idx.get(g)
        if j is not None:
            uf.union(idx, j)
    
    comps = uf.components()
    sizes = sorted([len(v) for v in comps.values()], reverse=True)
    
    if return_uf:
        return len(comps), sizes, uf, surjections
    return len(comps), sizes


def enumerate_surjections(n, p):
    """All surjections F₂ⁿ → Z_p as tuples."""
    N = 1 << n
    target = set(range(p))
    return [vals for vals in product(range(p), repeat=N) if len(set(vals)) == p]


# ═══════════════════════════════════════════════════════
# Complement analysis for (3,5)
# ═══════════════════════════════════════════════════════

def complement_analysis():
    """For (n=3, p=5): partition unrestricted surjections into orbits,
    tag complement-respecting ones, report per-orbit breakdown."""
    n, p = 3, 5
    N = 1 << n
    ones = N - 1  # 0b111 = 7
    
    print(f"\n{'='*70}")
    print("COMPLEMENT ANALYSIS: (n=3, p=5)")
    print(f"{'='*70}")
    
    # Enumerate surjections
    t0 = time.time()
    surjections = enumerate_surjections(n, p)
    t1 = time.time()
    print(f"  Enumerated {len(surjections)} surjections in {t1-t0:.1f}s")
    
    # Orbit partition
    t0 = time.time()
    n_orbits, sizes, uf, _ = uf_orbits(n, p, surjections, return_uf=True)
    t1 = time.time()
    print(f"  Partitioned into {n_orbits} orbits in {t1-t0:.1f}s")
    
    # Tag complement-respecting
    def is_comp_resp(f):
        for x in range(N // 2):
            if (f[x] + f[x ^ ones]) % p != 0:
                return False
        return True
    
    comp_flags = [is_comp_resp(f) for f in surjections]
    total_comp = sum(comp_flags)
    print(f"  Complement-respecting surjections: {total_comp} / {len(surjections)}")
    
    # Per-orbit breakdown
    comps = uf.components()
    orbit_data = []
    for root, indices in comps.items():
        total = len(indices)
        comp_count = sum(1 for i in indices if comp_flags[i])
        orbit_data.append((total, comp_count))
    
    # Sort by size descending
    orbit_data.sort(key=lambda x: (-x[0], -x[1]))
    
    # Only show orbits that contain complement-respecting surjections,
    # plus a summary of orbits that don't
    orbits_with_comp = [(i+1, total, comp) for i, (total, comp)
                        in enumerate(orbit_data) if comp > 0]
    orbits_without = [(total, comp) for total, comp in orbit_data if comp == 0]
    
    print(f"\n  Orbits WITH complement-respecting members:")
    print(f"  {'Orbit':<8} {'Size':<8} {'#CompResp':<12} {'Fraction':<10}")
    print(f"  {'-'*38}")
    for orbit_num, total, comp in orbits_with_comp:
        print(f"  {orbit_num:<8} {total:<8} {comp:<12} {comp/total*100:.1f}%")
    
    print(f"\n  Orbits WITHOUT: {len(orbits_without)} orbits")
    without_sizes = Counter(t for t, _ in orbits_without)
    for size, count in sorted(without_sizes.items(), reverse=True):
        print(f"    {count} orbits of size {size}")
    
    print(f"\n  Orbits containing complement-respecting surjections: "
          f"{len(orbits_with_comp)} / {len(orbit_data)}")
    
    # Summary of complement-containing orbits
    if orbits_with_comp:
        print(f"\n  Complement-containing orbits detail:")
        for orbit_num, total, comp in orbits_with_comp:
            print(f"    Orbit {orbit_num}: {comp}/{total} complement-respecting "
                  f"({comp/total*100:.2f}%)")
    
    # Global fraction
    print(f"\n  Global: {total_comp}/{len(surjections)} = "
          f"{total_comp/len(surjections)*100:.4f}% are complement-respecting")
    
    return orbit_data


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

CASES = [(2, 3), (3, 3), (3, 5), (3, 7), (4, 3), (4, 5)]
UF_CASES = [(2, 3), (3, 3), (3, 5), (3, 7)]  # feasible for union-find

if __name__ == "__main__":
    print("Phase 2: Unrestricted surjection orbits under GL(n,F₂) × Aut(Z_p)")
    print("=" * 70)
    
    # ── Step 1: Validate GL sizes ──
    print("\nValidating GL(n, F₂) sizes...")
    for nn in sorted(set(n for n, _ in CASES)):
        gl = get_gl(nn)
        expected = GL_ORDERS.get(nn, "?")
        status = "✓" if len(gl) == expected else "✗"
        print(f"  GL({nn}, F₂): {len(gl)} {status} (expected {expected})")
    
    # ── Step 2: Burnside for all cases ──
    print(f"\n{'='*70}")
    print("BURNSIDE ORBIT COUNTS")
    print(f"{'='*70}")
    
    burnside_results = {}
    for n, p in CASES:
        N = 1 << n
        surj_count = surjection_count_ie(N, p)
        
        t0 = time.time()
        orbits, total_fix, G_size, rem = burnside_orbits(n, p)
        elapsed = time.time() - t0
        
        naive = surj_count / G_size
        
        print(f"\n  (n={n}, p={p}):")
        print(f"    |surjections| = {surj_count}")
        print(f"    |G| = |GL({n})| × |Aut(Z_{p})| = {len(get_gl(n))} × {p-1} = {G_size}")
        print(f"    Naive ratio = {naive:.2f}")
        print(f"    Σ|Fix(g)| = {total_fix}")
        print(f"    Orbits = {orbits} (remainder={rem}) [{elapsed:.2f}s]")
        
        burnside_results[(n, p)] = {
            'surj': surj_count, 'G': G_size, 'naive': naive,
            'orbits': orbits, 'fix_sum': total_fix
        }
    
    # ── Step 3: Union-find validation for small cases ──
    print(f"\n{'='*70}")
    print("UNION-FIND VALIDATION (small cases)")
    print(f"{'='*70}")
    
    uf_results = {}
    for n, p in UF_CASES:
        t0 = time.time()
        print(f"\n  (n={n}, p={p}):")
        
        surjections = enumerate_surjections(n, p)
        t_enum = time.time() - t0
        print(f"    Enumerated {len(surjections)} surjections [{t_enum:.1f}s]")
        
        t0 = time.time()
        n_orbits, sizes = uf_orbits(n, p, surjections)
        t_uf = time.time() - t0
        
        burnside_count = burnside_results[(n, p)]['orbits']
        match = "✓" if n_orbits == burnside_count else "✗ MISMATCH"
        
        print(f"    Orbits: {n_orbits} {match} (Burnside: {burnside_count}) [{t_uf:.1f}s]")
        print(f"    Size distribution: {dict(Counter(sizes))}")
        print(f"    Min orbit: {min(sizes)}, Max orbit: {max(sizes)}")
        
        uf_results[(n, p)] = {
            'orbits': n_orbits, 'sizes': sizes,
            'min': min(sizes), 'max': max(sizes)
        }
    
    # ── Step 4: Complement analysis for (3,5) ──
    comp_data = complement_analysis()
    
    # ── Step 5: Summary table ──
    print(f"\n\n{'='*70}")
    print("SUMMARY TABLE")
    print(f"{'='*70}")
    
    header = (f"{'(n,p)':<10} {'|surj|':<15} {'|G|':<10} {'naive':<10} "
              f"{'orbits':<10} {'min_orb':<10} {'max_orb':<10}")
    print(header)
    print("-" * len(header))
    
    for n, p in CASES:
        b = burnside_results[(n, p)]
        u = uf_results.get((n, p))
        
        min_o = str(u['min']) if u else "—"
        max_o = str(u['max']) if u else "—"
        
        print(f"({n},{p}){'':<5} {b['surj']:<15} {b['G']:<10} {b['naive']:<10.2f} "
              f"{b['orbits']:<10} {min_o:<10} {max_o:<10}")
    
    # ── Step 6: Key observations ──
    print(f"\n{'='*70}")
    print("KEY OBSERVATIONS")
    print(f"{'='*70}")
    
    # Check which cases give 1 orbit
    rigid = [(n, p) for (n, p), b in burnside_results.items() if b['orbits'] == 1]
    if rigid:
        print(f"  Rigid cases (1 orbit): {rigid}")
    else:
        print(f"  No rigid cases found in unrestricted setting.")
    
    # Compare orbit counts
    print(f"\n  Orbit count progression by n (fixed p):")
    for p in sorted(set(pp for _, pp in CASES)):
        cases_p = [(n, pp) for n, pp in CASES if pp == p]
        if len(cases_p) > 1:
            vals = [(n, burnside_results[(n, p)]['orbits']) for n, _ in cases_p]
            print(f"    p={p}: " + ", ".join(f"n={n}→{o}" for n, o in vals))
    
    print(f"\n  Orbit count progression by p (fixed n):")
    for n in sorted(set(nn for nn, _ in CASES)):
        cases_n = [(nn, p) for nn, p in CASES if nn == n]
        if len(cases_n) > 1:
            vals = [(p, burnside_results[(n, p)]['orbits']) for _, p in cases_n]
            print(f"    n={n}: " + ", ".join(f"p={p}→{o}" for p, o in vals))
