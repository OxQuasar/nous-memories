# Sheaf Theory Investigation

## Background

The only sheaf-theoretic result so far is negative: the presheaf of dropped 京氏易傳 layers over the palace walk is trivial (every stalk has one element, H(fields | palace, rank) = 0.0 bits). This tested the wrong object — deterministic data over a deterministic base. Sheaf theory is interesting where local-to-global extension *fails*.

Three untested candidates where non-trivial sheaf structure might live.

---

## S1: The Surjection as a Sheaf over PG(2,F₂)

**Base space:** The Fano plane — 7 points, 7 lines.

**Stalks:** Over each point (nonzero trigram), the stalk is its Z₅ value. Over each line (3 collinear trigrams), there's a compatibility condition: the three points satisfy a + b + c = 0 in F₂³.

**The question:** Does the Z₅ assignment define a sheaf (or presheaf, or cosheaf) over PG(2,F₂) with non-trivial cohomology?

Synthesis-1 identified three "heterogeneous gluings" connecting the Fano geometry to Z₅:

| Gluing | Connects | Nature |
|--------|----------|--------|
| Z₅ monotonicity | Fano ↔ compass | Non-linear (cyclic ordering) |
| Complement symmetry | OMI ↔ element pairs | Non-linear (involves 五行 map) |
| FPF involutions | Fano ↔ block system | Non-linear (permutation-theoretic) |

These are described as "necessarily heterogeneous because the primes contribute different mathematical substances." That language — heterogeneous gluing of local data from different mathematical worlds — is exactly what sheaf cohomology measures.

**What to formalize:**
- Define the presheaf: for each open set U ⊆ PG(2,F₂) (using the order-complex or the line-cover topology), what is F(U)?
- The restriction maps: how does the Z₅ data on a line restrict to its points?
- The line condition: three points on a line sum to 0 in F₂³. Their Z₅ values satisfy f(a) + f(b) + f(c) = ? — this is NOT generally 0 mod 5. What constraint does it satisfy? Is there a cocycle condition?
- Compute H⁰ (global sections) and H¹ (obstruction to extending local to global).

**What to check first:**
For each of the 7 Fano lines, compute f(a) + f(b) + f(c) mod 5. If these sums are constant, the sheaf has a clean cocycle. If they vary, the variation IS the cohomological data.

**Data:** The surjection values are known: 001→0, 110→0, 010→4, 101→1, 011→3, 100→2, 111→3.

**References:** phase1-unification.md (heterogeneous gluing), synthesis-1.md §Three Heterogeneous Gluings.

---

## S2: 互 Dynamics as a Sheaf over Iteration Depth

**Base space:** The iteration sequence {0, 1, 2, ...} — the depth of 互 application.

**Stalks:** At depth k, the stalk is the effective space of hexagrams reachable after k applications of 互. The rank formula (R71) says dim = max(2, 6−2k), so:

| Depth | Rank | Effective dimension | Hexagrams reachable |
|-------|------|--------------------|--------------------|
| 0 | 6 | 6 | 64 |
| 1 | 4 | 4 | ≤16 (actual: specific subset) |
| 2 | 2 | 2 | 4 (attractor: 坤坤, 既濟, 未濟, 乾乾) |

**The question:** The rank drops uniformly (2 per step). But does the *direction* of the kernel carry structure? At each depth, certain hexagrams map to the same image under 互ᵏ. The equivalence classes at each depth form the stalks. The restriction map (going deeper) merges classes. Is this merging uniform, or does it have structure the rank formula doesn't capture?

**What to formalize:**
- Define the presheaf: F(k) = the partition of 64 hexagrams into equivalence classes under 互ᵏ
- Restriction maps: F(k) → F(k+1) merges classes
- The attractor partition F(2) has 4 classes (one per attractor). How do these refine at F(1) and F(0)?
- Is there a filtration with non-trivial associated graded?

**What might make this non-trivial:** The rank formula is about the *size* of the kernel. If two hexagrams share the same 互 image but have different 互² images, that's a non-trivial local section — consistent at depth 1 but distinguishable at depth 2. The rank formula says this can't happen (rank drops uniformly). But the *basin structure* (which attractor a hexagram converges to) is known to be an exact 互 invariant — it's determined at depth 0 and preserved at all depths. That's a global section. Are there other invariants that are determined at intermediate depths?

**Likely outcome:** Probably trivial — the rank formula's uniformity suggests the filtration is too regular for interesting cohomology. But worth checking whether the basin × onion-layer decomposition gives the partition at each depth exactly, or whether there's additional structure.

