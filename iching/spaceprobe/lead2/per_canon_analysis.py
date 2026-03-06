"""
Lead 2: Per-canon distribution of developmental priority and algebra↔meaning complementarity.

Questions:
1. How does meaning confidence (Clear/Suggestive) distribute across canons?
2. Does the algebra↔meaning inverse correlation hold per-canon?
3. Do dominators preferentially violate Lower Canon pairs?

Context: The sequence investigation found Upper Canon is structurally extreme
on kernel metrics; Lower Canon is structurally generic. If meaning organizes
the Lower Canon while algebra organizes the Upper, we should see:
- Meaning confidence roughly uniform (or stronger in Lower Canon)
- Algebraic fragility concentrated in Upper Canon
- Dominator violations concentrated in Lower Canon
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/logoswen/iter5')

from sequence import KING_WEN
from infra import (PAIRS, N_PAIRS, FREE_PAIRS, COMPONENTS, COMPONENT_VALID,
                   CONSTRAINED_PAIRS, free_bits, KW_O, compute_all_metrics,
                   is_s2_free, M_DECISIVE)

# ══════════════════════════════════════════════════════════════════════════════
# DATA: Reader assessments (from iter6 comparator_round3.py)
# ══════════════════════════════════════════════════════════════════════════════

PAIRS_DATA = {
    0:  {'conf': 'Clear',      'logic': 'Cosmological primacy'},
    1:  {'conf': 'Clear',      'logic': 'Birth→Education'},
    2:  {'conf': 'Suggestive', 'logic': 'Need→Conflict'},
    3:  {'conf': 'Clear',      'logic': 'Mobilization→Union'},
    4:  {'conf': 'Suggestive', 'logic': 'Restraint→Conduct'},
    5:  {'conf': 'Clear',      'logic': 'Flourishing→Decline'},
    6:  {'conf': 'Clear',      'logic': 'Fellowship→Abundance'},
    7:  {'conf': 'Clear',      'logic': 'Modesty→Enthusiasm'},
    8:  {'conf': 'Clear',      'logic': 'Following→Decay'},
    9:  {'conf': 'Clear',      'logic': 'Approach→Contemplation'},
    10: {'conf': 'Suggestive', 'logic': 'Justice→Adornment'},
    11: {'conf': 'Clear',      'logic': 'Dissolution→Return'},
    12: {'conf': 'Suggestive', 'logic': 'Innocence→Accumulation'},
    13: {'conf': 'Suggestive', 'logic': 'Nourishment→Excess'},
    14: {'conf': 'Suggestive', 'logic': 'Danger→Clarity'},
    # --- canon boundary (pair 15 = hex 31-32 = start of lower) ---
    15: {'conf': 'Clear',      'logic': 'Attraction→Duration'},
    16: {'conf': 'Suggestive', 'logic': 'Retreat→Power'},
    17: {'conf': 'Clear',      'logic': 'Progress→Darkening'},
    18: {'conf': 'Clear',      'logic': 'Family→Opposition'},
    19: {'conf': 'Clear',      'logic': 'Obstruction→Deliverance'},
    20: {'conf': 'Clear',      'logic': 'Decrease→Increase'},
    21: {'conf': 'Clear',      'logic': 'Breakthrough→Encounter'},
    22: {'conf': 'Clear',      'logic': 'Gathering→Rising'},
    23: {'conf': 'Suggestive', 'logic': 'Oppression→Source'},
    24: {'conf': 'Clear',      'logic': 'Revolution→Cauldron'},
    25: {'conf': 'Clear',      'logic': 'Movement→Stillness'},
    26: {'conf': 'Suggestive', 'logic': 'Gradual→Hasty'},
    27: {'conf': 'Clear',      'logic': 'Abundance→Wandering'},
    28: {'conf': 'Suggestive', 'logic': 'Penetrating→Joyous'},
    29: {'conf': 'Clear',      'logic': 'Dispersion→Limitation'},
    30: {'conf': 'Suggestive', 'logic': 'Inner Truth→Small Acts'},
    31: {'conf': 'Clear',      'logic': 'Completion→Incompletion'},
}

# S2-constrained pairs (from infra.py)
S2_PAIRS = CONSTRAINED_PAIRS

# Free bit fragility data from iter4: KW-dominates bits
KW_DOM_BITS = {0, 1, 2, 4, 7, 8, 13, 18, 19, 22, 25}
TRADEOFF_BITS = set(range(27)) - KW_DOM_BITS

# Dominator data (from dominator_meaning_check.py)
DOMINATORS = [
    {17, 26}, {9, 10, 16, 17}, {9, 17, 23, 24},
    {0, 6, 9, 17, 23}, {6, 9, 15, 17, 23}, {9, 10, 16, 17, 23},
    {9, 11, 17, 23, 24}, {9, 15, 17, 20, 23}, {9, 15, 17, 21, 23},
    {9, 10, 11, 16, 17, 26}, {9, 11, 15, 17, 23, 24}, {9, 11, 17, 23, 24, 26},
]

UPPER_CANON = range(0, 15)   # pairs 0-14 (hex 1-30)
LOWER_CANON = range(15, 32)  # pairs 15-31 (hex 31-64)


def free_bits_to_pairs(fb_set):
    """Convert free bit indices to pair indices."""
    pairs = set()
    for fb in fb_set:
        for p in free_bits[fb]['pairs']:
            pairs.add(p)
    return pairs


# ══════════════════════════════════════════════════════════════════════════════
# 1. MEANING CONFIDENCE PER CANON
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. DEVELOPMENTAL PRIORITY: CONFIDENCE PER CANON")
print("=" * 70)

for canon_name, canon_range in [("Upper Canon (pairs 0-14)", UPPER_CANON),
                                  ("Lower Canon (pairs 15-31)", LOWER_CANON)]:
    clear = [k for k in canon_range if PAIRS_DATA[k]['conf'] == 'Clear']
    sugg  = [k for k in canon_range if PAIRS_DATA[k]['conf'] == 'Suggestive']
    total = len(list(canon_range))
    print(f"\n  {canon_name}: {len(clear)} Clear, {len(sugg)} Suggestive (of {total})")
    print(f"    Clear rate: {100*len(clear)/total:.0f}%")
    print(f"    Clear pairs: {[k for k in clear]}")
    print(f"    Suggestive pairs: {[k for k in sugg]}")

# Also check S2 overlap per canon
print("\n  S2-constrained pairs per canon:")
s2_upper = [k for k in UPPER_CANON if k in S2_PAIRS]
s2_lower = [k for k in LOWER_CANON if k in S2_PAIRS]
print(f"    Upper: {s2_upper} ({len(s2_upper)} pairs)")
print(f"    Lower: {s2_lower} ({len(s2_lower)} pairs)")

# Key: are suggestive pairs correlated with S2 constraints?
print("\n  Suggestive ∩ S2 per canon:")
for canon_name, canon_range in [("Upper", UPPER_CANON), ("Lower", LOWER_CANON)]:
    sugg_s2 = [k for k in canon_range if PAIRS_DATA[k]['conf'] == 'Suggestive' and k in S2_PAIRS]
    sugg_free = [k for k in canon_range if PAIRS_DATA[k]['conf'] == 'Suggestive' and k not in S2_PAIRS]
    print(f"    {canon_name}: {len(sugg_s2)} Suggestive+S2, {len(sugg_free)} Suggestive+Free")

# ══════════════════════════════════════════════════════════════════════════════
# 2. ALGEBRAIC FRAGILITY PER CANON
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("2. ALGEBRAIC FRAGILITY PER CANON")
print("=" * 70)

# Map free bits to pairs, classify per canon
dom_pairs = free_bits_to_pairs(KW_DOM_BITS)
trade_pairs = free_bits_to_pairs(TRADEOFF_BITS)

print(f"\n  KW-dominates pairs (all 4 axes degrade on flip): {sorted(dom_pairs)}")
print(f"  Trade-off pairs (some improve, some degrade): {sorted(trade_pairs)}")

for canon_name, canon_range in [("Upper Canon", UPPER_CANON), ("Lower Canon", LOWER_CANON)]:
    canon_set = set(canon_range)
    dom_in = dom_pairs & canon_set
    trade_in = trade_pairs & canon_set
    both_in = dom_in & trade_in  # pairs with multiple free bits
    print(f"\n  {canon_name}:")
    print(f"    KW-dominates: {sorted(dom_in)} ({len(dom_in)} pairs)")
    print(f"    Trade-off: {sorted(trade_in)} ({len(trade_in)} pairs)")
    print(f"    In both: {sorted(both_in)}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. ALGEBRA↔MEANING CROSS-TAB PER CANON
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("3. ALGEBRA↔MEANING COMPLEMENTARITY PER CANON")
print("=" * 70)

# For each pair, classify as {dom, trade, both, neither(S2)} × {Clear, Suggestive}
for canon_name, canon_range in [("Upper Canon", UPPER_CANON), ("Lower Canon", LOWER_CANON)]:
    canon_set = set(canon_range)
    
    # Pairs with any free bit
    active_pairs = (dom_pairs | trade_pairs) & canon_set
    s2_only = canon_set - active_pairs
    
    dom_only = (dom_pairs - trade_pairs) & canon_set
    trade_only = (trade_pairs - dom_pairs) & canon_set
    both = (dom_pairs & trade_pairs) & canon_set
    
    print(f"\n  {canon_name}:")
    print(f"    S2-constrained (no free bits): {sorted(s2_only)}")
    
    # Cross-tab: fragility class × confidence
    for cat_name, cat_set in [("KW-dominates only", dom_only),
                                ("Trade-off only", trade_only),
                                ("Both (mixed)", both),
                                ("S2-constrained", s2_only)]:
        clear = sum(1 for p in cat_set if PAIRS_DATA[p]['conf'] == 'Clear')
        sugg = sum(1 for p in cat_set if PAIRS_DATA[p]['conf'] == 'Suggestive')
        total = len(cat_set)
        if total > 0:
            print(f"    {cat_name}: {clear} Clear, {sugg} Suggestive "
                  f"({100*sugg/total:.0f}% Suggestive) [n={total}]")

# ══════════════════════════════════════════════════════════════════════════════
# 4. DOMINATOR VIOLATIONS PER CANON
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("4. DOMINATOR VIOLATIONS PER CANON")
print("=" * 70)

from collections import Counter

pair_violation_count = Counter()
for dom in DOMINATORS:
    pairs_flipped = free_bits_to_pairs(dom)
    for p in pairs_flipped:
        pair_violation_count[p] += 1

upper_violations = {p: c for p, c in pair_violation_count.items() if p in set(UPPER_CANON)}
lower_violations = {p: c for p, c in pair_violation_count.items() if p in set(LOWER_CANON)}

print(f"\n  Upper Canon pairs flipped by dominators:")
for p in sorted(upper_violations.keys()):
    d = PAIRS_DATA[p]
    names = f"{KING_WEN[2*p][1]}/{KING_WEN[2*p+1][1]}"
    print(f"    Pair {p:2d} ({names:25s}): {upper_violations[p]:2d}/12 dominators  [{d['conf']}]")

print(f"\n  Lower Canon pairs flipped by dominators:")
for p in sorted(lower_violations.keys()):
    d = PAIRS_DATA[p]
    names = f"{KING_WEN[2*p][1]}/{KING_WEN[2*p+1][1]}"
    print(f"    Pair {p:2d} ({names:25s}): {lower_violations[p]:2d}/12 dominators  [{d['conf']}]")

total_upper = sum(upper_violations.values())
total_lower = sum(lower_violations.values())
total_all = total_upper + total_lower
print(f"\n  Total pair-reversals across 12 dominators: {total_all}")
print(f"    Upper Canon: {total_upper} ({100*total_upper/total_all:.0f}%)")
print(f"    Lower Canon: {total_lower} ({100*total_lower/total_all:.0f}%)")

# Per-dominator: how many upper vs lower violations?
print(f"\n  Per-dominator canon distribution:")
for i, dom in enumerate(DOMINATORS):
    pairs_flipped = free_bits_to_pairs(dom)
    upper = [p for p in pairs_flipped if p in set(UPPER_CANON)]
    lower = [p for p in pairs_flipped if p in set(LOWER_CANON)]
    upper_clear = sum(1 for p in upper if PAIRS_DATA[p]['conf'] == 'Clear')
    lower_clear = sum(1 for p in lower if PAIRS_DATA[p]['conf'] == 'Clear')
    print(f"    Dom {i+1:2d}: {len(upper)} upper ({upper_clear} Clear), "
          f"{len(lower)} lower ({lower_clear} Clear)")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE KEY TEST: Per-bit fragility × confidence × canon
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("5. COMPLETE FREE-BIT MAP: FRAGILITY × CONFIDENCE × CANON")
print("=" * 70)

kw_metrics = compute_all_metrics(KW_O)

print(f"\n  KW baseline: χ²={kw_metrics['chi2']:.3f}, asym={kw_metrics['asym']}, "
      f"m={kw_metrics['m_score']}/16, kac={kw_metrics['kac']:.4f}")

print(f"\n  {'Bit':>3s}  {'Type':>4s}  {'Pairs':>8s}  {'Canon':>6s}  {'Conf':>10s}  "
      f"{'Δχ²':>8s}  {'Δasym':>6s}  {'Δm':>4s}  {'Δkac':>8s}  {'Fragility':>10s}")

for fb in free_bits:
    bit_idx = fb['bit_index']
    pairs = fb['pairs']
    
    # Build flipped orientation
    flipped = list(KW_O)
    if fb['type'] == 'A':
        flipped[pairs[0]] = 1 - flipped[pairs[0]]
    else:
        # Component: flip both together (pick valid alternative)
        p1, p2 = pairs
        valid = fb['valid_states']
        current = (KW_O[p1], KW_O[p2])
        alt = [v for v in valid if v != current]
        if alt:
            flipped[p1], flipped[p2] = alt[0]
        else:
            continue
    
    if not is_s2_free(flipped):
        continue
    
    flip_metrics = compute_all_metrics(flipped)
    d_chi2 = flip_metrics['chi2'] - kw_metrics['chi2']
    d_asym = flip_metrics['asym'] - kw_metrics['asym']
    d_m = flip_metrics['m_score'] - kw_metrics['m_score']
    d_kac = flip_metrics['kac'] - kw_metrics['kac']
    
    # Classify fragility
    better = worse = 0
    if d_chi2 < -0.001: better += 1
    elif d_chi2 > 0.001: worse += 1
    if d_asym > 0: better += 1
    elif d_asym < 0: worse += 1
    if d_m > 0: better += 1
    elif d_m < 0: worse += 1
    if d_kac < -0.001: better += 1
    elif d_kac > 0.001: worse += 1
    
    if better == 0 and worse > 0: frag = "KW-dom"
    elif better > 0 and worse == 0: frag = "IMPROVES"
    elif better > 0 and worse > 0: frag = "trade-off"
    else: frag = "neutral"
    
    # Canon of the affected pair(s)
    canon = "upper" if all(p < 15 for p in pairs) else "lower" if all(p >= 15 for p in pairs) else "cross"
    
    # Confidence of the affected pair(s)
    confs = [PAIRS_DATA[p]['conf'] for p in pairs]
    conf_str = '/'.join(confs)
    
    pair_str = ','.join(str(p) for p in pairs)
    
    print(f"  {bit_idx:3d}  {fb['type']:>4s}  {pair_str:>8s}  {canon:>6s}  {conf_str:>10s}  "
          f"{d_chi2:>+8.3f}  {d_asym:>+6d}  {d_m:>+4d}  {d_kac:>+8.4f}  {frag:>10s}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("6. SUMMARY")
print("=" * 70)

upper_clear = sum(1 for k in UPPER_CANON if PAIRS_DATA[k]['conf'] == 'Clear')
upper_sugg = sum(1 for k in UPPER_CANON if PAIRS_DATA[k]['conf'] == 'Suggestive')
lower_clear = sum(1 for k in LOWER_CANON if PAIRS_DATA[k]['conf'] == 'Clear')
lower_sugg = sum(1 for k in LOWER_CANON if PAIRS_DATA[k]['conf'] == 'Suggestive')

print(f"""
  MEANING CONFIDENCE:
    Upper Canon: {upper_clear} Clear, {upper_sugg} Suggestive ({100*upper_clear/15:.0f}% Clear)
    Lower Canon: {lower_clear} Clear, {lower_sugg} Suggestive ({100*lower_clear/17:.0f}% Clear)

  QUESTION: Does meaning concentrate in the structurally silent canon?
    If Upper ≈ Lower on meaning: meaning is uniform, not compensatory
    If Lower > Upper on meaning: meaning fills the gap algebra leaves
    If Upper > Lower on meaning: meaning tracks algebra (same canon structured)

  DOMINATOR VIOLATIONS:
    Upper Canon reversals: {total_upper} ({100*total_upper/total_all:.0f}%)
    Lower Canon reversals: {total_lower} ({100*total_lower/total_all:.0f}%)

  QUESTION: Does developmental priority protect the structurally silent canon?
    If Lower >> Upper: dominators attack Lower, meaning defends it
    If Upper >> Lower: dominators attack Upper, algebra defends it
    If ≈ equal: no canon-level pattern
""")
