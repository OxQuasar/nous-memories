# Probe 4: Breaking the 2/5 Ceiling

## Part A: Element-Level Ceiling Test

For each (season, day_branch) pair (5 × 12 = 60), compute the set of
'potentially promotable' elements: {旺, 相} ∪ {day_element, day_generates}.

| Set size | Count | Fraction |
|----------|-------|----------|
| 2 | 12 | 20% |
| 3 | 24 | 40% |
| 4 | 24 | 40% |

**Maximum set size: 4**

Day element outside seasonal 旺/相: 36/60 pairs (60%).

日辰's element can introduce elements beyond the seasonal 旺/相 pair.
The element-level ceiling can be exceeded when the day's element
differs from both 旺 and 相.

## Part B: Hexagram-Level Active-Type Test (Definitive)

For each (season, day_branch, hexagram) triple (5 × 12 × 64 = 3840):
A line is **functionally active** if ANY of:
- Its element is 旺 or 相 in this season
- The day branch 沖's this line's branch (暗動)
- The day branch's element 生 this line's element

Count distinct 六親 types with ≥1 active line.

| Active types | States | Fraction |
|-------------|--------|----------|
| 0/5 | 29 | 0.8% |
| 1/5 | 522 | 13.6% |
| 2/5 | 1711 | 44.6% |
| 3/5 | 1352 | 35.2% |
| 4/5 | 226 | 5.9% |

**CEILING BROKEN: maximum 4/5 active types.**

日辰's branch-level mechanisms (沖/暗動, 日辰生) can activate 六親 types
whose elements are seasonally weak. The branch→element map (Z₁₂ → Z₅)
is many-to-one, so branch-level operations reach elements that the
season alone does not empower.

## Part C: Spotlight Dynamics

- Spring: 5 elements reachable across 12 branches: {'Wood', 'Fire', 'Metal', 'Earth', 'Water'}
- Summer: 5 elements reachable across 12 branches: {'Wood', 'Fire', 'Metal', 'Earth', 'Water'}
- Late_Summer: 5 elements reachable across 12 branches: {'Wood', 'Fire', 'Metal', 'Earth', 'Water'}
- Autumn: 5 elements reachable across 12 branches: {'Wood', 'Fire', 'Metal', 'Earth', 'Water'}
- Winter: 5 elements reachable across 12 branches: {'Wood', 'Fire', 'Metal', 'Earth', 'Water'}

**Cycle basin conflict resolution:** Both Fire AND Water promotable in 16/60 pairs (27%).
日辰 can simultaneously promote both Fire and Water elements,
partially resolving the Cycle basin's permanent internal conflict.

## Part D: 梅花 Temporal Distribution

Sample: year_branch=1, 12 months × 30 days × 12 hours = 4320 time points.

**Distinct hexagrams accessed: 64/64 (100%)**

| Frequency | # Hexagrams |
|-----------|-------------|
| 44× | 12 |
| 45× | 8 |
| 46× | 12 |
| 88× | 12 |
| 90× | 8 |
| 92× | 12 |

χ² = 481.8 (df=63, expected per hex = 67.5)
Distribution is **non-uniform**.

**2/5 ceiling in 梅花:** 梅花 uses seasonal strength (旺相休囚死) but does NOT
employ 日辰 branch mechanisms (沖, 暗動, 日辰生). Therefore:
- 六親→element bijection applies ✓
- Each season empowers exactly 2/5 elements ✓
- **梅花 inherits the 2/5 ceiling identically** ✓

## Part E: Connection to the Orthogonality Wall

### The two constraints

1. **2/5 ceiling** (element-level): limits simultaneous activation
2. **Orthogonality wall** (information-level): shell cannot see core

### 日辰's effect on each

- **2/5 ceiling**: BROKEN by 日辰 (expanded to 4/5)
- **Orthogonality wall**: UNTOUCHED — 日辰 operates on branches from 納甲,
  which reads trigram pairs (shell). No cross-talk with basin/depth (core).

### Why 日辰 cannot bridge the wall

日辰 increases resolution within the shell (Z₅ → Z₁₂). The branch-level
mechanisms (沖/暗動, 六合, 日辰生/克) all operate on data assigned by 納甲,
which factors through the trigram pair decomposition. 納甲 is inner-bit blind
(Probe 1): it reads (lower_trig, upper_trig), not (b₁,b₂,b₃,b₄).
Therefore 日辰's operations, however rich in Z₁₂, remain in the shell's
image. No temporal mechanism in 火珠林 creates a channel to the core.

### Structural summary

```
             Z₂⁶
            /    \
     Shell (trig pair)    Core (inner bits)
       ↓                    ↓
   納甲 → branches       互卦 → basins
       ↓                    ↓
   六親 × 旺相 × 日辰     凶 / depth
       ↓                    ↓
   2/5 ceiling            convergence
   (softened by 日辰)     (unreachable)
```

The 2/5 ceiling lives in the left branch. 凶 lives in the right branch.
日辰 can push the ceiling higher within the left branch, but the wall
between left and right is structural — it's the orthogonality of
trigram-pair vs inner-window decompositions of Z₂⁶.
