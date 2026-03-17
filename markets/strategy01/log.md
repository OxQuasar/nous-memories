# Strategy 01: regime_cycle

## Current State: v3.0 — Long-Only Baseline (FINAL)

File: `~/henry/callandor/strategy/strategies/regime_cycle.go`
Version: 3.0.0 (code reverted and verified)

### Model
4-regime directed cycle from sign(trend_8h) × sign(trend_48h):
- C0 (Bear): both negative → flat
- C1 (Reversal): 8h+, 48h- → flat
- C2 (Pullback): 8h-, 48h+ → hold through (81% → C3)
- C3 (Bull): both positive → long 1.0

Entry on C3 only. Exit on C0/C1. Hold through C2.
8% spot stop loss (insurance, never triggered in backtests).
Full-cycle cooldown after stop (must see C0/C1 before re-entering C3).
5-minute regime debounce (prevents per-second boundary flicker).

### Backtest Results (v3.0, 8% stop, -p 2)

| Period | Dates | Trades | WR | PnL |
|--------|-------|--------|-----|-----|
| P1 | Oct 2025 | 7 | 57% | -1.03% |
| P2 | Nov-Dec 2025 | 6 | 33% | -4.92% |
| P3 | Jan 2026 | 5 | 20% | +2.21% |
| Fwd | Feb-Mar 2026 | 5 | 60% | +7.95% |
| **Total** | | **23** | **43%** | **+4.18%** |

### Exit Type Decomposition

| Exit Type | Trades | WR | Total PnL | Avg PnL |
|-----------|--------|-----|-----------|---------|
| XC1 (Reversal) | 10 | 70% | +38.16% | +3.82% |
| XC0 (Bear) | 13 | 23% | -33.98% | -2.61% |

---

## Governing Principle: Fee-Constrained Signal

**The fee structure (0.18% round-trip) sets a floor: ~0.36% gross per trade minimum.** The regime model produces 5-7 signals per month. Every feature that increases trade count without proportionally increasing gross-per-trade is value-destructive.

v3.0 economics:
- Gross: +8.32% (23 trades × +0.36% avg)
- Fees: -4.14% (23 trades × 0.18%)
- Net: +4.18% (edge-to-fee ratio 2:1)

**Development metric: gross-per-trade, not total PnL.** Any proposed feature must show it increases or preserves gross-per-trade.

---

## Version History

### v3.2 (REJECTED — C1 breakthrough entries)
- Added 0.5 exposure entries in C1 when P(breakthrough) > 0.50
- **Result: -13.38% (vs v3.0's +4.18%)**
- 72 C1 trades: 14 upgrades (+53.61%), 57 failures (-35.03%), 1 stop (-16.33%)
- **Value trap**: successful breakthroughs captured first bull phase at 0.5 exposure, reducing subsequent C3 capture. The 0.5/1.0 split structurally loses value vs full 1.0 capture.
- C3 trades degraded: -14.51% (vs +4.18% in v3.0)
- Fee drag: 72 trades × 0.18% = ~12.96%
- Logs: `/tmp/rc7_p{1,2,3}.log`, `/tmp/rc7_fwd.log`

### v3.1 (REJECTED — C0 shorts with flip mechanism)
- Added C0 short exposure with symmetric stop and cooldown
- **Result: +1.85% (worse than v3.0's +4.18%)**
- Short signal real: +14.89% gross from 68 trades, fees -10.88% → net +4.01%
- **Longs degraded**: -11.37% vs +4.18%. Flip mechanism changed long entry timing.
- Sub-6h shorts: 28 trades, -23.05% net (uniformly destructive)
- 6h+ shorts: 40 trades, +27.06% net (positive all 4 periods)
- Lesson: shorts interact with long execution via flip mechanism. Not additive.
- Logs: `/tmp/rc6_p{1,2,3}.log`, `/tmp/rc6_fwd.log`

### v3.0 (CURRENT)
- Stop: 8% spot (was 3%) + full-cycle cooldown after stop
- Result: +4.18% (was -5.59% at 3% stop), zero stop-outs (was 6)
- Simple long-only: C3 enter, C2 hold, C0/C1 exit
- IsSet() bug fix — modules correctly disabled, 3× backtest speedup (~2 min vs ~50 min)
- Logs: `/tmp/rc5_p{1,2,3}.log`, `/tmp/rc5_fwd.log`

### v2.1
- Initial implementation: C3 long, C0/C1 exit, hold C2, 3% stop
- Result: -5.59%, 6 stop-outs at -37.12% combined
- Stop loss fired during indicator lag (trend_8h needs hours to confirm)

---

## Next Steps

### 1. Statistical Confidence (immediate)
Run v3.0 on full IS period (~30 weeks, Jul 2025 – Feb 2026). Need 45+ trades to test whether +0.36% gross per trade is distinguishable from zero at 95% CI.

### 2. Deploy (if confirmed)
v3.0 is simple enough to be robust: 4 states, 2 actions (long or flat), 1 stop. Forward data is the only true OOS validation.

### 3. Entry Quality (v4)
Improve per-trade quality without increasing trade count:
- Better entries within confirmed C3 (microstructure timing → higher gross)
- Position sizing by trend_8h magnitude at entry (higher conviction → bigger position)

### 4. C0 Shorts Redesign (deferred)
Requirements for viable shorts:
- Isolated execution (no flip mechanism — separate from long logic entirely)
- Context-gated (only after XC0 exit, or only 6h+ C0 episodes)
- Must show >0.36% gross per short trade after duration filter
- Gate: longs must not degrade when shorts are added

---

## Key Learnings (3 iterations)

1. **Regime signal produces real alpha** (+38.16% from 10 XC1 exits). This is the entire edge.
2. **Stop loss must match signal timescale** — 3% is noise for 8h OLS. 8% is insurance-only.
3. **Exit type > period** for decomposition. XC1 vs XC0 is the structural lens.
4. **Fee structure is the binding constraint.** 0.18% round-trip requires >0.36% gross. Trade count increases are destructive.
5. **Complexity must be isolated.** Both shorts (flip mechanism) and breakthroughs (exposure split) degraded the core C3 long signal through interaction effects.
6. **Sub-6h regime episodes are noise** for trading purposes, even when regime detection is correct.
7. **10× scale factor** between simulator (DS30) and research (5-min) trend units.

## Infrastructure Notes

- IsSet() bug fix in interface.go — strategies with all-false module flags
- VPManager nil guard in trademgr.go and callandor.go
- Sentinel nil guard in sentinel.go
- PnLPercent in TradeResult includes leverage and fees but NOT exposure scaling
