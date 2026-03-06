# Enumeration Findings: Thread A (Sequence Enumeration) + Thread D (Self-Loop Placement)

## Executive Summary

The King Wen sequence lives in a space of **~10⁴⁵ valid sequences**. This number decomposes into three completely independent layers:

| Layer | Count | Method |
|-------|-------|--------|
| Eulerian orbit paths | **150,955,488** (exact) | BEST theorem |
| Matchings per orbit | **105⁸ ≈ 1.48 × 10¹⁶** | Combinatorial |
| Orderings + orientations | **(24 × 16)⁸ ≈ 7.36 × 10²⁰** | Combinatorial |
| **Total** | **~1.054 × 10⁴⁵** | Product (layers independent) |

For reference: 64! ≈ 10⁸⁹. The four constraints (Hamiltonian, paired, Eulerian, Qian→Tai endpoints) eliminate **~44 orders of magnitude**, but ~10⁴⁵ valid sequences remain. The KW sequence is not forced by these constraints alone — a further selection principle operates.

---

## Thread A: Eulerian Path Count

### Exact Count via BEST Theorem

The orbit multigraph has **8 nodes** (orbits) and **31 directed edges** (bridges). Each orbit is visited exactly 4 times as a source node.

**Edge structure** (26 unique directed edge types, 31 total with multiplicities):

| Edge | Mult | Edge | Mult |
|------|------|------|------|
| Qian→Qian | 1 | Xu→Shi | 1 |
| Qian→Shi | 1 | Xu→WWang | 1 |
| Qian→Zhun | 1 | Xu→Bo | 1 |
| Qian→Tai | 1 | Xu→Tai | 1 |
| XChu→Bo | 1 | Zhun→XChu | 1 |
| XChu→Zhun | 1 | **Zhun→Xu** | **3** |
| **XChu→Tai** | **2** | Tai→Shi | 1 |
| **Shi→XChu** | **2** | Tai→Bo | 1 |
| Shi→Bo | 1 | Tai→Zhun | 1 |
| Shi→Zhun | 1 | WWang→Qian | 1 |
| **Bo→WWang** | **2** | WWang→XChu | 1 |
| Bo→Qian | 1 | WWang→Shi | 1 |
| Bo→Xu | 1 | WWang→WWang | 1 |

**Degree structure:** Qian: out=4, in=3 (source, +1). Tai: out=3, in=4 (sink, -1). All others: balanced at 4/4.

**BEST theorem computation** (verified with exact integer arithmetic):

