# 12. Orbit Analysis of the King Wen Sequence

> The 3 generators O (flip L1,L6), M (flip L2,L5), I (flip L3,L4) generate the group Z₂³ acting on {0,1}^6. Since no generator has fixed points, every orbit has exactly 8 elements — partitioning 64 hexagrams into 8 orbits, each a 3-cube (Q₃) embedded in the hypercube.

(This is the way to go, over quartets (10) amd octets (11))

---

## Finding 1: The XOR Signature Is a Complete Invariant

Every hexagram has three mirror-position line pairs: (L1,L6), (L2,L5), (L3,L4). The XOR of each pair — whether the two lines agree (0) or disagree (1) — is invariant under all generators, since each generator flips both lines of a pair simultaneously.

This 3-bit code `(L1⊕L6, L2⊕L5, L3⊕L4)` uniquely identifies the orbit. All 2³ = 8 possible signatures appear exactly once:

| Orbit | Signature | Pair Type | Weight Distribution | Representative |
|:---:|:---:|:---:|:---:|---|
| 1 | (0,0,0) | OMI | 0,2,2,2,4,4,4,6 | Qian, Kun, Yi, Da Guo, Kan, Li, Zhong Fu, Xiao Guo |
| 2 | (1,1,0) | OM | 2,2,2,2,4,4,4,4 | Zhun, Meng, Lin, Guan, Dun, Da Zhuang, Ge, Ding |
| 3 | (1,0,1) | OI | 2,2,2,2,4,4,4,4 | Xu, Song, Jin, Ming Yi, Zhen, Gen, Xun, Dui |
| 4 | (0,1,0) | M | 1,1,3,3,3,3,5,5 | Shi, Bi, Tong Ren, Da You, Xian, Heng, Sun, Yi |
| 5 | (0,0,1) | I | 1,1,3,3,3,3,5,5 | Xiao Chu, Lu, Qian, Yu, Shi He, Bi, Kun, Jing |
| 6 | (1,1,1) | OMI | 3,3,3,3,3,3,3,3 | Tai, Pi, Sui, Gu, Jian, Gui Mei, Ji Ji, Wei Ji |
| 7 | (1,0,0) | O | 1,1,3,3,3,3,5,5 | Bo, Fu, Guai, Gou, Feng, Lu, Huan, Jie |
| 8 | (0,1,1) | MI | 2,2,2,2,4,4,4,4 | Wu Wang, Da Chu, Jia Ren, Kui, Jian, Xie, Cui, Sheng |

The signature says: for each of the three mirror-position pairs, are the two lines in the same state (symmetric, 0) or opposite state (antisymmetric, 1)?

---

## Finding 2: Every Orbit Is a Perfectly Balanced Doubled Q₃

All 8 orbits share the same center [0.50, 0.50, 0.50, 0.50, 0.50, 0.50] and weight sum 24. This is forced by the group action: each generator flips a pair of bits, so for every vertex the orbit also contains its "opposite" under each generator.

The pairwise Hamming distance distribution within every orbit is {2: 12, 4: 12, 6: 4} — the standard cube graph Q₃ with edges doubled (since each generator flips 2 bits, not 1). Every orbit is geometrically isomorphic.

---

## Finding 3: The Pair Type Is an Orbit-Level Property

Within each orbit, all 4 King Wen pairs use the **same** generator type. The pair mask does not vary within an orbit — it is determined by the orbit's XOR signature.

This is not forced by group theory. The group action makes all 7 non-identity elements available as perfect matchings within each orbit. King Wen *chose* to use a single mask type per orbit, creating a strict correspondence:

- Signature → Orbit → Pair type (unique)
- Pair type → Orbit (unique, except OMI → two orbits)

The 7 mask types map to 8 orbits because OMI is used by both extremes: orbit 1 (signature 000, all symmetric) and orbit 6 (signature 111, all antisymmetric).

---

## Finding 4: Weight Classes Follow Signature Structure

The XOR signature determines the weight distribution:

- **All-zero signature** (0,0,0): weights span the full range 0–6 (includes Qian=6 and Kun=0)
- **All-one signature** (1,1,1): all weights are exactly 3 (perfectly balanced hexagrams)
- **Single-bit signatures** (0,1,0), (0,0,1), (1,0,0): weights are {1,1,3,3,3,3,5,5} — odd only
- **Double-bit signatures** (1,1,0), (1,0,1), (0,1,1): weights are {2,2,2,2,4,4,4,4} — even only

