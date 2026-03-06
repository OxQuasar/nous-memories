#!/usr/bin/env python3
"""
05_kw_depth_walk.py — Convergence depth along the King Wen sequence.

Depth labeling, clustering, basin interaction, pair depth, visualization.
"""

import sys
sys.path.insert(0, 'memories/iching/opposition-theory/phase4')
sys.path.insert(0, 'memories/iching/kingwen')

from collections import defaultdict, Counter
from cycle_algebra import (
    hugua, bit, fmt6, reverse6, kw_partner, is_palindrome6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES, TRIGRAM_ELEMENT,
    MASK_ALL,
)
from sequence import KING_WEN

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# Lookups & Depth Computation
# ═══════════════════════════════════════════════════════════════════════

NUM_HEX = 64
ATTRACTORS = frozenset({0, 21, 42, 63})
ATTRACTOR_SETS = [frozenset({0}), frozenset({63}), frozenset({21, 42})]

# KW sequence as (position, binary_value) — position 1-indexed
KW_SEQ = []
KW = {}
for kw_num, name, binstr in KING_WEN:
    val = sum(int(c) << i for i, c in enumerate(binstr))
    KW_SEQ.append((kw_num, val, name))
    KW[val] = (kw_num, name)

def compute_depths():
    """BFS from attractors — proper level-by-level."""
    edges = {h: hugua(h) for h in range(NUM_HEX)}
    depth = {a: 0 for a in ATTRACTORS}
    frontier = set(ATTRACTORS)
    d = 0
    while frontier:
        d += 1
        nxt = set()
        for h in range(NUM_HEX):
            if h not in depth and edges[h] in frontier:
                depth[h] = d
                nxt.add(h)
        frontier = nxt
    return depth

def basin_of(h):
    b2, b3 = bit(h, 2), bit(h, 3)
    if b2 == 0 and b3 == 0: return "Kun"
    if b2 == 1 and b3 == 1: return "Qian"
    return "Cycle"

BASIN_COLORS_PLOT = {"Kun": "#4488cc", "Qian": "#cc4444", "Cycle": "#44aa44"}

DEPTH = compute_depths()


# ═══════════════════════════════════════════════════════════════════════
# Part 1: Depth Labeling
# ═══════════════════════════════════════════════════════════════════════

def section_depth_labeling():
    print("=" * 80)
    print("PART 1: DEPTH LABELING — FULL KW SEQUENCE")
    print("=" * 80)

    print(f"\n{'pos':>4} {'KW#':>4} {'name':>12} {'bin':>7} {'depth':>5} {'basin':>6}")
    print("-" * 50)

    depth_seq = []
    for kw_num, val, name in KW_SEQ:
        d = DEPTH[val]
        b = basin_of(val)
        depth_seq.append(d)
        marker = " ★" if val in ATTRACTORS else ""
        print(f"{kw_num:4d} {kw_num:4d} {name:>12} {fmt6(val):>7} {d:5d} {b:>6}{marker}")

    # Summary
    dc = Counter(depth_seq)
    print(f"\n  Depth counts: {dict(sorted(dc.items()))}")
    print(f"  Depth-0 positions: {[i+1 for i, d in enumerate(depth_seq) if d == 0]}")
    print(f"  Depth-1 positions: {[i+1 for i, d in enumerate(depth_seq) if d == 1]}")

    # Compact depth string
    depth_str = ''.join(str(d) for d in depth_seq)
    print(f"\n  Depth sequence (positions 1-64):")
    for start in range(0, 64, 32):
        chunk = depth_str[start:start+32]
        positions = ''.join(f'{(start+i+1):>2}'[-1] for i in range(len(chunk)))
        print(f"    pos {start+1:2d}-{min(start+32,64):2d}: {chunk}")

    return depth_seq


# ═══════════════════════════════════════════════════════════════════════
# Part 2: Depth Clustering
# ═══════════════════════════════════════════════════════════════════════

