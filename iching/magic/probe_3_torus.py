#!/usr/bin/env python3
"""
Probe 3: The 5×5 Element-Pair Torus.
Covers 3a (magic square), 3b (mod-5), 3c (center cell), 3d (Lo Shu pullback).
"""

import json
import numpy as np
from collections import Counter, defaultdict
from itertools import permutations

# ── Load data ──
with open('memories/iching/atlas-hzl/hzl_profiles.json') as f:
    hzl = json.load(f)
with open('memories/iching/atlas/atlas.json') as f:
    atlas = json.load(f)

ELEMENTS = ['Wood', 'Fire', 'Earth', 'Metal', 'Water']
ELEM_IDX = {e: i for i, e in enumerate(ELEMENTS)}
ALG_Z5 = {'Wood': 0, 'Fire': 1, 'Earth': 2, 'Metal': 3, 'Water': 4}

BINARY_TO_TRIG = {
    '000': '坤', '001': '震', '010': '坎', '011': '兌',
    '100': '艮', '101': '離', '110': '巽', '111': '乾'
}
SURJ_ELEM = {
    '乾': 'Metal', '坤': 'Earth', '震': 'Wood', '巽': 'Wood',
    '坎': 'Water', '離': 'Fire', '艮': 'Earth', '兌': 'Metal'
}

# ── Build 5×5 grid ──
# For each hexagram, identify lower/upper trigram surjection elements
hex_grid_pos = {}  # hex_val → (row, col) in 5×5 grid
grid_hexes = defaultdict(list)  # (row, col) → list of hex_vals

for h in hzl:
    binary = h['hex_binary']
    lower_trig = BINARY_TO_TRIG[binary[3:6]]
    upper_trig = BINARY_TO_TRIG[binary[0:3]]
    lower_elem = SURJ_ELEM[lower_trig]
    upper_elem = SURJ_ELEM[upper_trig]
    row = ELEM_IDX[lower_elem]
    col = ELEM_IDX[upper_elem]
    hex_grid_pos[h['hex_val']] = (row, col)
    grid_hexes[(row, col)].append(h)

# Population matrix
pop = np.zeros((5, 5), dtype=int)
for (r, c), hexes in grid_hexes.items():
    pop[r, c] = len(hexes)

results = []
results.append("# Probe 3: The 5×5 Element-Pair Torus\n")

# ══════════════════════════════════════════════
# SETUP: Grid populations
# ══════════════════════════════════════════════

results.append("## Setup: 5×5 Grid Populations\n")
results.append("Rows = lower trigram surjection element, Columns = upper trigram surjection element.\n")

results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS) + "  | Row")
results.append("-" * 50)
for r in range(5):
    row = "  ".join(f"{pop[r, c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}  | {pop[r].sum()}")
results.append("-" * 50)
col_sums = pop.sum(axis=0)
results.append(f"{'Col sum':>12s}  " + "  ".join(f"{col_sums[c]:4d}" for c in range(5)) + f"  | {pop.sum()}")
results.append("")

# Fiber sizes
fiber_sizes = [0] * 5
for trig, elem in SURJ_ELEM.items():
    fiber_sizes[ELEM_IDX[elem]] += 1
results.append(f"Fiber sizes: {dict(zip(ELEMENTS, fiber_sizes))}")
results.append(f"Expected pop(i,j) = fiber(i) × fiber(j):")

expected_pop = np.zeros((5, 5), dtype=int)
for r in range(5):
    for c in range(5):
        expected_pop[r, c] = fiber_sizes[r] * fiber_sizes[c]

results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS) + "  | Row")
for r in range(5):
    row = "  ".join(f"{expected_pop[r, c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}  | {expected_pop[r].sum()}")

match = np.array_equal(pop, expected_pop)
results.append(f"\nActual = Expected: {match}")
results.append("")

