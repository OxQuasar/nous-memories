# Magic Square Investigation — Exploration Log

## Iteration 1: Probe 1a — Slice Sums of the 2×3×5 Cube

### What was tested

The 2×3×5 cube with axes Polarity(2) × Fano line(3) × Element(5) = 30 cells. The surjection f: F₂³ → Z₅ marks 6 cells (one per polarity-line pair). Tested whether the cube admits additive magic properties (constant slice sums) under various numberings.

**Numberings tested:**
- Lexicographic index (0–29)
- Three element-axis numberings: He Tu mod 5, Lo Shu (odds), Algebraic Z₅
- Product/multiplicative numberings
- Bijection 1–30
- Random permutations of 1–30 (200K for null distribution, 1M for frequency estimates)
- Targeted search via hill-climbing and simulated annealing

**Properties computed:**
- Slice sums across three families: 5 element-slices (6 cells each), 3 line-slices (10 cells each), 2 polarity-slices (15 cells each)
- Null distribution of slice-sum variance under random permutation
- Marked-cell sums under each numbering
- Complement structure and Z₅ negation across Fano lines
- Permutation matrix structure of each polarity slice
- Affine structure of the surjection on the Fano line axis

### What was found

**Proven (from definitions):**

1. **Element-only numberings are trivially line-constant and polarity-constant.** When cell value = f(element), each line and each polarity contains all 5 elements, so slice sums are automatically constant. This is a structural tautology of the balanced cube design — zero information content.

2. **Sum over all 8 trigrams = (R−1)·p under algebraic Z₅.** Each non-type-0 complement pair contributes exactly p as integers (since v + (p−v) = p for v ≠ 0), and the type-0 pair contributes 0. With R = 2^{n−1} complement pairs, total = (R−1)·p. At (3,5): (4−1)·5 = 15. Decomposition: 6 non-Frame cells sum to (R−2)·p = 10, Frame pair sums to p = 5. This holds for all Orbit C surjections, not just the I Ching's specific assignment.

3. **The sum = 15 coincidence with the Lo Shu magic constant follows from the Mersenne condition.** The Lo Shu magic constant = n(n²+1)/2. The algebraic sum = n·p. These are equal iff (n²+1)/2 = p, i.e., n² = 2^{n+1}−7. This follows algebraically from 2^{n−1} = n+1 (the Mersenne condition from the uniqueness theorem): substituting gives 2^{n+1} = 4n+4, so 2^{n+1}−7 = 4n−3, and n² = 4n−3 iff (n−1)(n−3) = 0, giving n = 3. Not an independent coincidence — a downstream consequence of the same arithmetic that makes (3,5) the unique rigid point.

4. **The affine structure σ₊ = −l mod 5 on the Fano line axis is forced by Z₅ arithmetic.** Each polarity slice is a permutation matrix (3 lines → 3 distinct elements). Under line ordering (H,Q,P) = (0,1,2), the positive map is multiplication by 4 ≡ −1 mod 5. The collinearity condition (2v₁ ≡ v₂ mod 5) is automatically satisfied because the 克 stride (multiplication by 2) maps each negation pair to the other. Verified: every choice of orientation representatives yields an affine ordering.

5. **Polarity-magic is impossible.** Sum 1–30 = 465, and 465/2 = 232.5 is not an integer. No permutation of 1–30 can give constant polarity-slice sums.

**Measured (from computation):**

6. **Element-magic is extremely rare; line-magic is rare but findable.** From 1M random permutations of 1–30: line-magic (all line sums = 155) occurred 340 times (0.034%, ≈1 in 2941). Element-magic (all element sums = 93) occurred 0 times (<0.0001%). Element-magic is harder because element slices have only 6 cells (vs 10 for lines) — less room for the law of large numbers.

7. **Doubly-magic numberings exist.** Found via simulated annealing on first attempt: a permutation of 1–30 with all element sums = 93 and all line sums = 155 simultaneously. Extremely rare but feasible.

