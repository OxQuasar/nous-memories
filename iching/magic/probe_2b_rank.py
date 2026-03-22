#!/usr/bin/env python3
"""
Probe 2b: Palace rank structure, zero cells, and Z₅ sum distribution.
"""

import json
import numpy as np
from collections import Counter, defaultdict

with open('memories/iching/atlas-hzl/hzl_profiles.json') as f:
    hzl = json.load(f)

ELEMENTS = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}
ALG_Z5 = {'Wood': 0, 'Fire': 1, 'Earth': 2, 'Metal': 3, 'Water': 4}
RANK_NAMES = ['本宮', '一世', '二世', '三世', '四世', '五世', '游魂', '歸魂']

results = []
results.append("# Probe 2b: Palace Rank Structure, Zero Cells, and Z₅ Sum Distribution\n")


# ══════════════════════════════════════════════════════════════
# PART 1: Zero Cells — Why (L1,Metal) and (L2,Metal) are zero
# ══════════════════════════════════════════════════════════════

results.append("## Part 1: Zero Cells and 納甲 Branch Structure\n")

# Step 1: For each trigram, extract its lower and upper element assignments
# Group hexagrams to find unique trigram→element mappings
# Key insight: the element pattern depends on the trigram's 天干 (stem),
# which comes from the 納甲 system. Different trigrams have different stems.

# Build trigram element maps from data
# We need to identify trigrams. The hex_binary field gives the 6-bit pattern.
# Lower trigram = bits [0:3], upper trigram = bits [3:6]

# First: find all distinct (stem_triple, element_triple) for lower and upper
lower_trig_map = {}  # stem_triple → element_triple
upper_trig_map = {}

for h in hzl:
    lower_stems = tuple(h['lines'][i]['stem'] for i in range(3))
    lower_elems = tuple(h['lines'][i]['element'] for i in range(3))
    lower_branches = tuple(h['lines'][i]['branch'] for i in range(3))
    
    upper_stems = tuple(h['lines'][i]['stem'] for i in range(3, 6))
    upper_elems = tuple(h['lines'][i]['element'] for i in range(3, 6))
    upper_branches = tuple(h['lines'][i]['branch'] for i in range(3, 6))
    
    stem = lower_stems[0]  # all 3 are same for a trigram
    if stem not in lower_trig_map:
        lower_trig_map[stem] = (lower_branches, lower_elems)
    
    stem_u = upper_stems[0]
    if stem_u not in upper_trig_map:
        upper_trig_map[stem_u] = (upper_branches, upper_elems)

# The 納甲 stem assignments:
# 乾→甲(lower)/壬(upper), 坤→乙(lower)/癸(upper)
# 震→庚, 巽→辛, 坎→戊, 離→己, 艮→丙, 兌→丁

TRIG_NAMES = {
    '甲': '乾', '乙': '坤', '庚': '震', '辛': '巽',
    '戊': '坎', '己': '離', '丙': '艮', '丁': '兌',
    '壬': '乾', '癸': '坤'
}

results.append("### 1a. Lower trigram 納甲 assignments (L1, L2, L3):\n")
results.append(f"{'Stem':>4s}  {'Trigram':>6s}  {'L1 branch':>10s}  {'L1 elem':>8s}  "
               f"{'L2 branch':>10s}  {'L2 elem':>8s}  {'L3 branch':>10s}  {'L3 elem':>8s}")
results.append("-" * 80)

for stem in sorted(lower_trig_map.keys()):
    branches, elems = lower_trig_map[stem]
    trig = TRIG_NAMES.get(stem, '?')
    results.append(f"{stem:>4s}  {trig:>6s}  {branches[0]:>10s}  {elems[0]:>8s}  "
                   f"{branches[1]:>10s}  {elems[1]:>8s}  {branches[2]:>10s}  {elems[2]:>8s}")

results.append("")
results.append("### 1b. Upper trigram 納甲 assignments (L4, L5, L6):\n")
results.append(f"{'Stem':>4s}  {'Trigram':>6s}  {'L4 branch':>10s}  {'L4 elem':>8s}  "
               f"{'L5 branch':>10s}  {'L5 elem':>8s}  {'L6 branch':>10s}  {'L6 elem':>8s}")
