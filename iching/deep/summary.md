# Deep Exploration Summary

## Question

Can every numerical parameter of the I Ching (5 elements, 3 lines, 8 trigrams, 6-line hexagrams, 64 hexagrams, element assignments, compass arrangements, KW pairing) be derived from first principles rather than being arbitrary choices?

**Answer: Yes.** Two axioms → all parameters forced, zero free choices.

## Axioms

1. **Relational structure.** A finite set of categories carries two independent non-degenerate cyclic orderings (生 and 克).
2. **Binary substrate.** Z₂ⁿ objects with complement involution surject onto the categories, with complement = negation.

## Derivation Chain

```
Axiom 1 (two cycles)
  → |Elements| = 5  (smallest prime supporting two independent strides)

Axiom 2 (complement = negation on Z₂ⁿ → Z₅)
  → n = 3 lines     (unique dimension forcing singleton fibers, pigeonhole)
  → 8 trigrams       (= 2³)
  → 6-line hexagrams (largest involutory 互 dimension)
  → 64 hexagrams     (= 2⁶)

Conjunction of algebra + text
  → Traditional 五行 assignment  (1/240 survives both filters)

Exhaustive compass search
  → 先天: unique Z₂ optimum (complement_diameter = 4/4)
  → 後天: unique 2×3×5 triple junction (96 → 8 → 2 → 1)
```

## Key Results

| Finding | Value | p-value / proof | Script |
|---|---|---|---|
| 5 elements forced | k=5 unique | Number theory proof | number-structure.md |
| 3 lines forced | n=3 unique | Pigeonhole theorem | 04_dimensional_forcing.py |
| 五行 assignment unique | 1/240 | Algebraic + Fisher p=0.007 | 01_assignment_test.py |
| 先天 unique Z₂ optimum | Score 6/6, gap of 3 | Exhaustive (96+1) | 02_arrangements.py |
| 後天 unique junction | 96→8→2→1 | Exhaustive (3 primes) | 03_prime_decomposition.py |
| V₄ orbits | 20 (0+8+12) | All commute with 互 | 06_v4_symmetry.py |
| V₄-compatible pairings | 3¹² = 531,441 | Independence proven | 08_pairing_torus.py |
| KW pairing = pure reversal | 28/32 same-basin | Unique maximum | 08_pairing_torus.py |
| 吉 × line hierarchy | χ²=15.1 | p=0.0005 | 09_line_valuations.py |
| Line 5 ruler effect | OR=2.15 | p=0.007 | 09_line_valuations.py |
| 生体 × Line 5 = 75% 吉 | Peak auspicious | χ²=58.6, p=0.0009 | 09_line_valuations.py |
| KW basin clustering | 60% vs 37% expected | p < 0.001 | 05_king_wen_sequence.py |
| Palace torus coverage | 25/25 Z₅×Z₅ cells | Complement-related | 07_palaces_transform.py |

## Status

**Resolved (4/7 deep questions):** §2 (two Z₅ incommensurability), §3 (3×5 grid null), §5 (complement as bridge), §6 (後天 uniqueness).

**Open (3/7):** §1 (coordinate-free space — ontological), §4 (incommensurability as mechanism — philosophical), §7 (說卦傳 — philological).

**Computational boundary reached.** All parameters derived. Open questions are interpretive, not computational.

## File Index

| Script | Computes |
|---|---|
| 01_assignment_test.py | Element assignment uniqueness (240 candidates, conjunction filter) |
| 02_arrangements.py | Compass arrangement scoring (96+1 on 7 metrics) |
| 03_prime_decomposition.py | 後天 uniqueness mechanism (Z₂³ residual, 3 primes) |
| 04_dimensional_forcing.py | n=3 necessity proof (singleton forcing theorem) |
| 05_king_wen_sequence.py | KW sequence analysis (basin clustering, complement pairs) |
| 06_v4_symmetry.py | V₄ group orbits, fiber preservation, anti-palindromes |
| 07_palaces_transform.py | Palace structure, line hierarchy, 体/用 trajectories |
| 08_pairing_torus.py | V₄-compatible pairings (3¹²), torus coverage |
| 09_line_valuations.py | Yaoci valuation by line position, algebraic role, 世 |
| derivation.md | Complete axiom → parameter derivation tree |
| deep-questions.md | 7 structural questions with resolution status |
| exploration-log.md | Iteration-by-iteration research narrative |