8. **Bijection (1–30) is mildly anti-structured.** Element variance at 5th percentile of null (mildly low), line variance at 96th percentile (anti-magic on lines).

**Structural observations (from analysis of findings):**

9. **The cube is not a magic object in the additive (Lo Shu) sense.** Its structure actively resists additive balance. The "spatial face" of the triple junction belongs to the Lo Shu's 3×3 grid, not to the 2×3×5 cube.

10. **The cube's native "magic" is complement equivariance — modular balance.** Complement pairs sum to 0 mod p through the type-0 fixed point (Wood = 0). This is structurally parallel to the Lo Shu's additive balance (opposite pairs sum to n²+1 through center 5) but arithmetically incommensurable. The Lo Shu encodes additive balance; the cube encodes modular balance. Same structural pattern, different arithmetic — confirming the triple junction is a genuine junction, not a reduction.

### Scripts and output

- `memories/iching/magic/cube_slice_sums.py` — main probe script
- `memories/iching/magic/probe_1a.md` — full numerical results

---

## Iteration 2: Probes 1c + 2a — Cube Symmetry and 六親 Grid

### What was tested

**Probe 1c:** Symmetry group of the marked cube. Enumerated all elements of S₂ × S₃ × S₅ (order 1440) and the algebraic subgroup Z₂ × S₃ × Aut(Z₅) (order 48), checking which preserve the 6-cell surjection marking.

**Probe 2a:** The 6×5 grid (line position × element) under the 火珠林 system. For each of 64 hexagrams, extracted the 納甲 element assignment to each of 6 line positions. Computed grid coverage, element profiles, 六親 profiles, palace-grouped structure, and structural invariants.

### What was found

**Proven (from definitions / verified exhaustively):**

11. **The stabilizer of the marked cube is V₄ (Klein four-group), order 4.** Generated by two independent involutions:
    - g1: P↔Q line swap + (Fire↔Earth)(Metal↔Water) element double transposition. No polarity change.
    - g2: polarity swap + (Fire↔Water)(Earth↔Metal). This is complement + Z₅ negation (×4 mod 5).

12. **Under the algebraic ambient group (Z₂ × S₃ × Aut(Z₅)), the stabilizer is only Z₂** — just g2 (complement + negation). The g1 element permutation (1 2)(3 4) is NOT in Aut(Z₅) — it is a non-multiplicative involution that preserves the marking but breaks the Z₅ ring structure.

13. **Wood and H are universally fixed** by every symmetry. Wood is the Z₅ identity (0); H carries the unique type-0 pair {震,巽} both mapping to Wood.

14. **The cube is confirmed as a display of complement equivariance, not an enrichment.** Its algebraic symmetry is just Z₂. Phase 1 is complete.

**Measured (from computation on 納甲 data):**

15. **49 distinct element profiles among 64 hexagrams.** Determined uniquely by the (lower, upper) trigram element pattern pair. 7 distinct lower patterns × 7 distinct upper patterns = 49 realized pairs.

16. **Grid coverage is highly structured.** Expected 12.8 per cell if uniform; actual range [0, 24], variance 58.03. Two cells permanently zero: (L1, Metal) and (L2, Metal). Element column sums: Earth=128, Wood=80, Fire=64, Water=64, Metal=48.

17. **59 distinct 六親 profiles** (54 singletons, 5 doublets). 16/64 hexagrams have all 5 六親 types present — the same 16 that have all 5 elements.

18. **六親 line position preferences in lower trigram.** L1 dominated by 父母 (29/64=45%), L2 by 官鬼 (28/64=44%), L3 by 兄弟 (26/64=41%). Upper lines (L4-L6) more balanced.

**Proven (structural invariants of 納甲):**

19. **⚡ Earth invariant: every trigram in 納甲 gets exactly 1 Earth element.** Verified across all 14 trigram patterns (7 lower, 7 upper). Consequence chain: 1 Earth/trigram → 2 Earth/hexagram → Earth column = 128 globally, 16 per palace.

