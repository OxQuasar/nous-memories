"""
Iter5 Round 2 — Priority 1: C2/C1 Disagreement Verification

Compare KW, C1 (M-rule), and C2 (sequential diversity) bit-by-bit.
At disagreement positions, does KW match C1 or C2?

Tests the hypothesis: "KW's m-score is a consequence of its sequential
diversity choices, not an independent principle."
"""

import sys
sys.path.insert(0, '/home/quasar/nous/logoswen/iter5')
from infra import *

import json

# ══════════════════════════════════════════════════════════════════════════════
# RECONSTRUCT C1 (M-rule) AND C2 (sequential diversity)
# ══════════════════════════════════════════════════════════════════════════════

# --- C1: M-rule (raw, before S=2 fix) ---
c1_raw = [0] * 32
for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    if a[1] != a[4]:  # M-decisive
        if a[1] == 0:
            c1_raw[k] = 0
        else:
            c1_raw[k] = 1
    else:  # M-indecisive: binary-high-first
        if hex_to_int(a) >= hex_to_int(b):
            c1_raw[k] = 0
        else:
            c1_raw[k] = 1

# --- C1: S=2-fixed (from round 1 data) ---
with open('/home/quasar/nous/logoswen/iter5/round1_data.json') as f:
    r1 = json.load(f)
c1_fixed = r1['C1']['orientation']
c2_o = r1['C2']['orientation']

# ══════════════════════════════════════════════════════════════════════════════
# PAIR-BY-PAIR ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 100)
print("C2/C1 DISAGREEMENT VERIFICATION")
print("=" * 100)
print()

# Pair properties
print(f"{'pair':>4s} {'KW':>3s} {'C1r':>3s} {'C1f':>3s} {'C2':>3s}  "
      f"{'M-dec':>5s} {'L2a':>3s} {'L5a':>3s}  "
      f"{'C1r=C2':>6s} {'KW=C1f':>6s} {'KW=C2':>5s}  "
      f"{'canon':>5s} {'note':>20s}")
print("─" * 100)

rows = []
m_decisive_set = set(M_DECISIVE)
s2_constrained = set()
for k in CONSTRAINTS:
    s2_constrained.add(k)
    s2_constrained.add(k + 1)

for k in range(N_PAIRS):
    a = PAIRS[k]['a']
    b = PAIRS[k]['b']
    
    kw = 0
    c1r = c1_raw[k]
    c1f = c1_fixed[k]
    c2 = c2_o[k]
    
    m_dec = 'Y' if k in m_decisive_set else 'N'
    l2a = a[1]
    l5a = a[4]
    
    c1r_eq_c2 = 'Y' if c1r == c2 else 'N'
    kw_eq_c1f = 'Y' if kw == c1f else 'N'
    kw_eq_c2 = 'Y' if kw == c2 else 'N'
    canon = 'upper' if k < 15 else 'lower'
    
    # Determine note
    notes = []
    if c1r != c1f:
        notes.append('S2-fix')
    if k in s2_constrained:
        notes.append('constrained')
    note = ', '.join(notes) if notes else ''
    
    print(f"{k:4d} {kw:3d} {c1r:3d} {c1f:3d} {c2:3d}  "
          f"{m_dec:>5s} {l2a:3d} {l5a:3d}  "
          f"{c1r_eq_c2:>6s} {kw_eq_c1f:>6s} {kw_eq_c2:>5s}  "
          f"{canon:>5s} {note:>20s}")
    
    rows.append({
        'pair': k, 'kw': kw, 'c1_raw': c1r, 'c1_fixed': c1f, 'c2': c2,
        'm_decisive': k in m_decisive_set, 'L2_a': l2a, 'L5_a': l5a,
        'c1r_eq_c2': c1r == c2, 'kw_eq_c1f': kw == c1f, 'kw_eq_c2': kw == c2,
        'canon': canon, 's2_constrained': k in s2_constrained,
        'c1_s2_fixed': c1r != c1f,
    })

print()

# ══════════════════════════════════════════════════════════════════════════════
# SUMMARY STATISTICS
# ══════════════════════════════════════════════════════════════════════════════

