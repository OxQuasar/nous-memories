# Position Topology — Signal Synthesis

## Signals Tested

### Tier 1: Strong Signal (conditional)

**Real wall density (R10%, R20%, R30%)** — cumulative real debt within X% below current ETH price.
- Measures how much cascade fuel exists if drawdown reaches depth X.
- R20% > $100M correctly identified all 4 escalating episodes as high-risk.
- R20% < $30M correctly identified post-clearing safety (FTX: $21M, no cascade despite 30% drawdown).
- 2 false positives at 6/8 (75%): Iran ($162M, absorbed — shock too shallow), Sep 2024 ($270M, absorbed — 7% dip didn't reach wall).
- **Limitation:** This is a conditional severity gauge, not a binary predictor. It tells you what happens *if* drawdown reaches a given depth, not whether it will.

**Gradient density (real debt per 1% of price within R20%)** — measures cascade self-sustainability.
- Self-sustaining progressive cascade threshold: ~$14M+ per 1% of price (empirical from Yen $21M/1%, Feb 2025 $14M/1%).
- Below ~$8M/1%, liquidations are absorbed individually without cascading (Iran $8M/1%, Aug 2023 $3.7M/1%).
- Overlap zone: Sep 2024 ($13.5M/1%, absorbed because dip was only 7%) and Feb 2025 ($14.0M/1%, escalated with 17% drawdown) — same density, different outcome depending on shock depth.

**Single whale proximity** — largest real position within reachable range.
- Cliff cascade mode: a single position >$100M can overwhelm market depth when breached.
- The stETH episode is the clearest example: $2M/1% gradient (would not self-sustain) but $282M whale at 34% below created a cliff when breached.
- This captures cases that gradient density alone misses.

### Tier 2: Structural Signal (not directly predictive, but essential context)

**Real/phantom decomposition** — fraction of near-price debt that is phantom (ETH-loop strategies).
- Not a trading signal. Infrastructure for interpreting all other signals correctly.
- Without it, any liquidation heatmap is dominated by phantom positions that don't respond to ETH price.
- Phantom ratio has evolved from 2% (Jan 2022) to >90% (Mar 2026). The "headline" wall numbers are increasingly misleading over time.

**Phantom ratio trend** — structural evolution of DeFi risk profile.
- Tracks the rotation from price-cascade fragility to correlation-cascade fragility.
- Jan 2022: 2% → Jun 2022: 35% → Nov 2022: 42% → Aug 2023: 43% → Apr 2024: 44% → Aug 2024: 54% → Sep 2024: 58% → Feb 2025: 70% → Mar 2026: >90%.
- Implication: the monitoring system should increasingly focus on LST depeg risk rather than ETH/USD wall proximity.

**Post-clearing state** — whether a recent crash has emptied the topology.
- After a major crash, positions above the crash trough are liquidated. Topology is defensively empty until new leverage rebuilds.
- FTX (Nov 2022): 5 months after June crash cleared everything above $1,000. Only $37M real debt in the 30% crash zone. 30% drawdown with no DeFi amplification.
- Useful as a "safe" signal: if recent crash cleared the path, moderate stress is absorbed.

### Tier 3: Noise / Not Useful

**R10% alone as binary classifier** — 5/8 correct.
- Misclassifies stETH (whale was at 34%, not within 10%), Sep 2024 (high R10% but shallow dip), Feb 2025 (low R10% but 17% drawdown hit walls at 10-20%).
- Too narrow a band to capture the full range of cascade paths.

**R20% / TotalDebt normalization** — does not improve classification.
- Threshold is not stable across regimes. Aug 2023 shows 9.1% (absorbed) while Feb 2025 shows 2.4% (escalated).
- Scale-dependent metric doesn't normalize cleanly because market growth, phantom ratio, and ETH price level all shift the denominator.

**Aggregate wall size without real/phantom decomposition** — misleading.
- The apparent $4.3B wall in 2026 is >99.99% phantom. Using undecomposed numbers would show massive wall 5% below price and predict imminent cascade risk — completely wrong.

## Composite Signal Design

The strongest prospective signal combines three components:

```
At episode onset, compute:
  1. R20% (real debt within 20% below current price)
  2. Gradient density = R20% / 20 (average real debt per 1% of price)
  3. Whale factor = max single real position within 30% of price

Risk assessment:
  - LOW:  R20% < $30M AND no whale > $50M within 30%
  - MOD:  R20% $30-100M OR gradient < $8M/1%
  - HIGH: R20% > $100M OR (gradient > $14M/1%) OR (whale > $100M within 30%)
```

Performance on 8 episodes:
- HIGH correctly flagged all 4 escalating episodes
- LOW correctly flagged FTX and Aug 2023 as safe
- 2 false positives (Iran, Sep 2024) — correctly identified potential that wasn't reached by shallow drawdowns

The composite signal is a severity gauge: "if drawdown exceeds 10-15%, here's the cascade risk." It does not predict whether the drawdown will occur.

## Current State Assessment (Mar 2026, ETH $2,202)

| Metric | Value | Assessment |
|--------|-------|------------|
| R5% real | $313K | Negligible |
| R10% real | $9.2M | Negligible |
| R20% real | $73M | LOW — moderate stress absorbed |
| R30% real | $572M | Moderate — significant fuel at 30%+ drawdown |
| R50% real | $1.57B | Substantial — severe crash would trigger meaningful cascade |
| Gradient/1% (R20%) | $3.6M | Well below self-sustaining threshold |
| Largest real whale | $143M at $1,347 (39% below) | No cliff within 30% |
| Phantom wall 5% | $3.78B | Massive — but only responds to LST depeg |

**Current risk:** ETH/USD price-cascade risk is LOW. First meaningful real wall at 30%+ below. The system's actual vulnerability is the $5.6B phantom wall at HF 1.03-1.05, which would activate on a staking derivative depeg event — a different risk surface not yet characterized.

## Next Steps

The position topology investigation is complete for the ETH/USD price-cascade question. Two directions remain:

1. **Real-time topology monitor:** Periodic (daily/weekly) snapshots computing the composite signal. Infrastructure exists. Would add a severity-assessment layer to the existing monitoring system.

2. **Correlation-cascade investigation:** Characterize the depeg-activation threshold for the $5.6B phantom wall. Requires: DEX liquidity depth per LST, historical depeg magnitudes, oracle lag behavior. This is the risk surface the current market is actually exposed to. Separate investigation with different data requirements.
