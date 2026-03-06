# Round 2: Corridor Arcs, Cyclical Boundaries, and Ordering Constraints

## Overview

This round tests three hypotheses about the relationship between corridor structure and the Xugua's narrative logic:

1. **Do cyclical-formula transitions mark corridor boundaries?** (Task A)
2. **Do corridors carry thematic content tied to their persistent trigram?** (Task B)
3. **How constrained is pair ordering by corridor structure?** (Task C)

The central finding: the corridor-cyclical alignment is **qualitatively structured but statistically modest**. The real finding is a clean partition of the sequence into two regimes — a corridor-rich region where cyclical formulas coincide with corridor structure, and a corridor-free zone where they don't — that maps onto the Upper Canon / Lower Canon divide.

---

## Task A: Cyclical Transitions × Corridor Boundaries

### Setup

The 8 cyclical-formula transitions from Round 1:

| T# | Bridge | Cyclical phrase |
|:--:|--------|----------------|
| T6 | Pi→Tong Ren | "Things cannot forever be at a standstill" |
| T11 | Bi(Grace)→Bo | "When adornment is carried to its limit" |
| T14 | Da Guo→Kan | "Things cannot remain in excess forever" |
| T16 | Heng→Dun | "Things cannot forever dwell in their place" |
| T17 | Da Zhuang→Jin | "Things cannot remain strong forever" |
| T21 | Yi→Guai | "Increase that doesn't cease must break through" |
| T23 | Sheng→Kun | "Ascending without cease necessarily leads to exhaustion" |
| T26 | Gen→Jian | "Things cannot remain stopped forever" |

### Corridor breathing pattern

Corridors occupy every-other-pair positions. Each corridor pair alternates with a non-corridor pair. This creates a "breathing" pattern of local exits (leaving the corridor temporarily) and re-entries (returning to it), plus a terminal exit (the final departure from the corridor).

**Earth corridor (P4, P6, P8, P10):**
```
T3: INITIAL ENTRY → P4 → T4: LOCAL EXIT
T5: RE-ENTRY      → P6 → T6: LOCAL EXIT      ← CYCLICAL ★
T7: RE-ENTRY      → P8 → T8: LOCAL EXIT
T9: RE-ENTRY      → P10 → T10: TERMINAL EXIT
```

**Heaven corridor (P1, P3, P5):**
```
(start)           → P1 → T1: LOCAL EXIT
T2: RE-ENTRY      → P3 → T3: LOCAL EXIT
T4: RE-ENTRY      → P5 → T5: TERMINAL EXIT
```

**Thunder/Mountain corridor (P9, P11):**
```
T8: INITIAL ENTRY → P9 → T9: LOCAL EXIT
T10: RE-ENTRY     → P11 → T11: TERMINAL EXIT  ← CYCLICAL ★
```

**Wind corridor (P14, P16):**
```
T13: INITIAL ENTRY → P14 → T14: LOCAL EXIT    ← CYCLICAL ★
T15: RE-ENTRY      → P16 → T16: TERMINAL EXIT ← CYCLICAL ★
```

**Lake/Wind corridor (P27, P29):**
```
T26: INITIAL ENTRY → P27 → T27: LOCAL EXIT    ← CYCLICAL ★ (at entry)
T28: RE-ENTRY      → P29 → T29: TERMINAL EXIT
```

### The critical table

| T# | Corridor relationship | Logic type | Xugua confidence |
|:--:|:---------------------|:----------:|:----------------:|
| T6 | LOCAL EXIT of Earth | Cyclical ★ | Direct |
| T11 | TERMINAL EXIT of Thunder/Mountain | Cyclical ★ | Direct |
| T14 | LOCAL EXIT of Wind | Cyclical ★ | Implied |
| T16 | TERMINAL EXIT of Wind | Cyclical ★ | Implied |
| T17 | No corridor contact | Cyclical | Implied |
| T21 | No corridor contact | Cyclical | Direct |
| T23 | No corridor contact | Cyclical | Direct |
| T26 | INITIAL ENTRY to Lake/Wind | Cyclical ★ | Implied |

