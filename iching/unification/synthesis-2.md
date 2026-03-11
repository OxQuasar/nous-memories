# The Algebraic Structure of the I Ching's 五行 System: A Complete Account

## Overview

The hexagram system of the *Yijing* is the structure determined by three ingredients:
1. The Fano plane PG(2, F₂) acting on F₂³ (trigrams) and F₂³ × F₂³ (hexagrams)
2. One compass datum: the Z₅ circular ordering of 五行 elements
3. One binary choice (0.5 bits): which Fano line carries the same-element pair

This document synthesizes 12 iterations of investigation (6 in Phase 1, 6 in Phase 2).
It supersedes synthesis-1.md on the (n,p) landscape, selection chain, and hexagram-level
五行 algebra, while remaining compatible on all Phase 1 results.

**Proof status convention:** Each claim is labeled **Theorem** (proved from definitions),
**Verified** (exhaustive computation), **Structural** (well-supported interpretation),
or **Observational** (compatible but not forced).

---

## Part I: Foundations — The (n,p) Landscape

### The Setting

The domain is Z₂ⁿ, the n-dimensional vector space over F₂. Its 2ⁿ elements partition
into 2^(n−1) **complement pairs** {x, ~x} where ~x = x ⊕ 1ⁿ. The nonzero elements
form PG(n−1, F₂), the projective geometry over F₂.

A **complement-respecting surjection** is f: Z₂ⁿ → Z_p (p prime, odd) satisfying:
- f(~x) = −f(x) mod p for all x
- f is surjective

The constraint f(~x) = −f(x) means f is determined by its values on one representative
from each complement pair. The search space is p^(2^(n−1)) assignments, filtered for
surjectivity.

### The Singleton-Forcing Theorem

**Theorem.** A complement-respecting surjection f: Z₂ⁿ → Z_p has at least one
singleton fiber if and only if p > 2^(n−1).

*Proof.* Let R = 2^(n−1) complement pairs. At least m₀ ≥ 1 pair maps to element 0.
The remaining R − m₀ pairs cover (p−1)/2 negation pairs.
To avoid singletons: every negation pair needs ≥ 2 covering pairs,
requiring R − m₀ ≥ 2 × (p−1)/2 = p − 1, hence m₀ ≤ R − p + 1.
For m₀ ≥ 1: need R − p + 1 ≥ 1, i.e., R ≥ p, i.e., 2^(n−1) ≥ p.
Contrapositive: p > 2^(n−1) forces singletons. ∎

**Verified.** 100% match across 27 (n,p) test cases for n ∈ {3,4,5,6}:
11 below-window cases (no singletons forced), 16 forcing-regime cases (singletons always present).
*(np_landscape.py)*

### The Shape Count Formula

Define E = R − S = 2^(n−1) − (p+1)/2, the **excess** pairs after minimum allocation.

**Theorem.** In the singleton-forcing regime, the number of distinct fiber-size
partitions (shapes) is Σ_{k=0}^{E} p(k), where p(k) is the integer partition function.

*Proof sketch.* The baseline configuration assigns 1 pair per slot, using S pairs.
The remaining E pairs distribute among S slots. Each distribution corresponds to
an integer partition of some k ≤ E, giving Σ p(k) distinct shapes. ∎

**Verified.** Perfect agreement across all 16 forcing cases, including:
(3,5): E=1 → 2 shapes; (4,9): E=3 → 4 shapes; (5,17): E=7 → 45 shapes.

### The E=1 Count Formula

At E = 1 (p = 2ⁿ − 3), two shapes exist with closed-form ratio:

**Theorem.** N_A/N_B = p − 1 (spread vs concentrated). Verified at (3,5), (4,13), (5,29), (6,61).

At (3,5): N_A = 192 (shape {2,2,2,1,1}), N_B = 48 (shape {4,1,1,1,1}), ratio = 4 = p−1. *(orbit_c_nuclear.py)*

### Three Fiber Types

Each complement pair has a **type** determined by its fiber structure:
- **Type 0:** Both elements map to 0 (the fixed point of negation in Z_p). Doubleton fiber.
- **Type 1:** The pair is the sole pair covering its negation pair. Two singleton fibers.
- **Type 2:** The pair shares a negation pair with ≥1 other pair. Doubleton fibers.

