#!/usr/bin/env python3
"""Earth mediation, element-direction constraints, and 木 pivot analysis.

Operates on the 32 combined matches (H2-segregation + directional purity)
found in n2_compass_uniqueness.py.

Task A: Earth mediation — does every non-trivial transition involve 土?
Task B: Element-direction constraint — adjacency & antipodality selection
Task C: 木 pivot — where does 木 sit relative to 克/生 boundary?
"""

from itertools import permutations
from collections import Counter

# === Data Definitions ===

EL = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}

TRIGRAMS = [
    ('坎', '010', 4),  # 0
    ('坤', '000', 2),  # 1
    ('震', '001', 0),  # 2
    ('巽', '110', 0),  # 3
    ('乾', '111', 3),  # 4
    ('兌', '011', 3),  # 5
    ('艮', '100', 2),  # 6
    ('離', '101', 1),  # 7
]

COMPASS = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
Z5_TYPE = {0: '比和', 1: '生↑', 4: '生↓', 2: '克↑', 3: '克↓'}

# Traditional assignment
TRAD_NAMES = ['離', '坤', '兌', '乾', '坎', '艮', '震', '巽']
TRAD_INDICES = tuple(next(i for i, t in enumerate(TRIGRAMS) if t[0] == n) for n in TRAD_NAMES)


# === Helpers ===

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

def cycle_z5_types(perm):
    return [Z5_TYPE[(TRIGRAMS[perm[(i+1)%8]][2] - TRIGRAMS[perm[i]][2]) % 5] for i in range(8)]

def cycle_hamming(perm):
    return [hamming(TRIGRAMS[perm[i]][1], TRIGRAMS[perm[(i+1)%8]][1]) for i in range(8)]

def check_combined(perm):
    """Check H2-segregation + directional purity."""
    z5t = cycle_z5_types(perm)
    hd = cycle_hamming(perm)
    # H2 segregation
    for typ, h in zip(z5t, hd):
        if typ != '比和' and h != 2:
            return False
        if typ == '比和' and h == 2:
            return False
    # Directional purity
    sheng = set(t for t in z5t if '生' in t)
    ke = set(t for t in z5t if '克' in t)
    if len(sheng) > 1 or len(ke) > 1:
        return False
    return True

def perm_elements(perm):
    return [TRIGRAMS[perm[i]][2] for i in range(8)]

def perm_names(perm):
    return [TRIGRAMS[perm[i]][0] for i in range(8)]

