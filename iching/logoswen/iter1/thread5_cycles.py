"""
Thread 5: Directed Graph Cycle Structure of King Wen Bridge Orbit Transitions

Questions:
- What are all simple cycles in the orbit transition graph?
- Does an Eulerian path/circuit exist?
- Is the actual walk Hamiltonian?
- Which edges are used once vs multiple times?
- How does the 31-step walk relate to the graph's topology?
"""

import sys
sys.path.insert(0, '../kingwen')

from collections import Counter, defaultdict
from itertools import permutations
from sequence import KING_WEN, all_bits

# ─── Build bridge data ─────────────────────────────────────────────────────

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): '1:Qian',
    (1,1,0): '2:Zhun',
    (1,0,1): '3:Xu',
    (0,1,0): '4:Shi',
    (0,0,1): '5:XChu',
    (1,1,1): '6:Tai',
    (1,0,0): '7:Bo',
    (0,1,1): '8:WWang',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

bridges = []
for k in range(31):
    idx_a = 2 * k + 1
    idx_b = 2 * k + 2
    a = tuple(M[idx_a])
    b = tuple(M[idx_b])
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    bridges.append({
        'idx': k,
        'num_a': idx_a + 1, 'num_b': idx_b + 1,
        'name_a': KING_WEN[idx_a][1], 'name_b': KING_WEN[idx_b][1],
        'sig_a': sig_a, 'sig_b': sig_b,
    })


# ─── 1. Build weighted directed graph ──────────────────────────────────────

print("=" * 70)
print("THREAD 5: ORBIT TRANSITION GRAPH — CYCLE STRUCTURE")
print("=" * 70)

# Adjacency: edge (u, v) -> count
edge_count = Counter()
edge_bridges = defaultdict(list)  # edge -> list of bridge indices

for b in bridges:
    u, v = b['sig_a'], b['sig_b']
    edge_count[(u, v)] += 1
    edge_bridges[(u, v)].append(b['idx'] + 1)

orbits = sorted(ORBIT_NAMES.keys())
adj = defaultdict(set)  # adjacency list (ignoring weights)

for (u, v) in edge_count:
    adj[u].add(v)

print(f"\n1. GRAPH SUMMARY")
print(f"   Nodes: {len(orbits)}")
print(f"   Directed edges (unique): {len(edge_count)}")
print(f"   Total edge traversals: {sum(edge_count.values())}")

self_loops = {e: c for e, c in edge_count.items() if e[0] == e[1]}
cross_edges = {e: c for e, c in edge_count.items() if e[0] != e[1]}
print(f"   Self-loops: {len(self_loops)} (traversals: {sum(self_loops.values())})")
print(f"   Cross-edges: {len(cross_edges)} (traversals: {sum(cross_edges.values())})")


# ─── 2. Degree analysis ───────────────────────────────────────────────────

print(f"\n2. DEGREE SEQUENCE")
print(f"   {'Orbit':<12s} Out  In  Self  OutNS  InNS")

for o in orbits:
    out_total = sum(edge_count[(o, v)] for v in orbits if (o, v) in edge_count)
    in_total = sum(edge_count[(u, o)] for u in orbits if (u, o) in edge_count)
    self_count = edge_count.get((o, o), 0)
    out_ns = out_total - self_count  # non-self out
    in_ns = in_total - self_count    # non-self in
    print(f"   {ORBIT_NAMES[o]:<12s}  {out_total:2d}   {in_total:2d}    {self_count:1d}     {out_ns:2d}     {in_ns:2d}")


# ─── 3. Eulerian path/circuit analysis ─────────────────────────────────────

print(f"\n3. EULERIAN PATH/CIRCUIT ANALYSIS")

# For Eulerian circuit: every node needs in-degree == out-degree
# For Eulerian path: exactly 2 nodes have |in - out| = 1, rest balanced
# We work with the multigraph (repeated edges count)

