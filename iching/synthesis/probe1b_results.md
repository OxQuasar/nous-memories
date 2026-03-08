# Probe 1b: Dissect the 凶 × Basin Bridge


## Part A: 凶 Rate Dissection

### A1: 凶 rate by basin

| Basin | Total 爻辭 | 凶 count | 凶 rate |
|-------|-----------|----------|---------|
| Kun   |        96 |       20 | 0.2083 |
| Qian  |        96 |       20 | 0.2083 |
| Cycle |       192 |       12 | 0.0625 |

### A2: 凶 rate by I-component

| I | Total | 凶 count | 凶 rate |
|---|-------|----------|---------|
| 0 |   192 |       40 | 0.2083 |
| 1 |   192 |       12 | 0.0625 |

### A3: 凶 rate by (basin, I-component)

| Basin | I | Total | 凶 count | 凶 rate |
|-------|---|-------|----------|---------|
| Kun   | 0 |    96 |       20 | 0.2083 |
| Qian  | 0 |    96 |       20 | 0.2083 |
| Cycle | 1 |   192 |       12 | 0.0625 |

**Note:** Basin determines I-component: I=0 ↔ {Kun, Qian}, I=1 ↔ Cycle exactly.
The basin and I-component signals are **identical** — not independent.

### A4: 凶 rate by line position × basin

| Line | Kun rate | Qian rate | Cycle rate | Kun n | Qian n | Cycle n |
|------|---------|-----------|------------|-------|--------|---------|
| 1    |  0.2500 |    0.2500 |     0.0312 |    16 |     16 |      32 |
| 2    |  0.2500 |    0.0625 |     0.0312 |    16 |     16 |      32 |
| 3    |  0.1875 |    0.3125 |     0.1562 |    16 |     16 |      32 |
| 4    |  0.0625 |    0.1250 |     0.0312 |    16 |     16 |      32 |
| 5    |  0.1250 |    0.0625 |     0.0000 |    16 |     16 |      32 |
| 6    |  0.3750 |    0.4375 |     0.1250 |    16 |     16 |      32 |

**Within-line basin tests:**

- Line 1: χ²=6.335, p=0.0421 ✓
- Line 2: χ²=6.253, p=0.0439 ✓
- Line 3: χ²=1.641, p=0.4402 ✗
- Line 4: χ²=1.600, p=0.4493 ✗
- Line 5: χ²=3.847, p=0.1461 ✗
- Line 6: χ²=6.648, p=0.0360 ✓

### A5: All valence markers × basin rates

| Marker | Kun rate | Qian rate | Cycle rate | χ² | p | Sig |
|--------|---------|-----------|------------|-----|------|-----|
| auspicious     |  0.2917 |    0.2604 |     0.3385 |  1.98 | 0.3712 | ✗ |
| inauspicious   |  0.2083 |    0.2083 |     0.0625 | 17.44 | 0.0002 | ✓ |
| regret         |  0.0521 |    0.1042 |     0.0833 |  1.79 | 0.4087 | ✗ |
| difficulty     |  0.0417 |    0.0521 |     0.0573 |  0.32 | 0.8536 | ✗ |
| no_blame       |  0.2812 |    0.2188 |     0.1927 |  2.92 | 0.2327 | ✗ |
| danger         |  0.0208 |    0.0833 |     0.0833 |  4.46 | 0.1078 | ✗ |
| advantageous   |  0.1875 |    0.1146 |     0.1406 |  2.13 | 0.3443 | ✗ |

## Part B: 大象 Embedding Tests

The 大象 texts explicitly reference trigram imagery (e.g. "天行健" for ☰☰).
Do they cluster by algebraic coordinates more than 卦辭?

### 大象 — Clustering Results

| Test | Δ (within−between) | p-value | Sig |
|------|--------------------|---------|-----|
| basin            |             0.0016 | 0.3083 | ✗ |
| palace           |             0.0095 | 0.0266 | ✓ |
| I_component      |            -0.0033 | 0.8577 | ✗ |
| upper_lower      |            -0.0040 | 0.8472 | ✗ |
| kernel           |            H=31.00 | 0.4662 | ✗ |