# Anti-diagonal structure (relation types)
RELATIONS = {0: '兄弟(同)', 1: '子孫(生)', 2: '妻財(克)', 3: '官鬼(被克)', 4: '父母(被生)'}
results.append("### Anti-diagonal populations (relation types):\n")
results.append("Relation (i+j) mod 5 = distance in 生 cycle.\n")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    total = sum(pop[r, c] for r, c in cells)
    pop_list = [pop[r, c] for r, c in cells]
    results.append(f"  d={d} {RELATIONS[d]:12s}: cells={cells}, pops={pop_list}, total={total}")
results.append("")


# ══════════════════════════════════════════════
# PART 3a: Magic Square Placement
# ══════════════════════════════════════════════

results.append("## Part 3a: Standard 5×5 Magic Square Placement\n")

# Siamese (de la Loubère) 5×5 magic square
MAGIC = np.array([
    [17, 24,  1,  8, 15],
    [23,  5,  7, 14, 16],
    [ 4,  6, 13, 20, 22],
    [10, 12, 19, 21,  3],
    [11, 18, 25,  2,  9]
])

results.append("Standard magic square:")
for r in range(5):
    results.append("  " + "  ".join(f"{MAGIC[r,c]:3d}" for c in range(5)))
results.append(f"Magic constant = {MAGIC[0].sum()}")
results.append("")

# Identity placement
results.append("### Identity placement (algebraic Z₅ order on both axes):\n")
results.append("Magic value at each element-pair cell:")
results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS))
for r in range(5):
    row = "  ".join(f"{MAGIC[r,c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}")
results.append("")

# Weighted sum by relation type
results.append("### Weighted magic sums by relation type (identity placement):\n")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    magic_sum = sum(MAGIC[r, c] for r, c in cells)
    weighted_sum = sum(MAGIC[r, c] * pop[r, c] for r, c in cells)
    results.append(f"  d={d} {RELATIONS[d]:12s}: magic_sum={magic_sum:3d}, "
                   f"pop-weighted={weighted_sum:4d}")
results.append("")

# Correlation with population across all placements
results.append("### Exhaustive search over row/column permutations:\n")

pop_flat = pop.flatten()
best_corr = -2
worst_corr = 2
best_perm = None
worst_perm = None
corrs = []

all_perms = list(permutations(range(5)))
n_total = len(all_perms) ** 2

for rp in all_perms:
    for cp in all_perms:
        # Permuted magic square: row i → rp[i], col j → cp[j]
        permuted = np.array([[MAGIC[rp[r], cp[c]] for c in range(5)] for r in range(5)])
        perm_flat = permuted.flatten()
        
        # Correlation with population
        corr = np.corrcoef(perm_flat, pop_flat)[0, 1]
        corrs.append(corr)
        
        if corr > best_corr:
            best_corr = corr
            best_perm = (rp, cp)
        if corr < worst_corr:
            worst_corr = corr
            worst_perm = (rp, cp)

corrs = np.array(corrs)
results.append(f"Total placements: {n_total}")
results.append(f"Correlation with cell population:")
results.append(f"  Mean: {corrs.mean():.4f}")
results.append(f"  Std: {corrs.std():.4f}")
results.append(f"  Max: {best_corr:.4f} at rows={best_perm[0]}, cols={best_perm[1]}")
results.append(f"  Min: {worst_corr:.4f} at rows={worst_perm[0]}, cols={worst_perm[1]}")
results.append(f"  Identity placement: {np.corrcoef(MAGIC.flatten(), pop_flat)[0,1]:.4f}")
results.append("")

# Show best placement
results.append("### Best-correlated placement:\n")
rp, cp = best_perm
best_magic = np.array([[MAGIC[rp[r], cp[c]] for c in range(5)] for r in range(5)])
results.append(f"Row permutation: {[ELEMENTS[i] for i in rp]}")
results.append(f"Col permutation: {[ELEMENTS[i] for i in cp]}")
results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS))
for r in range(5):
    row = "  ".join(f"{best_magic[r,c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}")
results.append("")

# Pop-weighted magic sums for best placement
results.append("Pop-weighted sums for best placement by relation:")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    weighted_sum = sum(best_magic[r, c] * pop[r, c] for r, c in cells)
    results.append(f"  d={d} {RELATIONS[d]:12s}: weighted={weighted_sum:4d}")
results.append("")

