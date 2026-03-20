# LST Phantom Position Cascade Vulnerability: Investigation Findings

> Investigation date: 2026-03-20
> Method: On-chain probing (Alchemy RPC), aggregated DEX quotes (Paraswap), Chainlink feed analysis, CAPO bytecode forensics
> Scope: 7 LST tokens, Aave v3 Core + Prime pools, Ethereum mainnet

---

## 1. Investigation Summary

DeFi lending protocols hold ~$5.6B in "phantom positions" — LST-collateral / WETH-debt loops that liquidate on LST/ETH exchange rate movement, not ETH/USD price. This investigation quantified the cascade vulnerability: how much selling triggers depeg, how fast the oracle reflects it, and what positions survive.

**Four measurement layers:**
1. **DEX liquidity depth** — how much selling depegs each LST by 1-5% (Paraswap aggregated quotes across all DEXes)
2. **March 10 CAPO incident forensics** — on-chain liquidation events, position cross-reference
3. **Chainlink feed timing** — stETH/ETH update frequency and deviation behavior
4. **Oracle architecture** — definitive CAPO adapter bytecode analysis, price composition verification

---

## 2. Critical Discovery: Oracle Architecture

**ALL THREE Aave CAPO adapters use: `cap(protocol_rate) × ETH/USD`**

No intermediate market feeds (stETH/ETH, eETH/ETH, osETH/ETH) are used. This was verified by:
- Extracting embedded addresses from PUSH32 instructions in adapter bytecode
- Price decomposition: `protocol_rate × ETH/USD = CAPO_latestAnswer` with 0.0000% error for all three tokens

| Token  | CAPO Adapter | Rate Function | Rate Provider | ETH/USD Feed |
|--------|-------------|---------------|---------------|--------------|
| wstETH | `0xe1d97b...` | `getPooledEthByShares(1e18)` | stETH contract | `0x542438...` |
| weETH  | `0x876253...` | `getRate()` | weETH contract | `0x542438...` |
| osETH  | `0x2b86d5...` | `convertToAssets(1e18)` | StakeWise vault | `0x542438...` |

**Implication:** DEX market depegs in stETH/ETH, eETH/ETH, or osETH/ETH **do not directly affect Aave oracle pricing**. The Aave oracle reads protocol-level exchange rates, not market prices. This fundamentally changes the cascade model.

The Chainlink stETH/ETH feed at `0x86392dC19c...` exists and updates daily, but is **NOT** embedded in any of these CAPO adapters. It serves other purposes (other protocols, reference).

---

## 3. Vulnerability Channels (Revised)

### Channel 1: CAPO Operational Risk (DEMONSTRATED)

**Mechanism:** CAPO misconfiguration → oracle underprices LST → phantom positions appear undercollateralized → mass liquidation

**Empirical evidence — March 10, 2026:**
- Chaos Labs pushed a stale `snapshotRatio` (1.1572) with a misaligned `snapshotTimestamp` (7 days old)
- On-chain 3% growth cap constrained the ratio to ~1.1919 vs actual market rate ~1.228
- 2.85% artificial underpricing → **49 liquidation events in 84 seconds**
- 10,938 wstETH seized ($28.7M) across 35 users in Core + Prime pools
- 5 liquidator bots captured all events; one bot seized $14M in a single block
- 11 of 35 liquidated users matched our phantom position snapshot (all HF 1.01-1.09)

**Proximity to catastrophe:**
- $1.42B wstETH whale (HF 1.040) needs 3.83% depeg → **survived by 0.98% margin**
- $110M weETH position (HF 1.031) needs 2.97% depeg → survived by 0.12% margin
- A slightly staler ratio or slightly more leverage would have triggered $1.5B+ in liquidations

**Ongoing risk factors:**
- weETH snapshot ratio dates to **March 2024** (2 years stale)
- osETH snapshot ratio dates to **April 2024** (also nearly 2 years stale)
- All three adapters use 7-day minimum snapshot delay with growth-rate caps
- The March 10 failure mode (ratio/timestamp misalignment) could recur for any token

### Channel 2: Protocol Rate Disruption (Theoretical)

**Mechanism:** Validator slashing or smart contract exploit → protocol rate drops → oracle reflects instantly → liquidations

For each LST, the protocol rate changes only when:
- **wstETH:** Lido validators slashed (reduces ETH backing per stETH share)
- **weETH:** EtherFi validators slashed or protocol exploit
- **osETH:** StakeWise validators slashed

**Rate sensitivity:** A 3% drop in protocol rate would:
- Push the $1.42B wstETH whale below HF 1.0 (liquidatable)
- Trigger liquidation of ~$2B+ in phantom positions at HF < 1.03

**Probability assessment:** Major slashing events (>1% rate impact) are historically rare but not impossible. The Ethereum PoS penalty structure limits single-incident impact, but correlated failures (e.g., client bug affecting multiple validators) could produce larger moves.