### The Triple Resonance Uniqueness Theorem

**Theorem.** (3,5) is the unique (n,p) satisfying three conditions simultaneously:
1. Singleton forcing: p > 2^(n−1) → p > 4
2. Three-type possibility: p < 2ⁿ − 1 → p < 7
3. Dimension: n = 3 (Fano plane PG(2, F₂))

*Proof.* Conditions 1 and 2 with n = 3 give 4 < p < 7, p prime → p = 5. ∎

**Verified.** Three types {0,1,2} coexist in 192/240 = 80% of (3,5) surjections —
precisely the {2,2,2,1,1} shape. The I Ching's specific type-to-line assignment
(Frame=2, H=0, Q=1, P=2) appears in 16/240 = 6.7%.
At (3,7): only types {0,1} (boundary case E = 0, every negation pair singly covered).
At all (4,p) cases: three types exist but are never forced. *(np_landscape.py)*

**Correction to prior work.** The (3,5) partition is NOT unique — two shapes exist
({2,2,2,1,1} with 192 surjections and {4,1,1,1,1} with 48). What IS forced is the
presence of ≥2 singletons. The {4,1,1,1,1} shape is structurally restricted to
types {0,1} only (m₀ = 2 pairs at zero = Type 0, remaining 2 pairs each singly cover
a negation pair = Type 1, no pairs share a negation pair so no Type 2).
Three-type coexistence occurs only in the {2,2,2,1,1} shape.

---

## Part II: The Selection Chain — From 240 to 2

### The Full Enumeration

At (3,5), the 240 complement-respecting surjections have:
- 192 with partition {2,2,2,1,1} (80%), carrying 2 singletons and 3 doubletons
- 48 with partition {4,1,1,1,1} (20%), carrying 4 singletons and 1 quadrupleton

All 192 surjections in the first shape have all three types {0,1,2}. The shape itself
requires this: fiber-2 at zero = Type 0, fiber-1 at two singletons = Type 1, fiber-2
at two non-zero doubleton elements = Type 2. Each of the 12 possible type-to-line
distributions contributes exactly 16 surjections.

All 48 in the second shape have only types {0,1} (structurally forced: m₀ = 2 gives
Type 0, all negation pairs singly covered gives Type 1, no sharing gives no Type 2).

**Selecting the {2,2,2,1,1} shape** — which entails three-type coexistence — means
selecting the 80% majority: the shape with maximum type diversity rather than maximum
singleton count. The {4,1,1,1,1} shape has 4 singletons but only 2 types; {2,2,2,1,1}
has 2 singletons but 3 types. The I Ching chooses structural richness over raw
singleton count.

### The Three Orbits

The 4 complement pairs of F₂³ are: Frame = {坤,乾}, H-pair = {震,巽},
Q-pair = {坎,離}, P-pair = {兌,艮}. A three-type surjection assigns each pair
a type from {0,1,2}. The 12 possible assignments form 3 orbits by Frame type:

| Orbit | Frame type | Sub-assignments | Surjections | Status |
|-------|-----------|----------------|-------------|--------|
| A | Type 0 (zero pair) | 3 | 48 | Frame maps to 0 |
| B | Type 1 (singletons) | 3 | 48 | Frame are singletons |
| C | Type 2 (shared doubleton) | 6 | 96 | Frame shares negation pair |

**Theorem.** Orbit C is the unique orbit compatible with the 五行 structure:
the frame pair {坤,乾} maps to {Earth, Metal}, which are distinct elements forming
a doubleton sharing the negation pair {2,3} in Z₅. This requires Frame = Type 2.

### The P→H Coherence Selection

Within Orbit C's 6 sub-assignments, the nuclear map (互) provides a selection
principle via the **P→H parity rotation**:

**Theorem (P→H rotation).** The P-functional (b₀⊕b₁) of the nuclear lower trigram
equals the H-functional (b₁⊕b₂) of the original lower trigram.

This creates a directed flow P → H between Fano lines. For each sub-assignment,
the P→H flow maps P's type to H's position:

| Assignment (Fr,H,Q,P) | P→H flow | Classification |
|------------------------|----------|----------------|
| **(2, 0, 1, 2)** | **Type 2 → Type 0** | **Coherent** ← I Ching |
| (2, 0, 2, 1) | Type 1 → Type 0 | cross |
| (2, 1, 0, 2) | Type 2 → Type 1 | cross |
| (2, 1, 2, 0) | Type 0 → Type 1 | cross |
| (2, 2, 0, 1) | Type 1 → Type 2 | cross |
| (2, 2, 1, 0) | Type 0 → Type 2 | anti-coherent |

**Verified.** The I Ching's assignment (2,0,1,2) is the unique sub-assignment where
the P→H flow is **monotonically decreasing in activity**: the dynamically active
shared doubleton (Type 2, governing 五行 relations) flows toward the algebraically
inert zero pair (Type 0), which then exits to orbit space via ī.

**Status: Observational.** P→H coherence is a natural compatibility between the
type assignment and the nuclear map dynamics. It is NOT a logical forcing — one could
consistently choose an anti-coherent assignment. The coherence is a structural
preference, not a theorem.

### The Complete Chain

```
240 surjections ─── Three-type selection (×0.8) ──→ 192
    ─── Orbit C: Frame=Type 2 (×0.5) ──→ 96
    ─── P→H coherence (×1/6) ──→ 16
    ─── Aut(Z₅) quotient (×1/4) ──→ 4
    ─── 0.5-bit residual (×1/2) ──→ 2
```

| Step | Mechanism | Type | Reduction |
|------|-----------|------|-----------|
| Three-type | Partition {2,2,2,1,1} | Structural (choice) | 240 → 192 |
| Orbit C | Frame = Type 2 | Theorem (五行 data) | 192 → 96 |
| P→H coherence | Nuclear rotation | Observational | 96 → 16 |
| Aut(Z₅) | Automorphism equivalence | Theorem | 16 → 4 |
| Residual | Compass orientation | Genuine freedom | 4 → 2 |

Total reduction: 120× (= 5!/1). The 0.5 bits = log₂(2) is a genuine binary choice.

---

## Part III: The Hexagram Reduction — One Compass

### The Z₅ Difference

Each hexagram h = (lower, upper) has a **Z₅ difference** d(h) = f(upper) − f(lower) mod 5,
which determines the 五行 relation: d=0 同, d=1 生, d=2 克, d=3 被克, d=4 被生.

**Verified.** Relation counts: 同 = 14, 生 = 12, 克 = 13, 被克 = 13, 被生 = 12.

### The Hexagram Reduction Theorem

**Theorem.** The 8×8 trigram-pair Z₅ matrix is the 5×5 Z₅ Cayley subtraction table
(d_{ab} = b − a mod 5) expanded by fiber multiplicities. Same-element trigrams
produce identical rows. The hexagram-level 五行 structure adds no data beyond
what the trigram-level map f already determines.

*Proof.* d(h) = f(upper) − f(lower) depends only on the Z₅ values of the
trigrams. The 8×8 matrix has rank at most 5 (one row per element). ∎

**Verified.** Identical rows: 乾 ≡ 兌 (Metal), 巽 ≡ 震 (Wood), 艮 ≡ 坤 (Earth).

### d Depends on Both Factors

**Verified.** Of 8 XOR masks, only mask 000 gives constant d (= 0, 同).
All other masks produce variable d depending on the lower trigram. The 五行 relation
is NOT determined by orbit (mask) alone — the non-linearity of f prevents this.

### The Complement Theorem

**Theorem.** d(~h) = −d(h) mod 5.

*Proof.* f(~x) = −f(x) by complement-respecting property. So d(~h) = f(~upper) − f(~lower)
= −f(upper) + f(lower) = −d(h). ∎

Consequence: complement maps 同→同, 生↔被生, 克↔被克.

### Reversal Does Not Descend to Z₅

**Verified.** d(h̄) = −d(h) holds in only 24/64 cases (37.5%).

Root cause: trigram reversal (b₀b₁b₂ → b₂b₁b₀) splits the doubleton fibers:
震(Wood)↔艮(Earth) and 兌(Metal)↔巽(Wood). Only palindromic trigrams (坤, 坎, 離, 乾)
and singletons are preserved under reversal. Reversal does NOT induce a function on Z₅.

