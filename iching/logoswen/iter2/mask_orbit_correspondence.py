"""
Investigate the KW mask-orbit correspondence.

Each orbit has signature (o,m,i) ∈ Z₂³. 
KW assigns each orbit a uniform mask from Z₂³.
Is there a pattern in the assignment?

Orbit sig → mask:
  (0,0,0) → OMI = (1,1,1)
  (1,1,0) → OM  = (1,1,0)
  (1,0,1) → OI  = (1,0,1)
  (0,1,0) → M   = (0,1,0)
  (0,0,1) → I   = (0,0,1)
  (1,1,1) → OMI = (1,1,1)
  (1,0,0) → O   = (1,0,0)
  (0,1,1) → MI  = (0,1,1)

Hmm... writing both as 3-bit vectors:
  sig (0,0,0) → mask (1,1,1) = sig ⊕ (1,1,1)
  sig (1,1,0) → mask (1,1,0) = sig (same!)
  sig (1,0,1) → mask (1,0,1) = sig (same!)
  sig (0,1,0) → mask (0,1,0) = sig (same!)
  sig (0,0,1) → mask (0,0,1) = sig (same!)
  sig (1,1,1) → mask (1,1,1) = sig (same!)
  sig (1,0,0) → mask (1,0,0) = sig (same!)
  sig (0,1,1) → mask (0,1,1) = sig (same!)

Wait — for sig (0,0,0), mask is OMI = (1,1,1) = sig ⊕ (1,1,1).
For all others, mask = sig.

Let me check: is the mask the COMPLEMENT when sig=(0,0,0)?
Actually, mask id = (0,0,0) is excluded (it pairs a hexagram with itself).
So sig (0,0,0) can't use id; OMI = (1,1,1) is the "opposite".

Actually, the mapping is: mask = sig unless sig = (0,0,0), in which case OMI = (1,1,1).

But this means mask ≠ id always. And for sig ≠ (0,0,0): mask = sig exactly.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
from sequence import all_bits

M = all_bits()

# The mapping
sig_to_mask = {
    (0,0,0): (1,1,1),  # Qian → OMI
    (1,1,0): (1,1,0),  # Zhun → OM
    (1,0,1): (1,0,1),  # Xu → OI
    (0,1,0): (0,1,0),  # Shi → M
    (0,0,1): (0,0,1),  # XChu → I
    (1,1,1): (1,1,1),  # Tai → OMI
    (1,0,0): (1,0,0),  # Bo → O
    (0,1,1): (0,1,1),  # WWang → MI
}

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

MASK_NAMES_3 = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}

print("KW mask-orbit correspondence:")
print(f"{'Orbit':>6s}  {'Sig':>5s}  {'Mask':>5s}  {'Mask name':>10s}  {'Relation':>15s}")
for sig in sorted(sig_to_mask.keys()):
    mask = sig_to_mask[sig]
    mask_name = MASK_NAMES_3[mask]
    
    # Check various relationships
    xor = tuple(sig[i] ^ mask[i] for i in range(3))
    
    if mask == sig:
        relation = "mask = sig"
    elif xor == (1,1,1):
        relation = "mask = sig ⊕ (1,1,1)"
    else:
        relation = f"mask ⊕ sig = {xor}"
    
    print(f"{ORBIT_NAMES[sig]:>6s}  {sig}  {mask}  {mask_name:>10s}  {relation}")

print()
print("Pattern: mask = sig for all orbits EXCEPT Qian(000),")
print("where mask = OMI(111) = sig ⊕ (1,1,1).")
print()
print("Equivalently: mask = max(sig, sig⊕(1,1,1)) = sig OR complement, choosing non-zero.")
print("Since (0,0,0) would map to the identity mask (which is excluded),")
print("Qian maps to OMI instead.")
print()

# Check: for sig ≠ (0,0,0), mask = sig means the pair mask is the SAME as the orbit signature.
# The orbit signature is (l1⊕l6, l2⊕l5, l3⊕l4).
# The pair mask says which bits to flip to get from h to its partner.
# When mask = sig, the pair mask flips exactly the bits that are "asymmetric" in the orbit.
# This means: for each line pair (i, j), the pair swaps their values iff they differ.
# In other words: the partner of h is the hexagram in the orbit that's maximally "symmetric"
# (or maximally "asymmetric" — depending on perspective).

# Actually let's verify: what does mask = sig mean operationally?
# Orbit Zhun has sig (1,1,0): l1≠l6, l2≠l5, l3=l4
# Mask OM = flips (l1,l6) and (l2,l5) but NOT (l3,l4)
# So the pair operation: for each line pair that's asymmetric, swap them.
# For the pair (l3,l4) which is already symmetric (l3=l4), leave them alone.
# This IS the orbit signature acting as a selection rule!

print("Operational meaning:")
print("  mask = sig means: 'pair each hexagram by swapping exactly the asymmetric line pairs.'")
print("  The orbit signature (o,m,i) tells you WHICH line pairs differ.")
print("  Using that signature AS the pair mask means: 'correct the asymmetries.'")
print()
print("  Exception Qian(000): ALL line pairs are symmetric (l1=l6, l2=l5, l3=l4).")
print("  Can't 'correct zero asymmetries' (that's the identity). So use OMI: flip everything.")
print("  Equivalently: pair each self-symmetric hexagram with its complement.")
print()

# Does this pattern have a name? It's essentially: 
# "The pair mask is the group element that maps each hexagram to its 
#  orbit-complement (the hexagram in the same orbit that's maximally distant)."

# Let's verify: in orbit Zhun (sig=(1,1,0)), mask OM flips l1,l2,l5,l6.
# Starting from hex h = (l1,l2,l3,l4,l5,l6), partner = (1-l1, 1-l2, l3, l4, 1-l5, 1-l6)
# Hamming distance = 4 (flips 4 of 6 bits)
# In the Q₃ orbit, this is a face diagonal (distance 4 in the doubled metric)
# = distance 2 in the Q₃ metric (flip 2 of 3 generators).

# For Qian (sig=(0,0,0)), mask OMI flips all 6 bits.
# Hamming distance = 6 (flips all bits) = space diagonal of Q₃

# So KW's pairing connects each hexagram to its:
# - Antipode in the orbit's Q₃ (for Qian/Tai: distance 3 in Q₃ = body diagonal)
# - Face diagonal (for orbits with sig weight 2: OM, OI, MI)
# - Edge (for orbits with sig weight 1: O, M, I)

# Wait, let me re-check. If mask = sig:
# sig weight 1 (O, M, I): mask flips 2 bits → Hamming distance 2 → Q₃ edge
# sig weight 2 (OM, OI, MI): mask flips 4 bits → Hamming distance 4 → Q₃ face diag
# sig weight 3 (OMI): mask flips 6 bits → Hamming distance 6 → Q₃ body diag

# The relationship to the Hamming weight:
# H = 2 × |generators in mask| (from H = w + 2S quantization result)
# Actually H = 2 * S where S = number of generators in the mask
# This is the Hamming distance of the pair.

print("Hamming distance pattern:")
for sig in sorted(sig_to_mask.keys()):
    mask = sig_to_mask[sig]
    weight = sum(mask)
    hamming = weight * 2
    print(f"  {ORBIT_NAMES[sig]:>6s}: mask weight {weight}, Hamming distance {hamming}")

# Interesting: the pair Hamming distance = 2 × (orbit signature weight)
# except for Qian where it's 6 (= 2 × 3)

print()
print("The pair Hamming distance = 2 × max(weight(sig), 3 if sig=(0,0,0))")
print("Or equivalently: Hamming = 2 × weight(mask), and mask = sig for non-zero sig.")

# This connects to the H = w + 2S quantization: S = weight of sig = weight of mask
# For Qian: S = 3 (OMI). For others: S = weight(sig).
# So S is determined by the orbit, and the specific mask is determined by WHICH generators.
# KW makes the unique choice where the mask IS the signature.

print()
print("═" * 70)
print("CONCLUSION: KW's uniform pairing rule IS the orbit signature itself.")
print("  mask(orbit) = orbit_signature (for sig ≠ 0)")
print("  mask(orbit) = OMI (for sig = 0, the identity orbit)")
print()
print("This is the unique assignment where the pair mask encodes the orbit's")
print("symmetry-breaking pattern: flip exactly the line pairs that are asymmetric.")
print("For the fully symmetric orbit (Qian), flip everything (maximal dressing).")
print("═" * 70)
