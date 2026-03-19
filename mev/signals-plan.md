# DeFi Signals Exploration Plan

## Goal

Test whether on-chain DeFi metrics produce actionable leading signals for ETH price direction.

## Baseline

ETH price: 1,539 daily / 36,734 hourly points, 2022-01-01 → 2026-03-19. `data/eth_price.csv`, `data/eth_price_1h.csv`. Script: `eth_price.py`.

## Method

Started with cross-correlation. Proved wrong tool for regime transitions. Shifted to conditional/threshold-based tests and temporal structure analysis. Signal "works" if it fires before price moves with enough consistency to be actionable.

Tools: Python, pandas, numpy, scipy. DefiLlama API + free public RPC + Binance data archive.

## Primary Finding

**Liquidation magnitude as capitulation classifier.** When daily liquidation volume > 90th percentile, classify by magnitude relative to trailing 180d window.

Best classifier (M1-P97: today ≥ 97th percentile of trailing 180d):

| Class | N | 7d Median Return | % Negative |
|---|---|---|---|
| Concentrated (extreme spike, ≥97th pctl) | 38 | +2.36% | 39.5% |
| Distributed (moderate, <97th pctl) | 75 | -3.31% | 68.0% |

Spread: 5.67pp. Mann-Whitney p=0.003. Computable in real-time from free RPC data.

**Regime-invariance stress test (Iteration 8):** Signal *strengthened* under regime-invariant reclassification (180d window eliminates trailing-7d denominator contamination). Survived: within-bear-market control (+7.2pp, p=0.001), momentum control (excess return +10.9pp, p=0.0003), episode-level clustering (27 independent episodes, +19.5pp, p=0.019). Not mean-reversion: concentrated days have deeper prior 7d drawdowns yet better forward returns.

**Revised interpretation:** This is a magnitude-based climactic volume pattern measured on-chain, not a novel "temporal structure" signal. The original framing (spike vs sequence) was wrong — pure shape-based classification (M2-Peak) fails (p=0.37). The edge, if any, is measurement precision from on-chain event logs rather than a structurally unique DeFi mechanism.

## Secondary Finding

**Perp → lending temporal lead.** Binance ETHUSDT open interest drops (proxy for perp liquidations) precede peak lending liquidation activity by a corrected median of **37 hours**. 16/17 episodes (94%), price typically fell **10.9%** between OI drop and lending peak. This is a genuine early warning — further decline is still coming when the OI signal fires.

Caveat: **~30% precision** at 3% OI drop threshold (~20 false alarms/year vs ~8 true episodes). The leverage hierarchy between perps (5-50x) and lending (1.5-3x) creates measurable temporal structure that the intra-lending protocol hierarchy (Maker-Aave gap) does not.

---

## Remaining Open — Deprioritized

_The investigation's core conclusions are established. The items below would refine precision or extend applicability, but are unlikely to change the fundamental findings._

### B. L2 Universality Test
- **Question**: Does the magnitude classifier hold on Aave liquidations on Arbitrum, Base, Optimism?
- **Status**: Deprioritized. Would increase sample size (27 → potentially ~40 episodes) but L2 events likely correlate with L1 (same market), limiting independence. Core finding already survives multiple stress tests.

### E. Cross-Collateral Contagion
- **Question**: When ETH liquidations are distributed AND WBTC/other collateral liquidations appear in the same window, does that predict worse outcomes?
- **Status**: Deprioritized. Would add a severity classifier layer. Interesting but marginal given sample size limits.

### H. Options/IV Overlay
- **Question**: Is the volatility expansion around capitulation events already priced into options?
- **Status**: Deprioritized. Determines options strategy viability, not core signal validity.

### F. Real-Time Monitor
- **Question**: Can we operationalize the magnitude classifier as a live signal?
- **Status**: Most valuable remaining work if the signal is to be used. Would combine: (1) real-time lending liquidation volume from RPC event logs, (2) Binance OI stream for perp lead, (3) utilization APY for regime pre-classification.

