#!/usr/bin/env python3
"""
eigenstructure.py — Two analyses:

Task 2: Eigenstructure of the 互 transition matrix on Z₅
Task 3: Exact P-coset alignment formula derivation
"""

from collections import Counter, defaultdict
from fractions import Fraction
import math

# ═══════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════

WUXING = {0:2, 1:0, 2:4, 3:3, 4:2, 5:1, 6:0, 7:3}
ELEM = {0:'Wood', 1:'Fire', 2:'Earth', 3:'Metal', 4:'Water'}
REL = {0:'同', 1:'生', 2:'克', 3:'被克', 4:'被生'}
TRIG = {0:'坤',1:'震',2:'坎',3:'兌',4:'艮',5:'離',6:'巽',7:'乾'}

def f(x): return WUXING[x]
def nuclear(h):
    L = [(h >> i) & 1 for i in range(6)]
    nlo = L[1] | (L[2] << 1) | (L[3] << 2)
    nup = L[2] | (L[3] << 1) | (L[4] << 2)
    return nlo | (nup << 3)

def hex_d(h): return (f((h>>3)&7) - f(h&7)) % 5
def P_parity(x): return ((x>>0)&1) ^ ((x>>1)&1)


# ═══════════════════════════════════════════════════════════
# Task 2: Eigenstructure of the transition matrix
# ═══════════════════════════════════════════════════════════

