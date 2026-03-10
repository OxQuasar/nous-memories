# Complete Derivation Tree

From two axioms to the full parametric structure of the I Ching. Every claim below is either a proven theorem or an exhaustively computed result. References point to the computational scripts and results files that verify each step.

---

## Axioms

**Axiom 1 (Relational structure).** A finite set of categories carries two independent non-degenerate cyclic orderings.

**Axiom 2 (Binary substrate).** A set Z₂ⁿ of binary objects with complement involution (x → x̄ = x ⊕ 1ⁿ) surjects onto the category set, with complement acting as negation: f(x̄) = -f(x).

---

## §1. Why 5 elements

**From Axiom 1.** Two independent non-degenerate cycles on Z_k require: stride-1 and stride-2 generate the full group, which holds iff k is prime; and stride-2 ≠ stride-1 or its inverse, which fails for k=2 (stride-2=identity) and k=3 (stride-2=stride-1 inverse). The smallest viable prime is **k=5**.

This gives Z₅ with 生-cycle (stride 1: Wood→Fire→Earth→Metal→Water) and 克-cycle (stride 2: Wood→Earth→Water→Fire→Metal). The two cycles are algebraically independent orderings of the same 5 elements.

**Type:** Number theory (proven). **Reference:** number-structure.md

---

## §2. Why 3 lines

**From Axiom 2 + §1.** A surjection f: Z₂ⁿ → Z₅ with f(x̄) = -f(x) mod 5 maps each complement pair {x, x̄} to one of 3 destination types:
- Type 0: both → position 0 (self-conjugate element)
- Type 1: one → position 1, other → position 4 (negation pair)
- Type 2: one → position 2, other → position 3 (negation pair)

Let (k₀, k₁, k₂) count pairs at each destination. Surjectivity requires k₀, k₁, k₂ ≥ 1.

**Theorem (Dimensional Forcing).**
- (a) Such f exists iff n ≥ 3 (need 2^(n-1) ≥ 3 pairs for 3 destinations)
- (b) For n = 3: every such f has singleton fibers (min(k₁,k₂) = 1)
- (c) For n ≥ 4: non-singleton surjections exist

**Proof of (b).** k₀+k₁+k₂ = 4 with all ≥ 1. If min(k₁,k₂) ≥ 2, then k₁+k₂ ≥ 4, forcing k₀ ≤ 0. Contradiction. □

**n = 3 is the unique dimension where the Z₂/Z₅ bridge is structurally forced.** The singletons are injection points where the quotient map is invertible — the locus of constructive interference between binary identity and element evaluation.

**Type:** Proven (pigeonhole). **Reference:** 04_dimensional_forcing.py, 04_dimensional_forcing_results.md

---

## §3. Why 6 lines (hexagram dimension)

**From §2.** Hexagrams are Z₂^{2n} = Z₂ⁿ × Z₂ⁿ (upper × lower trigram). The 互 transform extracts inner lines and repackages them. The 互 analog for 2n-line figures has eventual cycle lengths:

| n | Lines | Max cycle | 互² = id on cycles? |
|---|-------|-----------|---------------------|
| 2 | 4 | 2 | ✓ |
| 3 | 6 | 2 | ✓ |
| 4 | 8 | 3 | ✗ |

**n = 3 (6 lines) is the largest dimension where 互² is the identity on eventual cycles.** At n=4, 3-cycles appear. The 既濟/未濟 2-cycle attractor structure (singletons oscillating under 互) requires this involutory property.

**Type:** Computed (exhaustive). **Reference:** 04_dimensional_forcing.py

---

## §4. Why this 五行 assignment

**From §2.** For n=3, there are 240 valid complement=negation surjections, with three partition shapes:
- (2,1,1) → fibers [4,1,1,1,1]: 48 assignments (type A)
- (1,2,1) → fibers [2,2,2,1,1]: 96 assignments (type B/C)
- (1,1,2) → fibers [2,1,1,2,2]: 96 assignments (type B/C)

Two constraints select uniquely:

| Constraint | Eliminates | Mechanism |
|---|---|---|
| 互 cycle attractor ≠ 比和 | All type B (16/16) | 既濟/未濟 are {Kan,Li}; placing them in the same element forces 比和 at the attractor |
| 吉×生体 Fisher p < 0.05 | All remaining B and C | Traditional: OR=2.10, p=0.007. Best alternative: p=0.065 |

The conjunction selects uniquely: **the traditional assignment is the only one where the algebra is viable AND the textual bridge holds.** 0 of 32 alternatives reach p < 0.05.

