"""
Round 2 Comparator Analysis: Broadened Assessment

Tests reader's Round 2 meaning-characterizations against algebraic structure.
8 new pairs assessed: 1 M-rule exception, 3 M-rule conforming, 2 non-M-decisive,
1 complement pair, 1 upper-canon non-M-decisive.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')

from sequence import KING_WEN
from infra import (PAIRS, M_DECISIVE, N_PAIRS, xor6, hex_to_int,
                   KW_O, build_sequence, CONSTRAINTS, CONSTRAINED_PAIRS,
                   FREE_PAIRS, COMPONENTS)
from math import comb

kw_seq = build_sequence(KW_O)

# ═══════════════════════════════════════════════════════════════════════════
# READER'S ROUND 2 PAIRS
# ═══════════════════════════════════════════════════════════════════════════

# Reader assessed 8 pairs (0-indexed):
# Pair 21 (0-idx 20): Sun (#41) / Yi (#42) — 4th M-rule exception
# Pair 17 (0-idx 16): Dun (#33) / Da Zhuang (#34) — M-rule conforming
# Pair 20 (0-idx 19): Jian (#39) / Xie (#40) — M-rule conforming
# Pair 25 (0-idx 24): Ge (#49) / Ding (#50) — M-rule conforming
# Pair 24 (0-idx 23): Kun (#47) / Jing (#48) — non-M-decisive
# Pair 26 (0-idx 25): Zhen (#51) / Gen (#52) — non-M-decisive
# Pair 12 (0-idx 11): Bo (#23) / Fu (#24) — non-M-decisive (upper canon)
# Pair 15 (0-idx 14): Kan (#29) / Li (#30) — complement pair

reader_pairs = {
    20: {'name': 'Sun/Yi', 'reader_first': 'Sun', 'confidence': 'Clear',
         'reader_active': 'complex', 'reader_receptive': 'complex',
         'category': '4th M-rule exception', 'pattern': 'Discipline→Growth'},
    16: {'name': 'Dun/Da Zhuang', 'reader_first': 'Dun', 'confidence': 'Suggestive',
         'reader_active': 'Da Zhuang', 'reader_receptive': 'Dun',
         'category': 'M-rule conforming', 'pattern': 'Receptive→Active'},
    19: {'name': 'Jian/Xie', 'reader_first': 'Jian', 'confidence': 'Clear',
         'reader_active': 'Xie', 'reader_receptive': 'Jian',
         'category': 'M-rule conforming', 'pattern': 'Problem→Solution'},
    24: {'name': 'Ge/Ding', 'reader_first': 'Ge', 'confidence': 'Clear',
         'reader_active': 'Ge', 'reader_receptive': 'Ding',
         'category': 'M-rule conforming', 'pattern': 'Destroy→Build'},
    23: {'name': 'Kun/Jing', 'reader_first': 'Kun', 'confidence': 'Suggestive',
         'reader_active': 'neither', 'reader_receptive': 'neither',
         'category': 'Non-M-decisive', 'pattern': 'Exhaustion→Source'},
    25: {'name': 'Zhen/Gen', 'reader_first': 'Zhen', 'confidence': 'Clear',
         'reader_active': 'Zhen', 'reader_receptive': 'Gen',
         'category': 'Non-M-decisive', 'pattern': 'Movement→Stillness'},
    11: {'name': 'Bo/Fu', 'reader_first': 'Bo', 'confidence': 'Clear',
         'reader_active': 'neither', 'reader_receptive': 'neither',
         'category': 'Non-M-decisive (upper canon)', 'pattern': 'Dissolution→Renewal'},
    14: {'name': 'Kan/Li', 'reader_first': 'Kan', 'confidence': 'Suggestive',
         'reader_active': 'complex', 'reader_receptive': 'complex',
         'category': 'Complement pair', 'pattern': 'Danger→Clarity'},
}

# Round 1 pairs for cumulative analysis
round1_pairs = {
    3: {'name': 'Shi/Bi', 'reader_first': 'Shi', 'confidence': 'Clear',
        'category': 'M-rule exception'},
    5: {'name': 'Tai/Pi', 'reader_first': 'Tai', 'confidence': 'Clear',
        'category': 'M-rule exception'},
    9: {'name': 'Lin/Guan', 'reader_first': 'Lin', 'confidence': 'Clear',
        'category': 'M-rule exception'},
}

all_assessed = {**round1_pairs, **reader_pairs}

# ═══════════════════════════════════════════════════════════════════════════
# 1. DIRECT ALIGNMENT — ROUND 2
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST 1: DIRECT ALIGNMENT — ROUND 2")
print("=" * 70)

hits_r2 = 0
misses_r2 = 0
for k, info in reader_pairs.items():
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    if aligned:
        hits_r2 += 1
    else:
        misses_r2 += 1
    
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    m_decisive = k in M_DECISIVE
    l2_yin_first = (a[1] == 0) if m_decisive else None
    
    # Check pair type
    is_inversion = tuple(a[5-i] for i in range(6)) == b
    is_complement = all(a[i] != b[i] for i in range(6))
    pair_type = "inversion" if is_inversion else ("complement" if is_complement else "other")
    
    orbit = (a[0] ^ a[5], a[1] ^ a[4], a[2] ^ a[3])
    
    print(f"\n  Pair {k+1} ({info['name']}) [{info['category']}]")
    print(f"    Bits: {''.join(map(str,a))} / {''.join(map(str,b))}")
    print(f"    Type: {pair_type}, Orbit: {orbit}")
    print(f"    M-decisive: {m_decisive}", end="")
    if m_decisive:
        print(f", L2=yin first: {l2_yin_first}, Exception: {not l2_yin_first}")
    else:
        print()
    print(f"    KW first: {kw_first}")
    print(f"    Reader predicts: {info['reader_first']} (confidence: {info['confidence']})")
    print(f"    Aligned: {'✓ HIT' if aligned else '✗ MISS'}")

total_r2 = hits_r2 + misses_r2
print(f"\nRound 2: {hits_r2}/{total_r2} hits")

# ═══════════════════════════════════════════════════════════════════════════
# 2. CUMULATIVE ALIGNMENT — ROUNDS 1+2
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 2: CUMULATIVE ALIGNMENT — ROUNDS 1+2")
print("=" * 70)

hits_all = 0
misses_all = 0
for k, info in all_assessed.items():
    kw_first = KING_WEN[2*k][1]
    if kw_first == info['reader_first']:
        hits_all += 1
    else:
        misses_all += 1

total_all = hits_all + misses_all
p_cumulative = sum(comb(total_all, i) * (0.5)**total_all for i in range(hits_all, total_all + 1))

print(f"\nCumulative: {hits_all}/{total_all} hits")
print(f"Expected by chance: {total_all/2:.1f}/{total_all}")
print(f"Binomial p-value (one-sided, >= {hits_all}/{total_all}): {p_cumulative:.6f}")
print(f"  = 1 in {1/p_cumulative:.0f}")

if p_cumulative < 0.05:
    print(f"  *** STATISTICALLY SIGNIFICANT at α=0.05 ***")
if p_cumulative < 0.01:
    print(f"  *** STATISTICALLY SIGNIFICANT at α=0.01 ***")
if p_cumulative < 0.001:
    print(f"  *** STATISTICALLY SIGNIFICANT at α=0.001 ***")

# ═══════════════════════════════════════════════════════════════════════════
# 3. THE 4th EXCEPTION TEST
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 3: THE 4th M-RULE EXCEPTION (Sun/Yi)")
print("=" * 70)

# All 4 M-rule exceptions
exception_pairs_0idx = [3, 5, 9, 20]
all_exception_hits = 0

for k in exception_pairs_0idx:
    a = PAIRS[k]['a']
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    l2_yin_member = name_b if a[1] != 0 else name_a  # L2=yin member
    
    if k in all_assessed:
        reader_first = all_assessed[k]['reader_first']
        aligned_with_exception = (reader_first == name_a)  # KW-first = active member
        if aligned_with_exception:
            all_exception_hits += 1
        
        print(f"\n  Pair {k+1} ({name_a}/{name_b}):")
        print(f"    M-rule would place first: {l2_yin_member}")
        print(f"    KW places first: {name_a}")
        print(f"    Reader predicts: {reader_first}")
        print(f"    Reader agrees with exception: {'✓' if aligned_with_exception else '✗'}")
    else:
        print(f"\n  Pair {k+1}: NOT ASSESSED")

print(f"\nAll 4 M-rule exceptions: {all_exception_hits}/4 meaning-justified")
p_4exc = sum(comb(4, i) * (0.5)**4 for i in range(all_exception_hits, 5))
print(f"Binomial p-value: {p_4exc:.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. M-COMPONENT CORRELATION — EXPANDED
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 4: M-COMPONENT CORRELATION (all assessed M-decisive pairs)")
print("=" * 70)

m_corr_hits = 0
m_corr_total = 0

for k, info in all_assessed.items():
    if k not in M_DECISIVE:
        continue
    
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    l2_yin_member = name_a if a[1] == 0 else name_b
    
    # For this test: does the reader's "receptive" member = L2=yin member?
    reader_receptive = info.get('reader_receptive', info.get('receptive', 'unknown'))
    
    if reader_receptive in ('complex', 'neither', 'unknown'):
        print(f"  Pair {k+1} ({info['name']}): Reader did not clearly identify active/receptive — SKIP")
        continue
    
    match = (l2_yin_member == reader_receptive)
    m_corr_total += 1
    if match:
        m_corr_hits += 1
    
    print(f"  Pair {k+1} ({info['name']}): L2=yin={l2_yin_member}, Reader receptive={reader_receptive} → {'✓' if match else '✗'}")

if m_corr_total > 0:
    print(f"\nM-component = receptive: {m_corr_hits}/{m_corr_total}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. PATTERN ANALYSIS: "Active First" vs "Condition First"
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 5: PATTERN ANALYSIS — Active First vs Condition First")
print("=" * 70)

print("\nThe reader's Round 1 finding was 'active first' — the more active member precedes.")
print("Round 2 CORRECTS this to 'condition first, consequence second'.")
print()
print("Breakdown by pattern type:")
print()

pattern_counts = {}
for k, info in all_assessed.items():
    pattern = info.get('pattern', 'unknown')
    if pattern not in pattern_counts:
        pattern_counts[pattern] = []
    pattern_counts[pattern].append(info['name'])

for pattern, pairs in sorted(pattern_counts.items()):
    print(f"  {pattern}: {', '.join(pairs)}")

# Classify: does the "condition" that comes first tend to be active or receptive?
print("\nIs the first member (the 'condition') typically active or receptive?")
first_is_active = 0
first_is_receptive = 0
first_is_complex = 0

for k, info in all_assessed.items():
    reader_active = info.get('reader_active', info.get('active', 'unknown'))
    reader_first = info['reader_first']
    
    if reader_active in ('complex', 'neither', 'unknown'):
        first_is_complex += 1
    elif reader_active == reader_first:
        first_is_active += 1
    else:
        first_is_receptive += 1

print(f"  Active first: {first_is_active}")
print(f"  Receptive first: {first_is_receptive}")
print(f"  Complex/Neither: {first_is_complex}")
print()
print("→ 'Active first' is not the universal principle. 'Condition first' is.")

# ═══════════════════════════════════════════════════════════════════════════
# 6. BREAKDOWN BY CATEGORY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 6: ALIGNMENT BY CATEGORY")
print("=" * 70)

categories = {}
for k, info in all_assessed.items():
    cat = info['category']
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    if cat not in categories:
        categories[cat] = {'hits': 0, 'total': 0, 'pairs': []}
    categories[cat]['total'] += 1
    if aligned:
        categories[cat]['hits'] += 1
    categories[cat]['pairs'].append(f"{info['name']}({'✓' if aligned else '✗'})")

for cat, data in sorted(categories.items()):
    print(f"\n  {cat}: {data['hits']}/{data['total']}")
    print(f"    Pairs: {', '.join(data['pairs'])}")

# ═══════════════════════════════════════════════════════════════════════════
# 7. CONFIDENCE BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 7: ALIGNMENT BY READER CONFIDENCE")
print("=" * 70)

confidence_levels = {'Clear': {'hits': 0, 'total': 0}, 
                      'Suggestive': {'hits': 0, 'total': 0},
                      'Silent': {'hits': 0, 'total': 0}}

for k, info in all_assessed.items():
    conf = info['confidence']
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    confidence_levels[conf]['total'] += 1
    if aligned:
        confidence_levels[conf]['hits'] += 1

for conf, data in confidence_levels.items():
    if data['total'] > 0:
        print(f"  {conf}: {data['hits']}/{data['total']}")

# ═══════════════════════════════════════════════════════════════════════════
# 8. CANON POSITION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 8: UPPER vs LOWER CANON")
print("=" * 70)

upper_hits = 0
upper_total = 0
lower_hits = 0
lower_total = 0

for k, info in all_assessed.items():
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    if k < 15:  # upper canon
        upper_total += 1
        if aligned:
            upper_hits += 1
    else:
        lower_total += 1
        if aligned:
            lower_hits += 1

print(f"  Upper canon (pairs 1-15): {upper_hits}/{upper_total}")
print(f"  Lower canon (pairs 16-32): {lower_hits}/{lower_total}")

# ═══════════════════════════════════════════════════════════════════════════
# 9. PAIR TYPE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 9: INVERSION vs COMPLEMENT PAIRS")
print("=" * 70)

inv_hits = 0
inv_total = 0
comp_hits = 0
comp_total = 0

for k, info in all_assessed.items():
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    is_inversion = tuple(a[5-i] for i in range(6)) == b
    is_complement = all(a[i] != b[i] for i in range(6))
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    
    if is_inversion:
        inv_total += 1
        if aligned:
            inv_hits += 1
    elif is_complement:
        comp_total += 1
        if aligned:
            comp_hits += 1

print(f"  Inversion pairs: {inv_hits}/{inv_total}")
print(f"  Complement pairs: {comp_hits}/{comp_total}")

# ═══════════════════════════════════════════════════════════════════════════
# 10. THE XUGUA CIRCULARITY CAVEAT
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 10: XUGUA CIRCULARITY ASSESSMENT")
print("=" * 70)

print("""
The reader flagged a critical methodological concern:
The Xugua (Sequence Commentary) was likely written TO RATIONALIZE the 
existing KW ordering. If the reader relies on the Xugua for directional 
logic, the test is partially circular.

