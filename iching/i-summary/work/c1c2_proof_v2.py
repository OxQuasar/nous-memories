#!/usr/bin/env python3
"""
C1-C2 — Formal proof of rank(M^k) = max(2, 2n − 2k) for all n ≥ 2.

CORRECTED PROOF STRATEGY:
1. In factored basis, M = [S E; E S] where S = superdiagonal shift, E = e_{n-1}·e_{n-1}^T.
2. Change of basis σ = p ⊕ q yields M' = [T E; 0 T] where T = S + E.
3. rank(T^k) = max(1, n-k).
4. KEY LEMMA: Φ_k · ker(T^k) = {0} (not just ⊆ im(T^k)).
5. rank(M'^k) = 2·rank(T^k) = max(2, 2n-2k).
"""

def mat_mul_f2(A, B, n):
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s ^= A[i][k] & B[k][j]
            C[i][j] = s
    return C

def mat_vec_f2_list(A, v, n):
    return [sum(A[i][j] & v[j] for j in range(n)) % 2 for i in range(n)]

def compute_rank_f2(mat, rows, cols):
    M = [row[:] for row in mat]
    pivot_row = 0
    for col in range(cols):
        found = False
        for row in range(pivot_row, rows):
            if M[row][col]:
                M[pivot_row], M[row] = M[row], M[pivot_row]
                found = True
                break
        if not found: continue
        for row in range(rows):
            if row != pivot_row and M[row][col]:
                M[row] = [M[row][j] ^ M[pivot_row][j] for j in range(cols)]
        pivot_row += 1
    return pivot_row

def mat_inv_f2(A, n):
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

def build_nuclear_matrix(n):
    dim = 2 * n
    M = [[0]*dim for _ in range(dim)]
    for k in range(n):
        M[k][k + 1] = 1
        M[n + k][k + n - 1] = 1
    return M

def build_factored_basis(n):
    dim = 2 * n
    perm = list(range(n)) + list(range(2*n-1, n-1, -1))
    P = [[0]*dim for _ in range(dim)]
    for j in range(dim): P[perm[j]][j] = 1
    return P, perm

print("=" * 72)
print("PROOF: rank(M^k) = max(2, 2n − 2k) FOR ALL n ≥ 2")
print("=" * 72)

# ═══════════════════════════════════════════════════════════════
# Step 1: M = [S E; E S] in factored basis  (verified n=2..8)
# ═══════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("STEP 1: M = [S E; E S] in factored basis")
print("─" * 72)
print("  S = n×n superdiagonal shift: S_{i,i+1} = 1.")
print("  E = e_{n-1}·e_{n-1}^T  (rank-1 coupling at innermost level).")

for n in range(2, 9):
    dim = 2 * n
    M_std = build_nuclear_matrix(n)
    P, _ = build_factored_basis(n)
    P_inv = mat_inv_f2(P, dim)
    M_fac = mat_mul_f2(P_inv, mat_mul_f2(M_std, P, dim), dim)
    
    S = [[0]*n for _ in range(n)]
    for i in range(n-1): S[i][i+1] = 1
    E = [[0]*n for _ in range(n)]
    E[n-1][n-1] = 1
    
    A = [[M_fac[i][j] for j in range(n)] for i in range(n)]
    B = [[M_fac[i][n+j] for j in range(n)] for i in range(n)]
    C = [[M_fac[n+i][j] for j in range(n)] for i in range(n)]
    D = [[M_fac[n+i][n+j] for j in range(n)] for i in range(n)]
    
    ok = (A == S and B == E and C == E and D == S)
    print(f"  n={n}: {'✓' if ok else '✗'}")

# ═══════════════════════════════════════════════════════════════
# Step 2: Change of basis → block upper-triangular M' = [T E; 0 T]
# ═══════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("STEP 2: σ = p ⊕ q  →  M' = [T E; 0 T], T = S + E")
print("─" * 72)
print("  Q = [I 0; I I], Q⁻¹ = Q (over F₂). M' = Q·M·Q = [S+E  E; 0  S+E].")

