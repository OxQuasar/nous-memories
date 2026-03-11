# The Arithmetic Skeleton

The I Ching's algebraic structure is an instantiation of a pure number-theoretic phenomenon. This document strips away the interpretive content and states the naked arithmetic.

---

## The Abstract Problem

Given:
- A Boolean cube Z₂ⁿ
- A prime-order cyclic group Z_p admitting two independent non-degenerate cycles (stride-1 and stride-2 are both full-length generators)
- A surjection f: Z₂ⁿ → Z_p respecting complement (bitwise negation maps to additive negation: f(~x) = -f(x) mod p)

**Question:** For which (n, p) does this surjection force singletons (fibers of size 1)?

**Answer:** (n, p) = (3, 5) is the unique solution.

---

## Why (3, 5) Is Unique

### p = 5 is forced by the two-cycle requirement

On Z_p, stride-1 and stride-2 are both full cycles iff p is prime and stride-2 ≢ ±stride-1 mod p.

| p | stride-2 mod p | Independent? | Viable? |
|---|---|---|---|
| 2 | 0 | degenerate | No |
| 3 | -1 mod 3 | stride-2 = reverse of stride-1 | No |
| 4 | 2 has period 2 | degenerate (only visits half) | No |
| **5** | **2 ≢ ±1 mod 5** | **genuinely independent** | **Yes** |
| 7+ | works | but 2ⁿ must be ≥ p for surjection | Constrained |

p = 5 is the smallest prime where two independent full-length cycles coexist.

### n = 3 is forced by the singleton-forcing window

Z₂ⁿ has 2ⁿ elements forming 2ⁿ⁻¹ complement pairs. The complement-respecting surjection maps each pair either:
- **Together** → both into the same fiber (doubleton contribution)
- **Split** → into negated fibers f(x) and -f(x) (two singleton contributions)

Pigeonhole on 2ⁿ⁻¹ pairs into ⌈p/2⌉ available doubleton slots:

| n | 2ⁿ | Pairs | Doubleton slots for p=5 | Forced splits | Singletons | Surjects? |
|---|---|---|---|---|---|---|
| 2 | 4 | 2 | 2 | 0 | 0 | No — can't cover 5 elements with 4 trigrams |
| **3** | **8** | **4** | **3** | **≥1** | **≥2** | **Yes — forces exactly {2,2,2,1,1}** |
| 4 | 16 | 8 | 3 | ≥5 | ≥10 | Yes but singletons not forced — 8 pairs fit into 5 buckets without splitting |
| 5 | 32 | 16 | 3 | — | — | Same — no forcing |

Wait — the n=4 case needs more care. At n=4, 8 complement pairs into 5 elements. Each element can absorb up to ⌊8/5⌋ = 1-2 pairs. With 8 pairs and 5 elements, the average is 1.6 pairs per element. You CAN fit all 8 pairs without splitting any: give 2 pairs to 3 elements and 1 pair to 2 elements → {4,4,4,2,2}. No singletons. No singleton-forcing.

At n=3: 4 complement pairs into 5 elements. You can pair at most 3 (one per doubleton slot — each paired slot absorbs one complement pair, contributing 2 elements). 3 paired slots × 2 = 6 elements assigned. 2 elements remain, each needing at least 1 trigram for surjectivity. Only 2 trigrams remain (the 4th complement pair, split). Each singleton gets one. Forced.

**2³ is the unique power of 2 in the singleton-forcing window for Z₅.** One dimension lower (2²=4) can't surject. One dimension higher (2⁴=16) has enough pairs to avoid splitting. The window is exactly one dimension wide.

### The partition is forced

At (3, 5): 4 complement pairs, 3 absorbed as doubletons, 1 split into singletons.

Partition: {2, 2, 2, 1, 1}. Three doubleton elements, two singleton elements. No other partition shape satisfies complement-respecting surjection at these parameters.

---

## What Falls Out

From (n, p) = (3, 5) and the complement-respecting surjection, the following cascade:

| Level | What's determined | How |
|---|---|---|
| 5 elements | Z₅ with 生(stride-1) and 克(stride-2) | Axiom 1 |
| 3 lines per trigram | dimension of Z₂ⁿ | Singleton forcing at p=5 |
| 8 trigrams | 2³ | From n=3 |
| 64 hexagrams | 8² (ordered pairs of trigrams) | Standard construction |
| {2,2,2,1,1} partition | Forced by pigeonhole | 4 pairs, 5 targets, complement constraint |
| 2 singletons | The split pair | Pigeonhole remainder |
| Singletons = mutual 克 | Negation maps singletons to each other; stride-2 = 克 | f(~x) = -f(x), and the split pair occupies negated positions on Z₅ |
| Complement = negation | By construction | Axiom 2 |
| Zero free parameters | Conjunction of algebraic + statistical constraints | The 0.50-bit choice forced by singleton-attractor mechanism + textual bridge |

