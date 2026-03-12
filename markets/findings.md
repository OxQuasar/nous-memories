# Market Regime Dynamics: Consolidated Findings

> BTC intraday, 214 days (Jul 2025 – Feb 2026), 61,920 5-min bars.
> Method: binary trigram construction → 8-state transition matrices → spectral analysis → lumpability testing.

---

## 1. The (3,5) Test: Clean Negative

The Z₅ surjection hypothesis — that 8 binary market configurations collapse to 5 functional regime types — is definitively rejected.

**Evidence:**
- K=4 (not 5) across 3 independent binary bases, by eigenvalue gap analysis
- All 240 complement-equivariant surjections exhaustively tested
- Best K=5 lumpability error: 1.6×10⁻³ — **19× worse** than K=4 complement pairs (8.4×10⁻⁵)
- Best K=5 spectral gap: 0.30 (predicted 0.71)
- Best K=5 top-3 concentration: 68.6% (predicted 89%)

**What (3,5) got right:** Complement symmetry. The x ↦ x⊕7 involution is confirmed as a symmetry of the transition dynamics (all 4 complement pairs JSD < 0.09, degenerate T₈ eigenvalue pairs). This is the necessary condition; the sufficient conditions fail.

---

## 2. Four-Regime Directed Cycle

The market operates on a directed 4-state cycle:

```
Bear (C0) → Reversal (C1) → Bull (C3) → Pullback (C2) → Bear (C0) → ...
```

**Basis A** (trend_1h × trend_8h × trend_48h) jump chain:

|  | C0 bear | C1 reversal | C2 pullback | C3 bull |
|--|---------|-------------|-------------|---------|
| C0 | — | **0.925** | 0.076 | **0.000** |
| C1 | **0.795** | — | **0.000** | 0.205 |
| C2 | 0.230 | **0.000** | — | **0.770** |
| C3 | **0.005** | 0.075 | **0.919** | — |

**Properties:**
- 4 structural zeros: stage-skipping is forbidden
- Near-uniform stationary distribution: 22.6%–28.1% per regime
- Two coupled 2-cycles: {C0↔C1} bearish, {C2↔C3} bullish
- Stable across three 71-day subperiods (Frobenius 0.03–0.12)
- 794 regime episodes total, ~6–7h mean duration each

**Evidence strength: STRONG.** Robust across bases, stable across subperiods, physically interpretable.

---

## 3. Complement Symmetry (Coherence Parity)

**Basis D** (tot_8h × trend_8h × realized_vol_8h): all 4 complement pairs have near-identical transition dynamics under relabeling.

| Complement Pair | JSD | Description |
|----------------|-----|-------------|
| S0 (000) ↔ S7 (111) | 0.087 | calm-bear-decel ↔ volatile-bull-accel |
| S1 (001) ↔ S6 (110) | 0.074 | calm-bear-accel ↔ volatile-bull-decel |
| S2 (010) ↔ S5 (101) | 0.046 | calm-bull-decel ↔ volatile-bear-accel |
| S3 (011) ↔ S4 (100) | 0.048 | calm-bull-accel ↔ volatile-bear-decel |

**Algebraic confirmation:** T₈ eigenvalues show degenerate pairs (0.968, 0.968) and (0.957, 0.957) — signature of an involutory symmetry.

**Interpretation:** The market distinguishes *coherent* from *incoherent* states, not up from down. A clean downtrend and a clean uptrend are the same *kind of state* (all signals aligned). Inflection points (signals disagreeing) are structurally distinct from aligned states, regardless of direction.

