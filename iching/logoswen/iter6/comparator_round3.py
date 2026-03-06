"""
Round 3 Comparator Analysis: Complete 32-Pair Assessment

All 32 pairs now assessed. Full statistical analysis.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')

from sequence import KING_WEN
from infra import (PAIRS, M_DECISIVE, N_PAIRS, xor6, hex_to_int,
                   KW_O, build_sequence, CONSTRAINTS, CONSTRAINED_PAIRS)
from math import comb, log2

kw_seq = build_sequence(KW_O)

# ═══════════════════════════════════════════════════════════════════════════
# ALL 32 PAIRS — Reader's predictions
# ═══════════════════════════════════════════════════════════════════════════

# Complete mapping: 0-indexed pair → reader data
all_pairs = {
    0:  {'reader_first': 'Qian',     'confidence': 'Clear',      'logic': 'Cosmological primacy'},
    1:  {'reader_first': 'Zhun',     'confidence': 'Clear',      'logic': 'Birth→Education'},
    2:  {'reader_first': 'Xu',       'confidence': 'Suggestive', 'logic': 'Need→Conflict'},
    3:  {'reader_first': 'Shi',      'confidence': 'Clear',      'logic': 'Mobilization→Union'},
    4:  {'reader_first': 'Xiao Chu', 'confidence': 'Suggestive', 'logic': 'Restraint→Conduct'},
    5:  {'reader_first': 'Tai',      'confidence': 'Clear',      'logic': 'Flourishing→Decline'},
    6:  {'reader_first': 'Tong Ren', 'confidence': 'Clear',      'logic': 'Fellowship→Abundance'},
    7:  {'reader_first': 'Qian',     'confidence': 'Clear',      'logic': 'Modesty→Enthusiasm'},
    8:  {'reader_first': 'Sui',      'confidence': 'Clear',      'logic': 'Following→Decay'},
    9:  {'reader_first': 'Lin',      'confidence': 'Clear',      'logic': 'Approach→Contemplation'},
    10: {'reader_first': 'Shi He',   'confidence': 'Suggestive', 'logic': 'Justice→Adornment'},
    11: {'reader_first': 'Bo',       'confidence': 'Clear',      'logic': 'Dissolution→Return'},
    12: {'reader_first': 'Wu Wang',  'confidence': 'Suggestive', 'logic': 'Innocence→Accumulation'},
    13: {'reader_first': 'Yi',       'confidence': 'Suggestive', 'logic': 'Nourishment→Excess'},
    14: {'reader_first': 'Kan',      'confidence': 'Suggestive', 'logic': 'Danger→Clarity'},
    15: {'reader_first': 'Xian',     'confidence': 'Clear',      'logic': 'Attraction→Duration'},
    16: {'reader_first': 'Dun',      'confidence': 'Suggestive', 'logic': 'Retreat→Power'},
    17: {'reader_first': 'Jin',      'confidence': 'Clear',      'logic': 'Progress→Darkening'},
    18: {'reader_first': 'Jia Ren',  'confidence': 'Clear',      'logic': 'Family→Opposition'},
    19: {'reader_first': 'Jian',     'confidence': 'Clear',      'logic': 'Obstruction→Deliverance'},
    20: {'reader_first': 'Sun',      'confidence': 'Clear',      'logic': 'Decrease→Increase'},
    21: {'reader_first': 'Guai',     'confidence': 'Clear',      'logic': 'Breakthrough→Encounter'},
    22: {'reader_first': 'Cui',      'confidence': 'Clear',      'logic': 'Gathering→Rising'},
    23: {'reader_first': 'Kun',      'confidence': 'Suggestive', 'logic': 'Oppression→Source'},
    24: {'reader_first': 'Ge',       'confidence': 'Clear',      'logic': 'Revolution→Cauldron'},
    25: {'reader_first': 'Zhen',     'confidence': 'Clear',      'logic': 'Movement→Stillness'},
    26: {'reader_first': 'Jian',     'confidence': 'Suggestive', 'logic': 'Gradual→Hasty'},
    27: {'reader_first': 'Feng',     'confidence': 'Clear',      'logic': 'Abundance→Wandering'},
    28: {'reader_first': 'Xun',      'confidence': 'Suggestive', 'logic': 'Penetrating→Joyous'},
    29: {'reader_first': 'Huan',     'confidence': 'Clear',      'logic': 'Dispersion→Limitation'},
    30: {'reader_first': 'Zhong Fu', 'confidence': 'Suggestive', 'logic': 'Inner Truth→Small Acts'},
    31: {'reader_first': 'Ji Ji',    'confidence': 'Clear',      'logic': 'Completion→Incompletion'},
}

# ═══════════════════════════════════════════════════════════════════════════
# 1. DIRECT ALIGNMENT — ALL 32 PAIRS
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST 1: DIRECT ALIGNMENT — ALL 32 PAIRS")
print("=" * 70)

hits = 0
misses = 0
clear_hits = 0
clear_total = 0
suggestive_hits = 0
suggestive_total = 0

for k in range(N_PAIRS):
    info = all_pairs[k]
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    
    if aligned:
        hits += 1
    else:
        misses += 1
    
    if info['confidence'] == 'Clear':
        clear_total += 1
        if aligned:
            clear_hits += 1
    else:
        suggestive_total += 1
        if aligned:
            suggestive_hits += 1

total = hits + misses
p_all = (0.5)**total
p_clear = sum(comb(clear_total, i) * (0.5)**clear_total 
              for i in range(clear_hits, clear_total + 1))

print(f"\nAll pairs: {hits}/{total}")
print(f"  p-value: {p_all:.2e} (1 in {1/p_all:.0e})")
print(f"\nClear confidence only: {clear_hits}/{clear_total}")
print(f"  p-value: {p_clear:.2e} (1 in {1/p_clear:.0e})")
print(f"\nSuggestive confidence: {suggestive_hits}/{suggestive_total}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. M-RULE EXCEPTION ANALYSIS — COMPLETE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 2: M-RULE ANALYSIS — ALL 16 M-DECISIVE PAIRS")
print("=" * 70)

# Identify all exceptions
exception_pairs = []
conforming_pairs = []

for k in M_DECISIVE:
    a = PAIRS[k]['a']
    l2_yin_first = (a[1] == 0)
    if l2_yin_first:
        conforming_pairs.append(k)
    else:
        exception_pairs.append(k)

print(f"\nM-decisive pairs: {len(M_DECISIVE)}")
print(f"M-rule conforming (L2=yin first): {len(conforming_pairs)} → {[k+1 for k in conforming_pairs]}")
print(f"M-rule exceptions (L2=yang first): {len(exception_pairs)} → {[k+1 for k in exception_pairs]}")

# Check meaning alignment at conforming pairs
print(f"\nConforming pairs — meaning alignment:")
conf_hits = 0
for k in conforming_pairs:
    info = all_pairs[k]
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    if aligned:
        conf_hits += 1
    print(f"  Pair {k+1}: KW={kw_first}, Reader={info['reader_first']} → {'✓' if aligned else '✗'} ({info['confidence']})")
print(f"  Total: {conf_hits}/{len(conforming_pairs)}")

# Check meaning alignment at exception pairs
print(f"\nException pairs — meaning alignment:")
exc_hits = 0
for k in exception_pairs:
    info = all_pairs[k]
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    if aligned:
        exc_hits += 1
    a = PAIRS[k]['a']
    l2_yin_member = KING_WEN[2*k+1][1]  # b has L2=yin since a has L2=yang
    print(f"  Pair {k+1}: KW={kw_first} (L2=yang), M-rule would say {l2_yin_member} first")
    print(f"           Reader={info['reader_first']} → {'✓ AGREES with exception' if aligned else '✗'} ({info['confidence']})")
print(f"  Total: {exc_hits}/{len(exception_pairs)}")

p_exc = sum(comb(len(exception_pairs), i) * (0.5)**len(exception_pairs) 
            for i in range(exc_hits, len(exception_pairs) + 1))
print(f"  p-value: {p_exc:.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. PAIR TYPE BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 3: ALIGNMENT BY PAIR TYPE")
print("=" * 70)

inv_hits = inv_total = 0
comp_hits = comp_total = 0

for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    is_inv = tuple(a[5-i] for i in range(6)) == b
    is_comp = all(a[i] != b[i] for i in range(6))
    
    info = all_pairs[k]
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    
    if is_inv:
        inv_total += 1
        if aligned: inv_hits += 1
    elif is_comp:
        comp_total += 1
        if aligned: comp_hits += 1

print(f"\nInversion pairs: {inv_hits}/{inv_total}")
print(f"Complement pairs: {comp_hits}/{comp_total}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. CANON ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 4: UPPER vs LOWER CANON")
print("=" * 70)

upper_h = upper_t = 0
lower_h = lower_t = 0
upper_clear_h = upper_clear_t = 0
lower_clear_h = lower_clear_t = 0

for k in range(N_PAIRS):
    info = all_pairs[k]
    kw_first = KING_WEN[2*k][1]
    aligned = (kw_first == info['reader_first'])
    
    if k < 15:  # upper canon
        upper_t += 1
        if aligned: upper_h += 1
        if info['confidence'] == 'Clear':
            upper_clear_t += 1
            if aligned: upper_clear_h += 1
    else:
        lower_t += 1
        if aligned: lower_h += 1
        if info['confidence'] == 'Clear':
            lower_clear_t += 1
            if aligned: lower_clear_h += 1

print(f"\nUpper canon (pairs 1-15): {upper_h}/{upper_t}")
print(f"  Clear: {upper_clear_h}/{upper_clear_t}, Suggestive: {upper_h-upper_clear_h}/{upper_t-upper_clear_t}")
print(f"\nLower canon (pairs 16-32): {lower_h}/{lower_t}")
print(f"  Clear: {lower_clear_h}/{lower_clear_t}, Suggestive: {lower_h-lower_clear_h}/{lower_t-lower_clear_t}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. CONFIDENCE × CATEGORY MATRIX
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 5: SUGGESTIVE PAIRS — WHERE MEANING IS WEAKEST")
print("=" * 70)

print("\nThe 10 'Suggestive' pairs (where meaning is weakest):")
for k in range(N_PAIRS):
    if all_pairs[k]['confidence'] == 'Suggestive':
        a = PAIRS[k]['a']
        b = PAIRS[k]['b']
        is_inv = tuple(a[5-i] for i in range(6)) == b
        is_comp = all(a[i] != b[i] for i in range(6))
        ptype = "inv" if is_inv else ("comp" if is_comp else "?")
        m_dec = k in M_DECISIVE
        canon = "upper" if k < 15 else "lower"
        constrained = k in CONSTRAINED_PAIRS
        
        name_a = KING_WEN[2*k][1]
        name_b = KING_WEN[2*k+1][1]
        
        print(f"  Pair {k+1}: {name_a}/{name_b}  [{ptype}, {canon}]"
              f"  M-dec: {'Y' if m_dec else 'N'}  S2-const: {'Y' if constrained else 'N'}"
              f"  Logic: {all_pairs[k]['logic']}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. THE XUGUA CIRCULARITY PROBLEM — QUANTIFIED
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 6: XUGUA CIRCULARITY — QUANTIFIED")
print("=" * 70)

print(f"""
The Xugua (Sequence Commentary) was likely written to rationalize the 
existing KW ordering. This creates a circularity concern.

