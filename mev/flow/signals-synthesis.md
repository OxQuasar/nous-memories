# DeFi Signals Synthesis

## Summary

Seventeen iterations tested whether on-chain DeFi metrics produce actionable signals for ETH price direction. Started with "does on-chain data predict price direction?" Arrived at: "the leverage topology is legible and produces classifiable system states during stress, but does not yield trading edge due to zero information asymmetry on fully public data."

The program produced a fragility monitoring system, a structural principle about when temporal ordering exists in cascades, and a systematic catalog of what doesn't work across five data domains.

---

## Signals Tested — Ranked by Lead Time and Strength

### 1. Perp → Lending Temporal Lead ✦ Genuine Early Warning

**What it is:** Hourly Binance ETHUSDT open interest drops (>3-4%) as a proxy for perp liquidation activity, preceding lending protocol liquidation peaks.

**Lead time:** Corrected median 37 hours. 16/17 episodes (94%).

**Result:** When the OI drop fires, ETH price is typically 10.9% higher than it will be at the lending liquidation peak. This is genuine warning — further decline is still coming.

**False positive rate:** ~20 false alarms/year at 3% threshold (~30% precision, 3.9x enrichment). At 4% threshold: ~5 false alarms/year, 6.8x enrichment.

**Why it works:** The leverage gap between perps (5-50x) and lending (1.5-3x) is an order of magnitude — wide enough to overcome position heterogeneity and produce consistent temporal ordering.

**What it doesn't do:** Predict episode escalation. OI drops >3% fire for 15/17 episodes regardless of whether they escalate to produce concentrated spikes (Fisher's p=0.515). The signal warns that lending stress is developing, but cannot classify what type.

**Limitations:** OI is a proxy (includes voluntary closures). Data is fully public. Not a standalone trading signal due to precision.

### 2. Magnitude Classifier (Climactic Volume On-Chain) ✦ Validated Descriptive Signal

**What it is:** When daily lending liquidation volume crosses the 90th percentile, classify by magnitude relative to trailing 180d window. ≥97th percentile = concentrated/capitulation; below = distributed/continuation.

**Lead time:** None — fires on the event day. Classification is concurrent.

**Result:** Concentrated: median +2.36% 7d, 39.5% negative (n=38). Distributed: median -3.31% 7d, 68.0% negative (n=75). Spread: 5.67pp, p=0.003. Survived seven discriminant tests: regime-invariant reclassification, threshold stability, bear-market control (+7.2pp, p=0.001), episode clustering (+19.5pp, p=0.019), within-episode position, trailing momentum control (excess return +10.9pp, p=0.0003).

**Distributed signal decomposition (iterations 13-15):** The 68% headline hit rate is an honest base rate but is a mixture of two populations:

| Population | n | Hit rate | Interpretation |
|---|---|---|---|
| Post-concentrated (in escalating episodes) | 27 | 70.4% | **Clean signal** — aftershock prediction. The only sub-group above baseline without measurement contamination. |
| Non-escalating episodes (distributed-only) | 22 | 50.0% | **Noise** — market absorbed moderate stress without cascading. |
| Pre-concentrated (contaminated) | 21 | 90.5% | **Artifact** — concentrated spike inside 7d forward return window drives the measured decline. |
| Pre-concentrated (clean, gap >7d) | 5 | 40.0% | No signal — consistent with baseline. |

The 68% is correct as a forecast (the contamination is part of the natural data-generating process — pre-concentrated days *will* see the spike within 7d). But the causal claim is narrower: distributed flow is episode-context-dependent, meaningful after a concentrated spike (aftershock, 70%), noise without one (50%).

**What it is NOT:** The original "temporal structure of liquidation flow" interpretation was wrong. Shape-based classification (peak ratio) fails (p=0.37). This is the traditional climactic volume pattern measured on-chain with higher precision than exchange volume data allows.

### 3. Utilization as Regime Pre-Classifier ✦ Attention Routing, Not Filtering

**What it is:** TVL-weighted Aave v3 stablecoin supply APY classifies which type of liquidation event will occur.

**Lead time:** Pre-condition (regime-level), not event-level timing. No temporal lead in cross-correlation.

**Result:** High APY (>5.5%) → 88% of liquidation events are concentrated/capitulation. Low APY (<2.7%) → 64% are distributed/cascade. Monotonic Q1→Q4 gradient, Fisher p=0.001.

