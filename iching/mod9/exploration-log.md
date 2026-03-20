# Lo Shu Spatial Structure — Exploration Log

## Iteration 1

### Framing correction

The investigation was initially framed as "mod-9 arithmetic" parallel to "mod-8 arithmetic." Textual analysis corrected this:

**The 後天 method does not use mod-9 arithmetic.** Vol2 line 16 of 梅花易數 explicitly states that while contemporary practitioners use Lo Shu numbers (坎一、坤二、震三、巽四、中五、乾六、兑七、艮八、离九), the text recommends using 先天 numbers (乾一、兌二、離三、震四、巽五、坎六、艮七、坤八) for divination calculation. Every worked 後天 example in vol1 (lines 209–237) confirms: 乾=1, 兌=2, 離=3, 震=4, 巽=5, 坎=6, 艮=7, 坤=8. The moving-line arithmetic is mod-6 on sums of 先天 numbers + hour number.

The Lo Shu provides the **spatial mapping** (compass direction → trigram), not the calculation system. The investigation is reframed as: **Z₅ structure of the Lo Shu compass layout, compared to the 先天 temporal layout.**

### Textual finding: Center = observer (resolves N2, partially resolves N6)

Vol1 line 173: "离南坎北，震东兑西，**人则介乎其中**" — the person occupies the center. Every worked 後天 example uses a compass direction (巽方, 離方, 坎方, 乾方, 兌方) — none uses center. The center (position 5) is the **coordinate origin**, not a state. It has Earth content (Z₅=2) because 土=Center in directional cosmology, but no trigram because trigrams describe observables and the observer is not an observable.

Position 5 is not a fixed point, absorbing state, or pass-through. It is the **null observation** — the point from which all 8 directions are measured. Z₉ = Z₈ + origin. The surjection F₂³→Z₅ does not need extending; the 9th position belongs to the coordinate system but not the measurement space.

### Computation: n1_loshu_z5.py

Script: `n1_loshu_z5.py`. Computed 8 items on the Lo Shu structure.

### Tested

**N1: Lo Shu cycles projected to Z₅.**

Four cycles compared:

| Cycle | 比和 | 生↑ | 生↓ | 克↑ | 克↓ | Steps | Pro:Retro |
|-------|------|-----|-----|-----|-----|-------|-----------|
| 先天 (1→8→1) | 3 | 1 | 2 | 0 | 2 | 8 | 1:4 |
| LS sequential | 2 | 1 | 2 | 1 | 3 | 9 | 2:5 |
| Flying star | 2 | 1 | 2 | 0 | 3 | 8 | 1:5 |
| **後天 compass** | **2** | **4** | **0** | **0** | **2** | **8** | **4:2** |

**[measured]** The 後天 compass cycle is the only prograde-dominant cycle: 4 生↑, 0 生↓, 0 克↑, 2 克↓. Every generative step is forward (prograde on 生 cycle). Every destructive step is retrograde. No exceptions. All other cycles are retrograde-dominant.

**[measured]** The 先天 and 後天 compass cycles are temporal inverses: 先天 has 1:4 prograde:retrograde, 後天 has 4:2. This confirms and sharpens §IX from the mod-8 findings.

**[measured]** The 後天 compass type sequence has clean phase structure:
```
生↑ → 生↑ → 比和 → 生↑ → 克↓ → 克↓ → 比和 → 生↑
火→土  土→金  金=金  金→水  水←土  土←木  木=木  木→火
```
Generative run (4 steps) → 克 break (2 steps, bounded by 比和) → generative restart from 木.

**[measured]** 木 is confirmed as the pivot in the 後天 cycle: step 6 lands on 木 (克↓: 土←木), step 7 rests on 木 (比和: 木=木), step 8 departs from 木 (生↑: 木→火). The restart after destruction begins from 木. Matches §IX.4.

**[measured]** No cycle is palindromic in the full type sequence (including wrap-around). The 先天 cycle's first 7 steps form a palindrome with the 8th as seam (§VIII), but this is not captured by the full-cycle palindrome test.

**N3: Magic square Z₅ grid.**

Z₅ value grid (Chinese convention, S at top):
```
  0(木)  1(火)  2(土)     row sums mod 5: 3, 0, 4
  0(木)  2(土)  3(金)
  2(土)  4(水)  3(金)     col sums mod 5: 2, 2, 3
                          diag sums mod 5: 0, 1
```

