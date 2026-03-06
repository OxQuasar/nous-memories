# 五行 Structural Analysis — Synthesis

## The Question

The traditional 五行 (Wuxing) system assigns 8 trigrams to 5 elements. This mapping correlates with the bit algebra of hexagram structure (I-component predicts 生/克 at χ²=2209). How much of 五行 is derivable from the algebraic structure of Z₂³, and how much is an external cosmological overlay?

## The Answer

**五行 is 78% algebraic, 22% cosmological. The cosmological input is exactly one binary choice.**

H(五行) = 2.25 bits = 1.75 algebraic + 0.50 cosmological.

**The precise algebraic boundary:** 3 Boolean functions can produce 五行, but 3 linear functions cannot. One non-linear function is necessary and sufficient. Every standard algebraic construction on Z₂³ — subgroup quotient, kernel of linear map, automorphism orbit, symmetric function — is provably incapable of generating the partition.

---

## Architecture of the 五行 Partition

### The Three-Layer Decomposition

The 五行 map from 8 trigrams to 5 elements can be built in exactly three steps:

**Layer 1 — b₀⊕b₁ parity (1.0 algebraic bit):**
Separates trigrams into two cosets of Z₂³:
- Parity 0: {Kun(000), Dui(011), Gen(100), Qian(111)} → {Earth, Metal}
- Parity 1: {Zhen(001), Kan(010), Li(101), Xun(110)} → {Wood, Fire, Water}

This parity IS the I-component at the trigram level. It separates the "stable" elements (those whose trigram pairs are cube edges, XOR=100) from the "dynamic" elements (complement pairs and singletons).

**Layer 2 — b₀ within parity-0 (0.75 algebraic bits):**
Within the even-parity coset, b₀ cleanly separates:
- b₀=0: {Kun(000), Gen(100)} → Earth
- b₀=1: {Dui(011), Qian(111)} → Metal

This is a linear functional on the coset. After these two algebraic steps, Earth and Metal are fully resolved.

**Layer 3 — One binary choice within parity-1 (0.50 cosmological bits):**
The odd-parity coset {001, 010, 101, 110} contains exactly 2 complement pairs:
- {Zhen(001), Xun(110)} — XOR = 111
- {Kan(010), Li(101)} — XOR = 111

五行 chooses to keep {Zhen, Xun} together (= Wood) and split {Kan, Li} into singletons (Water, Fire). The alternative — keeping {Kan, Li} together and splitting {Zhen, Xun} — is algebraically equivalent. **No bit operation distinguishes these two options.** This is the sole cosmological input.

### Why This Choice?

The ranking analysis answers this. Among all 420 partitions of 8 trigrams with shape (2,2,2,1,1):
- Traditional 五行 ranks **#5 for alignment with Later Heaven compass** (top 1.2%)
- The 4 partitions that rank higher all keep 3 of 4 Later Heaven quadrant pairs — but every one includes {Kun, Li} (South), mixing Earth and Fire. They have maximum compass alignment but no coherent elemental interpretation.

**五行 is the most Later-Heaven-aligned partition that respects elemental identity.** The cosmological binary choice is: which compass pairing to respect. East(Zhen,Xun) = Wood stays together; South(Kun,Li) splits across Earth and Fire.

The alternative partition (keep Kan+Li, split Zhen+Xun) loses on every metric: MI(LH) drops 1.75→1.50, MI(Basin) drops 1.00→0.75, LH quadrant pairs kept drops 2→1.

---

## Impossibility Results (Phase C)

### What cannot produce 五行

| Construction | Result | Reason |
|---|---|---|
| Subgroup quotient Z₂³/H | **Impossible** | Quotients have equal-size classes; 五行 has sizes {2,2,2,1,1} |
| Kernel of linear map | **Impossible** | Preimages of a linear map are cosets of equal size |
| Orbit of any element of Aff(3,F₂) | **Impossible** | Orbit shape (1,1,2,2,2) does not exist among the 8 realized orbit shapes |
| 2 Boolean functions | **Impossible** | 2 bits give at most 4 classes; 五行 has 5 |
| 3 linear (affine) functions | **Impossible** | Only 1 non-trivial linear function is constant on all 5 classes (= b₀⊕b₁) |
| Any number of symmetric functions | **Impossible** | Yang-count classes cross-cut 五行; popcount cannot separate Wood from Fire/Water |

### What can produce 五行

| Construction | Result |
|---|---|
| 3 arbitrary Boolean functions | **Possible** — minimum sufficient |
| 2 linear + 1 non-linear Boolean function | **Possible** — the constructive decomposition |

**The boundary is sharp:** one non-linear Boolean function is both necessary and sufficient (given the 2 linear functions b₀⊕b₁ and b₀).

---

## Key Structural Findings

### Geometry on Z₂³ (Probe 1)

Element classes occupy three geometric types on the 3-cube:

| Type | Elements | XOR mask | Hamming d | Character |
|------|----------|----------|-----------|-----------|
| Edge pair | Earth, Metal | 100 | 1 | Differ in bit 2 only |
| Body diagonal | Wood | 111 | 3 | Complement pair |
| Singleton | Fire, Water | — | — | Mutual complements (XOR=111) |

Neither 生 nor 克 is a geometric operation (rotation, reflection, translation) on the cube. Both use 5 of 7 possible XOR masks. But they partition those masks cleanly:
- **生-exclusive: {011, 100}** — both preserve b₀⊕b₁ parity
- **克-exclusive: {010, 110}** — both break b₀⊕b₁ parity
- **Shared: {001, 101, 111}**
- Together: all 7 nonzero masks

**生 is parity-respecting; 克 is parity-breaking.** The algebraic Layer 1 of 五行 is precisely what separates the geometric character of generation from overcoming. This connects to the traditional reading: generation flows within the stable/dynamic divide; overcoming crosses it.

