"""
Round 1 Comparator Analysis: M-Rule Exception Pairs

Tests reader's meaning-characterizations against algebraic structure.
The captain assigned three pairs. The question: are these the M-rule exception pairs,
and does meaning predict the same ordering that KW uses?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')

from sequence import KING_WEN
from infra import (PAIRS, M_DECISIVE, N_PAIRS, xor6, hex_to_int,
                   KW_O, build_sequence, compute_m_score)

# ═══════════════════════════════════════════════════════════════════════════
# 1. IDENTIFY ALL PAIRS AND THEIR PROPERTIES
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("ALL 32 PAIRS: M-COMPONENT ANALYSIS")
print("=" * 70)

kw_seq = build_sequence(KW_O)

print(f"\nM-decisive pairs (0-indexed): {M_DECISIVE}")
print(f"Total M-decisive: {len(M_DECISIVE)}")

print(f"\n{'Pair':>4s}  {'#A':>3s} {'Name A':>12s} {'#B':>3s} {'Name B':>12s}  "
      f"{'L2a':>3s} {'L5a':>3s}  {'M-dec':>5s}  {'L2=yin?':>7s}  {'KW=M?':>5s}")

m_rule_hits = 0
m_rule_misses = 0
exception_pairs = []

for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    num_a = KING_WEN[2*k][0]
    num_b = KING_WEN[2*k+1][0]
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    l2_a = a[1]  # L2 of first member (KW order)
    l5_a = a[4]  # L5 of first member
    
    m_decisive = k in M_DECISIVE
    l2_yin_first = (l2_a == 0)  # Does first member have L2=yin?
    
    if m_decisive:
        if l2_yin_first:
            m_rule_hits += 1
            kw_follows_m = "YES"
        else:
            m_rule_misses += 1
            kw_follows_m = "NO ***"
            exception_pairs.append(k)
    else:
        kw_follows_m = "n/a"
    
    print(f"  {k+1:3d}  {num_a:3d} {name_a:>12s} {num_b:3d} {name_b:>12s}  "
          f"  {l2_a}   {l5_a}    {'Y' if m_decisive else 'N':>3s}     "
          f"{'Y' if l2_yin_first else 'N':>3s}     {kw_follows_m}")

print(f"\nM-rule: {m_rule_hits} hits / {m_rule_misses} misses out of {len(M_DECISIVE)} M-decisive pairs")
print(f"M-rule exceptions (0-indexed): {exception_pairs}")
print(f"M-rule exceptions (1-indexed): {[p+1 for p in exception_pairs]}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. IDENTIFY THE READER'S PAIRS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("READER'S ASSIGNED PAIRS")
print("=" * 70)

# The reader assessed:
# Pair A: Shi (#7) / Bi (#8) — pair index 3 (0-indexed)
# Pair B: Tai (#11) / Pi (#12) — pair index 5 (0-indexed)
# Pair C: Lin (#19) / Guan (#20) — pair index 9 (0-indexed)

reader_pairs = {
    3: {'name': 'Shi/Bi', 'reader_first': 'Shi', 'reader_prediction': 'Shi first',
        'confidence': 'Clear', 'active': 'Shi', 'receptive': 'Bi'},
    5: {'name': 'Tai/Pi', 'reader_first': 'Tai', 'reader_prediction': 'Tai first',
        'confidence': 'Clear', 'active': 'Tai', 'receptive': 'Pi'},
    9: {'name': 'Lin/Guan', 'reader_first': 'Lin', 'reader_prediction': 'Lin first',
        'confidence': 'Clear', 'active': 'Lin', 'receptive': 'Guan'},
}

for k, info in reader_pairs.items():
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    num_a = KING_WEN[2*k][0]
    num_b = KING_WEN[2*k+1][0]
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    kw_first = name_a
    reader_first = info['reader_first']
    
    l2_a = a[1]
    l5_a = a[4]
    m_decisive = k in M_DECISIVE
    l2_yin_first = (l2_a == 0)
    
    is_exception = k in exception_pairs
    
    # Binary comparison
    int_a = hex_to_int(a)
    int_b = hex_to_int(b)
    
    print(f"\n  Pair {k+1} (0-idx {k}): {name_a} (#{num_a}) / {name_b} (#{num_b})")
    print(f"    Bits A: {''.join(map(str,a))}  Bits B: {''.join(map(str,b))}")
    print(f"    Binary int A: {int_a}  Binary int B: {int_b}  Higher first: {'A' if int_a > int_b else 'B'}")
    print(f"    L2(A)={l2_a}, L5(A)={l5_a} → M-decisive: {m_decisive}")
    if m_decisive:
        print(f"    L2=yin first? {l2_yin_first} → M-rule exception: {is_exception}")
    print(f"    KW ordering: {kw_first} first")
    print(f"    Reader prediction: {reader_first} first (confidence: {info['confidence']})")
    print(f"    ALIGNMENT: {'HIT' if kw_first == reader_first else 'MISS'}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. THE KEY TEST: Were these the M-rule exception pairs?
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("CRITICAL QUESTION: ARE THESE THE M-RULE EXCEPTION PAIRS?")
print("=" * 70)

assigned_pairs = list(reader_pairs.keys())
print(f"\nAssigned pairs (0-indexed): {assigned_pairs}")
print(f"M-rule exception pairs (0-indexed): {exception_pairs}")
print(f"Overlap: {set(assigned_pairs) & set(exception_pairs)}")
print(f"Are all assigned pairs M-rule exceptions? {set(assigned_pairs) == set(exception_pairs)}")
print(f"Are all assigned pairs M-decisive? {all(k in M_DECISIVE for k in assigned_pairs)}")

for k in assigned_pairs:
    a = PAIRS[k]['a']
    l2_a = a[1]
    l5_a = a[4]
    m_dec = k in M_DECISIVE
    is_exc = k in exception_pairs
    name_a = KING_WEN[2*k][1]
    print(f"\n  Pair {k+1}: {name_a} is KW-first")
    print(f"    L2(first)={l2_a}, L5(first)={l5_a}")
    print(f"    M-decisive: {m_dec}")
    if m_dec:
        print(f"    L2=yin first (M-rule default): {l2_a == 0}")
        print(f"    M-rule exception: {is_exc}")
        if is_exc:
            print(f"    → KW places L2=YANG first here, BREAKING the M-rule default")
    else:
        print(f"    → Not M-decisive (L2 == L5), M-rule doesn't apply")

# ═══════════════════════════════════════════════════════════════════════════
# 4. ALIGNMENT STATISTICS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("ALIGNMENT STATISTICS")
print("=" * 70)

hits = 0
misses = 0
for k, info in reader_pairs.items():
    kw_first = KING_WEN[2*k][1]
    if kw_first == info['reader_first']:
        hits += 1
    else:
        misses += 1

total = hits + misses
print(f"\nDirect alignment: {hits}/{total} hits")
print(f"Expected by chance: {total/2:.1f}/{total}")

# Binomial test (manual)
from math import comb
if total > 0:
    p_value = sum(comb(total, i) * (0.5)**total for i in range(hits, total + 1))
    print(f"Binomial p-value (one-sided, >= {hits}/{total}): {p_value:.4f}")
    print(f"Note: n=3 is very small. 3/3 has p=0.125 against 50% null.")

# ═══════════════════════════════════════════════════════════════════════════
# 5. M-COMPONENT CORRELATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("M-COMPONENT CORRELATION")
print("=" * 70)

print("\nQuestion: Among M-decisive pairs, does the reader's 'more receptive'")
print("member correspond to L2=yin?")

for k, info in reader_pairs.items():
    if k not in M_DECISIVE:
        print(f"\n  Pair {k+1}: Not M-decisive, skip")
        continue
    
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    # Which member has L2=yin?
    l2_a_yin = (a[1] == 0)
    l2_b_yin = (b[1] == 0)
    
    l2_yin_member = name_a if l2_a_yin else name_b
    reader_receptive = info['receptive']
    
    print(f"\n  Pair {k+1} ({info['name']}):")
    print(f"    L2=yin member: {l2_yin_member}")
    print(f"    Reader's 'more receptive': {reader_receptive}")
    print(f"    Match: {l2_yin_member == reader_receptive}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. EXCEPTION TEST
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("THE EXCEPTION TEST")
print("=" * 70)

print("\nThe M-rule says: place L2=yin first (12/16 M-decisive pairs do this).")
print("The 3 exceptions break this rule. Does the reader's meaning-based")
print("ordering ALSO break the expected pattern?")
print()
print("The M-rule default would predict: 'more receptive first' (L2=yin first)")
print("At exception pairs, KW instead places 'more active first' (L2=yang first)")
print("Does the reader's meaning analysis AGREE with this exception?")

m_rule_default_meaning = "receptive first"
exception_meaning_justified = 0

for k in exception_pairs:
    if k not in reader_pairs:
        print(f"\n  Pair {k+1}: NOT ASSESSED BY READER")
        continue
    
    info = reader_pairs[k]
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    
    # L2=yin member is the "M-rule preferred" first member
    l2_a_yin = (a[1] == 0)
    m_rule_would_place_first = name_a if l2_a_yin else name_b
    kw_actually_places_first = name_a  # by definition, pair[0] is KW-first
    
    # Reader's prediction
    reader_first = info['reader_first']
    
    print(f"\n  Pair {k+1} ({info['name']}):")
    print(f"    M-rule would place first: {m_rule_would_place_first}")
    print(f"    KW actually places first: {kw_actually_places_first}")
    print(f"    Reader predicts first: {reader_first}")
    
    if reader_first == kw_actually_places_first and reader_first != m_rule_would_place_first:
        print(f"    → Reader AGREES with the exception (meaning justifies the override)")
        exception_meaning_justified += 1
    elif reader_first == kw_actually_places_first:
        print(f"    → Reader agrees with KW (but this isn't an override case)")
    else:
        print(f"    → Reader disagrees with KW ordering")

print(f"\nException test score: {exception_meaning_justified}/{len([k for k in exception_pairs if k in reader_pairs])}")
print("Interpretation:")
print("  3/3 → Meaning and algebra deeply integrated at conflict points")
print("  2/3 → Partial integration")
print("  1/3 → Weak")
print("  0/3 → Override is purely structural")

# ═══════════════════════════════════════════════════════════════════════════
# 7. PAIR TYPE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PAIR TYPE ANALYSIS")
print("=" * 70)

for k in reader_pairs:
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    # Check if inversion pair (b = reverse(a))
    is_inversion = tuple(a[5-i] for i in range(6)) == b
    # Check if complement pair (b = ~a)
    is_complement = all(a[i] != b[i] for i in range(6))
    
    pair_type = "inversion" if is_inversion else ("complement" if is_complement else "other")
    
    # XOR mask
    mask = xor6(a, b)
    
    # Orbit signature
    orbit = (a[0] ^ a[5], a[1] ^ a[4], a[2] ^ a[3])
    
    print(f"\n  Pair {k+1} ({name_a}/{name_b}):")
    print(f"    Type: {pair_type}")
    print(f"    Mask: {''.join(map(str, mask))}")
    print(f"    Orbit: {orbit}")
    print(f"    Hamming weight A: {sum(a)}  B: {sum(b)}")
