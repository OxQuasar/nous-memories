#!/usr/bin/env python3
"""
Market Regime Predictions from Q₃ × Z₅ Grammar

Maps 8 market regimes to Q₃ vertices using canonical axis assignment
(b₀=trend, b₁=volatility, b₂=liquidity), classifies all 12 single-axis
transitions, identifies P₄克 paths, and computes null P(克→克).
"""

from collections import defaultdict

# ── Axes ──────────────────────────────────────────────────────────────

AXIS_NAMES = {0: 'trend', 1: 'volatility', 2: 'liquidity'}
AXIS_VALUES = {
    0: {0: 'Down', 1: 'Up'},
    1: {0: 'Low vol', 1: 'High vol'},
    2: {0: 'Scarce liq', 1: 'Abundant liq'},
}

# ── Regime definitions ────────────────────────────────────────────────

REGIMES = {
    0b000: 'Quiet decline',
    0b001: 'Grinding rally',
    0b010: 'Panic/capitulation',
    0b011: 'Short squeeze',
    0b100: 'Slow bleed',
    0b101: 'Healthy bull',
    0b110: 'Correction',
    0b111: 'Euphoria',
}

# ── Canonical Z₅ typing (from trigram assignment) ─────────────────────

Z5_TYPING = {
    0b000: 2,  # 坤 → 土
    0b001: 0,  # 震 → 木
    0b010: 4,  # 坎 → 水
    0b011: 3,  # 兌 → 金
    0b100: 2,  # 艮 → 土
    0b101: 1,  # 離 → 火
    0b110: 0,  # 巽 → 木
    0b111: 3,  # 乾 → 金
}

Z5_NAMES = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}
TRIGRAMS = {
    0b000: '坤', 0b001: '震', 0b010: '坎', 0b011: '兌',
    0b100: '艮', 0b101: '離', 0b110: '巽', 0b111: '乾',
}

VERTICES = list(range(8))
EDGES = [(u, v) for u in VERTICES for v in VERTICES
         if u < v and bin(u ^ v).count('1') == 1]


def edge_type(fa, fb):
    """Classify by Z₅ difference."""
    d = (fa - fb) % 5
    if d == 0:
        return '比和'
    elif d in (1, 4):
        return '生'
    else:
        return '克'


def flipped_axis(u, v):
    """Return which single bit differs."""
    diff = u ^ v
    for i in range(3):
        if diff == (1 << i):
            return i
    return None


# ── Build transition table ────────────────────────────────────────────

def build_transitions():
    """All 12 edges with full annotation."""
    transitions = []
    for u, v in EDGES:
        axis = flipped_axis(u, v)
        t = edge_type(Z5_TYPING[u], Z5_TYPING[v])
        transitions.append({
            'from': u, 'to': v, 'axis': axis,
            'type': t,
            'z5_from': Z5_TYPING[u], 'z5_to': Z5_TYPING[v],
        })
        # Reverse direction (same type — undirected)
        transitions.append({
            'from': v, 'to': u, 'axis': axis,
            'type': t,
            'z5_from': Z5_TYPING[v], 'z5_to': Z5_TYPING[u],
        })
    return transitions


def find_paths(target_type):
    """Find connected components of edges with given type. Return as vertex paths."""
    typed_edges = [(u, v) for u, v in EDGES
                   if edge_type(Z5_TYPING[u], Z5_TYPING[v]) == target_type]
    adj = defaultdict(set)
    for u, v in typed_edges:
        adj[u].add(v)
        adj[v].add(u)

    visited = set()
    paths = []
    for start in sorted(adj):
        if start in visited:
            continue
        # Trace the path
        path = []
        # Find an endpoint (degree 1)
        node = start
        while len(adj[node] - visited) > 0 or not path:
            if not path:
                # Find a degree-1 node in this component
                comp = set()
                stack = [node]
                while stack:
                    n = stack.pop()
                    if n not in comp:
                        comp.add(n)
                        stack.extend(adj[n] - comp)
                endpoints = [n for n in comp if len(adj[n]) == 1]
                node = endpoints[0] if endpoints else min(comp)
                path = [node]
                visited.add(node)
            neighbors = adj[node] - visited
            if not neighbors:
                break
            node = min(neighbors)
            path.append(node)
            visited.add(node)
        paths.append(path)
    return paths


def vertex_label(v):
    return f"{v:03b}"


def regime_desc(v):
    axes = []
    for i in range(3):
        axes.append(AXIS_VALUES[i][(v >> i) & 1])
    return f"{REGIMES[v]} ({', '.join(axes)})"


# ── Null model: P(克→克) under uniform random walk ────────────────────

