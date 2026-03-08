# Probe 2: Contextual Obstruction — Readability Deficiency

## Construction

For each hexagram h and context (season, 用神 type), define:
```
F(h, season, yongshen) = # lines where:
  (1) line's 六親 type == yongshen, AND
  (2) line's branch element is 旺 or 相 in that season
```
Total contexts per hexagram: 25 (5 seasons × 5 用神 types)

Two derived measures:
- **n_zero**: count of contexts where F=0 (dark contexts — unreadable)
- **F_variance**: variance of F across contexts where F>0 (signal consistency)

## Distribution Summary

- n_zero range: [15, 19] out of 25
- n_zero mean: 17.00, median: 17.0
- F_variance range: [0.0000, 0.2500]

### n_zero distribution

| n_zero | Hexagrams |
|--------|-----------|
| 15 | 16 |
| 17 | 32 |
| 19 | 16 |

### By basin

| Basin | mean n_zero | mean F_var | mean 凶 |
|-------|-------------|------------|---------|
| Kun | 16.50 | 0.1638 | 1.25 |
| Qian | 17.00 | 0.1437 | 1.25 |
| Cycle | 17.25 | 0.1763 | 0.38 |

### By depth (I=0 only)

| Depth | n_hex | mean n_zero | mean F_var | mean 凶 |
|-------|-------|-------------|------------|---------|
| 0 | 2 | 15.00 | 0.1600 | 0.00 |
| 1 | 6 | 16.33 | 0.2200 | 2.17 |
| 2 | 24 | 17.00 | 0.1367 | 1.12 |

## Correlation with 凶

| Measure | Spearman ρ | p | Pearson r | p | Sig |
|---------|-----------|---|-----------|---|-----|
| n_zero vs 凶 | 0.1206 | 0.3423 | 0.0237 | 0.8527 | ✗ |
| F_variance vs 凶 | -0.0583 | 0.6474 | -0.0410 | 0.7478 | ✗ |
| F_total vs 凶 | 0.0000 | 1.0000 | 0.0000 | 1.0000 | ✗ |

### Group tests (Kruskal-Wallis by basin)

| Measure | H | p | Sig |
|---------|---|---|-----|
| n_zero | 2.9531 | 0.2284 | ✗ |
| F_variance | 2.0781 | 0.3538 | ✗ |
| F_total | — | — | constant=12 |

## Extreme Cases

### Highest n_zero (most dark contexts)

| KW# | Name | Basin | Depth | n_zero | F_var | 凶 |
|-----|------|-------|-------|--------|-------|-----|
| 29 | Kan | Kun | 2 | 19 | 0.000 | 2 |
| 60 | Jie | Kun | 2 | 19 | 0.000 | 2 |
| 47 | Kun | Cycle | 2 | 19 | 0.000 | 2 |
| 51 | Zhen | Cycle | 2 | 19 | 0.000 | 1 |
| 55 | Feng | Qian | 2 | 19 | 0.000 | 1 |
| 34 | Da Zhuang | Qian | 2 | 19 | 0.000 | 1 |
| 8 | Bi | Kun | 2 | 19 | 0.000 | 1 |
| 58 | Dui | Cycle | 2 | 19 | 0.000 | 1 |
| 21 | Shi He | Cycle | 2 | 19 | 0.000 | 1 |
| 30 | Li | Qian | 2 | 19 | 0.000 | 1 |

### Lowest n_zero (fewest dark contexts)

| KW# | Name | Basin | Depth | n_zero | F_var | 凶 |
|-----|------|-------|-------|--------|-------|-----|
| 2 | Kun | Kun | 0 | 15 | 0.160 | 0 |
| 19 | Lin | Kun | 2 | 15 | 0.160 | 0 |
| 48 | Jing | Cycle | 2 | 15 | 0.160 | 0 |
| 22 | Bi | Cycle | 2 | 15 | 0.160 | 0 |
| 26 | Da Chu | Cycle | 2 | 15 | 0.160 | 0 |
| 20 | Guan | Kun | 2 | 15 | 0.160 | 0 |
| 59 | Huan | Kun | 2 | 15 | 0.160 | 0 |
| 25 | Wu Wang | Cycle | 2 | 15 | 0.160 | 0 |
| 13 | Tong Ren | Qian | 2 | 15 | 0.160 | 0 |
| 1 | Qian | Qian | 0 | 15 | 0.160 | 0 |

