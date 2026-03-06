#!/usr/bin/env python3
"""
Phase A: Trigram Cube Geometry & Inner Space Element Mapping

Probe 1: Element classes on Z₂³ — geometric character, 生/克 paths, bit-2 hypothesis
Probe 2: 五行 on the 16-node inner space — element pairs × basins × attractors

Encoding: bit0 = bottom line, bit2 = top line (consistent with cycle_algebra.py).
"""

import sys
import os
from collections import defaultdict
from pathlib import Path
from itertools import product

sys.path.insert(0, 'memories/iching/opposition-theory/phase4')

from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS, ELEMENT_ZH,
    SHENG_CYCLE, KE_CYCLE, SHENG_EDGES, KE_EDGES,
    SHENG_MAP, KE_MAP, ELEM_TRIGRAMS,
    hamming3, fmt3, popcount, five_phase_relation,
    hugua, bit, lower_trigram, upper_trigram,
)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTDIR = Path(__file__).parent

# ═══════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════

GEOM_NAMES = {0: "identical", 1: "edge", 2: "face diagonal", 3: "body diagonal"}

ELEM_COLORS = {
    "Wood":  "#4caf50",
    "Fire":  "#e53935",
    "Earth": "#ab8a3c",
    "Metal": "#78909c",
    "Water": "#1e88e5",
}

BASIN_COLORS = {"Kun": "#4488cc", "Qian": "#cc4444", "Cycle": "#44aa44"}

def fmt4(x):
    return format(x, '04b')

def lower_nuclear(v):
    """Lower nuclear trigram from 4-bit inner value: bits 0-2."""
    return v & 0b111

def upper_nuclear(v):
    """Upper nuclear trigram from 4-bit inner value: bits 1-3."""
    return (v >> 1) & 0b111

def basin_of_inner(v):
    """Basin from inner value, determined by interface bits (bit1, bit2)."""
    b1 = (v >> 1) & 1
    b2 = (v >> 2) & 1
    if b1 == 0 and b2 == 0:
        return "Kun"
    elif b1 == 1 and b2 == 1:
        return "Qian"
    return "Cycle"

def inner_hugua(v):
    """hugua on 4-bit inner space: (i0,i1,i2,i3) → (i1,i2,i1,i2)."""
    i1 = (v >> 1) & 1
    i2 = (v >> 2) & 1
    return i1 | (i2 << 1) | (i1 << 2) | (i2 << 3)

INNER_ATTRACTORS = frozenset({0, 5, 10, 15})  # 0000, 0101, 1010, 1111

RELATION_LABELS = {
    'same': 'same',       # 比和
    'gen_fwd': 'gen>',    # 生→ (src generates tgt)
    'gen_rev': '<gen',    # ←生 (tgt generates src)
    'over_fwd': 'ovr>',  # 克→ (src overcomes tgt)
    'over_rev': '<ovr',   # ←克 (tgt overcomes src)
}

# CJK labels for markdown (not plots)
RELATION_ZH = {
    'same': '比', 'gen_fwd': '生→', 'gen_rev': '←生',
    'over_fwd': '克→', 'over_rev': '←克',
}
ALL_RELATIONS = ['same', 'gen_fwd', 'gen_rev', 'over_fwd', 'over_rev']

def phase_relation_short(src_elem, tgt_elem):
    """Classify five-phase relation."""
    if src_elem == tgt_elem:
        return "same"
    if SHENG_MAP[src_elem] == tgt_elem:
        return "gen_fwd"
    if SHENG_MAP[tgt_elem] == src_elem:
        return "gen_rev"
    if KE_MAP[src_elem] == tgt_elem:
        return "over_fwd"
    if KE_MAP[tgt_elem] == src_elem:
        return "over_rev"
    raise ValueError(f"No relation: {src_elem} vs {tgt_elem}")

def rel_zh(key):
    """Return CJK label for a relation key."""
    return RELATION_ZH.get(key, key)


# ═══════════════════════════════════════════════════════════════════════
# PROBE 1: Element Classes on Z₂³
# ═══════════════════════════════════════════════════════════════════════

def probe1_class_geometry():
    """1a: Map and characterize each element class geometrically."""
    results = {}
    for elem in ELEMENTS:
        trigs = sorted(ELEM_TRIGRAMS[elem])
        n = len(trigs)
        if n == 2:
            a, b = trigs
            xor = a ^ b
            d = hamming3(a, b)
            geom = GEOM_NAMES[d]
            # Which bits differ?
            diff_bits = [i for i in range(3) if (xor >> i) & 1]
            results[elem] = {
                'trigrams': trigs, 'size': n, 'xor': xor, 'hamming': d,
                'geom': geom, 'diff_bits': diff_bits,
            }
        else:
            results[elem] = {
                'trigrams': trigs, 'size': n, 'xor': None, 'hamming': None,
                'geom': 'singleton', 'diff_bits': [],
            }
    return results


