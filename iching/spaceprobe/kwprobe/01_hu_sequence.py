"""
Reanalyze the KW sequence through the divination lens.

What we now know:
- H bridges either preserve 互 (id, O → distance 0) or complement it (MI, OMI → distance 6)
- Non-H bridges scramble 互 (distance 2 or 4)
- Upper Canon prefers H, Lower Canon doesn't
- 互 biases toward 克

Questions:
1. What does the 互 sequence look like? (互 of each KW hexagram in order)
2. How does the 互 change across consecutive hexagrams?
3. Does the five-phase relation trace along the sequence have structure?
4. Does the 克 bias distribute differently across the sequence?
5. How does the divination "reading" change as you walk the sequence?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua, biangua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, kw_partner, reverse6,
    hamming6, popcount, bit, fmt6, fmt3,
)

# ══════════════════════════════════════════════════════════════════════════════
# Build KW sequence
# ══════════════════════════════════════════════════════════════════════════════

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}

H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

# ══════════════════════════════════════════════════════════════════════════════
# 1. THE 互 SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. THE 互 SEQUENCE (nuclear hexagram of each KW hexagram)")
print("=" * 70)

hu_seq = [hugua(h) for h in kw_hex]
hu_unique = len(set(hu_seq))
print(f"\n  64 hexagrams → {hu_unique} distinct 互 values in the sequence")
print(f"  (16 possible 互 values total)")

# How many times does each 互 value appear?
hu_counts = Counter(hu_seq)
print(f"\n  互 value frequencies in KW sequence:")
for hg in sorted(hu_counts.keys()):
    lo, up = lower_trigram(hg), upper_trigram(hg)
    print(f"    {fmt6(hg)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}): "
          f"{hu_counts[hg]} times")

# The 互 sequence itself
print(f"\n  互 sequence (first 32 = Upper Canon):")
for i in range(64):
    h = kw_hex[i]
    hg = hu_seq[i]
    lo, up = lower_trigram(hg), upper_trigram(hg)
    canon = "UC" if i < 30 else "LC"
    marker = " ← canon break" if i == 30 else ""
    print(f"    {i+1:2d}. {kw_names[i]:12s} ({fmt6(h)}) → 互={fmt6(hg)} "
          f"({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}) [{canon}]{marker}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. 互 TRANSITIONS ACROSS THE SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. 互 TRANSITIONS (how nuclear hexagram changes between consecutive)")
print("=" * 70)

# For each consecutive pair, what's the 互 distance and relationship?
hu_transitions = []
for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1, hg2 = hu_seq[i], hu_seq[i+1]
    
    # Bridge kernel
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    in_h = kernel in H_KERNELS
    
    # 互 distance
    hu_dist = hamming6(hg1, hg2)
    
    # 互 relationship
    if hg1 == hg2:
        hu_rel = "same"
    elif hg2 == hg1 ^ MASK_ALL:
        hu_rel = "complement"
    else:
        hu_rel = f"other(d={hu_dist})"
    
    hu_transitions.append({
        'i': i, 'kernel': kernel, 'in_h': in_h,
        'hu_dist': hu_dist, 'hu_rel': hu_rel,
        'hg1': hg1, 'hg2': hg2,
    })

# Summary
print(f"\n  互 transition types:")
rel_counts = Counter(t['hu_rel'] for t in hu_transitions)
for rel, count in sorted(rel_counts.items(), key=lambda x: -x[1]):
    print(f"    {rel}: {count}/63")

# By canon
print(f"\n  By canon:")
for canon_name, start, end in [("Upper (1-30)", 0, 29), ("Cross", 29, 30), ("Lower (31-64)", 30, 63)]:
    subset = [t for t in hu_transitions if start <= t['i'] < end]
    if not subset:
        continue
    rels = Counter(t['hu_rel'] for t in subset)
    h_count = sum(1 for t in subset if t['in_h'])
    print(f"\n    {canon_name}: {len(subset)} transitions, {h_count} in H ({100*h_count/len(subset):.0f}%)")
    for rel, count in sorted(rels.items(), key=lambda x: -x[1]):
        print(f"      {rel}: {count}")

# H bridges and 互 relationship
print(f"\n  H bridges → 互 relationship:")
for in_h in [True, False]:
    subset = [t for t in hu_transitions if t['in_h'] == in_h]
    tag = "H" if in_h else "non-H"
    rels = Counter(t['hu_rel'] for t in subset)
    print(f"\n    {tag} bridges ({len(subset)}):")
    for rel, count in sorted(rels.items(), key=lambda x: -x[1]):
        print(f"      {rel}: {count}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. THE 互 SEQUENCE AS A WALK IN 互-SPACE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. 互 SEQUENCE AS A WALK IN 互-SPACE (16 vertices)")
print("=" * 70)

# The 64 hexagrams project to 16 互 values. The KW sequence induces
# a walk on these 16 values. What does this walk look like?

# How many distinct 互 transitions (edges) are used?
hu_edges = set()
for t in hu_transitions:
    edge = (min(t['hg1'], t['hg2']), max(t['hg1'], t['hg2']))
    if t['hg1'] != t['hg2']:
        hu_edges.add(edge)

print(f"\n  Distinct 互-space edges traversed: {len(hu_edges)}")
print(f"  (16 vertices, max {16*15//2}=120 edges)")

# How many times does 互 stay the same? (Same 互 value for consecutive hexagrams)
same_count = sum(1 for t in hu_transitions if t['hu_rel'] == 'same')
print(f"  互 unchanged: {same_count}/63 transitions ({100*same_count/63:.0f}%)")

# Longest run of same 互 value
runs = []
current_run = 1
for i in range(1, 64):
    if hu_seq[i] == hu_seq[i-1]:
        current_run += 1
    else:
        runs.append(current_run)
        current_run = 1
runs.append(current_run)

print(f"  Longest run of same 互: {max(runs)}")
print(f"  Run length distribution: {Counter(runs)}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. FIVE-PHASE ALONG THE SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. FIVE-PHASE RELATIONS ALONG THE SEQUENCE")
print("=" * 70)

# For each hexagram in KW order, compute:
# - 本 relation (upper/lower trigram five-phase)
# - 互 relation (nuclear upper/lower five-phase)

rel_names = ["比和", "生体", "克体", "体生用", "体克用"]

ben_rels = []
hu_rels = []
for i in range(64):
    h = kw_hex[i]
    hg = hu_seq[i]
    
    lo, up = lower_trigram(h), upper_trigram(h)
    lo_e, up_e = TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up]
    
    hg_lo, hg_up = lower_trigram(hg), upper_trigram(hg)
    hg_lo_e, hg_up_e = TRIGRAM_ELEMENT[hg_lo], TRIGRAM_ELEMENT[hg_up]
    
    # Convention: lower=体, upper=用 (consistent convention for sequence analysis)
    ben_rel = five_phase_relation(lo_e, up_e)
    hu_rel = five_phase_relation(hg_lo_e, hg_up_e)
    
    ben_rels.append(ben_rel)
    hu_rels.append(hu_rel)

# Distribution by canon
for canon_name, start, end in [("Upper Canon (1-30)", 0, 30), ("Lower Canon (31-64)", 30, 64), ("Full", 0, 64)]:
    print(f"\n  {canon_name}:")
    ben_counts = Counter(ben_rels[start:end])
    hu_counts_canon = Counter(hu_rels[start:end])
    
    print(f"    本 relations: ", end="")
    for r in rel_names:
        print(f"{r}={ben_counts.get(r,0)} ", end="")
    print()
    print(f"    互 relations: ", end="")
    for r in rel_names:
        print(f"{r}={hu_counts_canon.get(r,0)} ", end="")
    print()
    
    # 克 ratio
    ben_ke = ben_counts.get('克体', 0) + ben_counts.get('体克用', 0)
    hu_ke = hu_counts_canon.get('克体', 0) + hu_counts_canon.get('体克用', 0)
    ben_sheng = ben_counts.get('生体', 0) + ben_counts.get('体生用', 0)
    hu_sheng = hu_counts_canon.get('生体', 0) + hu_counts_canon.get('体生用', 0)
    n = end - start
    print(f"    克 ratio: 本={ben_ke}/{n} ({100*ben_ke/n:.0f}%), "
          f"互={hu_ke}/{n} ({100*hu_ke/n:.0f}%)")
    print(f"    生 ratio: 本={ben_sheng}/{n} ({100*ben_sheng/n:.0f}%), "
          f"互={hu_sheng}/{n} ({100*hu_sheng/n:.0f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 5. 互 RELATION TRAJECTORY ALONG THE SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. 互 RELATION CHANGES ALONG THE SEQUENCE")
print("=" * 70)

# How does the 互 five-phase relation change from one hexagram to the next?
hu_rel_transitions = Counter()
for i in range(63):
    hu_rel_transitions[(hu_rels[i], hu_rels[i+1])] += 1

print(f"\n  互 relation transition matrix (consecutive hexagrams):")
print(f"  {'':>8s}", end="")
for r in rel_names:
    print(f"  {r:>6s}", end="")
print()
for r1 in rel_names:
    print(f"  {r1:>8s}", end="")
    for r2 in rel_names:
        c = hu_rel_transitions.get((r1, r2), 0)
        print(f"  {c:6d}", end="")
    print()

# ══════════════════════════════════════════════════════════════════════════════
# 6. KERNEL DISTANCE AND 互 DISTANCE CORRELATION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. BRIDGE KERNEL vs 互 DISTANCE")
print("=" * 70)

# For each bridge: kernel type → 互 distance
kernel_hu_dist = defaultdict(list)
for t in hu_transitions:
    k_name = kernel_names[t['kernel']]
    kernel_hu_dist[k_name].append(t['hu_dist'])

print(f"\n  Bridge kernel → 互 distance:")
for k in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    dists = kernel_hu_dist.get(k, [])
    in_h = k in ['id', 'O', 'MI', 'OMI']
    h_tag = " [H]" if in_h else "     "
    if dists:
        print(f"    {k:>3s}{h_tag}: mean={np.mean(dists):.2f}, values={sorted(Counter(dists).items())}, n={len(dists)}")

# Theoretical: H bridges should give 0 (id,O) or 6 (MI,OMI).
# Non-H bridges give 2 (M,OM) or 4 (I,OI).
# But that's only for PURE kernel operations. The actual bridge has
# orbit bits too, so the 互 distance isn't purely determined by kernel.

# Check: are id/O bridges always 互-distance 0?
print(f"\n  Verification:")
for k in ['id', 'O']:
    dists = kernel_hu_dist.get(k, [])
    all_zero = all(d == 0 for d in dists)
    print(f"    {k} bridges: 互 distance always 0? {all_zero} (values: {set(dists)})")

for k in ['MI', 'OMI']:
    dists = kernel_hu_dist.get(k, [])
    all_six = all(d == 6 for d in dists)
    print(f"    {k} bridges: 互 distance always 6? {all_six} (values: {set(dists)})")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE PAIR STRUCTURE IN 互-SPACE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. KW PAIRS IN 互-SPACE")
print("=" * 70)

# KW pairs consecutive hexagrams. Each pair maps to a pair of 互 values.
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1, hg2 = hugua(h1), hugua(h2)
    
    # Are they the same? complement? other?
    if hg1 == hg2:
        rel = "same"
    elif hg2 == hg1 ^ MASK_ALL:
        rel = "complement"
    else:
        d = hamming6(hg1, hg2)
        rel = f"d={d}"
    
    lo1, up1 = TRIGRAM_NAMES[lower_trigram(hg1)], TRIGRAM_NAMES[upper_trigram(hg1)]
    lo2, up2 = TRIGRAM_NAMES[lower_trigram(hg2)], TRIGRAM_NAMES[upper_trigram(hg2)]
    
    pair_idx = i // 2
    canon = "UC" if pair_idx < 15 else "LC"
    
    print(f"    Pair {pair_idx:2d} [{canon}]: {kw_names[i]:12s}→互={lo1}/{up1}  "
          f"{kw_names[i+1]:12s}→互={lo2}/{up2}  [{rel}]")

# Summary
pair_rels = Counter()
for i in range(0, 64, 2):
    hg1, hg2 = hugua(kw_hex[i]), hugua(kw_hex[i+1])
    if hg1 == hg2:
        pair_rels['same'] += 1
    elif hg2 == hg1 ^ MASK_ALL:
        pair_rels['complement'] += 1
    else:
        pair_rels['other'] += 1

print(f"\n  KW pair 互 relationship: {dict(pair_rels)}")

# By canon
for canon_name, start, end in [("Upper", 0, 15), ("Lower", 15, 32)]:
    rels = Counter()
    for pair_idx in range(start, end):
        hg1, hg2 = hugua(kw_hex[2*pair_idx]), hugua(kw_hex[2*pair_idx+1])
        if hg1 == hg2:
            rels['same'] += 1
        elif hg2 == hg1 ^ MASK_ALL:
            rels['complement'] += 1
        else:
            rels['other'] += 1
    print(f"  {canon_name}: {dict(rels)}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. CONVERGENCE POINTS IN THE SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. CONVERGENCE POINTS (互 fixed points in the sequence)")
print("=" * 70)

# The 4 fixed points of 互: 000000(Kun), 010101(WeiJi), 101010(JiJi), 111111(Qian)
# When do these appear as 互 values in the KW sequence?

fixed_points = {0b000000, 0b010101, 0b101010, 0b111111}
fp_names = {0b000000: 'Kun/Kun', 0b010101: 'Kan/Li(WeiJi)', 0b101010: 'Li/Kan(JiJi)', 0b111111: 'Qian/Qian'}

print(f"\n  Fixed points of 互 appearing in the sequence:")
for i in range(64):
    if hu_seq[i] in fixed_points:
        canon = "UC" if i < 30 else "LC"
        print(f"    Position {i+1:2d} [{canon}] {kw_names[i]:12s}: "
              f"互 = {fp_names[hu_seq[i]]}")

# How many hexagrams map to each fixed point?
for fp, name in fp_names.items():
    count = sum(1 for h in hu_seq if h == fp)
    positions = [i+1 for i in range(64) if hu_seq[i] == fp]
    print(f"\n  互 = {name}: {count} hexagrams at positions {positions}")

# ══════════════════════════════════════════════════════════════════════════════
# 9. THE SEQUENCE AS DIVINATION NARRATIVE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. SUMMARY: THE SEQUENCE AS DIVINATION STRUCTURE")
print("=" * 70)

# Compute overall statistics
upper_h = sum(1 for t in hu_transitions[:29] if t['in_h'])
lower_h = sum(1 for t in hu_transitions[30:] if t['in_h'])
upper_same = sum(1 for t in hu_transitions[:29] if t['hu_rel'] == 'same')
lower_same = sum(1 for t in hu_transitions[30:] if t['hu_rel'] == 'same')
upper_comp = sum(1 for t in hu_transitions[:29] if t['hu_rel'] == 'complement')
lower_comp = sum(1 for t in hu_transitions[30:] if t['hu_rel'] == 'complement')

print(f"""
  UPPER CANON (transitions 1-29):
    H bridges: {upper_h}/29 ({100*upper_h/29:.0f}%)
    互 unchanged: {upper_same}/29 ({100*upper_same/29:.0f}%)
    互 complemented: {upper_comp}/29 ({100*upper_comp/29:.0f}%)
    互 simple (same or complement): {upper_same+upper_comp}/29 ({100*(upper_same+upper_comp)/29:.0f}%)
    
  LOWER CANON (transitions 31-63):
    H bridges: {lower_h}/33 ({100*lower_h/33:.0f}%)
    互 unchanged: {lower_same}/33 ({100*lower_same/33:.0f}%)
    互 complemented: {lower_comp}/33 ({100*lower_comp/33:.0f}%)
    互 simple: {lower_same+lower_comp}/33 ({100*(lower_same+lower_comp)/33:.0f}%)
""")
