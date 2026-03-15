# Henry Architecture

> Crypto trading system with DSP-based signal processing, backtesting, and live execution.
> Go implementation. Module: `github.com/whiteher0n/henry`. Go 1.23.

---

## 1. Design Principles

1. **Simulation parity.** Backtest and live modes share indicator computation and strategy code. Only data source differs.
2. **Manager pattern.** Each signal processing subsystem (Goertzel, DWT, IIR, VolumeProfile) uses a Manager struct separating init/config/step.
3. **Strategy pluggability.** Registry + factory pattern. Strategies declare module requirements; unused modules are not initialized.
4. **Temporal correctness.** All times UTC. No lookahead — `IndicatorHistory` enforces past-only access. `SimState` controls time progression.
5. **Memory-conscious.** Chunked data loading, periodic trimming of old data/indicators, GC after each backtest period.

---

## 2. Directory Layout

```
henry/
├── main.go                 # Entry: log init → DB init → cmd.Execute()
├── cmd/                    # Cobra CLI commands
│   ├── root.go             # Root command
│   ├── callandor.go        # `callandor` — run sim (hardcoded dates, dev tool)
│   ├── iterate.go          # `backtest-strategy`, `iterate`, `sweep`, `status`
│   ├── datachannel.go      # `datachannel` — live WS data scraping
│   ├── tarvalon.go         # `tarvalon` — live trade execution
│   ├── trismegistus.go     # `trismegistus` — 8h trend detection + Markov
│   └── database.go         # `database` — table creation
│
├── callandor/              # Core backtesting engine
│   ├── callandor.go        # Callandor struct, SimState, Step(), main loop
│   ├── indicators.go       # ComputeIndicators(), all indicator computation
│   ├── sentinel.go         # Sentinel orchestrator, ExecutionData, TradeLog
│   ├── definition.go       # Legacy Strategy/TradeForm/JPForm interfaces
│   ├── jpow.go             # JPow — legacy trend strategy (swing highs/lows)
│   ├── swing_v2.go         # SwingStrategy — legacy form-based strategy
│   ├── elevator.go         # ElevatorUp/Down forms (legacy)
│   ├── forms.go            # Range trade forms (legacy)
│   ├── forms_jp.go         # JPow-specific forms
│   ├── exits_jp.go         # JPow exit logic
│   ├── trademgr.go         # TradeMgr — trade execution, TradeRequest
│   ├── pm.go               # FuturesPM — position/account simulator
│   ├── regime.go           # RegimeClassifier — trend/vol regime detection
│   ├── analysis.go         # TradeAnalyzer — P&L, win rate, bucketing
│   ├── goertzel_manager.go # GoertzelManager — multi-freq filter coordination
│   ├── dwt_manager.go      # DWTManager — wavelet decomposition filters
│   ├── iir_manager.go      # IIRManager — Bessel trend smoothing filters
│   ├── absorption.go       # AbsorptionDetector — OB absorption signals
│   ├── large_trade.go      # LargeTradeDetector — volume cluster detection
│   ├── funding.go          # Funding rate processing
│   ├── calcs.go            # TrendAndVolatility, NormalizedTrendAndVolatility
│   ├── plotter.go          # HTML chart generation (ECharts)
│   ├── context_writer.go   # Backtest result serialization
│   ├── montecarlo/         # Monte Carlo simulation
│   ├── iteration/          # Test period generation, parameter sweeps
│   └── strategy/           # New strategy framework
│       ├── interface.go    # Strategy interface, StrategyContext, TradeState, Signal
│       ├── registry.go     # GlobalRegistry — factory pattern registration
│       ├── adapter.go      # SentinelAdapter — bridges new strategies to Sentinel
│       ├── feature_capture.go  # Pre-entry indicator buffer
│       ├── trade_capture.go    # Trade CSV logging + P&L calculation
│       ├── market_logger.go    # Market data logging helper
│       └── strategies/     # Strategy implementations (self-register via init())
│           ├── goertzel_cycle.go
│           ├── goertzel_cycle_regime.go
│           ├── goertzel_cycle_regime_8h.go
│           ├── goertzel_cycle_tris_pure.go
│           ├── knn_memory.go
│           ├── sfp.go
│           └── datalogger.go
│
├── dsp/                    # Digital signal processing library
│   ├── indicatorts.go      # Indicator struct (116 fields), IndicatorTs, RangeStats
│   ├── goertzel.go         # Goertzel algorithm, GoertzelSignal, GoertzelConfig
│   ├── dwt.go              # DWT — discrete wavelet transform
│   ├── swt.go              # SWT — stationary wavelet transform
│   ├── iir.go              # IIRFilter (Bessel, Direct-Form II)
│   ├── fir.go              # FIRFilter (MA, windowed-sinc)
│   ├── band.go             # FIR bandpass design
│   ├── filter.go           # Filter interface (FilterArray, Step, Reset)
│   ├── normalize.go        # Normalizer — running z-score
│   ├── demean.go           # Demeaner — running mean subtraction
│   ├── pca.go              # OLS regression (OLSRotate)
│   ├── detection.go        # Activity detection (spike/peak finding)
│   ├── signals.go          # Signal generators (chirp, cos)
│   ├── timeseries.go       # TsPoint, Timeseries, TradeSecondTs, OrderbookTs, FundingTs
│   └── plot.go             # DSP plotting helpers
│
├── anatolia/               # Volume profile engine
│   ├── volprofile.go       # Volprofile — rolling VP with bins, stats (POC/VAH/VAL)
│   └── volprofile_manager.go  # VolumeProfileManager — multi-timeframe VP
│
├── trismegistus/           # 8h trend detection + regime classification
│   ├── trismegistus.go     # Core struct, HistoryPoint
│   ├── algo.go             # TrisAlgo — Goertzel-OLS hybrid
│   ├── run.go              # RunTrismegistus entry point
│   ├── prod.go             # TrisProd — production coordinator
│   ├── regime.go           # Regime labeling (trend/vol/logret)
│   ├── markov.go           # MarkovModel — regime transition probabilities
│   ├── markov_trend.go     # MarkovTrendModel — bull/bear prediction
│   └── volume_accumulator.go  # Rolling volume statistics
│
├── api/                    # Exchange API layer
│   ├── exchange_api.go     # ExchangeApi interface, factory, WS runners
│   ├── types.go            # WsTradeEvent, AggTradeSecond, LocalOrderBook
│   ├── binancef_api.go     # Binance futures implementation
│   ├── binance_api.go      # Binance spot implementation
│   ├── bitunixf_*.go       # Bitunix futures
│   ├── mexc_api.go         # MEXC implementation
│   ├── ccxt_api.go         # CCXT-based generic implementation
│   ├── pricescraper.go     # WS data pipeline runners
│   ├── tradestation.go     # TradeStation API (gold futures)
│   └── mainnet.go          # On-chain (ETH/DeFi)
│
├── database/               # PostgreSQL (TimescaleDB) data layer
│   ├── loader.go           # Loader — trades/OB/funding for backtests
│   ├── chunked_loader.go   # ChunkedDataLoader — weekly chunks with prefetch
│   ├── dao/                # KlineDAO, DepthDAO, TradeDAO
│   └── models/             # AggTrades, Depth, Kline, Funding, Liquidation
│
├── tarvalon/               # Live trading engine
│   ├── amerlyh.go          # Ameryln — coordinator
│   ├── blue.go             # BlueAjah — data processing (VP, SWT)
│   ├── white.go            # WhiteAjah — strategy execution
│   ├── green.go            # GreenAjah — trade execution
│   └── brown.go            # BrownAjah — visualization/dashboard
│
├── display/                # Live display HTTP server for Callandor tests (WebSocket chart)
├── socket/                 # WebSocket pub/sub for inter-component data flow
├── config/                 # Token/Dex/Blockchain config, context keys, logging
├── utils/                  # Array ops, math, time formatting, symbol utils
├── context/                # Session state, backtest results, insights
└── html_results/           # Backtest output HTML files
```

