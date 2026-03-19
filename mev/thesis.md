# MEV Program Thesis

## Context

DeFi in 2026 is a $95-140B TVL system dominated by lending (80% of activity), liquid staking, and tokenized RWAs. The institutional layer is fundamentally a shadow banking system built on smart contracts — recursive leverage loops where collateral is deposited, borrowed against, redeployed, and restaked in chains that exist outside traditional balance sheet reporting and capital adequacy rules.

This leverage topology is fully transparent on-chain. Every position, every liquidation threshold, every collateral ratio is public data. This is an information asymmetry in reverse — the data is open, but few are systematically reading it.

## Observation

The DeFi leverage machine creates mechanical price relationships:

**Expansion cycle:** Asset price rises → collateral value rises → borrowing capacity increases → more borrowing → buy more assets → price rises further. Observable as: TVL growth, stablecoin supply expansion, borrowing utilization climbing, bridge inflows.

**Contraction cycle:** Asset price drops → collateral ratios deteriorate → liquidations trigger → forced selling → price drops further → cascade. Observable as: liquidation spikes, stablecoin supply contraction, TVL collapse in USD terms while token-denominated TVL holds, bridge outflows.

## Empirical Findings (March 2026 exploration)

Eight iterations tested the thesis against data. The mechanical relationships are real and legible. The predictive picture is more nuanced than originally framed.

### What held

- The leverage topology IS transparent. Liquidation walls can be mapped in real-time ($2.16B ETH-collateral across 11 protocols). Stablecoin supply tracks leverage. On-chain event logs provide complete liquidation history.
- Mechanical relationships between leverage metrics and price are real — supply follows price (~8 day lag), liquidations accompany drawdowns, stETH spread reflected stress pre-Shanghai.

### What didn't hold

- **Expansion signals don't lead.** Stablecoin supply (DAI+GHO+USDS) lags ETH price by ~8 days. The reflexive loop doesn't close on the expansion side — minted stablecoins disperse into DeFi rather than feeding back to spot.
- **Contraction price signals get arbitraged.** stETH/ETH spread was a real stress indicator pre-Shanghai (r=-0.375 concurrent). Post-Shanghai redemption arbitrage destroyed it. Any signal based on a price spread closeable by faster participants will decay.
- **Cross-correlation is the wrong tool.** The thesis describes regime transitions and thresholds, not linear continuous relationships.

### What emerged: liquidation magnitude as capitulation classifier

The investigation's primary finding, refined through regime-invariance stress testing:

**When daily liquidation volume crosses the 90th percentile, the magnitude of the spike relative to recent history classifies whether the stress is resolving or deepening.**

Original framing was "temporal structure" (spike vs sequence). Stress testing showed the signal is **magnitude-based**, not shape-based:
- M1 (180d percentile) tests absolute magnitude and succeeds (p=0.003)
- M2 (peak ratio) tests temporal shape and fails (p=0.37)

