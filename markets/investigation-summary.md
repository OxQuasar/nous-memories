# Market Regime Dynamics: Investigation Summary

## 1. What We Tested

**Hypothesis:** The (3,5) Z₅ transition matrix from I Ching uniqueness theory provides a zero-parameter model for intraday BTC regime dynamics. Specific predictions: 5 functional regime types (from 8 observable configurations via complement-equivariant surjection), spectral gap ≈ 0.71, 89% stationary mass on 3 regime types, structural zeros, and fast mixing.

**Data:** BTC, 2025-07-21 to 2026-02-20 (214 days), 18.6M rows at 1-second resolution, downsampled to 5-minute bars (61,920 rows). Price range $60,024–$125,978. 96 features spanning volume profile, multi-timescale trends, realized volatility, CVD, orderbook, and Goertzel cyclical analysis.

**Method:** Construct 3 binary features → 8 observable states (trigram analogue). Estimate 8×8 transition matrix. Test whether eigenvalue gaps, lumpability analysis, and spectral clustering support K=5 regime types with (3,5) spectral properties.

---

## 2. (3,5) Result: Clean Negative

The (3,5) surjection hypothesis is definitively rejected on this data.

**K=4, not K=5.** Three independent feature bases (cross-timescale trend, flow×structure×activity, acceleration×velocity×energy) all produce eigenvalue gaps at position 3→4, indicating 4 natural clusters. No basis suggests K=5.

**Exhaustive surjection search.** All 240 complement-equivariant surjections from 8 states to 5 classes were tested against Basis D (the best-structured basis). The best K=5 surjection has lumpability error 0.00160 — 19× worse per degree of freedom than the K=4 complement-pair partition (error 0.0000837). Every single K=5 partition is worse than K=4.

**Spectral properties miss.** Even the best K=5 surjection produces spectral gap 0.30 (vs predicted 0.71) and top-3 stationary concentration 68.6% (vs predicted 89%).

**What the (3,5) model got right:** Complement symmetry (necessary condition). The F₂³ complement involution x ↦ x⊕7 is empirically confirmed as a symmetry of the transition dynamics — all 4 complement pairs have JSD < 0.09 under relabeling. The T₈ eigenvalue spectrum shows degenerate pairs (signature of an involutory symmetry). But complement symmetry is necessary, not sufficient, for (3,5), and the sufficient conditions fail.

---

## 3. What We Found Instead

### 3a. Four-Regime Directed Cycle

The market operates on a 4-regime cycle with directed transitions:

```
Bear (C0) → Reversal (C1) → Bull (C3) → Pullback (C2) → Bear (C0) → ...
```

**Basis A (trend_1h × trend_8h × trend_48h)** reveals this as two coupled 2-cycles: C0↔C1 (bearish oscillation) and C2↔C3 (bullish oscillation), weakly coupled by cross-macro transitions:

| From\To | C0 bear | C1 reversal | C2 pullback | C3 bull |
|---------|---------|-------------|-------------|---------|
| C0 | — | **0.925** | 0.076 | **0.000** |
| C1 | **0.795** | — | **0.000** | 0.205 |
| C2 | 0.230 | **0.000** | — | **0.770** |
| C3 | **0.005** | 0.075 | **0.919** | — |

Key structural properties:
- **4 structural zeros** in J₄: stage-skipping is forbidden (C0↛C3, C1↛C2, C2↛C1, C3↛C0)
- **Near-uniform stationary distribution:** 22.6%–28.1% per regime (no rare regime)
- **Subperiod stability:** Frobenius norm 0.03–0.12 across three 71-day windows — the structure is stationary

### 3b. Complement Symmetry (Coherence Parity)

Market-opposite states have identical transition dynamics under relabeling. In Basis D (tot_8h × trend_8h × realized_vol_8h), all 4 complement pairs pass with JSD < 0.09:

| Pair | JSD | Description |
|------|-----|-------------|
| S0 (000) ↔ S7 (111) | 0.087 | calm-bear-decel ↔ volatile-bull-accel |
| S1 (001) ↔ S6 (110) | 0.074 | calm-bear-accel ↔ volatile-bull-decel |
| S2 (010) ↔ S5 (101) | 0.046 | calm-bull-decel ↔ volatile-bear-accel |
| S3 (011) ↔ S4 (100) | 0.048 | calm-bull-accel ↔ volatile-bear-decel |

**Interpretation:** The market's transition dynamics distinguish *coherence* (are trend, acceleration, and volatility aligned?) from *direction* (bull vs bear). Coherent bear = coherent bull under the transition structure. The relevant dimension is alignment, not polarity.

### 3c. Exit Sub-State Signal

The most actionable finding: the fast bit (trend_1h) at the moment of regime exit predicts the next regime's direction and quality. This is a **general property of the 8-state chain**, not specific to C2: when trend_1h agrees with the macro-regime direction at exit, the transition is orderly; when it disagrees, the transition is messy. Phase 6 confirmed this for C3→C2 as well (S7 exits produce orderly pullbacks at +0.06%, S6 exits produce sharp pullbacks at −0.24%).

**C2 pullback exit states (strongest instance, 95% Wilson CIs):**

| Exit sub-state | → Bear | → Bull | Interpretation |
|----------------|--------|--------|----------------|
| S4 (trend_1h↓) | **50.8%** [39%,63%] | **49.2%** | Coin flip — uncertainty |
| S5 (trend_1h↑) | **8.2%** [5%,14%] | **91.8%** [86%,96%] | Near-certain continuation |

**Subperiod stability (remarkably consistent across 71-day windows):**

| Period | S4→bear | S4→bull | S5→bear | S5→bull |
|--------|---------|---------|---------|---------|
| 1 (Jul-Sep) | 56.0% | 44.0% | 7.9% | 92.1% |
| 2 (Oct-Dec) | 52.4% | 47.6% | 7.3% | 92.7% |
| 3 (Dec-Feb) | 42.1% | 57.9% | 9.3% | 90.7% |

**Return conditioning:** S5-exit C2 episodes have mean return +0.20% (recovering pullback), while S4-exit episodes have mean −0.81% (deepening pullback). This is a dual signal: direction prediction AND magnitude information.

**Forward-looking returns (Phase 6):** The exit sub-state also predicts the NEXT regime's character:
- C2-S5 → C3 bull episodes (n=111): mean return **+0.09%**, duration 7.6h — longer and positive
- C2-S4 → C3 bull episodes (n=32): mean return **−0.17%**, duration 4.3h — shorter and negative
- C2-S5 → C0 bear episodes (n=10, rare): mean return **+0.12%**, duration 4.2h — shallow bear

When a confirmed pullback (S5 exit) does fail to bear (8% of cases), the resulting bear episode is short and shallow. When an uncertain pullback (S4 exit) produces a bull episode, that bull is anemic and short-lived. The exit sub-state carries forward.

**Zero-flip C2 episodes:** 28 episodes total with 0 S4→S5 flips. Of these, 11 entered C2 as S5 and never transitioned to S4 (pullback never deepened) — all 11 exited to bull (100%), mean return +0.14%, duration 0.5h. The remaining 17 entered as S4 and never flipped to S5 (pullback never attempted recovery) — these are the mirror image and exited predominantly to bear.

### 3d. C1 Reversal Asymmetric Payoff

C1 reversal is the gateway between bear and bull macro-regimes. 80% of C1 exits return to C0 bear (failed reversal), 20% break through to C3 bull. But the payoffs are massively asymmetric:

- **C1 → C3 bull breakthrough (n=43):** mean return +1.09%, median +0.71% — large, fast moves
- **C1 → C0 bear failure (n=167):** mean return −0.25%, median −0.21% — small, slow losses

**Unconditional** expected value of entering C1 long: 0.20 × (+1.09%) + 0.80 × (−0.25%) = **+0.018%** — slightly positive despite 80% failure rate, but high variance and not tradeable in isolation.

