# CC Identity Results: The Algebraic Identity of the 五行 Map

## Summary

The 五行 map f: F₂³ → Z₅ induces a **coherent configuration** (CC) on F₂³ with **28 classes**, which equals the orbit partition of the fiber automorphism group (Z₂)³ on ordered pairs. It is **not** an association scheme (intersection matrices do not commute). The CC resolves all fiber structure — the Z₅ difference alone is too coarse.

The Walsh-Hadamard spectrum lives in Q(√5), with W(000) = −1/φ (negative reciprocal of the golden ratio). The power spectrum is complement-symmetric and parity-aligned (real for even-weight frequencies, imaginary for odd-weight).

Under Stab(111) × Aut(Z₅), the 240 surjections split into **5 orbits**, the 192 three-type into **3**, and the 16 IC-type into **1**. The predicted 2 orbits appear only when the 互 kernel line H is fixed (Stab(H)∩Stab(111) × Aut(Z₅)). This gives a precise orbit-theoretic formulation of the 0.5-bit.

The CC profiles **do** determine the 互 transition at individual hexagram level, but 互 does not preserve CC classes. The CC is necessary but not sufficient to derive the transition matrix T from pure algebra.

---

## Task 1: Coherent Closure from Z₅ Difference

### Seed Partition (6 classes)

| Class | Description | Size |
|-------|-------------|------|
| 0 | Diagonal {(x,x)} | 8 |
| 1 | d = 0, off-diagonal | 6 |
| 2 | d = 1 | 12 |
| 3 | d = 2 | 13 |
| 4 | d = 3 | 13 |
| 5 | d = 4 | 12 |

### The Seed is NOT a CC

**29 violations** of constant intersection numbers. The root cause: heterogeneous fiber sizes (2,2,2,1,1). Representative violations:

- Class 0 (diagonal), p_{c1,c1}^{c0}: value 1 for 6 points (doubleton fibers), value 0 for 2 points (singleton fibers). Singletons have no same-element partner; doubletons do.
- Class 0, p_{c2,c5}^{c0}: value 2 for 4 points, value 1 for 4 points. Different elements see different numbers of d=1/d=4 pairs.
- Class 1 (d=0 off-diag), p_{c3,c4}^{c1}: value 1 for 2 pairs (Earth within-fiber), value 2 for 4 pairs (Wood/Metal within-fiber).

### Coherent Closure: 28 Classes

**Round 1:** Every seed class splits. The 6 classes become 28 subclasses.
**Round 2:** Stable — no further splitting.

The **28 classes** coincide exactly with the orbits of the **fiber automorphism group** G = ⟨τ_E, τ_W, τ_M⟩ ≅ (Z₂)³ on ordered pairs, where:
- τ_E: 坤(000) ↔ 艮(100) (swap Earth pair)
- τ_W: 震(001) ↔ 巽(110) (swap Wood pair)
- τ_M: 兌(011) ↔ 乾(111) (swap Metal pair)

**Burnside verification:** (64 + 3·36 + 3·16 + 4)/8 = 224/8 = **28 orbits** ✓

### Class Structure

**Diagonal (5 classes, 8 pairs total):**

| Class | Content | Size | Element |
|-------|---------|------|---------|
| 0 | {(坎,坎)} | 1 | Water (singleton) |
| 1 | {(離,離)} | 1 | Fire (singleton) |
| 2 | {(兌,兌),(乾,乾)} | 2 | Metal (doubleton) |
| 3 | {(震,震),(巽,巽)} | 2 | Wood (doubleton) |
| 4 | {(坤,坤),(艮,艮)} | 2 | Earth (doubleton) |

The diagonal sees the full fiber structure: singletons get their own classes, doubletons share.

**Off-diagonal d=0 (3 classes, 6 pairs):**

| Class | Content | Size | XOR mask | Hamming |
|-------|---------|------|----------|---------|
| 5 | Metal same-fiber | 2 | 100 (I) | 1 |
| 6 | Wood same-fiber | 2 | 111 (OMI) | 3 |
| 7 | Earth same-fiber | 2 | 100 (I) | 1 |

Earth and Metal share the same XOR mask (I = 100), but are in different CC classes because the surrounding Z₅ relationships differ. Wood's mask is OMI = 111.

**Off-diagonal d≠0 (20 classes, 50 pairs):** Each Z₅ difference d ∈ {1,2,3,4} splits into 5 classes. The splitting is determined by which specific fibers are the source and target. For d=2 (克):

