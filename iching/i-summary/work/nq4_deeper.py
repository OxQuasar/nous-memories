#!/usr/bin/env python3
"""
NQ4 deeper analysis: understand WHY 6 syndromes per orbit.

The key mechanisms:
1. Kernel action: does it preserve or permute syndromes?
2. Aut(Z₁₃) action: what permutation on syndromes?
3. Type-0 constraint: v[0] = 0 always (pair 1 maps to 0).
"""

from collections import Counter, defaultdict
from itertools import product as iterproduct, permutations

def mat_vec_f2(A, v, n):
    result = 0
    for i in range(n):
        s = 0
        for j in range(n):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

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

n, p = 4, 13
N = 1 << n
all_ones = N - 1

comp_pairs = [(0,15), (1,14), (2,13), (3,12), (4,11), (5,10), (6,9), (7,8)]
non_frame_reps = [1, 2, 3, 4, 5, 6, 7]

H = [[0]*7 for _ in range(3)]
for j_idx in range(7):
    j_val = non_frame_reps[j_idx]
    for bit in range(3):
        H[bit][j_idx] = (j_val >> bit) & 1

def orientation_vector(f_tuple):
    return tuple(0 if f_tuple[non_frame_reps[j]] <= 6 else 1 for j in range(7))

def syndrome(v):
    return tuple(sum(H[bit][j] & v[j] for j in range(7)) % 2 for bit in range(3))

def syn_int(s): return s[0] + 2*s[1] + 4*s[2]

# Build kernel
kernel_matrices = []
kernel_lambdas = []
for bits in range(16):
    lam = [(bits >> i) & 1 for i in range(4)]
    if lam[0] ^ lam[1] ^ lam[2] ^ lam[3] != 0: continue
    g_matrix = [[0]*4 for _ in range(4)]
    for col in range(4):
        e_col = 1 << col
        img = e_col ^ (lam[col] * all_ones)
        for row in range(4):
            g_matrix[row][col] = (img >> row) & 1
    kernel_matrices.append(g_matrix)
    kernel_lambdas.append(lam)

print("=" * 72)
print("NQ4 DEEPER: UNDERSTANDING THE 6-SYNDROME STRUCTURE")
print("=" * 72)

# ═══════════════════════════════════════════════════════════════
# Analysis 1: What does the kernel do to orientation vectors?
# ═══════════════════════════════════════════════════════════════

print("\n--- KERNEL ACTION ON ORIENTATION VECTORS ---")
print("\nKernel elements (λ values, and their action on non-Frame pair reps):")

for i, (g, lam) in enumerate(zip(kernel_matrices, kernel_lambdas)):
    g_inv = mat_inv_f2(g, 4)
    # For each non-Frame rep x_j, compute g⁻¹(x_j)
    permuted_reps = []
    for j in range(7):
        xj = non_frame_reps[j]
        gx = mat_vec_f2(g_inv, xj, 4)
        permuted_reps.append(gx)
    
    # How does this affect orientation?
    # Original: v_j = 0 if f(x_j) ≤ 6
    # After kernel g: f ∘ g⁻¹, so new v_j = 0 if f(g⁻¹(x_j)) ≤ 6
    # g⁻¹(x_j) = x_j ⊕ λ(x_j)·1111
    # So new value at pair j: f(g⁻¹(x_j))
    # If λ(x_j) = 0: g⁻¹(x_j) = x_j → same pair, same value → v_j unchanged
    # If λ(x_j) = 1: g⁻¹(x_j) = x_j ⊕ 1111 = complement → value flips (neg mod p)
    #   → v_j flips from 0↔1
    
    flip_mask = []
    for j in range(7):
        xj = non_frame_reps[j]
        # λ(xj) = ∑ lam[i] * bit_i(xj) mod 2
        lam_xj = sum(lam[k] * ((xj >> k) & 1) for k in range(4)) % 2
        flip_mask.append(lam_xj)
    
    flip_vec = tuple(flip_mask)
    s_flip = syndrome(flip_vec)
    lam_str = ''.join(str(l) for l in lam)
    print(f"  λ={lam_str}: flip={flip_vec}, syndrome_of_flip={syn_int(s_flip)}")

# ═══════════════════════════════════════════════════════════════
# Analysis 2: The kernel swaps are Hamming codewords PLUS the
# constraint that v[0] can only be 0 (Type-0 pair always maps to 0)
# ═══════════════════════════════════════════════════════════════

print("\n--- UNDERSTANDING THE MISSING PAIR ---")
print("\nFor the type distribution (2,0,1,1,1,1,1,2):")
print("  Pair 1 has type 0 → both reps map to 0 → v[0] = 0 ALWAYS")
print("  This constrains orientation vectors to have v[0] = 0")
print(f"  → Only 64 of 128 possible vectors, in 8 cosets of 8 vectors each")

print("\nKernel flip masks and their syndromes:")
print("  The kernel generates 8 flip patterns. Applied to a base v,")
print("  the syndrome changes by: s(v ⊕ flip) = s(v) ⊕ s(flip)")
print("  Since flip is in the span of kernel actions.")

