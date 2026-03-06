# Theorist Final Note: Reconciliation and Correction

## The Priority Inversion

Two documents in this investigation state opposite priority orderings:

**The capstone (23-generation-findings.md, §1):** "KW occupies a specific position where sequential anti-repetition (kac) is prioritized over distributional uniformity (χ²) and m-score improvement."

**The final analysis (round5_final_analysis.md, §3):** "KW behaves as if chi² (distributional uniformity) is at least 2.4× more important per std-unit than balanced criteria assume... KW prioritizes having all transformation types available over using them non-repetitively."

These appear contradictory. They are not. They describe the same observation from two different reference frames.

### From the random baseline

KW has chi² = 2.290 (6th percentile) and kac = −0.464 (2nd percentile). Relative to random, kac is the more extreme signal. In this frame, KW "prioritizes kac" — it's more exceptional on kac than on chi².

### From the balanced-cost attractor

The balanced-cost attractor at Hamming 4 has chi² = 2.806 and kac = −0.581. Moving from KW to this attractor would improve kac (−0.464 → −0.581) at the cost of chi² (2.290 → 2.806). KW refuses this trade. In this frame, KW "prioritizes chi²" — it holds chi² at 2.290 rather than accepting the kac gain.

### The resolution

Both are correct descriptions of the same point, viewed from different directions:

- **Relative to random:** KW went further on kac than on chi² (kac is the more outlying signal)
- **Relative to the balanced attractor:** KW stops short on kac to protect chi² (chi² is the defended signal)

The first statement is about *where KW sits*. The second is about *why it stops there*. The first describes the *outcome*. The second describes the *mechanism*.

For the generative question, the mechanism statement is more useful. **KW's ridge position is where chi² protection prevents further kac improvement.** The M-rule gives the default; kac-sensitivity overrides it at 3 positions; but the override stops where it would damage chi². This is the "vocabulary-over-grammar" reading: use all kernel types roughly equally (chi²), and avoid immediate repetition when you can (kac), but not at the cost of vocabulary coverage.

### Recommended reading

The capstone's phrasing should be understood as: "KW achieves unusually strong kac (outcome), at a position where chi² is the defended constraint (mechanism)." The two statements are complementary, not contradictory.

---

## What the Builder's Final Round Confirmed

The builder's final response is a single sentence of agreement: "The record is complete." No new data was generated. No new generators were tested. This is appropriate — Round 5's correction was the last substantive contribution.

The builder notes the key methodological lesson: "The distinction between 'a point that's recovered when you target it' and 'a point that emerges from a KW-agnostic process' is the difference between a tautology and a finding." This is correct and is the single most important insight of the entire iter5 investigation.

---

## The Final State of the Question

**What we proved:**
1. KW's orientation requires N ≥ 2 principles (M-preference + sequential anti-repetition)
2. KW is locally Pareto-optimal (Hamming 1) but not globally (Hamming 2+)
3. KW is not a basin attractor under any KW-agnostic criterion
4. KW sits 3–5 Hamming steps from the balanced-cost minimum, shifted toward chi²-protection
5. The landscape near KW has effective dimensionality 3 (bits 9, 17, 23)
6. The 2.2% kac domination gap is within single-step-search construction noise

**What remains undetermined:**
1. Whether chi² was actively valued or emerged from attentive variety
2. Whether asymmetry is an independent principle (N=3) or emergent (N=2)
3. Whether a 5th criterion exists that would fully characterize KW
4. Whether the construction process was intentional craft, bounded search, or both

**The honest summary:** We found what KW is (a multi-objective ridge point), what it isn't (any kind of optimum or attractor), and what it implies (a 2-principle construction with single-step search limitation). We did not find a generative algorithm that produces it, because no such algorithm exists in the tested space. The last 3–5 bits of specificity are either contingent, constrained by an unmeasured property, or reflect an aesthetic priority we can identify (chi² > kac) but cannot derive from first principles.

This is where computation stops and interpretation begins.
