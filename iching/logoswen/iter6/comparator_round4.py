"""
Round 4 Comparator Analysis: Reversal Defensibility Test

Not a new alignment test — the 32/32 is established.
This round tests the STRENGTH of alignment: how constrained are the 
weakest pairs? Can reversals be equally defended?

The captain selected two pairs for reversal testing:
  Pair 18 (Jin/Ming Yi) — Clear confidence, non-M-decisive
  Pair 27 (Jian/Gui Mei) — Suggestive confidence, M-decisive, S2-constrained

These represent opposite ends of the meaning-constraint spectrum.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')

from sequence import KING_WEN
from infra import (PAIRS, M_DECISIVE, N_PAIRS, xor6, hex_to_int,
                   KW_O, build_sequence, compute_all_metrics,
                   CONSTRAINTS, CONSTRAINED_PAIRS)

kw_seq = build_sequence(KW_O)

# ═══════════════════════════════════════════════════════════════════════════
# 1. ALGEBRAIC PROPERTIES OF THE TWO TESTED PAIRS
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("ALGEBRAIC PROPERTIES OF REVERSAL-TESTED PAIRS")
print("=" * 70)

test_pairs = [17, 26]  # 0-indexed: pair 18 and pair 27

for k in test_pairs:
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    num_a = KING_WEN[2*k][0]
    num_b = KING_WEN[2*k+1][0]
    
    is_inv = tuple(a[5-i] for i in range(6)) == b
    is_comp = all(a[i] != b[i] for i in range(6))
    ptype = "inversion" if is_inv else ("complement" if is_comp else "other")
    
    m_dec = k in M_DECISIVE
    is_exc = m_dec and a[1] != 0
    s2_const = k in CONSTRAINED_PAIRS
    
    orbit = (a[0] ^ a[5], a[1] ^ a[4], a[2] ^ a[3])
    
    print(f"\n  Pair {k+1}: {name_a} (#{num_a}) / {name_b} (#{num_b})")
    print(f"    Bits A: {''.join(map(str,a))}")
    print(f"    Bits B: {''.join(map(str,b))}")
    print(f"    Type: {ptype}, Orbit: {orbit}")
    print(f"    L2(A)={a[1]}, L5(A)={a[4]}")
    print(f"    M-decisive: {m_dec}", end="")
    if m_dec:
        l2_yin_first = (a[1] == 0)
        print(f", L2=yin first: {l2_yin_first}, Exception: {not l2_yin_first}")
    else:
        print()
    print(f"    S2-constrained: {s2_const}")
    print(f"    Canon: {'upper' if k < 15 else 'lower'}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. WHAT HAPPENS ALGEBRAICALLY IF WE FLIP EACH PAIR?
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("ALGEBRAIC IMPACT OF FLIPPING EACH PAIR")
print("=" * 70)

kw_metrics = compute_all_metrics(KW_O)
print(f"\nKW baseline: χ²={kw_metrics['chi2']:.3f}, asym={kw_metrics['asym']}, "
      f"m={kw_metrics['m_score']}/16, kac={kw_metrics['kac']:.4f}")

for k in test_pairs:
    # Flip this pair
    flipped = list(KW_O)
    flipped[k] = 1 - flipped[k]
    
    name_a = KING_WEN[2*k][1]
    name_b = KING_WEN[2*k+1][1]
    
    # Check S2 validity
    from infra import is_s2_free
    s2_ok = is_s2_free(flipped)
    
    if s2_ok:
        flip_metrics = compute_all_metrics(flipped)
        d_chi2 = flip_metrics['chi2'] - kw_metrics['chi2']
        d_asym = flip_metrics['asym'] - kw_metrics['asym']
        d_m = flip_metrics['m_score'] - kw_metrics['m_score']
        d_kac = flip_metrics['kac'] - kw_metrics['kac']
        
        print(f"\n  Flip pair {k+1} ({name_a}/{name_b}):")
        print(f"    S2-free: {s2_ok}")
        print(f"    New: χ²={flip_metrics['chi2']:.3f} (Δ={d_chi2:+.3f}), "
              f"asym={flip_metrics['asym']} (Δ={d_asym:+d}), "
              f"m={flip_metrics['m_score']}/16 (Δ={d_m:+d}), "
              f"kac={flip_metrics['kac']:.4f} (Δ={d_kac:+.4f})")
        
        # Pareto comparison
        better = []
        worse = []
        if d_chi2 < -0.001: better.append('χ²')
        elif d_chi2 > 0.001: worse.append('χ²')
        if d_asym > 0: better.append('asym')
        elif d_asym < 0: worse.append('asym')
        if d_m > 0: better.append('m')
        elif d_m < 0: worse.append('m')
        if d_kac < -0.001: better.append('kac')
        elif d_kac > 0.001: worse.append('kac')
        
        print(f"    Better on: {better if better else 'none'}")
        print(f"    Worse on: {worse if worse else 'none'}")
        
        if better and not worse:
            print(f"    → DOMINATES KW (meaning reversal improves algebra!)")
        elif worse and not better:
            print(f"    → DOMINATED BY KW (meaning reversal degrades algebra)")
        elif better and worse:
            print(f"    → TRADE-OFF (meaning reversal changes algebra in both directions)")
        else:
            print(f"    → EQUAL (no algebraic difference)")
    else:
        print(f"\n  Flip pair {k+1} ({name_a}/{name_b}):")
        print(f"    S2-free: {s2_ok}")
        print(f"    → FLIP IS S2-FORBIDDEN (orientation is structurally forced)")
        
        # For S2-constrained pairs, check if it's constrained with neighbor
        for ck, forbidden in CONSTRAINTS.items():
            if k == ck or k == ck + 1:
                print(f"    Constraint at bridge {ck}: forbidden combos = {forbidden}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. S2 CONSTRAINT CHECK FOR PAIR 27
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("S2 CONSTRAINT DETAIL FOR PAIR 27 (Jian/Gui Mei)")
print("=" * 70)

k = 26  # pair 27, 0-indexed
a = PAIRS[k]['a']
b = PAIRS[k]['b']
print(f"\nPair 27: Jian (#{KING_WEN[2*k][0]}) bits={''.join(map(str,a))}")
print(f"         Gui Mei (#{KING_WEN[2*k+1][0]}) bits={''.join(map(str,b))}")

# Check both orientations with neighbors
for k_check in [k-1, k]:
    if k_check in CONSTRAINTS:
        print(f"\n  Bridge B{k_check+1} (between pair {k_check+1} and {k_check+2}):")
        print(f"    Forbidden: {CONSTRAINTS[k_check]}")
        print(f"    KW orientation: ({KW_O[k_check]}, {KW_O[k_check+1]})")
        is_forbidden = (KW_O[k_check], KW_O[k_check+1]) in CONSTRAINTS[k_check]
        print(f"    KW in forbidden set? {is_forbidden}")

# Check if pair 27 can be independently flipped
print(f"\n  Can pair 27 be independently flipped?")
flipped = list(KW_O)
flipped[26] = 1 - flipped[26]
print(f"    KW orientation at pair 27: {KW_O[26]}")
print(f"    Flipped: {flipped[26]}")
print(f"    S2-free after flip: {is_s2_free(flipped)}")

# If not, what about flipping with its constrained neighbor?
if not is_s2_free(flipped):
    # Try flipping pair 27 and its constrained neighbor
    for neighbor in [25, 27]:
        if neighbor < 32:
            flipped2 = list(KW_O)
            flipped2[26] = 1 - flipped2[26]
            flipped2[neighbor] = 1 - flipped2[neighbor]
            ok = is_s2_free(flipped2)
            if ok:
                metrics2 = compute_all_metrics(flipped2)
                print(f"\n  Flipping pair 27 + pair {neighbor+1} together: S2-free={ok}")
                print(f"    New metrics: χ²={metrics2['chi2']:.3f}, asym={metrics2['asym']}, "
                      f"m={metrics2['m_score']}/16, kac={metrics2['kac']:.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. THE MEANING-CONSTRAINT SPECTRUM
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("THE MEANING-CONSTRAINT SPECTRUM")
print("=" * 70)

print("""
The reader's Round 4 assessment establishes a spectrum of meaning-constraint:

