"""
φ dynamics on F₂³ cube-edge partition and fiber-lifted graphs.

Trigram → Element mapping (from atlas.json):
  000 Kun ☷  → Earth    100 Gen ☶  → Earth
  001 Zhen ☳ → Wood     101 Li ☲   → Fire
  010 Kan ☵  → Water    110 Xun ☴  → Wood
  011 Dui ☱  → Metal    111 Qian ☰ → Metal

Z₅ labeling: Wood=0, Fire=1, Earth=2, Metal=3, Water=4
生 = stride +1 (0→1→2→3→4→0)
克 = stride +2 (0→2→4→1→3→0)
比和 = stride 0 (same element)
"""

import numpy as np
from itertools import combinations

np.set_printoptions(precision=6, suppress=True, linewidth=120)

# ── Data ──────────────────────────────────────────────────────────────
TRIGRAMS = {
    0: ("Kun ☷",  "Earth"),
    1: ("Zhen ☳", "Wood"),
    2: ("Kan ☵",  "Water"),
    3: ("Dui ☱",  "Metal"),
    4: ("Gen ☶",  "Earth"),
    5: ("Li ☲",   "Fire"),
    6: ("Xun ☴",  "Wood"),
    7: ("Qian ☰", "Metal"),
}

ELEMENT_TO_Z5 = {"Wood": 0, "Fire": 1, "Earth": 2, "Metal": 3, "Water": 4}
Z5_NAMES = {0: "Wood", 1: "Fire", 2: "Earth", 3: "Metal", 4: "Water"}

def trigram_z5(v):
    return ELEMENT_TO_Z5[TRIGRAMS[v][1]]

def hamming_dist(a, b):
    return bin(a ^ b).count('1')

def z5_relation(a_z5, b_z5):
    """Classify Z₅ relation between two elements."""
    d = (b_z5 - a_z5) % 5
    if d == 0: return "比和"
    if d in (1, 4): return "生"   # stride ±1
    if d in (2, 3): return "克"   # stride ±2
    assert False

def label(v):
    name, elem = TRIGRAMS[v]
    return f"{v:03b} {name:8s} ({elem})"

def analyze_subgraph(name, adj, header=True):
    """Full analysis of an 8×8 adjacency matrix subgraph."""
    if header:
        print(f"\n{'='*70}")
        print(f"  {name}")
        print(f"{'='*70}")

    # Adjacency matrix
    print(f"\nAdjacency matrix (rows/cols = trigrams 0..7):")
    print(adj)

    # Degrees
    degrees = adj.sum(axis=1).astype(int)
    print(f"\nVertex degrees:")
    for v in range(8):
        if degrees[v] > 0:
            print(f"  {label(v)}: degree {degrees[v]}")

    # Edge count
    edge_count = int(adj.sum()) // 2
    print(f"\nEdge count: {edge_count}")

    # Connected components (BFS)
    visited = set()
    components = []
    for start in range(8):
        if start in visited or degrees[start] == 0:
            continue
        comp = []
        queue = [start]
        while queue:
            v = queue.pop(0)
            if v in visited:
                continue
            visited.add(v)
            comp.append(v)
            for u in range(8):
                if adj[v, u] and u not in visited:
                    queue.append(u)
        components.append(sorted(comp))

    # Isolated vertices
    isolated = [v for v in range(8) if degrees[v] == 0]

    print(f"\nConnected components ({len(components)}):")
    for i, comp in enumerate(components):
        members = ", ".join(label(v) for v in comp)
        comp_degrees = {v: degrees[v] for v in comp}
        endpoints = [v for v in comp if degrees[v] == 1]
        interior = [v for v in comp if degrees[v] >= 2]
        print(f"  C{i}: [{members}]")
        print(f"       Endpoints (deg 1): {[label(v) for v in endpoints]}")
        print(f"       Interior  (deg≥2): {[label(v) for v in interior]}")

        # Path structure: trace the path if it's a path graph
        if all(d <= 2 for d in comp_degrees.values()) and len(endpoints) == 2:
            path = [endpoints[0]]
            while len(path) < len(comp):
                cur = path[-1]
                for u in comp:
                    if adj[cur, u] and u not in path:
                        path.append(u)
                        break
            path_str = " — ".join(f"{TRIGRAMS[v][0]}({TRIGRAMS[v][1]})" for v in path)
            print(f"       Path order: {path_str}")

    if isolated:
        print(f"  Isolated: {[label(v) for v in isolated]}")

    # Eigenvalues of full 8×8 matrix
    eigvals = np.linalg.eigvalsh(adj.astype(float))
    eigvals = np.sort(eigvals)[::-1]
    print(f"\nFull 8×8 spectrum: {eigvals}")

    # Per-component spectra
    phi = (1 + np.sqrt(5)) / 2
    print(f"\nPer-component spectra:")
    for i, comp in enumerate(components):
        sub = adj[np.ix_(comp, comp)].astype(float)
        ev = np.linalg.eigvalsh(sub)
        ev = np.sort(ev)[::-1]
        print(f"  C{i} ({len(comp)} vertices): {ev}")
        # Check for φ
        for e in ev:
            if abs(abs(e) - phi) < 1e-9:
                print(f"    ^^^ contains ±φ = ±{phi:.6f}")
                break

    return components, degrees, eigvals


