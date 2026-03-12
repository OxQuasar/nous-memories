# King Wen Sequence: The Ordering — RESOLVED

## What's solved

**The pairing rule** is a theorem. Adjacent pairs (1-2, 3-4, ..., 63-64) follow: reversal first, complement fallback for palindromes. This is the unique V₄-compatible pairing maximizing basin preservation (28/32 same-basin, second-best 26/32). Source: unification phase 1, deep iteration 8.

**The 上經/下經 split** maps to the palindromic/non-palindromic partition of pure-trigram hexagrams. 上經 (1-30) opens with Qian/Kun (both palindromic), 下經 (31-64) opens with Xian/Heng (neither palindromic). This is the Q-axis distinction — PG(2,F₂) sees this split.

**The endpoints.** Qian/Kun first (the pure poles, identity and complement). 既濟/未濟 last (the 互 2-cycle attractors, the Q-line singletons, Water/Fire interlocked — the convergence point of the algebraic structure).

**The linear order of the 32 pairs** is **characterized but not determined.** See findings below.

## The ordering question — answered

### Verdict: DESIGNED (not forced, not random, not algebraically special)

The pair ordering is the unique point of genuine human authorship in the I Ching's structure. Everything else — the 五行 assignment, the pairing rule, the trigram arrangements, the uniqueness at (3,5) — is algebraically forced. The ordering is designed but not determined: it exhibits real aesthetic properties that characterize its style without constraining it to uniqueness.

### Hard constraints (verified computationally)

Two constraints define the valid ordering space:

1. **Fixed endpoints.** Pair 0 = Qian/Kun, pair 31 = Ji Ji/Wei Ji.
2. **Z₅×Z₅ anti-clustering.** No consecutive hexagrams share the same (lower element, upper element) pair. Acceptance rate: 27.37% of random pair orderings satisfy this.

These leave ~7.2×10³¹ valid orderings. The constraint space is enormous.

### Soft properties (describe KW's character without determining it)

Three borderline metrics distinguish KW's style within the valid ordering space:

1. **Directional orbit flow** (98.3rd %ile). Orbit-signature transitions are almost entirely one-directional — 91% of connected orbit pairs appear in only one direction.
2. **Small Z₅ torus steps** (9.5th %ile). Consecutive hexagrams have closer element pairs on the Z₅×Z₅ torus than typical.
3. **Complement proximity** (10.4th %ile). Complement-paired pairs are placed closer together than typical.

Joint analysis: 7/50,000 orderings match KW on all three simultaneously. But the omnibus test (Σz² at 65th percentile) confirms no joint anomaly after look-elsewhere correction (Bonferroni-corrected p ≈ 3.1%).

### Correction: basin clustering is a confound

The prior signal (p<0.001, from 05_king_wen_sequence.py) was measured against fully random permutations. Under the correct null model (anti-clustering + fixed endpoints), **KW is below average on basin clustering** (18th percentile, z = -0.94). The anti-clustering constraint induces basin clustering because Z₅×Z₅ cell sizes correlate with basin via shared inner bits (b₂, b₃). Basin clustering was a shadow of the element constraint, not an independent signal.

### What the ordering IS

The 序卦傳 provides narrative justifications for each transition. These narratives are internally coherent and the 上經/下經 split is explicitly marked with a cosmogenic reset. The ordering encodes information in semantic/pedagogical/cosmological dimensions that are real but not algebraic. Our metric space (12 structural metrics, 50K Monte Carlo comparison) cannot detect this information — which is itself evidence that the information is non-structural.

## Hypothesis verdicts

### A: Combinatorial design — REFUTED
No optimization target discriminates KW from constrained-random orderings, individually or jointly. The omnibus statistic (Σz² = 12.95, 65th percentile) is conclusive.

### B: Narrative structure — ALIVE (non-algebraic)
The 序卦傳 narrative exists and is internally coherent. The 上經/下經 cosmogenic reset marks a genuine structural division. But the narrative operates in dimensions our metrics cannot capture. Not algebraically testable.

### C: Mawangdui comparison — COMPUTED (both normal)
Mawangdui (reconstructed) falls within the constrained-random distribution on all metrics, as does KW. Both are "typical" valid orderings. MWD is purely algebraic (lexicographic by trigram); KW is narrative. Neither is anomalous structurally.

### D: Oral/mnemonic — MOOT
The ordering is not anomalous on any structural dimension that mnemonic properties would optimize. Not tested directly, but the null structural result makes this unlikely to yield signal.

### E: Unknown algebraic principle — REFUTED
12 metrics spanning basin structure, Hamming distance, orbit dynamics, complement geometry, torus flow, yang distribution, and split properties were tested. None discriminate. The omnibus test handles any missed dimension within these categories.

## Source materials

- `kw-final/01_ordering_montecarlo.py` — Monte Carlo comparison (50K orderings, 12 metrics)
- `kw-final/01_ordering_results.md` — Full results with tables
- `kw-final/01_null_distributions.npz` — Saved null metric distributions
- `kw-final/02_joint_analysis.py` — Omnibus + triple joint tests
- `kw-final/exploration-log.md` — Investigation log

## The meta-question — answered

The KW ordering IS the one part of the I Ching that is genuinely authored — a human design choice operating in narrative dimensions unconstrained by the mathematics. Everything else is forced. The system has exactly one free parameter, and it is the linear sequence.
