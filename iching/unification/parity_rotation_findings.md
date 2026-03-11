# Parity Rotation and 五行 Dynamics: Findings

## 1. Parity Axis Rotation Under 互

### The P→H Rotation Theorem

**Theorem.** The 五行 parity (P = b₀⊕b₁) of the nuclear lower trigram
equals the H-parity (b₁⊕b₂) of the original lower trigram.

*Proof.* 互 maps (L1,L2,L3) → (L2,L3,L4). The P-functional
b₀⊕b₁ of (L2,L3,L4) = L2⊕L3 = b₁⊕b₂ of (L1,L2,L3). ∎

This means 互 **rotates the parity axis** from P to H.
But the rotation does NOT continue to Q: the next step maps H
into the orbit ī-coordinate (the shear term), escaping position space.

### Mask Parity Table

| Mask | Bits | P-flip | H-flip | In P-subgroup | In H-subgroup |
|------|------|--------|--------|---------------|---------------|
| id | 000 | 0 | 0 | ✓ | ✓ |
| O | 001 | 1 | 0 |  | ✓ |
| M | 010 | 1 | 1 |  |  |
| OM | 011 | 0 | 1 | ✓ |  |
| I | 100 | 0 | 1 | ✓ |  |
| OI | 101 | 1 | 1 |  |  |
| MI | 110 | 1 | 0 |  | ✓ |
| OMI | 111 | 0 | 0 | ✓ | ✓ |

P-subgroup = {id, OM, I, OMI} = ker(b₀⊕b₁)
H-subgroup = {id, O, MI, OMI} = ker(b₁⊕b₂) = H

### Relation × Parity Matrix

| Relation | P=,H= | P=,H≠ | P≠,H= | P≠,H≠ | Total | P-pres% |
|----------|-------|-------|-------|-------|-------|---------|
| 同 | 10 | 4 | 0 | 0 | 14 | 100% |
| 生 | 2 | 6 | 2 | 2 | 12 | 67% |
| 被生 | 2 | 6 | 2 | 2 | 12 | 67% |
| 克 | 1 | 0 | 6 | 6 | 13 | 8% |
| 被克 | 1 | 0 | 6 | 6 | 13 | 8% |

### Key Findings

1. **同 is 100% P-preserving.** Same-element hexagrams use only masks
   in the P-subgroup {id, OM, I, OMI}. They never cross the P-parity boundary.

2. **克/被克 is overwhelmingly P-flipping** (12/13 = 92%).
   The exclusive 克 masks are M(010) and MI(110), both P-flipping.

3. **生/被生 has mixed P-parity** (8/12 P-preserving, 4/12 P-flipping).
   The exclusive 生 mask is OM(011), which is P-preserving but H-flipping.

4. **The 互 rotation from P to H reverses parity alignment.**
   生-exclusive OM is P-preserving → H-flipping.
   克-exclusive MI is P-flipping → H-preserving (MI ∈ H).
   This creates a cross-rotation between 生 and 克 visibility under 互.

## 2. Z₅ Torus in Product Fano Geometry

### Cell Size Matrix

The Z₅ × Z₅ torus has cell sizes |fiber_lower| × |fiber_upper|:

| Lower\Upper | Wood | Fire | Earth | Metal | Water |
|-------------|------|------|-------|-------|-------|
| Wood | 4 | 2 | 4 | 4 | 2 |
| Fire | 2 | 1 | 2 | 2 | 1 |
| Earth | 4 | 2 | 4 | 4 | 2 |
| Metal | 4 | 2 | 4 | 4 | 2 |
| Water | 2 | 1 | 2 | 2 | 1 |

All 25 cells are cosets of F₂-subspaces (algebraically structured).

### 五行 Fibers

| Element | Trigrams | Size | Type | XOR | On Fano line |
|---------|----------|------|------|-----|-------------|
| Wood | {震,巽} | 2 | doubleton | OMI(111) | H, P, Q (all through-OMI) |
| Fire | {離} | 1 | singleton | — | ker(M), Q, ker(OMI) |
| Earth | {坤,艮} | 2 | doubleton | I(100) | ker(O), ker(M), P |
| Metal | {兌,乾} | 2 | doubleton | I(100) | ker(O), ker(M), P |
| Water | {坎} | 1 | singleton | — | ker(O), ker(I), Q |

**Key:** Wood's XOR = OMI lives on the three through-OMI lines (H, P, Q).
Earth and Metal share XOR = I, living on {ker(O), ker(M), P}.
P is the ONLY line containing BOTH doubleton XORs (I and OMI).

### Fano Lines and Element Count