**S3-conditioned** (trend_1h↑ at exit): shifts breakthrough probability to 29% (n=69 S3 exits, 20 breakthroughs). S3-conditioned EV = 0.29 × (+1.09%) + 0.71 × (−0.25%) = **+0.14%** — more interesting but thin sample (n=69).

---

## 4. Duration Characteristics

All four macro-regimes have strikingly similar duration profiles:

| Regime | Episodes | Mean | Median | Description |
|--------|----------|------|--------|-------------|
| C0 bear | 211 | 6.9h | 5.6h | Persistent, negatively skewed |
| C1 reversal | 210 | 6.1h | 5.6h | Symmetric duration |
| C2 pullback | 187 | 6.2h | 5.8h | Short failures, long resolutions |
| C3 bull | 186 | 6.7h | 5.9h | Long normal, short exits to reversal |

**C2 pullback duration asymmetry:** Episodes exiting to bear have median 3.9h (sharp, fast failures). Episodes exiting to bull have median 5.8h (gradual, soaking recoveries). Fast pullback = danger. Slow pullback = resolution.

**Intra-regime oscillation:** The fast bit (trend_1h) flips ~3 times per episode (mean 3.1 S4↔S5 flips in C2, 2.8 S2↔S3 flips in C1). Individual flips carry negligible return information — they are noise within the regime. The actionable signal is the sub-state at regime EXIT, not at intra-regime transitions.

**Confirmed-flip trading:** Entering long on confirmed S4→S5 flips within C2 produces 38.4% win rate and +0.005% mean return across 511 trades — near-zero edge. The intra-regime flip is not tradeable on its own.

---

## 5. Caveats and Limitations

- **Single asset, in-sample only.** 214 days of BTC. The structural patterns (4 regimes, complement symmetry, directed cycle) are likely general. The exact numbers (92% S5→bull, 6-7h duration) are sample-specific and require out-of-sample validation.
- **Subperiod stability is encouraging but not sufficient.** Three 71-day windows all agree on the S5→bull rate (90.7%–92.7%), the structural zeros, and the eigenvalue gap structure. But this is still in-sample subdivision, not true out-of-sample testing.
- **187 C2 episodes** — adequate for confidence intervals but not large. The S4 exit sub-population has only 65 episodes; the rare C2-S5→C0 path has only 10. Small-n paths have wide CIs.
- **No transaction costs, no slippage.** The return numbers are gross. The sub-state signal operates at regime transitions (~6h timescale), so trading costs per unit of capital are low relative to signals at faster timescales.
- **The signal is at regime EXIT, not entry.** You know the regime is C2 in real time. You observe the sub-state in real time. But you don't know it's the exit bar until the next bar changes the macro-regime. In practice, this means the signal confirms on the first bar of the next regime — a 5-minute delay. This is fast enough for position sizing at the 6h timescale.

---

## 6. Method: Binary Trigram Regime Discovery

The analytical framework is general and portable:

1. **Select 3 binary features** from orthogonal information channels (direction, acceleration, energy; or trend at 3 timescales). Verify pairwise correlation |r| < 0.3.
2. **Construct 8-state sequence** via trigram encoding: state = b₂×4 + b₁×2 + b₀.
3. **Estimate T₈** (transition matrix) and **J₈** (jump chain). Compute eigenvalues.
4. **Eigenvalue gap analysis** determines K (natural cluster count). In this data: gap at position 3→4 consistently indicates K=4.
5. **Test for complement symmetry** (x ↔ x⊕7): compute JSD between complement-relabeled rows. If JSD < 0.1 for all pairs, the complement involution is a symmetry.
6. **Collapse to K-state chain** (via Hamming-adjacent pairs for trend bases, or complement pairs for orthogonal bases). Verify lumpability error is small.
7. **Regime-conditioned return analysis**: identify episodes, compute returns by entry/exit sub-state and destination, test subperiod stability.