### The partition

**Corridor-rich region** (P1–P16, P27–P29): Contains 5 of 8 cyclical transitions. **All 5 fall at corridor boundaries** — 4 at exits (T6, T11, T14, T16) and 1 at an entry (T26).

**Corridor-free zone** (P17–P26): Contains 3 of 8 cyclical transitions (T17, T21, T23). None have corridor contact — trivially, because there are no corridors in this region.

This is a clean partition: where corridors exist, cyclical transitions mark their edges. Where corridors don't exist, cyclical transitions appear freely.

### Statistical test

Within the corridor-rich region (20 transitions: T1–T16, T26–T29):
- 13 are corridor exit transitions (local or terminal)
- 5 are cyclical
- 4 cyclical transitions fall at exits
- Hypergeometric p(≥4) = 0.41

The enrichment is not statistically significant. The base rate of being at a corridor exit in the rich region is already 13/20 = 65%, so 4/5 = 80% is only modestly above expectation.

**However**: the pattern is qualitatively structured in a way the p-value misses. All 4 cyclical exit transitions fall at corridors that *actually exist*, and the 3 non-corridor cyclical transitions fall where corridors *don't exist*. The pattern is 100% consistent within each regime — it's the regime partition itself that's the finding, not a simple enrichment statistic.

### Converse: what logic types appear at corridor exits that are NOT cyclical?

| T# | Corridor exit type | Logic type | Notes |
|:--:|:------------------|:----------:|:------|
| T1 | Local exit of Heaven | Causal | Cosmogonic ("heaven and earth → things are born") |
| T3 | Local exit of Heaven | Causal | Escalation ("conflict → army") |
| T4 | Local exit of Earth | Causal | Compressed ("union → restraint") |
| T5 | Terminal exit of Heaven | Causal | Developmental ("proper conduct → peace") |
| T8 | Local exit of Earth | Causal | Compressed ("enthusiasm → following") |
| T9 | Local exit of Thunder/Mountain | Causal | Developmental ("work → greatness") |
| T10 | Terminal exit of Earth | Causal | Observation ("contemplating → joining") |
| T27 | Local exit of Lake/Wind | Causal | Settlement ("finding home → abundance") |
| T29 | Terminal exit of Lake/Wind | Causal | Dispersal ("joy → dispersal") |

**9 non-cyclical corridor exits — all causal.** The corridor exits that don't use the "cannot last forever" formula use direct causal chains instead. No other logic type (contrastive, analogical, temporal) appears at corridor exits.

### Entry transitions

| T# | Corridor entry type | Logic type | Notes |
|:--:|:-------------------|:----------:|:------|
| T3 | Initial entry to Earth | Causal | "conflict → army" |
| T8 | Initial entry to Thunder/Mountain | Causal | "enthusiasm → following" (Implied) |
| T13 | Initial entry to Wind | Causal | "accumulation → nourishment" |
| T26 | Initial entry to Lake/Wind | Cyclical ★ | "stillness cannot last → development" |

3 of 4 corridor entries are causal; 1 is cyclical. The single cyclical entry (T26) serves a special function: it marks the transition from the corridor-free zone (P17–P26) back into corridor structure (P27–P29). It's the **re-emergence** of corridor structure after the longest gap in the sequence.

### Assessment

**The sage's hypothesis is partially confirmed.** Cyclical transitions don't *always* fall at corridor boundaries, but they partition cleanly by regime:

1. **Where corridors exist**: cyclical = corridor boundary marker
2. **Where corridors don't exist**: cyclical = standalone phase-change marker

The cyclical formula serves the same function in both regimes — it marks the point where one state exhausts into another — but in the corridor-rich region, these exhaustion points coincide with the structural joints of the sequence's trigram architecture. This is not random, but it's not a strong statistical signal either. It's a **structural coincidence** that reflects the interleaving of narrative grammar and trigram geometry.

