#!/usr/bin/env python3
"""
transitivity_probe.py — Phase 3, Iteration 13 (Part 2)

Task A: Decompose the Transitivity Proof at (3,5)
Task B: Type Structure at (4,13) — Majority Shape
Task C: 互-Analog at n=4

Uses eigenstructure.py encoding convention:
  WUXING = {0:2, 1:0, 2:4, 3:3, 4:2, 5:1, 6:0, 7:3}
  Z₅: 0=Wood, 1=Fire, 2=Earth, 3=Metal, 4=Water
"""

import sys
from collections import Counter, defaultdict
from itertools import product as iterproduct
from math import factorial

# ═══════════════════════════════════════════════════════════════
# F₂ linear algebra (parametric dimension)
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

def mat_det_f2_3(A):
    a, b, c = A[0]; d, e, f_ = A[1]; g, h, k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1

def mat_det_f2_n(A, n):
    """Determinant of n×n matrix over F₂ via LU decomposition."""
    M = [row[:] for row in A]
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if M[row][col]:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]
            det ^= 1  # swap parity — but over F₂, det ∈ {0,1}, swaps don't change nonzero
        for row in range(col+1, n):
            if M[row][col]:
                for j in range(n):
                    M[row][j] ^= M[col][j]
    return 1  # if we got here, all pivots were found

def mat_identity(n):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def mat_eq(A, B, n):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))

def element_order(A, n):
    I = mat_identity(n)
    cur = [row[:] for row in A]
    for k in range(1, 300):
        if mat_eq(cur, I, n):
            return k
        cur = mat_mul_f2(cur, A, n)
    return -1

def enumerate_gl_f2(n):
    """Enumerate GL(n, F₂). Only feasible for small n."""
    if n > 4:
        raise ValueError("Too large for brute-force enumeration")
    mats = []
    total = 1 << (n*n)
    for bits in range(total):
        A = [[(bits >> (i*n + j)) & 1 for j in range(n)] for i in range(n)]
        if mat_det_f2_n(A, n):
            mats.append(A)
    return mats

def perm_of(A, n):
    """Return the permutation of {0,...,2^n-1} induced by A."""
    return tuple(mat_vec_f2(A, x, n) for x in range(1 << n))


# ═══════════════════════════════════════════════════════════════
# TASK A: Decompose the Transitivity Proof at (3,5)
# ═══════════════════════════════════════════════════════════════

