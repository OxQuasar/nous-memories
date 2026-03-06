# 火珠林 Algebraic Structure Analysis

The 火珠林 method reads hexagrams through palace coordinates (八宮 → 納甲 → 六親 → 旺衰).
Our algebraic framework reads through basin/kernel coordinates (互 → inner space → attractor).
These are provably orthogonal decompositions. The question: what IS 納甲 algebraically?
Does 火珠林 access the same information through different coordinates, or genuinely different information?

## 1. 納甲 as a Map on Z₂⁶

Each hexagram deterministically receives six 干支 labels. The assignment depends on:
(a) which trigrams compose it, (b) which palace it belongs to, (c) upper/lower position.

Express this as a function f: Z₂⁶ → (Z₁₀ × Z₁₂)⁶. Is it linear, affine, or nonlinear?
Does it factor through the trigram decomposition (the 3+3 bit split)?
Does any part of it depend on the inner bits (h₁,h₂,h₃,h₄) vs outer bits (b₀,b₅)?

The 天干 assignment is determined by trigram identity → one of {甲,乙,丙,丁,戊,己,庚,辛,壬,癸}.
The 地支 assignment cycles from a trigram-specific starting point, ascending (陽) or descending (陰).
Both depend on trigram identity, not on which hexagram the trigram appears in (except for 乾/坤
which split by position). So 納甲 factors through the trigram pair plus position flag.

Key test: two hexagrams with the same inner bits but different outer bits — do they share
any 納甲 structure? If 納甲 is entirely determined by the two trigrams (3+3 bit split),
then it's blind to the inner space entirely and reads orthogonal information.

## 2. Palace Generation in Kernel Language

The palace generation algorithm applies cumulative XOR masks from the root hexagram.
We know the mask set from the attractors work. But the palace rank (一世 through 歸魂)
determines the 世應 positions, which are the judgment anchors.

Map every hexagram's palace rank onto the kernel/basin decomposition. Is palace rank
correlated with convergence depth? With basin? With any kernel component (O, M, I)?

The 世 line position (1-6) is a function of palace rank. Express it as a function
of the hexagram's algebraic coordinates. Does 世 ever land on an interface line (3 or 4)?
When it does, does that have special significance in the basin framework?

## 3. 六親 as a Composite Function

六親(line) = 生克(line_element, palace_element). The line element comes from its 地支.
The palace element comes from the root trigram's element.

Six hexagrams sharing the same inner bits (the kernel fiber) — do they have the same
六親 assignments? If yes, 六親 lives on the inner space. If no, 六親 requires the
full 6-bit resolution and captures information that 互 discards.

Also: the six 六親 labels on a hexagram form a word over {父母,兄弟,妻財,子孫,官鬼}.
How many distinct 六親 words exist across the 64 hexagrams? How do they distribute
across palaces, basins, and kernel classes?

## 4. 飛伏 vs 互

Both are "hidden structure" mechanisms that answer what lies beneath the surface.

互 is a linear projection: 6 bits → 4 effective bits, extracting the nuclear hexagram.
飛伏 is a lookup: overlay the palace root's lines beneath the current hexagram.
The palace root is the pure doubled trigram at the head of the palace.

For each hexagram, compare: what does 互 reveal vs what does 飛伏 reveal?
互 shows the hidden dynamic (convergence toward attractor).
飛伏 shows the hidden relations (六親 present in the root but absent in the current hexagram).

When is 妻財 hidden (伏)? When is 官鬼 hidden? Map these absences onto the inner space.
Is the pattern of which 六親 are missing algebraically structured?

## 5. Multiple 動爻 in Kernel Language

梅花 flips exactly one line: 6 possible 變, each with a specific kernel (O, M, or I).
火珠林 can flip any subset of {1,...,6}: 64 possible 變 patterns, each an element of Z₂⁶.

Each 變 pattern has a kernel decomposition (O, M, I). The coin-toss mechanism has
specific probabilities: P(old yin) = P(old yang) = 1/8, P(young) = 3/8.
So P(line moves) = 1/4 independently per line.

What's the probability distribution over I-components (basin-crossing potential)?
P(I=0) vs P(I=1) under the coin mechanism. Is the method biased toward basin
preservation or basin crossing? Compare to 梅花's deterministic single-line flip.

Also: when multiple lines move, the 變卦 can be far from the 本卦 in Hamming distance.
What's the expected distance? Expected number of basin crossings?

## 6. 旺相休囚死 as Seasonal Metric

The seasonal strength is a cyclic permutation of {旺,相,休,囚,死} over the 五行,
rotating with the seasons (Wood→Fire→Earth→Metal→Water, spring→summer→...→winter).

This is a time-dependent weighting on the five-phase graph. In the inner space,
each node carries an element pair (from nuclear trigrams). The seasonal metric
selects which element pairs are currently empowered vs suppressed.

Does this interact with basin structure? In spring (Wood 旺), Wood is the universal
intruder in fixed-point convergence — does "Wood empowered" mean convergence
friction is amplified? In autumn (Metal 旺), Metal is a fixed-point attractor element —
does "Metal empowered" mean the Qian attractor is strengthened?

Map the seasonal rotation onto the inner-space five-phase graph. Four seasons give
four different weightings of the same graph. Does any season align with or oppose
the convergence dynamics?
