# Q3 Round 1: Hexagram Involution Structure — Results

## Bit Convention

L1 = MSB = bit 5 (bottom line), L6 = LSB = bit 0 (top line).
Integer = L1·32 + L2·16 + L3·8 + L4·4 + L5·2 + L6·1.
Reversal swaps L1↔L6, L2↔L5, L3↔L4 (reverses the 6-bit string).

## Section 1: Fixed Points and Cycle Structure

| Operation | Order | Fixed Points | 2-Cycles | Verification |
|-----------|-------|-------------|----------|--------------|
| σ₁ (complement) | 2 | 0 | 32 | 0 + 2×32 = 64 ✓ |
| σ₂ (reversal) | 2 | 8 | 28 | 8 + 2×28 = 64 ✓ |
| σ₃ (comp∘rev) | 2 | 8 | 28 | 8 + 2×28 = 64 ✓ |

**σ₁ fixed points:** None (no self-complementary 6-bit string exists — 6 is even)

**σ₂ fixed points (palindromes):** 8 hexagrams where reverse = self
```
000000, 001100, 010010, 011110, 100001, 101101, 110011, 111111
```
These are exactly the palindromic bit strings: L1=L6, L2=L5, L3=L4.
Degrees of freedom = 3 (choose L1, L2, L3 freely) → 2³ = 8. ✓

**σ₃ fixed points (anti-palindromes):** 8 hexagrams where complement = reversal
```
000111, 001011, 010101, 011001, 100110, 101010, 110100, 111000
```
These satisfy: reverse(h) = complement(h), i.e., L_i + L_{7-i} = 1 for all i.
Degrees of freedom = 3 → 2³ = 8. ✓

