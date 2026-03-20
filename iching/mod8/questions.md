# Mod-8 Investigation — Questions

## Core Question: What is the structural relationship between the 先天 mod-8 divination arithmetic and the F₂³ algebraic structure?

The 梅花易數 algorithm maps calendar numbers to trigrams via mod-8 arithmetic on the 先天 ordering. The Phase 1–8 findings (GMS, valve, complement-Z₅, forcing chain) all live on F₂³ (the Boolean hypercube Q₃). These are connected by a specific permutation — bit-reversal composed with complement — but the structural consequences of this connection have not been analyzed.

### The map

先天(n) = bit_reverse(8 − n), where n ∈ {1,...,8} is the 先天 position and the output is a 3-bit F₂³ vector.

| 先天 n | Trigram | F₂³ (top,mid,bot) | Decimal |
|--------|---------|-------------------|---------|
| 1 | 乾 | 111 | 7 |
| 2 | 兌 | 011 | 3 |
| 3 | 離 | 101 | 5 |
| 4 | 震 | 001 | 1 |
| 5 | 巽 | 110 | 6 |
| 6 | 坎 | 010 | 2 |
| 7 | 艮 | 100 | 4 |
| 8 | 坤 | 000 | 0 |

### What the map preserves

- **Complement:** n ↔ 9−n corresponds to bitwise NOT in F₂³ (乾↔坤, 兌↔艮, 離↔坎, 震↔巽)
- **Top-bit bisection:** positions 1–4 have bottom line yang (bit0=1), positions 5–8 have bottom line yin (bit0=0)

### What the map scrambles

- **Adjacency:** mod-8 neighbors (n, n+1) are NOT Hamming-1 neighbors on Q₃. E.g. positions 3,4 (離=101, 震=001) are Hamming distance 2. The cyclic topology and the hypercube topology are incompatible.
- **Addition:** mod-8 addition (used in the divination algorithm) does NOT correspond to XOR (the natural F₂³ operation). The divination arithmetic has no simple algebraic interpretation on the hypercube.

### Questions

**M1: [answered]** What does the 先天 permutation do to the 五行 partition? → Consecutive pairs for paired elements, singletons at positions 3,6. Bit-layer decomposition: bit₂ = 克-free, bit₁ = pure 克. The mod-8 cycle's Q₃ edges are entirely in the 克-free bit₂ layer. See findings §I–II.

**M2: [answered]** What does mod-8 addition do to transition types? → No non-trivial cyclic shift preserves 五行 pair types. The element map is never well-defined for k≠0. Z₈ and Z₅ are fundamentally incompatible. See findings §IV.4.

**M3: [answered]** What is the distribution of 五行 transition types over hexagrams reachable by the date formula? → Unweighted shift average = null exactly (algebraic necessity); hour-weighted ergodic shows +2.08% 克-enrichment and −2.60% favorability; mod-8/mod-6 gcd=2 coupling creates deterministic 2:1 体 bias per (upper, shift) pair but averages to 1/2. See findings §V.

**M4: [answered]** Do the grammatical constraints (GMS, valve) survive at hexagram level under the date formula? → No. Total failure: GMS 27.3% violation rate, valve 27.0% non-zero, all 克-克 pairs admit directed 克体-克体. Grammar requires Q₃-edge locality (single bit-flips); calendar navigates via Z₈ cyclic shifts (multi-bit jumps). See findings §VI.

**M5: [answered]** Which topology governs transition detection from sequential data? → Neither topology produces detectable grammar. Bit-layer structure is tautological (functor property of WUXING_MAP, not data property). GMS/valve fail for all tested data sources. Q₃ is not an interval graph (R286-R287), so scalar discretization cannot access Q₃ adjacency. See findings §VII.

**M6 (new from §VIII):** The 先天 cycle projects to a retrograde palindrome on Z₅ centered on 木. 木 is simultaneously the 互 kernel element (Fano line H), the palindrome center, and the b₀ yin/yang hinge. Is this triple alignment forced by some constraint, or is it a free choice of the 先天 ordering?

### Context

This question arose from assessing the fana trading signal document, which applies Shao Yong's mod-8 algorithm to price bars. The Phase 1–8 investigation characterized the I Ching's algebraic structure on Q₃ but never examined the divination layer's cyclic arithmetic. The relationship between these two layers — cyclic vs hypercubic — is an unexplored seam in the investigation.
