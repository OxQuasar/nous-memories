# Phase 6: Cross-Model Robustness

3 models, 10000 null permutations, 1000 Mantel permutations.

## Summary Table

| Metric | bge-m3 | e5-large | labse |
|--------|--------:|--------:|--------:|
| Dim | 1024 | 1024 | 768 |
| Algebraic R² | 0.1096 | 0.1082 | 0.1075 |
| Raw complement cos | +0.8179 | +0.9624 | +0.6397 |
| Resid complement cos | -0.2013 | -0.1753 | -0.2154 |
| Anti-corr pairs (/32) | 28 | 27 | 28 |
| Eff dim (90%) | 31 | 31 | 28 |
| PC1 var | 0.073 | 0.062 | 0.120 |
| Participation ratio | 18.4 | 19.5 | 14.9 |
| Mantel r | -0.0967 | -0.1121 | -0.0657 |
| Mantel p | 0.0000 | 0.0000 | 0.0060 |
| Bridge KW mean | 0.97388 | 0.98673 | 0.98507 |
| Bridge %ile | 5.6 | 13.2 | 22.3 |
| Bridge z | -1.59 | -1.11 | -0.77 |

## Exception Sets (complement pairs with residual cosine ≥ 0)

### bge-m3 (4 pairs)
- Shi(2)↔Tong Ren(61): +0.01105
- Sheng(6)↔Wu Wang(57): +0.07281
- Tai(7)↔Pi(56): +0.00730
- Ge(29)↔Meng(34): +0.03203

### e5-large (5 pairs)
- Shi(2)↔Tong Ren(61): +0.02321
- Sheng(6)↔Wu Wang(57): +0.05051
- Tai(7)↔Pi(56): +0.02676
- Zhun(17)↔Ding(46): +0.01200
- Ge(29)↔Meng(34): +0.03055

### labse (4 pairs)
- Sheng(6)↔Wu Wang(57): +0.13069
- Xiao Guo(12)↔Zhong Fu(51): +0.09687
- Feng(13)↔Huan(50): +0.02800
- Zhun(17)↔Ding(46): +0.03958

## Cross-Model Concordance

### Per-pair complement cosine (Spearman ρ)

- bge-m3 ↔ e5-large: ρ=+0.9611 (p=0.0000)
- bge-m3 ↔ labse: ρ=+0.8629 (p=0.0000)
- e5-large ↔ labse: ρ=+0.8211 (p=0.0000)

### Exception set overlap (Jaccard)

- bge-m3 ↔ e5-large: 0.800
- bge-m3 ↔ labse: 0.143
- e5-large ↔ labse: 0.286