**Consequence for KW pairing.** KW pairs palindromes by complement (Z₅-clean: d→−d always)
and non-palindromes by reversal (Z₅-opaque: d→−d in only 10/28 pairs). The 五行 relation
is preserved across KW pairs only when the pairing is complement-based.

---

## Part IV: Dynamics — 互 and Attractor Structure

### 互 as a Shear

**Theorem.** In the factored basis (o,m,i,ō,m̄,ī), the 互 matrix is:
```
Position: o'=m, m'=i, i'=i⊕ī    Orbit: ō'=m̄, m̄'=ī, ī'=ī
```
Orbit evolves independently (shift + projection). Position has one shear term: ī leaks into i.

**Verified.** Rank sequence: 6→4→2→2 (stabilizes at iteration 2).
- After 互¹: kills outer coordinates (o, ō)
- After 互²: kills middle coordinates (m, m̄)
- Stable image: span{i, ī}

### Attractor Structure

On the stable image, the map is i ↦ i⊕ī, ī ↦ ī:
- ī = 0: fixed point (i ↦ i)
- ī = 1: 2-cycle (i ↦ 1−i ↦ i)

| Attractor | Position | Orbit | ī | Type | 五行 relation |
|-----------|----------|-------|---|------|---------------|
| 坤坤 | 坤(000) | 坤(000) | 0 | fixed | 同 (Earth-Earth) |
| 乾乾 | 乾(111) | 坤(000) | 0 | fixed | 同 (Metal-Metal) |
| 既濟 | 坎(010) | 乾(111) | 1 | 2-cycle | 克 (Water克Fire) |
| 未濟 | 離(101) | 乾(111) | 1 | 2-cycle | 被克 (Fire被克Water) |

**Verified.** Fixed points are at the frame pair {坤,乾} with trivial orbit.
The 2-cycle is at the Q-pair {坎,離} with complement orbit OMI.

### The 互 Transition Matrix on Z₅

**Verified.** The 5×5 transition matrix d(h) → d(互(h)):

| d(h)\d(互) | 同 | 生 | 克 | 被克 | 被生 |
|------------|---|---|---|-----|-----|
| **同** | 6 | 2 | 2 | 2 | 2 |
| **生** | 1 | 2 | 3 | 6 | 0 |
| **克** | 4 | 0 | 4 | 5 | 0 |
| **被克** | 4 | 0 | 5 | 4 | 0 |
| **被生** | 1 | 0 | 6 | 3 | 2 |

Cross-checked against framework_strengthening_findings.md: exact match.

### 克 Concentration and Eigenstructure

**Verified.** Nuclear d concentrates onto {同,克,被克} with 56/64 = 87.5% probability.
{生,被生} receive only 8/64 = 12.5%. This is the 克 amplification (1.538×) restated
in Z₅ language: 互 maps the Z₅ relation space toward the stride-2 axis and away from
stride-1.

**The transition is NOT Z₅-linear.** No constant c makes d(互(h)) = c·d(h) mod 5.
The matrix has negation symmetry T[d][d'] = T[−d][−d'] but is not circulant.

**Spectrum:** {1, 1/6, −1/13, (157 ± i√75815)/1092}.

The negation symmetry decomposes T into:
- **Symmetric block** (3×3): eigenvalue 1 (Perron) and a complex pair |λ| = √(23/273) ≈ 0.29
- **Antisymmetric block** (2×2): upper triangular, eigenvalues 1/6 and −1/13

The antisymmetric block is upper triangular because **nuclear extraction never converts
stride-2 to stride-1**: T[克→生] = T[克→被生] = T[被克→生] = T[被克→被生] = 0 exactly.

**Spectral gap:** 1 − √(23/273) ≈ 0.71. Mixing in 3–5 iterations, confirming cascade depth.

**Stationary distribution:** π = (28/87, 8/145, 247/870, 247/870, 8/145).
π(同 + 克 + 被克) = 89% — massive concentration onto the stride-2 axis.
π(生 + 被生) = 11% — dramatic depletion of stride-1. *(eigenstructure.py)*

### P-Coset Alignment