## Part C: 彖傳 Embedding Tests

The 彖傳 discusses hexagram structure (剛柔, 上下, positions).
Does it show algebraic correlation?

### 彖傳 — Clustering Results

| Test | Δ (within−between) | p-value | Sig |
|------|--------------------|---------|-----|
| basin            |             0.0034 | 0.0448 | ✓ |
| palace           |            -0.0002 | 0.5284 | ✗ |
| I_component      |             0.0013 | 0.2379 | ✗ |
| upper_lower      |            -0.0015 | 0.7332 | ✗ |
| kernel           |            H=31.00 | 0.4662 | ✗ |

## Cross-Layer Comparison

| Layer | Basin p | Palace p | I-comp p | Upper/Lower p | Kernel p |
|-------|---------|----------|----------|---------------|----------|
| 卦辭 | 0.7382 | 0.4773 | 0.4689 | 0.9126 | 0.4662 |
| 大象 | 0.3083 | 0.0266* | 0.8577 | 0.8472 | 0.4662 |
| 彖傳 | 0.0448* | 0.5284 | 0.2379 | 0.7332 | 0.4662 |

## Part D: Interpretation

### The basin ↔ I-component identity

Basin is **fully determined** by the I-component: I=0 → {Kun, Qian} fixed-point basins,
I=1 → Cycle basin. The 凶×basin signal and 凶×I-component signal are the **same signal**.
There is no independent basin effect beyond what I-component explains.

### Direction of the 凶 signal

凶 is **concentrated in the fixed-point basins** (Kun and Qian, I=0): rate 20.8%,
vs only 6.3% in the Cycle basin (I=1). The ratio is 3.3×.
Kun and Qian have identical rates (20.8% each), confirming the signal tracks
I-component, not the Kun/Qian distinction within fixed-point basins.

### Structural meaning

This is the **opposite** of the naïve expectation. Cycle basin hexagrams —
the 'irresolvable' Fire↔Water oscillators with 克 interface — are *less* dangerous.
The fixed-point hexagrams (b₂=b₃, converging to pure Kun or pure Qian) carry 3× the 凶 rate.

Interpretation: **extremity is dangerous, not irresolution.** Hexagrams whose
interface bits agree (b₂=b₃) have aligned inner structure that converges to
a fixed point — pure yin or pure yang. This structural rigidity correlates with
textual danger. The Cycle hexagrams, with their permanent inner tension,
are paradoxically the *safer* configurations in the text tradition.

This inverts the 克-danger mapping: 克 at the interface (I=1, Cycle) does NOT
mean textual danger. Instead, the absence of interface tension (I=0) — structural
alignment heading toward extremes — is what the texts mark as 凶.

### Basin effect persists controlling for line position

The line×basin analysis (A4) shows the basin effect is significant at lines 1, 2, and 6
(the outer lines), controlling for position. At every line position, Cycle has the lowest
凶 rate. The signal is not an artifact of basin-correlated line-position distributions.

### Layer comparison

Across text layers, algebraic clustering is weak but layer-specific:

- **大象** clusters by **palace** (p=0.027) but not basin — expected since 大象
  uses trigram imagery, and palace groups share a root trigram.

- **彖傳** clusters by **basin** (p=0.045) but not palace — it discusses hexagram
  structure (剛柔, 上下) which relates to the interface-bit dynamics.

- **卦辭** shows no embedding clustering on any coordinate — its algebraic signal
  is purely in valence (凶), not in semantic similarity.

- **Upper/lower relation** — surprisingly not significant for any layer, including 大象.
  The probe 1 result (H=32.34, p<0.0001 on 卦辭) used Kruskal-Wallis on within-group
  distributions; the within-vs-between permutation test used here is a different,
  less powerful test for this case where groups have very unequal sizes.

- **Kernel (O,M,I)** shows identical H=31.0, p=0.47 across all three layers — a
  consequence of the 32 distinct kernel triples producing many small groups.
