# Probe 1a: Slice Sums of the 2×3×5 Cube

## Executive Summary

**Key findings:**

1. **Element-only numberings are trivially line-constant and polarity-constant.** When cell value = f(element), the line and polarity slices are automatically constant because each line contains all 5 elements and each polarity contains all 5 elements. The element slices simply reflect the non-uniformity of f. This is a structural tautology, not a constraint.

2. **Z₅ negation is exact.** The complement equivariance f(x⊕111) = -f(x) mod 5 is verified across all three Fano lines. The two polarity slices are exact Z₅ negations of each other: σ₋ = -σ₊ mod 5.

3. **Algebraic Z₅ total over all 8 trigrams = 15** (the Lo Shu magic constant). This decomposes as: 6 cube cells sum to 10, frame pair sums to 5.

4. **Bijection (1–30) has element variance at the 5th percentile** of the random null — mildly low but not extreme. Its line variance is at the 96th percentile — anti-magic on lines.

5. **Doubly-magic numberings (element=93 AND line=155) exist** but are extremely rare. Found via simulated annealing. Line-magic alone occurs at ≈0.034%; element-magic alone at <0.0001% of random permutations.

6. **The surjection marking has clean permutation structure:** each polarity slice maps 3 lines to 3 distinct elements, and the two slices are related by Z₅ negation. Under line ordering (H,Q,P), the positive map is σ₊ = 4l mod 5.

---

## 1. Slice Sums Under Natural Numberings

### 1a. Lexicographic index (0–29)

  element: Wood=75, Fire=81, Earth=87, Metal=93, Water=99
  line: H=95, P=145, Q=195
  polarity: pos=105, neg=330

Total: 435

### 1b. Element-axis numberings (value = element number)

Each cell's value equals the element number under the given system.

**He Tu mod 5:** Wood=3, Fire=2, Earth=0, Metal=4, Water=1
  element: Wood=18, Fire=12, Earth=0, Metal=24, Water=6
  line: H=20, P=20, Q=20 ✓ CONSTANT
  polarity: pos=30, neg=30 ✓ CONSTANT

**Lo Shu (odds):** Wood=3, Fire=9, Earth=5, Metal=7, Water=1
  element: Wood=18, Fire=54, Earth=30, Metal=42, Water=6
  line: H=50, P=50, Q=50 ✓ CONSTANT
  polarity: pos=75, neg=75 ✓ CONSTANT

**Algebraic Z₅:** Wood=0, Fire=1, Earth=2, Metal=3, Water=4
  element: Wood=0, Fire=6, Earth=12, Metal=18, Water=24
  line: H=20, P=20, Q=20 ✓ CONSTANT
  polarity: pos=30, neg=30 ✓ CONSTANT

### 1c. Product / bijection numberings

**Bijection (1–30):** value = p×15 + l×5 + e + 1
  element: Wood=81, Fire=87, Earth=93, Metal=99, Water=105
  line: H=105, P=155, Q=205
  polarity: pos=120, neg=345
Total: 465

**Multiplicative:** value = (2p+1) × (l+1) × algebraic[e]
  element: Wood=0, Fire=24, Earth=48, Metal=72, Water=96
  line: H=40, P=80, Q=120
  polarity: pos=60, neg=180
Total: 240

**Multiplicative shifted:** value = (2p+1) × (l+1) × (algebraic[e]+1)
  element: Wood=24, Fire=48, Earth=72, Metal=96, Water=120
  line: H=60, P=120, Q=180
  polarity: pos=90, neg=270
Total: 360

## 2. Magic Numbering Search

Sum 1–30 = 465
Element-constant target: 465/5 = 93.0
Line-constant target: 465/3 = 155.0
Polarity-constant target: 465/2 = 232.5 — NOT INTEGER, impossible

### Null distribution (200K random permutations of 1–30)
Element variance: mean=371.8, median=323.6, min=0.4, P(var=0)=0.0000%
Line variance: mean=517.8, median=370.7, min=0.0, P(var=0)=0.0305%
Element max-dev: mean=29.2, median=29.0, min=1.0
Line max-dev: mean=27.4, median=26.0, min=0.0

### Traditional numberings vs null distribution

