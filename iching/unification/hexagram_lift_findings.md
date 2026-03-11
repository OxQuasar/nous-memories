# Hexagram Lift: PG(2,2) × PG(2,2) Findings

## 1. Product Fano Analysis

Each hexagram decomposes as (position, orbit) ∈ F₂³ × F₂³:
- Position = lower trigram (o, m, i) = (L1, L2, L3)
- Orbit = palindromic signature (ō, m̄, ī) = (L1⊕L6, L2⊕L5, L3⊕L4)

### Line Conditions

In each factor, the three distinguished lines impose conditions:

| Line | Position condition | Orbit condition |
|---|---|---|
| H = ker(b₁⊕b₂) | L2 = L3 | L2⊕L5 = L3⊕L4 |
| P = ker(b₀⊕b₁) | L1 = L2 | L1⊕L6 = L2⊕L5 |
| Q = ker(b₀⊕b₂) | L1 = L3 | L1⊕L6 = L3⊕L4 |

### Key Finding: Only Line H Refines Blocks

From Computation 3 of iteration 1: the spaceprobe block system is refined
ONLY by line H's coset partition. In the product structure, this means
the block system lives on the H-axis of each factor.

## 2. 互 in the Factored Basis

### The Matrix

```
  o' = m
  m' = i
  i' = i ⊕ ī
  ō' = m̄
  m̄' = ī
  ī' = ī
```

### Decomposition

互 is NOT a product map. It is a **shear**:

- **Orbit factor** (independent): ō' = m̄, m̄' = ī, ī' = ī
  → shifts ō→m̄→ī then projects onto ī
- **Position factor** (almost independent): o' = m, m' = i
  → shifts o→m→i
- **Shear term**: i' = i ⊕ **ī** (position i gets orbit ī mixed in)

The shear is a single term: the orbit's ī-coordinate leaks into position.
This is the algebraic source of the JiJi/WeiJi 2-cycle:

- In the stable image (after 2+ applications), only i and ī survive
- The action on {i, ī} is: i ↦ i ⊕ ī, ī ↦ ī
- If ī = 0 (palindromic): i ↦ i → fixed point (Qian or Kun)
- If ī = 1 (anti-palindromic): i ↦ i ⊕ 1 → 2-cycle

### Rank Sequence

| Power | Rank | Nullity | Killed coordinates |
|---|---|---|---|
| M | 4 | 2 | o, ō |
| M² | 2 | 4 | o, m, ō, m̄ |
| M³ | 2 | 4 | (stable) |

The kernel chain kills coordinates symmetrically across factors:
first the outermost (o, ō), then the middle (m, m̄).
The surviving coordinates {i, ī} are the innermost positions in both factors.

## 3. Attractor Fano Alignment

| Attractor | hex | Position | Orbit | Pos lines | Orb lines |
|---|---|---|---|---|---|
| Qian 乾 | 111111 | 乾(111) | 坤(000) | P=ker(b₀⊕b₁), Q=ker(b₀⊕b₂), H=ker(b₁⊕b₂) | origin |
| Kun 坤 | 000000 | 坤(000) | 坤(000) | origin | origin |
| JiJi 既濟 | 010101 | 離(101) | 乾(111) | ker(M), Q=ker(b₀⊕b₂), ker(OMI) | P=ker(b₀⊕b₁), Q=ker(b₀⊕b₂), H=ker(b₁⊕b₂) |
| WeiJi 未濟 | 101010 | 坎(010) | 乾(111) | ker(O), ker(I), Q=ker(b₀⊕b₂) | P=ker(b₀⊕b₁), Q=ker(b₀⊕b₂), H=ker(b₁⊕b₂) |

### Structural Pattern

The 4 attractors split into two complementary pairs:

1. **Frame pair** {Qian, Kun}: orbit = 000 (origin = palindromic)
   - Position projections = {乾, 坤} = the frame pair itself
   - These are the FIXED POINTS of 互 (ī = 0 → no oscillation)

2. **Bridge pair** {JiJi, WeiJi}: orbit = 111 (OMI = anti-palindromic)
   - Position projections = {離, 坎} = the Q-line complement pair
   - These form the 2-CYCLE of 互 (ī = 1 → i oscillates)
   - 坎 and 離 are the Water/Fire singletons (k₁ destination type)

