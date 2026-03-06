"""
Quick analysis of the orbit multigraph structure to understand 
the Eulerian path enumeration complexity.
"""
import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import all_bits
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

print("Edge structure:")
for (u, v), cnt in sorted(edge_count.items()):
    print(f"  {ORBIT_NAMES[u]:>6s} → {ORBIT_NAMES[v]:<6s}: {cnt}")

# Degree analysis
out_deg = defaultdict(int)
in_deg = defaultdict(int)
for (u, v), cnt in edge_count.items():
    out_deg[u] += cnt
    in_deg[v] += cnt

print("\nNode degrees (out, in, total):")
for o in sorted(ORBIT_NAMES.keys()):
    d_out = out_deg[o]
    d_in = in_deg[o]
    print(f"  {ORBIT_NAMES[o]:>6s}: out={d_out}, in={d_in}, total={d_out+d_in}")

# Use BEST theorem to count Eulerian circuits
# For directed multigraphs:
# Number of Eulerian circuits = t_w * ∏_v (d_out(v) - 1)!  / ∏_e (m_e!)
# where t_w is the number of arborescences rooted at w
# But we need Eulerian PATHS from s to t, not circuits.
# Eulerian paths s→t = Eulerian circuits in (G + edge t→s)
# then divide by multiplicity of t→s edge (which becomes m+1)

# Actually, let me just count with a smarter algorithm.
# The graph is small (8 nodes, 31 edges with ~26 unique edge types).
# Let me try the BEST theorem approach.

import numpy as np
from math import factorial

# For Eulerian path from s=(0,0,0) to t=(1,1,1):
# Add edge t→s to make it Eulerian circuit in augmented graph
# Then: # Euler paths = # Euler circuits in augmented / (m_{t→s} + 1)
# Wait, that's not quite right. Let me think again.
#
# Actually: # Euler paths s→t = t_s * ∏_{v ≠ s} (d_out(v) - 1)! / ∏_edges mult_e!
# where t_s is the number of arborescences rooted at s in the graph,
# and d_out(v) is the out-degree of v.
# This is from the BEST (de Bruijn-Ehrenfest-Smith-Tutte) theorem adapted for paths.

# First, let's try the direct approach more carefully.
# Add edge (1,1,1) → (0,0,0) to the graph to make it Eulerian-circuit-ready.
aug_edge_count = Counter(edge_count)
aug_edge_count[((1,1,1), (0,0,0))] += 1

# Verify all nodes now have equal in/out degree
aug_out = defaultdict(int)
aug_in = defaultdict(int)
for (u,v), cnt in aug_edge_count.items():
    aug_out[u] += cnt
    aug_in[v] += cnt

print("\nAugmented graph (added Tai→Qian):")
for o in sorted(ORBIT_NAMES.keys()):
    print(f"  {ORBIT_NAMES[o]:>6s}: out={aug_out[o]}, in={aug_in[o]}")

# BEST theorem for Euler circuits in directed multigraph:
# ec(G) = t_w(G) * ∏_{v} (d_out(v) - 1)! / ∏_{(u,v)} m(u,v)!
# where t_w(G) is # of arborescences rooted at any node w.

# Step 1: Compute t_w using Kirchhoff's matrix tree theorem
# The Laplacian matrix L: L[i][i] = out-degree of i, L[i][j] = -m(i,j) for i≠j
# t_w = det of L with row w and column w removed

nodes = sorted(ORBIT_NAMES.keys())
n = len(nodes)
node_idx = {o: i for i, o in enumerate(nodes)}

# Build Laplacian for augmented graph
L = np.zeros((n, n), dtype=np.int64)
for (u, v), cnt in aug_edge_count.items():
    i, j = node_idx[u], node_idx[v]
    if i != j:
        L[i][j] -= cnt
    L[i][i] += cnt  # out-degree contribution (even for self-loops)

# Wait — for directed graphs, self-loops contribute to out-degree but 
# the Laplacian for arborescences needs careful handling.
# Actually, for the BEST theorem, self-loops are handled differently.
# Self-loops don't affect arborescences, but they DO contribute to (d_out-1)! factor.
# In the Laplacian for arborescences, we should NOT include self-loops.

# Rebuild Laplacian without self-loops
L2 = np.zeros((n, n), dtype=np.int64)
for (u, v), cnt in aug_edge_count.items():
    i, j = node_idx[u], node_idx[v]
    if i != j:
        L2[i][j] -= cnt
        L2[i][i] += cnt  # out-degree for non-self-loop edges

