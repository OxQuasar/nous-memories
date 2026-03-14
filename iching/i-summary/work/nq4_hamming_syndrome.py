#!/usr/bin/env python3
"""
NQ4 — Hamming syndrome structure at (4,13)

At n=4, p=13:
- 8 complement pairs, Frame = {0,15}
- 7 non-Frame pairs → F₂³ quotient → 7 points of PG(2,F₂) = Fano plane
- Kernel = {g(x) = x + λ(x)·1111} with λ(1111)=0 → 8 elements → (Z₂)³
- Orientation vector v ∈ (Z₂)⁷: v_j = 0 if f(x_j) ≤ 6, else v_j = 1
- Hamming parity-check H (3×7): columns = 7 nonzero vectors of F₂³
- Syndrome s = Hv mod 2 ∈ F₂³

Key test: within each full orbit (Kernel × Aut(Z₁₃), size 96),
how many distinct syndromes appear?
"""

import sys
from collections import Counter, defaultdict
from itertools import product as iterproduct, permutations

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

def mat_identity(n):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def mat_eq(A, B, n):
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))

# ═══════════════════════════════════════════════════════════════
# Setup
# ═══════════════════════════════════════════════════════════════

n, p = 4, 13
N = 1 << n            # 16
all_ones = N - 1      # 15
num_neg = (p - 1) // 2  # 6

# Complement pairs: {x, x⊕1111}
comp_pairs = []
seen = set()
for x in range(N):
    if x not in seen:
        cx = x ^ all_ones
        seen.add(x); seen.add(cx)
        comp_pairs.append((min(x, cx), max(x, cx)))
# [(0,15), (1,14), (2,13), (3,12), (4,11), (5,10), (6,9), (7,8)]

# Non-Frame pairs: indices 1..7 in comp_pairs
non_frame_reps = [comp_pairs[i][0] for i in range(1, 8)]  # [1,2,3,4,5,6,7]

print("=" * 72)
print("NQ4: HAMMING SYNDROME STRUCTURE AT (4,13)")
print("=" * 72)
print(f"\nComplement pairs: {comp_pairs}")
print(f"Non-Frame pair reps: {non_frame_reps}")

# ═══════════════════════════════════════════════════════════════
# Step 1: Map non-Frame pairs to F₂³ quotient vectors
# ═══════════════════════════════════════════════════════════════

# The quotient F₂⁴/⟨1111⟩ has dimension 3. 
# Project by dropping one coordinate (say bit 3, since 1111 has all bits).
# Equivalently: the 7 non-Frame reps {1,..,7} ARE the 7 nonzero vectors of F₂³
# when we view them as 3-bit vectors (since they have bit patterns 001..111,
# which is exactly the 7 nonzero elements of F₂³ embedded in the first 3 bits).
# But wait — reps 1..7 are 4-bit vectors. The quotient F₂⁴/⟨1111⟩ maps
# x → x mod ⟨1111⟩. Under this map, x and x⊕1111 go to the same coset.
# For reps 1..7 (which are < 8), their image in F₂³ is just their 3 low bits,
# since the high bit (bit 3) is 0 for all of them.

# Verify: each non-frame rep has bit 3 = 0 (i.e., rep < 8)
assert all(r < 8 for r in non_frame_reps)

# The Fano plane points are the 7 nonzero vectors of F₂³
# Non-Frame rep j (j=1..7) maps to the vector j ∈ {001, 010, ..., 111} in F₂³
# This is EXACTLY the column space of the Hamming parity-check matrix

# Step 2: Construct Hamming parity-check matrix H (3×7)
# Columns = the 7 nonzero vectors of F₂³, ordered by pair index j=1..7
# Column j = binary representation of j (3 bits)

H = [[0]*7 for _ in range(3)]
for j_idx in range(7):
    j_val = non_frame_reps[j_idx]  # 1,2,3,4,5,6,7
    for bit in range(3):
        H[bit][j_idx] = (j_val >> bit) & 1

print("\nHamming parity-check matrix H (3×7):")
for row in range(3):
    print(f"  [{' '.join(str(H[row][j]) for j in range(7))}]")
print(f"  Columns correspond to pair reps: {non_frame_reps}")

# Verify: this is the standard [7,4,3] Hamming code parity-check matrix
# (columns = all nonzero 3-bit vectors)
print(f"  Columns as integers: {non_frame_reps} = 1..7 ✓")

# ═══════════════════════════════════════════════════════════════
# Step 3: Enumerate surjections for one type distribution
# ═══════════════════════════════════════════════════════════════

# Type distribution: (2, 0, 1, 1, 1, 1, 1, 2) — the canonical Orbit-C type
type_dist = (2, 0, 1, 1, 1, 1, 1, 2)
neg_pairs = [(k, p-k) for k in range(1, num_neg+1)]

