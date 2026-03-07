# Open Questions

## 0. The interpretation problem: what does the algebra model?

The algebraic characterization is extensive — basins, projections, 五行 coordinates, shell/core duality, convergence dynamics. But algebra describes *what the structure is*, not *what it's for*. The central open question: what does this structure represent?

### What we have (interpretive fragments):

- **Convergence = what can't change.** 互 strips transient surface, reveals persistent core. Basin type = type of persistence: rest (fixed point) or irresolution (cycle). 梅花 reads this temporally (now → hidden → outcome).
- **克 dominates convergence, 生 only in transit.** Resolution requires destruction (Wood intrudes at every fixed-point approach). Irresolution is self-sustaining (Fire↔Water mutual 克). "Creation is a process, never a destination."
- **Interface homogeneity = harmony.** I=0 (trigrams agree at boundary) → 生. I=1 (disagree) → 克. Structural agreement at the seam predicts interaction quality.
- **Shell = being, core = becoming.** 火珠林 reads trigram identity (what it *is*). 梅花 reads convergence destination (what it *becomes*). Observable vs tangent vector.
- **Anti-phase breathing.** At every convergence step, one nuclear position generates while the other destroys. Never uniform — opposition is built into every transition.
- **Semantic embeddings correlate with algebra.** kwprobe showed traditional meanings track algebraic features (I-component predicts 生/克, reverse pairs have higher semantic similarity than complement pairs).

### What we don't have:

- **Hexagram semantics from algebra.** Can individual hexagram meanings be *derived* (not just correlated) from algebraic position? What makes 否 mean obstruction and 泰 mean peace, beyond upper/lower trigram identity?
- **Basin semantics.** What do Kun-basin, Qian-basin, and Cycle-basin situations look like in human experience? Types of problems? Types of outcomes? Types of processes?
- **Predictive embedding.** Can algebraic position *predict* the semantic embedding vector, not just correlate with it? This would close the algebra→meaning gap.
- **用神 algebra.** How does collapsing 5 六親 types → 1 signal type reshape the algebraic space? What structure survives the projection?
- **Descriptive vs notational.** Is the structure modeling something real about change and persistence (a physics of situations), or is it an algebraically coherent notation that humans project meaning onto? Can this distinction even be tested?
- **The 卦辭/爻辭 layer.** The traditional line texts and hexagram texts are the primary semantic content. Their relationship to the algebra is entirely unexplored. Are they consistent with algebraic predictions? Do they encode basin/kernel information in natural language?

This is the boundary between mathematics and meaning. Everything below is algebraic. Everything above is the question of what the algebra is *about*.

## 1. S₄ orbit boundaries vs 五行 coordinate lines

S₄ acts on Z₂³ via the three involutions (reverse, complement, reverse-complement), partitioning trigrams into orbits — structural equivalence classes. 五行 is a coordinate transformation: (parity, b₀, cosmological bit) → 5 element labels.

These are fundamentally different operations on the same space. S₄ orbits define what you *can't* distinguish. 五行 coordinates define what you *choose* to read.

**The question:** How do S₄ orbit boundaries interact with 五行 coordinate lines?

Specifically:
- Does the parity bit (b₀⊕b₁, layer 1 of 五行) align with or cut across S₄ orbits?
- Which S₄ elements preserve parity, and which break it?
- Parity-preserving S₄ elements would be "generative" (生-compatible), parity-breaking ones "destructive" (克-compatible) — does this hold?
- At the hexagram level, the three involutions have different semantic signatures (reverse: similarity 0.720, complement: 0.680 baseline). Does 五行 coordinate structure explain this gap?

**Known constraints:**
- Complement (flip all bits) breaks parity for half the trigrams: Kun(0)→Qian(1), Gen(0)→Xun(1), but Kan(1)→Li(1), Zhen(1)→Dui(0). Actually need to check systematically.
- Only Wood is closed under complement (Zhen↔Xun both Wood). All other elements cross boundaries.
- MI(五行, Complement pair) = 1.50/2.25 — complement predicts 67% of 五行, missing Earth/Metal distinction and Fire/Water split.

