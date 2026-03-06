# Phase 3: 互卦 (Hùguà) Self-Similarity Test

The 互卦 extracts the nuclear core and re-expands it:
given hexagram h = L1-L2-L3-L4-L5-L6, 互卦(h) = L2-L3-L4-L3-L4-L5.
This tests whether KW opposition is self-similar under nuclear projection.

## 1. The 互卦 Map

**Image size:** 16 of 64 hexagrams
(the 互卦 map is 16-to-64, i.e., 4.0:1 average preimage size)

**Idempotent:** hugua(hugua(x)) = hugua(x) for all x? **False**

Failures: 56 of 64 hexagrams.
The 互卦 is NOT a retraction — the image is not stable under reapplication.

**hugua²(x) = hugua(hugua(x))** converges to 4 hexagrams:
these are the L3,L4-alternation patterns (L3,L4,L3,L4,L3,L4).

| hugua² value | Binary | Structure |
|-------------|--------|-----------|
|  0 | 000000 | L3=0, L4=0 alternating |
| 21 | 010101 | L3=1, L4=0 alternating |
| 42 | 101010 | L3=0, L4=1 alternating |
| 63 | 111111 | L3=1, L4=1 alternating |

**Iteration depth:** hugua converges in exactly 2 steps (hugua³ = hugua²).
Each application peels off one layer: hugua strips L1,L6; hugua² additionally
collapses L2,L5 into the L3,L4 pattern.

**Fixed points** (x = hugua(x)): **2**

| Fixed point | Binary | Lines | Structure |
|------------|--------|-------|-----------|
|  0 | 000000 | 000000 | L1=L3=L5, L2=L4=L6 |
| 63 | 111111 | 111111 | L1=L3=L5, L2=L4=L6 |

### Image structure

The 互卦 output always satisfies **bit1 = bit3** and **bit2 = bit4**
(because L3 is placed at both positions 1,3 and L4 at positions 2,4).
This constrains the image to exactly 16 = 2⁴ hexagrams
(4 free bits: L2=bit0, L3=bit1, L4=bit2, L5=bit5).

Fixed points ⊂ image? **True**
Fixed points = image? **False** — the image is much larger (16) than the fixed set (2).
Most image hexagrams are NOT fixed under reapplication.

### Image of 互卦 with preimage sizes

| 互卦 hex | Binary | Preimage size | Preimage hexagrams |
|---------|--------|--------------|-------------------|
|  0 | 000000 | 4 | 000000, 000001, 100000, 100001 |
|  1 | 000001 | 4 | 000010, 000011, 100010, 100011 |
| 10 | 001010 | 4 | 000100, 000101, 100100, 100101 |
| 11 | 001011 | 4 | 000110, 000111, 100110, 100111 |
| 20 | 010100 | 4 | 001000, 001001, 101000, 101001 |
| 21 | 010101 | 4 | 001010, 001011, 101010, 101011 |
| 30 | 011110 | 4 | 001100, 001101, 101100, 101101 |
| 31 | 011111 | 4 | 001110, 001111, 101110, 101111 |
| 32 | 100000 | 4 | 010000, 010001, 110000, 110001 |
| 33 | 100001 | 4 | 010010, 010011, 110010, 110011 |
| 42 | 101010 | 4 | 010100, 010101, 110100, 110101 |
| 43 | 101011 | 4 | 010110, 010111, 110110, 110111 |
| 52 | 110100 | 4 | 011000, 011001, 111000, 111001 |
| 53 | 110101 | 4 | 011010, 011011, 111010, 111011 |
| 62 | 111110 | 4 | 011100, 011101, 111100, 111101 |
| 63 | 111111 | 4 | 011110, 011111, 111110, 111111 |

**Preimage size distribution:**

| Size | Count |
|------|-------|
| 4 | 16 |

## 2. Self-Similarity Test: Does KW Pairing Descend to 互卦?

**KW pairs preserved:** 28 of 32 pairs have hugua(a), hugua(b) forming a KW pair.

