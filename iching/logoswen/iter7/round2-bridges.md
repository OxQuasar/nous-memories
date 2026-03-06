# Round 2: The 9 Preserving Bridges and the Continuity Gradient

## Overview

Round 1 found that 9 of 31 bridges preserve one trigram — 5 lower, 4 upper. This round maps their meaning, tests their statistical significance, and examines the full continuity gradient. The central algebraic finding: **all 9 preserving bridges have kernel dressing = id** (no palindromic component in the bridge XOR mask). This is the first structural link between trigram preservation and the mirror-pair algebra.

---

## Task A: The 9 Preserving Bridges — Meaning Characterization

### Full transition table

| B# | Exit (Lo/Up) → Entry (Lo/Up) | Preserved | Changed |
|:--:|------------------------------|-----------|---------|
| B3 | Water☵/Heaven☰ → Water☵/Earth☷ | **Lower: Water☵** | Upper: Heaven☰ → Earth☷ |
| B6 | Earth☷/Heaven☰ → Fire☲/Heaven☰ | **Upper: Heaven☰** | Lower: Earth☷ → Fire☲ |
| B11 | Fire☲/Mountain☶ → Earth☷/Mountain☶ | **Upper: Mountain☶** | Lower: Fire☲ → Earth☷ |
| B12 | Thunder☳/Earth☷ → Thunder☳/Heaven☰ | **Lower: Thunder☳** | Upper: Earth☷ → Heaven☰ |
| B13 | Heaven☰/Mountain☶ → Thunder☳/Mountain☶ | **Upper: Mountain☶** | Lower: Heaven☰ → Thunder☳ |
| B18 | Fire☲/Earth☷ → Fire☲/Wind☴ | **Lower: Fire☲** | Upper: Earth☷ → Wind☴ |
| B26 | Mountain☶/Mountain☶ → Mountain☶/Wind☴ | **Lower: Mountain☶** | Upper: Mountain☶ → Wind☴ |
| B27 | Lake☱/Thunder☳ → Fire☲/Thunder☳ | **Upper: Thunder☳** | Lower: Lake☱ → Fire☲ |
| B30 | Lake☱/Water☵ → Lake☱/Wind☴ | **Lower: Lake☱** | Upper: Water☵ → Wind☴ |

### Preserved trigram frequency

| Trigram | As lower | As upper | Total |
|---------|:--------:|:--------:|:-----:|
| Mountain ☶ | 1 | 2 | **3** |
| Thunder ☳ | 1 | 1 | 2 |
| Water ☵ | 1 | 0 | 1 |
| Fire ☲ | 1 | 0 | 1 |
| Lake ☱ | 1 | 0 | 1 |
| Heaven ☰ | 0 | 1 | 1 |
| Earth ☷ | 0 | 0 | 0 |
| Wind ☴ | 0 | 0 | 0 |

Mountain appears 3 times — statistically notable (p = 0.04 vs random orderings). Earth and Wind are never preserved.

### Meaning characterization of each bridge

