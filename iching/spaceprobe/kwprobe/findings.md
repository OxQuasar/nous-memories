# KW Sequence Through the Divination Lens

## Core Discovery: 互 Convergence Basins

Iterated nuclear extraction (互→互→互→...) partitions all 64 hexagrams into **three basins** determined entirely by the **two interface lines** (line 3 = top of lower trigram, line 4 = bottom of upper trigram):

| Interface | Basin | Attractor | Count |
|-----------|-------|-----------|-------|
| Both yin (0,0) | Kun | Fixed point: 000000 | 16 |
| Both yang (1,1) | Qian | Fixed point: 111111 | 16 |
| Mixed (0,1 or 1,0) | Kan↔Li | 2-cycle: 010101↔101010 | 32 |

**The facing-line interpretation:** The interface lines are where each trigram *presents to the other*. Same-polarity encounters resolve (to pure type). Cross-polarity encounters persist as irreducible oscillation.

## Theorem: 互 Preserves Basins

**互 never changes the basin.** The nuclear hexagram always belongs to the same basin as its parent.

*Proof:* 互(h) has bits [h₁, h₂, h₃, h₂, h₃, h₄]. Its interface = (bit₂, bit₃) = (h₃, h₂) — the original interface *swapped*. Since basin depends only on homogeneity: (0,0)↔(0,0), (1,1)↔(1,1), mixed↔mixed. QED.

**Consequences:**
- 本→互 basin change: **0/32 pairs** (0%). Algebraically impossible.
- 本→变 same basin: **28/32 pairs** (88%). The 4 exceptions are the cross-basin complement pairs.
- The dominant divination trajectory is X→X→X (same basin throughout): 28/32.
- Basin is an **invariant** of the entire 互 chain. Once determined by the interface, it never changes.

## The 互 Interface Map

| Interface | 互 maps to | Effect |
|-----------|-----------|--------|
| (0,0) | (0,0) | Fixed — Kun stays Kun |
| (1,1) | (1,1) | Fixed — Qian stays Qian |
| (0,1) | (1,0) | Swap — but same basin class |
| (1,0) | (0,1) | Swap — but same basin class |

互 amplifies the interface: the interface lines become the center of the nuclear hexagram, then echo inward. The interface is the fixed point of this amplification, and its homogeneity/heterogeneity is absolutely conserved.

## The 互 Graph (16 vertices)

Three disconnected components:

- **Kun component** (4 vertices): 3 feeders → 1 fixed point (000000)
- **Qian component** (4 vertices): 3 feeders → 1 fixed point (111111)
- **KanLi component** (8 vertices): 6 feeders → 2-cycle core (010101↔101010)

Perfectly symmetric. Each attractor has exactly 3 feeder vertices. The three components are basin-segregated (no 互 path crosses basins).

## Kernel I-Component Controls Basin Crossing

**Algebraic theorem:** kernel[I] = xor_bit₂ ⊕ xor_bit₃

| kernel I | Interface change | Basin effect |
|----------|-----------------|-------------|
| I=0 | Both bits change together (or not at all) | Stays within {Kun,Qian} or within KanLi |
| I=1 | One bit changes, other doesn't | Always crosses between {Kun,Qian} ↔ KanLi |

### H subgroup splits by basin behavior

| Subgroup | Members | kernel I | Basin effect |
|----------|---------|----------|-------------|
| H_preserve | {id, O} | I=0 | Respects basin boundaries |
| H_cross | {MI, OMI} | I=1 | Always crosses to/from KanLi |

### Hamming distance gradient by interface change

| Interface change | Mean Hamming distance | Count |
|-----------------|----------------------|-------|
| No change (0,0) | 2.42 | 19 |
| One flip | 3.05 | 19 |
| Both flip (1,1) | 4.28 | 25 |

More interface disruption → more total change.

## Basin Clustering (0th percentile)

| Metric | KW | Random mean | Percentile |
|--------|-----|------------|-----------|
| Basin run count | 26 | 41.0 | **0th** (extreme clustering) |
| Compression ratio | 0.61 | 0.633 | 14.7th |
| UC/LC asymmetry | 6 | 0.0 | **97.4th** |

Against pair-respecting orderings: run count = 73rd percentile (pair structure accounts for most clustering), asymmetry = 92.5th (still significant).

**Information content:** Shannon entropy = 1.500 bits/symbol (94.6% of max). Conditional entropy given previous = 1.297. Knowing the previous basin saves 0.203 bits. The signal is in spatial clustering, not in symbol frequencies.

## Sequence Framing — Attractors at Boundaries

| KW Position | Hexagram | Attractor type |
|------------|----------|----------------|
| 1-2 | Qian, Kun | The two fixed points of 互 |
| 63-64 | Ji Ji, Wei Ji | The 2-cycle of 互 |

Combined probability: ~5×10⁻⁷. **From rest to motion.**

## The Self-Reverse Skeleton

8 self-reverse hexagrams form 4 complement pairs — the **only cross-basin pairs** and **almost the only site of direct Kun↔Qian transitions**:

| Positions | Pair | Basin crossing |
|-----------|------|---------------|
| #1-#2 | Qian/Kun | Qian↔Kun |
| #27-#28 | Yi/Da Guo | Kun↔Qian |
| #29-#30 | Kan/Li | Kun↔Qian |
| #61-#62 | Zhong Fu/Xiao Guo | Kun↔Qian |

