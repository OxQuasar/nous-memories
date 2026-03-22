#!/usr/bin/env python3
"""
Probe 1a: Slice sums of the 2×3×5 cube.

Cube axes:
  Axis 0 — Polarity (size 2): 0=positive (lower binary), 1=complement
  Axis 1 — Fano line (size 3): H={001,110}, P={011,100}, Q={010,101}
  Axis 2 — Element (size 5): Wood=0, Fire=1, Earth=2, Metal=3, Water=4 (algebraic Z₅)

The surjection marks 6 cells — one per (polarity, line):
  (0,H) → 震(001) → Wood(0)
  (1,H) → 巽(110) → Wood(0)
  (0,Q) → 坎(010) → Water(4)
  (1,Q) → 離(101) → Fire(1)
  (0,P) → 兌(011) → Metal(3)
  (1,P) → 艮(100) → Earth(2)

Frame pair: {坤(000)→Earth(2), 乾(111)→Metal(3)} — outside the cube.
"""

import numpy as np
from itertools import permutations
import random

# ── Constants ──
N_POL, N_LINE, N_ELEM = 2, 3, 5
TOTAL_CELLS = N_POL * N_LINE * N_ELEM  # 30

# Fano line labels
H, P, Q = 0, 1, 2
LINE_NAMES = {H: 'H', P: 'P', Q: 'Q'}

# Element labels (algebraic Z₅)
WOOD, FIRE, EARTH, METAL, WATER = 0, 1, 2, 3, 4
ELEM_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}

# ── The surjection marking: 6 marked cells ──
# (polarity, line, element)
MARKED = [
    (0, H, WOOD),   # 震 → Wood
    (1, H, WOOD),   # 巽 → Wood
    (0, Q, WATER),  # 坎 → Water
    (1, Q, FIRE),   # 離 → Fire
    (0, P, METAL),  # 兌 → Metal
    (1, P, EARTH),  # 艮 → Earth
]

# ── Element numbering systems ──
NUMBERINGS = {
    'He Tu mod 5':  {WOOD: 3, FIRE: 2, EARTH: 0, METAL: 4, WATER: 1},
    'Lo Shu (odds)': {WOOD: 3, FIRE: 9, EARTH: 5, METAL: 7, WATER: 1},
    'Algebraic Z₅':  {WOOD: 0, FIRE: 1, EARTH: 2, METAL: 3, WATER: 4},
}


def cell_index(p, l, e):
    """Lexicographic index: polarity major, line mid, element minor."""
    return p * (N_LINE * N_ELEM) + l * N_ELEM + e


def compute_slice_sums(values):
    """
    values: dict (p,l,e) → number, or flat array of 30.
    Returns dict with element_slices, line_slices, polarity_slices.
    """
    if isinstance(values, (list, np.ndarray)):
        v = {}
        for p in range(N_POL):
            for l in range(N_LINE):
                for e in range(N_ELEM):
                    v[(p, l, e)] = values[cell_index(p, l, e)]
        values = v

    elem_slices = {}
    for e in range(N_ELEM):
        elem_slices[e] = sum(values[(p, l, e)] for p in range(N_POL) for l in range(N_LINE))

    line_slices = {}
    for l in range(N_LINE):
        line_slices[l] = sum(values[(p, l, e)] for p in range(N_POL) for e in range(N_ELEM))

    pol_slices = {}
    for p in range(N_POL):
        pol_slices[p] = sum(values[(p, l, e)] for l in range(N_LINE) for e in range(N_ELEM))

    return {
        'element': elem_slices,
        'line': line_slices,
        'polarity': pol_slices,
    }


def slice_variance(sums_dict):
    """Variance of a dict of sums."""
    vals = list(sums_dict.values())
    return np.var(vals)


def is_constant(sums_dict):
    vals = list(sums_dict.values())
    return all(v == vals[0] for v in vals)