For each element numbering, broadcast to all 30 cells, compute slice variances,
and compare against random permutation null.

**He Tu mod 5:**
  Element slices: {0: 18, 1: 12, 2: 0, 3: 24, 4: 6} — var=72.00
  Line slices: {0: 20, 1: 20, 2: 20} — var=0.00 ✓ CONSTANT
  Polarity slices: {0: 30, 1: 30} — var=0.00 ✓ CONSTANT

**Lo Shu (odds):**
  Element slices: {0: 18, 1: 54, 2: 30, 3: 42, 4: 6} — var=288.00
  Line slices: {0: 50, 1: 50, 2: 50} — var=0.00 ✓ CONSTANT
  Polarity slices: {0: 75, 1: 75} — var=0.00 ✓ CONSTANT

**Algebraic Z₅:**
  Element slices: {0: 0, 1: 6, 2: 12, 3: 18, 4: 24} — var=72.00
  Line slices: {0: 20, 1: 20, 2: 20} — var=0.00 ✓ CONSTANT
  Polarity slices: {0: 30, 1: 30} — var=0.00 ✓ CONSTANT

### Bijection (1–30) against null

Element var=72.0, percentile=5.19%
Line var=1666.7, percentile=96.42%
Polarity var=12656.2

### Targeted search: element-magic numberings (sum=93 per element slice)

Best element variance after 500000 hill-climbing steps: 2
  Element sums: [94, 93, 93, 93, 92]

### Targeted search: line-magic numberings (sum=155 per line slice)

FOUND line-magic numbering!
  element: Wood=67, Fire=72, Earth=89, Metal=98, Water=139
  line: H=155, P=155, Q=155 ✓ CONSTANT
  polarity: pos=216, neg=249

### Targeted search: doubly-magic (element=93 AND line=155)

FOUND via simulated annealing (first attempt):
  Element sums: [93, 93, 93, 93, 93] ✓
  Line sums: [155, 155, 155] ✓

Doubly-magic numberings exist. They are rare but findable.

### Exact frequency from 1M random permutations

  Line-magic (all sums = 155): 340/1M = 0.034%  (≈1 in 2941)
  Element-magic (all sums = 93): 0/1M = <0.0001%  (very rare)
  Both simultaneously: 0/1M  (extremely rare)

Element-magic is much harder than line-magic because element slices have
only 6 cells each (vs 10 for line slices) — less room for the law of large numbers.

## 3. Marked-Cell Numbering

The 6 marked cells and their positions:

| Polarity | Line | Element | Trigram |
|----------|------|---------|---------|
| pos | H | Wood | 震 |
| neg | H | Wood | 巽 |
| pos | Q | Water | 坎 |
| neg | Q | Fire | 離 |
| pos | P | Metal | 兌 |
| neg | P | Earth | 艮 |

### Sum of marked-cell values under each element numbering

**He Tu mod 5:** values = [3, 3, 1, 2, 4, 0], sum = 13
**Lo Shu (odds):** values = [3, 3, 1, 9, 7, 5], sum = 28
**Algebraic Z₅:** values = [0, 0, 4, 1, 3, 2], sum = 10

### Lexicographic indices of marked cells

Indices: [0, 15, 14, 26, 8, 22]
Sum of indices: 85
Sum + 6 (if 1-based): 91

### Bijection (1–30) values at marked cells

Values: [1, 16, 15, 27, 9, 23]
Sum: 91

### Distribution of marked cells across axes

By element: Wood=2, Fire=1, Earth=1, Metal=1, Water=1
By line: H=2, P=2, Q=2
By polarity: pos=3, neg=3

### Surjection pattern on the element axis

Marked elements: Wood(×2), Fire(×1), Earth(×1), Metal(×1), Water(×1)
This is a surjection 6→5 with exactly one double-hit at Wood.

### Complement structure of marked elements

Complement pairs on Fano lines (polarity 0 vs 1):
  H: Wood(0) ↔ Wood(0), sum mod 5 = 0, diff mod 5 = 0
  P: Metal(3) ↔ Earth(2), sum mod 5 = 0, diff mod 5 = 1
  Q: Water(4) ↔ Fire(1), sum mod 5 = 0, diff mod 5 = 3

### Z₅ negation on complement pairs