The reader self-assessed each pair's Xugua dependence:
  Clear (22 pairs): hexagram meanings INDEPENDENTLY predict the ordering
  Suggestive (10 pairs): the Xugua tips the balance

Three significance levels:

  ALL 32 pairs: {hits}/{total} = 100%
    p = {p_all:.2e} (1 in {1/p_all:.0e})
    NOTE: Partially circular via Xugua dependence

  CLEAR-only (22 pairs, Xugua-independent): {clear_hits}/{clear_total} = 100%
    p = {p_clear:.2e} (1 in {1/p_clear:.0e})
    NOTE: Strongest test — meanings overdetermine ordering

  Suggestive-only (10 pairs): {suggestive_hits}/{suggestive_total} = 100%
    Even here, alignment is perfect — but these are the weakest predictions
""")

# ═══════════════════════════════════════════════════════════════════════════
# 7. THE PERFECT ALIGNMENT PROBLEM
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST 7: THE 100% ALIGNMENT PROBLEM")
print("=" * 70)

print("""
32/32 alignment is both the strongest possible finding and the most
suspicious. Several mechanisms could produce 100% besides genuine 
meaning-algebra alignment:

1. XUGUA CIRCULARITY: The Xugua was written to rationalize KW.
   → Addressed above: 22/22 Clear pairs don't depend on Xugua.

