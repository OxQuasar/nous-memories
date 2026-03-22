# Physics Phase — Signals Synthesis

## Signals Ranked by Strength

### 1. Oracle-Gated Threshold Batching (Confirmed — Strong)

**What:** Aave liquidations on spike days are not sequential cascades but simultaneous batch events triggered by discrete Chainlink oracle price updates. 67% of consecutive liquidations occur in the same block (Δt=0). Bursts are separated by ~7.6 minute gaps consistent with the oracle's ~0.5-1% deviation threshold update cadence.

**Evidence:** Burstiness B=0.77, CV=4.37, 21/21 spike days reject uniform null at p<0.001. 1,114 bursts across 22 spike days. Mega-bursts up to 377 events (single oracle step clearing hundreds of positions at similar health factors). 78% of multi-event bursts are single-collateral-type (WETH).

**Lead time:** None in the predictive sense. But the mechanism creates a ~7.6 minute quiet window between batches during which the next batch is structurally inevitable if price continues declining. The batch size is predictable from position density at the next oracle step (Phase 2 topology).

**Composite signal potential:** High. Position density distribution (Phase 2) + current price + oracle deviation threshold → predicted batch sizes at each price step. This is the fuel map made operational.

### 2. ETF Flow as Cascade-Type Classifier (Observed — Weak Statistical Support)

**What:** ETF outflows accompany multi-day liquidation clusters; terminal days show flow reversal (inflows). Cluster-initiating spike days have 2x stronger pre-outflows (-$595M vs -$304M average on day -1). 12/14 spike days show negative BTC ETF flows in [-1, 0] window.

**Evidence:** Pattern visible in event study across n=14 spike days. Not statistically significant (n=3 clusters). Two counter-examples (isolated spikes during positive flows) confirm that ETF outflows are not sufficient alone — need position density at next price level.

**Lead time:** 1-3 days. ETF flows are published daily after market close. Large outflows on a spike day's eve may indicate continued selling pressure via T+1 settlement.

**Composite signal potential:** Moderate as a classifier. ETF flow sign during a spike day classifies whether the event will extend (multi-day) or resolve (isolated). Not a predictor of spike initiation. Same structural role as Phase 6's BTC-ETH correlation classifier.

### 3. Within-Day Burst Acceleration (Suggestive — Inconclusive)

**What:** 13/21 spike days show negative Spearman correlation between gap sequence number and observed/expected ratio (later bursts arrive faster). 4 significant at p<0.01. Strongest case: 2025-03-10 shows 7x acceleration.

**Evidence:** Confounded by hourly price resolution. Cannot separate self-reinforcement (liquidation selling → price impact → faster oracle updates) from liquidity thinning (Phase 6: 8-27% LP withdrawal → same volume produces larger impact) or from temporal concentration of the external price decline. The headline ratio (0.39) could flip to >1 after correcting for the hourly averaging bias.

**Lead time:** N/A — would only be useful intra-day, and the resolution needed to confirm it would also be needed to exploit it.

**Composite signal potential:** Low independently. Contributes to the lifecycle model but not actionable without minute-level price data.

## Signals That Were Noise

### Funding Rate → OI Closure (Probe #1 — Negative)

**What was tested:** Whether negative funding settlements on Binance cause OI closures to cluster in the 0-4h post-settlement window.

**Why it failed:** Funding settlement is informationally constrained, not physically constrained. The timing is known, the rate is published in advance. Both funding extremes (deeply negative AND deeply positive) show OI declines — they measure volatility regimes, not cause closures. After conditioning on price direction, funding sign adds no signal (p=0.34). Pre-settlement OI *increased* before deeply negative funding (opposite of prediction).

**Structural lesson:** Informational timing gets arbitraged. Processes with known schedules and visible parameters do not create exploitable timing windows. This also deprioritizes #6 Margin Call Cycles (same structural category).

### Processes Not Tested (Deprioritized)

