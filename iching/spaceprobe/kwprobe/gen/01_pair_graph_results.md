# Pair Graph & Greedy 互-Continuity Reconstruction

## Search Space

Each KW pair has two members in a specific order (orientation).
A bridge goes from pair_k's member 2 → pair_{k+1}'s member 1.

- **Full search space:** 32! × 2^32 ≈ 1.1 × 10^45 (pair order × orientations)
- **Orientations are meaningful** (developmental priority, p = 2.3 × 10⁻¹⁰)
- **Round 1:** Fix orientations to KW's choices, explore pair ordering only (32! ≈ 2.6 × 10^35)

## 1. Pair Graph

Edge weight: `hamming6(hugua(pair_i[1]), hugua(pair_j[0]))` — bridge 互 distance.

| Metric | Value |
|--------|-------|
| Edges | 992 (32×31) |
| Weight range | 0–6 |
| Mean weight | 3.060 |
| Asymmetric edges | 80/496 |
| Weight distribution | {0: 34, 1: 128, 2: 194, 3: 256, 4: 200, 5: 128, 6: 52} |

## 2. KW Actual Path

Total 互 weight: **85** over 31 bridges (mean 2.74)

| Bridge | From | To | d_互 |
|--------|------|----|------|
| 0→1 | Qian/Kun | Zhun/Meng | 1 |
| 1→2 | Zhun/Meng | Xu/Song | 3 |
| 2→3 | Xu/Song | Shi/Bi | 3 |
| 3→4 | Shi/Bi | Xiao Chu/Lu | 3 |
| 4→5 | Xiao Chu/Lu | Tai/Pi | 5 |
| 5→6 | Tai/Pi | Tong Ren/Da You | 2 |
| 6→7 | Tong Ren/Da You | Qian/Yu | 3 |
| 7→8 | Qian/Yu | Sui/Gu | 1 |
| 8→9 | Sui/Gu | Lin/Guan | 2 |
| 9→10 | Lin/Guan | Shi He/Bi | 3 |
| 10→11 | Shi He/Bi | Bo/Fu | 2 |
| 11→12 | Bo/Fu | Wu Wang/Da Chu | 3 |
| 12→13 | Wu Wang/Da Chu | Yi/Da Guo | 3 |
| 13→14 | Yi/Da Guo | Kan/Li | 4 |
| 14→15 | Kan/Li | Xian/Heng | 1 |
| 15→16 | Xian/Heng | Dun/Da Zhuang | 2 |
| 16→17 | Dun/Da Zhuang | Jin/Ming Yi | 3 |
| 17→18 | Jin/Ming Yi | Jia Ren/Kui | 1 |
| 18→19 | Jia Ren/Kui | Jian/Xie | 6 |
| 19→20 | Jian/Xie | Sun/Yi | 2 |
| 20→21 | Sun/Yi | Guai/Gou | 5 |
| 21→22 | Guai/Gou | Cui/Sheng | 3 |
| 22→23 | Cui/Sheng | Kun/Jing | 5 |
| 23→24 | Kun/Jing | Ge/Ding | 3 |
| 24→25 | Ge/Ding | Zhen/Gen | 3 |
| 25→26 | Zhen/Gen | Jian/Gui Mei | 1 |
| 26→27 | Jian/Gui Mei | Feng/Lu | 3 |
| 27→28 | Feng/Lu | Xun/Dui | 4 |
| 28→29 | Xun/Dui | Huan/Jie | 2 |
| 29→30 | Huan/Jie | Zhong Fu/Xiao Guo | 0 |
| 30→31 | Zhong Fu/Xiao Guo | Ji Ji/Wei Ji | 3 |

Bridge distance distribution: {0: 1, 1: 5, 2: 6, 3: 13, 4: 2, 5: 3, 6: 1}

## 3. Random Baseline (100K pair-order shuffles)

| Metric | Value |
|--------|-------|
| KW total | 85 |
| Random mean | 94.9 |
| Random std | 8.2 |
| Random min | 57 |
| Random max | 133 |
| **KW percentile** | **12.74%** |

KW's pair ordering achieves lower total 互 weight than 87.3% of random orderings.

## 4. Greedy 互 Walk

### From pair 0 (Qian/Kun)

Total: **29** (KW: 85), percentile: 0.00%

