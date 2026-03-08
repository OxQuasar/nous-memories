# Synthesis Findings

## Central Thread

Structure → incompleteness → curvature → specificity → meaning.

The hexagram system (Z₂⁶) supports exactly two primitive projections — shell (trigram pair) and core (nuclear overlap) — proven algebraically, confirmed historically. Two divination traditions (火珠林, 梅花) exhaust these projections. They are orthogonal instruments that cannot see each other's signals. The system creates structured incompleteness at every level — missing types, seasonal ceilings, rotating shadows — and this incompleteness is the mechanism of discrimination, not a defect.

One bridge connects the algebra to the oldest textual layer: 凶 (irreversible misfortune) maps to algebraic irreversibility (convergence to absorbing attractor). This is the single point where mathematical structure touches semantic content.

---

## 1. The Decisive Test: What the 卦辭/爻辭 Revealed

### Decision: MIXED — Layer-Dependent

The oldest textual layers of the I Ching partially encode algebraic structure, but only through a single narrow channel: the placement of 凶. All deeper algebraic constructs are invisible to the texts at the semantic level.

### Confirmed Results

**Embedding-space tests (A–D, G): All null.**
- Basin → 卦辭 embedding: no clustering (p=0.73)
- Palace → 卦辭 embedding: no clustering (p=0.49)
- I-component → 卦辭 embedding: no clustering (p=0.47)
- Kernel (O,M,I) → 卦辭 embedding: no effect (p=0.47)
- 互卦 pairing → semantic similarity: no signal, trend anti-correlated (Δ=−0.014, p=0.92)

The algebraic structure of the binary encoding does not predict what the judgment texts *say*.

**Valence × line position (Test E): Expected signal.**
- 吉 × line: p=0.0002; 凶 × line: p=0.0013; 无咎 × line: p=0.034; 厲 × line: p=0.047
- Line position carries valence meaning — well-known in the tradition (初=beginning, 上=excess, 二/五=central).

**凶 × algebraic coordinates: The standout bridge.**
- 凶 × basin: χ²=17.44, p=0.0002
- 凶 × I-component: χ²=16.22, p=0.0001
- Basin and I-component are **identical partitions** on Z₂⁶: I=0 ↔ {Kun, Qian} basins, I=1 ↔ Cycle basin
- **Direction**: Kun basin 20.8% 凶, Qian basin 20.8% 凶, Cycle basin **6.3%** 凶
- Fixed-point basins carry 3.3× the 凶 rate of the Cycle basin
- Effect persists after controlling for line position; strongest at outer positions (lines 1, 2, 6)
- 凶 is the **only** valence marker with basin significance; all others p>0.10

**Upper/lower trigram relation (Test H): Significant.**
- Kruskal-Wallis H=32.34, p<0.0001
- Hexagrams grouped by five-phase relation (比和, 生体, 体生用, 克体, 体克用) show different within-group semantic similarities
- This is a shallow algebraic feature — the trigram-pair relationship the tradition explicitly uses

**Additional textual layers:**
- 大象 (Image commentary): clusters by **palace** (p=0.027) — expected, since 大象 explicitly names trigram pairs
- 彖傳 (Judgment commentary): clusters by **basin** (p=0.045) — the structural commentary detects the I-bit partition
- 卦辭 semantic content: no clustering by any algebraic partition

### Interpretation

**The inversion.** The algebra says I=0 → 生 tendency → convergence to fixed points (pure stasis). The texts say I=0 → 凶. Danger is not where 克 (conflict) dominates, but where 生 (harmony) drives the system toward pure extremes. The process of losing dynamism — the approach to stasis — is where irreversible harm concentrates.

**Why only 凶?** 凶 is the only valence marker denoting irreversibility. All others (吉, 悔, 吝, 无咎, 厲) are navigational — they indicate states that can be worked with. The algebraic property of irreversibility (convergence to absorbing attractor) maps onto the textual property of irreversibility (凶). This structural correspondence explains the selectivity: reversible markers have no corresponding algebraic invariant in the basin structure.

**Three channels, one structure.** The I-bit partition surfaces through three independent channels:
1. 爻辭 凶 placement (~9th c. BC) — distributional encoding
2. 彖傳 semantic clustering (~5th-3rd c. BC) — structural commentary language
3. Algebraic basin partition (京房, ~1st c. BC) — formal mathematical structure

