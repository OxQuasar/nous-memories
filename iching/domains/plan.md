# Domains — Plan

## Protocol: Steps 0–4 (from Iteration 3)

The grammar makes one structural prediction for any Q₃ domain, invariant under all axis assignments:

- **Step 0:** Verify transitions are predominantly single-axis (Q₃ edges)
- **Step 1:** Identify the axis where ALL transitions are disruptive → pure-克 axis
- **Step 2:** Identify the axis where NO transitions are disruptive → doublet axis
- **Step 3:** Verify the mixed axis has exactly 2/4 destructive transitions
- **Step 4:** Test GMS (no consecutive 克) on the P₄ paths (~30–40 transitions)

Steps 1–3 require classifying transition character only. Step 4 requires sequential data.

---

## Market Regime Test

### Data

`memories/markets/data/`:
- `btc_datalog_2025-07-21_2026-02-20.csv` — 18.5M rows, 1-second BTC data with pre-computed trend, vol, order book fields. 7 months.
- `btc_datalog_2026-02-20_2026-03-13.csv` — out-of-sample continuation (~3 weeks)
- `btc_1m_2023-01-01_2024-12-31.csv` — 1M rows, 1-minute OHLCV. 2 years. Longer history but fewer derived fields (trend/vol/liquidity must be computed from price + volume).

The datalog has a pre-built `tris_last_regime` column with 12 states (Bull/Bear/Flat × High/Low LogR × High/Low Vol). This is 3×2×2 = 12, not 2³ = 8. Trend is ternary. We need to construct our own binary axes from raw fields.

### Step 1: Resample

1-second data is too granular — regime transitions at that scale are noise. Resample to 4h bars (matching the trend/vol computation horizons). Each 4h bar gets one 3-bit regime label.

For the 7-month datalog: ~1,260 bars at 4h. For the 2-year 1m data: ~4,380 bars at 4h. Both well above the ~100 transitions needed for Steps 1–3 and ~30–40 for Step 4.

### Step 2: Construct three binary axes

From the datalog's raw fields:

| Axis | Field | Binary rule | Bit |
|------|-------|-------------|-----|
| Trend | `trend_4h` | positive → 1, negative → 0 | b₀ |
| Volatility | `realized_vol_4h` | above rolling median → 1, below → 0 | b₁ |
| Liquidity | `spread_bps_1m` (avg over bar) | below median → 1 (abundant), above → 0 (scarce) | b₂ |

**Threshold:** Rolling median over a trailing window (e.g., 30-day for vol, 7-day for spread). Median split is the simplest — exactly 50/50 by construction.

**Zero-crossings on trend:** `trend_4h` near zero (flat market) needs handling. Options: (a) sign only, ignore magnitude — simplest but noisy. (b) Require |trend_4h| > threshold — excludes flat periods. (c) Use `trend_8h` or `trend_24h` for a smoother signal. Start with (a), test (b) for robustness.

For the 1m OHLCV (no pre-computed fields): compute trend = sign of 4h return, vol = realized vol of 1m returns over 4h window, liquidity = average volume over 4h bar vs rolling median.

### Step 3: Assign Q₃ vertex and extract transitions

Each 4h bar → 3-bit label → Q₃ vertex → trigram → element. Consecutive bars produce a transition sequence. Classify each transition:
- Single-axis flip → Q₃ edge → typed as 比和/生/克 by the canonical assignment
- Multi-axis flip → not a Q₃ edge → categorize separately

### Step 4: Run protocol

**Step 0 (prerequisite):** What fraction of consecutive-bar transitions are single-axis (Q₃ edges)? If < 50%, the data doesn't prefer Q₃ adjacency and the grammar may not apply. If significantly > 33% (the random baseline for 3-of-7 non-self neighbors being Q₃-adjacent), there's a signal.

**Steps 1–3 (axis identification):**
- For each single-axis transition, measure "disruption" — e.g., absolute return over next bar, or spread widening, or vol increase. Something that captures transition cost.
- Partition by which axis flipped.
- Test: is vol-axis disruption > trend-axis disruption > liquidity-axis disruption?
- Prediction: vol flips uniformly high disruption (pure-克), liquidity flips uniformly low disruption (doublet), trend flips bimodal (mixed 2:2).

**Step 4 (GMS bigram test):**
- Extract all consecutive 克-type transitions.
- Count 克→克 bigrams.
- Compare against null: P(克→克) = 0.278 for uniform random walk on Q₃ (from Iteration 2).
- Under GMS: P(克→克) = 0.
- Need ~30–40 transitions along P₄ paths for detection at p<0.05.

### Step 5: Robustness

- **Bar size:** Repeat at 1h, 8h, daily. Does the structure survive across timescales?
- **Threshold:** Test quartile splits, fixed percentiles, adaptive thresholds.
- **Axis permutation:** Test all 6 assignments of (trend, vol, liquidity) to (b₀, b₁, b₂). The algebra predicts one axis is always pure-克 regardless of permutation — but which physical axis it is depends on the assignment.
- **Out-of-sample:** Run on the Feb-Mar 2026 continuation file.
- **Longer history:** Run on the 2023-2024 1m data (different market regime — bear-to-bull transition).

### What we expect

**Honest null:** Market regime transitions are probably not constrained by Z₅ algebra. The grammar operates on typological relations, and there's no reason physical market axes should align with the canonical 五行 surjection. A null result is expected and informative — it means the three binary axes exist but the Z₅ typing doesn't add predictive power beyond the raw axes.

**What would be surprising:** If Steps 1–3 show axis-type alignment (one axis uniformly disruptive, one uniformly benign) matching the algebraic prediction. This would mean the Z₅ typing captures something real about how market regime changes differ in character — not because markets follow I Ching algebra, but because any system with three genuinely independent binary oppositions might exhibit the {4,2+2,2+2} axis-type structure.

**What would be very surprising:** If Step 4 shows GMS suppression. That would mean consecutive destructive regime transitions are genuinely forbidden in market dynamics — a strong structural claim about regime change sequencing.

---

## TCM 八纲辨证 Test

Parked. Requires:
1. Verification of the traditional trigram-line ↔ diagnostic-axis mapping
2. Clinical progression data through the 8 diagnostic categories
3. Pre-treatment natural history (to avoid self-fulfilling prophecy from 五行-guided treatment)

Priority is below the market test because of data sourcing difficulty. But the mapping (D1.1–D1.2) could be investigated from classical texts without clinical data.

---

## Execution Order

1. **Market regime test** — data in-house, protocol concrete, can start immediately
2. **TCM mapping verification** — text research only, no clinical data needed
3. **TCM clinical test** — requires external data, lowest priority