**Updated role (iteration 13):** Utilization is **attention routing**, not accuracy filtering. It determines which type of event to expect but does not improve classification accuracy within the distributed class. Higher APY weakly predicts *worse* distributed signal quality (Spearman r=0.245, p=0.083) — high APY + distributed = moderate-sized event in an active environment, closer to noise.

### 4. Volatility Regime Signal — Real but Modest

**What it is:** Log-liquidation-volume → forward 7d realized volatility.

**Result:** r=0.235 (~5.5% variance explained). Quiet days: 2.36% abs return. Extreme days: 4.62%. Supporting evidence, not standalone.

---

## What Was Noise — Don't Revisit

| Signal | Why it's noise | Iteration |
|---|---|---|
| Stablecoin supply (DAI/GHO/USDS) | Lags ETH by ~8 days. Loop doesn't close — minted stables disperse, don't feed back to spot. | 1 |
| stETH/ETH spread (post-Shanghai) | Redemption arb compresses spread to noise. Any spread-based signal with an arb mechanism will decay. | 2 |
| Protocol cascade ordering (Maker → Compound → Aave) | No consistent ordering. Aave fires first (48%) due to volume dominance. Leverage gap too small. | 10 |
| Temporal shape classification (peak ratio) | Pure shape classification fails (p=0.37). The signal is magnitude, not shape. | 8 |
| OI as escalation predictor | Fires for 15/17 episodes regardless of type. Fisher's p=0.515. No magnitude separation. | 15 |
| Exchange flow signatures | Four tests, all null (p>0.75). Daily CEX flows don't distinguish episode types, don't separate TP/FP, don't show absorption pattern. | 16 |
| Options IV as early warning | IV peaks +1d after concentrated spike. Reactive, not predictive. Co-temporal with OI, does not lead. | 17 |
| FP anatomy — six lending traits | Episode position, trailing drawdown, volume percentile, utilization APY, prior episode recency, OI confirmation — none cleanly separate FP from TP distributed days. | 13 |

---

## Composite Signal Architecture

The four validated findings form a hierarchical monitoring system:

```
Layer 1: REGIME CONTEXT (attention routing)
  Input:  Aave v3 stablecoin APY (DefiLlama yields API)
  Logic:  APY < 2.7% → system primed for distributed/cascade mode
          APY > 5.5% → events likely to be concentrated/capitulation
  Lead:   Weeks to months (regime-level)
  Value:  Determines which event type to expect. Does not improve
          classification accuracy within the distributed class.

Layer 2: EARLY WARNING
  Input:  Binance ETHUSDT hourly OI change
  Logic:  OI drop > 4% in one hour → perp leverage layer unwinding
  Lead:   ~37 hours before peak lending liquidation
  Value:  Alert. Expect ~10% further decline. ~5 false alarms/year at 4%.
          Does NOT predict whether episode will escalate.

Layer 3: EVENT CLASSIFICATION
  Input:  Daily lending liquidation volume (Aave + Compound + Maker via RPC)
  Logic:  Volume > 90th pctl AND ≥ 97th pctl of 180d → capitulation
          Volume > 90th pctl AND < 97th pctl of 180d → continuation risk
  Lead:   Same-day (concurrent classification)
  Value:  +2.4% vs -3.3% median 7d forward return (spread 5.67pp, p=0.003)

Layer 4: EPISODE STATE
  Input:  Has a concentrated spike occurred within the current episode?
  Logic:  Post-concentrated distributed → 70% continuation (aftershock)
          No prior concentrated spike → 68% base rate (mixture of populations)
  Value:  Context for interpreting distributed flow. The concentrated spike
          is the earthquake; subsequent distributed flow is aftershock forecasting.
```

**Operational sequence during a stress event:**
1. Utilization context says: low APY → system fragile, expect distributed pattern
2. Perp OI drops >4% → early warning fires, ~37h before lending peak
3. Lending liquidation volume spikes → classify magnitude:
   - If extreme (≥97th pctl of 180d): likely capitulation, expect recovery
   - If moderate (90th-97th pctl): continuation risk
4. If a concentrated spike has already occurred in this episode → distributed flow is aftershock (70% continuation). If not → distributed flow is ambiguous (68% base rate, mixture of escalating and non-escalating episodes)