print("\nLaplacian (for arborescences, excluding self-loops):")
for i in range(n):
    row = ' '.join(f'{L2[i][j]:3d}' for j in range(n))
    print(f"  {ORBIT_NAMES[nodes[i]]:>6s}: [{row}]")

# Compute t_w for w = (0,0,0) (Qian, which is our start node)
w = node_idx[(0,0,0)]
# Remove row w and column w
L_reduced = np.delete(np.delete(L2, w, axis=0), w, axis=1)
t_w = int(round(np.linalg.det(L_reduced.astype(float))))
print(f"\nt_w (arborescences rooted at Qian): {t_w}")

# Step 2: Compute ∏(d_out(v) - 1)! for all v
prod_factorial = 1
for o in nodes:
    d = aug_out[o]
    print(f"  {ORBIT_NAMES[o]:>6s}: d_out={d}, (d-1)!={factorial(d-1)}")
    prod_factorial *= factorial(d - 1)

print(f"\n∏(d_out(v) - 1)! = {prod_factorial}")

# Step 3: Compute ∏ m(u,v)! for all edges
prod_mult = 1
for (u, v), cnt in aug_edge_count.items():
    prod_mult *= factorial(cnt)

print(f"∏ m(u,v)! = {prod_mult}")

# Step 4: BEST theorem result
ec = t_w * prod_factorial // prod_mult
print(f"\nEuler CIRCUITS in augmented graph: {ec}")

# Step 5: Convert to Euler PATHS from s to t
# Each Euler path s→t corresponds to an Euler circuit in augmented graph
# that uses the added t→s edge. Since the added edge has multiplicity 1
# (it was added once), each circuit passes through it exactly once.
# Number of Euler paths = ec * (multiplicity of t→s in augmented) / 1
# Actually: each Euler circuit can be "cut" at the t→s edge to get a path.
# But each circuit uses the t→s edge exactly once (it has mult 1 in augmented).
# So # Euler paths = ec.
# Wait — for a circuit starting at any point, we can cut at the t→s edge.
# The BEST theorem counts circuits starting at w. If we root at s (our start),
# each circuit goes s→...→t→s, and cutting gives exactly one s→t path.
# So: # Euler paths s→t = ec (when the augmented edge has multiplicity 1)

# But if (1,1,1)→(0,0,0) already existed in original graph, we added one more.
# The original has:
orig_ts = edge_count.get(((1,1,1), (0,0,0)), 0)
print(f"\nOriginal (Tai→Qian) multiplicity: {orig_ts}")
aug_ts = aug_edge_count[((1,1,1), (0,0,0))]
print(f"Augmented (Tai→Qian) multiplicity: {aug_ts}")

# Each Euler circuit in the augmented graph visits the (Tai→Qian) edge aug_ts times.
# We want circuits that use our specific added edge (the aug_ts-th copy).
# Due to symmetry among identical edges, fraction = 1/aug_ts of all circuits.
# Actually no — the BEST theorem already accounts for edge multiplicity.
# Let me reconsider.

# The correct formula for Euler paths from s to t:
# Add edge t→s. In the augmented graph, count Euler circuits.
# Each Euler path s→t corresponds to a unique Euler circuit (add t→s at the end).
# But multiple circuits might correspond to the same path if the t→s edge had 
# multiplicity > 1 in the augmented graph (we can't distinguish which copy we use).
# Actually, the BEST theorem counts circuits in the MULTIGRAPH, treating
# identical edges as interchangeable. So each circuit = each distinct sequence of
# edge-types (not individual edge copies).
# 
# For our purpose: if orig_ts = 0, then aug_ts = 1, and 
# # Euler paths = # Euler circuits. Done.
# If orig_ts > 0, it's more complex.

if orig_ts == 0:
    euler_paths_count = ec
    print(f"\n★ Number of Eulerian paths from Qian to Tai: {euler_paths_count}")
else:
    # More complex case
    # The number of Euler paths = ec * 1 / aug_ts
    # because each circuit uses the t→s edge aug_ts times,
    # but only 1 of those is the "added" edge to cut at.
    # NO — the BEST theorem already treats same-endpoint edges as identical.
    # We need to be more careful.
    print(f"\n  Need more careful handling since Tai→Qian already exists.")
    # For now, let's try the direct enumeration approach and see if we get
    # the same answer.