**Direct Kun↔Qian transitions:** 6 total, **5 of 6 occur at skeleton positions**. The single non-skeleton exception is step 42→43 (Yi→Guai). The self-reverse skeleton IS the apparatus that enables basin crossing. 5/6 have kernel=id, 4/6 are complement (distance 6).

**Theorem:** Cross-basin pairs must be complement pairs with homogeneous interface. Reverse pairs always preserve basin. Only self-reverse hexagrams with (0,0) or (1,1) interface, paired by complement, can cross basins.

## Canon Basin Asymmetry (p = 0.026)

| Basin | Upper Canon | Lower Canon |
|-------|------------|-------------|
| Kun | **11**/30 (37%) | 5/34 (15%) |
| Qian | 5/30 (17%) | **11**/34 (32%) |
| KanLi | 14/30 (47%) | 18/34 (53%) |

**Chiastic:** UC starts with Qian but is attracted to Kun. LC is attracted to Qian.

### Basin × Developmental Priority

| Basin | 克 | 生 | 比和 | UC count | LC count |
|-------|-----|-----|------|----------|----------|
| Kun | 44% | 31% | 25% | **11** | 5 |
| KanLi | 38% | **44%** | 19% | 14 | 18 |
| Qian | 44% | 31% | 25% | 5 | **11** |

Kun and Qian have identical five-phase profiles. **KanLi is different:** more 生 (generative), less 克 (adversarial). The oscillation basin favors growth; the fixed-point basins favor conflict.

UC (algebraic optimization) → Kun (emptiness, stripping away). LC (meaning organization) → Qian (fullness, building up). **Algebra strips away; meaning fills in.**

## Later Heaven Compass Alignment

| Facing type | Compass positions | Basin (doubled) |
|------------|------------------|-----------------|
| ○○ (both yin) | N (Kan), SW (Kun) | Kun |
| ●● (both yang) | S (Li), NW (Qian) | Qian |
| ○● (yin/yang) | NE (Gen), SE (Xun) | KanLi |
| ●○ (yang/yin) | E (Zhen), W (Dui) | KanLi |

The Later Heaven arrangement places facing types coherently:

- **N-S axis (Kan↔Li):** Complete facing opposition (both lines opposite). This is the axis of maximum polarity tension — and the basis of the KanLi oscillation.
- **E-W axis (Zhen↔Dui):** No facing opposition (both lines same!). Same-facing axis.
- **Diagonal axes:** Partial opposition (one line each).

The N-S axis is special: it's the only axis with complete facing opposition. This is why Kan↔Li is the irreducible pair — their encounter opposes at every interface.

## Doubled and Alternating Hexagrams

| Type | Count | Basin distribution |
|------|-------|-------------------|
| Doubled (lower=upper) | 8 | 2 Kun, 4 KanLi, 2 Qian |
| Self-reverse | 8 | 4 Kun, 4 Qian (no KanLi!) |
| Pure alternating | 2 | JiJi + WeiJi = pure KanLi |

For doubled trigrams, basin = (top, bottom) of the trigram. If top=bottom (Kun, Kan, Li, Qian), basin is Kun or Qian. If top≠bottom (Gen, Xun, Zhen, Dui), basin is KanLi.

Self-reverse hexagrams split perfectly: 4 Kun, 4 Qian. No KanLi. This is algebraically forced: self-reverse means bit₂=bit₃ (since line 3 maps to line 4 under reversal), so interface is always (x,x) = homogeneous.

## Longer-Range Correlations

| Lag | Autocorrelation | vs Expected (0.375) |
|-----|----------------|---------------------|
| 1 | **0.603** | Strongly above |
| 2 | 0.306 | Below (anti-correlated!) |
| 6 | 0.448 | Above |
| 8 | 0.196 | **Strongly below** (χ²=12.63, significant) |
| 12 | 0.442 | Above |

**Lag-2 anti-correlation:** consecutive basins tend to match (lag 1), but skip-one basins tend to differ. This is consistent with pair structure (pairs share basin, but adjacent pairs often differ).

**Lag-8 significance:** Strong anti-correlation at lag 8 (χ²=12.63, p<0.05). Groups of ~8 tend to alternate between basin types. This might reflect the octagram structure.

## He Tu Connection

### He Tu always flips the facing line

He Tu is an involution with exactly two XOR masks:
- **XOR 101** (flip top + bottom): Gen↔Zhen, Kan↔Qian
- **XOR 110** (flip top + middle): Kun↔Xun, Dui↔Li

The **top bit always flips** — the facing line (as lower trigram) always reverses.

### He Tu vs Fu Xi

| | He Tu | Fu Xi (complement) |
|---|---|---|
| XOR masks | 101 or 110 | 111 always |
| Facing opposition | Lower always, upper sometimes | Both always |
| Intersection | ∅ (no shared pairs) | |

Fu Xi maximizes opposition. He Tu is partial — always opposes the facing line, preserves one other line per pair.

## 互 Commutation Properties

- **互 commutes with reverse:** 互(rev(h)) = rev(互(h))
- **互 commutes with complement:** 互(comp(h)) = comp(互(h))
- **互 preserves basins** (proven algebraically)
- Both pair operations preserve KW pair structure through 互 projection

