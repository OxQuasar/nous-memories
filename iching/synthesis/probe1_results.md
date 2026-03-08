# Probe 1: The Decisive Test — Text ↔ Algebra Correlation

Do the oldest textual layers of the I Ching correlate with algebraic coordinates?

## Test Results Summary

| Test | Coordinate | Statistic | p-value | Verdict |
|------|-----------|-----------|---------|---------|
| A_basin | Basin | Δ=-0.0024 | 0.7337  | ✗ No signal |
| B_I_component | I-component | Δ=0.0003 | 0.4680  | ✗ No signal |
| C_palace | Palace | Δ=0.0003 | 0.4854  | ✗ No signal |
| D_kernel | Kernel (O,M,I) | H=31.00 | 0.4662  | ✗ No signal |
| E_advantageous_I | Valence: advantageous_I | χ²=0.02 | 0.8850  | ✗ No signal |
| E_advantageous_basin | Valence: advantageous_basin | χ²=2.13 | 0.3443  | ✗ No signal |
| E_advantageous_line | Valence: advantageous_line | χ²=5.18 | 0.3938  | ✗ No signal |
| E_auspicious_I | Valence: auspicious_I | χ²=1.48 | 0.2237  | ✗ No signal |
| E_auspicious_basin | Valence: auspicious_basin | χ²=1.98 | 0.3712  | ✗ No signal |
| E_auspicious_line | Valence: auspicious_line | χ²=24.61 | 0.0002 *** | ✓ Correlates |
| E_danger_I | Valence: danger_I | χ²=1.03 | 0.3098  | ✗ No signal |
| E_danger_basin | Valence: danger_basin | χ²=4.46 | 0.1078  | ✗ No signal |
| E_danger_line | Valence: danger_line | χ²=11.22 | 0.0472 * | ✓ Correlates |
| E_difficulty_I | Valence: difficulty_I | χ²=0.05 | 0.8183  | ✗ No signal |
| E_difficulty_basin | Valence: difficulty_basin | χ²=0.32 | 0.8536  | ✗ No signal |
| E_difficulty_line | Valence: difficulty_line | χ²=10.55 | 0.0611  | ✗ No signal |
| E_inauspicious_I | Valence: inauspicious_I | χ²=16.22 | 0.0001 *** | ✓ Correlates |
| E_inauspicious_basin | Valence: inauspicious_basin | χ²=17.44 | 0.0002 *** | ✓ Correlates |
| E_inauspicious_line | Valence: inauspicious_line | χ²=19.93 | 0.0013 ** | ✓ Correlates |
| E_no_blame_I | Valence: no_blame_I | χ²=1.51 | 0.2190  | ✗ No signal |
| E_no_blame_basin | Valence: no_blame_basin | χ²=2.92 | 0.2327  | ✗ No signal |
| E_no_blame_line | Valence: no_blame_line | χ²=12.04 | 0.0342 * | ✓ Correlates |
| E_regret_I | Valence: regret_I | χ²=0.00 | 1.0000  | ✗ No signal |
| E_regret_basin | Valence: regret_basin | χ²=1.79 | 0.4087  | ✗ No signal |
| E_regret_line | Valence: regret_line | χ²=5.65 | 0.3418  | ✗ No signal |
| F_nuclear_outer | Nuclear vs Outer | χ²=9.76 | 0.1349  | ✗ No signal |
| G_hugua | 互卦 | Δ=-0.0143 | 0.9196  | ✗ No signal |
| H_upper_lower | Upper/Lower relation | H=32.34 | 0.0000 *** | ✓ Correlates |

## Interpretation by Category

### Embedding-space tests (A–D, G): No clustering by algebraic coordinates

Tests A (basin), B (I-component), C (palace), D (kernel triple), and G (互卦)
all fail to find significant clustering in the semantic embedding space.
The 卦辭 texts do not cluster by basin, palace, kernel decomposition, or 互 pairing.
This means the **algebraic structure of the binary encoding does not predict
what the judgment texts say** at the level of overall semantic similarity.

