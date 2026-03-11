# Hexagram 五行 Relation Algebra: Complete Results

All analysis uses the complement-respecting 五行 surjection with Wood=0 in Z₅
(生-cycle numbering: Wood=0, Fire=1, Earth=2, Metal=3, Water=4).
d = f(upper) − f(lower) mod 5 determines the 五行 relation.

---

## Task 1: Z₅ × Z₅ Hexagram Relation Matrix

### 8×8 trigram-pair Z₅ difference matrix

d = f(upper) − f(lower) mod 5.  Rows = lower trigram, Cols = upper trigram.

| Lower\Upper | 坤 | 震 | 坎 | 兌 | 艮 | 離 | 巽 | 乾 |
|---|---|---|---|---|---|---|---|---|
| **坤** (Earth) | 0(同) | 3(被) | 2(克) | 1(生) | 0(同) | 4(被) | 3(被) | 1(生) |
| **震** (Wood) | 2(克) | 0(同) | 4(被) | 3(被) | 2(克) | 1(生) | 0(同) | 3(被) |
| **坎** (Water) | 3(被) | 1(生) | 0(同) | 4(被) | 3(被) | 2(克) | 1(生) | 4(被) |
| **兌** (Metal) | 4(被) | 2(克) | 1(生) | 0(同) | 4(被) | 3(被) | 2(克) | 0(同) |
| **艮** (Earth) | 0(同) | 3(被) | 2(克) | 1(生) | 0(同) | 4(被) | 3(被) | 1(生) |
| **離** (Fire) | 1(生) | 4(被) | 3(被) | 2(克) | 1(生) | 0(同) | 4(被) | 2(克) |
| **巽** (Wood) | 2(克) | 0(同) | 4(被) | 3(被) | 2(克) | 1(生) | 0(同) | 3(被) |
| **乾** (Metal) | 4(被) | 2(克) | 1(生) | 0(同) | 4(被) | 3(被) | 2(克) | 0(同) |

### Relation counts

| d | Relation | Count | Fraction |
|---|----------|-------|----------|
| 0 | 同 | 14 | 0.2188 |
| 1 | 生 | 12 | 0.1875 |
| 2 | 克 | 13 | 0.2031 |
| 3 | 被克 | 13 | 0.2031 |
| 4 | 被生 | 12 | 0.1875 |

**同 count verification:** 14 = 8 (self-pairs) + 6 (cross: 2×C(2,2) for Wood,Earth,Metal + 0 for Fire,Water)
  Wood×Wood: 2×2=4, Earth×Earth: 2×2=4, Metal×Metal: 2×2=4, Fire×Fire: 1, Water×Water: 1 → total = 14 ✓

### d determined by position or orbit?

The factored basis splits hexagram h into (pos, orb) where:
- pos = lower trigram (bits 0-2)
- orb = lower XOR upper = palindromic signature (bits 3-5 XOR bits 0-2)

**Same orbit (XOR mask), different d?**

  Mask 001: d values = [1, 2, 3, 4] (e.g., 震×坤→d=2, 坤×震→d=3)
  Mask 010: d values = [2, 3] (e.g., 坎×坤→d=3, 兌×震→d=2)
  Mask 011: d values = [1, 4] (e.g., 兌×坤→d=4, 坎×震→d=1)
  Mask 100: d values = [0, 1, 4] (e.g., 艮×坤→d=0, 離×震→d=4)
  Mask 101: d values = [1, 2, 3, 4] (e.g., 離×坤→d=1, 艮×震→d=3)
  Mask 110: d values = [2, 3] (e.g., 巽×坤→d=2, 乾×震→d=2)
  Mask 111: d values = [0, 1, 2, 3, 4] (e.g., 乾×坤→d=4, 巽×震→d=0)

**Masks with constant d (all lower trigrams give same relation):**
  Mask 000 (坤): always d=0 (同)