The 彖傳 likely propagates through trigram-relational language (structural channel), not by echoing 凶 counts — since the 卦辭 (equally downstream of 爻辭) doesn't cluster. The temporal separation (700+ years between 爻辭 and algebraic formalization) argues that the encoding predates the formalization.

**The tautology.** 易 means "change." The system marks the extinction of change (convergence to fixed point) as its deepest danger (凶). The algebraic and textual traditions agree: creation is a process, never a destination; arrival at stasis is where irreversible harm occurs.

### Depth Gradient — Confirmed

The 凶 rate within I=0 follows a non-monotonic depth gradient (χ²=8.63, p=0.013):

| Depth | Category | Hexagrams | 凶/total | Rate |
|-------|----------|-----------|----------|------|
| 0 | Attractors (乾 坤) | 2 | 0/12 | 0.000 |
| 1 | Penultimate (剝 復 頤 大過 夬 姤) | 6 | 13/36 | 0.361 |
| 2 | Deep I=0 | 24 | 27/144 | 0.188 |
| — | Cycle (I=1) | 32 | 12/192 | 0.063 |

**All three predictions confirmed:**
1. **Qian and Kun contain zero 凶** — the attractors themselves are beyond danger
2. **Depth-1 hexagrams carry the highest 凶 rate** (36.1%) — the penultimate moment before absorption is most dangerous
3. **Gradient shape 0% → 36% → 19% → 6%** — non-monotonic peak at the boundary layer

**Structural reading:** The attractors are not dangerous because they *are* stasis — danger is past. Depth-1 hexagrams are the boundary layer where absorption is imminent but not yet complete; every depth-1 hexagram has 凶 in at least one line (range: 1–3 of 6 lines). The six depth-1 hexagrams (剝 復 頤 大過 夬 姤) are traditionally recognized as liminal or extreme — the depth gradient confirms this is algebraically grounded, not merely interpretive convention.

---

## 2. The Curvature of the Reading Space

### The Orthogonality Wall (Probe 2)

The contextual obstruction measure (dark contexts where F=0 for a given season × 用神 pair) does not correlate with 凶. All three measures — n_zero, F_variance, F_total — fail to reach significance. But the *reason* they fail is the most important finding.

**F_total = 12 for all 64 hexagrams.** A conservation law: each line's element is 旺/相 in exactly 2 of 5 seasons, and each line belongs to exactly one 六親 type. So 6 lines × 2 seasons = 12 active slots, invariant across hexagrams.

**n_zero ∈ {15, 17, 19} with distribution 16:32:16.** This maps exactly to the number of missing 六親 types (0, 1, 2 missing types → 15, 17, 19 dark contexts). The 16:32:16 ratio matches the huozhulin finding that 16 hexagrams have 0 missing types, 32 have 1, 16 have 2.

**No correlation with 凶:**
- n_zero vs 凶: ρ=0.12, p=0.34
- F_variance vs 凶: ρ=−0.06, p=0.65
- n_zero by basin: H=2.95, p=0.23
- F_variance by basin: H=2.08, p=0.35

**The wall.** The null result is predicted by the 納甲 ⊥ 互卦 orthogonality discovered in the huozhulin workflow:

- **凶 lives in the inner bits** (b₂, b₃): basin, depth, I-component
- **六親 × 旺相 lives in the trigram pair** (outer projection): 納甲 assigns branch elements based on trigram identity, which reads bits [0:3] and [3:6] independently

These are **algebraically orthogonal projections** of Z₂⁶. No measure built from 六親 × seasonal strength can access basin/depth information, because the 火珠林 operational layer is structurally blind to the inner-bit dynamics that govern 凶 placement.

This confirms and extends the huozhulin finding: the two divination traditions (梅花 = inner-bit reader, 火珠林 = outer-bit reader) are not just different lenses on the same structure, they are **orthogonal instruments** that cannot see each other's signals.

### Three Sources of Curvature

The presheaf of reading contexts (season × 用神 × hexagram) has no global section. Three independent sources of curvature contribute:

1. **Palace incompleteness** = holes. 6/8 palaces permanently missing 2 of 5 六親 types. Topological defects — fixed by the hexagram, immovable.
2. **Seasonal ceiling** = torsion. The Z₅ 生克 cycle forces a width-2 window on a size-5 ring: exactly 2/5 elements strong at any time. Softened by 日辰 to 4/5 (see §4), but never eliminated.
3. **用神 projection** = dimensional reduction. The question collapses 5 六親 types → 1 signal type. Information loss depends on viewing angle.

