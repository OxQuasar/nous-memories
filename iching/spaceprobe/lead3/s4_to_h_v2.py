"""
V2: What property of the S₄ block structure picks out H?

From v1: "same block permutation on both trigrams" gives {id, M, OI, OMI} (O=I), not H (M=I).
The reversal in the hexagram structure means lower gets (O,M,I) while upper gets (I,M,O).

Let me try other criteria:
1. What if we ask which subgroup is the kernel of the 互 projection?
2. What if we ask which subgroup preserves the 互 value?
3. What if we relate H to the block structure via the nuclear trigrams?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from cycle_algebra import hugua, lower_trigram, upper_trigram, bit, fmt6, NUM_HEX, MASK_ALL
from collections import Counter

names = {(0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
         (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'}

Z2_3 = [(a,b,c) for a in range(2) for b in range(2) for c in range(2)]

def kernel_to_mask(k):
    """Convert kernel (O,M,I) to palindromic 6-bit mask."""
    return k[0] | (k[1]<<1) | (k[2]<<2) | (k[2]<<3) | (k[1]<<4) | (k[0]<<5)

# ══════════════════════════════════════════════════════════════════════════════
# 1. Which Z₂³ elements preserve 互?
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("1. WHICH KERNEL OPERATIONS PRESERVE 互卦?")
print("=" * 70)

# For each kernel k, check: 互(h ⊕ mask(k)) vs 互(h)
# We already know from deeper_analysis:
#   互(h ⊕ MI) = complement(互(h))  [distance 6]
#   互(h ⊕ OMI) = complement(互(h)) [distance 6]
# Let me check all 8.

for k in Z2_3:
    mask = kernel_to_mask(k)
    k_name = names[k]
    
    # For each hexagram, what's the relationship between 互(h) and 互(h⊕mask)?
    rels = Counter()
    dists = []
    for h in range(NUM_HEX):
        h2 = h ^ mask
        hu1 = hugua(h)
        hu2 = hugua(h2)
        d = bin(hu1 ^ hu2).count('1')
        dists.append(d)
        if hu1 == hu2:
            rels['identity'] += 1
        elif hu2 == hu1 ^ MASK_ALL:
            rels['complement'] += 1
        else:
            rels['other'] += 1
    
    dist_vals = set(dists)
    preserve = all(d == 0 for d in dists)
    print(f"  {k_name:>3s}: d(互(h), 互(h⊕k)) = {sorted(dist_vals)}, "
          f"preserve={preserve}, {dict(rels)}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. The kernel of 互 (which operations are invisible to 互)
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("2. KERNEL OF 互 (operations invisible to nuclear hexagram)")
print("=" * 70)

# 互(h) = (L2, L3, L4, L3, L4, L5) — depends on L2,L3,L4,L5 only.
# A palindromic mask (a,b,c,c,b,a) changes:
#   L1→L1⊕a, L2→L2⊕b, L3→L3⊕c, L4→L4⊕c, L5→L5⊕b, L6→L6⊕a
# 互 after mask: (L2⊕b, L3⊕c, L4⊕c, L3⊕c, L4⊕c, L5⊕b)
# This equals 互(h) iff b=0 and c=0.
# So kernel of 互 = {masks with M=0, I=0} = {id, O}.

print("  互(h) depends on L2,L3,L4,L5.")
print("  Palindromic mask (a,b,c,c,b,a) is invisible to 互 iff b=0 and c=0.")
print("  Kernel of 互 = {id, O} — only the outer pair operation.")
print()
print("  This is a subgroup of H (and of every subgroup containing O).")
print("  H = {id, O} × {id, MI}  — the kernel {id,O} extended by MI.")

# ══════════════════════════════════════════════════════════════════════════════
# 3. What does MI do to 互?
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("3. THE ACTION OF EACH Z₂³ ELEMENT ON 互-SPACE")
print("=" * 70)

# The 16 互 values form a subspace. Each Z₂³ element acts on this subspace.
hu_vals = sorted(set(hugua(h) for h in range(NUM_HEX)))

for k in Z2_3:
    mask = kernel_to_mask(k)
    k_name = names[k]
    
    # Action on the 16 互 values
    action = {}
    for hg in hu_vals:
        # Apply mask to 互, then take 互 again (since 互 is idempotent, 
        # the question is what 互(互⊕mask) gives — but that's not what we want.
        # We want: which 互 value does 互(h⊕mask) map to, given 互(h) = hg?
        # But different h with same 互 may give different results.
        pass
    
    # Instead: just check if the action h→h⊕mask is compatible with 互 fibers.
    # i.e., if 互(h1) = 互(h2), does 互(h1⊕mask) = 互(h2⊕mask)?
    fiber_compatible = True
    for h1 in range(NUM_HEX):
        for h2 in range(h1+1, NUM_HEX):
            if hugua(h1) == hugua(h2):
                if hugua(h1 ^ mask) != hugua(h2 ^ mask):
                    fiber_compatible = False
                    break
        if not fiber_compatible:
            break
    
    # If fiber-compatible, the action descends to a well-defined action on 互-space
    if fiber_compatible:
        induced = {}
        for hg in hu_vals:
            # pick any h in fiber
            h = next(h for h in range(NUM_HEX) if hugua(h) == hg)
            induced[hg] = hugua(h ^ mask)
        
        is_id = all(induced[hg] == hg for hg in hu_vals)
        is_complement = all(induced[hg] == hg ^ MASK_ALL for hg in hu_vals)
        
        desc = "identity" if is_id else "complement" if is_complement else "permutation"
        print(f"  {k_name:>3s}: fiber-compatible, induced action = {desc}")
    else:
        print(f"  {k_name:>3s}: NOT fiber-compatible (breaks 互 fibers)")

# ══════════════════════════════════════════════════════════════════════════════
# 4. H as the subgroup generated by ker(互) and complement-on-互-space
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("4. H = ker(互) × ⟨complement on 互-space⟩")
print("=" * 70)

print("""
  ker(互) = {id, O} — operations invisible to 互
  MI induces complement on 互-space: 互(h⊕MI) = complement(互(h))
  OMI = O·MI: O is in ker, MI gives complement → OMI also gives complement

  H = {id, O, MI, OMI} = ker(互) × {id, MI}

  In other words: H consists of exactly the operations that either
  (a) don't change 互 at all (id, O), or
  (b) complement 互 entirely (MI, OMI).

  The non-H elements {I, M, OI, OM} scramble the 互 fibers —
  they break the nuclear hexagram structure in ways that are 
  neither trivial nor systematic.