20. **⚡ Per-palace dominant 六親 = 16, explained by Earth chain.** Every palace's most frequent 六親 is exactly 16, and it equals the relation Earth has to the palace element. Verified 8/8 palaces: Wood palaces → 妻財=16, Fire → 子孫=16, Earth → 兄弟=16, Metal → 父母=16, Water → 官鬼=16.

21. **⚡ 納甲 tripartition: each trigram picks exactly one element from each mod-3 residue class of Z₅.** The three classes are:
    - Class 0 mod 3: {Wood=0, Metal=3}
    - Class 1 mod 3: {Fire=1, Water=4}
    - Class 2 mod 3: {Earth=2}

    Trigram Z₅ sum = 2 + (0 or 3) + (1 or 4) ≡ 0 mod 3. Always. This forces all hexagram Z₅ sums to be multiples of 3. The 5 observed hexagram sums are {6, 9, 12, 15, 18}.

22. **The tripartition is forced by the stride-2 structure of 納甲.** Root cause chain:
    1. The 12 earthly branches assign Earth at stride 3 (positions {1,4,7,10}), creating a mod-3 Z₅ structure with period 6 in the branch cycle.
    2. 納甲 assigns branches to trigrams at stride ±2 through the 12-branch cycle (Yang trigrams step forward by 2, Yin step backward by 2).
    3. Since gcd(2,3) = 1, stride-2 sampling covers all 3 mod-3 position classes.
    4. Combined with the sector structure (each 3 consecutive branches contain one element from each mod-3 Z₅ class), this forces each trigram to get exactly {1 Earth, 1 from {Wood,Metal}, 1 from {Fire,Water}}.

23. **Z₅ sum mod 5 distribution is highly non-uniform:** ≡2 (24 hexagrams), ≡4 (20), ≡0 (12), ≡1 (6), ≡3 (2 only). What determines which class a hexagram falls into remains untested.

**Structural observations (from analysis of findings):**

24. **Prime 3 appears three times independently in the system.** As Fano lines (algebraic: 3 lines through center of PG(2,F₂)), as Lo Shu grid dimension (spatial: 3×3), and as branch cycle factor (calendrical: 12 = 4×3). Each produces different structural consequences that happen to align at (3,5). The tripartition exists specifically because the calendrical 3 interacts with Z₅ to create mod-3 residue classes. If the branch cycle were any length not divisible by 3, the tripartition wouldn't exist.

25. **Earth has a dual role: algebraic Z₅=2 (not the identity) vs operational center.** In the algebra, Wood(0) is the identity/fixed point. In 納甲, Earth is the structural constant (1 per trigram, always). In the Lo Shu, Earth(5) is the spatial center. The "center" shifts depending on which face of the triple junction you're looking through — confirming the incommensurability between the three numbering systems.

26. **The stride-2 coincidence between 納甲 (stride 2 in Z₁₂) and 克 (stride 2 in Z₅) is notational, not structural.** They operate in different cyclic groups. The Z₁₂ stride connects to the tripartition through CRT: Z₁₂ ≅ Z₃ × Z₄, and the Z₃ component has stride 2, which generates all of Z₃ since gcd(2,3)=1. This has nothing to do with the 克 cycle in Z₅.

### Scripts and output

- `memories/iching/magic/probe_1c_symmetry.py` — cube symmetry computation
- `memories/iching/magic/probe_1c.md` — symmetry group results
- `memories/iching/magic/grid_liuqin.py` — 六親 grid analysis
- `memories/iching/magic/probe_2a.md` — full 六親 grid results

---

## Iteration 3: Probe 2b — Palace Rank Structure, Zero Cells, Z₅ Sum Distribution

### What was tested

**Part 1:** Zero cells in the 6×5 grid — traced to 納甲 branch assignments to determine which are structurally hard (no trigram can produce them) vs soft.

**Part 2:** Rank structure of the 16 all-5-element hexagrams — tested whether 游魂 (rank 6) concentrates all-5 hexagrams, and whether rank predicts element diversity.