# Compute: which syndromes does {s(flip)} generate?
kernel_syndromes = set()
for i, lam in enumerate(kernel_lambdas):
    flip = tuple(sum(lam[k] * ((non_frame_reps[j] >> k) & 1) for k in range(4)) % 2 for j in range(7))
    s = syndrome(flip)
    kernel_syndromes.add(s)

print(f"  Kernel flip syndromes: {sorted([syn_int(s) for s in kernel_syndromes])}")
print(f"  → The kernel generates syndrome shifts ∈ {sorted([syn_int(s) for s in kernel_syndromes])}")

# But wait: only the flips that preserve v[0]=0 are accessible.
# If flip[0]=0: v'[0] = v[0] ⊕ 0 = 0 ✓
# If flip[0]=1: v'[0] = v[0] ⊕ 1 = 1 ✗ — this BREAKS the constraint!

print("\n  But v[0] must remain 0 (Type-0 constraint).")
print("  Kernel elements with flip[0]=1 send v outside the constraint,")
print("  but the corresponding surjection has pair 1 values swapped.")
print("  Since pair 1 has type 0 (both → 0), swapping gives 0↔(−0 mod 13)=0↔0.")
print("  So pair 1 is UNCHANGED, but the orientation threshold changes!")
print("  Specifically: f(1) = 0 always, and 0 ≤ 6, so v[0] = 0 always.")
print("  After kernel: (f∘g⁻¹)(1) = f(1⊕1111) = f(14) = (−f(1)) mod 13 = 0.")
print("  So v[0] stays 0 regardless? Let me check...")

print("\n  Actually: pair 1 has type 0, meaning the pair is assigned value 0.")
print("  f(1) = 0, f(14) = (−0) mod 13 = 0. Both are 0.")
print("  After kernel with λ(1)=1: (f∘g⁻¹)(1) = f(14) = 0. So v[0] = 0 still.")
print("  ⇒ Type-0 pairs CANNOT contribute to orientation flips!")
print("  ⇒ The effective flip at position 0 is ALWAYS 0, regardless of λ(1).")
print()

# Re-examine: the flip from kernel element g with functional λ
# For the Type-0 pair (pair index 1, rep=1):
#   original: f(1) = 0 → v[0] = 0
#   after g:  f(g⁻¹(1)) = f(1 ⊕ λ(1)·1111)
#     if λ(1)=0: f(1) = 0 → v[0] = 0  
#     if λ(1)=1: f(14) = 0 → v[0] = 0  (since pair 1 is type 0, both values are 0)
# So v[0] = 0 ALWAYS. The effective flip at position 0 is 0 regardless of λ(1).

# The effective flip vector is: 
# flip_eff[j] = flip[j] if j != 0, and flip_eff[0] = 0 always
print("Effective flip vectors (accounting for Type-0 constraint):")

eff_kernel_syndromes = set()
for i, lam in enumerate(kernel_lambdas):
    flip_raw = [sum(lam[k] * ((non_frame_reps[j] >> k) & 1) for k in range(4)) % 2 for j in range(7)]
    flip_eff = [0] + flip_raw[1:]  # position 0 forced to 0
    s_raw = syndrome(tuple(flip_raw))
    s_eff = syndrome(tuple(flip_eff))
    lam_str = ''.join(str(l) for l in lam)
    print(f"  λ={lam_str}: raw_flip={tuple(flip_raw)} s={syn_int(s_raw)}, eff_flip={tuple(flip_eff)} s={syn_int(s_eff)}")
    eff_kernel_syndromes.add(syn_int(s_eff))

print(f"\n  Effective kernel syndrome shifts: {sorted(eff_kernel_syndromes)}")
print(f"  → The kernel generates shifts in {{{', '.join(str(s) for s in sorted(eff_kernel_syndromes))}}}")

if len(eff_kernel_syndromes) == 2:
    a, b = sorted(eff_kernel_syndromes)
    print(f"  → This is {{0, {b}}} = Z₂ acting on syndromes")
    print(f"  → Syndromes pair as: {{s, s ⊕ {b}}}")
    for s in range(8):
        partner = s ^ b
        if s < partner:
            print(f"    {{{s}, {partner}}}")

# ═══════════════════════════════════════════════════════════════
# Analysis 3: Aut(Z₁₃) action — what happens to syndromes?
# ═══════════════════════════════════════════════════════════════

print("\n--- Aut(Z₁₃) ACTION ON SYNDROMES ---")
print("\nNegation (α=12) acts as:")
print("  f(x) → (−f(x)) mod 13 = (13−f(x)) mod 13")
print("  This maps val ≤ 6 → val ≥ 7 (except val=0 stays 0)")
print("  For Type-1 pairs: v_j flips")
print("  For Type-0 pairs: val=0 → 0, so v stays 0")
print("  For Type-2 pairs: one of {k, 13-k} maps to ≤6, the other to ≥7.")
print("    Negation swaps them, so v_j flips.")

