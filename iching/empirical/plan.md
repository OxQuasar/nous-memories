# Empirical Investigation — Plan

## The Core Test

Apply the 五行 grammar to real transition data and check whether it predicts anything. The grammar: three transition types (continuation/generation/destruction), a forbidden bigram (no consecutive destruction), and a one-way valve (destruction → generation blocked). If these constraints hold in data the grammar wasn't fitted to, it's capturing real structure.

## The Mapping Problem — Solved by the Tradition

The tradition provides explicit correspondence tables mapping phenomena to the five elements. Each element governs specific domains:

| Element | Season | Direction | Phase | Quality | Body | Emotion |
|---------|--------|-----------|-------|---------|------|---------|
| 木 Wood | Spring | East | Growth/rising | Expansive | Liver | Anger |
| 火 Fire | Summer | South | Peak/fullness | Radiant | Heart | Joy |
| 土 Earth | Late summer | Center | Transition/stability | Settling | Spleen | Worry |
| 金 Metal | Autumn | West | Decline/contraction | Condensing | Lungs | Grief |
| 水 Water | Winter | North | Dormancy/storage | Flowing down | Kidneys | Fear |

These aren't metaphors — they're classification rules used operationally in Chinese medicine, agriculture, military strategy, and governance for millennia. The trigram correspondences are equally fixed (乾/兌=金, 離=火, 震/巽=木, 坎=水, 坤/艮=土).

**This changes the methodology.** We don't need to invent a 5-category classification per domain. We use the traditional correspondences as the mapping, then test whether the grammar's constraints hold. The mapping is given *a priori* by the system itself — not fitted to data.

**Three strategies, now:**

**Strategy A (strongest):** Use the traditional correspondences directly. Classify states by the 五行 rules the tradition provides. Test grammar constraints. No degrees of freedom in the mapping.

**Strategy B (robustness check):** Run all 120 permutations of the 5-type assignment anyway. Check whether the traditional assignment outperforms random permutations. If it does, the specific traditional mapping matters. If all permutations work equally well, the constraint is generic to Z₅ cycle structure.

**Strategy C (new domains):** For domains the tradition doesn't explicitly address, use the qualitative logic: identify which states correspond to growth, peak, stability, decline, dormancy. This has degrees of freedom but is constrained by the traditional definitions.

---

## Probe 1: Seasonal / Climate Transitions (E1, E2, E3)

**Why first:** The mapping is literally given — 木=spring, 火=summer, 土=late summer, 金=autumn, 水=winter. Zero ambiguity.

**States:** Seasonal climate regimes, defined by temperature/precipitation thresholds.

**Data source:** Long-run climate station data (GHCN-D, ~100+ years at many stations). Or: paleoclimate proxy data for longer timescales.

**Steps:**
1. Define 5 seasonal regimes by temperature thresholds (the tradition assigns specific temperature qualities to each element)
2. Extract regime transition sequence at each station
3. Classify transitions as 比和/生/克 by cycle distance
4. Test E2: are out-of-order transitions (e.g. summer directly to winter = 克-克 equivalent) suppressed?
5. Test E3: does the valve hold? After a disruptive transition (e.g. unseasonable cold snap = 克), does the system pass through a neutral phase before resuming the generative cycle?

**Why this is a strong first test:** Climate *should* follow the generative cycle (spring→summer→late summer→autumn→winter = 木→火→土→金→水 = pure 生 sequence). Deviations from this cycle are precisely the 克 transitions. The question becomes: when the cycle is disrupted, do the disruptions follow the grammar's constraints?

**Limitation:** Seasonal cycles are largely periodic and forced by orbital mechanics. The grammar's constraints may hold trivially. The real test is in the *anomalies* — when seasons arrive out of order, do the forbidden patterns hold?

## Probe 2: Chinese Medical Case Data (E1, E2, E3)

**Why second:** The mapping is native — Chinese medicine classifies organ systems, symptoms, and disease progressions by 五行. The grammar was *designed for* this domain.

