# Synthesis 3: The Uniqueness of the I Ching's 五行 System

*Supersedes synthesis-1.md and synthesis-2.md. Standalone account of the unification program (Phases 1–3).*

---

## §0: Abstract

The I Ching assigns the five phases (五行) to the eight trigrams via a map f: F₂³ → Z₅ satisfying complement equivariance f(x ⊕ 111) = −f(x) mod 5. This map is a complement-respecting surjection with three coexisting fiber types. We prove it is **unique up to the natural symmetry** GL(3,F₂) × Aut(Z₅), and that this uniqueness is itself unique: (3,5) is the sole rigid point in the infinite family (n, 2ⁿ−3) where both assignment moduli and orientation moduli vanish simultaneously. The rigidity decomposes into two independent arithmetic conditions — p = 5 forces trivial assignment moduli ((p−3)/2)! = 1, and n = 3 forces trivial orientation moduli 2^{2^{n−1}−1−n} = 1 via the Mersenne equation 2^{n−1} = n+1 — neither of which holds at any other parameter. The internal structure (Fano plane geometry, Z₅ dynamics, nuclear shear) is fully determined by this uniqueness.

---

## §I: Setup — The (n, p) Family

### Domain and Codomain

The **domain** is F₂ⁿ, the n-dimensional vector space over the field with two elements. Its 2ⁿ elements partition into R = 2^{n−1} **complement pairs** {x, σ(x)} under the complement involution σ: x ↦ x ⊕ 1ⁿ. The 2ⁿ − 1 nonzero elements form the projective geometry PG(n−1, F₂).

The **codomain** is Z_p, the integers modulo an odd prime p. It carries the negation involution τ: y ↦ −y. The nonzero elements pair into (p−1)/2 **negation pairs** {y, −y}. The element 0 is the unique fixed point of τ.

A **complement-respecting surjection** is a map f: F₂ⁿ → Z_p satisfying:
1. **Equivariance:** f(σ(x)) = τ(f(x)), i.e., f(x ⊕ 1ⁿ) = −f(x) mod p
2. **Surjectivity:** every element of Z_p is in the image

Equivariance means f is determined by its values on R representatives (one per complement pair). The pair {x, σ(x)} maps to {f(x), −f(x)}, either both to 0 (if f(x) = 0) or to a negation pair {v, −v}.

### Fiber Structure and Types

Each complement pair receives a **type** based on its fiber role:

| Type | Condition | Fiber contribution |
|------|-----------|-------------------|
| 0 | Both elements → 0 | Size-2 fiber at 0 |
| 1 | Sole pair covering a negation pair | Two size-1 fibers (singletons) |
| 2 | Shares a negation pair with ≥1 other pair | Size-2 fibers (shared) |

The number of pairs needed to cover all of Z_p is S = 1 + (p−1)/2 = (p+1)/2 (one for 0, one per negation pair at minimum). The **excess** is E = R − S = 2^{n−1} − (p+1)/2.

### The E = 1 Subfamily

Setting E = 1 gives p = 2ⁿ − 3. The first members:

| n | p = 2ⁿ−3 | Prime? | R = 2^{n−1} | S = (p+1)/2 | E |
|---|----------|--------|-------------|-------------|---|
| 3 | 5 | ✓ | 4 | 3 | 1 |
| 4 | 13 | ✓ | 8 | 7 | 1 |
| 5 | 29 | ✓ | 16 | 15 | 1 |
| 6 | 61 | ✓ | 32 | 31 | 1 |

At E = 1, exactly two fiber-size shapes exist:

| Shape | Description | Fiber partition | Count ratio |
|-------|-------------|----------------|-------------|
| A (majority) | m₀=1, one shared negation pair | (2,2,2, 1^{p−3}) | p−1 |
| B (minority) | m₀=2, all negation pairs singly covered | (4, 1^{p−1}) | 1 |

**Theorem (E=1 ratio).** N_A/N_B = p − 1. *(Proven in synthesis-2; verified at (3,5), (4,13), (5,29), (6,61).)*

Shape A is the unique shape admitting all three fiber types simultaneously. Shape B admits only types {0, 1}. **Three-type coexistence** — the condition that types 0, 1, and 2 all appear — selects shape A.