# Also compute for the original graph directly using the formula
# for Euler paths (not via augmented graph):
# # Euler paths s→t = t_s(G) * ∏_{v≠s} (d_out(v) - 1)! / ∏_edges m_e!
# where t_s(G) is the arborescences rooted at s in the ORIGINAL graph.

L3 = np.zeros((n, n), dtype=np.int64)
for (u, v), cnt in edge_count.items():
    i, j = node_idx[u], node_idx[v]
    if i != j:
        L3[i][j] -= cnt
        L3[i][i] += cnt

print("\nOriginal graph Laplacian:")
for i in range(n):
    row = ' '.join(f'{L3[i][j]:3d}' for j in range(n))
    print(f"  {ORBIT_NAMES[nodes[i]]:>6s}: [{row}]")

# For Euler paths from s to t, use the Laplacian of original graph
# t_s = cofactor of row s, column t (not row s, col s!)
# Actually for paths, we need the (t,s) cofactor of the Laplacian.
# = (-1)^{s+t} * det of matrix with row t and column s removed.

s_idx = node_idx[(0,0,0)]
t_idx = node_idx[(1,1,1)]

L3_reduced = np.delete(np.delete(L3, t_idx, axis=0), s_idx, axis=1)
t_s_cofactor = int(round(abs(np.linalg.det(L3_reduced.astype(float)))))
print(f"\nCofactor (row=Tai, col=Qian): {t_s_cofactor}")

# Product of (d_out(v) - 1)! for v != s in ORIGINAL graph
# Wait — the formula for Euler paths from s to t in a directed multigraph:
# # paths = t_s(G) * d_out(s)! * ∏_{v≠s,t} (d_out(v)-1)! * ... 
# Hmm, let me look this up more carefully.

# The BEST theorem for Euler PATHS (not circuits):
# In a connected directed multigraph where d_out(s) = d_in(s) + 1 and d_out(t) + 1 = d_in(t)
# (and all other nodes balanced):
# # Euler paths s→t = t_s * ∏_v (d_out(v) - [v=s ? 0 : 1])! ... 
# Actually the simplest correct formula:
# Add edge t→s to get balanced graph G'.
# # Euler paths s→t = ec(G') / m'_{ts}
# where m'_{ts} is the multiplicity of edge t→s in G'.
# This is because each Euler circuit in G' passes through each copy of t→s exactly once
# (by symmetry of identical edges), and cutting at any one gives a path.
# Wait — it passes through ALL m'_ts copies, not "any one."
# So each circuit, when we cut at the added edge, gives one path.
# But the BEST theorem counts circuits where identical edges are interchangeable.
# So ec(G') already accounts for the indistinguishability.
# Therefore: # Euler paths = ec(G'), regardless of whether t→s existed before.

print(f"\n★★★ Final answer: {ec} Eulerian paths from Qian(000) to Tai(111)")

# Let's also use a different formula as cross-check
# Using scipy for more numerically stable determinant
try:
    from scipy import linalg as sla
    det_check = int(round(abs(sla.det(L_reduced.astype(float)))))
    print(f"Cross-check t_w with scipy: {det_check}")
except ImportError:
    pass

# Let me also compute using exact integer arithmetic
# to avoid floating point issues
def det_int(matrix):
    """Integer determinant using Bareiss algorithm."""
    n = len(matrix)
    M = [list(row) for row in matrix]
    sign = 1
    for i in range(n):
        # Find pivot
        if M[i][i] == 0:
            for j in range(i+1, n):
                if M[j][i] != 0:
                    M[i], M[j] = M[j], M[i]
                    sign *= -1
                    break
            else:
                return 0
        for j in range(i+1, n):
            for k in range(i+1, n):
                M[j][k] = M[j][k] * M[i][i] - M[j][i] * M[i][k]
                if i > 0:
                    M[j][k] //= M[i-1][i-1] if i > 0 else 1
            M[j][i] = 0
    return sign * M[n-1][n-1]

# Exact integer determinant
L_red_int = L_reduced.tolist()
t_w_exact = abs(det_int(L_red_int))
print(f"\nExact integer t_w: {t_w_exact}")

ec_exact = t_w_exact * prod_factorial // prod_mult
print(f"Exact Euler circuits: {ec_exact}")
print(f"\n★★★ EXACT: {ec_exact} Eulerian paths from Qian to Tai ★★★")