| Class | Content | Size | Note |
|-------|---------|------|------|
| 13 | (坎→離) | 1 | Water→Fire singleton pair |
| 14 | (離→Metal) | 2 | Fire→{兌,乾} |
| 15 | (Metal→Wood) | 4 | {兌,乾}→{震,巽} |
| 16 | (Wood→Earth) | 4 | {震,巽}→{坤,艮} |
| 17 | (Earth→坎) | 2 | {坤,艮}→Water |

### Commutativity Test: NOT an Association Scheme

**375 out of 378 pairs** of intersection matrices fail to commute. The CC is emphatically not an AS.

**Why:** An AS requires the relation classes to have the same "local structure" everywhere — every vertex sees the same pattern. Here, singletons (Water, Fire) have fundamentally different neighborhoods than doubletons (Earth, Wood, Metal). The heterogeneous fiber partition breaks the homogeneity condition.

### Complement Symmetry

The complement map σ(x) = x ⊕ 111 maps CC classes to CC classes:

**Self-paired classes:**
- Class 3 (diagonal Wood) — σ sends 震↔巽, both Wood
- Class 6 (d=0 Wood) — σ sends (震,巽)↔(巽,震)

**Complement-paired classes (d ↔ −d mod 5):**
- Diagonal: (0,1) Water↔Fire, (2,4) Metal↔Earth
- d=0: (5,7) Metal↔Earth
- d=1↔d=4: (8,24), (9,23), (10,27), (11,26), (12,25)
- d=2↔d=3: (13,19), (14,18), (15,22), (16,21), (17,20)

Under the extended group G ⋊ ⟨σ⟩ (order 16), the 28 classes reduce to **15 orbits**.

---

## Task 2: Difference Table + Walsh-Hadamard Spectrum

### Difference Table

Δ_m(x) = f(x⊕m) − f(x) mod 5:

|  mask  |  坤  |  震  |  坎  |  兌  |  艮  |  離  |  巽  |  乾  |
|--------|------|------|------|------|------|------|------|------|
| 001(O) |   3  |   2  |   4  |   1  |   4  |   1  |   3  |   2  |
| 010(M) |   2  |   3  |   3  |   2  |   3  |   2  |   2  |   3  |
| 011(OM)|   1  |   4  |   1  |   4  |   1  |   4  |   1  |   4  |
| 100(I) |   0  |   1  |   1  |   0  |   0  |   4  |   4  |   0  |
| 101(OI)|   4  |   2  |   4  |   2  |   3  |   1  |   3  |   1  |
| 110(MI)|   3  |   3  |   3  |   3  |   2  |   2  |   2  |   2  |
| 111(OMI)|  1  |   0  |   2  |   4  |   1  |   3  |   0  |   4  |

**Complement equivariance:** Δ_m(~x) = −Δ_m(x) mod 5 **verified** for all 56 entries.

**Notable patterns:**
- Mask OM (011): constant pattern {1,4,1,4,1,4,1,4} — the 生/被生 alternation depends only on b₀
- Mask I (100): contains zeros at Earth and Metal (same-element pairs have Δ=0), and the pattern {0,1,1,0,0,4,4,0} reflects same-fiber structure
- Mask MI (110): only takes values {2,3}, splitting trigrams into P-even ({兌,艮,離,巽}→2) and P-odd ({坤,震,坎,乾}→3)

### Rank over Z₅

**Rank = 3**

The 7×8 difference matrix has rank 3 over Z₅. Since f is determined by 4 values (one per complement pair), with one constraint (Σ values cover Z₅), the rank 3 = dim(F₂³) is the natural maximum for a non-affine function.

### Walsh-Hadamard Spectrum

W_f(ω) = Σ_{x ∈ F₂³} ζ₅^{f(x)} · (−1)^{⟨ω,x⟩} where ζ₅ = e^{2πi/5}

**Exact algebraic forms (coefficients of ζ₅ powers):**

| ω | wt | c₀ | c₁ | c₂ | c₃ | c₄ | W_f exact | |W|² exact |
|---|----|----|----|----|----|----|-----------|-----------|
| 000 | 0 | 2 | 1 | 2 | 2 | 1 | (1−√5)/2 | (3−√5)/2 |
| 001 | 1 | 0 | −1 | 2 | −2 | 1 | 2i(−sin 2π/5 + 2sin 4π/5) | (25−11√5)/2 |
| 010 | 1 | 0 | 1 | 2 | −2 | −1 | 2i(sin 2π/5 + 2sin 4π/5) | (25+5√5)/2 |
| 011 | 2 | −2 | −1 | 2 | 2 | −1 | (−5−3√5)/2 | (35+15√5)/2 |
| 100 | 1 | 0 | −1 | 0 | 0 | 1 | −2i·sin(2π/5) | (5+√5)/2 |
| 101 | 2 | −2 | 1 | 0 | 0 | 1 | (√5−5)/2 | (15−5√5)/2 |
| 110 | 2 | 2 | −1 | 0 | 0 | −1 | (5−√5)/2 | (15−5√5)/2 |
| 111 | 3 | 0 | 1 | 0 | 0 | −1 | 2i·sin(2π/5) | (5+√5)/2 |

