"""
05: Dual map — outer trigram space vs inner space side by side.
Shows how the outer walk (fast, free, five-phase-neutral) diverges
from the inner walk (constrained, five-phase-structured).
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kwmapper')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from collections import Counter, defaultdict

from common import *

# ── Outer trigram-pair space: 8×8 = 64 possible, but only 32 used by KW ─────

# Actually, let's map the outer as (lower_trig, upper_trig) → an 8×8 grid
# But that's too large. Instead: map the 8 trigrams as a circle for each of
# lower and upper, or use a single 2D embedding.

# Simpler: both maps use the same structure.
# Inner: 16 nodes (4-bit values), basin-partitioned
# Outer: (lower_trig, upper_trig) pairs — but there are 36 unique pairs in KW.
# Too many. 

# Better approach: show the 8-trigram space for LOWER and UPPER separately,
# or show the walk in inner space vs the walk colored by outer properties.

# Most useful: side-by-side inner walk with five-phase coloring from
# (a) Hu lower (inner) and (b) outer lower — showing the contrast.

inner_pos = inner_layout()

# ── Compute both five-phase colorings ────────────────────────────────────────

inner_edges = []
outer_edges = []

for i in range(63):
    v1, v2 = INNER[i], INNER[i + 1]
    
    # Hu lower five-phase
    hu_rel = trig_phase(HU_LO[i], HU_LO[i + 1])
    hu_pc = phase_class(hu_rel)
    
    # Outer lower five-phase  
    out_rel = trig_phase(LO_TRIG[i], LO_TRIG[i + 1])
    out_pc = phase_class(out_rel)
    
    bridge = 'intra' if i % 2 == 0 else 'inter'
    
    inner_edges.append({'v1': v1, 'v2': v2, 'phase': hu_pc, 'bridge': bridge})
    outer_edges.append({'v1': v1, 'v2': v2, 'phase': out_pc, 'bridge': bridge})

# ── Draw side by side ────────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 10))

for ax, edge_list, title in [
    (ax1, inner_edges, 'Hu Lower Five-Phase\n(inner trigram dynamics)'),
    (ax2, outer_edges, 'Outer Lower Five-Phase\n(surface trigram dynamics)'),
]:
    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Basin regions
    import matplotlib.patches as mpatches
    for basin in [-1, 0, 1]:
        members = [v for v in INNER_VALS if INNER_BASINS[v] == basin]
        xs = [inner_pos[v][0] for v in members]
        ys = [inner_pos[v][1] for v in members]
        margin = 0.6
        rect = mpatches.FancyBboxPatch(
            (min(xs) - margin, min(ys) - margin),
            max(xs) - min(xs) + 2 * margin,
            max(ys) - min(ys) + 2 * margin,
            boxstyle="round,pad=0.2",
            facecolor=BASIN_LIGHT[basin], edgecolor=BASIN_COLOR[basin],
            alpha=0.3, linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(np.mean(xs), max(ys) + margin + 0.3,
                BASIN_NAME[basin], ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=BASIN_COLOR[basin])
    
    # Aggregate edges
    edge_data = defaultdict(lambda: Counter())
    for e in edge_list:
        if e['v1'] == e['v2']:
            continue
        edge_data[(e['v1'], e['v2'])][e['phase']] += 1
    
    drawn = set()
    for (v1, v2), counts in edge_data.items():
        x1, y1 = inner_pos[v1]
        x2, y2 = inner_pos[v2]
        dominant = counts.most_common(1)[0][0]
        total = sum(counts.values())
        color = PHASE_EDGE[dominant]
        lw = 0.8 + total * 0.8
        
        reverse_exists = (v2, v1) in edge_data
        if reverse_exists and (v2, v1) not in drawn:
            curve = 0.15
        elif reverse_exists:
            curve = -0.15
        else:
            curve = 0.05
        
        arrow = FancyArrowPatch(
            (x1, y1), (x2, y2),
            connectionstyle=f"arc3,rad={curve}",
            arrowstyle='->,head_length=5,head_width=3',
            color=color, linewidth=lw, alpha=0.7, zorder=3
        )
        ax.add_patch(arrow)
        drawn.add((v1, v2))
    
    # Nodes
    for v in INNER_VALS:
        x, y = inner_pos[v]
        basin = INNER_BASINS[v]
        ax.scatter(x, y, s=600, c=BASIN_COLOR[basin],
                   edgecolors='white', linewidths=2, zorder=5)
        name = inner_hu_name(v)
        ax.text(x, y + 0.02, name, ha='center', va='center',
                fontsize=6, fontweight='bold', color='white', zorder=6)
    
    # Stats
    n_s = sum(1 for e in edge_list if e['phase'] == 'sheng')
    n_k = sum(1 for e in edge_list if e['phase'] == 'ke')
    n_b = sum(1 for e in edge_list if e['phase'] == 'bi')
    ax.text(0.02, 0.02, f'{n_s} sheng  {n_k} ke  {n_b} bi',
            transform=ax.transAxes, fontsize=9, color='#333333')

# Shared legend
legend_elements = [
    plt.Line2D([0], [0], color=PHASE_EDGE['sheng'], lw=2, label='Sheng (generative)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['ke'], lw=2, label='Ke (destructive)'),
    plt.Line2D([0], [0], color=PHASE_EDGE['bi'], lw=2, label='Bi (same element)'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=10,
           bbox_to_anchor=(0.5, 0.01))

fig.suptitle('Inner vs Outer Five-Phase Dynamics on Inner Hexagram Space',
             fontsize=15, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])

save(fig, '05_dual_map')
plt.close()

# ── Summary stats ────────────────────────────────────────────────────────────

print("\n  Five-phase distribution comparison:")
for label, elist in [("Hu lower (inner)", inner_edges), ("Outer lower", outer_edges)]:
    s = sum(1 for e in elist if e['phase'] == 'sheng')
    k = sum(1 for e in elist if e['phase'] == 'ke')
    b = sum(1 for e in elist if e['phase'] == 'bi')
    print(f"    {label}: {s} sheng  {k} ke  {b} bi")

# Cross-tab: do they agree?
agree = sum(1 for i in range(63) if inner_edges[i]['phase'] == outer_edges[i]['phase'])
print(f"\n  Agreement: {agree}/63 transitions ({100*agree/63:.0f}%)")
print(f"  Expected by chance: ~{100/9*3:.0f}%")

print("\nDone.")
