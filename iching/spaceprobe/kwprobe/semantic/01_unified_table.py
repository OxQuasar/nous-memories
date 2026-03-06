"""
01_unified_table.py — Unified Transition Table

For each of the 31 inter-pair transitions (T1–T31), joins:
  - Algebraic profile (basins, 互, kernels, distances, runs)
  - Semantic profile (from Round 1 Xugua reading)
  - Corridor profile (from Round 2 corridor analysis)

Outputs console table + markdown to 01_unified_table.md
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
from pathlib import Path

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, hamming3, fmt6,
)

# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

# Bottom-to-top bit encoding (matching sequence.py's hex encoding):
# bit 0 = bottom line, bit 2 = top line.
# cycle_algebra.py's TRIGRAM_NAMES uses reversed bit order — we correct here.
TRIGRAM_SHORT = {
    0b000: "Earth", 0b001: "Thndr", 0b010: "Water", 0b011: "Lake",
    0b100: "Mtn",   0b101: "Fire",  0b110: "Wind",  0b111: "Heaven",
}

# Corridor memberships (1-indexed pairs)
PAIR_CORRIDOR = {
    1: 'Heaven', 3: 'Heaven', 5: 'Heaven',
    4: 'Earth', 6: 'Earth', 8: 'Earth', 10: 'Earth',
    9: 'Thun/Mtn', 11: 'Thun/Mtn',
    14: 'Wind', 16: 'Wind',
    27: 'Lake/Wind', 29: 'Lake/Wind',
}

CORRIDORS = {
    'Heaven':    [1, 3, 5],
    'Earth':     [4, 6, 8, 10],
    'Thun/Mtn':  [9, 11],
    'Wind':      [14, 16],
    'Lake/Wind': [27, 29],
}

# Corridor-rich: T1–T16, T26–T29  (from round2-corridors.md)
CORRIDOR_RICH = set(range(1, 17)) | set(range(26, 30))

# Semantic data from Round 1 Xugua reading (Section 7 cross-reference table)
SEMANTIC = {
    1:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'PP'},
    2:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    3:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '⇀', 'level': 'HH'},
    4:  {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    5:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    6:  {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '⇀', 'level': 'HH'},
    7:  {'logic': 'Contrastive', 'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    8:  {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    9:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    10: {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    11: {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    12: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    13: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    14: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    15: {'logic': 'Temporal',    'conf': 'Direct',  'dir': '→', 'level': 'PP'},
    16: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    17: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    18: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    19: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    20: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    21: {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    22: {'logic': 'Causal',      'conf': 'Direct',  'dir': '⇀', 'level': 'HH'},
    23: {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    24: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    25: {'logic': 'Analogical',  'conf': 'Direct',  'dir': '⇀', 'level': 'HH'},
    26: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
    27: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    28: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    29: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    30: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→', 'level': 'HH'},
    31: {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀', 'level': 'HH'},
}


# ═══════════════════════════════════════════════════════════════════════════
# Build KW hexagram data
# ═══════════════════════════════════════════════════════════════════════════

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])


def get_basin(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    if b2 == 1 and b3 == 1: return 'Qian'
    return 'KanLi'


def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])


def corridor_relation(t_num):
    """Corridor relationship for transition T_num (1-indexed)."""
    exit_pair = t_num
    entry_pair = t_num + 1
    exit_corr = PAIR_CORRIDOR.get(exit_pair)
    entry_corr = PAIR_CORRIDOR.get(entry_pair)

    exit_rel = entry_rel = None

    if exit_corr:
        members = CORRIDORS[exit_corr]
        exit_rel = 'TERM_EXIT' if exit_pair == members[-1] else 'LOCAL_EXIT'

    if entry_corr:
        members = CORRIDORS[entry_corr]
        entry_rel = 'INIT_ENTRY' if entry_pair == members[0] else 'RE_ENTRY'

    if exit_rel and entry_rel:
        return f"{exit_rel}+{entry_rel}"
    if exit_rel:
        return exit_rel
    if entry_rel:
        return entry_rel
    if t_num in CORRIDOR_RICH:
        return 'BETWEEN'
    return 'NONE'


# ═══════════════════════════════════════════════════════════════════════════
# Compute basin runs
# ═══════════════════════════════════════════════════════════════════════════

basin_seq = [get_basin(h) for h in kw_hex]

runs = []
run_start = 0
for i in range(1, 64):
    if basin_seq[i] != basin_seq[i - 1]:
        runs.append((run_start, i - 1, basin_seq[run_start]))
        run_start = i
runs.append((run_start, 63, basin_seq[run_start]))

pos_to_run = {}
for r_idx, (start, end, _) in enumerate(runs):
    for pos in range(start, end + 1):
        pos_to_run[pos] = r_idx


# ═══════════════════════════════════════════════════════════════════════════
# Compute all 31 transition profiles
# ═══════════════════════════════════════════════════════════════════════════

transitions = []
for t in range(31):
    exit_idx = 2 * t + 1
    entry_idx = 2 * t + 2
    h1, h2 = kw_hex[exit_idx], kw_hex[entry_idx]

    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    hu1, hu2 = hugua(h1), hugua(h2)
    lo1, up1 = lower_trigram(h1), upper_trigram(h1)
    lo2, up2 = lower_trigram(h2), upper_trigram(h2)
    lo_d, up_d = hamming3(lo1, lo2), hamming3(up1, up2)
    b1, b2 = get_basin(h1), get_basin(h2)

    # Preserving bridge (algebraic)
    if lo_d == 0:
        preserving = f"Lo:{TRIGRAM_SHORT[lo1]}"
    elif up_d == 0:
        preserving = f"Up:{TRIGRAM_SHORT[up1]}"
    else:
        preserving = None

    t_num = t + 1  # 1-indexed

    # Basin run
    exit_run = pos_to_run[exit_idx]
    entry_run = pos_to_run[entry_idx]

    # Semantic
    sem = SEMANTIC[t_num]

    # Corridor
    exit_pair = t_num       # 1-indexed pair
    entry_pair = t_num + 1

    transitions.append({
        'T': t_num,
        'exit_hex': kw_names[exit_idx],
        'entry_hex': kw_names[entry_idx],
        'exit_kw': KING_WEN[exit_idx][0],
        'entry_kw': KING_WEN[entry_idx][0],
        # Algebraic
        'hex_d': hamming6(h1, h2),
        'lo_d': lo_d, 'up_d': up_d,
        'basin_exit': b1, 'basin_entry': b2,
        'basin_cross': b1 != b2,
        'hu_d': hamming6(hu1, hu2),
        'k_name': KERNEL_NAMES[kernel],
        'h_kernel': kernel in H_KERNELS,
        'preserving': preserving,
        'exit_run': exit_run + 1, 'entry_run': entry_run + 1,
        'run_boundary': exit_run != entry_run,
        # Semantic
        'logic': sem['logic'],
        'conf': sem['conf'],
        'dir': sem['dir'],
        'level': sem['level'],
        # Corridor
        'exit_corr': PAIR_CORRIDOR.get(exit_pair, '—'),
        'entry_corr': PAIR_CORRIDOR.get(entry_pair, '—'),
        'corr_rel': corridor_relation(t_num),
        'regime': 'rich' if t_num in CORRIDOR_RICH else 'free',
    })


# ═══════════════════════════════════════════════════════════════════════════
# Console output
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 130)
print("UNIFIED TRANSITION TABLE — 31 Inter-Pair Bridges")
print("=" * 130)
print()

hdr = (f"{'T':>2} {'Bridge':>22} {'d':>2} {'lo':>2} {'up':>2} "
       f"{'Basin':>10} {'×':>1} {'互d':>2} {'Kern':>3} {'H':>1} "
       f"{'Logic':>11} {'Conf':>7} {'→':>1} {'Lv':>2} {'Preserving':>11} "
       f"{'Corridor Rel':>26} {'Reg':>4} {'RB':>2}")
print(hdr)
print("─" * 130)

for tr in transitions:
    bstr = f"{tr['basin_exit'][:3]}→{tr['basin_entry'][:3]}"
    bridge = f"{tr['exit_hex']}→{tr['entry_hex']}"
    cross = 'Y' if tr['basin_cross'] else '·'
    hk = 'Y' if tr['h_kernel'] else '·'
    pres = tr['preserving'] or '—'
    rb = 'Y' if tr['run_boundary'] else '·'

    print(f"{tr['T']:>2} {bridge:>22} {tr['hex_d']:>2} {tr['lo_d']:>2} {tr['up_d']:>2} "
          f"{bstr:>10} {cross:>1} {tr['hu_d']:>2} {tr['k_name']:>3} {hk:>1} "
          f"{tr['logic']:>11} {tr['conf']:>7} {tr['dir']:>1} {tr['level']:>2} {pres:>11} "
          f"{tr['corr_rel']:>26} {tr['regime']:>4} {rb:>2}")


# ═══════════════════════════════════════════════════════════════════════════
# Cross-tabulations
# ═══════════════════════════════════════════════════════════════════════════

def xtab(key1, key2, label, data=transitions, k1_order=None, k2_order=None):
    """Print a cross-tabulation to console."""
    vals1 = k1_order or sorted(set(d[key1] for d in data), key=str)
    vals2 = k2_order or sorted(set(d[key2] for d in data), key=str)

    print(f"\n  {label}")
    hdr = f"  {'':>15}"
    for v2 in vals2:
        hdr += f" {str(v2):>10}"
    hdr += f" {'Total':>6}"
    print(hdr)
    print("  " + "─" * (len(hdr) - 2))

    for v1 in vals1:
        row = f"  {str(v1):>15}"
        rt = 0
        for v2 in vals2:
            c = sum(1 for d in data if d[key1] == v1 and d[key2] == v2)
            row += f" {c:>10}"
            rt += c
        row += f" {rt:>6}"
        print(row)

    row = f"  {'Total':>15}"
    for v2 in vals2:
        c = sum(1 for d in data if d[key2] == v2)
        row += f" {c:>10}"
    row += f" {len(data):>6}"
    print(row)


print("\n" + "=" * 80)
print("CROSS-TABULATIONS")
print("=" * 80)

logic_order = ['Causal', 'Cyclical', 'Contrastive', 'Temporal', 'Analogical']

xtab('basin_cross', 'logic', 'Basin-crossing × Logic type', k2_order=logic_order)
xtab('basin_cross', 'conf', 'Basin-crossing × Confidence')
xtab('basin_cross', 'regime', 'Basin-crossing × Regime')
xtab('h_kernel', 'logic', 'H-kernel × Logic type', k2_order=logic_order)
xtab('h_kernel', 'conf', 'H-kernel × Confidence')

# Simplified corridor rel for cross-tab
corr_cats = []
for tr in transitions:
    r = tr['corr_rel']
    if 'EXIT' in r and 'ENTRY' in r:
        corr_cats.append('CROSS')
    elif 'EXIT' in r:
        corr_cats.append('EXIT')
    elif 'ENTRY' in r:
        corr_cats.append('ENTRY')
    elif r == 'BETWEEN':
        corr_cats.append('BETWEEN')
    else:
        corr_cats.append('NONE')

# Temporarily add simplified category
for tr, cc in zip(transitions, corr_cats):
    tr['_corr_cat'] = cc

xtab('_corr_cat', 'basin_cross', 'Corridor category × Basin-crossing',
     k1_order=['EXIT', 'ENTRY', 'CROSS', 'BETWEEN', 'NONE'])

# 互 distance by regime
print(f"\n  互 distance distribution by regime")
for regime in ['rich', 'free']:
    dists = [tr['hu_d'] for tr in transitions if tr['regime'] == regime]
    dc = Counter(dists)
    mean_d = sum(dists) / len(dists) if dists else 0
    dist_str = ' '.join(f"d{d}={dc.get(d, 0)}" for d in range(7) if dc.get(d, 0))
    print(f"    {regime:>4}: n={len(dists):>2}  mean={mean_d:.2f}  {dist_str}")


# ═══════════════════════════════════════════════════════════════════════════
# Write markdown
# ═══════════════════════════════════════════════════════════════════════════

L = []
w = L.append

w("# Unified Transition Table — 31 Inter-Pair Bridges\n")
w("Each row joins algebraic profile (basin, 互, kernel, distances) with semantic")
w("profile (Xugua logic, confidence, directionality) and corridor profile.\n")

# Column legend
w("## Column Key\n")
w("| Column | Meaning |")
w("|--------|---------|")
w("| T# | Transition number (1–31) |")
w("| Bridge | Exit hex (#) → Entry hex (#) |")
w("| d | Hex Hamming distance |")
w("| lo/up | Lower/upper trigram Hamming distance |")
w("| Basin | Exit basin → Entry basin (Kun/Qian/KanLi) |")
w("| ×? | Basin-crossing (Y/N) |")
w("| 互d | 互 Hamming distance |")
w("| Kern | Mirror kernel (id/O/M/I/OM/OI/MI/OMI) |")
w("| H? | H-kernel member (Y/N) |")
w("| Pres | Preserving bridge: which trigram preserved, or — |")
w("| Logic | Xugua logic type |")
w("| Conf | Xugua confidence (Direct/Implied) |")
w("| Dir | Directionality (→ unidirectional / ⇀ weakly directional) |")
w("| Lvl | Level (PP pair-to-pair / HH hex-to-hex) |")
w("| Corridor | Corridor relationship |")
w("| Regime | Corridor-rich or corridor-free |")
w("| RB | Basin run boundary (Y/N) |")
w("")

# Main table
w("## Main Table\n")
w("| T# | Bridge | d | lo | up | Basin | ×? | 互d | Kern | H? | Pres "
  "| Logic | Conf | Dir | Lvl | Corridor | Reg | RB |")
w("|:--:|--------|:-:|:--:|:--:|-------|:--:|:---:|:----:|:--:|------"
  "|-------|------|:---:|:---:|----------|:---:|:--:|")

for tr in transitions:
    bstr = f"{tr['basin_exit'][:3]}→{tr['basin_entry'][:3]}"
    bridge = f"{tr['exit_hex']}(#{tr['exit_kw']})→{tr['entry_hex']}(#{tr['entry_kw']})"
    cross = '**Y**' if tr['basin_cross'] else 'N'
    hk = '**Y**' if tr['h_kernel'] else 'N'
    pres = tr['preserving'] or '—'
    rb = '**Y**' if tr['run_boundary'] else 'N'
    logic = f"**{tr['logic']}**" if tr['logic'] not in ('Causal',) else tr['logic']

    w(f"| {tr['T']} | {bridge} | {tr['hex_d']} | {tr['lo_d']} | {tr['up_d']} "
      f"| {bstr} | {cross} | {tr['hu_d']} | {tr['k_name']} | {hk} | {pres} "
      f"| {logic} | {tr['conf']} | {tr['dir']} | {tr['level']} "
      f"| {tr['corr_rel']} | {tr['regime']} | {rb} |")

w("")


def md_xtab(key1, key2, label, k1_order=None, k2_order=None, data=transitions):
    """Append a markdown cross-tabulation."""
    vals1 = k1_order or sorted(set(d[key1] for d in data), key=str)
    vals2 = k2_order or sorted(set(d[key2] for d in data), key=str)

    w(f"### {label}\n")
    hdr = "| |"
    sep = "|---|"
    for v2 in vals2:
        hdr += f" {v2} |"
        sep += ":---:|"
    hdr += " Total |"
    sep += ":---:|"
    w(hdr)
    w(sep)

    for v1 in vals1:
        row = f"| **{v1}** |"
        rt = 0
        for v2 in vals2:
            c = sum(1 for d in data if d[key1] == v1 and d[key2] == v2)
            row += f" {c} |"
            rt += c
        row += f" {rt} |"
        w(row)

    total_row = "| **Total** |"
    for v2 in vals2:
        c = sum(1 for d in data if d[key2] == v2)
        total_row += f" **{c}** |"
    total_row += f" **{len(data)}** |"
    w(total_row)
    w("")


w("## Cross-Tabulations\n")

md_xtab('basin_cross', 'logic', 'Basin-crossing × Logic type', k2_order=logic_order)
md_xtab('basin_cross', 'conf', 'Basin-crossing × Confidence')
md_xtab('basin_cross', 'regime', 'Basin-crossing × Regime')
md_xtab('h_kernel', 'logic', 'H-kernel × Logic type', k2_order=logic_order)
md_xtab('h_kernel', 'conf', 'H-kernel × Confidence')
md_xtab('_corr_cat', 'basin_cross', 'Corridor category × Basin-crossing',
        k1_order=['EXIT', 'ENTRY', 'CROSS', 'BETWEEN', 'NONE'])

w("### 互 distance distribution by regime\n")
w("| Regime | d=0 | d=1 | d=2 | d=3 | d=4 | d=5 | d=6 | Mean | n |")
w("|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:----:|:-:|")
for regime in ['rich', 'free']:
    dists = [tr['hu_d'] for tr in transitions if tr['regime'] == regime]
    dc = Counter(dists)
    mean_d = sum(dists) / len(dists) if dists else 0
    row = f"| {regime} |"
    for d in range(7):
        row += f" {dc.get(d, 0)} |"
    row += f" {mean_d:.2f} | {len(dists)} |"
    w(row)
w("")

# Clean up temp key
for tr in transitions:
    del tr['_corr_cat']

out_path = Path(__file__).parent / "01_unified_table.md"
out_path.write_text('\n'.join(L))
print(f"\nMarkdown written to {out_path}")
