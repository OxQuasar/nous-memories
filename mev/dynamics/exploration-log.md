# Dynamics — Exploration Log

## Iteration 1: Exchange Flow Epoch Analysis (Step 1)

**Date:** 2026-03-20  
**Script:** `memories/mev/dynamics/exchange_flow_epochs.py`  
**Data produced:** `data/daily_flows.csv`, `data/epoch_flow_summary.csv`, `data/flow_price_lag.csv`

### What was tested

- Daily net exchange flow (flow_out - flow_in) vs daily ETH price returns, cross-correlated at lags -5 to +5 days across the full 2022-01 to 2026-03 dataset.
- Within-epoch Pearson correlation between daily net_flow_ntv and daily price returns for each of 11 epochs.
- Epoch-level summary metrics: total/avg net flow, reserve start/end, reserve change, price change.

### What was measured

**Flow-price signal: null at daily resolution.**
- Cross-correlations at all lags -5 to +5 are below |0.04|. No lead, no lag, no contemporaneous signal.
- Within-epoch correlations are also weak. Strongest is 0.17 (2022_bear_1). Most near zero.

**Epoch-level reserve patterns:**

| Epoch | Reserve Change | Reserve Δ% | Price Δ% |
|-------|---------------|-----------|----------|
| 2022_bear_1 | +333K ETH | +2.5% | -71% |
| 2022_rally | +294K | +2.1% | +88% |
| 2022_bear_2 (FTX) | -1,337K | -9.5% | -40% |
| 2023_recovery | +722K | +6.2% | +249% |
| 2024_consolidation | +145K | +1.2% | -37% |
| 2024_bull | +1,097K | +8.8% | +59% |
| 2025_crash | +3,956K | +29.2% | -61% |
| 2025_recovery | +1,155K | +6.6% | +177% |
| 2025_q4_chop | -4,203K | -22.8% | -34% |
| 2026_crash | +1,256K | +8.7% | -35% |
| 2026_recovery | -6K | -0.04% | +23% |

**Measurement gap discovered (unmeasured flows dominate):**
- Net measured flow and reserve changes diverge substantially. Examples:
  - 2025_crash: net measured outflow +1.58M ETH, but reserves *increased* +3.96M. ~5.5M ETH discrepancy.
  - 2023_recovery: net measured outflow +5.9M ETH, but reserves only +722K. ~5.2M discrepancy opposite direction.
  - 2025_q4_chop: net measured outflow +4.65M, reserves dropped -4.2M. ~8.9M discrepancy.
- The unmeasured component (staking, bridges, contract interactions) is larger than the measured flow_in/flow_out. The CoinMetrics flow methodology captures a minority of actual balance movements.

**FTX anomaly as structural control:**
- Every crash epoch shows reserve increases except 2022_bear_2 (FTX collapse), where reserves dropped by 1.34M ETH. FTX's own reserves vanished. This confirms reserve data partly reflects exchange solvency, not just user behavior.

### What was not tested

- Hourly or sub-daily flow resolution. Not pursued — the measurement gap means refining temporal resolution on partial data has low expected return.
- Causal attribution of reserve changes (what fraction comes from DeFi liquidation proceeds vs staking flows vs bridge activity).

### What remains open

- During the 2025 crash (+3.96M ETH to exchanges), what fraction of that reserve increase came from liquidated DeFi positions vs non-leveraged holder capitulation?
- Whether the *unmeasured* component of exchange flows carries signal is unknown and may not be directly testable with available data.

---

## Iteration 2: Reserve-Price Correlation + Full Liquidation Pull (Steps 1b + 2)

**Date:** 2026-03-20  
**Scripts:** `memories/mev/dynamics/reserve_price_lag.py`, `memories/mev/dynamics/liquidation_pull.py`  
**Data produced:** `data/reserve_price_lag.csv`, `data/liquidations_full.csv`

### What was tested

**Task A: Reserve change vs price correlation.**
- Daily `reserve_change_ntv` (direct balance observation from sply_ex_ntv) vs daily price returns, cross-correlated at lags -5 to +5. This tests whether the unmeasured flow component carries signal that net_flow missed.

**Task B: Full Aave v2/v3 liquidation event pull.**
- All LiquidationCall events from Aave v2 (block 14,000,000+) and v3 (block 16,300,000+) through present, with NO collateral asset filter. Full decode of collateral_asset, debt_asset, user, amounts, liquidator from event topics and data fields.
- Each event classified as: "phantom" (LST collateral → WETH debt), "real" (ETH/LST collateral → stablecoin debt), or "other."
- The original flow-phase pull filtered to WETH-collateral only (27,702 events). This pull captured all collateral types.

### What was measured

**Reserve-price correlation: also null.**
- Max |r| = 0.044 across all lags -5 to +5. Reserve changes are equally uninformative as net flows.
- Neither the measured flow component nor the direct balance observation predict or track daily price returns.
- Exchange flow analysis is exhausted for this phase. Neither net flows, reserve changes, nor any lag structure produces actionable signal at daily frequency.

**Full liquidation dataset: 65,382 events.**
- Aave v2: 41,264 events (63.1%). Aave v3: 24,118 events (36.9%).
- Category breakdown: real 38,055 (58.2%), other 27,166 (41.5%), phantom 161 (0.2%).

**Phantom liquidations are vanishingly rare: 161 out of 65,382 events (0.25%).**

Breakdown by collateral→debt:
- stETH→WETH: 108 events
- wstETH→WETH: 47 events
- weETH→WETH: 3, rETH→WETH: 2, cbETH→WETH: 1

Per-epoch phantom counts:

| Epoch | Total Events | Phantom | Phantom % |
|-------|-------------|---------|-----------|
| 2022_bear_1 | 12,284 | 12 | 0.10% |
| 2022_rally | 3,569 | 2 | 0.06% |
| 2022_bear_2 | 1,988 | 3 | 0.15% |
| 2023_recovery | 3,581 | 6 | 0.17% |
| 2024_consolidation | 5,791 | 16 | 0.28% |
| 2024_bull | 2,991 | 11 | 0.37% |
| 2025_crash | 12,054 | 21 | 0.17% |
| 2025_recovery | 4,386 | 30 | 0.68% |
| 2025_q4_chop | 10,568 | 24 | 0.23% |
| 2026_crash | 7,374 | 14 | 0.19% |
| 2026_recovery | 749 | 22 | 2.94% |

