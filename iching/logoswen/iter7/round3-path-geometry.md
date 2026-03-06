# Round 3: Path Geometry

## Overview

Rounds 1–2 examined local structure (pairs, bridges). This round maps the *global* geometry of the KW path through the 8×8 trigram-pair grid. The central finding: **the path has a significant lag-4 periodicity (p = 0.0017) — every second pair tends to share a trigram.** This creates "corridors" of partial trigram continuity spanning multiple pairs, most prominently the Earth corridor (positions 7–20) and the Heaven corridor (positions 1–9). Everything else — row/column coverage, return times, autocorrelation at other lags — is statistically unremarkable.

---

## Task A: Row and Column Coverage Balance

### Row coverage (lower trigram)

Each lower trigram appears in exactly 8 hexagrams. Their mean sequence positions:

| Lower trigram | Positions | Mean | StdDev | z-score |
|--------------|-----------|:----:|:------:|:-------:|
| Heaven ☰ | 1,5,9,11,14,26,34,43 | **17.9** | 13.9 | **−2.24** |
| Earth ☷ | 2,8,12,16,20,23,35,45 | **20.1** | 13.3 | −1.89 |
| Water ☵ | 4,6,7,29,40,47,59,64 | 32.0 | 22.7 | −0.08 |
| Thunder ☳ | 3,17,21,24,25,27,42,51 | 26.2 | 13.8 | −0.96 |
| Fire ☲ | 13,22,30,36,37,49,55,63 | 38.1 | 15.8 | +0.86 |
| Wind ☴ | 18,28,32,44,46,48,50,57 | 40.4 | 12.2 | +1.21 |
| Lake ☱ | 10,19,38,41,54,58,60,61 | 42.6 | 18.2 | +1.55 |
| Mountain ☶ | 15,31,33,39,52,53,56,62 | 42.6 | 14.8 | +1.55 |

**Heaven as lower trigram is significantly early** (z = −2.24, mean position 17.9 vs expected 32.5). Earth is also early (z = −1.89, marginal). Mountain and Lake are late. This reflects the traditional canon structure: the sequence opens with Heaven and Earth hexagrams and moves toward the "younger" trigrams.

### Column coverage (upper trigram)

| Upper trigram | Positions | Mean | z-score |
|--------------|-----------|:----:|:-------:|
| Heaven ☰ | 1,6,10,12,13,25,33,44 | **18.0** | **−2.22** |
| Earth ☷ | 2,7,11,15,19,24,36,46 | **20.0** | −1.91 |
| Mountain ☶ | 4,18,22,23,26,27,41,52 | 26.6 | −0.90 |
| Water ☵ | 3,5,8,29,39,48,60,63 | 31.9 | −0.10 |
| Fire ☲ | 14,21,30,35,38,50,56,64 | 38.5 | +0.92 |
| Lake ☱ | 17,28,31,43,45,47,49,58 | 39.8 | +1.11 |
| Wind ☴ | 9,20,37,42,53,57,59,61 | 42.2 | +1.49 |
| Thunder ☳ | 16,32,34,40,51,54,55,62 | 43.0 | +1.61 |

Same pattern: **Heaven and Earth as upper trigram appear early** (z = −2.22 and −1.91), Thunder and Wind appear late. The column pattern mirrors the row pattern — Heaven and Earth dominate the first half of the sequence, the "children" trigrams dominate the second half.

### Range significance

Row mean range: 24.8. Column mean range: 25.0. Against random permutations (10,000 trials), these ranges are at p ≈ 0.12 — suggestive but not individually significant. The consistency between rows and columns (both show the same early-Heaven/Earth pattern) strengthens the reading.

**Assessment: The early concentration of Heaven and Earth is the well-known Upper Canon / Lower Canon division.** The Upper Canon (pairs 1–15, hex 1–30) contains the "senior" trigrams; the Lower Canon (pairs 16–32, hex 31–64) emphasizes "junior" trigrams. This is traditional and expected. Not a new finding, but confirms the trigram frame sees the canon structure.

---

## Task B: Return Times

### Return time statistics

Return time = gap between consecutive visits to cells with the same lower (or upper) trigram.

| Metric | Lower trigram | Upper trigram |
|--------|:---:|:---:|
| Mean return | 6.79 | 6.86 |
| Median return | 6.0 | 5.0 |
| StdDev | 4.91 | 4.71 |
| Min return | 1 | 1 |
| Max return | 22 | 21 |
| Expected (balanced) | 8.0 | 8.0 |

