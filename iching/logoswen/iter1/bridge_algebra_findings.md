# Bridge Algebra Findings — Threads 1–4

> Investigating the algebraic structure of the 31 King Wen bridge masks (inter-pair transitions).
> Scripts: `logoswen/thread1_basis.py`, `logoswen/thread2_projection.py`, `logoswen/thread3_compound.py`, `logoswen/thread4_constraints.py`

---

## Thread 1: Bridge Mask Subspace

### Finding 1.1: Full Rank

The 31 bridge masks have **rank 6 over GF(2)** — they span the entire space Z₂⁶. Even the 23 unique masks alone achieve rank 6.

This means: **bridges can reach anywhere.** Any element of Z₂⁶ can be produced by XOR-combining bridge masks. The constraint on the King Wen sequence is not *what's reachable*, but *which specific masks are chosen* at each step.

The RREF basis is simply the 6 standard basis vectors — the bridge masks collectively cover all 6 dimensions with no blind spots.

### Finding 1.2: No Subgroup Structure

The 23 unique bridge masks are **not a subgroup** of Z₂⁶:
- They don't contain the identity (000000)
- 169 pairwise XOR products fall outside the set
- Their full closure generates all 64 elements of Z₂⁶

So the mask set is not a subgroup, coset, or linear code. It's an arbitrary-looking subset that happens to span everything — but "arbitrary" is doing work here: the selection is governed by the sequence's constraints, not by algebraic closure.

### Finding 1.3: Coset Distribution

The 23 unique masks distribute across the 8 cosets of the standard generator group ⟨O, M, I⟩ as follows:

| Coset representative | # masks | Orbit change |
|:---:|:---:|:---:|
| 000000 (kernel/id) | 2 | id |
| 001000 (Δi) | 3 | i |
| 010000 (Δm) | 3 | m |
| 011000 (Δmi) | 4 | mi |
| 100000 (Δo) | 2 | o |
| 101000 (Δoi) | 1 | oi |
| 110000 (Δom) | 4 | om |
| 111000 (Δomi) | 4 | omi |

This is **not uniform**: the omi, mi, and om cosets are overrepresented (4 each), while oi is underrepresented (1 mask). This reflects the King Wen sequence's preference for certain orbit transitions.

### Finding 1.4: Weight Distribution

Bridge masks avoid weight 5 entirely and show a symmetric peak at weight 3:

| Weight | Bridge masks | Total in Z₂⁶ | Coverage |
|:---:|:---:|:---:|:---:|
| 0 | 0 | 1 | 0% |
| 1 | 2 | 6 | 33% |
| 2 | 5 | 15 | 33% |
| 3 | 10 | 20 | 50% |
| 4 | 5 | 15 | 33% |
| 5 | 0 | 6 | 0% |
| 6 | 1 | 1 | 100% |

The distribution is roughly binomial but truncated: **no weight-5 masks appear** (and only the single weight-6 mask OMI=111111 exists at the top). Weight 3 has the highest coverage at 50%.

The absence of weight-5 masks means bridges never flip exactly 5 of 6 lines. This is equivalent to saying there's never a bridge that preserves exactly 1 line — the minimal change pattern is either 1 line changed (2 cases) or ≥2 lines preserved.

---

## Thread 2: The Projection Theorem

### Finding 2.1: Mask Determines Orbit Change (It's a Theorem)

The projection from 6-bit mask to 3-bit orbit change is:

```
P(m₁,m₂,m₃,m₄,m₅,m₆) = (m₁⊕m₆, m₂⊕m₅, m₃⊕m₄)
```

This holds **universally** — verified for all 4032 possible hex→hex transitions, not just the 31 bridges. It's not empirical; it follows from the definition:

```
sig(h) = (h₁⊕h₆, h₂⊕h₅, h₃⊕h₄)
sig(h⊕m) component k = (hᵢ⊕mᵢ)⊕(hⱼ⊕mⱼ) = (hᵢ⊕hⱼ)⊕(mᵢ⊕mⱼ)
∴ Δsig[k] = mᵢ ⊕ mⱼ
```

The hexagram cancels. **The orbit change depends only on the mask's asymmetry across mirror pairs.**

### Finding 2.2: P = [O; M; I]

The projection matrix is:

```
     m₁ m₂ m₃ m₄ m₅ m₆
Δo: [ 1  0  0  0  0  1 ]  = O
Δm: [ 0  1  0  0  1  0 ]  = M
Δi: [ 0  0  1  1  0  0 ]  = I
```

**The rows of the projection are the three generators.** The projection P is literally the map that tests "how much does this mask break each mirror symmetry?"

### Finding 2.3: ker(P) = ⟨O, M, I⟩

The kernel of P — masks that produce zero orbit change — consists of all masks with m₁=m₆, m₂=m₅, m₃=m₄. These are exactly the **symmetric (palindromic) masks**, which are exactly the standard generator group:

```
ker(P) = {000000, 001100, 010010, 011110, 100001, 101101, 110011, 111111}
       = ⟨O, M, I⟩ = Z₂³
```

**This gives the generators a precise algebraic meaning: they are the symmetry-preserving transformations.** A mask is generator-expressible if and only if it does not change the orbit. The generators are not just "the pair masks" — they are the kernel of the orbit projection. This is why standard pairs (which always use generator masks) always stay within an orbit.

### Finding 2.4: Unique Decomposition

Every mask decomposes uniquely as:

```
m = r ⊕ k
```

where:
- **r** = orbit change component: `(m₁⊕m₆, m₂⊕m₅, m₃⊕m₄, 0, 0, 0)` — lives in the "first 3 bits"
- **k** = within-orbit component: `(m₆, m₅, m₄, m₄, m₅, m₆)` — a standard generator mask

This means **every bridge does two things simultaneously**:
1. Changes the orbit (via the antisymmetric part of the mask)
2. Applies a standard generator transformation within-orbit (via the symmetric part)

The "free choice" at each bridge is which generator to compose with the required orbit change.

### Finding 2.5: Generator Component Distribution

The within-orbit (kernel) component across the 31 bridges:

| Generator | Count |
|:---:|:---:|
| O | 6 |
| OM | 4 |
| OMI | 4 |
| id | 4 |
| OI | 4 |
| MI | 4 |
| M | 3 |
| I | 2 |

Nearly uniform (expected: 31/8 ≈ 3.9 each). **O is slightly favored** (6 uses) and **I is slightly disfavored** (2 uses), but the distribution is close to equiprobable. The sequence doesn't strongly prefer any particular generator composition.

---

## Synthesis: The Short Exact Sequence

The complete algebraic picture is a **short exact sequence**:

```
0 → ⟨O,M,I⟩ → Z₂⁶ →P Z₂³ → 0
     ker(P)    masks    orbits
```

- **Z₂⁶** is the full mask space (64 elements)
- **⟨O, M, I⟩ ≅ Z₂³** is the kernel — the 8 symmetric/generator masks that preserve orbits
- **Z₂³** is the orbit change space — the 8 possible orbit transitions
- **P** is the projection that extracts the antisymmetric part

This sequence **splits**: every mask decomposes as (orbit change) ⊕ (generator). The two components are independent. So:

```
Z₂⁶ ≅ Z₂³ (orbit change) × Z₂³ (within-orbit generator)
```

**The 6-dimensional hypercube is the direct product of the orbit space and the generator space.** This is the fundamental algebraic structure:

- The 3 generators O, M, I span the "symmetric" subspace (kernel of P)
- The 3 "anti-generators" (asymmetric single-pair flips) span the orbit-change quotient
- Every hexagram transformation factors cleanly into these two independent 3-bit components
- Standard pairs use only the kernel (orbit-preserving). Bridges use both components simultaneously.

### What This Means for the Sequence

The King Wen sequence's bridge choices are constrained by:
1. **Which orbit to visit next** — determines the antisymmetric component (3 bits of freedom, but constrained by the orbit walk)
2. **Which generator to compose** — determines the symmetric component (3 bits of freedom, apparently near-uniformly distributed)

The "mystery" of bridge masks is now reduced to: **why does the sequence choose the particular generator composition it does at each step?** The orbit walk is one question; the generator dressing is another. Threads 3-4 investigate this.

---

## Thread 3: Compound Transitions (Pair + Bridge + Pair)

> Scripts: `logoswen/thread3_compound.py`

### Finding 3.1: The Compound Formula

The 4-hexagram window `h₁ →[pair_k]→ h₂ →[bridge_k]→ h₃ →[pair_{k+1}]→ h₄` produces a compound mask `h₁ ⊕ h₄` that decomposes cleanly:

```
compound = orbit_Δ₆ ⊕ (P_k ⊕ G ⊕ P')₆
```

where:
- `orbit_Δ₆ = (Δo, Δm, Δi, 0, 0, 0)` — the bridge's orbit change, embedded in first 3 bits
- `P_k` = pair type of starting orbit (orbit-determined)
- `G` = bridge's kernel/generator dressing (the "free choice")
- `P'` = pair type of ending orbit (orbit-determined)
- `(P_k ⊕ G ⊕ P')₆` = the 6-bit palindromic expansion of the 3-bit XOR

**Verified for all 31 windows.** The compound's orbit change equals the bridge's orbit change — pair steps cancel in the projection.

### Finding 3.2: Compound Does NOT Recover Generator Structure

The compound masks are no more structured than raw bridge masks:
- 24 unique compound masks (vs. 23 unique bridge masks)
- Only 2/31 are generator-expressible (same as bridges)
- Rank 6 over GF(2) (same as bridges)
- Mean Hamming 3.19 (between bridges at 2.94 and pairs at 3.75)