## Intra-pair vs Inter-pair 互 Bridges

The 63 consecutive transitions split into 32 intra-pair (within pairs) and 31 inter-pair (between consecutive pairs). These have fundamentally different character:

| | Intra-pair (32) | Inter-pair (31) |
|---|---|---|
| Kernel | **100% identity** | Diverse (MI=7, OMI=6, OM=5, ...) |
| Mean hex distance | 3.75 | 2.94 |
| Mean 互 distance | **3.75** | **2.74** |
| Basin preserved | 88% | 32% |
| H-kernel | 100% | 55% |
| 互 relationship | 24 reverse, 4 complement, 4 same | 28 "other", 2 reverse, 1 same |

**Key finding: 互 changes MORE within pairs than between them.** Intra-pair 互 distance (3.75) > inter-pair (2.74). The pair structure creates large algebraic jumps (reverse/complement), while the inter-pair bridges are conservative small steps. The sequence is *smoother in 互-space at pair boundaries than within pairs*.

**Inter-pair 互 distances favor d=3 (42%).** Typical inter-pair step changes 3 of 6 互 bits — exactly half. The dominant mode is moderate change, not minimal or maximal.

**Intra-pair kernel is always identity.** Every KW pair has palindromic XOR (forced: reverse pairs have symmetric XOR, complement of self-reverse also has symmetric XOR). This is an algebraic constraint, not a choice.

**The inter-pair bridge is where the sequence decides.** The intra-pair step is algebraically forced. The inter-pair step determines the 互 walk, the basin transitions, and the sequence's information content.

### Inter-pair 互 walk: no attractor basins, but directional flow

**Flat visit distribution (forced).** Each of 16 互 values appears exactly 4 times in 64 positions. This is the fiber structure (互 is 4-to-1), not a sequence property.

**Directional sources and sinks.** The inter-pair bridge graph has pure sources (out-degree only) and pure sinks (in-degree only):

| 互 value | In | Out | Role |
|-----------|---:|----:|------|
| Kan/Li ◎ | 4 | 0 | Pure sink |
| Xun/Qian ● | 4 | 0 | Pure sink |
| Li/Kan ◎ | 0 | 3 | Pure source |
| Qian/Dui ● | 0 | 4 | Pure source |

Sources and sinks are **reverse pairs** (Xun/Qian = rev(Qian/Dui), Kan/Li = rev(Li/Kan)). Forced by pair structure: 互 commutes with reverse, so pair-end 互 = rev(pair-start 互). Bridges always flow from reversed-互 to primary-互.

**Temporal clustering carries the breathing signature.** The 4 visits per 互 value are not evenly spaced — attractor 互 values clump at their pole:
- Kun/Kun (fixed point): positions 2, 23, 24, 27 — clusters at UC end
- Qian/Qian (fixed point): positions 1, 28, 43, 44 — clusters at LC start
- Zhen/Gen: positions 29, 59, 60, 61 — bursts at sequence end (gaps: 30, 1, 1)

No attractor basins in the walk-graph sense, but return-time distribution reproduces the same breathing asymmetry.

### The kernel collapse: hex Z₂³ → 互 H ≅ V₄

**互 kernel is always in H = {id, O, MI, OMI}.** Proven over all 4032 hexagram pairs. This is algebraically forced by the 互 construction: 互 = [h₁, h₂, h₃, h₂, h₃, h₄] has bit₁=bit₃ and bit₂=bit₄, so M(互) = I(互) always.

**The mapping is 2-to-1:** hex_kernel → 互_kernel = (hex_M, hex_I, hex_I).

| Hex kernel pair | 互 kernel | What's erased |
|----------------|-----------|---------------|
| {id, O} | id | Hex outer asymmetry vanishes |
| {M, OM} | O | Hex middle → 互 outer |
| {I, OI} | MI | Hex interface → 互 middle+interface (locked) |
| {MI, OMI} | OMI | Both survive |

**The hex O component is invisible to 互.** Only M and I pass through. 8 hex kernels collapse to 4 互 kernels = H.

**Consequence for pair structure:** Intra-pair kernel is always id (palindromic XOR). This means the same trigram-level mask applies to both upper and lower trigrams — the pair transformation is a pure lift of a single trigram-level operation. The pairing lives on the diagonal of the S₄ × S₄ action. Inter-pair bridges break this diagonal: they apply different operations to upper and lower.

### 互 trigram asymmetry at bridges

At inter-pair bridges, the 互 kernel distribution is:

| 互 kernel | Count | Meaning |
|-----------|------:|---------|
| OMI | 13/31 | Max asymmetry: edge and core differ |
| O | 8/31 | Only edges differ |
| MI | 6/31 | Shared core differs |
| id | 4/31 | Perfectly symmetric |

**The 互 trigrams experience asymmetric operations at most bridges** (87% non-id). But M=I is locked always — the middle and interface break together or not at all.

**Directional asymmetry:** The lower 互 trigram never changes alone (0/31). The upper changes alone 5 times (all O-kernel bridges, 16%). The sequence protects the lower 互 trigram. Structurally: 互 lower depends on h₁ (lower trigram middle line), 互 upper depends on h₄ (upper trigram middle line). When only the edge differs, it's always h₄ that flips while h₁ stays fixed.