**Evidence strength: STRONG.** Algebraically confirmed (degenerate eigenvalues don't arise from noise), all 4 pairs pass, physically interpretable.

---

## 4. Exit Sub-State Confirmation Signal

The fast bit (trend_1h) at the moment of regime exit predicts next regime direction and quality. This is a **general property** of the 8-state chain, not specific to any one regime.

### C2 Pullback Exit (strongest instance)

| Exit sub-state | → Bear | → Bull | n |
|----------------|--------|--------|---|
| S4 (trend_1h↓) | 51% [39%, 63%] | 49% | 65 |
| S5 (trend_1h↑) | 8% [5%, 14%] | **92%** [86%, 96%] | 122 |

**Subperiod stability:**

| Period | S5 → bull |
|--------|-----------|
| Jul–Sep 2025 | 92.1% |
| Oct–Dec 2025 | 92.7% |
| Dec 2025–Feb 2026 | 90.7% |

### Forward-Looking Returns

The exit sub-state predicts the NEXT regime's quality:

| Source → Dest | n | Mean Return | Duration |
|---------------|---|-------------|----------|
| C2-S5 → C3 (confirmed pullback → bull) | 111 | **+0.09%** | 7.6h |
| C2-S4 → C3 (uncertain pullback → bull) | 32 | **−0.17%** | 4.3h |
| C2-S5 → C0 (rare failure → bear) | 10 | **+0.12%** | 4.2h |
| C3-S7 → C2 (orderly bull → pullback) | 52 | **+0.06%** | 5.6h |
| C3-S6 → C2 (sharp bull → pullback) | 119 | **−0.24%** | 6.9h |

Confirmed pullbacks that fail produce shallow, short bears. Uncertain pullbacks that succeed produce anemic, short bulls. The exit sub-state carries forward.

### What This Is NOT

**Not a trading trigger.** Intra-episode flips are noise: ~3 S4↔S5 flips per C2 episode, each indistinguishable in real-time. Confirmed-flip trading: 511 trades, 38.4% win rate, +0.005% mean return. Near zero.

**It IS a confirmation signal.** Observable with 5-minute latency at regime transition. Applicable to position sizing: full conviction on S5 exits, reduced conviction on S4 exits.

**Evidence strength: MODERATE-TO-STRONG.** The pattern is stable and generalizes across transitions. But 122 S5 exits over 214 days is sufficient for confidence intervals, not overwhelming. In-sample only.

---

## 5. C1 Reversal: Asymmetric Payoff

| Exit | Probability | Mean Return | Character |
|------|------------|-------------|-----------|
| C1 → C3 (breakthrough) | 20% | +1.09% | Fast, large |
| C1 → C0 (failure) | 80% | −0.25% | Slow, small |

- Unconditional long EV: +0.018% (not tradeable — high variance)
- S3-conditioned EV: +0.14% (n=69, thin sample)
- The payoff asymmetry (4.4× win/loss ratio) partially compensates the low win rate

**Evidence strength: MODERATE.** Pattern is clear but n=43 breakthroughs is thin. S3 conditioning further thins the sample.

---

## 6. Duration Characteristics

| Regime | Episodes | Mean | Median |
|--------|----------|------|--------|
| C0 bear | 211 | 6.9h | 5.6h |
| C1 reversal | 210 | 6.1h | 5.6h |
| C2 pullback | 187 | 6.2h | 5.8h |
| C3 bull | 186 | 6.7h | 5.9h |

**Pullback duration asymmetry:** C2→bear exits have median 3.9h (fast, sharp). C2→bull exits have median 5.8h (gradual, soaking). Fast pullback = danger. Slow pullback = resolution.

**Evidence strength: MODERATE.** Consistent pattern, physically interpretable, but duration alone isn't discriminating enough for trading.

---

## 7. What Was Tried and Failed

| Approach | Result | Lesson |
|----------|--------|--------|
| K=5 surjection (3,5) | Rejected, 19× worse lumpability | Market has 4 regimes, not 5 |
| Basis B (volume profile) | Disqualified — no structure | VP distances don't produce stable discrete dynamics |
| Intra-episode flip triggers | Near-zero edge (+0.005%) | Signal is at boundaries, not within regimes |
| Entry state prediction | Uninformative (76% vs 79%) | Resolution is determined at exit, not entry |

---

## 8. Caveats

- **In-sample only.** 214 days of BTC. Structural patterns (regime count, cycle topology, complement symmetry) likely general. Exact numbers (92%, +0.20%, 6.5h) are sample-specific.
- **Single asset.** No multi-asset validation. The directed 4-cycle is probably universal (it's the standard market cycle); complement symmetry is the more fragile claim.
- **Subperiod stability ≠ out-of-sample.** Three consistent 71-day windows are encouraging but drawn from the same market environment.
- **Small-n paths.** C2-S5→C0 (n=10), C1 S3-conditioned breakthrough (n=20). Wide confidence intervals.

---

## 9. Open Questions

1. **Out-of-sample:** Does S5→bull > 85% hold on BTC 2023-2024 and post-Feb 2026?
2. **Multi-asset:** Does the 4-regime cycle and complement symmetry hold for ETH, SPY, QQQ?
3. **Timescale variation:** Do 1h or 24h feature bases produce the same K=4 structure?
4. **Real-time indicator:** Current regime + sub-state + duration as a live dashboard signal
5. **Position sizing:** Exploit S5/S4 asymmetry (full size vs reduced size at regime transitions)
6. **Complement symmetry universality:** Does it hold for other orthogonal channel selections?

---

*Analysis: March 2026. Scripts: `logos/markets/01-06_*.py`. Raw outputs: `memories/markets/01-06_*_output.txt`. Full synthesis: `memories/markets/investigation-summary.md`.*
