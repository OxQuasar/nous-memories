# Links — Execution Plan

## Question

What connects external events to DeFi liquidation cascades? Does DeFi amplify or dampen crashes? What's the transmission path from macro event → CEX price action → on-chain response?

The prior phases mapped the machine in isolation. This phase connects it to the world it operates in.

## Data Sources

### TradFi (all free, daily, 2022-2026)

| Ticker | Data | Source | Why |
|--------|------|--------|-----|
| `^GSPC` | S&P 500 | yfinance | Equity risk sentiment |
| `^VIX` | CBOE Volatility Index | yfinance | Fear gauge, regime indicator |
| `JPY=X` | USD/JPY | yfinance | Yen carry proxy (2024 crash catalyst) |
| `DX-Y.NYB` | US Dollar Index (DXY) | yfinance | Dollar strength, inverse crypto correlation |
| `^TNX` | 10Y Treasury Yield | yfinance | Rate environment |
| `GC=F` | Gold futures | yfinance | Safe haven flows |
| Fed Funds Rate | | FRED (`FEDFUNDS`) | Monetary policy |
| 2Y-10Y Spread | | FRED (`T10Y2Y`) | Recession signal |
| CPI YoY | | FRED (`CPIAUCSL`) | Inflation |

### Crypto (existing + new)

| Data | Source | Status |
|------|--------|--------|
| ETH daily price | `../data/eth_price.csv` | ✅ Exists |
| Aave liquidation events | `../dynamics/data/liquidations_full.csv` | ✅ Exists (65,382 events) |
| Aave borrow/TVL | `../dynamics/data/protocol_metrics_daily.csv` | ✅ Exists |
| Exchange flows | `../dynamics/data/daily_flows.csv` | ✅ Exists |
| BTC daily price | yfinance `BTC-USD` | New pull |
| ETH/BTC ratio | Derived | Computed |
| THORChain swap volume per pool | Midgard API (free, no key) | New pull |
| THORChain pool depths | Midgard API | New pull |

## Execution

### Step 1: Data Pull
Pull all TradFi tickers at daily resolution for 2022-01-01 → 2026-03-19. Pull THORChain daily swap history per pool for the same range. Merge with existing ETH price data into a single aligned dataframe.

**TradFi:** yfinance + FRED → `data/tradfi_daily.csv` — date, eth_price, sp500, vix, usdjpy, dxy, tnx, gold, btc, fed_funds, yield_spread

**THORChain:** Midgard `/history/swaps?pool={pool}&interval=day` for key pools. Pagination via `from`/`count` (max 400 per call).

Pools to pull: BTC.BTC, ETH.ETH, AVAX.AVAX, BSC.BNB, DOGE.DOGE, GAIA.ATOM, plus stablecoin pools (AVAX.USDC, AVAX.USDT, ETH.USDC, ETH.USDT, BASE.USDC). Also `/history/tvl` for aggregate liquidity.

Per pool per day: `toAssetVolumeUSD` (buying the asset), `toRuneVolumeUSD` (selling the asset), `totalVolumeUSD`, `totalCount`, `averageSlip`.

Derived metrics:
- **Net flow direction** per pool: `toAssetVolume - toRuneVolume` (positive = net buying, negative = net selling)
- **Flight-to-safety ratio**: stablecoin pool volume / total volume (high = panic)
- **BTC/ETH rotation**: BTC pool buy volume vs ETH pool buy volume (divergence = rotation)
- **Slip as stress indicator**: rising average slip = liquidity thinning

**Output:** `data/tradfi_daily.csv`, `data/thorchain_daily.csv`

### Step 2: Correlation Matrix
Compute rolling and epoch-level correlations between ETH and each TradFi variable.

**Tests:**
- Full-period Pearson correlation (baseline)
- 30-day rolling correlation (regime shifts — when does ETH decouple from equities?)
- Per-epoch correlation (does the ETH/S&P relationship change during crashes vs bulls?)
- Lead/lag cross-correlation at daily resolution, ±5 days (does VIX lead ETH, or follow?)

**Output:** `data/correlation_matrix.csv`, `data/rolling_correlations.csv`

### Step 3: Crash Event Reconstruction
For each of the 6 crash epochs, reconstruct the causal timeline:

1. **What moved first?** Compare daily returns: did USD/JPY, S&P, VIX, or ETH move first?
2. **Transmission lag.** Cross-correlate ETH daily returns with each TradFi variable within the crash window. Measure lead/lag in days.
3. **DeFi response lag.** From dynamics phase: how many days after the price drop onset did liquidation spikes occur? (Already measured: 8-49 days to first >$10M spike day.)
4. **Cross-chain flow direction.** Per crash: did THORChain flows go ETH→stables (flight to safety), ETH→BTC (rotation), or BTC→ETH (buying the dip)? Does the flight-to-safety ratio spike before, during, or after the price drop? Does the flow direction differ by crash catalyst (macro vs crypto-native)?
5. **Amplification test.** On spike liquidation days, did ETH drop more than S&P/BTC would predict? Regress ETH return on S&P return + BTC return for non-spike days, then check residuals on spike days. Positive residual on spike days = DeFi amplification.

**Key crash timelines to reconstruct:**
- **2022 Jun (Terra/3AC):** Was the stETH depeg cause or effect? Did Terra's UST collapse → stETH selling → ETH cascade, or did ETH drop independently?
- **2022 Nov (FTX):** CEX-specific contagion. Did on-chain metrics lead or lag FTX insolvency signals?
- **2024 Aug (Yen carry):** USD/JPY unwound → Nikkei crashed → global equities sold → ETH dropped → DeFi liquidations. What was the hourly sequence?
- **2025 Jan-Apr crash:** What triggered the largest drawdown in the dataset (-64%)? Macro or crypto-native?
- **2026 Jan-Feb crash:** Most recent, connects to position/correlation phase findings.