---

## 3. Command Structure

```
henry
├── callandor                # Fixed-date simulation (dev tool)
├── backtest-strategy        # Primary backtest command
│   -s / --strategy          # Strategy name from registry
│   --start / --end          # Date range (YYYY-MM-DD)
│   -p / --periods           # Week number within months (1-4)
│   -m / --months            # Number of months to test
│   -w / --workers           # Parallel workers (default 4)
│   --live                   # HTTP port for live display
│   --symbol                 # Trading pair (default BTC/USDT)
├── iterate                  # Multi-period improvement iteration
├── sweep                    # Parameter sweep optimization
├── status                   # Show iteration status + registered strategies
├── datachannel              # Live WS data scraping
│   --channel                # futures|spot|gold|firepoker
│   -s / --symbol            # Symbol (BASE/QUOTE)
│   -e / --exchange          # Exchange (binancef, binance, etc.)
├── tarvalon                 # Live trading execution
├── trismegistus             # 8h trend detection + Markov training
│   -m / --markov            # Train Markov model
│   -p / --predict           # Evaluate predictions
├── database                 # Table creation (TimescaleDB hypertables)
```

---

## 4. Key Types & Interfaces

### 4.1 Core Engine (`callandor/`)

| Type | File | Purpose |
|------|------|---------|
| `Callandor` | callandor.go | Top-level sim. Owns SimState, all managers, Sentinel, chunked loader |
| `SimState` | callandor.go | Time progression: `Ts`, `TradeIndex`, `OBIndex`, `StartTs`, `EndTs`, `StepInterval`. Methods: `Advance()`, `IsDone()`, `GetPeriodTrades()`, `GetCurrentOrderbook()` |
| `Sentinel` | sentinel.go | Strategy orchestrator. Owns `TradeLog []ExecutionData`, `Strategy JPow` (legacy), `StrategyAdapter *strategy.SentinelAdapter` (new), `TradeManager *TradeMgr`, `Analyzer *TradeAnalyzer` |
| `ExecutionData` | sentinel.go | One TradeLog row: timestamp, price, all trends, regimes, exposure, account value, strategy details |
| `FuturesPM` | pm.go | Futures position manager: cash, margin, leverage, fee, liquidation. Core method: `SetExposure(exposure, executionPrice)` |
| `TradeMgr` | trademgr.go | Trade execution: receives `TradeRequest`s, manages blackout window, delegates to `FuturesPM` |
| `TradeRequest` | trademgr.go | `Timestamp`, `Exposure`, `Reason`, `EMode`, `EntryPrice` |
| `RegimeClassifier` | regime.go | Bull/Bear/Flat/Transition × High/Normal volatility |
| `TradeAnalyzer` | analysis.go | Post-run analysis: trades bucketed by direction/trend/regime |
| `JPow` | jpow.go | Legacy strategy: swing high/low detection → trend state |