## The Character of the Walk

### Three-layer structure

The walk through basin space has three nested layers:

**Layer 1 — Basin Breathing.** The walk oscillates between a "pole" (Kun or Qian) and the "center" (KanLi). The pole shifts across the sequence:

| Phase | Pole | Mean polarity | Pattern |
|-------|------|--------------|---------|
| UC (positions 1-30) | Kun (○) | -0.20 | ○ ↔ ◎ oscillation |
| LC (positions 31-64) | Qian (●) | +0.18 | ● ↔ ◎ oscillation |

The running average (window=8) transitions smoothly from negative to positive with **zero crossings** — a monotonic breath from yin to yang. No oscillation at the macro scale.

**Layer 2 — KanLi Mediates.** KanLi is the bridge between the fixed-point basins. Of 9 KanLi runs: 5 bridge same-pole (returning oscillation), 4 bridge different poles (transition). Direct Kun↔Qian transitions are rare (3 at run level, all at skeleton positions). The walk breathes: pole → center → pole → center.

**Layer 3 — Facing Alternation.** Within KanLi, the two sub-types ○● and ●○ alternate **100% within pairs** (algebraically forced: reverse swaps bits 2↔3). Split is perfectly even: 16 of each. The facing transition matrix shows ○●→●○ (9) and ●○→○● (10) dominate, creating rapid oscillation within the KanLi runs.

### The run-level sequence

26 runs: `●○◎○◎●◎○◎○◎○●○●◎○●◎●◎●◎○●◎`

The pole-only sequence (KanLi stripped): `●○○●○○○●○●○●●●○●` (16 runs)

Cumulative pole counts equalize at #49-50 (13 Kun, 13 Qian), then Qian pulls slightly ahead (final: 16 each — perfect balance).

### The narrative arc

```
#1-2:    ●○    Opens with the two fixed points (Qian, Kun)
#3-12:   ○◎○◎  UC breathes between Kun and KanLi
#13-14:  ●●    Brief Qian island (Tong Ren / Da You)
#15-26:  ◎○◎○◎○◎ UC continues Kun-attracted breathing
#27-30:  ○●○●  Skeleton staccato — 4 rapid basin crossings
#30-34:  ●●●●● LC opens with Qian dominance
#35-40:  ◎◎◎◎◎◎ Longest KanLi run (relational hexagrams)
#41-56:  ○●◎●◎●◎● LC breathes between Qian and KanLi
#57-61:  ◎○○○  Last descent into Kun
#62:     ●     Final Qian flash (Xiao Guo)
#63-64:  ◎◎    Ends on KanLi — permanent oscillation
```

### Key properties

- **Basin conservation:** 互 never changes basin. 0/32 pairs change basin through 互. Basin is an exact invariant of nuclear extraction.
- **Pair conservation:** 28/32 pairs share basin. The 4 exceptions are the self-reverse skeleton.
- **Extreme clustering:** 0th percentile (26 runs vs random mean 41).
- **Chiastic asymmetry:** UC→Kun, LC→Qian. p=0.026.
- **Attractor framing:** Fixed points open, limit cycle closes. P ≈ 5×10⁻⁷.
- **Monotonic breath:** Running average crosses zero exactly once, at the canon break.

## The Dual Walk: Inner vs Outer

Each hexagram decomposes as outer(2 bits) × inner(4 bits). The inner determines 互, the outer is erased by 互. The KW walk operates on both simultaneously.

### The two walks are independent

| Metric | Value |
|--------|-------|
| Inner/outer distance correlation | -0.079 |
| Mutual information | 0.04 bits |
| P(both change)/P(independent) | 0.966 |

The inner walk (hidden structure) and outer walk (surface presentation) are statistically independent. They change at different rates, for different reasons.

### The inner walk dominates

| | Inner (互) | Outer (surface) |
|---|---|---|
| Changes | 58/63 steps (92%) | 45/63 steps (71%) |
| Mean distance per step | 2.16 (64% of total) | 1.19 (36% of total) |
| Runs | 59 (almost every step) | 46 |

The hidden structure is **more active** than the surface. Most of the walk's movement is inner.

### Transition types

| Type | Count | Meaning |
|------|-------|---------|
| Both change | 40/63 (63%) | Full transition |
| Inner only | 18/63 (29%) | Surface unchanged, hidden shifts |
| Outer only | 5/63 (8%) | Hidden unchanged, surface shifts |
| Neither | 0/63 (0%) | Never happens |

### Outer-only transitions are structurally special

The 5 cases where only the outer changes (same 互, different hexagram):

| Step | Pair | 互 value | Significance |
|------|------|---------|-------------|
| 23→24 | Bo/Fu | Kun/Kun | 互 = Kun fixed point |
| 43→44 | Guai/Gou | Qian/Qian | 互 = Qian fixed point |
| 55→56 | Feng/Lu | Xun/Dui | |
| 59→60 | Huan/Jie | Zhen/Gen | |
| 60→61 | Jie/Zhong Fu | Zhen/Gen | |

Bo/Fu and Guai/Gou sit at depth-0 attractors — their 互 IS the fixed point. When the hidden situation has reached its attractor, only the surface can change. **The walk can only move outward when the inner has converged.**

### The speed hierarchy

