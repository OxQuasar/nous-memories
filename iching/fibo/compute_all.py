#!/usr/bin/env python3
"""
Three computational tasks for I Ching Fibonacci analysis:
  Task A:  Exhaustive structural count sweep
  Task A5: Complement involution on 克 cycle  
  Task B:  Sparsity null model
"""

import json
import numpy as np
from math import gcd, factorial, comb
from collections import Counter
from itertools import product
from sympy import isprime, Matrix

# ── Fibonacci reference set ──────────────────────────────────────────────
def fibonacci_set(max_val=10000):
    fibs = set()
    fib_list = []
    a, b = 1, 1
    while a <= max_val:
        fibs.add(a)
        fib_list.append(a)
        a, b = b, a + b
    return fibs, fib_list

FIBS, FIB_LIST = fibonacci_set(100000)

def is_fib(n):
    return n in FIBS

# ── Load data ────────────────────────────────────────────────────────────
with open("memories/iching/atlas/atlas.json") as f:
    atlas = json.load(f)

with open("memories/iching/atlas/transitions.json") as f:
    transitions = json.load(f)


# ══════════════════════════════════════════════════════════════════════════
# TASK A: Exhaustive Structural Count Sweep
# ══════════════════════════════════════════════════════════════════════════
print("=" * 72)
print("TASK A: EXHAUSTIVE STRUCTURAL COUNT SWEEP")
print("=" * 72)

counts = {}  # name -> value

# ── A1: atlas.json counts ────────────────────────────────────────────────

# Total hexagrams
counts["hexagram_count"] = 64

# Trigram count
trigram_elements = {}
for h in atlas.values():
    for t in [h['lower_trigram'], h['upper_trigram']]:
        trigram_elements[t['val']] = t['element']
counts["trigram_count"] = len(trigram_elements)  # 8

# Element counts (how many trigrams per element)
elem_count = Counter(trigram_elements.values())
for e, c in sorted(elem_count.items()):
    counts[f"trigrams_with_element_{e}"] = c

# Palace structure
palaces = Counter(h['palace'] for h in atlas.values())
counts["palace_count"] = len(palaces)  # 8
counts["hexagrams_per_palace"] = 8  # all same

# Basin structure
basins = Counter(h['basin'] for h in atlas.values())
counts["basin_count"] = len(basins)
for b, c in sorted(basins.items()):
    counts[f"basin_size_{b}"] = c

# Surface relation counts
relations = Counter(h['surface_relation'] for h in atlas.values())
counts["surface_relation_types"] = len(relations)
for r, c in sorted(relations.items()):
    counts[f"surface_relation_{r}"] = c

# Hu relation counts
hu_relations = Counter(h['hu_relation'] for h in atlas.values())
counts["hu_relation_types"] = len(hu_relations)
for r, c in sorted(hu_relations.items()):
    counts[f"hu_relation_{r}"] = c

# Depth distribution
depths = Counter(h['depth'] for h in atlas.values())
for d, c in sorted(depths.items()):
    counts[f"depth_{d}_count"] = c

# Hu depth distribution
hu_depths = Counter(h['hu_depth'] for h in atlas.values())
for d, c in sorted(hu_depths.items()):
    counts[f"hu_depth_{d}_count"] = c

# Rank distribution
ranks = Counter(h['rank'] for h in atlas.values())
counts["rank_count"] = len(ranks)  # 8 ranks (0-7)

# I-component sizes
i_comp = Counter(h['i_component'] for h in atlas.values())
counts["i_component_count"] = len(i_comp)
for ic, c in sorted(i_comp.items()):
    counts[f"i_component_{ic}_size"] = c

# ── Hu (nuclear) transformation structure ────────────────────────────────
hu_map = {int(k): h['hu_hex'] for k, h in atlas.items()}

# Fixed points
hu_fixed = [k for k, v in hu_map.items() if k == v]
counts["hu_fixed_points"] = len(hu_fixed)

# Attractors
hu_attractors = set(h['hu_attractor'] for h in atlas.values())
counts["hu_attractor_count"] = len(hu_attractors)

# Orbit structure (following the map until revisiting)
def compute_orbits(mapping, n=64):
    visited = set()
    orbits = []
    for start in range(n):
        if start in visited:
            continue
        orbit = []
        cur = start
        while cur not in visited:
            visited.add(cur)
            orbit.append(cur)
            cur = mapping[cur]
        orbits.append(orbit)
    return orbits

def compute_cycles(mapping, n=64):
    visited = set()
    cycles = []
    for start in range(n):
        path = []
        seen_in_path = set()
        cur = start
        while cur not in visited and cur not in seen_in_path:
            seen_in_path.add(cur)
            path.append(cur)
            cur = mapping[cur]
        if cur in seen_in_path and cur not in visited:
            cycle_start = path.index(cur)
            cycle = path[cycle_start:]
            cycles.append(cycle)
        visited.update(seen_in_path)
    return cycles

hu_orbits = compute_orbits(hu_map)
hu_cycles = compute_cycles(hu_map)
counts["hu_orbit_count"] = len(hu_orbits)
hu_orbit_sizes = sorted([len(o) for o in hu_orbits])
counts["hu_cycle_count"] = len(hu_cycles)
hu_cycle_lengths = sorted([len(c) for c in hu_cycles])
for length, cnt in Counter(hu_orbit_sizes).items():
    counts[f"hu_orbits_of_size_{length}"] = cnt
for length, cnt in Counter(hu_cycle_lengths).items():
    counts[f"hu_cycles_of_length_{length}"] = cnt

# Basin sizes for hu map (how many hexagrams flow into each attractor)
hu_basin_sizes = Counter(h['hu_attractor'] for h in atlas.values())
for att, sz in sorted(hu_basin_sizes.items()):
    counts[f"hu_basin_to_attractor_{att}"] = sz

