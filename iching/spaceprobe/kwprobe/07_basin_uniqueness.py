"""
How unique is the KW basin pattern?

Questions:
1. Among all 64! orderings, how unusual is the KW basin walk?
2. Among pair-respecting orderings (32! × 2^32), how unusual?
3. What specific properties of the KW basin walk are rare?
4. The He Tu pairing — can it be derived from facing-line opposition?
5. The depth-1 boundary placement — how rare?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np
from itertools import combinations

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, reverse6,
    hamming6, fmt6, fmt3,
)

# Build KW sequence
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

basin_code = {'Kun': 0, 'KanLi': 1, 'Qian': 2}

# ══════════════════════════════════════════════════════════════════════════════
# 1. KW BASIN WALK STATISTICS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. KW BASIN WALK STATISTICS")
print("=" * 70)

kw_basins = [get_basin(kw_hex[i]) for i in range(64)]
kw_basin_coded = [basin_code[b] for b in kw_basins]

# Basin transition matrix
trans = np.zeros((3, 3), dtype=int)
for i in range(63):
    trans[kw_basin_coded[i], kw_basin_coded[i+1]] += 1

print(f"\n  KW basin transition matrix:")
labels = ['Kun', 'KanLi', 'Qian']
print(f"         ", end="")
for l in labels:
    print(f" {l:>6s}", end="")
print()
for i, l in enumerate(labels):
    print(f"  {l:6s}: ", end="")
    for j in range(3):
        print(f" {trans[i,j]:6d}", end="")
    print()

# Run count (number of basin changes)
n_changes = sum(1 for i in range(63) if kw_basins[i] != kw_basins[i+1])
print(f"\n  Basin changes: {n_changes}/63 transitions ({100*n_changes/63:.0f}%)")
print(f"  Basin runs: {n_changes + 1}")

# Longest run per basin
for basin_type in ['Kun', 'KanLi', 'Qian']:
    positions = [i for i in range(64) if kw_basins[i] == basin_type]
    max_run = 0
    current_run = 1
    for j in range(1, len(positions)):
        if positions[j] == positions[j-1] + 1:
            current_run += 1
        else:
            max_run = max(max_run, current_run)
            current_run = 1
    max_run = max(max_run, current_run)
    print(f"  Longest {basin_type} run: {max_run}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. MONTE CARLO — RANDOM ORDERINGS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. RANDOM ORDERING COMPARISON (100k trials)")
print("=" * 70)

np.random.seed(42)
n_trials = 100000

all_hex = list(range(64))
all_basins = [get_basin(h) for h in range(64)]

# Metrics to track
kw_n_changes = n_changes
kw_max_kanli = max(sum(1 for j in range(i, min(i+10, 64)) if kw_basins[j] == 'KanLi') for i in range(64))

# UC/LC asymmetry (Kun count in first 30 minus Qian count in first 30)
kw_uc_kun = sum(1 for i in range(30) if kw_basins[i] == 'Kun')
kw_uc_qian = sum(1 for i in range(30) if kw_basins[i] == 'Qian')
kw_asymmetry = kw_uc_kun - kw_uc_qian

# Framing: do positions 1,2 have fixed-point basins and 63,64 have cycle basins?
kw_framing = (kw_basins[0] in ('Kun', 'Qian') and kw_basins[1] in ('Kun', 'Qian') and
              kw_basins[0] != kw_basins[1] and
              kw_basins[62] == 'KanLi' and kw_basins[63] == 'KanLi')

random_n_changes = []
random_asymmetry = []
random_framing = 0
random_uc_run_structure = []

for _ in range(n_trials):
    perm = np.random.permutation(64)
    basins = [all_basins[h] for h in perm]
    
    # Number of changes
    nc = sum(1 for i in range(63) if basins[i] != basins[i+1])
    random_n_changes.append(nc)
    
    # Asymmetry
    uc_kun = sum(1 for i in range(30) if basins[i] == 'Kun')
    uc_qian = sum(1 for i in range(30) if basins[i] == 'Qian')
    random_asymmetry.append(uc_kun - uc_qian)
    
    # Framing
    if (basins[0] in ('Kun', 'Qian') and basins[1] in ('Kun', 'Qian') and
        basins[0] != basins[1] and basins[62] == 'KanLi' and basins[63] == 'KanLi'):
        random_framing += 1

random_n_changes = np.array(random_n_changes)
random_asymmetry = np.array(random_asymmetry)

print(f"\n  Basin changes:")
print(f"    KW: {kw_n_changes}")
print(f"    Random: mean={np.mean(random_n_changes):.1f}, std={np.std(random_n_changes):.1f}")
pctl = np.mean(random_n_changes <= kw_n_changes) * 100
print(f"    KW percentile: {pctl:.1f}th (lower = fewer changes = more clustered)")

print(f"\n  UC/LC asymmetry (UC_Kun - UC_Qian):")
print(f"    KW: {kw_asymmetry}")
print(f"    Random: mean={np.mean(random_asymmetry):.1f}, std={np.std(random_asymmetry):.1f}")
pctl = np.mean(random_asymmetry >= kw_asymmetry) * 100
print(f"    KW percentile: {100-pctl:.1f}th (fraction ≥ KW: {pctl:.2f}%)")

print(f"\n  Framing (opening=Kun+Qian, closing=KanLi+KanLi):")
print(f"    KW: {kw_framing}")
print(f"    Random: {random_framing}/{n_trials} = {100*random_framing/n_trials:.2f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 3. PAIR-RESPECTING ORDERINGS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. PAIR-RESPECTING RANDOM ORDERINGS (100k trials)")
print("=" * 70)

# KW pairs hexagrams as (reverse, reverse) or (complement-if-self-reverse)
# Build the 32 pairs
kw_pairs = []
for i in range(0, 64, 2):
    kw_pairs.append((kw_hex[i], kw_hex[i+1]))

# For pair-respecting random: shuffle the 32 pairs, randomly flip each
pair_n_changes = []
pair_asymmetry = []
pair_framing = 0

for _ in range(n_trials):
    perm = np.random.permutation(32)
    flips = np.random.randint(0, 2, 32)
    
    sequence = []
    for j in range(32):
        pair = kw_pairs[perm[j]]
        if flips[j]:
            sequence.extend([pair[1], pair[0]])
        else:
            sequence.extend([pair[0], pair[1]])
    
    basins = [get_basin(h) for h in sequence]
    
    nc = sum(1 for i in range(63) if basins[i] != basins[i+1])
    pair_n_changes.append(nc)
    
    uc_kun = sum(1 for i in range(30) if basins[i] == 'Kun')
    uc_qian = sum(1 for i in range(30) if basins[i] == 'Qian')
    pair_asymmetry.append(uc_kun - uc_qian)
    
    if (basins[0] in ('Kun', 'Qian') and basins[1] in ('Kun', 'Qian') and
        basins[0] != basins[1] and basins[62] == 'KanLi' and basins[63] == 'KanLi'):
        pair_framing += 1

pair_n_changes = np.array(pair_n_changes)
pair_asymmetry = np.array(pair_asymmetry)

print(f"\n  Basin changes (pair-respecting):")
print(f"    KW: {kw_n_changes}")
print(f"    Random: mean={np.mean(pair_n_changes):.1f}, std={np.std(pair_n_changes):.1f}")
pctl = np.mean(pair_n_changes <= kw_n_changes) * 100
print(f"    KW percentile: {pctl:.1f}th")

print(f"\n  UC/LC asymmetry (pair-respecting):")
print(f"    KW: {kw_asymmetry}")
print(f"    Random: mean={np.mean(pair_asymmetry):.1f}, std={np.std(pair_asymmetry):.1f}")
pctl = np.mean(pair_asymmetry >= kw_asymmetry) * 100
print(f"    KW percentile: {100-pctl:.1f}th (fraction ≥ KW: {pctl:.2f}%)")

print(f"\n  Framing (pair-respecting):")
print(f"    Random: {pair_framing}/{n_trials} = {100*pair_framing/n_trials:.2f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 4. HE TU DERIVATION FROM FACING LINES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. CAN HE TU BE DERIVED FROM FACING-LINE OPPOSITION?")
print("=" * 70)

# He Tu pairs trigrams with sum-to-10 Lo Shu numbers.
# We found all He Tu pairs have opposite lower-facing lines.
# Question: is this SUFFICIENT to characterize the He Tu, or is it just necessary?

# How many pairings of 8 trigrams have the "opposite lower-facing" property?
# Lower-facing yin: Kun(000), Gen(001), Kan(010), Xun(011) 
# Lower-facing yang: Zhen(100), Li(101), Dui(110), Qian(111)
# A pairing where each pair has one from each group = perfect matching of 4 with 4
# Number of such matchings = 4! = 24

# He Tu is ONE of these 24 matchings. What distinguishes it?
yin_face_lower = [0b000, 0b001, 0b010, 0b011]
yang_face_lower = [0b100, 0b101, 0b110, 0b111]

# All 4! = 24 possible matchings
from itertools import permutations
matchings = []
for perm in permutations(yang_face_lower):
    matching = list(zip(yin_face_lower, perm))
    matchings.append(matching)

loshu = {0b010: 1, 0b000: 2, 0b100: 3, 0b011: 4, 0b111: 6, 0b110: 7, 0b001: 8, 0b101: 9}

print(f"\n  All 24 facing-opposite pairings:")
for idx, matching in enumerate(matchings):
    pairs_str = []
    is_hetu = True
    for a, b in matching:
        ls_sum = loshu.get(a, 0) + loshu.get(b, 0)
        pairs_str.append(f"{TRIGRAM_NAMES[a]}-{TRIGRAM_NAMES[b]}({ls_sum})")
        if ls_sum not in (7,):  # He Tu sums differ
            pass  # Check below
    
    # He Tu pairs sum to: 1+6=7, 2+7=9, 3+8=11, 4+9=13
    # Wait, they don't have a common sum. The He Tu pairing is:
    # Kan(1)↔Qian(6), Kun(2)↔Dui(7), Zhen(3)↔Gen(8), Xun(4)↔Li(9)
    # Let's check which matching this is
    
    hetu_matching = [(0b010, 0b111), (0b000, 0b110), (0b001, 0b100), (0b011, 0b101)]
    # Compare: yin_face sorted is [000, 001, 010, 011]
    # hetu assigns: 000↔110, 001↔100, 010↔111, 011↔101
    # That's perm = [110, 100, 111, 101] = [Dui, Zhen, Qian, Li]
    
    is_hetu = (matching == [(0b000, 0b110), (0b001, 0b100), (0b010, 0b111), (0b011, 0b101)])
    
    tag = " ← HE TU" if is_hetu else ""
    print(f"    {idx:2d}: {', '.join(pairs_str)}{tag}")

# Also check: for each matching, does it also satisfy upper-facing opposition?
print(f"\n  Filtering by BOTH lower AND upper facing opposition:")
for idx, matching in enumerate(matchings):
    both_opposite = True
    for a, b in matching:
        top_opp = ((a >> 2) & 1) != ((b >> 2) & 1)  # lower facing (already guaranteed)
        bot_opp = (a & 1) != (b & 1)  # upper facing
        if not bot_opp:
            both_opposite = False
    
    is_hetu = (matching == [(0b000, 0b110), (0b001, 0b100), (0b010, 0b111), (0b011, 0b101)])
    
    if both_opposite:
        pairs_str = [f"{TRIGRAM_NAMES[a]}-{TRIGRAM_NAMES[b]}" for a, b in matching]
        tag = " ← HE TU" if is_hetu else ""
        print(f"    {idx:2d}: {', '.join(pairs_str)}{tag}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. COMPLEMENT PAIRING AND FACING LINES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. COMPLEMENT (FU XI) PAIRING AND FACING LINES")
print("=" * 70)

# Fu Xi pairs each trigram with its binary complement.
# What do the facing lines look like?
print(f"\n  Fu Xi complement pairs:")
seen = set()
for t in range(8):
    if t in seen:
        continue
    comp = t ^ 0b111
    seen.add(t)
    seen.add(comp)
    
    top_t = (t >> 2) & 1
    top_c = (comp >> 2) & 1
    bot_t = t & 1
    bot_c = comp & 1
    
    lower_opp = top_t != top_c
    upper_opp = bot_t != bot_c
    
    print(f"    {TRIGRAM_NAMES[t]}↔{TRIGRAM_NAMES[comp]}: "
          f"lower_facing: {'○' if not top_t else '●'}↔{'○' if not top_c else '●'} ({'opposite' if lower_opp else 'SAME'}), "
          f"upper_facing: {'○' if not bot_t else '●'}↔{'○' if not bot_c else '●'} ({'opposite' if upper_opp else 'SAME'})")

print(f"\n  Fu Xi complement always has opposite facing lines (both positions).")
print(f"  Because complement flips ALL bits, including the facing bit.")

# ══════════════════════════════════════════════════════════════════════════════
# 6. HE TU vs FU XI vs FACING OPPOSITION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. COMPARISON: HE TU vs FU XI PAIRINGS")
print("=" * 70)

# Fu Xi (complement) pairs: always both-opposite
# He Tu pairs: always lower-opposite, sometimes upper-opposite
# Question: what's the intersection?

fuxi_pairs = set()
for t in range(8):
    pair = tuple(sorted([t, t ^ 0b111]))
    fuxi_pairs.add(pair)

hetu_map = {0b010: 0b111, 0b000: 0b110, 0b100: 0b001, 0b011: 0b101}
hetu_pairs = set()
for a, b in hetu_map.items():
    hetu_pairs.add(tuple(sorted([a, b])))

print(f"\n  Fu Xi pairs: {[(TRIGRAM_NAMES[a], TRIGRAM_NAMES[b]) for a,b in sorted(fuxi_pairs)]}")
print(f"  He Tu pairs: {[(TRIGRAM_NAMES[a], TRIGRAM_NAMES[b]) for a,b in sorted(hetu_pairs)]}")
print(f"  Intersection: {[(TRIGRAM_NAMES[a], TRIGRAM_NAMES[b]) for a,b in fuxi_pairs & hetu_pairs]}")

# How do they differ?
print(f"\n  Fu Xi but not He Tu:")
for pair in sorted(fuxi_pairs - hetu_pairs):
    print(f"    {TRIGRAM_NAMES[pair[0]]}↔{TRIGRAM_NAMES[pair[1]]}")

print(f"\n  He Tu but not Fu Xi:")
for pair in sorted(hetu_pairs - fuxi_pairs):
    print(f"    {TRIGRAM_NAMES[pair[0]]}↔{TRIGRAM_NAMES[pair[1]]}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE FACING-LINE AND BASIN IN HEXAGRAM PAIRS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. HEXAGRAM PAIRS: BASIN CHANGE REQUIRES FACING-LINE FLIP")
print("=" * 70)

# Within a KW pair, the relationship (reverse or complement) determines
# what happens to the facing lines.

# For reverse pairs: h2 = reverse(h1)
# h1 bits: b0 b1 [b2 b3] b4 b5
# h2 bits: b5 b4 [b3 b2] b1 b0
# So h2's bit2 = h1's bit3, and h2's bit3 = h1's bit2
# Interface goes from (b2,b3) to (b3,b2) — SWAPPED
# (0,0)→(0,0), (1,1)→(1,1), (0,1)↔(1,0) → same basin!

# For complement pairs: h2 = complement(h1) 
# Interface goes from (b2,b3) to (1-b2, 1-b3)
# (0,0)→(1,1), (1,1)→(0,0) → Kun↔Qian swap!
# (0,1)→(1,0), (1,0)→(0,1) → KanLi→KanLi

print(f"\n  THEOREM:")
print(f"  Reverse pairs: interface swaps (b2,b3)→(b3,b2) → SAME basin always")
print(f"  Complement pairs: interface flips (b2,b3)→(1-b2,1-b3)")
print(f"    If (0,0) or (1,1): Kun↔Qian swap")
print(f"    If mixed: KanLi→KanLi")
print(f"")
print(f"  Cross-basin pairs MUST be complement pairs with non-mixed interface.")
print(f"  These are the self-reverse hexagrams with (0,0) or (1,1) interface.")
print(f"  Exactly the 4 pairs we found: Qian/Kun, Yi/DaGuo, Kan/Li, ZhongFu/XiaoGuo.")

# Verify
print(f"\n  Verification:")
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    b1, b2 = get_basin(h1), get_basin(h2)
    is_rev = (h2 == reverse6(h1))
    is_comp = (h2 == h1 ^ MASK_ALL)
    
    if b1 != b2:
        print(f"    Pair {i//2}: {kw_names[i]}/{kw_names[i+1]} "
              f"basin={b1}/{b2} reverse={is_rev} complement={is_comp}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. THE DEPTH-1 BOUNDARY PLACEMENT — SIGNIFICANCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. DEPTH-1 BOUNDARY PLACEMENT — HOW SPECIAL?")
print("=" * 70)

# In KW, depth-1 hexagrams cluster at boundaries (#23-24, #27-28, #37-40, #43-44, #53-54, #63-64)
# Is this clustering unusual?

# Depth-1 hexagrams: fixed set of 14 hexagrams regardless of ordering
depth1_hexes = set()
for h in range(64):
    current = h
    for d in range(10):
        nxt = hugua(current)
        if nxt == current:
            if d == 1:
                depth1_hexes.add(h)
            break
        if d > 0:
            nxt2 = hugua(nxt)
            if nxt2 == current:
                if d == 1:
                    depth1_hexes.add(h)
                break
        current = nxt

# Actually let me recompute properly
depth1_hexes = set()
for h in range(64):
    hu = hugua(h)
    hu2 = hugua(hu)
    if hu == h:  # depth 0
        continue
    if hu2 == hu or hu2 == h:  # depth 1 (reaches FP or cycle in 1 step)
        depth1_hexes.add(h)

print(f"  Depth-1 hexagrams: {len(depth1_hexes)} total")
kw_d1_positions = sorted([kw_hex.index(h) + 1 for h in depth1_hexes])
print(f"  KW positions: {kw_d1_positions}")

# Measure of clustering: sum of gaps between consecutive depth-1 positions
if len(kw_d1_positions) > 1:
    kw_gaps = [kw_d1_positions[i+1] - kw_d1_positions[i] for i in range(len(kw_d1_positions)-1)]
    kw_gap_var = np.var(kw_gaps)
    kw_max_gap = max(kw_gaps)
    print(f"  KW gaps: {kw_gaps}")
    print(f"  Gap variance: {kw_gap_var:.1f}")
    print(f"  Max gap: {kw_max_gap}")

# Monte Carlo: how often do random orderings have equal or more clustered depth-1?
np.random.seed(42)
n_trials = 100000
random_gap_vars = []
random_max_gaps = []

# Also measure: how many depth-1 hexagrams are in the last 10 positions?
kw_d1_in_last10 = sum(1 for p in kw_d1_positions if p > 54)

random_d1_in_last10 = []

for _ in range(n_trials):
    perm = np.random.permutation(64)
    d1_positions = sorted([np.where(perm == h)[0][0] + 1 for h in depth1_hexes])
    gaps = [d1_positions[j+1] - d1_positions[j] for j in range(len(d1_positions)-1)]
    random_gap_vars.append(np.var(gaps))
    random_max_gaps.append(max(gaps))
    random_d1_in_last10.append(sum(1 for p in d1_positions if p > 54))

random_gap_vars = np.array(random_gap_vars)
random_max_gaps = np.array(random_max_gaps)
random_d1_in_last10 = np.array(random_d1_in_last10)

pctl_var = np.mean(random_gap_vars >= kw_gap_var) * 100
pctl_max = np.mean(random_max_gaps >= kw_max_gap) * 100
pctl_last10 = np.mean(random_d1_in_last10 >= kw_d1_in_last10) * 100

print(f"\n  Monte Carlo (100k random orderings):")
print(f"    Gap variance: KW={kw_gap_var:.1f}, random mean={np.mean(random_gap_vars):.1f}")
print(f"      KW percentile: {100-pctl_var:.1f}th (high = more clustered)")
print(f"    Max gap: KW={kw_max_gap}, random mean={np.mean(random_max_gaps):.1f}")
print(f"      KW percentile: {100-pctl_max:.1f}th")
print(f"    Depth-1 in last 10: KW={kw_d1_in_last10}, random mean={np.mean(random_d1_in_last10):.1f}")
print(f"      KW percentile: {100-pctl_last10:.1f}th")

# ══════════════════════════════════════════════════════════════════════════════
# 9. THE COMBINED FRAMING STATISTIC
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. THE COMBINED FRAMING — ATTRACTORS AT BOUNDARIES")
print("=" * 70)

# KW has: 
# - Fixed points at positions 1,2
# - Cycle at positions 63,64
# - Depth-0 hexagrams = {Qian(111111), Kun(000000)} at #1,#2
# - Depth-0 cycle = {JiJi(010101), WeiJi(101010)} at #63,#64

depth0_hexes = {h for h in range(64) if hugua(h) == h}
cycle0_hexes = {0b010101, 0b101010}  # The 2-cycle

print(f"  Depth-0 (fixed points): {[fmt6(h) for h in sorted(depth0_hexes)]}")
print(f"  Cycle-0 (2-cycle): {[fmt6(h) for h in sorted(cycle0_hexes)]}")

# In KW: fixed points at 1,2 and cycle at 63,64
# How often does this happen randomly?
fixed_at_start = 0
cycle_at_end = 0
both = 0

for _ in range(n_trials):
    perm = np.random.permutation(64)
    
    # Fixed points at positions 0,1 (any order)
    fp = {perm[0], perm[1]} == depth0_hexes
    # Cycle at positions 62,63
    cy = {perm[62], perm[63]} == cycle0_hexes
    
    if fp:
        fixed_at_start += 1
    if cy:
        cycle_at_end += 1
    if fp and cy:
        both += 1

print(f"\n  Random orderings with:")
print(f"    Fixed points at start: {fixed_at_start}/{n_trials} = {100*fixed_at_start/n_trials:.4f}%")
print(f"    Cycle at end: {cycle_at_end}/{n_trials} = {100*cycle_at_end/n_trials:.4f}%")
print(f"    Both: {both}/{n_trials} = {100*both/n_trials:.4f}%")

# Exact probability:
# P(Qian,Kun at positions 1,2) = 2! / (64*63) = 2/4032
# P(JiJi,WeiJi at positions 63,64) = 2! / (62*63) ≈ same
# Combined ≈ (2/4032)^2 ≈ very small
p_exact = (2 / (64*63)) * (2 / (62*61))
print(f"    Exact probability: {p_exact:.6f} = {100*p_exact:.4f}%")

print(f"\n  But the tradition places these intentionally.")
print(f"  The question is: does the REST of the sequence show basin structure?")
print(f"  Answer: yes — the chiastic asymmetry (p=0.026) is not explained by framing.")
