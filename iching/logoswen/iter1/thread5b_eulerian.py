"""
Thread 5b: The Actual Walk vs. the Eulerian Path

Building on Thread 5's finding that an Eulerian path exists from Qian(000) to Tai(111).
Building on Thread 2's projection decomposition: mask = orbit_Δ ⊕ generator_dressing.

Questions:
- Can we construct an actual Eulerian path through the multigraph?
- Where does the King Wen walk diverge from an Eulerian traversal?
- The initial 6-step run (1→2→3→4→5→6) — forced or free?
- Self-loop placement in Eulerian vs actual walk
"""

import sys
sys.path.insert(0, '../kingwen')

from collections import Counter, defaultdict, deque
from copy import deepcopy
from sequence import KING_WEN, all_bits

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

# Build bridge data
bridges = []
for k in range(31):
    idx_a = 2 * k + 1
    idx_b = 2 * k + 2
    a = tuple(M[idx_a])
    b = tuple(M[idx_b])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'xor': xor,
        'num_a': idx_a + 1, 'num_b': idx_b + 1,
        'name_a': KING_WEN[idx_a][1], 'name_b': KING_WEN[idx_b][1],
        'sig_a': sig_a, 'sig_b': sig_b,
    })

# Build the multigraph: edge (u, v) with multiplicity
edge_count = Counter()
edge_bridges = defaultdict(list)
for b in bridges:
    u, v = b['sig_a'], b['sig_b']
    edge_count[(u, v)] += 1
    edge_bridges[(u, v)].append(b['idx'] + 1)

orbits = sorted(ORBIT_NAMES.keys())

# The actual walk
walk = [bridges[0]['sig_a']]
for b in bridges:
    walk.append(b['sig_b'])


print("=" * 70)
print("THREAD 5b: ACTUAL WALK vs. EULERIAN PATH")
print("=" * 70)


# ─── 1. Construct Eulerian paths via Hierholzer's algorithm ──────────────

print(f"\n1. CONSTRUCTING EULERIAN PATH (Hierholzer's algorithm)")
print(f"   Start: 1:Qian (000), Expected end: 6:Tai (111)")

def hierholzer(adj_multi, start):
    """
    Hierholzer's algorithm for Eulerian path in a directed multigraph.
    adj_multi: dict of {node: list of neighbors} where list has repeats for multiplicity.
    Returns list of nodes forming the Eulerian path.
    """
    adj = {k: list(v) for k, v in adj_multi.items()}
    stack = [start]
    path = []
    while stack:
        v = stack[-1]
        if adj.get(v):
            u = adj[v].pop()
            stack.append(u)
        else:
            path.append(stack.pop())
    path.reverse()
    return path

# Build adjacency with multiplicities
adj_multi = defaultdict(list)
for (u, v), count in edge_count.items():
    for _ in range(count):
        adj_multi[u].append(v)

# Run Hierholzer from Qian
start = (0, 0, 0)
euler_path = hierholzer(adj_multi, start)

# Verify it's valid
euler_edges_used = Counter()
for i in range(len(euler_path) - 1):
    euler_edges_used[(euler_path[i], euler_path[i+1])] += 1

valid = euler_edges_used == edge_count
total_edges_euler = sum(euler_edges_used.values())

print(f"   Eulerian path length: {len(euler_path)} nodes, {len(euler_path)-1} edges")
print(f"   Valid (all edges used exactly right): {valid}")
print(f"   Edges used: {total_edges_euler} (expected: {sum(edge_count.values())})")
print(f"   Start: {ORBIT_NAMES[euler_path[0]]}")
print(f"   End:   {ORBIT_NAMES[euler_path[-1]]}")

print(f"\n   Eulerian path orbit sequence:")
for i, o in enumerate(euler_path):
    print(f"     Step {i:2d}: {ORBIT_NAMES[o]}")


# ─── 2. Enumerate ALL Eulerian paths (or sample many) ────────────────────

print(f"\n2. ENUMERATING DISTINCT EULERIAN PATHS")
print(f"   (Backtracking search — may be large)")

def count_eulerian_paths(adj_multi, start, target_end=None):
    """Count all Eulerian paths from start (optionally ending at target_end).
    Uses DFS with backtracking. Returns list of paths (capped at max_paths).
    """
    adj = {k: list(v) for k, v in adj_multi.items()}
    total_edges = sum(len(v) for v in adj.values())
    paths = []
    max_paths = 100  # cap for tractability
    
    def dfs(node, edge_idx, current_path):
        if edge_idx == total_edges:
            if target_end is None or node == target_end:
                paths.append(list(current_path))
            return
        if len(paths) >= max_paths:
            return
        # Try each available neighbor
        neighbors = adj[node]
        # To avoid redundant exploration of identical edges, group by target
        tried = set()
        for i in range(len(neighbors)):
            if neighbors[i] is not None:
                target = neighbors[i]
                if target in tried:
                    continue
                tried.add(target)
                # Take this edge
                neighbors[i] = None
                current_path.append(target)
                dfs(target, edge_idx + 1, current_path)
                current_path.pop()
                neighbors[i] = target
                if len(paths) >= max_paths:
                    return
    
    dfs(start, 0, [start])
    return paths

