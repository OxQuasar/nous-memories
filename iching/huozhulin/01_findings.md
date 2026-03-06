# Probe 1: 納甲 as a Map on Z₂⁶

## 1. Verification

Implementation matches both worked examples exactly:

**姤 (天風姤) — 巽 lower, 乾 upper:**
```
  上六  壬戌  Earth
  九五  壬申  Metal
  九四  壬午  Fire
  九三  辛酉  Metal
  九二  辛亥  Water
  初六  辛丑  Earth
```

**遁 (天山遁) — 艮 lower, 乾 upper:**
```
  上九  壬戌  Earth
  九五  壬申  Metal
  九四  壬午  Fire
  九三  丙申  Metal
  六二  丙午  Fire
  初六  丙辰  Earth
```

## 2. Factoring Structure

**納甲 factors completely through the trigram pair** as two independent functions:

```
najia(h) = ( f_lower(lower_trig(h)), f_upper(upper_trig(h)) )
```

The upper half's assignment depends only on the upper trigram,
the lower half only on the lower trigram. No cross-trigram interaction.

**Position split:** Only 乾 and 坤 assign different stems/branches
depending on whether they occupy the lower or upper position.
The other 6 trigrams are position-invariant.

## 3. Inner-Bit Blindness

納甲 reads the 3+3 trigram split (bits [0:3] and [3:6]).
It accesses every bit, but only through trigram membership.

It is **completely blind** to features depending on the inner
4-bit window (bits 1–4):

- 互卦 (nuclear hexagram)
- Basin membership and convergence depth
- Kernel decomposition (O, M, I components)

Within each inner-bit group (4 hexagrams sharing bits 1–4),
all 4 get **maximally different** 納甲 assignments.

**納甲 and 互卦 decompose Z₂⁶ along orthogonal axes.**

## 4. Branch vs Trigram Elements

Across 384 (hexagram, line) states:

| Relation | Count | Fraction |
|----------|------:|----------|
| 生体 | 104 | 0.2708 |
| 克体 | 80 | 0.2083 |
| 体克用 | 80 | 0.2083 |
| 体生用 | 64 | 0.1667 |
| 比和 | 56 | 0.1458 |

Only **56/384 = 14.6%** of positions have matching branch
and trigram elements. The branch layer carries independent 五行 information.

### Mismatch count per hexagram

| Mismatches | Count |
|----------:|------:|
| 4/6 | 12 |
| 5/6 | 32 |
| 6/6 | 20 |

### Branch element spread per trigram

| Trigram | Element | Branch elements (3 lines) | Matches |
|---------|---------|---------------------------|---------|
| Kun ☷ | Earth | Earth, Fire, Wood | 1/3 |
| Zhen ☳ | Wood | Water, Wood, Earth | 1/3 |
| Kan ☵ | Water | Wood, Earth, Fire | 0/3 |
| Dui ☱ | Metal | Fire, Wood, Earth | 0/3 |
| Gen ☶ | Earth | Earth, Fire, Metal | 1/3 |
| Li ☲ | Fire | Wood, Earth, Water | 0/3 |
| Xun ☴ | Wood | Earth, Water, Metal | 0/3 |
| Qian ☰ | Metal | Water, Wood, Earth | 0/3 |

Each trigram's branches span multiple elements — typically 2–3 distinct
elements across its 3 lines, usually different from the trigram element.

## 5. Algebraic Characterization

```
Z₂⁶ ──split──→ Z₂³ × Z₂³ ──lookup──→ (Stem × Branch)³ × (Stem × Branch)³
  h              (lo, up)               6 labeled lines
```

The first step (trigram extraction) is linear. The second (stem/branch assignment)
is a table lookup with no algebraic structure beyond the cyclic branch progressions
(arithmetic mod 12, step ±2).

The starting points per trigram are specific to the 納甲 tradition —
they encode a particular correspondence between the 8 trigrams and the
12 branches that has no obvious group-theoretic origin.

## 6. Key Insight

**納甲 and the 互卦/kernel framework are algebraically orthogonal.**

| System | Reads | Blind to |
|--------|-------|----------|
| 納甲 | Trigram pair (shell) | Nuclear structure, basin, kernel |
| 互/kernel | Inner 4-bit window (core) | Trigram identity, outer bits |

火珠林 accesses information 梅花 discards (individual trigram identity, 6-node resolution).
梅花 accesses information 火珠林 ignores (nuclear convergence, basin dynamics).
They are **complementary projections** of the same Z₂⁶ space.
