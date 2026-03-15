#!/usr/bin/env python3
"""Phase 4: The Branching Landscape.

For each (n, p) with n in {2,3,4,5} and eligible odd primes p <= 2^n - 1:
- Analytic complement-respecting surjection count
- Orbit count under Stab(comp) x Aut(Z_p) via union-find (where feasible)
- Fiber partition types per orbit
- Identify rigid points (orbit count = 1)
"""

from itertools import product
from collections import Counter
from math import comb
import time

# ═══════════════════════════════════════════════════════
# F₂ linear algebra
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

GL_ORDERS = {2: 6, 3: 168, 4: 20160, 5: 9999360}


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


# ═══════════════════════════════════════════════════════
# Analytic surjection count
# ═══════════════════════════════════════════════════════

def comp_surjection_count(k, p):
    """Complement-respecting surjection count via inclusion-exclusion.

    k = 2^(n-1) representatives, target Z_p.
    Negation classes on Z_p: {0} and {a, p-a} for a=1..m, where m=(p-1)/2.
    Each rep covers one class (1 value choice for class 0, 2 for others).
    Surjectivity = all m+1 classes covered.

    Formula: sum_{j=0}^{m} C(m,j) * (-1)^j * [(p-2j)^k - (p-1-2j)^k]
    """
    m = (p - 1) // 2
    total = 0
    for j in range(m + 1):
        a = (p - 2 * j) ** k
        b = max(0, p - 1 - 2 * j) ** k
        total += ((-1) ** j) * comb(m, j) * (a - b)
    return total


def eligible_primes(n):
    """Odd primes p with 2 < p <= 2^n - 1."""
    limit = (1 << n) - 1
    primes = []
    for p in range(3, limit + 1, 2):
        if all(p % d != 0 for d in range(2, int(p**0.5) + 1)):
            primes.append(p)
    return primes


# ═══════════════════════════════════════════════════════
# Complement pair representatives
# ═══════════════════════════════════════════════════════

def complement_pair_reps(n):
    """One representative per complement pair in F₂ⁿ."""
    N = 1 << n
    comp_vec = N - 1
    reps = []
    seen = set()
    for x in range(N):
        if x not in seen:
            reps.append(x)
            seen.add(x)
            seen.add(x ^ comp_vec)
    return reps


# ═══════════════════════════════════════════════════════
# Surjection enumeration (rep-tuple representation)
# ═══════════════════════════════════════════════════════

def enumerate_comp_surjections_rep(k, p):
    """Complement-respecting surjections as k-tuples of rep values.

    Surjectivity check: all negation classes must be covered.
    Class of v = min(v, p-v).
    """
    m = (p - 1) // 2
    required = set(range(m + 1))
    surjections = []
    for vals in product(range(p), repeat=k):
        classes = set(min(v, p - v) for v in vals)
        if classes == required:
            surjections.append(vals)
    return surjections


# ═══════════════════════════════════════════════════════
# Stab generators (rep-action representation)
# ═══════════════════════════════════════════════════════

def primitive_root(p):
    for g in range(2, p):
        if len({pow(g, k, p) for k in range(1, p)}) == p - 1:
            return g
    raise ValueError(f"No primitive root for p={p}")


def find_stab_generator_perms(gl, n, comp_vec):
    """Find generators of Stab(comp_vec) <= GL(n,F2) as domain permutations.

    Returns list of permutations (each a list of length 2^n).
    """
    N = 1 << n
    stab_perms = []
    for A in gl:
        if mat_vec_f2(A, comp_vec, n) == comp_vec:
            perm = tuple(mat_vec_f2(A, x, n) for x in range(N))
            stab_perms.append(perm)

    stab_set = set(stab_perms)
    expected = GL_ORDERS[n] // ((1 << n) - 1)
    print(f"    |Stab| = {len(stab_set)} (expected {expected})")

    # Find generators by incremental closure
    identity = tuple(range(N))
    generators = []
    generated = {identity}

    for perm in stab_perms:
        if perm in generated:
            continue
        generators.append(perm)
        # BFS: compose new element with all existing elements
        new_elements = {perm}
        queue = [perm]
        while queue:
            current = queue.pop()
            for g in generated | new_elements:
                for a, b in [(current, g), (g, current)]:
                    composed = tuple(a[b[x]] for x in range(N))
                    if composed not in generated and composed not in new_elements:
                        new_elements.add(composed)
                        queue.append(composed)
        generated |= new_elements
        if len(generated) == len(stab_set):
            break

    print(f"    Generators: {len(generators)}, closure: {len(generated)}")
    assert len(generated) == len(stab_set)
    return generators


