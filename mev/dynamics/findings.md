# Dynamics — Findings

## 1. Summary

The DeFi leverage system on Ethereum operates as two structurally independent systems that share the same protocol infrastructure but respond to completely different forces. The phantom system — $5.6B in LST/WETH loops — is functionally immune to ETH/USD price crashes. In 4.2 years and six crash epochs totaling -290% cumulative drawdown, phantom positions produced 161 liquidation events (0.2% of all liquidations), 22 of which came from a single oracle misconfiguration on March 10, 2026. The real system — ETH-like collateral against stablecoin debt — produced $1.37B in liquidation volume across 38,055 events, concentrated into a handful of spike days that account for 45-89% of each epoch's total volume.

Real positions follow a recharge cycle: crashes deplete leverage, bull markets rebuild it with largely fresh participants (5-57% user overlap depending on rebuild time), and the next crash releases the stored energy. The intensity of each crash depends more on how much leverage accumulated beforehand than on the crash magnitude itself — a -39% crash (2024 yen carry) produced 25× more real liquidation volume ($302M) than a -42% crash (2022 FTX, $12M) because the system had 475 days to reload. The recharge model is directionally correct but quantitatively weak (r=0.47 for borrowed×crash_depth), limited by a sample of 6 crashes and confounded by crash catalyst type.

Exchange flows at daily resolution carry no signal for price direction (max |r| < 0.04 at all lags). The measured flow component (CoinMetrics flow_in/flow_out) diverges substantially from actual reserve balance changes, implying that unmeasured mechanisms (staking, bridges, contract interactions) dominate exchange balance movements. Protocol-level utilization is self-regulating, gravitating to 38-42% post-2022 through the interest rate controller's feedback loop.

## 2. The Two Systems

### Phantom positions: structurally crash-immune

The position phase identified $5.6B in phantom positions (LST collateral / WETH debt). The dynamics data confirms these do not participate in market-cycle dynamics.

**Evidence: 161 phantom liquidations out of 65,382 total (0.25%).**

| Collateral → Debt | Events | Context |
|---|---|---|
| stETH → WETH | 108 | Mostly Aave v2, spread across 4 years |
| wstETH → WETH | 47 | Aave v3, includes 22 from March 10 incident |
| weETH → WETH | 3 | |
| rETH → WETH | 2 | |
| cbETH → WETH | 1 | |

The mechanism: Aave's CAPO oracle reads protocol-level exchange rates (e.g., `getPooledEthByShares(1e18)` for wstETH), not DEX market prices. Protocol exchange rates only increase over time (staking yield accrual). An ETH/USD crash changes both sides of the phantom health factor equation equally — collateral and debt are both ETH-denominated — so the health factor is invariant to ETH/USD moves.

**The March 10 incident is the only meaningful phantom liquidation event.** Chaos Labs pushed a stale `snapshotRatio` to the CAPO adapter, causing 2.85% artificial underpricing of wstETH. This triggered 49 liquidation events in 84 seconds (22 phantom, 27 other), seizing 8,609 wstETH (~$20M). The $1.42B whale survived by a 0.98% margin. This was documented in the correlation phase; the dynamics data independently confirms it as the sole demonstrated trigger for phantom liquidation.

Excluding March 10: **139 organic phantom liquidations in 4.2 years** (~33/year), compared to ~15,500 real+other liquidations/year. The phantom wall is not a source of crash risk — it is a source of oracle operational risk.

### Real positions: the market-cycle system

The remaining 65,221 events (99.75%) are real directional positions (ETH-like or altcoin collateral against stablecoin debt) and various other combinations (stablecoin-on-stablecoin, short-ETH, etc.).

Category breakdown of all 65,382 events:
- Real (ETH-like → stablecoin): 38,055 (58.2%) — $1.37B in liquidation volume
- Other (altcoin → stablecoin, shorts, misc): 27,166 (41.5%) — $1.10B
- Phantom (LST → WETH): 161 (0.2%) — negligible volume

The "other" category includes LINK→USDC, WBTC→USDT, AAVE→DAI, and similar altcoin directional positions. These carry the same risk structure as "real" (collateral drops, debt fixed) but are not ETH-exposed. The dynamics analysis focuses on the "real" category to isolate ETH-linked leverage.