2. READER KNOWLEDGE BIAS: The reader knows the traditional ordering
   of these hexagrams and may unconsciously match it.
   → This is the hardest confound to eliminate. The reader IS the 
   tradition in some sense. A truly blind reader would need to work
   from hexagram meanings without knowing the conventional order.

3. POST-HOC RATIONALIZATION: For any pair, a clever reader can 
   construct a rationale for whichever ordering they see.
   → Partially addressed by confidence ratings. 10 pairs rated 
   "Suggestive" acknowledges weaker rationalization power.
   → But 0 pairs rated "Silent" or "Contradictory" is suspicious.
   A genuinely independent reader should find SOME pairs ambiguous.

4. THE XUGUA AS COMMON CAUSE: The Xugua may be the source of BOTH
   the reader's meaning-understanding AND the KW ordering. The 
   hexagram meanings may be less determinative than the reader 
   believes — what feels like "independent meaning" may be Xugua-
   shaped traditional understanding.

ASSESSMENT: The finding is real but its interpretation is bounded.
  - MINIMUM reading: The traditional I Ching framework provides a 
    post-hoc rationale for every orientation choice. This tells us 
    the sequence is COHERENT with meaning, not that meaning DROVE 
    the ordering.
  - MAXIMUM reading: Meaning genuinely determined the ordering, and
    the Xugua is a faithful report of the arranger's reasoning.
  - MIDDLE reading: Meaning was one of several factors (alongside 
    algebraic properties like kac and χ²). The arranger chose 
    orientations that satisfied both meaning AND algebraic criteria 
    simultaneously. The 100% alignment reflects the fact that these 
    criteria are COMPATIBLE, not that meaning alone determined the 
    sequence.