### Channel 3: ETH/USD Crash (Standard, Amplified)

**Mechanism:** ETH/USD drops → all phantom position HFs drop proportionally → liquidations → selling pressure → deeper ETH/USD drop

This is standard leverage risk, but the phantom position structure amplifies it:
- $5.6B in LST/WETH loops at 1.01-1.09 HF represents ~$250B-$550B in notional leverage
- These positions are often overlooked by standard risk models that focus on ETH/USD only
- During an ETH/USD crash, liquidation selling of LST collateral hits thin DEX pools

---

## 4. DEX Liquidity Depth (Cascade Execution Layer)

Even though DEX depegs don't directly affect the Aave oracle, DEX depth matters for:
1. **Liquidator execution** — when Aave liquidates, the bot must sell seized LST on DEX
2. **Market impact of liquidation selling** — thin DEX pools mean large price impact from collateral dumps
3. **Other protocols** that DO use market-price feeds

### Per-Token Depth Summary

| Token  | DEX Capacity | $→2% depeg | Phantom Exposure | Cascade Ratio |
|--------|-------------|------------|-----------------|---------------|
| ETHx   | ~$21K       | EXHAUSTED  | $100M           | 4,681×        |
| cbETH  | ~$390K      | ~$260K     | $150M           | 583×          |
| osETH  | ~$976K      | ~$388K     | $332M           | 856×          |
| rETH   | ~$1.0M      | ~$547K     | $200M           | 366×          |
| rsETH  | ~$2.0M      | EXHAUSTED  | $880M           | 434×          |
| wstETH | ~$5.7M      | ~$4.7M     | $1,700M         | 363×          |
| weETH  | ~$13.9M     | ~$11.3M    | $230M           | 20×           |

### Oracle-Facing Layer

| Token  | DEX Capacity | $→0.5% depeg | $→2% depeg |
|--------|-------------|-------------|------------|
| stETH  | ~$6.4M      | ~$4.4M      | ~$4.7M    |
| eETH   | ~$77K       | ~$5K        | ~$27K     |

**Key finding: cliff structure, not curves.** Every LST shows a sharp liquidity cliff where the aggregator exhausts ALL available DEX liquidity. Below the cliff: minimal slippage. Above: price falls off a cliff (13-14% depeg or NO ROUTE).

stETH and wstETH share the same underlying DEX pools (stETH routes through wstETH + Curve/Uniswap). They are not independent buffers.

eETH DEX liquidity is essentially zero ($77K total). But this doesn't matter for the oracle because the weETH CAPO reads `getRate()`, not market prices.

---

## 5. Chainlink stETH/ETH Feed Behavior

Even though this feed is NOT used by the CAPO adapter, it reveals Chainlink feed dynamics relevant to the broader ecosystem:

- **Update frequency:** Exactly 24.0h (heartbeat-only), no deviation-triggered updates in 20+ rounds
- **Answer range:** 0.99897 to 0.99992 (spread: 0.095% over 20 days)
- **Deviation threshold:** Appears to be ≥0.5% but has never been triggered (stETH/ETH is too stable)
- **Implication for other protocols:** Any protocol using this feed for stETH pricing would have up to 24h oracle lag during a depeg event

---

## 6. Structural Findings

### 6.1 Protocol-Rate Oracles as Cascade Damper

The CAPO architecture creates a **one-way valve** for cascade propagation:

- DEX selling → depeg → **BLOCKED at oracle** (oracle reads protocol rate, not market)
- Protocol event (slashing) → rate drop → oracle reflects instantly → liquidation → DEX selling

This means the classic reflexive cascade (depeg → liquidation → more selling → deeper depeg → more liquidation) **cannot complete through the oracle feedback loop** for market-price depegs. The DEX depeg and the oracle exist in separate domains.

However: sustained DEX depeg eventually manifests in protocol rates (via arbitrageurs unwrapping/wrapping, withdrawal queue dynamics), creating a slow feedback mechanism on the timescale of hours to days.

### 6.2 Liquidity Vacuum

Yield-seeking capital has drained DEX pools into lending positions, simultaneously:
1. Creating the phantom exposure ($5.6B in leveraged LST/WETH loops)
2. Destroying the liquidity buffer that would absorb selling pressure

The same capital that creates the vulnerability is the capital that was removed from the safety net.

### 6.3 CAPO as Single Point of Failure

The CAPO adapter is a centralized risk surface:
- A single `snapshotRatio` parameter update can instantly move the oracle by several percent
- The update pathway (Chaos Labs → AgentHub → on-chain, one block, no human review) has minimal safeguards
- March 10 demonstrated: configuration error → $28M liquidated in 84 seconds
- Near-miss: $1.42B whale was 0.98% from liquidation
- Stale snapshots for weETH (2 years old) and osETH (2 years old) represent ongoing operational risk

