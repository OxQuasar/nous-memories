# 16. The Algebra and Geometry of Bridges

> A deep structural analysis of the 31 inter-pair transitions in the King Wen sequence. Extends the synthesis in `14-synthesis.md` and the initial bridge survey in `15-bridges.md`. Based on 6 investigation threads: bridge basis (T1), projection theorem (T2), compound transitions (T3), constraint analysis (T4), orbit graph topology (T5/5b), and minimal bridges with quantization (T6/6b).

---

## 1. The Fundamental Decomposition

**Theorem.** The 6-bit mask space decomposes as a direct product:

```
Z₂⁶ ≅ Z₂³ (orbit change) × Z₂³ (generator dressing)
```

via the short exact sequence:

```
0 → ⟨O,M,I⟩ → Z₂⁶ →P Z₂³ → 0
```

The projection P extracts the antisymmetric part of a mask:

```
P(m₁,m₂,m₃,m₄,m₅,m₆) = (m₁⊕m₆, m₂⊕m₅, m₃⊕m₄)
```

**This is a theorem, not an empirical finding.** It holds for all 4032 possible hexagram-to-hexagram transitions. The hexagram drops out of the formula — the orbit change depends only on the mask's asymmetry across mirror pairs.

The kernel of P is exactly the generator group ⟨O, M, I⟩ — the 8 palindromic masks. **The generators are the symmetry-preserving transformations.** This is why standard pairs (which always use generator masks) always stay within an orbit.

Every mask decomposes uniquely:

```
m = orbit_Δ ⊕ kernel_dressing
```

where orbit_Δ lives in the first factor (antisymmetric component) and kernel_dressing lives in ker(P) = ⟨O, M, I⟩. The two components are independent. Every bridge does two things simultaneously: changes the orbit (forced by the walk) and applies a generator transformation within-orbit (the free choice).

The rows of the projection matrix are the three generators themselves — P tests "how much does this mask break each mirror symmetry?"

---

## 2. The Eulerian Path

**The King Wen bridge walk is an Eulerian path from Qian(000) to Tai(111).**

The orbit transition multigraph has 8 nodes and 31 edges (counting multiplicities: Zhun→Xu ×3, Shi→XChu ×2, XChu→Tai ×2, Bo→WWang ×2, plus 22 single-use edges and 2 self-loops). Its degree sequence:

| Orbit | Out | In | Balance |
|:---:|:---:|:---:|:---:|
| Qian (000) | 4 | 3 | **+1** |
| Tai (111) | 3 | 4 | **−1** |
| All others | 4 | 4 | 0 |

Exactly one source (Qian, all-symmetric) and one sink (Tai, all-antisymmetric). The graph is strongly connected with diameter 3. An Eulerian path exists from Qian to Tai, and the King Wen walk IS one — edge-by-edge verified. Every orbit-to-orbit transition is used exactly as many times as it occurs. The walk completely traverses its own transition graph.

**The opening is not forced.** From Qian, 4 first moves are available (self-loop, Zhun, Shi, Tai). All 4 lead to valid Eulerian paths ending at Tai. At least 100 distinct Eulerian paths exist through the multigraph. Among the enumerated paths, the King Wen walk has the longest Hamiltonian prefix — visiting 6 new orbits (Qian→Zhun→Xu→Shi→XChu→Tai) before any revisit. (This is observed, not proven extremal across all possible Eulerian paths.)

**Structural features of the specific KW path:**
- Every orbit visited exactly 4 times (perfectly uniform)
- Only 2 bidirectional edges: XChu↔Zhun and Bo↔Xu
- Self-loops at Qian (steps 13→14, the canon boundary) and WWang (steps 18→19)
- Opening 13-step circuit (steps 0–13) visits 6 distinct orbits before returning to origin
- Late 6-step cycle (B22–B27: XChu→Zhun→Xu→Tai→Bo→WWang) sweeps 6 orbits in one pass

---

## 3. The Quantization Formula

**Theorem.** For any mask m = (m₁,m₂,m₃,m₄,m₅,m₆):

```
H(mask) = w(sig_change) + 2S
```

where:
- w(sig_change) = weight of P(m) = minimum Hamming distance to target orbit
- S = (m₁∧m₆) + (m₂∧m₅) + (m₃∧m₄) = number of mirror pairs where BOTH lines flip
- Excess = 2S, always even, always in {0, 2, 4, 6}

**Proof.** Over integers: m_i + m_j = (m_i ⊕ m_j) + 2(m_i ∧ m_j). Sum over all three mirror pairs: H = Σ(m_i + m_j) = w(sig_change) + 2S. QED.

**Constraint:** S ≤ 3 − w(sig_change). A pair contributes to S only if both lines flip, which means that pair does NOT change the signature. So S counts a subset of the non-changing pairs.

This gives the full structure of allowed Hamming distances:

| w (orbit weight) | Allowed S | Allowed H | KW actual |
|:---:|:---:|:---:|:---:|
| 0 (self-transition) | 0,1,2,3 | 0,2,4,6 | 2, 6 |
| 1 (single-component) | 0,1,2 | 1,3,5 | 1, 3 |
| 2 (double-component) | 0,1 | 2,4 | 2, 4 |
| 3 (omi) | 0 only | 3 only | 3 |

**The weight-5 gap is partially structural, partially empirical.** For w=3 (omi changes), S=0 is forced, so H=3 always — weight 5 is structurally impossible here. For w=1, S=2 would give H=5 and is algebraically allowed, but the sequence never selects it. The S=2 avoidance is an empirical constraint, equivalent to the absence of weight-5 bridges.

---

## 4. The Constraint Landscape

### The 50/50 Split

| S value | Excess | Count | |
|:---:|:---:|:---:|:---|
| 0 | 0 | 15 | Optimal — pure asymmetric flip |
| 1 | +2 | 15 | One hidden mirror-pair flip |
| 2 | +4 | 0 | Never occurs |
| 3 | +6 | 1 | B19: all three mirror pairs both-flip |

The near-perfect 50/50 split between optimal and +2 bridges parallels other balances in the system (32 yang per line, 4 visits per orbit, mean weight 3.0).

### Freedom Narrows

Available valid targets at each bridge (requiring both target AND its pair partner unused):

- **B1–B5:** 8 valid targets (all fresh orbits)
- **B6–B9:** 6 valid targets
- **B10–B19:** 4 valid targets
- **B20–B31:** 2 valid targets

By the final 12 bridges, every choice is binary. The generator dressing "choices" in the second half are not really choices — they're forced by the Hamiltonian constraint (every hexagram visited exactly once). **The creative decisions happen in the first ~5 bridges**, where freedom is maximal.

### Generator Dressing Distribution

| Generator | Count | Upper Canon (B1–14) | Lower Canon (B15–31) |
|:---:|:---:|:---:|:---:|
| O | 6 | 2 | 4 |
| id | 4 | 3 | 1 |
| OMI | 4 | 3 | 1 |
| OM | 4 | 1 | 3 |
| OI | 4 | 1 | 3 |
| MI | 4 | 1 | 3 |
| M | 3 | 2 | 1 |
| I | 2 | 1 | 1 |

Nearly uniform overall (expected 31/8 ≈ 3.9). But the upper canon favors extremes (id, OMI — no dressing or full dressing), while the lower canon favors intermediates (O, OM, OI, MI). The sequence starts with simpler generator choices and progressively uses more varied ones.

### Kernel and Optimality

- kernel=id → always optimal (4/4)
- kernel=M → always optimal (3/3)
- kernel=OI → never optimal (0/4)
- Other kernels: mixed rates

---

## 5. What the Compound View Shows

Wrapping bridges in their pair context — the 4-hexagram window `h₁ →[pair_k]→ h₂ →[bridge]→ h₃ →[pair_{k+1}]→ h₄` — produces a compound mask `h₁ ⊕ h₄` that decomposes as:

```
compound = orbit_Δ₆ ⊕ (P_k ⊕ G ⊕ P')₆
```

where P_k and P' are the pair types (orbit-determined) and G is the bridge's kernel dressing.

**The pair envelope does not simplify bridge structure.** Compound masks have rank 6, 24 unique values, and only 2/31 generator-expressible — no improvement over raw bridges.

But the generator chain `P_k ⊕ G ⊕ P'` operates entirely within Z₂³ and reveals:

- **4/31 windows achieve total generator cancellation** (W2, W11, W17, W25) — the compound is a pure orbit change, bits only in positions 1–3
- **6/31 have bridge kernel = starting pair type** — the bridge "continues" the starting orbit's generator
- **Consecutive window XORs span the full generator space** — the gen compounds are not repetitive

The generator chain creates coupling between consecutive bridges: each bridge's dressing constrains the starting hexagram of the next pair, which propagates forward through the sequence.

---

## 6. Minimal Bridges and Structural Theorems

### Single-Bit Bridges Must Cross Orbits

**Theorem.** Flipping one line without its mirror partner always inverts one signature component. Single-bit bridges cannot be self-transitions. Corollary: self-transitions require at least Hamming 2 (mirror pair flip).

The two single-bit bridges (B26 and B30) both flip upper-half lines, both change yin→yang, both preserve the lower trigram, and both arrive at the Wind trigram. Both are late in the sequence and Hamming-optimal.

### The Parity Theorem

**Orbit change parity = Hamming distance parity (mod 2).** Each bit flip either changes one signature component (odd contribution) or pairs with its mirror (even contribution).

### B19: The Anti-Optimal Reset

B19 (Kui→Jian, hex 38→39) maps to the bit-complement — the maximally distant hexagram in its own orbit. Mask = OMI, H=6, excess = +6. It could have reached any of 7 alternatives at lower Hamming cost. This is the only bridge that applies the complete generator as pure dressing.

B14 (the other self-transition, at the canon boundary) uses kernel=I with H=2 — minimum non-trivial dressing. Together the two self-transitions span the extremes of within-orbit movement. They are the "pause" points in the Eulerian path — moments where the walk dwells in an orbit before resuming.

