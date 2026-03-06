# Phase 3: Nuclear Trigrams and the L3|L4 Membrane

## Summary

The nuclear trigram decomposition carries no independent opposition information. Every nuclear-level property is derivable from the hexagram-level mirror-pair signature by erasing the outer component. The nuclear level is a projection, not a new structural layer.

Phase 3's positive contribution is a **depth-function separation**: the outer pair (L1, L6) buffers weight, the inner pair (L3, L4) anchors opposition structure, and the middle pair (L2, L5) bridges between them. This decomposition of Phase 2's weight-preservation invariant into spatially localized mechanisms is the main finding.

---

## 1. Trigram-Level Opposition Under KW Pairing

### The two decompositions

A hexagram's 6 lines admit two natural decompositions:

- **Trigram decomposition**: lower (L1-L2-L3) and upper (L4-L5-L6)
- **Mirror-pair decomposition**: outer (L1, L6), middle (L2, L5), inner (L3, L4)

These cross-cut each other. The overlap matrix:

| Mirror pair | Lower trigram | Upper trigram |
|-------------|---------------|---------------|
| O (outer)   | L1            | L6            |
| M (middle)  | L2            | L5            |
| I (inner)   | L3            | L4            |

Every mirror pair is split across the trigram boundary — one member in each trigram. The inner pair {L3, L4} is uniquely significant: it straddles the trigram boundary AND appears in both nuclear trigrams.

### How reversal acts on trigrams

For the 28 non-palindromic KW pairs (b = rev₆(a)), hexagram-level reversal decomposes as:
1. **Swap** the upper and lower trigrams
2. **Reverse** each trigram internally (rev₃)

So upper(b) = rev₃(lower(a)) and lower(b) = rev₃(upper(a)). Verified for all 28 pairs.

