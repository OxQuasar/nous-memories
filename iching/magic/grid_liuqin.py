#!/usr/bin/env python3
"""
Probe 2a: 六親 as 6×5 grid marking.

Each hexagram marks 6 cells in a 6×5 grid (line_position × element).
Analyzes coverage, profiles, 六親 structure, and palace patterns.
"""

import json
import numpy as np
from collections import Counter, defaultdict

# ── Load data ──
with open('memories/iching/atlas-hzl/hzl_profiles.json') as f:
    hzl = json.load(f)

ELEMENTS = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}
LIUQIN = ['兄弟', '子孫', '妻財', '官鬼', '父母']

results = []
results.append("# Probe 2a: 六親 as 6×5 Grid Marking\n")

# ══════════════════════════════════════════════
# (a) Extract and classify the 64 element profiles
# ══════════════════════════════════════════════

results.append("## (a) Element Profile Classification\n")

profiles = []
profile_to_hexes = defaultdict(list)

for h in hzl:
    # Extract 6-line element profile
    profile = tuple(h['lines'][i]['element'] for i in range(6))
    profiles.append(profile)
    profile_to_hexes[profile].append(h['hex_val'])

n_distinct = len(profile_to_hexes)
results.append(f"Total hexagrams: {len(profiles)}")
results.append(f"Distinct element profiles: {n_distinct}")
results.append("")

# Frequency distribution
freq = sorted([(len(hexes), prof, hexes) for prof, hexes in profile_to_hexes.items()],
              reverse=True)

results.append("### Profile frequency distribution:\n")
results.append(f"| Count | Profile (L1→L6) | Hexagram indices |")
results.append(f"|-------|-----------------|------------------|")
for count, prof, hexes in freq:
    prof_str = '→'.join(p[0] for p in prof)  # First letter
    results.append(f"| {count} | {prof_str} | {hexes} |")
results.append("")

# Count distribution summary
count_dist = Counter(len(v) for v in profile_to_hexes.values())
results.append(f"Profile multiplicity distribution:")
for mult, count in sorted(count_dist.items()):
    results.append(f"  {count} profiles appear {mult} time(s)")
results.append("")

# ══════════════════════════════════════════════
# (b) Grid coverage: 6×5 count matrix
# ══════════════════════════════════════════════

results.append("## (b) Grid Coverage (6×5 count matrix)\n")

grid = np.zeros((6, 5), dtype=int)
for h in hzl:
    for line in h['lines']:
        pos = line['position'] - 1  # 0-indexed
        elem = ELEM_IDX[line['element']]
        grid[pos, elem] += 1

results.append("Each cell = how many of 64 hexagrams mark that (line, element) pair.\n")
results.append(f"{'':>4s}  " + "  ".join(f"{e:>5s}" for e in ELEMENTS) + "  | Row sum")
results.append("-" * 55)
for pos in range(6):
    row = "  ".join(f"{grid[pos, e]:5d}" for e in range(5))
    results.append(f"L{pos+1}    {row}  | {grid[pos].sum()}")
results.append("-" * 55)
col_sums = grid.sum(axis=0)
results.append(f"Sum   " + "  ".join(f"{col_sums[e]:5d}" for e in range(5)) + f"  | {grid.sum()}")
results.append("")

# Statistics
total_marks = grid.sum()
expected = total_marks / 30
variance = np.var(grid)
results.append(f"Total marks: {total_marks} (= 64 × 6)")
results.append(f"Expected per cell if uniform: {expected:.2f}")
results.append(f"Actual range: [{grid.min()}, {grid.max()}]")
results.append(f"Variance: {variance:.2f}")
results.append(f"Std dev: {np.sqrt(variance):.2f}")
results.append("")

# Check row uniformity
results.append("### Row sums (by line position):")
for pos in range(6):
    results.append(f"  L{pos+1}: {grid[pos].sum()}")
results.append(f"  All rows sum to {grid[0].sum()} — {'CONSTANT' if len(set(grid.sum(axis=1))) == 1 else 'NOT constant'}")
results.append("")

# Check column uniformity
results.append("### Column sums (by element):")
for e in range(5):
    results.append(f"  {ELEMENTS[e]}: {col_sums[e]}")
col_var = np.var(col_sums)
results.append(f"  Variance: {col_var:.2f}")
results.append("")

