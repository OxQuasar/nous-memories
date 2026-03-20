#!/usr/bin/env python3
"""Uniqueness of the 後天 compass cycle's binary-Z₅ segregation.

Enumerates all 8! trigram→compass assignments to find which produce:
A) Strict H2-segregation: non-trivial Z₅ ↔ Hamming-2, trivial ↔ non-H2
B) Directional purity: all 生 same direction AND all 克 same direction
C) Both A and B combined
D) Element-level: coarser enumeration over element assignments
"""

from itertools import permutations
from collections import Counter

# === Data Definitions ===

EL = {0: '木', 1: '火', 2: '土', 3: '金', 4: '水'}

# 8 trigrams: (name, binary, z5)
TRIGRAMS = [
    ('坎', '010', 4),
    ('坤', '000', 2),
    ('震', '001', 0),
    ('巽', '110', 0),
    ('乾', '111', 3),
    ('兌', '011', 3),
    ('艮', '100', 2),
    ('離', '101', 1),
]

# Compass positions in clockwise order from S
COMPASS_LABELS = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']

# Traditional 後天 assignment (index into TRIGRAMS list)
# S=離, SW=坤, W=兌, NW=乾, N=坎, NE=艮, E=震, SE=巽
TRAD_NAMES = ['離', '坤', '兌', '乾', '坎', '艮', '震', '巽']
TRAD_INDICES = [next(i for i, t in enumerate(TRIGRAMS) if t[0] == n) for n in TRAD_NAMES]

# Z₅ type from directed distance
Z5_TYPE = {0: '比和', 1: '生↑', 4: '生↓', 2: '克↑', 3: '克↓'}


# === Helpers ===

def hamming(bin_a, bin_b):
    """Hamming distance between two 3-bit binary strings."""
    return sum(a != b for a, b in zip(bin_a, bin_b))


def cycle_z5_types(perm):
    """Z₅ type sequence for a cyclic permutation of trigrams.
    perm: tuple of indices into TRIGRAMS, length 8, wraps around."""
    types = []
    for i in range(8):
        j = (i + 1) % 8
        za = TRIGRAMS[perm[i]][2]
        zb = TRIGRAMS[perm[j]][2]
        types.append(Z5_TYPE[(zb - za) % 5])
    return types


def cycle_hamming(perm):
    """Hamming distance sequence for a cyclic permutation."""
    dists = []
    for i in range(8):
        j = (i + 1) % 8
        ba = TRIGRAMS[perm[i]][1]
        bb = TRIGRAMS[perm[j]][1]
        dists.append(hamming(ba, bb))
    return dists


def check_strict_h2(z5_types, ham_dists):
    """Strict H2-segregation: non-trivial Z₅ ↔ H=2, trivial ↔ H≠2."""
    for typ, h in zip(z5_types, ham_dists):
        nontrivial = typ != '比和'
        if nontrivial and h != 2:
            return False
        if not nontrivial and h == 2:
            return False
    return True


def check_weak_h2(z5_types, ham_dists):
    """Weak: every non-trivial step has H=2 (比和 at H=2 allowed)."""
    for typ, h in zip(z5_types, ham_dists):
        if typ != '比和' and h != 2:
            return False
    return True


def check_directional_purity(z5_types):
    """All 生 same direction AND all 克 same direction."""
    sheng = [t for t in z5_types if '生' in t]
    ke = [t for t in z5_types if '克' in t]
    # Must have at least one of each to be meaningful, but also accept
    # vacuously pure (no 生 or no 克)
    if len(set(sheng)) > 1:
        return False
    if len(set(ke)) > 1:
        return False
    return True


def type_counts(z5_types):
    """Count each Z₅ type."""
    return Counter(z5_types)


def prograde_retrograde(z5_types):
    """Return (prograde, retrograde) counts."""
    pro = sum(1 for t in z5_types if t in ('生↑', '克↑'))
    retro = sum(1 for t in z5_types if t in ('生↓', '克↓'))
    return pro, retro


def perm_trigram_names(perm):
    """Trigram names for a permutation."""
    return [TRIGRAMS[i][0] for i in perm]


def perm_z5_values(perm):
    """Z₅ values for a permutation."""
    return [TRIGRAMS[i][2] for i in perm]


