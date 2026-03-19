# Freya — Architecture Document

Multi-chain DEX arbitrage bot. Monitors on-chain liquidity pools, discovers cyclic arbitrage via graph search, executes profitable trades through a custom smart contract ("Atlas").

## Design

Block-driven event loop (~100ms poll). Each new block:
1. Update all pool states (reserves/prices) from on-chain
2. Rebuild in-memory graph edge weights
3. Search pre-computed cyclic paths for profitable arbitrage
4. If profitable and execution enabled, pick best route and submit tx

Pipeline: `StateMachine → Cartographer (Graph) → Pathfinder → Quantifier → Executor`

## Package Map

### `main.go`
Orchestrates the block loop, initializes subsystems, implements kill-switch and failsafe.

- `KILL_LIMIT=5` — abort after 5 consecutive failed txs
- `MAX_ITERATIONS=6` — trade size search depth
- `CURVE_CALLER_AMT`, `BLACKBOX_CALLER_AMT` — 100 ETH reference amounts for price quoting
- **Kill switch:** tracks consecutive failures, reduces `AmtInFailsafeFactor` (0.75→0.50→0.25→0.12). Fatal at 5. Resets after 50 clean blocks.
- **Nonce:** refreshes after each execution and every 50 blocks.

### `config/`
Reads 4 config sources via `spf13/viper`:

| Source | Content |
|---|---|
| `.env` | private key, arb contract address, sentry quoter address |
| `rpc.json` | per-network RPC endpoints, chain ID, ref token, gas multiplier, gas cap |
| `{net}Tokens.json` | token list (symbol, address, decimals, chainId) |
| `{net}Pairs.json` | pool definitions (address, router, pool, fee, tokens, dex name, type) |
| `{net}Dexes.json` | DEX router addresses and types |

Key types: `Config`, `TokenData`, `PairData`, `Dex`, `Env`.

### `core/`

**`init.go`** — CLI flags (`-net`, `-e`, `-l`, `-p`, `-o`, `-f`, `-s`). `Init()` loads config, creates 3 w3 clients + 2 go-web3 clients, returns `NetworkState{Blockchain, GasPrice, BlockNo}`.

**`client.go`** — Factory for `w3.Client` (multicall) and `ethclient.Client`. Note: both have `defer client.Close()` immediately after creation — fragile, works due to w3 connection lifecycle.

**`caller.go`** — On-chain read functions via `eth.CallFunc` / w3 multicalls:
- `QuoteUniV3` — quoter `quoteExactInputSingle`
- `CallReserves` — UniV2 `getReserves()` + `token0()` / `token1()`
- `CallSecretAbcdefx` — ABCDEFx `getAmountOut`
- `CurveStableSwapAmountOut` / `CurveTricryptoAmountOut` — Curve `get_dy`
- `CallEliteDexRouter` — TraderJoe LB fork `getSwapOut`
- `CallEqualizerRouterAmts` / `CallEqualizerRouterReserves` — Equalizer (ve(3,3))
- `CallMummyFinanceAmts` / `MummyTradeableAmt` / `MummyFiBulkCaller` — GMX-fork vault queries
- `AwaitTxConfirmation` / `TxStatus` — polls tx receipt

**`termex.go`** — Terminal UI via `buger/goterm`. Appears vestigial — `RenderTermex` not called from `main.go`.

### `sauce/` (core logic)

#### `statemachine.go` — Pool State
`StateMachine` holds `map[string]*MEVNode`. Polymorphic node types discriminated by `Type` string (C-style union, not interface):

| Type | Struct | Use |
|---|---|---|
| `UniV2` | `UniV2Params{TokenPair, Token0/1, Reserves0/1}` | Standard AMM pairs |
| `Curve3Pool` | `Curve3Pool{Pool, Token[3], Prices[3x3], CallerAmt}` | 3-token Curve pools |
| `BlackBox2Way` | `BlackBox2Way{Pool, Router, Fee, Token0/1, Price01/10, CallerAmt}` | UniV3, Curve 2-pool, ABCDEFx, Eliteness, MummyFi |

`UpdateStateMachine()` — concurrent goroutine per node (`sync.WaitGroup`). MummyFi uses channel-gated singleton pattern for bulk calls.

All reserves/prices normalized to 18 decimals at the node boundary.