| Line | Points | Elements | Distinct |
|------|--------|----------|----------|
| ker(O) | 坎,艮,巽 | Water/Earth/Wood | 3 |
| ker(M) | 震,艮,離 | Wood/Earth/Fire | 3 |
| P=ker(b₀⊕b₁) | 兌,艮,乾 | Metal/Earth/Metal | 2 |
| ker(I) | 震,坎,兌 | Wood/Water/Metal | 3 |
| Q=ker(b₀⊕b₂) | 坎,離,乾 | Water/Fire/Metal | 3 |
| H=ker(b₁⊕b₂) | 震,巽,乾 | Wood/Wood/Metal | 2 |
| ker(OMI) | 兌,離,巽 | Metal/Fire/Wood | 3 |

Only **P** and **H** have ≤2 distinct elements.
These are the '五行-degenerate' directions where movement can preserve element.

### Compass: The Non-Fano Datum

The 後天 compass provides the Z₅ circular ordering:
Fire→Earth→Metal→Metal→Water→Earth→Wood→Wood (around the circle).

No Fano line maps to equally-spaced compass positions (8/3 ∉ Z).
The compass IS the Z₅ datum that F₂ cannot express:
it encodes the 生-cycle ordering and the non-linear monotonicity constraint.

## 3. Synthesis Data

### Forcing Table

| Step | In | Out | Type | Factor | Fano |
|------|-----|-----|------|--------|------|
| 後天 Z₅ monotone | 96 | 8 | non-linear | ×12 | compass (non-Fano) |
| 後天 Z₂ yy-balance | 8 | 2 | F₂-linear (codim 2) | ×4 | P-line |
| 後天 Z₃ sons | 2 | 1 | F₂-linear (codim 1) | ×2 | ker(I) line |
| 五行 parity | 420 | 36 | F₂-linear | ×11.7 | P-functional |
| 五行 b₀ coset | 36 | 6 | F₂-linear | ×6 | O within P-coset |
| 五行 complement | 6 | 2 | non-linear | ×3 | OMI lines |
| 五行 cosmological | 2 | 1 | empirical | ×2 | 0.5-bit choice |
| Spaceprobe H | — | — | F₂-linear | — | H line (codim 1) |
| Spaceprobe blocks | — | — | non-linear (FPF) | — | V₄ ∩ Stab(H) |
| 互 shear | — | — | F₂-linear | — | ī→i coupling |
| 互 attractors | — | — | F₂-linear | — | Q-pair at OMI orbit |
| KW orbit class | — | — | theorem | — | rev/comp preserve orbit |

### Constraint Classification

- **F₂-linear** (7 steps): codimension counting in PG(2,2) or F₂⁶.
  Each imposes a Fano-aligned condition. Together they form the 'skeleton'.

- **Non-linear** (3 steps): Z₅ monotonicity, complement symmetry, FPF involutions.
  These are the 'gluing' constraints that connect the Fano skeleton to
  the compass ordering and the combinatorial block system.

- **Empirical** (1 step): the 0.5-bit cosmological choice.
  This is the one bit of data that CANNOT be derived from any known
  structural principle — the choice of which complement pair becomes Wood.

- **Theorem** (1 step): KW pairing = orbit class.
  Not a constraint but a consequence of reversal/complement preserving orbit.

### The Parity Rotation Mechanism

The single shear term i' = i ⊕ ī in the 互 matrix creates a cascade:

1. P-parity of nuclear = H-parity of original (P→H rotation)
2. H-parity of nuclear = ī (orbit datum, escapes position space)
3. This 'leak' from position to orbit IS the shear

The consequence for 五行 dynamics:
- 同 masks are P-preserving → after 互, become H-preserving → stable
- 克-exclusive M/MI flip P-parity → after 互, the nuclear hexagram
  may have different H-parity → parity disruption
- 生-exclusive OM preserves P → after 互, flips H → intermediate

This creates a hierarchy: 同 > 生 > 克 in terms of parity stability
under the 互 rotation, matching the traditional 五行 importance ordering.

### Unification Summary

The system is determined by three primes and one compass:

1. **Prime 2** → PG(2,2) × PG(2,2) structure, 互 as F₂-linear shear,
   Fano lines H/P/Q as constraint axes, V₄ kernel, attractor geometry

2. **Prime 3** → Z₃ sons constraint, ker(I) line, 互 convergence in 3 steps

3. **Prime 5** → 五行 element classes, 生/克 cycle, Z₅ torus structure

4. **Compass** → Z₅ circular embedding, non-Fano ordering,
   the one datum that is structurally underdetermined (0.5-bit choice)

The Fano plane is the common arena where primes 2 and 3 meet.
Prime 5 lives on the compass, touching the Fano plane only through
the P-line (五行 parity) and the through-OMI lines (complement pairs).
The 0.5-bit choice is where Z₅ meets Z₂ and no further constraint resolves it.
