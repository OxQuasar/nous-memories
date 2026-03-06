#!/usr/bin/env python3
"""
03_inner_orbits.py — Inner 16-node orbit structure.

Project to inner 4 bits (bits 1-4). The hugua map on inner space is
a 16→16 self-map. Analyze components, hypercube geometry, five-phase
relations along convergence edges.
"""

import sys
sys.path.insert(0, 'memories/iching/opposition-theory/phase4')
sys.path.insert(0, 'memories/iching/kingwen')

from collections import defaultdict
from cycle_algebra import (
    hugua, bit, fmt6, fmt3,
    TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENT_ZH,
    five_phase_relation, popcount,
)
from sequence import KING_WEN

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════

ATTRACTORS_FULL = frozenset({0, 21, 42, 63})

BASIN_COLORS = {
    "Kun": "#4488cc",
    "Qian": "#cc4444",
    "Cycle": "#44aa44",
}

def fmt4(x):
    return format(x, '04b')


# ═══════════════════════════════════════════════════════════════════════
# Inner Space Map
# ═══════════════════════════════════════════════════════════════════════

def inner(h):
    """Extract inner 4 bits (bits 1-4) from a 6-bit hexagram."""
    return (h >> 1) & 0xF

def inner_hugua(v):
    """
    Compute hugua on inner space: v → inner(hugua(x)) where inner(x)=v.

    Representative hexagram: x = v << 1 (bits 0,5 = 0).
    inner(hugua(x)) extracts bits 1-4 of hugua output.
    """
    x = v << 1  # representative with bit0=0, bit5=0
    return inner(hugua(x))

def lower_nuclear(v):
    """Lower nuclear trigram from inner value: bits 0-2 of v."""
    return v & 0b111

def upper_nuclear(v):
    """Upper nuclear trigram from inner value: bits 1-3 of v."""
    return (v >> 1) & 0b111

def basin_of_inner(v):
    """Basin from inner value, determined by bits 1,2 (= interface bits)."""
    i1 = (v >> 1) & 1  # bit(x,2) for the original hexagram
    i2 = (v >> 2) & 1  # bit(x,3) for the original hexagram
    if i1 == 0 and i2 == 0:
        return "Kun"
    elif i1 == 1 and i2 == 1:
        return "Qian"
    else:
        return "Cycle"


# ═══════════════════════════════════════════════════════════════════════
# Analysis
# ═══════════════════════════════════════════════════════════════════════

def build_inner_graph():
    """Build the 16→16 inner map."""
    return {v: inner_hugua(v) for v in range(16)}

def compute_inner_depths(edges):
    """BFS from inner attractors."""
    # Find attractors: nodes in cycles
    inner_attractors = set()
    for v in range(16):
        # Check if v is in a cycle
        seen = set()
        node = v
        while node not in seen:
            seen.add(node)
            node = edges[node]
        # node is in a cycle — trace it
        cycle = {node}
        cur = edges[node]
        while cur != node:
            cycle.add(cur)
            cur = edges[cur]
        if v in cycle:
            inner_attractors.add(v)

    depth = {a: 0 for a in inner_attractors}
    frontier = set(inner_attractors)
    d = 0
    while frontier:
        d += 1
        next_frontier = set()
        for v in range(16):
            if v not in depth and edges[v] in frontier:
                depth[v] = d
                next_frontier.add(v)
        frontier = next_frontier
    return depth, inner_attractors

def find_components(edges):
    """Find disconnected components in the functional graph."""
    visited = set()
    components = []

    # Build undirected adjacency
    adj = defaultdict(set)
    for v in range(16):
        adj[v].add(edges[v])
        adj[edges[v]].add(v)

    for start in range(16):
        if start in visited:
            continue
        component = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            component.add(node)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    stack.append(neighbor)
        components.append(sorted(component))

    return components


