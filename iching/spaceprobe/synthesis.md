# Spaceprobe: Final Synthesis

## The arc of the investigation

This work began as **opposition theory** — the hypothesis that the I Ching optimizes a unified measure of oppositeness across scales. That hypothesis was wrong. But pursuing it led somewhere more precise.

The opposition theory (4 phases) established:
- The pairing layer is structurally thin — KW just inverts hexagrams, one of 9 options the geometry allows
- S and D are orthogonal — no trade-off between strength and diversity
- The five-phase layer is orthogonal to the pairing layer
- Nuclear trigrams carry no independent opposition information
- The real opposition lives in the **sequence**: consecutive transitions are directionally opposite

The **Lo Shu investigation** discovered:
- The KW trigram circle and Lo Shu magic square are the same structure
- Three pairing systems (Fu Xi, Lo Shu/KW, He Tu) occupy three distinct points in opposition measure space
- No direct number→binary bridge exists — the systems agree only through the trigrams

That convergence-without-reduction raised the central question:

> Multiple coordinate systems faithfully represent the same 8-state structure without being reducible to each other. What IS that structure?

The **spaceprobe** answered it.

---

## The answer

The trigram relational space is an **8-element set with three distinguished fixed-point-free involutions** satisfying two axioms:

> **Axiom 1 (Overlap):** One pair of involutions shares exactly one pair; the other two pairs of involutions share nothing.
>
> **Axiom 2 (Commutation):** The two involutions that share no pair with each other commute (their product has order 2).

This determines a **unique structure** (up to one orientation bit): S₄ acting faithfully on 4 blocks of 2.

The three involutions are the three traditional pairing systems:
- **ι₁ (Fu Xi complement):** pairs each trigram with its bitwise inverse
- **ι₂ (KW/Lo Shu diametric):** pairs trigrams opposite on the Later Heaven circle
- **ι₃ (He Tu):** pairs trigrams whose Lo Shu numbers differ by 5

The 4 blocks are: {Kun, Zhen}, {Gen, Dui}, {Kan, Li}, {Xun, Qian}.

**Almost rigid:** From the involutions alone, Aut = Z₂. Adding any orientation information (from Z₂³ binary structure, from five-phase assignments, from Lo Shu odd/even — all independently provide the same bit) makes the structure fully rigid: Aut = {id}. Every element is uniquely determined.

---

## Why the coordinate systems agree

The systems agree because the object they describe admits **at most two self-maps**. Once the single orientation bit is fixed, there is exactly one way to assign labels that respects all three involutions simultaneously. Any faithful coordinatization — binary, numerical, elemental, directional — must land on the same rigid assignment.

The systems don't reduce to each other because they coordinatize **different aspects** of the same object:
- **Binary (Z₂³):** algebraic structure — group operations, Hamming metric
- **Lo Shu:** number-theoretic structure — magic square sums, arithmetic pairs
- **Five phases:** directed interaction structure — 生/克 cycles, element groupings
- **He Tu:** the "clean" involution — the one that permutes blocks without disrupting their internal structure

These are genuinely different projections, like longitude and latitude describe the same point without being functions of each other. The rigidity of the underlying object forces them to agree.

---

## Extension to n=6

At n=6, the three basic involutions (complement, reversal, comp∘rev) all commute, generating only V₄ — trivially forced. The structurally interesting group is **G₃₈₄** (order 384), built from three layers:

1. Mirror-pair XOR masks T ≅ Z₂³
2. Within-pair position swaps ≅ Z₂³
3. Pair permutations ≅ S₃

T acts freely on 64 hexagrams, producing 8 orbits. S₃ merges them into 4 macro-orbits by residual weight. Two are forced (palindromes, anti-palindromes). Two are free, each with 3 choices. Total: **3² = 9 equivariant pairings** — the same count as n=3, for the same structural reason.

**KW is not in the group.** It applies reversal on 48 hexagrams and complement on 16 (the palindromes). A group element must act uniformly; KW selects between operations conditionally. It is equivariant *under* G₃₈₄ without being *in* it. The group provides the vocabulary and grammar; KW is a well-formed sentence.

