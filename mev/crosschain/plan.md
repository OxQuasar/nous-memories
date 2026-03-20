# Cross-Chain Flows — Execution Plan

## Question

Where does money go during crypto stress events? Do cross-chain flow patterns predict, coincide with, or lag price movements? Is there arbitrage opportunity in cross-chain price dislocations during volatility?

THORChain is the starting point: a freely available source of directional cross-chain swap data with arb/organic decomposition. ~44 active pools, 49 months of daily history (Mar 2022 → Mar 2026), covering BTC, ETH, AVAX, BSC, DOGE, ATOM, LTC, SOL, TRX, XRP, BASE chains + major tokens/stablecoins.

## Data Source

**Midgard API** (`https://midgard.ninerealms.com/v2`). Free, no key, ~100 req/min rate limit.

### Key endpoints

| Endpoint | Data | Resolution |
|----------|------|------------|
| `/history/swaps?pool={pool}` | Swap volume, directional (toAsset/toRune), trade/secured/synth breakdown, count, fees, average slip | 5min, hour, day |
| `/history/depths/{pool}` | Pool depth (asset + rune side), price, liquidity units, member count | 5min, hour, day |
| `/history/tvl` | Per-pool and aggregate TVL over time | day |
| `/actions?type=swap` | Individual swap transactions with addresses, amounts, memo, slip | Per-action |

### Key fields per swap interval

| Field | Meaning |
|-------|---------|
| `toAssetVolumeUSD` | Volume swapping *into* the pool's asset (buying the asset) |
| `toRuneVolumeUSD` | Volume swapping *out of* the pool's asset (selling the asset) |
| `fromTradeVolumeUSD` / `toTradeVolumeUSD` | Arb/trade account volume (high-frequency, typically arbitrageurs) |
| `fromSecuredVolumeUSD` / `toSecuredVolumeUSD` | Secured (L1 native) swap volume |
| `averageSlip` | Mean slippage in basis points (liquidity stress indicator) |
| `totalCount` | Number of swaps |
| `totalFees` | Fees collected (in RUNE) |
| `synthMintVolumeUSD` / `synthRedeemVolumeUSD` | Synthetic asset minting/burning |

### Initial observations (from API probe)

**Yen carry crash (Aug 2024):**
- BTC.BTC: net selling -$1.4B (Aug 3), -$594M (Aug 5)
- ETH.ETH: net buying +$342M (Aug 5), +$482M (Aug 4)
- ETH.USDC: USDC accumulation pre-crash (+$162M Aug 4), then massive selling on crash day (-$256M Aug 5)
- Trade (arb) share jumped from ~55% to 86% on crash day

**2026 crash (Jan-Feb 2025):**
- BTC.BTC: persistent net selling (-$600M to -$1.1B/day)
- ETH.ETH: persistent net buying (+$143M to +$1B/day)
- Trade share jumped from ~65% baseline to 88-91% during peak stress

**Baseline (Mar 2026):**
- Trade share: ~50% of ETH.ETH volume
- Net flows roughly balanced

## Execution

### Step 1: Full Data Pull

Pull daily swap history for all significant pools across the full 49-month range.

**Pools to pull** (by 24h volume from current data):

| Tier | Pools | Combined 24h volume |
|------|-------|-------------------|
| Major | BTC.BTC, ETH.ETH, ETH.USDC, ETH.USDT | >$1.6B |
| Mid | BCH.BCH, BSC.BNB, BSC.USDT, BASE.USDC, BASE.ETH, DOGE.DOGE, ETH.DAI, AVAX.AVAX, AVAX.USDC, LTC.LTC, XRP.XRP, GAIA.ATOM, SOL.SOL, TRON.TRX, TRON.USDT | $5M-500M |
| Small/staging | BSC.USDC, BSC.ETH, BSC.BTCB, ETH.WBTC, tokens (LINK, AAVE, FOX, TGT, THOR, etc.) | <$5M |

Start with Major + Mid tiers. Max 400 intervals per call → 49 months = ~1,490 days → 4 calls per pool.

Also pull `/history/depths/{pool}` for Major pools (pool depth = available liquidity) and `/history/tvl` for aggregate.

