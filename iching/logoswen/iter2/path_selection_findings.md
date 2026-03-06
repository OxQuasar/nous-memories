# Path Selection Analysis: Orbit-Change Weight Distribution

## Key Discovery

**The orbit-change weight profile is an INVARIANT of the multigraph — identical for ALL 150,955,488 Eulerian paths.**

Every Eulerian path uses every edge exactly once. The orbit multigraph has fixed edge multiplicities, and each edge has a fixed orbit-change weight. Therefore the multiset of orbit-change weights is the same for every path:

| w(orbit_change) | Edge count | S=2 status | max_S |
|-----------------|-----------|------------|-------|
| 0 (self-loop) | 2 | Susceptible | 3 |
| 1 (single-comp) | 9 | Susceptible | 2 |
| 2 (double-comp) | 14 | **Immune** | 1 |
| 3 (OMI) | 6 | **Immune** | 0 |

**Every Eulerian path has exactly 11 S=2-susceptible bridges and 20 S=2-immune bridges.** KW's 20/31 immune bridge count is not a choice — it's the only possible value.

---

## What Varies: Edge Ordering, Not Edge Content

While the multiset is fixed, different Eulerian paths place the 11 susceptible edges at different positions in the 31-bridge sequence. This affects:

1. **Hexagram correlations** — consecutive susceptible bridges share within-orbit constraints
2. **Self-loop placement** — the two w=0 bridges (P(S=2) = 37.5%) can appear at different positions
3. **Clustering** — susceptible bridges that cluster together may be harder to simultaneously avoid

### S=2 Absence Rate Across Paths

Sampling 200 Eulerian paths with 500 random orderings each (KW matching):

| Metric | Value |
|--------|-------|
| Mean S=2 absence | **2.47%** |
| Std | 0.67% |
| Min | 0.60% |
| Max | 4.60% |
| CV | 0.271 |
| **KW path** | **2.25% (42nd percentile)** |

The S=2 absence rate varies modestly across paths (CV = 0.27). KW's path is unremarkable — near the median. The variation comes from how susceptible edges interleave with immune edges, affecting hexagram availability correlations.

### Independence Approximation

Under independence (each susceptible bridge independently avoids S=2):

- 2 self-loops: P(avoid) = 1 − 24/64 = 0.625 each
- 9 weight-1 bridges: P(avoid) = 1 − 16/64 = 0.75 each
- P(all 11 avoid) ≈ 0.625² × 0.75⁹ = **2.93%**
- Actual (sampling): ~2.47%
- Ratio: 0.84× — weak negative correlation makes joint avoidance slightly harder

---

## KW's 11 Susceptible Bridges (Detail)

| Bridge | Transition | w | P(S=2) per pair |
|--------|-----------|---|-----------------|
| B8 | Tai→Zhun | 1 | 25.0% |
| B13 | Qian→Qian | 0 | 37.5% |
| B14 | Qian→Shi | 1 | 25.0% |
| B15 | Shi→Zhun | 1 | 25.0% |
| B18 | WWang→WWang | 0 | 37.5% |
| B19 | WWang→Shi | 1 | 25.0% |
| B22 | WWang→XChu | 1 | 25.0% |
| B25 | Xu→Tai | 1 | 25.0% |
| B27 | Bo→Xu | 1 | 25.0% |
| B28 | Xu→Bo | 1 | 25.0% |
| B29 | Bo→Qian | 1 | 25.0% |

The two self-loops (B13, B18) are the hardest to satisfy — they have 37.5% S=2 probability vs 25% for weight-1 bridges.

---

## Edge Classification (Full Multigraph)

| Edge | Multiplicity | w | S=2 status |
|------|-------------|---|------------|
| Qian→Qian | 1 | 0 | Susceptible |
| WWang→WWang | 1 | 0 | Susceptible |
| Qian→Shi | 1 | 1 | Susceptible |
| Shi→Zhun | 1 | 1 | Susceptible |
| WWang→XChu | 1 | 1 | Susceptible |
| WWang→Shi | 1 | 1 | Susceptible |
| Bo→Qian | 1 | 1 | Susceptible |
| Bo→Xu | 1 | 1 | Susceptible |
| Xu→Bo | 1 | 1 | Susceptible |
| Xu→Tai | 1 | 1 | Susceptible |
| Tai→Zhun | 1 | 1 | Susceptible |
| Qian→Zhun | 1 | 2 | Immune |
| Qian→Tai | 1 | 3 | Immune |
| XChu→Bo | 1 | 2 | Immune |
| XChu→Zhun | 1 | 3 | Immune |
| XChu→Tai | **2** | 2 | Immune |
| Shi→XChu | **2** | 2 | Immune |
| Shi→Bo | 1 | 2 | Immune |
| WWang→Qian | 1 | 2 | Immune |
| Bo→WWang | **2** | 3 | Immune |
| Xu→Shi | 1 | 3 | Immune |
| Xu→WWang | 1 | 2 | Immune |
| Zhun→XChu | 1 | 3 | Immune |
| Zhun→Xu | **3** | 2 | Immune |
| Tai→Shi | 1 | 2 | Immune |
| Tai→Bo | 1 | 2 | Immune |

---

## Constraint Hierarchy Correction

The earlier "Level 2b" hypothesis was wrong. The Eulerian path does NOT affect the S=2-susceptible bridge count — it's a graph invariant. The corrected hierarchy:

### Level 1: Orbit-consistent pairing
- Forces the Eulerian bridge structure
- The orbit multigraph has exactly 11 susceptible + 20 immune edges (INVARIANT)

### Level 2: Matching (mask=sig)
- Algebraic choice, NOT optimized for S=2 (ranks 26th/27)
- Weak effect on S=2 rate (~0.5% bridge mass shift)

### Level 3: Pair ordering
- **This is where S=2 avoidance lives** — p ≈ 2.5% under random ordering
- Hexagram correlations across the 11 susceptible bridges create weak negative correlation
- The specific Eulerian path affects the rate (CV = 0.27), but KW's path is unremarkable (42nd pctile)

### Level 4: Pair orientation
- 2³² remaining degrees of freedom

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `path_selection_analysis.py` | Full path selection analysis | ✓ Complete |