# Using cross-edges only (self-loops don't affect reachability but do affect Euler)
# Actually, for Eulerian analysis, include self-loops as they ARE edges to traverse.

degree_diff = {}  # out - in for each node
for o in orbits:
    out_d = sum(edge_count[(o, v)] for v in orbits if (o, v) in edge_count)
    in_d = sum(edge_count[(u, o)] for u in orbits if (u, o) in edge_count)
    degree_diff[o] = out_d - in_d
    
print(f"   Degree balance (out - in) per orbit:")
for o in orbits:
    name = ORBIT_NAMES[o]
    diff = degree_diff[o]
    status = "balanced" if diff == 0 else f"{'excess out' if diff > 0 else 'excess in'} by {abs(diff)}"
    print(f"     {name:<12s}: {diff:+d}  ({status})")

balanced = sum(1 for d in degree_diff.values() if d == 0)
excess_out = [o for o, d in degree_diff.items() if d > 0]
excess_in = [o for o, d in degree_diff.items() if d < 0]

if balanced == len(orbits):
    print(f"\n   ✓ ALL nodes balanced → Eulerian CIRCUIT exists (if graph is connected)")
elif len(excess_out) == 1 and len(excess_in) == 1:
    s = excess_out[0]
    t = excess_in[0]
    if degree_diff[s] == 1 and degree_diff[t] == -1:
        print(f"\n   ✓ Exactly one source ({ORBIT_NAMES[s]}) and one sink ({ORBIT_NAMES[t]})")
        print(f"     → Eulerian PATH exists from {ORBIT_NAMES[s]} to {ORBIT_NAMES[t]} (if graph is connected)")
    else:
        print(f"\n   ✗ Imbalance too large for Eulerian path")
        print(f"     Sources: {[ORBIT_NAMES[o] for o in excess_out]}")
        print(f"     Sinks: {[ORBIT_NAMES[o] for o in excess_in]}")
else:
    print(f"\n   ✗ No Eulerian path or circuit possible")
    print(f"     {balanced} balanced, {len(excess_out)} excess-out, {len(excess_in)} excess-in")


# ─── 4. Strongly connected components ─────────────────────────────────────

print(f"\n4. STRONGLY CONNECTED COMPONENTS")

# Kosaraju's algorithm (or just brute-force reachability for 8 nodes)
def reachable(start, adj_dict):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adj_dict.get(node, set()):
            if neighbor not in visited:
                stack.append(neighbor)
    return visited

# Forward reachability (ignoring self-loops for connectivity)
cross_adj = defaultdict(set)
rev_adj = defaultdict(set)
for (u, v) in edge_count:
    if u != v:
        cross_adj[u].add(v)
        rev_adj[v].add(u)

# Check if entire graph is strongly connected
all_nodes = set(orbits)
for start in orbits:
    fwd = reachable(start, cross_adj)
    bwd = reachable(start, rev_adj)
    if fwd == all_nodes and bwd == all_nodes:
        print(f"   From {ORBIT_NAMES[start]}: forward reaches ALL, backward reaches ALL")
        print(f"   → Graph is STRONGLY CONNECTED (single SCC)")
        break
    else:
        missing_fwd = all_nodes - fwd
        missing_bwd = all_nodes - bwd
        print(f"   From {ORBIT_NAMES[start]}: fwd misses {[ORBIT_NAMES[o] for o in missing_fwd]}, "
              f"bwd misses {[ORBIT_NAMES[o] for o in missing_bwd]}")


# ─── 5. All simple cycles ─────────────────────────────────────────────────

print(f"\n5. ALL SIMPLE CYCLES (Johnson's algorithm / brute force)")