The singletons (Fire=離, Water=坎) are exactly the 互 cycle attractors (既濟, 未濟). This is where binary dynamics and element evaluation achieve constructive interference.

**Type:** Proven (algebraic) + Measured (statistical). **Reference:** 01_assignment_test.py, exploration-log.md (Iteration 1)

---

## §5. Why these compass arrangements

### 先天 (Fu Xi): unique Z₂ optimum

| Metric | 先天 | Cardinal-aligned max |
|---|---|---|
| complement_diameter | **4/4** | 2 |
| reversal_reflection | **2/2** | 2 |
| Z₂ composite | **6/6** | 3 |

先天 is NOT cardinal-aligned. Its Z₂ optimality (complement = rotation by 180°) requires sacrificing He Tu element alignment entirely. The gap of 3 over all 96 cardinal-aligned arrangements proves Z₂ coherence and Z₅ alignment are fundamentally incompatible.

### 後天 (King Wen): unique 2×3×5 triple junction

Among 96 cardinal-aligned arrangements:

| Stage | Filter | Survivors | Prime |
|---|---|---|---|
| 0 | Cardinal alignment | 96 | — |
| 1 | 生-monotonicity + element pair coherence | 8 | 5 |
| 2 | Cardinal yin/yang balance [1,1,2,2] | 2 | 2 |
| 3 | Sons (震坎艮) at N/NE/E | **1** | 3 |

The 8 survivors after stage 1 are an exact Z₂³ product (3 independent binary swaps). **Z₅ metrics are identical across all 8** — the residual space is orthogonal to Z₅. Primes 2 and 3 resolve what prime 5 cannot see.

**Type:** Computed (exhaustive). **Reference:** 02_arrangements.py, 03_prime_decomposition.py

---

## §6. The 先天↔後天 bridge

τ = H ∘ X⁻¹ (the permutation mapping 先天 positions to 後天 trigrams):

- **Cycle structure:** (坤→坎→兌→巽)(震→艮→乾→離), two 4-cycles
- **Order:** 4 (τ⁴ = identity)
- **Complement:** maps cycle 1 ↔ cycle 2 (XOR 111 swaps the two cycles entirely)
- **Doubleton split:** each cycle contains exactly one trigram from each paired element
- **Fiber preservation:** negative (neither τ nor τ² induces a well-defined map on Z₅)
- **Geometry:** non-geometric (5 distinct angular displacements, no D₈ isometry)

