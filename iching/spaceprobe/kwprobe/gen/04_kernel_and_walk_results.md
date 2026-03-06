# Kernel Independence + Transition-Walk Reconstruction

## Part 1: Kernel Independence from Basin Crossing

**Question:** When KW chooses a basin-crossing pair at sub-optimal bridges, does H-kernel come 'for free' (redundant), or does it carry independent information?

### H-kernel rate by crossing type

| Category | Count | H-kernel | Rate |
|----------|-------|----------|------|
| Basin-crossing options | 206 | 105 | 51.0% |
| Same-basin options | 111 | 50 | 45.0% |

### Per-bridge detail

| Bridge | Avail | Cross (H%) | Same (H%) | KW chose |
|--------|-------|-----------|----------|----------|
| 1→2 | 30 | 22 (55%) | 8 (38%) | cross H |
| 2→3 | 29 | 14 (50%) | 15 (47%) | cross H |
| 3→4 | 28 | 21 (52%) | 7 (29%) | cross H |
| 4→5 | 27 | 13 (46%) | 14 (43%) | same ¬H |
| 5→6 | 26 | 13 (54%) | 13 (54%) | cross ¬H |
| 6→7 | 25 | 20 (40%) | 5 (60%) | cross H |
| 9→10 | 22 | 16 (50%) | 6 (17%) | cross H |
| 11→12 | 20 | 15 (53%) | 5 (80%) | cross H |
| 12→13 | 19 | 10 (60%) | 9 (56%) | cross H |
| 13→14 | 18 | 13 (62%) | 5 (40%) | cross H |
| 16→17 | 15 | 12 (42%) | 3 (33%) | cross H |
| 18→19 | 13 | 6 (67%) | 7 (57%) | same H |
| 20→21 | 11 | 9 (44%) | 2 (0%) | cross ¬H |
| 21→22 | 10 | 8 (62%) | 2 (50%) | cross H |
| 22→23 | 9 | 4 (75%) | 5 (40%) | same ¬H |
| 23→24 | 8 | 4 (25%) | 4 (50%) | cross H |
| 24→25 | 7 | 6 (33%) | 1 (0%) | cross H |

### Verdict: **INDEPENDENT**

H-kernel rate among basin-crossers is only 51% (vs 45% for same-basin). Crossing basins does NOT automatically give H-kernel. KW's preference for H-kernel carries information beyond basin-crossing.
 Among 14 bridges with multiple basin-crossing options, KW chose the H-kernel one in 12 cases.

## Part 2: Cost Gradient — Structural or Artifactual?

| Metric | KW | Random mean | Random std |
|--------|-----|-----------|-----------|
| First-half mean (bridges 0-15) | 2.56 | 3.06 | 0.37 |
| Second-half mean (bridges 16-30) | 2.93 | 3.06 | 0.38 |
| Gradient (first − second) | -0.37 | -0.00 | 0.53 |
| KW gradient percentile | 25.0% | — | — |

Random orderings show no systematic gradient (-0.00 ≈ 0). 
KW's gradient of -0.37 is at the 25.0th percentile — **within normal range** for random orderings. The apparent cost gradient is largely a depletion artifact.

