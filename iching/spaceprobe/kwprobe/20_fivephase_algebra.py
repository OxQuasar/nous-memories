"""
Five-phase relations in S₄ and Z₂³ spaces.

For each pair (i, i+1) in KW, compute:
  - Five-phase relation between lower trigrams
  - Five-phase relation between upper trigrams
  - Five-phase relation between 互 lower trigrams
  - Five-phase relation between 互 upper trigrams
  
Cross-tabulate with:
  - Kernel (O, M, I) components and full kernel type
  - H-membership
  - Basin transition (same/cross)
  - Inner/outer change
  - Intra-pair vs inter-pair

Also: the 64×64 all-pairs five-phase distribution by kernel.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np
from scipy import stats

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    TRIGRAM_ELEMENT, five_phase_relation,
)

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    elif b2 == 1 and b3 == 1: return 1
    else: return 0

def get_inner(h): return (h >> 1) & 0xF
def get_outer(h): return (h & 1) | (((h >> 5) & 1) << 1)

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}
basin_sym = {-1: '○', 0: '◎', 1: '●'}
RELS = ['比和', '生体', '克体', '体生用', '体克用']

def trig_phase(t1, t2):
    return five_phase_relation(TRIGRAM_ELEMENT[t1], TRIGRAM_ELEMENT[t2])

# Precompute
lo = [lower_trigram(kw_hex[i]) for i in range(64)]
up = [upper_trigram(kw_hex[i]) for i in range(64)]
hu = [hugua(kw_hex[i]) for i in range(64)]
hu_lo = [lower_trigram(hu[i]) for i in range(64)]
hu_up = [upper_trigram(hu[i]) for i in range(64)]
basins = [get_basin(kw_hex[i]) for i in range(64)]

# ══════════════════════════════════════════════════════════════════════════════
# 1. CONSECUTIVE TRANSITIONS: FIVE-PHASE × KERNEL
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. CONSECUTIVE TRANSITIONS: FIVE-PHASE × KERNEL")
print("=" * 70)

transitions = []
for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    kname = kernel_names[kernel]
    in_H = kernel in H_KERNELS
    b_same = basins[i] == basins[i+1]
    bridge_type = 'intra' if i % 2 == 0 else 'inter'
    
    t = {
        'i': i, 'kernel': kernel, 'kname': kname, 'in_H': in_H,
        'b_same': b_same, 'bridge': bridge_type,
        'lo_rel': trig_phase(lo[i], lo[i+1]),
        'up_rel': trig_phase(up[i], up[i+1]),
        'hu_lo_rel': trig_phase(hu_lo[i], hu_lo[i+1]),
        'hu_up_rel': trig_phase(hu_up[i], hu_up[i+1]),
        'basin_trans': f"{basin_sym[basins[i]]}{basin_sym[basins[i+1]]}",
    }
    transitions.append(t)

# Cross-tab: kernel × five-phase (lower trigram)
print(f"\n  Lower trigram five-phase × kernel (all 63 transitions):")
print(f"  {'Rel':>6s}", end="")
for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    print(f" {kn:>4s}", end="")
print(f" {'Total':>5s}")

for rel in RELS:
    counts = Counter(t['kname'] for t in transitions if t['lo_rel'] == rel)
    total = sum(counts.values())
    print(f"  {rel:>6s}", end="")
    for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
        print(f" {counts.get(kn, 0):4d}", end="")
    print(f" {total:5d}")

# Same for upper trigram
print(f"\n  Upper trigram five-phase × kernel:")
print(f"  {'Rel':>6s}", end="")
for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    print(f" {kn:>4s}", end="")
print(f" {'Total':>5s}")

for rel in RELS:
    counts = Counter(t['kname'] for t in transitions if t['up_rel'] == rel)
    total = sum(counts.values())
    print(f"  {rel:>6s}", end="")
    for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
        print(f" {counts.get(kn, 0):4d}", end="")
    print(f" {total:5d}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. 互 TRIGRAM FIVE-PHASE × KERNEL
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. 互 TRIGRAM FIVE-PHASE × KERNEL")
print("=" * 70)

print(f"\n  互 lower trigram five-phase × kernel:")
print(f"  {'Rel':>6s}", end="")
for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    print(f" {kn:>4s}", end="")
print(f" {'Total':>5s}")

for rel in RELS:
    counts = Counter(t['kname'] for t in transitions if t['hu_lo_rel'] == rel)
    total = sum(counts.values())
    print(f"  {rel:>6s}", end="")
    for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
        print(f" {counts.get(kn, 0):4d}", end="")
    print(f" {total:5d}")

print(f"\n  互 upper trigram five-phase × kernel:")
print(f"  {'Rel':>6s}", end="")
for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    print(f" {kn:>4s}", end="")
print(f" {'Total':>5s}")

for rel in RELS:
    counts = Counter(t['kname'] for t in transitions if t['hu_up_rel'] == rel)
    total = sum(counts.values())
    print(f"  {rel:>6s}", end="")
    for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
        print(f" {counts.get(kn, 0):4d}", end="")
    print(f" {total:5d}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. FIVE-PHASE × BASIN TRANSITION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. FIVE-PHASE × BASIN TRANSITION")
print("=" * 70)

for trig_label, rel_key in [("Lower", 'lo_rel'), ("Upper", 'up_rel'), 
                              ("互 lower", 'hu_lo_rel'), ("互 upper", 'hu_up_rel')]:
    print(f"\n  {trig_label} five-phase × basin transition:")
    print(f"  {'Rel':>6s} {'same':>5s} {'cross':>5s} {'%same':>6s}")
    
    for rel in RELS:
        same = sum(1 for t in transitions if t[rel_key] == rel and t['b_same'])
        cross = sum(1 for t in transitions if t[rel_key] == rel and not t['b_same'])
        total = same + cross
        pct = 100 * same / total if total > 0 else 0
        print(f"  {rel:>6s} {same:5d} {cross:5d} {pct:5.0f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 4. FIVE-PHASE × H-MEMBERSHIP
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. FIVE-PHASE × H-MEMBERSHIP")
print("=" * 70)

for trig_label, rel_key in [("Lower", 'lo_rel'), ("Upper", 'up_rel'),
                              ("互 lower", 'hu_lo_rel'), ("互 upper", 'hu_up_rel')]:
    print(f"\n  {trig_label} five-phase × H-membership:")
    print(f"  {'Rel':>6s} {'H':>4s} {'¬H':>4s} {'%H':>5s}")
    
    for rel in RELS:
        in_h = sum(1 for t in transitions if t[rel_key] == rel and t['in_H'])
        not_h = sum(1 for t in transitions if t[rel_key] == rel and not t['in_H'])
        total = in_h + not_h
        pct = 100 * in_h / total if total > 0 else 0
        print(f"  {rel:>6s} {in_h:4d} {not_h:4d} {pct:4.0f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 5. FIVE-PHASE × INTRA/INTER PAIR
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. FIVE-PHASE × INTRA/INTER PAIR")
print("=" * 70)

for trig_label, rel_key in [("Lower", 'lo_rel'), ("Upper", 'up_rel'),
                              ("互 lower", 'hu_lo_rel'), ("互 upper", 'hu_up_rel')]:
    print(f"\n  {trig_label} five-phase × bridge type:")
    print(f"  {'Rel':>6s} {'intra':>5s} {'inter':>5s}")
    
    for rel in RELS:
        intra = sum(1 for t in transitions if t[rel_key] == rel and t['bridge'] == 'intra')
        inter = sum(1 for t in transitions if t[rel_key] == rel and t['bridge'] == 'inter')
        print(f"  {rel:>6s} {intra:5d} {inter:5d}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. ALL 64×64 PAIRS: FIVE-PHASE × KERNEL (FULL DISTRIBUTION)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. ALL 64×64 PAIRS: FIVE-PHASE × KERNEL (STRUCTURAL)")
print("=" * 70)

# This asks: for ALL hexagram pairs (not just consecutive),
# does the five-phase relation between trigrams correlate with kernel type?
# This is algebraically determined — not a sequence property.

all_lo_phase_kernel = Counter()
all_up_phase_kernel = Counter()
all_hu_lo_phase_kernel = Counter()
all_hu_up_phase_kernel = Counter()

for i in range(64):
    for j in range(64):
        if i == j:
            continue
        xor = kw_hex[i] ^ kw_hex[j]
        kernel = mirror_kernel(xor)
        kname = kernel_names[kernel]
        
        all_lo_phase_kernel[(trig_phase(lo[i], lo[j]), kname)] += 1
        all_up_phase_kernel[(trig_phase(up[i], up[j]), kname)] += 1
        all_hu_lo_phase_kernel[(trig_phase(hu_lo[i], hu_lo[j]), kname)] += 1
        all_hu_up_phase_kernel[(trig_phase(hu_up[i], hu_up[j]), kname)] += 1

for label, phase_kernel in [("Lower trig", all_lo_phase_kernel), 
                              ("Upper trig", all_up_phase_kernel),
                              ("互 lower", all_hu_lo_phase_kernel),
                              ("互 upper", all_hu_up_phase_kernel)]:
    print(f"\n  {label} five-phase × kernel (all 4032 directed pairs):")
    print(f"  {'Rel':>6s}", end="")
    for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
        print(f" {kn:>5s}", end="")
    print(f" {'Total':>6s}")
    
    for rel in RELS:
        total = 0
        row = []
        for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
            c = phase_kernel.get((rel, kn), 0)
            row.append(c)
            total += c
        print(f"  {rel:>6s}", end="")
        for c in row:
            print(f" {c:5d}", end="")
        print(f" {total:6d}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. FIVE-PHASE RELATION IS DETERMINED BY ELEMENT PAIR, ELEMENT BY TRIGRAM
#    HOW DOES TRIGRAM DISTANCE MAP TO FIVE-PHASE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. TRIGRAM HAMMING DISTANCE × FIVE-PHASE RELATION")
print("=" * 70)

# For all 8×8 trigram pairs
from cycle_algebra import hamming3

trig_dist_by_rel = defaultdict(list)
for t1 in range(8):
    for t2 in range(8):
        if t1 == t2:
            continue
        rel = trig_phase(t1, t2)
        d = hamming3(t1, t2)
        trig_dist_by_rel[rel].append(d)

print(f"\n  Trigram Hamming distance by five-phase relation (56 directed pairs):")
for rel in RELS:
    dists = trig_dist_by_rel[rel]
    print(f"    {rel}: mean={np.mean(dists):.2f}  dist={Counter(dists)}  n={len(dists)}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. FIVE-PHASE HOMOGENEITY: DO LOWER AND UPPER AGREE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. FIVE-PHASE AGREEMENT: LOWER vs UPPER AT TRANSITIONS")
print("=" * 70)

# At each consecutive transition, is the five-phase relation the same
# for lower and upper trigrams?

agree_outer = Counter()
agree_hu = Counter()

for t in transitions:
    # Outer trigrams
    if t['lo_rel'] == t['up_rel']:
        agree_outer['same'] += 1
    else:
        agree_outer['diff'] += 1
    
    # 互 trigrams
    if t['hu_lo_rel'] == t['hu_up_rel']:
        agree_hu['same'] += 1
    else:
        agree_hu['diff'] += 1

print(f"\n  Outer trigrams (lower vs upper five-phase):")
print(f"    Same: {agree_outer['same']}/63  Different: {agree_outer['diff']}/63")

print(f"\n  互 trigrams (lower vs upper five-phase):")
print(f"    Same: {agree_hu['same']}/63  Different: {agree_hu['diff']}/63")

# By bridge type
for bt in ['intra', 'inter']:
    sub = [t for t in transitions if t['bridge'] == bt]
    agree = sum(1 for t in sub if t['lo_rel'] == t['up_rel'])
    print(f"\n  {bt}-pair outer agreement: {agree}/{len(sub)}")
    agree_h = sum(1 for t in sub if t['hu_lo_rel'] == t['hu_up_rel'])
    print(f"  {bt}-pair 互 agreement: {agree_h}/{len(sub)}")

# ══════════════════════════════════════════════════════════════════════════════
# 9. THE KEY: DOES KERNEL DETERMINE FIVE-PHASE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. DOES KERNEL DETERMINE FIVE-PHASE? (χ² test)")
print("=" * 70)

# For outer trigrams at all 4032 pairs
for label, phase_kernel in [("Lower trig", all_lo_phase_kernel),
                              ("Upper trig", all_up_phase_kernel),
                              ("互 lower", all_hu_lo_phase_kernel),
                              ("互 upper", all_hu_up_phase_kernel)]:
    # Build contingency table
    table = []
    for rel in RELS:
        row = [phase_kernel.get((rel, kn), 0) 
               for kn in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']]
        table.append(row)
    
    table = np.array(table)
    chi2, p, dof, expected = stats.chi2_contingency(table)
    
    # Cramér's V
    n = table.sum()
    k = min(table.shape)
    cramers_v = np.sqrt(chi2 / (n * (k - 1)))
    
    sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"  {label:>12s}: χ²={chi2:8.1f}  p={p:.2e}  Cramér's V={cramers_v:.3f}  {sig}")

# ══════════════════════════════════════════════════════════════════════════════
# 10. FIVE-PHASE FLOW: GENERATIVE vs DESTRUCTIVE AT BRIDGES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. GENERATIVE (生) vs DESTRUCTIVE (克) AT BRIDGES")
print("=" * 70)

# Classify relations as generative, destructive, or neutral
def phase_class(rel):
    if rel in ('生体', '体生用'): return '生'
    elif rel in ('克体', '体克用'): return '克'
    else: return '比'

for trig_label, rel_key in [("Lower", 'lo_rel'), ("Upper", 'up_rel'),
                              ("互 lower", 'hu_lo_rel'), ("互 upper", 'hu_up_rel')]:
    print(f"\n  {trig_label}:")
    
    # Overall
    overall = Counter(phase_class(t[rel_key]) for t in transitions)
    print(f"    All: 生={overall['生']}  克={overall['克']}  比={overall['比']}")
    
    # Intra vs inter
    for bt in ['intra', 'inter']:
        sub = [t for t in transitions if t['bridge'] == bt]
        counts = Counter(phase_class(t[rel_key]) for t in sub)
        print(f"    {bt}: 生={counts['生']}  克={counts['克']}  比={counts['比']}")
    
    # Basin-crossing vs basin-same
    for bs in [True, False]:
        sub = [t for t in transitions if t['b_same'] == bs]
        counts = Counter(phase_class(t[rel_key]) for t in sub)
        label = "b-same" if bs else "b-cross"
        print(f"    {label}: 生={counts['生']}  克={counts['克']}  比={counts['比']}")

# ══════════════════════════════════════════════════════════════════════════════
# 11. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("11. SUMMARY")
print("=" * 70)
