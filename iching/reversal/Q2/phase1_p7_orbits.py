#!/usr/bin/env python3
"""Phase 1: p=7 complement-respecting surjection orbits.

Case 1: (n=3, p=7) — 8 elements, 4 complement pairs, E=0
Case 2: (n=4, p=7) — 16 elements, 8 complement pairs, E=4

Uses Burnside's lemma with bitmask DP for surjectivity.
Cross-validates with union-find for the small case.
"""

from itertools import product
from collections import Counter
from math import comb

# ── F_2 linear algebra ──

def vec_to_int(v, n):
    return sum(b << (n - 1 - i) for i, b in enumerate(v))

def int_to_vec(x, n):
    return tuple((x >> (n - 1 - i)) & 1 for i in range(n))

def mat_vec_f2(M, x, n):
    """M is list of n rows (each an int bitmask), x is int. Returns int."""
    result = 0
    for i in range(n):
        # dot product of row i with x
        bits = M[i] & x
        parity = 0
        while bits:
            parity ^= bits & 1
            bits >>= 1
        result |= parity << (n - 1 - i)
    return result

def mat_mul_f2(A, B, n):
    """Multiply two n×n F_2 matrices (stored as list of row-ints)."""
    # B columns
    B_cols = []
    for j in range(n):
        col = 0
        for i in range(n):
            col |= ((B[i] >> (n - 1 - j)) & 1) << (n - 1 - i)
        B_cols.append(col)
    result = []
    for i in range(n):
        row = 0
        for j in range(n):
            bits = A[i] & B_cols[j]
            parity = 0
            while bits:
                parity ^= bits & 1
                bits >>= 1
            row |= parity << (n - 1 - j)
        result.append(row)
    return result

def is_invertible_f2(M, n):
    """Gaussian elimination mod 2. M is list of n row-ints."""
    rows = list(M)
    for col_bit in range(n):
        col_mask = 1 << (n - 1 - col_bit)
        pivot = None
        for r in range(col_bit, n):
            if rows[r] & col_mask:
                pivot = r
                break
        if pivot is None:
            return False
        rows[col_bit], rows[pivot] = rows[pivot], rows[col_bit]
        for r in range(n):
            if r != col_bit and rows[r] & col_mask:
                rows[r] ^= rows[col_bit]
    return True

def enumerate_gl_f2(n):
    """All invertible n×n matrices over F_2, as lists of row-ints."""
    N = 2**n
    matrices = []
    for rows in product(range(N), repeat=n):
        if is_invertible_f2(list(rows), n):
            matrices.append(list(rows))
    return matrices

def stab_allones_f2(matrices, n):
    """Filter matrices fixing the all-ones vector (2^n - 1)."""
    ones = (1 << n) - 1
    return [M for M in matrices if mat_vec_f2(M, ones, n) == ones]


# ── Complement pairs ──

def complement_pairs(n):
    """Return (reps, comps) as int-vectors. rep < comp."""
    ones = (1 << n) - 1
    seen = set()
    reps, comps = [], []
    for x in range(2**n):
        if x in seen:
            continue
        c = x ^ ones
        seen.add(x)
        seen.add(c)
        reps.append(x)
        comps.append(c)
    return reps, comps


# ── Burnside orbit counting with bitmask DP ──