### G. USDT/USDC Supply (capital inflow signal)
- **Question**: Does major stablecoin supply predict inflows that lead price?
- **Status**: Deprioritized. Different mechanism from leverage signals. Lower expected yield given DAI/GHO results.

---

## Done — Killed or Characterized

### ✦ Liquidation Magnitude Classifier — primary finding, stress-tested
- Scripts: `liquidation_events.py`, `liquidation_expand.py`, `volatility_signal.py`, `regime_test.py`
- Data: `data/liquidation_events_combined.csv`, `data/volatility_signal.csv`, `data/regime_test_results.txt`
- 36,237 events, $2.02B, Aave v2+v3 / Compound v2+v3 / Maker, 1,524 days
- Best method: M1-P97 (180d window, ≥97th pctl). Spread +5.67pp, p=0.003.
- Survives: regime-invariant reclassification, bear-market control, momentum control, episode clustering
- Limitation: 27 independent episodes, ~5-6 distributed-dominant. This is the climactic volume pattern measured on-chain with higher precision than traditional exchange volume.

### ✦ Perp → Lending Lead — genuine early warning, noisy
- Script: `perp_lead.py`, Data: `data/binance_oi_episodes.csv`, `data/perp_lead_results.txt`
- Proxy: Binance ETHUSDT 5-min OI snapshots. Hourly OI drop as perp liquidation proxy.
- 16/17 episodes (94%): perp OI drops before lending peak. Corrected median lead: 37h.
- Price fell median 10.9% between OI drop and lending peak — genuine warning, not same-event measurement.
- False positive: ~20/year at 3% threshold, ~30% precision. Enrichment 3.9x vs control periods.
- Caveat: OI is an imperfect proxy. Direct liquidation data would refine.

### ✦ Utilization → Liquidation Regime — characterized, inverse of hypothesis
- Script: `utilization_signal.py`, Data: `data/utilization_apy.csv`, `data/utilization_results.txt`
- High utilization → concentrated (capitulation); Low utilization → distributed (cascade). p=0.001.
- Regime-predictive, not time-predictive (no temporal lead in cross-correlation).
- Monotonic gradient: Q1 (low APY) = 64% distributed; Q4 (high APY) = 12% distributed.

### ✦ Protocol Cascade Sequencing — no consistent ordering within lending
- Script: `cascade_sequence.py`, Data: `data/cascade_sequence_results.txt`
- No architecturally-determined cascade across Maker/Compound/Aave.
- Aave fires first most often (48%) due to volume dominance, not structural ordering.
- Sequential activation (≥2d spread) correlates with worse outcomes but is the same signal as distributed episodes.
- The Maker-Aave collateral ratio gap is too small to produce consistent temporal ordering.

### ✦ Liquidation Walls — legible snapshot, not backtestable
- Script: `liquidation_walls.py`
- Data: `data/liquidation_bins.csv`, `data/liquidation_top_positions.csv`
- $2.16B total, walls at $1,300-$1,600. Two whale positions (94% of value).

### ✦ Volatility Signal — real but modest
- r=0.235 log-volume → 7d realized vol. 1d abs returns: quiet 2.36% → extreme 4.62%.
- Supporting evidence for fragility thesis, not standalone.

### ✗ Stablecoin Supply (DAI/GHO/USDS) — killed, lags
- Script: `stablecoin_supply.py`, Data: `data/stablecoin_supply.csv`
- Combined supply lags ETH by ~8 days. DAI concurrent (r=0.23). GHO/USDS noise.

### ✗ stETH/ETH Spread — killed, arbitraged away
- Script: `steth_spread.py`, Data: `data/steth_spread.csv`
- Pre-Shanghai: concurrent (r=-0.375). Post-Shanghai: noise.

### ⏸ TVL Divergence — parked, no connection to primary finding
### ⏸ Bridge Flows — parked, no connection to primary finding