### 4.2 Strategy Framework (`callandor/strategy/`)

| Type | File | Purpose |
|------|------|---------|
| `Strategy` | interface.go | **Interface**: `Name()`, `Description()`, `Init(*StrategyContext)`, `OnTick(*StrategyContext) []Signal`, `OnTradeExecuted(*TradeResult)`, `Reset()`, `Parameters()`, `SetParameters()` |
| `StopLossProvider` | interface.go | Optional interface: `GetCurrentStopLoss() float64` |
| `StrategyContext` | interface.go | Tick context: timestamp, price, exposure, `*dsp.Indicator`, `*IndicatorHistory`, VP stats (12h/24h/48h/96h), Goertzel signals (1h/2h/8h/12h/24h), trends (4h-96h), volatility, helper functions |
| `Signal` | interface.go | Strategy output: `Timestamp`, `Exposure` (-1 to 1), `Reason`, `IsEntry`. Method: `Direction() int` |
| `TradeState` | interface.go | Active trade: `EntryPrice`, `Direction`, `HighWater`, `LowWater`. Methods: `CalcPnL()`, `CalcExtremes()`, `UpdateWaterMarks()` |
| `ModuleRequirements` | interface.go | Declares expensive modules: `VolumeProfile`, `Goertzel`, `DWT`, `IIR`, `Trismegistus` bools + custom configs |
| `VolumeProfileStats` | interface.go | `POC`, `VAH`, `VAL`, `VAHE`, `VALE`, `Width`. Method: `DistancesFrom(price)` |
| `IndicatorHistory` | interface.go | Lookahead-safe: `GetPast(offset)` only allows negative offsets |
| `TradeResult` | interface.go | Completed trade: entry/exit ts/price, P&L, direction, reasons, water marks |
| `SentinelAdapter` | adapter.go | Bridges `Strategy` to `Sentinel`: builds context, processes signals, manages trade capture |
| `Registry` | registry.go | `GlobalRegistry` — `map[string]StrategyFactory`. Convenience: `Register()`, `Create()`, `List()` |
| `TradeCapture` | trade_capture.go | CSV logging of trade lifecycle. `TradeFeePerSide=0.00045`, `DefaultLeverage=2` |

