# Surjection Count Formula + Orbit C Selection + Nuclear Map Analysis

## Part 1: Surjection Count Formula for E=1 Cases

At excess E = 1 (p = 2^n − 3), exactly 2 partition shapes exist:
- **Shape A** ("spread"): m₀=1, one c_j=2, rest c_j=1 → partition {2,2,2,1^(p−3)}
- **Shape B** ("concentrated"): m₀=2, all c_j=1 → partition {4,1^(p−1)}

### Exact formulas

Let R = 2^(n−1), num_neg = (p−1)/2 = R − 2.

**Shape A count:**
```
N_A = (R!/2) × num_neg × 2^(R−1)
    = R! × (R−2) × 2^(R−2)
```
- Multinomial R!/(1!×2!×1!^(num_neg−1)) = R!/2
- Orderings: num_neg choices for which slot gets the 2
- Orientations: 2^(R−1) (m₀=1 pair fixed, R−1 others have orientation choice)

**Shape B count:**
```
N_B = (R!/2) × 1 × 2^(R−2)
    = R! × 2^(R−3)
```
- Multinomial R!/(2!×1!^num_neg) = R!/2
- Orderings: 1 (all c_j are identical)
- Orientations: 2^(R−2) (m₀=2 pairs fixed, R−2 others choose)

**Ratio:**
```
N_A/N_B = num_neg × 2 = 2(R−2) = 2^n − 6
```

### Verification

| n | p=2^n−3 | R | Shape A (spread) | Shape B (conc.) | Total | Ratio A:B | Match |
|---|---------|---|------------------|-----------------|-------|-----------|-------|
| 3 | 5 | 4 | 192 | 48 | 240 | 4:1 | A:✓ B:✓ |
| 4 | 13 | 8 | 15,482,880 | 1,290,240 | 16,773,120 | 12:1 | A:✓ B:✓ |
| 5 | 29 | 16 | 4,799,185,853,349,888,000 | 171,399,494,762,496,000 | 4,970,585,348,112,384,000 | 28:1 | A:✓ B:✓ |
| 6 | 61 | 32 | 8,476,037,543,994,919,744,162,430,801,469,977,395,200,000,000 | 141,267,292,399,915,329,069,373,846,691,166,289,920,000,000 | 8,617,304,836,394,835,073,231,804,648,161,143,685,120,000,000 | 60:1 | (no ref) |

**All verified cases match.** The ratio N_A/N_B = 2 × num_neg = p − 1 is exact:
- (n=3, p=5): ratio = 4:1, p−1 = 4 ✓
- (n=4, p=13): ratio = 12:1, p−1 = 12 ✓
- (n=5, p=29): ratio = 28:1, p−1 = 28 ✓
- (n=6, p=61): ratio = 60:1, p−1 = 60 ✓

**Closed-form ratio: N_A/N_B = 2 × num_neg = p − 1**

This makes intuitive sense: Shape A has num_neg choices for which negation pair
gets the doubleton, times 2 for the extra orientation freedom (m₀=1 vs m₀=2
means one more pair has a free orientation choice).

---
## Part 2: Orbit C Selection via Nuclear Map

Total surjections at (3,5): 240

### Three orbits of three-type assignments

The 12 three-type distributions group into 3 orbits under the
question "what type is the Frame pair?":

| Orbit | Frame type | Sub-assignments | Surjections | S₃ orbit size |
|-------|-----------|----------------|-------------|---------------|
| A | Type 0 | 3 | 48 | 3 |
| B | Type 1 | 3 | 48 | 3 |
| C | Type 2 | 6 | 96 | 6 |