**Comparison with n=3:** At n=3, σ₂ (reversal) has 4 fixed points (palindromic trigrams: 000, 010, 101, 111) and σ₃ has 0 fixed points. At n=6, σ₂ has 8 and σ₃ has 8. The n=3 asymmetry (σ₂ has fixed points but σ₃ doesn't) arises because 3 is odd: a 3-bit string can be a palindrome but cannot satisfy L_i + L_{4-i} = 1 for all i (the middle bit would need to equal its own complement). At n=6 (even), both palindromes and anti-palindromes exist.

## Section 2: Pair-Set Overlaps

| Intersection | Count | Shared Pairs |
|-------------|-------|--------------|
| pairs(σ₁) ∩ pairs(σ₂) | 4 | The 4 anti-palindromic complement pairs |
| pairs(σ₁) ∩ pairs(σ₃) | 4 | The 4 palindromic complement pairs |
| pairs(σ₂) ∩ pairs(σ₃) | **0** | No shared pairs |

**Shared pairs σ₁∩σ₂** (complement = reversal for these):
```
{000111, 111000}, {001011, 110100}, {010101, 101010}, {011001, 100110}
```
These are exactly the σ₃ fixed points grouped as complement pairs.

**Shared pairs σ₁∩σ₃** (complement = comp∘rev, i.e., reversal is identity):
```
{000000, 111111}, {001100, 110011}, {010010, 101101}, {011110, 100001}
```
These are exactly the σ₂ fixed points grouped as complement pairs.

**σ₂ and σ₃ share NO pairs.** A pair {h, rev(h)} can only equal {h, comp(rev(h))} if rev(h) = comp(rev(h)), i.e., rev(h) is self-complementary — impossible in 6 bits. This disjointness is structural.

## Section 3: Products and Composition

```
σ₁∘σ₂ = σ₃  ✓ (by definition)
σ₂∘σ₁ = σ₃  ✓ (they commute!)
```

**All three involutions commute pairwise.** This is because complement and reversal operate on independent aspects of the bit string: complement flips values, reversal permutes positions. These operations commute in general for any bit length.

| Product | = | Order | Cycle Structure |
|---------|---|-------|----------------|
| σ₁∘σ₂ | σ₃ | 2 | 8 fixed + 28 two-cycles |
| σ₁∘σ₃ | σ₂ | 2 | 8 fixed + 28 two-cycles |
| σ₂∘σ₃ | σ₁ | 2 | 32 two-cycles |

The product table closes: {e, σ₁, σ₂, σ₃} under composition gives back itself.

## Section 4: Generated Group

### G = ⟨σ₁, σ₂⟩ ≅ V₄ (Klein four-group)

| Property | Value |
|----------|-------|
| Order | 4 |
| Abelian | Yes |
| Solvable | Yes |
| Nilpotent | Yes |
| Center | G (entire group) |
| Derived subgroup | {e} |
| Abelianization | G/[G,G] ≅ V₄ |

**All 4 elements:**

| Element | Order | Cycle Type | Description |
|---------|-------|-----------|-------------|
| e | 1 | 64 fixed | Identity |
| σ₁ | 2 | 32 two-cycles | Complement |
| σ₂ | 2 | 8 fixed + 28 two-cycles | Reversal |
| σ₃ | 2 | 8 fixed + 28 two-cycles | Comp∘Rev |

**Subgroup lattice:**
```
        V₄
       / | \
    ⟨σ₁⟩ ⟨σ₂⟩ ⟨σ₃⟩    (each ≅ Z₂)
       \ | /
        {e}
```

### Comparison with n=3

At n=3: G = ⟨σ₁, σ₂⟩ on 8 trigrams is also V₄. σ₁ is FPF, σ₂ has 4 fixed points (palindromes), σ₃ has 0 (odd length prevents anti-palindromes). This gives 3 orbits: {000,111} (size 2), {010,101} (size 2), {001,011,100,110} (size 4).

At n=6: σ₁ is FPF, σ₂ has 8 fixed points, σ₃ has 8 fixed points (even length enables anti-palindromes). 20 orbits: 12 of size 4, 8 of size 2.

The group structure is identical (V₄), but the **action** differs due to even vs odd bit-length affecting which involutions have fixed points.

## Section 5: Orbit Structure

**20 orbits total:** 12 orbits of size 4, 8 orbits of size 2.
```
12 × 4 + 8 × 2 = 48 + 16 = 64 ✓
```

### Size-2 orbits (complement pairs where one element is palindromic or anti-palindromic)

| Orbit | Elements | Fixed by | Type |
|-------|----------|----------|------|
| {0, 63} | 000000, 111111 | σ₂ | Both palindromes |
| {12, 51} | 001100, 110011 | σ₂ | Both palindromes |
| {18, 45} | 010010, 101101 | σ₂ | Both palindromes |
| {30, 33} | 011110, 100001 | σ₂ | Both palindromes |
| {7, 56} | 000111, 111000 | σ₃ | Both anti-palindromes |
| {11, 52} | 001011, 110100 | σ₃ | Both anti-palindromes |
| {21, 42} | 010101, 101010 | σ₃ | Both anti-palindromes |
| {25, 38} | 011001, 100110 | σ₃ | Both anti-palindromes |

**Structure:** The 16 special hexagrams (8 palindromes + 8 anti-palindromes) form 8 complement pairs. Within each pair, σ₁ swaps them, while the other two operations either both fix or both swap — so V₄ acts as Z₂ (just σ₁) on these pairs.

### Size-4 orbits (generic hexagrams, free V₄ action)

Each orbit {h, σ₁(h), σ₂(h), σ₃(h)} has all four elements distinct.

| Orbit | h | σ₁(h) | σ₂(h) | σ₃(h) | Yang counts |
|-------|---|--------|--------|--------|-------------|
| 1 | 000001 | 111110 | 100000 | 011111 | {1,5,1,5} |
| 2 | 000010 | 111101 | 010000 | 101111 | {1,5,1,5} |
| 3 | 000011 | 111100 | 110000 | 001111 | {2,4,2,4} |
| 4 | 000100 | 111011 | 001000 | 110111 | {1,5,1,5} |
| 5 | 000101 | 111010 | 101000 | 010111 | {2,4,2,4} |
| 6 | 000110 | 111001 | 011000 | 100111 | {2,4,2,4} |
| 7 | 001001 | 110110 | 100100 | 011011 | {2,4,2,4} |
| 8 | 001010 | 110101 | 010100 | 101011 | {2,4,2,4} |
| 9 | 001101 | 110010 | 101100 | 010011 | {3,3,3,3} |
| 10 | 001110 | 110001 | 011100 | 100011 | {3,3,3,3} |
| 11 | 010001 | 101110 | 100010 | 011101 | {2,4,2,4} |
| 12 | 010110 | 101001 | 011010 | 100101 | {3,3,3,3} |

**Weight structure within orbits:**
- σ₁ always flips weight: w(σ₁(h)) = 6 - w(h)
- σ₂ preserves weight: w(σ₂(h)) = w(h)
- σ₃ flips weight: w(σ₃(h)) = 6 - w(h)

So each size-4 orbit contains two weight classes: {w, 6-w} with 2 elements each.
- 3 orbits with weights {1, 5}
- 6 orbits with weights {2, 4}
- 3 orbits with weights {3, 3}

## Section 6: Structural Summary

### The 64 hexagrams decompose under V₄ into:

1. **8 degenerate orbits** (size 2): complement pairs where reversal = identity or reversal = complement
   - 4 palindromic pairs: {h, comp(h)} where both h and comp(h) are palindromes
   - 4 anti-palindromic pairs: {h, comp(h)} where both h and comp(h) are anti-palindromes

2. **12 generic orbits** (size 4): each a complete V₄ coset {h, comp(h), rev(h), comp(rev(h))}

### Partition counts by weight:

| Weight w | Hexagrams | Palindromes | Anti-palindromes | Generic | Size-2 orbits | Size-4 orbits |
|----------|-----------|-------------|------------------|---------|--------------|--------------|
| 0 | 1 | 1 | 0 | 0 | — | — |
| 1 | 6 | 0 | 0 | 6 | — | 3 (shared w/ w=5) |
| 2 | 15 | 3 | 0 | 12 | — | 6 (shared w/ w=4) |
| 3 | 20 | 0 | 8 | 12 | — | 3 (shared w/ w=3) |
| 4 | 15 | 3 | 0 | 12 | — | — |
| 5 | 6 | 0 | 0 | 6 | — | — |
| 6 | 1 | 1 | 0 | 0 | — | — |

The weight-0/6 pair {000000, 111111} and weight-pairing structure mean complement always crosses the w ↔ 6-w boundary, while reversal stays within the same weight class.

### Key finding: Even bit-length doubles the degeneracy

At n=3 (odd): σ₃ is FPF, so only σ₂ contributes fixed points. 4 palindromes → 2 degenerate orbits (size 2) + 1 free orbit (size 4). Total: 3 orbits.

At n=6 (even): Both σ₂ and σ₃ have 8 fixed points each (palindromes and anti-palindromes both exist). 16 special hexagrams → 8 degenerate orbits + 12 free orbits. Total: 20 orbits.

**General pattern for n-bit strings:**
- σ₂ fixed points (palindromes): 2^⌈n/2⌉
- σ₃ fixed points (anti-palindromes): 2^⌈n/2⌉ if n even, 0 if n odd
- G is always V₄ (complement and reversal always commute)
- Free orbits = (2ⁿ - |Fix(σ₂)| - |Fix(σ₃)|) / 4 (when n even)

The 20-orbit decomposition is the natural equivalence class structure for hexagram analysis: each orbit groups hexagrams that are interchangeable under the three symmetries.