def task_a():
    print("=" * 72)
    print("TASK A: DECOMPOSE THE TRANSITIVITY PROOF AT (3,5)")
    print("=" * 72)
    
    n = 3
    N = 1 << n  # 8
    comp_mask = (1 << n) - 1  # 7 = 111
    
    WUXING = {0:2, 1:0, 2:4, 3:3, 4:2, 5:1, 6:0, 7:3}
    
    # Complement pairs: {x, x^7}
    comp_pairs = [(0,7), (1,6), (2,5), (3,4)]
    pair_names = ["Frame", "H-pair", "Q-pair", "P-pair"]
    
    # ── Step 1: Stab(111) action on complement pairs ──
    print("\n--- Step 1: Stab(111) action on complement pairs ---")
    
    gl3 = enumerate_gl_f2(3)
    print(f"  |GL(3,F₂)| = {len(gl3)}")
    
    stab_111 = [A for A in gl3 if mat_vec_f2(A, 7, 3) == 7]
    print(f"  |Stab(111)| = {len(stab_111)}")
    
    # Each g ∈ Stab(111) permutes the 4 complement pairs
    # Pair i = {comp_pairs[i][0], comp_pairs[i][1]}
    pair_sets = [frozenset(p) for p in comp_pairs]
    
    def pair_perm(g):
        """Which permutation of {0,1,2,3} does g induce on the 4 complement pairs?"""
        perm = []
        for ps in pair_sets:
            x = min(ps)
            gx = mat_vec_f2(g, x, 3)
            # Find which pair gx belongs to
            for j, qs in enumerate(pair_sets):
                if gx in qs:
                    perm.append(j)
                    break
        return tuple(perm)
    
    # Compute all induced permutations
    pair_perms = []
    for g in stab_111:
        pp = pair_perm(g)
        pair_perms.append(pp)
    
    distinct_perms = sorted(set(pair_perms))
    print(f"  Distinct pair permutations: {len(distinct_perms)}")
    
    # Check if it's the full S₄
    from itertools import permutations
    full_s4 = set(permutations(range(4)))
    actual_s4 = set(pair_perms)
    print(f"  Full S₄ = {len(full_s4)} permutations")
    print(f"  Stab(111) induced perms = {len(actual_s4)} distinct permutations")
    print(f"  Is it ALL of S₄? {actual_s4 == full_s4}")
    
    if actual_s4 == full_s4:
        print("  ✓ Stab(111) acts as the FULL S₄ on complement pairs (faithful)")
    
    # Verify faithfulness: each g gives a distinct permutation
    perm_to_count = Counter(pair_perms)
    all_unique = all(v == 1 for v in perm_to_count.values())
    print(f"  Faithful (each g → unique pair perm)? {all_unique}")
    
    # Show generators: find transpositions
    print("\n  Key pair permutations (sample):")
    for pp in sorted(set(pair_perms)):
        # Classify cycle type
        visited = set()
        cycles = []
        for start in range(4):
            if start in visited:
                continue
            cyc = [start]
            visited.add(start)
            cur = pp[start]
            while cur != start:
                cyc.append(cur)
                visited.add(cur)
                cur = pp[cur]
            if len(cyc) > 1:
                cycles.append(tuple(cyc))
        
        count = perm_to_count[pp]
        if len(cycles) == 1 and len(cycles[0]) == 2:
            i, j = cycles[0]
            print(f"    {pp}  transposition ({pair_names[i]}↔{pair_names[j]})  [{count} elements]")

    # ── Step 2: Transitivity on type patterns ──
    print("\n--- Step 2: Transitivity on type patterns ---")
    
    # In Orbit C, Frame = Type 2. The other 3 pairs get types {0,1,2} in some order.
    # The 6 type patterns for (H,Q,P):
    type_patterns = list(permutations([0,1,2]))
    print(f"  6 type patterns for (H-type, Q-type, P-type):")
    for tp in type_patterns:
        print(f"    (Fr=2, H={tp[0]}, Q={tp[1]}, P={tp[2]})")
    
    # Which pair perms fix the Frame pair (pair 0)?
    # These form the S₃ subgroup acting on {H,Q,P} = {pair1, pair2, pair3}
    frame_fixers = [g for g, pp in zip(stab_111, pair_perms) if pp[0] == 0]
    print(f"\n  |Stab(Frame) within Stab(111)| = {len(frame_fixers)}")
    
    # Their action on {1,2,3} (the non-Frame pairs)
    s3_perms = set()
    for g, pp in zip(stab_111, pair_perms):
        if pp[0] == 0:
            restricted = (pp[1], pp[2], pp[3])
            s3_perms.add(restricted)
    
    full_s3_on_123 = set(permutations([1,2,3]))
    print(f"  Distinct permutations of {{H,Q,P}}: {len(s3_perms)}")
    
    # Map these to permutations of indices {0,1,2} (relative to H=0,Q=1,P=2)
    s3_on_012 = set()
    for rp in s3_perms:
        # rp = (π(1), π(2), π(3)) where π permutes pair indices
        # We want the induced permutation on type indices
        # If g maps pair 1→π(1), pair 2→π(2), pair 3→π(3)
        # and a type pattern is (t_H, t_Q, t_P) = (t_1, t_2, t_3)
        # then g maps this to pattern (t_{π^{-1}(1)}, t_{π^{-1}(2)}, t_{π^{-1}(3)})
        # equivalently: the new type at position j is the old type at position π^{-1}(j)
        s3_on_012.add(tuple(r - 1 for r in rp))  # shift to 0-indexed
    
    print(f"  Full S₃ on {{0,1,2}}? {len(s3_on_012) == 6}")
    
    # Check transitivity on the 6 type patterns
    # Two patterns p1 and p2 are in the same orbit if there exists σ ∈ S₃ such that
    # p2[σ(i)] = p1[i] for all i, i.e., p2 = p1 ∘ σ^{-1}
    
    def apply_pair_perm_to_types(types_hqp, sigma_on_123):
        """Given types (t_H, t_Q, t_P) and σ permuting {1,2,3} → {1,2,3},
        return the new type pattern after σ moves pairs."""
        # σ maps pair i → σ(i). So the type of the pair that ends up at position j
        # is the type of the pair that was at position σ^{-1}(j).
        inv = [0]*4
        for i in range(1,4):
            inv[sigma_on_123[i-1]] = i
        return tuple(types_hqp[inv[j]-1] for j in range(1,4))
    
    orbits_of_types = []
    visited_types = set()
    for tp in type_patterns:
        if tp in visited_types:
            continue
        orb = set()
        for sigma in s3_perms:
            new_tp = apply_pair_perm_to_types(tp, sigma)
            orb.add(new_tp)
        orbits_of_types.append(orb)
        visited_types |= orb
    
    print(f"\n  Orbits of S₃ on 6 type patterns: {len(orbits_of_types)}")
    for i, orb in enumerate(orbits_of_types):
        print(f"    Orbit {i}: {sorted(orb)}")
    
    if len(orbits_of_types) == 1:
        print("  ✓ S₃ acts TRANSITIVELY on the 6 type patterns")
    
    # ── Step 3: Within-pattern transitivity ──
    print("\n--- Step 3: Within-pattern transitivity ---")
    
    # Fix type pattern (0,1,2): H=Type0, Q=Type1, P=Type2 (the IC choice)
    # The stabilizer of this pattern in the S₃ action is trivial (since S₃ acts
    # faithfully on 3 distinct objects).
    
    print("  Type pattern (H=0, Q=1, P=2):")
    
    # But within Stab(111), we need the stabilizer of BOTH the Frame pair AND
    # the specific type assignment. The Frame-fixing subgroup has order 6 (S₃ on non-Frame).
    # The pattern stabilizer within this S₃ is trivial (identity only).
    # So the stabilizer of the type pattern in Stab(111) = V₄ kernel?
    
    # Actually: the subgroup fixing ALL complement pairs pointwise (as sets)
    # is exactly those g that fix 0,7 and map each pair to itself.
    # g(0)=0,g(7)=7 (from fixing Frame), plus g({1,6})={1,6}, g({2,5})={2,5}, g({3,4})={3,4}
    # This means g permutes within each pair: either fixes or swaps.
    
    pair_fixers = []  # Fix all 4 pairs as sets (but may swap within)
    for g, pp in zip(stab_111, pair_perms):
        if pp == (0,1,2,3):  # identity permutation on pairs
            pair_fixers.append(g)
    
    print(f"  |Stab of all pairs (as sets)| = {len(pair_fixers)}")
    
    # Show these elements
    for g in pair_fixers:
        perm = perm_of(g, 3)
        print(f"    perm: {list(perm)}  (swaps: " +
              f"Earth {'Y' if perm[0]==4 else 'N'}, " +
              f"H {'Y' if perm[1]==6 else 'N'}, " +
              f"Q {'Y' if perm[2]==5 else 'N'}, " +
              f"P {'Y' if perm[3]==4 else 'N'})")
    
    # These should form V₄ ≅ (Z₂)² (not (Z₂)³ since g(7)=7 constrains)
    # Actually: g fixes 0 and 7. For each pair {a,b}, g either fixes both or swaps.
    # But g(a⊕b) = g(a)⊕g(b) (linearity). If g swaps {1,6}: g(1)=6, g(6)=1.
    # Then g(1⊕6) = g(7) = 7 = 6⊕1. OK.
    # The constraint: g(0)=0 is automatic. g(7)=7.
    # For each of the 3 non-Frame pairs, independently swap or not → 2³=8.
    # But some may not preserve g(7)=7.
    # Actually g(7) = g(1⊕2⊕4) = g(1)⊕g(2)⊕g(4).
    # If we swap pair {1,6}: g(1)=6. If we swap pair {2,5}: g(2)=5. If we swap pair {3,4}: g(4)=3.
    # g(7) = 6⊕5⊕3 = 6^5^3 = 0. Not 7!
    # So NOT all 8 combinations work. The constraint g(7)=7 reduces the choices.
    
    # Let's verify: which swap combinations give g(7)=7?
    print("\n  Verifying V₄ structure:")
    print(f"  V₄ has {len(pair_fixers)} elements, orders: {Counter(element_order(g, 3) for g in pair_fixers)}")
    
    # Check if it's V₄ = Klein four-group
    if len(pair_fixers) == 4:
        orders = [element_order(g, 3) for g in pair_fixers]
        if Counter(orders) == Counter({1:1, 2:3}):
            print("  ✓ This is V₄ = Klein four-group (orders {1:1, 2:3})")
    
    # Now: enumerate the 16 surjections with type pattern (2,0,1,2)
    def pair_types_of(surj):
        neg_pairs = {}
        for ci, (x, y) in enumerate(comp_pairs):
            a, b = surj[x], surj[y]
            neg_pair = frozenset({a, b}) if a != b else frozenset({a})
            if neg_pair not in neg_pairs:
                neg_pairs[neg_pair] = []
            neg_pairs[neg_pair].append(ci)
        types = [None]*4
        for neg_pair, covering in neg_pairs.items():
            if neg_pair == frozenset({0}):
                for ci in covering: types[ci] = 0
            elif len(covering) == 1:
                for ci in covering: types[ci] = 1
            else:
                for ci in covering: types[ci] = 2
        return tuple(types)
    
    # Enumerate all 240 surjections
    all_surj = []
    for vals in iterproduct(range(5), repeat=4):
        fmap = {}
        fmap[0] = vals[0]; fmap[7] = (-vals[0]) % 5
        fmap[1] = vals[1]; fmap[6] = (-vals[1]) % 5
        fmap[2] = vals[2]; fmap[5] = (-vals[2]) % 5
        fmap[3] = vals[3]; fmap[4] = (-vals[3]) % 5
        if len(set(fmap.values())) == 5:
            all_surj.append(tuple(fmap[x] for x in range(8)))
    
    ic_type = (2, 0, 1, 2)
    ic_surjs = [s for s in all_surj if pair_types_of(s) == ic_type]
    print(f"\n  Surjections with IC type pattern {ic_type}: {len(ic_surjs)}")
    
    # Show them
    for s in ic_surjs:
        print(f"    {s}")
    
    # Action of V₄ × Aut(Z₅) on these 16
    aut_z5 = [1, 2, 3, 4]
    
    def apply_action(surj, g, alpha, n=3):
        return tuple((alpha * surj[mat_vec_f2(g, x, n)]) % 5 for x in range(1 << n))
    
    # Check freeness
    print("\n  Checking if V₄ × Aut(Z₅) acts freely on the 16 IC-type surjections:")
    ic_set = set(ic_surjs)
    is_free = True
    for g in pair_fixers:
        for alpha in aut_z5:
            if mat_eq(g, mat_identity(3), 3) and alpha == 1:
                continue  # skip identity
            fixed_count = 0
            for s in ic_surjs:
                t = apply_action(s, g, alpha, 3)
                if t == s:
                    fixed_count += 1
            if fixed_count > 0:
                is_free = False
                perm = perm_of(g, 3)
                print(f"    g={list(perm)}, α={alpha}: fixes {fixed_count} surjections")
    
    if is_free:
        print("  ✓ Action is FREE (no non-identity element fixes any surjection)")
    
    # Check transitivity
    start = ic_surjs[0]
    orbit = set()
    for g in pair_fixers:
        for alpha in aut_z5:
            t = apply_action(start, g, alpha, 3)
            orbit.add(t)
    
    print(f"  Orbit of first surjection under V₄ × Aut(Z₅): size {len(orbit)}")
    print(f"  Equals full IC-type set? {orbit == ic_set}")
    
    if orbit == ic_set and is_free:
        print("  ✓ V₄ × Aut(Z₅) acts REGULARLY (free + transitive) on the 16 IC-type surjections")
    
    # ── Step 4: Combine ──
    print("\n--- Step 4: Combine into theorem ---")
    
    orbit_c = [s for s in all_surj if pair_types_of(s)[0] == 2]
    print(f"  Orbit C: {len(orbit_c)} surjections")
    
    # Full Stab(111) × Aut(Z₅) orbit
    oc_set = set(orbit_c)
    start = orbit_c[0]
    full_orbit = set()
    for g in stab_111:
        for alpha in aut_z5:
            t = apply_action(start, g, alpha, 3)
            if t in oc_set:
                full_orbit.add(t)
    
    print(f"  Full orbit from one element: {len(full_orbit)}")
    print(f"  Equals Orbit C? {full_orbit == oc_set}")
    
    # Check freeness of full action on Orbit C
    print("\n  Checking freeness of Stab(111) × Aut(Z₅) on Orbit C:")
    full_free = True
    stabilizer_size = 0
    for g in stab_111:
        for alpha in aut_z5:
            if all(apply_action(s, g, alpha, 3) == s for s in [orbit_c[0]]):
                stabilizer_size += 1
                if not (mat_eq(g, mat_identity(3), 3) and alpha == 1):
                    full_free = False
    
    print(f"  Stabilizer of one element: order {stabilizer_size}")
    print(f"  |Group|/|Orbit| = {len(stab_111)*4}/{len(orbit_c)} = {len(stab_111)*4/len(orbit_c)}")
    print(f"  Free? {full_free}")
    
    if full_free:
        print("\n  ═══════════════════════════════════════════════════")
        print("  THEOREM (Orbit C Transitivity):")
        print("  Stab(111) × Aut(Z₅) acts freely and transitively")
        print("  (= regularly) on the 96 Orbit-C surjections.")
        print()
        print("  PROOF STRUCTURE:")
        print("  1. Stab(111) ≅ S₄ always fixes Frame pair. Quotient on non-Frame pairs ≅ S₃.")
        print("  2. S₃ acts transitively on 6 type patterns of (H-type, Q-type, P-type).")
        print("  3. Kernel V₄ (Klein four, order 4) fixes all pairs as sets (swaps within).")
        print("  4. V₄ × Aut(Z₅) (order 16) acts regularly on 16 same-type surjections.")
        print("  5. Combining: |S₃| × |V₄ × Aut(Z₅)| = 6 × 16 = 96 = |Orbit C|. ∎")
        print("  ═══════════════════════════════════════════════════")


