# Magic Square Investigation

## Background

iching/unification/triple-junction.md

## Premise

The Lo Shu (3×3, constant 15 = 3×5) is the spatial face of the triple junction — an independent mathematical object that connects to the trigram algebra through the 後天 compass.

The algebraic structure involves three primes {2, 3, 5}. The natural grid should carry all three, not just one. A 5×5 grid uses only prime 5. The full structure wants 2 × 3 × 5 = 30.

---

## The Objects

### The 2 × 3 × 5 cube (primary)

The complete prime decomposition:
- **Axis of 2:** complement polarity (which representative of a complement pair)
- **Axis of 3:** the three Fano lines H, P, Q through 111
- **Axis of 5:** the five elements

The surjection F₂³ → Z₅ lives in this cube. The 3 lines × 2 polarities = 6 non-Frame trigrams. Each is assigned to one of 5 elements — a marking of 6 cells in the 30-cell cube (one per line×polarity slice).

### The 6 × 5 grid (flattened cube)

Collapse the 2 × 3 axes into 6:
- **Rows (6):** line positions, or 6 non-Frame trigrams, or 3 complement pairs × 2 polarities
- **Columns (5):** the five elements

This is the 六親 assignment space — the operationally central grid in 火珠林. Every hexagram maps 6 lines → 5 relation types.

### The 5 × 5 grid (secondary)

Only uses prime 5:
- **Rows:** lower trigram element
- **Columns:** upper trigram element

The hexagram torus. The Cayley table of Z₅ addition. Magic constant 65 = 5 × 13. A projection that throws away primes 2 and 3.

---

## What to Test

### Phase 1: The 2 × 3 × 5 Cube

#### 1a. Slice sums

A 2×3×5 cube has three families of slices:
- 5 slices of size 2×3 = 6 (fix element)
- 3 slices of size 2×5 = 10 (fix Fano line)
- 2 slices of size 3×5 = 15 (fix polarity)

**Test:** Number the 30 cells 1–30 (or use trigram/element data values). Do any natural numberings produce constant sums across a slice family? What numberings are induced by:
- The He Tu numbers (mod 5 residue on element axis, He Tu pair index on polarity axis)
- The Lo Shu numbers (on the 3-axis via Fano line ↔ Lo Shu position mapping)
- The algebraic Z₅ values (stride structure on element axis)

#### 1b. The surjection as cube marking

The surjection marks 6 of 30 cells (one per row in the 6×5 view). This marking has structure — it's not random.

**Test:** What are the properties of these 6 marked cells?
- Sum of element values at marked cells
- Distribution across Fano lines (H gets type-0, P gets type {2,3}, Q gets type {1,4})
- Symmetry of the marking under cube automorphisms

#### 1c. Complement equivariance as cube symmetry

f(x⊕111) = −f(x) means: swapping polarity (axis of 2) negates the element (axis of 5). This is a combined reflection across two axes.

**Test:** What is the full symmetry group of the marked cube? Does it reduce to something recognizable? The Fano line axis (3) should have S₃ symmetry. The polarity axis (2) has Z₂. The element axis (5) has Aut(Z₅) = Z₄. Total ambient symmetry is Z₂ × S₃ × Z₄ = order 48. What subgroup preserves the surjection marking?

### Phase 2: The 6 × 5 Grid

#### 2a. 六親 as grid marking

Every hexagram marks 6 cells in the 6×5 grid (one per line position). 64 hexagrams = 64 different markings.

**Test:** Classify the 64 markings. How many distinct 六親 profiles exist? Do they tile the grid? Is there a hexagram whose marking has magic-like properties (row sums constant, column sums constant)?

#### 2b. Latin rectangle structure

A 6×5 grid can't be a Latin square (6 ≠ 5). But the 64 hexagram markings collectively cover the grid.

**Test:** Do the 64 hexagram markings produce a balanced structure on the grid? Does each cell get approximately equal total hexagram weight? What's the variance across cells?

#### 2c. The palace structure on the grid

8 palaces × 8 ranks = 64 hexagrams. Each palace has a fixed element. Each rank has a 六親 profile.

**Test:** Do the 8 palaces produce 8 characteristic patterns on the 6×5 grid? Does the 游魂 rank (universal completeness, R: atlas-hzl) correspond to a marking that covers all 5 columns?

### Phase 3: The 5 × 5 Grid (secondary)

#### 3a. Standard magic square placement

The standard Siamese 5×5 magic square on the element-pair torus.

```
17  24   1   8  15
23   5   7  14  16
 4   6  13  20  22
10  12  19  21   3
11  18  25   2   9
```

**Test:** For each placement (element permutation × square symmetry), correlate magic square values with:
- Cell population (fiber sizes: 1, 2, or 4 hexagrams per cell)
- 互 attractor distance
- Basin membership distribution
- Relation type (Cayley table diagonal)

#### 3b. Mod-5 residue pattern

**Test:** Compute magic square values mod 5 on the grid. Does the residue pattern reproduce the Cayley table or any other Z₅ × Z₅ structure?

#### 3c. The center

Center value = 13. Center cell = (Earth, Earth) in algebraic ordering = 同-Earth.

**Test:** Properties of hexagrams in the center cell. Any distinguished behavior?

#### 3d. Cross-reference with Lo Shu

The Lo Shu lives on the 3×3 trigram space. The 5×5 square lives on the element-pair space. Connected by the surjection.

**Test:** Does the surjection F₂³ → Z₅ pull back any 5×5 structure to something compatible with the Lo Shu?

---

## Null Hypotheses

**Cube:** A random numbering of 30 cells will produce constant slice sums with probability depending on the slice family. Compute expected variance under random numbering.

**6×5 grid:** A random assignment of 6 lines to 5 elements produces balanced coverage with probability dependent on the partition. The {2,2,2,1,1} partition is one of 7 possible partitions of 6 into ≤5 parts — is it the most balanced? The most magic-compatible?

**5×5 grid:** With multiple tests × multiple placements × multiple properties, expect spurious correlations. Require conjunction of multiple alignments for significance.

## Priority

Phase 1 (cube) first — uses all three primes. Phase 2 (6×5) second — operationally grounded. Phase 3 (5×5) last — weakest candidate (one prime).

## Method

Write a script that:
1. Constructs the 2×3×5 cube with the surjection marking
2. Tests all slice-sum properties and symmetry groups
3. Constructs the 6×5 grid from 火珠林 六親 data
4. Tests the 5×5 magic square under all valid placements
5. Compares to null distributions

Data inputs:
- `atlas/atlas.json` — 64 hexagram profiles
- `atlas-hzl/hzl_profiles.json` — 六親 assignments
- `unification/synthesis-3.md` — Fano line definitions, fiber partition

Output to `magic/results.md`.

## Possible Outcomes

The cube's symmetry analysis (1c) may yield a clean result — the symmetry group of the marked cube is a definite mathematical object. The 六親 grid analysis connects to established results and may confirm rather than discover.

The interesting finding would be if the cube has a natural numbering with magic-like properties — a 2×3×5 magic cube on the algebraic face, paralleling the Lo Shu on the spatial face.