**Output:** `data/crash_timelines.csv`, `findings_crashes.md`

### Step 4: Regime Analysis
Does the ETH-TradFi relationship change structurally over time?

**Tests:**
- **Correlation regime shifts.** When does ETH/S&P 30-day rolling correlation break above 0.6 (highly coupled) or below 0.2 (decoupled)?
- **VIX threshold.** At what VIX level does the correlation regime shift? (Hypothesis: high VIX = everything correlates, low VIX = crypto decouples.)
- **Rate environment.** Does ETH behave differently in rate-hiking vs rate-cutting vs rate-hold periods?
- **DeFi leverage × macro sensitivity.** When Aave borrow is high (reloaded system), is ETH more sensitive to macro shocks? Interact borrow level with S&P beta.
- **Cross-chain flow regime.** Does THORChain flow composition (flight-to-safety ratio, BTC/ETH rotation) predict which correlation regime you're in? High stablecoin flow share = risk-off regime = high ETH/S&P correlation?

**Output:** `data/regime_analysis.csv`, `findings_regimes.md`

### Step 5: Amplification Quantification
The core question: does DeFi make crashes worse?

**Method:**
- Construct a simple model: `ETH_return = α + β₁(SP500_return) + β₂(BTC_return) + ε`
- Train on non-crash days. Predict ETH return on crash days.
- Measure residuals on liquidation spike days specifically.
- If residuals are systematically negative on spike days (ETH drops more than the model predicts), DeFi liquidation selling is amplifying the crash.
- Quantify: how many basis points of extra decline per $100M of liquidation volume?

**Alternative:** Compare ETH drawdown in weeks with high DeFi liquidation volume vs weeks with similar price decline but low liquidation volume. Control for magnitude.

**Output:** `data/amplification_test.csv`, section in findings

## Infrastructure

**New dependency:** `yfinance` Python library. Install via `pip install yfinance`.

**FRED API:** Free key from https://fred.stlouisfed.org/docs/api/api_key.html. Or use `fredapi` Python package. Alternatively, FRED data is available via CSV download without API.

**THORChain Midgard API:** `https://midgard.ninerealms.com/v2`. Free, no API key. Rate limit ~100 req/min. Intervals: 5min, hour, day, week, month. Max 400 intervals per call, pagination via `from`/`count`. Full chain history available (post hard-fork block 4786560). 44 active pools.

Everything else reuses existing infrastructure and data from prior phases.

## What This Would Produce

A model of how the DeFi leverage system connects to the broader financial system:
- **Correlation regimes** — when crypto is its own thing vs when it moves with equities
- **Transmission lags** — how fast macro events reach on-chain liquidations (hours? days?)
- **Amplification magnitude** — does $X of DeFi liquidation produce Y basis points of extra decline?
- **Crash-specific narratives** — the actual causal chain for each major episode, not just "Terra happened"
- **Cross-chain flow signatures** — where money goes during crashes (safety, rotation, exit) and whether flow direction differs by catalyst type

## Connection to Prior Work

| Phase | What it produced | What this phase uses |
|-------|-----------------|---------------------|
| Flow | Liquidation episode dates, perp→lending 37h lead time | Episode framework, timing benchmarks |
| Position | Real/phantom decomposition, conditional fuel map | Position topology context for amplification test |
| Correlation | CAPO oracle architecture, March 10 forensics | Oracle risk as confound vs market risk |
| Dynamics | Recharge cycle, crash/recovery asymmetry, liquidation event data | Liquidation spike days, borrow levels, epoch definitions |
| **Links** (this) | How external events trigger and interact with the DeFi system | — |

## Execution Status

| Step | Status | Output | Notes |
|------|--------|--------|-------|
| 1a: TradFi data pull | ✅ Complete | `data/tradfi_daily.csv` (1539 rows) | yfinance + FRED, verified against ETH source |
| 1b: THORChain data pull | ⏭ Skipped | — | Core questions answered without it. Would add flow direction color. |
| 2: Correlation matrix | ✅ Complete | `data/correlation_matrix.csv`, `data/rolling_correlations.csv` | Full-period, rolling, regime-split, lead/lag, borrow-growth null |
| 3: Crash reconstruction | ✅ Complete (merged with 5) | `data/crash_residuals.csv` | Per-crash timelines, catalyst classification, 2025 monthly decomposition |
| 4: Regime analysis | ⏭ Skipped | — | VIX regime finding from Step 2 answers core question. Rate regime time-confounded. |
| 5: Amplification quantification | ✅ Complete (merged with 3) | `findings.md` | Three-mode framework, amplification coefficients, causal ordering |

### Artifacts produced
- **Scripts:** `pull_tradfi.py`, `correlations.py`, `amplification.py`
- **Data:** `tradfi_daily.csv`, `correlation_matrix.csv`, `rolling_correlations.csv`, `crash_residuals.csv`
- **Documents:** `findings.md` (synthesis), `exploration-log.md` (4 iterations), `signals-synthesis.md` (signal ranking + composite)

### Core questions answered
1. **"Does DeFi amplify or dampen crashes?"** — Amplifies. ~100 bps per 100 Aave liquidation events during ramp phase, concave. Three modes: ramp amplification, recovery suppression, exhaustion reversal.
2. **"What's the transmission path?"** — Sub-daily macro→crypto (no daily lead/lag). 5-7 day DeFi cascade timescale (partial correlation doubles from 1d to 7d). Aave lending cascades are never the first mover.
3. **"What connects external events to DeFi cascades?"** — VIX determines coupling regime (monotonic Q1:0.23→Q4:0.51). Crash-chaining prevents recovery, making acute amplification practically permanent.