print(f"\nType distribution: {type_dist}")
print(f"Negation pairs in Z₁₃: {neg_pairs}")

type0_pairs = [i for i in range(8) if type_dist[i] == 0]  # [1]
type1_pairs = [i for i in range(8) if type_dist[i] == 1]  # [2,3,4,5,6]
type2_pairs = [i for i in range(8) if type_dist[i] == 2]  # [0,7]

print(f"Enumerating surjections...")
surjections = []
pair_reps = [min(cp) for cp in comp_pairs]

for shared_neg_idx in range(num_neg):
    shared_neg = neg_pairs[shared_neg_idx]
    remaining_neg = [neg_pairs[j] for j in range(num_neg) if j != shared_neg_idx]
    for assignment in permutations(remaining_neg):
        for t2_orient in iterproduct([0,1], repeat=len(type2_pairs)):
            for t1_orient in iterproduct([0,1], repeat=len(type1_pairs)):
                vals = [None]*8
                for pi in type0_pairs:
                    vals[pi] = 0
                for k, pi in enumerate(type2_pairs):
                    vals[pi] = shared_neg[t2_orient[k]]
                for k, pi in enumerate(type1_pairs):
                    vals[pi] = assignment[k][t1_orient[k]]
                fmap = {}
                for i, (a, b) in enumerate(comp_pairs):
                    fmap[a] = vals[i]
                    fmap[b] = (-vals[i]) % p
                if len(set(fmap.values())) == p:
                    surjections.append(tuple(fmap[x] for x in range(N)))

surj_set = set(surjections)
surjections = list(surj_set)
print(f"Surjections: {len(surjections)} (expected 92160)")

# ═══════════════════════════════════════════════════════════════
# Step 4: Compute orientation vectors and syndromes
# ═══════════════════════════════════════════════════════════════

print(f"\nComputing orientation vectors and syndromes...")

def orientation_vector(f_tuple):
    """For each non-Frame pair j (j=1..7), v_j = 0 if f(rep_j) ≤ 6, else 1."""
    v = []
    for j_idx in range(7):
        rep = non_frame_reps[j_idx]
        val = f_tuple[rep]
        v.append(0 if val <= (p-1)//2 else 1)  # ≤ 6 → 0, ≥ 7 → 1
    return tuple(v)

def syndrome(v):
    """Compute Hv mod 2."""
    s = [0]*3
    for bit in range(3):
        for j in range(7):
            s[bit] ^= H[bit][j] & v[j]
    return tuple(s)

# Compute syndromes for all surjections
syndromes = {}
syndrome_counts = Counter()
for f in surjections:
    v = orientation_vector(f)
    s = syndrome(v)
    syndromes[f] = (v, s)
    syndrome_counts[s] += 1

print(f"\nSyndrome distribution across all {len(surjections)} surjections:")
for s_val, count in sorted(syndrome_counts.items()):
    s_int = s_val[0] + 2*s_val[1] + 4*s_val[2]
    print(f"  s = {s_val} (={s_int}): {count} surjections ({count/len(surjections)*100:.1f}%)")

# Check: 8 syndromes × 11520 per syndrome = 92160
expected_per = len(surjections) // 8
print(f"\nExpected if uniform: {expected_per} per syndrome")
is_uniform = all(c == expected_per for c in syndrome_counts.values())
print(f"Uniform across 8 syndromes? {is_uniform}")

# ═══════════════════════════════════════════════════════════════
# Step 5: Build the kernel and compute orbits
# ═══════════════════════════════════════════════════════════════

print(f"\nBuilding kernel (Stab(1111) pair-fixing subgroup)...")

kernel = []
for bits in range(16):  # (λ₀, λ₁, λ₂, λ₃)
    lam = [(bits >> i) & 1 for i in range(4)]
    if lam[0] ^ lam[1] ^ lam[2] ^ lam[3] != 0:
        continue
    g_matrix = [[0]*4 for _ in range(4)]
    for col in range(4):
        e_col = 1 << col
        lam_e = lam[col]
        img = e_col ^ (lam_e * all_ones)
        for row in range(4):
            g_matrix[row][col] = (img >> row) & 1
    kernel.append(g_matrix)

print(f"|Kernel| = {len(kernel)}")

kernel_invs = [mat_inv_f2(g, 4) for g in kernel]
aut_zp = list(range(1, p))

# ═══════════════════════════════════════════════════════════════
# Step 6: Compute orbits and check syndrome constancy within orbits
# ═══════════════════════════════════════════════════════════════

print(f"\nComputing orbits and checking syndrome constancy...")

# Use union-find
parent = {f: f for f in surjections}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb

for f in surjections:
    for g_inv in kernel_invs:
        for alpha in aut_zp:
            t = tuple((alpha * f[mat_vec_f2(g_inv, x, 4)]) % p for x in range(N))
            if t in surj_set:
                union(f, t)

# Group into orbits
orbit_map = defaultdict(list)
for f in surjections:
    orbit_map[find(f)].append(f)

orbits = list(orbit_map.values())
print(f"Number of orbits: {len(orbits)} (expected 960)")
orbit_sizes = Counter(len(o) for o in orbits)
print(f"Orbit size distribution: {sorted(orbit_sizes.items())}")

# ═══════════════════════════════════════════════════════════════
# Step 7: KEY TEST — syndrome counts within each orbit
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*72}")
print(f"KEY TEST: SYNDROME DISTRIBUTION WITHIN ORBITS")
print(f"{'='*72}")