def find_all_simple_cycles(adj_dict, nodes):
    """Find all simple cycles in a directed graph. Brute force for small graphs."""
    cycles = []
    
    def dfs(path, start):
        current = path[-1]
        for neighbor in adj_dict.get(current, set()):
            if neighbor == start and len(path) > 1:
                cycles.append(list(path))
            elif neighbor not in path and neighbor > start:
                # Only start cycles from the smallest node to avoid duplicates
                # Actually, we need to be more careful — use node ordering
                pass
        # Better: standard approach
        for neighbor in adj_dict.get(current, set()):
            if neighbor == start and len(path) > 1:
                cycles.append(list(path))
            elif neighbor not in set(path) and nodes.index(neighbor) >= nodes.index(start):
                dfs(path + [neighbor], start)
    
    node_list = sorted(nodes)
    for i, start in enumerate(node_list):
        dfs([start], start)
    
    return cycles

simple_cycles = find_all_simple_cycles(cross_adj, orbits)
print(f"   Found {len(simple_cycles)} simple cycles")

# Group by length
cycle_by_len = defaultdict(list)
for c in simple_cycles:
    cycle_by_len[len(c)].append(c)

for length in sorted(cycle_by_len.keys()):
    cycles = cycle_by_len[length]
    print(f"\n   Length {length}: {len(cycles)} cycles")
    for c in cycles:
        names = [ORBIT_NAMES[o] for o in c]
        edge_list = [(c[i], c[(i+1) % len(c)]) for i in range(len(c))]
        weights = [edge_count.get(e, 0) for e in edge_list]
        # Check if all edges exist
        all_exist = all(w > 0 for w in weights)
        if all_exist:
            print(f"     {'→'.join(names)}→{names[0]}  edges: {weights}")


# ─── 6. The actual 31-step walk ────────────────────────────────────────────

print(f"\n\n6. THE ACTUAL 31-STEP WALK")
print(f"   Orbit sequence traced by the King Wen bridge transitions:")

walk = [bridges[0]['sig_a']]  # starting orbit
for b in bridges:
    walk.append(b['sig_b'])

print(f"\n   Step  Bridge  From → To")
for i, b in enumerate(bridges):
    u, v = b['sig_a'], b['sig_b']
    cross = "→" if u != v else "⟲"
    print(f"   {i+1:2d}    B{b['idx']+1:2d}    {ORBIT_NAMES[u]:<12s} {cross} {ORBIT_NAMES[v]}")

# Orbit visit counts
orbit_visits = Counter(walk)
print(f"\n   Orbit visit counts (in walk of {len(walk)} nodes):")
for o in orbits:
    print(f"     {ORBIT_NAMES[o]:<12s}: {orbit_visits[o]}×")


# ─── 7. Edge usage analysis ───────────────────────────────────────────────

print(f"\n7. EDGE USAGE IN THE WALK")
print(f"   {'Edge':<30s}  Count  Bridges")

for (u, v), count in sorted(edge_count.items(), key=lambda x: -x[1]):
    u_name = ORBIT_NAMES[u]
    v_name = ORBIT_NAMES[v]
    bridge_list = edge_bridges[(u, v)]
    mark = "★" if count > 1 else " "
    same = " (self)" if u == v else ""
    print(f"   {u_name} → {v_name:<12s}:  {count}×   B{bridge_list}{same}  {mark}")

# Edges used once vs multiple
single_use = sum(1 for c in edge_count.values() if c == 1)
multi_use = sum(1 for c in edge_count.values() if c > 1)
print(f"\n   Single-use edges: {single_use}")
print(f"   Multi-use edges: {multi_use}")
print(f"   Max repetitions: {max(edge_count.values())}×")


# ─── 8. Hamiltonian analysis ──────────────────────────────────────────────

print(f"\n8. HAMILTONIAN PATH ANALYSIS")
print(f"   Does the walk visit every orbit before revisiting any?")

visited = set()
first_revisit = None
for i, o in enumerate(walk):
    if o in visited and first_revisit is None:
        first_revisit = (i, o)
    visited.add(o)

