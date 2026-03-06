# Round 1: The Trigram Substrate — Complete Map

## Overview

This round introduces the trigram decomposition of the King Wen sequence — a *different* decomposition of the same 6 bits from the mirror-pair split used in iters 1–5. The trigram split divides Z₂⁶ as lower trigram (L1-L3) × upper trigram (L4-L6). The mirror-pair split divides it as orbit × position via (L1↔L6, L2↔L5, L3↔L4). These two cuts see different structure in the same object.

**Bit ordering convention (verified):** Binary strings in `kingwen/sequence.py` are bottom-to-top (L1 first). Hex #29 Kan = "010010" → lower = "010" (Water ☵), upper = "010" (Water ☵) ✓. Hex #30 Li = "101101" → lower = "101" (Fire ☲), upper = "101" (Fire ☲) ✓. Hex #5 Xu = "111010" → lower = "111" (Heaven ☰), upper = "010" (Water ☵) ✓. Hex #11 Tai = "111000" → lower = "111" (Heaven ☰), upper = "000" (Earth ☷) ✓.

---

## Task 1: Full Trigram Decomposition Table

All 64 hexagrams decomposed into primary and nuclear trigrams.

| # | Name | Binary | Lower | Upper | Nuc. Lower | Nuc. Upper | Orbit | Gen |
|---|------|--------|-------|-------|-----------|-----------|-------|-----|
| 1 | Qian | 111111 | Heaven ☰ | Heaven ☰ | Heaven ☰ | Heaven ☰ | (000) | id |
| 2 | Kun | 000000 | Earth ☷ | Earth ☷ | Earth ☷ | Earth ☷ | (000) | id |
| 3 | Zhun | 100010 | Thunder ☳ | Water ☵ | Earth ☷ | Mountain ☶ | (110) | OM |
| 4 | Meng | 010001 | Water ☵ | Mountain ☶ | Thunder ☳ | Earth ☷ | (110) | OM |
| 5 | Xu | 111010 | Heaven ☰ | Water ☵ | Lake ☱ | Fire ☲ | (101) | OI |
| 6 | Song | 010111 | Water ☵ | Heaven ☰ | Fire ☲ | Wind ☴ | (101) | OI |
| 7 | Shi | 010000 | Water ☵ | Earth ☷ | Thunder ☳ | Earth ☷ | (010) | M |
| 8 | Bi | 000010 | Earth ☷ | Water ☵ | Earth ☷ | Mountain ☶ | (010) | M |
| 9 | Xiao Chu | 111011 | Heaven ☰ | Wind ☴ | Lake ☱ | Fire ☲ | (001) | I |
| 10 | Lü | 110111 | Lake ☱ | Heaven ☰ | Fire ☲ | Wind ☴ | (001) | I |
| 11 | Tai | 111000 | Heaven ☰ | Earth ☷ | Lake ☱ | Thunder ☳ | (111) | OMI |
| 12 | Pi | 000111 | Earth ☷ | Heaven ☰ | Mountain ☶ | Wind ☴ | (111) | OMI |
| 13 | Tong Ren | 101111 | Fire ☲ | Heaven ☰ | Wind ☴ | Heaven ☰ | (010) | M |
| 14 | Da You | 111101 | Heaven ☰ | Fire ☲ | Heaven ☰ | Lake ☱ | (010) | M |
| 15 | Qian (Mod) | 001000 | Mountain ☶ | Earth ☷ | Water ☵ | Thunder ☳ | (001) | I |
| 16 | Yu | 000100 | Earth ☷ | Thunder ☳ | Mountain ☶ | Water ☵ | (001) | I |
| 17 | Sui | 100110 | Thunder ☳ | Lake ☱ | Mountain ☶ | Wind ☴ | (111) | OMI |
| 18 | Gu | 011001 | Wind ☴ | Mountain ☶ | Lake ☱ | Thunder ☳ | (111) | OMI |
| 19 | Lin | 110000 | Lake ☱ | Earth ☷ | Thunder ☳ | Earth ☷ | (110) | OM |
| 20 | Guan | 000011 | Earth ☷ | Wind ☴ | Earth ☷ | Mountain ☶ | (110) | OM |
| 21 | Shi He | 100101 | Thunder ☳ | Fire ☲ | Mountain ☶ | Water ☵ | (001) | I |
| 22 | Bi (Grace) | 101001 | Fire ☲ | Mountain ☶ | Water ☵ | Thunder ☳ | (001) | I |
| 23 | Bo | 000001 | Earth ☷ | Mountain ☶ | Earth ☷ | Earth ☷ | (100) | O |
| 24 | Fu | 100000 | Thunder ☳ | Earth ☷ | Earth ☷ | Earth ☷ | (100) | O |
| 25 | Wu Wang | 100111 | Thunder ☳ | Heaven ☰ | Mountain ☶ | Wind ☴ | (011) | MI |
| 26 | Da Chu | 111001 | Heaven ☰ | Mountain ☶ | Lake ☱ | Thunder ☳ | (011) | MI |
| 27 | Yi (Nour.) | 100001 | Thunder ☳ | Mountain ☶ | Earth ☷ | Earth ☷ | (000) | id |
| 28 | Da Guo | 011110 | Wind ☴ | Lake ☱ | Heaven ☰ | Heaven ☰ | (000) | id |
| 29 | Kan | 010010 | Water ☵ | Water ☵ | Thunder ☳ | Mountain ☶ | (000) | id |
| 30 | Li | 101101 | Fire ☲ | Fire ☲ | Wind ☴ | Lake ☱ | (000) | id |
| 31 | Xian | 001110 | Mountain ☶ | Lake ☱ | Wind ☴ | Heaven ☰ | (010) | M |
| 32 | Heng | 011100 | Wind ☴ | Thunder ☳ | Heaven ☰ | Lake ☱ | (010) | M |
| 33 | Dun | 001111 | Mountain ☶ | Heaven ☰ | Wind ☴ | Heaven ☰ | (110) | OM |
| 34 | Da Zhuang | 111100 | Heaven ☰ | Thunder ☳ | Heaven ☰ | Lake ☱ | (110) | OM |
| 35 | Jin | 000101 | Earth ☷ | Fire ☲ | Mountain ☶ | Water ☵ | (101) | OI |
| 36 | Ming Yi | 101000 | Fire ☲ | Earth ☷ | Water ☵ | Thunder ☳ | (101) | OI |
| 37 | Jia Ren | 101011 | Fire ☲ | Wind ☴ | Water ☵ | Fire ☲ | (011) | MI |
| 38 | Kui | 110101 | Lake ☱ | Fire ☲ | Fire ☲ | Water ☵ | (011) | MI |
| 39 | Jian (Obst.) | 001010 | Mountain ☶ | Water ☵ | Water ☵ | Fire ☲ | (011) | MI |
| 40 | Xie | 010100 | Water ☵ | Thunder ☳ | Fire ☲ | Water ☵ | (011) | MI |
| 41 | Sun | 110001 | Lake ☱ | Mountain ☶ | Thunder ☳ | Earth ☷ | (010) | M |
| 42 | Yi (Incr.) | 100011 | Thunder ☳ | Wind ☴ | Earth ☷ | Mountain ☶ | (010) | M |
| 43 | Guai | 111110 | Heaven ☰ | Lake ☱ | Heaven ☰ | Heaven ☰ | (100) | O |
| 44 | Gou | 011111 | Wind ☴ | Heaven ☰ | Heaven ☰ | Heaven ☰ | (100) | O |
| 45 | Cui | 000110 | Earth ☷ | Lake ☱ | Mountain ☶ | Wind ☴ | (011) | MI |
| 46 | Sheng | 011000 | Wind ☴ | Earth ☷ | Lake ☱ | Thunder ☳ | (011) | MI |
| 47 | Kun (Oppr.) | 010110 | Water ☵ | Lake ☱ | Fire ☲ | Wind ☴ | (001) | I |
| 48 | Jing | 011010 | Wind ☴ | Water ☵ | Lake ☱ | Fire ☲ | (001) | I |
| 49 | Ge | 101110 | Fire ☲ | Lake ☱ | Wind ☴ | Heaven ☰ | (110) | OM |
| 50 | Ding | 011101 | Wind ☴ | Fire ☲ | Heaven ☰ | Lake ☱ | (110) | OM |
| 51 | Zhen | 100100 | Thunder ☳ | Thunder ☳ | Mountain ☶ | Water ☵ | (101) | OI |
| 52 | Gen | 001001 | Mountain ☶ | Mountain ☶ | Water ☵ | Thunder ☳ | (101) | OI |
| 53 | Jian (Dev.) | 001011 | Mountain ☶ | Wind ☴ | Water ☵ | Fire ☲ | (111) | OMI |
| 54 | Gui Mei | 110100 | Lake ☱ | Thunder ☳ | Fire ☲ | Water ☵ | (111) | OMI |
| 55 | Feng | 101100 | Fire ☲ | Thunder ☳ | Wind ☴ | Lake ☱ | (100) | O |
| 56 | Lü (Wand.) | 001101 | Mountain ☶ | Fire ☲ | Wind ☴ | Lake ☱ | (100) | O |
| 57 | Xun | 011011 | Wind ☴ | Wind ☴ | Lake ☱ | Fire ☲ | (101) | OI |
| 58 | Dui | 110110 | Lake ☱ | Lake ☱ | Fire ☲ | Wind ☴ | (101) | OI |
| 59 | Huan | 010011 | Water ☵ | Wind ☴ | Thunder ☳ | Mountain ☶ | (100) | O |
| 60 | Jie | 110010 | Lake ☱ | Water ☵ | Thunder ☳ | Mountain ☶ | (100) | O |
| 61 | Zhong Fu | 110011 | Lake ☱ | Wind ☴ | Thunder ☳ | Mountain ☶ | (000) | id |
| 62 | Xiao Guo | 001100 | Mountain ☶ | Thunder ☳ | Wind ☴ | Lake ☱ | (000) | id |
| 63 | Ji Ji | 101010 | Fire ☲ | Water ☵ | Water ☵ | Fire ☲ | (111) | OMI |
| 64 | Wei Ji | 010101 | Water ☵ | Fire ☲ | Fire ☲ | Water ☵ | (111) | OMI |

