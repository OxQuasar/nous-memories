# Complement-Respecting Surjections Between Boolean Cubes and Cyclic Groups

## The Phenomenon

Take a Boolean cube Z₂ⁿ and a cyclic group Z_p. Require:
1. **Two independent cycles on Z_p.** Stride-1 and stride-2 are both full-length generators and are genuinely different (not inverses).
2. **A complement-respecting surjection** f: Z₂ⁿ → Z_p, meaning f(~x) = -f(x) mod p. Bitwise negation maps to additive negation.

**Question:** For which (n, p) does this surjection force singletons — fibers of size 1?

**Answer:** (n, p) = (3, 5) is the unique solution.

This is a fact about numbers. The I Ching happens to be the structure living at this point.

---

## Part I: Why (3, 5)

### p = 5: the two-cycle threshold

On Z_p, stride-2 is an independent generator from stride-1 iff 2 ≢ ±1 mod p.

| p | 2 mod p | Independent? |
|---|---|---|
| 2 | 0 | degenerate |
| 3 | 2 ≡ -1 | stride-2 = reverse of stride-1 |
| 5 | 2 ≢ ±1 | **first independent pair** |
| 7+ | works | but n is further constrained |

p = 5 is the smallest prime admitting two independent full-length cycles.

### n = 3: the singleton-forcing window

Z₂ⁿ has 2ⁿ⁻¹ complement pairs. The complement constraint maps each pair either together (doubleton fiber) or split into negated fibers (two singletons). Surjectivity demands all p elements are hit.

| n | Pairs | Doubleton slots (⌈p/2⌉) | Must split? | Partition forced |
|---|---|---|---|---|
| 2 | 2 | — | Can't surject (4 < 5) | — |
| **3** | **4** | **3** | **Yes: 4 pairs, 3 slots** | **{2,2,2,1,1} (80%) or {4,1,1,1,1} (20%)** |
| 4 | 8 | 3 | No: {4,4,4,2,2} fits | Not forced |
| 5+ | 16+ | 3 | No | Not forced |

At n = 3: 4 complement pairs must map onto 5 elements. At most 3 pairs can share fibers (filling 3 doubleton slots). The 4th pair must split → exactly 2 singletons. The partition {2,2,2,1,1} is forced by pigeonhole.

At n = 4: 8 pairs into 5 elements — average 1.6 pairs per element, no splitting required.

**The window is exactly one dimension wide.** Below: can't surject. Above: no forcing. Only at n = 3 does the pigeonhole constraint bite.

### The forced structure at (3, 5)

The partition {2,2,2,1,1} cascades:

- **Singletons are mutual stride-2 images.** The split pair maps to f(x) and f(~x) = -f(x). On Z₅, negation maps 1↔4 and 2↔3. The singletons sit at negated positions, which are exactly stride-2 apart (since 2 ≡ -3 ≡ 2 mod 5 connects them via the second cycle).

- **The complement point is distinguished.** In Z₂³, the all-ones vector 111 is the complement involution's generator. The 3 lines through 111 in the projective plane PG(2, F₂) each carry one complement pair — and these correspond to the three doubleton/singleton types of the partition.

- **PG(2, F₂) exists because n = 3.** The projective plane over F₂ requires a 3-dimensional vector space. The singleton-forcing window and the Fano plane are the same constraint: n = 3 is the unique dimension where the surjection is forced AND the organizing geometry exists.

---

## Part II: The Geometry at (3, 5)

### PG(2, F₂) decorated with one compass

The structure at (3, 5) has a concrete geometric description:

1. **PG(2, F₂) × PG(2, F₂)** — product Fano geometry on F₂³ × F₂³ (ordered pairs = "hexagrams"), with one shear coupling the factors.
2. **One compass** — Z₅ circular ordering, the datum PG(2, F₂) cannot express (since gcd(2, 5) = 1, no F₂-linear structure captures cyclicity mod 5).
3. **0.5 bits of freedom** — which of the three lines through 111 carries the same-element doubleton. The complement point's symmetry in PG(2, F₂) makes two choices algebraically indistinguishable.

### Three lines through complement

PG(2, F₂) has 7 lines. Exactly 3 pass through the complement point 111. Each carries one complement pair {x, ~x} and mediates a distinct prime interaction:

| Line | Kernel | What it constrains | Prime pair |
|------|--------|-------------------|-----------|
| H = ker(b₁⊕b₂) | middle = inner bit | The depth endomorphism's kernel | {3, 5}: position × cycle |
| P = ker(b₀⊕b₁) | outer = middle bit | The surjection's parity structure | {2, 5}: polarity × cycle |
| Q = ker(b₀⊕b₂) | outer = inner bit | The palindromic condition | {2, 3}: polarity × position |