# Rebuild adj_multi fresh
adj_multi2 = defaultdict(list)
for (u, v), count in edge_count.items():
    for _ in range(count):
        adj_multi2[u].append(v)

# Ensure all orbits have entries
for o in orbits:
    if o not in adj_multi2:
        adj_multi2[o] = []

euler_paths = count_eulerian_paths(adj_multi2, start, target_end=(1,1,1))

print(f"   Found {len(euler_paths)} Eulerian paths (capped at 100)")
if euler_paths:
    print(f"   All end at: {ORBIT_NAMES[euler_paths[0][-1]]}")
    
    # Check which start with the 1→2→3→4→5→6 opening
    kw_opening = [(0,0,0), (1,1,0), (1,0,1), (0,1,0), (0,0,1), (1,1,1)]
    matching_opening = [p for p in euler_paths if p[:6] == kw_opening]
    print(f"   Paths starting with 1→2→3→4→5→6 prefix: {len(matching_opening)}/{len(euler_paths)}")
    
    # Show a few
    print(f"\n   First Eulerian path found:")
    p = euler_paths[0]
    for i, o in enumerate(p):
        match_kw = " ← KW" if i < len(walk) and o == walk[i] else ""
        print(f"     Step {i:2d}: {ORBIT_NAMES[o]}{match_kw}")


# ─── 3. Compare actual walk to Eulerian paths ────────────────────────────

print(f"\n3. ACTUAL WALK vs EULERIAN PATHS")
print(f"   King Wen walk has {len(walk)} nodes, Eulerian path has {len(euler_path)} nodes")

# The KW walk uses 31 edges but the graph only has 26 unique edge types (with multiplicities totaling 31).
# Wait — check this carefully.
print(f"\n   Total edge traversals in multigraph: {sum(edge_count.values())}")
print(f"   Total edge traversals in KW walk: {len(walk) - 1}")
print(f"   These should be equal: {sum(edge_count.values()) == len(walk) - 1}")

# So the KW walk IS a traversal of all edges — it uses every edge the exact number of times.
# Is the KW walk itself an Eulerian path?
kw_edge_usage = Counter()
for i in range(len(walk) - 1):
    kw_edge_usage[(walk[i], walk[i+1])] += 1

is_eulerian = kw_edge_usage == edge_count
print(f"\n   KW walk uses every edge the correct number of times: {is_eulerian}")
if is_eulerian:
    print(f"   → The King Wen walk IS an Eulerian path!")
    print(f"   → Start: {ORBIT_NAMES[walk[0]]}, End: {ORBIT_NAMES[walk[-1]]}")
else:
    diff_over = {e: kw_edge_usage[e] - edge_count.get(e, 0) for e in kw_edge_usage if kw_edge_usage[e] > edge_count.get(e, 0)}
    diff_under = {e: edge_count[e] - kw_edge_usage.get(e, 0) for e in edge_count if edge_count[e] > kw_edge_usage.get(e, 0)}
    print(f"   Over-used edges: {diff_over}")
    print(f"   Under-used edges: {diff_under}")

# Check if KW walk is among the enumerated Eulerian paths
kw_in_euler = walk in euler_paths
print(f"   KW walk found in enumerated Eulerian paths: {kw_in_euler}")


# ─── 4. Visit counts comparison ──────────────────────────────────────────

print(f"\n4. ORBIT VISIT COUNTS")
print(f"   {'Orbit':<12s} KW walk  Euler path")

kw_visits = Counter(walk)
euler_visits = Counter(euler_path) if euler_path else Counter()

for o in orbits:
    ev = euler_visits.get(o, 0)
    print(f"   {ORBIT_NAMES[o]:<12s}   {kw_visits[o]:2d}       {ev:2d}")


# ─── 5. Self-loop placement ──────────────────────────────────────────────

print(f"\n5. SELF-LOOP PLACEMENT")

# In KW walk
print(f"   Self-loops in KW walk:")
for i in range(len(walk) - 1):
    if walk[i] == walk[i+1]:
        print(f"     Step {i}→{i+1}: {ORBIT_NAMES[walk[i]]} ⟲")

# In Eulerian path
print(f"   Self-loops in Eulerian path (first found):")
for i in range(len(euler_path) - 1):
    if euler_path[i] == euler_path[i+1]:
        print(f"     Step {i}→{i+1}: {ORBIT_NAMES[euler_path[i]]} ⟲")


# ─── 6. The opening sequence — forced or free? ──────────────────────────

print(f"\n6. OPENING SEQUENCE ANALYSIS")
print(f"   Is the 1→2→3→4→5→6 opening forced by graph structure?")

