# Probe 8e: 納甲 Under Complement

> Algebraic analysis of whether the complement involution σ extends
> from trigram-level to line-level 納甲 element assignments.

---

## Part 1: 納甲 as a Trigram-Level Map

The 納甲 system factors through trigrams: each line's assignment depends only on
which trigram it belongs to and its position (lower/upper) in the hexagram.

| Trigram | Position | Stem | Branches | Elements | Trig Elem |
|---------|----------|------|----------|----------|-----------|
| 坤 | lower | 乙 | 未 巳 卯 | 土 火 木 | 土 |
| 坤 | upper | 癸 | 丑 亥 酉 | 土 水 金 | 土 |
| 震 | lower | 庚 | 子 寅 辰 | 水 木 土 | 木 |
| 震 | upper | 庚 | 子 寅 辰 | 水 木 土 | 木 |
| 坎 | lower | 戊 | 寅 辰 午 | 木 土 火 | 水 |
| 坎 | upper | 戊 | 寅 辰 午 | 木 土 火 | 水 |
| 兌 | lower | 丁 | 巳 卯 丑 | 火 木 土 | 金 |
| 兌 | upper | 丁 | 巳 卯 丑 | 火 木 土 | 金 |
| 艮 | lower | 丙 | 辰 午 申 | 土 火 金 | 土 |
| 艮 | upper | 丙 | 辰 午 申 | 土 火 金 | 土 |
| 離 | lower | 己 | 卯 丑 亥 | 木 土 水 | 火 |
| 離 | upper | 己 | 卯 丑 亥 | 木 土 水 | 火 |
| 巽 | lower | 辛 | 丑 亥 酉 | 土 水 金 | 木 |
| 巽 | upper | 辛 | 丑 亥 酉 | 土 水 金 | 木 |
| 乾 | lower | 甲 | 子 寅 辰 | 水 木 土 | 金 |
| 乾 | upper | 壬 | 午 申 戌 | 火 金 土 | 金 |

**Position invariance:** Only 乾 and 坤 differ between lower and upper position.
All other trigrams are position-invariant in their branch-element assignments.

## Part 2: Complement at Trigram Level

At the trigram-element level, complement is known to induce -id on Z₅:
  Wood↔Wood, Fire↔Water, Earth↔Metal (verified for all 4 complement pairs).

**Key question:** Does this extend to the 3-line 納甲 branch-element assignments?

- 乾↔坤 (lower): ['水', '木', '土'] ↔ ['土', '火', '木']  Z₅ diffs=[3, 1, 3]  ✗
- 乾↔坤 (upper): ['火', '金', '土'] ↔ ['土', '水', '金']  Z₅ diffs=[1, 1, 1]  ✓
- 震↔巽 (lower): ['水', '木', '土'] ↔ ['土', '水', '金']  Z₅ diffs=[3, 4, 1]  ✗
- 震↔巽 (upper): ['水', '木', '土'] ↔ ['土', '水', '金']  Z₅ diffs=[3, 4, 1]  ✗
- 坎↔離 (lower): ['木', '土', '火'] ↔ ['木', '土', '水']  Z₅ diffs=[0, 0, 3]  ✗
- 坎↔離 (upper): ['木', '土', '火'] ↔ ['木', '土', '水']  Z₅ diffs=[0, 0, 3]  ✗
- 艮↔兌 (lower): ['土', '火', '金'] ↔ ['火', '木', '土']  Z₅ diffs=[4, 4, 4]  ✓
- 艮↔兌 (upper): ['土', '火', '金'] ↔ ['火', '木', '土']  Z₅ diffs=[4, 4, 4]  ✓

**Result:** σ produces Z₅ shifts [0, 1, 3, 4] across all lines.
The complement-Z₅ structure does **NOT** extend uniformly to 納甲 branch-level.

## Part 3: Hexagram-Level Complement

Of 32 complement pairs:
- **2** have a single uniform Z₅ shift across all 6 lines
- **30** have mixed shifts

Of the 30 inconsistent pairs:
- **2** have uniform shift within each half (lower vs upper)
  but different shifts between halves.

### Z₅ diff pattern distribution

