# Round 4: Comparator Analysis — Reversal Defensibility Test

## What This Round Tests

Not new alignment — 32/32 is established. This round tests the *strength* of the meaning constraint by asking: at two selected pairs, would the reversed ordering be equally defensible?

The captain selected one Clear pair (18: Jin/Ming Yi) and one Suggestive pair (27: Jian/Gui Mei). These represent opposite ends of the meaning-constraint spectrum.

---

## Test 1: Algebraic Properties of the Tested Pairs

| Property | Pair 18 (Jin/Ming Yi) | Pair 27 (Jian/Gui Mei) |
|---|---|---|
| Type | Inversion | Inversion |
| Orbit | (1,0,1) | (1,1,1) |
| M-decisive | No | Yes (conforming) |
| S2-constrained | **No** | **Yes** |
| Canon | Lower | Lower |
| Meaning confidence | Clear | Suggestive |

### Critical discovery: Pair 27 is S2-constrained

Pair 27 (Jian/Gui Mei) cannot be independently flipped. The S2 constraint at bridge B26 (between pairs 26 and 27) forbids the combinations (0,1) and (1,0) — meaning pairs 26 and 27 must be co-oriented. Flipping pair 27 alone creates an S2=2 transition.

**This means the "Suggestive" meaning rating at pair 27 is less informative than it appears.** The orientation at this pair was never a free choice — it's forced by the S2 hard constraint. The reader's meaning analysis is testing alignment with a structurally forced bit, not with a freely chosen one.

---

## Test 2: Algebraic Impact of Reversal

### Pair 18 (Jin/Ming Yi) — Free flip

| Metric | KW | Flipped | Change |
|---|---|---|---|
| χ² | 2.290 | 1.258 | **−1.032** (improved) |
| Asymmetry | +3 | +2 | −1 (degraded) |
| M-score | 12/16 | 12/16 | 0 (unchanged) |
| kac | −0.464 | −0.416 | +0.048 (degraded) |
| **Pareto status** | — | — | **Trade-off** |

Flipping Jin/Ming Yi improves χ² substantially (−1.032) but degrades asymmetry and kac. This is one of the 16 "trade-off" bits from the iter4 fragility map — flipping it moves along the Pareto frontier rather than falling off it.

**Algebraically, the reversal is a valid alternative** — it produces a different point on the trade-off surface, neither dominating nor dominated by KW. The algebraic frame provides no reason to prefer one orientation over the other at this pair.

**Semantically, the reversal is clearly inferior** — the reader found the causal asymmetry (advance → injury is inevitable; injury → advance is not), the cosmological grammar (yang/bright first), and the pattern consistency (matches Tai→Pi, Feng→Lü) all favor KW.

**This is a case where meaning disambiguates what algebra cannot.**

### Pair 27 (Jian/Gui Mei) — S2-forbidden flip

Flipping pair 27 alone violates the S2 constraint. It is structurally impossible without also flipping pair 26 (Zhen/Gen).

Flipping pairs 26+27 together:

| Metric | KW | Flipped (26+27) | Change |
|---|---|---|---|
| χ² | 2.290 | 1.774 | −0.516 (improved) |
| Asymmetry | +3 | +3 | 0 (unchanged) |
| M-score | 12/16 | 11/16 | −1 (degraded) |
| kac | −0.464 | −0.474 | −0.010 (improved) |
| **Pareto status** | — | — | **Trade-off** |

Even as a 2-pair flip, the reversal is an algebraic trade-off. But the question is moot for single-pair analysis — pair 27's orientation is not independently choosable.

---

## Test 3: The Meaning-Constraint Spectrum

The reader established two categories:

### Strong constraint (~21 pairs, "Clear")
Reversal is clearly inferior. The developmental logic is causally asymmetric, pattern-consistent, and supported by multiple independent textual signals.

**Jin/Ming Yi exemplifies this**: advance creates the conditions for injury (causally necessary); injury does not create the conditions for advance (merely hopeful). The Xugua's use of 必 (inevitability) marks the causal direction. The reversal is "narratively coherent but developmentally wrong within the Yijing's grammar."

### Moderate constraint (~11 pairs, "Suggestive")
Reversal is weaker but defensible. The pair is more contrastive than developmental, and alternative developmental logic exists.

**Jian/Gui Mei exemplifies this**: proper → improper is the Yijing's normative grammar, but improper → correction also has precedent (Meng, Bo/Fu). The Zagua's 終 (end/conclusion) for Gui Mei and the judgment's terminal tone ("nothing furthers") tip the balance to KW, but the margin is narrower.

### Zero pairs with no constraint
No pair where reversal is equally good or better.

---

## Test 4: Cross-Reference — Where Is Meaning Weakest?

The 11 "Suggestive" pairs cluster in specific algebraic categories:

| Property | Suggestive rate | Observation |
|---|---|---|
| S2-constrained | 5/10 (50%) | vs 6/22 (27%) for free pairs |
| Complement pairs | 3/4 (75%) | vs 8/28 (29%) for inversion pairs |
| Non-M-decisive | 7/16 (44%) | vs 4/16 (25%) for M-decisive |

