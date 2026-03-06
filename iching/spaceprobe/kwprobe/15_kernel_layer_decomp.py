"""
Which kernels contribute to outer vs inner change at inter-pair bridges?
Does the sequence prefer O-component (outer change) over MI-component (inner change)?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    MASK_ALL, hugua, reverse6, hamming6, fmt6,
)

kw_hex = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}

def get_inner(h): return (h >> 1) & 0xF
def get_outer(h): return (h & 1) | (((h >> 5) & 1) << 1)

# ══════════════════════════════════════════════════════════════════════════════
# 1. DECOMPOSE EACH INTER-PAIR BRIDGE BY KERNEL AND LAYER CHANGE
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. KERNEL vs LAYER CHANGE AT INTER-PAIR BRIDGES")
print("=" * 70)

bridges = []
for k in range(31):
    h1 = kw_hex[2*k + 1]
    h2 = kw_hex[2*(k+1)]
    xor = h1 ^ h2
    kernel = mirror_kernel(xor)
    kname = kernel_names[kernel]
    
    bits = [(xor >> i) & 1 for i in range(6)]
    outer_change = bits[0] + bits[5]
    inner_change = bits[1] + bits[2] + bits[3] + bits[4]
    hu_d = hamming6(hugua(h1), hugua(h2))
    
    bridges.append({
        'k': kname, 'kernel': kernel, 'xor': xor,
        'hex_d': hamming6(h1, h2),
        'outer': outer_change, 'inner': inner_change,
        'hu_d': hu_d, 'bits': bits,
    })

print(f"\n  {'Bridge':>3s} {'Kernel':>4s} {'XOR':>8s} {'hex_d':>5s} {'outer':>5s} {'inner':>5s} {'hu_d':>4s}")
for i, b in enumerate(bridges):
    xor_str = ''.join(str(x) for x in b['bits'])
    print(f"  {i:3d}    {b['k']:>4s}  {xor_str}  {b['hex_d']:5d} {b['outer']:5d} {b['inner']:5d} {b['hu_d']:4d}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. KERNEL-LEVEL STATISTICS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. MEAN LAYER CHANGE PER KERNEL TYPE")
print("=" * 70)

by_kernel = defaultdict(list)
for b in bridges:
    by_kernel[b['k']].append(b)

print(f"\n  {'Kernel':>4s} {'N':>3s} {'hex_d':>6s} {'outer':>6s} {'inner':>6s} {'hu_d':>5s} {'out/hex':>7s}")
for kname in ['id', 'O', 'M', 'I', 'OM', 'OI', 'MI', 'OMI']:
    bs = by_kernel.get(kname, [])
    if not bs:
        continue
    n = len(bs)
    hex_d = np.mean([b['hex_d'] for b in bs])
    outer = np.mean([b['outer'] for b in bs])
    inner = np.mean([b['inner'] for b in bs])
    hu_d = np.mean([b['hu_d'] for b in bs])
    out_frac = outer / hex_d if hex_d > 0 else 0
    print(f"  {kname:>4s} {n:3d}  {hex_d:6.2f} {outer:6.2f} {inner:6.2f} {hu_d:5.2f} {out_frac:7.3f}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. THE O vs MI QUESTION
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. O-COMPONENT vs MI-COMPONENT AT BRIDGES")
print("=" * 70)

# Decompose: does having O in the kernel add outer change?
# Does having M or I add inner change?

has_O = [b for b in bridges if b['kernel'][0] == 1]
no_O = [b for b in bridges if b['kernel'][0] == 0]
has_M = [b for b in bridges if b['kernel'][1] == 1]
no_M = [b for b in bridges if b['kernel'][1] == 0]
has_I = [b for b in bridges if b['kernel'][2] == 1]
no_I = [b for b in bridges if b['kernel'][2] == 0]

print(f"\n  Effect of O component (outer symmetry breaking):")
print(f"    Has O ({len(has_O)}): outer={np.mean([b['outer'] for b in has_O]):.2f}  inner={np.mean([b['inner'] for b in has_O]):.2f}  hu={np.mean([b['hu_d'] for b in has_O]):.2f}")
print(f"    No O  ({len(no_O)}): outer={np.mean([b['outer'] for b in no_O]):.2f}  inner={np.mean([b['inner'] for b in no_O]):.2f}  hu={np.mean([b['hu_d'] for b in no_O]):.2f}")

print(f"\n  Effect of M component (middle symmetry breaking):")
print(f"    Has M ({len(has_M)}): outer={np.mean([b['outer'] for b in has_M]):.2f}  inner={np.mean([b['inner'] for b in has_M]):.2f}  hu={np.mean([b['hu_d'] for b in has_M]):.2f}")
print(f"    No M  ({len(no_M)}): outer={np.mean([b['outer'] for b in no_M]):.2f}  inner={np.mean([b['inner'] for b in no_M]):.2f}  hu={np.mean([b['hu_d'] for b in no_M]):.2f}")

print(f"\n  Effect of I component (interface symmetry breaking):")
print(f"    Has I ({len(has_I)}): outer={np.mean([b['outer'] for b in has_I]):.2f}  inner={np.mean([b['inner'] for b in has_I]):.2f}  hu={np.mean([b['hu_d'] for b in has_I]):.2f}")
print(f"    No I  ({len(no_I)}): outer={np.mean([b['outer'] for b in no_I]):.2f}  inner={np.mean([b['inner'] for b in no_I]):.2f}  hu={np.mean([b['hu_d'] for b in no_I]):.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. ACTUAL BIT FLIP PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. ACTUAL XOR MASKS AT INTER-PAIR BRIDGES")
print("=" * 70)

xor_counts = Counter()
for b in bridges:
    xor_counts[tuple(b['bits'])] += 1

print(f"\n  XOR mask frequencies (bit₀...bit₅):")
print(f"  {'mask':>8s} {'cnt':>3s} {'kernel':>4s} {'hex_d':>5s} {'out':>3s} {'in':>3s}")
for mask, c in sorted(xor_counts.items(), key=lambda x: -x[1]):
    mask_str = ''.join(str(x) for x in mask)
    kernel = mirror_kernel(sum(mask[i] << i for i in range(6)))
    kname = kernel_names[kernel]
    hd = sum(mask)
    out = mask[0] + mask[5]
    inn = sum(mask[1:5])
    print(f"  {mask_str:>8s} {c:3d}  {kname:>4s}  {hd:5d} {out:3d} {inn:3d}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE REAL QUESTION: PALINDROMIC vs ANTI-PALINDROMIC XOR
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. PALINDROMIC (H-kernel) vs ANTI-PALINDROMIC XOR AT BRIDGES")
print("=" * 70)

# H-kernel (id, O) = palindromic XOR: bits symmetric under reversal
# Non-H (M, I, MI, OM, OI, OMI) = anti-palindromic in at least one layer

h_bridges = [b for b in bridges if b['k'] in ('id', 'O')]
non_h_bridges = [b for b in bridges if b['k'] not in ('id', 'O')]

print(f"\n  H-kernel (palindromic XOR, {len(h_bridges)}):")
print(f"    outer={np.mean([b['outer'] for b in h_bridges]):.2f}  inner={np.mean([b['inner'] for b in h_bridges]):.2f}  hu={np.mean([b['hu_d'] for b in h_bridges]):.2f}")

print(f"\n  Non-H (anti-palindromic XOR, {len(non_h_bridges)}):")
print(f"    outer={np.mean([b['outer'] for b in non_h_bridges]):.2f}  inner={np.mean([b['inner'] for b in non_h_bridges]):.2f}  hu={np.mean([b['hu_d'] for b in non_h_bridges]):.2f}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. KEY: WHAT DOES EACH KERNEL COMPONENT DO TO 互?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. KERNEL COMPONENT → 互 EFFECT (ALGEBRAIC)")
print("=" * 70)

# 互 extracts bits 1,2,3,4 and rearranges: 
#   hu = [bit2, bit1, bit4, bit3, bit2, bit3] (standard nuclear extraction)
# Wait, let me recalculate. 互 takes inner 4 lines (2,3,4,5 from bottom):
# Actually from our code: hugua extracts lines 2,3,4,5 from bottom-up
# Lines (bottom=0): 0,1,2,3,4,5
# 互 lower = lines 1,2,3 (bits 1,2,3)
# 互 upper = lines 2,3,4 (bits 2,3,4)
# So 互 = lower_tri(bits 1,2,3) + upper_tri(bits 2,3,4)

# When we XOR two hexagrams, the 互 XOR depends on:
# - lower 互 XOR: bits 1,2,3 of hex XOR
# - upper 互 XOR: bits 2,3,4 of hex XOR
# Combined: 互 XOR depends on bits 1,2,3,4 of hex XOR (the inner bits!)

# O component (bit0 ≠ bit5): only affects outer bits → NO effect on 互
# M component (bit1 ≠ bit4): affects inner bits 1 and 4 → affects 互
# I component (bit2 ≠ bit3): affects inner bits 2 and 3 → affects 互

print("""
  互 depends on hex bits 1,2,3,4 (the inner 4 bits).
  
  Kernel components and their effect on 互:
    O (bit₀ ≠ bit₅): outer only → NO 互 effect
    M (bit₁ ≠ bit₄): inner → DOES affect 互  
    I (bit₂ ≠ bit₃): interface → DOES affect 互
  
  Therefore:
    Kernels with O only (id, O):      互 change = 0 from this component
    Kernels with M or I (M, I, MI...): 互 change > 0 from these components
  
  To minimize 互 distance: prefer O over M,I.
  To maximize hex distance while minimizing 互: use O without M,I.
