# Unification Synthesis: The Hexagram System as PG(2,2) Decorated with One Compass

> **Bit convention A:** b₀ = bottom line, b₂ = top line. See `directory.md` for project standard.

## Overview

The hexagram system of the *Yijing* is the structure determined by:
1. The Fano plane PG(2,2) acting on F₂³ (trigrams) and F₂⁶ = F₂³ × F₂³ (hexagrams)
2. One compass datum: the Z₅ circular ordering of 五行 elements

All known structural features — the 五行 element classes, the 互 nuclear transformation,
the King Wen pairing, the spaceprobe block system, the 後天 compass arrangement, and the
attractor dynamics — follow from these two inputs plus the encoding convention, with
exactly 0.5 bits of residual freedom.

This document compiles the computational evidence from six iterations of investigation.
Each claim is labeled: **Theorem** (proven from definitions), **Verified** (computed and
checked exhaustively), **Structural** (well-supported interpretation), or **Conjecture**
(untested or partially supported).

---

## Part I: The Trigram Fano Plane

### The Geometry

The 8 trigrams form the vector space F₂³ under XOR addition. The 7 nonzero
elements are the 7 points of PG(2,2), the Fano plane. Its 7 lines are the
kernels of the 7 nonzero linear functionals f: F₂³ → F₂, restricted to
nonzero points.

**Encoding.** b₂b₁b₀ where b₀ = bottom line, b₂ = top line.
Generators: O = 001 (flip b₀), M = 010 (flip b₁), I = 100 (flip b₂).

### The Three Distinguished Lines

**Verified.** Exactly 3 of the 7 Fano lines pass through the complement
point OMI = 111 (乾). Each carries one of the three complement pairs
{x, x ⊕ 111}:

| Line | Functional | Points | Complement pair | 五行 types | Dest. type |
|------|-----------|--------|-----------------|-----------|-----------|
| **H** | ker(b₁⊕b₂) | 震,巽,乾 | {震,巽} Wood/Wood | k₀ (same) | 互 kernel |
| **P** | ker(b₀⊕b₁) | 兌,艮,乾 | {兌,艮} Metal/Earth | k₂ (diff doubleton) | 五行 parity |
| **Q** | ker(b₀⊕b₂) | 坎,離,乾 | {坎,離} Water/Fire | k₁ (singletons) | palindromic |

*Source: fano_probe.py Computation 1. All 7 lines enumerated, 3 through OMI verified,
complement pair content and destination types verified.*

### Structural Roles

Each line carries a distinct algebraic role:

- **H = ker(b₁⊕b₂)**: The 互 kernel — the subspace whose stabilizer generates S₄.
  Lines on H have b₁ = b₂ (middle = inner). H is the unique Fano line whose cosets
  refine the spaceprobe block system. *(Verified: fano_probe.py Computation 3.)*

- **P = ker(b₀⊕b₁)**: The 五行 parity axis — the functional that separates 五行
  classes into even/odd cosets. P is the unique line through OMI whose coset partition
  keeps all three doubleton element pairs within cosets. *(Verified: fano_probe.py
  Computation 4. P keeps 3/3 pairs vs. 1/3 for H and Q.)*

- **Q = ker(b₀⊕b₂)**: The palindromic condition — lines on Q have b₀ = b₂
  (outer = inner). The 互 attractor 2-cycle lives at the Q-pair positions {坎,離}.
  *(Verified: hexagram_lift.py Computation 3.)*

### Prime-Pair Correspondence

**Structural.** The three lines correspond to the three coprime pairings
of the system's three structural primes {2, 3, 5}:

| Line | Prime pair | Coupling |
|------|-----------|----------|
| P | {2, 5} | polarity × 五行 relation |
| Q | {2, 3} | polarity × spatial position |
| H | {3, 5} | position × relation |

*This is interpretive: each line mediates the interaction between two of the three
number-theoretic structures. The identification is supported by the algebraic roles
but not uniquely forced.*

### The Stabilizer

**Theorem.** |GL(3,F₂)| = 168. **Verified.** |Stab(H)| = 24 = |S₄|.

**Verified.** Stab(H) has exact sequence:
```
1 → V₄ → Stab(H) → S₃ → 1
```
where S₃ permutes the 3 points of line H, and V₄ fixes line H pointwise.