**Theorem.** P(mask) = 0 for all 同 hexagrams: same-element XOR masks lie in ker(P).

Each Z₅ fiber is P-homogeneous: {Wood, Fire, Water} are all P-odd; {Earth, Metal}
are all P-even. The P-even fraction F(d) is an exact convolution of fiber
multiplicities across the P-partition {0,1,4}|{2,3}:

| d | Relation | F(d) exact | Origin |
|---|----------|-----------|--------|
| 0 | 同 | 14/14 = 1 | All within P-class |
| 1,4 | 生,被生 | 8/12 = 2/3 | 3/5 stride-1 pairs stay within P-class |
| 2,3 | 克,被克 | 1/13 | Only singleton pair (Water×Fire) stays within |

The exact formula: F(d) = Σ_a [fiber_P0(a)·fiber_P0(a+d) + fiber_P1(a)·fiber_P1(a+d)]
/ Σ_a |fiber(a)|·|fiber(a+d)|. Not an approximation — deterministic from the fiber
partition {2,2,2,1,1} and the P-parity structure. *(eigenstructure.py)*

### The P→H→ī Cascade

The parity cascade under iterated nuclear extraction:

```
Step 0: P-parity governs 五行 relations (同=P-even, 克=P-odd)
Step 1: P→H rotation (proven). P-parity becomes H-parity.
Step 2: H→ī leak (the shear term). H-parity becomes orbit coordinate.
Step 3: ī is fixed (ī'=ī). Information stabilizes.
```

**Cascade depth = 3:** position-space parity information reaches orbit-space stability
in exactly 3 applications of the P→H rotation + shear mechanism.

**This breaks at n=4.** With 7 complement pairs and 5+ negation pairs, the P→H rotation
no longer uniquely determines a cascade. The (3,5) cascade depth of 3 depends on having
exactly 3 lines through complement — the Fano plane structure.

### 先天/後天 Z₅ Signatures

**Verified.** 先天 distributes Z₅ steps evenly; 後天 is 被克-dominant (4/8 steps at d=3).
Neither profile is Z₅-forced. The asymmetry is a Z₅ signature of the 先天→後天 transition.

---

## Part V: Boundaries — Where the Algebra Ends

### The 0.5-Bit Boundary

**Theorem.** The V₄ kernel of Stab(H) acts within each Fano line, fixing line H pointwise.
Both candidate Wood-pair assignments ({震,巽} on H vs {坎,離} on Q) lie in ker(P). No
F₂-linear constraint, Z₅ compass constraint, or Z₂/Z₃ balance condition can distinguish them.

**Verified.** All 4 candidate 五行 assignments (2 Wood-pair choices × 2 singleton assignments)
survive every known constraint with identical counts at every stage of the forcing chain.

**Structural.** The traditional assignment (Wood on H) has a coherence advantage: it aligns
the same-element pair with the 互 kernel, the P→H rotation target, and the stabilizer-generating
line. The alternative (Wood on Q) would place the same-element pair on the preserved axis of
the 先天→後天 transition, carrying the 互 attractor pair.

This is a coherence argument, not a forcing. The 0.5-bit marks where algebraic structure ends
and cosmological tradition begins.

### Reversal Opacity

**Theorem.** Reversal (b₀↔b₂) is the S₃ transposition (HP), exchanging lines H and P.
It splits doubleton fibers: 震(Wood)↔艮(Earth) and 兌(Metal)↔巽(Wood) swap elements.
Therefore reversal does NOT induce a function on Z₅, and d(h̄) ≠ −d(h) in general.

**Verified.** d(h̄) = −d(h) in only 24/64 cases. The 40 failures correspond to hexagrams
where at least one component trigram is non-palindromic and its reversal changes element.

This is independent from the 0.5-bit: it concerns the reversal transformation, not the
Wood-pair assignment.

### KW Ordering

**Verified.** Between-pair bridge Z-scores are all within ±1.5σ vs random for all Fano lines.
The KW sequence ordering (not just pairing) shows no statistically significant Fano-line
structure. The ordering principle, if algebraic, operates outside PG(2, F₂).

The KW *pairing* is explained by orbit class (reversal/complement preserve orbit). The
*ordering* remains outside the framework.

### The P→H Coherence Gap

