# 互 Attractor Probe — Complete Findings

## 1. The 互 Projection: Definition and Dimensional Reduction

### Definition

互 (hùguà, nuclear hexagram extraction) is a map on 6-bit hexagrams:

```
hugua(b₀, b₁, b₂, b₃, b₄, b₅) = (b₁, b₂, b₃, b₂, b₃, b₄)
```

It takes the four inner lines (b₁–b₄), constructs two overlapping nuclear trigrams — lower (b₁,b₂,b₃) and upper (b₂,b₃,b₄) — sharing the interface bits (b₂,b₃), and assembles them into a new hexagram.

### The three-layer onion

The hexagram decomposes into 3 concentric layers of 2 bits each:

```
Layer 3 (outer):     b₀, b₅     — surface presentation (top/bottom lines)
Layer 2 (shell):     b₁, b₄     — nuclear trigrams' free parameter
Layer 1 (interface): b₂, b₃     — where upper and lower trigrams meet
```

Each 互 application peels exactly one layer:
- **Step 1**: erases outer bits (b₀, b₅)
- **Step 2**: erases shell bits (b₁, b₄)
- **After step 2**: only interface bits (b₂, b₃) remain — permanently

This is **algebraically necessary** given the map definition. The onion structure is not a metaphor — it IS the kernel chain of M (§3).

### The inner map formula

Projecting onto the 4-bit inner space (b₁, b₂, b₃, b₄):

**(i₀, i₁, i₂, i₃) → (i₁, i₂, i₁, i₂)**

Shift-and-duplicate. The interface bits (i₁, i₂) stamp themselves into all positions. The edge bits (i₀, i₃) are erased. **Proven**: verified for all 64 hexagrams.

---

## 2. Functional Graph Topology

### The 64-node graph

Each hexagram has exactly one 互 image → 64 directed edges, each node out-degree 1. The graph decomposes into trees hanging off attractors.

### Attractors

| Attractor | Binary | Interface (b₂,b₃) | Type | KW# |
|-----------|--------|-------------------|------|-----|
| Kun 坤 | 000000 | (0,0) | Fixed point | 2 |
| Qian 乾 | 111111 | (1,1) | Fixed point | 1 |
| Ji Ji 既濟 | 010101 | (0,1) | 2-cycle member | 63 |
| Wei Ji 未濟 | 101010 | (1,0) | 2-cycle member | 64 |

The 4 attractors form a 2D linear subspace of F₂⁶ = im(M²) = span{(101010), (010101)}.

### Basin partition

| Interface (b₂,b₃) | Basin | Attractor | Count |
|--------------------|-------|-----------|-------|
| (0,0) | Kun | Fixed point: 000000 | 16 |
| (1,1) | Qian | Fixed point: 111111 | 16 |
| Mixed | Cycle | 2-cycle: 010101 ↔ 101010 | 32 |

Basin membership is a **linear functional**: b₂ ⊕ b₃ = 0 → fixed-point basin, b₂ ⊕ b₃ = 1 → cycle basin.

Basin is an exact invariant of 互 — **proven algebraically**, zero exceptions.

### Depth distribution

| Depth | Count | Description |
|-------|-------|-------------|
| 0 | 4 | Attractors themselves |
| 1 | 12 | Attractor inner bits, non-attractor outer bits |
| 2 | 48 | Feeder inner bits, any outer bits |

**Corrected** from previously stated {4, 24, 36}. The correction follows from the algebraic structure: depth-1 = 4 attractor inner values × 3 non-identity outer combos = 12; depth-2 = 12 feeder inner values × 4 outer combos = 48.

### Tree structure — perfectly balanced

Each basin has the identical internal ratio **1 : 3 : 12** (depth-0 : depth-1 : depth-2):

```
Kun basin (16 nodes):                    Qian basin (16 nodes):
        Kun(000000)                              Qian(111111)
       ╱     │     ╲                            ╱     │     ╲
    d1:a    d1:b    d1:c                     d1:a    d1:b    d1:c
   ╱╱╲╲   ╱╱╲╲   ╱╱╲╲                      ╱╱╲╲   ╱╱╲╲   ╱╱╲╲
   4×d2   4×d2   4×d2                       4×d2   4×d2   4×d2

Cycle basin (32 nodes):
     JiJi(010101) ←→ WeiJi(101010)
    ╱    │    ╲        ╱    │    ╲
  d1:a  d1:b  d1:c   d1:a  d1:b  d1:c
 ╱╱╲╲  ╱╱╲╲  ╱╱╲╲  ╱╱╲╲  ╱╱╲╲  ╱╱╲╲
 4×d2  4×d2  4×d2  4×d2  4×d2  4×d2
```

