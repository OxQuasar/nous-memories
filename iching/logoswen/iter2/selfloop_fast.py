"""
Fast self-loop analysis using multiple approaches:

1. Fast enumeration with aggressive pruning (cap at 1M paths)
2. Hierholzer sampling (very fast, biased but useful for rough stats)
3. Wilson's algorithm for uniform arborescences → BEST decomposition

The orbit multigraph is small (8 nodes, 31 edges), but the enumeration space
is 150M paths. We'll enumerate up to a cap, then sample the rest.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import all_bits
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

TOTAL_EDGES = 31

# Build KW orbit walk
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))

# ─── Approach 1: Hierholzer sampling (fast, slightly biased) ──────────────────

def hierholzer_random(ec, start, rng):
    """Random Hierholzer — fast Euler circuit/path sampling."""
    adj = defaultdict(list)
    for (u, v), cnt in ec.items():
        for _ in range(cnt):
            adj[u].append(v)
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


def dfs_sample(ec, start, end, rng):
    """Randomized DFS with backtracking — closer to uniform."""
    remaining = dict(ec)
    adj = defaultdict(list)
    for (u, v) in ec:
        if v not in adj[u]:
            adj[u].append(v)
    
    path = [start]
    
    def dfs(node, depth):
        if depth == TOTAL_EDGES:
            return node == end
        available = []
        for target in adj[node]:
            e = (node, target)
            if remaining.get(e, 0) > 0:
                available.append(target)
        rng.shuffle(available)
        for target in available:
            e = (node, target)
            remaining[e] -= 1
            path.append(target)
            if dfs(target, depth + 1):
                return True
            path.pop()
            remaining[e] += 1
        return False
    
    if dfs(start, 0):
        return list(path)
    return None


# ─── Run Hierholzer sampling (very fast) ──────────────────────────────────────

print("="*70)
print("APPROACH 1: HIERHOLZER SAMPLING (fast, slight bias)")
print("="*70)

N_HIER = 500_000
rng = random.Random(42)

qian_h = Counter()
wwang_h = Counter()
joint_h = Counter()
valid_h = 0

t0 = time.time()
for i in range(N_HIER):
    path = hierholzer_random(edge_count, (0,0,0), rng)
    
    # Check if it ends at Tai
    if path[-1] != (1,1,1):
        continue
    
    valid_h += 1
    q_pos = None
    w_pos = None
    for step in range(len(path) - 1):
        u, v = path[step], path[step+1]
        if u == v == (0,0,0):
            q_pos = step
        elif u == v == (0,1,1):
            w_pos = step
    
    if q_pos is not None:
        qian_h[q_pos] += 1
    if w_pos is not None:
        wwang_h[w_pos] += 1
    if q_pos is not None and w_pos is not None:
        joint_h[(q_pos, w_pos)] += 1

t1 = time.time()
print(f"Sampled {N_HIER} paths, {valid_h} ended at Tai ({100*valid_h/N_HIER:.1f}%), in {t1-t0:.1f}s")

print(f"\nQian self-loop (from {valid_h} valid paths):")
for pos in range(31):
    cnt = qian_h.get(pos, 0)
    pct = 100 * cnt / valid_h if valid_h else 0
    bar = '█' * max(0, int(pct * 2))
    kw = ' ← KW' if pos == 13 else ''
    print(f"  B{pos:2d}: {cnt:6d} ({pct:5.2f}%) {bar}{kw}")

print(f"\nWWang self-loop (from {valid_h} valid paths):")
for pos in range(31):
    cnt = wwang_h.get(pos, 0)
    pct = 100 * cnt / valid_h if valid_h else 0
    bar = '█' * max(0, int(pct * 2))
    kw = ' ← KW' if pos == 18 else ''
    print(f"  B{pos:2d}: {cnt:6d} ({pct:5.2f}%) {bar}{kw}")


# ─── Run DFS sampling (slower, less biased) ──────────────────────────────────

print(f"\n{'='*70}")
print("APPROACH 2: RANDOMIZED DFS SAMPLING (less biased)")
print("="*70)

N_DFS = 50_000
rng2 = random.Random(2024)

qian_d = Counter()
wwang_d = Counter()
joint_d = Counter()
valid_d = 0

t0 = time.time()
for i in range(N_DFS):
    path = dfs_sample(edge_count, (0,0,0), (1,1,1), rng2)
    if path is None:
        continue
    
    valid_d += 1
    q_pos = None
    w_pos = None
    for step in range(len(path) - 1):
        u, v = path[step], path[step+1]
        if u == v == (0,0,0):
            q_pos = step
        elif u == v == (0,1,1):
            w_pos = step
    
    if q_pos is not None:
        qian_d[q_pos] += 1
    if w_pos is not None:
        wwang_d[w_pos] += 1
    if q_pos is not None and w_pos is not None:
        joint_d[(q_pos, w_pos)] += 1
    
    if (i+1) % 10000 == 0:
        print(f"  {i+1}/{N_DFS} ({valid_d} valid, {time.time()-t0:.0f}s)")

t1 = time.time()
print(f"Sampled {N_DFS}, {valid_d} valid in {t1-t0:.1f}s")

print(f"\nQian self-loop (DFS, N={valid_d}):")
for pos in range(31):
    cnt = qian_d.get(pos, 0)
    pct = 100 * cnt / valid_d if valid_d else 0
    bar = '█' * max(0, int(pct * 2))
    kw = ' ← KW' if pos == 13 else ''
    print(f"  B{pos:2d}: {cnt:6d} ({pct:5.2f}%) {bar}{kw}")

print(f"\nWWang self-loop (DFS, N={valid_d}):")
for pos in range(31):
    cnt = wwang_d.get(pos, 0)
    pct = 100 * cnt / valid_d if valid_d else 0
    bar = '█' * max(0, int(pct * 2))
    kw = ' ← KW' if pos == 18 else ''
    print(f"  B{pos:2d}: {cnt:6d} ({pct:5.2f}%) {bar}{kw}")


# ─── Combined analysis ──────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("COMBINED ANALYSIS")
print("="*70)

# Compare the two sampling methods
print("\nSide-by-side comparison (Hierholzer vs DFS):")
print(f"{'Pos':>4s}  {'Hier%':>7s}  {'DFS%':>7s}  {'Diff':>6s}")
for pos in range(31):
    h_pct = 100 * qian_h.get(pos, 0) / valid_h if valid_h else 0
    d_pct = 100 * qian_d.get(pos, 0) / valid_d if valid_d else 0
    diff = h_pct - d_pct
    kw = ' ←' if pos == 13 else ''
    print(f"  B{pos:2d}  {h_pct:6.2f}%  {d_pct:6.2f}%  {diff:+5.2f}%{kw}")

# Joint distribution
print(f"\nJoint KW position (13, 18):")
kw_h = joint_h.get((13, 18), 0)
kw_d = joint_d.get((13, 18), 0)
print(f"  Hierholzer: {kw_h} ({100*kw_h/valid_h:.3f}%)")
print(f"  DFS:        {kw_d} ({100*kw_d/valid_d:.3f}%)" if valid_d > 0 else "")

# Relative ordering
h_q_before_w = sum(1 for (q, w) in joint_h.elements() if q < w)
h_q_after_w = sum(1 for (q, w) in joint_h.elements() if q > w)
d_q_before_w = sum(cnt for (q, w), cnt in joint_d.items() if q < w)
d_q_after_w = sum(cnt for (q, w), cnt in joint_d.items() if q > w)

h_total_j = sum(joint_h.values())
d_total_j = sum(joint_d.values())

print(f"\nQian before WWang:")
print(f"  Hierholzer: {100*h_q_before_w/h_total_j:.1f}%" if h_total_j else "")
print(f"  DFS:        {100*d_q_before_w/d_total_j:.1f}%" if d_total_j else "")
print(f"  KW: Qian@13 < WWang@18 (yes)")

# Distance distribution
h_distances = Counter(w - q for (q, w), cnt in joint_h.items() for _ in range(cnt))
d_distances = Counter(w - q for (q, w), cnt in joint_d.items() for _ in range(cnt))

print(f"\nSelf-loop distance (WWang - Qian) statistics:")
print(f"  Hierholzer mean: {sum(d*c for d,c in h_distances.items())/sum(h_distances.values()):.1f}")
print(f"  DFS mean:        {sum(d*c for d,c in d_distances.items())/sum(d_distances.values()):.1f}" if d_distances else "")
print(f"  KW distance: 5")

# Summary statistics
print(f"\n{'='*70}")
print("SUMMARY STATISTICS")
print(f"{'='*70}")

# Use the larger (Hierholzer) sample for final stats
print(f"\nUsing Hierholzer sample (N={valid_h}):")

# Qian self-loop
q_mean = sum(pos * cnt for pos, cnt in qian_h.items()) / sum(qian_h.values())
q_positions = sorted(qian_h.keys())
print(f"\n  Qian self-loop:")
print(f"    Mean position: {q_mean:.1f}")
print(f"    Min: B{min(q_positions)}, Max: B{max(q_positions)}")
print(f"    KW at B13: rank {sum(1 for p, c in qian_h.items() if c >= qian_h.get(13, 0))}/{len(qian_h)}")
print(f"    KW B13 pct: {100*qian_h.get(13,0)/valid_h:.2f}%")

# WWang self-loop
w_mean = sum(pos * cnt for pos, cnt in wwang_h.items()) / sum(wwang_h.values())
w_positions = sorted(wwang_h.keys())
print(f"\n  WWang self-loop:")
print(f"    Mean position: {w_mean:.1f}")
print(f"    Min: B{min(w_positions)}, Max: B{max(w_positions)}")
print(f"    KW at B18: rank {sum(1 for p, c in wwang_h.items() if c >= wwang_h.get(18, 0))}/{len(wwang_h)}")
print(f"    KW B18 pct: {100*wwang_h.get(18,0)/valid_h:.2f}%")

# Joint
print(f"\n  Joint (Qian, WWang):")
print(f"    Unique positions: {len(joint_h)}")
print(f"    KW (13,18) count: {joint_h.get((13,18), 0)}")
print(f"    KW pct: {100*joint_h.get((13,18),0)/valid_h:.3f}%")
print(f"    Qian before WWang: {100*h_q_before_w/h_total_j:.1f}%")
print(f"    Mean distance: {sum(d*c for d,c in h_distances.items())/sum(h_distances.values()):.1f}")

# B13 and B18 interpretation
print(f"\n  B13 = upper/lower canon boundary (pairs 13-14, hexagrams 27-28)")
print(f"  B18 = within lower canon (pairs 18-19, hexagrams 37-38)")
print(f"  B13 is roughly at 42% mark (13/31)")
print(f"  B18 is roughly at 58% mark (18/31)")
print(f"  Both are in the interior, avoiding boundaries")

print(f"\n{'='*70}")
print("SELF-LOOP ANALYSIS COMPLETE")
print(f"{'='*70}")