**Part 3:** Z₅ sum mod 5 distribution — cross-tabulated with palace element and rank. Decomposed hexagram Z₅ sums into trigram-level convolution. Tested whether trigram surjection element predicts 納甲 Z₅ sum.

### What was found

**Proven (from exhaustive enumeration of 納甲 branch assignments):**

27. **All 4 zero cells in the 6×5 grid are structurally hard.** No trigram in the 納甲 system can produce them:
    - (L1, Metal), (L2, Metal), (L4, Metal): Metal is impossible at position 1 of both trigram blocks. Metal branches (申, 酉) only appear at positions 2–3 in 納甲 branch sequences.
    - (L6, Wood): Wood is impossible at position 3 of the upper trigram block.
    
    The grid has 26 live cells out of 30. The structural possibility matrix (how many of 8 trigrams produce each cell) ranges from 0 to 3.

28. **⚡ 游魂 (rank 6) maximizes element diversity: 4/8 all-5, average 4.5 distinct elements.** This is the unique maximum across all 8 ranks. 三世 (rank 3) is the unique minimum: 0/8 all-5, all hexagrams have exactly 4 elements.

29. **⚡ The all-5-element condition is a disjointness condition on F₂².** By the tripartition, each trigram's non-Earth pair is one of 4 possibilities: {Wood,Fire}, {Wood,Water}, {Metal,Fire}, {Metal,Water}. These form an F₂² lattice indexed by (contains Wood?, contains Fire?). A hexagram has all 5 elements iff its lower and upper non-Earth pairs are **disjoint** — i.e., XOR = (1,1) in F₂².

30. **⚡ The two F₂² diagonals correspond to the two Z₅ strides, realized by 坤 and 乾.**
    - **Diagonal A (坤/坤):** {Wood,Fire}↔{Metal,Water} — the Z₅ negation pairs. Unequal-sum pairs (Z₅ pair sums differ: 0+1=1 vs 3+4=7). 生-adjacent within Z₅\{Earth}.
    - **Diagonal B (乾/乾):** {Wood,Water}↔{Metal,Fire} — the Z₅ 克-stride pairs. Equal-sum pairs (Z₅ pair sums match: 0+4=4 and 3+1=4).
    
    The equal-sum property of diagonal B is forced: the two tripartition factors {Wood=0, Metal=3} and {Fire=1, Water=4} have equal spread (both 3 in Z₅), so cross-swapping cancels. The identification of diagonals with strides is forced by the tripartition and Z₅ labeling, not labeling-dependent.

**Proven (from trigram-level Z₅ sum analysis):**

31. **⚡ The hexagram Z₅ sum mod 5 distribution is exactly predicted by trigram-level convolution.** Each trigram has Z₅ sum ∈ {3, 6, 9} (always ≡ 0 mod 3). The hexagram sum = lower + upper → convolution gives {6:6, 9:20, 12:24, 15:12, 18:2}. Predicted = actual for all 5 values (0/64 mismatches).

32. **⚡ 坤 is the sole source of lower/upper asymmetry.** All 7 other trigrams have identical Z₅ sums in lower and upper positions. Only 坤 differs: lower (stem 乙) → {Earth, Fire, Wood} = sum 3; upper (stem 癸) → {Earth, Water, Metal} = sum 9. These are Z₅-complementary triples sharing only Earth: {0,1,2} and {2,3,4}, related by translation by −Earth (= +3 mod 5).

33. **⚡ Yin/yang branch parity maps to 生/克 F₂² diagonal type.**
    - 乾 (yang branches, even indices): lower {Wood,Water}, upper {Fire,Metal} → equal-sum diagonal (克-type) → Z₅ sum symmetric (6 in both positions).
    - 坤 (yin branches, odd indices): lower {Wood,Fire}, upper {Metal,Water} → unequal-sum diagonal (生-type) → Z₅ sum asymmetric (3 vs 9).
    
    The yang branch cycle distributes elements so each half-cycle's non-Earth pair falls on the equal-sum (balanced) diagonal. The yin cycle produces unequal-sum (differentiated) pairs. This is arithmetic: the even-branch subsequence's element distribution cancels Z₅ sum differences across positions; the odd-branch subsequence does not.

