# Hierarchical Generator Test: Basin Schedule + Local 互

**Hypothesis:** KW's pair ordering = macro basin schedule + micro 互 greedy.

## Part 1: Basin Sequence

Entry basin sequence: `● ○ ◎ ○ ◎ ◎ ● ◎ ◎ ○ ◎ ○ ◎ ○ ○ ● ● ◎ ◎ ◎ ○ ● ◎ ◎ ● ◎ ◎ ● ◎ ○ ○ ◎`

Basin counts: {'Qian': 7, 'Kun': 9, 'KanLi': 16}

### Run-length encoding (23 runs)

| Run | Basin | Start | Length | Pairs |
|-----|-------|-------|--------|-------|
| 0 | ● | 0 | 1 | Qian |
| 1 | ○ | 1 | 1 | Zhun |
| 2 | ◎ | 2 | 1 | Xu |
| 3 | ○ | 3 | 1 | Shi |
| 4 | ◎ | 4 | 2 | Xiao Chu, Tai |
| 5 | ● | 6 | 1 | Tong Ren |
| 6 | ◎ | 7 | 2 | Qian, Sui |
| 7 | ○ | 9 | 1 | Lin |
| 8 | ◎ | 10 | 1 | Shi He |
| 9 | ○ | 11 | 1 | Bo |
| 10 | ◎ | 12 | 1 | Wu Wang |
| 11 | ○ | 13 | 2 | Yi, Kan |
| 12 | ● | 15 | 2 | Xian, Dun |
| 13 | ◎ | 17 | 3 | Jin, Jia Ren, Jian |
| 14 | ○ | 20 | 1 | Sun |
| 15 | ● | 21 | 1 | Guai |
| 16 | ◎ | 22 | 2 | Cui, Kun |
| 17 | ● | 24 | 1 | Ge |
| 18 | ◎ | 25 | 2 | Zhen, Jian |
| 19 | ● | 27 | 1 | Feng |
| 20 | ◎ | 28 | 1 | Xun |
| 21 | ○ | 29 | 2 | Huan, Zhong Fu |
| 22 | ◎ | 31 | 1 | Ji Ji |

Run-level sequence: `● ○ ◎ ○ ◎ ● ◎ ○ ◎ ○ ◎ ○ ● ◎ ○ ● ◎ ● ◎ ● ◎ ○ ◎`

Run lengths: [1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 2, 1, 2, 1, 1, 2, 1] (mean: 1.39)

## Part 2: Within-Run 互 Optimality

| Run | Basin | Length | KW 互 | Min 互 | Percentile | Optimal? |
|-----|-------|--------|-------|--------|------------|----------|
| 0 | ● | 1 | — | — | — | — |
| 1 | ○ | 1 | — | — | — | — |
| 2 | ◎ | 1 | — | — | — | — |
| 3 | ○ | 1 | — | — | — | — |
| 4 | ◎ | 2 | 5 | 5 | 100.0% | ✓ |
| 5 | ● | 1 | — | — | — | — |
| 6 | ◎ | 2 | 1 | 1 | 100.0% | ✓ |
| 7 | ○ | 1 | — | — | — | — |
| 8 | ◎ | 1 | — | — | — | — |
| 9 | ○ | 1 | — | — | — | — |
| 10 | ◎ | 1 | — | — | — | — |
| 11 | ○ | 2 | 4 | 4 | 100.0% | ✓ |
| 12 | ● | 2 | 2 | 2 | 100.0% | ✓ |
| 13 | ◎ | 3 | 7 | 2 | 100.0% | ✗ |
| 14 | ○ | 1 | — | — | — | — |
| 15 | ● | 1 | — | — | — | — |
| 16 | ◎ | 2 | 5 | 5 | 100.0% | ✓ |
| 17 | ● | 1 | — | — | — | — |
| 18 | ◎ | 2 | 1 | 1 | 100.0% | ✓ |
| 19 | ● | 1 | — | — | — | — |
| 20 | ◎ | 1 | — | — | — | — |
| 21 | ○ | 2 | 0 | 0 | 50.0% | ✓ |
| 22 | ◎ | 1 | — | — | — | — |

**7/8 multi-pair runs are within-run 互-optimal.**

**Caveat:** 7/8 of these runs have only 2 pairs (trivially optimal when both orderings give the same weight). Only 1 run(s) have ≥3 pairs, providing a real test.
- Run 13 (◎, 3 pairs): **WORST ordering** (KW=7, min=2)

## Part 3: Basin-Constrained Reconstruction

Fix KW's basin assignment per position, then greedily assign pairs by 互 proximity.

| Variant | Transitions matched | Position matches | Total 互 weight |
|---------|-------------------|-----------------|----------------|
| Basin + greedy 互 | 5/31 | 6/32 | 59 |
| Basin + greedy 互 + lookahead | 5/31 | 6/32 | 59 |
| KW actual | 31/31 | 32/32 | 85 |

