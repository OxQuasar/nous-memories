#!/usr/bin/env python3
"""
within_type_orbits.py — Phase 3, Iteration 13 (Part 3)

Task 1: Count surjections for one fixed type distribution at (4,13)
Task 2: Compute orbits under (F₂)³ × Aut(Z₁₃) within that type distribution
Task 3: Cross-check at (3,5)
Task 4: Characterize orbits if > 1
Task 5: Does 互 at n=4 reduce the moduli?
"""

import sys
from collections import Counter, defaultdict
from itertools import product as iterproduct, permutations
from math import factorial

# ═══════════════════════════════════════════════════════════════
# F₂ linear algebra
# ═══════════════════════════════════════════════════════════════

def mat_vec_f2(A, v, n):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_mul_f2(A, B, n):
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s ^= A[i][k] & B[k][j]
            C[i][j] = s
    return C

def mat_det_f2_n(A, n):
    M = [row[:] for row in A]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]:
                pivot = row; break
        if pivot is None: return 0
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
        for row in range(col+1, n):
            if M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(n)]
    return 1

def mat_identity(n):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def mat_eq(A, B, n):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))

def mat_inv_f2(A, n):
    """Compute inverse of A over F₂ via augmented row reduction."""
    M = [A[i][:] + [1 if i==j else 0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]: pivot = row; break
        if pivot is None: return None
        if pivot != col: M[col], M[pivot] = M[pivot], M[col]
        for row in range(n):
            if row != col and M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(2*n)]
    return [M[i][n:] for i in range(n)]

def enumerate_gl_f2(n):
    mats = []
    for bits in range(1 << (n*n)):
        A = [[(bits >> (i*n + j)) & 1 for j in range(n)] for i in range(n)]
        if mat_det_f2_n(A, n): mats.append(A)
    return mats


# ═══════════════════════════════════════════════════════════════
# TASK 3: Cross-check at (3,5) — do this first as a template
# ═══════════════════════════════════════════════════════════════