### Valence × line position (Test E): Strong signal

Line position (1–6) significantly predicts the distribution of several
valence markers:
- **吉 (auspicious)**: p=0.0002 — strongly non-uniform across line positions
- **凶 (inauspicious)**: p=0.0013 — concentrated at specific positions
- **无咎 (no blame)**: p=0.0342 — position-dependent
- **厲 (danger)**: p=0.0472 — marginally significant

This is expected and well-known: line position carries meaning in the
tradition (初 = beginning, 上 = excess, 二/五 = central positions).

### 凶 (inauspicious) × algebraic coordinates: The standout signal

凶 is the only valence marker that correlates with algebraic structure
**beyond** line position:
- **凶 × basin**: χ²=17.44, p=0.0002 — 凶 is non-uniformly distributed across basins
- **凶 × I-component**: χ²=16.22, p=0.0001 — hexagrams with I=1 (interface
  disagreement) carry significantly different 凶 rates

This is the single strongest bridge between the algebraic decomposition
and textual content. The I-component (b₂⊕b₃) determines basin membership,
so the basin and I-component effects are likely the same signal.

### Upper/lower trigram relation (Test H): Significant

Hexagrams grouped by their upper/lower five-phase relation (比和, 生体,
体生用, 克体, 体克用) show significantly different within-group semantic
similarities (H=32.34, p<0.0001). 比和 and 生体 groups have higher
internal coherence. This confirms that the trigram-pair relationship —
a feature visible to both 梅花 and 火珠林 — does predict textual themes.

### Nuclear vs outer (Test F): Not significant

The embedding centroid distance between nuclear (lines 2–5) and outer
(lines 1, 6) 爻辭 is tiny (d=0.006). Valence distributions differ
directionally (outer lines have 2× the 凶 rate of nuclear) but the
χ² test is not significant (p=0.13). The nuclear/outer distinction is
weak in the textual tradition.

### 互卦 prediction (Test G): No signal

互 pairs are not semantically closer than random pairs. In fact they
trend *less* similar (Δ=−0.014). The 互卦 map, which is the core of
the basin/kernel framework, has **no detectable footprint** in the
judgment texts. This is the most decisive negative result.

## Overall Verdict

**7 of 28 tests** significant at α=0.05.

### What correlates with text:
1. **Line position** → valence distribution (吉, 凶, 无咎, 厲). This is
   a property of the position *within* a hexagram, not of hexagram identity.
2. **凶 × basin/I-component** — the single algebraic-coordinate-level signal.
   Hexagrams in different basins have different rates of 凶 in their 爻辭.
3. **Upper/lower five-phase relation** → semantic clustering. The trigram-pair
   relationship predicts thematic similarity among 卦辭.

### What does NOT correlate:
- Basin → 卦辭 embedding (no clustering)
- Palace → 卦辭 embedding (no clustering)
- Kernel (O,M,I) → 卦辭 embedding (no effect)
- I-component → 卦辭 embedding (no clustering)
- 互卦 pairing → semantic similarity (no signal, if anything anti-correlated)
- Nuclear vs outer → valence (weak, not significant)

### Assessment: MIXED — Layer-Dependent

The algebraic framework is **not notational overlay** — the 凶×basin signal
and the upper/lower relation clustering are real. But the core algebraic
constructs (basin, kernel, 互卦, palace) do not predict what the judgment
texts *say* at the semantic level. They predict aspects of **valence**
(specifically 凶) and **thematic grouping** (via trigram relations), but
not the embedding-space meaning of the texts.

The algebra describes structure the text tradition was partly aware of
(trigram relations, line position) but does not encode the deeper
algebraic structure (basin convergence, kernel decomposition, 互卦 map).
These latter constructs are descriptive of the binary encoding's
mathematical properties, not of the received textual meaning.
