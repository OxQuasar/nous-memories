# Probe 5: S₄ × 五行 — Involutions, Parity, and the Semantic Gap

## A. V₄ Orbits on Trigrams vs Parity

V₄ = ⟨reverse, complement⟩ on Z₂³. Three non-identity elements:
reverse (swap b₀↔b₂), complement (XOR 111), reverse∘complement.

### Orbits

| Orbit | Trigrams | Parities (b₀⊕b₁) | Elements | Parity constant? |
|-------|---------|-------------------|----------|------------------|
| {000, 111} | Kun ☷, Qian ☰ | 0, 0 | Earth, Metal | ✓ |
| {001, 011, 100, 110} | Zhen ☳, Dui ☱, Gen ☶, Xun ☴ | 1, 0, 0, 1 | Earth, Metal, Wood | ✗ |
| {010, 101} | Kan ☵, Li ☲ | 1, 1 | Fire, Water | ✓ |

**Result:** 2/3 orbits have constant parity.
The size-4 orbit {Zhen ☳, Dui ☱, Gen ☶, Xun ☴} mixes parities [1, 0, 0, 1] and crosses three elements (Earth, Metal, Wood).

**Parity partially overlaps V₄ orbits.** The two size-2 orbits (fixed points of specific
involutions) are parity-pure, but the generic orbit crosses the parity boundary. V₄ action
does NOT respect the {Earth,Metal} / {Wood,Fire,Water} split in general.

## B. Which Involutions Preserve vs Break Parity?

### Per-involution classification

| Involution | Classification | Preserves | Breaks |
|-----------|----------------|-----------|--------|
| reverse | **mixed** | 4/8 | 4/8 |
| complement | **preserves** | 8/8 | 0/8 |
| rev∘comp | **mixed** | 4/8 | 4/8 |

### Detail: parity(t) vs parity(inv(t)) for each trigram

| Trigram | Element | Parity | Reverse | Complement | Rev∘Comp |
|---------|---------|--------|---------|------------|----------|
| Kun ☷ (000) | Earth | 0 | 0 ✓ | 0 ✓ | 0 ✓ |
| Zhen ☳ (001) | Wood | 1 | 0 ✗ | 1 ✓ | 0 ✗ |
| Kan ☵ (010) | Water | 1 | 1 ✓ | 1 ✓ | 1 ✓ |
| Dui ☱ (011) | Metal | 0 | 1 ✗ | 0 ✓ | 1 ✗ |
| Gen ☶ (100) | Earth | 0 | 1 ✗ | 0 ✓ | 1 ✗ |
| Li ☲ (101) | Fire | 1 | 1 ✓ | 1 ✓ | 1 ✓ |
| Xun ☴ (110) | Wood | 1 | 0 ✗ | 1 ✓ | 0 ✗ |
| Qian ☰ (111) | Metal | 0 | 0 ✓ | 0 ✓ | 0 ✓ |

### Key finding: complement preserves parity universally

Complement XOR mask = 111. Parity = b₀⊕b₁. Under XOR with 111:
b₀' = b₀⊕1, b₁' = b₁⊕1, so b₀'⊕b₁' = (b₀⊕1)⊕(b₁⊕1) = b₀⊕b₁. ✓

This means complement is **生-compatible** at the parity level: it preserves the
b₀⊕b₁ bit that separates {Earth,Metal} from {Wood,Fire,Water}.

Reverse swaps b₀↔b₂, changing parity to b₂⊕b₁, which ≠ b₀⊕b₁ in general.
Reverse is **mixed**: preserves parity for trigrams where b₀=b₂ (palindromes),
breaks it otherwise.

### Connection to 生/克 XOR masks

From wuxing findings:

- 生-exclusive masks {011, 100}: preserve b₀⊕b₁ parity
- 克-exclusive masks {010, 110}: break b₀⊕b₁ parity