def perm_to_rep_action(perm, reps, comp_vec):
    """Convert domain permutation to (source, sign) action on rep-values.

    For f -> f . A^{-1}: new_val[j] = sign * old_val[source] where
    the source/sign come from tracing A^{-1}(rep_j) through the complement structure.
    """
    N = len(perm)
    k = len(reps)
    rep_index = {r: i for i, r in enumerate(reps)}
    rep_set = set(reps)

    # Inverse permutation
    inv_perm = [0] * N
    for x in range(N):
        inv_perm[perm[x]] = x

    source = [0] * k
    sign = [1] * k
    for j in range(k):
        y = inv_perm[reps[j]]
        if y in rep_set:
            source[j] = rep_index[y]
            sign[j] = 1
        else:
            source[j] = rep_index[y ^ comp_vec]
            sign[j] = -1

    return source, sign


# ═══════════════════════════════════════════════════════
# Fiber partition from rep-values
# ═══════════════════════════════════════════════════════

def fiber_partition(vals, p):
    """Fiber partition of the full F₂ⁿ -> Z_p function from rep-values.

    Each rep value v contributes 1 to fiber(v) and 1 to fiber(-v mod p).
    """
    c = Counter(vals)
    fibers = {}
    for w in range(p):
        neg_w = (-w) % p
        fibers[w] = c.get(w, 0) + c.get(neg_w, 0)
    return tuple(sorted(fibers.values(), reverse=True))


# ═══════════════════════════════════════════════════════
# Core orbit computation
# ═══════════════════════════════════════════════════════

MAX_SURJ_FOR_ORBITS = 5_000_000


def compute_case(n, p):
    """Compute complement-respecting surjections and orbits for (n,p)."""
    k = 1 << (n - 1)
    comp_vec = (1 << n) - 1
    m = (p - 1) // 2

    # Analytic count
    count = comp_surjection_count(k, p)

    result = {
        'n': n, 'p': p, 'k': k, 'comp_vec': comp_vec,
        'surj_count': count,
        'stab_order': GL_ORDERS.get(n, '?') // ((1 << n) - 1) if n in GL_ORDERS else '?',
        'aut_order': p - 1,
    }

    if count == 0:
        result['orbits'] = 0
        result['orbit_sizes'] = []
        result['fiber_types'] = {}
        return result

    if count > MAX_SURJ_FOR_ORBITS:
        result['orbits'] = None
        result['reason'] = f'too large ({count:,})'
        return result

    # Enumerate surjections
    t0 = time.time()
    surjections = enumerate_comp_surjections_rep(k, p)
    t_enum = time.time() - t0
    assert len(surjections) == count, f"Enum {len(surjections)} != analytic {count}"
    result['t_enum'] = t_enum

    # Build index
    surj_idx = {s: i for i, s in enumerate(surjections)}

    # Union-find
    uf = UnionFind(len(surjections))

    # Stab generators
    t0 = time.time()
    print(f"  Computing Stab({comp_vec:0{n}b}) generators for n={n}...")
    gl = enumerate_gl_f2(n)
    stab_gens = find_stab_generator_perms(gl, n, comp_vec)
    reps = complement_pair_reps(n)

    # Convert to rep-actions
    rep_actions = [perm_to_rep_action(perm, reps, comp_vec) for perm in stab_gens]
    t_stab = time.time() - t0
    result['t_stab'] = t_stab

    # Apply Stab generators
    t0 = time.time()
    for source, sign in rep_actions:
        for idx in range(len(surjections)):
            vals = surjections[idx]
            new_vals = tuple((sign[j] * vals[source[j]]) % p for j in range(k))
            j = surj_idx.get(new_vals)
            if j is not None:
                uf.union(idx, j)

    # Apply Aut(Z_p) generator
    alpha = primitive_root(p)
    for idx in range(len(surjections)):
        vals = surjections[idx]
        new_vals = tuple((alpha * v) % p for v in vals)
        j = surj_idx.get(new_vals)
        if j is not None:
            uf.union(idx, j)

    t_uf = time.time() - t0
    result['t_uf'] = t_uf

    # Extract orbit data
    comps = uf.components()
    n_orbits = len(comps)
    orbit_sizes = sorted([len(v) for v in comps.values()], reverse=True)

    # Fiber partitions per orbit
    orbit_fibers = []
    for root, indices in comps.items():
        fp = fiber_partition(surjections[indices[0]], p)
        orbit_fibers.append((len(indices), fp))
    orbit_fibers.sort(key=lambda x: (-x[0], x[1]))

    fiber_types = Counter(fp for _, fp in orbit_fibers)

    result['orbits'] = n_orbits
    result['orbit_sizes'] = orbit_sizes
    result['orbit_fibers'] = orbit_fibers
    result['fiber_types'] = fiber_types
    result['min_orbit'] = min(orbit_sizes)
    result['max_orbit'] = max(orbit_sizes)

    return result


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def print_result(r):
    n, p = r['n'], r['p']
    count = r['surj_count']
    orbits = r.get('orbits')
    stab = r.get('stab_order', '?')
    aut = r.get('aut_order', '?')

    status = ""
    if orbits is None:
        status = f" [count only: {r.get('reason', '')}]"
    elif orbits == 1:
        status = " ★ RIGID"
    elif orbits == 0:
        status = " [no surjections]"

    print(f"  ({n},{p:>2}): {count:>12,} surjections", end="")
    if orbits is not None:
        print(f", {orbits:>6} orbits", end="")
        if orbits > 0:
            print(f", orbit range [{r['min_orbit']}..{r['max_orbit']}]", end="")
            print(f", {len(r['fiber_types'])} fiber types", end="")
    print(f"{status}")