**Output:** `data/swaps_daily.csv`, `data/depths_daily.csv`, `data/tvl_daily.csv`

### Step 2: Flow Mapping — Where Does Money Go?

Compute directional flow metrics per day across all pools:

**Per-pool metrics:**
- `net_flow = toAssetVolumeUSD - toRuneVolumeUSD` (positive = net buying, negative = net selling)
- `arb_share = (fromTradeVolumeUSD + toTradeVolumeUSD) / totalVolumeUSD`
- `organic_volume = totalVolumeUSD - trade_volume - secured_volume`

**Cross-pool derived metrics:**
- **Flight-to-safety ratio**: stablecoin pool buy volume / total volume across all pools
- **BTC/ETH rotation**: net BTC flow vs net ETH flow (divergence = rotation)
- **Chain dominance**: aggregate volume by source chain (ETH chain, BTC chain, BSC chain, etc.)
- **Concentration**: Herfindahl index across pools (high = flows concentrated in few pools)

**Per crash epoch:** Construct daily flow maps showing where money enters and exits. Visualize as: source chain → destination chain with net flow magnitude.

**Output:** `data/flow_metrics.csv`, flow maps per crash epoch

### Step 3: Flow-Price Correlation

Test whether THORChain flow metrics have predictive, contemporaneous, or lagging relationship with ETH price.

**Tests:**
- Pearson/Spearman correlation of daily net ETH flow (from ETH.ETH + BASE.ETH + BSC.ETH pools) with ETH daily return
- Same for BTC net flow vs BTC return
- Lead/lag cross-correlation at ±5 days
- Flight-to-safety ratio vs ETH return (and VIX, from links phase)
- Rolling 30-day correlation to detect regime shifts
- Per-epoch correlation (crash vs calm)

**Key hypothesis to test:** Do THORChain flows lead CEX price action? THORChain's slip-based AMM creates mechanical price impact that CEX arbitrageurs must correct. If large directional flows hit THORChain first (cross-chain users exiting positions), the flow direction could lead CEX price by minutes-to-hours.

**Counter-hypothesis:** THORChain flows lag CEX prices because arb bots continuously align THORChain prices to CEX. In this case, flows are reactive (arb correcting THORChain price after CEX moves) not predictive.

The arb share metric distinguishes these: if flows are arb-dominated (>70%), they're reactive corrections. If organic-dominated, they could be directional.

**Output:** `data/flow_price_correlations.csv`

### Step 4: Arbitrage Activity Analysis

THORChain's continuous liquidity pool model creates systematic arbitrage opportunities during price volatility. The `fromTrade`/`toTrade` fields directly measure this.

**Tests:**

**4a. Arb share as stress indicator:**
- Correlation of arb share with price volatility (daily absolute return)
- Does arb share spike *before* or *during* volatility? (lead/lag test)
- Arb share during Aave liquidation spike days vs normal days

**4b. Slip as liquidity stress:**
- `averageSlip` vs pool depth — does slip diverge from depth-predicted levels during stress?
- Slip spikes → do they precede or follow price drops?
- Compare slip across pools during same crash: which pools get stressed first?

**4c. Cross-chain arb economics:**
- Estimate arb profit: difference between THORChain pool price (from depths data) and external price (from eth_price.csv / yfinance)
- How long do price dislocations persist? (hourly resolution during crash windows)
- Pool depth vs dislocation magnitude — do shallow pools show larger/longer dislocations?
- Estimate MEV equivalent: total arb volume × average slip = approximate arb extraction

**4d. Arb as price transmission mechanism:**
- THORChain pools are isolated AMMs that arb bots connect to CEX. During fast moves, the arb correction lag creates a measurable price transmission delay.
- Pull hourly data during crash windows (5-min if needed)
- Compare THORChain ETH price (from depths endpoint) vs DefiLlama/yfinance ETH price
- Measure the lag between CEX price move and THORChain pool price correction
- Does the correction lag increase during extreme stress? (arb capital exhaustion)

**Output:** `data/arb_analysis.csv`, `data/price_dislocation.csv`