# Agreement counts
kw_eq_c1f_count = sum(1 for r in rows if r['kw_eq_c1f'])
kw_eq_c2_count = sum(1 for r in rows if r['kw_eq_c2'])
c1r_eq_c2_count = sum(1 for r in rows if r['c1r_eq_c2'])
c1f_eq_c2_count = sum(1 for r in rows if r['c1_fixed'] == r['c2'])

print("AGREEMENT COUNTS (out of 32 pairs):")
print(f"  KW = C1 (fixed):     {kw_eq_c1f_count}")
print(f"  KW = C2:             {kw_eq_c2_count}")
print(f"  C1 (raw) = C2:       {c1r_eq_c2_count}")
print(f"  C1 (fixed) = C2:     {c1f_eq_c2_count}")
print()

# Disagreement analysis: where C1_fixed ≠ C2
disagree_c1f_c2 = [r for r in rows if r['c1_fixed'] != r['c2']]
print(f"DISAGREEMENT PAIRS (C1_fixed ≠ C2): {len(disagree_c1f_c2)} pairs")
print()

if disagree_c1f_c2:
    kw_sides_c1 = sum(1 for r in disagree_c1f_c2 if r['kw'] == r['c1_fixed'])
    kw_sides_c2 = sum(1 for r in disagree_c1f_c2 if r['kw'] == r['c2'])
    
    print(f"  At disagreement positions, KW matches:")
    print(f"    C1 (fixed): {kw_sides_c1}/{len(disagree_c1f_c2)}")
    print(f"    C2:         {kw_sides_c2}/{len(disagree_c1f_c2)}")
    print()
    
    # Break down by M-decisive / M-indecisive
    disagree_m_dec = [r for r in disagree_c1f_c2 if r['m_decisive']]
    disagree_m_indec = [r for r in disagree_c1f_c2 if not r['m_decisive']]
    
    print(f"  Among M-decisive disagreements ({len(disagree_m_dec)}):")
    if disagree_m_dec:
        kw_c1_md = sum(1 for r in disagree_m_dec if r['kw'] == r['c1_fixed'])
        kw_c2_md = sum(1 for r in disagree_m_dec if r['kw'] == r['c2'])
        print(f"    KW matches C1: {kw_c1_md}")
        print(f"    KW matches C2: {kw_c2_md}")
    
    print(f"  Among M-indecisive disagreements ({len(disagree_m_indec)}):")
    if disagree_m_indec:
        kw_c1_mi = sum(1 for r in disagree_m_indec if r['kw'] == r['c1_fixed'])
        kw_c2_mi = sum(1 for r in disagree_m_indec if r['kw'] == r['c2'])
        print(f"    KW matches C1: {kw_c1_mi}")
        print(f"    KW matches C2: {kw_c2_mi}")
    print()
    
    # Break down by canon
    disagree_upper = [r for r in disagree_c1f_c2 if r['canon'] == 'upper']
    disagree_lower = [r for r in disagree_c1f_c2 if r['canon'] == 'lower']
    
    print(f"  By canon:")
    if disagree_upper:
        kw_c1_u = sum(1 for r in disagree_upper if r['kw'] == r['c1_fixed'])
        kw_c2_u = sum(1 for r in disagree_upper if r['kw'] == r['c2'])
        print(f"    Upper ({len(disagree_upper)}): KW=C1 {kw_c1_u}, KW=C2 {kw_c2_u}")
    if disagree_lower:
        kw_c1_l = sum(1 for r in disagree_lower if r['kw'] == r['c1_fixed'])
        kw_c2_l = sum(1 for r in disagree_lower if r['kw'] == r['c2'])
        print(f"    Lower ({len(disagree_lower)}): KW=C1 {kw_c1_l}, KW=C2 {kw_c2_l}")
    print()

# Detailed disagree table
print("DETAILED DISAGREEMENT TABLE:")
print(f"{'pair':>4s} {'KW':>3s} {'C1f':>3s} {'C2':>3s}  "
      f"{'KW sides':>8s} {'M-dec':>5s} {'constrained':>11s}")
