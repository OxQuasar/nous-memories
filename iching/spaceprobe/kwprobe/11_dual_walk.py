"""
Compare the full hexagram walk with its 互 projection.

The full walk: 64 steps through 6-bit space
The 互 walk: 64 steps through 4-bit (inner) space  
The outer walk: 64 steps through 2-bit (outer) space
The basin walk: 64 steps through 1-bit (interface) space

How do these relate? Are inner and outer changes correlated?
Does the 互 walk have simpler structure than the full walk?
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
    reverse6, hamming6, fmt6,
)

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

def get_inner(h):
    """Inner 4 bits (1,2,3,4) — determines 互"""
    return (h >> 1) & 0xF

def get_outer(h):
    """Outer 2 bits (0,5)"""
    return (h & 1) | (((h >> 5) & 1) << 1)

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    elif b2 == 1 and b3 == 1: return 'Qian'
    else: return 'KanLi'

sym = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}

# ══════════════════════════════════════════════════════════════════════════════
# 1. DECOMPOSE EACH STEP
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. FULL WALK DECOMPOSED: INNER + OUTER AT EACH STEP")
print("=" * 70)

outer_names = {0: '○○', 1: '●○', 2: '○●', 3: '●●'}

print(f"\n  {'#':>3s} {'Name':>12s} {'Hex':>8s} {'Inner':>6s} {'Outer':>6s} {'Basin':>6s} {'互':>8s}")
for i in range(64):
    h = kw_hex[i]
    inner = get_inner(h)
    outer = get_outer(h)
    basin = get_basin(h)
    hu = hugua(h)
    print(f"  {i+1:3d} {kw_names[i]:>12s} {fmt6(h):>8s} {inner:04b}   {outer_names[outer]:>4s}  {sym[basin]}  {fmt6(hu):>8s}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. TRANSITION DECOMPOSITION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. TRANSITION DECOMPOSITION: INNER vs OUTER CHANGES")
print("=" * 70)

inner_changes = 0
outer_changes = 0
both_changes = 0
neither_changes = 0

transitions = []
for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    in1, in2 = get_inner(h1), get_inner(h2)
    out1, out2 = get_outer(h1), get_outer(h2)
    
    inner_changed = (in1 != in2)
    outer_changed = (out1 != out2)
    
    # Hamming distances
    inner_xor = in1 ^ in2
    outer_xor = out1 ^ out2
    inner_dist = bin(inner_xor).count('1')
    outer_dist = bin(outer_xor).count('1')
    total_dist = hamming6(h1, h2)
    
    change_type = ('both' if inner_changed and outer_changed else
                   'inner' if inner_changed else
                   'outer' if outer_changed else 'none')
    
    transitions.append({
        'i': i, 'change': change_type,
        'inner_dist': inner_dist, 'outer_dist': outer_dist,
        'total_dist': total_dist,
        'in1': in1, 'in2': in2, 'out1': out1, 'out2': out2,
    })

change_counts = Counter(t['change'] for t in transitions)
print(f"\n  Change type distribution (63 transitions):")
for ct in ['inner', 'outer', 'both', 'none']:
    c = change_counts.get(ct, 0)
    print(f"    {ct:6s}: {c}/63 ({100*c/63:.0f}%)")

print(f"\n  Detailed transitions:")
for t in transitions:
    i = t['i']
    canon = "UC" if i < 29 else "LC"
    in_sym = f"{t['in1']:04b}→{t['in2']:04b}" if t['in1'] != t['in2'] else f"{t['in1']:04b}=    "
    out_sym = f"{outer_names[t['out1']]}→{outer_names[t['out2']]}" if t['out1'] != t['out2'] else f"{outer_names[t['out1']]}=   "
    print(f"    {i+1:2d}→{i+2:2d} [{canon}] d={t['total_dist']} "
          f"inner({t['inner_dist']}):{in_sym} outer({t['outer_dist']}):{out_sym} [{t['change']}]")

# ══════════════════════════════════════════════════════════════════════════════
# 3. DISTANCE DECOMPOSITION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. HAMMING DISTANCE DECOMPOSITION")
print("=" * 70)

inner_dists = [t['inner_dist'] for t in transitions]
outer_dists = [t['outer_dist'] for t in transitions]
total_dists = [t['total_dist'] for t in transitions]

print(f"\n  Total distance:  mean={np.mean(total_dists):.2f}, distribution={Counter(total_dists)}")
print(f"  Inner distance:  mean={np.mean(inner_dists):.2f}, distribution={Counter(inner_dists)}")
print(f"  Outer distance:  mean={np.mean(outer_dists):.2f}, distribution={Counter(outer_dists)}")
print(f"  Sum check: inner+outer should = total")
mismatches = sum(1 for t in transitions if t['inner_dist'] + t['outer_dist'] != t['total_dist'])
print(f"  Mismatches: {mismatches} (should be 0)")

# Correlation between inner and outer distance
from itertools import product
inner_arr = np.array(inner_dists)
outer_arr = np.array(outer_dists)
if np.std(inner_arr) > 0 and np.std(outer_arr) > 0:
    corr = np.corrcoef(inner_arr, outer_arr)[0, 1]
    print(f"\n  Correlation between inner and outer distance: {corr:.3f}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. THE 互 WALK AS ITS OWN SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. THE 互 WALK — DOES IT HAVE SIMPLER STRUCTURE?")
print("=" * 70)

hu_seq = [hugua(kw_hex[i]) for i in range(64)]
inner_seq = [get_inner(kw_hex[i]) for i in range(64)]

# How many distinct 互 transitions?
hu_transitions = Counter()
for i in range(63):
    if hu_seq[i] != hu_seq[i+1]:
        hu_transitions[(hu_seq[i], hu_seq[i+1])] += 1

print(f"\n  互 walk: {len(set(hu_seq))} distinct values visited")
print(f"  互 unchanged: {sum(1 for i in range(63) if hu_seq[i] == hu_seq[i+1])}/63")
print(f"  互 distinct transitions: {len(hu_transitions)}")

# Run-length of 互 walk
hu_runs = []
current = hu_seq[0]
count = 1
for i in range(1, 64):
    if hu_seq[i] == current:
        count += 1
    else:
        hu_runs.append((current, count))
        current = hu_seq[i]
        count = 1
hu_runs.append((current, count))

print(f"  互 runs: {len(hu_runs)}")
print(f"  互 run lengths: {Counter(l for _, l in hu_runs)}")

# Outer walk run-length
outer_seq = [get_outer(kw_hex[i]) for i in range(64)]
outer_runs = []
current = outer_seq[0]
count = 1
for i in range(1, 64):
    if outer_seq[i] == current:
        count += 1
    else:
        outer_runs.append((current, count))
        current = outer_seq[i]
        count = 1
outer_runs.append((current, count))

print(f"\n  Outer walk: {len(set(outer_seq))} distinct values visited")
print(f"  Outer unchanged: {sum(1 for i in range(63) if outer_seq[i] == outer_seq[i+1])}/63")
print(f"  Outer runs: {len(outer_runs)}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. WHEN DOES ONLY OUTER CHANGE? (SAME 互, DIFFERENT SURFACE)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. OUTER-ONLY TRANSITIONS (SAME 互, DIFFERENT SURFACE)")
print("=" * 70)

outer_only = [t for t in transitions if t['change'] == 'outer']
print(f"\n  {len(outer_only)} outer-only transitions:")
for t in outer_only:
    i = t['i']
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hu = hugua(h1)  # Same as hugua(h2)
    lo, up = lower_trigram(hu), upper_trigram(hu)
    print(f"    {i+1:2d}→{i+2:2d}: {kw_names[i]:12s}→{kw_names[i+1]:12s} "
          f"outer: {outer_names[t['out1']]}→{outer_names[t['out2']]} "
          f"互={TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]} "
          f"d={t['total_dist']}")

# These transitions change the "surface" but not the "hidden" — 
# the divination reading would be identical.

# ══════════════════════════════════════════════════════════════════════════════
# 6. WHEN DOES ONLY INNER CHANGE? (SAME SURFACE, DIFFERENT 互)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. INNER-ONLY TRANSITIONS (SAME OUTER, DIFFERENT 互)")
print("=" * 70)

inner_only = [t for t in transitions if t['change'] == 'inner']
print(f"\n  {len(inner_only)} inner-only transitions:")
for t in inner_only:
    i = t['i']
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hu1 = hugua(h1)
    hu2 = hugua(h2)
    lo1, up1 = lower_trigram(hu1), upper_trigram(hu1)
    lo2, up2 = lower_trigram(hu2), upper_trigram(hu2)
    b1, b2 = get_basin(h1), get_basin(h2)
    print(f"    {i+1:2d}→{i+2:2d}: {kw_names[i]:12s}→{kw_names[i+1]:12s} "
          f"互: {TRIGRAM_NAMES[lo1]}/{TRIGRAM_NAMES[up1]}→{TRIGRAM_NAMES[lo2]}/{TRIGRAM_NAMES[up2]} "
          f"basin: {sym[b1]}→{sym[b2]} d={t['total_dist']}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE OUTER WALK — WHAT IS IT?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. THE OUTER WALK (bits 0,5)")
print("=" * 70)

# Outer bits: bit 0 = bottom line of lower trigram, bit 5 = top line of upper trigram
# These are the "extremal" lines — the very bottom and very top of the hexagram

print(f"\n  Outer bit interpretation:")
print(f"  Bit 0 = bottom of hexagram (root of lower trigram)")
print(f"  Bit 5 = top of hexagram (crown of upper trigram)")
print(f"  These are the most exposed lines — the outermost presentation.")

print(f"\n  Outer sequence:")
for i in range(64):
    h = kw_hex[i]
    b0 = h & 1
    b5 = (h >> 5) & 1
    outer = get_outer(h)
    basin = get_basin(h)
    canon = "UC" if i < 30 else "LC"
    print(f"    {i+1:2d} {kw_names[i]:12s} [{canon}] outer={outer_names[outer]} "
          f"(root={'●' if b0 else '○'} crown={'●' if b5 else '○'}) basin={sym[basin]}")

# Outer walk pattern
outer_str = ''.join(outer_names[get_outer(kw_hex[i])] for i in range(64))
print(f"\n  Outer sequence: {outer_str}")

# Outer distribution by canon
uc_outer = Counter(get_outer(kw_hex[i]) for i in range(30))
lc_outer = Counter(get_outer(kw_hex[i]) for i in range(30, 64))
print(f"\n  UC outer distribution: {dict(uc_outer)}")
print(f"  LC outer distribution: {dict(lc_outer)}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. CORRELATION: INNER vs OUTER WALK STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. INNER vs OUTER WALK INDEPENDENCE")
print("=" * 70)

# Are inner and outer changes independent?
# If independent: P(inner_change AND outer_change) = P(inner)*P(outer)

p_inner = sum(1 for t in transitions if t['inner_dist'] > 0) / 63
p_outer = sum(1 for t in transitions if t['outer_dist'] > 0) / 63
p_both = sum(1 for t in transitions if t['inner_dist'] > 0 and t['outer_dist'] > 0) / 63
p_expected = p_inner * p_outer

print(f"\n  P(inner changes): {p_inner:.3f}")
print(f"  P(outer changes): {p_outer:.3f}")
print(f"  P(both change): {p_both:.3f}")
print(f"  P(both) if independent: {p_expected:.3f}")
print(f"  Ratio: {p_both/p_expected:.3f}")

if p_both > p_expected:
    print(f"  → Changes are positively correlated (tend to change together)")
else:
    print(f"  → Changes are negatively correlated (tend to change separately)")

# Mutual information
from math import log2
mi = 0
for ic in [0, 1]:
    for oc in [0, 1]:
        p_joint = sum(1 for t in transitions 
                      if (t['inner_dist'] > 0) == bool(ic) and
                         (t['outer_dist'] > 0) == bool(oc)) / 63
        p_i = sum(1 for t in transitions if (t['inner_dist'] > 0) == bool(ic)) / 63
        p_o = sum(1 for t in transitions if (t['outer_dist'] > 0) == bool(oc)) / 63
        if p_joint > 0 and p_i > 0 and p_o > 0:
            mi += p_joint * log2(p_joint / (p_i * p_o))

print(f"  Mutual information: {mi:.4f} bits")

# ══════════════════════════════════════════════════════════════════════════════
# 9. THE TWO WALKS SIDE BY SIDE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. SIDE-BY-SIDE: FULL vs 互 vs OUTER vs BASIN")
print("=" * 70)

print(f"\n  {'#':>3s} {'Name':>12s} {'Full':>8s}  {'Inner':>6s} {'Outer':>4s} {'Basin'} {'Δ_in':>4s} {'Δ_out':>5s} {'Δ_tot':>5s}")
for i in range(64):
    h = kw_hex[i]
    inner = get_inner(h)
    outer = get_outer(h)
    basin = get_basin(h)
    
    if i > 0:
        h_prev = kw_hex[i-1]
        d_in = bin(get_inner(h) ^ get_inner(h_prev)).count('1')
        d_out = bin(get_outer(h) ^ get_outer(h_prev)).count('1')
        d_tot = hamming6(h, h_prev)
        delta_str = f"{d_in:4d} {d_out:5d} {d_tot:5d}"
    else:
        delta_str = "   -     -     -"
    
    print(f"  {i+1:3d} {kw_names[i]:>12s} {fmt6(h):>8s}  {inner:04b}   {outer_names[outer]:>4s} {sym[basin]}    {delta_str}")

# ══════════════════════════════════════════════════════════════════════════════
# 10. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. SUMMARY: THE DUAL WALK")
print("=" * 70)

print(f"""
  DECOMPOSITION: h = outer(2 bits) × inner(4 bits)
                     surface          hidden (互)
  
  TRANSITION TYPES:
    Both change:   {change_counts.get('both', 0)}/63 ({100*change_counts.get('both',0)/63:.0f}%)
    Inner only:    {change_counts.get('inner', 0)}/63 ({100*change_counts.get('inner',0)/63:.0f}%)
    Outer only:    {change_counts.get('outer', 0)}/63 ({100*change_counts.get('outer',0)/63:.0f}%)
    Neither:       {change_counts.get('none', 0)}/63 ({100*change_counts.get('none',0)/63:.0f}%)
  
  DISTANCES:
    Mean total:  {np.mean(total_dists):.2f}
    Mean inner:  {np.mean(inner_dists):.2f} ({100*np.mean(inner_dists)/np.mean(total_dists):.0f}% of total)
    Mean outer:  {np.mean(outer_dists):.2f} ({100*np.mean(outer_dists)/np.mean(total_dists):.0f}% of total)
  
  STRUCTURE:
    互 runs: {len(hu_runs)} (changes {sum(1 for t in transitions if t['inner_dist']>0)}/63 steps)
    Outer runs: {len(outer_runs)} (changes {sum(1 for t in transitions if t['outer_dist']>0)}/63 steps)
    Basin runs: 26 (changes {sum(1 for i in range(63) if get_basin(kw_hex[i]) != get_basin(kw_hex[i+1]))}/63 steps)
    
  INDEPENDENCE:
    Inner/outer correlation: {corr:.3f}
    Mutual information: {mi:.4f} bits
    P(both)/P(independent): {p_both/p_expected:.3f}
""")