The reader self-assessed which pairs have ordering support INDEPENDENT 
of the Xugua (from hexagram meanings alone):

  STRONG (meaning alone predicts ordering):
    Jian/Xie, Ge/Ding, Bo/Fu, Zhen/Gen, Tai/Pi, Shi/Bi, Lin/Guan, Sun/Yi

  WEAKER (Xugua doing more of the work):
    Dun/Da Zhuang, Kun/Jing, Kan/Li

This is an important distinction. If we restrict to Xugua-independent
predictions only (Clear confidence, meaning overdetermines ordering):
""")

strong_hits = 0
strong_total = 0
for k, info in all_assessed.items():
    if info['confidence'] == 'Clear':
        kw_first = KING_WEN[2*k][1]
        if kw_first == info['reader_first']:
            strong_hits += 1
        strong_total += 1

p_strong = sum(comb(strong_total, i) * (0.5)**strong_total for i in range(strong_hits, strong_total + 1))
print(f"  Xugua-independent (Clear only): {strong_hits}/{strong_total}")
print(f"  Binomial p-value: {p_strong:.6f} = 1 in {1/p_strong:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# 11. COVERAGE MAP
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("COVERAGE MAP: Which pairs assessed, which remain")
print("=" * 70)

assessed_set = set(all_assessed.keys())
for k in range(N_PAIRS):
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    status = "ASSESSED" if k in assessed_set else ""
    m_dec = "M-dec" if k in M_DECISIVE else ""
    
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    is_inv = tuple(a[5-i] for i in range(6)) == b
    is_comp = all(a[i] != b[i] for i in range(6))
    ptype = "inv" if is_inv else ("comp" if is_comp else "?")
    
    canon = "upper" if k < 15 else "lower"
    
    if status:
        conf = all_assessed[k]['confidence']
        aligned = "✓" if KING_WEN[2*k][1] == all_assessed[k]['reader_first'] else "✗"
        print(f"  {k+1:2d}  {name_a:>12s}/{name_b:<12s}  {ptype:4s}  {canon:5s}  {m_dec:5s}  {status}  {aligned} {conf}")
    else:
        print(f"  {k+1:2d}  {name_a:>12s}/{name_b:<12s}  {ptype:4s}  {canon:5s}  {m_dec:5s}")

print(f"\nAssessed: {len(assessed_set)}/32 pairs")
print(f"Remaining: {32 - len(assessed_set)}/32 pairs")
