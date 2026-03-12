#!/usr/bin/env python3
"""
boolean_analysis.py — The IC surjection as a Boolean function

Analyzes:
1. Algebraic Normal Form (ANF) over Z₅
2. Complement constraint in ANF form
3. Indicator functions g_k and their Walsh-Hadamard spectra
4. Comparison across all 5 orbits
"""

import sys, io
from collections import Counter, defaultdict
from itertools import product as iterproduct

# ═══════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════

IC = [2, 0, 4, 3, 2, 1, 0, 3]
TRIG_ZH = {0:'坤', 1:'震', 2:'坎', 3:'兌', 4:'艮', 5:'離', 6:'巽', 7:'乾'}
ELEM = {0:'Wood', 1:'Fire', 2:'Earth', 3:'Metal', 4:'Water'}
P = 5

def fmt(x): return format(x, '03b')
def complement(x): return x ^ 7
def popcount(x): return bin(x).count('1')
def inner(s, x): return popcount(s & x) % 2  # <s,x> in F₂


# ═══════════════════════════════════════════════════════════
# ANF over Z₅
# ═══════════════════════════════════════════════════════════

# Monomials: indexed by subset S ⊆ {0,1,2}
# Monomial S evaluates to ∏_{i∈S} x_i (in F₂).
# The monomial value is 1 iff all bits in S are set in x.
MONOMIAL_LABELS = {
    0: '1', 1: 'x₀', 2: 'x₁', 3: 'x₀x₁',
    4: 'x₂', 5: 'x₀x₂', 6: 'x₁x₂', 7: 'x₀x₁x₂'
}

def monomial_eval(S, x):
    """Evaluate monomial S at point x: 1 iff (x & S) == S."""
    return 1 if (x & S) == S else 0

def compute_anf(f, p=5):
    """Compute ANF coefficients a_S such that f(x) = Σ_S a_S ∏_{i∈S} x_i mod p.
    Uses Möbius inversion over subsets."""
    # ANF via Möbius: a_S = Σ_{T⊆S} f(T) mod p (for Boolean functions)
    # But our f maps to Z_p, not F₂. The formula still works:
    # f(x) = Σ_S a_S · m_S(x) where m_S(x) = ∏_{i∈S} x_i ∈ {0,1}
    # Solve: 8×8 system. The Möbius inversion gives:
    # a_S = Σ_{T⊆S} (-1)^{|S\T|} f(T) = Σ_{T⊆S} (-1)^{|S|-|T|} f(T) mod p
    coeffs = {}
    for S in range(8):
        val = 0
        for T in range(8):
            if (T & S) == T:  # T ⊆ S
                sign = (-1) ** (popcount(S) - popcount(T))
                val = (val + sign * f[T]) % p
        coeffs[S] = val % p
    return coeffs

def verify_anf(coeffs, f, p=5):
    """Verify ANF reconstruction."""
    for x in range(8):
        val = 0
        for S in range(8):
            val = (val + coeffs[S] * monomial_eval(S, x)) % p
        if val != f[x]:
            return False
    return True


# ═══════════════════════════════════════════════════════════
# Complement constraint in ANF
# ═══════════════════════════════════════════════════════════

def analyze_complement_constraint(coeffs, p=5):
    """f(x⊕111) = -f(x) constrains ANF coefficients.
    
    m_S(x⊕111) = ∏_{i∈S} (1-x_i) = Σ_{T⊆S} (-1)^|T| m_T(x).
    
    f(x⊕111) = Σ_S a_S Σ_{T⊆S} (-1)^|T| m_T(x)
             = Σ_T [(-1)^|T| Σ_{S⊇T} a_S] m_T(x).
    
    Setting equal to -f(x) = Σ_T (-a_T) m_T(x):
    
    (-1)^|T| Σ_{S⊇T} a_S = -a_T for all T.
    
    Even |T|:  Σ_{S⊇T} a_S = -a_T → 2a_T + Σ_{S⊋T} a_S = 0
    Odd |T|:  -Σ_{S⊇T} a_S = -a_T → Σ_{S⊋T} a_S = 0
    """
    constraints = []
    for T in range(8):
        T_size = popcount(T)
        sup_sum = sum(coeffs[S] for S in range(8) if (S & T) == T and S != T) % p
        
        if T_size % 2 == 0:
            # Even: 2a_T + Σ_{S⊋T} a_S ≡ 0 mod p
            residual = (2 * coeffs[T] + sup_sum) % p
            desc = f"2·{coeffs[T]}+{sup_sum}={residual}"
        else:
            # Odd: Σ_{S⊋T} a_S ≡ 0 mod p
            residual = sup_sum % p
            desc = f"Σsup={sup_sum}"
        
        satisfied = (residual == 0)
        constraints.append((T, T_size, desc, satisfied))
    return constraints


