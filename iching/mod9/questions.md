# Lo Shu Spatial Structure — Questions

## Core Question: What is the Z₅ structure of the Lo Shu compass layout?

The 梅花易數 describes two divination methods. The 先天 method uses mod-8 arithmetic on the Fu Xi ordering (fully characterized in mod8/findings.md §I–§IX). The 後天 method uses physical observation + compass direction to select trigrams, with the Lo Shu magic square providing the spatial mapping from compass directions to trigrams.

**Framing correction:** The 後天 method does not use "mod-9 arithmetic." Vol2 line 16 explicitly recommends 先天 numbers for divination calculation, and every worked example (vol1 lines 209–237) confirms: the arithmetic uses 先天 numbers (乾=1 through 坤=8) with mod-6 for the moving line. The Lo Shu provides the **spatial mapping** (compass direction → trigram), not the calculation system.

### The 後天 numbering

From 梅花易數 vol2 line 16:

| Lo Shu # | Trigram | Binary | Element | Z₅ | Direction |
|----------|---------|--------|---------|-----|-----------|
| 1 | 坎 | 010 | 水 | 4 | N |
| 2 | 坤 | 000 | 土 | 2 | SW |
| 3 | 震 | 001 | 木 | 0 | E |
| 4 | 巽 | 110 | 木 | 0 | SE |
| 5 | (中) | — | 土 | 2 | Center |
| 6 | 乾 | 111 | 金 | 3 | NW |
| 7 | 兌 | 011 | 金 | 3 | W |
| 8 | 艮 | 100 | 土 | 2 | NE |
| 9 | 離 | 101 | 火 | 1 | S |

Position 5 (中/Center) is the observer's location — the coordinate origin from which all 8 directions are measured. It has Earth content (Z₅=2) but no trigram because the observer is not an observable state.

### How the 後天 method works (vol1 lines 149–151, vol2 line 16)

- **Input:** Physical observation (object + direction). Object → upper trigram (by 象 correspondence). Compass direction of the object → lower trigram (by Lo Shu position).
- **Moving line:** Sum of object number + direction number + hour, mod 6. Uses **先天 numbers** for calculation.
- **Evaluation:** Uses 爻辞 (line texts) AND 卦辭 (hexagram texts) alongside 體用 五行. Vol2: "先天者...辞前之《易》也" (先天 = Yi before the text); "后天则...辞后之《易》也" (後天 = Yi after the text).

### Key structural differences from 先天

| | 先天 | 後天 |
|---|---|---|
| Spatial structure | Z₈ cycle (binary counter) | Lo Shu compass (magic square) |
| Trigram mapping | 8 positions ↔ 8 trigrams (bijection) | 8 directions + center origin (surjection) |
| Input | Calendar arithmetic | Physical observation + compass |
| Evaluation | 體用 五行 only | 體用 + 爻辭 + 卦辭 |
| Complement | n ↔ 9−n (through 木 boundary) | n ↔ 10−n (through Earth center) |
| Z₅ character | Retrograde (1:4) | Prograde (4:2) |

---

## Questions

**N1 [answered]:** What does the Lo Shu cycle project to on Z₅? → The 後天 compass cycle (S→SW→W→NW→N→NE→E→SE) is uniquely prograde (4:2 pro:retro) among all tested cycles. Temporal inverse of 先天's 1:4. Type sequence: 生↑ 生↑ 比和 生↑ 克↓ 克↓ 比和 生↑. Clean phase structure with generative run → 克 break → restart from 木. See exploration-log §1.

**N2 [answered]:** What is the center position? → The observer's location. Vol1 line 173: "人则介乎其中." Not a fixed point, absorbing state, or pass-through — it is the null observation, the coordinate origin. The 9th position belongs to the number system (Z₉ needs an origin), not the state space (F₂³ describes observables). See exploration-log §1.

