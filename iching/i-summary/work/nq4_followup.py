#!/usr/bin/env python3
"""Quick follow-up: characterize which 2 syndromes are missing from each orbit."""

import sys
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

comp_pairs = []
seen = set()
for x in range(N):
    if x not in seen:
        cx = x ^ all_ones
        seen.add(x); seen.add(cx)
        comp_pairs.append((min(x, cx), max(x, cx)))

non_frame_reps = [comp_pairs[i][0] for i in range(1, 8)]
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

print("Enumerating surjections...")
surjections = []
for shared_neg_idx in range(6):
    shared_neg = neg_pairs[shared_neg_idx]
    remaining_neg = [neg_pairs[j] for j in range(6) if j != shared_neg_idx]
    for assignment in permutations(remaining_neg):
        for t2_orient in iterproduct([0,1], repeat=2):
            for t1_orient in iterproduct([0,1], repeat=5):
                vals = [None]*8
                for pi in type0_pairs: vals[pi] = 0
                for k, pi in enumerate(type2_pairs): vals[pi] = shared_neg[t2_orient[k]]
                for k, pi in enumerate(type1_pairs): vals[pi] = assignment[k][t1_orient[k]]
                fmap = {}
                for i, (a, b) in enumerate(comp_pairs):
                    fmap[a] = vals[i]
                    fmap[b] = (-vals[i]) % p
                if len(set(fmap.values())) == p:
                    surjections.append(tuple(fmap[x] for x in range(N)))
surj_set = set(surjections)
surjections = list(surj_set)
print(f"Surjections: {len(surjections)}")

def orientation_vector(f_tuple):
    return tuple(0 if f_tuple[non_frame_reps[j]] <= 6 else 1 for j in range(7))

def syndrome(v):
    return tuple(sum(H[bit][j] & v[j] for j in range(7)) % 2 for bit in range(3))

def syn_int(s): return s[0] + 2*s[1] + 4*s[2]

# Precompute syndromes
syn_map = {}
for f in surjections:
    v = orientation_vector(f)
    syn_map[f] = syndrome(v)

# Build kernel
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

# Compute orbits with union-find
parent = {f: f for f in surjections}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[ra] = rb

print("Computing orbits...")
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

# Analyze missing syndromes per orbit
missing_pair_counts = Counter()
orbit_missing = []
for orbit in orbits:
    present = set()
    for f in orbit:
        present.add(syn_int(syn_map[f]))
    missing = set(range(8)) - present
    missing_tup = tuple(sorted(missing))
    missing_pair_counts[missing_tup] += 1
    orbit_missing.append(missing_tup)

print(f"\nMissing syndrome pairs across {len(orbits)} orbits:")
for pair, count in sorted(missing_pair_counts.items()):
    print(f"  Missing {pair}: {count} orbits")

# Verify: are the missing pairs always Z₂ pairs?
z2_pairs = [(0,1), (2,3), (4,5), (6,7)]
print(f"\nZ₂ syndrome pairs (from kernel action): {z2_pairs}")

# Also check syndrome distribution per orbit
print(f"\nSyndrome counts within each missing-pair class (first 3 orbits each):")
for pair in sorted(missing_pair_counts.keys()):
    matching = [i for i, mp in enumerate(orbit_missing) if mp == pair]
    for idx in matching[:3]:
        orbit = orbits[idx]
        syn_counts = Counter(syn_int(syn_map[f]) for f in orbit)
        print(f"  Missing {pair}, orbit {idx}: {dict(sorted(syn_counts.items()))}")

# Check: do orbits with same missing pair have same syndrome count distribution?
print(f"\nWithin-orbit syndrome count distributions by class:")
for pair in sorted(missing_pair_counts.keys()):
    matching = [i for i, mp in enumerate(orbit_missing) if mp == pair]
    dist_counts = Counter()
    for idx in matching:
        orbit = orbits[idx]
        syn_counts = Counter(syn_int(syn_map[f]) for f in orbit)
        dist = tuple(sorted(syn_counts.values()))
        dist_counts[dist] += 1
    print(f"  Missing {pair}: {dict(dist_counts)}")

# Check: is the 3-way split (320, 320, 320)?
print(f"\n  Summary: {len(orbits)} = " + " + ".join(f"{v}" for _, v in sorted(missing_pair_counts.items())))

# Now check: what determines which pair is missing?
# Is it related to the shared negation pair of the type-2 complement pairs?
print(f"\n  Checking if missing syndrome pair correlates with assignment structure...")
# For the first orbit in each class, check the shared negation pair
for pair in sorted(missing_pair_counts.keys()):
    matching = [i for i, mp in enumerate(orbit_missing) if mp == pair]
    shared_negs = Counter()
    for idx in matching[:50]:
        f = orbits[idx][0]
        # Determine the shared negation pair
        val_pair0 = frozenset({f[comp_pairs[0][0]], f[comp_pairs[0][1]]})
        val_pair7 = frozenset({f[comp_pairs[7][0]], f[comp_pairs[7][1]]})
        shared_negs[frozenset({val_pair0, val_pair7})] += 1
    print(f"  Missing {pair}: {len(shared_negs)} distinct shared-neg patterns in first 50 orbits")

print("\nDone.")