Every attractor has exactly 3 feeders in inner space. Every depth-1 node has exactly 4 depth-2 children (the outer-bit fiber). **Algebraically necessary** — combinatorial consequence of free-bit counting.

### In-degree

Binary: exactly **0 or 4**. The 16 nodes that are 互 outputs each receive exactly 4 hexagrams (the fiber). The other 48 are never targets (depth-2 leaves).

### Feeder geometry

Feeders are complement-symmetric across basins:

| Basin | Feeder inner values | XOR masks to attractor |
|-------|-------------------|----------------------|
| Kun | {1, 8, 9} = {0001, 1000, 1001} | {0001, 1000, 1001} |
| Qian | {6, 7, 14} = {0110, 0111, 1110} | {0001, 1000, 1001} |
| Cycle→5 | {2, 3, 11} = {0010, 0011, 1011} | {0111, 0110, 1110} |
| Cycle→10 | {4, 12, 13} = {0100, 1100, 1101} | {1110, 0110, 0111} |

Kun feeders ↔ Qian feeders under complement. Cycle feeders split into two complement-related halves: {2,3,11} ↔ {4,12,13}. **Algebraically necessary** — complement commutes with 互.

---

## 3. F₂ Spectral Analysis

### The matrix

```
M = ⎡0 1 0 0 0 0⎤     hugua(b₀,b₁,b₂,b₃,b₄,b₅) = (b₁,b₂,b₃,b₂,b₃,b₄)
    ⎢0 0 1 0 0 0⎥
    ⎢0 0 0 1 0 0⎥     Rows 2,4 identical; rows 3,5 identical
    ⎢0 0 1 0 0 0⎥
    ⎢0 0 0 1 0 0⎥
    ⎣0 0 0 0 1 0⎦
```

### Matrix powers

```
M² = all rows are either (0,0,1,0,0,0) or (0,0,0,1,0,0)
     M²(b) = (b₂, b₃, b₂, b₃, b₂, b₃)

M³(b) = (b₃, b₂, b₃, b₂, b₃, b₂)    ← interface bits swapped

M⁴ = M²                                ← proven, period 2 from step 2
```

### Rank sequence

| k | rank(Mᵏ) | dim ker(Mᵏ) | dim im(Mᵏ) | Distinct Mᵏ values |
|---|----------|-------------|-------------|---------------------|
| 0 | 6 | 0 | 6 | 64 |
| 1 | 4 | 2 | 4 | 16 |
| 2 | 2 | 4 | 2 | 4 |
| 3 | 2 | 4 | 2 | 4 |
| k≥2 | 2 | 4 | 2 | 4 |

### Kernel chain (what gets erased)

```
ker(M)  = span{e₀, e₅}               dim 2 — outer bits
ker(M²) = span{e₀, e₁, e₄, e₅}       dim 4 — outer + shell bits
ker(M²) = ker(M³) = ⋯                 stabilized
```

Nested onion: outer layer first, then shell layer. Each step erases a 2D subspace.

### Image chain (what survives)

```
im(M)  = span{e₁, e₂, e₃, e₄}  (with constraint b₁=b₃, b₂=b₄)     dim 4
im(M²) = span{(101010), (010101)}                                     dim 2
im(M²) = im(M³) = ⋯                                                   stabilized
```

im(M²) IS the attractor set — a 2D linear subspace.

### Eigenstructure over F₂

**Minimal polynomial**: x²(x+1)² = x⁴ + x² over F₂

- x² factor → 2 nilpotent steps to reach attractor space
- (x+1)² factor → period-2 oscillation at the core (recall: over F₂, x+1 = x-1)

**Jordan structure** (over F₂):
- Eigenvalue 0: two 2×2 Jordan blocks (dim 4)
- Eigenvalue 1: one 2×2 Jordan block (dim 2)
- Total: 2+2+2 = 6 ✓

**Fixed points**: ker(M+I) = span{(111111)} — dim 1
→ Fixed-point hexagrams: {Kun(0), Qian(63)}

**2-periodic points**: ker(M²+I) = span{(101010), (010101)} — dim 2
→ 2-periodic hexagrams: {Kun(0), JiJi(21), WeiJi(42), Qian(63)}
→ The 2-cycle {JiJi, WeiJi} ∈ ker(M²+I) \ ker(M+I)

