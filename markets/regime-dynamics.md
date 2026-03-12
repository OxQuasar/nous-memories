# Market Regime Dynamics as Z₅ Relational Structure

## Core Thesis — Updated March 2026

The I Ching's Z₅ transition matrix was proposed as a structurally motivated, zero-parameter model for market regime dynamics. Not algebraically forced (the relations investigation R62–R68 proved the algebra doesn't generalize beyond F₂), but epistemologically grounded: markets share observer-participation architecture, partial visibility, and relational output.

**Empirical verdict: the (3,5) model is cleanly refuted for BTC intraday dynamics.** The market has 4 regime equivalence classes, not 5. The complement symmetry prerequisite holds, but K=5 fails across all tested bases and an exhaustive surjection search. See Investigation 1 results below.

**However, the investigation uncovered genuine market structure** that wouldn't have been found without the (3,5)-motivated methodology: complement symmetry (coherence parity), a directed 4-regime cycle with forbidden stage-skipping, and an exit sub-state confirmation signal. The method outlived the hypothesis.

---

## The Five Relations as Regime Types — Empirical Status

The conjectured mapping of Z₅ relations to market regimes was not confirmed. The market has 4 functional regime types, not 5:

| Empirical Regime | Character | Closest Z₅ analogue (if forced) |
|---|---|---|
| C0: Bear | All timescales aligned bearish | 克 (overcoming) |
| C1: Reversal | Short-term reversal in downtrend | Gateway state (no clean analogue) |
| C2: Pullback | Short-term pullback in uptrend | Gateway state (no clean analogue) |
| C3: Bull | All timescales aligned bullish | 生 (generating) |

The 4-state structure is two coupled 2-cycles ({C0↔C1} bearish, {C2↔C3} bullish), not the (3,5) architecture of two independent 5-cycles. The forced mapping to 5 Z₅ relations doesn't work — the market's natural regime count is 4.

---

## What Transferred from (3,5) and What Didn't

### Confirmed
1. **Complement symmetry.** The F₂³ complement involution (x ↦ x⊕7) IS a symmetry of the empirical transition dynamics. Market-opposite states (all-bearish-decelerating-calm ↔ all-bullish-accelerating-volatile) have identical transition behavior under relabeling. JSD < 0.09 for all 4 complement pairs, algebraically verified via degenerate T₈ eigenvalue pairs. This is "coherence parity": the market distinguishes aligned from misaligned, not up from down.

2. **Structural zeros.** Certain regime transitions are forbidden. Stage-skipping is structurally blocked: C0↛C3, C1↛C2, C2↛C1, C3↛C0. But these are 4-state zeros in a directed cycle, not the (3,5) stride-2→stride-1 zeros.

3. **Fast mixing within macro-regimes.** The coherence cycle (Basis D) has spectral gap 0.31. The trend cycle (Basis A) has fast mixing within each macro-pair (bear/reversal and bull/pullback), with slow cross-macro coupling (spectral gap 0.003).

### Refuted
1. **K=5.** Three independent bases all produce K=4 by eigenvalue gap. Exhaustive search of all 240 complement-equivariant surjections: best K=5 has lumpability error 19× worse than K=4 complement pairs.

2. **Spectral gap ≈ 0.71.** Best K=5 surjection: 0.30. The K=4 complement chain: 0.31.

3. **89% concentration on 3 types.** Best K=5: 68.6% top-3 concentration. K=4 stationary distribution is near-uniform (22–28% per regime).

4. **Two independent 5-cycles.** One directed 4-cycle instead.

### Not testable (structural mismatch)
- The 互 endomorphism's rank reduction (6→4→2) and single leak have no clean market analogue in a stochastic Markov chain.
- The P→H parity rotation has no identified market counterpart.
- The 2/5 visibility ceiling: the market has a 2-projection structure (trend view and coherence view provide orthogonal information), but it's 2 views × 4 states, not 2/5 of 5 states.

