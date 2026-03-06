"""
Thread F: Trigram Orientation Analysis

For each hexagram: lower trigram = L1,L2,L3; upper trigram = L4,L5,L6.
For inversion pairs (b = reverse(a)):
  lower_b = reverse(upper_a), upper_b = reverse(lower_a)
Orientation determines which trigram configuration is presented first.

This script:
1. For each pair, which upper/lower trigram configuration comes first?
2. Upper and lower trigram trajectories (64 steps) — orientation dependence
3. Nuclear trigrams (lines 2-3-4 and 3-4-5): orientation patterns
4. Preferred positions for specific trigrams (Heaven, Earth, Water, Fire)
5. Trigram-level rules that might recover KW orientation
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits, TRIGRAMS
import random
import numpy as np
import math

DIMS = 6
N_PAIRS = 32
M = [tuple(b) for b in all_bits()]

# ── Trigram constants ─────────────────────────────────────────────────────────

TRIGRAM_NAMES = {
    (1,1,1): 'Heaven', (0,0,0): 'Earth',
    (0,1,0): 'Water',  (1,0,1): 'Fire',
    (1,0,0): 'Thunder',(0,1,1): 'Wind',
    (0,0,1): 'Mountain',(1,1,0): 'Lake',
}

def lower_tri(h):
    """Lower trigram (L1,L2,L3) as tuple."""
    return h[:3]

def upper_tri(h):
    """Upper trigram (L4,L5,L6) as tuple."""
    return h[3:]

def nuclear_lower(h):
    """Lower nuclear trigram: lines 2,3,4."""
    return (h[1], h[2], h[3])

def nuclear_upper(h):
    """Upper nuclear trigram: lines 3,4,5."""
    return (h[2], h[3], h[4])

def reverse_tri(t):
    """Reverse a 3-bit trigram."""
    return (t[2], t[1], t[0])

def complement_tri(t):
    """Complement a 3-bit trigram."""
    return (1-t[0], 1-t[1], 1-t[2])

def reverse_hex(h):
    """Reverse a 6-bit hexagram (read upside-down)."""
    return tuple(h[5-i] for i in range(6))

def is_palindrome(h):
    return h == reverse_hex(h)

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def tri_name(t):
    return TRIGRAM_NAMES.get(t, '?')

def tri_str(t):
    return ''.join(map(str, t))


# ── Build pairs ───────────────────────────────────────────────────────────────

PAIRS = []
for k in range(N_PAIRS):
    a = M[2*k]
    b = M[2*k+1]
    is_inv = (reverse_hex(a) == b)
    is_comp = (not is_inv) and is_palindrome(a) and is_palindrome(b)
    PAIRS.append({
        'idx': k, 'a': a, 'b': b,
        'name_a': KING_WEN[2*k][1], 'name_b': KING_WEN[2*k+1][1],
        'sig': xor_sig(a),
        'is_inv': is_inv, 'is_comp': is_comp,
    })


# ═══════════════════════════════════════════════════════════════════════════════
# 1. TRIGRAM SWAP UNDER INVERSION
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("1. TRIGRAM CONFIGURATION PER PAIR")
print("   For inversion pairs: b = reverse(a)")
print("   lower_b = reverse(upper_a), upper_b = reverse(lower_a)")
print("=" * 80)
print()

print(f"  {'Pair':>4s}  {'Type':>5s}  {'Lo_A':>8s} {'Up_A':>8s}  {'Lo_B':>8s} {'Up_B':>8s}  "
      f"{'Rev check':>10s}  Names")
print("-" * 100)

inv_verified = 0
for p in PAIRS:
    a, b = p['a'], p['b']
    la, ua = lower_tri(a), upper_tri(a)
    lb, ub = lower_tri(b), upper_tri(b)
    
    # Verify reversal relationship for inversion pairs
    if p['is_inv']:
        rev_ok = (lb == reverse_tri(ua) and ub == reverse_tri(la))
        check = '✓' if rev_ok else '✗'
        if rev_ok:
            inv_verified += 1
        ptype = 'inv'
    elif p['is_comp']:
        comp_ok = (lb == complement_tri(la) and ub == complement_tri(ua))
        check = '✓c' if comp_ok else '✗c'
        ptype = 'comp'
    else:
        check = '?'
        ptype = '?'
    
    print(f"  {p['idx']+1:4d}  {ptype:>5s}  "
          f"{tri_name(la):>8s} {tri_name(ua):>8s}  "
          f"{tri_name(lb):>8s} {tri_name(ub):>8s}  "
          f"{check:>10s}  {p['name_a']}-{p['name_b']}")

print(f"\n  Inversion relationship verified: {inv_verified}/{sum(1 for p in PAIRS if p['is_inv'])}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. TRIGRAM TRAJECTORIES (64 STEPS)
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("2. TRIGRAM TRAJECTORIES (64 hexagrams)")
print("=" * 80)
print()

# Build full trajectories
lower_traj = [lower_tri(M[i]) for i in range(64)]
upper_traj = [upper_tri(M[i]) for i in range(64)]
nuc_lower_traj = [nuclear_lower(M[i]) for i in range(64)]
nuc_upper_traj = [nuclear_upper(M[i]) for i in range(64)]

# Trigram frequency in each position (lower/upper)
lower_freq = Counter(lower_traj)
upper_freq = Counter(upper_traj)
print("  Lower trigram frequency (64 positions):")
for t in sorted(TRIGRAM_NAMES.keys()):
    print(f"    {tri_name(t):>8s} {tri_str(t)}: {lower_freq[t]}")

print("\n  Upper trigram frequency (64 positions):")
for t in sorted(TRIGRAM_NAMES.keys()):
    print(f"    {tri_name(t):>8s} {tri_str(t)}: {upper_freq[t]}")

# Check: each trigram appears exactly 8 times as lower and 8 as upper
lower_balanced = all(v == 8 for v in lower_freq.values())
upper_balanced = all(v == 8 for v in upper_freq.values())
print(f"\n  Lower balanced (all 8×)? {lower_balanced}")
print(f"  Upper balanced (all 8×)? {upper_balanced}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. WITHIN-PAIR TRIGRAM PATTERNS: WHICH TRIGRAM COMES FIRST?
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("3. TRIGRAM POSITION PREFERENCES")
print("   For each trigram: how often does it appear as LOWER in the FIRST hexagram?")
print("=" * 80)
print()

# For first hexagram of each pair
first_lower = [lower_tri(PAIRS[k]['a']) for k in range(N_PAIRS)]
first_upper = [upper_tri(PAIRS[k]['a']) for k in range(N_PAIRS)]
second_lower = [lower_tri(PAIRS[k]['b']) for k in range(N_PAIRS)]
second_upper = [upper_tri(PAIRS[k]['b']) for k in range(N_PAIRS)]

# Count: how often is each trigram in position "first-lower" vs "second-lower"?
first_lower_freq = Counter(first_lower)
second_lower_freq = Counter(second_lower)
first_upper_freq = Counter(first_upper)
second_upper_freq = Counter(second_upper)

print("  Lower trigram: first vs second hexagram of each pair")
print(f"  {'Trigram':>8s}  {'1st hex':>7s}  {'2nd hex':>7s}  {'Ratio':>6s}")
for t in sorted(TRIGRAM_NAMES.keys()):
    f = first_lower_freq.get(t, 0)
    s = second_lower_freq.get(t, 0)
    total = f + s
    ratio = f / total if total > 0 else 0
    print(f"  {tri_name(t):>8s}  {f:7d}  {s:7d}  {ratio:6.3f}")

print("\n  Upper trigram: first vs second hexagram of each pair")
print(f"  {'Trigram':>8s}  {'1st hex':>7s}  {'2nd hex':>7s}  {'Ratio':>6s}")
for t in sorted(TRIGRAM_NAMES.keys()):
    f = first_upper_freq.get(t, 0)
    s = second_upper_freq.get(t, 0)
    total = f + s
    ratio = f / total if total > 0 else 0
    print(f"  {tri_name(t):>8s}  {f:7d}  {s:7d}  {ratio:6.3f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. SPECIFIC TRIGRAMS: HEAVEN, EARTH, WATER, FIRE
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("4. KEY TRIGRAMS — PREFERRED POSITION (FIRST vs SECOND)")
print("=" * 80)
print()

KEY_TRIGRAMS = [(1,1,1), (0,0,0), (0,1,0), (1,0,1)]  # Heaven, Earth, Water, Fire

for tri in KEY_TRIGRAMS:
    name = tri_name(tri)
    print(f"  === {name} ({tri_str(tri)}) ===")
    
    # Find all pairs where this trigram appears
    appearances = []
    for p in PAIRS:
        a, b = p['a'], p['b']
        la, ua, lb, ub = lower_tri(a), upper_tri(a), lower_tri(b), upper_tri(b)
        
        for pos, tri_val in [('1st-lower', la), ('1st-upper', ua),
                              ('2nd-lower', lb), ('2nd-upper', ub)]:
            if tri_val == tri:
                appearances.append((p['idx']+1, pos, p['name_a'] if '1st' in pos else p['name_b']))
    
    first_count = sum(1 for _, pos, _ in appearances if '1st' in pos)
    second_count = sum(1 for _, pos, _ in appearances if '2nd' in pos)
    lower_count = sum(1 for _, pos, _ in appearances if 'lower' in pos)
    upper_count = sum(1 for _, pos, _ in appearances if 'upper' in pos)
    
    print(f"    Total appearances: {len(appearances)}")
    print(f"    In 1st hex: {first_count}  In 2nd hex: {second_count}")
    print(f"    As lower: {lower_count}  As upper: {upper_count}")
    
    for pair_idx, pos, hex_name in appearances:
        print(f"      Pair {pair_idx:2d}: {pos:>10s}  ({hex_name})")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. TRIGRAM-LEVEL RULES FOR RECOVERING ORIENTATION
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("5. TRIGRAM-LEVEL RULES FOR ORIENTATION")
print("   Test: does a trigram-based rule predict which hexagram comes first?")
print("=" * 80)
print()

# For inversion pairs only (complement pairs have different structure)
inv_pairs = [p for p in PAIRS if p['is_inv']]
comp_pairs = [p for p in PAIRS if p['is_comp']]

def test_rule(rule_fn, rule_name, pairs_to_test):
    """Test a binary rule: returns 1 if rule predicts first hex correctly."""
    correct = 0
    total = len(pairs_to_test)
    results = []
    for p in pairs_to_test:
        pred = rule_fn(p['a'], p['b'])
        results.append(pred)
        if pred == 1:  # rule says 'a' should be first — and it is
            correct += 1
    
    # Also test the complementary rule
    comp_correct = total - correct
    best = max(correct, comp_correct)
    return correct, total, best, results

# Rule 1: Lower trigram has higher binary value
def rule_lower_higher(a, b):
    la = lower_tri(a)
    lb = lower_tri(b)
    va = la[0]*4 + la[1]*2 + la[2]
    vb = lb[0]*4 + lb[1]*2 + lb[2]
    return 1 if va > vb else (0 if va < vb else -1)

# Rule 2: Upper trigram has higher binary value
def rule_upper_higher(a, b):
    ua = upper_tri(a)
    ub = upper_tri(b)
    va = ua[0]*4 + ua[1]*2 + ua[2]
    vb = ub[0]*4 + ub[1]*2 + ub[2]
    return 1 if va > vb else (0 if va < vb else -1)

# Rule 3: Lower trigram precedes upper in traditional order
# Traditional order: Heaven > Lake > Fire > Thunder > Wind > Water > Mountain > Earth
TRAD_ORDER = {(1,1,1): 7, (1,1,0): 6, (1,0,1): 5, (1,0,0): 4,
              (0,1,1): 3, (0,1,0): 2, (0,0,1): 1, (0,0,0): 0}

def rule_lower_trad_higher(a, b):
    la = lower_tri(a)
    lb = lower_tri(b)
    va = TRAD_ORDER.get(la, -1)
    vb = TRAD_ORDER.get(lb, -1)
    return 1 if va > vb else (0 if va < vb else -1)

# Rule 4: First hex has Heaven or Fire in some position
def rule_heaven_fire_lower(a, b):
    la = lower_tri(a)
    return 1 if la in [(1,1,1), (1,0,1)] else 0

# Rule 5: First hex lower trigram weight >= upper trigram weight
def rule_lower_heavier_than_upper(a, b):
    la_w = sum(lower_tri(a))
    ua_w = sum(upper_tri(a))
    return 1 if la_w >= ua_w else 0

# Rule 6: First hex has more yang in lower trigram (L1+L2+L3 of a vs b)
def rule_lower_yang(a, b):
    la_w = sum(lower_tri(a))
    lb_w = sum(lower_tri(b))
    return 1 if la_w > lb_w else (0 if la_w < lb_w else -1)

# Rule 7: Nuclear lower trigram (L2,L3,L4) has higher yang count
def rule_nuclear_lower_yang(a, b):
    na_w = sum(nuclear_lower(a))
    nb_w = sum(nuclear_lower(b))
    return 1 if na_w > nb_w else (0 if na_w < nb_w else -1)

# Rule 8: L1 of first hex is yang
def rule_L1_yang(a, b):
    return 1 if a[0] == 1 else 0

# Rule 9: L6 of first hex is yang
def rule_L6_yang(a, b):
    return 1 if a[5] == 1 else 0

# Rule 10: Lower trigram of first hex != upper trigram of first hex
# (asymmetric hexagram first)
def rule_asymmetric_trigrams(a, b):
    return 1 if lower_tri(a) != upper_tri(a) else 0

rules = [
    (rule_lower_higher, "Lower tri binary higher"),
    (rule_upper_higher, "Upper tri binary higher"),
    (rule_lower_trad_higher, "Lower tri trad order higher"),
    (rule_heaven_fire_lower, "Heaven/Fire in lower"),
    (rule_lower_heavier_than_upper, "Lower ≥ upper weight"),
    (rule_lower_yang, "Lower tri more yang"),
    (rule_nuclear_lower_yang, "Nuclear lower more yang"),
    (rule_L1_yang, "L1 is yang"),
    (rule_L6_yang, "L6 is yang"),
    (rule_asymmetric_trigrams, "Trigrams are different"),
]

# Test on inversion pairs
print(f"  Testing {len(rules)} rules on {len(inv_pairs)} inversion pairs:")
print(f"  {'Rule':>35s}  {'Match':>5s}  {'Best':>5s}  {'%':>6s}")
print(f"  {'-'*60}")

for rule_fn, rule_name in rules:
    correct, total, best, _ = test_rule(rule_fn, rule_name, inv_pairs)
    pct = 100 * best / total if total > 0 else 0
    print(f"  {rule_name:>35s}  {correct:>5d}/{total}  {best:>5d}/{total}  {pct:6.1f}%")

# Test on all pairs
print(f"\n  Testing on ALL {len(PAIRS)} pairs (including complement):")
print(f"  {'Rule':>35s}  {'Match':>5s}  {'Best':>5s}  {'%':>6s}")
print(f"  {'-'*60}")

for rule_fn, rule_name in rules:
    correct, total, best, _ = test_rule(rule_fn, rule_name, PAIRS)
    pct = 100 * best / total if total > 0 else 0
    print(f"  {rule_name:>35s}  {correct:>5d}/{total}  {best:>5d}/{total}  {pct:6.1f}%")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. TRIGRAM PAIR (LOWER, UPPER) TRAJECTORY
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("6. TRIGRAM PAIR TRAJECTORY — (lower, upper) at each position")
print("=" * 80)
print()

# Full 64-step trajectory
print("  Position  Lower     Upper     Hex name")
for i in range(64):
    h = M[i]
    lo = lower_tri(h)
    up = upper_tri(h)
    name = KING_WEN[i][1]
    pair_idx = i // 2
    pos_in_pair = 'A' if i % 2 == 0 else 'B'
    print(f"  {i+1:3d} (P{pair_idx+1:02d}{pos_in_pair})  "
          f"{tri_name(lo):>8s}  {tri_name(up):>8s}  {name}")

# Trigram pair (lower, upper) frequency
print(f"\n  (Lower, Upper) pair frequency:")
pair_freq = Counter((tri_name(lower_tri(M[i])), tri_name(upper_tri(M[i]))) 
                     for i in range(64))
for (lo, up), cnt in sorted(pair_freq.items(), key=lambda x: -x[1]):
    print(f"    ({lo:>8s}, {up:>8s}): {cnt}")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. NUCLEAR TRIGRAMS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("7. NUCLEAR TRIGRAMS — lines 2-3-4 (lower) and 3-4-5 (upper)")
print("=" * 80)
print()

# Nuclear trigram swap under inversion:
# If h = (L1,L2,L3,L4,L5,L6), reverse(h) = (L6,L5,L4,L3,L2,L1)
# nuclear_lower(h) = (L2,L3,L4), nuclear_lower(reverse(h)) = (L5,L4,L3)
# nuclear_upper(h) = (L3,L4,L5), nuclear_upper(reverse(h)) = (L4,L3,L2)
# So nuclear_lower(reverse(h)) = reverse(nuclear_upper(h))
# And nuclear_upper(reverse(h)) = reverse(nuclear_lower(h))

# Verify this
print("  Verify: nuclear_lower(reverse(h)) = reverse(nuclear_upper(h))")
verified = 0
total_checked = 0
for p in PAIRS:
    if p['is_inv']:
        a, b = p['a'], p['b']
        # b = reverse(a)
        check1 = nuclear_lower(b) == reverse_tri(nuclear_upper(a))
        check2 = nuclear_upper(b) == reverse_tri(nuclear_lower(a))
        if check1 and check2:
            verified += 1
        total_checked += 1
print(f"  Verified: {verified}/{total_checked}")

# Nuclear trigram frequencies in first vs second hex
print(f"\n  Nuclear lower trigram: 1st hex vs 2nd hex of each pair")
nuc_lo_first = Counter(nuclear_lower(PAIRS[k]['a']) for k in range(N_PAIRS))
nuc_lo_second = Counter(nuclear_lower(PAIRS[k]['b']) for k in range(N_PAIRS))

print(f"  {'Trigram':>8s}  {'1st hex':>7s}  {'2nd hex':>7s}  {'Delta':>5s}")
for t in sorted(TRIGRAM_NAMES.keys()):
    f = nuc_lo_first.get(t, 0)
    s = nuc_lo_second.get(t, 0)
    print(f"  {tri_name(t):>8s}  {f:7d}  {s:7d}  {f-s:>+5d}")

print(f"\n  Nuclear upper trigram: 1st hex vs 2nd hex of each pair")
nuc_up_first = Counter(nuclear_upper(PAIRS[k]['a']) for k in range(N_PAIRS))
nuc_up_second = Counter(nuclear_upper(PAIRS[k]['b']) for k in range(N_PAIRS))

print(f"  {'Trigram':>8s}  {'1st hex':>7s}  {'2nd hex':>7s}  {'Delta':>5s}")
for t in sorted(TRIGRAM_NAMES.keys()):
    f = nuc_up_first.get(t, 0)
    s = nuc_up_second.get(t, 0)
    print(f"  {tri_name(t):>8s}  {f:7d}  {s:7d}  {f-s:>+5d}")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. ORIENTATION DEPENDENCE OF TRIGRAM TRAJECTORIES
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("8. HOW DOES ORIENTATION CHANGE TRIGRAM TRAJECTORIES?")
print("=" * 80)
print()

# For each pair, flipping orientation swaps (a, b) ↔ (b, a)
# For inversion pair: this swaps (lo_a, up_a) ↔ (reverse(up_a), reverse(lo_a))
# The trigram trajectory changes at positions 2k and 2k+1

# Compute: if we flip pair k, how many trigram positions change?
# For inversion pairs: both positions change (different hexagrams at each slot)
# Unless lo_a = reverse(up_a) and up_a = reverse(lo_a) (rare)

n_traj_changes = []
for k in range(N_PAIRS):
    a, b = PAIRS[k]['a'], PAIRS[k]['b']
    la, ua = lower_tri(a), upper_tri(a)
    lb, ub = lower_tri(b), upper_tri(b)
    
    # Count changes in the 4 trigram slots (2 positions × 2 trigrams each)
    changes = 0
    if la != lb:
        changes += 1  # lower trigram at pos 2k changes
    if ua != ub:
        changes += 1  # upper trigram at pos 2k changes
    # Pos 2k+1 also swaps
    if la != lb:
        changes += 1
    if ua != ub:
        changes += 1
    
    n_traj_changes.append(changes)

print(f"  Trigram position changes per pair flip:")
change_dist = Counter(n_traj_changes)
for c in sorted(change_dist.keys()):
    pairs_list = [k+1 for k in range(N_PAIRS) if n_traj_changes[k] == c]
    print(f"    {c}/4 slots change: {change_dist[c]} pairs — {pairs_list}")


# ═══════════════════════════════════════════════════════════════════════════════
# 9. TRIGRAM TRANSITIONS AT BRIDGES
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("9. TRIGRAM TRANSITIONS AT BRIDGES")
print("   Bridge k: exit hex (2k+1) → entry hex (2k+2)")
print("=" * 80)
print()

print(f"  {'Br':>3s}  {'Exit Lo':>8s} {'Exit Up':>8s}  →  {'Entry Lo':>8s} {'Entry Up':>8s}  "
      f"{'Lo match':>8s} {'Up match':>8s}")

lo_same = 0
up_same = 0
for k in range(31):
    exit_hex = M[2*k + 1]
    entry_hex = M[2*k + 2]
    
    elo = lower_tri(exit_hex)
    eup = upper_tri(exit_hex)
    nlo = lower_tri(entry_hex)
    nup = upper_tri(entry_hex)
    
    lo_match = 'same' if elo == nlo else 'diff'
    up_match = 'same' if eup == nup else 'diff'
    
    if elo == nlo: lo_same += 1
    if eup == nup: up_same += 1
    
    print(f"  B{k:2d}  {tri_name(elo):>8s} {tri_name(eup):>8s}  →  "
          f"{tri_name(nlo):>8s} {tri_name(nup):>8s}  "
          f"{lo_match:>8s} {up_match:>8s}")

print(f"\n  Lower trigram preserved at bridge: {lo_same}/31")
print(f"  Upper trigram preserved at bridge: {up_same}/31")


# ═══════════════════════════════════════════════════════════════════════════════
# 10. COMPARISON TO RANDOM S=2-FREE ORIENTATIONS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("10. TRIGRAM STATISTICS: KW vs RANDOM S=2-FREE ORIENTATIONS")
print("=" * 80)
print()

# S=2 constraints (from bridge_orientation.py)
def compute_S(hex_a, hex_b):
    m = tuple(hex_a[i] ^ hex_b[i] for i in range(6))
    return (m[0] & m[5]) + (m[1] & m[4]) + (m[2] & m[3])

CONSTRAINTS = {}
for k in range(31):
    forbidden = set()
    for o_k in [0, 1]:
        for o_k1 in [0, 1]:
            exit_hex = PAIRS[k]['b'] if o_k == 0 else PAIRS[k]['a']
            entry_hex = PAIRS[k+1]['a'] if o_k1 == 0 else PAIRS[k+1]['b']
            if compute_S(exit_hex, entry_hex) == 2:
                forbidden.add((o_k, o_k1))
    if forbidden:
        CONSTRAINTS[k] = forbidden


def build_sequence(orientation):
    """Build the 64-hexagram sequence from an orientation vector."""
    seq = []
    for k in range(N_PAIRS):
        if orientation[k] == 0:
            seq.append(PAIRS[k]['a'])
            seq.append(PAIRS[k]['b'])
        else:
            seq.append(PAIRS[k]['b'])
            seq.append(PAIRS[k]['a'])
    return seq


def trigram_stats(seq):
    """Compute trigram trajectory statistics for a 64-hex sequence."""
    lo_traj = [lower_tri(h) for h in seq]
    up_traj = [upper_tri(h) for h in seq]
    
    # (lower, upper) pair frequency
    pair_freq = Counter((lo_traj[i], up_traj[i]) for i in range(64))
    n_unique_pairs = len(pair_freq)
    max_pair_repeat = max(pair_freq.values())
    
    # Lower trigram at bridge transitions: how many preserved?
    lo_bridge_same = 0
    up_bridge_same = 0
    for k in range(31):
        if lo_traj[2*k+1] == lo_traj[2*k+2]:
            lo_bridge_same += 1
        if up_traj[2*k+1] == up_traj[2*k+2]:
            up_bridge_same += 1
    
    # First hex of each pair: trigram entropy
    first_lower = [lo_traj[2*k] for k in range(N_PAIRS)]
    first_lower_freq = Counter(first_lower)
    
    # Key trigram first-position counts
    heaven_first_lower = sum(1 for k in range(N_PAIRS) if lo_traj[2*k] == (1,1,1))
    earth_first_lower = sum(1 for k in range(N_PAIRS) if lo_traj[2*k] == (0,0,0))
    water_first_lower = sum(1 for k in range(N_PAIRS) if lo_traj[2*k] == (0,1,0))
    fire_first_lower = sum(1 for k in range(N_PAIRS) if lo_traj[2*k] == (1,0,1))
    
    # Nuclear trigram balance
    nuc_lo_first = Counter(nuclear_lower(seq[2*k]) for k in range(N_PAIRS))
    
    # Trigram transition entropy at bridges
    # How diverse are the (exit_lower, entry_lower) transitions?
    bridge_lo_trans = Counter()
    for k in range(31):
        bridge_lo_trans[(lo_traj[2*k+1], lo_traj[2*k+2])] += 1
    n_unique_lo_trans = len(bridge_lo_trans)
    
    return {
        'n_unique_pairs': n_unique_pairs,
        'max_pair_repeat': max_pair_repeat,
        'lo_bridge_same': lo_bridge_same,
        'up_bridge_same': up_bridge_same,
        'heaven_first_lower': heaven_first_lower,
        'earth_first_lower': earth_first_lower,
        'water_first_lower': water_first_lower,
        'fire_first_lower': fire_first_lower,
        'n_unique_lo_trans': n_unique_lo_trans,
    }


# KW baseline
kw_seq = build_sequence([0]*32)
kw_tri_stats = trigram_stats(kw_seq)

print(f"  KW trigram statistics:")
for key, val in kw_tri_stats.items():
    print(f"    {key}: {val}")

# Sample random S=2-free orientations
N_SAMPLES = 50_000
rng = random.Random(42)

sample_stats = defaultdict(list)
n_tried = 0

for i in range(N_SAMPLES):
    while True:
        n_tried += 1
        bits = rng.getrandbits(32)
        o = [(bits >> j) & 1 for j in range(32)]
        valid = True
        for k, forbidden in CONSTRAINTS.items():
            if (o[k], o[k+1]) in forbidden:
                valid = False
                break
        if valid:
            break
    
    seq = build_sequence(o)
    stats = trigram_stats(seq)
    for key, val in stats.items():
        sample_stats[key].append(val)

print(f"\n  Sampled {N_SAMPLES} S=2-free orientations (acceptance: {N_SAMPLES/n_tried:.4f})")
print(f"\n  {'Metric':>25s}  {'KW':>6s}  {'Mean':>6s}  {'Std':>6s}  {'p-val':>6s}")
print(f"  {'-'*60}")

for key in kw_tri_stats:
    kw_val = kw_tri_stats[key]
    arr = np.array(sample_stats[key])
    mean = arr.mean()
    std = arr.std()
    
    # Two-sided p-value
    p_low = np.mean(arr <= kw_val)
    p_high = np.mean(arr >= kw_val)
    p = 2 * min(p_low, p_high)
    
    print(f"  {key:>25s}  {kw_val:6.1f}  {mean:6.2f}  {std:6.2f}  {p:6.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 11. TRIGRAM-LEVEL ORIENTATION RULE: EXHAUSTIVE SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("11. EXHAUSTIVE TRIGRAM RULE SEARCH")
print("   For each of 64 (lower, upper) → bit mappings, how many match KW?")
print("=" * 80)
print()

# Build KW orientation vector from lower trigram
# For each pair, KW orientation = 0 (a first). 
# Can we find a function f(lower_tri, upper_tri) → {0,1} that matches?

# KW orientation: 0 for all pairs by convention 
# What we really want: can a trigram rule predict which hexagram of the pair
# is presented first? The "first" hex has certain lower/upper trigrams.

# For each pair, the first hex's trigram pair defines the "KW choice"
# A rule would map (lower, upper) → {first, second}
# But different pairs may have the same (lower, upper) with different orientations!

# Check: are (lower, upper) pairs unique across first hexagrams?
first_hex_trigram_pairs = [(lower_tri(PAIRS[k]['a']), upper_tri(PAIRS[k]['a'])) 
                           for k in range(N_PAIRS)]
fh_freq = Counter(first_hex_trigram_pairs)
repeated = {k: v for k, v in fh_freq.items() if v > 1}
print(f"  Repeated (lower, upper) pairs in first hexagrams: {len(repeated)}")
for (lo, up), cnt in repeated.items():
    print(f"    ({tri_name(lo)}, {tri_name(up)}): {cnt}×")

# A trigram rule can't distinguish pairs with the same (lower, upper) in the first hex.
# But it CAN distinguish if no pair shares the same trigram combination.

# Simpler approach: for INVERSION pairs, the choice is between (lo, up) and
# (reverse(up), reverse(lo)). A rule could be: prefer the one where lo > up
# in some ordering.

# Test: among inversion pairs, is there a total ordering on trigrams such that
# KW always picks the hex where the lower trigram ranks higher?

# There are 8! = 40320 possible orderings. Test them all.
from itertools import permutations

all_tris = list(TRIGRAM_NAMES.keys())

# For each inversion pair, record which trigram is lower in the first hex
inv_first_lowers = []
for p in PAIRS:
    if p['is_inv']:
        lo_a = lower_tri(p['a'])
        lo_b = lower_tri(p['b'])
        inv_first_lowers.append((lo_a, lo_b))

print(f"\n  Searching all {math.factorial(8)} trigram orderings...")
print(f"  ({len(inv_first_lowers)} inversion pairs to match)")

best_ordering = None
best_score = 0

for perm in permutations(range(8)):
    # perm defines an ordering: all_tris[i] has rank perm[i]
    tri_rank = {all_tris[i]: perm[i] for i in range(8)}
    
    score = 0
    for lo_a, lo_b in inv_first_lowers:
        # Check: does KW pick the hex whose lower trigram ranks higher?
        if tri_rank[lo_a] > tri_rank[lo_b]:
            score += 1
    
    best_dir = max(score, len(inv_first_lowers) - score)
    if best_dir > best_score:
        best_score = best_dir
        best_ordering = tri_rank.copy()

print(f"  Best lower-trigram ordering score: {best_score}/{len(inv_first_lowers)}")
if best_ordering:
    ordering_list = sorted(best_ordering.keys(), key=lambda t: -best_ordering[t])
    print(f"  Ordering (highest first): {[tri_name(t) for t in ordering_list]}")

# Same for upper trigram
inv_first_uppers = []
for p in PAIRS:
    if p['is_inv']:
        up_a = upper_tri(p['a'])
        up_b = upper_tri(p['b'])
        inv_first_uppers.append((up_a, up_b))

best_upper_score = 0
best_upper_ordering = None

for perm in permutations(range(8)):
    tri_rank = {all_tris[i]: perm[i] for i in range(8)}
    
    score = 0
    for up_a, up_b in inv_first_uppers:
        if tri_rank[up_a] > tri_rank[up_b]:
            score += 1
    
    best_dir = max(score, len(inv_first_uppers) - score)
    if best_dir > best_score:
        best_upper_score = best_dir
        best_upper_ordering = tri_rank.copy()
    elif best_dir > best_upper_score:
        best_upper_score = best_dir
        best_upper_ordering = tri_rank.copy()

print(f"\n  Best upper-trigram ordering score: {best_upper_score}/{len(inv_first_uppers)}")
if best_upper_ordering:
    ordering_list = sorted(best_upper_ordering.keys(), key=lambda t: -best_upper_ordering[t])
    print(f"  Ordering (highest first): {[tri_name(t) for t in ordering_list]}")


# ═══════════════════════════════════════════════════════════════════════════════
# 12. CANON-SPLIT TRIGRAM ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print()
print("=" * 80)
print("12. CANON SPLIT — TRIGRAM PATTERNS IN UPPER vs LOWER CANON")
print("=" * 80)
print()

# Upper canon: pairs 1-15 (positions 0-29)
# Lower canon: pairs 16-32 (positions 30-63, but actually pair 16 starts at pos 30)
# Note: traditionally hex 1-30 = upper canon, but in pair terms pair 15 ends at hex 30
# Actually pair 15 = (hex 29, hex 30), pair 16 = (hex 31, hex 32)

upper_canon_pairs = list(range(15))   # pairs 0-14 (1-indexed: 1-15)
lower_canon_pairs = list(range(15, 32))  # pairs 15-31 (1-indexed: 16-32)

for label, pair_range in [("Upper canon (pairs 1-15)", upper_canon_pairs),
                           ("Lower canon (pairs 16-32)", lower_canon_pairs)]:
    print(f"  {label}:")
    
    first_lo_freq = Counter(lower_tri(PAIRS[k]['a']) for k in pair_range)
    first_up_freq = Counter(upper_tri(PAIRS[k]['a']) for k in pair_range)
    
    print(f"    First hex lower trigrams:")
    for t in sorted(TRIGRAM_NAMES.keys()):
        cnt = first_lo_freq.get(t, 0)
        bar = '█' * cnt
        print(f"      {tri_name(t):>8s}: {cnt:2d} {bar}")
    
    print(f"    First hex upper trigrams:")
    for t in sorted(TRIGRAM_NAMES.keys()):
        cnt = first_up_freq.get(t, 0)
        bar = '█' * cnt
        print(f"      {tri_name(t):>8s}: {cnt:2d} {bar}")
    print()


print()
print("=" * 80)
print("TRIGRAM ORIENTATION ANALYSIS COMPLETE")
print("=" * 80)
