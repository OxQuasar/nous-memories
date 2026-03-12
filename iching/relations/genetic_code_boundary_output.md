# Genetic Code Boundary Test

Testing whether the standard genetic code (64 codons → 21 targets)
satisfies any equivariance condition f(σ(x)) = τ(f(x)).

## Step 1: Fiber Sizes of the Genetic Code

| Amino Acid | Codons | Count |
|------------|--------|-------|
| L | CUA, CUC, CUG... | 6 |
| S | AGC, AGU, UCA... | 6 |
| R | AGA, AGG, CGA... | 6 |
| P | CCA, CCC, CCG... | 4 |
| T | ACA, ACC, ACG... | 4 |
| V | GUA, GUC, GUG... | 4 |
| A | GCA, GCC, GCG... | 4 |
| G | GGA, GGC, GGG... | 4 |
| * | UAA, UAG, UGA | 3 |
| I | AUA, AUC, AUU | 3 |
| F | UUC, UUU | 2 |
| Y | UAC, UAU | 2 |
| C | UGC, UGU | 2 |
| H | CAC, CAU | 2 |
| Q | CAA, CAG | 2 |
| N | AAC, AAU | 2 |
| K | AAA, AAG | 2 |
| D | GAC, GAU | 2 |
| E | GAA, GAG | 2 |
| W | UGG | 1 |
| M | AUG | 1 |

Fiber size distribution: [6, 6, 6, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1]
Sum: 64 (should be 64)
Number of distinct targets: 21 (20 AAs + Stop)
Max fiber: 6 (Leu, Ser, Arg)
Min fiber: 1 (Met, Trp)
Fiber shape: (6, 6, 6, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1)

### Comparison with E=1 surjection shapes

| System | Domain | Target | Fiber shape | Max/Min ratio |
|--------|--------|--------|-------------|--------------|
| I Ching | F₂³ (8) | Z₅ (5) | (2,2,2,1,1) | 2 |
| Genetic | F₄³ (64) | 21 targets | (6, 6, 6, 4, 4)... | 6/1 = 6 |

The genetic code has much more heterogeneous fibers (6:1 ratio vs 2:1).
This is a structural difference, not just a scaling difference.

## Step 2: F₄ Involutions

Number of involutions on F₄: 10

  σ = (0, 1, 2, 3): identity
  σ = (0, 1, 3, 2): A↔G, [Frobenius: x↦x²], [field automorphism]
  σ = (0, 2, 1, 3): C↔A, [additive only]
  σ = (0, 3, 2, 1): C↔G, [additive only]
  σ = (1, 0, 2, 3): U↔C
  σ = (1, 0, 3, 2): U↔C, A↔G
  σ = (2, 1, 0, 3): U↔A
  σ = (2, 3, 0, 1): U↔A, C↔G, [Watson-Crick complement]
  σ = (3, 1, 2, 0): U↔G
  σ = (3, 2, 1, 0): U↔G, C↔A

## Step 3: Equivariance Tests

Testing componentwise domain involutions σ(x₁,x₂,x₃) = (σ₁(x₁), σ₂(x₂), σ₃(x₃))
with target involution τ = identity (f(σ(x)) = f(x) — symmetry of the code)

### Key named involutions (τ = identity)

| Domain involution | Violations (of 64) | Description |
|-------------------|-------------------|-------------|
| Frobenius pos 3 only | 4/64 = 6.2% | σ=((0, 1, 2, 3),(0, 1, 2, 3),(0, 1, 3, 2)) |
| Frobenius pos 2 only | 30/64 = 46.9% | σ=((0, 1, 2, 3),(0, 1, 3, 2),(0, 1, 2, 3)) |
| Frobenius pos 1 only | 32/64 = 50.0% | σ=((0, 1, 3, 2),(0, 1, 2, 3),(0, 1, 2, 3)) |
| Frobenius all positions | 46/64 = 71.9% | σ=((0, 1, 3, 2),(0, 1, 3, 2),(0, 1, 3, 2)) |
| WC pos 3 only | 30/64 = 46.9% | σ=((0, 1, 2, 3),(0, 1, 2, 3),(2, 3, 0, 1)) |
| WC pos 2 only | 64/64 = 100.0% | σ=((0, 1, 2, 3),(2, 3, 0, 1),(0, 1, 2, 3)) |
| WC pos 1 only | 64/64 = 100.0% | σ=((2, 3, 0, 1),(0, 1, 2, 3),(0, 1, 2, 3)) |
| WC all positions | 60/64 = 93.8% | σ=((2, 3, 0, 1),(2, 3, 0, 1),(2, 3, 0, 1)) |
| Transition (U↔C, A↔G) | 48/64 = 75.0% | σ=((1, 0, 2, 3),(1, 0, 2, 3),(1, 0, 2, 3)) |