# ── Complement/Reverse/RevComp structure ─────────────────────────────────
comp_map = {int(k): h['complement'] for k, h in atlas.items()}
rev_map = {int(k): h['reverse'] for k, h in atlas.items()}
rc_map = {int(k): h['rev_comp'] for k, h in atlas.items()}

counts["complement_fixed_points"] = sum(1 for k, v in comp_map.items() if k == v)
counts["reverse_fixed_points"] = sum(1 for k, v in rev_map.items() if k == v)
counts["rev_comp_fixed_points"] = sum(1 for k, v in rc_map.items() if k == v)

comp_orbits = compute_orbits(comp_map)
rev_orbits = compute_orbits(rev_map)
rc_orbits = compute_orbits(rc_map)
counts["complement_orbit_count"] = len(comp_orbits)
counts["reverse_orbit_count"] = len(rev_orbits)
counts["rev_comp_orbit_count"] = len(rc_orbits)

# Complement: all pairs (involution, no fixed points) → 32 pairs
counts["complement_pair_count"] = 32

# Reverse: 8 fixed + 28 pairs = 36 orbits
counts["reverse_pair_count"] = sum(1 for o in rev_orbits if len(o) == 2)

# ── Transitions: bian_fan structure ──────────────────────────────────────
bian_fan = transitions['bian_fan']
counts["bian_fan_total_transitions"] = len(bian_fan)

# Transitions per hexagram (each has 6 single-line flips)
counts["transitions_per_hexagram"] = 6

# Basin-crossing transitions
basin_cross = sum(1 for t in bian_fan if t['basin_crosses'])
counts["bian_basin_crossing_transitions"] = basin_cross
counts["bian_basin_preserving_transitions"] = len(bian_fan) - basin_cross

# Palace-crossing transitions
palace_cross = sum(1 for t in bian_fan if t['palace_crosses'])
counts["bian_palace_crossing_transitions"] = palace_cross
counts["bian_palace_preserving_transitions"] = len(bian_fan) - palace_cross

# I-component changes
i_comp_changes = sum(1 for t in bian_fan if t['i_component_changes'])
counts["bian_i_component_changing"] = i_comp_changes
counts["bian_i_component_preserving"] = len(bian_fan) - i_comp_changes

# Liuqin positions changed distribution
lq_changes = Counter(t['liuqin_positions_changed'] for t in bian_fan)
for ch, cnt in sorted(lq_changes.items()):
    counts[f"bian_liuqin_{ch}_positions_changed"] = cnt

# Surface relation preserved
rel_pres = sum(1 for t in bian_fan if t['surface_relation_preserved'])
counts["bian_relation_preserved"] = rel_pres
counts["bian_relation_changed"] = len(bian_fan) - rel_pres

# ── A3: F₂⁶ incidence geometry: Gaussian binomial coefficients ──────────

def gaussian_binomial(n, k, q=2):
    """Compute [n choose k]_q (Gaussian binomial coefficient)."""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    num = 1
    den = 1
    for i in range(k):
        num *= (q**(n - i) - 1)
        den *= (q**(i + 1) - 1)
    return num // den

print("\nF₂⁶ Gaussian binomial coefficients [6 choose k]₂:")
for k in range(7):
    gb = gaussian_binomial(6, k, 2)
    counts[f"gaussian_binom_6_{k}"] = gb
    print(f"  [6 choose {k}]₂ = {gb}")

# Number of k-dimensional subspaces of F₂⁶
# = [6 choose k]₂ (already computed above)

# Number of k-flats through the origin = [6 choose k]₂
# Number of k-flats in F₂⁶ (affine) = 2^(6-k) * [6 choose k]₂
print("\nAffine k-flats in F₂⁶:")
for k in range(7):
    gb = gaussian_binomial(6, k, 2)
    affine = (2**(6 - k)) * gb
    counts[f"affine_{k}_flats_in_F2_6"] = affine
    print(f"  {k}-flats: {affine}")

# F₂³ (trigram space)
print("\nF₂³ Gaussian binomial coefficients [3 choose k]₂:")
for k in range(4):
    gb = gaussian_binomial(3, k, 2)
    counts[f"gaussian_binom_3_{k}"] = gb
    print(f"  [3 choose {k}]₂ = {gb}")

# ── A4: Group-theoretic counts ──────────────────────────────────────────

def gl_order(n, q=2):
    """Order of GL(n, F_q)."""
    order = 1
    for i in range(n):
        order *= (q**n - q**i)
    return order

print("\n|GL(n, F₂)| for n=1..6:")
for n in range(1, 7):
    g = gl_order(n, 2)
    counts[f"GL_{n}_F2_order"] = g
    print(f"  |GL({n}, F₂)| = {g}")

# |SL(n, F₂)| = |GL(n, F₂)| / (q-1) = |GL(n, F₂)| for q=2
# |PGL(n, F₂)| = |GL(n, F₂)| / (q-1) = |GL(n, F₂)| for q=2

# Affine group |AGL(n, F₂)| = |GL(n, F₂)| * 2^n
print("\n|AGL(n, F₂)| for n=1..6:")
for n in range(1, 7):
    ag = gl_order(n, 2) * (2**n)
    counts[f"AGL_{n}_F2_order"] = ag
    print(f"  |AGL({n}, F₂)| = {ag}")

# ── A5: Derived counts ──────────────────────────────────────────────────

# Trigram cube F₂³: paths, distances, etc.
# Number of edges in the 3-cube (Q₃): 3 * 2^(3-1) = 12
counts["Q3_edges"] = 12
# Number of edges in Q₆: 6 * 2^5 = 192
counts["Q6_edges"] = 192

# Hamiltonian cycles on Q₃ (3-cube)
# Known: 6 directed Hamiltonian cycles, 3 undirected
counts["Q3_hamiltonian_cycles_directed"] = 6
counts["Q3_hamiltonian_cycles_undirected"] = 3

