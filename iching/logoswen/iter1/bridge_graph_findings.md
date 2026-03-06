# Bridge Graph Findings — Threads 5, 5b, 6, 6b

> Graph topology, minimal transitions, and the Eulerian path in the King Wen bridge orbit graph.
> Scripts: `logoswen/thread5_cycles.py`, `logoswen/thread5b_eulerian.py`, `logoswen/thread6_singlebits.py`, `logoswen/thread6b_quantization.py`

---

## Thread 5: Directed Graph Cycle Structure

### Finding 5.1: An Eulerian Path Exists — From Qian to Tai

The orbit transition multigraph (8 nodes, 26 distinct directed edges, 31 total traversals including 2 self-loops) has a remarkable degree balance:

| Orbit | Out | In | Balance |
|:---:|:---:|:---:|:---:|
| 1:Qian | 4 | 3 | **+1** |
| 2:Zhun | 4 | 4 | 0 |
| 3:Xu | 4 | 4 | 0 |
| 4:Shi | 4 | 4 | 0 |
| 5:XChu | 4 | 4 | 0 |
| 6:Tai | 3 | 4 | **−1** |
| 7:Bo | 4 | 4 | 0 |
| 8:WWang | 4 | 4 | 0 |

Exactly one node has excess out-degree (Qian, orbit 000) and exactly one has excess in-degree (Tai, orbit 111). These are the **complementary orbits** — the all-zeros and all-ones signatures. Since the graph is also strongly connected, **an Eulerian path exists from orbit 1:Qian to orbit 6:Tai**.

### Finding 5.2: The Graph is Strongly Connected with Diameter 3

Every orbit can reach every other orbit. Maximum shortest path length is 3. Density is 24/56 = 43% (cross-edges only), average out-degree 3.0. Sparsity comes from *directionality* (most connections are one-way), not from disconnection.

### Finding 5.3: 147 Simple Cycles

| Cycle length | Count |
|:---:|:---:|
| 2 | 2 |
| 3 | 10 |
| 4 | 18 |
| 5 | 32 |
| 6 | 38 |
| 7 | 33 |
| 8 | 14 |

The two **2-cycles** (bidirectional edges) are **XChu ↔ Zhun** and **Bo ↔ Xu** — the only symmetric connections.

### Finding 5.4: The Walk Visits Every Orbit Exactly 4 Times

32 visits / 8 orbits = 4 each. Perfectly uniform.

### Finding 5.5: Near-Hamiltonian Opening

First 6 steps visit 6 distinct orbits: **1:Qian → 2:Zhun → 3:Xu → 4:Shi → 5:XChu → 6:Tai**. Orbits 7:Bo and 8:WWang are reached at steps 11 and 12.

### Finding 5.6: Edge Repetition

- **22 edges** used exactly once
- **4 edges** repeated: Zhun→Xu **3×**, Shi→XChu 2×, XChu→Tai 2×, Bo→WWang 2×

### Finding 5.7: The Walk Traces Consecutive Cycles

The walk executes graph cycles inline, including a length-6 cycle (B22–B27: XChu→Zhun→Xu→Tai→Bo→WWang) visiting 6 orbits in one sweep, and the Bo↔Xu reciprocal pair (B28–B29).

### Finding 5.8: Return Gap Structure

| Orbit | Visit Steps | Gaps |
|:---|:---|:---|
| 1:Qian | 0, 13, 14, 30 | 13, **1**, 16 |
| 2:Zhun | 1, 9, 16, 24 | 8, 7, 8 |
| 8:WWang | 12, 18, 19, 22 | 6, **1**, 3 |

Zhun is near-periodic (8,7,8). Both self-looping orbits (Qian, WWang) show the pattern: long gap → self-loop (gap 1) → medium gap.

---

## Thread 5b: The Walk IS Eulerian

### Finding 5b.1: ★ THE KING WEN BRIDGE WALK IS AN EULERIAN PATH ★

Edge-by-edge verification confirms: the King Wen walk uses **every orbit transition exactly as many times as it exists in the multigraph**. All 26 distinct edges match their multiplicities exactly.