---

## Investigation 1: Results — Completed March 2026

**Full details:** `memories/markets/investigation-summary.md`

### What was tested
(3,5) predictions on BTC intraday data (214 days, 61,920 5-min bars). Four binary bases tested: trend timescales (A), volume profile (B, disqualified), flow×structure×activity (C), timescale-matched orthogonal channels (D).

### Result: K=4, not K=5

The market operates on a **4-regime directed cycle**:
```
Bear (C0) → Reversal (C1) → Bull (C3) → Pullback (C2) → Bear (C0) → ...
```

Key structural properties:
- 4 structural zeros (forbidden stage-skipping)
- Near-uniform stationary distribution (22.6%–28.1%)
- Complement symmetry confirmed (Basis D)
- K=4 lumpability error: 8.4×10⁻⁵ (nearly exact Markov at 4-state level)
- Stable across three 71-day subperiods

### Most actionable finding: exit sub-state signal

The fast bit (trend_1h) at regime exit predicts next regime quality. Strongest instance:

| C2 exit sub-state | → Bear | → Bull |
|---|---|---|
| S4 (trend_1h↓) | 51% | 49% |
| S5 (trend_1h↑) | 8% | **92%** |

Stable across subperiods (90.7%–92.7%). Not a trading trigger (intra-episode flips are noise), but a **confirmation signal** at regime transitions. Forward-looking: C2-S5 → C3 episodes have mean return +0.09%, while C2-S4 → C3 episodes have −0.17%. The exit sub-state predicts next regime quality, not just direction.

This generalizes across ALL regime boundaries (C3 exits show same pattern: S7→orderly, S6→sharp).

---

## Investigation 2: Observer-Participation — Status: OPEN (redesigned)

The original framing assumed 5 regimes and 2/5 visibility. With K=4 confirmed, the investigation redesigns as:

**Question:** Do the trend projection (Basis A: 4 Hamming-adjacent clusters) and coherence projection (Basis D: 4 complement-pair clusters) provide independent information about market dynamics?

**Preliminary finding (Phase 4):** The cross-basis contingency table shows weak coupling — the two projections capture largely independent information. C2 pullbacks overweight P0 (deceleration-aligned), but the correspondence is partial.

**Revised prediction:** Two orthogonal 4-state views × low mutual information → each view sees ~half the information. Not the (3,5) Fano-plane geometry, but a simpler 2-view complementarity.

---

## Investigation 3: Temporal Modulation — Status: OPEN (unchanged)

The temporal modulation question doesn't depend on K=5. The 4-regime cycle can still exhibit temporal modulation (calendar effects on transition probabilities). The perfect balance theorem prediction remains testable.

---

## The Algebraic Boundary — Sharpened

The uniqueness theorem Orbits(n,p) = 1 iff (n,p) = (3,5) remains valid mathematics. What's been empirically shown is that **the market doesn't instantiate this structure**. The complement symmetry (necessary condition) holds, but the surjection structure (sufficient condition) doesn't — the market prefers {2,2,2,2} complement-pair grouping over {2,2,2,1,1} type-0/1/2 grouping.

This sharpens the boundary: the epistemological parallels (observer-participation, partial visibility, relational output) are real but don't constrain the regime count. The market has its own structural logic — 4 regimes from 2 coupled oscillations — that doesn't map to Z₅.

---

## Provenance

Derived from:
- I Ching uniqueness theorem (iching/unification/unification.md)
- Z₅ transition matrix properties (iching/deep/open-questions.md, R15-R20)
- Cross-domain analysis — algebraic boundary (iching/relations/, R62-R68)
- **Empirical investigation** (markets/investigation-summary.md, March 2026)
  - 6-phase analysis, 3+ binary bases, exhaustive surjection search
  - Scripts: logos/markets/01-06_*.py
  - Raw outputs: memories/markets/01-06_*_output.txt