| Process | Reason Deprioritized |
|---------|---------------------|
| #4 Liquidity Withdrawal | Behavioral, not hard physical constraint. Partially covered by Phase 6 (8-27% LP depth loss). |
| #5 Validator Exit Queue | Weeks-to-months timescale — too slow for crash dynamics. |
| #6 Margin Call Cycles | Informationally constrained (known banking hours). Same category as probe #1. |
| #7 Stablecoin Mint/Burn | Connects to crashes only indirectly through stablecoin demand. |

## Composite Signal Construction

The phase did not produce independent trading signals. It produced a **crash lifecycle model** that makes prior phase signals interpretable as components of a single mechanism.

### The Lifecycle Model

```
Trigger → Within-day execution → Feedback → Inter-day extension → Termination
```

1. **Trigger:** External (macro → ETF redemption) or endogenous (position breach, oracle event).
2. **Within-day execution:** Oracle-gated threshold batching. Price decline quantized by ~0.5-1% oracle steps. Batch size = position density at that price level.
3. **Within-day feedback:** Second-order positive. ~100bps extra decline per 100 liquidations (Phase 5). Magnitude uncertain.
4. **Inter-day extension:** Requires BOTH external pressure (ETF outflows) AND position density at next price level. 3-5 trading day redemption waves align with 5-7 day cascade timescale.
5. **Termination:** ETF flow reversal + position cluster exhaustion.

### How Prior Phase Signals Map to the Model

| Signal | Model Stage | Role |
|--------|------------|------|
| 27h OI lead (Phase 1) | Between trigger and execution | Measures behavioral lag: perp closure (fast, continuous) precedes DeFi liquidation (slow, oracle-gated) |
| Position wall proximity (Phase 2) | Execution | Predicts batch size at each oracle step = density of positions near liquidation price |
| BTC-ETH hourly correlation (Phase 6) | Trigger classification | High correlation during macro-driven crashes (ETF-accompanied, multi-day) vs low correlation during endogenous events (isolated) |
| ETF flow sign (this phase) | Extension classification | Sustained outflows → multi-day. Flow reversal → terminal. Positive flows → isolated. |

### Constructable Composite

A real-time dashboard combining:
1. **Position density map** (Phase 2, on-chain): batch sizes at each price level below current price
2. **OI contraction rate** (Phase 1, CEX API): early warning of approaching liquidation zone
3. **ETF flow sign** (daily, public): classifier for whether a triggered event will extend
4. **Oracle step counter** (on-chain): which batches have fired, which remain

This would provide a read on where in the lifecycle a crash currently is, not whether one will happen. It's a situational awareness tool, not a predictor.

## Next Steps

### If continuing physics-adjacent investigation:
- **Minute-level price data** would resolve the self-reinforcement question. Sources: Binance 1-min klines (free API), or Kaiko (paid). This is the single highest-value data acquisition for strengthening the model.
- **Oracle event logs** (Chainlink AnswerUpdated) for spike days would confirm the oracle-gating mechanism directly. Requires archive RPC access (Alchemy paid tier or alternative).

### If pivoting to application:
- The lifecycle model is ready for prototyping as a monitoring dashboard. The components (position density, OI rate, ETF flows, oracle events) are all available via public APIs or on-chain data.
- The 27h OI signal remains the only tested predictive signal. The physics phase did not produce new predictive signals — it produced the mechanistic context that explains *why* the OI signal works and *when* it should be trusted (during oracle-gated batch regimes, not during smooth declines).

### Open questions the model does not answer:
- What triggers endogenous spike days? (The two non-ETF spikes during positive flows)
- Does wstETH's growing dominance (56% of real liquidation volume by 2025) change the feedback strength? (Less liquid collateral → more price impact per liquidation)
- Can position density be monitored in real-time with enough resolution to predict batch sizes before oracle updates?

## Data Acquired This Phase

| Data | Path | Coverage |
|------|------|----------|
| BTC/ETH ETF daily flows | `physics/data/etf_daily_flows.csv` | 565 trading days, Jan 2024 – Mar 2026 |

All other analyses used existing data from prior phases.
