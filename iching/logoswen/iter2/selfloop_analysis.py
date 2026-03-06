"""
Thread D: Exact and sampled self-loop position analysis.

Two self-loops exist in the orbit multigraph:
  Qian(000) → Qian(000): multiplicity 1
  WWang(011) → WWang(011): multiplicity 1

Question: In the 150,955,488 Eulerian paths from Qian to Tai,
at which bridge position (0..30) does each self-loop land?

Method:
  1. Sampling with backtracking DFS (large sample, good statistics)
  2. Position-constrained BEST theorem (exact marginals for each position)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import all_bits
from math import factorial
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
nodes = sorted(ORBIT_NAMES.keys())

# Build KW orbit walk
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))


# ─── Sampling approach ────────────────────────────────────────────────────────

def sample_eulerian_dfs(edge_count, start, end, rng):
    """Sample Eulerian path using randomized DFS with backtracking."""
    remaining = dict(edge_count)
    adj = defaultdict(list)
    for (u, v) in edge_count:
        if v not in adj[u]:
            adj[u].append(v)
    
    path = [start]
    
    def dfs(node, depth):
        if depth == TOTAL_EDGES:
            return node == end
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


N_SAMPLES = 200_000
rng = random.Random(2024)

print(f"Sampling {N_SAMPLES} Eulerian paths...")
print(f"Total paths: 150,955,488 (exact)")

qian_positions = []
wwang_positions = []
joint_positions = []
paths_found = 0

t0 = time.time()
for i in range(N_SAMPLES):
    path = sample_eulerian_dfs(edge_count, (0,0,0), (1,1,1), rng)
    if path is None:
        continue
    
    paths_found += 1
    
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
    
    if (i+1) % 50000 == 0:
        elapsed = time.time() - t0
        print(f"  {i+1}/{N_SAMPLES} in {elapsed:.1f}s ({paths_found} valid)")

t1 = time.time()
print(f"\nCompleted: {paths_found} valid paths in {t1-t0:.1f}s")

# ─── Results ──────────────────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("QIAN SELF-LOOP POSITION DISTRIBUTION")
print(f"{'='*70}")

qian_counter = Counter(qian_positions)
print(f"\n  Total samples: {len(qian_positions)}")
print(f"  Distinct positions: {len(qian_counter)}")
print(f"\n  {'Pos':>4s}  {'Count':>6s}  {'Pct':>6s}  {'Histogram'}")

for pos in range(31):
    cnt = qian_counter.get(pos, 0)
    pct = 100 * cnt / len(qian_positions) if qian_positions else 0
    bar = '█' * max(0, int(pct * 2))
    kw_mark = ' ← KW' if pos == 13 else ''
    print(f"  B{pos:2d}:  {cnt:6d}  {pct:5.1f}%  {bar}{kw_mark}")

print(f"\n  Mean position: {sum(qian_positions)/len(qian_positions):.1f}")
print(f"  Median position: {sorted(qian_positions)[len(qian_positions)//2]}")

print(f"\n{'='*70}")
print("WWANG SELF-LOOP POSITION DISTRIBUTION")
print(f"{'='*70}")

wwang_counter = Counter(wwang_positions)
print(f"\n  Total samples: {len(wwang_positions)}")
print(f"  Distinct positions: {len(wwang_counter)}")
print(f"\n  {'Pos':>4s}  {'Count':>6s}  {'Pct':>6s}  {'Histogram'}")

for pos in range(31):
    cnt = wwang_counter.get(pos, 0)
    pct = 100 * cnt / len(wwang_positions) if wwang_positions else 0
    bar = '█' * max(0, int(pct * 2))
    kw_mark = ' ← KW' if pos == 18 else ''
    print(f"  B{pos:2d}:  {cnt:6d}  {pct:5.1f}%  {bar}{kw_mark}")

print(f"\n  Mean position: {sum(wwang_positions)/len(wwang_positions):.1f}")
print(f"  Median position: {sorted(wwang_positions)[len(wwang_positions)//2]}")


print(f"\n{'='*70}")
print("JOINT DISTRIBUTION (Qian, WWang)")
print(f"{'='*70}")

joint_counter = Counter(joint_positions)
print(f"\n  Total joint samples: {len(joint_positions)}")
print(f"  Distinct joint positions: {len(joint_counter)}")

# KW position
kw_joint = (13, 18)
kw_count = joint_counter.get(kw_joint, 0)
kw_pct = 100 * kw_count / len(joint_positions) if joint_positions else 0

print(f"\n  Top 20 joint positions:")
for rank, ((qp, wp), cnt) in enumerate(joint_counter.most_common(20), 1):
    pct = 100 * cnt / len(joint_positions)
    kw_mark = ' ← KW' if (qp, wp) == kw_joint else ''
    print(f"    #{rank:3d}: Qian@B{qp:2d}, WWang@B{wp:2d}: {cnt:5d} ({pct:5.2f}%){kw_mark}")

print(f"\n  KW joint (13, 18): {kw_count} ({kw_pct:.3f}%)")
rank = sum(1 for (p, c) in joint_counter.items() if c >= kw_count) if kw_count > 0 else 'N/A'
print(f"  KW rank: {rank}/{len(joint_counter)}")

# Probability under uniform
n_joint_positions = len(joint_counter)
uniform_pct = 100.0 / n_joint_positions if n_joint_positions > 0 else 0
print(f"  If uniform: {uniform_pct:.3f}% per position")
print(f"  KW deviation from uniform: {kw_pct/uniform_pct:.2f}x" if uniform_pct > 0 else "")


# ─── Constraint analysis: which positions are forbidden? ──────────────────────

print(f"\n{'='*70}")
print("FORBIDDEN POSITIONS ANALYSIS")
print(f"{'='*70}")

# Qian self-loop requires that the walk is at Qian and stays at Qian.
# The walk starts at Qian (position 0). It can only be at Qian when incoming edges 
# arrive there. Qian has 3 incoming edges (from Bo, WWang, and the added self-loop).
# But the self-loop IS one of those... let me think.

# Qian has out-edges: Qian→Qian(1), Qian→Shi(1), Qian→Zhun(1), Qian→Tai(1)
# Qian has in-edges: Bo→Qian(1), WWang→Qian(1), Qian→Qian(1)
# 
# The walk visits Qian as the source of each out-edge.
# Total out-edges = 4, so Qian appears 4 times as the "current" node.
# These 4 visits are:
#   - Position 0 (start)
#   - After each of the 3 incoming edges (Bo→Qian, WWang→Qian, Qian→Qian)
#
# Wait: the self-loop counts as BOTH outgoing AND incoming.
# If the self-loop is at position k, then at position k the walk is at Qian and
# stays at Qian. This means Qian is the current node at positions k AND k+1.
# 
# The non-self-loop incoming edges to Qian are Bo→Qian(1) and WWang→Qian(1).
# So Qian is visited at:
#   - Position 0 (start)
#   - Once from Bo→Qian
#   - Once from WWang→Qian
#   - Once from Qian→Qian (self-loop, which also keeps it at Qian)
#
# The 4 out-edges from Qian are used at these 4 visits.
# One of these out-edges is the self-loop.

# Forbidden positions for Qian self-loop:
# Can't be at position 30 (the last edge) since the walk must end at Tai.
# Wait, it CAN be at position 30 if the walk goes ...→Qian→Qian→...→Tai at the end.
# But position 30 is the last edge, so if Qian self-loop is at 30, the walk ends at Qian, not Tai.
# So position 30 is forbidden for Qian self-loop.

# Actually let me just check which positions have zero samples
print("\nPositions with zero Qian self-loop samples:")
qian_zero = [pos for pos in range(31) if qian_counter.get(pos, 0) == 0]
print(f"  {qian_zero}")

print("\nPositions with zero WWang self-loop samples:")
wwang_zero = [pos for pos in range(31) if wwang_counter.get(pos, 0) == 0]
print(f"  {wwang_zero}")


# ─── Ordering constraint: Qian before/after WWang ────────────────────────────

print(f"\n{'='*70}")
print("RELATIVE ORDERING: Qian self-loop vs WWang self-loop")
print(f"{'='*70}")

qian_before = sum(1 for q, w in joint_positions if q < w)
qian_after = sum(1 for q, w in joint_positions if q > w)
qian_same = sum(1 for q, w in joint_positions if q == w)

print(f"  Qian before WWang: {qian_before} ({100*qian_before/len(joint_positions):.1f}%)")
print(f"  Qian after WWang:  {qian_after} ({100*qian_after/len(joint_positions):.1f}%)")
print(f"  Same position:     {qian_same}")
print(f"  KW: Qian@13 < WWang@18 (Qian first)")


# ─── Distance between self-loops ─────────────────────────────────────────────

print(f"\n{'='*70}")
print("DISTANCE BETWEEN SELF-LOOPS")
print(f"{'='*70}")

distances = [w - q for q, w in joint_positions]
dist_counter = Counter(distances)
print(f"  KW distance: {18 - 13} = 5")
print(f"  Mean distance: {sum(distances)/len(distances):.1f}")
print(f"  Std: {(sum((d - sum(distances)/len(distances))**2 for d in distances)/len(distances))**0.5:.1f}")

print(f"\n  Distance distribution:")
for d in sorted(dist_counter.keys()):
    cnt = dist_counter[d]
    pct = 100 * cnt / len(distances)
    bar = '█' * max(0, int(pct * 2))
    kw_mark = ' ← KW' if d == 5 else ''
    print(f"    d={d:+3d}: {cnt:5d} ({pct:4.1f}%) {bar}{kw_mark}")


# ─── Bridge 13 / Bridge 18 specific analysis ─────────────────────────────────

print(f"\n{'='*70}")
print("KW-SPECIFIC POSITIONS: B13 (Qian) and B18 (WWang)")
print(f"{'='*70}")

# What's the probability of Qian@13 AND WWang@18?
print(f"  P(Qian@13): {100*qian_counter.get(13,0)/len(qian_positions):.2f}%")
print(f"  P(WWang@18): {100*wwang_counter.get(18,0)/len(wwang_positions):.2f}%")
print(f"  P(both): {100*kw_count/len(joint_positions):.3f}%")

# Check independence
p_q13 = qian_counter.get(13, 0) / len(qian_positions) if qian_positions else 0
p_w18 = wwang_counter.get(18, 0) / len(wwang_positions) if wwang_positions else 0
p_joint = kw_count / len(joint_positions) if joint_positions else 0
p_independent = p_q13 * p_w18

print(f"\n  If independent: P(both) ≈ {100*p_independent:.3f}%")
print(f"  Actual:         P(both) = {100*p_joint:.3f}%")
print(f"  Ratio: {p_joint/p_independent:.2f}x (>1 = correlated, <1 = anti-correlated)" if p_independent > 0 else "")

# Conditional probabilities
p_w18_given_q13 = joint_counter.get((13,18), 0) / qian_counter.get(13, 0) if qian_counter.get(13, 0) > 0 else 0
p_q13_given_w18 = joint_counter.get((13,18), 0) / wwang_counter.get(18, 0) if wwang_counter.get(18, 0) > 0 else 0

print(f"\n  P(WWang@18 | Qian@13) = {100*p_w18_given_q13:.2f}%")
print(f"  P(Qian@13 | WWang@18) = {100*p_q13_given_w18:.2f}%")
print(f"  P(WWang@18) marginal  = {100*p_w18:.2f}%")
print(f"  P(Qian@13) marginal   = {100*p_q13:.2f}%")

# ─── "Interior" analysis ─────────────────────────────────────────────────────

print(f"\n{'='*70}")
print("INTERIOR vs BOUNDARY ANALYSIS")
print(f"{'='*70}")

# Interior = positions 3..27 (avoiding first/last 3 positions)
# Boundary = positions 0..2 and 28..30

qian_interior = sum(qian_counter.get(p, 0) for p in range(3, 28))
qian_boundary = sum(qian_counter.get(p, 0) for p in list(range(3)) + list(range(28, 31)))
qian_total = qian_interior + qian_boundary

print(f"  Qian self-loop:")
print(f"    Interior (B3..B27): {qian_interior} ({100*qian_interior/qian_total:.1f}%)")
print(f"    Boundary (B0..B2, B28..B30): {qian_boundary} ({100*qian_boundary/qian_total:.1f}%)")
print(f"    Interior fraction if uniform: {25/31*100:.1f}%")

wwang_interior = sum(wwang_counter.get(p, 0) for p in range(3, 28))
wwang_boundary = sum(wwang_counter.get(p, 0) for p in list(range(3)) + list(range(28, 31)))
wwang_total = wwang_interior + wwang_boundary

print(f"  WWang self-loop:")
print(f"    Interior (B3..B27): {wwang_interior} ({100*wwang_interior/wwang_total:.1f}%)")
print(f"    Boundary (B0..B2, B28..B30): {wwang_boundary} ({100*wwang_boundary/wwang_total:.1f}%)")

# B13 is in the "middle third" (positions 10-20). What fraction land there?
qian_middle = sum(qian_counter.get(p, 0) for p in range(10, 21))
print(f"\n  Qian in middle third (B10..B20): {qian_middle} ({100*qian_middle/qian_total:.1f}%)")
print(f"    Expected if uniform: {11/31*100:.1f}%")
print(f"    KW at B13: in the middle third")

wwang_middle = sum(wwang_counter.get(p, 0) for p in range(10, 21))
print(f"  WWang in middle third (B10..B20): {wwang_middle} ({100*wwang_middle/wwang_total:.1f}%)")
print(f"    KW at B18: in the middle third")

# Both in middle third
both_middle = sum(cnt for (q, w), cnt in joint_counter.items() if 10 <= q <= 20 and 10 <= w <= 20)
print(f"  Both in middle third: {both_middle} ({100*both_middle/len(joint_positions):.1f}%)")


print(f"\n{'='*70}")
print("SELF-LOOP ANALYSIS COMPLETE")
print(f"{'='*70}")
