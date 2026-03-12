# Investigation 1: Intraday Regime Transition Structure

## Status: COMPLETE — March 2026

**Result: Clean informative negative on (3,5). K=4, not K=5.**

The investigation ran 6 phases across ~20 workflow iterations. The (3,5) surjection hypothesis is definitively rejected for BTC intraday dynamics. Instead, the investigation discovered genuine market structure: a 4-regime directed cycle, complement symmetry, and an exit sub-state confirmation signal.

Full synthesis: `memories/markets/investigation-summary.md`
Iteration log: `memories/markets/exploration-log.md`

---

## Question

Does the empirical intraday transition structure for BTC match the (3,5) predictions? And if not, what DOES the transition structure look like?

**Answer:** No. The market has 4 functional regime types (not 5), organized as a directed cycle with forbidden stage-skipping. Complement symmetry holds (a necessary condition for (3,5)), but the sufficient conditions fail — K=4 beats K=5 by 19× in lumpability error across all 240 complement-equivariant surjections.

---

## Data

**Source:** `datalog_2025-07-21_2026-02-20.csv`
- BTC, 1-second sampling, 18.6M rows, 214 days
- Downsampled to 5-minute bars (61,920 rows)
- Price range: $60,024–$125,978
- 96 features spanning volume profile, trends, realized volatility, CVD, orderbook, Goertzel cyclicals

---

## What Was Tested

### Four binary bases (3 bits → 8 states each)

| Basis | Features | Outcome |
|-------|----------|---------|
| A: Cross-timescale trend | trend_1h / trend_8h / trend_48h | K=4, stable, informative |
| B: Volume profile | vp12h/48h/96h_poc_dist | Disqualified (heavy tails, no structure) |
| C: Flow × structure × activity | cvd_slope_15m / trend_8h / realized_vol_8h | K=4, but fast-bit artifact |
| D: Timescale-matched orthogonal | tot_8h / trend_8h / realized_vol_8h | K=4, complement symmetry confirmed |

### Six phases of analysis

1. **Phase 1: Diagnostics** — Transition matrices, eigenvalues, dwell times, subperiod stability for bases A/B/C
2. **Phase 2: 4×4 characterization** — Collapsed Basis A, discovered directed cycle and C2 heterogeneity. New Basis D with complement symmetry test.
3. **Phase 3: (3,5) closure** — Exhaustive 240-surjection search. K=4 wins by 19×.
4. **Phase 4: Regime-conditioned returns** — Duration, exit destination, price returns. C2 exit signal quantified.
5. **Phase 5: Flip dynamics** — Intra-episode S4↔S5 flips. Trigger is noise; signal is exit property.
6. **Phase 6: Forward-looking returns** — Exit sub-state predicts next regime quality. Generalizes across all transitions.

---

## (3,5) Prediction Results

| Prediction | Result | Evidence |
|-----------|--------|----------|
| K=5 equivalence classes | **REJECTED** | K=4 across 3 bases, eigenvalue gaps, exhaustive search |
| Complement equivariance | **CONFIRMED** | Basis D: all pairs JSD < 0.09, degenerate eigenvalues |
| Spectral gap ≈ 0.71 | **REJECTED** | Best K=5: 0.30. K=4 complement: 0.31 |
| 89% concentration on 3 types | **REJECTED** | Best K=5: 68.6%. K=4: near-uniform (22–28%) |
| Structural zeros | **PARTIALLY CONFIRMED** | 4 zeros in J₄ (stage-skipping forbidden), but different pattern from (3,5) |
| Two independent 5-cycles | **REJECTED** | One directed 4-cycle instead |
| Fast mixing | **CONFIRMED (different K)** | Coherence chain spectral gap 0.31 |

---

## What Was Found Instead

### 1. Four-Regime Directed Cycle

```
Bear (C0) → Reversal (C1) → Bull (C3) → Pullback (C2) → Bear (C0)
```

J₄ jump chain (Basis A):
```
         C0      C1      C2      C3
C0    —    0.925   0.076   0.000
C1  0.795    —     0.000   0.205
C2  0.230   0.000    —     0.770
C3  0.005   0.075   0.919    —
```

- 4 structural zeros: stage-skipping forbidden
- Near-uniform stationary distribution: 22.6%–28.1%
- Subperiod-stable: Frobenius norm 0.03–0.12 across 71-day windows
- 794 regime episodes, ~6–7h mean duration each

