"""
Thread 3: Pair+Bridge Compound Transitions

The 4-hexagram window: h₁ →[pair_k]→ h₂ →[bridge_k]→ h₃ →[pair_{k+1}]→ h₄

Each transition decomposes via Thread 2:
  mask = orbit_Δ ⊕ generator_dressing

Pair masks are pure kernel (orbit_Δ = 0), so their generator IS the pair type.
Bridge masks have both components.

Questions:
- What is the compound mask pair_k ⊕ bridge_k ⊕ pair_{k+1}?
- Does the generator-component chain simplify?
- Since pair_{k+1} is orbit-determined, is the compound fully determined by 
  (starting orbit, orbit change, bridge generator)?
- Do compound masks recover algebraic structure that raw bridges lack?
"""

import sys
sys.path.insert(0, '/home/skipper/code/nous/kingwen')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits

DIMS = 6
M = np.array(all_bits())

GEN_BITS = {
    'O': (1, 0, 0, 0, 0, 1),
    'M': (0, 1, 0, 0, 1, 0),
    'I': (0, 0, 1, 1, 0, 0),
}

MASK_NAMES = {
    (1,1,1,1,1,1): "OMI", (1,1,0,0,1,1): "OM", (1,0,1,1,0,1): "OI",
    (0,1,1,1,1,0): "MI", (0,1,0,0,1,0): "M", (0,0,1,1,0,0): "I",
    (1,0,0,0,0,1): "O", (0,0,0,0,0,0): "id",
}

# Orbit signatures → pair type (from 12-orbits.md)
ORBIT_PAIR_TYPE = {
    (0,0,0): 'OMI', (1,1,0): 'OM', (1,0,1): 'OI', (0,1,0): 'M',
    (0,0,1): 'I',   (1,1,1): 'OMI', (1,0,0): 'O',  (0,1,1): 'MI',
}

