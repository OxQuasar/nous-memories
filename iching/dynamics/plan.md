# Fingerprint Investigation — Plan

## Objective

Given the measured structural fingerprint of the I Ching's transition graph (R257–R269), identify what class of dynamical system it corresponds to. The questions are in `fingerprint.md`.

## Approach

**Literature-first.** The fingerprint elements (Chebyshev spectral spacing, Fibonacci walk counts, irreversible type flow, mean-isometric contraction, coherent sector φ survival) each appear in known systems. The investigation should find those systems, compare quantitatively, and determine whether the combination narrows to a specific class.

**Computation supports literature.** When a candidate system is identified from the literature, verify the match computationally against the transition graph data (in `p1_results.json` through `p8_results.json`).

## Probes

### Probe A: Golden mean shift (F2)

The 克 subgraph has topological entropy log φ at the trigram level. The golden mean shift (shift of finite type forbidding "11") also has entropy log φ. This is the most concrete identification to test.

**Do:**
- Compute the topological entropy of each 五行 subgraph at both trigram and hexagram levels
- Characterize the forbidden words (if any) of each subgraph
- Compare the 克 subgraph to the golden mean shift: same entropy, but is the symbolic dynamics equivalent?
- Literature: where does the golden mean shift appear in physical and dynamical systems?

### Probe B: 互 as renormalization (F7)

The sharpest question. The 互 map has RG-like properties: coarse-grains (64→4), preserves mean distance, has fixed points, the bit weights [0,1,2,2,1,0] resemble a decimation kernel.

**Do:**
- Test formal RG properties: semigroup (does hu∘hu = hu? — yes, on the attractor), scale reduction, what quantity is preserved or monotone?
- Compute entropy of the 64-state distribution under iterated 互: does it decrease monotonically? (analog of c-theorem / entropy monotonicity)
- Compare the bit weights to known block-spin / decimation schemes
- Literature: real-space renormalization on the hypercube, Kadanoff blocking, wavelet-based RG

### Probe C: Chebyshev spacing (F1)

Is the Chebyshev spacing of {1, √2, φ} generic to consecutive path graphs, or specific to {P₂, P₃, P₄}?

**Do:**
- Compute spectral radii of P_n for n = 2..10. Check whether any consecutive triple gives Chebyshev spacing
- Literature: where does Chebyshev spacing of eigenvalues appear in transfer matrix physics, coupled oscillators, or multi-scale dynamical systems?
- If generic: this is stage-level, not interesting. If specific to {2,3,4}: something selects these particular scales

### Probe D: Irreversibility and the chosen assignment (F3)

The valve is drama (1/6 contingent). The traditional assignment chose irreversibility.

**Do:**
- Characterize all 6 valid assignments: which have valves, which direction, which hinge content?
- Literature: irreversible transition networks in chemical kinetics, ecological succession, economic regime switching
- The question "why choose the assignment with the arrow of time?" is interpretive but the structural comparison (how does the chosen assignment differ from the other 5?) is computational

### Probe E: Combined signature (F6)

After Probes A-D, attempt the synthesis: does the combination narrow to a class?

**Do:**
- Cross-reference: what systems appear in multiple probe results?
- If RG identification holds (Probe B) and golden mean shift holds (Probe A): is there a known RG for the golden mean shift?
- If Chebyshev spacing is specific (Probe C): what physical constraint produces it?

### Probe F+: Captain's Discretion

Follow threads where they lead. 


## Priorities

The captain should structure iterations around these probes but follow whatever connections emerge between them. The probes are a starting frame, not a checklist.

## What to avoid

- Do not test fingerprint elements against the semantic manifold (the three-level null already established independence)
- Do not reframe the questions as embedding analysis
- Do not close a question because one candidate system doesn't match — the fingerprint may correspond to a class not yet checked