This means the cross-relationships (lower(a) ↔ upper(b), upper(a) ↔ lower(b)) are always either **identity** (when the trigram is a palindrome under rev₃) or **reversal** (when it's not). The distribution across 28 reversal pairs: 14 identity, 14 reversal in each cross-direction.

The direct relationships (lower(a) ↔ lower(b), upper(a) ↔ upper(b)) are generically "other" — 20 of 28 cases fall outside the {identity, complement, reversal, comp∘rev} vocabulary. This is expected: comparing lower(a) with lower(b) = rev₃(upper(a)) mixes the swap and reverse operations in a way that doesn't reduce to a single named operation on 3-bit strings.

For the 4 palindromic pairs (b = comp(a)), both direct trigram relationships are complement, as expected.

---

## 2. Nuclear Trigram Opposition Measures and Findings

### Nuclear trigram extraction

- **Lower nuclear**: (L2, L3, L4) — bits 1,2,3
- **Upper nuclear**: (L3, L4, L5) — bits 2,3,4

The two nuclear trigrams share L3 and L4 (the inner pair). This overlap is the defining structural feature.

### Nuclear XOR mask vocabulary

The hexagram-level 7 signature masks produce nuclear XOR masks by windowing:

| Hex signature | Hex mask | Lower nuc XOR | Upper nuc XOR |
|---------------|----------|---------------|---------------|
| (0,0,1)       | 001100   | 110           | 011           |
| (0,1,0)       | 010010   | 001           | 100           |
| (0,1,1)       | 011110   | 111           | 111           |
| (1,0,0)       | 100001   | 000           | 000           |
| (1,0,1)       | 101101   | 110           | 011           |
| (1,1,0)       | 110011   | 001           | 100           |
| (1,1,1)       | 111111   | 111           | 111           |

Key observations:
- Lower nuclear uses masks {000, 001, 110, 111}; upper nuclear uses {000, 011, 100, 111}
- These are **bit-reversals** of each other — a coordinate artifact of the windowing, not independent structure
- Only masks 000 and 111 appear in both vocabularies
- Signature (1,0,0) maps to the zero mask — opposition is erased entirely at the nuclear level

The nuclear XOR vocabulary is fully determined by the hexagram-level signature. No new information enters.

### Nuclear trigram relationship classification

Among all 32 pairs, the nuclear trigram relationship distribution:

| Nuclear relationship | Count (lower nuc) | Count (upper nuc) |
|---------------------|-------------------|-------------------|
| complement          | 12                | 12                |
| identity            | 4                 | 4                 |
| reversal            | 0                 | 0                 |
| other               | 16                | 16                |

The 4 identity cases correspond to signature (1,0,0) — where all nuclear opposition is erased. The 12 complement cases include all 4 palindromic pairs plus 8 reversal pairs where the nuclear XOR happens to equal 111.

---

## 3. Weight Preservation Decomposition

### Hexagram → trigram → nuclear

Phase 2 established that KW preserves hexagram-level weight perfectly for reversal pairs (Δw = 0). This does NOT propagate uniformly to sub-levels:

| Level | Mean |Δw| (all 32 pairs) | Mean |Δw| (28 reversal) | Weight correlation r |
|-------|-------------------------|------------------------|---------------------|
| **Full hexagram** | **0.375** | **0.000** | **+0.516** |
| Lower nuclear | 0.750 | 0.571 | +0.277 |
| Upper nuclear | 0.750 | 0.571 | +0.277 |
| Lower trigram | 1.125 | 1.071 | −0.077 |
| Upper trigram | 1.125 | 1.071 | +0.125 |

### The degradation hierarchy

Weight preservation degrades monotonically as we move from the full hexagram toward sub-structures:
- **Full hexagram**: perfect for reversal (Δw = 0), small for palindromic pairs (mean Δw = 0.375)
- **Nuclear trigrams**: 2× worse than full hexagram, but 2× better than standard trigrams
- **Standard trigrams**: 3× worse than full hexagram

The mechanism: reversal (swap + internal reverse) redistributes weight between upper and lower components. The full hexagram sees zero net change because the redistribution cancels globally. Nuclear trigrams see partial cancellation because they share the inner pair {L3, L4} — this shared anchor dampens the redistribution. Standard trigrams have no overlap and see the full disruption.

### Where weight preservation physically resides

The weight correlation hierarchy (full: +0.52, nuclear: +0.28, trigram: ~0) shows that weight preservation is NOT uniformly distributed across the hexagram. It is concentrated at the full-hexagram level and partially preserved at the nuclear level, with the outer pair acting as the key buffer.

Removing the outer pair (via 互卦 projection) increases mean |Δw| from 0.375 to 0.500. The outer lines absorb weight disruption that complement imposes on palindromic pairs.

---

## 4. The L3|L4 Membrane: Independent Information Content

### The question

Phase 2 identified {L1↔L6, L2↔L5, L3↔L4} as the mirror-pair partition underlying KW's symmetry. The trigram boundary falls between L3 and L4 — the inner pair. The nuclear trigrams (L2-L3-L4 and L3-L4-L5) straddle this boundary. Does this boundary carry opposition information that neither decomposition captures alone?

### The answer: No

Every nuclear-level opposition property reduces to the hexagram-level signature with the O-component erased. The L3|L4 boundary is geometrically special (the unique split mirror pair appearing in both nuclear trigrams) but informationally derivative. The nuclear trigrams function as bit-windows into the hexagram-level mask, not as independent structural entities.

### What the boundary DOES reveal

The boundary's significance is not informational but **functional**: it reveals *where* in the hexagram different aspects of the KW invariant are carried.

| Depth layer | Lines | Function |
|-------------|-------|----------|
| **Outer** (O) | L1, L6 | Weight buffer. Erased by 互卦. Contributes to opposition strength but not nuclear structure. |
| **Middle** (M) | L2, L5 | Bridge. Each belongs to exactly one nuclear trigram. Preserved by 互卦. |
| **Inner** (I) | L3, L4 | Opposition core. Both belong to BOTH nuclear trigrams. Doubled by 互卦. Structural anchor. |

This depth-function separation is a genuine structural finding — it decomposes Phase 2's weight-preservation invariant into spatially localized mechanisms.

---

## 5. Mirror-Pair vs Trigram Decomposition: Non-Alignment Analysis

### The overlap structure

The mirror-pair partition and the trigram partition are two independent geometric decompositions of 6 positions. Their non-alignment is captured by the overlap matrix (§1 above): every mirror pair has exactly one member in each trigram, so the two decompositions are maximally non-aligned — no mirror pair is contained within a single trigram.

### Nuclear trigrams as boundary-spanning elements

Nuclear trigrams are defined precisely at the site of maximal non-alignment:

| Nuclear trigram | Lines | Mirror pairs touched |
|-----------------|-------|---------------------|
| Lower nuclear | L2, L3, L4 | M (one member), I (both members) |
| Upper nuclear | L3, L4, L5 | I (both members), M (one member) |

Both nuclear trigrams contain the entire inner pair and one member of the middle pair. Neither touches the outer pair. This gives nuclear trigrams their characteristic properties:
- They **bridge** the trigram boundary (lower nuclear reaches into upper via L4; upper nuclear reaches into lower via L3)
- They are **insensitive** to outer-pair opposition
- They share a 2-position overlap (L3, L4), creating correlated nuclear behavior

### The 互卦 as a projection operator

The 互卦 map formalizes this non-alignment. It extracts the 4-bit nuclear core (L2-L5) and re-expands it:

```
hugua(L1-L2-L3-L4-L5-L6) = L2-L3-L4-L3-L4-L5
```

In mirror-pair terms: **erase O, preserve M, double I.** This is a lossy 4:1 projection (64 → 16 hexagrams), with uniform preimage sizes.

Properties:
- **Not idempotent.** hugua² converges to 4 hexagrams: {000000, 010101, 101010, 111111} — pure L3/L4 alternation patterns. Convergence in exactly 2 steps.
- **2 fixed points.** Only 000000 and 111111 (where L1=L3=L5 and L2=L4=L6).
- **Preserves 28 of 32 KW pairs** (87.5%).

### Mask vocabulary reduction under 互卦

The 7 hexagram signature masks reduce to 3 nonzero masks + identity:

| Hexagram signatures | 互卦 XOR | Mechanism |
|--------------------|----------|-----------|
| (0,0,1) and (1,0,1) | 011110 | O-bit erased, same (M,I) |
| (0,1,0) and (1,1,0) | 100001 | O-bit erased, same (M,I) |
| (0,1,1) and (1,1,1) | 111111 | O-bit erased, same (M,I) |
| (1,0,0)             | 000000 | Only O differed — opposition erased |

The reduction is exactly: project Z₂³ onto the M,I subspace Z₂², yielding 2² − 1 = 3 nonzero masks, plus the identity from the (1,0,0) pairs that lose all opposition.

---

## 6. Connection to Phase 2 Weight Preservation Principle

### Phase 2's characterization

KW is the unique weight-preserving pairing among 9 invariants of the mirror-pair partition group (order 384). Weight tilt = 0.375 vs ≥ 1.125 for all others.

### Phase 3's refinement

Phase 2 showed *that* weight is preserved. Phase 3 shows *where* the preservation physically resides:

1. **Reversal pairs (28/32)**: Weight is preserved perfectly at the hexagram level because reversal is weight-neutral (w(rev(x)) = w(x)). At sub-levels, the swap+reverse operation redistributes weight, but the full hexagram sums cancel. The inner pair's shared presence in both nuclear trigrams partially dampens this redistribution (nuclear |Δw| = 0.57 vs trigram |Δw| = 1.07).

2. **Complement pairs (4/32)**: Weight is maximally disrupted (Δw = |6 − 2w|). The outer pair absorbs some of this disruption — removing it via 互卦 makes the weight difference worse for some pairs.

3. **The depth separation is a decomposition of the invariant, not a new invariant.** Weight preservation at the hexagram level is a single scalar property. The depth separation tells us it has internal structure: the outer lines contribute differently from the inner lines. This is a refinement, not an extension.

### The two modes of opposition

The commutativity failure (§4 of the 互卦 analysis) reveals that KW's two-branch rule is not merely a "fallback" — it classifies opposition by depth:

- **Shell-only opposition** (signature (1,0,0), 4 pairs): Opposition lives entirely in the outer pair. Invisible to nuclear structure. The 互卦 collapses these pairs to identity.
- **Depth-penetrating opposition** (all other signatures, 28 pairs): Opposition reaches into the nuclear core. Preserved by 互卦 projection.

The 8 hexagrams (4 pairs) where 互卦 fails to commute with KW are exactly those where:
- The hexagram is non-palindromic (KW applies reversal)
- But the nuclear core (L2-L5) IS palindromic (L2=L5 and L3=L4)
- So 互卦 maps it to a palindromic hexagram where KW would apply complement

This is the **palindrome phase boundary** — the point where the KW rule's two-branch structure becomes visible through projection. The predicted failure set {non-palindromic x : L2=L5 and L3=L4} matches the actual failure set exactly (8 hexagrams).

---

## 7. Implications for Phase 4 (生克 and Five-Phase Mapping)

### What Phase 3 enables

Phase 3 provides three structural constraints for Phase 4:

**1. Depth-function separation constrains 体/用 analysis.** The traditional 互卦 interpretation assigns the nuclear trigram as the 体 (substance/body) of a hexagram. Phase 3 shows that for signature (1,0,0) pairs, opposition is invisible at the nuclear level — the 体 carries no opposition information. For all other pairs, opposition penetrates to the core. This creates a testable prediction: 体/用 analysis should behave differently for shell-only vs depth-penetrating opposition pairs.

**2. Weight preservation is peripherally concentrated.** Any five-phase cycle (生 or 克) that operates on trigram associations must interact with the weight-buffer function of the outer lines. The outer pair's role as weight stabilizer means that transformations affecting L1/L6 have different structural consequences than those affecting L3/L4 — even if both appear as "one line changes."

**3. The commutativity classification.** Five-phase theory assigns elements to trigrams, and 生克 cycles define directed relationships between elements. Phase 3 shows that the KW pairing commutes cleanly with trigram decomposition at the shell level but breaks at the nuclear level. If 生克 is defined on shell trigrams, it should compose cleanly with KW opposition. If defined on nuclear trigrams, the palindrome boundary creates complications for 4 of 32 pairs.

### The sage's caveat

The five-element assignment to trigrams is a **traditional mapping layer** — it is not inherent to the binary combinatorial structure. Phase 4 must distinguish between:
- The combinatorial structure of directed cycles on trigrams (binary, structural)
- The specific five-element assignment (traditional, interpretive)

These are different questions with different epistemic status. Phases 1–3 established results at the combinatorial level. Phase 4 will need to handle the mapping layer explicitly.

---

## 8. Open Questions

### Resolved by Phase 3

**Q5 (from plan): Nuclear trigram boundary.** The L3|L4 membrane does not carry independent opposition information. It is the site of maximal geometric non-alignment between mirror-pair and trigram decompositions, but the opposition structure there is fully determined by the hexagram-level signature. **Resolved.**

### Carried forward to Phase 4

1. **体/用 and depth separation.** The nuclear trigram traditionally determines the 体 (substance). Phase 3 shows opposition is invisible at 体 level for signature (1,0,0) pairs. Does this connect to traditional interpretations where these hexagrams are evaluated differently?

2. **L1/L6 as initial/final conditions.** Traditional I Ching interpretation assigns special status to L1 (beginning) and L6 (culmination). Phase 3's finding that these lines serve as weight buffers — carrying the quantitative balance while the inner lines carry qualitative transformation — may connect to this interpretive tradition. Whether the connection is structural or coincidental is a Phase 4 question.

3. **互卦 convergence structure.** The iteration 64 → 16 → 4 converges to {000000, 010101, 101010, 111111} — pure inner-pair alternation. This convergence is observed but uninterpreted. Filing for potential future relevance.

### Still open from earlier phases

4. **Cross-scale divergence (Q3).** The tradition applies opposite principles at n=3 (strength >> weight) and n=6 (weight >> strength). Phase 3 does not address this.

5. **Sequential variety (Q5/kac).** Integration of the sequence-dependent axis with the pairing characterization remains open.

---

## Files

| File | Description |
|------|-------------|
| `trigram_decomposition.py` | Trigram/nuclear extraction for all 32 KW pairs |
| `trigram_decomposition_results.md` | Full 32-pair tables + summary statistics |
| `hugua_test.py` | 互卦 self-similarity and commutativity test |
| `hugua_results.md` | 互卦 pair table + structural analysis |
| `phase3_cleanup.py` | Failure set confirmation |
| `phase3_summary.md` | Compact summary |
| `nuclear_trigram_analysis.md` | This document |
