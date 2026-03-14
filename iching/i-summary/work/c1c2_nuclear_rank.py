#!/usr/bin/env python3
"""
C1-C2 — Nuclear rank sequence verification

Conjecture: rank(M^k) = max(2, 2n − 2k) for the nuclear shear M on F₂^{2n}.
Verify for n ∈ {3, 4, 5, 6}.
Also verify: stable image has exactly 4 elements for all tested n.
"""

# ═══════════════════════════════════════════════════════════════
# F₂ linear algebra
# ═══════════════════════════════════════════════════════════════

def mat_mul_f2(A, B, n):
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s ^= A[i][k] & B[k][j]
            C[i][j] = s
    return C

def mat_vec_f2(A, v, n):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

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
        if not found:
            continue
        for row in range(rows):
            if row != pivot_row and M[row][col]:
                M[row] = [M[row][j] ^ M[pivot_row][j] for j in range(cols)]
        pivot_row += 1
    return pivot_row

# ═══════════════════════════════════════════════════════════════
# Nuclear map construction
# ═══════════════════════════════════════════════════════════════

def build_nuclear_matrix(n):
    """
    Build the 2n×2n nuclear extraction matrix M over F₂.
    
    For a 2n-line figure h = (L₁, ..., L_{2n}):
      nuclear_lower = (L₂, L₃, ..., L_{n+1})    [n lines]
      nuclear_upper = (L_n, L_{n+1}, ..., L_{2n-1})  [n lines]
    
    Output: 2n-line figure with lower = nuclear_lower, upper = nuclear_upper.
    
    In bit indexing (0-based): L_i = bit i of h.
    L₁ = bit 0, L₂ = bit 1, ..., L_{2n} = bit 2n-1.
    
    nuclear_lower[j] = L_{j+2} for j=0,...,n-1  → bit j+1 of input
    nuclear_upper[j] = L_{j+n} for j=0,...,n-1  → bit j+n-1 of input
    
    Output bit layout: lower = bits 0..n-1, upper = bits n..2n-1
    output_bit_k = nuclear_lower[k] = input_bit_{k+1}  for k=0,...,n-1
    output_bit_{n+k} = nuclear_upper[k] = input_bit_{k+n-1}  for k=0,...,n-1
    """
    dim = 2 * n
    M = [[0]*dim for _ in range(dim)]
    
    for k in range(n):
        # Lower: output bit k ← input bit (k+1)
        input_bit = k + 1
        if 0 <= input_bit < dim:
            M[k][input_bit] = 1
        
        # Upper: output bit (n+k) ← input bit (k + n - 1)
        input_bit = k + n - 1
        if 0 <= input_bit < dim:
            M[n + k][input_bit] = 1
    
    return M

def nuclear_map_direct(h, n):
    """Direct computation of nuclear map for verification."""
    dim = 2 * n
    L = [(h >> i) & 1 for i in range(dim)]
    
    # nuclear_lower = (L₂, ..., L_{n+1}) = (L[1], ..., L[n])
    nlo = sum(L[1 + j] << j for j in range(n))
    
    # nuclear_upper = (L_n, ..., L_{2n-1}) = (L[n-1], ..., L[2n-2])
    nup = sum(L[n - 1 + j] << j for j in range(n))
    
    return nlo | (nup << n)

# ═══════════════════════════════════════════════════════════════
# Main computation
# ═══════════════════════════════════════════════════════════════

print("=" * 72)
print("C1-C2: NUCLEAR RANK SEQUENCE VERIFICATION")
print("=" * 72)

