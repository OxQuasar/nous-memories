# Magic Square Investigation — Findings

45 results across 4 iterations and 3 phases. See `exploration-log.md` for the full iteration record.

## Central Result

The full 2×3×5 structure does not carry additive (Lo Shu-type) magic properties. Each face of the triple junction carries its own native "magic" — modular, combinatorial, and arithmetic — but these are arithmetically incommensurable. They meet at (3,5) without merging. The three failure modes are prime-indexed: prime 2 antagonizes, prime 3 over-constrains, prime 5 absorbs.

---

## Phase 1: The 2×3×5 Cube (Algebraic Face)

**R1. Sum over all 8 trigrams = (R−1)·p = 15 under algebraic Z₅.** Non-type-0 complement pairs each contribute p as integers; type-0 contributes 0. At (3,5): 3×5 = 15. This equals the Lo Shu magic constant because n²+1 = 2p, which follows from the Mersenne condition 2^{n−1} = n+1 — the same equation that drives the uniqueness theorem.

**R2. The cube actively resists additive magic.** Polarity-magic impossible (465/2 non-integer). Element-magic unfound in 1M random permutations. Line-magic rare (≈1 in 3000). The cube is anti-structured on lines (96th percentile variance).

**R3. The cube's native magic is modular balance.** Complement pairs sum to 0 mod p through the type-0 fixed point (Wood = 0). Structurally parallel to the Lo Shu's additive balance (opposite pairs sum to n²+1 through center 5) but arithmetically incommensurable.

**R4. The stabilizer of the surjection marking is V₄ (Klein four-group), order 4.** Under the algebraic ambient group, only Z₂ survives (complement + negation). The cube is a display of complement equivariance, not an enrichment. Wood and H are universally fixed.

**R5. The affine structure σ₊ = −l mod 5 on the Fano line axis is forced.** The 克 stride maps each negation pair to the other, guaranteeing collinearity. Every choice of orientation representatives yields an affine ordering.

---

## Phase 2: The 6×5 Grid (Operational Face)

### 納甲 Structural Invariants

**R6. ⚡ Earth invariant: every trigram in 納甲 gets exactly 1 Earth element.** Consequence chain: 1 Earth/trigram → 2 Earth/hexagram → Earth column = 128 → per-palace dominant 六親 = Earth's relation to palace element, count exactly 16.

**R7. ⚡ Tripartition: each trigram picks exactly one element from each mod-3 residue class of Z₅.**
- Class 0 mod 3: {Wood=0, Metal=3}
- Class 1 mod 3: {Fire=1, Water=4}
- Class 2 mod 3: {Earth=2}

Forced by stride-2 納甲 branch assignment: gcd(2,3) = 1 covers all mod-3 classes. All hexagram Z₅ sums are multiples of 3 (values: {6, 9, 12, 15, 18}).

**R8. ⚡ The all-5-element condition is a disjointness condition on F₂².** The 4 non-Earth pairs form an F₂² lattice (indexed by: contains Wood?, contains Fire?). A hexagram has all 5 elements iff its lower and upper non-Earth pairs satisfy XOR = (1,1).

**R9. ⚡ The two F₂² diagonals correspond to the two Z₅ strides:**
- Diagonal A (坤/坤): {Wood,Fire}↔{Metal,Water} — 生-adjacent, unequal-sum
- Diagonal B (乾/乾): {Wood,Water}↔{Metal,Fire} — 克-stride, equal-sum (forced by equal factor spread)

The identification is forced by the tripartition and Z₅ labeling, not labeling-dependent.

**R10. ⚡ Yin/yang branch parity maps to 生/克 F₂² diagonal type.** Yang (even) branches → equal-sum diagonal (克-type) → 乾 symmetric. Yin (odd) branches → unequal-sum diagonal (生-type) → 坤 asymmetric. Arithmetic, not philosophy.

### Rank and Distribution Structure

**R11. ⚡ 游魂 (rank 6) maximizes element diversity:** 4/8 all-5, average 4.5 distinct elements. 三世 (rank 3) is the unique minimum: 0/8 all-5, all exactly 4.