**Complement (mask 111)** is in the *shared* mask set (used by both 生 and 克),
and it preserves parity. **Reverse (mask for b₀↔b₂ swap, not a single XOR mask)
is mixed — neither purely 生 nor 克 compatible.**

The involution-to-生克 mapping is not a clean dichotomy at the parity level.
Instead, complement is parity-preserving (生-compatible), while reverse and rev∘comp
are mixed. The semantic gap must arise from a deeper mechanism.

## C. Hexagram-Level: Does 五行 Structure Explain the Semantic Gap?

kwprobe found: reversal pairs mean similarity ~0.720, complement pairs ~0.680,
rev∘comp ~0.673 (baseline 0.683).

### Disruption metrics per involution

| Metric | reverse₆ | complement₆ | rev∘comp₆ |
|--------|----------|-------------|-----------|
| Pairs | 28 | 32 | 28 |
| Parity Δ (lower) | 16/28 (57%) | 0/32 (0%) | 16/28 (57%) |
| Parity Δ (upper) | 16/28 (57%) | 0/32 (0%) | 16/28 (57%) |
| Element Δ (lower) | 25/28 (89%) | 24/32 (75%) | 25/28 (89%) |
| Element Δ (upper) | 25/28 (89%) | 24/32 (75%) | 25/28 (89%) |
| Element SET Δ | 22/28 (79%) | 25/32 (78%) | 28/28 (100%) |
| Relation Δ (exact) | 22/28 (79%) | 25/32 (78%) | 20/28 (71%) |
| Relation Δ (比/生/克) | 14/28 (50%) | 0/32 (0%) | 14/28 (50%) |

### The critical metric: element SET preservation

Reversal swaps upper↔lower trigrams but keeps the same two elements present.
Complement changes each trigram to a different element (except Wood pairs).

- **reverse₆**: element set changes in 22/28 (79%) pairs → semantic similarity 0.720
- **complement₆**: element set changes in 25/32 (78%) pairs → semantic similarity 0.680
- **rev∘comp₆**: element set changes in 28/28 (100%) pairs → semantic similarity 0.673

**Element-set disruption rank:** complement₆(0.781) < reverse₆(0.786) < rev∘comp₆(1.000)
**Similarity rank:** reverse₆(0.720) > complement₆(0.680) > rev∘comp₆(0.673)
**Anti-correlation (more set-disruption → less similarity)?** ✗ NO

### Relation category (比/生/克) preservation

Reversal swaps the *direction* of 生/克 (e.g., 生体 ↔ 体生用) but preserves the
*category* (both are 生-type). This is a weaker disruption.

- **reverse₆**: exact relation changes 22/28 (79%), category changes 14/28 (50%)
- **complement₆**: exact relation changes 25/32 (78%), category changes 0/32 (0%)
- **rev∘comp₆**: exact relation changes 20/28 (71%), category changes 14/28 (50%)

**Category disruption rank:** complement₆(0.000) < reverse₆(0.500) < rev∘comp₆(0.500)
**Anti-correlation with similarity?** ✗ NO

### Relation transition matrix: reverse₆ (n=28)

| Original \ Transformed | 比和 | 生体 | 克体 | 体生用 | 体克用 |
|----|----|----|----|----|----|
| 比和 | **2** | 1 | 0 | 0 | 2 |
| 生体 | 0 | **2** | 1 | 2 | 0 |
| 克体 | 2 | 3 | **0** | 0 | 1 |
| 体生用 | 1 | 1 | 0 | **2** | 3 |
| 体克用 | 0 | 0 | 4 | 1 | **0** |

Diagonal (preserved): 6/28 (21%)

### Relation transition matrix: complement₆ (n=32)

| Original \ Transformed | 比和 | 生体 | 克体 | 体生用 | 体克用 |
|----|----|----|----|----|----|
| 比和 | **7** | 0 | 0 | 0 | 0 |
| 生体 | 0 | **0** | 0 | 6 | 0 |
| 克体 | 0 | 0 | **0** | 0 | 7 |
| 体生用 | 0 | 6 | 0 | **0** | 0 |
| 体克用 | 0 | 0 | 6 | 0 | **0** |