### 4.3 DSP Package (`dsp/`)

| Type | File | Purpose |
|------|------|---------|
| `Indicator` | indicatorts.go | **116 top-level fields** (~220 scalar values with nested structs expanded): Goertzel signals, volume/CVD, OB ratios, trends (1h-96h), OLS + realized volatility, regime, Tris predictions |
| `IndicatorTs` | indicatorts.go | Time series of `Indicator`. Methods: `Append()`, `Trim()`, `GetLast()`, `GetPast(seconds)` |
| `Goertzel` | goertzel.go | Sliding DFT at single frequency. Window = 1 period. Output: magnitude, phase, real, imag |
| `GoertzelSignal` | goertzel.go | `Timestamp`, `Price`, `Magnitude`, `Phase`, `Real`, `Imag` |
| `GoertzelConfig` | goertzel.go | `Key`, `PeriodSeconds`, `NormalizerWindow`, `SampleRate`, `MaxHistory` |
| `DWT` | dwt.go | Discrete wavelet transform: multi-level decomposition with FIR high/low pass |
| `IIRFilter` | iir.go | Direct-Form II transposed. Bessel coefficients for 1h/4h/8h cutoffs |
| `FIRFilter` | fir.go | Finite impulse response (MA, windowed-sinc bandpass) |
| `Filter` | filter.go | **Interface**: `FilterArray([]float64)`, `Step(float64)`, `Reset()` |
| `Normalizer` | normalize.go | Running z-score: `(x - mean) / std` over fixed window |
| `Demeaner` | demean.go | Running mean subtraction over fixed window |
| `RangeStats` | indicatorts.go | VP range levels: Vahe/Vah/UpperPoc/LowerPoc/VaMid/Val/Vale |
| `Point` | pca.go | `{X, Y}` for OLS. `OLSRotate()` → intercept, mean, slope, stddev, quality, r² |
| `Timeseries` | timeseries.go | Generic `[]TsPoint` with MovingAverage, Cumsum, Difference, binary search |

### 4.4 Volume Profile (`anatolia/`)

| Type | File | Purpose |
|------|------|---------|
| `Volprofile` | volprofile.go | Rolling VP: bins, VWAP, buyer/seller separation, OB stats, realized volatility |
| `VolumeProfileManager` | volprofile_manager.go | Multi-timeframe VP (1s→96h). Methods: `InitAll()`, `RollAll()`, `FillAllRangeStats()` |
| `VPConfig` | volprofile_manager.go | `Key`, `Period` (seconds), `NeedsOrderbook` |

### 4.5 Exchange API (`api/`)

| Type | File | Purpose |
|------|------|---------|
| `ExchangeApi` | exchange_api.go | **Interface**: GetKline, GetPrice, GetOrderBookSnapshot, MarketTrade, LimitTrade, WS channels |
| `CexName` | exchange_api.go | Enum: Binance, BinanceFutures, BitunixFutures, OKX, MEXC, Tradestation |
| `AggTradeSecond` | types.go | 1-second aggregated trades: buyer/seller price-levels, count, start/end price |
| `LocalOrderBook` | types.go | Sorted bids/asks with `OBPriceLevel` (Price, Quantity) |

### 4.6 Trismegistus (`trismegistus/`)

| Type | File | Purpose |
|------|------|---------|
| `Trismegistus` | trismegistus.go | Hybrid Goertzel-OLS: 8h cycle phase → segment boundaries → OLS fit → labels |
| `TrisProd` | prod.go | Production coordinator: steps core algo, maintains regime history, Markov prediction |
| `HistoryPoint` | trismegistus.go | Price, slope, log return, volatility, volume, labels (trend/vol/logret) |
| `MarkovTrendModel` | markov_trend.go | Transition probabilities: regime → bull/bear prediction |
| `TrisAlgo` | algo.go | Core DSP: Goertzel filter + OLS line fitting |

