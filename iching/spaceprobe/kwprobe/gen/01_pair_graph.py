"""
Pair graph construction and greedy 互-continuity reconstruction.

Builds the directed weight graph over KW's 32 pairs, where edge weight
is the bridge 互 Hamming distance: hamming6(hugua(pair_i[1]), hugua(pair_j[0])).

Tests how close greedy 互 minimization gets to reconstructing KW order.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path
import random
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6,
)

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

random.seed(42)
np.random.seed(42)

# Convert KW sequence to integer hex values
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
    if b2 == 1 and b3 == 1: return 'Qian'
    return 'KanLi'

def hu_name(h):
    return f"{TRIGRAM_NAMES[lower_trigram(h)]}/{TRIGRAM_NAMES[upper_trigram(h)]}"

SYM = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}

# ═══════════════════════════════════════════════════════════════════════════════
# 1. PAIR EXTRACTION WITH KW ORIENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

# pairs[k] = (member0, member1) in KW order (member0 = first in sequence)
pairs = [(kw_hex[2*k], kw_hex[2*k+1]) for k in range(32)]
pair_names = [(kw_names[2*k], kw_names[2*k+1]) for k in range(32)]

# Precompute 互 values for each pair member
pair_hu = [(hugua(a), hugua(b)) for a, b in pairs]

print("=" * 70)
print("1. PAIR GRAPH CONSTRUCTION")
print("=" * 70)

print(f"\n  32 KW pairs with orientations:")
print(f"  {'Pair':>4s}  {'Member 0':>12s} {'Member 1':>12s}  "
      f"{'互0':>12s} {'互1':>12s}  {'Basin0':>6s} {'Basin1':>6s}")
for k in range(32):
    a, b = pairs[k]
    hu_a, hu_b = pair_hu[k]
    print(f"  {k:4d}  {pair_names[k][0]:>12s} {pair_names[k][1]:>12s}  "
          f"{hu_name(hu_a):>12s} {hu_name(hu_b):>12s}  "
          f"{SYM[get_basin(a)]:>6s} {SYM[get_basin(b)]:>6s}")

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD THE 32x32 DIRECTED WEIGHT MATRIX
# ═══════════════════════════════════════════════════════════════════════════════

# W[i][j] = bridge 互 distance from pair i to pair j
# = hamming6(hugua(pair_i[1]), hugua(pair_j[0]))
N_PAIRS = 32
W = np.zeros((N_PAIRS, N_PAIRS), dtype=int)
for i in range(N_PAIRS):
    hu_i_out = pair_hu[i][1]  # outgoing: pair i's second member's 互
    for j in range(N_PAIRS):
        if i == j:
            W[i][j] = 99  # sentinel for self-loop (invalid)
            continue
        hu_j_in = pair_hu[j][0]  # incoming: pair j's first member's 互
        W[i][j] = hamming6(hu_i_out, hu_j_in)

# Weight distribution (excluding self-loops)
weights = W[W < 99]
weight_dist = Counter(int(w) for w in weights)
print(f"\n  Weight matrix statistics (32×32, {len(weights)} edges):")
print(f"    Distribution: {dict(sorted(weight_dist.items()))}")
print(f"    Min: {weights.min()}, Max: {weights.max()}, Mean: {weights.mean():.3f}")

# Check asymmetry
asym_count = sum(1 for i in range(N_PAIRS) for j in range(i+1, N_PAIRS)
                 if W[i][j] != W[j][i])
print(f"    Asymmetric edges (W[i,j] ≠ W[j,i]): {asym_count}/{N_PAIRS*(N_PAIRS-1)//2}")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. KW ACTUAL PATH
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. KW ACTUAL PATH — 31 BRIDGE 互 DISTANCES")
print("=" * 70)

kw_bridge_dists = []
for k in range(31):
    d = W[k][k+1]
    kw_bridge_dists.append(d)

kw_total = sum(kw_bridge_dists)
print(f"\n  Bridge distances: {kw_bridge_dists}")
print(f"  Total 互 weight: {kw_total}")
print(f"  Mean per bridge: {kw_total / 31:.3f}")
print(f"  Distribution: {dict(sorted(Counter(kw_bridge_dists).items()))}")

print(f"\n  Bridge detail:")
print(f"  {'Bridge':>8s}  {'From pair':>20s}  {'To pair':>20s}  {'d_互':>4s}")
for k in range(31):
    d = kw_bridge_dists[k]
    print(f"  {k:2d}→{k+1:2d}    {pair_names[k][0]+'/'+pair_names[k][1]:>20s}  "
          f"{pair_names[k+1][0]+'/'+pair_names[k+1][1]:>20s}  {d:4d}")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. RANDOM BASELINE (PAIR-ORDER SHUFFLES)
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. RANDOM BASELINE — 100,000 PAIR-ORDER SHUFFLES")
print("=" * 70)

N_TRIALS = 100_000
random_totals = np.zeros(N_TRIALS)
order = list(range(N_PAIRS))

for trial in range(N_TRIALS):
    random.shuffle(order)
    total = sum(W[order[k]][order[k+1]] for k in range(31))
    random_totals[trial] = total

kw_pctile = 100.0 * np.sum(random_totals <= kw_total) / N_TRIALS
print(f"\n  KW total weight: {kw_total}")
print(f"  Random: mean={random_totals.mean():.1f}, std={random_totals.std():.1f}, "
      f"min={random_totals.min():.0f}, max={random_totals.max():.0f}")
print(f"  KW percentile: {kw_pctile:.2f}%")
print(f"  (KW is {'better' if kw_pctile < 50 else 'worse'} than average at 互 continuity)")

# Histogram
hist_vals, bin_edges = np.histogram(random_totals, bins=30)
max_bar = max(hist_vals)
print(f"\n  Distribution:")
for i in range(len(hist_vals)):
    lo, hi = bin_edges[i], bin_edges[i+1]
    bar_len = int(40 * hist_vals[i] / max_bar)
    marker = " ◄ KW" if lo <= kw_total < hi else ""
    print(f"    {lo:5.0f}-{hi:5.0f} | {'█' * bar_len} {hist_vals[i]}{marker}")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. GREEDY 互 WALK
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. GREEDY 互 WALK")
print("=" * 70)

def greedy_walk(start, weight_matrix, basin_tiebreak=False, force_last=None):
    """
    Greedy walk: at each step choose unvisited pair with minimum bridge 互 distance.
    
    Tiebreaking:
      1. If basin_tiebreak: prefer same basin as current pair's second member
      2. KW pair index (lower first)
    
    force_last: if set, reserve this pair index for position 31 (last pair).
    """
    n = weight_matrix.shape[0]
    path = [start]
    visited = {start}
    
    # If force_last is set, exclude it from normal selection
    reserved = {force_last} if force_last is not None else set()
    
    for step in range(n - 1):
        current = path[-1]
        
        # On the last step, if we reserved a pair, we must go there
        if step == n - 2 and force_last is not None:
            path.append(force_last)
            visited.add(force_last)
            continue
        
        candidates = [j for j in range(n) if j not in visited and j not in reserved]
        
        if not candidates:
            # If reserved but no candidates, must use reserved
            if force_last is not None and force_last not in visited:
                path.append(force_last)
                visited.add(force_last)
                continue
            break
        
        # Score candidates
        min_dist = min(weight_matrix[current][j] for j in candidates)
        best = [j for j in candidates if weight_matrix[current][j] == min_dist]
        
        if basin_tiebreak and len(best) > 1:
            cur_basin = get_basin(pairs[current][1])
            same_basin = [j for j in best if get_basin(pairs[j][0]) == cur_basin]
            if same_basin:
                best = same_basin
        
        # Final tiebreak: KW order
        chosen = min(best)
        path.append(chosen)
        visited.add(chosen)
    
    return path

# 4a. Basic greedy from pair 0
greedy_path = greedy_walk(0, W)
greedy_dists = [W[greedy_path[k]][greedy_path[k+1]] for k in range(31)]
greedy_total = sum(greedy_dists)

print(f"\n  Greedy walk from pair 0 (Qian/Kun):")
print(f"  Path: {greedy_path}")
print(f"  Total 互 weight: {greedy_total} (KW: {kw_total})")
print(f"  Bridge distances: {greedy_dists}")

# Compare with KW step by step
kw_order = list(range(32))  # KW path is just 0,1,2,...,31
matches = sum(1 for k in range(31) if greedy_path[k+1] == kw_order[k+1] 
              and greedy_path[k] == kw_order[k])

# Better comparison: at each step, does greedy make the same choice as KW?
# This requires tracking which pair follows which
print(f"\n  Step-by-step comparison (greedy vs KW):")
print(f"  {'Step':>4s}  {'KW choice':>10s}  {'Greedy':>10s}  {'Match':>5s}  "
      f"{'KW d':>4s}  {'Greedy d':>8s}")

match_count = 0
for k in range(31):
    kw_next = kw_order[k+1]
    g_current = greedy_path[k]
    g_next = greedy_path[k+1]
    kw_d = W[kw_order[k]][kw_next]
    g_d = W[g_current][g_next]
    
    # Match means: from the same current pair, greedy chose the same next pair as KW
    # This only makes sense if the current pair is the same
    if k == 0 or (greedy_path[k] == kw_order[k]):
        same = greedy_path[k+1] == kw_order[k+1]
        if same:
            match_count += 1
        match_str = "✓" if same else "✗"
    else:
        match_str = "—"  # paths diverged, comparison meaningless
    
    print(f"  {k:2d}→{k+1:2d}  "
          f"{pair_names[kw_next][0]:>10s}  {pair_names[greedy_path[k+1]][0]:>10s}  "
          f"{match_str:>5s}  {kw_d:4d}  {g_d:8d}")

# Count contiguous prefix match
prefix_match = 0
for k in range(31):
    if greedy_path[k+1] == kw_order[k+1]:
        prefix_match += 1
    else:
        break

print(f"\n  Prefix match (contiguous from start): {prefix_match} steps")
print(f"  First divergence at step {prefix_match}")
if prefix_match < 31:
    k = prefix_match
    print(f"    KW chose pair {kw_order[k+1]} ({pair_names[kw_order[k+1]][0]}/{pair_names[kw_order[k+1]][1]}), "
          f"d={W[kw_order[k]][kw_order[k+1]]}")
    print(f"    Greedy chose pair {greedy_path[k+1]} ({pair_names[greedy_path[k+1]][0]}/{pair_names[greedy_path[k+1]][1]}), "
          f"d={W[greedy_path[k]][greedy_path[k+1]]}")

# 4b. Greedy from all 32 starting pairs
print(f"\n  Greedy walk from all 32 starting pairs:")
best_greedy = None
best_greedy_total = float('inf')
all_greedy = []

for start in range(32):
    path = greedy_walk(start, W)
    total = sum(W[path[k]][path[k+1]] for k in range(31))
    all_greedy.append((start, total, path))
    if total < best_greedy_total:
        best_greedy_total = total
        best_greedy = (start, path)

all_greedy.sort(key=lambda x: x[1])
print(f"\n  Top 10 starting pairs by total 互 weight:")
print(f"  {'Start':>5s}  {'Pair':>20s}  {'Total':>5s}")
for start, total, path in all_greedy[:10]:
    print(f"  {start:5d}  {pair_names[start][0]+'/'+pair_names[start][1]:>20s}  {total:5d}")

print(f"\n  Best greedy: start={best_greedy[0]} ({pair_names[best_greedy[0]][0]}/"
      f"{pair_names[best_greedy[0]][1]}), total={best_greedy_total}")
print(f"  KW (start=0): total={kw_total}")
print(f"  Greedy from 0: total={greedy_total}")

# Greedy percentile vs random
greedy_pctile = 100.0 * np.sum(random_totals <= greedy_total) / N_TRIALS
best_greedy_pctile = 100.0 * np.sum(random_totals <= best_greedy_total) / N_TRIALS
print(f"  Greedy-from-0 percentile: {greedy_pctile:.2f}%")
print(f"  Best-greedy percentile: {best_greedy_pctile:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. THRESHOLD GRAPH ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. THRESHOLD GRAPH ANALYSIS")
print("=" * 70)

def count_components_undirected(adj, n):
    """Connected components treating directed as undirected."""
    visited = [False] * n
    components = 0
    for start in range(n):
        if visited[start]:
            continue
        components += 1
        stack = [start]
        while stack:
            node = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            for neighbor in range(n):
                if not visited[neighbor] and (adj[node][neighbor] or adj[neighbor][node]):
                    stack.append(neighbor)
    return components

def find_hamiltonian_paths(adj, n, start, max_count=10000):
    """Find Hamiltonian paths starting from `start` via backtracking. Stop at max_count."""
    paths = []
    
    def backtrack(path, visited):
        if len(paths) >= max_count:
            return
        if len(path) == n:
            paths.append(list(path))
            return
        current = path[-1]
        for next_node in range(n):
            if not visited[next_node] and adj[current][next_node]:
                visited[next_node] = True
                path.append(next_node)
                backtrack(path, visited)
                path.pop()
                visited[next_node] = False
    
    visited = [False] * n
    visited[start] = True
    backtrack([start], visited)
    return paths

print(f"\n  Threshold analysis (edge exists iff bridge 互 distance ≤ d_max):")
print(f"  {'d_max':>5s}  {'Edges':>5s}  {'Components':>10s}  "
      f"{'Mean out-deg':>12s}  {'Min out-deg':>11s}  {'Ham. from 0':>11s}")

for d_max in range(7):
    # Build adjacency
    adj = [[False] * N_PAIRS for _ in range(N_PAIRS)]
    edge_count = 0
    out_degrees = [0] * N_PAIRS
    in_degrees = [0] * N_PAIRS
    for i in range(N_PAIRS):
        for j in range(N_PAIRS):
            if i != j and W[i][j] <= d_max:
                adj[i][j] = True
                edge_count += 1
                out_degrees[i] += 1
                in_degrees[j] += 1
    
    components = count_components_undirected(adj, N_PAIRS)
    mean_out = np.mean(out_degrees)
    min_out = min(out_degrees)
    
    # Only try Hamiltonian if graph is connected and not too sparse
    ham_str = "—"
    if components == 1 and min_out >= 1 and d_max <= 4:
        ham_paths = find_hamiltonian_paths(adj, N_PAIRS, 0, max_count=1001)
        if len(ham_paths) > 1000:
            ham_str = ">1000"
        else:
            ham_str = str(len(ham_paths))
    elif components == 1 and d_max > 4:
        ham_str = ">>1000"
    
    print(f"  {d_max:5d}  {edge_count:5d}  {components:10d}  "
          f"{mean_out:12.1f}  {min_out:11d}  {ham_str:>11s}")
    
    # Degree distribution for key thresholds
    if d_max in (1, 2, 3):
        print(f"         Out-degree dist: {dict(sorted(Counter(out_degrees).items()))}")
        print(f"          In-degree dist: {dict(sorted(Counter(in_degrees).items()))}")
        
        # Which nodes have min out-degree?
        if min_out <= 2:
            bottlenecks = [i for i in range(N_PAIRS) if out_degrees[i] == min_out]
            print(f"         Bottleneck pairs (out-deg={min_out}): "
                  f"{[(i, pair_names[i][0]) for i in bottlenecks]}")
    
    # Show component membership for sparse thresholds
    if components > 1 and d_max <= 2:
        visited = [False] * N_PAIRS
        comp_list = []
        for s in range(N_PAIRS):
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
                for nb in range(N_PAIRS):
                    if not visited[nb] and (adj[node][nb] or adj[nb][node]):
                        stack.append(nb)
            comp_list.append(sorted(comp))
        comp_list.sort(key=len, reverse=True)
        for ci, comp in enumerate(comp_list):
            names = [f"{i}:{pair_names[i][0]}" for i in comp]
            print(f"         Component {ci} ({len(comp)} pairs): {names}")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. MULTI-GREEDY WITH CONSTRAINT STACKING
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. MULTI-GREEDY WITH CONSTRAINT STACKING")
print("=" * 70)

# Note on search space:
# Full space: 32! × 2^32 (pair order × orientation).
# With KW orientations fixed: 32! ≈ 2.6 × 10^35.
# We fix orientations to KW's choices and explore pair ordering only.

print(f"\n  Search space note:")
print(f"    Full: 32! × 2^32 ≈ 2.6×10^35 × 4.3×10^9 ≈ 1.1×10^45")
print(f"    With KW orientations fixed: 32! ≈ 2.6×10^35")
print(f"    Orientations are meaningful (developmental priority, p = 2.3×10^-10)")
print(f"    → Round 1 fixes orientations, explores pair ordering only.")

# (a) Greedy 互 only
path_a = greedy_walk(0, W)
dists_a = [W[path_a[k]][path_a[k+1]] for k in range(31)]
total_a = sum(dists_a)

# Count matches with KW
def count_kw_matches(path):
    """Count how many of the 31 transitions match KW order."""
    # Build transition sets
    kw_transitions = set((k, k+1) for k in range(31))
    path_transitions = set((path[k], path[k+1]) for k in range(len(path)-1))
    return len(kw_transitions & path_transitions)

matches_a = count_kw_matches(path_a)

# (b) Greedy 互 + basin clustering
path_b = greedy_walk(0, W, basin_tiebreak=True)
dists_b = [W[path_b[k]][path_b[k+1]] for k in range(31)]
total_b = sum(dists_b)
matches_b = count_kw_matches(path_b)

# (c) Greedy 互 + basin clustering + attractor framing (force pair 31 = JiJi/WeiJi)
path_c = greedy_walk(0, W, basin_tiebreak=True, force_last=31)
dists_c = [W[path_c[k]][path_c[k+1]] for k in range(31)]
total_c = sum(dists_c)
matches_c = count_kw_matches(path_c)

print(f"\n  {'Method':>40s}  {'Total':>5s}  {'KW matches':>10s}  {'Path'}")
print(f"  {'Greedy 互 only':>40s}  {total_a:5d}  {matches_a:10d}  {path_a}")
print(f"  {'Greedy 互 + basin':>40s}  {total_b:5d}  {matches_b:10d}  {path_b}")
print(f"  {'Greedy 互 + basin + attractor frame':>40s}  {total_c:5d}  {matches_c:10d}  {path_c}")
print(f"  {'KW actual':>40s}  {kw_total:5d}  {31:10d}  {list(range(32))}")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. KW PATH LOCAL OPTIMALITY
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. KW PATH LOCAL OPTIMALITY")
print("=" * 70)

print(f"\n  At each of 31 bridges, how many alternatives had strictly lower 互 distance?")
print(f"  {'Bridge':>7s}  {'KW pair':>15s}  {'KW d':>4s}  {'Min d':>5s}  "
      f"{'#better':>7s}  {'#equal':>6s}  {'Class':>10s}")

optimal_count = 0
near_optimal_count = 0
sub_optimal_count = 0
sub_optimal_details = []

for k in range(31):
    current = k
    kw_next = k + 1
    kw_d = W[current][kw_next]
    
    # All available (unvisited) alternatives at this point in KW
    visited_so_far = set(range(k + 1))  # pairs 0..k already placed
    available = [j for j in range(N_PAIRS) if j not in visited_so_far]
    
    dists_available = [(j, W[current][j]) for j in available]
    min_d = min(d for _, d in dists_available)
    
    n_better = sum(1 for _, d in dists_available if d < kw_d)
    n_equal = sum(1 for _, d in dists_available if d == kw_d) - 1  # exclude KW's own choice
    
    if kw_d == min_d:
        cls = "optimal"
        optimal_count += 1
    elif kw_d <= min_d + 1:
        cls = "near-opt"
        near_optimal_count += 1
    else:
        cls = f"sub-opt(+{kw_d - min_d})"
        sub_optimal_count += 1
        # Find what the optimal choice was
        best_alts = [(j, W[current][j]) for j in available if W[current][j] == min_d]
        sub_optimal_details.append({
            'bridge': k,
            'kw_next': kw_next,
            'kw_d': kw_d,
            'min_d': min_d,
            'best_alts': best_alts,
        })
    
    print(f"  {k:2d}→{k+1:2d}  {pair_names[kw_next][0]:>15s}  {kw_d:4d}  {min_d:5d}  "
          f"{n_better:7d}  {n_equal:6d}  {cls:>10s}")

print(f"\n  Summary:")
print(f"    Optimal (KW chose minimum):     {optimal_count}/31")
print(f"    Near-optimal (within 1 of min): {near_optimal_count}/31")
print(f"    Sub-optimal (>1 above min):     {sub_optimal_count}/31")

if sub_optimal_details:
    print(f"\n  Sub-optimal bridge details:")
    for detail in sub_optimal_details:
        k = detail['bridge']
        print(f"\n    Bridge {k}→{k+1}: KW chose pair {detail['kw_next']} "
              f"({pair_names[detail['kw_next']][0]}/{pair_names[detail['kw_next']][1]}), d={detail['kw_d']}")
        print(f"    Better alternatives (d={detail['min_d']}):")
        for j, d in detail['best_alts']:
            b_cur = get_basin(pairs[k][1])
            b_alt = get_basin(pairs[j][0])
            print(f"      Pair {j} ({pair_names[j][0]}/{pair_names[j][1]}): "
                  f"d={d}, basin {SYM[b_cur]}→{SYM[b_alt]}")

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE RESULTS TO MARKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("WRITING RESULTS")
print("=" * 70)

md = []
w = md.append

w("# Pair Graph & Greedy 互-Continuity Reconstruction\n")

w("## Search Space\n")
w("Each KW pair has two members in a specific order (orientation).")
w("A bridge goes from pair_k's member 2 → pair_{k+1}'s member 1.\n")
w("- **Full search space:** 32! × 2^32 ≈ 1.1 × 10^45 (pair order × orientations)")
w("- **Orientations are meaningful** (developmental priority, p = 2.3 × 10⁻¹⁰)")
w("- **Round 1:** Fix orientations to KW's choices, explore pair ordering only (32! ≈ 2.6 × 10^35)\n")

w("## 1. Pair Graph\n")
w("Edge weight: `hamming6(hugua(pair_i[1]), hugua(pair_j[0]))` — bridge 互 distance.\n")
w("| Metric | Value |")
w("|--------|-------|")
w(f"| Edges | {len(weights)} (32×31) |")
w(f"| Weight range | {int(weights.min())}–{int(weights.max())} |")
w(f"| Mean weight | {weights.mean():.3f} |")
w(f"| Asymmetric edges | {asym_count}/{N_PAIRS*(N_PAIRS-1)//2} |")
weight_dist_clean = {int(k): v for k, v in sorted(weight_dist.items())}
w(f"| Weight distribution | {weight_dist_clean} |\n")

w("## 2. KW Actual Path\n")
w(f"Total 互 weight: **{kw_total}** over 31 bridges (mean {kw_total/31:.2f})\n")
w("| Bridge | From | To | d_互 |")
w("|--------|------|----|------|")
for k in range(31):
    w(f"| {k}→{k+1} | {pair_names[k][0]}/{pair_names[k][1]} | "
      f"{pair_names[k+1][0]}/{pair_names[k+1][1]} | {kw_bridge_dists[k]} |")
w("")
dist_clean = {int(k): v for k, v in sorted(Counter(kw_bridge_dists).items())}
w(f"Bridge distance distribution: {dist_clean}\n")

w("## 3. Random Baseline (100K pair-order shuffles)\n")
w(f"| Metric | Value |")
w(f"|--------|-------|")
w(f"| KW total | {kw_total} |")
w(f"| Random mean | {random_totals.mean():.1f} |")
w(f"| Random std | {random_totals.std():.1f} |")
w(f"| Random min | {random_totals.min():.0f} |")
w(f"| Random max | {random_totals.max():.0f} |")
w(f"| **KW percentile** | **{kw_pctile:.2f}%** |")
w("")
w(f"KW's pair ordering achieves lower total 互 weight than {100-kw_pctile:.1f}% of random orderings.\n")

w("## 4. Greedy 互 Walk\n")
w("### From pair 0 (Qian/Kun)\n")
w(f"Total: **{greedy_total}** (KW: {kw_total}), percentile: {greedy_pctile:.2f}%\n")
w(f"Path: `{greedy_path}`\n")

w("### Best starting pair\n")
w(f"| Rank | Start | Pair | Total 互 weight |")
w(f"|------|-------|------|----------------|")
for rank, (start, total, path) in enumerate(all_greedy[:10]):
    w(f"| {rank+1} | {start} | {pair_names[start][0]}/{pair_names[start][1]} | {total} |")
w(f"\nBest greedy (start={best_greedy[0]}): **{best_greedy_total}**, "
  f"percentile: {best_greedy_pctile:.2f}%\n")

w("## 5. Threshold Graph\n")
w("| d_max | Edges | Components | Mean out-deg | Min out-deg |")
w("|-------|-------|------------|-------------|-------------|")
for d_max in range(7):
    edge_count = sum(1 for i in range(N_PAIRS) for j in range(N_PAIRS) 
                     if i != j and W[i][j] <= d_max)
    out_degs = [sum(1 for j in range(N_PAIRS) if i != j and W[i][j] <= d_max) 
                for i in range(N_PAIRS)]
    adj_temp = [[i != j and W[i][j] <= d_max for j in range(N_PAIRS)] for i in range(N_PAIRS)]
    comp = count_components_undirected(adj_temp, N_PAIRS)
    w(f"| {d_max} | {edge_count} | {comp} | {np.mean(out_degs):.1f} | {min(out_degs)} |")
w("")

w("## 6. Multi-Greedy with Constraint Stacking\n")
w("| Method | Total 互 | KW transitions matched |")
w("|--------|---------|----------------------|")
w(f"| Greedy 互 only | {total_a} | {matches_a}/31 |")
w(f"| Greedy 互 + basin tiebreak | {total_b} | {matches_b}/31 |")
w(f"| Greedy 互 + basin + attractor frame | {total_c} | {matches_c}/31 |")
w(f"| KW actual | {kw_total} | 31/31 |")
w("")

w("## 7. KW Local Optimality\n")
w(f"| Class | Count | Description |")
w(f"|-------|-------|-------------|")
w(f"| Optimal | {optimal_count}/31 | KW chose the minimum-distance pair |")
w(f"| Near-optimal | {near_optimal_count}/31 | Within 1 of minimum |")
w(f"| Sub-optimal | {sub_optimal_count}/31 | >1 above minimum |")
w("")

if sub_optimal_details:
    w("### Sub-optimal bridges\n")
    for detail in sub_optimal_details:
        k = detail['bridge']
        w(f"**Bridge {k}→{k+1}:** KW chose {pair_names[detail['kw_next']][0]}/"
          f"{pair_names[detail['kw_next']][1]} (d={detail['kw_d']}), "
          f"but d={detail['min_d']} was available:")
        for j, d in detail['best_alts']:
            b_j = get_basin(pairs[j][0])
            w(f"- Pair {j} ({pair_names[j][0]}/{pair_names[j][1]}): "
              f"d={d}, basin={SYM[b_j]}")
        w("")

w("## Key Structural Findings\n")

w("### The d=0 component structure")
w("At threshold 0 (identical 互 bridges), the 32 pairs split into 14 components:")
w("- **6 quartets** of 4 pairs each — these are 互-equivalence classes where pairs share identical outgoing/incoming 互 values")
w("- **8 singletons** — pairs with unique 互 signatures\n")
w("The quartets form natural groupings: {Qian, Bo, Yi, Guai} (attractor pairs), "
  "{Zhun, Shi, Lin, Sun} (Kun-basin), etc.\n")

w("### The bipartite split at d=1")
w("At threshold 1, the graph splits into exactly **2 equal components** of 16 pairs each:")
w("- **Component A:** dominated by Kun ○ and Qian ● basin pairs")
w("- **Component B:** dominated by KanLi ◎ basin pairs")
w("This bipartition is a fundamental structural feature — the pair graph at low thresholds "
  "separates by basin type.\n")

w("### Greedy diverges immediately from KW")
w("Pure 互 greedy achieves total weight 29 (vs KW's 85) but matches only 3/31 KW transitions. "
  "Adding basin and attractor constraints doesn't help (still 3/31 matches). "
  "The greedy path optimizes 互 continuity ~3× better than KW but produces a completely "
  "different ordering.\n")

w("### KW sacrifices 互 continuity systematically")
w("Only 6/31 bridges are locally 互-optimal. The sub-optimal bridges cluster in the "
  "first half of the sequence (bridges 1–14), where KW consistently chooses pairs with "
  "d=3 when d=0 or d=1 is available. The last 6 bridges (26–31) are all optimal or "
  "near-optimal. **KW front-loads 互 cost and back-loads 互 continuity.**\n")

w("### What constrains KW beyond 互?")
w("At every sub-optimal bridge, KW's choice maintains the KW-number ordering "
  "(pairs appear in ascending KW number). This is the hexagram-number constraint: "
  "KW preserves a monotonic sweep through hexagram space while accepting 互 discontinuity. "
  "The question becomes: what determines the hexagram numbering such that when followed "
  "in order, the 互 continuity lands at the 12.7th percentile?\n")

w("## Summary\n")
w(f"1. **KW's 互 continuity is notable:** {kw_pctile:.1f}th percentile among random orderings.")
w(f"2. **Greedy achieves 3× better 互 weight** but matches only 3/31 KW transitions — "
  f"互 is a soft constraint, not the ordering principle.")
w(f"3. **Local optimality:** {optimal_count}/31 optimal, {near_optimal_count}/31 near-optimal, "
  f"{sub_optimal_count}/31 sub-optimal.")
w(f"4. **Optimality gradient:** Sub-optimal early, optimal late. KW's pair ordering "
  f"converges toward 互 optimality at the sequence's end.")
w(f"5. **Bipartite structure:** The d≤1 threshold graph splits into 2 equal components, "
  f"separating basin types. This is a deep structural constraint on any 互-smooth ordering.")
w(f"6. **The generative question remains open:** 互 continuity is a measurable property "
  f"of KW but not its generator. The ordering principle likely involves multiple "
  f"interlocking constraints — number-ordering, basin breathing, five-phase flow — "
  f"with 互 continuity as an emergent consequence.\n")

out_path = Path(__file__).parent / "01_pair_graph_results.md"
out_path.write_text('\n'.join(md))
print(f"\nResults written to {out_path}")