# Number of surjections F₂³ → Z₅
# |surjections| from an 8-element set to a 5-element set
# = S(8,5) * 5! where S is Stirling numbers of 2nd kind
# Using inclusion-exclusion: sum_{i=0}^{5} (-1)^i * C(5,i) * (5-i)^8
surj_8_5 = sum((-1)**i * comb(5, i) * (5 - i)**8 for i in range(6))
counts["surjections_F2_3_to_Z5"] = surj_8_5
print(f"\nSurjections F₂³ → Z₅ = {surj_8_5}")

# Number of complement-respecting surjections
# Complement pairs 4 complementary pairs in F₂³: {000,111}, {001,110}, {010,101}, {011,100}
# A complement-respecting surjection f satisfies f(~x) = -f(x) mod 5
# So f(x) + f(~x) = 0 mod 5
# Pair {000,111}: f(111) = -f(000) mod 5
# Since we map to Z₅ and need surjection...
# We have 4 pairs. For each pair, choosing f(x) determines f(~x) = -f(x).
# But f(000) can be 0 (since -0=0) or nonzero.
# If f(000) = 0, then f(111) = 0.
# If f(000) = k ≠ 0, then f(111) = -k ≠ k (since 2k ≠ 0 mod 5 for k≠0).
# 
# Actually, -k mod 5: for k=0, -0=0. For k=1, -1=4. For k=2, -2=3. For k=3, -3=2. For k=4, -4=1.
# So the involution σ(k) = -k mod 5 on Z₅ fixes {0} and swaps {1,4} and {2,3}.

# Count complement-respecting surjections:
# 4 complement pairs in F₂³. For each pair, choose f on one representative.
# Let representatives be 000, 001, 010, 011 (i.e., the 4 with top bit = 0).
# f(~x) = -f(x) mod 5.
# We need the image to cover all of Z₅.
# Choices for each representative: any value in Z₅ (5 options each).
# Total unrestricted: 5^4 = 625 complement-compatible functions.
# Subtract non-surjective ones.

# The image of f must be all of Z₅.
# The image consists of: for each rep x, we get {f(x), -f(x)}.
# If f(x) = 0, we get {0}. If f(x) = k ≠ 0, we get {k, -k} = {k, 5-k}.
# So each representative contributes either {0} or a pair from {{1,4},{2,3}}.
# We need {0,1,2,3,4} covered.
# Need at least one rep mapping to 0.
# Need at least one rep mapping to 1 or 4.
# Need at least one rep mapping to 2 or 3.

# Count by choosing values for 4 reps from Z₅:
comp_surj_count = 0
for vals in product(range(5), repeat=4):
    image = set()
    for v in vals:
        image.add(v)
        image.add((-v) % 5)
    if len(image) == 5:
        comp_surj_count += 1

counts["complement_respecting_surjections_F2_3_to_Z5"] = comp_surj_count
print(f"Complement-respecting surjections F₂³ → Z₅ = {comp_surj_count}")

# Hamiltonian cycles on C₅ (pentagon)
# C₅ has exactly 2 directed Hamiltonian cycles (the cycle and its reverse)
# and if we count undirected: 1 for each direction = essentially the cycle itself
# Wait, for directed: you can go clockwise or counterclockwise = 2 * 5!/5 = ... 
# Actually for C₅ (5-cycle), Hamiltonian cycles: the graph IS a single Hamiltonian cycle
# So: 1 undirected Hamiltonian cycle, 2 directed (if we consider starting point as same)
# But traditionally: number of distinct Hamiltonian cycles in C_n = (n-1)!/2
# For C₅: 4!/2 = 12? No that's for K₅.
# C₅ itself IS a Hamiltonian cycle. So there is exactly 1 undirected Hamiltonian cycle 
# (the cycle 0-1-2-3-4-0 is the same as the graph itself).
counts["C5_hamiltonian_cycles_undirected"] = 1
counts["C5_hamiltonian_cycles_directed"] = 2

# Number of automorphisms of the cube Q₃
# Aut(Q₃) ≅ S₃ ⋉ (Z₂)³, |Aut(Q₃)| = 48
counts["Aut_Q3"] = 48

# Number of distinct hexagram pairs (complement-symmetric): C(64,2) = 2016 total pairs
counts["hexagram_pairs"] = comb(64, 2)

# Number of 五行 elements
counts["wuxing_element_count"] = 5

# Number of 五行 relations (生, 克, 比和, etc.)
counts["wuxing_relation_types"] = 5  # 生体, 体生用, 克体, 体克用, 比和

# Lines per hexagram
counts["lines_per_hexagram"] = 6

# Trigrams per hexagram
counts["trigrams_per_hexagram"] = 2

# Najia stems
najia_stems = set()
najia_branches = set()
for h in atlas.values():
    for n in h['najia']:
        najia_stems.add(n['stem'])
        najia_branches.add(n['branch'])
counts["najia_distinct_stems_used"] = len(najia_stems)
counts["najia_distinct_branches_used"] = len(najia_branches)

# Nayin elements - check
nayin_elements = set()
for h in atlas.values():
    for n in h['nayin']:
        nayin_elements.add(n['element'])
counts["nayin_distinct_elements"] = len(nayin_elements)

# Liuqin types
lq_types = set()
for h in atlas.values():
    for lq in h['liuqin_word']:
        lq_types.add(lq)
counts["liuqin_types"] = len(lq_types)

# Liuqin missing distribution
lq_missing = Counter(len(h['liuqin_missing']) for h in atlas.values())
for m, c in sorted(lq_missing.items()):
    counts[f"hexagrams_with_{m}_missing_liuqin"] = c