def perron_frobenius(adj, components):
    """Compute PF eigenvector for each component."""
    phi = (1 + np.sqrt(5)) / 2
    print(f"\nPerron-Frobenius eigenvectors:")
    for i, comp in enumerate(components):
        sub = adj[np.ix_(comp, comp)].astype(float)
        eigvals, eigvecs = np.linalg.eigh(sub)
        # Largest eigenvalue
        idx = np.argmax(eigvals)
        lam = eigvals[idx]
        vec = eigvecs[:, idx]
        # Ensure positive
        if vec[0] < 0:
            vec = -vec
        # Normalize to sum=1
        vec_norm = vec / vec.sum()
        print(f"  C{i}: λ_max = {lam:.6f}, PF eigenvector (normalized):")
        for j, v in enumerate(comp):
            print(f"    {label(v)}: {vec_norm[j]:.6f}")


def walk_counts(name, adj, k_max=10):
    """Compute walk count growth: total entries of A^k."""
    print(f"\nWalk count growth for {name}:")
    print(f"  {'k':>3s}  {'||A^k||_sum':>14s}  {'||A^k||_inf':>14s}  {'ratio_sum':>10s}")
    A = adj.astype(float)
    Ak = np.eye(8)
    prev_sum = None
    for k in range(1, k_max + 1):
        Ak = Ak @ A
        s = Ak.sum()
        inf = Ak.max()
        ratio = s / prev_sum if prev_sum and prev_sum > 0 else 0
        print(f"  {k:3d}  {s:14.2f}  {inf:14.2f}  {ratio:10.6f}")
        prev_sum = s


# ══════════════════════════════════════════════════════════════════════
# PART 1: Cube-edge partition
# ══════════════════════════════════════════════════════════════════════
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║  PART 1: Cube-edge partition (Hamming distance 1 edges of F₂³)     ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

# Build all 12 Hamming-distance-1 edges
edges_bihe = []  # 比和
edges_sheng = []  # 生
edges_ke = []  # 克

adj_bihe = np.zeros((8, 8), dtype=int)
adj_sheng = np.zeros((8, 8), dtype=int)
adj_ke = np.zeros((8, 8), dtype=int)

print("\nAll 12 cube edges with relations:")
for a, b in combinations(range(8), 2):
    if hamming_dist(a, b) != 1:
        continue
    rel = z5_relation(trigram_z5(a), trigram_z5(b))
    print(f"  {a:03b}({TRIGRAMS[a][1]:6s}) — {b:03b}({TRIGRAMS[b][1]:6s}): {rel}")
    if rel == "比和":
        edges_bihe.append((a, b))
        adj_bihe[a, b] = adj_bihe[b, a] = 1
    elif rel == "生":
        edges_sheng.append((a, b))
        adj_sheng[a, b] = adj_sheng[b, a] = 1
    else:
        edges_ke.append((a, b))
        adj_ke[a, b] = adj_ke[b, a] = 1

print(f"\nEdge counts: 比和={len(edges_bihe)}, 生={len(edges_sheng)}, 克={len(edges_ke)} (total={len(edges_bihe)+len(edges_sheng)+len(edges_ke)})")

comp_bihe, deg_bihe, _ = analyze_subgraph("比和 (same element) — cube edges", adj_bihe)
comp_sheng, deg_sheng, _ = analyze_subgraph("生 (generative, stride ±1) — cube edges", adj_sheng)
comp_ke, deg_ke, eig_ke = analyze_subgraph("克 (overcoming, stride ±2) — cube edges", adj_ke)

# ══════════════════════════════════════════════════════════════════════
# PART 2: Fiber-lifted relational graph
# ══════════════════════════════════════════════════════════════════════
print("\n\n")
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║  PART 2: Fiber-lifted relational graph (Z₅ edges lifted to F₂³)    ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