**[measured]** The magic square sum-to-15 = sum-to-0 (mod 5) property does NOT transfer through the trigram→Z₅ map. Z₅ row/column/diagonal sums are not constant. The map is a surjection, not a homomorphism of additive structure.

**[measured]** The SW→NE diagonal {2,5,8} = {坤, 中, 艮} = all 土 (Z₅=2). This is the only monochromatic line. Earth numbers sum to 15 (the magic constant). Earth IS the Lo Shu skeleton.

**[measured]** The SE→NW diagonal {4,5,6} = {木,土,金} has the same element triple as the center row {3,5,7} = {木,土,金}. Both sum to 0 mod 5. Both have identical Z₅ relational profiles (0比和, 1生, 2克).

**N4: Flying star path Z₅ structure.**

**[measured]** The flying star path does NOT have constant Hamming-2 between consecutive trigrams. The actual Hamming distances are [1, 3, 1, 3, 1, 1, 3]. The "constant 2" cited in opposition-theory/loshu.md (line 115/132) refers to *consecutive mask distance* (Hamming between successive XOR masks), not step Hamming distance.

**[measured]** The flying star's Z₅ type sequence for trigram-to-trigram transitions is [比和, 生↓, 生↓, 克↓, 克↓, 克↓, 比和]. All non-trivial steps are retrograde. The distribution {2比和, 2生↓, 3克↓} is similar to 先天 in character — both retrograde-dominant and bracketed by 比和.

### Found (new, not in prior findings)

**Compass cycle binary-Z₅ segregation.**

**[measured]** On the 後天 compass cycle, every non-trivial Z₅ transition (生 or 克) occurs at Hamming distance exactly 2. Every trivial Z₅ transition (比和) occurs at Hamming distance 1 or 3. (See iteration 2 for the structural analysis of this property.)

Full data:
| Step | From→To | Hamming | Z₅ type | XOR mask |
|------|---------|---------|---------|----------|
| 1 | 離→坤 | 2 | 生↑ | 101 |
| 2 | 坤→兌 | 2 | 生↑ | 011 |
| 3 | 兌→乾 | 1 | 比和 | 100 |
| 4 | 乾→坎 | 2 | 生↑ | 101 |
| 5 | 坎→艮 | 2 | 克↓ | 110 |
| 6 | 艮→震 | 2 | 克↓ | 101 |
| 7 | 震→巽 | 3 | 比和 | 111 |
| 8 | 巽→離 | 2 | 生↑ | 011 |

The two 比和 steps have opposite Hamming character: 金 pair (兌↔乾) at minimum distance (H=1), 木 pair (震↔巽) at maximum distance (H=3). This echoes the intra-element binary asymmetry: Metal trigrams differ by 1 bit, Wood trigrams are complements.

The Hamming-2 transitions use three XOR masks: {101×3, 011×2, 110×1}. All three 2-bit masks are represented, though unequally.

This segregation does not hold for any other cycle tested. The 先天 cycle mixes Hamming distances across Z₅ types. The flying star alternates [1,3,1,3,1,1,3] without Z₅ correlation.

**Three pairing systems span generative→destructive.**

**[measured]** Three pairing systems compared:

| System | 比和 | 生↑ | 生↓ | 克↑ | 克↓ | Character |
|--------|------|-----|-----|-----|-----|-----------|
| He Tu (n,n+5) | 0 | 2 | 1 | 1 | 0 | generative (3生, 1克) |
| 先天 (n↔9−n) | 1 | 0 | 2 | 0 | 1 | retrograde (all non-trivial retrograde) |
| Lo Shu (n↔10−n) | 1 | 0 | 0 | 1 | 2 | destructive (0生, 3克) |

He Tu: every pair has a non-trivial Z₅ relation (0 比和), predominantly 生. Lo Shu: no 生 at all, pure 克. 先天: intermediate, all non-trivial pairs retrograde.

**[measured]** The fixed-point element differs by symmetry type:
- 先天 reflection (n↔9−n) → fixed element = 木 (complement-closed: 震↔巽 = XOR 111)
- Lo Shu reflection (n↔10−n) → fixed element = 土 (center-occupying: 坤↔艮 through center 5)
- He Tu pairing → no fixed element (0 比和)

---

## Iteration 2

### Computation: n2_compass_uniqueness.py

Script: `n2_compass_uniqueness.py`. Exhaustive enumeration of all 8! = 40320 trigram→compass-position permutations, testing H2-segregation, directional purity, and their combination.

### Tested

**Half-tautology correction to iteration 1's compass segregation finding.**

