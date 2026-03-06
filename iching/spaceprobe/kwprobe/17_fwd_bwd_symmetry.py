"""
Forward/backward symmetry of the KW sequence.

The timewave claims the sequence reads equivalently forwards and backwards.
Test at multiple levels:
  1. Full hexagram Hamming distance (n=6)
  2. Inner bits distance (n=4, determines 互)
  3. Outer bits distance (n=2, surface)
  4. Basin sequence
  5. Lower trigram sequence (n=3)
  6. Upper trigram sequence (n=3)
  7. The actual hexagram sequence (is it a palindrome? reverse-complement?)
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
import numpy as np
from scipy import stats
import random

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, lower_trigram, upper_trigram, hugua,
    TRIGRAM_NAMES, reverse6, hamming6, fmt6,
)

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    elif b2 == 1 and b3 == 1: return 1
    else: return 0

def get_inner(h): return (h >> 1) & 0xF
def get_outer(h): return (h & 1) | (((h >> 5) & 1) << 1)
def hamming(a, b, nbits=6): return bin(a ^ b).count('1')

# ══════════════════════════════════════════════════════════════════════════════
# 1. FIRST-ORDER DIFFERENCES: FORWARD vs REVERSED
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. FIRST-ORDER DIFFERENCE SEQUENCES")
print("=" * 70)

# Compute all difference sequences
hex_diffs = [hamming6(kw_hex[i], kw_hex[i+1]) for i in range(63)]
inner_diffs = [hamming(get_inner(kw_hex[i]), get_inner(kw_hex[i+1]), 4) for i in range(63)]
outer_diffs = [hamming(get_outer(kw_hex[i]), get_outer(kw_hex[i+1]), 2) for i in range(63)]
basin_seq = [get_basin(h) for h in kw_hex]
basin_diffs = [abs(basin_seq[i+1] - basin_seq[i]) for i in range(63)]
lo_diffs = [hamming(lower_trigram(kw_hex[i]), lower_trigram(kw_hex[i+1]), 3) for i in range(63)]
up_diffs = [hamming(upper_trigram(kw_hex[i]), upper_trigram(kw_hex[i+1]), 3) for i in range(63)]

# Also the raw sequences
lo_seq = [lower_trigram(h) for h in kw_hex]
up_seq = [upper_trigram(h) for h in kw_hex]
hu_seq = [hugua(h) for h in kw_hex]
hu_diffs = [hamming6(hu_seq[i], hu_seq[i+1]) for i in range(63)]

for label, diffs in [
    ("Hex (n=6)", hex_diffs),
    ("Inner (n=4)", inner_diffs),
    ("Outer (n=2)", outer_diffs),
    ("Basin", basin_diffs),
    ("Lower tri (n=3)", lo_diffs),
    ("Upper tri (n=3)", up_diffs),
    ("互 (n=6)", hu_diffs),
]:
    rev = list(reversed(diffs))
    is_palindrome = diffs == rev
    
    # Correlation between forward and reversed
    r, p = stats.pearsonr(diffs, rev)
    
    # How many positions match?
    matches = sum(1 for i in range(63) if diffs[i] == rev[i])
    
    # Distance between forward and reversed sequences
    l1_dist = sum(abs(diffs[i] - rev[i]) for i in range(63))
    
    print(f"\n  {label}:")
    print(f"    Palindrome: {is_palindrome}")
    print(f"    Positions matching: {matches}/63 ({100*matches/63:.1f}%)")
    print(f"    Correlation fwd↔rev: r={r:.4f}  p={p:.4f}")
    print(f"    L1 distance: {l1_dist}")
    print(f"    Forward:  {diffs}")
    print(f"    Reversed: {rev}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. RAW SEQUENCE SYMMETRY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. RAW SEQUENCE SYMMETRY")
print("=" * 70)

# Is the hexagram sequence a palindrome?
rev_hex = list(reversed(kw_hex))
hex_palindrome = kw_hex == rev_hex
print(f"\n  Hexagram sequence is palindrome: {hex_palindrome}")

# Is the basin sequence a palindrome?
rev_basin = list(reversed(basin_seq))
basin_palindrome = basin_seq == rev_basin
basin_matches = sum(1 for i in range(64) if basin_seq[i] == rev_basin[i])
print(f"  Basin sequence is palindrome: {basin_palindrome}")
print(f"  Basin positions matching: {basin_matches}/64 ({100*basin_matches/64:.1f}%)")

# Is the lower/upper trigram sequence palindromic?
rev_lo = list(reversed(lo_seq))
rev_up = list(reversed(up_seq))
lo_matches = sum(1 for i in range(64) if lo_seq[i] == rev_lo[i])
up_matches = sum(1 for i in range(64) if up_seq[i] == rev_up[i])
print(f"  Lower trigram positions matching: {lo_matches}/64 ({100*lo_matches/64:.1f}%)")
print(f"  Upper trigram positions matching: {up_matches}/64 ({100*up_matches/64:.1f}%)")

# Cross-check: does reversed sequence swap lower↔upper?
lo_rev_matches_up = sum(1 for i in range(64) if lo_seq[i] == rev_up[i])
up_rev_matches_lo = sum(1 for i in range(64) if up_seq[i] == rev_lo[i])
print(f"  Lower[i] = Upper[64-i]? matches: {lo_rev_matches_up}/64 ({100*lo_rev_matches_up/64:.1f}%)")
print(f"  Upper[i] = Lower[64-i]? matches: {up_rev_matches_lo}/64 ({100*up_rev_matches_lo/64:.1f}%)")

# Is reversed sequence related by reverse6 (swap upper/lower trigrams)?
rev6_matches = sum(1 for i in range(64) if kw_hex[i] == reverse6(kw_hex[63-i]))
comp_matches = sum(1 for i in range(64) if kw_hex[i] == kw_hex[63-i] ^ MASK_ALL)
rev_comp_matches = sum(1 for i in range(64) if kw_hex[i] == reverse6(kw_hex[63-i]) ^ MASK_ALL)
print(f"\n  h[i] = reverse(h[64-i])? matches: {rev6_matches}/64")
print(f"  h[i] = complement(h[64-i])? matches: {comp_matches}/64")
print(f"  h[i] = rev∘comp(h[64-i])? matches: {rev_comp_matches}/64")

# ══════════════════════════════════════════════════════════════════════════════
# 3. RANDOM BASELINE: HOW PALINDROMIC IS TYPICAL?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. RANDOM BASELINE — PALINDROME CORRELATION")
print("=" * 70)

N_PERM = 10000
random.seed(42)

# For each difference type, compute fwd↔rev correlation for random permutations
for label, orig_seq, diff_fn in [
    ("Hex diffs", kw_hex, lambda s: [hamming6(s[i], s[i+1]) for i in range(63)]),
    ("Basin diffs", kw_hex, lambda s: [abs(get_basin(s[i+1]) - get_basin(s[i])) for i in range(63)]),
    ("Inner diffs", kw_hex, lambda s: [hamming(get_inner(s[i]), get_inner(s[i+1]), 4) for i in range(63)]),
    ("互 diffs", kw_hex, lambda s: [hamming6(hugua(s[i]), hugua(s[i+1])) for i in range(63)]),
]:
    kw_diffs = diff_fn(orig_seq)
    kw_r, _ = stats.pearsonr(kw_diffs, list(reversed(kw_diffs)))
    
    rand_rs = []
    for _ in range(N_PERM):
        perm = list(orig_seq)
        random.shuffle(perm)
        d = diff_fn(perm)
        r, _ = stats.pearsonr(d, list(reversed(d)))
        rand_rs.append(r)
    
    pct = stats.percentileofscore(rand_rs, kw_r)
    print(f"\n  {label}:")
    print(f"    KW fwd↔rev r = {kw_r:.4f}")
    print(f"    Random: mean={np.mean(rand_rs):.4f} ± {np.std(rand_rs):.4f}")
    print(f"    KW percentile: {pct:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 4. HALF-SEQUENCE SYMMETRY (UC vs LC mirror?)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. HALF-SEQUENCE MIRROR: UC vs REVERSED LC")
print("=" * 70)

# UC = positions 0-29 (hex 1-30), LC = positions 30-63 (hex 31-64)
uc_hex = kw_hex[:30]
lc_hex = kw_hex[30:]

uc_diffs = [hamming6(uc_hex[i], uc_hex[i+1]) for i in range(len(uc_hex)-1)]
lc_diffs = [hamming6(lc_hex[i], lc_hex[i+1]) for i in range(len(lc_hex)-1)]
lc_rev_diffs = list(reversed(lc_diffs))

# Trim to same length
min_len = min(len(uc_diffs), len(lc_rev_diffs))
r_uc_lc, p_uc_lc = stats.pearsonr(uc_diffs[:min_len], lc_rev_diffs[:min_len])

print(f"\n  UC diffs ({len(uc_diffs)}): {uc_diffs}")
print(f"  LC reversed ({len(lc_rev_diffs)}): {lc_rev_diffs}")
print(f"  Correlation UC ↔ reversed LC: r={r_uc_lc:.4f}  p={p_uc_lc:.4f}")

# Basin level
uc_basin = [get_basin(h) for h in uc_hex]
lc_basin = [get_basin(h) for h in lc_hex]
lc_rev_basin = list(reversed(lc_basin))

basin_match = sum(1 for i in range(min(len(uc_basin), len(lc_rev_basin))) 
                  if uc_basin[i] == lc_rev_basin[i])
print(f"\n  UC basin: {['○◎●'[b+1] for b in uc_basin]}")
print(f"  LC rev:   {['○◎●'[b+1] for b in lc_rev_basin]}")
print(f"  Basin matches: {basin_match}/{min(len(uc_basin), len(lc_rev_basin))}")

# With polarity flip (UC→Kun maps to LC→Qian, so flip sign)
lc_rev_flip = [-b for b in lc_rev_basin]
basin_flip_match = sum(1 for i in range(min(len(uc_basin), len(lc_rev_flip)))
                       if uc_basin[i] == lc_rev_flip[i])
print(f"\n  UC basin vs LC reversed + polarity flipped:")
print(f"  UC basin: {['○◎●'[b+1] for b in uc_basin]}")
print(f"  LC flip:  {['○◎●'[b+1] for b in lc_rev_flip]}")
print(f"  Matches: {basin_flip_match}/{min(len(uc_basin), len(lc_rev_flip))}")

r_basin_flip, p_basin_flip = stats.pearsonr(
    uc_basin[:min(len(uc_basin), len(lc_rev_flip))],
    lc_rev_flip[:min(len(uc_basin), len(lc_rev_flip))]
)
print(f"  Correlation: r={r_basin_flip:.4f}  p={p_basin_flip:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE TIMEWAVE'S 384 VALUES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. TIMEWAVE-STYLE 384-VALUE WAVE")
print("=" * 70)

# The timewave uses 6 values per transition (one per line), not just Hamming.
# For each consecutive pair, which lines change?
# This gives a 384-value sequence (63 transitions × 6 lines... 
# actually the timewave uses 64 hexagrams × 6 lines = 384)

# Method: for each of the 63 transitions, record which of 6 lines flip
# Then check if this 63×6 = 378 bit matrix is palindromic

print(f"\n  Line-level change matrix (63 transitions × 6 lines):")
line_changes = []
for i in range(63):
    xor = kw_hex[i] ^ kw_hex[i+1]
    bits = [(xor >> j) & 1 for j in range(6)]
    line_changes.append(bits)

# Is this matrix palindromic row-wise?
rev_line_changes = list(reversed(line_changes))
row_matches = sum(1 for i in range(63) if line_changes[i] == rev_line_changes[i])
print(f"  Row-palindrome: {row_matches}/63 rows match ({100*row_matches/63:.1f}%)")

# Column-wise palindrome check
for line in range(6):
    col = [line_changes[i][line] for i in range(63)]
    rev_col = list(reversed(col))
    col_match = sum(1 for i in range(63) if col[i] == rev_col[i])
    r_col, p_col = stats.pearsonr(col, rev_col)
    print(f"  Line {line}: matches={col_match}/63  r={r_col:.4f}  p={p_col:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. SUMMARY")
print("=" * 70)
