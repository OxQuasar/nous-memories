"""
Thread 6: Single-Bit Bridges — The Minimal Transitions

Questions:
- Which two bridges change only a single bit?
- Which hexagrams, which line, which orbit transition?
- Is the flipped bit a signature bit (tension) or harmony bit?
- What's special about these positions in the sequence?
- What's the full Hamming distance spectrum's relationship to sequence position?
"""

import sys
sys.path.insert(0, '../kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits, lower_trigram, upper_trigram, trigram_name

DIMS = 6
M = all_bits()

GEN_BITS = {
    'O': (1,0,0,0,0,1),
    'M': (0,1,0,0,1,0),
    'I': (0,0,1,1,0,0),
}

# Line labels: which generators each line participates in
LINE_ROLES = {
    0: 'O',       # line 1: outer generator
    1: 'M',       # line 2: middle generator  
    2: 'I',       # line 3: inner generator
    3: 'I',       # line 4: inner generator (mirror of line 3)
    4: 'M',       # line 5: middle generator (mirror of line 2)
    5: 'O',       # line 6: outer generator (mirror of line 1)
}

# Mirror pairs
MIRROR_PAIRS = [(0, 5), (1, 4), (2, 3)]  # (O, M, I)

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def sig_name(sig):
    parts = []
    labels = ['o', 'm', 'i']
    for i, s in enumerate(sig):
        if s: parts.append(labels[i])
    return ''.join(parts) if parts else 'id'


# ─── Build all bridges ────────────────────────────────────────────────────

bridges = []
for k in range(31):
    idx_a = 2 * k + 1
    idx_b = 2 * k + 2
    a = tuple(M[idx_a])
    b = tuple(M[idx_b])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'num_a': idx_a + 1, 'num_b': idx_b + 1,
        'name_a': KING_WEN[idx_a][1], 'name_b': KING_WEN[idx_b][1],
        'idx_a': idx_a, 'idx_b': idx_b,
        'xor': xor,
        'hamming': sum(xor),
        'sig_a': sig_a, 'sig_b': sig_b,
    })


print("=" * 70)
print("THREAD 6: SINGLE-BIT BRIDGES — MINIMAL TRANSITIONS")
print("=" * 70)

# ─── 1. Identify the two single-bit bridges ───────────────────────────────

print(f"\n1. THE TWO SINGLE-BIT BRIDGES")

single_bit_bridges = [b for b in bridges if b['hamming'] == 1]

for b in single_bit_bridges:
    # Which bit flips?
    flipped_line = [i for i in range(DIMS) if b['xor'][i] == 1][0]
    line_role = LINE_ROLES[flipped_line]
    mirror_partner = MIRROR_PAIRS[['O','M','I'].index(line_role)]
    
    # Is this a signature bit? 
    # Signature changes when a line flips but its mirror partner doesn't
    sig_change = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
    
    # The flipped bit's position in its mirror pair
    if flipped_line == mirror_partner[0]:
        position = "lower"
    else:
        position = "upper"
    
    # Line values before and after
    before_val = b['a'][flipped_line]
    after_val = b['b'][flipped_line]
    
    # Mirror line value (doesn't change)
    if flipped_line == mirror_partner[0]:
        mirror_line = mirror_partner[1]
    else:
        mirror_line = mirror_partner[0]
    mirror_val = b['a'][mirror_line]
    
    # Are they the same or different before the flip?
    were_same = (before_val == mirror_val)
    # After the flip?
    now_same = (after_val == mirror_val)
    
    print(f"\n   Bridge B{b['idx']+1}:")
    print(f"     #{b['num_a']:2d} {b['name_a']:<12s} ({''.join(map(str, b['a']))}) →"
          f" #{b['num_b']:2d} {b['name_b']:<12s} ({''.join(map(str, b['b']))})")
    print(f"     XOR mask: {''.join(map(str, b['xor']))}")
    print(f"     Flipped line: {flipped_line + 1} (0-indexed: {flipped_line})")
    print(f"     Line role: {line_role} generator ({position} half of mirror pair {mirror_partner})")
    print(f"     Line changes: {before_val} → {after_val} ({'yin→yang' if after_val > before_val else 'yang→yin'})")
    print(f"     Mirror partner (line {mirror_line + 1}): value = {mirror_val} (unchanged)")
    print(f"     Before flip: mirror pair {'SAME' if were_same else 'DIFFERENT'} → After: {'SAME' if now_same else 'DIFFERENT'}")
    print(f"     Orbit: {sig_name(b['sig_a'])}({''.join(map(str, b['sig_a']))}) → "
          f"{sig_name(b['sig_b'])}({''.join(map(str, b['sig_b']))})")
    print(f"     Sig change: {sig_name(sig_change)}")
    
    # Trigram analysis
    lower_a = ''.join(map(str, b['a'][:3]))
    upper_a = ''.join(map(str, b['a'][3:]))
    lower_b = ''.join(map(str, b['b'][:3]))
    upper_b = ''.join(map(str, b['b'][3:]))
    
    print(f"     Lower trigram: {lower_a}({trigram_name(lower_a)}) → {lower_b}({trigram_name(lower_b)})"
          f"  {'CHANGED' if lower_a != lower_b else 'same'}")
    print(f"     Upper trigram: {upper_a}({trigram_name(upper_a)}) → {upper_b}({trigram_name(upper_b)})"
          f"  {'CHANGED' if upper_a != upper_b else 'same'}")
    
    # Position in sequence
    print(f"     Sequence position: between hex #{b['num_a']} and #{b['num_b']} (pair {b['num_b']//2} of 32)")