**Scale dependence.** The obstruction is invisible at scale 1. One context = one clean reading. Curvature appears at larger scales: 2 seasons → 旺/相 windows don't align. 2 用神 types → signal for one question is noise for another. The inter-context disagreements *are* the structural content.

**The design question.** A flat system (H¹ = 0) gives the same answer from every angle — a lookup table. A curved system (H¹ ≠ 0) gives different answers from different angles — the *pattern of variation* across contexts is the reading. The structured gaps are what make the system discriminative. If all 5 六親 types were always present and strong, every reading says "everything is active" — zero bits of information. The curvature is the information channel.

### Structural Discoveries

1. **F_total conservation** (= 12): a previously unknown invariant arising from the double bijection (六親→element, season→2 active elements)
2. **n_zero is determined by missing-type count**: the 16:32:16 distribution of n_zero values is the same 1:2:1 binomial structure found in huozhulin Probe 3
3. **The seasonal system adds no hexagram-specific obstruction**: the "seasonal zeros" count is constant at 15 for all hexagrams with 0 missing types — the seasonal layer redistributes the 12 active slots but creates no differential opacity

---

## 3. Where Meaning Enters (用神/體用)

### The Discrimination Architecture

The discrimination mechanism has three layers:

1. **Hexagram** → which 六親 types exist (structural filter, algebraic) — **formalized**
2. **Season/day** → which existing types are strong (temporal filter, algebraic) — **formalized**
3. **Question** → which type is signal (intentional filter, semantic) — **now formalized** (Probe 3)

