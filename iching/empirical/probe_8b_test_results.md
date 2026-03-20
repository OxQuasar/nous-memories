# Probe 8b Test Results

> Statistical tests on 皇極經世 vol 6 event data.
> Tests whether event character correlates with 天干/五行 cycle position.

---

## Data Summary

- Source: 皇極經世書 vol 6 (四庫全書 edition)
- Entries: 1320 total, 1111 with text
- Period: ~44 × 30-year blocks (Warring States through Five Dynasties)

## Event Classification

| Class | Count | % |
|-------|------:|---:|
| Unfavorable | 314 | 23.8% |
| Favorable | 163 | 12.3% |
| Mixed | 292 | 22.1% |
| Neutral | 342 | 25.9% |
| Blank | 209 | 15.8% |

Testable (favorable + unfavorable): **477** entries.

## Test Results

### Test 1: event_character × 5 elements (天干→五行)

χ² = 1.962, df = 4, **p = 0.7428**
Cramér's V = 0.0641 [0.0000, 0.1539]

| Element | Unfav | Fav | Total | %Unfav |
|---------|------:|----:|------:|-------:|
| 木 | 58 | 38 | 96 | 60.4% |
| 火 | 52 | 26 | 78 | 66.7% |
| 土 | 78 | 38 | 116 | 67.2% |
| 金 | 62 | 33 | 95 | 65.3% |
| 水 | 64 | 28 | 92 | 69.6% |

**Result: NULL — no significant association.**

### Test 2: event_character × 10 stems

χ² = 4.054, df = 9, **p = 0.9078**
Cramér's V = 0.0922 [0.0024, 0.1819]

**Result: NULL.**

### Test 3: Permutation control

χ² is invariant to row permutation — all 120 element assignments give
identical χ² = 1.962. This is a structural property: permuting
which stem-pair maps to which element just reorders rows in the table.

Monte Carlo variance test (10,000 random 5-group partitions):
- Canonical pair-rate variance: 0.000925
- Monte Carlo p = 0.7499

**Result: canonical 五行 ordering is NOT special among random groupings.**

### Test 4: event_character × stem-branch 五行 relation

⚠ Tests 八字 year-pillar interpretation, not 梅花 date formula.

χ² = 3.910, df = 4, **p = 0.4183**
Cramér's V = 0.0905 [0.0008, 0.1803]

**Result: NULL.**

### Test 5: Effect size bounds

With N=477, if an effect exists, the maximum difference in unfavorable
rate between any two elements is bounded by **22.7%** (95% CI).

Largest observed difference: 木 vs 水 = 0.091

## Transition Analysis

Consecutive-year transitions (N=979):
- 比和: 490 (50.1%)
- 生: 489 (49.9%)
- 克: 0 (0.0%)

Event-to-event transitions, skipping blanks (N=1110):
- 比和: 490 (44.1%)
- 生: 589 (53.1%)
- 克: 27 (2.4%)

The 天干 cycle structurally forbids 克 at the year-to-year level.
Even with gaps, only 27 克 transitions exist.
E2 (克→克 suppression) and E3 (valve: 克→生=0) are **structurally untestable**.

## Synthesis

All tests return null. No detectable association between 天干/五行 cycle position and event character at the year level. This bounds the grammar resolution: the 梅花 date formula requires finer temporal input (full date+hour) to generate relational predictions. A single years 天干 label does not carry predictive information about historical event character.
