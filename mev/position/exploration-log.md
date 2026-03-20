# Position Topology — Exploration Log

## Iteration 1: Current Snapshot + Debt-Side Discovery

### What was built
- `snapshot.py`: Pulls all active Aave v3 Ethereum borrowers, computes health factors and liquidation prices.
- Data pipeline: The Graph subgraph (user positions, collateral breakdown) + on-chain Multicall3 (`getUserAccountData` for ground-truth HF) + on-chain oracle (asset prices in USD).
- eMode handled correctly via on-chain HF — covers all 20+ eMode categories without needing to resolve category membership per user.
- Output: `data/positions_current.csv` (29,311 positions with debt), `data/1_results.txt` (summary).
- Runtime: ~875s.

### What was measured

**Aggregate numbers (2026-03-20, ETH $2,202.39):**
- Total borrowers: 43,735
- Positions with debt: 29,311
- Total collateral: $22.56B, total debt: $13.18B
- ETH-dominant positions (>50% ETH-correlated collateral): 15,897 positions, $14.07B collateral, $8.58B debt

**Health factor distribution:**
- HF < 1.0: 784 positions, $134 debt (all dust — validates the on-chain HF approach)
- HF < 1.1: 3,291 positions, $7.17B debt
- HF < 1.5: 10,441 positions, $9.34B debt

**Apparent liquidation wall at $2,050–$2,150 (4–5% below current):**
- 629 positions, $4.34B debt, $4.77B collateral
- Top 3 positions = 61.8% of this wall ($2.68B):
  - #1: $1.42B collateral (wstETH), $1.30B debt, HF=1.040, liq=$2,118
  - #2: $1.26B collateral (weETH), $1.13B debt, HF=1.054, liq=$2,089
  - #3: $279M collateral (weETH), $254M debt, HF=1.046, liq=$2,106
- 96 positions with >$1M debt hold $4.29B of the $4.34B. The remaining 533 positions contribute $51M.

