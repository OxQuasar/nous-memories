# DeFi Signals Synthesis

## Summary

Six iterations tested whether on-chain DeFi metrics produce actionable signals for ETH price. Started with "does on-chain data predict price direction?" Arrived at a different and more interesting finding: "the temporal structure of liquidation flow classifies whether the system's fragility is resolving or deepening."

One characterized signal emerged. Several were killed. The thesis was refined.

---

## Signals Tested — Ranked by Outcome

### 1. Liquidation Concentration Ratio ✦ Primary Finding

**What it is:** When daily liquidation volume crosses the 90th percentile, classify by whether today's volume is >50% of the trailing 7-day total (concentrated) or ≤50% (distributed).

**Result:** Distributed liquidations (multi-day bleed) → median -3.48% over 7 days, 70.7% negative. Concentrated liquidations (single-day spike) → median +0.19%, ~50% negative. Spread: 3.67pp. Mann-Whitney p=0.076. Tested across Aave v2+v3, Compound v2+v3, and Maker. 36,237 events, $2.02B, 1,524 days.

**Mechanism:** A concentrated spike clears the overhang — weak positions liquidated in one event, fragility resolved, price stabilizes or bounces. Distributed liquidations mean the system is peeling through layers of leverage — each day's clearing reveals more fragile positions beneath.

**Properties:**
- Fires ~10x/year (distributed class)
- Computable in real-time from free public RPC data
- Not easily arbitraged — reads temporal structure, not just volume
- Borderline significant (p=0.076) but mechanistically grounded and stable across protocol expansion

### 2. Volatility Regime Signal — Real but Modest

**What it is:** Log-liquidation-volume predicts forward 7-day realized volatility.

**Result:** r=0.235 (~5.5% variance explained). 1-day absolute returns show clean monotonic gradient: quiet days 2.36%, extreme days 4.62% (~2x). Dissipates by 7 days.

**Assessment:** Confirms that liquidation events predict the *magnitude* of moves regardless of direction. But the explanatory power is modest and may already be priced into options markets (untested). Useful as supporting evidence for the fragility thesis, not standalone.

### 3. Stablecoin Supply (DAI + GHO + USDS) — Lags, Not Predictive

**What it is:** DeFi-native stablecoin supply as a proxy for leverage expansion.

**Result:** Combined supply lags ETH price by ~8 days. DAI shows concurrent correlation (r=0.23) but doesn't lead. GHO is governance-driven noise. USDS too new.

**Why it failed:** The thesis assumed a reflexive loop (price up → mint stablecoins → buy more → price up). The data shows the first half (price → minting) but the loop doesn't close — minted stablecoins disperse into DeFi rather than feeding back into spot demand. Expansion is voluntary and multi-path.

**Verdict:** Kill as a directional signal. The ~8-day lag is itself informative (confirms system response time) but not tradeable.

### 4. stETH/ETH Spread — Arbitraged Away

**What it is:** stETH discount from parity as a stress indicator.

**Result:** Pre-Shanghai (before April 2023): strong concurrent signal (r=-0.375), conditional -4.3% mean 14d returns at 67.5% hit rate. Post-Shanghai: noise. Coin-flip at all horizons.

**Why it failed:** Redemption arbitrage (enabled by Shanghai upgrade) compresses the spread before it can accumulate information. The mechanical relationship was real but got destroyed by infrastructure improvement.

**Verdict:** Kill. Signal existed in the illiquid regime and was arbitraged away. Pattern recognition: any signal based on a price spread that can be closed by a faster arbitrageur will decay.

### 5. Liquidation Wall Map — Legible but Snapshot-Only

**What it is:** Current distribution of liquidation thresholds by ETH price level.

**Result:** $2.16B total across 11 protocols. Two whale positions ($213M Compound, $201M Maker) at ~$1,400 dominate. Current regime: not fragile (walls 60%+ below price).

**Assessment:** The map is readable and informative for current-state assessment. But without historical wall snapshots, it can't be backtested. Useful as a monitoring dashboard, not a tested signal. Whale concentration (94% in two positions) makes walls unstable — one deleverage removes them.

---

## What Was Noise — Don't Revisit