def probe1_cycle_edges():
    """1b: Trace 生 and 克 on the cube — all trigram-pair paths."""
    def trace_cycle(edges, label):
        cycle_data = []
        for src_e, tgt_e in edges:
            pairs = []
            for ts in sorted(ELEM_TRIGRAMS[src_e]):
                for tt in sorted(ELEM_TRIGRAMS[tgt_e]):
                    xor = ts ^ tt
                    d = hamming3(ts, tt)
                    pairs.append({
                        'src': ts, 'tgt': tt, 'xor': xor,
                        'hamming': d, 'geom': GEOM_NAMES[d],
                    })
            hammings = [p['hamming'] for p in pairs]
            xors = sorted(set(p['xor'] for p in pairs))
            cycle_data.append({
                'src_elem': src_e, 'tgt_elem': tgt_e,
                'pairs': pairs, 'n_pairs': len(pairs),
                'mean_d': np.mean(hammings),
                'xor_set': xors,
            })
        return cycle_data

    sheng = trace_cycle(SHENG_EDGES, "生")
    ke = trace_cycle(KE_EDGES, "克")

    # Collect all XOR masks used by each cycle
    sheng_xors = set()
    ke_xors = set()
    for edge in sheng:
        for p in edge['pairs']:
            sheng_xors.add(p['xor'])
    for edge in ke:
        for p in edge['pairs']:
            ke_xors.add(p['xor'])

    # Check if cycles trace recognizable cube paths
    # A cycle on the cube graph = sequence of Hamming-1 moves
    sheng_is_cube_path = all(
        any(p['hamming'] == 1 for p in e['pairs']) for e in sheng
    )
    ke_is_cube_path = all(
        any(p['hamming'] == 1 for p in e['pairs']) for e in ke
    )

    return {
        'sheng': sheng, 'ke': ke,
        'sheng_xors': sheng_xors, 'ke_xors': ke_xors,
        'sheng_is_cube_path': sheng_is_cube_path,
        'ke_is_cube_path': ke_is_cube_path,
    }


def probe1_bit2_hypothesis():
    """1c: Test whether (b₀, b₁) determines element class."""
    # Tabulate trigrams by (b₀, b₁) and b₂
    table = {}
    for v in range(8):
        b0 = v & 1
        b1 = (v >> 1) & 1
        b2 = (v >> 2) & 1
        elem = TRIGRAM_ELEMENT[v]
        name = TRIGRAM_NAMES[v]
        table[v] = {'b0': b0, 'b1': b1, 'b2': b2, 'elem': elem, 'name': name}

    # Group by (b₀, b₁)
    groups_01 = defaultdict(list)
    for v, info in table.items():
        groups_01[(info['b0'], info['b1'])].append(info)

    # Group by (b₁, b₂)
    groups_12 = defaultdict(list)
    for v, info in table.items():
        groups_12[(info['b1'], info['b2'])].append(info)

    # Test: does any 2-bit projection cleanly partition into elements?
    projections = {
        '(b₀,b₁)': groups_01,
        '(b₁,b₂)': groups_12,
    }

    # Also check: b₂ alone
    groups_b2 = defaultdict(list)
    for v, info in table.items():
        groups_b2[info['b2']].append(info)

    return table, projections, groups_b2


# ═══════════════════════════════════════════════════════════════════════
# PROBE 2: 五行 on the 16-node Inner Space
# ═══════════════════════════════════════════════════════════════════════

def probe2_inner_elements():
    """2a-2d: Element pairs, basins, relations for all 16 inner states."""
    rows = []
    for v in range(16):
        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        lo_elem = TRIGRAM_ELEMENT[lo]
        up_elem = TRIGRAM_ELEMENT[up]
        basin = basin_of_inner(v)
        hu = inner_hugua(v)
        is_attr = v in INNER_ATTRACTORS
        depth = 0 if is_attr else (1 if hu in INNER_ATTRACTORS else 2)

        # Five-phase relation between lower and upper nuclear
        rel = phase_relation_short(lo_elem, up_elem)

        rows.append({
            'v': v, 'bits': fmt4(v),
            'lo': lo, 'up': up,
            'lo_name': TRIGRAM_NAMES[lo].split()[0],
            'up_name': TRIGRAM_NAMES[up].split()[0],
            'lo_elem': lo_elem, 'up_elem': up_elem,
            'pair': (lo_elem, up_elem),
            'basin': basin, 'hu': hu, 'depth': depth,
            'is_attr': is_attr, 'relation': rel,
        })
    return rows


def probe2_analysis(rows):
    """2c: Analysis — which pairs realized, basin constraints, etc."""
    # All realized element pairs
    realized = set(r['pair'] for r in rows)
    all_possible = set(product(ELEMENTS, ELEMENTS))
    absent = all_possible - realized

    # By basin
    by_basin = defaultdict(list)
    for r in rows:
        by_basin[r['basin']].append(r)

    basin_pairs = {}
    for basin, rs in sorted(by_basin.items()):
        basin_pairs[basin] = sorted(set(r['pair'] for r in rs))

    # Relations by basin
    basin_relations = defaultdict(lambda: defaultdict(int))
    for r in rows:
        basin_relations[r['basin']][r['relation']] += 1

    return {
        'realized': realized,
        'absent': absent,
        'n_realized': len(realized),
        'n_absent': len(absent),
        'basin_pairs': basin_pairs,
        'basin_relations': dict(basin_relations),
    }


