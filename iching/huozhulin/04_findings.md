# Probe 4: 飛伏 vs 互 — Two Hidden Structure Mechanisms

## 1. 飛伏 Verified

姤 (乾宮 Metal): visible = 父孫兄鬼兄父, missing = {妻財}
Root (乾) hidden = 孫財父鬼兄父
  → L2 hidden: 甲寅 (Wood) = 妻財

Matches example.md: 甲寅木 hidden under line 2 supplies the missing 妻財. ✓

## 2. Completeness Guarantee

| Status | Count |
|--------|-------|
| No missing types | 16 |
| Missing fully supplied by 飛伏 | 17 |
| Missing NOT fully supplied | 31 |

**Completeness fails for 31 hexagrams.** The palace root cannot supply all
missing types. This is a structural consequence of doubled trigrams:

Only 乾乾 and 坤坤 have position-dependent 納甲 (giving 6 distinct branches,
covering all 5 六親 types). The other 6 roots have upper = lower (position-invariant),
so their 6 lines use only **3 distinct branches → 3 六親 types**.

## 3. Root 六親 Words

| Root | Element | Word | Covers |
|------|---------|------|--------|
| Kun ☷ | Earth | 兄父鬼兄財孫 | 5/5 (miss: —) |
| Zhen ☳ | Wood | 父兄財父兄財 | 3/5 (miss: 孫,鬼) |
| Kan ☵ | Water | 孫鬼財孫鬼財 | 3/5 (miss: 兄,父) |
| Dui ☱ | Metal | 鬼財父鬼財父 | 3/5 (miss: 兄,孫) |
| Gen ☶ | Earth | 兄父孫兄父孫 | 3/5 (miss: 財,鬼) |
| Li ☲ | Fire | 父孫鬼父孫鬼 | 3/5 (miss: 兄,財) |
| Xun ☴ | Wood | 財父鬼財父鬼 | 3/5 (miss: 兄,孫) |
| Qian ☰ | Metal | 孫財父鬼兄父 | 5/5 (miss: —) |


**2 roots cover 5/5** (乾, 坤 — position-split trigrams with 6 distinct branches).
**6 roots cover 3/5** (all others — doubled position-invariant trigrams).

The 3/5 roots create a **structural gap**: 2 六親 types are permanently absent
from both visible and hidden lines for palace members that happen to miss them.
This is the algebraic reason 飛伏 is incomplete for 6 of 8 palaces.

### Structurally absent types by palace

| Palace | Element | Root covers | Absent from root |
|--------|---------|-------------|-----------------|
| Dui ☱ | Metal | 3/5 | 兄, 孫 |
| Gen ☶ | Earth | 3/5 | 財, 鬼 |
| Kan ☵ | Water | 3/5 | 兄, 父 |
| Li ☲ | Fire | 3/5 | 兄, 財 |
| Xun ☴ | Wood | 3/5 | 兄, 孫 |
| Zhen ☳ | Wood | 3/5 | 孫, 鬼 |

## 4. Missing Count × Outer Bits

| (b₀,b₅) | miss=0 | miss=1 | miss=2 |
|----------|--------|--------|--------|
| (0, 0) | 5 | 6 | 5 |
| (0, 1) | 3 | 10 | 3 |
| (1, 0) | 1 | 10 | 5 |
| (1, 1) | 7 | 6 | 3 |

b₀ marginal symmetric: ✓ (b₀=0: {0: 8, 1: 16, 2: 8}, b₀=1: {0: 8, 1: 16, 2: 8})
b₅ marginal symmetric: ✗ (b₅=0: {0: 6, 1: 16, 2: 10}, b₅=1: {0: 10, 1: 16, 2: 6})

If missing count = (b₀ contribution) + (b₅ contribution) as independent binary
variables, we'd expect the 1:2:1 ratio to factor into b₀ and b₅ effects.
The table above shows whether this factoring holds.

## 5. 飛伏 as XOR — Position Analysis

Total needed hidden lines: 32
- On flipped positions (vis ≠ hid): 18
- On unflipped positions (vis = hid): 14

14 needed lines sit on UNFLIPPED positions. At these positions,
the hidden and visible lines are identical — the 'hidden' line carries the
same branch as the visible one. The missing type appears in the root at a
position where the hexagram hasn't changed from its root.

Needed line onion layer distribution:

| Layer | Count |
|-------|-------|
| outer | 13 |
| shell | 12 |
| interface | 7 |

### By rank