# ═══════════════════════════════════════════════════════════
# Indicator functions and Walsh spectrum
# ═══════════════════════════════════════════════════════════

def walsh_hadamard(g):
    """Walsh-Hadamard transform of g: F₂³ → {0,1}.
    ĝ(s) = Σ_x (-1)^{g(x) ⊕ <s,x>}"""
    spectrum = {}
    for s in range(8):
        val = 0
        for x in range(8):
            exponent = g[x] ^ inner(s, x)
            val += (-1) ** exponent
        spectrum[s] = val
    return spectrum

def indicator(f, k, p=5):
    """g_k(x) = 1 if f(x) = k, else 0."""
    return [1 if f[x] == k else 0 for x in range(8)]

def algebraic_degree(g):
    """Degree of Boolean function g via ANF over F₂."""
    # ANF via Möbius
    anf = {}
    for S in range(8):
        val = 0
        for T in range(8):
            if (T & S) == T:
                val ^= g[T]
        anf[S] = val
    deg = 0
    for S in range(8):
        if anf[S] == 1:
            deg = max(deg, popcount(S))
    return deg, anf

def nonlinearity(g):
    """NL(g) = (2^n - max_s |ĝ(s)|) / 2 = (8 - max|ĝ|) / 2"""
    spec = walsh_hadamard(g)
    max_abs = max(abs(v) for v in spec.values())
    return (8 - max_abs) / 2, spec


# ═══════════════════════════════════════════════════════════
# Orbit infrastructure (minimal)
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

def mat_vec_f2(A, v):
    result = 0
    for i in range(3):
        s = 0
        for j in range(3):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_det_f2(A):
    a,b,c = A[0]; d,e,f_ = A[1]; g,h,k = A[2]
    return (a*(e*k ^ f_*h) ^ b*(d*k ^ f_*g) ^ c*(d*h ^ e*g)) & 1

def mat_inv_f2(A):
    M = [A[i][:] + [1 if i==j else 0 for j in range(3)] for i in range(3)]
    for col in range(3):
        pivot = None
        for row in range(col, 3):
            if M[row][col]: pivot = row; break
        if pivot is None: return None
        if pivot != col: M[col], M[pivot] = M[pivot], M[col]
        for row in range(3):
            if row != col and M[row][col]:
                M[row] = [M[row][j] ^ M[col][j] for j in range(6)]
    return [M[i][3:] for i in range(3)]