# ─── 2. Signature bit analysis ────────────────────────────────────────────

print(f"\n\n2. SIGNATURE BIT ANALYSIS")
print(f"   Is the flipped bit a 'signature bit' (part of the orbit-defining structure)?")
print(f"   ")
print(f"   The XOR signature is (line1⊕line6, line2⊕line5, line3⊕line4)")
print(f"   A single-bit flip changes one line but NOT its mirror partner.")
print(f"   This ALWAYS changes the signature → single-bit bridges ALWAYS cross orbits.")
print(f"   ")
print(f"   Proof: If line k flips, its mirror line k' doesn't.")
print(f"   Before: sig_component = line_k ⊕ line_k'")
print(f"   After:  sig_component = (1-line_k) ⊕ line_k' = 1 - (line_k ⊕ line_k')")
print(f"   The signature component INVERTS. Single-bit bridges cannot be self-transitions.")

# Verify
for b in single_bit_bridges:
    assert b['sig_a'] != b['sig_b'], "Single-bit bridge should cross orbits!"
print(f"   ✓ Verified: both single-bit bridges cross orbits")


# ─── 3. Contrast with 2-bit bridges ──────────────────────────────────────

print(f"\n\n3. ALL HAMMING-2 BRIDGES FOR COMPARISON")

h2_bridges = [b for b in bridges if b['hamming'] == 2]
print(f"   Found {len(h2_bridges)} Hamming-2 bridges")

for b in h2_bridges:
    flipped = [i for i in range(DIMS) if b['xor'][i] == 1]
    sig_change = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
    
    # Are the two flipped bits a mirror pair?
    is_mirror_pair = tuple(sorted(flipped)) in [tuple(sorted(p)) for p in MIRROR_PAIRS]
    
    lines_str = str([l+1 for l in flipped])
    print(f"   B{b['idx']+1:2d}: lines {lines_str:>8s}  "
          f"mirror_pair={'YES' if is_mirror_pair else 'no ':>3s}  "
          f"Δorbit={sig_name(sig_change):>3s}  "
          f"{b['name_a']:<12s}→{b['name_b']}")

mirror_pair_count = sum(1 for b in h2_bridges 
                       if tuple(sorted([i for i in range(DIMS) if b['xor'][i] == 1])) 
                       in [tuple(sorted(p)) for p in MIRROR_PAIRS])
