# Domains — Questions

## Core Question: Which domains have three independent binary oppositions whose pairwise relations follow the 五行 grammar?

The investigation established that the I Ching's structure is typological, not dynamical. Q₃ × Z₅ classifies relational configurations between 3-bit binary states. The grammar (GMS, valve, complement-Z₅) predicts which relational types are forbidden and which are directionally constrained. The question is: in what real domains do the 8 vertices of Q₃ correspond to meaningful states, and do the grammatical constraints hold for the relations between them?

### What makes a domain testable

1. **Three independent binary axes** — producing 8 states that map to Q₃ vertices
2. **Pre-existing classification** — the axes are defined by the domain, not invented by the researcher
3. **Known relations between states** — either empirical (observed transitions) or logical (structural adjacency)
4. **五行 typing is testable** — the Z₅ assignment to the 8 states can be checked against the grammatical predictions (GMS, valve)

---

## D1: Chinese Medicine — 八纲辨证 (Eight Principle Differentiation)

### Why this is the strongest candidate

TCM's diagnostic framework uses exactly three binary axes:
- **寒/热** (cold/hot) — thermal nature of the pathology
- **虚/实** (deficiency/excess) — strength of the pathogenic factor vs body's resistance  
- **表/里** (exterior/interior) — depth/location of the pathology

Eight diagnostic categories = Q₃ vertices. The system is native to the same tradition as the I Ching. 五行 is already used in TCM alongside the 八纲. The mapping is predetermined — zero researcher degrees of freedom.

### The trigram correspondence

The tradition provides an explicit mapping between trigram lines and the three diagnostic axes:
- Bottom line (b₀) = 表/里 (exterior/interior)
- Middle line (b₁) = 虚/实 (deficiency/excess)  
- Top line (b₂) = 寒/热 (cold/hot)

Or some permutation. The exact line↔axis correspondence needs verification from classical TCM sources.

### Questions

**D1.1:** What is the traditional mapping between trigram lines and 八纲 axes? Is it explicitly documented, or must it be reconstructed?

**D1.2:** Under this mapping, does the 五行 typing of the 8 diagnostic categories match the trigram 五行 typing? (e.g., does the category {热, 实, 表} = "hot, excess, exterior" map to the same element as its corresponding trigram?)

**D1.3:** Are the forbidden patterns (GMS: no consecutive 克) observable in clinical disease progression through the 8 categories? This tests whether the grammar constrains real pathological transitions.

**D1.4:** Does the valve hold? After a 克 transition (destructive change in diagnostic category), must the next transition pass through 比和 (same category) or 生 (generative change) before another 克?

**D1.5:** The 體用 framework maps directly onto TCM diagnosis: 體 = the patient's constitution, 用 = the pathogenic influence. Does the 五行 relation between 體 and 用 predict treatment strategy in the way the 梅花 decision rules (8c) specify?

### Caveats

- TCM practitioners already use 五行 for diagnosis — disease data reflects the grammar's influence on treatment selection, not just natural progression. Need pre-treatment or natural history data.
- The 八纲 axes may not be strictly binary in practice (there are degrees of cold/hot, not just on/off).
- Sample sizes in classical case literature are small and anecdotal.

---

## D2: Quantum Measurement — Three Qubits

### Why this is structurally exact

Three qubits measured in the computational basis produce outcomes in {0,1}³ = Q₃ vertices. This IS Q₃, not an analogy. The algebraic structure is identical by construction.

### What the grammar would classify

The 五行 typing would assign each of the 8 measurement outcomes to one of 5 elements via the canonical surjection. The grammar then classifies:
- Which pairs of outcomes are 比和 (same type), 生 (generative relation), 克 (destructive relation)
- Which sequences of measurements obey GMS (no consecutive 克)
- Whether the valve holds for measurement sequences

### Questions

**D2.1:** Under the canonical 五行 assignment, what is the Z₅ typing of the 8 computational basis states? (This is just the trigram typing — already known.)

**D2.2:** For entangled 3-qubit states, does the probability distribution over measurement outcomes respect the 五行 grammar? (e.g., are 克-克 consecutive measurement pairs suppressed relative to random?)

**D2.3:** Do quantum error correction codes on 3 qubits have any relationship to the GMS constraint? The GMS forbids certain adjacent patterns — error correction forbids certain error patterns. Is there structural overlap?

**D2.4:** The complement operation (σ: bitwise NOT) maps each outcome to its complement. In quantum mechanics, this is the bit-flip operator X⊗X⊗X. The complement-Z₅ constraint (complement must be a Z₅ isometry) — does this have any quantum information interpretation?

