# Round 2 Directive — Threads D, E, F (Parallel)

## What Round 1 Established

### The landscape (Thread C)
- S=2 avoidance constrains exactly **5 bits** of 32, leaving **2²⁷ ≈ 134M** valid orientations
- The constraints are local and factored: 4 equality constraints on adjacent pairs + 1 fixed value
- 6 of 11 graph-susceptible bridges were already neutralized by KW's pair assignments (a Layer 2+3 property, not Layer 4)
- Orientation is overwhelmingly a **free design choice** — not forced by bridge dynamics
- Kernel uniformity persists at this layer (p ≈ 0.06), but OMI-XOR contrast belongs to Layer 3

### The orientation itself (Threads A+B)
- Perfect inversion rule: reverse(first) = second for all 28 non-palindromic pairs, complement(first) = second for 4 palindromic pairs. Zero exceptions.
- **No single rule distinguishes "original" from "derived"** — all simple binary classifiers give exactly 14/14 on inversion pairs (algebraically forced by bit-reversal symmetry)
- The binary frame shows a **canon arc**: upper canon favors binary-high (67%), lower canon favors binary-low (62%), cumulative deviation peaks at pair 10 then reverses
- First 5 octets monotone decrease in binary-high count (4→3→2→1→0), p ≈ 0.07
- Coset structure in 5/7 orbits (p ≈ 0.23, not significant)

### The structural picture
Layer 4 has 27 free bits. No simple algebraic rule captures the orientation. The strongest signal is the **canon arc** — a position-dependent preference that reverses at the canon break. This is not a static rule but a *trajectory* property: the orientation drifts from one preference to its opposite across the sequence.

This changes the character of Round 2. We are not testing a discovered rule. We are exploring whether the orientation encodes a *flow* — a directional tendency that shows up in the position trajectory, weight dynamics, or trigram patterns.

---

## Thread D: Position Trajectory in the Factored Basis

**Agent: Analyst**

**Question:** In the factored basis (ō,m̄,ī,o,m,i), orientation swaps position coordinates (o,m,i) while leaving orbit coordinates (ō,m̄,ī) fixed. Thread A found that all binary classifiers give 14/14 on inversion pairs — there's no *static* rule. But the canon arc suggests a *sequential* pattern. Does the position trajectory through Z₂³ have sequential structure?

**Directions:**

1. **Build the full 64-step position trajectory.** For each hexagram in sequence order, extract position coordinates (L1, L2, L3). This gives a path through Z₂³ — 64 steps, visiting each of the 8 vertices exactly 8 times.

2. **Within-pair position dynamics.** For each pair, the position change is the mask (= orbit signature). The *starting position* within each pair is the orientation choice. Track starting positions across pairs within each orbit. Do the 4 starting positions in each orbit show sequential structure (monotone, alternating, etc.)?

3. **Cross-pair position dynamics.** At bridges, the position jumps from (pos of hex 2k+1) to (pos of hex 2k+2). This is the kernel dressing in position space. Track the **position trajectory at bridge boundaries**: the sequence of exit positions and entry positions. Are they correlated with each other? With the orbit trajectory?

4. **The canon arc in position space.** Thread A found binary-high (≡ L1-reading direction) favored in upper canon, reversed in lower. In position space, what does this correspond to? Is there a coordinate (o, m, or i) that flips preference at the canon break?

5. **Position coverage.** Do the 8 visits to each orbit cover all 8 positions? Is there a bias — some positions visited more than others? Compare to random S=2-free orientations.

6. **Compare to the 2²⁷ valid alternatives.** Sample 10K-50K S=2-free orientations and compute position trajectory statistics. Where does KW sit in the distribution?

**Key deliverable:** Whether the position trajectory has structure beyond what's forced by S=2 avoidance, and whether the canon arc manifests as a clean pattern in position space.

**Output:** `logoswen/iter3/position_trajectory_findings.md`

---

## Thread E: Weight and Yang Flow

**Agent: Structuralist**