def print_edge_table(edges, depth, inner_attractors):
    """16→16 edge table with trigram decomposition."""
    print("\n" + "=" * 90)
    print("16-NODE INNER MAP: v → inner_hugua(v)")
    print("=" * 90)

    header = (f"{'v':>3} {'bits':>5} {'lo_nuc':>8} {'up_nuc':>8} "
              f"{'lo_elem':>8} {'up_elem':>8} → "
              f"{'hu':>3} {'hu_bits':>7} {'depth':>5} {'basin':>6}")
    print(header)
    print("-" * len(header))

    for v in range(16):
        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        lo_name = TRIGRAM_NAMES[lo].split()[0]
        up_name = TRIGRAM_NAMES[up].split()[0]
        lo_elem = TRIGRAM_ELEMENT[lo]
        up_elem = TRIGRAM_ELEMENT[up]
        hu = edges[v]
        d = depth[v]
        basin = basin_of_inner(v)
        attr = " ★" if v in inner_attractors else ""

        print(f"{v:3d} {fmt4(v):>5} {lo_name:>8} {up_name:>8} "
              f"{lo_elem:>8} {up_elem:>8} → "
              f"{hu:3d} {fmt4(hu):>7} {d:5d} {basin:>6}{attr}")

    # Show the overlap constraint
    print("\n  Note: lower_nuclear = bits 0-2, upper_nuclear = bits 1-3")
    print("  Overlap at bits 1,2: lower_nuc[1:2] = upper_nuc[0:1]")
    print("  This shared pair (bit1, bit2) = interface bits → determines basin")


def print_components(components, edges, depth, inner_attractors):
    """Component structure."""
    print("\n" + "=" * 70)
    print("COMPONENT STRUCTURE (3 disconnected components)")
    print("=" * 70)

    for i, comp in enumerate(components):
        # Determine basin
        basin = basin_of_inner(comp[0])
        comp_attractors = [v for v in comp if v in inner_attractors]

        print(f"\n{'─' * 50}")
        print(f"Component {i+1}: {basin} basin — {len(comp)} nodes")
        print(f"{'─' * 50}")
        print(f"  Attractor(s): {comp_attractors}")
        print(f"  Nodes: {comp}")

        # Depth assignment
        depth_groups = defaultdict(list)
        for v in comp:
            depth_groups[depth[v]].append(v)

        for d in sorted(depth_groups):
            nodes = depth_groups[d]
            labels = []
            for v in nodes:
                lo = lower_nuclear(v)
                up = upper_nuclear(v)
                lo_name = TRIGRAM_NAMES[lo].split()[0]
                up_name = TRIGRAM_NAMES[up].split()[0]
                labels.append(f"{v}({lo_name}/{up_name})")
            print(f"  Depth {d}: {', '.join(labels)}")

        # Feeder → attractor chains
        feeders = [v for v in comp if v not in inner_attractors]
        print(f"\n  Convergence chains:")
        for v in feeders:
            chain = [v]
            cur = edges[v]
            while cur not in chain:
                chain.append(cur)
                cur = edges[cur]
            chain_str = " → ".join(str(x) for x in chain)
            print(f"    {chain_str}")

        # Shape
        children = defaultdict(list)
        for v in comp:
            if v not in inner_attractors:
                children[edges[v]].append(v)

        print(f"\n  Tree shape:")
        for a in comp_attractors:
            kids = children.get(a, [])
            print(f"    Attractor {a}: {len(kids)} feeders → {kids}")
            for k in kids:
                grandkids = children.get(k, [])
                if grandkids:
                    print(f"      Feeder {k}: {len(grandkids)} sub-feeders → {grandkids}")


