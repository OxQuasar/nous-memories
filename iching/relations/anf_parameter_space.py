#!/usr/bin/env python3
"""
anf_parameter_space.py — Group action on ANF parameter space Z₅⁴

The complement constraint parametrizes surjections by (a₁, a₂, a₄, a₇) ∈ Z₅⁴.
This script computes:
1. The Stab(111) representation as 4×4 matrices over Z₅
2. Orbit decomposition in Z₅⁴ matching the 5 known orbits
3. Surjectivity locus description
"""

import sys, io
from collections import Counter, defaultdict
from itertools import product as iterproduct

P = 5
IC = [2, 0, 4, 3, 2, 1, 0, 3]

def fmt(x): return format(x, '03b')
def popcount(x): return bin(x).count('1')
def monomial_eval(S, x): return 1 if (x & S) == S else 0

# ═══════════════════════════════════════════════════════════
# ANF computation
# ═══════════════════════════════════════════════════════════

def compute_anf(f, p=P):
    coeffs = {}
    for S in range(8):
        val = 0
        for T in range(8):
            if (T & S) == T:
                sign = (-1) ** (popcount(S) - popcount(T))
                val = (val + sign * f[T]) % p
        coeffs[S] = val % p
    return coeffs

def anf_to_params(coeffs):
    return (coeffs[1], coeffs[2], coeffs[4], coeffs[7])

def params_to_f(a1, a2, a4, a7, p=P):
    a0 = (3 * (-(a1 + a2 + a4) - 2*a7)) % p
    a3 = a5 = a6 = (2 * a7) % p
    coeffs = {0:a0, 1:a1, 2:a2, 3:a3, 4:a4, 5:a5, 6:a6, 7:a7}
    return [sum(coeffs[S] * monomial_eval(S, x) for S in range(8)) % p for x in range(8)]

def is_surjective(f, p=P): return len(set(f)) == p

# ═══════════════════════════════════════════════════════════
# F₂ linear algebra
# ═══════════════════════════════════════════════════════════

def mat_vec_f2(A, v, n=3):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_det_f2(A):
    a,b,c = A[0]; d,e,f_ = A[1]; g,h,k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1

def mat_mul_f2(A, B, n=3):
    return [[ sum(A[i][k] & B[k][j] for k in range(n)) % 2 for j in range(n)] for i in range(n)]

def mat_inv_f2(A, n=3):
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

def mat_to_str(A, n=3):
    return '[' + ','.join(''.join(str(A[i][j]) for j in range(n)) for i in range(n)) + ']'

def compute_stab():
    stab = []
    for row0 in range(1, 8):
        for row1 in range(1, 8):
            for row2 in range(1, 8):
                A = [[(row0>>j)&1 for j in range(3)],
                     [(row1>>j)&1 for j in range(3)],
                     [(row2>>j)&1 for j in range(3)]]
                if mat_det_f2(A) and mat_vec_f2(A, 7) == 7:
                    stab.append(A)
    return stab

# ═══════════════════════════════════════════════════════════
# Z₅ linear algebra (4×4)
# ═══════════════════════════════════════════════════════════

def mat_mul_z5(A, B, n=4, p=P):
    return [[(sum(A[i][k]*B[k][j] for k in range(n))) % p for j in range(n)] for i in range(n)]

def mat_vec_z5(A, v, n=4, p=P):
    return tuple((sum(A[i][j]*v[j] for j in range(n))) % p for i in range(n))

def mat_eq_z5(A, B, n=4):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))

def mat_id_z5(n=4):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

# ═══════════════════════════════════════════════════════════
# Orbit via union-find on surjections (reference)
# ═══════════════════════════════════════════════════════════

def enumerate_surjections():
    pairs = [(0,7), (1,6), (2,5), (3,4)]
    surjections = []
    for assignment in iterproduct(range(P), repeat=len(pairs)):
        fmap = {}
        for i, (rep, partner) in enumerate(pairs):
            fmap[rep] = assignment[i]
            fmap[partner] = (-assignment[i]) % P
        if len(set(fmap.values())) == P:
            surjections.append(tuple(fmap[x] for x in range(8)))
    return surjections

