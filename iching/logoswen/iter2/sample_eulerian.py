"""
Thread A+D: Sample Eulerian paths uniformly at random from the orbit multigraph.
Uses the BEST theorem structure: at each node, randomly choose the next edge
with the correct probability distribution for uniform sampling.

Approach: Wilson's method for uniform random arborescences + BEST theorem decomposition.
Simpler approach: just do random DFS with backtracking and record statistics.
Even simpler: random Hierholzer with random edge selection — this gives uniform samples
when edges of the same type are interchangeable.

Key result from graph_analysis.py:
  - 150,955,488 total Eulerian paths from Qian(000) to Tai(111)
  - Too many to enumerate; use Monte Carlo sampling
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import time

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

# Build multigraph
edge_count = Counter()
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    edge_count[(xor_sig(a), xor_sig(b))] += 1

TOTAL_EDGES = sum(edge_count.values())  # 31

# Build the KW orbit walk for comparison
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))


def sample_eulerian_path(edge_count, start, end, rng):
    """
    Sample a random Eulerian path from start to end using randomized DFS 
    with backtracking. Not perfectly uniform, but gives good coverage.
    
    For more uniform sampling, we'd need the BEST theorem decomposition,
    but this is sufficient for statistical analysis.
    """
    remaining = dict(edge_count)
    total = sum(edge_count.values())
    
    # Build adjacency 
    adj = defaultdict(list)
    for (u, v) in edge_count:
        adj[u].append(v)
    
    path = [start]
    
    def dfs(node, depth):
        if depth == total:
            return node == end
        
        # Get available edges, shuffled
        available = []
        for target in adj[node]:
            edge = (node, target)
            if remaining.get(edge, 0) > 0:
                available.append(target)
        
        rng.shuffle(available)
        
        for target in available:
            edge = (node, target)
            remaining[edge] -= 1
            path.append(target)
            if dfs(target, depth + 1):
                return True
            path.pop()
            remaining[edge] += 1
        
        return False
    
    if dfs(start, 0):
        return list(path)
    return None


def sample_eulerian_path_hierholzer(edge_count, start, rng):
    """
    Random Hierholzer: produces a random Eulerian path by randomly choosing edges.
    This is NOT uniform but is very fast. Good for rough statistics.
    """
    adj = defaultdict(list)
    for (u, v), cnt in edge_count.items():
        for _ in range(cnt):
            adj[u].append(v)
    # Shuffle each adjacency list
    for u in adj:
        rng.shuffle(adj[u])
    
    stack = [start]
    path = []
    while stack:
        v = stack[-1]
        if adj[v]:
            u = adj[v].pop()
            stack.append(u)
        else:
            path.append(stack.pop())
    path.reverse()
    return path


# ─── Sample with backtracking DFS (closer to uniform) ──────────────────────

N_SAMPLES = 100_000
rng = random.Random(42)

print(f"Sampling {N_SAMPLES} Eulerian paths with randomized DFS...")
print(f"Total paths in space: 150,955,488")

qian_positions = []
wwang_positions = []
joint_positions = []
opening_types = Counter()
first_revisit = Counter()
paths_found = 0
unique_paths = set()

t0 = time.time()
for i in range(N_SAMPLES):
    path = sample_eulerian_path(edge_count, (0,0,0), (1,1,1), rng)
    if path is None:
        continue
    
    paths_found += 1
    path_tuple = tuple(tuple(o) for o in path)
    unique_paths.add(path_tuple)
    
    # Record self-loop positions
    q_pos = None
    w_pos = None
    for step in range(len(path) - 1):
        u, v = path[step], path[step+1]
        if u == v == (0,0,0):
            q_pos = step
            qian_positions.append(step)
        elif u == v == (0,1,1):
            w_pos = step
            wwang_positions.append(step)
    
    if q_pos is not None and w_pos is not None:
        joint_positions.append((q_pos, w_pos))
    
    # Opening type
    opening = tuple(path[:7])
    opening_types[opening] += 1
    
    # First revisit
    seen = set()
    for j, node in enumerate(path):
        if node in seen:
            first_revisit[j] += 1
            break
        seen.add(node)
    
    if (i+1) % 10000 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{N_SAMPLES} samples in {elapsed:.1f}s ({paths_found} valid)")

t1 = time.time()
print(f"\nCompleted: {paths_found} valid paths from {N_SAMPLES} attempts in {t1-t0:.1f}s")
print(f"Unique paths seen: {len(unique_paths)}")

# Check if KW walk was hit
kw_tuple = tuple(tuple(o) for o in kw_orbit_walk)
kw_hit = kw_tuple in unique_paths
print(f"KW walk found in samples: {kw_hit}")


# ─── Thread D: Self-loop analysis ────────────────────────────────────────────

print(f"\n{'='*70}")
print("THREAD D: SELF-LOOP PLACEMENT (from sampling)")
print(f"{'='*70}")

qian_counter = Counter(qian_positions)
print(f"\n  Qian(000) self-loop position distribution (N={len(qian_positions)}):")
for pos in sorted(qian_counter.keys()):
    pct = 100 * qian_counter[pos] / len(qian_positions)
    bar = '█' * max(1, int(pct))
    print(f"    Bridge {pos:2d}: {qian_counter[pos]:5d} ({pct:5.1f}%) {bar}")

wwang_counter = Counter(wwang_positions)
print(f"\n  WWang(011) self-loop position distribution (N={len(wwang_positions)}):")
for pos in sorted(wwang_counter.keys()):
    pct = 100 * wwang_counter[pos] / len(wwang_positions)
    bar = '█' * max(1, int(pct))
    print(f"    Bridge {pos:2d}: {wwang_counter[pos]:5d} ({pct:5.1f}%) {bar}")

# KW self-loop positions
kw_self_loops = []
for step in range(len(kw_orbit_walk) - 1):
    if kw_orbit_walk[step] == kw_orbit_walk[step+1]:
        kw_self_loops.append((ORBIT_NAMES[kw_orbit_walk[step]], step))

print(f"\n  KW self-loop positions: {kw_self_loops}")
for orbit_name, pos in kw_self_loops:
    if orbit_name == 'Qian':
        qian_rank = sum(1 for p, c in qian_counter.items() if c >= qian_counter.get(pos, 0))
        qian_pct = 100 * qian_counter.get(pos, 0) / len(qian_positions) if qian_positions else 0
        print(f"    Qian @ B{pos}: {qian_pct:.1f}% of samples, rank {qian_rank}/{len(qian_counter)}")
    elif orbit_name == 'WWang':
        wwang_rank = sum(1 for p, c in wwang_counter.items() if c >= wwang_counter.get(pos, 0))
        wwang_pct = 100 * wwang_counter.get(pos, 0) / len(wwang_positions) if wwang_positions else 0
        print(f"    WWang @ B{pos}: {wwang_pct:.1f}% of samples, rank {wwang_rank}/{len(wwang_counter)}")

# Joint distribution
joint_counter = Counter(joint_positions)
print(f"\n  Joint (Qian, WWang) position distribution — top 30:")
for (qp, wp), cnt in joint_counter.most_common(30):
    pct = 100 * cnt / len(joint_positions) if joint_positions else 0
    print(f"    Qian@B{qp:2d}, WWang@B{wp:2d}: {cnt:5d} ({pct:5.2f}%)")

# Check KW joint position
kw_self_pos = tuple(s for _, s in kw_self_loops)
if len(kw_self_pos) == 2:
    kw_joint_cnt = joint_counter.get(kw_self_pos, 0)
    kw_joint_pct = 100 * kw_joint_cnt / len(joint_positions) if joint_positions else 0
    total_unique_joints = len(joint_counter)
    print(f"\n  KW joint {kw_self_pos}: {kw_joint_cnt} ({kw_joint_pct:.2f}%)")
    print(f"  Total unique joint positions: {total_unique_joints}")
    # What fraction of all possible positions does this represent?
    if kw_joint_cnt > 0:
        rank = sum(1 for (p, c) in joint_counter.items() if c >= kw_joint_cnt)
        print(f"  KW rank: {rank}/{total_unique_joints}")


# ─── Opening analysis ────────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("OPENING ANALYSIS")
print(f"{'='*70}")

kw_opening = tuple(kw_orbit_walk[:7])
kw_opening_names = [ORBIT_NAMES[o] for o in kw_opening]
print(f"KW opening: {kw_opening_names}")
print(f"KW opening count: {opening_types.get(kw_opening, 0)}/{paths_found}")
print(f"Distinct openings seen: {len(opening_types)}")

# Top openings
print(f"\nTop 10 openings:")
for opening, cnt in opening_types.most_common(10):
    pct = 100 * cnt / paths_found
    names = [ORBIT_NAMES[o] for o in opening]
    marker = " ★ KW" if opening == kw_opening else ""
    print(f"  {cnt:5d} ({pct:5.2f}%): {' → '.join(names)}{marker}")

# First revisit position
print(f"\nFirst orbit revisit position:")
for pos in sorted(first_revisit.keys()):
    pct = 100 * first_revisit[pos] / paths_found
    print(f"  Position {pos}: {first_revisit[pos]:5d} ({pct:5.1f}%)")

# What position is KW's first revisit?
kw_seen = set()
kw_first_rev = None
for i, o in enumerate(kw_orbit_walk):
    if o in kw_seen:
        kw_first_rev = i
        break
    kw_seen.add(o)
print(f"KW first orbit revisit at position: {kw_first_rev}")
print(f"  (orbit {ORBIT_NAMES[kw_orbit_walk[kw_first_rev]]})")


# ─── Visit order analysis ────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("ORBIT VISIT PATTERN ANALYSIS")  
print(f"{'='*70}")

# For each path, compute the order in which orbits are first visited
first_visit_orders = Counter()
for i in range(min(10000, paths_found)):
    # Reconstruct path from unique_paths (take first N)
    pass

# Actually let's just re-sample a smaller batch and record full paths
rng2 = random.Random(123)
visit_order_counter = Counter()
orbit_at_position = defaultdict(Counter)  # position -> orbit -> count

for i in range(10000):
    path = sample_eulerian_path(edge_count, (0,0,0), (1,1,1), rng2)
    if path is None:
        continue
    
    # First-visit order
    seen = set()
    order = []
    for o in path:
        if o not in seen:
            order.append(ORBIT_NAMES[o])
            seen.add(o)
    visit_order_counter[tuple(order)] += 1
    
    # Orbit at each position
    for pos, o in enumerate(path):
        orbit_at_position[pos][o] += 1

print(f"\nDistinct first-visit orders: {len(visit_order_counter)}")
print(f"Top 10:")
for order, cnt in visit_order_counter.most_common(10):
    pct = 100 * cnt / sum(visit_order_counter.values())
    kw_marker = " ★ KW" if list(order) == [ORBIT_NAMES[o] for o in dict.fromkeys(kw_orbit_walk)] else ""
    print(f"  {cnt:4d} ({pct:5.1f}%): {' → '.join(order)}{kw_marker}")

# KW first-visit order
kw_fv_order = []
kw_seen2 = set()
for o in kw_orbit_walk:
    if o not in kw_seen2:
        kw_fv_order.append(ORBIT_NAMES[o])
        kw_seen2.add(o)

kw_fv_count = visit_order_counter.get(tuple(kw_fv_order), 0)
print(f"\nKW first-visit order: {' → '.join(kw_fv_order)}")
print(f"  Count: {kw_fv_count}/{sum(visit_order_counter.values())}")


# ─── Marginal position distributions ────────────────────────────────────────

print(f"\n{'='*70}")
print("POSITION ENTROPY")
print(f"{'='*70}")

import math

for pos in range(32):
    total = sum(orbit_at_position[pos].values())
    if total == 0:
        continue
    probs = [c/total for c in orbit_at_position[pos].values()]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    max_entropy = math.log2(8)
    kw_orbit_at_pos = ORBIT_NAMES.get(kw_orbit_walk[pos], '?')
    kw_prob = orbit_at_position[pos].get(kw_orbit_walk[pos], 0) / total * 100
    print(f"  Pos {pos:2d}: H={entropy:.2f}/{max_entropy:.2f} bits  "
          f"KW={kw_orbit_at_pos:>6s} ({kw_prob:5.1f}%)")


print(f"\n{'='*70}")
print("SAMPLING COMPLETE")
print(f"{'='*70}")