def section_depth_clustering(depth_seq):
    print("\n" + "=" * 80)
    print("PART 2: DEPTH CLUSTERING")
    print("=" * 80)

    n = len(depth_seq)

    # Run-length analysis
    print(f"\n  Run-length analysis (consecutive same-depth):")
    runs = []
    cur_depth = depth_seq[0]
    cur_len = 1
    for i in range(1, n):
        if depth_seq[i] == cur_depth:
            cur_len += 1
        else:
            runs.append((cur_depth, cur_len))
            cur_depth = depth_seq[i]
            cur_len = 1
    runs.append((cur_depth, cur_len))

    print(f"  Total runs: {len(runs)}")
    for d in range(3):
        d_runs = [r for depth, r in runs if depth == d]
        if d_runs:
            print(f"    Depth {d}: {len(d_runs)} runs, lengths {sorted(d_runs, reverse=True)}")

    # Gap analysis for depth-1
    d1_positions = [i + 1 for i, d in enumerate(depth_seq) if d == 1]
    print(f"\n  Depth-1 positions ({len(d1_positions)} total): {d1_positions}")

    if len(d1_positions) > 1:
        gaps = [d1_positions[i+1] - d1_positions[i] for i in range(len(d1_positions) - 1)]
        print(f"  Gaps between consecutive depth-1: {gaps}")
        print(f"  Max gap: {max(gaps)} (between positions {d1_positions[gaps.index(max(gaps))]} and {d1_positions[gaps.index(max(gaps))+1]})")
        print(f"  Min gap: {min(gaps)}")
        print(f"  Mean gap: {sum(gaps)/len(gaps):.1f}")

    # Depth-1-free zones
    print(f"\n  Depth-1-free zones (contiguous stretches without depth 1):")
    in_zone = True
    zone_start = 1
    zones = []
    for pos in range(1, n + 1):
        is_d1 = depth_seq[pos - 1] == 1
        if is_d1 and in_zone:
            if pos > zone_start:
                zones.append((zone_start, pos - 1, pos - zone_start))
            in_zone = False
        elif not is_d1 and not in_zone:
            in_zone = True
            zone_start = pos
        elif is_d1:
            in_zone = False
    if in_zone and zone_start <= n:
        zones.append((zone_start, n, n - zone_start + 1))

    zones.sort(key=lambda x: -x[2])
    for start, end, length in zones[:10]:
        print(f"    Positions {start}-{end}: length {length}")


# ═══════════════════════════════════════════════════════════════════════
# Part 3: Depth × Basin Interaction
# ═══════════════════════════════════════════════════════════════════════

def section_depth_basin(depth_seq):
    print("\n" + "=" * 80)
    print("PART 3: DEPTH × BASIN INTERACTION")
    print("=" * 80)

    # Cross-tabulation
    cross = defaultdict(int)
    basins = []
    for kw_num, val, name in KW_SEQ:
        d = DEPTH[val]
        b = basin_of(val)
        cross[(d, b)] += 1
        basins.append(b)

    print(f"\n  {'':>8} {'Kun':>6} {'Cycle':>6} {'Qian':>6} {'Total':>6}")
    print(f"  {'─'*8} {'─'*6} {'─'*6} {'─'*6} {'─'*6}")
    for d in range(3):
        row = f"  depth {d}:"
        total = 0
        for b in ["Kun", "Cycle", "Qian"]:
            c = cross[(d, b)]
            row += f" {c:6d}"
            total += c
        row += f" {total:6d}"
        print(row)

    # Basin transitions
    print(f"\n  Basin transition analysis:")
    transitions = 0
    d1_at_boundary = 0
    total_boundaries = 0
    for i in range(len(basins) - 1):
        if basins[i] != basins[i + 1]:
            transitions += 1
            total_boundaries += 1
            d_left = depth_seq[i]
            d_right = depth_seq[i + 1]
            has_d1 = d_left == 1 or d_right == 1
            if has_d1:
                d1_at_boundary += 1
            left_name = KW_SEQ[i][2]
            right_name = KW_SEQ[i+1][2]
            print(f"    pos {i+1}-{i+2}: {basins[i]}→{basins[i+1]}"
                  f" (depth {d_left},{d_right})"
                  f" {left_name}→{right_name}"
                  f" {'← d1 at boundary' if has_d1 else ''}")

    print(f"\n  Total basin transitions: {transitions}")
    print(f"  Transitions with depth-1 at boundary: {d1_at_boundary}/{transitions}"
          f" ({100*d1_at_boundary/transitions:.0f}%)" if transitions > 0 else "")