def build_transition_matrix():
    """Build the 5×5 transition matrix T where T[d][d'] = count(d→d')/total(d)."""
    counts = [[0]*5 for _ in range(5)]
    row_totals = [0]*5
    for h in range(64):
        d = hex_d(h)
        dn = hex_d(nuclear(h))
        counts[d][dn] += 1
        row_totals[d] += 1
    
    # Exact rational transition probabilities
    T = [[Fraction(0)]*5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            T[i][j] = Fraction(counts[i][j], row_totals[i])
    return T, counts, row_totals


def mat_mul(A, B, n=5):
    """Multiply two n×n Fraction matrices."""
    C = [[Fraction(0)]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


def mat_pow(A, p, n=5):
    """Matrix power A^p."""
    if p == 0:
        return [[Fraction(1) if i==j else Fraction(0) for j in range(n)] for i in range(n)]
    if p == 1:
        return [row[:] for row in A]
    if p % 2 == 0:
        half = mat_pow(A, p//2, n)
        return mat_mul(half, half, n)
    else:
        return mat_mul(A, mat_pow(A, p-1, n), n)


def mat_vec(A, v, n=5):
    """Matrix-vector product."""
    return [sum(A[i][j]*v[j] for j in range(n)) for i in range(n)]


def vec_mat(v, A, n=5):
    """Row-vector times matrix."""
    return [sum(v[i]*A[i][j] for i in range(n)) for j in range(n)]


def find_stationary(T, n=5):
    """Find stationary distribution by power iteration with exact arithmetic."""
    # Start with uniform
    pi = [Fraction(1, n)] * n
    for _ in range(100):
        pi_new = vec_mat(pi, T, n)
        if pi_new == pi:
            break
        pi = pi_new
    return pi


def characteristic_poly_5x5(T):
    """Compute characteristic polynomial of 5×5 rational matrix via direct expansion.
    Returns coefficients [c0, c1, c2, c3, c4, c5] where p(λ) = c0 + c1*λ + ... + c5*λ^5.
    """
    # Use the Faddeev-LeVerrier algorithm
    n = 5
    # c_n = 1 (monic)
    # M_k = T^k + c_{n-1} T^{k-1} + ... + c_{n-k+1} I  (accumulated matrix)
    # c_{n-k} = -tr(T * M_{k-1}) / k
    
    coeffs = [Fraction(0)] * (n + 1)
    coeffs[n] = Fraction(1)
    
    I = [[Fraction(1) if i==j else Fraction(0) for j in range(n)] for i in range(n)]
    M = [row[:] for row in I]  # M_0 = I
    
    for k in range(1, n + 1):
        TM = mat_mul(T, M, n)
        tr = sum(TM[i][i] for i in range(n))
        c = -tr / k
        coeffs[n - k] = c
        # M_k = TM + c * I
        M = [[TM[i][j] + (c if i==j else Fraction(0)) for j in range(n)] for i in range(n)]
    
    return coeffs


def analyze_eigenstructure(out):
    out.append("## Task 2: 互 Transition Matrix Eigenstructure")
    out.append("")
    
    T, counts, row_totals = build_transition_matrix()
    
    # Display exact rational matrix
    out.append("### Exact rational transition matrix T")
    out.append("")
    out.append("T[d][d'] = P(d(互(h)) = d' | d(h) = d)")
    out.append("")
    header = "| d\\d' |"
    for d2 in range(5):
        header += f" {d2}({REL[d2]}) |"
    out.append(header)
    out.append("|" + "---|" * 6)
    for d1 in range(5):
        row = f"| **{d1}({REL[d1]})** |"
        for d2 in range(5):
            row += f" {T[d1][d2]} |"
        out.append(row)
    out.append("")
    
    out.append(f"Row totals (sanity): {[sum(T[i][j] for j in range(5)) for i in range(5)]}")
    out.append("")
    
    # Check negation symmetry
    neg_sym = all(T[d1][d2] == T[(-d1)%5][(-d2)%5] for d1 in range(5) for d2 in range(5))
    out.append(f"**Negation symmetry** T[d][d'] = T[−d][−d']: {'✓' if neg_sym else '✗'}")
    out.append("")
    
    # Check circulant
    is_circulant = all(T[d1][d2] == T[(d1+1)%5][(d2+1)%5] for d1 in range(5) for d2 in range(5))
    out.append(f"**Circulant?** T[d][d'] = T[d+1][d'+1]: {'✓' if is_circulant else '✗'}")
    out.append("")
    
    # Characteristic polynomial
    out.append("### Characteristic polynomial")
    out.append("")
    coeffs = characteristic_poly_5x5(T)
    terms = []
    for i, c in enumerate(coeffs):
        if c != 0:
            if i == 0:
                terms.append(f"({c})")
            elif i == 1:
                terms.append(f"({c})λ")
            else:
                terms.append(f"({c})λ^{i}")
    out.append(f"p(λ) = {' + '.join(terms)}")
    out.append("")
    
    # Verify p(T) = 0 (Cayley-Hamilton)
    # p(T) = c0*I + c1*T + c2*T^2 + c3*T^3 + c4*T^4 + c5*T^5
    T_powers = [mat_pow(T, k) for k in range(6)]
    pT = [[sum(coeffs[k] * T_powers[k][i][j] for k in range(6)) for j in range(5)] for i in range(5)]
    is_zero = all(pT[i][j] == 0 for i in range(5) for j in range(5))
    out.append(f"**Cayley-Hamilton check** p(T) = 0: {'✓' if is_zero else '✗'}")
    out.append("")
    
    # Factor the characteristic polynomial
    # Check eigenvalue λ = 1 (always exists for stochastic matrix)
    p_at_1 = sum(coeffs)
    out.append(f"p(1) = {p_at_1} → λ=1 is {'an eigenvalue' if p_at_1 == 0 else 'NOT an eigenvalue'}")
    out.append("")
    
    # By negation symmetry, if λ is eigenvalue then it appears with the same
    # multiplicity for the "negation-conjugate" eigenvector. Let's check specific values.
    out.append("### Eigenvalue search")
    out.append("")
    
    # Test rational eigenvalues with small denominators
    candidates = set()
    # Rational root theorem: eigenvalues = factors of c0 / factors of c5
    # c5 = 1, so rational eigenvalues divide c0
    c0 = coeffs[0]
    if c0 != 0:
        num = abs(c0.numerator)
        den = abs(c0.denominator)
        # Test ±(factors of num)/(factors of den)
        num_factors = set()
        for i in range(1, num + 1):
            if num % i == 0:
                num_factors.add(i)
        den_factors = set()
        for i in range(1, den + 1):
            if den % i == 0:
                den_factors.add(i)
        for n in num_factors:
            for d in den_factors:
                candidates.add(Fraction(n, d))
                candidates.add(Fraction(-n, d))
    candidates.add(Fraction(0))
    candidates.add(Fraction(1))
    
    eigenvalues = []
    for cand in sorted(candidates, key=lambda x: (abs(x), x)):
        val = sum(coeffs[k] * cand**k for k in range(6))
        if val == 0:
            eigenvalues.append(cand)
            out.append(f"  λ = {cand} ({float(cand):.6f}): p(λ) = 0 ✓ EIGENVALUE")
    
    non_rational_eigenvalues = []
    if len(eigenvalues) < 5:
        out.append(f"  Found {len(eigenvalues)} rational eigenvalues; {5-len(eigenvalues)} are irrational/complex")
        
        # Factor out the known roots to get reduced polynomial
        # If we have roots r1, r2, ..., then p(λ) = (λ-r1)(λ-r2)...q(λ)
        # Do polynomial long division
        remaining = list(reversed(coeffs))  # highest degree first
        for root in eigenvalues:
            new_poly = [Fraction(0)] * (len(remaining) - 1)
            new_poly[0] = remaining[0]
            for i in range(1, len(remaining) - 1):
                new_poly[i] = remaining[i] + root * new_poly[i-1]
            remaining = new_poly
        
        # remaining is the reduced polynomial (highest degree first)
        deg = len(remaining) - 1
        out.append(f"  Reduced polynomial (degree {deg}): ", )
        terms_r = []
        for i, c in enumerate(remaining):
            power = deg - i
            if c != 0:
                if power == 0:
                    terms_r.append(f"({c})")
                elif power == 1:
                    terms_r.append(f"({c})λ")
                else:
                    terms_r.append(f"({c})λ^{power}")
        out.append(f"  q(λ) = {' + '.join(terms_r)}")
        
        if deg == 2:
            # Quadratic formula: aλ² + bλ + c = 0
            a, b, c = remaining[0], remaining[1], remaining[2]
            disc = b*b - 4*a*c
            out.append(f"  Discriminant = {disc} = {float(disc):.6f}")
            if disc >= 0:
                # Real roots
                disc_float = float(disc)
                sqrt_disc = disc_float ** 0.5
                r1 = (-float(b) + sqrt_disc) / (2 * float(a))
                r2 = (-float(b) - sqrt_disc) / (2 * float(a))
                out.append(f"  Irrational roots: λ₃ ≈ {r1:.6f}, λ₄ ≈ {r2:.6f}")
                non_rational_eigenvalues = [r1, r2]
                
                # Check if discriminant is a perfect square (rational roots missed)
                num_d = disc.numerator
                den_d = disc.denominator
                sqrt_num = int(round(abs(num_d)**0.5))
                sqrt_den = int(round(abs(den_d)**0.5))
                if sqrt_num * sqrt_num == abs(num_d) and sqrt_den * sqrt_den == abs(den_d):
                    out.append(f"  (Actually rational: √disc = {sqrt_num}/{sqrt_den})")
                else:
                    out.append(f"  Exact form: λ = ({-b} ± √{disc}) / {2*a}")
            else:
                out.append(f"  Complex roots (disc < 0)")
                r_real = -float(b) / (2 * float(a))
                r_imag = (-float(disc))**0.5 / (2 * float(a))
                out.append(f"  λ₃,₄ = {r_real:.6f} ± {r_imag:.6f}i")
                out.append(f"  |λ₃| = |λ₄| = {(r_real**2 + r_imag**2)**0.5:.6f}")
                non_rational_eigenvalues = [complex(r_real, r_imag), complex(r_real, -r_imag)]
        
        elif deg == 3:
            # Cubic — use numerical approach
            a, b, c, d = [float(x) for x in remaining]
            # Find roots numerically via companion matrix or numpy-free method
            # Use Newton's method from different starting points
            import cmath
            roots_found = []
            for start in [-2, -1, -0.5, 0, 0.5, 1, 2, 1j, -1j]:
                z = complex(start)
                for _ in range(1000):
                    pval = a*z**3 + b*z**2 + c*z + d
                    dpval = 3*a*z**2 + 2*b*z + c
                    if abs(dpval) < 1e-30:
                        break
                    z -= pval / dpval
                if abs(a*z**3 + b*z**2 + c*z + d) < 1e-10:
                    # Check if it's a new root
                    is_new = True
                    for r in roots_found:
                        if abs(z - r) < 1e-6:
                            is_new = False
                            break
                    if is_new:
                        roots_found.append(z)
            
            for r in sorted(roots_found, key=lambda x: (-abs(x.real), abs(x.imag))):
                if abs(r.imag) < 1e-10:
                    out.append(f"  Root: λ ≈ {r.real:.6f}")
                    non_rational_eigenvalues.append(r.real)
                else:
                    out.append(f"  Root: λ ≈ {r.real:.6f} ± {abs(r.imag):.6f}i, |λ| ≈ {abs(r):.6f}")
                    non_rational_eigenvalues.append(r)
    
    out.append("")
    
    # Stationary distribution
    out.append("### Stationary distribution")
    out.append("")
    
    pi = find_stationary(T)
    out.append(f"π = {[str(x) for x in pi]}")
    out.append(f"π ≈ {[float(x) for x in pi]}")
    out.append("")
    
    # Verify: π·T = π
    pi_T = vec_mat(pi, T)
    is_stationary = pi_T == pi
    out.append(f"Verification πT = π: {'✓' if is_stationary else '✗'}")
    out.append("")
    
    # Compare to attractor distribution
    # Attractors: 坤坤(d=0), 乾乾(d=0), 既濟(d=2), 未濟(d=3)
    # Attractor d values: 0, 0, 2, 3
    attr_dist = [Fraction(2,4), Fraction(0), Fraction(1,4), Fraction(1,4), Fraction(0)]
    out.append(f"Attractor distribution: {[str(x) for x in attr_dist]}")
    out.append(f"  (d=0: 2 fixed points, d=2: 既濟, d=3: 未濟)")
    out.append(f"  Match stationary? {pi == attr_dist}")
    out.append("")
    
    if pi != attr_dist:
        out.append("**The stationary distribution does NOT equal the attractor distribution.**")
        out.append("This is expected: T is the transition matrix on the FULL 64-hexagram space,")
        out.append("not the restricted attractor space. The attractor distribution reflects")
        out.append("equal probability among the 4 attractors, not the mixing proportions of T.")
        out.append("")
    
    # Convergence rate
    out.append("### Convergence analysis")
    out.append("")
    
    all_eigs = [float(e) for e in eigenvalues]
    for e in non_rational_eigenvalues:
        if isinstance(e, complex):
            all_eigs.append(abs(e))
        else:
            all_eigs.append(abs(e))
    
    non_one = [abs(e) for e in all_eigs if abs(abs(e) - 1.0) > 1e-6]
    if non_one:
        second_largest = max(non_one)
        out.append(f"Second-largest eigenvalue magnitude: {second_largest:.6f}")
        out.append(f"Convergence rate: geometric with ratio ≈ {second_largest:.4f}")
        out.append(f"Mixing time (to ε): ≈ log(1/ε) / log(1/{second_largest:.4f}) = {1/math.log(1/second_largest) if second_largest < 1 else 'N/A (≥1)':.2f} × log(1/ε)")
    out.append("")
    
    # Power iteration: show T^k convergence
    out.append("### T^k convergence")
    out.append("")
    for k in [1, 2, 3, 5, 10]:
        Tk = mat_pow(T, k)
        out.append(f"**T^{k}:**")
        for i in range(5):
            row = [f"{float(Tk[i][j]):.4f}" for j in range(5)]
            out.append(f"  d={i}: [{', '.join(row)}]")
        out.append("")
    
    # Check if T preserves {生,被生} subspace
    out.append("### Invariant subspaces")
    out.append("")
    
    # Check: does the {d=1, d=4} subspace map to itself?
    # T restricted to rows {1,4}, columns {1,4}
    sub_14 = [[T[1][1], T[1][4]], [T[4][1], T[4][4]]]
    out.append(f"Restriction to {{生,被生}} (rows/cols 1,4):")
    out.append(f"  [{float(sub_14[0][0]):.4f}, {float(sub_14[0][1]):.4f}]")
    out.append(f"  [{float(sub_14[1][0]):.4f}, {float(sub_14[1][1]):.4f}]")
    out.append(f"  Row sums: {float(sub_14[0][0]+sub_14[0][1]):.4f}, {float(sub_14[1][0]+sub_14[1][1]):.4f}")
    
    is_absorbing = (sub_14[0][0] + sub_14[0][1] == 1) and (sub_14[1][0] + sub_14[1][1] == 1)
    out.append(f"  Is {{生,被生}} absorbing? {'✓' if is_absorbing else '✗ (probability leaks out)'}")
    out.append("")
    
    # Check: does the {d=0, d=2, d=3} subspace map to itself?
    sub_023_sum = [sum(T[d][d2] for d2 in [0,2,3]) for d in [0,2,3]]
    out.append(f"Restriction to {{同,克,被克}} (rows 0,2,3):")
    out.append(f"  Row sums within {{0,2,3}}: {[float(s) for s in sub_023_sum]}")
    is_023_absorbing = all(s == 1 for s in sub_023_sum)
    out.append(f"  Is {{同,克,被克}} absorbing? {'✓' if is_023_absorbing else '✗'}")
    out.append("")
    
    # Negation decomposition
    out.append("### Negation-symmetric decomposition")
    out.append("")
    out.append("Since T[d][d'] = T[−d][−d'], T commutes with the negation operator N.")
    out.append("This means T decomposes into blocks on the N-eigenspaces:")
    out.append("- N-even (symmetric): d=0, d=1+d=4, d=2+d=3 (3-dimensional)")
    out.append("- N-odd (antisymmetric): d=1−d=4, d=2−d=3 (2-dimensional)")
    out.append("")
    
    # Construct T in the symmetrized basis
    # Symmetric components: v0 = e_0, v+ = (e_1+e_4)/√2, v++ = (e_2+e_3)/√2
    # Antisymmetric: v- = (e_1-e_4)/√2, v-- = (e_2-e_3)/√2
    # T_sym is 3×3, T_anti is 2×2
    
    T_sym = [[Fraction(0)]*3 for _ in range(3)]
    # Basis: [e_0, (e_1+e_4), (e_2+e_3)]
    # T_sym[i][j] = how basis vector j maps to basis vector i under T
    
    # Row 0 (e_0): T e_0 = T[0][0]*e_0 + T[0][1]*e_1 + T[0][2]*e_2 + T[0][3]*e_3 + T[0][4]*e_4
    # In sym basis: T[0][0]*e_0 + T[0][1]*(e_1+e_4)/2 + ... but we need to be careful
    # Actually: if we use unnormalized basis {e_0, e_1+e_4, e_2+e_3} 
    # then T(e_0) = T[0][0]*e_0 + T[0][1]*e_1 + T[0][2]*e_2 + T[0][3]*e_3 + T[0][4]*e_4
    # Since T[0][1]=T[0][4] and T[0][2]=T[0][3] (by negation symmetry):
    # = T[0][0]*e_0 + T[0][1]*(e_1+e_4) + T[0][2]*(e_2+e_3)
    
    # Let's verify:
    assert T[0][1] == T[0][4], f"Neg sym violation at row 0: {T[0][1]} ≠ {T[0][4]}"
    assert T[0][2] == T[0][3], f"Neg sym violation at row 0: {T[0][2]} ≠ {T[0][3]}"
    
    T_sym[0][0] = T[0][0]
    T_sym[0][1] = T[0][1]   # coefficient of (e_1+e_4)
    T_sym[0][2] = T[0][2]   # coefficient of (e_2+e_3)
    
    # T(e_1+e_4): row 1 + row 4
    for j_sym, (j1, j2) in enumerate([(0,0), (1,4), (2,3)]):
        if j1 == j2:
            T_sym[1][j_sym] = T[1][j1] + T[4][j1]
        else:
            T_sym[1][j_sym] = T[1][j1] + T[1][j2] + T[4][j1] + T[4][j2]
    # Wait, this isn't right. Let me think more carefully.
    # T acting on basis vector b_j gives column j.
    # But T is a right-stochastic matrix: row i is the distribution from state i.
    # So T^T maps column vectors. Let me use the standard convention.
    
    # For a row-stochastic matrix T: (row vector) * T = (row vector)
    # The transition T: p_new = p * T where p is a row vector.
    # Eigendecomposition: p * T = λ * p (left eigenvector)
    
    # In the symmetric basis {e_0, (e_1+e_4)/2, (e_2+e_3)/2}:
    # Need T_sym where [a, b, c] * T_sym = [a', b', c'] with a' = ... 
    
    # Simpler: just express T in the change-of-basis
    # Symmetric block: project T onto the 3D symmetric subspace
    # Basis vectors (as row vectors): v0 = (1,0,0,0,0), v1 = (0,1,0,0,1)/2, v2 = (0,0,1,1,0)/2
    # (Not normalized, for ease)
    # v0 * T = (T[0][0], T[0][1], T[0][2], T[0][3], T[0][4])
    # Project back: coeff of v0 = T[0][0], coeff of v1 = T[0][1]+T[0][4], coeff of v2 = T[0][2]+T[0][3]
    
    T_sym = [[Fraction(0)]*3 for _ in range(3)]
    
    # Row for v0: v0 * T projected onto symmetric basis
    T_sym[0][0] = T[0][0]
    T_sym[0][1] = T[0][1] + T[0][4]
    T_sym[0][2] = T[0][2] + T[0][3]
    
    # Row for v1: (v1) * T = ((e_1+e_4)/2) * T = (T[1]+T[4])/2
    # But we use unnormalized v1 = e_1+e_4, so v1*T = T[1]+T[4] (row sums)
    r14 = [T[1][j] + T[4][j] for j in range(5)]
    T_sym[1][0] = r14[0]
    T_sym[1][1] = r14[1] + r14[4]
    T_sym[1][2] = r14[2] + r14[3]
    
    # Row for v2: (e_2+e_3)*T = T[2]+T[3]
    r23 = [T[2][j] + T[3][j] for j in range(5)]
    T_sym[2][0] = r23[0]
    T_sym[2][1] = r23[1] + r23[4]
    T_sym[2][2] = r23[2] + r23[3]
    
    # But we need to account for the fact that the basis vectors aren't normalized to 1
    # For the row-stochastic interpretation: v1 = (0,1/2,0,0,1/2), v2 = (0,0,1/2,1/2,0)
    # v1*T gives a row; we project: coeff of v0 = entry[0], coeff of 2*v1 = entry[1]+entry[4], etc.
    # Since v1 has total weight 1 (sum = 1) and v2 has total weight 1:
    # T_sym row 1: [(T[1][0]+T[4][0])/2, (T[1][1]+T[1][4]+T[4][1]+T[4][4])/2, (T[1][2]+T[1][3]+T[4][2]+T[4][3])/2]
    
    T_sym[0][0] = T[0][0]
    T_sym[0][1] = T[0][1] + T[0][4]
    T_sym[0][2] = T[0][2] + T[0][3]
    
    T_sym[1][0] = (T[1][0] + T[4][0]) / 2
    T_sym[1][1] = (T[1][1] + T[1][4] + T[4][1] + T[4][4]) / 2
    T_sym[1][2] = (T[1][2] + T[1][3] + T[4][2] + T[4][3]) / 2
    
    T_sym[2][0] = (T[2][0] + T[3][0]) / 2
    T_sym[2][1] = (T[2][1] + T[2][4] + T[3][1] + T[3][4]) / 2
    T_sym[2][2] = (T[2][2] + T[2][3] + T[3][2] + T[3][3]) / 2
    
    out.append("**Symmetric block** (basis: e₀, (e₁+e₄)/2, (e₂+e₃)/2):")
    out.append("")
    for i in range(3):
        row = [f"{float(T_sym[i][j]):.4f}" for j in range(3)]
        out.append(f"  [{', '.join(row)}]")
    out.append("")
    
    # Antisymmetric block
    T_anti = [[Fraction(0)]*2 for _ in range(2)]
    # Basis: w1 = (0,1/2,0,0,-1/2), w2 = (0,0,1/2,-1/2,0)
    # w1*T = (T[1]-T[4])/2. Project onto w1,w2:
    # coeff of 2*w1 = (entry[1]-entry[4])/1, coeff of 2*w2 = (entry[2]-entry[3])/1
    
    T_anti[0][0] = (T[1][1] - T[1][4] - T[4][1] + T[4][4]) / 2
    T_anti[0][1] = (T[1][2] - T[1][3] - T[4][2] + T[4][3]) / 2
    T_anti[1][0] = (T[2][1] - T[2][4] - T[3][1] + T[3][4]) / 2
    T_anti[1][1] = (T[2][2] - T[2][3] - T[3][2] + T[3][3]) / 2
    
    out.append("**Antisymmetric block** (basis: (e₁−e₄)/2, (e₂−e₃)/2):")
    out.append("")
    for i in range(2):
        row = [f"{float(T_anti[i][j]):.4f}" for j in range(2)]
        out.append(f"  [{', '.join(row)}]")
    out.append("")
    
    # Eigenvalues of the 2×2 antisymmetric block
    a, b = T_anti[0][0], T_anti[0][1]
    c, d = T_anti[1][0], T_anti[1][1]
    tr_anti = a + d
    det_anti = a*d - b*c
    disc_anti = tr_anti**2 - 4*det_anti
    
    out.append(f"Antisymmetric block: tr = {tr_anti} ({float(tr_anti):.6f}), "
               f"det = {det_anti} ({float(det_anti):.6f})")
    out.append(f"  Discriminant = {disc_anti} ({float(disc_anti):.6f})")
    if disc_anti >= 0:
        out.append(f"  Two real eigenvalues")
    else:
        out.append(f"  Two complex conjugate eigenvalues")
        r = float(tr_anti) / 2
        im = (-float(disc_anti))**0.5 / 2
        out.append(f"  λ = {r:.6f} ± {im:.6f}i")
        out.append(f"  |λ| = {(r**2 + im**2)**0.5:.6f}")
    out.append("")
    
    return T, counts, row_totals


# ═══════════════════════════════════════════════════════════
# Task 3: Exact P-coset alignment formula
# ═══════════════════════════════════════════════════════════

def analyze_p_coset(out):
    out.append("## Task 3: Exact P-Coset Alignment Formula")
    out.append("")
    
    # For each hexagram, compute d, mask, and P(mask)
    out.append("### Complete enumeration")
    out.append("")
    
    # Organize hexagrams by d and mask
    d_mask_table = defaultdict(list)
    for h in range(64):
        lo, up = h & 7, (h >> 3) & 7
        d = (f(up) - f(lo)) % 5
        mask = lo ^ up
        pp = P_parity(mask)
        d_mask_table[d].append((lo, up, mask, pp))
    
    # For each d, show the decomposition by mask
    for d in range(5):
        hexagrams = d_mask_table[d]
        n_total = len(hexagrams)
        n_even = sum(1 for _, _, _, pp in hexagrams if pp == 0)
        n_odd = n_total - n_even
        
        mask_breakdown = Counter()
        for _, _, mask, pp in hexagrams:
            mask_breakdown[(mask, pp)] += 1
        
        out.append(f"**d = {d} ({REL[d]}): {n_total} hexagrams, {n_even} P-even, {n_odd} P-odd**")
        out.append("")
        out.append(f"  | Mask | P(mask) | Count | Trigram pairs |")
        out.append(f"  |------|---------|-------|---------------|")
        for mask in sorted(set(m for m, _ in mask_breakdown)):
            pp = P_parity(mask)
            count = sum(1 for _, _, m, _ in hexagrams if m == mask)
            pairs = [(TRIG[lo], TRIG[up]) for lo, up, m, _ in hexagrams if m == mask]
            pair_str = ', '.join(f"{a}×{b}" for a, b in pairs[:4])
            if len(pairs) > 4:
                pair_str += f" (+{len(pairs)-4})"
            out.append(f"  | {mask:03b} | {pp} | {count} | {pair_str} |")
        out.append("")
    
    # Now derive the formula
    out.append("### Derivation of exact fractions")
    out.append("")
    
    # The fiber sizes: Wood=2, Fire=1, Earth=2, Metal=2, Water=1
    fiber_sizes = {0: 2, 1: 1, 2: 2, 3: 2, 4: 1}
    
    # For a given d, the hexagrams come from all (lower_elem, upper_elem) pairs
    # with upper_elem - lower_elem = d mod 5.
    # Count = Σ_{a ∈ Z₅} |fiber(a)| × |fiber(a+d)|
    
    out.append("**Step 1: Count hexagrams per d.**")
    out.append("")
    for d in range(5):
        total = sum(fiber_sizes[a] * fiber_sizes[(a+d)%5] for a in range(5))
        out.append(f"  |{{h : d(h)={d}}}| = Σ_a |fiber(a)| × |fiber(a+{d})| = {total}")
    out.append("")
    
    # For P-even: P(mask) = P(lower⊕upper) = P(lower)⊕P(upper) = 0
    # means lower and upper have the same P-parity.
    
    # P-parity of each trigram:
    out.append("**Step 2: P-parity of each trigram.**")
    out.append("")
    out.append("  | Trigram | Element | P-parity |")
    out.append("  |---------|---------|----------|")
    for x in range(8):
        out.append(f"  | {TRIG[x]}({x:03b}) | {ELEM[f(x)]} | {P_parity(x)} |")
    out.append("")
    
    # P-parity within each fiber:
    out.append("**Step 3: P-parity breakdown within each fiber.**")
    out.append("")
    for elem in range(5):
        fiber = [x for x in range(8) if f(x) == elem]
        p_even = sum(1 for x in fiber if P_parity(x) == 0)
        p_odd = len(fiber) - p_even
        out.append(f"  {ELEM[elem]}: fiber = {[TRIG[x] for x in fiber]}, "
                   f"P-even = {p_even}, P-odd = {p_odd}")
    out.append("")
    
    # For d and P-even: count pairs (lower, upper) with f(up)-f(lo)=d and P(lo)=P(up)
    out.append("**Step 4: P-even count per d.**")
    out.append("")
    out.append("P-even hexagrams have P(lower) = P(upper). For each element pair (a, a+d):")
    out.append("  P-even count = |{lo ∈ fiber(a), up ∈ fiber(a+d) : P(lo) = P(up)}|")
    out.append("              = fiber_P0(a) × fiber_P0(a+d) + fiber_P1(a) × fiber_P1(a+d)")
    out.append("")
    
    # Compute fiber_Pk(elem) = |{x ∈ fiber(elem) : P(x) = k}|
    fiber_P = {}
    for elem in range(5):
        fiber = [x for x in range(8) if f(x) == elem]
        fiber_P[(elem, 0)] = sum(1 for x in fiber if P_parity(x) == 0)
        fiber_P[(elem, 1)] = sum(1 for x in fiber if P_parity(x) == 1)
    
    out.append("  | Element | |fiber| | P=0 | P=1 |")
    out.append("  |---------|--------|-----|-----|")
    for elem in range(5):
        out.append(f"  | {ELEM[elem]}({elem}) | {fiber_sizes[elem]} | {fiber_P[(elem,0)]} | {fiber_P[(elem,1)]} |")
    out.append("")
    
    # Now compute P-even count for each d
    out.append("**Step 5: Exact P-even formula.**")
    out.append("")
    
    for d in range(5):
        total = 0
        p_even_count = 0
        detail_parts = []
        for a in range(5):
            b = (a + d) % 5
            n_ab = fiber_sizes[a] * fiber_sizes[b]
            n_even = fiber_P[(a,0)] * fiber_P[(b,0)] + fiber_P[(a,1)] * fiber_P[(b,1)]
            total += n_ab
            p_even_count += n_even
            detail_parts.append(f"{ELEM[a]}×{ELEM[b]}:{n_even}/{n_ab}")
        
        frac = Fraction(p_even_count, total)
        out.append(f"  d={d} ({REL[d]}): P-even = {p_even_count}/{total} = {frac} = {float(frac)*100:.1f}%")
        out.append(f"    Breakdown: {', '.join(detail_parts)}")
    out.append("")
    
    # Verify against known values
    out.append("### Verification against measured values")
    out.append("")
    
    known = {0: (14, 14), 1: (8, 12), 2: (1, 13), 3: (1, 13), 4: (8, 12)}
    all_match = True
    for d in range(5):
        total = sum(fiber_sizes[a] * fiber_sizes[(a+d)%5] for a in range(5))
        p_even = sum(fiber_P[(a,0)]*fiber_P[((a+d)%5,0)] + fiber_P[(a,1)]*fiber_P[((a+d)%5,1)] for a in range(5))
        expected_even, expected_total = known[d]
        match = (p_even == expected_even and total == expected_total)
        all_match = all_match and match
        out.append(f"  d={d}: formula gives {p_even}/{total}, measured = {expected_even}/{expected_total}: {'✓' if match else '✗'}")
    out.append("")
    out.append(f"**All match: {'✓' if all_match else '✗'}**")
    out.append("")
    
    # The closed-form explanation
    out.append("### Closed-form explanation")
    out.append("")
    out.append("The P-coset alignment fraction for relation d is:")
    out.append("")
    out.append("```")
    out.append("         Σ_a [fiber_P0(a)·fiber_P0(a+d) + fiber_P1(a)·fiber_P1(a+d)]")
    out.append("F(d) = ──────────────────────────────────────────────────────────────")
    out.append("                    Σ_a |fiber(a)| · |fiber(a+d)|")
    out.append("```")
    out.append("")
    out.append("Where fiber_Pk(a) = |{x ∈ f⁻¹(a) : P(x) = k}|.")
    out.append("")
    out.append("The key structural facts explaining the exact fractions:")
    out.append("")
    
    out.append("1. **同 (d=0) is 100% P-even** because within each fiber, every pair")
    out.append("   (lo, up) with lo,up in the same fiber has P(lo⊕up) = 0.")
    out.append("   This follows from the doubleton fiber XORs being P-even:")
    out.append("   Wood: 001⊕110 = 111, P(111) = 0. Earth: 000⊕100 = 100, P(100) = 0.")
    out.append("   Metal: 011⊕111 = 100, P(100) = 0. Singletons: 0⊕0 = 0, P(0) = 0.")
    out.append("")
    
    out.append("2. **克/被克 (d=2,3) is 92% P-odd** because the doubleton-to-doubleton")
    out.append("   pairs at stride-2 on Z₅ use masks M(010) and MI(110), both P-odd.")
    out.append("   The only P-even hexagram at d=2 is the singleton pair 坎×離")
    out.append("   (Water×Fire, mask = 111, P(111) = 0). Similarly for d=3.")
    out.append("")
    
    out.append("3. **生/被生 (d=1,4) is 67% P-even** because stride-1 mixes:")
    out.append("   the exclusive 生-mask OM(011) has P = 0, but non-exclusive masks")
    out.append("   (I=100, OI=101) from doubleton-to-singleton transitions have P = 0 and 1")
    out.append("   respectively, diluting toward 50%. The 8/12 fraction reflects the exact")
    out.append("   balance: 4 pairs via P-even exclusive mask + 4 P-even from doubleton-singleton")
    out.append("   alignment, vs 4 P-odd from misaligned doubleton-singleton transitions.")
    out.append("")
    
    out.append("### The hierarchy")
    out.append("")
    out.append("| d | Relation | P-even fraction | P-even numerics | Origin |")
    out.append("|---|----------|----------------|-----------------|--------|")
    out.append("| 0 | 同 | 14/14 = 1 | 100% | All same-fiber XORs are P-even |")
    out.append("| 1 | 生 | 8/12 = 2/3 | 66.7% | OM exclusive mask is P-even; mixed dilution |")
    out.append("| 4 | 被生 | 8/12 = 2/3 | 66.7% | Same by negation symmetry |")
    out.append("| 2 | 克 | 1/13 | 7.7% | M, MI exclusive masks are P-odd; 1 singleton exception |")
    out.append("| 3 | 被克 | 1/13 | 7.7% | Same by negation symmetry |")
    out.append("")
    out.append("This is the exact, derived P-coset alignment table. The fractions are")
    out.append("not approximate — they follow deterministically from the fiber partition")
    out.append("{2,2,2,1,1} and the P-parity structure of each fiber.")


def main():
    out = []
    out.append("# 互 Transition Eigenstructure + P-Coset Alignment Formula")
    out.append("")
    
    analyze_eigenstructure(out)
    out.append("---")
    out.append("")
    analyze_p_coset(out)
    
    path = "/home/quasar/nous/memories/iching/unification/eigenstructure_results.md"
    with open(path, 'w') as fout:
        fout.write('\n'.join(out))
    print(f"Written to {path}")
    print(f"Lines: {len(out)}")


if __name__ == '__main__':
    main()