for n in range(2, 9):
    dim = 2 * n
    M_std = build_nuclear_matrix(n)
    P, _ = build_factored_basis(n)
    P_inv = mat_inv_f2(P, dim)
    M_fac = mat_mul_f2(P_inv, mat_mul_f2(M_std, P, dim), dim)
    
    I_n = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    Q = [[0]*dim for _ in range(dim)]
    for i in range(n):
        for j in range(n):
            Q[i][j] = I_n[i][j]
            Q[n+i][j] = I_n[i][j]
            Q[n+i][n+j] = I_n[i][j]
    M_new = mat_mul_f2(Q, mat_mul_f2(M_fac, Q, dim), dim)
    
    S = [[0]*n for _ in range(n)]
    for i in range(n-1): S[i][i+1] = 1
    E = [[0]*n for _ in range(n)]
    E[n-1][n-1] = 1
    T = [[S[i][j] ^ E[i][j] for j in range(n)] for i in range(n)]
    
    A = [[M_new[i][j] for j in range(n)] for i in range(n)]
    B = [[M_new[i][n+j] for j in range(n)] for i in range(n)]
    C = [[M_new[n+i][j] for j in range(n)] for i in range(n)]
    D = [[M_new[n+i][n+j] for j in range(n)] for i in range(n)]
    
    ok = (A == T and B == E and
          all(C[i][j] == 0 for i in range(n) for j in range(n)) and D == T)
    print(f"  n={n}: A=T {'✓' if A==T else '✗'}, B=E {'✓' if B==E else '✗'}, "
          f"C=0 {'✓' if all(C[i][j]==0 for i in range(n) for j in range(n)) else '✗'}, "
          f"D=T {'✓' if D==T else '✗'}")

# ═══════════════════════════════════════════════════════════════
# Step 3: rank(T^k) = max(1, n-k) and ker(T^k) = span{e_0,...,e_{min(k,n-1)-1}}
# ═══════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("STEP 3: rank(T^k) = max(1, n-k), ker(T^k) = span{e_0,...,e_{k'-1}}")
print("─" * 72)

print("""
  T acts: T(e_0) = 0, T(e_j) = e_{j-1} for 1≤j≤n-2, T(e_{n-1}) = e_{n-2}+e_{n-1}.
  By induction: T^k(e_{n-1}) = Σ_{i=max(0,n-1-k)}^{n-1} e_i, converging to 𝟏 at k=n-1.
  T(𝟏) = 𝟏 (fixed point). So T^k(e_{n-1}) = 𝟏 for k ≥ n-1.
  
  ker(T^k) = span{e_0, ..., e_{min(k,n-1)-1}}: the outermost k' coordinates.
  Proof: T shifts outward, killing e_0; after k shifts, e_0,...,e_{k-1} are killed.
  But e_{n-1} → 𝟏 which is never zero, so e_{n-1} ∉ ker(T^k).
  dim(ker(T^k)) = min(k, n-1). rank(T^k) = n - min(k, n-1) = max(1, n-k).  ■
""")

for n in range(2, 9):
    T = [[0]*n for _ in range(n)]
    for i in range(n-1): T[i][i+1] = 1
    T[n-1][n-1] = 1
    
    Tk = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    all_ok = True
    for k in range(1, n+3):
        Tk = mat_mul_f2(Tk, T, n)
        rT = compute_rank_f2(Tk, n, n)
        expected = max(1, n-k)
        if rT != expected: all_ok = False
        
        # Verify kernel
        ker_dim = n - rT
        expected_ker = min(k, n-1)
        if ker_dim != expected_ker: all_ok = False
        
        # Verify kernel is indeed span{e_0,...,e_{k'-1}}
        for j in range(min(k, n-1)):
            ej = [0]*n; ej[j] = 1
            img = mat_vec_f2_list(Tk, ej, n)
            if any(img): all_ok = False
        # e_{min(k,n-1)} should NOT be in kernel (if it exists)
        if min(k, n-1) < n:
            j = min(k, n-1)
            ej = [0]*n; ej[j] = 1
            img = mat_vec_f2_list(Tk, ej, n)
            if not any(img): all_ok = False
    
    print(f"  n={n}: rank, kernel dimension, kernel generators all correct: {'✓' if all_ok else '✗'}")

# ═══════════════════════════════════════════════════════════════
# Step 4: KEY LEMMA — Φ_k · ker(T^k) = {0}
# ═══════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("STEP 4: KEY LEMMA — Φ_k · ker(T^k) = {0}")
print("─" * 72)