def compute_reference_orbits():
    surjections = enumerate_surjections()
    stab = compute_stab()
    stab_invs = [mat_inv_f2(A) for A in stab]
    aut = list(range(1, P))
    parent = {s: s for s in surjections}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    surj_set = set(surjections)
    for s in surjections:
        for A_inv in stab_invs:
            for alpha in aut:
                t = tuple((alpha * s[mat_vec_f2(A_inv, x)]) % P for x in range(8))
                if t in surj_set: union(s, t)
    orbit_map = defaultdict(list)
    for s in surjections:
        orbit_map[find(s)].append(s)
    return sorted(orbit_map.values(), key=lambda o: (-len(o), sorted(o)[0]))


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    old_stdout = sys.stdout
    captured = io.StringIO()
    class Tee:
        def __init__(self, *f): self.files = f
        def write(self, d):
            for f in self.files: f.write(d)
        def flush(self):
            for f in self.files: f.flush()
    sys.stdout = Tee(old_stdout, captured)
    try: run()
    finally: sys.stdout = old_stdout
    path = "/home/quasar/nous/memories/iching/relations/anf_parameter_space_output.md"
    with open(path, 'w') as out: out.write(captured.getvalue())
    print(f"\nResults written to {path}")

def run():
    stab = compute_stab()
    stab_invs = [mat_inv_f2(A) for A in stab]

    print("=" * 72)
    print("  GROUP ACTION ON ANF PARAMETER SPACE Z₅⁴")
    print("=" * 72)
    print()
    print(f"  |Stab(111)| = {len(stab)}")
    print()

    # ─── Part A: Full 4×4 representation ───
    print("  " + "=" * 68)
    print("  PART A: FULL 4×4 REPRESENTATION ON (a₁, a₂, a₄, a₇)")
    print("  " + "=" * 68)
    print()
    print("  The standard action: (A,α)·f = x ↦ α·f(A⁻¹x).")
    print("  For α=1, this means g(x) = f(A⁻¹x), so g = f∘A⁻¹.")
    print("  We compute the 4×4 matrix R_A such that")
    print("  params(f∘A⁻¹) = R_A · params(f).")
    print()

    # For each A, compute R_A via 4 probes
    rep_4x4 = []  # R_A for action g = f ∘ A⁻¹
    for A in stab:
        A_inv = mat_inv_f2(A)
        cols = []
        for probe_idx, probe in enumerate([(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]):
            f_probe = params_to_f(*probe)
            g = [f_probe[mat_vec_f2(A_inv, x)] for x in range(8)]
            c_g = compute_anf(g)
            col = (c_g[1], c_g[2], c_g[4], c_g[7])
            cols.append(col)
        # R_A[i][j] = column j, row i
        R = [[cols[j][i] for j in range(4)] for i in range(4)]
        rep_4x4.append(R)

    # Verify: R is a group homomorphism (R_{AB} = R_A · R_B)
    homo_ok = True
    for i in range(len(stab)):
        for j in range(len(stab)):
            AB = mat_mul_f2(stab[i], stab[j])
            ab_idx = None
            for k, C in enumerate(stab):
                if all(AB[r][c] == C[r][c] for r in range(3) for c in range(3)):
                    ab_idx = k; break
            R_AB = rep_4x4[ab_idx]
            R_A_R_B = mat_mul_z5(rep_4x4[i], rep_4x4[j])
            if not mat_eq_z5(R_AB, R_A_R_B):
                homo_ok = False; break
        if not homo_ok: break

    print(f"  Homomorphism R_{{AB}} = R_A · R_B: {'✓' if homo_ok else '✗'}")

    # Kernel
    identity_4 = mat_id_z5(4)
    kernel = [i for i, R in enumerate(rep_4x4) if mat_eq_z5(R, identity_4)]
    print(f"  Kernel: {len(kernel)} elements")

    # Distinct matrices
    distinct = {}
    for i, R in enumerate(rep_4x4):
        key = tuple(tuple(row) for row in R)
        if key not in distinct: distinct[key] = []
        distinct[key].append(i)
    print(f"  Distinct R_A: {len(distinct)} (|Stab|/|ker| = {len(stab)//max(len(kernel),1)})")
    print()

    # Show the block structure
    print("  Block structure analysis:")
    # Check if the (a₁,a₂,a₄) block is independent of a₇
    upper_left_independent = True
    a7_row = set()
    for R in rep_4x4:
        # Top-left 3×3 block
        block = tuple(tuple(R[i][j] for j in range(3)) for i in range(3))
        # Bottom-left 1×3 (a₇ depends on a₁,a₂,a₄?)
        bottom = tuple(R[3][j] for j in range(3))
        # Right column (a₁,a₂,a₄ depend on a₇?)
        right = tuple(R[i][3] for i in range(3))
        a7_row.add(bottom)
        if any(R[i][3] != 0 for i in range(3)):
            upper_left_independent = False

    a7_diag = set(R[3][3] for R in rep_4x4)

    print(f"  (a₁,a₂,a₄) independent of a₇ column: {'✓' if upper_left_independent else '✗'}")
    print(f"  a₇ depends on (a₁,a₂,a₄): {'yes' if any(r != (0,0,0) for r in a7_row) else 'no'}")
    print(f"  a₇→a₇ diagonal values: {sorted(a7_diag)}")
    print()

    # Print some representative matrices
    print("  Sample R_A matrices:")
    shown = 0
    for key, indices in sorted(distinct.items(), key=lambda x: x[0]):
        if shown >= 6: break
        R = [list(row) for row in key]
        A = stab[indices[0]]
        is_id = mat_eq_z5(R, identity_4)
        print(f"    A = {mat_to_str(A)}:")
        for row in R:
            print(f"      {row}")
        if is_id: print(f"      ← identity")
        print()
        shown += 1
    if len(distinct) > 6:
        print(f"    ... ({len(distinct) - 6} more)")
    print()

    # Check: is a₇ row = (0,0,0,1) always? (meaning a₇ is invariant)
    a7_invariant = all(rep_4x4[i][3] == [0, 0, 0, 1] for i in range(len(stab)))
    print(f"  a₇ invariant under Stab(111): {'✓' if a7_invariant else '✗'}")
    if not a7_invariant:
        # Show which A change a₇
        changers = [(i, stab[i], rep_4x4[i][3]) for i in range(len(stab)) if rep_4x4[i][3] != [0, 0, 0, 1]]
        print(f"  {len(changers)} elements change a₇:")
        for i, A, row4 in changers[:4]:
            print(f"    A = {mat_to_str(A)}: a₇ row = {row4}")
        if len(changers) > 4:
            print(f"    ... ({len(changers) - 4} more)")
    print()

    # Check: what is the 3×3 upper-left block?
    print("  Upper-left 3×3 block (action on (a₁,a₂,a₄)):")
    if upper_left_independent:
        # Compare to A, Aᵀ, A⁻¹, (A⁻¹)ᵀ
        natural = transpose = inverse = contragredient = 0
        for i, A in enumerate(stab):
            M3 = [rep_4x4[i][r][:3] for r in range(3)]
            A_z5 = [row[:] for row in A]
            A_T = [[A[j][ii] for j in range(3)] for ii in range(3)]
            A_inv_z5 = [row[:] for row in mat_inv_f2(A)]
            A_inv_T = [[A_inv_z5[j][ii] for j in range(3)] for ii in range(3)]
            if all(M3[r][c] == A_z5[r][c] for r in range(3) for c in range(3)): natural += 1
            if all(M3[r][c] == A_T[r][c] for r in range(3) for c in range(3)): transpose += 1
            if all(M3[r][c] == A_inv_z5[r][c] for r in range(3) for c in range(3)): inverse += 1
            if all(M3[r][c] == A_inv_T[r][c] for r in range(3) for c in range(3)): contragredient += 1

        print(f"    = A (natural): {natural}/24")
        print(f"    = Aᵀ: {transpose}/24")
        print(f"    = A⁻¹: {inverse}/24")
        print(f"    = (A⁻¹)ᵀ: {contragredient}/24")
    print()

    # ─── Part B: Aut(Z₅) action ───
    print("  " + "=" * 68)
    print("  PART B: AUT(Z₅) ACTION")
    print("  " + "=" * 68)
    print()
    print("  τ_k: f ↦ kf acts as scalar multiplication on ALL params.")
    print("  (a₁,a₂,a₄,a₇) → (ka₁,ka₂,ka₄,ka₇)")
    print()

    # ─── Part C: Orbit decomposition in full Z₅⁴ ───
    print("  " + "=" * 68)
    print("  PART C: ORBIT DECOMPOSITION IN Z₅⁴")
    print("  " + "=" * 68)
    print()

    # Map all 240 surjections to parameter space
    surjections = enumerate_surjections()
    surj_to_param = {}
    param_to_surj = {}
    for s in surjections:
        c = compute_anf(list(s))
        p = anf_to_params(c)
        surj_to_param[s] = p
        param_to_surj[p] = s

    param_pts = set(surj_to_param.values())
    print(f"  Total surjective param points: {len(param_pts)}")
    print()

    # Full G = Stab(111) × Aut(Z₅) acts on params as:
    # (A, α) · (a₁,a₂,a₄,a₇) = α · R_A · (a₁,a₂,a₄,a₇)
    parent_p = {p: p for p in param_pts}
    def find_p(x):
        while parent_p[x] != x: parent_p[x] = parent_p[parent_p[x]]; x = parent_p[x]
        return x
    def union_p(a, b):
        ra, rb = find_p(a), find_p(b)
        if ra != rb: parent_p[ra] = rb

    for p in param_pts:
        # Stab(111) action
        for R in rep_4x4:
            q = mat_vec_z5(R, p)
            if q in param_pts:
                union_p(p, q)
        # Aut(Z₅) action
        for k in range(1, P):
            q = tuple((k * v) % P for v in p)
            if q in param_pts:
                union_p(p, q)

    orbit_map_p = defaultdict(list)
    for p in param_pts:
        orbit_map_p[find_p(p)].append(p)
    orbits_p = sorted(orbit_map_p.values(), key=lambda o: (-len(o), sorted(o)[0]))

    print(f"  Orbits in Z₅⁴: {len(orbits_p)}, sizes {[len(o) for o in orbits_p]}")

    # Match to reference orbits
    ref_orbits = compute_reference_orbits()
    ic_tuple = tuple(IC)

    print()
    for idx, orb_p in enumerate(orbits_p):
        # Pick a representative, reconstruct surjection
        rep = sorted(orb_p)[0]
        s_rep = param_to_surj[rep]
        shape = tuple(sorted(Counter(s_rep).values(), reverse=True))

        # Find which reference orbit
        ref_idx = None
        for ri, ro in enumerate(ref_orbits):
            if s_rep in ro:
                ref_idx = ri; break

        has_ic = any(param_to_surj.get(p) == ic_tuple for p in orb_p if p in param_to_surj)

        # a₇ distribution
        a7_dist = Counter(p[3] for p in orb_p)

        marker = " ★ IC" if has_ic else ""
        print(f"  Orbit {idx} (size {len(orb_p)}, ref orbit #{ref_idx}, shape {list(shape)}){marker}:")
        print(f"    a₇ distribution: {dict(sorted(a7_dist.items()))}")
        print(f"    Rep: params={rep}, f={list(s_rep)}")
    print()

    # ─── Part D: a₇ strata ───
    print("  " + "=" * 68)
    print("  PART D: STRATA BY a₇")
    print("  " + "=" * 68)
    print()

    for a7_val in range(P):
        pts_at = [p for p in param_pts if p[3] == a7_val]
        # Which full orbits are represented?
        orbit_counts = Counter()
        for p in pts_at:
            s = param_to_surj[p]
            for ri, ro in enumerate(ref_orbits):
                if s in ro:
                    orbit_counts[ri] += 1
                    break
        print(f"  a₇={a7_val}: {len(pts_at)} points, orbit breakdown: {dict(sorted(orbit_counts.items()))}")

    print()

    # ─── Task 16: Surjectivity locus ───
    print("  " + "=" * 68)
    print("  TASK 16: SURJECTIVITY LOCUS")
    print("  " + "=" * 68)
    print()

    # f(x) as linear function of (a₁,a₂,a₄,a₇)
    # Compute via probes at the 4 basis directions
    print("  f(x) as affine function of (a₁,a₂,a₄,a₇):")
    print()

    # f(x) at params=0: the constant term
    f_zero = params_to_f(0, 0, 0, 0)  # all zeros
    # f at each basis: column of the linear map
    probes_f = []
    for b in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]:
        fb = params_to_f(*b)
        probes_f.append([(fb[x] - f_zero[x]) % P for x in range(8)])

    for x in range(8):
        const = f_zero[x]
        c1 = probes_f[0][x]
        c2 = probes_f[1][x]
        c4 = probes_f[2][x]
        c7 = probes_f[3][x]

        # Verify with a test point
        test_f = params_to_f(2, 3, 1, 4)
        expected = (const + 2*c1 + 3*c2 + 1*c4 + 4*c7) % P
        ok = expected == test_f[x]

        terms = []
        if const: terms.append(str(const))
        for coeff, name in [(c1,'a₁'),(c2,'a₂'),(c4,'a₄'),(c7,'a₇')]:
            if coeff == 0: continue
            if coeff == 1: terms.append(name)
            elif coeff == P-1: terms.append(f"4{name}")
            else: terms.append(f"{coeff}{name}")

        expr = ' + '.join(terms) if terms else '0'
        comp = fmt(7-x)
        print(f"    f({fmt(x)}) = {expr:>30} {'✓' if ok else '✗'}   [~{comp}: f(~{fmt(x)}) = {(-test_f[x])%P if ok else '?'}]")

    print()

    # Surjectivity = all 5 values hit = no value missed
    # For f to miss value k: none of the 8 equations f(x) = k (x ∈ F₂³) has a solution
    # Since x is Boolean (0/1), each f(x) = k is a constraint on (a₁,a₂,a₄,a₇)
    # f misses k iff (a₁,a₂,a₄,a₇) avoids {p : ∃x, f(x)=k at p}

    # Count "misses k" for each k
    print("  'Misses k' locus in Z₅⁴:")
    total_pts = list(iterproduct(range(P), repeat=4))
    for k in range(P):
        miss_count = 0
        for pt in total_pts:
            f = params_to_f(*pt)
            if k not in f:
                miss_count += 1
        # Also count how many of the 625 total complement-respecting functions miss k
        print(f"    Misses {k}: {miss_count}/625 params")
    print()

    # Complement symmetry
    print("  Complement symmetry of miss loci:")
    for k in range(P):
        neg_k = (-k) % P
        if neg_k <= k: continue
        miss_k = set(pt for pt in total_pts if k not in params_to_f(*pt))
        miss_nk = set(pt for pt in total_pts if neg_k not in params_to_f(*pt))
        print(f"    miss({k}) = miss({neg_k}): {'✓ identical' if miss_k == miss_nk else f'{len(miss_k.symmetric_difference(miss_nk))} differences'}")
    print()

    # Surjective count
    surj_count = sum(1 for pt in total_pts if is_surjective(params_to_f(*pt)))
    print(f"  Surjective: {surj_count}/625 (should = 240)")

    # Non-surjective structure
    nonsurj_pts = [pt for pt in total_pts if not is_surjective(params_to_f(*pt))]
    range_sizes = Counter(len(set(params_to_f(*pt))) for pt in nonsurj_pts)
    print(f"  Non-surjective range sizes: {dict(sorted(range_sizes.items()))}")
    print()

    # ─── Adjacency / geometry of surjective locus ───
    surj_set_4d = set(surj_to_param.values())

    # Stab(111)-orbits on Z₅⁴ surjective locus (without Aut scaling)
    parent_s = {p: p for p in surj_set_4d}
    def find_s(x):
        while parent_s[x] != x: parent_s[x] = parent_s[parent_s[x]]; x = parent_s[x]
        return x
    def union_s(a, b):
        ra, rb = find_s(a), find_s(b)
        if ra != rb: parent_s[ra] = rb

    for p in surj_set_4d:
        for R in rep_4x4:
            q = mat_vec_z5(R, p)
            if q in surj_set_4d:
                union_s(p, q)

    orb_s = defaultdict(list)
    for p in surj_set_4d:
        orb_s[find_s(p)].append(p)
    orbs_stab_only = sorted(orb_s.values(), key=lambda o: (-len(o), sorted(o)[0]))

    print(f"  Stab(111)-orbits (no Aut): {len(orbs_stab_only)}, sizes {sorted([len(o) for o in orbs_stab_only], reverse=True)}")

    for idx, orb in enumerate(orbs_stab_only):
        rep = sorted(orb)[0]
        s_rep = param_to_surj[rep]
        shape = tuple(sorted(Counter(s_rep).values(), reverse=True))
        a7_dist = Counter(p[3] for p in orb)
        has_ic = ic_tuple in [param_to_surj.get(p) for p in orb]
        marker = " ★" if has_ic else ""
        print(f"    Orbit {idx} (size {len(orb)}, shape {list(shape)}){marker}: a₇ dist = {dict(sorted(a7_dist.items()))}")


if __name__ == "__main__":
    main()