34. **The trigram surjection element does NOT predict its 納甲 Z₅ sum.** Both 兌(Metal=3) and 坎(Water=4) have sum=3, while 乾(Metal=3) has sum=6. The surjection (algebraic face) and 納甲 (operational face) are structurally independent at the trigram level.

**Measured (from cross-tabulation):**

35. **Z₅ sum mod 5 is not cleanly predicted by palace element or rank alone.** The cross-tabulations show structure but no simple rule. The non-uniform distribution traces entirely to the non-uniform trigram sum distribution: lower {3:3, 6:4, 9:1}, upper {3:2, 6:4, 9:2}, which differ only at 坤.

### Scripts and output

- `memories/iching/magic/probe_2b_rank.py` — rank structure and Z₅ sum analysis
- `memories/iching/magic/probe_2b.md` — full results

---

## Iteration 4: Probe 3 — The 5×5 Element-Pair Torus

### What was tested

The 5×5 grid where rows = lower trigram surjection element, columns = upper trigram surjection element (both in algebraic Z₅ order). Cell (i,j) contains all hexagrams whose lower and upper trigram elements are i and j respectively. Tested magic square placement, mod-5 residue structure, center cell properties, and Lo Shu pullback.

**Specifically tested:**
- Cell populations and their relation to fiber sizes
- Correlation between Siamese 5×5 magic square values and cell populations across all 14,400 row/column permutations
- Whether any placement produces constant relation-type magic sums
- Decomposition of the Siamese square into orthogonal Latin squares
- Mod-5 residue pattern of the magic square — is it a Latin square? What affine structure?
- Center cell (Earth, Earth) hexagram properties
- Lo Shu element-level sums via surjection pullback
- He Tu additive and multiplicative grids on the torus

### What was found

**Proven (from the Siamese construction):**

36. **⚡ The Siamese 5×5 magic square decomposes as M[i,j] = 5A[i,j] + B[i,j] + 1, where A and B are orthogonal Latin squares built from the two Z₅ strides.**
    - A[i,j] = (i + j + 3) mod 5 — the Z₅ Cayley addition table shifted by 3 = the 五行 relation index
    - B[i,j] = (i + 2j + 1) mod 5 — row stride 1 (生), column stride 2 (克)
    
    A sorts cells into tiers by 五行 relation type. B distributes values within each tier using the 克 stride.

37. **⚡ Each 五行 relation type receives exactly one tier of 5 consecutive magic values:**

    | Relation | d=(i+j)%5 | Tier | Values | Sum |
    |----------|-----------|------|--------|-----|
    | 克(妻財) | 2 | 0 | {1–5} | 15 |
    | 被克(官鬼) | 3 | 1 | {6–10} | 40 |
    | 被生(父母) | 4 | 2 | {11–15} | 65 |
    | 同(兄弟) | 0 | 3 | {16–20} | 90 |
    | 生(子孫) | 1 | 4 | {21–25} | 115 |

    The tier ordering (克 lowest → 生 highest) is forced by the Siamese starting rule: the algorithm places 1 at row 0, column ⌊n/2⌋ = 2, which has relation distance (0+2) mod 5 = 2 = 克. The Siamese starts at maximum-stride distance, which for n=5 is the 克 stride.

38. **⚡ The magic square mod 5 is a Latin square with affine structure: M mod 5 = (i + 2j + 2) mod 5.** Row successive difference = 1 (生 stride). Column successive difference = 2 (克 stride). Both fundamental 五行 cycle operations are embedded in the mod-5 residue pattern.

39. **⚡ Z₅ has exactly two independent stride types (up to sign): 生 = {1, 4} and 克 = {2, 3}.** Any coprime Latin square decomposition of a 5×5 magic square must use one stride from each type. The standard Siamese uses (1, 2) — the canonical representatives. The magic square construction IS the Z₅ stride structure: magic = 生 × 克 is the only structural option at n = 5.

**Measured (from exhaustive search):**

