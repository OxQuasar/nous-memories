# Position Topology — Execution Plan

## Status: COMPLETE (6 iterations, 8 episodes backtested)

See `findings.md` for results summary, `signals-synthesis.md` for signal ranking, `exploration-log.md` for full evidence trail.

## Infrastructure

| Resource | Endpoint | Verified |
|---|---|---|
| Alchemy RPC | `alchemy.txt` | ✅ Block 24,693,844. Supports archive `eth_call` (free tier). |
| The Graph (Aave v3 Ethereum) | `graph.txt`, subgraph `Cd2gEDVeqnjBn1hSeqFMitw8Q1iiyV9FYUZkLNRcL87g` | ✅ Position data + historical block queries via `block: {number: N}` |
| The Graph (Aave v2 Ethereum) | N/A | ❌ Dead — legacy hosted service removed, no active indexers on decentralized network |
| Aave v2 historical | Alchemy archive multicall (on-chain approach) | ✅ ~28 min per snapshot. Only path for 2022 data. |
| ETH price data | `../data/eth_price_1h.csv` (hourly, 2022-01 → 2026-03) | ✅ |
| Episode dates | `../data/liquidation_events_combined.csv` (27 episodes) | ✅ |

## Execution Status

### Step 1: Current Snapshot ✅
- `snapshot.py`: Aave v3 current positions via subgraph + on-chain multicall + oracle
- 29,311 positions, $22.6B collateral, $13.2B debt
- eMode handled via on-chain `getUserAccountData`
- **Key discovery:** Apparent $4.3B wall at 5% below is phantom (ETH-loop strategies)

### Step 1b: Debt-Side Decomposition ✅
- `decompose.py`: Classifies positions as real/phantom/mixed based on debt composition
- Real wall within 20%: $73M. Phantom: $5.5B. Near-price zone is 99.99% phantom.
- Two populations with opposite spatial signatures: phantom tight HF near price, real wide HF far from price.

### Step 2: Density Map — SUPERSEDED
- Original plan: bucket liquidation prices into bins. 
- Replaced by the real/phantom decomposed fuel map computed inline during snapshot analysis.
- Density maps computed per-episode in the backtest (Iterations 5-6).

### Step 3: Maker/Sky Scan ✅ (added, not in original plan)
- `maker_scan.py`: 852 active ETH vaults, $1.63B collateral, $516M debt
- All Maker vaults are "real" by construction (DAI debt only)
- Maker adds <10% to real wall at all proximity bands
- **Decision:** Proceed Aave-only for historical backtest

### Step 4: Historical Probe ✅
- `historical_probe.py`: Aave v2 on-chain approach (borrower enumeration via getAssetTransfers + multicall)
- June 2022 snapshot: found $282M whale at liq=$1,185, $605M real debt in crash zone
- V2 subgraph dead → fully on-chain approach required for 2022 data

### Step 5: Fail-Fast Backtest (4 episodes) ✅
- `failfast_backtest.py`: Jun 2022, Nov 2022, Apr 2024, Aug 2024
- 4/4 correct classification. Two cascade modes identified (progressive, cliff).
- V3 subgraph historical queries confirmed working (~6x faster than V2 on-chain).

### Step 6: Expanded Backtest (8 episodes) ✅
- `backtest_expanded.py`: Added Jan 2022, Aug 2023, Sep 2024, Feb 2025
- 6/8 prospective classification (R20% + whale), 8/8 with actual drawdown depth
- Two false positives explained: shallow drawdowns didn't reach existing walls
- **Conclusion:** Topology is a conditional fuel map, not a binary predictor

### Step 7: Wall Dynamics — NOT EXECUTED
- Original plan: daily snapshots during episodes to track wall movement
- Not needed: the conditional fuel map framing answers the question differently. Wall stability matters less when topology is a severity gauge rather than a prediction.

## Risks (assessed)

1. **Subgraph balance staleness** — Acceptable. On-chain multicall used for ground-truth HF.
2. **Multi-collateral complexity** — Handled via weighted threshold from on-chain `getUserAccountData`.
3. **E-mode positions** — Resolved. On-chain HF correctly handles all 20+ eMode categories.
4. **Oracle price divergence** — Used on-chain oracle prices for consistency.
5. **Protocol coverage gap** — Tested. Maker adds <10% to real wall. Aave-only is representative.
6. **V2 subgraph unavailability** — Not anticipated. Resolved with fully on-chain archive approach.
7. **Phantom positions** — Not anticipated. The most important finding. Without debt-side decomposition, all analysis is misleading.

## Success Criteria (assessed)

- ✅ Step 1 produces a snapshot matching DefiLlama order of magnitude
- ⚠️ Step 4 shows wall proximity has higher predictive power than flow-phase signals: **PARTIALLY MET.** Topology provides conditional severity assessment (what happens IF drawdown reaches X%), not binary prediction. Prospective classification: 6/8 (75%) with R20% + whale metric. This is useful but not a clean binary predictor.
- ✅ Or: document why the thesis is wrong. **DONE.** The thesis was partially right (topology does determine cascade gain) but the framing was wrong (it's conditional on drawdown depth, not predictive of it). Additionally, the market has structurally rotated away from the risk surface the thesis described.

## What Remains

### Not done (deprioritized, diminishing returns)
- **Remaining 19 episodes.** 8 of 27 tested. Structural insights are stable. More episodes would tighten the 25% FP rate confidence interval but won't change the conditional fuel map conclusion.
- **On-chain whale liquidation verification.** $282M whale inferred liquidated — not verified via on-chain events. Would strengthen the stETH narrative but doesn't change findings.
- **Compound v3 topology.** Not scanned. Maker was tested and added <10%. Compound likely similar.
- **Wall dynamics during episodes.** Superseded by conditional framing.

### Successor: Correlation-Cascade Investigation

The position topology investigation revealed that the current market's actual vulnerability is not ETH/USD price-cascade but LST depeg-cascade. $5.6B phantom positions at HF 1.03-1.05 activate on staking derivative depeg events, not ETH price drops.

**Question:** What depeg threshold triggers cascade activation for the $5.6B phantom wall?

**Required data (not collected here):**
- DEX liquidity depth per LST (wstETH, weETH, osETH, rsETH) — how much selling before peg breaks
- Historical staking derivative depeg magnitudes during stress events (stETH Jun 2022: 7%, others unknown)
- Oracle lag behavior during rapid depeg — do Chainlink oracles update fast enough to trigger liquidations before arb restores peg?
- Depeg contagion across LST tiers — does osETH cracking (thin liquidity) spread to weETH (medium) then wstETH (deep)?

**Conjectured LST fragility hierarchy:**
- Tier 3 (osETH, tETH, ETHx): thin DEX liquidity, low depeg threshold, activate early, small absolute size (~$300M)
- Tier 2 (weETH): medium liquidity, medium threshold, $1.5B+ in phantom positions
- Tier 1 (wstETH): deep Curve/Balancer liquidity, high threshold, only cracks in severe systemic stress, $1.4B+ when it does

**Connection to flow phase:** The real/phantom decomposition and cascade mechanics model provide the foundation. The flow phase's monitoring system (regime → early warning → classification) remains valid for the real-wall layer. The correlation-cascade investigation would add a parallel track for phantom-wall monitoring.

This is a separate investigation with different data requirements. Create `mev/correlation/` when ready.
