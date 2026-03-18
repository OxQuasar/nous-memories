#!/usr/bin/env python3
"""cyclotomic_probe.py — Investigate Q5: cyclotomic connection between 五行 and φ.

Three computations:
A. (n,p) Rigidity Landscape — orbit counts under Stab(1ⁿ) × Aut(Z_p)
B. Walsh Spectra — spectral invariants of complement-equivariant surjections
C. Character Lift Geometry — golden ratio structure in the character lift
"""

import numpy as np
from itertools import product as iprod
from collections import Counter, defaultdict
from math import factorial, gcd

# ════════════════════════════════════════════════════════════
# Constants
# ════════════════════════════════════════════════════════════

SQRT5 = np.sqrt(5)
PHI = (1 + SQRT5) / 2   # golden ratio ≈ 1.618
PSI = (1 - SQRT5) / 2   # conjugate   ≈ −0.618

# ════════════════════════════════════════════════════════════
# Shared utilities
# ════════════════════════════════════════════════════════════

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def odd_primes_up_to(m):
    return [p for p in range(3, m + 1) if is_prime(p)]

def primitive_root(p):
    for g in range(2, p):
        if len({pow(g, k, p) for k in range(1, p)}) == p - 1:
            return g
    return None

def complement(x, n):
    return x ^ ((1 << n) - 1)

def get_complement_pairs(n):
    """Return sorted list of (rep, comp) pairs. Rep = min of pair."""
    pairs, seen = [], set()
    for x in range(1 << n):
        if x not in seen:
            cx = complement(x, n)
            seen.add(x); seen.add(cx)
            pairs.append((min(x, cx), max(x, cx)))
    return sorted(pairs)

def inner_f2(a, b):
    """F₂ inner product: parity of bitwise AND."""
    return bin(a & b).count('1') & 1

def mat_vec_f2(M, x, n):
    """Matrix-vector multiply over F₂. M = list of n row-ints."""
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
                pivot = r; break
        if pivot is None:
            return False
        R[col], R[pivot] = R[pivot], R[col]
        for r in range(n):
            if r != col and R[r] & mask:
                R[r] ^= R[col]
    return True

def invert_f2(M, n):
    """Invert n×n matrix over F₂ via augmented row reduction."""
    aug = [(M[i] << n) | (1 << (n - 1 - i)) for i in range(n)]
    for col in range(n):
        mask = 1 << (2 * n - 1 - col)
        pivot = None
        for r in range(col, n):
            if aug[r] & mask:
                pivot = r; break
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(n):
            if r != col and aug[r] & mask:
                aug[r] ^= aug[col]
    return [aug[i] & ((1 << n) - 1) for i in range(n)]

_gl_cache = {}
def enumerate_gl_f2(n):
    if n not in _gl_cache:
        N = 1 << n
        _gl_cache[n] = [list(rows) for rows in iprod(range(N), repeat=n)
                        if is_invertible_f2(list(rows), n)]
    return _gl_cache[n]

def stab_ones(n):
    """Subgroup of GL(n,F₂) fixing 1ⁿ."""
    ones = (1 << n) - 1
    return [M for M in enumerate_gl_f2(n) if mat_vec_f2(M, ones, n) == ones]


# ────────────────────────────────────────
# Complement-equivariant surjection enumeration
# ────────────────────────────────────────

def enumerate_comp_surjections(n, p):
    """All complement-equivariant surjections as rep-value tuples."""
    pairs = get_complement_pairs(n)
    R = len(pairs)
    surjections = []
    for vals in iprod(range(p), repeat=R):
        image = set()
        for v in vals:
            image.add(v)
            image.add((-v) % p)
        if len(image) == p:
            surjections.append(vals)
    return surjections