**The March 10 CAPO incident dominates the phantom signal.**
- 22 of 161 phantom events occurred March 10-11 2026, in blocks 24626860-24626867 (~73 seconds) plus 2 dust events 16 hours later.
- 8,609 wstETH seized in total. Single largest event: 5,328 wstETH (~$12M) from one user in block 24626860.
- This was caused by Chaos Labs pushing a stale snapshot ratio (2.85% artificial underpricing), documented in correlation phase.
- Excluding March 10: **139 organic phantom liquidations in 4.2 years** (~33/year), vs ~15,500 non-phantom/year.

**The phantom wall is functionally non-liquidatable by market forces.** Mechanism confirmed:
- CAPO oracle reads protocol exchange rates (LST/ETH), not DEX market prices.
- Protocol exchange rates only increase (staking yield accrual).
- ETH/USD crashes do not affect phantom health factors — only real positions liquidate during crashes.
- The only demonstrated trigger for phantom liquidation is oracle operational failure (stale ratio, misconfigured cap).

**"Other" category decomposition:**
- Altcoin→stablecoin (LINK, WBTC, AAVE, UNI → USDC/USDT/DAI): ~8,600 events. Same directional risk structure as "real."
- Short-ETH positions (USDC/DAI → WETH): ~850 events. Inverse directional bets — liquidate when price rises.
- WETH→WETH: 737 events. Possibly e-mode positions or flash loan artifacts.
- Stablecoin→stablecoin: ~5,300 events.

**Liquidator concentration is extreme.**
- 570 unique liquidators for 65K events. Top 10 handle 48.4%, top 20 handle 63.9%.
- Top liquidator (`0xd9115609...`): 6,718 events (10.3%).
- During March 10 CAPO incident: 5 bots captured all 49 events in 84 seconds. Single largest capture: 5,328 wstETH in one block.

**Top collateral assets across all events:**
- WETH: 49.1%, stETH: 10.8%, WBTC: 8.3%, LINK: 7.6%, USDC: 6.1%, AAVE: 3.3%, wstETH: 2.4%

**Top debt assets:**
- USDC: 42.5%, USDT: 26.3%, DAI: 10.9%, WETH: 3.9%, WBTC: 2.1%, BUSD: 2.1%, GHO: 1.9%

### What was not tested

