# Resonance Test 3: Empirical Asymmetry in Climate Cycles

## Prediction

The {4,2,2,2,2} cascade assigns Earth to 4/12 branch positions
(inter-seasonal transitions: months 3, 6, 9, 12). If the five-phase
model captures something real about seasonal dynamics, natural 12-month
temperature cycles should partition into 5 groups with {4,2,2,2,2} structure,
where the 4-member group consists of transition months.

## Data

- 97 cities worldwide, 30-year normals (1991-2020)
- 83 seasonal (monthly std > 2°C)
- 14 flat (excluded): Mexico_City, Bangkok, Manila, Singapore, Jakarta, Kuala_Lumpur, Nairobi, Lagos, Kinshasa, Bogota, Quito, Manaus, Brasilia, Mumbai

## Phase 2: Partition Types (k=5 clustering)

### T+dT (83 cities)

| Partition | Count | % |
|-----------|-------|---|
| (3, 3, 2, 2, 2) | 43 | 51.8% |
| (4, 2, 2, 2, 2) | 23 | 27.7% **◄ PREDICTED** |
| (4, 3, 2, 2, 1) | 12 | 14.5% |
| (5, 2, 2, 2, 1) | 3 | 3.6% |
| (4, 4, 2, 1, 1) | 1 | 1.2% |
| (5, 3, 2, 1, 1) | 1 | 1.2% |

### T only (83 cities)

| Partition | Count | % |
|-----------|-------|---|
| (3, 3, 2, 2, 2) | 60 | 72.3% |
| (4, 3, 2, 2, 1) | 13 | 15.7% |
| (4, 2, 2, 2, 2) | 7 | 8.4% **◄ PREDICTED** |
| (4, 4, 2, 1, 1) | 1 | 1.2% |
| (3, 3, 3, 2, 1) | 1 | 1.2% |
| (5, 2, 2, 2, 1) | 1 | 1.2% |

### T+D+dT+dD (83 cities)

| Partition | Count | % |
|-----------|-------|---|
| (3, 3, 2, 2, 2) | 58 | 69.9% |
| (4, 2, 2, 2, 2) | 23 | 27.7% **◄ PREDICTED** |
| (4, 3, 2, 2, 1) | 1 | 1.2% |
| (3, 3, 3, 2, 1) | 1 | 1.2% |

## Phase 3: Statistical Test

Observed (T+dT): 23/83 = 27.7% are (4,2,2,2,2)

### Null distributions

- Smooth annual cycles (100K sims): 10.0% are (4,2,2,2,2)

Top null partitions (smooth cycles):

| Partition | Count | % |
|-----------|-------|---|
| (4, 3, 2, 2, 1) | 26557 | 26.6% |
| (3, 3, 2, 2, 2) | 22610 | 22.6% |
| (3, 3, 3, 2, 1) | 10626 | 10.6% |
| (4, 2, 2, 2, 2) | 10016 | 10.0% |
| (5, 2, 2, 2, 1) | 9347 | 9.3% |
| (5, 3, 2, 1, 1) | 7561 | 7.6% |
| (6, 2, 2, 1, 1) | 4714 | 4.7% |
| (4, 3, 3, 1, 1) | 3532 | 3.5% |

Uniform random null: 3.0% are (4,2,2,2,2)

**Binomial test**: p = 0.0000

## Phase 4: Rate-of-Change Structure

Top 4 months by |dT| are evenly spaced (±1 month): 0/83 = 0.0%
Null rate: 12.1%
Binomial p: 1.000000

### Transition month frequency

| Month | Count | % | Predicted? |
|-------|-------|---|------------|
| Jan | 1 | 1.2% |  |
| Feb | 10 | 12.0% |  |
| Mar | 62 | 74.7% | ✓ |
| Apr | 63 | 75.9% |  |
| May | 26 | 31.3% |  |
| Jun | 3 | 3.6% | ✓ |
| Jul | 0 | 0.0% |  |
| Aug | 17 | 20.5% |  |
| Sep | 61 | 73.5% | ✓ |
| Oct | 66 | 79.5% |  |
| Nov | 23 | 27.7% |  |
| Dec | 0 | 0.0% | ✓ |

## Phase 5: By Climate Zone

| Zone | N | (4,2,2,2,2) | % | Spaced | % |
|------|---|-------------|---|--------|---|
| arid | 10 | 2 | 20.0% | 0 | 0.0% |
| continental | 23 | 5 | 21.7% | 0 | 0.0% |
| monsoon | 2 | 0 | 0.0% | 0 | 0.0% |
| polar | 5 | 1 | 20.0% | 0 | 0.0% |
| subtropical | 8 | 0 | 0.0% | 0 | 0.0% |
| temperate | 33 | 13 | 39.4% | 0 | 0.0% |
| tropical | 2 | 2 | 100.0% | 0 | 0.0% |