If complement → Z₅ negation, then f(comp) = -f(orig) mod 5:
  H: f(pos)=0, -f(pos) mod 5 = 0, f(neg)=0 → MATCH
  P: f(pos)=3, -f(pos) mod 5 = 2, f(neg)=2 → MATCH
  Q: f(pos)=4, -f(pos) mod 5 = 1, f(neg)=1 → MATCH

### Frame pair context

Frame: 坤(000)→Earth(2), 乾(111)→Metal(3)
Sum: 2+3 = 5 ≡ 0 mod 5
Under He Tu: Earth=0, Metal=4 → sum = 4
Under Lo Shu: Earth=5, Metal=7 → sum = 12

### Comparison to known constants

**He Tu mod 5:** marked sum=13, frame sum=4, total=17
**Lo Shu (odds):** marked sum=28, frame sum=12, total=40
**Algebraic Z₅:** marked sum=10, frame sum=5, total=15

Reference constants: 15 (magic constant of Lo Shu 3×3), 30 (2×15), 65 (sum 1–10 He Tu)

**⚡ NOTABLE:** Under Algebraic Z₅, the sum over ALL 8 trigrams = 15 (the Lo Shu magic constant).
  All 8 trigram values: 坤(2)+震(0)+坎(4)+兌(3)+艮(2)+離(1)+巽(0)+乾(3) = 15
  Decomposition: 6 marked cells sum to 10, frame pair sums to 5, total = 15.

## 4. Structural Observations

### Marked cell positions in cube

```
        Wood  Fire  Earth Metal Water
pos H:   [X]   .     .     .     .
pos P:   .     .     .    [X]    .
pos Q:   .     .     .     .    [X]
neg H:   [X]   .     .     .     .
neg P:   .     .    [X]    .     .
neg Q:   .    [X]    .     .     .
```

### Is the marking a permutation matrix on (line, element)?
Per polarity slice, 3 cells are marked in 3 lines. For a permutation matrix,
we'd need distinct elements in each polarity slice.

Positive polarity elements: ['Wood', 'Metal', 'Water'] → distinct
Negative polarity elements: ['Wood', 'Fire', 'Earth'] → distinct

### Element indices at marked cells (algebraic Z₅)

Polarity 0: lines→elements = [('H', 'Wood', 0), ('P', 'Metal', 3), ('Q', 'Water', 4)]
Polarity 1: lines→elements = [('H', 'Wood', 0), ('P', 'Earth', 2), ('Q', 'Fire', 1)]

### Z₅ negation structure (EXACT)

Each polarity slice is a permutation matrix (3 lines → 3 distinct elements):
  Positive: H→Wood(0), P→Metal(3), Q→Water(4)  →  {0, 3, 4} = {0, -2, -1} mod 5
  Negative: H→Wood(0), P→Earth(2), Q→Fire(1)   →  {0, 2, 1} = {0, +2, +1} mod 5

The negative slice is EXACTLY the Z₅ negation of the positive slice:
  σ₋(l) = -σ₊(l) mod 5, for every line l.

This is forced by complement equivariance f(x⊕111) = -f(x) mod 5.

**Affine structure:** Under line ordering (H,Q,P) = (0,1,2):
  σ₊ = 4l mod 5, i.e. σ₊ is multiplication by 4 (= -1 mod 5) on Z₅
  Specifically: σ₊(0)=0, σ₊(1)=4, σ₊(2)=3

### Arithmetic relations among marked element values

**He Tu mod 5:**
  pol=0: values=[3, 4, 1], sum=8, diffs=[1, -3], sum mod 5 = 3
  pol=1: values=[3, 0, 2], sum=5, diffs=[-3, 2], sum mod 5 = 0

**Lo Shu (odds):**
  pol=0: values=[3, 7, 1], sum=11, diffs=[4, -6], sum mod 5 = 1
  pol=1: values=[3, 5, 9], sum=17, diffs=[2, 4], sum mod 5 = 2

**Algebraic Z₅:**
  pol=0: values=[0, 3, 4], sum=7, diffs=[3, 1], sum mod 5 = 2
  pol=1: values=[0, 2, 1], sum=3, diffs=[2, -1], sum mod 5 = 3