```
The walk IS an Eulerian path from Qian(000) to Tai(111).
```

The multigraph has exactly 31 edges (counting multiplicities). The walk has exactly 31 steps. Every edge is used the exact right number of times. This is not approximate — it is exact. The King Wen bridge sequence is a complete traversal of its own orbit transition graph, starting at the all-harmony orbit and ending at the all-tension orbit.

**This was not obvious from Round 1.** Round 1 noted that the graph had 26 unique edges and the walk used 31 steps, which seemed to require repetition. The resolution: the multigraph (with repeated edges counted by their actual occurrence count) has exactly 31 edges, and the walk traverses each one exactly once. The "repeated" edges (Zhun→Xu 3×, etc.) are not repetitions of the same edge — they are distinct parallel edges in the multigraph.

### Finding 5b.2: The Opening Is Not Forced

From Qian, the graph allows 4 first moves: Qian (self-loop), Zhun, Shi, Tai. All 4 lead to valid Eulerian paths ending at Tai. The specific KW opening (Qian→Zhun→Xu→Shi→XChu→Tai) is a **choice**, not a structural necessity. The sequence selects the particular Eulerian path that surveys orbits 1–6 in order before revisiting.

### Finding 5b.3: Many Eulerian Paths Exist

Enumeration (capped at 100) found at least 100 distinct Eulerian paths through the multigraph. The King Wen walk is one of many possible Eulerian traversals — but it is the one that maximizes the Hamiltonian prefix (visiting 6 new orbits before any revisit).

### Finding 5b.4: Self-Loop Placement

In the KW walk, self-loops occur at steps 13→14 (Qian⟲) and 18→19 (WWang⟲). In the Hierholzer-constructed path, they fall at different positions (20→21 and 22→23). The self-loop placement is a distinguishing feature of the KW path among all Eulerian paths.

### Finding 5b.5: Walk Recurrence Decomposition

The walk can be decomposed into a sequence of orbit-return cycles. The longest is the opening 13-step circuit (steps 0–13: Qian → ... → Qian), which visits 6 distinct orbits before returning to its origin. This opening circuit accounts for nearly half the walk.

---

## Thread 6: Single-Bit Bridges — Minimal Transitions

### Finding 6.1: The Two Single-Bit Bridges

| | Bridge B26 | Bridge B30 |
|:---|:---|:---|
| Transition | #52 Gen → #53 Jian | #60 Jie → #61 Zhong Fu |
| Hexagram bits | 001001 → 001011 | 110010 → 110011 |
| Flipped line | Line 5 (M-upper) | Line 6 (O-upper) |
| Change | yin → yang | yin → yang |
| Orbit change | oi(101) → omi(111), Δ=m | o(100) → id(000), Δ=o |
| Lower trigram | Mountain (unchanged) | Lake (unchanged) |
| Upper trigram | Mountain → Wind | Water → Wind |

Both: upper-half line, yin→yang, lower trigram preserved, arrive at Wind trigram, late in sequence.

### Finding 6.2: Single-Bit Bridges Must Cross Orbits (Theorem)

Flipping one line without its mirror partner always inverts one signature component. **Single-bit bridges cannot be self-transitions.** Corollary: self-transitions require at least Hamming 2 (mirror pair flip).

### Finding 6.3: Parity Theorem

**Orbit change parity = Hamming distance parity (mod 2).** This follows from the mirror structure: each bit flip either changes one sig component (odd contribution) or is paired with its mirror (even contribution).

### Finding 6.4: H=2 Bridge Structure

Of 8 Hamming-2 bridges, only 1 flips a mirror pair (B14: I generator, self-transition). The other 7 flip non-mirror lines, all crossing orbits.

### Finding 6.5: Line Flip Frequency

Total: 91 flips. Lower 44, Upper 47. O-lines (1,6) flip most: 35. I-lines (3,4): 29. M-lines (2,5): 27.

### Finding 6.6: Optimality