### Key Spectral Properties

1. **Parity prediction VERIFIED:** W_f(ω) is real for even-weight ω, purely imaginary for odd-weight ω. This follows from complement equivariance: f(~x) = −f(x) implies the sum splits into symmetric (real) and antisymmetric (imaginary) parts depending on ⟨ω, 111⟩.

2. **Power spectrum lives in Q(√5):** Every |W_f(ω)|² is of the form (a + b√5)/2 with a, b ∈ Z. The golden ratio field Q(√5) = Q(ζ₅ + ζ₅⁻¹) is the maximal real subfield of Q(ζ₅).

3. **W(000) = (1−√5)/2 = −1/φ:** The zero-frequency component equals the negative reciprocal of the golden ratio. Since W(000) = Σ ζ₅^{f(x)}, this is the "total phase" of the 五行 assignment. Its squared magnitude 1/φ² ≈ 0.382 is the smallest power spectrum value.

4. **W(011) dominates:** |W(011)|² = (35+15√5)/2 ≈ 34.27, over half the total power 64. The mask OM = 011 is the 生/被生-exclusive mask. The Walsh spectrum concentrates on the 五行-relation axis.

5. **Parseval check:** Σ|W(ω)|² = (128 + 0·√5)/2 = 64 = 8² ✓. The √5 terms cancel exactly.

6. **Complement pairs in spectrum:** |W(100)|² = |W(111)|² = (5+√5)/2 and |W(101)|² = |W(110)|² = (15−5√5)/2. These equalities follow from wt(ω) + wt(ω⊕111) = const and the complement structure.

### Spectral Hierarchy

| Rank | ω | |W|² | Fraction of total | Interpretation |
|------|---|------|-------------------|----------------|
| 1 | 011 (OM) | 34.27 | 53.5% | 生/被生 axis |
| 2 | 010 (M) | 18.09 | 28.3% | middle-line flip |
| 3 | 100 (I) = 111 (OMI) | 3.62 | 5.7% | fiber bridge / complement |
| 4 | 101 (OI) = 110 (MI) | 1.91 | 3.0% | Q-line / H-line |
| 5 | 000 | 0.38 | 0.6% | DC component |
| 6 | 001 (O) | 0.20 | 0.3% | bottom-line flip |

The spectrum reveals that f is "almost constant" along the O-direction (|W(001)| tiny) and "maximally varying" along the OM-direction. The Fano-line masks {OI, MI} have equal spectral weight, reflecting the P-symmetry between H-line and Q-line.

---

## Task 3: Automorphism Orbits

### Group Sizes

| Group | Order |
|-------|-------|
| GL(3,F₂) | 168 |
| Stab(111) | 24 (≅ S₄) |
| Stab(H-line) ∩ Stab(111) | 8 (≅ D₄; orders {1:1, 2:5, 4:2}) |
| Aut(Z₅) | 4 |
| Stab(111) × Aut(Z₅) | 96 |
| (Stab(H) ∩ Stab(111)) × Aut(Z₅) | 32 |

### Orbit Counts

| Set | Size | Orbits under Stab(111)×Aut(Z₅) | Orbits under (Stab(H)∩Stab(111))×Aut(Z₅) |
|-----|------|-------------------------------|---------------------------------------------|
| All surjections | 240 | **5** | — |
| Three-type {2,2,2,1,1} | 192 | **3** (sizes 48, 96, 48) | — |
| Orbit C (Frame=Type 2) | 96 | **1** | **3** (sizes 32, 32, 32) |
| IC + Alt type combined | 32 | **1** | **2** (sizes 16, 16) |
| IC type (2,0,1,2) | 16 | **1** | **1** |

### The 0.5-Bit: Precise Orbit-Theoretic Formulation

**Result:** Under the full Stab(111) × Aut(Z₅), all 96 Orbit C surjections form a **single orbit**. The 0.5-bit is invisible to this symmetry group.