### 6.4 Heterogeneous Risk Profiles

| Property | wstETH | weETH | osETH |
|----------|--------|-------|-------|
| Phantom exposure | $1.7B | $3.0B | $332M |
| Oracle rate source | stETH protocol | weETH protocol | StakeWise vault |
| Rate update trigger | Staking rewards (daily) | Staking rewards | Staking rewards |
| CAPO snapshot age | 17 days | ~2 years | ~2 years |
| DEX depth to 2% depeg | $4.7M | $11.3M | $388K |
| Cascade ratio | 363× | 20× | 856× |
| Market feed in oracle? | No | No | No |
| Biggest position at risk | $1.42B @ HF 1.040 | $1.26B @ HF 1.054 | smaller |

---

## 7. What Remains Uncertain

1. **Chainlink deviation threshold under stress:** Has the stETH/ETH feed EVER had a deviation-triggered update? The 24h heartbeat may mask a deviation trigger that would fire under genuine stress. No way to test this without historical data going back to the Merge.

2. **Cross-protocol contagion:** Other lending protocols (Spark, Morpho, Euler) may use market-price oracles for the same LSTs. A DEX depeg could trigger liquidations on those protocols even if Aave is shielded.

3. **Liquidator collateral disposal routing:** When bots seize wstETH, do they sell on DEX (amplifying depeg) or OTC/CEX (absorbing without DEX impact)? The March 10 data shows bots acted in-block, suggesting DEX routing.

4. **Withdrawal queue dynamics:** During stress, how fast can arbitrageurs unwrap LSTs through protocol withdrawal queues? If queues back up, the market-to-protocol rate gap can persist longer.

5. **Correlated slashing probability:** What is the realistic probability of a validator slashing event large enough to move wstETH protocol rate by 3%+? Depends on client diversity, infrastructure concentration.

6. **CAPO operational process:** Has Chaos Labs implemented safeguards since March 10 to prevent ratio/timestamp misalignment? Are the weETH and osETH stale snapshots scheduled for update?

---

## 8. Monitoring Signals

### For CAPO operational risk (highest demonstrated probability):
- **Watch:** CAPO `snapshotRatio` updates on-chain (topic: parameter update txs from Chaos Labs Edge Risk → AgentHub)
- **Alert:** Any update that moves the effective ratio >1% from current
- **Monitor:** Snapshot staleness for weETH and osETH (currently 2 years old)

### For protocol rate disruption:
- **Watch:** Ethereum validator slashing events (Beaconchain API)
- **Alert:** Any slashing affecting >100 validators in a single event
- **Monitor:** Lido, EtherFi, StakeWise operator health dashboards

### For DEX-layer stress (affects other protocols, and liquidator execution):
- **Watch:** stETH/ETH and wstETH/WETH DEX prices vs fair rate
- **Alert:** >0.5% persistent depeg (approaches cliff edge at $4-5M)
- **Canary:** ETHx and osETH depeg first (thinnest liquidity)

### For position topology shifts:
- **Watch:** New large phantom positions opening (Aave deposit/borrow events)
- **Monitor:** Health factor distribution of top-20 phantom positions
- **Alert:** Any mega-whale ($100M+) dropping below HF 1.03

---

## Data Files

All in `memories/mev/correlation/data/`:

| File | Description |
|------|-------------|
| `lst_liquidity_depth.csv` | 133 rows: detailed DEX quotes for 7 LSTs |
| `lst_depth_summary.csv` | Per-token depth summary with cascade ratios |
| `steth_depth.csv` | stETH→WETH depth (19 rows) |
| `eeth_depth.csv` | eETH→WETH depth (18 rows) |
| `chainlink_steth_eth_rounds.csv` | Last 20 Chainlink rounds with timing |
| `capo_liquidations_mar10.csv` | 49 March 10 liquidation events |
| `capo_position_overlap.csv` | 11 cross-referenced positions |
| `oracle_composition.csv` | CAPO adapter parameters |
| `oracle_feeds.csv` | Definitive CAPO architecture (bytecode-verified) |
| `oseth_oracle.csv` | osETH-specific oracle detail |
| `1_results.txt` | Step 1: DEX depth findings |
| `2_results.txt` | Step 2: CAPO incident forensics |
| `3_results.txt` | Step 3: Chainlink + oracle-layer depth |

Scripts:
| File | Purpose |
|------|---------|
| `depth_probe.py` | LST DEX depth measurement via Paraswap |
| `oracle_probe.py` | March 10 liquidation forensics + CAPO trace |
| `oracle_depth_probe.py` | Chainlink rounds + stETH/eETH depth + feed ID |
| `oseth_oracle_probe.py` | Definitive CAPO bytecode architecture verification |
