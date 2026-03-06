"""
02: Five-phase flow map on inner space.
For all 64x64 pairs, compute Hu-lower five-phase relations.
Show aggregate flow field: net sheng/ke per node.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kwmapper')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from collections import Counter, defaultdict

from common import *

pos = inner_layout()

# ── Compute all-pairs five-phase on Hu lower ─────────────────────────────────

# For each inner value, compute net sheng/ke flow from KW consecutive transitions
# Also compute the structural (all-pairs) flow

# KW consecutive flow
kw_node_sheng = Counter()  # incoming sheng
kw_node_ke = Counter()     # incoming ke

for i in range(63):
    v1 = INNER[i]
    v2 = INNER[i + 1]
    rel = trig_phase(HU_LO[i], HU_LO[i + 1])
    pc = phase_class(rel)
    
    if pc == 'sheng':
        kw_node_sheng[v2] += 1  # v2 receives sheng
    elif pc == 'ke':
        kw_node_ke[v2] += 1     # v2 receives ke

# ── Structural: for each pair of inner values, what's the Hu-lower five-phase? ──

# The Hu lower trigram is determined by inner bits (h1, h2, h3)
# For inner value v: h1=bit0, h2=bit1, h3=bit2 → hu_lower = trigram(h1,h2,h3)

def inner_hu_lower_trig(v):
    h1, h2, h3, h4 = inner_to_bits(v)
    return h1 | (h2 << 1) | (h3 << 2)

def inner_hu_upper_trig(v):
    h1, h2, h3, h4 = inner_to_bits(v)
    return h2 | (h3 << 1) | (h4 << 2)

# Structural five-phase between all 16×16 inner value pairs
struct_edges = {}
for v1 in INNER_VALS:
    for v2 in INNER_VALS:
        if v1 == v2:
            continue
        t1 = inner_hu_lower_trig(v1)
        t2 = inner_hu_lower_trig(v2)
        rel = trig_phase(t1, t2)
        pc = phase_class(rel)
        struct_edges[(v1, v2)] = pc

# ── Draw structural flow field ───────────────────────────────────────────────

fig, ax = setup_fig('Structural Five-Phase Flow (Hu Lower)\nAll 16x16 inner-value pairs', 
                    figsize=(14, 9))
draw_basin_regions(ax, pos)

# Draw all structural edges (light, background)
for (v1, v2), pc in struct_edges.items():
    x1, y1 = pos[v1]
    x2, y2 = pos[v2]
    color = PHASE_EDGE[pc]
    
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle="arc3,rad=0.08",
        arrowstyle='->,head_length=4,head_width=2.5',
        color=color, linewidth=0.4, alpha=0.25,
        zorder=2
    )
    ax.add_patch(arrow)

draw_nodes(ax, pos, node_size=700)

# Net balance label per node
for v in INNER_VALS:
    x, y = pos[v]
    # Count structural incoming sheng vs ke
    in_sheng = sum(1 for v2 in INNER_VALS if v2 != v and struct_edges.get((v2, v), '') == 'sheng')
    in_ke = sum(1 for v2 in INNER_VALS if v2 != v and struct_edges.get((v2, v), '') == 'ke')
    net = in_sheng - in_ke
    sign = '+' if net > 0 else ''
    ax.text(x, y - 0.55, f'{sign}{net}', ha='center', va='top',
            fontsize=7, fontweight='bold',
            color='#22AA44' if net > 0 else '#CC3333' if net < 0 else '#999999')

legend_elements = [
    plt.Line2D([0], [0], color=PHASE_EDGE['sheng'], lw=2, label='Sheng (generative)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['ke'], lw=2, label='Ke (destructive)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['bi'], lw=2, label='Bi (same element)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
ax.text(0.02, 0.02, 'Node labels: net incoming sheng - ke (structural)',
        transform=ax.transAxes, fontsize=8, color='#666666')

save(fig, '02_fivephase_structural')
plt.close()

# ── Draw KW flow with net balance ────────────────────────────────────────────

fig, ax = setup_fig('KW Walk Five-Phase Flow (Hu Lower)\nNode color: net sheng(green) / ke(red)', 
                    figsize=(14, 9))
draw_basin_regions(ax, pos)

# KW edges
kw_edge_data = defaultdict(lambda: Counter())
for i in range(63):
    v1 = INNER[i]
    v2 = INNER[i + 1]
    if v1 == v2:
        continue
    rel = trig_phase(HU_LO[i], HU_LO[i + 1])
    pc = phase_class(rel)
    kw_edge_data[(v1, v2)][pc] += 1

drawn = set()
for (v1, v2), counts in kw_edge_data.items():
    x1, y1 = pos[v1]
    x2, y2 = pos[v2]
    dominant = counts.most_common(1)[0][0]
    total = sum(counts.values())
    color = PHASE_EDGE[dominant]
    lw = 0.8 + total * 0.8
    
    reverse_exists = (v2, v1) in kw_edge_data
    if reverse_exists and (v2, v1) not in drawn:
        curve = 0.15
    elif reverse_exists:
        curve = -0.15
    else:
        curve = 0.05
    
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad={curve}",
        arrowstyle='->,head_length=6,head_width=4',
        color=color, linewidth=lw, alpha=0.7, zorder=3
    )
    ax.add_patch(arrow)
    drawn.add((v1, v2))

# Nodes colored by net KW sheng/ke balance
for v in INNER_VALS:
    x, y = pos[v]
    net = kw_node_sheng[v] - kw_node_ke[v]
    
    # Color interpolation: green (+) to red (-)
    max_net = max(abs(kw_node_sheng[vv] - kw_node_ke[vv]) for vv in INNER_VALS) or 1
    t = net / max_net  # -1 to 1
    if t >= 0:
        r, g, b = 0.2 * (1 - t) + 0.13 * t, 0.5 * (1 - t) + 0.67 * t, 0.3 * (1 - t) + 0.27 * t
    else:
        t2 = -t
        r, g, b = 0.2 * (1 - t2) + 0.8 * t2, 0.5 * (1 - t2) + 0.2 * t2, 0.3 * (1 - t2) + 0.2 * t2
    
    ax.scatter(x, y, s=700, c=[(r, g, b)], edgecolors='white', linewidths=2, zorder=5)
    
    name = inner_hu_name(v)
    ax.text(x, y + 0.02, name, ha='center', va='center',
            fontsize=7, fontweight='bold', color='white', zorder=6)
    
    sign = '+' if net > 0 else ''
    ax.text(x, y - 0.45, f'{sign}{net} ({kw_node_sheng[v]}S/{kw_node_ke[v]}K)',
            ha='center', va='top', fontsize=6, color='#333333')

legend_elements = [
    plt.Line2D([0], [0], color=PHASE_EDGE['sheng'], lw=2, label='Sheng (generative)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['ke'], lw=2, label='Ke (destructive)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['bi'], lw=2, label='Bi (same element)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

save(fig, '02_fivephase_kw')
plt.close()

# ── Basin-level summary ──────────────────────────────────────────────────────

print("\n  Structural five-phase flow by basin:")
for basin in [-1, 0, 1]:
    members = [v for v in INNER_VALS if INNER_BASINS[v] == basin]
    in_s = sum(1 for v in members 
               for v2 in INNER_VALS if v2 != v 
               and struct_edges.get((v2, v), '') == 'sheng')
    in_k = sum(1 for v in members
               for v2 in INNER_VALS if v2 != v
               and struct_edges.get((v2, v), '') == 'ke')
    print(f"    {BASIN_NAME[basin]:6s}: incoming sheng={in_s}  ke={in_k}  net={in_s-in_k}")

print("\n  KW walk five-phase flow by basin:")
for basin in [-1, 0, 1]:
    members = [v for v in INNER_VALS if INNER_BASINS[v] == basin]
    s = sum(kw_node_sheng[v] for v in members)
    k = sum(kw_node_ke[v] for v in members)
    print(f"    {BASIN_NAME[basin]:6s}: sheng={s}  ke={k}  net={s-k}")

print("\nDone.")
