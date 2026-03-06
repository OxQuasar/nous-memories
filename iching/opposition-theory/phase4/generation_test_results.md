# Phase 4 Round 3: Critical Null Model + Consolidation

## A. Z₂³ Generation Null Model

For each of 50,400 valid surjections (8 trigrams → 5 elements, partition 2,2,2,1,1),
compute the XOR masks produced by each five-phase cycle and test whether they generate
the full group Z₂³ under XOR closure (i.e., GF(2)-rank = 3).

### Generation rates

| Condition | Count | Rate |
|-----------|-------|------|
| 生 generates Z₂³ | 50400 | 1.0000 |
| 克 generates Z₂³ | 50400 | 1.0000 |
| **Both** generate Z₂³ | 50400 | 1.0000 |
| **Neither** generates Z₂³ | 0 | 0.0000 |
| 生 only | 0 | 0.0000 |
| 克 only | 0 | 0.0000 |

### Verdict

Both-generate rate: **100.0%**

**GENERIC:** Dual generation is the common case — the finding is not distinctive.
The traditional assignment is **not** algebraically distinguished by dual Z₂³ generation alone.

### Number of distinct nonzero masks per cycle

| # masks | 生 count | 生 frac | 克 count | 克 frac |
|---------|----------|---------|----------|---------|
| 5 | 8400 | 0.1667 | 8400 | 0.1667 |
| 6 | 21840 | 0.4333 | 21840 | 0.4333 |
| 7 | 20160 | 0.4000 | 20160 | 0.4000 |

**Traditional:** 生 has 5 masks, 克 has 5 masks.
**Mean masks:** 生 = 6.23, 克 = 6.23

### Mask count → generation rate

| # masks | 生 gen rate | 克 gen rate |
|---------|------------|------------|
| 5 | 1.0000 (n=8400) | 1.0000 (n=8400) |
| 6 | 1.0000 (n=21840) | 1.0000 (n=21840) |
| 7 | 1.0000 (n=20160) | 1.0000 (n=20160) |

## B. Exclusive Mask Partition Quality

Among surjections where both cycles generate Z₂³:

**N (both generate):** 50400

### Partition cleanness distribution

Cleanness = (exclusive_生 + exclusive_克) / total_distinct_masks

**Traditional:** excl_生=2, excl_克=2, shared=3, cleanness=0.5714

**Distribution:** min=0.0000, max=0.5714, mean=0.2190, std=0.1871
**Traditional percentile:** 100.0%

```
  -0.010-0.032 | ██████████████████████████████████████████████████ 13440
  0.032-0.074 |  0
  0.074-0.117 |  0
  0.117-0.159 | ██████████████████████████████████████████████████ 13440
  0.159-0.201 |  0
  0.201-0.243 |  0
  0.243-0.286 |  0
  0.286-0.328 | ██████████████████████████████████████████████████ 13440
  0.328-0.370 |  0
  0.370-0.412 |  0
  0.412-0.455 | ████████████ 3360
  0.455-0.497 |  0
  0.497-0.539 |  0
  0.539-0.581 | █████████████████████████ 6720 ◄ TRAD
```

### Exclusive mask counts

| excl_生 | excl_克 | shared | Count | Frac |
|---------|---------|--------|-------|------|
| 0 | 0 | 7 | 13440 | 0.2667 |
| 1 | 1 | 5 | 13440 | 0.2667 |
| 1 | 0 | 6 | 6720 | 0.1333 |
| 2 | 2 | 3 | 6720 | 0.1333 | ◄ TRAD
| 0 | 1 | 6 | 6720 | 0.1333 |
| 1 | 2 | 4 | 1680 | 0.0333 |
| 2 | 1 | 4 | 1680 | 0.0333 |

## C. Directed-Cycle Hamming Profile

### Traditional edge-mean sequences

**生:** ['1.50', '1.50', '2.50', '1.50', '1.50']
  Edges: ['W→F', 'F→E', 'E→M', 'M→Wa', 'Wa→W']

**克:** ['1.50', '1.50', '3.00', '1.50', '1.50']
  Edges: ['W→E', 'E→Wa', 'Wa→F', 'F→M', 'M→W']

### Autocorrelation at lag 1

Measures whether high/low distance edges cluster together (+) or alternate (−).

| Cycle | Traditional AC(1) | Mean | Std | Percentile |
|-------|-------------------|------|-----|------------|
| 生 | -0.3000 | -0.3369 | 0.2756 | 67.4% |
| 克 | -0.3000 | -0.3369 | 0.2756 | 67.4% |

### Histogram: 生 AC(1)

