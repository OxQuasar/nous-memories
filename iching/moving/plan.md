# Moving Lines — Single-Line Flip Textual Impact Study

## Idea

Take a hexagram. Flip one line. Compare the texts of the original and transformed hexagram via embeddings. Measure semantic distance at both line-level and hexagram-level. Test whether the algebra predicts which flips produce the largest semantic shifts.

## Why this matters

The axis-type theorem says the three bit positions are NOT interchangeable:
- **b₁ (middle line, positions 2 and 5):** pure-克 — every Z₅ transition across this axis is destructive
- **b₂ (top line, positions 3 and 6):** 克-free — transitions are 比和 or 生 only
- **b₀ (bottom line, positions 1 and 4):** mixed — 2克 + 2生

If this structure is reflected in the classical texts, then flipping the middle line should produce systematically larger semantic shifts than flipping the top line. This tests the algebra against the tradition's own words — no external data needed.

## Data

### Pre-computed pair table
`atlas-mh/mh_states.json` — 384 entries (64 hexagrams × 6 lines). Each entry has:
- `hex_val`, `line` → original hexagram and moving line
- `bian_hex` → transformed hexagram
- `ben_relation`, `bian_relation` → Z₅ relation before/after
- `ben_bian_shift` → relation change category
- `ti_trigram`, `yong_trigram`, `bian_yong_trigram` → trigram values and elements

### Pre-computed embeddings
`synthesis/embeddings.npz` — BGE-M3 embeddings (1024-dim), same model used in semantic-map work:
- `guaci`: (64, 1024) — 卦辭 hexagram judgments
- `yaoci`: (384, 1024) — 爻辭 line texts, indexed as hex*6 + (line-1)
- `daxiang`: (64, 1024) — 大象 image commentary
- `tuan`: (64, 1024) — 彖傳 judgment commentary

### Raw texts
`texts/iching/` — guaci.json, yaoci.json, tuan.json, xiangzhuan.json

## Structural setup

### Hexagram encoding
Each hexagram = 6 bits. Lower trigram = bits 0-2, upper trigram = bits 3-5. Convention A: b₀=bottom.

### Single-line flip
Flipping line k (1-indexed from bottom) toggles bit (k-1). This changes exactly one trigram:
- Lines 1-3: lower trigram changes, upper stays
- Lines 4-6: upper trigram changes, lower stays

### Bit position → Z₅ transition type
From the axis-type theorem:
- **b₁ flip:** Always changes the Z₅ relation to/from 克. Every b₁ transition crosses the pure-克 axis.
- **b₂ flip:** Never introduces 克. The Z₅ relation changes but stays within {比和, 生}.
- **b₀ flip:** Mixed — sometimes introduces 克, sometimes doesn't.

## Measurement approach

### Layer 1: Line-level embedding comparison

For each of the 384 moving-line pairs (hexagram A, line k → hexagram B):
- Compare the 爻辭 embedding at position k in hexagram A vs position k in hexagram B
  - This is the **moving line's own text** — what does the tradition say about this specific line in each context?
  - `yaoci[A*6 + (k-1)]` vs `yaoci[B*6 + (k-1)]` → cosine distance
- Compare ALL 6 line embeddings pairwise between A and B
  - 6 cosine distances (line 1 vs line 1, line 2 vs line 2, ...)
  - Mean distance across all 6 lines = overall line-level disruption
  - The moving line's distance vs the other 5 = is the changed line textually special?

This gives per pair:
- `d_moving`: cosine distance of the moving line's text
- `d_mean_all`: mean cosine distance across all 6 corresponding line pairs
- `d_mean_other`: mean cosine distance of the 5 non-moving lines

### Layer 2: Hexagram-level embedding comparison

Concatenate all 6 爻辭 texts per hexagram into a single string and embed with BGE-M3. This produces 64 holistic embeddings where the model sees inter-line context (attention across all 6 lines). These are NOT linear combinations of the individual line embeddings — the model captures interactions.

