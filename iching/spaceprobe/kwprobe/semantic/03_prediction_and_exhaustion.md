# Prediction Accuracy & Exhaustion-Basin Correspondence

## A. Prediction Accuracy

For each (algebraic feature, semantic feature) pair, we test whether the
algebraic feature can predict the semantic feature. The predictor orientation
is chosen to maximize accuracy. Base rate = accuracy of always predicting
the majority class.

| Predictor | Target | Acc | Base | Lift | MCC | Sens | Spec |
|-----------|--------|:---:|:----:|:----:|:---:|:----:|:----:|
| H-kernel | Weak directionality (⇀) | 0.65 | 0.61 | 1.05 | 0.322 | 0.75 | 0.58 |
| Corridor exit | Weak directionality (⇀) | 0.65 | 0.61 | 1.05 | 0.264 | 0.58 | 0.68 |
| Corridor exit | Implied confidence | 0.65 | 0.74 | 0.87 | 0.246 | 0.62 | 0.65 |
| H-kernel | Implied confidence | 0.58 | 0.74 | 0.78 | 0.239 | 0.75 | 0.52 |
| Preserving bridge | Implied confidence | 0.52 | 0.74 | 0.70 | -0.215 | 0.12 | 0.65 |
| ¬H-kernel | Cyclical logic | 0.61 | 0.74 | 0.83 | 0.205 | 0.62 | 0.61 |
| 互 smooth (≤2) | Cyclical logic | 0.61 | 0.74 | 0.83 | 0.137 | 0.50 | 0.65 |
| Basin crossing | Weak directionality (⇀) | 0.52 | 0.61 | 0.84 | 0.123 | 0.75 | 0.37 |
| Preserving bridge | Cyclical logic | 0.65 | 0.74 | 0.87 | 0.110 | 0.38 | 0.74 |
| Corridor exit | Cyclical logic | 0.58 | 0.74 | 0.78 | 0.096 | 0.50 | 0.61 |
| ¬互 smooth (≤2) | Weak directionality (⇀) | 0.52 | 0.61 | 0.84 | 0.088 | 0.67 | 0.42 |
| Preserving bridge | Weak directionality (⇀) | 0.52 | 0.61 | 0.84 | -0.071 | 0.25 | 0.68 |
| ¬Basin crossing | Cyclical logic | 0.61 | 0.74 | 0.83 | 0.066 | 0.38 | 0.70 |
| ¬Basin crossing | Implied confidence | 0.61 | 0.74 | 0.83 | 0.066 | 0.38 | 0.70 |
| 互 smooth (≤2) | Implied confidence | 0.55 | 0.74 | 0.74 | -0.015 | 0.38 | 0.61 |

### Key

- **Acc**: Prediction accuracy (fraction correct)
- **Base**: Base rate accuracy (always predict majority class)
- **Lift**: Acc / Base — values near 1.00 mean no improvement over guessing
- **MCC**: Matthews Correlation Coefficient (-1 to +1; 0 = no correlation)
- **Sens/Spec**: Sensitivity (true positive rate) / Specificity (true negative rate)

### Assessment

Best predictor: **H-kernel** → **Weak directionality (⇀)** (|MCC| = 0.322, lift = 1.05)

**No algebraic feature improves prediction of any semantic feature by more than 10% over base rate.** The best predictors achieve lifts of 1.00–1.08, meaning the algebraic profile is essentially useless for predicting semantic content.

This confirms the Fisher test results from Round 2: the independence at the bridge level is not a matter of statistical power — even with the most favorable predictor orientation, algebraic features carry no actionable information about semantic features.

## B. Exhaustion-Basin Correspondence

The 8 cyclical transitions use the Xugua's exhaustion formula: 'X cannot last forever.'
Does this narrative event correspond to a specific algebraic event in basin space?

### B1. The 8 exhaustion transitions

| T# | What exhausts | Bridge | Basin | ×? | Corridor | Regime |
|:--:|---------------|--------|-------|:--:|----------|:------:|
| 6 | Pi (Stagnation) | Pi→Tong Ren | Kan→Qia | **Y** | LOCAL_EXIT | rich |
| 11 | Bi (Adornment/Grace) | Bi→Bo | Kan→Kun | **Y** | TERM_EXIT | rich |
| 14 | Da Guo (Great Excess) | Da Guo→Kan | Qia→Kun | **Y** | LOCAL_EXIT | rich |
| 16 | Heng (Duration) | Heng→Dun | Qia→Qia | N | TERM_EXIT | rich |
| 17 | Da Zhuang (Great Strength) | Da Zhuang→Jin | Qia→Kan | **Y** | NONE | free |
| 21 | Yi (Increase) | Yi→Guai | Kun→Qia | **Y** | NONE | free |
| 23 | Sheng (Ascending) | Sheng→Kun | Kan→Kan | N | NONE | free |
| 26 | Gen (Keeping Still) | Gen→Jian | Kan→Kan | N | INIT_ENTRY | rich |

