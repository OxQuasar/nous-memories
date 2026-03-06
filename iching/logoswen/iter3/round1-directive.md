# Round 1 Directive — Threads A+B and C (Parallel)

## Problem Space

Layer 4 of the King Wen sequence: pair orientation — which hexagram comes first within each of the 32 pairs. This is 2³² ≈ 4 × 10⁹ degrees of freedom, the last unanalyzed structural layer.

Prior layers are settled:
- Layer 1 (orbit-consistent pairing): eliminates ~44 orders of magnitude
- Layer 2 (mask = signature identity, p ≈ 10⁻¹⁷): the pairing rule
- Layer 3 (pair ordering, p ≈ 10⁻³): S=2 avoidance + kernel diversity
- Layer 4 (pair orientation): **open**

The central question: is there a selection principle at this layer, or is the orientation arbitrary given the constraints above?

## Round 1 Structure

Two agents work in parallel on complementary foundations:

**Analyst (Threads A+B):** Census the orientation in multiple frames and test the traditional rule. The goal is to characterize the 32-bit orientation string and determine whether a single structural rule recovers KW's choices.

**Structuralist (Thread C):** How does orientation interact with bridge structure? Orientation determines which hexagram exits each pair and which enters the next — changing the bridge mask. The key question is how much of the orientation is *forced* by S=2 avoidance, and how the kernel chain depends on orientation.

These two threads are independent — A+B characterizes the orientation itself, C characterizes its interaction with the bridge layer. Their findings converge at the gate decision.

## Gate Decision (After Round 1)

After Round 1 completes, the findings determine how Round 2 proceeds:

1. **If Thread B finds a clean structural rule** → Threads D-F shift from open exploration to testing/extending that rule
2. **If Thread C shows orientation is almost entirely forced by S=2 avoidance** → the effective degrees of freedom shrink dramatically, and Thread G focuses on the residual
3. **If both produce null results** → Round 2 proceeds as planned (D, E, F open exploration)

The key number from Thread C: what fraction of 2³² orientations are S=2-free? This determines whether orientation is a genuine design choice or mostly constrained.

## Code Infrastructure

- `kingwen/sequence.py`: base data (KING_WEN list, bits(), name(), trigram functions)
- `kingwen/pairs.py`: pair computation 
- `kingwen/bridges.py`: bridge computation, MASK_NAMES, GEN_BITS, xor_sig()
- `logoswen/iter2/analysis_utils.py`: shared utilities (VALID_MASKS, analyze_sequence(), orbit lookups)
- Scripts go to `logoswen/iter3/`
- Findings go to `logoswen/iter3/census_findings.md` and `logoswen/iter3/bridge_orientation_findings.md`
