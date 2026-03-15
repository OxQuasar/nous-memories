# Q3 Phase 3: 說卦傳 象 Space vs Complement Embedding Geometry

## Phase 1: Association Matrix

- **Total unique associations:** 203
- **Matrix:** 8 trigrams × 203 associations

| Category | N associations | Example items |
|----------|---------------|---------------|
| nature | 16 | 冰, 地, 天, 寒, 山... |
| animal | 21 | 水族, 牛, 狐, 狗, 百禽... |
| body | 20 | 口, 大腹, 手, 指, 爪... |
| family | 11 | 中女, 中男, 少女, 少男, 母... |
| direction | 8 | 北, 南, 東, 東北, 東南... |
| quality | 34 | 不果, 伏, 健, 入, 剛... |
| material | 20 | 土, 寶, 布, 帛, 弓... |
| color | 11 | 大赤, 玄黃, 白, 碧, 紅... |
| shape | 9 | 上缺, 中虛, 圓, 小, 方... |
| object | 39 | 冠, 帆, 帶口之器, 廢物, 徑路... |
| social | 14 | 仙道, 僧尼, 君, 奴僕, 妾... |

| Trigram | Total associations |
|---------|-------------------|
| 坤 | 27 |
| 震 | 25 |
| 坎 | 32 |
| 艮 | 25 |
| 兌 | 20 |
| 離 | 28 |
| 巽 | 27 |
| 乾 | 32 |

## Phase 2: Hexagram 象 Profiles

- Concatenation: 64 × 406 (64 distinct profiles)
- Union: 64 × 203 (36 distinct profiles)

## Phase 3: Correlation Tests

### 3a: Mantel Test (full distance matrix)

| Space | Pearson r | p (parametric) | p (permutation) |
|-------|-----------|---------------|-----------------|
| Concat | -0.0031 | 0.889 | 0.5431 |
| Union | 0.0043 | 0.8487 | 0.4477 |

### 3b: CCA (complement difference vectors)

| CC | Concat r | Union r |
|----|----------|---------|
| CC1 | 0.6730 | 0.5349 |
| CC2 | 0.6334 | 0.3813 |
| CC3 | 0.3260 | 0.3604 |
| CC4 | 0.2009 | 0.2961 |
| CC5 | 0.0436 | 0.2186 |

**CCA CC1 permutation test (999 perms): p=0.334.** The apparent CC1=0.67 is spurious — CCA overfits with n=32 samples and 5 components (null mean=0.63, max=0.86).

### 3c: Procrustes Analysis

- Concat: disparity=0.7904, p_perm=0.4220
- Union: disparity=0.8741, p_perm=0.7210

### 3d: Per-Category Prediction

| Category | N | Pearson r | p | Spearman ρ | p |
|----------|---|-----------|---|------------|---|
| nature | 16 | -0.0066 | 0.7655 | 0.0043 | 0.8459 | 
| animal | 21 | -0.0065 | 0.7717 | -0.0063 | 0.7786 | 
| body | 20 | -0.0256 | 0.2507 | -0.0285 | 0.2006 | 
| family | 11 | -0.0046 | 0.8347 | -0.0058 | 0.7946 | 
| direction | 8 | -0.0052 | 0.8147 | -0.0020 | 0.9277 | 
| quality | 34 | 0.0018 | 0.9373 | 0.0110 | 0.621 | 
| material | 20 | -0.0083 | 0.7094 | -0.0062 | 0.7806 | 
| color | 11 | 0.0144 | 0.5174 | 0.0197 | 0.3768 | 
| shape | 9 | 0.0098 | 0.6606 | 0.0119 | 0.5936 | 
| object | 39 | 0.0170 | 0.4449 | 0.0211 | 0.3431 | 
| social | 14 | -0.0264 | 0.2352 | -0.0245 | 0.2722 | 

## Interpretation

**The 說卦傳 象 space does NOT predict embedding geometry** (Mantel p > 0.05).

The embeddings capture semantic structure BEYOND what the traditional 象 system encodes. The 18-dimensional complement space (R133) contains information that the 說卦傳 categorization cannot access — a richer or different semantic structure.

This is consistent with R135 (complement opposition lexically invisible) and extends it: the opposition is not just invisible at the vocabulary level, but also invisible at the level of traditional 象 categories. Whatever the embeddings see operates below both layers.
