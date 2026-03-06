#!/usr/bin/env python3
"""
01_functional_graph.py — Full 64-node 互 functional graph.

For every hexagram h (0–63), compute hugua(h). Analyze the resulting
functional graph: basins, convergence depth, tree structure, fiber
structure, in-degree distribution.
"""

import sys
sys.path.insert(0, 'memories/iching/opposition-theory/phase4')
sys.path.insert(0, 'memories/iching/kingwen')

from collections import defaultdict
from cycle_algebra import (
    hugua, lower_trigram, upper_trigram, fmt6, fmt3, bit,
    TRIGRAM_NAMES, TRIGRAM_ELEMENT
)
from sequence import KING_WEN

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

# ═══════════════════════════════════════════════════════════════════════
# Constants & Lookups
# ═══════════════════════════════════════════════════════════════════════

NUM_HEX = 64
ATTRACTORS = frozenset({0, 21, 42, 63})
ATTRACTOR_SETS = [frozenset({0}), frozenset({63}), frozenset({21, 42})]

BASIN_NAMES = {
    frozenset({0}): "Kun ☷",
    frozenset({63}): "Qian ☰",
    frozenset({21, 42}): "JiJi↔WeiJi ☵☲",
}

BASIN_COLORS = {
    "Kun ☷": "#4488cc",
    "Qian ☰": "#cc4444",
    "JiJi↔WeiJi ☵☲": "#44aa44",
}

def build_kw_lookup():
    """Binary value → (KW number, name)."""
    lookup = {}
    for kw_num, name, binstr in KING_WEN:
        val = sum(int(c) << i for i, c in enumerate(binstr))
        lookup[val] = (kw_num, name)
    return lookup

KW = build_kw_lookup()

def kw_label(h):
    kw_num, name = KW[h]
    return f"{kw_num}.{name}"

def inner(h):
    """Extract inner 4 bits (bits 1-4)."""
    return (h >> 1) & 0xF

def fmt_lines(h):
    """Bottom-to-top line representation."""
    return ''.join(str(bit(h, i)) for i in range(6))


# ═══════════════════════════════════════════════════════════════════════
# Graph Construction
# ═══════════════════════════════════════════════════════════════════════

def build_graph():
    """Build functional graph: each node h → hugua(h)."""
    return {h: hugua(h) for h in range(NUM_HEX)}

def find_basin(h, edges):
    """Follow h to its attractor set."""
    visited = set()
    node = h
    while node not in visited:
        visited.add(node)
        node = edges[node]
    # node is now in a cycle — find which attractor set
    for aset in ATTRACTOR_SETS:
        if node in aset:
            return aset
    raise ValueError(f"No attractor set for {h}")

def compute_depths(edges):
    """BFS from attractors — proper level-by-level."""
    depth = {a: 0 for a in ATTRACTORS}
    frontier = set(ATTRACTORS)
    d = 0
    while frontier:
        d += 1
        next_frontier = set()
        for h in range(NUM_HEX):
            if h not in depth and edges[h] in frontier:
                depth[h] = d
                next_frontier.add(h)
        frontier = next_frontier
    return depth


# ═══════════════════════════════════════════════════════════════════════
# Analysis
# ═══════════════════════════════════════════════════════════════════════

def print_edge_table(edges, depth, basins):
    """Full edge table: h → hugua(h) with metadata."""
    print("\n" + "=" * 90)
    print("FULL EDGE TABLE: h → hugua(h)")
    print("=" * 90)
    header = f"{'h':>3} {'bin(h)':>8} {'KW#':>4} {'Name':>12} → {'hu':>3} {'bin(hu)':>8} {'KW#hu':>4} {'HuName':>12} {'depth':>5} {'basin':>16}"
    print(header)
    print("-" * len(header))

    for h in range(NUM_HEX):
        hu = edges[h]
        kw_h, name_h = KW[h]
        kw_hu, name_hu = KW[hu]
        basin_name = BASIN_NAMES[basins[h]]
        print(f"{h:3d} {fmt6(h):>8} {kw_h:4d} {name_h:>12} → {hu:3d} {fmt6(hu):>8} {kw_hu:4d} {name_hu:>12} {depth[h]:5d} {basin_name:>16}")