### Inner Space Element Pairs (Probe 2)

Of 25 possible (lower element, upper element) pairs, only **12 are realized** on the 16-node inner space. The overlap constraint (lower and upper nuclear share 2 bits) combined with the element assignment determines which.

**Basin-element correlation:**
- Fixed-point basins (Kun/Qian): only 比 (same) and 克 (overcoming) relations between nuclear elements. Upper nuclear is element-pure (forced by overlap constraint). Lower nuclear varies — the free bit toggles between the "home" element and Wood.
- Cycle basin: all 4 non-比 relation types (生→, ←生, 克→, ←克). This is the only basin with generative flow.

**Wood as universal intruder:** In both fixed-point basins, Wood enters via the lower nuclear's free bit. Wood has 克 relations with both Earth (Wood overcomes Earth) and Metal (Metal overcomes Wood). Result: **lower nuclear convergence is 100% 克 when not 比 — zero 生.** Convergence strips; generation persists only where resolution is impossible (the Cycle).

### Partition Comparison (Probe 3)

Six partitions of 8 trigrams were compared via mutual information:

| Partition | H (bits) | Best predictor of Wuxing? |
|-----------|----------|---------------------------|
| Wuxing | 2.25 | — |
| Later Heaven | 2.00 | Best single: H(W\|LH) = 0.50 (77.8% captured) |
| Complement pair | 2.00 | Second: H(W\|Comp) = 0.75 (66.7%) |
| Yang count | 1.81 | H(W\|Yang) = 1.19 (47.2%) |
| Basin(TT) | 1.50 | H(W\|Basin) = 1.25 (44.4%) |
| b₀⊕b₁ parity | 1.00 | H(W\|par) = 1.25 (44.4%) |

**五行 is not informationally unique** — four pairs of partitions fully determine it (H=0):
1. Yang count + Complement pair
2. Basin(TT) + Later Heaven
3. Later Heaven + Complement
4. Later Heaven + b₀⊕b₁ parity

**Key orthogonality: Basin(TT) ⊥ b₀⊕b₁ parity** (MI = 0). Basin depends on (b₂, b₀) homogeneity; parity depends on b₀⊕b₁. They share b₀ but use it in structurally independent ways.

### Directed Graphs on Inner Space (Probe 4)

The five relation types partition K₈ (complete digraph on 8 trigrams) into {6, 12, 12, 13, 13} edges (56 total).

On the 16-node inner space, 互 (hugua) convergence edges carry:
- **克 on ≥1 nuclear position: 12/14 edges (86%)**
- **生 on ≥1 nuclear position: 4/14 edges (29%)**
- **Same relation on both positions: 4/14 edges**

By basin:
- Kun: {(克→,比)×2, (比,比)×1} — overcoming or identity
- Qian: {(←克,比)×2, (比,比)×1} — symmetric to Kun
- Cycle: all 8 edges distinct, mixing all relation types

The dominant combined relation types across all 240 ordered pairs on inner space are {(←克,生→), (克→,←生)} at 14 each — **克 and 生 are anti-correlated across nuclear positions.** When one nuclear trigram is being overcome, the other tends to be generating.

### Quotient Structure (Probe 5)

**Linear symmetries preserving 五行:** 1 (identity only)
**Affine symmetries:** 2 (identity + translation by 100)

The only non-trivial symmetry is x → x ⊕ 100 (bit-2 swap), which swaps within Earth (Kun↔Gen) and within Metal (Dui↔Qian). This is the same bit-2 degree of freedom that makes Earth and Metal both edge pairs.

**Unlabeled partition automorphisms:** |Aut| = 8, rank 29/420 (above median of 6).

---

## Structural vs Cosmological: The Verdict

### What the algebra forces (78%)

Given only Z₂³ and its linear structure:
1. **b₀⊕b₁ parity** creates two cosets of size 4. This is a linear functional — purely algebraic.
2. **b₀ within the even coset** creates a further clean 2+2 split. Also linear.
3. Together these produce a partition {2, 2, 2+1+1} where the two size-2 classes and the size-4 remainder are fixed.
4. The parity feature predicts which XOR masks 生 uses exclusively vs which 克 uses exclusively.
5. The basin orthogonality (Basin ⊥ parity) is forced by the bit structure.

### What requires cosmological input (22%)

One binary decision: within the odd-parity coset {001, 010, 101, 110}, which of the two complement pairs stays together?

The traditional choice ({Zhen, Xun} = Wood) is the one that maximizes alignment with the Later Heaven compass arrangement. This choice has no algebraic basis — it comes from the directional cosmology that places Zhen at East and Xun at Southeast, making them compass neighbors, while Kan (North) and Li (South) are compass opposites.

### The Character of 五行

五行 is not a quotient of Z₂³ by any subgroup or algebraic relation — the unequal class sizes (2,2,2,1,1) rule this out. It is not generated by any automorphism orbit. It is not the kernel or cokernel of any linear map. No number of symmetric (popcount-based) functions can produce it.

What it IS: **a maximally compass-aligned partition of Z₂³, constrained to respect elemental identity, built from two linear features plus one non-linear cosmological binary choice.** The algebraic skeleton determines 78% of the structure; the Later Heaven compass provides the final 22%.

The correlation with the I-component (χ²=2209 at the hexagram level) follows because the I-component IS b₀⊕b₁ parity lifted to pairs of trigrams — it is exactly Layer 1 of the decomposition. The deeper correlations between 五行 and hexagram dynamics arise from how this parity interacts with the overlap constraint of nuclear trigrams, which forces the 12/25 element-pair realization, the basin-specific relation distributions, and the 克-dominated convergence structure.