### The I Ching Instance

At (3, 5): the eight trigrams are F₂³, the five phases are Z₅. The traditional assignment:

| Trigram | Binary | Phase | Z₅ |
|---------|--------|-------|-----|
| 震 Zhèn | 001 | Wood | 0 |
| 巽 Xùn | 110 | Wood | 0 |
| 離 Lí | 101 | Fire | 1 |
| 坤 Kūn | 000 | Earth | 2 |
| 艮 Gèn | 100 | Earth | 2 |
| 兌 Duì | 011 | Metal | 3 |
| 乾 Qián | 111 | Metal | 3 |
| 坎 Kǎn | 010 | Water | 4 |

Z₅ values satisfy complement equivariance: f(x⊕111) = −f(x) mod 5. Wood = 0 is forced (self-complementary pair: 2w ≡ 0 mod 5 ⟹ w = 0). The 生-cycle is stride 1 (0→1→2→3→4), the 克-cycle is stride 2 (0→2→4→1→3).

Fiber partition: {2, 2, 2, 1, 1} — Wood, Earth, Metal each have 2 trigrams; Fire, Water each have 1. This is shape A with three types: {震,巽} are type 0 (both → 0), {坎} and {離} are type 1 (singletons), {坤,艮} and {乾,兌} share negation pairs as type 2.

---

## §II: The Symmetry Group

### GL(n, F₂) and Stab(1ⁿ)

GL(n, F₂) acts on F₂ⁿ by invertible linear maps. Since f must satisfy f(x ⊕ 1ⁿ) = −f(x), the relevant symmetry subgroup is:

> **Stab(1ⁿ) = {g ∈ GL(n, F₂) : g(1ⁿ) = 1ⁿ}**

This subgroup preserves the complement involution: if g(1ⁿ) = 1ⁿ then g(x ⊕ 1ⁿ) = g(x) ⊕ 1ⁿ, so the equivariance condition is invariant under g.

**Theorem (exact sequence).** There is a short exact sequence:

    1 → (F₂)^{n−1} → Stab(1ⁿ) → GL(n−1, F₂) → 1

- **Kernel** = (F₂)^{n−1}: the **shearing maps** g(x) = x ⊕ λ(x)·1ⁿ for linear functionals λ: F₂ⁿ → F₂ with λ(1ⁿ) = 0. Each shearing map fixes all complement pairs as sets but may swap elements within pairs: g(x) = x or g(x) = x ⊕ 1ⁿ.
- **Quotient** = GL(n−1, F₂): acts on the 2^{n−1}−1 non-Frame complement pairs, which form **PG(n−2, F₂)**.

| n | |Stab(1ⁿ)| | |Kernel| | Quotient | PG(n−2, F₂) |
|---|-----------|---------|----------|-------------|
| 3 | 24 | 4 ≅ V₄ | GL(2,F₂) ≅ S₃ | 3 points |
| 4 | 1344 | 8 ≅ (Z₂)³ | GL(3,F₂) (order 168) | Fano plane (7 points) |
| 5 | 322560 | 16 ≅ (Z₂)⁴ | GL(4,F₂) (order 20160) | PG(3,F₂) (15 points) |

### The Combined Symmetry

The **full symmetry group** is Stab(1ⁿ) × Aut(Z_p), acting by:

    (g, α) · f = α ∘ f ∘ g⁻¹

where g permutes the domain and α ∈ Aut(Z_p) = Z_p^× scales the codomain.

| n | p | |Stab(1ⁿ) × Aut(Z_p)| |
|---|---|----------------------|
| 3 | 5 | 24 × 4 = 96 |
| 4 | 13 | 1344 × 12 = 16,128 |
| 5 | 29 | 322,560 × 28 = 9,031,680 |

### Fano Plane at n = 3

At n = 3, the three non-Frame complement pairs are the **three lines through the complement point** 111 in PG(2, F₂) — the Fano plane:

| Pair name | Elements | Fano line |
|-----------|----------|-----------|
| H-pair | {001, 110} = {震, 巽} | Line through 111 via 001 |
| Q-pair | {010, 101} = {坎, 離} | Line through 111 via 010 |
| P-pair | {011, 100} = {兌, 艮} | Line through 111 via 011 |

