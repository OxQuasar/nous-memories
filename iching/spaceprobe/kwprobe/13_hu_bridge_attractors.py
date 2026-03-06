"""
Are there attractor patterns in the 互 values at inter-pair bridges?

The inter-pair bridge connects pair_k's second member to pair_{k+1}'s first member.
Each has a 互 value. Does the walk in 互-space have preferred regions, return points,
or corridors?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6,
)

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

sym = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}

def hu_name(h):
    lo = TRIGRAM_NAMES[lower_trigram(h)]
    up = TRIGRAM_NAMES[upper_trigram(h)]
    return f"{lo}/{up}"

# ══════════════════════════════════════════════════════════════════════════════
# 1. THE INTER-PAIR 互 WALK
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. 互 VALUES AT INTER-PAIR BOUNDARIES")
print("=" * 70)

# At each inter-pair bridge (step 2k+1 → 2k+2), we have:
# - outgoing 互: hugua(kw_hex[2k+1])  (pair k's second member)
# - incoming 互: hugua(kw_hex[2k+2])  (pair k+1's first member)
# These are the 互 values AT the bridge.

# But actually, each pair has two 互 values. The inter-pair walk connects:
# pair_k.hu2 → pair_{k+1}.hu1

# Let's track the full 互 walk at pair level:
# Each pair has (hu1, hu2). The bridge connects hu2[k] → hu1[k+1].

print(f"\n  The 互 walk across all 64 positions:")
hu_seq = [hugua(kw_hex[i]) for i in range(64)]

# Which 互 values appear at even positions (pair starts) vs odd (pair ends)?
even_hu = [hu_seq[i] for i in range(0, 64, 2)]  # pair starts
odd_hu = [hu_seq[i] for i in range(1, 64, 2)]   # pair ends

print(f"\n  互 at pair starts (even positions):")
start_counts = Counter(even_hu)
for hv, c in sorted(start_counts.items(), key=lambda x: -x[1]):
    print(f"    {hu_name(hv):12s} ({fmt6(hv)}): {c} times  basin={sym[get_basin(hv)]}")

print(f"\n  互 at pair ends (odd positions):")
end_counts = Counter(odd_hu)
for hv, c in sorted(end_counts.items(), key=lambda x: -x[1]):
    print(f"    {hu_name(hv):12s} ({fmt6(hv)}): {c} times  basin={sym[get_basin(hv)]}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. THE BRIDGE 互 VALUES — WHAT'S AT THE SEAM?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. 互 VALUES AT THE SEAM (pair end → next pair start)")
print("=" * 70)

# The seam is: hu(kw_hex[2k+1]) → hu(kw_hex[2(k+1)])
# These are the 互 values on either side of the inter-pair bridge.

seam_pairs = []
for k in range(31):
    hu_out = hu_seq[2*k + 1]  # outgoing (pair k, member 2)
    hu_in = hu_seq[2*(k+1)]   # incoming (pair k+1, member 1)
    seam_pairs.append((hu_out, hu_in))

# Which 互 values appear most at seams?
seam_hu = [h for pair in seam_pairs for h in pair]
seam_counts = Counter(seam_hu)
print(f"\n  互 values at seams (62 values = 31 bridges × 2 sides):")
for hv, c in sorted(seam_counts.items(), key=lambda x: -x[1]):
    print(f"    {hu_name(hv):12s} ({fmt6(hv)}): {c} times  basin={sym[get_basin(hv)]}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. PREFERRED CORRIDORS IN 互-SPACE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. PREFERRED 互 TRANSITIONS AT INTER-PAIR BRIDGES")
print("=" * 70)

# Which 互→互 transitions are most common at bridges?
bridge_trans = Counter()
for hu_out, hu_in in seam_pairs:
    if hu_out != hu_in:
        bridge_trans[(hu_out, hu_in)] += 1

print(f"\n  Most common 互 transitions at bridges:")
for (a, b), c in sorted(bridge_trans.items(), key=lambda x: -x[1]):
    ba = sym[get_basin(a)]
    bb = sym[get_basin(b)]
    d = hamming6(a, b)
    print(f"    {hu_name(a):12s}{ba} → {hu_name(b):12s}{bb} (d={d}): {c}")

# Same 互 at bridge (no change)
same_at_bridge = sum(1 for a, b in seam_pairs if a == b)
print(f"\n  Same 互 at bridge: {same_at_bridge}/31")

# ══════════════════════════════════════════════════════════════════════════════
# 4. RETURN PATTERNS — DOES THE WALK REVISIT 互 VALUES?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. RETURN PATTERNS IN THE 互 WALK")
print("=" * 70)

# For each 互 value, when does it appear in the sequence?
hu_positions = defaultdict(list)
for i in range(64):
    hu_positions[hu_seq[i]].append(i + 1)

print(f"\n  互 value recurrence (KW positions):")
for hv in sorted(hu_positions.keys()):
    positions = hu_positions[hv]
    basin = sym[get_basin(hv)]
    gaps = [positions[j+1] - positions[j] for j in range(len(positions)-1)] if len(positions) > 1 else []
    print(f"    {hu_name(hv):12s}{basin}: positions={positions}, "
          f"gaps={gaps}")

# Average return time per 互 value
print(f"\n  Return statistics:")
all_gaps = []
for hv, positions in hu_positions.items():
    gaps = [positions[j+1] - positions[j] for j in range(len(positions)-1)]
    all_gaps.extend(gaps)

if all_gaps:
    print(f"    Mean return gap: {np.mean(all_gaps):.1f}")
    print(f"    Gap distribution: {Counter(all_gaps)}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE 互 WALK GRAPH — WHICH EDGES ARE USED?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. THE 互 WALK GRAPH (edges used by inter-pair bridges)")
print("=" * 70)

# Build the directed graph of 互 transitions at inter-pair bridges
inter_graph = defaultdict(Counter)
for hu_out, hu_in in seam_pairs:
    inter_graph[hu_out][hu_in] += 1

# Adjacency structure
print(f"\n  互 transition graph (inter-pair only):")
for src in sorted(inter_graph.keys()):
    targets = inter_graph[src]
    src_basin = sym[get_basin(src)]
    target_str = ', '.join(f"{hu_name(t)}{sym[get_basin(t)]}({c})" 
                           for t, c in sorted(targets.items(), key=lambda x: -x[1]))
    print(f"    {hu_name(src):12s}{src_basin} → {target_str}")

# In-degree and out-degree
out_degree = {v: len(inter_graph[v]) for v in inter_graph}
in_sources = defaultdict(set)
for src in inter_graph:
    for tgt in inter_graph[src]:
        in_sources[tgt].add(src)
in_degree = {v: len(in_sources[v]) for v in in_sources}

print(f"\n  Node degrees (inter-pair transitions only):")
all_nodes = set(out_degree.keys()) | set(in_degree.keys())
for v in sorted(all_nodes):
    od = out_degree.get(v, 0)
    id_ = in_degree.get(v, 0)
    basin = sym[get_basin(v)]
    print(f"    {hu_name(v):12s}{basin}: in={id_:2d} out={od:2d}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. HUB DETECTION — ARE SOME 互 VALUES HUBS?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. HUB DETECTION IN THE 互 WALK")
print("=" * 70)

# A hub is a 互 value with high in+out degree and high visit count
print(f"\n  Combined hub score (visits × degree):")
for v in sorted(all_nodes):
    visits = seam_counts.get(v, 0)
    degree = out_degree.get(v, 0) + in_degree.get(v, 0)
    basin = sym[get_basin(v)]
    total_visits = len(hu_positions.get(v, []))
    print(f"    {hu_name(v):12s}{basin}: bridge_visits={visits:2d} seam_degree={degree:2d} "
          f"total_visits={total_visits}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. BASIN-LEVEL VIEW OF INTER-PAIR 互 WALK
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. BASIN-LEVEL VIEW OF INTER-PAIR 互 TRANSITIONS")
print("=" * 70)

# At the seam, the basin of the outgoing 互 and incoming 互
basin_trans = Counter()
for hu_out, hu_in in seam_pairs:
    b_out = get_basin(hu_out)
    b_in = get_basin(hu_in)
    basin_trans[(b_out, b_in)] += 1

print(f"\n  Basin transitions at inter-pair bridges:")
for b in ['Kun', 'KanLi', 'Qian']:
    row = []
    for b2 in ['Kun', 'KanLi', 'Qian']:
        c = basin_trans.get((b, b2), 0)
        row.append(f"{c:3d}")
    print(f"    {sym[b]}{b:6s} → [{' '.join(row)}]  (○ ◎ ●)")

# This should match the basin walk at inter-pair positions,
# which is where basin transitions happen

# ══════════════════════════════════════════════════════════════════════════════
# 8. DO CERTAIN 互 VALUES ACT AS BASIN GATEWAYS?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. 互 VALUES AS BASIN GATEWAYS")
print("=" * 70)

# A gateway 互 value is one that appears at basin-crossing bridges
# Which 互 values are present when the basin changes?

gateway_counts = Counter()
for hu_out, hu_in in seam_pairs:
    b_out = get_basin(hu_out)
    b_in = get_basin(hu_in)
    if b_out != b_in:
        gateway_counts[hu_out] += 1
        gateway_counts[hu_in] += 1

print(f"\n  互 values at basin-crossing bridges:")
if gateway_counts:
    for hv, c in sorted(gateway_counts.items(), key=lambda x: -x[1]):
        basin = sym[get_basin(hv)]
        print(f"    {hu_name(hv):12s}{basin}: appears at {c} crossings")
else:
    print(f"    (no basin crossings at inter-pair bridges)")

# ══════════════════════════════════════════════════════════════════════════════
# 9. THE 互 WALK TRAJECTORIES — UC vs LC
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. UC vs LC 互 WALK CHARACTER")
print("=" * 70)

# Split seam pairs by canon
uc_seams = seam_pairs[:14]  # pairs 0-13 → 14 bridges in UC
lc_seams = seam_pairs[14:]  # pairs 14-30 → 17 bridges in LC (including cross)

for label, seams in [("UC (bridges 0-13)", uc_seams), ("LC (bridges 14-30)", lc_seams)]:
    hu_vals = [h for pair in seams for h in pair]
    basin_counts = Counter(get_basin(h) for h in hu_vals)
    hu_dists = [hamming6(a, b) for a, b in seams if a != b]
    
    print(f"\n  {label}:")
    print(f"    Basin distribution at seams: {dict(basin_counts)}")
    if hu_dists:
        print(f"    Mean 互 step: {np.mean(hu_dists):.2f}")
    
    # Most visited 互 values
    val_counts = Counter(hu_vals)
    top = val_counts.most_common(3)
    print(f"    Top 互 values: {[(hu_name(v), sym[get_basin(v)], c) for v, c in top]}")

# ══════════════════════════════════════════════════════════════════════════════
# 10. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. SUMMARY")
print("=" * 70)