40. **Population-magic correlation is essentially zero.** Max |r| = 0.1076 across 14,400 placements, vs null distribution mean = 0, std = 0.053. The fiber structure (algebraic) and magic values (arithmetic) are independent.

41. **200/14400 placements (1.4%) produce constant relation-type sums (= 65 for all 5 types).** These are placements where the column permutation is a "complete mapping" of Z₅ for both strides simultaneously.

**Verified (from Lo Shu pullback):**

42. **Cell populations are exactly the outer product of fiber sizes:** Pop(i,j) = fiber(i) × fiber(j). Fiber sizes: Wood=2, Fire=1, Earth=2, Metal=2, Water=1. Three distinct population values: {1, 2, 4}.

43. **Lo Shu element-level sums are {Wood=7, Fire=9, Earth=10, Metal=13, Water=1}.** No magic property. Metal=13 = center magic value is arithmetic coincidence (not robust under Lo Shu dihedral symmetry). Singleton-fiber elements trivially inherit their Lo Shu values (Fire=9=離, Water=1=坎).

44. **He Tu additive grid has constant anti-diagonal sums (= 110) — structural tautology.** Any additive grid f(i)+g(j) has constant cyclic anti-diagonal sums (= Σf + Σg). Not informative. Population-weighted He Tu sums DO vary: {344, 272, 306, 302, 280}.

45. **Center cell (Earth, Earth) contains 4 hexagrams:** 坤坤 (hex 0, 本宮), 艮坤 (hex 4, rank 5), 坤艮 (hex 32, rank 5), 艮艮 (hex 36, 本宮). The 2×2 grid of Earth-mapping trigrams {坤, 艮}. Magic value = 13 = median of 1–25.

### Scripts and output

- `memories/iching/magic/probe_3_torus.py` — torus analysis script
- `memories/iching/magic/probe_3.md` — full results

---

## Investigation Summary

### Central question