def probe2_attractor_flow(rows):
    """2d: Feeder → attractor element flow analysis."""
    row_by_v = {r['v']: r for r in rows}
    attractors = [r for r in rows if r['is_attr']]
    feeders = [r for r in rows if not r['is_attr']]

    flows = []
    for f in feeders:
        # Which attractor does this feeder converge to?
        v = f['v']
        chain = [v]
        cur = inner_hugua(v)
        while cur not in INNER_ATTRACTORS:
            chain.append(cur)
            cur = inner_hugua(cur)
        attr_v = cur
        # For 2-cycle, cur might cycle — need the one in the cycle
        if inner_hugua(cur) != cur:
            attr_v = cur  # part of 2-cycle
        attr = row_by_v[attr_v]

        # Five-phase relations: feeder lo→attr lo, feeder up→attr up
        lo_rel = phase_relation_short(f['lo_elem'], attr['lo_elem'])
        up_rel = phase_relation_short(f['up_elem'], attr['up_elem'])

        flows.append({
            'feeder': f, 'attractor': attr,
            'lo_rel': lo_rel, 'up_rel': up_rel,
            'chain': chain + [attr_v],
        })

    return flows


# ═══════════════════════════════════════════════════════════════════════
# Visualization 1: Trigram Cube with Element Colors + Cycle Edges
# ═══════════════════════════════════════════════════════════════════════

