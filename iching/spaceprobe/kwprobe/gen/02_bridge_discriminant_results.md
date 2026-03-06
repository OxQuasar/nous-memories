# Sub-Optimal Bridge Discriminant Analysis

**Methodological note:** With 17 data points and 10+ features, post-hoc pattern finding risks overfitting. For every claimed discriminant, we report the chance baseline: if the 'chosen' label were assigned randomly among candidates, how often would that feature achieve the same discrimination score? Features with P(≥actual) > 0.05 are not significant.

## Data: 17 Sub-Optimal Bridges

These bridges have KW's 互 distance >1 above the minimum available.

| Bridge | KW chose | d_互 | Min d | Gap | # alternatives |
|--------|----------|------|-------|-----|----------------|
| 1→2 | Xu/Song | 3 | 0 | +3 | 3 |
| 2→3 | Shi/Bi | 3 | 0 | +3 | 1 |
| 3→4 | Xiao Chu/Lu | 3 | 1 | +2 | 5 |
| 4→5 | Tai/Pi | 5 | 0 | +5 | 1 |
| 5→6 | Tong Ren/Da You | 2 | 0 | +2 | 3 |
| 6→7 | Qian/Yu | 3 | 1 | +2 | 2 |
| 9→10 | Shi He/Bi | 3 | 1 | +2 | 5 |
| 11→12 | Wu Wang/Da Chu | 3 | 0 | +3 | 1 |
| 12→13 | Yi/Da Guo | 3 | 1 | +2 | 1 |
| 13→14 | Kan/Li | 4 | 0 | +4 | 1 |
| 16→17 | Jin/Ming Yi | 3 | 1 | +2 | 2 |
| 18→19 | Jian/Xie | 6 | 1 | +5 | 2 |
| 20→21 | Guai/Gou | 5 | 1 | +4 | 2 |
| 21→22 | Cui/Sheng | 3 | 1 | +2 | 1 |
| 22→23 | Kun/Jing | 5 | 1 | +4 | 1 |
| 23→24 | Ge/Ding | 3 | 0 | +3 | 1 |
| 24→25 | Zhen/Gen | 3 | 1 | +2 | 1 |

## Feature Set

For bridge from pair k → candidate pair j:

| # | Feature | Type | Description |
|---|---------|------|-------------|
| 1 | basin | categorical | Basin of candidate's entering hexagram |
| 2 | basin_match | binary | Candidate's entry basin = current pair's exit basin? |
| 3 | skeleton | binary | Is candidate a self-reverse complement pair? |
| 4 | lo_match | binary | Lower trigram continuity (exit hex → enter hex) |
| 5 | up_match | binary | Upper trigram continuity |
| 6 | trig_shared | 0–2 | Count of matching trigrams (lo + up) |
| 7 | hex_dist | 0–6 | Direct Hamming distance (not through 互) |
| 8 | yang_diff | 0–6 | Absolute yang-count difference |
| 9 | kernel | categorical | Mirror-kernel of XOR between exit/enter hexagrams |
| 10 | h_kernel | binary | Kernel ∈ H = {id, O, MI, OMI}? |
| 11 | reversed | binary | Candidate starts with reverse of current pair's end? |
| 12 | novelty | 0–4 | New trigrams in candidate pair (not in pairs 0..k) |
| 13 | phase_rel | categorical | Five-phase relation: exit upper → enter lower trigram |

## Part 1: Feature Comparison per Bridge

### Bridge 1→2

From Zhun/Meng (exit basin: ○)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Xu/Song | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 4 | 2 | MI | ✓ | ✗ | 0 | 克体 |
| Alt 1 | Shi/Bi | 0 | ○ | ✓ | ✗ | ✓ | ✗ | 1 | 1 | O | ✓ | ✗ | 0 | 生体 |
| Alt 2 | Lin/Guan | 0 | ○ | ✓ | ✗ | ✗ | ✗ | 2 | 0 | id | ✓ | ✗ | 2 | 比和 |
| Alt 3 | Sun/Yi | 0 | ○ | ✓ | ✗ | ✗ | ✓ | 1 | 1 | O | ✓ | ✗ | 2 | 比和 |

