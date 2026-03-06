#!/usr/bin/env python3
"""
Deep analysis of 六合 (Six Harmonies) connectivity structure on trigrams.

The Six Harmonies produced 6 trigram pairs that share ZERO pairs with any
of the 4 known involutions. This means 六合 defines a fundamentally
different connectivity pattern. Analyze what graph it creates.
"""

from itertools import combinations

TRIGRAMS = ['Kun', 'Zhen', 'Gen', 'Dui', 'Kan', 'Li', 'Xun', 'Qian']
BLOCKS = [
    frozenset({'Kun', 'Zhen'}),    # block 0
    frozenset({'Gen', 'Dui'}),     # block 1
    frozenset({'Kan', 'Li'}),      # block 2
    frozenset({'Xun', 'Qian'})     # block 3
]

# All known involution pairs (16 total across 4 involutions)
IOTA1 = {frozenset({'Qian', 'Kun'}), frozenset({'Dui', 'Gen'}),
         frozenset({'Li', 'Kan'}), frozenset({'Xun', 'Zhen'})}
IOTA2 = {frozenset({'Li', 'Kan'}), frozenset({'Kun', 'Gen'}),
         frozenset({'Zhen', 'Dui'}), frozenset({'Xun', 'Qian'})}
IOTA3 = {frozenset({'Kan', 'Qian'}), frozenset({'Kun', 'Dui'}),
         frozenset({'Zhen', 'Gen'}), frozenset({'Xun', 'Li'})}
TAU =   {frozenset({'Kun', 'Zhen'}), frozenset({'Gen', 'Dui'}),
         frozenset({'Kan', 'Li'}), frozenset({'Xun', 'Qian'})}

ALL_INVOLUTION_PAIRS = IOTA1 | IOTA2 | IOTA3 | TAU

# 六合 pairs on trigrams (from the 24 Mountains mapping)
LIUHE_TRIGRAM_PAIRS = [
    (frozenset({'Kan', 'Gen'}), 'Earth'),      # 子丑
    (frozenset({'Gen', 'Qian'}), 'Wood'),       # 寅亥
    (frozenset({'Zhen', 'Qian'}), 'Fire'),      # 卯戌
    (frozenset({'Xun', 'Dui'}), 'Metal'),       # 辰酉
    (frozenset({'Xun', 'Kun'}), 'Water'),       # 巳申
    (frozenset({'Li', 'Kun'}), 'Fire'),          # 午未
]
LIUHE_PAIRS = set(p for p, _ in LIUHE_TRIGRAM_PAIRS)

print("=" * 60)
print("六合 CONNECTIVITY GRAPH ON TRIGRAMS")
print("=" * 60)

# Build adjacency from 六合
adj = {t: set() for t in TRIGRAMS}
for pair, elem in LIUHE_TRIGRAM_PAIRS:
    a, b = list(pair)
    adj[a].add(b)
    adj[b].add(a)

print("\nAdjacency list (六合):")
for t in TRIGRAMS:
    neighbors = sorted(adj[t])
    degree = len(neighbors)
    block = next(i for i, bl in enumerate(BLOCKS) if t in bl)
    print(f"  {t:>5} (block {block}): degree={degree}, neighbors={neighbors}")

print(f"\nTotal edges: {len(LIUHE_PAIRS)}")
print(f"Total possible edges on 8 nodes: {8*7//2} = 28")
print(f"Edges used: {len(LIUHE_PAIRS)}/28")

# Degree sequence
degrees = sorted([len(adj[t]) for t in TRIGRAMS], reverse=True)
print(f"Degree sequence: {degrees}")

# Check bipartiteness
print("\n--- Bipartiteness check ---")
# Try 2-coloring
color = {}
queue = ['Kun']
color['Kun'] = 0
is_bipartite = True
while queue:
    node = queue.pop(0)
    for neighbor in adj[node]:
        if neighbor not in color:
            color[neighbor] = 1 - color[node]
            queue.append(neighbor)
        elif color[neighbor] == color[node]:
            is_bipartite = False

if is_bipartite:
    side0 = sorted([t for t, c in color.items() if c == 0])
    side1 = sorted([t for t, c in color.items() if c == 1])
    print(f"BIPARTITE! Sides: {side0} | {side1}")
    # Check if sides match P+ or P-
    P_PLUS = {'Kan', 'Zhen', 'Dui', 'Li'}
    P_MINUS = {'Kun', 'Gen', 'Qian', 'Xun'}
    if set(side0) == P_PLUS or set(side0) == P_MINUS:
        print("  → Sides match polarity partition P₊/P₋!")
    else:
        print(f"  → Sides do NOT match P₊/P₋")
        print(f"  P₊ = {sorted(P_PLUS)}, P₋ = {sorted(P_MINUS)}")
else:
    print("NOT bipartite (contains odd cycle)")

# Check which edges are CROSS-BLOCK
print("\n--- Block structure of 六合 edges ---")
within_block = 0
cross_block = 0
cross_block_pairs = []
for pair, elem in LIUHE_TRIGRAM_PAIRS:
    a, b = list(pair)
    bl_a = next(i for i, bl in enumerate(BLOCKS) if a in bl)
    bl_b = next(i for i, bl in enumerate(BLOCKS) if b in bl)
    kind = "WITHIN" if bl_a == bl_b else "CROSS"
    if bl_a == bl_b:
        within_block += 1
    else:
        cross_block += 1
        cross_block_pairs.append((pair, elem, bl_a, bl_b))
    print(f"  {a:>5} ↔ {b:<5} ({elem:>5}): block {bl_a}↔{bl_b} = {kind}")

print(f"\nWithin-block: {within_block}, Cross-block: {cross_block}")