**States:** 五行 organ system diagnoses (木=liver system, 火=heart system, 土=spleen system, 金=lung system, 水=kidney system).

**Data source:** Published case series from Chinese medical journals, or clinical databases from TCM hospitals. Disease progression records showing sequential organ involvement.

**Steps:**
1. Extract sequential diagnoses: which organ system is primary at each clinical visit
2. Classify transitions by 五行 cycle distance
3. Test E2: is consecutive 克 (e.g. liver→spleen→lung, two successive overcoming transitions) suppressed?
4. Test E3: after a 克 transition, does the patient pass through a 比和 or 生 phase before another 克?
5. Test E1: are 生 transitions (e.g. liver→heart, mother-to-child) associated with better prognosis than 克 transitions?

**Why this matters:** This is the domain where the grammar has been applied longest. If it fails here, it fails everywhere. If it works here but nowhere else, it's domain-specific (which would still be significant — it would mean the grammar captures something real about disease progression in the organ systems it was designed for).

**Bias risk:** TCM practitioners *use* 五行 theory to classify and treat. The data may reflect practitioner behavior (treating according to the grammar) rather than natural disease dynamics. Need to separate: does the grammar predict disease progression *before treatment*, not after treatment guided by the grammar?

## Probe 3: Political Regime Transitions (E1, E2, E3, E4)

**Why third:** Large dataset, and the traditional correspondences provide a mapping through the governance tradition.

**States:** Political regime types. The traditional mapping via governance theory:
- 木 Wood → emerging/revolutionary regimes (growth, new order rising)
- 火 Fire → expansionist/peak-power regimes (dominance, full expression)
- 土 Earth → consolidating/stable regimes (institutional, bureaucratic)
- 金 Metal → contracting/declining regimes (rigidity, loss of vitality)
- 水 Water → collapsed/dormant regimes (chaos, power vacuum, latency)

This follows the traditional phase logic: growth → peak → stability → decline → dormancy → growth.

**Data source:** Polity V (~170 countries, 1800–present) or V-Dem.

**Steps:**
1. Map Polity scores to 5 phases using the traditional quality definitions (not arbitrary score bins)
2. Extract year-to-year transitions where the phase changes
3. Classify as 比和/生/克
4. Test E2, E3
5. Strategy B robustness: run all 120 permutations, check if traditional ordering outperforms

**Key question for E4:** Compare results across regions — does the grammar work for both Western and East Asian political systems?

## Probe 4: 皇極經世 Dynasty Chronology (E2, E3)

**Why here:** The data is in-house (`texts/huangjijingshi/`, files 2–6). Shao Yong's 元會運世 system provides ~3,400 years of year-by-year chronology (~2357 BCE to ~1060 CE) with each year assigned to the 60-year 甲子 sexagenary cycle. The 天干 (Heavenly Stems) carry 五行 assignments:

| Stem pair | Element |
|-----------|---------|
| 甲乙 | 木 Wood |
| 丙丁 | 火 Fire |
| 戊己 | 土 Earth |
| 庚辛 | 金 Metal |
| 壬癸 | 水 Water |

Shao Yong himself didn't use 五行 — his system is binary-dualistic (陰/陽). But the 天干/地支 assignments he recorded carry an implicit 五行 layer through the stem correspondences. This is an independent system layered on the same data.

**The test:** At dynasty transitions (founding, collapse, conquest), what is the 五行 type of the transition year? Does the grammar predict anything about the character of the transition?

**Steps:**
1. Parse files 2–6: extract year, 甲子 label, ruler, dynasty, event annotations
2. Assign 五行 to each year via its 天干 (甲/乙=木, 丙/丁=火, etc.)
3. Identify all dynasty transitions (change of ruling house, not just succession within a dynasty)
4. For each transition, record: 五行 of the last year of the old dynasty, 五行 of the first year of the new dynasty, transition type (比和/生/克)
5. Also: for the years surrounding each transition (±5 years), compute the sequence of 五行 types
6. Test E2: are 克-克 bigrams at dynasty transitions suppressed vs the base rate of the 天干 cycle?
7. Test E3: after a 克-year transition, does the next transition avoid 生?

