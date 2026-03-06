# Lead 3: Operational Probe — Divination Circuit Invariants

## The question

Trace the Meihua evaluation circuit (本→互→变) through all coordinate systems. What's invariant along the path? What does the structure DO when operated?

384 states (64 hexagrams × 6 moving lines), each producing three hexagrams. Every hexagram examined through: binary (Z₂⁶), trigrams, five-phase elements, Lo Shu numbers, mirror-pair kernel, yang count, weight tilt, KW pairing, polarity partition, and the three involutions.

## The three findings

### 1. The H-projection theorem

**Every 互卦 has its mirror-pair kernel in H = {id, O, MI, OMI}.**

Proof: 互(h) = (L2, L3, L4, L3, L4, L5). The mirror-pair kernel of 互(h) is:
- O-bit = L1(互) ⊕ L6(互) = L2 ⊕ L5 = M-bit of 本
- M-bit = L2(互) ⊕ L5(互) = L3 ⊕ L4 = I-bit of 本
- I-bit = L3(互) ⊕ L4(互) = L4 ⊕ L3 = I-bit of 本

kernel(互) = (M_本, I_本, I_本). Since M-bit = I-bit (both equal I_本), kernel ∈ H always. □

The 16 互 values distribute exactly evenly: 4 each of {id, O, MI, OMI}.

**Connection to the sequence investigation:** The Upper Canon's bridge kernels reside in H 64.5% of the time (96.7th percentile). The 互卦 operation produces H-kernel hexagrams 100% of the time. The sequence and the divination operation both privilege the same subgroup — the sequence does it probabilistically (sequential constraint on transitions), 互 does it deterministically (structural constraint on the operation itself).

The kernel undergoes a **downward shift**: O-bit ← M-bit ← I-bit ← I-bit. Outer information is replaced by middle, middle by inner, inner is doubled. This is the algebraic expression of the amplification gradient discovered in Phase 3: inner perturbations (L3,L4) produce 2× the nuclear change of middle perturbations (L2,L5), which produce infinitely more than outer (L1,L6, which are erased entirely).

### 2. 互卦 destroys 生 and amplifies 克

The five-phase relation distribution shifts dramatically:

| Relation class | 本/变 (full space) | 互 (nuclear) | Ratio |
|---|---|---|---|
| 比和 (harmony) | 84/384 = 21.9% | 96/384 = 25.0% | ×1.14 |
| 生 (generation: 生体+体生用) | 144/384 = 37.5% | 48/384 = 12.5% | **×0.33** |
| 克 (overcoming: 克体+体克用) | 156/384 = 40.6% | 240/384 = 62.5% | **×1.54** |

Among the 16 互 values: only 4/32 relation-slots are 生-type vs 20/32 克-type (compared to 12/32 vs 13/32 in the full space). The nuclear hexagram is biased toward overcoming/conflict.

The transition matrix has structural zeros:
- 克 → 生: impossible (克体 and 体克用 never become 生体 or 体生用 in 互)
- 生 direction reversal: impossible (生体 never becomes 体生用, or vice versa)
- 生 → 克 absorption: 50% of 生体 states become 体克用 in 互; 50% of 体生用 become 克体

**Interpretation:** The nuclear hexagram (互) represents the *hidden dynamic* — what's happening beneath the surface. The algebraic bias toward 克 means the hidden layer disproportionately reveals tension, conflict, and overcoming. This is consistent with the traditional interpretive role of 互卦 as showing "the underlying situation" — structurally, the underlying situation is more adversarial than the surface.

### 3. 体 is absolutely preserved in 变, partially in 互

| Property | 本→变 | 本→互 |
|---|---|---|
| 体 trigram identical | **384/384 (100%)** | 48/384 (12.5%) |
| 体 element identical | **384/384 (100%)** | 96/384 (25.0%) |
| 体 polarity preserved | **384/384 (100%)** | 240/384 (62.5%) |

The 100% preservation in 变 is trivial by construction: the moving line is always in 用 (by definition), so 体 is untouched.

