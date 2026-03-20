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

## Hypothesis

**Proximity to dense liquidation walls at episode onset predicts escalation.** When a stress episode begins (distributed liquidation flow, detected by the existing monitoring system), the distance from current price to the nearest large liquidation cluster determines whether the episode will escalate:

- **Near wall** (large cluster within 5-10% of current price): high escalation probability. Small further decline reaches the wall, triggers massive liquidation, produces the concentrated spike.
- **Far wall** (nearest cluster >15-20% below): low escalation probability. The stress is moderate, positions being liquidated are small/scattered, market absorbs without cascading.

This is the structural explanation for the two populations discovered in the flow phase:
- Escalating episodes (76% hit rate) → wall was nearby
- Non-escalating episodes (50%, noise) → wall was distant

## What This Would Provide

If validated, wall proximity transforms the monitoring system from reactive classification to prospective risk assessment:

| Layer | Current | With position topology |
|---|---|---|
| Regime (APY) | Attention routing | Unchanged |
| Early warning (OI) | Alert, ~37h lead | Unchanged |
| Classification (magnitude) | Same-day, after the fact | Unchanged |
| **Escalation prediction** | **Cannot predict** | **Wall proximity at episode onset** |

The escalation layer fills the specific gap that five flow-domain investigations couldn't fill.

## Approach

### Phase 1: Current snapshot
Build a position scanner that reads active lending positions from Aave v3, Compound v3, and Maker and computes the liquidation density map. Validate against the existing one-time snapshot from flow phase iteration 3 ($2.16B, walls at $1,300-$1,600). Understand the data shape.

### Phase 2: Historical reconstruction
The hard part. To backtest wall proximity against the 27 historical episodes, we need position snapshots at each episode's start date. Options:
- **Archive RPC** with historical `eth_call` (block-specific state queries)
- **The Graph subgraphs** with time-travel queries
- **Event replay** — reconstruct position state by replaying deposit/borrow/repay/liquidation events from genesis

### Phase 3: Backtest
For each of the 27 episodes: compute wall proximity at onset, test whether proximity predicts escalation (binary: did the episode produce a concentrated spike?). Small n but the hypothesis is specific and the test is clean.

## Data Sources

| Source | What it provides | Access |
|---|---|---|
| Aave v3 subgraph | Active positions, collateral, debt, LTV | The Graph, free |
| Compound v3 contracts | Account state, collateral, borrows | Direct RPC |
| Maker CDPManager | Vault collateral and debt (ilk-specific) | Direct RPC |
| Protocol oracle contracts | Current price feeds used for liquidation calc | Direct RPC |
| Archive RPC (Alchemy/Infura) | Historical state at specific blocks | Free tier may suffice |

## What This Is Not

This is not a trading system. The position map is public — anyone can read it. The value is completing the monitoring architecture with the missing escalation layer, not creating information asymmetry. The thesis from the flow phase stands: this is fragility detection, not directional prediction.

## Open Questions

1. **How dynamic are walls?** If whales actively manage positions (top up collateral as price drops), the map shifts faster than episodes develop. The wall you see at episode onset may not be there when price reaches it. How much do walls move during the 1-7 day episode window?

2. **Granularity required.** Is it enough to know "there's $X within Y% below"? Or does the specific distribution matter (one whale vs many small positions at the same level)?

3. **Historical reconstruction feasibility.** Can we get position state at specific historical blocks without running our own archive node? Subgraph time-travel queries and archive RPC free tiers need testing.

4. **Protocol coverage.** Aave v3 dominates (~80% of lending volume). Is Aave-only sufficient, or do Compound/Maker walls matter for escalation prediction?
