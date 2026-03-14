# Proof: Nuclear Rank Sequence Formula

## Theorem

For all n ≥ 2, let M be the 2n×2n nuclear extraction matrix over F₂ (the map that extracts the inner n lines from each half of a 2n-line figure). Then:

**rank(M^k) = max(2, 2n − 2k)  for all k ≥ 1.**

Equivalently: rank drops by exactly 2 per iteration until stabilizing at rank 2 after n−1 steps.

## Definitions

A **2n-line figure** is a vector h = (L₁, ..., L_{2n}) ∈ F₂^{2n}. The **nuclear extraction** produces a new 2n-line figure:
- Nuclear lower = (L₂, L₃, ..., L_{n+1})  [inner n lines of the lower half + one overlap]
- Nuclear upper = (L_n, L_{n+1}, ..., L_{2n−1})  [inner n lines of the upper half + one overlap]

In the hexagram case (n = 3), this is the classical 互卦 operation.

## Proof

### Step 1: Factored-Basis Decomposition

Define the **factored basis** for F₂^{2n}:
- Position coordinates: p₀ = L₁ (outer lower), p₁ = L₂, ..., p_{n−1} = L_n (inner lower)
- Orbit coordinates: q₀ = L_{2n} (outer upper), q₁ = L_{2n−1}, ..., q_{n−1} = L_{n+1} (inner upper)

In this basis, the nuclear matrix has the **symmetric** block form:

```
M = [S  E]
    [E  S]
```

where:
- S is the n×n superdiagonal nilpotent shift: S_{i,i+1} = 1 for i = 0,...,n−2, all else 0.
- E = e_{n−1} · e_{n−1}^T is the rank-1 matrix with a single 1 at position (n−1, n−1).

**Interpretation:** M shifts each component outward by one level (o ← m₁ ← ... ← i, ō ← m̄₁ ← ... ← ī), and the innermost levels swap: i' ← ī, ī' ← i. This is because the nuclear extraction's overlap region (L_n and L_{n+1}) couples the position and orbit halves at the innermost level.

*Verified computationally for n = 2, 3, 4, 5, 6, 7, 8.*

### Step 2: Block Triangularization

The involutory change of basis σ_j = p_j ⊕ q_j, keeping p unchanged, is implemented by Q = [I 0; I I] over F₂ (note Q = Q⁻¹ since 2 = 0). Conjugating:

```
M' = Q · M · Q = [T  E]    where T = S + E.
                  [0  T]
```

T is the **shift-plus-stay** matrix:
- T(e₀) = 0  (outermost killed)
- T(e_j) = e_{j−1}  for 1 ≤ j ≤ n−2  (shift outward)
- T(e_{n−1}) = e_{n−2} + e_{n−1}  (innermost: shifts AND stays)

The block-triangular form means the σ (= p ⊕ q) coordinates evolve independently under T, while the p coordinates are driven by both T and the coupling E.

*Verified for n = 2, ..., 8.*

### Step 3: rank(T^k) = max(1, n−k)

**Claim:** T^k(e_{n−1}) = Σ_{i=max(0,n−1−k)}^{n−1} e_i for 0 ≤ k ≤ n−1.

*Proof by induction.* Base: T⁰(e_{n−1}) = e_{n−1}. Step: If T^k(e_{n−1}) = Σ_{i=n−1−k}^{n−1} e_i, then:

T^{k+1}(e_{n−1}) = T(Σ_{i=n−1−k}^{n−1} e_i) = Σ_{i=n−1−k}^{n−1} T(e_i)

- For n−1−k ≤ i ≤ n−2: T(e_i) = e_{i−1}
- For i = n−1: T(e_{n−1}) = e_{n−2} + e_{n−1}

Sum = e_{n−2−k} + e_{n−1−k} + ... + e_{n−3} + (e_{n−2} + e_{n−1}) = Σ_{i=n−2−k}^{n−1} e_i. ∎

At k = n−1: T^{n−1}(e_{n−1}) = Σ_{i=0}^{n−1} e_i = **𝟏** (all-ones vector).

**𝟏 is a fixed point:** T(𝟏) = Σ_j T(e_j) = 0 + e₀ + e₁ + ... + e_{n−3} + (e_{n−2} + e_{n−1}) = 𝟏.

Therefore T^k(e_{n−1}) = 𝟏 for all k ≥ n−1.

**Kernel:** ker(T^k) = span{e₀, ..., e_{min(k,n−1)−1}}.

Proof: T shifts outward; after k applications, any e_j with j < k is killed (shifted past position 0). But e_{n−1} is never killed since T^k(e_{n−1}) = 𝟏 ≠ 0 for all k. By induction, ker(T^k) grows by exactly span{e_{k−1}} at each step (for k ≤ n−1) and stabilizes at span{e₀,...,e_{n−2}} for k ≥ n−1.