if first_revisit:
    idx, orb = first_revisit
    print(f"   First revisit: step {idx} revisits {ORBIT_NAMES[orb]}")
    print(f"   Orbits visited before first revisit: {idx}")
    print(f"   Walk is NOT Hamiltonian (revisits at step {idx} of 32)")
else:
    print(f"   Walk visits all {len(orbits)} orbits without revisit → HAMILTONIAN")

# Check for Hamiltonian subsequences
print(f"\n   Longest prefix visiting distinct orbits:")
visited_prefix = set()
for i, o in enumerate(walk):
    if o in visited_prefix:
        print(f"   Visited {len(visited_prefix)} distinct orbits before revisit at step {i}")
        print(f"   Prefix: {' → '.join(ORBIT_NAMES[walk[j]] for j in range(i))}")
        break
    visited_prefix.add(o)
else:
    print(f"   Entire walk visits distinct orbits!")


# ─── 9. Return patterns ───────────────────────────────────────────────────

print(f"\n9. RETURN PATTERNS")
print(f"   When does the walk return to previously visited orbits?")

visits_by_orbit = defaultdict(list)
for i, o in enumerate(walk):
    visits_by_orbit[o].append(i)

for o in orbits:
    steps = visits_by_orbit[o]
    if len(steps) > 1:
        gaps = [steps[i+1] - steps[i] for i in range(len(steps)-1)]
        print(f"   {ORBIT_NAMES[o]:<12s}: steps {steps}, gaps {gaps}")


# ─── 10. Cycle coverage ───────────────────────────────────────────────────

print(f"\n10. CYCLE COVERAGE — Which cycles does the walk traverse?")

# Extract consecutive edge pairs from the walk
walk_edges = [(walk[i], walk[i+1]) for i in range(len(walk)-1)]

for length in sorted(cycle_by_len.keys()):
    for c in cycle_by_len[length]:
        cycle_edges = set((c[i], c[(i+1) % len(c)]) for i in range(len(c)))
        # Check if the walk ever traverses this cycle consecutively
        for start in range(len(walk_edges) - len(c) + 1):
            subwalk = walk_edges[start:start + len(c)]
            subwalk_set = set(subwalk)
            if cycle_edges == subwalk_set:
                names = [ORBIT_NAMES[o] for o in c]
                print(f"   Cycle {'→'.join(names)} found at walk positions {start}-{start+len(c)-1}")


# Check which cycles have all their edges used at least once
print(f"\n   Cycles whose edges are all traversed (not necessarily consecutively):")
walk_edge_set = set(walk_edges)
for length in sorted(cycle_by_len.keys()):
    for c in cycle_by_len[length]:
        cycle_edges = [(c[i], c[(i+1) % len(c)]) for i in range(len(c))]
        if all(e in walk_edge_set for e in cycle_edges):
            names = [ORBIT_NAMES[o] for o in c]
            print(f"   Length {length}: {'→'.join(names)}→{names[0]}")


# ─── 11. Graph density and comparison ─────────────────────────────────────

print(f"\n11. GRAPH METRICS")
n = len(orbits)
max_edges = n * (n - 1)  # excluding self-loops
actual_edges = len(cross_edges)
print(f"   Density (cross-edges): {actual_edges}/{max_edges} = {actual_edges/max_edges:.3f}")
print(f"   Average out-degree (cross): {sum(len(cross_adj[o]) for o in orbits)/n:.2f}")
print(f"   Diameter:", end=" ")

# Compute diameter (longest shortest path)
from collections import deque
def bfs_distances(start, adj_dict):
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adj_dict.get(node, set()):
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist

max_dist = 0
for o in orbits:
    dists = bfs_distances(o, cross_adj)
    for v, d in dists.items():
        max_dist = max(max_dist, d)

print(f"{max_dist}")


print(f"\n{'=' * 70}")
print(f"THREAD 5 COMPLETE")
print(f"{'=' * 70}")
