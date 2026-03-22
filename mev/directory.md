# MEV Research — Directory

## `data/`
Shared price data used across all phases.
- `eth_price.csv` — daily ETH/USD (1,539 rows, Jan 2022 → Mar 2026)
- `eth_price_1h.csv` — hourly ETH/USD (36,734 rows)

## `apis/`
API keys for Alchemy RPC (archive node) and The Graph (Aave subgraph).

## `flow/` — Phase 1: Aggregate Signal Search (17 iterations)
Systematic test of on-chain leverage signals for crash prediction. Tested 8 signal candidates, killed 5 cleanly.

**Findings:**
- Perp OI drops (>4%) precede lending liquidation peaks by 37h median, 94% consistency, 10.9% further price decline after signal. ~30% precision.
- Liquidation magnitude classifier separates climactic from distributed events (p=0.003). This is the climactic volume pattern measured on-chain with higher precision.
- Protocol cascade sequencing within lending (Maker→Aave→Compound) has no consistent ordering — leverage gap too small.
- Position heterogeneity principle: temporal ordering in forced-liquidation cascades requires ≥10x leverage gap. Applies to forced closures only, not pricing responses.

**Dead signals:** stablecoin supply, stETH spread, exchange flows, IV timing, OI as standalone predictor.

**Key files:** `thesis.md` (consolidated findings), `signals-synthesis.md` (ranked signals + composite architecture), `exploration-log.md` (17-iteration chronological record), 14 Python scripts, 31 data files.

## `position/` — Phase 2: Position Topology (6 iterations)
Mapped Aave v3 position structure at 8 historical crash episodes via subgraph + Alchemy archive RPC. 29,311 positions scanned, $22.6B collateral.

**Findings:**
- Real/phantom decomposition: >99.99% of near-price liquidation risk ($5.6B) is phantom (ETH-loop positions). Only $73M is real (stablecoin debt). All public liquidation heatmaps are misleading without this classification.
- Wall proximity predicts conditional severity, not binary escalation. Fuel map, not trigger.
- Two cascade modes: progressive (>$14M/1% density) and cliff (single whale >$100M).
- Risk rotation: phantom ratio grew from 2% (2022) to >90% (2026). Fragility shifted from price-cascade to correlation-cascade.

**Key files:** `thesis.md`, `findings.md`, `signals-synthesis.md`, 6 scripts, 17 data files including 9 position snapshots.

## `correlation/` — Phase 3: LST Depeg Cascade (4 iterations)
Tested whether LST market depegs could ignite the $5.6B phantom wall. Disproved own central thesis via bytecode extraction.

**Findings:**
- Aave CAPO oracle adapters read protocol exchange rates (e.g., `getPooledEthByShares`), not DEX market prices. Verified by extracting PUSH32 opcodes from deployed bytecode. Reflexive depeg cascade is structurally blocked.
- DEX liquidity tested via Paraswap: wstETH $5.7M, weETH $13.9M, osETH $976K capacity. Irrelevant because oracle architecture prevents cascade.
- Operational risk replaced market risk: March 10 CAPO misconfig (2.85% stale snapshot) triggered 49 liquidations in 84 seconds, $28.7M seized. $1.42B whale survived by 0.98% margin.
- weETH snapshot currently 2 years stale with 5.4% drift — exceeds the March 10 incident magnitude.

**Key files:** `plan.md` (includes post-investigation assessment), `findings.md`, 4 scripts, 13 data files.

## `dynamics/` — Phase 4: System in Motion (5 iterations + OI extension planned)
Measured leverage lifecycle across 11 price epochs (4 years). 65,382 liquidation events decoded. Exchange flows tested and killed.

**Findings:**
- Two structurally independent systems sharing Aave infrastructure. Phantom: 161 liquidations in 4.2 years (crash-immune). Real: 38,055 events, $1.37B volume.
- Recharge cycle: crash intensity = stored leverage × crash depth, not crash magnitude alone. Same -39% crash produced $12M (depleted) vs $302M (reloaded) — 25× difference.
- Temporal concentration: 3 spike days = 45-89% of each epoch's liquidation volume. Deleveraging in hours, rebuilding over months. Asymmetry ratio 9-203×.
- Crash taxonomy: 5/6 endogenous (participants deleverage), 1/6 exogenous (2024 Yen carry — borrowing +15% during crash). n=1.
- Utilization homeostasis at 38-42% post-2022. Rate controller provides structural ceiling on leverage buildup.
- Exchange flows: null signal (max |r| < 0.04 at all lags). Unmeasured flows dominate measured.
- Collateral composition shifting: wstETH grew from 0% (2022) to 56% (2025) of real liquidation volume. Distinct user population, larger positions.

**Planned extension (Step 6):** OI leading signal refinement — multi-exchange coverage, crash-type conditioning, voluntary/forced decomposition, conjunction test with utilization + VIX.

**Key files:** `findings.md`, `plan.md`, `exploration-log.md`, 7 scripts, 21 data files including `liquidations_full.csv` (65,382 events).

## `links/` — Phase 5: TradFi Connections (4 iterations)
Connected DeFi mechanics to macro markets. Pulled S&P, VIX, USD/JPY, DXY, yields, gold, Fed funds via yfinance + FRED.

