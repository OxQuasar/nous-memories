# Divination Examples: 梅花 Method × Algebraic Structure

Four examples showing how the 梅花易數 divination framework maps onto the algebraic (basin/kernel/五行) structure. Each example uses the correct 梅花 method: identify 體/用, evaluate all layers against the single 體, read temporally.

## Method (from 梅花易數)

1. **體/用:** The trigram without the moving line = 體 (self/static). The trigram with the moving line = 用 (situation/dynamic).
2. **互卦:** Remove lines 1 and 6, split middle 4 lines into two overlapping trigrams. The 互 on 體's side = 體互, the 互 on 用's side = 用互.
3. **變卦:** Flip the moving line. The changed trigram = 變.
4. **Evaluate:** All of 用, 體互, 用互, 變 are measured against the single 體's element.
5. **Temporal:** 用 = now, 互 = middle period, 變 = end result.
6. **體黨/用黨:** Count allies by element. 體黨 > 用黨 → 體勢盛.

**Priority (vol3:34):** 用 > 互 > 變. Within 互: 體互最緊，用互次之.

**五行 relations against 體:**

| Relation | Meaning | 斷 |
|---|---|---|
| 用生體 | other feeds self | 進益之喜 (gain) |
| 體克用 | self dominates other | 諸事吉 (auspicious) |
| 比和 | same element | 百事順遂 (smooth) |
| 體生用 | self feeds other | 耗失之患 (drain) |
| 用克體 | other dominates self | 諸事凶 (inauspicious) |

## Algebraic Overlay

Each transition also has a kernel (O,M,I) from the XOR structure:
- **I=0:** Interface preserved → basin preserved → harmonious territory
- **I=1:** Interface broken → basin may cross → destructive territory
- **本→互 always has I=0** (proven algebraically)
- **Lines 3,4** flip interface bits → I=1 → only lines that can cross basins

---

## Example 1: 泰 #11, Line 5 Moving

**Wing line (bit 4) → I=0 → basin preserved**

### Setup

```
line 6: 0  ──  ──  坤 ☷ (土) ← 用
line 5: 0  ──  ──  ← moving
line 4: 0  ──  ──  h₃ (interface) ┐ 坎離
line 3: 1  ══════  h₂ (interface) ┘
line 2: 1  ══════
line 1: 1  ══════  乾 ☰ (金) ← 體
```

**體** = 乾 (金/Metal), **用** = 坤 (土/Earth)

### 互卦 (歸妹 #54)

體 is lower → 體互 = lower 互, 用互 = upper 互
- **體互** = 兌 ☱ (金/Metal)
- **用互** = 震 ☳ (木/Wood)

### 變卦 (需 #5)

Flip line 5: 坤 → 坎. 變(用side) = 坎 ☵ (水/Water)

### 梅花 Evaluation (all vs 體=金)

| Layer | Trigram | 五行 | Relation | 斷 | 黨 |
|---|---|---|---|---|---|
| 用 | 坤 ☷ | 土 | 用生體 (土生金) | 進益之喜 | 用黨 |
| 體互 | 兌 ☱ | 金 | 比和 | 百事順遂 | 體黨 |
| 用互 | 震 ☳ | 木 | 體克用 (金克木) | 諸事吉 | — |
| 變 | 坎 ☵ | 水 | 體生用 (金生水) | 耗失之患 | — |

**體黨=2** (乾+兌, both 金), **用黨=1** (坤 alone). **體勢盛.**

### Temporal Reading

- **Now (用):** 土生金 → 體 receives nourishment. Favorable start.
- **Middle (互):** 體互=比和 (ally), 用互=體克 (dominated). 體 strongest here.
- **End (變):** 金生水 → **體 drains itself to produce the outcome.** Loss through generosity.

**先吉後有耗.** Starts well, middle is strong, ending involves expenditure. The traditional line text: 「帝乙歸妹」— the emperor gives his daughter in marriage. A willing gift from strength, not a defeat.

### Algebraic Layer

- 本→互: kernel=(0,0,0)=id, I=0, basin 坎離→坎離 (preserved)
- 本→變: kernel=(0,1,0)=M, I=0, basin 坎離→坎離 (preserved)

Both transitions are I=0. No basin crossing. The transformation stays within harmonious territory throughout — consistent with the 梅花 reading showing no 用克體 at any layer.

