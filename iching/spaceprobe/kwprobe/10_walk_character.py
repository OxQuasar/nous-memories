"""
Characterize the nature of KW's walk through basin space.

Not statistics — the sequential logic. What kind of walk is this?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, reverse6,
    hamming6, fmt6, fmt3,
)

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    elif b2 == 1 and b3 == 1: return 'Qian'
    else: return 'KanLi'

sym = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}
basins = [get_basin(kw_hex[i]) for i in range(64)]

# ══════════════════════════════════════════════════════════════════════════════
# 1. THE RUN-LEVEL SEQUENCE — THE WALK'S SKELETON
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. RUN-LEVEL SEQUENCE")
print("=" * 70)

runs = []
current = basins[0]
count = 1
start = 0
for i in range(1, 64):
    if basins[i] == current:
        count += 1
    else:
        runs.append((current, count, start, i-1))
        current = basins[i]
        count = 1
        start = i
runs.append((current, count, start, 63))

print(f"\n  {len(runs)} runs:")
for basin, length, s, e in runs:
    canon = "UC" if s < 30 else ("UC→LC" if s < 30 and e >= 30 else "LC")
    if e < 30: canon = "UC"
    elif s >= 30: canon = "LC"
    else: canon = "cross"
    print(f"    {sym[basin]} {basin:6s} ×{length} (#{s+1}-{e+1}) [{canon}]")

# The run-level basin sequence (just the basin, ignoring length)
run_basins = [b for b, l, s, e in runs]
run_str = ''.join(sym[b] for b in run_basins)
print(f"\n  Run-level sequence: {run_str}")
print(f"  Length: {len(run_basins)}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. TRANSITION GRAMMAR — WHAT FOLLOWS WHAT?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. TRANSITION GRAMMAR")
print("=" * 70)

# At run level, what transitions occur?
run_trans = Counter()
for i in range(len(run_basins) - 1):
    run_trans[(run_basins[i], run_basins[i+1])] += 1

print(f"\n  Run-level transitions:")
for (a, b), c in sorted(run_trans.items(), key=lambda x: -x[1]):
    print(f"    {sym[a]}{a:6s} → {sym[b]}{b:6s}: {c}")

# The grammar: KanLi connects, Kun and Qian are endpoints
# KanLi→Kun: 5, KanLi→Qian: 7
# Kun→KanLi: 6, Qian→KanLi: 5
# Kun→Qian: 2 (direct!), Qian→Kun: 1 (direct!)

# Which are the direct Kun↔Qian transitions at run level?
print(f"\n  Direct Kun↔Qian transitions at run level:")
for i in range(len(run_basins) - 1):
    a, b = run_basins[i], run_basins[i+1]
    if {a, b} == {'Kun', 'Qian'}:
        _, _, s1, e1 = runs[i]
        _, _, s2, e2 = runs[i+1]
        print(f"    Run {i}→{i+1}: {sym[a]}(#{s1+1}-{e1+1}) → {sym[b]}(#{s2+1}-{e2+1})")

# ══════════════════════════════════════════════════════════════════════════════
# 3. THE OSCILLATION PATTERN — POLE + CENTER
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. THE OSCILLATION PATTERN")
print("=" * 70)

# Key insight: the walk mostly oscillates between a "pole" (Kun or Qian) 
# and the "center" (KanLi). KanLi mediates.
# Track which pole the walk is oscillating with.

print(f"\n  Walk decomposed as pole↔center oscillation:")
last_pole = None
oscillation_log = []
for i, (basin, length, s, e) in enumerate(runs):
    if basin in ('Kun', 'Qian'):
        last_pole = basin
        pole_sym = sym[basin]
        oscillation_log.append(('pole', basin, length, s, e))
    else:
        # KanLi run — which pole is it between?
        # Look at prev and next non-KanLi
        prev_pole = None
        next_pole = None
        for j in range(i-1, -1, -1):
            if run_basins[j] != 'KanLi':
                prev_pole = run_basins[j]
                break
        for j in range(i+1, len(run_basins)):
            if run_basins[j] != 'KanLi':
                next_pole = run_basins[j]
                break
        oscillation_log.append(('center', basin, length, s, e, prev_pole, next_pole))

for entry in oscillation_log:
    if entry[0] == 'pole':
        _, basin, length, s, e = entry
        canon = "UC" if e < 30 else "LC"
        print(f"    POLE  {sym[basin]} ×{length:2d} (#{s+1:2d}-{e+1:2d}) [{canon}]")
    else:
        _, basin, length, s, e, prev_p, next_p = entry
        bridge = f"{sym.get(prev_p,'?')}↔{sym.get(next_p,'?')}" if prev_p and next_p else "edge"
        canon = "UC" if e < 30 else "LC"
        print(f"    LINK  ◎ ×{length:2d} (#{s+1:2d}-{e+1:2d}) [{canon}] bridging {bridge}")

# Count: how many KanLi runs bridge same-pole vs different-pole?
same_pole = 0
diff_pole = 0
for entry in oscillation_log:
    if entry[0] == 'center':
        _, _, _, _, _, prev_p, next_p = entry
        if prev_p and next_p:
            if prev_p == next_p:
                same_pole += 1
            else:
                diff_pole += 1

print(f"\n  KanLi links bridging same pole: {same_pole}")
print(f"  KanLi links bridging different poles: {diff_pole}")
print(f"  → KanLi mostly bridges {'same pole (returning)' if same_pole > diff_pole else 'different poles (transitioning)'}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. THE POLE SEQUENCE — STRIPPING KanLi
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. THE POLE SEQUENCE (KanLi removed)")
print("=" * 70)

# If we remove all KanLi runs, what's the pole-only sequence?
poles = [(b, l, s, e) for b, l, s, e in runs if b != 'KanLi']
pole_str = ''.join(sym[b] for b, l, s, e in poles)
print(f"\n  Pole sequence: {pole_str}")
print(f"  Length: {len(poles)} pole runs")

# Run-level of pole sequence
pole_run_basins = [b for b, l, s, e in poles]
pole_trans = Counter()
for i in range(len(pole_run_basins) - 1):
    pole_trans[(pole_run_basins[i], pole_run_basins[i+1])] += 1

print(f"\n  Pole transition matrix:")
for (a, b), c in sorted(pole_trans.items()):
    print(f"    {sym[a]} → {sym[b]}: {c}")

# Where does the pole switch from Kun-dominated to Qian-dominated?
print(f"\n  Pole sequence with positions:")
running_kun = 0
running_qian = 0
for b, l, s, e in poles:
    if b == 'Kun': running_kun += l
    else: running_qian += l
    canon = "UC" if e < 30 else "LC"
    print(f"    {sym[b]} ×{l} (#{s+1}-{e+1}) [{canon}]  cumulative: ○={running_kun} ●={running_qian}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE DUAL VIEW — EACH HEXAGRAM IN FACING-SPACE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. THE FACING-SPACE WALK (4 states)")
print("=" * 70)

# Each hexagram has a 2-bit facing signature: (lower_facing, upper_facing)
# This gives 4 states, more refined than the 3 basins

def get_facing(h):
    b2 = (h >> 2) & 1  # top of lower = lower's facing
    b3 = (h >> 3) & 1  # bottom of upper = upper's facing
    return (b2, b3)

facing_names = {
    (0,0): '○○', (0,1): '○●', (1,0): '●○', (1,1): '●●'
}
facing_basins = {
    (0,0): 'Kun', (0,1): 'KanLi', (1,0): 'KanLi', (1,1): 'Qian'
}

kw_facings = [get_facing(kw_hex[i]) for i in range(64)]
facing_str = ' '.join(facing_names[f] for f in kw_facings)

print(f"\n  Facing sequence (64 hexagrams, 4 states):")
# Print in rows of 16
for row in range(4):
    start = row * 16
    end = start + 16
    row_str = ' '.join(f"{facing_names[kw_facings[i]]}" for i in range(start, end))
    positions = f"#{start+1:2d}-#{end:2d}"
    print(f"    {positions}: {row_str}")

# Run-level of facing sequence
facing_runs = []
current = kw_facings[0]
count = 1
start = 0
for i in range(1, 64):
    if kw_facings[i] == current:
        count += 1
    else:
        facing_runs.append((current, count, start))
        current = kw_facings[i]
        count = 1
        start = i
facing_runs.append((current, count, start))

print(f"\n  Facing runs: {len(facing_runs)}")
for f, l, s in facing_runs:
    print(f"    {facing_names[f]} ×{l} (#{s+1})")

# Facing transitions
facing_trans = Counter()
for i in range(63):
    facing_trans[(kw_facings[i], kw_facings[i+1])] += 1

print(f"\n  Facing transition matrix:")
for f1 in [(0,0), (0,1), (1,0), (1,1)]:
    row = []
    for f2 in [(0,0), (0,1), (1,0), (1,1)]:
        c = facing_trans.get((f1, f2), 0)
        row.append(f"{c:3d}")
    print(f"    {facing_names[f1]} → [{' '.join(row)}]  (○○ ○● ●○ ●●)")

# ══════════════════════════════════════════════════════════════════════════════
# 6. THE ○● ↔ ●○ ALTERNATION WITHIN KanLi
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. KanLi INTERNAL STRUCTURE — ○● vs ●○ ALTERNATION")
print("=" * 70)

# Within the KanLi basin, there are two sub-types: ○● and ●○
# Do they alternate? Stay the same?

kanli_sub = [(i, kw_facings[i]) for i in range(64) if basins[i] == 'KanLi']
print(f"\n  KanLi sub-type sequence ({len(kanli_sub)} hexagrams):")

for i, (pos, f) in enumerate(kanli_sub):
    name = kw_names[pos]
    lo = TRIGRAM_NAMES[lower_trigram(kw_hex[pos])]
    up = TRIGRAM_NAMES[upper_trigram(kw_hex[pos])]
    print(f"    {facing_names[f]} #{pos+1:2d} {name:12s} ({lo}/{up})")

# Count ○● vs ●○
sub_counts = Counter(f for _, f in kanli_sub)
print(f"\n  ○● count: {sub_counts.get((0,1), 0)}")
print(f"  ●○ count: {sub_counts.get((1,0), 0)}")

# Do consecutive KanLi hexagrams alternate?
kanli_positions = [pos for pos, f in kanli_sub]
alternations = 0
same = 0
for i in range(len(kanli_sub) - 1):
    pos1, f1 = kanli_sub[i]
    pos2, f2 = kanli_sub[i+1]
    if pos2 == pos1 + 1:  # Actually consecutive in KW
        if f1 != f2:
            alternations += 1
        else:
            same += 1

print(f"\n  Consecutive KanLi hexagrams:")
print(f"    Alternating (○●↔●○): {alternations}")
print(f"    Same sub-type: {same}")

# 互 swaps the facing: (0,1)↔(1,0). So within a KanLi pair:
# pair member 1 has facing (a,b), pair member 2 has facing...
# If reverse pair: facing swaps → (b,a). So ○●↔●○ within pair.
# If complement pair: facing flips → but KanLi complement pairs are both KanLi
# with (0,1)→(1,0) and (1,0)→(0,1).

print(f"\n  Within KW pairs (both members KanLi):")
for i in range(0, 64, 2):
    if basins[i] == 'KanLi' and basins[i+1] == 'KanLi':
        f1, f2 = kw_facings[i], kw_facings[i+1]
        rel = "alternate" if f1 != f2 else "same"
        print(f"    Pair {i//2:2d}: {facing_names[f1]}→{facing_names[f2]} ({rel})")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE WALK AS A BREATHING PATTERN
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. THE WALK AS BREATHING — POLE OSCILLATION OVER TIME")
print("=" * 70)

# Assign a "polarity" value to each position:
# Kun = -1, KanLi = 0, Qian = +1
polarity = {'Kun': -1, 'KanLi': 0, 'Qian': 1}
kw_polarity = [polarity[b] for b in basins]

# Running average (window of 8)
window = 8
running_avg = []
for i in range(64 - window + 1):
    avg = np.mean(kw_polarity[i:i+window])
    running_avg.append(avg)

print(f"\n  Polarity score (Kun=-1, KanLi=0, Qian=+1):")
print(f"  Raw: {kw_polarity}")

# ASCII plot of running average
print(f"\n  Running average (window={window}):")
for i, avg in enumerate(running_avg):
    bar_pos = int((avg + 1) * 20)  # 0-40 range
    bar = ' ' * bar_pos + '█'
    canon = "UC" if i + window//2 < 30 else "LC"
    print(f"    #{i+1:2d}-{i+window:2d} [{canon}]: {'○' if avg < -0.3 else '●' if avg > 0.3 else '◎'} {avg:+.2f} |{'─' * 20}{'│'}{'─' * 20}|")

# Zero crossings
crossings = 0
for i in range(len(running_avg) - 1):
    if running_avg[i] * running_avg[i+1] < 0:
        crossings += 1

print(f"\n  Zero crossings of running average: {crossings}")
print(f"  (Points where the polarity flips from Kun-dominated to Qian-dominated)")

# The UC/LC means
uc_mean = np.mean(kw_polarity[:30])
lc_mean = np.mean(kw_polarity[30:])
print(f"\n  Mean polarity: UC={uc_mean:.3f}, LC={lc_mean:.3f}")
print(f"  The walk breathes from yin ({uc_mean:.2f}) to yang ({lc_mean:.2f})")

# ══════════════════════════════════════════════════════════════════════════════
# 8. THE WALK AT PAIR LEVEL — REDUCED DESCRIPTION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. THE PAIR-LEVEL WALK (32 steps)")
print("=" * 70)

# Each pair is either pure-basin or cross-basin
pair_data = []
for i in range(0, 64, 2):
    b1, b2 = basins[i], basins[i+1]
    f1, f2 = kw_facings[i], kw_facings[i+1]
    if b1 == b2:
        pair_data.append(('pure', b1, f1, f2))
    else:
        pair_data.append(('cross', f'{b1}/{b2}', f1, f2))

# Pair-level walk as basin sequence
pair_basins = [b if t == 'pure' else '×' for t, b, f1, f2 in pair_data]
pair_str = ''.join(sym.get(b, '×') for b in pair_basins)
print(f"\n  Pair basin sequence: {pair_str}")
print(f"  UC pairs (0-14): {pair_str[:15]}")
print(f"  LC pairs (15-31): {pair_str[15:]}")

# Can we describe this as a simple pattern?
# UC: ○ ○ ◎ ○ ◎ ◎ ● ◎ ◎ ○ ◎ ○ ◎ × × 
# LC: ● ● ◎ ◎ ◎ ○ ● ◎ ◎ ● ◎ ◎ ● ◎ ○ × ◎

# ══════════════════════════════════════════════════════════════════════════════
# 9. SUMMARY: THE CHARACTER OF THE WALK
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. SUMMARY: CHARACTER OF THE WALK")
print("=" * 70)

print(f"""
  THE WALK HAS THREE LAYERS:

  Layer 1 — BASIN BREATHING:
    The walk oscillates between a "pole" (Kun or Qian) and the "center" (KanLi).
    UC phase: pole = Kun (mean polarity = {uc_mean:.2f})
    LC phase: pole = Qian (mean polarity = {lc_mean:.2f})
    The pole shifts from yin to yang across the sequence.
    
  Layer 2 — KanLi MEDIATES:
    KanLi is the bridge basin. {same_pole} KanLi runs bridge same-pole (returning),
    {diff_pole} bridge different poles (transitioning).
    Direct Kun↔Qian transitions are rare (3 at run level).
    The walk mostly breathes: pole → center → pole → center
    
  Layer 3 — FACING ALTERNATION:
    Within KanLi, the sub-types ○● and ●○ alternate within pairs (reverse swaps them).
    ○● count: {sub_counts.get((0,1), 0)}, ●○ count: {sub_counts.get((1,0), 0)}
    
  THE NARRATIVE:
    Opens at ● (Qian/heaven) — the yang fixed point
    Descends into ○ (Kun) — the UC's home pole
    Breathes between ○ and ◎ through the Upper Canon
    Crosses through ×× (skeleton pairs) at the canon break
    Rises into ● (Qian) — the LC's home pole  
    Breathes between ● and ◎ through the Lower Canon
    Descends to ○ before the final ◎◎ (JiJi/WeiJi)
    Ends on the oscillation — the process never resolves
""")