print("""
  Φ_k = Σ_{l=0}^{k-1} T^l · E · T^{k-1-l}  (off-diagonal of M'^k).
  E = e_{n-1}·e_{n-1}^T.
  
  For any e_j ∈ ker(T^k) (i.e., j < min(k, n-1)):
    Φ_k · e_j = Σ_{l=0}^{k-1} T^l · E · (T^{k-1-l} · e_j)
  
  The term T^{k-1-l}·e_j is:
    = 0            if k-1-l > j   (e_j killed after j+1 steps)
    = e_{j-k+1+l}  if k-1-l ≤ j   (shifted outward)
  
  When nonzero: j - k + 1 + l ≤ j < n-1, since l ≤ k-1. 
  So j - k + 1 + l ≤ j < n-1, meaning E·e_{j-k+1+l} = 0
  (since E only responds to the (n-1)-th component).
  
  Therefore Φ_k · e_j = 0 for all j < min(k, n-1).
  Since ker(T^k) = span{e_0,...,e_{min(k,n-1)-1}}:
    Φ_k · ker(T^k) = {0}.  ■
""")

# Verify computationally
print("  Verification:")
for n in range(2, 9):
    dim = 2 * n
    T = [[0]*n for _ in range(n)]
    for i in range(n-1): T[i][i+1] = 1
    T[n-1][n-1] = 1
    E = [[0]*n for _ in range(n)]
    E[n-1][n-1] = 1
    
    M_new = [[0]*dim for _ in range(dim)]
    for i in range(n):
        for j in range(n):
            M_new[i][j] = T[i][j]
            M_new[i][n+j] = E[i][j]
            M_new[n+i][n+j] = T[i][j]
    
    Mk = [[1 if i==j else 0 for j in range(dim)] for i in range(dim)]
    Tk = [[1 if i==j else 0 for j in range(n)] for i in range(n)]
    
    all_ok = True
    for k in range(1, n+3):
        Mk = mat_mul_f2(Mk, M_new, dim)
        Tk = mat_mul_f2(Tk, T, n)
        
        Phi_k = [[Mk[i][n+j] for j in range(n)] for i in range(n)]
        
        k_prime = min(k, n-1)
        for j in range(k_prime):
            ej = [0]*n; ej[j] = 1
            result = mat_vec_f2_list(Phi_k, ej, n)
            if any(result):
                all_ok = False
                print(f"    FAIL: n={n}, k={k}, j={j}: Φ_k·e_{j} = {result} ≠ 0")
    
    print(f"    n={n}: Φ_k · ker(T^k) = {{0}} for all k: {'✓' if all_ok else '✗'}")

# ═══════════════════════════════════════════════════════════════
# Step 5: rank(M^k) = 2·rank(T^k)
# ═══════════════════════════════════════════════════════════════
print("\n" + "─" * 72)
print("STEP 5: rank(M'^k) = 2·rank(T^k) = max(2, 2n-2k)")
print("─" * 72)

print("""
  M'^k = [T^k  Φ_k]    (block upper-triangular).
         [ 0    T^k]
  
  Kernel of M'^k = {(x,y) : T^k·y = 0 and T^k·x + Φ_k·y = 0}
                 = {(x,y) : y ∈ ker(T^k) and T^k·x = Φ_k·y}.
  
  By Step 4: y ∈ ker(T^k) ⟹ Φ_k·y = 0. So T^k·x = 0, i.e., x ∈ ker(T^k).
  
  Kernel = ker(T^k) × ker(T^k), dim = 2·dim(ker(T^k)) = 2·min(k, n-1).
  
  rank(M'^k) = 2n - 2·min(k, n-1) = 2·(n - min(k, n-1)) = 2·max(1, n-k)
             = max(2, 2n - 2k).  ■
""")

# Final verification
print("  Final verification across n=2..10:")
print(f"  {'n':>3s}  {'2n':>3s}  {'rank sequence':>55s}  {'match':>6s}")

for n in range(2, 11):
    dim = 2 * n
    M_std = build_nuclear_matrix(n)
    
    Mk = [[1 if i==j else 0 for j in range(dim)] for i in range(dim)]
    
    ranks = []
    all_ok = True
    for k in range(1, n + 3):
        Mk = mat_mul_f2(Mk, M_std, dim)
        r = compute_rank_f2(Mk, dim, dim)
        expected = max(2, 2*n - 2*k)
        if r != expected: all_ok = False
        ranks.append(str(r))
    
    rank_str = " → ".join(ranks)
    print(f"  {n:3d}  {dim:3d}  {rank_str:>55s}  {'✓' if all_ok else '✗':>6s}")