| Level | Bits | Runs | Changes/63 |
|-------|------|------|-----------|
| Full hexagram | 6 | 64 | 63 (100%) |
| Inner (互) | 4 | 59 | 58 (92%) |
| Outer (surface) | 2 | 46 | 45 (71%) |
| Basin (interface) | ~1 | 26 | 25 (40%) |

Each deeper projection is slower, more stable. The basin barely moves while the surface churns. This is the hallmark of a **hierarchical dynamical system**: fast outer dynamics, slow inner invariants.

## Summary

**The basin is the deepest invariant of the hexagram under nuclear extraction.** It captures the polarity of the encounter between upper and lower trigrams: whether they face each other with same or opposite character. This polarity survives all layers of 互 and determines the ultimate fate: resolution (Kun/Qian) or permanent oscillation (Kan↔Li).

The KW sequence walks through this invariant space as a **single breath** — from yin pole to yang pole, with KanLi as the center through which all transitions pass. The breath is monotonic at the macro scale, oscillatory at the micro scale, and ends without resolving.

The full walk decomposes into independent inner and outer components. The inner walk (hidden, 互-determining) dominates in activity. The outer walk (surface, erased by 互) is slower. The basin walk (interface, invariant under 互) is slowest of all. **Three timescales in one sequence**: fast surface, moderate hidden structure, slow attractor dynamics.

**What the tradition may not have known explicitly:**
- The two middle lines determine 互 convergence
- Basin is an exact algebraic invariant (互 never changes it)
- The H subgroup splits into basin-preserving and basin-crossing operations
- The facing-line classification is orthogonal to traditional yin/yang
- The N-S axis has complete facing opposition while E-W has none — explaining why Kan↔Li is the irreducible pair
- The sequence is a monotonic breath in polarity space with zero macro-oscillation
- KanLi basin favors 生 (44%) while fixed-point basins favor 克 (44%) — tension generates growth
- Inner and outer walks are independent — hidden structure changes faster than surface
- Outer-only transitions occur at attractor fixed points — when the depths have converged, only the surface can move

## Generative Principle Search (LOGOS kw-generative)

### Question

Given the 32 fixed pairs, what principle determines their ordering? Can the 31 inter-pair bridge choices be derived from a rule simpler than the sequence itself?

### Method

Six rounds of systematic algebraic probing across 124+ parameter configurations:

| Round | Approach | Best reconstruction |
|-------|----------|-------------------|
| 1 | Pair graph + greedy 互 | 3/31 |
| 2 | Sub-optimal bridge discriminants | — (feature analysis) |
| 3 | Hierarchical basin + local 互 | 5/31 |
| 4 | Kernel independence + scoring walk | **7/31** (ceiling) |
| 5 | Global structure (bipartite, 互-graph) | — (null results) |
| 6 | Null models + anomaly analysis | — (decisive anomaly) |

### The skeleton (what any theory must respect)

| Constraint | Evidence | Status |
|------------|----------|--------|
| Basin clustering | 0th percentile | Proven structural |
| Basin-crossing at sub-optimal bridges | 14/17 (p=0.0002) | Deliberate strategy |
| H-kernel preference | 12/14 at multi-option bridges, independent of basin | Real, independent |
| Chiastic canon asymmetry | UC Kun-heavy, LC Qian-heavy (p=0.026) | Real |
| KanLi mediation | 90% of cross-basin transitions | Structural consequence |
| Attractor framing | p ≈ 5×10⁻⁷ | Proven |
| 互 continuity | 12.7th percentile | Real but subordinate |

### The decisive datum: Run 13

The only 3-pair basin run (Jin→Jia Ren→Jian, pairs 17-18-19) follows ascending pair-number order, achieving the **worst** possible 互 weight (7 vs minimum 2). All seven 2-pair runs also follow ascending pair-number order but are trivially 互-compatible. Run 13 is where pair numbering and 互 optimization conflict — **pair numbering wins decisively.**

### What was eliminated

- Greedy 互-continuity: 3/31 (wrong path)
- Basin-constrained greedy: 5/31 (hierarchical model refuted)
- Combined scoring (basin + H-kernel + 互): 7/31 ceiling across all parameters
- Bipartite structure: identical to basin (zero additional information)
- 互-graph coverage: 79th percentile (unremarkable)
- Cost gradient: 25th percentile (depletion artifact)
- Algebraic sorting of pair position: no property correlates (all p > 0.5)

### Verdict

**The ordering is semantic with algebraic consequences.** The meanings determine the sequence. Basin clustering, 互 continuity, H-kernel preference, and chiastic structure are real but emergent — they arise because semantic categories correlate with binary structure. The algebraic approach found the constraints (skeleton), not the generator (flesh). The generator lives in the Xugua (序卦) commentary — the traditional text giving reasons for each hexagram's position. Pursuing it requires a semantic investigation, different paradigm from the algebraic probing completed here.

Best algebraic reconstruction: 7/31 (23%). The remaining 77% requires information the algebraic framework does not contain.

## Scripts