def task_3():
    print("=" * 72)
    print("TASK 3: CROSS-CHECK AT (3,5)")
    print("=" * 72)

    n, p = 3, 5
    N = 1 << n           # 8
    comp_mask = N - 1     # 7
    R = N // 2            # 4 complement pairs
    num_neg = (p - 1) // 2  # 2 negation pairs

    # Complement pairs
    comp_pairs = [(0,7), (1,6), (2,5), (3,4)]
    pair_reps = [0, 1, 2, 3]  # one representative per pair

    # IC type distribution: (Fr=2, H=0, Q=1, P=2) → (2, 0, 1, 2)
    type_dist = (2, 0, 1, 2)
    print(f"\n  Type distribution: {type_dist}")
    print(f"  Pair 0 (Frame {{0,7}}): type 2")
    print(f"  Pair 1 (H {{1,6}}): type 0")
    print(f"  Pair 2 (Q {{2,5}}): type 1")
    print(f"  Pair 3 (P {{3,4}}): type 2")

    # Enumerate surjections with this type distribution
    # f is determined by f(0), f(1), f(2), f(3) with f(7-x) = (-f(x)) % 5
    surjections = []
    for f0 in range(p):
        for f1 in range(p):
            for f2 in range(p):
                for f3 in range(p):
                    vals = [f0, f1, f2, f3]
                    comp_vals = [(-v) % p for v in vals]
                    fmap = {}
                    for i, (a, b) in enumerate(comp_pairs):
                        fmap[a] = vals[i]
                        fmap[b] = comp_vals[i]
                    if len(set(fmap.values())) < p:
                        continue

                    # Check type distribution
                    neg_pair_coverage = defaultdict(list)
                    ok = True
                    for i, (a, b) in enumerate(comp_pairs):
                        va, vb = fmap[a], fmap[b]
                        if va == 0 and vb == 0:
                            neg_pair_coverage['zero'].append(i)
                        else:
                            neg_key = frozenset({va, vb})
                            neg_pair_coverage[neg_key].append(i)

                    pair_types = [None]*4
                    for key, covering in neg_pair_coverage.items():
                        if key == 'zero':
                            for ci in covering: pair_types[ci] = 0
                        elif len(covering) == 1:
                            for ci in covering: pair_types[ci] = 1
                        else:
                            for ci in covering: pair_types[ci] = 2

                    if tuple(pair_types) == type_dist:
                        surj_tuple = tuple(fmap[x] for x in range(N))
                        surjections.append(surj_tuple)

    print(f"\n  Surjections with this type distribution: {len(surjections)} (expected 16)")

    # Compute V₄ kernel
    gl3 = enumerate_gl_f2(3)
    stab_111 = [A for A in gl3 if mat_vec_f2(A, 7, 3) == 7]
    pair_sets = [frozenset(cp) for cp in comp_pairs]

    def pair_perm(g, pairs, nn):
        perm = []
        for ps in pairs:
            gx = mat_vec_f2(g, min(ps), nn)
            for j, qs in enumerate(pairs):
                if gx in qs: perm.append(j); break
        return tuple(perm)

    v4_kernel = [g for g in stab_111 if pair_perm(g, pair_sets, 3) == (0,1,2,3)]
    print(f"  |V₄ kernel| = {len(v4_kernel)}")

    # Aut(Z₅) = {1,2,3,4}
    aut_z5 = [k for k in range(1, p) if pow(k, p-1, p) == 1]  # all nonzero mod p
    print(f"  |Aut(Z₅)| = {len(aut_z5)}")

    # Compute orbits
    surj_set = set(surjections)
    visited = set()
    orbits = []
    for s in surjections:
        if s in visited: continue
        orbit = set()
        for g in v4_kernel:
            g_inv = mat_inv_f2(g, 3)
            for alpha in aut_z5:
                t = tuple((alpha * s[mat_vec_f2(g_inv, x, 3)]) % p for x in range(N))
                if t in surj_set:
                    orbit.add(t)
        orbits.append(orbit)
        visited |= orbit

    print(f"  Orbits under V₄ × Aut(Z₅): {len(orbits)} (expected 1)")
    for i, orb in enumerate(orbits):
        print(f"    Orbit {i}: size {len(orb)}")

    # Check freeness
    is_free = True
    for g in v4_kernel:
        g_inv = mat_inv_f2(g, 3)
        for alpha in aut_z5:
            if mat_eq(g, mat_identity(3), 3) and alpha == 1: continue
            for s in surjections[:1]:
                t = tuple((alpha * s[mat_vec_f2(g_inv, x, 3)]) % p for x in range(N))
                if t == s: is_free = False
    print(f"  Action free? {is_free}")
    print()


# ═══════════════════════════════════════════════════════════════
# TASKS 1-2: (4,13) within-type-distribution analysis
# ═══════════════════════════════════════════════════════════════