Composing pair transformations with bridges does NOT simplify the algebra. The non-generator structure of bridges persists through composition.

### Finding 3.3: Generator Chain Algebra

The generator component of the compound, `P_k ⊕ G ⊕ P'`, operates entirely in Z₂³. Since pair types are orbit-determined, the compound's generator part is fully determined by `(orbit_start, orbit_Δ, bridge_kernel)`.

**4 of 31 windows achieve total generator cancellation** (compound gen = id):
- W2, W11, W17, W25

In these cases, the compound is a *pure orbit change* — bits only in positions 1–3, zeros in 4–6. The bridge's generator dressing exactly compensates for the pair type mismatch between orbits.

### Finding 3.4: Consecutive Window Coupling

Consecutive windows W_k and W_{k+1} share the middle pair type P_{k+1}, which cancels in their XOR:

```
gen(W_k) ⊕ gen(W_{k+1}) = P_k ⊕ G_k ⊕ G_{k+1} ⊕ P_{k+2}
```

The consecutive XOR distribution is: OMI (6×), I (6×), OI (4×), MI (4×), OM (3×), O (3×), M (3×), id (1×). Only one consecutive pair has identical generator compounds (id XOR). The gen compounds are not repetitive — they move through the full generator space.

### Finding 3.5: Special Patterns in the Generator Chain

Several structural patterns appear:
- **Bridge kernel = pair_k type** (start cancels): 6 windows — the bridge "continues" the starting orbit's generator
- **Bridge kernel = pair_{k+1} type** (end cancels): 2 windows — the bridge "anticipates" the target orbit's generator  
- **Bridge kernel = id** (pure orbit change): 4 windows — the bridge adds no generator dressing
- **All cancel** (compound gen = id): 4 windows — the three generators form a closed loop in Z₂³

---

## Thread 4: Why These Generator Dressings?

> Scripts: `logoswen/thread4_constraints.py`

### Finding 4.1: The +2 Quantization Is Universal

Excess Hamming (actual - minimum) distribution across all 31 bridges:

| Excess | Count |
|:---:|:---:|
| 0 | 15 |
| +2 | 15 |
| +6 | 1 |

**Every non-optimal bridge overshoots by exactly +2**, except B19 at +6. The difference between actual and optimal masks is always a kernel element (verified for all 16 non-optimal bridges). This follows from the decomposition: the orbit_Δ component is fixed; only the generator dressing can vary. Generator masks have even weight (2, 4, or 6), so excess is always even.

**The +2 quantization is not a coincidence — it's a theorem.** Switching generator dressings changes Hamming distance by an even amount (the weight of the kernel element difference). The smallest non-zero kernel weights are 2 (O, M, I), so +2 is the minimum possible excess.

### Finding 4.2: kernel=id Is Sufficient (Not Necessary) for Optimality

All 4 bridges with `kernel=id` are Hamming-optimal. But 11 additional bridges are also optimal with non-id kernels. The `id` kernel means the bridge is a "pure orbit change" — no generator dressing — and this always minimizes the Hamming distance because the mask is just `(Δo, Δm, Δi, 0, 0, 0)`, which has the minimum weight for its orbit change.

But non-id kernels can also be optimal when the orbit change and kernel weights interact constructively (XOR can reduce total weight).

### Finding 4.3: Non-Optimal Bridges Never Use kernel=id

The non-optimal bridges use: O (4×), OI (4×), OM (3×), OMI (2×), MI (2×), I (1×). **No `id` kernel appears among non-optimal bridges.** This confirms: non-optimality = the generator dressing adds unnecessary bit flips.

### Finding 4.4: B19 Is Maximum-Excess by Design

B19 (Kui→Jian) is a self-transition (orbit mi→mi) using OMI (full complement):
- **Minimum possible Hamming: 0** (Kui could stay as Kui, identity mask)
- **Actual Hamming: 6** (every bit flips)
- **Excess: +6** (maximum possible for a self-transition)

The target Jian is the *complement* of Kui — the maximally distant hexagram in the orbit. All 8 hexagrams in the orbit are available, but B19 deliberately chooses the farthest. This is the only bridge that uses OMI, and the only bridge with excess > 2.

This is structurally meaningful: B19 marks the mid-lower-canon boundary (hex 38→39), one of only two self-transitions. It's a "reset" — same orbit, maximum internal change.

### Finding 4.5: Generator Dressing Shifts from Upper to Lower Canon

| Generator | Upper canon (B1–B14) | Lower canon (B15–B31) |
|:---:|:---:|:---:|
| id | 3 | 1 |
| OMI | 3 | 1 |
| O | 2 | 4 |
| OI | 1 | 3 |
| OM | 1 | 3 |
| MI | 1 | 3 |
| M | 2 | 1 |
| I | 1 | 1 |

