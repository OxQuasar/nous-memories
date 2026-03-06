# 19. Pair Orientation — Layer 4 Analysis

> The 32 King Wen pairs each have an internal ordering: which hexagram comes first (odd position) and which comes second (even position). This is 2³² ≈ 4 × 10⁹ degrees of freedom — the last unanalyzed layer. The traditional rule pairs hexagrams by inversion (read upside-down) or, for palindromic hexagrams, by complementation. But the *ordering* within each pair — which one is presented first — is a separate choice from the pairing itself.

Prior work in kingwen/ and logoswen/iter1-2. Key context:
- Layer 1 (orbit-consistent pairing) eliminates ~44 orders of magnitude
- Layer 2 (mask = signature identity, p ≈ 10⁻¹⁷) determines the pairing rule
- Layer 3 (pair ordering, p ≈ 10⁻³) determines the sequence of pairs
- Layer 4 (pair orientation) is the residual: given the pairs and their order, which hexagram is odd-positioned?
- The sequence data is in kingwen/sequence.py
- The orbit/mask/generator framework is established in kingwen/ studies 4-15 and logoswen/iter1-2

---

## Thread A: Orientation Census (Structured)

**Question:** What is the orientation of each pair, and what patterns exist in the 32-bit orientation string?

**Method:**
1. For each of the 32 pairs, record which hexagram is first (odd position) and which is second (even position)
2. Characterize the orientation in multiple frames:
   - **Inversion frame:** Is the first hexagram the "original" or the "inverted" form? For palindromic hexagrams (where inversion = identity), is the first the "original" or the "complement"?
   - **Weight frame:** Does the higher-weight (more yang) or lower-weight hexagram come first?
   - **Binary frame:** Does the numerically larger or smaller hexagram come first?
   - **Orbit position frame:** In the factored basis (ō,m̄,ī,o,m,i), what distinguishes the first from the second hexagram?
3. Encode each frame as a 32-bit binary string. Compute:
   - Balance (how close to 16/16 is each frame?)
   - Run-length structure
   - Autocorrelation at key lags (1, 2, 4, 8, 16)
   - Spectral content (FFT)
   - Correlation between the different frames
4. Compare each 32-bit string against 10,000 random orientations on the same pair sequence

**Output:** The orientation pattern in each frame, which frame (if any) produces the most structured 32-bit string, and which properties are statistically significant.

---

## Thread B: The Traditional Rule (Structured)

**Question:** The traditional King Wen pairing rule is: pair by inversion (flip the hexagram upside-down). For palindromic hexagrams, pair by complement. Within each pair, the "original" comes first. But what defines "original" vs "derived"?

**Method:**
1. For non-palindromic pairs (24 of 32): the first hexagram inverted gives the second. Verify this for all 24 pairs. Record any exceptions.
2. For palindromic pairs (8 of 32): the first hexagram complemented gives the second. Verify. Record exceptions.
3. The traditional literature assigns hexagram numbers — #1 Qian comes before #2 Kun, not the reverse. Is there a structural rule that recovers the traditional first/second assignment?
   - Weight ordering (yang-heavy first)?
   - Lower trigram ordering?
   - Upper trigram ordering?
   - Binary value ordering?
   - Some function of the orbit position coordinates?
4. For non-palindromic pairs: the two hexagrams are related by bit-reversal (reading lines bottom-to-top vs top-to-bottom). One reading direction is "first." Does the sequence consistently prefer one reading direction?
5. Test: does the orientation correlate with the pair's position in the sequence (early pairs vs late pairs)?

**Output:** Whether a single structural rule recovers KW's orientation choices, and if so, what that rule is.

---

## Thread C: Orientation and Bridge Structure (Structured)

**Question:** The bridge mask between pair k and pair k+1 is hex[2k+1] ⊕ hex[2k+2] — it depends on which hexagram is the *exit* (second in pair k) and which is the *entry* (first in pair k+1). Flipping orientation of either pair changes the bridge mask. How does orientation affect bridge properties?

