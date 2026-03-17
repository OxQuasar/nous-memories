# Henry Trading Strategies - Current and WIP Log

## Active Strategies

### regime_cycle (v3.0) — Long-Only Regime Following
- **Status**: Baseline validated, pending full IS backtest for statistical confidence
- **File**: `~/henry/callandor/strategy/strategies/regime_cycle.go`
- **Logic**: Long 1.0 in C3 (Bull), hold through C2 (Pullback), flat in C0/C1. 8% spot stop (insurance).
- **Results**: +4.18% over 16 weeks (23 trades, 43% WR). Edge from XC1 exits (+38.16%).
- **Fee constraint**: 0.18% round-trip → min 0.36% gross/trade. Current avg 0.36% (2:1 edge-to-fee).
- **Next**: Full IS backtest (45+ trades), then deploy if confirmed.
- **Detailed log**: `memories/markets/strategy01/log.md`

### Signal Usage

| Signal | Source | Used in v3.0? | Role |
|--------|--------|---------------|------|
| trend_8h sign | OLS 8h / mean price | **Yes** | Regime bit 0: distinguishes Bull/Reversal from Bear/Pullback |
| trend_48h sign | OLS 48h / mean price | **Yes** | Regime bit 1: distinguishes Bull/Pullback from Bear/Reversal |
| Regime state (2-bit) | sign(t8h) × sign(t48h) | **Yes** | C3=enter long, C2=hold, C0/C1=exit |
| Directed cycle topology | Structural property | **Implicit** | No diagonal transitions → hold-through-C2 is safe (81% → C3) |
| trend_1h | OLS 1h / mean price | **No** | Too noisy for regime (flips every ~55 min). Logistic predictor only. |
| P(bull) logistic | σ(5.209 + coefs × trends) | **No** | AUC 0.992 but hold-through-C2 outperforms conditional exit |
| P(breakthrough) logistic | σ(-4.890 + coefs × trends) | **No** | AUC 0.964 but C1 entries are fee-destructive (v3.2 proved) |

**Why unused signals stay unused:** Fee structure (0.18% RT) requires >0.36% gross/trade. Both C1 entries (72 trades, v3.2) and C0 shorts (68 trades, v3.1) diluted gross/trade below this floor. The exit scoring functions (`pBull`, `pBreakthrough`) remain in code for future use (position sizing, monitoring).

## Rejected Variants (with learnings)

| Variant | Change | Result | Why Failed |
|---------|--------|--------|-----------|
| v3.2 | C1 breakthrough (0.5 exp) | -13.38% | Value trap: splits C3 capture at 0.5/1.0 |
| v3.1 | C0 shorts (flip) | +1.85% | Fees + flip mechanism degraded longs (-11.37%) |
| v2.1 | 3% stop | -5.59% | Stop fired during 8h indicator lag |

## Design Principles (learned from 3 iterations)

1. **Gross-per-trade is the metric**, not total PnL. Fee floor = 0.36%.
2. **Trade count increases are destructive** unless gross/trade scales proportionally.
3. **New features must be isolated** — interaction effects dominate direct contribution (v3.1 longs went from +4.18% to -11.37% when shorts were added).
4. **Stop loss must match signal timescale** — 8h OLS indicator needs wide (8%) stop.
5. **The regime model is a state labeler, not a timing tool.** Entry timing within confirmed regimes is the next improvement axis.
6. **Sub-6h regime episodes are noise** for trading purposes. Duration filters needed for any regime-entry feature.