Diagonal (preserved): 7/32 (22%)

### Relation transition matrix: rev∘comp₆ (n=28)

| Original \ Transformed | 比和 | 生体 | 克体 | 体生用 | 体克用 |
|----|----|----|----|----|----|
| 比和 | **4** | 0 | 1 | 1 | 1 |
| 生体 | 1 | **1** | 0 | 0 | 2 |
| 克体 | 1 | 0 | **1** | 2 | 0 |
| 体生用 | 0 | 4 | 2 | **1** | 0 |
| 体克用 | 1 | 2 | 2 | 0 | **1** |

Diagonal (preserved): 8/28 (29%)

### Why reversal preserves meaning despite high positional disruption

Reversal pairs: 6 preserve element set, 22 change it.

Among set-preserving reversal pairs, the relation transition pattern:
  克 → 克: 3
  生 → 生: 3

Reversal = 'visual flip' of the hexagram. While it changes trigrams (reverse₃ applied
to each), 6/28 pairs preserve the element set and all set-preserving pairs preserve
the 比/生/克 category. The Tuan treats reversed hexagrams as related perspectives.

Complement = all lines flipped. New elements in most pairs, but the 比/生/克 category
is **always preserved** (0% category disruption — complement is an anti-automorphism
of the 五行 graph). Despite this, the Tuan sees different situations.

## D. Wood's Special Status

### Element preservation under each involution

**reverse:**

| Element | Size | Preserved | Broken to |
|---------|------|-----------|-----------|
| Wood (木) | 2 | 0/2 | Earth(1), Metal(1) |
| Fire (火) | 1 | 1/1 | — |
| Earth (土) | 2 | 1/2 | Wood(1) |
| Metal (金) | 2 | 1/2 | Wood(1) |
| Water (水) | 1 | 1/1 | — |

**complement:**

| Element | Size | Preserved | Broken to |
|---------|------|-----------|-----------|
| Wood (木) | 2 | 2/2 | — |
| Fire (火) | 1 | 0/1 | Water(1) |
| Earth (土) | 2 | 0/2 | Metal(2) |
| Metal (金) | 2 | 0/2 | Earth(2) |
| Water (水) | 1 | 0/1 | Fire(1) |

**rev∘comp:**

| Element | Size | Preserved | Broken to |
|---------|------|-----------|-----------|
| Wood (木) | 2 | 0/2 | Metal(1), Earth(1) |
| Fire (火) | 1 | 0/1 | Water(1) |
| Earth (土) | 2 | 0/2 | Metal(1), Wood(1) |
| Metal (金) | 2 | 0/2 | Wood(1), Earth(1) |
| Water (水) | 1 | 0/1 | Fire(1) |

### Element closure under complement

| Element | Trigrams | Complement → | Elements | Closed? |
|---------|---------|-------------|----------|---------|
| Wood | Zhen ☳, Xun ☴ | Xun ☴, Zhen ☳ | Wood, Wood | ✓ |
| Fire | Li ☲ | Kan ☵ | Water | ✗ |
| Earth | Kun ☷, Gen ☶ | Qian ☰, Dui ☱ | Metal, Metal | ✗ |
| Metal | Dui ☱, Qian ☰ | Gen ☶, Kun ☷ | Earth, Earth | ✗ |
| Water | Kan ☵ | Li ☲ | Fire | ✗ |

**Wood is the unique element closed under complement.** The complement permutation on elements:
- Earth ↔ Metal (swap)
- Fire ↔ Water (swap)
- Wood → Wood (fixed)

### Wood as the 生-cycle hinge

The 生 cycle: Wood → Fire → Earth → Metal → Water → Wood

