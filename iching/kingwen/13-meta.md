# 13. Meta-Hexagram Analysis of the King Wen Sequence

> Each pair has a 3-bit orbit signature (L1⊕L6, L2⊕L5, L3⊕L4). Stack two adjacent pair signatures → a 6-bit meta-hexagram. The sequence quotiented through its own symmetry structure.

---

## Construction

Each King Wen pair lives in one of 8 orbits, identified by a 3-bit XOR signature. Stacking the signatures of adjacent pairs produces a 6-bit meta-hexagram — itself a point in {0,1}^6.

- **Non-overlapping**: 32 pairs → 16 meta-hexagrams (quartets)
- **Sliding window**: 32 pairs → 31 meta-hexagrams (all bridges)

---

## Finding 1: The Meta-Hexagrams Map to King Wen Hexagrams

All 31 sliding-window meta-hexagrams correspond to actual hexagrams (guaranteed since {0,1}^6 = the 64 hexagrams). The specific hexagrams that appear:

```
P1→P2:  #45 Cui         P17→P18: #38 Kui
P2→P3:  #38 Kui         P18→P19: #37 Jia Ren
P3→P4:  #63 Ji Ji       P19→P20: #57 Xun
P4→P5:  #4  Meng        P20→P21: #48 Jing
P5→P6:  #33 Dun         P21→P22: #40 Xie
P6→P7:  #5  Xu          P22→P23: #42 Yi
P7→P8:  #4  Meng        P23→P24: #18 Gu
P8→P9:  #33 Dun         P24→P25: #31 Xian
P9→P10: #43 Guai        P25→P26: #38 Kui
P10→P11:#41 Sun         P26→P27: #13 Tong Ren
P11→P12:#62 Xiao Guo    P27→P28: #34 Da Zhuang
P12→P13:#42 Yi          P28→P29: #21 Shi He
P13→P14:#46 Sheng       P29→P30: #55 Feng
P14→P15:#2  Kun         P30→P31: #24 Fu
P15→P16:#8  Bi          P31→P32: #12 Pi
P16→P17:#47 Kun
```

26 of 31 are unique. #38 Kui (Opposition) appears 3 times — the most frequent meta-hexagram. The non-overlapping set has 15/16 unique (Q9 and Q13 both produce Kui, both from OM→OI transitions).

---

## Finding 2: Meta-Signature Has an Exact Formula

Each meta-hexagram is itself a 6-bit string with its own XOR signature. This meta-signature follows an exact algebraic rule:

**meta_sig(k) = sig(pair_k) ⊕ reverse(sig(pair_{k+1}))**

Verified for all 16 non-overlapping meta-hexagrams.

### Why the Reversal

The meta-hexagram stacks two 3-bit signatures into 6 bits: `(s1[0], s1[1], s1[2], s2[0], s2[1], s2[2])`. The XOR signature of any hexagram pairs mirror positions: bit 1 with bit 6, bit 2 with bit 5, bit 3 with bit 4. Applied to the meta-hexagram, the mirror pairing crosses the boundary between the two stacked signatures:

```
meta_sig[0] = s1[0] ⊕ s2[2]    (bit 1 ⊕ bit 6)
meta_sig[1] = s1[1] ⊕ s2[1]    (bit 2 ⊕ bit 5)
meta_sig[2] = s1[2] ⊕ s2[0]    (bit 3 ⊕ bit 4)
```

The reversal isn't arbitrary — it's forced by the hexagram's mirror geometry. The mirror structure that defines orbits at the hexagram level imposes a reflection when applied at the meta-level.

### In Generator Terms: O and I Swap

Each position in the 3-bit signature corresponds to a generator:
- Position 0 = O (outer, L1⊕L6)
- Position 1 = M (middle, L2⊕L5)
- Position 2 = I (inner, L3⊕L4)

The reversal swaps positions 0↔2, which is O↔I. M stays fixed. The meta-signature measures:

```
Bit 0:  O_lower ⊕ I_upper     (outer of one regime vs inner of the next)
Bit 1:  M_lower ⊕ M_upper     (middle vs middle — direct comparison)
Bit 2:  I_lower ⊕ O_upper     (inner of one regime vs outer of the next)
```

