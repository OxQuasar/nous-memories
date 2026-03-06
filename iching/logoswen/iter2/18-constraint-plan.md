# 18. Constraint Depth and Statistical Significance — Research Plan

> The bridge deep analysis (16/17) established three theorems: the short exact sequence Z₂⁶ ≅ Z₂³ × Z₂³, the Eulerian path from Qian(000) to Tai(111), and the quantization H = w + 2S. The question shifts from "what structure exists?" to "how much of this structure is forced vs chosen?"

---

## Thread A: Sequence Enumeration (Critical)

**Question:** How many valid King Wen-type sequences exist?

A valid sequence satisfies ALL of:
1. **Hamiltonian**: visits all 64 hexagrams exactly once
2. **Paired**: hexagrams occur in 32 pairs, each pair using the orbit-determined mask
3. **Eulerian**: the 31 bridges form an Eulerian path through the orbit multigraph
4. **Endpoint**: starts in orbit Qian(000), ends in orbit Tai(111)

If the count is O(1), the KW sequence is essentially forced — all remaining "choices" are illusions of the constraint closure. If O(10³+), there's a genuine selection principle we haven't found.

**Approach:** Direct enumeration is infeasible (64! space). Decompose using the factored structure:

1. **Enumerate Eulerian paths** through the orbit multigraph (≥100 exist, probably ~10³-10⁴). This fixes the orbit visit order.
2. **For each Eulerian path, enumerate pair-slot assignments.** Each orbit has 4 pairs (4 pair-slots). The Eulerian path visits each orbit 4 times. Assignment = which pair-slot to use at each visit. 4!⁸ ≈ 10¹² total — too large for brute force, but massively pruned by bridge constraints (each bridge connects specific hexagrams, constraining which pair-slots can follow which).
3. **For each pair-slot assignment, check hexagram-level validity.** Each pair-slot has 2 orientations (which hexagram comes first). Check that the 64-hex sequence is a valid path.

Estimate: with aggressive pruning, this may be tractable for sampling even if not for exact count.

**Fallback:** If exact enumeration is infeasible, use Monte Carlo sampling:
- Sample random Eulerian paths
- For each, greedily assign pair-slots with backtracking
- Estimate the density of valid completions
- Determine confidence interval on total count

**Output:** Count (or estimate + confidence) of valid sequences. Distribution of properties (S-distribution, self-loop positions, opening length) across the valid set.

---

## Thread B: Random Baseline

**Question:** How special is the KW sequence compared to random?

Three null models, increasing constraint:

**B1. Random Hamiltonian path through {0,1}⁶.** Generate random Hamiltonian paths on the 6-cube. For each:
- Pair consecutive hexagrams: is each pair orbit-consistent (uses orbit-determined mask)?
- Compute bridge orbit transitions: is the walk Eulerian?
- Compute S distribution, Hamming excess, weight-5 gap presence

**B2. Random orbit-paired Hamiltonian path.** Fix the constraint that pairs use orbit-determined masks (partition the 64 hexagrams into 32 orbit-consistent pairs first, then find Hamiltonian orderings). For each:
- Is the bridge walk Eulerian?
- What's the S distribution?

**B3. Random Eulerian-consistent sequence.** Start from a random Eulerian path through the orbit graph, then try to build a valid Hamiltonian hexagram sequence. Compare properties to KW.

For each null model, compute:
- P(Eulerian | Hamiltonian + paired)
- Expected S distribution
- Expected self-loop count and placement
- Expected Hamiltonian prefix length (new orbits before first revisit)

**Method:** Sampling. Hamiltonian paths on the 6-cube can be generated via random walks with backtracking (the 6-cube is small enough). Need ~10⁴ samples per null model for stable statistics.

**Output:** p-values for each KW property under each null model. Which properties are "free" (common under null) vs "remarkable" (rare under null)?

---

## Thread C: Meta-Hexagram Walk Structure

**Question:** The Eulerian orbit walk generates a specific walk through meta-hexagram space. What's its structure?

From 13-meta: stacking adjacent pair signatures produces meta-hexagrams. The bridge's orbit change Δsig feeds directly into this. The kernel dressing is invisible to meta-hexagrams — they see only the antisymmetric component (im(P)).

Now that we know the orbit walk is Eulerian:
- The meta-hexagram walk is a deterministic function of the Eulerian path
- Different Eulerian paths generate different meta-walks
- Is the KW meta-walk special among all possible meta-walks from valid Eulerian paths?

**Method:**
1. For all enumerated Eulerian paths (from Thread A), compute the induced meta-hexagram sequence
2. For each meta-walk: which hexagrams appear? How many unique? Any repeating patterns?
3. Compute meta-signatures and check the cross-generator decomposition from 13-meta
4. Is the KW meta-walk's property (26/31 unique, #38 Kui appearing 3×) typical or atypical?

