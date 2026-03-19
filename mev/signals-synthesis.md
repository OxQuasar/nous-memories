# DeFi Signals Synthesis

## Summary

Twelve iterations tested whether on-chain DeFi metrics produce actionable signals for ETH price direction. Started with "does on-chain data predict price direction?" Arrived at: "the leverage topology is legible and produces classifiable system states during stress, but does not yield trading edge due to zero information asymmetry on fully public data."

Three characterized findings emerged. Several signals were killed. The thesis was refined from "directional signal generator" to "fragility monitoring system."

The investigation's deepest contribution is the **position heterogeneity principle**: temporal ordering in liquidation cascades is measurable only when the leverage gap between position types is large (order of magnitude). This explains every structural hypothesis outcome in the investigation.

---

## Signals Tested — Ranked by Lead Time and Strength

### 1. Perp → Lending Temporal Lead ✦ Genuine Early Warning

**What it is:** Hourly Binance ETHUSDT open interest drops (>3-4%) as a proxy for perp liquidation activity, preceding lending protocol liquidation peaks.

**Lead time:** Corrected median 37 hours. 16/17 episodes (94%).

**Result:** When the OI drop fires, ETH price is typically 10.9% higher than it will be at the lending liquidation peak. This is genuine warning — further decline is still coming.

**False positive rate:** ~20 false alarms/year at 3% threshold (~30% precision, 3.9x enrichment). At 4% threshold: ~5 false alarms/year, 6.8x enrichment.

**Why it works:** The leverage gap between perps (5-50x) and lending (1.5-3x) is an order of magnitude — wide enough to overcome position heterogeneity and produce consistent temporal ordering. The same mechanism failed within lending protocols (Maker vs Aave, <2x gap).

**Limitations:** OI is a proxy (includes voluntary closures). Data is fully public. Not a standalone trading signal due to precision.

### 2. Magnitude Classifier (Climactic Volume On-Chain) ✦ Validated Descriptive Signal

**What it is:** When daily lending liquidation volume crosses the 90th percentile, classify by magnitude relative to trailing 180d window. ≥97th percentile = concentrated/capitulation; below = distributed/continuation.

**Lead time:** None — fires on the event day. Classification is concurrent.

**Result:** Concentrated: median +2.36% 7d, 39.5% negative (n=38). Distributed: median -3.31% 7d, 68.0% negative (n=75). Spread: 5.67pp, p=0.003. Survived seven discriminant tests: regime-invariant reclassification, threshold stability, bear-market control (+7.2pp, p=0.001), episode clustering (+19.5pp, p=0.019), within-episode position, trailing momentum control (excess return +10.9pp, p=0.0003).

**What it is NOT:** The original "temporal structure of liquidation flow" interpretation was wrong. Shape-based classification (peak ratio) fails (p=0.37). This is the traditional climactic volume pattern measured on-chain with higher precision than exchange volume data allows. The pattern is not novel; the measurement precision is the DeFi contribution.

**Limitations:** 27 independent episodes, ~5-6 distributed-dominant. Fully public data.

### 3. Utilization as Regime Pre-Classifier ✦ Contextual, Not Predictive

**What it is:** TVL-weighted Aave v3 stablecoin supply APY classifies which type of liquidation event will occur.

**Lead time:** Pre-condition (regime-level), not event-level timing. No temporal lead in cross-correlation.

**Result:** High APY (>5.5%) → 88% of liquidation events are concentrated/capitulation. Low APY (<2.7%) → 64% are distributed/cascade. Monotonic Q1→Q4 gradient, Fisher p=0.001.

**Caveat:** Likely a regime confound — APY moves in month-scale waves that proxy bull/bear markets. The statistical tests assume independence but ~5-8 clustered episodes provide effective N far below the nominal sample. However, the directional information is consistent with the position heterogeneity principle: high utilization = crowded positions at similar thresholds = concentrated clearance.

### 4. Volatility Regime Signal — Real but Modest

**What it is:** Log-liquidation-volume → forward 7d realized volatility.

**Result:** r=0.235 (~5.5% variance explained). Quiet days: 2.36% abs return. Extreme days: 4.62%. Supporting evidence, not standalone.

---

## What Was Noise — Don't Revisit

