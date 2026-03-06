# Q4: Additional Traditional Coordinate Systems and the Trigram Relational Space

## 1. The Test

The trigram relational space is characterized by two axioms on three fixed-point-free involutions (Fu Xi complement ι₁, KW diametric ι₂, He Tu ι₃), determining a unique S₄ action on 4 blocks of 2: B1={Kun,Zhen}, B2={Gen,Dui}, B3={Kan,Li}, B4={Xun,Qian}. The structure has Aut = Z₂; adding a polarity partition P₊={Kan,Zhen,Dui,Li} / P₋={Kun,Gen,Qian,Xun} makes it fully rigid (Aut = {id}).

**Q4 asks:** Do additional traditional coordinate systems independently reproduce this structure or determine the polarity?

Three classification levels:
- **Compatible**: assignments respect the 4-block system
- **Informative**: independently determines P₊/P₋ (breaks the Z₂ ambiguity without reference to Lo Shu, binary, or compass geometry)
- **Redundant**: carries no structural information beyond what's already determined

The key methodological distinction: if a system maps to trigrams *via* the five-element/direction layer, and that layer already determines the blocks, then block compatibility is trivially forced. Only structure that arrives through an independent path counts as informative.

---

## 2. Systems Tested

Four candidate systems were evaluated across three rounds of computation and two rounds of expert consultation.

### 2.1 天干 (Heavenly Stems)

10 stems with yin/yang polarity and five-element assignment (2 per element). Traditional 合化 (combining transformation) pairs: 甲己→Earth, 乙庚→Metal, 丙辛→Water, 丁壬→Wood, 戊癸→Fire.

**Mapping:** Each stem maps to a trigram via element+polarity — yang Wood (甲)→Zhen, yin Wood (乙)→Xun, yang Metal (庚)→Qian, yin Metal (辛)→Dui, etc. The mapping is well-defined for 8 of 10 stems. Fire and Water each have only one trigram (Li and Kan respectively), so both yang and yin stems of these elements collapse to the same trigram.

**Source:** Standard five-element/yin-yang correspondences, verified via web search.

### 2.2 地支 (Earthly Branches)

12 branches with element, yin/yang, season, and direction assignments. Three pairing structures examined:

- **六冲 (Six Clashes)**: 6 diametrically opposed pairs on the 12-branch circle (子午, 丑未, 寅申, 卯酉, 辰戌, 巳亥)
- **六合 (Six Harmonies)**: 6 adjacent-branch combining pairs (子丑, 寅亥, 卯戌, 辰酉, 巳申, 午未)
- **三合 (Triple Harmonies)**: 4 frame-element triples (申子辰→Water, 亥卯未→Wood, 寅午戌→Fire, 巳酉丑→Metal)

**Mapping:** The 24 Mountains (二十四山) Luo Pan compass system, which assigns branches to trigram sectors: 1 branch per cardinal trigram (Kan, Zhen, Li, Dui) and 2 per intercardinal trigram (Gen, Xun, Kun, Qian). Verified against standard Luo Pan references.

### 2.3 Systems not tested

**28宿 (Lunar Mansions)** and **24节气 (Solar Terms)** were not computationally tested. Both connect to trigrams through directional quadrants → elements → trigrams, the same intermediary layer that rendered all tested systems redundant. The argument by mechanism is sound (confirmed by sage evaluation) but noted as "argued convincingly" rather than "demonstrated."

---

## 3. Results per System

### 3.1 天干 — Redundant

**Mapping problem:** The 10→8 stem→trigram mapping is category-incompatible. Stems encode element × polarity as independent axes; trigrams entangle them. Fire and Water each absorb both yang and yin stems (丙 and 丁 both → Li; 壬 and 癸 both → Kan), destroying the stem system's distinctive yin/yang information at precisely the two singleton-element trigrams.

**合化 analysis:** The 5 combining pairs on stems induce only 3 non-trivial trigram pairs (the Fire/Water pairs collapse to trivial self-pairs). These 3 pairs cannot form a fixed-point-free involution on 8 elements (requires 4 disjoint pairs). The Earth stem assignment (which of Kun/Gen gets 戊 vs 己) is ambiguous, introducing a free parameter that shouldn't exist in clean structure.

**Block compatibility:** Forced through the element layer — not informative.

**Polarity:** Stem yin/yang fails to determine P₊/P₋ because Li and Kan each receive both polarities.

**Verdict: Redundant.** The 10→8 collapse prevents the stem system from carrying any structural information not already present in the five-element partition.

### 3.2 地支 六冲 — Redundant