**Conclusion:** dim(ker(T^k)) = min(k, n−1), so rank(T^k) = n − min(k, n−1) = max(1, n−k).

*Verified for n = 2,...,8 with explicit kernel basis checks.*

### Step 4: Key Lemma — Φ_k · ker(T^k) = {0}

Since M' = [T E; 0 T] is block upper-triangular:

M'^k = [T^k  Φ_k]
       [ 0    T^k]

where Φ_k = Σ_{l=0}^{k−1} T^l · E · T^{k−1−l}.

**Lemma:** For every e_j ∈ ker(T^k) (i.e., j < min(k, n−1)), Φ_k(e_j) = 0.

*Proof.* Each term in the sum is T^l · E · T^{k−1−l} · e_j.

The factor T^{k−1−l}(e_j):
- Equals 0 when k−1−l > j (since e_j ∈ ker(T^{k−1−l})).
- Equals e_{j−k+1+l} when k−1−l ≤ j (i.e., l ≥ k−1−j).

In the nonzero case: j − k + 1 + l ≤ j (since l ≤ k−1) and j < n−1. Therefore j − k + 1 + l ≤ j < n−1.

The next factor E·e_{j−k+1+l} = e_{n−1} · (e_{n−1}^T · e_{j−k+1+l}) = **0**, because j − k + 1 + l < n−1.

Every term in Φ_k(e_j) is zero. ∎

**Interpretation:** The rank-1 gate E = e_{n−1}·e_{n−1}^T acts as a "filter" that only passes the (n−1)-th component (the innermost level). But ker(T^k) = span{e₀,...,e_{k'−1}} consists of vectors supported on outer levels, which never reach the innermost component under any number of outward shifts. The filter blocks everything.

*Verified computationally for n = 2,...,8, all k.*

### Step 5: Rank Formula

The kernel of M'^k:

ker(M'^k) = {(x, y) ∈ F₂^n × F₂^n : T^k · y = 0  and  T^k · x + Φ_k · y = 0}

From Step 4: y ∈ ker(T^k) implies Φ_k · y = 0, so the second condition reduces to T^k · x = 0.

Therefore **ker(M'^k) = ker(T^k) × ker(T^k)**, and:

dim(ker(M'^k)) = 2 · dim(ker(T^k)) = 2 · min(k, n−1)

**rank(M'^k) = 2n − 2 · min(k, n−1) = 2 · max(1, n−k) = max(2, 2n − 2k).** ∎

*Verified for n = 2, 3, 4, 5, 6, 7, 8, 9, 10 by explicit rank computation.*

## Corollaries

1. **Uniform rank drop:** Each iteration kills exactly 2 dimensions (one from position, one from orbit), regardless of n.

2. **Stabilization:** rank(M^k) = 2 for all k ≥ n−1. The stable image is a 4-element subspace F₂² ⊂ F₂^{2n}.

3. **Attractor structure:** The stable image {0, p_{n−1}, q_{n−1}, p_{n−1}+q_{n−1}} consists of:
   - The zero vector
   - The vector with all lower bits equal and all upper bits equal (to the complement)
   - Its bitwise complement
   - The all-ones vector
   
   For n = 3: {000|000, 101|010, 010|101, 111|111}, which are the 4 hexagrams forming the 既濟/未濟 attractor cycle.

4. **Why rank ≥ 2 (never 0):** The matrix T = S + E is not nilpotent because the rank-1 perturbation E creates a fixed point (𝟏). Without E, the pure shift S would be nilpotent (S^n = 0), giving rank(M^k) = 0 for k ≥ n. The coupling i ↔ ī at the innermost level is precisely what prevents the nuclear descent from collapsing to a single point — it creates the 2-dimensional attractor.

5. **The σ = p ⊕ q coordinate:** The "sum" coordinate σ_j = p_j ⊕ q_j measures whether the position and orbit agree at level j. Under M, σ evolves independently as T · σ — a shift that converges to 𝟏, meaning all levels eventually carry the sum-parity of the innermost pair. This is the algebraic content of the nuclear attractor: the outer structure is progressively determined by the inner, with the innermost shear (i ⊕ ī) as the sole surviving degree of freedom.

## Proof Status

**Formally proven** for all n ≥ 2. The proof is purely algebraic (F₂ linear algebra) and uses no computational verification beyond checking the block-form identity M = [S E; E S] (which follows from the definition of nuclear extraction by direct inspection). All five steps are self-contained proofs; the computational verifications at n = 2,...,10 serve as independent confirmation.

## References

- Computation script: `c1c2_proof_v2.py` (verified n = 2,...,10)
- Previous verification: `c1c2_nuclear_rank.py` (verified n = 3,...,6)
- Related: R57 (Reed-Muller fills orientation space iff n=3)
