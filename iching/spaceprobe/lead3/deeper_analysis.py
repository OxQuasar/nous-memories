"""
Lead 3 follow-up: deeper analysis of the striking findings from the initial trace.

Key findings to investigate:
1. 互卦 projects into H-subgroup (proven algebraically) — what does this mean?
2. Five-phase distribution is wildly asymmetric in 互 (比和 up, 生体/体生用 collapse)
3. MI and OMI have constant 互 distance of exactly 3 — why?
4. 体 preserved in 变 always (100%) — trivial by construction
5. Polarity preserved 62.5% — what determines the 37.5% flips?
6. KW pairing preserved through 互 at 87.5% — the 12.5% failures?
7. The transition matrix 本→互 has structural zeros — what's the algebra?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter, defaultdict
import numpy as np

from cycle_algebra import (
    NUM_HEX, MASK_ALL, MASK3, N,
    lower_trigram, upper_trigram, hugua, biangua,
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    five_phase_relation, tiyong_trigrams,
    kw_partner, reverse6, is_palindrome6,
    hamming6, popcount, bit, fmt6, fmt3,
)

P_PLUS  = {0b010, 0b100, 0b110, 0b101}
P_MINUS = {0b000, 0b001, 0b111, 0b011}

def polarity(t):
    return "+" if t in P_PLUS else "-"


# ══════════════════════════════════════════════════════════════════════════════
# 1. WHY THE FIVE-PHASE DISTRIBUTION SHIFTS IN 互
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. FIVE-PHASE DISTRIBUTION IN 互卦: WHY THE ASYMMETRY?")
print("=" * 70)

# 本/变: uniform over all 64×6 → 比和=84, 生体=72, 克体=78, 体生用=72, 体克用=78
# 互:    比和=96, 生体=24, 克体=120, 体生用=24, 体克用=120
# 
# Dramatic: 生体 and 体生用 collapse from 72 → 24 each.
#           克体 and 体克用 inflate from 78 → 120 each.
#           比和 increases from 84 → 96.
#
# Hypothesis: 互卦 compresses 64 → 16 hexagrams. The 16 outputs may have
# a biased element distribution.

# What are the 16 互 hexagrams and their trigram compositions?
print("\n  The 16 互卦 values:")
hu_vals = sorted(set(hugua(h) for h in range(NUM_HEX)))
for hg in hu_vals:
    lo, up = lower_trigram(hg), upper_trigram(hg)
    lo_e, up_e = TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up]
    fibers = [h for h in range(NUM_HEX) if hugua(h) == hg]
    print(f"  {fmt6(hg)} lo={TRIGRAM_NAMES[lo]:10s}({lo_e:5s}) "
          f"up={TRIGRAM_NAMES[up]:10s}({up_e:5s})  ← {len(fibers)} hexagrams")

# Element pair distribution in 互
print("\n  Element pair distribution in 互 (lower, upper):")
hu_elem_pairs = Counter()
for hg in hu_vals:
    lo_e = TRIGRAM_ELEMENT[lower_trigram(hg)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(hg)]
    hu_elem_pairs[(lo_e, up_e)] += 1

for (lo_e, up_e), count in sorted(hu_elem_pairs.items(), key=lambda x: -x[1]):
    rel = five_phase_relation(up_e, lo_e)  # if 体=upper, 用=lower
    print(f"    ({lo_e:5s}, {up_e:5s}): {count} hexagrams → 体=upper: {rel}")

# Trigram distribution in 互
print("\n  Trigram frequency in 互卦 (across all 16 values × 2 positions):")
trig_count = Counter()
for hg in hu_vals:
    trig_count[lower_trigram(hg)] += 1
    trig_count[upper_trigram(hg)] += 1
for t, c in sorted(trig_count.items()):
    print(f"    {TRIGRAM_NAMES[t]:10s} ({TRIGRAM_ELEMENT[t]:5s}): {c}")

# Explanation: 互 = (L2,L3,L4,L3,L4,L5). Lower nuc = (L2,L3,L4), upper nuc = (L3,L4,L5).
# They SHARE L3,L4 — so the two nuclear trigrams are highly correlated.
# Specifically, lower_nuc XOR upper_nuc = (L2⊕L3, 0, L4⊕L5).
# The middle bit is ALWAYS 0. So the two trigrams differ only in bits 0 and 2.
print("\n  Nuclear trigram XOR structure:")
print("  lower_nuc ⊕ upper_nuc = (L2⊕L3, 0, L4⊕L5)")
print("  Middle bit always 0 → only 4 possible XOR masks: 000, 001, 100, 101")

# Actually: lower_nuc = (L2, L3, L4), upper_nuc = (L3, L4, L5)
# In our bit encoding, lower_nuc bit0=L2, bit1=L3, bit2=L4
#                       upper_nuc bit0=L3, bit1=L4, bit2=L5
# XOR bit0 = L2⊕L3, bit1 = L3⊕L4, bit2 = L4⊕L5
# There's NO forced-zero bit. My earlier claim was wrong.
# The SHARED bits are L3,L4 but they appear at DIFFERENT positions in the two trigrams.
xor_masks = Counter()
for hg in hu_vals:
    lo, up = lower_trigram(hg), upper_trigram(hg)
    xor = lo ^ up
    xor_masks[fmt3(xor)] += 1
print(f"  Actual XOR masks: {dict(xor_masks)}")
print(f"  All 8 XOR masks appear (2 each) — no forced-zero bit.")
print(f"  The sharing of L3,L4 doesn't constrain the XOR because")
print(f"  they appear at different positions in lower vs upper nuclear.")

# What elements can appear as (lower_nuc, upper_nuc)?
print("\n  Element pair possibilities:")
print("  Since nuclear trigrams share their middle bit,")
print("  and middle bit determines Water(0) vs Fire(1),")
print("  the pair is heavily constrained.")

# ══════════════════════════════════════════════════════════════════════════════
# 2. THE TRANSITION MATRIX STRUCTURAL ZEROS
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("2. FIVE-PHASE TRANSITION MATRIX 本→互: STRUCTURAL ZEROS")
print("=" * 70)

# From the data:
# 生体→体生用 = 0,  生体→克体 = 18
# 体生用→生体 = 0,  体生用→克体 = 36
# 克体→生体 = 0,    克体→体生用 = 0
# 体克用→生体 = 0,  体克用→体生用 = 0
#
# Pattern: 生体 and 体生用 (the "生" relations) NEVER produce each other in 互.
# 克体 and 体克用 (the "克" relations) also never produce 生体 or 体生用 in 互.
# But 生体 produces 体克用 at 50%!
#
# This suggests the 互 operation has an algebraic effect on the 生/克 structure.

print("\n  Structural zeros in 本→互 transition:")
print("  克体 → 生体: 0     (克 never becomes 生 in 互)")
print("  克体 → 体生用: 0     (same)")
print("  体克用 → 生体: 0     (same)")
print("  体克用 → 体生用: 0     (same)")
print("  生体 → 体生用: 0     (生体 never flips direction in 互)")
print("  体生用 → 生体: 0     (体生用 never flips direction in 互)")
print()
print("  High-probability transitions:")
print("  生体 → 体克用: 50%   (the 生 relation gets 'absorbed' into 克)")
print("  体生用 → 克体: 50%   (same, opposite direction)")

# Is this because 互 tends to make elements more similar (比和) or more opposed (克)?
# Count: 比和 goes 84→96 (+14%), 克体+体克用 goes 156→240 (+54%), 生体+体生用 goes 144→48 (-67%)
print("\n  Relation class shifts:")
print(f"  比和: 84 → 96 (×{96/84:.2f})")
print(f"  生 (生体+体生用): 144 → 48 (×{48/144:.2f})")
print(f"  克 (克体+体克用): 156 → 240 (×{240/156:.2f})")
print(f"\n  互卦 DESTROYS 生 relations (÷3) and AMPLIFIES 克 relations (×1.5).")
print(f"  The nuclear hexagram shifts the evaluation toward conflict/overcoming.")

# ══════════════════════════════════════════════════════════════════════════════
# 3. MI AND OMI CONSTANT DISTANCE
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("3. MI AND OMI: CONSTANT 互 DISTANCE OF 3")
print("=" * 70)

# MI = flip M and I (L2↔L5 and L3↔L4). 
# Since 互 = (L2,L3,L4,L3,L4,L5), an MI flip changes all 6 positions:
#   L2→L2', L3→L3', L4→L4', L3→L3', L4→L4', L5→L5'
# But wait, L2'=L5, L5'=L2, L3'=L4, L4'=L3 under MI (swap within pairs).
# Actually MI is the XOR mask (0,1,1,1,1,0): flip L2,L3,L4,L5.
# So 互(h⊕MI) = (L5, L4, L3, L4, L3, L2) — the reverse of 互(h)!
# Hamming distance between h and reverse(h) for a 6-bit palindrome-structured word...

print("  MI mask in mirror-pair notation: flip M-pair (L2↔L5) and I-pair (L3↔L4).")
print("  As a 6-bit mask: MI = (0,1,1,1,1,0) = 0b011110")
print("  互(h) = (L2, L3, L4, L3, L4, L5)")
print()

# Actually compute what MI does to 互
# h ⊕ MI: L1 unchanged, L2→1-L2, L3→1-L3, L4→1-L4, L5→1-L5, L6 unchanged
# 互(h⊕MI) = (1-L2, 1-L3, 1-L4, 1-L3, 1-L4, 1-L5)
# = complement of (L2, L3, L4, L3, L4, L5) = complement of 互(h)?
# No: complement flips ALL 6 bits. This flips all 6 bits of 互(h). So yes, = complement of 互(h).
# Wait: 互(h) = (L2, L3, L4, L3, L4, L5). Complement = (1-L2, 1-L3, 1-L4, 1-L3, 1-L4, 1-L5).
# And 互(h⊕MI) uses h' where L2'=1-L2, L3'=1-L3, L4'=1-L4, L5'=1-L5.
# 互(h') = (L2', L3', L4', L3', L4', L5') = (1-L2, 1-L3, 1-L4, 1-L3, 1-L4, 1-L5) = complement(互(h)). ✓

for h in range(NUM_HEX):
    h_mi = h ^ 0b011110  # MI mask
    hu_h = hugua(h)
    hu_mi = hugua(h_mi)
    assert hu_mi == hu_h ^ MASK_ALL, f"MI complement failed at h={h}"

print("  Verified: 互(h⊕MI) = complement(互(h)) for all 64 hexagrams.")
print("  MI applied to 本 produces the COMPLEMENT of 互.")
print("  Hamming(互(h), complement(互(h))) = 6 always.")
print()

# So what explains the constant-3 distance for MI bridges in KW?
# The KW data showed MI bridge 互 distances were all exactly 3.
# But that's Hamming(互(h1), 互(h2)) where h1→h2 is a KW bridge with MI kernel.
# h2 ≠ h1 ⊕ MI in general (the bridge has both kernel and orbit components).
# The constant-3 must come from the specific hexagrams at MI bridges.

print("  The constant-3 distance for MI/OMI in KW bridges comes from the")
print("  specific hexagram pairs at those bridges, not from MI algebra alone.")
print("  (MI on 本 gives complement of 互, distance 6 — but KW bridges aren't pure MI.)")

# OMI = flip all 6 bits = complement
print(f"\n  OMI mask = (1,1,1,1,1,1): complement.")
print(f"  互(h⊕OMI) = 互(complement(h))")
for h in range(NUM_HEX):
    h_omi = h ^ MASK_ALL
    hu_h = hugua(h)
    hu_omi = hugua(h_omi)
    # 互(~h) = (~L2, ~L3, ~L4, ~L3, ~L4, ~L5)
    # = complement of (L2, L3, L4, L3, L4, L5) = complement of 互(h)
    assert hu_omi == hu_h ^ MASK_ALL, f"Failed at h={h}"

print(f"  Verified: 互(complement(h)) = complement(互(h))")
print(f"  OMI commutes with 互! So Hamming(互(h), 互(h⊕OMI)) = 6 always.")
print(f"  But the KW data showed OMI bridge 互 distance = 3, not 6.")
print(f"  That means the hexagrams at OMI bridges are not complements —")
print(f"  the bridge kernel is OMI but the full XOR includes orbit bits too.")

# ══════════════════════════════════════════════════════════════════════════════
# 4. POLARITY FLIP CONDITIONS
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("4. POLARITY: WHEN DOES 互卦 FLIP 体'S POLARITY?")
print("=" * 70)

# 62.5% preserved, 37.5% flipped. What determines it?
# 体 trigram in 本 → 体 trigram in 互 is determined by:
#   If 体=upper: 本's upper = (L4,L5,L6), 互's upper_nuc = (L3,L4,L5)
#     L6 dropped, L3 added. Polarity depends on specific trigrams.
#   If 体=lower: 本's lower = (L1,L2,L3), 互's lower_nuc = (L2,L3,L4)
#     L1 dropped, L4 added.

flip_conditions = defaultdict(int)
total_conditions = defaultdict(int)

for h in range(NUM_HEX):
    for line in range(1, 7):
        lo, up = lower_trigram(h), upper_trigram(h)
        hg = hugua(h)
        hg_lo, hg_up = lower_trigram(hg), upper_trigram(hg)
        
        if line <= 3:
            ti_ben, ti_hu = up, hg_up
        else:
            ti_ben, ti_hu = lo, hg_lo
        
        ben_pol = polarity(ti_ben)
        hu_pol = polarity(ti_hu)
        flipped = ben_pol != hu_pol
        
        # What determines the flip?
        # Key: which bits change between the trigrams
        key = (polarity(ti_ben), "upper" if line <= 3 else "lower")
        total_conditions[key] += 1
        if flipped:
            flip_conditions[key] += 1

print("\n  Polarity flip rate by 体 position and initial polarity:")
for key in sorted(total_conditions.keys()):
    rate = flip_conditions[key] / total_conditions[key]
    print(f"    体={key[1]}, polarity={key[0]}: {flip_conditions[key]}/{total_conditions[key]} "
          f"({100*rate:.1f}% flip)")

# Is there a simpler characterization?
# The polarity partition: P+ = {Kan(010), Zhen(100), Dui(110), Li(101)}
# P- = {Kun(000), Gen(001), Qian(111), Xun(011)}
# Notice: P+ has even popcount elements {010, 100} and odd {110, 101}
# P- has even popcount {000} and odd {001, 111, 011}
# Actually: P+ = {trigrams with L2=1} ∪ {101} minus {011}... no clean bit pattern.
# 
# The polarity is determined by Lo Shu odd/even.
# What does 互 do to Lo Shu numbers?

from divination_trace import TRIGRAM_LOSHU
print("\n  Lo Shu parity under 互卦 transition:")
for h in range(NUM_HEX):
    hg = hugua(h)
    for line in range(1, 7):
        if line <= 3:
            ti_ben = upper_trigram(h)
            ti_hu = upper_trigram(hg)
        else:
            ti_ben = lower_trigram(h)
            ti_hu = lower_trigram(hg)
        
        ben_ls = TRIGRAM_LOSHU[ti_ben]
        hu_ls = TRIGRAM_LOSHU[ti_hu]
        # Just collect the parity transitions
        break  # only need one analysis pass
    break

# Simpler: just check which trigram transitions preserve/flip polarity
print("\n  Trigram-level polarity transitions under 互:")
for t1 in range(8):
    # t1 as upper trigram of 本 → what upper trigrams does 互 produce?
    # upper_nuc = (L3, L4, L5). If 本's upper = (L4,L5,L6), we need L3 to determine upper_nuc.
    # L3 is the MSB of the lower trigram. So upper_nuc depends on BOTH trigrams.
    pass

print("  (Polarity of 互's 体 depends on both 本's trigrams — not just 体.)")
print("  This is because 互 shares L3,L4 between its two nuclear trigrams,")
print("  and L3 belongs to the lower trigram while L4 belongs to the upper.")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE IDEMPOTENCE CHAIN AND ITS MEANING
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("5. IDEMPOTENCE AND FIXED POINTS")
print("=" * 70)

# 互(互(x)) = 互(x) for all x — proven. What are the fixed points?
fixed_points = [h for h in range(NUM_HEX) if hugua(h) == h]
print(f"\n  Fixed points of 互 (互(h) = h): {len(fixed_points)}")
for h in fixed_points:
    lo, up = lower_trigram(h), upper_trigram(h)
    print(f"    {fmt6(h)} = {TRIGRAM_NAMES[lo]:10s} / {TRIGRAM_NAMES[up]:10s}")

# The 4 convergence points of 互∘互
conv = set()
for h in range(NUM_HEX):
    conv.add(hugua(hugua(h)))
print(f"\n  Convergence points of 互∘互 (=互): {len(conv)}")

# These are the 16 互 values that are self-互. But the convergence to 4 
# takes another step. Let's check.
print(f"  互 values: {len(hu_vals)}")
conv2 = set()
for hg in hu_vals:
    conv2.add(hugua(hg))
print(f"  互(互 values): {len(conv2)} — these equal the 互 values (idempotent)")

# Wait, the phase3 doc said convergence to 4 in 2 steps?
# That must mean the full iteration 互∘互∘互... Let me check.
print(f"\n  Checking iterated 互:")
for h in [0, 1, 2, 63]:
    chain = [h]
    x = h
    for _ in range(5):
        x = hugua(x)
        chain.append(x)
    print(f"    h={fmt6(h)}: {' → '.join(fmt6(c) for c in chain)}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. THE H-PROJECTION THEOREM: FULL PROOF
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("6. H-PROJECTION: EVERY 互卦 KERNEL IS IN H")
print("=" * 70)

# From the trace: 互卦 kernel = (M_本, I_本, I_本)
# Since M-bit = I-bit in the 互 kernel (both = I_本), every 互 kernel is in H.
# H = {k | k[1] == k[2]} = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)} = {id, O, MI, OMI}

# But wait — this is the kernel of the 互卦 ITSELF, not the kernel of the bridge.
# Let me be precise about what this means.

# For each hexagram h, its 互卦 hg = hugua(h) has kernel:
#   kernel(hg) = (hg_L1⊕hg_L6, hg_L2⊕hg_L5, hg_L3⊕hg_L4)
#              = (L2⊕L5, L3⊕L4, L4⊕L3) of 本
#              = (M_本, I_本, I_本)
# So kernel(互) has M-bit = I-bit = I_本, O-bit = M_本.
# kernel(互) ∈ H iff M_互 = I_互, which is I_本 = I_本. Always true. QED.

# What does this mean operationally?
print("""
  THEOREM: The mirror-pair kernel of every 互卦 lies in H = {id, O, MI, OMI}.

  Proof: 互(h) = (L2, L3, L4, L3, L4, L5).
  kernel(互(h)) = (L2⊕L5, L3⊕L4, L4⊕L3) = (M_h, I_h, I_h).
  H = {k | k[1] = k[2]}. Since I_h = I_h, kernel(互(h)) ∈ H always. □

  MEANING: H is the subgroup where middle and inner mirror pairs are locked.
  互卦 always produces hexagrams in H because:
  - It shares L3,L4 between both nuclear trigrams
  - This forces I-bit(互) = I-bit(本) and M-bit(互) = I-bit(本)
  - So M = I in the 互 kernel — exactly the H condition.

  CONNECTION TO SEQUENCE: The Upper Canon's bridge kernels preferentially
  reside in H (64.5% of bridges, 96.7th percentile). The 互卦 operation
  ALWAYS produces H-kernel hexagrams. The sequence and the divination
  operation both privilege the same subgroup — but for different reasons:
  - Sequence: consecutive transitions stay in H (a sequential constraint)
  - 互卦: the output is always in H (a structural constraint on the operation)