**Output:** Distribution of meta-walk properties across all valid Eulerian paths. Whether the KW meta-walk is distinguished.

---

## Thread D: Self-Loop and Boundary Forcing

**Question:** Are the two self-transition positions (B14 at the canon boundary, B19 at mid-lower-canon) forced by the Eulerian constraint?

Self-loops in the orbit multigraph: Qian has 1 self-loop, WWang has 1 self-loop. In any Eulerian path, these must be used exactly once each. But WHEN in the walk they occur is a choice.

- Across all valid Eulerian paths, where do self-loops appear?
- Is there a position that's more common? Are positions 14 and 19 special?
- Does the Hamiltonian constraint further restrict self-loop placement?
- B14 uses kernel=I (minimal dressing), B19 uses kernel=OMI (maximal). Is this forced?

**Method:**
1. From enumerated Eulerian paths, record self-loop positions
2. Distribution of Qian self-loop position, WWang self-loop position
3. For valid complete sequences (from Thread A), check if self-loop positions are further constrained

**Output:** Whether B14 and B19 positions are forced, typical, or rare.

---

## Thread E: Generator Chain Dynamics

**Question:** The kernel dressing sequence lives in Z₂³. Does it have its own structure?

The 31 kernel dressings form a path through the 8 elements of ⟨O,M,I⟩. This path is:
```
id → O → OMI → O → OMI → id → OI → M → O → MI → id → OMI → id → I → OM → OM → O → OM → OMI → OI → OI → O → MI → I → O → M → id → MI → OI → O → MI
```

Analyze:
- Autocorrelation at each lag (XOR of consecutive dressings)
- Return times (gap between consecutive uses of same dressing)
- Does this sequence have its own walk structure in Z₂³?
- The XOR of consecutive kernel dressings — is this sequence structured?
- Spectral analysis (DFT of the 31-element binary sequence, treating each component separately)
- Comparison to the kernel sequences from other valid complete sequences (Thread A)

**Output:** Whether the kernel chain has internal structure or is effectively random given constraints.

---

## Thread F: Fu Xi Comparison

**Question:** Does the Fu Xi (binary) ordering have any of these properties?

Fu Xi orders hexagrams by their binary value (0-63). This is the natural "computer science" ordering. Apply the complete analysis pipeline:
- Pair by adjacency (0-1, 2-3, ...) and compute pair masks
- Compute orbit signatures and bridge transitions
- Check if any Eulerian property holds
- Compute S distribution, generator decomposition

This is the cleanest null comparison — a "non-designed" sequence that's maximally regular.

**Output:** Complete comparison table: KW vs Fu Xi on every structural measure.

---

## Thread G: Anti-Generator Basis and Full Decomposition

**Question:** The natural basis for Z₂⁶ = Z₂³ × Z₂³ is {O, M, I} (kernel) + {Ō, M̄, Ī} (anti-generators, spanning im(P)). What does every hexagram look like in this basis?

The anti-generators are the asymmetric single-pair flips:
- Ō = (1,0,0,0,0,0) — flip line 1 only (breaks O-symmetry)
- M̄ = (0,1,0,0,0,0) — flip line 2 only (breaks M-symmetry)
- Ī = (0,0,1,0,0,0) — flip line 3 only (breaks I-symmetry)

Every hexagram h has coordinates (ō, m̄, ī, o, m, i) in this basis where:
- (ō, m̄, ī) = orbit coordinates (determines which orbit)
- (o, m, i) = within-orbit coordinates (determines position in orbit)

Rewrite the entire KW sequence in this basis. Does the path simplify? Do patterns emerge that were invisible in the standard basis?

**Output:** The 64-hexagram sequence in the factored basis. Visualization of the orbit and within-orbit trajectories separately.

---

## Execution Strategy

**Round 1 (parallel, heavy computation):**
- Thread A (enumeration) — the big computational job
- Thread B (random baseline) — independent sampling
- Thread F (Fu Xi comparison) — quick computation

**Round 2 (parallel, builds on Round 1):**
- Thread C (meta-walk) — needs Eulerian paths from A
- Thread D (self-loop forcing) — needs Eulerian paths from A
- Thread E (generator chain) — needs valid sequences from A

**Round 3 (synthesis):**
- Thread G (anti-generator basis) — conceptual reframing using all results
- Captain + sage synthesis of what's forced vs chosen

**Gate decision points:**
- After Round 1: if enumeration count is O(1), threads C-E become "verify the unique solution" rather than "compare across solutions." Adjust accordingly.
- After Round 2: if generator chain shows no structure, drop it. If meta-walk is distinguished, pursue.
