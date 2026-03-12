# Transitivity Probe Results

## Summary

Three investigations at (3,5) and beyond.

**Task A** decomposes the 1-orbit result on Orbit C into a structural proof: Stab(111) ≅ S₄ acts through its S₃ quotient on non-Frame complement pairs, with V₄ kernel acting by within-pair swaps. The combined action of Stab(111) × Aut(Z₅) on the 96 Orbit-C surjections is **free and regular** (= simply transitive). This is proven, not merely verified.

**Task B** shows that at (4,13), the same pattern holds at the type-distribution level. The 7 non-Frame complement pairs form a **Fano plane** PG(2,F₂), and Stab(1111) acts through its GL(3,F₂) quotient on this Fano plane. The 42 "Orbit C analog" type distributions form a **single orbit** — transitivity generalizes. The 4 total orbits on 168 type distributions have a clean Fano-geometric classification.

**Task C** defines the nuclear map at n=4 and shows its factored-basis formula is a direct generalization of n=3: one additional shift step, same shear/projection structure. The rank sequence drops by 2 per step, stabilizing at rank 2 after n−1 steps: a clean pattern that conjecturally holds for all n.

---

## Task A: Transitivity Proof at (3,5)

### Step 1: Stab(111) on Complement Pairs

Stab(111) ≅ S₄ has 24 elements. All of them fix the Frame pair {0,7} (since g(0)=0 for linear maps and g(7)=7 by definition). The induced action on the **3 non-Frame complement pairs** {H, Q, P} yields only **6 distinct permutations** — exactly S₃.

| Property | Value |
|----------|-------|
| |Stab(111)| | 24 |
| Pair permutations induced | 6 = |S₃| |
| Kernel V₄ = {g : fixes all pairs as sets} | 4 elements |
| Is quotient all of S₃? | **Yes** |
| Is the map Stab(111) → S₃ faithful? | **No** (kernel = V₄) |

**The kernel V₄ (Klein four-group):** Each non-identity element of V₄ swaps exactly 2 of the 3 non-Frame complement pairs internally (element-by-element within each pair). The constraint g(7) = 7 forces an **even** number of pairs to be swapped (since 7 = 1⊕2⊕4, and swapping within a pair flips the contribution to the XOR).

| V₄ element | Action | Pairs swapped |
|------------|--------|---------------|
| identity | (0,1,2,3,4,5,6,7) | — |
| τ_{HQ} | (0,6,5,3,4,2,1,7) | H: 1↔6, Q: 2↔5 |
| τ_{HP} | (0,6,2,4,3,5,1,7) | H: 1↔6, P: 3↔4 |
| τ_{QP} | (0,1,5,4,3,2,6,7) | Q: 2↔5, P: 3↔4 |

**Algebraic explanation:** The short exact sequence is:

    1 → V₄ → Stab(111) → S₃ → 1

where V₄ ≅ Hom(F₂³/⟨111⟩, ⟨111⟩) ≅ (F₂)² (shearing maps that fix the complement and act trivially on the quotient). This is a general construction: for any v ∈ F₂ⁿ, Stab(v) → GL(F₂ⁿ/⟨v⟩) ≅ GL(n−1, F₂) is surjective with kernel Hom(F₂^{n−1}, F₂) ≅ (F₂)^{n−1}.

### Step 2: S₃ Transitivity on Type Patterns

The 6 type patterns (H-type, Q-type, P-type) = all permutations of {0,1,2}. Since S₃ acts as the full symmetric group on {H,Q,P}, it permutes these 6 patterns transitively:

**VERIFIED:** S₃ acts transitively on 6 type patterns. (This is immediate since S₃ is the full symmetric group on 3 objects.)

### Step 3: V₄ × Aut(Z₅) Regular on 16 Surjections

Fix the IC type pattern (Fr=2, H=0, Q=1, P=2). There are exactly 16 surjections with this pattern.

**VERIFIED:** V₄ × Aut(Z₅) (order 4 × 4 = 16) acts:
- **Freely**: No non-identity (g, α) fixes any surjection.
- **Transitively**: The orbit of any surjection is all 16.
- Therefore **regularly** (= simply transitively).

**Why it's free:** V₄ permutes trigrams within pairs, changing which specific trigram maps to which element. Aut(Z₅) scales all Z₅ values. Neither alone can be undone by the other, so no non-trivial stabilizer exists.

### Step 4: Theorem

