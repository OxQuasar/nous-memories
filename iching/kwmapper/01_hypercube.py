"""
01: The 16-node inner space with KW walk traced.
Edges colored by 互 lower five-phase (生/克/比).
Basin-partitioned layout.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kwmapper')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
from collections import Counter, defaultdict

from common import *

pos = inner_layout()

# ── Compute KW walk edges on inner space ─────────────────────────────────────

edges = []
for i in range(63):
    v1 = INNER[i]
    v2 = INNER[i + 1]
    
    # Five-phase on 互 lower
    hu_lo_rel = trig_phase(HU_LO[i], HU_LO[i + 1])
    pclass = phase_class(hu_lo_rel)
    
    bridge = 'intra' if i % 2 == 0 else 'inter'
    
    edges.append({
        'v1': v1, 'v2': v2, 'step': i,
        'phase': pclass, 'phase_rel': hu_lo_rel,
        'bridge': bridge,
        'basin_cross': BASINS[i] != BASINS[i + 1],
    })

# ── Count edge usage ─────────────────────────────────────────────────────────

edge_counts = Counter()
edge_phases = defaultdict(list)
for e in edges:
    key = (e['v1'], e['v2'])
    edge_counts[key] += 1
    edge_phases[key].append(e['phase'])

# ── Draw ─────────────────────────────────────────────────────────────────────

fig, ax = setup_fig('KW Walk in Inner Hexagram Space\n(edges: Hu lower five-phase)', figsize=(14, 9))
draw_basin_regions(ax, pos)

# Draw edges with curvature to handle bidirectional
drawn = set()
for (v1, v2), count in edge_counts.items():
    if v1 == v2:
        continue  # self-loops (inner unchanged)
    
    x1, y1 = pos[v1]
    x2, y2 = pos[v2]
    
    # Dominant phase for this edge
    phases = edge_phases[(v1, v2)]
    phase_counts = Counter(phases)
    dominant = phase_counts.most_common(1)[0][0]
    color = PHASE_EDGE[dominant]
    
    # Width by count
    lw = 0.8 + count * 0.8
    
    # Curvature: offset if reverse edge exists
    reverse_exists = (v2, v1) in edge_counts
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
        color=color, linewidth=lw, alpha=0.7,
        zorder=3
    )
    ax.add_patch(arrow)
    drawn.add((v1, v2))

# Self-loops (inner unchanged = outer-only transitions)
self_loops = Counter(e['v1'] for e in edges if e['v1'] == e['v2'])
for v, count in self_loops.items():
    x, y = pos[v]
    circle = patches.Arc((x, y + 0.35), 0.3, 0.3, angle=0,
                          theta1=0, theta2=300,
                          color='#666666', linewidth=1 + count * 0.5)
    ax.add_patch(circle)
    ax.text(x + 0.2, y + 0.45, f'×{count}', fontsize=6, color='#666666')

draw_nodes(ax, pos, node_size=700)

# Visit counts per node
visit_counts = Counter(INNER)
for v in INNER_VALS:
    x, y = pos[v]
    ax.text(x, y - 0.55, f'n={visit_counts[v]}', ha='center', va='top',
            fontsize=6, color='#666666')

# Legend
legend_elements = [
    plt.Line2D([0], [0], color=PHASE_EDGE['sheng'], lw=2, label='Sheng (generative)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['ke'], lw=2, label='Ke (destructive)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['bi'], lw=2, label='Bi (same element)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

# Stats annotation
n_sheng = sum(1 for e in edges if e['phase'] == 'sheng')
n_ke = sum(1 for e in edges if e['phase'] == 'ke')
n_bi = sum(1 for e in edges if e['phase'] == 'bi')
ax.text(0.02, 0.02, f'63 transitions: {n_sheng} sheng  {n_ke} ke  {n_bi} bi',
        transform=ax.transAxes, fontsize=9, color='#333333')

save(fig, '01_hypercube')
plt.close()

# ── Also make intra/inter split version ──────────────────────────────────────

for bridge_type in ['intra', 'inter']:
    fig, ax = setup_fig(f'KW Walk — {bridge_type.upper()}-pair bridges\n(Hu lower five-phase)',
                        figsize=(14, 9))
    draw_basin_regions(ax, pos)
    
    sub_edges = [e for e in edges if e['bridge'] == bridge_type]
    sub_counts = Counter()
    sub_phases = defaultdict(list)
    for e in sub_edges:
        key = (e['v1'], e['v2'])
        sub_counts[key] += 1
        sub_phases[key].append(e['phase'])
    
    drawn = set()
    for (v1, v2), count in sub_counts.items():
        if v1 == v2:
            continue
        x1, y1 = pos[v1]
        x2, y2 = pos[v2]
        phases = sub_phases[(v1, v2)]
        dominant = Counter(phases).most_common(1)[0][0]
        color = PHASE_EDGE[dominant]
        lw = 0.8 + count * 1.0
        
        reverse_exists = (v2, v1) in sub_counts
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
    
    # Self-loops
    sub_self = Counter(e['v1'] for e in sub_edges if e['v1'] == e['v2'])
    for v, count in sub_self.items():
        x, y = pos[v]
        circle = patches.Arc((x, y + 0.35), 0.3, 0.3, angle=0,
                              theta1=0, theta2=300,
                              color='#666666', linewidth=1 + count * 0.5)
        ax.add_patch(circle)
        ax.text(x + 0.2, y + 0.45, f'×{count}', fontsize=6, color='#666666')
    
    draw_nodes(ax, pos, node_size=700)
    
    n_s = sum(1 for e in sub_edges if e['phase'] == 'sheng')
    n_k = sum(1 for e in sub_edges if e['phase'] == 'ke')
    n_b = sum(1 for e in sub_edges if e['phase'] == 'bi')
    n_total = len(sub_edges)
    ax.text(0.02, 0.02, f'{n_total} {bridge_type}: {n_s} sheng  {n_k} ke  {n_b} bi',
            transform=ax.transAxes, fontsize=9, color='#333333')
    
    legend_elements = [
        plt.Line2D([0], [0], color=PHASE_EDGE['sheng'], lw=2, label='Sheng (generative)'),
        plt.Line2D([0], [0], color=PHASE_EDGE['ke'], lw=2, label='Ke (destructive)'),
        plt.Line2D([0], [0], color=PHASE_EDGE['bi'], lw=2, label='Bi (same element)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    save(fig, f'01_{bridge_type}')
    plt.close()

print("Done.")