The mean return is below the balanced expectation of 8.0 (because short returns are more frequent than long returns in any permutation — a known statistical effect). 

### Short returns

Short returns (≤2 steps): lower = 13/56, upper = 12/56.
Null expectation: 13.2 for each. **Not significant** (p = 0.59, 0.71).

The return time distributions are right-skewed with modes at 1–4 and tails extending to 20+. Water has the longest returns (max 22 as lower, 21 as upper) — it is the most "scattered" trigram, consistent with Water's mean position being closest to 32.5 (centered in the sequence, evenly distributed).

**Assessment: Return times are unremarkable.** The path does not cluster by row or column beyond what random permutations produce.

---

## Task C: Step-Distance Distribution

### Total grid distance (lower Hamming + upper Hamming)

| Distance | Within-pair (32) | Bridge (31) | All (63) |
|:--------:|:----------------:|:-----------:|:--------:|
| 1 | 0 | 2 | 2 |
| 2 | 12 | 8 | 20 |
| 3 | 0 | 13 | 13 |
| 4 | 12 | 7 | 19 |
| 5 | 0 | 0 | 0 |
| 6 | 8 | 1 | 9 |

### Within-pair distances are deterministic

Within-pair grid distances take only values {2, 4, 6} with distribution {2:12, 4:12, 6:8}. This is entirely determined by the orbit structure:

| Generator(s) | Mirror pairs active | Trigram Δ per side | Grid distance |
|---|:---:|:---:|:---:|
| O, M, I (single) | 1 | 1 | 2 |
| OM, OI, MI (double) | 2 | 2 | 4 |
| OMI, id (triple/complement) | 3 | 3 | 6 |

Count: 4 pairs × 3 single generators = 12 at distance 2; 4 × 3 double = 12 at distance 4; 4 × (OMI + id) = 8 at distance 6. This is exact.

**Key theorem: within-pair lo_dist always equals up_dist.** Each generator's mirror pairs contribute exactly one bit change to each trigram. This is a forced consequence of the cross-trigram structure: every mirror pair has one member in each trigram.

### Bridge distances are the free variable

Bridge distances span {1, 2, 3, 4, 6} (no distance-5 bridges). Mean: 2.935. The mode is 3 (13/31 bridges). Bridges are on average closer than within-pair steps (2.935 vs 3.750).

### Component distances

| Step type | Lo Hamming mean | Up Hamming mean | Lo = Up? |
|-----------|:---:|:---:|:---:|
| Within-pair | 1.875 | 1.875 | **Always** (forced) |
| Bridge | 1.419 | 1.516 | No (free) |

Bridge lo-up correlation: **r = −0.354** (p = 0.063 vs random pair orderings). This negative correlation means: when a bridge changes the lower trigram more, it changes the upper less (and vice versa). The 9 preserving bridges (one side = 0) are the extreme manifestation of this tendency.

**Assessment: The within-pair distance structure is completely determined by the orbit algebra. Bridge distances are free and show a moderate (marginally significant) negative lo-up correlation — a tendency toward "trading off" between which trigram changes more.**

---

## Task D: Trigram Sequence Projection

### The lag-4 periodicity (the main finding)

Combined (lower + upper) trigram autocorrelation at various lags:

| Lag | KW matches | Expected | Null mean ± σ | p-value | Assessment |
|:---:|:----------:|:--------:|:-------------:|:-------:|:---:|
| 1 | 9 | ~16 | 14.0 ± 3.3 | 0.085 (low) | Artifact (see below) |
| 2 | 16 | ~16 | 13.8 ± 3.2 | 0.29 | Unremarkable |
| 3 | 15 | ~15 | 13.6 ± 3.3 | 0.38 | Unremarkable |
| **4** | **24** | ~15 | **13.3 ± 3.2** | **0.0017** | **Highly significant** |
| 5 | 10 | ~15 | 13.1 ± 3.2 | 0.88 (low) | Anti-correlated |
| 6 | 14 | ~14 | 12.9 ± 3.2 | 0.42 | Unremarkable |
| 8 | 17 | ~14 | 12.4 ± 3.1 | 0.093 | Marginal |