Layer 3 is the primary projection — it collapses the 5-dimensional 六親 space to a 1-dimensional signal/noise split. Without it, the structural and temporal incompleteness has no meaning (a missing type only matters if it's the one you need).

### The Querrent's Geometric Position

The querrent (兄弟 = self, same element as palace) sits on the 克 cycle between the two heaviest 用神 types:

```
官鬼(8) →克→ 兄弟(0) →克→ 父母(3) →克→ 妻財(7) →克→ 子孫(4) →克→ 官鬼
```

兄弟 has 0 domains — it is the **reference frame**, never the object of inquiry. You don't divine about yourself; you divine about what acts on you (官鬼), what you seek (妻財), what you tend (子孫), what shelters you (父母). The querrent is the excluded node: '破財之人，不為主、不為輔.'

官鬼 (8 domains) + 妻財 (7 domains) = 15/22 = 68% of all question domains.

### The Triad Formalization

Each 用神 operates within a diagnostic triad: auxiliary = σ⁻¹(X) (what generates the 用神 on the 六親 cycle), 忌神 = what 克s the 用神.

| 用神 | Domains | Auxiliary (σ⁻¹) | 忌神 (what 克s 用) |
|------|---------|-----------------|------------------|
| 官鬼 | 8 | 妻財 | 子孫 |
| 妻財 | 7 | 子孫 | 父母 |
| 子孫 | 4 | 兄弟 | 妻財 |
| 父母 | 3 | 官鬼 | 兄弟 |
| 兄弟 | 0 | 父母 | 官鬼 |

The triad (用神, auxiliary, 忌神) is the minimal diagnostic unit. Whether a hexagram provides a complete reading depends on which triad members are present.

### Structural Symmetry, Projective Asymmetry

**The temporal system is perfectly symmetric.** Every 用神 type is suppressed (囚/死) in exactly 2/5 of seasonal contexts and 克ed by 1/5 of daily elements. The 五行 cycle's Z₅ symmetry ensures no type is systematically favored or penalized temporally. This uniformity is algebraically necessary — each element occupies each strength level in exactly one season.

**ALL asymmetry enters through the 用神 projection.** The 8:7:4:3:0 domain weighting is where the system becomes non-uniform. This means: the structural space (Z₂⁶ algebra, palace incompleteness, seasonal rotation) treats all 六親 types equally. It is the mapping from human concerns to 六親 types that creates differential difficulty.

### Gen Palace as Darkest — The Structural Darkness Gradient

When a palace is missing a 六親 type, all question domains mapped to that type become structurally unreadable:

| Palace | Missing types | Domains affected | Fraction of 22 |
|--------|---------------|:----------------:|:--------------:|
| Gen ☶ | 妻財(7) + 官鬼(8) | 15 | **68%** |
| Zhen ☳ | 子孫(4) + 官鬼(8) | 12 | 55% |
| Li ☲ | 兄弟(0) + 妻財(7) | 7 | 32% |
| Dui ☱ / Xun ☴ | 兄弟(0) + 子孫(4) | 4 | 18% |
| Kan ☵ | 兄弟(0) + 父母(3) | 3 | 14% |
| Kun ☷ / Qian ☰ | — | 0 | 0% |

Gen ☶ (missing the two heaviest types) is structurally dark for 68% of domains. Palaces where 兄弟 is one of the missing types have effective darkness halved — 兄弟's absence costs nothing because it has 0 domains.

### The Triad Diagnostic Gradient

Of 256 (hexagram × 用神) diagnostic contexts:

| Category | Count | Fraction | Meaning |
|----------|------:|----------|---------|
| Full | 116 | 45.3% | Signal + support + threat all present |
| Exposed | 42 | 16.4% | Signal + threat, no support |
| Unguarded | 42 | 16.4% | Signal + support, no threat |
| Isolated | 5 | 2.0% | Signal only |
| Blind | 51 | 19.9% | Signal absent — structural impossibility |

The diagnostic environment is not binary (can/cannot read) but **graded**. 45% of contexts provide full diagnostic information; 20% are structurally impossible; 35% are degraded in specific ways. This gradient is the mechanism through which structural incompleteness becomes differential meaning — not by preventing readings entirely, but by controlling how much diagnostic context is available.

### 兄弟's Benign Absence

兄弟 is missing from 13/64 hexagrams (4 palaces) but has 0 domains — its absence never blocks a question. When paired with another missing type, it effectively halves the darkness. This makes the incompleteness less severe than it appears: roughly half the missing-pair combinations include the zero-weight type.

### 火珠林 vs 梅花: Who Selects the Projection?

火珠林 lets the **question** select the projection (用神). The 30+ domain sections are a **practitioner's atlas** mapping the presheaf curvature from the questioner's perspective. 梅花 lets the **hexagram** select the projection (體用) via the 動爻 position.

| | 梅花 | 火珠林 |
|---|---|---|
| **Projection** | Hexagram selects (體用) | Question selects (用神) |
| **Time** | Encodes into question | Encodes into resolution |
| **Reads** | Core (becoming) | Shell (being) |
| **Ceiling** | 2/5 (seasonal only) | 4/5 (seasonal + 日辰) |

### Practitioner Navigation

Skilled practitioners implicitly navigate the presheaf curvature:
- Knowing which season favors which question type (用神 × season alignment)
- Knowing when 日辰 overrides seasonal suppression (local patch switching)
- Knowing which palaces structurally lack which types (topology of holes)
- Advising *when* to ask certain questions (choosing favorable contexts)

---

## 4. The Ceiling and Its Escape

### Decision: POSITIVE — ceiling broken to 4/5 (theorem)

日辰 (daily branch, Z₁₂) breaks the 2/5 seasonal ceiling. The maximum number of simultaneously active 六親 types rises from 2 to 4. This is proven as a theorem, not just observed computationally.

### The 4/5 Ceiling Theorem

**Theorem.** In the joint (season × day-branch) system, at most 4 of 5 elements can be simultaneously promotable. This bound is tight.

**Proof.** The seasonal 旺/相 pair = {i, i+1} in the 生 cycle (Z₅). The day pair = {j, SHENG_MAP[j]} = {j, j+1}. Two consecutive pairs in Z₅ cover at most 4 of 5 nodes (2+2, with possible overlap). The maximum is achieved when the pairs are disjoint. ∎

**Which element is excluded?** At maximum coverage, the seasonal complement is {i+2, i+3, i+4}. The only disjoint day-pairs within this arc are {i+2, i+3} and {i+3, i+4}. Both include i+3 (= 囚, the overcomer of the season). The excluded element alternates between:
- **休** (i+2): the element that generated the season — the exhausted source
- **死** (i+4): the element the season overcomes — the conquered object

The system can illuminate everything except one form of the past: either what gave rise to the present (休), or what the present has already overcome (死). Opposition (囚) is always representable at maximum reach.

### Computational Results

Across 3840 (season × day-branch × hexagram) states:

| Active types | States | Fraction |
|-------------|--------|----------|
| 0/5 | 29 | 0.8% |
| 1/5 | 522 | 13.6% |
| 2/5 | 1711 | 44.6% |
| 3/5 | 1352 | 35.2% |
| 4/5 | 226 | 5.9% |

The modal outcome remains 2/5 (44.6%), but 41.1% of states exceed the old ceiling.

At element level (60 season × day-branch pairs): set size 2 in 20%, size 3 in 40%, size 4 in 40%. Day element falls outside seasonal 旺/相 in 60% of pairs.

### Cycle Basin Conflict Resolution

Fire AND Water simultaneously promotable in 16/60 (27%) of (season, day-branch) pairs. The "permanent internal conflict" of the Cycle basin attractors (Fire↔Water mutual 克) is partially resolved by 日辰 — in roughly a quarter of temporal contexts, both elements of the oscillating attractor are accessible.

### Pipeline Asymmetry

- **梅花** encodes time into *the question*: temporal input selects which hexagram is cast (先天起卦 modular arithmetic). Curvature is in the state space.
- **火珠林** encodes time into *the answer's resolution*: temporal input (日辰) selects which aspects of a fixed hexagram are visible. Curvature is in the observation space.

One curves the domain, the other curves the codomain. The 2/5 vs 4/5 difference is a consequence of this architectural difference, not an independent fact.

梅花 does NOT use 日辰 branch mechanisms (沖, 暗動, 日辰生). It inherits the 2/5 ceiling identically.

梅花 temporal distribution: all 64 hexagrams accessible (100%), but non-uniform (χ² = 481.8, df=63). Two frequency classes separated by ~2× factor.

### Orthogonality Wall — Untouched

日辰 enriches the shell (Z₅ → Z₁₂ resolution) but cannot bridge to the core. 納甲 assigns branches by reading trigram pairs; 日辰 operates on those branches. Both are shell-level. The 凶 signal (inner bits / basin / depth) remains invisible to the operational layer regardless of 日辰.

```
             Z₂⁶
            /    \
     Shell (trig pair)    Core (inner bits)
       ↓                    ↓
   納甲 → branches       互卦 → basins
       ↓                    ↓
   六親 × 旺相 × 日辰     凶 / depth
       ↓                    ↓
   2/5 ceiling            convergence
   (softened to 4/5)      (unreachable)
```

### Curvature Update

The three curvature sources are now better characterized:

1. **Palace incompleteness** (holes): unchanged by 日辰. Static, hexagram-determined.
2. **Seasonal ceiling** (torsion): softened from 3/5 shadow to 1/5 shadow by 日辰, but never eliminated. The residual 1/5 exclusion is the minimal aperture — **proven as theorem**.
3. **用神 projection** (dimensional reduction): unchanged. Question-determined.

日辰 reduces one source of curvature without touching the other two. The residual curvature is sufficient for discrimination: when the 用神's element is the one excluded element, the hexagram cannot answer that question in that temporal context. The probability of this "shadow hit" is 1/5 at maximum coverage. This rotating shadow — one element always dark, rotating with the day — is the mechanism's aperture, not its defect.

---

## 5. Symmetry and Semantics (S₄ × 五行)

### The Three-Layer Decomposition of 五行 (from wuxing workflow)

**Status: proven.** H(五行) = 2.2500 bits, decomposing as:

| Layer | Feature | Information | Type |
|-------|---------|------------|------|
| 1 | b₀⊕b₁ parity | 1.0000 bits | Algebraic (linear) |
| 2 | b₀ within parity-0 coset | 0.7500 bits | Algebraic (linear) |
| 3 | Complement pair choice in parity-1 coset | 0.5000 bits | Cosmological |

**Layer 1** separates {Earth, Metal} (stable) from {Wood, Fire, Water} (dynamic). This IS the I-component at trigram level — the same bit that governs 生/克 separation, basin membership, and 凶 placement.

**Layer 3** is the sole non-algebraic input: the choice to keep {Zhen, Xun} together as Wood (rather than {Kan, Li}). This choice is resolved by Later Heaven compass alignment. Traditional 五行 ranks top 1.2% (5th of 420 possible {2,2,2,1,1} partitions) for compass alignment while respecting elemental identity.

### Connection to the 凶 Bridge

The I-component (Probe 1's 凶×basin bridge) is Layer 1 of the 五行 decomposition. This means:

- **生-exclusive XOR masks** {011, 100} **preserve** b₀⊕b₁ parity
- **克-exclusive XOR masks** {010, 110} **break** b₀⊕b₁ parity
- I=0 (parity-homogeneous interface) → 生-dominated convergence → fixed-point basins → **high 凶**
- I=1 (parity-broken interface) → 克-dominated dynamics → Cycle basin → **low 凶**

The parity that separates 生 from 克 in the 五行 geometry is the same parity that separates high-凶 from low-凶 basins in the textual tradition. The algebraic mechanism (parity preservation/violation) and the textual signal (凶 concentration) are two readings of the same invariant.

### The Complement Anti-Automorphism (Probe 5)

**Status: proven.** The complement permutation π = (Earth↔Metal)(Fire↔Water)(Wood) conjugates the 生 cycle to its inverse:

**π ∘ σ ∘ π⁻¹ = σ⁻¹**

Verified for all 5 elements. Complement reverses all directed edges in the 五行 graph, yielding three consequences at the hexagram level:

- 比和 → 比和 (identity preserved)
- 生体 ↔ 体生用 (direction of generation reverses)
- 克体 ↔ 体克用 (direction of overcoming reverses)
- **The 比/生/克 category is always preserved** (0% category disruption across 32 complement pairs)

The complement₆ transition matrix is perfectly block-diagonal: complement swaps "who generates whom" but preserves *whether* generation or overcoming is occurring.

### Parity Preservation Under Complement — Hypothesis Corrected

**Complement preserves b₀⊕b₁ parity universally** (8/8 trigrams). This is algebraically necessary: XOR with 111 flips both b₀ and b₁, so b₀'⊕b₁' = (b₀⊕1)⊕(b₁⊕1) = b₀⊕b₁.

Complement belongs to the *shared* XOR mask vocabulary (used by both 生 and 克), not the 克-exclusive set. The 克-exclusive masks {010, 110} break parity by flipping exactly one of {b₀, b₁}. Complement flips both, canceling the effect. Reverse (b₀↔b₂ swap) is mixed: preserves parity only for palindromic trigrams (b₀=b₂).

| Involution | Parity preservation |
|-----------|-------------------|
| complement | **8/8** (universal) |
| reverse | 4/8 (palindromes only) |
| rev∘comp | 4/8 |

### The Semantic Gap — Concrete > Abstract

The kwprobe semantic gap (Tuan embeddings) across the three involutions:

| Involution | Semantic similarity | 比/生/克 category disruption | Element set disruption |
|-----------|:------------------:|:--------------------------:|:---------------------:|
| reverse₆ | 0.720 | 50% | 79% |
| complement₆ | 0.680 | **0%** | 78% |
| rev∘comp₆ | 0.673 | 50% | 100% |

Complement has the *lowest* category disruption (0%) but only *middle* semantic similarity. The Tuan perceives concrete identity over abstract relational structure. The semantic hierarchy is:

**Visual flip** (0.720) > **category-preserving element change** (0.680) > **full disruption** (0.673)

The gap between reverse and complement is the difference between concrete similarity (same hexagram shape, different orientation) and abstract structural analogy (same interaction type, different elements). This confirms the Layer 2→3 gap: algebra constrains but does not generate semantic content.

### Wood as Fixed Point and Cycle Conjugator

Wood is the unique element closed under complement (Zhen↔Xun both Wood). It is the fixed point of the anti-automorphism — the hinge where the 生 cycle reverses to 克. Wood intrudes into both fixed-point basins via the overlap's free bit, creating 克 friction at every convergence step. Without Wood, convergence would be frictionless. The cosmological choice to keep {Zhen, Xun} as one element preserves this bridge — the system needs Wood whole.

### MI Decomposition Corrected (Probe 5)

MI(五行, complement pair partition) = 1.500 bits (67%). The 0.750 bits lost is the **within-pair element identity** (Layer 2: Earth vs Metal in two pairs, Fire vs Water in one), **not** the cosmological choice (Layer 3, which is preserved — complement pairs distinguish {Zhen,Xun}=Wood from {Kan,Li}={Fire,Water}).

As a function (not partition), complement preserves ALL 五行 information: MI = 2.250 = H(五行). The complement is a perfect permutation on elements. The 1.500 of the pair partition reflects loss of *which member you are*, not structural degradation.

| Involution | Pair MI | Function MI | H(五行 \| partner) |
|-----------|:-------:|:----------:|:------------------:|
| complement | 1.500 | **2.250** | 0.000 |
| reverse | 1.750 | 1.500 | 0.750 |
| rev∘comp | 1.250 | 1.500 | 0.750 |

---

## 6. The Unified Picture: What Does the Hexagram System Model?

### The Instrument, Not the World

The hexagram system is not a model of the world. It is a model of the **constraints on observing** a 6-bit state under complementary projections with temporal modulation. Its structure answers the question: *what can you know, from what angle, at what time?*

### The Architecture

**State space:** Z₂⁶ — 64 hexagrams. The unique balanced factorization into 3+3 (trigram pairs) creates exactly two primitive projections:

1. **Shell** (trigram pair decomposition) → 納甲 → 六親 → 火珠林. Reads identity: what it *is*.
2. **Core** (nuclear overlap) → 互卦 → basins → 梅花. Reads convergence: what it *becomes*.

These are the only two, proven algebraically (closure theorem on Z₂⁶ with 3+3 factorization) and confirmed historically (Chinese sources classify hexagram divination into exactly these two methods).

**Orthogonality:** Shell and core are structurally blind to each other. The 火珠林 operational layer cannot see basin/depth/凶. The 梅花 核 projection cannot see 六親/seasonal strength. They are complementary instruments — each exhausts an independent subspace.

**Temporal modulation:** Time enters the two systems at different pipeline stages:
- 梅花 curves the domain: time selects which hexagram is cast
- 火珠林 curves the codomain: time (日辰) selects which aspects are visible

This creates structured incompleteness — the reading is specific to this hexagram, this question, this season, this day.

### The Curvature

Three independent sources of curvature prevent any single reading context from revealing the full hexagram:

| Source | Type | Mechanism | Modifiable? |
|--------|------|-----------|-------------|
| Palace incompleteness | Holes | 6/8 palaces lack 2/5 六親 types | No — hexagram-fixed |
| Seasonal ceiling | Torsion | Z₅ rotation forces width-2 window | Softened to 4/5 by 日辰 (theorem) |
| 用神 projection | Reduction | Question collapses 5→1 | No — question-fixed |

**用神 projection now quantified (Probe 3).** Of 256 (hexagram × 用神) contexts: 45.3% provide full diagnostics (triad complete), 19.9% are structurally blind (用神 absent), 34.8% are degraded (partial triad). The projection's asymmetric domain weighting (官鬼=8, 妻財=7, 子孫=4, 父母=3, 兄弟=0) concentrates practical impact: Gen palace is dark for 68% of question domains, while palaces with 兄弟 as a missing type have benign darkness.

The residual curvature (1/5 shadow after 日辰) is the minimal aperture: one element always dark, rotating with the day. The system can illuminate everything except one form of the past — either what gave rise to the present (休) or what the present has already overcome (死). Opposition (囚) is always representable.

### The Single Bridge to Meaning

The 凶×basin correlation is the one point where algebraic structure touches textual content:

- **Algebraic irreversibility** (convergence to absorbing attractor, I=0) → **textual irreversibility** (凶)
- **Algebraic dynamism** (oscillation, I=1) → **textual safety** (low 凶)
- The depth gradient peaks at the boundary layer: depth-1 hexagrams (one step from absorption) carry 36.1% 凶 — the penultimate moment is most dangerous

This bridge is narrow but deep. It connects across 700+ years of independent development (爻辭 ~9th c. BC → algebraic formalization ~1st c. BC). The I-bit partition surfaces through three independent channels: distributional encoding in the line texts, semantic clustering in the 彖傳, and formal mathematical structure in the 京房 palace system.

**The tautology at the heart:** 易 means "change." The system marks the extinction of change as its deepest danger. Algebraic and textual traditions agree: stasis is where irreversible harm occurs. Creation is a process, never a destination.

### Zero Free Parameters

The system has zero structural free parameters (proven in huozhulin workflow). The 乾/坤 position-split is uniquely determined by complement symmetry + fixed-point coherence. The closure to two systems is a theorem. The only genuine design information (1-2 bits) is in the 五行↔trigram element mapping, and even this is constrained to top 1.2% of possible partitions by compass alignment.

The system was discovered, not designed.

---

## 7. What Remains Open

### Resolved by this workflow

**Q1 (decisive test):** MIXED. The algebra is partially descriptive (凶×basin, trigram-relation clustering) but not fully — deeper constructs (kernel, 互卦, palace) don't predict textual semantics. The bridge is through irreversibility only.

**Q4 (breaking the ceiling):** POSITIVE. 日辰 breaks 2/5 → 4/5 (theorem). Orthogonality wall untouched. Pipeline asymmetry: 梅花 curves domain, 火珠林 curves codomain.

**Q2 (curvature):** PARTIALLY RESOLVED. Contextual obstruction measured — F_total = 12 conservation law, orthogonality wall confirmed. Formal H¹ computation not done but the structural picture is clear: three independent curvature sources, none eliminable, now characterized.

**Q5 (用神 mapping):** FORMALIZED. The 用神 projection is structured by the 六親 生/克 cycle. Auxiliary = σ⁻¹, 忌神 = 克-preimage. 兄弟 (self) excluded as reference frame with 0 domains. Domain weighting 8:7:4:3:0 creates differential darkness. Temporal treatment uniform (2/5 suppression). Triad diagnostic gradient: 45.3% full / 19.9% blind / 34.8% degraded. Gen palace darkest (68% of domains unreadable).

**Q6 (S₄ × 五行):** RESOLVED. Complement is an anti-automorphism of the 五行 cycle (π∘σ∘π⁻¹ = σ⁻¹). Preserves parity universally. Preserves 比/生/克 category (0% disruption). Semantic gap tracks concrete identity, not abstract relational structure. MI: 0.750 bits lost = within-pair identity (Layer 2), cosmological choice (Layer 3) preserved. Wood = fixed point of anti-automorphism.

### Still open

**H¹ computation.** All three curvature sources are now quantified. A formal H¹ computation would test whether curvature varies with basin, palace rank, or 互 depth. Lower priority given the orthogonality wall — the shell-layer presheaf cannot see core-layer dynamics.

**Is the curvature optimized?** Does the specific combination of Z₅ torsion + palace holes + 用神 projection maximize discriminative power for some natural measure? Or is any nonzero curvature sufficient?

**Cycle basin's updated epistemological status.** Previously "permanently conflicted" (Fire↔Water never simultaneously strong). Now "usually conflicted, resolved 27% of the time by 日辰." Does this change the relative difficulty of reading Cycle-basin hexagrams in practice?

**The 納甲 modification.** 京氏易傳 uses universal upper trigram offset +3 (63/63 match). 火珠林 modified to 乾/坤-only, gaining one unique 六親 word (58→59/64). When and why did this modification occur?

---

## Epistemic Status

| Category | Claims | Status |
|----------|--------|--------|
| **Proven** | 4/5 ceiling theorem; shell⊥core orthogonality; F_total=12 conservation; closure to two systems; zero free parameters; 3+3 factorization uniqueness; 五行 three-layer decomposition; basin=I-component identity; complement anti-automorphism (π∘σ∘π⁻¹=σ⁻¹); parity preservation under complement; 用神 temporal symmetry (2/5 suppression uniform) | Exact computation or theorem over finite structures |
| **Measured** | 凶×basin (p=0.0002); depth gradient (p=0.013); 彖傳×basin clustering (p=0.045); 大象×palace clustering (p=0.027); embedding null results (all p>0.4); 梅花 χ²=481.8 non-uniformity; triad diagnostic gradient (45.3% full / 19.9% blind / 34.8% degraded); Gen palace 68% darkness; domain-weighted blindness equalization (官鬼=80, 子孫=84, 妻財=77, 父母=27) | Statistical tests or exact computation on textual/structural data |
| **Structural interpretation** | "Irreversibility maps irreversibility"; "curvature is the information channel"; "rotating shadow is mechanism not defect"; pipeline asymmetry framing; "querrent as excluded reference frame"; "concrete > abstract in Tuan semantics"; "Wood as hinge of 生↔克 conjugation" | Pattern descriptions of proven facts — interpretive framing suggested, not proven |
| **Conjectured** | Curvature is optimized | Consistent with findings but not tested |

---

*Scripts: `01_decisive_test.py`, `02_probe1b_dissect.py`, `02b_depth_gradient.py`, `03_presheaf_h1.py`, `04_ceiling_break.py`, `05_s4_wuxing.py`, `05_yongshen.py`*
*Data: `embeddings.npz` (guaci, yaoci, daxiang, tuan embeddings)*
*Raw results: `probe1_results.md`, `probe1b_results.md`, `probe2_results.md`, `probe3_results.md`, `probe4_results.md`, `probe5_results.md`*
*Cross-references: huozhulin/findings.md, wuxing/summary_findings.md, jingshiyizhuan/findings.md*