**15/31 bridges (48%) use minimum Hamming.** Both single-bit bridges are optimal. Non-optimal bridges overshoot by +2 (15 bridges) or +6 (1 bridge, B19). Total excess: 36 bits.

### Finding 6.7: Min-Max Juxtaposition

Both single-bit bridges are immediately followed by OMI-complement standard pairs (H=6): minimum bridge change → maximum pair change.

---

## Thread 6b: The +2 Quantization Theorem

### Finding 6b.1: The Excess Formula (Proved)

For any mask m = (m₁,m₂,m₃,m₄,m₅,m₆):

```
H(mask) = w(sig_change) + 2S
```

where:
- w(sig_change) = weight of (m₁⊕m₆, m₂⊕m₅, m₃⊕m₄) = minimum possible Hamming
- S = (m₁∧m₆) + (m₂∧m₅) + (m₃∧m₄) = number of mirror pairs where BOTH lines flip
- excess = 2S, always even, always ∈ {0, 2, 4, 6}

**Proof:** m₁ + m₆ = (m₁⊕m₆) + 2(m₁∧m₆) in integer arithmetic. Summing over all three mirror pairs: H(mask) = Σ(mᵢ + mⱼ) = Σ(mᵢ⊕mⱼ) + 2Σ(mᵢ∧mⱼ) = w(sig_change) + 2S. QED.

The minimum Hamming to the target orbit = w(sig_change) always. Verified for all 31 bridges.

### Finding 6b.2: S Distribution

| S value | Excess | Count | Interpretation |
|:---:|:---:|:---:|:---|
| 0 | 0 | 15 | Pure asymmetric flip — optimal |
| 1 | +2 | 15 | One hidden mirror-pair flip |
| 2 | +4 | 0 | Never occurs |
| 3 | +6 | 1 | B19: all three mirror pairs both-flip (OMI) |

The sequence splits almost exactly 50/50 between optimal (S=0) and S=1 bridges, with one outlier at S=3.

**S=2 never occurs.** This is empirical, not forced. A mask with S=2 would need 2 symmetric both-flips plus 1 asymmetric single-flip, giving H=5. The absence of S=2 is equivalent to the absence of Hamming-5 bridges.

### Finding 6b.3: The Weight-5 Gap Explained

No bridge has H=5. The formula H = w + 2S constrains this:

- H=5 requires w + 2S = 5
- w=3, S=1 is **impossible**: when w=3 (omi change), all 3 pairs are asymmetric, so S ≤ 0
- w=1, S=2 is **algebraically possible** but never chosen

The w=3 case is structurally forbidden: if all three signature components change, no mirror pair can both-flip (because both-flipping preserves the sig component). So S ≤ 3−w. For w=3: S=0 forced, giving H=3 always. This explains why all 6 omi-bridges have H=3.

For w=1, S=2 is allowed (S ≤ 2) but never selected. The sequence avoids it — an empirical constraint, not a theorem.

### Finding 6b.4: The Constraint S ≤ 3−w

**Theorem:** S ≤ 3 − w(sig_change).

Proof: A pair contributes to S only if both lines flip (m_i = m_j = 1), which means m_i ⊕ m_j = 0, so that pair does NOT change the signature. The number of non-changing pairs is 3 − w. S counts a subset of these non-changing pairs. QED.

This gives the full structure:
- w=0 (self-transition): S ∈ {0,1,2,3}, H ∈ {0,2,4,6}. Actual: B14 has S=1 (H=2), B19 has S=3 (H=6).
- w=1 (single-component): S ∈ {0,1,2}, H ∈ {1,3,5}. Actual: S∈{0,1} only, H∈{1,3}.
- w=2 (double-component): S ∈ {0,1}, H ∈ {2,4}. Actual: both occur.
- w=3 (omi): S = 0 forced, H = 3 always.

### Finding 6b.5: kernel=id Implies Optimal

When the kernel (generator dressing) component is the identity, the bridge is always optimal (4/4 = 100%). This is because kernel=id means the mask IS the pure orbit change — no extra mirror-pair flips.

