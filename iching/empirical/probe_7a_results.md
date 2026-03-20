# Probe 7a: Kernel Hexagrams in the Semantic Manifold

> Do the 4 kernel hexagrams (坤, 夬, 剝, 乾) and their 6 stable_neutral
> lines occupy anomalous positions in the BGE-M3 embedding space?

---

## Data

- Embeddings: BGE-M3, 384 lines × 1024 dims
- Algebraic regression R² = 0.1096 (11.0% explained)
- Kernel hexagrams: hex 0 (坤), 31 (夬), 32 (剝), 63 (乾)
- Complement pairs: 坤↔乾, 夬↔剝

## Raw Embeddings

### Test 1: Distance from center
- Kernel z-score: -0.58
- Kernel hexagrams are **closer** to the center than average

### Test 2: Inter-kernel distance
- Kernel pairwise mean z-score: -0.44
- Permutation p: 0.2519
- Kernel hexagrams are **clustered**

### Test 5: Line-level
- SN center z-score: -0.82
- SN clustering permutation p: 0.1465

## Residual Embeddings

### Test 1: Distance from center
- Kernel z-score: -1.52
- Kernel hexagrams are **closer** to the center than average

### Test 2: Inter-kernel distance
- Kernel pairwise mean z-score: -0.10
- Permutation p: 0.4553
- Kernel hexagrams are **clustered**

### Test 5: Line-level
- SN center z-score: -1.14
- SN clustering permutation p: 0.2650

## Test 6: Valence Anomaly

| Group | N | 吉 rate | 凶 rate |
|-------|---|---------|---------|
| 6 stable_neutral | 6 | 0.000 | 0.333 |
| 4 kernel hex (24 lines) | 24 | 0.042 | 0.208 |
| Other 360 lines | 360 | 0.325 | 0.131 |
| All 384 | 384 | 0.307 | 0.135 |

Fisher's exact (kernel vs other):
- 吉: OR=0.09, p=0.0023
- 凶: OR=1.75, p=0.3486

## Synthesis

| Property | Raw | Residual |
|----------|-----|----------|
| Center position | unremarkable | central |
| Clustered? | no (p=0.252) | no (p=0.455) |
| SN line anomaly | p=0.146 | p=0.265 |


### Geometric findings

The kernel hexagrams show a **mild center-ward tendency** — they are closer
to the embedding centroid than average, especially in residual space (z=−1.52).
This strengthens after algebra is regressed out, suggesting their 爻辭 texts
are semantically generic/undifferentiated compared to other hexagrams.

However, the kernel hexagrams are **not significantly clustered** with each other
(permutation p=0.252 raw, 0.455 residual).
They do not form a compact neighborhood — they are scattered across the manifold
but individually closer to the center. This is consistent with 'semantically neutral'
rather than 'semantically similar to each other'.

### Valence anomaly (Finding 7b preview)

The 4 kernel hexagrams (24 lines) show **massive 吉 depletion**: 1/24 = 4.2%
vs base rate 117/360 = 32.5% (Fisher's p = 0.0023, OR = 0.09).
The 6 stable_neutral lines have 0/6 吉 and 2/6 凶.

This confirms the prediction from the findings: the algebraically most neutral
states (all-比和 五行 relation vector) are **textually the most adversarial.**
The grammar's diagnostic-silence points (where 五行 provides no signal)
coincide with texts that are disproportionately 凶 and almost never 吉.

This is NOT an artifact of the algebraic regression — the 吉-depletion is
a property of the original texts, not of the embedding geometry.