> **Theorem (Orbit C Regularity at (3,5)).**
> *The group Stab(111) × Aut(Z₅) acts freely and transitively (= regularly) on the 96 Orbit-C complement-respecting surjections f: F₂³ → Z₅.*
>
> **Proof.** Factor the action as:
> 1. **S₃ on type patterns:** The quotient Stab(111)/V₄ ≅ S₃ permutes the 3 non-Frame complement pairs. This acts transitively on the 6 type patterns (H-type, Q-type, P-type) ∈ Perm({0,1,2}), since S₃ is the full permutation group.
> 2. **V₄ × Aut(Z₅) within a pattern:** Fix a type pattern. The kernel V₄ and Aut(Z₅) together form a group of order 16 that acts regularly on the 16 surjections sharing that pattern (verified computationally: free + transitive + |group| = |set|).
> 3. **Combining:** |S₃| × |V₄ × Aut(Z₅)| = 6 × 16 = 96 = |Orbit C|. The stabilizer of any element is trivial (V₄ × Aut(Z₅) contributes no stabilizer within a pattern, and S₃ acts faithfully on patterns). ∎

**Corollary:** The 0.5-bit = the choice of orbit when the H-line is fixed. Since Stab(111) → S₃ acts transitively on non-Frame pairs, fixing H (the 互 kernel) reduces S₃ to the point stabilizer S₂ ≅ Z₂ (the Q↔P swap), giving 6/2 = 3 type-pattern orbits. The 0.5-bit distinguishes H=Type0 (IC traditional) from H=Type1 (alternative).

---

## Task B: Type Structure at (4,13)

### Step 1: Partition Shapes

At (n,p) = (4,13): R = 8 complement pairs, S = 7 slots (1 zero-slot + 6 negation pairs), excess E = 1.

| Shape | m₀ | c_vals | Fiber partition | Count | Fraction |
|-------|-----|--------|----------------|-------|----------|
| A (majority) | 1 | (1,1,1,1,1,2) | (2,2,2, 1×10) | 15,482,880 | 92.3% |
| B (minority) | 2 | (1,1,1,1,1,1) | (4, 1×12) | 1,290,240 | 7.7% |

**Ratio N_A/N_B = 12 = p−1.** (Proven in synthesis-2; verified here.)

### Step 2: Type Counts (Majority Shape)

| Type | Description | Count |
|------|-------------|-------|
| 0 | Zero pair (both → 0) | 1 |
| 1 | Singleton coverage (uniquely covers a negation pair) | 5 |
| 2 | Shared coverage (2 pairs share a negation pair) | 2 |
| **Total** | | **8** |

All three types present → **three-type surjection** ✓

Type distributions: C(8,1) × C(7,2) = **168**.

### Step 3: Stab(1111) and the Fano Plane

| Group/Space | Order/Size |
|-------------|-----------|
| GL(4,F₂) | 20,160 |
| Stab(1111) | 1,344 |
| Kernel (fixes all pairs) | 8 ≅ (Z₂)³ |
| Quotient (on 7 non-Frame pairs) | 168 = |GL(3,F₂)| |

**Key structural fact:** The 7 non-Frame complement pairs are the 7 points of PG(2,F₂) — a **Fano plane**. Stab(1111) acts on this Fano plane through its quotient GL(3,F₂), which is the full automorphism group of PG(2,F₂).

This follows from the general principle: for v ∈ F₂ⁿ nonzero, the map Stab(v) → GL(F₂ⁿ/⟨v⟩) is surjective with elementary abelian kernel (F₂)^{n−1}.

| n | Non-Frame pairs | Structure | Quotient action |
|---|----------------|-----------|-----------------|
| 3 | 3 | PG(1,F₂) = 3 points | GL(2,F₂) ≅ S₃ |
| 4 | 7 | PG(2,F₂) = Fano plane | GL(3,F₂) (order 168) |
| k | 2^{k−1}−1 | PG(k−2,F₂) | GL(k−1,F₂) |

### Step 4: Orbits on Type Distributions

GL(3,F₂) acts on PG(2,F₂) and is **2-transitive** (any ordered pair of distinct points can be mapped to any other). This determines the orbit structure:

| Orbit | Size | Frame type | Fano structure | Why this orbit size |
|-------|------|-----------|----------------|---------------------|
| 0 | 21 | Type 0 | unordered pair of points (Type 2) | C(7,2) = 21; 2-transitivity → 1 orbit |
| 1 | **42** | **Type 2** | **ordered pair (Type 0, Type 2)** | **7×6 = 42; 2-transitivity → 1 orbit** |
| 2 | 21 | Type 1 | collinear triple (on a Fano line) | 7 lines × 3 labelings = 21 |
| 3 | 84 | Type 1 | non-collinear triple | 7×12 = 84 (complement of collinear) |

**Total:** 21 + 42 + 21 + 84 = **168** ✓

**The Orbit C analog (Frame = Type 2) forms a single orbit of size 42.**
This confirms that the transitivity property **generalizes** from (3,5) to (4,13).

