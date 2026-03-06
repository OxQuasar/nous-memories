# Global Structure: Bipartite Traversal, 互-Graph Walk, Skeleton Intervals

## Part 1: Bipartite Structure and KW's Traversal

### 1a. The two d≤1 components

At threshold d≤1 (bridge 互 distance ≤ 1), the 32-pair graph splits into exactly 2 components.

| Component | Pairs | Kun ○ | KanLi ◎ | Qian ● |
|-----------|-------|-------|---------|--------|
| A | 16 | 9 | 0 | 7 |
| B | 16 | 0 | 16 | 0 |

**Component A:** 0:Qian, 1:Zhun, 3:Shi, 6:Tong Ren, 9:Lin, 11:Bo, 13:Yi, 14:Kan, 15:Xian, 16:Dun, 20:Sun, 21:Guai, 24:Ge, 27:Feng, 29:Huan, 30:Zhong Fu

**Component B:** 2:Xu, 4:Xiao Chu, 5:Tai, 7:Qian, 8:Sui, 10:Shi He, 12:Wu Wang, 17:Jin, 18:Jia Ren, 19:Jian, 22:Cui, 23:Kun, 25:Zhen, 26:Jian, 28:Xun, 31:Ji Ji


### 1b. KW's component traversal

Sequence: `AABABBABBABABAAAABBBAABBABBABAAB`

| Metric | Value |
|--------|-------|
| Component switches | 19/31 (61%) |
| Same-component stays | 12/31 |
| Number of runs | 20 |
| Mean run length | 1.60 |
| Alternation rate | 0.613 |

Run-length encoding:

| Run | Component | Start | Length |
|-----|-----------|-------|--------|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 1 |
| 2 | A | 3 | 1 |
| 3 | B | 4 | 2 |
| 4 | A | 6 | 1 |
| 5 | B | 7 | 2 |
| 6 | A | 9 | 1 |
| 7 | B | 10 | 1 |
| 8 | A | 11 | 1 |
| 9 | B | 12 | 1 |
| 10 | A | 13 | 4 |
| 11 | B | 17 | 3 |
| 12 | A | 20 | 2 |
| 13 | B | 22 | 2 |
| 14 | A | 24 | 1 |
| 15 | B | 25 | 2 |
| 16 | A | 27 | 1 |
| 17 | B | 28 | 1 |
| 18 | A | 29 | 2 |
| 19 | B | 31 | 1 |

### 1c. Comparison with basin-consistent random orderings

| Metric | KW | Random mean | Random std | Percentile |
|--------|-----|-----------|-----------|------------|
| Component switches | 19 | 19.0 | 0.0 | 100.0% |

**All** basin-consistent orderings produce exactly 19 component switches — the component traversal is **completely determined** by the basin sequence. This confirms that Component A = polar pairs (Kun + Qian) and Component B = center pairs (KanLi). The bipartite structure adds no information beyond what the basin sequence already provides.

### 1d. Component-crossing vs basin-crossing

| Category | Count |
|----------|-------|
| Both cross | 19 |
| Neither | 10 |
| Comp cross only | 0 |
| Basin cross only | 2 |
| Agreement rate | 94% |

Mean d_互: component-crossing = 2.79, same-component = 2.67

Component-crossing and basin-crossing are **largely the same classification** — the bipartite structure aligns with basin structure.

## Part 2: The 互 Graph Walk

### 2a. The 互 graph

| Metric | Value |
|--------|-------|
| Distinct 互 values | 16 |
| Values visited | 16 |
| Edges (transitions) | 31 |
| Distinct edges | 29 |
| Max edge reuse | 2 |
| Degree-imbalanced vertices | 15 |

All 互 values are visited in the inter-pair walk.

### 2b. Visit pattern per 互 value (entry-互 fibers)