**KW is the unique weight-tilt minimizer** among the 9 (WT = 0.375, threefold gap to next-best 1.125).

---

## The cross-scale divergence: resolved

At n=3, the tradition chose complement (ι₁) — maximum strength, a group element, no fixed points. At n=6, it chose the reversal-hybrid (KW) — minimum weight tilt, not a group element, hybrid construction forced by palindromic fixed points.

This is **not** the same tradeoff resolved differently. It is the **emergence of a tradeoff that didn't exist at n=3**.

At odd n: complement is simultaneously FPF, a group element, and the strongest involution. No tension. Everything aligns.

At even n: parity creates palindromic fixed points. Reversal (the weight-preserving operation) has 8 fixed points. To get a complete pairing, you must either accept complement everywhere (WT = 1.875, a pure group element) or patch reversal's fixed points with complement (WT = 0.375, exiting the group). The tradition chose weight preservation.

The common skeleton across scales: a translation subgroup T ≅ Z₂³ whose orbits are organized by S₃ into 4 macro-orbits, 2 forced + 2 free, yielding 3² = 9 equivariant pairings. The divergence is in which pairing is selected and why.

**n=6 is the minimum even length where this works.** At n=4 (2 mirror pairs), 117 equivariant pairings — too loose. At n=6 (3 mirror pairs), S₃ creates the precise structure for unique selection. This doesn't explain why hexagrams have 6 lines (they have 6 because they're two 3-line trigrams stacked), but it shows that n=6 is the natural scale for the pairing mechanism — the compositional choice of doubling trigrams happens to produce the minimum length where equivariant pairings are tightly constrained.

---

## Opposition in the flow: the sequence layer

*(Investigated in 5 computational rounds. Full results in `sequence/synthesis.md`.)*

The pairing layer turned out to be structurally thin. The sequence layer is where opposition actually lives — but the structure is descriptive, not axiomatic.

### Corrected measurements

The earlier synthesis reported inflated figures. Under the correct null model (randomize both pair permutation and orientation):

| Claim | Earlier report | Corrected |
|-------|---------------|-----------|
| Kernel distance percentile | 99.2nd | **96.6th** |
| kac (kernel repeats) | 0th percentile (no repeats) | **2 repeats** (OM→OM, OI→OI) |
| Load-bearing orientation bits | 27/27 | **16/32** |
| Transition grammar (MI) | 1.33 bits | **Artifact** of small-sample bias |

### Two independent signals survive deflation

**1. Consecutive kernel distance (f1 = 1.767, 96.6th percentile).** The mechanism: 8 of 30 consecutive kernel transitions are OMI (full complement) — each transition maximally opposes the previous. f1 and OMI count are one signal (r = 0.65).

**2. H-subgroup residence (20/31 = 64.5%, 96.7th percentile).** The running product of bridge kernels preferentially inhabits H = {id, O, MI, OMI}, uniquely distinguished among all 7 order-4 subgroups of Z₂³. **Algebraic characterization:** z ∈ H iff the M-bit equals the I-bit (the "M-I lock"). The middle and inner mirror pairs flip together or not at all; the outer pair is free. This bias comes from pair *ordering*, not orientation choices, and is **independent of f1** (r = −0.001).

### The two-canon asymmetry

Both signals localize entirely to the Upper Canon (hex 1–30):

| | Upper Canon (14 bridges) | Lower Canon (16 bridges) |
|---|---|---|
| f1 | 2.154 — **99.84th %ile** | 1.467 — **51st %ile** |
| H-residence | 11/14 = 79% — **99.42nd %ile** | 8/16 = 50% — **60th %ile** |
| Joint probability | ~1 in 10,000 | Indistinguishable from random |

The Lower Canon is structurally generic on every metric tested (kernel distance, subgroup residence, weight smoothness, trigram continuity, raw Hamming distance). Whatever it encodes — if anything at the structural level — is not visible in bridge-transition metrics.