def tasks_1_2():
    print("=" * 72)
    print("TASK 1: COUNT SURJECTIONS FOR ONE TYPE DISTRIBUTION AT (4,13)")
    print("=" * 72)

    n, p = 4, 13
    N = 1 << n            # 16
    comp_mask = N - 1      # 15
    R = N // 2             # 8 complement pairs
    num_neg = (p - 1) // 2  # 6 negation pairs

    # Complement pairs: {x, x^15}
    comp_pairs = []
    seen = set()
    for x in range(N):
        if x not in seen:
            cx = x ^ comp_mask
            seen.add(x); seen.add(cx)
            comp_pairs.append((min(x, cx), max(x, cx)))
    # comp_pairs = [(0,15), (1,14), (2,13), (3,12), (4,11), (5,10), (6,9), (7,8)]

    print(f"\n  Complement pairs: {comp_pairs}")

    # Representative type distribution: (2, 0, 1, 1, 1, 1, 1, 2)
    type_dist = (2, 0, 1, 1, 1, 1, 1, 2)
    print(f"  Type distribution: {type_dist}")
    print(f"  Pair 0 (Frame {{0,15}}): type 2")
    print(f"  Pair 1 ({{1,14}}): type 0 → both map to 0")
    print(f"  Pairs 2-6: type 1 → each uniquely covers a negation pair")
    print(f"  Pair 7 ({{7,8}}): type 2 → shares a negation pair with pair 0")

    # Negation pairs in Z₁₃: {1,12}, {2,11}, {3,10}, {4,9}, {5,8}, {6,7}
    neg_pairs = [(k, p-k) for k in range(1, num_neg+1)]
    print(f"  Negation pairs: {neg_pairs}")

    # Enumerate surjections with this type distribution.
    # Each representative has value in Z₁₃.
    # Pair 1 (type 0): rep maps to 0. Done.
    # Pairs 0,7 (type 2): share a negation pair. Choose which: 6 choices.
    #   Then orient each: rep → positive or negative. 2² = 4 orientations.
    # Pairs 2-6 (type 1): each assigned to a distinct remaining negation pair.
    #   5! = 120 assignments. Each oriented: 2 each → 2⁵ = 32.
    # Total = 6 × 4 × 120 × 32 = 92,160

    surjections = []
    pair_reps = [min(cp) for cp in comp_pairs]  # [0,1,2,3,4,5,6,7]

    type0_pairs = [i for i in range(8) if type_dist[i] == 0]  # [1]
    type1_pairs = [i for i in range(8) if type_dist[i] == 1]  # [2,3,4,5,6]
    type2_pairs = [i for i in range(8) if type_dist[i] == 2]  # [0,7]

    print(f"\n  Type 0 pairs: {type0_pairs}")
    print(f"  Type 1 pairs: {type1_pairs}")
    print(f"  Type 2 pairs: {type2_pairs}")

    # Enumerate systematically
    count = 0
    for shared_neg_idx in range(num_neg):  # which negation pair is shared by type-2
        shared_neg = neg_pairs[shared_neg_idx]  # e.g., (1, 12)
        remaining_neg = [neg_pairs[j] for j in range(num_neg) if j != shared_neg_idx]

        # Assign remaining 5 negation pairs to the 5 type-1 pairs
        for assignment in permutations(remaining_neg):
            # For each type-2 pair, choose orientation: rep → shared_neg[0] or shared_neg[1]
            for t2_orient in iterproduct([0,1], repeat=len(type2_pairs)):
                # For each type-1 pair, choose orientation
                for t1_orient in iterproduct([0,1], repeat=len(type1_pairs)):
                    vals = [None]*8
                    # Type 0: maps to 0
                    for pi in type0_pairs:
                        vals[pi] = 0
                    # Type 2: maps to shared_neg[orient]
                    for k, pi in enumerate(type2_pairs):
                        vals[pi] = shared_neg[t2_orient[k]]
                    # Type 1: maps to assignment[k][orient]
                    for k, pi in enumerate(type1_pairs):
                        vals[pi] = assignment[k][t1_orient[k]]

                    # Build full map
                    fmap = {}
                    for i, (a, b) in enumerate(comp_pairs):
                        fmap[a] = vals[i]
                        fmap[b] = (-vals[i]) % p

                    # Verify surjectivity
                    if len(set(fmap.values())) == p:
                        surj_tuple = tuple(fmap[x] for x in range(N))
                        surjections.append(surj_tuple)
                        count += 1

    surj_set_check = set(surjections)
    print(f"\n  Surjections enumerated: {count}")
    print(f"  Distinct surjections: {len(surj_set_check)}")
    print(f"  Expected: 6 × 4 × 120 × 32 = {6*4*120*32}")

    if count != len(surj_set_check):
        print(f"  WARNING: {count - len(surj_set_check)} duplicates found!")
    surjections = list(surj_set_check)

    # Verify: each surjection truly has the right type distribution
    def compute_type_dist(fmap_tuple, pairs, pp):
        neg_cov = defaultdict(list)
        for i, (a, b) in enumerate(pairs):
            va, vb = fmap_tuple[a], fmap_tuple[b]
            if va == 0 and vb == 0:
                neg_cov['zero'].append(i)
            else:
                neg_cov[frozenset({va, vb})].append(i)
        ptypes = [None]*len(pairs)
        for key, covering in neg_cov.items():
            if key == 'zero':
                for ci in covering: ptypes[ci] = 0
            elif len(covering) == 1:
                for ci in covering: ptypes[ci] = 1
            else:
                for ci in covering: ptypes[ci] = 2
        return tuple(ptypes)

    bad = 0
    for s in surjections[:100]:
        td = compute_type_dist(s, comp_pairs, p)
        if td != type_dist:
            bad += 1
    if bad == 0:
        print(f"  Type distribution verified on sample ✓")
    else:
        print(f"  WARNING: {bad} surjections have wrong type distribution!")

    # ── TASK 2: Orbits under (F₂)³ × Aut(Z₁₃) ──
    print("\n" + "=" * 72)
    print("TASK 2: ORBITS UNDER KERNEL × Aut(Z₁₃)")
    print("=" * 72)

    # Compute kernel: elements of Stab(1111) that fix all complement pairs as sets
    all_ones = comp_mask  # 15
    print("\n  Computing Stab(1111)...")

    # Rather than enumerating all GL(4,F₂), construct kernel directly.
    # Kernel = {g ∈ GL(4,F₂) : g(1111)=1111, g({x,x⊕1111})={x,x⊕1111} for all x}
    # This means for each complement pair {a,b}: g(a)∈{a,b} and g(b)∈{a,b}.
    # Since g is linear and g(0)=0, g(15)=15, for non-Frame pairs:
    # g(rep) = rep or g(rep) = rep⊕15.
    # The condition g(rep⊕15) = g(rep)⊕g(15) = g(rep)⊕15.
    # So if g(rep) = rep, then g(rep⊕15)=rep⊕15 (no swap).
    # If g(rep) = rep⊕15, then g(rep⊕15) = rep (swap).

    # Kernel element: for each non-Frame rep r ∈ {1,...,7}, choose swap or no-swap.
    # But g must be linear! So the choices aren't independent.
    # g(x) = x ⊕ (something depending on x). Since g(15)=15:
    # g(x) = x + φ(x)·15 for some linear functional φ: F₂⁴ → F₂ with φ(15)=0.
    # Wait, that's not quite right. Let me think more carefully.

    # Actually, the kernel consists of g such that g fixes every coset of ⟨1111⟩.
    # g(x) ∈ {x, x⊕1111}. Since g is linear: g(x) = x + λ(x)·1111 for some
    # linear functional λ: F₂⁴ → F₂. And g(1111) = 1111 + λ(1111)·1111 = 1111·(1+λ(1111)).
    # For this to equal 1111, need λ(1111) = 0.
    # So kernel = {g(x) = x + λ(x)·1111 : λ linear, λ(1111)=0}.
    # Linear functionals on F₂⁴ form F₂⁴ (dual space). Those vanishing at 1111
    # form a 3-dimensional subspace → 2³ = 8 kernel elements. ✓

    # Enumerate kernel elements explicitly
    # λ: F₂⁴ → F₂ linear, λ(1111) = 0
    # λ is determined by (λ(0001), λ(0010), λ(0100), λ(1000))
    # Constraint: λ(1111) = λ(0001)⊕λ(0010)⊕λ(0100)⊕λ(1000) = 0

    kernel = []
    for bits in range(16):  # (λ₀, λ₁, λ₂, λ₃)
        lam = [(bits >> i) & 1 for i in range(4)]
        if lam[0] ^ lam[1] ^ lam[2] ^ lam[3] != 0:
            continue
        # Build g(x) = x ⊕ λ(x)·1111
        # λ(x) = Σ lam[i] * x_i (mod 2)
        g_matrix = [[0]*4 for _ in range(4)]
        for col in range(4):
            e_col = 1 << col
            lam_e = lam[col]  # λ(e_col)
            img = e_col ^ (lam_e * all_ones)
            for row in range(4):
                g_matrix[row][col] = (img >> row) & 1
        kernel.append(g_matrix)

    print(f"  |Kernel| = {len(kernel)} (expected 8)")

    # Verify kernel elements fix all pairs
    for g in kernel:
        for x in range(N):
            gx = mat_vec_f2(g, x, 4)
            if gx != x and gx != (x ^ all_ones):
                print(f"  ERROR: g maps {x:04b} to {gx:04b}, not in pair!")
                break

    # Show kernel elements
    print("  Kernel elements (which reps are swapped):")
    for g in kernel:
        swapped = []
        for r in range(1, 8):  # non-Frame reps
            gr = mat_vec_f2(g, r, 4)
            if gr != r:
                swapped.append(r)
        print(f"    λ-vector: swaps reps {swapped}")

    # Aut(Z₁₃) = Z₁₃* = {1,2,...,12}
    aut_zp = list(range(1, p))
    print(f"\n  |Aut(Z₁₃)| = {len(aut_zp)}")
    print(f"  |Kernel × Aut(Z₁₃)| = {len(kernel)} × {len(aut_zp)} = {len(kernel)*len(aut_zp)}")

    # Compute inverse of each kernel element
    kernel_invs = [mat_inv_f2(g, 4) for g in kernel]

    # Action: (g, α)·f(x) = α · f(g⁻¹(x))
    surj_set = set(surjections)

    # Use union-find for orbit computation
    parent = {s: s for s in surjections}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb

    print(f"\n  Computing orbits on {len(surjections)} surjections...")
    orbit_count_progress = 0
    for s in surjections:
        for g_inv in kernel_invs:
            for alpha in aut_zp:
                t = tuple((alpha * s[mat_vec_f2(g_inv, x, 4)]) % p for x in range(N))
                if t in surj_set:
                    union(s, t)

    # Count orbits
    orbit_roots = set(find(s) for s in surjections)
    num_orbits = len(orbit_roots)

    # Compute orbit sizes
    orbit_sizes = Counter()
    for s in surjections:
        orbit_sizes[find(s)] += 1
    size_dist = sorted(Counter(orbit_sizes.values()).items())

    print(f"  Number of orbits: {num_orbits}")
    print(f"  Orbit size distribution: {size_dist}")
    if num_orbits == 1:
        print(f"  ✓ Single orbit — action is transitive")
    print(f"  Total surjections accounted for: {sum(orbit_sizes.values())}")

    # Check freeness
    print("\n  Checking freeness of action...")
    non_free_count = 0
    for g, g_inv in zip(kernel, kernel_invs):
        for alpha in aut_zp:
            if mat_eq(g, mat_identity(4), 4) and alpha == 1: continue
            for s in surjections[:20]:  # spot check
                t = tuple((alpha * s[mat_vec_f2(g_inv, x, 4)]) % p for x in range(N))
                if t == s:
                    non_free_count += 1
                    break

    if non_free_count == 0:
        print(f"  ✓ No non-identity element fixes any sampled surjection → likely free")
    else:
        print(f"  ✗ {non_free_count} non-identity elements fix some surjection → NOT free")

    # If free and transitive:
    if num_orbits == 1 and non_free_count == 0:
        print(f"\n  If free+transitive (regular), expected |surj| = |group| = {len(kernel)*len(aut_zp)}")
        print(f"  Actual |surj| = {len(surjections)}")
        if len(surjections) == len(kernel) * len(aut_zp):
            print(f"  ✓ REGULAR action confirmed")
        else:
            print(f"  ✗ Not regular: |surj| ≠ |group|")
            print(f"  Ratio: |surj|/|group| = {len(surjections)}/{len(kernel)*len(aut_zp)} = {len(surjections)/(len(kernel)*len(aut_zp)):.1f}")
            print(f"  This means orbits have size {len(kernel)*len(aut_zp)}, and there are {len(surjections)//(len(kernel)*len(aut_zp))} orbits")

    return surjections, kernel, kernel_invs, aut_zp, num_orbits, comp_pairs, p, n


