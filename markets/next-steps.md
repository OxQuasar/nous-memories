# Next Steps: Regime Model Development

## Current State — v3.0 Baselined, Boundary Study Cycle 1 Complete

4-regime directed cycle validated across BTC and ETH. Strategy v3.0 (long-only, +4.18% over 16 weeks) establishes baseline. Edge is thin (2:1 edge-to-fee) and concentrated in XC1 exits. First boundary study cycle complete: →C2 outcome fully characterized, real signal found but not actionable at current fees.

### The Loop

```
1. Study boundaries (analysis)
2. Refine model and strategy
3. Backtest strategy
4. Find weaknesses
5. Back to 1
```

This is the main work. Keep looping and refining. Each cycle produces: one analysis, one insight (or confirmed negative), and either a strategy change or a documented reason not to change.

---

## Next Cycle: →C3 Entry Quality Study

### Question
Can we time entries better within confirmed C3 (bull)? Improve gross/trade without adding trades.

### Why this is next
- Targets per-trade quality, not trade count (avoids the fee trap discovered in cycle 1)
- C3 entry quality doesn't create extra trades — it modifies existing entry timing
- 189 C3 episodes available in IS data
- The boundary study design (boundary-study.md) already scopes this as priority #2

### Approach
Same framework as →C2 study: snapshot indicators at C3 entry, split by outcome metric (trade PnL, duration, exit type), rank by AUC. But the outcome variable is different — not binary (C3 doesn't have a simple success/fail), so needs duration or PnL-based outcome definition.

### Open questions before execution
- What's the right outcome variable? Episode duration? Price change during episode? Next exit type (XC1 vs XC0)?
- Should we condition on entry context (which regime preceded C3)?
- Which indicator groups? Same initial set (trends, vol, CVD) or expand to microstructure/order flow?

---

## Ideas Backlog

### Strategy Refinements
- ~~**C2 early exit:** Filter bad pullbacks using intermediate trends~~ → DONE (Cycle 1: real signal, not actionable at current fees)
- **C3 entry timing:** Microstructure signals for better entry within confirmed bull ← NEXT
- **Position sizing:** Scale by transition quality (trend magnitude, vol level, order flow confirmation)
- **C0 shorts (isolated):** Separate execution from long logic, 6h+ duration filter, context-gated
- **C1 breakthrough entry redesign:** Fix the value trap (full size or nothing, not 0.5/1.0 split)
- **Duration filter:** Sub-6h episodes are noise — filter or weight by expected duration

### Model Extensions
- **Multi-indicator regime:** Replace 2-bit sign with richer state using vol/order flow
- **Transition probability refinement:** Condition base rates on indicator context (not all C2s are equal — we now know trend_24h differentiates them, even if not actionable)
- **Temporal patterns:** Do certain hours/sessions have different transition probabilities?
- **Failure clustering:** Do bad C2 outcomes cluster in time? (risk management)

### Validation
- **Full IS backtest:** Run current strategy on full Jul 2025 – Feb 2026 for 45+ trades and statistical confidence
- **Additional assets:** PENGU (different vol profile), traditional markets (different microstructure)
- **Forward reconciliation:** 2.17% gap between FuturesPM and TradeCapture on forward data

### Shelved (Real Signal, Not Actionable)
- **trend_24h at C2 entry:** AUC 0.765 for C2 outcome, independent of both trend_8h (r=0.036) and trend_48h (r=0.460). Operational split: 85.4% vs 44.4% success rate by sign. But C2 price moves (0.2-0.6%) ≈ fee cost (0.36% RT), so exit filter EV is -6.45%. Becomes actionable if fees decrease or a non-fee-generating use emerges.

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

### v3.0 Baseline

| Metric | Value |
|--------|-------|
| Total PnL | +4.18% (16 weeks) |
| Trades | 23 |
| Win rate | 43% |
| Gross/trade | +0.36% |
| Edge-to-fee | 2:1 |
| XC1 exits | +38.16% (10 trades, 70% WR) |
| XC0 exits | -33.98% (13 trades, 23% WR) |

Strategy: long 1.0 in C3, hold through C2, flat in C0/C1. 8% stop (insurance). 5-min debounce.

### Key Constraints
- **Fee floor:** 0.18% RT → >0.36% gross/trade minimum
- **Interaction effects dominate:** v3.1 and v3.2 both degraded core signal through indirect mechanisms
- **Sub-6h episodes are noise** for trading
- **The regime model labels states, not timing.** Entry/exit timing is the improvement axis.
- **C2 episode price moves ≈ fee cost.** Any filter that adds round-trips during C2 is structurally negative EV.

---

## DONE

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

### Strategy Development (Phase 17) — v3.0 BASELINED

| Version | Change | Result | Trades | Lesson |
|---------|--------|--------|--------|--------|
| v2.1 | 3% stop | -5.59% | 29 | Stop fires during indicator lag |
| v3.0 | 8% stop + cooldown | **+4.18%** | 23 | Zero stop-outs, regime exits only |
| v3.1 | +C0 shorts (flip) | +1.85% | 92 | Longs degraded, fees killed it |
| v3.2 | +C1 breakthrough | -13.38% | 97 | Value trap, splits C3 capture |

### Simulator Validation (Phase 16) — PASS
Zero topology violations. Exit AUC 0.992/0.964 (IS), 1.000/0.983 (forward). 10× scale factor discovered and handled.

### Research Phases 1-15 — COMPLETE
K=4 topology, complement symmetry, exit prediction, OOS validation, ETH cross-asset transfer. See `findings.md`, `investigation-1.md`, `exploration-log.md`.