---

## D3: Structural Invariance — Q₃ Edge-Coloring Orbit Analysis

**Status: computed** (`q3_edge_orbits.py`, `market_regime_predictions.py`)

The canonical Z₅ typing assigns each Q₃ vertex a Z₅ element. Each Q₃ edge (single-bit transition) gets classified as 比和 (diff=0), 生 (diff∈{1,4}), or 克 (diff∈{2,3}). This section records what's invariant under axis relabeling, what the full landscape of valid typings looks like, and the axis-type alignment theorem.

### Result 1: 克-dominance invariance

Under any axis assignment (all 48 elements of Aut(Q₃) = S₃ ⋉ (Z₂)³), the edge-type distribution is always 比和=2, 生=4, 克=6. No axis permutation or polarity flip changes this ratio. 50% of single-axis transitions are destructive. 24 distinct patterns, stabilizer = {id, complement}. All 24 share identical subgraph structure: 克 = 2×P₄, 生 = 2×P₃, 比和 = 2×K₂. No 生↔克 swap within the orbit.

### Result 2: Full surjection landscape (102 colorings from 240 functions)

| (比和, 生, 克) | Patterns | Functions | In Aut(Q₃) orbit |
|----------------|----------|-----------|-------------------|
| (2, 4, 6) | 36 | 72 | 24 of 36 |
| (2, 6, 4) | 36 | 72 | 0 |
| (0, 4, 8) | 15 | 48 | 0 |
| (0, 8, 4) | 15 | 48 | 0 |

The 78 extra patterns (outside Aut(Q₃)) arise from GL(3,F₂) shearing maps and Z₅ automorphisms. The (0,\*,\*) patterns require nonlinear axis entanglement — they serve as an **axis-independence diagnostic**: if observed data produces a (0,\*,\*) coloring, the domain's axes are not genuinely independent binary oppositions.

### Result 3: Minimal determining set

6 edges (one per complement pair) are necessary and sufficient to uniquely identify the coloring among all 102. Any transversal of the 6 complement pairs works (64 = 2⁶ minimal sets). Within the 24 Aut(Q₃) patterns, 5 edges suffice.

### Result 4: Axis-Type Alignment Theorem

**Theorem.** In any {2,2,2,1,1} complement-equivariant surjection F₂³ → Z₅ with Q₃-adjacent doublets, the three axes have types:
- **Doublet axis:** 2比和 + 2生 (never destructive)
- **Pure-克 axis:** 4克 (always destructive)
- **Mixed axis:** 2克 + 2生 (exactly half destructive)

**Proof core:** (a+s₁)(a-s₁) = a²-s₁² = 4-1 = 3 mod 5. Since (3/5) = -1 (QNR), exactly one of {a+s₁, a-s₁} is QR (生) and the other QNR (克). The axis collecting the QNR sum gets 4/4 克; the other gets 2克+2生.

This connects to 8c-ext2.5: both R=B (interpretation symmetry count = 56) and axis-type purity are manifestations of (3/5) = -1. The (4/2+2/2+2) axis-type partition is specific to p=5 — at p=13, (3/13) = +1 and the split lemma does not force opposite types.

### Result 5: Empirical testing sequence

Derived from Results 1-4:

- **Step 0:** Verify transitions are predominantly single-axis (M1 prerequisite)
- **Step 1:** Identify the axis where ALL transitions are disruptive → pure-克 axis
- **Step 2:** Identify the axis where NO transitions are disruptive → doublet axis
- **Step 3:** Verify the mixed axis has exactly 2/4 destructive transitions
- **Step 4:** Test GMS (no consecutive 克) on the P₄ paths (pure-克 + mixed axes)

Steps 1-3 require classifying transition character only (no time-series data). Step 4 requires ~30-40 sequential transitions for detection at p<0.05 under non-backtracking null.

---

## D4: Market Regimes — Explicit Predictions

**Status: tested** (`market_regime_predictions.py`, `market_regime_data.py`, `market_regime_diagnostics.py`, `market_partition_test.py`, `market_gms_test.py`)

Three binary market axes: trend (down=0/up=1), volatility (low=0/high=1), liquidity (scarce=0/abundant=1). Eight regimes on Q₃.

### Regime typing (canonical assignment)