print("─" * 50)
for r in disagree_c1f_c2:
    side = 'C1' if r['kw'] == r['c1_fixed'] else 'C2'
    m_dec = 'Y' if r['m_decisive'] else 'N'
    const = 'Y' if r['s2_constrained'] else 'N'
    print(f"{r['pair']:4d} {r['kw']:3d} {r['c1_fixed']:3d} {r['c2']:3d}  "
          f"{side:>8s} {m_dec:>5s} {const:>11s}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# C2's M-SCORE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("C2's M-SCORE DECOMPOSITION")
print("=" * 80)
print()

# For each M-decisive pair, does C2 match the M-rule?
c2_seq = build_sequence(c2_o)
c2_m_matches = 0
c2_m_misses = 0

print(f"{'pair':>4s} {'C2':>3s} {'C2_L2':>5s} {'M-rule':>6s} {'match':>5s}")
print("─" * 30)
for k in M_DECISIVE:
    first_hex = c2_seq[2*k]
    c2_l2 = first_hex[1]
    m_wants = 0  # M-rule wants L2=yin (0)
    match = 'Y' if c2_l2 == 0 else 'N'
    if c2_l2 == 0:
        c2_m_matches += 1
    else:
        c2_m_misses += 1
    print(f"{k:4d} {c2_o[k]:3d} {c2_l2:5d} {'L2=0':>6s} {match:>5s}")

print()
print(f"C2 m_score: {c2_m_matches}/{len(M_DECISIVE)} (matches M-rule at {c2_m_matches} of {len(M_DECISIVE)} decisive pairs)")
print(f"KW m_score: {KW_M}/{len(M_DECISIVE)}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# KERNEL CHAIN AT DISAGREEMENT POINTS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("KERNEL CHAIN CONTEXT AT DISAGREEMENT POINTS")
print("=" * 80)
print()

kw_seq = build_sequence(KW_O)

# Show kernel chain around each disagreement
for r in disagree_c1f_c2:
    k = r['pair']
    print(f"Pair {k} — KW={r['kw']}, C1f={r['c1_fixed']}, C2={r['c2']}:")
    
    # Show bridges k-2, k-1, k (if they exist)
    for bk in range(max(0, k-2), min(31, k+1)):
        # KW kernel
        kw_kern = kernel_name(kw_seq[2*bk+1], kw_seq[2*bk+2])
        # What kernel would C1 produce?
        c1_seq = build_sequence(c1_fixed)
        c1_kern = kernel_name(c1_seq[2*bk+1], c1_seq[2*bk+2])
        # What kernel does C2 produce?
        c2_kern = kernel_name(c2_seq[2*bk+1], c2_seq[2*bk+2])
        
        marker = ' <-- disagree bridge' if bk == k-1 or bk == k else ''
        print(f"  bridge {bk:2d}: KW={kw_kern:>3s}  C1={c1_kern:>3s}  C2={c2_kern:>3s}{marker}")
    print()


# ══════════════════════════════════════════════════════════════════════════════
# SAVE DATA
# ══════════════════════════════════════════════════════════════════════════════

save_data = json_clean({
    'pair_comparison': rows,
    'summary': {
        'kw_eq_c1f': kw_eq_c1f_count,
        'kw_eq_c2': kw_eq_c2_count,
        'c1r_eq_c2': c1r_eq_c2_count,
        'c1f_eq_c2': c1f_eq_c2_count,
        'n_disagree': len(disagree_c1f_c2),
        'kw_sides_c1_at_disagree': sum(1 for r in disagree_c1f_c2 if r['kw'] == r['c1_fixed']),
        'kw_sides_c2_at_disagree': sum(1 for r in disagree_c1f_c2 if r['kw'] == r['c2']),
        'c2_m_score': c2_m_matches,
    },
})

with open('/home/quasar/nous/logoswen/iter5/round2_verify_data.json', 'w') as f:
    json.dump(save_data, f, indent=2)

print("Data saved to round2_verify_data.json")