### Eigenspace decomposition

**F₂⁶ = ker(M²) ⊕ ker(M²+I) = 4D transient ⊕ 2D attractor**

M² is the projection onto the attractor subspace: every hexagram decomposes as h = (h ⊕ M²h) + M²h, with the first term transient, the second the attractor component. **Verified** for all 64 hexagrams.

---

## 4. Information Cascade

### Bits lost per iteration

| Step | Effective bits | Distinct values | Bits lost | What's erased |
|------|---------------|-----------------|-----------|---------------|
| 0 | 6 | 64 | — | — |
| 1 | 4 | 16 | 2 | Outer layer (b₀, b₅) |
| 2 | 2 | 4 | 2 | Shell layer (b₁, b₄) |
| 3 | 2 | 4 | 0 | Nothing — oscillation |
| k≥2 | 2 | 4 | 0 | Stabilized |

Each step removes exactly 2 bits = one layer. The loss is uniform, not bursty. **Algebraically necessary** from the rank sequence.

### Bit survival analysis

```
Step 0: all 6 bits free — {b₀, b₁, b₂, b₃, b₄, b₅}
Step 1: output determined by (b₁, b₂, b₃, b₄) — 4 free bits
Step 2: output determined by (b₂, b₃) — 2 free bits
Step 3+: same 2 free bits, alternating between positions
```

The cascade traces the kernel chain: each step annihilates one more 2D subspace until only the interface remains.

### The attractor as information

After convergence, only 2 bits survive: (b₂, b₃). These 2 bits encode:
- Basin identity: b₂ ⊕ b₃ determines fixed vs cycle (1 bit)
- Basin polarity: the specific attractor within the basin type (1 bit)

Total information surviving 互 iteration: **2 bits out of 6** = 33%.

---

## 5. Five-Phase Along Convergence Direction

### Attractor elements

| Attractor | Lower nuclear | Upper nuclear | Elements |
|-----------|--------------|--------------|----------|
| Kun (000000) | Kun ☷ | Kun ☷ | Earth / Earth |
| Qian (111111) | Qian ☰ | Qian ☰ | Metal / Metal |
| JiJi (010101) | Li ☲ | Kan ☵ | Fire / Water |
| WeiJi (101010) | Kan ☵ | Li ☲ | Water / Fire |

Fixed-point attractors are element-pure. The 2-cycle attractors are element-opposed.

### Feeder → attractor five-phase relations

**Fixed-point basins**: upper nuclear is ALWAYS 比和 (same element) to attractor.

This is **forced by the overlap constraint**: upper nuclear = (b₂, b₃, b₄). Within a basin, (b₂, b₃) is fixed. For Kun: (0,0,b₄) produces only Kun ☷ or Gen ☶ — both Earth. For Qian: (1,1,b₄) produces only Dui ☱ or Qian ☰ — both Metal.

Lower nuclear varies by exactly 1 bit (b₁), toggling between 2 elements:
- Kun basin: (b₁,0,0) → Kun(Earth) or Zhen(Wood) → {比和, 克}
- Qian basin: (b₁,1,1) → Qian(Metal) or Xun(Wood) → {比和, 体克用}
- Never 生 in fixed-point basins

**Cycle basin**: all 5 relation types appear. Mixed interface breaks element-purity.

### Overall distribution (feeder → attractor, both trigrams, 24 directed pairs)

| Relation | Count | Percentage |
|----------|-------|-----------|
| 比和 | 8 | 33% |
| 克体 | 6 | 25% |
| 体克用 | 6 | 25% |
| 体生用 | 2 | 8% |
| 生体 | 2 | 8% |

### Verdict

Five-phase structure along convergence is **derivative of the bit algebra**. The 比和 prevalence in fixed-point basins is forced by the interface constraint, not by elemental affinity. The relation type is determined by the single free bit (b₁ or b₄) — toggling between exactly 2 possible elements. This is not a five-phase flow; it is a 1-bit switch with five-phase labels attached.

---

## 6. KW Walk Through Convergence Depth

### Depth profile

```
KW position:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
Depth:        0  0  2  2  2  2  2  2  2  2  2  2  2  2  2  2

KW position: 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32
Depth:        2  2  2  2  2  2  1  1  2  2  1  1  2  2  2  2

KW position: 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48
Depth:        2  2  2  2  1  1  1  1  2  2  1  1  2  2  2  2

KW position: 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64
Depth:        2  2  2  2  1  1  2  2  2  2  2  2  2  2  0  0
```