def burnside_complement_orbits(n, p):
    """Count orbits of complement-respecting surjections F_2^n → Z_p
    under Stab(1...1) × Aut(Z_p), using Burnside + bitmask DP."""
    
    ones = (1 << n) - 1
    N = 2**n
    reps, comps = complement_pairs(n)
    R = len(reps)
    
    # Map each element to its pair index and whether it's the rep
    elem_pair = {}  # element → (pair_index, is_rep)
    for i in range(R):
        elem_pair[reps[i]] = (i, True)
        elem_pair[comps[i]] = (i, False)
    
    # Symmetry group
    print(f"  Computing GL({n}, F_2)...")
    all_gl = enumerate_gl_f2(n)
    print(f"  |GL({n}, F_2)| = {len(all_gl)}")
    
    stab = stab_allones_f2(all_gl, n)
    print(f"  |Stab({bin(ones)})| = {len(stab)}")
    
    auts = list(range(1, p))  # Aut(Z_p)
    G_size = len(stab) * len(auts)
    print(f"  |Aut(Z_{p})| = {len(auts)}")
    print(f"  |G| = {G_size}")
    
    FULL_MASK = (1 << p) - 1
    
    # Precompute: for each A in stab, the permutation on complement pairs + signs
    # A maps rep[i] → some element. That element is in pair σ(i).
    # If A(rep[i]) is the rep of pair σ(i), sign = +1. If it's the comp, sign = -1.
    
    total_fix = 0
    
    for A in stab:
        # Compute pair permutation and signs for this A
        sigma = [0] * R  # sigma[i] = target pair index
        signs = [0] * R  # +1 or -1
        
        for i in range(R):
            Ar = mat_vec_f2(A, reps[i], n)
            j, is_rep = elem_pair[Ar]
            sigma[i] = j
            signs[i] = 1 if is_rep else -1  # -1 means maps to comp → need negation
        
        # Find cycles of sigma
        visited = [False] * R
        cycles = []  # list of (indices, sign_product)
        
        for start in range(R):
            if visited[start]:
                continue
            cycle_idx = []
            cycle_signs = []
            i = start
            while not visited[i]:
                visited[i] = True
                cycle_idx.append(i)
                cycle_signs.append(signs[i])
                i = sigma[i]
            cycles.append((cycle_idx, cycle_signs))
        
        # For each alpha in Aut(Z_p), compute Fix count
        for alpha in auts:
            # For each cycle, determine free/forced and compute multiplier bitmask
            forced_any = False  # any forced cycle → 0 is covered
            free_cycle_masks = []  # list of (bitmask_for_each_v,) for free cycles
            
            all_forced = True
            for cycle_idx, cycle_signs in cycles:
                k = len(cycle_idx)
                eps_prod = 1
                for s in cycle_signs:
                    eps_prod *= s  # +1 or -1
                eps_prod_mod = eps_prod % p  # -1 → p-1
                
                beta = (eps_prod_mod * pow(alpha, k, p)) % p
                
                if beta != 1:
                    # Forced: value = 0, range = {0}
                    forced_any = True
                else:
                    all_forced = False
                    # Free cycle: compute multipliers γ_t
                    # γ_1 = 1, γ_{t+1} = signs[t] * alpha * γ_t mod p
                    gammas = []
                    g = 1
                    for t in range(k):
                        gammas.append(g)
                        g = (cycle_signs[t] * alpha * g) % p
                    
                    # Range set Γ = {±γ_t mod p : t}
                    gamma_set = set()
                    for g in gammas:
                        gamma_set.add(g % p)
                        gamma_set.add((-g) % p)
                    
                    # Bitmask for each value v ∈ Z_p
                    masks = [0] * p
                    masks[0] = 1  # v=0 → only 0
                    for v in range(1, p):
                        m = 0
                        for g in gamma_set:
                            m |= 1 << ((v * g) % p)
                        masks[v] = m
                    
                    free_cycle_masks.append(masks)
            
            if not free_cycle_masks:
                # All forced: range = {0}, not surjective (if p > 1)
                # Unless p=1 (trivial), skip
                continue
            
            # DP over free cycles: dp[mask] = # ways to achieve this mask
            base_mask = 1 if forced_any else 0  # forced cycles contribute {0}
            
            dp = [0] * (FULL_MASK + 1)
            dp[base_mask] = 1
            
            for masks in free_cycle_masks:
                new_dp = [0] * (FULL_MASK + 1)
                for old_mask in range(FULL_MASK + 1):
                    if dp[old_mask] == 0:
                        continue
                    for v in range(p):
                        new_mask = old_mask | masks[v]
                        new_dp[new_mask] += dp[old_mask]
                dp = new_dp
            
            total_fix += dp[FULL_MASK]
    
    orbit_count = total_fix // G_size
    remainder = total_fix % G_size
    
    return orbit_count, total_fix, G_size, remainder


# ── Union-Find (for cross-validation) ──

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
    
    def component_sizes(self):
        groups = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            groups.setdefault(r, []).append(i)
        return sorted([len(g) for g in groups.values()], reverse=True)


def union_find_complement_orbits(n, p):
    """Direct orbit enumeration via union-find. Only feasible for small cases."""
    ones = (1 << n) - 1
    N = 2**n
    reps, comps = complement_pairs(n)
    R = len(reps)
    
    # Enumerate complement-respecting surjections
    surjections = []
    for vals in product(range(p), repeat=R):
        f = [0] * N
        for i, v in enumerate(vals):
            f[reps[i]] = v
            f[comps[i]] = (-v) % p
        if len(set(f)) == p:
            surjections.append(tuple(f))
    
    if not surjections:
        return 0, [], surjections
    
    surj_idx = {s: i for i, s in enumerate(surjections)}
    uf = UnionFind(len(surjections))
    
    stab = stab_allones_f2(enumerate_gl_f2(n), n)
    auts = list(range(1, p))
    
    # Precompute A permutations
    for A in stab:
        perm = [mat_vec_f2(A, x, n) for x in range(N)]
        for alpha in auts:
            for idx, f in enumerate(surjections):
                # g(Ax) = alpha * f(x) for all x → g[perm[x]] = (alpha * f[x]) % p
                g = [0] * N
                for x in range(N):
                    g[perm[x]] = (alpha * f[x]) % p
                g_key = tuple(g)
                if g_key in surj_idx:
                    uf.union(idx, surj_idx[g_key])
    
    sizes = uf.component_sizes()
    return len(sizes), sizes, surjections