This is not "are the two orbits the same?" — that would be plain XOR without reversal. It's "how do the two regimes compare when one is reflected?" A chirality-sensitive cross-correlation. The transition between two regimes is measured not by how their surfaces compare, but by how the outer layer of one relates to the inner layer of the next.

### What Specific Meta-Signatures Mean

- **(0,0,0)**: The two signatures are exact reverses of each other. O_lower = I_upper, M_lower = M_upper, I_lower = O_upper. The transition swaps outer and inner while preserving middle — a structural inversion. The next regime is the mirror of the current one, seen from the inside out.

- **(1,1,1)**: Maximum cross-disagreement on every axis. Nothing from one regime maps to the other, even with reflection. The transition is maximally disorienting.

- **(0,1,0)**: Outer↔inner align across the transition, but middle breaks. The surface and core are consistent across the regime change; the mediating layer shifts.

### Self-Reference with a Twist

The hexagram's structural invariant (XOR signature) classifies hexagrams into orbits. The same invariant applied to meta-hexagrams produces a quantity algebraically determined by the original orbit signatures — but with O and I exchanged. The self-referential structure isn't a simple copy; it reproduces with a reflection. The algebra recurs at the meta-level, but outer and inner generators swap roles.

The structural analogue: when you observe the pattern of regime transitions, the pattern itself has regime structure — but with surface and depth inverted.

### Cross-Generator Decomposition (Computed)

The 16 non-overlapping meta-hexagrams decomposed into their cross-generator bits:

```
 Q   lower  upper   O⊕I  M⊕M  I⊕O   meta_sig  interpretation
 1     000    110     0    1    1    (0,1,1)   O=I across; M shifts; I≠O across
 2     101    010     1    1    1    (1,1,1)   max cross-disagreement
 3     001    111     1    1    0    (1,1,0)   O≠I across; M shifts; I=O across
 4     010    001     1    1    0    (1,1,0)   O≠I across; M shifts; I=O across
 5     111    110     1    0    0    (1,0,0)   O≠I across; M stable; I=O across
 6     001    100     0    0    0    (0,0,0)   structural mirror (lower = reverse of upper)
 7     011    000     0    1    1    (0,1,1)   O=I across; M shifts; I≠O across
 8     000    010     0    1    0    (0,1,0)   O=I across; M shifts; I=O across
 9     110    101     0    1    1    (0,1,1)   O=I across; M shifts; I≠O across
10     011    011     1    0    1    (1,0,1)   O≠I across; M stable; I≠O across
11     010    100     0    1    1    (0,1,1)   O=I across; M shifts; I≠O across
12     011    001     1    1    1    (1,1,1)   max cross-disagreement
13     110    101     0    1    1    (0,1,1)   O=I across; M shifts; I≠O across
14     111    100     1    1    0    (1,1,0)   O≠I across; M shifts; I=O across
15     101    100     1    0    0    (1,0,0)   O≠I across; M stable; I=O across
16     000    111     1    1    1    (1,1,1)   max cross-disagreement
```

**M is the most unstable cross-axis.** M_lower ≠ M_upper in 12/16 non-overlapping (75%) and 21/31 sliding (68%) transitions. Since M compares directly (no reversal — middle maps to middle), this is a straight measure: consecutive regimes usually disagree on middle-pair harmony/tension. The mediating layer is the most volatile structural axis across transitions.

**O↔I cross-frequency is symmetric but individual transitions are not.** O_lower≠I_upper and I_lower≠O_upper both occur in exactly 9/16 (56.2%) of non-overlapping transitions — perfectly balanced in aggregate. But only 6/16 transitions are symmetric within the same meta-hexagram (bit 0 = bit 2). The outer-inner cross-relationship has balanced statistics but asymmetric instances.

**One structural mirror (Q6).** The I→O transition (pairs 11-12: Xiao Chu/Lu → Bo/Fu). Lower signature (0,0,1) is the exact reverse of upper (1,0,0). The outer and inner generators swap roles perfectly while middle holds constant. Meta-sig (0,0,0) — the transition is a pure reflection, the most structurally coherent regime change in the sequence.