### Key observations (empirical, about KW ordering)

**Depth-0 positions**: {1, 2, 63, 64} — attractors bookend the sequence.

**Depth-1 positions**: {23, 24, 27, 28, 37, 38, 39, 40, 43, 44, 53, 54} — 12 hexagrams forming 6 complete KW pairs. Concentrated in the central region (positions 23–54). No depth-1 in positions 3–22 or 55–62.

**Depth-1 pairs**:

| KW pair | Hexagrams | Basin | Attractor |
|---------|-----------|-------|-----------|
| 23–24 | Bo / Fu | Kun | Kun |
| 27–28 | Yi / Da Guo | Kun / Qian | Kun / Qian |
| 37–38 | Jia Ren / Kui | Cycle | WeiJi / JiJi |
| 39–40 | Jian / Xie | Cycle | WeiJi / JiJi |
| 43–44 | Guai / Gou | Qian | Qian |
| 53–54 | Jian / Gui Mei | Cycle | WeiJi / JiJi |

**Pair depth invariance**: both members of every KW pair share the same depth. **Algebraically necessary** — 互 commutes with both reverse and complement, so the pair operation preserves the attractor-inner-bit property that defines depth.

**Basin × depth**: each basin has ratio 1:3:12. **Algebraically necessary** — self-similar structure.

### KW walk five-phase dynamics

No correlation between depth change and five-phase type at consecutive KW transitions. At Δd=0 transitions (51/63 steps): 克 41%, 比 30%, 生 28%. **Measured** — no structured pattern.

---

## 7. Trigram Fiber Structure and 京房八宮

### Overlap constraint

Nuclear lower = (b₁, b₂, b₃), nuclear upper = (b₂, b₃, b₄). They share 2 of 3 bits (the interface). Consequences:

- Only **16 of 64** possible trigram pairs are reachable as nuclear pairs
- Given nuclear lower, only **2** upper partners are possible (b₄ = 0 or 1)
- The 16 reachable pairs form **four 2×2 blocks** indexed by interface (b₂, b₃)

### Fiber structure

Each of 16 nuclear trigram-pair outputs receives exactly 4 hexagrams, parameterized by outer bits (b₀, b₅). The 4-to-1 fiber IS the kernel of M. **Algebraically necessary**.

### 京房八宮

The 京房 system groups 64 hexagrams into 8 palaces of 8, each rooted at a doubled hexagram. The generation algorithm from root TT:

```
1. 本宮: root TT
2–6. Cumulatively flip b₀, b₁, b₂, b₃, b₄ (lines 1–5, bottom to top)
7. 游魂: un-flip b₃ (line 4 reverts)
8. 归魂: un-flip b₀, b₁, b₂ (lower trigram reverts to palace T)
```

### Test of S5: do palaces = fibers?

**No.** Each palace spans exactly **7 of 16 inner values** (not 2 or 4).

All 8 palaces use the identical inner XOR mask set from their root: **{0000, 0001, 0011, 0111, 1000, 1011, 1111}**. The palace algorithm is a rigid traversal pattern — same shape from any starting point.

Every palace touches all 3 basins. 京房 organizes by trigram genealogy (surface structure), 互 organizes by nuclear convergence (depth structure). These are **orthogonal decompositions** of the 64-element set.

**S5: Refuted.** The orthogonality is algebraically necessary once the palace XOR mask set is identified — it spans 7 inner values, which cannot partition into groups of 4 (the fiber size).

---

## 8. Comparison Across Orderings

### What's empirical vs necessary

Almost everything in this investigation is **algebraically necessary** once the map is defined. The single genuinely empirical finding is:

**KW attractor framing**: the King Wen sequence places the 4 attractors at positions {1, 2, 63, 64}. Probability under random placement: **p ≈ 5×10⁻⁷**.

This is a fact about one specific historical ordering, not a consequence of the algebra. No other traditional ordering was tested (Fu Xi, Mawangdui, 邵雍); such comparison was assessed as low marginal value since the framing probability is already quantified.

### The two fixed points open; the 2-cycle closes

- KW #1–2 (Qian, Kun) = ker(M+I), the fixed-point eigenspace
- KW #63–64 (JiJi, WeiJi) = ker(M²+I) \ ker(M+I), the pure 2-cycle