| Signal | Why it's noise | Notes |
|---|---|---|
| GHO supply | Driven by Aave governance, not market conditions | r=-0.061, peak at window edge |
| USDS (Sky Dollar) supply | Too new (541 days), spurious peak at lag boundary | Only launched mid-2024 |
| stETH/ETH post-Shanghai | Redemption arb compresses spread to noise | Any spread-based signal with an arb mechanism will decay |
| Raw liquidation volume → price direction | Volume alone doesn't predict direction | Must be combined with temporal structure (concentration ratio) |

---

## What Was Not Tested

| Signal | Reason deferred | Connection to findings |
|---|---|---|
| USDT/USDC supply | Different mechanism (capital inflow, not DeFi leverage) | Could be a separate investigation |
| Lending utilization (Realm 2) | Cross-correlation is wrong tool; reframe as fragility-state test | Could test: does high utilization predict distributed liquidation patterns? |
| TVL divergence (Realm 4) | No clear connection to primary finding | Park |
| Bridge flows (Realm 5) | No clear connection to primary finding | Park |
| L2 liquidation events | Same code, different RPCs | Tests universality of concentration ratio across chains |
| IV/options data | Requires options market data | Tests whether vol expansion is already priced in |

---

## Composite Signal Potential

The concentration ratio is currently a standalone signal. Two extensions could strengthen it:

**Extension 1: Utilization → Liquidation Regime Chain**
If high lending utilization predicts distributed (cascade-type) liquidation patterns, that creates a two-step causal chain: high utilization → distributed liquidations → further downside. Utilization becomes a *precondition indicator* — it tells you the system is primed for cascade mode before the liquidations start. Each link is independently testable.

**Extension 2: Wall Proximity + Concentration Ratio**
During periods where liquidation walls are near the current price (not the case now, but would be in a drawdown), the concentration ratio signal becomes more meaningful — there's a known pool of forced selling ahead. The wall map as context + concentration ratio as classification = a richer fragility model.

Both extensions are premature until the base signal is further characterized.

---

## Thesis Revision

The original thesis claimed: "On-chain leverage data is transparent and can be used for directional positioning."

**What held:**
- The leverage topology IS transparent and legible. Liquidation walls can be mapped. Stablecoin supply tracks leverage. The data is real and accessible.
- Mechanical relationships between leverage metrics and price are real — supply follows price, liquidations accompany drawdowns, spread reflects stress.

**What didn't hold:**
- Expansion-side signals (supply growth, TVL, utilization climbing) lag or are concurrent — they don't lead. The reflexive loop doesn't close on the expansion side because minted stablecoins disperse rather than feeding back into spot demand.
- Contraction-side price signals (stETH spread) get arbitraged away by infrastructure improvement.
- Simple cross-correlation is the wrong tool. The thesis describes regime transitions and thresholds, not linear continuous relationships.

**What emerged instead:**
- The legible thing isn't *where price goes* — it's *what mode the system is in*. Fragility resolving vs deepening is classifiable from the temporal structure of liquidation flow.
- The concentration ratio (single-spike capitulation vs multi-day bleed) is a second-order structural reading that classifies system state with a 3.67pp median effect and 71% hit rate.
- This is harder to arbitrage than first-order signals because it requires reading the *shape* of liquidation flow over time, not just volume or price.

---

## Next Steps — Decision Point

**Option A: L2 Universality Test**
Run the same concentration ratio analysis on Aave liquidations on Arbitrum, Base, Optimism. Same code, different RPC endpoints. Tests whether the mechanism is about leverage topology universally or Ethereum-L1-specific. Low effort, characterization value.

**Option B: Utilization → Liquidation Regime Link**
Pull lending utilization data (Realm 2, reframed). Test whether high utilization predicts distributed liquidation patterns. Builds a causal chain that extends the primary finding. Higher effort, higher value if it works.

**Option C: Real-Time Monitor**
Build a simple pipeline that monitors daily liquidation events across Aave/Compound/Maker, computes the concentration ratio, and flags distributed-mode days. Shifts from research to operational. Premature if the signal needs more validation, appropriate if the current characterization is sufficient.

The investigation is at a natural stopping point for the broad exploration phase. The concentration ratio signal is the output worth carrying forward.