STRONG (reversal clearly inferior, ~21 pairs):
  Meaning overdetermines the ordering. Reversal violates the Yijing's
  developmental grammar. Multiple independent textual signals converge.
  Example: Jin→Ming Yi (advance → injury is causal; injury → advance is not)

MODERATE (reversal weaker but defensible, ~11 pairs):
  Meaning prefers KW but doesn't absolutely require it. The pair is more
  contrastive than developmental. Alternative developmental logic exists.
  Example: Jian→Gui Mei (proper → improper is conventional; 
           improper → correction is also coherent)

ZERO pairs where reversal is equally good or better.

This maps to a meaning-constraint function across the 32 pairs:
""")

# Build the constraint spectrum
# Clear = strong constraint, Suggestive = moderate
all_pairs_info = {
    0:  'Clear', 1:  'Clear', 2:  'Suggestive', 3:  'Clear', 4:  'Suggestive',
    5:  'Clear', 6:  'Clear', 7:  'Clear', 8:  'Clear', 9:  'Clear',
    10: 'Suggestive', 11: 'Clear', 12: 'Suggestive', 13: 'Suggestive', 14: 'Suggestive',
    15: 'Clear', 16: 'Suggestive', 17: 'Clear', 18: 'Clear', 19: 'Clear',
    20: 'Clear', 21: 'Clear', 22: 'Clear', 23: 'Suggestive', 24: 'Clear',
    25: 'Clear', 26: 'Suggestive', 27: 'Clear', 28: 'Suggestive', 29: 'Clear',
    30: 'Suggestive', 31: 'Clear'
}

strong = sum(1 for v in all_pairs_info.values() if v == 'Clear')
moderate = sum(1 for v in all_pairs_info.values() if v == 'Suggestive')

print(f"  Strong constraint (Clear): {strong}/32 pairs")
print(f"  Moderate constraint (Suggestive): {moderate}/32 pairs")
print(f"  No constraint (Silent/Contradictory): 0/32 pairs")

# Cross-reference: are the S2-constrained pairs disproportionately Suggestive?
s2_sugg = sum(1 for k in CONSTRAINED_PAIRS if all_pairs_info[k] == 'Suggestive')
s2_clear = sum(1 for k in CONSTRAINED_PAIRS if all_pairs_info[k] == 'Clear')
free_sugg = moderate - s2_sugg
free_clear = strong - s2_clear

print(f"\n  Cross-reference with S2 constraints:")
print(f"    S2-constrained pairs: {s2_clear} Clear, {s2_sugg} Suggestive "
      f"({s2_sugg}/{len(CONSTRAINED_PAIRS)} = {100*s2_sugg/len(CONSTRAINED_PAIRS):.0f}% Suggestive)")
print(f"    Free pairs: {free_clear} Clear, {free_sugg} Suggestive "
      f"({free_sugg}/{32-len(CONSTRAINED_PAIRS)} = {100*free_sugg/(32-len(CONSTRAINED_PAIRS)):.0f}% Suggestive)")

# Cross-reference: are complement pairs disproportionately Suggestive?
comp_pairs = []
for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    if all(a[i] != b[i] for i in range(6)):
        comp_pairs.append(k)

comp_sugg = sum(1 for k in comp_pairs if all_pairs_info[k] == 'Suggestive')
comp_clear = sum(1 for k in comp_pairs if all_pairs_info[k] == 'Clear')
inv_sugg = moderate - comp_sugg
inv_clear = strong - comp_clear

print(f"\n  Cross-reference with pair type:")
print(f"    Complement pairs: {comp_clear} Clear, {comp_sugg} Suggestive "
      f"({comp_sugg}/{len(comp_pairs)} = {100*comp_sugg/len(comp_pairs):.0f}% Suggestive)")
print(f"    Inversion pairs: {inv_clear} Clear, {inv_sugg} Suggestive "
      f"({inv_sugg}/{32-len(comp_pairs)} = {100*inv_sugg/(32-len(comp_pairs)):.0f}% Suggestive)")

# ═══════════════════════════════════════════════════════════════════════════
# 5. KEY QUESTION: DOES ALGEBRAIC CONSTRAINT TRACK MEANING CONSTRAINT?
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("DOES ALGEBRAIC CONSTRAINT TRACK MEANING CONSTRAINT?")
print("=" * 70)

print("""
The fragility map (iter4) classified each bit as either:
  KW-dominates (flipping makes all 4 axes worse) — 11 bits
  Trade-off (flipping improves some axes, degrades others) — 16 bits

