# Atlas — Complete 五行 Map of Hexagram Space

## Purpose

A comprehensive structural map between hexagram space (Z₂⁶) and 五行 space (Z₅), covering all projections, their joint constraints, temporal modulation, transformation behavior, and textual semantics. The reference document against which all interpretive questions can be indexed.

## Dependencies

- opposition-theory/phase4/cycle_algebra.py — trigram/hexagram primitives, 互
- huozhulin/01_najia_map.py — 納甲, BRANCH_ELEMENT
- huozhulin/02_palace_kernel.py — palace generation, basin, kernel, depth
- huozhulin/03_liuqin.py — 六親 computation
- wuxing/ — 五行 trigram assignment, 生克 cycle
- synthesis/ — embeddings, valence data, 體/用 findings
- jingshiyizhuan/ — 納音, 京氏 temporal layers
- spaceprobe/ — 互 convergence, basin/kernel definitions, attractors, 梅花 體/用 framework

---

## I. The Static Map

The time-independent 五行 profile of each hexagram. Every hexagram has coordinates in multiple Z₅-derived spaces simultaneously.

### A. Per-hexagram coordinates

**Surface (shell projection, Z₂³ × Z₂³ → Z₅ × Z₅):**
- Upper trigram element
- Lower trigram element
- Directed 生克 relation between them

**Depth (core projection, inner 4 bits → Z₂³ × Z₂³ → Z₅ × Z₅):**
- 互上 trigram element
- 互下 trigram element
- Directed relation between 互 trigrams
- Iterated: 互互 elements, 互互互... → attractor

**Reference frame (palace system):**
- Palace element
- 六親 word (6 positions × 5 types)
- Rank, 世應 positions

**Structural (binary invariants):**
- Basin (Kun/Qian/Cycle)
- Kernel (O,M,I)
- Depth to attractor
- Parity (b₀⊕b₁) per trigram

**納音 (second 五行 layer, from 60-甲子):**
- 納音 element per line (6 values ∈ Z₅, distinct from branch elements)
- 納音 names (海中金, 劍鋒金, etc.)
- Relationship of 納音 elements to branch elements: agreement/disagreement pattern

### B. The Z₅ × Z₅ meta-space

The 25-cell element-pair space. Each hexagram maps to a cell at surface level and a (potentially different) cell at depth level.

- 生克 network on Z₅ × Z₅: how do the 25 cells relate through generation/overcoming?
- Cell populations: how many hexagrams land in each cell (surface)? Each cell (depth)?
- Diagonal cells (比和) vs off-diagonal: structural properties
- The complement anti-automorphism acting on Z₅ × Z₅

### C. Joint constraints and information content

- Full MI matrix across all coordinates
- Forbidden combinations: which (surface relation, depth relation) pairs can/can't coexist
- Which minimal coordinate set uniquely identifies each hexagram?
- H(hexagram | full 五行 profile) = ? The residual ambiguity
- The 1.50-bit gap: 五行 carries ~4.50 bits, Z₂⁶ has 6. What lives in the residual?
- Which hexagrams are 五行-indistinguishable? What distinguishes them beyond 五行?
- Constraint graph: which coordinates determine which others

---

## II. Transformations

How the 五行 profile changes under the system's fundamental operations.

### A. 互 transition (depth peeling)

互 as a map on Z₅ × Z₅ (element-pair space):
- Full transition table: (surface pair) → (depth pair) → (depth² pair) → attractor
- Fixed points in Z₅ × Z₅ = attractors
- Orbits under iterated 互: correspondence to basins
- Anti-phase breathing: at consecutive steps, does 生/克 alternate between upper and lower nuclear? Verify across all 64.
- Is 互 on Z₅ × Z₅ well-defined (depends only on element pair) or does it require information beyond the pair?
- Algebraic characterization: group action? contraction? what structure?

### B. 變 fan (single-bit perturbation)

For each hexagram × each of 6 動爻 positions:
- 體/用 assignment (which trigram is 體, which is 用)
- 體/用 五行 relation
- Change in surface element pair
- Change in basin, kernel, depth
- The 6-neighborhood in Z₅ × Z₅: where does each single-bit flip send you?

Structural questions:
- Which line positions preserve 生/克 category? Which break it?
- Lines 2-5 (nuclear, core bits) vs lines 1,6 (outer, shell bits): different 五行 impact?
- The 變 fan as local geometry of hexagram space in 五行 coordinates

### C. Palace walk (shell traversal)

For each of 8 palaces, rank 0→7:
- Element pair trajectory
- 互 element pair trajectory
- 六親 word evolution
- Basin/kernel transitions
- 游魂 (rank 6) and 歸魂 (rank 7) reversions in 五行 terms
- Isomorphism question: do all 8 palaces have the same walk pattern up to Z₅ rotation?

### D. S₄ involutions on the full profile

How complement, reverse, and rev∘comp transform the *complete* 五行 profile:
- Surface element pair transformation (known: complement = anti-automorphism)
- Depth element pair transformation
- Palace/六親 transformation
- Basin/kernel transformation
- Which coordinates are invariant under each involution?
- Which coordinates swap?
- The full transformation table: involution × coordinate → effect

### E. Cross-hexagram network

