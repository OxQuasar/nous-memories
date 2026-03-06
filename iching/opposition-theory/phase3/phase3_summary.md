# Phase 3 Summary: Nuclear Trigrams and the L3|L4 Membrane

## What Was Tested

Three analyses probing whether the nuclear/trigram decomposition carries
independent opposition information beyond the hexagram-level pairing:

1. **Trigram decomposition** (`trigram_decomposition.py`): Full trigram and nuclear trigram
   extraction for all 32 KW pairs. Relationship classification, XOR mask analysis,
   weight preservation at each sub-hexagram level.
2. **互卦 self-similarity** (`hugua_test.py`): Does the 互卦 projection (nuclear core → hexagram)
   preserve the KW pairing? Commutativity test, image structure, weight analysis.
3. **Phase 3 cleanup** (`phase3_cleanup.py`): Confirm failure set identity, close loose ends.

---

## Main Result: The Nuclear Level Is a Projection, Not Independent

The nuclear trigram decomposition carries no opposition information beyond what the
hexagram-level mirror-pair signature already determines. Every nuclear-level property
(XOR masks, weight differences, relationship types) is derivable from the hexagram-level
signature (O,M,I) by erasing the outer component.

The 互卦 map is a lossy projection: 64 → 16 hexagrams, 7 signature masks → 3 + identity.
It preserves 28 of 32 KW pairs and nearly commutes with the pairing (56 of 64).

---

## Finding 1: Depth-Function Separation

The 6 line positions separate into three depth layers with distinct roles under the KW pairing:

| Layer | Lines | Mirror pair | Role under KW |
|-------|-------|-------------|---------------|
| Outer | L1, L6 | O | **Weight buffer.** Erased by 互卦. Contributes to opposition
  strength but not to nuclear structure. When O is the only differing pair (sig (1,0,0)),
  opposition is invisible at the nuclear level. |
| Middle | L2, L5 | M | **Bridge.** Each line belongs to exactly one nuclear trigram
  (L2 → lower_nuc, L5 → upper_nuc). Preserved by 互卦. |
| Inner | L3, L4 | I | **Opposition core.** Both lines belong to BOTH nuclear trigrams.
  Doubled by 互卦. The structural anchor — the site where mirror-pair geometry
  and trigram geometry maximally non-align. |

This separation is not imposed — it emerges from the interaction of two independent
geometric structures (mirror-pair partition and trigram partition) at the L3|L4 boundary.

---

## Finding 2: The Palindrome Phase Boundary

**8 hexagrams** (forming 4 KW pairs) cross the palindrome threshold under 互卦:
they are non-palindromic, but their nuclear core (L2-L5) IS palindromic (L2=L5 and L3=L4).

These are exactly the hexagrams with mirror-pair signature (1,0,0) —
opposition lives entirely in the outer pair, which 互卦 discards.

| x | kw(x) | Signature | hugua(x) | hg palindromic? | hugua(kw(x)) | kw(hugua(x)) |
|---|-------|-----------|----------|-----------------|--------------|--------------|
| 000001 | 100000 | (1, 0, 0) | 000000 | True | 000000 | 111111 |
| 001101 | 101100 | (1, 0, 0) | 011110 | True | 011110 | 100001 |
| 010011 | 110010 | (1, 0, 0) | 100001 | True | 100001 | 011110 |
| 011111 | 111110 | (1, 0, 0) | 111111 | True | 111111 | 000000 |
| 100000 | 000001 | (1, 0, 0) | 000000 | True | 000000 | 111111 |
| 101100 | 001101 | (1, 0, 0) | 011110 | True | 011110 | 100001 |
| 110010 | 010011 | (1, 0, 0) | 100001 | True | 100001 | 011110 |
| 111110 | 011111 | (1, 0, 0) | 111111 | True | 111111 | 000000 |

**Confirmation:** The failure set equals {non-palindromic x : L2=L5 and L3=L4} exactly.
Predicted set size: 8, actual failure set size: 8, match: **True**.

