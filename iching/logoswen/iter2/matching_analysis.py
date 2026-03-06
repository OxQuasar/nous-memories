"""
Deep analysis of the matching structure within orbits.

Key finding from hexagram_completion.py:
- Each orbit has 105 valid perfect matchings (using generator masks)
- KW uses a UNIFORM matching: all 4 pairs in each orbit use the SAME generator
- Is uniform matching special? How many of the 105 are uniform?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
from math import comb

DIMS = 6
M = all_bits()

MASK_NAMES = {
    (0,0,0,0,0,0): 'id', (1,0,0,0,0,1): 'O', (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I', (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI', (1,1,1,1,1,1): 'OMI',
}

GEN_FLIPS = {'O': [0, 5], 'M': [1, 4], 'I': [2, 3]}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def apply_gens(h, gens):
    h = list(h)
    for g in gens:
        for idx in GEN_FLIPS[g]:
            h[idx] = 1 - h[idx]
    return tuple(h)

# Build orbits
GROUP = [frozenset(), frozenset({'O'}), frozenset({'M'}), frozenset({'I'}),
         frozenset({'O','M'}), frozenset({'O','I'}), frozenset({'M','I'}),
         frozenset({'O','M','I'})]

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

# Build one orbit to analyze (all orbits are isomorphic as Q₃)
seen = set()
orbits = {}
for i in range(64):
    h = tuple(M[i])
    if h in seen:
        continue
    sig = xor_sig(h)
    orbit = {}
    for g in GROUP:
        gh = apply_gens(h, g)
        for j in range(64):
            if tuple(M[j]) == gh:
                orbit[gh] = j
                seen.add(gh)
                break
    orbits[sig] = orbit

# Analyze matching structure for one orbit (say Qian)
sig = (0,0,0)
hexes = sorted(orbits[sig].keys())
n = 8

print(f"Orbit {ORBIT_NAMES[sig]}: {[orbits[sig][h]+1 for h in hexes]}")

# All valid pairs
valid_pairs = []
for i in range(n):
    for j in range(i+1, n):
        xor = tuple(hexes[i][d] ^ hexes[j][d] for d in range(DIMS))
        if xor in MASK_NAMES:
            valid_pairs.append((i, j, MASK_NAMES[xor]))

print(f"\nValid pairs: {len(valid_pairs)}")
for i, j, mask in valid_pairs:
    print(f"  ({hexes[i]}, {hexes[j]}): {mask}")

# Enumerate all perfect matchings
matchings = []
def find_matchings(remaining, current):
    if not remaining:
        matchings.append(list(current))
        return
    v = min(remaining)
    for i, j, mask in valid_pairs:
        if i == v and j in remaining:
            find_matchings(remaining - {i, j}, current + [(i, j, mask)])

find_matchings(set(range(n)), [])
print(f"\nTotal perfect matchings: {len(matchings)}")

# Classify matchings by mask signature
mask_sig_counter = Counter()
uniform_matchings = []
for matching in matchings:
    masks = tuple(sorted(m[2] for m in matching))
    mask_sig_counter[masks] += 1
    if len(set(m[2] for m in matching)) == 1:
        uniform_matchings.append(matching)

print(f"\nUniform matchings (all same mask): {len(uniform_matchings)}")
for m in uniform_matchings:
    masks = [m_[2] for m_ in m]
    print(f"  {masks}")

print(f"\nDistinct mask signatures: {len(mask_sig_counter)}")
print("Top 10:")
for masks, cnt in mask_sig_counter.most_common(10):
    print(f"  {masks}: {cnt}×")

# How many matchings use exactly one mask type?
single_mask = sum(cnt for masks, cnt in mask_sig_counter.items() 
                  if len(set(masks)) == 1)
print(f"\nMatchings using a single mask type: {single_mask}")

# How many matchings use exactly 2 mask types?
two_masks = sum(cnt for masks, cnt in mask_sig_counter.items() 
                if len(set(masks)) == 2)
print(f"Matchings using exactly 2 mask types: {two_masks}")

three_masks = sum(cnt for masks, cnt in mask_sig_counter.items() 
                  if len(set(masks)) == 3)
print(f"Matchings using exactly 3 mask types: {three_masks}")

four_masks = sum(cnt for masks, cnt in mask_sig_counter.items() 
                 if len(set(masks)) == 4)
print(f"Matchings using exactly 4 mask types: {four_masks}")

# The Q₃ cube has 12 edges: 4 per generator (O, M, I)
# The generators partition the edges into 3 parallel classes of 4 edges each
# But we have 8 mask types, not 3! 
# That's because OM, OI, MI, OMI also connect hexagrams within the orbit
# (they are compound generators — face diagonals and body diagonals of Q₃)

# Count edges per mask type
edge_by_mask = Counter()
for i, j, mask in valid_pairs:
    edge_by_mask[mask] += 1

print(f"\nEdges per mask type (in Q₃):")
for mask in sorted(edge_by_mask.keys()):
    print(f"  {mask:>4s}: {edge_by_mask[mask]} edges")

# The Q₃ has 12 edges at Hamming distance 2 (single generator: O, M, I)
# Plus 12 edges at Hamming distance 4 (double generator: OM, OI, MI)  
# Plus 4 edges at Hamming distance 6 (triple generator: OMI)
# Total: 28 edges = C(8,2)
# All pairs are valid! (Every pair of hexagrams in an orbit differs by a generator)

# How many of the 105 matchings are achievable by selecting from 
# each of the 7 non-identity generator types?
# Each type has a fixed number of edges:
# O, M, I: 4 each (these form a perfect matching by themselves!)
# OM, OI, MI: 4 each (these also form perfect matchings!)
# OMI: 4 edges, but 4 edges on 8 vertices = only a matching if no vertex reuse
# = perfect matching iff the 4 edges form a matching

# Check: for each mask type with 4 edges, do they form a perfect matching?
for mask_name in ['O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI', 'id']:
    edges = [(i, j) for i, j, m in valid_pairs if m == mask_name]
    if not edges:
        continue
    verts = set()
    is_matching = True
    for i, j in edges:
        if i in verts or j in verts:
            is_matching = False
            break
        verts.add(i)
        verts.add(j)
    covers_all = len(verts) == 8
    print(f"  {mask_name:>4s}: {len(edges)} edges, perfect matching: {is_matching and covers_all}")

# So EVERY generator type gives exactly one perfect matching!
# The 7 uniform matchings + their mixes give 105 total.

# Mathematical explanation: Q₃ has 3 generators, each partitioning into 4 parallel edges.
# The 7 non-identity elements of Z₂³ each define a fixed-point-free involution,
# which is always a perfect matching. There are C(7,4)/something = 105 total matchings.

# Actually 105 = C(7,2)*3 = ... let me think.
# The perfect matchings of K_{4,4} (complete bipartite on 4+4) = 4! = 24
# But our graph is complete K_8 restricted to Z₂³ distances... 
# Actually our graph is the complete graph on 8 vertices (all pairs valid).
# Perfect matchings of K_8 = (8-1)!! = 7!! = 7*5*3*1 = 105. Yes!

print(f"\n(8-1)!! = 7!! = {7*5*3*1}")
print("Every pair of hexagrams in an orbit is related by a unique generator.")
print("So: perfect matchings of orbit = perfect matchings of K_8 = 7!! = 105.")
print("The matching is completely determined by the partition into pairs,")
print("and the mask of each pair is forced by which hexagrams are paired.")
print()
print("KW's choice: all 4 pairs use the SAME mask. This is 1 of 7 uniform matchings.")
print(f"KW uniform matching probability: 7/105 = 1/15 per orbit")
print(f"  For all 8 orbits independently: (1/15)^8 = {(1/15)**8:.2e}")
print(f"  But each orbit has a DIFFERENT uniform mask in KW!")

# What uniform mask does KW use per orbit?
print(f"\nKW uniform masks per orbit:")
kw_pairs = []
for k in range(32):
    a = tuple(M[2*k])
    b = tuple(M[2*k+1])
    xor = tuple(a[i] ^ b[i] for i in range(DIMS))
    sig = xor_sig(a)
    kw_pairs.append({'a': a, 'b': b, 'mask': MASK_NAMES[xor], 'orbit': sig})

orbit_masks = defaultdict(list)
for p in kw_pairs:
    orbit_masks[p['orbit']].append(p['mask'])

for sig in sorted(orbit_masks.keys()):
    masks = orbit_masks[sig]
    uniform = len(set(masks)) == 1
    print(f"  {ORBIT_NAMES[sig]:>6s}: {masks}  {'UNIFORM' if uniform else 'MIXED'}")

# Count uniform matchings where EACH orbit uses a DIFFERENT mask
# There are 7 masks and 8 orbits. By pigeonhole, at least 2 orbits must share a mask.
# KW: Qian=OMI, XChu=I, Shi=M, WWang=MI, Bo=O, Xu=OI, Zhun=OM, Tai=OMI
# Qian and Tai both use OMI!
# So KW uses 7 distinct masks across 8 orbits, with exactly one repeat (OMI).

# How many ways to assign uniform masks to 8 orbits using 7 mask types?
# = 7^8 total uniform assignments
# How many have all-distinct? Impossible (7 masks, 8 orbits).
# How many have exactly one repeat? = C(7,1) * C(8,2) * 7! / ... 
# Actually: choose which mask repeats (7), choose which 2 orbits get it (C(8,2)=28),
# distribute remaining 6 masks to 6 orbits (6!).
# = 7 * 28 * 720 = 141120

one_repeat = 7 * 28 * 720
total_uniform = 7**8
print(f"\nTotal uniform assignments: {total_uniform}")
print(f"With exactly one repeat: {one_repeat}")
print(f"Fraction with one repeat: {one_repeat/total_uniform:.4f}")

# But KW specifically uses OMI for both Qian and Tai (the endpoints!)
# How likely is that?
# Given one repeat: prob that it's OMI = 1/7
# Given the repeated mask is OMI: prob that Qian and Tai are the pair = 1/C(8,2) = 1/28
# Overall: 1/7 * 1/28 * 141120 / total_uniform ... hmm, just count directly:
# Fix OMI for Qian and Tai. Remaining 6 orbits get 6 distinct masks from {O,M,I,OM,OI,MI}.
# = 6! = 720 ways.
# Total probability among uniform assignments = 720 / 7^8
print(f"\nProbability that KW's specific mask assignment occurs")
print(f"  (among all uniform assignments): {720/total_uniform:.6f}")
print(f"  = 720 / {total_uniform} = 1 / {total_uniform/720:.0f}")