The sequence opens with resolution (convergence to rest) and closes with irreducible oscillation (permanent alternation). **From rest to motion.**

---

## 9. Speculations S1–S5: Status

| # | Speculation | Verdict | Key evidence | Status type |
|---|-----------|---------|--------------|-------------|
| S1 | 互 iteration is the 生 cycle projected onto basins | **Refuted** | Five-phase is mixed along convergence; upper 比和 is forced by overlap constraint, not elemental affinity | Algebraically necessary (given element assignment) |
| S2 | 6×6 matrix has rank 4, kernel = outer bits | **Confirmed with refinement** | Rank 4 at step 1; inner map has effective rank 2 at step 2; kernel chain traces the onion | Proven (algebraically necessary) |
| S3 | Convergence depth correlates with hexagram complexity | **Weakened** | 75% at depth-2; uniform 1:3:12 ratio across all basins; not discriminating | Algebraically necessary (depth distribution) |
| S4 | Feeder trees have five-phase meaning | **Derivative** | 比和 dominance in fixed basins is forced by interface bits; the single free bit toggles between exactly 2 elements | Algebraically necessary (given element assignment) |
| S5 | 京房八宮 is the fiber structure of 互 | **Refuted** | Palaces span 7/16 inner values; XOR mask set is universal across palaces; orthogonal to convergence | Algebraically necessary (given palace algorithm) |

---

## 10. Key Insight and Open Questions

### The key insight

**互 defines an independent structural axis of the hexagram system, orthogonal to the axes used by the major traditional classification schemes.**

The traditional overlays (五行 element flow, 京房 palace genealogy, KW sequential ordering) organize hexagrams by surface trigram relationships. 互 organizes them by depth — what survives when surface is stripped. These are genuinely different decompositions of the same 64-element set.

The onion vocabulary (outer / shell / interface) is the insight, not merely the linear algebra underneath it. The bit positions are not arbitrary — they are defined by the trigram overlap geometry. The outer bits are surface presentation. The shell bits are the nuclear trigrams' degrees of freedom. The interface bits are where above and below meet. Reading the algebra's partitioning as an anatomy gives a structural vocabulary for talking about what the hexagram's layers *do*.

What the perspective does NOT do: reveal anything about meaning, interpretation, or divination practice. It characterizes one structural axis of a multi-axis system.

### Open questions

**1. Are there other independent axes?** The hexagram system admits other operations (错 inversion, 综 reversal, 变 line-change). Each defines its own graph on the 64. What is the full group of structural symmetries, and how many independent axes exist? The spaceprobe investigation characterized the S₄ action and Z₂³ kernel; this investigation adds the 互 convergence axis. What else?

**2. What is the design grammar of KW?** The attractor framing is almost certainly intentional (p ≈ 5×10⁻⁷). If the sequence designer placed the eigenspace decomposition at the boundaries, what other structural properties were encoded? The interior (positions 3–62) remains uncharacterized against 互 depth.

**3. Does the interface have interpretive weight?** The two interface bits (b₂, b₃) = lines 3 and 4 determine the attractor. In traditional reading, these are classically the transition point between inner and outer, lower and upper, the liminal position. Is there a historical interpretive tradition that weights these lines differently? Does it align with the algebraic finding?

**4. What is the joint structure of 京房 × 互?** They are orthogonal as classifications. But orthogonality is itself a structural relationship. The 8 palaces × 3 basins gives a 24-cell grid. Is the population of this grid uniform or structured?

---

## Scripts

| Script | Content |
|--------|---------|
| `01_functional_graph.py` | Full 64-node directed graph, tree structure, in-degree, fiber verification |
| `02_information_cascade.py` | F₂ matrix M, powers, rank/kernel/image chains, minimal polynomial, eigenspaces |
| `03_inner_orbits.py` | 16-node inner space, convergence trees, feeder geometry, five-phase edges |
| `04_trigram_projection.py` | Trigram-pair mapping, overlap constraint, reachability, 京房 palace test |
| `05_kw_depth_walk.py` | Depth profile along KW, clustering, basin×depth, pair invariance |
| `07_convergence_fivephase.py` | Attractor elements, feeder→attractor relations, 生 cycle geometry, KW dynamics |

Visualizations: `01_functional_graph.png/svg`, `03_inner_orbits.png/svg`, `04_trigram_projection.png/svg`, `05_kw_depth_walk.png/svg`