**Question:** For inversion pairs, weight is preserved (reversal doesn't change Hamming weight). For complement pairs (OMI mask, orbit (0,0,0)), weight flips: w → 6-w. Orientation of complement pairs determines whether the pair goes heavy→light or light→heavy. For inversion pairs, orientation affects the weight *trajectory* only at bridges (changing which hexagram is at the boundary). What is orientation's net effect on the yang flow?

**Directions:**

1. **The complement pair contribution.** There are exactly 4 complement pairs (pairs 1, 14, 15, 31). KW's orientation: pair 1 heavy→light (6→0), pair 14 light→heavy (2→4), pair 15 light→heavy (2→4), pair 31 heavy→light (4→2). What is the total pattern? Is it structured (alternating, or related to pair position)?

2. **Weight trajectory at all 64 positions.** Plot/compute the weight sequence. Within inversion pairs, weight is constant (both hexagrams have the same weight). At bridges, weight jumps. Orientation changes *which* weight occupies each position — but for inversion pairs, the two weights are the same, so orientation is invisible to the weight trajectory for those pairs. **Critical realization: for inversion pairs, orientation does NOT affect the weight trajectory.** Only the 4 complement pairs have weight-visible orientation. Verify this.

3. **If weight is orientation-invisible for 28/32 pairs:** The weight trajectory is almost entirely determined by Layer 3 (pair ordering), not Layer 4 (orientation). The only orientation-dependent weight signal comes from the 4 complement pairs. With 4 bits and 2 already constrained by S=2 (pair 31 has o₃₁ in the {29,30} constraint group — check if pair 1, 14, 15 are constrained too). Quantify: how many complement-pair orientations are free vs forced?

4. **Bridge weight dynamics.** Even though inversion pairs preserve weight, the bridge Hamming distance depends on orientation (different exit hexagram → different bridge mask → different weight). Compute the bridge weight trajectory under KW vs random S=2-free orientations. Does KW's orientation minimize bridge weight? Maximize smoothness? Create a specific weight flow pattern?

5. **Yang drainage revisited.** The synthesis found 7/8 octets drain yang. Is this orientation-dependent? Under random S=2-free orientations, what fraction of octets drain yang? If it's always ~7/8 regardless of orientation, the finding belongs to Layer 3. If it varies, orientation contributes.

**Key deliverable:** Whether orientation has any detectable effect on weight/yang dynamics, and which effects (if any) belong specifically to Layer 4 vs being inherited from Layer 3.

**Output:** `logoswen/iter3/weight_flow_findings.md`

---

## Thread F: Trigram Orientation

**Agent: Structuralist**

**Question:** Each hexagram has lower trigram (L1-L3) and upper trigram (L4-L6). For inversion pairs (b = reverse(a)): if a has lower trigram T₁ and upper trigram T₂, then b has lower trigram reverse(T₂) and upper trigram reverse(T₁). Orientation determines which trigram configuration is presented first. Do the trigram trajectories show structure at the orientation layer?

**Directions:**

1. **Trigram swap under inversion.** For each inversion pair, record the lower and upper trigrams of both hexagrams. Verify the reversal relationship. For complement pairs, record the complementary trigram relationship.

2. **The lower trigram trajectory (64 steps).** Which trigram appears at each position? How does orientation affect it? For inversion pairs, flipping orientation swaps (lower_a, upper_a) with (reverse(upper_a), reverse(lower_a)). This is a non-trivial swap — it's not just exchanging upper and lower, it also reverses each trigram.

3. **Trigram pair frequencies.** The 64 hexagrams contain 64 lower-upper trigram pairs. Under KW's orientation, what is the distribution of the 8×8 = 64 possible (lower, upper) combinations? Under random S=2-free orientations? Is KW's distribution special?

4. **Nuclear trigrams.** Lines 2-3-4 form the lower nuclear trigram, lines 3-4-5 form the upper nuclear trigram. These share line pair (3,4) — the inner generator's domain. How do nuclear trigrams depend on orientation? For inversion pairs, flipping orientation sends (L1,L2,L3,L4,L5,L6) → (L6,L5,L4,L3,L2,L1), so nuclear lower (L2,L3,L4) → (L5,L4,L3) = reverse(nuclear upper). The nuclear trigrams swap-and-reverse under orientation flip. Is there a pattern?

5. **Trigram balance.** Each of the 8 trigrams should appear 8 times as lower and 8 times as upper (forced by the permutation). Under KW's orientation, is this exactly satisfied? Under orientation changes, how does the per-position trigram distribution shift?

6. **Sequential trigram patterns.** The lower trigram trajectory (pair by pair, 32 values for the first hexagram of each pair). Does it repeat, cycle, or show any pattern? Compare to random.

**Key deliverable:** Whether trigram-level patterns distinguish KW's orientation from random S=2-free alternatives, and whether the "original first" convention corresponds to a trigram-level preference.

**Output:** `logoswen/iter3/trigram_findings.md`

---

## Convergence Notes for Round 2

The three threads explore different faces of the same 27-bit freedom:

- **D** (position trajectory): the algebraic face — orientation as a path through Z₂³
- **E** (weight flow): the dynamical face — orientation as yang distribution  
- **F** (trigrams): the traditional face — orientation as trigram presentation order

Thread E may produce a quick null: if weight is truly orientation-invisible for 28/32 pairs, the weight story collapses to 4 complement pairs. This is a useful result — it means weight dynamics belong to Layer 3, not Layer 4. Thread E should verify this quickly, then pivot to bridge weight dynamics if the complement-pair analysis terminates early.

The canon arc (from Thread A) is the main signal to pursue. Thread D is best positioned to explain it — the arc is likely a position-space phenomenon (L1 preference flipping at the canon break). Thread F may find the trigram-level expression of the same arc.

## Code Infrastructure

Same as Round 1 plus:
- Round 1 scripts in `logoswen/iter3/` (thread_a_census.py etc.) — can import data structures
- `logoswen/iter3/census_findings.md` and `bridge_orientation_findings.md` — reference findings
- The S=2-free sampling method from `orientation_enumeration.py` — reuse for null models
- New scripts and findings to `logoswen/iter3/`