### 4.7 Tarvalon — Live Trading (`tarvalon/`)

| Type | File | Purpose |
|------|------|---------|
| `Ameryln` | amerlyh.go | Coordinator — starts Blue/White/Green/Brown via channels |
| `BlueAjah` | blue.go | Data processing: receives WS data, computes VPs/SWT |
| `WhiteAjah` | white.go | Strategy: runs swing strategy, emits trade proposals |
| `GreenAjah` | green.go | Execution: receives proposals, executes via exchange API |
| `BrownAjah` | brown.go | Visualization: HTTP dashboard for live monitoring |

---

## 5. Data Flow

### 5.1 Backtest Flow

```
cmd/iterate.go
  ├── strategy.Create(name)          # Factory from GlobalRegistry
  └── CallandorMainWithOutput(...)
        │
        ├── database.LoadDataChunked(...)     # Weekly chunks, prefetch
        │     └── Loader { Trades, Orderbook, Funding }
        │
        ├── NewCallandor(...)                 # Init managers based on ModuleRequirements
        │     ├── VolumeProfileManager        (if VP=true)
        │     ├── GoertzelManager             (if Goertzel=true)
        │     ├── DWTManager                  (if DWT=true)
        │     ├── IIRManager                  (if IIR=true)
        │     ├── TrisProd                    (if Tris=true)
        │     ├── Sentinel { JPow, TradeMgr, Analyzer }
        │     └── AbsorptionDetector, LargeTradeDetector, RegimeClassifier
        │
        ├── PreWarmTris()                     # 7d warmup at 1-min steps
        ├── VPManager.InitAll(loader, ts)     # Bulk-load VP histories
        │
        └── Main Loop (1s steps):
              ├── ensureDataLoaded()          # Chunked loading + trim old data
              ├── Step()
              │   ├── SimState.Advance()
              │   ├── SearchTrades/OB         # Advance indices to current Ts
              │   ├── RollVolprofiles()
              │   ├── ComputeIndicators()     # → all 116 indicator fields
              │   │   ├── computeVolumeIndicators()
              │   │   ├── computeOrderbookIndicators()
              │   │   ├── computeOrderflowIndicators()
              │   │   ├── computeBigOrderIndicators()
              │   │   ├── computeAbsorptionIndicators()
              │   │   ├── computeLargeTradeIndicators()
              │   │   ├── computeTrendIndicators()      # OLS slopes 1h-96h
              │   │   ├── computeCycleIndicators()      # Goertzel
              │   │   ├── computeRegimeIndicators()
              │   │   └── computeTrismegistusIndicators()
              │   │
              │   └── Sentinel.Step() or WarmupStep()
              │       ├── BuildContext()      # SentinelAdapter → StrategyContext
              │       ├── Strategy.OnTick()   # → []Signal
              │       ├── ProcessSignal()     # Signal → TradeRequest + TradeResult
              │       ├── TradeMgr.Step()     # Execute via FuturesPM
              │       └── Append(ExecutionData)
              │
              ├── Warmup → normal transition at actualStartTs
              └── Periodic trim (every hour): indicators, trade log, tris history

  Post-simulation:
  ├── PrintAnalysis()        # Trade stats, reconciliation
  └── Plot HTML              # Sentinel chart + Callandor indicator chart
```

### 5.2 Live Trading Flow

```
cmd/tarvalon.go
  └── Ameryln.Convene()
        ├── api.OrderbookWsMain() ──→ BlueAjah
        ├── api.AggTradesWSMain() ──→     │
        │                                 ├── Compute VPs, SWT
        │                                 └── Signal WhiteAjah
        │
        ├── WhiteAjah ──→ Run SwingStrategy ──→ TradeRequest ──→ GreenAjah
        ├── GreenAjah ──→ Execute via ExchangeApi
        └── BrownAjah ──→ HTTP dashboard
```

### 5.3 Data Ingestion Flow