**Findings:**
- DeFi amplifies crashes it did not initiate. After controlling for BTC + S&P: ~100 bps extra ETH decline per 100 Aave liquidations, concave (first 100 events do 3× marginal damage).
- Three modes of DeFi/crash interaction: (1) ramp-phase amplification (first wave most damaging, 5-7 day timescale), (2) recovery suppression (ongoing deleveraging blocks ETH participation in bounces), (3) exhaustion reversal (forced selling completes → disproportionate bounce).
- VIX monotonically drives ETH/S&P coupling: Q1 (VIX <15) r=0.23, Q4 (VIX >22) r=0.51. High VIX = strong, stable coupling.
- Macro crashes produce 2× daily and 4× cumulative amplification vs crypto-native.
- Borrow growth null is definitive (r=0.007, p=0.81). Chronic ETH/BTC decline is market-structural (BTC ETF, institutional rotation), not DeFi-mechanical.
- Aave lending cascades are never the first mover in any of 5 crashes. DeFi broadly (UST) did initiate Terra — the claim is specific to lending liquidation cascades as second-order amplifier.
- 2025 January mystery: -11.2% model residual with 18 liqs/day. Unexplained by any measured variable.

**Key files:** `findings.md`, `signals-synthesis.md` (composite signal design), `exploration-log.md`, 3 scripts, 8 data files including `tradfi_daily.csv`.

## `crosschain/` — Phase 6: Cross-Chain Flows (4 iterations)
THORChain Midgard API investigation of directional cross-chain swap flows, arb activity, and price transmission.

**Findings:**
- During crashes, THORChain shows BTC net selling ($600M-1.4B/day) and ETH net buying ($300M-1B/day) — rotation, not uniform flight to safety.
- Arb share jumps from ~50% (calm) to 86-91% (crash). Mechanically clean: volatile prices → AMM lags CEX → arbs correct.
- USDC accumulation pre-crash, then selling on crash day (dip buying).
- All directional flow signals dead (BTC→ETH rotation is persistent baseline, flight-to-safety inverted, momentum is depth artifact).
- Found arb correction mechanism (ratio ≈1.0, scales with profit opportunity) and BTC-ETH hourly correlation as crash-type classifier (clear-direction vs contested). No predictive power.

**Key files:** `findings.md`, `signals-synthesis.md`, `plan.md`, 4 scripts, 8 data files.

## `physics/` — Phase 7: Physical Latency in Markets (4 iterations, complete)
Markets are fast at pricing information but slow at moving atoms. Tested which physical processes create exploitable timing windows and which are arbitraged despite their latency. Produced the crash lifecycle model connecting all prior phases.

**Findings:**
- **Informational timing gets arbitraged.** Funding settlement (known schedule, visible rates) produces no exploitable OI clustering. Both funding extremes show OI drops — regime symptom, not cause. Deprioritizes margin call cycles (same category).
- **Oracle-gated threshold batching, not cascade.** Within-day liquidations are simultaneous batch events (67% same-block) triggered by discrete Chainlink oracle price updates (~0.5-1% deviation threshold). Burstiness B=0.77, 21/21 spike days reject uniform null. Mega-bursts up to 377 events = extreme positional herding within one oracle step.
- **Self-reinforcement exists but magnitude uncertain.** Hourly price resolution insufficient to separate liquidation-driven acceleration from velocity clustering and liquidity thinning. Best estimate: second-order positive feedback.
- **ETF flows classify cascade type.** Outflows accompany multi-day clusters; terminal days show flow reversal. Acts as cascade-type classifier (multi-day vs isolated), not predictor. ETF outflows necessary but not sufficient — also requires position density at next price level.
- **January 2025 mystery partially resolved.** +$5.3B BTC ETF inflows in Jan 2025 — the -11.2% ETH residual was NOT ETF-driven. Brief ETH→BTC rotation visible.

**Crash Lifecycle Model (phase output):**
1. Trigger: external (macro → ETF) or endogenous (position breach)
2. Within-day: oracle-gated threshold batching (~7.6 min inter-burst gap)
3. Feedback: second-order positive, magnitude uncertain
4. Inter-day extension: requires both external pressure (ETF outflows) AND position density at next level
5. Termination: flow reversal + position cluster exhaustion

**Key files:** `plan.md` (status table), `exploration-log.md` (4 iterations + consolidation), `signals-synthesis.md` (ranked signals + composite), 4 scripts, 1 data file (`data/etf_daily_flows.csv`), 9 plots.

---

## Cross-Phase Arc

Each phase answered the question left open by its predecessor:

1. **Flow** → "Escalation is a topology question, not a flow question"
2. **Position** → "Risk has rotated to depeg-cascade fragility"
3. **Correlation** → "Oracle architecture blocks the depeg cascade; real risk is operational"
4. **Dynamics** → "System has two independent components; crashes are externally initiated"
5. **Links** → "DeFi amplifies macro shocks via three distinct modes"
6. **Cross-chain** → "Flows don't predict, but arb mechanics characterize crash type in real time"
7. **Physics** → "Crash lifecycle is oracle-gated batching + external pressure. Informational timing is arbitraged; physical latency persists."

## Structural Principles

**Position heterogeneity determines signal quality.** Temporal ordering in forced-liquidation cascades scales with the leverage gap between position types. Requires ≥10x gap to produce consistent ordering. Governs forced closures only — pricing mechanisms (IV, spreads, funding rates) follow their own timing dynamics.

**Physical processes create measurable lead time. Information doesn't.** The contract OI signal works not because it contains private information (it's public data) but because it measures a physical process — position unwinding — that takes time regardless of who knows about it. Signals based on information content get arbitraged; signals based on physical latency persist.

**The system produces classifiers, not predictors.** Across phases 6 and 7, the recurring pattern is regime classification (BTC-ETH correlation classifies crash type; ETF flow sign classifies cascade duration) rather than event prediction. The 27h OI signal from Phase 1 remains the only tested predictive signal.