# From Qian(000), what are the possible first steps?
adj_simple = defaultdict(set)
for (u, v) in edge_count:
    adj_simple[u].add(v)

first_moves = adj_simple[(0,0,0)]
print(f"\n   From 1:Qian, possible first moves: {[ORBIT_NAMES[o] for o in sorted(first_moves)]}")

# From each first move, what are the options?
for fm in sorted(first_moves):
    second_moves = adj_simple[fm] - {(0,0,0)} if False else adj_simple[fm]
    print(f"   From 1:Qian→{ORBIT_NAMES[fm]}, next moves: {[ORBIT_NAMES[o] for o in sorted(second_moves)]}")

# How many paths of length 6 start from Qian and visit 6 distinct orbits?
def count_ham_prefix(adj, start, length):
    """Count paths of given length from start visiting distinct nodes."""
    paths = []
    def dfs(path):
        if len(path) == length + 1:
            paths.append(tuple(path))
            return
        current = path[-1]
        for nb in sorted(adj[current]):
            if nb not in set(path):  # distinct orbits
                path.append(nb)
                dfs(path)
                path.pop()
    dfs([start])
    return paths

ham_6 = count_ham_prefix(adj_simple, (0,0,0), 6)
print(f"\n   Distinct-orbit paths of length 6 from Qian: {len(ham_6)}")

# Check which ones match the KW opening
kw_prefix = tuple(walk[:7])  # 7 nodes = 6 steps
matching = [p for p in ham_6 if p == kw_prefix]
print(f"   Of these, matching KW opening (1→2→3→4→5→6): {len(matching)}")

# What fraction of Eulerian paths start with this prefix?
if euler_paths:
    ep_with_prefix = sum(1 for p in euler_paths if tuple(p[:7]) == kw_prefix)
    print(f"   Eulerian paths with KW opening: {ep_with_prefix}/{len(euler_paths)}")


# ─── 7. Walk divergence points ──────────────────────────────────────────

print(f"\n7. WALK DIVERGENCE FROM FRESH-ORBIT TRAVERSAL")
print(f"   The KW walk visits orbits 1-6 fresh, then revisits 4:Shi at step 6.")
print(f"   Where does the walk 'repeat' vs 'explore'?")

visited_so_far = set()
for i, o in enumerate(walk):
    status = "NEW" if o not in visited_so_far else "REVISIT"
    visited_so_far.add(o)
    n_visited = len(visited_so_far)
    print(f"   Step {i:2d}: {ORBIT_NAMES[o]:<12s} {status:>7s}  ({n_visited}/8 orbits seen)")


# ─── 8. Orbit-level recurrence structure ─────────────────────────────────

print(f"\n8. RECURRENCE STRUCTURE — WALK AS SEQUENCE OF CYCLES")
print(f"   Decomposing the walk into maximal cycle segments")

# Find sub-walks that form closed cycles
walk_edges = [(walk[i], walk[i+1]) for i in range(len(walk)-1)]

# Check for orbit-level patterns: when does the walk return to a previously-visited orbit?
print(f"\n   Sub-walks between returns to same orbit:")
last_seen = {}
segments = []
for i, o in enumerate(walk):
    if o in last_seen:
        seg_start = last_seen[o]
        seg = walk[seg_start:i+1]
        seg_names = [ORBIT_NAMES[s] for s in seg]
        segments.append((seg_start, i, seg))
        print(f"   [{seg_start:2d}-{i:2d}] {'→'.join(seg_names)}")
    last_seen[o] = i


# ─── 9. The walk as Euler path — definitive check ───────────────────────

print(f"\n9. DEFINITIVE EULER PATH CHECK")
print(f"   The multigraph has exactly 31 edges (counting multiplicities).")
print(f"   The KW walk has exactly 31 edges.")
print(f"   If the walk uses each edge the exact right number of times, it IS Eulerian.")

print(f"\n   Edge-by-edge comparison:")
print(f"   {'Edge':<30s} Graph  Walk  Match?")
all_match = True
for e in sorted(edge_count.keys()):
    g_count = edge_count[e]
    w_count = kw_edge_usage.get(e, 0)
    match = "✓" if g_count == w_count else "✗"
    if g_count != w_count:
        all_match = False
    u_name = ORBIT_NAMES[e[0]]
    v_name = ORBIT_NAMES[e[1]]
    print(f"   {u_name} → {v_name:<12s}  {g_count:2d}     {w_count:2d}    {match}")

print(f"\n   ALL edges match: {all_match}")
if all_match:
    print(f"   ★ THE KING WEN BRIDGE WALK IS AN EULERIAN PATH ★")
    print(f"   ★ From {ORBIT_NAMES[walk[0]]} to {ORBIT_NAMES[walk[-1]]} ★")
    print(f"   ★ It traverses every orbit transition exactly as many times as it appears ★")


print(f"\n{'=' * 70}")
print(f"THREAD 5b COMPLETE")
print(f"{'=' * 70}")