### B2. Basin-crossing rates

| Category | Crossing | Total | Rate |
|----------|:--------:|:-----:|:----:|
| Cyclical | 5 | 8 | 62% |
| Causal | 14 | 20 | 70% |
| All | 21 | 31 | 68% |

Cyclical transitions cross basins at **the same rate as causal** transitions.
Exhaustion is not a basin-crossing event.

### B3. Basin directionality

Among the 5 crossing cyclical transitions:

| Exit basin | Entry basin | Count |
|-----------|-------------|:-----:|
| KanLi | Kun | 1 |
| KanLi | Qian | 1 |
| Kun | Qian | 1 |
| Qian | KanLi | 1 |
| Qian | Kun | 1 |

No single direction dominates. Exhaustion can exit any basin and enter any basin.
Compare with causal crossings:

| Exit basin | Entry basin | Count |
|-----------|-------------|:-----:|
| KanLi | Kun | 5 |
| KanLi | Qian | 2 |
| Kun | KanLi | 4 |
| Qian | KanLi | 3 |

### B4. Fixed-point basin exits

Does exhaustion preferentially exit fixed-point basins (Kun/Qian) vs the
oscillation basin (KanLi)?

| Category | From fixed | From KanLi | n |
|----------|:----------:|:----------:|:-:|
| Cyclical crossings | 3 | 2 | 5 |
| Causal crossings | 7 | 7 | 14 |

Cyclical exits from fixed-point basins: 60%. Causal: 50%. 
No meaningful difference.

### B5. Non-crossing exhaustion (within-basin)

Three cyclical transitions stay within their basin — the exhaustion
is purely semantic, with no algebraic basin event:

| T# | Bridge | Basin | What exhausts |
|:--:|--------|-------|---------------|
| 16 | Heng→Dun | Qian | Heng (Duration) |
| 23 | Sheng→Kun | KanLi | Sheng (Ascending) |
| 26 | Gen→Jian | KanLi | Gen (Keeping Still) |

Two stay in KanLi, one in a fixed-point basin.

### B6. Corridor mediation

- Cyclical at corridor exits: **4/8**
- Cyclical NOT at corridor exits: **4/8**

Among all corridor exits, basin-crossing rate by logic type:

| Logic at exit | Crossing | Total | Rate |
|------------|:--------:|:-----:|:----:|
| Cyclical | 3 | 4 | 75% |
| Causal | 6 | 9 | 67% |

Cyclical and causal transitions at corridor exits cross basins at similar rates.
The corridor exit itself — not the logic type — determines whether a basin
crossing occurs.

### B7. Direct Kun↔Qian crossings: exclusively cyclical

A specific finding emerges from the basin direction data:

| T# | Direction | Logic | Bridge |
|:--:|-----------|-------|--------|
| 14 | Qian→Kun | Cyclical | Da Guo→Kan |
| 21 | Kun→Qian | Cyclical | Yi→Guai |

**Both** direct Kun↔Qian inter-pair crossings are cyclical. All 19 other crossings involve KanLi as source or destination.

Hypergeometric p = 0.0476 (5 cyclical among 21 crossings, both of 2 Kun↔Qian slots filled by cyclical).

**Interpretation:** Causal transitions always route through the oscillation basin (KanLi) — they need an intermediary. Only the exhaustion formula ('cannot last forever') jumps directly between fixed-point basins. The causal chain channels through KanLi; exhaustion-reversal leaps across it.

This is the one point where algebra and semantics show a *specific* correspondence at the bridge level: the narrative event of exhaustion-reversal maps to the algebraic event of direct fixed-point basin crossing. But the sample (n=2) is structurally fixed — there are only 2 such crossings in the sequence — so this is a structural observation, not a generalizable statistical finding.

### B8. Summary: The exhaustion-basin relationship

**Exhaustion is primarily a semantic event, not an algebraic one.**

At the aggregate level, the 'cannot last forever' formula:
- Does NOT preferentially cross basins (63% vs 68% base rate)
- Does NOT preferentially exit fixed-point basins
- Operates equally within-basin (3/8) and across basins (5/8)

**But at the specific point of direct Kun↔Qian crossing**, exhaustion and algebra coincide: both direct fixed-point crossings use the cyclical formula (p=0.048). This is where the 'grain' of coupling shows: not at the level of general cross-tabs, but at the level of specific structural events.

The relationship:
- **General crossings:** algebra and semantics independent
- **Direct fixed-point crossings:** exclusively cyclical (n=2, structurally fixed)
- **Within-basin exhaustion:** purely semantic (no algebraic event at all)

The basin structure and the exhaustion grammar are largely orthogonal, but they touch at the extreme — where the sequence makes its rarest algebraic move (direct Kun↔Qian jump), the narrative always uses its strongest formula (exhaustion-reversal).