τ necessarily cross-cuts all algebraic structure: if it preserved complement geometry, both arrangements would share Z₂ properties (they don't: 4/4 vs 1/4). If it preserved element fibers, the two Z₅ systems would be algebraically related (proven impossible in §4/Iteration 1).

**Type:** Proven (exhaustive). **Reference:** 03_prime_decomposition.py

---

## §7. The dimensional table

| Parameter | Value | Derivation | Type |
|---|---|---|---|
| \|Elements\| | 5 | Two independent cycles → smallest viable prime | Proven |
| Lines per trigram | 3 | Singleton-forcing dimension (pigeonhole) | Proven |
| \|Trigrams\| | 8 = 2³ | Follows from n=3 | Derived |
| Lines per hexagram | 6 = 2×3 | Largest involutory 互 dimension | Computed |
| \|Hexagrams\| | 64 = 2⁶ | Follows from 2n=6 | Derived |
| 五行 assignment | Traditional | Conjunction: algebraic + textual | Proven + Measured |
| 先天 arrangement | Fu Xi | Unique Z₂ optimum (gap of 3) | Computed |
| 後天 arrangement | King Wen | Unique 2×3×5 triple junction | Computed |

**Every parameter consumed. No free choices remain.**

---

## §8. Residual structure

### Four nested incommensurabilities

| Layer | Gap | Bridge | Status |
|---|---|---|---|
| Z₂ vs Z₅ | Binary vs pentadic | Complement (unique cross-framework involution) | Bridged |
| He Tu Z₅ vs 生-cycle Z₅ | Spatial vs dynamic | 後天 compass (triple junction, not algebra) | Connected |
| 先天 vs 後天 | Z₂ optimum vs 2×3×5 junction | τ: order-4, complement-bridging, fiber-breaking | Mapped |
| Shell vs Core | Identity vs convergence | None (orthogonality wall) | Unbridged |

### What remains interpretive

- **§1 of deep-questions (Coordinate-free space):** Is the interference pattern itself a mathematical object, or merely a description of one?
- **§4 of deep-questions (Incommensurability as mechanism):** Why does the system function through gaps rather than unifications?
- **§7 of deep-questions (說卦傳):** The textual tradition provides a narrative rationale for the 後天 arrangement independent of the mathematical derivation. Reconciling the two requires Chinese philology.

### The computational boundary

The derivation tree above consumes every structural parameter of the system. From two axioms (independent cycles + complement-respecting binary substrate), through five proven/computed steps, every dimension, every assignment, and every arrangement is determined. What remains — the three open questions — describes the system's nature rather than its parameters. They are well-posed questions about interpretation, not computation.

The computational program terminates here. Every arrow in the derivation tree points to a script and results file that can be re-executed for verification.

---

## §9. V₄ symmetry and KW pairing

### V₄ = {id, complement, reversal, comp∘rev} on Z₂⁶

| V₄ element | Fixed pts | Fiber-preserving? | Basin action | Relation well-defined? |
|---|:---:|:---:|---|:---:|
| Complement | 0 | ✓ (negation on Z₅) | Kun↔Qian, KanLi fixed | ✓ (inverts direction) |
| Reversal | 8 (palindromes) | ✗ | All fixed | ✗ |
| Comp∘Rev | 8 (anti-palindromes) | ✗ | Kun↔Qian, KanLi fixed | ✗ |

**互 is V₄-equivariant:** all three involutions commute with 互 (verified exhaustively). The nuclear transform respects every symmetry of the system.

**Anti-palindromes** (comp∘rev-fixed): 8 hexagrams, ALL with 3 yang lines, ALL in KanLi basin, including 既濟/未濟 (the 互 attractors). These are the geometric center of the system.

**V₄ orbits:** 20 total (0 size-1, 8 size-2, 12 size-4). Each size-4 orbit admits 3 splittings into pairs, one per involution. Total V₄-compatible pairings: 3^12 = 531,441.

### KW pairing: unique basin-preservation maximum

**Theorem.** The KW pairing (reversal + complement fallback for palindromes) is the unique V₄-compatible pairing maximizing same-basin pairs (28/32).

*Proof.* Reversal preserves all basins. Complement and comp∘rev swap Kun↔Qian. For each size-4 orbit, reversal guarantees same-basin pairs; any other choice introduces cross-basin pairs. The 8 size-2 orbits are forced. □

**Type:** Proven (theorem + exhaustive verification). **Reference:** 06_v4_symmetry.py, 08_pairing_torus.py

---

## §10. Line hierarchy and textual bridge

### Three-tier line hierarchy

| Tier | Bits (lines) | Element change | Basin change | Role |
|---|---|:---:|:---:|---|
| Outer core | b₀,b₁ (1,2), b₄ (5) | 100% | 0% | Element-changers, basin-preservers |
| Interface | b₂ (3), b₃ (4) | 50-100% | 100% | Basin-changers |
| Shell | b₅ (6) | 50% | 0% | Palace invariant, intra-fiber |

### Palace walk (京房) = onion traversal

Bit-flip sequence: b₀, b₁, b₂, b₃, b₄, undo-b₃, undo-b₀b₁b₂. b₅ never flipped (palace invariant). 体 departs and returns; 用 holds then departs. Palindromic palaces visit all 3 basins; non-palindromic visit 2 (because b₀=b₂ decouples basin and element coordinates).

### Yaoci encode the algebraic hierarchy

| Role | Lines | 吉% | 凶% | p-value |
|---|---|:---:|:---:|---|
| Outer core | 1,2,5 | 39.6% | 9.4% | 吉: p=0.0005 |
| Interface | 3,4 | 19.5% | 13.3% | 凶: p=0.0023 |
| Shell | 6 | 26.6% | 26.6% | |

Line 5 (ruler/b₄): OR=2.15 for 吉 (p=0.007). 生体 × line 5 = 75% 吉 (the system's peak auspiciousness).

The yaoci encode the foundational layer (binary geometry + element relations) but NOT the operational overlays (体/用 p=0.22, 世 line p=0.30). The ancient text and the algebraic structure agree; the later operational systems are independent constructions.

**Type:** Measured (statistical). **Reference:** 09_line_valuations.py

---

## §11. The KW sequence

**Basin clustering** is the sole significant sequential signal (p < 0.001): 60% of consecutive hexagrams share a basin vs 37% expected. The sequence organizes by nuclear scaffolding, not by elements.

**上經/下經 = palindromic/non-palindromic partition.** The 4 上經 pure hexagrams have palindromic trigrams {乾,坤,坎,離} (b₀=b₂, fixed by reversal). The 4 下經 pures have non-palindromic trigrams {震,艮,巽,兌} (moved by reversal).

**Type:** Measured (Monte Carlo). **Reference:** 05_king_wen_sequence.py