---

## The Generalization

The I Ching is case study #1 of this phenomenon. The abstract question is:

**For which primes p and dimensions n does a complement-respecting surjection Z₂ⁿ → Z_p with two independent cycles on Z_p produce a rigid structure?**

The analysis shows (3, 5) is the unique solution in the "interesting" range. But the framework generalizes:

### Other (n, p) pairs to investigate

| (n, p) | 2ⁿ | Surjects? | Two cycles? | Singletons forced? | Status |
|---|---|---|---|---|---|
| (3, 5) | 8 | ✓ | ✓ | ✓ | **The I Ching** |
| (3, 7) | 8 | ✓ | ✓ | ✗ (8/7 ≈ 1.14, all near-singletons) | Degenerate — almost injective |
| (4, 5) | 16 | ✓ | ✓ | ✗ | No singleton forcing |
| (5, 5) | 32 | ✓ | ✓ | ✗ | Same |
| (3, 3) | 8 | ✓ | ✗ (cycles collapse) | — | Fails axiom 1 |
| (2, 3) | 4 | ✓ | ✗ | — | Fails axiom 1 |
| (4, 7) | 16 | ✓ | ✓ | Possibly | Unexplored |
| (5, 11) | 32 | ✓ | ✓ | Possibly | Unexplored |

The question for a general theory: is there a family of (n, p) pairs producing rigid structures, or is (3, 5) genuinely isolated? If isolated, the I Ching sits at the unique point. If part of a family, there are "I Ching-like" systems at other parameters.

### What a framework would formalize

1. **The surjection type:** complement-respecting maps Z₂ⁿ → Z_p as a category. Morphisms between them. When are two such maps equivalent?

2. **The rigidity criterion:** conditions on (n, p) guaranteeing the map is unique (up to automorphisms of Z_p). At (3, 5), the conjunction of algebraic and statistical constraints yields uniqueness. Is this generic or special?

3. **The cascade:** how the surjection's properties (partition shape, singleton positions) determine higher-level structures (arrangements, pairings, dynamics). The derivation tree from the deep workflow. Does it generalize — does every rigid (n, p) pair produce an analogous cascade?

4. **The gluing heterogeneity:** the three prime pairs require different constraint types (algebraic, combinatorial, geometric). Is this always the case for coprime triples, or is it special to {2, 3, 5}?

---

## Relationship to the I Ching Instance

Everything in the I Ching's algebraic structure is a concretization of the abstract arithmetic:

| Abstract | I Ching |
|---|---|
| Z₂³ | 8 trigrams |
| Z₅ | 5 elements (五行) |
| stride-1 on Z₅ | 生 (generation cycle) |
| stride-2 on Z₅ | 克 (overcoming cycle) |
| complement-respecting surjection | trigram → element assignment |
| singletons | Fire (離) and Water (坎) |
| doubleton fibers | Wood {震,巽}, Earth {坤,艮}, Metal {乾,兌} |
| (Z₂³)² = Z₂⁶ | 64 hexagrams |
| endomorphism on inner 4 bits | 互 (nuclear extraction) |
| single-bit flip | 變 (line change) |
| Z₅ × Z₅ quotient | the torus (element pair coordinates) |
| cyclic strength assignment | seasonal overlay (旺相休囚死) |

The I Ching is the unique instantiation. The arithmetic is the skeleton. A unification framework should formalize the skeleton, then recover the I Ching as the (3, 5) case.

---

## What This Changes for the Unification Program

The five gaps identified in `toward-unification.md` are framed around the I Ching instance. Reframed around the arithmetic:

1. **Prime-indexed constraints** → constraints arising from the factorization of 2ⁿ relative to p. The prime indexing is intrinsic to the number theory, not imposed.

2. **Heterogeneous gluing** → the surjection itself IS the glue between Z₂ and Z₅. The combinatorial glue (position) arises from n=3 (which bits serve which role). The geometric glue (arrangement) arises from embedding the cycles into spatial structure. The heterogeneity follows from the three primes being coprime — there's no common factor through which to route a uniform morphism.

3. **Finite rigidity criterion** → at (3, 5), the complement-respecting surjection is unique (modulo automorphisms). Is this a general phenomenon for singleton-forcing (n, p) pairs, or specific to (3, 5)?

4. **Dynamics** → endomorphisms of Z₂⁶ that respect the surjection partially (complement commutes, 互 doesn't). The equivariance pattern is determined by which Z₂ⁿ operations preserve fibers and which break them.

5. **Statistical gluing** → the one gap that doesn't reduce to pure arithmetic. The textual bridge (吉×生体, p=0.007) connects the number theory to empirical semantics. This is where the I Ching instance goes beyond the skeleton — the skeleton determines the structure, but the textual constraint is needed to fix the orientation (which fiber becomes which element on the 生 cycle). Pure arithmetic leaves a residual symmetry that only empirical data breaks.