**Method:**
1. For each of the 31 bridges, compute:
   - The current bridge mask (KW orientation)
   - The three alternative bridge masks (flip pair k, flip pair k+1, flip both)
   - For each alternative: the orbit_Δ (should be unchanged — flipping orientation doesn't change orbits), the kernel dressing, the S value, the Hamming distance
2. Verify: flipping orientation preserves orbit_Δ at every bridge (this should be a theorem — the orbit change depends only on which orbits are adjacent, not on which hexagram within the orbit is at the boundary)
3. For each bridge, how many of the 4 orientations produce S=0, S=1, S=2, S=3?
4. The 11 S=2-susceptible bridges: for each, does KW's specific orientation choice avoid S=2? Is the alternative orientation S=2? Quantify: how constrained is the orientation by S=2 avoidance?
5. Compute: if we fix everything except orientation (same pairs, same order, same Eulerian path), what fraction of 2³² orientations produce S=2-free sequences?
6. Among S=2-free orientations: what is the kernel dressing distribution? Does the kernel chain's uniformity and OMI contrast survive?

**Output:** How much of the orientation is forced by S=2 avoidance, and what properties of the kernel chain depend on orientation.

---

## Thread D: Orientation in the Factored Basis (Semi-structured)

**Question:** In the factored basis (ō,m̄,ī,o,m,i), pair orientation swaps the position coordinates (o,m,i) while leaving the orbit coordinates (ō,m̄,ī) fixed (since both hexagrams share an orbit). What pattern do the position coordinates follow?

**Method:**
1. For each pair, record the position coordinates of the first and second hexagram: (o₁,m₁,i₁) and (o₂,m₂,i₂)
2. Since mask = sig, the position change within a pair is the mask itself (verified in iter2). So (o₁,m₁,i₁) ⊕ (o₂,m₂,i₂) = mask. The question is: given this constraint, which of the two possible assignments does KW choose?
3. Track the position trajectory through the full 64-hexagram sequence. The orbit trajectory is known (step-function, changes at bridges). The position trajectory changes at every step. Characterize its structure:
   - Is there a preferred "starting" position within each orbit?
   - Do the 8 visits to each orbit (4 pairs × 2 hexagrams) cover all 8 positions?
   - What is the position trajectory's autocorrelation structure?
4. The position trajectory is the "hidden" path through Z₂³. The orbit trajectory is the "visible" path. Characterize their relationship: correlated, anti-correlated, independent?

**Output:** The structure of the position trajectory and its relationship to the orbit trajectory.

---

## Thread E: Weight and Yang Flow (Open-ended)

**Question:** The synthesis noted yang drainage within octets (7/8 octets lose yang). The orientation determines which hexagram — the heavier or lighter — comes first in each pair. Explore the relationship between orientation and the sequence's weight dynamics.

Directions to consider:
- The weight trajectory (yang count at each of the 64 positions). How does it depend on orientation?
- Within each pair, the weight either stays constant (mask preserves weight — true for all non-complement pairs) or jumps by |6 - 2w| (complement pairs). For complement pairs, orientation determines whether the jump is up or down.
- The 8 complement pairs (OMI mask) have weight sum exactly 6 (w + (6-w) = 6). KW places the heavier hexagram first in how many of these?
- Does the weight trajectory have a monotonic or structured character that depends on orientation?
- Connection to the traditional "waxing/waning" interpretation of hexagram pairs

---

## Thread F: Trigram Orientation (Open-ended)

**Question:** Each hexagram has an upper and lower trigram. Orientation swaps which trigram configuration is "first presented." Explore trigram-level patterns in the orientation.

Directions to consider:
- For each pair, which upper trigram comes first? Which lower trigram?
- The trigram trajectories (upper and lower separately, 64 steps each). How do they depend on orientation?
- Nuclear trigrams (lines 2-3-4 and 3-4-5). Do they show orientation patterns?
- The traditional "inner/outer" trigram interpretation: does orientation consistently present a particular trigram relationship first?

---

## Thread G: Captain's Direction (Fully open)

**Question:** Based on the findings from Threads A–F, the captain identifies the most promising seam and directs a focused investigation. This thread is defined after Threads A–F complete.

Possible entry points (to be refined or replaced based on findings):
- If Thread C reveals that S=2 avoidance tightly constrains orientation → enumerate the valid orientation space
- If Thread B finds a clean structural rule → test its uniqueness and algebraic status
- If Thread D shows position trajectory structure → connect to the kernel chain dynamics from iter2
- If Threads E/F reveal weight or trigram structure → connect to traditional interpretive framework
- Something unexpected

---

## Execution

**Round 1 (parallel, foundational):** Threads A + B + C
- A: census and statistical characterization
- B: traditional rule verification
- C: bridge structure dependence on orientation

**Round 2 (parallel, builds on Round 1):** Threads D + E + F
- D: factored basis analysis (needs A for orientation data)
- E: weight dynamics (needs A for orientation, C for bridge dependence)
- F: trigram patterns (needs A for orientation)

**Round 3:** Thread G — captain's direction from Round 1-2 findings

**Gate decisions:**
- After Round 1: if Thread B finds a complete structural rule, Threads D-F shift to testing/extending that rule rather than open exploration
- After Round 1: if Thread C shows orientation is almost entirely forced by S=2 avoidance, the effective degrees of freedom shrink dramatically — adjust Thread G accordingly