""")

# Verify: non-H elements are NOT fiber-compatible
print("  Verification: non-H elements break fibers:")
non_H = [(0,0,1), (0,1,0), (1,0,1), (1,1,0)]
for k in non_H:
    mask = kernel_to_mask(k)
    k_name = names[k]
    broken = 0
    for h1 in range(NUM_HEX):
        for h2 in range(h1+1, NUM_HEX):
            if hugua(h1) == hugua(h2):
                if hugua(h1 ^ mask) != hugua(h2 ^ mask):
                    broken += 1
    print(f"    {k_name}: {broken} fiber violations")

# ══════════════════════════════════════════════════════════════════════════════
# 5. THE THREAD: S₄ → blocks → 互 → H
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("5. THE THREAD: S₄ → BLOCKS → 互 → H")
print("=" * 70)

print("""
  S₄ acts on 4 blocks of 2 trigrams.
  
  Hexagrams = (lower_trigram, upper_trigram) = pairs from that space.
  
  Mirror-pair operations (Z₂³) act on hexagrams via palindromic masks.
  Each mask (O,M,I) XORs lower with (O,M,I) and upper with (I,M,O).
  
  互卦 erases the outer pair and fuses middle+inner:
    互(h) = f(L2,L3,L4,L5) — depends only on the inner 4 bits.
  
  This creates a projection 64 → 16 with 4-element fibers.
  The fibers are the equivalence classes {hexagrams differing only in L1,L6}.
  
  H = {operations compatible with this projection}
    = {k ∈ Z₂³ | k preserves or systematically transforms the fibers}
    = ker(互) ∪ {elements that complement all fibers}
    = {id, O} ∪ {MI, OMI}
    = {id, O, MI, OMI}

  The thread:
  
  1. S₄ structures the trigram space into 4 blocks
  2. Doubling (trigram → hexagram) creates Z₂³ via mirror pairs
  3. 互卦 projects hexagrams by erasing the outer pair (L1,L6)
  4. H = the subgroup of Z₂³ that respects this projection
  5. The Upper Canon sequence walks through Z₂³ preferring H
  6. This means: the sequence preferentially uses transformations
     that are COMPATIBLE with the nuclear hexagram operation.

  The sequence is arranged so that consecutive transitions 
  don't break the divination structure.
""")