Under complement, the cycle undergoes two transpositions: Earth↔Metal, Fire↔Water.
Applied to the cycle order:
```
Original: Wood → Fire  → Earth → Metal → Water → Wood
Compl'd:  Wood → Water → Metal → Earth → Fire  → Wood
```
The complemented cycle = the original cycle reversed (克 direction).
**Complement maps the 生 cycle to the 克 cycle.** Wood is the hinge: the fixed
point of complement, connecting the two directions of the cycle.

**Verification: π∘σ∘π⁻¹ = σ⁻¹?** (π = complement perm, σ = 生 cycle)

- Wood: π∘σ∘π⁻¹(Wood) = π(σ(Wood)) = π(Fire) = Water = σ⁻¹(Wood) = Water ✓
- Fire: π∘σ∘π⁻¹(Fire) = π(σ(Water)) = π(Wood) = Wood = σ⁻¹(Fire) = Wood ✓
- Earth: π∘σ∘π⁻¹(Earth) = π(σ(Metal)) = π(Water) = Fire = σ⁻¹(Earth) = Fire ✓
- Metal: π∘σ∘π⁻¹(Metal) = π(σ(Earth)) = π(Metal) = Earth = σ⁻¹(Metal) = Earth ✓
- Water: π∘σ∘π⁻¹(Water) = π(σ(Fire)) = π(Earth) = Metal = σ⁻¹(Water) = Metal ✓

**Complement is an anti-automorphism of the 生 cycle?** ✓ YES

This means complement reverses all directed 生-edges: if A生B, then π(B)生π(A).
Equivalently, complement swaps 生体↔体生用 and 克体↔体克用, while preserving 比和.
The *category* (比/生/克) is invariant — only the direction within each category reverses.

This explains the complement₆ transition matrix: 0% category changes, but 生体↔体生用
and 克体↔体克用 swap perfectly.

### Structural role summary

| Property | Wood | Earth/Metal | Fire/Water |
|----------|------|-------------|------------|
| Complement closure | ✓ Fixed | ✗ Swap | ✗ Swap |
| Parity | Odd (1) | Even (0) | Odd (1) |
| 生-cycle role | Hinge (start/end) | Middle | Middle |
| Trigram geometry | Body diagonal | Edge pair | Singletons |
| Basin intrusion | Both fixed-point basins | Within respective basin | Cycle basin only |

## E. The 1.50/2.25 Bit Prediction

Two related quantities:

1. **MI(五行, complement_pair_partition)** — how much does knowing the pair {t, comp(t)}
   tell you about element? This is the 1.50 from the wuxing MI matrix.
2. **MI(五行, complement_function)** — how much does element(comp(t)) tell you about
   element(t)? This is potentially different.

### 1. Complement pair partition

H(五行) = 2.2500 bits
H(五行 | complement_pair) = 0.7500 bits
MI(五行, complement_pair) = 1.5000 bits
Fraction preserved: 66.7%

Pair decomposition:

| Pair | Trigrams | Elements | H(五行 | pair) |
|------|---------|----------|---------------|
| 0 | Kun ☷, Qian ☰ | Earth, Metal | 1.0 |
| 1 | Zhen ☳, Xun ☴ | Wood, Wood | 0.0 |
| 2 | Kan ☵, Li ☲ | Water, Fire | 1.0 |
| 3 | Dui ☱, Gen ☶ | Metal, Earth | 1.0 |

Three of four pairs have distinct elements (H=1 bit each). One pair (Wood) has
identical elements (H=0). Weighted: H(五行|pair) = 3/4 × 1 + 1/4 × 0 = 0.7500

### 2. Complement function (element → element)

H(五行 | element(comp(t))) = 0.0000 bits
MI = 2.2500 bits

The complement function is a **deterministic permutation** on elements:
Earth↔Metal, Fire↔Water, Wood→Wood. Knowing element(comp(t)) determines element(t)
with zero ambiguity. Hence MI = H(五行) = 2.25.

