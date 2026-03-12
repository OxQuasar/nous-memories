# KW Sequence Ordering — Monte Carlo Comparison

**Monte Carlo samples:** 50,000 valid orderings
**Acceptance rate:** 27.37% (182,706 total attempts)
**Constraints:** Fixed endpoints (Qian/Kun at 0, JiJi/WeiJi at 31) + Z₅×Z₅ anti-clustering

## Metric Comparison

| Metric | KW | MWD | Null Mean | Null Std | KW %ile | KW z-score | Flag |
|--------|-----|-----|-----------|----------|---------|------------|------|
| basin_clustering | 0.2903 | 0.1935 | 0.3650 | 0.0798 | 18.2% | -0.94 |  |
| bridge_hamming_mean | 2.9355 | 3.0000 | 3.1013 | 0.2010 | 20.9% | -0.82 |  |
| bridge_hamming_max | 6.0000 | 5.0000 | 5.2805 | 0.4889 | 85.0% | +1.47 |  |
| orbit_unique_edges | 0.4286 | 0.3929 | 0.4287 | 0.0362 | 49.1% | -0.00 |  |
| orbit_oneway_frac | 0.9091 | 0.7059 | 0.7294 | 0.1002 | 98.3% | +1.79 | • Notable |
| complement_distance_median | 6.0000 | 5.0000 | 9.2255 | 2.6185 | 11.1% | -1.23 |  |
| complement_distance_mean | 7.9167 | 5.6667 | 10.2884 | 1.8393 | 10.4% | -1.29 |  |
| split15_basin_balance | 8.0000 | 2.0000 | 6.8209 | 3.3128 | 65.8% | +0.36 |  |
| yang_total_first_half | 86.0000 | 88.0000 | 90.1085 | 5.9887 | 25.2% | -0.69 |  |
| basin_run_count | 26.0000 | 30.0000 | 24.8296 | 2.4608 | 67.1% | +0.48 |  |
| basin_run_mean_length | 2.4615 | 2.1333 | 2.6041 | 0.2703 | 32.9% | -0.53 |  |
| torus_step_mean | 2.4444 | 2.5079 | 2.5576 | 0.0861 | 9.5% | -1.31 |  |

## Complement Pair Map

### Self-complementary pairs (8)

| Pair # | h1 | h2 | Basin |
|--------|----|----|-------|
| 0 | 63 (Qian) | 0 (Kun) | Qian |
| 5 | 7 (Tai) | 56 (Pi) | KanLi |
| 8 | 25 (Sui) | 38 (Gu) | KanLi |
| 13 | 33 (Yi) | 30 (Da Guo) | Kun |
| 14 | 18 (Kan) | 45 (Li) | Kun |
| 26 | 52 (Jian) | 11 (Gui Mei) | KanLi |
| 30 | 51 (Zhong Fu) | 12 (Xiao Guo) | Kun |
| 31 | 21 (Ji Ji) | 42 (Wei Ji) | KanLi |

### Complement orbits (12 pairs)

| Pair A | Pair B | Distance |
|--------|--------|----------|
| 18 (Jia Ren/Kui) | 19 (Jian/Xie) | 1 |
| 27 (Feng/Lu) | 29 (Huan/Jie) | 2 |
| 3 (Shi/Bi) | 6 (Tong Ren/Da You) | 3 |
| 4 (Xiao Chu/Lu) | 7 (Qian/Yu) | 3 |
| 25 (Zhen/Gen) | 28 (Xun/Dui) | 3 |
| 15 (Xian/Heng) | 20 (Sun/Yi) | 5 |
| 9 (Lin/Guan) | 16 (Dun/Da Zhuang) | 7 |
| 11 (Bo/Fu) | 21 (Guai/Gou) | 10 |
| 12 (Wu Wang/Da Chu) | 22 (Cui/Sheng) | 10 |
| 10 (Shi He/Bi) | 23 (Kun/Jing) | 13 |
| 2 (Xu/Song) | 17 (Jin/Ming Yi) | 15 |
| 1 (Zhun/Meng) | 24 (Ge/Ding) | 23 |

## Basin Pairing Verification

**4 pairs have mismatched basins** (palindromic complement pairs):

| Pair # | h1 | h2 | Basin(h1) | Basin(h2) |
|--------|----|----|-----------|-----------|
| 0 | 63 | 0 | Qian | Kun |
| 13 | 33 | 30 | Kun | Qian |
| 14 | 18 | 45 | Kun | Qian |
| 30 | 51 | 12 | Kun | Qian |

Basin is computed from h1 of each pair.

## Summary

No metrics fall below 1st or above 99th percentile.

### Interpretation

These metrics test whether the KW pair *ordering* is special,
given that the pairing rule and anti-clustering constraint are already satisfied.
Discriminating metrics point to additional structure beyond the known constraints.

---

## Joint Analysis

### Omnibus Statistic (Σz²)

KW's sum of squared z-scores across all 12 metrics: **12.95**

| Statistic | Value |
|-----------|-------|
| KW Σz² | 12.95 |
| Null mean Σz² | 12.00 |
| Null std Σz² | 6.38 |
| KW percentile | 65.0% |
| KW z-score of Σz² | +0.15 |

KW is **not jointly unusual** — metric deviations are within normal joint variation.

Per-metric z-scores feeding the omnibus:

| Metric | z | z² |
|--------|---|------|
| basin_clustering | -0.94 | 0.88 |
| bridge_hamming_mean | -0.82 | 0.68 |
| bridge_hamming_max | +1.47 | 2.17 |
| orbit_unique_edges | -0.00 | 0.00 |
| orbit_oneway_frac | +1.79 | 3.22 |
| complement_distance_median | -1.23 | 1.52 |
| complement_distance_mean | -1.29 | 1.66 |
| split15_basin_balance | +0.36 | 0.13 |
| yang_total_first_half | -0.69 | 0.47 |
| basin_run_count | +0.48 | 0.23 |
| basin_run_mean_length | -0.53 | 0.28 |
| torus_step_mean | -1.31 | 1.73 |

### Triple Joint Test

Simultaneous threshold on the three most notable single metrics:

- **orbit_oneway_frac** >= KW value
- **torus_step_mean** <= KW value
- **complement_distance_mean** <= KW value

| Statistic | Value |
|-----------|-------|
| Null samples meeting all three | 7 / 50,000 |
| Joint fraction | 0.0001 (0.01%) |

**The triple conjunction is rare** — only 0.01% of null samples match.
This suggests weak but real joint structure in the KW ordering.

### Pairwise Correlations (Notable Metrics)

| Metric A | Metric B | Pearson r |
|----------|----------|-----------|
| orbit_oneway_frac | complement_distance_mean | +0.068 |
| orbit_oneway_frac | torus_step_mean | +0.013 |
| torus_step_mean | complement_distance_mean | -0.011 |

Notable metrics are **approximately independent** in the null — the joint test captures genuinely multi-dimensional information.