**Masks with variable d:** 7/8
**Masks with constant d:** 1/8

**Conclusion:** d depends on BOTH the lower trigram and the XOR mask.
The 五行 relation is NOT determined by orbit alone (because f is non-linear).
Only mask=000 gives constant d=0 (同).

---

## Task 2: 五行 Relations Under 互 — Z₅ Perspective

### Transition matrix: d(h) → d(互(h))

| d(h)\d(互) | 0(同) | 1(生) | 2(克) | 3(被克) | 4(被生) | Total |
|---|---|---|---|---|---|---|
| **0(同)** | 6 | 2 | 2 | 2 | 2 | 14 |
| **1(生)** | 1 | 2 | 3 | 6 | 0 | 12 |
| **2(克)** | 4 | 0 | 4 | 5 | 0 | 13 |
| **3(被克)** | 4 | 0 | 5 | 4 | 0 | 13 |
| **4(被生)** | 1 | 0 | 6 | 3 | 2 | 12 |
| **Nuclear** | 16 | 4 | 20 | 20 | 4 | 64 |

### Is d(互(h)) = c × d(h) mod 5?

  c=0: 16/64 match (25.0%)
  c=1: 18/64 match (28.1%)
  c=2: 12/64 match (18.8%)
  c=3: 18/64 match (28.1%)
  c=4: 16/64 match (25.0%)

**Conclusion:** No single constant c makes d(互(h)) = c·d(h) mod 5.
The nuclear map is NOT a Z₅-linear operation on the relation index.

### Structure of the transition

**Conditioning on P-parity of lower trigram:**

  P-parity = 0:
    | d(h)\d(互) | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | 0 | 4 | 2 | 0 | 0 | 2 |
    | 1 | 0 | 0 | 1 | 5 | 0 |
    | 2 | 2 | 0 | 2 | 2 | 0 |
    | 3 | 2 | 0 | 2 | 2 | 0 |
    | 4 | 0 | 0 | 5 | 1 | 0 |
    (32 hexagrams)

  P-parity = 1:
    | d(h)\d(互) | 0 | 1 | 2 | 3 | 4 |
    |---|---|---|---|---|---|
    | 0 | 2 | 0 | 2 | 2 | 0 |
    | 1 | 1 | 2 | 2 | 1 | 0 |
    | 2 | 2 | 0 | 2 | 3 | 0 |
    | 3 | 2 | 0 | 3 | 2 | 0 |
    | 4 | 1 | 0 | 1 | 2 | 2 |
    (32 hexagrams)

### Transition matrix structure analysis

**Symmetry check:**
  Negation symmetry T[d][d'] = T[-d][-d']: ✓

**Cross-check with existing findings:**
  Same transition matrix as in framework_strengthening_findings.md: ✓ MATCH

---

## Task 3: P/H/Q Parity vs Z₅ Difference

### P-parity of lower trigram vs d

| d | Relation | P=0 | P=1 | Total | P=0 frac |
|---|----------|------|------|-------|-----------|
| 0 | 同 | 8 | 6 | 14 | 0.5714 |
| 1 | 生 | 6 | 6 | 12 | 0.5000 |
| 2 | 克 | 6 | 7 | 13 | 0.4615 |
| 3 | 被克 | 6 | 7 | 13 | 0.4615 |
| 4 | 被生 | 6 | 6 | 12 | 0.5000 |

### H-parity of lower trigram vs d

| d | Relation | H=0 | H=1 | Total | H=0 frac |
|---|----------|------|------|-------|-----------|
| 0 | 同 | 8 | 6 | 14 | 0.5714 |
| 1 | 生 | 5 | 7 | 12 | 0.4167 |
| 2 | 克 | 7 | 6 | 13 | 0.5385 |
| 3 | 被克 | 7 | 6 | 13 | 0.5385 |
| 4 | 被生 | 5 | 7 | 12 | 0.4167 |

### Q-parity of lower trigram vs d

