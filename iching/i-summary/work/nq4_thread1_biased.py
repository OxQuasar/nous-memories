#!/usr/bin/env python3
"""
NQ4 Thread 1: Internal geometry of the 144 biased orbits.

Within each missing-pair class of 240 orbits:
  96 "uniform" orbits (16 surjections per syndrome)
  144 "biased" orbits  (8,8,8,8,32,32 per syndrome)

Questions:
1. In biased orbits, do the 2 overrepresented syndromes form a Z₂ pair?
2. Do the 144 biased orbits split as 48×3 among the 3 non-missing Z₂ pairs?
3. Does the 96/144 split correlate with the shared negation pair?
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

# ═══════════════════════════════════════════════════════════════
# Setup
# ═══════════════════════════════════════════════════════════════

n, p = 4, 13
N = 1 << n  # 16
all_ones = N - 1

comp_pairs = []
seen = set()
for x in range(N):
    if x not in seen:
        cx = x ^ all_ones
        seen.add(x); seen.add(cx)
        comp_pairs.append((min(x, cx), max(x, cx)))

non_frame_reps = [comp_pairs[i][0] for i in range(1, 8)]  # [1..7]

H = [[0]*7 for _ in range(3)]
for j_idx in range(7):
    j_val = non_frame_reps[j_idx]
    for bit in range(3):
        H[bit][j_idx] = (j_val >> bit) & 1

type_dist = (2, 0, 1, 1, 1, 1, 1, 2)
neg_pairs = [(k, p-k) for k in range(1, 7)]
type0_pairs = [i for i in range(8) if type_dist[i] == 0]
type1_pairs = [i for i in range(8) if type_dist[i] == 1]
type2_pairs = [i for i in range(8) if type_dist[i] == 2]

# ═══════════════════════════════════════════════════════════════
# Enumerate surjections
# ═══════════════════════════════════════════════════════════════

print("=" * 72)
print("NQ4 THREAD 1: BIASED ORBIT INTERNAL GEOMETRY")
print("=" * 72)

print(f"\nType distribution: {type_dist}")
print(f"Type-0 pairs (assign 0): {type0_pairs}")
print(f"Type-1 pairs (assign one neg pair): {type1_pairs}")
print(f"Type-2 pairs (share neg pair): {type2_pairs}")

print("\nEnumerating surjections...")
surjections = []
# Also track construction metadata for each surjection
surj_metadata = {}

for shared_neg_idx in range(6):
    shared_neg = neg_pairs[shared_neg_idx]
    remaining_neg = [neg_pairs[j] for j in range(6) if j != shared_neg_idx]
    for assignment in permutations(remaining_neg):
        for t2_orient in iterproduct([0,1], repeat=len(type2_pairs)):
            for t1_orient in iterproduct([0,1], repeat=len(type1_pairs)):
                vals = [None]*8
                for pi in type0_pairs: vals[pi] = 0
                for k, pi in enumerate(type2_pairs):
                    vals[pi] = shared_neg[t2_orient[k]]
                for k, pi in enumerate(type1_pairs):
                    vals[pi] = assignment[k][t1_orient[k]]
                fmap = {}
                for i, (a, b) in enumerate(comp_pairs):
                    fmap[a] = vals[i]
                    fmap[b] = (-vals[i]) % p
                if len(set(fmap.values())) == p:
                    f_tuple = tuple(fmap[x] for x in range(N))
                    surjections.append(f_tuple)
                    surj_metadata[f_tuple] = {
                        'shared_neg_idx': shared_neg_idx,
                        'shared_neg': shared_neg,
                    }

surj_set = set(surjections)
surjections = list(surj_set)
print(f"Surjections: {len(surjections)}")

# ═══════════════════════════════════════════════════════════════
# Compute syndromes
# ═══════════════════════════════════════════════════════════════

def orientation_vector(f_tuple):
    return tuple(0 if f_tuple[non_frame_reps[j]] <= 6 else 1 for j in range(7))

def syndrome(v):
    return tuple(sum(H[bit][j] & v[j] for j in range(7)) % 2 for bit in range(3))

def syn_int(s): return s[0] + 2*s[1] + 4*s[2]

syn_map = {}
for f in surjections:
    v = orientation_vector(f)
    syn_map[f] = syndrome(v)

# ═══════════════════════════════════════════════════════════════
# Compute orbits
# ═══════════════════════════════════════════════════════════════

kernel = []
for bits in range(16):
    lam = [(bits >> i) & 1 for i in range(4)]
    if lam[0] ^ lam[1] ^ lam[2] ^ lam[3] != 0: continue
    g_matrix = [[0]*4 for _ in range(4)]
    for col in range(4):
        e_col = 1 << col
        img = e_col ^ (lam[col] * all_ones)
        for row in range(4):
            g_matrix[row][col] = (img >> row) & 1
    kernel.append(g_matrix)
kernel_invs = [mat_inv_f2(g, 4) for g in kernel]
aut_zp = list(range(1, p))

print("Computing orbits...")
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

orbit_map = defaultdict(list)
for f in surjections:
    orbit_map[find(f)].append(f)
orbits = list(orbit_map.values())
print(f"Orbits: {len(orbits)}")

# ═══════════════════════════════════════════════════════════════
# Classify orbits by (missing pair, bias structure)
# ═══════════════════════════════════════════════════════════════

z2_pairs = [(0,1), (2,3), (4,5), (6,7)]

print("\n" + "=" * 72)
print("ANALYSIS 1: BIASED ORBIT OVERREPRESENTED PAIR")
print("=" * 72)

# For each orbit, compute full syndrome profile
orbit_profiles = []
for orbit in orbits:
    syn_counts = Counter(syn_int(syn_map[f]) for f in orbit)
    present = set(syn_counts.keys())
    missing = set(range(8)) - present
    missing_tup = tuple(sorted(missing))
    
    # Identify distribution type
    vals_sorted = tuple(sorted(syn_counts.values()))
    
    over_pair = None
    if vals_sorted == (8, 8, 8, 8, 32, 32):
        # Biased: find the 2 syndromes with count 32
        over_syns = tuple(sorted([s for s, c in syn_counts.items() if c == 32]))
        over_pair = over_syns
    
    orbit_profiles.append({
        'missing': missing_tup,
        'dist': vals_sorted,
        'is_biased': vals_sorted == (8, 8, 8, 8, 32, 32),
        'over_pair': over_pair,
        'syn_counts': dict(syn_counts),
    })

# Q1: Do the 2 overrepresented syndromes form a Z₂ pair?
print("\nQ1: Do overrepresented syndromes in biased orbits form Z₂ pairs?")
z2_pair_set = set(z2_pairs)
biased_orbits = [p for p in orbit_profiles if p['is_biased']]
non_z2_count = 0
over_pair_is_z2 = Counter()
for bp in biased_orbits:
    if bp['over_pair'] in z2_pair_set:
        over_pair_is_z2[True] += 1
    else:
        over_pair_is_z2[False] += 1
        non_z2_count += 1
        if non_z2_count <= 5:
            print(f"  NON-Z₂ example: missing={bp['missing']}, over={bp['over_pair']}, counts={bp['syn_counts']}")

print(f"\n  Z₂ pair: {over_pair_is_z2.get(True, 0)} orbits")
print(f"  Not Z₂:  {over_pair_is_z2.get(False, 0)} orbits")
if over_pair_is_z2.get(False, 0) == 0:
    print(f"  ✓ ALL overrepresented pairs are Z₂ pairs")
else:
    print(f"  ✗ Some overrepresented pairs are NOT Z₂ pairs")

# Q2: Do the 144 biased orbits split 48×3 among the 3 non-missing Z₂ pairs?
print("\n" + "=" * 72)
print("Q2: BIASED ORBIT SPLIT ACROSS NON-MISSING Z₂ PAIRS")
print("=" * 72)

for missing_pair in z2_pairs:
    matching_biased = [bp for bp in orbit_profiles if bp['is_biased'] and bp['missing'] == missing_pair]
    matching_uniform = [bp for bp in orbit_profiles if not bp['is_biased'] and bp['missing'] == missing_pair]
    
    non_missing_z2 = [zp for zp in z2_pairs if zp != missing_pair]
    
    over_counts = Counter()
    for bp in matching_biased:
        over_counts[bp['over_pair']] += 1
    
    print(f"\n  Missing {missing_pair}: {len(matching_uniform)} uniform + {len(matching_biased)} biased")
    for zp in non_missing_z2:
        print(f"    Overrepresented {zp}: {over_counts.get(zp, 0)} orbits")
    
    # Check uniformity
    vals = [over_counts.get(zp, 0) for zp in non_missing_z2]
    if len(set(vals)) == 1 and vals[0] == 48:
        print(f"    ✓ Perfect 48×3 = 144 split")
    else:
        print(f"    Split: {vals} (expected [48, 48, 48])")

# Q3: Summary table
print("\n" + "=" * 72)
print("FULL CLASSIFICATION TABLE")
print("=" * 72)

print(f"\n{'Missing':>10s} {'Uniform':>8s} {'Biased':>7s}  {'Bias→Z2pair':>12s} {'Counts':>20s}")
for missing_pair in z2_pairs:
    matching_biased = [bp for bp in orbit_profiles if bp['is_biased'] and bp['missing'] == missing_pair]
    matching_uniform = [bp for bp in orbit_profiles if not bp['is_biased'] and bp['missing'] == missing_pair]
    
    non_missing_z2 = [zp for zp in z2_pairs if zp != missing_pair]
    over_counts = Counter(bp['over_pair'] for bp in matching_biased)
    
    bias_str = '/'.join(f"{over_counts.get(zp,0)}" for zp in non_missing_z2)
    nm_str = ','.join(f"{zp}" for zp in non_missing_z2)
    
    print(f"  {str(missing_pair):>10s} {len(matching_uniform):>8d} {len(matching_biased):>7d}  {bias_str:>12s} {nm_str:>20s}")

# ═══════════════════════════════════════════════════════════════
# Q4: Does the 96/144 split correlate with shared negation pair?
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 72)
print("Q3: ALGEBRAIC CHARACTERIZATION OF UNIFORM VS BIASED")
print("=" * 72)

# For each orbit, check the shared negation pair of its first surjection
# The shared_neg is the negation pair assigned to BOTH type-2 comp pairs
print("\nChecking shared negation pair correlation...")

# First: does metadata exist for all surjections?
# Some surjections may have been deduplicated. Track by orbit.

# For each orbit, characterize by the frame pair values
# Frame pair = comp_pairs[0] = (0, 15). f(0) and f(15) are the Frame values.
# For Type-2 orbits, the shared neg pair is {f(0), f(15)} since pair 0 is type-2.

for missing_pair in z2_pairs:
    print(f"\n  Missing {missing_pair}:")
    uniform_frame = Counter()
    biased_frame = Counter()
    
    for i, orbit in enumerate(orbits):
        bp = orbit_profiles[i]
        if bp['missing'] != missing_pair:
            continue
        
        # Get frame pair value for first surjection in orbit
        f = orbit[0]
        frame_val = frozenset({f[0], f[15]})  # values at Frame pair (0,15)
        
        if bp['is_biased']:
            biased_frame[frame_val] += 1
        else:
            uniform_frame[frame_val] += 1
    
    print(f"    Uniform: {len(uniform_frame)} distinct frame pairs, total {sum(uniform_frame.values())}")
    print(f"    Biased:  {len(biased_frame)} distinct frame pairs, total {sum(biased_frame.values())}")
    
    # Show overlap
    all_frame = set(uniform_frame.keys()) | set(biased_frame.keys())
    if len(all_frame) <= 8:
        for fv in sorted(all_frame, key=lambda x: sorted(x)):
            u = uniform_frame.get(fv, 0)
            b = biased_frame.get(fv, 0)
            print(f"      Frame {set(fv)}: uniform={u}, biased={b}")

# ═══════════════════════════════════════════════════════════════
# Deeper: check the Aut(Z₁₃) subgroup structure
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 72)
print("Q4: Aut(Z₁₃) SUBGROUP STRUCTURE")
print("=" * 72)

# Aut(Z₁₃) = (Z/13Z)* ≅ Z₁₂
# Subgroups: Z₁, Z₂, Z₃, Z₄, Z₆, Z₁₂
# Z₂ = {1, 12} (negation)
# Z₃ = {1, 3, 9} (cube roots: 3³ = 27 ≡ 1 mod 13)
# Z₄ = {1, 5, 12, 8} (5⁴ = 625 ≡ 1 mod 13)  
# Z₆ = {1, 3, 9, 12, 10, 4}

# Check: what is the order of each element?
print("\nElement orders in (Z/13Z)*:")
for a in range(1, 13):
    order = 1
    cur = a
    while cur != 1:
        cur = (cur * a) % 13
        order += 1
    print(f"  α={a:2d}: order {order}")

# Z₃ subgroup
z3 = [a for a in range(1, 13) if pow(a, 3, 13) == 1]
print(f"\nZ₃ subgroup: {z3}")

# Z₂ × Z₃ = Z₆
z6 = [a for a in range(1, 13) if pow(a, 6, 13) == 1]
print(f"Z₆ subgroup: {z6}")

# Z₄ subgroup
z4 = [a for a in range(1, 13) if pow(a, 4, 13) == 1]
print(f"Z₄ subgroup: {z4}")

# The biased/uniform split: does it correspond to kernel × Z₃ vs kernel × Z₄ sub-orbits?
# Each orbit has size 96 = 8 × 12. 
# Biased: (8,8,8,8,32,32) → 96 total. Sum = 96 ✓
# Uniform: (16,16,16,16,16,16) → 96 total. Sum = 96 ✓

# In biased orbits: 32 = 8 × 4 surjections at two syndromes
# In uniform orbits: 16 = 8 × 2 surjections at each of 6 syndromes

# The kernel contributes factor 8 (preserving or shifting syndrome by ⊕1).
# For Z₂ paired syndromes, each pair gets 8 from kernel action.
# So per Z₂ pair in a biased orbit:
#   overrepresented pair: 32+32 = 64 surjections (for the pair) → 32 per syndrome
#   underrepresented pair: 8+8 = 16 surjections → 8 per syndrome

# That's 64 + 16 + 16 = 96. But there are 3 non-missing pairs: 64+16+16 = 96 ✓

# For uniform: each of 3 pairs gets 16+16 = 32 → 3×32 = 96 ✓

print(f"\n  Biased orbit: 64+16+16 = 96 across 3 Z₂ pairs")
print(f"  Uniform orbit: 32+32+32 = 96 across 3 Z₂ pairs")

# Separate kernel and Aut(Z₁₃) actions within individual orbits
print("\n" + "=" * 72)
print("Q5: KERNEL VS Aut(Z₁₃) DECOMPOSITION WITHIN ORBITS")
print("=" * 72)

# Pick one uniform orbit and one biased orbit
examples = {'uniform': None, 'biased': None}
for i, orbit in enumerate(orbits):
    bp = orbit_profiles[i]
    if bp['is_biased'] and examples['biased'] is None:
        examples['biased'] = i
    if not bp['is_biased'] and examples['uniform'] is None:
        examples['uniform'] = i
    if all(v is not None for v in examples.values()):
        break

for label, idx in examples.items():
    orbit = orbits[idx]
    bp = orbit_profiles[idx]
    print(f"\n  Example {label} orbit (idx={idx}):")
    print(f"    Missing: {bp['missing']}, Syn counts: {bp['syn_counts']}")
    
    # Take one surjection and apply kernel-only and Aut-only
    f0 = orbit[0]
    s0 = syn_int(syn_map[f0])
    
    # Kernel action on f0 (α=1, vary g)
    kernel_syns = Counter()
    for g_inv in kernel_invs:
        t = tuple(f0[mat_vec_f2(g_inv, x, 4)] for x in range(N))
        if t in surj_set:
            kernel_syns[syn_int(syn_map[t])] += 1
    
    # Aut(Z₁₃) action on f0 (g=identity, vary α)
    id_inv = kernel_invs[0]  # identity
    aut_syns = Counter()
    for alpha in aut_zp:
        t = tuple((alpha * f0[x]) % p for x in range(N))
        if t in surj_set:
            aut_syns[syn_int(syn_map[t])] += 1
    
    print(f"    Base syndrome: {s0}")
    print(f"    Kernel-only syndromes (8 images): {dict(sorted(kernel_syns.items()))}")
    print(f"    Aut-only syndromes (12 images):   {dict(sorted(aut_syns.items()))}")

# ═══════════════════════════════════════════════════════════════
# Final: precise characterization of uniform vs biased
# ═══════════════════════════════════════════════════════════════

print("\n" + "=" * 72)
print("CHARACTERIZATION: WHAT DETERMINES UNIFORM VS BIASED?")
print("=" * 72)

# Check: for each orbit, compute the Aut(Z₁₃) orbit of the base syndrome
# In biased orbits, Aut visits fewer cosets → concentrates at one pair

# For each orbit's first surjection, apply all 12 Aut elements and record syndromes
print("\nAut(Z₁₃) syndrome orbits across biased vs uniform:")
aut_orbit_sizes = {'uniform': Counter(), 'biased': Counter()}

for i, orbit in enumerate(orbits):
    bp = orbit_profiles[i]
    f0 = orbit[0]
    aut_syns_set = set()
    for alpha in aut_zp:
        t = tuple((alpha * f0[x]) % p for x in range(N))
        if t in surj_set:
            aut_syns_set.add(syn_int(syn_map[t]))
    
    label = 'biased' if bp['is_biased'] else 'uniform'
    aut_orbit_sizes[label][len(aut_syns_set)] += 1

print(f"  Uniform orbits — Aut syndrome orbit sizes: {dict(sorted(aut_orbit_sizes['uniform'].items()))}")
print(f"  Biased orbits  — Aut syndrome orbit sizes: {dict(sorted(aut_orbit_sizes['biased'].items()))}")

# Check: in biased orbits, which syndromes does Aut visit?
print("\nBiased orbit Aut syndrome patterns:")
biased_aut_patterns = Counter()
for i, orbit in enumerate(orbits):
    bp = orbit_profiles[i]
    if not bp['is_biased']:
        continue
    f0 = orbit[0]
    aut_syns = set()
    for alpha in aut_zp:
        t = tuple((alpha * f0[x]) % p for x in range(N))
        if t in surj_set:
            aut_syns.add(syn_int(syn_map[t]))
    biased_aut_patterns[tuple(sorted(aut_syns))] += 1

for pattern, count in sorted(biased_aut_patterns.items()):
    # Identify Z₂ pairs visited
    pairs_visited = set()
    for s in pattern:
        for zp in z2_pairs:
            if s in zp:
                pairs_visited.add(zp)
    print(f"  {pattern}: {count} orbits (visits {len(pairs_visited)} Z₂ pairs)")

# Similarly for uniform
print("\nUniform orbit Aut syndrome patterns:")
uniform_aut_patterns = Counter()
for i, orbit in enumerate(orbits):
    bp = orbit_profiles[i]
    if bp['is_biased']:
        continue
    f0 = orbit[0]
    aut_syns = set()
    for alpha in aut_zp:
        t = tuple((alpha * f0[x]) % p for x in range(N))
        if t in surj_set:
            aut_syns.add(syn_int(syn_map[t]))
    uniform_aut_patterns[tuple(sorted(aut_syns))] += 1

for pattern, count in sorted(uniform_aut_patterns.items()):
    pairs_visited = set()
    for s in pattern:
        for zp in z2_pairs:
            if s in zp:
                pairs_visited.add(zp)
    print(f"  {pattern}: {count} orbits (visits {len(pairs_visited)} Z₂ pairs)")

print("\nDone.")
