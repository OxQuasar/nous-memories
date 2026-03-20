# Position Topology — Findings

## Summary

The position topology investigation tested whether proximity to liquidation walls at episode onset predicts escalation of ETH stress episodes. Across 8 historical episodes (2022-2025), the answer is: **topology predicts the amplifier gain of an exogenous shock, not whether the shock occurs.** It is a conditional severity assessment, not a binary predictor.

The investigation also produced three findings that were not anticipated by the original thesis:

1. **Real/phantom decomposition** — most near-price DeFi lending positions are phantom (ETH-loop strategies immune to ETH/USD price moves). Without debt-side classification, any liquidation heatmap is misleading.
2. **Risk rotation** — DeFi fragility has structurally shifted from ETH-price-cascade risk (2022) to staking-derivative-depeg-cascade risk (2026).
3. **Cascade mechanics** — two distinct cascade modes with measurable thresholds.

---

## Key Findings

### 1. Real vs Phantom Positions

Every DeFi lending position with ETH-correlated collateral falls into one of two categories based on its debt composition:

- **Real positions** (stablecoin debt): liquidation price is a function of ETH/USD. When ETH drops, collateral value falls while debt stays fixed → HF drops → liquidation fires → ETH selling pressure.
- **Phantom positions** (ETH-correlated debt, e.g. wstETH collateral / WETH debt): ETH/USD cancels from the health factor equation. HF depends only on the staking derivative exchange rate (wstETH/ETH). No ETH/USD liquidation price exists.

**Current state (Mar 2026, ETH $2,202):** The apparent $4.3B liquidation wall at 4-5% below current price is >99.99% phantom. Real wall within 20%: $73M. Within 30%: $572M. The near-price zone is almost entirely phantom; real liquidation risk only becomes significant at 30%+ drawdown levels.

**This decomposition is the necessary foundation for any liquidation topology analysis.** Without it, publicly available heatmaps (e.g., DefiLlama) show misleading walls dominated by positions that won't respond to ETH price movements.

### 2. The Conditional Fuel Map

Position topology does not predict whether an episode will escalate. It predicts **how much cascade fuel lies in the path if the drawdown continues.**

Across 8 episodes, the fuel map correctly identified:
- Where danger zones were (price levels with concentrated real debt)
- How much cascade fuel existed at each depth
- Whether the path was clear (empty topology = safe for any drawdown magnitude)

**Operational framing:**

| Topology State | Meaning |
|---|---|
| R20% < $30M, no whale | Path clear. Moderate stress absorbed without DeFi amplification. |
| R20% $100-300M, distributed | Moderate fuel. Unlikely to self-sustain without major external shock. |
| R20% > $300M OR whale > $100M within 20% | Dense path or cliff. Cascade likely if drawdown reaches 15-20%. |

The two false positives (Iran $162M, Sep 2024 $270M) had real walls that simply weren't reached by the actual drawdown (14% and 7% respectively). The topology correctly identified the danger zones; the exogenous shocks were insufficient to reach them.

### 3. Cascade Mechanics

Two distinct cascade modes observed:

**Progressive cascade:** Continuous density of real positions through the price path. Each layer of liquidations produces enough selling to push price into the next layer. Self-sustaining when gradient density exceeds ~$14M per 1% of price.
- Example: Yen carry (Aug 2024) — $566M across 1,469 positions, no single position >$29M, but $21M/1% density created a self-sustaining cascade.

**Cliff cascade:** Thin gradient (individually absorbed) until price reaches a single concentrated whale position. The whale's liquidation overwhelms market depth at that price point.
- Example: stETH depeg (Jun 2022) — $2M/1% gradient (absorbed) plus $282M single whale at $1,185. When breached, the whale's liquidation accelerated the crash from $1,200 to $1,000.

**The gradient is kindling; the whale is the cliff.** Both contribute to cascading but through different mechanisms. A composite signal needs both density (R10%/R20%) and concentration (max single position within range).

### 4. Risk Rotation

Phantom ratio evolution across 9 measured snapshots:

| Date | Phantom % | Regime |
|------|-----------|--------|
| Jan 2022 | 2% | Real-dominated |
| Jun 2022 | 35% | Mixed |
| Nov 2022 | 42% | Mixed |
| Aug 2023 | 43% | Mixed |
| Apr 2024 | 44% | Mixed |
| Aug 2024 | 54% | Phantom-growing |
| Sep 2024 | 58% | Phantom-growing |
| Feb 2025 | 70% | Phantom-dominant |
| Mar 2026 | >90% | Phantom-dominant |

**The system hasn't become less fragile. It has shifted what it's fragile to.**

- **2022:** Mostly real positions, dense near price. DeFi was a powerful amplifier of ETH/USD price shocks. Cascade fuel was abundant in the path of typical drawdowns.
- **2026:** Almost entirely phantom near price. DeFi is a negligible amplifier of ETH/USD price shocks. But $5.6B of phantom positions at HF 1.03-1.05 means DeFi is now a powerful amplifier of staking derivative depeg events.

The risk has rotated from price-cascade to correlation-cascade fragility. A monitoring system designed for ETH/USD walls is watching the wrong risk surface.

### 5. Post-Clearing Effect

After a crash liquidates positions above a price level, the topology is defensively empty until new leveraged positions rebuild. FTX (Nov 2022) is the natural experiment: the June 2022 crash cleared everything above $1,000. Five months later, FTX produced a 30% shock and found empty topology — only $12M in Aave liquidations despite a severe drawdown. The drawdown occurred from centralized contagion, but DeFi did not amplify it.

---

## Data & Infrastructure

**Scripts built:**
- `snapshot.py` — Aave v3 current snapshot (subgraph + on-chain multicall)
- `decompose.py` — debt-side decomposition for real/phantom classification
- `maker_scan.py` — Maker/Sky vault scanner (on-chain via CdpManager/Vat/Spot)
- `historical_probe.py` — Aave v2 historical snapshots (fully on-chain via Alchemy archive)
- `failfast_backtest.py` — multi-episode backtest (V2 on-chain + V3 subgraph)
- `backtest_expanded.py` — expanded 8-episode backtest

**Data produced:**
- 9 position snapshots (8 historical + 1 current): ~130K total positions
- Maker vault scan: 852 active ETH vaults
- Full real/phantom decomposition at each snapshot

**Infrastructure notes:**
- Aave v2 subgraph is dead (legacy hosted service removed, no active indexers on decentralized network). Fully on-chain approach via Alchemy archive multicall is the only path for 2022 data. ~28 min per V2 snapshot.
- Aave v3 subgraph supports `block: {number: N}` historical queries. ~6 min per V3 snapshot.
- Alchemy free tier supports historical `eth_call` (archive access).

---

## Successor Investigation

The natural successor is the **correlation-cascade thesis**: given $5.6B+ phantom positions at HF 1.03-1.05, what depeg threshold triggers cascade activation?

Required data (not collected in this investigation):
- DEX liquidity depth per LST (wstETH, weETH, osETH, rsETH)
- Historical staking derivative depeg magnitudes during stress events
- Oracle lag behavior during rapid depeg
- Depeg contagion dynamics across LST tiers (does osETH cracking spread to weETH?)

The real/phantom decomposition and the cascade mechanics model from this investigation provide the foundation for that work.
