# Dynamics Findings (Threads C + E + G)

## Executive Summary

Three threads investigating the structure **within** the ordering layer: the meta-hexagram walk (C), the kernel dressing chain (E), and the factored basis decomposition (G).

**Core findings:**

1. **Meta-hexagram multiset is a graph invariant** — EVERY Eulerian path through the orbit multigraph produces the SAME set of 31 meta-hexagrams (same 26 unique, same #38 Kui ×3, same mean weight 3.000). Only the ordering varies. This is a theorem, not an empirical finding.
2. **KW's kernel chain is more uniform than random** — chi² from uniform at 7th percentile (p = 0.07). Marginal but suggestive: KW selects for near-uniform kernel dressing.
3. **KW's kernel XOR chain is dominated by OMI** — 8/30 consecutive kernel XORs are OMI (26.7%), vs 12.8% expected. This means consecutive bridges tend to use maximally different kernel dressings.
4. **In the factored basis, within-pair orbit changes vanish** — the pair mask = orbit signature, so applying it does NOT change the orbit coordinates. The orbit trajectory is step-function constant within pairs, changing only at bridges.
5. **Orbit uniformity is trivially forced** — ANY complete traversal of {0,1}⁶ visits each orbit exactly 8 times (partition property). Eulerian is forced by orbit-consistent pairing, not by orbit-uniformity.

---

## Thread C: Meta-Hexagram Walk Structure

### Construction

Each pair has a 3-bit orbit signature sig_k = (L1⊕L6, L2⊕L5, L3⊕L4). Stacking adjacent signatures produces a 6-bit meta-hexagram:

```
meta_hex(k) = (sig_k[0], sig_k[1], sig_k[2], sig_{k+1}[0], sig_{k+1}[1], sig_{k+1}[2])
```

This maps each bridge to a specific element of {0,1}⁶ — itself a hexagram.

### The Invariance Theorem

**Theorem.** The multiset of 31 meta-hexagrams is an invariant of the orbit multigraph. It does not depend on which Eulerian path is chosen.

**Proof.** The meta-hexagram at bridge k is the concatenation of the endpoints of edge k: (source_orbit, target_orbit). An Eulerian path traverses each edge exactly once. Therefore the multiset of meta-hexagrams equals the multiset of edges. Since the edge multiset is a property of the graph (not the path), the meta-hexagram multiset is invariant. **QED.**

**Consequence:** All properties that depend only on the meta-hexagram *multiset* — number of unique meta-hexagrams, most-repeated meta-hexagram, mean weight, meta-signature distribution — are invariant across all 150,955,488 Eulerian paths.

### Empirical Verification

10,000 sampled Eulerian paths: **100%** produce identical statistics:

| Property | Value | Variance across paths |
|----------|-------|-----------------------|
| Unique meta-hexagrams | **26/31** | **0** (invariant) |
| Most repeated | **#38 Kui, 3×** | **0** (invariant) |
| Mean meta-weight | **3.000** | **0** (invariant) |
| Meta-sig distribution | {MI:7, M:6, OM:5, I:3, O:3, OMI:3, id:2, OI:2} | **0** (invariant) |

### The Complete Meta-Hexagram Table

Every meta-hexagram corresponds to an edge in the orbit multigraph:

| Edge | Meta-hex | Mult | KW # | Name | Meta-sig |
|------|----------|------|------|------|----------|
| Qian→Qian | 000000 | 1 | #2 | Kun | id |
| Qian→Shi | 000010 | 1 | #8 | Bi | M |
| Qian→Zhun | 000110 | 1 | #45 | Cui | MI |
| Qian→Tai | 000111 | 1 | #12 | Pi | OMI |
| XChu→Bo | 001100 | 1 | #62 | Xiao Guo | id |
| XChu→Zhun | 001110 | 1 | #31 | Xian | M |
| **XChu→Tai** | **001111** | **2** | **#33** | **Dun** | **OM** |
| **Shi→XChu** | **010001** | **2** | **#4** | **Meng** | **OM** |
| Shi→Bo | 010100 | 1 | #40 | Xie | MI |
| Shi→Zhun | 010110 | 1 | #47 | Kun | I |
| WWang→Qian | 011000 | 1 | #46 | Sheng | MI |
| WWang→XChu | 011001 | 1 | #18 | Gu | OMI |
| WWang→Shi | 011010 | 1 | #48 | Jing | I |
| WWang→WWang | 011011 | 1 | #57 | Xun | OI |
| Bo→Qian | 100000 | 1 | #24 | Fu | O |
| **Bo→WWang** | **100011** | **2** | **#42** | **Yi** | **M** |
| Bo→Xu | 100101 | 1 | #21 | Shi He | I |
| Xu→Shi | 101010 | 1 | #63 | Ji Ji | OMI |
| Xu→WWang | 101011 | 1 | #37 | Jia Ren | MI |
| Xu→Bo | 101100 | 1 | #55 | Feng | O |
| Xu→Tai | 101111 | 1 | #13 | Tong Ren | M |
| Zhun→XChu | 110001 | 1 | #41 | Sun | M |
| **Zhun→Xu** | **110101** | **3** | **#38** | **Kui** | **MI** |
| Tai→Shi | 111010 | 1 | #5 | Xu | OI |
| Tai→Bo | 111100 | 1 | #34 | Da Zhuang | OM |
| Tai→Zhun | 111110 | 1 | #43 | Guai | O |

### Why Kui Appears 3×

#38 Kui (Opposition, 110101) is the meta-hexagram for the edge Zhun→Xu. This edge has multiplicity 3 — the highest in the multigraph. Since the meta-hexagram is just the edge encoded as a 6-bit string, Kui's triple appearance is forced by the Zhun→Xu multiplicity.

**Structural interpretation:** Kui (Opposition/Estrangement) encodes the OM→OI transition — the most-used inter-orbit connection. The orbit pair Zhun/Xu shares the O generator and differs only in the M↔I axis. This is the most "traversed" structural boundary in the sequence, and the hexagram of Opposition is the meta-level signature of that boundary.

### What DOES Vary: Meta-Walk Ordering

The ordering of the 31 meta-hexagrams varies across Eulerian paths. In 100 sampled paths, all 100 had distinct meta-walk orderings. Specific properties:

- **Kui placement:** 97/100 distinct position patterns for Kui's 3 appearances. KW places Kui at positions (1, 16, 24) — not seen in the 100-sample batch.
- **Non-overlapping uniqueness:** Varies from 12/16 to 16/16 unique (KW has 15/16, ~57th percentile).

### Meta-Signature Distribution (Invariant)

The meta-signature of each meta-hexagram = (bit0⊕bit5, bit1⊕bit4, bit2⊕bit3) = the cross-generator decomposition from 13-meta.md:

| Meta-sig | Name | Count/31 | % | Interpretation |
|----------|------|----------|---|----------------|
| (0,1,1) | MI | 7 | 22.6% | O=I across, M shifts, I≠O across |
| (0,1,0) | M | 6 | 19.4% | O=I across, M shifts, I=O across |
| (1,1,0) | OM | 5 | 16.1% | O≠I across, M shifts, I=O across |
| (0,0,1) | I | 3 | 9.7% | O=I across, M stable, I≠O across |
| (1,0,0) | O | 3 | 9.7% | O≠I across, M stable, I=O across |
| (1,1,1) | OMI | 3 | 9.7% | max cross-disagreement |
| (0,0,0) | id | 2 | 6.5% | structural mirror |
| (1,0,1) | OI | 2 | 6.5% | O≠I across, M stable, I≠O across |

**MI dominates** (22.6%) — the middle-inner cross-axis is the most common meta-signature. This confirms the finding from 13-meta.md that M is the most "volatile" axis and is a direct consequence of the multigraph having MI-type transitions as the most common edge type (7/31).

---

## Thread E: Generator Chain Dynamics

### The Kernel Dressing Chain

Each bridge mask decomposes as mask = orbit_Δ ⊕ kernel_dressing. The kernel dressing is the symmetric component: kernel = (m₆, m₅, m₄), an element of Z₂³ = ⟨O,M,I⟩.

The KW kernel sequence (31 bridges):
```
M → OM → OMI → O → OMI → id → OI → M → O → MI → id → OMI → id → I → OM → OM → O → OM → OMI → OI → OI → O → MI → I → O → M → id → MI → OI → O → MI
```

### KW Kernel Frequency

| Generator | KW count | Expected (31/8) | Deviation |
|-----------|----------|------------------|-----------|
| O | **6** | 3.9 | +2.1 |
| OM | 4 | 3.9 | +0.1 |
| OMI | 4 | 3.9 | +0.1 |
| id | 4 | 3.9 | +0.1 |
| OI | 4 | 3.9 | +0.1 |
| MI | 4 | 3.9 | +0.1 |
| M | 3 | 3.9 | −0.9 |
| I | **2** | 3.9 | −1.9 |

Chi² from uniform: **2.29**

O is overrepresented (6×), I is underrepresented (2×). The outer generator dominates the kernel dressing — bridges preferentially apply outer-pair flips as their "hidden" symmetric component.

### Comparison to Random Completions

10,000 random pair orderings on KW's Eulerian path with KW's matching:

| Metric | KW | Sample mean ± std | KW percentile |
|--------|-----|-------------------|---------------|
| Chi² (uniformity) | **2.29** | 7.06 ± 3.77 | **7th** (more uniform than 93%) |
| Lag-1 autocorrelation | **0.067** | 0.125 ± 0.061 | **27th** (less repetitive than 73%) |
| Mean return time | **6.83** | 5.79 ± 0.70 | High (longer returns) |

**Interpretation:** KW's kernel chain is **more uniform than typical** (7th percentile in chi²). The nearly-uniform generator usage is not forced by the constraints — random completions show chi² values 2-3× larger. The p-value (0.07) is marginal but suggestive of a design principle: distribute kernel dressings as evenly as possible across the 8 generators.

### Consecutive Kernel XOR Analysis

The XOR of consecutive kernel dressings (kernel[k] ⊕ kernel[k+1]) measures how much the kernel changes step-by-step:

| XOR | KW count/30 | KW % | Random % |
|-----|-------------|------|----------|
| **OMI** | **8** | **26.7%** | **12.8%** |
| I | 5 | 16.7% | 12.0% |
| M | 5 | 16.7% | 12.6% |
| MI | 4 | 13.3% | 12.7% |
| OM | 3 | 10.0% | 12.6% |
| OI | 2 | 6.7% | 12.1% |
| id | 2 | 6.7% | 12.5% |
| O | 1 | 3.3% | 12.7% |

**OMI dominates at 2× the expected rate.** Consecutive kernel dressings tend to be maximally different — the full complement XOR appears 8 times out of 30. Meanwhile O appears only once, and id (no change) appears only twice. The kernel chain actively avoids repeating itself and favors maximum structural contrast between consecutive bridges.

**The random baseline shows perfectly uniform XOR distribution (~12.5% each).** KW's OMI concentration is a genuine structural feature of the specific ordering, not a consequence of the constraints.

---

## Thread G: Factored Basis Decomposition

### The Basis

Every hexagram h = (l₁,l₂,l₃,l₄,l₅,l₆) decomposes as:

```
orbit coords: (ō, m̄, ī) = (l₁⊕l₆, l₂⊕l₅, l₃⊕l₄)     [asymmetric part]
position coords: (o, m, i) = (l₆, l₅, l₄)                [base position]
```

Recovery: l₁ = ō⊕o, l₂ = m̄⊕m, l₃ = ī⊕i, l₄ = i, l₅ = m, l₆ = o.

The orbit coordinates identify WHICH orbit the hexagram belongs to. The position coordinates identify WHERE within the orbit it sits.

### Key Structural Results

**Within-pair orbit changes are zero.** Since KW uses mask = orbit signature, the pair mask flips exactly the asymmetric line pairs. In the factored basis, this means the pair mask changes only the position coordinates, leaving orbit coordinates unchanged. Verified: all 32 within-pair orbit changes are (0,0,0).

**Within-pair position changes are the masks themselves.** The pair mask in 3-bit form equals the orbit signature. Since mask = sig and the position change is determined by the mask's kernel component, the within-pair position changes reproduce the mask distribution exactly:

| Position change | Count | Interpretation |
|----------------|-------|----------------|
| OMI | 8 | Qian and Tai orbits (sig=000, 111 → mask=OMI) |
| O | 4 | Bo orbit (sig=100) |
| M | 4 | Shi orbit (sig=010) |
| I | 4 | XChu orbit (sig=001) |
| OM | 4 | Zhun orbit (sig=110) |
| OI | 4 | Xu orbit (sig=101) |
| MI | 4 | WWang orbit (sig=011) |

**Bridge position changes = kernel dressings.** Verified: 31/31 match. The kernel dressing IS the position change at each bridge — the two decompositions are identical.

**Each orbit visits all 8 positions.** Every orbit's 8 hexagrams (4 pairs × 2) cover all 8 possible position coordinates. This is forced by the matching structure (each matching is a perfect matching on K₈).

### The Two Trajectories

In the factored basis, the 64-step KW sequence decomposes into two independent 3-bit trajectories:

1. **Orbit trajectory** (ō, m̄, ī): Step-function constant within pairs, changing at bridges. The 31 bridge orbit changes reproduce the signature transition sequence from 13-meta.md. This trajectory is Eulerian through the orbit multigraph.

2. **Position trajectory** (o, m, i): Changes at both pair transitions and bridges. Within pairs, the position change = the orbit signature (mask = sig identity). At bridges, the position change = the kernel dressing. This trajectory has no Eulerian constraint — it's determined by the specific hexagram choices.

### Independence of Orbit and Position Changes at Bridges

Chi² test for independence of (orbit_change, position_change) at bridges: χ² = 62.15, df ≈ 49.

At the KW-specific level, there is **mild positive association** (χ² somewhat above df), suggesting the orbit and position changes are not fully independent in KW's specific sequence. However, this is a single-sequence observation and cannot be tested against a null easily.

---

## Orbit Uniformity and Eulerian Property

### Chain of Implications

```
orbit-consistent pairing (all pair masks ∈ Z₂³)
  → each orbit has exactly 4 pairs (8 hexagrams / 2)
  → pair-level orbit visits: exactly 4 per orbit (forced)
  → degree balance: in = out at each internal orbit, ±1 at endpoints
  → Eulerian bridge walk (theorem)
```

### Orbit Uniformity Is Trivially Forced

**Any** complete traversal of {0,1}⁶ visits each orbit exactly 8 times — this is simply because the 8 orbits form a partition of the 64-element set into equal parts. This holds for Hamiltonian paths, random permutations, or any other complete ordering. Verified: 5000/5000 random Q₆ Hamiltonian paths have perfectly uniform orbit visits.

Therefore: orbit-uniformity is NOT a constraint at all — it's a tautology. The **real** constraint is orbit-consistent pairing, which forces the bridges to form an Eulerian walk. Without orbit-consistent pairing, the bridges can have arbitrary degree imbalances and are never Eulerian (as shown in B1).

---

## Synthesis: What's Forced vs What's Chosen

### Forced by the Multigraph (Invariant across all Eulerian paths):
- Meta-hexagram multiset (26 unique, Kui ×3)
- Meta-signature distribution (MI: 7, M: 6, OM: 5, ...)
- Mean meta-weight (exactly 3.000)
- Total self-loops (2: Qian and WWang)

### Forced by KW's Matching (mask = sig):
- Within-pair orbit changes are zero
- Within-pair position changes reproduce the mask distribution
- Bridge position changes = kernel dressings

### Chosen by KW (Not forced by constraints):
- **Kernel chain uniformity** (7th percentile in chi² — more uniform than 93% of random completions)
- **Kernel XOR chain dominated by OMI** (26.7% vs 12.8% expected — maximally contrastive consecutive bridges)
- **Meta-walk ordering** (specific placement of Kui's 3 appearances, etc.)
- **Low lag-1 autocorrelation** (0.067 vs 0.125 mean — kernel chain actively avoids repetition)

### The Kernel Chain as Hidden Structure

The kernel dressing sequence is invisible to the meta-hexagram construction — meta-hexagrams see only the orbit-change (antisymmetric) component of each bridge. The kernel is the "hidden variable" that operates below the meta-level.

KW's kernel chain shows two suggestive properties:
1. **Near-uniform generator usage** — distributes dressings evenly across all 8 generators
2. **Maximally contrastive consecutive dressings** — the OMI XOR dominance means consecutive bridges use maximally different kernel dressings

These properties are consistent with a design principle of **maximum diversity in the hidden layer** — while the visible layer (orbit transitions) is constrained to be Eulerian, the invisible layer (kernel dressings) is made as varied and non-repetitive as possible.

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `thread_ceg_dynamics.py` | Combined C+E+G analysis | ✓ Complete |
| `meta_invariance_proof.py` | Proof that meta-hex multiset is graph invariant | ✓ Complete |
| `orbit_uniformity_check.py` | Orbit uniformity in random Q₆ paths | ✓ Complete |