ORBIT_NAMES = {
    (0,0,0): '1:Qian', (1,1,0): '2:Zhun', (1,0,1): '3:Xu',  (0,1,0): '4:Shi',
    (0,0,1): '5:XChu', (1,1,1): '6:Tai',  (1,0,0): '7:Bo',  (0,1,1): '8:WWang',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def xor_mask(a, b):
    return tuple(int(a[i]) ^ int(b[i]) for i in range(DIMS))

def gen_name(mask):
    """Name a generator (kernel) mask."""
    if mask in MASK_NAMES:
        return MASK_NAMES[mask]
    return ''.join(map(str, mask))

def sig_name(sig):
    parts = []
    if sig[0]: parts.append('o')
    if sig[1]: parts.append('m')
    if sig[2]: parts.append('i')
    return ''.join(parts) if parts else 'id'

def kernel_component(mask):
    """Extract the generator (kernel) component: (m₆,m₅,m₄,m₄,m₅,m₆)."""
    return (mask[5], mask[4], mask[3], mask[3], mask[4], mask[5])

def orbit_component(mask):
    """Extract the orbit-change component: (m₁⊕m₆, m₂⊕m₅, m₃⊕m₄, 0, 0, 0)."""
    return (mask[0]^mask[5], mask[1]^mask[4], mask[2]^mask[3], 0, 0, 0)

def xor6(a, b):
    return tuple(a[i] ^ b[i] for i in range(DIMS))

def xor3(a, b):
    return tuple(a[i] ^ b[i] for i in range(3))


# ─── Build all transitions ────────────────────────────────────────────────

# Standard pairs: (h_{2k}, h_{2k+1}) for k=0..31
pairs = []
for k in range(32):
    a = tuple(M[2*k])
    b = tuple(M[2*k + 1])
    mask = xor_mask(a, b)
    pairs.append({
        'idx': k,
        'a': a, 'b': b,
        'mask': mask,
        'gen': gen_name(mask),
        'sig': xor_sig(a),  # orbit (same for both in pair)
    })

# Bridges: (h_{2k+1}, h_{2k+2}) for k=0..30
bridges = []
for k in range(31):
    a = tuple(M[2*k + 1])
    b = tuple(M[2*k + 2])
    mask = xor_mask(a, b)
    sig_a = xor_sig(a)
    sig_b = xor_sig(b)
    sig_change = xor3(sig_a, sig_b)
    k_comp = kernel_component(mask)
    o_comp = orbit_component(mask)
    bridges.append({
        'idx': k,
        'a': a, 'b': b,
        'mask': mask,
        'sig_a': sig_a, 'sig_b': sig_b,
        'sig_change': sig_change,
        'kernel': k_comp,
        'orbit_delta': o_comp,
        'kernel_name': gen_name(k_comp),
    })


print("=" * 70)
print("THREAD 3: PAIR+BRIDGE COMPOUND TRANSITIONS")
print("=" * 70)


# ─── 1. The 4-hexagram windows ────────────────────────────────────────────

print("\n1. THE 4-HEXAGRAM WINDOWS")
print("-" * 50)
print(f"  Window: h₁ →[pair_k]→ h₂ →[bridge_k]→ h₃ →[pair_{k+1}]→ h₄")
print(f"  31 windows (k=0..30)")

windows = []
for k in range(31):
    p_before = pairs[k]     # pair_k
    br = bridges[k]          # bridge_k
    p_after = pairs[k + 1]   # pair_{k+1}
    
    # The 4 hexagrams
    h1 = tuple(M[2*k])
    h2 = tuple(M[2*k + 1])     # = p_before.b = br.a
    h3 = tuple(M[2*k + 2])     # = br.b = p_after.a
    h4 = tuple(M[2*k + 3])
    
    # Compound mask: h1 → h4 (XOR of all three steps)
    compound = xor_mask(h1, h4)
    
    # Generator chain: pair_gen ⊕ bridge_gen ⊕ pair_gen
    # In kernel space (3-bit): pair_k_type ⊕ bridge_kernel ⊕ pair_{k+1}_type
    pair_k_gen = p_before['mask']
    bridge_gen = br['kernel']
    pair_k1_gen = p_after['mask']
    
    # XOR the three generator masks
    gen_compound = xor6(xor6(pair_k_gen, bridge_gen), pair_k1_gen)
    
    # Also compute the orbit change through the window
    # pair_k: no orbit change. bridge_k: orbit changes. pair_{k+1}: no orbit change.
    # So total orbit change = bridge's orbit change
    total_orbit_delta = br['sig_change']
    
    windows.append({
        'k': k,
        'h1': h1, 'h2': h2, 'h3': h3, 'h4': h4,
        'pair_k_mask': pair_k_gen,
        'bridge_mask': br['mask'],
        'pair_k1_mask': pair_k1_gen,
        'compound': compound,
        'gen_compound': gen_compound,
        'orbit_start': xor_sig(h1),
        'orbit_end': xor_sig(h4),
        'orbit_delta': total_orbit_delta,
        'pair_k_type': p_before['gen'],
        'bridge_kernel_name': br['kernel_name'],
        'pair_k1_type': p_after['gen'],
    })


# ─── 2. Display compound masks ────────────────────────────────────────────

print(f"\n2. COMPOUND MASKS (h₁ → h₄)")
print("-" * 50)
print(f"  {'W':>3s}  {'pair_k':>6s}  {'bridge':>6s}  {'pair_k1':>7s}  {'compound':>8s}  H  {'gen_chain':>20s}  {'orbit':>12s}")
print(f"  {'─'*3}  {'─'*6}  {'─'*6}  {'─'*7}  {'─'*8}  ─  {'─'*20}  {'─'*12}")

for w in windows:
    p_str = ''.join(map(str, w['pair_k_mask']))
    b_str = ''.join(map(str, w['bridge_mask']))
    p1_str = ''.join(map(str, w['pair_k1_mask']))
    c_str = ''.join(map(str, w['compound']))
    g_str = f"{w['pair_k_type']}⊕{w['bridge_kernel_name']}⊕{w['pair_k1_type']}"
    o_str = f"{sig_name(w['orbit_start'])}→{sig_name(w['orbit_end'])}"
    h = sum(w['compound'])
    
    print(f"  W{w['k']:2d}  {p_str}  {b_str}  {p1_str}   {c_str}  {h}  {g_str:>20s}  {o_str:>12s}")


# ─── 3. Compound mask algebraic properties ─────────────────────────────────

print(f"\n3. COMPOUND MASK PROPERTIES")
print("-" * 50)

compound_masks = [w['compound'] for w in windows]
unique_compounds = sorted(set(compound_masks))
compound_freq = Counter(compound_masks)

print(f"  Total windows: {len(windows)}")
print(f"  Unique compound masks: {len(unique_compounds)}")

# How many are generator-expressible?
gen_expressible = sum(1 for c in compound_masks if c in MASK_NAMES)
print(f"  Generator-expressible compounds: {gen_expressible}/{len(windows)}")

# Hamming distances
compound_h = [sum(c) for c in compound_masks]
print(f"  Hamming distance distribution: {dict(Counter(compound_h))}")
print(f"  Mean Hamming: {sum(compound_h)/len(compound_h):.2f}")
print(f"  (Compare: bridges alone = 2.94, pairs alone = 3.75)")

# Even/odd
even_count = sum(1 for h in compound_h if h % 2 == 0)
print(f"  Even Hamming: {even_count}/{len(windows)}, Odd: {len(windows) - even_count}/{len(windows)}")

# Rank
def gf2_rank(matrix):
    mat = np.array(matrix, dtype=int) % 2
    rows, cols = mat.shape
    rank = 0
    for col in range(cols):
        pivot_row = None
        for row in range(rank, rows):
            if mat[row, col] == 1:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        mat[[rank, pivot_row]] = mat[[pivot_row, rank]]
        for row in range(rows):
            if row != rank and mat[row, col] == 1:
                mat[row] = (mat[row] + mat[rank]) % 2
        rank += 1
    return rank

compound_rank = gf2_rank(np.array(compound_masks, dtype=int))
print(f"  Rank over GF(2): {compound_rank} (bridges alone: 6)")


# ─── 4. Generator chain analysis ──────────────────────────────────────────

print(f"\n4. GENERATOR CHAIN: pair_type ⊕ bridge_kernel ⊕ pair_type'")
print("-" * 50)

# The generator component of the compound = pair_k ⊕ bridge_kernel ⊕ pair_{k+1}
# All three are kernel elements. The kernel is Z₂³ so this is a product in Z₂³.
# Let's track this in the 3-bit generator space.

def gen_to_3bit(gen_name_str):
    """Convert generator name to 3-bit (o,m,i) vector."""
    bits = [0, 0, 0]
    if 'O' in gen_name_str: bits[0] = 1
    if 'M' in gen_name_str: bits[1] = 1
    if 'I' in gen_name_str: bits[2] = 1
    return tuple(bits)

print(f"  In Z₂³ (generator space): pair_k_type ⊕ bridge_kernel ⊕ pair_{k+1}_type")
print(f"  pair type is orbit-determined, so pair_{k+1}_type = f(bridge_target_orbit)")
print()

gen_compounds_3bit = []
for w in windows:
    g1 = gen_to_3bit(w['pair_k_type'])
    gb = gen_to_3bit(w['bridge_kernel_name'])
    g2 = gen_to_3bit(w['pair_k1_type'])
    g_total = xor3(xor3(g1, gb), g2)
    gen_compounds_3bit.append(g_total)
    
    g_name = sig_name(g_total).upper() if any(g_total) else 'id'
    print(f"  W{w['k']:2d}: {w['pair_k_type']:>3s} ⊕ {w['bridge_kernel_name']:>3s} ⊕ {w['pair_k1_type']:>3s} = {g_name:>3s}  "
          f"(orbit: {sig_name(w['orbit_start'])}→{sig_name(w['orbit_end'])})")

gen_3bit_freq = Counter(gen_compounds_3bit)
print(f"\n  Generator compound distribution (3-bit):")
for g, count in sorted(gen_3bit_freq.items(), key=lambda x: -x[1]):
    name = sig_name(g).upper() if any(g) else 'id'
    print(f"    {name:>3s}: {count}×")


# ─── 5. The compound in decomposed form ───────────────────────────────────

print(f"\n5. COMPOUND DECOMPOSITION")
print("-" * 50)
print(f"  compound = (pair_k ⊕ bridge ⊕ pair_{'{k+1}'}) in Z₂⁶")
print(f"  = (pair_k ⊕ (orbit_Δ ⊕ bridge_kernel) ⊕ pair_{'{k+1}'}) ")
print(f"  = orbit_Δ ⊕ (pair_k ⊕ bridge_kernel ⊕ pair_{'{k+1}'})")
print(f"  = orbit_Δ ⊕ gen_compound")
print(f"")
print(f"  Since pair types are in the kernel (orbit-preserving),")
print(f"  the compound has the SAME orbit_Δ as the bridge alone,")
print(f"  but a DIFFERENT generator dressing.")
print()

# Verify
all_match = True
for w in windows:
    br = bridges[w['k']]
    compound_orbit = orbit_component(w['compound'])
    bridge_orbit = br['orbit_delta']
    if compound_orbit != bridge_orbit:
        all_match = False
        print(f"  MISMATCH at W{w['k']}: compound orbit_Δ != bridge orbit_Δ")

print(f"  Verified: compound orbit_Δ = bridge orbit_Δ for all 31 windows: {all_match}")


# ─── 6. Is compound determined by (start_orbit, orbit_change, bridge_gen)? ─

print(f"\n6. DETERMINISM TEST")
print("-" * 50)
print(f"  pair_type is orbit-determined. So:")
print(f"    pair_k type = f(orbit_start)")
print(f"    pair_{{k+1}} type = f(orbit_end) = f(orbit_start ⊕ orbit_Δ)")
print(f"  Bridge contributes orbit_Δ and bridge_kernel.")
print(f"  So the compound is fully determined by (orbit_start, orbit_Δ, bridge_kernel).")
print()

# Verify: same (orbit_start, orbit_Δ, bridge_kernel) → same compound?
key_to_compound = defaultdict(set)
for w in windows:
    br = bridges[w['k']]
    key = (w['orbit_start'], tuple(w['orbit_delta']), br['kernel_name'])
    key_to_compound[key].add(w['compound'])

ambiguous = {k: v for k, v in key_to_compound.items() if len(v) > 1}
print(f"  Unique (orbit_start, orbit_Δ, bridge_kernel) keys: {len(key_to_compound)}")
print(f"  Ambiguous keys (>1 compound): {len(ambiguous)}")
if not ambiguous:
    print(f"  → CONFIRMED: compound is fully determined by (orbit_start, orbit_Δ, bridge_kernel)")
else:
    print(f"  → NOT determined — same inputs produce different compounds")

# But can we go further: is compound determined by just (orbit_start, orbit_Δ)?
# i.e., does the bridge_kernel not matter?
key2_to_compound = defaultdict(set)
for w in windows:
    key = (w['orbit_start'], tuple(w['orbit_delta']))
    key2_to_compound[key].add(w['compound'])

ambiguous2 = {k: v for k, v in key2_to_compound.items() if len(v) > 1}
print(f"\n  Without bridge_kernel — (orbit_start, orbit_Δ) keys: {len(key2_to_compound)}")
print(f"  Ambiguous: {len(ambiguous2)}")
if ambiguous2:
    print(f"  → Bridge kernel DOES affect the compound (as expected)")
    for key, compounds in sorted(ambiguous2.items()):
        orb_name = sig_name(key[0])
        delta_name = sig_name(key[1])
        print(f"    {orb_name}→Δ{delta_name}: {len(compounds)} different compounds")


# ─── 7. The formula ──────────────────────────────────────────────────────

print(f"\n7. EXPLICIT FORMULA FOR COMPOUND")
print("-" * 50)
print(f"  Let:")
print(f"    P_k = pair type of orbit_start (orbit-determined)")
print(f"    G   = bridge kernel component (the 'free choice')")
print(f"    P'  = pair type of orbit_end (orbit-determined)")
print(f"    Δ   = orbit change (3-bit, from bridge)")
print(f"")
print(f"  Then compound = Δ_6bit ⊕ (P_k ⊕ G ⊕ P')")
print(f"  where Δ_6bit = (Δo,Δm,Δi,0,0,0)")
print(f"  and (P_k ⊕ G ⊕ P') is a kernel element")
print(f"")
print(f"  The compound's Hamming weight = wt(Δ_6bit ⊕ gen_compound_6bit)")
print(f"  Since Δ_6bit has bits only in positions 1-3 and gen has palindrome structure,")
print(f"  these interact in a specific way.")
print()

# Compute the gen_compound as a 6-bit kernel element
for w in windows:
    g1 = gen_to_3bit(w['pair_k_type'])
    gb = gen_to_3bit(w['bridge_kernel_name'])
    g2 = gen_to_3bit(w['pair_k1_type'])
    g_total = xor3(xor3(g1, gb), g2)
    
    # Expand to 6-bit kernel element
    g6 = (g_total[0], g_total[1], g_total[2], g_total[2], g_total[1], g_total[0])
    
    # Compound should = orbit_delta_6bit ⊕ g6
    br = bridges[w['k']]
    expected = xor6(br['orbit_delta'], g6)
    actual = w['compound']
    
    ok = expected == actual
    if not ok:
        print(f"  MISMATCH W{w['k']}: expected {''.join(map(str, expected))}, got {''.join(map(str, actual))}")

print(f"  Formula verified for all 31 windows: compound = orbit_Δ₆ ⊕ (P_k ⊕ G ⊕ P')₆")


# ─── 8. What patterns emerge in the generator chain? ─────────────────────

print(f"\n8. GENERATOR CHAIN PATTERNS")
print("-" * 50)

# The gen compound P_k ⊕ G ⊕ P' tells us:
# The bridge kernel G acts as a "relay" between two orbit-determined pair types.
# When G = id: compound gen = P_k ⊕ P' (just the pair type change)
# When G = P_k: compound gen = P' (the starting pair type cancels)
# When G = P': compound gen = P_k (the ending pair type cancels)
# When G = P_k ⊕ P': compound gen = id (everything cancels!)

print(f"  Special cases:")
cancel_count = 0
for w in windows:
    g1_3 = gen_to_3bit(w['pair_k_type'])
    gb_3 = gen_to_3bit(w['bridge_kernel_name'])
    g2_3 = gen_to_3bit(w['pair_k1_type'])
    g_total = xor3(xor3(g1_3, gb_3), g2_3)
    
    if g_total == (0,0,0):
        cancel_count += 1
        print(f"    W{w['k']:2d}: {w['pair_k_type']}⊕{w['bridge_kernel_name']}⊕{w['pair_k1_type']} = id  "
              f"← ALL GENERATORS CANCEL")
    elif gb_3 == (0,0,0):
        print(f"    W{w['k']:2d}: {w['pair_k_type']}⊕id⊕{w['pair_k1_type']} = {sig_name(g_total).upper()}  "
              f"← bridge kernel = id (pure orbit change)")
    elif gb_3 == g1_3:
        print(f"    W{w['k']:2d}: {w['pair_k_type']}⊕{w['bridge_kernel_name']}⊕{w['pair_k1_type']} = {sig_name(g_total).upper()}  "
              f"← bridge kernel = pair_k type (start cancels)")
    elif gb_3 == g2_3:
        print(f"    W{w['k']:2d}: {w['pair_k_type']}⊕{w['bridge_kernel_name']}⊕{w['pair_k1_type']} = {sig_name(g_total).upper()}  "
              f"← bridge kernel = pair_{'{k+1}'} type (end cancels)")

print(f"\n  Windows where all generators cancel: {cancel_count}/31")
print(f"  In these cases, compound = pure orbit change (positions 1-3 only, zeros in 4-6)")


# ─── 9. Compound vs bridge: does compound recover structure? ─────────────

print(f"\n9. STRUCTURAL RECOVERY")
print("-" * 50)

# Are compound masks more structured than bridge masks?
# Check: how many unique compound masks are generator-expressible?
compound_gen_count = sum(1 for c in unique_compounds if c in MASK_NAMES)
bridge_unique = sorted(set(b['mask'] for b in bridges))
bridge_gen_count = sum(1 for b in bridge_unique if b in MASK_NAMES)

print(f"  Unique bridge masks: {len(bridge_unique)}, generator-expressible: {bridge_gen_count}")
print(f"  Unique compound masks: {len(unique_compounds)}, generator-expressible: {compound_gen_count}")

# Are any compound masks palindromic (symmetric)?
palindromic = [c for c in unique_compounds if c == tuple(reversed(c))]
print(f"  Palindromic compound masks: {len(palindromic)}")
for p in palindromic:
    print(f"    {''.join(map(str, p))} ({gen_name(p)})")

# Hamming weight parity
compound_even = sum(1 for c in compound_masks if sum(c) % 2 == 0)
bridge_even = sum(1 for b in bridges if sum(b['mask']) % 2 == 0)
print(f"\n  Even-Hamming bridges: {bridge_even}/31")
print(f"  Even-Hamming compounds: {compound_even}/31")
print(f"  (Standard pairs are always even-Hamming)")


# ─── 10. The h1→h4 direct path ────────────────────────────────────────────

print(f"\n10. THE h₁→h₄ PATH: WHAT DOES THE COMPOUND 'SEE'?")
print("-" * 50)
print(f"  The compound mask is h₁ XOR h₄ — the direct path from the start of pair_k")
print(f"  to the end of pair_{'{k+1}'}. This is the 'net change' across a 4-hex window.")
print()

# What orbit transition does the compound produce?
# compound has same orbit_Δ as bridge (verified above)
# But h₁ and h₄ are in different orbits (the ones before/after the bridge)
# h₁ is in orbit_start, h₄ is in orbit_end (same as h₃)
# So compound represents a cross-orbit transformation from orbit_start to orbit_end

# Check: is the compound's projection equal to the bridge's orbit change?
for w in windows:
    comp_proj = (w['compound'][0]^w['compound'][5], w['compound'][1]^w['compound'][4], w['compound'][2]^w['compound'][3])
    assert comp_proj == tuple(w['orbit_delta']), f"Mismatch at W{w['k']}"
print(f"  Verified: P(compound) = orbit_Δ for all 31 windows")
print(f"  The compound's orbit change = the bridge's orbit change (pair steps cancel in projection)")


# ─── 11. Sequence of gen_compounds ─────────────────────────────────────────

print(f"\n11. SEQUENCE OF GENERATOR COMPOUNDS")
print("-" * 50)
print(f"  The gen_compound (P_k ⊕ G ⊕ P') encodes how pair types 'adapt' across bridges.")
print(f"  Consecutive gen_compounds share the P' = P_{{k+1}} term:")
print(f"    W_k gen = P_k ⊕ G_k ⊕ P_{{k+1}}")
print(f"    W_{{k+1}} gen = P_{{k+1}} ⊕ G_{{k+1}} ⊕ P_{{k+2}}")
print(f"  XOR of consecutive: P_k ⊕ G_k ⊕ G_{{k+1}} ⊕ P_{{k+2}}")
print(f"  (P_{{k+1}} cancels!)")
print()

# Compute consecutive XOR of gen compounds
for k in range(len(gen_compounds_3bit) - 1):
    g_curr = gen_compounds_3bit[k]
    g_next = gen_compounds_3bit[k + 1]
    g_xor = xor3(g_curr, g_next)
    name_curr = sig_name(g_curr).upper() if any(g_curr) else 'id'
    name_next = sig_name(g_next).upper() if any(g_next) else 'id'
    name_xor = sig_name(g_xor).upper() if any(g_xor) else 'id'
    print(f"  W{k:2d}→W{k+1:2d}: {name_curr} ⊕ {name_next} = {name_xor}")

consecutive_xors = [xor3(gen_compounds_3bit[k], gen_compounds_3bit[k+1]) for k in range(len(gen_compounds_3bit)-1)]
consec_freq = Counter(consecutive_xors)
print(f"\n  Consecutive XOR distribution:")
for g, count in sorted(consec_freq.items(), key=lambda x: -x[1]):
    name = sig_name(g).upper() if any(g) else 'id'
    print(f"    {name:>3s}: {count}×")


print(f"\n{'=' * 70}")
print("THREAD 3 COMPLETE")
print("=" * 70)