---

## Example 2: 坎 #29, Line 3 Moving

**Interface line (bit 2) → I=1 → basin CROSSING**

### Setup

```
line 6: 0  ──  ──  坎 ☵ (水) ← 體
line 5: 1  ══════
line 4: 0  ──  ──  h₃ (interface) ┐ 坤
line 3: 0  ──  ──  h₂ (interface) ┘
line 2: 1  ══════
line 1: 0  ──  ──  坎 ☵ (水) ← 用, moving
```

**體** = 坎 upper (水/Water), **用** = 坎 lower (水/Water)

### 互卦 (頤 #27)

體 is upper → 體互 = upper 互, 用互 = lower 互
- **體互** = 艮 ☶ (土/Earth)
- **用互** = 震 ☳ (木/Wood)

### 變卦 (井 #48)

Flip line 3: 坎 lower → 巽. 變(用side) = 巽 ☴ (木/Wood)

### 梅花 Evaluation (all vs 體=水)

| Layer | Trigram | 五行 | Relation | 斷 | 黨 |
|---|---|---|---|---|---|
| 用 | 坎 ☵ | 水 | 比和 | 百事順遂 | 體黨 |
| 體互 | 艮 ☶ | 土 | 用克體 (土克水) | **諸事凶** | — |
| 用互 | 震 ☳ | 木 | 體生用 (水生木) | 耗失之患 | — |
| 變 | 巽 ☴ | 木 | 體生用 (水生木) | 耗失之患 | — |

**體黨=2** (坎+坎, both 水), **用黨=0**. 體黨 numerically strong but under attack.

### Temporal Reading

- **Now (用):** 比和 → surface is calm. Danger meets itself neutrally.
- **Middle (互):** **體互=土克水 → 用克體.** The hidden process attacks 體. This is the crisis.
- **End (變):** 水生木 → 體 drains into the outcome. Continued expenditure.

**似吉實凶.** Appears neutral (比和 at start), but the middle period is dangerous (用克體 from 體互=土). The 體 is attacked from its own hidden side, then drained by both 用互 and 變.

### Algebraic Layer

- 本→互: kernel=(0,0,0)=id, I=0, basin 坤→坤 (preserved)
- 本→變: kernel=(0,0,1)=I, **I=1**, basin **坤→坎離 (CROSSING)**

The 梅花 reading and algebraic structure converge: the 互 is within the same basin (safe structurally, but 體互=土克水 is elemental attack), while the 變 **crosses basins** (I=1). The interface line breaks the boundary. The danger isn't just elemental — it's topological. The transformation (井, The Well) exists in a different basin from the starting point.

---

## Example 3: 既濟 #63, Line 2 Moving

**Wing line (bit 1) → I=0 → basin preserved**

### Setup

```
line 6: 0  ──  ──  坎 ☵ (水) ← 體
line 5: 1  ══════
line 4: 0  ──  ──  h₃ (interface) ┐ 坎離
line 3: 1  h₂ (interface) ┘
line 2: 0  ──  ──  ← moving
line 1: 1  ══════  離 ☲ (火) ← 用
```

**體** = 坎 upper (水/Water), **用** = 離 lower (火/Fire)

### 互卦 (未濟 #64)

體 is upper → 體互 = upper 互, 用互 = lower 互
- **體互** = 離 ☲ (火/Fire)
- **用互** = 坎 ☵ (水/Water)

### 變卦 (需 #5)

Flip line 2: 離 lower → 乾. 變(用side) = 乾 ☰ (金/Metal)

### 梅花 Evaluation (all vs 體=水)

| Layer | Trigram | 五行 | Relation | 斷 | 黨 |
|---|---|---|---|---|---|
| 用 | 離 ☲ | 火 | 體克用 (水克火) | 諸事吉 | 用黨 |
| 體互 | 離 ☲ | 火 | 體克用 (水克火) | 諸事吉 | 用黨 |
| 用互 | 坎 ☵ | 水 | 比和 | 百事順遂 | 體黨 |
| 變 | 乾 ☰ | 金 | 用生體 (金生水) | 進益之喜 | — |

**體黨=2** (坎+坎), **用黨=2** (離+離). **體勢平.**

