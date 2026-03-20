# Links — Signal Synthesis

## Signals Ranked by Lead Time and Strength

### Tier 1: Strong, quantified, survives controls

| Signal | Lead time | Strength | Evidence |
|--------|-----------|----------|----------|
| **Liquidation count (Aave)** | Contemporaneous + 5-day persistence | Spearman r=-0.263 (7d partial, p=1.2e-25) | Monotonic gradient: 500+ liqs/day → -1.96% ETH residual. Survives BTC return control. Doubles in crash regimes (-0.287 vs -0.144 calm). |
| **VIX level** | Contemporaneous (regime indicator) | Monotonic: Q1 0.228 → Q4 0.512 ETH/S&P coupling | Determines whether ETH couples to equities. High VIX = strong, stable coupling (std 0.127). Low VIX = decoupled, unstable (std 0.238). |
| **BTC return** | Contemporaneous | Pearson r=+0.822 with ETH return | Baseline: ETH moves 0.979:1 with BTC. The residual after BTC+S&P control is where DeFi amplification lives. |
| **S&P 500 return** | Contemporaneous | Pearson r=+0.425 with ETH return | ETH adds 0.506x S&P sensitivity on top of BTC. Coupling doubles from 0.23 to 0.51 as VIX rises. |

### Tier 2: Informative but limited

| Signal | Lead time | Strength | Evidence |
|--------|-----------|----------|----------|
| **VIX change** | Contemporaneous | Pearson r=-0.361 with ETH return | Strong same-day signal but no daily lead/lag. Transmission is sub-daily. |
| **DXY return** | Contemporaneous | Pearson r=-0.129 with ETH return | Weak inverse. Dollar strength hurts ETH mildly. |
| **ETH/BTC ratio** | Structural trend indicator | First-class crash variable (mult 1.26-2.14x) | Macro crashes show higher ETH/BTC drawdown multiples. The ratio's behavior *during* crashes isolates ETH-specific dynamics. |

### Tier 3: Noise — do not revisit

| Signal | Result | Why noise |
|--------|--------|-----------|
| **Borrow growth (30d)** | Spearman r=+0.007, p=0.81 | Definitive null across all calm periods, pre/post-2024 splits, and 1-30 day lags. DeFi leverage rebuilding does not explain ETH/BTC decline. |
| **Total borrowed (level)** | r=+0.009 with ETH/BTC return | Near-zero at daily frequency. Level correlates with yield spread (r=0.762) but both are co-symptoms of macro regime, not operationally connected (daily changes r=-0.030). |
| **Fed funds rate** | ETH/S&P coupling monotonic but time-confounded | Each rate regime maps to one time period. Cannot separate rate effect from period/maturation effects. |
| **Utilization rate** | r=-0.023 with ETH return | Noise. |
| **Gold return** | r=+0.057 with ETH return | No relationship. |
| **10Y Treasury yield (level)** | r=+0.024 with ETH return | No relationship at daily frequency. |
| **Yield spread (level)** | r=-0.003 with ETH/BTC return | No operational connection despite high correlation with borrow levels. |
| **CPI** | Not tested individually | Monthly frequency, forward-filled. Too slow to matter at daily resolution. |

## Composite Signal Construction

The winners suggest a two-layer composite:

**Layer 1 — Regime detection (VIX-based):**
- VIX < 15: Low coupling regime. ETH/S&P correlation ~0.23. Crypto moves on its own narratives.
- VIX 15-22: Transition zone. Coupling rising (0.28-0.43).
- VIX > 22: High coupling regime. ETH/S&P correlation ~0.51. Macro drives crypto.

**Layer 2 — Amplification detection (liquidation-based):**
- Aave liquidation count < 50/day: No measurable amplification (residual ≈ 0).
- 50-200/day: Amplification active. -0.63 bps per event (ramp phase). Maximum marginal damage.
- 200+/day: Amplification continuing but concave. -0.23 bps per event. Watch for exhaustion reversal.

**Combined interpretation:**
- High VIX + rising liquidation count (50-200 range): Maximum danger. Macro stress coupling ETH to equities while DeFi cascade amplifies. ETH-specific damage accumulating at 5-7 day timescale.
- High VIX + peak/declining liquidation count (500+): Exhaustion approaching. Damage mostly done. Watch for reversal.
- Low VIX + rising liquidation count: Crypto-specific event. ETH-specific damage present but no macro amplifier. Smaller total impact (2x less daily damage than macro crashes).
- Low VIX + low liquidation count: Baseline. No amplification.

**What's missing from the composite:**
- No leading indicator. All signals are contemporaneous at daily resolution. The composite detects the current state, not future states.
- The 2025 January rotation (-11.2% residual, 18 liqs/day, low VIX) would not have been detected by this composite. ETH-specific rotation outside of DeFi and macro channels remains unmodeled.
- Aave liquidation count is a proxy (~2% R² of residual variance). Total forced selling across all venues would be a stronger signal but is harder to measure.

## Next Step Assessment

**What's been answered:**
- Does DeFi amplify crashes? Yes, quantified with three-mode framework.
- What connects external events to DeFi cascades? VIX regime determines coupling. Crash-chaining prevents recovery.
- Transmission path? Sub-daily macro→crypto, 5-7 day DeFi cascade.
- Chronic vs acute? Acute only. Borrow growth null is definitive.

**What would deepen this but with diminishing returns:**
- THORChain cross-chain flow data — would add "where money goes" (stables vs BTC rotation) but won't change amplification coefficients.
- Hourly data — would resolve sub-daily transmission timing but daily resolution already answers the key questions.
- Oracle-separated liquidation analysis — would decompose amplification into market-risk vs oracle-design components. Data exists from Correlation phase. Moderate value.

**What would be genuinely new:**
- Real-time liquidation monitoring pipeline — applying the composite signal to live data. The three-mode framework suggests an actionable sequence: detect ramp phase early (50-200 liqs/day) → expect 5-7 day cascade → watch for exhaustion signal (peak liqs) → position for reversal.
- 2025 January rotation forensics — institutional flow data, ETH ETF flows, on-chain wallet clustering. Would explain what initiates the worst crash type (non-DeFi ETH-specific rotation).
- Cross-cycle comparison — this dataset covers one full cycle (2022-2026). The next cycle's crashes would test whether the amplification coefficients and three-mode framework are stable or cycle-specific.

**Recommendation:** The Links investigation is complete for its planned scope. The findings integrate cleanly with prior phases (Flow, Position, Correlation, Dynamics). The natural next step depends on the broader research direction — if operational, build the real-time pipeline; if research, pursue the January 2025 forensics or oracle decomposition.
