# The Number Structure: 2, 3, 5

The hexagram system rests on three prime numbers. Each generates a different kind of structure. Their interactions produce the system's architecture.

---

## The Three Primes

**2 — polarity.** Yin/yang. The atomic unit. Generates all binary structures: lines (Z₂), bigrams (Z₂²), trigrams (Z₂³ = 8), hexagrams (Z₂⁶ = 64). Boolean algebra: complement, XOR, Hamming distance. Everything combinatorial.

**3 — position.** The trigram has 3 lines. The hexagram has 6 = 2×3. The Lo Shu is 3×3. Three is the structural dimension — how many positions exist, how the hexagram decomposes into layers (outer/middle/interface, or upper/lower trigrams with shared nuclear zone). Position creates geometry.

**5 — relation.** The 五行 elements. 生 (stride-1) and 克 (stride-2) on Z₅. Five is the relational dimension — not what things are, but how they interact. Relation creates dynamics.

---

## Why 5?

5 is the smallest odd prime where two independent non-degenerate cycles coexist on Z_n:

| n | stride-1 (生) | stride-2 (克) | Viable? |
|---|---|---|---|
| 3 | full cycle | stride-2 ≡ stride-(-1) = reverse of stride-1 | No — 生 and 克 collapse |
| 4 | full cycle | period 2 (visits only 2 of 4) | No — 克 degenerates |
| **5** | **full cycle** | **full cycle, independent of stride-1** | **Yes** |
| 7 | full cycle | full cycle | Yes, but 7 > 8 trigrams → degenerate partition |

5 is forced by the requirement that 生 and 克 be genuinely different operations on the same ring, and that the ring be coverable by ≤ 8 trigrams.

---

## How 2 Meets 5: The Projection

The trigram→element map:

```
Z₂³ (8 trigrams) → Z₅ (5 elements)
```

Partition: {2, 2, 2, 1, 1}

| Element | Trigrams | Count |
|---|---|---|
| Wood | 震 (100), 巽 (011) | 2 |
| Fire | 離 (101) | 1 |
| Earth | 坤 (000), 艮 (001) | 2 |
| Metal | 乾 (111), 兌 (110) | 2 |
| Water | 坎 (010) | 1 |

**This map is not a group homomorphism.** gcd(8, 5) = 1. There is no structural morphism from Z₂³ to Z₅. The map is a set function — heavily constrained (1.75 of 2.25 bits forced by parity, complement closure, Hamming geometry) but not a natural algebraic arrow.

The two number systems are **coprime and incommensurable**. They coexist in the hexagram but cannot be derived from each other.

---

## The Fire/Water Bridge

Fire (離 = 101) and Water (坎 = 010) are the **singletons** — the only elements with exactly 1 trigram each. At these two points, the projection Z₂³ → Z₅ is injective. Knowing the element tells you the exact trigram. No fiber, no ambiguity.

Fire and Water are where Z₂ and Z₅ perfectly coincide. Every other element has a 2-trigram fiber where binary information is lost.

What accumulates at this junction:

| Structure | Fire/Water role |
|---|---|
| Z₂³ | Binary complements (離 ↔ 坎, Hamming distance 3, maximal) |
| Z₅ | 克-related (Water 克 Fire, stride-2) |
| 互 dynamics | Cycle attractor (既濟/未濟 = Water×Fire / Fire×Water) |
| V₄ involutions | Complement and reverse coincide (both swap Fire ↔ Water). V₄ degenerates to Z₂ on this pair. complement∘reverse = identity on 既濟/未濟. |
| 後天八卦 | North-South axis (坎=N, 離=S) |
| Lo Shu | Extremes of 1-9 (坎=1, 離=9) |
| Torus | Thinnest cells (singleton×singleton = 1 hexagram each) |
| Temporal | Hardest simultaneous access (only 16/60 states have both active) |

