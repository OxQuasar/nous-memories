# Phase C: Algebraic Generation Test

## Probe 6: Constructive Decomposition

### Three-layer construction

**Layer 1 — b₀⊕b₁ parity:**
- Parity 0: {000, 011, 100, 111} = {Kun, Dui, Gen, Qian}
- Parity 1: {001, 010, 101, 110} = {Zhen, Kan, Li, Xun}

**Layer 2 — b₀ within parity-0:**
- b₀=0: {000, 100} → Earth
- b₀=1: {011, 111} → Metal

**Layer 3 — complement pair choice within parity-1:**
- Complement pairs available: [(1, 6), (2, 5)]
- Traditional: keep (1, 6) → Wood, singletons [2, 5] → Water, Fire
- Alternative: keep (2, 5) → Alt-Pair, singletons [1, 6]

### Verification

| Trigram | Value | Traditional | Reconstructed | Match |
|---------|-------|-------------|---------------|-------|
| Kun ☷ | 000 | Earth | Earth | ✓ |
| Zhen ☳ | 001 | Wood | Wood | ✓ |
| Kan ☵ | 010 | Water | Water | ✓ |
| Dui ☱ | 011 | Metal | Metal | ✓ |
| Gen ☶ | 100 | Earth | Earth | ✓ |
| Li ☲ | 101 | Fire | Fire | ✓ |
| Xun ☴ | 110 | Wood | Wood | ✓ |
| Qian ☰ | 111 | Metal | Metal | ✓ |

**All 8 trigrams match: True** ✓

The three-layer decomposition (2 algebraic + 1 cosmological) reconstructs 五行 exactly.

## Probe 7: Impossibility Tests

### 7a. Subgroup quotient

Z₂³ subgroup orders: [1, 2, 4, 8]
Quotient by order-k subgroup gives equal-size classes of size k.
Wuxing class sizes = {2,2,2,1,1} — not all equal.
**Result: impossible** — Subgroup quotients produce equal-size classes; Wuxing has sizes {2,2,2,1,1}

### 7b. Kernel of linear map

**Result: impossible** — Kernel of linear map is a subgroup; preimages are cosets of equal size

### 7c. Orbit of affine map

**Result: impossible** — no element of Aff(3,F₂) has orbit structure matching 五行's class sizes {2,2,2,1,1}

Orbit sizes of affine maps on Z₂³:
  (1, 1, 1, 1, 1, 1, 1, 1)
  (1, 1, 1, 1, 2, 2)
  (1, 1, 2, 4)
  (1, 1, 3, 3)
  (1, 7)
  (2, 2, 2, 2)
  (2, 6)
  (4, 4)

Target shape (1,1,2,2,2) does NOT exist among orbit shapes.


### 7d. Boolean function classification

| Construction | Can produce Wuxing? |
|-------------|-------------------|
| 2 arbitrary Boolean functions | No (max 4 classes from 2 bits) |
| 3 arbitrary Boolean functions | Yes |
| 3 affine (linear) functions | No |
| 2 symmetric functions | No |
| 3 symmetric functions | No |

**Key finding:** 3 arbitrary Boolean functions CAN produce Wuxing, but 3 LINEAR functions cannot. This confirms the partition requires at least one non-linear (cosmological) function.

**Symmetric functions:** Even 3 symmetric (popcount-based) functions cannot produce Wuxing. The partition is not derivable from yang count alone.

## Probe 8: The Alternative Partition

The alternative partition makes the opposite Layer-3 choice: keep {Kan(010), Li(101)} together, split {Zhen(001), Xun(110)}.

### Alternative partition

| Trigram | Value | Traditional | Alternative |
|---------|-------|-------------|-------------|
| Kun ☷ | 000 | Earth | Earth |
| Zhen ☳ | 001 | Wood | Alt-Sing-A |
| Kan ☵ | 010 | Water | Alt-Pair |
| Dui ☱ | 011 | Metal | Metal |
| Gen ☶ | 100 | Earth | Earth |
| Li ☲ | 101 | Fire | Alt-Pair |
| Xun ☴ | 110 | Wood | Alt-Sing-B |
| Qian ☰ | 111 | Metal | Metal |

### Comparison

| Metric | Traditional 五行 | Alternative |
|--------|-----------------|-------------|
| MI(Later Heaven) | 1.7500 | 1.5000 ← |
| MI(Yang count) | 1.0613 | 1.0613 = |
| MI(Basin(TT)) | 1.0000 | 0.7500 ← |
| MI(Complement) | 1.5000 | 1.5000 = |
| Total MI | 5.3113 | 4.8113 |
| |Aut| (unlabeled) | 8 | 8 |
| LH quadrant pairs kept | 2/4 | 1/4 |
| Mean intra-pair Hamming | 1.67 | 1.67 |

Traditional 五行 keeps **2** Later Heaven quadrant pairs intact vs **1** for the alternative. 
This confirms: the cosmological binary choice maximizes compass alignment.

### Later Heaven quadrant pair analysis

| Quadrant | Pair | Trad same class? | Alt same class? |
|----------|------|-----------------|-----------------|
| East | Zhen, Xun | ✓ (Wood/Wood) | ✗ (Alt-Sing-A/Alt-Sing-B) |
| South | Li, Kun | ✗ (Fire/Earth) | ✗ (Alt-Pair/Earth) |
| West | Dui, Qian | ✓ (Metal/Metal) | ✓ (Metal/Metal) |
| North | Kan, Gen | ✗ (Water/Earth) | ✗ (Alt-Pair/Earth) |