## 3. The Recharge Cycle

### Intensity depends on stored leverage, not crash magnitude

| Crash Epoch | Price Δ | Real Liq Volume | Intensity ($/1%) | Rebuild Time |
|---|---|---|---|---|
| 2022_bear_1 | -71% | $229M | $322M/1% | — (first epoch) |
| 2022_bear_2 (FTX) | -42% | $12M | $29M/1% | 56 days |
| 2024_consolidation (Yen) | -39% | $302M | $774M/1% | 475 days |
| 2025_crash | -61% | $315M | $518M/1% | 131 days |
| 2025_q4_chop | -39% | $217M | $558M/1% | 136 days |
| 2026_crash | -34% | $193M | $568M/1% | 0 days (continuous) |

Intensity per 1% of price decline varies 26× across epochs. The lowest (FTX, $29M/1%) came after 2022_bear_1 had already depleted the system 56 days earlier. The highest (Yen carry, $774M/1%) came after 475 days of bull market leverage accumulation. Similar ~40% crashes produce anywhere from $12M to $302M in liquidation volume depending on the pre-crash state.

### User overlap confirms participant turnover

| Prior → Next Crash | Rebuild Time | User Overlap |
|---|---|---|
| 2022_bear_1 → 2022_bear_2 | 56 days | 55.7% (414/743) |
| 2022_bear_2 → 2024_consolidation | 475 days | 5.1% (74/1,447) |
| 2024_consolidation → 2025_crash | 131 days | 15.2% (632/4,162) |
| 2025_crash → 2025_q4_chop | 136 days | 20.7% (894/4,325) |
| 2025_q4_chop → 2026_crash | 0 days | 16.9% (414/2,456) |

After a 475-day bull, 95% of liquidated users are new participants. After only 56 days, 56% are the same addresses being liquidated again (mostly dust positions). The leverage supply replenishes proportional to rally magnitude × rebuild time, bringing in fresh capital that has not experienced the prior crash.

### Temporal concentration: liquidation is a spike phenomenon

| Crash Epoch | Total Real Vol | Spike Days (>2σ) | Top 3 Days % | Days to First >$10M |
|---|---|---|---|---|
| 2022_bear_1 | $229M | 6 | 46% | 20 |
| 2022_bear_2 | $12M | 2 | 89% | never |
| 2024_consolidation | $302M | 1 | 77% | 8 |
| 2025_crash | $315M | 5 | 52% | 49 |
| 2025_q4_chop | $217M | 5 | 75% | 31 |
| 2026_crash | $193M | 3 | 87% | 45 |

In every crash epoch, 3 days account for 45-89% of total real liquidation volume. Aug 5, 2024 alone produced $187M — 62% of the entire 2024_consolidation epoch. Spike days cluster around -8% to -18% daily price moves. Between spikes, liquidation volume is minimal.

Spike onset timing varies by crash type. Sudden external shocks (yen carry: 8 days) spike early. Slow-burn crashes (2025_crash: 49 days; 2026_crash: 45 days) bleed gradually before late-stage capitulation.

### Crash/recovery asymmetry

| Crash → Recovery | Crash Real Vol | Recovery Real Vol | Ratio |
|---|---|---|---|
| 2022_bear_1 → 2022_rally | $229M | $6M | 36× |
| 2024_consolidation → 2024_bull | $302M | $35M | 9× |
| 2025_crash → 2025_recovery | $315M | $22M | 14× |
| 2025_q4_chop → 2026_crash | (continuous) | — | — |
| 2026_crash → 2026_recovery | $193M | $1M | 203× |

Crash epochs produce 9-203× more real liquidation volume than subsequent recoveries. The system deleverages in hours (spike days) and rebuilds over months. The 2022_bear_2→2023_recovery pair is inverted (0.4×) because the FTX crash produced anomalously low volume ($12M) from a depleted system.

### Aggregate borrow as predictor

Pre-crash total Aave borrowed (USD) alone weakly correlates with real liquidation volume (r=0.29, n=6). The interaction term `borrowed_start × |crash_depth|` is directionally better (r=0.47) but not statistically reliable with 6 data points. Pre-crash utilization is slightly informative (r=0.59).