Does the full 2×3×5 structure (the product of the three primes 2, 3, 5 that characterize the I Ching's algebraic backbone) carry magic properties beyond the Lo Shu's 3×3?

### Answer

Each face of the triple junction carries its own native "magic," but these are arithmetically incommensurable — they meet at (3,5) without merging.

| Phase | Object | Native "magic" | Additive magic? |
|-------|--------|---------------|-----------------|
| 1 | 2×3×5 cube | Complement equivariance (modular balance) | No — actively resists |
| 2 | 6×5 grid | Earth invariant + tripartition (combinatorial constraint) | No — too constrained by 納甲 |
| 3 | 5×5 torus | 生×克 decomposition (coprime stride arithmetic) | Only what Z₅ forces |

The spatial face (Lo Shu) doesn't extend to higher-dimensional objects. The cube's magic is modular, the grid's is combinatorial, the torus's is arithmetic. The consistent negative across all three phases — the cube resists additive magic, the grid is over-constrained, the torus produces only forced structure — constitutes positive evidence that the incommensurability is real.

### Top findings (ranked by structural content)

1. **The Siamese magic square = 生 × 克.** The construction necessarily uses both fundamental Z₅ strides. At n = 5 there is no other option. (Finding 36–39)

2. **The Earth invariant and its consequences.** Every trigram in 納甲 gets exactly 1 Earth → every palace's dominant 六親 is Earth's relation to the palace element, count exactly 16. A structural fact about 納甲 not previously articulated. (Findings 19–20)

3. **The F₂² lattice and yin/yang → 生/克 mapping.** Non-Earth pairs form F₂²; the two diagonals correspond to the two Z₅ strides. Yang branches produce equal-sum (克-type) pairs; yin produce unequal-sum (生-type). The two primordial hexagrams (乾/乾, 坤/坤) realize the two diagonals. Yin/yang at the calendar level maps to 生/克 at the algebraic level — arithmetic, not philosophy. (Findings 29–30, 33)

4. **The cube's modular magic = complement equivariance.** Reframing "magic" from additive to modular: complement pairs sum to 0 mod p through the type-0 fixed point. Structurally parallel to Lo Shu's additive balance but incommensurable. (Finding 10)

5. **Sum = 15 = n·p follows from the Mersenne condition.** The Lo Shu magic constant and the algebraic trigram sum coincide because n²+1 = 2p, which is downstream of 2^{n−1} = n+1. Same equation, different face. (Finding 3)

6. **Prime 3 appears three times independently:** Fano lines (algebraic), Lo Shu dimension (spatial), branch cycle factor (calendrical). The tripartition exists because the calendrical 3 interacts with Z₅. (Finding 24)

7. **Earth's center shifts across faces.** Wood(0) is algebraic center; Earth(5) is spatial center; Earth is operational center (1 per trigram in 納甲). The incommensurability is concrete. (Finding 25)

8. **坤 is the sole source of lower/upper asymmetry.** All other trigrams have identical Z₅ sums in both positions. 坤's complementary triples {0,1,2} and {2,3,4} break the symmetry. (Finding 32)

### All scripts

| File | Purpose |
|------|---------|
| `memories/iching/magic/cube_slice_sums.py` | Probe 1a: cube slice sums |
| `memories/iching/magic/probe_1c_symmetry.py` | Probe 1c: cube symmetry group |
| `memories/iching/magic/grid_liuqin.py` | Probe 2a: 六親 grid analysis |
| `memories/iching/magic/probe_2b_rank.py` | Probe 2b: rank structure and Z₅ sums |
| `memories/iching/magic/probe_3_torus.py` | Probe 3: 5×5 torus analysis |

### All results

| File | Content |
|------|---------|
| `memories/iching/magic/probe_1a.md` | Cube slice sums and magic search |
| `memories/iching/magic/probe_1c.md` | Cube symmetry group |
| `memories/iching/magic/probe_2a.md` | 六親 grid coverage and profiles |
| `memories/iching/magic/probe_2b.md` | Rank structure, zero cells, Z₅ convolution |
| `memories/iching/magic/probe_3.md` | 5×5 torus, magic square, Lo Shu pullback |

---

## Final Synthesis

### The shape of the negative result

The three faces don't just fail to unify — they fail in structurally different ways, indexed by the three primes:

- **2-failure (cube):** The polarity axis (size 2) makes 465/2 non-integer → polarity-magic impossible. The binary structure actively antagonizes additive balance.
- **3-failure (grid):** The tripartition (from 12 = 4×3) over-constrains the grid. Earth gets 1 per trigram because the calendrical 3 forces mod-3 coverage. No degrees of freedom remain for balance.
- **5-failure (torus):** Z₅ has only two independent stride types (生 and 克). The magic square consumes both, reducing to a tautology. The prime 5 makes the magic square identical to the algebra.

Each prime prevents unification in its own characteristic way. This is itself evidence for the triple junction's structure — if the faces were unrelated, their failure modes would be arbitrary. Instead, each fails in a way characteristic of its prime content.

### What extends beyond the magic square question

1. **The Earth invariant** (R6) constrains all 六親 analysis. Any future work on 火珠林 should account for Earth's operational privilege: 1 per trigram, 2 per hexagram, dominant 六親 always Earth's relation to the palace element.

2. **The yin/yang → 生/克 mapping** (R10) is a concrete triple-junction interaction: calendrical structure (branch parity) determines algebraic structure (stride type) through Z₅ arithmetic.

3. **The Siamese = 生 × 克** (R16–R17) closes the magic square question: the 5×5 magic square IS the Z₅ stride structure, adding no information beyond what the algebra already contains.

### What remains open

The investigation confirms the incommensurability but doesn't explain why three independent structural traditions all use the same prime pair (3,5). The Mersenne condition explains the algebra. The Lo Shu's primality is well-understood. But the calendrical 12 = 4×3 with stride-2 element assignments is a historical/design question. A counterfactual test (10-branch cycle, factoring as 2×5) would break the tripartition and Earth invariant, confirming the calendrical 3 is load-bearing.

See `findings.md` for the consolidated result summary and `questions.md` for open questions.
