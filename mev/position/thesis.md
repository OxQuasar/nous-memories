# Position Topology Thesis

## Premise

The flow phase (17 iterations) established that on-chain lending liquidation data produces a working fragility monitoring system — but with a hole. The system classifies events after they happen (concentrated = capitulation, distributed = continuation risk) but cannot predict whether a moderate stress episode will escalate into a capitulation spike. Five data domains were tested against this escalation question. All failed.

The diagnosis: **escalation is a topology question, not a flow question.**

A stress episode escalates when price falls far enough to reach a large position's liquidation threshold. Whether that threshold exists, how large the position is, and how far away it sits from current price — this is the information that determines escalation. No aggregate metric (volume, OI, exchange flows, IV) captures it because these measure consequences of price movement, not what's waiting ahead of it.

## What Position Topology Is

Every lending position on Aave, Compound, and Maker has a computable liquidation price — the ETH price at which the position's health factor drops below 1 and becomes eligible for liquidation. This depends on:

- Collateral amount and type
- Debt amount and type  
- Protocol-specific liquidation threshold (LTV)
- Oracle price feed

The aggregate of all active positions forms a **liquidation density map**: at each price level below current, how much collateral becomes liquidatable? This map has structure:

- **Walls**: clusters of large positions at similar thresholds (e.g., $200M+ at $1,400 from a single Compound whale)
- **Gradients**: smooth distributions of smaller positions across price ranges
- **Gaps**: empty zones where no significant liquidations would trigger

The map is fully readable on-chain. Every position's collateral, debt, and liquidation parameters are public contract state. The information exists — it's just not aggregated.

## Original Hypothesis

**Proximity to dense liquidation walls at episode onset predicts escalation.** When a stress episode begins (distributed liquidation flow, detected by the existing monitoring system), the distance from current price to the nearest large liquidation cluster determines whether the episode will escalate:

- **Near wall** (large cluster within 5-10% of current price): high escalation probability. Small further decline reaches the wall, triggers massive liquidation, produces the concentrated spike.
- **Far wall** (nearest cluster >15-20% below): low escalation probability. The stress is moderate, positions being liquidated are small/scattered, market absorbs without cascading.

## Empirical Results (6 iterations, 8 episodes backtested)

### The hypothesis is partially supported, with critical refinements

**What was confirmed:**
- Position topology does determine cascade dynamics. All 4 escalating episodes had significant real debt in the drawdown path; all non-escalating episodes had thin or empty paths. 8/8 correct classification when matched to actual drawdown depth.
- Empty topology = no DeFi amplification. FTX (Nov 2022) is the natural experiment: 30% drawdown against empty topology (post-clearing) → only $12M in Aave liquidations. Same asset, severe shock, no cascade.

**What was wrong or incomplete:**

1. **Binary prediction fails.** The best prospective binary metric (R20% > $100M + whale) achieves 6/8 (75%), with two false positives. These are episodes where walls existed but the drawdown was too shallow to reach them (Iran: 14% actual vs wall at 10-20%; Sep 2024: 7% actual vs wall at 10-20%). Topology tells you what's waiting; it doesn't tell you how deep the shock will push.

2. **The correct framing is conditional, not predictive.** Topology is a severity gauge: "if the drawdown reaches X%, here's how much cascade fuel is in the path." This is the missing piece for the monitoring system — not a predictor layer, but a severity-assessment layer.

3. **Most near-price "walls" are phantom.** The investigation's most important technical finding: positions with ETH-correlated collateral AND ETH-correlated debt (e.g., wstETH collateral / WETH debt) have no ETH/USD liquidation price. ETH/USD cancels from their health factor equation. Without debt-side decomposition, any liquidation heatmap is dominated by these phantom positions. In 2026, >99.99% of near-price debt is phantom.

4. **Two cascade modes, not one.** "Wall proximity" is too simple. Cascades operate through two distinct mechanisms:
   - **Progressive cascade**: continuous density of real debt through the price path (~$14M+ per 1% of price). Self-sustaining — each layer of liquidations pushes price into the next.
   - **Cliff cascade**: thin gradient plus a single concentrated whale position. The gradient is absorbed individually until price reaches the whale, whose liquidation overwhelms market depth.

5. **The risk surface has rotated.** DeFi fragility has shifted from ETH-price-cascade (2022: 2% phantom) to staking-derivative-depeg-cascade (2026: >90% phantom). The thesis described a mechanism that was real in 2022 but that the market has structurally moved away from. Today's equivalent question is about depeg thresholds, not ETH/USD walls.

### Answers to Open Questions

1. **How dynamic are walls?** Not directly tested (wall dynamics during episodes not measured). But the post-clearing effect shows walls are cleared by crashes and take months to rebuild. The FTX episode (5 months after June 2022 crash) found topology still empty.

2. **Granularity required.** Yes, distribution matters enormously. Iran ($162M at R20%, distributed in small positions <$21M each) did not escalate. Yen carry ($420M at R20%, continuous density of $21M/1%) did escalate. The stETH episode ($99M at R20%, but one $282M whale at 34%) escalated via the cliff mechanism. Aggregate wall size alone is insufficient — need both density per unit of price and maximum single-position concentration.

3. **Historical reconstruction feasibility.** Feasible but mixed: Aave v3 subgraph supports `block: {number: N}` queries (~6 min/snapshot). Aave v2 subgraph is dead; requires fully on-chain archive multicall approach (~28 min/snapshot). Alchemy free tier covers both.

4. **Protocol coverage.** Aave-only is representative. Maker scan showed <10% contribution to real wall at all proximity bands. Cross-protocol pattern is consistent: borrowers taking real ETH/USD risk maintain wide HF margins (1.5+) on both Aave and Maker.

## Revised Understanding

The original thesis framed topology as a predictive layer. The empirical finding is that topology is a **conditional amplifier gauge**: it measures how much DeFi will amplify an exogenous shock at each drawdown depth. This is more nuanced and arguably more useful than a binary predictor, because it provides severity information that scales with the situation.

The monitoring system architecture becomes:

| Layer | Function | Signal |
|---|---|---|
| Regime (APY) | Attention routing | Unchanged |
| Early warning (OI) | Alert, ~37h lead | Unchanged |
| Classification (magnitude) | Same-day identification | Unchanged |
| **Topology (fuel map)** | **Severity assessment** | **"If drawdown reaches X%, cascade fuel is Y"** |

The topology layer doesn't predict escalation — it tells you the stakes if the drawdown continues. Combined with the early warning layer (which detects that a drawdown has started), this provides: "a stress episode has started, and here's how much DeFi cascade fuel lies in its path."

## Successor Question

The 2026 market's primary vulnerability is not ETH/USD walls (thin, distant) but the $5.6B phantom wall at HF 1.03-1.05. This activates on staking derivative depeg events, not ETH price drops. The natural successor investigation is the **correlation-cascade thesis**: what depeg threshold activates this wall, and what is the probability of reaching that threshold during stress?