| 互 value | Fiber size | KW positions | Gaps | Gap variance |
|----------|-----------|-------------|------|-------------|
| Kun ☷/Kun ☷ | 2 | 11, 13 | 2 | 0.0 |
| Gen ☶/Kun ☷ | 3 | 3, 9, 20 | 6, 11 | 6.2 |
| Kan ☵/Gen ☶ | 1 | 7 | — | 0.0 |
| Xun ☴/Gen ☶ | 1 | 5 | — | 0.0 |
| Zhen ☳/Kan ☵ | 3 | 10, 17, 25 | 7, 8 | 0.2 |
| Dui ☱/Xun ☴ | 1 | 27 | — | 0.0 |
| Kun ☷/Zhen ☳ | 1 | 1 | — | 0.0 |
| Gen ☶/Zhen ☳ | 3 | 14, 29, 30 | 15, 1 | 49.0 |
| Kan ☵/Li ☲ | 4 | 18, 19, 26, 31 | 1, 7, 5 | 6.2 |
| Xun ☴/Li ☲ | 3 | 2, 4, 28 | 2, 24 | 121.0 |
| Zhen ☳/Dui ☱ | 3 | 8, 12, 22 | 4, 10 | 9.0 |
| Li ☲/Dui ☱ | 1 | 23 | — | 0.0 |
| Dui ☱/Qian ☰ | 4 | 6, 15, 16, 24 | 9, 1, 8 | 12.7 |
| Qian ☰/Qian ☰ | 2 | 0, 21 | 21 | 0.0 |

Mean gap variance: 22.7 (uniform spacing would give 0.0)

### 2c. Intra-pair vs inter-pair 互 distances

| Type | Distribution | Mean |
|------|-------------|------|
| Intra-pair (forced) | 0:4, 2:8, 4:8, 6:12 | 3.75 |
| Inter-pair (chosen) | 0:1, 1:5, 2:6, 3:13, 4:2, 5:3, 6:1 | 2.74 |

### 2d. Walk self-intersection

2 inter-pair edges are reused (29 distinct / 31 total):

| Edge | Count |
|------|-------|
| Qian ☰/Xun ☴→Zhen ☳/Kan ☵ | 2 |
| Kan ☵/Gen ☶→Kan ☵/Li ☲ | 2 |

## Part 3: Skeleton Intervals

Skeleton pairs (self-reverse complement): positions [0, 13, 14, 30]

| Position | Pair | Entry basin | Exit basin |
|----------|------|------------|-----------|
| 0 | Qian/Kun | ● | ○ |
| 13 | Yi/Da Guo | ○ | ● |
| 14 | Kan/Li | ○ | ● |
| 30 | Zhong Fu/Xiao Guo | ○ | ● |

### Interval decomposition

The skeleton pairs divide the sequence into intervals:

- **Skeleton** pair 0: Qian/Kun
- **Interval [1..12]** (12 pairs): ◎:7, ○:4, ●:1
- **Skeleton** pair 13: Yi/Da Guo
- **Skeleton** pair 14: Kan/Li
- **Interval [15..29]** (15 pairs): ◎:8, ○:2, ●:5
- **Skeleton** pair 30: Zhong Fu/Xiao Guo
- **Interval [31..31]** (1 pairs): ◎:1

### 3a. Interval characterization

| Property | [1..12] | [15..29] |
|----------|———————--|————————--|
| Pairs | 12 | 15 |
| ○ Kun | 4 | 2 |
| ◎ KanLi | 7 | 8 |
| ● Qian | 1 | 5 |
| Total 互 | 30 | 43 |
| Mean 互 | 2.73 | 3.07 |
| H-kernel rate | 55% | 50% |

Basin sequences:

- IV1: `○◎○◎◎●◎◎○◎○◎`
- IV2: `●●◎◎◎○●◎◎●◎◎●◎○`

Component sequences:

- IV1: `ABABBABBABAB`
- IV2: `AABBBAABBABBABA`

### 3b. Skeleton as basin-transition gates

- **pair 0 (Qian/Kun):** START→[●|○]→○
- **pair 13 (Yi/Da Guo):** ◎→[○|●]→○
- **pair 14 (Kan/Li):** ●→[○|●]→●
- **pair 30 (Zhong Fu/Xiao Guo):** ○→[○|●]→◎

## Part 4: Composite Timeline