The 12.5% trigram preservation in 互 means the nuclear hexagram almost always changes the 体 trigram — the "self" is recontextualized. The 62.5% polarity preservation is uniform across positions and initial polarities (37.5% flip rate everywhere), confirming the polarity flip depends on both trigrams jointly.

## Secondary findings

### Lo Shu arithmetic

- 体+用 Lo Shu sum has mean 10.00 at all three stages (forced by uniform trigram sampling)
- The sum is NOT preserved point-wise: only 54/384 states maintain the same sum from 本 to 互
- Lo Shu |体−用| increases slightly in 互 (mean 3.62 vs 3.12) — nuclear hexagrams push 体 and 用 further apart in number space, consistent with the 克 amplification

### Yang count and weight tilt

- Mean Δyang (本→互) = 0.000 (zero bias), but 互 does NOT contract yang count toward the center: 40.6% expand, only 18.8% contract, 40.6% unchanged
- Weight tilt preserved 本→互 for 144/384 states (37.5%)

### KW pairing through 互

- 互(h) and 互(partner(h)) are KW partners for 56/64 hexagrams (87.5%)
- 互(h) = 互(partner(h)) for the remaining 8/64 (12.5%) — these are the 4 complement pairs whose 互 values are identical
- **0/64 cases** where the KW pairing relationship is broken — it's either preserved (87.5%) or collapsed (12.5%)

### Algebraic identities

- **MI commutes with 互 via complement**: 互(h ⊕ MI) = complement(互(h))
- **OMI commutes with 互 via complement**: 互(complement(h)) = complement(互(h))
- **Idempotence**: 互(互(h)) = 互(h) for all h (the 16-element image is a retract)
- **Convergence**: 64 → 16 → 4 fixed points: {000000, 010101, 101010, 111111} = {Kun, Wei Ji, Ji Ji, Qian}

### Involution preservation

When 本's 体/用 pair forms an involution pair (ι₁, ι₂, or ι₃), how often does 互 preserve it?
- ι₁ (Fu Xi complement): 25.0% preserved
- ι₂ (Lo Shu diametric): 37.5% preserved  
- ι₃ (He Tu): 12.5% preserved

Lo Shu (ι₂) is best preserved — consistent with the theme that 互 privileges the KW/Lo Shu structure over Fu Xi or He Tu.

## The structural picture

The Meihua circuit operates on three temporal layers:

| Stage | What it shows | Structural role |
|---|---|---|
| 本卦 | Present situation | Full 6-bit state, uniform five-phase distribution |
| 互卦 | Hidden dynamic | Projected into H-subgroup, 克-biased, inner-amplified |
| 变卦 | Future development | Single-bit perturbation, 体 preserved absolutely |

The 互卦 is the structurally richest stage. It:
1. **Projects into H** (the M-I locked subgroup that the Upper Canon sequence also privileges)
2. **Amplifies conflict** (克 relations ×1.54, 生 relations ×0.33)
3. **Shifts the kernel downward** (O ← M ← I ← I: outer info replaced by middle, middle by inner)
4. **Preserves KW pairing** (87.5% partner-paired, 12.5% collapsed to identity, 0% broken)