**Commutativity:** hugua(kw(x)) = kw(hugua(x)) for all x? **False**

8 failures:

| x | Binary | hugua(kw(x)) | kw(hugua(x)) |
|---|--------|-------------|-------------|
|  1 | 000001 | 000000 | 111111 |
| 13 | 001101 | 011110 | 100001 |
| 19 | 010011 | 100001 | 011110 |
| 31 | 011111 | 111111 | 000000 |
| 32 | 100000 | 000000 | 111111 |
| 44 | 101100 | 011110 | 100001 |
| 50 | 110010 | 100001 | 011110 |
| 62 | 111110 | 111111 | 000000 |

**Pairing compatible with nuclear projection:** False
(If hugua(a₁) = hugua(a₂), is hugua(b₁) = hugua(b₂)?)

Compatibility failures:

- hugua value 000000 maps to partners: {000000, 111111}
- hugua value 011110 maps to partners: {011110, 100001}
- hugua value 100001 maps to partners: {011110, 100001}
- hugua value 111111 maps to partners: {000000, 111111}

## 3. Full 互卦 Pair Table

| # | a | b | Type | hugua(a) | hugua(b) | KW pair? | Relation | XOR | Sig? | Δw |
|---|---|---|------|----------|----------|----------|----------|-----|------|-----|
| 1 | 000000 | 111111 | pal | 000000 | 111111 | ✓ | complement | 111111 | ✓ | 6 |
| 2 | 000001 | 100000 | rev | 000000 | 000000 | ✗ | identity | 000000 | ✗ | 0 |
| 3 | 000010 | 010000 | rev | 000001 | 100000 | ✓ | reversal | 100001 | ✓ | 0 |
| 4 | 000011 | 110000 | rev | 000001 | 100000 | ✓ | reversal | 100001 | ✓ | 0 |
| 5 | 000100 | 001000 | rev | 001010 | 010100 | ✓ | reversal | 011110 | ✓ | 0 |
| 6 | 000101 | 101000 | rev | 001010 | 010100 | ✓ | reversal | 011110 | ✓ | 0 |
| 7 | 000110 | 011000 | rev | 001011 | 110100 | ✓ | reversal | 111111 | ✓ | 0 |
| 8 | 000111 | 111000 | rev | 001011 | 110100 | ✓ | reversal | 111111 | ✓ | 0 |
| 9 | 001001 | 100100 | rev | 010100 | 001010 | ✓ | reversal | 011110 | ✓ | 0 |
| 10 | 001010 | 010100 | rev | 010101 | 101010 | ✓ | reversal | 111111 | ✓ | 0 |
| 11 | 001011 | 110100 | rev | 010101 | 101010 | ✓ | reversal | 111111 | ✓ | 0 |
| 12 | 001100 | 110011 | pal | 011110 | 100001 | ✓ | complement | 111111 | ✓ | 2 |
| 13 | 001101 | 101100 | rev | 011110 | 011110 | ✗ | identity | 000000 | ✗ | 0 |
| 14 | 001110 | 011100 | rev | 011111 | 111110 | ✓ | reversal | 100001 | ✓ | 0 |
| 15 | 001111 | 111100 | rev | 011111 | 111110 | ✓ | reversal | 100001 | ✓ | 0 |
| 16 | 010001 | 100010 | rev | 100000 | 000001 | ✓ | reversal | 100001 | ✓ | 0 |
| 17 | 010010 | 101101 | pal | 100001 | 011110 | ✓ | complement | 111111 | ✓ | 2 |
| 18 | 010011 | 110010 | rev | 100001 | 100001 | ✗ | identity | 000000 | ✗ | 0 |
| 19 | 010101 | 101010 | rev | 101010 | 010101 | ✓ | reversal | 111111 | ✓ | 0 |
| 20 | 010110 | 011010 | rev | 101011 | 110101 | ✓ | reversal | 011110 | ✓ | 0 |
| 21 | 010111 | 111010 | rev | 101011 | 110101 | ✓ | reversal | 011110 | ✓ | 0 |
| 22 | 011001 | 100110 | rev | 110100 | 001011 | ✓ | reversal | 111111 | ✓ | 0 |
| 23 | 011011 | 110110 | rev | 110101 | 101011 | ✓ | reversal | 011110 | ✓ | 0 |
| 24 | 011101 | 101110 | rev | 111110 | 011111 | ✓ | reversal | 100001 | ✓ | 0 |
| 25 | 011110 | 100001 | pal | 111111 | 000000 | ✓ | complement | 111111 | ✓ | 6 |
| 26 | 011111 | 111110 | rev | 111111 | 111111 | ✗ | identity | 000000 | ✗ | 0 |
| 27 | 100011 | 110001 | rev | 000001 | 100000 | ✓ | reversal | 100001 | ✓ | 0 |
| 28 | 100101 | 101001 | rev | 001010 | 010100 | ✓ | reversal | 011110 | ✓ | 0 |
| 29 | 100111 | 111001 | rev | 001011 | 110100 | ✓ | reversal | 111111 | ✓ | 0 |
| 30 | 101011 | 110101 | rev | 010101 | 101010 | ✓ | reversal | 111111 | ✓ | 0 |
| 31 | 101111 | 111101 | rev | 011111 | 111110 | ✓ | reversal | 100001 | ✓ | 0 |
| 32 | 110111 | 111011 | rev | 101011 | 110101 | ✓ | reversal | 011110 | ✓ | 0 |