Path: `[0, 11, 13, 21, 6, 27, 15, 5, 8, 2, 23, 4, 12, 7, 10, 18, 17, 19, 25, 26, 3, 1, 9, 14, 16, 24, 28, 22, 20, 29, 30, 31]`

### Best starting pair

| Rank | Start | Pair | Total 互 weight |
|------|-------|------|----------------|
| 1 | 14 | Kan/Li | 27 |
| 2 | 29 | Huan/Jie | 27 |
| 3 | 1 | Zhun/Meng | 28 |
| 4 | 2 | Xu/Song | 28 |
| 5 | 3 | Shi/Bi | 28 |
| 6 | 4 | Xiao Chu/Lu | 28 |
| 7 | 6 | Tong Ren/Da You | 28 |
| 8 | 8 | Sui/Gu | 28 |
| 9 | 9 | Lin/Guan | 28 |
| 10 | 12 | Wu Wang/Da Chu | 28 |

Best greedy (start=14): **27**, percentile: 0.00%

## 5. Threshold Graph

| d_max | Edges | Components | Mean out-deg | Min out-deg |
|-------|-------|------------|-------------|-------------|
| 0 | 34 | 14 | 1.1 | 0 |
| 1 | 162 | 2 | 5.1 | 3 |
| 2 | 356 | 1 | 11.1 | 7 |
| 3 | 612 | 1 | 19.1 | 15 |
| 4 | 812 | 1 | 25.4 | 23 |
| 5 | 940 | 1 | 29.4 | 27 |
| 6 | 992 | 1 | 31.0 | 31 |

## 6. Multi-Greedy with Constraint Stacking

| Method | Total 互 | KW transitions matched |
|--------|---------|----------------------|
| Greedy 互 only | 29 | 3/31 |
| Greedy 互 + basin tiebreak | 33 | 3/31 |
| Greedy 互 + basin + attractor frame | 37 | 3/31 |
| KW actual | 85 | 31/31 |

## 7. KW Local Optimality

| Class | Count | Description |
|-------|-------|-------------|
| Optimal | 6/31 | KW chose the minimum-distance pair |
| Near-optimal | 8/31 | Within 1 of minimum |
| Sub-optimal | 17/31 | >1 above minimum |

### Sub-optimal bridges

**Bridge 1→2:** KW chose Xu/Song (d=3), but d=0 was available:
- Pair 3 (Shi/Bi): d=0, basin=○
- Pair 9 (Lin/Guan): d=0, basin=○
- Pair 20 (Sun/Yi): d=0, basin=○

**Bridge 2→3:** KW chose Shi/Bi (d=3), but d=0 was available:
- Pair 23 (Kun/Jing): d=0, basin=◎

**Bridge 3→4:** KW chose Xiao Chu/Lu (d=3), but d=1 was available:
- Pair 11 (Bo/Fu): d=1, basin=○
- Pair 13 (Yi/Da Guo): d=1, basin=○
- Pair 14 (Kan/Li): d=1, basin=○
- Pair 29 (Huan/Jie): d=1, basin=○
- Pair 30 (Zhong Fu/Xiao Guo): d=1, basin=○

**Bridge 4→5:** KW chose Tai/Pi (d=5), but d=0 was available:
- Pair 23 (Kun/Jing): d=0, basin=◎

**Bridge 5→6:** KW chose Tong Ren/Da You (d=2), but d=0 was available:
- Pair 8 (Sui/Gu): d=0, basin=◎
- Pair 12 (Wu Wang/Da Chu): d=0, basin=◎
- Pair 22 (Cui/Sheng): d=0, basin=◎

**Bridge 6→7:** KW chose Qian/Yu (d=3), but d=1 was available:
- Pair 21 (Guai/Gou): d=1, basin=●
- Pair 27 (Feng/Lu): d=1, basin=●

**Bridge 9→10:** KW chose Shi He/Bi (d=3), but d=1 was available:
- Pair 11 (Bo/Fu): d=1, basin=○
- Pair 13 (Yi/Da Guo): d=1, basin=○
- Pair 14 (Kan/Li): d=1, basin=○
- Pair 29 (Huan/Jie): d=1, basin=○
- Pair 30 (Zhong Fu/Xiao Guo): d=1, basin=○

**Bridge 11→12:** KW chose Wu Wang/Da Chu (d=3), but d=0 was available:
- Pair 13 (Yi/Da Guo): d=0, basin=○