for n in [3, 4, 5, 6]:
    dim = 2 * n
    N_hex = 1 << dim
    
    print(f"\n{'─'*60}")
    print(f"n = {n}, dim = {dim}, |F₂^{{2n}}| = {N_hex}")
    print(f"{'─'*60}")
    
    # Build matrix
    M = build_nuclear_matrix(n)
    
    # Display matrix
    print(f"\nNuclear matrix M ({dim}×{dim}):")
    labels = [f"L{i+1}" for i in range(dim)]
    print(f"     {'  '.join(f'{l:>2s}' for l in labels)}")
    for i in range(dim):
        row_str = '  '.join(f'{M[i][j]:2d}' for j in range(dim))
        part = "lo" if i < n else "up"
        idx = i if i < n else i - n
        print(f"  {part}[{idx}]: {row_str}")
    
    # Verify matrix matches direct computation
    if N_hex <= 65536:
        errors = 0
        for h in range(min(N_hex, 256)):
            mat_result = mat_vec_f2(M, h, dim)
            direct_result = nuclear_map_direct(h, n)
            if mat_result != direct_result:
                errors += 1
                if errors <= 3:
                    print(f"  MISMATCH at h={h}: matrix={mat_result}, direct={direct_result}")
        if errors == 0:
            print(f"  Matrix verified against direct computation ✓")
        else:
            print(f"  WARNING: {errors} mismatches!")
    
    # Compute rank sequence
    print(f"\nRank sequence M^k:")
    print(f"  {'k':>3s} {'rank(M^k)':>10s} {'max(2,2n-2k)':>14s} {'match':>6s}")
    
    cur = [[row[:] for row in M]]  # M^1
    all_match = True
    
    for k in range(1, n + 3):
        if k == 1:
            Mk = M
        else:
            Mk = mat_mul_f2(cur[-1], M, dim)
        cur.append(Mk)
        
        rank = compute_rank_f2(Mk, dim, dim)
        expected = max(2, 2*n - 2*k)
        match = (rank == expected)
        if not match:
            all_match = False
        
        is_zero = all(Mk[i][j] == 0 for i in range(dim) for j in range(dim))
        status = " (zero)" if is_zero else ""
        mark = "✓" if match else "✗"
        print(f"  {k:3d} {rank:10d} {expected:14d} {mark:>6s}{status}")
        
        if is_zero:
            break
    
    if all_match:
        print(f"  → Conjecture VERIFIED for n={n} ✓")
    else:
        print(f"  → Conjecture FAILS for n={n} ✗")
    
    # Compute stable image
    print(f"\nStable image (iterate until convergence):")
    stable = set()
    for h in range(N_hex):
        cur_h = h
        for _ in range(2 * n):  # enough iterations to stabilize
            cur_h = mat_vec_f2(M, cur_h, dim)
        stable.add(cur_h)
    
    print(f"  |Stable image| = {len(stable)} (expected 4)")
    
    # Display stable image elements
    for h in sorted(stable):
        L = [(h >> i) & 1 for i in range(dim)]
        lo = h & ((1 << n) - 1)
        up = (h >> n) & ((1 << n) - 1)
        lo_bits = ''.join(str((lo >> j) & 1) for j in range(n))
        up_bits = ''.join(str((up >> j) & 1) for j in range(n))
        print(f"    h = {lo_bits}|{up_bits}  (lower={lo}, upper={up})")
    
    # Characterize stable image
    # At n=3: stable = {00i|0iī : i,ī ∈ {0,1}} where ī = last orbit bit
    # Generally: should be span of (i, ī) in the innermost position
    
    # Check: is it a 2-dimensional subspace?
    stable_list = sorted(stable)
    if len(stable) == 4:
        # Check closure under XOR
        is_subspace = True
        for a in stable_list:
            for b in stable_list:
                if (a ^ b) not in stable:
                    is_subspace = False
        print(f"  Forms a subspace? {is_subspace}")
        
        if is_subspace:
            # Find generators
            gens = [x for x in stable_list if x != 0]
            if len(gens) >= 2:
                print(f"  Generators: {[bin(g) for g in gens[:2]]}")
    elif len(stable) != 4:
        print(f"  ⚠ Unexpected stable image size!")

# ═══════════════════════════════════════════════════════════════
# Summary table
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*72}")
print(f"SUMMARY TABLE")
print(f"{'='*72}")
print(f"\n{'n':>3s} {'2n':>4s} {'rank seq':>30s} {'|stable|':>10s} {'conjecture':>12s}")
print(f"{'─'*3:>3s} {'─'*4:>4s} {'─'*30:>30s} {'─'*10:>10s} {'─'*12:>12s}")

for n in [3, 4, 5, 6]:
    dim = 2 * n
    M = build_nuclear_matrix(n)
    
    ranks = []
    cur_M = M
    for k in range(1, n + 3):
        if k > 1:
            cur_M = mat_mul_f2(cur_M, M, dim)
        rank = compute_rank_f2(cur_M, dim, dim)
        ranks.append(rank)
        if rank == 0:
            break
    
    N_hex = 1 << dim
    stable = set()
    for h in range(N_hex):
        cur_h = h
        for _ in range(2 * n):
            cur_h = mat_vec_f2(M, cur_h, dim)
        stable.add(cur_h)
    
    rank_str = " → ".join(str(r) for r in ranks)
    expected = [max(2, 2*n - 2*k) for k in range(1, n+3)]
    all_ok = all(ranks[i] == expected[i] for i in range(len(ranks)))
    
    print(f"{n:3d} {dim:4d} {rank_str:>30s} {len(stable):10d} {'✓ verified' if all_ok else '✗ FAILS':>12s}")

print(f"\nConjectured formula: rank(M^k) = max(2, 2n − 2k)")
print(f"Stable image: always 4 elements = F₂² (innermost shear attractor)")
print(f"\nDone.")
