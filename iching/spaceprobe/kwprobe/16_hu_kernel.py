"""
Characterize the kernel of 互 XOR at inter-pair bridges.

Algebraic prediction:
  互_kernel = (hex_M, hex_I, hex_I)  →  always in H = {id, O, MI, OMI}
  hex O component vanishes (outer bits invisible to 互)

Verify and characterize the distribution.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6, fmt6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
)

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}

H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

def hu_name(h):
    return f"{TRIGRAM_NAMES[lower_trigram(h)]}/{TRIGRAM_NAMES[upper_trigram(h)]}"

# ══════════════════════════════════════════════════════════════════════════════
# 1. VERIFY: 互 KERNEL IS ALWAYS IN H
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. VERIFY: 互 KERNEL ALWAYS IN H")
print("=" * 70)

# Check ALL 64×64 hexagram pairs
violations = 0
for a in range(64):
    for b in range(64):
        if a == b:
            continue
        hu_a = hugua(a)
        hu_b = hugua(b)
        hu_xor = hu_a ^ hu_b
        hu_k = mirror_kernel(hu_xor)
        if hu_k not in H_KERNELS:
            violations += 1

print(f"\n  Checked all 64×63 = {64*63} hexagram pairs")
print(f"  互 kernel NOT in H: {violations}")
print(f"  互 kernel ALWAYS in H: {'✓ PROVEN' if violations == 0 else '✗ VIOLATED'}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. VERIFY: 互_KERNEL = (HEX_M, HEX_I, HEX_I)
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. VERIFY: 互 KERNEL = (hex_M, hex_I, hex_I)")
print("=" * 70)

mapping_violations = 0
for a in range(64):
    for b in range(64):
        if a == b:
            continue
        hex_xor = a ^ b
        hex_k = mirror_kernel(hex_xor)
        
        hu_xor = hugua(a) ^ hugua(b)
        hu_k = mirror_kernel(hu_xor)
        
        predicted = (hex_k[1], hex_k[2], hex_k[2])  # (hex_M, hex_I, hex_I)
        if hu_k != predicted:
            mapping_violations += 1

print(f"\n  Mapping violations: {mapping_violations}")
print(f"  互_kernel = (hex_M, hex_I, hex_I): {'✓ PROVEN' if mapping_violations == 0 else '✗ VIOLATED'}")

# The full mapping:
print(f"\n  Complete kernel transformation hex → 互:")
print(f"  {'hex_kernel':>12s} → {'互_kernel':>12s}")
for hk in sorted(kernel_names.keys()):
    O, M, I = hk
    hu_k = (M, I, I)
    print(f"  {kernel_names[hk]:>12s} ({O},{M},{I}) → {kernel_names[hu_k]:>12s} ({M},{I},{I})")

# ══════════════════════════════════════════════════════════════════════════════
# 3. INTER-PAIR BRIDGES: HEX KERNEL → 互 KERNEL
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. INTER-PAIR BRIDGES: HEX KERNEL → 互 KERNEL")
print("=" * 70)

print(f"\n  {'Bridge':>8s} {'hex_k':>5s} → {'hu_k':>5s}  "
      f"{'hex_XOR':>8s} {'互_XOR':>8s} "
      f"{'hex ΔL':>6s} {'hex ΔU':>6s} {'互 ΔL':>6s} {'互 ΔU':>6s}")

hex_kernel_dist = Counter()
hu_kernel_dist = Counter()

for k in range(31):
    h1 = kw_hex[2*k + 1]
    h2 = kw_hex[2*(k+1)]
    
    hex_xor = h1 ^ h2
    hex_k = mirror_kernel(hex_xor)
    hex_bits = [(hex_xor >> i) & 1 for i in range(6)]
    
    hu1, hu2 = hugua(h1), hugua(h2)
    hu_xor = hu1 ^ hu2
    hu_k = mirror_kernel(hu_xor)
    hu_bits = [(hu_xor >> i) & 1 for i in range(6)]
    
    # Trigram-level masks
    hex_lower_mask = tuple(hex_bits[0:3])
    hex_upper_mask = tuple(hex_bits[3:6])
    hu_lower_mask = tuple(hu_bits[0:3])
    hu_upper_mask = tuple(hu_bits[3:6])
    
    hex_kernel_dist[kernel_names[hex_k]] += 1
    hu_kernel_dist[kernel_names[hu_k]] += 1
    
    hx_str = ''.join(str(x) for x in hex_bits)
    hu_str = ''.join(str(x) for x in hu_bits)
    
    print(f"  {k:2d}→{k+1:2d}   {kernel_names[hex_k]:>5s} → {kernel_names[hu_k]:>5s}  "
          f"{hx_str}   {hu_str}   "
          f"{''.join(str(x) for x in hex_lower_mask):>6s} "
          f"{''.join(str(x) for x in hex_upper_mask):>6s} "
          f"{''.join(str(x) for x in hu_lower_mask):>6s} "
          f"{''.join(str(x) for x in hu_upper_mask):>6s}")

print(f"\n  Hex kernel distribution at bridges: {dict(sorted(hex_kernel_dist.items()))}")
print(f"  互 kernel distribution at bridges:  {dict(sorted(hu_kernel_dist.items()))}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. 互 TRIGRAM SYMMETRY AT BRIDGES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. 互 TRIGRAM MASKS: ARE THEY SYMMETRIC?")
print("=" * 70)

# For 互, the lower mask = (Δh1, Δh2, Δh3) and upper = (Δh2, Δh3, Δh4)
# They share the middle two components. They differ only at the edges:
# lower[0] = Δh1, upper[2] = Δh4 (outer)
# lower[2] = Δh3 = upper[1], lower[1] = Δh2 = upper[0] (shared)

# So the 互 lower and upper trigram masks overlap in 2 of 3 positions.
# When kernel(互) = id: lower mask = upper mask (all 3 match)
# When kernel(互) = O: only outer differs

hu_sym_count = Counter()
for k in range(31):
    h1 = kw_hex[2*k + 1]
    h2 = kw_hex[2*(k+1)]
    hu1, hu2 = hugua(h1), hugua(h2)
    hu_xor = hu1 ^ hu2
    hu_k = mirror_kernel(hu_xor)
    hu_bits = [(hu_xor >> i) & 1 for i in range(6)]
    
    lower_mask = tuple(hu_bits[0:3])
    upper_mask = tuple(hu_bits[3:6])
    
    if lower_mask == upper_mask:
        sym = "identical"
    elif lower_mask == tuple(reversed(upper_mask)):
        sym = "reversed"
    else:
        # Check overlap
        shared = sum(1 for i in range(3) if lower_mask[i] == upper_mask[i])
        sym = f"differ({3-shared}/3)"
    
    hu_sym_count[sym] += 1

print(f"\n  互 trigram mask symmetry at bridges:")
for s, c in sorted(hu_sym_count.items(), key=lambda x: -x[1]):
    print(f"    {s}: {c}/31")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE KEY: 互 TRIGRAMS SHARE THEIR CORE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. 互 TRIGRAM OVERLAP STRUCTURE")
print("=" * 70)

print("""
  互 lower trigram = (h₁, h₂, h₃) = lines 2,3,4
  互 upper trigram = (h₂, h₃, h₄) = lines 3,4,5
  
  They share lines 3,4 (h₂, h₃) — the interface!
  
  At a bridge, the 互 trigram XOR masks are:
    lower Δ = (Δh₁, Δh₂, Δh₃)
    upper Δ = (Δh₂, Δh₃, Δh₄)
  
  Shared: middle two components always identical (the interface change).
  Different: only the edge — lower[0]=Δh₁ vs upper[2]=Δh₄.
  
  互 kernel = id ↔ Δh₁ = Δh₄ (edges match too → complete symmetry)
  互 kernel = O  ↔ Δh₁ ≠ Δh₄ (edges differ → only outer asymmetry)
  互 kernel = MI ↔ Δh₂ ≠ Δh₃ (shared core differs → but still M=I)
  互 kernel = OMI↔ both edge and core differ
