# Lead 2: Developmental Priority Per Canon

## The question

The sequence investigation found the Upper Canon (hex 1–30) is structurally extreme on kernel-transition metrics (~1 in 10,000) while the Lower Canon (hex 31–64) is structurally generic on every metric tested. Earlier work (logoswen iter6) established that all 32 KW pair orientations align with developmental priority — "whatever creates the conditions for the other comes first" — at 32/32 (p = 2.3 × 10⁻¹⁰), with 22 Clear and 10 Suggestive confidence ratings.

**Question:** Does developmental priority distribute differently across canons? Does it explain the Lower Canon's structural silence?

## Findings

### 1. Meaning is stronger in the structurally silent canon

| | Clear | Suggestive | Clear rate |
|---|---|---|---|
| Upper Canon (15 pairs) | 9 | 6 | 60% |
| Lower Canon (17 pairs) | 12 | 5 | 71% |

The Lower Canon — where kernel metrics find nothing — has stronger meaning clarity. Not dramatic (60% vs 71%) but directionally consistent with complementarity.

### 2. Algebra constrains the Upper Canon harder

Free-bit fragility classification (from iter4: does flipping degrade all 4 axes or create a trade-off?):

| | KW-dominates | Trade-off | Domination rate |
|---|---|---|---|
| Upper Canon | 8 pairs | 7 pairs | 53% |
| Lower Canon | 5 pairs | 12 pairs | 29% |

The Upper Canon has less algebraic slack. The Lower Canon's orientations are more freely chosen — algebra alone doesn't pin them.

### 3. Algebra↔meaning complementarity replicates within each canon

| | KW-dom Suggestive rate | Trade-off Suggestive rate |
|---|---|---|
| Upper Canon | 50% (4/8) | 29% (2/7) |
| Lower Canon | 40% (2/5) | 25% (3/12) |

Same inverse pattern in both canons: where algebra binds tightest, meaning is weakest. The complementarity is not a canon-level artifact — it operates at the pair level across both canons.

### 4. Dominators attack the Lower Canon

The 12 Hamming-2+ algebraic dominators (orientations that beat KW on all 4 metrics: χ², asymmetry, m-score, kac) achieve their superiority primarily by reversing Lower Canon pairs:

| | Pair-reversals | Share |
|---|---|---|
| Upper Canon | 21 | 28% |
| Lower Canon | 53 | **72%** |

Every dominator reverses at least as many Lower as Upper pairs. The most-attacked pairs are all Lower Canon with Clear developmental priority:

| Pair | Dominators that flip it | Confidence | Logic |
|---|---|---|---|
| 21 (Guai/Gou) | 12/12 | Clear | Breakthrough→Encounter |
| 19 (Jian/Xie) | 9/12 | Clear | Obstruction→Deliverance |
| 20 (Sun/Yi) | 9/12 | Clear | Decrease→Increase |

These are pairs where the developmental ordering is semantically unambiguous (Clear) and where reversal would violate the condition→consequence grammar. The dominators *must* reverse them to achieve algebraic improvement — and doing so breaks the meaning.

### 5. The two-canon picture

| | Upper Canon | Lower Canon |
|---|---|---|
| Kernel structure | Extreme (~1 in 10,000) | Generic |
| Algebraic fragility | Tight (53% dominated) | Loose (29% dominated) |
| Meaning clarity | 60% Clear | 71% Clear |
| Dominator target | 28% of violations | 72% of violations |
| **Organizing principle** | **Algebra** | **Meaning** |

The Upper Canon is organized by kernel-transition constraints (consecutive opposition, H-subgroup residence). The Lower Canon is organized by developmental priority (condition→consequence ordering). Together they prevent algebraic domination: no alternative orientation can improve all 4 algebraic metrics without reversing Clear developmental pairs in the Lower Canon.

This is not a clean separation — both canons have both algebra and meaning. But the *binding constraints* differ: the Upper Canon's orientations are algebraically pinned (53% KW-dominates), while the Lower Canon's are semantically pinned (attacked by 72% of dominator violations, defended by 71% Clear confidence).

## What this means for the investigation

The Lower Canon's structural silence on kernel metrics is not absence of structure. It is the presence of a *different kind* of structure — one that operates in the semantic domain (developmental priority, condition→consequence grammar) rather than the algebraic domain (kernel distance, subgroup residence).

The KW sequence uses two organizing principles on two canons:
1. **Upper Canon:** maximize kernel opposition and constrain the cumulative transformation path
2. **Lower Canon:** order pairs by developmental priority (the semantically deterministic ordering)

The cross-canon bridge (hex 30→31, kernel = OM, breaking the M-I lock) marks the transition between regimes.

## Limitations

- The "reader" is an LLM trained on traditional I Ching scholarship, not a naive assessor. Confirmation bias and Xugua circularity remain confounds (detailed in logoswen iter6).
- The 60% vs 71% Clear difference is small (n=15 vs n=17). The direction matters more than the magnitude.
- The algebra↔meaning complementarity within canons has small cell sizes (n=5 to n=12). The pattern is consistent but not independently significant per canon.
- The dominator analysis is the strongest signal: 72% Lower Canon violations is robust across all 12 dominators (none is Upper-dominated).

## Data

Script: `per_canon_analysis.py` in this directory.
Dependencies: `kingwen/sequence.py`, `logoswen/iter5/infra.py`.
Source data: `logoswen/iter6/comparator_round3.py` (reader assessments), `logoswen/iter6/dominator_meaning_check.py` (dominator sets).