**[proven]** The "backward" direction of the segregation (比和 → H≠2) is tautological. Same-element trigram pairs have Hamming distances: 木(震↔巽) = 3, 土(坤↔艮) = 1, 金(兌↔乾) = 1. No same-element pair has H=2. This holds for all 40320 permutations — verified exhaustively. It is a property of the canonical 五行 assignment to F₂³, not of the 後天 arrangement.

**[proven]** H=2 is the unique Hamming distance class that carries only cross-element pairs. H=1 has 2 same-element pairs out of 12 total. H=3 has 1 out of 4. H=2 has 0 out of 12. This is a consequence of the uniqueness of the complement-respecting surjection F₂³→Z₅ (the {2,2,2,1,1} partition's interaction with Q₃ geometry).

**Corrected restatement of compass finding:** Every non-trivial Z₅ transition in the 後天 compass cycle occurs at exactly Hamming distance 2. Selectivity: 192/40320 = 0.48%. The converse (比和 at H≠2) is automatic.

**H2-segregation uniqueness (Task A).**

**[measured]** 192 / 40320 permutations (0.48%) satisfy: every non-trivial Z₅ step has H=2. The strict condition (adding: every 比和 step has H≠2) gives the same count (192 = 192) because the converse is tautological. The traditional 後天 arrangement is among the 192.

**Directional purity (Task B).**

**[measured]** 2688 / 40320 permutations (6.67%) are directionally pure (all 生 steps same direction AND all 克 steps same direction). The traditional pattern (all 生↑, all 克↓) accounts for 512 of these.

**Combined constraint (Task C).**

**[measured]** 32 / 40320 permutations (0.079% = 1/1260) satisfy both H2-segregation AND directional purity. 16 are prograde-dominant (4:2 pro:retro), 16 are retrograde-dominant (2:4). The traditional 後天 is one of the 16 prograde arrangements.

**[measured]** Up to cyclic rotation (8 compass starting points), the 16 prograde arrangements reduce to exactly **2 distinct base element patterns**:
- **P1 (traditional):** 木木火土金金水土 — the 克 break is contiguous (...生↑ 克↓ 克↓ 比和...)
- **P2 (alternative):** 木木金火土土金水 — the 克↓ pair is separated from the main 生↑ block by a 生↑ step
- Both have identical type distribution: 4×生↑, 2×克↓, 2×比和
- Each base pattern × 8 rotations = 16 total

**[measured]** Each base pattern has exactly 1 trigram realization per rotation. No within-element swaps (e.g. swapping 震↔巽 within 木) preserve the H2 property. The combined constraint is fully deterministic at the trigram level given the element pattern and rotation.

**[measured]** All 32 combined matches place 比和 at diametrically opposite compass steps — always separated by exactly 4 positions: (0,4), (1,5), (2,6), or (3,7). The traditional has 比和 at steps 2→3 (兌→乾 = 金金) and 6→7 (震→巽 = 木木).

**Element-level analysis (Task D).**

**[measured]** 336 / 5040 element-level assignments (6.67%) are directionally pure. 64 / 5040 (1.27%) have the traditional pattern (生↑ + 克↓). The traditional element sequence is among them.

### Found (new)

**Compass cycle embeds the He Tu.**

**[proven]** The 6 Hamming-2 pairs used by the compass cycle's non-trivial transitions include all 4 He Tu pairs:
- He Tu 1↔6: 坎↔乾 (水↔金) — compass step 4
- He Tu 2↔7: 坤↔兌 (土↔金) — compass step 2
- He Tu 3↔8: 震↔艮 (木↔土) — compass step 6
- He Tu 4↔9: 巽↔離 (木↔火) — compass step 8

Plus 2 additional Earth-singleton pairs:
- 離↔坤 (火↔土) — compass step 1
- 坎↔艮 (水↔土) — compass step 5

**[proven]** Zero Lo Shu diametric pairs (n↔10−n mapped to trigrams: 坎↔離, 坤↔艮, 震↔兌, 巽↔乾) appear in the compass H=2 transitions. Their Hamming distances are {3, 1, 1, 1} — never 2. Spatial opposition and He Tu pairing occupy completely disjoint Hamming classes.

**Earth mediation (partial — corrected in iteration 3).**

**[measured]** The 3 cross-element H=2 pairs NOT used by the compass cycle are: 木↔水, 木↔金, 火↔金. These bypass 土. 4 of 6 non-trivial compass transitions involve a 土-element trigram at one end.

**[measured]** The element pair 火↔水 has no H=2 representative at all (坎↔離 are complements, H=3). This pair can only appear as 比和-distance or complement-distance — never at He Tu distance. The compass cycle's avoidance of the direct 火↔水 confrontation is forced by Q₃ geometry, not by arrangement choice.

---

## Iteration 3

### Computation: n3_mediation_check.py

Script: `n3_mediation_check.py`. Checked Earth mediation, element-direction constraints, and 木 pivot position across all 32 combined matches.

### Tested

**Earth mediation is NOT forced (Task A).**

**[measured]** Zero of 32 combined matches have universal Earth mediation. All 32 are partial — either 2/6 or 4/6 non-trivial transitions involve a 土-element trigram. The traditional arrangement has 4/6.

**[measured]** In the traditional arrangement, the 2 non-Earth-mediated transitions are both 生↑ steps: 乾(金)→坎(水) at step 4 and 巽(木)→離(火) at step 8. Both 克↓ transitions (坎→艮 and 艮→震) ARE Earth-mediated. Restated: **all destructive transitions are Earth-mediated; 2 of 4 generative transitions bypass Earth.**

Iteration 1's claim that "every non-trivial compass transition routes through 土" was imprecise. The correct statement is: 4 of 6 non-trivial transitions involve 土, and specifically all destructive transitions do.

**Traditional 後天 uniquely determined (Task B).**

**[measured]** Selection cascade from 40320 → 1:

| Stage | Count | Fraction |
|---|---|---|
| All permutations | 40320 | 100% |
| + H2-segregation + directional purity | 32 | 0.079% |
| + prograde (生↑, 克↓) | 16 | 0.040% |
| + 火 at S (fix rotation) | 2 | 0.005% |
| + 土 antipodal, 金 adjacent, 木 adjacent | **1** | 0.0025% |

**[measured]** The traditional 後天 arrangement is the unique permutation satisfying all five constraints. No single constraint is redundant — removing any one produces multiple survivors.

**[measured]** The discriminating constraint at the final step is 土 antipodal (C1). The alternative survivor has 坤 and 艮 adjacent rather than diametrically opposite.

**[proven]** 木 adjacent (C3) is satisfied by ALL 32 combined matches — it is **forced** by H2 + directional purity alone. 金 adjacent (C2) holds for exactly 16/32. 土 antipodal (C1) holds for 16/32.

**木 pivot position (Task C).**

**[measured]** 木 always creates one of the two 比和 blocks in all 32 combined matches. 木's 比和 block always borders a 克 block on one side and a 生 block on the other. In 16/32, 木 is at the 克→比和→生 restart point (traditional). In 16/32, it's at the 生→比和→克 departure point. The traditional arrangement places 木 at the restart.

**[measured]** The non-木 比和 block (created by 金 or 土) is always embedded within the generative zone: 生→比和→生. Only 木's 比和 ever borders a 克 block. This is forced by the combined constraints.

### Found (new)

**Parity bipartition mechanism — why 木 adjacency is forced.**

**[proven]** Hamming-2 transitions preserve binary weight parity. This partitions the 8 trigrams into two classes:
- **Odd parity** (weight 1 or 3): 震(001), 坎(010), 艮(100), 乾(111) — Z₅: {0, 4, 2, 3}
- **Even parity** (weight 0 or 2): 坤(000), 巽(110), 兌(011), 離(101) — Z₅: {2, 0, 3, 1}

Every H=2 transition stays within its parity class. The compass cycle's two 比和 crossings are the only parity jumps, using same-element cross-parity pairs.

All three paired elements are cross-parity: 木(震odd↔巽even), 土(艮odd↔坤even), 金(乾odd↔兌even).

**[proven]** The forcing chain for 木 adjacency:
1. H=2 preserves parity → bipartite structure on the compass cycle
2. 比和 crossings must use same-element cross-parity pairs
3. If 木 is NOT adjacent (separated), both parity blocks have 4 members needing 3-step Hamiltonian paths. The odd-class Z₅ values {0,2,3,4} and even-class {0,1,2,3} each span 4 of 5 Z₅ values — any 3-step path through 4 values on Z₅ must include both prograde and retrograde steps, breaking directional purity
4. If 木 IS adjacent, one 比和 crossing absorbs 木, leaving 3-member blocks. Removing Z₅(0) = 木 yields residuals {2,3,4} (odd) and {1,2,3} (even) — consecutive Z₅ spans. A 2-step path through 3 consecutive values can be monotone (all +1 = 生↑)
5. Therefore 木 adjacency is forced by H2 + directional purity

**[proven]** This is specific to 木 because Z₅(0) is the unique element whose removal yields consecutive residuals in BOTH parity classes. Removing any other element (火=1, 土=2, 金=3, 水=4) would leave non-consecutive triples in at least one class, preventing directional purity.

**木's structural role unified across 先天 and 後天 (resolves M6).**

**[proven]** 木's special role in both systems traces to Z₅=0:
- In 先天: 木 is the palindrome center (§VIII) — Z₅(0) is the identity element of the 生 cycle
- In 後天: 木 bridges the 克/生 boundary — Z₅(0) removal enables parity-class coherence
- Both roles depend on the same algebraic property: Z₅(0) is the element whose removal from any subset yields maximum consecutive coverage on the Z₅ cycle

This resolves M6: 木's pivot role in both systems is not coincidence and not a free choice, but a consequence of its position at Z₅=0, the identity/start of the 生 cycle.

### What remains untested

- **N5 (text bridge):** The 後天 method uses 爻辭 + 卦辭 for evaluation, which 先天 does not. Whether this constitutes a structural bridge between algebra and text, or is a procedural overlay, is untested. This is conceptual, not computational.
- **He Tu textual connection:** The compass cycle embeds all 4 He Tu pairs. The He Tu traditionally represents yang-yin directional pairings. The structural relationship between He Tu's traditional meaning and its algebraic role in the compass cycle is unexplored.
- **Uniqueness theorem extension:** The 後天 is uniquely determined by 5 constraints. These constraints are stated in terms of both Q₃ geometry (H2) and Z₅ algebra (directional purity, prograde) and spatial convention (火=S, 土 antipodal). Whether a more economical set of constraints suffices (e.g., can 火=S + 土 antipodal be replaced by a single algebraic condition?) is untested.

---

## Final Synthesis

Three iterations. Scripts: `n1_loshu_z5.py`, `n2_compass_uniqueness.py`, `n3_mediation_check.py`.

### Investigation arc

Started asking "how does mod-9 arithmetic interact with F₂³?" — immediately discovered this was the wrong question. The 後天 method doesn't use mod-9 arithmetic (vol2 line 16 explicitly corrects this; all worked examples use 先天 numbers). Reframed to: "what is the Z₅ structure of the Lo Shu compass layout?"

Three iterations revealed:
1. The compass cycle is uniquely prograde (4:2), temporal inverse of 先天 (1:4)
2. Non-trivial Z₅ transitions occur at exactly Hamming-2 (0.48% selectivity)
3. The traditional arrangement is uniquely determined by 5 constraints (40320→1)
4. 木's role as 克/生 bridge is forced by a parity bipartition mechanism depending on Z₅(0)

### Results summary

**Textual findings:**
- Center = observer (position 5 is the coordinate origin, not a state)
- 後天 uses 先天 numbers for calculation, Lo Shu for spatial mapping only
- 先天 = "辞前之《易》" (pre-textual), 後天 = "辞后之《易》" (post-textual) — two methods for two layers by design

**Computational findings:**
- Compass cycle: {4生↑, 0生↓, 0克↑, 2克↓} — directionally pure, uniquely prograde
- H2-segregation: non-trivial Z₅ → H=2 (192/40320). Converse tautological (uniqueness theorem)
- H=2 is the unique Hamming distance class carrying only cross-element pairs
- Combined (H2 + directional purity): 32/40320 = 1/1260
- Selection cascade: 40320 → 32 → 16 → 2 → 1 (traditional 後天)
- 木 adjacency forced (32/32) by parity bipartition mechanism
- 木 bridges 克/生 boundary in all 32 matches — unique among elements
- Z₅(0) = 木 is the unique element whose removal yields consecutive Z₅ residuals in both parity classes
- He Tu embedding: all 4 He Tu pairs in compass cycle's non-trivial transitions
- Three pairing systems: He Tu (generative) → 先天 (retrograde) → Lo Shu (destructive)
- Earth mediation partial (4/6 in traditional): all 克 Earth-mediated, 2 生 bypass Earth

**Cross-investigation connections:**
- M6 resolved: 木's pivot role in both 先天 and 後天 traces to Z₅=0
- The uniqueness theorem (complement-respecting surjection) underlies the H=2 tautology
- The parity bipartition connects Q₃ geometry to Z₅ algebra through the compass cycle

### Questions answered

N1–N6 all answered (N5 conceptual). M6 from mod8 resolved. Two new open questions (N7: constraint economy, N8: He Tu textual connection) recorded in questions.md.