| Signal | Why it's noise | Iteration |
|---|---|---|
| Stablecoin supply (DAI/GHO/USDS) | Lags ETH by ~8 days. Loop doesn't close — minted stables disperse, don't feed back to spot. | 1 |
| stETH/ETH spread (post-Shanghai) | Redemption arb compresses spread to noise. Any spread-based signal with an arb mechanism will decay. | 2 |
| GHO supply | Governance-driven, r=-0.061 | 1 |
| USDS supply | Too new (541 days), spurious boundary peak | 1 |
| Protocol cascade ordering (Maker → Compound → Aave) | No consistent ordering. Aave fires first (48%) due to volume dominance. Leverage gap too small. | 10 |
| Raw liquidation volume → direction | Volume alone doesn't predict direction. Must be combined with magnitude classification. | 4 |
| Temporal shape classification (peak ratio) | Pure shape classification fails (p=0.37). The signal is magnitude, not shape. | 8 |

---

## Composite Signal Architecture

The three validated findings form a three-layer monitoring system. Each layer was individually stress-tested; the conjunction has not been tested as a system.

```
Layer 1: REGIME PRE-CONDITION
  Input:  Aave v3 stablecoin APY (DefiLlama yields API)
  Logic:  APY < 2.7% → system primed for distributed/cascade mode
          APY > 5.5% → events likely to be concentrated/capitulation
  Lead:   Weeks to months (regime-level)
  Value:  Context. Tells you which mode to expect.

Layer 2: EARLY WARNING
  Input:  Binance ETHUSDT hourly OI change
  Logic:  OI drop > 4% in one hour → perp leverage layer unwinding
  Lead:   ~37 hours before peak lending liquidation
  Value:  Alert. Expect ~10% further decline. ~5 false alarms/year at 4%.

Layer 3: EVENT CLASSIFICATION
  Input:  Daily lending liquidation volume (Aave + Compound + Maker via RPC)
  Logic:  Volume > 90th pctl AND ≥ 97th pctl of 180d → capitulation
          Volume > 90th pctl AND < 97th pctl of 180d → continuation risk
  Lead:   Same-day (concurrent classification)
  Value:  Assessment. +2.4% vs -3.3% median 7d forward return.
```

**Operational sequence during a stress event:**
1. Utilization context says: low APY → system fragile, expect distributed pattern
2. Perp OI drops >4% → early warning fires, ~37h before lending peak
3. Lending liquidation volume spikes → classify magnitude:
   - If extreme (≥97th pctl of 180d): likely capitulation, expect recovery
   - If moderate (90th-97th pctl): continuation risk, expect further decline

**What this does NOT provide:** A systematic trading signal. The false positive rate on Layer 2 is too high for mechanical execution. The magnitude classifier in Layer 3 has a real effect (5.7pp) but fires rarely (~10-15 moderate events/year, ~5-6 extreme). Sample size (27 episodes over 4 years) limits confidence for position sizing.

---

## Position Heterogeneity Principle

The investigation's most generalizable finding, spanning multiple tests:

**Temporal ordering in forced-liquidation cascades scales with the leverage gap between position types.**

| Comparison | Leverage gap | Consistent ordering? | Result |
|---|---|---|---|
| Perps vs lending | 10-30x (5-50x vs 1.5-3x) | Yes, 94% | 37h median lead |
| Maker vs Aave | <2x (150% vs 120%) | No | Volume-proportional |
| Within single protocol | ~1x | N/A | No structure |

**Why:** Protocol-level parameters (collateral ratios, liquidation thresholds) set the threshold at which a position liquidates. But the timing depends on each position's entry price and LTV, not just protocol minimums. Positions are distributed across the full price range within each protocol. When the leverage gap between venue types is small, this position diversity washes out the structural ordering. When the gap is an order of magnitude, even diverse position distributions can't bridge it — 20x perp positions mechanically liquidate before 2x lending positions.

**Implication for future investigation:** Only test structural hypotheses where the leverage gap is ≥10x. Within-protocol or within-tier structural signals are unlikely to overcome position heterogeneity.

---

## Next Step

The investigation is at its natural conclusion for the exploration phase. The broad question ("does on-chain DeFi data produce trading signals?") has been answered: the data is legible and classifiable, but constitutes a monitoring system, not a trading edge.

**If continuing this line:**
- **Real-time monitor (Plan F)** is the most valuable remaining work. Operationalizing the three-layer system as a live tool. This shifts from research to engineering.
- **Conjunction testing:** The three layers have only been tested individually. A forward-looking period or simulation testing the combined system could reveal whether the conjunction adds precision beyond individual signals.

**If pivoting:**
- The position heterogeneity principle suggests looking at **wider leverage gaps** for structural signals — e.g., options (effectively 10-100x via delta) vs perps vs lending. The options/IV overlay (Plan H) becomes more interesting from this angle.
- Alternatively, the finding that the magnitude pattern is generic climactic volume suggests DeFi-specific edge may not exist in price prediction at all, and the program's value is in the monitoring/risk-management layer.