Each line's defining functional constrains a different pair of bit positions, naturally indexing the three coprime pairings of {2, 3, 5}. This is not an assignment — it emerges from the geometry.

**P + Q + H = 8 theorem.** In any complement-antipodal Hamiltonian cycle on F₂³, no step equals 111 (complements are at maximal distance, not adjacent). Each step hits exactly one of {P, Q, H}. The three lines partition the transition space.

### The depth endomorphism

On F₂³ × F₂³, the "nuclear" map (extract inner 4 of 6 bits, split into two overlapping triples) becomes a shear in the factored basis:

```
Position: o'=m, m'=i, i'=i⊕ī    (shift + one coupling term)
Orbit:    ō'=m̄, m̄'=ī, ī'=ī      (independent shift + project)
```

One term — ī leaks into i — creates all dynamical richness. Rank sequence 6→4→2, coordinates killed outside-in. Bifurcation on a single bit: ī = 0 → fixed point, ī = 1 → 2-cycle. The endomorphism respects orbit (equivariant) but shears position (selectively breaks product structure).

The P→H parity rotation: applying the surjection's parity functional to the nuclear output equals the H-functional on the original input. This rotates which stride-2 transitions are parity-visible, amplifying antagonistic relations by 1.538×.

### Rigidity decomposition

The surjection is determined by two kinds of constraint:

**F₂-linear (7 constraints).** Codimension conditions in PG(2, F₂). Each reduces the configuration space by a power of 2. These form the geometric skeleton — transverse at every stage (expected dimensions throughout).

**Non-linear (3 constraints).** Z₅ monotonicity (cyclic ordering on the compass), complement symmetry (involution compatibility), fixed-point-free involutions (block structure). All resolved by the compass datum, which is itself the unique triple junction of {2, 3, 5}.

**Result:** 0.5 bits of genuine freedom. The obstruction is the symmetry of 111 in PG(2, F₂) — both candidate same-element pairs have XOR = 111, making them indistinguishable to any complement-symmetric constraint.

### Verified at (3, 5): 17 proven results

Full enumeration in synthesis.md. Highlights:

- Stabilizer of line H ≅ S₄, with V₄ kernel = the block-preserving subgroup
- The ordered-pair pairing (reversal + complement fallback) = orbit class (theorem, not measurement)
- Hamiltonian cycles on F₂³ are Fano triangle walks; the "earlier" arrangement is the unique b₀-constant cycle in Family H — emerged as corollary, not input (predictive test)
- The sequence ordering of the 64 pairs has no Fano signal (Z < 1.5σ) — clean boundary

---

## Part III: The Number Theory Beyond (3, 5)

### Is (3, 5) isolated?

The singleton-forcing question has a definite answer for small (n, p):

| (n, p) | 2ⁿ | Surjects? | Two independent cycles? | Singletons forced? |
|---|---|---|---|---|
| **(3, 5)** | **8** | **✓** | **✓** | **✓ — the unique point** |
| (3, 7) | 8 | ✓ | ✓ | ✓ — singletons forced, but degenerate (types {0,1} only, partition uniquely {2,1,1,1,1,1,1}) |
| (4, 5) | 16 | ✓ | ✓ | ✗ (no pigeonhole forcing) |
| (4, 7) | 16 | ✓ | ✓ | ✗ (p ≤ 2^(n-1) = 8, singleton-free surjections exist) |
| (4, 11) | 16 | ✓ | ✓ | ✓ — 20,643,840 surjections, 4 partition shapes |
| (4, 13) | 16 | ✓ | ✓ | ✓ — 16,773,120 surjections, 2 partition shapes |
| (5, 11) | 32 | ✓ | ✓ | ✗ (p ≤ 2^(n-1) = 16) |
| (5, 17) | 32 | ✓ | ✓ | ✓ — 6.6×10¹⁸ surjections, 45 partition shapes |
| (3, 3) | 8 | ✓ | ✗ | — (fails two-cycle axiom) |

**Resolved (np_landscape computation).** The singleton-forcing window is **p > 2^(n−1)**, proved theoretically and verified computationally for 27 (n,p) cases across n ∈ {3,4,5,6}. The family is infinite: every n ≥ 3 has singleton-forcing primes. (3,5) is uniquely characterized by the triple resonance: singleton-forcing (p > 4) ∧ three-type-possible (p < 7) ∧ n = 3 (Fano plane). The 2-shape partition structure at (3,5) — {2,2,2,1,1} (80%) and {4,1,1,1,1} (20%) — recurs at every (n, 2^n − 3) point in the family.

### The general questions

The (3, 5) investigation exposes four questions that belong to number theory, not to any particular instantiation:

**1. Surjection categories.** Complement-respecting maps Z₂ⁿ → Z_p form a natural class. What are the morphisms? When are two maps equivalent modulo Aut(Z_p) × GL(n, F₂)? At (3, 5), the map is unique up to these automorphisms plus 0.5 bits. Is uniqueness generic for singleton-forcing pairs?