results.append("-" * 80)

for stem in sorted(upper_trig_map.keys()):
    branches, elems = upper_trig_map[stem]
    trig = TRIG_NAMES.get(stem, '?')
    results.append(f"{stem:>4s}  {trig:>6s}  {branches[0]:>10s}  {elems[0]:>8s}  "
                   f"{branches[1]:>10s}  {elems[1]:>8s}  {branches[2]:>10s}  {elems[2]:>8s}")

results.append("")

# Step 2: Build per-position element possibility set
results.append("### 1c. Possible elements at each position:\n")

# For lower positions (L1, L2, L3): collect all elements across all trigrams
lower_possible = [set() for _ in range(3)]
for branches, elems in lower_trig_map.values():
    for i in range(3):
        lower_possible[i].add(elems[i])

upper_possible = [set() for _ in range(3)]
for branches, elems in upper_trig_map.values():
    for i in range(3):
        upper_possible[i].add(elems[i])

for i in range(3):
    missing = set(ELEMENTS) - lower_possible[i]
    results.append(f"L{i+1}: possible = {sorted(lower_possible[i])}, "
                   f"IMPOSSIBLE = {sorted(missing) if missing else '∅'}")

for i in range(3):
    missing = set(ELEMENTS) - upper_possible[i]
    results.append(f"L{i+4}: possible = {sorted(upper_possible[i])}, "
                   f"IMPOSSIBLE = {sorted(missing) if missing else '∅'}")

results.append("")

# Step 3: Zero cell analysis
results.append("### 1d. Zero cell analysis:\n")

# Build actual grid to identify zero cells
grid = np.zeros((6, 5), dtype=int)
for h in hzl:
    for line in h['lines']:
        pos = line['position'] - 1
        elem = ELEM_IDX[line['element']]
        grid[pos, elem] += 1

results.append("Zero cells in the 6×5 grid:")
for pos in range(6):
    for elem in range(5):
        if grid[pos, elem] == 0:
            # Is it structurally impossible?
            if pos < 3:
                possible = lower_possible[pos]
            else:
                possible = upper_possible[pos - 3]
            
            is_hard = ELEMENTS[elem] not in possible
            kind = "HARD (no trigram produces this)" if is_hard else "SOFT (possible but absent)"
            results.append(f"  (L{pos+1}, {ELEMENTS[elem]}): count=0 — {kind}")

results.append("")

# Step 4: Full position×element possibility matrix (structural)
results.append("### 1e. Structural possibility matrix:\n")
results.append("How many of the 8 trigrams produce each (position, element) pair:")
results.append(f"{'':>4s}  " + "  ".join(f"{e:>5s}" for e in ELEMENTS))

# Count how many trigrams produce each (pos, elem) for lower
for pos in range(3):
    counts = [0] * 5
    for branches, elems in lower_trig_map.values():
        counts[ELEM_IDX[elems[pos]]] += 1
    row = "  ".join(f"{c:5d}" for c in counts)
    impossible = "  ←" + ",".join(ELEMENTS[i] for i in range(5) if counts[i] == 0) + " impossible" if any(c == 0 for c in counts) else ""
    results.append(f"L{pos+1}    {row}{impossible}")

for pos in range(3):
    counts = [0] * 5
    for branches, elems in upper_trig_map.values():
        counts[ELEM_IDX[elems[pos]]] += 1
    row = "  ".join(f"{c:5d}" for c in counts)
    impossible = "  ←" + ",".join(ELEMENTS[i] for i in range(5) if counts[i] == 0) + " impossible" if any(c == 0 for c in counts) else ""
    results.append(f"L{pos+4}    {row}{impossible}")

results.append("")


# ══════════════════════════════════════════════════════════════
# PART 2: Rank Structure of All-5-Element Hexagrams
# ══════════════════════════════════════════════════════════════

results.append("## Part 2: Rank Structure and All-5-Element Hexagrams\n")

# Step 1: Which of the 16 all-5-element hexagrams at which ranks?
results.append("### 2a. The 16 all-5-element hexagrams by rank:\n")