""")

# ═══════════════════════════════════════════════════════════════════════════
# 8. CROSS-REFERENCE: MEANING ALIGNMENT vs ALGEBRAIC PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("TEST 8: MEANING + ALGEBRA CROSS-REFERENCE")
print("=" * 70)

print("\nFor each pair: algebraic properties + meaning alignment")
print()

print(f"{'Pair':>4s}  {'Names':>24s}  {'M-dec':>5s} {'Except':>6s} "
      f"{'S2-con':>6s} {'Type':>4s} {'Canon':>5s} {'Conf':>10s} {'Logic':>30s}")

for k in range(N_PAIRS):
    info = all_pairs[k]
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    is_inv = tuple(a[5-i] for i in range(6)) == b
    is_comp = all(a[i] != b[i] for i in range(6))
    ptype = "inv" if is_inv else ("comp" if is_comp else "?")
    
    m_dec = k in M_DECISIVE
    is_exc = m_dec and a[1] != 0
    constrained = k in CONSTRAINED_PAIRS
    canon = "upper" if k < 15 else "lower"
    
    print(f"  {k+1:2d}  {name_a:>12s}/{name_b:<12s}  "
          f"{'Y' if m_dec else 'N':>3s}   {'Y' if is_exc else ('N' if m_dec else '-'):>4s}   "
          f"{'Y' if constrained else 'N':>4s}   {ptype:>4s} {canon:>5s}  "
          f"{info['confidence']:>10s}  {info['logic']:>30s}")

# ═══════════════════════════════════════════════════════════════════════════
# 9. INFORMATION CONTENT
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("TEST 9: INFORMATION CONTENT OF MEANING ALIGNMENT")
print("=" * 70)

print(f"""
The orientation layer has 32 bits total, 27 free bits (5 forced by S=2).