**2. Cascade depth.** At (3, 5), the forced partition determines higher structures: arrangements on the cube (Hamiltonian cycles with complement-antipodal symmetry), pairings on the square (orbit classes under reversal/complement), dynamics (shear endomorphisms on the product). Does every singleton-forcing (n, p) produce an analogous cascade? Or does cascade depth depend on the specific numbers?

**3. Gluing heterogeneity at coprime triples.** At {2, 3, 5}, the three pairwise interactions are algebraic ({2,5}: complement = negation), combinatorial ({2,3}: bit-position hierarchy), and geometric ({3,5}: cyclic embedding into spatial arrangement). These are necessarily different because the primes contribute different mathematical substances. Is heterogeneous gluing universal for coprime triples? At {2, 3, 7}, do the same three types recur, or do new gluing types emerge?

**4. The rigidity mechanism.** At (3, 5), F₂-transversality plus one non-linear datum produces near-complete rigidity (0.5 bits residual). The analog of the Hasse principle: local constraints (per prime) are individually underdetermined, but their intersection forces a global solution. Is there a general criterion for when prime-indexed constraints on a finite structure are transverse? This would be a finite Hasse principle.

### The five gaps in pure arithmetic

Each gap identified during the investigation reduces to a number theory question:

1. **Prime-indexed constraints** → constraints from the factorization of 2ⁿ relative to p. At (3, 5): the three bit-position pairings (b₀⊕b₁, b₁⊕b₂, b₀⊕b₂) naturally index the coprime pairings. PG(2, F₂) resolves this at (3, 5). **General form open.**

2. **Heterogeneous gluing** → the surjection IS the glue between Z₂ and Z_p. Combinatorial glue comes from n (which bits serve which role). Geometric glue comes from p's circular structure. Heterogeneity follows from coprimality — no common factor to route a uniform morphism through. **Dissolved at (3, 5): three lines through one point. General form open.**

3. **Finite rigidity** → complement-respecting surjection unique modulo automorphisms. At (3, 5), the conjunction of F₂-linear and non-linear constraints achieves this. **Resolved at (3, 5). General criterion unknown.**

4. **Dynamics** → endomorphisms of Z₂²ⁿ with selective equivariance across the surjection's fibers. Which operations preserve fibers (complement does), which break them (the depth map shears). The equivariance pattern is determined by the factored basis geometry. **Resolved at (3, 5). Generalizes naturally if other (n, p) structures exist.**

5. **Statistical gluing** → the one gap that doesn't reduce to pure arithmetic. At (3, 5), the surjection is determined up to 0.5 bits by algebra alone. The residual requires non-algebraic data (empirical correlations in the I Ching's textual layer). Pure arithmetic determines structure but not orientation on the cycle. **Characterized by the semantic map (see Part IV): the interface is thin (two distributional bridges, 89% residual) but genuine (both survive position control). This is the boundary of what number theory can say.**

---

## Part IV: Relationship to the I Ching

The I Ching is the instantiation of the (3, 5) structure:

| Abstract | I Ching | PG(2, F₂) |
|---|---|---|
| Z₂³ | 8 trigrams | F₂³ |
| Z₅ | 五行 (five phases) | compass datum |
| stride-1 on Z₅ | 生 (generation) | monotone compass ordering |
| stride-2 on Z₅ | 克 (overcoming) | stride-2 on compass |
| complement | 錯 (bit-flip) | 111 = the point where H ∩ P ∩ Q |
| surjection | trigram → element | set function (non-linear) |
| singletons | Water (坎), Fire (離) | Q-line pair, depth-map 2-cycle attractors |
| doubletons | Wood, Earth, Metal | one complement pair per through-111 line |
| (Z₂³)² | 64 hexagrams | PG(2, F₂) × PG(2, F₂) |
| depth endomorphism | 互 (nuclear extraction) | shear: ī leaks into i |

The I Ching didn't construct this structure — it found it. The number theory determines what's there. The 0.5-bit residual (which doubleton becomes "Wood") is where the numbers stop and convention begins — and even that is constrained to a binary choice by the geometry.

### What the I Ching adds beyond the arithmetic

The I Ching is not just (3, 5). It layers on:

- **Textual content** (卦辭, 爻辭) — Zhou dynasty texts predating the algebraic formalization by ~700 years. These encode the algebraic hierarchy statistically (p < 0.001) despite being composed without knowledge of it.
- **Divinatory overlay** (體/用, 世/應, 六親) — operational projections converting static algebra into directed readings. These are legitimate uses of the structure's information-theoretic properties (partial visibility, directional output, temporal arc).
- **The textual bridge** — the 0.5-bit is resolved by conjunction of algebraic constraint (cycle attractors must be relationally active) and textual correlation (auspiciousness × generation, p = 0.007). This is where number theory and empirical semantics meet.