# Show worst placement
results.append("### Worst-correlated placement:\n")
rp, cp = worst_perm
worst_magic = np.array([[MAGIC[rp[r], cp[c]] for c in range(5)] for r in range(5)])
results.append(f"Row permutation: {[ELEMENTS[i] for i in rp]}")
results.append(f"Col permutation: {[ELEMENTS[i] for i in cp]}")
results.append(f"Correlation: {worst_corr:.4f}")
results.append("")

# Check: are relation-type magic sums constant for any placement?
results.append("### Are relation-type magic sums ever constant?\n")
results.append("For each placement, compute the 5 relation-type magic sums.")
results.append("Check if any placement makes them all equal (= 65, since total = 325).\n")

relation_constant_count = 0
for rp in all_perms:
    for cp in all_perms:
        permuted = np.array([[MAGIC[rp[r], cp[c]] for c in range(5)] for r in range(5)])
        diag_sums = []
        for d in range(5):
            s = sum(permuted[r, c] for r in range(5) for c in range(5) if (r + c) % 5 == d)
            diag_sums.append(s)
        if len(set(diag_sums)) == 1:
            relation_constant_count += 1
            if relation_constant_count <= 3:
                results.append(f"  FOUND: rows={rp}, cols={cp}, sums={diag_sums}")

results.append(f"\nTotal placements with constant relation sums: {relation_constant_count}/{n_total}")
results.append("")


# ══════════════════════════════════════════════
# PART 3b: Mod-5 Residue Pattern
# ══════════════════════════════════════════════

results.append("## Part 3b: Mod-5 Residue Pattern\n")

magic_mod5 = MAGIC % 5
results.append("Magic square mod 5:")
for r in range(5):
    results.append("  " + "  ".join(f"{magic_mod5[r,c]:2d}" for c in range(5)))
results.append("")

# Check if Latin square
is_latin = True
for r in range(5):
    if len(set(magic_mod5[r])) != 5:
        is_latin = False
        break
if is_latin:
    for c in range(5):
        if len(set(magic_mod5[:, c])) != 5:
            is_latin = False
            break

results.append(f"Is Latin square: {is_latin}")
results.append("")

# Compare to Z₅ addition table
add_table = np.array([[(i + j) % 5 for j in range(5)] for i in range(5)])
results.append("Z₅ addition table (i+j mod 5):")
for r in range(5):
    results.append("  " + "  ".join(f"{add_table[r,c]:2d}" for c in range(5)))
results.append("")

# Check if magic_mod5 is a permuted version of addition table
# A Latin square based on (i+j) mod 5 has the form (σ(i) + τ(j)) mod 5
# for some permutations σ, τ of Z₅.

results.append("### Is magic mod 5 an affine transform of Z₅ addition?\n")
results.append("Looking for σ, τ, c such that magic_mod5[i,j] = (σ(i) + τ(j) + c) mod 5.\n")

found_affine = False
for c_const in range(5):
    for sigma in permutations(range(5)):
        for tau in permutations(range(5)):
            match = True
            for i in range(5):
                for j in range(5):
                    if (sigma[i] + tau[j] + c_const) % 5 != magic_mod5[i, j]:
                        match = False
                        break
                if not match:
                    break
            if match:
                found_affine = True
                results.append(f"  FOUND: σ={sigma}, τ={tau}, c={c_const}")
                results.append(f"  i.e., magic_mod5[i,j] = (σ(i) + τ(j) + {c_const}) mod 5")
                
                # Check if σ and τ are affine maps on Z₅
                for a in range(1, 5):
                    for b in range(5):
                        if all((a * i + b) % 5 == sigma[i] for i in range(5)):
                            results.append(f"  σ(i) = {a}i + {b} mod 5 (affine)")
                for a in range(1, 5):
                    for b in range(5):
                        if all((a * j + b) % 5 == tau[j] for j in range(5)):
                            results.append(f"  τ(j) = {a}j + {b} mod 5 (affine)")
                break
        if found_affine:
            break
    if found_affine:
        break

if not found_affine:
    results.append("  NOT an affine transform of Z₅ addition.")