The overall KW properties (f1 = 1.77, H-residence = 64.5%) are averages of two qualitatively different regimes. The cross-canon bridge (hex 30→31, kernel = OM) explicitly breaks the M-I lock.

### Constraint tightness

Five constraints (f1 ≥ 1.70, H-residence ≥ 20/31, repeats ≤ 2, all 8 kernel types, OMI ≥ 8) jointly eliminate ~99.9% of random orderings. About 1 in 1,200 random orderings satisfies all. This constrains but does not characterize — the sequence layer resists axiomatic determination.

### Developmental priority and the two-canon division

*(Investigated in lead 2. Full results in `lead2/findings.md`.)*

The 32/32 developmental priority alignment (every KW pair oriented with condition before consequence, p = 2.3 × 10⁻¹⁰) distributes asymmetrically: 60% Clear in the Upper Canon, 71% Clear in the Lower Canon. The structurally silent canon has stronger meaning.

The critical finding is in the dominator analysis. The 12 algebraic dominators (orientations beating KW on all 4 metrics) achieve superiority by reversing Lower Canon pairs: **72% of all dominator pair-reversals target the Lower Canon**, concentrated on Clear-confidence pairs (Guai/Gou 12/12, Jian/Xie 9/12, Sun/Yi 9/12). Every dominator reverses at least as many Lower as Upper pairs.

The algebra↔meaning inverse correlation (where algebra binds tightest, meaning is weakest) replicates within each canon separately — it's a pair-level phenomenon, not a canon-level artifact.

**The two-canon picture:**

| | Upper Canon | Lower Canon |
|---|---|---|
| Kernel structure | Extreme (~1 in 10,000) | Generic |
| Algebraic fragility | Tight (53% KW-dominates) | Loose (29% KW-dominates) |
| Meaning clarity | 60% Clear | 71% Clear |
| Dominator target | 28% of violations | 72% of violations |
| Organizing principle | Algebra | Meaning |

The cross-canon bridge (hex 30→31) marks the transition between regimes.

### The divination operation: H-projection and 克 bias

*(Investigated as lead 3. Full results in `lead3/findings.md`.)*

Tracing the Meihua circuit (本→互→变) through all coordinate systems for 384 states reveals three structural properties of the nuclear hexagram (互卦):

**1. H-projection theorem.** Every 互卦 has its mirror-pair kernel in H = {id, O, MI, OMI}. Proof: kernel(互(h)) = (M_本, I_本, I_本), and since M-bit = I-bit = I_本, the kernel is always in H. The 16 互 values distribute evenly: 4 each of {id, O, MI, OMI}. The kernel undergoes a downward shift: O ← M ← I ← I (outer replaced by middle, middle by inner, inner doubled).

**2. 克 amplification.** 互 destroys 生 (generation) relations (×0.33) and amplifies 克 (overcoming) relations (×1.54). The transition matrix has structural zeros: 克 states never become 生 in 互. The nuclear hexagram is algebraically biased toward adversarial dynamics.

**3. 体 absolute preservation in 变.** The 体 trigram is unchanged from 本 to 变 (100%, trivial by construction — moving line is always in 用). Combined with the 克-biased 互, the circuit reads: surface situation → hidden conflict → future development with preserved identity.

Additional path invariants: the 本→互 XOR kernel is restricted to {id, O, M, OM} (I-bit always 0); the amplification gradient d(互(本), 互(変)) = {0, 1, 2} for {outer, middle, inner} lines is an exact constant, not a mean; 34/125 possible five-phase trajectories are structurally forbidden; yang(互) = yang(本) + L3 + L4 − L1 − L6 (depends only on inner-outer pair difference).

**H characterized via 互:** H = ker(互) × ⟨complement on 互-space⟩ = {id, O} × {id, MI}. The elements that either don't change the nuclear hexagram at all (id, O — distance 0) or complement it entirely (MI, OMI — distance 6). Non-H elements produce intermediate scrambling (distance 2 or 4). H is the subgroup whose effect on divination is *extremal* — maximally simple.

