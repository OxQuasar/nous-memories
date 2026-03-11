# 先天 as Fano Walk: Findings

## 1. 先天 Fano Characterization

### Step-XOR Pattern

The 先天 arrangement (clockwise from S):
乾→兌→離→震→坤→艮→坎→巽→乾

| Step | From → To | XOR | Mask | Fano lines |
|------|-----------|-----|------|------------|
| 1 | 乾→兌 | 100 | I | ker(O), ker(M), P |
| 2 | 兌→離 | 110 | MI | ker(O), H, ker(OMI) |
| 3 | 離→震 | 100 | I | ker(O), ker(M), P |
| 4 | 震→坤 | 001 | O | ker(M), ker(I), H |
| 5 | 坤→艮 | 100 | I | ker(O), ker(M), P |
| 6 | 艮→坎 | 110 | MI | ker(O), H, ker(OMI) |
| 7 | 坎→巽 | 100 | I | ker(O), ker(M), P |
| 8 | 巽→乾 | 001 | O | ker(M), ker(I), H |

**Pattern: (I, MI, I, O) × 2** — period 4, using 3 generators.

### Generator Triangle

The generators {O(001), I(100), MI(110)} form a **triangle** in PG(2,2):

| Edge | Generators | Fano line | Third point |
|------|-----------|-----------|-------------|
| 1 | {O, MI} | **H** = ker(b₁⊕b₂) | OMI(111) |
| 2 | {I, MI} | ker(O) = ker(b₀) | M(010) |
| 3 | {O, I} | ker(M) = ker(b₁) | OI(101) |

This triangle has one edge on the distinguished line H and two edges
on non-through-OMI lines. The generators are NOT collinear.

### Hamiltonian Cycle Structure

**Verified.** 12 three-element generator sets admit complement-antipodal
Hamiltonian cycles on F₂³. All are non-collinear triples (triangles).
No single Fano line admits any Hamiltonian cycle.

The 12 sets partition into **3 families of 4** by through-OMI edge:

| Family | Fixed edge | On line | Third generator options |
|--------|-----------|---------|------------------------|
| H | {O, MI} | H = ker(b₁⊕b₂) | M, OM, **I**, OI |
| P | {OM, I} | P = ker(b₀⊕b₁) | O, M, OI, MI |
| Q | {M, OI} | Q = ker(b₀⊕b₂) | O, OM, I, MI |

先天 uses **{O, I, MI}** from Family H. Within Family H, it is the
unique member whose other two edges lie on the single-bit lines
ker(O) = ker(b₀) and ker(M) = ker(b₁).

Each generator set admits exactly 4 directed (= 2 undirected)
complement-antipodal cycles.

## 2. 後天 Step-XOR Analysis

| Step | From → To | XOR | Mask | Fano lines |
|------|-----------|-----|------|------------|
| 1 | 離→巽 | 011 | OM | P, ker(I), ker(OMI) |
| 2 | 巽→震 | 111 | OMI | P, Q, H |
| 3 | 震→艮 | 101 | OI | ker(M), Q, ker(OMI) |
| 4 | 艮→坎 | 110 | MI | ker(O), H, ker(OMI) |
| 5 | 坎→乾 | 101 | OI | ker(M), Q, ker(OMI) |
| 6 | 乾→兌 | 100 | I | ker(O), ker(M), P |
| 7 | 兌→坤 | 011 | OM | P, ker(I), ker(OMI) |
| 8 | 坤→離 | 101 | OI | ker(M), Q, ker(OMI) |

後天 uses **5 generators** (OM, I, OI, MI, OMI) vs. 先天's 3.

### Generator Comparison

| | 先天 | 後天 |
|---|------|------|
| Generators | O, I, MI | OM, I, OI, MI, OMI |
| Count | 3 | 5 |
| Shared | I, MI | |
| Unique | O | OM, OI, OMI |

### Fano Line Hit Counts