The graph structure of hexagram space in 五行 coordinates:
- 互 graph: who maps to whom under 互 (64 nodes, 64 edges, directed)
- Complement pairs in Z₅ × Z₅: where do they land?
- Reverse pairs in Z₅ × Z₅: where do they land?
- Hexagrams sharing the same 五行 profile: equivalence classes
- Hexagrams sharing the same 六親 word: the 59 singletons + collisions
- The 變 neighborhood graph: 64 nodes, each with 6 edges (single-bit flips), colored by 五行 relation change

---

## III. Temporal Overlay

The time-dependent modulation of the static map. How the presheaf structure acts on the 五行 coordinates.

### A. Seasonal window on Z₅

- 旺相休囚死 as width-2 sliding window on the 5-ring
- For each season: which cells of Z₅ × Z₅ are fully active, partially active, dark?
- The F_total = 12 conservation law: derivation from atlas coordinates
- Seasonal trajectory: as the window rotates through 5 seasons, how does the visible portion of Z₅ × Z₅ change?

### B. 日辰 extension

- 日辰 as Z₁₂ branch-level modulation: 沖/合/生 on individual lines
- The 4/5 ceiling theorem: derivation from Z₅ geometry
- Joint (season × day) coverage: the 60 (season, day-branch) states mapped onto Z₅ × Z₅
- The excluded element at maximum coverage: 休 vs 死 alternation
- Fire/Water simultaneous access: the 16/60 resolution of Cycle basin conflict

### C. The presheaf on Z₅

- Base space: (season, 用神) ∈ Z₅ × Z₅
- Stalk: which lines are visible (present + strong + relevant)
- The orthogonality wall: 納甲-level stalks cannot see core coordinates
- n_zero distribution (16:32:16) derived from atlas
- The 1/5 residual shadow after 日辰: minimal aperture theorem

### D. 梅花 temporal input

- 先天起卦: time → hexagram via modular arithmetic
- Distribution of hexagrams across time slots: non-uniform (χ² = 481.8)
- Which Z₅ × Z₅ cells are reachable at which times?
- 梅花 inherits 2/5 ceiling (no 日辰 mechanism)
- Pipeline asymmetry: 梅花 curves domain (which hexagram), 火珠林 curves codomain (which aspects visible)

---

## IV. The Semantic Layer

How the 五行 map connects to textual meaning.

### A. Valence bridges (established)

- 凶 × basin (core channel): convergence → danger, p=0.0002
- 吉 × 生体 (shell channel): receiving generation → fortune, p=0.007
- Both encode process (flow direction), not state (element identity)
- Depth gradient: 凶 peaks at depth-1 (boundary layer, 36.1%)

### B. Thematic content by 五行 relation (uncharacterized)

For each of the 5 surface relations (比和/生体/体生用/克体/体克用):
- Dominant vocabulary and imagery in 卦辭 and 爻辭
- Thematic clustering beyond valence markers
- Do 生体 texts share nourishment/growth themes?
- Do 克体 texts share threat/pressure themes?
- Do 比和 texts share stasis/equilibrium themes?

At depth:
- Do 互 relation types predict thematic content of nuclear lines (2-5)?
- Do lines 1,6 (outer, shell) differ thematically from lines 2-5 (inner, core)?

### C. 納音 semantics

- The 納音 names (海中金 = sea-metal, 劍鋒金 = sword-metal, etc.) carry qualitative distinctions within elements
- Does 納音 name predict textual imagery? (e.g., 劍鋒金 → sharp, cutting imagery in 爻辭?)
- This is the finest-grained 五行 coordinate — 60 distinct values vs 5 elements

### D. The tradition's interpolation

- Where the 梅花 tradition's 體用 schema agrees with the texts (生体→吉)
- Where it distorts (symmetrization of directional signals, 比和→吉 not in texts)
- The process/state confusion: texts encode flow direction, frameworks encode categories

---

## V. Outputs

### Reference data
- `atlas.json` — complete 五行 profile for all 64 hexagrams. Pure algebra, no semantics. Structural coordinates only.
- `z5z5_cells.json` — the 25-cell meta-space: populations, basin distributions, 凶/吉 rates (measured, numeric). Thematic labels added *only if* probe IV.B finds significant clustering — no interpretive labels without p-values.
- `transitions.json` — 互, 變, palace walk, S₄ transition tables. Pure algebra.

### Findings
- Per-section findings documents
- Cross-section constraint analysis
- Updated open-questions.md with newly resolved/opened questions

### Visualizations (sketch — refine after results)
- **The torus.** Z₅ × Z₅ is topologically a torus (both axes cyclic). The primary visual: 64 hexagrams as points on the torus surface, colored by basin. 互 as contracting flow arrows toward 4 attractor points. 生 cycle runs one direction around the torus, 克 runs at a different angle. The seasonal window sweeps diagonally across the surface — the rotating shadow visible as the dark region that moves.
- Z₅ × Z₅ heatmaps (population, 凶 rate, 吉 rate per cell)
- 互 flow diagram on Z₅ × Z₅
- Palace walk trajectories
- 變 fan neighborhoods
- Presheaf per hexagram: 5×5 (season × 用神) grid with visible lines highlighted
