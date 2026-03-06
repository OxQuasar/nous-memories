# Q3 Round 2: Extended Involution Analysis — Results

## Bit Convention (same as Round 1)

L1 = MSB = bit 5 (bottom line), L6 = LSB = bit 0 (top line).
Mirror pairs: {L1,L6} = outer, {L2,L5} = middle, {L3,L4} = inner.

## Part 1: Mirror-pair Translation Group T = ⟨O, M, I⟩

XOR masks on mirror pairs:
```
O  = 100001 = 33  (flip L1,L6)
M  = 010010 = 18  (flip L2,L5)
I  = 001100 = 12  (flip L3,L4)
OM = 110011 = 51   OI = 101101 = 45   MI = 011110 = 30   OMI = 111111 = 63
```

**O ⊕ M ⊕ I = 63 = complement (σ₁).** Complement is the product of all three mirror-pair flips.

| Property | Value |
|----------|-------|
| \|T\| | 8 |
| T ≅ | Z₂³ |
| All elements order ≤ 2 | Yes |
| Orbits on {0,...,63} | 8 orbits of size 8 |
| Action | Free (regular on each coset) |

**The 8 T-orbits** are the cosets of T in Z₂⁶. Each is determined by its **residual** — the 3-bit signature (L1⊕L6, L2⊕L5, L3⊕L4):

| Orbit | Residual | Interpretation | Size |
|-------|----------|----------------|------|
| 0 | 000 | All mirror pairs "same" (palindromes) | 8 |
| 1 | 100 | Outer pair differs | 8 |
| 2 | 010 | Middle pair differs | 8 |
| 3 | 110 | Outer + middle differ | 8 |
| 4 | 001 | Inner pair differs | 8 |
| 5 | 101 | Outer + inner differ | 8 |
| 6 | 011 | Middle + inner differ | 8 |
| 7 | 111 | All pairs differ (anti-palindromes) | 8 |

**Key fact:** The quotient Z₂⁶/T ≅ Z₂³. The residual map hexagram → 3-bit signature is the quotient projection. The 8 cosets ARE a copy of Z₂³.

T-orbits do NOT correspond to upper or lower trigrams — each orbit contains all 8 upper trigrams and all 8 lower trigrams. This is because O flips both L1 and L6, crossing the upper/lower boundary.

## Part 2: Adding reversal — G_ext = ⟨T, σ₂⟩ ≅ Z₂⁴

**σ₂ commutes with all of O, M, I** — verified computationally. This is because reversal swaps positions within each mirror pair (L1↔L6, L2↔L5, L3↔L4), while each XOR mask flips values at both positions of its pair. Swapping positions then flipping values = flipping values then swapping positions.

| Property | Value |
|----------|-------|
| \|G_ext\| | 16 |
| G_ext = T × ⟨σ₂⟩ ≅ Z₂⁴ | Yes (direct product) |
| σ₂ preserves all T-orbits | **Yes** — trivial quotient action |

**σ₂ acts within each T-orbit, never between them.** The quotient action on the 8 orbits is trivial. This is the critical departure from n=3: at n=3, the non-XOR involutions acted nontrivially on blocks.

## Part 3: Trigram swap σ₄

σ₄ swaps upper trigram (L1,L2,L3) ↔ lower trigram (L4,L5,L6).

| Property | Value |
|----------|-------|
| Order | 2 |
| Fixed points | 8 (hexagrams with upper = lower: Kun/Kun, Gen/Gen, etc.) |
| σ₄ commutes with σ₂ | Yes |

**σ₄ normalizes T but does not commute with it:**
```
σ₄ ∘ O ∘ σ₄ = I    (swaps outer ↔ inner masks)
σ₄ ∘ M ∘ σ₄ = M    (middle mask fixed)
σ₄ ∘ I ∘ σ₄ = O
```

σ₄ permutes T-generators as the transposition (O I), fixing M. But σ₄ is NOT the same as the pair permutation that swaps pair O with pair I — it's a cross-pair operation (swaps L1↔L4, L2↔L5, L3↔L6) rather than a whole-pair reallocation.