results.append("")

# Compare to multiplication table
mult_table = np.array([[(i * j) % 5 for j in range(5)] for i in range(5)])
results.append("Z₅ multiplication table (i×j mod 5):")
for r in range(5):
    results.append("  " + "  ".join(f"{mult_table[r,c]:2d}" for c in range(5)))
results.append("")

# Direct comparison
results.append(f"Magic mod 5 == Addition table: {np.array_equal(magic_mod5, add_table)}")
results.append(f"Magic mod 5 == Multiplication table: {np.array_equal(magic_mod5, mult_table)}")
results.append("")

# What IS the structure of the magic mod 5?
results.append("### Row-by-row analysis of magic mod 5:\n")
for r in range(5):
    row = list(magic_mod5[r])
    diffs = [(row[(i+1) % 5] - row[i]) % 5 for i in range(5)]
    results.append(f"  Row {r}: {row}, successive diffs mod 5: {diffs}")
results.append("")
for c in range(5):
    col = list(magic_mod5[:, c])
    diffs = [(col[(i+1) % 5] - col[i]) % 5 for i in range(5)]
    results.append(f"  Col {c}: {col}, successive diffs mod 5: {diffs}")
results.append("")


# ══════════════════════════════════════════════
# PART 3c: Center Cell (Earth, Earth)
# ══════════════════════════════════════════════

results.append("## Part 3c: Center Cell (Earth, Earth)\n")

earth_earth = grid_hexes[(2, 2)]
results.append(f"Cell (Earth, Earth): {len(earth_earth)} hexagrams\n")

results.append("| Hex | Name | Binary | Palace | Rank | Lower trig | Upper trig |")
results.append("|-----|------|--------|--------|------|------------|------------|")
for h in earth_earth:
    binary = h['hex_binary']
    lower_trig = BINARY_TO_TRIG[binary[3:6]]
    upper_trig = BINARY_TO_TRIG[binary[0:3]]
    results.append(f"| {h['hex_val']:2d} | {h['name']:12s} | {binary} | {h['palace']:8s} | "
                   f"{h['palace_rank']} ({h['rank_name']}) | {lower_trig} | {upper_trig} |")
results.append("")

# Earth-mapping trigrams are 坤 and 艮
results.append("Earth-mapping trigrams: 坤 (000) and 艮 (100)")
results.append("So (Earth,Earth) cell = hexagrams with lower ∈ {坤,艮} AND upper ∈ {坤,艮}")
results.append("Possible combos: 坤坤, 坤艮, 艮坤, 艮艮 = 4 hexagrams")
results.append("")

# Properties of these hexagrams
results.append("### Properties:\n")
for h in earth_earth:
    binary = h['hex_binary']
    lower_trig = BINARY_TO_TRIG[binary[3:6]]
    upper_trig = BINARY_TO_TRIG[binary[0:3]]
    
    # Element profile
    elem_prof = '→'.join(h['lines'][i]['element'][0] for i in range(6))
    lq_prof = '→'.join(h['lines'][i]['liuqin'][:2] for i in range(6))
    
    # Z₅ sum
    z5_sum = sum(ALG_Z5[h['lines'][i]['element']] for i in range(6))
    
    results.append(f"**h{h['hex_val']} ({h['name']}):** {lower_trig}/{upper_trig}")
    results.append(f"  Element profile: {elem_prof}, Z₅ sum={z5_sum}")
    results.append(f"  六親 profile: {lq_prof}")
    results.append(f"  Palace: {h['palace']} (rank {h['palace_rank']})")
    results.append("")

# Magic square value at center
results.append(f"Magic square value at (2,2) = {MAGIC[2,2]}")
results.append(f"This is the center of the 5×5 magic square (value 13 = (25+1)/2).")
results.append("")


# ══════════════════════════════════════════════
# PART 3d: Lo Shu Pullback via Surjection
# ══════════════════════════════════════════════

results.append("## Part 3d: Lo Shu Pullback via Surjection\n")

