# Resolution Investigation — Plan

## Context

The dynamics investigation (R253–R281) established the I Ching as the smallest discrete system where symbolic dynamics (GMS), spectral theory (Chebyshev), and renormalization (block-spin RG) coexist. The literature review confirmed every component is the first nontrivial instance of its standard construction. The minimal Markov partition interpretation reframes the question: not "does it model dynamics" but "what resolution does this projection give, and what is it projecting?"

Questions in `questions.md`. Six questions (R1–R6), ordered by tractability.

## Probe 1: Logistic Map at Fibonacci Parameter (R1)

**Method:** Computation.

The logistic map x → rx(1-x) has a symbolic dynamics that transitions through SFT types as r increases. At a specific parameter r_fib (the accumulation point of the Fibonacci cascade), the symbolic dynamics becomes the GMS — forbidding "11."

Steps:
1. Identify r_fib precisely (literature value or numerical computation)
2. Generate the Markov partition of the logistic map at r_fib with 8 cells (3 bits of resolution)
3. Compute the 2-step transition matrix on 64 = 8² states
4. Compare to the I Ching's 五行-typed transition structure on Q₆
5. Check: do the three transition types (比和/生/克) correspond to identifiable features of the logistic map's dynamics?

**Success criterion:** Exact or near-exact match of transition matrices. If the 64-state structure matches, the projection target is the logistic map at the boundary of chaos.

**Failure mode:** The logistic map produces a GMS in its symbolic dynamics but the full 64-state structure doesn't match Q₆. This would mean the GMS connection is real but the projection target is something else.

**Note:** This probe requires no embeddings, no text, no cached methodology. Pure computation on the logistic map.

## Probe 2: Timescale Survey (R2)

**Method:** Literature survey + data analysis.

The three spectral radii {1, √2, φ} give timescale ratios. In a physical system, these would correspond to relaxation times, oscillation frequencies, or growth rates of three interacting processes.

Steps:
1. Survey systems with three dominant timescales
2. For each candidate, compute the ratio of the fastest to middle and fastest to slowest timescale
3. Check for {√2, φ} ratios (within measurement uncertainty)
4. If a match is found, check whether the system also has: (a) binary states, (b) inversion symmetry, (c) a forbidden-pattern constraint

**Candidates to check first:**
- Ecological succession: pioneer/intermediate/climax stages with disturbance
- Neural oscillation bands: gamma/beta/alpha frequency ratios
- Predator-prey-resource systems: fast predation / medium reproduction / slow resource renewal
- Market microstructure: tick/daily/structural timescales

**Note:** This is an empirical search. The ratios {√2, φ} are irrational, so exact matches won't occur — look for convergence within natural variability.

## Probe 3: Regime Transition Data (R3)

**Method:** Empirical data analysis.

Test the GMS constraint and valve on real regime-change data. The prediction: in systems with binary exclusion and inversion symmetry, consecutive destructive states are suppressed, and destruction never directly produces generation.

Steps:
1. Find a dataset with classified regime transitions (political science, ecology, or finance)
2. Map regimes to 比和/生/克 categories (continuity/generation/destruction)
3. Count transition type bigrams
4. Test: is 克-克 suppressed relative to random? Is 克→生 absent or suppressed?
5. Compare to the I Ching's transition matrix

**Best candidate datasets:**
- Polity IV (political regime changes, ~200 countries × decades)
- Ecological regime shift database (ERSE)
- Market regime classification (bull/bear/sideways × sector)

**Note:** The mapping from empirical regimes to 比和/生/克 is the hard part. Multiple mappings should be tested to avoid confirmation bias.

## Probe 4: Dark Sector Characterization (R5)

**Method:** Computation (spectral analysis of Q₆ transition matrices).

The 60 uncharacterized hex-level eigenvalues dominate long-time dynamics. Characterize them.

Steps:
1. Compute full spectrum of each 五行 OR-symmetrized adjacency matrix on Q₆
2. Identify the 60 eigenvalues with no trigram-level ancestor (dark sector)
3. Check: do they organize by any symmetry group? (Walsh weight? Automorphism orbits?)
4. Compute the time at which dark sector modes dominate over coherent sector
5. Interpret: what dynamics do the dark sector modes correspond to?

**This probe can run immediately** — all data is cached, pure computation.

## Probe 5: Composability (R6, connects to Q2)

**Method:** Algebraic analysis.

Check whether the transition structure supports meaningful composition: if hex A transitions to hex B, and hex B transitions to hex C, does the A→C relationship preserve dynamical information?

Steps:
1. Compute the 2-step transition matrix A² for each 五行 type
2. Check: does A² preserve the 五行 typing? (Is 克² still 克-like?)
3. Characterize the "information loss" per step: mutual information between n-step and (n+1)-step transition types
4. Connect to the RG structure: does composability align with the 互 coarse-graining?

## Priority Order

1. **Probe 4 (dark sector)** — immediate, computational, fills the largest gap in current knowledge
2. **Probe 1 (logistic map)** — immediate, computational, could identify the projection target
3. **Probe 5 (composability)** — computational, connects to the sole open structural question
4. **Probe 2 (timescale survey)** — literature search, medium effort
5. **Probe 3 (regime data)** — empirical, high effort, mapping ambiguity
