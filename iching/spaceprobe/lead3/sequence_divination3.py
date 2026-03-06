"""
互² convergence: the deepest structure.

Key discovery: iterated 互 has THREE basins:
1. Kun (000000) — 16 hexagrams, fixed point
2. Qian (111111) — 16 hexagrams, fixed point
3. JiJi↔WeiJi (101010↔010101) — 32 hexagrams, 2-cycle

The 2-cycle IS Kan↔Li oscillation. So iterated 互 either dies (Kun/Qian)
or oscillates on the Water↔Fire axis forever.

Questions:
1. What determines which basin a hexagram falls into?
2. Is the basin assignment algebraically clean?
3. How does the basin structure interact with the KW sequence?
4. Does the convergence depth (1-step vs 2-step) matter?
5. The UC-Kun / LC-Qian asymmetry — what drives it?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, reverse6,
    hamming6, fmt6, fmt3,
)

# Build KW sequence
kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

# ══════════════════════════════════════════════════════════════════════════════
# 1. BASIN CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. 互 CONVERGENCE BASIN CLASSIFICATION")
print("=" * 70)

# Classify every hexagram
KUN = 0b000000
QIAN = 0b111111
JIJI = 0b010101
WEIJI = 0b101010

def classify_basin(h):
    """Returns (basin, depth) where basin is 'Kun', 'Qian', or 'KanLi'"""
    current = h
    for depth in range(10):
        nxt = hugua(current)
        if nxt == current:
            if current == KUN:
                return 'Kun', depth
            elif current == QIAN:
                return 'Qian', depth
            else:
                return f'Fixed({fmt6(current)})', depth
        if nxt == hugua(hugua(current)):
            # Check for 2-cycle
            pass
        current = nxt
    # Check for cycle
    current = hugua(h)
    if hugua(current) != current and hugua(hugua(current)) == current:
        return 'KanLi', -1  # Cycle
    return 'Unknown', -1

# More careful classification
def get_convergence(h, max_iter=20):
    """Returns (type, attractor, depth)"""
    chain = [h]
    for _ in range(max_iter):
        nxt = hugua(chain[-1])
        chain.append(nxt)
        # Fixed point
        if nxt == chain[-2]:
            return ('fixed', nxt, len(chain) - 2)
        # 2-cycle detection
        if len(chain) >= 3 and nxt == chain[-3]:
            return ('cycle2', (chain[-3], chain[-2]), len(chain) - 3)
    return ('unknown', None, -1)

basins = {}
for h in range(64):
    conv_type, attractor, depth = get_convergence(h)
    basins[h] = (conv_type, attractor, depth)

# Print classification
print(f"\n  All 64 hexagrams by basin:")
basin_groups = defaultdict(list)
for h in range(64):
    conv_type, attractor, depth = basins[h]
    if conv_type == 'fixed':
        basin_name = 'Kun' if attractor == KUN else 'Qian'
    else:
        basin_name = 'KanLi'
    basin_groups[basin_name].append((h, depth))

for basin_name in ['Kun', 'Qian', 'KanLi']:
    hexagrams = basin_groups[basin_name]
    print(f"\n  Basin {basin_name} ({len(hexagrams)} hexagrams):")
    for h, depth in sorted(hexagrams, key=lambda x: x[1]):
        bits = [(h >> i) & 1 for i in range(6)]
        lo = lower_trigram(h)
        up = upper_trigram(h)
        # Find KW position
        kw_pos = kw_hex.index(h) + 1
        canon = "UC" if kw_pos <= 30 else "LC"
        d_str = f"d={depth}" if depth >= 0 else "cycle"
        print(f"    {fmt6(h)} {TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]:4s} "
              f"KW#{kw_pos:2d} [{canon}] {d_str}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. WHAT DETERMINES THE BASIN?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. BASIN DETERMINANT — WHAT PROPERTY DECIDES THE BASIN?")
print("=" * 70)

# The inner 4 bits (bits 1-4, 0-indexed) determine the 互 value.
# So the basin is determined by the inner 4 bits of h.
# Let's verify and find the pattern.

print(f"\n  Inner 4 bits → basin:")
inner_basin = {}
for h in range(64):
    inner = (h >> 1) & 0xF  # bits 1,2,3,4
    conv_type, attractor, depth = basins[h]
    basin_name = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
                 'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
    
    if inner not in inner_basin:
        inner_basin[inner] = basin_name
    else:
        assert inner_basin[inner] == basin_name, f"Inconsistent: inner={inner:04b}"

for inner in sorted(inner_basin.keys()):
    # Which hexagrams have this inner?
    hexes = [h for h in range(64) if (h >> 1) & 0xF == inner]
    print(f"    inner={inner:04b}: basin={inner_basin[inner]:6s} "
          f"  hexagrams={[fmt6(h) for h in hexes]}")

# The inner 4 bits are what 互 reads. So the basin is really about
# what the 互 VALUE converges to.
print(f"\n  互 values by basin:")
for h in sorted(set(hugua(h) for h in range(64))):
    # Where does this 互 value converge?
    conv_type, attractor, depth = get_convergence(h)
    if conv_type == 'fixed':
        basin = 'Kun' if attractor == KUN else 'Qian'
    else:
        basin = 'KanLi'
    lo, up = lower_trigram(h), upper_trigram(h)
    print(f"    互={fmt6(h)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}): {basin} (depth {depth})")

# ══════════════════════════════════════════════════════════════════════════════
# 3. THE PATTERN IN INNER BITS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. BASIN PATTERN — INNER BIT STRUCTURE")
print("=" * 70)

# Let's look at the inner 4 bits pattern
# Bits 1,2,3,4 (0-indexed from right)
# If we call them a,b,c,d:
# 互 lower trigram = (a,b,c) = bits 1,2,3
# 互 upper trigram = (b,c,d) = bits 2,3,4
# So 互 has overlap in bits b,c (middle of inner)

# The iterated 互 chain depends on how these inner bits evolve.
# 互(h) inner bits are determined by 互(h)'s bits 1-4, which are:
# 互(h) bit 1 = b (original bit 2)
# 互(h) bit 2 = c (original bit 3)  
# 互(h) bit 3 = b (original bit 2)
# 互(h) bit 4 = c (original bit 3)
# Wait, that's not right. Let me think more carefully.

# 互(h) = hexagram with:
# bit 0 (lowest) = h bit 1
# bit 1 = h bit 2
# bit 2 = h bit 3
# bit 3 = h bit 2
# bit 4 = h bit 3
# bit 5 = h bit 4

# So 互(h) inner bits (positions 1-4):
# 互(h) bit 1 = h bit 2
# 互(h) bit 2 = h bit 3
# 互(h) bit 3 = h bit 2
# 互(h) bit 4 = h bit 3

# So the inner bits of 互(h) = (b, c, b, c) where b = h_bit2, c = h_bit3!
# This means 互² inner bits are determined by the MIDDLE 2 BITS of h's inner 4.

# And 互² of anything has inner bits (b,c,b,c) where b,c are from 互,
# which are (h_bit2, h_bit3) → 互² inner = (h_bit3, h_bit2, h_bit3, h_bit2)?

# Wait, let me be more precise. Let me just compute 互² directly.

print(f"\n  互² inner bits analysis:")
print(f"  (h inner abcd → 互 inner → 互² inner)")
for inner in range(16):
    a, b, c, d = (inner >> 0) & 1, (inner >> 1) & 1, (inner >> 2) & 1, (inner >> 3) & 1
    
    # 互(h) has bits: a=h1, b2=h2, c3=h3, b2=h2, c3=h3, d=h4
    # So 互(h) = bit0=a, bit1=b, bit2=c, bit3=b, bit4=c, bit5=d
    hu_h = a | (b << 1) | (c << 2) | (b << 3) | (c << 4) | (d << 5)
    
    # Actually let me just use the function
    # Pick a hexagram with this inner
    h = inner << 1  # outer bits 0
    hu = hugua(h)
    hu2 = hugua(hu)
    
    hu_inner = (hu >> 1) & 0xF
    hu2_inner = (hu2 >> 1) & 0xF
    
    conv_type, attractor, depth = get_convergence(h)
    basin = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
            'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
    
    print(f"    {a}{b}{c}{d} → {(hu_inner>>0)&1}{(hu_inner>>1)&1}{(hu_inner>>2)&1}{(hu_inner>>3)&1} → "
          f"{(hu2_inner>>0)&1}{(hu2_inner>>1)&1}{(hu2_inner>>2)&1}{(hu2_inner>>3)&1}  "
          f"basin={basin}")

# Let's check: the middle 2 bits (b,c) = bits 2,3 of h determine 互's structure
print(f"\n  Middle 2 bits (bits 2,3 of h) → basin:")
mid_basin = defaultdict(set)
for h in range(64):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    mid = (b2, b3)
    
    conv_type, attractor, depth = basins[h]
    basin_name = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
                 'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
    mid_basin[mid].add(basin_name)

for mid, basins_set in sorted(mid_basin.items()):
    print(f"    bits 2,3 = {mid}: basins = {basins_set}")

# Hmm, it's not just the middle 2 bits. Let me look at what determines convergence.
# The key insight: 互 extracts inner 4 bits and redistributes them.
# The repeated application concentrates on the middle 2 bits (positions 2,3).
# If both are 0 → converges to Kun
# If both are 1 → converges to Qian
# If mixed → oscillates (KanLi)

# But from the data above, bits 2,3 don't alone determine basin.
# Let's check what does.

print(f"\n  Comprehensive inner bit pattern analysis:")
# Check every possible boolean function of inner 4 bits
for bit_combo in [(1,), (2,), (3,), (1,2), (1,3), (2,3), (1,4), (2,4), (3,4),
                   (1,2,3), (1,2,4), (1,3,4), (2,3,4), (1,2,3,4)]:
    patterns = defaultdict(set)
    for h in range(64):
        key = tuple((h >> b) & 1 for b in bit_combo)
        conv_type, attractor, depth = basins[h]
        basin_name = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
                     'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
        patterns[key].add(basin_name)
    
    # Check if this determines basin uniquely
    unique = all(len(v) == 1 for v in patterns.values())
    if unique:
        print(f"    Bits {bit_combo} DETERMINE basin uniquely!")
        for key, basins_set in sorted(patterns.items()):
            print(f"      {key} → {list(basins_set)[0]}")
        break

# ══════════════════════════════════════════════════════════════════════════════
# 4. BASIN WALK ALONG KW SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. BASIN WALK ALONG KW SEQUENCE")
print("=" * 70)

# How does the basin change as you walk the KW sequence?
basin_seq = []
for i in range(64):
    h = kw_hex[i]
    conv_type, attractor, depth = basins[h]
    basin_name = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
                 'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
    basin_seq.append(basin_name)

# Print the basin sequence
print(f"\n  Basin sequence:")
for i in range(64):
    canon = "UC" if i < 30 else "LC"
    b = basin_seq[i]
    symbol = {'Kun': '○', 'Qian': '●', 'KanLi': '◎'}[b]
    print(f"    {i+1:2d}. {kw_names[i]:12s} [{canon}] → {symbol} {b}")

# Basin transitions
basin_trans = Counter()
for i in range(63):
    basin_trans[(basin_seq[i], basin_seq[i+1])] += 1

print(f"\n  Basin transition matrix:")
for b1 in ['Kun', 'KanLi', 'Qian']:
    for b2 in ['Kun', 'KanLi', 'Qian']:
        c = basin_trans.get((b1, b2), 0)
        print(f"    {b1:6s} → {b2:6s}: {c}")

# Basin runs (consecutive same basin)
runs = []
current_basin = basin_seq[0]
current_run = 1
for i in range(1, 64):
    if basin_seq[i] == current_basin:
        current_run += 1
    else:
        runs.append((current_basin, current_run))
        current_basin = basin_seq[i]
        current_run = 1
runs.append((current_basin, current_run))

print(f"\n  Basin runs along KW sequence:")
pos = 1
for basin, length in runs:
    symbol = {'Kun': '○', 'Qian': '●', 'KanLi': '◎'}[basin]
    end_pos = pos + length - 1
    canon = "UC" if pos <= 30 else "LC"
    if end_pos > 30 and pos <= 30:
        canon = "UC→LC"
    print(f"    KW {pos:2d}-{end_pos:2d}: {symbol} {basin:6s} (run of {length})")
    pos = end_pos + 1

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE ASYMMETRY: UC→KUN, LC→QIAN
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. CANON BASIN ASYMMETRY")
print("=" * 70)

uc_basins = Counter(basin_seq[:30])
lc_basins = Counter(basin_seq[30:])

print(f"\n  Upper Canon basin distribution:")
for b in ['Kun', 'KanLi', 'Qian']:
    c = uc_basins.get(b, 0)
    print(f"    {b:6s}: {c}/30 ({100*c/30:.0f}%)")

print(f"\n  Lower Canon basin distribution:")
for b in ['Kun', 'KanLi', 'Qian']:
    c = lc_basins.get(b, 0)
    print(f"    {b:6s}: {c}/34 ({100*c/34:.0f}%)")

# Is this significant? Monte Carlo test
np.random.seed(42)
n_trials = 100000

all_basins = [basins[h] for h in range(64)]
all_basin_names = []
for h in range(64):
    conv_type, attractor, depth = basins[h]
    bn = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
         'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
    all_basin_names.append(bn)

# KW actual: count of Kun basin in UC
kw_uc_kun = sum(1 for i in range(30) if basin_seq[i] == 'Kun')
kw_uc_qian = sum(1 for i in range(30) if basin_seq[i] == 'Qian')
kw_asymmetry = kw_uc_kun - kw_uc_qian  # Positive = UC has more Kun

asymmetries = []
for _ in range(n_trials):
    perm = np.random.permutation(64)
    uc = perm[:30]
    uc_kun = sum(1 for h in uc if all_basin_names[h] == 'Kun')
    uc_qian = sum(1 for h in uc if all_basin_names[h] == 'Qian')
    asymmetries.append(uc_kun - uc_qian)

asymmetries = np.array(asymmetries)
pctl = np.mean(asymmetries >= kw_asymmetry) * 100

print(f"\n  Asymmetry test (UC Kun count - UC Qian count):")
print(f"    KW asymmetry: {kw_asymmetry} (UC has {kw_uc_kun} Kun, {kw_uc_qian} Qian)")
print(f"    Random mean: {np.mean(asymmetries):.1f}, std: {np.std(asymmetries):.1f}")
print(f"    KW percentile: {100-pctl:.1f}th (fraction ≥ KW: {pctl:.2f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 6. BASIN AND THE FOUR ATTRACTORS AS STRUCTURE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. THE FOUR ATTRACTORS AS THE SEQUENCE'S SKELETON")
print("=" * 70)

# The four attractors: Kun (earth), Qian (heaven), JiJi (completion), WeiJi (incompletion)
# These are positions 2, 1, 63, 64 in KW sequence!
# The sequence begins and ends with the attractors.

print(f"\n  The four attractors in the KW sequence:")
attractor_positions = {
    KUN: ('Kun', 'Basin: Kun (earth)'),
    QIAN: ('Qian', 'Basin: Qian (heaven)'),
    JIJI: ('JiJi', 'Basin: KanLi cycle (completion)'),
    WEIJI: ('WeiJi', 'Basin: KanLi cycle (incompletion)'),
}

for h, (name, desc) in attractor_positions.items():
    kw_pos = kw_hex.index(h) + 1
    print(f"    {name:6s} = KW position {kw_pos:2d} — {desc}")

print(f"\n  The sequence starts with the two fixed points (Qian#1, Kun#2)")
print(f"  and ends with the two cycle points (JiJi#63, WeiJi#64).")
print(f"  This IS the 互 convergence structure encoded as narrative.")

# ══════════════════════════════════════════════════════════════════════════════
# 7. DOES THE SEQUENCE WALK THROUGH BASINS IN A MEANINGFUL WAY?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. BASIN PATTERN STRUCTURE")
print("=" * 70)

# Encode basins as numbers for pattern detection
basin_code = {'Kun': 0, 'KanLi': 1, 'Qian': 2}
basin_coded = [basin_code[b] for b in basin_seq]

# Check if pairs always share basins
print(f"\n  Do KW pairs share basins?")
same_basin_pairs = 0
for i in range(0, 64, 2):
    if basin_seq[i] == basin_seq[i+1]:
        same_basin_pairs += 1
    else:
        print(f"    Pair {i//2}: {kw_names[i]:12s}({basin_seq[i]}) ≠ "
              f"{kw_names[i+1]:12s}({basin_seq[i+1]})")

print(f"\n  Pairs with same basin: {same_basin_pairs}/32")

# Verify: if pair is (h, reverse(h)), does reverse preserve basin?
print(f"\n  Does reverse preserve basin?")
for h in range(64):
    rev = reverse6(h)
    b1 = basins[h]
    b2 = basins[rev]
    
    bn1 = 'Kun' if (b1[0] == 'fixed' and b1[1] == KUN) else \
           'Qian' if (b1[0] == 'fixed' and b1[1] == QIAN) else 'KanLi'
    bn2 = 'Kun' if (b2[0] == 'fixed' and b2[1] == KUN) else \
           'Qian' if (b2[0] == 'fixed' and b2[1] == QIAN) else 'KanLi'
    
    if bn1 != bn2:
        print(f"    MISMATCH: {fmt6(h)} ({bn1}) ≠ reverse {fmt6(rev)} ({bn2})")

# Does complement preserve basin?
print(f"\n  Does complement preserve basin?")
for h in range(64):
    comp = h ^ MASK_ALL
    b1 = basins[h]
    b2 = basins[comp]
    
    bn1 = 'Kun' if (b1[0] == 'fixed' and b1[1] == KUN) else \
           'Qian' if (b1[0] == 'fixed' and b1[1] == QIAN) else 'KanLi'
    bn2 = 'Kun' if (b2[0] == 'fixed' and b2[1] == KUN) else \
           'Qian' if (b2[0] == 'fixed' and b2[1] == QIAN) else 'KanLi'
    
    if bn1 != bn2:
        lo1, up1 = lower_trigram(h), upper_trigram(h)
        lo2, up2 = lower_trigram(comp), upper_trigram(comp)
        print(f"    {fmt6(h)} ({TRIGRAM_NAMES[lo1]}/{TRIGRAM_NAMES[up1]}, {bn1}) ↔ "
              f"{fmt6(comp)} ({TRIGRAM_NAMES[lo2]}/{TRIGRAM_NAMES[up2]}, {bn2})")

# ══════════════════════════════════════════════════════════════════════════════
# 8. THE CONVERGENCE DEPTH IN THE SEQUENCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. CONVERGENCE DEPTH ALONG THE SEQUENCE")
print("=" * 70)

print(f"\n  Depth = steps until fixed point or cycle entry:")
for i in range(64):
    h = kw_hex[i]
    conv_type, attractor, depth = basins[h]
    basin_name = 'Kun' if (conv_type == 'fixed' and attractor == KUN) else \
                 'Qian' if (conv_type == 'fixed' and attractor == QIAN) else 'KanLi'
    
    canon = "UC" if i < 30 else "LC"
    depth_bar = "█" * (depth + 1) if depth >= 0 else "∞∞∞"
    print(f"    {i+1:2d}. {kw_names[i]:12s} [{canon}] {basin_name:6s} d={depth:2d} {depth_bar}")

# Depth by canon
uc_depths = []
lc_depths = []
for i in range(64):
    h = kw_hex[i]
    conv_type, attractor, depth = basins[h]
    # For cycle, use depth = 2 (they reach the cycle in 2 steps typically)
    # Actually let's use the actual depth field which is -1 for cycles
    # but the chain shows they need 2-4 steps to reach cycle
    
    if i < 30:
        uc_depths.append(depth)
    else:
        lc_depths.append(depth)

# For non-cycle hexagrams
uc_fixed = [d for d in uc_depths if d >= 0]
lc_fixed = [d for d in lc_depths if d >= 0]
print(f"\n  Fixed-point hexagrams depth:")
print(f"    UC: mean={np.mean(uc_fixed):.2f}, values={Counter(uc_fixed)}")
print(f"    LC: mean={np.mean(lc_fixed):.2f}, values={Counter(lc_fixed)}")

# ══════════════════════════════════════════════════════════════════════════════
# 9. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. SYNTHESIS")
print("=" * 70)

print(f"""
  THE 互 CONVERGENCE MAP:

  64 hexagrams
    ├── 16 → Kun (○ fixed point, emptiness)
    │     UC: {uc_basins.get('Kun',0)}/30  LC: {lc_basins.get('Kun',0)}/34
    ├── 16 → Qian (● fixed point, fullness)  
    │     UC: {uc_basins.get('Qian',0)}/30  LC: {lc_basins.get('Qian',0)}/34
    └── 32 → JiJi↔WeiJi (◎ 2-cycle, Kan↔Li oscillation)
          UC: {uc_basins.get('KanLi',0)}/30  LC: {lc_basins.get('KanLi',0)}/34

  THE SEQUENCE FRAMING:
  
  Positions 1-2:   Qian, Kun     = the two fixed-point attractors
  Positions 63-64: JiJi, WeiJi   = the two cycle attractors
  
  The sequence opens with stability (fixed points)
  and closes with oscillation (the irreducible Kan↔Li cycle).
  
  COMPLEMENT SWAPS BASINS:
  Kun ↔ Qian (complement exchanges fixed points)
  KanLi ↔ KanLi (complement preserves the oscillation)
  
  This means complement pairs (4 of them, all self-reverse)
  cross between Kun and Qian basins.
  Reverse pairs stay in the same basin.
""")