# Test 1: Fiber-weighted sum verification
results.append("### Test 1: Fiber partition verification\n")
results.append(f"Fiber sizes: Wood={fiber_sizes[0]}, Fire={fiber_sizes[1]}, "
               f"Earth={fiber_sizes[2]}, Metal={fiber_sizes[3]}, Water={fiber_sizes[4]}")
results.append(f"Partition: {sorted(fiber_sizes, reverse=True)} = [2, 2, 2, 1, 1]")
results.append(f"Pop(i,j) = fiber(i) × fiber(j): verified = {match}")
results.append("")

# Population matrix in detail
results.append("Population matrix (actual):")
for r in range(5):
    results.append(f"  {ELEMENTS[r]:>8s}: " + "  ".join(f"{pop[r,c]:2d}" for c in range(5)))
results.append(f"  Unique values: {sorted(set(pop.flatten()))}")
results.append("")

# Test 2: Lo Shu element numbering
results.append("### Test 2: Lo Shu → element-level sums\n")

# Traditional Lo Shu placement on trigrams
LO_SHU_TRIG = {
    '巽': 4, '離': 9, '坤': 2,
    '震': 3,           '兌': 7,
    '艮': 8, '坎': 1, '乾': 6
}
# Center = 5, associated with Earth

results.append("Lo Shu trigram placement:")
results.append("  巽(4) 離(9) 坤(2)")
results.append("  震(3)  [5]  兌(7)")
results.append("  艮(8) 坎(1) 乾(6)")
results.append("")

# Element-level sums
elem_loshu_sums = defaultdict(int)
for trig, val in LO_SHU_TRIG.items():
    elem = SURJ_ELEM[trig]
    elem_loshu_sums[elem] += val

results.append("Element-level Lo Shu sums (sum of fiber trigram values):")
for elem in ELEMENTS:
    idx = ELEM_IDX[elem]
    results.append(f"  {elem}: {elem_loshu_sums[elem]} (fiber size {fiber_sizes[idx]})")
results.append(f"  Total: {sum(elem_loshu_sums.values())} (= 45 - 5 = 40, center excluded)")
results.append("")

# Check relations to known constants
results.append("Relations to known constants:")
elem_sums = [elem_loshu_sums[e] for e in ELEMENTS]
results.append(f"  Element sums: {elem_sums}")
results.append(f"  Sum = {sum(elem_sums)}")
results.append(f"  Pairwise sums (consecutive in Z₅): "
               f"{[elem_sums[i] + elem_sums[(i+1)%5] for i in range(5)]}")
results.append("")

# Lo Shu sums on the 5×5 grid
results.append("### Lo Shu element sums placed on 5×5 grid:\n")
results.append("Each cell (i,j) gets value = elem_loshu_sum(i) + elem_loshu_sum(j):")
loshu_grid = np.zeros((5, 5), dtype=int)
for r in range(5):
    for c in range(5):
        loshu_grid[r, c] = elem_sums[r] + elem_sums[c]

results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS))
for r in range(5):
    row = "  ".join(f"{loshu_grid[r,c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}")
results.append("")

# Row/column sums of this grid
results.append("Row sums: " + str(list(loshu_grid.sum(axis=1))))
results.append("Col sums: " + str(list(loshu_grid.sum(axis=0))))
results.append("")

# Pop-weighted Lo Shu sums
pop_weighted_loshu = (loshu_grid * pop).sum()
results.append(f"Population-weighted total: {pop_weighted_loshu}")
results.append("")

# Test 3: He Tu element numbers
results.append("### Test 3: He Tu element numbers on 5×5 grid\n")

# He Tu pair sums
HE_TU_SUMS = {'Water': 7, 'Fire': 9, 'Wood': 11, 'Metal': 13, 'Earth': 15}
hetu_sums = [HE_TU_SUMS[e] for e in ELEMENTS]
results.append(f"He Tu pair sums: {dict(zip(ELEMENTS, hetu_sums))}")
results.append("")

# Additive grid
hetu_add_grid = np.zeros((5, 5), dtype=int)
for r in range(5):
    for c in range(5):
        hetu_add_grid[r, c] = hetu_sums[r] + hetu_sums[c]

