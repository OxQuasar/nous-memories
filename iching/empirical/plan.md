# Empirical Plan — Probe 8: 梅花易數

**Source:** `texts/meihuajingshu/` (vol1–vol5, appendix)

The 梅花易數 is the operational manual for the 五行 grammar. It provides a fully deterministic algorithm (date → hexagram → 體用 → 五行 relation → prediction), 10 worked examples, decision rules for 18 domains, seasonal modulation tables, and the 納甲 line-level element assignment. Everything is in-house. Zero external dependencies.

`plan-ideas.md` has other probe ideas (climate, medicine, politics, ecology, cross-domain).

---

## TODO

### Next empirical test: source with date resolution

8b established the resolution boundary: the grammar requires relational input (体 + 用) at temporal resolution finer than year-level. The 梅花 date formula demands year+month+day+hour. The 皇極經世 provides only year (0.9% of entries mention months). The grammar is untestable with this data.

**What would enable the test:**
- A historical source with events dated to month+day (e.g. 《資治通鑒》 has many day-level dates in Chinese calendar format)
- A dataset of divination records with full timestamps and recorded outcomes
- Modern time-series data discretized via the 梅花 mod-8 algorithm (→ connects to mod8/ investigation)

**What the test would look like:**
1. Convert full dates (year+month+day+hour) to 梅花 hexagrams via the algorithm
2. Compute 体用 五行 relation → favorable/unfavorable prediction
3. Compare against independently classified event outcomes
4. Run 120-permutation control

This is parked until a suitable data source is identified.

### Q-卦辭: 吉 Depletion in Hexagram Judgments

Probe 7a found standalone 吉 absent from the 24 kernel lines (p=0.0006). Does this extend to the 卦辭 (hexagram-level judgments)?

**Method:**
1. Extract 卦辭 for the 4 kernel hexagrams (坤, 剥, 夬, 乾)
2. Check for standalone 吉 vs 元吉 vs 利 vs 凶
3. Compare rates against the other 60 hexagrams

Small N (4 hexagrams), data in atlas.json. Quick test that strengthens or bounds the 7a finding.

---

## What Would Change Our Understanding

- **Date-resolution test significant:** The grammar predicts event character from full timestamps. Would require careful confound examination.
- **Date-resolution test null:** Grammar's resolution boundary is below the 梅花 date formula. The system is algebraically coherent but empirically inert.

---

## DONE

### 8a: Internal Consistency of Worked Examples ✓

**Result:** 10/10 examples fully consistent. Every example passes all 5 mechanical checks (arithmetic, hexagram identity, 互, 變, 体用 assignment). Gate passed.

**Derived findings:**
- 8a.1: 192/384 parity constraint applies to date formula only; other 先天 methods break parity lock
- 8a.2: 6 stable_neutral states = kernel of 五行 map on even-parity fiber = RG attractor + predecessors
- 8a.3: Practitioner process separates into position selection (mechanizable) and semantic interpretation (requires context)
- 8a.4: When 五行 saturates (all-比和), system falls through to Z₂ counting
- 8a.5: 象 imagery reinforces but never contradicts the 五行 signal (N=10, pedagogical)

See `probe_8a_results.md` for full verification.

---

### 8c: 體用 Decision Rules as Formal Grammar ✓

**Result:** 4+1 invariant structure. Four relations domain-invariant, 体克用 is the single free parameter with three modes (competition/manifestation/nurture).

