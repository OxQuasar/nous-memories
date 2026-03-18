# Next Steps: Regime Model Development

## Current State — Directional Trading Research COMPLETE, No Tradeable Edge Found

All directional trading avenues for the 2-bit regime model have been systematically tested and closed:

| Avenue | Result | Evidence |
|--------|--------|----------|
| C3 confirmed entry (v3.0) | Gross negative (−0.555%) | Script 19 |
| C2 exit filter | Real signal, negative EV | Script 17c |
| C3 entry quality | Clean null (24 indicators) | Script 18 |
| C1 breakthrough EV | Logistic at chance at entry | Script 20 |
| C0 shorts (v3.1) | Interaction degraded longs | Strategy log |
| C1 entry (v3.2) | Value trap, −13.38% | Strategy log |
| Longer timescale (24h/96h) | Exit signal collapses (2.8pp gap) | Findings §6 |

The 2-bit regime model is a **validated state classifier** (K=4 topology, AUC 0.957+, cross-asset) that does not produce a tradeable directional strategy at current timescales and fees. Its value is in state classification — risk labeling, position sizing — for strategies that source their edge elsewhere.

---

## Why Directional Trading Failed

### Core failure: state identification ≠ tradeable edge
The regime model correctly identifies market states — topology is validated, transition structure is real, exit AUCs are high. But:
- C3 episodes are too noisy to extract consistent profit (mean price change ≈ 0%)
- XC1 exits (the supposed edge source) are 56% WR on full sample (not 70%)
- 3 outlier wins (+24.67%, +20.89%, +10.26%) drive the XC1 total positive
- XC0 exits bleed −1.88%/trade on 31 trades, overwhelming any XC1 edge

### Structural impossibility: entry-bar prediction with trend indicators
Scripts 18 and 20 converge on one structural insight: **backward-looking trend indicators at regime entry contain no forward-predictive information about episode quality.** At regime entry, the defining trend variable has *just* crossed its threshold — its magnitude is minimal and uninformative. The logistic models work at exits (AUC 0.96+) precisely because by exit time, the trend has developed magnitude. This generalizes: any proposal to predict episode quality from entry-bar snapshots of OLS trends, vol, CVD, or microstructure is pre-closed. Entry-time prediction requires a fundamentally different information source.

### Duration unpredictability
The model tells you *what state you're in*, not *how long you'll stay there*. Sub-6h episodes lose money (−0.49% mean) but no entry-bar indicator predicts duration (Script 18).

---

## Pivot: Regime Model as Infrastructure

The regime model's value is as a **risk overlay**, not a signal source. The question shifts from "how to trade regimes" to "what strategy sources its own edge, and how does regime-conditioned sizing/filtering improve it?"

### Concrete pivot path
1. **Risk overlay for other strategies:** Regime-conditioned position sizing, stop placement, or entry gating for strategies with independently-sourced edge
2. **Different asset/fee structure:** The model may work on lower-fee venues or assets with larger regime moves
3. **Non-directional uses:** Vol regime classification for options strategies, funding rate arbitrage gating

### Model extension backlog (flagged: these don't address the core failure)
These items enrich the state classifier but do NOT solve entry-timing — they would still face the same structural impossibility of entry-bar prediction:
- **Multi-indicator regime:** Richer state using vol/order flow → better labeling, same entry problem
- **Transition probability refinement:** Conditional base rates → better probability estimates, same entry problem
- **Temporal patterns:** Session-based transition rates → incremental, doesn't change entry economics

---

## Ideas Backlog

### Closed — Directional Trading (all avenues exhausted)
- ~~C2 early exit~~ → DONE (Cycle 1: real signal, negative EV at current fees)
- ~~C3 entry timing~~ → DONE (Cycle 2: clean null, 24 indicators)
- ~~v3.0 deployment~~ → DONE (Script 19: no edge, −36.76%)
- ~~C1 breakthrough EV~~ → DONE (Script 20: logistic AUC=0.533 at entry)
- ~~Position sizing~~ → Moot (no base edge to scale)
- ~~Duration filter~~ → Confirmed effect, not predictable at entry
- ~~C0 shorts~~ → Interaction-degraded in v3.1; isolated evaluation would face same entry-timing problem
- ~~Longer timescale (24h/96h)~~ → Exit signal collapses (Findings §6)

### Open — Pivot Track (regime model as infrastructure)
- **Risk overlay prototype:** Apply regime labels to an independently-edged strategy, measure improvement
- **Lower-fee venue test:** Same model, different fee structure — does the math change?
- **Failure clustering analysis:** Do bad outcomes cluster in time? (risk management value even without directional edge)
- **Additional assets:** PENGU (different vol profile), non-crypto (different microstructure)

### Shelved (Real Signal, Not Actionable)
- **trend_24h at C2 entry:** AUC 0.765, independent of trend_8h/trend_48h. But C2 price moves ≈ fee cost → negative EV. Becomes actionable if fees decrease or non-fee use emerges.

