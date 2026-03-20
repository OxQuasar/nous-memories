# Mod-9 Investigation — Questions

## Core Question: What is the structural relationship between the 後天 mod-9 divination arithmetic and the F₂³/Z₅ algebraic structure?

The 梅花易數 describes two divination methods. The 先天 method uses mod-8 arithmetic on the Fu Xi ordering. The 後天 method uses mod-9 arithmetic on the Lo Shu ordering with a 9th "center" position. The mod-8 system has been fully characterized (mod8/findings.md §I–§IX). The mod-9 system is unexamined.

### The 後天 numbering

From 梅花易數 vol2 line 16:

| Lo Shu # | Trigram | Binary | Element | Z₅ | Direction |
|----------|---------|--------|---------|-----|-----------|
| 1 | 坎 | 010 | 水 | 4 | N |
| 2 | 坤 | 000 | 土 | 2 | SW |
| 3 | 震 | 001 | 木 | 0 | E |
| 4 | 巽 | 110 | 木 | 0 | SE |
| 5 | (中) | — | 土 | 2 | Center |
| 6 | 乾 | 111 | 金 | 3 | NW |
| 7 | 兌 | 011 | 金 | 3 | W |
| 8 | 艮 | 100 | 土 | 2 | NE |
| 9 | 離 | 101 | 火 | 1 | S |

Position 5 (中/Center) has no trigram — it is the 9th state the I Ching cannot represent. The 後天 system operates on 9 positions, not 8. This is the structural gap noted in the fana document.

### How the 後天 method works (vol1 lines 149–151, vol2 line 16)

- **Input:** Physical observation (object + direction). Object → upper trigram (by 象 correspondence). Compass direction of the object → lower trigram (by Lo Shu position).
- **Moving line:** Sum of object number + direction number + hour, mod 6.
- **Evaluation:** Uses 爻辞 (line texts) AND 卦辭 (hexagram texts), not just 體用 五行. This is different from 先天 method.

### Key structural differences from mod-8

| | 先天 (mod-8) | 後天 (mod-9) |
|---|---|---|
| Number system | Z₈ | Z₉ (with center) |
| Trigram mapping | 8 positions = 8 trigrams (bijection) | 9 positions, 8 trigrams + 1 center (surjection) |
| Input | Calendar arithmetic | Physical observation + compass |
| Evaluation | 體用 五行 only | 體用 + 爻辭 + 卦辭 |
| Numbering basis | Fu Xi binary counter | Lo Shu magic square |
| Complement | Position n ↔ 9−n | Position n ↔ 10−n (through center 5) |

### Questions

**N1:** What does the Lo Shu cycle (1→2→3→4→5→6→7→8→9) project to on Z₅? Is it retrograde, prograde, or mixed? How does it compare to the 先天 palindrome?

**N2:** Position 5 (center/土) is the 9th state. In mod-9 arithmetic, does it act as a fixed point, an absorbing state, or a pass-through? What happens to 體用 evaluation when one trigram "would be" position 5?

**N3:** The Lo Shu magic square has rows/columns/diagonals summing to 15. The 先天 ordering is a binary counter. Do the magic square constraints produce any Z₅ structure (e.g., do rows/columns/diagonals have balanced 五行 distributions)?

**N4:** The flying star path (Lo Shu traversal: 5→6→7→8→9→1→2→3→4) has constant Hamming distance 2 between consecutive steps (from opposition-theory/loshu.md). What is its Z₅ type sequence? Compare to 先天 and 後天 compass cycles.

**N5:** The 後天 method uses 爻辭 for evaluation. The mod-8 investigation showed the 先天 method's 體用 evaluation is structurally independent of the hexagram texts (8c.5: 0/17 domains reference hexagram names). Does the 後天 method's use of 爻辭 connect the algebraic grammar to the textual layer that 先天 bypasses?

**N6:** The fana document claims the 9th state (center) is "something the I Ching structurally cannot represent" and that a 36-number grid "completes" it. Is position 5 genuinely a structural gap, or is it Earth (土) represented by its trigrams (坤=2, 艮=8) at two other positions already?

### Connection to mod-8 findings

The mod-8 investigation established that Z₈ and Q₃ are topologically incommensurable for grammar transport (§VII). The 後天 system introduces Z₉ — a different modular arithmetic. Key question: does Z₉ have any structural advantage over Z₈ for accessing Q₃ grammar? Since gcd(9,8)=1 (coprime), the Z₉ and Z₈ cycles are maximally misaligned. The center position breaks the bijection with trigrams, introducing a state that has element content (土) but no binary representation.

### Source

梅花易數 vol1 lines 140, 149–151; vol2 lines 15–16. Full text in `texts/meihuajingshu/`.