- `d_hex`: cosine distance of concatenated 爻辭 embedding (primary hexagram-level metric)
- `d_guaci`: cosine distance of 卦辭 (secondary — different text, judgment only)
- `d_tuan`: cosine distance of 彖傳 (secondary — commentary)
- `d_daxiang`: cosine distance of 大象 (secondary — image commentary)

### Layer 3: Algebraic annotation

For each pair, record (mostly from mh_states.json, some derived):
- `bit_position`: b₀, b₁, or b₂ (from line number: lines 1,4→b₀; 2,5→b₁; 3,6→b₂)
- `trigram_changed`: lower (lines 1-3) or upper (lines 4-6)
- `z5_before`: ben_relation
- `z5_after`: bian_relation
- `z5_shift`: ben_bian_shift
- `ke_introduced`: did 克 appear where it wasn't before?
- `ke_removed`: did 克 disappear?
- `element_changed`: did the flipped trigram change its 五行 element?
- `basin_before`, `basin_after`: 互 attractor of each hexagram
- `basin_changed`: boolean

## Test design

### T1: Bit-position effect on semantic distance

Group 384 pairs by bit position (b₀, b₁, b₂ — 128 each). Compare distributions of each distance metric.


Run for each metric independently: d_moving, d_mean_all, d_hex, d_guaci, d_tuan, d_daxiang.

### T2: Z₅ transition type vs semantic distance

Group pairs by Z₅ shift type (比和→克, 生→克, 克→生, 比和→生, etc.). Compare semantic distances.


### T3: Directional semantic shift

Not just distance but direction. For pairs where 克 is introduced:
- Does the embedding move toward the "凶 region" of the space?
- Use the known bridge (凶×basin from semantic-map F7) as a reference direction.

For pairs where 克 is removed:
- Does the embedding move toward the "吉 region"?
- Use the known bridge (吉×生体) as reference.

This tests whether semantic shift direction, not just magnitude, aligns with the algebra.

### T4: Moving line vs bystander lines

For each pair, compare d_moving (the flipped line's text change) vs d_mean_other (the 5 untouched lines' text change).

**Question:** Does changing one line's identity mostly affect that line's text, or does it ripple across all 6 lines? If texts are composed line-independently, d_mean_other ≈ 0. If the hexagram is a holistic composition, all lines shift together.


### T5: Basin change effect

Split pairs by whether the 互 attractor changed. Does basin change predict larger semantic distance, controlling for bit position?

This connects to the known 凶×basin bridge — if basin change is the mechanism, we'd expect basin-changing flips to shift 凶-marker density.

### T6: Semantic Shift Similarities

Group by semantic shift similarities and see if there are notable algebraic similarities. 


## Execution order

1. **Generate concat-爻辭 embeddings.** Concatenate all 6 line texts per hexagram into one string. Embed with BGE-M3 → (64, 1024). Save to embeddings file.

2. **Load pair table + all embeddings.** Enrich mh_states with bit_position, basin info. Verify yaoci indexing (hex*6 + line-1).

3. **Compute all distances.** For each of 384 pairs: d_moving, d_mean_all, d_mean_other, d_hex, d_guaci, d_tuan, d_daxiang. Store as enriched table.

4. Run Tests.


## Sources

- `atlas-mh/mh_states.json` — 384 moving-line pairs (pre-computed)
- `synthesis/embeddings.npz` — BGE-M3 embeddings: guaci(64,1024), yaoci(384,1024), daxiang(64,1024), tuan(64,1024)
- `moving/yaoci_concat_embeddings.npz` — to be generated: concatenated 爻辭 embeddings (64,1024)
- `texts/iching/` — raw text JSONs (guaci, yaoci, tuan, xiangzhuan)
- `semantic-map/findings.md` — known bridges (凶×basin, 吉×生体), marker families, 89% residual
- `unification/synthesis-3.md` — axis-type theorem proof
- `wuxing/summary_findings.md` — five-phase assignment
