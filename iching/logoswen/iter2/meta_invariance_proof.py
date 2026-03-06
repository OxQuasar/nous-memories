"""
Investigate WHY the meta-hexagram walk is invariant across ALL Eulerian paths.

Key observation from thread_ceg_dynamics.py: 
  Every sampled Eulerian path produces EXACTLY the same meta-hexagram statistics.
  26/31 unique, #38 Kui appears 3×, mean weight 3.000, identical meta-sig distribution.

Hypothesis: The meta-hexagram at bridge k = (sig_k, sig_{k+1}) = the edge being traversed.
Since an Eulerian path uses every edge exactly once, the multiset of meta-hexagrams
is just the multiset of edges — invariant across all Eulerian paths.

The only thing that changes is the ORDER, not the CONTENT.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

# Build the multigraph edge list
edge_count = Counter()
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    edge_count[(xor_sig(a), xor_sig(b))] += 1

print("=" * 70)
print("META-HEXAGRAM INVARIANCE: WHY THE META-WALK IS FORCED")
print("=" * 70)

# The meta-hexagram at bridge k stacks sig_k and sig_{k+1}.
# A meta-hexagram = (s1[0],s1[1],s1[2], s2[0],s2[1],s2[2]) 
# This is exactly the EDGE (s1, s2) encoded as a 6-bit string.
#
# An Eulerian path traverses every edge exactly once.
# Therefore: the MULTISET of meta-hexagrams = the MULTISET of edges.
# This is invariant across ALL Eulerian paths. Only the ORDER changes.

print("\nTheorem: The multiset of meta-hexagrams is an invariant of")
print("the orbit multigraph. It does not depend on which Eulerian path")
print("is chosen.")
print()
print("Proof: Meta-hexagram at bridge k = concatenation of edge endpoints.")
print("An Eulerian path traverses each edge exactly once.")
print("Therefore the multiset of meta-hexagrams = multiset of edges. QED.")
print()

# Verify: multiset of meta-hexagrams = multiset of edges
print("Verification: edge multiset = meta-hexagram multiset")
print()

hex_to_kw = {}
for i in range(64):
    hex_to_kw[tuple(M[i])] = KING_WEN[i]

edge_metas = Counter()
for (s1, s2), cnt in edge_count.items():
    meta = (s1[0], s1[1], s1[2], s2[0], s2[1], s2[2])
    edge_metas[meta] += cnt

print(f"{'Edge':>18s}  {'Meta-hex':>10s}  {'Mult':>4s}  {'KW#':>4s}  {'Name':<12s}  {'Meta-sig':>10s}")
print(f"{'─'*18}  {'─'*10}  {'─'*4}  {'─'*4}  {'─'*12}  {'─'*10}")

for meta in sorted(edge_metas.keys()):
    cnt = edge_metas[meta]
    s1 = meta[:3]
    s2 = meta[3:]
    edge_str = f"{ORBIT_NAMES[s1]:>6s}→{ORBIT_NAMES[s2]:<6s}"
    meta_str = ''.join(map(str, meta))
    kw_info = hex_to_kw.get(meta, (None, '???'))
    meta_sig = (meta[0] ^ meta[5], meta[1] ^ meta[4], meta[2] ^ meta[3])
    sig_name = KERNEL_NAMES[meta_sig]
    print(f"  {edge_str}  {meta_str:>10s}  {cnt:>4d}  #{kw_info[0]:>3d}  {kw_info[1]:<12s}  {meta_sig} ({sig_name})")

# Count unique
unique_metas = sum(1 for v in edge_metas.values() if v >= 1)
total_edges = sum(edge_metas.values())
print(f"\nUnique meta-hexagrams: {unique_metas}")
print(f"Total edges (= total meta-hexagrams): {total_edges}")

# Which meta-hexagram repeats?
repeats = {m: c for m, c in edge_metas.items() if c > 1}
print(f"\nRepeating meta-hexagrams:")
for meta, cnt in sorted(repeats.items(), key=lambda x: -x[1]):
    kw_info = hex_to_kw.get(meta, (None, '???'))
    s1, s2 = meta[:3], meta[3:]
    print(f"  {meta} #{kw_info[0]} {kw_info[1]}: {cnt}×")
    # Which edges produce this meta?
    for (e1, e2), ecnt in edge_count.items():
        if (e1[0], e1[1], e1[2], e2[0], e2[1], e2[2]) == meta and ecnt > 0:
            print(f"    {ORBIT_NAMES[e1]}→{ORBIT_NAMES[e2]}: {ecnt}×")

# Why does #38 Kui (110101) appear 3 times?
print(f"\n{'─'*70}")
print("WHY #38 KUI APPEARS 3×")
print(f"{'─'*70}")
kui = (1, 1, 0, 1, 0, 1)
print(f"Kui = {kui}")
print(f"Decomposed: sig1=(1,1,0)={ORBIT_NAMES[(1,1,0)]}, sig2=(1,0,1)={ORBIT_NAMES[(1,0,1)]}")
print(f"Edge: Zhun→Xu")
print(f"Multiplicity in multigraph: {edge_count[((1,1,0),(1,0,1))]}")
print(f"\nKui appears 3× because the Zhun→Xu edge has multiplicity 3.")
print(f"This is the highest-multiplicity edge in the multigraph.")

# What about doubly-repeated meta-hexagrams?
print(f"\n{'─'*70}")
print("DOUBLY-REPEATED META-HEXAGRAMS")
print(f"{'─'*70}")
for meta, cnt in sorted(repeats.items(), key=lambda x: -x[1]):
    if cnt == 2:
        kw_info = hex_to_kw.get(meta, (None, '???'))
        s1, s2 = meta[:3], meta[3:]
        # Find the edges
        edges = []
        for (e1, e2), ecnt in edge_count.items():
            m = (e1[0], e1[1], e1[2], e2[0], e2[1], e2[2])
            if m == meta:
                for _ in range(ecnt):
                    edges.append(f"{ORBIT_NAMES[e1]}→{ORBIT_NAMES[e2]}")
        print(f"  #{kw_info[0]:2d} {kw_info[1]:<12s} = {meta}: {' + '.join(edges)}")

# Now investigate: what DOES vary across Eulerian paths? The ORDER of meta-hexagrams.
print(f"\n{'─'*70}")
print("WHAT VARIES: META-HEXAGRAM ORDER")
print(f"{'─'*70}")
print("The multiset is fixed. The ORDER depends on which Eulerian path is chosen.")
print("This is the sequence of edges traversed, which varies across paths.")
print()
print("The meta-hexagram WALK is a path through a 64-vertex space")
print("where consecutive meta-hexagrams share an endpoint (the intermediate orbit).")
print("Different Eulerian paths produce different orderings of the same 31 meta-hexagrams.")
print()

# Check: does the META-hexagram walk have any additional structure?
# Specifically: consecutive meta-hexagrams share a 3-bit overlap.
# meta[k] = (sig_k, sig_{k+1}), meta[k+1] = (sig_{k+1}, sig_{k+2})
# So they share the middle 3 bits: meta[k][3:6] = meta[k+1][0:3]

import random
from collections import Counter as C

def sample_eulerian_path(edge_count, start, end, rng):
    remaining = dict(edge_count)
    total = sum(edge_count.values())
    adj = defaultdict(list)
    for (u, v) in edge_count:
        if v not in adj[u]:
            adj[u].append(v)
    for u in adj:
        adj[u].sort()
    path = [start]
    def dfs(node, depth):
        if depth == total:
            return node == end
        available = [t for t in adj[node] if remaining.get((node, t), 0) > 0]
        rng.shuffle(available)
        for target in available:
            remaining[(node, target)] -= 1
            path.append(target)
            if dfs(target, depth + 1):
                return True
            path.pop()
            remaining[(node, target)] += 1
        return False
    if dfs(start, 0):
        return list(path)
    return None

# Sample a few paths and check meta-walk ordering diversity
rng = random.Random(42)
meta_orderings = []
for _ in range(100):
    path = sample_eulerian_path(edge_count, (0,0,0), (1,1,1), rng)
    if path:
        metas = []
        for k in range(len(path)-1):
            s1, s2 = path[k], path[k+1]
            metas.append((s1[0],s1[1],s1[2],s2[0],s2[1],s2[2]))
        meta_orderings.append(tuple(metas))

unique_orderings = len(set(meta_orderings))
print(f"Meta-walk orderings sampled: {len(meta_orderings)}")
print(f"Unique orderings: {unique_orderings}")
print(f"All distinct: {unique_orderings == len(meta_orderings)}")

# Check: what properties of the meta-walk ordering DO vary?
# 1. Position of Kui's 3 appearances
# 2. Position of self-loop meta-hexagrams
# 3. Pattern of consecutive meta-signature changes

print(f"\n{'─'*70}")
print("KUI PLACEMENT ACROSS PATHS")
print(f"{'─'*70}")

kui_meta = (1, 1, 0, 1, 0, 1)
kui_positions_all = []
for ordering in meta_orderings:
    positions = [i for i, m in enumerate(ordering) if m == kui_meta]
    kui_positions_all.append(tuple(positions))

kui_pos_freq = C(kui_positions_all)
print(f"Distinct Kui position patterns: {len(kui_pos_freq)}")
print(f"Top 10:")
for pos_pattern, cnt in kui_pos_freq.most_common(10):
    print(f"  {pos_pattern}: {cnt}×")

# KW Kui positions
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))

kw_metas = []
for k in range(31):
    s1, s2 = kw_orbit_walk[k], kw_orbit_walk[k+1]
    kw_metas.append((s1[0],s1[1],s1[2],s2[0],s2[1],s2[2]))

kw_kui_pos = tuple(i for i, m in enumerate(kw_metas) if m == kui_meta)
print(f"\nKW Kui positions: {kw_kui_pos}")
kw_kui_count = kui_pos_freq.get(kw_kui_pos, 0)
print(f"Frequency in sample: {kw_kui_count}/{len(meta_orderings)}")

# Non-overlapping meta-hex analysis: quartets
print(f"\n{'─'*70}")
print("NON-OVERLAPPING META-HEXAGRAM ANALYSIS")
print(f"{'─'*70}")
print("Non-overlapping = every other bridge: B0, B2, B4, ..., B30 (16 total)")

kw_nonoverlap = [kw_metas[2*k] for k in range(16)]
nonoverlap_unique = len(set(kw_nonoverlap))
print(f"KW non-overlapping: {nonoverlap_unique}/16 unique")

# Check if this varies across paths
nonoverlap_uniques = []
for ordering in meta_orderings:
    no = [ordering[2*k] for k in range(16)]
    nonoverlap_uniques.append(len(set(no)))

no_counter = C(nonoverlap_uniques)
print(f"\nNon-overlapping unique count distribution (100 samples):")
for u, cnt in sorted(no_counter.items()):
    print(f"  {u}/16: {cnt}×")


print(f"\n{'='*70}")
print("INVARIANCE ANALYSIS COMPLETE")
print("=" * 70)