within_orbit_syndrome_counts = Counter()  # maps (num_distinct_syndromes) → orbit_count

orbit_syndrome_details = []
for i, orbit in enumerate(orbits):
    orbit_syndromes = set()
    orbit_orientations = set()
    for f in orbit:
        v, s = syndromes[f]
        orbit_syndromes.add(s)
        orbit_orientations.add(v)
    n_syn = len(orbit_syndromes)
    within_orbit_syndrome_counts[n_syn] += 1
    orbit_syndrome_details.append((n_syn, orbit_syndromes, orbit_orientations))

print(f"\nDistribution of distinct syndromes per orbit:")
for n_syn, count in sorted(within_orbit_syndrome_counts.items()):
    print(f"  {n_syn} distinct syndrome(s): {count} orbits")

if 1 in within_orbit_syndrome_counts and within_orbit_syndrome_counts[1] == len(orbits):
    print(f"\n✓ CLEAN PRODUCT DECOMPOSITION CONFIRMED")
    print(f"  Every orbit has exactly 1 syndrome → syndromes classify orbits")
    print(f"  960 orbits = 8 syndrome classes × 120 orbits per class")
    
    # Verify 120 per class
    syndrome_to_orbits = defaultdict(int)
    for i, orbit in enumerate(orbits):
        s = orbit_syndrome_details[i][1].pop()  # the unique syndrome
        orbit_syndrome_details[i][1].add(s)  # put it back
        syndrome_to_orbits[s] += 1
    
    print(f"\n  Orbits per syndrome class:")
    for s_val, count in sorted(syndrome_to_orbits.items()):
        s_int = s_val[0] + 2*s_val[1] + 4*s_val[2]
        print(f"    s={s_val} (={s_int}): {count} orbits")
