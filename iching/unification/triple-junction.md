# The Triple Junction: Three Numberings of Five Elements

## The Three Windows

Three numbering systems assign integers to the five elements. Each makes different structure visible. Each was discovered independently — two by the tradition, one by this research.

| Numbering | Assignment | What it captures |
|-----------|-----------|-----------------|
| **He Tu** (河圖 mod 5) | Earth=0, Water=1, Fire=2, Wood=3, Metal=4 | Cosmogonic order — what emerged when |
| **Lo Shu** (洛書 odds) | Water=1, Wood=3, Earth=5, Metal=7, Fire=9 | Spatial arrangement — where things sit |
| **Algebraic** (生-cycle Z₅) | Wood=0, Fire=1, Earth=2, Metal=3, Water=4 | Relational dynamics — how things interact |

---

## He Tu: Genesis (primes 2 × 5)

```
天一生水    Heaven 1 generates Water
地二生火    Earth  2 generates Fire
天三生木    Heaven 3 generates Wood
地四生金    Earth  4 generates Metal
天五生土    Heaven 5 generates Earth/Soil
```

Each element has a generation number (1–5) and a completion number (6–10), differing by 5. Odd = 天 (Heaven/Yang). Even = 地 (Earth/Yin). The pairing {n, n+5} encodes yin-yang duality within each element.

The sequence Water → Fire → Wood → Metal → Earth is the cosmogonic order — neither the 生 cycle nor the 克 cycle. It describes *emergence*, not *interaction*.

Mod 5, the He Tu numbers give a Z₅ structure: Earth=0, Water=1, Fire=2, Wood=3, Metal=4. The complement operation (negation) on this ring is **not affine** — proven by exhaustive search of all 25 affine maps (R42). The conjugation γ = [3,2,0,4,1] between He Tu and algebraic Z₅ is a pure permutation with no algebraic structure.

Prime content: 5 (five elements) × 2 (yin-yang alternation of 天/地).

## Lo Shu: Space (primes 3 × 5)

```
4  9  2
3  5  7
8  1  6
```

The 3×3 magic square. Elements placed by compass direction: North=Water=1, South=Fire=9, East=Wood=3, West=Metal=7, Center=Earth=5. These are the odd (天) He Tu numbers arranged spatially.

Magic constant = 15 = 3 × 5. Every row, column, and diagonal sums to the meeting point of primes 3 and 5. Diametrically opposite pairs sum to 10 through center 5.

The Lo Shu is NOT a mod-5 encoding of the He Tu — only 2/8 non-center positions match He Tu element numbers mod 5. The Lo Shu encodes spatial balance, not cosmogonic order.

Prime content: 5 (five elements) × 3 (3×3 grid, magic constant 15).

## Algebraic: Dynamics (prime 5)

Wood=0 is forced by complement equivariance: the self-complementary pair {震, 巽} both map to Wood, so f(震) = −f(巽) = −f(震), giving 2w ≡ 0 mod 5, thus w = 0.

Once Wood = 0, the 生 cycle determines everything:

```
生 (stride 1): Wood(0) → Fire(1) → Earth(2) → Metal(3) → Water(4)
克 (stride 2): Wood(0) → Earth(2) → Water(4) → Fire(1) → Metal(3)
```

The two fundamental cycles become constant strides on Z₅. Complement = negation: f(x⊕111) = −f(x) mod 5. This is the unique labeling (up to Aut(Z₅)) where the relational dynamics are algebraically transparent.

Prime content: 5 (pure Z₅ cycle structure). No yin-yang alternation (prime 2). No spatial grid (prime 3). Pure dynamics.

---

## The Incommensurability (R42)

The three numberings are **not reducible to each other**.

The He Tu Z₅ and the algebraic Z₅ generate the same dihedral group D₅ under {生-step, complement}. They are conjugate as *group actions* — the same symmetry group acts on both. But the conjugation γ is non-affine: no map ax + b mod 5 connects them. They are incommensurable as *ring structures*.