def format_slices(slices, names=None):
    lines = []
    for family_name, sums in slices.items():
        vals = []
        for k in sorted(sums.keys()):
            label = k
            if family_name == 'element':
                label = ELEM_NAMES[k]
            elif family_name == 'line':
                label = LINE_NAMES[k]
            elif family_name == 'polarity':
                label = ['pos', 'neg'][k]
            vals.append(f"{label}={sums[k]}")
        constant = " ✓ CONSTANT" if is_constant(sums) else ""
        lines.append(f"  {family_name}: {', '.join(vals)}{constant}")
    return '\n'.join(lines)


# ══════════════════════════════════════════════
# SECTION 1: Slice sums under various numberings
# ══════════════════════════════════════════════

results = []
results.append("# Probe 1a: Slice Sums of the 2×3×5 Cube\n")
results.append("## 1. Slice Sums Under Natural Numberings\n")

# ── 1a: Pure lexicographic index (0–29) ──
results.append("### 1a. Lexicographic index (0–29)\n")
values_lex = {}
for p in range(N_POL):
    for l in range(N_LINE):
        for e in range(N_ELEM):
            values_lex[(p, l, e)] = cell_index(p, l, e)

slices_lex = compute_slice_sums(values_lex)
results.append(format_slices(slices_lex))
results.append(f"\nTotal: {sum(values_lex.values())}")
results.append("")

# ── 1b: Three traditional element numberings ──
results.append("### 1b. Element-axis numberings (value = element number)\n")
results.append("Each cell's value equals the element number under the given system.\n")

for name, num in NUMBERINGS.items():
    results.append(f"**{name}:** {', '.join(f'{ELEM_NAMES[e]}={num[e]}' for e in range(5))}")
    values = {}
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                values[(p, l, e)] = num[e]
    slices = compute_slice_sums(values)
    results.append(format_slices(slices))
    results.append("")

# ── 1c: Product and bijection numberings ──
results.append("### 1c. Product / bijection numberings\n")

# Bijection 1–30: value = p*15 + l*5 + e + 1
results.append("**Bijection (1–30):** value = p×15 + l×5 + e + 1")
values_bij = {}
for p in range(N_POL):
    for l in range(N_LINE):
        for e in range(N_ELEM):
            values_bij[(p, l, e)] = p * 15 + l * 5 + e + 1
slices_bij = compute_slice_sums(values_bij)
results.append(format_slices(slices_bij))
results.append(f"Total: {sum(values_bij.values())}")
results.append("")

# Multiplicative: value = (2p+1) * (l+1) * alg[e]
results.append("**Multiplicative:** value = (2p+1) × (l+1) × algebraic[e]")
alg = NUMBERINGS['Algebraic Z₅']
values_mult = {}
for p in range(N_POL):
    for l in range(N_LINE):
        for e in range(N_ELEM):
            values_mult[(p, l, e)] = (2*p + 1) * (l + 1) * alg[e]
slices_mult = compute_slice_sums(values_mult)
results.append(format_slices(slices_mult))
results.append(f"Total: {sum(values_mult.values())}")
results.append("")

# Multiplicative shifted: value = (2p+1) * (l+1) * (alg[e]+1)
results.append("**Multiplicative shifted:** value = (2p+1) × (l+1) × (algebraic[e]+1)")
values_mult2 = {}
for p in range(N_POL):
    for l in range(N_LINE):
        for e in range(N_ELEM):
            values_mult2[(p, l, e)] = (2*p + 1) * (l + 1) * (alg[e] + 1)
slices_mult2 = compute_slice_sums(values_mult2)
results.append(format_slices(slices_mult2))
results.append(f"Total: {sum(values_mult2.values())}")
results.append("")


# ══════════════════════════════════════════════
# SECTION 2: Search for magic numberings
# ══════════════════════════════════════════════

results.append("## 2. Magic Numbering Search\n")

# Theoretical constants
total_1_30 = 30 * 31 // 2  # = 465
elem_target = total_1_30 / N_ELEM   # 93
line_target = total_1_30 / N_LINE   # 155
pol_target = total_1_30 / N_POL     # 232.5