# ══════════════════════════════════════════════
# (c) 六親 profile classification
# ══════════════════════════════════════════════

results.append("## (c) 六親 Profile Classification\n")

liuqin_profiles = []
liuqin_profile_to_hexes = defaultdict(list)

for h in hzl:
    lq_profile = tuple(h['lines'][i]['liuqin'] for i in range(6))
    liuqin_profiles.append(lq_profile)
    liuqin_profile_to_hexes[lq_profile].append(h['hex_val'])

n_lq_distinct = len(liuqin_profile_to_hexes)
results.append(f"Distinct 六親 profiles: {n_lq_distinct}")
results.append("")

# Frequency distribution
lq_freq = sorted([(len(hexes), prof, hexes) for prof, hexes in liuqin_profile_to_hexes.items()],
                 reverse=True)

results.append("### 六親 profile frequency (top 15):\n")
results.append(f"| Count | Profile (L1→L6) | Hex indices |")
results.append(f"|-------|-----------------|-------------|")
for count, prof, hexes in lq_freq[:15]:
    prof_str = '→'.join(p[:2] for p in prof)
    results.append(f"| {count} | {prof_str} | {hexes} |")
if len(lq_freq) > 15:
    results.append(f"... and {len(lq_freq) - 15} more profiles")
results.append("")

# Count distribution
lq_count_dist = Counter(len(v) for v in liuqin_profile_to_hexes.values())
results.append(f"六親 profile multiplicity distribution:")
for mult, count in sorted(lq_count_dist.items()):
    results.append(f"  {count} profiles appear {mult} time(s)")
results.append("")

# Hexagrams with all 5 relation types present
results.append("### Hexagrams with all 5 六親 types present:\n")
all_five_count = 0
for h in hzl:
    types_present = set(h['lines'][i]['liuqin'] for i in range(6))
    if len(types_present) == 5:
        all_five_count += 1
        elem_profile = '→'.join(h['lines'][i]['element'][0] for i in range(6))
        results.append(f"  h{h['hex_val']:2d} ({h['name']:12s}) palace={h['palace']:6s} "
                       f"elems={elem_profile}")
results.append(f"\nTotal: {all_five_count}/64")
results.append("")

# Hexagrams with all 5 elements present in 6 lines
results.append("### Hexagrams with all 5 elements in 6 lines:\n")
all_five_elem = 0
for h in hzl:
    elems_present = set(h['lines'][i]['element'] for i in range(6))
    if len(elems_present) == 5:
        all_five_elem += 1
        elem_profile = '→'.join(h['lines'][i]['element'][0] for i in range(6))
        lq_profile = '→'.join(h['lines'][i]['liuqin'][:2] for i in range(6))
        results.append(f"  h{h['hex_val']:2d} ({h['name']:12s}) palace={h['palace']:6s} "
                       f"elems={elem_profile} 六親={lq_profile}")
results.append(f"\nTotal: {all_five_elem}/64")
results.append("")

# Census of 六親 counts across all hexagrams
results.append("### 六親 census across all hexagrams:\n")
lq_census = defaultdict(list)
for h in hzl:
    census = h['liuqin_census']
    for lq in LIUQIN:
        lq_census[lq].append(census.get(lq, 0))

results.append(f"{'六親':8s}  mean   min  max  zeros  distribution")
for lq in LIUQIN:
    vals = lq_census[lq]
    dist = Counter(vals)
    dist_str = " ".join(f"{k}:{v}" for k, v in sorted(dist.items()))
    results.append(f"{lq:8s}  {np.mean(vals):5.2f}  {min(vals):3d}  {max(vals):3d}  "
                   f"{vals.count(0):5d}  {dist_str}")
results.append("")

# Missing 六親
results.append("### Hexagrams with missing 六親:\n")
missing_count = Counter()
for h in hzl:
    for m in h['missing_liuqin']:
        missing_count[m] += 1
        
if missing_count:
    for lq, count in missing_count.most_common():
        results.append(f"  {lq}: missing in {count} hexagrams")
else:
    results.append("  No hexagrams have missing 六親 types (all 5 present in every hexagram)")
results.append("")

# ══════════════════════════════════════════════
# (d) Palace-grouped analysis
# ══════════════════════════════════════════════

results.append("## (d) Palace-Grouped Analysis\n")

# Group by palace
palaces = defaultdict(list)
for h in hzl:
    palaces[h['palace']].append(h)