**What this does NOT provide:** A systematic trading signal. The false positive rate on Layer 2 is too high for mechanical execution. The distributed signal in Layer 3 is substantially driven by proximity to concentrated spikes. Sample size (27 episodes over 4 years) limits confidence for position sizing.

---

## Position Heterogeneity Principle

The investigation's most generalizable finding, spanning multiple tests:

**Temporal ordering in forced-liquidation cascades scales with the leverage gap between position types.**

| Comparison | Leverage gap | Consistent ordering? | Result |
|---|---|---|---|
| Perps vs lending | 10-30x (5-50x vs 1.5-3x) | Yes, 94% | 37h median lead |
| Maker vs Aave | <2x (150% vs 120%) | No | Volume-proportional |
| Within single protocol | ~1x | N/A | No structure |

**Boundary condition (from IV test, iteration 17):** The principle applies to **forced position closures**, not to **market pricing responses**. Options IV (set by market makers via delta hedging) is a pricing mechanism, not a position event. This is why options don't lead despite higher effective leverage — the principle governs forced liquidation cascades, not market pricing. In systems with feedback (price → liquidation → more price decline), an event's *effect on the feedback loop* matters more than its *informational content*.

**Implication:** Only test structural hypotheses where the leverage gap is ≥10x and the mechanism involves forced closures. Within-tier structural signals and pricing-based signals (IV, spreads, funding rates) are unlikely to produce temporal ordering.

---

## Information Boundaries Mapped

Five data domains were tested against the escalation prediction question (which episodes will produce a concentrated spike):

| Domain | Tests | Result | Why it fails |
|---|---|---|---|
| On-chain lending features | 6 traits (position, drawdown, percentile, APY, recency, OI) | None separate FP/TP | 97th percentile threshold already extracts nearly everything in this domain |
| Perp OI (episode-level) | OI drop as escalation predictor | Fires for 15/17 episodes | Threshold too common; cannot discriminate |
| CEX exchange flows | Episode signature, TP/FP, absorption, timing | All null (p>0.75) | Flows measure consequences, not causes |
| Options IV | Level, timing, vs OI | Reactive (+1d lag) | Pricing response, not position event |

**Structural explanation:** The escalation question is a **topology question** — depends on where large positions sit relative to current price — not a **flow question**. No aggregate flow metric captures position topology. The only structurally grounded predictor (liquidation wall proximity) requires position-level data, a different analytical mode.

---

## What Was Learned About Investigating

### Methodological findings
- **Cross-correlation was the wrong starting tool.** Regime transitions require conditional/threshold-based analysis, not lag-correlation.
- **Forward-window contamination** inflated the pre-concentrated signal from ~40% to ~81%. Always check whether the predicted event falls inside the return measurement window.
- **Progressive sharpening works.** Iterations 13→14→15: "32% FP rate is irreducible" → "it's two populations" → "the stronger population is a measurement artifact." Each iteration made the claim more honest.
- **Pre-register predictions before testing.** The episode arc probe predicted post-concentrated > pre-concentrated. The data showed the opposite. The wrong prediction was informative: it revealed the concentrated spike is a physical event (clears positions, breaks feedback loop) not just an information event (confirms cascade).

### What didn't need to be tested
- **TVL divergence, bridge flows, USDT/USDC supply** — no connection to primary finding after iteration 6. Correctly parked early.
- **Cross-collateral contagion** — no specific hypothesis motivating it after escalation prediction failures. Correctly left untested.

---

## Next Step

The statistical probing program is complete. Every accessible data domain has been tested. Five consecutive probes (iterations 13-17) confirmed boundaries rather than expanding territory.

**If continuing this line:**
- **Real-time monitor implementation** is the most valuable remaining work. Operationalizing the four-layer system as a live tool. This shifts from research to engineering.
- **Liquidation wall proximity as escalation predictor** is the most structurally grounded remaining question. Whether price proximity to large lending position thresholds at episode onset predicts escalation. Requires position-level snapshot data and is a different analytical mode from the aggregate flow statistics conducted here.

**What's settled:**
- The data is legible and classifiable. The mechanical relationships are real.
- The system is a monitoring tool, not a trading edge. No information asymmetry on fully public data.
- The position heterogeneity principle (forced closures only, leverage gap ≥10x) guides which future signals are worth investigating.
- The escalation question is unanswerable with aggregate flow metrics. It's a topology question.