## 4. Relationship Summary

### 互卦 pair relationship distribution

| Relationship | Count |
|-------------|-------|
| reversal | 24 |
| complement | 4 |
| identity | 4 |

#### Reversal pairs (28)

| Relationship | Count |
|-------------|-------|
| reversal | 24 |
| identity | 4 |

#### Palindromic pairs (4)

| Relationship | Count |
|-------------|-------|
| complement | 4 |

### 互卦 XOR mask distribution

| XOR mask | Count | Signature mask? | popcount |
|----------|-------|----------------|----------|
| 000000 | 4 | ✗ | 0 |
| 011110 | 8 | ✓ | 4 |
| 100001 | 8 | ✓ | 2 |
| 111111 | 12 | ✓ | 6 |

## 5. Weight Analysis at 互卦 Level

**Mean |Δw|:** 0.5000

**Weight correlation:** r = 0.5000

| Δw | Count | Pair types |
|----|-------|------------|
| 0 | 28 | reversal: 28 |
| 2 | 2 | palindromic: 2 |
| 6 | 2 | palindromic: 2 |

**Comparison:** hexagram-level mean |Δw| = 0.3750 (互卦 level = 0.5000)

## 6. Structural Analysis

### 6.1 The 互卦 map in mirror-pair terms

The 互卦 discards L1 and L6 (the outer pair) and duplicates L3, L4 (the inner pair).
In mirror-pair terms: it **erases O** (outer), **preserves M** (middle), and **doubles I** (inner).

Algebraic consequences for the KW pairing:

**Reversal pairs** (b = rev₆(a)): The hexagram-level XOR mask is palindromic with
signature (o,m,i). The 互卦 erases the O-component, so the 互卦 XOR depends only on M and I.
This reduces the 7-mask vocabulary to 3+1 effective masks (plus identity when only O differs).

**Palindromic (complement) pairs** (b = comp(a)): hugua commutes with complement exactly —
complement flips all bits including L2-L5, and hugua(comp(x)) = comp(hugua(x)).
So all 4 palindromic pairs map to complement pairs at the 互卦 level.

### 6.2 Reversal pair fate under 互卦

| 互卦 relationship | Count | Mechanism |
|-------------------|-------|-----------|
| reversal | 24 | M or I (or both) differ → reversal persists |
| identity | 4 | Only O differs → opposition erased |
| complement | 0 | — |
| other | 0 | — |

The 4 **identity** cases are reversal pairs whose only opposition is at the outer pair.
These have hexagram-level signature (1,0,0) — erasing O leaves no difference.

