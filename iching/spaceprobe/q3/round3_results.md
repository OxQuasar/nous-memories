# Q3 Round 3: KW Pairing Verification and Closing Gaps — Results

## Part 1: The 9 Equivariant Pairings

All 9 pairings enumerated explicitly. Each arises from choosing one of {rev, comp, comp∘rev} for macro-orbits C (residual weight 1) and D (residual weight 2). Macro-orbits A (palindromes) and B (anti-palindromes) are forced.

| # | C_op | D_op | S | WT | D (bits) | #masks | Notes |
|---|------|------|---|------|----------|--------|-------|
| **1 (KW)** | **rev** | **rev** | **120** | **0.375** | **2.750** | **7** | **Min WT, max D** |
| 2 | rev | comp | 144 | 1.125 | 1.549 | 4 | |
| 3 | rev | comp∘rev | 96 | 1.125 | 2.000 | 4 | Min S |
| 4 | comp | rev | 168 | 1.125 | 1.549 | 4 | |
| 5 (Shao Yong) | comp | comp | 192 | 1.875 | 0.000 | 1 | Max S, 0 diversity |
| 6 | comp | comp∘rev | 144 | 1.875 | 1.549 | 4 | |
| 7 | comp∘rev | rev | 144 | 1.125 | 2.000 | 4 | |
| 8 | comp∘rev | comp | 168 | 1.875 | 1.549 | 4 | |
| 9 (KW mirror) | comp∘rev | comp∘rev | 120 | 1.875 | 2.750 | 7 | Same S,D as KW |