# ═══════════════════════════════════════════════════════════════════════
# Part 4: Depth Within Pairs
# ═══════════════════════════════════════════════════════════════════════

def section_depth_pairs():
    print("\n" + "=" * 80)
    print("PART 4: DEPTH WITHIN KW PAIRS")
    print("=" * 80)

    paired = set()
    pairs = []
    for kw_num, val, name in KW_SEQ:
        if val in paired:
            continue
        partner = kw_partner(val)
        ptype = "complement" if is_palindrome6(val) else "reversal"
        pairs.append((val, partner, ptype))
        paired.add(val)
        paired.add(partner)

    # Verify same depth
    all_same = True
    for a, b, ptype in pairs:
        if DEPTH[a] != DEPTH[b]:
            print(f"  MISMATCH: {a}({KW[a][1]}) depth={DEPTH[a]}, {b}({KW[b][1]}) depth={DEPTH[b]}")
            all_same = False

    print(f"\n  All KW pairs share same depth: {'✓ YES' if all_same else '✗ NO'}")

    # Algebraic reason
    print(f"  Reason: inner bits under reversal: (i₀,i₁,i₂,i₃)→(i₃,i₂,i₁,i₀)")
    print(f"  Attractor inners {{0,5,10,15}} are closed under 4-bit reversal ✓")
    print(f"  Under complement: inner→inner⊕15, also closed ✓")

    # Show depth-1 pairs
    d1_pairs = [(a, b, pt) for a, b, pt in pairs if DEPTH[a] == 1]
    print(f"\n  Depth-1 pairs ({len(d1_pairs)} pairs, {len(d1_pairs)*2} hexagrams):")

    print(f"\n  {'a':>3} {'KW_a':>16} {'basin_a':>7} {'b':>3} {'KW_b':>16} {'basin_b':>7} {'type':>10}")
    print(f"  {'─'*3} {'─'*16} {'─'*7} {'─'*3} {'─'*16} {'─'*7} {'─'*10}")
    for a, b, pt in d1_pairs:
        kw_a = f"KW#{KW[a][0]}({KW[a][1]})"
        kw_b = f"KW#{KW[b][0]}({KW[b][1]})"
        print(f"  {a:3d} {kw_a:>16} {basin_of(a):>7}"
              f" {b:3d} {kw_b:>16} {basin_of(b):>7} {pt:>10}")

    # Depth-0 pairs
    d0_pairs = [(a, b, pt) for a, b, pt in pairs if DEPTH[a] == 0]
    print(f"\n  Depth-0 pairs ({len(d0_pairs)} pairs):")
    for a, b, pt in d0_pairs:
        print(f"    {a}({KW[a][1]}) ↔ {b}({KW[b][1]}) [{pt}]")


# ═══════════════════════════════════════════════════════════════════════
# Part 5: Visualization
# ═══════════════════════════════════════════════════════════════════════