### Temporal Reading

- **Now (用):** 水克火 → 體 dominates. Strong opening.
- **Middle (互):** 體互=火(being 克'd), 用互=水(比和). 體 dominates and has allies. Still strong.
- **End (變):** 金生水 → **the outcome feeds 體.** Metal generates Water. Gain at the end.

**先吉後亦吉.** Every layer is either 體克用, 比和, or 用生體. No attack on 體 anywhere. 既濟 with line 2 moving is comprehensively favorable. The completion doesn't collapse — it strengthens.

### Algebraic Layer

- 本→互: kernel=(0,0,0)=id, I=0, basin 坎離→坎離 (preserved)
- 本→變: kernel=(0,1,0)=M, I=0, basin 坎離→坎離 (preserved)

Both I=0. No basin crossing. Structurally safe — consistent with the purely favorable 梅花 reading. Note: 既濟↔未濟 互 is a 2-cycle attractor in the algebraic structure, but the 梅花 reading shows this oscillation is favorable (體 克's both 用 and 體互 Fire).

---

## Example 4: 乾 #1, Line 3 Moving

**Interface line (bit 2) → I=1 → basin CROSSING — but 梅花 reads pure 比和**

### Setup

```
line 6: 1  ══════  乾 ☰ (金) ← 體
line 5: 1  ══════
line 4: 1  ══════  h₃ (interface) ┐ 乾
line 3: 1  ══════  h₂ (interface) ┘
line 2: 1  ══════
line 1: 1  ══════  乾 ☰ (金) ← 用, moving
```

**體** = 乾 upper (金/Metal), **用** = 乾 lower (金/Metal)

Note: 梅花 says 「乾坤無互，互其變卦」— 乾 and 坤 have trivial 互 (identical to 本). The 互 adds no information.

### 互卦 (乾 #1 = itself)

- **體互** = 乾 ☰ (金)
- **用互** = 乾 ☰ (金)

### 變卦 (履 #10)

Flip line 3: 乾 lower → 兌. 變(用side) = 兌 ☱ (金/Metal)

### 梅花 Evaluation (all vs 體=金)

| Layer | Trigram | 五行 | Relation | 斷 | 黨 |
|---|---|---|---|---|---|
| 用 | 乾 ☰ | 金 | 比和 | 百事順遂 | 體黨 |
| 體互 | 乾 ☰ | 金 | 比和 | 百事順遂 | 體黨 |
| 用互 | 乾 ☰ | 金 | 比和 | 百事順遂 | 體黨 |
| 變 | 兌 ☱ | 金 | 比和 | 百事順遂 | 體黨 |

**體黨=5** (everything is 金), **用黨=0**. **體勢極盛.**

### Temporal Reading

- **Now (用):** 比和. Smooth.
- **Middle (互):** 比和. Smooth.
- **End (變):** 比和. Smooth.

**百事順遂.** Pure Metal throughout. No conflict at any layer. The 梅花 reading is completely bland — no tension, no dynamic.

### Algebraic Layer

- 本→互: kernel=(0,0,0)=id, I=0, basin 乾→乾 (preserved). Trivially — 本=互.
- 本→變: kernel=(0,0,1)=I, **I=1**, basin **乾→坎離 (CROSSING)**

**Here the algebra sees what 梅花 misses.** The five-phase evaluation is all 比和 because Metal→Metal can't produce 生/克. But the basin CROSSES — the transformation moves from the 乾 fixed-point attractor into the 坎離 oscillating basin. The I-component is 1. Interface symmetry breaks.

The traditional text for 履: 「履虎尾，不咥人，亨」— treading on the tiger's tail, it does not bite, success. The danger (basin crossing, I=1) is real structurally but invisible to elemental analysis. The tiger doesn't bite because 金=金 everywhere — there's no elemental enemy. But you've left the fixed point. You're now in oscillating territory. The "not biting" is conditional on the elemental protection; the structural danger persists beneath it.

This is the limitation of pure 梅花 五行 analysis: it cannot see basin topology. When all trigrams share an element, the method returns 比和 regardless of whether the transformation crosses algebraic boundaries.

Notably, the 梅花易數 itself acknowledges this gap. Vol2:17 (卦斷遺論) gives the 西林寺 example: 山地剝 where "體用互變，俱比和" (all layers are 比和) yet the result is inauspicious — because a purely 陰 hexagram in a purely 陽 place (a monastery) violates a structural principle that 五行 生克 cannot see. The text concludes: "此理甚明，不必拘體用也" (this principle is clear — don't be rigid about 體用). The I-component captures exactly this kind of structural violation.

---

## Summary: Where 梅花 and Algebra Converge/Diverge

| Example | Moving line | I | Basin | 梅花 verdict | Match? |
|---|---|---|---|---|---|
| 泰 L5 | wing | 0 | preserved | 先吉後有耗 | ✓ Both say safe, gradual drain |
| 坎 L3 | interface | 1 | **crosses** | 似吉實凶 | ✓ Both find hidden danger |
| 既濟 L2 | wing | 0 | preserved | 先吉後亦吉 | ✓ Both say comprehensively safe |
| 乾 L3 | interface | 1 | **crosses** | 百事順遂 | ✗ **Algebra sees danger 梅花 cannot** |

**Convergence:** When elements differ (examples 1-3), the 梅花 五行 evaluation tracks the algebraic I-component well. 用克體 appears when I=1 creates destructive dynamics.

**Divergence:** When elements are identical (example 4), 梅花 returns 比和 uniformly. The algebra still detects basin crossing through I=1. The traditional text (「履虎尾」) knows the danger — it just can't be derived from 五行 alone. The I-component captures structural information invisible to elemental analysis.


## The Hu Operation 

The 互 operation is literally a dimension reduction — 6 bits → 6 bits, but rank drops because it reuses the inner 4 bits with overlap. Apply 
it again, rank drops further. The iteration 本→互→互(互)→... is a cascade of projections that loses information at each step until it hits a fixed
point or cycle.

The basins are the preimages of those fixed points under this projection cascade. 坤 basin = everything that projects down to 000000 (坤). 乾     
basin = everything that projects down to 111111 (乾). 坎離 basin = everything that projects down to the 既濟↔未濟 2-cycle.                        
                       
So the 64-hexagram space is a 6-dimensional structure, but the 互 dynamics really live in 4 dimensions (inner bits), and the attractors live in   
even fewer — the fixed points are 0-dimensional, the 2-cycle is 1-dimensional. Each 互 iteration sheds information until you hit the skeleton.    
              
五行 is labeling the *topology* of this projection — which regions of the 4-dimensional inner space collapse to the same attractor, and whether   
transitions between regions preserve or break the projection path. 生 means the projection path stays smooth. 克 means it crosses a fold.

The I-component detects exactly when you cross a fold — when the projection discontinuity happens. It's the parity of the interface, which is     
where the dimensional overlap in 互 is concentrated.                                                                                         

Thought: Divination as a structured reduction of dimensionality - until the outcome space becomes clearer. 

## Divination lineage

Three key texts, layered historically:

**1. 《京氏易傳》** (京房, Western Han, ~77-37 BC) — the origin. 六爻納甲 was created by the Han dynasty figure 京房 (Jing Fang). 京房 (前77-前37)
was a Western Han 易學 master who founded 今文易學's "京氏學." His text established the 納甲 system — assigning 天干地支 to each line, the 八宮   (eight palace) classification of all 64 hexagrams, and the 六親 (six relations) framework. Each trigram receives a 天干, and each line receives a 
地支, with 陽卦 taking 陽支 and 陰卦 taking 陰支. The original《京氏易傳》survives in 3 volumes with 陸績's annotations, available on ctext.org.  

**2. 《火珠林》** (唐末宋初, ~900-1000 AD) — the practical manual. Traditionally attributed to 麻衣道者 (a Five Dynasties/early Song monk), it is 
the systematic application of 京房's 納甲 method using coins instead of yarrow stalks. It shifted from the original 周易 approach of interpreting 
卦爻辭 to using 五行, 六親 and their 旺相衰弱/生克冲合 to judge outcomes. Its core principle was "卦定根源，六親為主" — the hexagram's palace     
defines the root, the six relations govern judgment.                                       

**3. Later practical compilations** (Ming-Qing):
- 《黃金策》(劉伯溫, Ming)                   
- 《增刪卜易》(李文輝, early Qing)
- 《卜筮正宗》(王洪緒, Qing)    