**Meaning is weakest at complement pairs and S2-constrained pairs.** This makes sense:
- Complement pairs (B = NOT(A)) have polarity relationships rather than developmental sequences — more like co-equal opposites than condition → consequence.
- S2-constrained pairs have their orientation partially forced by structure, so the arranger had less freedom to optimize for meaning.

---

## Test 5: Does Algebraic Constraint Track Meaning Constraint?

The iter4 fragility map classified 27 free bits as:
- **KW-dominates** (11 bits): flipping degrades all 4 axes
- **Trade-off** (16 bits): flipping improves some axes, degrades others

If algebraic and meaning constraints tracked each other, we'd expect KW-dominates bits to be at "Clear" (meaning-strong) pairs and trade-off bits at "Suggestive" (meaning-weak) pairs.

| Fragility class | Clear | Suggestive | Suggestive rate |
|---|---|---|---|
| KW-dominates (11 bits → 13 pairs) | 7 | 6 | **46%** |
| Trade-off (16 bits → 19 pairs) | 14 | 5 | **26%** |

**The pattern is INVERTED.** KW-dominates bits are *more* likely to be at meaning-Suggestive pairs (46%) than trade-off bits (26%). Algebraic rigidity and meaning strength operate **independently** — or even inversely.

**Interpretation:** At pairs where the algebra is most constrained (all 4 axes degrade under flipping), meaning tends to be weaker. At pairs where the algebra allows trade-offs (flipping improves some axes), meaning tends to be stronger. This suggests:

1. The algebraic and semantic constraints are **complementary, not redundant.** Where one is strong, the other may be weak, and vice versa.
2. KW's position is held by **both constraints jointly** — algebraic rigidity covers some pairs, meaning covers others, and together they leave no pair unanchored.
3. The "vocabulary-over-grammar" finding from iter5 may be related: the algebraic axes protect distributional properties (vocabulary), while meaning protects developmental ordering (grammar). The arranger attended to both.

---

## Test 6: The S2/Meaning Interaction

Five of the 10 S2-constrained pairs are "Suggestive" — exactly 50%. For free pairs, only 27% are Suggestive. The higher Suggestive rate at S2-constrained positions is notable:

- At free positions, the arranger could choose the orientation. If meaning was the primary guide, we'd expect strong meaning signals at free positions — and we see them (73% Clear).
- At S2-constrained positions, the orientation is forced by structure. The arranger couldn't optimize for meaning here, so we'd expect weaker meaning alignment — but we still see alignment (100%, just with lower confidence).

This is consistent with the "middle reading": the arranger chose orientations based on meaning where free to do so, and the S2 constraint happened to produce meaning-compatible orientations at forced positions. The 50% Clear rate at S2-constrained pairs is the "accidental" meaning alignment at positions where structure, not meaning, determined the choice.

---

## Summary: What Round 4 Establishes

### 1. The meaning-constraint spectrum is real
Not all 32 alignments are equal in strength. ~21 pairs are overdetermined by meaning (reversal clearly inferior). ~11 pairs are meaning-preferred but not meaning-required (reversal defensible). Zero pairs are meaning-indifferent.

### 2. Pair 27 (Jian/Gui Mei) is S2-forced
The "weakest" pair in the investigation is structurally forced — its orientation isn't a free choice. The meaning-alignment at this pair is real but less informative than at free pairs.

### 3. Meaning disambiguates where algebra cannot
At pair 18 (Jin/Ming Yi), algebra sees a trade-off (flipping improves χ², degrades asym+kac). Meaning clearly favors KW's ordering. This is the cleanest example of meaning providing information that algebra does not.

### 4. Algebraic and meaning constraints are complementary
The inverted correlation between fragility class and meaning confidence shows they're not measuring the same thing. Together they cover the full orientation space — what one doesn't constrain, the other does.

### 5. The "middle reading" gains support
The arranger chose orientations based on meaning at free positions (73% Clear among free pairs) and accepted structural constraints at forced positions (50% Clear among S2-constrained). Both meaning and structure shaped the final sequence, with meaning operating where structure permitted.

---

## Updated Interpretation

The three readings from the alignment map, updated by the reversal test:

| Reading | Round 4 evidence |
|---|---|
| **Meaning is substance** | Supported at ~21 Clear pairs where reversal is clearly inferior. Weakened by the 11 Suggestive pairs and the inverted fragility correlation. |
| **Co-projection** | Most strongly supported. Algebraic and semantic constraints are complementary (not redundant), jointly anchoring all 32 bits. The specific orientation where both constraints are satisfied is KW. |
| **Post-hoc coherence** | Still possible for the 11 Suggestive pairs, where the meaning case relies more on the Xugua. Unlikely for the 21 Clear pairs where reversal is assessed as "clearly inferior" based on hexagram meanings alone. |
