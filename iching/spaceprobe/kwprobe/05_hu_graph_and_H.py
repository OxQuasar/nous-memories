"""
Probe the 互 graph structure and interaction with H subgroup.

Key mechanism found: interface lines determine basin via:
  (0,0) → (0,0) fixed → Kun
  (1,1) → (1,1) fixed → Qian
  (0,1) ↔ (1,0) swap → KanLi oscillation

Questions:
1. The 16-vertex 互 graph — what is its structure?
2. How does the H subgroup interact with basins?
3. The depth-1 cluster at #37-40 — what's special?
4. The 互 walk along the KW sequence — graph-theoretic view
5. Does basin structure predict any kernel metric behavior?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, reverse6,
    hamming6, fmt6, fmt3,
)

# Build KW sequence
kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    elif b2 == 1 and b3 == 1: return 'Qian'
    else: return 'KanLi'

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

# All 16 互 values
hu_values = sorted(set(hugua(h) for h in range(64)))

# ══════════════════════════════════════════════════════════════════════════════
# 1. THE 互→互 GRAPH (16 vertices, directed)
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. THE 互 GRAPH — 16 VERTICES, DIRECTED")
print("=" * 70)

print(f"\n  Each 互 value maps to another 互 value under 互:")
hu_graph = {}
for hv in hu_values:
    target = hugua(hv)
    lo, up = lower_trigram(hv), upper_trigram(hv)
    t_lo, t_up = lower_trigram(target), upper_trigram(target)
    basin = get_basin(hv)
    hu_graph[hv] = target
    print(f"    {fmt6(hv)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]:4s}) → "
          f"{fmt6(target)} ({TRIGRAM_NAMES[t_lo]}/{TRIGRAM_NAMES[t_up]:4s}) "
          f"[{basin}]")

# Graph structure
print(f"\n  Graph components:")
# Find connected components (treating as undirected for structure)
visited = set()
components = []
for hv in hu_values:
    if hv in visited:
        continue
    component = set()
    stack = [hv]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        component.add(v)
        # Forward edge
        if hu_graph[v] not in visited:
            stack.append(hu_graph[v])
        # Backward edges
        for hv2 in hu_values:
            if hu_graph[hv2] == v and hv2 not in visited:
                stack.append(hv2)
    components.append(component)

for i, comp in enumerate(components):
    basins = set(get_basin(v) for v in comp)
    members = [(fmt6(v), get_basin(v)) for v in sorted(comp)]
    print(f"\n    Component {i+1} ({len(comp)} vertices, basins={basins}):")
    for name, basin in members:
        target = hu_graph[int(name, 2)]
        print(f"      {name} [{basin:6s}] → {fmt6(target)}")

# Fixed points and cycles
print(f"\n  Fixed points: {[fmt6(v) for v in hu_values if hu_graph[v] == v]}")
cycles = []
for hv in hu_values:
    if hu_graph[hv] != hv and hu_graph[hu_graph[hv]] == hv:
        pair = tuple(sorted([hv, hu_graph[hv]]))
        if pair not in cycles:
            cycles.append(pair)
print(f"  2-cycles: {[(fmt6(a), fmt6(b)) for a, b in cycles]}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. THE 互 GRAPH STRUCTURE — TREES TO ATTRACTORS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. 互 GRAPH AS TREES TO ATTRACTORS")
print("=" * 70)

# Each vertex either IS an attractor or has a path to one.
# Draw the tree structure.

print(f"\n  Kun tree (fixed point 000000):")
print(f"    000000 ← 000001")
print(f"    000000 ← 100000")
print(f"    000000 ← 100001")

print(f"\n  Qian tree (fixed point 111111):")
print(f"    111111 ← 011110")
print(f"    111111 ← 011111")
print(f"    111111 ← 111110")

print(f"\n  KanLi cycle (010101 ↔ 101010):")
# Which 互 values map to 010101?
to_weiji = [v for v in hu_values if hu_graph[v] == 0b010101]
to_jiji = [v for v in hu_values if hu_graph[v] == 0b101010]
print(f"    → 010101 (WeiJi): {[fmt6(v) for v in to_weiji]}")
print(f"    → 101010 (JiJi):  {[fmt6(v) for v in to_jiji]}")

# Full tree visualization
print(f"\n  Complete convergence structure:")
for attractor_name, attractor, feeders in [
    ("Kun (000000)", 0b000000, [v for v in hu_values if hu_graph[v] == 0b000000 and v != 0b000000]),
    ("Qian (111111)", 0b111111, [v for v in hu_values if hu_graph[v] == 0b111111 and v != 0b111111]),
    ("WeiJi (010101)", 0b010101, [v for v in hu_values if hu_graph[v] == 0b010101 and v != 0b101010]),
    ("JiJi (101010)", 0b101010, [v for v in hu_values if hu_graph[v] == 0b101010 and v != 0b010101]),
]:
    print(f"\n    {attractor_name}:")
    print(f"      ← {', '.join(fmt6(v) for v in feeders)}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. H SUBGROUP AND BASINS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. H SUBGROUP AND BASIN INTERACTION")
print("=" * 70)

# H = {id, O, MI, OMI} acts on kernel space
# Does H have a relationship with basins?

# For each bridge in the KW sequence, what's the kernel and what are the basins?
print(f"\n  H-kernel bridges and basin transitions:")
h_basin_trans = defaultdict(Counter)
non_h_basin_trans = defaultdict(Counter)

for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    in_h = kernel in H_KERNELS
    
    b1, b2 = get_basin(h1), get_basin(h2)
    trans = (b1, b2)
    
    if in_h:
        h_basin_trans[kernel_names[kernel]][trans] += 1
    else:
        non_h_basin_trans[kernel_names[kernel]][trans] += 1

print(f"\n  H-kernel bridges:")
for k in ['id', 'O', 'MI', 'OMI']:
    if k in h_basin_trans:
        print(f"    {k:3s}: {dict(h_basin_trans[k])}")

print(f"\n  Non-H-kernel bridges:")
for k in ['M', 'I', 'OM', 'OI']:
    if k in non_h_basin_trans:
        print(f"    {k:3s}: {dict(non_h_basin_trans[k])}")

# Key question: does H preserve basins?
# H kernel components:
# id: no change → same basin
# O: flips bits 0↔5 → interface bits 2,3 unchanged → same basin
# MI: flips bits 1↔4 AND bit 2↔3 → interface (b2,b3) → (b3,b2)
#     (0,0)→(0,0), (1,1)→(1,1), (0,1)→(1,0) → same basin!
# OMI: flips bits 0↔5, 1↔4, 2↔3 → interface (b2,b3) → (b3,b2) → same basin!

print(f"\n  THEORETICAL: How do kernel operations affect the interface (bits 2,3)?")
for k_name, k_val in [('id', (0,0,0)), ('O', (1,0,0)), ('M', (0,1,0)), ('I', (0,0,1)),
                        ('OM', (1,1,0)), ('OI', (1,0,1)), ('MI', (0,1,1)), ('OMI', (1,1,1))]:
    # The kernel (o,m,i) means:
    # o=1: bits 0,5 flipped (outer pair)
    # m=1: bits 1,4 flipped (middle pair) 
    # i=1: bits 2,3 flipped (inner pair)
    # But wait — the mirror kernel definition:
    # kernel = (bits[0]^bits[5], bits[1]^bits[4], bits[2]^bits[3])
    # So kernel (o,m,i) tells us which PAIRS changed.
    # i=1 means bit2 and bit3 changed TOGETHER (both flipped) or OPPOSITELY?
    
    # Actually: the kernel records XOR of symmetric pairs.
    # kernel[2] = bit2 XOR bit3 of the XOR
    # XOR bit2 = h1_bit2 XOR h2_bit2
    # XOR bit3 = h1_bit3 XOR h2_bit3
    # kernel[2] = (h1_bit2 XOR h2_bit2) XOR (h1_bit3 XOR h2_bit3)
    
    # So kernel[2]=0 means: bit2 and bit3 changed the same way (both flipped or both not)
    # kernel[2]=1 means: bit2 and bit3 changed differently (one flipped, other not)
    
    o, m, i = k_val
    in_h = k_val in H_KERNELS
    
    # Effect on interface:
    # The XOR has 6 bits. The interface bits of XOR are bits 2,3.
    # We need to think about what the kernel tells us about bits 2,3 of the XOR.
    
    # Actually, the XOR between h1 and h2 directly tells us which bits changed.
    # The kernel compresses: kernel[j] = xor_bit[j] XOR xor_bit[5-j]
    # For j=2: kernel[2] = xor_bit[2] XOR xor_bit[3]
    
    # So kernel[2]=0: either both bits 2,3 flipped, or neither did
    # kernel[2]=1: exactly one of bits 2,3 flipped
    
    # Basin effect:
    # If neither bit 2,3 changed: interface unchanged → same basin
    # If both bits 2,3 changed: (b2,b3) → (1-b2, 1-b3)
    #   (0,0)→(1,1): Kun→Qian
    #   (1,1)→(0,0): Qian→Kun
    #   (0,1)→(1,0): KanLi→KanLi
    # If exactly one changed: (b2,b3) → mixed change
    #   (0,0)→(0,1) or (1,0): Kun→KanLi
    #   (1,1)→(0,1) or (1,0): Qian→KanLi
    #   (0,1)→(0,0) or (1,1): KanLi→Kun or Qian
    #   (1,0)→(0,0) or (1,1): KanLi→Kun or Qian
    
    if i == 0:
        effect = "interface unchanged OR both flipped → {same basin} or {Kun↔Qian, KanLi→KanLi}"
    else:
        effect = "exactly one interface bit flipped → {Kun→KanLi, Qian→KanLi, KanLi→Kun/Qian}"
    
    h_tag = " [H]" if in_h else "     "
    print(f"    {k_name:3s}{h_tag}: kernel_i={i} → {effect}")

# Wait, I need to be more precise. kernel[2] = xor_bit2 XOR xor_bit3
# This doesn't tell us the individual values, just their XOR.
# H has kernel_i = 0 (for id, O) and kernel_i = 1 (for MI, OMI)

# Let's just empirically check: for H bridges, does basin change?
print(f"\n  Empirical: H bridges and basin preservation:")
h_preserves = 0
h_crosses = 0
non_h_preserves = 0
non_h_crosses = 0

for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    in_h = kernel in H_KERNELS
    
    b1, b2 = get_basin(h1), get_basin(h2)
    same = (b1 == b2)
    
    if in_h:
        if same: h_preserves += 1
        else: h_crosses += 1
    else:
        if same: non_h_preserves += 1
        else: non_h_crosses += 1

print(f"    H bridges: {h_preserves} preserve, {h_crosses} cross ({h_preserves+h_crosses} total)")
print(f"    non-H bridges: {non_h_preserves} preserve, {non_h_crosses} cross ({non_h_preserves+non_h_crosses} total)")

# More detailed: which specific transitions?
print(f"\n  H bridge basin transitions (detailed):")
for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    if kernel not in H_KERNELS:
        continue
    b1, b2 = get_basin(h1), get_basin(h2)
    if b1 != b2:
        k_name = kernel_names[kernel]
        # What actually happened to bits 2,3?
        xor_b2 = (xor >> 2) & 1
        xor_b3 = (xor >> 3) & 1
        print(f"    Step {i+1}→{i+2}: {kw_names[i]:12s}({b1}) → {kw_names[i+1]:12s}({b2}) "
              f"kernel={k_name} xor_bits23=({xor_b2},{xor_b3})")

# ══════════════════════════════════════════════════════════════════════════════
# 4. KERNEL I-COMPONENT AND BASIN CROSSING
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. THE I-COMPONENT OF THE KERNEL CONTROLS BASIN CROSSING")
print("=" * 70)

# The kernel's third component (I) = bit2_xor XOR bit3_xor
# I=0: bits 2,3 change together → can swap Kun↔Qian or stay
# I=1: bits 2,3 change differently → must cross to/from KanLi

# But within I=0, we need to know if BOTH changed or NEITHER changed
# That depends on the actual XOR bits, not just the kernel.

# Let's classify ALL 63 bridges by what happens to interface bits
print(f"\n  Interface (bits 2,3) change classification:")
interface_changes = Counter()
for i in range(63):
    xor = kw_hex[i] ^ kw_hex[i+1]
    xor_b2 = (xor >> 2) & 1
    xor_b3 = (xor >> 3) & 1
    
    change_type = f"({xor_b2},{xor_b3})"
    b1, b2 = get_basin(kw_hex[i]), get_basin(kw_hex[i+1])
    interface_changes[(change_type, b1, b2)] += 1

print(f"\n  XOR(bit2,bit3) | basin_from → basin_to | count")
for (change, b1, b2), count in sorted(interface_changes.items()):
    print(f"    {change:7s}  {b1:6s} → {b2:6s}: {count}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. WHAT'S SPECIAL ABOUT THE DEPTH-1 CLUSTER (#37-40)?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. THE DEPTH-1 CLUSTER: #37-40 (JIA REN, KUI, JIAN, XIE)")
print("=" * 70)

cluster = [(36, 37), (37, 38), (38, 39)]  # 0-indexed pairs for transitions
for i in range(36, 40):
    h = kw_hex[i]
    hu = hugua(h)
    lo, up = lower_trigram(h), upper_trigram(h)
    hu_lo, hu_up = lower_trigram(hu), upper_trigram(hu)
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    
    print(f"    #{i+1:2d} {kw_names[i]:12s} = {fmt6(h)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}) "
          f"interface=({b2},{b3}) → 互={fmt6(hu)} ({TRIGRAM_NAMES[hu_lo]}/{TRIGRAM_NAMES[hu_up]})")

print(f"\n  These are the only consecutive run of 4+ depth-1 KanLi hexagrams.")
print(f"  Their 互 values are exactly JiJi and WeiJi — the cycle points themselves!")
print(f"  They are the hexagrams whose nuclear IS the Water↔Fire axis.")

# What trigram pairs produce depth-1 KanLi?
# Need: 互(h) ∈ {JiJi, WeiJi} = {010101, 101010}
# 互(h) = 010101 means inner bits map to WeiJi pattern
# 互(h) = 101010 means inner bits map to JiJi pattern

d1_kanli = [h for h in range(64) if hugua(h) in (0b010101, 0b101010)]
print(f"\n  All hexagrams whose 互 IS JiJi or WeiJi ({len(d1_kanli)} total):")
for h in d1_kanli:
    lo, up = lower_trigram(h), upper_trigram(h)
    hu = hugua(h)
    kw_pos = kw_hex.index(h) + 1
    print(f"    {fmt6(h)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}) KW#{kw_pos:2d} "
          f"互={'JiJi' if hu == 0b101010 else 'WeiJi'}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. THE 互 WALK AS GRAPH TRAVERSAL
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. THE 互 WALK ON THE 16-VERTEX GRAPH")
print("=" * 70)

# The KW sequence induces a walk on the 16 互 values.
# What edges does this walk use?

hu_seq = [hugua(kw_hex[i]) for i in range(64)]

# Edges used (directed)
edges_used = Counter()
for i in range(63):
    if hu_seq[i] != hu_seq[i+1]:
        edge = (hu_seq[i], hu_seq[i+1])
        edges_used[edge] += 1

print(f"\n  Edges used by KW 互-walk: {len(edges_used)} directed edges")
print(f"  (Out of {16*15} possible = {16*15})")

# Edge usage distribution
print(f"\n  Edge frequency distribution:")
for count in sorted(set(edges_used.values())):
    n = sum(1 for v in edges_used.values() if v == count)
    print(f"    Used {count} time(s): {n} edges")

# Most used edges
print(f"\n  Most traversed edges:")
for edge, count in sorted(edges_used.items(), key=lambda x: -x[1])[:10]:
    lo1, up1 = lower_trigram(edge[0]), upper_trigram(edge[0])
    lo2, up2 = lower_trigram(edge[1]), upper_trigram(edge[1])
    b1, b2 = get_basin(edge[0]), get_basin(edge[1])
    print(f"    {TRIGRAM_NAMES[lo1]}/{TRIGRAM_NAMES[up1]:4s} → "
          f"{TRIGRAM_NAMES[lo2]}/{TRIGRAM_NAMES[up2]:4s} ({b1}→{b2}): {count}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE 8 SELF-REVERSE HEXAGRAMS — STRUCTURAL ROLE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. THE 8 SELF-REVERSE HEXAGRAMS AS SEQUENCE SKELETON")
print("=" * 70)

self_rev = sorted([h for h in range(64) if reverse6(h) == h])
sr_positions = sorted([kw_hex.index(h) + 1 for h in self_rev])
print(f"\n  Self-reverse hexagram KW positions: {sr_positions}")

# These form 4 complement pairs. Their positions in the sequence:
sr_pairs = []
for h in self_rev:
    comp = h ^ MASK_ALL
    if h < comp:
        pos_h = kw_hex.index(h) + 1
        pos_c = kw_hex.index(comp) + 1
        sr_pairs.append((min(pos_h, pos_c), max(pos_h, pos_c)))

print(f"  Self-reverse complement pairs (KW positions):")
for p1, p2 in sorted(sr_pairs):
    h1 = kw_hex[p1-1]
    h2 = kw_hex[p2-1]
    print(f"    #{p1}-#{p2}: {kw_names[p1-1]}/{kw_names[p2-1]} "
          f"({get_basin(h1)}/{get_basin(h2)})")

# They divide the sequence into segments
boundaries = sorted(set([p for pair in sr_pairs for p in pair]))
print(f"\n  Boundary positions: {boundaries}")
print(f"  Segments between boundaries:")
all_boundaries = [0] + boundaries + [65]
for i in range(len(all_boundaries) - 1):
    start = all_boundaries[i] + 1
    end = all_boundaries[i+1] - 1
    if start > end:
        continue
    segment_basins = Counter(get_basin(kw_hex[j-1]) for j in range(start, end+1))
    segment_names = [kw_names[j-1] for j in range(start, end+1)]
    n = end - start + 1
    print(f"    #{start:2d}-#{end:2d} ({n:2d} hex): "
          f"Kun={segment_basins.get('Kun',0):2d} KanLi={segment_basins.get('KanLi',0):2d} "
          f"Qian={segment_basins.get('Qian',0):2d}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. BASIN AND TRADITIONAL INTERPRETIVE CATEGORIES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. BASIN AND TRADITIONAL GROUPINGS")
print("=" * 70)

# The 8 palaces (八宫) — each trigram's "family" of 8 hexagrams
# Palace = grouped by lower trigram in traditional arrangement
# But let's check: do trigram families have uniform basin?

print(f"\n  Lower trigram → basin distribution:")
for t in range(8):
    hexes = [h for h in range(64) if lower_trigram(h) == t]
    basins = Counter(get_basin(h) for h in hexes)
    print(f"    {TRIGRAM_NAMES[t]:4s} (bottom={fmt3(t)}): "
          f"Kun={basins.get('Kun',0)} KanLi={basins.get('KanLi',0)} Qian={basins.get('Qian',0)}")

print(f"\n  Upper trigram → basin distribution:")
for t in range(8):
    hexes = [h for h in range(64) if upper_trigram(h) == t]
    basins = Counter(get_basin(h) for h in hexes)
    print(f"    {TRIGRAM_NAMES[t]:4s} (bottom_bit={(t>>0)&1}): "
          f"Kun={basins.get('Kun',0)} KanLi={basins.get('KanLi',0)} Qian={basins.get('Qian',0)}")

# Check: does the top bit of lower trigram alone determine half the basin?
print(f"\n  Top bit of lower trigram (bit 2) and bottom bit of upper trigram (bit 3):")
print(f"  These are exactly the interface lines!")
print(f"  Lower trigrams with top bit 0: {[TRIGRAM_NAMES[t] for t in range(8) if (t>>2)&1 == 0]}")
print(f"  Lower trigrams with top bit 1: {[TRIGRAM_NAMES[t] for t in range(8) if (t>>2)&1 == 1]}")
print(f"  Upper trigrams with bottom bit 0: {[TRIGRAM_NAMES[t] for t in range(8) if (t>>0)&1 == 0]}")
print(f"  Upper trigrams with bottom bit 1: {[TRIGRAM_NAMES[t] for t in range(8) if (t>>0)&1 == 1]}")

# This gives us the trigram classification for basins:
print(f"\n  BASIN RULE IN TRIGRAM LANGUAGE:")
print(f"  Kun basin: lower ∈ {{Kun,Gen,Kan,Xun}} AND upper ∈ {{Kun,Kan,Zhen,Dui}}")
print(f"  Qian basin: lower ∈ {{Zhen,Li,Dui,Qian}} AND upper ∈ {{Gen,Xun,Li,Qian}}")
print(f"  KanLi basin: mixed (one from each group)")

# The groups:
# Lower top=0: Kun(000), Gen(001), Kan(010), Xun(011) — the "yin-topped" trigrams
# Lower top=1: Zhen(100), Li(101), Dui(110), Qian(111) — the "yang-topped" trigrams
# Upper bot=0: Kun(000), Kan(010), Zhen(100), Dui(110) — the "yin-based" trigrams
# Upper bot=1: Gen(001), Xun(011), Li(101), Qian(111) — the "yang-based" trigrams

# This is a beautiful correspondence with the Later Heaven arrangement!
# Yin-topped = inner/yin essence, Yang-topped = outer/yang essence

# ══════════════════════════════════════════════════════════════════════════════
# 9. TRIGRAM GROUPS AND POLARITY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. TRIGRAM GROUPS — THE INTERFACE POLARITY")
print("=" * 70)

# The interface classifies trigrams into two groups by one bit:
# Lower trigram: classified by top line (bit 2)
# Upper trigram: classified by bottom line (bit 0 of the trigram = bit 3 of hex)

# Group A (yin interface contribution): 
#   Lower: top=0 (Kun, Gen, Kan, Xun)
#   Upper: bottom=0 (Kun, Kan, Zhen, Dui)

# Group B (yang interface contribution):
#   Lower: top=1 (Zhen, Li, Dui, Qian)
#   Upper: bottom=1 (Gen, Xun, Li, Qian)

# Check if these groups have any traditional significance
# Note: the lower group A has trigrams whose "facing line" (toward the interface) is yin
# and the upper group A has trigrams whose "facing line" is yin.

# This is exactly the line that faces the OTHER trigram!
# Lower trigram's top line faces upper, upper trigram's bottom line faces lower.

print(f"\n  The interface line is the 'facing line' — the line each trigram")
print(f"  presents to the other.")
print(f"\n  Lower trigram facing yin (○): Kun ☷, Gen ☶, Kan ☵, Xun ☴")
print(f"  Lower trigram facing yang (●): Zhen ☳, Li ☲, Dui ☱, Qian ☰")
print(f"\n  Upper trigram facing yin (○): Kun ☷, Kan ☵, Zhen ☳, Dui ☱")
print(f"  Upper trigram facing yang (●): Gen ☶, Xun ☴, Li ☲, Qian ☰")

# Check: these groups align with yin/yang classification?
# Traditional: Qian, Zhen, Kan, Gen = yang trigrams
#              Kun, Xun, Li, Dui = yin trigrams
# Our groups are different! They're based on the facing line, not overall nature.

print(f"\n  Compare with traditional yin/yang classification:")
print(f"  Traditional yang: Qian, Zhen, Kan, Gen (odd number of yang lines)")
print(f"  Traditional yin:  Kun, Xun, Li, Dui (even number of yang lines)")
print(f"\n  Facing-line groups (ours) vs Traditional:")
print(f"    Lower facing yin: Kun(yin), Gen(yang), Kan(yang), Xun(yin) — 2 match")
print(f"    Lower facing yang: Zhen(yang), Li(yin), Dui(yin), Qian(yang) — 2 match")
print(f"    → No correlation! The facing line is orthogonal to traditional yin/yang.")

# But check Lo Shu numbers
# Traditional Lo Shu: Kan=1, Kun=2, Zhen=3, Xun=4, center=5, Qian=6, Dui=7, Gen=8, Li=9
# Check parity of Lo Shu number vs facing line

print(f"\n  Lo Shu numbers and facing lines:")
loshu = {0b010: 1, 0b000: 2, 0b100: 3, 0b011: 4, 0b111: 6, 0b110: 7, 0b001: 8, 0b101: 9}
for t in range(8):
    top_bit = (t >> 2) & 1  # facing line as lower trigram
    bot_bit = t & 1  # facing line as upper trigram
    ls = loshu.get(t, '?')
    print(f"    {TRIGRAM_NAMES[t]:4s}: Lo Shu={ls}, "
          f"facing_as_lower={'●' if top_bit else '○'}, "
          f"facing_as_upper={'●' if bot_bit else '○'}")

# ══════════════════════════════════════════════════════════════════════════════
# 10. THE BASIN PATTERN IN TERMS OF FACING LINES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. THE BASIN IN TERMS OF FACING LINES")
print("=" * 70)

print(f"""
  BASIN = agreement/disagreement of facing lines:
  
  Both face yin  (○○) → Kun basin (receptive meeting)    → dissolves
  Both face yang (●●) → Qian basin (active meeting)      → consolidates  
  One each       (○● or ●○) → KanLi basin (tension)     → oscillates
  
  This is the POLARITY OF THE ENCOUNTER between upper and lower trigrams.
  
  Same-polarity encounters resolve (to their shared type).
  Cross-polarity encounters persist as irreducible tension.
  
  The Kan↔Li oscillation is what happens when yin meets yang directly.
  It cannot resolve. It can only alternate.
""")

# Final summary: the 64 hexagrams partition by meeting type
for meeting in ['○○ (Kun)', '●● (Qian)', '○● (KanLi)', '●○ (KanLi)']:
    interface = meeting[:2]
    b2 = 0 if interface[0] == '○' else 1
    b3 = 0 if interface[1] == '○' else 1
    
    hexes_in = []
    for h in range(64):
        if (h >> 2) & 1 == b2 and (h >> 3) & 1 == b3:
            hexes_in.append(h)
    
    kw_positions = sorted([kw_hex.index(h) + 1 for h in hexes_in])
    print(f"  {meeting}: KW positions = {kw_positions}")