**Note on lag-1.** The apparent anti-clustering at lag-1 (9 vs expected ~16) is an artifact of KW's pairing structure. All 9 lag-1 matches are at bridges (the 9 preserving bridges). The 32 within-pair transitions contribute *zero* matches — forced by the cross-trigram theorem. A random permutation has no such constraint, so its lag-1 is higher. Among bridges alone, 9/31 matches vs expected 2×31/8 ≈ 7.75 — bridges actually have *more* same-trigram transitions than expected. The pairing constraint suppresses lag-1 and lag-3 (odd lags) while leaving lag-4 (even lags at pair level) free to express the genuine periodicity.

**Lag-4 stands alone as significant at p = 0.0017.** KW has 24 lag-4 trigram matches vs an expected ~13. This is 3.3σ above the null mean.

### What lag-4 means structurally

Lag-4 = 4 hexagrams = 2 pairs. So hexagram at position i shares a trigram with hexagram at position i+4. This connects:
- First hex of pair k ↔ First hex of pair k+2
- Second hex of pair k ↔ Second hex of pair k+2

In other words: **every second pair tends to echo the same trigram in corresponding positions.** The path traces through trigram space with a period-2 resonance at the pair level.

### The corridors

The lag-4 matches are not uniformly distributed — they cluster into **corridors** where the same trigram persists at every other pair for 3+ consecutive pairs:

**Earth corridor (positions 7–20):**
- Lower Earth: Bi(#8), Pi(#12), Yu(#16), Guan(#20) — 4 hexagrams spanning pairs 4–10
- Upper Earth: Shi(#7), Tai(#11), Qian/Modesty(#15), Lin(#19) — 4 hexagrams spanning pairs 4–10
- These interleave perfectly: positions 7,8,11,12,15,16,19,20 alternate between upper-Earth and lower-Earth

This means: in pairs 4 through 10, Earth appears in every pair, alternating between the first hex's upper trigram and the second hex's lower trigram. Earth is the persistent element — the receptive ground — through this entire developmental arc from Army/Holding Together through Approach/Contemplation.

**Heaven corridor (positions 1–14):**
- Lower Heaven: Qian(#1), Xu(#5), Xiao Chu(#9), Tai(#11), Da You(#14) — but the lag-4 chain is positions 1,5,9
- Upper Heaven: Qian(#1), Song(#6), Lü(#10), Pi(#12), Tong Ren(#13) — lag-4 chain at 6,10

**Thunder corridor (positions 17–25):**
- Lower Thunder: Sui(#17), Shi He(#21), Wu Wang(#25) — 3-hex chain

**Mountain-upper corridor (positions 18–26):**
- Upper Mountain: Gu(#18), Bi/Grace(#22), Da Chu(#26) — 3-hex chain

**Wind corridor (positions 44–50, 53–61):**
- Multiple overlapping Wind chains in the lower canon

### The interpretation

The lag-4 periodicity means the KW path doesn't just jump randomly through the 8×8 grid — it maintains *partial trigram memory* across consecutive pairs. This memory has a specific period: every other pair echoes. The corridors are regions where this memory is strongest, creating extended developmental arcs bound by a persistent trigram quality.

The longest corridor (Earth, positions 7–20) spans 7 pairs — nearly a quarter of the entire Upper Canon. Earth as the persistent element through this arc is semantically coherent: the hexagrams in this region (Army, Holding Together, Small Taming, Treading, Peace, Standstill, Fellowship, Great Possession, Modesty, Enthusiasm, Following, Decay, Approach, Contemplation) describe the progression from collective organization through social flourishing to its decline and renewal — all grounded in Earth's receptive, collective quality.

### Run lengths

Maximum run length (same trigram in consecutive positions): 2, for both lower and upper. No long runs. The path never stays in the same row or column for more than 2 steps.

Number of runs: lower 59, upper 60 (vs null 57.0 ± 2.5). Not significant. The path changes trigram at nearly every step — consistent with the jumping character established in Round 1.

### Self-transitions

Same lower trigram at consecutive positions: 5/63 (null: 7.0 ± 2.5, p(≤5) = 0.16). Same upper: 4/63 (null: 7.0 ± 2.5, p(≤4) = 0.07). The path has marginally *fewer* self-transitions than random — it slightly avoids repeating the same row or column. This is the lag-1 anti-clustering.

### Transition matrices

The lower and upper transition matrices are relatively flat — no strong preferred directions of movement. No row-to-row or column-to-column transition is conspicuously over- or under-represented. The one notable feature: lower Earth → lower Thunder has 4 transitions (most frequent single cell), which is part of the Earth corridor structure.

**Assessment: The lag-4 periodicity is the genuine structural finding. Everything else (run lengths, transition matrices, return times) is unremarkable. The path looks random *locally* (no clustering, no preferred directions) but has pair-level resonance that creates extended corridors of trigram continuity.**

---

## Task E: Pair Footprints on the Grid

### Pair grid distance

Each pair occupies two cells in the 8×8 grid. The cross-trigram theorem forces these cells into different rows AND columns. The grid distance between pair members:

| Grid distance | Count | Generator types |
|:---:|:---:|---|
| 2 | 12 | Single (O, M, I): 4 each |
| 4 | 12 | Double (OM, OI, MI): 4 each |
| 6 | 8 | Triple (OMI) + complement (id): 4 each |

Mean: 3.75. This distribution is entirely determined by the orbit structure.

**Theorem: lo_dist = up_dist for all 32 pairs.** Every pair has identical lower and upper Hamming distances. This is forced: each mirror-pair generator contributes one bit change to each trigram, so the number of active generators equals both lo_dist and up_dist. The pair footprints are perfectly symmetric across the grid diagonal.

The 32 pair footprints decompose into three tiers:
- **Distance-2 pairs (12):** Close neighbors in the grid (1 bit different in each trigram). These are the "minimal mutation" pairs where the pairing changes one quality in each trigram.
- **Distance-4 pairs (12):** Moderate separation (2 bits different in each trigram).
- **Distance-6 pairs (8):** Maximum separation (3 bits = complete trigram change in each). These include all 4 complement pairs (where lower and upper each fully invert) and all 4 OMI pairs.

### Family quadrant distribution

Grouping trigrams by traditional family role (parent: Heaven/Earth; son: Thunder/Water/Mountain; daughter: Wind/Fire/Lake):

| | Up: parent | Up: son | Up: daughter |
|---|:---:|:---:|:---:|
| **Lo: parent** | 4 | 6 | 6 |
| **Lo: son** | 6 | 9 | 9 |
| **Lo: daughter** | 6 | 9 | 9 |

The grid partitions into family quadrants with a clean structure: 4 parent×parent cells, 6 cells in each parent×child quadrant, and 9 cells in each child×child quadrant. This is determined by the trigram counts (2 parents, 3 sons, 3 daughters).

Pair footprints across quadrants: the most common pattern is (son×daughter) ↔ (daughter×son) with 9 pairs. This is the largest quadrant pairing. The family structure is respected by the pairing: pairs tend to cross between son-typed and daughter-typed trigrams.

---

## Task F: Within-pair vs Bridge Geometry

### Component distributions

| | Lo Hamming | Up Hamming |
|---|:---:|:---:|
| **Within-pair** | {1:12, 2:12, 3:8} | {1:12, 2:12, 3:8} |
| **Bridge** | {0:5, 1:12, 2:10, 3:4} | {0:4, 1:11, 2:12, 3:4} |

Within-pair component distances are identical for lower and upper (forced by generator symmetry). Bridge component distances are free and show more variation — including the 0 values (trigram preservation).

### Asymmetry

Within-pair: **zero asymmetry** (lo_dist − up_dist = 0 for all 32 pairs). This is the fundamental geometric consequence of the mirror-pair structure: each generator is a cross-trigram operation that affects both sides equally.

Bridge: mean asymmetry = −0.097 (negligible). Distribution of lo_dist − up_dist: {−3:2, −2:2, −1:10, 0:7, 1:3, 2:7}. Slight lean toward upper changing more (10 bridges where upper changes more by 1, vs 3 where lower changes more by 1), but not significant.

### Bridge lo-up negative correlation

r = −0.354 (p = 0.063 against random pair orderings). When one trigram changes more at a bridge, the other changes less. This is the trigram-level signature of a trade-off: the bridge either changes the inner world or the outer world more — rarely both maximally. The 9 preserving bridges (one component = 0) are the extreme case of this tendency.

**Assessment: The geometry has two regimes. Within-pair steps are perfectly symmetric (forced), have fixed distances {2,4,6}, and carry zero asymmetry. Bridge steps are free, have a full range of distances {1,...,6}, and show a moderate trade-off between lower and upper change. The KW path alternates between these two geometric regimes, creating a rhythm of forced symmetry and free choice.**

---

## Summary

### Three genuine structural findings

**1. The lag-4 periodicity (p = 0.0017).** The KW path has a significant pair-level resonance: every second pair tends to share a trigram in corresponding positions. This creates corridors — extended regions of partial trigram continuity. The strongest corridors:

| Corridor | Trigram | Positions | Pairs spanned | Region |
|----------|---------|-----------|:---:|---|
| Earth (lower) | Earth ☷ | 8,12,16,20 | 4–10 | Upper Canon core |
| Earth (upper) | Earth ☷ | 7,11,15,19 | 4–10 | Upper Canon core |
| Heaven (lower) | Heaven ☰ | 1,5,9 | 1–5 | Sequence opening |
| Thunder (lower) | Thunder ☳ | 17,21,25 | 9–13 | Upper Canon late |
| Mountain (upper) | Mountain ☶ | 18,22,26 | 9–13 | Upper Canon late |
| Wind (upper) | Wind ☴ | 53,57,61 | 27–31 | Sequence closing |

The corridors are not uniformly distributed — they cluster in the early Upper Canon (Earth/Heaven) and late in both canons (Thunder/Mountain, Wind). The sequence opens with Heaven, develops through Earth, and closes with Wind. This is the traditional macro-structure of the I Ching, now visible as trigram corridors in pair-level periodicity.

**2. Within-pair perfect symmetry (lo_dist = up_dist always).** This is forced by the mirror-pair structure and constitutes a new theorem. Each mirror-pair generator contributes equally to both trigrams because it has exactly one member in each. Pair grid distances are exactly {2:12, 4:12, 6:8}, determined by the number of active generators. The within-pair geometry is entirely algebraic.

**3. The two-regime rhythm.** The path alternates between forced (within-pair) and free (bridge) steps. Within-pair steps have zero asymmetry, fixed distances, and perfect lo-up symmetry. Bridge steps have free distances, moderate lo-up anti-correlation (r = −0.354), and the possibility of trigram preservation. The KW path uses this alternation to create both the local pairing structure (algebraic) and the global corridor structure (pair-level periodicity).

### Findings that are null

- **Row/column coverage balance:** Heaven and Earth appear early, but this is the known canon structure. Not new.
- **Return times:** Unremarkable. No clustering or spacing patterns beyond random.
- **Run lengths:** Maximum 2. No extended row or column persistence.
- **Transition matrices:** Flat. No preferred trigram-to-trigram transitions.
- **Lag-1, lag-2, lag-3 autocorrelation:** Not significant. (Lag-1 apparent anti-clustering is a pairing artifact.)

The global geometry is **locally random but periodically structured**. The path looks like a random walk at each step, but has a pair-level resonance that creates macro-scale trigram corridors. This is consistent with the construction: KW built from pairs (local algebraic constraint) assembled in an order that creates macro-scale thematic arcs (the corridors).

### What the lag-4 periodicity means for co-projection

The corridors create regions where a persistent trigram quality (Earth, Heaven, Thunder, Wind) provides thematic continuity across multiple pairs. This is neither algebraic (the orbit structure doesn't determine pair ordering) nor purely semantic (the corridors emerge from positional statistics, not meaning analysis). It's a *structural* property of the pair ordering that creates the *space* for extended developmental narratives.

The Earth corridor (positions 7–20) binds together the hexagrams of collective life — Army, Holding Together, Small Taming, Treading, Peace, Standstill, Fellowship, Great Possession, Modesty, Enthusiasm, Following, Decay, Approach, Contemplation — under the persistent quality of Earth/receptivity. This is the developmental arc of social organization, from military to spiritual, held together by the ground itself.

---

## Questions for Round 4

1. **Do the corridors correspond to traditional hexagram groupings?** The I Ching commentarial tradition has identified natural groupings within the sequence. Do the trigram corridors match these groupings?

2. **Corridor × bridge preservation interaction.** The 9 preserving bridges provide local trigram continuity. The corridors provide pair-level continuity. Do they reinforce each other, or are they independent features?

3. **The lag-4 mechanism.** What aspect of the pair ordering produces the lag-4 periodicity? Is it a direct constraint of the pairing algorithm, or an emergent property of meaning-based ordering?

4. **The lag-1 anti-clustering is explained.** It is an artifact of the pairing constraint — 32 within-pair transitions are forced to contribute zero matches at lag-1, while bridges contribute 9 (above the bridge-only expected 7.75). The pairing structure suppresses odd-lag autocorrelation while leaving even-lag (pair-level) periodicity free to express.

---

## Data Files

| File | Contents |
|------|----------|
| `path_geometry.py` | Complete computation script |
| `round3-path-geometry.md` | This document |