**Three maximum cross-disagreements (Q2, Q12, Q16).** All meta-sig (1,1,1). Q16 is the final quartet: signature (0,0,0) → (1,1,1), from the all-symmetric orbit to the all-antisymmetric orbit. The sequence ends with maximum structural disorientation — every cross-generator axis disagrees. The closing transition is as far from a mirror as possible.

---

## Finding 3: Signature Transitions Form Their Own Generator Sequence

The 31 bridge transitions in orbit-signature space use the same Z₂³ alphabet:

```
om→mi→omi→mi→om→oi→mi→om→i→omi→oi→omi→mi→id→m→o→mi→om→id→i→om→omi→m→omi→mi→m→mi→i→i→o→omi
```

Transition frequency:

| Change | Count | Description |
|:---:|:---:|---|
| mi | 7 | middle + inner orbit shift |
| omi | 6 | full orbit shift |
| om | 5 | outer + middle orbit shift |
| i | 4 | inner-only orbit shift |
| m | 3 | middle-only orbit shift |
| o | 2 | outer-only orbit shift |
| oi | 2 | outer + inner orbit shift |
| id | 2 | same orbit (self-transition) |

The sequence's orbit dynamics reproduce the same algebraic vocabulary as the pair-level generators. The group Z₂³ acts simultaneously at two scales: on hexagrams (pair masks) and on orbits (signature transitions).

---

## Finding 4: Two Self-Transitions Mark Structural Boundaries

Only 2 of 31 bridges are identity transitions (staying in the same orbit):

- **P14→P15** (pairs 14-15): OMI→OMI — both in orbit 1 (signature 000). This is the boundary between hexagrams 28-29 (Da Guo→Kan), the traditional break between the upper and lower canons.
- **P19→P20** (pairs 19-20): MI→MI — both in orbit 8 (signature 011). Hexagrams 38-39 (Kui→Jian), within the lower canon.

The canon boundary is the only place where the sequence stays in the all-symmetric orbit (000) across a bridge.

---

## Finding 5: Meta-Hexagram Weight Is Exactly 3.00

The 16 non-overlapping meta-hexagrams have mean weight exactly 3.00, ranging from 1 to 5. The meta-sequence is perfectly balanced despite the original sequence's yang-drainage tendency.

---

## Finding 6: Meta-Orbit Concentration in Orbit 8

The 16 meta-hexagrams' own orbit distribution is uneven:

| Orbit | Count | Signature |
|:---:|:---:|:---:|
| 8 (MI) | 5 | (0,1,1) |
| 2 (OM) | 3 | (1,1,0) |
| 6 (OMI) | 3 | (1,1,1) |
| 7 (O) | 2 | (1,0,0) |
| 1 (OMI) | 1 | (0,0,0) |
| 3 (OI) | 1 | (1,0,1) |
| 4 (M) | 1 | (0,1,0) |

Orbit 8 (MI, the middle-inner signature) captures 5 of 16 meta-hexagrams. The meta-level has a strong bias toward the MI symmetry class — the same generator pair that dominates the signature transition frequency.

---

## Summary

The meta-hexagram construction reveals self-similarity in the King Wen sequence:

1. **Stacked signatures produce hexagrams** — the orbit-level quotient maps back into the original space
2. **Exact algebraic formula** — meta-signatures follow `sig ⊕ reverse(sig')`, a cross-correlation between adjacent orbit types
3. **Same group at two scales** — Z₂³ acts on both hexagrams (pair masks) and orbits (signature transitions), with `mi` dominating at the meta-level
4. **Canon boundary is an orbit fixed point** — the only all-symmetric self-transition occurs at the traditional upper/lower canon split
5. **Perfect weight balance** — the meta-level achieves mean weight 3.00 despite the original sequence's yang drift
6. **MI concentration** — the meta-level preferentially inhabits the middle-inner symmetry class

The sequence's structure is not just hierarchical but self-referential: the orbit-level dynamics reproduce the same algebraic vocabulary that governs the hexagram-level pairing.