---

## Task 2: The 8×8 Trigram-Pair Grid

The 64 hexagrams fill an 8×8 grid exactly (lower trigram × upper trigram). Each cell is one hexagram.

### KW Numbers on the Grid

Rows = lower trigram, columns = upper trigram. Trigrams ordered: Heaven, Lake, Fire, Thunder, Wind, Water, Mountain, Earth.

```
             Heaven  Lake   Fire  Thunder  Wind  Water  Mtn   Earth
            ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  Heaven    │   1  │  43  │  14  │  34  │   9  │   5  │  26  │  11  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Lake      │  10  │  58  │  38  │  54  │  61  │  60  │  41  │  19  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Fire      │  13  │  49  │  30  │  55  │  37  │  63  │  22  │  36  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Thunder   │  25  │  17  │  21  │  51  │  42  │   3  │  27  │  24  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Wind      │  44  │  28  │  50  │  32  │  57  │  48  │  18  │  46  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Water     │   6  │  47  │  64  │  40  │  59  │  29  │   4  │   7  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Mountain  │  33  │  31  │  56  │  62  │  53  │  39  │  52  │  15  │
            ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
  Earth     │  12  │  45  │  35  │  16  │  20  │   8  │  23  │   2  │
            └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
```

### Hexagram Names on the Grid