**Null model:** The 天干 cycle is deterministic (10-year period), so 五行 repeats every 2 years (甲乙 both = 木, etc.). The null is: dynasty transitions are independent of the 天干 cycle. Test whether transition years cluster in particular 五行 types more than the 2/10 = 20% base rate for each element.

**Advantage:** Data already available, no external sourcing needed. The mapping is mechanical (天干 → 五行, no interpretation). The chronology is structured and parseable.

**Limitation:** ~15–20 dynasty transitions in 3,400 years. Small N. Better as a pilot/sanity check than a powered statistical test. Also: the 天干 cycle is periodic and uncorrelated with political events by construction (it's a calendar, not a causal system). Any signal would be surprising.

**Secondary test:** Regardless of 五行, check whether Shao Yong's 元會運世 grid coordinates (which 運 and 世 a dynasty transition falls in) predict anything about dynasty duration or transition character. This tests his temporal hierarchy directly.

## Probe 5: Ecological Succession (E1, E2, E3)

**Mapping via traditional correspondences:**
- 木 Wood → pioneer/growth phase (colonization, biomass increase)
- 火 Fire → peak productivity (canopy closure, maximum energy throughput)
- 土 Earth → climax/stable phase (nutrient cycling, equilibrium)
- 金 Metal → senescence/decline (standing dead, nutrient lock-up)
- 水 Water → disturbance/reset (flood, fire, clearing — dormancy before regrowth)

**Data source:** Regime Shifts Database (RSDB) or long-term ecological research (LTER) sites.

**Same tests as above.** Smaller sample size but the most natural alignment with the element qualities.

## Probe 6: Cross-Domain Comparison (E4)

**After Probes 1–5:** Compare effect sizes and constraint structure across climate, medicine, politics, dynastic chronology, and ecology.

**The key test:** Does the *same* grammar work across all domains when the traditional correspondences are used? If yes, the grammar is universal at the level of transition structure. If it works in some domains but not others, identify what distinguishes the domains where it works.

## Probe 7: Decorrelation Test (E6)

**Use whichever dataset from Probes 1–5 has the longest transition sequences.**

Compute mutual information between transition type at step t and step t+k for k=1,2,3,4,5. Phase 8 predicts decorrelation at k≈2 (R288). If the data matches this, the single-step assessment regime is confirmed empirically.

---

## Priority Order

1. **Probe 4 (皇極經世 chronology)** — data in-house, mechanical mapping, no sourcing needed, good pilot
2. **Probe 1 (seasonal/climate)** — mapping is literal, zero ambiguity, large data, strong first test
3. **Probe 2 (Chinese medicine)** — native domain, grammar was built for this, highest relevance but highest bias risk
4. **Probe 3 (political)** — large dataset, traditional governance mapping, good for E4
5. **Probe 5 (ecological)** — natural alignment with element qualities, smaller N
6. **Probe 6 (cross-domain)** — depends on 1–5
7. **Probe 7 (decorrelation)** — piggybacks on longest sequence from 1–5

## What Would Change Our Understanding

- **E2 positive across domains:** The forbidden-pattern constraint is a real feature of natural transitions when classified by the traditional correspondences. The grammar captures something about how destructive change works.
- **E2 negative everywhere:** The constraint is specific to the algebraic structure, not to nature. The grammar is self-consistent but not empirically descriptive.
- **E2 positive only in native domains (medicine, seasonal):** The grammar captures domain-specific structure in the systems it was designed for, but doesn't generalize.
- **E3 positive (valve holds):** Destruction genuinely requires a cooling-off period before generation. Most surprising and practically significant finding.
- **Traditional mapping outperforms random permutations (Strategy B):** The specific element assignments matter — it's not just any Z₅ cycle, it's *this* Z₅ cycle applied to *these* correspondences.
- **E6 matches R288:** Single-step prediction outperforms multi-step, confirming the system is designed for immediate assessment, not trajectory forecasting.