**Result:** The 6 六冲 branch pairs, mapped through the 24 Mountains, produce exactly the 4 pairs of ι₂ (KW diametric involution): Kan↔Li, Gen↔Kun, Zhen↔Dui, Xun↔Qian. Two branch pairs (寅↔申 and 辰↔戌) duplicate existing pairs (Gen↔Kun and Xun↔Qian respectively) due to the 2-to-1 mapping at intercardinal sectors.

**Explanation:** 六冲 is diametric opposition on the 12-branch circle. The 24 Mountains maps branches to the Later Heaven Bagua. Diametric on the branch circle = diametric on the Bagua = ι₂. The reproduction is geometrically tautological.

**Verdict: Redundant.** Reproduces a known involution by geometric necessity.

### 3.3 地支 三合 — Redundant

**Result:** Each of the 4 frame-element triples (Water, Wood, Fire, Metal) maps to a triple of trigrams spanning 3 of 4 blocks. No triple is contained within a single block. The 4 triples together cover all blocks, but the coverage pattern is generic — not distinguished from what random triples would produce.

**Verdict: Redundant.** Generic block coverage, not new structure.

### 3.4 地支 六合 — Compatible, Not Informative

This was the most structurally promising system, investigated across all three rounds.

**Round 1 findings:**
- 六合 induces 6 edges on the trigram graph with **zero overlap** with all 16 involution edges (from ι₁, ι₂, ι₃, τ). It lives entirely in the complement of the involution graph within K₈.
- The graph is bipartite, all edges cross blocks, degree sequence [2,2,2,2,1,1,1,1].
- Not a clean involution (some trigrams paired with multiple others).

**Round 2 findings:**
- The degree-2 set = {Gen, Kun, Qian, Xun} = P₋ exactly.
- The degree-1 set = {Dui, Kan, Li, Zhen} = P₊ exactly.
- The unique perfect matching extractable from the 6 edges is {Dui↔Xun, Gen↔Kan, Kun↔Li, Qian↔Zhen} — **not** in the S₄ group ⟨ι₁, ι₂, ι₃⟩.
- Two extended matchings (3 六合 edges + 1 unclaimed edge) are both in S₄, but are existing group elements, not new.
- This appeared to be an independent determination of P₊/P₋ through graph theory alone.

**Round 3 stress test (three checks):**

1. **Yin/yang circularity:** Ruled out. Yang and yin branches distribute identically across P₊ and P₋ (ratio 2:4 in both cases, matching the base rate). Branch yin/yang carries zero information about polarity. The degree-structure result is not a yin/yang artifact.

2. **Mapping dependence:** Confirmed. Under alternative mappings (element-based, swapped), the degree structure does **not** recover P₊/P₋. The result requires the 24 Mountains mapping specifically.

3. **Root cause:** The 24 Mountains assigns 2 branches to each intercardinal trigram (= P₋) and 1 to each cardinal trigram (= P₊). Since 六合 pairs adjacent branches, more branches → higher degree. The causal chain is: compass geometry → branch-count asymmetry → 六合 degree → P₊/P₋. The branch-count asymmetry **is** the cardinal/intercardinal distinction in another guise.

**The zero-overlap property:** 六合 edges and involution edges are complementary on the Later Heaven Bagua circle — 六合 pairs adjacent positions, involutions pair distant positions. This is a geometric consequence of adjacency vs. opposition, not independent algebraic structure.

**Verdict: Compatible but not informative.** P₊/P₋ recovery traces through compass geometry, not through an independent path. No new involution produced.

---

## 4. The Polarity Partition

**No tested system independently determines P₊/P₋.**

Three known paths to the polarity partition exist:
1. **Spatial:** cardinal directions (= P₊) vs. intercardinal (= P₋) — compass geometry
2. **Algebraic:** the non-trivial automorphism τ = ι₂∘ι₃ is non-affine on Z₂³, so the binary structure rules it out
3. **Elemental:** τ disrupts 生/克 cycle assignments, so the five-phase structure rules it out

All three break the same Z₂ symmetry. They carry the same one bit of orientation information.

The 六合 degree-structure result appeared to offer a fourth path, but Round 3 showed it routes through path (1) — the branch-count asymmetry in the 24 Mountains encoding is the cardinal/intercardinal distinction restated. The yin/yang channel is verified clean (zero information about polarity), but this is a negative result — it eliminates a possible circularity without providing a new independent witness.

**The element/direction layer is the unique traditional conduit for the orientation bit.** The algebraic path (Z₂³ non-affinity) is arguably a modern analytical frame, not a traditional coordinate system. Whether any traditional system determines P₊/P₋ without going through compass geometry remains an open question — but the evidence from Q4 suggests the polarity partition is fundamentally spatial in the traditional systems.

---

## 5. Overall Verdict

**The S₄ block structure does not extend beyond the core three involutions.**