---

## Task B: Corridor Arc Thematic Readings

### Earth Corridor (P4, P6, P8, P10) — Rating: **Semantic Unit**

**P4: Shi/Bi** — Army/Holding Together
**P6: Tai/Pi** — Peace/Standstill
**P8: Qian(Mod)/Yu** — Modesty/Enthusiasm
**P10: Lin/Guan** — Approach/Contemplation

**The arc:** Collective mobilization (Army/Bonding) → the full cycle of collective flourishing and stagnation (Peace/Standstill) → the inner disposition needed to lead (Modesty/Enthusiasm) → the outward exercise of authority (Approach/Contemplation).

This is a developmental arc of **collective governance**:
1. First, people are organized and bonded (P4)
2. Then the collective achieves its fullest expression — and discovers its limits (P6)
3. The leader cultivates the right character (P8)
4. The leader exercises oversight from a position of maturity (P10)

**Earth's quality maps directly.** Earth ☷ = receptive ground, the social fabric, the collective body. Every pair in this corridor concerns collective/social themes: armies, alliances, peace-and-stagnation of the state, the leader's character, the contemplation of how things are governed. The persistent trigram is not an accident — it's the semantic throughline.

**Intervening pairs:**
- P5 (Xiao Chu/Lü: Small Taming/Treading) — individual discipline within the collective
- P7 (Tong Ren/Da You: Fellowship/Great Possession) — the harvest of collective action
- P9 (Sui/Gu: Following/Decay) — the dynamics of leadership and institutional decay

The intervening pairs describe **what happens on Earth's ground**: individual conduct (P5), shared prosperity (P7), the tensions of leadership succession (P9). The corridor provides the stage; the intervening pairs are the drama played upon it.

### Heaven Corridor (P1, P3, P5) — Rating: **Semantic Unit**

**P1: Qian/Kun** — Creative/Receptive
**P3: Xu/Song** — Waiting/Conflict
**P5: Xiao Chu/Lü** — Small Taming/Treading

**The arc:** Pure creative force (P1) → creative force meeting its first obstacle (P3: Waiting = Heaven below Water, Conflict = Water below Heaven) → creative force encountering social limitation (P5: Small Taming = Heaven below Wind, Treading = Lake below Heaven).

This is a developmental arc of **the creative principle encountering limitation**:
1. Undifferentiated creative power (P1)
2. The creative meets natural resistance — having to wait, having to contend (P3)
3. The creative meets social restraint — being tamed by gentle influence, learning to tread carefully (P5)

**Heaven's quality maps directly.** Heaven ☰ = creative force, initiative, the masculine principle. The arc traces how raw creative energy becomes civilized through successive encounters with constraint. Each pair shows Heaven in a different relationship to a limiting trigram (Water in P3, Wind/Lake in P5).

**Intervening pairs:**
- P2 (Zhun/Meng: Difficulty at the Beginning/Youthful Folly) — the birth process itself
- P4 (Shi/Bi: Army/Holding Together) — collective organization as the first social structure

P2 is what's being born from the Heaven-Earth ground; P4 is the first collective form that the creative principle requires.

**Note:** P5 belongs to both the Heaven corridor (Heaven as lower trigram in both hexagrams) and functions as the bridge between Heaven and Earth corridors. It is the hinge where creative force (Heaven corridor) yields to collective ground (Earth corridor). This dual membership is structurally meaningful.

### Thunder/Mountain Corridor (P9, P11) — Rating: **Suggestive**

**P9: Sui/Gu** — Following/Decay
**P11: Shi He/Bi(Grace)** — Biting Through/Grace

**The arc:** The dynamics of following a leader and the decay that follows (P9) → the response: decisive action to restore order (Biting Through) and the adornment of form (Grace) (P11).

