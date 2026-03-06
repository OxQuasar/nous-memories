"""
Shared infrastructure for KW inner-space mapping.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

import numpy as np
from collections import defaultdict

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    TRIGRAM_ELEMENT, five_phase_relation,
)

# ── Constants ────────────────────────────────────────────────────────────────

BASIN_COLOR = {-1: '#4488CC', 0: '#44AA66', 1: '#CC4444'}  # Kun, KanLi, Qian
BASIN_LIGHT = {-1: '#AACCEE', 0: '#AADDBB', 1: '#EEAAAA'}
BASIN_SYM = {-1: '○', 0: '◎', 1: '●'}
BASIN_NAME = {-1: 'Kun', 0: 'KanLi', 1: 'Qian'}

PHASE_COLOR = {'sheng': '#22AA44', 'ke': '#CC3333', 'bi': '#999999'}
PHASE_EDGE = {'sheng': '#22AA44', 'ke': '#CC3333', 'bi': '#AAAAAA'}

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

# ── KW sequence data ────────────────────────────────────────────────────────

KW_HEX = []
KW_NAMES = []
KW_NUMBERS = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    KW_HEX.append(sum(b[j] << j for j in range(6)))
    KW_NAMES.append(KING_WEN[i][1])
    KW_NUMBERS.append(KING_WEN[i][0])

# Precomputed per-position
LO_TRIG = [lower_trigram(h) for h in KW_HEX]
UP_TRIG = [upper_trigram(h) for h in KW_HEX]
HU_VAL = [hugua(h) for h in KW_HEX]
HU_LO = [lower_trigram(v) for v in HU_VAL]
HU_UP = [upper_trigram(v) for v in HU_VAL]
INNER = [(h >> 1) & 0xF for h in KW_HEX]
OUTER = [(h & 1) | (((h >> 5) & 1) << 1) for h in KW_HEX]

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    elif b2 == 1 and b3 == 1: return 1
    else: return 0

BASINS = [get_basin(h) for h in KW_HEX]

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

def trig_phase(t1, t2):
    return five_phase_relation(TRIGRAM_ELEMENT[t1], TRIGRAM_ELEMENT[t2])

def phase_class(rel):
    if rel in ('生体', '体生用'): return 'sheng'
    elif rel in ('克体', '体克用'): return 'ke'
    else: return 'bi'

# ── Inner space: 16 nodes ───────────────────────────────────────────────────

def inner_to_bits(v):
    """4-bit inner value → (h1, h2, h3, h4)."""
    return ((v >> 0) & 1, (v >> 1) & 1, (v >> 2) & 1, (v >> 3) & 1)

def inner_basin(v):
    """Basin of an inner 4-bit value."""
    h2 = (v >> 1) & 1
    h3 = (v >> 2) & 1
    if h2 == 0 and h3 == 0: return -1
    elif h2 == 1 and h3 == 1: return 1
    else: return 0

def inner_hu_name(v):
    """互 trigram pair name for inner 4-bit value."""
    # Reconstruct 互 hexagram from inner bits
    h1, h2, h3, h4 = inner_to_bits(v)
    hu = h1 | (h2 << 1) | (h3 << 2) | (h2 << 3) | (h3 << 4) | (h4 << 5)
    lo = TRIGRAM_NAMES[lower_trigram(hu)]
    up = TRIGRAM_NAMES[upper_trigram(hu)]
    # Short names
    short = {'Kun ☷': 'Kun', 'Gen ☶': 'Gen', 'Kan ☵': 'Kan', 'Xun ☴': 'Xun',
             'Zhen ☳': 'Zhe', 'Li ☲': 'Li', 'Dui ☱': 'Dui', 'Qian ☰': 'Qia'}
    lo_s = short.get(lo, lo[:3])
    up_s = short.get(up, up[:3])
    return f"{lo_s}/{up_s}"

# All 16 inner values
INNER_VALS = list(range(16))
INNER_BASINS = {v: inner_basin(v) for v in INNER_VALS}

# ── Basin-natural layout ────────────────────────────────────────────────────

def inner_layout():
    """
    Basin-natural 2D coordinates for 16 inner values.
    
    Horizontal: basin (Kun left, KanLi center, Qian right)
    Vertical: wing bits (h1, h4) spread within basin
    
    Returns dict: inner_val → (x, y)
    """
    pos = {}
    
    # Group by basin
    by_basin = defaultdict(list)
    for v in INNER_VALS:
        by_basin[inner_basin(v)].append(v)
    
    # Basin x-centers
    basin_x = {-1: 0.0, 0: 2.5, 1: 5.0}
    
    for basin, members in by_basin.items():
        cx = basin_x[basin]
        n = len(members)
        # Sort by wing bits (h1, h4) for consistent vertical ordering
        members.sort(key=lambda v: (inner_to_bits(v)[3], inner_to_bits(v)[0]))
        
        if basin == 0:  # KanLi has 8 members — 2 columns of 4
            # Split by interface sub-type: (0,1) vs (1,0)
            col_01 = [v for v in members if inner_to_bits(v)[1:3] == (0, 1)]
            col_10 = [v for v in members if inner_to_bits(v)[1:3] == (1, 0)]
            for i, v in enumerate(col_01):
                pos[v] = (cx - 0.4, i * 1.0)
            for i, v in enumerate(col_10):
                pos[v] = (cx + 0.4, i * 1.0)
        else:  # Kun and Qian have 4 members — single column
            for i, v in enumerate(members):
                pos[v] = (cx, i * 1.0 + 0.5)  # center vertically
        
    return pos

# ── Figure setup ────────────────────────────────────────────────────────────

def setup_fig(title, figsize=(14, 8)):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax

def draw_basin_regions(ax, pos):
    """Draw light background rectangles for each basin."""
    import matplotlib.patches as patches
    
    for basin in [-1, 0, 1]:
        members = [v for v in INNER_VALS if INNER_BASINS[v] == basin]
        xs = [pos[v][0] for v in members]
        ys = [pos[v][1] for v in members]
        
        margin = 0.6
        rect = patches.FancyBboxPatch(
            (min(xs) - margin, min(ys) - margin),
            max(xs) - min(xs) + 2 * margin,
            max(ys) - min(ys) + 2 * margin,
            boxstyle="round,pad=0.2",
            facecolor=BASIN_LIGHT[basin],
            edgecolor=BASIN_COLOR[basin],
            alpha=0.3, linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Basin label
        ax.text(np.mean(xs), max(ys) + margin + 0.3,
                BASIN_NAME[basin], ha='center', va='bottom',
                fontsize=11, fontweight='bold', color=BASIN_COLOR[basin])

def draw_nodes(ax, pos, node_size=600, labels=True):
    """Draw the 16 inner-value nodes."""
    for v in INNER_VALS:
        x, y = pos[v]
        basin = INNER_BASINS[v]
        ax.scatter(x, y, s=node_size, c=BASIN_COLOR[basin],
                   edgecolors='white', linewidths=2, zorder=5)
        
        if labels:
            name = inner_hu_name(v)
            bits = format(v, '04b')
            ax.text(x, y + 0.02, name, ha='center', va='center',
                    fontsize=7, fontweight='bold', color='white', zorder=6)
            ax.text(x, y - 0.35, bits, ha='center', va='top',
                    fontsize=6, color='#333333', zorder=6,
                    fontfamily='monospace')

def save(fig, name, folder='/home/quasar/nous/memories/iching/kwmapper'):
    import os
    fig.savefig(os.path.join(folder, f'{name}.png'), dpi=150, bbox_inches='tight')
    fig.savefig(os.path.join(folder, f'{name}.svg'), bbox_inches='tight')
    print(f"  Saved {name}.png and {name}.svg")
