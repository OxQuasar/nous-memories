# Foundation Extraction Results (S1–S4)

## S1: Stock Phrase Analysis

**Marker frequencies in 384 line texts (爻辭):**
| Marker | Count | Prevalence |
|--------|-------|-----------|
| 吉 | 118 | 30.7% |
| 无咎 | 84 | 21.9% |
| 貞 | 71 | 18.5% |
| 凶 | 52 | 13.5% |
| 利 | 51 | 13.3% |
| 厲 | 26 | 6.8% |
| 吝 | 20 | 5.2% |
| 悔亡 | 18 | 4.7% |
| 悔 | 13 | 3.4% |
| 亨 | 8 | 2.1% |
| 咎 | 8 | 2.1% |
| 利貞 | 3 | 0.8% |
| 利涉大川 | 2 | 0.5% |
| 元亨利貞 | 0 | — |
| 元亨 | 0 | — |

**Key finding:** 元亨利貞 and 元亨 never appear in 爻辭 — they are exclusively 卦辭 vocabulary.

**PCA:** 8 components for 90% variance. PC1: 吉(+) vs 无咎(−). PC2: 无咎(+) vs 凶(−). PC3: 貞(+). The marker system has ~8 latent dimensions — not reducible to a simple good/bad axis.

**Positional bias (significant):**
- 吉: peaks at lines 2 and 5 (central positions), trough at line 3. χ²=17.1, p=0.004
- 凶: peaks at lines 3 and 6 (extremes), trough at line 5. χ²=17.2, p=0.004
- Other markers: no significant positional bias

**Marker families:**
- k=2 split: {无咎, 亨, 利} vs {everything else} — a "neutral/enabling" vs "valenced" partition
- k=3 split: {无咎, 亨, 利} | {悔亡, 吉, 貞} | {凶, 悔, 吝, 咎, 厲, 利涉大川, 利貞}
  - Group 1: enabling/neutral
  - Group 2: favorable outcomes  
  - Group 3: unfavorable/cautionary

## S2: 卦辭 Clustering

**Silhouette scores:** All very low (0.032–0.058). Best k=2 (0.058). The embedding space has no strong natural clusters — guaci texts are distributed diffusely.

**Optimal k=2 clusters:**
- Cluster 0 (36): 謙, 睽, 坤, 泰, 隨, 明夷, 同人, 頤, 咸, 巽, 遯, 渙, 夬, 蠱, 臨, 鼎, 否, 比, 大畜, 大有, 恆, 師, 家人, 革, 需, 晉, 節, 履, 屯, 豐, 剝, 旅, 姤, 既濟, 益, 損
- Cluster 1 (28): 未濟, 中孚, 兌, 升, 大過, 豫, 賁, 訟, 復, 歸妹, 坎, 震, 无妄, 乾, 小過, 困, 噬嗑, 解, 大壯, 漸, 井, 萃, 艮, 蒙, 觀, 蹇, 離, 小畜

**Stability:** kmeans↔ward ARI=0.51 (moderate). All other pairs near 0 — clustering is unstable. DBSCAN found 1 cluster (everything), confirming diffuse distribution.

**Interpretation:** Guaci texts don't form tight semantic clusters. The k=2 split has very weak separation. Any clustering-based analysis of guaci must account for this.

## S3: 爻辭 Diagnostic

**DECISION: `formulaic_dominated = False`**

Marker-based prediction of embedding clusters:
- k=3: RF accuracy 47.4% (baseline 45.6%) — essentially random
- k=5: RF accuracy 31.5% (baseline 24.2%) — marginal lift
- k=8: RF accuracy 28.6% (baseline 24.7%) — marginal lift

χ² tests: Only 吝 at k=3 shows weak significance (p=0.044). No marker shows strong association with cluster membership.

**Conclusion:** Yaoci embedding clusters are NOT driven by formulaic valence markers. The BGE-M3 embeddings capture something beyond stock phrases — likely situational/imagistic content. This validates using the full embedding space for downstream analysis without needing to "subtract out" formulaic structure.

## S4: Commentary Structure

### III.1 大象 (64 texts)
- 50/64 (78%) have trigram images matching actual trigrams
- 14 mismatches use secondary nature images: 雲(=水), 泉(=水), 電(=火), 木(=風)
- Relation types: spatial 37, functional 14, dynamic 13

### III.2 彖傳 term frequencies
| Category | Top terms |
|----------|-----------|
| 剛柔 | 剛(60), 柔(39) |
| Position | 中(50), 正(35), 位(20), 當位(5), 得位(4) |
| Correspondence | 應(27) |
| Movement | 往(24), 來(12), 進(8), 乘(5) |
| Line refs | 二(5), 四(5), 三(4), 初(2), 五(1) |

剛/柔 and 中/正 dominate. The 彖傳 is primarily a positional/structural commentary.

### III.3 小象 positional bias (significant)
| Term | Pattern | χ² | p |
|------|---------|-----|---|
| 中 | Lines 2,5 only (24,23) | 80.2 | <0.0001 |
| 位 | Lines 3,4,5 only (10,11,12) | 33.4 | <0.0001 |
| 正 | Peak at line 5 (14/27) | 28.8 | <0.0001 |
| 上 | Peak at line 6 (17/35) | 28.3 | <0.0001 |
| 當 | Lines 3,4,5 (11,9,7) | 26.0 | 0.0001 |

**Critical finding:** 小象 vocabulary is strongly line-position-dependent. 中 appears almost exclusively at lines 2 and 5 (the "central" positions of each trigram). 位 clusters at lines 3-5. This confirms the 小象 encodes structural/positional information that maps directly to the line's position in the hexagram.