**Thunder ☳ and Mountain ☶ map partially.** Thunder (arousing movement) appears as the lower trigram in Sui and Shi He — the initiating, moving force. Mountain (keeping still, form) appears as the upper trigram in Gu and Bi(Grace) — the constraining, structuring force. The corridor captures the dynamic of **action against form**: movement from below meets structure from above.

The thematic connection is present but looser than Earth or Heaven. P9's theme (leadership succession/institutional decay) connects to P11's theme (legal/aesthetic order) through the idea that decay requires either forceful remedy (Shi He) or beautiful form (Bi/Grace). But this is a thematic resonance, not a clean developmental arc.

**Intervening pair:**
- P10 (Lin/Guan: Approach/Contemplation) — the Earth corridor's final pair, the perspective of the overseer

Rating: **Suggestive.** The persistent trigram pair (Thunder-below/Mountain-above) carries a coherent dynamic (movement vs. stillness), but the thematic arc is more associative than developmental.

### Wind Corridor (P14, P16) — Rating: **Suggestive**

**P14: Yi/Da Guo** — Nourishment/Great Excess
**P16: Xian/Heng** — Influence/Duration

**The arc:** Nourishment and its excess (P14) → Influence and its persistence (P16). These are separated by P15 (Kan/Li), the canon boundary.

**Wind ☴ appears in specific positions:** Da Guo has Wind as lower trigram; Heng has Wind as upper trigram. Wind's quality (gentle penetration, the gradual) is thematically present in both pairs: nourishment is a gradual process (Yi), and duration is the persistence of what gently penetrates (Heng). But the connection is stretched — Xian (Influence/Attraction) doesn't obviously connect to Wind's quality.

The more striking feature: this corridor **spans the canon boundary**. P14 closes the Upper Canon's penultimate section; P16 opens the Lower Canon. The Wind corridor is the structural bridge between the two canons. Wind as "gentle penetration" is the quality that crosses the divide — the gradual, insinuating force that connects the cosmic order (Upper Canon) to the human order (Lower Canon).

**Intervening pair:**
- P15 (Kan/Li: Water/Fire) — the elemental completion of the Upper Canon

Rating: **Suggestive.** The canon-spanning position is structurally remarkable, but the thematic arc is more associative than developmental. The Wind quality (gradual penetration) resonates with both pairs but doesn't create a clean narrative thread.

### Lake/Wind Corridor (P27, P29) — Rating: **Semantic Unit**

**P27: Jian(Dev)/Gui Mei** — Development/Marrying Maiden
**P29: Xun/Dui** — Gentle Wind/Joyous Lake

**The arc:** Gradual development in relationship (Jian) and its sudden culmination in marriage (Gui Mei) → the elemental expression of these same forces: gentle penetration (Xun/Wind) and joyful openness (Dui/Lake).

**Lake ☱ and Wind ☴ map precisely.** These are the two constituent trigrams of both corridor pairs. P27 shows them in combination with Mountain and Thunder (the other non-palindromic trigram pair); P29 shows them in pure form — Wind doubled (Xun) and Lake doubled (Dui). The corridor traces **Lake and Wind from their social manifestation (courtship/marriage) to their elemental essence (gentle penetration and joyful exchange)**.

This is a remarkable structural-semantic alignment. The corridor's two pairs share the same four trigrams ({Mountain, Lake, Wind, Thunder} for P27; {Wind, Wind, Lake, Lake} for P29 — Wind and Lake have "won" and become the sole constituents). The thematic content tracks this: P27 is about the *process* of coming together (Development, Marriage); P29 is about the *qualities* that make coming-together possible (gentleness, joy).

**Intervening pair:**
- P28 (Feng/Lü: Abundance/Wanderer) — the apex and dispersal of what was gathered

P28 is what happens *between* the formation of the bond (P27) and the pure expression of its constituent qualities (P29): abundance peaks and then scatters, leaving only the essential qualities behind.

