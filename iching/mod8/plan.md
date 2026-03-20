# Mod-8 Plan — Remaining Questions

M1 (bit-layer decomposition) and M2 (cyclic shift invariance) are complete. M3–M5 remain.

---

## M3: 體用 Distribution Under the Date Formula

**Question:** What 五行 relations does the 梅花 algorithm actually produce? The algorithm generates two trigrams from a single timestamp. Their 五行 relation (生/克/比和) is the prediction. What is the distribution?

**Why it matters:** If the algorithm systematically underproduces 克 relations (as the mod-8 克-suppression at trigram level suggests), then the grammar's most informative signal is structurally rare at generation — which could be by design (rare signal = high information) or a defect (the algorithm can't access the grammar).

**Method:**
1. Verify the exact formula against 梅花易數 vol1: upper = (year+month+day) mod 8, lower = (year+month+day+hour) mod 8. The key relationship: lower = upper + hour mod 8, so the hour determines the cyclic shift between upper and lower trigrams.
2. For each hour value h ∈ {1,...,12}, compute the cyclic shift S_h on the 先天 ordering. Map each (upper, lower=S_h(upper)) pair to its 五行 relation.
3. Tabulate: for each hour, what fraction of (upper, lower) pairs are 比和/生/克?
4. Compare against the null (uniform random trigram pairs: 比和=2/12, 生=4/12, 克=6/12 from Q₃ edge counts).

**Expected finding:** The hour-shift determines the 體用 五行 distribution. Some hours may produce more 克 than others. If the algorithm is ergodic over all hours and all upper trigrams, the long-run distribution should average to the Q₃ edge proportions. But specific hours may be 克-enriched or 克-depleted.

**Connection to M2:** The cyclic shift analysis already showed no shift preserves all 五行 types. M3 asks the finer question: what is the type distribution per shift?

---

## M4: Grammar Survival at Hexagram Level

**Question:** The GMS constraint (no consecutive 克) and the valve (克→生=0) live on Q₃ edges. The mod-8 cycle's Q₃ edges are 100% 克-free. Does the grammar re-emerge when two trigrams are composed into a hexagram?

**Why this is the central question:** A hexagram has 体 (one trigram) and 用 (the other). Their 五行 relation CAN be 克 even if each trigram was reached via 克-free mod-8 steps. The grammar operates on the 体-用 relation, not on how the trigrams were generated. So the grammar might be fully operational at hexagram level despite being invisible at the trigram-step level.

**Method:**
1. Generate all 64 hexagrams via the 梅花 algorithm (all upper × lower trigram combinations reachable by the date formula).
2. For each hexagram, compute the 体用 五行 relation (depends on which trigram is 体 — determined by moving line position).
3. Check: is the GMS constraint (no consecutive 克) meaningful for hexagram sequences? A "sequence" here is consecutive divination results — successive timestamps producing successive hexagrams.
4. For the mod-8 cycle's reachable hexagrams: construct the transition graph on hexagram space induced by single-hour shifts. Classify transitions as 比和/生/克 at hexagram level.
5. Test whether the valve (克→生=0) holds on this induced transition graph.

**Key subtlety:** "Consecutive" in divination means successive consultations (different timestamps), not successive bars in the mod-8 cycle. The grammar's constraints may hold for natural temporal sequences even if they don't hold for cyclic navigation.

**Connection to fana:** If the grammar survives at hexagram level, then discretizing price returns mod-8 and reading 体用 relations could access the GMS constraint. If it doesn't survive, the I Ching labels are cosmetic.

---

## M5: Which Topology Governs Sequential Data?

**Question:** When price bars (or any time series) are discretized mod-8, consecutive bars produce consecutive 先天 positions. The transition between them can be read on either topology — cyclic (mod-8 distance) or hypercubic (Hamming distance on the underlying F₂³ vectors). Which topology's structure appears in the data?

**Why it matters:** This is the empirical question behind fana. If price transitions cluster on Q₃ edges (single-bit flips), the hypercube grammar applies. If they're distributed across all mod-8 distances, only the cyclic structure matters.

**Method:**
1. Take any time series (prices, temperatures, whatever). Discretize returns into 8 bins via the mod-8 mapping.
2. Compute the transition matrix: for each pair of consecutive states (i, j), record the 先天 positions.
3. Classify each transition by: (a) mod-8 distance |j-i| mod 8, (b) Hamming distance on F₂³, (c) 五行 type.
4. Test: are single-bit (Q₃ edge) transitions more frequent than expected under uniform mod-8 transitions? If yes, the hypercube topology is visible in the data.
5. For transitions that ARE Q₃ edges: are they 克-free (as the mod-8 cycle predicts) or do all three types appear?

**This requires real data.** Can use any public time series — crypto prices, stock indices, climate data. The test is purely structural: does discretized sequential data prefer Q₃ edges?

**Depends on:** M4 (if grammar doesn't survive at hexagram level, M5 is moot for grammar purposes, though still informative about topology).

---

## Execution Order

1. **M3** — straightforward computation, needs only the date formula and existing trigram tables
2. **M4** — the critical test, depends on M3 for the reachable hexagram set
3. **M5** — requires real data, depends on M4 for interpretation

## What Would Change Our Understanding

- **M3 shows 克-enrichment at certain hours:** The algorithm has access to 克 despite trigram-level 克-suppression. The suppression is layer-specific, not systemic.
- **M3 shows uniform 克-depletion:** The algorithm systematically underproduces 克 at hexagram level too. The grammar's most informative signal is structurally rare — by design or defect.
- **M4 grammar survives:** The GMS/valve constraints hold on hexagram-level transitions. The divination algorithm is a valid instrument for the grammar despite the topological separation at trigram level. This would validate fana's approach in principle.
- **M4 grammar dies:** The grammar is an algebraic property of Q₃ that doesn't propagate through the mod-8 interface. The I Ching labels on discretized data are cosmetic.
- **M5 data prefers Q₃ edges:** Real time series, when discretized mod-8, show structure aligned with the hypercube. The algebraic topology is visible in empirical data.
- **M5 no preference:** Discretized data is uniformly distributed across mod-8 transitions. The topology is invisible and the grammar inaccessible from sequential observations.