print("\nSo negation flips ALL non-Type-0 positions.")
print("Flip pattern for negation:")
type_dist = (2, 0, 1, 1, 1, 1, 1, 2)
neg_flip = []
for j in range(7):
    pair_idx = j + 1  # pairs 1..7 map to non-frame pair j=0..6
    t = type_dist[pair_idx]
    if t == 0:
        neg_flip.append(0)
    else:
        neg_flip.append(1)
neg_flip_tup = tuple(neg_flip)
neg_syndrome = syndrome(neg_flip_tup)
print(f"  neg_flip = {neg_flip_tup}")
print(f"  syndrome(neg_flip) = {syn_int(neg_syndrome)}")
print(f"  Negation shifts syndrome by ⊕ {syn_int(neg_syndrome)}")

# Combined: kernel shift is ⊕ X, negation shift is ⊕ Y
# Together they generate the subgroup ⟨X, Y⟩ ⊆ F₂³

# What about α=2 and α=3?
print(f"\n  For cube root α=2:")
print(f"  α=2 permutes {{1,...,12}} mod 13. The negation pairs {{k,13-k}} may be preserved or swapped.")
print(f"  This is more complex — it depends on the assignment structure.")

# ═══════════════════════════════════════════════════════════════
# Analysis 4: The 6-syndrome result decomposed
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 72)
print("DECOMPOSITION OF 960 ORBITS")
print("=" * 72)

print(f"""
Within each full orbit (size 96 = 8 kernel × 12 Aut(Z₁₃)):
- 8 kernel elements generate syndrome shifts ∈ {{0, 1}} (Z₂)
- Negation (part of Aut(Z₁₃)) generates shift ⊕ {syn_int(neg_syndrome)}
- Together these give ⟨1, {syn_int(neg_syndrome)}⟩ = {{0, 1, {syn_int(neg_syndrome)}, {1 ^ syn_int(neg_syndrome)}}} ⊆ F₂³

Wait — negation syndrome shift depends on type distribution.
For type_dist = (2, 0, 1, 1, 1, 1, 1, 2):
  Type-0 pair: pair 1 (position 0)
  neg_flip[0] = 0 (Type-0 → doesn't flip)
  neg_flip[j] = 1 for j=1..6 (Type-1 and Type-2 → flip)
  neg_flip = {neg_flip_tup}
  syndrome = {syn_int(neg_syndrome)}

Combined Z₂ shifts accessible: {{0, 1}} ⊕ {{0, {syn_int(neg_syndrome)}}} = ... 
""")

# Let me compute properly
from_kernel = {0, 1}  # syndrome shifts from kernel
from_negation = {0, syn_int(neg_syndrome)}
combined = set()
for a in from_kernel:
    for b in from_negation:
        combined.add(a ^ b)
print(f"  Kernel shifts: {from_kernel}")
print(f"  Negation shifts: {from_negation}")
print(f"  Combined shifts: {sorted(combined)}")
print(f"  → {len(combined)} accessible syndromes from any base → missing {8 - len(combined)}")

# Number of orbits of the shift group on F₂³
shift_orbits = []
visited = set()
for s in range(8):
    if s in visited: continue
    orbit = set()
    for d in combined:
        orbit.add(s ^ d)
    visited |= orbit
    shift_orbits.append(sorted(orbit))

print(f"\n  Syndrome orbits under combined shifts:")
for orb in shift_orbits:
    print(f"    {orb}")
print(f"  → {len(shift_orbits)} orbit classes of syndromes")
print(f"  → 960 / {len(shift_orbits)} = {960 // len(shift_orbits)} orbits per syndrome class")
print(f"     if shift action fully accounts for within-orbit variation.")

# But wait: the actual data shows 6 syndromes per orbit, not |combined|.
# This means other Aut(Z₁₃) elements also shift syndromes!
# The FULL orbit uses ALL of Aut(Z₁₃), not just negation.

print(f"\n  Note: actual observation = 6 syndromes per orbit")
print(f"  Pure kernel+negation gives {len(combined)} shifts")
print(f"  The remaining Aut(Z₁₃) elements (α=2,3,...,11) contribute more shifts")

# The missing pair is always one of {(0,1), (2,3), (4,5), (6,7)}
# These are cosets of ⟨1⟩ = {0,1} in F₂³  
# So: the kernel shift ⟨1⟩ pairs syndromes. The Aut(Z₁₃) visits 3 of the 4 cosets.
print(f"\n  The 4 Z₂ pairs: {{0,1}}, {{2,3}}, {{4,5}}, {{6,7}}")
print(f"  Each orbit visits 3 of 4 pairs → misses exactly 1 pair")
print(f"  960 = 4 (missing-pair class) × 240 (orbits per class)")

print(f"\n  The orbit structure is:")
print(f"    Kernel: pairs syndromes as {{s, s⊕1}} → 4 pairs")
print(f"    Aut(Z₁₃): visits 3 of 4 pairs → determines which pair is missing")
print(f"    Assignment: 240 = 120 × 2 sub-orbits within each missing-pair class")

print(f"\n  This means the correct decomposition is:")
print(f"    960 = 4 (syndrome pair classes) × 240 (assignment-like orbits)")
print(f"    NOT 8 × 120 as hoped.")

print(f"\nDone.")