| d | Relation | Q=0 | Q=1 | Total | Q=0 frac |
|---|----------|------|------|-------|-----------|
| 0 | 同 | 6 | 8 | 14 | 0.4286 |
| 1 | 生 | 7 | 5 | 12 | 0.5833 |
| 2 | 克 | 6 | 7 | 13 | 0.4615 |
| 3 | 被克 | 6 | 7 | 13 | 0.4615 |
| 4 | 被生 | 7 | 5 | 12 | 0.5833 |

### The P-parity theorem in Z₅ language

**Note:** The tables above show P/H/Q-parity of the **lower trigram alone**,
which is approximately uniform. The meaningful quantity is P-parity of the
**XOR mask** (= P(lower) ⊕ P(upper)), which measures whether lower and upper
trigrams have the SAME P-parity. This is computed below.

### Algebraic relationship

Is there a function g: Z₅ → Z₂ such that P-parity ≈ g(d)?

**P-parity of XOR mask vs d:**

| d | Relation | P(mask)=0 | P(mask)=1 | P(mask)=0 frac |
|---|----------|-----------|-----------|----------------|
| 0 | 同 | 14 | 0 | 1.0000 |
| 1 | 生 | 8 | 4 | 0.6667 |
| 2 | 克 | 1 | 12 | 0.0769 |
| 3 | 被克 | 1 | 12 | 0.0769 |
| 4 | 被生 | 8 | 4 | 0.6667 |

**Key insight:** P(mask) = P(lower) ⊕ P(upper), so P(mask)=0 means
lower and upper have the SAME P-parity. The 100% for 同 means
same-element trigrams always have the same P-parity — this is the
P-coset alignment theorem from synthesis-1.md.

**Connection to exclusive masks:**

Each 五行 relation has exclusive XOR masks with fixed P-parity:
- 同 exclusive mask: id(000) → P(mask)=0
- 生 exclusive mask: OM(011) → P(mask)=0
- 克 exclusive masks: M(010), MI(110) → P(mask)=1

Non-exclusive masks dilute the relationship, which is why
同 is 100% P-even but 克 is only 92% P-odd (one exception).

---

## Task 4: 先天/後天 Orderings and Z₅ Relations

### 先天 (Fu Xi) circular ordering

| Position | Trigram | Element (Z₅) |
|----------|--------|-------------|
| 0 | 乾 (111) | Metal (3) |
| 1 | 巽 (110) | Wood (0) |
| 2 | 離 (101) | Fire (1) |
| 3 | 艮 (100) | Earth (2) |
| 4 | 坤 (000) | Earth (2) |
| 5 | 震 (001) | Wood (0) |
| 6 | 坎 (010) | Water (4) |
| 7 | 兌 (011) | Metal (3) |

| Step | From → To | d (fwd) | Relation | d (rev) | Relation |
|------|-----------|---------|----------|---------|----------|
| 0→1 | 乾→巽 | 2 | 克 | 3 | 被克 |
| 1→2 | 巽→離 | 1 | 生 | 4 | 被生 |
| 2→3 | 離→艮 | 1 | 生 | 4 | 被生 |
| 3→4 | 艮→坤 | 0 | 同 | 0 | 同 |
| 4→5 | 坤→震 | 3 | 被克 | 2 | 克 |
| 5→6 | 震→坎 | 4 | 被生 | 1 | 生 |
| 6→7 | 坎→兌 | 4 | 被生 | 1 | 生 |
| 7→0 | 兌→乾 | 0 | 同 | 0 | 同 |

Z₅ step multiset (forward): {0: 2, 1: 2, 2: 1, 3: 1, 4: 2}

### 後天 (King Wen) circular ordering