# Shi/Ying values
shi_vals = Counter(h['shi'] for h in atlas.values())
ying_vals = Counter(h['ying'] for h in atlas.values())
counts["shi_distinct_values"] = len(shi_vals)
counts["ying_distinct_values"] = len(ying_vals)

# ── Print all counts sorted ─────────────────────────────────────────────
print("\n" + "─" * 72)
print(f"{'Count Name':<55} {'Value':>8} {'Fib?':>5}")
print("─" * 72)
all_counts = sorted(counts.items(), key=lambda x: x[1])
fib_counts = []
for name, val in all_counts:
    fib = is_fib(val)
    if fib:
        fib_counts.append((name, val))
    print(f"{name:<55} {val:>8} {'  ✓' if fib else ''}")

print("\n" + "─" * 72)
print("FIBONACCI COUNTS FOUND:")
print("─" * 72)
for name, val in fib_counts:
    idx = FIB_LIST.index(val) if val in FIB_LIST else -1
    print(f"  F({idx+1 if idx >= 0 else '?'}) = {val:>8}  ← {name}")

# Check specifically for 34 and 55
print(f"\n*** Does 34 appear? {34 in [v for _, v in all_counts]} ***")
matches_34 = [(n, v) for n, v in all_counts if v == 34]
print(f"    Counts equal to 34: {matches_34}")

print(f"\n*** Does 55 appear? {55 in [v for _, v in all_counts]} ***")
matches_55 = [(n, v) for n, v in all_counts if v == 55]
print(f"    Counts equal to 55: {matches_55}")

# Nearby: what counts are in [30,40] and [50,60]?
print(f"\n  Counts in [30,40]: {[(n,v) for n,v in all_counts if 30<=v<=40]}")
print(f"  Counts in [50,60]: {[(n,v) for n,v in all_counts if 50<=v<=60]}")


# ══════════════════════════════════════════════════════════════════════════
# TASK A.5: Complement Involution on 克 Cycle
# ══════════════════════════════════════════════════════════════════════════
print("\n\n" + "=" * 72)
print("TASK A.5: COMPLEMENT INVOLUTION ON 克 CYCLE")
print("=" * 72)

# Step 1: Trigram → Element mapping
print("\nTrigram → Element mapping:")
for v in sorted(trigram_elements.keys()):
    print(f"  {v} ({bin(v)[2:].zfill(3)}) → {trigram_elements[v]}")

# Step 2: Z₅ labeling of elements
# We need a consistent labeling. The 克 cycle is:
# Wood →克 Earth →克 Water →克 Fire →克 Metal →克 Wood
# In Z₅ with the 克 cycle as +2 mod 5:
# Standard: Wood=0, Fire=1, Earth=2, Metal=3, Water=4
# Then 生 (generation) cycle: Wood→Fire→Earth→Metal→Water→Wood = +1 mod 5
# And 克 (destruction) cycle: Wood→Earth→Water→Fire→Metal→Wood = +2 mod 5
# Let's verify: Wood(0)→Earth(2): +2. Earth(2)→Water(4): +2. Water(4)→Fire(1): +2 mod 5. 
# Fire(1)→Metal(3): +2. Metal(3)→Wood(0): +2 mod 5. ✓

element_to_z5 = {"Wood": 0, "Fire": 1, "Earth": 2, "Metal": 3, "Water": 4}
z5_to_element = {v: k for k, v in element_to_z5.items()}

print("\nZ₅ labeling (生 = +1, 克 = +2):")
for e, z in sorted(element_to_z5.items(), key=lambda x: x[1]):
    print(f"  {z}: {e}")

# Verify 克 cycle
print("\n克 cycle verification (each step is +2 mod 5):")
ke_cycle = ["Wood", "Earth", "Water", "Fire", "Metal"]
for i in range(5):
    src = ke_cycle[i]
    dst = ke_cycle[(i + 1) % 5]
    print(f"  {src}({element_to_z5[src]}) →克 {dst}({element_to_z5[dst]}): "
          f"delta = {(element_to_z5[dst] - element_to_z5[src]) % 5}")

# Step 3: Build the directed 克 adjacency matrix A (5×5)
# A[i,j] = 1 iff element i destroys element j
A = np.zeros((5, 5))
for i in range(5):
    j = (i + 2) % 5  # 克 = +2
    A[i, j] = 1

print("\n克 adjacency matrix A (row i destroys column j):")
print(A)

# Step 4: Complement involution on F₂³
# Complement: x ↦ ~x = x XOR 111
# This induces σ on Z₅ via the surjection.
# By the complement-antisymmetry property: if f(x) = e, then f(~x) = -e mod 5
# So σ(e) = -e mod 5

# σ on Z₅:
sigma_map = {i: (-i) % 5 for i in range(5)}
print(f"\nσ(e) = -e mod 5:")
for i in range(5):
    print(f"  σ({i}={z5_to_element[i]}) = {sigma_map[i]}={z5_to_element[sigma_map[i]]}")

# σ as permutation matrix
Sigma = np.zeros((5, 5))
for i in range(5):
    Sigma[i, sigma_map[i]] = 1

print(f"\nσ permutation matrix:")
print(Sigma)

# Verify σ is an involution
assert np.allclose(Sigma @ Sigma, np.eye(5)), "σ is not an involution!"
print("σ² = I ✓ (involution confirmed)")

# Fixed points: σ(0) = 0. Swaps: {1,4} and {2,3}.
print(f"Fixed point: 0 ({z5_to_element[0]})")
print(f"Swapped pairs: {{1,4}} ({z5_to_element[1]},{z5_to_element[4]}), "
      f"{{2,3}} ({z5_to_element[2]},{z5_to_element[3]})")

# Step 5: Eigendecomposition of Sigma
# Eigenvalues of σ: +1 (multiplicity 3: eigenvectors for fixed point + symmetric combos)
#                   -1 (multiplicity 2: antisymmetric combos)

eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
print(f"\nσ eigenvalues: {eigenvalues}")

# V⁺ (σ-eigenspace for +1): dimension 3
# Basis: e₀, (e₁ + e₄)/√2, (e₂ + e₃)/√2
# V⁻ (σ-eigenspace for -1): dimension 2
# Basis: (e₁ - e₄)/√2, (e₂ - e₃)/√2

# Construct orthonormal bases explicitly
e = [np.zeros(5) for _ in range(5)]
for i in range(5):
    e[i][i] = 1.0

# V⁺ basis (3D)
v_plus = np.array([
    e[0],
    (e[1] + e[4]) / np.sqrt(2),
    (e[2] + e[3]) / np.sqrt(2)
])

# V⁻ basis (2D)
v_minus = np.array([
    (e[1] - e[4]) / np.sqrt(2),
    (e[2] - e[3]) / np.sqrt(2)
])

# Verify
for i, v in enumerate(v_plus):
    assert np.allclose(Sigma @ v, v), f"v_plus[{i}] not in V⁺"
for i, v in enumerate(v_minus):
    assert np.allclose(Sigma @ v, -v), f"v_minus[{i}] not in V⁻"

print(f"\nV⁺ basis (dim {v_plus.shape[0]}):")
for i, v in enumerate(v_plus):
    print(f"  v⁺_{i} = {v}")

print(f"\nV⁻ basis (dim {v_minus.shape[0]}):")
for i, v in enumerate(v_minus):
    print(f"  v⁻_{i} = {v}")

# Step 6: Restrict A to V⁻
# A⁻ = P⁻ A P⁻ᵀ where P⁻ is 2×5 matrix (rows = V⁻ basis vectors)
P_minus = v_minus  # 2×5
A_minus = P_minus @ A @ P_minus.T

print(f"\n克 matrix restricted to V⁻ (2×2):")
print(A_minus)

# Characteristic polynomial of A⁻
# For 2×2 matrix [[a,b],[c,d]]: char poly = x² - (a+d)x + (ad-bc)
a, b = A_minus[0, 0], A_minus[0, 1]
c, d = A_minus[1, 0], A_minus[1, 1]
trace = a + d
det = a * d - b * c
print(f"\nTrace = {trace}")
print(f"Determinant = {det}")
print(f"Characteristic polynomial: x² - ({trace})x + ({det})")
print(f"                         = x² {'-' if trace >= 0 else '+'} {abs(trace)}x {'+' if det >= 0 else '-'} {abs(det)}")

# Compare to x² - x - 1 (Fibonacci polynomial)
if np.isclose(trace, 1.0) and np.isclose(det, -1.0):
    print("\n★★★ MATCH: Characteristic polynomial = x² − x − 1 (FIBONACCI POLYNOMIAL) ★★★")
    print(f"  Roots: φ = (1+√5)/2 ≈ {(1 + np.sqrt(5))/2:.6f}")
    print(f"        -1/φ = (1-√5)/2 ≈ {(1 - np.sqrt(5))/2:.6f}")
else:
    print(f"\n✗ Does NOT match x² − x − 1")
    # Compute actual eigenvalues
    disc = trace**2 - 4*det
    if disc >= 0:
        r1 = (trace + np.sqrt(disc)) / 2
        r2 = (trace - np.sqrt(disc)) / 2
        print(f"  Actual roots: {r1:.6f}, {r2:.6f}")
    else:
        print(f"  Complex roots (discriminant = {disc})")

# Also compute A⁺ (restriction to V⁺)
P_plus = v_plus  # 3×5
A_plus = P_plus @ A @ P_plus.T

print(f"\n克 matrix restricted to V⁺ (3×3):")
print(A_plus)

# Characteristic polynomial of A⁺ using numpy
eigenvals_plus = np.linalg.eigvals(A_plus)
print(f"Eigenvalues of A⁺: {eigenvals_plus}")

# Use sympy for exact characteristic polynomial
A_plus_sym = Matrix(A_plus).applyfunc(lambda x: int(round(x)) if abs(x - round(x)) < 1e-10 else x)
# Actually let's be more careful with sympy
from sympy import symbols, Rational, sqrt, Poly
x = symbols('x')

# For A⁻, compute exact char poly using rational arithmetic
# Recompute A⁻ with exact fractions
# A[i,j] = 1 iff j = (i+2) % 5
# v⁻₀ = (e₁ - e₄)/√2, v⁻₁ = (e₂ - e₃)/√2
# A⁻[0,0] = v⁻₀ᵀ A v⁻₀ = (e₁-e₄)ᵀ A (e₁-e₄) / 2
# A*e₁ = e₃ (since 1→3), A*e₄ = e₁ (since 4→1)
# (e₁-e₄)ᵀ (e₃ - e₁) / 2 = (0 - 1) / 2 = -1/2
# Hmm wait, Aᵀ or A? Let me re-check.
# A[i,j] = 1 iff i destroys j, i.e., j = (i+2)%5
# So A @ e_j picks out column j: (A @ e_j)[i] = A[i,j] = 1 iff j=(i+2)%5 iff i=(j-2)%5
# So A @ e_j = e_{(j-2)%5}
# A @ e₁ = e_{(1-2)%5} = e₄
# A @ e₄ = e_{(4-2)%5} = e₂
# A @ e₂ = e_{(2-2)%5} = e₀
# A @ e₃ = e_{(3-2)%5} = e₁

# Wait actually:
# A[i,j] = 1 iff element i destroys element j
# The 克 cycle: 0→2→4→1→3→0 (each destroys +2 mod 5)
# So A[0,2]=1, A[2,4]=1, A[4,1]=1, A[1,3]=1, A[3,0]=1
# A @ e_j: the j-th column of A. A[i,j]=1 when i is the destroyer of j.
# j is destroyed by (j-2)%5. So column j has a 1 at row (j-2)%5.
# A @ e_j = e_{(j-2)%5}