Do the "KW-dominates" bits correspond to meaning-Clear pairs?
Do the "trade-off" bits correspond to meaning-Suggestive pairs?
""")

# From iter4 findings: KW-dominates bits (0-indexed free bit): 0,1,2,4,7,8,13,18,19,22,25
# These map to pairs. Free bits 0-21 are Type A (single pair each).
# Need to map free bit → pair index

from infra import free_bits, FREE_PAIRS, COMPONENTS

kw_dom_bits = [0, 1, 2, 4, 7, 8, 13, 18, 19, 22, 25]
tradeoff_bits = [i for i in range(27) if i not in kw_dom_bits]

print("  Free bit → Pair mapping (Type A bits):")
kw_dom_pairs = set()
tradeoff_pairs = set()
for fb in free_bits:
    bit_idx = fb['bit_index']
    pair_list = fb['pairs']
    
    if bit_idx in kw_dom_bits:
        for p in pair_list:
            kw_dom_pairs.add(p)
    else:
        for p in pair_list:
            tradeoff_pairs.add(p)

# Some pairs appear in both if they have multiple bits (components)
both = kw_dom_pairs & tradeoff_pairs

print(f"\n  KW-dominates pairs: {sorted([p+1 for p in kw_dom_pairs])}")
print(f"  Trade-off pairs: {sorted([p+1 for p in tradeoff_pairs])}")
print(f"  In both: {sorted([p+1 for p in both])}")

# Cross-tabulate with meaning confidence
print("\n  Cross-tabulation:")
kd_clear = sum(1 for p in kw_dom_pairs if all_pairs_info[p] == 'Clear')
kd_sugg = sum(1 for p in kw_dom_pairs if all_pairs_info[p] == 'Suggestive')
to_clear = sum(1 for p in tradeoff_pairs if all_pairs_info[p] == 'Clear')
to_sugg = sum(1 for p in tradeoff_pairs if all_pairs_info[p] == 'Suggestive')
print(f"    KW-dominates: {kd_clear} Clear, {kd_sugg} Suggestive")
print(f"    Trade-off: {to_clear} Clear, {to_sugg} Suggestive")
if kw_dom_pairs:
    print(f"    KW-dom Suggestive rate: {kd_sugg}/{len(kw_dom_pairs)} = {100*kd_sugg/len(kw_dom_pairs):.0f}%")
if tradeoff_pairs:
    print(f"    Trade-off Suggestive rate: {to_sugg}/{len(tradeoff_pairs)} = {100*to_sugg/len(tradeoff_pairs):.0f}%")
