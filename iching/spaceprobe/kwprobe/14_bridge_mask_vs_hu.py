"""
Does KW maximize hex distance while minimizing 互 distance at bridges?

Test: at inter-pair bridges, is hex distance high and 互 distance low
compared to random orderings? Are they anti-correlated?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np
from scipy import stats
import random

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6,
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
    if b2 == 0 and b3 == 0: return -1  # Kun
    elif b2 == 1 and b3 == 1: return 1  # Qian
    else: return 0  # KanLi

def get_inner(h):
    return (h >> 1) & 0xF

def get_outer(h):
    return (h & 1) | (((h >> 5) & 1) << 1)

# ══════════════════════════════════════════════════════════════════════════════
# 1. KW INTER-PAIR: HEX DISTANCE vs 互 DISTANCE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. HEX DISTANCE vs 互 DISTANCE AT INTER-PAIR BRIDGES")
print("=" * 70)

inter_hex_d = []
inter_hu_d = []
inter_inner_d = []
inter_outer_d = []

for k in range(31):
    h1 = kw_hex[2*k + 1]   # pair k end
    h2 = kw_hex[2*(k+1)]   # pair k+1 start
    hu1 = hugua(h1)
    hu2 = hugua(h2)
    
    inter_hex_d.append(hamming6(h1, h2))
    inter_hu_d.append(hamming6(hu1, hu2))
    inter_inner_d.append(bin(get_inner(h1) ^ get_inner(h2)).count('1'))
    inter_outer_d.append(bin(get_outer(h1) ^ get_outer(h2)).count('1'))

print(f"\n  Inter-pair bridges (31):")
print(f"    Hex distance:   mean={np.mean(inter_hex_d):.3f}  std={np.std(inter_hex_d):.3f}")
print(f"    互 distance:    mean={np.mean(inter_hu_d):.3f}  std={np.std(inter_hu_d):.3f}")
print(f"    Inner distance: mean={np.mean(inter_inner_d):.3f}  std={np.std(inter_inner_d):.3f}")
print(f"    Outer distance: mean={np.mean(inter_outer_d):.3f}  std={np.std(inter_outer_d):.3f}")

# Correlation between hex distance and 互 distance
r_hex_hu, p_hex_hu = stats.pearsonr(inter_hex_d, inter_hu_d)
r_hex_inner, p_hex_inner = stats.pearsonr(inter_hex_d, inter_inner_d)
r_inner_hu, p_inner_hu = stats.pearsonr(inter_inner_d, inter_hu_d)
r_outer_hu, p_outer_hu = stats.pearsonr(inter_outer_d, inter_hu_d)

print(f"\n  Correlations at inter-pair bridges:")
print(f"    hex vs 互:     r={r_hex_hu:.3f}  p={p_hex_hu:.4f}")
print(f"    hex vs inner:  r={r_hex_inner:.3f}  p={p_hex_inner:.4f}")
print(f"    inner vs 互:   r={r_inner_hu:.3f}  p={p_inner_hu:.4f}")
print(f"    outer vs 互:   r={r_outer_hu:.3f}  p={p_outer_hu:.4f}")

# Ratio: hex_d / hu_d (surface change per unit depth change)
ratios = [inter_hex_d[i] / inter_hu_d[i] if inter_hu_d[i] > 0 else float('inf')
          for i in range(31)]
finite_ratios = [r for r in ratios if r != float('inf')]
print(f"\n  Hex/互 ratio: mean={np.mean(finite_ratios):.3f}  "
      f"(>1 means more surface than depth change)")

# ══════════════════════════════════════════════════════════════════════════════
# 2. SAME ANALYSIS FOR INTRA-PAIR BRIDGES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. INTRA-PAIR BRIDGES FOR COMPARISON")
print("=" * 70)

intra_hex_d = []
intra_hu_d = []

for k in range(32):
    h1 = kw_hex[2*k]      # pair k start
    h2 = kw_hex[2*k + 1]  # pair k end
    hu1 = hugua(h1)
    hu2 = hugua(h2)
    
    intra_hex_d.append(hamming6(h1, h2))
    intra_hu_d.append(hamming6(hu1, hu2))

print(f"\n  Intra-pair bridges (32):")
print(f"    Hex distance:   mean={np.mean(intra_hex_d):.3f}")
print(f"    互 distance:    mean={np.mean(intra_hu_d):.3f}")
print(f"    Ratio hex/互:   {np.mean(intra_hex_d)/np.mean(intra_hu_d):.3f}")

print(f"\n  Compare ratios:")
print(f"    Intra-pair: hex/互 = {np.mean(intra_hex_d):.2f}/{np.mean(intra_hu_d):.2f} = {np.mean(intra_hex_d)/np.mean(intra_hu_d):.3f}")
print(f"    Inter-pair: hex/互 = {np.mean(inter_hex_d):.2f}/{np.mean(inter_hu_d):.2f} = {np.mean(inter_hex_d)/np.mean(inter_hu_d):.3f}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. RANDOM BASELINE — PAIR-PRESERVING PERMUTATIONS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. KW vs RANDOM: PAIR-PRESERVING PERMUTATIONS")
print("=" * 70)

# KW has 32 pairs. The inter-pair bridges depend on pair ordering.
# Permute pair ordering, measure inter-pair hex and 互 distances.

# Extract pairs
pairs = [(kw_hex[2*k], kw_hex[2*k+1]) for k in range(32)]

N_PERM = 50000
random.seed(42)

rand_hex_means = []
rand_hu_means = []
rand_ratios = []

for _ in range(N_PERM):
    perm = list(pairs)
    random.shuffle(perm)
    
    hex_ds = []
    hu_ds = []
    for k in range(31):
        h1 = perm[k][1]      # pair k end
        h2 = perm[k+1][0]    # pair k+1 start
        hex_ds.append(hamming6(h1, h2))
        hu_ds.append(hamming6(hugua(h1), hugua(h2)))
    
    rand_hex_means.append(np.mean(hex_ds))
    rand_hu_means.append(np.mean(hu_ds))
    if np.mean(hu_ds) > 0:
        rand_ratios.append(np.mean(hex_ds) / np.mean(hu_ds))

kw_hex_mean = np.mean(inter_hex_d)
kw_hu_mean = np.mean(inter_hu_d)
kw_ratio = kw_hex_mean / kw_hu_mean

hex_pct = stats.percentileofscore(rand_hex_means, kw_hex_mean)
hu_pct = stats.percentileofscore(rand_hu_means, kw_hu_mean)
ratio_pct = stats.percentileofscore(rand_ratios, kw_ratio)

print(f"\n  KW inter-pair vs {N_PERM} random pair orderings:")
print(f"    Hex distance:  KW={kw_hex_mean:.3f}  random={np.mean(rand_hex_means):.3f}±{np.std(rand_hex_means):.3f}  pct={hex_pct:.1f}%")
print(f"    互 distance:   KW={kw_hu_mean:.3f}  random={np.mean(rand_hu_means):.3f}±{np.std(rand_hu_means):.3f}  pct={hu_pct:.1f}%")
print(f"    Hex/互 ratio:  KW={kw_ratio:.3f}  random={np.mean(rand_ratios):.3f}±{np.std(rand_ratios):.3f}  pct={ratio_pct:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 4. SEPARATE: DOES KW MAXIMIZE HEX DISTANCE? MINIMIZE 互 DISTANCE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. SEPARATE TESTS: MAX HEX? MIN 互?")
print("=" * 70)

print(f"\n  Hex distance at inter-pair bridges:")
print(f"    KW percentile: {hex_pct:.1f}%")
print(f"    {'HIGH' if hex_pct > 75 else 'NORMAL' if hex_pct > 25 else 'LOW'} hex distance")

print(f"\n  互 distance at inter-pair bridges:")
print(f"    KW percentile: {hu_pct:.1f}%")
print(f"    {'HIGH' if hu_pct > 75 else 'NORMAL' if hu_pct > 25 else 'LOW'} 互 distance")

print(f"\n  Hex/互 ratio:")
print(f"    KW percentile: {ratio_pct:.1f}%")
print(f"    {'HIGH' if ratio_pct > 75 else 'NORMAL' if ratio_pct > 25 else 'LOW'} ratio (surface change per depth change)")

# ══════════════════════════════════════════════════════════════════════════════
# 5. ALL 63 TRANSITIONS: HEX vs 互 DISTANCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. ALL 63 TRANSITIONS: HEX vs 互 SCATTER")
print("=" * 70)

all_hex_d = []
all_hu_d = []
all_types = []

for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    all_hex_d.append(hamming6(h1, h2))
    all_hu_d.append(hamming6(hugua(h1), hugua(h2)))
    all_types.append('intra' if i % 2 == 0 else 'inter')

print(f"\n  Joint distribution (hex_d, hu_d):")
joint = Counter(zip(all_hex_d, all_hu_d))
print(f"  {'hex\\hu':>6s}", end="")
for hud in range(7):
    print(f"  {hud:3d}", end="")
print()
for hxd in range(7):
    print(f"  {hxd:5d}", end=" ")
    for hud in range(7):
        c = joint.get((hxd, hud), 0)
        print(f"  {c:3d}" if c > 0 else "    .", end="")
    print()

# Separate joint distributions for intra vs inter
print(f"\n  Intra-pair joint distribution (hex_d, hu_d):")
intra_joint = Counter((all_hex_d[i], all_hu_d[i]) for i in range(63) if all_types[i] == 'intra')
print(f"  {'hex\\hu':>6s}", end="")
for hud in range(7):
    print(f"  {hud:3d}", end="")
print()
for hxd in range(7):
    print(f"  {hxd:5d}", end=" ")
    for hud in range(7):
        c = intra_joint.get((hxd, hud), 0)
        print(f"  {c:3d}" if c > 0 else "    .", end="")
    print()

print(f"\n  Inter-pair joint distribution (hex_d, hu_d):")
inter_joint = Counter((all_hex_d[i], all_hu_d[i]) for i in range(63) if all_types[i] == 'inter')
print(f"  {'hex\\hu':>6s}", end="")
for hud in range(7):
    print(f"  {hud:3d}", end="")
print()
for hxd in range(7):
    print(f"  {hxd:5d}", end=" ")
    for hud in range(7):
        c = inter_joint.get((hxd, hud), 0)
        print(f"  {c:3d}" if c > 0 else "    .", end="")
    print()

# ══════════════════════════════════════════════════════════════════════════════
# 6. THE KEY QUESTION: SURFACE-DEPTH DECOUPLING
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. SURFACE-DEPTH DECOUPLING")
print("=" * 70)

# Decompose hex distance into outer (bits 0,5) and inner (bits 1-4)
# 互 distance depends only on inner bits.
# If sequence maximizes outer change while minimizing inner change,
# then hex distance is high but 互 distance is low.

print(f"\n  Inter-pair bridges — outer vs inner contribution to hex distance:")
for k in range(31):
    h1 = kw_hex[2*k + 1]
    h2 = kw_hex[2*(k+1)]
    hd = hamming6(h1, h2)
    id_ = bin(get_inner(h1) ^ get_inner(h2)).count('1')
    od = bin(get_outer(h1) ^ get_outer(h2)).count('1')
    hud = hamming6(hugua(h1), hugua(h2))
    
# Summary stats
inner_frac = np.mean(inter_inner_d) / np.mean(inter_hex_d)
outer_frac = np.mean(inter_outer_d) / np.mean(inter_hex_d)

print(f"    Inner fraction of hex distance: {inner_frac:.3f}")
print(f"    Outer fraction of hex distance: {outer_frac:.3f}")

# Compare to intra-pair
intra_inner_d2 = []
intra_outer_d2 = []
for k in range(32):
    h1 = kw_hex[2*k]
    h2 = kw_hex[2*k + 1]
    intra_inner_d2.append(bin(get_inner(h1) ^ get_inner(h2)).count('1'))
    intra_outer_d2.append(bin(get_outer(h1) ^ get_outer(h2)).count('1'))

intra_inner_frac = np.mean(intra_inner_d2) / np.mean(intra_hex_d)
intra_outer_frac = np.mean(intra_outer_d2) / np.mean(intra_hex_d)

print(f"\n  Compare inner/outer fraction:")
print(f"    Intra-pair: inner={intra_inner_frac:.3f}  outer={intra_outer_frac:.3f}")
print(f"    Inter-pair: inner={inner_frac:.3f}  outer={outer_frac:.3f}")

# Random baseline for outer fraction
rand_inner_fracs = []
rand_outer_fracs = []
for _ in range(N_PERM):
    perm = list(pairs)
    random.shuffle(perm)
    
    inner_ds = []
    outer_ds = []
    hex_ds = []
    for k in range(31):
        h1 = perm[k][1]
        h2 = perm[k+1][0]
        hex_ds.append(hamming6(h1, h2))
        inner_ds.append(bin(get_inner(h1) ^ get_inner(h2)).count('1'))
        outer_ds.append(bin(get_outer(h1) ^ get_outer(h2)).count('1'))
    
    if np.mean(hex_ds) > 0:
        rand_inner_fracs.append(np.mean(inner_ds) / np.mean(hex_ds))
        rand_outer_fracs.append(np.mean(outer_ds) / np.mean(hex_ds))

outer_frac_pct = stats.percentileofscore(rand_outer_fracs, outer_frac)
inner_frac_pct = stats.percentileofscore(rand_inner_fracs, inner_frac)

print(f"\n  KW vs random — inner/outer fraction at inter-pair bridges:")
print(f"    Inner fraction: KW={inner_frac:.3f}  random={np.mean(rand_inner_fracs):.3f}±{np.std(rand_inner_fracs):.3f}  pct={inner_frac_pct:.1f}%")
print(f"    Outer fraction: KW={outer_frac:.3f}  random={np.mean(rand_outer_fracs):.3f}±{np.std(rand_outer_fracs):.3f}  pct={outer_frac_pct:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 7. DIRECT TEST: DOES KW MINIMIZE 互 DISTANCE GIVEN HEX DISTANCE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. CONDITIONAL TEST: 互 DISTANCE GIVEN HEX DISTANCE")
print("=" * 70)

# For each hex distance value, compare KW's mean 互 distance to random
for hd in range(1, 7):
    kw_hud = [inter_hu_d[i] for i in range(31) if inter_hex_d[i] == hd]
    if not kw_hud:
        continue
    
    # Collect from random
    rand_huds = []
    for _ in range(10000):
        perm = list(pairs)
        random.shuffle(perm)
        for k in range(31):
            h1 = perm[k][1]
            h2 = perm[k+1][0]
            if hamming6(h1, h2) == hd:
                rand_huds.append(hamming6(hugua(h1), hugua(h2)))
    
    if rand_huds:
        print(f"\n  hex_d={hd}: KW has {len(kw_hud)} bridges, mean 互_d={np.mean(kw_hud):.2f}")
        print(f"    Random mean 互_d given hex_d={hd}: {np.mean(rand_huds):.2f}±{np.std(rand_huds):.2f}")
        pct = stats.percentileofscore(rand_huds, np.mean(kw_hud))
        print(f"    KW percentile: {pct:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. SUMMARY")
print("=" * 70)

print(f"""
  Inter-pair bridges (the sequence's choice):
    Hex distance:  {kw_hex_mean:.2f}  (pct {hex_pct:.1f}% vs random)
    互 distance:   {kw_hu_mean:.2f}  (pct {hu_pct:.1f}% vs random)  
    Hex/互 ratio:  {kw_ratio:.2f}  (pct {ratio_pct:.1f}% vs random)
    
    Outer fraction: {outer_frac:.3f}  (pct {outer_frac_pct:.1f}% vs random)
    Inner fraction: {inner_frac:.3f}  (pct {inner_frac_pct:.1f}% vs random)
    
  Intra-pair bridges (algebraically forced):
    Hex distance:  {np.mean(intra_hex_d):.2f}
    互 distance:   {np.mean(intra_hu_d):.2f}
    Hex/互 ratio:  {np.mean(intra_hex_d)/np.mean(intra_hu_d):.2f}
""")
