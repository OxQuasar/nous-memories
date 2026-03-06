"""
All remaining probes in one script.

1. Basin walk information — compressibility
2. Basin × developmental priority 
3. 变 circuit through basins
4. Doubled vs alternating trigrams
5. Facing-line × Later Heaven
6. Longer-range basin correlations
7. The 6 direct Kun↔Qian transitions
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np
import zlib
import json

from sequence import KING_WEN
from cycle_algebra import (
    NUM_HEX, MASK_ALL,
    lower_trigram, upper_trigram, hugua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES,
    five_phase_relation, reverse6,
    hamming6, fmt6, fmt3,
)

# ══════════════════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════════════════

kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    val = sum(b[j] << j for j in range(6))
    kw_hex.append(val)
    kw_names.append(KING_WEN[i][1])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    elif b2 == 1 and b3 == 1: return 'Qian'
    else: return 'KanLi'

basin_code = {'Kun': 0, 'KanLi': 1, 'Qian': 2}
basin_sym = {'Kun': '○', 'KanLi': '◎', 'Qian': '●'}

kw_basins = [get_basin(kw_hex[i]) for i in range(64)]
kw_basin_coded = [basin_code[b] for b in kw_basins]

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 1: BASIN WALK INFORMATION
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("PROBE 1: BASIN WALK INFORMATION CONTENT")
print("=" * 70)

# The basin sequence as a ternary string
basin_str = ''.join(str(c) for c in kw_basin_coded)
print(f"\n  Basin sequence (0=Kun, 1=KanLi, 2=Qian):")
print(f"  {basin_str}")
print(f"  Visual: {''.join(basin_sym[b] for b in kw_basins)}")

# Shannon entropy
counts = Counter(kw_basin_coded)
n = 64
entropy = -sum((c/n) * np.log2(c/n) for c in counts.values())
max_entropy = np.log2(3)  # If uniform ternary
print(f"\n  Symbol frequencies: Kun={counts[0]}/64, KanLi={counts[1]}/64, Qian={counts[2]}/64")
print(f"  Shannon entropy: {entropy:.3f} bits/symbol (max={max_entropy:.3f})")
print(f"  Efficiency: {100*entropy/max_entropy:.1f}%")

# Conditional entropy (bigram)
bigram_counts = Counter()
for i in range(63):
    bigram_counts[(kw_basin_coded[i], kw_basin_coded[i+1])] += 1

cond_entropy = 0
for a in range(3):
    a_count = sum(bigram_counts.get((a, b), 0) for b in range(3))
    if a_count == 0:
        continue
    for b in range(3):
        p_ab = bigram_counts.get((a, b), 0) / 63
        p_a = a_count / 63
        if p_ab > 0:
            cond_entropy -= p_ab * np.log2(p_ab / p_a)

print(f"  Conditional entropy H(X|X-1): {cond_entropy:.3f} bits/symbol")
print(f"  Predictability gain: {entropy - cond_entropy:.3f} bits")

# Compression ratio
raw_bytes = basin_str.encode()
compressed = zlib.compress(raw_bytes, 9)
print(f"\n  Compression: {len(raw_bytes)} → {len(compressed)} bytes")
print(f"  Ratio: {len(compressed)/len(raw_bytes):.2f}")

# Compare with random
np.random.seed(42)
random_ratios = []
for _ in range(10000):
    perm = np.random.permutation(64)
    random_basins = [basin_code[get_basin(perm[i])] for i in range(64)]
    raw = ''.join(str(c) for c in random_basins).encode()
    comp = zlib.compress(raw, 9)
    random_ratios.append(len(comp) / len(raw))

pctl = np.mean(np.array(random_ratios) <= len(compressed)/len(raw_bytes)) * 100
print(f"  Random compression ratio: mean={np.mean(random_ratios):.3f}")
print(f"  KW percentile: {pctl:.1f}th (lower = more compressible)")

# Run-length encoding comparison
runs = []
current = kw_basin_coded[0]
count = 1
for i in range(1, 64):
    if kw_basin_coded[i] == current:
        count += 1
    else:
        runs.append((current, count))
        current = kw_basin_coded[i]
        count = 1
runs.append((current, count))
rle_length = len(runs)

np.random.seed(42)
random_rle = []
for _ in range(10000):
    perm = np.random.permutation(64)
    basins = [basin_code[get_basin(perm[i])] for i in range(64)]
    r = 1
    rle = 1
    for i in range(1, 64):
        if basins[i] != basins[i-1]:
            rle += 1
    random_rle.append(rle)

pctl_rle = np.mean(np.array(random_rle) <= rle_length) * 100
print(f"\n  RLE runs: KW={rle_length}, random mean={np.mean(random_rle):.1f}")
print(f"  KW percentile: {pctl_rle:.1f}th (lower = fewer runs = more structured)")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 2: BASIN × DEVELOPMENTAL PRIORITY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PROBE 2: BASIN × DEVELOPMENTAL PRIORITY")
print("=" * 70)

# From spaceprobe lead 2: Upper Canon uses algebra (kernel opposition metrics),
# Lower Canon uses meaning (developmental priority).
# Question: is Kun basin = algebra-friendly? Qian basin = meaning-friendly?

# We don't have the meaning clarity scores directly, but we can check:
# Do hexagrams in Kun basin have different kernel properties than Qian basin?

# Compute kernel distance to complement for each hexagram
# (a key metric from the opposition theory)
for basin_type in ['Kun', 'KanLi', 'Qian']:
    basin_hexes = [kw_hex[i] for i in range(64) if kw_basins[i] == basin_type]
    
    # Kernel distribution of bridges within this basin's KW subsequence
    basin_positions = [i for i in range(64) if kw_basins[i] == basin_type]
    
    # Five-phase relations
    rels = Counter()
    for h in basin_hexes:
        lo, up = lower_trigram(h), upper_trigram(h)
        rel = five_phase_relation(TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up])
        rels[rel] += 1
    
    n = len(basin_hexes)
    ke = rels.get('克体', 0) + rels.get('体克用', 0)
    sheng = rels.get('生体', 0) + rels.get('体生用', 0)
    bihe = rels.get('比和', 0)
    
    print(f"\n  {basin_type} basin ({n} hexagrams in KW):")
    print(f"    克: {ke}/{n} ({100*ke/n:.0f}%)  生: {sheng}/{n} ({100*sheng/n:.0f}%)  比和: {bihe}/{n} ({100*bihe/n:.0f}%)")
    
    # Which canon are they in?
    uc_count = sum(1 for i in basin_positions if i < 30)
    lc_count = sum(1 for i in basin_positions if i >= 30)
    print(f"    UC: {uc_count}  LC: {lc_count}")

# The key question: is there a basin that correlates with "algebraically extreme" 
# vs "meaning-organized"?
# UC body (#3-26) is Kun=8 KanLi=14 Qian=2 → UC prefers Kun
# LC body (#31-60) is Kun=4 KanLi=16 Qian=10 → LC prefers Qian
# UC is algebraically optimized → Kun basin = algebraic?
# LC is meaning-organized → Qian basin = meaning?

print(f"\n  Interpretation:")
print(f"  UC (algebraic) is Kun-attracted: emptiness/receptivity ↔ algebraic purity")
print(f"  LC (meaning) is Qian-attracted: fullness/activity ↔ semantic richness")
print(f"  This is consistent: algebra strips away, meaning fills in.")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 3: 变 CIRCUIT THROUGH BASINS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PROBE 3: 本→互→变 BASIN CIRCUIT")
print("=" * 70)

# For each KW pair: h1=本, h2=变 (or vice versa)
# What's the basin trajectory 本basin → 互basin → 变basin?

print(f"\n  Pair basin trajectories (本→互→变):")
traj_counter = Counter()
for i in range(0, 64, 2):
    h1, h2 = kw_hex[i], kw_hex[i+1]
    hu1 = hugua(h1)
    
    b_ben = get_basin(h1)
    b_hu = get_basin(hu1)
    b_bian = get_basin(h2)
    
    traj = (b_ben, b_hu, b_bian)
    traj_counter[traj] += 1
    
    canon = "UC" if i < 30 else "LC"
    traj_str = f"{basin_sym[b_ben]}{basin_sym[b_hu]}{basin_sym[b_bian]}"
    print(f"    Pair {i//2:2d} [{canon}]: {kw_names[i]:12s}→{kw_names[i+1]:12s}  "
          f"{traj_str}  {b_ben}→{b_hu}→{b_bian}")

print(f"\n  Trajectory frequencies:")
for traj, count in sorted(traj_counter.items(), key=lambda x: -x[1]):
    traj_str = f"{basin_sym[traj[0]]}{basin_sym[traj[1]]}{basin_sym[traj[2]]}"
    print(f"    {traj_str} ({traj[0]}→{traj[1]}→{traj[2]}): {count}")

# Does 互 always change basin?
hu_changes = sum(1 for i in range(0, 64, 2) 
                 if get_basin(kw_hex[i]) != get_basin(hugua(kw_hex[i])))
print(f"\n  本→互 basin change: {hu_changes}/32 pairs ({100*hu_changes/32:.0f}%)")

# Does 变 return to 本's basin?
returns = sum(1 for i in range(0, 64, 2) 
              if get_basin(kw_hex[i]) == get_basin(kw_hex[i+1]))
print(f"  本→变 same basin: {returns}/32 pairs ({100*returns/32:.0f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 4: DOUBLED vs ALTERNATING TRIGRAMS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PROBE 4: DOUBLED vs ALTERNATING TRIGRAM HEXAGRAMS")
print("=" * 70)

# Doubled: lower == upper (8 hexagrams: Qian/Qian, Kun/Kun, etc.)
# Alternating: lines strictly alternate (like JiJi=010101, WeiJi=101010, etc.)
# Self-interface: lower trigram == upper trigram

doubled = [h for h in range(64) if lower_trigram(h) == upper_trigram(h)]
print(f"\n  Doubled trigrams (lower=upper): {len(doubled)}")
for h in doubled:
    t = lower_trigram(h)
    basin = get_basin(h)
    kw_pos = kw_hex.index(h) + 1
    # Interface: top of lower = bottom of upper
    top = (t >> 2) & 1
    bot = t & 1
    print(f"    {TRIGRAM_NAMES[t]:4s}/{TRIGRAM_NAMES[t]:4s} ({fmt6(h)}) KW#{kw_pos:2d} "
          f"interface=({top},{bot}) basin={basin}")

doubled_basins = Counter(get_basin(h) for h in doubled)
print(f"\n  Doubled basin distribution: {dict(doubled_basins)}")

# For doubled: interface = (top_of_t, bottom_of_t)
# If top == bottom: basin is Kun or Qian (homogeneous)
# If top != bottom: basin is KanLi
print(f"\n  Doubled trigrams interface analysis:")
for h in doubled:
    t = lower_trigram(h)
    top = (t >> 2) & 1
    bot = t & 1
    basin = get_basin(h)
    print(f"    {TRIGRAM_NAMES[t]:4s}: top={top} bot={bot} → {'same' if top==bot else 'different'} → {basin}")

# Reversed trigrams (upper = reverse of lower)
reversed_trig = [h for h in range(64) if reverse6(h) == h]
print(f"\n  Self-reverse hexagrams (upper = reverse(lower)): {len(reversed_trig)}")
for h in reversed_trig:
    lo, up = lower_trigram(h), upper_trigram(h)
    basin = get_basin(h)
    kw_pos = kw_hex.index(h) + 1
    print(f"    {TRIGRAM_NAMES[lo]:4s}/{TRIGRAM_NAMES[up]:4s} ({fmt6(h)}) KW#{kw_pos:2d} basin={basin}")

# Pure alternating hexagrams (no two adjacent lines same)
alternating = []
for h in range(64):
    bits = [(h >> i) & 1 for i in range(6)]
    is_alt = all(bits[i] != bits[i+1] for i in range(5))
    if is_alt:
        alternating.append(h)

print(f"\n  Pure alternating hexagrams (no adjacent same): {len(alternating)}")
for h in alternating:
    lo, up = lower_trigram(h), upper_trigram(h)
    basin = get_basin(h)
    kw_pos = kw_hex.index(h) + 1
    print(f"    {TRIGRAM_NAMES[lo]:4s}/{TRIGRAM_NAMES[up]:4s} ({fmt6(h)}) KW#{kw_pos:2d} basin={basin}")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 5: FACING-LINE × LATER HEAVEN
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PROBE 5: FACING-LINE × LATER HEAVEN ARRANGEMENT")
print("=" * 70)

# Later Heaven (King Wen) compass:
# S=Li, N=Kan, E=Zhen, W=Dui, SE=Xun, NE=Gen, SW=Kun, NW=Qian
later_heaven = {
    'S': 0b101,   # Li
    'SW': 0b000,  # Kun
    'W': 0b110,   # Dui
    'NW': 0b111,  # Qian
    'N': 0b010,   # Kan
    'NE': 0b001,  # Gen
    'E': 0b100,   # Zhen
    'SE': 0b011,  # Xun
}

# Facing-line groups:
# As lower (top bit): yin={Kun,Gen,Kan,Xun}(0), yang={Zhen,Li,Dui,Qian}(1)
# As upper (bot bit): yin={Kun,Kan,Zhen,Dui}(0), yang={Gen,Xun,Li,Qian}(1)

print(f"\n  Later Heaven compass with facing-line classification:")
directions = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
for d in directions:
    t = later_heaven[d]
    top = (t >> 2) & 1
    bot = t & 1
    print(f"    {d:3s}: {TRIGRAM_NAMES[t]:4s} "
          f"facing_lower={'●' if top else '○'} "
          f"facing_upper={'●' if bot else '○'}")

# Check: do the cardinal directions have a facing-line pattern?
print(f"\n  Cardinal directions (N,S,E,W):")
for d in ['N', 'S', 'E', 'W']:
    t = later_heaven[d]
    top = (t >> 2) & 1
    bot = t & 1
    print(f"    {d}: {TRIGRAM_NAMES[t]:4s} lower_facing={'●' if top else '○'} upper_facing={'●' if bot else '○'}")

print(f"\n  Intercardinal directions (NE,SE,SW,NW):")
for d in ['NE', 'SE', 'SW', 'NW']:
    t = later_heaven[d]
    top = (t >> 2) & 1
    bot = t & 1
    print(f"    {d}: {TRIGRAM_NAMES[t]:4s} lower_facing={'●' if top else '○'} upper_facing={'●' if bot else '○'}")

# Check: N-S axis facing opposition?
n_t = later_heaven['N']  # Kan
s_t = later_heaven['S']  # Li
print(f"\n  N-S axis (Kan↔Li):")
print(f"    Lower facing opposite: {((n_t>>2)&1) != ((s_t>>2)&1)}")
print(f"    Upper facing opposite: {(n_t&1) != (s_t&1)}")

# E-W axis
e_t = later_heaven['E']  # Zhen
w_t = later_heaven['W']  # Dui
print(f"  E-W axis (Zhen↔Dui):")
print(f"    Lower facing opposite: {((e_t>>2)&1) != ((w_t>>2)&1)}")
print(f"    Upper facing opposite: {(e_t&1) != (w_t&1)}")

# NW-SE axis
nw_t = later_heaven['NW']  # Qian
se_t = later_heaven['SE']  # Xun
print(f"  NW-SE axis (Qian↔Xun):")
print(f"    Lower facing opposite: {((nw_t>>2)&1) != ((se_t>>2)&1)}")
print(f"    Upper facing opposite: {(nw_t&1) != (se_t&1)}")

# NE-SW axis
ne_t = later_heaven['NE']  # Gen
sw_t = later_heaven['SW']  # Kun
print(f"  NE-SW axis (Gen↔Kun):")
print(f"    Lower facing opposite: {((ne_t>>2)&1) != ((sw_t>>2)&1)}")
print(f"    Upper facing opposite: {(ne_t&1) != (sw_t&1)}")

# Which compass positions have which facing types?
print(f"\n  Compass positions by facing type:")
for face_type, label in [('○○', 'Both yin'), ('●●', 'Both yang'), 
                          ('○●', 'Yin/Yang'), ('●○', 'Yang/Yin')]:
    positions = []
    for d in directions:
        t = later_heaven[d]
        top = (t >> 2) & 1
        bot = t & 1
        sym = ('●' if top else '○') + ('●' if bot else '○')
        if sym == face_type:
            positions.append(d)
    print(f"    {face_type} ({label}): {positions}")

# What basin does a doubled trigram from each direction produce?
print(f"\n  Doubled trigrams by compass direction:")
for d in directions:
    t = later_heaven[d]
    h = t | (t << 3)  # doubled hexagram
    basin = get_basin(h)
    print(f"    {d:3s} {TRIGRAM_NAMES[t]:4s}/{TRIGRAM_NAMES[t]:4s}: basin={basin}")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 6: LONGER-RANGE BASIN CORRELATIONS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PROBE 6: LONGER-RANGE BASIN CORRELATIONS")
print("=" * 70)

# Autocorrelation of basin sequence
print(f"\n  Basin autocorrelation (fraction same basin at lag k):")
for lag in range(1, 17):
    same = sum(1 for i in range(64 - lag) if kw_basins[i] == kw_basins[i + lag])
    total = 64 - lag
    frac = same / total
    
    # Expected if random
    p_same = (16/64)**2 + (32/64)**2 + (16/64)**2  # = 0.375
    bar = '█' * int(frac * 40)
    print(f"    lag {lag:2d}: {frac:.3f} (expected {p_same:.3f}) {bar}")

# Mutual information between basins at distance k
print(f"\n  Basin pair correlation by lag:")
for lag in [2, 4, 6, 8, 16, 32]:
    pair_counts = Counter()
    for i in range(64 - lag):
        pair_counts[(kw_basins[i], kw_basins[i+lag])] += 1
    
    # Chi-squared test
    total = 64 - lag
    expected = {}
    row_totals = Counter(kw_basins[i] for i in range(64 - lag))
    col_totals = Counter(kw_basins[i+lag] for i in range(64 - lag))
    
    chi2 = 0
    for b1 in ['Kun', 'KanLi', 'Qian']:
        for b2 in ['Kun', 'KanLi', 'Qian']:
            obs = pair_counts.get((b1, b2), 0)
            exp = row_totals[b1] * col_totals[b2] / total
            if exp > 0:
                chi2 += (obs - exp)**2 / exp
    
    print(f"    Lag {lag:2d}: χ² = {chi2:.2f} (>9.49 = significant at p<0.05)")

# ══════════════════════════════════════════════════════════════════════════════
# PROBE 7: THE 6 DIRECT KUN↔QIAN TRANSITIONS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("PROBE 7: DIRECT KUN↔QIAN TRANSITIONS (SKIPPING KanLi)")
print("=" * 70)

direct_transitions = []
for i in range(63):
    b1, b2 = kw_basins[i], kw_basins[i+1]
    if (b1 == 'Kun' and b2 == 'Qian') or (b1 == 'Qian' and b2 == 'Kun'):
        h1, h2 = kw_hex[i], kw_hex[i+1]
        xor = h1 ^ h2
        kernel = mirror_kernel(xor)
        k_name = kernel_names[kernel]
        
        direct_transitions.append({
            'step': i+1,
            'h1': h1, 'h2': h2,
            'n1': kw_names[i], 'n2': kw_names[i+1],
            'b1': b1, 'b2': b2,
            'kernel': k_name,
            'hamming': hamming6(h1, h2),
        })

print(f"\n  {len(direct_transitions)} direct Kun↔Qian transitions:")
for t in direct_transitions:
    lo1, up1 = TRIGRAM_NAMES[lower_trigram(t['h1'])], TRIGRAM_NAMES[upper_trigram(t['h1'])]
    lo2, up2 = TRIGRAM_NAMES[lower_trigram(t['h2'])], TRIGRAM_NAMES[upper_trigram(t['h2'])]
    
    # What changed at the interface?
    xor = t['h1'] ^ t['h2']
    xor_b2 = (xor >> 2) & 1
    xor_b3 = (xor >> 3) & 1
    
    print(f"    Step {t['step']:2d}→{t['step']+1:2d}: "
          f"{t['n1']:12s}({t['b1']}) → {t['n2']:12s}({t['b2']}) "
          f"kernel={t['kernel']:3s} d={t['hamming']} "
          f"interface_xor=({xor_b2},{xor_b3})")

# What do they have in common?
print(f"\n  Analysis:")
kernels = Counter(t['kernel'] for t in direct_transitions)
distances = [t['hamming'] for t in direct_transitions]
print(f"    Kernels: {dict(kernels)}")
print(f"    Distances: {distances}")

# All must have both interface bits flipping (xor = 1,1)
# because that's the only way to go Kun(0,0)↔Qian(1,1)
all_both_flip = all(
    ((t['h1'] ^ t['h2']) >> 2) & 1 == 1 and 
    ((t['h1'] ^ t['h2']) >> 3) & 1 == 1
    for t in direct_transitions
)
print(f"    All have both interface bits flipping: {all_both_flip}")
print(f"    (This is algebraically necessary: (0,0)↔(1,1) requires both to flip)")

# What are the non-interface bits doing?
print(f"\n  Non-interface bit changes:")
for t in direct_transitions:
    xor = t['h1'] ^ t['h2']
    bits = [(xor >> i) & 1 for i in range(6)]
    non_if = [bits[0], bits[1], bits[4], bits[5]]  # bits 0,1,4,5
    print(f"    Step {t['step']:2d}: xor={fmt6(xor)} non-interface={non_if} "
          f"(outer={bits[0]},{bits[5]} middle={bits[1]},{bits[4]})")

# Where are these transitions in the sequence?
print(f"\n  Positions in sequence:")
positions = [t['step'] for t in direct_transitions]
print(f"    {positions}")
uc_count = sum(1 for p in positions if p <= 30)
lc_count = sum(1 for p in positions if p > 30)
print(f"    UC: {uc_count}, LC: {lc_count}")

# Are they near the self-reverse skeleton?
skeleton = [1, 2, 27, 28, 29, 30, 61, 62]
print(f"\n  Distance to nearest skeleton position:")
for t in direct_transitions:
    min_dist = min(abs(t['step'] - s) for s in skeleton)
    nearest = min(skeleton, key=lambda s: abs(t['step'] - s))
    print(f"    Step {t['step']}: distance {min_dist} to #{nearest}")

print(f"\n{'=' * 70}")
print("PROBES COMPLETE")
print("=" * 70)