# ═══════════════════════════════════════════════════════════════
# TASK 4: Characterize orbits (if > 1)
# ═══════════════════════════════════════════════════════════════

def task_4(surjections, kernel, kernel_invs, aut_zp, num_orbits, comp_pairs, p, n):
    if num_orbits <= 1:
        print("\n" + "=" * 72)
        print("TASK 4: ORBIT CHARACTERIZATION (SKIPPED — single orbit)")
        print("=" * 72)
        return

    print("\n" + "=" * 72)
    print("TASK 4: CHARACTERIZE ORBITS")
    print("=" * 72)

    N = 1 << n
    surj_set = set(surjections)

    # Recompute orbits explicitly
    visited = set()
    orbits = []
    for s in surjections:
        if s in visited: continue
        orbit = set()
        stack = [s]
        while stack:
            cur = stack.pop()
            if cur in visited: continue
            visited.add(cur)
            orbit.add(cur)
            for g_inv in kernel_invs:
                for alpha in aut_zp:
                    t = tuple((alpha * cur[mat_vec_f2(g_inv, x, n)]) % p for x in range(N))
                    if t in surj_set and t not in visited:
                        stack.append(t)
        orbits.append(orbit)

    print(f"\n  {len(orbits)} orbits, sizes: {[len(o) for o in orbits]}")

    # Invariant 1: difference table signature
    # For each surjection, compute the multiset of Δ_m(x) values
    def diff_signature(f_tuple):
        sig = []
        for m in range(1, N):
            row = []
            for x in range(N):
                row.append((f_tuple[x ^ m] - f_tuple[x]) % p)
            sig.append(tuple(sorted(row)))
        return tuple(sorted(sig))

    # Invariant 2: fiber partition (should be same for all in same type dist)
    def fiber_partition(f_tuple):
        fibers = Counter(f_tuple)
        return tuple(sorted(fibers.values(), reverse=True))

    # Invariant 3: "negation-pair profile" — which Z₁₃ elements appear in type-2 positions
    def neg_pair_profile(f_tuple, pairs):
        t2_vals = set()
        type_dist_local = (2, 0, 1, 1, 1, 1, 1, 2)
        for i, (a, b) in enumerate(pairs):
            if type_dist_local[i] == 2:
                t2_vals.add(frozenset({f_tuple[a], f_tuple[b]}))
        return frozenset(t2_vals)

    for i, orbit in enumerate(orbits):
        rep = sorted(orbit)[0]
        ds = diff_signature(rep)
        fp = fiber_partition(rep)
        npp = neg_pair_profile(rep, comp_pairs)

        print(f"\n  Orbit {i} (size {len(orbit)}):")
        print(f"    Representative: {rep}")
        print(f"    Fiber partition: {fp}")
        print(f"    Negation pairs used by type-2: {npp}")

        # Check if all elements in orbit have same diff signature
        sigs = set()
        for s in orbit:
            sigs.add(diff_signature(s))
        print(f"    Distinct diff signatures in orbit: {len(sigs)}")

    # Check if different orbits have different diff signatures
    orbit_sigs = []
    for orbit in orbits:
        rep = sorted(orbit)[0]
        orbit_sigs.append(diff_signature(rep))

    if len(set(orbit_sigs)) == len(orbits):
        print(f"\n  All orbits have DISTINCT diff signatures")
    else:
        print(f"\n  Some orbits share diff signatures: {len(set(orbit_sigs))} distinct out of {len(orbits)}")

    # What Z₁₃ value is shared by the type-2 pairs?
    print("\n  Type-2 shared values across orbits:")
    for i, orbit in enumerate(orbits):
        shared_vals = set()
        for s in list(orbit)[:5]:
            npp = neg_pair_profile(s, comp_pairs)
            shared_vals.add(frozenset(npp))
        print(f"    Orbit {i}: {shared_vals}")