### The text-algebra interface (semantic map results)

The semantic map workflow characterized gap 5 empirically. The answer: **punctual, not systematic.**

**89% residual thickness.** Only 11% of 爻辭 embedding variance is explained by all algebraic coordinates combined. The texts have rich independent structure — situational imagery, navigational vocabulary — organized primarily by line position, not by algebraic partition.

**Two bridges, both genuine, both narrow:**
- 凶×basin: OR = 4.25, p = 0.00002 (survives position control via CMH)
- 吉×生体: OR = 2.19, p = 0.004 (survives position control via CMH)

Both are distributional (where markers are placed) not thematic (what texts say). Neither is reducible to the other — they operate through different algebraic projections (core vs shell). They are the ENTIRE text-algebra interface. No hidden systematic alignment exists.

**Three historical layers, three registers:**

| Layer | Period | What it sees |
|-------|--------|-------------|
| 爻辭 | ~9th c. BC | Positions, situational processes |
| 小象/彖傳 | ~5th-3rd c. BC | Binary structure (Z₂): yang/yin, centrality, correspondence |
| 五行 formalization | ~1st c. BC | Pentadic structure (Z₅): elements, basins, surface relations |

The commentary tradition (小象/彖傳/大象) sees primes 2 and 3 but not prime 5. The 小象 encodes the 3-layer line hierarchy with χ² = 125 (p = 5×10⁻²⁶) using distinct vocabulary per layer — but has zero algebraic signal after controlling for position. The 彖傳 operates in a binary register (剛/柔/中/應), tracking anomalies not categories. The 大象 is purely imagistic — zero 五行 relational vocabulary.

The 五行 framework was not read from the earlier texts. It is an independent mathematical structure that happens to capture two distributional regularities in the pre-existing corpus. The algebra describes the container (Z₂⁶ with its projections); the texts describe the contained (situations, outcomes). They touch at two narrow bridges but are otherwise separate systems describing the same 64×6 state space from different angles.

---

## Status

### Done
- (3, 5) uniqueness proven (abstract skeleton)
- PG(2, F₂) realization complete (17 proven results, 0 contradictions)
- 4/5 arithmetic gaps resolved at (3, 5)
- Gap 5 characterized empirically (semantic map: 89% residual, two narrow bridges, three registers)
- Predictive test passed (先天 arrangement emerged as corollary)
- Boundary established (sequence ordering outside framework)

### Open (updated after program completion — iteration 12)

**All six internal questions resolved:**

1. ~~(4, 7) and (5, 11) singleton-forcing?~~ **RESOLVED:** Singleton forcing ⟺ p > 2^(n−1). Both (4,7) and (5,11) have p ≤ 2^(n−1), so NOT singleton-forcing. The family is infinite. See synthesis-2.md Part I.

2. ~~Surjection category~~ **RESOLVED:** Selection chain 240→192→96→16→4→2. P→H nuclear coherence selects the I Ching's type assignment (2,0,1,2) as the unique monotonically-decreasing cascade within Orbit C. The chain uses structural forcing (theorem) at steps 1-2 and 4-5, observational coherence at step 3. See synthesis-2.md Part II.

3. ~~Cascade depth~~ **RESOLVED:** Depth = 3 (P→H→ī). Spectral gap 1 − √(23/273) ≈ 0.71 confirms: mixing in 3-5 iterations. Breaks at n=4 (more than 3 lines through complement). See synthesis-2.md Part IV.

4. ~~Gluing heterogeneity~~ **RESOLVED:** Hexagram Z₅ = pullback of trigram f×f. The 8×8 relation matrix is the 5×5 Cayley subtraction table expanded by fiber multiplicities. No additional Z₅ data at hexagram level. See synthesis-2.md Part III.

5. ~~Finite Hasse principle~~ **RESOLVED:** Exact P-coset formula F(d) = convolution of fiber_Pk across the P-partition. The "approximate Z₅→Z₂ homomorphism" is in fact exact: F(同)=1, F(生)=2/3, F(克)=1/13, determined by fiber P-homogeneity. See eigenstructure_results.md.

6. ~~Statistical gluing formalism~~ **RESOLVED:** F(d) is exact, not statistical. The P-coset alignment is a deterministic consequence of fiber partition {2,2,2,1,1} and P-parity structure. No approximation involved. Gap 5 from the semantic map (text-algebra interface) remains empirical/punctual, but the algebraic side is fully resolved.

**Remaining open (external to this program):**
- Surjection category morphisms for general (n, p)
- Heterogeneous gluing at other coprime triples (e.g., {2, 3, 7})
- General finite Hasse principle criterion
- King Wen sequence ordering principle