Best classifier (M1-P97: today's volume ≥97th percentile of trailing 180d):
- **Concentrated** (extreme spike, n=38): median +2.36% 7d forward return, 39.5% negative
- **Distributed** (moderate, n=75): median -3.31% 7d forward return, 68.0% negative
- Spread: 5.67pp. Mann-Whitney p=0.0027.

### Stress test results (Iteration 8)

The signal survived five discriminant tests:

1. **Regime-invariant classification (A):** Replacing the original 7d-sum denominator with a 180d-window percentile *strengthened* the signal (spread 3.7pp → 5.7pp, p 0.076 → 0.003). Regime artifacts would weaken under regime-invariant normalization.

2. **Threshold stability (B):** Spread is positive and significant from 91st through 99th percentile. Not threshold-dependent.

3. **Within-regime control (C):** In bear markets (trailing 30d return ≤ 0), spread survives at +7.2pp, p=0.001. Bull markets have too few distributed events to test (n=5), consistent with structural interpretation.

4. **Within-episode position (E):** Concentrated days cluster later in episodes (mean position 0.62 vs 0.42, p=0.006). Position-in-crash contributes to the spread — but doesn't explain it fully, because:

5. **Trailing 7d return control (F):** Concentrated days actually have *deeper* prior 7d drawdowns (-13.2% vs -10.1%). Yet their forward returns are better. Excess return spread (forward minus trailing) is +10.9pp, p=0.0003. **Not mean-reversion.** The signal persists after removing the momentum component — concentrated days bounce disproportionately relative to their prior drawdown.

### Utilization as regime classifier (Iteration 8, Investigation A)

Aave v3 stablecoin supply APY (proxy for lending utilization) classifies which liquidation pattern follows, but in the **opposite** direction from the original hypothesis:
- Higher utilization → concentrated (capitulation) liquidations. Median pre-event APY: 4.81%
- Lower utilization → distributed (cascade) liquidations. Median pre-event APY: 3.69%
- p=0.001. Monotonic: Q1 (low APY) = 64% distributed; Q4 (high APY) = 12% distributed.

Interpretation: high utilization = crowded leverage = when a shock hits, many positions liquidate at once (concentrated spike, capitulation). Low utilization = sparse leverage = liquidations trickle across days (distributed, unresolved). This is regime-predictive (classifies which type) but not time-predictive (no temporal lead in cross-correlation).

### Structural asymmetry

Expansion and contraction are not symmetric:
- **Expansion** is voluntary, multi-path, produces lagging or concurrent signals.
- **Contraction** is forced, single-path (liquidation → sell collateral → price drop), produces classifiable system states.

The thesis's value is concentrated on the contraction/fragility side.

### What the signal is

Revised claim: **"Extremely large liquidation days (≥97th percentile of trailing 180d) tend to mark capitulation with positive forward returns; moderately large days (90th-97th percentile) tend to precede further declines."**

This is a variant of the climactic volume pattern from traditional microstructure, measured on-chain with precision. It's not purely mean-reversion (excess return test confirms). The on-chain advantage is measurement precision — exact liquidation volumes computed from event logs rather than estimated from exchange volume.

The signal fires ~10 times/year for distributed events, ~4 times/year for concentrated events (at M1-P97). Independent episodes: ~27 over 4 years, of which ~5-6 are distributed-dominant. Small sample — the effect is large but the event count limits confidence.

## Revised Thesis

### Layer 1: Fragility Regime Detection

The on-chain leverage topology is legible and the mechanical relationships are real. The edge is not in predicting price from continuous metrics. It's in:

1. **Classifying stress events by magnitude** — extremely large liquidation days (capitulation) have positive forward returns; moderate-but-elevated days precede further declines. The 180d-percentile classifier is the best-characterized version. Survives regime controls, momentum controls, and regime-invariant reclassification.

2. **Mapping current fragility state** — liquidation walls show where forced selling sits relative to current price. Context that determines when magnitude classification matters most.

3. **Utilization as pre-condition classifier** — lending utilization level predicts whether a liquidation event will be concentrated (capitulation) or distributed (cascade). Not a timing signal, but a regime classifier: low utilization + high liquidations = distributed pattern more likely.

### Layer 2: Micro-Structural MEV (Evolution of Freya)

Unchanged from original assessment:
- Ethereum L1: saturated (PBS/Flashbots, 90%+ to proposers)
- Established L2s: moderate competition
- Emerging chains: wider margins, where block-level design still works

### Synthesis

Layer 1's shape is different than originally envisioned:
- **Not** a directional signal generator ("leverage is expanding, go long")
- **Instead** a stress classifier ("this liquidation spike is capitulation, expect stabilization" vs "this is moderate distributed stress, expect continuation")
- Actionable for: defensive positioning during distributed events, contrarian entry after capitulation events, options straddles during elevated-but-not-extreme days
- The edge is measurement precision (on-chain liquidation volumes) applied to a known microstructure pattern (climactic volume), not a novel structural signal

## Open Questions (updated)

### Answered
- ~~What is the actual correlation strength between on-chain leverage metrics and subsequent price action?~~ → Expansion metrics lag. Contraction metrics are bimodal, classifiable by magnitude. Cross-correlation is the wrong frame.
- ~~Are there existing tools/dashboards that aggregate this data?~~ → DefiLlama provides snapshots. The gap is in classification, not raw data.
- ~~What's the minimum viable data pipeline?~~ → Liquidation events via RPC logs + ETH price. Concentration ratio computable from this alone.
- ~~Does lending utilization predict liquidation regime?~~ → Yes, but inverted: high utilization → concentrated (capitulation), low → distributed (cascade). Regime-predictive, not time-predictive. p=0.001.
- ~~Is the concentration ratio shape-based or magnitude-based?~~ → Magnitude-based. 180d percentile (magnitude) succeeds (p=0.003); peak ratio (shape) fails (p=0.37).
- ~~Is the forward return spread just mean-reversion?~~ → No. Concentrated days have deeper prior drawdowns yet better forward returns. Excess return spread +10.9pp, p=0.0003.

### Open
- **Protocol cascade sequencing (Plan C):** Do Maker/Compound liquidations systematically precede Aave? Architecturally determined, could provide hours of lead time. Zero cost — data exists.
- **Perp liquidation as leading edge (Plan D):** Do perp DEX liquidation spikes precede lending protocol spikes? Higher leverage = earlier liquidation. Would test whether the magnitude signal has a faster upstream trigger.
- **Cross-chain universality (Plan B):** Does the magnitude classifier work on L2 Aave liquidations? Tests mechanism universality vs L1-specific.
- **Options IV overlay (Plan H):** Is the volatility expansion on capitulation days already priced? If IV spikes before liquidation events, the signal may be redundant for options strategies.
- **Is the magnitude pattern DeFi-specific or generic?** Comparison to traditional-market climactic volume behavior would determine whether on-chain data provides genuine measurement edge or merely reproduces a known effect.
- **Sample size:** 27 episodes, ~5-6 distributed-dominant. Effect is large but event count limits confidence. More data (pre-2022, L2s) would help.
