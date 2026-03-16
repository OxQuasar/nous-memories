# Phase 7: Hamming-Thematic Anti-Correlation Deep Dive

## Test 1: Line-Level Mechanism (BGE-M3, Hamming-1 pairs)

192 Hamming-1 pairs: each differs at exactly one line position.

- Changed line mean cosine dist: **1.01996**
- Shared lines mean cosine dist: **1.02569**
- Hex centroid cosine dist: 1.07156
- Ratio changed/shared: **0.994**

### Per-position breakdown

| Position | Line | Changed | Shared | Hex dist | Ratio |
|----------|------|--------:|-------:|---------:|------:|
| 0 | 初 | 1.05084 | 1.03845 | 1.09588 | 1.012 |
| 1 | 二 | 0.99684 | 1.02049 | 1.02471 | 0.977 |
| 2 | 三 | 0.99486 | 1.00976 | 1.04246 | 0.985 |
| 3 | 四 | 1.03499 | 1.02591 | 1.07318 | 1.009 |
| 4 | 五 | 1.04123 | 1.03405 | 1.12016 | 1.007 |
| 5 | 上 | 1.00098 | 1.02551 | 1.07296 | 0.976 |

## Test 2: Position Dependence

| Position | Line | Overall | When changed | When shared | Δ |
|----------|------|--------:|------------:|-----------:|--:|
| 0 | 初 | 1.01540 | 1.01850 | 1.01220 | +0.00630 |
| 1 | 二 | 1.01575 | 1.01636 | 1.01513 | +0.00124 |
| 2 | 三 | 1.01567 | 1.01860 | 1.01266 | +0.00594 |
| 3 | 四 | 1.01547 | 1.01789 | 1.01298 | +0.00491 |
| 4 | 五 | 1.01572 | 1.01294 | 1.01859 | -0.00565 |
| 5 | 上 | 1.01554 | 1.01517 | 1.01592 | -0.00076 |

## Test 3: Trigram-Level Analysis

| Hamming | Share upper | Share lower | Neither | Overall |
|--------:|-----------:|-----------:|--------:|--------:|
| 1 | 1.05435 | 1.08877 | — | 1.07156 |
| 2 | 0.98575 | 0.98867 | 1.07101 | 1.03749 |
| 3 | 1.01867 | 0.94201 | 0.98728 | 0.98658 |
| 4 | — | — | 1.01507 | 1.01507 |
| 5 | — | — | 0.97339 | 0.97339 |
| 6 | — | — | 1.20130 | 1.20130 |

## Test 4: Hamming Distance Spectrum

| d | Mean cos dist |
|--:|--------------:|
| 1 | 1.07156 |
| 2 | 1.03749 |
| 3 | 0.98658 |
| 4 | 1.01507 |
| 5 | 0.97339 |
| 6 | 1.20130 (complements) |

- Pearson (d=1..5, excl complements): r=-0.1659 (p=1.04e-13)
- Pearson (d=1..6, incl complements): r=-0.0967 (p=1.37e-05)

### Hamming-5 by un-flipped position

| Kept pos | Line | Mean dist |
|---------:|------:|----------:|
| 0 | 初 | 0.97899 |
| 1 | 二 | 0.96029 |
| 2 | 三 | 0.89967 |
| 3 | 四 | 0.93173 |
| 4 | 五 | 1.01572 |
| 5 | 上 | 1.05393 |

## Test 5: Cross-Model Summary

| Metric | bge-m3 | e5-large | labse |
|--------|-------:|--------:|------:|
| d=1 dist | 1.07156 | 1.07327 | 1.06325 |
| d=2 dist | 1.03749 | 1.03803 | 1.04046 |
| d=3 dist | 0.98658 | 0.98604 | 0.98643 |
| d=4 dist | 1.01507 | 1.01618 | 1.01098 |
| d=5 dist | 0.97339 | 0.97347 | 0.98189 |
| d=6 dist (comp) | 1.20130 | 1.17531 | 1.21544 |
| Pearson (d=1..5) | -0.1659 | -0.1767 | -0.1227 |
| Pearson (d=1..6) | -0.0967 | -0.1121 | -0.0657 |
| Changed line dist | 1.01996 | 1.01954 | 1.01415 |
| Shared lines dist | 1.02569 | 1.02836 | 1.02730 |
| Ratio changed/shared | 0.994 | 0.991 | 0.987 |