**Verified.** The V₄ kernel equals exactly the 4 elements of Stab(H) that
preserve the spaceprobe block system {坤震, 艮兌, 坎離, 巽乾}.
Only 4/24 elements of Stab(H) preserve the blocks.

*Source: fano_probe.py Computation 2. All 168 GL(3,F₂) elements enumerated,
24-element stabilizer extracted, V₄ kernel identified, block preservation tested.*

**Structural.** V₄ is the "blind spot" bridge — the maximal subgroup shared by
both the linear Stab(H) and the (non-linear) spaceprobe S₄. The linear/non-linear
boundary runs through V₄.

### Fano Lines and 五行 Compatibility

**Verified.** Only two Fano lines have ≤2 distinct 五行 elements among their
three points:
- **P**: Metal/Earth/Metal (2 elements)
- **H**: Wood/Wood/Metal (2 elements)

All other 5 lines have 3 distinct elements. P and H are the "五行-degenerate"
directions: movement along them can preserve element class.

**Verified.** P is the unique Fano line containing both doubleton fiber XORs:
I(100) for Earth/Metal and OMI(111) for Wood. P is the "fiber bridge."

*Source: parity_rotation.py Computation 2.*

---

## Part II: The Hexagram Product Geometry

### Product Structure

Each hexagram is a pair of trigrams: (lower, upper) ∈ F₂³ × F₂³.
In the **factored basis** (o, m, i, ō, m̄, ī):
- Position coordinates (o, m, i) = lower trigram (L₁, L₂, L₃)
- Orbit coordinates (ō, m̄, ī) = palindromic signatures (L₁⊕L₆, L₂⊕L₅, L₃⊕L₄)

Each factor has its own copy of PG(2,2). The product PG(2,2) × PG(2,2) organizes
the hexagram space.

### The 互 Map

**Theorem.** In the factored basis, the 互 matrix is:
```
o' = m      ō' = m̄
m' = i      m̄' = ī
i' = i ⊕ ī  ī' = ī
```

**Verified.** The orbit factor evolves independently (pure shift + projection).
The position factor has one additive correction: **ī leaks into i**.
This is the minimal departure from a product map — a single shear term.

*Source: hexagram_lift.py Computation 2. Matrix computed by explicit basis
transformation of the standard 互 matrix.*

### Rank Sequence and Attractors

**Verified.** Rank sequence: 6 → 4 → 2 → 2 (stabilizes).
- After M¹: kills o, ō (outer coordinates)
- After M²: kills m, m̄ (middle coordinates)
- Stable image: span{i, ī} (inner coordinates, one from each factor)

**Theorem.** On the stable image:
- i ↦ i ⊕ ī, ī ↦ ī
- If ī = 0: fixed point (i ↦ i)
- If ī = 1: 2-cycle (i ↦ 1−i ↦ i)

**Verified.** The four 互 attractors, with Fano alignment:

| Attractor | Hex | Position | Orbit | ī | Type |
|-----------|-----|----------|-------|---|------|
| 乾 Qian | 111111 | 乾(111) | 坤(000) | 0 | fixed |
| 坤 Kun | 000000 | 坤(000) | 坤(000) | 0 | fixed |
| 既濟 JiJi | 010101 | 坎(010) | 乾(111) | 1 | 2-cycle |
| 未濟 WeiJi | 101010 | 離(101) | 乾(111) | 1 | 2-cycle |

The fixed points have position from the frame pair {坤,乾} with trivial orbit.
The 2-cycle has position from the Q-line pair {坎,離} with complement orbit OMI.

*Source: hexagram_lift.py Computation 3.*

### The KW Orbit Theorem

**Theorem.** All King Wen within-pair bridges have Δorb = 0. KW pairing
operates entirely within the position factor.

*Proof:* KW pairs are either reversals or complements. Reversal swaps
(L₁,...,L₆) → (L₆,...,L₁), preserving all Lᵢ ⊕ L₇₋ᵢ.
Complement flips all bits, also preserving XOR pairs. Both operations
fix the orbit coordinates. ∎