```
cmd/datachannel.go
  └── datachannel()
        ├── NewExchangeApi()              # Factory: binancef, binance, etc.
        ├── LaunchSocketServer()          # WebSocket pub/sub
        └── futuresChannelHandle()
              ├── go OrderbookWsMain()    # OB snapshots → DB + socket
              ├── go AggTradesWSMain()    # Trades → AggTradeSecond → DB + socket
              ├── go KlineWSMain()        # 1m candles → DB + socket
              └── go LiquidationWSMain()  # Liquidations → DB
```

---

## 6. Strategy Registration & Lifecycle

### Registration (compile-time via init())

```go
// callandor/strategy/strategies/goertzel_cycle.go
func init() {
    strategy.Register("goertzel_cycle", func() strategy.Strategy {
        return NewGoertzelCycleStrategy()
    }, strategy.StrategyMetadata{
        Name:    "goertzel_cycle",
        Modules: strategy.ModuleRequirements{
            VolumeProfile: true,
            Goertzel:      true,
        },
    })
}
```

**Import trigger**: `cmd/iterate.go` has `_ "henry/callandor/strategy/strategies"` — blank import runs all `init()`.

### Registered Strategies

| Name | Description |
|------|-------------|
| `goertzel_cycle` | Phase-based entries from 12h Goertzel, dynamic stop/TP |
| `goertzel_cycle_regime` | + 24h/12h regime filtering |
| `goertzel_cycle_regime_8h` | + 8h regime variant |
| `goertzel_cycle_tris_pure` | Trismegistus-only regime entries |
| `knn_memory` | KNN pattern matching with memory |
| `sfp` | Swing failure pattern detection |
| `datalogger` | No trades — pure data logging |

### Lifecycle

1. `strategy.Create(name)` → factory → fresh Strategy instance
2. `Sentinel.SetStrategy(strat)` → creates `SentinelAdapter`, sets `UseNewStrategy=true`
3. Each tick: `SentinelAdapter.BuildContext()` → `Strategy.OnTick(ctx)` → `[]Signal`
4. Signal processing: entry → `TradeState` populated; exit → `TradeResult` → `Strategy.OnTradeExecuted()` → `TradeAnalyzer.AddTrade()`

---

## 7. Manager Pattern

All signal processing subsystems share structural pattern:

```
Manager {
    configs []Config           // Declarative: what to compute
    instances map[string]*X    // Concrete: initialized processors
}

NewXManager(configs)           // Init all from configs
  .Get(key) *X                 // Access by key
  .StepAll(data, ts)           // Process one tick through all
```

| Manager | Config | Instance | Domain |
|---------|--------|----------|--------|
| `GoertzelManager` | `GoertzelConfig` | `Goertzel` + `Normalizer` | Multi-frequency sliding DFT |
| `DWTManager` | `DWTConfig` | `DWT` | Multi-level wavelet decomposition |
| `IIRManager` | `IIRConfig` | `IIRFilter` | Bessel low-pass smoothing |
| `VolumeProfileManager` | `VPConfig` | `Volprofile` | Multi-timeframe volume distribution |

---

## 8. Dual Strategy System

Two coexisting systems:

**Legacy** (`callandor/definition.go`):
- Interface: `Step(s *Sentinel) StrategyDetails`
- Concrete: `JPow` (trend detection) → `SwingStrategy` → `TradeForm` interface
- Forms: `ElevatorUp`, `ElevatorDown`, `RangeShort`, `RangeSpike`
- Active when `Sentinel.UseNewStrategy = false`
- Note: `Sentinel.Strategy` field is concrete type `JPow`, not an interface

**New** (`callandor/strategy/interface.go`):
- Interface: `OnTick(ctx *StrategyContext) []Signal`
- Registry + factory pattern
- Bridged via `SentinelAdapter`
- Active when `Sentinel.UseNewStrategy = true` (set by `SetStrategy()`)

Both flow through `TradeMgr.Step()` → `FuturesPM.SetExposure()`.

---

## 9. Key Constants

### Trading
```
DefaultLeverage     = 2
TradeFeePerSide     = 0.00045      # Hyperliquid fee
InitCash            = 1000.0
MaintenanceRate     = 0.0125
```

