# Round 1: 天干 & 地支 → Trigram Analysis Results


PART A: 天干 (Heavenly Stems)
─────────────────────────────
1. Stem→Trigram mapping: Well-defined for 8/10 stems via element+polarity.
   Fire & Water collapse (2 stems → 1 trigram each).
   Earth assignment (Wu→Gen or Kun) is ambiguous.

2. 合化 (Five Combinations): 5 stem pairs → 3 non-trivial + 2 trivial trigram pairs.
   NOT a clean involution on 8 trigrams due to Fire/Water collapse.
   The 3 non-trivial pairs are: {Zhen,Kun/Gen}, {Xun,Dui}, {Li,Kan/Qian}
   (depends on Earth assignment).
   Block compatibility is FORCED through the element layer.

3. Polarity: Stem yin/yang → trigram yin/yang is BROKEN by Fire/Water collapse.
   Li and Kan each receive both yang and yin stems.

PART B: 地支 (Earthly Branches)
─────────────────────────────
1. Branch→Trigram mapping: Well-defined via 24 Mountains (Later Heaven Bagua).
   12→8 mapping with specific collisions at intercardinal trigram sectors.

2. 六冲 (Six Clashes): Produces 4 non-trivial + 2 trivial trigram pairs.
   The 4 non-trivial pairs = ι₂ (KW diametric / Lo Shu).
   BUT this is geometrically forced (六冲 = diametric on LH Bagua = ι₂).

3. 六合 (Six Harmonies): Produces non-trivial trigram pairings that
   partially overlap with multiple known involutions.
   Does NOT form a clean involution (some trigrams paired with multiple others).

4. 三合 (Three Harmonies): Each triple hits 3 of 4 blocks.
   The 4 triples partition the 12 branches into 4 groups by frame-element.

5. Polarity: Branch yin/yang → trigram yin/yang is BROKEN.
   Each trigram sector contains both yang and yin branches.

VERDICT: Neither system independently produces new involutions.
─────────────────────────────────────────────────────────────
The stem/branch systems are primarily ELEMENT-ENCODING systems.
Their pairing structures (合化, 六冲, 六合, 三合) operate through
the element layer and/or the compass geometry. Block compatibility
is trivially forced through these intermediaries.

The most structurally interesting finding is that 六冲 reproduces ι₂
exactly (including the geometric explanation of WHY), and that 六合
creates a different connectivity pattern on trigrams that doesn't
reduce to any single involution.

## Detailed Data

### Stem → Trigram Mapping (Option A: Wu→Gen, Ji→Kun)

| Stem | Yin/Yang | Element | Trigram |
|------|----------|---------|--------|
| 甲 Jiǎ | Yang | Wood | Zhen |
| 乙 Yǐ | Yin | Wood | Xun |
| 丙 Bǐng | Yang | Fire | Li |
| 丁 Dīng | Yin | Fire | Li |
| 戊 Wù | Yang | Earth | Gen |
| 己 Jǐ | Yin | Earth | Kun |
| 庚 Gēng | Yang | Metal | Qian |
| 辛 Xīn | Yin | Metal | Dui |
| 壬 Rén | Yang | Water | Kan |
| 癸 Guǐ | Yin | Water | Kan |

### Branch → Trigram Mapping (24 Mountains)

| Branch | Yin/Yang | Element | Direction | Trigram | Trigram Element |
|--------|----------|---------|-----------|---------|----------------|
| 子 Zǐ | Yang | Water | N | Kan | Water |
| 丑 Chǒu | Yin | Earth | NNE | Gen | Earth |
| 寅 Yín | Yang | Wood | ENE | Gen | Earth |
| 卯 Mǎo | Yin | Wood | E | Zhen | Wood |
| 辰 Chén | Yang | Earth | ESE | Xun | Wood |
| 巳 Sì | Yin | Fire | SSE | Xun | Wood |
| 午 Wǔ | Yang | Fire | S | Li | Fire |
| 未 Wèi | Yin | Earth | SSW | Kun | Earth |
| 申 Shēn | Yang | Metal | WSW | Kun | Earth |
| 酉 Yǒu | Yin | Metal | W | Dui | Metal |
| 戌 Xū | Yang | Earth | WNW | Qian | Metal |
| 亥 Hài | Yin | Water | NNW | Qian | Metal |

### 六冲 → Trigram Pairs

| Branch Pair | Trigram Pair | Trivial? | Involution |
|-------------|-------------|----------|------------|
| 子 Zǐ↔午 Wǔ | Kan↔Li | No | ι₂ |
| 丑 Chǒu↔未 Wèi | Gen↔Kun | No | ι₂ |
| 寅 Yín↔申 Shēn | Gen↔Kun | No | ι₂ |
| 卯 Mǎo↔酉 Yǒu | Zhen↔Dui | No | ι₂ |
| 辰 Chén↔戌 Xū | Xun↔Qian | No | ι₂ |
| 巳 Sì↔亥 Hài | Xun↔Qian | No | ι₂ |

### 六合 → Trigram Pairs

| Branch Pair | Result Element | Trigram Pair |
|-------------|---------------|-------------|
| 子 Zǐ+丑 Chǒu | Earth | Kan↔Gen |
| 寅 Yín+亥 Hài | Wood | Gen↔Qian |
| 卯 Mǎo+戌 Xū | Fire | Zhen↔Qian |
| 辰 Chén+酉 Yǒu | Metal | Xun↔Dui |
| 巳 Sì+申 Shēn | Water | Xun↔Kun |
| 午 Wǔ+未 Wèi | Fire | Li↔Kun |

### 三合 → Trigram Triples

| Frame Element | Branches | Trigrams | Blocks Hit |
|--------------|----------|---------|------------|
| Water | 申 Shēn,子 Zǐ,辰 Chén | Kan,Kun,Xun | [0, 2, 3] |
| Wood | 亥 Hài,卯 Mǎo,未 Wèi | Kun,Qian,Zhen | [0, 3] |
| Fire | 寅 Yín,午 Wǔ,戌 Xū | Gen,Li,Qian | [1, 2, 3] |
| Metal | 巳 Sì,酉 Yǒu,丑 Chǒu | Dui,Gen,Xun | [1, 3] |

### Key Structural Findings

1. **六冲 = ι₂**: The Six Clashes reproduce the KW diametric involution exactly.
   This is geometrically necessary (diametric on 12-branch circle = diametric on LH Bagua).

2. **10→8 collapse prevents clean involutions from stems**:
   Fire (Li) and Water (Kan) each absorb 2 stems, breaking the 1:1 mapping.

3. **★ 六合 has ZERO edge overlap with all 4 known involutions ★**:
   The 6 trigram pairs induced by 六合 use exclusively edges from the complement
   of the involution edge set within K₈. This means:
   - K₈ has 28 edges total
   - The 4 involutions (ι₁, ι₂, ι₃, τ) use 12 distinct edges
   - 六合 uses 6 edges from the remaining 16
   - 10 edges are claimed by neither system
   - The 六合 graph is bipartite, all-cross-block, with degree sequence [2,2,2,2,1,1,1,1]
   - Block 3↔0 and Block 3↔1 each get 2 六合 edges; Block 0↔2 and Block 1↔2 each get 1

4. **三合 triples each span 3 of 4 blocks**: Each frame-element triple
   covers 3 blocks, leaving 1 uncovered. The 4 triples together cover all blocks.

5. **Neither system independently produces new involutions or the polarity partition.**
   All block compatibility is forced through the element layer or compass geometry.
   However, the 六合 zero-overlap with involution edges is geometrically non-trivial
   and suggests the 六合 connectivity may encode an independent structural layer.