**B3: Song (#6) → Shi (#7) — Lower Water persists**
*Pair 3 (Xu/Song) → Pair 4 (Shi/Bi)*

Water ☵ (the Abysmal, danger, depth) persists as the inner condition. The outer context transforms from Heaven ☰ (the Creative, vast force) to Earth ☷ (the Receptive, yielding openness).

The narrative: after Conflict (Song), the inner condition of peril and depth remains, but the outer context shifts from the confrontational force of Heaven to the receptive yielding of Earth. The Army (Shi) arises when danger is met not with more force but with organized response on yielding ground. Inner depth endures; outer strategy transforms.

The Xugua says: "Contention necessarily involves the rising up of the masses; hence there follows the hexagram of the Army." The logic is consequential: conflict produces mobilization. The trigram story adds a mechanism — the *inner* condition (danger, depth of engagement) persists while the *outer* framework transforms from adversarial to collective. **Confidence: Clear.** The Xugua's causal logic aligns with the trigram continuity.

**B6: Pi (#12) → Tong Ren (#13) — Upper Heaven persists**
*Pair 6 (Tai/Pi) → Pair 7 (Tong Ren/Da You)*

Heaven ☰ (the Creative, the vast, the public sphere) persists as the outer context. The inner condition transforms from Earth ☷ (pure receptivity, stagnation) to Fire ☲ (clarity, discernment).

The narrative: after Standstill (Pi), the outer world of Heaven remains — the large-scale context hasn't changed. What changes is the inner response: from passive receptivity (Earth) to active clarity (Fire). Tong Ren (Fellowship of Men) arises when a person brings inner light to an unchanged larger situation. The world stays the same; the person within it wakes up.

The Xugua says: "Things cannot forever be at a standstill; hence there follows Fellowship with Men." The trigram story names the mechanism: the *outer* context is unchanged, but a new *inner* quality (Fire/clarity) enters. **Confidence: Clear.** The transition from stagnation to fellowship through inner awakening is a well-attested I Ching teaching.

**B11: Bi/Grace (#22) → Bo (#23) — Upper Mountain persists**
*Pair 11 (Shi He/Bi) → Pair 12 (Bo/Fu)*

Mountain ☶ (Keeping Still, restraint, limit) persists as the outer context. The inner condition transforms from Fire ☲ (clarity, adornment) to Earth ☷ (pure receptivity, dissolution).

The narrative: after Grace (Bi), the outer condition of stillness and boundary remains, but the inner vitality (Fire) drains to pure receptivity (Earth). Splitting Apart (Bo) occurs when outer form persists but inner substance is exhausted. The mountain is still there, but what lived within it has yielded.

The Xugua says: "Grace is form. When form is carried to its extreme, it becomes exhausted; hence there follows Splitting Apart." The trigram reading adds: the outer *structure* (Mountain) persists — the form — while the inner *life* (Fire → Earth) empties. **Confidence: Clear.** This is one of the most precise meaning-trigram correspondences.

**B12: Fu (#24) → Wu Wang (#25) — Lower Thunder persists**
*Pair 12 (Bo/Fu) → Pair 13 (Wu Wang/Da Chu)*

Thunder ☳ (the Arousing, movement, initiative, the first stirring) persists as the inner condition. The outer context transforms from Earth ☷ (receptivity, the ground of return) to Heaven ☰ (the Creative, the full cosmic context).

The narrative: after Return (Fu), the inner stirring of new movement persists — the impulse that arose as a single yang line at the bottom. What changes is the outer context: from the quiet ground of Earth to the vast arena of Heaven. Innocence (Wu Wang) arises when the initial impulse meets the full creative field without distortion. The spark endures; the stage expands.

The Xugua says: "Return means turning back. One who turns back will not err; hence there follows Innocence." The trigram story: the inner *impulse* (Thunder) carries from Return into Innocence; the outer *context* expands from Earth to Heaven. **Confidence: Clear.** The developmental logic from the first stirring (Return) to its authentic expression in the world (Innocence) is traditional.

**B13: Da Chu (#26) → Yi/Nourishment (#27) — Upper Mountain persists**
*Pair 13 (Wu Wang/Da Chu) → Pair 14 (Yi/Da Guo)*

Mountain ☶ (Keeping Still, containment, accumulation) persists as the outer context. The inner condition transforms from Heaven ☰ (creative force) to Thunder ☳ (arousing, the initiating impulse).

The narrative: after Great Taming (Da Chu), the outer condition of containment (Mountain) remains — what has been accumulated still stands. But the inner energy shifts from the full creative power of Heaven to the specific, focused impulse of Thunder. Nourishment (Yi) arises when accumulated resources meet directed action. The container persists; the energy within it becomes more specific and personal.

The Xugua says: "Only after great accumulation can nourishing take place; hence there follows the hexagram of Nourishment." The trigram story: the *outer vessel* (Mountain/containment) persists from accumulation to nourishment, while the *inner quality* shifts from vast creative potential to directed first-impulse. **Confidence: Suggestive.** The Xugua logic is clear; the trigram correspondence is natural but not as crisp as B11 or B12.

**B18: Ming Yi (#36) → Jia Ren (#37) — Lower Fire persists**
*Pair 18 (Jin/Ming Yi) → Pair 19 (Jia Ren/Kui)*

Fire ☲ (Clinging, clarity, discernment, light) persists as the inner condition. The outer context transforms from Earth ☷ (suppression, darkness, the flat ground that buries light) to Wind ☴ (gentle penetrating influence, the household order).

The narrative: after Darkening of the Light (Ming Yi), inner clarity endures despite external suppression. The outer condition shifts from Earth (oppressive flatness) to Wind (gentle ordering). The Family (Jia Ren) arises when the same inner discernment that survived suppression now meets a structure where it can work — the gentle, penetrating order of Wind. Same capacity for seeing; new context for acting.

The sage gave this as a paradigm case. The Xugua says: "One who is wounded in what is without will inevitably turn to the household; hence there follows the Family." The trigram story: *inner clarity* (Fire) carries from exile into the home; the *outer condition* transforms from hostile ground to receptive order. **Confidence: Clear.** This is the strongest meaning-trigram alignment among all 9.

**B26: Gen (#52) → Jian/Development (#53) — Lower Mountain persists**
*Pair 26 (Zhen/Gen) → Pair 27 (Jian/Gui Mei)*

Mountain ☶ (Keeping Still, inner restraint, rootedness) persists as the inner condition. The outer context transforms from Mountain ☶ (pure keeping still — doubled Mountain) to Wind ☴ (gradual development, gentle penetration).

The narrative: after Keeping Still (Gen), inner stillness endures — the meditative foundation persists. What changes is the outer context: from the doubled, absolute stillness of Mountain/Mountain to the gradual unfoldment of Wind. Development (Jian) arises when inner rootedness meets outward gentle influence. Same inner state; transformed expression.

The sage gave this as the second paradigm case. The Xugua says: "Things cannot forever keep still; hence there follows Development." The trigram story: the inner *stillness* (Mountain) of Gen carries into the developmental phase; only the outer expression transforms from static to gradual. **Confidence: Clear.** Note this is also the lowest total displacement of any bridge (only 1 bit changes).

**B27: Gui Mei (#54) → Feng (#55) — Upper Thunder persists**
*Pair 27 (Jian/Gui Mei) → Pair 28 (Feng/Lü)*

Thunder ☳ (the Arousing, movement, decisive action) persists as the outer context. The inner condition transforms from Lake ☱ (joy, openness, the youngest daughter) to Fire ☲ (clarity, illumination, the middle daughter).

The narrative: after the Marrying Maiden (Gui Mei), the outer condition of arousal and decisive action persists — the event horizon of marriage/commitment remains. What changes is the inner quality: from joy/openness (Lake) to clarity/illumination (Fire). Abundance (Feng) arises when the same outer movement meets inner clarity instead of youthful joy. The thunderstorm continues; what changes is the light within it.

The Xugua says: "One who achieves the girl's home becomes great; hence there follows Abundance." The trigram correspondence: the outer *arousal/action* (Thunder) persists from hasty commitment into full abundance, while inner quality deepens from joy to clarity. **Confidence: Suggestive.** The correspondence is natural but less crisp than B18 or B26.

**B30: Jie (#60) → Zhong Fu (#61) — Lower Lake persists**
*Pair 30 (Huan/Jie) → Pair 31 (Zhong Fu/Xiao Guo)*

Lake ☱ (the Joyous, openness, inner receptivity, communication) persists as the inner condition. The outer context transforms from Water ☵ (danger, the formless, the abysmal) to Wind ☴ (gentle penetration, subtle influence).

The narrative: after Limitation (Jie), inner joy and openness endure — the capacity for delight persists despite constraint. The outer condition shifts from Water (dangerous formlessness) to Wind (gentle ordering influence). Inner Truth (Zhong Fu) arises when inner joy meets outward gentleness instead of outward danger. Same inner openness; transformed outer field.

The Xugua says: "Regulation and measure bring trust; hence there follows Inner Truth." The trigram story: inner *joy/openness* (Lake) carries from limitation into truth, while the outer condition gentles from danger to Wind. **Confidence: Clear.** The developmental arc from limitation to trust through persistent inner openness is well-established.

Note: this bridge also preserves both nuclear trigrams (Thunder/Mountain), creating a triple continuity — primary lower, nuclear lower, and nuclear upper all persist. B30 is the only bridge in the sequence with this property.

### Nuclear trigram preservation at the 9 bridges

| B# | Primary preserved | Nuclear lower | Nuclear upper | Continuity depth |
|:--:|:-:|:-:|:-:|:-:|
| B3 | lower | changes | changes | 1 layer |
| B6 | upper | changes | changes | 1 layer |
| B11 | upper | changes | changes | 1 layer |
| B12 | lower | changes | changes | 1 layer |
| B13 | upper | changes | changes | 1 layer |
| B18 | lower | **preserved** (Water) | changes | 2 layers |
| B26 | lower | **preserved** (Water) | changes | 2 layers |
| B27 | upper | changes | changes | 1 layer |
| B30 | lower | **preserved** (Thunder) | **preserved** (Mountain) | **3 layers** |

Three tiers of continuity depth emerge:
- **Tier 1** (6 bridges): Only primary trigram preserved. Nuclear trigrams change.
- **Tier 2** (2 bridges, B18 and B26): Primary lower AND nuclear lower preserved. These share an identical nuclear transition pattern: Water persists as nuclear lower, while nuclear upper changes Thunder → Fire. The same hidden dynamic underlies both Ming Yi → Jia Ren and Gen → Jian/Development.
- **Tier 3** (1 bridge, B30): Primary lower AND both nuclear trigrams preserved. Only a single bit (L6) changes. This is the maximal continuity point in the entire King Wen sequence — the transition from Limitation to Inner Truth maintains inner joy (Lake), hidden impulse (Thunder), and hidden restraint (Mountain) simultaneously.

### Summary: the developmental grammar at preserving bridges

| Preserved | Narrative pattern | Count |
|-----------|------------------|:-----:|
| Lower (inner) persists | "Inner state endures while outer context transforms" | 5 |
| Upper (outer) persists | "Outer context endures while inner state transforms" | 4 |

**The 5 lower-preserved bridges** tell stories of inner continuity: the same danger (B3), impulse (B12), clarity (B18), stillness (B26), or joy (B30) persists across an external transformation.

**The 4 upper-preserved bridges** tell stories of contextual stability: the same Heaven (B6), Mountain (B11, B13), or Thunder (B27) persists while the inner quality transforms.

**Xugua correspondence: 8 of 9 bridges show clear or suggestive alignment** between the Xugua's stated pair-to-pair logic and the trigram preservation narrative. The strongest alignments are at B11 (form persists while substance drains → Splitting Apart), B12 (impulse persists while context expands → Innocence), B18 (clarity persists while ground transforms → Family), and B26 (stillness persists while expression unfolds → Development).

**Confidence assessment:**
- Clear alignment (Xugua logic matches trigram narrative closely): B3, B6, B11, B12, B18, B26, B30 — **7 of 9**
- Suggestive alignment: B13, B27 — **2 of 9**
- No contradictions.

---

## Task B: The Continuity Gradient

### All 31 bridges sorted by total trigram displacement

| Total | Count | Bridges |
|:-----:|:-----:|---------|
| 1 | 2 | B26 (Gen→Jian), B30 (Jie→Zhong Fu) |
| 2 | 8 | B3, B6, B11, B13, B18, B27, B1, B8 |
| 3 | 13 | B3(=3), B12(=3), B9, B10, B14, B15, B16, B20, B22, B23, B24, B28, B29, B31 |
| 4 | 7 | B2, B4, B5, B7, B17, B21, B25 |
| 5 | 0 | (none) |
| 6 | 1 | B19 (Kui→Jian/Obst.) |

Note: B3 and B12 have total displacement 3 (not 2) — they preserve one trigram but the other trigram changes by 3 bits (full complement). Correcting from above:

### Precise gradient table

| Disp. | Min | Bridges | Character |
|:-----:|:---:|---------|-----------|
| 1 | 0 | B26, B30 | **Preserving — minimal change** |
| 2 | 0 | B6, B11, B13, B18, B27 | **Preserving — moderate change** |
| 2 | 1 | B1, B8, B14 | Near-preserving (both trigrams change by 1 bit) |
| 3 | 0 | B3, B12 | **Preserving — one trigram fully complements** |
| 3 | 1 | B9, B10, B15, B16, B20, B22, B23, B24, B28, B29, B31 | Near-preserving (one trigram 1-bit, other 2-bit) |
| 4 | 1 | B4, B5, B17, B25 | Moderate displacement |
| 4 | 2 | B2, B7, B21 | Symmetric displacement (2+2) |
| 6 | 3 | B19 | **Maximal displacement** (both trigrams fully complement) |

### Key observations

1. **No gap at min_dist = 0 → 1.** The gradient is smooth — preserving bridges (min=0) shade into near-preserving bridges (min=1) without a discontinuity. 9 bridges have min=0, 18 have min=1, 3 have min=2, 1 has min=3.

2. **The two minimally-displaced bridges** (B26 and B30, total=1) are both lower-preserving. They change only a single bit in the upper trigram. B26 changes only L5; B30 changes only L6. These are the moments of greatest continuity in the entire path.

3. **B19 (Kui→Jian/Obst.)** is the sole maximal displacement (total=6, both trigrams fully complement). This is the bridge from pair 19 (Jia Ren/Kui) to pair 20 (Jian/Xie). Lake/Fire → Mountain/Water — complete inversion. The Family/Opposition transition jumps to Obstruction/Deliverance with maximum discontinuity.

4. **Mean total displacement:** 2.935. Against random pair orderings, this is at the 28th percentile (not significant). Against random orientations with same pair ordering, the mean is exactly as expected (0.5764 percentile). The *average* continuity is unremarkable.

5. **The absence of total_dist = 5.** Every total displacement from 1 to 4 occurs, then 5 is skipped. This is a minor structural constraint (to get total=5, you need one trigram at distance 2 and one at distance 3, or distance 1 + distance 4 which is impossible since max trigram Hamming is 3).

### Gradient distribution

```
total_dist=1:  ██                         (2)
total_dist=2:  ████████                   (8)
total_dist=3:  █████████████              (13) ← mode
total_dist=4:  ███████                    (7)
total_dist=6:  █                          (1)
```

The distribution peaks at total_dist=3. The 9 preserving bridges (total ≤ 3 with min=0) occupy the left tail of this distribution.

---

## Task C: Statistical Significance

### Test 1: Random pair orderings (100,000 trials)

Preserve pairing and internal orientation, shuffle pair order.

| Metric | KW | Null mean ± σ | p-value |
|--------|:--:|:-------------:|:-------:|
| Preserving bridges (min=0) | 9 | 6.87 ± 2.28 | 0.231 |
| Mean total displacement | 2.935 | 3.073 ± 0.204 | 0.277 |

**KW's 9 preserving bridges are not significant against random pair orderings.** The count of 9 falls well within the null distribution (range 0–17, KW at 77th percentile).

### Test 2: Random orientations, same pair ordering (100,000 trials)

Preserve pair order, randomly flip orientation (S2 pairs constrained).

| Metric | KW | Null mean ± σ | p-value |
|--------|:--:|:-------------:|:-------:|
| Preserving bridges (min=0) | 9 | 9.00 ± 1.87 | 0.606 |
| Mean total displacement | 2.935 | 2.935 ± 0.157 | 0.576 |

**KW's orientation produces exactly the expected number of preserving bridges given its pair ordering.** The null mean is 9.00, matching KW's 9 exactly. The orientation bits carry no trigram-continuity signal.

### Test 3: Which-trigram distribution

| Trigram | KW count | Null mean | p(≥KW) |
|---------|:--------:|:---------:|:------:|
| Mountain ☶ | 3 | 0.93 | **0.044** |
| Thunder ☳ | 2 | 0.75 | 0.155 |
| Fire ☲ | 1 | 0.85 | 0.624 |
| Water ☵ | 1 | 0.97 | 0.671 |
| Lake ☱ | 1 | 0.85 | 0.621 |
| Heaven ☰ | 1 | 0.95 | 0.667 |
| Earth ☷ | 0 | 0.96 | 1.000 |
| Wind ☴ | 0 | 0.59 | 1.000 |

**Mountain appears 3 times, significant at p = 0.044.** Mountain is the trigram of Keeping Still — restraint, boundary, limit. Its overrepresentation at preserving bridges suggests that the quality of *containment* preferentially persists across pair boundaries. (But note: with 8 trigrams tested, multiple comparison correction would render this borderline.)

Earth and Wind never appear. Their absence is within null expectations.

### Test 4: Position of preserving bridges

Positions: [3, 6, 11, 12, 13, 18, 26, 27, 30]

- Upper canon (B1–B15): 5 bridges
- Lower canon (B16–B31): 4 bridges
- Balanced between canons.

Consecutive clustering: B11-B12-B13 form a three-bridge streak (pairs 11–14). This is the Bo/Fu/Wu Wang/Da Chu/Yi region — a sequence of dissolution, return, innocence, accumulation, and nourishment. Three consecutive preserving bridges means four consecutive pair transitions each maintain partial trigram continuity: a sustained developmental arc.

Gaps: [3, 5, 1, 1, 5, 8, 1, 3]. Mean gap 3.4. The largest gap (8, between B18 and B26) spans the middle of the lower canon.

### Statistical summary

The *count* of 9 preserving bridges is not significant — it's what random pair orderings produce. The *which-trigram* distribution shows Mountain is overrepresented (p = 0.044). The *positions* show one notable cluster (B11-B12-B13). The *meaning* characterization (Task A) is where the signal lives: 7/9 show clear Xugua correspondence, and the trigram narratives are semantically coherent. The signal is in the *content* of the 9, not their *quantity*.

---

## Task D: Bridge Trigrams × Algebraic Properties

### The central finding: all 9 preserving bridges have kernel = id

| Bridge | Kernel dressing | Orbit delta | Exit orbit → Entry orbit |
|:------:|:-:|---|---|
| B3 | **id** | L6+L5+L4 | OI → M |
| B6 | **id** | L1+L3 | OMI → M |
| B11 | **id** | L1+L3 | I → O |
| B12 | **id** | L6+L5+L4 | O → MI |
| B13 | **id** | L2+L3 | MI → id |
| B18 | **id** | L6+L5 | OI → MI |
| B26 | **id** | L5 | OI → OMI |
| B27 | **id** | L2+L3 | OMI → O |
| B30 | **id** | L6 | O → id |

**All 9 preserving bridges have kernel dressing = id** (the XOR mask between exit and entry hexagrams has zero palindromic component — no mirror pair is simultaneously flipped on both lines).

### What this means

The kernel dressing of a bridge XOR mask measures how much of the bridge transition acts on the mirror-pair structure. When kernel = id, the bridge changes *only asymmetric bits* — it never flips both members of any mirror pair. Since mirror pairs straddle the trigram boundary (one line in lower, one in upper), a non-id kernel necessarily changes bits in *both* trigrams. Therefore:

**A bridge can preserve a trigram only if its kernel dressing is id.**

This is almost a theorem. The kernel is the palindromic (symmetric) part of the XOR mask. Each kernel generator flips one bit from lower and one from upper trigram. If any kernel generator is active, both trigrams necessarily change. The only way to preserve one trigram is to have all changes concentrated on one side of the boundary — which requires kernel = id.

Proof sketch: The kernel generators are O (L1↔L6), M (L2↔L5), I (L3↔L4). Each flips one bit in lower (L1, L2, or L3) and one in upper (L4, L5, or L6). If any kernel generator is active, at least one bit changes in each trigram. Therefore kernel ≠ id → both trigrams change. Contrapositive: trigram preservation → kernel = id. ∎

### Cross-tabulation: kernel dressing × preservation

| Kernel | Preserving | Non-preserving | Total |
|--------|:----------:|:--------------:|:-----:|
| id | **9** | 6 | 15 |
| O | 0 | 9 | 9 |
| M | 0 | 2 | 2 |
| I | 0 | 4 | 4 |
| OMI | 0 | 1 | 1 |
| **Total** | **9** | **22** | **31** |

15 bridges have kernel = id. Of these 15, 9 (60%) preserve a trigram and 6 (40%) don't. Among the 6 non-preserving id-kernel bridges, all have min_dist = 1 (near-preserving). So: **kernel = id is necessary for preservation and near-preservation.**

The 16 bridges with kernel ≠ id all have min_dist ≥ 1, confirming the theorem.

### Hamming distance × preservation

| Hamming | Preserving | Non-preserving |
|:-------:|:----------:|:--------------:|
| 1 | 2 | 0 |
| 2 | 5 | 3 |
| 3 | 2 | 11 |
| 4 | 0 | 7 |
| 6 | 0 | 1 |

Preserving bridges have lower total Hamming distance (mean 2.1 vs 3.3 for non-preserving). This is tautological: preserving one trigram limits how many bits can change.

### Orbit transitions at preserving bridges

No single orbit transition pattern characterizes preserving bridges — they connect diverse orbits. But all orbit transitions at preserving bridges are *cross-orbit* (entry orbit ≠ exit orbit). This is consistent with kernel = id: the bridge's asymmetric bits change the orbit identity.

### Pair kernel correlations at preserving bridges

| Bridge | Exit pair kernel | Entry pair kernel | Match? |
|:------:|:----------------:|:-----------------:|:------:|
| B3 | OI | M | |
| B6 | OMI | M | |
| B11 | I | O | |
| B12 | O | MI | |
| B13 | MI | OMI | |
| B18 | OI | MI | |
| B26 | OI | OMI | |
| B27 | OMI | O | |
| B30 | O | OMI | |

No pair kernel matches at preserving bridges (0/9). The pairs on either side always have different generators. This is expected: preserving bridges connect different orbits, and pair kernel = orbit generator.

---

## Task E: Bridge Trigrams × Meaning Confidence

### Cross-tabulation: preservation × meaning confidence

Adjacent pairs' developmental priority confidence:

| | Clear | Suggestive | Clear rate |
|---|:---:|:---:|:---:|
| Preserving bridge pairs (18 adj.) | 10 | 8 | **56%** |
| Non-preserving bridge pairs (44 adj.) | 30 | 14 | **68%** |

Preserving bridges are *more likely* to be adjacent to Suggestive pairs (44% Suggestive) than non-preserving bridges (32% Suggestive). This is the opposite of what one might expect if trigram preservation helped meaning transparency.

### Cross-tabulation: preservation × fragility class

| | KW-dominates | Trade-off | S2 |
|---|:---:|:---:|:---:|
| Preserving bridge adj. pairs (18) | 2 (11%) | 12 (**67%**) | 4 (22%) |
| Non-preserving bridge adj. pairs (44) | 18 (41%) | 18 (41%) | 8 (18%) |

**Preserving bridges cluster near algebraically flexible (trade-off) pairs.** 67% of pairs adjacent to preserving bridges are in the trade-off class, vs 41% for non-preserving bridges. This is the complementary coverage pattern from iter6, now localized: trigram preservation appears where algebra allows latitude.

### Individual preserving bridge profiles

| B# | Exit pair conf. → Entry pair conf. | Exit fragility → Entry fragility |
|:--:|:-:|:-:|
| B3 | Sugg → Clear | KW-dom → trade-off |
| B6 | Clear → Clear | trade-off → trade-off |
| B11 | Sugg → Clear | trade-off → trade-off |
| B12 | Clear → Sugg | trade-off → trade-off |
| B13 | Sugg → Sugg | trade-off → S2 |
| B18 | Clear → Clear | trade-off → trade-off |
| B26 | Clear → Sugg | KW-dom → S2 |
| B27 | Sugg → Clear | S2 → trade-off |
| B30 | Clear → Sugg | trade-off → S2 |

5 of 9 preserving bridges connect a Clear pair to a Suggestive pair (or vice versa). This alternation (C→S or S→C) at 5/9 vs the base rate of ~50% is not significant, but the pattern is notable: preserving bridges tend to sit at transitions between confidence levels.

---

## The 22 Non-Preserving Bridges

### Trigram Hamming distance distribution

| (lo_dist, up_dist) | Count |
|:---:|:---:|
| (1, 1) | 3 |
| (1, 2) | 8 |
| (1, 3) | 1 |
| (2, 1) | 3 |
| (2, 2) | 3 |
| (3, 1) | 3 |
| (3, 3) | 1 |

The most common pattern is (1, 2): one trigram changes by 1 bit, the other by 2 bits. Pure minimal change (1, 1) occurs 3 times. Full complement (3, 3) occurs once (B19).

### Line change frequency at non-preserving bridges

| Line | Frequency (/22) |
|------|:---:|
| L1 | 15 |
| L2 | 10 |
| L3 | 11 |
| L4 | 12 |
| L5 | 11 |
| L6 | 14 |

The outer lines (L1, L6) change more frequently than inner lines at non-preserving bridges. This is consistent with the O-generator being the most common kernel component (9/16 non-id bridges include O).

---

## Summary

### Three findings

**1. The kernel = id theorem.** All 9 preserving bridges have kernel dressing = id. This is algebraically forced: any kernel generator flips one bit in each trigram, so kernel ≠ id → both trigrams change. The 15 id-kernel bridges are the only candidates for trigram preservation; 9 of 15 achieve it, the other 6 are near-preserving (min_dist = 1).

This connects the trigram frame to the mirror-pair frame at bridges: **trigram preservation is the trigram-frame name for the absence of palindromic components in the bridge transition.**

**2. The count of 9 is not significant; the content is.** Random pair orderings produce ~7 preserving bridges on average; KW's 9 is within the null distribution (p = 0.23). The orientation bits don't add trigram continuity beyond what the pair ordering determines (null mean exactly matches). What's significant is: (a) Mountain is overrepresented at p = 0.044; (b) the meaning characterization shows 7/9 clear Xugua alignment; (c) the B11-B12-B13 cluster creates a sustained developmental arc.

**3. Preserving bridges cluster at algebraically flexible positions.** 67% of pairs adjacent to preserving bridges are in the trade-off fragility class (vs 41% for non-preserving). This extends the iter6 complementary coverage pattern: where algebra allows latitude, trigram continuity appears as an additional structural feature. The trigram-level narrative carries the developmental logic that algebra alone can't resolve.

### The picture so far

The two decompositions (mirror-pair and trigram) interact at bridges through the kernel dressing. Bridges with kernel = id (no palindromic component) can preserve a trigram — and 9 of 15 such bridges do. These 9 moments of trigram continuity carry semantically coherent developmental narratives, and they cluster at positions where the algebraic constraint is weakest (trade-off pairs). This is consistent with co-projection: algebra and meaning are not independent, but they are not derivable from each other either. The trigram continuity is a third visible face of the underlying structure.

### Questions for Round 3

1. **The 6 id-kernel non-preserving bridges.** They are near-preserving (min_dist = 1). What prevents them from achieving full preservation? Is there a secondary constraint that selects which 9 of the 15 id-kernel bridges actually preserve?

2. **Mountain's overrepresentation.** Mountain appears 3× (p = 0.044). Is this connected to Mountain's role in the developmental grammar (the youngest son, the boundary, the place of stillness)?

3. **The B11-B12-B13 cluster.** Three consecutive preserving bridges. What happens in this region of the sequence at the algebraic level? Is this cluster structurally forced or contingent?

4. **The full cross-tabulation.** Kernel dressing × trigram preservation × meaning confidence × fragility class. Is there a four-way pattern that explains more variance than any two-way cross?

5. **The nuclear trigram at preserving bridges.** Round 1 showed O is invisible to nuclear trigrams and B30 preserves both nuclear trigrams. What about the other 8 preserving bridges? Does nuclear trigram behavior at preserving bridges reveal additional structure?

---

## Data Files

| File | Contents |
|------|----------|
| `bridge_trigrams.py` | Complete computation script for all tasks |
| `round2-bridges.md` | This document |