| Regime | Binary | Trigram | Element |
|--------|--------|---------|---------|
| Quiet decline | 000 | 坤 | 土 |
| Grinding rally | 001 | 震 | 木 |
| Panic/capitulation | 010 | 坎 | 水 |
| Short squeeze | 011 | 兌 | 金 |
| Slow bleed | 100 | 艮 | 土 |
| Healthy bull | 101 | 離 | 火 |
| Correction | 110 | 巽 | 木 |
| Euphoria | 111 | 乾 | 金 |

### Axis-type alignment (canonical assignment)

| Axis | 克 | 生 | 比和 | Character |
|------|---|---|-----|-----------|
| Volatility (b₁) | **4** | 0 | 0 | Pure-克: every vol flip is destructive |
| Trend (b₀) | 2 | 2 | 0 | Mixed: half destructive |
| Liquidity (b₂) | 0 | 2 | **2** | Doublet: never destructive |

### GMS-forbidden sequences

Two P₄ 克-paths, each on one liquidity face:

**Path 1 (scarce liquidity):** Panic →克(vol)→ Quiet decline →克(trend)→ Grinding rally →克(vol)→ Short squeeze

**Path 2 (abundant liquidity):** Slow bleed →克(vol)→ Correction →克(trend)→ Euphoria →克(vol)→ Healthy bull

Forbidden: any two consecutive steps along either path. All involve a vol flip immediately followed by a trend flip, or vice versa. Liquidity transitions never participate.

### Null model

P(克→克) under uniform random walk: 0.3333 at P₄-internal vertices (Quiet decline, Grinding rally, Correction, Euphoria), 0.2222 at P₄-endpoints (Panic, Short squeeze, Slow bleed, Healthy bull). Average: 0.2778. GMS predicts 0.

### Questions — Empirical Evidence

**D4.1: Are market regime transitions predominantly single-axis?**

**Tested.** Data: BTC 1-second datalog 2025-07-21 to 2026-02-20 (18.6M rows). Resampled to 1h bars (5,160 bars).

| Metric | Value |
|--------|-------|
| M1 (Q₃ edge fraction among non-self, 1h) | 0.789 |
| Q₃ edges (single-axis) | 2,065 (40.0%) |
| Self-loops | 2,540 (49.2%) |
| Multi-axis jumps | 554 (10.7%) |

**Result: YES.** 79% of non-self transitions are single-axis at 1h resolution. M1 increases at shorter timescales (0.44 at 8h → 0.79 at 1h), confirming that multi-axis jumps at longer bars are sequential single-axis flips that shorter bars resolve. The Q₃ adjacency structure is empirically relevant.

**Axis note:** The original liquidity proxy (`spread_bps_1m`) was degenerate (>97% zeros). `volume_since_last` had MI=0.346 with volatility, collapsing Q₃ to Q₂. The final axis uses `ob100_ratio_1m` (top-100 order book ratio): MI=0.0025 with vol, min vertex count=143, entropy=2.995 (near-uniform). Axes are genuinely independent.

**D4.2: Is volatility the uniformly disruptive axis?**

**Tested.** Edge-level partition test using two observables (regime persistence at destination, volatility ratio) across all 12 Q₃ edges, 2,065 traversals at 1h.

**Result: NO.** The Z₅ typing does not predict behavioral differentiation between edges.

*Level 1 (partition existence):* Persistence FAILS (max/median ratio 1.52, threshold 2.0). Vol ratio PASSES (ratio 2.32) but is confounded — vol-axis flips mechanically change vol.

*Level 2 (canonical assignment):* FAILS on both observables. The volatility axis (pure-克, predicted uniform) has the LARGEST within-axis range. The trend axis (mixed, predicted bimodal) has the SMALLEST range. Opposite of prediction.

*Within-axis type comparison (controls for axis confound):*
- Trend axis (2克 + 2生): persistence p=0.226, |log(vol_ratio)| p=0.444 — no significant type effect
- Liquidity axis (2比和 + 2生): persistence p=0.853, |log(vol_ratio)| p=0.411 — no significant type effect

*Effect size (η²):* Axis identity explains 2.4–3.0× more variance than Z₅ type. Neither explains much (<10% of total), but the comparison is consistent: which axis flips matters more than the algebraic type of the flip.

*Type-pooled means (opposite of grammar prediction for persistence):*

| Type | Persistence | Vol ratio |
|------|------------|-----------|
| 比和 | 1.81 ± 0.06 | 1.008 ± 0.007 |
| 生 | 1.99 ± 0.05 | 1.017 ± 0.006 |
| 克 | 2.10 ± 0.07 | 1.031 ± 0.011 |