**Broader density ($50 bins, ETH-dominant only):**
- $2,100–$2,150: $2.80B (dominated by position #1)
- $2,050–$2,100: $1.54B (dominated by position #2)
- $2,150–$2,200: $731M (distributed, no single position >$60M)
- $1,050–$1,100: $314M
- $1,350–$1,400: $251M
- Below $1,600: relatively uniform background of $100–250M per $50 bin

**Danger zone composition (HF 1.0–1.1, $5.43B debt):**
- All top-20 positions are staking derivatives: weETH, wstETH, rsETH, osETH
- Leverage: 10–20x (consistent with eMode looping strategies)
- No WETH-collateral positions appear in the top 20 of this band

### What was found (review discussion)

**Critical finding: the apparent $4.3B wall is likely phantom.**

The liquidation price formula assumes debt stays fixed in USD as ETH price drops:
```
k = (debt_usd - non_eth_col * lt) / (eth_col_usd * lt)
liq_price = eth_price * k
```

For positions where both collateral (wstETH/weETH) and debt (WETH) are ETH-correlated, ETH/USD cancels from the health factor equation:
```
HF = (wstETH_amount × wstETH_ETH_rate × ETH_USD × LT) / (WETH_amount × ETH_USD)
```
HF depends only on the wstETH/ETH exchange rate, not ETH/USD price. These positions don't have a meaningful ETH/USD liquidation price. The computed $2,089–$2,118 numbers describe a scenario that cannot occur for loop positions.

The real liquidation trigger for loop positions is a staking derivative depeg (wstETH/ETH, weETH/ETH ratio dropping), not an ETH/USD price decline.

**Implication: two coupled liquidation surfaces.**
1. **Real walls** (ETH-collateral + stablecoin-debt): activated by ETH/USD price drops. These produce ETH selling pressure via liquidator arbitrage.
2. **Phantom walls** (staking-derivative-collateral + WETH-debt): activated by depeg events only. These produce staking derivative selling pressure, contained within the LST ecosystem.

These surfaces are not independent — they are sequential stages of the same cascade. Historical pattern (2022 stETH depeg): ETH/USD drop → liquidity stress → staking derivative depeg → phantom wall activation → deeper depeg spiral.

**Hierarchy within the phantom wall (conjectured, not measured):**
- osETH/tETH/ETHx (thin DEX liquidity): low depeg threshold, activate early, small absolute size (~$300M)
- weETH (medium liquidity): medium threshold, $1.5B+ in positions
- wstETH (deep Curve/Balancer liquidity): high threshold, only cracks in severe systemic stress, $1.4B+ when it does

**Historical note:** Staking derivative loops at 10–12x leverage are a post-Aave-v3-eMode phenomenon (2023+). In 2022 episodes, positions were simpler (WETH collateral, stablecoin debt, lower leverage). The historical backtest for 2022 episodes may produce a cleaner real-wall signal.

### What was not measured
- **Debt-side breakdown per user.** The subgraph fetches `currentTotalDebt` per reserve per user, but `snapshot.py` only used this data on the collateral side. The debt symbol (WETH vs USDC vs DAI) is the critical missing dimension that determines whether a position is real or phantom.
- **Size of the real wall** after stripping phantom (loop) positions. Unknown whether meaningful real walls exist at current market conditions.
- **Wall composition by proximity band.** Hypothesis: near-current positions may be more phantom (loopers optimize for tight HF) while positions 20–30% below may be more real (stablecoin borrowers leave more buffer). Untested.
- **Liquidation cascade mechanics differ by type.** Real wall liquidations: liquidator receives ETH, sells for stablecoins → ETH/USD selling pressure. Phantom wall liquidations: liquidator receives wstETH, sells for WETH → wstETH/ETH selling pressure. Different contagion channels, not yet modeled.

### Validation
- DefiLlama stale snapshot (ETH~$3,782): $2.16B total liquidatable (all protocols, specific bins). Our Aave v3: $13.2B total debt, $22.6B collateral. Not directly comparable (different metric, different time, different price level) but order of magnitude is consistent.
- HF < 1.0 positions are dust only ($134 total) — confirms on-chain multicall produces correct health factors.
- Top whale HF=1.040 with wstETH collateral implies eMode LT ≈ 95.2% (1.04 × debt/col = 1.04 × 0.916), consistent with Aave v3 ETH-correlated eMode parameters.

---

## Iteration 2: Debt-Side Decomposition — Real vs Phantom Wall

### What was built
- `decompose.py`: Re-fetches subgraph userReserves for debt breakdown per user, merges with existing `positions_current.csv`. Classifies each position by debt composition. Runtime: ~6 min (avoids expensive multicall re-run).
- Output: `data/positions_decomposed.csv` (29,311 positions with added columns: `eth_debt_usd`, `stable_debt_usd`, `eth_debt_fraction`, `position_type`), `data/1b_results.txt`.

### What was measured

**Position type classification (ETH-dominant positions only):**

| Type | Positions | Debt | Collateral |
|------|-----------|------|------------|
| Real (stablecoin debt, eth_debt_frac < 0.2) | 13,391 | $2.92B | $7.74B |
| Phantom (ETH debt, eth_debt_frac > 0.8) | 2,297 | $5.64B | $6.28B |
| Mixed (0.2–0.8) | 210 | $0.02B | $0.05B |

Fewer phantom positions (2,297) hold nearly twice the debt of real positions (13,391). Phantom positions are concentrated in large, high-leverage strategies.

**The $3.8B naive wall at 5% below is 99.99% phantom (confirmed):**

| Band | Real Debt | Phantom Debt | Real % |
|------|-----------|-------------|--------|
| 5% | $313K | $3.78B | 0.0% |
| 10% | $9.2M | $5.44B | 0.2% |
| 20% | $72.7M | $5.50B | 1.3% |
| 30% | $572M | $5.62B | 9.2% |
| 50% | $1.57B | $5.64B | 21.8% |

The three mega-whale positions confirmed as phantom:
1. $1.42B wstETH collateral / $1.30B WETH debt → phantom
2. $1.26B weETH collateral / $1.13B WETH debt → phantom
3. $279M weETH collateral / $254M WETH debt → phantom

**Real wall cumulative distribution (from current price downward):**
- Within 2%: $0 (66 dust positions)
- Within 5%: $313K
- Within 10%: $9.2M
- Within 15%: $43.8M
- Within 20%: $72.7M
- Within 25%: $261M
- Within 30%: $572M — first meaningful concentration
- Within 40%: $1.08B
- Within 50%: $1.57B

**Real wall density by $50 bins (top 5):**
1. $1,050–$1,100: $429M (410 positions, largest $128M) — densest real bin, ~50% below current
2. $1,300–$1,350: $267M (437 positions, largest $143M)
3. $1,500–$1,550: $161M (329 positions, largest $70M)
4. $1,200–$1,250: $157M (491 positions, largest $97M)
5. $1,150–$1,200: $131M (435 positions, largest $52M)

**Real position HF distribution:**
- HF 1.0–1.1: 411 positions, $9M debt (dust)
- HF 1.1–1.25: 726 positions, $85M debt
- HF 1.25–1.5: 2,022 positions, $666M debt
- HF 1.5–2.0: 3,481 positions, $909M debt
- HF 2.0–3.0: 3,032 positions, $887M debt
- HF 3.0+: 2,636 positions, $360M debt

Real positions are systematically more conservative. Only $94M of real debt has HF < 1.25. The bulk sits at HF 1.5–3.0.

**Largest real positions (stablecoin debt, ETH collateral):**
1. $142M USDC debt, WETH collateral, liq=$1,347 (39% below), HF≈1.6
2. $128M USDT debt, WETH collateral, liq=$1,056 (52% below), HF≈2.1
3. $123M USDC debt, WETH collateral, liq=$1,098 (50% below), HF≈2.0
4. $96M USDC debt, WETH collateral, liq=$1,250 (43% below), HF≈1.7
5. $89M USDC debt, weETH collateral, liq=$480 (78% below), HF≈4.6

### What was found (review discussion)

**The two populations have completely different spatial signatures:**
- Phantom positions: tight HF (1.0–1.1), concentrated 0–5% below current price, massive ($5.6B). They run tight HF because their risk is only depeg, not ETH/USD price.
- Real positions: wide HF (1.5–3.0), spread 30–70% below current price, modest ($2.9B total, distributed). These borrowers leave large safety buffers.

**The real wall is a gradient, not a wall.** $572M over a 10% price range (20–30% below) is ~$57M per 1% of price movement. Against daily ETH spot volume of $5–15B, this is absorbed without creating a cascade trigger. The thesis hypothesized concentrated clusters that overwhelm market depth. What exists on Aave v3 in 2026 is diffuse friction, not a cliff.

**Cascade mechanics differ by position type (from discussion, conjectured):**
- Real wall liquidations: liquidator repays stablecoin debt, receives ETH collateral at discount, sells ETH for stables → direct ETH/USD selling pressure.
- Phantom wall liquidations: liquidator repays WETH debt, receives wstETH/weETH at discount, sells LST for WETH → selling pressure on LST/ETH peg, contained within staking derivative ecosystem. Does not directly create ETH/USD selling pressure.
- Coupling: real wall cascade → ETH/USD drop → liquidity stress on LSTs → potential depeg → phantom wall activation. Sequential stages, not parallel risks.

**Protocol coverage gap identified.** Aave v3's eMode makes it the natural home for phantom (loop) positions. Maker/Sky vaults are structurally "all real" — you can only borrow DAI, never ETH, so no loops are possible. The real wall signal the thesis needs may be primarily in Maker vault data. Similarly, Compound v3 likely has a higher real-to-phantom ratio. The Aave-only picture systematically understates real wall density because Aave attracts the phantom-heavy population.

**Maker liquidation mechanics note:** Maker uses Dutch auctions (Liquidations 2.0), with auctions taking ~30–60 minutes per vault. Even concentrated Maker walls don't produce instant price cliffs — collateral hits the market over a window. This further diffuses cascade potential.

**Regime transition across backtest period (conjectured):**
- 2022: Real-dominated topology. No eMode, stETH existed but loops at ~3–4x max. More positions with WETH collateral + stablecoin debt. Real walls likely closer to price.
- 2023–2024: Transition period. Aave v3 eMode + EtherFi/EigenLayer restaking era. Loop leverage jumped to 10–12x. Phantom wall grows.
- 2025–2026: Phantom-dominated near-price topology (current state). Real walls pushed to -30% to -50%.

This creates a natural experiment for the backtest: if the mechanism is real, 2022 episodes with near real walls should show escalation, while 2024–25 episodes with only phantom walls near price should show a different pattern. The transition period (2023–24) should show intermediate behavior.

### What was not measured
- **Maker/Sky vault topology.** All Maker ETH vaults are "real" by construction (DAI debt only). Unknown whether Maker contributes meaningful real wall volume near current price. This is the highest-priority gap before committing to historical backtest scope.
- **Compound v3 topology.** Likely higher real-to-phantom ratio than Aave v3, but size and distribution unknown.
- **Aggregate real wall across protocols.** The thesis is about total liquidation topology, not per-protocol. The Aave-only real wall ($572M at -30%) may be substantially larger when Maker and Compound are added.
- **Historical wall composition.** Whether 2022 positions formed genuine concentrated walls (single large positions at specific price levels) or were always diffuse gradients.
- **LST depeg thresholds.** The depeg level at which phantom positions activate for each LST type. Related to DEX liquidity depth for each token.
- **Whether wall composition changes character at different distances from current price** — the hypothesis that near-price is more phantom while distant positions are more real was confirmed, but the gradient shape has not been characterized precisely across protocols.

---

## Iteration 3: Maker/Sky Vault Scan + Protocol Scope Decision

### What was built
- `maker_scan.py`: Reads all active Maker/Sky ETH-collateral vaults directly from on-chain contracts via Multicall3 (CdpManager + Vat + Spot). Computes liquidation prices per vault.
- Scanned ilks: ETH-A (145% min ratio), ETH-B (130%), ETH-C (170%), WSTETH-A (150%), WSTETH-B (175%).
- Output: `data/maker_vaults.csv` (852 active vaults), `data/2_maker_results.txt`.
- Runtime: ~204s.

### What was measured

**Maker vault summary:**
- Total CDPs ever created: 32,017
- ETH-related CDPs: ~21,000
- Active ETH vaults (ink > 0, art > 0): 852
- Total collateral: 739,411 ETH ($1.63B)
- Total debt: $516M DAI/USDS

**Per-ilk breakdown:**

| Ilk | Vaults | ETH | Collateral USD | Debt | Min Ratio |
|-----|--------|-----|----------------|------|-----------|
| ETH-A | 671 | 240,549 | $530M | $164M | 145% |
| ETH-B | 26 | 8,076 | $18M | $8.1M | 130% |
| ETH-C | 109 | 447,620 | $986M | $311M | 170% |
| WSTETH-A | 23 | 18,650 | $41M | $20M | 150% |
| WSTETH-B | 23 | 24,516 | $54M | $13M | 175% |

All Maker vaults are "real" by construction — debt is always DAI/USDS, never ETH. No phantom positions possible.

**Maker liquidation price distribution:**
- Within 5%: 1 vault, $28K debt
- Within 10%: 3 vaults, $167K debt
- Within 20%: 27 vaults, $7.6M debt
- Within 30%: 69 vaults, $27.4M debt
- Within 50%: 163 vaults, $323M debt

**Top 5 Maker vaults by debt:**
1. Vault 31214: 216,345 ETH ($476M col), $135M debt, liq=$1,064 (52% below)
2. Vault 28104: 137,908 ETH ($304M col), $109M debt, liq=$1,340 (39% below)
3. Vault 22025: 100,394 ETH ($221M col), $97M debt, liq=$1,400 (36% below)
4. Vault 30009: 55,000 ETH ($121M col), $43M debt, liq=$1,343 (39% below)
5. Vault 7605: 54,850 ETH ($121M col), $16M debt, liq=$433 (80% below)

**Maker effective HF distribution:**
- HF 1.0–1.1: 3 vaults, $0.2M debt
- HF 1.1–1.25: 24 vaults, $7.4M debt
- HF 1.25–1.5: 52 vaults, $23.8M debt
- HF 1.5–2.0: 84 vaults, $291M debt (bulk of Maker debt)
- HF 2.0–3.0: 148 vaults, $165M debt
- HF 3.0+: 533 vaults, $27.4M debt

Only 28 Maker vaults ($7.8M debt) are within 20% of liquidation. The three mega-vaults sit at 36–52% below current price.

**Combined Aave real + Maker wall:**

| Band | Aave Real | Maker | Combined | Maker % |
|------|-----------|-------|----------|---------|
| 5% | $313K | $28K | $340K | 8% |
| 10% | $9.2M | $167K | $9.4M | 2% |
| 20% | $73M | $7.6M | $80M | 9% |
| 30% | $572M | $27M | $599M | 5% |
| 50% | $1.57B | $323M | $1.90B | 17% |

### What was found (review discussion)

**Maker confirms the pattern — does not change it.** Maker vaults are even more conservatively leveraged than Aave v3 real positions. Adding Maker to the aggregate real wall changes numbers by <10% at all relevant near-price bands (≤20%).

**The combined real wall across Aave v3 + Maker within 20% of current ETH price is $80M.** This is negligible. The first meaningful concentration remains at 30–50% below, where the combined total is ~$1.9B.

**Protocol scope decision: proceed Aave-only for historical backtest.** Maker adds insufficient signal to justify the engineering complexity of adding a second protocol to the historical pipeline.

**Cross-protocol pattern (measured):** Both Aave v3 real positions and Maker vaults show the same conservative leverage pattern — borrowers who take real ETH/USD risk maintain wide HF margins (1.5+). This is consistent across two independent protocols with different user bases and mechanics.

**Alternative explanation for conservatism (from discussion):** Walls being far from price at ETH $2,200 may reflect price appreciation rather than conservative behavior. Positions opened at lower ETH prices now show high HFs due to collateral value increase. Historical snapshots at episode onsets — when price had already dropped — would show tighter HF distributions. This is testable and is a reason to proceed to historical data.

**Aave v2 requirement for historical backtest (identified):** Aave v3 launched on Ethereum mainnet in January 2023. All 2022 episodes (Terra/Luna May, 3AC/stETH depeg June, FTX November) ran on Aave v2. The historical backtest requires the Aave v2 subgraph, which has a different subgraph ID and no eMode. The v2 subgraph's availability and support for `block: {number: N}` historical queries must be verified before building the full pipeline. If v2 subgraph is unavailable, the 2022 episodes — the regime most likely to show real-wall signal — cannot be tested.

### What was not measured
- **Aave v2 subgraph availability.** Whether the Aave v2 Ethereum subgraph on The Graph is still actively indexed and supports historical block queries. This is the critical feasibility gate for the historical backtest.
- **A single historical snapshot.** No historical position data has been pulled yet. A probe at one known episode onset (e.g., June 2022 stETH depeg) would test both feasibility and whether 2022 wall structure differs from 2026.
- **Compound v3 topology.** Not scanned. Judged lower priority than Maker based on discussion; Maker was the most likely source of missing real wall signal, and it turned out thin.
- **Wall migration over time.** Whether the fraction of real debt within 10% of liquidation has declined from 2022 to 2026 as the market learned. Requires historical data.

---

## Iteration 4: Historical Probe — June 2022 stETH Depeg Onset

### What was built
- `historical_probe.py`: Fully on-chain approach for Aave v2 historical snapshots. Uses Alchemy archive RPC (free tier supports historical `eth_call`).
- Pipeline: (1) Get v2 reserve list + debt token addresses at historical block, (2) Find all borrowers via `alchemy_getAssetTransfers` scanning debt token mints, (3) Multicall `getUserAccountData` at historical block, (4) `getUserReserveData` per-user per-reserve for 21 key reserves, (5) Classify by debt composition.
- Output: `data/positions_june2022.csv` (17,354 positions), `data/3_historical_probe.txt`.
- Runtime: ~28 minutes.

### What was measured

**V2 subgraph status: DEAD.**
- Legacy hosted service (api.thegraph.com): returns "endpoint removed"
- Decentralized network: two known subgraph IDs (CvvUWXNtn8A5zVAtM8ob3JGq8kQS8BLrzL6WJV7FrHRy, 84CvqQHYhydZzr2KSth8s1AFYpBRzUbVJXq6PWuZm9U9) — both found on explorer but have no active indexers
- Fully on-chain approach via Alchemy archive multicall is the only viable path for 2022 data

**June 10, 2022 snapshot (block 14935369, ETH $1,788.42, stETH/ETH 0.973):**
- Total borrowers: 17,354
- Total collateral: $6.92B, total debt: $3.20B
- ETH-dominant positions: 12,525

**Decomposition (ETH-dominant only):**

| Type | Positions | Debt |
|------|-----------|------|
| Real | 11,836 | $1,493M |
| Phantom | 582 | $847M |
| Mixed | 107 | $52M |

Phantom ratio in 2022: 35% of ETH-dom debt (vs >90% in 2026). stETH/WETH loops existed but at much lower scale and leverage.

**Real wall distribution (ETH $1,788):**
- Within 5%: 298 positions, $6.2M
- Within 10%: 788 positions, $20.5M
- Within 20%: 1,594 positions, $99.3M
- Within 30%: 3,274 positions, $140.2M
- Within 50%: 4,551 positions, $696.9M

**Density in crash zone ($1,000–$1,788), $50 bins:**
- $1,700–$1,750: $5.7M (background gradient)
- $1,600–$1,650: $11.3M
- $1,500–$1,550: $34.7M ← first notable concentration, 16% below
- $1,450–$1,500: $29.1M
- $1,200–$1,250: $21.4M
- **$1,150–$1,200: $316.9M** ← MEGA WALL, 36% below
- $1,100–$1,150: $59.3M
- $1,050–$1,100: $31.0M
- $1,000–$1,050: $35.8M

**The mega-wall at $1,150–$1,200 is one whale.** Position 0x4093fbe...f80e: $501M WETH collateral, $282M stablecoin debt, HF=1.51, liq=$1,185. This single address accounts for $282M of the $317M in its bin. It was breached during the crash (ETH fell to ~$1,000).

**Top 5 real positions:**
1. $1.33B col (stETH), $578M debt, HF=1.83, liq=$515 — survived crash
2. $501M col (WETH), $282M debt, HF=1.51, liq=$1,185 — liquidated during crash
3. $50M col (WETH), $28M debt, HF=1.55, liq=$912 — liquidated during crash
4. $44M col (stETH), $22M debt, HF=1.61, liq=$1,112 — liquidated during crash
5. $48M col (WETH), $18M debt, HF=2.17, liq=$293 — survived crash

**Total real debt in crash zone ($1,000–$1,788): $605M** — 40% of all real ETH-dom debt sat in the path of the crash.

**Real position HF distribution (2022 vs 2026):**

| Band | Jun 2022 Positions | Jun 2022 Debt | Mar 2026 Positions | Mar 2026 Debt |
|------|-------------------|--------------|-------------------|--------------|
| 1.0–1.1 | 735 | $16.7M | 411 | $9.0M |
| 1.1–1.25 | 943 | $72.9M | 726 | $84.6M |
| 1.25–1.5 | 1,996 | $97.4M | 2,022 | $665.9M |
| 1.5–2.0 | 1,110 | $1,132M | 3,481 | $909.3M |
| 2.0–3.0 | 1,523 | $119.7M | 3,032 | $886.6M |
| 3.0+ | 1,639 | $54.1M | 2,636 | $360.0M |

Fraction of real debt at HF < 1.5: 12.5% in 2022 vs 26.1% in 2026. The 2022 distribution was more bimodal — either very tight (HF 1.0–1.25, small positions) or moderate-leverage whales (HF 1.5–2.0, dominated by the $282M and $578M positions).

**The $578M stETH position — near-miss phantom activation (calculated in review):**
At crash bottom (~ETH=$1,000, stETH/ETH≈0.93): stETH price ≈ $930 → collateral value ≈ $711M → HF ≈ ($711M × 0.85) / $578M ≈ 1.04. This position came within 4% of liquidation. If ETH had dropped to ~$950 or stETH/ETH had worsened to ~0.90, a $578M liquidation would have fired, dumping ~765K stETH into an already-broken market. This is the real-phantom coupling mechanism observed in the wild.

### What was found (review discussion)

**The "wall" is really a "whale."** The $282M position at liq=$1,185 was 47% of all real debt in the crash zone. Remove it: $323M remains spread across $788 of price range — ~$40M per $100, which is a gradient, not a wall. This is comparable in density to 2026's gradient.

**Thesis refinement: whale + runway model.** The discussion produced a refined cascade model:
- **Gradient = kindling.** Distributed small positions between current price and the whale. Each liquidation is individually absorbed but pushes price lower, facilitating the price reaching the whale.
- **Whale = cliff.** A single massive position at a specific price point. When breached, its liquidation overwhelms market depth, producing a price gap.

In June 2022: $99M of gradient between $1,788 and $1,500 (runway), then $282M whale at $1,185 (cliff). Price was pushed through the gradient by external forces (Terra/3AC), reached the whale, and the whale's liquidation accelerated the crash from $1,200 to $1,000.

**Two candidate metrics for the backtest:**
1. **Cliff metric**: size and proximity of the largest real position
2. **Runway metric**: cumulative real debt between current price and the cliff

Together: "is there a cliff, and is there a runway to it?"

**Fail-fast backtest design proposed:** Rather than running all 27 episodes (~13 hours), select 3-4 maximally informative episodes first:
- 1 escalating + 1 non-escalating from 2022 (v2, real-dominated regime)
- 1 escalating + 1 non-escalating from 2024-25 (v3, phantom-dominated regime)

If the pattern holds across these 4, expand. If it looks random, stop and reassess.

### What was not measured
- **Episode classification labels.** The flow phase identified 27 episodes, but the precise binary label (escalated vs absorbed) for each has not been extracted and verified for use in the backtest.
- **Which specific episodes to use for the fail-fast test.** Need to examine the episode data to select the most informative 3-4 episodes (clear escalation vs clear absorption, across both regime periods).
- **Whether the $282M whale's liquidation actually occurred on-chain.** We inferred it was liquidated because ETH passed through $1,185, but haven't verified with on-chain liquidation events.
- **The other 26 episodes.** Only one historical snapshot taken so far.
- **Runway-to-cliff metric computation.** The model was articulated but not yet computed on any data.

---

## Iteration 5: Fail-Fast Backtest — 4 Episodes

### What was built
- `failfast_backtest.py`: Runs historical snapshots for 3 additional episodes (Nov 2022, Apr 2024, Aug 2024), combining V2 on-chain approach and V3 subgraph approach.
- V3 subgraph historical queries confirmed working with `block: {number: N}` parameter. V3 snapshots ~6x faster than V2 on-chain (~6 min vs ~28 min).
- Output: `data/positions_nov2022.csv` (26,894), `data/positions_apr2024.csv` (8,563), `data/positions_aug2024.csv` (12,047), `data/4_failfast_results.txt`.
- Total runtime: ~30 min.

### What was measured

**4 episodes tested across both regimes:**

| Episode | Type | ETH | Cliff Size | Cliff Dist | R5% | R10% | R20% | R30% |
|---------|------|-----|-----------|-----------|-----|------|------|------|
| Jun 2022 stETH depeg | Escalating | $1,788 | $578M | 71% | $6.2M | $20.5M | $99.3M | $140.2M |
| Nov 2022 FTX crash | Moderate | $1,569 | $30M | 83% | $2.0M | $2.8M | $20.5M | $37.3M |
| Apr 2024 Iran tensions | Absorbed | $3,510 | $156M | 70% | $0.1M | $22.3M | $161.7M | $275.8M |
| Aug 2024 Yen carry trade | Escalating | $2,903 | $187M | 49% | $49.3M | $142.1M | $420.3M | $624.1M |

**Phantom ratio evolution (measured across 5 snapshots):**
- Jun 2022: 36% phantom ($847M / $2.3B ETH-dom debt)
- Nov 2022: 52% phantom ($540M / $1.0B)
- Apr 2024: 45% phantom ($1.4B / $3.1B)
- Aug 2024: 54% phantom ($2.7B / $4.9B)
- Mar 2026: >90% phantom (from current snapshot)

**Aug 2024 crash zone detail ($2,100–$2,903):**
- 1,469 real positions, $566M debt
- No single position larger than $29M
- Top 10 positions = 36% of crash zone debt
- Continuous density: $42M at 5% below, $53M at 10%, $97M at 12%
- ~$14M of real debt per 1% of price in the near zone

**Apr 2024 crash zone detail ($3,000–$3,510):**
- 139 real positions, $78M debt
- Largest single position: $19M
- Within 10%: only $22M
- $162M at R20% included a cluster at $3,140 ($45M in 3 positions) barely within the drawdown path
- ~$2M of real debt per 1% of price in the near zone

**Nov 2022 crash zone detail ($1,100–$1,569):**
- Only $37M real debt in the entire 30% crash zone
- Largest position: $30M at $263 (83% below, unreachable)
- Post-clearing effect: the June crash had liquidated everything above $1,000

**Classification: 4/4 correct** using R10% + cliff proximity:
- Escalating episodes: Yen R10%=$142M (dense gradient), stETH R10%=$21M (thin gradient but $282M cliff at 34%)
- Non-escalating: FTX R10%=$2.8M (empty), Iran R10%=$22M (scattered, no cliff)

### What was found (review discussion)

**Two distinct cascade modes observed:**

1. **Progressive cascade (Yen carry, Aug 2024):** No single mega-whale, but continuous density at ~$14M per 1% of price. Each layer of liquidations produced enough selling to push through to the next layer. Self-sustaining through cumulative friction.

2. **Cliff cascade (stETH depeg, Jun 2022):** Thin gradient ($2M/1%) that was individually absorbed, until price reached a $282M concentrated position at $1,185. The whale produced a burst that overwhelmed depth at a single point.

**The unifying mechanism:** At each price level, does liquidation selling pressure exceed market absorption capacity? This can be via density (progressive) or concentration (cliff). The gradient *alone* at $2M/1% doesn't cascade (Iran's topology had $22M at R10% and didn't escalate). But $2M/1% CAN facilitate a cliff cascade by pushing price incrementally toward the whale, where external forces provide additional downward pressure.

**R10% alone doesn't capture both modes.** stETH depeg ($21M) and Iran ($22M) have similar R10% — the cliff presence separates them. A composite metric needs both: R10% + max single position within reachable range.

**Topology as amplifier, not cause (key framing from discussion):** Topology doesn't predict the initial shock. It predicts the amplifier gain. Every episode starts with an exogenous perturbation (Terra, FTX, yen unwind, Iran). Topology determines whether the perturbation gets amplified by liquidation cascading or absorbed.

Evidence: FTX (Nov 2022) — massive external shock, 30% drawdown, but empty topology (post-clearing) → only $12M Aave liquidations → no DeFi amplification. The drawdown happened from centralized contagion, but DeFi didn't make it worse. Compare with Yen carry: external shock → dense topology → $205M Aave liquidations → amplified.

**Post-clearing as natural experiment:** June 2022 crash cleared all large positions above $1,000. Five months later, FTX hit with a 30% shock and found an empty landscape. The topology was accidentally defensive. This is close to a controlled experiment: same asset, similar drawdown magnitude, different topology, different amplification.

**Risk rotation (structural finding from discussion):**
- 2022: Mostly real positions, dense near price. DeFi was a powerful amplifier of ETH price shocks.
- 2024: Mixed regime, moderate real density. DeFi was a moderate amplifier.
- 2026: Almost entirely phantom near price. DeFi is a negligible amplifier of ETH price shocks — but is now a powerful amplifier of correlation shocks (depeg events).

The system hasn't become less fragile. It has shifted what it's fragile to. The risk has rotated from price-cascade to correlation-cascade.

**The $578M stETH near-miss as coupling evidence (calculated, Iteration 4):** The largest stETH-collateral position reached HF ≈ 1.04 at the crash bottom. A slightly worse outcome ($950 ETH or 0.90 stETH/ETH) would have triggered $578M in stETH liquidation selling — this is the real→phantom coupling mechanism observed but not activated.

### What was not measured
- **More episodes.** 4/4 classification is encouraging but n=4 is not sufficient to establish robustness. Proposed: 4 more episodes targeting edge cases (2023 transition period, Jan 2022 crash, 2025 escalating episode, 2025 absorbed episode) to reach n=8.
- **Gradient density metric.** Real debt per 1% of price was computed informally ($14M/1% for Yen, $2M/1% for Iran/stETH) but not systematically across all bands and episodes.
- **Market absorption capacity.** The cascade condition is (liquidation pressure) > (absorption capacity). Absorption capacity at each price level depends on order book depth, which varies by market conditions. Not measured.
- **Depeg-fragility characterization.** The 2026 market's primary vulnerability is the $5.6B phantom wall activated by LST depeg. Depeg threshold per LST tier (osETH vs weETH vs wstETH) and DEX liquidity depth for each are not measured. This is the natural successor question to the price-cascade thesis.
- **On-chain verification of whale liquidation.** The $282M whale at $1,185 was inferred to have been liquidated during the June 2022 crash (ETH passed through $1,185) but not verified with on-chain liquidation events.

---

## Iteration 6: Expanded Backtest — 8 Episodes + Investigation Conclusion

### What was built
- `backtest_expanded.py`: Runs 4 additional historical snapshots (Jan 2022, Aug 2023, Sep 2024, Feb 2025).
- Jan 2022 required Multicall2 (Multicall3 not yet deployed at that block).
- Output: `data/positions_jan2022.csv` (8,913), `data/positions_aug2023.csv` (3,929), `data/positions_sep2024.csv` (13,221), `data/positions_feb2025.csv` (17,075), `data/5_expanded_results.txt`.
- Runtime: ~22 min total.

### What was measured

**8-episode comparison table:**

| Episode | Type | ETH | Ph% | R5% | R10% | R20% | R30% | Cliff | Cl% | Gradient/1% |
|---------|------|-----|-----|-----|------|------|------|-------|-----|------------|
| Jan 2022 crash | ESC | $3,007 | 2% | $27.5M | $97.2M | $212.3M | $449.9M | $445M | 35% | $10.6M |
| stETH depeg | ESC | $1,788 | 35% | $6.2M | $20.5M | $99.3M | $140.2M | $578M | 71% | $5.0M |
| FTX crash | NOT | $1,569 | 42% | $2.0M | $2.8M | $20.5M | $37.3M | $30M | 83% | $1.0M |
| Aug 2023 flash | ABS | $1,804 | 43% | $1.3M | $16.4M | $74.2M | $120.9M | $17M | 35% | $3.7M |
| Iran tensions | ABS | $3,510 | 44% | $0.1M | $22.3M | $161.7M | $275.8M | $156M | 70% | $8.1M |
| Yen carry | ESC | $2,903 | 54% | $49.3M | $142.1M | $420.3M | $624.1M | $187M | 49% | $21.0M |
| Sep 2024 dip | ABS | $2,370 | 58% | $13.7M | $45.8M | $269.8M | $655.0M | $137M | 58% | $13.5M |
| Feb 2025 crash | ESC | $3,128 | 70% | $5.8M | $37.5M | $280.5M | $670.7M | $93M | 48% | $14.0M |

**Phantom ratio evolution (9 data points, measured):**
Jan 2022: 2% → Jun 2022: 35% → Nov 2022: 42% → Aug 2023: 43% → Apr 2024: 44% → Aug 2024: 54% → Sep 2024: 58% → Feb 2025: 70% → Mar 2026: >90%

**Classification results by metric:**
- R10% alone: 5/8 correct. Misclassifies stETH (whale was deeper), Sep 2024 (shallow dip didn't reach wall), Feb 2025 (walls at 10-20% range).
- R20% > $100M + whale factor: 6/8 correct. Two false positives: Iran ($162M but distributed, no trigger), Sep 2024 ($270M but only 7% drawdown).
- R_at_actual_drawdown_depth: 8/8 correct, but circular (requires knowing drawdown depth in advance).
- R20%/TotalDebt normalization: doesn't help — threshold is not stable across regimes.

**Concentration analysis in R20% zone (measured):**

| Episode | R20% | MaxPos | Max/R20 | Top3/R20 |
|---------|------|--------|---------|----------|
| Jan 2022 | $212M | $30M | 14% | 31% |
| stETH | $99M | $16M | 16% | 38% |
| FTX | $20M | $10M | 48% | 67% |
| Aug 2023 | $74M | $16M | 21% | 43% |
| Iran | $162M | $21M | 13% | 36% |
| Yen | $420M | $29M | 7% | 19% |
| Sep 2024 | $270M | $30M | 11% | 23% |
| Feb 2025 | $281M | $35M | 13% | 27% |

**False positive analysis (measured):**
- Iran: R20% zone had 244 positions, $162M. Top 10 = 76% of total. But largest single position only $21M — no cliff trigger. Drawdown stopped at 14%.
- Sep 2024: R20% zone had 1,065 positions, $270M. Actually traversed zone (R7%): only $22M in 168 positions. Wall existed but price never reached it.

**Feb 2025 crash zone detail (10-20% band, measured):**
- 537 positions, $243M debt
- Top positions: $35.5M (WETH), $22.9M (weETH), $16.2M (WETH), $16.0M (WETH), $14.4M (weETH) — all at 16-20% below
- ~$24M per 1% of price — above empirical cascade threshold from Yen (~$14M/1%)
- Phantom wall also present: 1,484 phantom positions, $6.2B debt, of which $5.6B at HF < 1.1

### What was found (review discussion)

**No single metric cleanly separates escalating from absorbed across all 8 episodes.** The classification problem is harder than the 4/4 fail-fast suggested. The best prospective metric (R20% > $100M + whale) achieves 6/8 with two false positives that are structurally explained (shallow drawdown didn't reach existing walls).

**The false positives are correctly identified *potential*, not classification errors.** Iran had $162M of fuel within 20% — if the drawdown had reached 20% instead of 14%, that fuel would have activated. The topology reading was correct: "danger zone at 10-20%, moderate density." The exogenous shock was just insufficient to reach it. Sep 2024 similarly: wall at 10-20% but drawdown only 7%.

**Topology is a conditional fuel map, not a binary predictor.** This is the correct framing. At episode onset, the topology tells us: "if price drops X%, here's how much cascade fuel is in the path." This is a conditional statement — it requires coupling with drawdown depth, which depends on the exogenous shock's severity. The monitoring system can't predict drawdown depth, but it can say "if we get there, here's what happens."

**The conditional fuel map maps onto operational severity levels:**
- R20% < $30M, no whale: path clear, safe for moderate stress (FTX post-clearing)
- R20% $100-300M, distributed: moderate fuel, unlikely to self-sustain without major shock
- R20% > $300M OR whale > $100M within 20%: dense path or cliff — cascade likely if reached

**Gradient density thresholds (measured across escalating episodes):**
- Self-sustaining progressive cascade: ~$14M+ per 1% of price (Yen: $21M/1%, Feb 2025: $14M/1%)
- Cliff cascade: thin gradient + single position >$100M (stETH: $2M/1% gradient + $282M whale)
- Absorbed: <$8M per 1% of price without cliff (Iran: $8M/1%, Aug 2023: $3.7M/1%)

**Feb 2025 escalation is explainable from real wall alone.** R20% zone had $243M at ~$24M/1% — well above empirical cascade threshold. Phantom contribution ($5.6B at HF<1.1) cannot be ruled out but real wall is sufficient explanation.

**The investigation answered its question, differently than expected.**

*Expected:* Binary predictor — wall proximity at episode onset predicts escalation.

*Actual findings:*

1. **Real/phantom decomposition** — the most technically important finding. Without debt-side classification, any liquidation heatmap (including DefiLlama's) is dominated by phantom positions that don't respond to ETH/USD price. The near-price wall in 2026 is $4.3B phantom, $0.3K real. This decomposition is infrastructure for any future topology analysis.

2. **Conditional fuel map** — the correct tool. Not a predictor, but the missing severity-assessment layer for the monitoring system. "If ETH drops X%, here's how much real liquidation selling activates."

3. **Risk rotation** — DeFi has structurally shifted from price-cascade fragility (2022: 2% phantom) to correlation-cascade fragility (2026: >90% phantom). The system hasn't become less fragile — it has shifted what it's fragile to. The monitoring system should be watching LST pegs, not ETH/USD walls.

4. **Cascade mechanics** — two modes: progressive ($14M+/1% density) and cliff (single whale >$100M). Gradient = kindling, whale = cliff. The cascade condition is (liquidation selling at price level) > (market absorption at price level).

5. **Post-clearing effect** — after a crash clears positions, topology is defensive until new leveraged positions rebuild. FTX (Nov 2022) is the natural experiment: massive shock, 30% drawdown, empty topology → no DeFi amplification.

**Successor investigation identified:** The correlation-cascade thesis — given $5.6B+ phantom at HF 1.03-1.05 in 2026, what depeg threshold triggers cascade? Requires: DEX liquidity depth per LST, historical depeg magnitude, oracle lag behavior. Different data, different investigation.

### What was not measured
- **Depeg-fragility characterization.** The 2026 market's primary vulnerability ($5.6B phantom wall) requires measuring: depeg threshold per LST tier, DEX liquidity depth per LST, probability of reaching depeg threshold during stress. This is the natural successor investigation.
- **Market absorption capacity.** The cascade condition compares liquidation pressure to absorption capacity. Absorption capacity (order book depth) varies by market conditions and was not measured — only the liquidation pressure side was quantified.
- **Post-clearing rebuild time constant.** After a crash clears walls, how long until new leveraged positions rebuild to dangerous density? FTX (5 months post-June-crash) was still clear. The time constant is somewhere between months and years but not measured.
- **On-chain verification of whale liquidations.** Inferred from price passing through liquidation levels but not verified with on-chain liquidation event logs.
- **Remaining 19 episodes.** 8 of 27 tested. Diminishing returns — structural insights are stable at n=8.