**The 1.50 vs 2.25 gap:** the pair partition tells you WHICH pair but not WHICH
member you are. The complement function tells you exactly which element your partner
has, which determines your element. The 0.75-bit gap is the within-pair identity.

### 3. Is the missing 0.75 bits the cosmological choice?

The three-layer decomposition of H(五行) = 2.25 bits:
- Layer 1: b₀⊕b₁ parity = 1.000 bits
- Layer 2: b₀ within even coset = 0.750 bits (Earth vs Metal)
- Layer 3: complement pair choice in odd coset = 0.500 bits (cosmological)

Lost information: H(五行|pair) = 0.7500 bits

This 0.750 bits is NOT just the cosmological Layer 3 (0.500 bits). It decomposes as:
- Earth/Metal ambiguity in pair {Kun,Qian}: 0.25 bits
- Earth/Metal ambiguity in pair {Dui,Gen}: 0.25 bits
- Fire/Water ambiguity in pair {Kan,Li}: 0.25 bits
Total: 0.75 bits

The lost information spans **both** Layer 2 (Earth vs Metal, two occurrences)
**and** part of the structure that Layer 3 encodes (Fire vs Water).
It is exactly **Layer 2** in the information-theoretic sense:
complement pairs preserve Layer 1 (parity — each pair is parity-pure) and Layer 3
(which complement pair in the odd coset — {Zhen,Xun}=Wood vs {Kan,Li}=Fire/Water),
but lose Layer 2 (the within-pair identity).

**What the pair partition captures (1.500 bits):**
- Layer 1 (parity): 1.000 bits — each pair is parity-pure ✓
- Within parity-1: {Zhen,Xun}=Wood vs {Kan,Li}={Fire,Water} = 0.500 bits ✓
- Total: 1.500 bits ✓

**What it loses (0.750 bits):**
- Within parity-0: Earth vs Metal (0.750 bits, covering 4 trigrams in 2 pairs)
- Within parity-1, pair {Kan,Li}: Fire vs Water (implicit in the 0.750)

The within-pair ambiguity accounts for all lost information. The cosmological
choice (Layer 3 = 0.500 bits) is PRESERVED: the pair partition distinguishes
{Zhen,Xun} from {Kan,Li}, which is exactly the cosmological input.

### 4. Comparison across all involutions (pair partition MI)

| Involution | MI(五行, pair partition) | H(五行|pair) | Pairs |
|-----------|------------------------|------------|-------|
| complement | 1.5000 | 0.7500 | {Kun ☷, Qian ☰}, {Zhen ☳, Xun ☴}, {Kan ☵, Li ☲}, {Dui ☱, Gen ☶} |
| reverse | 1.7500 | 0.5000 | {Kun ☷}, {Zhen ☳, Gen ☶}, {Kan ☵}, {Dui ☱, Xun ☴}, {Li ☲}, {Qian ☰} |
| rev∘comp | 1.2500 | 1.0000 | {Kun ☷, Qian ☰}, {Zhen ☳, Dui ☱}, {Kan ☵, Li ☲}, {Gen ☶, Xun ☴} |

| Involution | MI(五行, partner_element) | H(五行|partner_elem) |
|-----------|-------------------------|---------------------|
| complement | 2.2500 | 0.0000 |
| reverse | 1.5000 | 0.7500 |
| rev∘comp | 1.5000 | 0.7500 |

## Synthesis

### 1. Complement preserves parity — hypothesis corrected

The initial hypothesis was that complement, being 克-associated, would break parity.
In fact, complement **preserves** b₀⊕b₁ parity universally: XOR with 111 flips both
b₀ and b₁, so their XOR is unchanged. Complement belongs to the *shared* XOR mask
vocabulary (used by both 生 and 克), not the 克-exclusive set.

The 克-exclusive masks {010, 110} break parity by flipping exactly one of {b₀, b₁}.
Complement flips both, canceling the effect. Reverse replaces b₀ with b₂ in the
parity calculation — mixed behavior depending on whether b₀ = b₂.