**References:** i-summary/work/proof_nuclear_rank.md (R71), attractors/findings.md (basin structure).

---

## S3: The Operational System as a Sheaf over Domains

**Base space:** The 31 火珠林 domains (marriage, illness, travel, weather, lost objects, etc.), with overlap structure defined by shared 用神 assignments.

**Stalks:** Over each domain d, the stalk F(d) is the operational protocol — the 用神 assignment, the judgment rules, the special exceptions.

**The question:** Do the 31 domain-specific protocols glue into a global system, or is there genuine local-to-global obstruction?

This is the most promising candidate. The atlas-hzl found:
- 31 domains cluster into 8 groups + 5 genuine exceptions
- The 5 exceptions (疾病, 天時, 射覆, 來情, 姓字) break the standard protocol
- The 5 are classified by a 2D taxonomy (layer × mode) with zero residual
- The 用神 distribution is highly asymmetric: 官鬼 covers 8 domains, 兄弟 covers 0

**What to formalize:**
- **Cover:** Define an open cover of the domain space by "protocol neighborhoods" — domains sharing the same 用神 type
- **Sections:** Over each neighborhood, the protocol is consistent (same 用神, same evaluation rules)
- **Overlaps:** Some domains share 用神 but differ in judgment rules. Some domains share judgment style but differ in 用神. The overlap data is the cocycle.
- **The 5 exceptions as cohomology:** The 5 special domains are exactly where the global protocol fails. They require local modifications that can't be absorbed into the standard framework. This is a non-trivial H¹ — 5 independent obstructions to global extension.

**What to check:**
- Can the 5 exceptions be expressed as a Čech 1-cocycle on an open cover of the domain space?
- Is the 2D taxonomy (layer × mode) the classification of H¹? (It has zero residual — every exception is classified. That's what a cohomology computation would give.)
- Does the 8-cluster structure correspond to H⁰ (the global sections — the part of the protocol that works everywhere)?

**What makes this different from S1/S2:** The base space is *semantic* (domains of human concern), not algebraic. The stalks are *operational* (protocols), not numerical. The obstruction is *practical* (certain domains need special rules), not abstract. If sheaf theory applies here, it would be formalizing the structure of the judgment boundary (reversal/questions.md Q3) — the place where algorithm meets practitioner.

**Data:** atlas-hzl/hzl_domains.json (31 domain bindings), atlas-hzl/hzl_yongshen_protocol.json (用神 protocol), atlas-hzl/findings.md §Domain Analysis.

---

## Relations Between the Three

| Candidate | Base space | Stalks | Expected outcome |
|-----------|-----------|--------|-----------------|
| S1 | PG(2,F₂) (7 points) | Z₅ values | Unknown — depends on line sums |
| S2 | Iteration depth {0,1,2} | Hexagram partitions | Probably trivial (uniform rank drop) |
| S3 | 31 domains | Operational protocols | Most likely non-trivial (5 exceptions = obstructions) |

S1 would formalize the core algebra in sheaf language. S2 would formalize the dynamics. S3 would formalize the operational boundary. They live at different levels of the system.

S3 is the most likely to produce a genuine result — it has actual failure of global extension. S1 is the most mathematically interesting — it might connect the "heterogeneous gluing" to standard cohomological machinery. S2 is the least promising but the quickest to check.

## Priority

S3 first (most likely non-trivial), S1 second (most mathematically interesting), S2 last (probably trivial).

## Quick preliminary computation

Before formalizing anything, compute the 7 Fano line sums for S1:

```
Line {001, 010, 011}: f = 0 + 4 + 3 = 7 ≡ 2 mod 5
Line {001, 100, 101}: f = 0 + 2 + 1 = 3 ≡ 3 mod 5
Line {010, 100, 110}: f = 4 + 2 + 0 = 6 ≡ 1 mod 5
Line {011, 101, 110}: f = 3 + 1 + 0 = 4 ≡ 4 mod 5
Line {001, 110, 111}: f = 0 + 0 + 3 = 3 ≡ 3 mod 5
Line {010, 101, 111}: f = 4 + 1 + 3 = 8 ≡ 3 mod 5
Line {011, 100, 111}: f = 3 + 2 + 3 = 8 ≡ 3 mod 5
```

The three lines through 111 all sum to 3. The four lines not through 111 take values {1, 2, 3, 4}. This is already structure — the complement point creates a constant-sum condition on its lines while the remaining lines vary. This is not a trivial cocycle. Worth pursuing.