| Line | 先天 | 後天 | Change |
|------|------|------|--------|
| ker(O) | 6/8 | 2/8 | ↓4 |
| ker(M) | 6/8 | 4/8 | ↓2 |
| P | 4/8 | 4/8 | =0 |
| ker(I) | 2/8 | 2/8 | =0 |
| Q | 0/8 | 4/8 | ↑4 |
| H | 4/8 | 2/8 | ↓2 |
| ker(OMI) | 2/8 | 6/8 | ↑4 |

**Key shift:** Q goes from 0/8 (absent in 先天) to 4/8 (prominent in 後天).
The transition introduces Q-line structure that 先天 lacks entirely.

## 3. Symmetry Breaking

### Complement-Antipodal Pairs

| Pair | 先天 | 後天 | Status |
|------|------|------|--------|
| S-N | 乾/坤 ✓ | 離/坎 ✓ | PRESERVED |
| SE-NW | 兌/艮 ✓ | 巽/乾 ✗ | BROKEN |
| E-W | 離/坎 ✓ | 震/兌 ✗ | BROKEN |
| NE-SW | 震/巽 ✓ | 艮/坤 ✗ | BROKEN |

Only **{坎,離}** (Q-line pair, Water/Fire) remains diametrically opposite.

### Transition Permutation

The 先天→後天 transition has cycle structure:

- **(S→NW→NE→E)**: carries {乾→艮→震→離}
- **(SW→SE→W→N)**: carries {巽→兌→坎→坤}
- The two 4-cycles are related by 180° rotation.

The transition is NOT a dihedral element (not a pure rotation or reflection).

### The 0.5-Bit in Transition Context

In 先天, all four complement pairs are equivalent (D₂ symmetry).
The transition breaks this, preserving only the Q-axis:

| Pair | Fano line | 後天 distance | Status |
|------|-----------|--------------|--------|
| 坤/乾 | P | 2 | BROKEN |
| 震/巽 | H | 1 | BROKEN |
| 坎/離 | Q | 4 | PRESERVED |
| 兌/艮 | P | 3 | BROKEN |

The 0.5-bit chooses whether Wood (same-element pair) goes on:
- **H** (traditional): the BROKEN axis — Wood elements adjacent in 後天
- **Q** (alternative): the PRESERVED axis — Wood elements still opposite

Traditional = breaking the same-element pair's antipodality while
preserving the singleton elements' antipodality (Water/Fire on Q).

## 4. Synthesis Addendum

### 先天 = Fano triangle walk

The 先天 arrangement is characterized by:
1. Generator set {O, I, MI} from Family H (12 triangle sets exist,
   in 3 families by through-OMI edge; 先天 uses Family H)
2. Within Family H, unique member with single-bit edges (ker(O), ker(M))
3. Step pattern (I, MI, I, O) × 2: alternating I with MI/O
4. 2 undirected cycles exist; 先天 is one of them

### 後天 = 先天 + compass (Z₅)
The transition from 先天 to 後天:
- Breaks 3/4 complement-antipodal pairs
- Preserves only Q-axis (the dynamic/attractor axis)
- Introduces Q-line steps (absent in 先天)
- Increases generator count from 3 to 5
- Is two 4-cycles, related by 180° rotation

### What this means for the 0.5-bit

The 先天→後天 transition selects the Q-axis as the preserved
complement-antipodal axis. This creates an asymmetry between
the two odd-coset complement pairs:
- {坎,離} on Q: PRESERVED by transition, 互 attractor positions
- {震,巽} on H: BROKEN by transition, adjacent in 後天

The traditional assignment places Wood (same-element) on H,
the broken axis. The alternative places it on Q, the preserved axis.
While neither is forced by algebraic constraints alone,
the transition provides geometric context for the choice:

**The same-element pair belongs to the axis whose symmetry
the compass datum breaks.** The preserved axis carries the
dynamic singletons (Water/Fire = 互 attractors).