results.append(f"Number of palaces: {len(palaces)}")
results.append("")

# For each palace, show the 8 hexagrams' grid coverage
results.append("### Per-palace 6×5 coverage grids:\n")
results.append("Each palace has 8 hexagrams × 6 lines = 48 marks across 30 cells.")
results.append("If uniform: 48/30 = 1.6 per cell.\n")

palace_grids = {}
for palace_name in sorted(palaces.keys()):
    hexes = palaces[palace_name]
    palace_elem = hexes[0]['palace_element']
    
    pgrid = np.zeros((6, 5), dtype=int)
    for h in hexes:
        for line in h['lines']:
            pos = line['position'] - 1
            elem = ELEM_IDX[line['element']]
            pgrid[pos, elem] += 1
    
    palace_grids[palace_name] = pgrid
    
    results.append(f"**{palace_name} (element={palace_elem}):**")
    results.append(f"{'':>4s}  " + "  ".join(f"{e[0]:>3s}" for e in ELEMENTS))
    for pos in range(6):
        row = "  ".join(f"{pgrid[pos, e]:3d}" for e in range(5))
        results.append(f"L{pos+1}    {row}")
    
    col_sums_p = pgrid.sum(axis=0)
    results.append(f"Sum   " + "  ".join(f"{col_sums_p[e]:3d}" for e in range(5)))
    results.append(f"  Variance: {np.var(pgrid):.2f}, Range: [{pgrid.min()}, {pgrid.max()}]")
    
    # How many cells are zero?
    zeros = (pgrid == 0).sum()
    results.append(f"  Zero cells: {zeros}/30, Covered: {30 - zeros}/30")
    results.append("")

# Cross-palace comparison
results.append("### Cross-palace column sums (element totals per palace):\n")
results.append(f"{'Palace':12s}  " + "  ".join(f"{e:>5s}" for e in ELEMENTS) + "  | Total")
results.append("-" * 60)
for palace_name in sorted(palaces.keys()):
    pgrid = palace_grids[palace_name]
    col_s = pgrid.sum(axis=0)
    results.append(f"{palace_name:12s}  " + "  ".join(f"{col_s[e]:5d}" for e in range(5))
                   + f"  | {col_s.sum()}")
results.append("")

# 六親 distribution per palace
results.append("### 六親 census per palace:\n")
results.append(f"{'Palace':12s}  {'Element':7s}  " + "  ".join(f"{lq[:2]:>4s}" for lq in LIUQIN))
results.append("-" * 65)
for palace_name in sorted(palaces.keys()):
    hexes = palaces[palace_name]
    palace_elem = hexes[0]['palace_element']
    
    lq_total = defaultdict(int)
    for h in hexes:
        for lq in LIUQIN:
            lq_total[lq] += h['liuqin_census'].get(lq, 0)
    
    results.append(f"{palace_name:12s}  {palace_elem:7s}  " + 
                   "  ".join(f"{lq_total[lq]:4d}" for lq in LIUQIN))
results.append("")

# ══════════════════════════════════════════════
# (e) Element profile patterns — lower/upper trigram structure
# ══════════════════════════════════════════════

results.append("## (e) Structural Patterns\n")

# Since 納甲 assigns elements based on trigrams, the element profile
# is really determined by upper+lower trigram pair.
# L1-L3 = lower trigram, L4-L6 = upper trigram

results.append("### Lower trigram (L1-L3) element patterns:\n")
lower_patterns = defaultdict(list)
for h in hzl:
    lower = tuple(h['lines'][i]['element'] for i in range(3))
    lower_patterns[lower].append(h['hex_val'])

results.append(f"Distinct lower-trigram element patterns: {len(lower_patterns)}")
for pattern, hexes in sorted(lower_patterns.items(), key=lambda x: -len(x[1])):
    results.append(f"  {pattern[0][0]}-{pattern[1][0]}-{pattern[2][0]}: {len(hexes)} hexagrams")
results.append("")

results.append("### Upper trigram (L4-L6) element patterns:\n")
upper_patterns = defaultdict(list)
for h in hzl:
    upper = tuple(h['lines'][i]['element'] for i in range(3, 6))
    upper_patterns[upper].append(h['hex_val'])