**Bridge 12→13:** KW chose Yi/Da Guo (d=3), but d=1 was available:
- Pair 28 (Xun/Dui): d=1, basin=◎

**Bridge 13→14:** KW chose Kan/Li (d=4), but d=0 was available:
- Pair 21 (Guai/Gou): d=0, basin=●

**Bridge 16→17:** KW chose Jin/Ming Yi (d=3), but d=1 was available:
- Pair 21 (Guai/Gou): d=1, basin=●
- Pair 27 (Feng/Lu): d=1, basin=●

**Bridge 18→19:** KW chose Jian/Xie (d=6), but d=1 was available:
- Pair 23 (Kun/Jing): d=1, basin=◎
- Pair 25 (Zhen/Gen): d=1, basin=◎

**Bridge 20→21:** KW chose Guai/Gou (d=5), but d=1 was available:
- Pair 29 (Huan/Jie): d=1, basin=○
- Pair 30 (Zhong Fu/Xiao Guo): d=1, basin=○

**Bridge 21→22:** KW chose Cui/Sheng (d=3), but d=1 was available:
- Pair 24 (Ge/Ding): d=1, basin=●

**Bridge 22→23:** KW chose Kun/Jing (d=5), but d=1 was available:
- Pair 28 (Xun/Dui): d=1, basin=◎

**Bridge 23→24:** KW chose Ge/Ding (d=3), but d=0 was available:
- Pair 28 (Xun/Dui): d=0, basin=◎

**Bridge 24→25:** KW chose Zhen/Gen (d=3), but d=1 was available:
- Pair 27 (Feng/Lu): d=1, basin=●

## Key Structural Findings

### The d=0 component structure
At threshold 0 (identical 互 bridges), the 32 pairs split into 14 components:
- **6 quartets** of 4 pairs each — these are 互-equivalence classes where pairs share identical outgoing/incoming 互 values
- **8 singletons** — pairs with unique 互 signatures

The quartets form natural groupings: {Qian, Bo, Yi, Guai} (attractor pairs), {Zhun, Shi, Lin, Sun} (Kun-basin), etc.

### The bipartite split at d=1
At threshold 1, the graph splits into exactly **2 equal components** of 16 pairs each:
- **Component A:** dominated by Kun ○ and Qian ● basin pairs
- **Component B:** dominated by KanLi ◎ basin pairs
This bipartition is a fundamental structural feature — the pair graph at low thresholds separates by basin type.

### Greedy diverges immediately from KW
Pure 互 greedy achieves total weight 29 (vs KW's 85) but matches only 3/31 KW transitions. Adding basin and attractor constraints doesn't help (still 3/31 matches). The greedy path optimizes 互 continuity ~3× better than KW but produces a completely different ordering.

### KW sacrifices 互 continuity systematically
Only 6/31 bridges are locally 互-optimal. The sub-optimal bridges cluster in the first half of the sequence (bridges 1–14), where KW consistently chooses pairs with d=3 when d=0 or d=1 is available. The last 6 bridges (26–31) are all optimal or near-optimal. **KW front-loads 互 cost and back-loads 互 continuity.**

### What constrains KW beyond 互?
At every sub-optimal bridge, KW's choice maintains the KW-number ordering (pairs appear in ascending KW number). This is the hexagram-number constraint: KW preserves a monotonic sweep through hexagram space while accepting 互 discontinuity. The question becomes: what determines the hexagram numbering such that when followed in order, the 互 continuity lands at the 12.7th percentile?

## Summary

1. **KW's 互 continuity is notable:** 12.7th percentile among random orderings.
2. **Greedy achieves 3× better 互 weight** but matches only 3/31 KW transitions — 互 is a soft constraint, not the ordering principle.
3. **Local optimality:** 6/31 optimal, 8/31 near-optimal, 17/31 sub-optimal.
4. **Optimality gradient:** Sub-optimal early, optimal late. KW's pair ordering converges toward 互 optimality at the sequence's end.
5. **Bipartite structure:** The d≤1 threshold graph splits into 2 equal components, separating basin types. This is a deep structural constraint on any 互-smooth ordering.
6. **The generative question remains open:** 互 continuity is a measurable property of KW but not its generator. The ordering principle likely involves multiple interlocking constraints — number-ordering, basin breathing, five-phase flow — with 互 continuity as an emergent consequence.