The H-subgroup now appears in four independent contexts:
- **互卦 output**: kernel(互) always in H (algebraic necessity)
- **互卦 action**: H = elements acting simply on 互-space (structural characterization)
- **Sequence** (Upper Canon): 64.5% H-residence, 96.7th percentile
- **Algebraic structure**: uniquely distinguished among 7 order-4 subgroups

**The thread:** The sequence is arranged so that consecutive transitions preferentially either don't affect the nuclear hexagram, or complement it entirely — never scramble it. The ordering and the divination operation are algebraically coherent.

### Fu Xi vs KW: opposite sequential designs

Fu Xi is maximally smooth (constant kernel distance, 2 types, zero variance). KW is maximally rough in the Upper Canon (high kernel distance, all 8 types, OMI-dominated transitions). They sit at opposite extremes of the same combinatorial space — systematic enumeration vs process ordering.

---

## What was eliminated

- **Unified opposition theory:** No single measure or framework captures the tradition's design logic across scales. S and D are orthogonal. The information-theoretic framework was superseded. Weight preservation is tautological with reversal.

- **Scale bridge via 生克:** The five-phase system is orthogonal to the hexagram pairing. 体/用 projection is structurally neutral (uniform sampling theorem). The five-phase layer's one distinctive property (modal complementarity, top 13.3%) is about differentiating 生 from 克 mask vocabularies, independent of pairing.

- **Nuclear trigram independence:** 互卦 carries no *opposition* information beyond the hexagram level. It's a lossy projection (erase outer pair, double inner pair). However, it has rich structural properties: it projects into the H-subgroup (always), biases toward 克 relations (×1.54), and preserves KW pairing (87.5%). See the divination section below and `lead3/findings.md`.

- **Additional coordinate systems:** 天干, 地支 (六冲, 六合, 三合) are all compatible with but redundant to the S₄ structure. The two-axiom characterization absorbs everything.

- **The missing mask:** Mask 011 being absent from the three generators is a coincidence of the realization, not forced by the axioms.

- **Kernel transition grammar:** The MI of 1.33 bits between consecutive kernel types is an artifact of small-sample upward bias (Miller-Madow correction: −0.41 bits). After correction, KW's sequential structure is 0.43σ above the shuffle null — unremarkable.

- **Sequence-layer axiomatic characterization:** Five rounds of computation found no constraint set that tightly determines the ordering. The sequence layer yields a structural *signature* (two-canon asymmetry, H-subgroup bias) but not a generating *rule*.

---

## What remains genuinely open

### Resolved in this investigation

3. **The Lower Canon.** ~~Structurally generic on all bridge-transition metrics.~~ **Resolved (lead 2):** organized by developmental priority. 72% of dominator violations target Lower Canon pairs. See `lead2/findings.md`.

4. **Why H = {id, O, MI, OMI}?** ~~Unexplored.~~ **Resolved (lead 3):** H = ker(互) × ⟨complement on 互-space⟩. The algebraic fingerprint of the nuclear hexagram operation. See `lead3/findings.md`.

### Still open

1. **Why FPF involutions?** FPF = every element has a partner = no orphans, no spectators. This forces 4 blocks, which forces categorical completeness — every state has a type, every state participates in every pairing. Drop FPF and blocks become ragged (some elements unpaired), categories incomplete, the interpretive apparatus (体/用, 生/克) breaks. Weakening analysis confirms: FPF bounds group size (≤168 vs ≤40,320), forces block decomposition, and in Rep A propagates deeply (63% of group is FPF, not just the generators). The axiom is the minimal philosophical commitment — universal complementarity — that generates the maximal structural yield. Everything downstream (S₄, the bridge, H, divination coherence) follows from it. Not derivable from mathematics; it is the assertion that the universe has no spectators. See `doubles/weakening-findings.md`.