The number of 1s in the signature determines the weight parity: even count → even weights; odd count → odd weights. And signature (1,1,1) forces weight 3 for all members — the only orbit with uniform weight.

---

## Finding 5: Every Orbit Contains All 8 Trigrams

In both upper and lower positions, every orbit contains all 8 trigrams exactly once. This is forced by the group action: the 3 generators can independently flip each trigram bit-pair, generating all 8 combinations from any starting trigram.

This means the orbit decomposition is invisible to trigram-level analysis — every orbit looks the same when projected to trigrams.

---

## Finding 6: Bridges Rarely Stay Within an Orbit

Only 2 of 31 bridges connect pairs in the same orbit. The sequence overwhelmingly crosses orbit boundaries at each bridge transition, visiting different symmetry classes in rapid succession.

The orbit traversal sequence (by pair) is:

```
1→2→3→4→5→6→4→5→6→2→5→7→8→1→1→4→2→3→8→8→4→7→8→5→2→3→6→7→3→7→1→6
```

The first 6 pairs visit orbits 1–6 in order. After that, the sequence revisits orbits in a complex pattern with only 2 self-transitions (pairs 13→14 staying in orbit 1, and pairs 19→20 staying in orbit 8).

---

## Finding 7: Orbit Scatter in the Sequence

Orbits vary dramatically in how spread out their hexagrams are across the 64-position sequence:

| Orbit | Positions | Span | Std | Canon Split |
|:---:|---|:---:|:---:|:---:|
| 1 (Qian) | 1,2,27,28,29,30,61,62 | 61 | 21.3 | 6/2 |
| 2 (Zhun) | 3,4,19,20,33,34,49,50 | 47 | 17.0 | 4/4 |
| 3 (Xu) | 5,6,35,36,51,52,57,58 | 53 | 20.2 | 2/6 |
| 4 (Shi) | 7,8,13,14,31,32,41,42 | 35 | 13.6 | 6/2 |
| 5 (Xiao Chu) | 9,10,15,16,21,22,47,48 | 39 | 14.5 | 6/2 |
| 6 (Tai) | 11,12,17,18,53,54,63,64 | 53 | 22.4 | 4/4 |
| 7 (Bo) | 23,24,43,44,55,56,59,60 | 37 | 14.0 | 2/6 |
| 8 (Wu Wang) | 25,26,37,38,39,40,45,46 | 21 | 7.3 | 2/6 |

Orbit 8 (MI, signature 011) is the most tightly clustered — all 8 hexagrams fall within positions 25–46, entirely in the middle of the sequence. Orbits 1 and 6 (the two OMI orbits) are the most dispersed, bookending the sequence.

The canon split shows a clear pattern: orbits 4 and 5 (M and I, the single-generator types for middle and inner lines) concentrate in the upper canon, while orbits 3, 7, and 8 concentrate in the lower canon.

---

## Summary

The orbit decomposition reveals the deepest structural layer of the King Wen sequence:

1. **Complete invariant** — the 3-bit XOR signature (L1⊕L6, L2⊕L5, L3⊕L4) perfectly classifies hexagrams into 8 orbits
2. **Perfect geometric uniformity** — all orbits are isomorphic, same center, same distance distribution
3. **Pair type is orbit-determined** — King Wen chose a single mask type per orbit, making the pair structure an orbit-level property
4. **Weight classes from signature** — the signature's Hamming weight determines the weight parity and distribution of the orbit
5. **Trigram invisibility** — orbits are invisible to trigram decomposition (each orbit contains all 8 trigrams)
6. **Near-total orbit crossing** — bridges almost always change orbits (29/31 transitions)
7. **Asymmetric scatter** — orbits range from tightly clustered (orbit 8, span 21) to fully dispersed (orbit 1, span 61)

The orbit is the natural "atom" of King Wen structure: a set of 8 hexagrams sharing the same mirror-symmetry type, connected by a single pair mask, and forming a perfect cube in the hypercube. The sequence threads through these 8 cubes, visiting each exactly 4 times (as pairs), crossing orbit boundaries at nearly every bridge.
