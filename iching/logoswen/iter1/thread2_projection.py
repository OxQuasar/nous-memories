"""
Thread 2: Bridge-to-Orbit Projection

Questions:
- Can we predict the orbit transition (3-bit signature change) from the bridge mask (6-bit XOR)?
- Is the projection a function of the mask alone, or does it depend on the starting hexagram?
- If it's a function, what is the projection formula?
- If not, what determines the outcome?
"""

import sys
sys.path.insert(0, '/home/skipper/code/nous/kingwen')

import numpy as np
from collections import defaultdict, Counter
from sequence import KING_WEN, all_bits

DIMS = 6
M = np.array(all_bits())

GEN_BITS = {
    'O': (1, 0, 0, 0, 0, 1),
    'M': (0, 1, 0, 0, 1, 0),
    'I': (0, 0, 1, 1, 0, 0),
}

def xor_sig(h):
    """XOR signature (orbit) of a hexagram: (l1^l6, l2^l5, l3^l4)."""
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def sig_name(sig):
    parts = []
    if sig[0]: parts.append('o')
    if sig[1]: parts.append('m')
    if sig[2]: parts.append('i')
    return ''.join(parts) if parts else 'id'

# ─── Build bridge data ─────────────────────────────────────────────────────
bridges = []
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    xor = tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    sig_change = tuple(sig_a[i] ^ sig_b[i] for i in range(3))
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'xor': xor,
        'sig_a': sig_a, 'sig_b': sig_b,
        'sig_change': sig_change,
    })

print("=" * 70)
print("THREAD 2: BRIDGE MASK → ORBIT TRANSITION PROJECTION")
print("=" * 70)

# ─── 1. Is mask → sig_change a function? ───────────────────────────────────
print("\n1. IS MASK → ORBIT CHANGE A FUNCTION?")
print("-" * 50)

mask_to_sig_changes = defaultdict(set)
for b in bridges:
    mask_to_sig_changes[b['xor']].add(b['sig_change'])

ambiguous = {m: sigs for m, sigs in mask_to_sig_changes.items() if len(sigs) > 1}
deterministic = {m: list(sigs)[0] for m, sigs in mask_to_sig_changes.items() if len(sigs) == 1}

print(f"  Unique masks: {len(mask_to_sig_changes)}")
print(f"  Deterministic (1 sig change per mask): {len(deterministic)}")
print(f"  Ambiguous (>1 sig change per mask): {len(ambiguous)}")

if ambiguous:
    print(f"\n  AMBIGUOUS MASKS:")
    for mask, sigs in sorted(ambiguous.items()):
        mask_str = ''.join(map(str, mask))
        sig_strs = [sig_name(s) for s in sigs]
        print(f"    mask={mask_str}: orbit changes = {sig_strs}")
        # Show instances
        for b in bridges:
            if b['xor'] == mask:
                print(f"      B{b['idx']+1}: "
                      f"{''.join(map(str, b['sig_a']))} → {''.join(map(str, b['sig_b']))}  "
                      f"Δ={sig_name(b['sig_change'])}  "
                      f"from hex {''.join(map(str, b['a']))}")

if not ambiguous:
    print(f"\n  → MASK DETERMINES ORBIT CHANGE — it's a function!")
else:
    print(f"\n  → MASK DOES NOT DETERMINE ORBIT CHANGE — context matters")

# ─── 2. Derive the projection formula ──────────────────────────────────────
print(f"\n2. PROJECTION FORMULA ANALYSIS")
print("-" * 50)

# The signature is (l1^l6, l2^l5, l3^l4)
# If we XOR hexagram h with mask m to get h' = h⊕m, then:
#   sig(h') = (h1'^h6', h2'^h5', h3'^h4')
#           = ((h1⊕m1)^(h6⊕m6), (h2⊕m2)^(h5⊕m5), (h3⊕m3)^(h4⊕m4))
#
# sig_change = sig(h) ⊕ sig(h')
#   component k: (h_i ⊕ h_j) ⊕ ((h_i⊕m_i) ⊕ (h_j⊕m_j))
#              = (h_i ⊕ h_j) ⊕ (h_i ⊕ m_i ⊕ h_j ⊕ m_j)
#              = m_i ⊕ m_j
#
# So sig_change[k] = m_i ⊕ m_j for mirror pair (i,j)!
# This is INDEPENDENT of h — it's purely a function of the mask.