**Verified.** 100% of 32 KW within-pair bridges have Δorb = (0,0,0).
Line H is enriched in position bridges: 52.5% vs 42.9% expected.

*Source: hexagram_lift.py Computation 4.*

---

## Part III: The Five-Element Interface

### 五行 as a Set Function

The 五行 assignment maps trigrams to elements:
```
Earth = {坤(000), 艮(100)}    Wood  = {震(001), 巽(110)}
Metal = {兌(011), 乾(111)}    Fire  = {離(101)}    Water = {坎(010)}
```

This is a set function F₂³ → Z₅, **not** a linear map (Earth = {000, 100}
is not a subspace of F₂³ — it contains the origin but is not closed under
addition since 000 ⊕ 100 = 100 ∈ Earth ✓, but Earth has only 2 elements
while the subspace generated by 100 would need to include 000 and 100,
which it does — so Earth IS a 1-dimensional subspace).

More precisely: the three doubleton fibers are F₂-cosets:
- Earth = {000, 100} = ⟨I⟩ (1-dimensional subspace)
- Metal = {011, 111} = 011 + ⟨I⟩ (coset of ⟨I⟩)
- Wood = {001, 110} = 001 + ⟨OMI⟩ ... no. Wood XOR = 111.

The fibers are cosets but of different subgroups: Earth and Metal are cosets
of ⟨I⟩ = {000, 100}; Wood is a coset of ⟨OMI⟩ = {000, 111}. This
heterogeneity is exactly the non-linearity of the 五行 map.

**Verified.** All 25 cells of the Z₅ × Z₅ torus (lower element × upper element)
are F₂-cosets in F₂⁶. Cell sizes = product of fiber sizes.

*Source: parity_rotation.py Computation 2.*

### The P-Coset Alignment Theorem

**Theorem.** 同 (same-element) hexagrams are 100% P-preserving. That is,
if lower and upper trigrams have the same 五行 element, their XOR mask
preserves the P-functional b₀⊕b₁.

*Proof:* Same-element XOR masks are:
- Earth within: 000 ⊕ 100 = I(100). P-flip = b₀⊕b₁ of 100 = 0. ✓
- Metal within: 011 ⊕ 111 = I(100). Same. ✓
- Wood within: 001 ⊕ 110 = OMI(111). P-flip = b₀⊕b₁ of 111 = 0. ✓
- Singletons: XOR = 000. P-flip = 0. ✓

All same-element XOR masks lie in ker(b₀⊕b₁) = the P-subgroup. ∎

**Verified.** Distribution across all 64 hexagrams:

| Relation | P-preserving | Total | P-pres % |
|----------|-------------|-------|----------|
| 同 | 14 | 14 | **100%** |
| 生/被生 | 16 | 24 | 67% |
| 克/被克 | 2 | 26 | **8%** |

*Source: parity_rotation.py Computation 1.*

### The P→H Parity Rotation

**Theorem.** The 互 map rotates the 五行 parity axis: the P-functional
(b₀⊕b₁) of the nuclear lower trigram equals the H-functional (b₁⊕b₂)
of the original lower trigram.

*Proof:* 互 maps lower (L₁,L₂,L₃) → nuclear lower (L₂,L₃,L₄).
P applied to nuclear = b₀⊕b₁ of (L₂,L₃,L₄) = L₂⊕L₃.
H applied to original = b₁⊕b₂ of (L₁,L₂,L₃) = L₂⊕L₃. ∎

**Verified.** The rotation does NOT continue to Q. The next step
maps H-parity to ī (an orbit coordinate), escaping position space.
This is precisely the shear term: L₃⊕L₄ = ī.

*Source: parity_rotation.py Computation 1.*

### The 生/克 Cross-Rotation

**Verified.** The exclusive masks for each 五行 relation are:

| Mask | Exclusive to | P-preserving | H-preserving |
|------|-------------|-------------|-------------|
| id (000) | 同 | ✓ | ✓ |
| OM (011) | 生/被生 | ✓ | ✗ |
| M (010) | 克/被克 | ✗ | ✗ |
| MI (110) | 克/被克 | ✗ | ✓ (MI ∈ H) |

The 互 rotation P→H swaps parity alignment:
- 生-exclusive OM: P-preserving → becomes H-flipping after rotation
- 克-exclusive MI: P-flipping → becomes H-preserving (MI ∈ H!)