| Position | Trigram | Element (Z₅) |
|----------|--------|-------------|
| 0 | 坎 (010) | Water (4) |
| 1 | 艮 (100) | Earth (2) |
| 2 | 震 (001) | Wood (0) |
| 3 | 巽 (110) | Wood (0) |
| 4 | 乾 (111) | Metal (3) |
| 5 | 兌 (011) | Metal (3) |
| 6 | 離 (101) | Fire (1) |
| 7 | 坤 (000) | Earth (2) |

| Step | From → To | d (fwd) | Relation | d (rev) | Relation |
|------|-----------|---------|----------|---------|----------|
| 0→1 | 坎→艮 | 3 | 被克 | 2 | 克 |
| 1→2 | 艮→震 | 3 | 被克 | 2 | 克 |
| 2→3 | 震→巽 | 0 | 同 | 0 | 同 |
| 3→4 | 巽→乾 | 3 | 被克 | 2 | 克 |
| 4→5 | 乾→兌 | 0 | 同 | 0 | 同 |
| 5→6 | 兌→離 | 3 | 被克 | 2 | 克 |
| 6→7 | 離→坤 | 1 | 生 | 4 | 被生 |
| 7→0 | 坤→坎 | 2 | 克 | 3 | 被克 |

Z₅ step multiset (forward): {0: 2, 1: 1, 2: 1, 3: 4}

### Comparison of Z₅ step multisets

| d | 先天 count | 後天 count |
|---|-----------|-----------|
| 0 (同) | 2 | 2 |
| 1 (生) | 2 | 1 |
| 2 (克) | 1 | 1 |
| 3 (被克) | 1 | 4 |
| 4 (被生) | 2 | 0 |

**Same multiset?** No

### 先天 hexagram arrangement: Z₅ difference matrix

Lower trigram = row (先天 order), Upper = column (先天 order).
Entry = d = f(upper) - f(lower) mod 5.

| | 乾 | 巽 | 離 | 艮 | 坤 | 震 | 坎 | 兌 |
|---|---|---|---|---|---|---|---|---|
| **乾** | 0 | 2 | 3 | 4 | 4 | 2 | 1 | 0 |
| **巽** | 3 | 0 | 1 | 2 | 2 | 0 | 4 | 3 |
| **離** | 2 | 4 | 0 | 1 | 1 | 4 | 3 | 2 |
| **艮** | 1 | 3 | 4 | 0 | 0 | 3 | 2 | 1 |
| **坤** | 1 | 3 | 4 | 0 | 0 | 3 | 2 | 1 |
| **震** | 3 | 0 | 1 | 2 | 2 | 0 | 4 | 3 |
| **坎** | 4 | 1 | 2 | 3 | 3 | 1 | 0 | 4 |
| **兌** | 0 | 2 | 3 | 4 | 4 | 2 | 1 | 0 |

**Diagonal (同) entries:** main diagonal is always 0 (同). ✓

**Anti-diagonal (complement pairs):**
  乾×兌: d=0 (同)
  巽×坎: d=4 (被生)
  離×震: d=4 (被生)
  艮×坤: d=0 (同)

**Structural insight:** The 8×8 matrix is the 5×5 Z₅ Cayley subtraction table
expanded by fiber multiplicities. Same-element trigrams produce identical rows/columns:
- 乾 and 兌 (Metal): identical rows
- 巽 and 震 (Wood): identical rows
- 艮 and 坤 (Earth): identical rows
The collapsed 5×5 table is simply d_{ab} = b − a mod 5 — the Z₅ group operation.

### 後天 step pattern — 被克 dominance

The 後天 arrangement has 4/8 steps with d=3 (被克 = reverse-克 = stride-3 on Z₅).
The 2 同-steps join same-element pairs (震/巽=Wood, 乾/兌=Metal).
The remaining 2 steps are d=1 (生) and d=2 (克).
The 先天 arrangement distributes steps more evenly across all five Z₅ values.
This asymmetry is a Z₅ signature of the 先天→後天 transition.

---

## Task 5: Complement, Reversal, and Z₅

### Complement: d(~h) vs d(h)

