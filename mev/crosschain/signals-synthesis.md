# Cross-Chain Flows — Signal Synthesis

## Signals Tested, Ranked by Outcome

### Signals with lead time: None

No cross-chain flow signal showed predictive power for price at any tested resolution (daily, 7-day rolling) or lag structure. The investigation tested organic flow, depth-normalized flow, multi-day momentum, and stablecoin ratios — all dead.

### Robust mechanism findings (not predictive, but measurably informative)

**Rank 1: Arb correction ratio (trade_net / -organic_net)**
- Strength: Mean 1.007, median 0.999, std 0.228 across 531 qualifying days. Survived every stress test including $1.2B criminal laundering.
- What it measures: The precision of AMM→CEX price alignment. Near-perfect 1:1 means THORChain pools are fully price-corrected by arb bots.
- Limitation: Descriptive of mechanism, not predictive of price direction.

**Rank 2: BTC-ETH hourly return correlation as crash-type classifier**
- Strength: Cleanly separates clear-direction crashes (corr > 0.8: Aug 2024, Dec 2024, Jan-Feb 2026) from contested crashes (corr < 0.5: Oct 2025). Observable within hours.
- What it measures: Whether the market has directional consensus during a crash.
- Limitation: Classifier, not predictor. Only 5 episodes tested.

**Rank 3: Arb precision ∝ profit opportunity**
- Strength: Monotonic Q1→Q5: 9-14% tight at low impact → 83-87% tight at high impact. Holds for both BTC and ETH.
- What it measures: Arb bot rationality — they correct large dislocations precisely, ignore small ones.
- Limitation: Confirms rational agent behavior. Not directly actionable.

**Rank 4: Correction ratio variance as crash character descriptor**
- Strength: 7d std ranges from 0.057 (smooth decline, Nov 2025) to 0.513 (contested, Oct 2025).
- What it measures: Real-time crash type — directional conviction vs contested direction.
- Limitation: Not predictive. Small sample (5 episodes).

### Noise (tested, no signal)

| Signal | Kill metric | Why it failed |
|--------|------------|---------------|
| BTC→ETH rotation as crash signal | BTC selling -$594M on rally days vs -$551M on crash days | Persistent user-composition flow, direction-indifferent |
| Single-day flow → next-day price | r ≈ -0.05 | No information content |
| 7-day flow momentum | Deep-pool quintile spread: flat | Artifact of mixing depth regimes; shallow-pool signal driven by few bounce episodes |
| Flight-to-safety ratio | 0.028-0.044 (crash) vs 0.048 (baseline) | Inverted — total volume grows faster than stablecoin buying during stress |
| Herfindahl concentration | 0.191-0.240 (crash) vs 0.226 (baseline) | No separation; volume rises proportionally across all pools |
| Slip as stress indicator | r = -0.01 to -0.16 vs turnover/returns | Governed by protocol fee tiers, not market conditions |

### Protocol event contamination

Two windows must be excluded from any market-behavior analysis:
- **THORFi pause (Jan 24-26, 2025):** RUNE -30%, correction ratio spiked to 2.65x then -0.15x
- **Bybit laundering (Feb 22 – Mar 5, 2025):** $1.2B criminal ETH→BTC conversion, 772x normal turnover

## Composite Signal

No composite signal can be constructed from the winners because none have predictive power for price. The mechanism findings (correction ratio, BTC-ETH correlation, correction variance) describe crash character, not direction. They could theoretically form a "crash regime classifier" composite:

- BTC-ETH hourly return correlation (rolling 24h) distinguishes clear vs contested
- Correction ratio 7d variance distinguishes tight vs oscillatory arb behavior
- These two metrics are correlated (both measure directional consensus)

This classifier would characterize ongoing crashes in real-time but cannot predict their onset or direction.

## What's Next

The investigation found no tradeable cross-chain flow signal. The mechanism characterization is complete for THORChain at hourly resolution. Remaining options:

1. **5-min resolution probe (low cost, diminishing returns):** Pin down the Oct 2025 oscillation period. If it's 15-20 min rather than 2-3 hours, that's a different timescale for the correction mechanism. ~6 API calls. Would refine understanding but not change the core conclusion.

2. **Pivot to different data source:** THORChain's declining pool depth (70-90% loss) and protocol-specific events (THORFi insolvency, Bybit laundering) make it an increasingly noisy window into broader crypto markets. A different DEX or bridge with more depth and fewer protocol crises might yield cleaner signals.

3. **Integrate mechanism into broader crash model:** The correction ratio variance and BTC-ETH correlation are crash-type descriptors. If combined with the OI signal (37h lead on liquidations), the correction mechanism could add real-time characterization once a crash is detected — "this is a clear-direction crash" vs "this is contested" — which might inform position management even if it can't predict onset.

4. **Close this thread.** The original questions are answered (mostly negative). The mechanism characterization is interesting science but doesn't produce a trading signal. Resources may be better spent on other phases of the research arc.