The 本→互 transition is a *lossy projection that privileges the inner core and biases toward adversarial dynamics*. The 本→变 transition is a *minimal perturbation that preserves the self absolutely*. Together: the reading sees the present (本), reveals what's actually happening underneath (互, more conflictual than it appears), and shows where it's going (变, a small change that doesn't alter who you are).

## The thread: S₄ → Z₂³ → H → divination → sequence

### H characterized via 互

H is not an arbitrary subgroup. It is determined by the nuclear hexagram operation:

**H = ker(互) × ⟨complement on 互-space⟩ = {id, O} × {id, MI}**

- **ker(互) = {id, O}:** the operations invisible to 互 (flipping the outer pair doesn't change the nuclear hexagram at all)
- **MI:** the operation that uniformly complements 互 (every nuclear hexagram maps to its complement, distance 6)

The four H elements have constant 互-distance: {id, O} → distance 0, {MI, OMI} → distance 6. The non-H elements produce intermediate distances: {M, OM} → 2, {I, OI} → 4. **H is the subgroup whose effect on 互 is extremal — either invisible or maximal.**

All 8 elements of Z₂³ are fiber-compatible (they preserve the partition into 互 fibers). But only H acts *simply* on 互-space (as identity or complement). The non-H elements permute the 16 互 values non-trivially.

### The complete thread

1. **S₄** structures the trigram space into 4 blocks of 2 (two axioms → unique)
2. **Doubling** (trigram → hexagram) creates Z₂³ via three mirror pairs (O, M, I)
3. **互卦** projects hexagrams by erasing the outer pair: 64 → 16, fibers of size 4
4. **H** = the subgroup of Z₂³ that acts simply (trivially or by complement) on 互-space
5. **The Upper Canon sequence** walks through Z₂³ preferring H (64.5%, 96.7th percentile)
6. **Interpretation:** the sequence is arranged so that consecutive transitions either don't affect the nuclear hexagram, or complement it entirely — never scramble it

The sequence doesn't just randomly prefer some algebraic subgroup. It preferentially uses the transitions that are *compatible with divination* — the ones that don't break the structure the nuclear hexagram operation depends on.

### H in three contexts

| Context | How H appears | Nature |
|---|---|---|
| 互卦 output | kernel(互) always in H | Algebraic necessity |
| 互卦 action | H = elements acting simply on 互-space | Structural characterization |
| Upper Canon sequence | Bridge kernels in H 64.5% of time | Statistical preference (96.7th %ile) |
| Abstract Z₂³ | Uniquely distinguished order-4 subgroup | Algebraic uniqueness |

## Path invariants

*(From `path_invariants.py` — analyzing the triple (本,互,变) as a trajectory.)*

### True invariants (all 384 states)

1. **d(本, 变) = 1** — single bit flip, by construction
2. **体 trigram preserved 本→变** — moving line in 用 by definition
3. **kernel(互) ∈ H** — algebraic (proven above)
4. **yang(变) = yang(本) ± 1** — single bit flip
5. **互(本) = 互(变) iff line ∈ {1,6}** — outer pair invisible to 互
6. **d(互(本), 互(变)) is exactly {0,1,2} for lines {outer, middle, inner}** — the amplification gradient is constant for every hexagram, not just a mean

### The 本→互 kernel constraint

The XOR kernel of 本→互 is restricted to **{id, O, M, OM}** — exactly the four kernels where I-bit = 0. The inner pair (L3↔L4) is never flipped by the 本→互 transition. Combined with the H-projection (互 output always has M=I in its kernel), the system has a striking algebraic structure:

| Transition | Kernel constraint | Subgroup |
|---|---|---|
| 本→互 (XOR) | I-bit = 0 | {id, O, M, OM} |
| 互 (output) | M-bit = I-bit | H = {id, O, MI, OMI} |
| Upper Canon bridges | M-bit = I-bit preferentially | H (96.7th %ile) |

### Distance triangle

- d(互,变) = d(本,互) ± 1, with exact 50/50 split. 变 is never equidistant — it always breaks the symmetry.
- d(本,互) is independent of moving line position (mean=3.00 for every line). The nuclear hexagram's distance from the original depends on the hexagram content, not on which line moves.

### Trajectory constraints

91 of 125 possible five-phase trajectories (本,互,变) are realized. 34 are structurally forbidden. The forbidden set includes all trajectories where 克 in 本 would need to become 生 in 互 (20 trajectories), plus 生 direction reversals (生体↛体生用).

### Yang count path formula

yang(互) = yang(本) + L3 + L4 − L1 − L6. The nuclear hexagram's yang count depends only on the difference between inner and outer pairs — the very decomposition that defines the mirror-pair structure.

## Data

Scripts: `divination_trace.py` (384-state trace), `deeper_analysis.py` (follow-up), `path_invariants.py` (path characterization).
Dependencies: `opposition-theory/phase4/cycle_algebra.py`, `kingwen/sequence.py`.