**Key findings:**
- 8c.1: 4+1 structure — 用克体 always −, 体生用 always −, 用生体 always +, 比和 always +, 体克用 domain-dependent
- 8c.2: 生 is context-free (creator depletes regardless), 克 is context-dependent (destroyer's welfare depends on target) → maps to dynamics valve
- 8c.3: 4-layer override hierarchy (base template → domain mode → external omens → 体用 abandonment)
- 8c.4: Adversarial-first ordering REFUTED for templates (was narrative exposition artifact)
- 8c.5: 0/17 domains reference hexagram names — naming is practitioner lore, not system architecture
- 8c.6: 天時 (weather) is a structurally different system — frequency model vs relational model
- 8c.7: 象 tables are vocabulary (lexicon), not protocol (deterministic lookup)

See `probe_8c_results.md` for full 18-domain table.

---

### 8c-ext: Arc Symmetry Under Domain Templates ✓

**Result:** Complement-Z₅ involution generates R=B invariance at the interpretation level — same algebraic structure as the dynamics valve.

**Key findings:**
- 8c-ext.1: R=B (rescued=betrayed) is INVARIANT under all valence templates — theorem of complement involution σ
- 8c-ext.2: I=D (improving=deteriorating) holds only under competition; breaks under manifestation/nurture
- 8c-ext.3: Competition template is the unique favorable maximum; domain specialization can only narrow the favorable space
- 8c-ext.4: All 6 stable_neutral states survive under every template (absolute)
- 8c-ext.5: Arc reclassification scales with template distance: 32% (manifestation), 47% (nurture), 72% (nurture-full)

See `probe_8c_ext_results.md`.

---

### 8c-ext2: Symmetry Theorem ✓

**Result:** Three-tier symmetry theorem proven empirically across 16 alphabets.

**Key findings:**
- 8c-ext2.1: R=B holds for any positive (a,b); I=D holds iff alphabet is symmetric; stable_neutral invariance is absolute
- 8c-ext2.2: Two I=D counts: 34 (a=b) and 52 (a≠b), gap = 18 boundary states
- 8c-ext2.3: I=D breaks exactly at V(体克用) ≤ 0 — the manifestation boundary
- 8c-ext2.4: Competition template is simultaneously maximum-symmetry and maximum-favorability — unique structural optimum
- 8c-ext2.5: R=B count = 56 absolutely invariant, from Z₅ QR structure × bit-flip geometry × {2,2,2,1,1} partition
- 8c-ext2.6: Complement-Z₅ unifies dynamics (valve), interpretation (R=B), and combinatorics (count=56) — three levels, one algebraic fact

See `probe_8c_ext2_results.md`.

---

### 8b: 皇極經世 Event Catalogue ✓ (NULL)

**Result:** 1111 events parsed from vol 6. All tests return null (p=0.42–0.91). Event character is completely independent of position in the 10-year stem cycle. The canonical 五行 ordering is not special among all 120 permutations.

**Key findings:**
- 8b.1: 1111 events extracted, 天干 distribution perfectly uniform (132/stem), no selection bias by cycle position
- 8b.2: Consecutive 天干 produce only 比和 and 生, never 克 — the 天干 cycle IS the 生 cycle. E2/E3 structurally untestable at year resolution.
- 8b.3: All statistical tests null (χ²=1.96–4.05, p=0.42–0.91, Cramér's V < 0.064)
- 8b.4: 120-permutation control — all permutations produce identical χ², no ordering is special
- 8b.5: Z₅ orbit invariance proven — 12/60 relation uniformity forced by group theory, independent of 地支→五行 distribution
- 8b.6: Approach B blocked — only 0.9% of entries mention months

**Resolution boundary established:** The grammar requires relational input (体+用) at finer-than-year temporal resolution. Year-level 天干 gives one element, not a relation.

See `probe_8b_test_results.md`, `hjjs_events.json`.

---

### 8d: Seasonal Modulation ✓ (BLOCKED)

**Result:** Blocked by 8b null. No year-level signal to modulate. Requires finer temporal resolution data.

---

### 8e: 納甲 Under Complement-Z₅ ✓

**Result:** Complement-Z₅ holds at trigram-element level (梅花) but FAILS at line-element level (火珠林 納甲). Clean structural boundary between the two systems.

**Key findings:**
- 8e.1: σ produces 4 different Z₅ shifts {0,1,3,4} across complement pairs. Only 2/32 hexagram pairs have uniform 6-line shift.
- 8e.2: Root cause — 地支→五行 has non-uniform fibers ({4,2,2,2,2}). Arithmetic in Z₁₂ becomes non-arithmetic in Z₅ after projection.
- 8e.3: 艮↔兌 is the unique fully consistent pair — coincidence of starting offsets, not structural.
- 8e.4: 24 alternative start tables achieve full consistency, none includes historical values. System not designed for complement consistency at branch level.
- 8e.5: Corrected 京氏 rule makes consistency worse (3/8 → 2/8).
- 8e.6: 納甲 is not a group homomorphism. It's affine in Z₁₂ then non-linear projection to Z₅.

See `probe_8e_results.md`.

---

### 7a: Kernel Hexagrams in the Semantic Manifold ✓

**Result:** The 4 algebraic kernel hexagrams (Earth/Metal pairs where bit-flip preserves element) are completely depleted of standalone 吉 in the 爻辞 (0/24 vs 106/360, p=0.0006). Effect is a threshold at the 變卦 level, not a gradient.

**Key findings:**
- 7a.1: Kernel hexagrams are individually center-ward in semantic space (z=−1.52) but NOT mutually clustered (p=0.455)
- 7a.2: Standalone 吉 absent (0/24, p=0.0006). All other valence markers at baseline rates — including 元吉, 利, 无咎, 凶.
- 7a.3: Threshold, not gradient — 2 Wood hexagrams with main+互=比和 but no 變=比和 lines have baseline 吉 rates (0.167). The discriminant is bit-flip geometry from 8a.3.
- 7a.4: The single 吉 near the kernel is 坤 L5 黃裳元吉 — superlative form, not standalone.

**Cross-temporal correspondence:** The algebraic kernel (梅花, ~1000 CE) picks out hexagrams whose original texts (~1000 BCE) independently encode diagnostic silence through 吉-withdrawal. Local exception to the 89%/11% global independence.

See `probe_7a_results.md`.