| Pattern (lower|upper) | Count | Uniform? |
|----------------------|------:|----------|
| [2, 4, 2]\|[4, 4, 4] | 1 |  |
| [3, 4, 1]\|[4, 4, 4] | 1 |  |
| [0, 0, 3]\|[4, 4, 4] | 1 |  |
| [1, 1, 1]\|[4, 4, 4] | 1 |  |
| [4, 4, 4]\|[4, 4, 4] | 1 | ✓ |
| [0, 0, 2]\|[4, 4, 4] | 1 |  |
| [2, 1, 4]\|[4, 4, 4] | 1 |  |
| [3, 1, 3]\|[4, 4, 4] | 1 |  |
| [2, 4, 2]\|[3, 4, 1] | 1 |  |
| [3, 4, 1]\|[3, 4, 1] | 1 |  |
| [0, 0, 3]\|[3, 4, 1] | 1 |  |
| [1, 1, 1]\|[3, 4, 1] | 1 |  |
| [4, 4, 4]\|[3, 4, 1] | 1 |  |
| [0, 0, 2]\|[3, 4, 1] | 1 |  |
| [2, 1, 4]\|[3, 4, 1] | 1 |  |
| [3, 1, 3]\|[3, 4, 1] | 1 |  |
| [2, 4, 2]\|[0, 0, 3] | 1 |  |
| [3, 4, 1]\|[0, 0, 3] | 1 |  |
| [0, 0, 3]\|[0, 0, 3] | 1 |  |
| [1, 1, 1]\|[0, 0, 3] | 1 |  |
| [4, 4, 4]\|[0, 0, 3] | 1 |  |
| [0, 0, 2]\|[0, 0, 3] | 1 |  |
| [2, 1, 4]\|[0, 0, 3] | 1 |  |
| [3, 1, 3]\|[0, 0, 3] | 1 |  |
| [2, 4, 2]\|[1, 1, 1] | 1 |  |
| [3, 4, 1]\|[1, 1, 1] | 1 |  |
| [0, 0, 3]\|[1, 1, 1] | 1 |  |
| [1, 1, 1]\|[1, 1, 1] | 1 | ✓ |
| [4, 4, 4]\|[1, 1, 1] | 1 |  |
| [0, 0, 2]\|[1, 1, 1] | 1 |  |
| [2, 1, 4]\|[1, 1, 1] | 1 |  |
| [3, 1, 3]\|[1, 1, 1] | 1 |  |

## Part 4: Line-Level vs Trigram-Level Elements

Each trigram's 3 branch elements form an arithmetic progression in Z₁₂ (branch ring),
projected to Z₅ via the 地支→五行 map.

## Part 5: Algebraic Structure

**地支 → 五行 fiber sizes:** Earth=4, Wood=2, Fire=2, Metal=2, Water=2

**Not a group homomorphism** from Z₈ × Z₃ → Z₅ because:
- Starting points are a table lookup (not linear in trigram index)
- The Z₁₂ → Z₅ projection is non-homomorphic (12 ∤ 5)
- Best linear approximation matches only 9/24 cells

**Actual structure:** composition of an affine map and a fixed projection:
```
(trigram, line_pos) → start[trigram] + polarity × 2 × pos  (mod 12)  →  element
         Z₂³ × Z₃        affine per trigram on Z₁₂               Z₁₂ → Z₅
```

## Synthesis

The complement-Z₅ involution, which operates cleanly at the trigram-element
level (as -id on Z₅), does **not** extend uniformly to the 納甲 branch-element
level. The inconsistency arises because:
1. Complement swaps yang↔yin polarity, reversing the branch stepping direction
2. The branch→element projection (Z₁₂ → Z₅) is non-linear
3. Reversing direction in Z₁₂ does not commute with projection to Z₅

This confirms the structural boundary between the trigram-level algebra
(where complement-Z₅ operates) and the 火珠林 line-level system
(where 納甲 introduces a non-algebraic table lookup that breaks the symmetry).

### Why it breaks: the Earth fiber

The Z₁₂ branch ring maps to Z₅ elements via 地支→五行. This projection is
non-uniform: Earth has 4 branches (丑辰未戌) while all others have 2.
Yang/yin sequences step by ±2 in Z₁₂ (arithmetic progressions), but the
Z₁₂ → Z₅ projection converts these to non-constant Z₅ step sequences:
- Yang Z₅ steps: [1, 2, 4, 2, 4]
- Yin Z₅ steps: [2, 4, 4, 4, 4]

Non-constant steps mean that shifting the starting point in Z₁₂ (as complement does)
changes the Z₅ step pattern seen by a 3-line window. Only 艮↔兌 avoids this
because their specific starting-point offsets happen to sample windows with
identical Z₅ step sequences.

### Factoring structure of the inconsistency

2/30 inconsistent pairs maintain per-half consistency
(uniform Z₅ shift within each half, different shifts between halves).
This follows from 納甲 factoring: complement acts independently on each trigram half.
The two halves receive different Z₅ shifts when their trigram complement pairs differ
(which is true for all hexagrams where lower and upper trigrams are from different
complement families).

Only 2/32 pairs achieve full 6-line consistency:
- 000100 (艮|坤) ↔ 111011 (兌|乾): uniform shift +4
- 011011 (兌|兌) ↔ 100100 (艮|艮): uniform shift +1
