# Markets Investigation — Exploration Log

## Iterations 1–3: (3,5) Test → Clean Negative
- K=4 across 3 independent bases (trend, volume profile, orthogonal channels)
- Complement symmetry confirmed (Basis D: JSD < 0.09 all pairs, degenerate eigenvalues)
- Exhaustive 240-surjection search: K=4 lumpability 19× better than best K=5
- (3,5) formally closed

## Iteration 4: Regime-Conditioned Returns
- 4-regime directed cycle: bear(C0) → reversal(C1) → bull(C3) → pullback(C2) → bear
- C2 exit sub-state signal: S5 (trend_1h↑) → 92% bull, S4 (trend_1h↓) → 50/50
- Stable across 3 subperiods (92.1%, 92.7%, 90.7%)
- S5 episodes net positive (+0.20%), S4 episodes net negative (−0.81%)
- C1 reversal: asymmetric payoff (+1.09% for bull breakthrough, −0.25% for failure)

## Iteration 5: Intra-Episode Flip Dynamics
- Flip trigger is noise: 511 confirmed-flip trades, 38.4% win rate, +0.005% mean. Not tradeable.
- ~3 flips per episode. Can't distinguish final recovery from earlier fails.
- The signal is an exit property, not a trigger. The sub-state at exit confirms the transition quality.
- C2 is a holding pattern where the market oscillates before deciding.

## Iteration 6: Forward-Looking Returns + Synthesis

### What was tested
- Does exit sub-state of prior regime predict returns/duration in the NEXT regime?
- C3 bull episodes tagged by entry path: C2-S5 vs C2-S4 vs C1
- C0 bear episodes tagged by entry path
- Zero-flip episode outcomes

### What was found

**Forward-looking signal confirmed:**
- C2-S5 → C3 (n=111): +0.09%, 7.6h — longer, positive returns
- C2-S4 → C3 (n=32): −0.17%, 4.3h — shorter, negative returns (anemic bull)
- C2-S5 → C0 (n=10, rare failures): +0.12%, 4.2h — short, shallow (barely bear)
- The exit sub-state predicts next regime quality, not just direction

**Generalization across transitions:**
- C3 exits show same pattern: S7→C2 produces orderly pullback (+0.06%), S6→C2 produces sharp pullback (−0.24%)
- The fast bit at exit carries information at ALL regime boundaries, not just C2→C3

**Zero-flip episodes:**
- 11 S5-entry C2 episodes never visited S4: all 11 → bull (100%), mean +0.14%, 0.5h
- 17 S4-entry C2 episodes never flipped to S5: never attempted recovery, predominantly → bear

### Sage corrections applied to summary
1. C1 EV: clarified unconditional (+0.018%) vs S3-conditioned (+0.14%, n=69)
2. Zero-flip accounting: 28 total = 11 S5-entry + 17 S4-entry (mirror images)
3. Exit sub-state generalization: added C3-S7/S6 data to section 3c, elevated from C2-specific to general property

### Investigation status: COMPLETE
Full synthesis in `memories/markets/investigation-summary.md`. Investigation reached natural diminishing returns on this dataset. Next steps require different data (out-of-sample, multi-asset).

---

## Final Synthesis

### The arc

Started testing whether the (3,5) Z₅ transition matrix captures BTC intraday regime structure. Six phases of computation, 4 binary bases tested, 240 surjections exhaustively searched. **The hypothesis failed cleanly.** But the methodology — binary trigram construction, transition matrix estimation, spectral analysis, lumpability testing — uncovered genuine market structure that wouldn't have been found otherwise.

### What we're confident about (strong evidence)

1. **K=4 regime structure.** Three independent bases, unambiguous eigenvalue gaps, 19× lumpability advantage over K=5. The market has 4 functional regime types organized as a directed cycle: bear → reversal → bull → pullback. Robust across bases and subperiods.

2. **Complement symmetry.** Market-opposite states (all-bearish-decelerating-calm ↔ all-bullish-accelerating-volatile) have identical transition dynamics under relabeling. Algebraically confirmed via degenerate T₈ eigenvalue pairs. This is coherence parity: the market distinguishes aligned from misaligned, not up from down.

3. **Directed cycle with forbidden stage-skipping.** You can't jump from bear directly to bull without passing through reversal. The 4 structural zeros are stable across subperiods.

### What we found but need to validate (moderate evidence)

4. **Exit sub-state confirmation signal.** trend_1h at regime exit predicts next regime quality (92% vs 50% for C2 pullback). Stable across 3 subperiods within this sample. Generalizes across all regime boundaries. But: in-sample only, single asset, 122 S5 exits total.

5. **C1 reversal asymmetric payoff.** +1.09% breakthrough vs −0.25% failure. Structurally interesting but n=43 breakthroughs is thin.

### What failed (informative negatives)

6. **(3,5) surjection.** K≠5. Complement symmetry holds but doesn't extend to a 5-class partition.

7. **Intra-episode flip triggers.** 511 trades, near-zero edge. The signal lives at boundaries, not within regimes.

8. **Volume profile basis.** No discrete structure. VP distances at these timescales don't produce stable regimes.

### What the investigation produced beyond the data

The binary trigram + transition matrix + lumpability framework is a general-purpose regime discovery tool. It takes three orthogonal binary features, constructs an 8-state chain, and discovers structural invariants (K, cycle topology, symmetries, forbidden transitions) that are properties of the dynamics, not artifacts of the features. Applicable to any asset and feature set. The (3,5) hypothesis motivated building it; the framework outlives the hypothesis.

### Deliverables
- `memories/markets/investigation-summary.md` — complete synthesis
- `memories/markets/findings.md` — consolidated findings with evidence strength ratings
- `memories/markets/regime-dynamics.md` — updated thesis
- `memories/markets/investigation-1.md` — investigation record with results
- `logos/markets/01-06_*.py` — all computation scripts
- `memories/markets/01-06_*_output.txt` — all raw outputs
