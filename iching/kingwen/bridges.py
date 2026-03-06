"""
Bridge analysis: pair hexagrams offset by one (2-3, 4-5, 6-7, ...)
instead of the standard King Wen pairs (1-2, 3-4, 5-6, ...).

These are the inter-pair transitions — the "real" structural changes.
"""

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

N = 64
DIMS = 6
M = np.array(all_bits())

# Standard pair masks for reference
MASK_NAMES = {
    (1,1,1,1,1,1): "OMI", (1,1,0,0,1,1): "OM", (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI", (0,1,0,0,1,0): "M", (0,0,1,1,0,0): "I",
    (1,0,0,0,0,1): "O", (0,0,0,0,0,0): "id",
}

GEN_BITS = {
    'O': (1,0,0,0,0,1),
    'M': (0,1,0,0,1,0),
    'I': (0,0,1,1,0,0),
}


def mask_name(xor):
    if xor in MASK_NAMES:
        return MASK_NAMES[xor]
    return ''.join(map(str, xor))


def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))


def xor_sig(h):
    """XOR signature (orbit) of a hexagram."""
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])


# Build bridge pairs: (hex 2, hex 3), (hex 4, hex 5), ...
bridges = []
for k in range(31):
    idx_a = 2 * k + 1  # hex 2, 4, 6, ...
    idx_b = 2 * k + 2  # hex 3, 5, 7, ...
    a = tuple(M[idx_a])
    b = tuple(M[idx_b])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'num_a': idx_a + 1, 'num_b': idx_b + 1,
        'name_a': KING_WEN[idx_a][1], 'name_b': KING_WEN[idx_b][1],
        'xor': xor,
        'hamming': sum(xor),
        'sig_a': xor_sig(a), 'sig_b': xor_sig(b),
    })


# ─── 1. Bridge masks ─────────────────────────────────────────────────────────

print("=" * 70)
print("1. BRIDGE MASKS (offset pairs: 2-3, 4-5, 6-7, ...)")
print("=" * 70)

for b in bridges:
    mn = mask_name(b['xor'])
    print(f"  B{b['idx']+1:2d}: #{b['num_a']:2d} {b['name_a']:12s} → "
          f"#{b['num_b']:2d} {b['name_b']:12s}  "
          f"XOR={''.join(map(str, b['xor']))}  H={b['hamming']}  {mn}")

# How many are standard generator masks?
standard_count = sum(1 for b in bridges if b['xor'] in MASK_NAMES)
print(f"\n  Standard generator masks: {standard_count}/31")
print(f"  Non-standard masks: {31 - standard_count}/31")

# Mask frequency
xor_freq = Counter(b['xor'] for b in bridges)
print(f"\n  Unique masks: {len(xor_freq)}/31")
print(f"  Mask frequency:")
for xor, count in sorted(xor_freq.items(), key=lambda x: -x[1]):
    print(f"    {mask_name(xor):>10s} ({''.join(map(str, xor))}): {count}×")


# ─── 2. Hamming distance distribution ────────────────────────────────────────

print(f"\n{'=' * 70}")
print("2. BRIDGE HAMMING DISTANCES")
print("=" * 70)

h_dist = Counter(b['hamming'] for b in bridges)
print(f"  Distribution: {dict(sorted(h_dist.items()))}")
print(f"  Mean: {np.mean([b['hamming'] for b in bridges]):.2f}")

# Compare to standard pairs
std_pairs_h = []
for k in range(32):
    a = tuple(M[2*k])
    b = tuple(M[2*k+1])
    std_pairs_h.append(hamming(a, b))
print(f"  Standard pair mean: {np.mean(std_pairs_h):.2f}")


# ─── 3. Generator decomposition of bridge masks ──────────────────────────────

print(f"\n{'=' * 70}")
print("3. GENERATOR DECOMPOSITION OF BRIDGE MASKS")
print("=" * 70)