results.append("Additive He Tu grid (row_sum + col_sum):")
results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS))
for r in range(5):
    row = "  ".join(f"{hetu_add_grid[r,c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}")
results.append("")

results.append("Row sums: " + str(list(hetu_add_grid.sum(axis=1))))
results.append("Col sums: " + str(list(hetu_add_grid.sum(axis=0))))
results.append("")

# Anti-diagonal sums for He Tu grid
results.append("He Tu grid anti-diagonal sums (by relation type):")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    s = sum(hetu_add_grid[r, c] for r, c in cells)
    ws = sum(hetu_add_grid[r, c] * pop[r, c] for r, c in cells)
    results.append(f"  d={d} {RELATIONS[d]:12s}: sum={s:3d}, pop-weighted={ws:4d}")
results.append("")

# Multiplicative grid
hetu_mult_grid = np.zeros((5, 5), dtype=int)
for r in range(5):
    for c in range(5):
        hetu_mult_grid[r, c] = hetu_sums[r] * hetu_sums[c]

results.append("Multiplicative He Tu grid (row_sum × col_sum):")
results.append(f"{'Lower\\Upper':>12s}  " + "  ".join(f"{e[:2]:>4s}" for e in ELEMENTS))
for r in range(5):
    row = "  ".join(f"{hetu_mult_grid[r,c]:4d}" for c in range(5))
    results.append(f"{ELEMENTS[r]:>12s}  {row}")
results.append("")

# Check: do He Tu sums on anti-diagonals form a pattern?
results.append("### He Tu pair sums on anti-diagonals:\n")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    vals = [hetu_sums[r] + hetu_sums[c] for r, c in cells]
    results.append(f"  d={d}: values={vals}, sum={sum(vals)}")
results.append("")

# ══════════════════════════════════════════════
# PART 3e: Additional structural observations
# ══════════════════════════════════════════════

results.append("## Additional Observations\n")

# The population matrix has a specific symmetry
results.append("### Population matrix symmetry:\n")
results.append(f"Symmetric (pop = pop^T): {np.array_equal(pop, pop.T)}")
results.append("")

# Population by anti-diagonal
results.append("### Population per anti-diagonal (relation type):\n")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    total = sum(pop[r, c] for r, c in cells)
    pops = [pop[r, c] for r, c in cells]
    results.append(f"  d={d} {RELATIONS[d]:12s}: pops={pops}, total={total}")

# These should be: d=0 (same element) → fiber(i)² summed
# fiber sizes: W=2, F=1, E=2, M=2, Wa=1
# d=0: 2²+1²+2²+2²+1² = 4+1+4+4+1 = 14
# d=1: fiber(0)*fiber(1)+fiber(1)*fiber(2)+... = 2*1+1*2+2*2+2*1+1*2 = 2+2+4+2+2 = 12
# etc.
results.append("")

# Check diagonal sums analytically
results.append("### Analytical population per anti-diagonal:\n")
for d in range(5):
    total = sum(fiber_sizes[r] * fiber_sizes[(d - r) % 5] for r in range(5))
    results.append(f"  d={d}: Σ fiber(r)×fiber((d-r) mod 5) = {total}")
results.append("")

# The magic square's anti-diagonal sums (no permutation)
results.append("### Magic square anti-diagonal sums (identity placement):\n")
for d in range(5):
    cells = [(r, c) for r in range(5) for c in range(5) if (r + c) % 5 == d]
    s = sum(MAGIC[r, c] for r, c in cells)
    results.append(f"  d={d}: sum={s}")

# Are they constant? Sum of all = 325, 5 diagonals → 65 each if constant
results.append(f"  Total: {sum(MAGIC[r,c] for r in range(5) for c in range(5))}")
results.append(f"  Constant at 65? {all(sum(MAGIC[r,c] for r in range(5) for c in range(5) if (r+c)%5==d) == 65 for d in range(5))}")
results.append("")

# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

output = '\n'.join(results)
print(output)

with open('memories/iching/magic/probe_3.md', 'w') as f:
    f.write(output)

print("\n\nSaved to memories/iching/magic/probe_3.md")
