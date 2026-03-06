"""
Exact self-loop position marginals via BEST theorem.

For each possible bridge position k (0..30), count the number of Eulerian paths
where the Qian self-loop is at position k.

Method: Split the Eulerian path at position k. The path decomposes into:
  - A prefix: Eulerian walk using k edges, starting at Qian, ending at Qian
  - Edge k: Qian→Qian (self-loop)
  - A suffix: Eulerian walk using 30-k edges, starting at Qian, ending at Tai

The prefix and suffix use the remaining edges (total 30, since self-loop is removed).
The prefix uses exactly k edges, the suffix uses 30-k edges.

This is complex to compute exactly because the prefix/suffix must partition the 
remaining 30 edges. Instead, use a direct counting approach:

For each position k, we need to count walks of length 31 that:
  1. Start at Qian, end at Tai
  2. Use each edge exactly its multiplicity times
  3. The k-th edge (0-indexed) is Qian→Qian

We can compute this by multiplying:
  - Number of prefix paths (k edges from Qian to Qian, using some subset of edges)
  × Number of suffix paths (30-k edges from Qian to Tai, using remaining edges)

But this requires summing over all valid edge partitions, which is intractable.

Alternative: Direct computation using the BEST theorem for the modified problem.
For the Qian self-loop at position k, we need to count Eulerian paths where:
  - Among the 4 out-edges from Qian, the self-loop is used at a specific rank.

The BEST theorem gives: total paths = t_w × ∏_v (d_out(v)-1)! / ∏_e m_e!

For each node v, the ordering of outgoing edges matters. The ∏(d_out-1)! factor
counts the (d_out-1)! orderings of the LAST d_out-1 edges from v (the first edge 
from v is fixed by the arborescence structure).

For Qian: d_out = 4 (including self-loop). The 3! = 6 orderings of the last 3 edges
determine relative positions of {Qian→Qian, Qian→Shi, Qian→Zhun, Qian→Tai}.
The arborescence fixes ONE of these as the first edge from Qian.

So the self-loop position among Qian's out-edges is determined by:
  1. Which edge the arborescence assigns first (this varies by arborescence)
  2. The permutation of the remaining 3 edges

To get the exact marginal, we need to decompose the BEST theorem more carefully.

Actually, a simpler approach: among the 150M paths, what fraction has the Qian 
self-loop at each LOCAL position (1st, 2nd, 3rd, or 4th usage of Qian as source)?

By the BEST theorem's symmetry structure, the self-loop is equally likely to be
in any of the 4 positions among Qian's outgoing edges — but this isn't exactly 
true because the arborescence structure breaks symmetry.

Let me instead compute exact counts by enumerating over a constrained problem.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import all_bits
from math import factorial

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

nodes = sorted(ORBIT_NAMES.keys())
n = len(nodes)
node_idx = {o: i for i, o in enumerate(nodes)}
TOTAL_EDGES = 31

def exact_det(matrix):
    """Bareiss algorithm for exact integer determinant."""
    n = len(matrix)
    M = [list(row) for row in matrix]
    sign = 1
    prev_pivot = 1
    for i in range(n):
        if M[i][i] == 0:
            found = False
            for j in range(i+1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    sign *= -1
                    found = True
                    break
            if not found:
                return 0
        for j in range(i+1, n):
            for k in range(i+1, n):
                M[j][k] = (M[i][i] * M[j][k] - M[j][i] * M[i][k]) // prev_pivot
            M[j][i] = 0
        prev_pivot = M[i][i]
    return sign * M[n-1][n-1]


def count_euler_paths(ec, start, end):
    """Count Eulerian paths from start to end using BEST theorem."""
    # Add edge end→start
    aug = Counter(ec)
    aug[(end, start)] += 1
    
    # Build Laplacian (excl self-loops)
    L = [[0]*n for _ in range(n)]
    for (u, v), cnt in aug.items():
        i, j = node_idx[u], node_idx[v]
        if i != j:
            L[i][j] -= cnt
            L[i][i] += cnt
    
    # t_w rooted at start
    w = node_idx[start]
    L_red = []
    for i in range(n):
        if i == w: continue
        row = [L[i][j] for j in range(n) if j != w]
        L_red.append(row)
    
    t_w = abs(exact_det(L_red))
    
    # Out-degrees
    aug_out = defaultdict(int)
    for (u, v), cnt in aug.items():
        aug_out[u] += cnt
    
    prod_f = 1
    for o in nodes:
        d = aug_out.get(o, 0)
        if d > 0:
            prod_f *= factorial(d - 1)
    
    prod_m = 1
    for (u, v), cnt in aug.items():
        prod_m *= factorial(cnt)
    
    return t_w * prod_f // prod_m


# ─── Compute: how many paths use the Qian self-loop as the k-th LOCAL edge ───

# Qian has 4 outgoing edges: Qian→Qian(1), Qian→Shi(1), Qian→Zhun(1), Qian→Tai(1)
# In any Euler path starting at Qian, these 4 edges are used in some order.
# Question: in how many paths is the self-loop the j-th edge used from Qian? (j=1,2,3,4)

# The BEST theorem decomposes the count as:
# Total = t_w × ∏_v (d_out(v)-1)! / ∏_e m_e!
# 
# For node Qian in the augmented graph: d_out = 4 (incl self-loop and the added Tai→Qian).
# Wait — in the augmented graph for circuits, Qian has:
#   Original out-edges: Qian→Qian(1), Qian→Shi(1), Qian→Zhun(1), Qian→Tai(1) = 4
#   Added: Tai→Qian (doesn't affect Qian's out-degree)
#   So d_out(Qian) = 4 in augmented = 4 in original
#
# The BEST theorem says: for each node v, choose an ordering of its d_out(v) outgoing
# edges. The arborescence fixes the LAST outgoing edge from each v (except the root).
# The remaining (d_out(v)-1)! orderings of the first d_out(v)-1 edges are free.
#
# So for Qian (root in augmented graph, but in the path version...):
# In the path version, Qian is the start. The arborescence determines which edge 
# from Qian is used LAST among all 4 outgoing edges. The other 3 can be in any order.
#
# Among the 6 permutations of the first 3 edges, 2 have the self-loop first,
# 2 have it second, 2 have it third — NO, that's uniform: 3!/3 = 2 each.
# Wait: 3! = 6 orderings of 3 edges. Self-loop occupies position 1, 2, or 3 with
# equal probability 6/3 = 2 paths per position. But the 4th position is fixed by arb.

# This means: self-loop is at local position j (among Qian's 4 exits) with probability:
#   j=1,2,3: each contributes 2/6 = 1/3 of the total (weighted by arborescences)
#   j=4: when arborescence assigns self-loop as last

# The arborescences at Qian distribute the "last edge" among the 4 outgoing edges.
# For each arborescence, one specific edge is the last. If that edge is the self-loop,
# then self-loop is at local position 4.

# To compute this exactly, we need to decompose arborescences by which edge from 
# Qian is the arborescence edge. This IS computable via Kirchhoff.

# In a rooted arborescence at w, each non-root node v has exactly one outgoing edge
# (the edge in the arborescence). For the root w, NO outgoing edge is in the arb.
# The BEST theorem says: for each non-root v, the arborescence edge from v is used LAST.

# So for Qian (root):
# The arborescence doesn't fix any edge from Qian.
# All 4! orderings of Qian's edges are equally likely? No: only (d_out-1)! = 3! = 6.
# Wait — for the ROOT, ALL d_out edges are free (no edge is fixed by the arb).
# So the root gets d_out! orderings, but BEST gives (d_out-1)!. 

# Actually, re-reading BEST: the formula for circuits is:
# ec = t_w × ∏_v (d_out(v)-1)! / ∏_e m_e!
# The (d_out(v)-1)! applies to ALL nodes INCLUDING the root w.
# For the root: (d_out(w)-1)! = 3! = 6.
# For non-root nodes: (d_out(v)-1)! = 3! = 6 each (since all have d_out=4 in augmented).
#
# The interpretation: for the root w, the first edge used is arbitrary, but the last 
# edge is the one that "closes the circuit" (returns to w). Since we're counting 
# circuits as equivalence classes (starting at any point), the root's first edge 
# doesn't matter? No — we're rooted.
#
# Actually for ROOTED circuits (starting at w): 
# The arborescence determines, for each non-root v, which outgoing edge is used LAST.
# For the root w, the LAST outgoing edge is the one that returns to w in the circuit.
# But in the augmented graph, the "return edge" is Tai→Qian (the added edge).
# This edge is outgoing from TAI, not from Qian.

# I think the cleanest way to compute the self-loop's local position distribution
# is to note that:
# For the root Qian: all 4 outgoing edges have no arborescence constraint.
# Their ordering contributes (d_out-1)! = 6 to the total count.
# But wait, that's not 4! = 24. 
#
# The resolution: the "first edge" from the root in a circuit must be chosen to avoid
# disconnection. The arborescence encodes this: the first edge from w must lead to a 
# subtree of the arborescence that contains all other nodes.
#
# This is getting complex. Let me just compute numerically by comparing path counts
# with specific edges fixed.

print("=" * 70)
print("EXACT LOCAL POSITION OF SELF-LOOPS")
print("=" * 70)

# For Qian self-loop: remove it from the graph. Count Euler paths from Qian to Tai
# using the remaining 30 edges. Then the self-loop can be inserted at any of the 
# 4 visits to Qian (before each non-self-loop outgoing edge from Qian).
# Wait, this doesn't account for the visit created by the self-loop itself.

# Simpler: the self-loop's GLOBAL position (bridge index) depends on all the 
# structure. Let me instead compute the fraction of paths where the self-loop 
# is the j-th out-edge used from Qian.

# Approach: enumerate Qian's 4 out-edges as [self, Shi, Zhun, Tai].
# For each permutation of these 4 edges, compute the number of valid completions.
# The permutation determines the order of Qian's exits; the rest of the graph
# follows from the BEST decomposition.

# For each non-Qian node v, the arborescence fixes the last out-edge.
# For Qian, we're fixing the full order. So:
# Total paths for a given Qian-order = sum over arborescences of 
#   ∏_{v≠Qian} (d_out(v)-1)! / ∏_e m_e! × (valid arborescences for this order)

# This is still complex. Let me try a different, cleaner approach.

# Key insight: the BEST theorem for the AUGMENTED graph gives Euler circuits.
# In the augmented graph, Qian has the added edge Tai→Qian coming IN.
# So Qian's out-degree is 4 and in-degree is 4.
# 
# In an Euler CIRCUIT, the 4 outgoing edges from Qian are used in some order.
# The BEST theorem says: for each arborescence rooted at Qian, the last outgoing 
# edge from each non-Qian node is determined. For Qian (root), there's no constraint
# on which edge is last.
#
# The (d_out(w)-1)! = 6 factor at the root w=Qian means: among the 4 outgoing edges,
# the LAST one is free (it's the one that starts the circuit), and the remaining 3
# can be in any of 3! = 6 orders.
#
# Wait no — for the root in BEST, the circuit starts by leaving w. The first edge 
# from w is the arborescence edge? No...
#
# Actually, in the standard BEST theorem proof:
# For a rooted Euler circuit (starting at w), the arborescence determines, for 
# each node v≠w, the last outgoing edge. This leaves (d_out(v)-1)! free orderings 
# for the remaining edges at each v≠w.
# For the root w: one edge is "first" (start of circuit), but ALL orderings of 
# w's edges are possible. However, the formula gives (d_out(w)-1)!, not d_out(w)!.
# This is because the circuit is ROOTED — starting at w and returning. The "first" 
# edge from w is fixed by the circuit's start, leaving (d_out(w)-1)! for the rest.
#
# No wait — rooted means we count (w → ... → w) as a SINGLE circuit. Without rooting,
# we'd divide by total edges. With rooting at w, each circuit is counted once (starting at w).
# The formula gives: t_w × ∏_ALL v (d-1)! / ∏ m!.
# For the root: the "last" edge from w (in the circuit traversal) is the one that 
# returns to w for the last time. The arborescence doesn't constrain this.
# So all (d-1)! orderings of the first d-1 departures from w are valid, with the 
# last departure being fixed... hmm.

# I think the cleanest resolution is: among all Euler paths from Qian to Tai,
# the self-loop's position among Qian's 4 departures is determined by:
# P(self-loop is k-th departure from Qian | k=1) = P(SL is k-th | k=2) = ... = 1/4

# This would give uniform local distribution. But is this true?

# If true, then:
# The GLOBAL position of the self-loop depends on when the walk visits Qian.
# Qian is visited at positions that depend on the rest of the path.

# Let me test this conjecture via sampling.
# But first, let me try a direct approach for a simpler graph to validate.

# Actually, let me just compute this numerically using a smaller version of the BEST decomposition.
# For each of the 4 Qian out-edges e, compute the number of Euler paths where e is 
# used FIRST from Qian. This means: e is at position 0 (the first bridge).

# Method: fix the first edge, compute BEST on residual.

print("\nCounting paths by first edge from Qian:")
qian_out_edges = [(u, v) for (u, v) in edge_count if u == (0,0,0)]
for u, v in qian_out_edges:
    # Remove one copy of edge u→v. Count Euler paths from v to Tai in residual.
    residual = Counter(edge_count)
    residual[(u, v)] -= 1
    if residual[(u, v)] == 0:
        del residual[(u, v)]
    
    cnt = count_euler_paths(residual, v, (1,1,1))
    mult = edge_count[(u, v)]
    print(f"  First edge {ORBIT_NAMES[u]}→{ORBIT_NAMES[v]}: {cnt} paths (mult={mult}, total={cnt*mult})")

# Wait, count_euler_paths uses BEST on the residual, but the residual may not be 
# Eulerian-path-ready (degree balance may be off). Let me check.

print("\nDegree balance after removing each first edge:")
for u, v in qian_out_edges:
    residual = Counter(edge_count)
    residual[(u, v)] -= 1
    if residual[(u, v)] == 0:
        del residual[(u, v)]
    
    res_out = defaultdict(int)
    res_in = defaultdict(int)
    for (a, b), cnt in residual.items():
        res_out[a] += cnt
        res_in[b] += cnt
    
    imbalance = {}
    for node in set(res_out.keys()) | set(res_in.keys()):
        diff = res_out.get(node, 0) - res_in.get(node, 0)
        if diff != 0:
            imbalance[ORBIT_NAMES[node]] = diff
    
    print(f"  {ORBIT_NAMES[u]}→{ORBIT_NAMES[v]}: imbalance = {imbalance}")
    # For Euler path from v to Tai: need v as source (+1), Tai as sink (-1), rest balanced


# The correct residual analysis:
# Original: Qian out=4, in=3 (source +1), Tai out=3, in=4 (sink -1)
# Remove Qian→v: Qian out=3, in=3 (balanced). v gets in-1.
# If v=Qian (self-loop): Qian out=3, in=2 → source +1. Tai still sink -1. Good.
# If v≠Qian: Qian balanced. v gets out unchanged, in-1 → source +1. Tai still sink -1. Good.
# New path: from v to Tai. ✓

print("\n" + "="*70)
print("EXACT FIRST-DEPARTURE FROM QIAN COUNTS")
print("="*70)

first_depart_counts = {}
total_via_first = 0
for u, v in qian_out_edges:
    residual = Counter(edge_count)
    residual[(u, v)] -= 1
    if residual[(u, v)] == 0:
        del residual[(u, v)]
    
    # Count paths from v to Tai in residual
    # But count_euler_paths internally adds end→start edge.
    # For self-loop case (v=Qian): adds Tai→Qian to residual.
    # Residual after removing self-loop: Qian out=3, in=2.
    # After adding Tai→Qian: Qian out=3, in=3. Tai out=4, in=4. All balanced. 
    # → Euler circuits from Qian in augmented residual.
    
    cnt = count_euler_paths(residual, v, (1,1,1))
    first_depart_counts[(u, v)] = cnt
    total_via_first += cnt
    pct = 100 * cnt / 150955488
    print(f"  1st depart {ORBIT_NAMES[v]:>6s}: {cnt:>12,d} ({pct:5.2f}%)")

print(f"\n  Total: {total_via_first:>12,d}")
print(f"  Expected: 150,955,488")
print(f"  Match: {total_via_first == 150955488}")

# If the self-loop is equally likely to be the 1st, 2nd, 3rd, or 4th departure,
# the fraction at position 1 should be 1/4 = 25%.
sl_first_frac = first_depart_counts.get(((0,0,0), (0,0,0)), 0) / 150955488
print(f"\n  Self-loop as 1st departure: {100*sl_first_frac:.2f}% (uniform would be 25.0%)")

# Also compute for LAST departure from Qian
# The last departure from Qian is the last time the walk leaves Qian.
# In the BEST theorem, the arborescence determines which edge from each non-root 
# node is last. For the root (Qian), the last edge is... well, in the circuit 
# (augmented), it's fixed by the arborescence too? Actually no — for the root, 
# ALL edges can be in any order given the arborescence constraint on other nodes.

# Let me compute: for each possible LAST edge from Qian, how many paths exist?
# The last departure from Qian is the last time the walk is at Qian.
# After the 4th departure from Qian, the walk never returns to Qian.

# This is harder to compute directly. Let me instead verify the first-departure
# computation matches the expected total, and infer symmetry.

if total_via_first == 150955488:
    print("\n  ★ First-departure decomposition verified exact.")
    # Self-loop is NOT equally likely as 1st departure — the Qian→Qian edge
    # leaves the walk at Qian, so it "wastes" a departure without making progress.
    # The graph structure breaks symmetry.
    
    for (u, v), cnt in first_depart_counts.items():
        pct = 100 * cnt / 150955488
        print(f"    {ORBIT_NAMES[v]:>6s} first: {pct:5.2f}%")

# For the Qian self-loop global position distribution:
# If the self-loop is the 1st departure: it's at global position 0.
# If the self-loop is the j-th departure: its global position depends on 
# how many other edges are traversed between Qian visits.

# Since exact computation of all 31 positions requires conditioning on the 
# full walk structure, let me stick with sampling for the global distribution.
# The local position (1st/2nd/3rd/4th departure) is what we can compute exactly.

# Let's also compute for WWang:
print(f"\n{'='*70}")
print("EXACT FIRST-DEPARTURE FROM WWANG COUNTS")
print("="*70)

wwang_out_edges = [(u, v) for (u, v) in edge_count if u == (0,1,1)]
for u, v in wwang_out_edges:
    print(f"  {ORBIT_NAMES[u]}→{ORBIT_NAMES[v]}: mult={edge_count[(u,v)]}")

# For WWang: which edge is used first? 
# But WWang is not the start of the walk. The walk arrives at WWang via incoming edges.
# The "first departure from WWang" is the first time the walk leaves WWang, which
# happens after the first arrival at WWang.
# 
# This is much harder to compute with BEST — it requires knowing the walk's trajectory.
# Stick with sampling.

print("\n  (WWang is not the start node — first-departure analysis requires ")
print("   knowing arrival times. Using sampling instead.)")

print(f"\n{'='*70}")
print("EXACT ANALYSIS COMPLETE")
print("="*70)