## Part 4: Basin Sequence Entropy

| Metric | Value |
|--------|-------|
| Basin-consistent orderings | 2^75.0 |
| Full search space (32!) | 2^117.7 |
| Compression from basin schedule | 42.6 bits |
| Remaining search fraction | 1.45e-13 |

The basin schedule reduces the search space by a factor of ~2^43, from 32! down to ~2^75 orderings.

## Part 5: All-Bridges Basin Analysis

| Bridge type | Count | Mean d_互 | Optimal rate | Near-optimal rate |
|-------------|-------|----------|-------------|-------------------|
| Same-basin | 10 | 2.30 | 3/10 | 7/10 |
| Cross-basin | 21 | 2.95 | 3/21 | 7/21 |

### Bridge detail

| Bridge | Exit | Entry | Type | d_互 | Min d | Optimal? |
|--------|------|-------|------|------|-------|----------|
| 0→1 | ○ | ○ | same | 1 | 0 | +1 |
| 1→2 | ○ | ◎ | **cross** | 3 | 0 | +3 |
| 2→3 | ◎ | ○ | **cross** | 3 | 0 | +3 |
| 3→4 | ○ | ◎ | **cross** | 3 | 1 | +2 |
| 4→5 | ◎ | ◎ | same | 5 | 0 | +5 |
| 5→6 | ◎ | ● | **cross** | 2 | 0 | +2 |
| 6→7 | ● | ◎ | **cross** | 3 | 1 | +2 |
| 7→8 | ◎ | ◎ | same | 1 | 0 | +1 |
| 8→9 | ◎ | ○ | **cross** | 2 | 1 | +1 |
| 9→10 | ○ | ◎ | **cross** | 3 | 1 | +2 |
| 10→11 | ◎ | ○ | **cross** | 2 | 1 | +1 |
| 11→12 | ○ | ◎ | **cross** | 3 | 0 | +3 |
| 12→13 | ◎ | ○ | **cross** | 3 | 1 | +2 |
| 13→14 | ● | ○ | **cross** | 4 | 0 | +4 |
| 14→15 | ● | ● | same | 1 | 0 | +1 |
| 15→16 | ● | ● | same | 2 | 1 | +1 |
| 16→17 | ● | ◎ | **cross** | 3 | 1 | +2 |
| 17→18 | ◎ | ◎ | same | 1 | 1 | ✓ |
| 18→19 | ◎ | ◎ | same | 6 | 1 | +5 |
| 19→20 | ◎ | ○ | **cross** | 2 | 1 | +1 |
| 20→21 | ○ | ● | **cross** | 5 | 1 | +4 |
| 21→22 | ● | ◎ | **cross** | 3 | 1 | +2 |
| 22→23 | ◎ | ◎ | same | 5 | 1 | +4 |
| 23→24 | ◎ | ● | **cross** | 3 | 0 | +3 |
| 24→25 | ● | ◎ | **cross** | 3 | 1 | +2 |
| 25→26 | ◎ | ◎ | same | 1 | 1 | ✓ |
| 26→27 | ◎ | ● | **cross** | 3 | 3 | ✓ |
| 27→28 | ● | ◎ | **cross** | 4 | 3 | +1 |
| 28→29 | ◎ | ○ | **cross** | 2 | 2 | ✓ |
| 29→30 | ○ | ○ | same | 0 | 0 | ✓ |
| 30→31 | ● | ◎ | **cross** | 3 | 3 | ✓ |

## Part 6: Basin Transition Direction

### Transition matrix (at cross-basin bridges)

| From \ To | Kun ○ | KanLi ◎ | Qian ● |
|----------|-------|---------|--------|
| ○ Kun | — | 4 | 1 |
| ◎ KanLi | 6 | — | 3 |
| ● Qian | 1 | 6 | — |

Transitions through center (KanLi): **19/21** (90%)

Direct pole-to-pole (Kun↔Qian): 2/21

### Transition sequence

```
Bridge  1: ○→◎
Bridge  2: ◎→○
Bridge  3: ○→◎
Bridge  5: ◎→●
Bridge  6: ●→◎
Bridge  8: ◎→○
Bridge  9: ○→◎
Bridge 10: ◎→○
Bridge 11: ○→◎
Bridge 12: ◎→○
Bridge 13: ●→○
Bridge 16: ●→◎
Bridge 19: ◎→○
Bridge 20: ○→●
Bridge 21: ●→◎
Bridge 23: ◎→●
Bridge 24: ●→◎
Bridge 26: ◎→●
Bridge 27: ●→◎
Bridge 28: ◎→○
Bridge 30: ●→◎
```

## Part 7: Reconstruction Quality Summary