**Structural.** This creates a parity stability hierarchy: 同 > 生 > 克.
After 互 applies the P→H rotation, 同 masks remain aligned, 生 masks lose
P-alignment but don't gain H-alignment, and 克 masks (MI) gain H-alignment.
The rotation mechanism exchanges which relations are parity-visible.

*Source: parity_rotation.py Computations 1 and 3.*

---

## Part IV: The Rigidity Decomposition

### Complete Forcing Table

| Step | Input | Output | Type | Factor | Fano involvement |
|------|-------|--------|------|--------|-----------------|
| 後天 Z₅ monotone | 96 | 8 | non-linear | ×12 | compass (non-Fano) |
| 後天 Z₂ yy-balance | 8 | 2 | F₂-linear (codim 2) | ×4 | P-line |
| 後天 Z₃ sons | 2 | 1 | F₂-linear (codim 1) | ×2 | ker(I) line |
| 五行 parity | 420 | 36 | F₂-linear | ×11.7 | P-functional |
| 五行 b₀ coset | 36 | 6 | F₂-linear | ×6 | O within P-coset |
| 五行 complement | 6 | 2 | non-linear | ×3 | OMI (complement) |
| 五行 cosmological | 2 | 1 | **genuine choice** | ×2 | H vs Q line assignment |

Additional structural constraints (not in a reduction chain):
| Constraint | Type | Fano |
|-----------|------|------|
| Spaceprobe H-subspace | F₂-linear | H = ker(b₁⊕b₂) |
| Spaceprobe block system | non-linear (FPF) | V₄ ∩ Stab(H) |
| 互 shear structure | F₂-linear | ī → i coupling |
| 互 attractor alignment | F₂-linear | Q-pair at OMI orbit |
| KW pairing = orbit | theorem | rev/comp preserve orbit |

### Constraint Classification

**F₂-linear constraints (7):** These are Fano-aligned codimension conditions.
Each imposes a linear condition over F₂, reducing the space by a power of 2.
Together they form the geometric "skeleton."

**Non-linear constraints (3):** Z₅ monotonicity (compass ordering), complement
symmetry (OMI structure), and FPF involutions (spaceprobe blocks). These are
the "gluings" that connect the Fano skeleton to structures that F₂ cannot express.

**Genuine free parameter (1):** The 0.5-bit cosmological choice — which
complement pair becomes the same-element doubleton (Wood). See below.

**Theorem (1):** KW pairing = orbit class. Not a constraint but a consequence
of reversal and complement preserving palindromic signatures.

### The 0.5-Bit Test

**Verified.** The 0.5-bit cannot be forced by any combination of:
- F₂-linear constraints (Fano geometry)
- Z₅ compass constraints (He Tu cardinals, 生-cycle monotonicity)
- Z₂/Z₃ constraints (yin-yang balance, sons placement)

All four candidate 五行 assignments (two Wood pair choices × two singleton
assignments) survive every known constraint with **identical counts**:
96 cardinal-aligned → 56 sheng-monotone → ... at every stage.

*Source: half_bit_test.py. All 4! × 2⁴ = 384 compass arrangements tested
for each of the 4 candidate assignments.*

**Why identical:** The four assignments are isomorphic under compass geometry.
Earth and Metal classes are fixed; the remaining four trigrams are just relabeled
among {Wood, Fire, Water}. Both candidate Wood pairs have XOR = OMI, which lies
on all three through-OMI lines. No compass or F₂ constraint can distinguish them.

**What distinguishes them:** The two Wood pair choices differ in Fano line alignment:

| | Traditional | Alternative |
|---|-----------|------------|
| Wood pair | {震,巽} on **H** | {坎,離} on **Q** |
| 互 attractor elements | Water/Fire (克) | Wood/Wood (同) |
| P→H rotation target | carries same-element pair | carries diff-element pair |

**Structural argument for traditional:** Placing the same-element pair on H
makes H simultaneously the 互 kernel line, the stabilizer-generating line,
and the 五行-internal direction. The P→H parity rotation sends 五行 parity
toward the element-preserving direction. This is a coherence argument, not a
logical forcing.