# Key observation: ALL 六合 edges are cross-block!
if within_block == 0:
    print("★ ALL 六合 edges are CROSS-BLOCK!")
    print("  This means 六合 exclusively connects elements from DIFFERENT blocks.")
    print("  This is consistent with: 六合 pairs come from adjacent (not opposite)")
    print("  branches, so they connect adjacent (not opposite) trigram sectors.")
    
    # Analyze which block-pairs are connected
    block_connections = {}
    for pair, elem, bl_a, bl_b in cross_block_pairs:
        key = frozenset({bl_a, bl_b})
        block_connections.setdefault(key, []).append((pair, elem))
    
    print("\n  Block-pair connections:")
    for bp, edges in sorted(block_connections.items(), key=lambda x: sorted(x[0])):
        blocks = sorted(bp)
        bl_names = [f"{sorted(BLOCKS[i])}" for i in blocks]
        print(f"    Block {blocks[0]}↔{blocks[1]} ({bl_names[0]} ↔ {bl_names[1]}): {len(edges)} edge(s)")
        for pair, elem in edges:
            a, b = sorted(pair)
            print(f"      {a}↔{b} (→{elem})")

# All 28 possible edges: classify each
print("\n--- Complete edge classification ---")
all_possible = list(combinations(TRIGRAMS, 2))
in_iota1 = set()
in_iota2 = set()
in_iota3 = set()
in_tau = set()
in_liuhe = set()

for a, b in all_possible:
    pair = frozenset({a, b})
    flags = []
    if pair in IOTA1: flags.append('ι₁')
    if pair in IOTA2: flags.append('ι₂')
    if pair in IOTA3: flags.append('ι₃')
    if pair in TAU: flags.append('τ')
    if pair in LIUHE_PAIRS: flags.append('六合')
    
involution_edges = IOTA1 | IOTA2 | IOTA3 | TAU
liuhe_only = LIUHE_PAIRS - involution_edges
involution_only = involution_edges - LIUHE_PAIRS
neither = set(frozenset({a,b}) for a,b in all_possible) - involution_edges - LIUHE_PAIRS

print(f"Edges in known involutions only: {len(involution_only)}")
print(f"Edges in 六合 only: {len(liuhe_only)}")
print(f"Edges in both: {len(involution_edges & LIUHE_PAIRS)}")
print(f"Edges in neither: {len(neither)}")

# Count distinct involution pairs
distinct_inv_pairs = set()
for inv in [IOTA1, IOTA2, IOTA3, TAU]:
    distinct_inv_pairs |= inv
print(f"\nDistinct pairs across all 4 involutions: {len(distinct_inv_pairs)}")
print(f"六合 pairs: {len(LIUHE_PAIRS)}")
print(f"Overlap: {len(distinct_inv_pairs & LIUHE_PAIRS)}")

if len(distinct_inv_pairs & LIUHE_PAIRS) == 0:
    print("\n★★★ ZERO OVERLAP ★★★")
    print("六合 uses EXCLUSIVELY edges that appear in NONE of the 4 known involutions.")
    print("This means the 六合 connectivity graph lives in the COMPLEMENT of the")
    print("involution edge set within the complete graph K₈.")
    
    # How many edges total in involutions?
    print(f"\nThe 4 involutions use {len(distinct_inv_pairs)} of 28 edges.")
    print(f"六合 uses {len(LIUHE_PAIRS)} of the remaining {28-len(distinct_inv_pairs)} edges.")
    print(f"Unclaimed edges: {28 - len(distinct_inv_pairs) - len(LIUHE_PAIRS)}")
    
    # List the unclaimed edges
    remaining = set(frozenset({a,b}) for a,b in all_possible) - distinct_inv_pairs - LIUHE_PAIRS
    print(f"\nEdges in neither involutions nor 六合 ({len(remaining)}):")
    for p in sorted(remaining, key=lambda x: sorted(x)):
        a, b = sorted(p)
        bl_a = next(i for i, bl in enumerate(BLOCKS) if a in bl)
        bl_b = next(i for i, bl in enumerate(BLOCKS) if b in bl)
        print(f"  {a}↔{b} (block {bl_a}↔{bl_b})")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
The 六合 (Six Harmonies) connectivity graph on trigrams:
1. Has 6 edges on 8 nodes
2. ZERO edges overlap with any known involution (ι₁, ι₂, ι₃, τ)
3. ALL edges are cross-block (connect different blocks)
4. The graph is a specific subgraph of the "involution complement"

This means the 28 edges of K₈ partition into:
- 12 edges used by the 4 known involutions (some shared between involutions)
- 6 edges used by 六合 (shared with NO involution)  
- Remaining edges unused by either system

Actually let's count more carefully:
""")

# Careful count: how many DISTINCT edges across all involutions?
all_inv_edges = IOTA1 | IOTA2 | IOTA3 | TAU
print(f"Distinct involution edges: {len(all_inv_edges)}")
print(f"六合 edges: {len(LIUHE_PAIRS)}")
print(f"Overlap: {len(all_inv_edges & LIUHE_PAIRS)}")
print(f"Total distinct edges used: {len(all_inv_edges | LIUHE_PAIRS)}")
print(f"Remaining of 28: {28 - len(all_inv_edges | LIUHE_PAIRS)}")

# Check: do some involution edges overlap?
for name1, inv1 in [('ι₁', IOTA1), ('ι₂', IOTA2), ('ι₃', IOTA3), ('τ', TAU)]:
    for name2, inv2 in [('ι₁', IOTA1), ('ι₂', IOTA2), ('ι₃', IOTA3), ('τ', TAU)]:
        if name1 < name2:
            shared = inv1 & inv2
            if shared:
                print(f"  {name1} ∩ {name2}: {len(shared)} shared: {[set(p) for p in shared]}")
