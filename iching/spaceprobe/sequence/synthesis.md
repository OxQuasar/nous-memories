# Sequence Layer Investigation — Synthesis

## The question

The KW sequence ordering has the strongest signals in the I Ching's combinatorial structure — consecutive bridge kernel distances at ~97th percentile, all kernel types used, orientation bits load-bearing. The pairing layer was characterized axiomatically (two axioms → unique structure). Can the sequence layer be similarly characterized? What group-theoretic or combinatorial framework explains *which pair goes where*?

## The answer (honest version)

**No axiomatic characterization was found.** The sequence layer resists the kind of tight determination that worked for the pairing layer. What was found instead is a *structural signature* — a set of properties that are genuine, independent, and localized, but that constrain rather than determine the ordering.

The investigation's real contribution is **deflation**: correcting inflated claims from the earlier synthesis and identifying exactly where the structure lives and where it doesn't.

---

## What was corrected

| Claim from synthesis | Actual finding |
|---------------------|---------------|
| "All 27 orientation bits load-bearing" | 16/32 under metric-degradation criteria |
| "99.2nd percentile kernel distance" | 96.6th under the correct null model (randomize permutation AND orientation) |
| "0th percentile kac (no repeats)" | KW has 2 kernel repeats (OM→OM, OI→OI) |
| "Transition grammar (MI = 1.33 bits)" | Artifact of small-sample bias; 0.43σ above shuffle null after correction |

---

## What survived deflation: two independent signals

### Signal 1: Consecutive kernel distance (f1)

Mean consecutive 3-bit kernel distance = 1.767 (96.6th percentile). The mechanism: 8 of 30 deltas are OMI (full complement), at the 99.2nd percentile unconditionally (93.6th conditional on f1). **f1 and OMI count are one signal** (r = 0.65). Conditioned on OMI≥8, f1 is unremarkable (55.7th percentile).

### Signal 2: Subgroup residence

The running product of bridge kernels spends 64.5% of its time in H = {id, O, MI, OMI}, a specific order-4 subgroup of Z₂³ (96.7th percentile). This subgroup is **uniquely distinguished** among all seven order-4 subgroups (next closest: 86.1th percentile). The bias comes from pair *ordering*, not orientation choices.

**Algebraic characterization of H**: z ∈ H iff the M-bit equals the I-bit. In hexagram terms: the middle mirror pair (L2,L5) and inner mirror pair (L3,L4) are "locked" — they always flip together or not at all. The outer pair (L1,L6) is free. The cumulative effect of the Upper Canon's transitions preferentially treats the inner four lines as a block.

**These two signals are independent**: r(f1, H-residence) = −0.001.

---

## The central finding: two-canon asymmetry

The signals do not distribute uniformly across the sequence. They concentrate entirely in the Upper Canon (hex 1–30, pairs 0–14).

| | Upper Canon (14 bridges) | Lower Canon (16 bridges) |
|---|---|---|
| f1 | 2.154 — **99.84th %ile** | 1.467 — **51st %ile** |
| H-residence | 11/14 = 79% — **99.42nd %ile** | 8/16 = 50% — **60th %ile** |
| OMI deltas | 5/13 (38.5%) | 2/15 (13.3%) |
| Weight change | 99.9th %ile (anti-smooth) | 53rd %ile |

The Upper Canon is simultaneously extreme on two independent axes — roughly 1 in 10,000 for that 14-bridge segment alone. The Lower Canon is indistinguishable from random on every metric tested: kernel distance, subgroup residence, weight smoothness, trigram continuity, raw Hamming distance.

**The overall KW properties (f1 = 1.77, H-residence = 64.5%) are averages of two qualitatively different regimes**, not a uniform optimization. The cross-canon bridge (B15, kernel = OM, not in H) explicitly breaks the M-I lock.

---

## What the Lower Canon doesn't do

The Lower Canon was tested for:
- Kernel distance optimization → 51st percentile
- Subgroup residence → 60th percentile  
- Weight smoothness → 53rd percentile
- Trigram continuity → 72nd percentile
- Raw Hamming distance → 49th percentile

All dead center. Whatever the Lower Canon encodes — if anything at the structural level — it is not detectable by transition-between-adjacent-pairs metrics. The absence is measured within a specific frame; structure at other levels (semantic grouping, non-local relationships, developmental narrative) remains untested.

---

## What was eliminated