## Probe 9: Later Heaven Alignment Ranking

Total (2,2,2,1,1) partitions: 420

**Traditional 五行:**
- MI(LH) = 1.7500
- Rank: 5/420 (top 1.2%)
- LH quadrant pairs kept: 2/4

**Alternative partition:**
- MI(LH) = 1.5000
- Rank: 29/420 (top 6.9%)

### Partitions with higher MI(LH) than traditional 五行

Count: 4

| # | MI(LH) | LH pairs kept | Classes |
|---|--------|---------------|---------|
| 1 | 2.0000 | 3/4 | {Kan, Gen}; {Kun, Li}; {Zhen, Xun}; {Qian}; {Dui} |
| 2 | 2.0000 | 3/4 | {Dui, Qian}; {Kun, Li}; {Zhen, Xun}; {Kan}; {Gen} |
| 3 | 2.0000 | 3/4 | {Dui, Qian}; {Kun, Li}; {Kan, Gen}; {Zhen}; {Xun} |
| 4 | 2.0000 | 3/4 | {Dui, Qian}; {Kan, Gen}; {Zhen, Xun}; {Kun}; {Li} |

Of 4 partitions beating Wuxing's MI(LH), 4 keep ≥3 LH pairs.

**Element coherence of higher-MI partitions:**

All 4 keep 3 LH quadrant pairs as partition-pairs. But every one of them includes {Kun(000), Li(101)} — the South quadrant pair — which mixes Earth and Fire (a 生 relationship: Fire generates Earth). Traditional 五行 specifically BREAKS this compass pair, sacrificing compass alignment to preserve element separation.

Observation: with only 3 pair-slots for 4 quadrant pairs, any (2,2,2,1,1) partition must break at least one. The 4 higher-MI partitions all choose to keep South (Earth+Fire). Traditional 五行 is the ONLY partition at its MI level that keeps East (Wood) and West (Metal) — the two quadrants where the compass pairing coincides with element identity.

### MI(LH) value distribution

| MI(LH) value | # partitions | Cumulative |
|-------------|-------------|-----------|
| 2.0000 | 4 | 4 |
| 1.7500 | 24 | 28 ← Wuxing |
| 1.5000 | 120 | 148 ← Alternative |
| 1.2500 | 272 | 420 |

## Probe 10: Parity and XOR Masks

### XOR mask parity properties

Does b₀⊕b₁ parity separate 生-exclusive from 克-exclusive XOR masks?

| Mask | Binary | Category | Preserves parity? |
|------|--------|----------|------------------|
| 1 | 001 | shared       | ✗ |
| 2 | 010 | ke_only      | ✗ |
| 3 | 011 | sheng_only   | ✓ |
| 4 | 100 | sheng_only   | ✓ |
| 5 | 101 | shared       | ✗ |
| 6 | 110 | ke_only      | ✗ |
| 7 | 111 | shared       | ✓ |

**生-exclusive masks ({011, 100}) all preserve parity: True**
**克-exclusive masks ({010, 110}) all break parity: True**

This confirms: **生 is parity-respecting, 克 is parity-breaking.**
The b₀⊕b₁ parity — Layer 1 of the 五行 decomposition — is precisely the feature that separates the geometric character of 生 from 克.

Structural interpretation:
- 生 (generation) flows WITHIN the two cosets — it respects the algebraic divide
- 克 (overcoming) flows ACROSS the two cosets — it bridges the algebraic divide
- This is the bit-algebraic basis for the traditional principle that generation is harmonious (stays within) while overcoming is confrontational (crosses)

## Summary

### Algebraic generation verdict


| Test | Result |
|------|--------|
| Subgroup quotient | Impossible (unequal class sizes) |
| Kernel of linear map | Impossible (cosets have equal size) |
| Orbit of affine map | Impossible (orbit shape not achievable) |
| 2 Boolean functions | Impossible (max 4 classes) |
| 3 Boolean functions | Possible |
| 3 affine functions | Impossible |
| Symmetric functions | Impossible (even 3 insufficient) |
| Constructive decomposition | ✓ (2 linear + 1 non-linear) |

### The 0.5-bit cosmological choice


Within the parity-1 coset {001, 010, 101, 110}, there are exactly **2 complement pairs**:
- (1, 6) = (Zhen, Xun)
- (2, 5) = (Kan, Li)

Choosing which pair stays together is a single binary decision — 0.5 bits (weighted by the coset's probability mass of 4/8).

The traditional choice (Zhen+Xun=Wood) is the one that maximizes Later Heaven compass alignment: MI(LH) = 1.7500 (rank 5/420). The alternative choice gives MI(LH) = 1.5000 (rank 29/420).

### What the algebra does and doesn't determine


**Determined by Z₂³ algebra alone:**
- Earth and Metal are distinguished from Wood, Fire, Water (Layer 1)
- Earth is distinguished from Metal (Layer 2)
- 生 respects the Layer-1 divide; 克 crosses it
- The pair structure within Earth and Metal (both edge pairs, XOR=100)
- The singleton nature of Fire and Water

**Requires external (cosmological) input:**
- Which of {Zhen,Xun} vs {Kan,Li} forms the pair class
- This choice is resolved by Later Heaven compass alignment
- It cannot be derived from any linear, symmetric, or orbit-based construction
