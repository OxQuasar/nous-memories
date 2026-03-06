"""
Probe the cross-basin pairs and depth structure.

The 4 cross-basin pairs sit at sequence boundaries:
  Pair 0: Qian/Kun (#1-2) — opening
  Pair 13: Yi/DaGuo (#27-28) — pre-canon-break
  Pair 14: Kan/Li (#29-30) — canon break
  Pair 30: ZhongFu/XiaoGuo (#61-62) — pre-closing

Questions:
1. What makes these 4 pairs structurally special beyond complement?
2. Do they partition the sequence into meaningful segments?
3. Depth-1 hexagrams (one step from attractor) — where are they?
4. The basin run pattern — is there a rhythm?
5. Do cross-basin pairs mark phase transitions in the sequence?
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

KUN = 0b000000
QIAN = 0b111111

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0:
        return 'Kun'
    elif b2 == 1 and b3 == 1:
        return 'Qian'
    else:
        return 'KanLi'

def get_depth(h):
    """Steps to fixed point or cycle entry."""
    current = h
    for depth in range(10):
        nxt = hugua(current)
        if nxt == current:
            return depth
        if depth > 0:
            # Check 2-cycle
            nxt2 = hugua(nxt)
            if nxt2 == current:
                return depth  # Already in cycle
        current = nxt
    return -1  # Shouldn't happen

basin_seq = [get_basin(kw_hex[i]) for i in range(64)]

# ══════════════════════════════════════════════════════════════════════════════
# 1. THE 4 CROSS-BASIN PAIRS — STRUCTURAL PROPERTIES
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. THE 4 CROSS-BASIN PAIRS — WHAT MAKES THEM SPECIAL")
print("=" * 70)

cross_pairs = [(0,1), (26,27), (28,29), (60,61)]  # 0-indexed KW positions
cross_pair_names = [
    "Qian/Kun", "Yi/Da Guo", "Kan/Li", "Zhong Fu/Xiao Guo"
]

print(f"\n  The 4 complement-only pairs (self-reverse hexagrams):")
for idx, ((i1, i2), name) in enumerate(zip(cross_pairs, cross_pair_names)):
    h1, h2 = kw_hex[i1], kw_hex[i2]
    lo1, up1 = lower_trigram(h1), upper_trigram(h1)
    lo2, up2 = lower_trigram(h2), upper_trigram(h2)
    
    # Properties
    is_self_rev1 = (reverse6(h1) == h1)
    is_self_rev2 = (reverse6(h2) == h2)
    is_comp = (h2 == h1 ^ MASK_ALL)
    
    # Bits
    print(f"\n  Pair: {name}")
    print(f"    {kw_names[i1]:12s} = {fmt6(h1)} ({TRIGRAM_NAMES[lo1]}/{TRIGRAM_NAMES[up1]}) "
          f"self-rev={is_self_rev1} basin={get_basin(h1)}")
    print(f"    {kw_names[i2]:12s} = {fmt6(h2)} ({TRIGRAM_NAMES[lo2]}/{TRIGRAM_NAMES[up2]}) "
          f"self-rev={is_self_rev2} basin={get_basin(h2)}")
    print(f"    complement={is_comp}")
    
    # Middle bits
    b2_1, b3_1 = (h1 >> 2) & 1, (h1 >> 3) & 1
    b2_2, b3_2 = (h2 >> 2) & 1, (h2 >> 3) & 1
    print(f"    Middle bits: {b2_1}{b3_1} ↔ {b2_2}{b3_2}")
    
    # 互 values
    hu1, hu2 = hugua(h1), hugua(h2)
    print(f"    互: {fmt6(hu1)} ↔ {fmt6(hu2)}")
    
    # Trigram structure: self-reverse means lower = reverse(upper)?
    # Actually, self-reverse means bit0=bit5, bit1=bit4, bit2=bit3
    # So lower trigram = reverse of upper trigram
    print(f"    Lower/Upper: {TRIGRAM_NAMES[lo1]}={fmt3(lo1)} / {TRIGRAM_NAMES[up1]}={fmt3(up1)}")

# How many self-reverse hexagrams total?
self_rev = [h for h in range(64) if reverse6(h) == h]
print(f"\n  Total self-reverse hexagrams: {len(self_rev)}")
print(f"  (These are hexagrams where lower trigram = reverse of upper trigram)")
print(f"  They form {len(self_rev)//2} complement pairs + possibly self-complement")

# List them all
print(f"\n  All self-reverse hexagrams:")
for h in self_rev:
    lo, up = lower_trigram(h), upper_trigram(h)
    kw_pos = kw_hex.index(h) + 1
    comp = h ^ MASK_ALL
    comp_pos = kw_hex.index(comp) + 1
    basin = get_basin(h)
    print(f"    {fmt6(h)} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}) "
          f"KW#{kw_pos:2d} basin={basin:6s}  complement=KW#{comp_pos:2d}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. SEGMENTS BETWEEN CROSS-BASIN PAIRS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. SEQUENCE SEGMENTS BETWEEN CROSS-BASIN PAIRS")
print("=" * 70)

# Cross-basin pairs at positions: 1-2, 27-28, 29-30, 61-62
# Plus framing: 63-64 (JiJi/WeiJi, both KanLi)
# Segments: 3-26, 31-60

segments = [
    ("Opening pair", 0, 2),
    ("Segment 1 (UC body)", 2, 26),
    ("Pre-break pair", 26, 28),
    ("Canon break pair", 28, 30),
    ("Segment 2 (LC body)", 30, 60),
    ("Pre-close pair", 60, 62),
    ("Closing pair", 62, 64),
]

for name, start, end in segments:
    subset = basin_seq[start:end]
    counts = Counter(subset)
    n = len(subset)
    hex_names = [kw_names[i] for i in range(start, end)]
    
    print(f"\n  {name} (KW {start+1}-{end}):")
    print(f"    Hexagrams: {', '.join(hex_names)}")
    print(f"    Basin distribution: ", end="")
    for b in ['Kun', 'KanLi', 'Qian']:
        c = counts.get(b, 0)
        pct = 100*c/n if n > 0 else 0
        print(f"{b}={c}/{n}({pct:.0f}%) ", end="")
    print()

# ══════════════════════════════════════════════════════════════════════════════
# 3. DEPTH-1 HEXAGRAMS — NEAR-ATTRACTOR POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. DEPTH-1 HEXAGRAMS (ONE STEP FROM ATTRACTOR)")
print("=" * 70)

# Depth 0: the attractors themselves (Qian, Kun, JiJi, WeiJi)
# Depth 1: one 互 application reaches attractor or cycle
# These are structurally "close" to the attractors

depth_groups = defaultdict(list)
for i in range(64):
    h = kw_hex[i]
    d = get_depth(h)
    basin = get_basin(h)
    depth_groups[d].append((i+1, kw_names[i], basin, h))

for d in sorted(depth_groups.keys()):
    items = depth_groups[d]
    print(f"\n  Depth {d}: {len(items)} hexagrams")
    for pos, name, basin, h in items:
        lo, up = lower_trigram(h), upper_trigram(h)
        canon = "UC" if pos <= 30 else "LC"
        hu = hugua(h)
        hu_lo, hu_up = lower_trigram(hu), upper_trigram(hu)
        print(f"    KW#{pos:2d} [{canon}] {name:12s} ({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}) "
              f"→ 互={TRIGRAM_NAMES[hu_lo]}/{TRIGRAM_NAMES[hu_up]} basin={basin}")

# Depth-1 positions in the sequence
d1_positions = [pos for pos, name, basin, h in depth_groups.get(1, [])]
print(f"\n  Depth-1 positions: {d1_positions}")
print(f"  These are the 'gateway' hexagrams — one nuclear extraction from the attractor.")

# Are depth-1 positions clustered or spread?
if len(d1_positions) > 1:
    gaps = [d1_positions[i+1] - d1_positions[i] for i in range(len(d1_positions)-1)]
    print(f"  Gaps between depth-1 positions: {gaps}")
    print(f"  Mean gap: {np.mean(gaps):.1f}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. THE DEPTH-1 HEXAGRAMS — WHAT ARE THEY?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. DEPTH-1 IDENTITY — THE GATEWAYS")
print("=" * 70)

# Depth 0: Qian(#1), Kun(#2), JiJi(#63), WeiJi(#64)
# Depth 1: their 互 preimages that are themselves 1 step away

# For Kun basin depth-1: 互(h) ∈ {Kun, Gen/Zhen}
# For Qian basin depth-1: 互(h) ∈ {Qian, Dui/Xun}  
# For KanLi depth-1: 互(h) ∈ {JiJi, WeiJi, ...}

print(f"\n  Depth-1 hexagrams and their 互 values:")
for pos, name, basin, h in depth_groups.get(1, []):
    hu = hugua(h)
    hu_lo, hu_up = lower_trigram(hu), upper_trigram(hu)
    hu_hu = hugua(hu)
    hu_hu_lo, hu_hu_up = lower_trigram(hu_hu), upper_trigram(hu_hu)
    
    print(f"    {name:12s} (KW#{pos:2d}, {basin}): "
          f"互={TRIGRAM_NAMES[hu_lo]}/{TRIGRAM_NAMES[hu_up]} ({fmt6(hu)}) → "
          f"互²={TRIGRAM_NAMES[hu_hu_lo]}/{TRIGRAM_NAMES[hu_hu_up]} ({fmt6(hu_hu)})")

# ══════════════════════════════════════════════════════════════════════════════
# 5. BASIN RHYTHM — THE PULSE OF THE SEQUENCE  
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. BASIN RHYTHM — RUN LENGTHS AND PATTERN")
print("=" * 70)

# Encode basin as symbol
basin_symbols = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}
basin_line = ''.join(basin_symbols[b] for b in basin_seq)
print(f"\n  Basin sequence (visual):")
print(f"  UC: {basin_line[:30]}")
print(f"  LC: {basin_line[30:]}")

# Run-length encoding
runs = []
current = basin_seq[0]
count = 1
start_pos = 0
for i in range(1, 64):
    if basin_seq[i] == current:
        count += 1
    else:
        runs.append((current, count, start_pos))
        current = basin_seq[i]
        count = 1
        start_pos = i
runs.append((current, count, start_pos))

print(f"\n  Run-length encoding ({len(runs)} runs):")
for basin, length, start in runs:
    symbol = basin_symbols[basin]
    print(f"    {symbol}{basin:6s} × {length}  (KW {start+1}-{start+length})")

# Run length statistics by basin type
for basin_type in ['Kun', 'KanLi', 'Qian']:
    type_runs = [length for basin, length, _ in runs if basin == basin_type]
    if type_runs:
        print(f"\n  {basin_type} runs: {type_runs}")
        print(f"    count={len(type_runs)}, mean={np.mean(type_runs):.1f}, "
              f"max={max(type_runs)}, total={sum(type_runs)}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. PAIR-LEVEL BASIN PATTERN
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. PAIR-LEVEL BASIN PATTERN (32 pairs)")
print("=" * 70)

# Since 28/32 pairs share basin, we can mostly describe the sequence
# at pair level

pair_basins = []
for i in range(0, 64, 2):
    b1, b2 = basin_seq[i], basin_seq[i+1]
    if b1 == b2:
        pair_basins.append(b1)
    else:
        pair_basins.append(f"{b1}/{b2}")

print(f"\n  Pair basin sequence:")
for i, pb in enumerate(pair_basins):
    symbol = basin_symbols.get(pb, '⊗')
    canon = "UC" if i < 15 else "LC"
    print(f"    Pair {i:2d} [{canon}]: {symbol if symbol != '⊗' else '⊗'} {pb:12s}  "
          f"({kw_names[2*i]}/{kw_names[2*i+1]})")

# The cross-basin pairs
print(f"\n  Cross-basin pairs (⊗):")
for i, pb in enumerate(pair_basins):
    if '/' in str(pb):
        print(f"    Pair {i:2d}: {pb} ({kw_names[2*i]}/{kw_names[2*i+1]})")

# Pair-level runs
pair_runs = []
current = pair_basins[0]
count = 1
start = 0
for i in range(1, 32):
    if pair_basins[i] == current:
        count += 1
    else:
        pair_runs.append((current, count, start))
        current = pair_basins[i]
        count = 1
        start = i
pair_runs.append((current, count, start))

print(f"\n  Pair-level runs ({len(pair_runs)} runs):")
for basin, length, start in pair_runs:
    symbol = basin_symbols.get(basin, '⊗')
    end_pair = start + length - 1
    print(f"    {symbol} {basin:12s} × {length}  (pairs {start}-{end_pair}, "
          f"KW {2*start+1}-{2*(end_pair)+2})")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE ALTERNATION PATTERN
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. ALTERNATION AND RETURN STRUCTURE")
print("=" * 70)

# How does the sequence move between basins?
# Track transitions at pair level (ignoring cross-basin pairs)
simple_pairs = [(i, pb) for i, pb in enumerate(pair_basins) if '/' not in str(pb)]

print(f"\n  Pure-basin pair transitions:")
trans_count = Counter()
for j in range(len(simple_pairs) - 1):
    i1, b1 = simple_pairs[j]
    i2, b2 = simple_pairs[j+1]
    if i2 == i1 + 1:  # Adjacent pairs
        trans_count[(b1, b2)] += 1

for (b1, b2), c in sorted(trans_count.items(), key=lambda x: -x[1]):
    print(f"    {b1:6s} → {b2:6s}: {c}")

# How often does the sequence return to the same basin after excursion?
print(f"\n  Basin return structure:")
for basin_type in ['Kun', 'KanLi', 'Qian']:
    positions = [i for i in range(64) if basin_seq[i] == basin_type]
    if len(positions) > 1:
        gaps = [positions[j+1] - positions[j] for j in range(len(positions)-1)]
        print(f"    {basin_type}: positions={positions}")
        print(f"      gaps={gaps}, mean_gap={np.mean(gaps):.1f}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. THE MIDDLE LINES — TRADITIONAL SIGNIFICANCE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. MIDDLE LINES AND TRIGRAM RELATIONSHIP")
print("=" * 70)

# Bits 2 and 3 are:
# Bit 2 = top line of lower trigram
# Bit 3 = bottom line of upper trigram
# These are the "interface" lines — where the two trigrams meet.

# So the basin is determined by the INTERFACE between upper and lower trigrams!

print(f"\n  The basin is determined by the interface lines:")
print(f"  Bit 2 = top of lower trigram, Bit 3 = bottom of upper trigram")
print(f"  Interface (0,0): both yin at interface → Kun basin")
print(f"  Interface (1,1): both yang at interface → Qian basin")
print(f"  Interface mixed: → KanLi basin (oscillation)")

# Verify: what trigram combinations give each interface?
print(f"\n  Trigram pairs by interface type:")
for b2 in range(2):
    for b3 in range(2):
        interface = (b2, b3)
        basin = get_basin(b2 << 2 | b3 << 3)  # Minimal hex with these middle bits
        
        # Which lower trigrams have top bit = b2?
        lower_tris = [t for t in range(8) if (t >> 2) & 1 == b2]
        # Which upper trigrams have bottom bit = b3?
        upper_tris = [t for t in range(8) if (t >> 0) & 1 == b3]
        
        print(f"\n    Interface ({b2},{b3}) → {basin}:")
        print(f"      Lower trigrams (top={b2}): {[TRIGRAM_NAMES[t] for t in lower_tris]}")
        print(f"      Upper trigrams (bottom={b3}): {[TRIGRAM_NAMES[t] for t in upper_tris]}")
        print(f"      = {len(lower_tris)}×{len(upper_tris)} = {len(lower_tris)*len(upper_tris)} hexagrams")

# ══════════════════════════════════════════════════════════════════════════════
# 9. INTERFACE POLARITY AND FIVE-PHASE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("9. BASIN vs FIVE-PHASE RELATION")
print("=" * 70)

# Does the basin correlate with the five-phase relation?
basin_rel = defaultdict(Counter)
for h in range(64):
    basin = get_basin(h)
    lo, up = lower_trigram(h), upper_trigram(h)
    rel = five_phase_relation(TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up])
    basin_rel[basin][rel] += 1

rel_names = ["比和", "生体", "克体", "体生用", "体克用"]
print(f"\n  Five-phase distribution by basin:")
for basin in ['Kun', 'KanLi', 'Qian']:
    n = sum(basin_rel[basin].values())
    print(f"\n    {basin} ({n} hexagrams):")
    for r in rel_names:
        c = basin_rel[basin].get(r, 0)
        print(f"      {r}: {c}/{n} ({100*c/n:.0f}%)")
    ke = basin_rel[basin].get('克体', 0) + basin_rel[basin].get('体克用', 0)
    sheng = basin_rel[basin].get('生体', 0) + basin_rel[basin].get('体生用', 0)
    print(f"      Total 克: {ke}/{n} ({100*ke/n:.0f}%)")
    print(f"      Total 生: {sheng}/{n} ({100*sheng/n:.0f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 10. TRIGRAM INTERFACE AS 体用 BRIDGE
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("10. THE INTERFACE AS 体用 BRIDGE")
print("=" * 70)

# In 体用 theory:
# lower trigram = 体 (substance/self)
# upper trigram = 用 (function/other)
# The interface is where 体 meets 用.

# Interface (0,0) = yin-yin = receptive meeting → Kun basin (dissolution)
# Interface (1,1) = yang-yang = active meeting → Qian basin (consolidation)
# Interface mixed = asymmetric meeting → KanLi (oscillation/tension)

# How does this interact with 互?
# 互 takes lines 2,3,4,5. The interface lines ARE lines 3,4 (bits 2,3).
# So 互 reads the interface directly!

print(f"\n  互 reads the interface lines as its own inner core:")
print(f"  h = [bit0, bit1, |bit2, bit3|, bit4, bit5]")
print(f"                    ^^^^^^^^^^^^")
print(f"                    interface lines")
print(f"  互(h) = [bit1, bit2, bit3, bit2, bit3, bit4]")
print(f"                  ^^^^^^^^^^^^")
print(f"           interface appears in middle of 互!")
print(f"  So 互 amplifies the interface: it becomes the repeated core.")

# Verify: in 互(h), what are bits 2,3?
print(f"\n  Verification: 互 inner structure")
for h in [0b010101, 0b101010, 0b000000, 0b111111, 0b100001, 0b011110]:
    hu = hugua(h)
    h_b2, h_b3 = (h >> 2) & 1, (h >> 3) & 1
    hu_b2, hu_b3 = (hu >> 2) & 1, (hu >> 3) & 1
    print(f"    h={fmt6(h)}: interface=({h_b2},{h_b3}) → 互 interface=({hu_b2},{hu_b3})")

# More thorough: for all 64
print(f"\n  Interface transformation h → 互(h):")
interface_map = Counter()
for h in range(64):
    hu = hugua(h)
    h_if = ((h >> 2) & 1, (h >> 3) & 1)
    hu_if = ((hu >> 2) & 1, (hu >> 3) & 1)
    interface_map[(h_if, hu_if)] += 1

for (h_if, hu_if), count in sorted(interface_map.items()):
    h_basin = {(0,0): 'Kun', (1,1): 'Qian'}.get(h_if, 'KanLi')
    hu_basin = {(0,0): 'Kun', (1,1): 'Qian'}.get(hu_if, 'KanLi')
    print(f"    {h_if} ({h_basin:6s}) → {hu_if} ({hu_basin:6s}): {count} hexagrams")

# ══════════════════════════════════════════════════════════════════════════════
# 11. SUMMARY: THE SEQUENCE TELLS ITS OWN ATTRACTOR STORY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("11. SUMMARY")
print("=" * 70)

print(f"""
  THE INTERFACE DETERMINES THE BASIN:
  
  Line 3 (top of 体/lower) and Line 4 (bottom of 用/upper) = the interface.
  Where substance meets function:
    Both yin → dissolves to Kun (pure receptivity)
    Both yang → consolidates to Qian (pure activity)  
    Mixed → oscillates as Kan↔Li (irreducible tension)
  
  互 READS AND AMPLIFIES THE INTERFACE:
  The nuclear hexagram places the interface lines at its own center.
  Each 互 application re-reads the interface → the interface echoes inward.
  
  THE SEQUENCE AS ATTRACTOR NARRATIVE:
  Opens with the fixed points (Qian/Kun, #1-2)
  Traverses the basins with Kun-heavy UC, Qian-heavy LC  
  Closes with the cycle (JiJi/WeiJi, #63-64)
  
  4 cross-basin pairs mark structural boundaries:
    #1-2 (Qian/Kun): opening gate
    #27-28 (Yi/Da Guo): penultimate UC 
    #29-30 (Kan/Li): canon boundary
    #61-62 (Zhong Fu/Xiao Guo): penultimate LC
""")
