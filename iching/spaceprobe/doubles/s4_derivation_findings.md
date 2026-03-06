# S₄ Derivation Test: Findings

## Question
Does S₄ follow from recursive binary splitting (the derivation chain's claim)?

## Answer: CONSTRAINED — not forced, not freely chosen

S₄ requires the involution axioms. The tree alone doesn't produce it, but once the axioms are accepted, S₄ is inevitable.

---

## Test 1: Tree → S₄ blocks? **NO**

| Property | Binary tree | S₄ blocks |
|----------|------------|-----------|
| Block pairing | Single-bit-flip siblings | Mixed XOR masks (100, 111) |
| Hamming distance | Uniform: all pairs distance 1 | Mixed: two at distance 1, two at distance 3 |
| Block permutation group | S₂ ≀ S₂ (order 8) | S₄ (order 24) |

- **0 of 48 tree labelings** (6 bit orderings × 8 flip conventions) reproduce S₄ blocks.
- The gap is structural: tree siblings are always uniform (same XOR mask), but S₄ blocks use two different masks.
- The tree automorphism group has order 128 (on 8 leaves), with block action of order 8 — three times smaller than S₄.

## Test 2: S₄ inside AGL(3,2)? **NO** (for the traditional S₄)

- AGL(3,2) = Z₂³ ⋊ GL(3,2) has order 1344. It contains **280 S₄ subgroups**.
- **No pair partition** is preserved by the full AGL(3,2) — every S₄ subgroup is properly contained.
- The **traditional S₄ is NOT among the 280** — it's not a subgroup of AGL(3,2).

Why: ι₁ (complement, x→x⊕111) and ι₃ (He Tu) are affine maps, but **ι₂ (KW diameters) is non-affine**. The traditional S₄ escapes the affine group.

**Block structure insight:**
- AGL(3,2)'s 280 S₄ subgroups use 63 distinct block systems.
- The 7 most common (24 S₄ subgroups each) are **coset partitions** — all 4 pairs share a single uniform XOR mask. These correspond to the 7 nonzero elements of Z₂³.
- The traditional blocks {Kun,Zhen}, {Gen,Dui}, {Kan,Li}, {Xun,Qian} have **mixed XOR masks** (100 and 111) — NOT a coset partition. This is what forces the traditional S₄ outside AGL(3,2).

## Test 3: FPF involution triples → S₄? **26.9% (plurality)**

Generated group order distribution over all 187,460 unordered FPF involution triples:

| Order | Count | Fraction | Identity |
|-------|-------|----------|----------|
| 24 | 50,400 | **26.89%** | **S₄** |
| 168 | 47,040 | 25.09% | PSL(2,7) = GL(3,2) |
| 48 | 30,240 | 16.13% | |
| 64 | 20,160 | 10.75% | |
| 16 | 15,120 | 8.07% | |
| 32 | 10,080 | 5.38% | |
| 8 | 8,610 | 4.59% | |
| 12 | 5,040 | 2.69% | |
| 6 | 560 | 0.30% | |
| 4 | 210 | 0.11% | |

- S₄ is the **most common single outcome** but far from forced (~1 in 4).
- All order-24 groups generated this way are S₄ (verified: no A₄×Z₂ or SL(2,3)).
- Of the S₄ triples, only **0.95%** (480/50,400) have complement-pair block systems.

### Axiom effect

Applying the two axioms from `invariants.md`:
- **20,160 triples** (10.75%) satisfy both axioms (under some role assignment).
- **100% of those generate S₄.**
- The axioms are perfectly selective: they filter to exactly S₄, with zero false positives.

---

## Structural Assessment

### The derivation gap

```
3-fold binary splitting
    ↓ (forced)
8 elements with Z₂³ structure
    ↓ (tree gives S₂≀S₂, order 8)
    ✕ S₄ not reachable from tree alone
    
8 elements + 3 FPF involutions
    ↓ (~27% chance)
    S₄ (most common but not forced)
    
8 elements + 3 FPF involutions + 2 axioms
    ↓ (100% forced)
    S₄ (inevitable)
```

### Where the empirical content lives

The axioms (overlap pattern (1,0,0) + ι₂∘ι₃ commutation) carry exactly the information needed to bridge from "8 elements" to "S₄ on those elements." The tree structure contributes nothing to S₄ beyond the 8-element set itself.

Moreover, the traditional S₄ is **non-affine** — it doesn't respect the Z₂³ group structure at all (ι₂ is not an affine map). So the binary structure and the S₄ structure are **genuinely independent** structures on the same set. The binary splitting gives you the set; the involutions give you S₄; and these two structures don't interact via any natural algebraic homomorphism.

### Correction to invariants.md: τ ≠ block involution

The claim "The blocks are the pairs of τ = ι₂∘ι₃" is **incorrect**.

| | τ = ι₂∘ι₃ pairs | S₄ blocks |
|---|---|---|
| Pair 1 | {Kun, Zhen} | {Kun, Zhen} ✓ |
| Pair 2 | {Gen, Dui} | {Gen, Dui} ✓ |
| Pair 3 | {Kan, Xun} | {Kan, Li} ✗ |
| Pair 4 | {Li, Qian} | {Xun, Qian} ✗ |

They share 2 of 4 pairs but differ on the other 2.

The within-block swap involution β = (0↔4, 1↔6, 2↔5, 3↔7) is **not in G** at all. It commutes with all elements of G (it centralizes S₄) but lives outside the group. This is because S₄ acts *faithfully* on the 4 blocks (kernel = {id}), meaning every non-identity element moves at least one block — no element of G can simultaneously swap within all blocks.

τ itself IS in G (it's an FPF involution in V₄), but its pairs don't equal the blocks. The blocks are an intrinsic feature of G's action on 8 elements, defined by the finest preserved partition — not the pairs of any single group element.