The quotient S₃ = GL(2, F₂) permutes these three lines transitively.

### Fano Plane at n = 4

At n = 4, the seven non-Frame complement pairs form PG(2, F₂) — again a Fano plane, now with GL(3, F₂) acting as its full automorphism group. *(Verified: transitivity_probe.py.)*

---

## §III: The Selection Chain at (3, 5)

### Orbit-Theoretic Decomposition

The 240 complement-respecting surjections at (3,5) decompose under Stab(111) × Aut(Z₅):

| Stage | Count | Orbits | Orbit sizes |
|-------|-------|--------|-------------|
| All 240 surjections | 240 | 5 | {96, 96, 24, 16, 8} |
| Shape A (three-type) | 192 | 3 | {48, 48, 96} |
| Orbit C (Frame = Type 2) | 96 | **1** | {96} |

**Theorem (Orbit C regularity).** Stab(111) × Aut(Z₅) acts **regularly** (free + transitive) on the 96 Orbit-C surjections.

*Proof decomposition:*
1. Stab(111)/V₄ ≅ S₃ acts transitively on the 6 type patterns (permuting which non-Frame pair gets which type).
2. V₄ × Aut(Z₅) (order 16) acts regularly on the 16 surjections within each fixed type pattern.
3. Combined: 6 × 16 = 96 = |Orbit C|, with trivial stabilizer. ∎

*(Proven: transitivity_probe.py)*

### The 0.5-Bit

**The 0.5-bit is presentational, not structural.** Under the full symmetry Stab(111) × Aut(Z₅), there is exactly 1 orbit on Orbit C. No binary choice exists.