def print_hypercube_geometry(edges, depth, inner_attractors):
    """4-bit hypercube analysis: Hamming distances, patterns."""
    print("\n" + "=" * 70)
    print("4-BIT HYPERCUBE GEOMETRY")
    print("=" * 70)

    # Group by basin
    basins = defaultdict(list)
    for v in range(16):
        basins[basin_of_inner(v)].append(v)

    # For each basin: Hamming distances between feeders, and feeders→attractor
    for basin_name, nodes in sorted(basins.items()):
        attractors = [v for v in nodes if v in inner_attractors]
        feeders = [v for v in nodes if v not in inner_attractors]

        print(f"\n  {basin_name} basin:")
        print(f"    Attractors: {attractors}")
        print(f"    Feeders: {feeders}")

        if attractors and feeders:
            # Hamming distances: feeders to attractors
            print(f"\n    Feeder → Attractor Hamming distances:")
            for f in feeders:
                for a in attractors:
                    d = popcount(f ^ a)
                    print(f"      {f}({fmt4(f)}) → {a}({fmt4(a)}): Hamming={d}")

            # Hamming distances between feeders
            if len(feeders) > 1:
                print(f"\n    Inter-feeder Hamming distances:")
                for i in range(len(feeders)):
                    for j in range(i + 1, len(feeders)):
                        d = popcount(feeders[i] ^ feeders[j])
                        print(f"      {feeders[i]}({fmt4(feeders[i])}) ↔ "
                              f"{feeders[j]}({fmt4(feeders[j])}): Hamming={d}")

    # Check for bit-pattern regularity
    print(f"\n  Feeder bit patterns by basin:")
    for basin_name, nodes in sorted(basins.items()):
        feeders = [v for v in nodes if v not in inner_attractors]
        if feeders:
            bits_set = [fmt4(f) for f in feeders]
            # Which bits differ among feeders?
            if len(feeders) > 1:
                xor_all = 0
                for f in feeders:
                    xor_all |= f
                for f in feeders:
                    xor_all &= ~(~f & 0xF) | f  # This isn't right, let me just XOR pairs
                diff_bits = set()
                for i in range(len(feeders)):
                    for j in range(i + 1, len(feeders)):
                        diff = feeders[i] ^ feeders[j]
                        for b in range(4):
                            if diff & (1 << b):
                                diff_bits.add(b)
                print(f"    {basin_name}: {bits_set}, varying bits: {sorted(diff_bits)}")
            else:
                print(f"    {basin_name}: {bits_set}")


def print_five_phase(edges, depth, inner_attractors):
    """Five-phase overlay: element assignment and convergence relations."""
    print("\n" + "=" * 70)
    print("FIVE-PHASE OVERLAY")
    print("=" * 70)

    # Element assignment for each inner value
    print(f"\n{'v':>3} {'bits':>5} {'lo_nuc':>8} {'up_nuc':>8} "
          f"{'lo_elem':>8} {'up_elem':>8} {'basin':>6}")
    print("-" * 60)

    for v in range(16):
        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        lo_name = TRIGRAM_NAMES[lo].split()[0]
        up_name = TRIGRAM_NAMES[up].split()[0]
        lo_elem = TRIGRAM_ELEMENT[lo]
        up_elem = TRIGRAM_ELEMENT[up]
        basin = basin_of_inner(v)
        print(f"{v:3d} {fmt4(v):>5} {lo_name:>8} {up_name:>8} "
              f"{lo_elem:>8} {up_elem:>8} {basin:>6}")

    # Convergence edge five-phase relations
    print(f"\n{'─' * 60}")
    print("CONVERGENCE EDGE FIVE-PHASE RELATIONS")
    print(f"{'─' * 60}")
    print(f"\n{'v':>3} → {'hu':>3}  {'v_lo_e':>8} {'v_up_e':>8}  →  "
          f"{'hu_lo_e':>8} {'hu_up_e':>8}  {'lo_rel':>10} {'up_rel':>10}")
    print("-" * 85)

    relations_count = defaultdict(int)
    all_relations = []

    for v in range(16):
        hu = edges[v]
        if v == hu:
            continue  # skip self-loops
        if v in inner_attractors and hu in inner_attractors:
            pass  # cycle edge, still interesting

        v_lo = lower_nuclear(v)
        v_up = upper_nuclear(v)
        hu_lo = lower_nuclear(hu)
        hu_up = upper_nuclear(hu)

        v_lo_elem = TRIGRAM_ELEMENT[v_lo]
        v_up_elem = TRIGRAM_ELEMENT[v_up]
        hu_lo_elem = TRIGRAM_ELEMENT[hu_lo]
        hu_up_elem = TRIGRAM_ELEMENT[hu_up]

        # Five-phase relation: source trigram element → target trigram element
        lo_rel = five_phase_relation(hu_lo_elem, v_lo_elem)
        up_rel = five_phase_relation(hu_up_elem, v_up_elem)

        print(f"{v:3d} → {hu:3d}  {v_lo_elem:>8} {v_up_elem:>8}  →  "
              f"{hu_lo_elem:>8} {hu_up_elem:>8}  {lo_rel:>10} {up_rel:>10}")

        relations_count[(lo_rel, up_rel)] += 1
        all_relations.append((v, hu, lo_rel, up_rel))

    # Summary
    print(f"\n  Relation pair distribution:")
    for (lo_r, up_r), cnt in sorted(relations_count.items(), key=lambda x: -x[1]):
        print(f"    ({lo_r}, {up_r}): {cnt}")

    # Pattern check: is convergence uniformly 生, 克, or 比?
    lo_rels = defaultdict(int)
    up_rels = defaultdict(int)
    for _, _, lr, ur in all_relations:
        lo_rels[lr] += 1
        up_rels[ur] += 1

    print(f"\n  Lower nuclear relation distribution:")
    for r, c in sorted(lo_rels.items(), key=lambda x: -x[1]):
        print(f"    {r}: {c}")

    print(f"\n  Upper nuclear relation distribution:")
    for r, c in sorted(up_rels.items(), key=lambda x: -x[1]):
        print(f"    {r}: {c}")


