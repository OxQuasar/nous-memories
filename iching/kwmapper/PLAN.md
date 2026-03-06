# KW Mapper — Spatial Mapping of Inner Hexagram Space

## Goal

Visualize the KW sequence walk through the 16-node inner hexagram (互) space, with five-phase (生/克) relations, basin structure, and kernel properties overlaid spatially.

## The space

The inner 4 bits (bits 1-4 of the hexagram) determine 互. 16 possible values. Each is a pair of overlapping trigrams: 互_lower = (h₁, h₂, h₃), 互_upper = (h₂, h₃, h₄). The shared interface (h₂, h₃) determines basin.

Natural coordinates:
- **4-bit hypercube** projected to 2D (the inner bits form a 4D binary space)
- **Basin partition** as spatial regions: 坤 (00), 坎離 (01/10), 乾 (11) on the interface axis

## Scripts

### `01_hypercube.py` — The 4-bit hypercube with KW walk

**Layout:** Basin-natural coordinates:
- Horizontal axis: interface bits (h₂, h₃) → basin (3 columns: 00, mixed, 11)
- Vertical axis: wing bits (h₁, h₄) → 4 rows within each basin
- This gives a 3-column × 4-row grid, basin-partitioned by construction

**Content:**
- 16 nodes colored by basin (○=blue, ◎=green, ●=red)
- Node labels: 互 trigram pair name + inner 4-bit value
- KW walk traced as directed edges (63 steps)
- Edge color: five-phase relation on 互 lower (生=green, 克=red, 比=gray)
- Edge style: intra-pair (solid) vs inter-pair (dashed)
- 互 iteration arrows (convergence to attractors) as a second layer

**Output:** PNG + SVG

### `02_fivephase_flow.py` — Five-phase flow map on inner space

**Layout:** Same 16-node layout as 01.

**Content:**
- For ALL 64×64 pairs (not just consecutive), compute 互-lower and 互-upper five-phase relations
- Draw the **五行 flow field**: for each inner-value node, aggregate incoming/outgoing 生 and 克 edges
- Color each node by net five-phase balance: net 生 = green, net 克 = red
- Show the dominant flow direction (which basin generates, which destroys)
- Overlay the KW walk to show how it navigates the flow field

**Output:** PNG + SVG

### `03_kernel_map.py` — Kernel components on inner space

**Layout:** Same 16-node layout.

**Content:**
- For each KW consecutive transition, mark the kernel type on the edge
- Color edges by kernel: H-kernels (blue), non-H (orange)
- Specifically highlight I-component: I=0 (thin) vs I=1 (thick)
- Show how the I component maps onto the 生/克 boundary (from script 20 finding)

**Output:** PNG + SVG

### `04_walk_animation.py` — Step-by-step KW walk (not yet built)

**Layout:** Same 16-node layout.

**Content:**
- Generate 64 frames showing the KW walk progressing one step at a time
- Current position highlighted, trail fading
- Basin breathing visible as the walk moves through the three columns
- Frame annotation: hex name, pair number, basin, 互 value, five-phase

**Output:** Series of PNGs or animated GIF

### `05_dual_map.py` — Outer vs inner space side by side

**Layout:** Two panels:
- Left: 8-node trigram-pair space (outer hexagram as lower×upper trigram)
- Right: 16-node inner space (互)

**Content:**
- Same KW walk on both spaces simultaneously
- Shows how the outer walk (fast, free) and inner walk (constrained, five-phase-structured) diverge
- Edge colors: five-phase on each respective space
- Demonstrates the decoupling: outer five-phase is uniform, inner five-phase is structured

**Output:** PNG + SVG

## Shared infrastructure

### `common.py` — Shared layout and data
- 16-node inner-space layout function (basin-natural coordinates)
- 8-node outer trigram-pair space layout
- KW sequence data loading
- Five-phase computation helpers
- Color maps for basin, five-phase, kernel
- Standard figure setup (size, fonts, style)

## Execution order

1. `common.py` (shared code)
2. `01_hypercube.py` (core map — validates layout)
3. `02_fivephase_flow.py` (overlay 生/克)
4. `03_kernel_map.py` (overlay kernel/I-component)
5. `05_dual_map.py` (outer vs inner comparison)
6. `04_walk_animation.py` (optional, if static maps warrant it)

## Dependencies

- matplotlib (just installed)
- networkx (available)
- numpy, scipy (available)
- cycle_algebra.py, sequence.py (existing infrastructure)