---

## Reference

### Production Model

**Regime detection:** 2-bit macro (sign of trend_8h × sign of trend_48h)

| Macro | trend_8h | trend_48h | Regime |
|-------|----------|-----------|--------|
| 0 | − | − | C0 Bear |
| 1 | + | − | C1 Reversal |
| 2 | − | + | C2 Pullback |
| 3 | + | + | C3 Bull |

**Scale factor:** Simulator trends are 10× smaller than research convention (DS30 vs 5-min bars).

**Exit scoring (simulator units):**
```
C2: P(bull) = σ(5.209 + 14770 × trend_1h + 3485330 × trend_8h)
C1: P(bt)   = σ(−4.890 + 31380 × trend_1h + 4215050 × trend_8h)
```

### v3.0 Results

**Prior baseline (−p 2 rotation, biased sample):**
| Metric | Value |
|--------|-------|
| Total PnL | +4.18% (16 weeks) |
| Trades | 23 |
| Win rate | 43% |
| Gross/trade | +0.36% |

**Full IS backtest (complete period):**
| Metric | Value |
|--------|-------|
| Total PnL | **−36.76%** (30 weeks) |
| Trades | 50 |
| Win rate | 40% |
| Gross/trade | **−0.555%** |
| 95% CI | [−2.47%, +1.36%] |
| t-test p-value | 0.563 |
| XC1 exits | +37.62% (18 trades, 56% WR) |
| XC0 exits | −58.19% (31 trades, 32% WR) |
| Stop-outs | 1 (−16.19%) |

Strategy: long 1.0 in C3, hold through C2, flat in C0/C1. 8% stop (insurance). 5-min debounce.
**Verdict: No detectable edge. Prior baseline was sample artifact.**