print(f"\n   Of {len(h2_bridges)} H=2 bridges, {mirror_pair_count} flip a mirror pair (generator move)")
print(f"   Mirror-pair flips preserve orbit (sig unchanged).")
print(f"   Non-mirror-pair flips with H=2: both lines from same half → orbit changes")


# ─── 4. Full Hamming spectrum analysis ─────────────────────────────────────

print(f"\n\n4. FULL HAMMING DISTANCE SPECTRUM")

hamming_groups = defaultdict(list)
for b in bridges:
    hamming_groups[b['hamming']].append(b)

for h in sorted(hamming_groups.keys()):
    group = hamming_groups[h]
    sig_changes = [tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3)) for b in group]
    cross_count = sum(1 for s in sig_changes if s != (0,0,0))
    
    print(f"\n   Hamming {h}: {len(group)} bridges, {cross_count} cross-orbit")
    
    # Signature change distribution within this Hamming class
    sig_dist = Counter(sig_changes)
    for sig, count in sorted(sig_dist.items(), key=lambda x: -x[1]):
        print(f"     Δ{sig_name(sig):>3s}: {count}×")


# ─── 5. Hamming distance vs sequence position ─────────────────────────────

print(f"\n\n5. HAMMING DISTANCE vs SEQUENCE POSITION")
print(f"   Does bridge 'gentleness' correlate with position?")

# Split into halves (upper/lower canon)
first_half = bridges[:15]   # B1-B15 (upper canon bridges, roughly hex 1-30)
second_half = bridges[15:]  # B16-B31 (lower canon bridges, roughly hex 31-64)

h_first = [b['hamming'] for b in first_half]
h_second = [b['hamming'] for b in second_half]

print(f"   First half  (B1-B15):  mean H = {sum(h_first)/len(h_first):.2f}, distribution: {dict(Counter(h_first))}")
print(f"   Second half (B16-B31): mean H = {sum(h_second)/len(h_second):.2f}, distribution: {dict(Counter(h_second))}")

# Running average
print(f"\n   Position-by-position:")
for i, b in enumerate(bridges):
    bar = '█' * b['hamming'] + '░' * (6 - b['hamming'])
    sig_change = tuple(b['sig_a'][j] ^ b['sig_b'][j] for j in range(3))
    print(f"   B{i+1:2d} H={b['hamming']} {bar} Δ={sig_name(sig_change):>3s}  "
          f"{b['name_a']:<12s}→{b['name_b']}")


# ─── 6. Line-level analysis of single-bit bridges ─────────────────────────

print(f"\n\n6. LINE FLIP FREQUENCY ACROSS ALL BRIDGES")
print(f"   Which lines get flipped most often?")

line_flip_count = Counter()
for b in bridges:
    for i in range(DIMS):
        if b['xor'][i]:
            line_flip_count[i] += 1

print(f"   {'Line':<8s} Flips  Role  Position")
for line in range(DIMS):
    role = LINE_ROLES[line]
    pos = "lower" if line < 3 else "upper"
    print(f"   Line {line+1}:   {line_flip_count[line]:2d}×   {role}     {pos}")

total_flips = sum(line_flip_count.values())
print(f"\n   Total line flips: {total_flips} across 31 bridges")
print(f"   Lower trigram flips: {sum(line_flip_count[i] for i in range(3))}")
print(f"   Upper trigram flips: {sum(line_flip_count[i] for i in range(3, 6))}")


# ─── 7. Single-bit bridges in context ─────────────────────────────────────

print(f"\n\n7. NEIGHBORHOOD CONTEXT OF SINGLE-BIT BRIDGES")
print(f"   What happens immediately before and after each single-bit bridge?")

