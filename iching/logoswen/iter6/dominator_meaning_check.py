"""
Addendum to iter6: Do the 12 Hamming-2+ dominators violate developmental priority?

Cross-references iter5 dominator data with iter6 meaning alignment.
"""
import sys, json
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')

from sequence import KING_WEN
from infra import FREE_PAIRS, COMPONENTS, COMPONENT_VALID, PAIRS

# ── Build free-bit → pair mapping ────────────────────────────────────────────

free_bit_map = []
for p in FREE_PAIRS:
    free_bit_map.append({'bit': len(free_bit_map), 'type': 'single', 'pairs': [p]})
for (p1, p2), valid in COMPONENT_VALID.items():
    free_bit_map.append({'bit': len(free_bit_map), 'type': 'component', 'pairs': [p1, p2]})

print("=" * 70)
print("FREE BIT → PAIR MAPPING")
print("=" * 70)
for fb in free_bit_map:
    pair_names = []
    for p in fb['pairs']:
        a_name = KING_WEN[2*p][1]
        b_name = KING_WEN[2*p+1][1]
        pair_names.append(f"pair {p} ({a_name}/{b_name})")
    print(f"  Free bit {fb['bit']:2d} [{fb['type']:9s}] → {', '.join(pair_names)}")

# ── Alignment map data (from iter6) ─────────────────────────────────────────
# pair_idx is 0-indexed. KW ordering = 'a' first.
# dev_priority: which comes first under condition→consequence
# conf: Clear or Sugg

ALIGNMENT = {
    0:  {'names': 'Qian/Kun',           'logic': 'Cosmological primacy',       'conf': 'Clear'},
    1:  {'names': 'Zhun/Meng',          'logic': 'Birth → Education',          'conf': 'Clear'},
    2:  {'names': 'Xu/Song',            'logic': 'Need → Conflict',            'conf': 'Sugg'},
    3:  {'names': 'Shi/Bi',             'logic': 'Mobilization → Union',       'conf': 'Clear'},
    4:  {'names': 'Xiao Chu/Lü',        'logic': 'Restraint → Conduct',        'conf': 'Sugg'},
    5:  {'names': 'Tai/Pi',             'logic': 'Flourishing → Decline',      'conf': 'Clear'},
    6:  {'names': 'Tong Ren/Da You',    'logic': 'Fellowship → Abundance',     'conf': 'Clear'},
    7:  {'names': 'Qian/Yu',            'logic': 'Modesty → Enthusiasm',       'conf': 'Clear'},
    8:  {'names': 'Sui/Gu',             'logic': 'Following → Decay',          'conf': 'Clear'},
    9:  {'names': 'Lin/Guan',           'logic': 'Approach → Contemplation',   'conf': 'Clear'},
    10: {'names': 'Shi He/Bi',          'logic': 'Justice → Adornment',        'conf': 'Sugg'},
    11: {'names': 'Bo/Fu',              'logic': 'Dissolution → Return',       'conf': 'Clear'},
    12: {'names': 'Wu Wang/Da Chu',     'logic': 'Innocence → Accumulation',   'conf': 'Sugg'},
    13: {'names': 'Yi/Da Guo',          'logic': 'Nourishment → Excess',       'conf': 'Sugg',  's2': True},
    14: {'names': 'Kan/Li',             'logic': 'Danger → Clarity',           'conf': 'Sugg',  's2': True},
    15: {'names': 'Xian/Heng',          'logic': 'Attraction → Duration',      'conf': 'Clear'},
    16: {'names': 'Dun/Da Zhuang',      'logic': 'Retreat → Power',            'conf': 'Sugg'},
    17: {'names': 'Jin/Ming Yi',        'logic': 'Progress → Darkening',       'conf': 'Clear'},
    18: {'names': 'Jia Ren/Kui',        'logic': 'Family → Opposition',        'conf': 'Clear'},
    19: {'names': 'Jian/Xie',           'logic': 'Obstruction → Deliverance',  'conf': 'Clear', 's2': True},
    20: {'names': 'Sun/Yi',             'logic': 'Decrease → Increase',        'conf': 'Clear', 's2': True},
    21: {'names': 'Guai/Gou',           'logic': 'Breakthrough → Encounter',   'conf': 'Clear'},
    22: {'names': 'Cui/Sheng',          'logic': 'Gathering → Rising',         'conf': 'Clear'},
    23: {'names': 'Kun/Jing',           'logic': 'Oppression → Source',        'conf': 'Sugg'},
    24: {'names': 'Ge/Ding',            'logic': 'Revolution → Cauldron',      'conf': 'Clear'},
    25: {'names': 'Zhen/Gen',           'logic': 'Movement → Stillness',       'conf': 'Clear', 's2': True},
    26: {'names': 'Jian/Gui Mei',       'logic': 'Gradual → Hasty',            'conf': 'Sugg',  's2': True},
    27: {'names': 'Feng/Lü',            'logic': 'Abundance → Wandering',      'conf': 'Clear', 's2': True},
    28: {'names': 'Xun/Dui',            'logic': 'Penetrating → Joyous',       'conf': 'Sugg',  's2': True},
    29: {'names': 'Huan/Jie',           'logic': 'Dispersion → Limitation',    'conf': 'Clear'},
    30: {'names': 'Zhong Fu/Xiao Guo',  'logic': 'Inner Truth → Small Acts',   'conf': 'Sugg',  's2': True},
    31: {'names': 'Ji Ji/Wei Ji',       'logic': 'Completion → Incompletion',  'conf': 'Clear'},
}

# ── 12 Dominator orientations (from iter5 round3) ───────────────────────────
# Stored as free-bit sets that are flipped from KW (all-zeros)