2. ~~**The polarity partition.**~~ **Fully resolved.** The polarity is derivable from Z₂³ + S₄ alone — no magic square needed. The predicate: P₋ = {blocks containing a binary extreme (000 or 111)}. This is forced because: (a) Z₂³ distinguishes 000 and 111 as extremes, (b) ι₁ (complement) pairs 000↔111, (c) ι₁ maps between blocks so they're in different blocks, (d) the overlap block {Kan,Li} = {010,101} contains neither extreme, (e) exactly 2 of 4 blocks contain an extreme → 2+2 split = polarity. The magic square agrees (odd Lo Shu = P₊ blocks) but is not needed — it's a number-theoretic coordinate system that realizes a partition already forced by the algebraic structure. See `doubles/magic_square_probe.py`.

3. ~~**The 52-triple question.**~~ **Resolved.** 52 minimal FPF-generating triples exist in S₄. They split into 4 classes by overlap × signature. The traditional class (overlap (0,0,1), commutation, sub-pair orders {2,3,4}) contains 24 triples forming **1 conjugacy class** — all related by relabeling. The traditional triple is unique up to symmetry. No residual freedom. See `doubles/triple_question.py`.

3b. **Two paths to S₄.** Rep A (traditional) and Rep B both give S₄ on 4 blocks of 2. They differ in two ways: (a) Rep A has a bridge (Kan↔Li, overlap (0,0,1)) while Rep B has dense overlap (1,1,2) and no distinguished axis; (b) Rep A has deep complementarity (63% of group elements are FPF — compositions of the three pairings mostly still move everything) while Rep B is shallow (only 25% FPF — compositions mostly leave elements fixed). The tradition chose the representation where the founding principle (universal complementarity) pervades the algebra, not just the generators. See `doubles/weakening-findings.md`.

4. **Selection effect in the Upper Canon.** Does the specific hexagram content of the first 15 pairs inherently support higher f1 and H-residence? Untested.

5. **Referential status.** The characterization says what the structure IS (a rigid combinatorial object derivable from four minimal inputs). It does not say what it is FOR. The tradition's claim — that this structure is isomorphic to the relational structure of events — is outside this analysis.

6. **The cohabitation.** Two algebraically independent structures — Z₂³ (from doubling) and S₄ (from involution axioms) — share the same carrier set. That they *fit* is a fact about S₄'s representation theory, not a consequence of the doubling. Whether this cohabitation is discovered (the mathematical universe forces it) or designed (someone chose inputs knowing they'd cohabit) is the question the structural analysis cannot answer.

---

## The strongest claim the evidence supports