The recharge model is qualitatively correct — depleted systems produce low liquidation, fully reloaded systems produce high liquidation — but aggregate borrow level is not a clean quantitative predictor. The confound is crash type: endogenous vs exogenous crashes interact differently with the same leverage level (§4).

## 4. Crash Taxonomy

### Endogenous vs exogenous (conjectured, n=1 exogenous)

USD-denominated borrowing changes during crashes reveal two distinct patterns:

**Endogenous crashes** (5 of 6: Terra/3AC, FTX, 2025_crash, 2025_q4_chop, 2026_crash):
- Participants deleverage. USD borrow declines 22-69%.
- Utilization drops or stays flat (-0.1 to -10.3pp).
- Liquidation volume proportional to stored leverage.

**Exogenous crash** (1 of 6: 2024_consolidation / Yen carry):
- Participants increase leverage. USD borrow grew +15.3% during a -39% crash.
- Utilization jumped +5.7pp (33.0% → 38.7%).
- Liquidation intensity was highest of any epoch ($774M/1%) — liquidation from speed of price drop + fresh leverage being added mid-crash.

The ETH-denominated borrow metric initially appeared to show leverage increasing in all crashes. This is a denomination artifact: when ETH price drops 50%, the ETH-equivalent of constant USD debt doubles. Comparing actual ETH-borrow change to the mechanical (price-only) expectation, the residual is negative in 5 of 6 cases — confirming real deleveraging. Only 2024_consolidation has a positive residual (+25%).

| Epoch | Mechanical ETH Δ (price-only) | Actual ETH Δ | Residual |
|---|---|---|---|
| 2022_bear_1 | +247% | +7% | -240% |
| 2022_bear_2 | +73% | +31% | -42% |
| 2024_consolidation | +64% | +89% | **+25%** |
| 2025_crash | +155% | +69% | -86% |
| 2025_q4_chop | +63% | +19% | -45% |
| 2026_crash | +51% | +18% | -33% |

**This taxonomy is conjectured from 1 exogenous case in 6.** The pattern is consistent and mechanically intuitive (external shock → DeFi participants buy the dip → counter-cyclical leverage), but it requires more exogenous crash samples to confirm. The predictive implication — if a crash is exogenous, expect higher liquidation intensity relative to stored leverage — requires classifying the catalyst, which is only known after the fact.

## 5. Protocol Self-Regulation

### Utilization homeostasis: 38-42% post-2022

| Epoch | Regime | Util Start | Util End | Δ |
|---|---|---|---|---|
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

Post-2022, utilization stays in a narrow 33-43% band. Average crash Δ = -0.9pp, average bull Δ = +1.1pp — nearly symmetric. The 2022_bear_1 was the only epoch to break below 30%. The rate controller provides negative feedback: utilization rises → rates rise → discourages borrowing / attracts deposits → utilization falls back. This acts as a structural ceiling on leverage buildup, preventing the system from reaching the extreme utilization levels that would amplify crashes.

### Leverage build vs unwind rates

- Crash deleveraging (USD borrow change/day): -0.10% to -0.41%/day (median ~-0.27%/day)
- Bull rebuilding: +0.34% to +1.30%/day (median ~+0.41%/day)

Rebuilding is faster than unwinding in daily rate terms. This coexists with the 9-203× crash/recovery asymmetry in liquidation volume because rebuilding adds healthy high-HF positions, while crashes only liquidate the lowest-HF tail. Most positions survive crashes — the system's total borrow drops 22-69% in USD during crashes, but this is from voluntary deleveraging plus liquidation of the vulnerable margin, not from liquidation alone.

### Protocol growth context

Aave Ethereum grew 4× in real terms over this period:
- Jan 2022: $8.5B TVL, $6.0B borrowed (v2 only)
- Peak Aug 2025: $32.8B TVL, $24.4B borrowed (mostly v3)
- Mar 2026: $20.4B TVL, $13.3B borrowed
- ETH-denominated borrow: 1.6M ETH (2022) → 6.1M ETH (2026), 3.8× real growth