1. **Transition grammar.** MI = 1.33 bits is a small-sample bias artifact (Miller-Madow correction: −0.41 bits). After correction and shuffle-null comparison, the kernel sequence has no significant sequential structure beyond its marginal frequencies.

2. **Delta autocorrelation.** All lag-structure measures (lag-1 correlation, run-length distribution, max run) are within normal range. No hidden periodicity.

3. **OMI spacing pattern.** The front-loading of OMI deltas (98.3rd percentile for first-half count) is a corollary of the two-canon asymmetry, not an independent signal.

4. **Joint constraint tightness as uniqueness.** Five constraints together (f1, H-residence, repeats, types, OMI count) yield ~1 in 1,200 survival rate. This constrains but does not characterize — roughly 800 orderings in a million-trial sample satisfy everything measured.

---

## Constraint inventory

| Constraint | KW value | Percentile | Independent? |
|-----------|----------|-----------|-------------|
| f1 (mean consecutive kernel distance) | 1.767 | 96.6% | — |
| OMI delta count | 8/30 | 99.2% (93.6% | f1) | ≈ f1 |
| H-residence (running product in {id,O,MI,OMI}) | 20/31 | 96.7% | Yes (r = −0.001 with f1) |
| Kernel repeats | 2/30 | ~75th %ile | Weak |
| Kernel types used | 8/8 | ~87% baseline | Weak |
| Upper Canon f1 | 2.154 | 99.84% | f1 localized |
| Upper Canon H-residence | 11/14 | 99.42% | H-res localized |

**Effective independent constraints: 2** (f1 and H-residence). Everything else is either derivative, weak, or localized.

---

## The structural picture

The King Wen sequence is a **two-phase process**:

**Phase 1 (Upper Canon, hex 1–30):** Maximizes opposition between consecutive bridge transitions while constraining the cumulative transformation path to the M-I locked subgroup. The inner hexagram core (lines 2–5) is treated as a unit; the outer boundary (lines 1, 6) is free. Every transition is as different as possible from the last, and the running effect of all transitions keeps returning to a constrained subspace. Jointly extreme at ~1 in 10,000.

**Phase 2 (Lower Canon, hex 31–64):** Releases all kernel-level constraints. Structurally generic on every measured axis. May encode structure at a level not captured by bridge-transition metrics.

The cross-canon bridge (hex 30→31, kernel = OM) explicitly breaks the M-I lock, transitioning from the constrained to the unconstrained regime.

---

## Comparison to the pairing characterization

| | Pairing layer | Sequence layer |
|---|---|---|
| Characterization type | Axiomatic (2 axioms → unique) | Descriptive (2 signals, ~1 in 1,200) |
| Constraint tightness | 1 of 9 (then 1 of 1 with WT) | ~1 in 1,200 |
| Algebraic object | S₄ on 4 blocks of 2 | H = V₄ subgroup of Z₂³ |
| Nature of selection | Unique optimum (WT minimizer) | Extreme but not unique |
| Layer completeness | Complete (fully explains pairing) | Partial (explains Upper Canon only) |

The pairing layer yielded a *characterization* — axioms that determine the structure. The sequence layer yields a *signature* — properties that distinguish the ordering but don't determine it. This is an honest difference in the layers' susceptibility to algebraic analysis.

---

## Open questions

1. **Lower Canon structure.** Does it encode something not visible in transition metrics? Semantic grouping, developmental narrative, and non-local relationships are untested.

2. **Why H specifically?** The M-I lock's algebraic characterization (inner core as unit, outer boundary free) is suggestive but unconnected to any interpretive framework. Does it relate to the hexagram's compositional structure (two trigrams stacked)?

3. **Selection effect.** Is the Upper Canon's extremity partly because its specific hexagram content (containing the Heaven/Earth, Water/Fire pairs) inherently supports higher f1 and H-residence? Untested: maximum achievable f1 over all 15! orderings of the Upper Canon pairs vs random 15-pair sets.

4. **Why 30 + 34?** The 上经/下经 division is a known traditional structural feature. The investigation found that all measurable sequential structure lives in the shorter first half. Whether this is cause (the division exists to separate structured from unstructured) or effect (the structure was concentrated in what became the Upper Canon) is unknown.

5. **Generative model.** No rule has been found that *produces* the Upper Canon's ordering. The H-subgroup bias and high f1 are consequences of some organizing principle; that principle remains unidentified.