def print_separator(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


# === Generate the 32 combined matches ===

combined = []
for perm in permutations(range(8)):
    if check_combined(perm):
        combined.append(perm)

print(f"Generated {len(combined)} combined matches (expected 32)")


# =======================================================================
#  TASK A: Earth Mediation
# =======================================================================

print_separator("TASK A: EARTH MEDIATION")
print("For each non-trivial (生/克) transition, check if at least one")
print("trigram in the pair has element 土 (Z₅=2).\n")

EARTH_Z5 = 2

universal_earth = []
partial_earth = []
no_earth = []

for perm in combined:
    z5t = cycle_z5_types(perm)
    els = perm_elements(perm)
    names = perm_names(perm)

    nontrivial_steps = []
    earth_mediated = 0
    non_earth_mediated = 0

    for i in range(8):
        j = (i + 1) % 8
        if z5t[i] != '比和':
            has_earth = (els[i] == EARTH_Z5 or els[j] == EARTH_Z5)
            nontrivial_steps.append((i, z5t[i], els[i], els[j], has_earth))
            if has_earth:
                earth_mediated += 1
            else:
                non_earth_mediated += 1

    total_nontrivial = earth_mediated + non_earth_mediated
    if non_earth_mediated == 0:
        universal_earth.append(perm)
    elif earth_mediated == 0:
        no_earth.append(perm)
    else:
        partial_earth.append(perm)

print(f"Universal Earth mediation: {len(universal_earth)} / {len(combined)}")
print(f"Partial Earth mediation:   {len(partial_earth)} / {len(combined)}")
print(f"No Earth mediation:        {len(no_earth)} / {len(combined)}")

# Show detail for all 32
print(f"\n--- Detail: Earth mediation per permutation ---")
print(f"{'#':>3}  {'Assignment':>45}  {'Types':>45}  {'Earth':>6}  {'Non-E':>6}  {'Status'}")
print('-' * 130)
for idx, perm in enumerate(combined):
    z5t = cycle_z5_types(perm)
    els = perm_elements(perm)
    names = perm_names(perm)

    earth_count = 0
    nonearth_count = 0
    for i in range(8):
        j = (i + 1) % 8
        if z5t[i] != '比和':
            if els[i] == EARTH_Z5 or els[j] == EARTH_Z5:
                earth_count += 1
            else:
                nonearth_count += 1

    assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
    types_str = ' '.join(z5t)
    is_trad = " ◀TRAD" if perm == TRAD_INDICES else ""
    status = "ALL" if nonearth_count == 0 else f"partial({earth_count}/{earth_count+nonearth_count})"
    print(f"{idx+1:>3}  {assign:>45}  {types_str:>45}  {earth_count:>6}  {nonearth_count:>6}  {status}{is_trad}")

# For non-universal, show which steps lack Earth
if partial_earth or no_earth:
    print(f"\n--- Non-Earth-mediated transitions ---")
    for perm in partial_earth + no_earth:
        z5t = cycle_z5_types(perm)
        els = perm_elements(perm)
        names = perm_names(perm)
        for i in range(8):
            j = (i + 1) % 8
            if z5t[i] != '比和' and els[i] != EARTH_Z5 and els[j] != EARTH_Z5:
                print(f"  {COMPASS[i]}={names[i]}({EL[els[i]]}) → {COMPASS[j]}={names[j]}({EL[els[j]]})  type={z5t[i]}")


# =======================================================================
#  TASK B: Element-Direction Constraints
# =======================================================================

print_separator("TASK B: ELEMENT-DIRECTION CONSTRAINTS")

# Traditional Lo Shu element-direction correspondence:
# Fire=S, Water=N, Wood=E side, Metal=W side, Earth=diagonal(SW+NE)
# More specifically, check three adjacency constraints:
# 1. Two 土 trigrams diametrically opposite (4 positions apart)
# 2. Two 金 trigrams adjacent (1 position apart)
# 3. Two 木 trigrams adjacent (1 position apart)

print("\nConstraint set: paired elements' spatial arrangement")
print("  C1: 土×2 diametrically opposite (separation = 4)")
print("  C2: 金×2 adjacent (separation = 1)")
print("  C3: 木×2 adjacent (separation = 1)\n")

def element_positions(perm, z5_val):
    """Return compass positions (0-7) where element z5_val appears."""
    return [i for i in range(8) if TRIGRAMS[perm[i]][2] == z5_val]

def separation(a, b):
    """Circular separation between two positions (0-7), min of clockwise/counter."""
    d = abs(a - b)
    return min(d, 8 - d)

c1_pass = []  # 土 antipodal
c2_pass = []  # 金 adjacent
c3_pass = []  # 木 adjacent
all_pass = []

for perm in combined:
    earth_pos = element_positions(perm, 2)  # 土
    metal_pos = element_positions(perm, 3)  # 金
    wood_pos = element_positions(perm, 0)   # 木

    c1 = separation(earth_pos[0], earth_pos[1]) == 4
    c2 = separation(metal_pos[0], metal_pos[1]) == 1
    c3 = separation(wood_pos[0], wood_pos[1]) == 1

    if c1: c1_pass.append(perm)
    if c2: c2_pass.append(perm)
    if c3: c3_pass.append(perm)
    if c1 and c2 and c3: all_pass.append(perm)

print(f"C1 (土 antipodal):     {len(c1_pass)} / {len(combined)}")
print(f"C2 (金 adjacent):      {len(c2_pass)} / {len(combined)}")
print(f"C3 (木 adjacent):      {len(c3_pass)} / {len(combined)}")
print(f"All three (C1∧C2∧C3): {len(all_pass)} / {len(combined)}")
print(f"Traditional in all:    {TRAD_INDICES in all_pass}")

if all_pass:
    print(f"\n--- Arrangements satisfying all three constraints ---")
    print(f"{'#':>3}  {'Assignment':>55}  {'Types':>45}  {'P:R':>5}")
    print('-' * 120)
    for idx, perm in enumerate(all_pass):
        z5t = cycle_z5_types(perm)
        names = perm_names(perm)
        pro = sum(1 for t in z5t if t in ('生↑', '克↑'))
        retro = sum(1 for t in z5t if t in ('生↓', '克↓'))
        assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
        is_trad = " ◀TRAD" if perm == TRAD_INDICES else ""
        print(f"{idx+1:>3}  {assign:>55}  {' '.join(z5t):>45}  {pro}:{retro}{is_trad}")

# Now fix rotation: put 火 at position 0 (S)
print(f"\n--- Rotation-fixed: 火 at S (position 0) ---")
fire_at_s = [p for p in combined if TRIGRAMS[p[0]][2] == 1]
print(f"Combined matches with 火 at S: {len(fire_at_s)}")
for idx, perm in enumerate(fire_at_s):
    z5t = cycle_z5_types(perm)
    names = perm_names(perm)
    els = [EL[TRIGRAMS[perm[i]][2]] for i in range(8)]
    pro = sum(1 for t in z5t if t in ('生↑', '克↑'))
    retro = sum(1 for t in z5t if t in ('生↓', '克↓'))
    assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
    is_trad = " ◀TRAD" if perm == TRAD_INDICES else ""
    print(f"  {idx+1}. {assign}")
    print(f"     Elements: {' '.join(els)}")
    print(f"     Types:    {' '.join(z5t)}  P:R={pro}:{retro}{is_trad}")

# Fire at S + all three constraints
fire_s_and_c123 = [p for p in all_pass if TRIGRAMS[p[0]][2] == 1]
print(f"\n火 at S + C1∧C2∧C3: {len(fire_s_and_c123)}")
for perm in fire_s_and_c123:
    names = perm_names(perm)
    z5t = cycle_z5_types(perm)
    assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
    is_trad = " ◀TRAD" if perm == TRAD_INDICES else ""
    print(f"  {assign}  |  {' '.join(z5t)}{is_trad}")

# Fire at S + prograde
fire_s_prograde = [p for p in fire_at_s
                   if sum(1 for t in cycle_z5_types(p) if t in ('生↑','克↑')) >
                      sum(1 for t in cycle_z5_types(p) if t in ('生↓','克↓'))]
print(f"\n火 at S + prograde: {len(fire_s_prograde)}")
for perm in fire_s_prograde:
    names = perm_names(perm)
    z5t = cycle_z5_types(perm)
    assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
    is_trad = " ◀TRAD" if perm == TRAD_INDICES else ""
    print(f"  {assign}  |  {' '.join(z5t)}{is_trad}")

# Fire at S + prograde + C1∧C2∧C3
final = [p for p in fire_s_and_c123
         if sum(1 for t in cycle_z5_types(p) if t in ('生↑','克↑')) >
            sum(1 for t in cycle_z5_types(p) if t in ('生↓','克↓'))]
print(f"\n火 at S + prograde + C1∧C2∧C3: {len(final)}")
for perm in final:
    names = perm_names(perm)
    z5t = cycle_z5_types(perm)
    assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
    is_trad = " ◀TRAD" if perm == TRAD_INDICES else ""
    print(f"  {assign}  |  {' '.join(z5t)}{is_trad}")


# =======================================================================
#  TASK C: 木 Pivot Analysis
# =======================================================================

print_separator("TASK C: 木 PIVOT ANALYSIS")
print("Where does 木 sit relative to the 克/生 boundary in each cycle?\n")

# --- Traditional cycles first ---
print("--- Known cycles ---\n")

# 先天 cycle
FX = {1: ('乾','金',3), 2: ('兌','金',3), 3: ('離','火',1), 4: ('震','木',0),
      5: ('巽','木',0), 6: ('坎','水',4), 7: ('艮','土',2), 8: ('坤','土',2)}
fx_z5 = [FX[n][2] for n in range(1, 9)]
fx_types = [Z5_TYPE[(fx_z5[(i+1)%8] - fx_z5[i]) % 5] for i in range(8)]
print(f"先天 cycle: {' '.join(FX[n][0] for n in range(1,9))}")
print(f"  Elements: {' '.join(EL[FX[n][2]] for n in range(1,9))}")
print(f"  Types:    {' '.join(fx_types)}")
wood_positions_fx = [i for i in range(8) if fx_z5[i] == 0]
print(f"  木 at positions: {wood_positions_fx} (FX#{[i+1 for i in wood_positions_fx]})")
# Find 克/生 boundaries
for i in range(8):
    j = (i + 1) % 8
    t_cur, t_next = fx_types[i], fx_types[j]
    if '克' in t_cur and '生' in t_next:
        print(f"  克→生 boundary: step {i}({fx_types[i]}) → step {j}({fx_types[j]})")
    if '克' in t_cur and '比' in t_next:
        print(f"  克→比和 boundary: step {i}({fx_types[i]}) → step {j}({fx_types[j]})")
    if '比' in t_cur and '生' in t_next:
        print(f"  比和→生 boundary: step {i}({fx_types[i]}) → step {j}({fx_types[j]})")

# 後天 compass cycle
trad_z5 = [TRIGRAMS[TRAD_INDICES[i]][2] for i in range(8)]
trad_types = cycle_z5_types(TRAD_INDICES)
print(f"\n後天 compass: {' '.join(TRAD_NAMES)}")
print(f"  Elements: {' '.join(EL[e] for e in trad_z5)}")
print(f"  Types:    {' '.join(trad_types)}")
wood_positions_ht = [i for i in range(8) if trad_z5[i] == 0]
print(f"  木 at positions: {wood_positions_ht} ({[COMPASS[i] for i in wood_positions_ht]})")
for i in range(8):
    j = (i + 1) % 8
    t_cur, t_next = trad_types[i], trad_types[j]
    if '克' in t_cur and '生' in t_next:
        print(f"  克→生 boundary: step {i}({trad_types[i]}) → step {j}({trad_types[j]}) at {COMPASS[j]}")
    if '克' in t_cur and '比' in t_next:
        print(f"  克→比和 boundary: step {i}({trad_types[i]}) → step {j}({trad_types[j]}) at {COMPASS[j]}")
    if '比' in t_cur and ('生' in t_next or '克' in t_next):
        print(f"  比和→{t_next} boundary: step {i}({trad_types[i]}) → step {j}({trad_types[j]}) at {COMPASS[j]}")

# --- Now analyze all 32 combined matches ---
print(f"\n--- 木 position relative to 克/生 boundary across all 32 ---")
print("For directionally pure arrangements, the cycle has blocks of")
print("生, 克, and 比和. 木 can be: at the boundary, inside a block, etc.\n")

# For prograde (生↑+克↓) arrangements: 
# The type sequence has 生↑ blocks and 克↓ blocks separated by 比和.
# Where are the 木 elements?

print(f"{'#':>3}  {'P:R':>3}  {'Elements':>20}  {'Types':>40}  {'木 pos':>8}  {'木 in block':>15}  {'Boundary':>20}")
print('-' * 130)

for idx, perm in enumerate(combined):
    z5t = cycle_z5_types(perm)
    els = perm_elements(perm)
    names = perm_names(perm)

    pro = sum(1 for t in z5t if t in ('生↑', '克↑'))
    retro = sum(1 for t in z5t if t in ('生↓', '克↓'))

    wood_pos = [i for i in range(8) if els[i] == 0]  # 木 positions

    # Determine which block each 木 sits in
    # A position i is involved in steps i-1→i and i→i+1
    wood_blocks = []
    for wp in wood_pos:
        # Step ending at wp (from wp-1 to wp)
        step_in = z5t[(wp - 1) % 8]
        # Step starting at wp (from wp to wp+1)
        step_out = z5t[wp]
        wood_blocks.append(f"{step_in}|{step_out}")

    # Find boundaries: where type changes between 生 and 克 (via 比和)
    boundaries = []
    for i in range(8):
        j = (i + 1) % 8
        t_cur, t_next = z5t[i], z5t[j]
        if ('克' in t_cur and '比' in t_next):
            boundaries.append(f"克→比@{j}")
        elif ('比' in t_cur and '生' in t_next):
            boundaries.append(f"比→生@{j}")
        elif ('比' in t_cur and '克' in t_next):
            boundaries.append(f"比→克@{j}")
        elif ('生' in t_cur and '比' in t_next):
            boundaries.append(f"生→比@{j}")

    el_str = ''.join(EL[e] for e in els)
    is_trad = "◀" if perm == TRAD_INDICES else ""
    print(f"{idx+1:>3}  {pro}:{retro}  {el_str:>20}  {' '.join(z5t):>40}  {str(wood_pos):>8}  {', '.join(wood_blocks):>15}  {', '.join(boundaries):>20} {is_trad}")

# Summary: is 木 always at a specific structural position?
print(f"\n--- Summary: 木 structural role ---")

# For each permutation, determine if 木 is at the 克→生 restart point
# "Restart point" = the position where 克 block ends (via 比和) and 生 block begins
wood_at_restart = 0
wood_patterns = Counter()

for perm in combined:
    z5t = cycle_z5_types(perm)
    els = perm_elements(perm)
    wood_pos = set(i for i in range(8) if els[i] == 0)

    # Find restart: step transitions 克→比和 then 比和→生
    # The 比和 step is between positions i and i+1 where both have same element
    # The 木 pair creates a 比和 step, so check if 木's 比和 is the one
    # between 克 and 生 blocks

    bihe_positions = []
    for i in range(8):
        if z5t[i] == '比和':
            # This step goes from position i to i+1
            bihe_positions.append(i)

    # Check if 木 pair creates one of the 比和 steps
    for bp in bihe_positions:
        start, end = bp, (bp + 1) % 8
        if start in wood_pos and end in wood_pos:
            # This 比和 is the 木 pair. Check what's on either side.
            step_before = z5t[(bp - 1) % 8]
            step_after = z5t[(bp + 1) % 8]
            pattern = f"{step_before}→比和(木)→{step_after}"
            wood_patterns[pattern] += 1
            if '克' in step_before:
                wood_at_restart += 1

print(f"木 at 克→比和→生 restart: {wood_at_restart} / {len(combined)}")
print(f"\n木 boundary patterns:")
for pattern, count in sorted(wood_patterns.items(), key=lambda x: -x[1]):
    print(f"  {pattern}: {count}")

# Also check: what about the 金/土 pairs?
print(f"\n--- Paired-element 比和 block analysis ---")
print("Which element pair creates which 比和, and what borders it?\n")

for idx, perm in enumerate(combined):
    z5t = cycle_z5_types(perm)
    els = perm_elements(perm)
    names = perm_names(perm)

    bihe_info = []
    for i in range(8):
        if z5t[i] == '比和':
            start, end = i, (i + 1) % 8
            el_val = els[start]
            step_before = z5t[(i - 1) % 8]
            step_after = z5t[(i + 1) % 8]
            bihe_info.append(f"{EL[el_val]}:{step_before}→比→{step_after}")

    is_trad = "◀" if perm == TRAD_INDICES else ""
    if idx < 16 or perm == TRAD_INDICES:  # Show prograde + traditional
        pro = sum(1 for t in z5t if t in ('生↑', '克↑'))
        retro = sum(1 for t in z5t if t in ('生↓', '克↓'))
        if pro > retro or perm == TRAD_INDICES:
            print(f"  {idx+1:>3}  {' '.join(z5t):>40}  {'  |  '.join(bihe_info)} {is_trad}")


# === Final: the element-level constraint check ===
print_separator("FINAL SELECTION CASCADE")
print("Starting from 40320 permutations, applying cumulative constraints:\n")

all_perms = list(permutations(range(8)))

# Filter stages
stage1 = [p for p in all_perms if check_combined(p)]  # H2 + dir purity

stage2 = []  # + prograde
for p in stage1:
    z5t = cycle_z5_types(p)
    pro = sum(1 for t in z5t if t in ('生↑', '克↑'))
    retro = sum(1 for t in z5t if t in ('生↓', '克↓'))
    if pro > retro:
        stage2.append(p)

stage3 = [p for p in stage2 if TRIGRAMS[p[0]][2] == 1]  # 火 at S

stage4 = []  # + C1∧C2∧C3
for p in stage3:
    earth_pos = element_positions(p, 2)
    metal_pos = element_positions(p, 3)
    wood_pos = element_positions(p, 0)
    c1 = separation(earth_pos[0], earth_pos[1]) == 4
    c2 = separation(metal_pos[0], metal_pos[1]) == 1
    c3 = separation(wood_pos[0], wood_pos[1]) == 1
    if c1 and c2 and c3:
        stage4.append(p)

# Also: 水 at N (position 4)?
stage5 = [p for p in stage4 if TRIGRAMS[p[4]][2] == 4]

print(f"{'Stage':<45} {'Count':>6}  {'Fraction':>10}")
print('-' * 65)
print(f"{'All permutations':<45} {len(all_perms):>6}  {'100%':>10}")
print(f"{'+ H2-segregation + directional purity':<45} {len(stage1):>6}  {100*len(stage1)/40320:.3f}%")
print(f"{'+ prograde (生↑, 克↓)':<45} {len(stage2):>6}  {100*len(stage2)/40320:.4f}%")
print(f"{'+ 火 at S (fix rotation)':<45} {len(stage3):>6}  {100*len(stage3)/40320:.4f}%")
print(f"{'+ 土 antipodal, 金 adj, 木 adj':<45} {len(stage4):>6}  {100*len(stage4)/40320:.5f}%")
print(f"{'+ 水 at N':<45} {len(stage5):>6}  {100*len(stage5)/40320:.5f}%")

if stage5:
    print(f"\n--- Final survivors ---")
    for perm in stage5:
        names = perm_names(perm)
        z5t = cycle_z5_types(perm)
        assign = ' '.join(f'{COMPASS[i]}={names[i]}' for i in range(8))
        is_trad = " ◀ TRADITIONAL" if perm == TRAD_INDICES else ""
        print(f"  {assign}")
        print(f"  Types: {' '.join(z5t)}{is_trad}")


print("\n" + "=" * 70)
print("  DONE")
print("=" * 70)