all5_hexes = []
for h in hzl:
    elems = set(h['lines'][i]['element'] for i in range(6))
    if len(elems) == 5:
        all5_hexes.append(h)

rank_of_all5 = Counter()
results.append(f"| Hex | Name | Palace | Rank | Rank Name | Element Profile |")
results.append(f"|-----|------|--------|------|-----------|-----------------|")
for h in sorted(all5_hexes, key=lambda x: (x['palace_rank'], x['palace'])):
    rank_of_all5[h['palace_rank']] += 1
    prof = '→'.join(h['lines'][i]['element'][0] for i in range(6))
    results.append(f"| {h['hex_val']:2d} | {h['name']:12s} | {h['palace']:8s} | {h['palace_rank']} | "
                   f"{h['rank_name']} | {prof} |")
results.append("")

results.append("### 2b. All-5-element count by rank:\n")
results.append(f"| Rank | Name | All-5 count | Out of 8 |")
results.append(f"|------|------|-------------|----------|")
for r in range(8):
    results.append(f"| {r} | {RANK_NAMES[r]} | {rank_of_all5.get(r, 0)} | 8 |")
results.append("")

# Step 2: Average distinct elements per rank
results.append("### 2c. Average distinct elements per rank:\n")
results.append(f"| Rank | Name | Avg distinct | Min | Max | All-5 count |")
results.append(f"|------|------|-------------|-----|-----|-------------|")

for r in range(8):
    rank_hexes = [h for h in hzl if h['palace_rank'] == r]
    distinct_counts = [len(set(h['lines'][i]['element'] for i in range(6))) for h in rank_hexes]
    avg = np.mean(distinct_counts)
    results.append(f"| {r} | {RANK_NAMES[r]} | {avg:.3f} | {min(distinct_counts)} | "
                   f"{max(distinct_counts)} | {rank_of_all5.get(r, 0)} |")
results.append("")

# Step 3: Palace × Rank grid of distinct element counts
results.append("### 2d. Distinct elements by palace × rank:\n")

palaces_ordered = sorted(set(h['palace'] for h in hzl))
palace_elems = {}
for h in hzl:
    palace_elems[h['palace']] = h['palace_element']

results.append(f"{'Palace':12s} elem   " + "  ".join(f"R{r}" for r in range(8)) + "  | Avg")
results.append("-" * 75)

for palace in palaces_ordered:
    elem = palace_elems[palace]
    vals = []
    for r in range(8):
        h = [x for x in hzl if x['palace'] == palace and x['palace_rank'] == r][0]
        n_distinct = len(set(h['lines'][i]['element'] for i in range(6)))
        vals.append(n_distinct)
    row = "  ".join(f"{v:2d}" for v in vals)
    avg = np.mean(vals)
    results.append(f"{palace:12s} {elem:5s}  {row}  | {avg:.2f}")

results.append("")

# Step 4: Which specific elements appear at each rank?
results.append("### 2e. Element multiplicity distribution by rank:\n")
results.append("For each rank, how many hexagrams have each element count (0, 1, or 2):\n")

for r in range(8):
    rank_hexes = [h for h in hzl if h['palace_rank'] == r]
    results.append(f"**Rank {r} ({RANK_NAMES[r]}):**")
    for elem in ELEMENTS:
        counts = [sum(1 for line in h['lines'] if line['element'] == elem) for h in rank_hexes]
        dist = Counter(counts)
        results.append(f"  {elem:6s}: " + ", ".join(f"{k}×={dist[k]}" for k in sorted(dist.keys())))
    results.append("")


# ══════════════════════════════════════════════════════════════
# PART 3: Z₅ Sum Distribution
# ══════════════════════════════════════════════════════════════

results.append("## Part 3: Z₅ Sum Distribution\n")

# Compute Z₅ sums
for h in hzl:
    h['_z5_sum'] = sum(ALG_Z5[h['lines'][i]['element']] for i in range(6))
    h['_z5_mod5'] = h['_z5_sum'] % 5
    h['_lower_z5'] = sum(ALG_Z5[h['lines'][i]['element']] for i in range(3))
    h['_upper_z5'] = sum(ALG_Z5[h['lines'][i]['element']] for i in range(3, 6))