Additional traditional coordinate systems are **compatible** with the structure — but only because every system routes through the element/direction layer that already determines it. No system produces:
- A genuinely new involution independent of ⟨ι₁, ι₂, ι₃⟩
- An independent determination of P₊/P₋ that doesn't trace back to compass geometry
- Any structural information not already present in the two-axiom characterization

The pattern is consistent and has a clear structural explanation: the three involutions + polarity partition leave zero degrees of freedom (Aut = {id}). There is nothing left for additional systems to determine. They can only be compatible (consistent with the rigid structure) or incompatible (which would signal an error in the traditional correspondences). Every tested system is compatible.

**The strongest claim Q4 supports:**

> The S₄ block structure and the three generating involutions are the complete relational content of the trigram system. Additional traditional coordinate systems (天干, 地支 六冲/六合/三合) are compatible with this structure but carry no independent structural information beyond the element/direction assignments that already determine it. The polarity partition P₊/P₋ is not independently recoverable from any tested traditional system without routing through compass geometry. The two-axiom characterization remains minimal and complete: nothing tested requires a third axiom, and nothing tested makes the third axiom (polarity) derivable.

---

## 6. Implications for the Trigram Space Characterization

### The tradition's consistency is structurally necessary

If the underlying object has Aut = Z₂ (or {id} with polarity), then any faithful coordinatization is forced into the same assignments. The convergence of multiple traditional systems is a **theorem about the object**, not merely a fact about the tradition's design process. The S₄ rigidity is sufficient to explain the observed consistency. Whether it is also the historical cause is underdetermined by structural evidence alone — but Occam favors the structural explanation.

### The two axioms are complete

No additional axiom is needed from any tested traditional system. The characterization from invariants.md stands:

> An 8-element set with three distinguished involutions, two of which commute, the third sharing exactly one pair with one of them and none with the other.

Everything traditional is either generated by these three involutions or is compatible with them by construction.

### The polarity partition remains external

The P₊/P₋ partition requires Axiom 3 (orientation). No traditional system tested provides a new, independent path to this axiom. The three known paths (spatial, algebraic, elemental) all break the same Z₂. The polarity partition appears to be **irreducibly spatial** in the traditional systems — always routing through the cardinal/intercardinal distinction.

### Distinguishing self-consistency from structural constraint

Q4 helps separate two claims:
- "The tradition is self-consistent" — trivially true if all systems route through the same element/direction layer
- "The structure constrains the tradition" — the stronger claim: S₄ rigidity forces compatibility

The evidence supports the stronger claim. The structure doesn't just happen to be consistent — it **must** be, because Aut = Z₂ leaves only one degree of freedom, and the element/direction layer fixes it.

---

## 7. Open Questions for Q3 (n=6 Triple-Involution Analysis)

The n=3 characterization is now fully tested at its own scale. The next frontier is n=6.

1. **Does the triple-involution framework extend to hexagrams?** The hexagram space has its own involutions: complement (XOR 111111), reversal (flip upside down), and their composition (comp∘rev). These are three fixed-point-free involutions on 64 elements. Do they satisfy analogous overlap and commutation axioms? What group do they generate? What block system emerges?

2. **The cross-scale divergence.** n=3 chose complement for Fu Xi pairing (max strength); n=6 chose reversal for KW pairing (weight preservation). Is there a principle that generates both choices from the same source? The phase transition at n=5 (KW-style goes from mediocre to extreme) is noted but unexplained.

3. **The missing mask at n=3.** The nonzero element 011 (= e₂+e₃) of Z₂³ is the only one not used by any involution pair. Is this gap forced by the S₄ block structure, or does it carry independent information? At n=6, is there an analogous gap?

4. **Block structure at n=6.** The 64 hexagrams have known groupings: 32 KW pairs, 8 nuclear-trigram classes, element assignments. Do any of these correspond to a block system under the n=6 involution group, analogous to the 4 blocks of 2 at n=3?

5. **Axiom unification.** Can the two n=3 axioms (overlap pattern + commutation) be derived from a single principle? And if so, does that principle have a natural n=6 formulation?

---

## Appendix: Computational Artifacts

All scripts and intermediate results are in `memories/iching/spaceprobe/q4/`:

| File | Content |
|------|---------|
| `round1_stems_branches.py` | 天干/地支 mapping and analysis |
| `round1_liuhe_deep.py` | 六合 edge analysis and zero-overlap computation |
| `round2_liuhe.py` | 六合 degree structure, bipartition, perfect matchings |
| `round3_stresstest.py` | Yin/yang circularity, alternative mappings, root cause |
| `round1_results.md` | Round 1 detailed findings |
| `round2_results.md` | Round 2 detailed findings |
| `round3_results.md` | Round 3 stress-test findings |