#### `coxswain.go` — Price Oracle
`Cox` — single source of truth for token prices (DAI equivalents).
- `TokenPrice map[string]TokenPriceData` — `DaiToToken` per symbol
- `MummyCallData` — cached MummyFi bulk data
- Decimal shifting utilities

#### `cartographer.go` — Graph
`Graph` — adjacency matrix representation:
- `nodes []*GraphNode` — one per unique token `{id, token, decimals, address, oneDaiEq}`
- `route map[int]map[int][]PoolData` — `route[i][j]` = slice of pools connecting tokens i↔j
- `aps []GraphPath` — pre-computed arbitrage circles
- `dps map[int][]GraphPath` — paths from refToken to each token (for DAI pricing)
- `EthToDaiFactor` — for gas cost calculations

`PoolData` discriminated union: `UniV2PoolData{name, dex, reserve0, reserve1}` or `TwoWayPool{name, dex, Price}`.

`InitCartographer()` → extract tokens → build graph → initial update → pre-compute all arb paths + DAI-eq paths.

`UpdateGraph()` — refreshes edge weights from MEVNode data. `UpdateDaiEq()` — recalculates token prices.

#### `pathfinder.go` — Graph Search
- `initArbPaths()` — for every token, `returnArbCircles()` finds all cycles up to `MAX_PATH_LEN=5` hops
- `findAllPaths()` — recursive DFS, all simple paths between two nodes
- Paths computed **once at startup**, reused every block. Only edge weights change.

#### `quanta.go` — Trade Quantification
`SearchArbRoutes()`:
1. Start at 1 DAI equivalent
2. Scale: 10x → 2x → 2x... up to `MAX_ITERATIONS`
3. Fine-tune at 0.75x if no new routes found
4. Filter on profit threshold

Per path: `routeTrade()` → `bestOutput()` per hop → `calcUniv2Trade()` or `calcTwoWayPoolTrade()`.

DEX-specific fees: Equalizer=998/1000, Tombswap=995/1000, default=997/1000.

Key types: `TradeStatus` (single hop), `ArbRoute` (full route with profit).

#### `trade.go` — Trade Math
- `uniV2Trade()` — standard AMM formula: `out = (amtIn * fee * resv1) / (resv0 * 1000 + amtIn * fee)`
- `calcTwoWayPoolTrade()` — price multiplication via MulWad
- Contains commented-out Curve StableSwap math (abandoned for on-chain `get_dy` calls)

#### `executor.go` — Execution
`SwapData` → Atlas smart contract: `{Routers[], RouterType[], PairBinId[], TokensIn[], TokensOut[], Curvei[], Curvej[], Amt}`

Router types: 0=UniV2, 1=Eliteness, 2=Equalizer, 3=Curve, 4=MummyFi, 5=UniV3.

`ExecuteArb()` flow:
1. `arbRouteToTxData()` → ABI-encode SwapData
2. Apply failsafe factor, cap at contract balance
3. Sentry simulation (optional): `eth_call` to SentryQuoter pre-flight
4. `calcGas()` — gas = network × multiplier. Limits: 200k/UniV2 hop, 400k/Curve/MummyFi/UniV3 hop. Arbitrum: 2x
5. `ensureProfitGtGasCost()` — abort if gas > profit or gas > cap
6. Sign tx (EIP-155)
7. **Broadcast to 3 RPCs concurrently** for latency
8. `MonitorTxInFlight()` — 10s timeout

Smart contract functions: `arbswap(SwapData)` (normal, profit check), `multiswap(SwapData)` (force mode via `-f`).

#### `logger.go` — Scribe
Leveled logger (0=System → 4=Debug). 4 output files: `log.txt`, `arb.txt`, `exec.txt`, `aborted.txt`. Colored terminal output.

#### `ops.go` — Data Structures
`TokensToOrderedMap()`, `reservesToMap()`, array utilities (`MakeRange`, `RemoveUnion`, `ArrEqual`, dedup).

### `utils/`
- **`math.go`** — WAD (1e18) fixed-point arithmetic: `MulWad`, `DivWad`, `DecimalUp/Down`, variadic ops, `DecimalsToReadable`
- **`int.go`** — `EthInt` wrapper around `*big.Int` with method chaining. Used in commented-out Curve math.
- **`eth.go`** — address validation, wei/ether/gwei conversions, block formatting