def compute_orbits():
    surjections = enumerate_surjections()
    gl3 = []
    for row0 in range(1,8):
        for row1 in range(1,8):
            for row2 in range(1,8):
                A = [[(row0>>j)&1 for j in range(3)],
                     [(row1>>j)&1 for j in range(3)],
                     [(row2>>j)&1 for j in range(3)]]
                if mat_det_f2(A): gl3.append(A)
    stab = [A for A in gl3 if mat_vec_f2(A, 7) == 7]
    stab_invs = [mat_inv_f2(A) for A in stab]
    aut = list(range(1, P))
    
    from collections import defaultdict
    parent = {s: s for s in surjections}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    
    surj_set = set(surjections)
    for s in surjections:
        for A_inv in stab_invs:
            for alpha in aut:
                t = tuple((alpha * s[mat_vec_f2(A_inv, x)]) % P for x in range(8))
                if t in surj_set:
                    union(s, t)
    
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

    try:
        print("=" * 72)
        print("  THE IC SURJECTION AS A BOOLEAN FUNCTION")
        print("=" * 72)
        print()
        
        # ─── 1. ANF over Z₅ ───
        print("  " + "=" * 68)
        print("  1. ALGEBRAIC NORMAL FORM (ANF) OVER Z₅")
        print("  " + "=" * 68)
        print()
        print(f"  f = {IC}")
        print(f"  f(x₂x₁x₀) = Σ_S a_S · m_S(x) mod 5")
        print()
        
        coeffs = compute_anf(IC, P)
        ok = verify_anf(coeffs, IC, P)
        
        print(f"  ANF coefficients:")
        for S in range(8):
            if coeffs[S] != 0:
                print(f"    a_{{{MONOMIAL_LABELS[S]}}} = {coeffs[S]}")
        print()
        print(f"  Full polynomial:")
        terms = []
        for S in range(8):
            if coeffs[S] != 0:
                if S == 0:
                    terms.append(str(coeffs[S]))
                else:
                    c = coeffs[S] if coeffs[S] != 1 else ''
                    terms.append(f"{c}{MONOMIAL_LABELS[S]}")
        print(f"  f = {' + '.join(terms)} (mod 5)")
        print(f"  Verification: {'✓' if ok else '✗'}")
        print()
        
        # Algebraic degree (over Z₅)
        max_deg = max(popcount(S) for S in range(8) if coeffs[S] != 0)
        print(f"  Algebraic degree: {max_deg}")
        # Count nonzero coefficients
        nz = sum(1 for S in range(8) if coeffs[S] != 0)
        print(f"  Nonzero coefficients: {nz}/8")
        print()
        
        # ─── 2. Complement constraint ───
        print("  " + "=" * 68)
        print("  2. COMPLEMENT CONSTRAINT IN ANF FORM")
        print("  " + "=" * 68)
        print()
        print("  f(x⊕111) = -f(x) mod 5 implies:")
        print("  For each T: Σ_{S⊇T} a_S ≡ -a_T mod 5")
        print("  i.e., 2·a_T + Σ_{S⊋T} a_S ≡ 0 mod 5")
        print()
        
        constraints = analyze_complement_constraint(coeffs, P)
        for T, T_size, desc, sat in constraints:
            parity = "even" if T_size % 2 == 0 else "odd"
            rule = "2a_T+Σsup=0" if T_size % 2 == 0 else "Σsup=0"
            print(f"  T={MONOMIAL_LABELS[T]:>7} (|T|={T_size},{parity:>4}): {desc:>15} ≡ 0? {'✓' if sat else '✗'}  [{rule}]")
        
        print()
        
        # Derive the general constraint
        print("  General constraints for ANY complement-respecting surjection:")
        print()
        print("  Even |T|: 2a_T + Σ_{S⊋T} a_S = 0 mod 5 → a_T = 3·(-Σ_{S⊋T} a_S) mod 5")
        print("  Odd |T|:  Σ_{S⊋T} a_S = 0 mod 5")
        print()
        print("  Degree 3 (|T|=3, odd): No supersets → 0 = 0. Always true. a₇ is FREE.")
        print("  Degree 2 (|T|=2, even): 2a_{ij} + a_{ijk} = 0 → a_{ij} = 2·a₇")
        print("  Degree 1 (|T|=1, odd): Σ_{S⊋T} a_S = a_{ij}+a_{ik}+a_{ijk} = 2a₇+2a₇+a₇ = 5a₇ = 0 ✓")
        print("    → Degree-1 coefficients a₁, a₂, a₄ are UNCONSTRAINED (always satisfied)")
        print("  Degree 0 (|T|=0, even): 2a₀ + (a₁+a₂+a₄) + 3·(2a₇) + a₇ = 0")
        print("    → 2a₀ + (a₁+a₂+a₄) + 7a₇ = 0 → a₀ = 3·(-(a₁+a₂+a₄) - 2a₇) mod 5")
        print()
        print("  FREE PARAMETERS: a₁, a₂, a₄, a₇ (4 free, each ∈ Z₅)")
        print("  DETERMINED: a₀ from above, a₃=a₅=a₆ = 2a₇")
        print("  Total complement-respecting functions: 5⁴ = 625 (of which 240 surjective)")
        print()
        
        # Verify this for the IC surjection
        a7 = coeffs[7]  # x₀x₁x₂
        for S in [3, 5, 6]:  # x₀x₁, x₀x₂, x₁x₂
            expected_val = (2 * a7) % P
            actual = coeffs[S]
            print(f"  a_{{{MONOMIAL_LABELS[S]}}} = {actual}, 2·a_{{x₀x₁x₂}} = {expected_val}: {'✓' if actual == expected_val else '✗'}")
        
        print()
        
        # ─── 3. Indicator functions ───
        print("  " + "=" * 68)
        print("  3. INDICATOR FUNCTIONS AND WALSH SPECTRA")
        print("  " + "=" * 68)
        print()
        
        for k in range(P):
            g = indicator(IC, k, P)
            deg, anf = algebraic_degree(g)
            nl, spec = nonlinearity(g)
            support = sum(g)
            
            print(f"  g_{k}(x) = [f(x) = {k}] ({ELEM[k]})")
            print(f"    Support: {support} ({[fmt(x) for x in range(8) if g[x]]})")
            print(f"    Algebraic degree: {deg}")
            
            # ANF terms
            anf_terms = [MONOMIAL_LABELS[S] for S in range(8) if anf[S] == 1]
            print(f"    ANF: {' ⊕ '.join(anf_terms) if anf_terms else '0'}")
            
            # Walsh spectrum
            spec_str = ', '.join(f"ĝ({fmt(s)})={spec[s]}" for s in range(8))
            print(f"    Walsh: {{{spec_str}}}")
            print(f"    Nonlinearity: {nl}")
            print()
        
        # ─── 4. Cross-orbit comparison ───
        print("  " + "=" * 68)
        print("  4. ANF COMPARISON ACROSS ALL 5 ORBITS")
        print("  " + "=" * 68)
        print()
        
        orbits = compute_orbits()
        ic_tuple = tuple(IC)
        
        print(f"  {'Orbit':>5} {'Size':>5} {'f':>25} {'ANF coeffs':>25} {'Deg':>3} {'#NZ':>3}")
        print(f"  {'-'*67}")
        
        for idx, orbit in enumerate(orbits):
            rep = sorted(orbit)[0]
            is_ic = ic_tuple in orbit
            c = compute_anf(list(rep), P)
            deg = max((popcount(S) for S in range(8) if c[S] != 0), default=0)
            nz = sum(1 for S in range(8) if c[S] != 0)
            
            coeff_str = str([c[S] for S in range(8)])
            marker = " ★" if is_ic else ""
            print(f"  {idx:>5} {len(orbit):>5} {str(list(rep)):>25} {coeff_str:>25} {deg:>3} {nz:>3}{marker}")
        
        print()
        
        # Check if ANF structure is orbit-invariant
        print("  ANF structure orbit-invariance check:")
        for idx, orbit in enumerate(orbits):
            is_ic = ic_tuple in orbit
            degs = set()
            nzs = set()
            coeff_patterns = set()
            for s in orbit:
                c = compute_anf(list(s), P)
                deg = max((popcount(S) for S in range(8) if c[S] != 0), default=0)
                nz = sum(1 for S in range(8) if c[S] != 0)
                degs.add(deg)
                nzs.add(nz)
                # Pattern: which coefficients are nonzero
                pattern = tuple(1 if c[S] != 0 else 0 for S in range(8))
                coeff_patterns.add(pattern)
            
            marker = " ★" if is_ic else ""
            deg_inv = "✓" if len(degs) == 1 else f"({degs})"
            nz_inv = "✓" if len(nzs) == 1 else f"({nzs})"
            print(f"    Orbit {idx}: deg {deg_inv}, #NZ {nz_inv}, {len(coeff_patterns)} coeff patterns{marker}")
        
        # Check which ANF relations hold universally
        print()
        print("  UNIVERSAL ANF PROPERTIES (all 240 surjections):")
        print()
        
        all_surj = enumerate_surjections()
        
        # Check full complement constraint
        all_complement_ok = True
        for s in all_surj:
            c = compute_anf(list(s), P)
            cons = analyze_complement_constraint(c, P)
            if not all(sat for _, _, _, sat in cons):
                all_complement_ok = False
                break
        print(f"  Full complement constraint (parity-correct): {'✓' if all_complement_ok else '✗'}")
        
        # Check degree-2 coefficient equality
        all_eq = True
        for s in all_surj:
            c = compute_anf(list(s), P)
            a7 = c[7]
            for S in [3, 5, 6]:
                if c[S] != (2 * a7) % P:
                    all_eq = False
                    break
        print(f"  a_{{ij}} = 2·a_{{012}} mod 5: {'✓' if all_eq else '✗'}")
        
        # Check a₀ = 3·(-(a₁+a₂+a₄) - 2a₇) mod 5
        all_a0 = True
        for s in all_surj:
            c = compute_anf(list(s), P)
            expected_a0 = (3 * (-(c[1] + c[2] + c[4]) - 2 * c[7])) % P
            if c[0] != expected_a0:
                all_a0 = False
                break
        print(f"  a₀ = 3·(-(a₁+a₂+a₄) - 2a₇): {'✓' if all_a0 else '✗'}")
        
        # Degree-1 distribution
        deg1_vals = defaultdict(Counter)
        for s in all_surj:
            c = compute_anf(list(s), P)
            for S in [1, 2, 4]:
                deg1_vals[S][c[S]] += 1
        
        print(f"  a_{{x₀}} distribution: {dict(sorted(deg1_vals[1].items()))}")
        print(f"  a_{{x₁}} distribution: {dict(sorted(deg1_vals[2].items()))}")
        print(f"  a_{{x₂}} distribution: {dict(sorted(deg1_vals[4].items()))}")
        print()
        
        # Distinct ANF coefficient tuples
        anf_tuples = set()
        for s in all_surj:
            c = compute_anf(list(s), P)
            anf_tuples.add(tuple(c[S] for S in range(8)))
        print(f"  Distinct ANF coefficient vectors: {len(anf_tuples)}")
        
        # Group by a₇
        by_a7 = Counter()
        for s in all_surj:
            c = compute_anf(list(s), P)
            by_a7[c[7]] += 1
        print(f"  Distribution by a₇: {dict(sorted(by_a7.items()))}")
        
        # Count of complement-respecting functions (surjective or not)
        comp_count = 0
        for a1 in range(P):
            for a2 in range(P):
                for a4 in range(P):
                    for a7 in range(P):
                        a0 = (3 * (-(a1 + a2 + a4) - 2*a7)) % P
                        a3 = a5 = a6 = (2*a7) % P
                        f_vals = []
                        for x in range(8):
                            val = a0
                            if x & 1: val = (val + a1) % P
                            if x & 2: val = (val + a2) % P
                            if x & 4: val = (val + a4) % P
                            if x & 3 == 3: val = (val + a3) % P
                            if x & 5 == 5: val = (val + a5) % P
                            if x & 6 == 6: val = (val + a6) % P
                            if x & 7 == 7: val = (val + a7) % P
                            f_vals.append(val % P)
                        comp_count += 1
        surj_from_params = 0
        for a1 in range(P):
            for a2 in range(P):
                for a4 in range(P):
                    for a7 in range(P):
                        a0 = (3 * (-(a1 + a2 + a4) - 2*a7)) % P
                        coeffs_test = {0:a0, 1:a1, 2:a2, 3:(2*a7)%P,
                                       4:a4, 5:(2*a7)%P, 6:(2*a7)%P, 7:a7}
                        f_vals = []
                        for x in range(8):
                            val = 0
                            for S in range(8):
                                if monomial_eval(S, x):
                                    val = (val + coeffs_test[S]) % P
                            f_vals.append(val)
                        if len(set(f_vals)) == P:
                            surj_from_params += 1
        
        print(f"\n  Total complement-respecting functions: {comp_count} (= 5⁴ = 625)")
        print(f"  Of which surjective: {surj_from_params} (should = 240)")
        
        print("  " + "=" * 68)
        print("  SUMMARY")
        print("  " + "=" * 68)
        print()
        print("  1. PARAMETRIZATION: Complement-respecting functions F₂³ → Z₅")
        print("     are parametrized by 4 free coefficients (a₁, a₂, a₄, a₇) ∈ Z₅⁴.")
        print("     Total: 5⁴ = 625 functions. Of these, 240 are surjective.")
        print()
        print("  2. UNIVERSAL RELATION: a_{x₀x₁} = a_{x₀x₂} = a_{x₁x₂} = 2·a₇ mod 5")
        print("     All degree-2 coefficients are locked to the cubic coefficient.")
        print("     a₀ is determined by a₁ + a₂ + a₄ + 2a₇.")
        print()
        print("  3. DEGREE-1 COEFFICIENTS (a₁, a₂, a₄) break the S₃ symmetry of")
        print("     the Boolean cube. They are the 'orientation' parameters that")
        print("     distinguish surjections within the same orbit.")
        print()
        print("  4. a₇ (the cubic coefficient) determines the 'type' of the")
        print("     surjection modulo orientation. Distribution: 48 surjections/value.")
        print("     a₇ = 0 forces all degree-2 coefficients to 0 (degree ≤ 1).")
        print()
        print("  5. IC SURJECTION:")
        print(f"     f = {' + '.join(terms)} (mod 5)")
        print(f"     (a₁,a₂,a₄,a₇) = ({coeffs[1]},{coeffs[2]},{coeffs[4]},{coeffs[7]})")

    finally:
        sys.stdout = old_stdout
    
    path = "/home/quasar/nous/memories/iching/relations/boolean_analysis_output.md"
    with open(path, 'w') as out:
        out.write(captured.getvalue())
    print(f"\nResults written to {path}")


if __name__ == "__main__":
    main()