# Step 1: Z₅ sum mod 5 × palace element
results.append("### 3a. Z₅ sum mod 5 × palace element:\n")
results.append(f"{'Palace elem':>12s}  " + "  ".join(f"≡{m}" for m in range(5)) + "  | Total")
results.append("-" * 50)

for elem in ELEMENTS:
    row = []
    for m in range(5):
        count = sum(1 for h in hzl if h['palace_element'] == elem and h['_z5_mod5'] == m)
        row.append(count)
    n_palaces = sum(1 for h in hzl if h['palace_element'] == elem) // 8
    results.append(f"{elem:>12s}  " + "  ".join(f"{c:2d}" for c in row) + 
                   f"  | {sum(row)} ({n_palaces} palace{'s' if n_palaces>1 else ''})")

# Totals row
totals = [sum(1 for h in hzl if h['_z5_mod5'] == m) for m in range(5)]
results.append(f"{'Total':>12s}  " + "  ".join(f"{t:2d}" for t in totals) + f"  | {sum(totals)}")
results.append("")

# Step 2: Z₅ sum mod 5 × palace rank
results.append("### 3b. Z₅ sum mod 5 × palace rank:\n")
results.append(f"{'Rank':>12s}  " + "  ".join(f"≡{m}" for m in range(5)) + "  | Total")
results.append("-" * 50)

for r in range(8):
    row = []
    for m in range(5):
        count = sum(1 for h in hzl if h['palace_rank'] == r and h['_z5_mod5'] == m)
        row.append(count)
    results.append(f"{r} {RANK_NAMES[r]:>8s}  " + "  ".join(f"{c:2d}" for c in row) + f"  | {sum(row)}")

results.append("")

# Step 3: (lower_sum, upper_sum) cross-tabulation
results.append("### 3c. (Lower trigram Z₅ sum, Upper trigram Z₅ sum) cross-tab:\n")

lower_upper_pairs = Counter()
for h in hzl:
    lower_upper_pairs[(h['_lower_z5'], h['_upper_z5'])] += 1

lower_vals = sorted(set(p[0] for p in lower_upper_pairs))
upper_vals = sorted(set(p[1] for p in lower_upper_pairs))

results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{u:3d}" for u in upper_vals) + "  | Total")
results.append("-" * 40)
for lv in lower_vals:
    row = [lower_upper_pairs.get((lv, uv), 0) for uv in upper_vals]
    results.append(f"{lv:>12d}  " + "  ".join(f"{c:3d}" for c in row) + f"  | {sum(row)}")

results.append("")
results.append("Total hexagram Z₅ sum = lower + upper:")
for total in sorted(set(h['_z5_sum'] for h in hzl)):
    count = sum(1 for h in hzl if h['_z5_sum'] == total)
    pairs = [(h['_lower_z5'], h['_upper_z5']) for h in hzl if h['_z5_sum'] == total]
    pair_dist = Counter(pairs)
    results.append(f"  sum={total:2d}: {count:2d} hexagrams  compositions: "
                   + ", ".join(f"{l}+{u}(×{c})" for (l, u), c in sorted(pair_dist.items())))
results.append("")

# Step 4: Trigram → Z₅ sum mapping
results.append("### 3d. Per-trigram Z₅ sums:\n")

# Build trigram-level Z₅ sums
# Each trigram is identified by its stem
# Lower trigrams
results.append("**Lower trigrams (stem → trigram → branches → elements → Z₅ sum):**\n")

SURJ_ELEM = {'乾': 'Metal', '坤': 'Earth', '震': 'Wood', '巽': 'Wood',
             '坎': 'Water', '離': 'Fire', '艮': 'Earth', '兌': 'Metal'}

for stem in sorted(lower_trig_map.keys()):
    branches, elems = lower_trig_map[stem]
    trig = TRIG_NAMES.get(stem, '?')
    z5_vals = [ALG_Z5[e] for e in elems]
    z5_sum = sum(z5_vals)
    surj = SURJ_ELEM.get(trig, '?')
    surj_z5 = ALG_Z5.get(surj, '?')
    results.append(f"  {stem} ({trig}): {elems} → Z₅={z5_vals} → sum={z5_sum} "
                   f"(surjection elem={surj}, Z₅={surj_z5})")