**Conclusion:** The system has exactly 0.5 bits of genuine freedom.

**Origin of the 0.5 bits (reduction chain from np_landscape analysis).**
At (3,5), the 192 three-type surjections (partition {2,2,2,1,1}) decompose as:

1. **12 pre-symmetry options.** Each three-type surjection assigns one pair to each of
   Types 0, 1, 2, with the fourth pair also Type 2. The number of ordered type
   distributions is C(4,1) × C(3,1) × 1 = 12 (choose Type 0 pair, Type 1 pair,
   rest are Type 2). Each contains exactly 16 surjections.

2. **3 S₃ orbits.** S₃ acts on {H, P, Q} (the non-frame lines). The 12 distributions
   split by Frame type: Orbit A (Frame = Type 0, 3 options), Orbit B (Frame = Type 1,
   3 options), Orbit C (Frame = Type 2, 6 options). Within each orbit, S₃ acts
   transitively on the non-frame assignments.

3. **1 by structural elimination.** Orbit C (Frame = Type 2) is the unique orbit where
   the frame pair shares a negation pair with a non-frame pair, matching the I Ching's
   structure (坤/乾 share {Earth,Metal} with 艮/兌). The other orbits have Frame as
   Type 0 (坤/乾 both map to 0) or Type 1 (坤/乾 as singletons), which contradicts
   the 五行 assignment. Orbit C has 6 sub-options.

4. **2 residual choices → 0.5 bits.** Within Orbit C's 6 sub-options, the algebraic
   structure distinguishes which non-frame pair is Type 0 (the "same-element" doubleton =
   Wood). This is the choice between H and Q carrying Wood. P is forced to Type 2
   (shares negation pair with Frame). So: 6 options / S₃ action on the Type 0/1
   assignment to {H,Q,P} → 2 remaining choices (H=0,Q=1 vs H=1,Q=0) after fixing P=2.

The I Ching picks H=0 (Wood on 互 kernel), Q=1 (Water/Fire singletons on palindromic line).

---

## Part V: The Unification Claim

### Statement

> The hexagram system is PG(2,2) decorated with one compass.

More precisely: the algebraic structure of the 64 hexagrams — their 五行 element
classes, the 互 nuclear transformation, the King Wen pairing, the spaceprobe
block system, the 後天 compass arrangement, and the attractor dynamics — is
determined by:

1. **PG(2,2) × PG(2,2):** The product Fano geometry on F₂³ × F₂³, with three
   distinguished lines H, P, Q through the complement point, and one shear
   coupling the factors.

2. **One compass:** The Z₅ circular ordering that provides the 五行 生-cycle,
   He Tu cardinal alignment, and 後天 monotonicity.

3. **One choice (0.5 bits):** Which through-OMI line carries the same-element pair.

### What the Framework Explains

**With proof (theorem or exhaustive verification):**

1. **Three complement pairs on three lines.** The Fano geometry forces exactly
   3 lines through OMI, each carrying one complement pair with a distinct 五行
   destination type. *(fano_probe.py)*

2. **Stab(H) ≅ S₄ with V₄ = block preservers.** The linear stabilizer of H
   is S₄, and its V₄ kernel exactly equals the spaceprobe block-preserving
   subgroup. *(fano_probe.py)*

3. **互 is a shear on PG(2,2) × PG(2,2).** In the factored basis, orbit
   evolves independently; one term (ī→i) couples the factors. *(hexagram_lift.py)*

4. **Attractor bifurcation from ī.** Fixed points at ī=0 (frame pair, origin orbit),
   2-cycle at ī=1 (Q-pair, complement orbit). *(hexagram_lift.py)*

5. **KW pairing = orbit class.** Reversal and complement preserve orbit.
   All within-pair bridges have zero orbit delta. *(hexagram_lift.py)*

6. **同 = 100% P-preserving.** Same-element masks lie entirely in ker(P).
   *(parity_rotation.py)*

7. **P→H parity rotation under 互.** The 五行 parity axis rotates to the
   H-line, then escapes to orbit (the shear). *(parity_rotation.py)*

8. **生/克 cross-rotation.** Exclusive masks swap parity alignment:
   生-exclusive OM is P-preserving→H-flipping; 克-exclusive MI is the
   reverse. *(parity_rotation.py)*