| Script | Content |
|--------|---------|
| `01_hu_sequence.py` | 互 sequence, transitions, five-phase along KW |
| `02_hu_deeper.py` | 互² convergence, 克 amplification, pair preservation |
| `03_basin_convergence.py` | Basin classification, depth structure, convergence chains |
| `04_cross_basin_and_depth.py` | Cross-basin pairs, depth-1 clustering, facing lines |
| `05_hu_graph_and_H.py` | 互 graph, H subgroup interaction, trigram groups |
| `06_basin_kernel_bridge.py` | Kernel I-component theorem, H splitting, distance gradient |
| `07_basin_uniqueness.py` | Monte Carlo uniqueness tests, He Tu facing opposition |
| `08_hetu_algebra.py` | He Tu as involution, XOR masks, facing-line analysis |
| `09_all_probes.py` | Basin info, priority, 变 circuit, doubled, Later Heaven, correlations, Kun↔Qian |
| `10_walk_character.py` | Walk grammar, oscillation pattern, breathing, facing-space |
| `11_dual_walk.py` | Inner vs outer decomposition, independence, speed hierarchy |
| `12_inter_pair_hu.py` | Intra vs inter-pair 互 bridges, pair-level 互 walk |
| `13_hu_bridge_attractors.py` | 互 walk graph, return patterns, basin gateways |
| `14_bridge_mask_vs_hu.py` | Surface-depth decoupling: inner minimized, outer maximized |
| `15_kernel_layer_decomp.py` | Kernel component → layer change (O vs MI) |
| `16_hu_kernel.py` | Kernel collapse hex Z₂³ → 互 H, 互 trigram asymmetry |
| `17_semantic_embeddings.py` | BGE-M3 embeddings of Tuan/Xugua/Guaci, similarity vs algebra |
| `18_semantic_residuals.py` | Trigram name/structural keyword deconfounding |
| `19_semantic_algebra_layers.py` | Layer decomposition: outer/inner/互/kernel/basin/S₄ orbit |
| `20_fivephase_algebra.py` | Five-phase × kernel/basin/H in S₄ and Z₂³ spaces |
| `17_semantic_embeddings.py` | Semantic similarity (BGE-M3) vs algebraic distance, basin, KW adjacency |
| `gen/01_pair_graph.py` | Pair graph, greedy 互 walk, random baselines |
| `gen/02_bridge_discriminant.py` | Sub-optimal bridge feature analysis, discrimination power |
| `gen/03_hierarchical_test.py` | Basin schedule + local 互 reconstruction |
| `gen/04_kernel_and_walk.py` | Kernel independence, cost gradient, scoring walk |
| `gen/05_global_structure.py` | Bipartite traversal, 互-graph walk, skeleton intervals |
| `gen/06_null_model_and_anomaly.py` | Null models, Run 13 anomaly, algebraic sorting tests |

## Semantic-Algebraic Bridge (LOGOS kw-semantic)

### Question

The generative search established that "the ordering is semantic with algebraic consequences." The iter8 semantic investigation found the Xugua, corridors, and two-regime structure. How do the algebraic and semantic descriptions relate at each transition?

### Method

Built a unified table joining algebraic profile (basin, 互 distance, kernel, preservation) with semantic profile (Xugua logic type, confidence, directionality) and corridor profile for all 31 inter-pair transitions. Tested six cross-tabulations via Fisher exact tests, in both corridor-rich (n=21) and corridor-free (n=10) zones.

### Finding: Grain-Dependent Coupling

The algebra-meaning relationship has a specific grain — the pair:

| Scale | Coupling | Evidence |
|---|---|---|
| Orientation (1 bit/pair) | **Complete** | 32/32, p < 10⁻⁵ |
| Individual bridges (multi-dim) | **Independent** | All 6 Fisher tests p ≥ 0.524 |
| Aggregate statistics (whole-seq) | **Emergent** | Basin clustering 0th %ile, chiastic p=0.026, framing p~10⁻⁷ |

**No algebraic feature predicts any semantic feature at the individual transition level.** H-kernel does not predict logic type. 互 distance does not predict confidence. Basin-crossing does not predict directionality. This holds equally in corridor-rich and corridor-free zones. Systematic prediction testing confirms: best lift over base rate = 1.05 (5%), best |MCC| = 0.32.

**One specific exception:** Both direct Kun↔Qian inter-pair crossings are cyclical (p=0.048). All 14 causal crossings route through KanLi. Exhaustion-reversal is the only narrative formula that jumps directly between fixed-point basins. Sample structurally fixed at n=2.

**Coupling appears wherever the question compresses to ~1 bit, vanishes at higher categorical dimensionality.** This is the natural grain of the object: the pair is the resolution at which algebra and meaning converge.

### Preserving bridges (structural note, n=9)

Lower-trigram preservation → 4/5 causal (ground carries causes). Upper-trigram preservation → 2/4 cyclical (canopy survives exhaustion). Fisher p=0.524. Interpretively coherent, permanently at n=9, not independently confirmable.

### Implication

The 7/31 algebraic reconstruction ceiling reflects genuine independence at the bridge level — there is no hidden algebraic rule that the search missed. The aggregate signatures (basin clustering, chiastic asymmetry, attractor framing) are emergent consequences of semantic ordering, not design criteria. The two descriptions are genuinely different projections of the same arrangement, converging at the pair level and diverging everywhere else.

Full analysis: `semantic/findings.md`

| `semantic/01_unified_table.py` | 31-transition table: algebraic + semantic + corridor profiles |
| `semantic/02_regime_test.py` | Regime comparison, preserving bridge analysis, Fisher tests |
| `semantic/03_prediction_and_exhaustion.py` | Prediction accuracy, exhaustion-basin correspondence, Kun↔Qian finding |

