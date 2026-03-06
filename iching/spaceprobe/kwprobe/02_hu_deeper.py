"""
Deeper analysis of KW sequence through divination lens.

Key findings from round 1:
- Every 互 value appears exactly 4 times (perfectly uniform)
- 克 amplification: 41% → 62% (本→互)
- Lower Canon 互 克 is 71% vs Upper Canon 53%
- Fixed points split by canon: UC uses Qian/Kun, LC uses JiJi/WeiJi
- KW pair structure preserved through 互

Now dig into:
1. Is uniform 互 distribution forced or chosen?
2. The 克 asymmetry between canons — structural or accidental?
3. What does 互² (nuclear of nuclear) look like?
4. Does the 互 walk have simpler structure than the hex walk?
5. Trace the full 本→互→变 circuit through the sequence
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np
from itertools import permutations

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua, biangua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, kw_partner, reverse6,
    hamming6, popcount, bit, fmt6, fmt3,
)

# Build KW sequence
kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

# Removed: TRIGRAM_ELEMENT_NAME was dead code with wrong convention. Use TRIGRAM_ELEMENT from cycle_algebra.
ELEMENT_NAMES = ['Water', 'Wood', 'Fire', 'Earth', 'Metal']
FIVE_ELEMENTS = ['Water', 'Wood', 'Fire', 'Earth', 'Metal']

# ══════════════════════════════════════════════════════════════════════════════
# 1. IS UNIFORM 互 DISTRIBUTION FORCED?
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. IS UNIFORM 互 DISTRIBUTION FORCED?")
print("=" * 70)

# How many hexagrams map to each 互 value? (This is a property of the
# 互 function, not the KW sequence.)

hu_preimage = defaultdict(list)
for h in range(64):
    hg = hugua(h)
    hu_preimage[hg].append(h)

print(f"\n  互 preimage sizes (how many hexagrams → each 互 value):")
sizes = Counter(len(v) for v in hu_preimage.values())
for size, count in sorted(sizes.items()):
    print(f"    {count} values have preimage size {size}")

for hg in sorted(hu_preimage.keys()):
    lo, up = lower_trigram(hg), upper_trigram(hg)
    preimage = hu_preimage[hg]
    print(f"    互={fmt6(hg)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}): "
          f"{len(preimage)} hexagrams → {[fmt6(h) for h in preimage]}")

print(f"\n  → Every 互 value has exactly 4 preimages.")
print(f"  → UNIFORM DISTRIBUTION IS FORCED by the 互 function itself.")
print(f"  → The KW sequence visits all 64, so it must hit each 互 value 4 times.")

# ══════════════════════════════════════════════════════════════════════════════
# 2. 互² — NUCLEAR OF NUCLEAR
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. 互² — NUCLEAR OF NUCLEAR (CONVERGENCE)")
print("=" * 70)

# 互 erases outer lines. 互² erases more. Where does iterated 互 converge?

print(f"\n  Iterated 互 chains for all 64 hexagrams:")
convergence = {}
for h in range(64):
    chain = [h]
    current = h
    for _ in range(10):
        current = hugua(current)
        chain.append(current)
        if current == chain[-2]:  # Fixed point
            break
    convergence[h] = chain

# What are the fixed points of 互?
fixed_points = [h for h in range(64) if hugua(h) == h]
print(f"\n  Fixed points of 互: {[fmt6(h) for h in fixed_points]}")
for h in fixed_points:
    lo, up = lower_trigram(h), upper_trigram(h)
    print(f"    {fmt6(h)} = {TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}")

# How many steps to convergence?
steps_to_fix = {}
for h in range(64):
    chain = convergence[h]
    for i in range(len(chain) - 1):
        if chain[i] == chain[i+1]:
            steps_to_fix[h] = i
            break
    else:
        # Check for cycles
        seen = {}
        for i, v in enumerate(chain):
            if v in seen:
                steps_to_fix[h] = -1  # Cycle, not fixed point
                break
            seen[v] = i
        else:
            steps_to_fix[h] = len(chain) - 1

step_dist = Counter(steps_to_fix.values())
print(f"\n  Steps to fixed point distribution:")
for s, count in sorted(step_dist.items()):
    print(f"    {s} steps: {count} hexagrams")

# Show 互 chains for KW sequence
print(f"\n  互 convergence chains along KW sequence:")
for i in range(64):
    h = kw_hex[i]
    chain = convergence[h]
    chain_str = " → ".join(fmt6(c) for c in chain[:5])
    fp = chain[-1]
    fp_lo, fp_up = lower_trigram(fp), upper_trigram(fp)
    canon = "UC" if i < 30 else "LC"
    print(f"    {i+1:2d}. {kw_names[i]:12s} [{canon}]: {chain_str}  → {TRIGRAM_NAMES[fp_lo]}/{TRIGRAM_NAMES[fp_up]}")

# What fixed point does each hexagram converge to?
fp_groups = defaultdict(list)
for i in range(64):
    h = kw_hex[i]
    fp = convergence[h][-1]
    fp_groups[fp].append(i+1)  # KW position

print(f"\n  Fixed point basins (KW positions):")
for fp in sorted(fp_groups.keys()):
    lo, up = lower_trigram(fp), upper_trigram(fp)
    positions = fp_groups[fp]
    uc = [p for p in positions if p <= 30]
    lc = [p for p in positions if p > 30]
    print(f"    → {TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]} ({fmt6(fp)}): "
          f"{len(positions)} total (UC={len(uc)}, LC={len(lc)})")
    print(f"      UC: {uc}")
    print(f"      LC: {lc}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. 克 ASYMMETRY — FORCED OR SEQUENCE-DEPENDENT?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. 克 AMPLIFICATION — SEQUENCE vs COMBINATORICS")
print("=" * 70)

# Is the 克 amplification a property of ALL hexagrams or is it
# enhanced by the KW ordering?

# Global: for ALL 64 hexagrams
ben_rels_all = []
hu_rels_all = []
for h in range(64):
    lo, up = lower_trigram(h), upper_trigram(h)
    lo_e, up_e = TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up]
    
    hg = hugua(h)
    hg_lo, hg_up = lower_trigram(hg), upper_trigram(hg)
    hg_lo_e, hg_up_e = TRIGRAM_ELEMENT[hg_lo], TRIGRAM_ELEMENT[hg_up]
    
    ben_rels_all.append(five_phase_relation(lo_e, up_e))
    hu_rels_all.append(five_phase_relation(hg_lo_e, hg_up_e))

rel_names = ["比和", "生体", "克体", "体生用", "体克用"]
print(f"\n  ALL 64 hexagrams (no ordering):")
ben_c = Counter(ben_rels_all)
hu_c = Counter(hu_rels_all)
print(f"    本 relations: ", end="")
for r in rel_names:
    print(f"{r}={ben_c.get(r,0)} ", end="")
print()
print(f"    互 relations: ", end="")
for r in rel_names:
    print(f"{r}={hu_c.get(r,0)} ", end="")
print()

ben_ke = ben_c.get('克体', 0) + ben_c.get('体克用', 0)
hu_ke = hu_c.get('克体', 0) + hu_c.get('体克用', 0)
ben_sheng = ben_c.get('生体', 0) + ben_c.get('体生用', 0)
hu_sheng = hu_c.get('生体', 0) + hu_c.get('体生用', 0)

print(f"    克: 本={ben_ke}/64 ({100*ben_ke/64:.0f}%) → 互={hu_ke}/64 ({100*hu_ke/64:.0f}%)")
print(f"    生: 本={ben_sheng}/64 ({100*ben_sheng/64:.0f}%) → 互={hu_sheng}/64 ({100*hu_sheng/64:.0f}%)")
print(f"\n  → The 克 amplification is a property of the 互 function itself,")
print(f"     not of the KW sequence. KW sequence inherits it.")

# But is the CANON SPLIT an accident of which hexagrams are in which canon?
# Let's check: is there something about hex 1-30 vs 31-64 that makes 克 different?

# Actually, the canon split is by KW position. Let me check if the UC hexagrams
# just happen to have less 克 in their 互 values.
uc_hex = set(kw_hex[:30])
lc_hex = set(kw_hex[30:])

print(f"\n  Canon split:")
for name, hexset in [("Upper Canon hexagrams", uc_hex), ("Lower Canon hexagrams", lc_hex)]:
    ke_count = 0
    sheng_count = 0
    total = len(hexset)
    for h in hexset:
        hg = hugua(h)
        hg_lo, hg_up = lower_trigram(hg), upper_trigram(hg)
        rel = five_phase_relation(TRIGRAM_ELEMENT[hg_lo], TRIGRAM_ELEMENT[hg_up])
        if rel in ['克体', '体克用']:
            ke_count += 1
        elif rel in ['生体', '体生用']:
            sheng_count += 1
    print(f"    {name}: 互 克={ke_count}/{total} ({100*ke_count/total:.0f}%), "
          f"互 生={sheng_count}/{total} ({100*sheng_count/total:.0f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 4. THE 互 WALK — DOES IT SIMPLIFY THE SEQUENCE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. THE 互 WALK — PATTERN DETECTION")
print("=" * 70)

# The raw KW sequence visits 64 hexagrams.
# The 互 projection visits 16 values, each exactly 4 times.
# Does the walk on 互-space have a simpler pattern?

hu_seq = [hugua(kw_hex[i]) for i in range(64)]

# Look for repeating patterns in 互 walk
print(f"\n  互 walk (16-value sequence, length 64):")
# Convert to indices for pattern detection
hu_to_idx = {}
for i, hg in enumerate(sorted(set(hu_seq))):
    hu_to_idx[hg] = i
hu_idx_seq = [hu_to_idx[hg] for hg in hu_seq]
print(f"    Indexed: {hu_idx_seq}")

# Check if the walk has period-32 or period-16 symmetry
print(f"\n  Period-32 check (UC vs LC):")
matches_32 = sum(1 for i in range(32) if i + 32 < 64 and hu_idx_seq[i] == hu_idx_seq[i+32])
print(f"    Matches: {matches_32}/32")

# Check if pairs have consistent 互 relationship
print(f"\n  KW pair 互 relationship types:")
pair_hu_rels = []
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1, hg2 = hugua(h1), hugua(h2)
    
    # What's the relationship?
    xor = hg1 ^ hg2
    lo1, up1 = lower_trigram(hg1), upper_trigram(hg1)
    lo2, up2 = lower_trigram(hg2), upper_trigram(hg2)
    
    # Check specific patterns
    if hg1 == hg2:
        ptype = "same"
    elif hg2 == hg1 ^ MASK_ALL:
        ptype = "complement"
    elif hg2 == reverse6(hg1):
        ptype = "reverse"
    else:
        ptype = f"other(d={hamming6(hg1, hg2)})"
    
    pair_hu_rels.append(ptype)

print(f"    {Counter(pair_hu_rels)}")
print(f"\n    Detail:")
for i, ptype in enumerate(pair_hu_rels):
    canon = "UC" if i < 15 else "LC"
    print(f"      Pair {i:2d} [{canon}]: {ptype}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. PAIR TYPE AND 互 RELATIONSHIP
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. KW PAIR TYPE → 互 PAIR RELATIONSHIP (DERIVATION)")
print("=" * 70)

# Theory:
# If KW pair is (h, reverse(h)): 互(reverse(h)) = reverse(互(h))
# If KW pair is (h, complement(h)): 互(complement(h)) = complement(互(h))
# Verify this.

print(f"\n  Verification of 互 commutation with pair operations:")
correct_rev = 0
correct_comp = 0
total_rev = 0
total_comp = 0

for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1, hg2 = hugua(h1), hugua(h2)
    
    if h2 == reverse6(h1):
        total_rev += 1
        if hg2 == reverse6(hg1):
            correct_rev += 1
        else:
            print(f"    FAIL reverse: pair {i//2}, h1={fmt6(h1)}, h2={fmt6(h2)}, "
                  f"互(h1)={fmt6(hg1)}, 互(h2)={fmt6(hg2)}, rev(互(h1))={fmt6(reverse6(hg1))}")
    elif h2 == h1 ^ MASK_ALL:
        total_comp += 1
        if hg2 == hg1 ^ MASK_ALL:
            correct_comp += 1
        else:
            print(f"    FAIL complement: pair {i//2}, h1={fmt6(h1)}, h2={fmt6(h2)}, "
                  f"互(h1)={fmt6(hg1)}, 互(h2)={fmt6(hg2)}, comp(互(h1))={fmt6(hg1^MASK_ALL)}")
    else:
        print(f"    UNKNOWN pair type: pair {i//2}, h1={fmt6(h1)}, h2={fmt6(h2)}, "
              f"rev(h1)={fmt6(reverse6(h1))}, comp(h1)={fmt6(h1^MASK_ALL)}")

print(f"\n  Reverse pairs: {correct_rev}/{total_rev} commute correctly")
print(f"  Complement pairs: {correct_comp}/{total_comp} commute correctly")
print(f"\n  → 互 commutes with both reverse and complement.")
print(f"  → KW pair structure is EXACTLY preserved by 互 projection.")
print(f"  → If hex pair is reverse → 互 pair is reverse")
print(f"  → If hex pair is complement → 互 pair is complement")

# ══════════════════════════════════════════════════════════════════════════════
# 6. WHAT DOES REVERSE LOOK LIKE IN 互-SPACE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. REVERSE IN 互-SPACE")
print("=" * 70)

# For a reverse pair in hex-space, the 互 pair is also reverse.
# But reverse in hex-space might be "same" in 互-space (if 互 is palindromic).
# How many of the 16 互 values are palindromic?

palindromic = []
non_palindromic = []
for hg in sorted(set(hu_seq)):
    if reverse6(hg) == hg:
        palindromic.append(hg)
    else:
        non_palindromic.append(hg)

print(f"\n  Palindromic 互 values (reverse = self): {len(palindromic)}")
for hg in palindromic:
    lo, up = lower_trigram(hg), upper_trigram(hg)
    print(f"    {fmt6(hg)} = {TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}")

print(f"\n  Non-palindromic 互 values: {len(non_palindromic)}")
for hg in non_palindromic:
    lo, up = lower_trigram(hg), upper_trigram(hg)
    rev = reverse6(hg)
    rev_lo, rev_up = lower_trigram(rev), upper_trigram(rev)
    print(f"    {fmt6(hg)} = {TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]} ↔ "
          f"{fmt6(rev)} = {TRIGRAM_NAMES[rev_lo]}/{TRIGRAM_NAMES[rev_up]}")

# So for reverse hex pairs:
# - If their 互 is palindromic → same 互 value (distance 0)
# - If non-palindromic → reverse 互 pair (distance = hamming between value and its reverse)

# Check what KW reverse pairs look like
print(f"\n  Reverse hex pairs and their 互 relationship:")
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    if h2 != reverse6(h1):
        continue
    hg1 = hugua(h1)
    is_pal = (reverse6(hg1) == hg1)
    d = hamming6(hg1, reverse6(hg1))
    print(f"    Pair {i//2:2d}: {kw_names[i]:12s}/{kw_names[i+1]:12s} "
          f"互={fmt6(hg1)} palindromic={is_pal} 互-dist={d}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE 变 LAYER — CHANGING LINES IN SEQUENCE CONTEXT
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. 变卦 — EACH KW PAIR AS A DIVINATION READING")
print("=" * 70)

# In a divination reading, each KW pair can be seen as 本→变:
# The first hexagram is 本, the second is 变.
# Then 互 is the hidden layer.
# What do these readings look like?

print(f"\n  KW pairs as divination circuits (本→互→变):")
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1, hg2 = hugua(h1), hugua(h2)
    
    # 本 five-phase
    lo1, up1 = lower_trigram(h1), upper_trigram(h1)
    ben_rel = five_phase_relation(TRIGRAM_ELEMENT[lo1], TRIGRAM_ELEMENT[up1])
    
    # 互 five-phase  
    hg_lo, hg_up = lower_trigram(hg1), upper_trigram(hg1)
    hu_rel = five_phase_relation(TRIGRAM_ELEMENT[hg_lo], TRIGRAM_ELEMENT[hg_up])
    
    # 变 five-phase (= second hex of pair)
    lo2, up2 = lower_trigram(h2), upper_trigram(h2)
    bian_rel = five_phase_relation(TRIGRAM_ELEMENT[lo2], TRIGRAM_ELEMENT[up2])
    
    # Trajectory
    trajectory = f"{ben_rel} → {hu_rel} → {bian_rel}"
    
    canon = "UC" if i < 30 else "LC"
    print(f"    Pair {i//2:2d} [{canon}]: {kw_names[i]:12s}→{kw_names[i+1]:12s}  "
          f"{trajectory}")

# Count trajectory types
trajectories = Counter()
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1 = hugua(h1)
    
    lo1, up1 = lower_trigram(h1), upper_trigram(h1)
    ben_rel = five_phase_relation(TRIGRAM_ELEMENT[lo1], TRIGRAM_ELEMENT[up1])
    
    hg_lo, hg_up = lower_trigram(hg1), upper_trigram(hg1)
    hu_rel = five_phase_relation(TRIGRAM_ELEMENT[hg_lo], TRIGRAM_ELEMENT[hg_up])
    
    lo2, up2 = lower_trigram(h2), upper_trigram(h2)
    bian_rel = five_phase_relation(TRIGRAM_ELEMENT[lo2], TRIGRAM_ELEMENT[up2])
    
    trajectories[(ben_rel, hu_rel, bian_rel)] += 1

print(f"\n  Trajectory frequencies:")
for traj, count in sorted(trajectories.items(), key=lambda x: -x[1]):
    print(f"    {traj[0]} → {traj[1]} → {traj[2]}: {count}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. CONSECUTIVE PAIRS AS 变 — THE SEQUENCE AS READING
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. THE SEQUENCE AS A CHAIN OF READINGS")
print("=" * 70)

# Each step in the KW sequence: h[i] is 本, h[i+1] is 变.
# The changing lines = XOR between consecutive hexagrams.
# How many changing lines at each step?

changing_lines = []
for i in range(63):
    xor = kw_hex[i] ^ kw_hex[i+1]
    nchanging = bin(xor).count('1')
    changing_lines.append(nchanging)

print(f"\n  Changing lines between consecutive KW hexagrams:")
cl_dist = Counter(changing_lines)
for n in sorted(cl_dist.keys()):
    print(f"    {n} changing lines: {cl_dist[n]}/63 transitions")

print(f"  Mean changing lines: {np.mean(changing_lines):.2f}")

# By canon
uc_cl = changing_lines[:29]
lc_cl = changing_lines[30:]
print(f"  UC mean: {np.mean(uc_cl):.2f}, LC mean: {np.mean(lc_cl):.2f}")

# Divination: 0 changing lines = no movement. 6 = total transformation.
# What's the distribution?

# The full circuit for each step: 本[i] → 互[i] → 变[i+1]
# with 互 of 本[i]
print(f"\n  Full divination circuit along the sequence:")
print(f"  (reading each step as a mini-divination)")
print(f"\n  {'Step':>5s} {'本':>12s} {'互':>12s} {'变':>12s} {'CL':>3s} {'本rel':>8s} {'互rel':>8s} {'变rel':>8s}")

for i in range(63):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hg1 = hugua(h1)
    
    lo1, up1 = lower_trigram(h1), upper_trigram(h1)
    ben_rel = five_phase_relation(TRIGRAM_ELEMENT[lo1], TRIGRAM_ELEMENT[up1])
    
    hg_lo, hg_up = lower_trigram(hg1), upper_trigram(hg1)
    hu_rel = five_phase_relation(TRIGRAM_ELEMENT[hg_lo], TRIGRAM_ELEMENT[hg_up])
    
    lo2, up2 = lower_trigram(h2), upper_trigram(h2)
    bian_rel = five_phase_relation(TRIGRAM_ELEMENT[lo2], TRIGRAM_ELEMENT[up2])
    
    cl = changing_lines[i]
    
    canon = "UC" if i < 29 else ("X" if i == 29 else "LC")
    print(f"  {i+1:3d}→{i+2:<2d} {kw_names[i]:>12s} {fmt6(hg1):>12s} {kw_names[i+1]:>12s} "
          f"{cl:3d} {ben_rel:>8s} {hu_rel:>8s} {bian_rel:>8s}")

# ══════════════════════════════════════════════════════════════════════════════
# 9. COMPARISON: RANDOM SEQUENCES vs KW
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. KW 互 STATISTICS vs RANDOM SEQUENCES")
print("=" * 70)

# Monte Carlo: how special is KW's 互-projected five-phase distribution?
np.random.seed(42)
n_trials = 100000

# KW actual: 互 克 ratio per canon
kw_uc_ke = sum(1 for i in range(30) 
               if five_phase_relation(
                   TRIGRAM_ELEMENT[lower_trigram(hugua(kw_hex[i]))],
                   TRIGRAM_ELEMENT[upper_trigram(hugua(kw_hex[i]))]
               ) in ['克体', '体克用'])

kw_lc_ke = sum(1 for i in range(30, 64) 
               if five_phase_relation(
                   TRIGRAM_ELEMENT[lower_trigram(hugua(kw_hex[i]))],
                   TRIGRAM_ELEMENT[upper_trigram(hugua(kw_hex[i]))]
               ) in ['克体', '体克用'])

# All 64 hexagrams' 互 克 status
hu_ke_flags = []
for h in range(64):
    hg = hugua(h)
    rel = five_phase_relation(
        TRIGRAM_ELEMENT[lower_trigram(hg)],
        TRIGRAM_ELEMENT[upper_trigram(hg)]
    )
    hu_ke_flags.append(1 if rel in ['克体', '体克用'] else 0)

total_ke = sum(hu_ke_flags)
print(f"\n  Total hexagrams with 互-克: {total_ke}/64")
print(f"  KW Upper Canon 互-克: {kw_uc_ke}/30")
print(f"  KW Lower Canon 互-克: {kw_lc_ke}/34")

# For random partitions of 64 hexagrams into 30 (UC) and 34 (LC):
# what's the distribution of 互-克 in UC?
uc_ke_counts = []
lc_ke_counts = []
diff_counts = []
all_hex = list(range(64))

for _ in range(n_trials):
    perm = np.random.permutation(64)
    uc = perm[:30]
    lc = perm[30:]
    
    uc_ke = sum(hu_ke_flags[h] for h in uc)
    lc_ke = sum(hu_ke_flags[h] for h in lc)
    
    uc_ke_counts.append(uc_ke)
    lc_ke_counts.append(lc_ke)
    diff_counts.append(lc_ke - uc_ke)

uc_ke_counts = np.array(uc_ke_counts)
lc_ke_counts = np.array(lc_ke_counts)
diff_counts = np.array(diff_counts)

kw_diff = kw_lc_ke - kw_uc_ke
pctl = np.mean(diff_counts >= kw_diff) * 100

print(f"\n  Random partition test (100k trials):")
print(f"    UC 互-克 mean={np.mean(uc_ke_counts):.1f}, std={np.std(uc_ke_counts):.1f}")
print(f"    LC 互-克 mean={np.mean(lc_ke_counts):.1f}, std={np.std(lc_ke_counts):.1f}")
print(f"    LC-UC diff mean={np.mean(diff_counts):.1f}, std={np.std(diff_counts):.1f}")
print(f"    KW diff = {kw_diff}")
print(f"    KW percentile: {100-pctl:.1f}th (fraction ≥ KW: {pctl:.2f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 10. DOES THE 互 WALK FOLLOW THE KW PAIR GROUPING?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. 互 WALK SYMMETRY — PAIR GROUPS")
print("=" * 70)

# The 16 互 values pair as:
# - 4 palindromic values pair with themselves  
# - 12 non-palindromic form 6 reverse pairs
# So the 16 values form 4 + 6 = 10 pair orbits under reverse.

# Under complement:
# - 4 fixed points: those with 3 ones (self-complement? no, 000000↔111111, etc.)
# Actually complement pairs each 互 value with its bitwise complement.

print(f"\n  互 value orbit structure (reverse × complement):")
seen = set()
orbits = []
for hg in sorted(set(hu_seq)):
    if hg in seen:
        continue
    orbit = {hg}
    orbit.add(reverse6(hg))
    orbit.add(hg ^ MASK_ALL)
    orbit.add(reverse6(hg ^ MASK_ALL))
    for x in list(orbit):
        seen.add(x)
    orbit_list = sorted(orbit)
    orbits.append(orbit_list)
    
    orbit_str = ", ".join(f"{fmt6(x)}({TRIGRAM_NAMES[lower_trigram(x)]}/{TRIGRAM_NAMES[upper_trigram(x)]})" 
                          for x in orbit_list)
    print(f"    Orbit (size {len(orbit_list)}): {orbit_str}")

print(f"\n  {len(orbits)} orbits total")

# Each orbit should appear 4*orbit_size times in the sequence.
# For size-4 orbits: each value appears 4 times, so 16 hexagrams map to this orbit.
# For size-2 orbits: each value appears 4 times, so 8 hexagrams.
# For size-1 orbits: 4 hexagrams.
for orb in orbits:
    count = sum(1 for h in hu_seq if h in set(orb))
    print(f"    Orbit {[fmt6(x) for x in orb]}: appears {count} times in KW sequence")
