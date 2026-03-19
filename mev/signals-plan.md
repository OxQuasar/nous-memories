# DeFi Signals Exploration Plan

## Goal

Test whether on-chain DeFi metrics produce actionable leading signals for ETH price direction.

## Baseline

ETH price: 1,539 daily / 36,734 hourly points, 2022-01-01 → 2026-03-19. `data/eth_price.csv`, `data/eth_price_1h.csv`. Script: `eth_price.py`.

## Method

Started with cross-correlation. Proved wrong tool for regime transitions. Shifted to conditional/threshold-based tests and temporal structure analysis. Signal "works" if it fires before price moves with enough consistency to be actionable.

Tools: Python, pandas, numpy, scipy. DefiLlama API + free public RPC.

## Primary Finding

**Liquidation magnitude as capitulation classifier.** When daily liquidation volume > 90th percentile, classify by magnitude relative to trailing 180d window.

Best classifier (M1-P97: today ≥ 97th percentile of trailing 180d):

| Class | N | 7d Median Return | % Negative |
|---|---|---|---|
| Concentrated (extreme spike, ≥97th pctl) | 38 | +2.36% | 39.5% |
| Distributed (moderate, <97th pctl) | 75 | -3.31% | 68.0% |

Spread: 5.67pp. Mann-Whitney p=0.003. Computable in real-time from free RPC data.

**Regime-invariance stress test (Iteration 8):** Signal *strengthened* under regime-invariant reclassification (180d window eliminates trailing-7d denominator contamination). Survived: within-bear-market control (+7.2pp, p=0.001), momentum control (excess return +10.9pp, p=0.0003), episode-level clustering (27 independent episodes, +19.5pp, p=0.019). Concentrated days cluster later in episodes (mean position 0.62 vs 0.42, p=0.006) — position-in-crash contributes but doesn't explain the spread. Not mean-reversion: concentrated days have deeper prior 7d drawdowns yet better forward returns.

**Revised interpretation:** This is a magnitude-based climactic volume pattern measured on-chain, not a novel "temporal structure" signal. The original framing (spike vs sequence) was wrong — pure shape-based classification (M2-Peak) fails (p=0.37). The edge, if any, is measurement precision from on-chain event logs rather than a structurally unique DeFi mechanism.

---

## Open — Next Investigations

### C. Protocol Cascade Sequencing (highest priority)
- **Question**: Do Maker/Compound liquidations systematically precede Aave liquidations by hours/days?
- **Why**: Different collateral ratios and liquidation thresholds mean protocols should liquidate in order. If there's a measurable lag, earlier protocols become a leading indicator for later ones. This is architecturally determined and regime-invariant — the first genuinely structural test remaining.
- **Source**: Already collected in `data/liquidation_events_combined.csv` — analyze intra-day/inter-day ordering across protocols
- **Cost**: Zero — data exists, just needs temporal analysis at finer resolution

### D. Perp Liquidation as Leading Edge (high priority)
- **Question**: Do perpetual DEX liquidation spikes precede lending protocol liquidation spikes?
- **Why**: Perps run higher leverage, should liquidate first. If perp spikes lead lending spikes by even hours, that's a faster-reacting upstream trigger for the magnitude signal. Tests whether the DeFi leverage hierarchy creates genuine temporal structure that the magnitude classifier misses.
- **Source**: Hyperliquid (public API), dYdX, GMX event logs
- **Note**: Hyperliquid data is the most accessible.

### B. L2 Universality Test
- **Question**: Does the magnitude classifier hold on Aave liquidations on Arbitrum, Base, Optimism?
- **Why**: Tests mechanism universality. Also increases sample size (currently 27 episodes).
- **Source**: Same code, different RPC endpoints
- **Risk**: L2 liquidation events may correlate with L1 (same market conditions), limiting independent sample

### E. Cross-Collateral Contagion
- **Question**: When ETH liquidations are distributed AND WBTC/other collateral liquidations appear in the same window, does that predict worse outcomes?
- **Why**: Multi-collateral distributed = systemic stress. A severity classifier on top of the magnitude classifier.
- **Source**: Same RPC event log approach, filter for WBTC/wstETH collateral seizures

### H. Options/IV Overlay
- **Question**: Is the volatility expansion around capitulation events already priced into options?
- **Why**: If IV spikes before liquidation days, options strategies based on the signal are redundant
- **Source**: Deribit historical IV data (needs sourcing)

### F. Real-Time Monitor
- **Question**: Can we operationalize the magnitude classifier as a live signal?
- **Why**: Shifts from research to usable tool
- **Prerequisite**: Best after C-E determine whether structural content exists beyond climactic volume

### G. USDT/USDC Supply (capital inflow signal)
- **Question**: Does major stablecoin supply predict inflows that lead price?
- **Why**: Different mechanism from DAI/GHO — tracks capital entering crypto, not DeFi leverage
- **Source**: DefiLlama stablecoins API

---

## Done — Killed or Characterized

### ✦ Liquidation Magnitude Classifier — primary finding, stress-tested
- Scripts: `liquidation_events.py`, `liquidation_expand.py`, `volatility_signal.py`, `regime_test.py`
- Data: `data/liquidation_events_combined.csv`, `data/volatility_signal.csv`, `data/regime_test_results.txt`
- 36,237 events, $2.02B, Aave v2+v3 / Compound v2+v3 / Maker, 1,524 days
- Best method: M1-P97 (180d window, ≥97th pctl). Spread +5.67pp, p=0.003.
- Survives: regime-invariant reclassification, bear-market control, momentum control, episode clustering
- Limitation: 27 independent episodes, ~5-6 distributed-dominant. May reduce to known climactic volume pattern.

### ✦ Liquidation Walls — legible snapshot, not backtestable
- Script: `liquidation_walls.py`
- Data: `data/liquidation_bins.csv`, `data/liquidation_top_positions.csv`
- $2.16B total, walls at $1,300-$1,600. Two whale positions (94% of value).

### ✦ Volatility Signal — real but modest
- r=0.235 log-volume → 7d realized vol. 1d abs returns: quiet 2.36% → extreme 4.62%.
- Supporting evidence for fragility thesis, not standalone.

### ✦ Utilization → Liquidation Regime — characterized, inverse of hypothesis
- Script: `utilization_signal.py`, Data: `data/utilization_apy.csv`, `data/utilization_results.txt`
- High utilization → concentrated (capitulation); Low utilization → distributed (cascade). p=0.001.
- Regime-predictive, not time-predictive (no temporal lead in cross-correlation).
- Monotonic gradient: Q1 (low APY) = 64% distributed; Q4 (high APY) = 12% distributed.
- Interpretation: crowded leverage liquidates at once (spike); sparse leverage trickles (distributed).

### ✗ Stablecoin Supply (DAI/GHO/USDS) — killed, lags
- Script: `stablecoin_supply.py`, Data: `data/stablecoin_supply.csv`
- Combined supply lags ETH by ~8 days. DAI concurrent (r=0.23). GHO/USDS noise.
- Reflexive loop doesn't close — minted stablecoins disperse rather than feeding back to spot.

### ✗ stETH/ETH Spread — killed, arbitraged away
- Script: `steth_spread.py`, Data: `data/steth_spread.csv`
- Pre-Shanghai: concurrent (r=-0.375). Post-Shanghai: noise.
- Redemption infrastructure destroyed the signal.

### ⏸ TVL Divergence — parked, no connection to primary finding
### ⏸ Bridge Flows — parked, no connection to primary finding