**KW is the unique minimizer of weight tilt (WT = 0.375)** — the gap to the next best (1.125) is threefold. KW also uniquely maximizes mask diversity (tied with #9 at 2.750 bits). It does NOT maximize opposition strength S — the Shao Yong pairing (#5, all complement) achieves S=192 vs KW's 120.

**Pairings #1 and #9 are algebraic twins** — same S, same D, same mask vocabulary (all 7 masks used). They differ only in weight tilt: KW preserves weight (reversal), #9 inverts it (comp∘rev). This confirms the opposition theory's characterization.

## Part 2: KW Pairing Verification

**KW rule:** reverse the hexagram; if result is itself (palindrome), complement instead.

KW matches **pairing #1** (C=rev, D=rev) — verified by exhaustive comparison of all 32 pairs.

**KW mask vocabulary:**
```
I   (001100): 4 pairs     O   (100001): 4 pairs
M   (010010): 4 pairs     O⊕I (101101): 4 pairs
M⊕I (011110): 4 pairs     O⊕M (110011): 4 pairs
                           O⊕M⊕I (111111): 8 pairs
```

All 7 nonzero masks are used. The complement mask (111111) appears twice as often (8 pairs) because it serves both the forced-complement palindrome pairs AND some reversal pairs. The other 6 masks appear uniformly (4 pairs each).

**Weight structure:** 28 of 32 pairs have Δw = 0 (reversal preserves weight). The 4 palindrome pairs have Δw ∈ {2, 2, 2, 6}. Overall WT = 0.375 — the theoretical minimum given the forced complement constraint.

## Part 3: KW as Group Element

**KW ∉ G₃₈₄.**

The KW pairing is an involution (order 2) with 32 two-cycles and 0 fixed points. But it is NOT an element of the 384-element mirror-pair partition group.

**Why:** The KW pairing is a hybrid — it applies reversal on 48 hexagrams and complement on 16 (the 8 palindromes + their 8 complements). A group element must act by a single algebraic operation uniformly across all elements. The hybrid breaks this uniformity.

The three pure involutions σ₁ (complement), σ₂ (reversal), σ₃ (comp∘rev) are all in G₃₈₄. The KW pairing is a "conditional" combination of σ₂ and σ₁ that lies outside the group.

**Structural significance:** The KW pairing DEFINES the 9-pairing space (it's the unique WT-minimizer among the 9 equivariant pairings), but it is not itself a group symmetry. It is a SELECTION from the group's orbit structure, not a member of the group. The group constrains which pairings are possible; the tradition selects among them.

## Part 4: Palindromes and Anti-palindromes

### 8 Palindromes (macro-orbit A, residual 000)

| Binary | w | Upper/Lower |
|--------|---|-------------|
| 000000 | 0 | Kun/Kun |
| 001100 | 2 | Gen/Zhen |
| 010010 | 2 | Kan/Kan |
| 011110 | 4 | Xun/Dui |
| 100001 | 2 | Zhen/Gen |
| 101101 | 4 | Li/Li |
| 110011 | 4 | Dui/Xun |
| 111111 | 6 | Qian/Qian |

Palindromes have upper and lower trigrams that are either equal (Kun/Kun, Kan/Kan, Li/Li, Qian/Qian) or reversed-complement pairs (Gen/Zhen, Zhen/Gen, Xun/Dui, Dui/Xun). Weight range: {0, 2, 4, 6} — all even.

### 8 Anti-palindromes (macro-orbit B, residual 111)

| Binary | w | Upper/Lower |
|--------|---|-------------|
| 000111 | 3 | Kun/Qian |
| 001011 | 3 | Gen/Xun |
| 010101 | 3 | Kan/Li |
| 011001 | 3 | Xun/Gen |
| 100110 | 3 | Zhen/Dui |
| 101010 | 3 | Li/Kan |
| 110100 | 3 | Dui/Zhen |
| 111000 | 3 | Qian/Kun |

**All anti-palindromes have weight 3** (exactly half yang). Each has upper and lower trigrams that are Fu Xi complements (ι₁ pairs): Kun↔Qian, Gen↔Xun, Kan↔Li, Zhen↔Dui.

### KW pairs

**Palindrome pairs** (forced complement):
```
Kun/Kun ↔ Qian/Qian       (w=0 ↔ w=6, Δw=6)
Gen/Zhen ↔ Dui/Xun        (w=2 ↔ w=4, Δw=2)
Kan/Kan ↔ Li/Li            (w=2 ↔ w=4, Δw=2)
Xun/Dui ↔ Zhen/Gen        (w=4 ↔ w=2, Δw=2)
```

**Anti-palindrome pairs** (rev=comp, so reversal IS complement):
```
Kun/Qian ↔ Qian/Kun       (w=3 ↔ w=3, Δw=0)
Gen/Xun ↔ Dui/Zhen        (w=3 ↔ w=3, Δw=0)
Kan/Li ↔ Li/Kan            (w=3 ↔ w=3, Δw=0)
Xun/Gen ↔ Zhen/Dui        (w=3 ↔ w=3, Δw=0)
```

Anti-palindrome pairs have Δw = 0 despite being complement pairs — because all anti-palindromes have w=3.

## Part 5: Kernel of G₃₈₄ → S₃

The quotient map G₃₈₄ → S₃ (action on T-orbits) has kernel K:

| Property | Value |
|----------|-------|
| K = ⟨O, M, I, swap_L1L6, swap_L2L5, swap_L3L4⟩ | |
| \|K\| | 64 = 384/6 |
| K ≅ Z₂⁶ | Yes (abelian, all elements order ≤ 2) |
| K = T × ⟨swaps⟩ | Yes (direct product, T and swaps commute) |
| K ◁ G₃₈₄ | **Yes** (normal subgroup) |
| swap_OM ∈ K | No |
| cycle_OMI ∈ K | No |

**Short exact sequence:**
```
1 → K ≅ Z₂⁶ → G₃₈₄ → S₃ → 1
```

K is the "within-orbit" part of G₃₈₄ — it acts on hexagrams without crossing T-orbit boundaries. S₃ is the "between-orbit" part — it permutes the 3 mirror pairs as units, merging T-orbits into macro-orbits.

The decomposition G₃₈₄ = K ⋊ S₃ shows:
- K handles all transformations that preserve the residual signature
- S₃ handles all transformations that permute residual coordinates

## Part 6: Summary Comparison — n=3 vs n=6

| Property | n=3 | n=6 |
|---|---|---|
| State space | Z₂³ (8 elements) | Z₂⁶ (64 elements) |
| Translation group T | Z₂³ (full, regular rep) | Z₂³ (subgroup, index 8) |
| T-orbits | 1 (whole space) | 8 (size 8 each) |
| Quotient Z/T | trivial | Z₂³ (residual space) |
| Ambient symmetry group | ... | G₃₈₄ = (Z₂≀S₃)×Z₂³ |
| Quotient action | S₄ on 4 blocks | S₃ on 8 orbits → 4 macro-orbits |
| Macro-orbits | 4 blocks of 2 | 4 orbits (8, 8, 24, 24) |
| Kernel of quotient map | ... | K ≅ Z₂⁶ (order 64), normal |
| Equivariant pairings | 9 (under Z₂²) | 9 (under G₃₈₄) |
| Traditional pairing | complement (ι₁) | rev + comp hybrid (KW) |
| Trad. pairing ∈ group? | Yes (ι₁ ∈ Z₂³) | **No** (KW ∉ G₃₈₄) |
| KW: C_op / D_op | — | rev / rev |
| KW S (strength) | — | 120 |
| KW WT (weight tilt) | — | 0.375 (unique min) |
| KW D (diversity) | — | 2.750 (max, tied with #9) |

### Key structural finding

The coincidence of 9 equivariant pairings at both n=3 and n=6 is **not a numerical coincidence** — it arises from the same counting mechanism (independent binary choices on macro-orbits) applied to different group structures. At n=3, the choice is among 3 XOR masks for 2 independent blocks (3² = 9). At n=6, it's among 3 involutions for 2 independent macro-orbit classes (3² = 9 again). The number 9 = 3² is forced by having exactly 2 free macro-orbits and 3 candidate operations.

### The KW pairing is NOT a group element

At n=3, the traditional pairing (complement ι₁) IS a group element — it's one of the 8 translations in Z₂³. At n=6, the KW pairing (reversal where possible, complement where forced) is NOT a group element of G₃₈₄ — it's a conditional hybrid that breaks uniform algebraic action.

This is structurally inevitable: at n=3 each involution acts as a single XOR mask (uniform), while at n=6 the KW pairing must use DIFFERENT operations on the palindromic vs non-palindromic T-orbits. No single element of G₃₈₄ can do this.

The group G₃₈₄ CONSTRAINS the pairing space (from ~10¹⁷ arbitrary pairings to 9), but the KW selection within that space lies outside the group. The group defines the landscape; the tradition chooses a point on it.