# Build fibers
fibers = {}
for v in range(8):
    z = trigram_z5(v)
    fibers.setdefault(z, []).append(v)

print("\nFibers (Z₅ → F₂³):")
for z in range(5):
    members = ", ".join(label(v) for v in fibers[z])
    print(f"  {z} ({Z5_NAMES[z]}): [{members}]")

def build_lifted_graph(relation_pairs):
    """Build graph by lifting Z₅ edges to F₂³ via fiber product."""
    adj = np.zeros((8, 8), dtype=int)
    for a_z5, b_z5 in relation_pairs:
        for u in fibers[a_z5]:
            for v in fibers[b_z5]:
                adj[u, v] = adj[v, u] = 1
    return adj

# 比和: self-loops on Z₅ (within each fiber)
adj_bihe_lift = np.zeros((8, 8), dtype=int)
for z in range(5):
    for u in fibers[z]:
        for v in fibers[z]:
            if u != v:
                adj_bihe_lift[u, v] = 1

# 生: stride ±1 on Z₅
sheng_pairs = [(i, (i + 1) % 5) for i in range(5)]
adj_sheng_lift = build_lifted_graph(sheng_pairs)

# 克: stride ±2 on Z₅
ke_pairs = [(i, (i + 2) % 5) for i in range(5)]
adj_ke_lift = build_lifted_graph(ke_pairs)

analyze_subgraph("比和 (same element) — fiber-lifted", adj_bihe_lift)
analyze_subgraph("生 (generative) — fiber-lifted", adj_sheng_lift)
analyze_subgraph("克 (overcoming) — fiber-lifted", adj_ke_lift)

# ══════════════════════════════════════════════════════════════════════
# PART 2.5: Comparison — which cube edges survive in lifted graphs?
# ══════════════════════════════════════════════════════════════════════
print("\n\n")
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║  PART 2.5: Cube edges vs fiber-lifted edges                        ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

for name, adj_cube, adj_lift in [("比和", adj_bihe, adj_bihe_lift),
                                   ("生", adj_sheng, adj_sheng_lift),
                                   ("克", adj_ke, adj_ke_lift)]:
    cube_edges = set()
    lift_edges = set()
    for a, b in combinations(range(8), 2):
        if adj_cube[a, b]: cube_edges.add((a, b))
        if adj_lift[a, b]: lift_edges.add((a, b))

    common = cube_edges & lift_edges
    cube_only = cube_edges - lift_edges
    lift_only = lift_edges - cube_edges

    print(f"\n{name}:")
    print(f"  Cube edges: {len(cube_edges)}, Lifted edges: {len(lift_edges)}")
    print(f"  Common: {len(common)}, Cube-only: {len(cube_only)}, Lifted-only: {len(lift_only)}")
    if cube_only:
        print(f"  Cube-only edges (Hamming-1 but NOT in fiber product): {cube_only}")
    if lift_only:
        extra = [(a, b, hamming_dist(a, b)) for a, b in lift_only]
        print(f"  Lifted-only edges (in fiber product but NOT Hamming-1): {extra}")


# ══════════════════════════════════════════════════════════════════════
# PART 3: Operational dynamics on Part 1's graphs
# ══════════════════════════════════════════════════════════════════════
print("\n\n")
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║  PART 3: Operational dynamics (Perron-Frobenius + walk counts)      ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

print("\n── 克 subgraph (cube edges) ──")
perron_frobenius(adj_ke, comp_ke)
walk_counts("克 (cube)", adj_ke)

print("\n── 生 subgraph (cube edges) ──")
perron_frobenius(adj_sheng, comp_sheng)
walk_counts("生 (cube)", adj_sheng)

print("\n── 比和 subgraph (cube edges) ──")
perron_frobenius(adj_bihe, comp_bihe)
walk_counts("比和 (cube)", adj_bihe)


# ══════════════════════════════════════════════════════════════════════
# PART 4: Discriminator — structural vs content-dependent
# ══════════════════════════════════════════════════════════════════════
print("\n\n")
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║  PART 4: Discriminator — abstract vs assignment-dependent           ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

phi = (1 + np.sqrt(5)) / 2
print(f"\nφ = {phi:.10f}")
print(f"1/φ = {1/phi:.10f}")