| Property | Algebraic Z₅ | He Tu Z₅ |
|----------|-------------|----------|
| Complement | = negation (−x mod 5) | ≠ negation (non-affine) |
| 生 cycle | stride 1 (constant) | stride varies |
| Group generated | D₅ | D₅ |
| Connected by | γ = [3,2,0,4,1] (non-affine permutation) | |

The Lo Shu numbers (1,3,5,7,9) don't even live in Z₅ — they're odd integers with a magic-square constraint. They encode spatial harmony, not cyclic dynamics.

Three systems, three mathematical structures, no algebraic bridge between any pair.

---

## The Three Pairing Characters

Each numbering system induces a different pairing of elements, with different relational character:

| System | Pairing rule | 生 | 克 | 比和 | Character |
|--------|-------------|-----|-----|------|-----------|
| He Tu | (n, n+5) | 3 | 1 | 0 | Generative |
| 先天 | (n, 9−n) | 2 | 1 | 1 | Retrograde |
| Lo Shu | (n, 10−n) | 0 | 3 | 1 | Destructive |

He Tu pairs are almost pure 生 — a cosmogony that generates. Lo Shu pairs are pure 克 — a spatial arrangement that constrains. The 先天 arrangement sits between, with retrograde character.

Wood is the unique element bridging the 克/生 boundary in all three systems. Its He Tu pair includes the only 克 relationship in an otherwise generative system. In the algebraic Z₅, it occupies 0 — the self-complementary fixed point.

---

## The Triple Junction

```
          He Tu (2 × 5)
         genesis / emergence
              /\
             /  \
            /    \
           / 後天 \
          /________\
Lo Shu (3 × 5)    Algebraic (5)
space / balance    dynamics / relation
```

The 後天 (Later Heaven) compass arrangement is the unique point where all three systems converge — the triple junction of primes {2, 3, 5}.

- From prime 2: the 後天 satisfies yin-yang balance constraints (He Tu face)
- From prime 3: the 後天 sits on the Lo Shu magic square (Lo Shu face)
- From prime 5: the 後天 respects 五行 relational structure (algebraic face)

The 後天 was proven to be the unique arrangement surviving all three constraint sets simultaneously: 96 → 8 → 2 → 1 (R36, R37). Each face contributes independent constraints. The junction is a single point — not a region, not a family.

---

## What the Tradition Had, and What It Didn't

The tradition possessed two vertices of the triangle:

- **He Tu**: the cosmogonic ordering with yin-yang pairing (attested ~Han dynasty or earlier)
- **Lo Shu**: the spatial magic square with directional element placement (attested ~Han dynasty or earlier)

The tradition also knew the 生 and 克 cycles — Wood generates Fire, Wood destroys Earth, etc. But it expressed them as *named relationships between elements*, not as *constant strides on a cyclic group*. The step from "Wood generates Fire" to "generation = stride 1 on Z₅" was never taken.

The algebraic numbering makes three things explicit that the tradition left implicit:

1. **Wood = 0 is forced**, not chosen. The complement equivariance condition f(x⊕111) = −f(x) has exactly one solution for the self-complementary element.

2. **生 and 克 are the same operation at different speeds.** Stride 1 and stride 2 on the same cyclic group. The tradition treated them as qualitatively different; the algebra shows they're quantitatively related.

3. **The assignment is unique.** Given the binary trigram structure and the five-element relational structure, there is exactly one way to connect them (up to symmetry). The tradition inherited the assignment; the algebra proves it couldn't have been otherwise.

The algebraic vertex completes the triangle. Genesis, space, and dynamics — three faces of the same five elements, each carrying different prime information, meeting at the 後天 compass.

---

## References

- R32: Zero free parameters in 五行 assignment (`deep/01_assignment_test.py`)
- R36, R37: 先天 = Z₂ optimum, 後天 = {2,3,5} triple junction (`deep/exploration-log.md`, iterations 2–3)
- R42: Two Z₅ incommensurability (`deep/01_assignment_test.py`)
- Synthesis-3 §I: The uniqueness theorem, complement equivariance
- `deep/number-structure.md`: The {2, 3, 5} prime architecture
- `opposition-theory/loshu.md`: Lo Shu–He Tu–先天 pairing analysis