```
  -0.866 to -0.803 |  48
  -0.803 to -0.741 | ██████████████████ 3408
  -0.741 to -0.679 | █████████████ 2448
  -0.679 to -0.617 | ███████████ 2136
  -0.617 to -0.555 | ██████ 1176
  -0.555 to -0.493 | █████████████████████████ 4704
  -0.493 to -0.431 | ██████████████████████████████████████████████████ 9216
  -0.431 to -0.369 | █████████████ 2496
  -0.369 to -0.307 | █████ 1056
  -0.307 to -0.244 | ███████████████████████████████████████████████ 8736 ◄ TRAD
  -0.244 to -0.182 | █████ 1008
  -0.182 to -0.120 | ██████ 1224
  -0.120 to -0.058 | ██████ 1248
  -0.058 to +0.004 | ███████████████████████████████████████ 7368
  +0.004 to +0.066 | ████████ 1632
  +0.066 to +0.128 |  0
  +0.128 to +0.190 |  144
  +0.190 to +0.252 | █ 288
  +0.252 to +0.315 | █ 288
  +0.315 to +0.377 | █████████ 1776
```

### Histogram: 克 AC(1)

```
  -0.866 to -0.803 |  48
  -0.803 to -0.741 | ██████████████████ 3408
  -0.741 to -0.679 | █████████████ 2448
  -0.679 to -0.617 | ███████████ 2136
  -0.617 to -0.555 | ██████ 1176
  -0.555 to -0.493 | █████████████████████████ 4704
  -0.493 to -0.431 | ██████████████████████████████████████████████████ 9216
  -0.431 to -0.369 | █████████████ 2496
  -0.369 to -0.307 | █████ 1056
  -0.307 to -0.244 | ███████████████████████████████████████████████ 8736 ◄ TRAD
  -0.244 to -0.182 | █████ 1008
  -0.182 to -0.120 | ██████ 1224
  -0.120 to -0.058 | ██████ 1248
  -0.058 to +0.004 | ███████████████████████████████████████ 7368
  +0.004 to +0.066 | ████████ 1632
  +0.066 to +0.128 |  0
  +0.128 to +0.190 |  144
  +0.190 to +0.252 | █ 288
  +0.252 to +0.315 | █ 288
  +0.315 to +0.377 | █████████ 1776
```

## D. 互卦 Amplification Verification

**All pass:** True

| Line | Bit | Expected Hamming | Actual | Deterministic | Matches |
|------|-----|-----------------|--------|---------------|---------|
| L1 (outer) | 0 | 0 | 0 | True | True |
| L2 (middle) | 1 | 1 | 1 | True | True |
| L3 (inner) | 2 | 2 | 2 | True | True |
| L4 (inner) | 3 | 2 | 2 | True | True |
| L5 (middle) | 4 | 1 | 1 | True | True |
| L6 (outer) | 5 | 0 | 0 | True | True |

**Theorem (confirmed):** The 互卦 map has deterministic Hamming response to single-line flips:

- **Outer pair (L1, L6):** Hamming = 0 — completely erased
- **Middle pair (L2, L5):** Hamming = 1 — faithfully transmitted
- **Inner pair (L3, L4):** Hamming = 2 — doubled (amplified)

This follows directly from the 互卦 definition: it picks bits {1,2,3,2,3,4},
so bit 2 (L3) and bit 3 (L4) each appear twice in the output, bits 1,4 appear once,
and bits 0,5 are absent. The amplification factor per mirror-pair layer is:
O→0, M→1, I→2.

## Structural Summary

### Is dual Z₂³ generation remarkable?

**No.** 100.0% achieve it — this is the generic case.
Dual Z₂³ generation is a near-automatic consequence of the partition shape,
not a distinguishing feature of the traditional assignment.

### What IS distinctive about the traditional mapping?

Combining all Phase 4 results:

- **克 edge variance** is extreme (96.2nd percentile from Round 2) — the Water→Fire singleton edge at d=3 is structurally forced
- **生−克 asymmetry** (0.2179) at ~77th percentile — moderately unusual directional bias
- **Partition cleanness** (0.5714) at 100.0th percentile
- **Dual Z₂³ generation** (100.0%) — generic, not distinctive
- **XOR mask coverage:** all 7 nonzero masks covered (生 ∪ 克 = Z₂³ \ {0})
- **Shell-only pairs** show 2.33× agreement ratio (structural, not mapping-dependent)
- **互卦 amplification** O→0, M→1, I→2 (theorem, not mapping-dependent)
- **体/用 samples uniformly** from all trigram pairs (theorem, not mapping-dependent)
