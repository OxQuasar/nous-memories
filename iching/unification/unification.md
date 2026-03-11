# Unification Phase 3: The Object

## Where we are

Phase 1 answered "what is the structure at (3,5)?" — PG(2,F₂) decorated with one compass, 17 proven results.

Phase 2 answered "how is it selected?" — selection chain 240→2, eigenstructure, (n,p) landscape, singleton-forcing theorem.

Phase 3 asks: **what IS it?**

At (3,5), we have a binary substrate (F₂³), a cyclic quotient (Z₅), a distinguished involution (complement), a depth map (a shear on F₂³ × F₂³), and three lines through the involution's generator organizing the interaction. These aren't coordinates — they're structure. We've described this structure exhaustively from multiple angles. We still can't name it.

If the object has a definition, everything else follows from studying its properties at different parameters. Without it, each (n,p) is a separate investigation and we have a catalogue, not a theory.

Prior phases: `phase1-unification.md` (the (3,5) framework + I Ching mapping), `synthesis-1.md` (PG(2,F₂) results), `synthesis-2.md` (complete account including landscape + selection chain + eigenstructure).

---

## The central question

### What is the object?

What is the mathematical object that a complement-respecting surjection Z₂ⁿ → Z_p with a shear endomorphism on (Z₂ⁿ)² *is*?

PG(2,F₂) organizes the interactions but is the skeleton, not the whole object. The whole object includes the compass (Z₅ ordering, which PG(2,F₂) can't express) and the shear (which lives on the product, not the base).

**Its components:**
- A vector space F₂ⁿ with a distinguished point (complement generator, all-ones)
- A non-linear surjection onto Z_p respecting the involution x ↦ x ⊕ 1ⁿ
- A cyclic ordering on Z_p (two independent generators: stride-1, stride-2)
- An endomorphism on F₂ⁿ × F₂ⁿ (the shear — shift in both factors, one cross-coupling term)
- The projective geometry PG(n−1, F₂) organizing the lines through the distinguished point

**Candidates for what it might be:**
- A decorated projective plane — PG(n−1, F₂) + a cyclic ordering on fibers of a non-linear map
- A finite fiber bundle — base Z_p, fiber = complement pairs, structure group = V₄ (at n=3)
- An F₁ geometry object — where combinatorial and algebraic structure merge
- A "surjection geometry" — a new kind of object, defined by the interplay of F₂-linear and Z_p-cyclic structure through a complement-respecting map

**The test:** Does every singleton-forcing (n,p) produce an analogous composite? If yes, the object has a definition independent of (3,5). If (3,5) is the only point where all components cohere, the object might be irreducibly the Fano plane plus a compass — no further abstraction possible.

---

## Supporting questions

These are all subordinate to the central question. If the object is found, most answer themselves.

### Q1: Is rigidity specific to {2, 3, 5}?

At (3,5), the surjection is rigid up to 0.5 bits. At other singleton-forcing points — (4,13), (5,29), (6,61) in the E=1 family — does rigidity persist? At (4,13): 16,773,120 surjections, 2 shapes. Is the selection chain analogous to 240→2, or does it degrade?

More fundamentally: at {2,3,7} or {2,5,7}, what kind of structure appears? Do the gluing types change? Do lines through complement still organize the interactions, or does PG(3,F₂) work differently?

### Q2: General rigidity criterion

At (3,5), F₂-transversality + one compass datum produces near-complete rigidity. Is there a general criterion for when prime-indexed constraints on a finite structure are transverse — a finite Hasse principle?

The rigidity decomposes cleanly at (3,5): F₂-linear skeleton + Z₅ compass + 0.5-bit residual. Does this decomposition generalize?

### Q3: Cascade depth

At (3,5), the forced partition cascades: partition → type assignment → arrangements → pairings → dynamics. Depth = 3 (P→H→ī, spectral gap 0.71). This depends on exactly 3 lines through complement.

At n=4: PG(3,F₂) has 7 lines through complement. The P→H rotation breaks. What replaces it? Does cascade depth grow, shrink, or change character?

### Q4: What does each prime contribute?

At {2,3,5}: 2 = polarity, 3 = dimension, 5 = dynamics. Heterogeneity follows from coprimality.

Is this decomposition universal for coprime triples involving 2? At {2,3,7}, does 7 contribute "dynamics" the same way 5 does? At {2,5,7}, do the roles shift?

### Q5: The E=1 family

The points (n, 2ⁿ−3) — (3,5), (4,13), (5,29), (6,61) — share: 2 partition shapes, N_A/N_B = p−1, majority shape has three-type coexistence.

Is there a uniform description? The E=1 family sits closest to the forcing boundary — if rigidity degrades here, it degrades everywhere.

### Q6: The role of the Fano plane

PG(2,F₂) is the unique projective plane where every line has exactly 3 points. Each line through complement carries exactly one complement pair. At n=4, lines carry multiple complement pairs — the clean 1:1 correspondence (line ↔ pair ↔ prime pairing) breaks.

Is this a coincidence of small numbers, or a structural constraint? Does the object's definition require PG(2,F₂) specifically, or does it generalize to PG(n−1,F₂) with a different organizing principle?

---

## Strategy

**The (4,13) computation is the decisive empirical step.** It provides a second data point for the central question: does the object exist at (4,13)? Simultaneously tests Q1 (rigidity), Q3 (cascade depth), Q5 (E=1 family structure), and Q6 (what happens beyond the Fano plane).

If (4,13) has an analogous composite object — some PG(3,F₂)-based structure decorated with a Z₁₃ compass — then the object generalizes and has a definition. If the structure degrades into loose combinatorics, (3,5) is genuinely special and the object IS the Fano plane plus compass, irreducibly.

Q2 and Q4 are theoretical — need mathematical insight, not computation. Q6 may be answered by the central question (the Fano plane's role might be a consequence of the object's definition at n=3, not a separate fact).

---

## What's established (from phases 1–2)

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

Full results: `synthesis-2.md` (486 lines, 30+ proven results, exhaustive computations).