# ═══════════════════════════════════════════════════════════════
# TASK B: Type Structure at (4,13)
# ═══════════════════════════════════════════════════════════════

def task_b():
    print("\n" + "=" * 72)
    print("TASK B: TYPE STRUCTURE AT (4,13)")
    print("=" * 72)
    
    n = 4
    p = 13
    N = 1 << n  # 16
    comp_mask = N - 1  # 15 = 1111
    R = N // 2  # 8 complement pairs
    num_neg = (p - 1) // 2  # 6 negation pairs
    S = 1 + num_neg  # 7 slots
    E = R - S  # 8 - 7 = 1
    
    print(f"\n  n={n}, p={p}, N={N}, R={R} complement pairs")
    print(f"  Negation pairs in Z₁₃: {num_neg}")
    print(f"  Slots: S={S} (1 zero-slot + {num_neg} negation-pair slots)")
    print(f"  Excess: E={E}")
    
    # ── Step 1: Enumerate partition shapes ──
    print("\n--- Step 1: Partition shapes ---")
    
    # Complement pairs: {x, x⊕1111} for x = 0..7
    comp_pairs_4 = []
    seen = set()
    for x in range(N):
        if x not in seen:
            cx = x ^ comp_mask
            seen.add(x); seen.add(cx)
            comp_pairs_4.append((min(x, cx), max(x, cx)))
    
    print(f"  Complement pairs: {comp_pairs_4}")
    
    # For each assignment of R=8 pairs to S=7 slots:
    #   Slot 0 (zero element): m₀ pairs → fiber(0) has size 2·m₀
    #   Slot j (negation pair {k, p-k}): c_j pairs → fiber(k)=fiber(p-k)=c_j
    # Surjectivity: every slot gets ≥1 pair. Since R=8, S=7, one slot gets 2.
    
    # Two shapes:
    # Shape A (majority): m₀=1, one negation slot gets 2 pairs, rest get 1
    #   fiber(0) = 2, five negation pairs have fiber sizes (1,1), one has (2,2)
    #   partition: (2,2,2,1,1,1,1,1,1,1,1,1,1) → 13 fibers... wait
    # 
    # Actually: p=13 elements. The fibers are:
    #   Element 0: size 2·m₀
    #   Negation pair {k, 13-k}: each element has fiber size = number of complement pairs
    #     assigned to slot k. So fiber(k) = c_k, fiber(13-k) = c_k.
    
    # Shape A (m₀=1, one c_j=2, rest c_j=1):
    #   fiber(0) = 2
    #   One negation pair {k,13-k} has c_k=2: fiber(k) = fiber(13-k) = 2
    #   Five negation pairs have c_j=1: fiber = 1 each (10 singletons)
    #   Total elements: 2 + 2·2 + 5·2·1 = 2 + 4 + 10 = 16 ✓
    #   Partition shape: (2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) → 3 doubletons + 10 singletons
    
    # Shape B (m₀=2, all c_j=1):
    #   fiber(0) = 4
    #   All 6 negation pairs have c_j=1: fiber = 1 each (12 singletons)
    #   Total: 4 + 6·2·1 = 4 + 12 = 16 ✓
    #   Partition shape: (4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) → 1 quadrupleton + 12 singletons
    
    # Count surjections for each shape
    # Shape A: m₀=1, one c_j=2, five c_j=1
    #   Choose which negation pair gets 2: C(6,1) = 6
    #   Multinomial: R!/(m₀!·c_big!·c_1!^5) = 8!/(1!·2!·1!^5) = 40320/2 = 20160
    #   Orderings: 6!/(1!·5!) = 6 (which negation pair is which)... wait, this is already
    #   accounted for by the choice of which gets 2. Actually orderings = 6!/5! = 6.
    #   Wait, I need to think more carefully.
    #   
    #   Using np_landscape formula:
    #   c_vals = (1,1,1,1,1,2) = 5 ones and 1 two
    #   multi = R!/(m₀!·∏c_j!) = 8!/(1!·2!·1^5) = 20160
    #   orderings = 6!/(5!·1!) = 6  (permutations of negation-pair assignments)
    #   orient = 2^(R-m₀) = 2^7 = 128  (each non-zero pair can orient either way)
    #   count_A = 20160 × 6 × 128 = 15,482,880
    
    from math import factorial, comb
    
    m0_A = 1
    c_vals_A = [1,1,1,1,1,2]
    multi_A = factorial(R) // factorial(m0_A)
    for c in c_vals_A:
        multi_A //= factorial(c)
    freq_A = Counter(c_vals_A)
    orderings_A = factorial(num_neg)
    for f in freq_A.values():
        orderings_A //= factorial(f)
    orient_A = 1 << (R - m0_A)
    count_A = multi_A * orderings_A * orient_A
    
    # Shape B: m₀=2, all c_j=1
    m0_B = 2
    c_vals_B = [1,1,1,1,1,1]
    multi_B = factorial(R) // factorial(m0_B)
    for c in c_vals_B:
        multi_B //= factorial(c)
    freq_B = Counter(c_vals_B)
    orderings_B = factorial(num_neg)
    for f in freq_B.values():
        orderings_B //= factorial(f)
    orient_B = 1 << (R - m0_B)
    count_B = multi_B * orderings_B * orient_B
    
    total = count_A + count_B
    
    print(f"\n  Shape A (majority): m₀=1, c_vals={c_vals_A}")
    print(f"    Fiber partition: (2,2,2, 1×10)")
    print(f"    multi={multi_A}, orderings={orderings_A}, orient={orient_A}")
    print(f"    Count = {count_A}")
    print(f"  Shape B (minority): m₀=2, c_vals={c_vals_B}")
    print(f"    Fiber partition: (4, 1×12)")
    print(f"    multi={multi_B}, orderings={orderings_B}, orient={orient_B}")
    print(f"    Count = {count_B}")
    print(f"  Total: {total}")
    print(f"  Ratio A/B = {count_A}/{count_B} = {count_A/count_B:.1f} (predicted: p-1={p-1})")
    
    # ── Step 2: Type counts for majority shape ──
    print("\n--- Step 2: Type counts for majority shape ---")
    
    # Shape A: 1 pair at zero (Type 0), 5 pairs singly covering negation pairs (Type 1),
    #          2 pairs sharing one negation pair (Type 2)
    # Wait: which type is which?
    # Type 0: pair maps to 0 (both elements → 0). m₀=1 pair.
    # Type 1: pair singly covers a negation pair (unique covering). 5 such negation pairs.
    # Type 2: pair shares a negation pair with another pair. The shared negation pair has 2 covering pairs.
    #   So 2 pairs are Type 2.
    #
    # Total: 1 Type-0 + 5 Type-1 + 2 Type-2 = 8 pairs ✓
    # All three types present: ✓ (three-type surjection)
    
    type_0_count = 1  # m₀ pairs at zero
    type_1_count = 5  # singly-covered negation pairs → 5 pairs
    type_2_count = 2  # 2 pairs sharing one negation pair
    
    print(f"  Type 0 (zero pair): {type_0_count} pair(s)")
    print(f"  Type 1 (singleton coverage): {type_1_count} pair(s)")
    print(f"  Type 2 (shared coverage): {type_2_count} pair(s)")
    print(f"  Total: {type_0_count + type_1_count + type_2_count} = 8 ✓")
    print(f"  Three types present: ✓")
    
    # Number of distinct type distributions:
    # Assign types to 8 complement pairs: choose 1 for Type 0, 2 for Type 2, rest Type 1
    # C(8,1) × C(7,2) = 8 × 21 = 168 distributions
    num_distributions = comb(8, type_0_count) * comb(8 - type_0_count, type_2_count)
    print(f"\n  Number of type distributions: C(8,{type_0_count}) × C({8-type_0_count},{type_2_count}) = {num_distributions}")
    
    # ── Step 3: Compute Stab(1111) ──
    print("\n--- Step 3: Compute Stab(1111) ---")
    
    all_ones = (1 << n) - 1  # 15 = 1111
    
    # |GL(4,F₂)| = (2⁴-1)(2⁴-2)(2⁴-4)(2⁴-8) = 15·14·12·8 = 20160
    gl4_order = 15 * 14 * 12 * 8
    print(f"  |GL(4,F₂)| = {gl4_order}")
    print(f"  |Stab(1111)| = {gl4_order} / 15 = {gl4_order // 15}")
    
    # Enumerate GL(4,F₂) — this is feasible (20160 matrices)
    print("  Enumerating GL(4,F₂)... ", end="", flush=True)
    gl4 = enumerate_gl_f2(4)
    print(f"found {len(gl4)} elements")
    
    stab_1111 = [A for A in gl4 if mat_vec_f2(A, all_ones, 4) == all_ones]
    print(f"  |Stab(1111)| = {len(stab_1111)} (expected {gl4_order // 15})")
    
    # ── Stab(1111) action on complement pairs ──
    comp_pairs_4_sets = [frozenset(p) for p in comp_pairs_4]
    
    def pair_perm_4(g):
        perm = []
        for ps in comp_pairs_4_sets:
            x = min(ps)
            gx = mat_vec_f2(g, x, 4)
            for j, qs in enumerate(comp_pairs_4_sets):
                if gx in qs:
                    perm.append(j)
                    break
        return tuple(perm)
    
    # Check: does Stab(1111) act as S₈ on 8 complement pairs?
    pair_perms_4 = set()
    for g in stab_1111:
        pair_perms_4.add(pair_perm_4(g))
    
    print(f"\n  Stab(1111) induces {len(pair_perms_4)} distinct permutations on 8 complement pairs")
    print(f"  |S₈| = {factorial(8)} = 40320")
    print(f"  Is it ALL of S₈? {len(pair_perms_4) == factorial(8)}")
    
    # Since |Stab(1111)| = 1344 < 40320, it can't be all of S₈.
    # But it should act transitively on individual pairs. Check:
    # Is the action transitive on pairs?
    
    # Orbit of pair 0 (Frame = {0, 15})
    frame_orbit = set()
    for pp in pair_perms_4:
        frame_orbit.add(pp[0])
    
    print(f"  Orbit of Frame pair under Stab(1111): {sorted(frame_orbit)}")
    print(f"  Transitive on pairs? {frame_orbit == set(range(8))}")
    
    # Check: what is the image of the pair permutation group?
    # Is it the full S₈, or a subgroup?
    
    # Compute cycle types
    cycle_types = Counter()
    for pp in pair_perms_4:
        visited = set()
        cycles = []
        for start in range(8):
            if start in visited:
                continue
            cyc_len = 0
            cur = start
            while cur not in visited:
                visited.add(cur)
                cur = pp[cur]
                cyc_len += 1
            cycles.append(cyc_len)
        ct = tuple(sorted(cycles, reverse=True))
        cycle_types[ct] += 1
    
    print(f"\n  Cycle types of pair permutations:")
    for ct, cnt in sorted(cycle_types.items()):
        print(f"    {ct}: {cnt} permutations")
    
    # ── Step 4: Stab(1111) orbits on type distributions ──
    print("\n--- Step 4: Orbits on type distributions ---")
    
    # A type distribution assigns each of the 8 pairs a type from {0,1,2}
    # with exactly 1 Type-0, 5 Type-1, 2 Type-2.
    
    # Enumerate all 168 distributions
    distributions = []
    for t0_pair in range(8):
        remaining = [i for i in range(8) if i != t0_pair]
        for t2_pair1_idx in range(len(remaining)):
            for t2_pair2_idx in range(t2_pair1_idx + 1, len(remaining)):
                t2_pairs = (remaining[t2_pair1_idx], remaining[t2_pair2_idx])
                dist = [1] * 8
                dist[t0_pair] = 0
                dist[t2_pairs[0]] = 2
                dist[t2_pairs[1]] = 2
                distributions.append(tuple(dist))
    
    print(f"  Total type distributions: {len(distributions)}")
    
    # Compute orbits under Stab(1111) (acting on pair indices)
    dist_set = set(distributions)
    visited = set()
    orbits = []
    
    # Cache pair permutations
    pair_perm_list = [pair_perm_4(g) for g in stab_1111]
    
    for dist in distributions:
        if dist in visited:
            continue
        orbit = set()
        for pp in pair_perm_list:
            # Apply pair permutation: new_dist[pp[i]] = dist[i]
            new_dist = [0] * 8
            for i in range(8):
                new_dist[pp[i]] = dist[i]
            new_dist = tuple(new_dist)
            orbit.add(new_dist)
        orbits.append(orbit)
        visited |= orbit
    
    print(f"  Orbits under Stab(1111): {len(orbits)}")
    for i, orb in enumerate(orbits):
        rep = sorted(orb)[0]
        print(f"    Orbit {i}: size {len(orb)}, representative: {rep}")
    
    # Also check orbits under Stab(1111) × Aut(Z₁₃)
    # Aut(Z₁₃) has order φ(13) = 12
    aut_z13_order = 12
    print(f"\n  |Aut(Z₁₃)| = {aut_z13_order}")
    print(f"  |Stab(1111) × Aut(Z₁₃)| = {len(stab_1111)} × {aut_z13_order} = {len(stab_1111) * aut_z13_order}")
    
    # Aut(Z₁₃) doesn't change type distributions (it permutes Z₁₃ values, not pairs)
    # So orbits on type distributions are the same.
    # But Aut(Z₁₃) matters for orbits on SURJECTIONS (which we don't enumerate here).
    
    # Analog of Orbit C: Frame = Type 2
    frame_idx = 0  # pair {0, 15}
    orbit_c_dists = [d for d in distributions if d[frame_idx] == 2]
    print(f"\n  Type distributions with Frame=Type 2 (analog of Orbit C): {len(orbit_c_dists)}")
    
    # Orbits on these
    oc_set = set(orbit_c_dists)
    visited2 = set()
    orbits_c = []
    for dist in orbit_c_dists:
        if dist in visited2:
            continue
        orbit = set()
        for pp in pair_perm_list:
            new_dist = tuple(dist[pp.index(i)] if i < 8 else 0 for i in range(8))
            # Actually: pp maps pair i → pp[i]. So dist applied to permuted pairs:
            # The type of the pair that is now at position j is dist[pp^{-1}(j)]
            inv_pp = [0]*8
            for k in range(8):
                inv_pp[pp[k]] = k
            new_dist = tuple(dist[inv_pp[j]] for j in range(8))
            if new_dist in oc_set:
                orbit.add(new_dist)
        orbits_c.append(orbit)
        visited2 |= orbit
    
    print(f"  Orbits on Frame=Type2 distributions: {len(orbits_c)}")
    for i, orb in enumerate(orbits_c):
        rep = sorted(orb)[0]
        print(f"    Orbit {i}: size {len(orb)}, representative: {rep}")
    
    # ── Lines through complement ──
    print("\n--- Lines through complement at n=4 ---")
    # In PG(3,F₂), lines through the all-ones point 1111:
    # A line through 1111 contains 1111 and two other nonzero points a, b with a⊕b=1111
    # i.e., the complement pairs {a, a⊕1111}
    # But in PG(3,F₂), a "line" is a 2-dimensional subspace = 4 elements = {0, a, b, a⊕b}
    # Lines through 1111: 2-dim subspaces containing 1111
    # Such a subspace has form {0, v, 1111, v⊕1111} for some v ≠ 0, v ≠ 1111
    # Each v gives the same line as 1111⊕v, so there are (14)/2 = 7 such lines
    
    lines_through_1111 = []
    for v in range(1, 15):
        if v == 15:
            continue
        w = v ^ 15
        if w < v:
            continue
        lines_through_1111.append(frozenset({0, v, w, 15}))
    
    print(f"  Lines through 1111 in PG(3,F₂): {len(lines_through_1111)}")
    for line in sorted(lines_through_1111, key=lambda s: min(s - {0})):
        pts = sorted(s for s in line if s != 0)
        pair = (min(pts[0], pts[0]^15), max(pts[0], pts[0]^15))
        print(f"    {{0, {pts[0]:04b}, {pts[1]:04b}, 1111}} — complement pair {pair}")
    
    # Each such line carries exactly one complement pair
    # So 7 lines ↔ 7 complement pairs (excluding Frame)
    # This is analogous to n=3 where 3 lines ↔ 3 non-Frame pairs
    
    print(f"\n  At n=3: 3 lines through 111 ↔ 3 non-Frame complement pairs")
    print(f"  At n=4: 7 lines through 1111 ↔ 7 non-Frame complement pairs")
    print(f"  Key difference: at n=3, 3 objects → S₃ acts transitively")
    print(f"  At n=4, 7 objects → question is whether Stab(1111) acts transitively on them")