Meaning alignment provides how many bits of orientation information?

If meaning perfectly predicts all 32 orientations: 32 bits
But we must discount:
  - 5 S=2-forced bits: meaning alignment here is forced, not informative
  - 10 Suggestive pairs: weaker predictions, partially Xugua-dependent

S=2 constrained pairs: """, end="")

s2_pairs = sorted(CONSTRAINED_PAIRS)
s2_clear = sum(1 for k in s2_pairs if all_pairs[k]['confidence'] == 'Clear')
s2_sugg = sum(1 for k in s2_pairs if all_pairs[k]['confidence'] == 'Suggestive')
print(f"{[k+1 for k in s2_pairs]}")
print(f"  Clear: {s2_clear}, Suggestive: {s2_sugg}")

free_pairs = sorted(set(range(32)) - CONSTRAINED_PAIRS)
free_clear = sum(1 for k in free_pairs if all_pairs[k]['confidence'] == 'Clear')
free_sugg = sum(1 for k in free_pairs if all_pairs[k]['confidence'] == 'Suggestive')
print(f"\nFree pairs (22): Clear: {free_clear}, Suggestive: {free_sugg}")

# Information content estimate
print(f"""
Conservative information estimate:
  - 22 Clear pairs × 1 bit each = 22 bits of meaning-driven orientation
  - 10 Suggestive pairs × ~0.5 bits each = ~5 bits 
  - Total: ~27 bits of orientation information from meaning
  - This covers ALL 27 free bits

But this overcounts due to confirmation bias and Xugua circularity.
A more conservative estimate:
  - 22 Clear, non-S2-constrained pairs: {free_clear} bits
  - Minus bias discount (~30%): ~{int(free_clear * 0.7)} bits
  - This is STILL substantial: meaning accounts for ~{int(free_clear * 0.7)} 
    of 27 free orientation bits
""")

# ═══════════════════════════════════════════════════════════════════════════
# 10. FINAL STATISTICS
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("FINAL STATISTICS")
print("=" * 70)

print(f"""
╔══════════════════════════════════════════════════════════╗
║  COMPLETE ALIGNMENT MAP: 32/32 pairs                    ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Direct alignment:          32/32 = 100%                 ║
║  p-value (all):             2.3 × 10⁻¹⁰                 ║
║  p-value (Clear only):      2.4 × 10⁻⁷                  ║
║                                                          ║
║  M-rule exceptions:         4/4 meaning-justified        ║
║  M-rule conforming:         12/12 meaning-aligned        ║
║  Non-M-decisive:            16/16 meaning-aligned        ║
║                                                          ║
║  Upper canon:               15/15                        ║
║  Lower canon:               17/17                        ║
║                                                          ║
║  Inversion pairs:           28/28                        ║
║  Complement pairs:          4/4                          ║
║                                                          ║
║  Clear confidence:          22/22 (69%)                  ║
║  Suggestive confidence:     10/10 (31%)                  ║
║  Silent/Contradictory:      0/32  (0%)                   ║
║                                                          ║
║  Semantic principle:        Developmental priority       ║
║  (condition → consequence, not active → receptive)       ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  CONFOUNDS                                               ║
║  • Xugua circularity (10 pairs partially dependent)      ║
║  • Reader knowledge bias (traditional ordering known)    ║
║  • Zero "Silent" predictions (suspicious — should be >0) ║
║  • Post-hoc rationalization power of rich tradition       ║
╠══════════════════════════════════════════════════════════╣
║  INTERPRETATION                                          ║
║  Minimum: KW is coherent with meaning (post-hoc)         ║
║  Middle:  Meaning was one factor among several            ║
║  Maximum: Meaning determined the orientation              ║
╚══════════════════════════════════════════════════════════╝
""")