## 2. Temporal gating: dynamics and interaction between methods

The 2/5 seasonal ceiling is proven. What's unexplored is the *dynamics* of temporal gating and how the two methods' temporal structures interact.

### 2a. 梅花's temporal input — hexagram selection bias

梅花's 先天起卦 maps year/month/day/hour via modular arithmetic to (upper trigram, lower trigram, 動爻). This gates which hexagrams are *reachable* at a given moment.

- What is the distribution of accessible hexagrams per time slot? Uniform or structured?
- Does the modular arithmetic create temporal clusters (e.g. certain basins overrepresented in certain hours)?
- The 動爻 is (year+month+day+hour) mod 6 — this means 動爻 position cycles predictably. What's the period? How does it interact with basin structure?

### 2b. Joint temporal effect across methods

火珠林 gates the *reading* by season (旺相休囚死). 梅花 gates the *hexagram* by time (起卦 arithmetic). Applied to the same moment:

- Are the two gating mechanisms complementary or redundant?
- If 梅花 selects a hexagram whose 體 element is seasonally 旺, does 火珠林 applied to the same hexagram at the same time reinforce or contradict?
- Is there a temporal window where both methods' spotlights converge on the same region of the space?

### 2c. Day branch (日辰) fine structure

Probe 6 touches 日辰 gap-filling briefly (section 3) but only checks coverage counts. The day branch is a second temporal coordinate beyond season, cycling through 12 branches (→ 5 elements) on a daily basis.

- How does 日辰 interact with the 2/5 seasonal ceiling? Can the day branch promote a 囚/死 element to functional relevance?
- The 12-branch cycle has period 12 within the 5-season frame. What's the joint period? Which (season, day-branch) pairs maximize/minimize functional coverage?
- 火珠林 texts emphasize 日辰 as the "arbiter" (日辰為主) — is this because it breaks the seasonal ceiling in specific configurations?

### 2d. Spotlight dynamics over time

The 2/5 ceiling means only 2 elements are illuminated per season. As seasons rotate (Z₅ action), the spotlight sweeps through all 5 elements.

- What is the *autocorrelation* of the spotlight? Adjacent seasons share 0, 1, or 2 旺/相 elements — what's the pattern?
- Over a full 5-season cycle, each element is 旺 once and 相 once = 2/5 coverage per element. Is the sweep uniform or does the 生 cycle ordering create temporal clustering of related elements?
- For a fixed hexagram, how does its 六親 functional profile change across the 5 seasons? Is the trajectory through functional space structured (e.g. always the same sequence of which types activate)?

## 3. The 用神 projection — intentional filter as primary structure

The discrimination mechanism has three layers:

1. **Hexagram** → which 六親 types exist (structural filter, algebraic)
2. **Season/day** → which existing types are strong (temporal filter, algebraic)
3. **Question** → which type is signal (intentional filter, semantic)

Layers 1 and 2 are formalized. Layer 3 is not, yet it's arguably the primary projection — it collapses the 5-dimensional 六親 space to a 1-dimensional signal/noise split. Without it, the structural and temporal incompleteness has no meaning (a missing type only matters if it's the one you need).

### What's unexplored:

- **The 用神 mapping itself.** 火珠林 dedicates 30+ sections to mapping human concerns → 六親 types (marriage→妻財, litigation→官鬼, parents→父母, etc.). Is this mapping arbitrary or does it have internal structure? Do related concerns map to 生克-adjacent types?
- **Signal/noise partition statistics.** Given a 用神 choice, the hexagram's 6 lines split into signal (lines carrying that type) and noise (everything else). What's the expected signal line count? How does it vary by palace?
- **Interaction with incompleteness.** For each 用神, which palaces structurally lack it? The 飛伏 finding (probe 4) showed 兄弟 is most frequently absent (4/6 incomplete palaces). Does this mean questions mapped to 兄弟 are structurally harder to read? Do practitioners know this?
- **用神 × season interaction.** Each 用神 maps to exactly one element. That element is 旺 in exactly one season. So every question type has a "peak season" and a "dead season." Is this acknowledged in the tradition? Does 火珠林 text advise seasonal timing?
- **Comparison with 梅花's 體用.** 梅花 uses 體/用 (subject/object) rather than 用神. The 體用 split is determined by the 動爻 position (which trigram contains the moving line = 用). This is structurally determined, not chosen by the questioner. Two different approaches to the same problem: 火珠林 lets the question select the projection, 梅花 lets the hexagram select it.