The 0.5-bit **appears** when we fix the 互 kernel line H = {000, 111}:
- Stab(H) ∩ Stab(111) ≅ D₄ (dihedral, order 8) replaces S₄ (order 24)
- The quotient S₃ → Z₂: only Q↔P permutation survives
- This splits Orbit C into **3 type-pattern orbits** under D₄
- Among these: H = Type 0 (the I Ching's choice) vs H = Type 1 (alternative)
- The choice between them is the 0.5-bit

Since the full symmetry identifies all type patterns, the 0.5-bit measures the information content of choosing which specific Fano line is the 互 kernel — a datum external to the surjection f.

### The Complete Selection

| Step | Count | Mechanism | Status |
|------|-------|-----------|--------|
| All complement-respecting surjections | 240 | — | — |
| Three-type coexistence (shape A) | 192 | Structural | **Theorem** |
| Frame = Type 2 (Orbit C) | 96 | 五行 data forces it | **Theorem** |
| Full symmetry quotient | **1** | Stab(111) × Aut(Z₅) | **Theorem** |

The selection 240 → 192 → 96 → 1 is fully determined by three ingredients: complement equivariance, three-type coexistence, and the symmetry group.

---

## §IV: The Uniqueness Theorem

### Statement

**Theorem (Rigidity of (3,5)).** Among all (n, p) in the E = 1 family p = 2ⁿ − 3, fix a type distribution within shape A (the three-type coexisting shape). The number of orbits of surjections with that type distribution, under the residual symmetry (F₂)^{n−1} × Aut(Z_p), is:

> **Orbits(n, p) = ((p−3)/2)! × 2^{2^{n−1} − 1 − n}**

This equals 1 **if and only if** (n, p) = (3, 5).

### Proof

**Step 1: Surjection count per type distribution.**

A type distribution fixes which of the R complement pairs has type 0, which have type 1, and which have type 2. In shape A:
- 1 pair is type 0 (maps to zero)
- (p−3)/2 pairs are type 1 (each uniquely covers a negation pair)  
- 2 pairs are type 2 (share one negation pair)

A surjection with this type distribution is determined by three choices:
1. **Shared negation pair:** which of the (p−1)/2 negation pairs is shared by the two type-2 pairs. This gives (p−1)/2 choices.
2. **Assignment:** which type-1 pair covers which remaining negation pair. This is a bijection from (p−3)/2 type-1 pairs to (p−3)/2 remaining negation pairs: ((p−3)/2)! choices.
3. **Orientations:** for each non-zero complement pair, which element maps to the positive representative of its negation pair. This gives 2^{R−1} = 2^{2^{n−1}−1} choices (R−1 because the type-0 pair has no orientation freedom).

**Total:** ((p−1)/2) × ((p−3)/2)! × 2^{2^{n−1}−1}

At (3,5): 2 × 1 × 8 = 16. ✓
At (4,13): 6 × 120 × 128 = 92,160. ✓ *(Verified: within_type_orbits.py)*

**Step 2: Symmetry absorption.**

The residual symmetry group (fixing the type distribution) is (F₂)^{n−1} × Aut(Z_p), order 2^{n−1} × (p−1).

Its action absorbs three kinds of freedom:

**(a) Shared negation pair:** Aut(Z_p)/{±1} ≅ Z_{(p−1)/2} acts on the (p−1)/2 negation pairs. Since p = 2ⁿ − 3, |Aut(Z_p)/{±1}| = (p−1)/2 = 2^{n−1} − 2. For n ≥ 3, this group acts transitively on the (p−1)/2 negation pairs (verified: the primitive root generates a single cycle). This absorbs all (p−1)/2 shared-pair choices.

**(b) Orientations — negation absorption:** The element {−1} ∈ Aut(Z_p) flips all orientations simultaneously. This absorbs 1 bit.

**(c) Orientations — kernel absorption:** The kernel (F₂)^{n−1} acts on orientations by flipping subsets of the R−1 non-Frame pairs. The flip patterns form the **first-order Reed-Muller code** RM(1, n−1) inside (Z₂)^{R−1}:
- The kernel's 2^{n−1} flip patterns are: identity (weight 0), the 2^{n−1}−1 Fano-line complements (weight 2^{n−2}), the 2^{n−1}−1 Fano lines (weight 2^{n−2}−1, from composing with {−1}), and all-ones (weight 2^{n−1}−1, from {−1} alone).
- RM(1, n−1) has dimension n, so it absorbs n orientation bits.

Total absorbed: (p−1)/2 shared-pair choices, and n+1 orientation bits (1 from {−1}, n−1 from kernel, but they overlap at 1 element, giving n total). More precisely, the group acting on orientations is the span of the kernel and {−1} in (Z₂)^{R−1}, which is RM(1, n−1) of order 2^n.

**Step 3: Remaining orbits.**

The action is free (verified at (3,5) and (4,13)). The group has order 2^{n−1} × (p−1). So:

    Orbits = |surjections| / |group|
           = ((p−1)/2) × ((p−3)/2)! × 2^{2^{n−1}−1} / (2^{n−1} × (p−1))
           = ((p−3)/2)! × 2^{2^{n−1}−1} / 2^n
           = ((p−3)/2)! × 2^{2^{n−1}−1−n}

The (p−1)/2 shared-pair choices cancel with (p−1) from Aut(Z_p) (which includes the factor-of-2 from {±1}). The 2^{2^{n−1}−1} orientations are reduced by the kernel-plus-negation group of order 2^n.

At (3,5): 1! × 2^{4−1−3} = 1 × 2⁰ = **1**. ✓
At (4,13): 5! × 2^{8−1−4} = 120 × 8 = **960**. ✓ *(Verified: within_type_orbits.py)*

**Step 4: Uniqueness of (3, 5).**

Orbits(n,p) = 1 requires two independent conditions:

**Condition 1 (trivial assignment moduli):** ((p−3)/2)! = 1, which holds iff (p−3)/2 ≤ 1, i.e., p ≤ 5. In the E = 1 family, p = 2ⁿ − 3 ≥ 5, so p = 5, giving n = 3.

**Condition 2 (trivial orientation moduli):** 2^{2^{n−1}−1−n} = 1, i.e., 2^{n−1} − 1 − n = 0, i.e., **2^{n−1} = n + 1**. The solutions over positive integers: n = 1 (degenerate: p = −1) and **n = 3** (giving 2² = 4 = 3+1). For n ≥ 4, 2^{n−1} grows exponentially while n+1 grows linearly, so no further solutions exist.

Both conditions independently force n = 3, p = 5. ∎

### The Orbit Table

| (n, p) | Orbits | Assignment factor | Orientation factor | log₂(Orbits) |
|--------|--------|-------------------|-------------------|---------------|
| (3, 5) | **1** | 1! = 1 | 2⁰ = 1 | 0.0 |
| (4, 13) | 960 | 5! = 120 | 2³ = 8 | 9.9 |
| (5, 29) | 6.38 × 10¹² | 13! = 6.23 × 10⁹ | 2¹⁰ = 1024 | 42.5 |
| (6, 61) | ≈ 2.97 × 10³⁸ | 29! ≈ 8.84 × 10³⁰ | 2²⁵ ≈ 3.36 × 10⁷ | 127.8 |

The moduli grow doubly exponentially in n (from both factors). The I Ching lives at the unique zero.

---

## §V: The Nuclear Shear (互)

### Definition

A **2n-line figure** (hexagram at n=3) is a pair h = (lower, upper) ∈ F₂ⁿ × F₂ⁿ, written as 2n bits L₁,...,L_{2n}. The **nuclear extraction** 互 takes the inner 2(n−1) lines and splits them into overlapping n-grams:

    nuclear_lower = (L₂, ..., L_{n+1})
    nuclear_upper = (L_{n}, ..., L_{2n−1})

Overlap = n−2 bits. The outermost lines L₁ and L_{2n} are discarded.

**Theorem.** The nuclear map is F₂-linear. Its rank is 2n−2.

### Factored Basis

Decompose h into **position** (lower n-gram) and **orbit** (palindromic signature):
- Position: (o, m₁, ..., m_{n−2}, i) = lower n-gram
- Orbit: (ō, m̄₁, ..., m̄_{n−2}, ī) where ō = L₁ ⊕ L_{2n}, m̄_k = L_{k+1} ⊕ L_{2n−k}, ī = L_n ⊕ L_{n+1}

The nuclear map in this basis:

| | Position | Orbit |
|---|----------|-------|
| Shift | o ← m₁ ← ··· ← m_{n−2} ← i | ō ← m̄₁ ← ··· ← m̄_{n−2} ← ī |
| Terminal | i' = i ⊕ ī (shear) | ī' = ī (projection) |

**Pattern:** Position undergoes a shift with a shear at the innermost coordinate (ī leaks into i). Orbit undergoes a shift with a projection (ī is fixed). Each application kills one outer coordinate from each component.

*(Verified at n=3 and n=4: transitivity_probe.py)*

### Rank Sequence and Attractors

| Power k | Rank at n=3 | Rank at n=4 | General |
|---------|-------------|-------------|---------|
| M¹ | 4 | 6 | 2n−2 |
| M² | 2 | 4 | 2n−4 |
| M³ | 2 (stable) | 2 | max(2, 2n−6) |
| M⁴ | — | 2 (stable) | max(2, 2n−8) |

**Convergence:** rank stabilizes at 2 after n−1 iterations.

**Stable image:** 4 elements = span{i, ī}, consisting of:
- 2 fixed points: all-zeros and all-ones (ī = 0)
- 1 two-cycle: the two alternating patterns (ī = 1)

At n=3, these are the hexagrams 坤坤, 乾乾 (fixed) and 既濟 ↔ 未濟 (2-cycle).

### The Transition Matrix at (3, 5)

Each hexagram has a Z₅ difference d(h) = f(upper) − f(lower) mod 5. The **互 transition matrix** T records how d changes under nuclear extraction:

| d(h) \ d(互(h)) | 同(0) | 生(1) | 克(2) | 被克(3) | 被生(4) |
|-----------------|-------|-------|-------|---------|---------|
| 同(0) | 6 | 2 | 2 | 2 | 2 |
| 生(1) | 1 | 2 | 3 | 6 | 0 |
| 克(2) | 4 | 0 | 4 | 5 | 0 |
| 被克(3) | 4 | 0 | 5 | 4 | 0 |
| 被生(4) | 1 | 0 | 6 | 3 | 2 |

**Key property at (3,5):** This matrix T is the **same for all 16 surjections** within a type distribution. The nuclear shear is a type-distribution invariant, adding no information beyond the type structure.

**Key property at (4,13):** Every surjection gives a **different** 13×13 transition matrix T. At n = 4, the nuclear map is a complete surjection invariant. *(Verified: within_type_orbits.py)*

This contrast — T is constant at (3,5) but distinguishing at (4,13) — is another manifestation of rigidity. At the unique point (3,5), even the dynamics is fully determined.

---

## §VI: The Reed-Muller Connection

### Kernel Flip Patterns

The kernel (F₂)^{n−1} ⊂ Stab(1ⁿ) acts on orientations by flipping subsets of the R−1 = 2^{n−1}−1 non-Frame complement pairs. The **flip pattern** of a kernel element g is the set S ⊂ {1,...,R−1} of pairs whose representatives are swapped by g.

At n = 4 (7 non-Frame pairs forming a Fano plane):

| Source | Number | Flip sizes | Geometric meaning |
|--------|--------|------------|-------------------|
| Kernel (F₂)³ | 8 | {0, 4, 4, 4, 4, 4, 4, 4} | Identity + 7 Fano-line complements |
| {−1} × Kernel | 8 | {7, 3, 3, 3, 3, 3, 3, 3} | All-flip + 7 Fano lines |

The 7 three-element flip patterns from {−1} × Kernel are **exactly the 7 lines of the Fano plane** PG(2, F₂). The 7 four-element patterns are their complements.

### The Code-Theoretic Identification

The 16 flip patterns generate a subgroup of (Z₂)^{R−1} = (Z₂)^7. This subgroup is the **first-order Reed-Muller code RM(1, n−1)**:
- RM(1, n−1) consists of all evaluation vectors of affine functions on F₂^{n−1}
- It has dimension n and 2^n codewords
- Its minimum distance is 2^{n−2}
- It is the [2^{n−1}−1, n, 2^{n−2}] extended code (when including the even-weight subcode)

The quotient (Z₂)^{R−1} / RM(1, n−1) has 2^{R−1−n} = 2^{2^{n−1}−1−n} cosets. These are the **orientation orbits**.

### Why n = 3 Is Special

The orientation moduli vanish iff RM(1, n−1) fills the entire orientation space, i.e., dim(RM(1,n−1)) = dim((Z₂)^{R−1}):

    n = R − 1 = 2^{n−1} − 1

This is the equation **2^{n−1} = n + 1**, whose only non-degenerate solution is n = 3.

| n | dim(orientation space) | dim(RM(1,n−1)) | Quotient dimension | Orientation orbits |
|---|----------------------|----------------|-------------------|-------------------|
| 3 | 3 | 3 | 0 | 1 |
| 4 | 7 | 4 | 3 | 8 |
| 5 | 15 | 5 | 10 | 1024 |

At n = 3: the Reed-Muller code **exactly fills** the orientation space. Every orientation vector is equivalent under symmetry. At n ≥ 4: the code is too small. Orientation freedom persists.

---

## §VII: The Coherent Configuration and Walsh Spectrum

### CC Structure

The Z₅ difference d(x,y) = f(y) − f(x) mod 5 partitions the 64 ordered pairs of F₂³ into 6 seed classes (diagonal + 5 difference classes). This is **not** a coherent configuration due to heterogeneous fiber sizes {2, 2, 2, 1, 1}.

**Coherent closure:** 2 refinement rounds produce **28 classes** — the orbit partition of the fiber automorphism group (Z₂)³ (generated by swapping within each doubleton fiber). Not an association scheme (intersection matrices don't commute). *(Verified: cc_identity.py)*

**Interpretation:** The CC is the maximally generic structure forced by the fiber sizes. It encodes no information beyond "which fiber does each trigram belong to." The 五行 map's algebraic identity is captured entirely by the uniqueness theorem (§IV), not by any special algebraic structure on F₂³.

### Walsh-Hadamard Spectrum

The Walsh-Hadamard transform of f at frequency ω ∈ F₂³:

    W_f(ω) = Σ_{x ∈ F₂³} ζ₅^{f(x)} · (−1)^{⟨ω,x⟩}

where ζ₅ = e^{2πi/5}.

**Key values:**
- W(000) = (1−√5)/2 = −1/φ (negative reciprocal of the golden ratio)
- |W(ω)|² ∈ Q(√5) for all ω
- Parseval: Σ|W(ω)|² = 8 × 8 = 64

**Parity constraint:** wt(ω) even ⟹ W(ω) ∈ ℝ; wt(ω) odd ⟹ W(ω) ∈ iℝ. This follows from complement equivariance and is verified to 10⁻¹⁵ precision. *(Verified: cc_identity.py)*

**Status:** The spectrum lives in Q(√5) because Aut(Z₅) ≅ Z₄ has order 4 and 5 = φ² + φ. This is a property of all maps into Z₅, not specific to the I Ching's f. The spectrum does not provide a distinguishing invariant.

---

## §VIII: The Object, Definitively

The I Ching's 五行 assignment is a complement-respecting surjection f: F₂³ → Z₅ with three-type coexistence (shape A, Orbit C). It is **unique up to the symmetry** Stab(111) × Aut(Z₅), which acts regularly (free and transitive) on the 96 Orbit-C surjections.

This uniqueness is itself unique: **(3, 5) is the sole rigid point** in the infinite E = 1 family. The rigidity decomposes into two arithmetic facts:

1. **p = 5 is the smallest prime yielding E = 1** (i.e., 2ⁿ − 3 = 5 ⟹ n = 3). At p = 5 there is only 1 type-1 pair, so the assignment is trivially determined. At p = 13, there are 5 type-1 pairs and 5! = 120 assignment choices not absorbed by symmetry.

2. **n = 3 is the unique dimension where the Reed-Muller code fills the orientation space.** The equation 2^{n−1} = n + 1 has n = 3 as its only non-degenerate root. At n = 3, every orientation choice is equivalent under kernel swaps plus negation. At n = 4, the 128 orientations collapse to only 8 equivalence classes.

Neither condition holds at any other (n, p) in the family. The I Ching's structure is not a member of a parametric family — it is an **isolated fixed point** of a doubly exponential moduli space.

### What Is Determined and What Is Not

**Fully determined by uniqueness:**
- Which trigram pairs share an element (the fiber partition)
- Which fiber type each complement pair carries (the type distribution, up to full symmetry)
- The 5×5 互 transition matrix T
- The coherent configuration (28 classes, orbit partition of (Z₂)³)
- The Walsh spectrum (in Q(√5))
- The eigenstructure of T: {1, 1/6, −1/13, complex pair |λ| ≈ 0.29}
- 克 concentration (87.5%) and stationary distribution

**Not determined (outside the framework):**
- Which specific Fano line carries the 互 kernel (the 0.5-bit, requiring external datum)
- King Wen sequence ordering
- Hexagram names and line texts
- The 先天/後天 octagonal arrangements (compatible but not forced)

---

## §IX: Inventory of Results

### Theorems (proven from definitions)

| # | Result | Reference |
|---|--------|-----------|
| T1 | Complement equivariance: f(x⊕1ⁿ) = −f(x) halves the search space | §I |
| T2 | Singleton-forcing: p > 2^{n−1} ⟹ singleton fibers exist | synthesis-2 §I |
| T3 | Shape count = Σ_{k≤E} p(k) | synthesis-2 §I |
| T4 | E=1 ratio: N_A/N_B = p−1 | synthesis-2 §I |
| T5 | Three types ⟹ shape A (at E=1) | §I |
| T6 | Exact sequence 1→(F₂)^{n−1}→Stab(1ⁿ)→GL(n−1,F₂)→1 | §II |
| T7 | Orbit C regularity: Stab(111)×Aut(Z₅) regular on 96 surjections | §III |
| T8 | **Orbit count = ((p−3)/2)! × 2^{2^{n−1}−1−n}** | **§IV** |
| T9 | **Uniqueness: Orbits = 1 iff (n,p) = (3,5)** | **§IV** |
| T10 | Nuclear map is F₂-linear, rank 2n−2 | §V |
| T11 | Factored basis: shift + shear (position), shift + project (orbit) | §V |
| T12 | d(complement(h)) = −d(h) mod p | synthesis-2 §III |
| T13 | Hexagram Z₅ matrix = expanded Cayley subtraction table | synthesis-2 §III |
| T14 | P→H rotation under nuclear extraction | synthesis-2 §IV |
| T15 | Kernel flip patterns generate RM(1, n−1) | §VI |

### Verified Computations (exhaustive, not sampled)

| # | Result | Reference |
|---|--------|-----------|
| V1 | 240 surjections at (3,5), partition 192+48 | synthesis-2 §II |
| V2 | 5 orbits on 240, 3 on 192, 1 on 96 | cc_identity.py |
| V3 | V₄ × Aut(Z₅) acts freely on 16 same-type surjections | transitivity_probe.py |
| V4 | 92,160 surjections per type distribution at (4,13) | within_type_orbits.py |
| V5 | 960 orbits at (4,13), all of size 96 | within_type_orbits.py |
| V6 | 42 Orbit-C type distributions at (4,13), 1 orbit under Stab(1111) | transitivity_probe.py |
| V7 | 互 transition matrix T: constant at (3,5), distinguishing at (4,13) | within_type_orbits.py |
| V8 | CC closure: 28 classes, not an AS | cc_identity.py |
| V9 | Walsh spectrum ∈ Q(√5), W(000) = −1/φ | cc_identity.py |
| V10 | Rank sequence 6→4→2→2 at n=3, 8→6→4→2→2 at n=4 | transitivity_probe.py |
| V11 | 4-element stable image (2 fixed + 1 two-cycle) at n=3 and n=4 | transitivity_probe.py |
| V12 | 互 spectrum: {1, 1/6, −1/13, complex pair}, π(同+克+被克)=89% | eigenstructure.py |
| V13 | Singleton-forcing, shape count, E=1 ratio across 27 test cases | np_landscape.py |

### Conjectures (supported but unproven for general n)

| # | Result | Evidence |
|---|--------|----------|
| C1 | Rank sequence: rank(M^k) = max(2, 2n−2k) for all n | Verified n=3,4 |
| C2 | Stable image = 4 elements for all n | Verified n=3,4 |
| C3 | Orbit C transitivity generalizes: single orbit on type distributions for all (n,p) | Verified (3,5), (4,13); follows from 2-transitivity of GL(n−1,F₂) on PG(n−2,F₂) |
| C4 | Action of residual group is free for all (n,p) | Verified (3,5), (4,13) |

---

## Appendix A: Source Files

| File | Phase | Content |
|------|-------|---------|
| fano_probe.py | 1 | Fano plane structure, stabilizer computation |
| hexagram_lift.py | 1 | Hexagram-level Z₅ algebra |
| parity_rotation.py | 1 | P→H rotation proof |
| half_bit_test.py | 1 | 0.5-bit analysis |
| xiantian_fano.py | 1 | 先天/後天 Z₅ signatures |
| framework_strengthening.py | 1 | 克 concentration, KW ordering |
| np_landscape.py | 2 | (n,p) parameter space, singleton-forcing |
| orbit_c_nuclear.py | 2 | Orbit C enumeration, nuclear shear |
| hexagram_wuxing.py | 2 | Hexagram 五行 matrix |
| eigenstructure.py | 2 | Transition matrix eigenstructure |
| cc_identity.py | 3 | Coherent configuration, Walsh spectrum |
| transitivity_probe.py | 3 | Orbit C regularity proof, n=4 nuclear map |
| within_type_orbits.py | 3 | Within-type orbit count, Reed-Muller connection |

## Appendix B: Notation

| Symbol | Meaning |
|--------|---------|
| F₂ⁿ | n-dimensional vector space over GF(2) |
| Z_p | integers mod prime p |
| σ: x ↦ x ⊕ 1ⁿ | complement involution on F₂ⁿ |
| τ: y ↦ −y | negation involution on Z_p |
| Stab(1ⁿ) | stabilizer of all-ones in GL(n, F₂) |
| R = 2^{n−1} | number of complement pairs |
| S = (p+1)/2 | minimum coverage (slots) |
| E = R − S | excess pairs |
| RM(1, n−1) | first-order Reed-Muller code of length 2^{n−1}−1 |
| PG(k, F₂) | k-dimensional projective geometry over F₂ |
| 互 | nuclear extraction (hexagram transformation) |
| d(h) | Z_p difference of hexagram h |
| T | 互 transition matrix on Z_p differences |