### Warmup & Data
```
indicatorWarmupHours = 24           # Indicator warmup before trading
trisStepIntervalMs   = 60000       # 1 min Trismegistus steps
trisWarmupHours      = 168         # 7 days Tris warmup
chunkLoadBufferMs    = 3_600_000   # 1 hour load buffer
TrimRetentionMs      = 604_800_000 # 7 days data retention
```

### Regime Classifier
```
TrendThreshold  = 0.6              # Bull/Bear boundary
VolThreshold    = 240.0            # High/Normal volatility
FlatThreshold   = 0.36             # 60% of TrendThreshold
```

### Default Goertzel Configs
```
8h:  period=28800s, normalizer=28800s
12h: period=43200s, normalizer=86400s
24h: period=86400s, normalizer=86400s
All at sampleRate=1Hz
```

### Default VP Configs
```
1s, 1m, 5m, 1h, 4h, 8h, 12h, 16h, 24h, 48h, 96h
All trade-only (NeedsOrderbook=false)
```

### IIR Bessel Cutoffs
```
1h:  fc = 1/3600
4h:  fc = 1/14400
8h:  fc = 1/28800
```

### Step Interval
```
StepInterval = 1000ms              # SimState field, set by caller
```

---

## 10. Key Invariants

1. **SimState.Ts is the single source of time.** All data access bounded by Ts. Trade/OB indices track position in sorted arrays.

2. **1-second step interval assumption.** TradeLog indices ≈ seconds. OLS downsampling factors (10, 30, 300) correspond to real-time intervals.

3. **Indicator struct is the data bus.** All computed values land in one `dsp.Indicator`. Strategies access via `StrategyContext.Indicator`.

4. **Volume profiles are the price source.** `VPManager.Price()` (from 1s VP) provides canonical price. No raw trade price used directly.

5. **Trend calculation via OLS.** All `Trend*h` values = OLS slope over downsampled price history. `NormalizedTrendAndVolatility` divides by mean price for price-invariance.

6. **Goertzel phase lag.** Output lags by one filter period. Strategies must forward-estimate: `estimatedPhase = laggedPhase + phaseVelocity * filterPeriodMs`.

7. **Memory management.** Strategies declare `IndicatorRetention` and `TrisHistoryRetention` to bound growth. Hourly trim in `Step()`.

8. **TradeCapture is the P&L source of truth.** `BuildTradeResult()` calculates leveraged P&L with fees. `FuturesPM` tracks account value (with reconciliation check).

9. **Chunked loading boundary.** `ensureDataLoaded()` triggers `AppendNext()` when Ts within 1 hour of loaded data end. Old data trimmed to 7-day retention.

10. **WarmupSamples offset.** Post-simulation plotting uses `skipSamples = WarmupSamples` to exclude warmup data from charts.

---

## 11. Database Schema (TimescaleDB)

Tables dynamically named by symbol + exchange (e.g., `btcusdt_binancef_aggtrades`), all converted to hypertables.

| Table Pattern | Time Column | Key Fields |
|---------------|-------------|------------|
| `*_aggtrades` | trade_time_end | price, quantity, trade_count, is_buyer_maker, start/end_price |
| `*_depth` | timestamp | ask, ask_quantity, bid, bid_quantity |
| `*_klines` | close_time | interval, OHLCV, quote_volume, active_buy_volume, trade_num |
| `*_liquidations` | time_end | price, quantity, is_buy, trade_count, total_volume |
| `*_funding` | timestamp | funding, markprice, lastprice |

---

## 12. External Dependencies

| Dependency | Purpose |
|------------|---------|
| `spf13/cobra` + `viper` | CLI + config |
| `sirupsen/logrus` | Structured logging |
| `uptrace/bun` + `lib/pq` | PostgreSQL ORM (TimescaleDB) |
| `gonum.org/v1/gonum` | Numerical computation |
| `whiteher0n/go-binance` | Binance WebSocket/REST (fork) |
| `ccxt/ccxt/go/v4` | Multi-exchange API |
| `gorilla/websocket` | WebSocket connections |
| `go-echarts/go-echarts` | HTML chart generation |
| `ethereum/go-ethereum` | Ethereum client (DeFi) |
| `chromedp/chromedp` | Headless browser (screenshot) |