### Bridge 2→3

From Xu/Song (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Shi/Bi | 3 | ○ | ✗ | ✗ | ✓ | ✗ | 3 | 3 | OMI | ✓ | ✗ | 0 | 体生用 |
| Alt 1 | Kun/Jing | 0 | ◎ | ✓ | ✗ | ✓ | ✗ | 1 | 1 | O | ✓ | ✗ | 2 | 体生用 |

### Bridge 3→4

From Shi/Bi (exit basin: ○)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Xiao Chu/Lu | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 4 | 4 | MI | ✓ | ✗ | 2 | 生体 |
| Alt 1 | Bo/Fu | 1 | ○ | ✓ | ✗ | ✓ | ✗ | 2 | 0 | OM | ✗ | ✗ | 0 | 克体 |
| Alt 2 | Yi/Da Guo | 1 | ○ | ✓ | ✓ | ✗ | ✗ | 3 | 1 | M | ✗ | ✗ | 2 | 克体 |
| Alt 3 | Kan/Li | 1 | ○ | ✓ | ✓ | ✗ | ✓ | 1 | 1 | M | ✗ | ✗ | 2 | 比和 |
| Alt 4 | Huan/Jie | 1 | ○ | ✓ | ✗ | ✗ | ✗ | 2 | 2 | OM | ✗ | ✗ | 2 | 比和 |
| Alt 5 | Zhong Fu/Xiao Guo | 1 | ○ | ✓ | ✓ | ✗ | ✗ | 3 | 3 | M | ✗ | ✗ | 2 | 体生用 |

### Bridge 4→5

From Xiao Chu/Lu (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Tai/Pi | 5 | ◎ | ✓ | ✗ | ✗ | ✗ | 4 | 2 | OM | ✗ | ✗ | 0 | 比和 |
| Alt 1 | Kun/Jing | 0 | ◎ | ✓ | ✗ | ✗ | ✗ | 2 | 2 | id | ✓ | ✗ | 0 | 体生用 |

### Bridge 5→6

From Tai/Pi (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Tong Ren/Da You | 2 | ● | ✗ | ✗ | ✗ | ✓ | 2 | 2 | OI | ✗ | ✗ | 2 | 克体 |
| Alt 1 | Sui/Gu | 0 | ◎ | ✓ | ✗ | ✗ | ✗ | 2 | 0 | id | ✓ | ✗ | 0 | 生体 |
| Alt 2 | Wu Wang/Da Chu | 0 | ◎ | ✓ | ✗ | ✗ | ✓ | 1 | 1 | O | ✓ | ✗ | 0 | 生体 |
| Alt 3 | Cui/Sheng | 0 | ◎ | ✓ | ✗ | ✓ | ✗ | 1 | 1 | O | ✓ | ✗ | 0 | 生体 |

### Bridge 6→7

From Tong Ren/Da You (exit basin: ●)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Qian/Yu | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 4 | 4 | MI | ✓ | ✗ | 0 | 生体 |
| Alt 1 | Guai/Gou | 1 | ● | ✓ | ✗ | ✓ | ✗ | 2 | 0 | OM | ✗ | ✗ | 0 | 体克用 |
| Alt 2 | Feng/Lu | 1 | ● | ✓ | ✗ | ✗ | ✗ | 2 | 2 | OM | ✗ | ✗ | 0 | 比和 |

### Bridge 9→10

From Lin/Guan (exit basin: ○)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Shi He/Bi | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 3 | 1 | OMI | ✓ | ✗ | 0 | 生体 |
| Alt 1 | Bo/Fu | 1 | ○ | ✓ | ✗ | ✓ | ✗ | 1 | 1 | M | ✗ | ✗ | 0 | 生体 |
| Alt 2 | Yi/Da Guo | 1 | ○ | ✓ | ✓ | ✗ | ✗ | 2 | 0 | OM | ✗ | ✗ | 0 | 生体 |
| Alt 3 | Kan/Li | 1 | ○ | ✓ | ✓ | ✗ | ✗ | 2 | 0 | OM | ✗ | ✗ | 0 | 体生用 |
| Alt 4 | Huan/Jie | 1 | ○ | ✓ | ✗ | ✗ | ✓ | 1 | 1 | M | ✗ | ✗ | 0 | 体生用 |
| Alt 5 | Zhong Fu/Xiao Guo | 1 | ○ | ✓ | ✓ | ✗ | ✓ | 2 | 2 | OM | ✗ | ✗ | 0 | 体克用 |

### Bridge 11→12

From Bo/Fu (exit basin: ○)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Wu Wang/Da Chu | 3 | ◎ | ✗ | ✗ | ✓ | ✗ | 3 | 3 | OMI | ✓ | ✗ | 0 | 比和 |
| Alt 1 | Yi/Da Guo | 0 | ○ | ✓ | ✓ | ✓ | ✗ | 1 | 1 | O | ✓ | ✗ | 0 | 比和 |

### Bridge 12→13

From Wu Wang/Da Chu (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Yi/Da Guo | 3 | ○ | ✗ | ✓ | ✗ | ✓ | 2 | 2 | MI | ✓ | ✗ | 0 | 体克用 |
| Alt 1 | Xun/Dui | 1 | ◎ | ✓ | ✗ | ✗ | ✗ | 2 | 0 | OM | ✗ | ✗ | 0 | 克体 |

### Bridge 13→14

From Yi/Da Guo (exit basin: ●)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Kan/Li | 4 | ○ | ✗ | ✓ | ✗ | ✗ | 2 | 2 | id | ✓ | ✗ | 0 | 生体 |
| Alt 1 | Guai/Gou | 0 | ● | ✓ | ✗ | ✗ | ✓ | 1 | 1 | O | ✓ | ✗ | 0 | 克体 |

### Bridge 16→17

From Dun/Da Zhuang (exit basin: ●)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Jin/Ming Yi | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 4 | 2 | MI | ✓ | ✗ | 0 | 比和 |
| Alt 1 | Guai/Gou | 1 | ● | ✓ | ✗ | ✓ | ✗ | 1 | 1 | M | ✗ | ✗ | 0 | 体生用 |
| Alt 2 | Feng/Lu | 1 | ● | ✓ | ✗ | ✗ | ✓ | 1 | 1 | M | ✗ | ✗ | 0 | 生体 |

### Bridge 18→19

From Jia Ren/Kui (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Jian/Xie | 6 | ◎ | ✓ | ✗ | ✗ | ✗ | 6 | 2 | id | ✓ | ✗ | 0 | 生体 |
| Alt 1 | Kun/Jing | 1 | ◎ | ✓ | ✗ | ✗ | ✗ | 3 | 1 | M | ✗ | ✗ | 0 | 克体 |
| Alt 2 | Zhen/Gen | 1 | ◎ | ✓ | ✗ | ✗ | ✗ | 2 | 2 | OM | ✗ | ✗ | 0 | 体生用 |

### Bridge 20→21

From Sun/Yi (exit basin: ○)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Guai/Gou | 5 | ● | ✗ | ✗ | ✗ | ✗ | 4 | 2 | OM | ✗ | ✗ | 0 | 比和 |
| Alt 1 | Huan/Jie | 1 | ○ | ✓ | ✗ | ✗ | ✓ | 2 | 0 | OM | ✗ | ✗ | 0 | 体生用 |
| Alt 2 | Zhong Fu/Xiao Guo | 1 | ○ | ✓ | ✓ | ✗ | ✓ | 1 | 1 | M | ✗ | ✗ | 0 | 体克用 |

### Bridge 21→22

From Guai/Gou (exit basin: ●)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Cui/Sheng | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 3 | 3 | OMI | ✓ | ✗ | 0 | 生体 |
| Alt 1 | Ge/Ding | 1 | ● | ✓ | ✗ | ✗ | ✗ | 3 | 1 | M | ✗ | ✗ | 0 | 克体 |

### Bridge 22→23

From Cui/Sheng (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Kun/Jing | 5 | ◎ | ✓ | ✗ | ✗ | ✗ | 3 | 1 | M | ✗ | ✗ | 0 | 体克用 |
| Alt 1 | Xun/Dui | 1 | ◎ | ✓ | ✗ | ✓ | ✗ | 2 | 2 | OM | ✗ | ✗ | 0 | 体生用 |

### Bridge 23→24

From Kun/Jing (exit basin: ◎)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Ge/Ding | 3 | ● | ✗ | ✗ | ✗ | ✗ | 3 | 1 | OMI | ✓ | ✗ | 0 | 体克用 |
| Alt 1 | Xun/Dui | 0 | ◎ | ✓ | ✗ | ✓ | ✗ | 1 | 1 | O | ✓ | ✗ | 0 | 生体 |

### Bridge 24→25

From Ge/Ding (exit basin: ●)

| | Pair | d_互 | Basin | B.match | Skel | Lo | Up | d_hex | Δyang | Kernel | ∈H | Rev | Nov | Phase |
|---|------|------|-------|---------|------|----|----|-------|-------|--------|----|----|-----|-------|
| **KW** | Zhen/Gen | 3 | ◎ | ✗ | ✗ | ✗ | ✗ | 4 | 2 | MI | ✓ | ✗ | 0 | 体生用 |
| Alt 1 | Feng/Lu | 1 | ● | ✓ | ✗ | ✗ | ✗ | 3 | 1 | M | ✗ | ✗ | 0 | 比和 |

## Part 2: Feature Discrimination Power

A feature 'strictly discriminates' a bridge if it uniquely identifies KW's choice among all candidates (KW's value differs from every alternative in a consistent direction).

### Single features

| Feature | Bridges discriminated | Rate | Chance mean | Chance 95th | P(≥actual) | Sig? |
|---------|----------------------|------|-------------|-------------|------------|------|
| hu_dist | 17/17 | 100% | 11.2 | 13 | 0.0002 | **YES** |
| kernel | 16/17 | 94% | 12.3 | 14 | 0.0046 | **YES** |
| basin_match | 14/17 | 82% | 8.8 | 11 | 0.0002 | **YES** |
| hex_dist | 14/17 | 82% | 9.8 | 12 | 0.0008 | **YES** |
| basin | 14/17 | 82% | 8.8 | 11 | 0.0002 | **YES** |
| phase_rel | 14/17 | 82% | 12.3 | 14 | 0.0864 | no |
| yang_diff | 12/17 | 71% | 10.5 | 13 | 0.2286 | no |
| h_kernel | 10/17 | 59% | 5.6 | 7 | 0.0003 | **YES** |
| trig_shared | 5/17 | 29% | 5.3 | 7 | 0.7766 | no |
| skeleton | 3/17 | 18% | 3.3 | 4 | 1.0000 | no |
| up_match | 3/17 | 18% | 3.1 | 5 | 0.7241 | no |
| lo_match | 2/17 | 12% | 3.5 | 5 | 1.0000 | no |
| novelty | 1/17 | 6% | 1.4 | 2 | 1.0000 | no |
| reversed | 0/17 | 0% | 0.0 | 0 | 1.0000 | no |

### Best feature pairs (union coverage)

| F1 | F2 | Bridges | Rate | Chance mean | P(≥actual) | Sig? |
|----|----|---------|------|-------------|------------|------|
| basin_match | hex_dist | 17/17 | 100% | 12.0 | 0.0002 | **YES** |
| basin_match | hu_dist | 17/17 | 100% | 11.2 | 0.0001 | **YES** |
| basin_match | kernel | 17/17 | 100% | 12.7 | 0.0010 | **YES** |
| basin_match | phase_rel | 17/17 | 100% | 14.4 | 0.0138 | **YES** |
| skeleton | hu_dist | 17/17 | 100% | 11.5 | 0.0001 | **YES** |
| lo_match | hu_dist | 17/17 | 100% | 0.0 | 0.0001 | **YES** |
| up_match | hu_dist | 17/17 | 100% | 0.0 | 0.0001 | **YES** |
| up_match | kernel | 17/17 | 100% | 0.0 | 0.0001 | **YES** |
| h_kernel | hex_dist | 17/17 | 100% | 0.0 | 0.0001 | **YES** |
| h_kernel | hu_dist | 17/17 | 100% | 0.0 | 0.0001 | **YES** |

## Part 3: Deferred Optimality

Where do the rejected 互-closer alternatives actually land in KW? Are they 互-optimal at their final position?

| Bridge | Rejected pair | KW position | d_互 there | Min d there | Optimal? |
|--------|---------------|-------------|-----------|-------------|----------|
| 1→2 | Shi/Bi | 3 | 3 | 0 | +3 |
| 1→2 | Lin/Guan | 9 | 2 | 1 | near |
| 1→2 | Sun/Yi | 20 | 2 | 1 | near |
| 2→3 | Kun/Jing | 23 | 5 | 1 | +4 |
| 3→4 | Bo/Fu | 11 | 2 | 1 | near |
| 3→4 | Yi/Da Guo | 13 | 3 | 1 | +2 |
| 3→4 | Kan/Li | 14 | 4 | 0 | +4 |
| 3→4 | Huan/Jie | 29 | 2 | 2 | ✓ |
| 3→4 | Zhong Fu/Xiao Guo | 30 | 0 | 0 | ✓ |
| 4→5 | Kun/Jing | 23 | 5 | 1 | +4 |
| 5→6 | Sui/Gu | 8 | 1 | 0 | near |
| 5→6 | Wu Wang/Da Chu | 12 | 3 | 0 | +3 |
| 5→6 | Cui/Sheng | 22 | 3 | 1 | +2 |
| 6→7 | Guai/Gou | 21 | 5 | 1 | +4 |
| 6→7 | Feng/Lu | 27 | 3 | 3 | ✓ |
| 9→10 | Bo/Fu | 11 | 2 | 1 | near |
| 9→10 | Yi/Da Guo | 13 | 3 | 1 | +2 |
| 9→10 | Kan/Li | 14 | 4 | 0 | +4 |
| 9→10 | Huan/Jie | 29 | 2 | 2 | ✓ |
| 9→10 | Zhong Fu/Xiao Guo | 30 | 0 | 0 | ✓ |
| 11→12 | Yi/Da Guo | 13 | 3 | 1 | +2 |
| 12→13 | Xun/Dui | 28 | 4 | 3 | near |
| 13→14 | Guai/Gou | 21 | 5 | 1 | +4 |
| 16→17 | Guai/Gou | 21 | 5 | 1 | +4 |
| 16→17 | Feng/Lu | 27 | 3 | 3 | ✓ |
| 18→19 | Kun/Jing | 23 | 5 | 1 | +4 |
| 18→19 | Zhen/Gen | 25 | 3 | 1 | +2 |
| 20→21 | Huan/Jie | 29 | 2 | 2 | ✓ |
| 20→21 | Zhong Fu/Xiao Guo | 30 | 0 | 0 | ✓ |
| 21→22 | Ge/Ding | 24 | 3 | 0 | +3 |
| 22→23 | Xun/Dui | 28 | 4 | 3 | near |
| 23→24 | Xun/Dui | 28 | 4 | 3 | near |
| 24→25 | Feng/Lu | 27 | 3 | 3 | ✓ |

**Summary:** 9/33 rejected alternatives (27%) are 互-optimal at their actual KW position. Baseline: 6/31 bridges overall are 互-optimal (19%).

The rejected alternatives have roughly the same optimality rate as the sequence average — no clear evidence of global planning via deferral.

## Summary

### Significant discriminants (excluding tautological hu_dist)

- **basin_match:** 14/17 bridges (p = 0.0002)
- **h_kernel:** 10/17 bridges (p = 0.0003)
- **hex_dist:** 14/17 bridges (p = 0.0008)
- **basin:** 14/17 bridges (p = 0.0002)
- **kernel:** 16/17 bridges (p = 0.0046)

### Interpretation

**Note:** `hu_dist` trivially discriminates 17/17 because sub-optimal bridges are *defined* as those where KW's 互 distance exceeds all alternatives'. This is tautological — the interesting discriminants are the non-互 features.

The best non-trivial discriminant is **kernel** at 16/17. 
This is strong — KW's choice at sub-optimal bridges is largely predicted by kernel.


The best feature pair covers 17/17 bridges, combining basin_match and hex_dist.

### Coverage map: which features discriminate which bridges?

| Bridge | basin_ | skelet | lo_mat | up_mat | h_kern | revers | trig_s | hex_di | yang_d | novelt | hu_dis | basin | kernel | phase_ |
|--------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|  1→ 2 |   ✓    |        |        |        |        |        |        |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
|  2→ 3 |   ✓    |        |        |        |        |        |        |   ✓    |   ✓    |   ✓    |   ✓    |   ✓    |   ✓    |        |
|  3→ 4 |   ✓    |        |        |        |   ✓    |        |        |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
|  4→ 5 |        |        |        |        |   ✓    |        |        |   ✓    |        |        |   ✓    |        |   ✓    |   ✓    |
|  5→ 6 |   ✓    |        |        |        |   ✓    |        |        |        |   ✓    |   ✓    |   ✓    |   ✓    |   ✓    |   ✓    |
|  6→ 7 |   ✓    |        |        |        |   ✓    |        |        |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
|  9→10 |   ✓    |        |        |        |   ✓    |        |        |   ✓    |        |        |   ✓    |   ✓    |   ✓    |        |
| 11→12 |   ✓    |   ✓    |        |        |        |        |        |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |        |
| 12→13 |   ✓    |   ✓    |        |   ✓    |   ✓    |        |   ✓    |        |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
| 13→14 |   ✓    |   ✓    |        |   ✓    |        |        |   ✓    |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
| 16→17 |   ✓    |        |        |        |   ✓    |        |   ✓    |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
| 18→19 |        |        |        |        |   ✓    |        |        |   ✓    |        |        |   ✓    |        |   ✓    |   ✓    |
| 20→21 |   ✓    |        |        |   ✓    |        |        |   ✓    |   ✓    |   ✓    |        |   ✓    |   ✓    |        |   ✓    |
| 21→22 |   ✓    |        |        |        |   ✓    |        |        |        |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |
| 22→23 |        |        |   ✓    |        |        |        |   ✓    |   ✓    |   ✓    |        |   ✓    |        |   ✓    |   ✓    |
| 23→24 |   ✓    |        |   ✓    |        |        |        |   ✓    |   ✓    |        |        |   ✓    |   ✓    |   ✓    |   ✓    |
| 24→25 |   ✓    |        |        |        |   ✓    |        |        |   ✓    |   ✓    |        |   ✓    |   ✓    |   ✓    |   ✓    |

Bridges with zero discriminating features: none
Mean features per bridge: 7.5
Bridges covered by ≥1 feature: 17/17

### What basin_match reveals

At 14/17 sub-optimal bridges, KW chooses a pair that **crosses basins** while the 互-closer alternative would have **stayed in the same basin**. This is the opposite of what you'd expect from basin clustering (which is extreme at 0th percentile). Interpretation: KW uses the sub-optimal bridges as **basin crossing points** — it deliberately accepts 互 cost to transition between basins. The 互-closer alternatives would keep the walk within the same basin, which conflicts with the breathing pattern that drives the narrative structure.

### What h_kernel reveals

At 10/17 sub-optimal bridges, KW's choice has kernel ∈ H while alternatives don't (8 bridges), or vice versa (2 bridges). KW preferentially chooses H-kernel transitions even when they cost more in 互 distance. H-kernel transitions are the ones that respect the mirror symmetry of the hexagram — they're the 'structurally clean' transitions. KW trades 互 for algebraic coherence.

### What hex_dist reveals

At 14/17 sub-optimal bridges, KW's choice has strictly higher hexagram Hamming distance than all alternatives. KW systematically chooses the 'bigger jump' in hexagram space. Since the alternatives are 互-close (similar inner structure), they're also hex-close. KW instead chooses pairs that are hex-distant but may share other structural properties.

### Core conclusion

互 continuity is a *soft* constraint in KW — the sequence accepts significant 互 costs at 17/31 bridges. The features tested here probe whether a simple structural rule explains the 'why' of each choice. 
The significant discriminant(s) (basin_match, h_kernel, hex_dist, basin, kernel) suggest that KW's pair ordering is not random with respect to these properties — there is additional structure beyond 互 optimization. The strongest signal is **basin crossing**: KW uses sub-optimal bridges to transition between basins, sacrificing 互 continuity for the breathing pattern that structures the sequence narratively.