**σ₄ action on T-orbits:**
```
Orbit 0 (000) → Orbit 0 (000)    fixed
Orbit 1 (100) → Orbit 4 (001)    swapped
Orbit 2 (010) → Orbit 2 (010)    fixed
Orbit 3 (110) → Orbit 6 (011)    swapped
Orbit 4 (001) → Orbit 1 (100)    swapped
Orbit 5 (101) → Orbit 5 (101)    fixed
Orbit 6 (011) → Orbit 3 (110)    swapped
Orbit 7 (111) → Orbit 7 (111)    fixed
```
On residuals: σ₄ swaps bit 0 ↔ bit 2 of the residual (the outer/inner pair difference indicator). This is the transposition (O↔I) acting on the residual Z₂³.

## Part 4: G_full = ⟨O, M, I, σ₂, σ₄⟩

| Property | Value |
|----------|-------|
| \|G_full\| | 32 |
| Abelian | No |
| Solvable | Yes |
| Nilpotent | Yes |
| \|Center\| | 8 |
| \|[G,G]\| | 2 |
| Element orders | {1:1, 2:23, 4:8} |

Orbits: **6** orbits (sizes 8, 8, 8, 8, 16, 16).

The two size-16 orbits are pairs of T-orbits merged by σ₄: {orbits 1,4} and {orbits 3,6}.