1. Augment graph: add edge Tai→Qian (mult 1, doesn't exist in original)
2. All nodes now balanced at out=in=4
3. Build Laplacian L (excluding self-loops): 8×8 matrix
4. Arborescences rooted at Qian: t_w = |det(L̃)| = **4,314**
5. Factorial product: ∏(d_out - 1)! = 6⁸ = **1,679,616**
6. Edge multiplicity correction: ∏ m_e! = 2! × 2! × 2! × 3! = **48**
7. Euler circuits = 4,314 × 1,679,616 / 48 = **150,955,488**
8. Since Tai→Qian has multiplicity 0 in original: **Euler paths = Euler circuits = 150,955,488**

**Cross-check:** Cofactor method on original Laplacian gives same arborescence count t_w = 4,314. ✓

### Within-Orbit Completion Count

Each orbit contains 8 hexagrams forming a complete graph K₈ under Z₂³ generators:
- Every pair of hexagrams in an orbit differs by exactly one of 7 non-identity generators
- **28 valid pairs** per orbit (= C(8,2), all possible pairs)
- **105 perfect matchings** per orbit (= 7!! = 7×5×3×1, the double factorial for K₈)

For each Eulerian path:
- Each orbit is visited 4 times
- Choose which matching to use: **105** options per orbit
- Choose pair ordering: **4! = 24** per orbit
- Choose pair orientation: **2⁴ = 16** per orbit
- Total per orbit: 105 × 24 × 16 = **40,320**
- Total across 8 orbits: 40,320⁸ ≈ **6.985 × 10³⁶**

### Independence Verification

**Theorem:** The three layers (Eulerian path, matching choice, ordering/orientation) are completely independent.

**Proof:** Each orbit's hexagrams are disjoint. The bridge between pair k and pair k+1 is simply hex[2k+1] ⊕ hex[2k+2] — any two hexagrams define a valid bridge. No additional constraint couples within-orbit choices across orbits.

**Empirical verification:** 1000/1000 random completions of the KW Eulerian path produced valid 64-hexagram sequences with all required properties. ✓

### Total Count

**Total valid KW-type sequences = 150,955,488 × 40,320⁸ ≈ 1.054 × 10⁴⁵**

This is 10⁻⁴⁴ of the full 64! ≈ 10⁸⁹ permutation space.

---

## Thread A-bis: What Makes KW Special Within 10⁴⁵

### The Uniform Matching Property

KW uses the **same generator mask** for all 4 pairs within each orbit — a "uniform matching":

| Orbit | Signature | KW Mask | Weight |
|-------|-----------|---------|--------|
| Qian | (0,0,0) | OMI (1,1,1) | 6 |
| XChu | (0,0,1) | I (0,0,1) | 2 |
| Shi | (0,1,0) | M (0,1,0) | 2 |
| WWang | (0,1,1) | MI (0,1,1) | 4 |
| Bo | (1,0,0) | O (1,0,0) | 2 |
| Xu | (1,0,1) | OI (1,0,1) | 4 |
| Zhun | (1,1,0) | OM (1,1,0) | 4 |
| Tai | (1,1,1) | OMI (1,1,1) | 6 |

**Statistics:**
- Only 7 of 105 matchings per orbit are uniform → P(uniform) = 1/15
- All 8 orbits uniform: (1/15)⁸ ≈ **3.9 × 10⁻¹⁰**
- Specific KW matching: (1/105)⁸ ≈ 7 × 10⁻¹⁷

### The Mask-Signature Identity

**For 7 of 8 orbits: mask = signature exactly.** For Qian(000): mask = OMI = complement of sig.

**Operational meaning:** The orbit signature (o,m,i) = (l₁⊕l₆, l₂⊕l₅, l₃⊕l₄) tells you which line pairs are asymmetric. KW's pairing rule is: *swap exactly the asymmetric line pairs*. For Qian (fully symmetric), flip everything.

This is a structural identity — the orbit classification (topological) coincides with the pair construction (combinatorial).

### Complete Generator Coverage

All 7 non-identity generators {O, M, I, OM, OI, MI, OMI} appear exactly once across 8 orbits, with OMI appearing twice (for Qian and Tai, the Eulerian endpoints).

Among 7⁸ = 5,764,801 possible uniform assignments:
- 141,120 have exactly one repeated mask (P ≈ 2.4%)
- KW's specific assignment: P ≈ 1/8,007

---

## Thread D: Self-Loop Placement

### Self-Loop Structure

The multigraph has exactly **2 self-loops**:
- **Qian(000) → Qian(000):** multiplicity 1
- **WWang(011) → WWang(011):** multiplicity 1

In any Eulerian path, each self-loop must be used exactly once. The position (bridge index 0..30) is a free parameter.

### KW Self-Loop Positions

| Self-loop | Bridge position | Hexagrams | Location |
|-----------|----------------|-----------|----------|
| Qian | **B13** | 27-28 (Yi-Da Guo) | Upper/lower canon boundary |
| WWang | **B18** | 37-38 (Jia Ren-Kui) | Mid-lower canon |

### Position Distributions (500K Hierholzer samples + 50K DFS samples)

**Forbidden positions** (structural constraints):

| Position | Qian | WWang | Reason |
|----------|------|-------|--------|
| B0 | **Allowed (25%)** | Forbidden | Walk starts at Qian; WWang unreachable in 0 steps |
| B1 | Forbidden | Forbidden | No edge into Qian from {Shi, Zhun, Tai}; minimum 3 steps to return |
| B2 | Forbidden | Forbidden | Same — shortest Qian return cycle has length 3 |
| B28 | Forbidden | **Peak (~10%)** | Qian can't reach Tai in 2 remaining steps |
| B29 | **Peak (~7%)** | Forbidden | WWang has no edge to Tai; can't end correctly |
| B30 | Forbidden | Forbidden | Walk must end at Tai |

**Qian self-loop distribution:**

```
Position  |  Pct (DFS) |  Notes
B0        |  24.9%     |  Strong peak — immediate self-loop from start
B1-B2     |   0.0%     |  Forbidden (can't return to Qian in 1-2 steps)
B3-B26    |  2.0-3.6%  |  Nearly uniform, gradual increase
B27       |   6.3%     |  Secondary peak
B28       |   0.0%     |  Forbidden
B29       |   6.9%     |  Secondary peak (penultimate)
B30       |   0.0%     |  Forbidden
B13 (KW)  |   2.6%     |  Interior, rank ~15/27 — unremarkable
```

Mean position: ~14. Median: ~14. KW's B13 is near the mean.

**WWang self-loop distribution:**

```
Position  |  Pct (DFS) |  Notes
B0-B2     |   0.0%     |  Forbidden (shortest path to WWang = 3 edges)
B3-B26    |  2.2-5.9%  |  Monotonically increasing toward later positions
B27       |   7.6%     |  Peak near end
B28       |  10.5%     |  Maximum — last available position
B29-B30   |   0.0%     |  Forbidden (no WWang→Tai edge)
B18 (KW)  |   3.5%     |  Interior, rank ~12/26 — unremarkable
```

Mean position: ~18. Median: ~18. KW's B18 is near the mean.

### Joint Distribution

- **556 distinct joint positions** observed in 500K samples
- KW joint (13, 18): **0.09-0.12%** of paths (rank ~300-400/556)
- **Most common** joint: Qian@B0, WWang@B28: ~3%
- **Qian before WWang:** 56-60% of paths (KW: yes, Qian@13 < WWang@18)
- **Mean distance (WWang - Qian):** 4-5 bridges (KW distance: 5)

### Independence of Self-Loop Positions

Testing whether P(joint) ≈ P(Qian) × P(WWang):
- P(Qian@13): 2.6%
- P(WWang@18): 3.5%
- If independent: P(both) ≈ 0.091%
- Actual: ~0.09-0.12%
- **Ratio ≈ 1.0-1.3x** — approximately independent, slight positive correlation

### Interpretation

Self-loop positions are **not forced** by the Eulerian constraint:
- **Qian self-loop** can appear at 27 of 31 positions (0, 3-27, 29)
- **WWang self-loop** can appear at 26 of 31 positions (3-28)
- Distributions are non-uniform but smooth in the interior

**KW's choices (B13 and B18) are:**
- ✅ Interior positions (avoiding boundary peaks at B0, B27-29)
- ✅ Near the respective means/medians
- ✅ Both in the "middle third" of the walk
- ❌ Not special — typical interior positions
- ❌ Not forced — each has ~30 alternatives

**The structural insight:** KW avoids the "trivial" options:
1. **Not using the Qian self-loop immediately** (position 0, the 25% peak). This creates a longer opening exploration before returning to Qian.
2. **Not placing WWang self-loop near the end** (position 28, the 10% peak). This distributes structure more evenly.

---

## Key Conclusions

### What IS forced by the four constraints:
1. Start at Qian(000), end at Tai(111) ← exact
2. Each orbit visited exactly 4 times ← exact
3. All 31 bridge transitions used exactly as prescribed ← exact
4. The orbit multigraph structure ← exact
5. Eulerian property of the bridge walk ← **theorem** (100% of orbit-paired sequences are Eulerian)

### What is NOT forced:
1. **Which Eulerian path** — 150 million options
2. **Which pairing within orbits** — 105 options per orbit
3. **Which pair ordering** — 24 per orbit
4. **Which orientation** — 16 per orbit
5. **Self-loop positions** — 27 × 26 ≈ 700 valid joint positions

### What IS remarkable about KW (beyond the four constraints):

| Property | p-value | Layer |
|----------|---------|-------|
| Uniform matching (all 8 orbits) | **3.9 × 10⁻¹⁰** | Matching |
| Mask = signature identity | **7 × 10⁻¹⁷** | Matching |
| S=2 absence | **0.012** | Ordering |
| Qian→Tai endpoints | **0.018** | Ordering |
| Complete generator coverage | **1/8,007** | Matching |
| No weight-5 bridges | **0.046** | Ordering (consequence of S=2) |
| Joint S=2-free AND Qian→Tai | **0.0002** | Ordering |
| All measured properties | **< 10⁻⁴** | Combined |

### The Constraint Hierarchy

**Level 0:** The space — 64 hexagrams ∈ {0,1}⁶, 8 orbits of 8.

**Level 1:** Orbit-consistent pairing — forces Eulerian bridge walk (theorem). Eliminates ~44 orders of magnitude.

**Level 2:** Uniform matching per orbit — not forced. P ≈ 4 × 10⁻¹⁰. KW uses mask = signature.

**Level 3:** Pair ordering — determines bridge structure. S=2 absence and Qian→Tai are significant (p < 0.02 each).

**Level 4:** Pair orientation — remaining degree of freedom (2³² ≈ 4 × 10⁹ choices).

The deepest selection principle is the **mask-signature identity**: KW's pairing rule IS the orbit's own symmetry structure, applied as a combinatorial operator. This single principle (mask = signature for non-zero sig, OMI for zero sig) determines 7 × 10⁻¹⁷ of the matching layer, leaving "only" the Eulerian path and pair ordering as remaining degrees of freedom.

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `graph_analysis.py` | BEST theorem exact Eulerian path count | ✓ Verified |
| `best_crosscheck.py` | Independent BEST computation + first-departure decomposition | ✓ Verified |
| `hexagram_completion.py` | Within-orbit matching enumeration, independence proof | ✓ Verified |
| `matching_analysis.py` | Uniform vs mixed matchings, mask diversity | ✓ Complete |
| `mask_orbit_correspondence.py` | mask = signature identity discovery | ✓ Complete |
| `selfloop_fast.py` | Self-loop position distributions (Hierholzer + DFS) | ✓ 500K + 50K samples |
| `selfloop_exact.py` | Exact first-departure from Qian | ✓ Partial |
| `enumerate_eulerian.py` | Naive enumeration (superseded by BEST) | Killed — 150M too large |
| `sample_eulerian.py` | Original sampling script | Superseded by selfloop_fast.py |