The framework produces structural invariants (regime count, cycle topology, zero pattern, symmetries) that are properties of the market's dynamics, not artifacts of the feature engineering. The features are inputs; the structure is discovered.

---

## 7. Open Questions / Future Work

1. **Out-of-sample validation.** Run the identical analysis on a new BTC period (post-Feb 2026) and on historical data (2023-2024). Does the S5→bull rate remain >85%?
2. **Multi-asset.** Apply to ETH, SOL, and traditional markets (SPY, QQQ). Is the 4-regime directed cycle universal, or BTC-specific? Does complement symmetry hold?
3. **Timescale variation.** The current basis uses 8h-timescale features. Do 1h or 24h timescales produce similar structure? The theory predicts the same topology at different timescales (with different dwell times).
4. **Real-time regime indicator.** Build a live indicator that tracks: (a) current macro-regime, (b) current sub-state, (c) duration in current regime. The S5 sub-state within C2 after >median duration is the highest-confidence bull signal.
5. **Position sizing.** S5-exit C2 has 92% directional accuracy but ~0.26% mean return. Can position sizing exploit the asymmetry (small positions on S4 exits, larger on S5)?
6. **Complement symmetry across bases.** Confirmed for Basis D. Test whether it holds for other orthogonal channel selections. If universal, it constrains the space of valid models.
7. **The 4-cycle as market microstructure.** The bear→reversal→bull→pullback cycle is the familiar trend-cycle. The contribution here is quantifying the transition probabilities and forbidden transitions with a structural (not fitted) model.

---

## Appendix: Key Numbers Reference

| Quantity | Value | Source |
|----------|-------|--------|
| Downsampled bars | 61,920 | Phase 1 |
| Price range | $60,024–$125,978 | Phase 1 |
| Regime episodes (clean) | 794 | Phase 4 |
| Natural cluster count K | 4 (all bases) | Phase 1, 2 |
| K=4 lumpability error | 0.0000837 | Phase 3 |
| K=5 best lumpability error | 0.00160 (19× worse) | Phase 3 |
| Complement-pair JSD range | 0.046–0.087 | Phase 2 |
| T₈ degenerate eigenvalue pairs | (0.968, 0.968), (0.957, 0.957) | Phase 2 |
| C2-S5 → bull rate | 91.8% [86%, 96%] | Phase 4 |
| C2-S4 → bull rate | 49.2% [38%, 61%] | Phase 4 |
| S5 subperiod stability | 90.7%–92.7% | Phase 4 |
| C2-S5 exit mean return | +0.20% | Phase 4 |
| C2-S4 exit mean return | −0.81% | Phase 4 |
| C1→C3 breakthrough return | +1.09% | Phase 4 |
| C1→C0 failure return | −0.25% | Phase 4 |
| C1 unconditional long EV | +0.018% | Phase 4 |
| C1 S3-conditioned long EV | +0.14% (n=69) | Phase 4 |
| Mean regime duration | 6.1–6.9h | Phase 4 |
| Intra-episode S4↔S5 flips | 3.1 per episode | Phase 5 |
| Confirmed-flip trade edge | +0.005% (not tradeable) | Phase 5 |
| Zero-flip C2 episodes (S5-entry) | 11/11 → bull (100%) | Phase 6 |
| Zero-flip C2 episodes (S4-entry) | 17 (never recovered) | Phase 5/6 |
| C2-S5 → C3 forward return | +0.09%, 7.6h | Phase 6 |
| C2-S4 → C3 forward return | −0.17%, 4.3h | Phase 6 |
| C3-S7 → C2 forward return | +0.06% (orderly pullback) | Phase 6 |
| C3-S6 → C2 forward return | −0.24% (sharp pullback) | Phase 6 |

---

*Analysis completed March 2026. All computations in UTC. Scripts and raw outputs in `logos/markets/01–06_*.py` and `memories/markets/*_output.txt`.*