```
             Heaven     Lake      Fire    Thunder    Wind     Water    Mtn      Earth
            ┌──────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
  Heaven    │  Qian    │  Guai   │  Da You │  DaZhng │  XiaoChu│  Xu     │  Da Chu │  Tai    │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Lake      │  Lü     │  Dui    │  Kui    │  GuiMei │  ZhngFu │  Jie    │  Sun    │  Lin    │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Fire      │  TongRen│  Ge     │  Li     │  Feng   │  JiaRen │  Ji Ji  │  Bi(Gr) │  MingYi │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Thunder   │  WuWang │  Sui    │  ShiHe  │  Zhen   │  Yi(Inc)│  Zhun   │  Yi(Nrn)│  Fu     │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Wind      │  Gou    │  Da Guo │  Ding   │  Heng   │  Xun    │  Jing   │  Gu     │  Sheng  │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Water     │  Song   │ Kun(Op) │  Wei Ji │  Xie    │  Huan   │  Kan    │  Meng   │  Shi    │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Mountain  │  Dun    │  Xian   │  Lü(Wn)│  XiaoGuo│  Jian(D)│ Jian(O) │  Gen    │ Qian(M) │
            ├──────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
  Earth     │  Pi     │  Cui    │  Jin    │  Yu     │  Guan   │  Bi(HT) │  Bo     │  Kun    │
            └──────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
```

### KW Path Character

The sequence path through this grid does NOT cluster, spiral, or follow a simple pattern. Numbers 1-64 scatter across the grid. There is no visible "snaking" or "diagonal" motion. The path is better described as **jumping** — most transitions move to a completely different grid cell (both trigrams change). This is consistent with the finding below that 54/63 transitions change both trigrams.

The grid does show one structural regularity: **pairs always occupy cells that share neither row nor column** (see Task 5). This is forced by the algebraic structure.

---

## Task 3: KW Path Through Trigram-Pair Space

### Transition Classification

All 63 transitions (hex[n] → hex[n+1]) classified by which trigrams change:

| Type | All 63 | Within-pair (32) | Bridge (31) |
|------|:------:|:----------------:|:-----------:|
| Both change | 54 | **32** | 22 |
| Lower-only | 4 | 0 | 4 |
| Upper-only | 5 | 0 | 5 |
| Neither | 0 | 0 | 0 |

### Key Finding: Within-pair transitions ALWAYS change both trigrams

**All 32 within-pair transitions change both lower and upper trigram.** This is not a statistical finding — it is algebraically forced. Every mirror-pair generator (O, M, I, OM, OI, MI, OMI) flips at least one bit in both the lower trigram (L1-L3) and the upper trigram (L4-L6):

| Generator | Lower bits flipped | Upper bits flipped |
|-----------|:-:|:-:|
| O (L1,L6) | 1 (L1) | 1 (L6) |
| M (L2,L5) | 1 (L2) | 1 (L5) |
| I (L3,L4) | 1 (L3) | 1 (L4) |
| OM (L1,L2,L5,L6) | 2 (L1,L2) | 2 (L5,L6) |
| OI (L1,L3,L4,L6) | 2 (L1,L3) | 2 (L4,L6) |
| MI (L2,L3,L4,L5) | 2 (L2,L3) | 2 (L4,L5) |
| OMI (all) | 3 (L1,L2,L3) | 3 (L4,L5,L6) |

**Every generator is a cross-trigram operation.** This is the fundamental structural tension between the two decompositions: the pairing rule (which lives in the mirror-pair frame) cannot be expressed as a trigram-preserving operation. When you flip a hexagram to its pair partner, *both* trigrams always change.

### Bridge transitions: 9 of 31 share a trigram

Among the 31 bridges, 9 preserve one trigram:

| Bridge | Exit hex → Entry hex | Shared trigram |
|--------|---------------------|----------------|
| B3 | Song → Shi | Lower: Water ☵ |
| B6 | Pi → Tong Ren | Upper: Heaven ☰ |
| B11 | Bi(Grace) → Bo | Upper: Mountain ☶ |
| B12 | Fu → Wu Wang | Lower: Thunder ☳ |
| B13 | Da Chu → Yi(Nour.) | Upper: Mountain ☶ |
| B18 | Ming Yi → Jia Ren | Lower: Fire ☲ |
| B26 | Gen → Jian(Dev.) | Lower: Mountain ☶ |
| B27 | Gui Mei → Feng | Upper: Thunder ☳ |
| B30 | Jie → Zhong Fu | Lower: Lake ☱ |

**Asymmetry:** 4 bridges share the lower trigram, 5 share the upper. Near-balanced (no significant asymmetry).

### Lower vs Upper trigram change frequency

| Context | Lower changes | Upper changes |
|---------|:---:|:---:|
| All 63 transitions | 58 | 59 |
| Within-pair (32) | 32 | 32 |
| Bridge (31) | 26 | 27 |

Near-perfect symmetry between lower and upper trigram changes across the entire sequence.

---

## Task 4: The Two Decompositions — Trigram Split vs Mirror-Pair Split

### The core structural relationship

The trigram split divides 6 bits as (L1,L2,L3 | L4,L5,L6).
The mirror-pair split divides 6 bits as (L1↔L6, L2↔L5, L3↔L4).

These two decompositions are **maximally non-aligned**: each mirror pair straddles the trigram boundary, taking one bit from the lower trigram and one from the upper. The trigram boundary falls between L3 and L4, while the mirror-pair structure is symmetric around that same boundary. They are complementary ways of cutting the hexagram.

### Generator → Trigram XOR Table

Each mirror-pair generator, expressed as XOR masks on the lower and upper trigrams:

| Generator | Line flips | Lower XOR | Upper XOR | Lo bits Δ | Up bits Δ |
|-----------|-----------|-----------|-----------|:---------:|:---------:|
| id | none | 000 | 000 | 0 | 0 |
| O | L1,L6 | 100 | 001 | 1 | 1 |
| M | L2,L5 | 010 | 010 | 1 | 1 |
| I | L3,L4 | 001 | 100 | 1 | 1 |
| OM | L1,L2,L5,L6 | 110 | 011 | 2 | 2 |
| OI | L1,L3,L4,L6 | 101 | 101 | 2 | 2 |
| MI | L2,L3,L4,L5 | 011 | 110 | 2 | 2 |
| OMI | all | 111 | 111 | 3 | 3 |

**Key observations:**

1. **Every non-identity generator flips equal numbers of lower and upper bits.** This is not coincidence — each generator flips a *mirror pair*, which by definition has one member in each trigram. Single generators flip 1+1, compound generators flip 2+2, OMI flips 3+3.