The rising intensity floor — post-2024, even mild crashes trigger >$190M in real liquidation volume — reflects this protocol growth, not a change in market structure.

## 6. What Exchange Flows Don't Tell You

### Null signal at daily resolution

Net exchange flows (CoinMetrics flow_in/flow_out) and daily reserve changes (sply_ex_ntv) both show no correlation with daily ETH price returns at any lag from -5 to +5 days. Maximum |r| = 0.044 for reserve changes, 0.036 for net flows. Neither leads, lags, nor coincides with price.

Within-epoch correlations are also weak (max |r| = 0.17). The flow data has no short-term predictive or contemporaneous value for price at daily resolution.

### The measurement gap

Measured flow components diverge substantially from actual reserve balance changes:
- 2025_crash: measured net outflow +1.58M ETH, reserves *increased* +3.96M. ~5.5M discrepancy.
- 2025_q4_chop: measured net outflow +4.65M, reserves *decreased* -4.2M. ~8.9M discrepancy in opposite direction.

Unmeasured mechanisms (staking contract interactions, bridge activity, internal exchange wallet rebalancing) dominate balance movements. The CoinMetrics methodology captures a minority of actual reserve changes.

### FTX as structural control

Every crash epoch shows exchange reserve increases except 2022_bear_2 (FTX), where reserves dropped by 1.34M ETH — FTX's own reserves vanished. This confirms that reserve data partly reflects exchange solvency events, not purely user behavior.

## 7. Connections to Prior Phases

### Position phase → Dynamics

The position phase mapped the $5.6B phantom wall and developed the real/phantom decomposition. Dynamics confirms the decomposition's predictive value: the phantom wall is structurally crash-immune (161/65,382 events). The "apparent $4.3B liquidation wall at 4-5% below current price" identified by the position phase is >99.99% phantom — dynamics data shows these positions don't liquidate during crashes of any observed magnitude (up to -71%).

The position phase's "conditional fuel map" concept — that topology predicts cascade severity, not occurrence — is consistent with the recharge model: the fuel (stored leverage) determines crash intensity, the spark (price drop) determines whether it ignites.

### Correlation phase → Dynamics

The correlation phase identified the CAPO oracle architecture and forensically analyzed the March 10 incident. Dynamics data independently confirms March 10 as the sole demonstrated trigger for phantom liquidation: 22 of 161 phantom events (14%) occurred in a single 84-second window from one oracle misconfiguration. The remaining 139 organic phantom events over 4.2 years are noise.

The correlation phase concluded that DEX market depegs do not affect Aave oracle pricing (protocol rates only). Dynamics validates this: despite multiple crash epochs where LST DEX prices would have temporarily deviated from protocol rates, no corresponding phantom liquidation spikes appear.

### Flow phase → Dynamics

The flow phase classified liquidation episodes and developed the concentration ratio methodology used to define epoch boundaries. The dynamics epoch analysis uses the same episode framework.

The flow phase's WETH-only liquidation pull found 27,702 events. The full dynamics pull found 65,382 events (2.36× more), expanding coverage to all collateral types. WETH's 49.1% share by event count matches the original pull's capture rate.

### Collateral composition shift

A finding that bridges the position and dynamics phases: the collateral base of real liquidations is shifting.

| Epoch | WETH % | wstETH % | other LST % |
|---|---|---|---|
| 2022_bear_1 | 97% | 0% | 0% |
| 2024_consolidation | 64% | 33% | 1% |
| 2025_q4_chop | 44% | 56% | 1% |
| 2026_crash | 78% | 21% | 1% |

wstETH rose from 0% to as high as 56% of real liquidation collateral (by USD volume in 2025_q4_chop). This reflects LST adoption: users increasingly post wstETH rather than WETH as collateral for stablecoin borrows. These are real positions (wstETH→USDC), not phantom loops — the collateral is yield-bearing ETH, but the debt is still stablecoins. The system's collateral mix is evolving even as its risk structure (ETH/USD exposure) stays the same.