| Pos | Pair | Basin | Comp | Entry 互 | Exit 互 | Skel | Interval |
|-----|------|-------|------|---------|--------|------|----------|
| 0 | Qian/Kun | ● | A | Qian ☰/Qian ☰ | Kun ☷/Kun ☷ | **Y** | SKEL |
| 1 | Zhun/Meng | ○ | A | Kun ☷/Zhen ☳ | Gen ☶/Kun ☷ |  | [1..12] |
| 2 | Xu/Song | ◎ | B | Xun ☴/Li ☲ | Li ☲/Dui ☱ |  | [1..12] |
| 3 | Shi/Bi | ○ | A | Gen ☶/Kun ☷ | Kun ☷/Zhen ☳ |  | [1..12] |
| 4 | Xiao Chu/Lu | ◎ | B | Xun ☴/Li ☲ | Li ☲/Dui ☱ |  | [1..12] |
| 5 | Tai/Pi | ◎ | B | Xun ☴/Gen ☶ | Zhen ☳/Dui ☱ |  | [1..12] |
| 6 | Tong Ren/Da You | ● | A | Dui ☱/Qian ☰ | Qian ☰/Xun ☴ |  | [1..12] |
| 7 | Qian/Yu | ◎ | B | Kan ☵/Gen ☶ | Zhen ☳/Kan ☵ |  | [1..12] |
| 8 | Sui/Gu | ◎ | B | Zhen ☳/Dui ☱ | Xun ☴/Gen ☶ |  | [1..12] |
| 9 | Lin/Guan | ○ | A | Gen ☶/Kun ☷ | Kun ☷/Zhen ☳ |  | [1..12] |
| 10 | Shi He/Bi | ◎ | B | Zhen ☳/Kan ☵ | Kan ☵/Gen ☶ |  | [1..12] |
| 11 | Bo/Fu | ○ | A | Kun ☷/Kun ☷ | Kun ☷/Kun ☷ |  | [1..12] |
| 12 | Wu Wang/Da Chu | ◎ | B | Zhen ☳/Dui ☱ | Xun ☴/Gen ☶ |  | [1..12] |
| 13 | Yi/Da Guo | ○ | A | Kun ☷/Kun ☷ | Qian ☰/Qian ☰ | **Y** | SKEL |
| 14 | Kan/Li | ○ | A | Gen ☶/Zhen ☳ | Dui ☱/Xun ☴ | **Y** | SKEL |
| 15 | Xian/Heng | ● | A | Dui ☱/Qian ☰ | Qian ☰/Xun ☴ |  | [15..29] |
| 16 | Dun/Da Zhuang | ● | A | Dui ☱/Qian ☰ | Qian ☰/Xun ☴ |  | [15..29] |
| 17 | Jin/Ming Yi | ◎ | B | Zhen ☳/Kan ☵ | Kan ☵/Gen ☶ |  | [15..29] |
| 18 | Jia Ren/Kui | ◎ | B | Kan ☵/Li ☲ | Li ☲/Kan ☵ |  | [15..29] |
| 19 | Jian/Xie | ◎ | B | Kan ☵/Li ☲ | Li ☲/Kan ☵ |  | [15..29] |
| 20 | Sun/Yi | ○ | A | Gen ☶/Kun ☷ | Kun ☷/Zhen ☳ |  | [15..29] |
| 21 | Guai/Gou | ● | A | Qian ☰/Qian ☰ | Qian ☰/Qian ☰ |  | [15..29] |
| 22 | Cui/Sheng | ◎ | B | Zhen ☳/Dui ☱ | Xun ☴/Gen ☶ |  | [15..29] |
| 23 | Kun/Jing | ◎ | B | Li ☲/Dui ☱ | Xun ☴/Li ☲ |  | [15..29] |
| 24 | Ge/Ding | ● | A | Dui ☱/Qian ☰ | Qian ☰/Xun ☴ |  | [15..29] |
| 25 | Zhen/Gen | ◎ | B | Zhen ☳/Kan ☵ | Kan ☵/Gen ☶ |  | [15..29] |
| 26 | Jian/Gui Mei | ◎ | B | Kan ☵/Li ☲ | Li ☲/Kan ☵ |  | [15..29] |
| 27 | Feng/Lu | ● | A | Dui ☱/Xun ☴ | Dui ☱/Xun ☴ |  | [15..29] |
| 28 | Xun/Dui | ◎ | B | Xun ☴/Li ☲ | Li ☲/Dui ☱ |  | [15..29] |
| 29 | Huan/Jie | ○ | A | Gen ☶/Zhen ☳ | Gen ☶/Zhen ☳ |  | [15..29] |
| 30 | Zhong Fu/Xiao Guo | ○ | A | Gen ☶/Zhen ☳ | Dui ☱/Xun ☴ | **Y** | SKEL |
| 31 | Ji Ji/Wei Ji | ◎ | B | Kan ☵/Li ☲ | Li ☲/Kan ☵ |  | [31..31] |