""")

# Count how many bridges have each type
print(f"  At inter-pair bridges:")
hu_id = hu_kernel_dist.get('id', 0)
hu_O = hu_kernel_dist.get('O', 0)
hu_MI = hu_kernel_dist.get('MI', 0)
hu_OMI = hu_kernel_dist.get('OMI', 0)
print(f"    id  (完全 symmetric, edges match):     {hu_id}/31")
print(f"    O   (only edges differ):               {hu_O}/31")
print(f"    MI  (shared core differs):             {hu_MI}/31")
print(f"    OMI (both edge and core differ):       {hu_OMI}/31")
print(f"    Total id+O (edge-only variation):      {hu_id + hu_O}/31")
print(f"    Total MI+OMI (core changes):           {hu_MI + hu_OMI}/31")

# ══════════════════════════════════════════════════════════════════════════════
# 6. HEX KERNEL COLLAPSE: 8 → 4
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. THE KERNEL COLLAPSE: hex Z₂³ → 互 H ≅ V₄")
print("=" * 70)

# The mapping hex_kernel → 互_kernel is a 2-to-1 surjection onto H:
# {id, O} → id      (hex O is invisible)
# {M, OM} → O       
# {I, OI} → MI      
# {MI, OMI} → OMI   

collapse = {}
for hk in sorted(kernel_names.keys()):
    O, M, I = hk
    hu_k = (M, I, I)
    hk_name = kernel_names[hk]
    hu_name_k = kernel_names[hu_k]
    if hu_name_k not in collapse:
        collapse[hu_name_k] = []
    collapse[hu_name_k].append(hk_name)

print(f"\n  Kernel collapse (2-to-1 onto H):")
for hu_k, hex_ks in sorted(collapse.items()):
    print(f"    {{{', '.join(hex_ks)}}} → {hu_k}")

print(f"\n  Interpretation:")
print(f"    The hex O component (outer bit asymmetry) is ERASED by 互.")
print(f"    互 sees only M and I — the middle and interface structure.")
print(f"    8 hex kernels collapse to 4 互 kernels = the H subgroup.")

# ══════════════════════════════════════════════════════════════════════════════
# 7. WHAT DOES THIS MEAN FOR THE 互 TRIGRAM EXPERIENCE?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. THE 互 TRIGRAM EXPERIENCE AT BRIDGES")
print("=" * 70)

# For each bridge, show what the 互 lower and upper trigrams actually experience
print(f"\n  {'Brg':>3s} {'互₁ lo/up':>16s} → {'互₂ lo/up':>16s} {'ΔL':>4s} {'ΔU':>4s} {'hu_k':>4s} {'shared?':>8s}")
for k in range(31):
    h1 = kw_hex[2*k + 1]
    h2 = kw_hex[2*(k+1)]
    hu1, hu2 = hugua(h1), hugua(h2)
    
    lo1 = TRIGRAM_NAMES[lower_trigram(hu1)]
    up1 = TRIGRAM_NAMES[upper_trigram(hu1)]
    lo2 = TRIGRAM_NAMES[lower_trigram(hu2)]
    up2 = TRIGRAM_NAMES[upper_trigram(hu2)]
    
    lo_changed = lo1 != lo2
    up_changed = up1 != up2
    
    hu_k = mirror_kernel(hu1 ^ hu2)
    
    if lo_changed and up_changed:
        shared = "both"
    elif lo_changed:
        shared = "lo only"
    elif up_changed:
        shared = "up only"
    else:
        shared = "none"
    
    lo_d = hamming6(lower_trigram(hu1), lower_trigram(hu2))
    up_d = hamming6(upper_trigram(hu1), upper_trigram(hu2))
    
    print(f"  {k:2d}→{k+1:2d} {lo1:>4s}/{up1:<4s}     → {lo2:>4s}/{up2:<4s}      {lo_d:3d}  {up_d:3d}  {kernel_names[hu_k]:>4s}  {shared:>8s}")

# Count
change_types = Counter()
for k in range(31):
    h1 = kw_hex[2*k + 1]
    h2 = kw_hex[2*(k+1)]
    hu1, hu2 = hugua(h1), hugua(h2)
    lo_ch = lower_trigram(hu1) != lower_trigram(hu2)
    up_ch = upper_trigram(hu1) != upper_trigram(hu2)
    if lo_ch and up_ch: change_types['both'] += 1
    elif lo_ch: change_types['lo_only'] += 1
    elif up_ch: change_types['up_only'] += 1
    else: change_types['none'] += 1

print(f"\n  互 trigram change pattern at bridges:")
print(f"    Both change:    {change_types.get('both', 0)}/31")
print(f"    Lower only:     {change_types.get('lo_only', 0)}/31")
print(f"    Upper only:     {change_types.get('up_only', 0)}/31")
print(f"    Neither (same): {change_types.get('none', 0)}/31")
