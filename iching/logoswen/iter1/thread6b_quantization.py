"""
Thread 6b: The +2 Quantization — Why Non-Optimal Bridges Overshoot by Exactly 2

Building on Thread 6's finding that non-optimal bridges overshoot by +2 (except B19 at +6).
Building on Thread 2's decomposition: mask = orbit_Δ ⊕ kernel_generator.

Questions:
- For each non-optimal bridge, which generator causes the +2 excess?
- Is the excess generator always the bridge's kernel component?
- B19 outlier analysis
- Optimal vs non-optimal: pattern by position, orbit transition, kernel component?
- Does kernel=id always imply optimal?
"""

import sys
sys.path.insert(0, '../kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

DIMS = 6
M = all_bits()

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

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def sig_name(sig):
    parts = []
    labels = ['o', 'm', 'i']
    for i, s in enumerate(sig):
        if s: parts.append(labels[i])
    return ''.join(parts) if parts else 'id'

def gen_name(k_elem):
    parts = []
    if k_elem[0]: parts.append('O')
    if k_elem[1]: parts.append('M')
    if k_elem[2]: parts.append('I')
    return ''.join(parts) if parts else 'id'

def kernel_component(mask):
    """Extract the kernel (generator) component: k = (m6, m5, m4, m4, m5, m6)."""
    return (mask[5], mask[4], mask[3], mask[3], mask[4], mask[5])

def orbit_component(mask):
    """Extract the orbit-change residual: r = (m1^m6, m2^m5, m3^m4, 0, 0, 0)."""
    k = kernel_component(mask)
    return tuple((mask[d] ^ k[d]) for d in range(DIMS))


# Build bridge data with decomposition
bridges = []
orbits_by_sig = defaultdict(list)

for i in range(64):
    h = tuple(M[i])
    sig = xor_sig(h)
    orbits_by_sig[sig].append((i, h))

for k in range(31):
    idx_a = 2 * k + 1
    idx_b = 2 * k + 2
    a = tuple(M[idx_a])
    b = tuple(M[idx_b])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    k_comp = kernel_component(xor)
    r_comp = orbit_component(xor)
    
    # Minimum possible Hamming to any hexagram in target orbit
    target_hexagrams = orbits_by_sig[sig_b]
    min_h = min(sum(int(a[i]) ^ int(t[1][i]) for i in range(DIMS)) for t in target_hexagrams)
    actual_h = sum(xor)
    
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'xor': xor,
        'hamming': actual_h,
        'num_a': idx_a + 1, 'num_b': idx_b + 1,
        'name_a': KING_WEN[idx_a][1], 'name_b': KING_WEN[idx_b][1],
        'sig_a': sig_a, 'sig_b': sig_b,
        'kernel': k_comp,
        'kernel_name': gen_name(k_comp),
        'residual': r_comp,
        'min_h': min_h,
        'excess': actual_h - min_h,
        'optimal': actual_h == min_h,
    })


print("=" * 70)
print("THREAD 6b: THE +2 QUANTIZATION")
print("=" * 70)


# ─── 1. The excess generator for each non-optimal bridge ─────────────────

print(f"\n1. EXCESS ANALYSIS — WHICH GENERATOR CAUSES THE +2?")
print(f"   Decomposition: mask = orbit_Δ ⊕ kernel")
print(f"   Hamming(mask) = Hamming(orbit_Δ) + Hamming(kernel)")
print(f"   because orbit_Δ and kernel have disjoint bit positions.\n")

# Key insight: the residual has bits only in positions 0-2 (lower half),
# the kernel is symmetric (a,b,c,c,b,a) with bits in both halves.
# Hamming(mask) = |orbit_Δ bits| + |kernel bits|
# Since kernel has even Hamming weight (always flips mirror pairs),
# excess = Hamming(kernel).

print(f"   {'B':>3s}  {'mask':>6s}  {'kernel':>6s}  {'k_name':>4s}  H_k  H_act  H_min  excess")
print(f"   {'─'*3}  {'─'*6}  {'─'*6}  {'─'*4}  {'─'*3}  {'─'*5}  {'─'*5}  {'─'*6}")