Quotient action on 8 T-orbits: Z₂ (just σ₄'s transposition).

## Part 5: The 384-element group G_384

The opposition theory's group is (Z₂ ≀ S₃) × Z₂³ = 48 × 8 = 384.

**Three layers of generators:**

1. **Z₂³ = {O, M, I}** — pair-value flips (XOR masks)
2. **Z₂³ = {swap_L1L6, swap_L2L5, swap_L3L4}** — within-pair position swaps
3. **S₃ = ⟨swap_OM, cycle_OMI⟩** — permutations of the 3 mirror pairs as units

Layer 1 and Layer 2 commute with each other (and each layer is internally commutative), giving Z₂⁶ (order 64). Layer 3 acts by conjugation on both other layers, permuting the pair labels.

**Conjugation by pair permutations:**
```
swap_OM:   O ↦ M, M ↦ O, I ↦ I
cycle_OMI: O ↦ M ↦ I ↦ O
```

**Subgroup structure:**
```
T ⋊ S₃ = Z₂ ≀ S₃    order 48    (wreath product)
⟨swaps⟩ ⋊ S₃         order 48    (position operations only)
G_384 = (Z₂ ≀ S₃) × Z₂³   order 384
```

| Property | Value |
|----------|-------|
| \|G_384\| | **384** ✓ |
| Abelian | No |
| Solvable | Yes |
| \|Center\| | 4 |
| \|[G,G]\| | 48 |
| \|G/[G,G]\| | 8 |
| σ₂ ∈ G_384 | Yes |
| σ₄ ∈ G_384 | Yes |

**S₃ action on T-orbits (quotient action on Z₂³):**
```
swap_OM on orbits:  swaps residual bits 1↔2  (outer↔middle)
cycle_OMI on orbits: cycles residual bits 0→1→2→0
swap_L1L6 on orbits: trivial (within-pair swaps fix residuals)
```

**Quotient group on 8 T-orbits: S₃** (order 6, non-abelian).

## Part 6: The 4 Macro-orbits

Under G_384, the 64 hexagrams fall into exactly **4 orbits** (sizes 8, 8, 24, 24):

| Orbit | Size | Residuals | Yang counts | Palindromes | Anti-palindromes |
|-------|------|-----------|-------------|-------------|-----------------|
| A | 8 | {000} | {0,2,4,6} | 8 | 0 |
| B | 8 | {111} | {3} | 0 | 8 |
| C | 24 | {100,010,001} | {1,3,5} | 0 | 0 |
| D | 24 | {110,101,011} | {2,4} | 0 | 0 |

**T-orbit → macro-orbit mapping:**
```
res 000 (wt 0) → A    (fixed by S₃)
res 111 (wt 3) → B    (fixed by S₃)
res 100,010,001 (wt 1) → C    (S₃ orbit of size 3)
res 110,101,011 (wt 2) → D    (S₃ orbit of size 3)
```

The S₃ action on residuals has 4 orbits: the two fixed points {000, 111} and the two weight classes {wt=1, wt=2}. These become the 4 macro-orbits.

**This matches the opposition theory exactly:** 2 orbits of size 8 (palindromes, anti-palindromes — pairing forced to complement) and 2 orbits of size 24 (non-palindromic hexagrams — each with 3 pairing choices: reversal, complement, comp∘rev).

## Part 7: The Hexagram-Trigram Bridge

### The quotient projection

The mirror-pair residual map φ: {0,...,63} → Z₂³ defined by
```
φ(h) = (L1⊕L6, L2⊕L5, L3⊕L4)
```
projects hexagrams onto a copy of Z₂³. The fibers φ⁻¹(r) are exactly the T-orbits.

This quotient IS the trigram-signature space:
- **res = 000**: all mirror pairs "same" → palindromic hexagrams
- **res = 111**: all mirror pairs "different" → anti-palindromic hexagrams
- Each residual bit records whether a mirror pair is "aligned" or "crossed"

The residual is NOT the upper or lower trigram — T-orbits contain all 8 upper and all 8 lower trigrams. It's a genuinely new coordinate: the **mirror-pair difference signature**.

### Structural parallel with n=3

| Aspect | n=3 | n=6 |
|--------|-----|-----|
| Base space | Z₂³ (8 trigrams) | Z₂⁶ (64 hexagrams) |
| Translation subgroup | Z₂³ (full group on itself) | T ≅ Z₂³ (subgroup of Z₂⁶, index 8) |
| Orbits of T | 1 (the whole set) | 8 (cosets of T) |
| Quotient space | trivial | Z₂⁶/T ≅ Z₂³ |
| Additional symmetry on quotient | S₄ on 4 blocks | S₃ on 8 residuals |
| Macro-orbits | 4 blocks of 2 | 4 orbits (8,8,24,24) |
| Key group | S₄ ⋊ Z₂⁴ = ... | (Z₂ ≀ S₃) × Z₂³ = 384 |

The bridge: at n=6, the quotient Z₂⁶/⟨O,M,I⟩ ≅ Z₂³ creates a new 8-element space isomorphic to the trigram space. S₃ (pair permutations) acts on this quotient with orbits {000}, {111}, {wt=1}, {wt=2} — the 4 macro-orbits. The pairing structure of the KW tradition lives on this quotient.

### What the residual means for KW pairing

**All three involutions σ₁, σ₂, σ₃ preserve the residual.** This is because:
- σ₂ (reversal): swaps L_i ↔ L_{7-i} within each pair, so L_i⊕L_{7-i} unchanged ✓
- σ₁ (complement): flips both bits of each pair: (1-L_i)⊕(1-L_{7-i}) = L_i⊕L_{7-i} ✓
- σ₃ = σ₁∘σ₂: composition of two residual-preserving maps ✓

Every KW pair {h, partner(h)} lies **within a single T-orbit** — no pair crosses between orbits. The 32 pairs decompose as 4 pairs per T-orbit.

The T-orbit residual is therefore a complete invariant of the pairing structure: the KW pairing operates independently within each of the 8 fibers of the residual map.

Within each T-orbit, all 3 involutions produce 4 pairs. But fixed points collapse choices:
- **Orbit 000** (palindromes): rev(h)=h, so comp∘rev=comp. Only **1 distinct pairing** (complement).
- **Orbit 111** (anti-palindromes): rev(h)=comp(h), so rev pairs = comp pairs. Only **1 distinct pairing**.
- **All other orbits**: all 3 involutions give **3 distinct pairings**.

Since the G_384 macro-orbits merge T-orbits with the same pairing count (via S₃):
- Macro-orbit A (res=000, 1 T-orbit): 1 option
- Macro-orbit B (res=111, 1 T-orbit): 1 option
- Macro-orbit C (res wt=1, 3 T-orbits): 3 options per T-orbit, but S₃ forces same choice → 3 options
- Macro-orbit D (res wt=2, 3 T-orbits): 3 options per T-orbit, but S₃ forces same choice → 3 options

Total equivariant pairings: **1 × 1 × 3 × 3 = 9** — recovering the opposition theory's count exactly.

KW chooses reversal for orbits C and D, complement (forced) for A and B.
