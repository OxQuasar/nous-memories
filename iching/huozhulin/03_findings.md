# Probe 3: 六親 as a Composite Function

## 1. Verification

姤 (乾宮 Metal): word = 父孫兄鬼兄父
= 父母,子孫,兄弟,官鬼,兄弟,父母. Matches example.md exactly. ✓

Missing from 姤: {妻財} — 妻財 absent (Wood, overcome by Metal).

## 2. Inner-Bit Fiber Test (Cross-Talk Detection)

Group 64 hexagrams by inner bits (b₁,b₂,b₃,b₄): 16 groups of 4.

If 六親 lived on the inner space: every group would have 1 word.
If it requires full 6-bit resolution: groups will have multiple words.

| Distinct words per group | Groups |
|--------------------------|--------|
| 4 | 16 |

**No group has identical words.** Every inner-bit group contains hexagrams with
different 六親 assignments. The composition introduces **total cross-talk** —
六親 requires the full 6-bit hexagram, not just the inner 4 bits.

This is expected: 六親 depends on palace element (determined by palace membership,
which traverses the onion) AND branch elements (from 納甲, which reads the trigram
pair). The outer bits (b₀, b₅) change the trigram identities and therefore the
branch elements, while palace membership follows a different path through the
onion. Both channels contribute information that cannot be recovered from inner
bits alone.

## 3. 六親 Word Census

**59 distinct 六親 words** across 64 hexagrams.

| Frequency | Words with this frequency |
|-----------|--------------------------|
| 1× | 54 |
| 2× | 5 |

Most common words:

| Word | Count |
|------|-------|
| 財鬼兄兄財孫 | 2 |
| 父鬼兄兄財孫 | 2 |
| 父鬼兄父孫兄 | 2 |
| 財父鬼財父鬼 | 2 |
| 父兄財財父鬼 | 2 |
| 兄父鬼兄財孫 | 1 |
| 孫鬼財鬼兄父 | 1 |
| 孫鬼兄鬼兄父 | 1 |
| 財孫兄父兄財 | 1 |
| 父兄財父兄財 | 1 |

## 4. 六親 Words × Palace

| Palace | Element | Distinct words (of 8) |
|--------|---------|-----------------------|
| Kun ☷ | Earth | 7 |
| Zhen ☳ | Wood | 8 |
| Kan ☵ | Water | 8 |
| Dui ☱ | Metal | 8 |
| Gen ☶ | Earth | 8 |
| Li ☲ | Fire | 8 |
| Xun ☴ | Wood | 7 |
| Qian ☰ | Metal | 8 |

## 5. 六親 Words × Basin

| Basin | Hexagrams | Distinct words |
|-------|-----------|----------------|
| Kun | 16 | 15 |
| Qian | 16 | 16 |
| Cycle | 32 | 30 |

Overlap: Kun∩Qian=0, Kun∩Cycle=2, Qian∩Cycle=0, all three=0

## 6. Missing 六親

| Missing count | Hexagrams |
|---------------|-----------|
| 0 | 16 |
| 1 | 32 |
| 2 | 16 |

### Which types are most commonly missing?

| Type | Missing in N hexagrams |
|------|------------------------|
| 兄弟 (兄) | 13 |
| 子孫 (孫) | 21 |
| 父母 (父) | 9 |
| 妻財 (財) | 11 |
| 官鬼 (鬼) | 10 |

### Missing by basin

| Basin | 兄 | 孫 | 父 | 財 | 鬼 |
|-------|----|----|----|----|-----|
| Kun | 2 | 3 | 4 | 2 | 1 |
| Qian | 3 | 5 | 3 | 4 | 1 |
| Cycle | 8 | 13 | 2 | 5 | 8 |

## 7. Mutual Information (Cross-Talk Quantification)

| Variable pair | MI (bits) | Normalized (/ H(word)) |
|---------------|-----------|------------------------|
| word × inner | 3.8438 | 0.6578 |
| word × outer | 1.9062 | 0.3262 |
| word × palace | 2.9062 | 0.4973 |
| word × basin | 1.4375 | 0.2460 |

H(六親 word) = 5.8438 bits

**Substantial cross-talk.** The 六親 word carries significant information about
the inner bits, even though neither ingredient (納甲 or palace) individually
transmits inner-bit information efficiently. The COMPOSITION creates a channel
between shell structure and core structure.

## 8. Key Findings

### Finding 1: 六親 requires full 6-bit resolution

16/16 inner-bit groups have multiple distinct 六親 words. The composition of 納甲 (shell reader) and palace element (onion traversal) does not collapse to an inner-space function.

### Finding 2: Palace element dominates

I(word; palace) = 2.9062 accounts for 49.7% of the word entropy. The palace element (which 五行 to compare against) is the primary determinant.

### Finding 3: Composition creates near-complete information recovery

I(word; inner) = 3.8438 bits = 96.1% of max inner entropy (4 bits).
I(word; outer) = 1.9062 bits = 95.3% of max outer entropy (2 bits).
The 六親 word recovers almost ALL information about both inner and outer bits.

Neither ingredient alone captures inner-bit information (納甲 is inner-blind,
palace membership is orthogonal to basins). But their COMPOSITION — using palace
element as the comparison reference for branch elements — creates a near-injective
function on Z₂⁶. The two orthogonal projections are **complementary**: together
they reconstruct virtually the entire hexagram identity.

### Finding 4: Near-injectivity — only 5 degenerate pairs

59 distinct words for 64 hexagrams. The 5 word-collisions:

| Word | Hexagram A | Palace A | Hexagram B | Palace B |
|------|-----------|----------|-----------|----------|
| 財鬼兄兄財孫 | 000001 | Kun ☷ | 000111 | Kun ☷ |
| 父鬼兄兄財孫 | 000011 | Kun ☷ | 110011 | Gen ☶ |
| 父鬼兄父孫兄 | 000100 | Dui ☱ | 111011 | Gen ☶ |
| 財父鬼財父鬼 | 000110 | Zhen ☳ | 110110 | Xun ☴ |
| 父兄財財父鬼 | 110001 | Xun ☴ | 110111 | Xun ☴ |

4 of 5 pairs share the same palace element (Earth-Earth or Wood-Wood), so
identical 納甲 branch sequences produce the same 生克 pattern. The 5th pair
(000100 Metal vs 111011 Earth) has different palace elements — a deeper
coincidence where different branch sequences against different references
produce the same 六親 word.

### Finding 5: Kun∩Qian = ∅ in word space

No 六親 word appears in both fixed-point basins. The two basins have
completely disjoint 六親 vocabularies. Only the Cycle basin shares 2 words
with Kun (and 0 with Qian).

### Finding 6: Missing count follows 0:32:16 = 1:2:1

16 hexagrams missing 0 types, 32 missing 1, 16 missing 2. This 1:2:1 ratio
suggests a binomial-like structure — possibly each of 2 independent factors
contributes 0 or 1 missing type.

### Finding 7: Missing types are not uniform

子孫 is missing most often (21 hexagrams), 父母 least often (9). The missing pattern is the input for Probe 4 (飛伏): hidden lines supply exactly the absent types.