print("  Theoretical derivation:")
print("  sig_change[k] = m_i ⊕ m_j  for mirror pair (i,j)")
print("  where pairs are: (0,5), (1,4), (2,3)")
print()
print("  This means:")
print("    Δo = m₁ ⊕ m₆  (outer pair)")
print("    Δm = m₂ ⊕ m₅  (middle pair)")
print("    Δi = m₃ ⊕ m₄  (inner pair)")
print()
print("  The projection is LINEAR over GF(2), and depends ONLY on the mask.")

# Verify empirically
print(f"\n  Empirical verification:")
all_correct = True
for b in bridges:
    m = b['xor']
    predicted = (m[0] ^ m[5], m[1] ^ m[4], m[2] ^ m[3])
    actual = b['sig_change']
    ok = predicted == actual
    if not ok:
        all_correct = False
    print(f"    B{b['idx']+1}: mask={''.join(map(str, m))}  "
          f"predicted={sig_name(predicted)}  actual={sig_name(actual)}  "
          f"{'✓' if ok else '✗ MISMATCH'}")

print(f"\n  All predictions correct: {all_correct}")

# ─── 3. The projection as a linear map ─────────────────────────────────────
print(f"\n3. THE PROJECTION AS A LINEAR MAP")
print("-" * 50)

print("  P: Z₂⁶ → Z₂³")
print("  P(m₁,m₂,m₃,m₄,m₅,m₆) = (m₁⊕m₆, m₂⊕m₅, m₃⊕m₄)")
print()
print("  Matrix form:")
print("        m₁ m₂ m₃ m₄ m₅ m₆")
print("  Δo: [ 1  0  0  0  0  1 ]")
print("  Δm: [ 0  1  0  0  1  0 ]")
print("  Δi: [ 0  0  1  1  0  0 ]")
print()
print("  Note: The rows of P are exactly the generators O, M, I!")
print("  P = [O; M; I] as a 3×6 matrix")
print()
print("  Kernel of P: masks that DON'T change the orbit")

# Compute kernel of P
# Kernel: m₁=m₆, m₂=m₅, m₃=m₄
# So kernel elements are (a,b,c,c,b,a) for a,b,c ∈ {0,1}
kernel = []
for a in range(2):
    for b in range(2):
        for c in range(2):
            kernel.append((a, b, c, c, b, a))

print(f"  Kernel size: {len(kernel)} (= 2³, as expected for rank-3 map from Z₂⁶)")
print(f"  Kernel elements (symmetric masks):")
for k in kernel:
    print(f"    {''.join(map(str, k))}")

print(f"\n  The kernel is exactly the standard generator group!")
print(f"  ker(P) = <O, M, I> = the 8-element subgroup of mirror-pair masks")

# Verify
from itertools import combinations
std_group = set()
std_group.add((0,0,0,0,0,0))
for g in GEN_BITS.values():
    new = set()
    for elem in std_group:
        product = tuple((elem[d] ^ g[d]) for d in range(DIMS))
        new.add(product)
    std_group |= new

kernel_set = set(kernel)
print(f"  Kernel == Standard group: {kernel_set == std_group}")

# ─── 4. Fiber analysis: what maps to each orbit change? ────────────────────
print(f"\n4. FIBER ANALYSIS: PREIMAGES OF EACH ORBIT CHANGE")
print("-" * 50)

# For each possible orbit change (3-bit vector), how many masks map to it?
# Each fiber is a coset of the kernel, so each has exactly 8 elements
for sig in sorted(set(tuple(x) for x in np.ndindex(2,2,2))):
    fiber = []
    for elem in sorted(set(tuple(int(x) for x in e) for e in 
                           [tuple((i >> (5-d)) & 1 for d in range(6)) for i in range(64)])):
        projected = (elem[0] ^ elem[5], elem[1] ^ elem[4], elem[2] ^ elem[3])
        if projected == sig:
            fiber.append(elem)
    
    sn = sig_name(sig)
    # Which of these are actual bridge masks?
    used = [f for f in fiber if f in set(bridge_masks for bridge_masks in [b['xor'] for b in bridges])]
    bridge_mask_set = set(b['xor'] for b in bridges)
    actual_used = [f for f in fiber if f in bridge_mask_set]
    
    print(f"  Δ={sn:>3s} ({','.join(map(str,sig))}): "
          f"|fiber|={len(fiber)}, actual bridge masks={len(actual_used)}")
    for f in fiber:
        marker = " ← USED" if f in bridge_mask_set else ""
        print(f"    {''.join(map(str, f))}{marker}")