wstETH and WETH users are largely distinct populations. In 2024_consolidation, 134 users were liquidated on wstETH-only positions, 1,216 on WETH-only, with just 22 overlap. wstETH positions are substantially larger (13.5× median size) and more concentrated on spike days (61% of wstETH volume on Aug 5 vs 47% for WETH). This profile — distinct users, larger positions, spike-concentrated — suggests a separate class of participants using yield-bearing collateral for larger positions with tighter health factors. As wstETH adoption continues, the liquidation distribution shifts from many small WETH events to fewer, larger wstETH events — same total risk, different fragility profile.

Note on stETH event counts: stETH appears as 44% of real liquidation events by count in some epochs, but this is a dust artifact. In 2025_q4_chop, 2,538 stETH events totaled just 11.1 stETH (~$33K) with a median of 0.002 stETH (~$6). By USD volume, stETH is <0.1% of that epoch. All composition percentages in this document use USD volume, not event counts.

## 8. Open Questions

### Position snapshots for HF distribution

**What:** Query Aave v3 subgraph at epoch start, mid, and end blocks to get health factor distributions, real vs phantom split, and concentration metrics at each point.

**Why:** The recharge model currently uses aggregate borrow as a proxy for stored leverage. HF distributions would show *where* the leverage sits — tightly clustered near liquidation threshold (fragile) or spread across high HF values (resilient). Two systems with the same total borrow but different HF distributions would produce very different liquidation volumes from the same crash.

**What would answer it:** 3 snapshots × 11 epochs = 33 subgraph queries, reusing the position scanner from the position phase. Compare HF distribution shape (kurtosis, tail concentration) across pre-crash states and test whether tail concentration predicts liquidation intensity better than aggregate borrow.

### 2024 consolidation anomaly decomposition

**What:** The only epoch where borrowing increased during a crash. Who was adding leverage during a -39% drawdown? Were they new entrants or existing positions increasing exposure? Did the new leverage survive the crash or get liquidated?

**Why:** This is the only clearly exogenous crash in the sample. Understanding who adds counter-cyclical leverage and whether they profit would characterize a potentially distinct market behavior mode. If counter-cyclical leveragers systematically survive, they represent informed flow; if they get liquidated, they represent naive dip-buying.

**What would answer it:** Filter `liquidations_full.csv` for 2024_consolidation epoch. Cross-reference liquidated users against position creation timestamps (from subgraph events). Compare users whose positions were created *during* the drawdown vs before it.

### Phantom position lifecycle

**What:** When do LST loops open and close? Do they open during bulls (when staking yield > borrow cost) and close during rate inversions? Or are they relatively static?

**Why:** The $5.6B phantom wall is crash-immune, but it's not eternal. Understanding the open/close dynamics would indicate whether the wall is growing or shrinking and what triggers structural shifts.

**What would answer it:** Position snapshots at monthly resolution over 2023-2026, tracking individual phantom positions (identified by collateral=LST, debt=WETH). Compute net phantom position creation/destruction rate per period, correlated with borrow rate spreads (wstETH staking yield minus WETH borrow rate from Aave).

### Per-position analysis of mid-crash leverage builders

**What:** In crash epochs, some users add new positions. How large are these positions, how long do they survive, and do they contribute to liquidation volume?

**Why:** The aggregate data shows crashes produce deleveraging (negative residual in 5/6 epochs), but the 2024_consolidation anomaly proves some participants build leverage mid-crash. The question is whether this is confined to one exogenous case or whether it happens in every crash at a smaller scale.

**What would answer it:** Aave v3 subgraph events (supply/borrow events) filtered by crash epoch block ranges. Match new position creation events against subsequent liquidation events for the same user. Compute survival rate and average survival time of positions created during crashes.

### Liquidator ecosystem structure

**What:** 570 unique liquidators for 65,382 events, with extreme concentration (top 10 handle 48.4%). How has the liquidator ecosystem evolved? Do the same bots persist across years, or is there turnover?

**Why:** Liquidator efficiency affects how quickly cascade potential converts to actual selling pressure. If a small number of bots handle most liquidations, their infrastructure reliability and capital constraints become system-level risk factors.

**What would answer it:** Per-epoch liquidator concentration metrics from the existing `liquidations_full.csv`. Track top-10 liquidator persistence across epochs. Measure time-to-liquidation (block delay from HF breach to liquidation event) across epochs to test whether liquidator efficiency has improved.