The orbit classification is entirely determined by:
1. The Frame pair's type (0, 1, or 2)
2. For Frame = Type 1: whether the triple {Type 0, Type 2, Type 2} is collinear in the Fano plane

### Comparison: (3,5) vs (4,13)

| Property | (3,5) | (4,13) |
|----------|-------|--------|
| Non-Frame pairs | 3 (PG(1,F₂)) | 7 (PG(2,F₂)) |
| Quotient group | S₃ = GL(2,F₂) | GL(3,F₂) |
| Type dist count | 18 | 168 |
| Orbits (all types) | 3 | 4 |
| Orbit C analog size | 6 | 42 |
| Orbit C orbits | 1 | **1** |
| 2-transitivity | trivial (S₃ on 3 pts) | GL(3,F₂) on Fano plane |
| Extra orbit source | — | Fano collinearity (2 Frame=Type1 orbits) |

---

## Task C: 互-Analog at n=4

### Definition

For an 8-line figure h = (L₁,...,L₈), the **nuclear extraction** with overlap 2:
- Nuclear lower = (L₂, L₃, L₄, L₅)
- Nuclear upper = (L₄, L₅, L₆, L₇)
- Drops outermost lines L₁ and L₈
- Overlap = {L₄, L₅} (2 bits)

This preserves the n=3 pattern: from 2n lines, take inner 2(n−1), split into lower-n and upper-n with (n−2)-bit overlap.

### Linearity and Matrix

The nuclear map is **linear** over F₂. Its 8×8 matrix M in the standard basis:

```
       L₁ L₂ L₃ L₄ L₅ L₆ L₇ L₈
L'₁:   0  1  0  0  0  0  0  0
L'₂:   0  0  1  0  0  0  0  0
L'₃:   0  0  0  1  0  0  0  0
L'₄:   0  0  0  0  1  0  0  0
L'₅:   0  0  0  1  0  0  0  0
L'₆:   0  0  0  0  1  0  0  0
L'₇:   0  0  0  0  0  1  0  0
L'₈:   0  0  0  0  0  0  1  0
```

This is **not** a permutation matrix: rows 3,5 and rows 4,6 are identical pairs (the overlap creates duplication). Rank = 6 (loses 2 dimensions, corresponding to L₁ and L₈).

### Factored Basis Formula

Using the factored basis (position, orbit):
- Position: (o, m₁, m₂, i) = (L₁, L₂, L₃, L₄)
- Orbit: (ō, m̄₁, m̄₂, ī) = (L₁⊕L₈, L₂⊕L₇, L₃⊕L₆, L₄⊕L₅)

The nuclear map becomes:

| | o' | m₁' | m₂' | i' |
|---|---|---|---|---|
| **Position** | m₁ | m₂ | i | i⊕ī |
| **Orbit** | m̄₁ | m̄₂ | ī | ī |

**Comparison with n=3:**

| | n=3 Position | n=3 Orbit | n=4 Position | n=4 Orbit |
|---|---|---|---|---|
| Coord 1 | o' = m | ō' = m̄ | o' = m₁ | ō' = m̄₁ |
| Coord 2 | m' = i | m̄' = ī | m₁' = m₂ | m̄₁' = m̄₂ |
| Coord 3 | i' = i⊕ī | ī' = ī | m₂' = i | m̄₂' = ī |
| Coord 4 | — | — | i' = i⊕ī | ī' = ī |

**Pattern:** Identical structure with one additional shift step. At general n:
- **Position:** shift chain o → m₁ → m₂ → ... → i, with shear i ↦ i⊕ī at the end
- **Orbit:** shift chain ō → m̄₁ → m̄₂ → ... → ī, with projection ī ↦ ī at the end

**Numerically verified** on all 256 8-line figures.

### Rank Sequence

| Power k | n=3 rank (dim 6) | n=4 rank (dim 8) |
|---------|------------------|------------------|
| M¹ | 4 | 6 |
| M² | 2 | 4 |
| M³ | 2 (stable) | 2 |
| M⁴ | — | 2 (stable) |

**Pattern (proven for n=3,4; conjectured for general n):**

> For the nuclear map 互_n on F₂^{2n}, the rank of M^k is max(2, 2n − 2k).
> Equivalently: rank drops by 2 per step, stabilizing at **rank 2 after n−1 steps**.

**Why:** Each application kills one "outer" coordinate from each of position and orbit, removing 2 dimensions. After n−1 steps, only (i, ī) remain — the innermost position bit and the innermost palindromic bit.

### Attractor Structure

| Property | n=3 | n=4 |
|----------|-----|-----|
| Fixed points | 2: {000000, 111111} | 2: {00000000, 11111111} |
| 2-cycles | 1: {010101 ↔ 101010} | 1: {01010101 ↔ 10101010} |
| Stable image size | 4 | 4 |
| Stable image rank | 2 | 2 |

