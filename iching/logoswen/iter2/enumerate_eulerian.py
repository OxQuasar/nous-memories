"""
Thread A + D: Enumerate ALL Eulerian paths through the orbit multigraph.
Record self-loop positions for each path.

The orbit multigraph has 8 nodes (orbits) and 31 directed edges (bridges).
Each orbit is visited exactly 4 times (4 pairs per orbit = 8 hexagrams / 2).
An Eulerian path uses each edge exactly once, starting at Qian(000) and ending at Tai(111).

Uses connectivity pruning: at each step, check that the remaining graph 
(plus the current position) can still reach an Eulerian path to the endpoint.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import time
import json

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): 'Qian',
    (1,1,0): 'Zhun',
    (1,0,1): 'Xu',
    (0,1,0): 'Shi',
    (0,0,1): 'XChu',
    (1,1,1): 'Tai',
    (1,0,0): 'Bo',
    (0,1,1): 'WWang',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])


# ─── Build the multigraph from KW bridges ───────────────────────────────────

edge_count = Counter()
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    edge_count[(sig_a, sig_b)] += 1

print("Orbit multigraph edges (with multiplicities):")
for (u, v), cnt in sorted(edge_count.items()):
    print(f"  {ORBIT_NAMES[u]} → {ORBIT_NAMES[v]}: {cnt}×")
total_edges = sum(edge_count.values())
print(f"Total edges: {total_edges}")


# ─── Enumerate ALL Eulerian paths with pruning ───────────────────────────────

def is_weakly_connected(remaining, current_node, end_node):
    """Check if the graph formed by remaining edges (plus current and end nodes) is weakly connected.
    All nodes with remaining edges must be in one weakly-connected component with current_node."""
    # Build undirected adjacency from remaining edges
    adj = defaultdict(set)
    nodes_with_edges = set()
    for (u, v), cnt in remaining.items():
        if cnt > 0:
            adj[u].add(v)
            adj[v].add(u)
            nodes_with_edges.add(u)
            nodes_with_edges.add(v)
    
    if not nodes_with_edges:
        return True  # no edges left, trivially connected
    
    # current_node must be in the component
    nodes_with_edges.add(current_node)
    
    # BFS from current_node
    visited = {current_node}
    queue = [current_node]
    while queue:
        node = queue.pop()
        for nb in adj.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    
    return nodes_with_edges.issubset(visited)


def enumerate_eulerian_paths(edge_count, start, end):
    """
    Enumerate ALL Eulerian paths with connectivity pruning.
    """
    remaining = dict(edge_count)
    
    # Build adjacency structure (sorted for determinism)
    adj = defaultdict(list)
    for (u, v) in edge_count:
        if v not in adj[u]:
            adj[u].append(v)
    for u in adj:
        adj[u].sort()
    
    paths = []
    path_count = [0]
    
    def dfs(node, depth):
        if depth == total_edges:
            if node == end:
                paths.append(list(current_path))
                path_count[0] += 1
                if path_count[0] % 10000 == 0:
                    print(f"  Found {path_count[0]} paths so far...")
            return
        
        for target in adj[node]:
            edge = (node, target)
            if remaining.get(edge, 0) > 0:
                remaining[edge] -= 1
                
                # Pruning: check weak connectivity of remaining graph
                if is_weakly_connected(remaining, target, end):
                    current_path.append(target)
                    dfs(target, depth + 1)
                    current_path.pop()
                
                remaining[edge] += 1
    
    current_path = [start]
    dfs(start, 0)
    return paths


print(f"\nEnumerating ALL Eulerian paths from {ORBIT_NAMES[(0,0,0)]} to {ORBIT_NAMES[(1,1,1)]}...")
t0 = time.time()
all_paths = enumerate_eulerian_paths(edge_count, (0,0,0), (1,1,1))
t1 = time.time()
print(f"Found {len(all_paths)} Eulerian paths in {t1-t0:.2f}s")


# ─── Verify the KW walk is among them ────────────────────────────────────────

# The orbit walk: orbit of each pair
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))

print(f"\nKW orbit walk (32 nodes = 31 edges):")
for i, o in enumerate(kw_orbit_walk):
    print(f"  Pair {i:2d}: {ORBIT_NAMES[o]}")

kw_found = kw_orbit_walk in all_paths
print(f"\nKW walk found among enumerated paths: {kw_found}")
if kw_found:
    kw_index = all_paths.index(kw_orbit_walk)
    print(f"KW walk is path #{kw_index}")


# ─── Thread D: Self-loop analysis ────────────────────────────────────────────

print(f"\n{'='*70}")
print("THREAD D: SELF-LOOP PLACEMENT")
print(f"{'='*70}")

# Which edges are self-loops?
self_loop_edges = {(u,v): cnt for (u,v), cnt in edge_count.items() if u == v}
print(f"\nSelf-loop edges in multigraph:")
for (u,v), cnt in self_loop_edges.items():
    print(f"  {ORBIT_NAMES[u]}: {cnt}×")

# For each path, find where self-loops occur
qian_loop_positions = []
wwang_loop_positions = []

for pi, path in enumerate(all_paths):
    for step in range(len(path) - 1):
        u, v = path[step], path[step+1]
        if u == v == (0,0,0):
            qian_loop_positions.append(step)
        elif u == v == (0,1,1):
            wwang_loop_positions.append(step)

print(f"\nSelf-loop position distributions across {len(all_paths)} paths:")

qian_counter = Counter(qian_loop_positions)
print(f"\n  Qian(000) self-loop at bridge position:")
for pos in sorted(qian_counter.keys()):
    pct = 100 * qian_counter[pos] / len(all_paths)
    bar = '█' * max(1, int(pct / 2))
    print(f"    Bridge {pos:2d}: {qian_counter[pos]:6d} paths ({pct:5.1f}%) {bar}")

wwang_counter = Counter(wwang_loop_positions)
print(f"\n  WWang(011) self-loop at bridge position:")
for pos in sorted(wwang_counter.keys()):
    pct = 100 * wwang_counter[pos] / len(all_paths)
    bar = '█' * max(1, int(pct / 2))
    print(f"    Bridge {pos:2d}: {wwang_counter[pos]:6d} paths ({pct:5.1f}%) {bar}")

# KW-specific self-loop positions
print(f"\n  King Wen self-loop positions:")
for step in range(len(kw_orbit_walk) - 1):
    if kw_orbit_walk[step] == kw_orbit_walk[step+1]:
        print(f"    Bridge {step}: {ORBIT_NAMES[kw_orbit_walk[step]]} self-loop")

# Joint distribution
joint_positions = []
for pi, path in enumerate(all_paths):
    q_pos = None
    w_pos = None
    for step in range(len(path) - 1):
        u, v = path[step], path[step+1]
        if u == v == (0,0,0):
            q_pos = step
        elif u == v == (0,1,1):
            w_pos = step
    if q_pos is not None and w_pos is not None:
        joint_positions.append((q_pos, w_pos))

joint_counter = Counter(joint_positions)
print(f"\n  Joint (Qian_pos, WWang_pos) distribution — top 30:")
for (qp, wp), cnt in joint_counter.most_common(30):
    pct = 100 * cnt / len(all_paths)
    print(f"    Qian@B{qp:2d}, WWang@B{wp:2d}: {cnt:6d} paths ({pct:5.1f}%)")

kw_self_loops = []
for step in range(len(kw_orbit_walk) - 1):
    if kw_orbit_walk[step] == kw_orbit_walk[step+1]:
        kw_self_loops.append(step)

print(f"\n  KW self-loop positions: {kw_self_loops}")
if len(kw_self_loops) == 2:
    kw_joint = tuple(kw_self_loops)
    kw_count = joint_counter.get(kw_joint, 0)
    pct = 100 * kw_count / len(all_paths) if len(all_paths) > 0 else 0
    rank = sorted(joint_counter.values(), reverse=True).index(kw_count) + 1 if kw_count > 0 else "N/A"
    print(f"  KW joint {kw_joint}: {kw_count} paths ({pct:.2f}%), rank {rank} of {len(joint_counter)} unique positions")


# ─── Opening analysis ────────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("OPENING SEQUENCE ANALYSIS")
print(f"{'='*70}")

kw_opening_6 = tuple(kw_orbit_walk[:7])
print(f"KW opening (first 6 bridges): {[ORBIT_NAMES[o] for o in kw_opening_6]}")

opening_counter = Counter(tuple(p[:7]) for p in all_paths)
print(f"\nDistinct openings (first 6 bridges): {len(opening_counter)}")
print(f"Paths with KW opening: {opening_counter.get(kw_opening_6, 0)}")

# How many visit 6+ distinct orbits in first 6 bridges?
six_distinct = sum(1 for p in all_paths if len(set(p[:7])) >= 6)
print(f"Paths with ≥6 distinct orbits in first 6 bridges: {six_distinct} ({100*six_distinct/max(1,len(all_paths)):.1f}%)")

# First revisit position
first_revisit_pos = []
for p in all_paths:
    seen = set()
    for i, node in enumerate(p):
        if node in seen:
            first_revisit_pos.append(i)
            break
        seen.add(node)
    else:
        first_revisit_pos.append(len(p))

revisit_counter = Counter(first_revisit_pos)
print(f"\nFirst orbit revisit position:")
for pos in sorted(revisit_counter.keys()):
    pct = 100 * revisit_counter[pos] / len(all_paths)
    print(f"  Position {pos}: {revisit_counter[pos]} paths ({pct:.1f}%)")


# ─── Save paths for downstream use ──────────────────────────────────────────

output = {
    'total_paths': len(all_paths),
    'paths': [[(o[0], o[1], o[2]) for o in p] for p in all_paths],
    'kw_orbit_walk': [(o[0], o[1], o[2]) for o in kw_orbit_walk],
}

with open('/home/quasar/nous/logoswen/iter2/eulerian_paths.json', 'w') as f:
    json.dump(output, f)

print(f"\nSaved {len(all_paths)} paths to eulerian_paths.json")
print(f"\n{'='*70}")
print("ENUMERATION COMPLETE")
print(f"{'='*70}")