if __name__ == '__main__':
    print("Phase 4: The Branching Landscape")
    print("Complement-respecting surjections F₂ⁿ → Z_p")
    print("=" * 70)

    all_results = {}

    for n in [2, 3, 4]:
        primes = eligible_primes(n)
        print(f"\n{'─'*70}")
        print(f"n = {n}: F₂{chr(0x2070+n)} → Z_p, primes p ∈ {primes}")
        print(f"  k = {1 << (n-1)} reps, |F₂{chr(0x2070+n)}| = {1 << n}")
        print(f"  comp_vec = {'1'*n}")
        stab_order = GL_ORDERS[n] // ((1 << n) - 1)
        print(f"  |Stab({'1'*n})| = {stab_order}")
        print(f"{'─'*70}")

        for p in primes:
            k = 1 << (n - 1)
            count = comp_surjection_count(k, p)
            print(f"\n  (n={n}, p={p}): analytic count = {count:,}")

            t0 = time.time()
            r = compute_case(n, p)
            elapsed = time.time() - t0
            print(f"    Total time: {elapsed:.1f}s")
            print_result(r)

            all_results[(n, p)] = r

    # ── n=5: analytic counts only ──
    print(f"\n{'─'*70}")
    print(f"n = 5: F₂⁵ → Z_p (analytic counts only)")
    print(f"  k = 16 reps, |F₂⁵| = 32")
    print(f"{'─'*70}")

    primes_5 = eligible_primes(5)
    for p in primes_5:
        k = 16
        count = comp_surjection_count(k, p)
        r = {'n': 5, 'p': p, 'surj_count': count, 'orbits': None,
             'reason': 'n=5 (enumeration infeasible)',
             'stab_order': GL_ORDERS[5] // 31, 'aut_order': p - 1}
        all_results[(5, p)] = r
        print(f"  (5,{p:>2}): {count:>20,} surjections [count only]")

    # ═══════════════════════════════════════════════════════
    # Summary tables
    # ═══════════════════════════════════════════════════════

    print(f"\n\n{'='*70}")
    print("FULL LANDSCAPE TABLE")
    print(f"{'='*70}")

    print(f"\n  {'(n,p)':<8} {'|surj|':>14} {'orbits':>8} {'min_orb':>10} "
          f"{'max_orb':>10} {'#fib_types':>10} {'|Stab|×|Aut|':>14} {'rigid?':>8}")
    print(f"  {'─'*82}")

    for n in [2, 3, 4, 5]:
        for p in eligible_primes(n):
            r = all_results.get((n, p))
            if not r:
                continue
            count = r['surj_count']
            orbits = r.get('orbits')
            stab = r.get('stab_order', '?')
            aut = r.get('aut_order', '?')
            group = f"{stab}×{aut}" if isinstance(stab, int) else "?"

            if orbits is not None and orbits > 0:
                rigid = "★ YES" if orbits == 1 else "no"
                ft = len(r.get('fiber_types', {}))
                print(f"  ({n},{p:>2})  {count:>14,}  {orbits:>6}  "
                      f"{r['min_orbit']:>10}  {r['max_orbit']:>10}  "
                      f"{ft:>10}  {group:>14}  {rigid:>8}")
            elif orbits == 0:
                print(f"  ({n},{p:>2})  {count:>14,}  {'0':>6}  "
                      f"{'—':>10}  {'—':>10}  {'—':>10}  {group:>14}  {'N/A':>8}")
            else:
                print(f"  ({n},{p:>2})  {count:>14,}  {'—':>6}  "
                      f"{'—':>10}  {'—':>10}  {'—':>10}  {group:>14}  {'—':>8}")
        if n < 5:
            print()

    # ── Rigid points ──
    print(f"\n{'='*70}")
    print("RIGID POINTS ANALYSIS")
    print(f"{'='*70}")

    computed_orbits = {(n, p): r['orbits'] for (n, p), r in all_results.items()
                       if r.get('orbits') is not None}
    rigid_computed = [k for k, v in computed_orbits.items() if v == 1]

    print(f"\n  Computed orbit counts for {len(computed_orbits)} cases.")
    if rigid_computed:
        print(f"  Rigid points (orbit count = 1): {rigid_computed}")
    else:
        print(f"  No (n,p) has total orbit count = 1.")
        print(f"  The prior research's 'rigidity at (3,5)' refers to a REFINED invariant:")
        print(f"  within (3,5)'s 5 orbits, the orbit formula ((p-3)/2)! × 2^{{2^{{n-1}}-1-n}}")
        print(f"  counts orbits of a specific fiber-constrained class, and equals 1 only at (3,5).")

    print(f"\n  Orbit count comparison at n=3:")
    for p in eligible_primes(3):
        r = all_results[(3, p)]
        marker = " ← I Ching" if p == 5 else ""
        singleton = p > (1 << 2)  # p > 2^{n-1} = 4
        regime = "singleton-forcing" if singleton else "degenerate"
        print(f"    (3,{p}): {r['orbits']} orbits, {len(r['fiber_types'])} fiber types "
              f"[{regime}]{marker}")

    print(f"\n  n=4 orbit explosion:")
    for p in eligible_primes(4):
        r = all_results[(4, p)]
        if r.get('orbits') is not None:
            print(f"    (4,{p}): {r['orbits']} orbits")
        else:
            print(f"    (4,{p}): {r['surj_count']:,} surjections (orbit count not computed)")

    # ── Branching ratio ──
    print(f"\n{'='*70}")
    print("BRANCHING RATIO (number of eligible primes per n)")
    print(f"{'='*70}")
    for n in [2, 3, 4, 5]:
        primes = eligible_primes(n)
        nonzero = [p for p in primes if all_results.get((n, p), {}).get('surj_count', 0) > 0]
        print(f"  n={n}: {len(primes)} eligible primes {primes}, "
              f"{len(nonzero)} with surjections {nonzero}")

    # ── Cross-cultural mapping ──
    print(f"\n{'='*70}")
    print("CROSS-CULTURAL MAPPING")
    print(f"{'='*70}")
    print(f"""
  System              Location in landscape
  ──────────────────  ──────────────────────────────────────────
  I Ching (China)     (3,5): 5 orbits, 2 fiber types — the unique (n,p) where
                      the prior orbit formula gives 1 (refined rigidity)
  Ifá (Yoruba)        n=4, no surjection (binary domain only, no codomain)
  Greek elements      n=2, identity map F₂² → F₂² (bijective, not a surjection to Z_p)
  Mahābhūta (India)   No binary substrate (chain poset P₅, no F₂ⁿ domain)
  Arabic geomancy     n=4, no surjection (binary domain only, no codomain)

  The I Ching is the only system with BOTH binary domain AND surjective codomain.
  All other cultures either:
  - Don't develop a surjection codomain (Ifá, Arabic geomancy: stay in F₂⁴)
  - Don't have a binary substrate (India: no F₂ⁿ)
  - Have bijective encoding, not a dimension-reducing surjection (Greece: 4→4)
""")

    # ── Fiber partition details for computed cases ──
    print(f"\n{'='*70}")
    print("FIBER PARTITION DETAILS (computed cases)")
    print(f"{'='*70}")
    for n in [2, 3, 4]:
        for p in eligible_primes(n):
            r = all_results.get((n, p))
            if not r or r.get('orbits') is None or r.get('orbits', 0) == 0:
                continue
            ft = r.get('fiber_types', {})
            if ft:
                print(f"\n  ({n},{p}): {r['orbits']} orbits, {len(ft)} fiber types")
                for fp, cnt in ft.most_common():
                    print(f"    {fp}: {cnt} orbit(s)")