def print_separator(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


# === Verify traditional arrangement ===

print_separator("TRADITIONAL 後天 VERIFICATION")

trad_z5 = cycle_z5_types(tuple(TRAD_INDICES))
trad_ham = cycle_hamming(tuple(TRAD_INDICES))
print(f"Assignment: {' '.join(f'{COMPASS_LABELS[i]}={TRAD_NAMES[i]}' for i in range(8))}")
print(f"Z₅ values:  {perm_z5_values(tuple(TRAD_INDICES))}")
print(f"Z₅ types:   {trad_z5}")
print(f"Hamming:     {trad_ham}")
print(f"Strict H2:   {check_strict_h2(trad_z5, trad_ham)}")
print(f"Weak H2:     {check_weak_h2(trad_z5, trad_ham)}")
print(f"Dir purity:  {check_directional_purity(trad_z5)}")
counts = type_counts(trad_z5)
pro, retro = prograde_retrograde(trad_z5)
print(f"Counts:      {dict(counts)}")
print(f"Pro:Retro:   {pro}:{retro}")


# === Task A: Full 8! enumeration ===

print_separator("TASK A: H2-SEGREGATION ENUMERATION (8! = 40320)")

strict_h2_perms = []
weak_h2_perms = []
trad_tuple = tuple(TRAD_INDICES)

for perm in permutations(range(8)):
    z5t = cycle_z5_types(perm)
    hd = cycle_hamming(perm)

    if check_weak_h2(z5t, hd):
        weak_h2_perms.append(perm)
    if check_strict_h2(z5t, hd):
        strict_h2_perms.append(perm)

print(f"Total permutations:    40320")
print(f"Weak H2 matches:       {len(weak_h2_perms)} ({100*len(weak_h2_perms)/40320:.2f}%)")
print(f"Strict H2 matches:     {len(strict_h2_perms)} ({100*len(strict_h2_perms)/40320:.2f}%)")
print(f"Traditional in strict: {trad_tuple in strict_h2_perms}")
print(f"Traditional in weak:   {trad_tuple in weak_h2_perms}")

# Analyze strict matches
if strict_h2_perms:
    print(f"\n--- Strict H2 matches: Z₅ type distributions ---")
    print(f"{'#':>3}  {'Assignment':>40}  {'比和':>3} {'生↑':>3} {'生↓':>3} {'克↑':>3} {'克↓':>3}  {'P:R':>5}  {'Types'}")
    print('-' * 120)
    for idx, perm in enumerate(strict_h2_perms):
        z5t = cycle_z5_types(perm)
        c = type_counts(z5t)
        pro, retro = prograde_retrograde(z5t)
        names = perm_trigram_names(perm)
        assign = ' '.join(f'{COMPASS_LABELS[i]}={names[i]}' for i in range(8))
        trad_mark = " ◀ TRAD" if perm == trad_tuple else ""
        print(f"{idx+1:>3}  {assign:>40}  {c.get('比和',0):>3} {c.get('生↑',0):>3} {c.get('生↓',0):>3} {c.get('克↑',0):>3} {c.get('克↓',0):>3}  {pro}:{retro}  {' '.join(z5t)}{trad_mark}")


# === Task B: Directional purity enumeration ===

print_separator("TASK B: DIRECTIONAL PURITY ENUMERATION")

dir_pure_perms = []
for perm in permutations(range(8)):
    z5t = cycle_z5_types(perm)
    if check_directional_purity(z5t):
        dir_pure_perms.append(perm)

print(f"Directionally pure:    {len(dir_pure_perms)} ({100*len(dir_pure_perms)/40320:.2f}%)")
print(f"Traditional in set:    {trad_tuple in dir_pure_perms}")

# Breakdown by direction pattern
dir_patterns = Counter()
for perm in dir_pure_perms:
    z5t = cycle_z5_types(perm)
    sheng_dirs = set(t for t in z5t if '生' in t)
    ke_dirs = set(t for t in z5t if '克' in t)
    # Pattern: which direction for 生, which for 克 (or "none" if absent)
    s_dir = sheng_dirs.pop() if sheng_dirs else 'none'
    k_dir = ke_dirs.pop() if ke_dirs else 'none'
    dir_patterns[(s_dir, k_dir)] += 1

print(f"\nDirection pattern breakdown:")
print(f"{'生 direction':>12}  {'克 direction':>12}  {'Count':>6}")
print('-' * 35)
for (s, k), cnt in sorted(dir_patterns.items()):
    print(f"{s:>12}  {k:>12}  {cnt:>6}")


# === Task C: Combined (strict H2 AND directional purity) ===

print_separator("TASK C: COMBINED — STRICT H2 + DIRECTIONAL PURITY")

combined_perms = []
for perm in strict_h2_perms:
    z5t = cycle_z5_types(perm)
    if check_directional_purity(z5t):
        combined_perms.append(perm)

print(f"Combined matches:      {len(combined_perms)} ({100*len(combined_perms)/40320:.4f}%)")
print(f"Traditional in set:    {trad_tuple in combined_perms}")

if combined_perms:
    print(f"\n--- All combined matches ---")
    print(f"{'#':>3}  {'Assignment':>55}  {'Z₅ types':>50}  {'P:R':>5}")
    print('-' * 130)
    for idx, perm in enumerate(combined_perms):
        z5t = cycle_z5_types(perm)
        pro, retro = prograde_retrograde(z5t)
        names = perm_trigram_names(perm)
        assign = ' '.join(f'{COMPASS_LABELS[i]}={names[i]}' for i in range(8))
        trad_mark = " ◀ TRAD" if perm == trad_tuple else ""
        print(f"{idx+1:>3}  {assign:>55}  {' '.join(z5t):>50}  {pro}:{retro}{trad_mark}")

    # Structural comparison: what do matches share?
    if len(combined_perms) > 1:
        print(f"\n--- Structural comparison ---")
        # Check which positions have same element across all matches
        n_matches = len(combined_perms)
        for pos in range(8):
            elements_at_pos = set()
            trigrams_at_pos = set()
            for perm in combined_perms:
                elements_at_pos.add(TRIGRAMS[perm[pos]][2])
                trigrams_at_pos.add(TRIGRAMS[perm[pos]][0])
            trigs = ','.join(sorted(trigrams_at_pos))
            els = ','.join(EL[e] for e in sorted(elements_at_pos))
            fixed = "FIXED" if len(elements_at_pos) == 1 else ""
            print(f"  {COMPASS_LABELS[pos]:>3}: elements={{{els}}}  trigrams={{{trigs}}}  {fixed}")

        # Check which trigram pairs always co-occupy the same pair of positions
        print(f"\n  Pair analysis (which element-pairs swap):")
        for perm in combined_perms:
            names = perm_trigram_names(perm)
            z5v = perm_z5_values(perm)
            print(f"    {' '.join(f'{COMPASS_LABELS[i]}:{names[i]}({EL[z5v[i]]})' for i in range(8))}")


# === Task D: Element-level enumeration ===

print_separator("TASK D: ELEMENT-LEVEL ENUMERATION")
print("Element partition: 木×2, 火×1, 土×2, 金×2, 水×1 = {0,0,1,2,2,3,3,4}")
print("Distinct assignments: 8!/(2!×2!×2!) = 5040\n")

# Generate distinct element permutations
base_elements = (0, 0, 1, 2, 2, 3, 3, 4)
seen = set()
element_perms = []
for p in permutations(base_elements):
    if p not in seen:
        seen.add(p)
        element_perms.append(p)

print(f"Generated {len(element_perms)} distinct element permutations (expected 5040)")

# Traditional element sequence: S=火, SW=土, W=金, NW=金, N=水, NE=土, E=木, SE=木
trad_el = tuple(TRIGRAMS[i][2] for i in TRAD_INDICES)
print(f"Traditional element sequence: {trad_el} = {tuple(EL[e] for e in trad_el)}")

# For each element assignment, check directional purity
# All-prograde 生 + all-retrograde 克 (like traditional)
# Also check all 4 direction combinations

def el_cycle_z5_types(el_seq):
    """Z₅ type sequence for element sequence (length 8, cyclic)."""
    types = []
    for i in range(8):
        j = (i + 1) % 8
        types.append(Z5_TYPE[(el_seq[j] - el_seq[i]) % 5])
    return types

dir_pure_el = []
trad_pattern_el = []  # 生↑ + 克↓ specifically

for el in element_perms:
    z5t = el_cycle_z5_types(el)
    if check_directional_purity(z5t):
        dir_pure_el.append(el)
        sheng_dirs = set(t for t in z5t if '生' in t)
        ke_dirs = set(t for t in z5t if '克' in t)
        s_dir = sheng_dirs.pop() if sheng_dirs else 'none'
        k_dir = ke_dirs.pop() if ke_dirs else 'none'
        if s_dir == '生↑' and k_dir == '克↓':
            trad_pattern_el.append(el)

print(f"\nDirectionally pure (any combo): {len(dir_pure_el)} ({100*len(dir_pure_el)/5040:.2f}%)")
print(f"Traditional pattern (生↑+克↓):   {len(trad_pattern_el)} ({100*len(trad_pattern_el)/5040:.2f}%)")
print(f"Traditional in set:              {trad_el in trad_pattern_el}")

# Breakdown by direction pattern
el_dir_patterns = Counter()
for el in dir_pure_el:
    z5t = el_cycle_z5_types(el)
    sheng_dirs = set(t for t in z5t if '生' in t)
    ke_dirs = set(t for t in z5t if '克' in t)
    s_dir = sheng_dirs.pop() if sheng_dirs else 'none'
    k_dir = ke_dirs.pop() if ke_dirs else 'none'
    c = type_counts(z5t)
    el_dir_patterns[(s_dir, k_dir)] += 1

print(f"\nDirection pattern breakdown:")
print(f"{'生 direction':>12}  {'克 direction':>12}  {'Count':>6}")
print('-' * 35)
for (s, k), cnt in sorted(el_dir_patterns.items()):
    print(f"{s:>12}  {k:>12}  {cnt:>6}")

# List traditional-pattern matches if manageable
if len(trad_pattern_el) <= 50:
    print(f"\n--- All 生↑+克↓ element assignments ---")
    print(f"{'#':>3}  {'Element sequence':>30}  {'Z₅ types':>50}  {'比和':>3} {'生↑':>3} {'克↓':>3}  {'P:R':>5}")
    print('-' * 110)
    for idx, el in enumerate(trad_pattern_el):
        z5t = el_cycle_z5_types(el)
        c = type_counts(z5t)
        pro, retro = prograde_retrograde(z5t)
        el_names = tuple(EL[e] for e in el)
        trad_mark = " ◀ TRAD" if el == trad_el else ""
        print(f"{idx+1:>3}  {str(el_names):>30}  {' '.join(z5t):>50}  {c.get('比和',0):>3} {c.get('生↑',0):>3} {c.get('克↓',0):>3}  {pro}:{retro}{trad_mark}")

# Also check: element assignments with strict H2 + dir purity
# For this we need to map back to trigram assignments
# An element assignment is compatible with H2-segregation only if there exist
# trigram assignments realizing it that satisfy H2-segregation.
# But we can check at element level: which 比和 positions could have H≠2?
# 比和 means same element → either same trigram (impossible, distinct) or
# the two same-element trigrams are adjacent. Check Hamming distances within
# element pairs.
print_separator("TASK D EXTRA: INTRA-ELEMENT HAMMING DISTANCES")
print("For 比和 steps (same element), the two trigrams must have H≠2 for strict segregation.")
print("For non-trivial steps, the two trigrams must have H=2.\n")

# Hamming distances between same-element trigram pairs
element_trigrams = {}
for name, binary, z5 in TRIGRAMS:
    element_trigrams.setdefault(z5, []).append((name, binary))

print("Intra-element pairs (potential 比和 transitions):")
for z5val in sorted(element_trigrams.keys()):
    trigs = element_trigrams[z5val]
    if len(trigs) >= 2:
        for i in range(len(trigs)):
            for j in range(i+1, len(trigs)):
                h = hamming(trigs[i][1], trigs[j][1])
                print(f"  {EL[z5val]}(Z₅={z5val}): {trigs[i][0]}({trigs[i][1]}) ↔ {trigs[j][0]}({trigs[j][1]})  H={h}")

# Cross-element Hamming-2 pairs (potential non-trivial transitions at H=2)
print("\nCross-element Hamming-2 pairs:")
for i in range(8):
    for j in range(i+1, 8):
        if TRIGRAMS[i][2] != TRIGRAMS[j][2]:
            h = hamming(TRIGRAMS[i][1], TRIGRAMS[j][1])
            if h == 2:
                za, zb = TRIGRAMS[i][2], TRIGRAMS[j][2]
                typ_fwd = Z5_TYPE[(zb - za) % 5]
                typ_rev = Z5_TYPE[(za - zb) % 5]
                print(f"  {TRIGRAMS[i][0]}({TRIGRAMS[i][1]},{EL[za]}) ↔ {TRIGRAMS[j][0]}({TRIGRAMS[j][1]},{EL[zb]})  H=2  {typ_fwd}/{typ_rev}")


print("\n" + "=" * 70)
print("  DONE")
print("=" * 70)
