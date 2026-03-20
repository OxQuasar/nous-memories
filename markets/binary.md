# Markets — Three Binary Axes on Q₃

## The Axes

Three independent binary regime descriptors:

| Axis | 0 | 1 | What it measures |
|------|---|---|------------------|
| b₀ | Down | Up | Trend direction |
| b₁ | Low | High | Volatility |
| b₂ | Scarce | Abundant | Liquidity |

Eight market regimes = Q₃ vertices:

| Binary | Regime | Character |
|--------|--------|-----------|
| 000 | Down, low vol, scarce liquidity | Quiet decline, illiquid |
| 001 | Up, low vol, scarce liquidity | Grinding rally, thin |
| 010 | Down, high vol, scarce liquidity | Panic, capitulation |
| 011 | Up, high vol, scarce liquidity | Short squeeze, melt-up |
| 100 | Down, low vol, abundant liquidity | Slow bleed, heavy |
| 101 | Up, low vol, abundant liquidity | Healthy bull, steady |
| 110 | Down, high vol, abundant liquidity | Selloff with bids, correction |
| 111 | Up, high vol, abundant liquidity | Euphoria, blow-off top |

## What the grammar would predict

Under the canonical 五行 assignment (same Z₅ typing as trigrams):

| Regime | Trigram | Element |
|--------|---------|---------|
| 000 | 坤 | 土 |
| 001 | 震 | 木 |
| 010 | 坎 | 水 |
| 011 | 兌 | 金 |
| 100 | 艮 | 土 |
| 101 | 離 | 火 |
| 110 | 巽 | 木 |
| 111 | 乾 | 金 |

**GMS prediction (E2):** Consecutive 克 regime transitions are suppressed. Two consecutive destructive relational shifts should be rarer than expected by chance.

**Valve prediction (E3):** After a 克 transition, the next transition must pass through 比和 or 生 before another 克.

**Single-bit transitions:** Q₃ edges = one axis flips while others hold. The grammar predicts these single-axis regime changes have typed character (比和/生/克) depending on which axis flips and which regime you're in.

## What's testable

1. Classify each trading day/week into one of 8 regimes by thresholding trend, volatility, and liquidity
2. Record the transition sequence
3. Check: are 克→克 transitions suppressed? Does the valve hold?
4. Compare against shuffled null

## Caveats

- **Axis definition:** Trend, volatility, and liquidity are continuous. Binarizing them introduces a threshold choice. Different thresholds produce different Q₃ paths. Need to test robustness across thresholds.
- **Axis independence:** Trend and volatility are correlated in practice (vol rises in downtrends). The axes aren't fully independent. This breaks the clean Q₃ structure — correlated axes mean some vertices are undersampled.
- **Axis assignment:** Which axis maps to b₀, b₁, b₂ matters — it determines the 五行 typing. The assignment above (trend=b₀, vol=b₁, liquidity=b₂) is one of 6 permutations. Each gives a different 五行 map. Need to either use a principled assignment or test all 6.
- **Temporal framing:** The grammar is typological, not temporal. Testing it on temporal sequences (day-to-day transitions) is projecting a relational structure onto time — exactly what the mod-8 investigation showed doesn't preserve the grammar. The stronger test would be: classify regime *pairs* (not sequences) and check whether the relational typing matches market behavior (e.g., do 克-typed regime pairs have higher drawdown risk?).

## Connection to fana

The fana document discretizes price returns into 8 bins via mod-8 on a scalar (price). This investigation would discretize market *state* into 8 regimes via 3 binary axes. The difference:
- Fana: 1D scalar → Z₈ → 先天 bijection → Q₃ labels (mod-8 investigation showed this can't access Q₃ grammar)
- Here: 3D binary state → Q₃ directly (no mod-8 intermediary, no bijection needed)

If the three axes are genuinely independent and binary, the Q₃ adjacency is intrinsic — single-axis regime changes ARE Q₃ edges. No permutation scrambles the structure. This is the native coordinate the mod-8 investigation said was needed.

## Open questions

**M1:** Do real market regime transitions prefer Q₃ edges (single-axis flips) over multi-axis jumps? If yes, Q₃ adjacency is empirically relevant.

**M2:** Under the canonical 五行 assignment, is the 克→克 suppression observable in market regime sequences?

**M3:** Is the typing robust across axis permutations (which axis is b₀/b₁/b₂), or does only one assignment produce structure?

**M4:** Does the relational typing (克 pairs = high risk) have portfolio management value beyond what the individual axes provide?