# ═══════════════════════════════════════════════════════════════
# TASK 5: Does 互 at n=4 reduce the moduli?
# ═══════════════════════════════════════════════════════════════

def task_5(surjections, comp_pairs, p, n):
    print("\n" + "=" * 72)
    print("TASK 5: DOES 互 AT n=4 REDUCE THE MODULI?")
    print("=" * 72)

    N = 1 << n     # 16
    dim = 2 * n    # 8

    # Nuclear map at n=4
    def nuclear_n4(h):
        L = [(h >> i) & 1 for i in range(dim)]
        nlo = L[1] | (L[2] << 1) | (L[3] << 2) | (L[4] << 3)
        nup = L[3] | (L[4] << 1) | (L[5] << 2) | (L[6] << 3)
        return nlo | (nup << n)

    # The kernel of the nuclear map: vectors h with nuclear(h) = 0
    # From the matrix, kernel = {L : L₂=L₃=L₄=L₅=L₆=L₇=0} = span{e₁, e₈}
    # = span{(1,0,0,0,0,0,0,0), (0,0,0,0,0,0,0,1)}
    # In PG(3,F₂) × PG(3,F₂), these correspond to L₁ and L₈.

    nuc_kernel = []
    for h in range(1 << dim):
        if nuclear_n4(h) == 0:
            nuc_kernel.append(h)
    print(f"\n  Kernel of nuclear map: {len(nuc_kernel)} elements")
    for h in nuc_kernel:
        print(f"    {h:08b} (L₁={h&1}, L₈={(h>>7)&1})")

    # The kernel in "hexagram" terms: lower = (L₁,0,0,0), upper = (0,0,0,L₈)
    # These are hexagrams where only the outermost lines are nonzero.
    # In complement pair terms: the kernel spans elements 0b00000001=1 and 0b10000000=128
    # which are bit 0 and bit 7 of the 8-bit hexagram representation.

    print(f"\n  Kernel corresponds to the 2-dim subspace spanned by")
    print(f"  the outermost lines (L₁ and L₈).")

    # Which Fano-plane points does this fix?
    # In PG(3,F₂), the nuclear map drops L₁ and L₈.
    # The "fixed" structure is the image = 6-dim subspace.
    # The kernel is the 2-dim subspace {(L₁,0,0,0,0,0,0,L₈)}.

    # Question: what does this correspond to in terms of complement pairs?
    # A hexagram h = (lower, upper) where lower ∈ F₂⁴, upper ∈ F₂⁴.
    # lower = bits 0-3, upper = bits 4-7.
    # The "4-gram" complement pair of a 4-gram x is x ⊕ 1111.

    # Build transition matrix for nuclear map
    # For each surjection f, compute the "Z_p difference" of hexagrams
    # d(h) = f(upper) - f(lower) mod p, and d(nuclear(h)).

    print("\n  Computing 互 transition matrices for sample surjections...")

    # Use first few surjections
    for s_idx, s in enumerate(surjections[:3]):
        f = list(s)
        T = [[0]*p for _ in range(p)]
        for h in range(1 << dim):
            lo = h & (N-1)
            up = (h >> n) & (N-1)
            d_before = (f[up] - f[lo]) % p

            hn = nuclear_n4(h)
            nlo = hn & (N-1)
            nup = (hn >> n) & (N-1)
            d_after = (f[nup] - f[nlo]) % p

            T[d_before][d_after] += 1

        print(f"\n  Surjection {s_idx}: f = {s[:8]}...")
        print(f"  Transition matrix T (13×13, nonzero entries):")
        for d in range(p):
            row = [f"{T[d][dp]}" if T[d][dp] > 0 else "." for dp in range(p)]
            total = sum(T[d])
            print(f"    d={d:2d}: [{' '.join(f'{x:>3s}' for x in row)}] total={total}")

    # Check if all surjections in the same orbit give the same T
    print("\n  Checking if T is orbit-invariant...")

    def compute_T(surj):
        f = list(surj)
        T = [[0]*p for _ in range(p)]
        for h in range(1 << dim):
            lo = h & (N-1)
            up = (h >> n) & (N-1)
            d_before = (f[up] - f[lo]) % p
            hn = nuclear_n4(h)
            nlo = hn & (N-1)
            nup = (hn >> n) & (N-1)
            d_after = (f[nup] - f[nlo]) % p
            T[d_before][d_after] += 1
        return tuple(tuple(row) for row in T)

    # Sample surjections and check T
    T_values = set()
    for s in surjections[:min(200, len(surjections))]:
        T_values.add(compute_T(s))

    print(f"  Distinct transition matrices among first {min(200, len(surjections))} surjections: {len(T_values)}")

    if len(T_values) == 1:
        print(f"  ✓ All sampled surjections give the SAME T → 互 is type-distribution-invariant")
    else:
        print(f"  ✗ Multiple T matrices → 互 distinguishes surjections within a type distribution")
        print(f"  This means 互 can potentially reduce the moduli!")

        # Check if T is an orbit invariant
        # Group T matrices by orbit
        if len(surjections) <= 5000:
            print(f"\n  Full check: computing T for all {len(surjections)} surjections...")
            T_by_surj = {}
            for s in surjections:
                T_by_surj[s] = compute_T(s)

            # How many distinct T?
            all_T = set(T_by_surj.values())
            print(f"  Total distinct T matrices: {len(all_T)}")

            # If T varies, does it distinguish orbits?
            # T is invariant under Aut(Z_p): if (g,α)·f gives T', then T'[α·d][α·d'] = T[d][d']
            # So T is only invariant up to row/column permutation by α.
            # Define a canonical form for T: sort rows and columns somehow.
            def T_canonical(T_mat):
                # T under α: T'[d][d'] = T[α⁻¹·d][α⁻¹·d']
                # Canonical = minimum over all α
                candidates = []
                for alpha in range(1, p):
                    alpha_inv = pow(alpha, p-2, p)
                    T_perm = tuple(
                        tuple(T_mat[(alpha_inv * d) % p][(alpha_inv * dp) % p] for dp in range(p))
                        for d in range(p)
                    )
                    candidates.append(T_perm)
                return min(candidates)

            canonical_T = set()
            for T_mat in all_T:
                canonical_T.add(T_canonical(T_mat))
            print(f"  Distinct T up to Aut(Z₁₃) row/col permutation: {len(canonical_T)}")

            # Also account for kernel action on T
            # Kernel swaps within complement pairs, which permutes elements of F₂⁴.
            # This doesn't change the Z_p values, so T is kernel-invariant.
            # So T_canonical should be an orbit invariant.
            print(f"  → These {len(canonical_T)} canonical T classes should match orbit count")
        else:
            print(f"  (Too many surjections for full T computation)")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()

    output_path = "/home/quasar/nous/memories/iching/unification/within_type_orbits_output.txt"
    with open(output_path, 'w') as log_file:
        tee = Tee(sys.stdout, log_file)
        old_stdout = sys.stdout
        sys.stdout = tee

        try:
            task_3()
            surjections, kernel, kernel_invs, aut_zp, num_orbits, comp_pairs, p, nn = tasks_1_2()
            task_4(surjections, kernel, kernel_invs, aut_zp, num_orbits, comp_pairs, p, nn)
            task_5(surjections, comp_pairs, p, nn)
        finally:
            sys.stdout = old_stdout

    print(f"\nOutput saved to {output_path}")