### `x/` — Standalone Utilities
- **`tx.go`** — ERC20 transfer/approve, recoverTokens, unwrapETH builders
- **`privateKey.go`** — reads private key from `.env`
- **`gasCalc.go`** — gas price + nonce fetcher
- Not imported by main. Used ad-hoc via test harness.

## Data Flow

```
Block N arrives (100ms poll)
    │
    ├─ NetworkState.UpdateNetstate()        ← eth_gasPrice, eth_blockNumber
    │
    ├─ StateMachine.UpdateStateMachine()    ← concurrent per-pool goroutines
    │   ├─ UniV2: CallReserves() → normalize to 18 dec
    │   ├─ Curve3Pool: CurveStableSwapAmountOut() × 6 pairs
    │   ├─ BlackBox2Way: dispatch per DEX type
    │   └─ MummyFi: singleton bulk call → distribute
    │
    ├─ Graph.UpdateGraph()                  ← copy node data → edge weights
    │
    ├─ Graph.UpdateDaiEq()                  ← price all tokens in DAI
    │
    ├─ Graph.SearchArbRoutes()              ← scan pre-computed paths
    │   └─ iterative amount scaling → quantifyProfit() → filter
    │
    ├─ Executor.PickBestRoute()             ← highest DaiProfit, tradeable
    │
    └─ Executor.ExecuteArb()                ← encode → simulate → gas check → sign → broadcast×3
```

## Configuration

**CLI Flags:** `-net` (network), `-e` (execute y/n), `-p` (profit threshold ETH), `-l` (delete old logs), `-o` (failsafe factor 0-1), `-f` (force mode), `-s` (sentry y/n)

**File naming:** `{network}Tokens.json`, `{network}Pairs.json`, `{network}Dexes.json`

**Key relationships:**
- Pair `token0..7` must match symbol keys in Tokens file
- Pair `dex` must match a name in Dexes file
- Pair `type` ∈ {`UniV2`, `Curve3Pool`, `BlackBox2Way`, `MummyFiBulk`}
- `rpc.json` `ref` = reference stablecoin for profit calc, `eth` = native gas token wrapper

**Adding a new chain:** rpc.json entry + 3 JSON files (tokens/dexes/pairs)

## Multi-Chain

Configured in `rpc.json`: eth, goerli, polygon, evmos, dogechain, astar, aurora, fantom, arbitrum, base, milkomeda.

Chain-specific behaviors:
- **Dogechain:** go-web3 client (no multicall)
- **Arbitrum:** gas limit doubled
- **Fantom:** primary target (most DEX integrations built here). Default in systemd service.

## Dependencies

| Package | Role |
|---|---|
| `github.com/lmittmann/w3` v0.11.0 | Primary RPC client, multicall, ABI encoding |
| `github.com/ethereum/go-ethereum` v1.11.4 | Core types, ethclient fallback, tx signing |
| `github.com/Black-Shard/go-web3` | Alt Web3 client (Dogechain) |
| `github.com/Black-Shard/w3-utils` | `DecimalsToReadable()` |
| `github.com/spf13/viper` v1.15.0 | Config file reading |
| `github.com/elliotchance/orderedmap/v2` | Deterministic token ordering |
| `github.com/buger/goterm` | Terminal UI (vestigial) |

## Key Design Decisions

**Pre-computed paths:** All arbitrage cycles enumerated at startup (bounded by `MAX_PATH_LEN=5`). Runtime is a linear scan — trades startup cost for per-block speed.

**Heuristic amount scaling:** Empirical search (1 DAI → 10x → 2x...) instead of analytical optimal input. Avoids complex multi-hop optimization math.

**BlackBox2Way abstraction:** Pools without accessible reserves (Curve, UniV3, ABCDEFx, Eliteness, MummyFi) treated uniformly as normalized price ratios. On-chain `get_dy` / quoter calls provide the price.

**18-decimal internal standard:** All math in WAD fixed-point. Conversion to native decimals only at tx construction.

**Triple RPC broadcast:** Transactions sent to 3 RPCs concurrently for latency.

**Sentry simulation:** Optional pre-flight `eth_call` via SentryQuoter to catch reverts before spending gas.

**Failsafe cascade:** Progressive position sizing reduction on consecutive failures, with kill switch.

**Block-level only:** No mempool monitoring. Reacts to confirmed blocks, not pending transactions. Not a flashbot/MEV-boost system.

**MummyFi singleton:** Channel-gated mutex ensures one bulk call per update cycle, shared across all MummyFi nodes.