results.append(f"Sum 1–30 = {total_1_30}")
results.append(f"Element-constant target: {total_1_30}/{N_ELEM} = {elem_target}")
results.append(f"Line-constant target: {total_1_30}/{N_LINE} = {line_target}")
results.append(f"Polarity-constant target: {total_1_30}/{N_POL} = {pol_target} — NOT INTEGER, impossible")
results.append("")

# ── Null distribution via sampling ──
N_SAMPLES = 200_000
random.seed(42)
np.random.seed(42)

elem_vars = []
line_vars = []
elem_maxdevs = []
line_maxdevs = []

base_perm = list(range(1, 31))
for _ in range(N_SAMPLES):
    perm = base_perm.copy()
    random.shuffle(perm)
    
    # Compute element slice sums
    e_sums = [0] * N_ELEM
    l_sums = [0] * N_LINE
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                v = perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    
    e_var = np.var(e_sums)
    l_var = np.var(l_sums)
    elem_vars.append(e_var)
    line_vars.append(l_var)
    elem_maxdevs.append(max(abs(s - elem_target) for s in e_sums))
    line_maxdevs.append(max(abs(s - line_target) for s in l_sums))

elem_vars = np.array(elem_vars)
line_vars = np.array(line_vars)
elem_maxdevs = np.array(elem_maxdevs)
line_maxdevs = np.array(line_maxdevs)

results.append("### Null distribution (200K random permutations of 1–30)")
results.append(f"Element variance: mean={elem_vars.mean():.1f}, median={np.median(elem_vars):.1f}, "
               f"min={elem_vars.min():.1f}, P(var=0)={np.mean(elem_vars==0)*100:.4f}%")
results.append(f"Line variance: mean={line_vars.mean():.1f}, median={np.median(line_vars):.1f}, "
               f"min={line_vars.min():.1f}, P(var=0)={np.mean(line_vars==0)*100:.4f}%")
results.append(f"Element max-dev: mean={elem_maxdevs.mean():.1f}, median={np.median(elem_maxdevs):.1f}, "
               f"min={elem_maxdevs.min():.1f}")
results.append(f"Line max-dev: mean={line_maxdevs.mean():.1f}, median={np.median(line_maxdevs):.1f}, "
               f"min={line_maxdevs.min():.1f}")
results.append("")

# ── Evaluate traditional numberings against null ──
results.append("### Traditional numberings vs null distribution\n")
results.append("For each element numbering, broadcast to all 30 cells, compute slice variances,")
results.append("and compare against random permutation null.\n")

for name, num in NUMBERINGS.items():
    values = {}
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                values[(p, l, e)] = num[e]
    slices = compute_slice_sums(values)
    
    e_var = slice_variance(slices['element'])
    l_var = slice_variance(slices['line'])
    
    # Note: these are degenerate (same value for all cells with same element)
    # so element slices will have non-trivial variance, but line/pol will be constant
    # since each line has all 5 elements
    results.append(f"**{name}:**")
    results.append(f"  Element slices: {dict(slices['element'])} — var={e_var:.2f}")
    results.append(f"  Line slices: {dict(slices['line'])} — var={l_var:.2f}" + 
                   (" ✓ CONSTANT" if l_var == 0 else ""))
    results.append(f"  Polarity slices: {dict(slices['polarity'])} — var={slice_variance(slices['polarity']):.2f}" +
                   (" ✓ CONSTANT" if slice_variance(slices['polarity']) == 0 else ""))
    results.append("")

# ── Also evaluate the bijection numbering against null ──
results.append("### Bijection (1–30) against null\n")
slices = compute_slice_sums(values_bij)
e_var_bij = slice_variance(slices['element'])
l_var_bij = slice_variance(slices['line'])
p_var_bij = slice_variance(slices['polarity'])
e_pct = np.mean(elem_vars <= e_var_bij) * 100
l_pct = np.mean(line_vars <= l_var_bij) * 100
results.append(f"Element var={e_var_bij:.1f}, percentile={e_pct:.2f}%")
results.append(f"Line var={l_var_bij:.1f}, percentile={l_pct:.2f}%")
results.append(f"Polarity var={p_var_bij:.1f}")
results.append("")