### 2. Complement is an anti-automorphism of 五行 — the deepest structural finding

The complement permutation π = (Earth↔Metal)(Fire↔Water)(Wood) conjugates the 生 cycle
to its inverse: π∘σ∘π⁻¹ = σ⁻¹. This means complement reverses all directed edges in the
五行 graph. Consequences:

- 比和 → 比和 (identity preserved)
- 生体 ↔ 体生用 (direction of generation reverses)
- 克体 ↔ 体克用 (direction of overcoming reverses)
- **The 比/生/克 category is always preserved** (0% category disruption at hex level)

This is why the complement₆ transition matrix is perfectly block-diagonal: every pair
stays within its 比/生/克 class. The complement swaps 'who generates whom' but preserves
*whether* generation or overcoming is occurring.

### 3. The semantic gap has a layered explanation

The three involutions create a hierarchy of 五行 disruption:

| Layer | reverse₆ | complement₆ | rev∘comp₆ |
|-------|----------|-------------|-----------|
| 比/生/克 category | 50% changed | **0% changed** | 50% changed |
| Element vocabulary | 22/28 (79%) changed | 25/32 (78%) changed | 28/28 (100%) changed |
| Semantic similarity | 0.720 | 0.680 | 0.673 |

The semantic similarity does NOT track 比/生/克 preservation (complement has 0% disruption
but only middle similarity). Nor does it purely track element-set changes (reverse and
complement are nearly equal at ~79%). The gap arises from what reversal uniquely preserves:

**Reversal produces the 'visual flip'** — the hexagram turned upside down. While this
also reverses bits within each trigram (not just swapping positions), it preserves the
hexagram's 'shape.' The Tuan sees structurally related situations. Complement preserves
the abstract interaction category but changes all concrete elements — structurally
analogous but elementally different situations. Rev∘comp changes both.

The semantic hierarchy: **visual flip** (0.720) > **category-preserving element change**
(0.680) > **full disruption** (0.673). The gap between reverse and complement is the
difference between concrete similarity and abstract structural analogy.

### 4. Wood is the complement fixed point and cycle conjugator

Wood is the unique element closed under complement. The complement permutation maps the 生
cycle to its inverse, with Wood as the fixed point. This is the algebraic expression of
Wood's role as universal intruder: it bridges 生 and 克 because it is the hinge where
the direction of causation reverses. Wood creates 克 friction in every convergence path
because it connects the two directions of the cycle.

### 5. The complement pair captures 1.500/2.250 bits — cosmological choice preserved

MI(五行, complement_pair_partition) = 1.500 bits (67%). The 0.750 bits lost is the
within-pair element identity. The cosmological choice (Layer 3 = 0.500 bits) is
PRESERVED: complement pairs distinguish {Zhen,Xun}=Wood from {Kan,Li}={Fire,Water}.
The complement function itself preserves ALL 五行 information (MI = 2.250): it is a
deterministic permutation on elements. The 1.500 of the pair partition reflects the
loss of *which member you are*, not any structural degradation.

### 6. Summary of corrections to initial hypotheses

| Hypothesis | Result |
|-----------|--------|
| Complement breaks parity | **Wrong.** Complement preserves parity (mask 111 flips b₀ and b₁ together) |
| Complement is 克-compatible | **Partially wrong.** At parity level, complement is in the shared vocabulary. As a permutation on elements, complement is an anti-automorphism (reverses both 生 and 克 directions) |
| 五行 disruption rank-orders with semantic similarity | **Wrong for simple metrics.** Category disruption anti-correlates with the gap. The semantic gap tracks concrete trigram identity, not abstract relational structure |
| Missing 33% = cosmological choice | **Wrong.** Missing 0.750 bits = within-pair ambiguity (Layer 2), not Layer 3. The cosmological choice is preserved by complement pairs |
| Complement predicts 67% of 五行 | **Correct as pair partition.** But as a function, complement predicts 100% of 五行 — it's a perfect permutation |