# ─── 5. What determines WHICH mask from the fiber is chosen? ───────────────
print(f"\n5. WITHIN-FIBER SELECTION: WHY THIS MASK?")
print("-" * 50)
print("  For bridges with the same orbit change, what determines the specific mask?")
print("  Answer: The mask encodes BOTH the orbit change AND the within-orbit movement.")
print()
print("  Decomposition: mask = orbit_change_component ⊕ within_orbit_component")
print("  where within_orbit_component ∈ ker(P) = standard generator group")
print()

for b in bridges:
    m = b['xor']
    sig_ch = b['sig_change']
    
    # Find the kernel component: the unique element of ker(P) such that
    # m = fiber_rep ⊕ kernel_elem
    # Since kernel elements are (a,b,c,c,b,a), the kernel component is:
    # For each mirror pair (i,j): both get the same value
    # The "within-orbit" part: for pair (i,j), it's m[i] AND m[j] when they agree
    # Actually: decompose m into symmetric part + antisymmetric part
    # Symmetric: s_i = s_j for each pair → this is in kernel
    # The kernel component for pair (i,j) is (m[i]&m[j]) repeated
    # Wait, let me think...
    # m = k ⊕ r where k ∈ ker(P) and r is a coset representative
    # k has form (a,b,c,c,b,a). We need m ⊕ k to be a fixed coset rep.
    # Choose minimal coset rep: for each pair, if m[i]=m[j], pair contributes (0,0);
    # if m[i]≠m[j], we need to break the tie.
    # Natural choice: for pair (i,j) with i<j, coset rep has bit in position i, not j.
    
    # Compute kernel component
    # For each pair (i,j): if m[i]==m[j], kernel contribution is (m[i],m[j])
    # if m[i]!=m[j], we need to pick: either (0,0)→kernel, (1,1)→kernel
    # If m[i]=1,m[j]=0: kernel=(0,0), residual=(1,0) or kernel=(1,1), residual=(0,1)
    
    # Let's just express: m = (m₁,m₂,m₃,m₄,m₅,m₆)
    # symmetric part: s = ((m₁∧m₆), (m₂∧m₅), (m₃∧m₄), (m₃∧m₄), (m₂∧m₅), (m₁∧m₆))
    # But this isn't right either. Let me just find the kernel coset.
    
    # Find which kernel element k satisfies m⊕k is in a canonical coset rep set
    for k in kernel:
        residual = tuple((m[d] ^ k[d]) for d in range(DIMS))
        # Residual should project to the same sig_change as m
        res_proj = (residual[0] ^ residual[5], residual[1] ^ residual[4], residual[2] ^ residual[3])
        assert res_proj == sig_ch
    
    # The kernel element is: match m's symmetric part
    # For pair (i,j): kernel bit = m[j] (the "reflection" side)
    # Then residual[j] = m[j]^m[j] = 0, residual[i] = m[i]^m[j] = sig_change bit
    k_elem = (m[5], m[4], m[3], m[3], m[4], m[5])
    residual = tuple((m[d] ^ k_elem[d]) for d in range(DIMS))
    
    # Name the kernel element
    k_parts = []
    if k_elem[0]: k_parts.append('O')
    if k_elem[1]: k_parts.append('M')
    if k_elem[2]: k_parts.append('I')
    k_name = ''.join(k_parts) if k_parts else 'id'
    
    print(f"  B{b['idx']+1:2d}: mask={''.join(map(str, m))}  "
          f"= orbit_Δ {''.join(map(str, residual))} ⊕ kernel {''.join(map(str, k_elem))} ({k_name})")

# ─── 6. The decomposition's meaning ────────────────────────────────────────
print(f"\n6. INTERPRETATION OF DECOMPOSITION")
print("-" * 50)

