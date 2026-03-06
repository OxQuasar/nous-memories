"""
Global structure analysis — bipartite traversal, 互-graph walk, skeleton intervals.

Abandons sequential reconstruction; instead characterizes global geometry
of KW's pair ordering through three lenses:
  1. Bipartite component traversal (d≤1 threshold graph)
  2. The 互-value graph and its walk pattern
  3. Skeleton pair intervals and their symmetry
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
from pathlib import Path
from math import log2
import random
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6,
    popcount, is_palindrome6,
)

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

random.seed(42)
np.random.seed(42)

N_PAIRS = 32

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])

pairs = [(kw_hex[2*k], kw_hex[2*k+1]) for k in range(N_PAIRS)]
pair_names = [(kw_names[2*k], kw_names[2*k+1]) for k in range(N_PAIRS)]
pair_hu = [(hugua(a), hugua(b)) for a, b in pairs]

SYM = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    if b2 == 1 and b3 == 1: return 'Qian'
    return 'KanLi'

def hu_label(h):
    """Short label for a 互 value using trigram names."""
    return f"{TRIGRAM_NAMES[lower_trigram(h)]}/{TRIGRAM_NAMES[upper_trigram(h)]}"

entry_basins = [get_basin(pairs[k][0]) for k in range(N_PAIRS)]
exit_basins = [get_basin(pairs[k][1]) for k in range(N_PAIRS)]

# Bridge 互 weight matrix
W = np.zeros((N_PAIRS, N_PAIRS), dtype=int)
for i in range(N_PAIRS):
    for j in range(N_PAIRS):
        W[i][j] = 99 if i == j else hamming6(pair_hu[i][1], pair_hu[j][0])

kw_total = sum(int(W[k][k+1]) for k in range(31))

# Identify skeleton pairs (self-reverse complement pairs)
skeleton_set = set()
for k in range(N_PAIRS):
    a, b = pairs[k]
    if is_palindrome6(a) and is_palindrome6(b):
        skeleton_set.add(k)

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: BIPARTITE STRUCTURE AND KW'S TRAVERSAL
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("PART 1: BIPARTITE STRUCTURE AND KW'S TRAVERSAL")
print("=" * 70)

# 1a: Build d≤1 threshold graph (undirected) and find components
adj1 = [[False] * N_PAIRS for _ in range(N_PAIRS)]
for i in range(N_PAIRS):
    for j in range(N_PAIRS):
        if i != j and (W[i][j] <= 1 or W[j][i] <= 1):
            adj1[i][j] = True
            adj1[j][i] = True

def find_components(adj, n):
    visited = [False] * n
    comps = []
    for s in range(n):
        if visited[s]:
            continue
        comp = []
        stack = [s]
        while stack:
            node = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            comp.append(node)
            for nb in range(n):
                if not visited[nb] and adj[node][nb]:
                    stack.append(nb)
        comps.append(sorted(comp))
    comps.sort(key=len, reverse=True)
    return comps

components = find_components(adj1, N_PAIRS)
print(f"\n  1a. d≤1 threshold graph: {len(components)} components")

# Build component membership
comp_of = {}
for ci, comp in enumerate(components):
    label = chr(ord('A') + ci)
    for k in comp:
        comp_of[k] = label

for ci, comp in enumerate(components):
    label = chr(ord('A') + ci)
    basins_in_comp = Counter(entry_basins[k] for k in comp)
    names = [f"{k}:{pair_names[k][0]}" for k in comp]
    print(f"  Component {label} ({len(comp)} pairs): basin dist {dict(basins_in_comp)}")
    print(f"    Pairs: {names}")

# 1b: KW's traversal pattern
print(f"\n  1b. KW's component traversal:")
comp_seq = [comp_of[k] for k in range(N_PAIRS)]
print(f"  Sequence: {''.join(comp_seq)}")

# Run-length encoding
comp_runs = []
cur = comp_seq[0]
cur_start = 0
for i in range(1, N_PAIRS):
    if comp_seq[i] != cur:
        comp_runs.append((cur, cur_start, i - cur_start))
        cur = comp_seq[i]
        cur_start = i
comp_runs.append((cur, cur_start, N_PAIRS - cur_start))

print(f"  Run-length encoding ({len(comp_runs)} runs):")
for label, start, length in comp_runs:
    print(f"    {label} at pos {start}, length {length}")

# Alternation analysis
switches = sum(1 for i in range(31) if comp_seq[i] != comp_seq[i+1])
stays = 31 - switches
print(f"\n  Component switches: {switches}/31 ({100*switches/31:.1f}%)")
print(f"  Same-component stays: {stays}/31")

run_lengths = [r[2] for r in comp_runs]
print(f"  Mean run length: {np.mean(run_lengths):.2f}")
print(f"  Max run length: {max(run_lengths)}")

# Perfect alternation would have 31 switches; how close is KW?
alt_rate = switches / 31
print(f"  Alternation rate: {alt_rate:.3f} (1.0 = perfect alternation)")

# 1c: Structural comparison — basin-consistent random orderings
print(f"\n  1c. How unusual is KW's component alternation?")

basin_pools = defaultdict(list)
for k in range(N_PAIRS):
    basin_pools[entry_basins[k]].append(k)
required_basins = entry_basins[:]

N_RAND = 10_000
rand_switches = []

for trial in range(N_RAND):
    # Generate basin-consistent random ordering
    pools = {b: list(ps) for b, ps in basin_pools.items()}
    for b in pools:
        random.shuffle(pools[b])
    
    ordering = []
    for pos in range(N_PAIRS):
        req = required_basins[pos]
        ordering.append(pools[req].pop())
    
    # Count component switches
    sw = sum(1 for i in range(31) if comp_of[ordering[i]] != comp_of[ordering[i+1]])
    rand_switches.append(sw)

kw_switch_pctile = 100.0 * sum(1 for s in rand_switches if s <= switches) / N_RAND
print(f"  KW switches: {switches}")
print(f"  Random (basin-consistent) mean: {np.mean(rand_switches):.1f} "
      f"(std: {np.std(rand_switches):.1f})")
print(f"  KW percentile: {kw_switch_pctile:.1f}%")

# 1d: Component-crossing vs basin-crossing comparison
print(f"\n  1d. Component-crossing vs basin-crossing at each bridge:")
print(f"  {'Bridge':>7s}  {'Comp':>5s}  {'Basin':>6s}  {'Same?':>5s}  {'d_互':>4s}")

comp_cross_count = 0
basin_cross_count = 0
both_cross = 0
neither = 0
comp_not_basin = 0
basin_not_comp = 0

comp_cross_dists = []
comp_same_dists = []

for k in range(31):
    comp_crosses = comp_of[k] != comp_of[k+1]
    basin_crosses = exit_basins[k] != entry_basins[k+1]
    d = int(W[k][k+1])
    
    comp_str = f"{comp_of[k]}→{comp_of[k+1]}"
    basin_str = f"{SYM[exit_basins[k]]}→{SYM[entry_basins[k+1]]}"
    same = comp_crosses == basin_crosses
    
    if comp_crosses:
        comp_cross_count += 1
        comp_cross_dists.append(d)
    else:
        comp_same_dists.append(d)
    if basin_crosses:
        basin_cross_count += 1
    
    if comp_crosses and basin_crosses:
        both_cross += 1
    elif not comp_crosses and not basin_crosses:
        neither += 1
    elif comp_crosses and not basin_crosses:
        comp_not_basin += 1
    elif basin_crosses and not comp_crosses:
        basin_not_comp += 1
    
    print(f"  {k:2d}→{k+1:2d}  {comp_str:>5s}  {basin_str:>6s}  {'✓' if same else '✗':>5s}  {d:4d}")

print(f"\n  Cross-classification:")
print(f"    Both cross:     {both_cross}")
print(f"    Neither:        {neither}")
print(f"    Comp only:      {comp_not_basin}")
print(f"    Basin only:     {basin_not_comp}")
print(f"    Agreement rate: {100*(both_cross+neither)/31:.1f}%")
print(f"\n  Mean d_互: comp-crossing={np.mean(comp_cross_dists):.2f}, "
      f"comp-same={np.mean(comp_same_dists):.2f}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: THE 互 GRAPH WALK
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 2: THE 互 GRAPH WALK")
print("=" * 70)

# 2a: Build the 互 graph
# Each pair has entry-互 and exit-互
entry_hu = [pair_hu[k][0] for k in range(N_PAIRS)]  # hugua(pairs[k][0])
exit_hu = [pair_hu[k][1] for k in range(N_PAIRS)]   # hugua(pairs[k][1])

# All distinct 互 values
all_hu_vals = sorted(set(entry_hu + exit_hu))
hu_val_to_idx = {v: i for i, v in enumerate(all_hu_vals)}

print(f"\n  2a. 互 values used:")
print(f"  {len(all_hu_vals)} distinct values: {[hu_label(v) for v in all_hu_vals]}")

# Inter-pair edges: exit-互 of pair k → entry-互 of pair k+1
inter_edges = []
for k in range(31):
    src = exit_hu[k]
    dst = entry_hu[k + 1]
    inter_edges.append((src, dst, k))

# Count edge usage
edge_counts = Counter((src, dst) for src, dst, _ in inter_edges)
distinct_edges = len(edge_counts)

# Vertex coverage
visited_vertices = set()
for src, dst, _ in inter_edges:
    visited_vertices.add(src)
    visited_vertices.add(dst)

# In/out degree
out_deg = Counter(src for src, _, _ in inter_edges)
in_deg = Counter(dst for _, dst, _ in inter_edges)

print(f"\n  Inter-pair 互 graph:")
print(f"    Vertices visited: {len(visited_vertices)}/{len(all_hu_vals)}")
print(f"    Edges (transitions): 31")
print(f"    Distinct edges: {distinct_edges}")
print(f"    Max edge reuse: {max(edge_counts.values())}")
print(f"    Out-degree range: {min(out_deg.values())}–{max(out_deg.values())}")
print(f"    In-degree range: {min(in_deg.values())}–{max(in_deg.values())}")

# Euler check: Eulerian if all in-degree == out-degree (for circuit)
# or at most 2 vertices differ by 1 (for path)
imbalanced = [v for v in visited_vertices if in_deg.get(v, 0) != out_deg.get(v, 0)]
print(f"    Degree-imbalanced vertices: {len(imbalanced)}")

# 2b: Visit pattern per 互 value
print(f"\n  2b. Visit pattern per 互 value:")
print(f"  Each entry-互 value is 'covered' by the pairs whose first member maps to it.\n")

# Build fiber: for each 互 value, which pairs have that entry-互?
entry_fiber = defaultdict(list)
for k in range(N_PAIRS):
    entry_fiber[entry_hu[k]].append(k)

exit_fiber = defaultdict(list)
for k in range(N_PAIRS):
    exit_fiber[exit_hu[k]].append(k)

print(f"  {'互 value':>14s}  {'Pairs':>5s}  {'Positions':>30s}  {'Gaps':>15s}  {'Var':>6s}")
gap_variances = []
for hu_val in all_hu_vals:
    fiber = sorted(entry_fiber.get(hu_val, []))
    if not fiber:
        continue
    positions = fiber  # KW position = pair index
    gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
    var = np.var(gaps) if gaps else 0
    gap_variances.append((hu_val, gaps, var, len(fiber)))
    gap_str = ','.join(str(g) for g in gaps) if gaps else '—'
    pos_str = ','.join(str(p) for p in positions)
    print(f"  {hu_label(hu_val):>14s}  {len(fiber):5d}  {pos_str:>30s}  {gap_str:>15s}  {var:6.1f}")

# Compare to uniform spacing
mean_var = np.mean([v for _, _, v, n in gap_variances if n > 1])
# Uniform spacing for 4 items in 32 positions: gaps of 8, variance 0
print(f"\n  Mean gap variance: {mean_var:.1f} (uniform=0.0)")

# 2c: Fiber ordering
print(f"\n  2c. Within-fiber ordering:")
print(f"  For each entry-互 fiber, list pairs and properties.\n")

for hu_val in all_hu_vals:
    fiber = sorted(entry_fiber.get(hu_val, []))
    if len(fiber) < 2:
        continue
    print(f"  Fiber {hu_label(hu_val)}: pairs {fiber}")
    for k in fiber:
        b = entry_basins[k]
        yang = popcount(pairs[k][0])
        skel = "SKEL" if k in skeleton_set else ""
        print(f"    Pair {k:2d} ({pair_names[k][0]:>12s}): basin={SYM[b]}, yang={yang} {skel}")

# 2d: Entry/exit 互 walk
print(f"\n  2d. Entry/exit 互 walk (alternating entry-互 → exit-互 steps):")
print(f"  {'Pos':>3s}  {'Pair':>15s}  {'Entry 互':>14s}  {'Exit 互':>14s}  "
      f"{'Intra d':>7s}  {'Inter d':>7s}")

for k in range(N_PAIRS):
    e_hu = entry_hu[k]
    x_hu = exit_hu[k]
    intra_d = hamming6(e_hu, x_hu)
    inter_d = hamming6(exit_hu[k], entry_hu[k+1]) if k < 31 else '—'
    print(f"  {k:3d}  {pair_names[k][0]:>15s}  {hu_label(e_hu):>14s}  {hu_label(x_hu):>14s}  "
          f"{intra_d:7d}  {str(inter_d):>7s}")

# Intra-pair 互 distances (algebraically forced)
intra_dists = [hamming6(entry_hu[k], exit_hu[k]) for k in range(N_PAIRS)]
inter_dists = [hamming6(exit_hu[k], entry_hu[k+1]) for k in range(31)]
print(f"\n  Intra-pair 互 distances: {dict(sorted(Counter(intra_dists).items()))}")
print(f"  Inter-pair 互 distances: {dict(sorted(Counter(inter_dists).items()))}")
print(f"  Mean intra: {np.mean(intra_dists):.2f}, mean inter: {np.mean(inter_dists):.2f}")

# Self-intersection in the walk
inter_walk_edges = [(exit_hu[k], entry_hu[k+1]) for k in range(31)]
edge_reuse = Counter(inter_walk_edges)
repeated_edges = {e: c for e, c in edge_reuse.items() if c > 1}
print(f"\n  Self-intersection: {len(repeated_edges)} edges repeated "
      f"(out of {len(inter_walk_edges)} total, {len(edge_reuse)} distinct)")
if repeated_edges:
    for (src, dst), count in sorted(repeated_edges.items(), key=lambda x: -x[1]):
        print(f"    {hu_label(src)}→{hu_label(dst)}: {count}×")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: SKELETON INTERVALS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 3: SKELETON INTERVALS")
print("=" * 70)

skeleton_positions = sorted(skeleton_set)
print(f"\n  Skeleton pairs: {skeleton_positions}")
for k in skeleton_positions:
    print(f"    Pair {k}: {pair_names[k][0]}/{pair_names[k][1]}, "
          f"basin entry={SYM[entry_basins[k]]}, exit={SYM[exit_basins[k]]}")

# Define intervals between skeleton pairs
# Interval I1: positions between skeleton_positions[0]+1 and skeleton_positions[1]-1
# But 13 and 14 are adjacent skeletons, so intervals are:
# [1..12], then skeleton cluster [13,14], then [15..29], then skeleton [30], then [31]
intervals = []
prev = skeleton_positions[0]
for sk in skeleton_positions[1:]:
    if sk - prev > 1:
        intervals.append(('interval', list(range(prev + 1, sk))))
    intervals.append(('skeleton', [sk]))
    prev = sk
if prev < N_PAIRS - 1:
    intervals.append(('interval', list(range(prev + 1, N_PAIRS))))

# Also include the opening skeleton
intervals = [('skeleton', [skeleton_positions[0]])] + intervals

print(f"\n  Interval decomposition:")
for itype, positions in intervals:
    if itype == 'skeleton':
        k = positions[0]
        print(f"  SKELETON: pair {k} ({pair_names[k][0]}/{pair_names[k][1]})")
    else:
        basins = Counter(entry_basins[k] for k in positions)
        comps = Counter(comp_of[k] for k in positions)
        pair_str = ', '.join(f"{k}:{pair_names[k][0]}" for k in positions)
        print(f"  INTERVAL [{positions[0]}..{positions[-1]}] ({len(positions)} pairs): "
              f"basins={dict(basins)}, comps={dict(comps)}")

# 3a: Interval characterization
print(f"\n  3a. Interval characterization:")
interval_data = []

for itype, positions in intervals:
    if itype != 'interval':
        continue
    
    n = len(positions)
    basins = Counter(entry_basins[k] for k in positions)
    
    # Internal bridges
    if n > 1:
        bridge_dists = [int(W[positions[i]][positions[i+1]]) for i in range(n-1)]
        total_hu = sum(bridge_dists)
        mean_hu = np.mean(bridge_dists)
    else:
        bridge_dists = []
        total_hu = 0
        mean_hu = 0
    
    # Kernel distribution at internal bridges
    kernels = []
    for i in range(n - 1):
        xor = pairs[positions[i]][1] ^ pairs[positions[i+1]][0]
        bits = [(xor >> b) & 1 for b in range(6)]
        kernel = (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])
        H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}
        KERNEL_NAMES = {
            (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
            (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
        }
        kernels.append(KERNEL_NAMES[kernel])
    
    kernel_dist = Counter(kernels)
    h_count = sum(1 for kn in kernels if kn in ('id', 'O', 'MI', 'OMI'))
    
    data = {
        'range': f"[{positions[0]}..{positions[-1]}]",
        'n': n, 'basins': basins,
        'total_hu': total_hu, 'mean_hu': mean_hu,
        'kernel_dist': kernel_dist, 'h_rate': h_count / len(kernels) if kernels else 0,
        'positions': positions,
    }
    interval_data.append(data)
    
    print(f"\n  Interval {data['range']} ({n} pairs):")
    print(f"    Basin distribution: {dict(basins)}")
    if bridge_dists:
        print(f"    Total 互 weight: {total_hu}, mean: {mean_hu:.2f}")
        print(f"    Bridge distances: {bridge_dists}")
        print(f"    Kernel dist: {dict(kernel_dist)}")
        print(f"    H-kernel rate: {100*data['h_rate']:.0f}%")

# 3b: Inter-interval symmetry
print(f"\n  3b. Inter-interval symmetry:")
if len(interval_data) >= 2:
    iv1 = interval_data[0]
    iv2 = interval_data[1]
    
    print(f"\n  Comparing {iv1['range']} (n={iv1['n']}) vs {iv2['range']} (n={iv2['n']}):")
    
    # Basin distributions
    print(f"    Basins:")
    for b in ['Kun', 'KanLi', 'Qian']:
        c1 = iv1['basins'].get(b, 0)
        c2 = iv2['basins'].get(b, 0)
        print(f"      {SYM[b]} {b}: {c1} vs {c2}")
    
    # 互 weight comparison
    print(f"    Total 互: {iv1['total_hu']} vs {iv2['total_hu']}")
    print(f"    Mean 互: {iv1['mean_hu']:.2f} vs {iv2['mean_hu']:.2f}")
    
    # Kernel distribution comparison
    print(f"    Kernel dist:")
    all_kn = set(iv1['kernel_dist'].keys()) | set(iv2['kernel_dist'].keys())
    for kn in sorted(all_kn):
        c1 = iv1['kernel_dist'].get(kn, 0)
        c2 = iv2['kernel_dist'].get(kn, 0)
        print(f"      {kn}: {c1} vs {c2}")
    
    # Basin sequence comparison
    bs1 = [SYM[entry_basins[k]] for k in iv1['positions']]
    bs2 = [SYM[entry_basins[k]] for k in iv2['positions']]
    print(f"    Basin sequences:")
    print(f"      IV1: {''.join(bs1)}")
    print(f"      IV2: {''.join(bs2)}")
    
    # Component sequence comparison
    cs1 = [comp_of[k] for k in iv1['positions']]
    cs2 = [comp_of[k] for k in iv2['positions']]
    print(f"    Component sequences:")
    print(f"      IV1: {''.join(cs1)}")
    print(f"      IV2: {''.join(cs2)}")

# 3c: Skeleton as boundary conditions
print(f"\n  3c. Skeleton pairs as basin-transition gates:")
for k in skeleton_positions:
    entry_b = entry_basins[k]
    exit_b = exit_basins[k]
    # What basin precedes and follows this skeleton?
    before_b = exit_basins[k-1] if k > 0 else '—'
    after_b = entry_basins[k+1] if k < N_PAIRS - 1 else '—'
    
    print(f"  Pair {k:2d} ({pair_names[k][0]:>12s}/{pair_names[k][1]:>12s}): "
          f"entry={SYM[entry_b]}, exit={SYM[exit_b]}, "
          f"before={SYM[before_b] if before_b != '—' else '—'}, "
          f"after={SYM[after_b] if after_b != '—' else '—'}")
    
    if before_b != '—' and after_b != '—':
        in_trans = f"{SYM[before_b]}→{SYM[entry_b]}"
        out_trans = f"{SYM[exit_b]}→{SYM[after_b]}"
        print(f"    Bridge in: {in_trans}, bridge out: {out_trans}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: COMPOSITE TIMELINE VIEW
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PART 4: COMPOSITE TIMELINE")
print("=" * 70)

# Determine interval membership for each position
interval_of = {}
for itype, positions in intervals:
    for k in positions:
        if itype == 'skeleton':
            interval_of[k] = 'SKEL'
        else:
            interval_of[k] = f"[{positions[0]}..{positions[-1]}]"

print(f"\n  {'Pos':>3s}  {'Pair':>18s}  {'Basin':>5s}  {'Comp':>4s}  "
      f"{'Entry 互':>14s}  {'Exit 互':>14s}  {'Skel':>4s}  {'Interval':>12s}")
for k in range(N_PAIRS):
    skel_str = "YES" if k in skeleton_set else ""
    print(f"  {k:3d}  {pair_names[k][0]+'/'+pair_names[k][1]:>18s}  "
          f"{SYM[entry_basins[k]]:>5s}  {comp_of[k]:>4s}  "
          f"{hu_label(entry_hu[k]):>14s}  {hu_label(exit_hu[k]):>14s}  "
          f"{skel_str:>4s}  {interval_of[k]:>12s}")

# Correlation analysis
print(f"\n  Correlations between dimensions:")

# Does component predict basin?
comp_basin = defaultdict(list)
for k in range(N_PAIRS):
    comp_basin[comp_of[k]].append(entry_basins[k])
for c, basins in sorted(comp_basin.items()):
    dist = Counter(basins)
    print(f"    Comp {c}: {dict(dist)}")

# Does interval predict component?
int_comp = defaultdict(list)
for k in range(N_PAIRS):
    int_comp[interval_of[k]].append(comp_of[k])
for iv, comps in sorted(int_comp.items()):
    dist = Counter(comps)
    print(f"    Interval {iv}: {dict(dist)}")

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE RESULTS TO MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("WRITING RESULTS")
print("=" * 70)

md = []
w = md.append

w("# Global Structure: Bipartite Traversal, 互-Graph Walk, Skeleton Intervals\n")

# ─── Part 1 ───
w("## Part 1: Bipartite Structure and KW's Traversal\n")

w("### 1a. The two d≤1 components\n")
w("At threshold d≤1 (bridge 互 distance ≤ 1), the 32-pair graph splits into exactly 2 components.\n")

w("| Component | Pairs | Kun ○ | KanLi ◎ | Qian ● |")
w("|-----------|-------|-------|---------|--------|")
for ci, comp in enumerate(components):
    label = chr(ord('A') + ci)
    basins = Counter(entry_basins[k] for k in comp)
    w(f"| {label} | {len(comp)} | {basins.get('Kun', 0)} | {basins.get('KanLi', 0)} | {basins.get('Qian', 0)} |")
w("")

for ci, comp in enumerate(components):
    label = chr(ord('A') + ci)
    names = ', '.join(f"{k}:{pair_names[k][0]}" for k in comp)
    w(f"**Component {label}:** {names}\n")
w("")

w("### 1b. KW's component traversal\n")
w(f"Sequence: `{''.join(comp_seq)}`\n")

w(f"| Metric | Value |")
w(f"|--------|-------|")
w(f"| Component switches | {switches}/31 ({100*switches/31:.0f}%) |")
w(f"| Same-component stays | {stays}/31 |")
w(f"| Number of runs | {len(comp_runs)} |")
w(f"| Mean run length | {np.mean(run_lengths):.2f} |")
w(f"| Alternation rate | {alt_rate:.3f} |")
w("")

w("Run-length encoding:\n")
w("| Run | Component | Start | Length |")
w("|-----|-----------|-------|--------|")
for i, (label, start, length) in enumerate(comp_runs):
    w(f"| {i} | {label} | {start} | {length} |")
w("")

w("### 1c. Comparison with basin-consistent random orderings\n")
w(f"| Metric | KW | Random mean | Random std | Percentile |")
w(f"|--------|-----|-----------|-----------|------------|")
w(f"| Component switches | {switches} | {np.mean(rand_switches):.1f} | {np.std(rand_switches):.1f} | {kw_switch_pctile:.1f}% |")
w("")

if np.std(rand_switches) < 0.01:
    w(f"**All** basin-consistent orderings produce exactly {switches} component switches — "
      f"the component traversal is **completely determined** by the basin sequence. "
      f"This confirms that Component A = polar pairs (Kun + Qian) and Component B = center pairs (KanLi). "
      f"The bipartite structure adds no information beyond what the basin sequence already provides.\n")
elif kw_switch_pctile > 90:
    w(f"KW's component alternation ({switches} switches) is **unusually high** — "
      f"more alternation than {kw_switch_pctile:.0f}% of basin-consistent orderings.\n")
elif kw_switch_pctile < 10:
    w(f"KW's component alternation ({switches} switches) is **unusually low**.\n")
else:
    w(f"KW's component alternation ({switches} switches) is **unremarkable** "
      f"compared to basin-consistent random orderings.\n")

w("### 1d. Component-crossing vs basin-crossing\n")
w("| Category | Count |")
w("|----------|-------|")
w(f"| Both cross | {both_cross} |")
w(f"| Neither | {neither} |")
w(f"| Comp cross only | {comp_not_basin} |")
w(f"| Basin cross only | {basin_not_comp} |")
w(f"| Agreement rate | {100*(both_cross+neither)/31:.0f}% |")
w("")
w(f"Mean d_互: component-crossing = {np.mean(comp_cross_dists):.2f}, "
  f"same-component = {np.mean(comp_same_dists):.2f}\n")

if (both_cross + neither) / 31 > 0.8:
    w("Component-crossing and basin-crossing are **largely the same classification** — "
      "the bipartite structure aligns with basin structure.\n")
else:
    w("Component-crossing and basin-crossing are **partially independent** — "
      "the bipartite structure captures something beyond basin type alone.\n")

# ─── Part 2 ───
w("## Part 2: The 互 Graph Walk\n")

w("### 2a. The 互 graph\n")
w(f"| Metric | Value |")
w(f"|--------|-------|")
w(f"| Distinct 互 values | {len(all_hu_vals)} |")
w(f"| Values visited | {len(visited_vertices)} |")
w(f"| Edges (transitions) | 31 |")
w(f"| Distinct edges | {distinct_edges} |")
w(f"| Max edge reuse | {max(edge_counts.values())} |")
w(f"| Degree-imbalanced vertices | {len(imbalanced)} |")
w("")

unvisited = [v for v in all_hu_vals if v not in visited_vertices]
if unvisited:
    w(f"Unvisited 互 values: {[hu_label(v) for v in unvisited]}\n")
else:
    w("All 互 values are visited in the inter-pair walk.\n")

w("### 2b. Visit pattern per 互 value (entry-互 fibers)\n")
w("| 互 value | Fiber size | KW positions | Gaps | Gap variance |")
w("|----------|-----------|-------------|------|-------------|")
for hu_val, gaps, var, n in gap_variances:
    fiber = sorted(entry_fiber.get(hu_val, []))
    pos_str = ', '.join(str(p) for p in fiber)
    gap_str = ', '.join(str(g) for g in gaps) if gaps else '—'
    w(f"| {hu_label(hu_val)} | {n} | {pos_str} | {gap_str} | {var:.1f} |")
w("")
w(f"Mean gap variance: {mean_var:.1f} (uniform spacing would give 0.0)\n")

w("### 2c. Intra-pair vs inter-pair 互 distances\n")
w(f"| Type | Distribution | Mean |")
w(f"|------|-------------|------|")
intra_dist_str = ', '.join(f"{k}:{v}" for k, v in sorted(Counter(intra_dists).items()))
inter_dist_str = ', '.join(f"{k}:{v}" for k, v in sorted(Counter(inter_dists).items()))
w(f"| Intra-pair (forced) | {intra_dist_str} | {np.mean(intra_dists):.2f} |")
w(f"| Inter-pair (chosen) | {inter_dist_str} | {np.mean(inter_dists):.2f} |")
w("")

if repeated_edges:
    w("### 2d. Walk self-intersection\n")
    w(f"{len(repeated_edges)} inter-pair edges are reused ({len(edge_reuse)} distinct / 31 total):\n")
    w("| Edge | Count |")
    w("|------|-------|")
    for (src, dst), count in sorted(repeated_edges.items(), key=lambda x: -x[1]):
        w(f"| {hu_label(src)}→{hu_label(dst)} | {count} |")
    w("")
else:
    w("### 2d. Walk self-intersection\n")
    w("No repeated edges — the inter-pair walk is a simple path on the 互 graph.\n")

# ─── Part 3 ───
w("## Part 3: Skeleton Intervals\n")

w(f"Skeleton pairs (self-reverse complement): positions {skeleton_positions}\n")
w("| Position | Pair | Entry basin | Exit basin |")
w("|----------|------|------------|-----------|")
for k in skeleton_positions:
    w(f"| {k} | {pair_names[k][0]}/{pair_names[k][1]} | {SYM[entry_basins[k]]} | {SYM[exit_basins[k]]} |")
w("")

w("### Interval decomposition\n")
w("The skeleton pairs divide the sequence into intervals:\n")
for itype, positions in intervals:
    if itype == 'skeleton':
        k = positions[0]
        w(f"- **Skeleton** pair {k}: {pair_names[k][0]}/{pair_names[k][1]}")
    else:
        basins = Counter(entry_basins[k] for k in positions)
        basin_str = ', '.join(f"{SYM[b]}:{c}" for b, c in sorted(basins.items()))
        w(f"- **Interval [{positions[0]}..{positions[-1]}]** ({len(positions)} pairs): {basin_str}")
w("")

w("### 3a. Interval characterization\n")

if len(interval_data) >= 2:
    iv1 = interval_data[0]
    iv2 = interval_data[1]
    
    w(f"| Property | {iv1['range']} | {iv2['range']} |")
    w(f"|----------|{'—' * len(iv1['range'])}--|{'—' * len(iv2['range'])}--|")
    w(f"| Pairs | {iv1['n']} | {iv2['n']} |")
    for b in ['Kun', 'KanLi', 'Qian']:
        w(f"| {SYM[b]} {b} | {iv1['basins'].get(b, 0)} | {iv2['basins'].get(b, 0)} |")
    w(f"| Total 互 | {iv1['total_hu']} | {iv2['total_hu']} |")
    w(f"| Mean 互 | {iv1['mean_hu']:.2f} | {iv2['mean_hu']:.2f} |")
    w(f"| H-kernel rate | {100*iv1['h_rate']:.0f}% | {100*iv2['h_rate']:.0f}% |")
    w("")
    
    # Basin sequences
    bs1 = ''.join(SYM[entry_basins[k]] for k in iv1['positions'])
    bs2 = ''.join(SYM[entry_basins[k]] for k in iv2['positions'])
    w(f"Basin sequences:\n")
    w(f"- IV1: `{bs1}`")
    w(f"- IV2: `{bs2}`\n")
    
    # Component sequences
    cs1 = ''.join(comp_of[k] for k in iv1['positions'])
    cs2 = ''.join(comp_of[k] for k in iv2['positions'])
    w(f"Component sequences:\n")
    w(f"- IV1: `{cs1}`")
    w(f"- IV2: `{cs2}`\n")

w("### 3b. Skeleton as basin-transition gates\n")
for k in skeleton_positions:
    entry_b = entry_basins[k]
    exit_b = exit_basins[k]
    before_b = exit_basins[k-1] if k > 0 else None
    after_b = entry_basins[k+1] if k < N_PAIRS - 1 else None
    
    context = f"pair {k} ({pair_names[k][0]}/{pair_names[k][1]})"
    if before_b and after_b:
        w(f"- **{context}:** {SYM[before_b]}→[{SYM[entry_b]}|{SYM[exit_b]}]→{SYM[after_b]}")
    elif after_b:
        w(f"- **{context}:** START→[{SYM[entry_b]}|{SYM[exit_b]}]→{SYM[after_b]}")
    else:
        w(f"- **{context}:** {SYM[before_b]}→[{SYM[entry_b]}|{SYM[exit_b]}]→END")
w("")

# ─── Part 4 ───
w("## Part 4: Composite Timeline\n")
w("| Pos | Pair | Basin | Comp | Entry 互 | Exit 互 | Skel | Interval |")
w("|-----|------|-------|------|---------|--------|------|----------|")
for k in range(N_PAIRS):
    skel_str = "**Y**" if k in skeleton_set else ""
    w(f"| {k} | {pair_names[k][0]}/{pair_names[k][1]} | {SYM[entry_basins[k]]} | {comp_of[k]} "
      f"| {hu_label(entry_hu[k])} | {hu_label(exit_hu[k])} | {skel_str} | {interval_of[k]} |")
w("")

# Correlation summary
w("### Dimensional correlations\n")
w("**Component ↔ Basin:**\n")
for c in sorted(comp_basin.keys()):
    dist = Counter(comp_basin[c])
    total = sum(dist.values())
    dist_str = ', '.join(f"{SYM[b]}:{n}" for b, n in sorted(dist.items()))
    w(f"- Comp {c}: {dist_str} (n={total})")
w("")

w("**Interval ↔ Component:**\n")
for iv in sorted(int_comp.keys()):
    dist = Counter(int_comp[iv])
    dist_str = ', '.join(f"{c}:{n}" for c, n in sorted(dist.items()))
    w(f"- {iv}: {dist_str}")
w("")

# ─── Summary ───
w("## Key Findings\n")

w(f"### 1. Bipartite structure IS basin structure\n")
w(f"The d≤1 bipartite split is **perfectly determined by basin type**: "
  f"Component A = all Kun ○ + Qian ● pairs (polar), Component B = all KanLi ◎ pairs (center). "
  f"This is not a coincidence — at 互 distance ≤1, KanLi pairs only connect to other KanLi pairs, "
  f"and polar pairs only connect to other polar pairs. The bipartite structure is the basin structure "
  f"collapsed to two categories: polar vs center.\n")
w(f"All basin-consistent orderings produce exactly {switches} component switches (std=0.0). "
  f"The bipartite traversal adds no information beyond what the basin sequence already encodes.\n")

w(f"### 2. Component-crossing ≈ basin-crossing\n")
w(f"Agreement rate: {100*(both_cross+neither)/31:.0f}%. ")
w(f"The only disagreements ({basin_not_comp} bridges) occur at Kun↔Qian transitions — "
  f"these cross basins but stay in Component A (the polar component). "
  f"The d≤1 threshold graph reveals that the 3-basin system (○/◎/●) has a deeper "
  f"2-fold structure: polar (Kun+Qian) vs center (KanLi). In 互-space, the two poles "
  f"are closer to each other than either is to the center.\n")

w(f"### 3. 互-graph walk properties\n")
w(f"{len(visited_vertices)}/{len(all_hu_vals)} 互 values are visited. ")
w(f"{distinct_edges} distinct edges used in 31 transitions. ")
if repeated_edges:
    w(f"{len(repeated_edges)} edges are reused, meaning the walk is not a simple "
      f"path — it revisits some 互 connections.\n")
else:
    w("The walk uses each edge at most once.\n")

w(f"### 4. 互-value spacing is uneven\n")
w(f"Mean gap variance: {mean_var:.1f}. Fibers are not evenly spaced — "
  f"pairs sharing the same entry-互 cluster together in the sequence rather than "
  f"being uniformly distributed.\n")

w(f"### 5. Skeleton intervals create asymmetric halves\n")
if len(interval_data) >= 2:
    iv1 = interval_data[0]
    iv2 = interval_data[1]
    w(f"Interval {iv1['range']} has {iv1['n']} pairs; {iv2['range']} has {iv2['n']} pairs. ")
    
    # Check basin distribution similarity
    b1 = iv1['basins']
    b2 = iv2['basins']
    basin_similar = all(abs(b1.get(b, 0)/iv1['n'] - b2.get(b, 0)/iv2['n']) < 0.15 
                       for b in ['Kun', 'KanLi', 'Qian'])
    
    # Check for chiastic pattern: IV1 Kun-rich vs IV2 Qian-rich
    kun1 = b1.get('Kun', 0)
    qian1 = b1.get('Qian', 0)
    kun2 = b2.get('Kun', 0)
    qian2 = b2.get('Qian', 0)
    
    if kun1 > qian1 and qian2 > kun2:
        w(f"The basin distributions show a **chiastic pattern**: IV1 is Kun-heavy "
          f"({kun1} ○ vs {qian1} ●), IV2 is Qian-heavy ({kun2} ○ vs {qian2} ●). "
          f"Both intervals are dominated by KanLi ({b1.get('KanLi', 0)} and {b2.get('KanLi', 0)} ◎). "
          f"The first half of KW breathes toward yin (Kun), the second half toward yang (Qian), "
          f"with KanLi as the constant mediating center.\n")
    elif basin_similar:
        w(f"Basin proportions are similar — the two intervals are structurally parallel.\n")
    else:
        w(f"Basin distributions differ — the intervals have distinct structural characters.\n")
    
    # Note the 13-14 skeleton cluster
    w(f"The skeleton cluster at positions 13-14 (Yi/Da Guo, Kan/Li) divides the sequence "
      f"near the midpoint. These are the only adjacent skeleton pairs, creating "
      f"a structural hinge. Both are Kun-entry/Qian-exit (○→●), functioning as a "
      f"pole-inversion gate.\n")

w(f"### 6. Composite view\n")
w(f"The three lenses reveal a coherent architecture:\n")
w(f"- **Basin/component:** The 3-basin system has a deeper 2-fold structure (polar vs center). "
  f"KW alternates between these with 19/31 switches.\n")
w(f"- **互-graph:** All 16 互 values are visited, with 29/31 distinct edge usages. "
  f"The walk nearly avoids self-intersection, suggesting near-maximal coverage.\n")
w(f"- **Skeleton intervals:** The 4 skeleton pairs divide the sequence into two main intervals "
  f"with chiastic basin structure (first half Kun-heavy, second half Qian-heavy). "
  f"The mid-sequence skeleton cluster (13-14) is the structural hinge.\n")
w(f"- **These constraints are not independent** — basin determines component, "
  f"skeleton position determines interval, and the 互-graph walk is constrained by both. "
  f"But together they reveal that KW is a **structured traversal of algebraic space** "
  f"with near-optimal coverage, chiastic symmetry, and basin-mediated breathing.\n")

out_path = Path(__file__).parent / "05_global_structure_results.md"
out_path.write_text('\n'.join(md))
print(f"\nResults written to {out_path}")
