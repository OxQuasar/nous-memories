# Round 2 Directive

## What Round 1 Established

The count is **~10⁴⁵** — vastly larger than "small" (< 100). The remaining threads do NOT dissolve. There IS a genuine selection principle operating beyond the four structural constraints.

The selection operates at two distinct layers:

**Layer A (Matching): mask = signature identity (p ≈ 10⁻¹⁷)**
- KW pairs each orbit using its own signature as the mask
- This is the deepest structural choice — far deeper than any ordering property
- The rule: "swap exactly the asymmetric line pairs"

**Layer B (Ordering): S=2 avoidance + Qian→Tai (p ≈ 0.0002)**
- Given orbit-paired sequences, the specific ordering avoids S=2 bridges
- S=2 ⟺ (weight-5 cross-orbit) OR (weight-4 same-orbit) bridges
- Joint with Qian→Tai endpoints: only 2/10,000 random orbit-paired sequences achieve both

The Eulerian property collapsed — it's a theorem, not a constraint. Self-loop placement is unremarkable. The investigation now focuses on **what forces the solution within these layers**.

## Round 2 Focus: Understanding What Distinguishes KW

Two threads, complementary:

### Thread 1: The mask-signature identity — algebraic necessity or design choice?

The mask = sig rule is the single deepest selection. Is it the UNIQUE self-consistent rule, or one of several valid choices?

Questions to investigate:
1. Among the 7 uniform matchings per orbit, which ones produce "nice" algebraic properties? Does mask=sig uniquely produce the even-Hamming-only pairing (Layer 1 of the synthesis)?
2. What happens to the S distribution under different uniform matchings? Does mask=sig uniquely minimize S, or is S=2 avoidance achievable with other uniform assignments?
3. The pair Hamming distance = 2 × weight(mask). Under mask=sig, single-generator orbits (O, M, I) have H=2, double-generator orbits (OM, OI, MI) have H=4, triple-generator orbits (OMI) have H=6. Is this the only assignment producing the observed weight distribution {2,4,6} for pairs?

### Thread 2: The ordering layer — conditional analysis

Given KW's specific matching (mask=sig for all orbits):
1. What fraction of orderings produce S=2-free sequences? (This is baseline_findings.md Open Question 1)
2. Among S=2-free orderings, what does the S=0/S=1 balance look like? Is 15/15 typical or extreme?
3. The generator chain dynamics (Thread E from the plan): does the kernel dressing sequence have internal structure, or is it effectively random given the Hamiltonian constraint?
4. Meta-hexagram walk (Thread C from the plan): among S=2-free orderings with the KW matching, is the KW meta-walk distinguished?