results.append("")
results.append("**Upper trigrams (stem → trigram → branches → elements → Z₅ sum):**\n")

for stem in sorted(upper_trig_map.keys()):
    branches, elems = upper_trig_map[stem]
    trig = TRIG_NAMES.get(stem, '?')
    z5_vals = [ALG_Z5[e] for e in elems]
    z5_sum = sum(z5_vals)
    surj = SURJ_ELEM.get(trig, '?')
    surj_z5 = ALG_Z5.get(surj, '?')
    results.append(f"  {stem} ({trig}): {elems} → Z₅={z5_vals} → sum={z5_sum} "
                   f"(surjection elem={surj}, Z₅={surj_z5})")

results.append("")

# Summary: trigram sum vs surjection element
results.append("**Trigram Z₅ sum vs surjection element:**\n")
results.append(f"| Trigram | Surj elem | Z₅(surj) | Lower sum | Upper sum |")
results.append(f"|---------|-----------|----------|-----------|-----------|")

# Merge lower and upper info
trig_info = {}
for stem, (branches, elems) in lower_trig_map.items():
    trig = TRIG_NAMES.get(stem, '?')
    z5_sum = sum(ALG_Z5[e] for e in elems)
    if trig not in trig_info:
        trig_info[trig] = {}
    trig_info[trig]['lower_sum'] = z5_sum

for stem, (branches, elems) in upper_trig_map.items():
    trig = TRIG_NAMES.get(stem, '?')
    z5_sum = sum(ALG_Z5[e] for e in elems)
    if trig not in trig_info:
        trig_info[trig] = {}
    trig_info[trig]['upper_sum'] = z5_sum

for trig in ['乾', '坤', '震', '巽', '坎', '離', '艮', '兌']:
    surj = SURJ_ELEM[trig]
    surj_z5 = ALG_Z5[surj]
    info = trig_info.get(trig, {})
    lower = info.get('lower_sum', '-')
    upper = info.get('upper_sum', '-')
    results.append(f"| {trig} | {surj:5s} | {surj_z5} | {lower} | {upper} |")

results.append("")

# Step 5: Verify hexagram sum is determined by trigram pair
results.append("### 3e. Verification: hexagram Z₅ sum determined by trigram pair\n")

# Each hexagram's lower stem determines lower Z₅ sum, upper stem determines upper Z₅ sum
# Build stem → Z₅ sum maps
lower_stem_to_z5 = {}
for stem, (branches, elems) in lower_trig_map.items():
    lower_stem_to_z5[stem] = sum(ALG_Z5[e] for e in elems)

upper_stem_to_z5 = {}
for stem, (branches, elems) in upper_trig_map.items():
    upper_stem_to_z5[stem] = sum(ALG_Z5[e] for e in elems)

mismatches = 0
for h in hzl:
    lower_stem = h['lines'][0]['stem']
    upper_stem = h['lines'][3]['stem']
    predicted = lower_stem_to_z5[lower_stem] + upper_stem_to_z5[upper_stem]
    actual = h['_z5_sum']
    if predicted != actual:
        mismatches += 1

results.append(f"Mismatches between predicted (from stems) and actual Z₅ sum: {mismatches}/64")
results.append("")

# Step 6: Explain the mod-5 distribution from trigram-level sums
results.append("### 3f. Explaining the mod-5 distribution:\n")

# Lower trigram sums
lower_sum_dist = Counter()
for stem, z5 in lower_stem_to_z5.items():
    # How many hexagrams use this stem for lower?
    count = sum(1 for h in hzl if h['lines'][0]['stem'] == stem)
    lower_sum_dist[z5] += count

results.append(f"Lower trigram Z₅ sum distribution (across 64 hexagrams):")
for s in sorted(lower_sum_dist.keys()):
    results.append(f"  sum={s}: {lower_sum_dist[s]} hexagrams")