The cycle attractor (既濟/未濟) is the fixed point of the compound involution (complement∘reverse). It is the one place in Z₂⁶ where "flip everything" and "swap positions" are the same act.

---

## How 3 Meets 5: The Lo Shu

The Lo Shu (洛書) magic square:

```
4  9  2
3  5  7
8  1  6
```

Every row, column, and diagonal sums to **15 = 3 × 5**. The meeting point of the two primes.

| Property | Value | Decomposition |
|---|---|---|
| Grid dimension | 3×3 | Pure 3 |
| Center | 5 | Pure 5 |
| Magic constant | 15 | 3 × 5 |
| Opposite pair sum | 10 | 2 × 5 |
| Total | 45 | 9 × 5 = 3² × 5 |
| Perimeter cells | 8 | 2³ (= trigram count) |

The 後天八卦 maps directly onto the 8 perimeter cells. 5 sits in the center — occupied by no trigram. The trigrams surround the element hub.

**Mod-5 conservation:** Every alignment in the Lo Shu sums to 15 ≡ 0 mod 5 (and 0 mod 3). The 3×3 geometry carries a Z₅ conservation law. The two primes are interlocked through the magic square constraint — you cannot have one without the other.

---

## The He Tu: 五行 as Mod-5 Residue

The He Tu (河圖) formula:

> 天一生水，地六成之。地二生火，天七成之。天三生木，地八成之。地四生金，天九成之。天五生土，地十成之。

Each element has a generating number (生, 1-5) and a completing number (成, 6-10), differing by exactly 5:

| Element | 生 | 成 | mod 5 |
|---|---|---|---|
| Water | 1 (天/yang) | 6 (地/yin) | 1 |
| Fire | 2 (地/yin) | 7 (天/yang) | 2 |
| Wood | 3 (天/yang) | 8 (地/yin) | 3 |
| Metal | 4 (地/yin) | 9 (天/yang) | 4 |
| Earth | 5 (天/yang) | 10 (地/yin) | 0 |

The element IS the residue class. Not assigned to one — it is one. Every integer ≡1 mod 5 is Water. Every integer ≡2 mod 5 is Fire. The He Tu reveals Z₅ as the quotient of the integers by the element relation.

Within each class, the two representatives carry yin/yang polarity (odd = 天/yang, even = 地/yin). This gives:

**Z₁₀ ≅ Z₅ × Z₂** — the 10 heavenly stems (天干) decompose as elements × polarity. CRT guarantees this since gcd(5, 2) = 1.

| Yang stem | Yin stem | Element |
|---|---|---|
| 甲 | 乙 | Wood |
| 丙 | 丁 | Fire |
| 戊 | 己 | Earth |
| 庚 | 辛 | Metal |
| 壬 | 癸 | Water |

---

## Two Parallel Z₅ Structures

There are two Z₅ systems operating in the hexagram framework:

**Arithmetic Z₅** — the counting numbers mod 5. Source: He Tu. Manifests in: heavenly stems (Z₁₀ = Z₅ × Z₂), Lo Shu conservation law, 60-甲子 cycle (via the stems), 納甲 branch elements.

**Structural Z₅** — the trigram→element assignment. Source: binary structure of trigrams (parity, complement closure, Hamming geometry). Manifests in: the torus (Z₅ × Z₅), 生克 evaluation, 體/用 reading, the {2,2,2,1,1} partition.

Both produce the same 5 elements. Both use the same 生 and 克 cycles. But they arrive at the assignment through different mechanisms:

- Arithmetic Z₅ says: Water = 1 because 天一生水 (Heaven-One generates Water). The number comes first.
- Structural Z₅ says: Water = 坎 because 坎 is a singleton in the complement-closed partition forced by binary geometry. The structure comes first.

**These are genuinely incommensurable.** Proven computationally (deep/01_assignment_test.py, Part 4).

### Setup