The orbit projection {000, 111} = {origin, OMI} is the complement axis —
the unique pair that lies in ALL subgroups (origin) or ALL OMI-lines (OMI).

## 4. Bridge Kernels in Product Fano

### Bridge Decomposition

| Category | Count |
|---|---|
| Position-only (Δorb = 0) | 34 |
| Orbit-only (Δpos = 0) | 5 |
| Mixed (both nonzero) | 25 |
| Total | 64 |

### Fano Line Statistics

| Line | Pos hits | Pos % | Orb hits | Orb % | Expected % |
|---|---|---|---|---|---|
| H=ker(b₁⊕b₂) | 31 | 52.5% | 16 | 53.3% | 42.9% |
| P=ker(b₀⊕b₁) | 25 | 42.4% | 16 | 53.3% | 42.9% |
| Q=ker(b₀⊕b₂) | 27 | 45.8% | 12 | 40.0% | 42.9% |
| ker(O) | 21 | 35.6% | 14 | 46.7% | 42.9% |
| ker(M) | 27 | 45.8% | 8 | 26.7% | 42.9% |
| ker(I) | 23 | 39.0% | 10 | 33.3% | 42.9% |
| ker(OMI) | 23 | 39.0% | 14 | 46.7% | 42.9% |

Expected % = 3/7 ≈ 42.9% (each nonzero vector lies on 3 of 7 lines).

### Within-Pair vs Between-Pair

KW pairs: (1,2), (3,4), ..., (63,64)

**Key finding: All 32 within-pair bridges have Δorb = 0.**
This is a theorem, not a coincidence: KW pairs are either
reversals or complements, and both operations preserve orbit:
- Reversal swaps (L1,L2,L3) ↔ (L6,L5,L4) → symmetric XOR unchanged
- Complement flips all lines → L_k⊕L_{7-k} unchanged

Therefore **KW pairing = orbit class**. Within-pair transitions
change only position (lower trigram), never the palindromic signature.

| Metric | Within-pair | Between-pair |
|---|---|---|
| Count | 32 | 32 |
| Δpos = 0 | 0 (0%) | 5 (16%) |
| Δorb = 0 | 32 (100%) | 2 (6%) |

## Synthesis

### The Shear Structure of 互

The factored basis reveals 互 as a shear map on F₂³ × F₂³:
it acts independently on orbit but couples orbit→position via a single
term (ī leaks into i). This is the minimal departure from a product map.

The rank sequence 6→4→2→2 kills coordinates symmetrically: first the
outer O-coordinates (o,ō), then the middle M-coordinates (m,m̄), leaving
only the inner I-coordinates (i,ī). The stable image is 2-dimensional,
spanned by {i, ī}, and the dynamics on this 2D space is:

```
i ↦ i ⊕ ī
ī ↦ ī
```

This gives exactly the observed attractor structure:
- ī = 0 → i is fixed → {Qian, Kun} (position i=1,0)
- ī = 1 → i oscillates → {JiJi, WeiJi} 2-cycle

### Fano Alignment of Attractors

The attractors occupy a remarkably constrained locus in PG(2,2) × PG(2,2):
- Orbit: only {000, 111} = {origin, OMI} — the complement axis endpoints
- Position of 2-cycle: {坎, 離} = the Q-line pair = Water/Fire singletons
- Position of fixed points: {坤, 乾} = the frame pair = Earth/Metal doublets

The Q-line (palindromic condition ker(o⊕i)) governs which hexagrams
oscillate under 互: those with position on line Q and orbit = OMI.

### KW Pairing = Orbit Class

All 32 within-pair bridges have Δorb = 0 (100%). This is a theorem:
reversal and complement both preserve orbit (palindromic signature),
and every KW pair is related by one of these operations.
Within-pair transitions change only position; between-pair transitions
typically change both.

Line H is enriched in position bridges (52.5% vs 42.9% expected),
and H + P together dominate orbit bridges (53.3% each).
This suggests the KW sequence navigates preferentially along
Fano-line-aligned axes in the product geometry.
