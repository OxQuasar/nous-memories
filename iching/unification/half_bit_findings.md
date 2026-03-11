# The 0.5-Bit Test: Findings

## Setup

After all F₂-linear constraints, the 五行 assignment has one binary
degree of freedom: which odd-coset complement pair becomes Wood?

Four candidate assignments (all sharing Earth={坤,艮}, Metal={兌,乾}):

| Key | Wood pair | Fire | Water | Fano line |
|-----|-----------|------|-------|-----------|
| A1 | {震,巽} | 坎 | 離 | H |
| A2 | {震,巽} | 離 | 坎 | H | ← **TRADITIONAL** |
| A3 | {坎,離} | 震 | 巽 | Q |
| A4 | {坎,離} | 巽 | 震 | Q |

## Constraint Chain

1. **He Tu cardinal alignment**: N=Water, S=Fire, E=Wood, W=Metal
   (pins one trigram of each element to each cardinal direction)

2. **生-cycle monotonicity**: tracing Wood→Fire→Earth→Metal→Water
   around the compass, each step ≤180° clockwise (no backtracking)

## Results

| Assignment | Cardinal-aligned | Sheng-monotone |
|------------|-----------------|----------------|
| A1 | 96 | 56 |
| A2 | 96 | 56 | ← TRAD
| A3 | 96 | 56 |
| A4 | 96 | 56 |

**All four assignments produce identical survivor counts at every stage.**

## Why the Counts Are Identical

The four assignments are **isomorphic under compass geometry**:
- Earth={坤,艮} and Metal={兌,乾} are the same in all four
- The remaining 4 trigrams {震,坎,離,巽} are just relabeled among {Wood, Fire, Water}
- He Tu constraints and 生-monotonicity depend only on element class sizes
- Both candidate Wood pairs have XOR = OMI (111), which lies on ALL three
  through-OMI lines (H, P, Q) — so the XOR structure is identical
- No compass constraint can distinguish {震,巽} from {坎,離}

## What DOES Distinguish Them

The two Wood pair choices differ in their **Fano line alignment**:

| Property | Traditional (A1/A2) | Alternative (A3/A4) |
|----------|--------------------|--------------------|
| Wood pair | {震(001),巽(110)} | {坎(010),離(101)} |
| Same-element pair on line | **H** = ker(b₁⊕b₂) | **Q** = ker(b₀⊕b₂) |
| 互 attractor 2-cycle elements | Water/Fire (克) | Wood/Wood (同) |
| P→H rotation target carries | same-element pair | different-element pair |
| H is '五行-degenerate'? | ✓ (Wood/Wood/Metal) | ✗ (Water/Fire/Metal) |

The Fano line distinction is invisible to compass geometry but visible to
互 dynamics and parity rotation.

## Structural Arguments for the Traditional Choice

While no single constraint forces the choice, three structural arguments
favor placing the same-element pair on **H** (traditional):

1. **P→H parity rotation**: 互 rotates the 五行 parity axis from P to H.
   Having the same-element pair on the rotation TARGET (H) means 五行
   parity information flows toward the element-preserving direction.

2. **互 attractor semantics**: The 2-cycle {JiJi,WeiJi} oscillates between
   坎 and 離 positions. Traditional makes this Water↔Fire (a 克 oscillation),
   matching JiJi/WeiJi's semantic content (completion↔incompletion).
   Alternative makes it Wood↔Wood (同), losing the dynamic tension.

3. **H as the divination line**: H = ker(b₁⊕b₂) is the 互 kernel line
   and the stabilizer-generating line. Having H carry the same-element pair
   makes H simultaneously the structural backbone (Stab(H) = S₄) and the
   五行-internal direction (movement along H preserves element class).

## Conclusion: The 0.5-Bit Is Genuine

The 0.5-bit **cannot be forced** by any combination of:
- F₂-linear constraints (Fano geometry)
- Z₅ compass constraints (He Tu cardinals, 生-cycle monotonicity)
- Z₂/Z₃ constraints (yin-yang balance, sons placement)

All four candidate assignments survive every known constraint with
identical counts. The choice is a genuine free parameter.

**However**, the traditional choice has strong structural motivation:
it uniquely aligns the same-element pair with the 互 kernel line H,
the target of parity rotation, and the stabilizer-generating line.
This is a coherence argument, not a forcing argument.

The system has exactly **0.5 bits of freedom**: enough to choose
which through-OMI line carries the same-element pair (H vs Q),
but not enough to affect any other structure.