Grammar predicted 克 = low persistence (destabilizing). Observed: 克 = highest persistence.

**D4.3: Are 克→克 bigrams suppressed?**

**Tested.** GMS bigram test on 2,065 Q₃ edges (1h bars). Two framings, three null models.

**Result: NO — 克→克 is ENHANCED, not suppressed.** This is the opposite of the GMS prediction.

| Framing | Observed 克→克 | Expected (independence) | Ratio | Permutation p |
|---------|---------------|------------------------|-------|---------------|
| A (temporal adjacency) | 93 | 63.8 | 1.46 | 1.0000 |
| B (Q₃ walk) | 222 | 156.2 | 1.42 | 1.0000 |

p=1.0000 means in all 10,000 permutation shuffles, the observed count was higher than the shuffled count. 克→克 is significantly more common than chance, not less.

Under the vertex-conditional null (Null B), expected=219.0 for Framing B (ratio 1.014). The enhancement is almost fully explained by graph topology: vertices at P₄-internal positions (000, 001, 110, 111) have P(next Q₃ edge is 克) ≈ 0.38–0.49, so once you take a 克 step you're likely at a high-克-probability vertex.

75 of 222 克→克 bigrams (34%) fall on the P₄ paths — the sequences the GMS specifically forbids. They are not suppressed.

**D4.4: Does the valve hold after 克 transitions?**

**Not separately tested.** Since 克→克 is enhanced rather than suppressed (D4.3), the valve — which is a stronger constraint than GMS — cannot hold. If consecutive 克 transitions were forbidden, there could be no valve violation. Since they are positively correlated, the valve is falsified by implication.

**D4.5: Which axis assignment is correct?**

**Moot.** The Z₅ typing fails to predict behavioral differentiation regardless of axis assignment (D4.2). The partition test checked the canonical assignment and found no signal. Since the edge-type distribution {比和=2, 生=4, 克=6} is invariant under all axis permutations (D3 Result 1), testing other axis assignments would produce the same edge types on different axes but the same null result: axis identity dominates over Z₅ type.

### What was established

1. Q₃ adjacency IS empirically relevant for BTC market regimes at 1h resolution (M1=0.79)
2. Three genuinely independent binary axes can be constructed (MI=0.0025)
3. The Z₅ grammar does NOT transfer to this domain — no edge-type behavioral differentiation, no 克→克 suppression
4. Physical axis identity (which axis flips) explains more behavioral variance than algebraic Z₅ typing
5. The 克→克 enhancement (1.42×) is explained by graph topology (vertex-conditional transition probabilities), not by any grammar effect

---

## Other Candidate Domains (Not Yet Developed)

**Genetics:** Three independently regulated genes, each on/off. Eight expression states. Test: do gene regulatory networks show GMS suppression in expression state transitions?

**Ecology:** Three binary environmental axes (e.g., wet/dry, warm/cold, nutrient-rich/poor). Eight habitat types. Test: do ecological succession patterns follow 五行 constraints?

**Personality/Decision:** Three binary psychological axes. Eight personality types. Test: do interpersonal dynamics follow the grammar's relational typing?

---

## Execution Priority

1. ~~**D4 (Markets)** — COMPLETE. Negative result across all tests.~~
2. **D1 (TCM)** — native domain, pre-existing mapping, highest relevance, but bias risk from practitioners using the system. Now the primary remaining candidate.
3. **D2 (Quantum)** — algebraically exact, no bias risk, but likely physically empty
4. **Other domains** — require constructing the three binary axes, which introduces researcher degrees of freedom

## What Would Change Our Understanding

- **D4 outcome: shows nothing.** The grammar does not transfer to BTC market regimes. All five predictions tested (D4.1–D4.5) are either falsified or moot. The Q₃ adjacency structure is empirically valid, but the Z₅ typing on top of it adds no predictive power. This is consistent with the grammar being specific to its native Q₃ (the I Ching's trigram space) and not a universal property of binary-axis systems.
- **D1 mapping exists and grammar holds:** Would still be significant. TCM's 八纲 is the native domain — the grammar could work there even if it doesn't transfer to markets.
- **D1 mapping exists but grammar fails:** Would narrow the grammar to the I Ching's own internal structure — a classification system without domain transfer.
- **D4 negative strengthens the "typological not dynamical" conclusion from the mod-8 investigation.** The grammar classifies static relational configurations between the 8 trigrams. Temporal sequences of regime transitions are a different kind of object — the grammar was not designed for temporal prediction.