# ══════════════════════════════════════════════
# SECTION 2b: Targeted search for magic numberings
# ══════════════════════════════════════════════

results.append("### Targeted search: element-magic numberings (sum=93 per element slice)\n")

# Greedy/hill-climbing search for element-magic
best_elem_var = float('inf')
best_elem_perm = None
best_line_var = float('inf')
best_line_perm = None

N_HILL = 500_000
perm = list(range(1, 31))
random.shuffle(perm)

# Element-magic search
for trial in range(N_HILL):
    if trial % 50_000 == 0:
        perm = list(range(1, 31))
        random.shuffle(perm)
    
    # Random swap
    i, j = random.sample(range(30), 2)
    perm[i], perm[j] = perm[j], perm[i]
    
    e_sums = [0] * N_ELEM
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                e_sums[e] += perm[cell_index(p, l, e)]
    
    e_var = sum((s - 93)**2 for s in e_sums)
    
    if e_var < best_elem_var:
        best_elem_var = e_var
        best_elem_perm = perm.copy()
        if e_var == 0:
            break
    else:
        # Reject swap
        perm[i], perm[j] = perm[j], perm[i]

if best_elem_var == 0:
    results.append(f"FOUND element-magic numbering!")
    slices = compute_slice_sums(best_elem_perm)
    results.append(format_slices(slices))
else:
    results.append(f"Best element variance after {N_HILL} hill-climbing steps: {best_elem_var}")
    e_sums = [0] * N_ELEM
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                e_sums[e] += best_elem_perm[cell_index(p, l, e)]
    results.append(f"  Element sums: {e_sums}")
results.append("")

# Line-magic search
results.append("### Targeted search: line-magic numberings (sum=155 per line slice)\n")
perm = list(range(1, 31))
random.shuffle(perm)
best_line_var = float('inf')

for trial in range(N_HILL):
    if trial % 50_000 == 0:
        perm = list(range(1, 31))
        random.shuffle(perm)
    
    i, j = random.sample(range(30), 2)
    perm[i], perm[j] = perm[j], perm[i]
    
    l_sums = [0] * N_LINE
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                l_sums[l] += perm[cell_index(p, l, e)]
    
    l_var = sum((s - 155)**2 for s in l_sums)
    
    if l_var < best_line_var:
        best_line_var = l_var
        best_line_perm = perm.copy()
        if l_var == 0:
            break
    else:
        perm[i], perm[j] = perm[j], perm[i]

if best_line_var == 0:
    results.append(f"FOUND line-magic numbering!")
    slices = compute_slice_sums(best_line_perm)
    results.append(format_slices(slices))
else:
    results.append(f"Best line variance after {N_HILL} hill-climbing steps: {best_line_var}")
    l_sums = [0] * N_LINE
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                l_sums[l] += best_line_perm[cell_index(p, l, e)]
    results.append(f"  Line sums: {l_sums}")
results.append("")

# ── Search for BOTH element and line magic simultaneously ──
results.append("### Targeted search: doubly-magic (element=93 AND line=155)\n")
perm = list(range(1, 31))
random.shuffle(perm)
best_both_var = float('inf')
best_both_perm = None

for trial in range(N_HILL):
    if trial % 50_000 == 0:
        perm = list(range(1, 31))
        random.shuffle(perm)
    
    i, j = random.sample(range(30), 2)
    perm[i], perm[j] = perm[j], perm[i]
    
    e_sums = [0] * N_ELEM
    l_sums = [0] * N_LINE
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                v = perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    
    total_var = sum((s - 93)**2 for s in e_sums) + sum((s - 155)**2 for s in l_sums)
    
    if total_var < best_both_var:
        best_both_var = total_var
        best_both_perm = perm.copy()
        if total_var == 0:
            break
    else:
        perm[i], perm[j] = perm[j], perm[i]

if best_both_var == 0:
    results.append(f"FOUND doubly-magic numbering!")
    slices = compute_slice_sums(best_both_perm)
    results.append(format_slices(slices))
