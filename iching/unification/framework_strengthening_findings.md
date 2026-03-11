# Framework Strengthening: Findings

## 1. P-Invariance Test

| Generator set | ker(O) | ker(M) | P | ker(I) | Q | H | ker(OMI) |
|--------------|--------|--------|---|--------|---|---|----------|
| O,M,OI | 2 | 6 | 0 | 6 | 4 | 4 | 2 |
| O,M,MI | 6 | 2 | 0 | 6 | 4 | 4 | 2 |
| O,OM,I | 2 | 6 | 4 | 6 | 0 | 4 | 2 |
| O,OM,MI | 2 | 2 | 4 | 6 | 0 | 4 | 6 |
| O,I,MI | 6 | 6 | 4 | 2 | 0 | 4 | 2 |
| O,OI,MI | 2 | 6 | 0 | 2 | 4 | 4 | 6 |
| M,OM,I | 6 | 2 | 4 | 6 | 4 | 0 | 2 |
| M,OM,OI | 2 | 2 | 4 | 6 | 4 | 0 | 6 |
| M,I,OI | 6 | 6 | 4 | 2 | 4 | 0 | 2 |
| M,OI,MI | 6 | 2 | 0 | 2 | 4 | 4 | 6 |
| OM,I,OI | 2 | 6 | 4 | 2 | 4 | 0 | 6 |
| OM,I,MI | 6 | 2 | 4 | 2 | 0 | 4 | 6 |

**Variable:**
- ker(O): [2, 6]
- ker(M): [2, 6]
- P: [0, 4]
- ker(I): [2, 6]
- Q: [0, 4]
- H: [0, 4]
- ker(OMI): [2, 6]

**Theorem.** P+Q+H = 8 for all complement-antipodal Hamiltonian cycles.
No such cycle uses OMI as a step-XOR (adjacent elements cannot be
complements since complements are fixed at distance 4). Therefore each
step hits exactly 1 of {P,Q,H}, and 8 steps give P+Q+H = 8.

P is NOT individually constant (values {0,4}), but the sum P+Q+H is.

**Note:** 先天 and 後天 both have P=4, but this is the modal value
(51.4% of all Hamiltonian cycles have P=4). The shared value is not
forced by a deep constraint.

## 2. Quantitative 克 Amplification

### 互 Transition Matrix

| Original \ Nuclear | 同 | 生 | 被生 | 克 | 被克 | Total |
|---|---|---|---|---|---|---|
| **同** | 6 | 2 | 2 | 2 | 2 | 14 |
| **生** | 1 | 2 | 0 | 3 | 6 | 12 |
| **被生** | 1 | 0 | 2 | 6 | 3 | 12 |
| **克** | 4 | 0 | 0 | 4 | 5 | 13 |
| **被克** | 4 | 0 | 0 | 5 | 4 | 13 |
| **Nuclear** | 16 | 4 | 4 | 20 | 20 | 64 |

### Amplification Factors

| Relation | Original | Nuclear | Factor |
|----------|----------|---------|--------|
| 同 | 14 | 16 | 1.143× |
| 生 | 12 | 4 | 0.333× |
| 被生 | 12 | 4 | 0.333× |
| 克 | 13 | 20 | 1.538× |
| 被克 | 13 | 20 | 1.538× |

**克 amplification: 1.538×** — 克 fraction increases from 13/64 to 20/64 under 互.

### Parity Rotation Mechanism

The P→H parity rotation provides the algebraic mechanism:
- 克-exclusive masks (M, MI) flip P-parity but MI preserves H-parity
- Under 互, P-parity rotates to H-parity
- What was P-misaligned (克) becomes H-aligned in the nuclear

## 3. 先天 Uniqueness

Among the 4 directed complement-antipodal cycles with {O, I, MI} generators,
先天 is one of 2 undirected cycles.

### What distinguishes 先天

**Verified.** 先天 is the unique cycle where b₀ (bottom line) is **constant**
within each semicircle:

- 先天 b₀ pattern: (1,1,1,1,0,0,0,0) — yang half / yin half
- Other cycle b₀ pattern: (1,1,0,0,0,0,1,1) — mixed

This means the O step (which flips b₀) occurs only at the semicircle
boundary in 先天, while I and MI steps occur within semicircles.
先天 maximally separates the 'outer line flip' (O) from the
'inner line flips' (I, MI), placing O at the poles and I/MI in between.

## 4. KW Ordering Probe

### Between-pair bridge statistics

31 between-pair bridges (transitions from pair k to pair k+1) were
decomposed into position (Δpos) and orbit (Δorb) components.

### Statistical comparison (KW vs 1000 random pair orderings)

All Z-scores are within ±1.5σ for position bridges.
No Fano line shows a statistically significant preference or avoidance
in the KW ordering compared to random.

The H-line has the highest combined hit count (30 = 15 pos + 15 orb),
but this is within ~1σ of random expectation.

### Structural features

- **Cumulative position XOR** visits: OMI→I→M→O→O→I→OI
  (traces a path through PG(2,2) that doesn't stay on any single line)
- **Canon bridge** (pair 15→16): Δpos=O, Δorb=M — both single-bit masks
- **Upper Canon** has higher ker(M) pos hits; **Lower Canon** has higher
  ker(O) pos hits — a complementary pattern, but within noise range

### Conclusion

The KW ordering does NOT show statistically significant Fano-line
structure in its between-pair bridges. The ordering principle,
if algebraic, operates at a level not captured by the product
Fano decomposition of between-pair transitions.

**The KW sequence ordering remains outside the PG(2,2) framework.**
This is consistent with the synthesis claim: the framework explains
the pairing (orbit class) but not the ordering.