# v⁻₀ = (e₁ - e₄)/√2
# A v⁻₀ = (A e₁ - A e₄)/√2 = (e₄ - e₂)/√2 ... wait
# A e₁ = e_{(1-2)%5} = e_{4}
# A e₄ = e_{(4-2)%5} = e_{2}
# So A v⁻₀ = (e₄ - e₂)/√2

# Now project onto V⁻ basis:
# A⁻[0,0] = v⁻₀ · (A v⁻₀) = (e₁-e₄)/√2 · (e₄-e₂)/√2 = (0 - 1 + 0 + 0)/(2) = -1/2  (e₁·e₄=0, e₄·e₄=1... wait)
# (e₁-e₄)·(e₄-e₂) = e₁·e₄ - e₁·e₂ - e₄·e₄ + e₄·e₂ = 0 - 0 - 1 + 0 = -1
# So A⁻[0,0] = -1/2

# A⁻[1,0] = v⁻₁ · (A v⁻₀) = (e₂-e₃)/√2 · (e₄-e₂)/√2 = (e₂·e₄-e₂·e₂-e₃·e₄+e₃·e₂)/2
#          = (0 - 1 - 0 + 0)/2 = -1/2

# v⁻₁ = (e₂ - e₃)/√2
# A v⁻₁ = (A e₂ - A e₃)/√2 = (e₀ - e₁)/√2
# A e₂ = e_{(2-2)%5} = e₀
# A e₃ = e_{(3-2)%5} = e₁

# A⁻[0,1] = v⁻₀ · (A v⁻₁) = (e₁-e₄)/√2 · (e₀-e₁)/√2 = (e₁·e₀ - e₁·e₁ - e₄·e₀ + e₄·e₁)/2
#          = (0 - 1 - 0 + 0)/2 = -1/2

# A⁻[1,1] = v⁻₁ · (A v⁻₁) = (e₂-e₃)/√2 · (e₀-e₁)/√2 = (e₂·e₀-e₂·e₁-e₃·e₀+e₃·e₁)/2
#          = (0 - 0 - 0 + 0)/2 = 0

print("\n── Exact computation of A⁻ ──")
print("A⁻ = [[-1/2, -1/2], [-1/2, 0]]")
print(f"Numerical check: {A_minus}")

# Char poly of [[-1/2, -1/2],[-1/2, 0]]:
# det(xI - A⁻) = (x+1/2)(x-0) - (-1/2)(-1/2) = x² + x/2 - 1/4
# = x² + x/2 - 1/4
# Multiply by -4: -4x² - 2x + 1 ... no let's just compute
# trace = -1/2, det = (-1/2)(0) - (-1/2)(-1/2) = 0 - 1/4 = -1/4
print(f"Exact trace = -1/2, exact det = -1/4")
print(f"Char poly: x² - (-1/2)x + (-1/4) = x² + x/2 - 1/4")
print(f"Multiply by 4: 4x² + 2x - 1")
print(f"This is NOT x² - x - 1.")
print()

# But wait — let's check if A⁻ is a scalar multiple of something with char poly x²-x-1
# Eigenvalues of A⁻: roots of x² + x/2 - 1/4 = 0
# x = (-1/2 ± √(1/4 + 1))/2 = (-1/2 ± √(5/4))/2 = (-1/2 ± √5/2)/2 = (-1 ± √5)/4
r1_exact = (-1 + np.sqrt(5)) / 4
r2_exact = (-1 - np.sqrt(5)) / 4
print(f"Eigenvalues of A⁻: (-1+√5)/4 ≈ {r1_exact:.6f}, (-1-√5)/4 ≈ {r2_exact:.6f}")
print(f"Ratio: {r1_exact / ((1+np.sqrt(5))/2):.6f} (compared to φ)")
print(f"Note: eigenvalues are φ/2 and -1/(2φ) = -(φ-1)/2")
print(f"  φ/2 = {(1+np.sqrt(5))/4:.6f}")
print(f"  -1/(2φ) = {-2/((1+np.sqrt(5))*2):.6f}")

# So A⁻ = (1/2) * M where M has char poly x² - x - 1? Let's check.
# If A⁻ = M/2, then M = 2A⁻ = [[-1, -1],[-1, 0]]
M = 2 * A_minus
print(f"\n2A⁻ = {M}")
M_trace = M[0,0] + M[1,1]
M_det = M[0,0]*M[1,1] - M[0,1]*M[1,0]
print(f"Trace of 2A⁻ = {M_trace}, Det of 2A⁻ = {M_det}")
print(f"Char poly of 2A⁻: x² - ({M_trace})x + ({M_det}) = x² + x - 1")

# x² + x - 1 has roots (-1±√5)/2 — these are -φ and 1/φ.
# Compare to x² - x - 1 which has roots φ and -1/φ.
# x² + x - 1 = -((-x)² - (-x) - 1), so it's the "negated variable" version.
# Eigenvalues of 2A⁻: (-1+√5)/2 = 1/φ ≈ 0.618 and (-1-√5)/2 = -φ ≈ -1.618

print(f"\n★ KEY RESULT:")
print(f"  Char poly of 2A⁻ = x² + x − 1")
print(f"  This is the RECIPROCAL Fibonacci polynomial (x² + x − 1)")  
print(f"  Related to x² − x − 1 by the substitution x → −x")
print(f"  Eigenvalues: 1/φ and −φ (vs φ and −1/φ for x² − x − 1)")
print(f"  The golden ratio φ appears as an eigenvalue in both cases")