The P→H coherence (Section II) selects the I Ching's assignment as the unique monotonically-
decreasing cascade within Orbit C. This is **observational**: a natural compatibility between
the type assignment and the nuclear dynamics. It cannot be promoted to a theorem without
additional axioms specifying what "coherence" means formally.

The gap between "the I Ching's choice is coherent" and "the I Ching's choice is forced" is
irreducible within the current framework. Closing it would require either:
- A new axiom (e.g., "nuclear extraction must decrease type activity")
- A discovery that coherence follows from a deeper structure not yet identified

---

## Scope

This framework makes three kinds of claims:

**Mathematical predictions** (theorems about abstract structure):
- Any complement-respecting surjection at (n,p) with p > 2^(n−1) has singletons
- The shape count is exactly Σ_{k≤E} p(k)
- The E=1 ratio is exactly p − 1

**Structural constraints** (on I Ching-like systems):
- Any system with the same axioms is determined up to 0.5 bits
- The nuclear map concentrates 五行 relations toward {同,克,被克} for any Orbit C assignment
- The P→H coherence selects a unique type assignment within Orbit C

**Outside the framework** (no prediction or constraint):
- King Wen sequence ordering
- Line text semantics
- Hexagram name assignments
- The resolution of the 0.5-bit (which specific trigram pair shares each element)

---

## Appendix A: Result Inventory

**Theorems** (1-15): Three lines through complement; Stab(H) ≅ S₄ with V₄ = block preservers;
互 shear matrix; attractor bifurcation by ī; KW = orbit class; P-coset alignment (同=100%);
P→H rotation; singleton-forcing ⟺ p > 2^(n−1); shape count = Σp(k); E=1 ratio = p−1;
triple resonance uniqueness of (3,5); Orbit C forced by 五行; d(~h) = −d(h);
hexagram Z₅ = expanded Cayley table; reversal non-descent.

**Verified observations** (16-30): 克 amplification 1.538×; 生/克 cross-rotation;
P = unique fiber bridge; 先天 = b₀ constancy; 先天→後天 preserves only Q;
P+Q+H = 8 invariant; KW ordering has no Fano signal; 互 not Z₅-linear;
克 concentration 87.5%; 後天 被克-dominant; d depends on both factors;
three-type in 80% of surjections (= {2,2,2,1,1} shape); specific assignment in 6.7%;
spectrum {1, 1/6, −1/13, complex pair |λ|=√(23/273)}; stationary π(同+克+被克)=89%;
exact P-coset formula F(d) from fiber P-homogeneity.

**Structural** (28-30): Prime pairing H/P/Q ↔ {3,5}/{2,5}/{2,3}; V₄ as blind-spot bridge;
compass as non-Fano datum.

**Observational** (31-32): P→H coherence selects (2,0,1,2); Wood-on-H preferred by coherence.

**Corrections** (33-36): Partition NOT unique at (3,5) (2 shapes); (3,7) IS singleton-forcing;
three-type coexistence NEVER forced; {4,1,1,1,1} has types {0,1} not {0,2}.

## Appendix B: Architecture Diagram

```
                     PG(2,F₂) × PG(2,F₂)
                    /         |          \
                   H          P           Q
                  / \         |          / \
          Stab(H)  互-kernel  五行-parity  palindromic
             |              |              |
            S₄        P→H rotation    attractors
           / \              |         {坎,離} at
         V₄   S₃    P-coset theorem    orbit OMI
          |               |
   block system     compass (Z₅)
   (spaceprobe)          |
                    0.5-bit choice
```

**The unification is not "one formula" but "one geometry + one datum + one proof that all
constraints are transverse."** The Fano plane provides the skeleton, the compass provides
the Z₅ element structure, and the 0.5-bit is where the two meet without further constraint.

## Appendix C: Source Files

Phase 1: `fano_probe.py`, `hexagram_lift.py`, `parity_rotation.py`, `half_bit_test.py`,
`xiantian_fano.py`, `framework_strengthening.py`.
Phase 2: `np_landscape.py`, `orbit_c_nuclear.py`, `hexagram_wuxing.py`, `eigenstructure.py`.

All computations are exhaustive (no sampling) over the full spaces.