def print_indegree(edges):
    """In-degree distribution."""
    in_deg = defaultdict(int)
    sources = defaultdict(list)
    for h in range(NUM_HEX):
        target = edges[h]
        in_deg[target] += 1
        sources[target].append(h)

    print("\n" + "=" * 70)
    print("IN-DEGREE DISTRIBUTION")
    print("=" * 70)

    # Group by in-degree value
    by_indeg = defaultdict(list)
    for h in range(NUM_HEX):
        by_indeg[in_deg[h]].append(h)

    for deg in sorted(by_indeg.keys()):
        nodes = by_indeg[deg]
        print(f"\n  In-degree {deg}: {len(nodes)} nodes")
        if deg > 0:
            for h in nodes:
                srcs = sources[h]
                kw_num, name = KW[h]
                src_labels = [f"{s}({KW[s][0]})" for s in srcs]
                print(f"    {h:3d} KW#{kw_num:2d} {name:12s} ← [{', '.join(src_labels)}]")

    # Summary
    never_targets = [h for h in range(NUM_HEX) if in_deg[h] == 0]
    print(f"\n  Never-target hexagrams: {len(never_targets)}")
    print(f"  Always-target (hugua output) hexagrams: {NUM_HEX - len(never_targets)}")

    return in_deg


def print_tree_structure(edges, depth, basins):
    """Tree structure per basin."""
    print("\n" + "=" * 70)
    print("TREE STRUCTURE PER BASIN")
    print("=" * 70)

    # Build reverse adjacency (children → parent in the tree)
    children = defaultdict(list)
    for h in range(NUM_HEX):
        if h not in ATTRACTORS:
            children[edges[h]].append(h)

    for aset in ATTRACTOR_SETS:
        basin_name = BASIN_NAMES[aset]
        basin_nodes = [h for h in range(NUM_HEX) if basins[h] == aset]
        basin_nodes.sort()

        print(f"\n{'─' * 60}")
        print(f"Basin: {basin_name} ({len(basin_nodes)} hexagrams)")
        print(f"{'─' * 60}")

        # Depth distribution within basin
        depth_groups = defaultdict(list)
        for h in basin_nodes:
            depth_groups[depth[h]].append(h)

        for d in sorted(depth_groups):
            nodes = depth_groups[d]
            print(f"  Depth {d}: {len(nodes)} nodes")

        # Draw the tree
        if len(aset) == 1:
            # Fixed point — single root
            root = list(aset)[0]
            _print_subtree(root, children, depth=0, prefix="")
        else:
            # 2-cycle — draw both roots with cross-link
            roots = sorted(aset)
            print(f"\n  {kw_label(roots[0])} ←→ {kw_label(roots[1])}  [2-cycle]")
            for root in roots:
                _print_subtree(root, children, depth=0, prefix="  ")

        # Shape analysis
        max_d = max(depth[h] for h in basin_nodes)
        branching = {}
        for d in range(max_d + 1):
            parents = [h for h in basin_nodes if depth[h] == d and children[h]]
            if parents:
                factors = [len(children[p]) for p in parents]
                branching[d] = factors

        print(f"\n  Shape: max_depth={max_d}")
        for d, factors in sorted(branching.items()):
            print(f"    Depth {d} branching: {factors} (mean={sum(factors)/len(factors):.1f})")


def _print_subtree(node, children, depth, prefix):
    """Recursively print tree."""
    kw_num, name = KW[node]
    marker = " ★" if node in ATTRACTORS else ""
    lo = lower_trigram(node)
    up = upper_trigram(node)
    trig_label = f"{TRIGRAM_NAMES[lo].split()[0]}/{TRIGRAM_NAMES[up].split()[0]}"
    print(f"{prefix}{'└── ' if depth > 0 else ''}{node:2d} KW#{kw_num:2d} {name:12s} ({fmt6(node)}) [{trig_label}]{marker}")

    kids = sorted(children.get(node, []))
    for i, child in enumerate(kids):
        new_prefix = prefix + ("    " if depth > 0 else "  ")
        _print_subtree(child, children, depth + 1, new_prefix)


def print_fiber_structure(edges):
    """Group 64 hexagrams by hugua value (4-to-1 fibers)."""
    print("\n" + "=" * 70)
    print("FIBER STRUCTURE (4-to-1 by outer bits)")
    print("=" * 70)

    # Group by inner value
    inner_groups = defaultdict(list)
    for h in range(NUM_HEX):
        inner_groups[inner(h)].append(h)

    print(f"\n{'inner':>5} {'bits1-4':>7} → {'hugua':>5} {'hu_bin':>8} {'KW#':>4} | {'fiber members (varying bits 0,5)'}")
    print("-" * 90)

    for v in range(16):
        fiber = sorted(inner_groups[v])
        hu = hugua(fiber[0])  # all have same hugua
        kw_num, name = KW[hu]

        # Verify: all fiber members map to same hugua
        assert all(hugua(h) == hu for h in fiber), f"Fiber {v} inconsistent"

        # Show outer bit pattern
        outer_patterns = [(bit(h, 0), bit(h, 5)) for h in fiber]
        fiber_labels = [f"{h}({fmt6(h)})" for h in fiber]

        print(f"{v:5d} {format(v, '04b'):>7} → {hu:5d} {fmt6(hu):>8} {kw_num:4d} | {', '.join(fiber_labels)}")

    # Verify grouping is by outer bits
    print("\n  Verification: within each fiber, inner bits are identical,")
    print("  outer bits (0,5) take all 4 combinations (00,01,10,11).")
    all_ok = True
    for v in range(16):
        fiber = sorted(inner_groups[v])
        outers = sorted([(bit(h, 0), bit(h, 5)) for h in fiber])
        expected = [(0, 0), (0, 1), (1, 0), (1, 1)]
        if outers != expected:
            print(f"  MISMATCH at inner={v}: {outers}")
            all_ok = False
    print(f"  Result: {'✓ All fibers have exactly the 4 outer-bit combinations' if all_ok else '✗ MISMATCH'}")