else:
    print(f"\n✗ Syndromes vary within orbits — no clean product")
    print(f"  Investigating the Aut(Z₁₃) action on syndromes...")
    
    # Separate kernel and Aut(Z₁₃) actions
    # First: does the KERNEL preserve syndromes?
    print(f"\n  Testing kernel action on syndromes...")
    kernel_preserves = True
    for f in surjections[:1000]:
        v_f, s_f = syndromes[f]
        for g_inv in kernel_invs:
            t = tuple((1 * f[mat_vec_f2(g_inv, x, 4)]) % p for x in range(N))  # α=1
            if t in surj_set:
                v_t, s_t = syndromes[t]
                if s_t != s_f:
                    kernel_preserves = False
                    break
        if not kernel_preserves:
            break
    
    print(f"  Kernel preserves syndromes? {kernel_preserves}")
    
    # Test: does α (negation, α=p-1=12) preserve syndromes?
    print(f"\n  Testing negation (α=12) on syndromes...")
    negation_preserves = True
    for f in surjections[:1000]:
        v_f, s_f = syndromes[f]
        t = tuple((12 * f[x]) % p for x in range(N))  # negation, no domain change
        if t in surj_set:
            v_t, s_t = syndromes[t]
            if s_t != s_f:
                negation_preserves = False
                # Show example
                print(f"    Example: f→s={s_f}, neg(f)→s={s_t}")
                print(f"    v_f={v_f}, v_neg={syndromes[t][0]}")
                break
    
    print(f"  Negation preserves syndromes? {negation_preserves}")
    
    # Test: what does multiplication by a generator of Aut(Z₁₃) do?
    # Aut(Z₁₃) = Z₁₂. A generator is 2 (since 2 has order 12 mod 13).
    print(f"\n  Testing α=2 (generator of Aut(Z₁₃)) on syndromes...")
    alpha = 2
    syndrome_transition = defaultdict(Counter)
    for f in surjections[:5000]:
        v_f, s_f = syndromes[f]
        t = tuple((alpha * f[x]) % p for x in range(N))
        if t in surj_set:
            v_t, s_t = syndromes[t]
            syndrome_transition[s_f][s_t] += 1
    
    print(f"  Syndrome transitions under α=2:")
    for s_from in sorted(syndrome_transition.keys()):
        targets = syndrome_transition[s_from]
        s_from_int = s_from[0] + 2*s_from[1] + 4*s_from[2]
        parts = []
        for s_to, cnt in sorted(targets.items()):
            s_to_int = s_to[0] + 2*s_to[1] + 4*s_to[2]
            parts.append(f"{s_to_int}({cnt})")
        print(f"    s={s_from_int} → {', '.join(parts)}")
    
    # Check: what is the permutation representation of Aut(Z₁₃) on F₂³?
    print(f"\n  Full Aut(Z₁₃) permutation on 8 syndromes:")
    for alpha in [2, 3, 4, 12]:
        syn_perm = {}
        for f in surjections[:5000]:
            v_f, s_f = syndromes[f]
            t = tuple((alpha * f[x]) % p for x in range(N))
            if t in surj_set:
                v_t, s_t = syndromes[t]
                if s_f not in syn_perm:
                    syn_perm[s_f] = s_t
        perm_str = []
        for s_from in sorted(syn_perm.keys()):
            s_from_int = s_from[0] + 2*s_from[1] + 4*s_from[2]
            s_to_int = syn_perm[s_from][0] + 2*syn_perm[s_from][1] + 4*syn_perm[s_from][2]
            perm_str.append(f"{s_from_int}→{s_to_int}")
        print(f"    α={alpha}: {', '.join(perm_str)}")

    # Detailed orbit analysis: how many syndromes per orbit?
    print(f"\n  Detailed within-orbit syndrome analysis:")
    # Show a few example orbits
    for i in range(min(5, len(orbits))):
        n_syn, syns, oris = orbit_syndrome_details[i]
        print(f"    Orbit {i}: {n_syn} syndromes: {sorted([s[0]+2*s[1]+4*s[2] for s in syns])}")
        print(f"              {len(oris)} orientation vectors")

    # What is the orbit structure of syndromes under Aut(Z₁₃)?
    # I.e., does the Aut(Z₁₃) action partition the 8 syndromes into orbits?
    print(f"\n  Aut(Z₁₃) orbit structure on 8 syndromes:")
    # Build the full permutation for α=2 (generator)
    full_syn_perm_2 = {}
    checked = 0
    for f in surjections:
        if len(full_syn_perm_2) == 8:
            break
        v_f, s_f = syndromes[f]
        if s_f in full_syn_perm_2:
            continue
        t = tuple((2 * f[x]) % p for x in range(N))
        if t in surj_set:
            v_t, s_t = syndromes[t]
            full_syn_perm_2[s_f] = s_t
    
    # Find orbits of this permutation
    syn_visited = set()
    syn_orbits = []
    for s in full_syn_perm_2:
        if s in syn_visited:
            continue
        orb = []
        cur = s
        while cur not in syn_visited:
            syn_visited.add(cur)
            orb.append(cur)
            cur = full_syn_perm_2.get(cur, cur)
        syn_orbits.append(orb)
    
    for i, orb in enumerate(syn_orbits):
        labels = [s[0]+2*s[1]+4*s[2] for s in orb]
        print(f"    Orbit {i}: {labels} (size {len(orb)})")

# ═══════════════════════════════════════════════════════════════
# Step 8: Orientation vector statistics
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*72}")
print(f"ORIENTATION VECTOR ANALYSIS")
print(f"{'='*72}")

# How many distinct orientation vectors?
all_orientations = Counter()
for f in surjections:
    v, _ = syndromes[f]
    all_orientations[v] += 1

print(f"\nDistinct orientation vectors: {len(all_orientations)} out of 128 possible")
print(f"Weight distribution of orientation vectors:")
weight_dist = Counter()
for v, count in all_orientations.items():
    w = sum(v)
    weight_dist[w] += count

for w in sorted(weight_dist.keys()):
    print(f"  weight {w}: {weight_dist[w]} surjections")

# Check if orientation vectors form a coset of the Hamming code RM(1,3)
# RM(1,3) has 2⁴=16 codewords. A coset has 16 vectors too.
# With 8 syndrome classes, we should see 8 cosets of 16 vectors each
# Total distinct vectors = 128 (all vectors!) if all cosets appear,
# or 16 if only one coset
print(f"\nOrientation vectors form {'all 8 cosets' if len(all_orientations)==128 else f'{len(all_orientations)} vectors'} of RM(1,3)")

# Count vectors per syndrome (=coset)
vecs_per_syndrome = defaultdict(set)
for f in surjections:
    v, s = syndromes[f]
    vecs_per_syndrome[s].add(v)

print(f"\nOrientation vectors per syndrome class:")
for s_val in sorted(vecs_per_syndrome.keys()):
    s_int = s_val[0] + 2*s_val[1] + 4*s_val[2]
    vecs = vecs_per_syndrome[s_val]
    print(f"  s={s_int}: {len(vecs)} distinct orientation vectors")

print(f"\nDone.")