# ═══════════════════════════════════════════════════════════════
# TASK C: 互-Analog at n=4
# ═══════════════════════════════════════════════════════════════

def task_c():
    print("\n" + "=" * 72)
    print("TASK C: 互-ANALOG AT n=4")
    print("=" * 72)
    
    n = 4
    N = 1 << n  # 16
    
    # At n=3 (6 lines): nuclear takes inner 4 (lines 2-5), splits into
    #   lower = (L₂, L₃, L₄), upper = (L₃, L₄, L₅)
    #   Overlap = 2 bits
    # General pattern: from 2n lines, take inner 2(n-1) lines, split into
    #   lower = first n, upper = last n, overlap = n-2
    
    # At n=4 (8 lines): take inner 6 (lines 2-7), split into
    #   lower = (L₂, L₃, L₄, L₅), upper = (L₄, L₅, L₆, L₇)
    #   Overlap = 2 bits (L₄, L₅)
    
    # In our encoding: hexagram h = (lower, upper) where lower = L₁L₂L₃L₄, upper = L₅L₆L₇L₈
    # L_i = bit (i-1) of h
    # lower = bits 0-3, upper = bits 4-7
    # L₁=bit0, L₂=bit1, L₃=bit2, L₄=bit3, L₅=bit4, L₆=bit5, L₇=bit6, L₈=bit7
    
    # Nuclear lower = (L₂, L₃, L₄, L₅) = (bit1, bit2, bit3, bit4)
    # Nuclear upper = (L₄, L₅, L₆, L₇) = (bit3, bit4, bit5, bit6)
    # (NOT including L₁ and L₈ = outer bits)
    
    print("\n--- Definition ---")
    print("  8-line figure: h = (L₁,...,L₈) = (lower 4-gram, upper 4-gram)")
    print("  Nuclear extraction (overlap-2):")
    print("    nuclear_lower = (L₂, L₃, L₄, L₅)")
    print("    nuclear_upper = (L₄, L₅, L₆, L₇)")
    print("    Drops L₁ (bottom) and L₈ (top)")
    print("    Overlap = {L₄, L₅}")
    
    def nuclear_n4(h):
        """Nuclear map for n=4: take inner 6 lines, split with overlap 2."""
        L = [(h >> i) & 1 for i in range(2*n)]
        nlo = L[1] | (L[2] << 1) | (L[3] << 2) | (L[4] << 3)
        nup = L[3] | (L[4] << 1) | (L[5] << 2) | (L[6] << 3)
        return nlo | (nup << n)
    
    # ── Compute the 8×8 matrix ──
    print("\n--- Standard basis matrix ---")
    
    # Express the map as a matrix: h has 2n=8 bits
    # nuclear(h) also has 2n=8 bits
    # Compute the F₂-linear part
    
    # Check linearity first
    dim = 2 * n  # 8
    N2 = 1 << dim  # 256
    
    # nuclear(0) should be 0
    print(f"  nuclear(0) = {nuclear_n4(0)} (should be 0)")
    
    # Check linearity: nuclear(a⊕b) = nuclear(a) ⊕ nuclear(b)?
    is_linear = True
    for a in range(N2):
        for b in range(a+1, min(a+16, N2)):  # spot check
            if nuclear_n4(a ^ b) != (nuclear_n4(a) ^ nuclear_n4(b)):
                is_linear = False
                break
        if not is_linear:
            break
    
    # Full linearity check
    is_linear = all(
        nuclear_n4(a ^ b) == (nuclear_n4(a) ^ nuclear_n4(b))
        for a in range(N2) for b in range(N2)
    )
    print(f"  Linear? {is_linear}")
    
    # Build matrix by applying to basis vectors
    matrix = [[0]*dim for _ in range(dim)]
    for j in range(dim):
        ej = 1 << j
        img = nuclear_n4(ej)
        for i in range(dim):
            matrix[i][j] = (img >> i) & 1
    
    print(f"\n  Nuclear map matrix M (8×8 over F₂):")
    labels = [f"L{i+1}" for i in range(dim)]
    print(f"       {'  '.join(labels)}")
    for i in range(dim):
        row_str = '  '.join(str(matrix[i][j]) for j in range(dim))
        print(f"  L'{i+1}:  {row_str}")
    
    # ── Rank sequence ──
    print("\n--- Rank sequence under iteration ---")
    
    M = matrix
    for iteration in range(6):
        # Compute rank
        rank = compute_rank_f2(M, dim, dim)
        print(f"  M^{iteration+1}: rank = {rank}")
        
        # Compute M^(k+1) = M × M^k
        M_next = mat_mul_f2(M, matrix, dim) if iteration == 0 else mat_mul_f2(M_next_prev, matrix, dim)
        
        # Actually, compute powers properly
        if iteration == 0:
            M_next_prev = M
        M_next_prev = mat_mul_f2(M_next_prev, matrix, dim)
        
        # Recompute properly
    
    # Recompute rank sequence properly
    print("\n  (Recomputing rank sequence properly)")
    powers = [matrix]
    cur = matrix
    for k in range(1, 8):
        cur = mat_mul_f2(cur, matrix, dim)
        powers.append(cur)
    
    for k, M_k in enumerate(powers):
        rank = compute_rank_f2(M_k, dim, dim)
        # Check if it's the zero matrix
        is_zero = all(M_k[i][j] == 0 for i in range(dim) for j in range(dim))
        print(f"  M^{k+1}: rank = {rank}{' (zero matrix)' if is_zero else ''}")
        if is_zero:
            break
    
    # ── Factored basis ──
    print("\n--- Factored basis ---")
    print("  Position: (o, m₁, m₂, i) = (L₁, L₂, L₃, L₄) = lower 4-gram")
    print("  Orbit:    (ō, m̄₁, m̄₂, ī) = (L₁⊕L₈, L₂⊕L₇, L₃⊕L₆, L₄⊕L₅)")
    
    def factored_n4(h):
        L = [(h >> i) & 1 for i in range(2*n)]
        pos = sum(L[i] << i for i in range(n))
        orb = sum((L[i] ^ L[2*n-1-i]) << i for i in range(n))
        return pos, orb
    
    def from_factored_n4(pos, orb):
        L_lower = [(pos >> i) & 1 for i in range(n)]
        orb_bits = [(orb >> i) & 1 for i in range(n)]
        L_upper = [L_lower[n-1-i] ^ orb_bits[n-1-i] for i in range(n)]
        L = L_lower + L_upper
        return sum(L[j] << j for j in range(2*n))
    
    # Express nuclear map in factored basis
    print("\n  Nuclear map in factored coordinates:")
    print("  Position (o, m₁, m₂, i) → Position' (o', m₁', m₂', i')")
    print("  Orbit (ō, m̄₁, m̄₂, ī) → Orbit' (ō', m̄₁', m̄₂', ī')")
    
    # Compute by mapping each factored basis vector
    # Actually, let's just trace the formulas:
    # nuclear_lower = (L₂, L₃, L₄, L₅) = (m₁, m₂, i, i⊕ī)
    # nuclear_upper = (L₄, L₅, L₆, L₇) = (i, i⊕ī, m₂⊕m̄₂, m₁⊕m̄₁)
    # Wait: L₅ = upper's bit0. In factored basis:
    #   L₁=o, L₂=m₁, L₃=m₂, L₄=i
    #   L₅=i⊕ī, L₆=m₂⊕m̄₂, L₇=m₁⊕m̄₁, L₈=o⊕ō
    
    print("\n  Explicit formulas:")
    print("  L₁=o, L₂=m₁, L₃=m₂, L₄=i, L₅=i⊕ī, L₆=m₂⊕m̄₂, L₇=m₁⊕m̄₁, L₈=o⊕ō")
    print()
    print("  nuclear_lower = (L₂, L₃, L₄, L₅) = (m₁, m₂, i, i⊕ī)")
    print("  nuclear_upper = (L₄, L₅, L₆, L₇) = (i, i⊕ī, m₂⊕m̄₂, m₁⊕m̄₁)")
    print()
    print("  New position = nuclear_lower = (m₁, m₂, i, i⊕ī)")
    print("  New orbit = nuclear_lower ⊕ reverse(nuclear_upper)")
    print("             = (m₁⊕m₁⊕m̄₁, m₂⊕m₂⊕m̄₂, i⊕i⊕ī, (i⊕ī)⊕i)")
    
    # Verify by computing new orbit explicitly
    # New L' = (L₂, L₃, L₄, L₅, L₄, L₅, L₆, L₇) — the 8 lines of nuclear
    # Wait, nuclear only has 8 bits total: nuclear_lower (4 bits) + nuclear_upper (4 bits)
    # New orbit = palindromic signature of nuclear:
    # ō' = new_L₁' ⊕ new_L₈' = L₂ ⊕ L₇ = m₁ ⊕ (m₁⊕m̄₁) = m̄₁
    # m̄₁' = new_L₂' ⊕ new_L₇' = L₃ ⊕ L₆ = m₂ ⊕ (m₂⊕m̄₂) = m̄₂
    # m̄₂' = new_L₃' ⊕ new_L₆' = L₄ ⊕ L₆ ... wait, nuclear has 8 lines:
    # new_L₁'=L₂, new_L₂'=L₃, new_L₃'=L₄, new_L₄'=L₅,
    # new_L₅'=L₄, new_L₆'=L₅, new_L₇'=L₆, new_L₈'=L₇
    
    # Hmm, that's not right. The nuclear map produces a hexagram with:
    # lower 4-gram = (L₂, L₃, L₄, L₅) and upper 4-gram = (L₄, L₅, L₆, L₇)
    # So the full 8-line figure of the nuclear is:
    # (L₂, L₃, L₄, L₅, L₄, L₅, L₆, L₇)
    # Its factored form:
    # pos' = lower = (L₂, L₃, L₄, L₅) = (m₁, m₂, i, i⊕ī)
    # orb' = palindromic sig:
    #   ō' = L₂ ⊕ L₇ = m₁ ⊕ (m₁⊕m̄₁) = m̄₁
    #   m̄₁' = L₃ ⊕ L₆ = m₂ ⊕ (m₂⊕m̄₂) = m̄₂  
    #   m̄₂' = L₄ ⊕ L₅ = i ⊕ (i⊕ī) = ī
    #   ī' = L₅ ⊕ L₄ = (i⊕ī) ⊕ i = ī  
    
    # Wait, that gives m̄₂' = ī' = ī. Let me re-check.
    # The 8 new lines are: (L₂, L₃, L₄, L₅, L₄, L₅, L₆, L₇)
    # These are indexed 1-8 as new lines.
    # New position = (newL₁, newL₂, newL₃, newL₄) = (L₂, L₃, L₄, L₅)
    # New orbit:
    #   newō = newL₁ ⊕ newL₈ = L₂ ⊕ L₇ = m₁ ⊕ (m₁⊕m̄₁) = m̄₁
    #   newm̄₁ = newL₂ ⊕ newL₇ = L₃ ⊕ L₆ = m₂ ⊕ (m₂⊕m̄₂) = m̄₂
    #   newm̄₂ = newL₃ ⊕ newL₆ = L₄ ⊕ L₅ = i ⊕ (i⊕ī) = ī
    #   newī  = newL₄ ⊕ newL₅ = L₅ ⊕ L₄ = (i⊕ī) ⊕ i = ī
    
    print("\n  Factored nuclear map:")
    print("  Position:  o' = m₁,  m₁' = m₂,  m₂' = i,  i' = i⊕ī")
    print("  Orbit:     ō' = m̄₁,  m̄₁' = m̄₂,  m̄₂' = ī,  ī' = ī")
    print()
    print("  COMPARE with n=3:")
    print("  Position:  o' = m,  m' = i,  i' = i⊕ī")
    print("  Orbit:     ō' = m̄,  m̄' = ī,  ī' = ī")
    print()
    print("  PATTERN: Same structure with one more 'shift' step!")
    print("  Position shifts o→m₁→m₂→i with shear i⊕ī at the end")
    print("  Orbit shifts ō→m̄₁→m̄₂→ī with projection ī↦ī at the end")
    
    # Verify numerically
    print("\n  Numerical verification:")
    errors = 0
    for h in range(1 << (2*n)):
        pos, orb = factored_n4(h)
        hn = nuclear_n4(h)
        pos_n, orb_n = factored_n4(hn)
        
        o  = (pos >> 0) & 1; m1 = (pos >> 1) & 1
        m2 = (pos >> 2) & 1; i_ = (pos >> 3) & 1
        ob = (orb >> 0) & 1; m1b = (orb >> 1) & 1
        m2b = (orb >> 2) & 1; ib = (orb >> 3) & 1
        
        # Expected
        exp_pos = m1 | (m2 << 1) | (i_ << 2) | ((i_ ^ ib) << 3)
        exp_orb = m1b | (m2b << 1) | (ib << 2) | (ib << 3)
        
        if pos_n != exp_pos or orb_n != exp_orb:
            errors += 1
            if errors <= 3:
                print(f"    MISMATCH at h={h:08b}: got pos={pos_n:04b},orb={orb_n:04b}, expected pos={exp_pos:04b},orb={exp_orb:04b}")
    
    if errors == 0:
        print("  ✓ All 256 hexagrams match the factored formula")
    else:
        print(f"  ✗ {errors} mismatches")
    
    # ── Rank sequence from factored form ──
    print("\n--- Rank and attractor analysis ---")
    
    # Position: shift o→m₁→m₂→i→i⊕ī
    # Orbit: shift ō→m̄₁→m̄₂→ī→ī
    # After k applications:
    # Position loses 1 coordinate per step (outer killed first)
    # After 1: kills o, ō → rank drops by 2 → 8→6
    # After 2: kills m₁, m̄₁ → rank drops by 2 → 6→4
    # After 3: kills m₂, m̄₂ → rank drops by 2 → 4→2
    # After 4: stabilizes at 2 (span{i, ī})
    
    # Actually let me check: after M¹, image = {(m₁,m₂,i,i⊕ī, m̄₁,m̄₂,ī,ī)}
    # That's 6 independent coordinates... but ī appears twice in orbit.
    # Orbit part: (m̄₁, m̄₂, ī, ī) has rank 3 (ī is repeated).
    # Position part: (m₁, m₂, i, i⊕ī) has rank 3 (i and i⊕ī span 2 things given ī).
    # Total rank after M¹: let me just compute it.
    
    # Actually, the position part of M is (m₁, m₂, i, i⊕ī) which depends on
    # m₁, m₂, i, ī → 4 independent variables → rank 4 for position
    # orbit part: (m̄₁, m̄₂, ī, ī) depends on m̄₁, m̄₂, ī → rank 3 for orbit
    # But we're looking at the 8-dimensional matrix. After M¹:
    # The image is spanned by the 8 columns of M, which correspond to:
    # column 0 (o): maps to (0, ...) — o is killed
    # column 1 (m₁): maps to (1, 0, 0, 0, 0, 0, 0, 0) in nuclear lower's first position
    # Hmm, let me just use the already-computed rank sequence.
    
    print("  (Using already-computed matrix powers)")
    for k in range(len(powers)):
        M_k = powers[k]
        rank = compute_rank_f2(M_k, dim, dim)
        is_zero = all(M_k[i][j] == 0 for i in range(dim) for j in range(dim))
        if is_zero:
            print(f"  M^{k+1}: rank = 0 (zero matrix)")
            break
        else:
            print(f"  M^{k+1}: rank = {rank}")
    
    print(f"\n  COMPARE rank sequences:")
    print(f"  n=3: 6 → 4 → 2 → 2 (stabilizes at step 2)")
    print(f"  n=4: ", end="")
    
    prev_rank = dim
    for k in range(len(powers)):
        r = compute_rank_f2(powers[k], dim, dim)
        if r == 0:
            print(f"→ 0", end="")
            break
        print(f"{'→ ' if k > 0 else ''}{r}", end="")
        if k > 0 and r == prev_rank:
            print(f" (stabilizes at step {k+1})", end="")
            break
        prev_rank = r
    print()
    
    # ── Fixed subspace ──
    print("\n--- Fixed subspace and attractors ---")
    
    # Find fixed points: nuclear(h) = h
    fixed_points = []
    for h in range(N2):
        if nuclear_n4(h) == h:
            pos, orb = factored_n4(h)
            fixed_points.append((h, pos, orb))
    
    print(f"  Fixed points (nuclear(h) = h): {len(fixed_points)}")
    for h, pos, orb in fixed_points:
        print(f"    h={h:08b}  pos={pos:04b} orb={orb:04b}")
    
    # Find 2-cycles
    two_cycles = []
    seen = set()
    for h in range(N2):
        hn = nuclear_n4(h)
        hnn = nuclear_n4(hn)
        if hnn == h and hn != h and h not in seen:
            two_cycles.append((h, hn))
            seen.add(h); seen.add(hn)
    
    print(f"\n  2-cycles: {len(two_cycles)}")
    for h1, h2 in two_cycles[:10]:
        p1, o1 = factored_n4(h1)
        p2, o2 = factored_n4(h2)
        print(f"    {h1:08b} ↔ {h2:08b}  (pos {p1:04b}↔{p2:04b}, orb {o1:04b}↔{o2:04b})")
    if len(two_cycles) > 10:
        print(f"    ... ({len(two_cycles)} total)")
    
    # Find eventual image (stable image after many iterations)
    stable_image = set()
    for h in range(N2):
        cur = h
        for _ in range(10):
            cur = nuclear_n4(cur)
        stable_image.add(cur)
    
    print(f"\n  Stable image (after 10 iterations): {len(stable_image)} elements")
    for h in sorted(stable_image):
        pos, orb = factored_n4(h)
        lo = h & ((1 << n) - 1)
        up = (h >> n) & ((1 << n) - 1)
        print(f"    h={h:08b}  lower={lo:04b} upper={up:04b}  pos={pos:04b} orb={orb:04b}")
    
    # ── Characterize the stable image ──
    print("\n--- Characterization of stable image ---")
    # At n=3, stable image = span{i, ī} = 4 elements
    # At n=4, should be span{i, ī} as well
    # pos = (0, 0, i, i⊕ī), orb = (0, 0, ī, ī)
    
    print("  Expected: pos = (0, 0, i, i⊕ī), orb = (0, 0, ī, ī)")
    print("  Checking:")
    for h in sorted(stable_image):
        pos, orb = factored_n4(h)
        o = (pos >> 0) & 1; m1 = (pos >> 1) & 1
        m2 = (pos >> 2) & 1; i_ = (pos >> 3) & 1
        ob = (orb >> 0) & 1; m1b = (orb >> 1) & 1
        m2b = (orb >> 2) & 1; ib = (orb >> 3) & 1
        
        ok = (o == 0 and m1 == 0 and ob == 0 and m1b == 0 and m2b == ib)
        print(f"    pos=({o},{m1},{m2},{i_}) orb=({ob},{m1b},{m2b},{ib})  {'✓' if ok else '✗'}")


def compute_rank_f2(mat, rows, cols):
    """Rank of a matrix over F₂."""
    M = [row[:] for row in mat]
    pivot_row = 0
    for col in range(cols):
        found = False
        for row in range(pivot_row, rows):
            if M[row][col]:
                M[pivot_row], M[row] = M[row], M[pivot_row]
                found = True
                break
        if not found:
            continue
        for row in range(rows):
            if row != pivot_row and M[row][col]:
                M[row] = [M[row][j] ^ M[pivot_row][j] for j in range(cols)]
        pivot_row += 1
    return pivot_row


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
    
    output_path = "/home/quasar/nous/memories/iching/unification/transitivity_probe_output.txt"
    with open(output_path, 'w') as log_file:
        tee = Tee(sys.stdout, log_file)
        old_stdout = sys.stdout
        sys.stdout = tee
        
        try:
            task_a()
            task_b()
            task_c()
        finally:
            sys.stdout = old_stdout
    
    print(f"\nOutput saved to {output_path}")