## Step 4: Exhaustive Search — Best (σ, τ) Pairs

Testing all componentwise domain involutions × all target involutions
(identity + single transpositions = 1 + 210 = 211 target involutions)

Domain involutions (componentwise, non-identity): 999
Target involutions: 211
Total pairs to test: 210789

### All matches with τ = identity (code symmetries)

These are NOT analogous to I Ching equivariance — they are trivial
symmetries where the domain involution preserves codons within fibers.
(Wobble degeneracy.)

| Violations | Domain σ | Description |
|------------|----------|-------------|
| 0/64 (0.0%) | (identity, identity, U↔C) | wobble symmetry |
| 4/64 (6.2%) | (identity, identity, A↔G, [Frobenius: x↦x²], [field automorphism]) | wobble symmetry |
| 4/64 (6.2%) | (identity, identity, U↔C, A↔G) | wobble symmetry |

### Best matches with NON-TRIVIAL τ (analogous to I Ching)

For comparison with f(~x) = -f(x): need non-trivial target involution.

| Violations | Domain σ | Target τ |
|------------|----------|----------|
| 2/64 (3.1%) | (identity, identity, U↔C) | swap(M,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(C,M) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(C,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(D,M) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(D,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(E,M) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(E,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(F,M) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(F,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(H,M) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(H,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(K,M) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(K,W) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(M,N) |
| 3/64 (4.7%) | (identity, identity, U↔C) | swap(M,Q) |

## Step 5: Coordinate Permutation Tests

Testing involutions that also permute codon positions.
Only checking the most biologically relevant: reverse complement.

### Best matches with coordinate reversal (≤ 10 violations)

No pairs found with ≤ 10 violations.

## Summary

**Best trivial equivariance (τ=id, wobble): 0/64 violations**
**Best non-trivial equivariance (τ≠id): 2/64 violations**

The genetic code DOES have perfect trivial equivariance: swapping U↔C
at position 3 preserves the amino acid. This is the well-known wobble
degeneracy — a code symmetry, not an involutory structure.

Near-equivariance with non-trivial τ: 2 violations.
Some structural pairing of amino acids is approximately respected.

### Structural comparison with I Ching

| Property | I Ching (3,5) | Genetic Code |
|----------|--------------|--------------|
| Domain | F₂³ (8 elements) | F₄³ (64 codons) |
| Target | Z₅ (5 elements) | 21 targets |
| Fiber shape | (2,2,2,1,1) | (6, 6, 6, 4, 4)... |
| Max/min ratio | 2 | 6 |
| Trivial equivariance (τ=id) | EXACT (complement) | EXACT (wobble) |
| Non-trivial equivariance | EXACT (τ=negation) | NONE (2/64 best) |
| Rigidity (orbits) | 1 (unique) | N/A (not rigid) |
| Target structure | Z₅ (cyclic, prime) | No group structure |

### Key finding

The genetic code is a surjection from a combinatorial domain (F₄³)
to a functional codomain (amino acids), just as the I Ching is a
surjection from F₂³ to Z₅. But the structural properties diverge:

1. **No equivariance**: The genetic code doesn't respect any natural
   involution on F₄³. The I Ching's equivariance is exact.
2. **No target group**: Amino acids have no natural cyclic order.
   Z₅'s cyclic structure is essential for the I Ching's rigidity.
3. **Heterogeneous fibers**: The genetic code's fiber sizes span
   1-6, much more varied than the I Ching's 1-2 range.
4. **The connection is architectural, not algebraic**: Both are
   surjections from combinatorial to functional space, but the
   genetic code lacks the algebraic constraints that make (3,5) rigid.