**Mechanism:** For these hexagrams, the KW rule applies reversal (x is non-palindromic),
but 互卦 maps to a palindromic hexagram where the KW rule would apply complement.
The two paths through the commutativity diagram use different branches of the KW rule:
- hugua(kw(x)) = hugua(rev(x)) = rev(hugua(x)) = hugua(x)  ← palindromic, so rev is identity
- kw(hugua(x)) = comp(hugua(x))  ← because hugua(x) is palindromic
- Result: hugua(x) ≠ comp(hugua(x))  ← commutativity breaks

---

## Finding 3: Weight Preservation Degrades at Nuclear Level

| Level | Mean |Δw| (all 32 pairs) | Mean |Δw| (28 reversal) | Correlation r |
|-------|-------------------------|------------------------|---------------|
| Full hexagram | 0.375 | 0.000 | +0.516 |
| Nuclear trigram | 0.750 | 0.571 | +0.277 |
| Standard trigram | 1.125 | 1.071 | +0.024 |

Reversal preserves hexagram-level weight perfectly (Δw = 0 for all 28 pairs).
At sub-hexagram levels, the swap+reverse operation redistributes weight between
upper and lower components. Nuclear trigrams are more weight-stable than standard
trigrams (0.57 vs 1.07) because they share the inner pair {L3, L4},
which dampens the redistribution.

The outer pair acts as a weight buffer: removing it (via 互卦) increases mean |Δw|
from 0.375 to 0.500 for palindromic pairs, because L1 and L6 partially absorb
the weight disruption that complement imposes.

---

## Finding 4: 互卦 Map Structure

| Property | Value |
|----------|-------|
| Image size | 16 of 64 (constrained: bit1=bit3, bit2=bit4) |
| Preimage size | Uniform: 4 hexagrams per image element |
| Fixed points | 2 (000000, 111111 — all bits equal) |
| Idempotent | No — hugua² converges to 4 hexagrams (L3,L4 alternation) |
| KW pairs preserved | 28 of 32 (87.5%) |
| Commutativity | 56 of 64 (87.5%) — fails at palindrome boundary |
| 互卦 XOR masks | 3 nonzero + identity (down from 7 hex-level) |

The 互卦 is a 4:1 compression that erases the outer pair and doubles the inner pair.
It is NOT idempotent: iterated application converges in 2 steps to the 4-element set
{000000, 010101, 101010, 111111} — pure L3,L4 alternation.

---

## Mask Vocabulary Reduction Under 互卦

| Hex signature | Hex mask | 互卦 XOR |
|--------------|----------|---------|
| (0,0,1) | 001100 | 011110 |
| (1,0,1) | 101101 | 011110 |
| (0,1,0) | 010010 | 100001 |
| (1,1,0) | 110011 | 100001 |
| (0,1,1) | 011110 | 111111 |
| (1,1,1) | 111111 | 111111 |
| **(1,0,0)** | **100001** | **000000** |

Pairs differing only in O-bit collapse to the same 互卦 XOR.
Signature (1,0,0) collapses to identity — all opposition erased.

---

## Status

**Phase 3: Complete.**

No new opposition measures emerge from the nuclear/trigram decomposition.
The nuclear level is a strict projection of the hexagram level, with the outer pair erased.

One structural insight carries forward: the **depth-function separation** (outer = buffer,
inner = core) may connect to the 体/用 (tǐ/yòng) distinction in Phase 4,
where the nuclear trigram traditionally determines the 体 (substance) of a hexagram.

### Open questions resolved
- **Q5 from plan (nuclear trigram boundary):** The L3|L4 membrane does not carry
  independent opposition information. It is the site of maximal geometric non-alignment,
  but the opposition structure there is fully determined by the hexagram-level signature.

### Files
| File | Description |
|------|-------------|
| `trigram_decomposition.py` | Trigram/nuclear extraction and analysis |
| `trigram_decomposition_results.md` | Full 32-pair tables + summary statistics |
| `hugua_test.py` | 互卦 self-similarity and commutativity test |
| `hugua_results.md` | 互卦 pair table + structural analysis |
| `phase3_cleanup.py` | Failure set confirmation (this script) |
| `phase3_summary.md` | This summary document |