| Rank | Flipped | Needing 飛伏 | Needed positions |
|------|---------|-------------|-----------------|
| 本宮 | — | 0/8 | — |
| 一世 | L1 | 2/8 | L2:2 |
| 二世 | L1,L2 | 1/8 | L1:1, L2:1 |
| 三世 | L1,L2,L3 | 2/8 | L1:1, L2:1 |
| 四世 | L1,L2,L3,L4 | 4/8 | L2:2, L3:2, L5:1, L6:3 |
| 五世 | L1,L2,L3,L4,L5 | 5/8 | L1:1, L2:1, L3:2, L5:1, L6:3 |
| 游魂 | L1,L2,L3,L5 | 4/8 | L3:2, L5:1, L6:3 |
| 歸魂 | L5 | 2/8 | L4:1, L5:2, L6:1 |

## 6. 互 vs 飛伏: Element Comparison

Of 48 hexagrams needing 飛伏:
- 互 and 飛伏 share ≥1 element: **7** (15%)
- 互 and 飛伏 disjoint elements: **41** (85%)

| Element | Overlap | 互-only | 飛伏-only |
|---------|---------|---------|----------|
| Wood | 3 | 19 | 1 |
| Fire | 0 | 15 | 6 |
| Earth | 0 | 16 | 0 |
| Metal | 4 | 13 | 4 |
| Water | 0 | 15 | 6 |

The two mechanisms mostly point to **different elements** — they reveal
complementary aspects of the hidden structure, not redundant ones.

## 7. Missing Type → Position Mapping

| Type | Total | Positions | Layers |
|------|-------|-----------|--------|
| 兄弟 (兄) | 4 | L2:1, L5:3 | shell:4 |
| 子孫 (孫) | 9 | L1:3, L3:1, L6:5 | interface:1, outer:8 |
| 父母 (父) | 3 | L2:3 | shell:3 |
| 妻財 (財) | 9 | L2:3, L3:2, L5:2, L6:2 | interface:2, outer:2, shell:5 |
| 官鬼 (鬼) | 7 | L3:3, L4:1, L6:3 | interface:4, outer:3 |

### Position concentration

- 兄弟: max at L5 = 3/4 (75%)
- 子孫: max at L6 = 5/9 (56%)
- 父母: max at L2 = 3/3 (100%)
- 妻財: max at L2 = 3/9 (33%)
- 官鬼: max at L3 = 3/7 (43%)

## 8. Key Findings

### Finding 1: Completeness FAILS — structural gap in 6 palaces

Only 乾宮 and 坤宮 achieve full coverage (visible ∪ hidden = all 5 types).
The other 6 palaces each have **2 types permanently absent** from both visible
and hidden lines. 31 of 48 hexagrams needing 飛伏 have unrecoverable gaps.

The root cause: 納甲's position-split rule. Only 乾 and 坤 assign different
branches when lower vs upper. All other trigrams are position-invariant →
doubled roots have 3 branch elements repeated twice → 3/5 types.

This is the **deepest algebraic asymmetry** in the 火珠林 system: the 乾/坤
distinction in 納甲 (a shell-level design choice) propagates through palace
membership into 飛伏, creating a structural divide between 2 complete palaces
and 6 incomplete ones.

### Finding 2: 兄弟 is the most structurally absent type

- 兄弟 (兄): absent from 4/6 incomplete roots
- 子孫 (孫): absent from 3/6 incomplete roots
- 父母 (父): absent from 1/6 incomplete roots
- 妻財 (財): absent from 2/6 incomplete roots
- 官鬼 (鬼): absent from 2/6 incomplete roots

兄弟 is absent from the most roots. This connects to Probe 1's finding:
most trigrams have 0/3 branch elements matching their own element (same = 兄弟).
The position-invariant doubled trigrams inherit this mismatch.

### Finding 3: Two complementary hidden-structure mechanisms

互 and 飛伏 share elements in 7/48 cases (15%). 
They mostly reveal different elements — the two mechanisms are complementary,
not redundant. 互 shows where the hexagram is going (convergence). 飛伏 shows
what the hexagram lacks (absence). Different questions, different answers.

### Finding 4: Needed hidden lines are NOT restricted to flipped positions

Of 32 needed hidden lines, 14 (44%) sit
on UNFLIPPED positions where hidden = visible. The missing type exists in the
root at that position with the same branch as the visible line — the missing type
is 'present but spoken for' (already assigned a different 六親 in the hexagram's
context). 飛伏 doesn't just fill gaps at changed positions — it searches the
entire root for missing types.
