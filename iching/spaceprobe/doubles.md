# Doubles: The Derivation Chain

## 1. The Claim

**Does recursive binary doubling (太极→两仪→四象→八卦) force the I Ching's algebraic structure?**

The traditional account presents a seamless progression: unity → two principles → four images → eight trigrams → sixty-four hexagrams. If this recursion fully determines the system's symmetry group, pairing logic, nuclear hexagram operation, and sequential coherence, then the I Ching is pure mathematics — a structure discovered, not designed.

If the recursion breaks — if the symmetry requires input the doubling can't provide — then there is a boundary between what is mathematically forced and what is designed. Finding that boundary precisely is the goal.

**Answer:** The doubling builds the object space (Z₂³, the 8-element set) but cannot build the symmetry group (S₄). Two independent structures cohabit the same 8 elements with no algebraic bridge. Four minimal, non-redundant design inputs are needed to derive everything. The boundary between mathematics and design is crisp.

---

## 2. The Chain

### Step 1: 太极 → 两仪 → 四象 → 八卦 (1 → 2 → 4 → 8)

**Classification: FORCED.**

A line is binary (yin/yang). Recursive doubling gives Z₂ⁿ:
- n=1: 2 elements (两仪)
- n=2: 4 elements (四象)  
- n=3: 8 elements (八卦 = trigrams = Z₂³, the vertices of a cube)

Each step is the unique operation of taking a binary product with Z₂. No choice.

### Step 2: 八卦 → 六十四卦 (8 → 64)

**Classification: FORCED.**

Doubling trigrams to hexagrams: 6-bit strings, |Z₂⁶| = 64. The mirror-pair structure emerges from the positional pairing of a hexagram's 6 lines: L1↔L6 (outer, O), L2↔L5 (middle, M), L3↔L4 (inner, I). These three pairs give Z₂³ acting on 64 hexagrams via palindromic XOR masks.

### Step 3: 8 Elements → S₄

**Classification: BROKEN BRIDGE — requires independent axioms.**

The recursive doubling that builds Z₂³ does NOT produce S₄.

| Structure | Source | Order |
|-----------|--------|-------|
| Binary tree automorphisms | S₂ ≀ S₂ ≀ S₂ | 48 |
| Tree block action at depth 2 | S₂ ≀ S₂ | 8 |
| Traditional trigram symmetry | S₄ | 24 |
| Affine group on Z₂³ | AGL(3,2) | 1344 |

**Key findings:**

- **0 of 48 tree labelings** (6 bit orderings × 8 flip conventions) reproduce the S₄ block system. Tree siblings have Hamming distance 1; S₄ blocks include complement pairs at distance 3. The structures are incompatible.

- **The traditional S₄ is non-affine.** AGL(3,2) contains 280 S₄ subgroups, but the traditional one is not among them. ι₂ (KW diameters) is not an affine map on Z₂³. The binary algebraic structure and the S₄ structure are genuinely independent — they share only the carrier set.

- **S₄ is the plurality outcome among random FPF triples** (26.9%, or 50,400 of 187,460 unordered triples), but far from forced. PSL(2,7) is close behind at 25.1%.

### Step 4: Three FPF Involutions → S₄

**Classification: FORCED (given the axioms).**

The two axioms from the invariant characterization:
- **Axiom 1 (Overlap):** Sorted pair-overlap vector = (0, 0, 1)
- **Axiom 2 (Commutation):** The pair sharing no pairs with the others has product of order 2

**Results (exhaustive enumeration over all 187,460 triples):**
- 20,160 ordered triples satisfy both axioms
- **100% generate S₄** — zero false positives
- Each passing triple admits exactly **1 valid role assignment** (ι₁, ι₂, ι₃ are uniquely determined by the axioms)

The axioms don't just constrain to S₄ — they perfectly select it with no ambiguity in the labeling.

### Step 5: S₄ → H via 互卦

**Classification: FORCED (given outer-pair erasure).**

The nuclear hexagram 互(h) = (L2, L3, L4, L3, L4, L5) erases the outer pair and doubles the inner. This determines:

- **ker(互) = {id, O}** — only the outer-pair operation is invisible
- **H = {id, O, MI, OMI} = ker(互) × ⟨MI⟩** — elements acting simply (as identity or complement) on 互-space
- **H-projection theorem:** every 互卦 has its mirror-pair kernel in H (algebraic necessity: kernel(互) = (M_本, I_本, I_本), and since M-bit = I-bit, it's always in H)

### Step 6: H → Sequence/Divination Coherence

**Classification: FORCED.**

Once 互 is defined and H = {id, O, MI, OMI} is its algebraic consequence:
- The Upper Canon sequence preferentially transitions through H (64.5%, 96.7th percentile)
- 互 destroys 生 (×0.33) and amplifies 克 (×1.54) — the nuclear hexagram is structurally biased toward adversarial dynamics
- 体 is absolutely preserved through 变 (100%, trivial by construction)

The sequence and the divination operation privilege the same subgroup — one probabilistically, the other deterministically.

---

## 3. The Choice Points

### Choice Point 1: FPF Involutions as Generators

**Status: FORCED (minimum = 3).**

If symmetries are to be complete pairings (every element has a partner, none maps to itself), you need fixed-point-free involutions. Two FPF involutions cannot generate S₄ — verified exhaustively: 0 of the 36 pairs within the traditional S₄ suffice (all generate groups of order ≤ 8). Three is the exact minimum.

This S₄ has 9 FPF involutions among its 24 elements. The remaining 15 elements have types: 8 elements of type (3,3,1,1) with fixed points, 6 elements of type (4,4) that are order-4 (not involutions).

52 minimal FPF-generating triples exist within the traditional S₄. The traditional triple {ι₁, ι₂, ι₃} has sub-pair orders {4, 6, 8} with V₄ emerging from the commuting pair ⟨ι₂, ι₃⟩. Whether this is uniquely distinguished among the 52 remains the one open question (see §7).

### Choice Point 2: Rep A vs Rep B

**Status: FORCED (one predicate).**

There are exactly two non-conjugate representations of S₄ acting faithfully on 8 points with a block system of 4 × 2:

| Property | Rep A | Rep B |
|----------|-------|-------|
| Overlap patterns | (0,0,1), (0,1,1) | (1,1,1), (1,1,2) |
| V₄ elements | All FPF: type (2,2,2,2) | Have fixed points: type (2,2,1,1,1,1) |
| 4-cycles | Type (4,4) — FPF | Type (4,2,1,1) — have fixed points |
| S₄ reliability | 50% of (0,0,1) triples | 100% of (1,1,2) triples |

The FPF axiom on commuting pairs eliminates Rep B entirely:
- Rep A commuting pairs have overlap 0 → pattern includes (0,0,1) ✓
- Rep B commuting pairs have overlap 2 → pattern includes (0,0,2) ✗

One predicate, binary fork, one survivor.

**The V₄ substructure split:** Among the 1,260 V₄ subgroups of FPF involution pairs, exactly two classes exist:
- **Class A** (630 V₄s, overlap = 0): 48 S₄ extensions each, 32 satisfy both axioms (ratio 2/3). These contain the traditional structure.
- **Class B** (630 V₄s, overlap = 2): 8 S₄ extensions each, 0 satisfy the axioms. These are the Rep B V₄s.

### Choice Point 3: The Nuclear Operation (互)

**Status: FORCED (by outer-pair erasure / line adjacency).**

Three consecutive-window nuclear operations exist (start at L1, L2, or L3). Each produces a different algebraic signature:

| Window | Kernel | H-like subgroup | Idempotent |
|--------|--------|-----------------|------------|
| L1–L4 | {id} (trivial) | {id, OMI} | No |
| **L2–L5** | **{id, O}** | **{id, O, MI, OMI}** | **No** |
| L3–L6 | {id} (trivial) | {id, OMI} | No |

Only L2–L5 (traditional 互):
1. Has a non-trivial kernel — the outer-pair operation O is invisible
2. Produces the full H = {id, O, MI, OMI}
3. Is the unique 4-line window with kernel = {id, O} among all C(6,4) = 15 windows

The nuclear operation is determined by: "erase the outermost positional pair." This is the simplest geometric description, and the only one that makes a full palindromic position invisible.

---

## 4. The Minimal Input Set

Four non-redundant inputs generate everything:

| # | Input | Type | What it determines |
|---|-------|------|--------------------|
| 1 | Binary lines (yin/yang) | **Object** | Z₂ⁿ recursion → 8 trigrams, 64 hexagrams |
| 2 | Symmetries are FPF involutions | **Symmetry** | Generator count = 3 (forced minimum) |
| 3 | FPF extends to commuting pairs | **Symmetry** | Selects Rep A, kills Rep B |
| 4 | Outer-pair erasure (line adjacency) | **Operation** | Selects 互, determines H = {id,O,MI,OMI} |

**Minimality proof:** Remove any one and the derivation fails:
- Without 1: no object.
- Without 2: S₄ is not selected (infinitely many groups act on 8 elements; S₄ is a plurality but not forced).
- Without 3: Rep B survives — binary structural ambiguity.
- Without 4: three nuclear operations remain — three different H subgroups.

No input implies another. No input is redundant.

---

## 5. Alternative Structures

### At Step 3 (the broken bridge): What if you stay in Z₂³?

Without the S₄ axioms, the natural symmetry group on 8 trigrams is Aut(Z₂³) = GL(3,2), order 168. This gives PSL(2,7), the simple group — rich symmetry but no block decomposition, no distinguished involutions, no pairing structure. The I Ching's specific relational architecture (three pairings, four blocks, V₄ normal subgroup) does not exist here.

### At Choice Point 2: What if Rep B?

Rep B gives S₄ on 8 points where the V₄ normal subgroup has fixed points. FPF involutions exist but are all in the outer coset — they cannot commute with disjoint pairs. This breaks the axiom system: no (0,0,1) overlap pattern is achievable, no clean role assignment is possible. The system would lack the {id, O, MI, OMI} subgroup and the M-I lock that connects to divination.

### At Choice Point 3: What if a different nuclear operation?

| Alternative | Result |
|------------|---------|
| Erase inner pair (L3,L4) | Kernel = {id, I}. H-like = {id, I, OM, OMI}. Different subgroup, no O-invisibility. |
| Erase middle pair (L2,L5) | Kernel = {id, M}. H-like = {id, M, OI, OMI}. Different subgroup, no O-invisibility. |
| Non-consecutive window | Trivial kernel ({id} only). H-like = {id, OMI} at best. Strictly less structure. |

Each erasure choice produces a different Klein four-group inside Z₂³. The traditional choice (erase outer) is the only one that erases the pair corresponding to the *outermost* positional layer of the hexagram — the boundary between the hexagram and its environment.

---

## 6. Connection to 太极→两仪→四象→八卦

The traditional cosmogonic sequence describes the **object construction**: 1 → 2 → 4 → 8 → 64. This is pure Z₂ recursion and is complete as stated. Each step is the unique binary product. The tradition gets this exactly right.

What the tradition does NOT make explicit is that the **symmetry** (S₄) is not a continuation of the doubling. The 太极 sequence builds the *carrier set*. The three pairing systems (Fu Xi complement, KW diameters, He Tu differ-by-5) impose a *separate structure* on that set. These are two independent origins meeting on common ground.

The 四象 (four images) at depth 2 are traditionally {太阳, 少阴, 少阳, 太阴} — named, but the naming is external. The binary tree gives them S₂ ≀ S₂ symmetry (order 8). To get S₄ (order 24), you need the three involution axioms, which have no source in the recursion.

**The cosmogonic sequence is the first half of the derivation.** The second half — three pairings, their axioms, their S₄ — is architecture, not cosmogony.

---

## 7. What This Means

### How much is mathematics?

**Everything downstream of the four inputs.** Given the inputs, the group S₄, its unique representation, the kernel H, the divination circuit's algebraic properties, and the coherence between sequence and operation all follow by mathematical necessity. No further choices are available. The constraints are "just barely sufficient" — at every fork the alternative space is minimal (0, 2, or 3 options) and a single predicate collapses it. No constraint is redundant, no constraint is insufficient.

### How much is design?

**The four inputs themselves.** Someone chose:
1. To work with binary lines
2. To require pairings without fixed points
3. To extend that requirement to commuting pairs
4. To define the nuclear hexagram by outer-pair erasure

These are elegant choices — minimal, non-redundant, each targeting a small alternative space. But they are choices. The analysis can verify their consequences but not explain why *these* inputs rather than others.

### How much is cosmology?

**The cohabitation itself.** Two algebraically independent structures — Z₂³ (from recursive doubling) and S₄ (from involution axioms) — share the same 8-element set without any structural relationship between them. That they *fit* — that S₄ acts faithfully on 8 points by FPF involutions with the right block structure — is a fact about S₄'s representation theory. It is neither forced by the doubling nor explained by the axioms. It is the ground on which the two structures meet.

The 互卦 operation is the bridge: it lives in the geometry of 6-bit strings (the object, from doubling) but its kernel H lives in the symmetry landscape (from the axioms). The nuclear hexagram connects what the doubling built to what the axioms constrain. Whether this connection is discovery or design is the question the structural analysis cannot answer.

### What remains open

1. ~~**The 52-triple question.**~~ **Resolved.** 52 minimal triples split into 4 classes by overlap × sub-pair order signature: (0,0,1)/{2,3,4} (24 triples), (0,0,1)/{3,4,4} (12), (0,1,1)/{2,3,3} (12), (1,1,1)/{3,3,3} (4). The traditional class (24 triples, overlap (0,0,1), commutation, orders {2,3,4}) forms exactly **1 conjugacy class** — all related by relabeling of elements. The traditional triple is unique up to symmetry. The derivation chain closes completely: given the four minimal inputs, no residual freedom exists at the generator level.

2. **Why FPF involutions?** The weakening analysis resolves this structurally, if not mathematically. FPF means every element has a partner — categorical completeness. No orphans, no spectators, no inert elements. Drop FPF and blocks become ragged, the partition incomplete, the interpretive apparatus (体/用, 生/克) breaks. In Rep A, complementarity is generative: 63% of the group is FPF, not just the three generators. The principle pervades the algebra. The axiom is the minimal philosophical commitment — universal complementarity — with maximal structural yield. Everything downstream (S₄, the bridge, H, the divination coherence) follows from this single assertion. It is not derivable from mathematics. It is the design input that says the universe has no spectators.

3. ~~**The polarity partition.**~~ **Fully resolved.** The polarity requires no external input. It is forced by the interaction of Z₂³ and S₄: P₋ = {blocks containing a binary extreme (000=Kun or 111=Qian)}. The chain: (a) Z₂³ distinguishes 000 and 111 as extremes, (b) ι₁ pairs them (complement), (c) ι₁ maps between blocks so they're in different blocks, (d) the overlap block {010,101} contains neither extreme, (e) exactly 2 of 4 blocks contain an extreme → the traditional 2+2 polarity split. The Lo Shu magic square agrees (odd numbers = P₊ blocks, even = P₋) and adds geometric information (alternating parity on the octagon), but the partition itself is derivable from the four minimal inputs alone. This reduces the open questions by one and confirms the minimal input set is truly minimal.

---

## 8. Weakening Analysis (post-hoc)

Exhaustive enumeration of all 187,460 FPF triples on 8 elements. Full results in `weakening-findings.md`.

**Two involutions can't reach S₄.** Maximum group from 2 FPF involutions is order 8 (D₄). Three is the exact minimum.

**Two paths to pure S₄ exist:**
- **Rep A:** overlap (0,0,1) + commutation → 20,160 triples, 100% S₄. Sparse — one bridge pair (Kan↔Li), one mediator (ι₂).
- **Rep B:** overlap (1,1,2) alone → 5,040 triples, 100% S₄. Dense — every pair of involutions overlaps, no distinguished axis.

The tradition chose Rep A. Two reasons emerge from the weakening analysis:

1. **Bridge structure.** Rep A has overlap (0,0,1) — one shared pair (Kan↔Li) creating a bridge where ι₂ (Lo Shu/KW) mediates between ι₁ (Fu Xi) and ι₃ (He Tu). Rep B has overlap (1,1,2) — every pair of involutions overlaps, no distinguished axis, no mediator.

2. **Deep complementarity.** In Rep A, 63% of the group's 24 elements are FPF — the "everything has an opposite" principle propagates from the three generator involutions through their compositions. In Rep B, only 25% are FPF — complementarity holds at the generator level but breaks down under composition. The 4-cycles in Rep A have type (4,4), all FPF. In Rep B they have type (4,2,1,1), leaving 2 elements untouched. Rep A: the axiom is generative. Rep B: the axiom is skin-deep.

**FPF is load-bearing:** with fixed points, groups can reach order 40,320 (S₈). FPF bounds the maximum at 168 (PSL(2,7)) and forces the 4-block decomposition. Not aesthetic — structural.

**Commutation is a perfect selector:** among (0,0,1) triples, commutation eliminates all non-S₄ groups (PSL(2,7), order-48) and all Rep B realizations. 100% precision, zero false positives.

---

## Data

Scripts: `doubles/s4_derivation_test.py`, `doubles/s4_gap_analysis.py`, `doubles/choice_generators.py`, `doubles/choice_overlap.py`, `doubles/choice_nuclear.py`, `doubles/weakening_analysis.py`.

Dependencies: `opposition-theory/phase4/cycle_algebra.py`, `kingwen/sequence.py`.

Prior results: `spaceprobe/invariants.md` (two-axiom characterization), `spaceprobe/lead3/findings.md` (H-projection theorem, 克 amplification), `spaceprobe/synthesis.md` (full investigation synthesis).