Under Stab(H)∩Stab(111) × Aut(Z₅) — the residual symmetry when the 互 kernel line H is fixed — Orbit C splits into **3 orbits** of 32, distinguished by H's type (0, 1, or 2).

The 0.5-bit is the choice between:
- **H = Type 0** (Wood on H, IC traditional): 32 surjections in one orbit
- **H = Type 1** (Singletons on H, alternative): 32 surjections in another orbit

These merge under full Stab(111) because **4 elements** of Stab(111) swap the H-pair {1,6} with the Q-pair {2,5}, mapping Type 0 ↔ Type 1.

**Conclusion:** The 0.5-bit is not a symmetry-independent feature. It is the residual freedom after imposing the 互 structure, which fixes a specific Fano line (H) and thereby breaks the S₄ symmetry of Stab(111) down to the 8-element subgroup Stab(H)∩Stab(111).

### Orbit Structure of the 5 Orbits on 240

| Orbit | Size | Shape | Frame type | Prior classification |
|-------|------|-------|-----------|---------------------|
| 0 | 24 | {4,1,1,1,1} | Type 0 | — (2 types only) |
| 1 | 48 | {2,2,2,1,1} | Type 0 | Orbit A |
| 2 | 24 | {4,1,1,1,1} | Type 1 | — (2 types only) |
| 3 | 96 | {2,2,2,1,1} | Type 2 | **Orbit C** (contains IC) |
| 4 | 48 | {2,2,2,1,1} | Type 1 | Orbit B |

The two {4,1,1,1,1} orbits (sizes 24 each) account for all 48 four-type surjections (types {0,1} only). The three {2,2,2,1,1} orbits (48 + 96 + 48 = 192) correspond to Orbits A, C, B with all three types. Orbit C is the largest (96 = 6 sub-assignments × 16), consistent with having 6 possible type distributions for non-Frame pairs.

---

## Task 4a: Can the CC Predict 互 Dynamics?

### 互 Transition Matrix (Cross-Checked)

T[d][d'] raw counts, d(h) → d(互(h)):

| d\d' | 同 | 生 | 克 | 被克 | 被生 | total |
|------|---|---|---|-----|-----|-------|
| 同 | 6 | 2 | 2 | 2 | 2 | 14 |
| 生 | 1 | 2 | 3 | 6 | 0 | 12 |
| 克 | 4 | 0 | 4 | 5 | 0 | 13 |
| 被克 | 4 | 0 | 5 | 4 | 0 | 13 |
| 被生 | 1 | 0 | 6 | 3 | 2 | 12 |

**Cross-check with synthesis-2: EXACT MATCH ✓**

### CC Profiles Determine d' Uniquely

**Key finding:** For every hexagram h, the full CC profile — the tuple of CC classes for all six pairings among {lo, up, nlo, nup} — determines d(互(h)) uniquely.

| d-class | Distinct CC profiles | All determine d'? |
|---------|---------------------|-------------------|
| 同 (d=0) | 14 | ✓ |
| 生 (d=1) | 10 | ✓ |
| 克 (d=2) | 12 | ✓ |
| 被克 (d=3) | 12 | ✓ |
| 被生 (d=4) | 10 | ✓ |

This means the CC contains **enough information** to predict the nuclear Z₅ transition for each individual hexagram. The CC profile acts as a fine-grained fingerprint that resolves all ambiguity in the d→d' mapping.

### But 互 Does NOT Preserve CC Classes

CC(lo,up) = CC(nlo,nup) for only **2 out of 64** hexagrams (3.1%). The nuclear map scrambles the CC class structure almost completely.

The CC-class-to-CC-class transition is many-to-many:
- Class 15 (Metal→Wood, d=2) maps to 4 different target classes
- Class 22 (Earth→Wood, d=3) maps to 4 different target classes
- Only 5 classes map to a single target (deterministic at class level)

### Can T Be Derived from CC Intersection Numbers?

**Answer: Partially, but not simply.**

The CC captures the fiber-pair structure but NOT the bit-level structure that 互 uses. The nuclear map takes lines 2-5 of a hexagram — this is an F₂-linear operation that depends on the actual bit positions, not on which Z₅ elements the trigrams represent.

The CC-profile determination works because each hexagram's CC profile is essentially unique (58 distinct profiles out of 64 hexagrams, with duplicates only within the same d and d'). This is a consequence of the CC being fine-grained (28 classes on 8 elements), not evidence that the CC algebra generates T.