for b in single_bit_bridges:
    k = b['idx']
    print(f"\n   === Bridge B{k+1} (#{b['num_a']}→#{b['num_b']}) ===")
    
    # Previous bridge
    if k > 0:
        prev = bridges[k-1]
        print(f"   Prev bridge B{k}: H={prev['hamming']} "
              f"({''.join(map(str, prev['xor']))}) "
              f"{prev['name_a']}→{prev['name_b']}")
    
    # This bridge
    print(f"   THIS bridge B{k+1}: H={b['hamming']} "
          f"({''.join(map(str, b['xor']))}) "
          f"{b['name_a']}→{b['name_b']}")
    
    # Next bridge
    if k < 30:
        nxt = bridges[k+1]
        print(f"   Next bridge B{k+2}: H={nxt['hamming']} "
              f"({''.join(map(str, nxt['xor']))}) "
              f"{nxt['name_a']}→{nxt['name_b']}")
    
    # The standard pairs surrounding this bridge
    # Before bridge k: pair (2k+1, 2k+2) → standard pair at positions 2k+1 and 2k+2
    # Pair before: hex 2k+1 and hex 2k+2 (0-indexed: 2k, 2k+1)
    pair_before_a = tuple(M[2*k])
    pair_before_b = tuple(M[2*k + 1])
    pair_before_xor = tuple(int(pair_before_a[i]) ^ int(pair_before_b[i]) for i in range(DIMS))
    
    # Pair after: hex 2k+3 and hex 2k+4 (0-indexed: 2k+2, 2k+3)
    pair_after_a = tuple(M[2*k + 2])
    pair_after_b = tuple(M[2*k + 3])
    pair_after_xor = tuple(int(pair_after_a[i]) ^ int(pair_after_b[i]) for i in range(DIMS))
    
    print(f"   Pair before: #{2*k+1}-#{2*k+2} XOR={''.join(map(str, pair_before_xor))} H={sum(pair_before_xor)}")
    print(f"   Pair after:  #{2*k+3}-#{2*k+4} XOR={''.join(map(str, pair_after_xor))} H={sum(pair_after_xor)}")


# ─── 8. Minimum-change principle ──────────────────────────────────────────

print(f"\n\n8. MINIMUM-CHANGE PRINCIPLE")
print(f"   For each bridge, what's the minimum possible Hamming distance")
print(f"   to achieve the required orbit transition from that starting hexagram?")

# For each bridge, find all hexagrams in the target orbit
# and compute the minimum Hamming distance to any of them

orbits_by_sig = defaultdict(list)
for i in range(64):
    h = tuple(M[i])
    sig = xor_sig(h)
    orbits_by_sig[sig].append((i, h))

for b in bridges:
    target_sig = b['sig_b']
    target_hexagrams = orbits_by_sig[target_sig]
    
    # Minimum Hamming from b['a'] to any hexagram in target orbit
    min_h = min(sum(int(b['a'][i]) ^ int(t[1][i]) for i in range(DIMS)) for t in target_hexagrams)
    actual_h = b['hamming']
    
    optimal = "✓ OPTIMAL" if actual_h == min_h else f"  +{actual_h - min_h} above min"
    marker = "◀ SINGLE-BIT" if actual_h == 1 else ""
    
    print(f"   B{b['idx']+1:2d}: actual H={actual_h}, min possible H={min_h}  {optimal}  {marker}")

# Summary
optimal_count = 0
for b in bridges:
    target_sig = b['sig_b']
    target_hexagrams = orbits_by_sig[target_sig]
    min_h = min(sum(int(b['a'][i]) ^ int(t[1][i]) for i in range(DIMS)) for t in target_hexagrams)
    if b['hamming'] == min_h:
        optimal_count += 1

print(f"\n   Optimal (minimum Hamming): {optimal_count}/31 bridges")
print(f"   The sequence DOES NOT always minimize bit changes, but how close?")

total_excess = 0
for b in bridges:
    target_sig = b['sig_b']
    target_hexagrams = orbits_by_sig[target_sig]
    min_h = min(sum(int(b['a'][i]) ^ int(t[1][i]) for i in range(DIMS)) for t in target_hexagrams)
    total_excess += b['hamming'] - min_h

total_actual = sum(b['hamming'] for b in bridges)
total_minimum = total_actual - total_excess
print(f"   Total Hamming: {total_actual}, Minimum possible: {total_minimum}, Excess: {total_excess}")


print(f"\n{'=' * 70}")
print(f"THREAD 6 COMPLETE")
print(f"{'=' * 70}")