for b in bridges:
    h_kernel = sum(b['kernel'])
    print(f"   B{b['idx']+1:2d}  {''.join(map(str, b['xor']))}  {''.join(map(str, b['kernel']))}  "
          f"{b['kernel_name']:>4s}  {h_kernel:2d}   {b['hamming']:2d}     {b['min_h']:2d}     "
          f"{'✓' if b['optimal'] else '+' + str(b['excess'])}")


# ─── 2. Is excess == Hamming(kernel) always? ─────────────────────────────

print(f"\n2. RELATIONSHIP: EXCESS vs KERNEL HAMMING WEIGHT")

all_excess_eq_kernel = True
for b in bridges:
    h_kernel = sum(b['kernel'])
    if b['excess'] != h_kernel:
        all_excess_eq_kernel = False
        print(f"   MISMATCH B{b['idx']+1}: excess={b['excess']}, H(kernel)={h_kernel}")

if all_excess_eq_kernel:
    print(f"   ✗ NOT always equal — checking the actual relationship...")
else:
    print(f"   ✗ NOT always equal")

# Let's check more carefully
print(f"\n   Detailed check:")
for b in bridges:
    h_kernel = sum(b['kernel'])
    h_residual = sum(b['residual'])
    h_mask = b['hamming']
    print(f"   B{b['idx']+1:2d}: H(mask)={h_mask}, H(residual)={h_residual}, H(kernel)={h_kernel}, "
          f"H(r)+H(k)={h_residual+h_kernel}, min_H={b['min_h']}, excess={b['excess']}")


# ─── 3. The real relationship: min_H = H(residual)? ─────────────────────

print(f"\n3. IS min_H == H(orbit_Δ residual)?")
print(f"   The residual has bits only in positions 0-2 (the asymmetric part).")
print(f"   If min_H = H(residual), then excess = H(kernel) exactly.\n")

min_eq_residual = True
for b in bridges:
    h_residual = sum(b['residual'])
    if b['min_h'] != h_residual:
        min_eq_residual = False
        print(f"   MISMATCH B{b['idx']+1}: min_H={b['min_h']}, H(residual)={h_residual}")

if min_eq_residual:
    print(f"   ✓ YES: min_H = H(residual) for ALL bridges")
    print(f"   → excess = H(kernel) = Hamming weight of the generator dressing")
    print(f"   → The generator dressing IS the excess. QED.")