## 4. Sheaf-theoretic structure of incompleteness

The structured incompleteness of 火珠林 (missing types, seasonal ceiling, 用神 collapse) has the shape of a presheaf with no global section. The obstruction is not accidental — it's cohomological.

### The presheaf

- **Base space:** Reading contexts. A context = (season, 用神) pair. 5 × 5 = 25 contexts per hexagram.
- **Stalk at each context:** The 六親 types that are both *present* in the hexagram AND *seasonally strong* (旺/相). This is the local observable — what's legible from this vantage.
- **Restriction maps:** Moving between contexts changes what's visible. Adjacent seasons share some active elements; different 用神 choices highlight different types.
- **Global section:** A simultaneous assignment of "strong and present" across all 25 contexts. Would mean "readable from every angle at once."

### The obstruction (proven)

No global section exists. Three independent contributions:

1. **Palace incompleteness** (probe 4): 6/8 palaces permanently missing 2 types. Topological — fixed by the hexagram's palace membership, immovable.
2. **Seasonal ceiling** (probe 6): ≤2/5 types strong at any season. Rotational — cycles through Z₅, forced by 六親→element bijection meeting pentacyclic 旺相休囚死.
3. **用神 projection** (question choice): collapses 5 types → 1 signal type. Intentional — chosen by the questioner, determines which absence matters.

### Quantum contextuality parallel

Abramsky-Brandenburger formalized quantum contextuality as the failure of a presheaf of measurement outcomes to admit a global section. Kochen-Specker: you can't assign definite values to all observables simultaneously. 火珠林 has the same shape — you can't assign "strong and present" to all 六親 types simultaneously. The obstacle is structural, not epistemic.

The analogy is precise:
| Quantum mechanics | 火珠林 |
|---|---|
| Observable | 六親 type |
| Measurement context | (season, 用神) pair |
| Outcome | strong/weak/absent |
| Global assignment (hidden variables) | All types simultaneously legible |
| Kochen-Specker obstruction | 2/5 ceiling + palace gaps |

### Computational proposal

**Compute H¹ of the presheaf.** For each hexagram:

1. Construct the 25-context presheaf: for each (season, 用神), the set of types that are present AND strong.
2. Check consistency on overlaps between contexts sharing a season or sharing a 用神.
3. Compute the first cohomology group — this quantifies *how much* local views fail to cohere.
4. Compare H¹ across palaces and basins. Does the Cycle basin (permanently conflicted) have higher cohomological obstruction than fixed-point basins?
5. Check whether H¹ varies with palace rank / 互 depth — does algebraic distance from the root predict the degree of contextuality?

**Expected outcome:** Non-trivial H¹, varying systematically with basin and palace structure. The cohomology would formalize what the sage identified: the system is a spotlight whose pattern of gaps carries structured information. The local sections *are* the content — the obstruction to gluing is what makes each reading specific to its context.

### Interpretive payoff

If incompleteness is cohomological:
- A hexagram isn't read once from a privileged viewpoint. It's read from multiple contexts, and the *variation* between readings is itself the message.
- The practitioner's skill isn't finding the "right" context — it's navigating the presheaf, understanding which local views are available and what their disagreements reveal.
- The sheaf doesn't need a global section. The structured failure of gluing is the diagnostic instrument. A system with a global section would be a lookup table, not a divination method.