| Method | Transitions matched | Total 互 weight |
|--------|-------------------|----------------|
| Random (mean of 10000) | 1.0/31 | 95 |
| Greedy 互 only | 3/31 | 29 |
| Basin-constrained greedy 互 | 5/31 | 59 |
| Basin-constrained greedy 互 + lookahead | 5/31 | 59 |
| KW actual | 31/31 | 85 |

**Basin constraint improves matches from 3 → 5** (+2 without lookahead), **5** (+2 with lookahead).

The basin schedule alone is insufficient — it provides modest improvement over unconstrained greedy but falls well short of full reconstruction.

## Part 8: What Remains Unexplained

After basin-constrained reconstruction (lookahead), **26 of 32 positions diverge** from KW.

Divergence distribution: first half 14, second half 12.

### Divergence detail

| Position | KW pair | Recon pair | Required basin |
|----------|---------|------------|----------------|
| 1 | Zhun/Meng | Bo/Fu | ○ |
| 2 | Xu/Song | Qian/Yu | ◎ |
| 3 | Shi/Bi | Yi/Da Guo | ○ |
| 4 | Xiao Chu/Lu | Xu/Song | ◎ |
| 5 | Tai/Pi | Kun/Jing | ◎ |
| 6 | Tong Ren/Da You | Guai/Gou | ● |
| 7 | Qian/Yu | Xiao Chu/Lu | ◎ |
| 9 | Lin/Guan | Shi/Bi | ○ |
| 10 | Shi He/Bi | Wu Wang/Da Chu | ◎ |
| 11 | Bo/Fu | Lin/Guan | ○ |
| 12 | Wu Wang/Da Chu | Jia Ren/Kui | ◎ |
| 13 | Yi/Da Guo | Sun/Yi | ○ |
| 14 | Kan/Li | Zhun/Meng | ○ |
| 15 | Xian/Heng | Feng/Lu | ● |
| 16 | Dun/Da Zhuang | Tong Ren/Da You | ● |
| 17 | Jin/Ming Yi | Tai/Pi | ◎ |
| 18 | Jia Ren/Kui | Cui/Sheng | ◎ |
| 19 | Jian/Xie | Xun/Dui | ◎ |
| 20 | Sun/Yi | Kan/Li | ○ |
| 21 | Guai/Gou | Xian/Heng | ● |
| 22 | Cui/Sheng | Shi He/Bi | ◎ |
| 23 | Kun/Jing | Jian/Xie | ◎ |
| 24 | Ge/Ding | Dun/Da Zhuang | ● |
| 25 | Zhen/Gen | Jin/Ming Yi | ◎ |
| 27 | Feng/Lu | Ge/Ding | ● |
| 28 | Xun/Dui | Zhen/Gen | ◎ |

## Key Findings

1. **Basin sequence is highly fragmented:** 23 runs for 32 pairs (mean length 1.4). 15/23 runs are singletons. The basin schedule compresses the search space by 43 bits (from 2^118 to 2^75), but this compression is modest.

2. **Within-run optimality is vacuous.** 7/8 multi-pair runs are 互-optimal, but 7/8 are 2-pair runs where optimality is trivial. The sole 3-pair run (run 13: Jin, Jia Ren, Jian) has the **worst** possible ordering. The data neither supports nor refutes within-run 互 optimization because almost all runs are too short to test.

3. **Same-basin vs cross-basin bridges:** Same-basin bridges are slightly more optimal (3/10) vs cross-basin (3/21), but the mean d_互 is only moderately lower (2.3 vs 3.0). The separation is not as clean as the hierarchical model predicts.

4. **Basin transitions are center-mediated:** 19/21 cross-basin bridges involve KanLi (90%). Direct pole-to-pole (Kun↔Qian): only 2/21. KanLi functions as a transit hub between the poles.

5. **Reconstruction: basin + 互 greedy fails.** Only 5/31 transitions matched (vs 3/31 unconstrained, ~1/31 random). The improvement over unconstrained greedy is +2 transitions — the basin schedule provides minimal generative leverage.

6. **The hierarchical model is refuted.** The two-level decomposition (macro basin schedule + micro 互 greedy) does not reconstruct KW. The fundamental problem: basin runs are too short (mean 1.4) for within-run optimization to matter. KW alternates basins almost every pair, which means the ordering principle operates *at* the basin transition level, not *within* basin blocks. The generator is not hierarchical — it's interleaved.

### What this tells us

The basin sequence is a *consequence* of the ordering, not its generator. KW doesn't build runs of same-basin pairs and then order within runs. Instead, it weaves basins together in a rapid-alternation pattern (23 runs in 32 positions). The ordering principle must simultaneously determine both which basin to visit and which specific pair to place — these are not separable decisions.

The next question: what interleaving rule produces this specific basin sequence while maintaining the observed 互 continuity (12.7th percentile)?
