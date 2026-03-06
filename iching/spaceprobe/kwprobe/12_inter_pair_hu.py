"""
Characterize 互 at inter-pair bridges.

Intra-pair bridges (within a pair): algebraically constrained
  - reverse pair: 互 values are reverses
  - complement pair: 互 values are complements

Inter-pair bridges (between pairs): the sequence's actual choice.
What does 互 do at these boundaries?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, reverse6, hamming6, fmt6,
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

def get_inner(h):
    return (h >> 1) & 0xF

def get_outer(h):
    return (h & 1) | (((h >> 5) & 1) << 1)

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

sym = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}
outer_names = {0: '○○', 1: '●○', 2: '○●', 3: '●●'}

# ══════════════════════════════════════════════════════════════════════════════
# 1. SEPARATE INTRA vs INTER PAIR BRIDGES
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. INTRA-PAIR vs INTER-PAIR BRIDGES")
print("=" * 70)

intra = []  # odd→even (within pair): steps 1→2, 3→4, ...
inter = []  # even→odd (between pairs): steps 2→3, 4→5, ...

for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hu1, hu2 = hugua(h1), hugua(h2)
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    
    entry = {
        'step': i, 'h1': h1, 'h2': h2,
        'hu1': hu1, 'hu2': hu2,
        'hu_dist': hamming6(hu1, hu2),
        'hex_dist': hamming6(h1, h2),
        'inner_dist': bin(get_inner(h1) ^ get_inner(h2)).count('1'),
        'outer_dist': bin(get_outer(h1) ^ get_outer(h2)).count('1'),
        'kernel': kernel,
        'k_name': kernel_names[kernel],
        'in_h': kernel in H_KERNELS,
        'b1': get_basin(h1), 'b2': get_basin(h2),
        'hu_same': hu1 == hu2,
        'hu_rev': hu2 == reverse6(hu1),
        'hu_comp': hu2 == hu1 ^ MASK_ALL,
    }
    
    if i % 2 == 0:  # positions 0,1 = pair; step 0→1 is intra
        intra.append(entry)
    else:
        inter.append(entry)

print(f"\n  Intra-pair bridges: {len(intra)} (within KW pairs)")
print(f"  Inter-pair bridges: {len(inter)} (between consecutive pairs)")

# ══════════════════════════════════════════════════════════════════════════════
# 2. INTRA-PAIR 互 RELATIONSHIPS (EXPECTED: FORCED)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. INTRA-PAIR 互 RELATIONSHIPS")
print("=" * 70)

print(f"\n  互 relationship within pairs:")
intra_hu_rels = Counter()
for e in intra:
    if e['hu_same']:
        rel = 'same'
    elif e['hu_rev']:
        rel = 'reverse'
    elif e['hu_comp']:
        rel = 'complement'
    else:
        rel = f"other(d={e['hu_dist']})"
    intra_hu_rels[rel] += 1

for rel, c in sorted(intra_hu_rels.items(), key=lambda x: -x[1]):
    print(f"    {rel}: {c}/32")

# ══════════════════════════════════════════════════════════════════════════════
# 3. INTER-PAIR 互 RELATIONSHIPS (THE SEQUENCE'S CHOICE)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. INTER-PAIR 互 RELATIONSHIPS")
print("=" * 70)

print(f"\n  互 relationship between pairs (31 bridges):")
inter_hu_rels = Counter()
for e in inter:
    if e['hu_same']:
        rel = 'same'
    elif e['hu_rev']:
        rel = 'reverse'
    elif e['hu_comp']:
        rel = 'complement'
    else:
        rel = f"other(d={e['hu_dist']})"
    inter_hu_rels[rel] += 1

for rel, c in sorted(inter_hu_rels.items(), key=lambda x: -x[1]):
    print(f"    {rel}: {c}/31")

# Detail
print(f"\n  Inter-pair bridge detail:")
print(f"  {'Bridge':>10s} {'Pair_end':>12s} {'Next_start':>12s} "
      f"{'互_end':>10s} {'互_start':>10s} {'互_rel':>10s} "
      f"{'Basin':>6s} {'Kernel':>4s} {'d_hex':>5s} {'d_互':>4s} {'d_in':>4s} {'d_out':>5s}")

for e in inter:
    i = e['step']
    # This is the bridge from pair[i//2] to pair[(i+1)//2]
    pair_from = i // 2
    pair_to = (i + 1) // 2
    
    hu1_lo = TRIGRAM_NAMES[lower_trigram(e['hu1'])]
    hu1_up = TRIGRAM_NAMES[upper_trigram(e['hu1'])]
    hu2_lo = TRIGRAM_NAMES[lower_trigram(e['hu2'])]
    hu2_up = TRIGRAM_NAMES[upper_trigram(e['hu2'])]
    
    if e['hu_same']:
        hu_rel = 'same'
    elif e['hu_rev']:
        hu_rel = 'reverse'
    elif e['hu_comp']:
        hu_rel = 'complement'
    else:
        hu_rel = f'd={e["hu_dist"]}'
    
    basin_trans = f"{sym[e['b1']]}{sym[e['b2']]}"
    canon = "UC" if i < 29 else "LC"
    
    print(f"  {pair_from:2d}→{pair_to:2d} [{canon}] "
          f"{kw_names[i]:>12s} {kw_names[i+1]:>12s} "
          f"{hu1_lo}/{hu1_up:4s} {hu2_lo}/{hu2_up:4s} "
          f"{hu_rel:>10s} {basin_trans} {e['k_name']:>4s} "
          f"{e['hex_dist']:5d} {e['hu_dist']:4d} {e['inner_dist']:4d} {e['outer_dist']:5d}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. COMPARE INTRA vs INTER STATISTICS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. INTRA vs INTER COMPARISON")
print("=" * 70)

for label, bridges in [("Intra-pair", intra), ("Inter-pair", inter)]:
    n = len(bridges)
    hu_dists = [e['hu_dist'] for e in bridges]
    hex_dists = [e['hex_dist'] for e in bridges]
    inner_dists = [e['inner_dist'] for e in bridges]
    outer_dists = [e['outer_dist'] for e in bridges]
    h_count = sum(1 for e in bridges if e['in_h'])
    hu_same = sum(1 for e in bridges if e['hu_same'])
    basin_same = sum(1 for e in bridges if e['b1'] == e['b2'])
    
    print(f"\n  {label} ({n} bridges):")
    print(f"    Hex distance:   mean={np.mean(hex_dists):.2f}")
    print(f"    Inner distance: mean={np.mean(inner_dists):.2f}")
    print(f"    Outer distance: mean={np.mean(outer_dists):.2f}")
    print(f"    互 distance:    mean={np.mean(hu_dists):.2f}")
    print(f"    H-kernel:       {h_count}/{n} ({100*h_count/n:.0f}%)")
    print(f"    互 same:        {hu_same}/{n} ({100*hu_same/n:.0f}%)")
    print(f"    Basin same:     {basin_same}/{n} ({100*basin_same/n:.0f}%)")
    
    # Kernel distribution
    k_dist = Counter(e['k_name'] for e in bridges)
    print(f"    Kernels: {dict(sorted(k_dist.items()))}")
    
    # Change type
    change_types = Counter()
    for e in bridges:
        ic = e['inner_dist'] > 0
        oc = e['outer_dist'] > 0
        if ic and oc: change_types['both'] += 1
        elif ic: change_types['inner'] += 1
        elif oc: change_types['outer'] += 1
        else: change_types['none'] += 1
    print(f"    Change types: {dict(change_types)}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE 互 CONTINUITY AT PAIR BOUNDARIES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. 互 CONTINUITY — HOW SMOOTHLY DOES 互 TRANSITION BETWEEN PAIRS?")
print("=" * 70)

# Within a pair, 互 values are forced (reverse or complement).
# Between pairs, 互 values are a choice.
# How much does 互 change at pair boundaries vs within pairs?

print(f"\n  互 distance distribution:")
print(f"    Intra-pair: {Counter(e['hu_dist'] for e in intra)}")
print(f"    Inter-pair: {Counter(e['hu_dist'] for e in inter)}")

print(f"\n  Mean 互 distance:")
print(f"    Intra-pair: {np.mean([e['hu_dist'] for e in intra]):.2f}")
print(f"    Inter-pair: {np.mean([e['hu_dist'] for e in inter]):.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. INTER-PAIR 互 TRANSITIONS — THE PAIR-LEVEL 互 WALK
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. THE PAIR-LEVEL 互 WALK")
print("=" * 70)

# Each pair has two 互 values (one per member). 
# For reverse pairs: hu2 = reverse(hu1), so the pair's 互 is a reverse pair in 互-space.
# For complement pairs: hu2 = complement(hu1).
# 
# At pair level, we can represent each pair by its first member's 互 value.
# The inter-pair bridge connects pair_k's second member to pair_{k+1}'s first member.

print(f"\n  Pair-level 互 walk:")
print(f"  {'Pair':>5s} {'Hex1':>12s} {'Hex2':>12s} "
      f"{'互1':>10s} {'互2':>10s} {'Pair_type':>10s} "
      f"{'→ Bridge →':>12s}")

for p in range(32):
    h1, h2 = kw_hex[2*p], kw_hex[2*p+1]
    hu1, hu2 = hugua(h1), hugua(h2)
    
    hu1_lo = TRIGRAM_NAMES[lower_trigram(hu1)]
    hu1_up = TRIGRAM_NAMES[upper_trigram(hu1)]
    hu2_lo = TRIGRAM_NAMES[lower_trigram(hu2)]
    hu2_up = TRIGRAM_NAMES[upper_trigram(hu2)]
    
    if h2 == reverse6(h1):
        ptype = "reverse"
    elif h2 == h1 ^ MASK_ALL:
        ptype = "complement"
    else:
        ptype = "other"
    
    # Bridge to next pair
    if p < 31:
        next_h = kw_hex[2*(p+1)]
        next_hu = hugua(next_h)
        bridge_dist = hamming6(hu2, next_hu)
        next_lo = TRIGRAM_NAMES[lower_trigram(next_hu)]
        next_up = TRIGRAM_NAMES[upper_trigram(next_hu)]
        bridge_str = f"d={bridge_dist} → {next_lo}/{next_up}"
    else:
        bridge_str = "(end)"
    
    canon = "UC" if p < 15 else "LC"
    print(f"  {p:3d} [{canon}] {kw_names[2*p]:>12s} {kw_names[2*p+1]:>12s} "
          f"{hu1_lo}/{hu1_up:4s} {hu2_lo}/{hu2_up:4s} {ptype:>10s} "
          f"{bridge_str}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. INNER CHANGE AT INTER-PAIR BRIDGES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. WHAT CHANGES AT INTER-PAIR BRIDGES?")
print("=" * 70)

# At an inter-pair bridge, the outgoing hexagram (pair_k member 2) transitions
# to the incoming hexagram (pair_{k+1} member 1).
# Since intra-pair 互 is forced, the inter-pair bridge is where 互 genuinely changes.

# How much inner vs outer changes at these boundaries?
print(f"\n  Inner/outer decomposition at inter-pair bridges:")
for e in inter:
    i = e['step']
    pair_from = i // 2
    pair_to = (i + 1) // 2
    
    h1, h2 = e['h1'], e['h2']
    in1, in2 = get_inner(h1), get_inner(h2)
    out1, out2 = get_outer(h1), get_outer(h2)
    
    inner_changed = in1 != in2
    outer_changed = out1 != out2
    
    if inner_changed and outer_changed:
        change = "BOTH"
    elif inner_changed:
        change = "INNER"
    elif outer_changed:
        change = "OUTER"
    else:
        change = "NONE"
    
    canon = "UC" if i < 29 else "LC"
    print(f"    {pair_from:2d}→{pair_to:2d} [{canon}]: "
          f"{kw_names[i]:>12s}→{kw_names[i+1]:>12s} "
          f"inner:{in1:04b}→{in2:04b}({e['inner_dist']}) "
          f"outer:{outer_names[out1]}→{outer_names[out2]}({e['outer_dist']}) "
          f"[{change}]")

inter_change_types = Counter()
for e in inter:
    ic = e['inner_dist'] > 0
    oc = e['outer_dist'] > 0
    if ic and oc: inter_change_types['both'] += 1
    elif ic: inter_change_types['inner'] += 1
    elif oc: inter_change_types['outer'] += 1
    else: inter_change_types['none'] += 1

print(f"\n  Inter-pair change types: {dict(inter_change_types)}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. SUMMARY")
print("=" * 70)

print(f"""
  INTRA-PAIR (within pair, 32 bridges):
    互 relationship is FORCED:
      {intra_hu_rels}
    Mean hex distance: {np.mean([e['hex_dist'] for e in intra]):.2f}
    Mean 互 distance:  {np.mean([e['hu_dist'] for e in intra]):.2f}
    Basin same: {sum(1 for e in intra if e['b1']==e['b2'])}/32

  INTER-PAIR (between pairs, 31 bridges):
    互 relationship is CHOSEN:
      {inter_hu_rels}
    Mean hex distance: {np.mean([e['hex_dist'] for e in inter]):.2f}
    Mean 互 distance:  {np.mean([e['hu_dist'] for e in inter]):.2f}
    Basin same: {sum(1 for e in inter if e['b1']==e['b2'])}/31
""")