**N3 [answered]:** Magic square Z₅ structure? → Z₅ sums are not constant (the sum-to-15 property doesn't transfer through the surjection). The SW→NE diagonal {坤,中,艮} = all 土 is the only monochromatic line. Earth IS the Lo Shu skeleton. See exploration-log §1.

**N4 [answered]:** Flying star Z₅ structure? → Does NOT have constant Hamming-2 (correcting opposition-theory/loshu.md). Actual Hamming distances: [1,3,1,3,1,1,3]. Z₅ type sequence for trigram transitions: all non-trivial steps retrograde, bracketed by 比和. See exploration-log §1.

**N5 [answered, conceptual]:** Does the 後天 method's use of 爻辭 bridge algebra and text? → The bridge is operational, not structural. The 先天 method uses algebra alone (体用 五行). The 後天 adds text (爻辭 + 卦辭) to the judgment. This doesn't change the mathematical independence (89% separation, semantic-map findings). The tradition explicitly designed two methods for two layers: 先天 = "辞前之《易》" (Yi before the text), 後天 = "辞后之《易》" (Yi after the text).

**N6 [answered]:** Is position 5 a structural gap? → No. It is the observer's position — structurally outside F₂³ because F₂³ describes observable states and the observer is not observable. Earth is already represented by 坤 and 艮 in the state space. The center belongs to the coordinate system, not the measurement space. See exploration-log §1.

---

## Findings beyond initial questions

### Compass H2-segregation (§2)

Every non-trivial Z₅ transition (生 or 克) in the compass cycle occurs at Hamming distance exactly 2. Selectivity: 192/40320 = 0.48%. The converse (比和 → H≠2) is tautological — same-element trigram pairs never have H=2, a consequence of the canonical 五行 surjection. H=2 is the unique Hamming distance class carrying only cross-element pairs.

### Traditional 後天 uniquely determined (§3)

Five constraints intersect at exactly 1 permutation:

| Stage | Count | Constraint |
|---|---|---|
| All permutations | 40320 | — |
| + H2-segregation + directional purity | 32 | Non-trivial→H=2, all 生 same dir, all 克 same dir |
| + prograde | 16 | 生↑, 克↓ |
| + 火 at S | 2 | Fix rotation by element-direction correspondence |
| + 土 antipodal | **1** | 坤(SW) and 艮(NE) diametrically opposite |

No constraint is redundant. 木 adjacent is forced by H2 + directional purity alone (32/32).

### Parity bipartition — why 木 adjacency is forced (§3)

Hamming-2 preserves binary weight parity, creating a bipartite structure:
- Odd parity: 震(001), 坎(010), 艮(100), 乾(111) — Z₅: {0, 4, 2, 3}
- Even parity: 坤(000), 巽(110), 兌(011), 離(101) — Z₅: {2, 0, 3, 1}

All same-element pairs are cross-parity. The two 比和 crossings are the compass cycle's parity jumps. If 木 is not adjacent, both parity blocks have 4 members needing 3-step paths through 4 Z₅ values — impossible to traverse directionally pure. If 木 IS adjacent, removing Z₅(0) leaves residuals {2,3,4} and {1,2,3} — both consecutive on Z₅, enabling monotone 2-step paths.

Z₅(0) = 木 is the **unique** element whose removal yields consecutive residuals in both parity classes. Removing Z₅(1)=火 leaves {0,2,3,4}/{0,2,3}: non-consecutive. Z₅(2)=土 leaves {0,3,4}/{0,1,3}: non-consecutive. Z₅(3)=金 leaves {0,2,4}/{0,1,2}: odd non-consecutive. Z₅(4)=水 leaves {0,2,3}/{0,1,3}: even non-consecutive.

### M6 resolved: 木's dual pivot role (§3)

木's pivot in both 先天 (palindrome center, §VIII) and 後天 (克/生 bridge) traces to Z₅=0, the identity of the 生 cycle. Not coincidence, not free choice — forced by the same algebraic property in both systems.

### He Tu embedding (§2)

The compass cycle's 6 non-trivial transitions include all 4 He Tu pairs plus 2 Earth-singleton bridges. Zero Lo Shu diametric pairs appear (H ∈ {1,3}, never 2). The compass walks through the He Tu at He Tu distance.

### Three pairing systems (§1)

| System | 生 | 克 | 比和 | Character |
|--------|-----|-----|------|-----------|
| He Tu | 3 | 1 | 0 | generative |
| 先天 | 2 | 1 | 1 | retrograde |
| Lo Shu | 0 | 3 | 1 | destructive |

Fixed elements: 木 for 先天 (complement-algebraic), 土 for Lo Shu (spatial-geometric), none for He Tu.

---

## Open questions

**N7:** The uniqueness cascade uses 5 constraints. Can a more economical set suffice? E.g., can 火=S + 土 antipodal be replaced by a single algebraic condition?

**N8:** The He Tu embedding in the compass cycle connects to the He Tu's traditional meaning (yang-yin directional pairings). What is the structural relationship between the He Tu's cosmological interpretation and its algebraic role as the transition vocabulary of the compass cycle?

### Source

梅花易數 vol1 lines 140, 149–151, 173, 209–237; vol2 lines 15–16. Full text in `texts/meihuajingshu/`.