DOMINATORS = [
    {'id': 1,  'free_bits': {17, 26}},
    {'id': 2,  'free_bits': {9, 10, 16, 17}},
    {'id': 3,  'free_bits': {9, 17, 23, 24}},
    {'id': 4,  'free_bits': {0, 6, 9, 17, 23}},
    {'id': 5,  'free_bits': {6, 9, 15, 17, 23}},
    {'id': 6,  'free_bits': {9, 10, 16, 17, 23}},
    {'id': 7,  'free_bits': {9, 11, 17, 23, 24}},
    {'id': 8,  'free_bits': {9, 15, 17, 20, 23}},
    {'id': 9,  'free_bits': {9, 15, 17, 21, 23}},
    {'id': 10, 'free_bits': {9, 10, 11, 16, 17, 26}},
    {'id': 11, 'free_bits': {9, 11, 15, 17, 23, 24}},
    {'id': 12, 'free_bits': {9, 11, 17, 23, 24, 26}},
]

# ── Check each dominator ────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("DOMINATOR MEANING ANALYSIS")
print("=" * 70)

# First: which pairs does each free bit flip?
def free_bits_to_pairs(fb_set):
    """Convert a set of free bit indices to the set of pair indices flipped."""
    flipped = set()
    for fb in fb_set:
        entry = free_bit_map[fb]
        for p in entry['pairs']:
            flipped.add(p)
    return flipped

all_flipped_pairs = set()
for dom in DOMINATORS:
    pairs_flipped = free_bits_to_pairs(dom['free_bits'])
    dom['pairs_flipped'] = pairs_flipped
    all_flipped_pairs |= pairs_flipped

    print(f"\nDominator #{dom['id']} (free bits: {sorted(dom['free_bits'])})")
    print(f"  Pairs flipped: {sorted(pairs_flipped)}")
    violations = []
    for p in sorted(pairs_flipped):
        a = ALIGNMENT[p]
        reversed_logic = ' → '.join(reversed(a['logic'].split(' → '))) if ' → ' in a['logic'] else f"[reversed: {a['logic']}]"
        is_s2 = a.get('s2', False)
        s2_tag = " [S2-constrained]" if is_s2 else ""
        print(f"    Pair {p:2d} ({a['names']:25s}): {a['logic']:35s} [{a['conf']}]{s2_tag}")
        print(f"      Reversed → {reversed_logic}")
        violations.append({'pair': p, 'names': a['names'], 'logic': a['logic'],
                          'conf': a['conf'], 's2': is_s2})

    clear_violations = sum(1 for v in violations if v['conf'] == 'Clear' and not v.get('s2'))
    sugg_violations = sum(1 for v in violations if v['conf'] == 'Sugg' and not v.get('s2'))
    s2_violations = sum(1 for v in violations if v.get('s2'))
    print(f"  → {clear_violations} Clear violations, {sugg_violations} Sugg violations, {s2_violations} S2-constrained")

# ── Summary ─────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"\nAll pairs flipped across any dominator: {sorted(all_flipped_pairs)}")
print(f"\nPer-pair flip frequency across 12 dominators:")
from collections import Counter
pair_freq = Counter()
for dom in DOMINATORS:
    for p in dom['pairs_flipped']:
        pair_freq[p] += 1

for p, count in pair_freq.most_common():
    a = ALIGNMENT[p]
    s2_tag = " [S2]" if a.get('s2', False) else ""
    print(f"  Pair {p:2d} ({a['names']:25s}): {count:2d}/12  [{a['conf']}]  {a['logic']}{s2_tag}")

# ── The key question ────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("KEY QUESTION: Do dominators violate developmental priority?")
print("=" * 70)

# Every pair flipped by a dominator has its KW ordering reversed.
# Since KW aligns with developmental priority at 32/32, reversing = violating.
# The question is how many and how severe.

total_pair_flips = sum(len(dom['pairs_flipped']) for dom in DOMINATORS)
clear_free_flips = 0
sugg_free_flips = 0
s2_flips = 0

for dom in DOMINATORS:
    for p in dom['pairs_flipped']:
        a = ALIGNMENT[p]
        if a.get('s2'):
            s2_flips += 1
        elif a['conf'] == 'Clear':
            clear_free_flips += 1
        else:
            sugg_free_flips += 1

print(f"\nAcross all 12 dominators:")
print(f"  Total pair-reversals: {total_pair_flips}")
print(f"  Clear dev-priority violations (free pairs): {clear_free_flips}")
print(f"  Suggestive dev-priority violations (free pairs): {sugg_free_flips}")
print(f"  S2-constrained reversals: {s2_flips}")
print(f"\nEvery dominator reverses at least {min(len(dom['pairs_flipped']) for dom in DOMINATORS)} pairs with established developmental priority.")

# ── Note on the label error ─────────────────────────────────────────────────

print("\n" + "=" * 70)
print("NOTE: LABEL CORRECTION")
print("=" * 70)
print("The iter5 findings label free bit 17 as 'pair 21 (Lin/Guan)'.")
print("This is a mislabel. Free bit 17 → pair index 21 (0-indexed) = Guai/Gou.")
print("Lin/Guan is pair index 9 (0-indexed), which is free bit 9.")
fb9 = free_bit_map[9]
fb17 = free_bit_map[17]
print(f"  Free bit 9 → pair {fb9['pairs'][0]} = {KING_WEN[2*fb9['pairs'][0]][1]}/{KING_WEN[2*fb9['pairs'][0]+1][1]}")
print(f"  Free bit 17 → pair {fb17['pairs'][0]} = {KING_WEN[2*fb17['pairs'][0]][1]}/{KING_WEN[2*fb17['pairs'][0]+1][1]}")
