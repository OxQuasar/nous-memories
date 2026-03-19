# MEV Program Thesis

## Context

DeFi in 2026 is a $95-140B TVL system dominated by lending (80% of activity), liquid staking, and tokenized RWAs. The institutional layer is fundamentally a shadow banking system built on smart contracts — recursive leverage loops where collateral is deposited, borrowed against, redeployed, and restaked in chains that exist outside traditional balance sheet reporting and capital adequacy rules.

This leverage topology is fully transparent on-chain. Every position, every liquidation threshold, every collateral ratio is public data. This is an information asymmetry in reverse — the data is open, but few are systematically reading it.

## Observation

The DeFi leverage machine creates mechanical price relationships:

**Expansion cycle:** Asset price rises → collateral value rises → borrowing capacity increases → more borrowing → buy more assets → price rises further. Observable as: TVL growth, stablecoin supply expansion, borrowing utilization climbing, bridge inflows.

**Contraction cycle:** Asset price drops → collateral ratios deteriorate → liquidations trigger → forced selling → price drops further → cascade. Observable as: liquidation spikes, stablecoin supply contraction, TVL collapse in USD terms while token-denominated TVL holds, bridge outflows. October 2025's $19B liquidation cascade is this loop unwinding.

**The signal set is uniquely legible:**
- Aggregate collateral deposited across Aave/Maker/Compound/Morpho — real-time leverage gauge
- Liquidation threshold distribution — known price levels where forced selling activates
- Stablecoin supply dynamics (DAI, GHO, USDS mint/burn) — proxy for leverage expansion/contraction
- stETH/ETH, cbETH/ETH ratios — stress indicators in the liquid staking leverage chain
- Borrowing utilization rates — how close the system is to capacity
- Bridge flows between chains — risk-on/risk-off capital rotation
- DeFi TVL in token-denominated vs USD terms — divergence reveals real deposit flows vs price effects

## Thesis

There are two distinct opportunity layers:

### Layer 1: Macro Leverage Signals → Directional Positioning

Monitor the on-chain leverage topology to identify:
- **Leverage accumulation phases** — borrowing utilization rising, stablecoin supply expanding, collateral ratios healthy but thinning. Signals continued upward pressure.
- **Fragility thresholds** — liquidation walls at specific price levels where forced selling volume would exceed available liquidity. Signals cascade risk.
- **Unwind events** — liquidation rate spiking, stablecoin supply contracting, bridge outflows accelerating. Signals active contraction.

This is the on-chain equivalent of monitoring repo markets, margin debt, and VIX. The edge is that the data is fully transparent and real-time, but underutilized because most participants are focused on micro-level trading, not macro-level regime detection.

### Layer 2: Micro-Structural MEV (Evolution of Freya)

The cyclic DEX arbitrage Freya was built for still exists but the competitive landscape has shifted:

- **Ethereum L1**: Saturated. PBS/Flashbots mean searchers pay 90%+ of revenue to proposers. Not viable without builder integration.
- **Established L2s (Arbitrum, Optimism, Base)**: Moderate competition. Base has private mempool with 80%+ extraction by two entities. Arbitrum more accessible.
- **Emerging chains (Sonic, Monad, HyperEVM)**: MEV infrastructure still developing. Wider margins. Fewer competitors. This is where Freya's block-level design could still work.
- **Niche markets**: Newly launched tokens, smaller DEXes on any chain where sophisticated operators haven't deployed yet.

Key constraint: Freya's block-level-only design (no mempool, no Flashbots) is structurally disadvantaged on chains with mature MEV infrastructure. It can only capture opportunities visible in confirmed state — leftovers after the builder auction. Viable only on chains where that infrastructure doesn't exist yet.

### Synthesis

The higher-value play is Layer 1 — building the on-chain equivalent of macro risk monitoring. The data infrastructure to:
1. Map the leverage topology across major lending protocols and chains
2. Identify liquidation cascade price levels in real-time
3. Detect regime transitions (accumulation → fragility → unwind)
4. Generate actionable signals for directional positioning or hedging

Layer 2 (micro-arb) can run in parallel on underserved chains, but it's a declining-margin business as MEV infrastructure proliferates. Layer 1 is a structural edge that grows more valuable as DeFi leverage grows more complex.

## Open Questions

- What is the actual correlation strength between on-chain leverage metrics and subsequent price action? Needs backtesting against historical data (Aave TVL, stablecoin supply, liquidation events vs ETH/BTC price).
- How fast do liquidation cascades propagate across chains? Is there a measurable lag between Ethereum liquidations and L2/alt-chain contagion that creates a trading window?
- Are there existing tools/dashboards that aggregate this data, or is the monitoring infrastructure itself a gap?
- What's the minimum viable data pipeline? Which protocols and metrics provide the highest signal-to-noise for regime detection?
- How do AI "solvers" (the automated capital allocators now entering DeFi) change the dynamics? Do they dampen cascades or amplify them?
- Is the RWA tokenization layer creating new correlation channels between TradFi rates and DeFi leverage that didn't exist before?