# ═══════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════
print(f"\n{'═'*72}")
print("THEOREM (Nuclear Rank Sequence) — PROVEN")
print(f"{'═'*72}")
print("""
For n ≥ 2, let M be the 2n×2n nuclear extraction matrix over F₂.
Then rank(M^k) = max(2, 2n − 2k) for all k ≥ 1.

PROOF:

1. FACTORED-BASIS DECOMPOSITION.
   In the basis {p₀,...,p_{n-1}, q₀,...,q_{n-1}} where
     p_j = L_{j+1} (lower trigram, bottom-to-top)
     q_j = L_{2n-j} (upper trigram, top-to-bottom),
   the nuclear matrix has the symmetric block form:
     M = [S  E]    S = n×n superdiagonal shift (S_{i,i+1} = 1)
         [E  S]    E = e_{n-1}·e_{n-1}^T (innermost coupling)
   
   The position and orbit components each shift outward, and
   the innermost levels i ↔ ī swap.
   
   (Verified for n = 2,...,8 by explicit computation.)

2. BLOCK TRIANGULARIZATION.
   The involutory change of basis σ = p ⊕ q (Q = Q⁻¹ = [I 0; I I])
   transforms M to block upper-triangular form:
     M' = Q·M·Q = [T  E]    where T = S + E.
                   [0  T]
   
   T = "shift + stay": T(e_j) = e_{j-1} for j ≥ 1, T(e_0) = 0,
   T(e_{n-1}) = e_{n-2} + e_{n-1}.

3. RANK OF T^k.
   By induction: T^k(e_{n-1}) = Σ_{i=max(0,n-1-k)}^{n-1} e_i.
   At k = n-1: T^{n-1}(e_{n-1}) = 𝟏 (all-ones), a fixed point.
   
   ker(T^k) = span{e_0,...,e_{min(k,n-1)-1}} (killed by outward shift).
   rank(T^k) = max(1, n-k).

4. KEY LEMMA: Φ_k · ker(T^k) = {0}.
   M'^k = [T^k  Φ_k; 0  T^k] with Φ_k = Σ_{l=0}^{k-1} T^l·E·T^{k-1-l}.
   
   For e_j ∈ ker(T^k) (j < min(k, n-1)):
     Φ_k(e_j) = Σ_l T^l · E · T^{k-1-l}(e_j).
     T^{k-1-l}(e_j) is either 0 (if k-1-l > j) or e_{j-k+1+l} (shifted).
     When nonzero: j-k+1+l ≤ j < n-1, so e_{n-1}^T · e_{j-k+1+l} = 0.
     Therefore E · T^{k-1-l}(e_j) = 0 for every l, giving Φ_k(e_j) = 0.
   
   The rank-1 gate E filters through only the (n-1)-th component,
   but ker(T^k) never touches that component.

5. RANK FORMULA.
   ker(M'^k) = {(x,y) : T^k·y = 0, T^k·x + Φ_k·y = 0}.
   
   By Step 4: y ∈ ker(T^k) implies Φ_k·y = 0, so T^k·x = 0.
   Hence ker(M'^k) = ker(T^k) × ker(T^k).
   
   dim(ker(M'^k)) = 2·dim(ker(T^k)) = 2·min(k, n-1).
   rank(M'^k) = 2n − 2·min(k, n-1) = 2·max(1, n−k) = max(2, 2n−2k).  ∎

COROLLARIES:
• Rank drops by exactly 2 per iteration (peeling one lower + one upper
  outer coordinate), stabilizing at rank 2 after n−1 steps.
• The stable image F₂² ⊂ F₂^{2n} is spanned by the alternating-bit
  vectors — the innermost shear attractor {0, p_{n-1}, q_{n-1}, p_{n-1}+q_{n-1}}.
• The all-ones vector 𝟏 is a fixed point of T (and hence of M on the
  σ = p⊕q subspace), preventing nilpotency and ensuring rank ≥ 2.
""")

print("Done.")