# ═══════════════════════════════════════════════════════════════════════
# Visualization
# ═══════════════════════════════════════════════════════════════════════

def make_visualization(edges, depth, basins, in_deg, outdir):
    """NetworkX graph with hierarchical layout per basin."""
    G = nx.DiGraph()
    for h in range(NUM_HEX):
        G.add_node(h)
        G.add_edge(h, edges[h])

    # Layout: position nodes by basin (x) and depth (y)
    # Basin x-centers: Kun=0, Cycle=5, Qian=10
    basin_x = {
        frozenset({0}): 0,
        frozenset({21, 42}): 5.5,
        frozenset({63}): 11,
    }

    pos = {}
    for aset in ATTRACTOR_SETS:
        bname = BASIN_NAMES[aset]
        cx = basin_x[aset]
        bnodes = sorted([h for h in range(NUM_HEX) if basins[h] == aset])

        # Group by depth
        by_depth = defaultdict(list)
        for h in bnodes:
            by_depth[depth[h]].append(h)

        for d, nodes in by_depth.items():
            nodes.sort()
            n = len(nodes)
            # Spread horizontally, centered on cx
            width = min(n * 0.45, 4.0)
            for i, h in enumerate(nodes):
                x = cx - width / 2 + (i / max(n - 1, 1)) * width if n > 1 else cx
                y = -d * 2.0  # depth goes downward
                pos[h] = (x, y)

    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    ax.set_title("Hugua Functional Graph \u2014 64 Hexagrams", fontsize=16, fontweight='bold')

    # Draw edges
    # Separate self-loops, cycle edges, and tree edges
    tree_edges = []
    cycle_edges = []
    for h in range(NUM_HEX):
        target = edges[h]
        if h == target:
            continue  # self-loop handled separately
        elif target in ATTRACTORS and h in ATTRACTORS:
            cycle_edges.append((h, target))
        else:
            tree_edges.append((h, target))

    nx.draw_networkx_edges(G, pos, edgelist=tree_edges, ax=ax,
                           edge_color='#888888', alpha=0.4, arrows=True,
                           arrowsize=8, width=0.6,
                           connectionstyle="arc3,rad=0.05")

    nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, ax=ax,
                           edge_color='#ff6600', alpha=0.8, arrows=True,
                           arrowsize=12, width=2.0,
                           connectionstyle="arc3,rad=0.15")

    # Draw self-loops as circles
    for h in range(NUM_HEX):
        if edges[h] == h:
            x, y = pos[h]
            circle = plt.Circle((x, y + 0.35), 0.25, fill=False,
                                edgecolor='#ff6600', linewidth=2, alpha=0.8)
            ax.add_patch(circle)

    # Node colors and sizes
    node_colors = []
    node_sizes = []
    node_edgecolors = []
    for h in range(NUM_HEX):
        bname = BASIN_NAMES[basins[h]]
        node_colors.append(BASIN_COLORS[bname])
        # Size by in-degree
        base = 80
        node_sizes.append(base + in_deg[h] * 40)
        # Attractor border
        if h in ATTRACTORS:
            node_edgecolors.append('#ff6600')
        else:
            node_edgecolors.append('#333333')

    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_color=node_colors,
                           node_size=node_sizes,
                           edgecolors=node_edgecolors,
                           linewidths=[2.5 if h in ATTRACTORS else 0.5 for h in range(NUM_HEX)],
                           alpha=0.85)

    # Labels: KW number
    labels = {h: str(KW[h][0]) for h in range(NUM_HEX)}
    nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=6, font_weight='bold')

    # Legend
    legend_patches = [
        mpatches.Patch(color=BASIN_COLORS["Kun ☷"], label="Kun ☷ basin (16)"),
        mpatches.Patch(color=BASIN_COLORS["JiJi↔WeiJi ☵☲"], label="JiJi↔WeiJi ☵☲ basin (32)"),
        mpatches.Patch(color=BASIN_COLORS["Qian ☰"], label="Qian ☰ basin (16)"),
        mpatches.Patch(facecolor='none', edgecolor='#ff6600', linewidth=2, label="Attractor"),
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9)

    # Depth labels on left
    for d in range(3):
        ax.text(-2.5, -d * 2.0, f"depth {d}", fontsize=10, ha='center', va='center',
                fontweight='bold', color='#666666')

    ax.set_xlim(-3.5, 13)
    ax.axis('off')
    plt.tight_layout()

    for ext in ('png', 'svg'):
        path = f"{outdir}/01_functional_graph.{ext}"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Key Findings