### Key Constraints
- **No edge detected:** Full IS backtest shows gross/trade is negative (−0.555%), not just sub-fee
- **Fee floor:** 0.18% RT → >0.36% gross/trade minimum (strategy doesn't clear even gross=0)
- **XC1 concentration risk:** 3 outlier wins drive XC1 positive; remove them and total collapses further
- **Sub-6h episodes are noise** for trading (−0.49% mean) but not predictable at entry
- **The regime model labels states, not timing.** No entry-bar indicator predicts episode quality
- **Entry-bar prediction pre-closed:** Backward-looking trend indicators at regime entry carry no forward-predictive info (Scripts 18, 20). Defining trend just crossed threshold → magnitude minimal. Any entry-time prediction requires a fundamentally different information source, not a different indicator in the same family.
- **C2 episode price moves ≈ fee cost.** Any filter that adds round-trips during C2 is structurally negative EV
- **Sample artifact:** −p 2 rotation selects specific weeks, producing biased trade subsets

---

## DONE

### C1 Breakthrough EV: Logistic at Chance Level (Script 20)

**Finding: NOT ACTIONABLE.** The C1 logistic model (AUC 0.965 for exit prediction) has AUC=0.533 when applied at C1 entry — effectively chance level.
- 204 C1 episodes: 22.5% breakthrough rate (46→C3, 158→C0)
- P(bt) distribution: 187/204 episodes at P < 0.10 (logistic says "no info" at entry)
- P > 0.8 bin: n=10, 30% BT rate — actually *lower* than P > 0.1 bin's 29.4%
- "Positive EV" at high confidence bins is driven by failures having positive price changes (noise at n=10)
- Unconditional C1 price change: +0.039% (near zero)

**Mechanistic explanation:** The C1 logistic was designed for EXIT prediction — it measures trend_8h magnitude near the C1→C0/C3 transition point. At C1 *entry*, trend_8h just crossed zero (small positive by construction), so the logistic correctly says "not enough information yet." This is consistent with Script 18's finding that entry-bar snapshots don't predict episode outcomes.

**Closes:** C1 breakthrough EV from ideas backlog. The logistic model cannot be repurposed for entry prediction.

Script: `20_c1_breakthrough_ev.py` | Output: `20_c1_breakthrough_ev_output.txt`

### Full IS Backtest: v3.0 Invalidated (Script 19)

**Finding: NO DETECTABLE EDGE.** 50 trades over full IS period (Jul 2025 – Feb 2026).
- Mean gross/trade: −0.555% (95% CI: [−2.47%, +1.36%], t-test p=0.563)
- Total PnL: −36.76% net
- Wilcoxon p=0.081 (also fails to reject)
- Prior +4.18% baseline (23 trades, −p 2 rotation) was sample artifact
- XC1 exits: 56% WR (not 70%), driven by 3 large outliers
- XC0 exits: 31 trades at −1.88% avg, overwhelming any XC1 edge
- 1 stop-out at −16.19%; even excluding it, total is −20.57%
- Temporal split: first half −38.80%, second half +2.04% (unstable)

**Closes:** v3.0 deployment. Strategy does not clear even the gross=0 bar.

Output: `19_full_is_backtest_output.txt`

### Boundary Study Cycle 2: →C3 Entry Quality (Script 18)

**Finding: CLEAN NULL.** No entry-bar indicator predicts C3 episode quality after Bonferroni correction (24 indicators, n=189 episodes).

**Best suggestive signals (sub-Bonferroni):**
- realized_vol_24h: ρ=−0.20 with episode price change (p_raw=0.006, p_corr=0.14)
- trend_1h: AUC=0.623 for duration ≥6h (p_raw=0.004, p_corr=0.085)

**Null results (high confidence):**
- Microstructure (ob_total_ratio, spread_bps, depth_asymmetry, liquidity_shift, ob_imbalance_slope): uniformly AUC ≈ 0.50, no signal
- All trends (4h, 8h, 16h, 24h, 48h, 96h): |ρ| < 0.19 with price change, all p_corr > 0.25
- Volume/CVD: null (same as cycle 1)
- Trend-of-trends: structurally zero in C3 regime (same as C2)
- Predecessor regime (C2 vs C1): AUC=0.581 for duration, not significant (p_corr=0.24)

**Duration finding (confirmed, not predictable):**
- Sub-6h C3 episodes: mean price change −0.49%, median −0.37%
- ≥6h C3 episodes: mean +0.41%, median +0.16%
- Duration ≥6h fraction: 51.3% (median split near 6h)
- But no indicator at entry predicts which episodes will be long vs short

**Mechanistic interpretation:** C3 episode quality is exogenously determined during the episode, not endogenously set at entry. The coupled-oscillator model explains this: at C3 entry, the fast trend has committed (positive by construction), and the outcome depends on whether the medium trend stays positive — which is a function of future price action, not current state.

**Closes:** "C3 entry timing" from ideas backlog. Entry-bar snapshot doesn't contain episode quality information.

Script: `18_c3_entry_quality.py` | Output: `18_c3_entry_quality_output.txt`

### Boundary Study Cycle 1: →C2 Outcome (Scripts 17, 17b, 17c)

**Finding:** trend_24h carries strong, independent information about C2 pullback outcomes.
- AUC 0.765 (p=3e-6 after Bonferroni), Cohen's d=0.815
- Independent of trend_8h (r=0.036) AND trend_48h (r=0.460)
- Split-half stable (0.77/0.76)
- Forward-consistent (93.8% vs 70.0%, n=26)
- Signal is primarily binary (sign), with continuous tail in positive group (within-AUC 0.680)

**Null results (high confidence):**
- Volatility (OLS + realized, all timescales): AUC 0.50-0.54, no signal
- Volume/CVD (cvd_slope_5m, cvd_div_15m, vwap_divergence): AUC 0.50-0.56, no signal
- Trend-of-trends (tot_4h/8h/24h): structurally zero during C2 regime

**Operationalization: NOT ACTIONABLE at current fees.**
- C2 exit filter (trend_24h ≤ 0): EV = -6.45%. C2 price moves (avg 0.2-0.6%) ≈ fee cost (0.36% RT).
- Stack depth filter (depth < 2): EV = -11.61%. Wider net, worse economics.
- The filter correctly identifies losers but the economics don't support extra round-trips.

**Mechanistic insight:** trend_24h measures how far the negative signal has propagated up the timescale hierarchy. When only trend_8h is negative (trend_24h still positive), the pullback is shallow and the bull structure is intact. When trend_24h is also negative, the deeper structure is eroding. This is the coupled-oscillator mechanism: intermediate trends measure structural depth of pullback.

Scripts: `17_c2_boundary_study.py`, `17b_c2_followup.py`, `17c_c2_filter_ev.py`
Output: `17_c2_boundary_output.txt`, `17b_c2_followup_output.txt`, `17c_c2_filter_ev_output.txt`

### Strategy Development (Phase 17) — v3.0 INVALIDATED

| Version | Change | Result | Trades | Lesson |
|---------|--------|--------|--------|--------|
| v2.1 | 3% stop | -5.59% | 29 | Stop fires during indicator lag |
| v3.0 (−p 2) | 8% stop + cooldown | +4.18% | 23 | Sample artifact (biased week rotation) |
| v3.0 (full IS) | same | **-36.76%** | 50 | **No edge.** Gross/trade = -0.555% |
| v3.1 | +C0 shorts (flip) | +1.85% | 92 | Longs degraded, fees killed it |
| v3.2 | +C1 breakthrough | -13.38% | 97 | Value trap, splits C3 capture |

### Simulator Validation (Phase 16) — PASS
Zero topology violations. Exit AUC 0.992/0.964 (IS), 1.000/0.983 (forward). 10× scale factor discovered and handled.

### Research Phases 1-15 — COMPLETE
K=4 topology, complement symmetry, exit prediction, OOS validation, ETH cross-asset transfer. See `findings.md`, `investigation-1.md`, `exploration-log.md`.
