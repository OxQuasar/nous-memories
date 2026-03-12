# Unification Phase 3: The Object — COMPLETE

## Where we are

Phase 1 answered "what is the structure at (3,5)?" — PG(2,F₂) decorated with one compass, 17 proven results.

Phase 2 answered "how is it selected?" — selection chain 240→2, eigenstructure, (n,p) landscape, singleton-forcing theorem.

Phase 3 answered: **what IS it?** — the unique complement-respecting surjection F₂³ → Z₅ with three-type coexistence, proven unique by a theorem.

**Status: COMPLETE.** The definitive account is `synthesis-3.md` (519 lines, 15 theorems, 13 verified computations, 4 conjectures).

---

## The answer

The I Ching's 五行 assignment is a complement-respecting surjection f: F₂³ → Z₅ satisfying f(x ⊕ 111) = −f(x) mod 5. It is **unique up to the natural symmetry** Stab(111) × Aut(Z₅), which acts regularly (free + transitive) on the 96 Orbit-C surjections.

This uniqueness is itself unique. The orbit count formula

> **Orbits(n, p) = ((p−3)/2)! × 2^{2^{n−1}−1−n}**

equals 1 **if and only if** (n, p) = (3, 5), following from two independent arithmetic conditions:

1. **p = 5**: the smallest prime with independent generation/destruction cycles. At p = 5 there is only 1 type-1 pair → trivial assignment moduli ((p−3)/2)! = 1! = 1.

2. **n = 3**: the unique Boolean cube dimension where the first-order Reed-Muller code RM(1, n−1) fills the entire orientation space. The equation 2^{n−1} = n + 1 has exactly one non-degenerate solution: n = 3 (giving 2² = 4 = 3+1). → trivial orientation moduli 2^{2^{n−1}−1−n} = 2⁰ = 1.

The object is an **isolated rigid point** in a doubly-exponentially growing moduli space. At (4,13): 960 orbits. At (5,29): ~6.4 × 10¹² orbits. The I Ching lives at the unique zero.

---

## The central question — RESOLVED

### What is the object?

**It is the unique complement-respecting surjection F₂³ → Z₅ with three-type coexistence, equipped with the involutory nuclear shear on F₂⁶.** Its uniqueness is a theorem, not a description. The proof decomposes into:

1. **Exact sequence** 1 → V₄ → Stab(111) → S₃ → 1: S₃ acts transitively on 6 type patterns, V₄ × Aut(Z₅) acts regularly on 16 surjections within each pattern. Combined: 96/96 = 1 orbit.

2. **The 0.5-bit is presentational**: it appears only when fixing the 互 kernel line H (external datum), breaking S₃ → Z₂. Under full symmetry, there is no binary choice.

3. **No other (n, p) has this property**: both assignment moduli and orientation moduli must vanish, requiring p = 5 AND n = 3.

### What the object includes
- F₂³ with complement involution σ: x ↦ x ⊕ 111
- Z₅ with negation involution τ: y ↦ −y
- The equivariant surjection f (unique up to symmetry)
- PG(2, F₂) organizing three non-Frame complement pairs
- The nuclear shear 互 on F₂³ × F₂³ (F₂-linear, rank 4, involutory on eventual cycles)

### What it does NOT include (frameworks tested and found empty)
- Association scheme: fails (heterogeneous fibers {2,2,2,1,1} destroy homogeneity)
- Coherent configuration: generic (28-class orbit partition for ANY function with this fiber shape)
- Walsh-Hadamard spectrum: automatic from ζ₅ arithmetic (W(000) = −1/φ determined by fiber sizes)
- F₁ geometry / branched cover / fiber bundle: descriptive but non-constraining

---

## Supporting questions — RESOLVED

### Q1: Is rigidity specific to {2, 3, 5}?
**YES.** Proven: 960 orbits at (4,13), growing doubly-exponentially. Rigidity requires both p = 5 (assignment) and n = 3 (orientation). (within_type_orbits.py)

### Q2: General rigidity criterion
**ANSWERED.** The criterion is: ((p−3)/2)! × 2^{2^{n−1}−1−n} = 1. Two independent conditions, each with a clean number-theoretic characterization. The "finite Hasse principle" is just the two-factor decomposition. (synthesis-3.md §IV)