# Now let's think about whether a different sign convention gives x² - x - 1
# If we define A as the TRANSPOSE (j destroys i), or use 生 instead of 克...
# Let's try: if A is "destroyed BY" (transpose)
A_T = A.T
A_T_minus = P_minus @ A_T @ P_minus.T
print(f"\nA^T restricted to V⁻:")
print(A_T_minus)
AT_trace = A_T_minus[0,0] + A_T_minus[1,1]
AT_det = A_T_minus[0,0]*A_T_minus[1,1] - A_T_minus[0,1]*A_T_minus[1,0]
print(f"Char poly of A^T|V⁻: x² - ({AT_trace})x + ({AT_det})")

# Try 生 (generation) cycle: +1 mod 5
A_sheng = np.zeros((5, 5))
for i in range(5):
    j = (i + 1) % 5
    A_sheng[i, j] = 1
A_sheng_minus = P_minus @ A_sheng @ P_minus.T
print(f"\n生 matrix restricted to V⁻:")
print(A_sheng_minus)
AS_trace = A_sheng_minus[0,0] + A_sheng_minus[1,1]
AS_det = A_sheng_minus[0,0]*A_sheng_minus[1,1] - A_sheng_minus[0,1]*A_sheng_minus[1,0]
print(f"Char poly of 生|V⁻: x² - ({AS_trace})x + ({AS_det})")

# Compute for ALL cyclic shifts on Z₅
print(f"\n── All cyclic shift matrices restricted to V⁻ ──")
for shift in range(5):
    A_s = np.zeros((5, 5))
    for i in range(5):
        A_s[i, (i + shift) % 5] = 1
    A_s_minus = P_minus @ A_s @ P_minus.T
    tr = A_s_minus[0,0] + A_s_minus[1,1]
    dt = A_s_minus[0,0]*A_s_minus[1,1] - A_s_minus[0,1]*A_s_minus[1,0]
    print(f"  shift={shift}: trace={tr:.4f}, det={dt:.4f}, "
          f"char poly: x² - ({tr:.4f})x + ({dt:.4f})")

# Also the full V⁺ restriction for 克
print(f"\n克 matrix restricted to V⁺ (3×3):")
print(A_plus)
eigvals_plus_exact = np.linalg.eigvals(A_plus)
print(f"Eigenvalues of A⁺: {eigvals_plus_exact}")
coeffs_plus = np.poly(A_plus)
print(f"Char poly coefficients of A⁺: {coeffs_plus}")
print(f"Char poly of A⁺: x³ {'+' if coeffs_plus[1]>=0 else '-'} {abs(coeffs_plus[1]):.4f}x² "
      f"{'+' if coeffs_plus[2]>=0 else '-'} {abs(coeffs_plus[2]):.4f}x "
      f"{'+' if coeffs_plus[3]>=0 else '-'} {abs(coeffs_plus[3]):.4f}")


# ══════════════════════════════════════════════════════════════════════════
# TASK B: Sparsity Null Model
# ══════════════════════════════════════════════════════════════════════════
print("\n\n" + "=" * 72)
print("TASK B: SPARSITY NULL MODEL")
print("=" * 72)

# The "forcing chain" at dimension n:
#   base = 2 (always)
#   dimension = n
#   prime_candidate = 2^n - 3 (only if prime)
#   trigram_count = 2^n

print("\n── Forcing chain parameters for n=2..20 ──")
print(f"{'n':>3} {'base':>5} {'dim':>5} {'2^n-3':>8} {'prime?':>7} {'2^n':>8} "
      f"{'base∈F':>6} {'dim∈F':>6} {'2n-3∈F':>7} {'2n∈F':>5} {'all_F':>6} {'consec':>7}")
print("─" * 85)

results = []
for n in range(2, 21):
    base = 2
    dim = n
    p_cand = 2**n - 3
    trig = 2**n
    p_is_prime = isprime(p_cand)
    
    base_fib = is_fib(base)
    dim_fib = is_fib(dim)
    pcand_fib = is_fib(p_cand) if p_is_prime else False
    trig_fib = is_fib(trig)
    
    all_fib = base_fib and dim_fib and trig_fib and (pcand_fib if p_is_prime else False)
    
    # Check consecutiveness: are base, dim, p_cand, trig consecutive Fibonacci numbers?
    consec = False
    if all_fib and p_is_prime:
        vals = [base, dim, p_cand, trig]
        indices = [FIB_LIST.index(v) for v in vals if v in FIB_LIST]
        if len(indices) == 4:
            consec = (indices == sorted(indices) and 
                     indices[-1] - indices[0] == 3 and
                     len(set(indices)) == 4)
    
    results.append({
        'n': n, 'base': base, 'dim': dim, 'p_cand': p_cand, 'p_prime': p_is_prime,
        'trig': trig, 'base_fib': base_fib, 'dim_fib': dim_fib, 
        'pcand_fib': pcand_fib, 'trig_fib': trig_fib, 'all_fib': all_fib, 
        'consec': consec
    })
    
    print(f"{n:>3} {base:>5} {dim:>5} {p_cand:>8} {'✓' if p_is_prime else '✗':>7} "
          f"{trig:>8} {'✓' if base_fib else '':>6} {'✓' if dim_fib else '':>6} "
          f"{'✓' if pcand_fib else ('n/a' if not p_is_prime else ''):>7} "
          f"{'✓' if trig_fib else '':>5} {'★' if all_fib else '':>6} "
          f"{'★★' if consec else '':>7}")

# ── Probability calculations ─────────────────────────────────────────────
print("\n── Probability Analysis ──")

# Among n=2..20, which have 2^n as Fibonacci?
n_range = list(range(2, 21))
powers_of_2_that_are_fib = [n for n in n_range if is_fib(2**n)]
print(f"\nn values where 2^n is Fibonacci: {powers_of_2_that_are_fib}")
print(f"  2^1=2 ✓, 2^3=8 ✓, and those are the ONLY powers of 2 that are Fibonacci (by Carmichael)")
p_trig_fib = len(powers_of_2_that_are_fib) / len(n_range)
print(f"  P(2^n ∈ Fibonacci | n ∈ [2,20]) = {len(powers_of_2_that_are_fib)}/{len(n_range)} = {p_trig_fib:.4f}")