2. **The lower XOR and upper XOR are always bit-reversals of each other** (for single generators O, M, I). O gives lower XOR = 100, upper XOR = 001 — mirror images. This reflects the mirror-pair structure: bit k in the lower trigram is paired with bit (3-k) in the upper trigram. Specifically:
   - L1 (lower pos 0) ↔ L6 (upper pos 2) — O generator
   - L2 (lower pos 1) ↔ L5 (upper pos 1) — M generator  
   - L3 (lower pos 2) ↔ L4 (upper pos 0) — I generator

3. **M is the only generator that flips the *same* position in both trigrams** (position 1 in both). O and I flip opposite positions (0↔2). This is why M has a special status in the trigram frame: it's the only generator whose trigram-level effect is symmetric.

### What generators do to trigram identity

| Generator | Effect | Example (from Heaven/Heaven) |
|-----------|--------|-----|
| O | Flips L1 in lower, L6 in upper | Heaven/Heaven → Thunder/Mountain |
| M | Flips L2 in lower, L5 in upper | Heaven/Heaven → Fire/Fire |
| I | Flips L3 in lower, L4 in upper | Heaven/Heaven → Mountain/Thunder |
| OM | Flips L1,L2 in lower; L5,L6 in upper | Heaven/Heaven → Water/Wind |
| OI | Flips L1,L3 in lower; L4,L6 in upper | Heaven/Heaven → Water/Water |
| MI | Flips L2,L3 in lower; L4,L5 in upper | Heaven/Heaven → Wind/Water |
| OMI | Complements both | Heaven/Heaven → Earth/Earth |

**OMI is special:** it's the only generator that independently complements each trigram. The lower trigram maps to its complement, the upper trigram maps to its complement. This means OMI *preserves the trigram decomposition* — it operates within the trigram frame. All other generators produce cross-trigram effects.

### The pair mask as trigram transformation

Since the mask = signature identity (Theorem 5), each orbit's pairs are connected by a specific generator. The trigram-level transformation for each pair depends on its orbit type:

| Orbit sig | Generator | Lower trigram Δ | Upper trigram Δ | #Pairs |
|-----------|-----------|-----------------|-----------------|:------:|
| (0,0,0) | id | — (complement pairs) | — | 4 |
| (1,0,0) | O | Flip bit 0 | Flip bit 2 | 4 |
| (0,1,0) | M | Flip bit 1 | Flip bit 1 | 4 |
| (0,0,1) | I | Flip bit 2 | Flip bit 0 | 4 |
| (1,1,0) | OM | Flip bits 0,1 | Flip bits 1,2 | 4 |
| (1,0,1) | OI | Flip bits 0,2 | Flip bits 0,2 | 4 |
| (0,1,1) | MI | Flip bits 1,2 | Flip bits 0,1 | 4 |
| (1,1,1) | OMI | Flip all | Flip all | 4 |

Note: for id-orbit (complement pairs), the pair members are related by full complement, not by inversion. Their trigram transformation is lower → complement(lower), upper → complement(upper).

---

## Task 5: The 32 Pairs in Trigram Space

### The central theorem: No pair shares a trigram

**All 32 pairs share neither their lower trigram nor their upper trigram.**

- Pairs sharing both trigrams: 0
- Pairs sharing lower only: 0
- Pairs sharing upper only: 0  
- Pairs sharing neither: **32**

This is algebraically forced, not a statistical finding. Because every mirror-pair generator flips at least one bit in each trigram, applying any generator to a hexagram necessarily changes both its lower and upper trigram identity. No pair can share a row or column in the 8×8 grid.

**Geometric interpretation:** Each pair occupies two cells in the 8×8 grid that are never in the same row or column. The 32 pairs place 64 entries in the 8×8 grid such that no pair shares a row or column. This is a constraint that the trigram frame reveals but the orbit frame does not: in orbit space, pairs *do* share orbits (4 pairs per orbit).

### Pair table with trigram compositions