print(f"  Can each bridge mask be expressed as a combination of O, M, I?")
print(f"  O = (1,0,0,0,0,1), M = (0,1,0,0,1,0), I = (0,0,1,1,0,0)")

for b in bridges:
    xor = b['xor']
    # Try all 8 combinations of O, M, I
    found = False
    for use_o in [0, 1]:
        for use_m in [0, 1]:
            for use_i in [0, 1]:
                combo = tuple(
                    (use_o * GEN_BITS['O'][d] + use_m * GEN_BITS['M'][d] +
                     use_i * GEN_BITS['I'][d]) % 2
                    for d in range(DIMS)
                )
                if combo == xor:
                    gens = []
                    if use_o: gens.append('O')
                    if use_m: gens.append('M')
                    if use_i: gens.append('I')
                    label = ''.join(gens) if gens else 'id'
                    found = True
                    break
            if found: break
        if found: break

    if found:
        status = f"= {label}"
    else:
        status = "NOT expressible as O,M,I combination"

    print(f"  B{b['idx']+1:2d}: {''.join(map(str, xor))}  {status}")


# ─── 4. Orbit transitions at bridges ─────────────────────────────────────────

print(f"\n{'=' * 70}")
print("4. ORBIT TRANSITIONS AT BRIDGES")
print("=" * 70)

for b in bridges:
    cross = "CROSS" if b['sig_a'] != b['sig_b'] else "SAME"
    sig_xor = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
    sig_xor_name = mask_name(tuple(
        sig_xor[0], 0, sig_xor[2], sig_xor[2], 0, sig_xor[0]
    )) if False else ''.join(map(str, sig_xor))

    # Name the sig change using lowercase generators
    sig_change_parts = []
    if sig_xor[0]: sig_change_parts.append('o')
    if sig_xor[1]: sig_change_parts.append('m')
    if sig_xor[2]: sig_change_parts.append('i')
    sig_change = ''.join(sig_change_parts) if sig_change_parts else 'id'

    print(f"  B{b['idx']+1:2d}: orbit {''.join(map(str, b['sig_a']))} → "
          f"{''.join(map(str, b['sig_b']))}  "
          f"Δ={sig_change:>3s}  {cross}")

same_count = sum(1 for b in bridges if b['sig_a'] == b['sig_b'])
cross_count = 31 - same_count
print(f"\n  Same orbit: {same_count}/31, Cross orbit: {cross_count}/31")

# Signature change distribution
sig_changes = []
for b in bridges:
    sig_xor = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
    sig_changes.append(sig_xor)

sig_freq = Counter(sig_changes)
print(f"\n  Signature change distribution:")
for sig, count in sorted(sig_freq.items(), key=lambda x: -x[1]):
    parts = []
    if sig[0]: parts.append('o')
    if sig[1]: parts.append('m')
    if sig[2]: parts.append('i')
    name = ''.join(parts) if parts else 'id'
    print(f"    {name:>3s} {sig}: {count}×")


# ─── 5. Bridge masks vs orbit change ─────────────────────────────────────────

print(f"\n{'=' * 70}")
print("5. BRIDGE MASK vs ORBIT CHANGE")
print("   Does the bridge mask relate to which orbits it connects?")
print("=" * 70)

for b in bridges:
    xor = b['xor']
    mn = mask_name(xor)

    sig_xor = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
    parts = []
    if sig_xor[0]: parts.append('o')
    if sig_xor[1]: parts.append('m')
    if sig_xor[2]: parts.append('i')
    sig_name = ''.join(parts) if parts else 'id'

    print(f"  B{b['idx']+1:2d}: mask={mn:>10s}  orbit_change={sig_name:>3s}  "
          f"mask_is_gen={'yes' if xor in MASK_NAMES else 'NO ':>3s}")


print(f"\n{'=' * 70}")
print("BRIDGE ANALYSIS COMPLETE")
print("=" * 70)