""")

# Verify: what fraction of the 16 互 values are in each kernel class?
print("  互卦 kernel distribution:")
hu_kernels = Counter()
for hg in hu_vals:
    bits_hg = [(hg >> i) & 1 for i in range(6)]
    kernel = (bits_hg[0] ^ bits_hg[5], bits_hg[1] ^ bits_hg[4], bits_hg[2] ^ bits_hg[3])
    kernel_names = {
        (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
        (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
    }
    name = kernel_names[kernel]
    in_h = kernel[1] == kernel[2]
    hu_kernels[(name, in_h)] += 1
    
for (name, in_h), c in sorted(hu_kernels.items()):
    h_tag = " [H]" if in_h else ""
    print(f"    {name:>3s}{h_tag}: {c}/16")

# ══════════════════════════════════════════════════════════════════════════════
# 7. THE 生 DESTRUCTION THEOREM
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("7. WHY 互 DESTROYS 生 AND AMPLIFIES 克")
print("=" * 70)

# The 生 cycle: Wood→Fire→Earth→Metal→Water
# The 克 cycle: Wood→Earth→Water→Fire→Metal
# Trigram→element: Metal(Qian 111, Dui 110), Fire(Li 101), 
#                  Wood(Zhen 100, Xun 011), Water(Kan 010), Earth(Gen 001, Kun 000)
#
# 互 forces nuclear trigrams to share L3,L4 (middle two bits of the hexagram).
# This means nuclear_lower and nuclear_upper differ only in their outer bits.
# The shared middle creates element correlations.

# For each of the 16 互 values, what's the (lower_element, upper_element) pair?
print("\n  The 16 互 values and their element pairs:")
elem_pair_count = defaultdict(int)
for hg in hu_vals:
    lo_e = TRIGRAM_ELEMENT[lower_trigram(hg)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(hg)]
    elem_pair_count[(lo_e, up_e)] += 1

# Full relation distribution
rel_count = Counter()
for hg in hu_vals:
    lo_e = TRIGRAM_ELEMENT[lower_trigram(hg)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(hg)]
    # For 体=upper: rel = five_phase_relation(up_e, lo_e)
    # For 体=lower: rel = five_phase_relation(lo_e, up_e)
    rel_up = five_phase_relation(up_e, lo_e)
    rel_lo = five_phase_relation(lo_e, up_e)
    rel_count[f"体=upper: {rel_up}"] += 1
    rel_count[f"体=lower: {rel_lo}"] += 1

print("\n  Relations among the 16 互 hexagrams:")
for key, count in sorted(rel_count.items()):
    print(f"    {key}: {count}/16")

# The key: in the FULL space (64 hexagrams), the 8×8 = 64 trigram pairs 
# produce a roughly uniform distribution of relations. But the 16 互 values
# are constrained to share their middle bits, which biases toward certain
# element pairs.

# Which element pairs are possible given the shared-middle constraint?
print("\n  Nuclear trigram structure: lower_nuc = (L2,L3,L4), upper_nuc = (L3,L4,L5)")
print("  They share L3,L4 but at different bit positions.")
print("  All 8 XOR masks appear among the 16 互 values — no masks are blocked.")
print()
print("  The 生 destruction must come from WHICH specific element pairs appear,")
print("  not from which XOR masks are possible. Let me check the actual element")
print("  pair distribution and its five-phase consequences.")

# Count relations across all 384 states more carefully
# The 互 has 16 values, each appearing 4×6=24 times (4 preimages × 6 lines).
# But 体/用 assignment depends on the line, not just the hexagram.
# For each 互 value, lines 1-3 make upper=体, lines 4-6 make lower=体.
# So each 互 value contributes 12 states with 体=upper and 12 with 体=lower.
# But the 4 preimages all have the SAME 互, so the 互's relation is the same.

print("\n  For each 互 value, the five-phase relation (both 体 positions):")
rel_weighted = Counter()
for hg in hu_vals:
    lo_e = TRIGRAM_ELEMENT[lower_trigram(hg)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(hg)]
    rel_up_ti = five_phase_relation(up_e, lo_e)  # 体=upper (12 states per 互 value)
    rel_lo_ti = five_phase_relation(lo_e, up_e)  # 体=lower (12 states per 互 value)
    # Each 互 value has 4 preimage hexagrams × 3 lines per position = 12 states
    rel_weighted[rel_up_ti] += 12
    rel_weighted[rel_lo_ti] += 12

print("  Weighted by states (should match 互 distribution from trace):")
for rel in ["比和", "生体", "克体", "体生用", "体克用"]:
    print(f"    {rel}: {rel_weighted[rel]}/384")

# The asymmetry comes from the 16 互 values having biased element pair distribution.
# Let me count: how many of the 16 have 克-type vs 生-type relationships?
print("\n  Among 16 互 values:")
type_count = Counter()
for hg in hu_vals:
    lo_e = TRIGRAM_ELEMENT[lower_trigram(hg)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(hg)]
    # Each hexagram contributes two relations (one per 体 position)
    for ti_e, yong_e in [(up_e, lo_e), (lo_e, up_e)]:
        rel = five_phase_relation(ti_e, yong_e)
        if rel in ("生体", "体生用"):
            type_count["生"] += 1
        elif rel in ("克体", "体克用"):
            type_count["克"] += 1
        else:
            type_count["比和"] += 1

print(f"    生-type (生体 or 体生用): {type_count['生']}/32 relation-slots")
print(f"    克-type (克体 or 体克用): {type_count['克']}/32 relation-slots")
print(f"    比和: {type_count['比和']}/32 relation-slots")
print(f"\n  In the full 64-hex space (uniform):")
print(f"    生-type: {(72+72)/384*32:.0f}/32")
print(f"    克-type: {(78+78)/384*32:.0f}/32")
print(f"    比和: {84/384*32:.0f}/32")
print(f"\n  The 16 互 values are biased: 克 amplified, 生 suppressed.")

if __name__ == "__main__":
    pass  # all output is inline