| P# | Hex A: Lo/Up | Hex B: Lo/Up | Gen | Type |
|----|-------------|-------------|-----|------|
| 1 | Heaven/Heaven | Earth/Earth | id | comp |
| 2 | Thunder/Water | Water/Mountain | OM | inv |
| 3 | Heaven/Water | Water/Heaven | OI | inv |
| 4 | Water/Earth | Earth/Water | M | inv |
| 5 | Heaven/Wind | Lake/Heaven | I | inv |
| 6 | Heaven/Earth | Earth/Heaven | OMI | inv |
| 7 | Fire/Heaven | Heaven/Fire | M | inv |
| 8 | Mountain/Earth | Earth/Thunder | I | inv |
| 9 | Thunder/Lake | Wind/Mountain | OMI | inv |
| 10 | Lake/Earth | Earth/Wind | OM | inv |
| 11 | Thunder/Fire | Fire/Mountain | I | inv |
| 12 | Earth/Mountain | Thunder/Earth | O | inv |
| 13 | Thunder/Heaven | Heaven/Mountain | MI | inv |
| 14 | Thunder/Mountain | Wind/Lake | id | comp |
| 15 | Water/Water | Fire/Fire | id | comp |
| 16 | Mountain/Lake | Wind/Thunder | M | inv |
| 17 | Mountain/Heaven | Heaven/Thunder | OM | inv |
| 18 | Earth/Fire | Fire/Earth | OI | inv |
| 19 | Fire/Wind | Lake/Fire | MI | inv |
| 20 | Mountain/Water | Water/Thunder | MI | inv |
| 21 | Lake/Mountain | Thunder/Wind | M | inv |
| 22 | Heaven/Lake | Wind/Heaven | O | inv |
| 23 | Earth/Lake | Wind/Earth | MI | inv |
| 24 | Water/Lake | Wind/Water | I | inv |
| 25 | Fire/Lake | Wind/Fire | OM | inv |
| 26 | Thunder/Thunder | Mountain/Mountain | OI | inv |
| 27 | Mountain/Wind | Lake/Thunder | OMI | inv |
| 28 | Fire/Thunder | Mountain/Fire | O | inv |
| 29 | Wind/Wind | Lake/Lake | OI | inv |
| 30 | Water/Wind | Lake/Water | O | inv |
| 31 | Lake/Wind | Mountain/Thunder | id | comp |
| 32 | Fire/Water | Water/Fire | OMI | inv |

### Inversion pairs: the trigram swap-and-reverse

For the 28 inversion pairs, the transformation is:
- lower_b = reverse(upper_a)
- upper_b = reverse(lower_a)

This is a **coupled operation**: it simultaneously swaps the trigrams AND reverses each one. The reversal matters because 4 of 8 trigrams are non-palindromic:

| Palindromic (reverse = self) | Non-palindromic pairs |
|:---:|:---:|
| Heaven (111), Earth (000), Water (010), Fire (101) | Mountain (001) ↔ Thunder (100), Wind (011) ↔ Lake (110) |

When both trigrams of hex A are palindromic (Heaven, Earth, Water, Fire), inversion is a simple swap: lower_b = upper_a, upper_b = lower_a. The pair occupies symmetric positions in the grid (reflected across the diagonal).

When either trigram is non-palindromic, inversion also transforms the trigram identity: Mountain becomes Thunder, Wind becomes Lake (and vice versa). This makes the trigram-level relationship more complex.

### Complement pairs: independent trigram complementation

The 4 complement pairs (id-orbit) transform each trigram independently:
- Pair 1: Heaven/Heaven ↔ Earth/Earth (complement of each)
- Pair 14: Thunder/Mountain ↔ Wind/Lake (complement of each)
- Pair 15: Water/Water ↔ Fire/Fire (complement of each)
- Pair 31: Lake/Wind ↔ Mountain/Thunder (complement of each)

These pairs occupy diagonally opposite positions in the grid.

---

## Task 6: Nuclear Trigrams

### Nuclear trigram decomposition

Nuclear lower = (L2,L3,L4): shares L2,L3 with the lower primary trigram and L4 with the upper.
Nuclear upper = (L3,L4,L5): shares L3 with the lower primary and L4,L5 with the upper.

**Nuclear trigram frequency:** Each of the 8 trigrams appears exactly 8 times as nuclear lower and exactly 8 times as nuclear upper. This is a forced property.

**Nuclear (lower, upper) pair frequency:** Only 16 of the 64 possible combinations appear, each exactly 4 times. The nuclear pair space is exactly 1/4 the size of the primary pair space.

The 16 nuclear pairs that appear:

| Nuclear lower | Nuclear upper | Count | Hexagrams |
|--------------|---------------|:-----:|-----------|
| Heaven | Heaven | 4 | 1, 28, 43, 44 |
| Heaven | Lake | 4 | 14, 32, 34, 50 |
| Earth | Earth | 4 | 2, 23, 24, 27 |
| Earth | Mountain | 4 | 3, 8, 20, 42 |
| Thunder | Earth | 4 | 4, 7, 19, 41 |
| Thunder | Mountain | 4 | 29, 59, 60, 61 |
| Lake | Fire | 4 | 5, 9, 48, 57 |
| Lake | Thunder | 4 | 11, 18, 26, 46 |
| Fire | Wind | 4 | 6, 10, 47, 58 |
| Fire | Water | 4 | 38, 40, 54, 64 |
| Wind | Heaven | 4 | 13, 31, 33, 49 |
| Wind | Lake | 4 | 30, 55, 56, 62 |
| Water | Fire | 4 | 37, 39, 53, 63 |
| Water | Thunder | 4 | 15, 22, 36, 52 |
| Mountain | Wind | 4 | 12, 17, 25, 45 |
| Mountain | Water | 4 | 16, 21, 35, 51 |

### Verification: Nuclear trigram rule ≡ M-component (Theorem 12)

For all 16 M-decisive pairs (where L2 ≠ L5 in the first hexagram):

| Pair | First hex | L2 | L5 | L2=yin? | Nuc.Lo yang | Nuc.Up yang | NL < NU? | Match? |
|:----:|-----------|:--:|:--:|:-------:|:-----------:|:-----------:|:--------:|:------:|
| 2 | Zhun | 0 | 1 | ✓ | 0 | 1 | ✓ | ✓ |
| 4 | Shi | 1 | 0 | ✗ | 1 | 0 | ✗ | ✓ |
| 6 | Tai | 1 | 0 | ✗ | 2 | 1 | ✗ | ✓ |
| 7 | Tong Ren | 0 | 1 | ✓ | 2 | 3 | ✓ | ✓ |
| 9 | Sui | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |
| 10 | Lin | 1 | 0 | ✗ | 1 | 0 | ✗ | ✓ |
| 13 | Wu Wang | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |
| 16 | Xian | 0 | 1 | ✓ | 2 | 3 | ✓ | ✓ |
| 17 | Dun | 0 | 1 | ✓ | 2 | 3 | ✓ | ✓ |
| 19 | Jia Ren | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |
| 20 | Jian(Obst.) | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |
| 21 | Sun | 1 | 0 | ✗ | 1 | 0 | ✗ | ✓ |
| 23 | Cui | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |
| 25 | Ge | 0 | 1 | ✓ | 2 | 3 | ✓ | ✓ |
| 27 | Jian(Dev.) | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |
| 32 | Ji Ji | 0 | 1 | ✓ | 1 | 2 | ✓ | ✓ |

**Result: 16/16 match.** The nuclear trigram rule (nuclear lower yang < nuclear upper yang) is algebraically identical to the M-component rule (L2=yin first). This is because:

nuclear lower yang - nuclear upper yang = (L2 + L3 + L4) - (L3 + L4 + L5) = L2 - L5

So nuclear lower < nuclear upper ⟺ L2 < L5 ⟺ L2=0, L5=1 ⟺ L2=yin.

The nuclear trigram rule is the M-component, seen from the trigram frame. Same structure, different language.

### Nuclear trigram path structure

Nuclear trigram changes across the KW sequence:

| Type | Within-pair (32) | Bridge (31) | Total (63) |
|------|:---:|:---:|:---:|
| Both change | 28 | 25 | 53 |
| Nuc. lower only | 0 | 0 | 0 |
| Nuc. upper only | 0 | 5 | 5 |
| Neither | 4 | 1 | 5 |

Notable: **4 within-pair transitions preserve both nuclear trigrams.** All 4 use the same generator: **O** (XOR mask 100001, flipping only L1 and L6). This is algebraically necessary: nuclear trigrams use bits L2-L5, and O is the only generator that flips bits *outside* this range (L1 and L6 only). The O generator is invisible to nuclear trigrams.

The 4 O-generator pairs preserving nuclear trigrams:

| Pair | Hex A → Hex B | Nuclear lower | Nuclear upper |
|:----:|---------------|:-------------:|:-------------:|
| 12 | Bo → Fu | Earth ☷ | Earth ☷ |
| 22 | Guai → Gou | Heaven ☰ | Heaven ☰ |
| 28 | Feng → Lü(Wand.) | Wind ☴ | Lake ☱ |
| 30 | Huan → Jie | Thunder ☳ | Mountain ☶ |

**1 bridge also preserves both nuclear trigrams:** B30 (Jie → Zhong Fu), with nuclear pair (Thunder, Mountain). This means the hidden dynamic persists across the pair boundary — the inner structural character of Jie carries into Zhong Fu despite the primary trigrams changing.

