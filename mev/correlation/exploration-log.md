# Correlation-Cascade Investigation — Exploration Log

## Iteration 1: DEX Liquidity Depth Probe + Oracle Gate Assessment

**Date:** 2026-03-20

### What was tested

**Step 1: DEX Liquidity Depth per LST**

Used Paraswap aggregator API to simulate sells of increasing sizes (10–100,000 ETH-equivalent) for 7 LST tokens against WETH. Paraswap routes through all available DEX liquidity (Uniswap V3, Curve, Balancer, SushiSwap, etc.) simultaneously. Adaptive bisection refinement used to locate exact liquidity cliff boundaries.

Tokens probed: weETH, osETH, rsETH, wstETH, rETH, cbETH, ETHx.

ETH price at time of probe: $2,136.

### What was found

**Measured: DEX liquidity cliff structure**

| Token | Cliff Edge (sell volume) | DEX Capacity | Cliff Behavior |
|-------|-------------------------|-------------|----------------|
| ETHx | ~10 ETH ($21K) | $21K | NO ROUTE beyond 10 ETH. Only PancakeswapV3+UniswapV3 at minimum size. |
| cbETH | ~200 ETH ($427K) | $390K | 0.26% depeg at 100 ETH → 8.78% at 200 ETH → NO ROUTE at 225 ETH. |
| osETH | ~100–500 ETH ($214K–$1.07M) | $976K | 0.12% depeg at 100 ETH → 9.33% at 500 ETH → NO ROUTE at 562 ETH. |
| rETH | ~100–500 ETH ($214K–$1.07M) | $1.0M | 0.08% depeg at 100 ETH → 5.0% at 500 ETH → NO ROUTE at 562 ETH. |
| rsETH | ~950 ETH ($2.03M) | $2.0M | 0.44% depeg at 950 ETH → NO ROUTE at 969 ETH (19 ETH past last quotable point). |
| wstETH | ~2000–2750 ETH ($4.3M–$5.9M) | $5.7M | 0.09% depeg at 2000 ETH → 7.63% at 2750 ETH (84x impact increase from 37% more volume). |
| weETH | ~5000–7500 ETH ($10.7M–$16M) | $13.9M | 0.50% depeg at 5000 ETH → 13.35% at 7500 ETH. |

Key structural finding: liquidity exhibits **phase-transition behavior**, not smooth degradation. Below the cliff edge, AMM math applies with minimal impact. Above it, liquidity ceases to exist (Paraswap returns NO ROUTE at ~33% price impact). There is no gradual degradation zone. Risk models assuming smooth price impact functions are structurally wrong for these assets.

**Measured: DEX routing fragmentation**

Small sells route through Uniswap V3 concentrated liquidity. Larger sells add Curve pools. At the limit, the aggregator scrapes SushiSwap, UniswapV2, and token-specific unwrap paths (e.g., wstETH→stETH→Curve). No single deep pool backs any LST — depth comes from aggregating multiple thin pools.

**Measured: Cascade ratios (phantom exposure / trigger cost)**

| Token | $ to 2% depeg | Phantom Exposure (from position phase) | Cascade Ratio |
|-------|--------------|---------------------------------------|---------------|
| ETHx | exhausted <1% | $100M | ~4,681x (at exhaust) |
| osETH | ~$388K | $332M | ~856x |
| cbETH | ~$260K | $150M | ~583x |
| rsETH | exhausted <0.5% | $880M | ~434x (at exhaust) |
| rETH | ~$547K | $200M | ~366x |
| wstETH | ~$4.7M | $1,700M | ~363x |
| weETH | ~$11.3M | $230M | ~20x |

Caveat on cascade ratios: these compare notional phantom exposure to instantaneous DEX depth. The numerator is positions that *would* become liquidatable at that depeg level. The denominator is single-block absorptive capacity. They are not directly commensurable — useful for relative ordering and scale, not as a precise cascade multiplier.

**Measured: Phantom position activation thresholds (from position phase data)**

Cross-referenced Step 1 depth data against phantom position HF distribution:

- weETH: $230M activates at <1% depeg, $315M at 1-2%, $328M at 2-3%, $903M at 3-5%
- osETH: $332M concentrated at 2-3% depeg
- rsETH: $141M at 2-3%, $616M at 3-5%
- wstETH: $1,452M at 3-5% depeg (largest single bucket)