**Theorem.** d(~h) = −d(h) mod 5.

*Proof.* ~h = (~lower, ~upper). By complement-respecting property,
f(~x) = −f(x) mod 5. So d(~h) = f(~upper) − f(~lower) = 
(−f(upper)) − (−f(lower)) = −(f(upper) − f(lower)) = −d(h). ∎

**Computational verification:** ✓ ALL 64 match

**Consequence:** Complement maps 五行 relations as:
- 同 (d=0) → 同 (d=0): same relation preserved
- 生 (d=1) → 被生 (d=4): generation reverses
- 克 (d=2) → 被克 (d=3): conquest reverses
- 被克 (d=3) → 克 (d=2): conquest reverses
- 被生 (d=4) → 生 (d=1): generation reverses

### Reversal: d(h̄) vs d(h)

**Claim.** d(h̄) = −d(h) mod 5 (same as complement).

*Proof.* h̄ reverses L₁...L₆ → L₆...L₁. The lower trigram of h̄ is
the upper trigram of h (reversed), and vice versa. So
d(h̄) = f(lower(h)) − f(upper(h)) = −d(h). ∎

**Computational verification:** ✗ FAIL

**Wait — correction needed.** Reversal doesn't simply swap lower and upper.
It reverses the LINE order, so lower(h̄) = reverse(upper(h)) and
upper(h̄) = reverse(lower(h)). Since f is NOT reverse-invariant in general,
d(h̄) ≠ −d(h) in general.

**Proper verification:** d(h̄) = −d(h) in 24/64 cases

**Counterexamples (d(h̄) ≠ −d(h)):**

| h | lower×upper | d(h) | h̄ | lower×upper | d(h̄) | −d(h) |
|---|------------|------|-----|------------|-------|-------|
| 000001 | 震×坤 | 2 | 100000 | 坤×艮 | 0 | 3 |
| 000011 | 兌×坤 | 4 | 110000 | 坤×巽 | 3 | 1 |
| 000100 | 艮×坤 | 0 | 001000 | 坤×震 | 3 | 0 |
| 000110 | 巽×坤 | 2 | 011000 | 坤×兌 | 1 | 3 |
| 001000 | 坤×震 | 3 | 000100 | 艮×坤 | 0 | 2 |
| 001010 | 坎×震 | 1 | 010100 | 艮×坎 | 2 | 4 |
| 001100 | 艮×震 | 3 | 001100 | 艮×震 | 3 | 2 |
| 001101 | 離×震 | 4 | 101100 | 艮×離 | 4 | 1 |
| 001110 | 巽×震 | 0 | 011100 | 艮×兌 | 1 | 0 |
| 001111 | 乾×震 | 2 | 111100 | 艮×乾 | 1 | 3 |
| ... | ... | ... | ... | ... | ... | ... |

### Reverse-complement (錯綜): d(~h̄) vs d(h)

d(~h̄) = d(h) in 24/64 cases

### King Wen pairing and Z₅

KW pairs hexagrams by reversal (or complement for palindromes).
For each KW pair (h, h'), check d(h) vs d(h'):

**KW pairs where d(partner) = −d(h):** 14/32

  Non-palindrome pairs (reversal): 28
    d(h̄) = −d(h): 10/28
  Palindrome pairs (complement): 4
    d(~h) = −d(h): 4/4 (should be 100%)

### Reversal and the 五行 map

For a trigram x = b₂b₁b₀, its reversal is x̃ = b₀b₁b₂.
The 五行 map of reversed trigrams:

| x | x̃ | f(x) | f(x̃) | f(x̃)−f(x) mod 5 |
|---|---|------|------|-----------------|
| 坤(000) | 坤(000) | 2(Earth) | 2(Earth) | 0 |
| 震(001) | 艮(100) | 0(Wood) | 2(Earth) | 2 |
| 坎(010) | 坎(010) | 4(Water) | 4(Water) | 0 |
| 兌(011) | 巽(110) | 3(Metal) | 0(Wood) | 2 |
| 艮(100) | 震(001) | 2(Earth) | 0(Wood) | 3 |
| 離(101) | 離(101) | 1(Fire) | 1(Fire) | 0 |
| 巽(110) | 兌(011) | 0(Wood) | 3(Metal) | 3 |
| 乾(111) | 乾(111) | 3(Metal) | 3(Metal) | 0 |

**Palindromic trigrams** (x = x̃): ['坤', '坎', '離', '乾']
**Non-palindromic pairs:** [('震', '艮'), ('兌', '巽')]

**Reversal permutation on Z₅:**
  f(x) → f(x̃) images: {'Earth': {'Earth', 'Wood'}, 'Wood': {'Earth', 'Metal'}, 'Water': {'Water'}, 'Metal': {'Wood', 'Metal'}, 'Fire': {'Fire'}}

  **Well-defined permutation on Z₅?** No — reversal mixes elements

  This means trigram reversal does NOT induce a function on Z₅.
  For doubleton fibers, reversal may send the two trigrams to
  DIFFERENT elements. This is why d(h̄) ≠ −d(h) in general.

  **Fiber-splitting by reversal:**
    Wood: ['震', '巽'] → ['Earth', 'Metal'] (SPLIT!)
    Fire: ['離'] → ['Fire'] (preserved)
    Earth: ['坤', '艮'] → ['Earth', 'Wood'] (SPLIT!)
    Metal: ['兌', '乾'] → ['Wood', 'Metal'] (SPLIT!)
    Water: ['坎'] → ['Water'] (preserved)

---

## Synthesis: What the Z₅ Language Reveals

### 1. The 五行 relation d is genuinely non-linear
d depends on both the lower trigram and the XOR mask (orbit).
Only mask=000 gives constant d=0. The non-linearity of the 五行 map
prevents d from being an orbit-only quantity.

### 2. The 互 transition is NOT Z₅-linear but concentrates onto {0,2,3}
No constant c makes d(互(h)) = c·d(h) mod 5. The transition
matrix has negation symmetry T[d][d'] = T[−d][−d'] (from complement
equivariance) but is otherwise non-algebraic on Z₅.
However, 互 strongly concentrates the output: nuclear d lands in
{0,2,3} = {同,克,被克} with probability 56/64 = 87.5%, while
{1,4} = {生,被生} receive only 8/64 = 12.5%. This is the 克 amplification
(1.538×) restated in Z₅ language: 互 maps the relation space toward the
克/被克 axis (stride-2 on Z₅) and away from the 生/被生 axis (stride-1).

### 3. P-parity is the Z₅ shadow of the F₂ structure
The P-parity theorem (同=100% P-even, 克=92% P-odd) is
the nearest thing to a Z₅→Z₂ homomorphism: d mod 2 approximately
determines P(mask). The exclusive masks explain the exact distribution.

### 4. Complement negates d; reversal does NOT
Complement is a clean Z₅ operation (d → −d) because f(~x) = -f(x).
Reversal splits doubleton fibers: 震(Wood)↔艮(Earth) and 兌(Metal)↔巽(Wood)
swap elements under reversal. Only palindromic trigrams (坤,坎,離,乾) and
singletons (坎,離) are preserved. This means reversal does NOT induce a
function on Z₅, and d(h̄) = −d(h) holds in only 24/64 cases.
This is the precise algebraic statement of the synthesis-1 result that
complement descends to Z₅ but reversal does not.

### 5. The KW pairing lives at the reversal/complement boundary
KW pairs non-palindromes by reversal (NOT Z₅-clean) and palindromes
by complement (Z₅-clean). The 4 palindrome pairs have d → −d exactly.
The 28 reversal pairs break this: d(h̄) ≠ −d(h) in general,
because the 五行 map is not reversal-invariant.