Rating: **Semantic Unit.** The trigram content and the thematic content are tightly coupled. The corridor traces Wind and Lake from relational process to elemental essence.

### Summary of corridor ratings

| Corridor | Rating | Quality of trigram-theme alignment |
|:---------|:------:|:----------------------------------|
| Earth (P4,P6,P8,P10) | **Semantic Unit** | Earth's receptive/collective quality directly maps to governance arc |
| Heaven (P1,P3,P5) | **Semantic Unit** | Heaven's creative force directly maps to limitation-encounter arc |
| Thunder/Mountain (P9,P11) | **Suggestive** | Movement-vs-stillness dynamic present but arc is associative |
| Wind (P14,P16) | **Suggestive** | Canon-spanning position is remarkable; Wind quality resonates but loosely |
| Lake/Wind (P27,P29) | **Semantic Unit** | Tight coupling of trigram content and relational-to-elemental progression |

**3 of 5 corridors are Semantic Units.** The two longest corridors (Earth, Heaven) and one short corridor (Lake/Wind) show clear thematic arcs tied to their persistent trigrams. The two Suggestive corridors (Thunder/Mountain, Wind) show trigram resonance without clean developmental arcs.

---

## Task C: Degrees of Freedom in Pair Ordering

### The computation

Each corridor constrains its member pairs to occupy positions at spacing exactly 2 (every other pair position). The question: how many of 32! pair orderings satisfy all five corridor constraints simultaneously?

**Corridor blocks:**
| Corridor | Length | Footprint width | Starting positions |
|:---------|:------:|:---------------:|:------------------:|
| Earth | 4 | 7 | 26 options (0–25) |
| Heaven | 3 | 5 | 28 options (0–27) |
| Thunder/Mountain | 2 | 3 | 30 options (0–29) |
| Wind | 2 | 3 | 30 options (0–29) |
| Lake/Wind | 2 | 3 | 30 options (0–29) |

**Method:** Exact enumeration of all non-overlapping placements of 5 corridor blocks in 32 positions. For each valid placement, the corridor pairs fill 13 positions and the 19 non-corridor pairs fill the remaining 19 positions freely.

### Results

| Quantity | Value |
|:---------|:------|
| Valid block placements | 3,768,480 |
| Internal corridor permutations | 4!·3!·2!·2!·2! = 1,152 |
| Free pair permutations | 19! ≈ 1.22 × 10¹⁷ |
| **Corridor-preserving orderings (any internal order)** | **≈ 5.28 × 10²⁶** |
| **Corridor-preserving orderings (KW internal order)** | **≈ 4.58 × 10²³** |
| Total orderings (32!) | ≈ 2.63 × 10³⁵ |

### Degrees of freedom

| Measure | Value |
|:--------|:------|
| Total freedom | log₂(32!) = 117.7 bits |
| Bits removed by corridors (any internal order) | **28.9 bits** |
| Bits removed by corridors (KW internal order) | **39.1 bits** |
| Remaining freedom (any order) | 88.8 bits |
| Remaining freedom (KW order) | 78.6 bits |

### Interpretation

**Corridors remove about 29 bits** of the 118-bit pair-ordering space (any internal order). This is substantial — about **one quarter** of the total freedom. But it leaves ~89 bits unconstrained, meaning the corridor structure alone determines only a fraction of the pair ordering.

The additional constraint of preserving KW's internal corridor order removes a further ~10 bits (the 1,152 internal permutations contribute log₂(1152) ≈ 10.2 bits). This represents the specific choice of *which* pair goes where within each corridor.

**What fills the remaining 89 bits?**
- 19 non-corridor pairs can go in any of 19! orderings (≈ 56.7 bits)
- 3,768,480 block placement options (≈ 21.8 bits)
- Internal corridor permutations (≈ 10.2 bits)