def compute_null_ke_ke():
    """At each vertex, compute P(克→克) under uniform random walk on Q₃.

    At vertex v, 3 neighbors (one per axis flip). Each equally likely (p=1/3).
    P(克|v) = fraction of v's neighbors connected by 克 edge.
    P(克→克|v) = P(first step is 克 from v) × P(second step is 克 from neighbor).
    """
    results = {}
    for v in VERTICES:
        neighbors = [v ^ (1 << i) for i in range(3)]
        neighbor_types = [edge_type(Z5_TYPING[v], Z5_TYPING[n]) for n in neighbors]
        ke_neighbors = [(n, t) for n, t in zip(neighbors, neighbor_types) if t == '克']
        p_ke_from_v = len(ke_neighbors) / 3

        # For each 克 neighbor, P(克) from that neighbor
        p_ke_ke_paths = 0
        for n, _ in ke_neighbors:
            n_neighbors = [n ^ (1 << i) for i in range(3)]
            n_types = [edge_type(Z5_TYPING[n], Z5_TYPING[nn]) for nn in n_neighbors]
            p_ke_from_n = sum(1 for t in n_types if t == '克') / 3
            p_ke_ke_paths += (1 / 3) * p_ke_from_n  # P(go to n) × P(克 from n)

        results[v] = {
            'p_ke': p_ke_from_v,
            'p_ke_ke': p_ke_ke_paths,
            'ke_neighbors': ke_neighbors,
            'all_types': list(zip(neighbors, neighbor_types)),
        }
    return results


# ── Main ──────────────────────────────────────────────────────────────