# Among n=2..20, which n are Fibonacci?
n_fib = [n for n in n_range if is_fib(n)]
print(f"\nn values that are Fibonacci: {n_fib}")
p_dim_fib = len(n_fib) / len(n_range)
print(f"  P(n ∈ Fibonacci | n ∈ [2,20]) = {len(n_fib)}/{len(n_range)} = {p_dim_fib:.4f}")

# Among primes of form 2^n-3 for n=2..20, which are Fibonacci?
primes_2n3 = [(n, 2**n - 3) for n in n_range if isprime(2**n - 3)]
print(f"\nPrimes of form 2^n-3 for n ∈ [2,20]: {primes_2n3}")
fib_primes_2n3 = [(n, p) for n, p in primes_2n3 if is_fib(p)]
print(f"Of those, Fibonacci: {fib_primes_2n3}")
if primes_2n3:
    p_prime_fib = len(fib_primes_2n3) / len(primes_2n3)
    print(f"  P(2^n-3 ∈ Fibonacci | 2^n-3 prime, n ∈ [2,20]) = {len(fib_primes_2n3)}/{len(primes_2n3)} = {p_prime_fib:.4f}")

# Joint probability (assuming independence)
p_joint = p_trig_fib * p_dim_fib * p_prime_fib  # base=2 is always Fibonacci
print(f"\nJoint probability (assuming independence):")
print(f"  P(all four Fibonacci) ≈ 1 × {p_dim_fib:.4f} × {p_prime_fib:.4f} × {p_trig_fib:.4f} = {p_joint:.6f}")
print(f"  = {p_joint*100:.4f}%")

# Consecutiveness analysis
print(f"\n── Consecutiveness ──")
print(f"At n=3: base=2, dim=3, prime=5, count=8")
print(f"These are F(3), F(4), F(5), F(6) — consecutive Fibonacci numbers.")
print(f"Given that all four are Fibonacci and monotonically increase from 2 to 8,")
print(f"the only Fibonacci numbers in [2,8] are: 2, 3, 5, 8")
print(f"So consecutiveness is FORCED once we have all-Fibonacci + monotonicity.")
print(f"Conditional P(consecutive | all Fibonacci) = 1")
print(f"Overall P(four consecutive Fibonacci) = P(all Fibonacci) = {p_joint*100:.4f}%")

# ── Ambient density: "structurally interesting" numbers in [2,20] ────────
print(f"\n── Ambient Density of Structurally Interesting Numbers in [2,20] ──")

primes_set = {n for n in range(2, 21) if isprime(n)}
prime_powers = set()
for p in primes_set:
    pk = p
    while pk <= 20:
        prime_powers.add(pk)
        pk *= p

fib_set_2_20 = {n for n in range(2, 21) if is_fib(n)}
catalan = {1, 2, 5, 14}  # C(0)..C(4) within range
catalan_in_range = catalan & set(range(2, 21))
triangular = {n*(n+1)//2 for n in range(1, 7)} & set(range(2, 21))
bell = {1, 2, 5, 15}  # B(1)..B(4)
bell_in_range = bell & set(range(2, 21))

# Binomial coefficients C(n,k) for n≤10 in range [2,20]
binom_set = set()
for nn in range(2, 11):
    for kk in range(0, nn + 1):
        c = comb(nn, kk)
        if 2 <= c <= 20:
            binom_set.add(c)

all_interesting = set(range(2, 21))
interesting = primes_set | prime_powers | fib_set_2_20 | catalan_in_range | triangular | bell_in_range | binom_set

print(f"  Primes: {sorted(primes_set)}")
print(f"  Prime powers: {sorted(prime_powers)}")
print(f"  Fibonacci: {sorted(fib_set_2_20)}")
print(f"  Catalan: {sorted(catalan_in_range)}")
print(f"  Triangular: {sorted(triangular)}")
print(f"  Bell: {sorted(bell_in_range)}")
print(f"  Binomial C(n,k): {sorted(binom_set)}")
print(f"  Union: {sorted(interesting & set(range(2, 21)))}")
print(f"  Coverage: {len(interesting & set(range(2, 21)))}/{len(range(2, 21))} = "
      f"{len(interesting & set(range(2, 21)))/len(range(2, 21))*100:.1f}%")

not_interesting = set(range(2, 21)) - interesting
print(f"  Not in any family: {sorted(not_interesting)}")

# ── Summary ──────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("SUMMARY")
print("=" * 72)

print(f"""
TASK A: Found {len(counts)} structural counts. 
  Fibonacci counts: {len(fib_counts)} out of {len(counts)}.
  34 appears: {34 in [v for _,v in all_counts]}
  55 appears: {55 in [v for _,v in all_counts]}
  
TASK A.5: Complement involution on 克 cycle restricted to V⁻:
  A⁻ = [[-1/2, -1/2], [-1/2, 0]]
  Char poly of A⁻: x² + x/2 − 1/4
  Char poly of 2A⁻: x² + x − 1  (RECIPROCAL Fibonacci polynomial)
  Eigenvalues: (-1±√5)/4 = φ/2 and -1/(2φ)
  ⟹ Golden ratio DOES appear, but as x² + x − 1 not x² − x − 1.
  The sign flip comes from the directionality of 克.
  
TASK B: Probability of n=3 forcing chain being all-Fibonacci:
  P ≈ {p_joint*100:.4f}%
  This is a SURPRISING coincidence (< 5% threshold).
  Consecutiveness is forced once all-Fibonacci holds in [2,8].
  Ambient density of "interesting" numbers in [2,20]: ~{len(interesting & set(range(2,21)))/19*100:.0f}%.
""")