9. **P is the unique fiber bridge.** P contains both doubleton XORs (I and OMI),
   bridging the Earth/Metal fiber and the Wood fiber. *(parity_rotation.py)*

10. **Z₅ torus cells are F₂-cosets.** The 25 element-pair cells have algebraic
    structure. *(parity_rotation.py)*

11. **The 0.5-bit is genuine.** No known constraint forces the Wood pair
    assignment. All candidates produce isomorphic compass arrangements.
    *(half_bit_test.py)*

12. **先天 is a Fano triangle walk.** The 先天 arrangement is a Hamiltonian
    cycle on F₂³ using generators {O, I, MI}, a triangle in PG(2,2) with
    one edge on H. It belongs to Family H (one of 3 families of 4 triangle
    generator sets, classified by through-OMI edge). *(xiantian_fano.py)*

13. **The 先天→後天 transition preserves only Q.** Among 4 complement-
    antipodal axes, only Q ({坎,離}) survives. Q goes from 0/8 to 4/8
    hits in step-XORs. The transition introduces Q-line structure.
    *(xiantian_fano.py)*

14. **P+Q+H = 8 theorem.** In any complement-antipodal Hamiltonian cycle on
    F₂³, no step-XOR equals OMI (complements are at distance 4, not 1).
    Each step hits exactly 1 of {P,Q,H}, giving the invariant P+Q+H = 8.
    *(framework_strengthening.py)*

15. **克 amplification = 1.538×.** The full 互 transition matrix on 五行
    relations: 克/被克 amplified from 13/64 to 20/64; 生/被生 suppressed
    from 12/64 to 4/64; 同 slightly amplified. 克's P-flip rate is 92.3%,
    confirming the parity rotation mechanism. *(framework_strengthening.py)*

16. **先天 uniqueness = b₀ constancy.** Among the 2 undirected complement-
    antipodal {O,I,MI} cycles, 先天 is the unique one where b₀ is constant
    within each semicircle: (1,1,1,1,0,0,0,0) = yang/yin separation.
    *(framework_strengthening.py)*

17. **KW ordering has no Fano signal.** Between-pair bridge Z-scores all
    within ±1.5σ vs random. The sequence ordering is outside PG(2,2).
    *(framework_strengthening.py)*

**With structural argument (well-supported interpretation):**

18. **H/P/Q ↔ {3,5}/{2,5}/{2,3} prime pairing.** Each line mediates the
    interaction between two of the three structural primes.

19. **V₄ as the blind-spot bridge.** The maximal subgroup shared by linear
    and non-linear S₄ structures, straddling the linear/non-linear boundary.

20. **The compass as the non-Fano datum.** Z₅ is coprime to 2; no Fano
    structure can express cyclic ordering. The compass IS the Z₅ embedding.

21. **Traditional assignment preferred by coherence.** Placing Wood on H
    aligns the same-element pair with the 互 kernel, the parity rotation
    target, and the stabilizer-generating line. The 先天→後天 transition
    context adds: the H-axis is BROKEN by the transition, while the Q-axis
    (carrying Water/Fire singletons = 互 attractors) is PRESERVED.

### The 先天 Walk and 先天→後天 Transition

**Verified.** The 先天 (Earlier Heaven) arrangement is a Hamiltonian cycle
on F₂³ using generators {O(001), I(100), MI(110)} with step pattern
(I, MI, I, O) × 2.

These three generators form a **triangle** in PG(2,2) with edges on
H, ker(O), ker(M). There are 12 three-element generator sets (in 3 families
of 4 by through-OMI edge) admitting complement-antipodal Hamiltonian cycles.
No single Fano line admits any cycle at all.

先天 uses Family H (edge on the 互 kernel line). Within Family H, {O, I, MI}
is the unique member with single-bit edges (ker(b₀), ker(b₁)) — the most
"coordinate-aligned" triangle.

**Verified.** The 先天→後天 transition:
- Is a permutation with cycle structure (two 4-cycles, related by 180° rotation)
- Breaks 3 of 4 complement-antipodal pairs, preserving only Q-axis {坎,離}
- Introduces Q-line generators (absent from 先天: 0/8 → 4/8)
- Increases generator count from 3 to 5
- Is NOT a dihedral element