### 2. Complement Symmetry (Coherence Parity)

Basis D (tot_8h × trend_8h × realized_vol_8h): all 4 complement pairs have JSD < 0.09 under relabeling. T₈ eigenvalues show degenerate pairs (0.968, 0.968) and (0.957, 0.957).

**Interpretation:** The market distinguishes *coherent* from *incoherent* states, not up from down. Coherent bear = coherent bull under the transition structure. The relevant dimension is alignment, not polarity.

### 3. Exit Sub-State Confirmation Signal

The fast bit (trend_1h) at regime exit predicts next regime quality:

**C2 pullback (strongest instance):**
- S5 exit (trend_1h↑) → 92% bull [86%, 96%], stable across 3 subperiods
- S4 exit (trend_1h↓) → 50/50 coin flip

**General property:** S7 exits from C3 → orderly pullback (+0.06%); S6 exits → sharp pullback (−0.24%). The pattern holds at all regime boundaries.

**NOT a trading trigger:** Intra-episode flips are noise (511 confirmed-flip trades, +0.005% mean). The signal confirms at the moment of regime transition — a position sizing input, not an entry signal.

### 4. C1 Reversal Asymmetric Payoff

- 20% breakthrough to bull: +1.09% mean return
- 80% failure to bear: −0.25% mean return
- Unconditional EV: +0.018% (not tradeable)
- S3-conditioned EV: +0.14% (n=69, thin sample)

---

## Key Numbers

| Quantity | Value |
|----------|-------|
| K=4 lumpability error | 8.4×10⁻⁵ |
| K=5 best lumpability error | 1.6×10⁻³ (19× worse) |
| C2-S5 → bull rate | 91.8% [86%, 96%] |
| S5 subperiod stability | 90.7%–92.7% |
| C2-S5 exit mean return | +0.20% |
| C2-S4 exit mean return | −0.81% |
| C2-S5 → C3 forward return | +0.09%, 7.6h |
| C2-S4 → C3 forward return | −0.17%, 4.3h |
| Mean regime duration | 6.1–6.9h |
| Intra-episode flips | ~3 per episode (noise) |

---

## Caveats

- **Single asset, in-sample only.** 214 days of BTC. Structural patterns likely general; exact numbers sample-specific.
- **Subperiod stability encouraging but insufficient.** Three 71-day windows agree, but this is in-sample subdivision, not out-of-sample testing.
- **Signal is at regime EXIT, not entry.** Observable with 5-minute (one bar) latency. Fast enough for position sizing at 6h timescale.
- **187 C2 episodes** — adequate for CIs but not large. Small-n paths (C2-S5→C0: n=10) have wide intervals.

---

## Methodology Produced

The binary trigram + transition matrix + lumpability framework is general-purpose:

1. Select 3 binary features from orthogonal channels (|r| < 0.3)
2. Construct 8-state trigram series
3. Estimate T₈ and J₈ (jump chain)
4. Eigenvalue gap analysis → K
5. Test complement symmetry (JSD between complement-relabeled rows)
6. Collapse to K-state chain, verify lumpability
7. Regime-conditioned return analysis with subperiod stability

Applicable to any asset and feature set. The (3,5) hypothesis motivated building it; the framework outlives the hypothesis.

---

## Next Steps (require different data)

1. Out-of-sample: BTC 2023-2024 and post-Feb 2026
2. Multi-asset: ETH, SOL, SPY, QQQ
3. Timescale variation: 1h and 24h feature bases
4. Real-time regime indicator implementation

---

## Scripts and Outputs

| Phase | Script | Output |
|-------|--------|--------|
| 1 | `logos/markets/01_phase1_diagnostics.py` | `memories/markets/01_phase1_output.txt` |
| 2 | `logos/markets/02_phase2_diagnostics.py` | `memories/markets/02_phase2_output.txt` |
| 3 | `logos/markets/03_phase3_closure.py` | `memories/markets/03_phase3_output.txt` |
| 4 | `logos/markets/04_regime_returns.py` | `memories/markets/04_phase4_output.txt` |
| 5 | `logos/markets/05_flip_dynamics.py` | `memories/markets/05_phase5_output.txt` |
| 6 | `logos/markets/06_forward_returns.py` | `memories/markets/06_phase6_output.txt` |