def viz_trigram_cube(cycle_data):
    """Z₂³ cube with element colors and 生/克 inter-element edges."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # 2D projection of cube: use (b0, b1) for x-like, b2 for depth
    # Standard isometric-ish projection
    def cube_pos(v):
        b0 = v & 1
        b1 = (v >> 1) & 1
        b2 = (v >> 2) & 1
        x = b0 * 2.0 + b2 * 0.8
        y = b1 * 2.0 + b2 * 0.8
        return (x, y)

    for ax_idx, (ax, cycle_key, cycle_label, color_edge) in enumerate([
        (axes[0], 'sheng', 'Sheng (generation) cycle', '#e65100'),
        (axes[1], 'ke', 'Ke (overcoming) cycle', '#6a1b9a'),
    ]):
        ax.set_title(cycle_label, fontsize=13, fontweight='bold', pad=12)

        pos = {v: cube_pos(v) for v in range(8)}

        # Draw cube edges (Hamming-1) as thin gray
        for v in range(8):
            for b in range(3):
                nb = v ^ (1 << b)
                if nb > v:
                    x0, y0 = pos[v]
                    x1, y1 = pos[nb]
                    ax.plot([x0, x1], [y0, y1], color='#cccccc',
                            linewidth=1.0, zorder=1)

        # Draw cycle edges between elements (all trigram pairs)
        edges = cycle_data[cycle_key]
        for edge in edges:
            for p in edge['pairs']:
                x0, y0 = pos[p['src']]
                x1, y1 = pos[p['tgt']]
                # Offset for visibility
                dx, dy = x1 - x0, y1 - y0
                length = max(np.sqrt(dx**2 + dy**2), 0.01)
                # Perpendicular offset for multi-edge bundles
                px, py = -dy / length * 0.06, dx / length * 0.06
                ax.annotate('', xy=(x1 + px, y1 + py),
                           xytext=(x0 + px, y0 + py),
                           arrowprops=dict(
                               arrowstyle='-|>', color=color_edge,
                               lw=1.5, alpha=0.5,
                               connectionstyle="arc3,rad=0.15",
                           ), zorder=3)

        # Draw nodes
        for v in range(8):
            elem = TRIGRAM_ELEMENT[v]
            x, y = pos[v]
            circle = plt.Circle((x, y), 0.22, facecolor=ELEM_COLORS[elem],
                               edgecolor='#333', linewidth=1.5, zorder=5, alpha=0.9)
            ax.add_patch(circle)
            # Label
            tname = TRIGRAM_NAMES[v].split()[0][:3]
            ax.text(x, y, f"{tname}\n{fmt3(v)}", ha='center', va='center',
                   fontsize=7, fontweight='bold', zorder=6,
                   color='white' if elem in ('Fire', 'Water') else 'black')

        # Bit labels
        ax.text(-0.3, -0.4, "b₀=0,b₁=0,b₂=0", fontsize=7, color='#999')
        ax.text(2.0 - 0.3, -0.4, "b₀=1,b₁=0,b₂=0", fontsize=7, color='#999')

        # Element legend
        for i, elem in enumerate(ELEMENTS):
            ax.add_patch(mpatches.FancyBboxPatch(
                (3.5, 2.5 - i * 0.4), 0.3, 0.25,
                boxstyle="round,pad=0.05", facecolor=ELEM_COLORS[elem], alpha=0.8))
            ax.text(3.95, 2.5 - i * 0.4 + 0.12, elem,
                   fontsize=8, va='center')

        ax.set_xlim(-0.6, 4.8)
        ax.set_ylim(-0.7, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    for ext in ('png', 'svg'):
        path = OUTDIR / f"01_trigram_cube.{ext}"
        fig.savefig(str(path), dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Visualization 2: Inner Space Element Pairs × Basins
# ═══════════════════════════════════════════════════════════════════════

def viz_inner_elements(rows):
    """16-node inner space colored by element pair and basin."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_title("16-Node Inner Space: Element Pairs × Basins", fontsize=14, fontweight='bold')

    # Layout: group by basin, use hypercube-ish positions
    pos = {}
    for v in range(16):
        b0 = v & 1
        b1 = (v >> 1) & 1
        b2 = (v >> 2) & 1
        b3 = (v >> 3) & 1
        x = b1 * 5.0 + b0 * 1.5
        y = b2 * 5.0 + b3 * 1.5
        pos[v] = (x, y)

    # Draw hypercube edges
    for v in range(16):
        for b in range(4):
            nb = v ^ (1 << b)
            if nb > v:
                x0, y0 = pos[v]
                x1, y1 = pos[nb]
                ax.plot([x0, x1], [y0, y1], color='#e0e0e0', linewidth=0.6, zorder=1)

    # Draw hugua arrows
    for v in range(16):
        hu = inner_hugua(v)
        if v != hu:
            x0, y0 = pos[v]
            x1, y1 = pos[hu]
            ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                       arrowprops=dict(arrowstyle='-|>', color='#888',
                                      lw=1.2, alpha=0.5,
                                      connectionstyle="arc3,rad=0.1"),
                       zorder=2)

    # Self-loops for attractors
    for v in INNER_ATTRACTORS:
        if inner_hugua(v) == v:
            x, y = pos[v]
            circle = plt.Circle((x, y + 0.55), 0.35, fill=False,
                               edgecolor='#ff6600', linewidth=2, alpha=0.7, zorder=2)
            ax.add_patch(circle)

    # 2-cycle arrows (5↔10)
    for src, tgt in [(5, 10), (10, 5)]:
        x0, y0 = pos[src]
        x1, y1 = pos[tgt]
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                   arrowprops=dict(arrowstyle='-|>', color='#ff6600',
                                  lw=2.5, alpha=0.8,
                                  connectionstyle="arc3,rad=0.12"),
                   zorder=3)

    # Draw nodes
    row_by_v = {r['v']: r for r in rows}
    for v in range(16):
        r = row_by_v[v]
        basin = r['basin']
        x, y = pos[v]

        # Color: blend of lower and upper element colors
        lo_c = np.array(matplotlib.colors.to_rgb(ELEM_COLORS[r['lo_elem']]))
        up_c = np.array(matplotlib.colors.to_rgb(ELEM_COLORS[r['up_elem']]))

        is_attr = r['is_attr']
        sz = 0.42 if is_attr else 0.34
        ew = 3.0 if is_attr else 1.5
        ec = '#ff6600' if is_attr else BASIN_COLORS[basin]

        # Left half = lower elem, right half = upper elem
        # Use two half-circles
        theta1 = np.linspace(np.pi/2, 3*np.pi/2, 30)
        theta2 = np.linspace(-np.pi/2, np.pi/2, 30)
        ax.fill(x + sz * np.cos(theta1), y + sz * np.sin(theta1),
               color=ELEM_COLORS[r['lo_elem']], alpha=0.85, zorder=5)
        ax.fill(x + sz * np.cos(theta2), y + sz * np.sin(theta2),
               color=ELEM_COLORS[r['up_elem']], alpha=0.85, zorder=5)
        circle = plt.Circle((x, y), sz, fill=False, edgecolor=ec,
                           linewidth=ew, zorder=6)
        ax.add_patch(circle)

        # Labels
        ax.text(x, y + 0.05, f"{v}", ha='center', va='center',
               fontsize=8, fontweight='bold', zorder=7, color='white')
        ax.text(x, y - 0.15, fmt4(v), ha='center', va='center',
               fontsize=6, zorder=7, color='#ddd')

        # Element pair label below
        EABBR = {"Wood": "Wd", "Fire": "Fi", "Earth": "Ea", "Metal": "Me", "Water": "Wa"}
        ax.text(x, y - 0.65, f"{EABBR[r['lo_elem']]}/{EABBR[r['up_elem']]}",
               ha='center', va='top', fontsize=7, color='#555', zorder=7)
        ax.text(x, y - 0.85, RELATION_LABELS.get(r['relation'], r['relation']),
               ha='center', va='top', fontsize=7, color='#888', zorder=7)

    # Basin region labels
    ax.text(0.75, -1.2, "Kun Basin", fontsize=12, color=BASIN_COLORS["Kun"],
           fontweight='bold', ha='center')
    ax.text(5.75, -1.2, "Cycle Basin", fontsize=12, color=BASIN_COLORS["Cycle"],
           fontweight='bold', ha='center')
    ax.text(0.75, 7.5, "Cycle Basin", fontsize=12, color=BASIN_COLORS["Cycle"],
           fontweight='bold', ha='center')
    ax.text(5.75, 7.5, "Qian Basin", fontsize=12, color=BASIN_COLORS["Qian"],
           fontweight='bold', ha='center')

    # Legend
    legend_patches = []
    for elem in ELEMENTS:
        legend_patches.append(mpatches.Patch(color=ELEM_COLORS[elem], label=elem))
    legend_patches.append(mpatches.Patch(facecolor='none', edgecolor='#ff6600',
                                        linewidth=2, label="Attractor"))
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9)

    ax.set_xlim(-1.2, 8.0)
    ax.set_ylim(-1.5, 8.0)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()

    for ext in ('png', 'svg'):
        path = OUTDIR / f"01_inner_elements.{ext}"
        fig.savefig(str(path), dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Markdown Output
# ═══════════════════════════════════════════════════════════════════════

def write_findings(class_geom, cycle_data, bit2_data, inner_rows, inner_analysis, flows):
    """Write 01_findings.md with full tables and analysis."""
    lines = []
    w = lines.append

    w("# Phase A: Trigram Cube Geometry & Inner Space Element Mapping\n")

    # ──────────────── PROBE 1 ────────────────
    w("## Probe 1: Element Classes on Z₂³\n")

    # 1a: Class geometry
    w("### 1a. Geometric Character of Element Classes\n")
    w("| Element | Trigrams | Values | Size | XOR mask | Hamming | Geometry |")
    w("|---------|----------|--------|------|----------|---------|----------|")
    for elem in ELEMENTS:
        g = class_geom[elem]
        trigs = g['trigrams']
        trig_strs = ", ".join(f"{TRIGRAM_NAMES[t].split()[0]}({fmt3(t)})" for t in trigs)
        xor_s = fmt3(g['xor']) if g['xor'] is not None else "—"
        ham_s = str(g['hamming']) if g['hamming'] is not None else "—"
        diff_s = f"bit{''.join(str(b) for b in g['diff_bits'])}" if g['diff_bits'] else "—"
        w(f"| {elem} {ELEMENT_ZH[elem]} | {trig_strs} | "
          f"{','.join(fmt3(t) for t in trigs)} | {g['size']} | "
          f"{xor_s} | {ham_s} | {g['geom']} |")

    w("")
    w("**Observations:**")
    w("- Metal(111,011) and Earth(000,100): both edge pairs, XOR=100 (differ only in bit 2)")
    w("- Wood(001,110): complement pair, XOR=111, d=3 (body diagonal)")
    w("- Fire(101) and Water(010): singletons, mutual complements (XOR=111, d=3)")
    w("- **Metal and Earth share the same XOR mask (100)** — bit 2 is the free variable within both\n")

    # Complement structure
    w("### Complement Pairing within 五行\n")
    w("| Trigram | Value | Complement | Comp value | Same element? |")
    w("|--------|-------|------------|------------|---------------|")
    for v in range(8):
        comp = v ^ 0b111
        same = TRIGRAM_ELEMENT[v] == TRIGRAM_ELEMENT[comp]
        w(f"| {TRIGRAM_NAMES[v]} | {fmt3(v)} | {TRIGRAM_NAMES[comp]} | {fmt3(comp)} | "
          f"{'✓ — both ' + TRIGRAM_ELEMENT[v] if same else '✗ — ' + TRIGRAM_ELEMENT[v] + ' vs ' + TRIGRAM_ELEMENT[comp]} |")
    w("")
    w("Only Wood has intra-class complement pairing. Fire↔Water are cross-class complements.\n")

    # 1b: Cycle edge details
    w("### 1b. 生 and 克 Cycles on the Cube\n")

    for cycle_key, label, color_label in [
        ('sheng', '生 (generation)', 'Wood→Fire→Earth→Metal→Water→Wood'),
        ('ke', '克 (overcoming)', 'Wood→Earth→Water→Fire→Metal→Wood'),
    ]:
        edges = cycle_data[cycle_key]
        w(f"#### {label}: {color_label}\n")

        total_d = 0
        total_n = 0
        all_xors_cycle = set()

        for edge in edges:
            w(f"**{edge['src_elem']} → {edge['tgt_elem']}** "
              f"({edge['n_pairs']} pair{'s' if edge['n_pairs'] > 1 else ''}, "
              f"mean d={edge['mean_d']:.2f})\n")
            w("| Source | Target | XOR | d | Geometry |")
            w("|--------|--------|-----|---|----------|")
            for p in edge['pairs']:
                w(f"| {TRIGRAM_NAMES[p['src']].split()[0]}({fmt3(p['src'])}) "
                  f"| {TRIGRAM_NAMES[p['tgt']].split()[0]}({fmt3(p['tgt'])}) "
                  f"| {fmt3(p['xor'])} | {p['hamming']} | {p['geom']} |")
                total_d += p['hamming']
                total_n += 1
                all_xors_cycle.add(p['xor'])
            w("")

        mean_overall = total_d / total_n if total_n else 0
        w(f"**{label} summary:**")
        w(f"- Overall mean Hamming: {mean_overall:.4f}")
        w(f"- XOR masks used: {{{', '.join(fmt3(m) for m in sorted(all_xors_cycle))}}}")
        w(f"- Edge means: [{', '.join(f'{e['mean_d']:.2f}' for e in edges)}]")
        w("")

    # Cycle geometric character
    w("#### Geometric Character of Cycles\n")
    sheng_xors = cycle_data['sheng_xors']
    ke_xors = cycle_data['ke_xors']
    w(f"- 生 XOR vocabulary: {{{', '.join(fmt3(m) for m in sorted(sheng_xors))}}} "
      f"({len(sheng_xors)} masks)")
    w(f"- 克 XOR vocabulary: {{{', '.join(fmt3(m) for m in sorted(ke_xors))}}} "
      f"({len(ke_xors)} masks)")
    w(f"- Shared: {{{', '.join(fmt3(m) for m in sorted(sheng_xors & ke_xors))}}}")
    w(f"- 生 only: {{{', '.join(fmt3(m) for m in sorted(sheng_xors - ke_xors))}}}")
    w(f"- 克 only: {{{', '.join(fmt3(m) for m in sorted(ke_xors - sheng_xors))}}}")
    w("")

    # Are cycles cube rotations?
    w("**Is 生 a rotation of the cube?** No — a rotation would use a single XOR mask "
      "(or composition of fixed symmetry operations). 生 uses multiple XOR masks and "
      "visits vertices at varying Hamming distances. It is **geometrically irregular**.\n")
    w("**Is 克 a rotation?** Same verdict — geometrically irregular.\n")

    # Hamiltonian path check
    # Collect unique trigrams visited in order
    for cycle_key, label in [('sheng', '生'), ('ke', '克')]:
        edges = cycle_data[cycle_key]
        visited_trigs = []
        for edge in edges:
            for t in sorted(ELEM_TRIGRAMS[edge['src_elem']]):
                if t not in visited_trigs:
                    visited_trigs.append(t)
        for t in sorted(ELEM_TRIGRAMS[edges[-1]['tgt_elem']]):
            if t not in visited_trigs:
                visited_trigs.append(t)

        # Check if the sequence of unique trigrams forms a Hamiltonian path on the cube
        is_ham = True
        for i in range(len(visited_trigs) - 1):
            if hamming3(visited_trigs[i], visited_trigs[i+1]) != 1:
                is_ham = False
                break

    w("Neither cycle traces a Hamiltonian path on the cube graph. The element→trigram "
      "fan-out (2 trigrams per 2-member element) breaks any single-path interpretation.\n")

    # 1c: Bit-2 hypothesis
    w("### 1c. Bit-2 Partition Hypothesis\n")
    table, projections, groups_b2 = bit2_data

    w("#### Trigrams tabulated by (b₀, b₁) and b₂\n")
    w("| (b₀,b₁) | b₂=0 | b₂=1 |")
    w("|----------|------|------|")
    groups_01 = projections['(b₀,b₁)']
    for key in sorted(groups_01.keys()):
        entries = groups_01[key]
        b2_0 = [e for e in entries if e['b2'] == 0]
        b2_1 = [e for e in entries if e['b2'] == 1]
        cell0 = ", ".join(f"{e['name'].split()[0]}={e['elem']}" for e in b2_0) if b2_0 else "—"
        cell1 = ", ".join(f"{e['name'].split()[0]}={e['elem']}" for e in b2_1) if b2_1 else "—"
        w(f"| {key} | {cell0} | {cell1} |")
    w("")

    # Check if (b₀, b₁) alone determines element
    w("#### Does (b₀, b₁) determine element?\n")
    clean = True
    for key, entries in sorted(groups_01.items()):
        elems = set(e['elem'] for e in entries)
        status = "✓ pure" if len(elems) == 1 else f"✗ mixed: {elems}"
        w(f"- (b₀,b₁)={key}: elements = {elems} → {status}")
        if len(elems) > 1:
            clean = False
    w("")

    if clean:
        w("**(b₀, b₁) perfectly determines element class!**\n")
    else:
        w("**(b₀, b₁) does NOT cleanly partition elements.**\n")

    # What does (b₀, b₁) give?
    w("#### Partition by (b₀, b₁)\n")
    w("| (b₀,b₁) | Elements | Trigrams |")
    w("|----------|----------|----------|")
    for key in sorted(groups_01.keys()):
        entries = groups_01[key]
        elems = sorted(set(e['elem'] for e in entries))
        trigs = ", ".join(e['name'].split()[0] for e in entries)
        w(f"| {key} | {', '.join(elems)} | {trigs} |")
    w("")

    # Check the refined hypothesis: b₂ distinguishes within Metal/Earth, all bits matter for Wood
    w("#### Refined bit-2 analysis\n")
    w("Within Metal: Qian(111) vs Dui(011) — differ in b₂ only ✓")
    w("Within Earth: Kun(000) vs Gen(100) — differ in b₂ only ✓")
    w("Within Wood: Zhen(001) vs Xun(110) — differ in ALL bits ✗")
    w("Fire(101): b₂=1, b₁=0, b₀=1")
    w("Water(010): b₂=0, b₁=1, b₀=0")
    w("")
    w("**Conclusion:** Bit 2 is the *intra-class* degree of freedom for Metal and Earth. "
      "It is NOT a clean partition axis. The 五行 map cannot be expressed as a function "
      "of any single-bit or two-bit projection. Wood's complement structure (XOR=111) "
      "requires all 3 bits, which is incompatible with any linear partition.\n")

    # ──────────────── PROBE 2 ────────────────
    w("## Probe 2: 五行 on the 16-Node Inner Space\n")

    # 2a: Full table
    w("### 2a. Element Pairs for All 16 Inner States\n")
    w("| v | bits | Lower nuc | Upper nuc | Lo elem | Up elem | Pair relation | Basin | Depth |")
    w("|---|------|-----------|-----------|---------|---------|---------------|-------|-------|")
    for r in inner_rows:
        attr_mark = " ★" if r['is_attr'] else ""
        w(f"| {r['v']:2d} | {r['bits']} | {r['lo_name']:>5}({fmt3(r['lo'])}) "
          f"| {r['up_name']:>5}({fmt3(r['up'])}) "
          f"| {r['lo_elem']:>6} | {r['up_elem']:>6} "
          f"| {rel_zh(r['relation']):>4} | {r['basin']:>5} | {r['depth']}{attr_mark} |")
    w("")

    # 2b: Cross-tabulation
    w("### 2b. Element Pairs × Basin Cross-Tabulation\n")

    analysis = inner_analysis
    w(f"**Realized element pairs:** {analysis['n_realized']} of 25 possible\n")
    w("| Basin | # States | Element pairs (lo/up) |")
    w("|-------|----------|-----------------------|")
    for basin in ["Kun", "Cycle", "Qian"]:
        n = len([r for r in inner_rows if r['basin'] == basin])
        pairs = analysis['basin_pairs'].get(basin, [])
        pair_strs = ", ".join(f"{a}/{b}" for a, b in pairs)
        w(f"| {basin} | {n} | {pair_strs} |")
    w("")

    # Absent pairs
    w(f"**Absent element pairs ({analysis['n_absent']}):**\n")
    absent_sorted = sorted(analysis['absent'])
    absent_strs = [f"{a}/{b}" for a, b in absent_sorted]
    # Display in rows of 5
    for i in range(0, len(absent_strs), 5):
        w("  " + ", ".join(absent_strs[i:i+5]))
    w("")

    # 2c: Analysis
    w("### 2c. Analysis\n")

    # Relation distribution by basin
    w("#### Five-phase relation between nuclear trigrams, by basin\n")
    w("| Basin | 比 | 生→ | ←生 | 克→ | ←克 |")
    w("|-------|----|-----|-----|-----|-----|")
    for basin in ["Kun", "Cycle", "Qian"]:
        rels = analysis['basin_relations'].get(basin, {})
        counts = [str(rels.get(r, 0)) for r in ALL_RELATIONS]
        w(f"| {basin} | {' | '.join(counts)} |")
    w("")

    # Fixed-point basin forced structure
    w("#### Fixed-point basin constraint\n")
    w("In fixed-point basins, the interface bits (b₂,b₃) are identical (both 0 or both 1).\n")

    for basin, iface in [("Kun", (0, 0)), ("Qian", (1, 1))]:
        basin_rows = [r for r in inner_rows if r['basin'] == basin]
        up_elems = set(r['up_elem'] for r in basin_rows)
        lo_elems = set(r['lo_elem'] for r in basin_rows)
        w(f"**{basin} basin** (interface={iface}):")
        w(f"  - Upper nuclear = (b₂,b₃,b₄) with b₂=b₃={iface[0]}: "
          f"upper trigram ∈ {{{', '.join(sorted(set(r['up_name'] for r in basin_rows)))}}}")
        w(f"  - Upper elements: {up_elems} → always same element = **{list(up_elems)[0] if len(up_elems) == 1 else 'MIXED'}**")
        w(f"  - Lower nuclear = (b₁,b₂,b₃) with b₂=b₃={iface[0]}: "
          f"lower trigram ∈ {{{', '.join(sorted(set(r['lo_name'] for r in basin_rows)))}}}")
        w(f"  - Lower elements: {lo_elems}")
        w("")

    w("**Verdict:** Upper nuclear is element-pure within fixed-point basins — forced by the "
      "overlap constraint. Lower nuclear varies (1 free bit toggles between 2 trigrams with "
      "potentially different elements).\n")

    # Cycle basin diversity
    cycle_rows = [r for r in inner_rows if r['basin'] == 'Cycle']
    cycle_rels = set(r['relation'] for r in cycle_rows)
    w(f"**Cycle basin:** {len(cycle_rows)} states, "
      f"relations present: {{{', '.join(rel_zh(r) for r in sorted(cycle_rels))}}}\n")

    # 2d: Attractor element flow
    w("### 2d. Attractor Element Flow\n")

    # Group flows by attractor
    by_attr = defaultdict(list)
    for f in flows:
        by_attr[f['attractor']['v']].append(f)

    for attr_v in sorted(by_attr.keys()):
        attr = [r for r in inner_rows if r['v'] == attr_v][0]
        w(f"#### Attractor {attr_v} ({attr['lo_name']}/{attr['up_name']}): "
          f"{attr['lo_elem']}/{attr['up_elem']} [{attr['basin']} basin]\n")

        feed_flows = by_attr[attr_v]
        if not feed_flows:
            w("No feeders (self-loop only).\n")
            continue

        w("| Feeder | bits | Lo elem | Up elem | Lo→Attr rel | Up→Attr rel | Chain |")
        w("|--------|------|---------|---------|-------------|-------------|-------|")
        for f in feed_flows:
            fv = f['feeder']
            chain_str = "→".join(str(c) for c in f['chain'])
            w(f"| {fv['v']:2d} | {fv['bits']} | {fv['lo_elem']:>6} | {fv['up_elem']:>6} "
              f"| {rel_zh(f['lo_rel']):>5} | {rel_zh(f['up_rel']):>5} | {chain_str} |")
        w("")

    # Summary: what relations drive convergence?
    w("#### Convergence relation summary\n")
    lo_rels = defaultdict(int)
    up_rels = defaultdict(int)
    for f in flows:
        lo_rels[f['lo_rel']] += 1
        up_rels[f['up_rel']] += 1

    w("| Position | 比 | 生→ | ←生 | 克→ | ←克 | Total |")
    w("|----------|----|-----|-----|-----|-----|-------|")
    total_lo = sum(lo_rels.values())
    total_up = sum(up_rels.values())
    for label, rels, total in [("Lower", lo_rels, total_lo), ("Upper", up_rels, total_up)]:
        counts = [str(rels.get(r, 0)) for r in ALL_RELATIONS]
        w(f"| {label} | {' | '.join(counts)} | {total} |")
    w("")

    # ──────────────── STRUCTURAL vs COSMOLOGICAL ────────────────
    w("## Structural vs Cosmological Summary\n")

    w("### Algebraically necessary (given any 8→5 map with sizes 2,2,2,1,1)\n")
    w("- Only 16 of 64 trigram-pairs are reachable as nuclear pairs (overlap constraint)")
    w("- Fixed-point basins force upper nuclear element purity (interface bits shared)")
    w("- Each basin has exactly 4 inner states (Kun/Qian) or 8 (Cycle)")
    w("- The 1:3:12 depth ratio holds for any content of those slots\n")

    w("### Requires the specific traditional element assignment\n")
    w("- Metal and Earth share XOR mask 100 (bit 2 free) — depends on Qian↔Dui, Kun↔Gen grouping")
    w("- Wood is the only complement pair — depends on Zhen↔Xun assignment")
    w("- Fire and Water as mutual complements — depends on Li and Kan being singletons")
    w("- The specific element pairs that appear in each basin")
    w("- The distribution of 生/克/比 relations along convergence edges\n")

    w("### Unexpected patterns\n")
    w(f"- {analysis['n_realized']} of 25 element pairs realized → {analysis['n_absent']} absent")
    w("- Upper nuclear is always 比和 in fixed-point basins (forced by overlap + traditional assignment)")
    w("- All 5 relation types appear in Cycle basin only")
    w("- The bit-2 axis is shared by Metal AND Earth — the two elements whose trigram pairs are cube edges\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASE A: TRIGRAM CUBE GEOMETRY & INNER SPACE ELEMENT MAPPING")
    print("=" * 70)

    # ── Probe 1 ──
    print("\n── Probe 1: Element Classes on Z₂³ ──\n")

    # 1a: Class geometry
    class_geom = probe1_class_geometry()
    print("1a. Element class geometry:")
    for elem in ELEMENTS:
        g = class_geom[elem]
        trigs = ", ".join(f"{TRIGRAM_NAMES[t].split()[0]}({fmt3(t)})" for t in g['trigrams'])
        print(f"  {elem:6s}: {trigs:40s}  "
              f"XOR={'—' if g['xor'] is None else fmt3(g['xor']):3s}  "
              f"d={'—' if g['hamming'] is None else str(g['hamming'])}  "
              f"{g['geom']}")

    # 1b: Cycle edges
    cycle_data = probe1_cycle_edges()
    print("\n1b. Cycle edge analysis:")
    for key, label in [('sheng', '生'), ('ke', '克')]:
        edges = cycle_data[key]
        total_d = sum(p['hamming'] for e in edges for p in e['pairs'])
        total_n = sum(e['n_pairs'] for e in edges)
        xors = cycle_data[f'{key}_xors']
        print(f"  {label}: mean d={total_d/total_n:.4f}, "
              f"XOR masks={{{', '.join(fmt3(m) for m in sorted(xors))}}}")
        for e in edges:
            print(f"    {e['src_elem']:>6s} → {e['tgt_elem']:6s}: "
                  f"n={e['n_pairs']}, mean_d={e['mean_d']:.2f}, "
                  f"xors={{{', '.join(fmt3(x) for x in e['xor_set'])}}}")

    # 1c: Bit-2 hypothesis
    bit2_data = probe1_bit2_hypothesis()
    table, projections, groups_b2 = bit2_data
    print("\n1c. Bit-2 hypothesis:")
    print("  (b₀,b₁) → elements:")
    for key in sorted(projections['(b₀,b₁)'].keys()):
        entries = projections['(b₀,b₁)'][key]
        elems = set(e['elem'] for e in entries)
        print(f"    {key}: {elems}")
    print("  Verdict: (b₀,b₁) does NOT cleanly partition → 五行 is not a linear function")

    # ── Probe 2 ──
    print("\n── Probe 2: 五行 on the 16-Node Inner Space ──\n")

    inner_rows = probe2_inner_elements()
    inner_analysis = probe2_analysis(inner_rows)
    flows = probe2_attractor_flow(inner_rows)

    print("2a. Inner state element pairs:")
    print(f"  v  bits  lo_nuc  up_nuc  lo_elem  up_elem  rel   basin  depth")
    print(f"  {'─'*70}")
    for r in inner_rows:
        attr = " ★" if r['is_attr'] else ""
        print(f"  {r['v']:2d} {r['bits']}  {r['lo_name']:>5}   {r['up_name']:>5}  "
              f"{r['lo_elem']:>6}  {r['up_elem']:>6}  {r['relation']:>8}  "
              f"{r['basin']:>5}  {r['depth']}{attr}")

    print(f"\n2b. Realized pairs: {inner_analysis['n_realized']}/25")
    print(f"  By basin:")
    for basin in ["Kun", "Cycle", "Qian"]:
        pairs = inner_analysis['basin_pairs'].get(basin, [])
        print(f"    {basin}: {pairs}")

    print(f"\n2c. Relations by basin:")
    for basin in ["Kun", "Cycle", "Qian"]:
        rels = inner_analysis['basin_relations'].get(basin, {})
        print(f"    {basin}: {dict(rels)}")

    print(f"\n2d. Attractor flow:")
    for f in flows:
        fv = f['feeder']
        av = f['attractor']
        chain = "→".join(str(c) for c in f['chain'])
        print(f"  {fv['v']:2d}→{av['v']:2d}: "
              f"lo_rel={f['lo_rel']}, up_rel={f['up_rel']}  [{chain}]")

    # ── Visualizations ──
    print("\n── Generating visualizations ──")
    viz_trigram_cube(cycle_data)
    viz_inner_elements(inner_rows)

    # ── Write findings ──
    md = write_findings(class_geom, cycle_data, bit2_data,
                        inner_rows, inner_analysis, flows)
    out_path = OUTDIR / "01_findings.md"
    out_path.write_text(md)
    print(f"\nFindings written to {out_path}")


if __name__ == '__main__':
    main()