### The Min-Max Juxtaposition

Both single-bit bridges (H=1) are immediately followed by OMI-complement standard pairs (H=6). Minimum bridge change → maximum pair change. The most delicate inter-pair transitions lead into the most violent intra-pair transformations.

---

## 7. Open Questions

### What selects the early generator dressings?

In bridges B1–B5, there are 8 valid targets per bridge — 4 generator dressings available at each. That gives 4⁵ = 1024 possible openings before any constraint bites. The chain constraint means each early choice restricts later choices. **The critical empirical question: how many complete valid sequences exist** (satisfying Hamiltonian + Eulerian + pairing constraints simultaneously)? If the answer is very few — single digits — then the early choices are effectively forced by the requirement that the entire sequence close, and the "selection principle" question dissolves. If many, there is a genuine further constraint we haven't identified.

### Is the 50/50 S-split a balancing constraint?

The 15:15:1 distribution (optimal : +2 : +6) is suspiciously balanced. Does it follow from more fundamental constraints, or is it an independent design parameter? It parallels the system's other exact balances but has no proven derivation.

### Hamiltonian vs. Eulerian: The Channel Separation

The sequence is simultaneously:
- A **Hamiltonian path** through the 64-vertex hypercube (hexagram level)
- An **Eulerian path** through the 8-node orbit multigraph (orbit level)

These are different combinatorial constraints operating at different scales on the same sequence. They are not independent, but neither does one imply the other. The Hamiltonian path determines the orbit visit counts (4 each), but a Hamiltonian path with uniform orbit visits could still traverse the orbit graph non-Eulerianly — repeating some edges, missing others. The Eulerian property is an additional constraint on *which* orbit transitions are used, not just which orbits are visited.

**The decomposition Z₂⁶ ≅ Z₂³ × Z₂³ separates their channels cleanly.** The Eulerian path lives in im(P) — the orbit-change factor. The Hamiltonian path lives in ker(P) — the generator-dressing factor. The two completeness constraints operate on the two independent components of every bridge mask. This is the cleanest statement of the dual structure: the projection P separates the sequence into an orbit-level walk (Eulerian, visible to meta-hexagrams) and a hexagram-level selection (Hamiltonian, invisible at meta level).

### Bridge structure and meta-hexagram self-similarity

From `13-meta.md`: stacking adjacent pair signatures produces meta-hexagrams with meta-signature `sig ⊕ reverse(sig')`, where O and I swap roles. The bridge's orbit change Δsig feeds directly into this construction — each bridge determines one meta-hexagram. The Eulerian path through orbit space therefore generates a specific walk through meta-hexagram space. The kernel dressing is invisible to the orbit projection and therefore invisible to the meta-hexagram construction. The meta-hexagrams see only the antisymmetric part of each bridge. The symmetric (generator) part is the hidden variable — present at the hexagram level, absent at the meta level.

### Predictions for applications

If markets or other dynamical systems follow this structure:
- **Regime transitions (bridges) carry two independent signals:** which regime you're entering (orbit change) and how you enter it (generator dressing). These can be measured separately.
- **Freedom is front-loaded.** Early regime transitions have many possible targets; late ones are forced. A system that has been running long enough has its transitions largely determined by its history.
- **Non-optimal transitions overshoot by a quantized amount.** The +2 excess means: when a regime change is "rougher than necessary," it's rougher by exactly one hidden mirror-pair flip. The roughness is never intermediate — it's 0 or discrete.
- **Self-transitions are structural boundaries,** not static rest. Both self-transitions in the KW sequence carry non-trivial generator dressing — they are internal reorganizations at points where the orbit walk pauses. In application: regime persistence signals restructuring, not inactivity.
- **The system traverses its own transition graph completely.** Every possible regime-to-regime connection is used. No transition is wasted or repeated beyond its multiplicity. The dynamics are maximally efficient at the orbit level.

---

## Summary

The 31 King Wen bridges decompose into orbit changes (forced by the walk) and generator dressings (the free choice, progressively constrained by the Hamiltonian path). The orbit walk is an Eulerian path from all-symmetric to all-antisymmetric. The Hamming excess is exactly quantized at H = w + 2S, splitting 50/50 between optimal and +2. The pair envelope doesn't simplify bridge structure. Freedom is front-loaded; the second half of the sequence is largely determined by the first. The weight-5 gap is partially structural (omi forces S=0) and partially empirical (S=2 avoidance). The two self-transitions span the extremes of within-orbit movement and mark structural boundaries. The single-bit bridges must cross orbits and are immediately followed by maximum-change pairs.

The deepest finding: **the sequence is simultaneously a Hamiltonian path through the hexagram hypercube and an Eulerian path through the orbit multigraph** — two different completeness constraints operating on the two independent factors of the decomposition Z₂⁶ ≅ Z₂³ × Z₂³. The projection P cleanly separates them: Eulerian in the image, Hamiltonian in the kernel.