### Dimensional correlations

**Component ↔ Basin:**

- Comp A: ○:9, ●:7 (n=16)
- Comp B: ◎:16 (n=16)

**Interval ↔ Component:**

- SKEL: A:4
- [1..12]: A:5, B:7
- [15..29]: A:7, B:8
- [31..31]: B:1

## Key Findings

### 1. Bipartite structure IS basin structure

The d≤1 bipartite split is **perfectly determined by basin type**: Component A = all Kun ○ + Qian ● pairs (polar), Component B = all KanLi ◎ pairs (center). This is not a coincidence — at 互 distance ≤1, KanLi pairs only connect to other KanLi pairs, and polar pairs only connect to other polar pairs. The bipartite structure is the basin structure collapsed to two categories: polar vs center.

All basin-consistent orderings produce exactly 19 component switches (std=0.0). The bipartite traversal adds no information beyond what the basin sequence already encodes.

### 2. Component-crossing ≈ basin-crossing

Agreement rate: 94%. 
The only disagreements (2 bridges) occur at Kun↔Qian transitions — these cross basins but stay in Component A (the polar component). The d≤1 threshold graph reveals that the 3-basin system (○/◎/●) has a deeper 2-fold structure: polar (Kun+Qian) vs center (KanLi). In 互-space, the two poles are closer to each other than either is to the center.

### 3. 互-graph walk properties

16/16 互 values are visited. 
29 distinct edges used in 31 transitions. 
2 edges are reused, meaning the walk is not a simple path — it revisits some 互 connections.

### 4. 互-value spacing is uneven

Mean gap variance: 22.7. Fibers are not evenly spaced — pairs sharing the same entry-互 cluster together in the sequence rather than being uniformly distributed.

### 5. Skeleton intervals create asymmetric halves

Interval [1..12] has 12 pairs; [15..29] has 15 pairs. 
The basin distributions show a **chiastic pattern**: IV1 is Kun-heavy (4 ○ vs 1 ●), IV2 is Qian-heavy (2 ○ vs 5 ●). Both intervals are dominated by KanLi (7 and 8 ◎). The first half of KW breathes toward yin (Kun), the second half toward yang (Qian), with KanLi as the constant mediating center.

The skeleton cluster at positions 13-14 (Yi/Da Guo, Kan/Li) divides the sequence near the midpoint. These are the only adjacent skeleton pairs, creating a structural hinge. Both are Kun-entry/Qian-exit (○→●), functioning as a pole-inversion gate.

### 6. Composite view

The three lenses reveal a coherent architecture:

- **Basin/component:** The 3-basin system has a deeper 2-fold structure (polar vs center). KW alternates between these with 19/31 switches.

- **互-graph:** All 16 互 values are visited, with 29/31 distinct edge usages. The walk nearly avoids self-intersection, suggesting near-maximal coverage.

- **Skeleton intervals:** The 4 skeleton pairs divide the sequence into two main intervals with chiastic basin structure (first half Kun-heavy, second half Qian-heavy). The mid-sequence skeleton cluster (13-14) is the structural hinge.

- **These constraints are not independent** — basin determines component, skeleton position determines interval, and the 互-graph walk is constrained by both. But together they reveal that KW is a **structured traversal of algebraic space** with near-optimal coverage, chiastic symmetry, and basin-mediated breathing.