## Interpretation

### Why n_zero takes only 3 values

n_zero decomposes into two independent components:
1. **Missing-type zeros**: if 用神 type is absent from the 六親 word,
   F=0 for ALL 5 seasons → contributes 5 zeros per missing type
2. **Seasonal zeros**: 用神 type is present but no line of that type
   has its branch element in {旺, 相} for that season

Since hexagrams have 0, 1, or 2 missing types (from Probe 3 of huozhulin),
the missing-type contribution is 0, 5, or 10 — a coarse step function.
The remaining seasonal zeros depend on which elements appear in which
positions, adding 5–9 more zeros. The result: n_zero ∈ {15, 17, 19}
with the 16:32:16 distribution reflecting the 0:1:2 missing-type count.

This means n_zero is dominated by the **static** 六親 coverage structure,
not by the **dynamic** seasonal modulation. The seasonal system adds
only a constant offset of ~15 zeros regardless of hexagram — it does
not create hexagram-specific variance.

### n_zero × 凶 (ρ=0.121, p=0.3423 ✗)

Not significant. The 3-valued n_zero is too coarse to resolve the
凶 gradient. The depth gradient (0→36→19→6% 凶) and the n_zero
gradient (15→17→19) move in the same direction within I=0, but the
correlation lacks power because n_zero has no variance within
its 3 levels.

### F_variance × 凶 (ρ=-0.058, p=0.6474 ✗)

Not significant. F_variance also takes few distinct values
(0.000 for n_zero=19, 0.250 for n_zero=17, 0.160 for n_zero=15)
because F itself takes only values 0, 1, or 2 per context.

### F_total: conservation law

**F_total = 12 for every hexagram.** This is a structural invariant —
the total number of active line-slots across all 25 contexts is identical
for all 64 hexagrams. The measure cannot correlate with anything.

This conservation arises from the double bijection: 六親 maps each type to
one element, and each season activates exactly 2 elements. Each line
appears in exactly one 六親 type, and its element is 旺/相 in exactly
2 of 5 seasons. So each line contributes exactly 2 active slots → 6 lines × 2 = 12.

### Structural diagnosis

The contextual obstruction construction is **algebraically too constrained**
to produce hexagram-specific variation. The key constraints:

1. **六親→element is a bijection** (5 types → 5 elements): each type maps to
   exactly one element, so seasonal strength applies uniformly per type
2. **旺/相 activates exactly 2 elements per season**: at most 2 用神 types can
   be active in any season (the 2/5 ceiling from Probe 6)
3. **Lines of the same 六親 type share the same branch element** within a trigram:
   the trigram determines which branches appear, so lines of type u tend to
   cluster on 1–2 elements, making F ∈ {0, 1, 2} with no finer resolution

These constraints make F a function of (palace, trigram pair, season) rather than
of individual hexagram identity. The basin/depth structure — which lives in the
inner 4 bits — is invisible to 納甲 (confirmed in Probe 1 of huozhulin),
and therefore invisible to any measure built on 六親 × seasonal strength.

### The orthogonality wall

This is the precise manifestation of the **納甲 ⊥ 互卦 orthogonality** discovered
in the huozhulin workflow. The 火珠林 operational structure (六親, 旺相, 用神)
is built entirely on the trigram-pair projection (outer bits). The 凶 signal lives
in the basin/depth structure (inner bits). These two structures cannot see each other.
No measure derived from 六親 × seasonal strength can predict basin-correlated 凶,
because the information channels are algebraically orthogonal.

The prediction that n_zero would correlate with 凶 implicitly assumed that
operational narrowness and textual danger share a structural basis. They do not:
they live in complementary subspaces of Z₂⁶.