**Specific test:** If T were a CC algebra element, it would be expressible as T = Σ λ_k M_k where M_k are the intersection matrices. The transition T[d][d'] would then be a linear combination of intersection numbers p_{ij}^k. Since 互 does not preserve CC classes, T is NOT in the CC algebra in this sense.

**What the CC can express:** The fiber multiplicities and Z₅ structure. The CC-derived prediction is that T has negation symmetry T[d][d'] = T[−d][−d'] (which it does). But the specific entries of T require knowing the bit-level action of 互, which is outside the CC.

---

## Cross-Cutting Findings

### 1. The CC Is the Fiber Symmetry Partition

The coherent closure of the Z₅-difference relation on F₂³ equals exactly the orbit partition under the fiber automorphism group. This is the **generic** situation for a function with heterogeneous fibers — the CC resolves all fiber structure. 

For a surjection with partition {k₁,...,k_p}, the fiber automorphism group is S_{k₁} × ... × S_{k_p}. At {2,2,2,1,1}, this gives (Z₂)³ × 1 × 1 = (Z₂)³ of order 8, yielding 28 orbits on ordered pairs.

**Implication for "what is the object":** The Z₅ difference is not algebraically self-sufficient — it does not close into an AS or even a homogeneous CC. The object's algebraic identity at the trigram level is: **the orbit CC of (Z₂)³ acting on F₂³ via fiber automorphisms**, equipped with the complement involution σ and the P→H parity cascade.

### 2. The Walsh Spectrum Is Golden

Every spectral value lives in Q(√5), the golden ratio field. This is forced by the ζ₅ structure (Q(ζ₅) has degree 4 over Q, with maximal real subfield Q(√5) of degree 2). The complement-equivariance of f restricts W to real or purely imaginary values, projecting from Q(ζ₅) to Q(√5).

The spectral concentration on mask OM = 011 (53.5% of power) confirms this mask's role as the 五行-relation axis: it produces the maximally non-constant behavior of f under XOR.

### 3. The 0.5-Bit Is a Symmetry-Breaking Effect

The 0.5-bit is invisible to the full point-stabilizer symmetry Stab(111). It emerges specifically when the 互 kernel line H is fixed, reducing the symmetry from |Stab(111)| = 24 to |Stab(H)∩Stab(111)| = 8. The 4 H↔Q swapping elements of Stab(111) are precisely what absorbs the 0.5-bit.

**Hierarchy:**

| Symmetry group | Order | Orbits on Orbit C | 0.5-bit visible? |
|---------------|-------|-------------------|-------------------|
| Stab(111) × Aut(Z₅) | 96 | 1 | No |
| (Stab(H)∩Stab(111)) × Aut(Z₅) | 32 | 3 | Yes (3 orbits) |
| Aut(Z₅) alone | 4 | 24 | Yes |
| Trivial | 1 | 96 | Yes |

The 0.5-bit sits exactly at the boundary where 互-structure breaks point-stabilizer symmetry.

### 4. The CC Sees 互 But Cannot Generate It

The CC profiles predict individual hexagram transitions (Task 4a), but this is because the CC is fine enough (28 classes on 8 elements) to almost distinguish individual pairs. The prediction is empirically total but algebraically accidental — it reflects the CC's resolution power, not a structural relationship between the CC algebra and the 互 dynamics.

The fundamental mismatch: the CC encodes Z₅ fiber structure (a non-linear invariant), while 互 is an F₂-linear operation (a bit-level map). Their interaction is mediated by the specific encoding of trigrams, not by any algebraic bridge between Z₅ and F₂.

---

## Raw Data

### Exact Power Spectrum

| ω | |W_f(ω)|² | Decimal |
|---|----------|---------|
| 000 | (3−√5)/2 = 1/φ² | 0.3820 |
| 001 | (25−11√5)/2 | 0.2016 |
| 010 | 5(5+√5)/2 = 5φ² | 18.090 |
| 011 | (35+15√5)/2 | 34.271 |
| 100 | (5+√5)/2 = φ+2 | 3.618 |
| 101 | (15−5√5)/2 = 5/φ² | 1.910 |
| 110 | (15−5√5)/2 = 5/φ² | 1.910 |
| 111 | (5+√5)/2 = φ+2 | 3.618 |

Where φ = (1+√5)/2 is the golden ratio.

### Parseval Check

Σ |W|² = (3−√5 + 25−11√5 + 25+5√5 + 35+15√5 + 5+√5 + 15−5√5 + 15−5√5 + 5+√5)/2
= (128 + 0·√5)/2 = **64 = 8²** ✓

### Files

- `cc_identity.py` — computation script (Tasks 1–4a)
- `cc_identity_output.txt` — full computation output
- `cc_identity_results.md` — this document
