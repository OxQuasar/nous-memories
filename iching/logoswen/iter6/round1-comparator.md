# Round 1: Comparator Analysis — M-Rule Exception Pairs

## Null Hypothesis

The reader's meaning-predicted ordering is independent of KW's actual ordering. Under this null, each pair has a 50% chance of alignment. For 3 pairs, the expected alignment is 1.5/3.

---

## Test 1: Direct Alignment

| Pair (1-idx) | Hexagrams | KW First | Reader Predicts | Aligned? |
|:---:|---|---|---|:---:|
| 4 | Shi (#7) / Bi (#8) | Shi | Shi | ✓ |
| 6 | Tai (#11) / Pi (#12) | Tai | Tai | ✓ |
| 10 | Lin (#19) / Guan (#20) | Lin | Lin | ✓ |

**Result: 3/3 hits.**

- Expected by chance: 1.5/3
- Binomial p-value (one-sided): 0.125
- **Verdict: Weak alignment.** 3/3 is directionally positive but n=3 is too small for statistical significance. The p=0.125 does not reject the null at any conventional threshold. The pattern is suggestive, not probative.

---

## Test 2: M-Component Correlation

The M-rule says: among M-decisive pairs (where L2 ≠ L5), KW places L2=yin first in 12/16 cases. The semantic analog: does the reader's "more receptive" member correspond to L2=yin?

| Pair | L2=yin Member | Reader's "Receptive" | Match? |
|:---:|---|---|:---:|
| 4 | Bi | Bi | ✓ |
| 6 | Pi | Pi | ✓ |
| 10 | Guan | Guan | ✓ |

**Result: 3/3 match.** In every assessed pair, the reader independently identified the L2=yin member as the more receptive/inward hexagram. The algebraic property (L2=yin) maps to a semantic property (receptive/inward) with perfect correspondence across these 3 cases.

**However**, this is a necessary condition for the M-rule to have semantic content, not a surprising finding. If the M-component *didn't* correspond to activity/receptivity, the entire M-rule-as-meaning hypothesis would collapse. The informative test is not whether L2=yin correlates with receptivity — it's what happens at the *exceptions*.

---

## Test 3: The Exception Test (the sharpest test)

This is the key test of the investigation's Round 1.

The M-rule default says: place L2=yin first ("receptive within"). If meaning simply tracked the M-rule, the meaning-predicted ordering at exception pairs would *disagree* with KW — because KW breaks the rule at these pairs. Instead:

| Pair | M-Rule Would Place First | KW Actually Places First | Reader Predicts First | Reader Agrees With Exception? |
|:---:|---|---|---|:---:|
| 4 | Bi (receptive) | **Shi** (active) | **Shi** | ✓ |
| 6 | Pi (withdrawn) | **Tai** (flourishing) | **Tai** | ✓ |
| 10 | Guan (contemplative) | **Lin** (approaching) | **Lin** | ✓ |

**Result: 3/3 exception pairs have meaning-level justification for the override.**

In all three cases:
- The M-rule would place the more receptive member first
- KW instead places the more active member first
- The reader, working from meaning alone, agrees with KW's ordering (not the M-rule default)
- The reader rates confidence as "Clear" in all three cases

The reader's rationale in each case:
- **Shi → Bi**: Mobilization precedes union. The Xugua explicitly states multitudes necessitate bonds. Active gathering before receptive bonding.
- **Tai → Pi**: Flourishing precedes decline. Cosmological law — fullness transforms to its opposite. The generative condition is prior.
- **Lin → Guan**: Approach precedes contemplation. The Xugua states that approaching with greatness produces something worth contemplating.

### What This Means

At these 3 pairs, the algebraic M-rule and the semantic ordering principle **pull in opposite directions**:
- The M-rule says: receptive first (L2=yin first)
- The meaning says: active first (the active member naturally precedes)
- KW sides with meaning

This is the first evidence that KW's orientation encodes semantic information that cannot be reduced to the M-component alone. The M-rule captures 12/16 cases — but the 3 assessed exceptions are not random noise or structural artifacts. They are semantically motivated overrides.

### Statistical Caveat

3/3 on a binary test has p = 0.125 (one-sided binomial). This is not statistically significant by conventional standards. The test becomes meaningful only cumulatively — across more pairs and more rounds.

However, the test is asymmetric in informativeness:
- A result of 0/3 or 1/3 would have strongly supported "override is purely structural"
- A result of 3/3 is consistent with "meaning justifies the override" but doesn't prove it
- The 4th M-rule exception (Pair 21: Sun/Yi, #41/#42) was not assessed this round and represents a natural next test point

---

## Test 4: Pair Type Properties

All three assessed pairs are **inversion pairs** (B = reverse(A)):

| Pair | Type | Orbit | Hamming Weight |
|:---:|---|---|:---:|
| 4 | Inversion | (0,1,0) | A=1, B=1 |
| 6 | Inversion | (1,1,1) | A=3, B=3 |
| 10 | Inversion | (1,1,0) | A=2, B=2 |

For inversion pairs, both members always have the same Hamming weight (Theorem 8 from synthesis). This means weight-based classifiers cannot distinguish the ordering — it must come from something else. The reader's meaning-based ordering provides a candidate for that "something else."

All three are also in the upper canon (pairs 1-15), where the canon asymmetry signal (+3) is concentrated.

---

## Test 5: Activity/Receptivity Pattern

The reader consistently identified the same pattern across all three pairs:

| Dimension | First Member | Second Member |
|---|---|---|
| Activity | More active, outward | More receptive, inward |
| Xugua logic | Condition / cause | Consequence / result |
| Temporal | Initiating phase | Responding phase |
| Traditional | The "doing" hexagram | The "receiving" hexagram |

In KW's ordering, the active member comes first in all 3 exception pairs. This is the *opposite* of the M-rule default (receptive first). The reader's analysis suggests the M-rule's semantic analog isn't "receptive first" but rather "the M-rule captures a *different* meaning principle — one that happens to anti-correlate with the activity ordering at these specific pairs."

### A Refinement

The M-rule (L2=yin first) can be read as "the inner ruler is receptive" — but this is about the *internal structure* of the first hexagram, not about which hexagram is more receptive overall. A hexagram can have a receptive inner ruler (L2=yin) while being the more *active* member of its pair. The 12/16 M-rule hits may reflect an orthogonal principle from the one the reader is tracking.

At the exception pairs, two principles conflict:
1. **M-component**: prefer L2=yin first (inner receptivity)
2. **Semantic ordering**: prefer the active/initiating member first

Where they conflict, KW follows the semantic ordering. This is the finding.

---

## Summary Statistics

| Test | Result | Expected by Chance | p-value | Verdict |
|---|---|---|---|---|
| Direct alignment | 3/3 | 1.5/3 | 0.125 | Weak alignment |
| M-component = receptive | 3/3 | ? | — | Necessary condition met |
| Exception justification | 3/3 | — | — | All exceptions meaning-justified |
| Activity pattern | Consistent | — | — | Active-first in all 3 |

**Overall assessment: Suggestive positive signal, not yet significant.**

The 3/3 exception justification is the strongest finding. It cannot be evaluated by binomial test alone because the question isn't "are these aligned by chance?" but "do these specific overrides have specific semantic reasons?" The reader provided detailed, text-grounded rationales drawing on the Xugua, Zagua, and commentarial tradition. The rationales are mutually consistent (all follow the active→receptive pattern) and independently sourced.

---

## What Remains

1. **The 4th exception**: Pair 21 (Sun #41 / Yi #42, Decrease/Increase). This is the remaining M-rule exception not yet assessed. Does it also have semantic justification?

2. **The M-rule conforming pairs**: Do the 12 M-rule-conforming pairs also show meaning-predicted = KW ordering? If the active-first principle is universal, it should predict the correct ordering at conforming pairs too (where the M-rule and meaning align).

3. **Complement pairs**: The 4 complement pairs (Qian/Kun, Kan/Li, Xian/Heng, Ji Ji/Wei Ji) have different pairing logic. Does meaning predict their ordering too?

4. **The lower canon**: All 3 assessed pairs are in the upper canon. The orientation signals are concentrated in the lower canon (pairs 16-32). Does the active-first principle hold there too, or does it attenuate?

5. **Sample size**: n=3 is insufficient. Extending to all 16 M-decisive pairs or all 32 pairs would make the binomial test meaningful.

---

## Falsifiability Check

The null hypothesis (meaning is independent of ordering) was **not rejected** this round. p=0.125 is not significant. The exception test result (3/3) is striking but not statistically definitive.

**What would falsify the meaning-alignment hypothesis in future rounds:**
- Overall alignment ≤ 50% across all 32 pairs
- The 4th exception (Sun/Yi) having no semantic justification
- M-rule conforming pairs showing alignment no better than chance
- The active-first pattern failing in the lower canon

The investigation remains in an informative state: positive signal, insufficient data.