**Nuclear lower never changes alone** (0 cases at any transition). When nuclear lower changes, nuclear upper always changes too. But nuclear upper can change alone (5 bridge transitions). This asymmetry arises because nuclear lower (L2,L3,L4) and nuclear upper (L3,L4,L5) share two bits (L3,L4) — they are strongly coupled. A transition that changes nuclear upper but not nuclear lower must change L5 without changing L2, L3, or L4. This is exactly what happens when only the M-component (L2↔L5) contributes at the upper end.

---

## Summary: What the Trigram Substrate Reveals

### Three structural findings

**1. The cross-trigram theorem: Mirror-pair operations always change both trigrams.**

Every generator in the pairing structure flips bits in both the lower and upper trigram. This is because each generator acts on a *mirror pair* — one line from the lower trigram (L1, L2, or L3) and one from the upper (L4, L5, or L6). Consequence: no KW pair can share a trigram. All 32 pairs differ in both their lower and upper trigram identity.

This is the central structural tension between the two decompositions. The pairing rule lives naturally in the mirror-pair frame (where pairs share an orbit). The trigram frame sees pairs as maximally displaced — every pair jumps to a different row AND column of the 8×8 grid.

**2. The M-generator symmetry: M is unique in the trigram frame.**

Among the three single generators, M is the only one that flips the *same* position in both trigrams (position 1, i.e., the middle bit). O flips position 0 in lower and position 2 in upper. I flips position 2 in lower and position 0 in upper. But M flips position 1 in both. This gives M a symmetric, non-crossing character in the trigram frame — explaining why the M-component has special status in both the algebraic findings (Theorem 12, the nuclear trigram equivalence) and the meaning findings (activity/receptivity correlation).

**3. Bridge transitions concentrate trigram sharing: 9/31 bridges preserve one trigram.**

While within-pair transitions are forced to change both trigrams, bridges are free. 9 of 31 bridges preserve exactly one trigram (4 preserve lower, 5 preserve upper). These are the transitions where the sequence moves along a row or column of the 8×8 grid rather than jumping to a completely new cell. Whether this 9/31 rate is significant (vs random pair orderings) is a question for subsequent analysis.

### What the trigram frame sees that the orbit frame doesn't

1. **The 8×8 grid as a map.** The orbit frame sees 8 orbits of 8 hexagrams each, connected by bridges. The trigram frame sees 64 cells in an 8×8 grid, where each cell has both a structural identity (which trigram pair) and a meaning identity (which situational interaction). The sequence traces a path through this grid. The grid's geometry — which cells are adjacent, which transitions preserve a trigram — creates a distance metric that the orbit frame lacks.

2. **The pairing constraint as non-adjacency.** In the orbit frame, pair partners share an orbit. In the trigram frame, pair partners are *never* adjacent (never share a row or column). This is the same constraint seen from opposite angles: orbit sharing means algebraic closeness; trigram non-sharing means grid-distance.

3. **Nuclear trigrams as the bridge between frames.** Nuclear trigrams (L2-L4, L3-L5) overlap with both primary trigrams. They sit physically between lower and upper, sharing bits with each. The nuclear trigram rule ≡ M-component proves that this intermediate layer connects to the mirror-pair structure. The full nuclear pair space is much smaller (16 types vs 64) — it's a contracted view that might reveal patterns invisible at full resolution.

### Questions opened

1. **Is the 9/31 bridge trigram-sharing rate significant?** Compare to random pair orderings. If bridges that share a trigram are more common than expected, the sequence preferentially moves along grid rows/columns at pair boundaries.

2. **What meaning structure does the 8×8 grid carry?** Each cell is a specific inner-outer trigram interaction. Adjacent cells (sharing a trigram) represent situations that share either their inner or outer condition. The KW path's choice of which grid transitions to use at bridges — and specifically which trigram to preserve — may encode the developmental logic found in iter6.

3. **Does the trigram frame explain complementary coverage?** Algebraically rigid pairs (where flipping degrades all 4 axes) vs algebraically flexible pairs — do they differ in their trigram-level properties? If the rigid pairs are those where the trigram transition structure is tightest, that would explain why meaning has less work to do there.

4. **The nuclear contraction:** 64 hexagrams map to only 16 nuclear pair types (each appearing 4×). Does the KW path through nuclear space have structure that the full trigram path obscures?

5. **The M-generator's special status:** M is the only generator with symmetric trigram-level effects. This connects to M being the strongest orientation signal (L2=yin first, p ≈ 0.04). Is there a trigram-level explanation for why M's symmetry makes it a natural orientation criterion?

---

## Data Files

| File | Contents |
|------|----------|
| `trigram_decompose.py` | Complete computation script for all 6 tasks |
| `round1-trigram-map.md` | This document |