**Structural.** The 0.5-bit acquires geometric context through the transition:
the traditional assignment places the same-element pair on H (the BROKEN axis),
while the alternative places it on Q (the PRESERVED axis). The preserved Q-axis
carries the 互 attractor pair (坎/離 = Water/Fire).

*Source: xiantian_fano.py.*

### What Remains Outside the Framework

1. **King Wen ORDERING.** The KW sequence (not just pairing) assigns specific
   positions 1–64 to hexagrams. The pairing (into 32 pairs) is explained by
   orbit class, but the linear ordering within and between pairs is not addressed.
   **Probed and confirmed:** between-pair bridges show no statistically significant
   Fano-line structure (all Z-scores within ±1.5σ vs random). *(framework_strengthening.py)*

2. **Textual and semantic content.** The hexagram names, judgments, line texts,
   and interpretive traditions are outside the algebraic framework.

3. **Higher-order dynamics.** Iterated 互 beyond the attractor analysis;
   interactions between 互 and other transformations (錯, 綜, etc.).

### The Three Heterogeneous Gluings

The system has three types of non-F₂ constraint:

| Gluing | Connects | Nature |
|--------|----------|--------|
| Z₅ monotonicity | Fano ↔ compass | non-linear (cyclic ordering) |
| Complement symmetry | OMI ↔ element pairs | non-linear (involves 五行 map) |
| FPF involutions | Fano ↔ block system | non-linear (permutation-theoretic) |

These are NOT a defect — they ARE the structure. The coprime components
(2, 3, 5) must be glued heterogeneously because they contribute different
kinds of mathematical substance:
- Prime 2 gives the vector space (F₂ linear algebra, Fano geometry)
- Prime 3 gives the convergence rate (互 stabilizes in 3 steps) and
  the sons constraint (ker(I) line)
- Prime 5 gives the element partition and the compass ordering

The gluings are the minimal inter-prime connections. The shear term (ī→i)
is the unique F₂-linear coupling between position and orbit factors. The
compass is the unique non-F₂ datum. The V₄ is the unique subgroup bridging
linear and non-linear structures.

### The Architecture

```
                    PG(2,2) × PG(2,2)
                   /        |         \
                  H         P          Q
                 / \        |         / \
            Stab(H)  互-kernel  五行-parity  palindromic
               |              |              |
              S₄         P→H rotation    attractors
             / \              |           {坎,離}
           V₄   S₃     生/克 cross-     at orbit
            |              rotation        OMI
     block system              |
     (spaceprobe)        compass (Z₅)
                              |
                        0.5-bit choice
```

The unification is not "one formula" but "one geometry + one datum + one proof
that all constraints are transverse."

---

## Appendix: Source Files

| File | Lines | Contents |
|------|-------|---------|
| `fano_probe.py` | 929 | Fano atlas, GL(3,F₂) stabilizer, block correspondence, transversality |
| `fano_findings.md` | 194 | Trigram-level Fano results |
| `hexagram_lift.py` | 879 | Product Fano, 互 factored matrix, attractors, KW bridges |
| `hexagram_lift_findings.md` | 427 | Hexagram-level product structure results |
| `parity_rotation.py` | ~700 | P→H rotation, mask×parity, Z₅ torus, forcing table |
| `parity_rotation_findings.md` | 182 | 五行 dynamics and synthesis data |
| `half_bit_test.py` | ~440 | 0.5-bit test across all 4 candidate assignments |
| `half_bit_findings.md` | ~100 | 0.5-bit test results |
| `xiantian_fano.py` | ~570 | 先天 Fano walk, 後天 transition, symmetry breaking |
| `xiantian_fano_findings.md` | ~170 | 先天/後天 Fano structure results |
| `framework_strengthening.py` | ~700 | P-invariance, 克 amplification, 先天 uniqueness, KW probe |
| `framework_strengthening_findings.md` | ~120 | Strengthening results |

All computations are exhaustive (no sampling). All claims labeled as "verified"
have been checked against the full spaces (8 trigrams, 64 hexagrams, 168 GL(3,F₂)
elements, 420 partitions, 384 compass arrangements per assignment).
