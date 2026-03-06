"""
03: Kernel components on inner space.
Show I-component as the sheng/ke boundary.
H-kernel vs non-H at bridges.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kwmapper')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from collections import Counter, defaultdict

from common import *

pos = inner_layout()

# ── Compute transitions with kernel info ─────────────────────────────────────

edges = []
for i in range(63):
    h1, h2 = KW_HEX[i], KW_HEX[i + 1]
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    kname = KERNEL_NAMES[kernel]
    in_H = kernel in H_KERNELS
    I_comp = kernel[2]
    
    v1, v2 = INNER[i], INNER[i + 1]
    
    hu_up_rel = trig_phase(HU_UP[i], HU_UP[i + 1])
    pclass = phase_class(hu_up_rel)
    bridge = 'intra' if i % 2 == 0 else 'inter'
    
    edges.append({
        'v1': v1, 'v2': v2, 'step': i,
        'kernel': kernel, 'kname': kname,
        'in_H': in_H, 'I': I_comp,
        'phase': pclass, 'bridge': bridge,
    })

# ── Plot 1: I-component as sheng/ke boundary ────────────────────────────────

fig, ax = setup_fig('Kernel I-Component and Five-Phase\nI=0 (thin/blue) vs I=1 (thick/orange)', 
                    figsize=(14, 9))
draw_basin_regions(ax, pos)

edge_data = defaultdict(list)
for e in edges:
    if e['v1'] == e['v2']:
        continue
    edge_data[(e['v1'], e['v2'])].append(e)

drawn = set()
for (v1, v2), elist in edge_data.items():
    x1, y1 = pos[v1]
    x2, y2 = pos[v2]
    
    # Dominant I value
    i_vals = [e['I'] for e in elist]
    dominant_I = 1 if sum(i_vals) > len(i_vals) / 2 else 0
    count = len(elist)
    
    color = '#CC6600' if dominant_I else '#3366CC'
    lw = (1.0 + count * 0.6) * (1.5 if dominant_I else 0.8)
    
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
        arrowstyle='->,head_length=6,head_width=4',
        color=color, linewidth=lw, alpha=0.7, zorder=3
    )
    ax.add_patch(arrow)
    drawn.add((v1, v2))

draw_nodes(ax, pos, node_size=700)

# Add phase annotations to nodes
for v in INNER_VALS:
    x, y = pos[v]
    incoming = [e for e in edges if e['v2'] == v and e['v1'] != v]
    i0_sheng = sum(1 for e in incoming if e['I'] == 0 and e['phase'] == 'sheng')
    i0_ke = sum(1 for e in incoming if e['I'] == 0 and e['phase'] == 'ke')
    i1_sheng = sum(1 for e in incoming if e['I'] == 1 and e['phase'] == 'sheng')
    i1_ke = sum(1 for e in incoming if e['I'] == 1 and e['phase'] == 'ke')
    ax.text(x, y - 0.55, f'I=0:{i0_sheng}S/{i0_ke}K  I=1:{i1_sheng}S/{i1_ke}K',
            ha='center', va='top', fontsize=5, color='#444444')

legend_elements = [
    plt.Line2D([0], [0], color='#3366CC', lw=1.5, label='I=0 (basin preserved)'),
    plt.Line2D([0], [0], color='#CC6600', lw=3, label='I=1 (basin crossing)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

# Stats
i0_edges = [e for e in edges if e['I'] == 0 and e['v1'] != e['v2']]
i1_edges = [e for e in edges if e['I'] == 1 and e['v1'] != e['v2']]
i0_s = sum(1 for e in i0_edges if e['phase'] == 'sheng')
i0_k = sum(1 for e in i0_edges if e['phase'] == 'ke')
i1_s = sum(1 for e in i1_edges if e['phase'] == 'sheng')
i1_k = sum(1 for e in i1_edges if e['phase'] == 'ke')
ax.text(0.02, 0.06,
        f'I=0: {i0_s} sheng, {i0_k} ke (of {len(i0_edges)})\n'
        f'I=1: {i1_s} sheng, {i1_k} ke (of {len(i1_edges)})',
        transform=ax.transAxes, fontsize=8, color='#333333',
        fontfamily='monospace')

save(fig, '03_kernel_I')
plt.close()

# ── Plot 2: H-kernel vs non-H ───────────────────────────────────────────────

fig, ax = setup_fig('H-Kernel (diagonal lift) vs non-H at KW Bridges',
                    figsize=(14, 9))
draw_basin_regions(ax, pos)

drawn = set()
for (v1, v2), elist in edge_data.items():
    x1, y1 = pos[v1]
    x2, y2 = pos[v2]
    
    h_count = sum(1 for e in elist if e['in_H'])
    non_h_count = len(elist) - h_count
    dominant_H = h_count >= non_h_count
    count = len(elist)
    
    color = '#3366CC' if dominant_H else '#CC6600'
    lw = 0.8 + count * 0.8
    style = '-' if dominant_H else '--'
    
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
        arrowstyle='->,head_length=6,head_width=4',
        color=color, linewidth=lw, alpha=0.7, zorder=3,
        linestyle=style,
    )
    ax.add_patch(arrow)
    drawn.add((v1, v2))

draw_nodes(ax, pos, node_size=700)

legend_elements = [
    plt.Line2D([0], [0], color='#3366CC', lw=2, label='H-kernel (diagonal lift)'),
    plt.Line2D([0], [0], color='#CC6600', lw=2, linestyle='--', label='non-H (cross-talk)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

h_total = sum(1 for e in edges if e['in_H'] and e['v1'] != e['v2'])
nh_total = sum(1 for e in edges if not e['in_H'] and e['v1'] != e['v2'])
ax.text(0.02, 0.02, f'H-kernel: {h_total}  non-H: {nh_total}',
        transform=ax.transAxes, fontsize=9, color='#333333')

save(fig, '03_kernel_H')
plt.close()

# ── Print summary ────────────────────────────────────────────────────────────

print("\n  I-component × five-phase (Hu upper, non-self transitions):")
for I_val in [0, 1]:
    sub = [e for e in edges if e['I'] == I_val and e['v1'] != e['v2']]
    s = sum(1 for e in sub if e['phase'] == 'sheng')
    k = sum(1 for e in sub if e['phase'] == 'ke')
    b = sum(1 for e in sub if e['phase'] == 'bi')
    print(f"    I={I_val}: {s} sheng  {k} ke  {b} bi  (total {len(sub)})")

print("\n  I-component × bridge type:")
for I_val in [0, 1]:
    for bt in ['intra', 'inter']:
        sub = [e for e in edges if e['I'] == I_val and e['bridge'] == bt and e['v1'] != e['v2']]
        s = sum(1 for e in sub if e['phase'] == 'sheng')
        k = sum(1 for e in sub if e['phase'] == 'ke')
        print(f"    I={I_val} {bt}: {s} sheng  {k} ke  (total {len(sub)})")

print("\nDone.")