**R12. ⚡ 坤 is the sole source of lower/upper asymmetry.** Lower: {Earth, Fire, Wood} = sum 3. Upper: {Earth, Water, Metal} = sum 9. Z₅-complementary triples sharing only Earth. All 7 other trigrams have identical sums in both positions.

**R13. ⚡ Hexagram Z₅ sum mod 5 = exact convolution of trigram sums.** Predicted = actual for all 5 values, 0/64 mismatches. The non-uniform distribution {≡0: 12, ≡1: 6, ≡2: 24, ≡3: 2, ≡4: 20} traces entirely to the trigram sum distribution, which differs lower vs upper only at 坤.

**R14. The trigram surjection element does NOT predict its 納甲 Z₅ sum.** The surjection (algebraic) and 納甲 (operational) faces are structurally independent at the trigram level.

**R15. All 4 zero cells in the 6×5 grid are structurally hard.** Metal impossible at L1, L2, L4 (position 1 of both trigram blocks). Wood impossible at L6 (position 3 of upper block). 26 live cells out of 30.

---

## Phase 3: The 5×5 Torus (Arithmetic Face)

**R16. ⚡ The Siamese 5×5 magic square decomposes as M[i,j] = 5A + B + 1, where A and B use the two Z₅ strides.** A = (i+j+3) mod 5 = relation index (生-stride). B = (i+2j+1) mod 5 = within-tier index (克-stride). Each 五行 relation type gets one tier of 5 consecutive values.

**R17. ⚡ Z₅ has exactly two independent stride types (up to sign): 生 = {1,4} and 克 = {2,3}.** Any coprime Latin square decomposition at n = 5 must use one from each. The magic square construction IS the Z₅ stride structure — it adds no information beyond what 生 and 克 already encode.

**R18. Magic mod 5 is a Latin square with affine structure: (i + 2j + 2) mod 5.** Row stride = 1 (生), column stride = 2 (克).

**R19. Population-magic correlation is zero.** Max |r| = 0.1076 across 14,400 placements. Fiber structure and magic values are independent.

**R20. Lo Shu pullback produces no magic.** Element-level Lo Shu sums {7, 9, 10, 13, 1} have no additive structure. He Tu anti-diagonal constancy is a structural tautology of additive grids.

**R21. Cell populations = outer product of fiber sizes.** Pop(i,j) = fiber(i)×fiber(j). Three values: {1, 2, 4}. Symmetric.

---

## Structural Observations

**S1. The three failure modes are prime-indexed.**
- **2-failure (cube):** Polarity axis makes 465/2 non-integer. Binary structure antagonizes additive balance.
- **3-failure (grid):** Tripartition (from 12 = 4×3) over-constrains the grid. No degrees of freedom for balance.
- **5-failure (torus):** Z₅ has only two stride types. Magic square reduces to tautology.

**S2. Prime 3 appears three times independently.** Fano lines (algebraic), Lo Shu dimension (spatial), branch cycle factor (calendrical: 12 = 4×3). The tripartition exists because the calendrical 3 interacts with Z₅ to create mod-3 residue classes.

**S3. Earth's "center" shifts across faces.** Algebraic center = Wood (Z₅ = 0, identity). Spatial center = Earth (Lo Shu = 5). Operational center = Earth (1 per trigram in 納甲). The incommensurability of the three numbering systems is concrete.

**S4. The Mersenne condition downstream cascade.** 2^{n−1} = n+1 forces: uniqueness of (3,5), n²+1 = 2p, Lo Shu constant = algebraic sum = 15, R−1 = n. All are the same equation.

---

## Files

| File | Content |
|------|---------|
| `exploration-log.md` | Full iteration log (4 iterations, 45 findings) |
| `plan.md` | Original investigation plan |
| `probe_1a.md` | Cube slice sums and magic search |
| `probe_1c.md` | Cube symmetry group |
| `probe_2a.md` | 六親 grid coverage and profiles |
| `probe_2b.md` | Rank structure, zero cells, Z₅ convolution |
| `probe_3.md` | 5×5 torus, magic square, Lo Shu pullback |
| `cube_slice_sums.py` | Probe 1a script |
| `probe_1c_symmetry.py` | Probe 1c script |
| `grid_liuqin.py` | Probe 2a script |
| `probe_2b_rank.py` | Probe 2b script |
| `probe_3_torus.py` | Probe 3 script |
