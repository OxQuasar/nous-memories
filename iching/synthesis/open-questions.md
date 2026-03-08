# Open Questions

## Central thread

Structure → incompleteness → curvature → specificity → meaning.

The algebraic characterization is extensive: Z₂⁶ with shell/core projections, 五行 coordinates, basin convergence, palace walks, 六親 near-bijection. Two divination systems exhaust the hexagram's information through the only two primitive projections available (proven algebraically, confirmed historically). Orthogonality between shell and core is confirmed. Temporal curvature is characterized: three sources, one softened by 日辰 to a 1/5 residual (proven as theorem). The single text↔algebra bridge is 凶×basin (irreversibility↔irreversibility).

The open territory is: **quantifying the curvature** (H¹ computation, optimality) and remaining structural questions. The meaning layer (用神, S₄ involutions) is now formalized.

---

## 1. Formal H¹ computation

**Status: open, lower priority**

The presheaf is now well-characterized qualitatively and all three curvature sources are quantified (用神 projection: 45/20/35; seasonal ceiling: 2/5→4/5; palace holes: 16:32:16). What remains is the formal cohomological computation. Lower priority given the orthogonality wall — the shell-layer presheaf cannot see core-layer dynamics, limiting the interpretive reach of H¹.

### Proposal

For each hexagram:
1. Construct the reading-context presheaf. Context = (season, day-branch, 用神) triple. Now 5 × 12 × 5 = 300 contexts per hexagram (expanded from the original 25 by including 日辰).
2. Compute H¹ — quantifies *how much* local views fail to cohere.
3. Compare H¹ across palaces and basins. Does the Cycle basin (partially resolved Fire/Water conflict) have different cohomological obstruction than fixed-point basins?
4. Check whether H¹ varies with palace rank / 互 depth.

### The optimality question

Does the specific combination of Z₅ torsion + palace holes + 用神 projection maximize discriminative power for some natural measure? Or is any nonzero curvature sufficient? The F_total = 12 conservation and n_zero = {15,17,19} distribution suggest rigidity, but this hasn't been tested against a natural information-theoretic criterion.

---

## 2. Cycle basin's updated epistemological status

**Status: partially resolved**

Previously: permanently conflicted. Fire↔Water mutual 克 means the two attractor elements can never both be seasonally strong.

Now: 日辰 partially resolves this. Fire AND Water simultaneously promotable in 16/60 (27%) of (season, day-branch) pairs. The Cycle basin goes from "permanent irresolution" to "usually irresolved, sometimes both accessible."

### Open questions

- Does this change the relative difficulty of reading Cycle-basin hexagrams in practice?
- Is the 27% resolution rate acknowledged in the tradition?
- The depth gradient showed the boundary layer (depth-1) carries peak 凶. For Cycle-basin hexagrams, is there an analogous "resolution layer" where 日辰 most often resolves the conflict?

---

## 3. The 納甲 modification

**Status: documented, mechanism unclear**

京氏易傳 uses universal upper trigram branch offset +3 (63/63 match). 火珠林 modified to 乾/坤-only, gaining one unique 六親 word (58→59/64). This is likely a deliberate optimization.

- When did this modification occur?
- Is the additional unique 六親 word functionally important for specific question types?
- Does the modification interact with the 日辰 ceiling-breaking mechanism?

---

## Resolved

### R1. Do the dropped 京氏 layers carry independent information?
**No.** H(all 5 fields | palace, rank) = 0.0000 bits. 火珠林's compression was lossless. (jingshiyizhuan workflow)

### R2. Does the full 京氏 temporal system resolve the 2/5 ceiling?
**No.** Finer notation repackages the same pentacyclic structure. Breaking the ceiling requires information orthogonal to 五行. (jingshiyizhuan workflow)

### R3. Are the astronomical assignments algebraically determined?
**Yes.** Each is a cyclic quotient of the palace walk: Q∈Z₃, planets∈Z₅, mansions∈Z₂₈, 建始∈Z₆₀. Zero design freedom in stepping; only palace base values are free. (jingshiyizhuan workflow)

### R4. Original vs modified 納甲 rule
**Discovery:** 京氏易傳 uses universal upper trigram branch offset +3 (63/63 match). 火珠林 modified to 乾/坤-only, gaining one unique 六親 word (58→59/64). Likely deliberate optimization. **New sub-question promoted to §3 above.** (jingshiyizhuan/findings.md §3)

### R5. Only two hexagram-reading methods exist
**Confirmed algebraically and historically.** Shell (3+3 trigram split) and core (1+4+1 nuclear overlap) are the only two primitive projections on the 3+3 factorization of Z₂⁶. Chinese sources independently classify hexagram divination into exactly 六爻/納甲法 and 梅花易數 — no third method. (huozhulin/findings.md, closure theorem)

### R6. The decisive test — text ↔ algebra
**MIXED.** The oldest textual layers partially encode algebraic structure, but only through 凶×basin (p=0.0002). All deeper constructs (kernel, palace, I-component on embeddings) are null. The bridge is through irreversibility only. The depth gradient is confirmed (p=0.013): peak 凶 at depth-1 (boundary layer), zero at attractors. Three independent channels surface the I-bit partition across 700+ years. (synthesis Probe 1)

### R7. Does 日辰 break the 2/5 ceiling?
**Yes — proven as theorem.** Maximum rises from 2/5 to 4/5. The excluded element alternates between 休 (exhausted source) and 死 (conquered object). 囚 (opposition) is always representable. 梅花 inherits 2/5. Pipeline asymmetry: 梅花 curves domain, 火珠林 curves codomain. Orthogonality wall untouched. (synthesis Probe 4)

### R8. Contextual obstruction × 凶
**NULL — predicted by orthogonality.** F_total = 12 conservation law. n_zero determined by missing-type count (16:32:16). Shell-layer measures cannot see core-layer 凶 signal — confirmed as algebraically orthogonal projections. (synthesis Probe 2)

### R9. 用神 mapping structure
**STRUCTURED — by 生克 cycle.** Auxiliary = 生-preimage (σ⁻¹). 忌神 = 克-preimage. 兄弟 (self) excluded as reference frame with 0 domains. 官鬼+妻財 = 15/22 = 68% of all domains. Structural space symmetric (2/5 suppression, 1/5 日辰-克, uniform across types). ALL asymmetry enters through 用神 projection's domain weighting (8:7:4:3:0). Gen palace darkest (missing 妻財+官鬼 = 68% of domains unreadable). Triad diagnostic: 45.3% full, 19.9% blind, 34.8% degraded. 兄弟's absence benign (0 domains). (synthesis Probe 3)

### R10. S₄ × 五行 involutions
**COMPLEMENT IS ANTI-AUTOMORPHISM.** π∘σ∘π⁻¹ = σ⁻¹, where π = (Earth↔Metal)(Fire↔Water)(Wood). Complement reverses 生 to 克, preserves 比/生/克 category (0% hexagram-level disruption), preserves b₀⊕b₁ parity universally. Semantic gap (reverse 0.720 > complement 0.680 > rev∘comp 0.673) tracks concrete visual identity, not abstract relational structure — Tuan perceives sameness through concrete trigram identity, not 五行 category preservation. Wood = fixed point of anti-automorphism, hinge of 生↔克 conjugation. MI correction: 0.750 bits lost under complement pairing = within-pair element identity (Layer 2), NOT cosmological choice (Layer 3, which is preserved). As function, complement preserves ALL 五行 information (MI=2.250). (synthesis Probe 5)