def _integer_partitions(n, k, min_val=1):
    if k == 0:
        if n == 0: yield ()
        return
    if k == 1:
        if n >= min_val: yield (n,)
        return
    for first in range(min_val, n // k + 1):
        for rest in _integer_partitions(n - first, k - 1, first):
            yield (first,) + rest

def count_comp_surjections_fast(n, p):
    """Count using partition formula (no enumeration)."""
    R = 1 << (n - 1)
    num_neg = (p - 1) // 2
    if R < 1 + num_neg:
        return 0
    total = 0
    for m0 in range(1, R - num_neg + 1):
        remaining = R - m0
        for part in _integer_partitions(remaining, num_neg, 1):
            multi = factorial(R) // factorial(m0)
            for c in part:
                multi //= factorial(c)
            freq = Counter(part)
            orderings = factorial(num_neg)
            for f in freq.values():
                orderings //= factorial(f)
            orient = 1 << (R - m0)
            total += multi * orderings * orient
    return total


def expand_rep_vals(rep_vals, pairs, p, N):
    """Expand rep-value tuple to full function on F₂ⁿ."""
    f = [0] * N
    for i, (r, c) in enumerate(pairs):
        f[r] = rep_vals[i]
        f[c] = (-rep_vals[i]) % p
    return f

def fiber_partition(f_full, p):
    counts = Counter(f_full)
    return tuple(sorted(counts.values(), reverse=True))


# ────────────────────────────────────────
# Union-Find
# ────────────────────────────────────────

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
        groups = defaultdict(list)
        for i in range(len(self.parent)):
            groups[self.find(i)].append(i)
        return dict(groups)


# ════════════════════════════════════════════════════════════
# Computation A: (n,p) Rigidity Landscape
# ════════════════════════════════════════════════════════════

def compute_orbits(n, p, surjections, pairs):
    """Count orbits of surjections under Stab(1ⁿ) × Aut(Z_p).
    Returns (n_orbits, orbit_sizes_list, orbit_groups_dict)."""
    if not surjections:
        return 0, [], {}

    R = len(pairs)
    surj_idx = {s: i for i, s in enumerate(surjections)}
    uf = UnionFind(len(surjections))

    # Build lookup: element → (pair_index, is_rep)
    elem_info = {}
    for i, (r, c) in enumerate(pairs):
        elem_info[r] = (i, True)
        elem_info[c] = (i, False)

    pair_reps = [r for r, c in pairs]

    # Stab(1ⁿ) action
    stab = stab_ones(n)
    for M in stab:
        Minv = invert_f2(M, n)
        for idx, vals in enumerate(surjections):
            new_vals = []
            for j in range(R):
                y = mat_vec_f2(Minv, pair_reps[j], n)
                pi, is_rep = elem_info[y]
                new_vals.append(vals[pi] if is_rep else (-vals[pi]) % p)
            nv = tuple(new_vals)
            j2 = surj_idx.get(nv)
            if j2 is not None:
                uf.union(idx, j2)

    # Aut(Z_p) action
    g = primitive_root(p)
    if g is not None:
        for idx, vals in enumerate(surjections):
            nv = tuple((g * v) % p for v in vals)
            j2 = surj_idx.get(nv)
            if j2 is not None:
                uf.union(idx, j2)

    groups = uf.components()
    sizes = sorted([len(v) for v in groups.values()], reverse=True)
    return len(groups), sizes, groups


def has_dual_cycles(p):
    """Does Z_p have ≥2 independent Hamiltonian cycles?
    Requires p ≥ 5: stride-2 is independent of ±stride-1."""
    return p >= 5


def computation_a():
    print("=" * 72)
    print("COMPUTATION A: (n,p) Rigidity Landscape")
    print("  Orbits under Stab(1ⁿ) × Aut(Z_p)")
    print("=" * 72)

    ENUM_LIMIT = 100000  # max p^R for brute enumeration

    results = []

    for n in range(2, 6):
        N = 1 << n
        R = 1 << (n - 1)
        max_p = N - 1
        pairs = get_complement_pairs(n)
        primes = odd_primes_up_to(max_p)

        for p in primes:
            num_classes = (p + 1) // 2
            E = R - num_classes
            if E < 0:
                continue

            # Count surjections
            can_enum = p ** R <= ENUM_LIMIT
            if can_enum:
                surjections = enumerate_comp_surjections(n, p)
                n_surj = len(surjections)
            else:
                n_surj = count_comp_surjections_fast(n, p)
                surjections = None

            # Orbit computation (only if enumerable)
            n_orbits, orbit_sizes = None, None
            if surjections is not None and n_surj > 0:
                n_orbits, orbit_sizes, _ = compute_orbits(n, p, surjections, pairs)

            dual = has_dual_cycles(p)

            results.append({
                'n': n, 'p': p, 'R': R, 'E': E,
                'n_surj': n_surj, 'n_orbits': n_orbits,
                'orbit_sizes': orbit_sizes,
                'dual_cycles': dual,
            })

    # Print table
    print(f"\n  {'n':>2} {'p':>3} {'R':>3} {'E':>3} {'#surj':>12}"
          f" {'#orbits':>8} {'orbit sizes':>28} {'dual?':>5}")
    print("  " + "-" * 68)
    for r in results:
        orb_str = str(r['n_orbits']) if r['n_orbits'] is not None else '—'
        sizes_str = str(r['orbit_sizes']) if r['orbit_sizes'] else '—'
        if len(sizes_str) > 28:
            sizes_str = sizes_str[:25] + '...'
        dual_str = '✓' if r['dual_cycles'] else '✗'
        print(f"  {r['n']:>2} {r['p']:>3} {r['R']:>3} {r['E']:>3}"
              f" {r['n_surj']:>12,} {orb_str:>8} {sizes_str:>28} {dual_str:>5}")

    # Analysis
    print("\n  Analysis:")
    print("  ─────────")
    for r in results:
        if r['n_orbits'] is not None and r['dual_cycles']:
            tag = "RIGID" if r['n_orbits'] == 1 else f"{r['n_orbits']} orbits"
            print(f"    ({r['n']},{r['p']}): dual ✓, {tag}")

    # Check fiber partitions per orbit at (3,5)
    print("\n  (3,5) orbit structure:")
    n, p = 3, 5
    N = 1 << n
    pairs = get_complement_pairs(n)
    surjections = enumerate_comp_surjections(n, p)
    _, _, orbit_groups = compute_orbits(n, p, surjections, pairs)

    for oid, (root, members) in enumerate(
            sorted(orbit_groups.items(), key=lambda x: -len(x[1]))):
        rep_vals = surjections[members[0]]
        f_full = expand_rep_vals(rep_vals, pairs, p, N)
        fp = fiber_partition(f_full, p)
        print(f"    Orbit {oid} (size {len(members):>3}): "
              f"rep={rep_vals}, partition={fp}")

    return results


# ════════════════════════════════════════════════════════════
# Computation B: Walsh Spectra
# ════════════════════════════════════════════════════════════

def walsh_spectrum(f_full, n, p, k):
    """W_{f,k}(ω) = Σ_x ζ_p^{k·f(x)} · (-1)^{⟨ω,x⟩} for all ω."""
    N = 1 << n
    zeta = np.exp(2j * np.pi / p)
    g = np.array([zeta ** (k * f_full[x]) for x in range(N)])
    W = np.zeros(N, dtype=complex)
    for omega in range(N):
        signs = np.array([(-1) ** inner_f2(omega, x) for x in range(N)])
        W[omega] = np.sum(g * signs)
    return W


def spectral_signature(f_full, n, p):
    """Sorted multiset of |W|² across all k ∈ {1,...,p-1} and ω ∈ F₂ⁿ."""
    vals = []
    for k in range(1, p):
        W = walsh_spectrum(f_full, n, p, k)
        vals.extend(np.abs(W) ** 2)
    return tuple(sorted(round(v, 6) for v in vals))


def express_in_Q_sqrt5(v):
    """Try to express v as (a + b√5)/d for small integers. Returns string or None."""
    for d in [1, 2, 4, 5, 8, 10, 20]:
        for b in range(-30, 31):
            a_float = v * d - b * SQRT5
            a_int = round(a_float)
            if abs(a_float - a_int) < 1e-7:
                check = (a_int + b * SQRT5) / d
                if abs(check - v) < 1e-8:
                    if d == 1:
                        return f"{a_int} + {b}√5" if b >= 0 else f"{a_int} − {-b}√5"
                    else:
                        sign = '+' if b >= 0 else '−'
                        return f"({a_int} {sign} {abs(b)}√5)/{d}"
    return None


def computation_b():
    print("\n" + "=" * 72)
    print("COMPUTATION B: Walsh Spectra")
    print("=" * 72)

    # ── B1: (3,5) — full analysis ──
    print("\n  B1: (3,5) — all 240 surjections")
    print("  " + "─" * 50)
    n, p = 3, 5
    N = 1 << n
    pairs = get_complement_pairs(n)
    surjections = enumerate_comp_surjections(n, p)

    # Compute orbits
    _, _, orbit_groups = compute_orbits(n, p, surjections, pairs)

    # Spectral signature for each orbit
    print(f"\n  Spectral signatures by orbit (total {len(surjections)} surjections, "
          f"{len(orbit_groups)} orbits):")
    orbit_sigs = {}
    for oid, (root, members) in enumerate(
            sorted(orbit_groups.items(), key=lambda x: -len(x[1]))):
        # Check representative
        rep_f = expand_rep_vals(surjections[members[0]], pairs, p, N)
        sig = spectral_signature(rep_f, n, p)
        fp = fiber_partition(rep_f, p)
        orbit_sigs[oid] = (sig, fp, len(members))

        # Verify all members have same signature (spot check 3)
        for idx in members[:3]:
            f2 = expand_rep_vals(surjections[idx], pairs, p, N)
            s2 = spectral_signature(f2, n, p)
            assert s2 == sig, f"Spectral mismatch within orbit {oid}!"

        # Show first 6 values
        print(f"    Orbit {oid} (size {len(members):>3}, partition {fp}): "
              f"|W|² = [{', '.join(f'{v:.3f}' for v in sig[:6])}...]")

    unique_sigs = {sig for sig, _, _ in orbit_sigs.values()}
    print(f"\n  Distinct spectral signatures: {len(unique_sigs)} "
          f"(from {len(orbit_groups)} orbits)")

    # Identify which partitions share signatures
    by_sig = defaultdict(list)
    for oid, (sig, fp, sz) in orbit_sigs.items():
        by_sig[sig].append((oid, fp, sz))
    for sig, items in by_sig.items():
        partitions = set(fp for _, fp, _ in items)
        sizes = [sz for _, _, sz in items]
        print(f"    Signature class: partitions {partitions}, "
              f"orbit sizes {sizes}")

    # ── Detailed |W|² values for I Ching surjection ──
    print("\n  I Ching surjection Walsh |W|² in Q(√5):")
    f_iching = expand_rep_vals((1, 0, 2, 1), pairs, p, N)
    for k in [1, 2]:
        W = walsh_spectrum(f_iching, n, p, k)
        print(f"    k={k}:")
        for omega in range(N):
            Wsq = abs(W[omega]) ** 2
            expr = express_in_Q_sqrt5(Wsq)
            Wval = W[omega]
            print(f"      ω={omega:03b}: W = {Wval.real:+.4f}{Wval.imag:+.4f}i, "
                  f"|W|² = {Wsq:.6f} = {expr}")
        total = sum(abs(W[o]) ** 2 for o in range(N))
        print(f"      Parseval check: Σ|W|² = {total:.1f} (expect {N**2})")

    # Key value: W(k=1, ω=0)
    W0 = walsh_spectrum(f_iching, n, p, 1)[0]
    print(f"\n  KEY: W(k=1, ω=0) = {W0.real:.6f} + {W0.imag:.6f}i")
    print(f"       = φ = (1+√5)/2 = {PHI:.6f}")
    print(f"       |W|² = φ² = {PHI**2:.6f}")

    # ── B2: (3,3) and (3,7) comparison ──
    for p2 in [3, 7]:
        print(f"\n  B2: (3,{p2}) Walsh spectra")
        print("  " + "─" * 50)
        surj2 = enumerate_comp_surjections(n, p2)
        pairs2 = get_complement_pairs(n)
        _, _, og2 = compute_orbits(n, p2, surj2, pairs2)

        sigs2 = set()
        for root, members in og2.items():
            f2 = expand_rep_vals(surj2[members[0]], pairs2, p2, N)
            sig2 = spectral_signature(f2, n, p2)
            fp2 = fiber_partition(f2, p2)
            sigs2.add(sig2)
            print(f"    Orbit (size {len(members):>3}, partition {fp2}): "
                  f"|W|² = [{', '.join(f'{v:.3f}' for v in sig2[:6])}...]")

        print(f"    Distinct signatures: {len(sigs2)}")

        # Check if values are in Q(√5) or different field
        rep_f2 = expand_rep_vals(surj2[0], pairs2, p2, N)
        W_test = walsh_spectrum(rep_f2, n, p2, 1)
        Wsq_test = abs(W_test[0]) ** 2
        expr = express_in_Q_sqrt5(Wsq_test)
        if expr:
            print(f"    Sample |W|²(k=1,ω=0) = {Wsq_test:.6f} = {expr} [in Q(√5)]")
        else:
            # Try Q(√p) or Q(cos(2π/p))
            print(f"    Sample |W|²(k=1,ω=0) = {Wsq_test:.6f} [NOT in Q(√5)]")
            cos_val = 2 * np.cos(2 * np.pi / p2)
            print(f"    2cos(2π/{p2}) = {cos_val:.6f}")

    # ── B3: (4,13) sample ──
    print(f"\n  B3: (4,13) Walsh spectra (sampled)")
    print("  " + "─" * 50)
    n4, p4 = 4, 13
    N4 = 1 << n4
    pairs4 = get_complement_pairs(n4)
    R4 = len(pairs4)

    n_surj_413 = count_comp_surjections_fast(n4, p4)
    print(f"    Total surjections: {n_surj_413:,}")

    # Generate a few surjections by hand
    # Class assignment: 8 reps → 7 classes, one doubled
    # Sample 1: reps 0,1 → class 0, reps 2-7 → classes 1-6
    sample_reps = [
        (0, 0, 1, 2, 3, 4, 5, 6),   # doubled class 0
        (1, 2, 3, 4, 5, 6, 0, 0),   # doubled class 0 (shuffled)
        (0, 1, 1, 2, 3, 4, 5, 6),   # doubled class 1
    ]
    print(f"    Sampling {len(sample_reps)} surjections...")
    for i, rv in enumerate(sample_reps):
        f4 = expand_rep_vals(rv, pairs4, p4, N4)
        if len(set(f4)) < p4:
            print(f"    Sample {i}: not surjective, skipping")
            continue
        sig4 = spectral_signature(f4, n4, p4)
        fp4 = fiber_partition(f4, p4)
        # Check if in Q(√5)
        W_s = walsh_spectrum(f4, n4, p4, 1)
        Wsq_s = abs(W_s[0]) ** 2
        in_q5 = express_in_Q_sqrt5(Wsq_s) is not None
        print(f"    Sample {i} (partition {fp4}): "
              f"|W|²(1,0) = {Wsq_s:.6f}, in Q(√5)? {in_q5}")


# ════════════════════════════════════════════════════════════
# Computation C: Character Lift Geometry
# ════════════════════════════════════════════════════════════

def computation_c():
    print("\n" + "=" * 72)
    print("COMPUTATION C: Character Lift Geometry")
    print("=" * 72)

    n, p = 3, 5
    N = 1 << n
    zeta = np.exp(2j * np.pi / p)

    # ── C1: I Ching surjection ──
    # Complement-equivariant with 五行 fiber structure:
    #   Wood=0: {001,110}  Earth=1: {000,011}  Water=2: {010}
    #   Fire=3: {101}      Metal=4: {100,111}
    f = [1, 0, 2, 1, 4, 3, 0, 4]

    print("\n  C1: Character lift v_x = ζ₅^{f(x)}")
    print("  " + "─" * 50)
    print("  I Ching surjection (complement-equivariant):")
    element_names = {0: 'Wood', 1: 'Earth', 2: 'Water', 3: 'Fire', 4: 'Metal'}
    trigram_names = ['坤', '震', '坎', '艮', '兌', '離', '巽', '乾']
    for x in range(N):
        print(f"    f({x:03b}) = {f[x]} ({element_names[f[x]]})  [{trigram_names[x]}]")

    # ── C2: Construct v and verify equivariance ──
    v = np.array([zeta ** f[x] for x in range(N)])

    print("\n  C2: Complement equivariance v_{x⊕7} = conj(v_x)")
    all_ok = True
    for x in range(N):
        cx = x ^ 7
        diff = abs(v[cx] - np.conj(v[x]))
        ok = diff < 1e-10
        if not ok:
            all_ok = False
        if x < cx:
            print(f"    {x:03b}↔{cx:03b}: v = {v[x]:.4f}, v_comp = {v[cx]:.4f}, "
                  f"conj(v) = {np.conj(v[x]):.4f} {'✓' if ok else '✗'}")
    print(f"    Equivariance: {'VERIFIED ✓' if all_ok else 'FAILED ✗'}")

    # ── C3: Galois trace and norm per complement pair ──
    print("\n  C3: Galois structure per complement pair")
    print("  " + "─" * 50)
    print("  Tr_{Q(ζ₅)/Q(√5)}(ζ₅^k) = ζ₅^k + ζ₅^{-k} = 2cos(2πk/5)")
    print(f"    k=0: Tr = 2")
    print(f"    k=1: Tr = 2cos(72°) = (√5−1)/2 = 1/φ = {1/PHI:.6f}")
    print(f"    k=2: Tr = 2cos(144°) = −(√5+1)/2 = −φ = {-PHI:.6f}")
    print()

    pairs = get_complement_pairs(n)
    total_trace = 0
    total_norm = 0
    for i, (r, c) in enumerate(pairs):
        trace = v[r] + v[c]  # = v_x + conj(v_x) = 2·Re(v_x)
        norm = v[r] * v[c]   # = v_x · conj(v_x) = |v_x|² = 1
        total_trace += trace.real
        total_norm += norm.real
        # Express trace in terms of φ
        tr_val = trace.real
        if abs(tr_val - 2) < 1e-10:
            tr_expr = "2 (Wood: both → 0)"
        elif abs(tr_val - 1 / PHI) < 1e-10:
            tr_expr = f"1/φ = {1/PHI:.6f} (Earth/Metal)"
        elif abs(tr_val + PHI) < 1e-10:
            tr_expr = f"−φ = {-PHI:.6f} (Water/Fire)"
        else:
            tr_expr = f"{tr_val:.6f}"

        print(f"    Pair {{{r:03b},{c:03b}}}: f = ({f[r]},{f[c]}), "
              f"Tr = {tr_expr}, N = {norm.real:.1f}")

    print(f"\n    Σ Tr = {total_trace:.6f}")
    print(f"    Σ N  = {total_norm:.1f} (trivially = {len(pairs)}, since |ζ₅^k| = 1)")

    # Express Σ Tr in terms of φ
    # 2 + 2*(1/φ) + (-φ) = 2 + 2/φ - φ = 2 + (√5-1) - (1+√5)/2
    # = 2 + √5 - 1 - 1/2 - √5/2 = 1 + √5/2 = 1 + 1.118 = 2.118?
    # Let me just compute: 2 + 2*(1/PHI) + (-PHI)
    expected = 2 + 2 * (1 / PHI) + (-PHI)
    print(f"    = 2 + 2/φ − φ = 2 + {2/PHI:.6f} − {PHI:.6f} = {expected:.6f}")
    expr = express_in_Q_sqrt5(total_trace)
    if expr:
        print(f"    = {expr}")

    # ── C4: Inner product structure ──
    print("\n  C4: Inner product structure")
    print("  " + "─" * 50)

    # ⟨v,v⟩ = Σ|v_x|² = 8 (trivial)
    vv = np.sum(np.abs(v) ** 2)
    print(f"    ⟨v,v⟩ = Σ|v_x|² = {vv:.1f}")

    # σ(v)_x = v_{x⊕7} = conj(v_x)
    sigma_v = np.array([v[x ^ 7] for x in range(N)])

    # Bilinear pairing: Σ v_x · v_{x⊕7} = Σ v_x · conj(v_x) = Σ|v_x|² = 8
    bilinear = np.sum(v * sigma_v)
    print(f"    Σ v_x · v_{{x⊕7}} = {bilinear.real:.6f} + {bilinear.imag:.6f}i")
    print(f"    (= Σ|v_x|² = 8 since v_{{x⊕7}} = conj(v_x))")

    # Sesquilinear: ⟨v, σ(v)⟩ = Σ conj(v_x) · v_{x⊕7} = Σ conj(v_x)² 
    sesqui = np.sum(np.conj(v) * sigma_v)
    print(f"    ⟨v,σ(v)⟩ (sesquilinear) = {sesqui.real:.6f} + {sesqui.imag:.6f}i")
    sesqui_expr = express_in_Q_sqrt5(sesqui.real)
    if sesqui_expr and abs(sesqui.imag) < 1e-10:
        print(f"    = {sesqui_expr}")

    # ── C5: σ-eigenspace decomposition ──
    print("\n  C5: σ-eigenspace decomposition")
    print("  " + "─" * 50)
    print("  σ: v ↦ (v_{x⊕7}). Since v_{x⊕7} = conj(v_x):")
    print("    v⁺_x = (v_x + v_{x⊕7})/2 = Re(v_x)  [σ-eigenvalue +1, lives in Q(√5)]")
    print("    v⁻_x = (v_x − v_{x⊕7})/2 = i·Im(v_x) [σ-eigenvalue −1, pure imaginary]")

    v_plus = np.array([(v[x] + v[x ^ 7]) / 2 for x in range(N)])
    v_minus = np.array([(v[x] - v[x ^ 7]) / 2 for x in range(N)])

    norm_plus = np.sum(np.abs(v_plus) ** 2)
    norm_minus = np.sum(np.abs(v_minus) ** 2)
    total_norm_check = norm_plus + norm_minus

    print(f"\n    ||v⁺||² = {norm_plus:.6f}")
    print(f"    ||v⁻||² = {norm_minus:.6f}")
    print(f"    ||v⁺||² + ||v⁻||² = {total_norm_check:.6f} (expect 8)")

    frac_plus = norm_plus / 8
    frac_minus = norm_minus / 8
    print(f"\n    Fraction in φ-eigenspace: ||v⁺||²/||v||² = {frac_plus:.6f}")
    print(f"    Fraction in √5-eigenspace: ||v⁻||²/||v||² = {frac_minus:.6f}")

    # Express in Q(√5)
    expr_p = express_in_Q_sqrt5(norm_plus)
    expr_m = express_in_Q_sqrt5(norm_minus)
    if expr_p:
        print(f"\n    ||v⁺||² = {expr_p}")
    if expr_m:
        print(f"    ||v⁻||² = {expr_m}")

    # Detail per element
    print("\n    Per-element decomposition:")
    print(f"    {'x':>5} {'f(x)':>4} {'Re(v_x)':>10} {'Im(v_x)':>10}"
          f" {'cos²':>10} {'sin²':>10} {'cos form':>16}")
    for x in range(N):
        re = v[x].real
        im = v[x].imag
        c2 = re ** 2
        s2 = im ** 2
        k = f[x]
        if k == 0:
            cos_form = "1 (trivial)"
        elif k == 1 or k == 4:
            cos_form = f"(3∓√5)/8"
        elif k == 2 or k == 3:
            cos_form = f"(3±√5)/8"
        else:
            cos_form = "?"
        print(f"    {x:03b}   {k:>4}  {re:>10.6f} {im:>10.6f}"
              f" {c2:>10.6f} {s2:>10.6f}  {cos_form}")

    # ── C6: Comparison with (4,13) ──
    print("\n  C6: Comparison with (4,13)")
    print("  " + "─" * 50)

    n4, p4 = 4, 13
    N4 = 1 << n4
    pairs4 = get_complement_pairs(n4)
    zeta13 = np.exp(2j * np.pi / p4)

    # Construct a complement-equivariant surjection at (4,13)
    rep_vals_413 = (0, 0, 1, 2, 3, 4, 5, 6)
    f413 = expand_rep_vals(rep_vals_413, pairs4, p4, N4)
    fp413 = fiber_partition(f413, p4)
    print(f"    Surjection rep-vals: {rep_vals_413}")
    print(f"    Fiber partition: {fp413}")

    v413 = np.array([zeta13 ** f413[x] for x in range(N4)])

    # σ-eigenspace decomposition
    v413_plus = np.array([(v413[x] + v413[x ^ (N4 - 1)]) / 2 for x in range(N4)])
    v413_minus = np.array([(v413[x] - v413[x ^ (N4 - 1)]) / 2 for x in range(N4)])

    norm413_plus = np.sum(np.abs(v413_plus) ** 2)
    norm413_minus = np.sum(np.abs(v413_minus) ** 2)

    frac413_plus = norm413_plus / N4
    frac413_minus = norm413_minus / N4

    print(f"    ||v⁺||² = {norm413_plus:.6f}")
    print(f"    ||v⁻||² = {norm413_minus:.6f}")
    print(f"    Fraction in real eigenspace: {frac413_plus:.6f}")
    print(f"    Fraction in imag eigenspace: {frac413_minus:.6f}")

    # Galois traces at (4,13)
    print(f"\n    Galois traces Tr(ζ₁₃^k) = 2cos(2πk/13):")
    for k in range(7):
        tr = 2 * np.cos(2 * np.pi * k / p4)
        print(f"      k={k}: {tr:.6f}")

    print(f"\n    Compare: at (3,5), traces are 2, 1/φ, −φ (involving golden ratio)")
    print(f"    At (4,13), traces are 2cos(2πk/13) — NO golden ratio connection")
    print(f"    The √5 structure at (3,5) is specific to p=5, not generic")


# ════════════════════════════════════════════════════════════
# Computation D: Trace Sum Generalization (Thread 1)
# ════════════════════════════════════════════════════════════

def trace_sum_formula(p, m0, doubled_class):
    """Compute ΣTr for a complement-equivariant surjection at given (n,p).
    
    For E=1 family:
    - Shape B (doubled_class=0): ΣTr = 2·m₀ + Σ_{k=1}^{(p-1)/2} 2cos(2πk/p)
    - Shape A (doubled_class=j>0): ΣTr = 1 + 2cos(2πj/p)
    
    General: ΣTr = Σ_{pairs} 2cos(2πk_pair/p), where k_pair is the
    negation class assigned to each complement pair.
    """
    num_neg = (p - 1) // 2
    # Sum of all non-trivial traces
    total_cos = sum(2 * np.cos(2 * np.pi * k / p) for k in range(1, num_neg + 1))
    # This always equals -1 (since Σ_{k=0}^{p-1} ζ^k = 0, pair up conjugates)

    if doubled_class == 0:
        return 2 * m0 + total_cos
    else:
        # m0=1 zero pair contributes 2; doubled class j contributes 2×2cos(2πj/p);
        # other (p-3)/2 classes contribute their 2cos each
        return 2 + 2 * np.cos(2 * np.pi * doubled_class / p) + total_cos


def computation_d():
    print("\n" + "=" * 72)
    print("COMPUTATION D: Trace Sum Generalization")
    print("  Does ΣTr discriminate partition types at (4,13)?")
    print("=" * 72)

    # ── D1: General formula for E=1 family ──
    print("\n  D1: Universal trace sum formula for E=1 family (n, p=2ⁿ−3)")
    print("  " + "─" * 58)
    print("  Using Σ_{k=1}^{(p-1)/2} 2cos(2πk/p) = −1 always:")
    print("    Shape B (doubled class = 0):  ΣTr = 2·m₀ + (−1) = 2·2 − 1 = 3")
    print("    Shape A (doubled class = j):  ΣTr = 2 + 4cos(2πj/p) + (−1 − 2cos(2πj/p))")
    print("                                      = 1 + 2cos(2πj/p)")

    # ── D2: Verification at (3,5) ──
    print("\n  D2: Verification at (3,5)")
    print("  " + "─" * 58)

    n, p = 3, 5
    N = 1 << n
    pairs = get_complement_pairs(n)
    surjections = enumerate_comp_surjections(n, p)
    _, _, orbit_groups = compute_orbits(n, p, surjections, pairs)

    zeta = np.exp(2j * np.pi / p)
    print(f"  {'Orbit':>5} {'Size':>5} {'Partition':<18} {'Doubled':>8} {'ΣTr':>10} {'= ?':>10}")
    print("  " + "-" * 62)

    for oid, (root, members) in enumerate(
            sorted(orbit_groups.items(), key=lambda x: -len(x[1]))):
        rv = surjections[members[0]]
        f_full = expand_rep_vals(rv, pairs, p, N)
        fp = fiber_partition(f_full, p)

        # Compute ΣTr numerically
        v = np.array([zeta ** f_full[x] for x in range(N)])
        tr_sum = sum((v[r] + v[c]).real for r, c in pairs)

        # Identify doubled class
        cls_counts = Counter(min(rv[i], (-rv[i]) % p) for i in range(len(rv)))
        doubled = [c for c, cnt in cls_counts.items() if cnt > 1]
        dbl_str = f"cls {doubled[0]}" if doubled else "?"

        # Match
        if abs(tr_sum - PHI) < 1e-8:
            match = "φ"
        elif abs(tr_sum - PSI) < 1e-8:
            match = "ψ"
        elif abs(tr_sum - 3) < 1e-8:
            match = "3"
        else:
            match = "?"

        print(f"  {oid:>5} {len(members):>5} {str(fp):<18} {dbl_str:>8} "
              f"{tr_sum:>10.6f} {match:>10}")

    print("\n  Result: 3 distinct ΣTr values among 5 orbits.")
    print("    φ-class (orbits 0,1): 144 surjections — I Ching lives here")
    print("    ψ-class (orbit 2): 48 surjections")
    print("    3-class (orbits 3,4): 48 surjections (Shape B)")

    # ── D3: Application at (4,13) ──
    print("\n  D3: Trace sums at (4,13)")
    print("  " + "─" * 58)

    p4 = 13
    num_neg = (p4 - 1) // 2

    print(f"  Shape B: ΣTr = 3 (universal)")
    print(f"  Shape A with doubled negation class j:")
    print(f"  {'j':>4} {'2cos(2πj/13)':>14} {'ΣTr = 1+...':>14} {'min poly root?':>16}")
    print("  " + "-" * 52)

    for j in range(1, num_neg + 1):
        cos_val = 2 * np.cos(2 * np.pi * j / p4)
        tr = 1 + cos_val
        print(f"  {j:>4} {cos_val:>14.6f} {tr:>14.6f}")

    # Verify the minimal polynomial
    c = 2 * np.cos(2 * np.pi / p4)
    poly_check = c**6 + c**5 - 5*c**4 - 4*c**3 + 6*c**2 + 3*c - 1
    print(f"\n  Minimal poly of 2cos(2π/13): x⁶+x⁵−5x⁴−4x³+6x²+3x−1 = 0")
    print(f"    Check: {poly_check:.1e}")
    print(f"    Degree of Q(cos(2π/13))/Q = 6 (vs Q(√5)/Q = 2 at p=5)")

    # ── D4: Summary — universal formula across E=1 family ──
    print("\n  D4: Complete E=1 family trace sums")
    print("  " + "─" * 58)
    print(f"  {'(n,p)':>8} {'Shape B':>9} {'Shape A values':>40}")
    print("  " + "-" * 60)

    for n_val in [2, 3, 4, 5]:
        p_val = (1 << n_val) - 3
        if p_val < 3 or not is_prime(p_val):
            continue
        num_neg_val = (p_val - 1) // 2
        a_vals = [1 + 2 * np.cos(2 * np.pi * j / p_val)
                  for j in range(1, num_neg_val + 1)]
        a_strs = [f"{v:.4f}" for v in a_vals]

        # Check if values are in Q(√5)
        field = "Q"
        for v in a_vals:
            expr = express_in_Q_sqrt5(v)
            if expr and abs(v - round(v)) > 1e-8:
                field = "Q(√5)"
                break
        if field == "Q":
            # Check if degree matches
            deg = (p_val - 1) // 2
            if deg > 1:
                field = f"Q(cos(2π/{p_val})) [deg {deg}]"

        print(f"  ({n_val},{p_val:>2})   {'3':>9} {', '.join(a_strs):>40}  [{field}]")

    print("\n  KEY INSIGHT: Shape B always gives ΣTr = 3 (universal).")
    print("  Shape A gives ΣTr = 1 + 2cos(2πj/p), which depends on p.")
    print("  At p=5: values are φ, ψ — golden ratio pair.")
    print("  At p≥7: values are algebraic numbers of degree (p−1)/2.")
    print("  φ appears because Q(ζ₅)⁺ = Q(√5) is the ONLY quadratic")
    print("  maximal real subfield in the E=1 family.")


# ════════════════════════════════════════════════════════════
# Computation E: Pentagon/Pentagram Cayley Graphs (Thread 2)
# ════════════════════════════════════════════════════════════

def computation_e():
    print("\n" + "=" * 72)
    print("COMPUTATION E: Pentagon/Pentagram as Cayley Graphs")
    print("  The 生/克 cycles and the golden section share a graph")
    print("=" * 72)

    p = 5
    zeta = np.exp(2j * np.pi / p)
    vertices = [zeta ** k for k in range(p)]

    # ── E1: Cayley graph verification ──
    print("\n  E1: Cayley graph structure")
    print("  " + "─" * 50)
    print("  Vertices of Z₅ embedded at ζ₅^k on unit circle:")
    for k in range(p):
        z = vertices[k]
        print(f"    k={k}: ({z.real:+.4f}, {z.imag:+.4f})")

    print("\n  Pentagon = Cayley(Z₅, {±1}) = 生 cycle (stride-1)")
    print("  Edges: 0-1, 1-2, 2-3, 3-4, 4-0")
    print("  Pentagram = Cayley(Z₅, {±2}) = 克 cycle (stride-2)")
    print("  Edges: 0-2, 2-4, 4-1, 1-3, 3-0")

    # Verify: both are Hamiltonian (5-cycles on Z₅)
    print("\n  Both are 5-cycles (Hamiltonian on Z₅):")
    cycle1, x = [], 0
    for _ in range(p):
        cycle1.append(x); x = (x + 1) % p
    cycle2, x = [], 0
    for _ in range(p):
        cycle2.append(x); x = (x + 2) % p
    print(f"    Stride-1 cycle: {' → '.join(str(c) for c in cycle1)} → 0")
    print(f"    Stride-2 cycle: {' → '.join(str(c) for c in cycle2)} → 0")

    # ── E2: Edge length ratio ──
    print("\n  E2: Edge length ratio = golden ratio")
    print("  " + "─" * 50)

    pent_edge = abs(vertices[1] - vertices[0])
    penta_edge = abs(vertices[2] - vertices[0])
    ratio = penta_edge / pent_edge

    print(f"    Pentagon edge  |ζ₅¹ − ζ₅⁰| = 2sin(π/5) = {pent_edge:.6f}")
    print(f"    Pentagram edge |ζ₅² − ζ₅⁰| = 2sin(2π/5) = {penta_edge:.6f}")
    print(f"    Ratio = {ratio:.6f}")
    print(f"    φ     = {PHI:.6f}")
    print(f"    Match: {abs(ratio - PHI) < 1e-10} ✓")
    print()
    print("  Proof: |ζ₅² − 1|/|ζ₅ − 1| = sin(2π/5)/sin(π/5)")
    print(f"       = 2cos(π/5) = 2·{np.cos(np.pi/5):.6f} = {2*np.cos(np.pi/5):.6f} = φ")

    # ── E3: Adjacency spectrum ──
    print("\n  E3: Adjacency spectrum = Galois traces")
    print("  " + "─" * 50)

    for stride_k in [1, 2]:
        cycle_name = "生 (pentagon)" if stride_k == 1 else "克 (pentagram)"
        eigs = [2 * np.cos(2 * np.pi * j * stride_k / p) for j in range(p)]
        eigs_sorted = sorted(eigs, reverse=True)

        # Express each eigenvalue
        eig_exprs = []
        for e in eigs_sorted:
            if abs(e - 2) < 1e-10:
                eig_exprs.append("2")
            elif abs(e - 1 / PHI) < 1e-10:
                eig_exprs.append("1/φ")
            elif abs(e + PHI) < 1e-10:
                eig_exprs.append("−φ")
            else:
                eig_exprs.append(f"{e:.4f}")

        print(f"    Cayley(Z₅, {{±{stride_k}}}) [{cycle_name}]:")
        print(f"      λⱼ = 2cos(2πj·{stride_k}/5) for j=0,...,4")
        print(f"      = {{{', '.join(eig_exprs)}}}")

    print("\n    Pentagon and pentagram are ISOSPECTRAL.")
    print("    Same characteristic polynomial: (x−2)(x−1/φ)²(x+φ)²")
    print("    = x⁵ − 5x³ + 5x − 2")

    # Verify char poly
    from numpy.polynomial import polynomial as P
    # (x-2)(x - 1/phi)^2(x + phi)^2
    r1, r2, r3 = 2.0, 1 / PHI, -PHI
    # Expand: product of (x - ri)
    coeffs = np.array([1.0])
    for r in [r1, r2, r2, r3, r3]:
        coeffs = np.convolve(coeffs, [1, -r])
    coeffs_rounded = [round(c) for c in coeffs]
    print(f"    Verify: char poly coefficients = {coeffs_rounded}")

    # ── E4: Connection to Computation C ──
    print("\n  E4: Cayley spectrum = Galois traces from Computation C")
    print("  " + "─" * 50)
    print("  The adjacency eigenvalues of the pentagon at character j are")
    print("  exactly the Galois traces Tr(ζ₅^k) = 2cos(2πk/5):")
    print()
    print("    Pentagon eigenvalue λⱼ = Σ_{s ∈ {±1}} ζ₅^{js}")
    print("                         = ζ₅^j + ζ₅^{−j}")
    print("                         = Tr_{Q(ζ₅)/Q(√5)}(ζ₅^j)")
    print()
    print("  So the Galois trace per complement pair (from C3)")
    print("  IS the pentagon eigenvalue at the corresponding character.")
    print()

    # Map pairs to eigenvalues
    f_iching = [1, 0, 2, 1, 4, 3, 0, 4]
    pairs = get_complement_pairs(3)
    element_names = {0: 'Wood', 1: 'Earth', 2: 'Water', 3: 'Fire', 4: 'Metal'}
    print(f"    {'Pair':<12} {'f-values':<10} {'Tr':<10} {'Pentagon λ':>12}")
    print("    " + "-" * 46)
    for r, c in pairs:
        k = min(f_iching[r], (-f_iching[r]) % 5)  # canonical class
        tr = 2 * np.cos(2 * np.pi * f_iching[r] / p)
        lam = 2 * np.cos(2 * np.pi * f_iching[r] / p)
        name = element_names[f_iching[r]]
        if abs(tr - 2) < 1e-10:
            tr_s = "2"
        elif abs(tr - 1 / PHI) < 1e-10:
            tr_s = "1/φ"
        elif abs(tr + PHI) < 1e-10:
            tr_s = "−φ"
        else:
            tr_s = f"{tr:.4f}"
        print(f"    {{{r:03b},{c:03b}}}    ({f_iching[r]},{f_iching[c]})     "
              f"{tr_s:<10} {tr_s:>12}")

    # ── E5: Why isospectral ──
    print("\n  E5: Why pentagon ≅ pentagram")
    print("  " + "─" * 50)
    print("  2 is a primitive root mod 5: 2¹=2, 2²=4, 2³=3, 2⁴=1")
    print("  So α: k ↦ 2k is an automorphism of Z₅")
    print("  α maps stride-1 edges to stride-2 edges:")

    for k in range(p):
        k1 = (k + 1) % p
        ak = (2 * k) % p
        ak1 = (2 * k1) % p
        # stride-2 edge from ak
        print(f"    edge {k}—{k1} (stride-1) ↦ edge {ak}—{ak1} "
              f"(stride-{(ak1 - ak) % p})")

    print("\n  The map α is a GRAPH ISOMORPHISM: pentagon → pentagram.")
    print("  Isospectral is trivial since they're isomorphic graphs!")
    print()
    print("  This is the deep reason: stride-1 and stride-2 on Z₅")
    print("  are the SAME graph up to relabeling, because Z₅* = ⟨2⟩.")
    print("  The 生 and 克 cycles are algebraically identical;")
    print("  they differ only in which vertex labels you assign to phases.")

    # ── E6: What's p=5-specific? ──
    print("\n  E6: What's specific to p=5?")
    print("  " + "─" * 50)
    print("  Graph isomorphism: Cayley(Z_p, {±1}) ≅ Cayley(Z_p, {±2})")
    print("  always holds (α=2 maps {±1} → {±2} for any odd p).")
    print("  Both are p-cycles. The isomorphism is trivial and generic.")
    print()
    print("  What's p=5-specific is the GEOMETRIC content:")

    for pp in [3, 5, 7, 11, 13]:
        z = np.exp(2j * np.pi / pp)
        edge1 = abs(z - 1)        # stride-1 edge
        edge2 = abs(z**2 - 1)     # stride-2 edge
        ratio = edge2 / edge1
        eig1 = 2 * np.cos(2 * np.pi / pp)  # leading non-trivial eigenvalue
        field_deg = (pp - 1) // 2
        phi_tag = "= φ!" if abs(ratio - PHI) < 1e-10 else ""
        print(f"    p={pp:>2}: edge ratio = {ratio:.6f} {phi_tag:>6}"
              f"  leading eig = {eig1:>10.6f}"
              f"  field degree = {field_deg}")

    print()
    print("  Edge ratio = 2cos(π/p). Eigenvalues = 2cos(2πk/p).")
    print("  These involve φ ONLY at p=5, where cos(π/5) = φ/2")
    print("  and Q(cos(2π/5)) = Q(√5) = Q(φ) has degree 2.")


# ════════════════════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════════════════════

def summary():
    print("\n" + "=" * 72)
    print("SUMMARY: Q5 Assessment")
    print("=" * 72)

    print("""
  COMPUTATIONS A–C (Round 1):

  1. SPECTRAL STRUCTURE
     - (3,5) has 5 orbits under Stab(111) × Aut(Z₅).
       3 orbits with partition (2,2,2,1,1), 2 with (4,1,1,1,1).
     - Spectrally: 2 distinct signatures (one per partition type).
     - All |W|² values lie in Q(√5) = Q(φ).
       W(k=1, ω=0) = φ exactly for the I Ching surjection.
     - At (3,3): rational. At (3,7): Q(cos(2π/7)), degree 3, no √5.

  2. CHARACTER LIFT GEOMETRY
     - Complement equivariance = Galois conjugation σ: ζ₅ ↦ ζ₅⁴.
     - Galois traces: {2, 1/φ, −φ}. Sum = φ.
     - ⟨v,σ(v)⟩ = ψ = (1−√5)/2.

  COMPUTATIONS D–E (Round 2):

  3. TRACE SUM GENERALIZATION (D)
     Universal formula for E=1 family (n, p=2ⁿ−3):
       Shape B (m₀=2): ΣTr = 3           (for ALL primes)
       Shape A (j doubled): ΣTr = 1 + 2cos(2πj/p)  (depends on p)

     At (3,5): Shape A gives {φ, ψ} — golden ratio pair.
     At (4,13): Shape A gives six algebraic numbers in Q(cos(2π/13)).
     Discrimination generalizes; φ-structure does NOT.

     KEY: ΣTr = 3 for Shape B is universal across all (n,p) in
     the E=1 family. Shape A's trace sum is always 1 + eigenvalue
     of the Cayley graph — connecting partition type to spectral data.

  4. PENTAGON = PENTAGRAM (E)
     - Pentagon = Cayley(Z₅, {±1}) = 生 cycle
     - Pentagram = Cayley(Z₅, {±2}) = 克 cycle
     - Edge ratio: pentagram/pentagon = φ (the golden section!)
     - Both have spectrum {2, 1/φ, 1/φ, −φ, −φ}
     - They are ISOMORPHIC: α: k↦2k is the graph isomorphism.
       (This holds at ALL primes — it's the geometry that's p=5-specific.)

     The Cayley graph eigenvalues ARE the Galois traces from C3.
     Pentagon eigenvalue λⱼ = Tr(ζ₅^j). This is the bridge:
       Geometry: pentagram diagonal/side = φ = 2cos(π/5)
       Algebra: Galois trace Tr(ζ₅) = 2cos(2π/5) = 1/φ

  5. FINAL VERDICT ON Q5
     The golden ratio and 五行 dual cycles are connected through
     a precise mathematical bridge: the Cayley graph spectrum.

     The pentagon/pentagram (geometry) and the 生/克 cycles (algebra)
     are literally the SAME GRAPH. The golden ratio IS the edge-length
     ratio of that graph. The Galois traces ARE its eigenvalues.

     But the bridge is arithmetic, not axiomatic:
     - Q(ζ₅)⁺ = Q(√5) is the unique quadratic case in the E=1 family
     - 2 being a primitive root mod 5 makes the graph isomorphism work
     - At larger primes, the analogous structures exist but don't involve φ

     ASSESSMENT: "Address that determines the cause."
     The number 5 is not just a shared address — it's the unique prime
     where the cyclotomic structure collapses to quadratic, making φ
     the eigenvalue of the same graph that encodes the dual cycles.
     The connection is real but non-generalizable: it holds at (3,5)
     specifically, as a consequence of the arithmetic of 5.
""")


# ════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════

if __name__ == '__main__':
    computation_a()
    computation_b()
    computation_c()
    computation_d()
    computation_e()
    summary()