results.append(f"Distinct upper-trigram element patterns: {len(upper_patterns)}")
for pattern, hexes in sorted(upper_patterns.items(), key=lambda x: -len(x[1])):
    results.append(f"  {pattern[0][0]}-{pattern[1][0]}-{pattern[2][0]}: {len(hexes)} hexagrams")
results.append("")

# Check: is the element profile uniquely determined by (lower_trigram, upper_trigram)?
results.append("### Is element profile determined by trigram pair?\n")
trigram_to_profile = defaultdict(set)
for h in hzl:
    # We don't have trigram names easily, use lower/upper element patterns as proxy
    lower = tuple(h['lines'][i]['element'] for i in range(3))
    upper = tuple(h['lines'][i]['element'] for i in range(3, 6))
    full = lower + upper
    trigram_to_profile[(lower, upper)].add(full)

all_unique = all(len(v) == 1 for v in trigram_to_profile.values())
results.append(f"Each (lower, upper) element pattern maps to unique full profile: {all_unique}")
results.append(f"Number of distinct (lower, upper) pairs: {len(trigram_to_profile)}")
results.append("")

# ══════════════════════════════════════════════
# (f) Magic-like properties
# ══════════════════════════════════════════════

results.append("## (f) Magic-like Properties\n")

# Convert elements to Z₅ numbers and check for sum properties
ALG_Z5 = {'Wood': 0, 'Fire': 1, 'Earth': 2, 'Metal': 3, 'Water': 4}

results.append("### Sum of line elements (algebraic Z₅) per hexagram:\n")
sums = []
for h in hzl:
    s = sum(ALG_Z5[h['lines'][i]['element']] for i in range(6))
    sums.append(s)

sum_dist = Counter(sums)
results.append(f"Sum distribution:")
for s in sorted(sum_dist.keys()):
    results.append(f"  sum={s:2d}: {sum_dist[s]} hexagrams  (mod 5 = {s % 5})")
results.append("")

# Sum mod 5
mod5_dist = Counter(s % 5 for s in sums)
results.append(f"Sum mod 5 distribution:")
for m in range(5):
    results.append(f"  ≡{m} mod 5: {mod5_dist.get(m, 0)} hexagrams")
results.append("")

# Per-palace sum analysis
results.append("### Per-palace element sum (algebraic Z₅):\n")
for palace_name in sorted(palaces.keys()):
    hexes = palaces[palace_name]
    palace_elem = hexes[0]['palace_element']
    palace_z5 = ALG_Z5[palace_elem]
    hex_sums = []
    for h in hexes:
        s = sum(ALG_Z5[h['lines'][i]['element']] for i in range(6))
        hex_sums.append(s)
    results.append(f"  {palace_name:12s} (Z₅={palace_z5}): sums={hex_sums}, "
                   f"total={sum(hex_sums)}, mod5={[s%5 for s in hex_sums]}")
results.append("")

# ══════════════════════════════════════════════
# (g) 六親 grid: which lines carry which relations
# ══════════════════════════════════════════════

results.append("## (g) 六親 by Line Position\n")

lq_grid = np.zeros((6, 5), dtype=int)  # line × liuqin
LQ_IDX = {lq: i for i, lq in enumerate(LIUQIN)}

for h in hzl:
    for line in h['lines']:
        pos = line['position'] - 1
        lq = LQ_IDX[line['liuqin']]
        lq_grid[pos, lq] += 1

results.append("Count of each 六親 type by line position (across all 64 hexagrams):\n")
results.append(f"{'':>4s}  " + "  ".join(f"{lq[:2]:>4s}" for lq in LIUQIN) + "  | Sum")
results.append("-" * 45)
for pos in range(6):
    row = "  ".join(f"{lq_grid[pos, lq]:4d}" for lq in range(5))
    results.append(f"L{pos+1}    {row}  | {lq_grid[pos].sum()}")
results.append("-" * 45)
lq_col = lq_grid.sum(axis=0)
results.append(f"Sum   " + "  ".join(f"{lq_col[lq]:4d}" for lq in range(5)) + f"  | {lq_grid.sum()}")
results.append("")

results.append(f"六親 column variance: {np.var(lq_col):.2f}")
results.append(f"六親 grid variance: {np.var(lq_grid):.2f}")
results.append("")


# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

output = '\n'.join(results)
print(output)

with open('memories/iching/magic/probe_2a.md', 'w') as f:
    f.write(output)

print("\n\nSaved to memories/iching/magic/probe_2a.md")