The upper canon favors `id` and `OMI` (the extremes: no dressing or full dressing). The lower canon favors `O`, `OI`, `OM`, `MI` (the intermediate generators). The sequence starts with simpler generator choices and progressively uses more varied ones.

### Finding 4.6: The Weight-5 Gap Is Contingent, Not Structural

Weight-5 masks require orbit_Δ with exactly 1 bit set (single-axis orbit change: o, m, or i) combined with specific heavy generators (OM, OI, MI, or OMI). These combinations exist algebraically but happen not to occur in the King Wen sequence.

The 6 weight-5 masks are:
```
011111 = Δo ⊕ OMI     101111 = Δm ⊕ OMI     110111 = Δi ⊕ OMI
111110 = Δo ⊕ MI      111101 = Δm ⊕ OI      111011 = Δi ⊕ OM
```

All require single-axis orbit changes dressed with heavy generators. The sequence uses single-axis changes (o: 2×, m: 3×, i: 4×) and heavy generators (OMI: 4×, OM: 4×, OI: 4×, MI: 4×), but **never in the specific combinations that would produce weight 5**. This is a selection effect, not a structural impossibility.

### Finding 4.7: Degrees of Freedom Narrow Through the Sequence

At each bridge, the target orbit has 8 hexagrams, but some are already used. Available valid targets (requiring both target AND its pair partner unused) decrease steadily:

- Bridges B1–B5: 8 valid targets each (all fresh orbits)
- Bridges B6–B9: 6 valid targets each
- Bridges B10–B19: 4 valid targets each
- Bridges B20–B31: 2 valid targets each

**By the final 12 bridges, every choice is binary.** The sequence's "freedom" is front-loaded. The first 5 bridges have full choice (any of 4 pair slots in each orbit); the last 12 bridges are forced to choose between the 2 remaining pair slots in each orbit.

This means: the generator dressing "choices" in the second half are not really choices — they're forced by the Hamiltonian constraint (every hexagram visited exactly once). The upper canon is where the creative decisions happen.

### Finding 4.8: Trigram Decomposition of Bridges

The upper and lower trigrams of a bridge mask reveal its structure directly:
- **Upper trigram change = generator dressing** (positions 4–6 are purely the kernel component)
- **Lower trigram change = orbit_Δ ⊕ generator** (positions 1–3 mix both components)

This means: **you can read the generator dressing directly from the upper trigram change at any bridge.** If the upper trigram is preserved, the bridge kernel is `id` (pure orbit change). If it changes, the change pattern IS the generator.

Trigram preservation rates:
- Upper trigram preserved: 4/31 (all are kernel=id bridges)
- Lower trigram preserved: 5/31 (orbit_Δ exactly cancels kernel in lower half)
- Both preserved: 0/31 (impossible except identity transition)
- Neither preserved: 22/31 (the common case)

---

## Cross-Thread Synthesis: The Architecture of Bridge Choice

The complete picture from Threads 1–4:

### The Algebraic Framework

```
Z₂⁶ ≅ Z₂³ (orbit change) × Z₂³ (generator dressing)
```

Every bridge mask has two independent components:
1. **Orbit change** (antisymmetric part) — determined by the orbit walk
2. **Generator dressing** (symmetric/kernel part) — the "free choice"

### The Constraints on Free Choice

The generator dressing is constrained by three forces:

1. **Hamiltonian constraint**: Every hexagram must be visited exactly once. This progressively eliminates options — from 4 valid pair slots early to 1 forced pair slot late. The second half of the sequence has almost no generator freedom.

2. **Chain constraint**: Each bridge's generator dressing determines the starting hexagram of the next pair, which propagates forward. Choices are not independent — they form a chain through the sequence.

3. **Hamming optimization**: 15/31 bridges use the Hamming-optimal generator dressing. The other 15 overshoot by exactly +2 (one mirror-pair flip), with B19 as the single +6 outlier. The sequence doesn't minimize Hamming distance globally, but deviations are always the smallest possible non-zero amount.

### The Compound View

The 4-hexagram compound (pair + bridge + pair) has the same orbit change as the bridge alone, but its generator component is `P_k ⊕ G ⊕ P'` — the bridge kernel modulated by the pair types of source and target orbits. This compound does NOT recover algebraic structure; it's as "free" as the bridge itself. The pair envelope doesn't tame the bridge's non-generator character.

### What Remains

The deepest remaining question: **what selects the specific generator dressing when there IS freedom?** In the first 5 bridges (8 valid targets each), the sequence makes specific choices that aren't forced by Hamiltonian or optimality constraints. These early choices determine much of the subsequent structure through the chain constraint. Are they arbitrary, or is there a further selection principle?