## Key Findings

### The {4,2,2,2,2} partition IS significantly overrepresented

Using temperature + rate-of-change clustering: 27.7% of seasonal cities show
{4,2,2,2,2}, vs 10.0% expected under the smooth-cycle null. Binomial p ≈ 0.
This holds across the two feature-set variants that include dT (T+dT: 27.7%,
T+D+dT+dD: 27.7%), but collapses with temperature-only (8.4%).

The rate-of-change feature is what drives the {4,2,2,2,2} partition. Temperature
alone produces {3,3,2,2,2} in 72% of cities — the natural partition of a
sinusoidal cycle into 5 groups.

### BUT: the transition months are NOT evenly spaced

The prediction says Earth occupies months 3, 6, 9, 12 (evenly spaced transitions).
The actual transition months (top 4 by |dT|) cluster at **March-April** and
**September-October** — the two equinoctial transitions, not four evenly
spaced ones. 0/83 cities have evenly spaced transitions.

This is physically obvious: temperature changes fastest at the equinoxes (when
solar declination changes most rapidly), not at four evenly spaced points.
The annual temperature cycle is approximately sinusoidal with ONE dominant
harmonic. A sinusoid has 2 transition zones (zero-crossings) and 2 stable
zones (peaks), not the 4+8 split the model predicts.

### The 4-group is CONTIGUOUS and VARIES by city

Inspection of which months form the 4-member group reveals it is always
4 contiguous months, but the specific months depend entirely on local climate:

- Mediterranean/warm-temperate: cool season (Jan, Feb, Mar, Dec) — the
  compressed temperature end
- Continental/cold: warm season (Jun, Jul, Aug, Sep) or spring
- Southern Hemisphere: cold season (Jun-Sep)
- Oceanic: mild season (varies)

Aggregate month frequency in the 4-group across all 23 cities:

| Month | Count | | Month | Count |
|-------|-------| |-------|-------|
| Jan | 9 | | Jul | 9 |
| Feb | 11 | | Aug | 7 |
| Mar | 10 | | Sep | 6 |
| Apr | 8 | | Oct | 3 |
| May | 8 | | Nov | 4 |
| Jun | 9 | | Dec | 8 |

The distribution is approximately UNIFORM across months. The 4-group
is not preferentially any season — it's whichever 4 contiguous months
have the most compressed temperature range (the "flat" side of the
annual sinusoid).

### The dominant partition is {3,3,2,2,2}

51.8% of cities show {3,3,2,2,2} — the natural 5-fold partition of a
near-sinusoidal cycle: two 3-month cores (summer, winter) + four 2-month
transition periods. This is the expected partition for any smooth annual
cycle with dominant first harmonic.

### Interpretation for the resonance question

**Numerically positive, structurally negative.**

The {4,2,2,2,2} partition type IS genuinely overrepresented (27.7% vs 10%
null, p ≈ 0). But the mechanism is entirely geometric, not algebraic:

- A near-sinusoidal annual temperature cycle, when clustered into 5 groups,
  naturally produces either {3,3,2,2,2} (symmetric sinusoid) or {4,2,2,2,2}
  (slightly asymmetric sinusoid where one half has a flatter temperature range)
- The 4-group is always 4 contiguous months — whichever half-year has more
  compressed temperatures — not 4 evenly spaced transition months
- The model predicts 4 months at positions 3,6,9,12 (quarterly transitions).
  Reality shows 4 contiguous months at an arbitrary position
- The overrepresentation vs null comes from the low harmonic content of real
  climate data compared to the null's random harmonic mix

### Transition structure: strongly 2-fold, not 4-fold

The rate-of-change analysis reveals the actual temporal structure:
- 2 transition zones (equinoctial: Mar/Apr and Sep/Oct) — 75%+ frequency
- 2 stable zones (solstitial: Jun/Jul/Dec/Jan) — near 0% frequency
- This is simple sinusoidal physics: max |dT/dt| at zero-crossings (equinoxes),
  min |dT/dt| at extrema (solstices)

The model predicts 4-fold transition symmetry. Nature shows 2-fold.

### Test 3 verdict: **Negative**

The {4,2,2,2,2} cardinality appears in the data, but is explained by the
geometry of sinusoidal cycles rather than by the algebraic embedding of Z₅
into a 12-fold cycle. The critical structural prediction — 4 evenly spaced
transition months — is empirically false (0/83 cities). The asymmetry is
in the model's algebra, not in nature's dynamics.