else:
    results.append(f"Best combined variance after {N_HILL} steps: {best_both_var}")
    e_sums = [0] * N_ELEM
    l_sums = [0] * N_LINE
    for p in range(N_POL):
        for l in range(N_LINE):
            for e in range(N_ELEM):
                v = best_both_perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    results.append(f"  Element sums: {e_sums}")
    results.append(f"  Line sums: {l_sums}")
results.append("")


# ══════════════════════════════════════════════
# SECTION 3: Marked-cell analysis
# ══════════════════════════════════════════════

results.append("## 3. Marked-Cell Numbering\n")
results.append("The 6 marked cells and their positions:\n")
results.append("| Polarity | Line | Element | Trigram |")
results.append("|----------|------|---------|---------|")
for p, l, e in MARKED:
    names = {(0,H):'震', (1,H):'巽', (0,Q):'坎', (1,Q):'離', (0,P):'兌', (1,P):'艮'}
    results.append(f"| {'pos' if p==0 else 'neg'} | {LINE_NAMES[l]} | {ELEM_NAMES[e]} | {names[(p,l)]} |")
results.append("")

results.append("### Sum of marked-cell values under each element numbering\n")

for name, num in NUMBERINGS.items():
    marked_vals = [num[e] for _, _, e in MARKED]
    results.append(f"**{name}:** values = {marked_vals}, sum = {sum(marked_vals)}")
results.append("")

# Also: lexicographic index of marked cells
results.append("### Lexicographic indices of marked cells\n")
marked_indices = [cell_index(p, l, e) for p, l, e in MARKED]
results.append(f"Indices: {marked_indices}")
results.append(f"Sum of indices: {sum(marked_indices)}")
results.append(f"Sum + 6 (if 1-based): {sum(marked_indices) + 6}")
results.append("")

# Bijection values at marked cells
results.append("### Bijection (1–30) values at marked cells\n")
bij_vals = [p * 15 + l * 5 + e + 1 for p, l, e in MARKED]
results.append(f"Values: {bij_vals}")
results.append(f"Sum: {sum(bij_vals)}")
results.append("")

# ── Marked cell distribution analysis ──
results.append("### Distribution of marked cells across axes\n")

# By element
elem_counts = [0]*N_ELEM
for _, _, e in MARKED:
    elem_counts[e] += 1
results.append(f"By element: {', '.join(f'{ELEM_NAMES[e]}={elem_counts[e]}' for e in range(5))}")

# By line
line_counts = [0]*N_LINE
for _, l, _ in MARKED:
    line_counts[l] += 1
results.append(f"By line: {', '.join(f'{LINE_NAMES[l]}={line_counts[l]}' for l in range(3))}")

# By polarity
pol_counts = [0]*N_POL
for p, _, _ in MARKED:
    pol_counts[p] += 1
results.append(f"By polarity: pos={pol_counts[0]}, neg={pol_counts[1]}")
results.append("")

# ── Surjection pattern analysis ──
results.append("### Surjection pattern on the element axis\n")
results.append("Marked elements: Wood(×2), Fire(×1), Earth(×1), Metal(×1), Water(×1)")
results.append("This is a surjection 6→5 with exactly one double-hit at Wood.")
results.append("")

# Complement structure within marked cells
results.append("### Complement structure of marked elements\n")
results.append("Complement pairs on Fano lines (polarity 0 vs 1):")
for l in range(N_LINE):
    e0 = [e for p, ll, e in MARKED if ll == l and p == 0][0]
    e1 = [e for p, ll, e in MARKED if ll == l and p == 1][0]
    results.append(f"  {LINE_NAMES[l]}: {ELEM_NAMES[e0]}({e0}) ↔ {ELEM_NAMES[e1]}({e1}), "
                   f"sum mod 5 = {(e0+e1)%5}, diff mod 5 = {(e0-e1)%5}")
results.append("")