## Semantic Embedding Analysis

Embedded Tuan (彖傳), Xugua (序卦傳), and Guaci (卦辭) texts via BGE-M3 (1024-dim). Tested semantic similarity vs algebraic distance, basin membership, and KW adjacency.

### Three semantic layers

| Text | KW adjacency r | Hamming r | Basin clustering | Character |
|------|:-:|:-:|:-:|---|
| **Xugua** | **+0.276*** | 0.006 (ns) | weak (p=0.008) | Strongly sequential, algebra-blind |
| **Tuan** | +0.103*** | **-0.068*** | marginal (p=0.09) | Weakly sequential, sees algebra |
| **Guaci** | +0.047* | -0.036 (ns) | none | Nearly independent |

### Key findings

1. **Xugua is purely sequential.** Consecutive pairs have high semantic similarity (r=0.276, p=10⁻³⁶), but zero correlation with Hamming distance. The Xugua narrative creates semantic continuity *along* the sequence without tracking algebraic structure. Intra-pair vs inter-pair similarity is identical (0.761 vs 0.760) — pair boundaries are semantically invisible.

2. **Tuan sees the algebra.** Significant correlation between semantic similarity and Hamming distance (r=-0.068, permutation p=0.0001). Algebraically closer hexagrams get more similar Tuan commentaries. Top similar Tuan pairs (Xu↔Jian, Tai↔JiJi) tend to be algebraically close (d=2).

3. **Basin is semantically invisible.** Within-basin vs between-basin similarity is tiny across all three texts. The basin structure is algebraically real but the texts don't "know" about interface-line homogeneity.

4. **Xugua doesn't predict bridge algebra.** At inter-pair bridges, Xugua similarity has no correlation with hex distance, 互 distance, or basin (all p>0.2). The narrative logic at bridges is independent of algebraic signatures.

5. **Guaci is nearly independent.** The judgments don't systematically track algebra, basin, or KW adjacency.

### Interpretation

The semantic structure is *sequential continuity* (Xugua) layered on *algebraic awareness* (Tuan), on *near-independence* (Guaci). The meaning system tracks sequence order strongly but algebra weakly. The ordering logic of the Xugua creates its own semantic fabric that neither drives nor follows the algebraic signatures. The "semantic structure that produces algebraic consequences" operates at a level the texts reflect only partially — the Tuan sees it dimly, the Xugua ignores it, the Guaci is blind to it.

### Algebraic layer decomposition (script 19)

The Tuan semantic similarity was tested against every algebraic layer separately, with partial correlations and permutation tests.

**The Tuan tracks the hidden structure (互/inner bits), not the surface:**

| Algebraic layer | r vs Tuan | Perm p | |
|---|---:|---:|---|
| 互 full distance | **-0.075** | **0.0000** | Strongest signal |
| Inner bit distance | **-0.072** | **0.0000** | = 互 (inner bits determine 互) |
| 互 lower trigram dist | -0.068 | 0.0001 | *** |
| 互 upper trigram dist | -0.068 | 0.0001 | *** |
| Upper trigram dist | -0.050 | 0.0025 | ** |
| Lower trigram dist | -0.044 | 0.0068 | ** |
| Outer bit distance | -0.013 | 0.19 | Not significant |
| Kernel (all components) | ~0 | >0.4 | Invisible |
| Basin same | +0.038 | 0.09 | Marginal |

**Partial correlations reveal one underlying signal.** Controlling for inner bit distance reduces all other correlations to zero. Outer trigram and 互 trigram signals are entirely mediated through the inner bits. The primary driver is the inner 4 bits — the same bits that determine 互.

**S₄ orbit: reverse shares meaning, complement doesn't.**

| Orbit relationship | Mean Tuan similarity | n | vs baseline (0.683) |
|---|---:|---:|---|
| Reverse (swap upper/lower) | **0.720** | 28 | +0.037 |
| Complement (flip all) | 0.680 | 28 | -0.003 |
| Reverse + complement | 0.673 | 24 | -0.010 |

Reverse = same situation, different perspective → Tuan sees as similar.
Complement = opposite situation → Tuan sees as unrelated.

**Trigram-level clustering: 互 lower is strongest** (t=3.08, p=0.002). Standouts: Kan ☵ as 互 lower (0.708), Dui ☱ as 互 lower (0.714). The hidden lower trigram creates a semantic fingerprint.

**Residual analysis (script 18):** After physically removing all trigram names and structural keywords (剛柔中正上下天地陰陽) from texts and re-embedding, the Hamming correlation drops from r=-0.068 to r=-0.050 but remains significant (permutation p=0.0000). ~2/3 genuine semantic content, ~1/3 structural vocabulary. The Tuan perceives inner-bit structure through two channels: structural vocabulary (partial) and genuine situational meaning (dominant).

**The commentary writers perceived the hidden structure, not the surface.** The outer bits — the visible presentation of the hexagram — are semantically irrelevant. The inner 4 bits that determine 互 are what the Tuan tracks. Basin (interface homogeneity) and kernel (XOR symmetry class) are algebraically real but semantically invisible.

### Five-phase in S₄ and Z₂³ spaces (script 20)