""")

# Verify: O-only bridges (kernel = O or id) should have lower 互 distance
pure_outer = [b for b in bridges if b['kernel'][1] == 0 and b['kernel'][2] == 0]  # no M, no I
has_inner_k = [b for b in bridges if b['kernel'][1] == 1 or b['kernel'][2] == 1]  # M or I

print(f"  Pure outer kernels (no M, no I): {len(pure_outer)} bridges")
if pure_outer:
    print(f"    hu_d = {[b['hu_d'] for b in pure_outer]}")
    print(f"    mean hu_d = {np.mean([b['hu_d'] for b in pure_outer]):.2f}")
    print(f"    mean hex_d = {np.mean([b['hex_d'] for b in pure_outer]):.2f}")
    print(f"    kernels: {Counter(b['k'] for b in pure_outer)}")

print(f"\n  Inner kernels (has M or I): {len(has_inner_k)} bridges")
if has_inner_k:
    print(f"    mean hu_d = {np.mean([b['hu_d'] for b in has_inner_k]):.2f}")
    print(f"    mean hex_d = {np.mean([b['hex_d'] for b in has_inner_k]):.2f}")
    print(f"    kernels: {Counter(b['k'] for b in has_inner_k)}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE ACTUAL INNER BIT PATTERN AT BRIDGES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. INNER BIT CHANGE PATTERN AT BRIDGES")  
print("=" * 70)

# For each bridge, which inner bits change?
inner_bit_counts = Counter()
for b in bridges:
    changed = tuple(b['bits'][1:5])  # bits 1,2,3,4
    inner_bit_counts[changed] += 1

print(f"\n  Inner XOR patterns (bits 1,2,3,4):")
print(f"  {'pattern':>7s} {'cnt':>3s} {'inner_d':>7s} {'kernel M,I':>10s}")
for pattern, c in sorted(inner_bit_counts.items(), key=lambda x: -x[1]):
    pstr = ''.join(str(x) for x in pattern)
    d = sum(pattern)
    # M component: bit1 != bit4
    m = pattern[0] ^ pattern[3]
    # I component: bit2 != bit3  
    i = pattern[1] ^ pattern[2]
    mi_str = f"M={m} I={i}"
    print(f"  {pstr:>7s} {c:3d}  {d:7d}  {mi_str:>10s}")

# How many have 0 inner change?
zero_inner = sum(c for p, c in inner_bit_counts.items() if sum(p) == 0)
print(f"\n  Zero inner change: {zero_inner}/31 bridges")

# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. SUMMARY")
print("=" * 70)

print(f"""
  The O kernel component changes ONLY outer bits → zero 互 effect.
  The M and I components change inner bits → directly affect 互.
  
  At inter-pair bridges:
    Pure O (id + O): {len(pure_outer)} bridges, mean hu_d={np.mean([b['hu_d'] for b in pure_outer]) if pure_outer else 'N/A':.2f}
    Has M or I:      {len(has_inner_k)} bridges, mean hu_d={np.mean([b['hu_d'] for b in has_inner_k]):.2f}
    
    Has O component: {len(has_O)}, outer={np.mean([b['outer'] for b in has_O]):.2f}
    No O component:  {len(no_O)}, outer={np.mean([b['outer'] for b in no_O]):.2f}
    
    Has M component: {len(has_M)}, inner={np.mean([b['inner'] for b in has_M]):.2f}
    Has I component: {len(has_I)}, inner={np.mean([b['inner'] for b in has_I]):.2f}
    
  The sequence has {len(has_O)}/31 = {len(has_O)/31*100:.0f}% bridges with O component.
  Random expectation for any component: 50%.
""")