def main():
    print("=" * 75)
    print("MARKET REGIME PREDICTIONS — Q₃ × Z₅ Grammar")
    print("=" * 75)

    # ── Regime table ──
    print("\n── 8 Market Regimes ──")
    print(f"  {'Binary':>6}  {'Trigram':>4}  {'Z₅':>3}  {'Element':>4}  Regime")
    print(f"  {'------':>6}  {'------':>4}  {'--':>3}  {'-------':>4}  ------")
    for v in VERTICES:
        print(f"  {vertex_label(v):>6}  {TRIGRAMS[v]:>4}  "
              f"{Z5_TYPING[v]:>3}  {Z5_NAMES[Z5_TYPING[v]]:>4}  {regime_desc(v)}")

    # ── All 12 transitions ──
    print(f"\n── 12 Single-Axis Transitions (Q₃ edges) ──")
    print(f"  {'From':>20} → {'To':<20}  Axis        Z₅→Z₅  Type")
    print(f"  {'----':>20}   {'--':<20}  ----        ------  ----")

    by_type = defaultdict(list)
    for u, v in EDGES:
        axis = flipped_axis(u, v)
        t = edge_type(Z5_TYPING[u], Z5_TYPING[v])
        by_type[t].append((u, v, axis))
        axis_name = AXIS_NAMES[axis]
        flip_desc = f"{AXIS_VALUES[axis][((u>>axis)&1)]}→{AXIS_VALUES[axis][((v>>axis)&1)]}"
        print(f"  {REGIMES[u]:>20} → {REGIMES[v]:<20}  "
              f"{axis_name:<6} ({flip_desc:<16})  "
              f"{Z5_NAMES[Z5_TYPING[u]]}→{Z5_NAMES[Z5_TYPING[v]]}  {t}")

    # ── Edge counts ──
    print(f"\n── Edge count by type ──")
    for t in ('比和', '生', '克'):
        edges = by_type[t]
        print(f"  {t}: {len(edges)} edges")

    # ── P₄ paths (克 subgraph) ──
    print(f"\n── 克 subgraph: two P₄ paths ──")
    ke_paths = find_paths('克')
    for i, path in enumerate(ke_paths):
        labels = [f"{REGIMES[v]} ({vertex_label(v)}, {Z5_NAMES[Z5_TYPING[v]]})"
                  for v in path]
        print(f"\n  P₄ path {i + 1}:")
        for j, v in enumerate(path):
            prefix = "    " if j == 0 else " →克→"
            print(f"  {prefix} {labels[j]}")

    # ── P₃ paths (生 subgraph) ──
    print(f"\n── 生 subgraph: two P₃ paths ──")
    sheng_paths = find_paths('生')
    for i, path in enumerate(sheng_paths):
        labels = [f"{REGIMES[v]} ({vertex_label(v)}, {Z5_NAMES[Z5_TYPING[v]]})"
                  for v in path]
        print(f"\n  P₃ path {i + 1}:")
        for j, v in enumerate(path):
            prefix = "    " if j == 0 else " →生→"
            print(f"  {prefix} {labels[j]}")

    # ── K₂ pairs (比和 subgraph) ──
    print(f"\n── 比和 subgraph: two K₂ pairs ──")
    for u, v, axis in by_type['比和']:
        print(f"  {REGIMES[u]} ({Z5_NAMES[Z5_TYPING[u]]}) "
              f"↔ {REGIMES[v]} ({Z5_NAMES[Z5_TYPING[v]]})  "
              f"[{AXIS_NAMES[axis]} flip]")

    # ── GMS-forbidden sequences ──
    print(f"\n── GMS-Forbidden Sequences (克→克 consecutive) ──")
    print(f"  The GMS predicts: after a 克 transition, the next single-axis")
    print(f"  transition should NOT be 克. Forbidden 3-step paths on P₄:")
    print()

    for i, path in enumerate(ke_paths):
        print(f"  P₄ path {i + 1}: ", end="")
        print(" →克→ ".join(REGIMES[v] for v in path))
        # Consecutive 克→克 pairs within this path
        for j in range(len(path) - 2):
            a, b, c = path[j], path[j + 1], path[j + 2]
            axis_ab = flipped_axis(a, b) if a < b else flipped_axis(b, a)
            axis_bc = flipped_axis(b, c) if b < c else flipped_axis(c, b)
            print(f"    FORBIDDEN: {REGIMES[a]} →克({AXIS_NAMES[axis_ab]})→ "
                  f"{REGIMES[b]} →克({AXIS_NAMES[axis_bc]})→ {REGIMES[c]}")

    # ── Null model ──
    print(f"\n── P(克→克) under uniform random walk null ──")
    print(f"  At each vertex, 3 neighbors (one per axis). Uniform p=1/3 each.")
    print()
    null = compute_null_ke_ke()

    print(f"  {'Regime':>20}  Elem  #克 nbrs  P(克)  P(克→克)")
    print(f"  {'------':>20}  ----  --------  -----  --------")
    total_p_ke_ke = 0
    for v in VERTICES:
        r = null[v]
        n_ke = len(r['ke_neighbors'])
        print(f"  {REGIMES[v]:>20}  {Z5_NAMES[Z5_TYPING[v]]:>4}  "
              f"{n_ke:>8}  {r['p_ke']:.3f}  {r['p_ke_ke']:.4f}")
        total_p_ke_ke += r['p_ke_ke']

    avg_p_ke_ke = total_p_ke_ke / 8
    print(f"\n  Average P(克→克) across all vertices: {avg_p_ke_ke:.4f}")
    print(f"  Under uniform null (3 types, if independent): ~(6/12)×(6/12) = 0.2500")
    print(f"  Actual average vs naive: {avg_p_ke_ke:.4f} vs 0.2500")

    # ── Neighbor type table ──
    print(f"\n── Complete neighbor type table ──")
    print(f"  {'Regime':>20}  {'Axis 0 (trend)':>16}  {'Axis 1 (vol)':>16}  {'Axis 2 (liq)':>16}")
    print(f"  {'------':>20}  {'-------------':>16}  {'----------':>16}  {'----------':>16}")
    for v in VERTICES:
        types = []
        for i in range(3):
            n = v ^ (1 << i)
            t = edge_type(Z5_TYPING[v], Z5_TYPING[n])
            types.append(f"{t}→{REGIMES[n][:8]}")
        print(f"  {REGIMES[v]:>20}  {types[0]:>16}  {types[1]:>16}  {types[2]:>16}")

    # ── Summary ──
    print(f"\n{'=' * 75}")
    print("SUMMARY")
    print(f"{'=' * 75}")
    print(f"""
  Canonical axis assignment: b₀=trend, b₁=volatility, b₂=liquidity
  Z₅ typing: canonical trigram assignment (equivariant, surjective)

  Edge distribution: 比和=2, 生=4, 克=6 (invariant under axis relabeling)
  克 dominance: 50% of transitions are destructive

  Two 克-paths (P₄):""")
    for i, path in enumerate(ke_paths):
        chain = " →克→ ".join(f"{REGIMES[v]}" for v in path)
        print(f"    {i + 1}. {chain}")

    print(f"""
  GMS prediction: consecutive 克→克 transitions are suppressed.
  This forbids {2 * (len(ke_paths[0]) - 2)} specific 3-regime sequences
  (2 per P₄ path × 2 directions = {2 * 2 * (len(ke_paths[0]) - 2)} directed sequences).

  Null P(克→克): {avg_p_ke_ke:.4f} (ranges {min(r['p_ke_ke'] for r in null.values()):.4f}–{max(r['p_ke_ke'] for r in null.values()):.4f} by vertex)
  If GMS holds, observed rate should be significantly below this.
""")


if __name__ == '__main__':
    main()