| # | a | b | Hex XOR | Signature |
|---|---|---|---------|-----------|
| 2 | 000001 | 100000 | 100001 | (1,0,0) |
| 13 | 001101 | 101100 | 100001 | (1,0,0) |
| 18 | 010011 | 110010 | 100001 | (1,0,0) |
| 26 | 011111 | 111110 | 100001 | (1,0,0) |

### 6.3 The XOR mask reduction

The 7 hexagram-level signature masks reduce under 互卦 as follows:

| Hex signature | Hex mask | 互卦 XOR | Popcount | O erased? |
|--------------|----------|---------|----------|-----------|
| (0,0,1) | 001100 | 011110 | 4 | no |
| (0,1,0) | 010010 | 100001 | 2 | no |
| (0,1,1) | 011110 | 111111 | 6 | no |
| (1,0,0) | 100001 | 000000 | 0 | yes |
| (1,0,1) | 101101 | 011110 | 4 | no |
| (1,1,0) | 110011 | 100001 | 2 | no |
| (1,1,1) | 111111 | 111111 | 6 | no |

Signature pairs with same (m,i) but different o collapse to the same 互卦 XOR:
- (0,0,1) and (1,0,1) → 011110
- (0,1,0) and (1,1,0) → 100001
- (0,1,1) and (1,1,1) → 111111
- (1,0,0) → 000000 (opposition erased)

The 7 hexagram masks reduce to **3 nonzero 互卦 masks + identity**.
The outer pair is invisible; opposition at the 互卦 level is determined entirely by M and I.

**Note:** In the 互卦 image (where bit1=bit3, bit2=bit4), reversal and complement
can coincide on certain hexagrams. For example, reverse₆(001011) = 110100 = complement(001011).
This means the 互卦 XOR mask 111111 can arise from both reversal and complement operations,
unlike at the full hexagram level where they are always distinct.

## 7. Commutativity Analysis

The key algebraic question: does this diagram commute?

```
       kw_partner
  x  ───────────→  kw(x)
  │                  │
  │ hugua            │ hugua
  ↓                  ↓
hugua(x) ─────→  hugua(kw(x))
       kw_partner?
```

**Result: False**

The diagram fails to commute for **8 of 64** hexagrams.

### Failure mechanism

All failures share the same structure: x is **non-palindromic** but hugua(x) is **palindromic**.

- Left path: kw(x) = rev(x) → hugua(rev(x))
- Right path: hugua(x) is palindromic → kw(hugua(x)) = **comp**(hugua(x))
- But hugua(rev(x)) = **rev**(hugua(x)) (the reversal propagates through hugua)
- Since hugua(x) is palindromic: rev(hugua(x)) = hugua(x) ≠ comp(hugua(x))

The failure is a **palindrome boundary crossing**: the 互卦 map changes the palindrome
status of the hexagram, which switches which branch of the KW rule applies.
The two paths compute rev vs comp of the same 互卦, producing different results.

### The 8 palindrome-boundary hexagrams

| x | Palindromic? | hugua(x) | hg(x) palindromic? | hugua(kw(x)) | kw(hugua(x)) |
|---|-------------|----------|--------------------|--------------|--------------| 
| 000001 | False | 000000 | True | 000000 | 111111 |
| 001101 | False | 011110 | True | 011110 | 100001 |
| 010011 | False | 100001 | True | 100001 | 011110 |
| 011111 | False | 111111 | True | 111111 | 000000 |
| 100000 | False | 000000 | True | 000000 | 111111 |
| 101100 | False | 011110 | True | 011110 | 100001 |
| 110010 | False | 100001 | True | 100001 | 011110 |
| 111110 | False | 111111 | True | 111111 | 000000 |

These form **4 KW pairs** (each pair contributes both members to the failure list).
All are non-palindromic hexagrams with signature (1,0,0) whose reversal partner
differs only at L1,L6. Their 互卦 is palindromic because the inner 4 bits (L2-L5)
happen to form a palindrome, even though the full 6-bit hexagram does not.