# ═══════════════════════════════════════════════════════════════════════
# Visualization
# ═══════════════════════════════════════════════════════════════════════

def make_visualization(edges, depth, inner_attractors, outdir):
    """16-node graph on 4-bit hypercube layout."""
    G = nx.DiGraph()
    for v in range(16):
        G.add_node(v)
        G.add_edge(v, edges[v])

    # Hypercube layout: map 4 bits to 2D
    # Use bit pairs: (bit0, bit1) → x, (bit2, bit3) → y
    # With slight offsets to separate inner/outer squares
    pos = {}
    for v in range(16):
        b0 = v & 1
        b1 = (v >> 1) & 1
        b2 = (v >> 2) & 1
        b3 = (v >> 3) & 1
        # Outer position from bits 1,2 (interface bits → basin)
        # Inner position from bits 0,3 (free bits)
        x = b1 * 4 + b0 * 1.2
        y = b2 * 4 + b3 * 1.2
        pos[v] = (x, y)

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_title("Inner 16-Node Orbit Structure (Hypercube Layout)", fontsize=14, fontweight='bold')

    # Draw hypercube edges (Hamming distance 1) as thin gray lines
    hypercube_edges = []
    for v in range(16):
        for b in range(4):
            neighbor = v ^ (1 << b)
            if neighbor > v:
                hypercube_edges.append((v, neighbor))

    for u, w in hypercube_edges:
        x0, y0 = pos[u]
        x1, y1 = pos[w]
        ax.plot([x0, x1], [y0, y1], color='#dddddd', linewidth=0.8, zorder=1)

    # Classify convergence edges
    self_loops = []
    cycle_edges = []
    tree_edges = []
    for v in range(16):
        target = edges[v]
        if v == target:
            self_loops.append(v)
        elif v in inner_attractors and target in inner_attractors:
            cycle_edges.append((v, target))
        else:
            tree_edges.append((v, target))

    # Draw convergence edges
    nx.draw_networkx_edges(G, pos, edgelist=tree_edges, ax=ax,
                           edge_color='#555555', alpha=0.7, arrows=True,
                           arrowsize=15, width=1.5, arrowstyle='-|>',
                           connectionstyle="arc3,rad=0.08")

    nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, ax=ax,
                           edge_color='#ff6600', alpha=0.9, arrows=True,
                           arrowsize=18, width=2.5, arrowstyle='-|>',
                           connectionstyle="arc3,rad=0.15")

    # Self-loops
    for v in self_loops:
        x, y = pos[v]
        circle = plt.Circle((x, y + 0.45), 0.3, fill=False,
                             edgecolor='#ff6600', linewidth=2.5, alpha=0.9)
        ax.add_patch(circle)

    # Node styling
    for v in range(16):
        basin = basin_of_inner(v)
        color = BASIN_COLORS[basin]
        is_attr = v in inner_attractors

        size = 700 if is_attr else 500
        edge_color = '#ff6600' if is_attr else '#333333'
        edge_width = 3.0 if is_attr else 1.0

        x, y = pos[v]
        circle = plt.Circle((x, y), 0.35 if is_attr else 0.28,
                             facecolor=color, edgecolor=edge_color,
                             linewidth=edge_width, alpha=0.85, zorder=5)
        ax.add_patch(circle)

        # Label: inner value + trigram pair
        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        lo_name = TRIGRAM_NAMES[lo].split()[0][:3]
        up_name = TRIGRAM_NAMES[up].split()[0][:3]
        label = f"{v}\n{lo_name}/{up_name}"
        ax.text(x, y, label, ha='center', va='center', fontsize=7,
                fontweight='bold', zorder=6)

        # Element labels below (English abbreviations to avoid CJK font issues)
        lo_elem = TRIGRAM_ELEMENT[lo]
        up_elem = TRIGRAM_ELEMENT[up]
        ELEM_ABBR = {"Wood": "Wd", "Fire": "Fi", "Earth": "Ea", "Metal": "Me", "Water": "Wa"}
        elem_label = f"{ELEM_ABBR[lo_elem]}/{ELEM_ABBR[up_elem]}"
        ax.text(x, y - 0.5, elem_label, ha='center', va='top', fontsize=7,
                color='#666666', zorder=6)

    # Axis labels showing bit meaning
    ax.text(-0.8, -0.5, "bit1=0\nbit2=0", fontsize=8, color='#888', ha='center')
    ax.text(4 - 0.8, -0.5, "bit1=1\nbit2=0", fontsize=8, color='#888', ha='center')
    ax.text(-0.8, 4 - 0.5, "bit1=0\nbit2=1", fontsize=8, color='#888', ha='center')
    ax.text(4 - 0.8, 4 - 0.5, "bit1=1\nbit2=1", fontsize=8, color='#888', ha='center')

    # Basin region labels
    ax.text(0.6, -1.0, "Kun Basin", fontsize=11, color=BASIN_COLORS["Kun"],
            fontweight='bold', ha='center')
    ax.text(4.6, -1.0, "Cycle Basin (L)", fontsize=11, color=BASIN_COLORS["Cycle"],
            fontweight='bold', ha='center')
    ax.text(0.6, 5.8, "Cycle Basin (R)", fontsize=11, color=BASIN_COLORS["Cycle"],
            fontweight='bold', ha='center')
    ax.text(4.6, 5.8, "Qian Basin", fontsize=11, color=BASIN_COLORS["Qian"],
            fontweight='bold', ha='center')

    # Legend
    legend_patches = [
        mpatches.Patch(color=BASIN_COLORS["Kun"], label="Kun basin (4 nodes)"),
        mpatches.Patch(color=BASIN_COLORS["Cycle"], label="Cycle basin (8 nodes)"),
        mpatches.Patch(color=BASIN_COLORS["Qian"], label="Qian basin (4 nodes)"),
        mpatches.Patch(facecolor='none', edgecolor='#ff6600', linewidth=2,
                       label="Attractor"),
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9)

    ax.set_xlim(-1.5, 6.5)
    ax.set_ylim(-1.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()

    for ext in ('png', 'svg'):
        path = f"{outdir}/03_inner_orbits.{ext}"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Key Findings
# ═══════════════════════════════════════════════════════════════════════

def print_key_findings(edges, depth, inner_attractors):
    """Structured summary."""
    print("\n" + "=" * 70)
    print("## Key Findings")
    print("=" * 70)

    # 1. Component structure
    print(f"\n1. COMPONENT STRUCTURE")
    print(f"   3 disconnected components matching the 3 basins: Kun(4), Cycle(8), Qian(4)")
    print(f"   Inner attractors: {sorted(inner_attractors)}")
    print(f"     Fixed points: 0 (Kun), 15 (Qian)")
    print(f"     2-cycle: 5 ↔ 10 (JiJi ↔ WeiJi)")

    # 2. Tree balance
    children = defaultdict(list)
    for v in range(16):
        if v not in inner_attractors:
            children[edges[v]].append(v)

    print(f"\n2. TREE BALANCE")
    for basin_name in ["Kun", "Cycle", "Qian"]:
        nodes = [v for v in range(16) if basin_of_inner(v) == basin_name]
        attrs = [v for v in nodes if v in inner_attractors]
        feeds = [v for v in nodes if v not in inner_attractors]
        print(f"   {basin_name}: {len(attrs)} attractor(s), {len(feeds)} feeders")
        for a in attrs:
            kids = children.get(a, [])
            print(f"     Attractor {a} ← feeders {kids}")

    # 3. Hypercube pattern
    print(f"\n3. HYPERCUBE FEEDER GEOMETRY")
    for basin_name in ["Kun", "Cycle", "Qian"]:
        nodes = [v for v in range(16) if basin_of_inner(v) == basin_name]
        attrs = [v for v in nodes if v in inner_attractors]
        feeds = [v for v in nodes if v not in inner_attractors]
        if feeds:
            # Check: do feeders form a coset or regular pattern?
            feed_bits = [fmt4(f) for f in feeds]
            # XOR of all feeder pairs
            xors = set()
            for i in range(len(feeds)):
                for j in range(i + 1, len(feeds)):
                    xors.add(feeds[i] ^ feeds[j])
            print(f"   {basin_name} feeders: {feeds} (bits: {feed_bits})")
            print(f"     Pairwise XOR masks: {[fmt4(x) for x in sorted(xors)]}")
            # Hamming to attractor
            for a in attrs:
                dists = [popcount(f ^ a) for f in feeds]
                print(f"     Hamming to attractor {a}: {dists}")

    # 4. Inner map is a radical contraction
    print(f"\n4. CONTRACTION PROPERTIES")
    print(f"   Inner map: (i0,i1,i2,i3) → (i1,i2,i1,i2)")
    print(f"   Only 4 output values possible: 0, 5, 10, 15")
    print(f"   4-to-1 collapse in ONE step (16 → 4 distinct values)")
    print(f"   Second step: 4 → 2 or fixed (attractors)")
    print(f"   Maximum depth on inner space: {max(depth.values())}")

    # 5. Five-phase
    print(f"\n5. FIVE-PHASE PATTERN")
    # Compute relations along edges
    relations = defaultdict(int)
    for v in range(16):
        hu = edges[v]
        if v == hu:
            continue
        v_lo_e = TRIGRAM_ELEMENT[lower_nuclear(v)]
        v_up_e = TRIGRAM_ELEMENT[upper_nuclear(v)]
        hu_lo_e = TRIGRAM_ELEMENT[lower_nuclear(hu)]
        hu_up_e = TRIGRAM_ELEMENT[upper_nuclear(hu)]
        lo_r = five_phase_relation(hu_lo_e, v_lo_e)
        up_r = five_phase_relation(hu_up_e, v_up_e)
        relations[lo_r] += 1
        relations[up_r] += 1

    total = sum(relations.values())
    print(f"   All convergence-edge trigram relations (both lo and up):")
    for r, c in sorted(relations.items(), key=lambda x: -x[1]):
        print(f"     {r}: {c}/{total} ({100*c/total:.0f}%)")

    dominant = max(relations, key=relations.get)
    if relations[dominant] > total * 0.5:
        print(f"   → Dominant pattern: {dominant}")
    else:
        print(f"   → Mixed pattern — no single dominant relation")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import os
    outdir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("03: INNER 16-NODE ORBIT STRUCTURE")
    print("=" * 70)

    # Build inner graph
    edges = build_inner_graph()
    depth, inner_attractors = compute_inner_depths(edges)
    components = find_components(edges)

    # Print analyses
    print_edge_table(edges, depth, inner_attractors)
    print_components(components, edges, depth, inner_attractors)
    print_hypercube_geometry(edges, depth, inner_attractors)
    print_five_phase(edges, depth, inner_attractors)

    # Visualization
    print("\nGenerating visualization...")
    make_visualization(edges, depth, inner_attractors, outdir)

    # Key findings
    print_key_findings(edges, depth, inner_attractors)


if __name__ == '__main__':
    main()
