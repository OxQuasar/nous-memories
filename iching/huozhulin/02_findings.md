# Probe 2: Palace Generation in Kernel Language

## 1. Palace Generation Verified

Standard 京房 algorithm: from doubled root TT, cumulatively flip
b₀→b₄ (ranks 1–5), un-flip b₃ (游魂), un-flip b₀,b₁,b₂ (歸魂).

All 64 hexagrams uniquely assigned to 8 palaces × 8 ranks. ✓

### Cumulative XOR masks

| Rank | Mask | Bits flipped |
|------|------|-------------|
| 本宮 | 000000 | (none) |
| 一世 | 000001 | b₀ |
| 二世 | 000011 | b₀, b₁ |
| 三世 | 000111 | b₀, b₁, b₂ |
| 四世 | 001111 | b₀, b₁, b₂, b₃ |
| 五世 | 011111 | b₀, b₁, b₂, b₃, b₄ |
| 游魂 | 010111 | b₀, b₁, b₂, b₄ |
| 歸魂 | 010000 | b₄ |

**Key observation:** b₅ (line 6) is NEVER flipped. The top line is the palace
invariant — the unchanging bit across all 8 members. 本宮 places 世 at this
invariant position (世=6).

### Verification

- 姤 (111110): Qian ☰ 一世 ✓
- 遁 (111100): Qian ☰ 二世
  (Note: example.md labels 遁 as 三世. Standard 京房 algorithm gives 二世.)

## 2. Rank → Basin

| Rank | Kun | Qian | Cycle | Basin change? |
|------|-----|------|-------|---------------|
| 本宮 | 2 | 2 | 4 | No |
| 一世 | 2 | 2 | 4 | No |
| 二世 | 2 | 2 | 4 | No |
| 三世 | 2 | 2 | 4 | Yes |
| 四世 | 2 | 2 | 4 | No |
| 五世 | 2 | 2 | 4 | No |
| 游魂 | 2 | 2 | 4 | Yes |
| 歸魂 | 2 | 2 | 4 | No |

**The distribution is 2-2-4 at every rank** — perfectly uniform. Rank and basin
are statistically independent.

At ranks 3 and 6, every individual hexagram changes basin from its root (the mask
flips b₂ but not b₃, toggling b₂⊕b₃). But the aggregate distribution is preserved
because the root distribution is already 2-2-4 and the basin permutation is symmetric:
Kun↔Cycle (for roots with b₃=0), Qian↔Cycle (for roots with b₃=1).

## 3. Rank → Depth

| Rank | d=0 | d=1 | d=2 |
|------|-----|-----|-----|
| 本宮 | 2 | 0 | 6 |
| 一世 | 0 | 2 | 6 |
| 二世 | 0 | 2 | 6 |
| 三世 | 2 | 0 | 6 |
| 四世 | 0 | 2 | 6 |
| 五世 | 0 | 2 | 6 |
| 游魂 | 0 | 2 | 6 |
| 歸魂 | 0 | 2 | 6 |

### Attractor positions

| Attractor | Palace | Rank |
|-----------|--------|------|
| 000000 | Kun ☷ | 本宮 |
| 010101 | Kan ☵ | 三世 |
| 101010 | Li ☲ | 三世 |
| 111111 | Qian ☰ | 本宮 |

The two **fixed-point** attractors (乾, 坤) sit at **rank 0** (本宮) — the palace roots.

The two **cycle** attractors (既濟, 未濟) sit at **rank 3** (三世) — the rank where
the palace algorithm first penetrates the interface layer. The oscillating attractors
appear exactly when the generation walk reaches the basin-determining core.

## 4. Inner XOR Mask — Onion Decomposition

| Rank | Full mask | O(b₀,b₅) | M(b₁,b₄) | I(b₂,b₃) | Inner | ker(M)? | im(M)? |
|------|-----------|-----------|-----------|-----------|-------|---------|--------|
| 本宮 | 000000 | (0, 0) | (0, 0) | (0, 0) | 0000 | ✓ | ✓ |
| 一世 | 000001 | (1, 0) | (0, 0) | (0, 0) | 0000 | ✓ | ✓ |
| 二世 | 000011 | (1, 0) | (1, 0) | (0, 0) | 0001 | ✓ |  |
| 三世 | 000111 | (1, 0) | (1, 0) | (1, 0) | 0011 |  |  |
| 四世 | 001111 | (1, 0) | (1, 0) | (1, 1) | 0111 |  |  |
| 五世 | 011111 | (1, 0) | (1, 1) | (1, 1) | 1111 |  | ✓ |
| 游魂 | 010111 | (1, 0) | (1, 1) | (1, 0) | 1011 |  |  |
| 歸魂 | 010000 | (0, 0) | (0, 1) | (0, 0) | 1000 | ✓ |  |

### The palace walk as onion traversal