### Q3: Cascade depth
**UNCHANGED AT n=4.** The 互 factored-basis formula generalizes cleanly (one additional shift step). Rank sequence 8→6→4→2→2. Same 4-element attractor. But 互 becomes a complete surjection invariant at (4,13) (every surjection gives a distinct T), unlike (3,5) where T is constant. (transitivity_probe.py)

### Q4: What does each prime contribute?
**ANSWERED BY THE ORBIT FORMULA.** p contributes the assignment factor ((p−3)/2)!. n (via 2) contributes the orientation factor 2^{2^{n−1}−1−n}. The two are independent. (synthesis-3.md §IV)

### Q5: The E=1 family
**FULLY CHARACTERIZED.** Type-distribution transitivity (1 orbit on Orbit-C distributions) generalizes to all E=1 members. Within-type orbit count = ((p−3)/2)! × 2^{2^{n−1}−1−n}. Only (3,5) has orbit count 1. The family is uniform in structure but (3,5) is the unique rigid point. (synthesis-3.md §IV, transitivity_probe.py)

### Q6: The role of the Fano plane
**CLARIFIED.** PG(n−2, F₂) organizes non-Frame pairs at ANY n. At n=3: 3 points (trivial). At n=4: Fano plane PG(2,F₂) with GL(3,F₂). The Fano plane's role at n=3 is that PG(1,F₂) = 3 points allows S₃ transitivity (trivial). What makes n=3 special is NOT the Fano plane but the RM(1,2) code filling the orientation space. (synthesis-3.md §VI)

---

## What's established (Phases 1–3)

### Phase 1: The (3,5) framework
- PG(2,F₂) × PG(2,F₂) + one Z₅ compass + 0.5 bits freedom
- Three lines through complement (H, P, Q) carry three coprime pairings
- 互 is a single shear on the product geometry
- P→H parity rotation → 克 amplification 1.538×
- 先天 = Fano triangle walk (predictive test)
- KW ordering outside framework (clean negative)
- Text-algebra interface: 89% residual, two narrow distributional bridges

### Phase 2: Selection and landscape
- Singleton-forcing ⟺ p > 2^(n−1) (theorem, 27 cases verified)
- (3,5) unique by triple resonance
- Selection chain 240→192→96→16→4→2 (complete)
- Hexagram Z₅ = pullback of trigram f×f (no new data at hexagram level)
- Eigenstructure: spectral gap 0.71, π(同+克+被克) = 89%, zero stride-2→stride-1 flow
- P-coset alignment exact: F(同)=1, F(克)=1/13

### Phase 3: The uniqueness theorem
- CC/AS hypothesis closed (generic orbit partition, not f-specific)
- Walsh spectrum automatic (Q(√5), W(000)=−1/φ, determined by fiber sizes)
- **Orbit C regularity**: Stab(111)×Aut(Z₅) regular on 96 surjections (proven)
- **0.5-bit is presentational**: 1 orbit under full symmetry, 2 orbits only when H fixed
- **Uniqueness theorem**: Orbits = ((p−3)/2)! × 2^{2^{n−1}−1−n} = 1 iff (n,p)=(3,5) (proven)
- **Reed-Muller connection**: kernel flips generate RM(1,n−1); fills orientation space iff 2^{n−1}=n+1 iff n=3
- **(4,13) comparison**: 960 orbits, 互 distinguishes all surjections (complete invariant at n≥4)
- **General exact sequence**: 1→(F₂)^{n−1}→Stab(1ⁿ)→GL(n−1,F₂)→1, non-Frame pairs = PG(n−2,F₂)

Full results: `synthesis-3.md` (519 lines, supersedes synthesis-1.md and synthesis-2.md).

---

## Source files (Phase 3)

| File | Content |
|------|---------|
| cc_identity.py | CC closure, Walsh spectrum, orbit computation |
| transitivity_probe.py | Orbit C regularity proof, (4,13) type structure, 互 at n=4 |
| within_type_orbits.py | Within-type orbit count, Reed-Muller connection |
| synthesis-3.md | Definitive synthesis document |
| exploration-log.md | Phase 3 iteration log (iterations 13-16) |
