# DeFi Signals Exploration Plan

## Goal

Test whether on-chain DeFi metrics produce actionable leading signals for ETH price direction.

## Answer

The data is legible and classifiable, but constitutes a **monitoring system**, not a trading edge. No information asymmetry on fully public data. The program's value is in fragility detection, not directional prediction.

## Baseline

ETH price: 1,539 daily / 36,734 hourly points, 2022-01-01 → 2026-03-19. `data/eth_price.csv`, `data/eth_price_1h.csv`. Script: `flow/eth_price.py`.

## Method

Started with cross-correlation. Proved wrong tool for regime transitions. Shifted to conditional/threshold-based tests and temporal structure analysis. Tools: Python, pandas, numpy, scipy. DefiLlama API + free public RPC + Binance data archive + CoinMetrics Community Data (exchange flows) + Deribit public API (IV data).

## Key Principle

**Position heterogeneity:** Temporal ordering in forced-liquidation cascades scales with leverage gap between position types. Only works at ≥10x gap. Failed within lending protocols (~2x gap), succeeded between perps and lending (10-30x gap). **Boundary condition:** applies to forced position closures only, not to market pricing responses (IV, spreads). Pricing mechanisms have their own timing independent of leverage structure.

---

## Findings — Monitoring Architecture

### Layer 1: Regime Context (utilization APY)
- High APY (>5.5%) → 88% of events are concentrated/capitulation
- Low APY (<2.7%) → 64% are distributed/cascade
- Lead: weeks-months (regime-level), no temporal spike. p=0.001
- **Role: attention routing** — determines which type of event to expect, does not improve classification accuracy within the distributed class
- Script: `flow/utilization_signal.py`

### Layer 2: Early Warning (perp OI drop)
- Binance ETHUSDT hourly OI drop >4% → perp leverage unwinding
- Lead: ~37h before lending peak. 16/17 episodes (94%)
- Price falls median 10.9% between signal and lending peak
- ~5 false alarms/year at 4% threshold
- Does not predict episode escalation (fires for 15/17 episodes regardless of type)
- Script: `flow/perp_lead.py`

### Layer 3: Event Classification (liquidation magnitude)
- Volume > 90th pctl, classify vs trailing 180d: ≥97th = capitulation, <97th = continuation
- Concentrated: median +2.36% 7d (n=38). Distributed: median -3.31% 7d (n=75)
- Spread: 5.67pp, p=0.003. Survived 7 stress tests including momentum control (p=0.0003)
- **Distributed signal decomposition:** 68% overall hit rate is a blend of two populations:
  - Escalating episodes (containing concentrated spikes): ~76% hit rate
  - Non-escalating episodes (distributed-only): 50% hit rate (no signal)
  - Post-concentrated distributed: 70.4% (only clean sub-signal above baseline)
- The 68% is an honest base rate for a monitoring system but the causal claim is narrower: distributed flow is episode-context-dependent, meaningful after a concentrated spike, noise without one
- Scripts: `flow/liquidation_events.py`, `flow/liquidation_expand.py`, `flow/regime_test.py`, `flow/false_positive_anatomy.py`

Architecture is **hierarchical**: utilization sets the prior → OI warns of stress → magnitude classifies resolution. Layers are context, not conjunctive filters.

---

## Done

### Characterized ✦