```
Rank 0 (本宮):  identity         — no change
Rank 1 (一世):  outer only        — surface perturbation
Rank 2 (二世):  outer + shell     — enters ker(M)
Rank 3 (三世):  + one interface   — CROSSES into core ← basin changes
Rank 4 (四世):  + both interface  — full core engagement (basin returns)
Rank 5 (五世):  all inner bits    — complete inner inversion ∈ im(M)
Rank 6 (游魂):  partial retract   — un-flip one interface ← basin changes again
Rank 7 (歸魂):  shell only        — returns to ker(M)
```

The palace generation is a **drill-in, then retract** pattern through the onion.
It starts at the surface, penetrates to the core, then partially withdraws.

## 5. 世 Line → Onion Layer

| Rank | 世 | 應 | 世 layer | 應 layer |
|------|----|----|----------|----------|
| 本宮 | L6 (b5) | L3 (b2) | outer | interface |
| 一世 | L1 (b0) | L4 (b3) | outer | interface |
| 二世 | L2 (b1) | L5 (b4) | shell | shell |
| 三世 | L3 (b2) | L6 (b5) | interface | outer |
| 四世 | L4 (b3) | L1 (b0) | interface | outer |
| 五世 | L5 (b4) | L2 (b1) | shell | shell |
| 游魂 | L4 (b3) | L1 (b0) | interface | outer |
| 歸魂 | L3 (b2) | L6 (b5) | interface | outer |

### Layer occupancy count

| Layer | Ranks with 世 | Count |
|-------|--------------|-------|
| outer | 本宮, 一世 | 2 |
| shell | 二世, 五世 | 2 |
| interface | 三世, 四世, 游魂, 歸魂 | 4 |

**Interface gets the most 世 occupancy** (4 of 8 ranks). The querent's self (世)
sits on the basin-determining bits at ranks 三世, 四世, 游魂, 歸魂. At these ranks,
the structural core of the hexagram is literally the querent's position.

### 世-on-interface basin distribution

32 hexagrams with 世 on interface: Kun=8, Qian=8, Cycle=16
(Compare uniform: 8, 8, 16 for the Kun/Qian/Cycle ratio.)

## 6. Full Cross-Tabulation: Rank × Basin × Depth

```
Rank    Kun(d0,d1,d2)  Qian(d0,d1,d2)  Cycle(d0,d1,d2)
────────────────────────────────────────────────────────────
本宮      1  0  1    1  0  1    0  0  4  
一世      0  1  1    0  1  1    0  0  4  
二世      0  0  2    0  0  2    0  2  2  
三世      0  0  2    0  0  2    2  0  2  
四世      0  0  2    0  0  2    0  2  2  
五世      0  1  1    0  1  1    0  0  4  
游魂      0  1  1    0  1  1    0  0  4  
歸魂      0  0  2    0  0  2    0  2  2  
```

Totals: depth-0=4, depth-1=12, depth-2=48 (of 64)

## 7. Key Findings

### Finding 1: Palace walk = onion traversal

The palace generation algorithm is a structured walk through the three-layer onion:
outer → shell → interface → (retract). This is NOT coincidental — the algorithm
cumulatively flips bits from b₀ inward, which exactly follows the onion layers.

### Finding 2: Attractors mark structural boundaries

Fixed-point attractors (乾, 坤) = palace roots (rank 0).
Cycle attractors (既濟, 未濟) = rank 3 (first interface penetration).
The 4 attractors of the 互 system appear at exactly the two structurally
distinguished ranks in the palace system.

### Finding 3: Basin distribution invariant across ranks

Despite individual hexagrams changing basins at ranks 3 and 6 (where the mask
toggles b₂⊕b₃), the aggregate distribution 2-2-4 (Kun-Qian-Cycle) is identical
at every rank. The root basin distribution happens to be 2-2-4 (坤/坎 in Kun,
乾/離 in Qian, 4 others in Cycle), and the basin permutation at ranks 3/6
preserves this ratio.

### Finding 4: 世 favors the interface

The 世 line occupies the interface (b₂ or b₃) at 4 of 8 ranks — double the
frequency of outer or shell. When 世 sits on an interface bit, the querent's
identity is bound to the basin-determining structure.

### Finding 5: Line 6 is the palace invariant

b₅ (line 6, top line) is never touched by the palace algorithm. It is the only
bit that stays constant across all 8 members of any palace. The 本宮 hexagram
places 世 precisely at this invariant — the self is anchored to what never changes.

### Finding 6: 世 and 應 sit on complementary layers

世 and 應 are always 3 lines apart. The line pairs (1,4), (2,5), (3,6) map to
layer pairs (outer,interface), (shell,shell), (interface,outer). So 世 and 應
always occupy complementary onion layers — when the self is on the surface,
the other is at the core, and vice versa. The only exception is shell-shell
(二世, 五世), where both sit at the same depth.

### Finding 7: Rank ≠ depth (orthogonality maintained)

There is no rank that concentrates depth-0 or depth-1 hexagrams beyond what
the attractor positions force. The 1:3:12 ratio within basins means most cells
in the rank×basin×depth table are sparse. Rank and convergence depth are
effectively independent coordinates.