Orbit C (Frame = Type 2) has 6 sub-assignments because the Frame pair
is Type 2, meaning it shares a negation pair with one non-frame pair,
and the remaining assignment of Types 0 and 1 to the other two non-frame
pairs has 3! / 1 = 6 possibilities (P₃(Types) = 3×2×1 but one Type 2
is absorbed by Frame's partner).

### The P→H rotation as selection principle

The nuclear map (互) rotates parity axes: P-parity of the nuclear trigram
equals H-parity of the original (proved in synthesis-1.md). This creates
a flow between line types:

Within Orbit C, the P→H flow for each sub-assignment:

| Type tuple (Fr,H,Q,P) | P type | H type | P→H flow | Coherence |
|----------------------|--------|--------|----------|-----------|
| (2, 0, 1, 2) | 2 | 0 | Type 2 → Type 0 | **COHERENT** ← I Ching |
| (2, 0, 2, 1) | 1 | 0 | Type 1 → Type 0 | cross |
| (2, 1, 0, 2) | 2 | 1 | Type 2 → Type 1 | cross |
| (2, 1, 2, 0) | 0 | 1 | Type 0 → Type 1 | cross |
| (2, 2, 0, 1) | 1 | 2 | Type 1 → Type 2 | cross |
| (2, 2, 1, 0) | 0 | 2 | Type 0 → Type 2 | anti-coherent |

**Result:** Exactly 1/6 Orbit C sub-assignment has coherent P→H flow.

### What "coherent" means

In the coherent assignment (2,0,1,2):
- **P carries Type 2** (shared doubleton = Earth/Metal)
- **H carries Type 0** (zero-mapped pair = Wood)
- The P→H rotation sends the P-parity axis to the H-parity axis
- This means: the "dynamically active" parity (governing 五行 relations)
  flows toward the "algebraically inert" direction (zero pair)
- The next step (H→ī) ejects this to orbit space, where it becomes
  the attractor bifurcation bit (ī=0 → fixed point, ī=1 → 2-cycle)

The parity cascade under iterated nuclear extraction:

```
Step 0: P-parity (Type 2, active)  — governs 五行 relations (同/生/克)
Step 1: → H-parity (Type 0, inert) — via P→H rotation
Step 2: → ī (orbit, stable)         — via H→orbit projection
```

This cascade is **monotonically decreasing in activity** (active → inert → stable)
only for the I Ching's assignment. The anti-coherent assignment (2,2,1,0) would
have the inert pair flowing to the active direction — parity information would
*increase* in complexity under nuclear extraction, violating the convergence
structure of 互.

### The complete reduction chain

```
240 surjections at (3,5)
 │
 ├── 48 two-type {0,1} → partition {4,1,1,1,1}, 4 singletons
 │   (6 sub-assignments × 8 each)
 │
 └── 192 three-type {0,1,2} → partition {2,2,2,1,1}, 2 singletons
     │
     ├── Orbit A: Frame=Type 0  (48 surjections, 3 sub-assignments)
     ├── Orbit B: Frame=Type 1  (48 surjections, 3 sub-assignments)
     └── Orbit C: Frame=Type 2  (96 surjections, 6 sub-assignments)
         │
         │ Selection: Frame as Type 2 is the ONLY orbit where
         │ Frame shares a negation pair with a line pair,
         │ matching the 五行 structure (坤/乾 share {Earth,Metal}
         │ with 艮/兌 on the P-line)
         │
         ├── (2,0,1,2): P→H COHERENT  ← I Ching
         ├── (2,0,2,1): cross
         ├── (2,1,0,2): cross
         ├── (2,1,2,0): cross
         ├── (2,2,0,1): cross
         └── (2,2,1,0): anti-coherent
             │
             │ Selection: P→H coherence (unique)
             │
             └── 16 surjections with assignment (2,0,1,2)
                 │
                 ├── 8 on negation pair {1,4}: Frame→1, P→4 or Frame→4, P→1
                 └── 8 on negation pair {2,3}: Frame→2, P→3 or Frame→3, P→2
                     │
                     │ Aut(Z₅) acts: 4 orbits of 4
                     │ Each orbit ≅ {×1, ×2, ×3, ×4}
                     │
                     └── 2 final choices (0.5 bits)
                         Orientation within the non-Aut(Z₅) residual
```

### Summary of selection factors

| Step | Factor | Reduction | Mechanism |
|------|--------|-----------|-----------|
| Three-type selection | ×(192/240) | 240 → 192 | Partition {2,2,2,1,1} |
| Orbit C selection | ×(96/192) | 192 → 96 | Frame = Type 2 (五行 structure) |
| P→H coherence | ×(16/96) | 96 → 16 | Nuclear map rotation coherence |
| Aut(Z₅) quotient | ×(4/16) | 16 → 4 | Automorphism equivalence |
| Residual | ×(2/4) | 4 → 2 | Genuine 0.5-bit freedom |

Total: 240 → 2, reduction factor = 120 = |S₅|/1 = 5!/1.
The 0.5 bits = log₂(2) = 1 binary choice, corresponding to which
orientation within the Aut(Z₅)-orbit is chosen by the compass datum.

---
## Part 3: Why the Nuclear Map Breaks the Line Symmetry

The abstract algebra at (3,5) treats H, P, Q symmetrically — S₃ acts
transitively on them, and the type distributions are uniform. But the
nuclear map (互) breaks this symmetry:

| Line | Nuclear role | P→H rotation | Attractor connection |
|------|-------------|-------------|---------------------|
| **H** = ker(b₁⊕b₂) | 互 kernel | Rotation TARGET | Stab(H) = S₄ |
| **P** = ker(b₀⊕b₁) | 五行 parity | Rotation SOURCE | Fiber bridge |
| **Q** = ker(b₀⊕b₂) | Palindromic | Exits to orbit | Attractor pair {坎,離} |

The nuclear map creates a directed flow P → H → orbit(Q).
This flow orders the three lines, breaking S₃ down to the identity.
The I Ching's type assignment is the unique one aligned with this flow:

- **P = Type 2** (source of parity flow, shared doubleton)
- **H = Type 0** (target of rotation, inert zero-pair)
- **Q = Type 1** (orbit exit, singleton attractor pair)

Each line carries the type that matches its dynamical role:
the most "active" type (shared pair, largest fiber) at the source,
the most "inert" type (zero pair) at the intermediate,
and the most "distinguished" type (singletons) at the terminus.

---
*Computed in 0.00s*