The non-corridor pairs account for most of the remaining freedom. The corridor block placement (where corridors are positioned in the sequence) accounts for ~22 bits — these are the choices about whether Earth comes early or late, whether corridors interleave or separate, etc.

### What this tells us about pair ordering

1. **Corridors are a real constraint but not the whole story.** They eliminate ~2 × 10⁹ orderings for every one they allow. But they still leave enormous freedom — the specific positions of 19 non-corridor pairs are essentially unconstrained by corridor structure.

2. **The corridor-free zone (P17–P26) is the least constrained region.** With no corridor pairs in this range, its 10 pairs could be in any internal order without violating corridor structure. If pair ordering has additional meaning-level logic, this zone is where it would be most visible.

3. **Block placement is a significant degree of freedom.** The ~3.8 million valid placements mean the sequence could look very different while preserving all corridor structures. KW's specific choice — Earth corridor early-to-mid, Heaven opening, corridors concentrated in Upper Canon — is one of millions of options. The concentration of corridors in the Upper Canon is itself a design choice, not a structural necessity.

---

## Synthesis: Are Corridors the Joints of the Narrative Skeleton?

### Three findings converge

**1. Cyclical transitions mark where corridors exhale.** In the corridor-rich region, every cyclical formula coincides with a corridor boundary. These are the points where one trigram-regime gives way to the next — Pi's stagnation exhausting the Earth corridor's local arc, Grace's overadornment exhausting the Thunder/Mountain corridor, etc. The Xugua's narrative grammar (the "cannot last forever" formula) is marking the same structural joints that the trigram architecture creates.

**2. Three corridors are semantic units.** Earth, Heaven, and Lake/Wind corridors carry developmental arcs whose thematic content is directly tied to the persistent trigram's quality. The corridors aren't just trigram statistics — they're meaning-carrying threads. The persistent trigram names the *domain* (collective governance, creative initiative, gentle-joyful relating), and the corridor's pairs trace an arc within that domain.

**3. Corridors leave substantial ordering freedom.** About 75% of the ordering space remains unconstrained by corridor structure. This means pair ordering is jointly determined by corridors (which constrain ~25% of the freedom) and some other principle(s) that govern the remaining choices — particularly the 19 non-corridor pairs and the corridor block placements.

### The emerging picture

The pair ordering has (at least) two layers:

**Layer 1: Corridor placement** (~29 bits). Which trigrams persist across the sequence, and where. This creates the structural skeleton — the domains (Earth=governance, Heaven=creation, Lake/Wind=relating) that organize the sequence into thematic zones.

**Layer 2: Non-corridor sequencing** (~89 bits). How the remaining pairs fill the gaps between corridor members, and how the corridors are positioned relative to each other. This is where the Xugua's causal chains operate — the hex-to-hex narrative logic that connects individual situations.

The cyclical-formula transitions are where these two layers *interface*. When a corridor's thematic domain has been exhausted, the Xugua marks the transition with "cannot last forever" — a narrative formula that also signals a structural shift in the trigram architecture. The two layers are coupled at their joints.

### What remains unclear

1. **What governs Layer 2?** The non-corridor pairs and corridor block placements have no known structural principle analogous to corridors. Is there a meaning-level account for why P17–P26 are in their specific order?

2. **Is the corridor-free zone differently structured?** P17–P26 contains the longest stretch without corridor structure. All three corridor-free cyclical transitions fall here (T17, T21, T23). Does this zone have its own organizing principle?

3. **Does the Upper Canon / Lower Canon divide reflect a shift in organizing logic?** The Upper Canon is corridor-rich (11 of 13 corridor pairs). The Lower Canon is almost corridor-free (only P27, P29). This suggests different structural regimes in the two halves — the Upper Canon is organized partly by trigram persistence, the Lower Canon mostly by narrative logic.

---

## Data Files

| File | Contents |
|:-----|:---------|
| `round2_constraints.py` | Exact enumeration of corridor-preserving orderings |
| `round2-corridors.md` | This document |