def surjection_count_ie(N, p):
    """Inclusion-exclusion: |surj(N→p)| = Σ (-1)^k C(p,k)(p-k)^N."""
    return sum((-1)**k * comb(p, k) * (p - k)**N for k in range(p + 1))


# ── Main ──

def run_case(n, p, use_uf=False):
    print(f"\n{'='*60}")
    print(f"Case: (n={n}, p={p})")
    print(f"{'='*60}")
    
    N = 2**n
    ones = (1 << n) - 1
    reps, comps = complement_pairs(n)
    R = len(reps)
    S = (p + 1) // 2
    E = R - S
    
    print(f"  N={N}, R={R} pairs, S={S} slots, E={E} excess")
    
    # Surjection counts
    total_surj = surjection_count_ie(N, p)
    
    # Complement-respecting surjection count (via inclusion-exclusion on negation slots)
    # Negation classes: {0} (size 1), then (p-1)/2 classes of size 2
    neg_classes = [{0}]
    for v in range(1, (p + 1) // 2):
        neg_classes.append({v, (-v) % p})
    
    nc = len(neg_classes)
    class_sizes = [len(c) for c in neg_classes]
    
    # IE over negation classes: must cover all classes
    comp_surj = 0
    for T in product([0, 1], repeat=nc):
        excluded = sum(T)
        avail = sum(class_sizes[j] for j in range(nc) if T[j] == 0)
        comp_surj += ((-1) ** excluded) * (avail ** R)
    
    print(f"  Total surjections (unrestricted): {total_surj}")
    print(f"  Complement-respecting surjections: {comp_surj}")
    print()
    
    # Burnside
    print(f"  --- Burnside's Lemma ---")
    orbit_count, total_fix, G_size, rem = burnside_complement_orbits(n, p)
    print(f"  Σ|Fix(g)| = {total_fix}")
    print(f"  |G| = {G_size}")
    print(f"  Orbit count = {total_fix} / {G_size} = {orbit_count} (remainder {rem})")
    
    # Cross-validation with union-find for small cases
    if use_uf:
        print(f"\n  --- Union-Find Cross-Validation ---")
        uf_orbits, uf_sizes, surjs = union_find_complement_orbits(n, p)
        print(f"  Union-find orbits: {uf_orbits}")
        print(f"  Orbit sizes: {uf_sizes}")
        print(f"  Size distribution: {dict(Counter(uf_sizes))}")
        if uf_orbits == orbit_count:
            print(f"  ✓ Matches Burnside result!")
        else:
            print(f"  ✗ MISMATCH with Burnside!")
    
    print(f"\n  RESULT: {orbit_count} orbits")
    return orbit_count, total_fix, G_size


if __name__ == "__main__":
    print("Phase 1: p=7 complement-respecting surjection orbits")
    print("Testing whether p=7 yields rigidity (1 orbit)")
    print()
    print("Theoretical expectation: NO rigidity for p=7")
    print("  p=7 has (p-3)/2 = 2 independent negation cycles")
    print("  Assignment factorial = 2! = 2, preventing orbit collapse")
    
    # Case 1: (n=3, p=7) — small, use both methods
    r1 = run_case(3, 7, use_uf=True)
    
    # Case 2: (n=4, p=7) — larger, Burnside only
    r2 = run_case(4, 7, use_uf=False)
    
    # Also run (3,5) for reference — the known rigid case
    print(f"\n{'='*60}")
    print("Reference: (n=3, p=5) — known rigid case")
    print(f"{'='*60}")
    r_ref = run_case(3, 5, use_uf=True)
    
    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'(n,p)':<10} {'orbits':<10} {'Σ|Fix|':<15} {'|G|':<10}")
    print(f"{'-'*45}")
    for label, r in [("(3,5)", r_ref), ("(3,7)", r1), ("(4,7)", r2)]:
        print(f"{label:<10} {r[0]:<10} {r[1]:<15} {r[2]:<10}")
    print()
    print("Rigidity = exactly 1 orbit.")
    print("(3,5): RIGID" if r_ref[0] == 1 else "(3,5): NOT rigid — UNEXPECTED!")
    print(f"(3,7): {'RIGID — UNEXPECTED!' if r1[0] == 1 else f'{r1[0]} orbits — confirms non-rigidity'}")
    print(f"(4,7): {'RIGID — UNEXPECTED!' if r2[0] == 1 else f'{r2[0]} orbits — confirms non-rigidity'}")