| Signal | Key Result | Script |
|---|---|---|
| Liquidation magnitude classifier | Spread +5.67pp, p=0.003. 27 episodes, 7 stress tests passed | `flow/regime_test.py` |
| Perp → lending lead | 37h lead, 94%, price -10.9% between signal and peak | `flow/perp_lead.py` |
| Utilization regime | APY classifies event type, p=0.001. Attention routing, not filtering | `flow/utilization_signal.py` |
| Protocol cascade ordering | No consistent ordering. Aave first 48% by volume, not structure | `flow/cascade_sequence.py` |
| Liquidation walls | Legible snapshot, $2.16B, two whales = 94% of value | `flow/liquidation_walls.py` |
| Volatility signal | r=0.235 log-vol → 7d realized vol. Supporting, not standalone | `flow/volatility_signal.py` |
| False positive anatomy | 32% FP rate is two populations (50% noise + 76% escalating), not irreducible | `flow/false_positive_anatomy.py` |
| Episode arc structure | Post-concentrated 70.4% is only clean sub-signal; pre-concentrated is forward-window artifact | `flow/false_positive_anatomy.py` |
| Options IV timing | IV peaks +1d after concentrated spike. Reactive, not predictive. No early warning | `flow/iv_timing.py` |
| Exchange flows | Four tests, all null. Daily CEX flows add no discriminating power | `flow/exchange_flows.py` |

### Killed ✗

| Signal | Why | Script |
|---|---|---|
| Stablecoin supply (DAI/GHO/USDS) | Lags ETH by ~8d. Loop doesn't close. | `flow/stablecoin_supply.py` |
| stETH/ETH spread | Arbitraged away post-Shanghai | `flow/steth_spread.py` |
| Shape-based classification (peak ratio) | p=0.37. Signal is magnitude, not shape | tested in `flow/regime_test.py` |
| OI as escalation predictor | Fires for 15/17 episodes regardless of type. Fisher's p=0.515 | `flow/false_positive_anatomy.py` |
| Exchange flow absorption signature | No difference between escalating and non-escalating episodes (p=0.817) | `flow/exchange_flows.py` |
| IV as faster warning layer | IV peaks after OI trough (median 0.0d gap). Does not lead | `flow/iv_timing.py` |

### Parked ⏸

| Signal | Why |
|---|---|
| TVL divergence | No connection to primary finding |
| Bridge flows | No connection to primary finding |
| USDT/USDC supply | Different mechanism, low expected yield given DAI/GHO results |
| Conjunction test | Demoted: utilization doesn't improve distributed accuracy, OI doesn't predict escalation |
| Cross-collateral contagion | No specific hypothesis motivating it after five consecutive escalation-prediction nulls |

---

## Open — Remaining

### 1. Perp Data Upgrade
- **What**: Replace Binance OI proxy with direct Hyperliquid/Coinglass liquidation data
- **Why**: OI includes voluntary closures — primary source of 30% precision problem. Direct liquidation events separate forced unwinds from strategic exits. Could push precision from 30% to 50%+ and tighten the 37h lead time estimate.
- **Source**: Hyperliquid public API (stats endpoint returned 403 in iteration 11 — needs re-check), Coinglass (may need API key)
- **Status**: Not attempted. Only remaining research item that improves an existing finding rather than confirming a boundary.

### 2. Liquidation Wall Proximity as Escalation Predictor
- **What**: Whether price proximity to large lending position thresholds at episode onset predicts escalation to concentrated spike
- **Why**: The only structurally grounded escalation predictor identified. Five data domains tested against escalation (lending features, OI, exchange flows, IV, combined filters) all failed because escalation is a topology question, not a flow question. This tests topology directly.
- **Source**: Position-level snapshot data from Aave/Compound/Maker (on-chain, requires periodic scanning of active positions and their liquidation prices)
- **Status**: Different analytical mode from the aggregate flow statistics conducted so far. Engineering-heavy (requires building a position scanner). Parked unless the monitoring system is operationalized.

### 3. Real-Time Monitor Implementation
- **What**: Operationalize the four-layer monitoring system as a live tool
- **Why**: The research program is complete. Every accessible data domain has been tested. The system's value is practical (fragility detection), not further research.
- **Scope**: Ingest live data (Aave APY, Binance OI, on-chain liquidation events), compute classifications in real-time, emit alerts
- **Status**: Engineering task, not research. Depends on whether the monitoring system is worth operationalizing given the "no trading edge" conclusion.
