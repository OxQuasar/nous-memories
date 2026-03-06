# Frame-Walking: Approaches to the 19 Silent Bits

The iter3 investigation exhausted a single analytical frame (Z₂⁶ decomposition, pairwise statistics, marginal frequencies) and found 19 of 27 free orientation bits with no detectable structure. The coupling finding (ratio 1.68, collective, not per-pair) proves that joint properties invisible to per-bit analysis can exist and be detected — if you ask the right question. The problem is generating the right questions systematically.

A frame-walking algorithm doesn't test hypotheses within a frame. It generates frames and navigates the space of frames.

---

## 1. Learn the Distinguisher

Take KW's 27 free orientation bits as the single positive example. Sample thousands of S=2-free orientations as negatives. The goal is not classification (one positive example is insufficient) but feature discovery.

**Approach:** Train an autoencoder or variational model on the S=2-free orientation space. Map all 2²⁷ valid orientations (or a dense sample) into a learned latent space. Examine where KW lands — is it near the center (typical) or in a specific region (structured)?

**What it finds:** Nonlinear features of the orientation vector that the linear/pairwise tests missed. If the latent space clusters, KW's cluster membership is the frame. If KW is an outlier in the latent space but not in any marginal — that's the 19-bit structure.

**Limitation:** With only one positive example, any finding needs validation against the known signals (coupling, M-component, canon asymmetry) to confirm it's detecting real structure rather than overfitting.

---

## 2. Neighborhood Geometry

Instead of asking "is KW special?" ask "is KW's neighborhood special?"

**Approach:** Compute properties of all orientations within Hamming distance k (k = 1, 2, 3) of KW. Compare the distribution of any metric (kernel chi², canon asymmetry, coupling ratio, or new metrics) in this neighborhood vs the global S=2-free distribution.

**What it finds:** Local geometry. If KW sits at a basin (neighbors are worse on all metrics), a ridge (better along one direction, worse along others), or a saddle — each implies different structure. A basin means KW is a local optimum of some implicit objective. A ridge means there's a privileged direction in orientation space. A saddle means KW balances competing pressures.

**Key test:** The coupling analysis found only 3/32 single-bit flips improve both kernel chi² and canon asymmetry simultaneously. Extending this to 2-bit and 3-bit flips maps the local geometry more completely. If the "improvement cone" has a specific shape in 27-dimensional space, that shape is the frame.

**Advantage:** No new metrics needed. Uses existing measurements but asks a geometric rather than statistical question.

---

## 3. Mutual Information Graph

The current tests checked marginal frequencies (1-bit) and pairwise correlations (2-bit, linear). Mutual information captures nonlinear dependencies between bits.

**Approach:** For all pairs of free orientation bits (27 choose 2 = 351 pairs), compute the mutual information I(bᵢ; bⱼ) conditioned on S=2 constraints. Also compute conditional mutual information I(bᵢ; bⱼ | bₖ) for triples — dependencies that only appear when a third bit is known.

**What it finds:** A dependency graph. If bits 7 and 23 are uncorrelated but I(b₇; b₂₃) > 0, there's a nonlinear relationship invisible to Pearson correlation. The graph topology — clusters, chains, hubs, isolated nodes — is itself a structural finding. Clusters of mutually-informative bits are candidates for joint properties like the coupling.

**Extension:** Compute the total correlation (multi-information) of subsets of bits. The subset with highest total correlation per bit is the most structured subset — and its complement is the genuinely free residual.

**Limitation:** Requires sampling from the conditional distribution P(orientations | S=2-free), which is straightforward (the constraints factor). But 351 pairwise MI estimates need enough samples for stable estimates — probably 500K+.

---

## 4. Subgroup Lattice Scan

The current frame factors Z₂⁶ as orbit × position via the ⟨O,M,I⟩ kernel. But Z₂⁶ has other subgroup decompositions. Each decomposition is a different frame.

**Approach:** Enumerate subgroups of Z₂⁶ and their coset decompositions. For each decomposition, express the orientation choices in the new coordinates. Test whether the 19 silent bits align with any alternative factoring.

**Candidate decompositions:**
- Trigram × trigram: (L1,L2,L3) × (L4,L5,L6). The standard trigram reading.
- Nuclear × outer: (L2,L3,L4,L5) × (L1,L6). Nuclear hexagram vs outer lines.
- Weight strata: partition by Hamming weight rather than algebraic structure.
- Complement classes: group hexagrams by their relationship to their complement.

**What it finds:** Whether the orientation structure aligns with a decomposition other than the one used throughout the investigation. The M-component finding (L2,L5 axis) already hints that the middle mirror pair has special status — a trigram-based factoring might make this clearer.

**Key question:** Does there exist a decomposition of Z₂⁶ in which the 19 silent bits become structured and the 8 structured bits become silent? If so, the structure isn't fading — it's rotated relative to the frame.

---

## 5. Fragility Mapping (Adversarial) <This has been done  in iters 4-6>

Don't search for what makes KW special. Search for the smallest perturbation that destroys each known property.