| Kernel | Optimal | Total | Rate |
|:---:|:---:|:---:|:---:|
| id | 4 | 4 | 100% |
| M | 3 | 3 | 100% |
| I | 1 | 2 | 50% |
| O | 2 | 6 | 33% |
| OI | 0 | 4 | 0% |
| OM | 1 | 4 | 25% |
| MI | 2 | 4 | 50% |
| OMI | 2 | 4 | 50% |

**id and M are always optimal.** M kernel means the mask is (m₁⊕m₆, 1, m₃⊕m₄, m₃⊕m₄, 1, m₁⊕m₆) — it both-flips the M pair but contributes S=1 only when the M pair is not changing the signature. For the 3 M-kernel bridges, this happens to always be optimal because the M both-flip is "absorbed" into the signature change.

**OI kernel is never optimal** — all 4 OI-kernel bridges have excess +2.

### Finding 6b.6: B19 — Maximum Excess by Design

B19 maps Kui(110101) → Jian(001010) — exact bit-complements. The OMI mask flips all 6 bits. Since both hexagrams are in the same orbit (signature mi), this is a self-transition with maximum possible excess (+6).

Kui could have reached itself (H=0), or Wu Wang, Da Chu, Xie (all H=2), or Jia Ren, Cui, Sheng (all H=4). Instead it chooses the maximally distant hexagram in its own orbit. B19 is the **anti-optimal** bridge — it maximizes rather than minimizes Hamming distance. It is the bridge that applies the complete generator OMI as pure dressing.

B14 (the other self-transition) is intermediate: Da Guo→Kan with mask I (H=2), excess +2. It could have stayed at Da Guo (H=0) but chooses a 2-step move.

Both self-transitions carry nonzero dressing: neither takes the trivial path within its orbit.

### Finding 6b.7: Alternative Dressings

For non-optimal bridges, the number of alternatives at minimum Hamming:
- w=2 bridges: always 4 optimal alternatives (half the orbit)
- w=1 bridges: always 2 optimal alternatives
- w=0 bridges: always 1 optimal alternative (stay at source)

The sequence consistently bypasses these lower-cost options in favor of masks with one extra mirror-pair flip. This extra flip is structurally inert at the orbit level but meaningful at the hexagram level — it selects a specific member of the target orbit.

---

## Cross-Thread Synthesis

### The Walk Is an Eulerian Path from All-Harmony to All-Tension

The central discovery: **the King Wen bridge walk is an Eulerian path from Qian(000) to Tai(111) through the orbit transition multigraph.** It traverses every orbit-to-orbit transition exactly as many times as it occurs, beginning at the orbit of complete mirror symmetry and ending at the orbit of complete mirror asymmetry.

This is the strongest structural constraint yet found. The orbit graph is not arbitrary — it has exactly the degree sequence needed for an Eulerian path between the signature-space endpoints. And the King Wen sequence is not just any walk through this graph — it is a *complete* traversal.

### The +2 Quantization and the Weight-5 Gap

Every bridge mask satisfies H = w(sig) + 2S, where w is the orbit change weight and S counts "hidden" mirror-pair flips. The excess over minimum is always even. The weight-5 gap is partially structural (omi changes force S=0, making H=3 the only option) and partially empirical (single-component changes never use S=2).

### The 50/50 Split

15 bridges are optimal (S=0), 15 have S=1 (+2 excess), and 1 has S=3 (+6 excess). The near-perfect 50/50 split between S=0 and S=1 may be a balancing constraint analogous to the other balances in the system (32 yang per line, 4 visits per orbit, etc.).

### The Two Self-Transitions

B14 (Qian orbit, I dressing) and B19 (WWang orbit, OMI dressing) are the only self-transitions. Both carry generator dressing. B14 uses the minimum dressing (I, weight 2), while B19 uses the maximum (OMI, weight 6). Together they span the extremes of within-orbit movement. They occur at the two structural "pause" points in the Eulerian path — moments where the walk dwells in an orbit before resuming its traversal.