Label the 5 elements in two ways:
- **生-cycle numbering**: Wood=0, Fire=1, Earth=2, Metal=3, Water=4. The 生-step σ is +1 mod 5.
- **He Tu numbering**: Earth=0, Water=1, Fire=2, Wood=3, Metal=4. The cosmological counting order.

The complement anti-automorphism π acts on elements as: Wood↔Wood, Fire↔Water, Earth↔Metal.

### Key results

**1. π is affine on 生-cycle, not on He Tu.**

On the 生-cycle ring: π(x) = -x mod 5 for all x. Clean algebraic negation.

On the He Tu ring: no affine map ax+b mod 5 reproduces π. Verified by exhaustive search of all 25 candidates. The complement is "non-linear" in He Tu coordinates.

**2. Both generate D₅.**

On both rings, the group generated by {σ, π} has order 10 = |D₅|. The pair (生-step, complement) generates the full dihedral group regardless of coordinate system.

**3. The conjugation γ is non-affine.**

The map γ: 生-cycle → He Tu that takes each element to its He Tu index is:
```
γ = {Wood:0→3, Fire:1→2, Earth:2→0, Metal:3→4, Water:4→1}
```

γ satisfies γσγ⁻¹ = σ_hetu and γπγ⁻¹ = π_hetu — it is the conjugating permutation between the two D₅ actions. But γ is itself not affine: it cannot be written as x → ax+b mod 5.

**4. The 生-cycle steps are irregular on He Tu.**

生 in He Tu coordinates: 3→2→0→4→1→3. Step differences mod 5: [4, 3, 4, 2, 2]. The 生-step is NOT a constant translation in He Tu — the generative cycle has variable "speed" in cosmological coordinates.

### Interpretation

The He Tu Z₅ encodes **spatial position** (compass directions: Water=North, Fire=South, Wood=East, Metal=West, Earth=Center). The 生-cycle Z₅ encodes **relational dynamics** (generation and destruction). They share the same 5 categories and the same D₅ symmetry, but their internal geometry is non-trivially twisted.

The connection runs through the 後天八卦 (Later Heaven arrangement), which maps trigrams from cosmological positions to relational roles. This mapping is conventional (historical, mediated by tradition) rather than algebraic (forced by group theory). γ exists but has no algebraic structure — it's a "pure permutation."

This is an instance of the broader incommensurability: the hexagram system's structures share points and global symmetry but differ in local operations. Position and relation are two views of one thing that cannot be unified into a single algebraic frame.

---

## The Synthesis

The hexagram system uses three primes:

- **2** generates the combinatorial space (what exists)
- **3** generates the positional geometry (where it sits)
- **5** generates the relational dynamics (how it interacts)

They are pairwise coprime: gcd(2,3) = gcd(2,5) = gcd(3,5) = 1. None can be derived from the others. Each is algebraically independent.

Their meeting points:
- **2 meets 3**: the trigram (Z₂³). 8 objects from 3 binary choices. The Boolean cube.
- **2 meets 5**: the Fire/Water bridge. Two singleton elements where Z₂ and Z₅ coincide. The projection's fixed points.
- **3 meets 5**: the Lo Shu. Magic constant 15 = 3×5. A 3×3 geometry carrying Z₅ conservation.
- **2 × 3 × 5 = 30**: the 納音 cycle. 60 甲子 / 2 = 30 pairs, each assigned to one of 5 elements × 6 types. Also: 30 = the number of distinct element+quality combinations.

The hexagram at full resolution lives in Z₂⁶ = Z₂^(2×3) — the combinatorial space with both the binary and positional dimensions encoded. The 五行 projection collapses this to Z₅ × Z₅ — the relational surface. The Lo Shu mediates between the positional (3) and relational (5) dimensions. Fire/Water mediates between the combinatorial (2) and relational (5) dimensions.

The system is the joint product of three independent prime structures, each irreducible, each contributing a different axis of description, with specific bridge points where pairs of primes make contact.