# ═══════════════════════════════════════════════════════════════════════

def print_key_findings(edges, depth, basins, in_deg):
    """Structured summary."""
    print("\n" + "=" * 70)
    print("## Key Findings")
    print("=" * 70)

    # 1. Depth distribution
    from collections import Counter
    depth_counts = Counter(depth.values())
    print(f"\n1. DEPTH DISTRIBUTION: {dict(sorted(depth_counts.items()))}")
    print(f"   Attractors (depth 0): 4  —  {0}=Kun, {63}=Qian, {21}↔{42} (JiJi↔WeiJi)")
    print(f"   Depth 1: {depth_counts[1]}  —  map directly to an attractor")
    print(f"   Depth 2: {depth_counts[2]}  —  map to a depth-1 node")

    # 2. Tree shape
    children = defaultdict(list)
    for h in range(NUM_HEX):
        if h not in ATTRACTORS:
            children[edges[h]].append(h)

    print(f"\n2. TREE SHAPE")
    for aset in ATTRACTOR_SETS:
        bname = BASIN_NAMES[aset]
        bnodes = [h for h in range(NUM_HEX) if basins[h] == aset]
        n = len(bnodes)

        # Count at each depth
        d_counts = Counter(depth[h] for h in bnodes)
        attractors_in_basin = [h for h in bnodes if h in ATTRACTORS]

        branching_d0 = [len(children[a]) for a in attractors_in_basin]
        d1_nodes = [h for h in bnodes if depth[h] == 1]
        branching_d1 = [len(children[h]) for h in d1_nodes if children[h]]

        shape = "balanced" if len(set(branching_d1)) <= 1 else "irregular"

        print(f"   {bname} ({n} nodes): depths={dict(sorted(d_counts.items()))}")
        print(f"     Attractor branching: {branching_d0}")
        print(f"     Depth-1 branching: {sorted(branching_d1) if branching_d1 else 'none (all leaves)'}")
        print(f"     Shape: {shape}")

    # 3. In-degree
    in_vals = sorted(set(in_deg.values()))
    print(f"\n3. IN-DEGREE")
    print(f"   Possible values: {in_vals}")
    for v in in_vals:
        nodes = [h for h in range(NUM_HEX) if in_deg[h] == v]
        print(f"   In-degree {v}: {len(nodes)} nodes")
    max_indeg = max(in_deg.values())
    max_nodes = [h for h in range(NUM_HEX) if in_deg[h] == max_indeg]
    print(f"   Max in-degree {max_indeg} at: {[kw_label(h) for h in max_nodes]}")

    # 4. Fiber regularity
    print(f"\n4. FIBER STRUCTURE")
    print(f"   Exactly 4-to-1: each of 16 hugua outputs receives exactly 4 hexagrams")
    print(f"   Outer bits (0,5) are erased: fibers are parameterized by (bit0, bit5)")
    print(f"   48 hexagrams are never targets (in-degree 0) = depth-2 leaves")
    print(f"   16 hexagrams are hugua outputs: 4 attractors + 12 depth-1 intermediates")

    # 5. Basin sizes and symmetry
    print(f"\n5. BASIN SIZES")
    for aset in ATTRACTOR_SETS:
        bname = BASIN_NAMES[aset]
        n = sum(1 for h in range(NUM_HEX) if basins[h] == aset)
        print(f"   {bname}: {n} hexagrams")
    print(f"   Cycle basin is 2× each fixed-point basin (32 vs 16)")
    print(f"   Basin determined by (bit2, bit3): (0,0)→Kun, (1,1)→Qian, mixed→Cycle")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import os
    outdir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("01: FULL 64-NODE 互 FUNCTIONAL GRAPH")
    print("=" * 70)

    # Build graph
    edges = build_graph()

    # Compute basins
    basins = {h: find_basin(h, edges) for h in range(NUM_HEX)}

    # Compute depths (proper BFS)
    depth = compute_depths(edges)

    # In-degree
    in_deg = defaultdict(int)
    for h in range(NUM_HEX):
        in_deg[edges[h]] += 1

    # Print analyses
    print_edge_table(edges, depth, basins)
    in_deg = print_indegree(edges)
    print_tree_structure(edges, depth, basins)
    print_fiber_structure(edges)

    # Visualization
    print("\nGenerating visualization...")
    make_visualization(edges, depth, basins, in_deg, outdir)

    # Key findings
    print_key_findings(edges, depth, basins, in_deg)


if __name__ == '__main__':
    main()