upper_sum_dist = Counter()
for stem, z5 in upper_stem_to_z5.items():
    count = sum(1 for h in hzl if h['lines'][3]['stem'] == stem)
    upper_sum_dist[z5] += count

results.append(f"\nUpper trigram Z₅ sum distribution (across 64 hexagrams):")
for s in sorted(upper_sum_dist.keys()):
    results.append(f"  sum={s}: {upper_sum_dist[s]} hexagrams")

results.append("")

# How many trigrams have each sum?
lower_trig_sums = Counter(lower_stem_to_z5.values())
upper_trig_sums = Counter(upper_stem_to_z5.values())

results.append(f"Lower: {dict(sorted(lower_trig_sums.items()))} trigrams per sum value")
results.append(f"Upper: {dict(sorted(upper_trig_sums.items()))} trigrams per sum value")
results.append("")

# Predicted distribution: each lower trigram pairs with each of 8 upper trigrams
# So hexagram sum distribution = convolution of trigram sum distributions
results.append("**Predicted hex sum distribution from trigram-level convolution:**")
results.append("(Each of 8 lower trigrams × each of 8 upper trigrams = 64 pairs)")
results.append("")

predicted = Counter()
for ls, lc in lower_trig_sums.items():
    for us, uc in upper_trig_sums.items():
        predicted[ls + us] += lc * uc

for s in sorted(predicted.keys()):
    actual = sum(1 for h in hzl if h['_z5_sum'] == s)
    results.append(f"  sum={s:2d}: predicted={predicted[s]:2d}, actual={actual:2d} "
                   f"{'✓' if predicted[s] == actual else '✗ MISMATCH'}")

results.append("")

# Predicted mod-5 distribution
results.append("**Predicted mod-5 distribution:**")
pred_mod5 = Counter()
for s, c in predicted.items():
    pred_mod5[s % 5] += c

for m in range(5):
    actual = sum(1 for h in hzl if h['_z5_mod5'] == m)
    results.append(f"  ≡{m} mod 5: predicted={pred_mod5.get(m, 0):2d}, actual={actual:2d}")

results.append("")

# Root cause: which trigrams have which Z₅ sums?
results.append("### 3g. Root cause of non-uniform mod-5 distribution:\n")

# Lower trigram sum mod 5
results.append("Trigram Z₅ sums (lower position):")
for stem in sorted(lower_stem_to_z5.keys()):
    trig = TRIG_NAMES.get(stem, '?')
    s = lower_stem_to_z5[stem]
    results.append(f"  {stem} ({trig}): sum={s}, mod 5 = {s % 5}")

results.append("")
results.append("Trigram Z₅ sums (upper position):")
for stem in sorted(upper_stem_to_z5.keys()):
    trig = TRIG_NAMES.get(stem, '?')
    s = upper_stem_to_z5[stem]
    results.append(f"  {stem} ({trig}): sum={s}, mod 5 = {s % 5}")

results.append("")

# Lower mod-5 distribution
lower_mod5 = Counter(s % 5 for s in lower_stem_to_z5.values())
upper_mod5 = Counter(s % 5 for s in upper_stem_to_z5.values())
results.append(f"Lower trigram sum mod 5 distribution (across 8 trigrams): {dict(sorted(lower_mod5.items()))}")
results.append(f"Upper trigram sum mod 5 distribution (across 8 trigrams): {dict(sorted(upper_mod5.items()))}")
results.append("")

# The hex mod-5 = (lower mod 5 + upper mod 5) mod 5
# = convolution of the two mod-5 distributions
results.append("Hex sum mod 5 = convolution of trigram mod-5 distributions:")
conv = Counter()
for lm, lc in lower_mod5.items():
    for um, uc in upper_mod5.items():
        conv[(lm + um) % 5] += lc * uc

for m in range(5):
    results.append(f"  ≡{m} mod 5: {conv.get(m, 0)} (from 64 = 8×8 pairs)")
results.append("")


# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

output = '\n'.join(results)
print(output)

with open('memories/iching/magic/probe_2b.md', 'w') as f:
    f.write(output)

print("\n\nSaved to memories/iching/magic/probe_2b.md")