**Stable image** = span{all-ones, alternating} = {all-0, alternating-A, alternating-B, all-1}.

In factored coordinates: the stable image is parameterized by (i, ī) ∈ F₂²:
- Position = (0,...,0, i, i⊕ī) — all outer coordinates zero, innermost has shear
- Orbit = (0,...,0, ī, ī) — all outer coordinates zero, innermost duplicated

The two fixed points are (i=0,ī=0) → all-zeros and (i=1,ī=0) → all-ones.
The 2-cycle consists of (i=0,ī=1) and (i=1,ī=1), which are the two alternating patterns.

**Conjecture (stable image at general n):**
> The stable image of 互_n on F₂^{2n} has 4 elements: {0, all-ones, alternating-A, alternating-B}, forming a 2-dimensional affine subspace. The attractor consists of 2 fixed points and 1 two-cycle.

---

## Cross-Cutting Results

### 1. The General Structure Theorem

For (n, p) with p prime, p > 2^{n-1}, complement-respecting surjections exist and have a clean orbit theory:

**At the trigram level (n):**
- Complement pairs form 2^{n-1} pairs
- Frame pair {0, all-ones} is always fixed by Stab(all-ones)
- Non-Frame pairs ↔ points of PG(n−2, F₂)
- Stab(all-ones)/kernel ≅ GL(n−1, F₂) acts on PG(n−2, F₂)
- Kernel ≅ (F₂)^{n−1} (within-pair swaps with parity constraint)

**At the hexagram level (2n):**
- 互_n is an F₂-linear map of rank 2n−2
- Factored basis: shift + shear (position) and shift + project (orbit)
- Converges to rank-2 image in n−1 steps
- Stable image: 4 elements (2 fixed + 1 two-cycle)

### 2. Why Frame Is Special

Frame = {0, all-ones} is the unique complement pair where g(0) = 0 (linear) and g(all-ones) = all-ones (by Stab definition). No other complement pair is universally fixed. This is why the "Frame type" is the primary orbit discriminant.

### 3. From n=3 to n=4: What Changes

| Feature | n=3 | n=4 |
|---------|-----|-----|
| Non-Frame geometry | 3 points (trivial) | 7-point Fano plane |
| New orbit source | — | Collinearity (Fano lines) |
| Orbit C analog: 1 orbit? | Yes (proven) | Yes (computed) |
| 互 convergence time | 2 steps | 3 steps |
| Kernel structure | V₄ = (F₂)² | (F₂)³ |

The transition from n=3 to n=4 introduces genuine geometry: the Fano plane structure on non-Frame pairs creates new orbit distinctions (collinear vs non-collinear triples). But the Orbit C transitivity **persists** because GL(3,F₂) is 2-transitive on PG(2,F₂).

### 4. Conjectured Generalization

> **Conjecture.** For all (n, p) with p prime, p > 2^{n-1}, the "Orbit C" type distributions (Frame = Type 2) form a **single orbit** under Stab(all-ones).
>
> **Evidence:** Verified at (3,5) (6 distributions, 1 orbit) and (4,13) (42 distributions, 1 orbit).
>
> **Mechanism:** 2-transitivity of GL(n−1, F₂) on PG(n−2, F₂), which holds for all n ≥ 3.

The 2-transitivity ensures that any ordered pair of distinct non-Frame pairs can be mapped to any other, and an Orbit C type distribution is essentially a labeled ordered pair (Type 0 pair, Type 2 partner pair).

---

## Status

| Claim | Status |
|-------|--------|
| Orbit C transitivity at (3,5) | **Proven** (Theorem, with decomposition) |
| Orbit C action is regular at (3,5) | **Proven** (stabilizer = trivial) |
| V₄ kernel structure | **Proven** (parity constraint on pair swaps) |
| Partition shapes at (4,13) | **Computed** (2 shapes, ratio 12) |
| Fano-geometric orbit classification | **Computed** (4 orbits, sizes 21+42+21+84) |
| Orbit C transitivity at (4,13) | **Computed** (1 orbit of size 42) |
| 互_n factored formula generalization | **Proven** for n=3,4; pattern clear |
| Rank sequence 2n→2(n-1)→...→2 | **Verified** for n=3,4; **conjectured** for general n |
| Stable image = 4 elements | **Verified** for n=3,4; **conjectured** for general n |
| Orbit C transitivity for all (n,p) | **Conjectured** (from 2-transitivity argument) |

### Files

- `transitivity_probe.py` — computation script (Tasks A, B, C)
- `transitivity_probe_output.txt` — full computation output
- `transitivity_probe_results.md` — this document