### Step 5: Short-Timeframe Dynamics (Hourly / Weekly)

The daily macro view answers "what happened per crash." Shorter timeframes answer "how did it unfold" and "what does normal look like."

**5a. Hourly flow anatomy of crash days**

For the top 10 liquidation spike days (from dynamics phase), pull hourly swap data for ETH.ETH, BTC.BTC, ETH.USDC:

- When within the day do directional flows shift? Does selling concentrate in a specific window (US open, Asia close)?
- Does the arb share spike precede or follow the flow direction shift?
- How fast does the BTC→ETH rotation pattern emerge? Hours before the crash day, or only after the initial drop?
- Compare THORChain hourly ETH price (from depths endpoint) against hourly CEX price — measure arb correction lag in real time

Pull: `/history/swaps?pool={pool}&interval=hour&count=168` (7 days centered on each spike day) × 3 pools × 10 events = 30 calls. Plus depths for price comparison.

**5b. Weekly rhythm in normal markets**

Pull 4 months of hourly data during calm periods (e.g., mid-2023 recovery, mid-2024 bull) to establish baseline:

- Is there a weekly cycle in flow direction? (e.g., weekend risk-off, Monday risk-on)
- Arb share by day-of-week and hour-of-day — when are arbs most/least active?
- Do organic (non-arb) flows cluster at specific times?
- Volume profile: what does "normal" look like so we can define "abnormal"

**5c. 1-week flow momentum**

At daily resolution across the full dataset:
- 7-day rolling net flow for ETH.ETH and BTC.BTC
- Does 1-week flow momentum predict next-week price return? (the simplest trend-following test)
- Does 1-week flow reversal (sustained buying → sudden selling) precede crash onset?
- Compare weekly flow momentum vs weekly OI changes (from dynamics phase) — do they carry independent information?

**Output:** `data/hourly_crash_flows.csv`, `data/hourly_baseline_flows.csv`, `data/weekly_momentum.csv`

### Step 6: Synthesis

Connect THORChain flow findings to the broader research arc:

mev/directory.md

- Do cross-chain flows tell a different story than on-chain DeFi (from prior phases)?
- Does the BTC→ETH rotation pattern hold across all crashes or just the two probed?
- Can THORChain flow direction + arb share improve the OI signal precision (30% → higher)?
- Is there actionable cross-chain arb signal during stress?
- Do hourly flow patterns reveal transmission timing that daily data hides?
- Is there a tradeable weekly or intraday rhythm in cross-chain flows?

**Output:** `findings.md`

## Infrastructure

- Python 3.14.3 in venv at `~/nous/.venv`
- requests for Midgard API calls
- pandas for data manipulation
- Existing data: `~/nous/memories/mev/data/eth_price.csv`, `~/nous/memories/mev/links/data/tradfi_daily.csv`
- No API keys needed

## Pagination

Midgard max 400 intervals per call. For daily data over 1,490 days:
- Call 1: `from=1646092800&count=400` (Mar 2022 → Apr 2023)
- Call 2: `from=1680652800&count=400` (Apr 2023 → May 2024)
- Call 3: `from=1715126400&count=400` (May 2024 → Jun 2025)
- Call 4: `from=1749686400&count=400` (Jun 2025 → Mar 2026)

~4 calls × 20 pools = 80 API calls for swaps. Plus 4 × 4 for major pool depths + 4 for TVL = 100 total.

Step 5 adds: 30 calls (hourly crash windows) + 12 calls (hourly baseline) + 30 calls (depths for price comparison) = ~72 calls.

Grand total: ~172 API calls. Well within rate limits.

## Connection to Prior Work

| Phase | What it produced | What this phase uses |
|-------|-----------------|---------------------|
| Flow | 37h OI signal, position heterogeneity principle | OI signal for conjunction test with THORChain flows |
| Dynamics | Recharge cycle, crash taxonomy, 65K liquidation events | Crash epoch dates, liquidation spike days for flow comparison |
| Links | VIX regime, amplification model, ETH price data, TradFi data | Price baseline, VIX for regime conditioning, crash residuals |
| **Cross-chain** (this) | Directional flow signatures, arb activity as stress indicator | — |