The trigram relational space is a determinate mathematical object, uniquely characterized by two elementary combinatorial axioms on three fixed-point-free involutions. It admits multiple faithful coordinatizations — binary, number-theoretic, elemental, directional — which agree by structural necessity (the object's near-rigidity forces agreement) rather than by convention or coincidence.

The hexagram pairing space is a constrained extension of this object. The same 3² = 9 counting mechanism operates at both scales, but the traditional pairing choice diverges: complement at n=3 (where no tradeoff exists), reversal-hybrid at n=6 (where parity forces a new tradeoff between algebraic purity and weight preservation). n=6 is the minimum even length where the constraint space is tight enough for unique selection.

The hexagram sequence carries genuine but non-axiomatic structure: two independent algebraic signals (consecutive kernel distance and H-subgroup residence) that localize entirely to the Upper Canon (~1 in 10,000 on the joint metric). The Lower Canon is algebraically generic but semantically organized: developmental priority (condition→consequence ordering) defends it against the algebraic dominators that would otherwise improve KW's metrics. Two canons, two organizing principles — algebra and meaning — jointly preventing domination.

The tradition's design logic is not opposition-maximization. It is:
- **At the pairing level:** conservation within the constraints geometry permits
- **At the sequence level (Upper Canon):** maximum opposition between consecutive transitions, with the cumulative transformation path constrained to a specific subgroup (the M-I lock)
- **At the sequence level (Lower Canon):** developmental priority — condition→consequence ordering of pair orientations, defending against algebraic domination (72% of dominator violations target this canon)
- **At the five-phase level:** maximum differentiation between interaction modes

- **At the operational level:** the divination circuit (本→互→变) projects through the H-subgroup, biases toward 克 dynamics, and preserves the 体 trigram absolutely — structure optimized for reading conflict beneath surfaces

Multiple optimization targets on orthogonal structural layers, unified by: (a) the rigid combinatorial object they all act on, and (b) the H-subgroup {id, O, MI, OMI}, which appears as the sequence's preferred transition space, the divination operation's algebraic image, and the uniquely distinguished order-4 subgroup of Z₂³.

---

## The derivation chain: what's forced, what's designed

*(Investigated as "doubles" workflow. Full results in `doubles.md`.)*

The recursive doubling 太极→两仪→四象→八卦 builds the **object space** (Z₂ⁿ) but not the **symmetry** (S₄). These are two algebraically independent structures sharing the same 8-element carrier set. The binary tree gives S₂ ≀ S₂ ≀ S₂ (order 48) at the trigram level; S₄ (order 24) is not a subgroup. 0 of 48 tree labelings reproduce the S₄ block system. The traditional S₄ is not even affine on Z₂³ — it lies outside all 280 S₄ subgroups of AGL(3,2).

**Four minimal, non-redundant inputs generate everything:**

| # | Input | Type | What it forces |
|---|-------|------|----------------|
| 1 | Binary lines (yin/yang) | Object | Z₂ⁿ recursion → 8 trigrams, 64 hexagrams |
| 2 | Symmetries are FPF involutions | Symmetry | Minimum 3 generators required |
| 3 | FPF extends to commuting pairs | Symmetry | Selects Rep A, kills Rep B → S₄ unique |
| 4 | Outer-pair erasure (line adjacency) | Operation | Selects 互 among 15 windows, determines H |

Remove any one and the derivation fails. No input implies another.

**The boundary between mathematics and design is crisp.** Everything downstream of the four inputs — S₄, the unique representation, the three involutions, Z₂³, H, the 克 bias, the divination circuit's algebraic properties, the sequence/divination coherence — follows by mathematical necessity. The four inputs themselves are design choices: elegant, minimal, non-redundant, but not derivable from each other or from the recursion.

**Key structural findings:**
- The broken bridge (Step 3) is the core result: the doubling that builds trigrams and the axioms that structure them have independent origins. That they cohabit the same carrier set is a fact about S₄'s representation theory.
- Two non-conjugate representations (Rep A vs Rep B) exist for S₄ on 4×2 blocks. A single predicate (FPF on commuting pairs) eliminates Rep B.
- Three consecutive-window nuclear operations exist; only the traditional 互 (L2–L5) has non-trivial kernel {id, O} and produces the full H.
- 52 minimal FPF-generating triples exist within the traditional S₄. Whether the traditional triple {ι₁, ι₂, ι₃} is distinguished among them by its sub-pair signature {4, 6, 8} is unresolved.

## Why S₄? 
                             
Because you want to say things about the vertices that the cube itself can't say.    

The cube (Z₂³) treats all vertices symmetrically — its automorphism group is order 336, every vertex is equivalent to every other. You can't classify, can't type, can't distinguish. It's the formless symmetric soup.            

S₄ says: these 8 things are actually 4 kinds of thing. That's a *claim about the world* — that there are categories, that some states are the same
type as each other. The cube can't make that claim because its symmetry is too large.          

But why S₄ specifically and not some other way to categorize 8 things? You could split 8 into 4+4, or 2+2+2+2, or any other partition. S₄ is what you get when your categorization satisfies:  

- Every state has a partner (FPF — universal complementarity)
- Three independent pairings exist (minimum to generate S₄)
- The pairings have the right overlap/commutation structure       

And the "why" behind *those* axioms, as we established: universal complementarity is the philosophical input. Everything has an opposite, in three independent senses. That's the assertion about the world that the cube alone can't make and the magic square alone can't make. S₄ is the minimal algebra that encodes it.      

So: Z₂³ because binary recursion. S₄ because categorization through universal complementarity. One builds the space. The other gives it meaning.  