def section_visualization(depth_seq, outdir):
    print("\n  Generating visualization...")

    n = len(depth_seq)
    positions = np.arange(1, n + 1)

    fig, ax = plt.subplots(1, 1, figsize=(18, 5))
    ax.set_title("Convergence Depth Along King Wen Sequence", fontsize=14, fontweight='bold')

    # Color by basin
    colors = []
    for kw_num, val, name in KW_SEQ:
        colors.append(BASIN_COLORS_PLOT[basin_of(val)])

    ax.bar(positions, depth_seq, color=colors, width=0.8, edgecolor='none', alpha=0.8)

    # Mark attractors
    for i, (kw_num, val, name) in enumerate(KW_SEQ):
        if val in ATTRACTORS:
            ax.plot(i + 1, depth_seq[i], 'k*', markersize=12, zorder=5)

    # Mark depth-1 positions
    for i, d in enumerate(depth_seq):
        if d == 1:
            ax.plot(i + 1, 1, 'o', color='white', markersize=4, zorder=4,
                    markeredgecolor='black', markeredgewidth=0.5)

    # Basin transition lines
    basins = [basin_of(val) for _, val, _ in KW_SEQ]
    for i in range(len(basins) - 1):
        if basins[i] != basins[i + 1]:
            ax.axvline(i + 1.5, color='black', linewidth=0.8, linestyle='--', alpha=0.5)

    ax.set_xlabel("KW Position", fontsize=11)
    ax.set_ylabel("Convergence Depth", fontsize=11)
    ax.set_xlim(0.5, 64.5)
    ax.set_ylim(-0.1, 2.5)
    ax.set_yticks([0, 1, 2])

    # X-axis: show KW numbers
    ax.set_xticks(positions[::4])
    ax.tick_params(axis='x', labelsize=7)

    # Legend
    import matplotlib.patches as mpatches
    legend_patches = [
        mpatches.Patch(color=BASIN_COLORS_PLOT["Kun"], label="Kun basin"),
        mpatches.Patch(color=BASIN_COLORS_PLOT["Cycle"], label="Cycle basin"),
        mpatches.Patch(color=BASIN_COLORS_PLOT["Qian"], label="Qian basin"),
    ]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9)

    plt.tight_layout()
    for ext in ('png', 'svg'):
        path = f"{outdir}/05_kw_depth_walk.{ext}"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Key Findings
# ═══════════════════════════════════════════════════════════════════════

def section_key_findings(depth_seq):
    print("\n" + "=" * 70)
    print("## Key Findings")
    print("=" * 70)

    dc = Counter(depth_seq)
    d1_positions = [i + 1 for i, d in enumerate(depth_seq) if d == 1]
    d0_positions = [i + 1 for i, d in enumerate(depth_seq) if d == 0]

    print(f"""
1. DEPTH DISTRIBUTION
   Depth 0: {dc[0]} hexagrams (attractors at KW positions {d0_positions})
   Depth 1: {dc[1]} hexagrams (= 6 pairs)
   Depth 2: {dc[2]} hexagrams (= 24 pairs, the majority)

2. KW FRAMING
   KW opens with depth-0 pair (Qian=1, Kun=2) and closes with
   depth-0 pair (JiJi=63, WeiJi=64). Attractors bookend the sequence.

3. PAIR DEPTH INVARIANCE
   Both members of every KW pair share the same depth.
   Algebraic: inner bits under reversal preserve the attractor set
   {{0,5,10,15}}. Under complement, inner→inner⊕15, also preserved.

4. DEPTH-1 CLUSTERING
   Depth-1 positions: {d1_positions}
   Not uniformly distributed — concentrated in certain regions.
   Depth-2 dominates the middle of the sequence.

5. BASIN × DEPTH
   Each basin has its own depth distribution:
   - Kun:  1 depth-0, 3 depth-1, 12 depth-2 (16 total)
   - Qian: 1 depth-0, 3 depth-1, 12 depth-2 (16 total)
   - Cycle: 2 depth-0, 6 depth-1, 24 depth-2 (32 total)
   Perfectly proportional within each basin (1:3:12 for fixed, 1:3:12 for cycle).
""")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import os
    outdir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("05: CONVERGENCE DEPTH ALONG KW SEQUENCE")
    print("=" * 70)

    depth_seq = section_depth_labeling()
    section_depth_clustering(depth_seq)
    section_depth_basin(depth_seq)
    section_depth_pairs()
    section_visualization(depth_seq, outdir)
    section_key_findings(depth_seq)


if __name__ == '__main__':
    main()