### Oracle gate — assessed via CAPO incident

**Found (from sage's research):** On March 10, 2026, Aave experienced a CAPO oracle misconfiguration that artificially depressed the reported wstETH/ETH exchange rate by ~2.85%. This liquidated 34 E-Mode wstETH/WETH loop positions for ~$26M in liquidation volume. No bad debt accrued.

**Established:** The cascade path from depeg → oracle → liquidation is not theoretical. It was demonstrated. The positions liquidated were exactly the "phantom" positions identified in the position topology phase.

**Found: CAPO asymmetry.** CAPO caps upward price growth (9.68%/year for wstETH/ETH) but imposes no limit in the downward direction. Market-driven depegs flow directly through to HF calculations. Additionally, upward recovery is rate-limited (3% every 3 days for the snapshot ratio parameter), creating a directional asymmetry: instant down, slow up.

**Not yet determined:** Whether the CAPO upward rate-limit applies to live-market depeg recovery scenarios (vs. only to the snapshot ratio parameter that was misconfigured on March 10). The exact composition of each LST's CAPO price feed — which component carries the Chainlink market price and which is the rate-limited protocol rate — has not been traced on-chain.

### Structural observations (conjectured, not measured)

**Reflexive liquidity trap:** The yield from LST-loop strategies (deposit wstETH, borrow WETH, buy more wstETH) exceeds what LPs earn providing LST/ETH liquidity on DEXes. Rational capital therefore drains DEX pools to enter lending protocols. The same capital flow that creates phantom exposure simultaneously destroys the DEX liquidity that would absorb its unwinding. This predicts DEX liquidity for an LST should be inversely correlated with its phantom exposure ratio — suggestive in the 7-token dataset but not statistically testable at this sample size.

**Recovery-suppression loop (conjectured):** If the CAPO upward rate-limit applies to recovery from real market depegs, then: market recovers → oracle stuck showing depressed price → "stale" liquidations fire on positions not actually underwater → seized collateral sold on DEX → pushes price back down → market tries to heal again. A second feedback loop operating on a slower timescale (days) than the primary cascade loop (minutes). Whether this mechanism actually applies to live-market depegs depends on the CAPO composition trace (not yet performed).

### What remains untested

1. **Chainlink feed parameters per LST** — heartbeat, deviation threshold for each constituent feed in the CAPO composition. Determines the time constant of the cascade feedback loop.

2. **CAPO composition trace** — for wstETH, weETH, osETH: query Aave oracle contracts to trace the full price composition end-to-end. Which component is the Chainlink market feed? Which is the protocol rate? Which is rate-limited? How does a DEX depeg map onto the reported price?

3. **March 10 liquidation forensics** — pull LiquidationCall events from Aave v3 around March 10. Cross-reference with phantom position snapshots: do any of the 34 accounts overlap with identified mega-whales? Where did seized collateral get sold? What HF margin saved the survivors?

4. **Historical depeg magnitudes (Step 2)** — what LST/ETH depegs have actually occurred during stress events? June 2022 stETH depeg (~7%) was pre-Merge/pre-CAPO. Post-Merge depeg magnitudes for any LST are not yet measured.

5. **Withdrawal queue dynamics** — redemption latency for each LST under stress conditions. Determines whether the DEX cliff is the true floor or has a slow-acting shock absorber (response time: days vs. cascade dynamics: hours).

6. **Liquidation bot routing** — do bots sell seized LST collateral through DEX (deepening depeg) or CEX/OTC (absorbing without DEX impact)? March 10 transaction data would reveal this.

### Data produced

- `data/lst_liquidity_depth.csv` — 133 rows: token, sell amount, fair rate, effective rate, depeg %, ETH received, DEX route
- `data/lst_depth_summary.csv` — per-token summary: capacity, depeg thresholds, phantom exposure, cascade ratio
- `data/1_results.txt` — narrative summary of Step 1 findings
- `depth_probe.py` — Paraswap-based liquidity depth probe script

### Question evolution

Started: "What depeg magnitude in LST/ETH triggers cascade activation for the $5.6B phantom wall?"

After iteration 1: "Does any self-correcting mechanism operate faster than the cascade feedback loop?" The trigger magnitudes are measured (single-digit millions for wstETH, sub-million for Tier 3). The mechanism is demonstrated (CAPO incident). The open question is whether the loop is self-sustaining or self-limiting — determined by Chainlink update speed vs. withdrawal queue / CEX routing / JIT liquidity response times.

---

## Iteration 2: CAPO Incident Forensics + Oracle Composition Trace

**Date:** 2026-03-20

### What was tested

**Task A: March 10 CAPO Liquidation Forensics**

Pulled all `LiquidationCall` events from Aave v3 Core and Prime pools around March 10, 2026 (blocks 24626850–24626910). Cross-referenced liquidated accounts against our phantom position snapshot (`positions_decomposed.csv`). Computed survival margins for mega-whale positions.

**Task B: Oracle Composition Trace**

Queried Aave oracle contracts on-chain for wstETH, weETH, and osETH. Traced each CAPO adapter's composition chain: ratio provider, snapshot parameters, Chainlink feed addresses, current capping status.

### What was found

**Measured: Liquidation event data from March 10 incident**

- 49 LiquidationCall events across Aave Core (22) and Prime (27) pools
- 35 unique users liquidated
- 10,938.59 wstETH seized, 12,943.60 WETH debt repaid (~$28.7M total)
- All events completed in blocks 24626860–24626867 (84 seconds, 11:46:11–11:47:35 UTC)
- 5 liquidator bots captured all events. Top bot (0xbd321...) seized 5,328 wstETH in a single transaction in the same block as the CAPO parameter update.

**Measured: Cross-reference with position snapshot**

11 of 35 liquidated users found in our position snapshot. All 11 matched positions were phantom E-Mode loops (wstETH or weETH collateral, WETH debt), HF 1.01–1.09 at snapshot time. Largest matched:

| User | Snapshot HF | Snapshot Size | wstETH Seized |
|------|------------|---------------|---------------|
| 0x4f962bb0... | 1.0593 | $15.2M | 5,328 |
| 0x1e2799e0... | 1.0601 | $12.6M | 792 |
| 0x5cede91b... | 1.0328 | $6.2M | 126 |
| 0x4bacce55... | 1.0918 | $5.3M | 1,874 |
| 0xf82d8c60... | 1.0457 | $3.2M | 1,155 |

24 of 35 liquidated users were not in our snapshot — either positions opened between snapshot and incident, or too small to appear. Mega-whales appear stable across both timepoints.

**Measured: Mega-whale survival margins**

| User | Size | HF | Collateral | Depeg to Liquidation | Margin vs. 2.85% Incident |
|------|------|-----|-----------|---------------------|--------------------------|
| 0x9600a48e... | $1.42B | 1.0398 | wstETH | 3.83% | 0.98% survived |
| 0xf0bb2086... | $1.26B | 1.0541 | weETH | 5.14% | 2.29% survived |
| 0xef417fce... | $0.28B | 1.0457 | weETH | 4.37% | 1.52% survived |
| 0x58e70d8b... | $0.11B | 1.0306 | weETH | 2.97% | 0.12% survived |

The $1.42B wstETH whale survived the 2.85% incident by 0.98 percentage points. The $0.11B weETH position survived by 0.12 percentage points. These margins are approximate — HF values are from our snapshot date, not the exact incident moment.

**Measured: CAPO oracle composition**

Each LST's Aave price is computed as: `min(actual_on_chain_rate, capped_rate) × Chainlink_market_feed × ETH/USD`

| Token | CAPO Adapter | Ratio Provider | Snapshot Ratio | Snapshot Date | Snapshot Delay | Currently Capped |
|-------|-------------|----------------|---------------|---------------|----------------|-----------------|
| wstETH | 0xe1d9... | Lido stETH (stEthPerToken) | 1.2283 | 2026-03-03 | 7 days | No |
| weETH | 0x8762... | weETH contract (getRate) | 1.0347 | 2024-03-26 | 7 days | No |
| osETH | 0x2b86... | StakeWise vault | 1.0144 | 2024-04-24 | 7 days | No |

CAPO caps downward only: `min(actual, capped)`. It prevents upward manipulation but provides zero protection against downward depegs. Real market depegs pass through to HF calculations unimpeded.

wstETH's Chainlink stETH/ETH feed: 0.99991556, last updated 2026-03-19. This is the market-driven component for wstETH.

weETH and osETH Chainlink market feed addresses were not resolved in this probe (blank fields in output). Their specific market-driven components remain untraced.

**Measured: Incident mechanism**

The March 10 incident was caused by a CAPO snapshotRatio configuration error, not a market event:
- Stale snapshotRatio: ~1.1572
- On-chain max growth cap (3% per 7-day delay): allowed increase only to ~1.1919
- Actual market rate: ~1.228
- Capped price: 1.1919/1.228 = 97.06% of true value → 2.85% undervaluation
- Execution: Chaos Labs' Edge Risk engine pushed update via BGD Labs' AgentHub using Chainlink Automation. No manual review. No human in the loop.

### Structural findings from review discussion

**Recovery-suppression loop withdrawn for market depegs.** The CAPO rate-limit (3% per 3 days on upward moves) applies to the snapshot ratio parameter, which constrains the *protocol exchange rate* from growing too fast. In a real market depeg, the price drop propagates through the Chainlink stETH/ETH component, which has no rate limit in either direction. Both downward depeg and upward recovery are governed by Chainlink's symmetric update dynamics. The CAPO ratchet is specific to configuration errors (like March 10), not to market events.

**Two-layer cascade model for wstETH.** The Aave oracle for wstETH watches Chainlink stETH/ETH, not the wstETH/ETH DEX price directly. For a market-driven cascade:

1. wstETH sold on DEX → wstETH/ETH drops
2. Arbitrageurs unwrap wstETH → stETH (at protocol rate, no slippage) and sell stETH
3. stETH/ETH drops on Curve → Chainlink stETH/ETH crosses deviation threshold → updates
4. CAPO composition reflects lower stETH/ETH → wstETH Aave price drops
5. Phantom positions' HF drops → liquidations → bots seize wstETH
6. Bots sell wstETH on DEX → back to step 1

Step 1's depth probe measured wstETH→WETH, but the oracle pathway runs through stETH→ETH (step 3). If Curve stETH/ETH has significantly different depth than the wstETH DEX pools, the cascade dynamics differ from what the Step 1 numbers imply. The Curve stETH/ETH pool once held >$1B but now has ~$40M TVL. Its actual depth at various sell sizes has not been measured.

**84-second execution speed.** The full liquidation wave completed in 84 seconds. The largest single liquidation (5,328 wstETH, ~$14M) occurred in the same block as the CAPO parameter update. Liquidation bots had transactions pre-staged, waiting for the oracle to tip. This demonstrates that once the oracle reflects a depeg, the liquidation→collateral seizure step takes 0-1 blocks. The Chainlink update is the only speed bottleneck for real market depegs.

**Bot collateral disposal: unknown.** 10,938 wstETH was seized but wstETH DEX capacity is only ~2,663 ETH ($5.7M). In the March 10 case, the market was healthy so bots could sell at fair value. In a real depeg, bots must choose: sell on DEX (amplifies depeg), unwrap to stETH and sell on Curve (propagates to oracle layer), sell on CEX (doesn't amplify on-chain depeg), or hold. The choice determines whether liquidations amplify or absorb the cascade. Not yet traced from March 10 transaction data.

### What remains untested

1. **Chainlink stETH/ETH deviation threshold and heartbeat** — the single number that determines trigger sensitivity for the wstETH cascade loop. If 0.5%, moderate selling starts the loop. If 2%, a larger dislocation is needed. Queryable on-chain from the Chainlink aggregator contract.

2. **stETH/ETH DEX depth** — repeat the Paraswap probe for stETH→ETH. This is the layer the wstETH oracle actually watches. If Curve stETH/ETH is significantly deeper than wstETH/WETH pools, the cascade is harder to trigger through the oracle than Step 1 numbers suggest.

3. **weETH and osETH oracle market feeds** — the Chainlink feed addresses that compose their CAPO prices were not resolved. Need to trace: does each use a direct market feed, or similar indirection through base tokens (eETH, osETH underlying)?

4. **Historical depeg magnitudes** — have real market depegs of 2-4% occurred post-Merge for any LST? The June 2022 stETH depeg (~7%) was pre-Merge/pre-CAPO. Post-Merge data would tell us whether the measured cliff edges have been historically reached by organic market stress.

5. **Bot collateral disposal routing** — trace the liquidator bot transactions post-seizure on March 10 to determine where they sold/held the wstETH. Reveals bot playbook for future events.

6. **weETH/osETH CAPO staleness risk** — weETH snapshot from March 2024, osETH from April 2024. Both are nearly 2 years old. The same configuration error class that hit wstETH could hit these tokens, creating an oracle-driven (not market-driven) cascade affecting different phantom positions.

### Data produced

- `data/capo_liquidations_mar10.csv` — 49 liquidation events with block, timestamp, user, collateral/debt amounts, liquidator, tx hash
- `data/capo_position_overlap.csv` — 11 cross-referenced positions with snapshot data
- `data/oracle_composition.csv` — CAPO adapter parameters for wstETH, weETH, osETH
- `data/2_results.txt` — narrative summary
- `oracle_probe.py` — on-chain forensics and oracle trace script

### Question evolution

After iteration 1: "Does any self-correcting mechanism operate faster than the cascade feedback loop?"

After iteration 2: The question splits into two pathways:

**Market-driven cascade:** Chainlink stETH/ETH deviation threshold determines loop speed. stETH/ETH Curve depth determines whether the cascade stalls at the oracle layer. Both unmeasured. The cascade has a two-layer structure (wstETH DEX → stETH/ETH Curve → Chainlink → Aave) that Step 1's single-layer measurement didn't capture.

**Oracle-driven cascade (CAPO misconfiguration):** Demonstrated on March 10. Missed the $1.42B whale by 0.98%. A repeat with slightly staler parameters or slightly more leveraged positions would trigger catastrophic liquidations into $5.7M of DEX capacity. The weETH and osETH CAPO snapshots (2024) are candidates for the same failure mode.

---

## Iteration 3: Chainlink Feed Timing + Oracle-Layer Depth + Feed Architecture

**Date:** 2026-03-20

### What was tested

**Task A: Chainlink stETH/ETH feed timing**

Pulled last 20 rounds from the Chainlink stETH/ETH proxy (`0x86392dC19c0b719886221c78AB11eb8Cf5c52812`) via the underlying aggregator (`0xc9c8efa84eab332d1950e5ba0a913b090775825c`). Computed gap between rounds, deviation between consecutive answers.

**Task B: Oracle-facing DEX depth probes**

Ran Paraswap aggregator depth probes for stETH→WETH and eETH→WETH using the same methodology as Step 1, with adaptive bisection refinement at cliff boundaries.

**Task C: CAPO feed architecture identification**

Decomposed each CAPO adapter's `latestAnswer` into components to identify whether a market-priced Chainlink feed sits in the oracle path. For each token: `USD_price = effective_ratio × implied_market_feed × ETH/USD`. If `implied_market_feed ≈ 1.0`, no separate market feed exists; if it deviates significantly, an intermediate Chainlink feed is present.

### What was found

**Measured: Chainlink stETH/ETH operates on a pure 24-hour heartbeat**

All 20 consecutive rounds update at exactly 24.0h intervals (~19:25-19:31 UTC daily). Zero deviation-triggered updates observed. Maximum inter-round price deviation: 0.039%. Answer range over 20 days: 0.99897 to 0.99992 (total spread: 0.095%).

The stETH/ETH rate has been stable enough that the deviation threshold (likely 0.5% or 1.0%) has never been triggered in the observed window. The feed updates once daily regardless of market conditions.

**Measured: stETH→WETH DEX depth (oracle-facing layer)**

| Sell Amount | Depeg | Route |
|------------|-------|-------|
| 1,000 ETH | 0.008% | UniswapV3+wstETH |
| 2,000 ETH | 0.047% | CurveV1Factory+UniswapV3+wstETH |
| 3,500 ETH | 13.78% | CurveV1Factory+UniswapV2+UniswapV3+wstETH |
| 3,688 ETH | NO ROUTE | — |

Max capacity: ~3,018 ETH ($6.4M). Cliff between 2,000 and 3,500 ETH. Thresholds: 0.5% depeg at ~$4.4M, 1.0% at ~$4.5M, 2.0% at ~$4.7M.

The stETH sell routes go through `UniswapV3+wstETH` — the Paraswap router wraps stETH→wstETH then uses wstETH/WETH pools. The stETH/ETH oracle layer and the wstETH/WETH DEX layer share the same underlying liquidity. No additional buffer exists at the oracle-facing layer. stETH/ETH capacity ($6.4M) and wstETH/WETH capacity ($5.7M) are overlapping, not additive.

**Measured: eETH→WETH DEX depth**

| Sell Amount | Depeg | Route |
|------------|-------|-------|
| 10 ETH | 0.30% | CurveV1StableNg |
| 30 ETH | 3.17% | CurveV1StableNg+SushiSwap |
| 42 ETH | 14.06% | CurveV1StableNg+SushiSwap |
| 45 ETH | NO ROUTE | — |

Max capacity: ~36 ETH ($77K). Catastrophically thin — $5K of selling produces 0.5% depeg. Pool exhausts at 42 ETH (~$90K). However, this is not directly relevant to weETH cascade because the weETH CAPO oracle reads protocol rates, not eETH market prices.

**Measured: CAPO feed architecture decomposition**

| Token | Implied Market Feed | Structure | Market Feed in Oracle Path? |
|-------|--------------------|-----------|-----------------------------|
| wstETH | ~1.004 | ratio × stETH/ETH_CL × ETH/USD | **Yes** — Chainlink stETH/ETH (confirmed) |
| weETH | ~1.002 | ratio × ETH/USD | **No** — reads getRate() protocol rate |
| osETH | ~1.055 | ratio × X/ETH × ETH/USD | **Uncertain** — 1.055 too far from 1.0, suggests intermediate feed |

wstETH is the only LST where a genuine DEX-market Chainlink feed sits in the oracle path. The weETH CAPO adapter reads `getRate()` on the weETH contract — this is a protocol-level exchange rate that only changes with staking yield accrual, not with DEX market prices. A weETH/ETH DEX depeg does not flow through to the Aave oracle.

The osETH implied market feed of 1.055 is too far from 1.0 to be rounding noise. This suggests an intermediate Chainlink feed exists but was not resolved. osETH may have a market-cascade pathway similar to wstETH.

### Structural findings from review discussion

**The cascade model splits into three distinct vulnerability channels:**

1. **wstETH market cascade ($1.7B phantom):** DEX depeg → Chainlink stETH/ETH → CAPO → liquidations. Gated by 24h heartbeat. Slow-burn "siege" dynamics with daily oracle update cycles. Self-correction window exists (arbitrageurs have up to 24h to restore peg before oracle updates). But if depeg persists through heartbeat, all accumulated liquidation eligibility resolves simultaneously — potentially a larger single-block detonation than a gradual cascade. The $1.42B whale at HF 1.040 needs 3.83% sustained depeg. Achievable with ~$5-6M of selling pressure on the shared stETH/wstETH pools.

2. **weETH protocol/operational cascade ($3.0B phantom):** NOT vulnerable to DEX market depeg. Oracle reads protocol rates. Vulnerable to: (a) CAPO misconfiguration — demonstrated March 10, weETH snapshot stale since March 2024 (live operational risk), (b) validator slashing affecting getRate() — instant propagation, no oracle gate, (c) EtherFi smart contract exploit. When triggered, zero delay — CAPO rate-limit does not apply to downward moves.

3. **osETH uncertain ($332M phantom):** Possibly market-cascade vulnerable if the implied 1.055 feed is a live Chainlink market feed. If so: cheapest trigger in the system ($388K to 2% depeg), $332M phantom at that threshold, 856x cascade ratio. Oracle pathway unconfirmed.

**Deviation threshold behavior under stress: genuinely uncertain.** The 24h heartbeat is what we observe in calm conditions. In a real 3% stETH depeg, Chainlink nodes might trigger a deviation-based early update (if threshold is 0.5-1%), making the cascade faster than the pure 24h model. But this has never been tested for this feed. We cannot determine from current data whether the 24h or deviation-triggered model applies in stress.

**The "delayed detonation" model:** If the depeg persists beyond 24h (because withdrawal queue takes 1-5 days and arb capital is limited), each oracle update produces a step-function wave of liquidations. The cascade unfolds over days, not seconds. Each cycle: oracle updates → liquidation wave fires within seconds → seized collateral dumped → depeg deepens → next 24h wait → repeat. Self-sustaining if depeg persists above whale liquidation thresholds between cycles.

### What remains untested

1. **osETH oracle pathway** — resolve the 1.055 implied market feed. If it's a Chainlink market feed, osETH is the cheapest cascade trigger. If it's a protocol rate artifact, osETH has the same protection as weETH.

2. **Chainlink stETH/ETH deviation threshold** — the actual threshold value (0.5%? 1%? 2%) determines whether a real depeg triggers an early oracle update or waits for the 24h heartbeat. Not determinable from on-chain data alone (off-chain Chainlink node configuration). Could potentially be inferred from historical stress periods if stETH/ETH has ever deviated significantly.

3. **Historical depeg magnitudes (Step 2)** — what stETH/ETH depegs have occurred post-Merge? The June 2022 event was pre-Merge. Post-Merge depeg history would reveal whether the measured cliff edges ($4.5M for 1% stETH depeg) have been approached by organic market stress.

4. **Bot collateral disposal routing** — where did March 10 liquidator bots sell their seized wstETH? Determines amplification factor of each cascade cycle.

5. **Validator slashing magnitude for weETH** — how much correlated slashing would change EtherFi's getRate() by 3-5%? Determines the protocol-event trigger threshold for the $3.0B weETH phantom exposure.

### Data produced

- `data/chainlink_steth_eth_rounds.csv` — 20 rounds with timestamps, gaps, deviations
- `data/steth_depth.csv` — 19 rows of stETH→WETH depth quotes
- `data/eeth_depth.csv` — 18 rows of eETH→WETH depth quotes
- `data/oracle_feeds.csv` — CAPO feed decomposition for wstETH, weETH, osETH
- `data/3_results.txt` — narrative summary
- `oracle_depth_probe.py` — reproducible script

### Question evolution

After iteration 2: "Does anything stop the cascade loop from becoming self-sustaining?"

After iteration 3: The single cascade model has decomposed into three distinct vulnerability channels with different mechanisms, speeds, and trigger costs:

- **wstETH:** Market-cascade viable but gated by 24h Chainlink heartbeat. Slow-burn siege dynamics. Self-correction window exists. Unknown whether deviation-triggered updates would accelerate the loop in genuine stress.
- **weETH:** NOT DEX-cascade vulnerable. Protocol/operational risk only. CAPO stale snapshot (March 2024) is a live operational risk for repeat of the March 10 incident. Validator slashing would propagate instantly through protocol rate.
- **osETH:** Oracle pathway unresolved. If market feed exists, cheapest cascade trigger in the system.

The investigation found a heterogeneous vulnerability surface rather than a single dramatic cascade. Different tokens fail through different mechanisms at different speeds. No single fix addresses all channels.

---

## Iteration 4: osETH Oracle Resolution + CAPO Bytecode Forensics + Findings

**Date:** 2026-03-20

### What was tested

**Task A: osETH oracle pathway resolution**

Investigated the ~1.055 implied market feed factor from iteration 3. Tested both the `convertToAssets()` function (actual protocol rate) vs. the stale `snapshotRatio` (1.01445, from April 2024). Extracted all embedded addresses from CAPO adapter bytecode via PUSH32 instruction scanning for all three adapters (wstETH, weETH, osETH).

**Task B: Consolidated findings document**

Wrote `findings.md` integrating all four iterations.

### What was found

**Measured: osETH implied feed was a measurement artifact**

The ~1.055 factor from iteration 3 resulted from using the wrong ratio function. Iteration 3 used `snapshotRatio` (1.01445, stale since April 2024) instead of the actual protocol rate from `convertToAssets(1e18)` (1.06788). Correct decomposition:

```
osETH CAPO price = convertToAssets(1e18) × ETH/USD = 1.06788 × $2150.76 = $2296.76
Actual CAPO latestAnswer = $2296.76 → 0.0000% error
```

No intermediate market feed exists. The implied 1.055 was an artifact of dividing by the wrong ratio.

**Measured: No CAPO adapter embeds any market-price Chainlink feed (bytecode-verified)**

PUSH32 instruction extraction from all three adapter bytecodes confirmed each embeds exactly three addresses:

| Adapter | Address 1 | Address 2 | Address 3 |
|---------|-----------|-----------|-----------|
| wstETH | `0x5424...` (ETH/USD CL) | `0xae7a...` (stETH contract) | `0xc2aa...` (PoolAddressesProvider) |
| weETH | `0x5424...` (ETH/USD CL) | `0xc2aa...` (PoolAddressesProvider) | `0xcd5f...` (weETH contract) |
| osETH | `0x2a26...` (StakeWise vault) | `0x5424...` (ETH/USD CL) | `0xc2aa...` (PoolAddressesProvider) |

The Chainlink stETH/ETH feed (`0x86392dC19c...`) is NOT present in any adapter's bytecode. All three adapters use the identical architecture: `cap(protocol_rate) × ETH/USD`.

**This overturns the iteration 3 finding** that wstETH's CAPO included a Chainlink stETH/ETH market feed. The market-cascade channel modeled for wstETH in iterations 1-3 does not exist. DEX selling of stETH/wstETH does not propagate to the Aave oracle.

### Major model revision

**The reflexive cascade thesis is structurally blocked at the Aave oracle layer for ALL phantom positions.**

The cascade model from iterations 1-3 — DEX depeg → Chainlink market feed → CAPO reflects → Aave liquidation → collateral dump → deeper depeg → loop — cannot complete because no CAPO adapter reads market prices. The oracle reads protocol-level exchange rates that change only with staking rewards accrual, validator slashing, or smart contract events.

**Revised vulnerability channels:**

1. **CAPO operational risk (demonstrated, live preconditions):** Misconfigured snapshot parameter → oracle underprices LST → mass liquidation. March 10 demonstrated this for wstETH: 2.85% artificial depression, 49 liquidations, $28.7M seized, $1.42B whale survived by 0.98%. weETH snapshot is 2 years stale (5.4% drift from actual rate). osETH snapshot similarly stale. Same automated update pipeline (Chaos Labs → AgentHub → on-chain, no human review).

2. **Protocol rate disruption (theoretical, instant propagation):** Validator slashing or smart contract exploit changes protocol exchange rate → oracle reflects instantly → liquidations. No Chainlink delay, no heartbeat gate. A 3.83% drop in wstETH's `getPooledEthByShares` would liquidate the $1.42B whale. Requires correlated validator failure at scale — historically rare but not impossible.

3. **ETH/USD crash (standard leverage risk):** Not LST-specific. Phantom positions amplify standard leverage risk because they represent concentrated leverage ($5.6B) that standard risk dashboards may undercount.

**What the DEX depth data remains relevant for:**
- Liquidator execution: when Aave does liquidate (for any reason), bots must sell seized LST on DEX. Thin pools ($5.7M wstETH capacity) mean large slippage on $1.42B worth of collateral.
- Cross-protocol cascade: other protocols (Morpho, Euler, Spark) may use market-price Chainlink feeds for LSTs. The reflexive cascade model disproved for Aave may apply to those protocols. Their liquidations dump onto the same thin DEX pools.
- Market microstructure: cliff structure (phase-transition behavior) is real regardless of oracle architecture.

### Structural synthesis from review discussion

**"The system traded distributed market risk for concentrated operational risk."** — The CAPO architecture that blocks market cascades simultaneously creates a centralized configuration surface where a single parameter error produces the exact cascade the architecture was designed to prevent. The March 10 incident demonstrated this trade-off empirically.

**Cross-protocol contagion elevated as testable hypothesis:** The reflexive cascade model disproved for Aave may apply to protocols using market-price LST oracles. A cascade originating in Morpho/Euler could propagate to Aave through sustained market stress → protocol rate erosion. This is an unexamined extension, not merely an uncertainty.

**CAPO operational risk assessed as highest-priority finding:** Demonstrated failure mode, ongoing preconditions (stale snapshots), automated pipeline with minimal safeguards, $1.42B whale within 0.98% of demonstrated trigger. The weETH snapshot drift (5.4%) already exceeds the wstETH incident magnitude (2.85%).

### Data produced

- `data/oseth_oracle.csv` — definitive osETH oracle decomposition
- `data/oracle_feeds.csv` — updated with bytecode-verified architecture for all three tokens
- `findings.md` — 248-line consolidated investigation document
- `oseth_oracle_probe.py` — bytecode extraction and verification script

### Question evolution

After iteration 3: "Does anything stop the cascade loop?" → decomposed into three channels, with wstETH having a market feed.

After iteration 4: The market cascade channel does not exist for any Aave CAPO adapter. The original reflexive cascade thesis is refuted for Aave.

**Final question state:**

The investigation began asking: "What depeg magnitude triggers cascade activation for the $5.6B phantom wall?"

It ended with: "The phantom wall's primary defense (protocol-rate oracles) is also its primary vulnerability (CAPO operational risk). The system traded distributed market risk for concentrated operational risk. Is the operational discipline of the teams managing CAPO parameters adequate to the $5.6B at stake?"

This question is not answerable through on-chain measurement alone — it depends on process, governance, and human factors. The investigation has reached the boundary of what technical probing can determine.
