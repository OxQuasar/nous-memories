# Round 3: Stress-Testing the 六合 Degree-Structure Result

## 1. The 24 Mountains Mapping (Source Verification)

The branch→trigram mapping used in Rounds 1-2 is the standard 24 Mountains (二十四山)
system from feng shui compass (Luo Pan) practice. Each trigram sector spans 45° and
contains exactly 3 of the 24 mountains. The 12 Earthly Branches distribute as:

- **Cardinal trigrams** (Kan=N, Zhen=E, Li=S, Dui=W): 1 branch each
- **Intercardinal trigrams** (Gen=NE, Xun=SE, Kun=SW, Qian=NW): 2 branches each

Source: standard Luo Pan arrangement, confirmed via Wikipedia (Earthly Branches article),
Imperial Harvest (Later Heaven Bagua), fengshuied.com (24 Mountains), and others.

## 2. Yin/Yang Circularity Check

Cross-tabulation of branch yin/yang vs trigram polarity:

| | P₊ (cardinal) | P₋ (intercardinal) |
|---------|---------------|--------------------|
| Yang branches | 2 | 4 |
| Yin branches | 2 | 4 |

**Result: PERFECTLY MIXED** — yang and yin branches have *identical* distributions
(2 to P₊, 4 to P₋ each). The 2:4 ratio is the base rate (4 cardinal trigrams × 1 branch
= 4 branches in P₊, 4 intercardinal × 2 branches = 8 in P₋). Branch yin/yang carries
zero information about P₊/P₋. The degree-structure result is NOT a yin/yang artifact.

## 3. Alternative Mappings

### 3a. Jing Fang Na Zhi (京房纳支)

Na Zhi assigns branches to hexagram LINE POSITIONS across multiple trigrams.
It does not define a clean 12→8 branch→trigram function.
Cannot be used as an alternative mapping for this test.

### 3b. Element-based mapping (branch element+polarity → trigram)

Differences from 24 Mountains: 8/12 branches map differently.
六合 degree structure: deg2 = ['Gen', 'Kan', 'Kun', 'Li']
Matches P₋? **False**

### 3c. Swapped within-element mapping

六合 degree structure: deg2 = ['Dui', 'Gen', 'Kun', 'Zhen']
Matches P₋? **False**

## 4. Root Cause Analysis

The degree-structure result (deg2 = P₋) arises because:

1. The 24 Mountains system assigns **2 branches to each P₋ trigram** (intercardinal)
   and **1 branch to each P₊ trigram** (cardinal).
2. 六合 pairs adjacent branches, so trigrams with more branches get higher degree.
3. P₋ = intercardinal = 2-branch sectors → degree 2.
4. P₊ = cardinal = 1-branch sectors → degree 1.

## 5. Verdict

### Is the result mapping-dependent or mapping-independent?

**MAPPING-DEPENDENT.** The result requires the 24 Mountains assignment
(or the equivalent seasonal assignment). Under the element-based mapping,
deg2 ≠ P₋ (breaks).
Under the swapped mapping, deg2 ≠ P₋ (breaks).

### Is the P₊/P₋ recovery circular?

**NOT through yin/yang** — branch yin/yang splits 50/50 across P₊ and P₋.

**Through geometry** — the result depends on the 24 Mountains assigning
2 branches to intercardinal sectors (P₋) and 1 to cardinal (P₊). This
branch-count asymmetry IS the P₊/P₋ distinction in another guise.

### Strongest claim about 六合's relationship to the trigram space

六合 provides a **through-geometry witness** to P₊/P₋ that is:
- Independent of binary encoding, Lo Shu numbers, and yang-count
- Independent of branch yin/yang assignments
- Dependent on the 24 Mountains compass assignment (branch-count per sector)
- The causal chain is: compass geometry → branch multiplicity → 六合 degree → P₊/P₋

This is COMPATIBLE but REDUNDANT with the prior characterization.
The P₊/P₋ partition is not independently discovered by 六合;
rather, 六合 reflects the branch-count asymmetry that is itself
a manifestation of the cardinal/intercardinal (= P₊/P₋) distinction
built into the 24 Mountains system.

The zero-overlap of 六合 edges with all known involution edges
remains structurally interesting — 六合 lives in the complement
of the involution graph — but this complementarity is a geometric
consequence of adjacency (六合) vs opposition (involutions) on the
Later Heaven Bagua circle.