**Approach:** For each known signal (kernel uniformity, canon asymmetry, M-component, coupling), find the minimum-weight perturbation (fewest bit flips) that moves KW from the significant tail to the bulk. Map these "destruction vectors" in the 27-dimensional free-bit space.

**What it finds:** Which bits are load-bearing for which properties. A bit that appears in the destruction vector for multiple properties is a structural keystone. A bit that appears in none is genuinely free.

**The key output:** A partition of the 27 free bits into:
- **Fragile bits**: flipping them destroys at least one signal. These carry structure.
- **Robust bits**: flipping them changes nothing detectable. These are genuinely free (or carry structure invisible to all current metrics).
- **Coupling bits**: flipping them affects the *relationship* between signals (changes the coupling ratio) without affecting either signal individually. These are the most interesting — they carry the holistic structure.

**Advantage:** This is the most operationally precise approach. It doesn't require new metrics or new frames — it maps the existing findings onto specific bits, answering "which bits matter?" directly.

---

## 6. Frame-Space Navigation (Meta-Algorithm)

The five approaches above are all specific frame choices. The meta-question: how do you navigate the space of frames?

**Principle:** Each frame is a projection of the 27-bit orientation vector onto a lower-dimensional feature space. The current frame projects onto {chi², canon_asym, m_score}. Each approach above proposes a different projection. The meta-algorithm needs to evaluate projections and move toward more informative ones.

**Criterion:** A frame is more informative if it compresses the distinction between KW and random into fewer dimensions. The current frame compresses the distinction into 2.5 dimensions (the effective signal count). A better frame would compress it into fewer — ideally into a single principle that explains all three signals and predicts the coupling.

**Search strategy:** Start with the fragility mapping (Approach 5) because it's cheapest and most grounded. Use the fragile/robust partition to constrain the neighborhood geometry (Approach 2) — only vary the robust bits and see if the neighborhood has structure. If yes, feed those features into the MI graph (Approach 3) to find the dependency structure. If the MI graph has clusters, try the subgroup scan (Approach 4) for an algebraic interpretation of those clusters. The learned distinguisher (Approach 1) is the last resort — use it only if the structured approaches fail.

**Stopping criterion:** The frame search stops when either:
- The 19 bits are partitioned into explained (fragile) and genuinely free (robust + no MI structure), or
- A new joint property is discovered (like the coupling) that accounts for additional bits, in which case update the partition and continue.

The gradient from clarity to silence may sharpen into a cleaner boundary — or it may persist, confirming that the fade is real and not a frame artifact.

---

## 7. Internal Structure → Meaning-Space Geometry

The investigation decomposed Z₂⁶ into orbit × position and tracked how the sequence moves through that product space. But each hexagram has internal structural relationships that generate its meaning, and these haven't been connected to the sequence path.

**Three untouched internal layers:**

- **Trigram interaction** (L1-L3 × L4-L6): the primary meaning-carrier. Lower trigram = inner situation, upper = outer. 8 trigrams with their own relational geometry (family, elemental, Earlier/Later Heaven arrangements). Each hexagram is a specific inner-outer pairing.

- **Nuclear trigrams** (L2-L4, L3-L5): the hidden dynamic inside the hexagram. The investigation collapsed this to a single bit (Theorem 12: nuclear trigram ≡ M-component). The full nuclear structure — which hidden dynamic lives inside each configuration — is unexplored.

- **Line-role configurations**: each position carries a role (seed, inner ruler, transition, threshold, outer ruler, culmination). Yin or yang at each role creates a specific situational meaning. The interaction of all 6 role-value pairs produces the hexagram's gestalt — not decomposable into single-line properties.

**The question:** as KW walks through the 64 hexagrams, what path does it trace through trigram-interaction space? Through nuclear-trigram space? Do the transitions between consecutive hexagrams follow a logic at the trigram level — not just XOR masks on bits, but transformations of inner-outer situational relationships?

**Connection to developmental priority:** iter6 found that KW's orientation encodes "condition → consequence" across all 32 pairs. Does this principle have a trigram-level description? When inner-Water/outer-Mountain transforms into inner-Fire/outer-Wind, is there a structural relationship between the trigram transitions that carries the developmental logic?

**Connection to the complementary coverage finding:** algebra and meaning cover different pairs with inverse strength. The trigram interaction layer sits between them — it's where bit patterns become situational meanings. Mapping this intermediate layer might reveal *why* the coverage is complementary: which structural features of the trigram interactions make some pairs algebraically rigid and others semantically transparent.

**What this requires:** treating the 64 hexagram meanings not as a lookup table but as points in a meaning-space with its own geometry. The trigram relationships provide the coordinate system. The hexagram names and judgments provide the metric (how "far apart" are two situations?). The KW sequence traces a path. The question is whether that path has structure in meaning-space that the algebraic path through Z₂⁶ cannot see.

This is the frame that would operate on both algebra and meaning simultaneously — not by adding axes to either, but by working in the intermediate space where one becomes the other.