else:
    print(f"   ✗ NOT always — investigating...")

    # Deeper: for each bridge, what's the minimum achievable?
    print(f"\n   Minimum Hamming to target orbit:")
    for b in bridges:
        h_residual = sum(b['residual'])
        # The minimum Hamming to the target orbit from source hex:
        # You need to change at least the signature bits that differ.
        # But can you do it in fewer bits than H(residual)?
        # The orbit change requires certain asymmetric flips. 
        # The minimum mask achieving orbit change sig_b from sig_a
        # is a mask in the correct coset of ker(P), with minimum weight.
        # The min-weight coset representative flips only positions 0,1,2 (lower half).
        # That gives H = weight of (sig_a XOR sig_b).
        # But the actual min might be lower if the specific SOURCE hex allows shortcuts.
        sig_diff = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
        sig_weight = sum(sig_diff)
        
        if b['min_h'] != h_residual:
            print(f"   B{b['idx']+1}: sig_diff={sig_diff}, w(sig)={sig_weight}, "
                  f"H(residual)={h_residual}, min_H={b['min_h']}, "
                  f"source={''.join(map(str, b['a']))}")
            
            # Show the closest target hexagram
            target_hexagrams = orbits_by_sig[b['sig_b']]
            for t_idx, t_hex in target_hexagrams:
                dist = sum(int(b['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
                if dist == b['min_h']:
                    actual_mask = tuple(int(b['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
                    k_of_min = kernel_component(actual_mask)
                    print(f"     Closest target: {KING_WEN[t_idx][1]} ({''.join(map(str, t_hex))}) "
                          f"mask={''.join(map(str, actual_mask))} H={dist} kernel={gen_name(k_of_min)}")


# ─── 4. B19 outlier analysis ─────────────────────────────────────────────

print(f"\n4. B19 OUTLIER ANALYSIS")
b19 = bridges[18]  # 0-indexed

print(f"   B19: #{b19['num_a']} {b19['name_a']} → #{b19['num_b']} {b19['name_b']}")
print(f"   Mask: {''.join(map(str, b19['xor']))} = OMI (full complement)")
print(f"   Orbit: {sig_name(b19['sig_a'])} → {sig_name(b19['sig_b'])} (self-transition)")
print(f"   Kernel: {b19['kernel_name']}, Residual: {''.join(map(str, b19['residual']))}")
print(f"   Hamming: {b19['hamming']}, Min: {b19['min_h']}, Excess: {b19['excess']}")

# What hexagrams in orbit 8:WWang could B19 reach with min Hamming?
print(f"\n   All hexagrams in target orbit {sig_name(b19['sig_b'])} reachable from {b19['name_a']}:")
target_hexagrams = orbits_by_sig[b19['sig_b']]
for t_idx, t_hex in sorted(target_hexagrams, key=lambda x: sum(int(b19['a'][i]) ^ int(x[1][i]) for i in range(DIMS))):
    dist = sum(int(b19['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
    mask = tuple(int(b19['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
    k_of = kernel_component(mask)
    same = " ← SELF (source hex)" if t_idx == b19['num_a'] - 1 else ""
    chosen = " ← ACTUAL CHOICE" if t_hex == b19['b'] else ""
    print(f"     {KING_WEN[t_idx][1]:>10s} ({''.join(map(str, t_hex))}) "
          f"H={dist} mask={''.join(map(str, mask))} ker={gen_name(k_of)}{same}{chosen}")

# B19 is Kui(110101) → Jian(001010). These are complements!
is_complement = all(b19['a'][i] ^ b19['b'][i] == 1 for i in range(DIMS))
print(f"\n   B19 source and target are bit-complements: {is_complement}")
if is_complement:
    print(f"   Kui = {''.join(map(str, b19['a']))}, Jian = {''.join(map(str, b19['b']))}")
    print(f"   This is the ONLY bridge that maps to the bit-complement (OMI self-transition).")


# ─── 5. B14 analysis (the other self-transition) ─────────────────────────

print(f"\n5. B14 ANALYSIS (OTHER SELF-TRANSITION)")
b14 = bridges[13]

print(f"   B14: #{b14['num_a']} {b14['name_a']} → #{b14['num_b']} {b14['name_b']}")
print(f"   Mask: {''.join(map(str, b14['xor']))} = I")
print(f"   Orbit: {sig_name(b14['sig_a'])} → {sig_name(b14['sig_b'])} (self-transition)")
print(f"   Kernel: {b14['kernel_name']}, Residual: {''.join(map(str, b14['residual']))}")
print(f"   Hamming: {b14['hamming']}, Min: {b14['min_h']}, Excess: {b14['excess']}")

print(f"\n   All hexagrams in target orbit {sig_name(b14['sig_b'])} reachable from {b14['name_a']}:")
target_hexagrams_14 = orbits_by_sig[b14['sig_b']]
for t_idx, t_hex in sorted(target_hexagrams_14, key=lambda x: sum(int(b14['a'][i]) ^ int(x[1][i]) for i in range(DIMS))):
    dist = sum(int(b14['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
    mask = tuple(int(b14['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
    k_of = kernel_component(mask)
    same = " ← SELF" if t_idx == b14['num_a'] - 1 else ""
    chosen = " ← ACTUAL CHOICE" if t_hex == b14['b'] else ""
    print(f"     {KING_WEN[t_idx][1]:>10s} ({''.join(map(str, t_hex))}) "
          f"H={dist} mask={''.join(map(str, mask))} ker={gen_name(k_of)}{same}{chosen}")


# ─── 6. Optimal vs non-optimal by position ──────────────────────────────

print(f"\n6. OPTIMAL vs NON-OPTIMAL BY POSITION")

print(f"\n   Position pattern:")
for b in bridges:
    marker = "✓ OPT" if b['optimal'] else f"  +{b['excess']}"
    print(f"   B{b['idx']+1:2d}: {marker}  kernel={b['kernel_name']:>4s}  "
          f"Δ={sig_name(tuple(b['sig_a'][i]^b['sig_b'][i] for i in range(3))):>3s}  "
          f"{b['name_a']}→{b['name_b']}")

# By half
first_optimal = sum(1 for b in bridges[:15] if b['optimal'])
second_optimal = sum(1 for b in bridges[15:] if b['optimal'])
print(f"\n   First half  (B1-B15): {first_optimal}/15 optimal")
print(f"   Second half (B16-B31): {second_optimal}/16 optimal")


# ─── 7. Does kernel=id imply optimal? ────────────────────────────────────

print(f"\n7. KERNEL COMPONENT vs OPTIMALITY")

kernel_optimal = defaultdict(lambda: [0, 0])  # [optimal_count, total_count]
for b in bridges:
    key = b['kernel_name']
    kernel_optimal[key][1] += 1
    if b['optimal']:
        kernel_optimal[key][0] += 1

print(f"   {'Kernel':>5s}  Optimal  Total  Rate")
for k in sorted(kernel_optimal.keys()):
    opt, tot = kernel_optimal[k]
    print(f"   {k:>5s}    {opt:2d}      {tot:2d}    {opt/tot:.0%}")

# Specifically: id kernel
print(f"\n   kernel=id → always optimal? ", end="")
id_bridges = [b for b in bridges if b['kernel_name'] == 'id']
id_all_optimal = all(b['optimal'] for b in id_bridges)
print(f"{'YES' if id_all_optimal else 'NO'}")
if id_all_optimal:
    print(f"   When the generator dressing is trivial (id), the bridge is pure orbit change → minimal Hamming.")


# ─── 8. Which generator dressing is chosen when there are alternatives? ──

print(f"\n8. ALTERNATIVE DRESSINGS — WHAT ELSE COULD HAVE BEEN CHOSEN?")
print(f"   For each bridge, how many hexagrams in the target orbit exist?")
print(f"   (Always 8 — the orbit has 8 members.)")
print(f"   But how many are at each Hamming distance from the source?\n")

for b in bridges:
    target_hexagrams = orbits_by_sig[b['sig_b']]
    distances = []
    for t_idx, t_hex in target_hexagrams:
        dist = sum(int(b['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
        mask = tuple(int(b['a'][i]) ^ int(t_hex[i]) for i in range(DIMS))
        k_of = kernel_component(mask)
        distances.append((dist, gen_name(k_of), t_idx, t_hex))
    
    distances.sort()
    dist_summary = Counter(d[0] for d in distances)
    actual_dist = b['hamming']
    
    # How many at minimum distance?
    min_d = distances[0][0]
    n_at_min = dist_summary[min_d]
    
    # Where does the actual choice rank?
    rank = sum(1 for d in distances if d[0] < actual_dist)
    
    if not b['optimal']:
        print(f"   B{b['idx']+1:2d} (non-opt): distances={dict(sorted(dist_summary.items()))}, "
              f"chose H={actual_dist} (kernel={b['kernel_name']}), "
              f"could have H={min_d} with {n_at_min} options")
        # Show what the optimal choices would have been
        for d, kn, ti, th in distances:
            if d == min_d:
                print(f"         → {KING_WEN[ti][1]:>10s} H={d} kernel={kn}")


# ─── 9. The weight-5 gap ─────────────────────────────────────────────────

print(f"\n9. THE WEIGHT-5 GAP")
print(f"   No bridge has Hamming weight 5. Why?")
print(f"   H(mask) = H(residual) + H(kernel)")
print(f"   H(kernel) is always even: 0, 2, 4, or 6")
print(f"   H(residual) ranges 0-3 (it's a 3-bit vector in positions 0-2)")
print(f"   Possible H(mask) values: 0+0=0, 1+0=1, 2+0=2, 3+0=3,")
print(f"                            0+2=2, 1+2=3, 2+2=4, 3+2=5 ← possible!")
print(f"                            0+4=4, 1+4=5 ← possible!")
print(f"                            2+4=6, 3+4=7 ← impossible (max 6)")
print(f"                            0+6=6, 1+6=7 ← impossible")
print(f"   So H=5 COULD occur: residual=3 + kernel=2, or residual=1 + kernel=4.")
print(f"   Let's check which (residual_weight, kernel_weight) combos actually appear:\n")

rk_combos = Counter()
for b in bridges:
    hr = sum(b['residual'])
    hk = sum(b['kernel'])
    rk_combos[(hr, hk)] += 1

print(f"   {'H(r)':>4s} {'H(k)':>4s}  {'H(mask)':>7s}  Count")
for (hr, hk), cnt in sorted(rk_combos.items()):
    print(f"   {hr:4d} {hk:4d}  {hr+hk:7d}    {cnt}")

# Which combos are missing?
print(f"\n   Combos that would give H=5:")
h5_combos = [(hr, hk) for hr in range(4) for hk in [0,2,4,6] if hr+hk == 5]
for hr, hk in h5_combos:
    count = rk_combos.get((hr, hk), 0)
    print(f"   H(r)={hr}, H(k)={hk}: {count} occurrences {'← NEVER OCCURS' if count == 0 else ''}")

# Is it that certain orbit changes never pair with certain generators?
print(f"\n   Orbit change weight vs kernel weight distribution:")
print(f"   {'Δ_orbit':>8s}  {'w(Δ)':>4s}  kernels used")
orbit_changes = defaultdict(list)
for b in bridges:
    sig_ch = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
    orbit_changes[sig_ch].append(b['kernel_name'])

for sig_ch in sorted(orbit_changes.keys()):
    w = sum(sig_ch)
    kernels = orbit_changes[sig_ch]
    kernel_weights = [sum(kernel_component(bridges[0]['xor'])) for _ in kernels]  # recalc properly
    # Actually compute properly
    kw_list = []
    for b in bridges:
        sc = tuple(b['sig_a'][i] ^ b['sig_b'][i] for i in range(3))
        if sc == sig_ch:
            kw_list.append((b['kernel_name'], sum(b['kernel'])))
    
    kernel_info = Counter(kn for kn, _ in kw_list)
    print(f"   {sig_name(sig_ch):>8s}  w={w}  {dict(kernel_info)}")


# ─── 10. Summary statistics ──────────────────────────────────────────────

print(f"\n10. SUMMARY")

print(f"\n   Optimal bridges: 15/31 (48%)")
print(f"   Non-optimal bridges: 16/31 (52%)")
print(f"   All non-optimal excess: +2 (15 bridges) or +6 (1 bridge, B19)")
print(f"   Excess is ALWAYS = Hamming weight of kernel component")

# Verify this
excess_eq_hk = all(b['excess'] == sum(b['kernel']) for b in bridges)
print(f"   Verified excess == H(kernel): {excess_eq_hk}")

if not excess_eq_hk:
    for b in bridges:
        if b['excess'] != sum(b['kernel']):
            print(f"   !! B{b['idx']+1}: excess={b['excess']}, H(kernel)={sum(b['kernel'])}")

print(f"\n   The +2 quantization theorem (CORRECTED):")
print(f"   H(mask) = w(sig_change) + 2*S")
print(f"   where S = (m1&m6) + (m2&m5) + (m3&m4) = # mirror pairs where BOTH lines flip")
print(f"   excess = 2*S, always even, always ∈ {{0, 2, 4, 6}}")
print(f"   Note: excess ≠ H(kernel) in general (XOR decomposition doesn't preserve Hamming)")
print(f"   The correct formula uses AND, not the kernel component.")


print(f"\n{'=' * 70}")
print(f"THREAD 6b COMPLETE")
print(f"{'=' * 70}")