- USD-denominated liquidation volume per epoch (events are counted, not value-weighted — requires price at each event's timestamp to compute USD amounts).
- Temporal structure within crash epochs: steady drip vs concentrated spikes for real liquidations.
- Cross-referencing liquidation event timestamps with exchange reserve changes to test whether DeFi liquidation proceeds explain the reserve movement gap.
- Position topology snapshots (Step 3) — how does the real position map reshape across cycles?
- Protocol TVL and utilization changes (Step 4).

### What remains open

- What is the USD volume of real liquidations per epoch, and how does it compare to the exchange reserve changes in those epochs?
- Do real liquidations during crashes follow a steady drip or spike pattern? Does the temporal structure differ by crash catalyst (Terra vs FTX vs Yen carry vs 2025/2026)?
- How does the real position topology (health factor distribution, concentration, total collateral/debt) change through each epoch? (Requires Step 3 subgraph snapshots.)
- The plan's Key Question #1 (leverage build/unwind asymmetry) and #5 (post-crash topology) remain untested — these require position snapshots, not just liquidation events.
- The plan's Key Question #2 (phantom position lifecycle) is partially answered: phantom positions don't liquidate during crashes. When they open/close (during bulls? rate inversions?) still requires position snapshot comparison across epochs.

### Connections to prior phases

- The 22 phantom events on March 10 match the correlation phase's documentation of the CAPO incident (49 liquidation events in 84 seconds from stale Chaos Labs snapshot). The dynamics data independently confirms the same event and extends it: the $1.42B whale survived by 0.98% margin.
- The position phase identified $5.6B in phantom positions. The dynamics data shows this wall is structurally immune to market crashes — the risk is oracle operational, not market-directional.

### Next steps identified

1. Epoch-level real liquidation volume/intensity analysis on existing data (no new pulls needed).
2. Scoping Step 3 (position topology snapshots via subgraph historical queries) — focused on real positions across cycles.

---

## Iteration 3: Real Liquidation Dynamics — Temporal Structure, Intensity, Recharge Cycle

**Date:** 2026-03-20  
**Script:** `memories/mev/dynamics/liquidation_dynamics.py`  
**Data produced:** `data/epoch_liquidation_summary.csv`, `data/crash_spike_days.csv`

### What was tested

- USD-denominated real liquidation volume per epoch, estimated via debt-side conversion (stablecoin debt amounts taken at face value, WETH debt × ETH price, WBTC debt × rough BTC price).
- Temporal concentration within crash epochs: spike days (>2σ above epoch mean) and fraction of epoch volume in top 3 days.
- Cross-epoch intensity comparison: liquidation volume normalized by crash magnitude and epoch duration.
- Collateral composition of real liquidations by epoch (by event count and by USD volume).
- User overlap between consecutive crash epochs (measuring leverage recharge).

### What was measured

**Temporal concentration: liquidation is a spike phenomenon.**

| Crash Epoch | Real Liq USD | Spike Days | Top 3 Days % | Days to First $10M+ |
|-------------|-------------|-----------|-------------|---------------------|
| 2022_bear_1 | $229M | 6 | 46% | 20 |
| 2022_bear_2 | $12M | 2 | 89% | never reached |
| 2024_consolidation | $302M | 1 | 77% | 8 |
| 2025_crash | $315M | 5 | 52% | 49 |
| 2025_q4_chop | $217M | 5 | 75% | 31 |
| 2026_crash | $193M | 3 | 87% | 45 |

In every crash, 3 days account for 45-89% of total liquidation volume. A single day (Aug 5, 2024 — Yen carry unwind) produced $187M, which was 62% of the entire 2024_consolidation epoch. That day's 1,633 real events were concentrated in the first 4 hours (UTC 0-3am), with 1,528 events by 4am.

**Intensity varies 26× across epochs — pre-crash leverage state dominates.**

| Crash Epoch | Price Δ% | Real Liq USD | Liq/Day USD | Rebuild Time |
|-------------|---------|-------------|------------|-------------|
| 2022_bear_1 | -71% | $229M | $1.4M | — (first epoch) |
| 2022_bear_2 | -42% | $12M | $0.1M | 56 days |
| 2024_consolidation | -39% | $302M | $13.0M | 475 days |
| 2025_crash | -61% | $315M | $15.2M | 131 days |
| 2025_q4_chop | -39% | $217M | $5.3M | 136 days |
| 2026_crash | -34% | $193M | $61.8M | 0 days (continuous) |

The 2022_bear_2 (FTX, -42%) produced only $12M while 2024_consolidation (-39%) produced $302M — similar % decline, 25× difference. The difference is the 475-day bull market between them that rebuilt leverage with fresh participants.

**Crash/recovery asymmetry is massive.**

| Crash → Recovery | Crash Liq | Recovery Liq | Ratio |
|-----------------|----------|-------------|-------|
| 2022_bear_1 → 2022_rally | $229M | $6M | 36× |
| 2022_bear_2 → 2023_recovery | $12M | $35M | 0.4× |
| 2024_consolidation → 2024_bull | $1,930M | $98M | 20× |
| 2025_crash → 2025_recovery | $1,713M | $26M | 65× |
| 2026_crash → 2026_recovery | $4,261M | $5M | 894× |

Crashes produce 20-894× more liquidation volume than subsequent recoveries (exception: FTX→2023_recovery inversion, because FTX produced anomalously low liquidations). The system deleverages in hours, rebuilds over months.

Note: the $1,930M and $4,261M figures for 2024_consolidation and 2026_crash in the "all categories" view are substantially higher than the "real only" figures ($302M and $193M). The difference comes from "other" category (altcoin→stablecoin) liquidations. By "real" category alone, which isolates ETH-exposed leverage, the ratios are still 20-65×.

**User overlap confirms the recharge cycle.**

| Prior Crash → Next Crash | Rebuild Time | User Overlap |
|--------------------------|-------------|-------------|
| 2022_bear_1 → 2022_bear_2 | 56 days | 55.7% (414/743) |
| 2022_bear_2 → 2024_consolidation | 475 days | 5.1% (74/1,447) |
| 2024_consolidation → 2025_crash | 131 days | 15.2% (632/4,162) |
| 2025_crash → 2025_q4_chop | 136 days | 20.7% (894/4,325) |
| 2025_q4_chop → 2026_crash | 0 days | 16.9% (414/2,456) |

After 475 days of rebuild, 95% of liquidated users are new participants. After 56 days, 56% are the same people being liquidated again (on dust positions). The leverage supply replenishes proportional to rally magnitude × rebuild time.

**Collateral composition: WETH dominates by USD volume, stETH event count is dust.**

By USD volume, WETH is 73-99% of real liquidation collateral across all crash epochs. wstETH grew to 22% by volume in 2025_q4_chop, but reverted to 0.9% in 2026_crash. The stETH event count is high (44% in Q4 2025) but represents dust positions — median stETH event is 0.002 stETH (~$6), total 2,534 stETH events = 11.1 stETH (~$33K). Meanwhile WETH events: 2,997 events = 28,946 WETH (~$85M+).

The LST transition has happened in position building (the phantom wall at $5.6B) but NOT in liquidation outcomes. The system that actually liquidates is still overwhelmingly WETH→stablecoin.

### What was not tested

- Pre-crash total real debt levels at epoch boundaries (requires Step 3 position snapshots). This would convert the recharge model from qualitative to quantitative.
- Health factor distribution shifts through crash epochs.
- Post-crash topology comparison: is the rebuilt system the same shape or structurally different?
- Protocol TVL and utilization rate changes (Step 4).
- Hourly liquidation clustering within spike days (partially examined for Aug 5 2024 — concentrated in first 4 hours UTC 0-3am — but not systematically across all spike days).

### What remains open

- The recharge model predicts: pre-crash total real-position debt should correlate with subsequent epoch liquidation volume. This is testable via Step 3 position snapshots. If confirmed, it provides a leading indicator for liquidation intensity.
- What does the health factor distribution look like before a crash vs after? How far does the distribution shift, and how quickly does it rebuild?
- Is the rebuilt leverage topology the same shape as pre-crash (same collateral types, same user size distribution), or does it change structurally? The user overlap data suggests substantial turnover (5-57% overlap), but we don't know the size distribution of new vs returning participants.
- The 2026_crash "all categories" figure ($4,261M) vs "real only" ($193M) has a large gap. The "other" category contributed heavily — suggesting altcoin positions (LINK, WBTC, etc.) may be a larger part of the liquidation picture than the "real" filter captures.

### Emerging model: DeFi leverage recharge cycle

The data across three iterations points to a coherent model:

1. **The phantom wall ($5.6B LST loops) does not participate in market-cycle dynamics.** 139 organic liquidations in 4.2 years. Risk is oracle-operational (CAPO stale ratios), not market-directional.

2. **Real positions follow a recharge cycle:** crash depletes leverage → bull rebuilds it with fresh participants → next crash releases stored energy. The intensity of the crash depends on how much energy was stored (rebuild time × rally magnitude), not on crash magnitude.

3. **Liquidation is a spike phenomenon:** 3 days = 45-89% of epoch volume. The system can go from stable to mass liquidation in hours (Aug 5 2024: 1,528 events in 4 hours).

4. **Crash/recovery asymmetry is 20-894×** by liquidation volume. Deleveraging is violent and fast; rebuilding is slow and gradual.

5. **The collateral being liquidated is still overwhelmingly WETH→stablecoin** by USD value, despite the system's position topology having migrated heavily toward LSTs.

---

## Iteration 4: Protocol Metrics + Recharge Model Test (Step 4)

**Date:** 2026-03-20  
**Script:** `memories/mev/dynamics/protocol_metrics.py`  
**Data produced:** `data/protocol_metrics_daily.csv`, `data/protocol_epoch_summary.csv`

### What was tested

- Aave v2 + v3 Ethereum TVL and borrow data from DefiLlama API, daily resolution, full 2022-2026 range.
- Pre-crash total borrowed (USD and ETH-denominated) correlated with epoch real liquidation volume across 6 crash epochs.
- Interaction term: borrowed × crash depth as a predictor of liquidation intensity.
- Utilization rate dynamics across epochs (utilization = borrowed / (tvl + borrowed)).
- ETH-denominated vs USD-denominated borrow changes during crashes — testing whether the system truly deleverages.

### What was measured

**Recharge model quantitative test: weak in simple form.**

| Crash Epoch | Borrowed Start | Crash % | Real Liq USD | Utilization |
|-------------|---------------|---------|-------------|-------------|
| 2022_bear_1 | $6.0B | -71% | $229M | 41.5% |
| 2022_bear_2 | $2.2B | -42% | $12M | 29.2% |
| 2024_consolidation | $4.8B | -39% | $302M | 33.0% |
| 2025_crash | $13.6B | -61% | $315M | 41.5% |
| 2025_q4_chop | $24.1B | -39% | $217M | 42.5% |
| 2026_crash | $17.0B | -34% | $193M | 38.7% |

- `borrowed_start` vs `total_real_liquidation_usd`: r = 0.29
- `borrowed_start × crash_pct`: r = 0.47
- `crash_pct` alone: r = 0.28

The interaction term (borrowed × crash depth) is the best single predictor at r=0.47, but with only 6 data points this is not strong. The qualitative recharge pattern holds (FTX low because depleted, Yen carry high because rebuilt) but aggregate borrow is not a clean quantitative predictor.

**ETH-denominated borrow change during crashes: a denomination artifact.**

Initial observation: ETH-denominated borrowing INCREASES during every crash epoch (+7% to +89%). This appeared to contradict the deleveraging narrative.

Correction (via review discussion): this is almost entirely a mechanical price effect. When ETH price drops 50%, the ETH-equivalent of constant USD debt doubles. Comparing actual ETH-borrow change to the mechanical (price-only) expectation:

| Epoch | Mechanical (price-only) | Actual ETH Δ | Residual (real change) |
|-------|------------------------|-------------|----------------------|
| 2022_bear_1 | +247% | +7% | -240% |
| 2022_bear_2 | +73% | +31% | -42% |
| 2024_consolidation | +64% | +89% | **+25%** |
| 2025_crash | +155% | +69% | -86% |
| 2025_q4_chop | +63% | +19% | -45% |
| 2026_crash | +51% | +18% | -33% |

The residual is negative in 5 of 6 crashes — the system IS deleveraging in real terms. USD borrow change was the truthful measure. The one positive residual is 2024_consolidation (+25%), a genuine anomaly.

**The 2024_consolidation anomaly: counter-cyclical leverage building.**

During a -39% crash (Yen carry unwind):
- TVL dropped -10% (depositors withdrew)
- Borrowing GREW +15% in USD, +89% in ETH (borrowers increased leverage)
- Utilization jumped from 33.0% to 38.7%
- Aug 5 produced $187M in liquidations (62% of epoch) — happening WHILE aggregate borrowing was growing

This is an exogenous macro shock: ETH price dropped from a non-crypto catalyst, but DeFi participants treated it as a buying opportunity. New leverage was being added during the crash, creating fresh liquidation candidates in real time.

**Crash taxonomy (conjectured from observed patterns):**
- **Endogenous crashes** (Terra 2022, FTX 2022, 2025 crash): participants deleverage, USD borrow declines 22-69%, residual deeply negative. Liquidation volume proportional to stored leverage.
- **Exogenous crashes** (Yen carry 2024): participants increase leverage (buying the dip), USD borrow grows +15%, residual positive. Liquidation volume comes from speed of price drop overwhelming position management, compounded by new leverage being added mid-crash.

This taxonomy is conjectured from a sample of 6 crashes, with only 1 classified as exogenous. It fits the observed data but is not robustly tested.

**Utilization homeostasis: sticky at 38-42%.**

| Epoch | Regime | Util Start | Util End | Δ |
|-------|--------|-----------|---------|---|
| 2022_bear_1 | crash | 41.5% | 31.2% | -10.3pp |
| 2022_rally | bull | 30.2% | 29.2% | -0.9pp |
| 2022_bear_2 | crash | 29.2% | 33.2% | +4.0pp |
| 2023_recovery | bull | 33.8% | 33.1% | -0.7pp |
| 2024_consolidation | crash | 33.0% | 38.7% | +5.7pp |
| 2024_bull | bull | 38.4% | 41.3% | +2.9pp |
| 2025_crash | crash | 41.5% | 39.2% | -2.3pp |
| 2025_recovery | bull | 38.2% | 42.6% | +4.5pp |
| 2025_q4_chop | crash | 42.5% | 39.9% | -2.6pp |
| 2026_crash | crash | 38.7% | 38.6% | -0.1pp |
| 2026_recovery | bull | 39.0% | 38.5% | -0.4pp |

Post-2022, utilization stays in a narrow 33-43% band. The 2022_bear_1 was the only epoch to break below 30%. This suggests a rate-controller feedback loop: utilization rises → rates rise → discourages borrowing / attracts deposits → utilization falls back. The protocol's interest rate model acts as a structural ceiling on leverage buildup.

**Leverage build vs unwind rates (USD, controlling for denomination):**

- Crash deleveraging: -0.10% to -0.41%/day (median ~-0.27%/day)
- Bull rebuilding: +0.34% to +1.30%/day (median ~+0.41%/day)

Rebuilding is faster than unwinding in daily rate terms. The asymmetry in liquidation volume (20-894× crash vs recovery) coexists with *faster* rebuilding rates. This is because rebuilding adds healthy high-HF positions, while crashes only liquidate the lowest-HF tail. Most positions survive crashes.

### What was not tested

- Decomposition of borrow changes by asset type during crashes (how much is phantom WETH borrowing vs real stablecoin borrowing). DefiLlama data is aggregate — would require subgraph queries.
- Per-position analysis of the 2024_consolidation anomaly: who was adding leverage during a -39% crash, and did they survive?
- Health factor distribution at epoch boundaries.
- Interest rate spikes during crash epochs and their effect on borrow behavior.

### What remains open

- The 2024_consolidation anomaly: a single exogenous crash in a sample of 6 is enough to identify but not enough to characterize. Are there sub-epoch patterns (weekly resolution) that would show when during the crash new borrowing accelerated?
- Does the utilization homeostasis break down under extreme conditions? The 2022_bear_1 is the only case where it broke below 30% — was that because the rate controller parameters were different, or because the crash was uniquely severe (-71%)?
- The crash taxonomy (endogenous vs exogenous) has predictive implications: if a crash is exogenous, expect counter-cyclical leverage building and higher liquidation intensity relative to stored leverage. But classifying crashes as endo/exogenous requires knowing the catalyst in advance.
- Per-position snapshots (Step 3) would decompose the aggregate findings: what fraction of the 2024 borrow increase was phantom expansion vs real directional leverage? How does the HF distribution reshape during and after crashes?

---

## Iteration 5: Synthesis + Review (Step 5)

**Date:** 2026-03-20  
**Document produced:** `findings.md` (263 lines, 8 sections)

### What was done

- Wrote synthesis document consolidating findings from iterations 1-4 across all four measurement layers.
- Verified all key numbers against source data: $1.37B total real liquidation volume, individual epoch volumes, collateral composition percentages, crash/recovery ratios (real category).
- Review discussion identified and verified wstETH collateral composition finding.

### What was found in review

**wstETH users are a distinct population from WETH users, not the same people switching collateral.**

In 2024_consolidation: 134 wstETH-only liquidated users, 1,216 WETH-only users, 22 overlap. wstETH positions are 13.5× larger by median (16.4 wstETH vs 1.2 WETH). wstETH liquidations are more concentrated on spike days (61% on Aug 5 vs 47% for WETH).

This profile — distinct users, larger positions, spike-day concentrated — suggests a separate class of participants who use yield-bearing collateral for larger positions with tighter health factors. They survive gradual bleeds but break on the sharpest price drops.

**The collateral composition shift is structural adoption, not behavioral.**

wstETH grows as real-position collateral because it's strictly better than WETH (earns staking yield on collateral). The adoption curve: 0% (2022) → 33% by volume (2024) → 56% (2025_q4_chop) → 21% (2026_crash). The non-monotonic drop reflects varying size distribution of who gets caught in each crash, not a reversal in adoption.

**Fragility profile is shifting: many-small-WETH → fewer-larger-wstETH.**

Same total risk, different distribution. Each wstETH liquidation is higher-impact. Whether this makes cascades more or less severe is an open question — fewer large events might mean less order book pressure per unit time, or single large position liquidations could move the market more.

**stETH event count inflation is confirmed as dust artifact.**

2,538 stETH "liquidation events" in 2025_q4_chop totaling 11.1 stETH (median 0.002 stETH, ~$6). These are dust farming artifacts. By volume, stETH is <0.1% of that epoch. The high stETH event count (44% of real events) is misleading; the 56% wstETH figure by volume is driven by 33,120 wstETH (~$115M) from only 142 events.

### Corrections identified

- Two clarifications needed in findings.md: (1) wstETH users as distinct population note in section 7, (2) stETH dust artifact warning for count-based metrics.

### What remains open

- All open questions from iteration 4 remain (HF distribution snapshots, 2024 anomaly decomposition, phantom lifecycle, mid-crash leverage builders, liquidator ecosystem).
- The fragility profile shift (many-small → fewer-larger) and its cascade implications are flagged for future work.
- Step 3 (position snapshots) deferred — the aggregate dynamics picture is established. Snapshots would add depth to specific questions (HF distributions, the 2024 anomaly) but are not needed for the overall findings.

---

## Iteration 6: Multi-Exchange OI Coverage (Step 6a)

**Date:** 2026-03-20  
**Script:** `memories/mev/dynamics/multi_exchange_oi.py`  
**Data produced:** `data/bybit_oi_episodes.csv`, `data/bybit_oi_control.csv`, `data/okx_oi_episodes.csv`, `data/okx_oi_control.csv`, `data/6a_results.txt`

### What was tested

- Pulled Bybit ETHUSDT perpetual OI (hourly) for all 17 episode windows (2024-2026) and 3 control months. Full coverage: 7,289 hourly records.
- Pulled OKX ETH-USDT-SWAP OI (hourly). Only ~2 months of hourly history available (from Jan 2026). Covers 1/17 episodes.
- Resampled existing Binance 5-min OI cache to hourly. 7,697 hourly records, all 17 episodes.
- Cross-exchange cascade ordering: which exchange's OI drops first within ±48h of lending peak, at >3% hourly threshold.
- Aggregate OI signal: average of per-exchange % changes. Compared enrichment (episode vs control drop rates) for Binance-only, aggregate-mean, and either-exchange OR gate at multiple thresholds.
- Cross-exchange correlation of hourly OI % changes, overall and during stress.

### What was measured

**OI drops are exchange-specific, not market-wide.**

Measured on contract-denominated OI (ETH/contracts, not USD):
- Binance-Bybit hourly OI % change correlation: 0.495 overall, -0.144 when either drops >1%, 0.073 when either drops >3%.
- When Binance drops >3%: Bybit median change is -0.10% (flat). When Bybit drops >3%: Binance median is -0.09% (flat).
- When either exchange drops >3%: both drop >3% only 2% of the time (2/80 hours). Binance-only: 38% (30/80). Bybit-only: 60% (48/80).
- The conditional median test rules out threshold coarseness — the non-dropping exchange is genuinely flat, not just below threshold.

**Aggregating dilutes the signal.**

Enrichment ratios (episode drop rate / control drop rate) at >3% threshold:
- Binance-only: 4.7x
- Aggregate-mean: 2.3x
- Either-exchange OR gate: 2.5x
- Binance-only dominates at every threshold ≥3%.

At >4% threshold: Binance 3.1x, Aggregate 1.4x, OR 1.7x. Binance-only at >4% produces ~4 false alarms/year.

**Cascade ordering: essentially simultaneous when both fire.**

Only 6/17 episodes had >3% drops on both Binance and Bybit within ±48h of peak. Among these 6:
- Binance leads 4/6 (67%), median lead +1.5h
- 3/6 (50%) simultaneous within 2h
- One outlier: episode 11 (Mar-Apr 2025) with 85h gap — two separate events, not a cascade

5 episodes had drops on only one exchange. 6 episodes had no >3% drop on either.

**OKX has insufficient historical data.** Only ~2 months of hourly OI available. Covers 1/17 episodes. Not useful for this analysis.

### Methodological discovery: USD vs contract OI

The flow phase's OI signal (37h lead, 94% consistency, 15/17 hit rate at >3% threshold) was measured on USD-denominated OI (`sum_open_interest_value`). This analysis used contract-denominated OI (`sum_open_interest`). The difference matters:

- USD OI = contracts × price. During a -5% ETH hour with zero contracts closed, USD OI drops 5% while contract OI is flat.
- Flow phase found >3% Binance USD-OI drops in ~15/17 episodes. This analysis found >3% contract-OI drops in only 7/17 episodes.
- The 8-episode gap represents episodes where price dropped (mechanically reducing USD OI) but no significant perp position closure occurred.

Contract OI is the cleaner metric for detecting actual position changes. USD OI conflates position closure with price movement. The flow phase's 37h lead finding may be partially a price proxy — the "lead" could come from price declining before lending peaks, not from genuine early position closure.

This has not yet been verified. The rerun of perp_lead.py on contract OI is the immediate next step to determine whether the lead time survives on the cleaner metric.

### What was not tested

- The flow phase's core lead analysis (37h, 94% consistency) on contract-denominated OI. This is the critical validation step.
- Funding rate behavior during OI drops (6c) — whether funding rate spikes distinguish forced from voluntary closures.
- 5-min OI velocity profiles — whether forced liquidation cascades produce sharper, more concentrated OI drop shapes than voluntary de-risking.
- Whether the 7 contract-OI episodes correspond to the escalating episodes from the flow phase (the discriminant hypothesis).
- Crash-type conditioning of the OI signal (6b).
- Conjunction test with utilization and VIX (6d).

### What remains open

- Does the 37h lead time and 94% consistency survive when measured on contract OI? If it degrades substantially, the flow phase's OI signal is partially a price proxy and the remaining 6b-6d analyses need to be redesigned around that.
- The exchange-specificity finding implies OI drops are dominated by voluntary de-risking (exchange-specific user behavior) rather than forced liquidation cascades (which would be cross-exchange correlated via the same price trigger). This is strong pre-6c evidence for the voluntary closure hypothesis, but not yet confirmed by funding rate data.
- The 8 episodes where only USD-OI (not contract-OI) drops are detected — are these the non-escalating episodes? If contract OI is the discriminant for episode severity, it may be more valuable than the original USD OI signal despite lower hit rate.
- Bybit shows more single-exchange >3% drops (5 episodes) than Binance (1 episode). Whether Bybit is noisier or captures different events is unknown.
- The control sample is thin (3 months, n=2 control drops at >3%). Enrichment ratios are rank-order reliable (Binance > OR > aggregate at ≥3%) but absolute magnitudes are fragile.

### Connections to prior work

- The exchange-specificity finding connects to the dynamics phase's wstETH/WETH population finding: different venues attract different behavior profiles. Binance's larger, stickier OI base produces a cleaner signal, analogous to how wstETH positions are larger and more concentrated than WETH positions.
- The USD vs contract OI distinction is relevant to the flow phase's entire OI signal chain. All flow phase OI analysis used USD OI. The contract OI metric may reframe what was actually being measured.

---

## Iteration 7: Contract OI Validation + Funding Rate Data (Step 6a validation + 6c prep)

**Date:** 2026-03-20  
**Script:** `memories/mev/dynamics/contract_oi_validation.py`  
**Data produced:** `data/contract_oi_results.txt`, `data/binance_funding_episodes.csv` (919 records), `data/binance_funding_control.csv` (267 records)

### What was tested

- Side-by-side comparison of contract-denominated OI (`sum_open_interest`) vs USD-denominated OI (`sum_open_interest_value`) as a lending liquidation lead indicator. Same methodology as flow phase's `perp_lead.py` (sections A, B, G, H), run on both metrics for direct comparison.
- Discriminant test: do the 7 episodes with >3% contract-OI drops near peak correspond to the more severe episodes?
- Pulled Binance ETHUSDT 8h funding rate data for all 17 episode windows and 3 control months. Computed descriptives near episode peaks.

### What was measured

**Contract OI signal survives on the cleaner metric, with different characteristics than USD OI.**

| Metric | Contract OI | USD OI |
|--------|-------------|--------|
| Hit rate (adaptive threshold) | 17/17 | 17/17 |
| Corrected median lead time | +27h | +37h |
| Corrected consistency (perps lead) | 82% (14/17) | 94% (16/17) |
| Price Δ (OI drop → lending peak) | -7.2% | -10.9% |
| Enrichment at >3% | 7.9x | 3.9x |
| Annual false alarms at >3% | ~2 | ~20 |
| Enrichment at >4% | 5.3x | 6.8x |
| Annual false alarms at >4% | ~1 | ~5 |

These are two different signals, not two measures of the same thing:
- USD OI detects "price is dropping" (fires early via mechanical price effect, high sensitivity, low specificity, ~20 false alarms/year at >3%).
- Contract OI detects "traders are actually closing positions" (fires 10h later, much higher specificity, ~2 false alarms/year at >3%).

The 10h gap between USD and contract OI signals is the reaction time of perp traders to price moves. USD OI fires when price starts declining (mechanical); contract OI fires when traders respond by closing positions (behavioral).

The -7.2% median price decline after contract OI fires confirms this is a genuine early warning: price continues falling after traders start closing, eventually reaching levels that trigger lending liquidations ~27h later.

**Contract OI is a severity discriminant.**

7/17 episodes have >3% contract-OI drops within ±48h of peak lending day. Those 7 vs the other 10:
- Median peak-day liquidation: $73M vs $7M
- Median 7d forward return: -4.4% vs +0.3%
- Mean 7d forward return: -5.8% vs +0.1%
- Mann-Whitney U=19, p=0.067 (one-tailed, drop < no-drop)

The 7 contract-OI episodes (eps 1, 4, 9, 11, 15, 16, 17) are the high-severity episodes. The 10 without are mostly mild (4/10 have positive 7d returns, 6/10 have peak liquidation under $10M).

**This resolves the flow phase's central open question.** The flow phase tested OI as an escalation predictor (iteration 15) and found Fisher's p=0.515 — concluding "OI does not predict escalation." That test used USD OI, which fires for 15/17 episodes (no discriminating power). Contract OI fires for 7/17, precisely the severe episodes. The flow phase's conclusion was drawn from the wrong metric.

**Funding rate confirms forced liquidation in a subset of contract-OI episodes.**

4/17 episodes have significantly negative funding rate (<-0.01%) within ±48h of peak:
- Episode 4 (Yen carry, Aug 2024): min -0.0107%
- Episode 9 (2025 crash, Feb 2025): min -0.0251% (most extreme)
- Episode 15 (Q4 chop, Oct 2025): min -0.0131%
- Episode 17 (2026 crash, Jan 2026): min -0.0164%

All 4 are in the contract-OI-drop group. None of the 10 non-contract-OI episodes have significantly negative funding. This creates a 3-tier structure:
- Tier 1 (4 episodes): Contract OI drop + negative funding → forced liquidation cascade
- Tier 2 (3 episodes: eps 1, 11, 16): Contract OI drop + normal funding → large voluntary de-risking
- Tier 3 (10 episodes): No significant contract OI drop → mild episodes

**Episode 10 defines the structural blind spot.**

Episode 10 (Feb 2025, -20.2% 7d return, $44M peak liquidation) has no >3% contract OI drop and no negative funding. This is the "2025 January mystery" from the links phase — ETH-specific rotation without perp market participation. Lending stress came from direct price decline hitting lending positions, bypassing the perp → lending cascade the OI signal detects. The OI signal structurally cannot detect events where lending stress bypasses the perp layer.

### What was not tested

- Fisher's exact test of contract OI >3% vs the flow phase's actual escalation classification (M1-P97 concentrated spike labels). The discriminant test used peak liquidation USD and 7d returns as severity proxies, not the flow phase's specific escalation/non-escalation labels. The direct retest is the highest-value remaining test.
- 3-tier severity analysis: whether the funding rate sub-partition (forced vs voluntary) predicts severity within the 7 contract-OI episodes.
- 5-min OI velocity profiles: whether forced liquidation episodes (Tier 1) show sharper, more concentrated OI drop shapes than voluntary de-risking episodes (Tier 2).
- Whether the 4 Tier 1 episodes correspond to specific crash types from the links phase (macro vs crypto-native).

### What remains open

- The escalation predictor retest (contract OI vs flow-phase escalation labels) is the single highest-value test remaining. If Fisher's p<0.05, it resolves the flow phase's central open question using nothing but the correct OI metric.
- The 3-tier structure (forced/voluntary/mild) is observed but not yet tested for predictive power. Do Tier 1 episodes have higher peak liquidation and worse forward returns than Tier 2?
- The 5-min velocity profile test would provide a second empirical axis (beyond funding rate) for the forced/voluntary decomposition.
- The original plan items 6b (crash-type conditioning) and 6d (utilization + VIX conjunction) are superseded. 6b is absorbed into the 3-tier analysis. 6d is replaced by the escalation predictor retest — contract OI at >3% already achieves 7.9x enrichment with ~2 false alarms/year, making utilization and VIX overlays marginal.
- Episode 10's blind spot: are there other rotation/rebalancing events in earlier data (pre-2024) where lending stress occurred without perp participation? This would characterize how common the blind spot is.

### Connections to prior work

- Directly reopens and potentially resolves the flow phase iteration 15 finding ("OI does not predict escalation," Fisher's p=0.515). That conclusion was an artifact of using USD OI, which fires too broadly. Contract OI may be the discriminant the flow phase spent 5 iterations failing to find.
- The 3-tier structure connects to the dynamics phase's crash taxonomy (iteration 4): endogenous crashes (participants deleverage) map to Tiers 1-2, while the exogenous Yen carry crash (ep 4) is Tier 1. Episode 10 (rotation without perp stress) is a new category not in the original taxonomy.
- The funding rate finding connects to the 6a exchange-specificity result: OI drops being exchange-specific (not cross-exchange correlated) is consistent with voluntary de-risking dominating. The 4 episodes with negative funding are the exceptions where forced liquidation cascades actually occurred.

---

## Iteration 8: Escalation Predictor + 3-Tier Severity + Velocity Profiles (Step 6 completion)

**Date:** 2026-03-20  
**Script:** `memories/mev/dynamics/escalation_test.py`  
**Data produced:** `data/escalation_results.txt`

### What was tested

- Fisher's exact test of contract OI >3% vs the flow phase's M1-P97 escalation classification (episodes containing both distributed and concentrated spike days).
- Same test on USD OI for direct comparison, reproducing the flow phase's p=0.515 result.
- 3-tier severity analysis: Tier 1 (contract OI drop + negative funding), Tier 2 (contract OI drop + normal funding), Tier 3 (no contract OI drop). Kruskal-Wallis across tiers on peak liquidation USD and 7d forward return.
- Mann-Whitney between Tier 1 and Tier 2 on 7d forward return.
- 5-min OI velocity profiles for the 7 contract-OI episodes: 30-minute concentration of OI drops, classified as sharp cascade (>50% in 30min) vs gradual decline.

### What was measured

**Contract OI >3% predicts escalation: Fisher's p=0.0345.**

Contingency table (contract OI, 17 episodes with OI data):

|                    | Escalated | Not escalated | Total |
|--------------------|-----------|---------------|-------|
| Contract OI >3%    |         7 |             0 |     7 |
| No contract OI >3% |         4 |             6 |    10 |
| Total              |        11 |             6 |    17 |

Fisher's exact: odds ratio=∞, p=0.0345. All 7 episodes with contract-OI drops escalated (100%). Episodes without contract-OI drops escalated only 40% of the time (4/10).

USD OI comparison: fires for 16/17 episodes. Fisher's p=1.0000. No discriminating power whatsoever.

The flow phase's iteration 15 conclusion ("OI does not predict escalation," p=0.515) was entirely an artifact of using USD-denominated OI, which fires for nearly every episode due to mechanical price contamination.

**The escalation label is coarser than the signal.**

11/17 episodes are classified as "escalated" by M1-P97. This includes episodes 5 (7d return -0.5%, peak $18M) and 8 (7d return +2.5%, peak $7M), which are mild by every outcome metric despite containing a single concentrated spike day. The 4 episodes in the "no OI drop but escalated" cell (eps 3, 5, 8, 10) have median peak liquidation $18M — intermediate between the contract-OI group ($73M) and the non-escalated group ($3M). The contract OI signal identifies the subset of escalated episodes that are both escalated AND severe. Two of the four "false negatives" are episodes that technically escalated but were not dangerous.

**3-tier severity validated on peak liquidation: Kruskal-Wallis p=0.007.**

| Metric | Tier 1 (forced, n=4) | Tier 2 (voluntary, n=3) | Tier 3 (mild, n=10) |
|--------|---------------------|------------------------|---------------------|
| Median peak liq USD | $122M | $35M | $7M |
| Mean peak liq USD | $116M | $69M | $12M |
| Median 7d fwd return | -5.9% | -4.4% | +0.3% |
| Median OI worst drop | -5.3% | -3.9% | -2.3% |

Kruskal-Wallis on peak liquidation: H=9.92, p=0.007 (highly significant separation by tier).
Kruskal-Wallis on 7d forward return: H=2.47, p=0.291 (not significant).
Mann-Whitney Tier 1 vs Tier 2 on 7d return: U=6, p=0.571 (not significant, n=4 vs 3).

The tiers separate on how much liquidation occurs (mechanism) but not on how bad the forward return is (outcome). Tier 2 includes episode 11 (-13.3% fwd return), worse than most Tier 1 episodes. Tier 3 includes episode 10 (-20.2%), the worst of all. Forward return depends on factors beyond the perp-lending cascade — macro context, price trajectory, leverage recharge state.

**Velocity profiles: directionally correct, small n.**

| Ep | Tier | 30m concentration | Profile |
|----|------|-------------------|---------|
| 4 | T1 (forced) | 65% | sharp cascade |
| 15 | T1 (forced) | 96% | sharp cascade |
| 17 | T1 (forced) | 72% | sharp cascade |
| 9 | T1 (forced) | 20% | gradual decline |
| 16 | T2 (voluntary) | 69% | sharp cascade |
| 1 | T2 (voluntary) | 15% | gradual decline |
| 11 | T2 (voluntary) | 1% | gradual decline |

Tier 1 median 30m concentration: 69%. Tier 2 median: 15%. Tier 1 has 3/4 sharp cascades; Tier 2 has 1/3.

Exceptions: Episode 9 (Tier 1, most extreme negative funding at -0.0251%) shows a gradual decline (20% concentration) — sustained forced liquidation over hours, not a single burst. Episode 16 (Tier 2, normal funding) shows a sharp cascade (69%) — a large voluntary position closing quickly resembles a forced cascade. Velocity profile and funding rate measure overlapping but not identical phenomena.

### What was not tested

- Whether the velocity profile pattern holds on larger n (requires more episodes over time).
- Whether combining contract OI with leverage state (recharge model from iteration 3) or macro context (VIX/crash taxonomy from links phase) improves outcome prediction beyond mechanism detection.
- Whether the intermediate group (4 escalated episodes without OI drops, $18M median) has a different detectable precursor.
- Whether the Tier 1 (forced) episodes correspond to specific crash types from the links phase. The 4 episodes are: ep 4 (macro/Yen carry), ep 9 (rotation→macro), ep 15 (crypto-native/Q4 chop), ep 17 (crypto-native/2026 crash). No clean pattern by crash type — forced cascades occur in both macro and crypto-native contexts.

### What remains open

- The 3-tier structure classifies mechanism, not outcome. Predicting outcome (how far price falls) requires mechanism × leverage state × macro context. Each factor was explored in a different phase; cross-phase synthesis is where the full picture would emerge.
- The flow phase's conclusion that "the escalation question is fundamentally a topology question requiring position-level data" (iteration 16) needs qualification. Price proximity to large liquidation walls determines WHETHER an episode will escalate (pre-condition). Contract OI detects that escalation HAS started (concurrent indicator with 27h lead). These are different questions. The topology conclusion about pre-condition prediction is compatible with contract OI as a concurrent detector.
- Episode 10 (lending stress bypassing the perp layer) represents a structural blind spot. How common is this class of event? Only 1/17 in the 2024-2026 sample.
- The enrichment ratio (7.9x at >3%) and false alarm rate (~2/year) are measured on a small control sample (3 months, n≈2 control drops). Rank ordering (Binance > aggregate) is robust but absolute magnitudes are fragile.

### Connections to prior work

- Resolves the flow phase iteration 15 finding. The escalation predictor works — it was tested on the wrong metric (USD OI instead of contract OI).
- The mechanism vs outcome distinction connects to the dynamics phase's leverage recharge model (iteration 3): the recharge state determines whether a given mechanism (forced cascade vs voluntary de-risking) produces a self-reinforcing feedback loop or a self-limiting spike. Contract OI detects the mechanism; recharge state modulates the outcome.
- The 3-tier structure refines the flow phase's "perp → lending cascade" model: not all OI drops are cascades. Only Tier 1 (forced, 4/17 episodes) represents the full cascade mechanism. Tier 2 (voluntary, 3/17) represents coordinated de-risking without forced liquidation. Tier 3 (10/17) represents episodes where the perp layer is uninvolved.
- The velocity profile exceptions (ep 9 gradual despite forced, ep 16 sharp despite voluntary) demonstrate that forced liquidation ≠ rapid liquidation and voluntary ≠ gradual. These are two orthogonal axes: speed of closure and voluntariness of closure.