Five-phase (生/克) relations were cross-tabulated with kernel type, basin transition, and H-membership across all algebraic layers.

**Five-phase operates on inner/互 trigrams, not outer.** Outer trigram five-phase distributes uniformly across all 8 kernels (χ²=30, p=0.35, Cramér's V=0.04). The 互 trigrams are strongly determined by kernel:

| Layer | χ² | Cramér's V | Significance |
|---|---:|---:|---|
| Outer (lower or upper) | 30.3 | 0.04 | ns (p=0.35) |
| 互 lower | 323.3 | 0.14 | *** (p=5.6e-52) |
| 互 upper | **2209.2** | **0.37** | *** (p≈0) |

**互 upper is the primary structural layer.** The I-component perfectly predicts five-phase at 互 upper (all 4032 directed pairs):

| 互 upper five-phase | I=0 count | I=1 count | Pattern |
|---|---:|---:|---|
| 比和 (same element) | 832 | **0** | I=1 → 比和 impossible |
| 生 (generative) | 512 | 256 | I=0 favored 2:1 |
| 克 (destructive) | 64 | 768 | I=1 favored 12:1 |

**The I kernel component is the switch.** I=0 → harmonious territory (比 or 生, almost no 克). I=1 → destructive territory (克 dominant, 比 impossible). Interface symmetry breaking produces elemental conflict.

**At consecutive KW transitions:** 互 upper 比和 → 100% basin preserved (22/22). 互 upper 体克用 → 90% basin crosses (9/10).

**Intra/inter polarity reversal.** The two 互 trigrams show opposite five-phase polarity at the same bridge type:

| Bridge type | 互 lower (生:克) | 互 upper (生:克) |
|---|---|---|
| Intra-pair | **克-dominant** (6:20) | **生-dominant** (12:4), 比=16 |
| Inter-pair | balanced (12:11) | **克-dominant** (10:15) |

The pair structure holds 互 upper in 生/比 (harmonious) and 互 lower in 克 (destructive). The bridge between pairs shifts 互 upper toward 克. The two 互 trigrams breathe in anti-phase.

**Five-phase agreement between upper and lower is rare.** Only 12/63 outer transitions and 15/63 互 transitions have the same five-phase relation on both trigrams. Lower and upper experience different elemental dynamics — the hexagram is a tension between two independent five-phase flows.

**Inner bits are where everything structural lives.** Tuan semantics track them. Five-phase dynamics operate on them. Basin is determined by them. The outer bits are presentation — algebraically free, semantically irrelevant, five-phase-neutral.

---

## The Architecture: n=3 Grammar, n=6 Vocabulary

The hexagram level (n=6) is a presentation layer. The trigram level (n=3) is where the structural grammar lives. Everything found in this investigation confirms this.

### The evidence

**互 extracts the trigram layer.** It strips the outer bits (the presentation) and works only with the inner 4 bits, which reconstitute as a trigram pair. Basin is determined by just 2 interface bits. The kernel collapse erases the outer component entirely. The deep structure is n=4 (inner bits) which is really n=3 with overlap — two trigrams sharing their interface.

**S₄ acts on 8 trigrams, not 64 hexagrams.** The three involutions, the four blocks, the Later Heaven arrangement — all trigram-level. The hexagram doubles this by stacking two trigrams, creating a product space. But the product doesn't add new algebraic structure — it gives the base structure room to be presented in 64 different ways.

**The pairing rule operates at n=3.** Reverse swaps upper and lower trigrams. Complement inverts both. Both are trigram-level operations lifted to hexagrams (kernel = id = same mask on both trigrams). The pair is the simplest hexagram-level structure that respects the trigram factorization.

**The narrative lives at n=6 because meaning needs specificity.** "Water over Mountain" means something different from "Mountain over Water" — Jian vs Meng, obstruction vs youthful folly. The narrative needs 64 distinct situations to tell its story. But the structural constraints the story obeys — basin coherence, 互 continuity, chiastic asymmetry — all reduce to n=3 properties.

### The architecture

**n=3 provides the grammar.** The S₄ action, the He Tu algebra, the Later Heaven compass, the H-subgroup, the basin structure, the kernel space — these are the rules of the language.

**n=6 provides the vocabulary.** 64 hexagrams = 64 distinct situations, each a specific stacking of two trigrams. The stacking gives meaning specificity that the trigram level cannot express.

**The KW sequence is a narrative composed in that vocabulary that respects that grammar without being generated by it.** The spaceprobe findings (S₄, He Tu, Later Heaven, H-subgroup) are n=3 results. The kwprobe findings (basin dynamics, 互 walk, kernel collapse) are the trace of n=3 structure visible through n=6 presentation. The semantic investigation confirmed the boundary: where n=3 structure ends (7/31), n=6 meaning begins.

### The 7/31 boundary

This number now has a structural interpretation. 7 of 31 inter-pair bridges are where n=3 constraints happen to coincide with the narrative's choice — where the grammar and the story agree by convergence, not by design. The remaining 24 are where the story exercises its n=6 freedom: choosing specific situations for their meaning while the n=3 shadow follows along, producing emergent algebraic signatures (basin clustering, chiastic asymmetry, attractor framing) without being optimized for them.

The sequence doesn't oscillate between structure and meaning. It is meaning, and structure is its shadow.