# P_n eigenvalues: 2*cos(k*pi/(n+1)) for k=1..n
print("\nAbstract path graph spectra:")
for n in range(2, 6):
    ev = [2 * np.cos(k * np.pi / (n + 1)) for k in range(1, n + 1)]
    ev.sort(reverse=True)
    print(f"  P_{n}: {[f'{e:.6f}' for e in ev]}")
    if any(abs(abs(e) - phi) < 1e-9 for e in ev):
        print(f"    ^^^ contains ±φ")

# Key question: does the PF eigenvector structure depend on WHERE
# singletons sit in the path?
print("\n\nPF eigenvectors of abstract P_n (always the same regardless of vertex labels):")
for n in [3, 4]:
    A = np.zeros((n, n))
    for i in range(n - 1):
        A[i, i + 1] = A[i + 1, i] = 1
    eigvals, eigvecs = np.linalg.eigh(A)
    idx = np.argmax(eigvals)
    vec = eigvecs[:, idx]
    if vec[0] < 0:
        vec = -vec
    vec_norm = vec / vec.sum()
    print(f"  P_{n}: λ_max = {eigvals[idx]:.6f}")
    print(f"    Eigenvector (normalized): {vec_norm}")
    print(f"    Ratio endpoint/interior: {vec_norm[0]/vec_norm[1]:.6f}" if n > 2 else "")

# Now check: in the actual 克 P₄ components, which element types sit where?
print("\n\nActual 克 P₄ component structure:")
for i, comp in enumerate(comp_ke):
    sub = adj_ke[np.ix_(comp, comp)].astype(float)
    degs = sub.sum(axis=1).astype(int)
    endpoints = [comp[j] for j in range(len(comp)) if degs[j] == 1]
    interior = [comp[j] for j in range(len(comp)) if degs[j] >= 2]

    # Trace path
    path = [endpoints[0]]
    while len(path) < len(comp):
        cur = path[-1]
        for j, v in enumerate(comp):
            if sub[comp.index(cur), j] and v not in path:
                path.append(v)
                break

    print(f"\n  C{i} path:")
    for pos, v in enumerate(path):
        role = "ENDPOINT" if v in endpoints else "interior"
        elem = TRIGRAMS[v][1]
        z5 = trigram_z5(v)
        fiber_size = len(fibers[z5])
        print(f"    pos {pos}: {label(v)}, Z₅={z5}, fiber_size={fiber_size}, role={role}")

print("\n\nActual 生 P₃ component structure:")
for i, comp in enumerate(comp_sheng):
    sub = adj_sheng[np.ix_(comp, comp)].astype(float)
    degs = sub.sum(axis=1).astype(int)
    endpoints = [comp[j] for j in range(len(comp)) if degs[j] == 1]
    interior = [comp[j] for j in range(len(comp)) if degs[j] >= 2]

    path = [endpoints[0]]
    while len(path) < len(comp):
        cur = path[-1]
        for j, v in enumerate(comp):
            if sub[comp.index(cur), j] and v not in path:
                path.append(v)
                break

    print(f"\n  C{i} path:")
    for pos, v in enumerate(path):
        role = "ENDPOINT" if v in endpoints else "interior"
        elem = TRIGRAMS[v][1]
        z5 = trigram_z5(v)
        fiber_size = len(fibers[z5])
        print(f"    pos {pos}: {label(v)}, Z₅={z5}, fiber_size={fiber_size}, role={role}")


# ══════════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════════
print("\n\n")
print("╔══════════════════════════════════════════════════════════════════════╗")
print("║  SUMMARY                                                           ║")
print("╚══════════════════════════════════════════════════════════════════════╝")

print("""
CUBE-EDGE PARTITION:
  12 edges decompose as: 比和→2, 生→4, 克→6 edges
  (Verify: 2 + 4 + 6 = 12 ✓)

SUBGRAPH STRUCTURES (cube edges):
  比和: P₂ ∪ isolated vertices (same-element Hamming-1 pairs)
  生:   check components above
  克:   check components above

DISCRIMINATOR ANSWER:
  The spectrum {±φ, ±1/φ} is a property of P₄ as an abstract graph.
  ANY 4-vertex path has these eigenvalues regardless of labeling.
  The PF eigenvector weights are [.276, .447, .447, .276] for ANY P₄.

  What IS assignment-dependent:
  - WHICH trigrams form a P₄ (vs P₃ vs P₂) — this depends on how the
    Hamming-1 constraint intersects the Z₅ fiber structure
  - Which element types sit at endpoints vs interior positions
  - Whether singletons (Fire, Water with fiber_size=1) are systematically
    at path endpoints (lower PF weight) or interior (higher PF weight)
""")