# Z₅ negation check
results.append("### Z₅ negation on complement pairs\n")
results.append("If complement → Z₅ negation, then f(comp) = -f(orig) mod 5:")
for l in range(N_LINE):
    e0 = [e for p, ll, e in MARKED if ll == l and p == 0][0]
    e1 = [e for p, ll, e in MARKED if ll == l and p == 1][0]
    neg_e0 = (-e0) % 5
    results.append(f"  {LINE_NAMES[l]}: f(pos)={e0}, -f(pos) mod 5 = {neg_e0}, f(neg)={e1} → "
                   f"{'MATCH' if neg_e0 == e1 else 'NO MATCH'}")
results.append("")

# ── Frame pair context ──
results.append("### Frame pair context\n")
results.append("Frame: 坤(000)→Earth(2), 乾(111)→Metal(3)")
results.append(f"Sum: 2+3 = 5 ≡ 0 mod 5")
results.append(f"Under He Tu: Earth=0, Metal=4 → sum = 4")
results.append(f"Under Lo Shu: Earth=5, Metal=7 → sum = 12")
results.append("")

# ── Known constant checks ──
results.append("### Comparison to known constants\n")
for name, num in NUMBERINGS.items():
    marked_sum = sum(num[e] for _, _, e in MARKED)
    frame_sum = num[EARTH] + num[METAL]
    total = marked_sum + frame_sum
    results.append(f"**{name}:** marked sum={marked_sum}, frame sum={frame_sum}, total={total}")

results.append("")
results.append("Reference constants: 15 (magic constant of Lo Shu 3×3), 30 (2×15), 65 (sum 1–10 He Tu)")


# ══════════════════════════════════════════════
# SECTION 4: Additional structural observations
# ══════════════════════════════════════════════

results.append("\n## 4. Structural Observations\n")

# The marked cells form a specific pattern in the cube
results.append("### Marked cell positions in cube\n")
results.append("```")
results.append("        Wood  Fire  Earth Metal Water")
results.append("pos H:   [X]   .     .     .     .")
results.append("pos P:   .     .     .    [X]    .")
results.append("pos Q:   .     .     .     .    [X]")
results.append("neg H:   [X]   .     .     .     .")
results.append("neg P:   .     .    [X]    .     .")
results.append("neg Q:   .    [X]    .     .     .")
results.append("```")
results.append("")

# Check: is the marking a permutation matrix on (line, element)?
results.append("### Is the marking a permutation matrix on (line, element)?")
results.append("Per polarity slice, 3 cells are marked in 3 lines. For a permutation matrix,")
results.append("we'd need distinct elements in each polarity slice.\n")
pos_elems = sorted([e for p, l, e in MARKED if p == 0])
neg_elems = sorted([e for p, l, e in MARKED if p == 1])
results.append(f"Positive polarity elements: {[ELEM_NAMES[e] for e in pos_elems]} → {'distinct' if len(set(pos_elems))==3 else 'NOT distinct'}")
results.append(f"Negative polarity elements: {[ELEM_NAMES[e] for e in neg_elems]} → {'distinct' if len(set(neg_elems))==3 else 'NOT distinct'}")
results.append("")

# Check diagonal structure
results.append("### Element indices at marked cells (algebraic Z₅)\n")
for p in range(N_POL):
    elems = [(l, e) for pp, l, e in MARKED if pp == p]
    elems.sort()
    results.append(f"Polarity {p}: lines→elements = {[(LINE_NAMES[l], ELEM_NAMES[e], e) for l, e in elems]}")

results.append("")
results.append("### Arithmetic relations among marked element values\n")
# Check all line-pairs for additive structure
for name, num in NUMBERINGS.items():
    results.append(f"**{name}:**")
    for p in range(N_POL):
        vals = [(l, num[e]) for pp, l, e in MARKED if pp == p]
        vals.sort()
        vs = [v for _, v in vals]
        results.append(f"  pol={p}: values={vs}, sum={sum(vs)}, "
                       f"diffs=[{vs[1]-vs[0]}, {vs[2]-vs[1]}], "
                       f"sum mod 5 = {sum(vs)%5}")
    results.append("")


# ══════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════

output = '\n'.join(results)
print(output)

with open('memories/iching/magic/probe_1a.md', 'w') as f:
    f.write(output)

print("\n\nSaved to memories/iching/magic/probe_1a.md")