**Important distinction:** Round 1 found 'sub-optimal early, optimal late' — meaning early bridges have more *locally sub-optimal* choices (choosing d=3 when d=0 exists). But the *absolute* d_互 values are actually lower in the first half (2.56 vs 2.93). These are compatible: early bridges pick 'bad' options from a richer pool (many d=0 alternatives exist but are skipped), while late bridges pick 'good' options from a depleted pool (fewer alternatives, so KW's choice is closer to the minimum).

## Part 3: Transition-Walk Reconstruction

Score-based greedy walk from pair 0, choosing highest-scoring available pair.

### Results summary

| Method | Transitions matched | Positions matched | Total 互 weight |
|--------|-------------------|------------------|----------------|
| C: α=1,β=1 | 7/31 | 6/32 | 45 |
| B: α=1 | 7/31 | 4/32 | 35 |
| E: δ=1 | 7/31 | 4/32 | 35 |
| F: α=1,γ=0,β=0 | 7/31 | 4/32 | 35 |
| B: α=2 | 5/31 | 2/32 | 65 |
| E: δ=2 | 5/31 | 2/32 | 65 |
| C: α=1,β=2 | 4/31 | 2/32 | 57 |
| C: α=1,β=3 | 4/31 | 2/32 | 57 |
| C: α=1,β=5 | 4/31 | 2/32 | 57 |
| C: α=1,β=8 | 4/31 | 1/32 | 58 |
| A: 互 only | 3/31 | 6/32 | 29 |
| D: γ=0.5 | 2/31 | 4/32 | 36 |
| D: γ=1 | 1/31 | 2/32 | 42 |
| B: α=3 | 1/31 | 2/32 | 77 |
| B: α=5 | 1/31 | 2/32 | 77 |
| B: α=8 | 1/31 | 2/32 | 77 |
| B: α=13 | 1/31 | 2/32 | 77 |
| E: δ=3 | 1/31 | 2/32 | 77 |
| E: δ=5 | 1/31 | 2/32 | 77 |
| E: δ=8 | 1/31 | 2/32 | 77 |
| KW actual | 31/31 | 32/32 | 85 |

### Score F grid search (top 15)

| α | γ | β | Matches | Positions | Weight |
|---|---|---|---------|-----------|--------|
| 1 | 0 | 1 | 7/31 | 6/32 | 45 |
| 1 | 0 | 0 | 7/31 | 4/32 | 35 |
| 4 | 0 | 1 | 5/31 | 5/32 | 88 |
| 8 | 0 | 1 | 5/31 | 5/32 | 88 |
| 2 | 0 | 0 | 5/31 | 2/32 | 65 |
| 1 | 0 | 2 | 4/31 | 2/32 | 57 |
| 1 | 0 | 4 | 4/31 | 2/32 | 57 |
| 1 | 0 | 8 | 4/31 | 1/32 | 58 |
| 1 | 2 | 4 | 3/31 | 4/32 | 103 |
| 2 | 2 | 2 | 3/31 | 3/32 | 107 |
| 0 | 0 | 1 | 3/31 | 2/32 | 38 |
| 0 | 1 | 2 | 3/31 | 2/32 | 60 |
| 2 | 1 | 0 | 3/31 | 2/32 | 94 |
| 4 | 1 | 0 | 3/31 | 2/32 | 94 |
| 8 | 1 | 0 | 3/31 | 2/32 | 94 |

**Best reconstruction: C: α=1,β=1** — 7/31 transitions, 6/32 positions, weight 45.

## Part 4: Divergence Analysis

26 positions diverge (first half: 14, second half: 12).

| Position | KW pair | Recon pair | KW basin | Recon basin |
|----------|---------|------------|----------|-------------|
| 1 | Zhun/Meng | Bo/Fu | ○ | ○ |
| 2 | Xu/Song | Yi/Da Guo | ◎ | ○ |
| 3 | Shi/Bi | Guai/Gou | ○ | ● |
| 4 | Xiao Chu/Lu | Xu/Song | ◎ | ◎ |
| 5 | Tai/Pi | Kun/Jing | ◎ | ◎ |
| 6 | Tong Ren/Da You | Xiao Chu/Lu | ● | ◎ |
| 7 | Qian/Yu | Zhun/Meng | ◎ | ○ |
| 8 | Sui/Gu | Shi/Bi | ◎ | ○ |
| 9 | Lin/Guan | Qian/Yu | ○ | ◎ |
| 11 | Bo/Fu | Tai/Pi | ○ | ◎ |
| 12 | Wu Wang/Da Chu | Sui/Gu | ◎ | ◎ |
| 13 | Yi/Da Guo | Lin/Guan | ○ | ○ |
| 14 | Kan/Li | Wu Wang/Da Chu | ○ | ◎ |
| 15 | Xian/Heng | Kan/Li | ● | ○ |
| 16 | Dun/Da Zhuang | Feng/Lu | ● | ● |
| 17 | Jin/Ming Yi | Tong Ren/Da You | ◎ | ● |
| 18 | Jia Ren/Kui | Xian/Heng | ◎ | ● |
| 19 | Jian/Xie | Dun/Da Zhuang | ◎ | ● |
| 20 | Sun/Yi | Jin/Ming Yi | ○ | ◎ |
| 21 | Guai/Gou | Jia Ren/Kui | ● | ◎ |
| 22 | Cui/Sheng | Sun/Yi | ◎ | ○ |
| 23 | Kun/Jing | Jian/Xie | ◎ | ◎ |
| 24 | Ge/Ding | Cui/Sheng | ● | ◎ |
| 25 | Zhen/Gen | Jian/Gui Mei | ◎ | ◎ |
| 26 | Jian/Gui Mei | Zhen/Gen | ◎ | ◎ |
| 27 | Feng/Lu | Ge/Ding | ● | ● |

## Part 5: Compression

| Metric | Value |
|--------|-------|
| log₂(orderings from scoring rule) | 60.2 |
| log₂(basin-consistent orderings) | 75.0 |
| log₂(32!) | 117.7 |
| Bits eliminated | 57.5 / 117.7 |

Steps with ties: 24/31. Max tie size: 17. The scoring rule reduces 32! to ~2^60 orderings.

## Key Findings

1. **H-kernel is independent from basin-crossing.** H-kernel rate among basin-crossers: 51%, among same-basin: 45%. 
Basin-crossing and H-kernel carry partially independent information.

2. **Cost gradient:** KW's first-vs-second-half gradient is at the 25th percentile vs random. 
The apparent gradient is within normal depletion range.

3. **Best reconstruction: C: α=1,β=1** achieves 7/31 transitions (vs 3/31 互-only, 5/31 basin-constrained). 
The improvement is modest. No simple linear scoring of these features reconstructs KW.

4. **Compression:** The best scoring rule reduces the search space to 2^60 orderings (from 2^118), eliminating 57 bits. 
Substantial ambiguity remains at 24 tie-breaking steps.

### Reconstruction progression

| Round | Method | Matches |
|-------|--------|---------|
| 1 | Greedy 互 only | 3/31 |
| 3 | Basin-constrained greedy | 5/31 |
| 4 | C: α=1,β=1 | 7/31 |
| — | KW actual | 31/31 |