print("  Every bridge mask m decomposes uniquely as:")
print("    m = r ⊕ k")
print("  where:")
print("    r = (Δo,Δm,Δi,0,0,0) — the 'orbit change' part (bits only in positions 1-3)")
print("    k = (m₆,m₅,m₄,m₄,m₅,m₆) — a standard generator mask")
print()
print("  Choosing k = (m₆,m₅,m₄,m₄,m₅,m₆) gives residual r = (m₁⊕m₆, m₂⊕m₅, m₃⊕m₄, 0, 0, 0)")
print("  which has the orbit change in positions 1-3 and zeros in positions 4-6.")
print()
print("  This means: a bridge does TWO things simultaneously:")
print("    1. Changes the orbit (via the antisymmetric part)")  
print("    2. Applies a standard generator transformation (via the symmetric part)")
print()
print("  The 'free' choice at each bridge is which generator to compose with the orbit change.")

# ─── 7. Distribution of kernel components ──────────────────────────────────
print(f"\n7. DISTRIBUTION OF KERNEL (GENERATOR) COMPONENTS")
print("-" * 50)

kernel_components = []
for b in bridges:
    m = b['xor']
    k_elem = (m[5], m[4], m[3], m[3], m[4], m[5])
    k_parts = []
    if k_elem[0]: k_parts.append('O')
    if k_elem[1]: k_parts.append('M')
    if k_elem[2]: k_parts.append('I')
    k_name = ''.join(k_parts) if k_parts else 'id'
    kernel_components.append(k_name)

kernel_freq = Counter(kernel_components)
print(f"  Kernel component distribution across 31 bridges:")
for k, count in sorted(kernel_freq.items(), key=lambda x: -x[1]):
    print(f"    {k:>4s}: {count}× ({''.join('█' * count)})")

# ─── 8. Full mask table ────────────────────────────────────────────────────
print(f"\n8. COMPLETE BRIDGE DECOMPOSITION TABLE")
print("-" * 50)
print(f"  {'B':>3s}  {'mask':>6s}  {'orbit_Δ':>7s}  {'kernel':>6s}  {'gen':>4s}  {'orbit_change':>12s}")
print(f"  {'─'*3}  {'─'*6}  {'─'*7}  {'─'*6}  {'─'*4}  {'─'*12}")

for b in bridges:
    m = b['xor']
    k_elem = (m[5], m[4], m[3], m[3], m[4], m[5])
    residual = tuple((m[d] ^ k_elem[d]) for d in range(DIMS))
    
    k_parts = []
    if k_elem[0]: k_parts.append('O')
    if k_elem[1]: k_parts.append('M')
    if k_elem[2]: k_parts.append('I')
    k_name = ''.join(k_parts) if k_parts else 'id'
    
    print(f"  B{b['idx']+1:2d}  {''.join(map(str, m))}   {''.join(map(str, residual))}  "
          f"{''.join(map(str, k_elem))}  {k_name:>4s}  "
          f"{''.join(map(str, b['sig_a']))}→{''.join(map(str, b['sig_b']))}")

# ─── 9. Cross-check with ALL possible hex→hex transitions ──────────────────
print(f"\n9. UNIVERSAL PROJECTION VERIFICATION")
print("-" * 50)
print("  Verifying P(m) = sig_change for ALL 64×63 possible transitions...")

all_h = all_bits()
violations = 0
for i in range(64):
    for j in range(64):
        if i == j:
            continue
        h1 = all_h[i]
        h2 = all_h[j]
        mask = tuple(h1[d] ^ h2[d] for d in range(DIMS))
        sig1 = xor_sig(h1)
        sig2 = xor_sig(h2)
        actual_change = tuple(sig1[k] ^ sig2[k] for k in range(3))
        predicted = (mask[0] ^ mask[5], mask[1] ^ mask[4], mask[2] ^ mask[3])
        if predicted != actual_change:
            violations += 1

print(f"  Violations: {violations} / {64*63}")
if violations == 0:
    print(f"  → The projection P holds UNIVERSALLY for any hex→hex transition")
    print(f"  → This is a theorem, not an empirical finding")

print(f"\n{'=' * 70}")
print("THREAD 2 COMPLETE")
print("=" * 70)
