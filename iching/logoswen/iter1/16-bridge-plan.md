# 16. Bridge Structure Deep Investigation — Research Plan

> The bridge analysis (15) revealed that inter-pair transitions break the generator algebra, form a sparse asymmetric directed graph over orbits, and use 23 unique non-generator masks. There is more structure here than we've extracted. This plan targets the remaining seams.

All research up to this point found in kingwen/

---

## Thread 1: Bridge Mask Generator Basis

**Question:** Do the 23 non-standard bridge masks form their own algebraic structure?

The standard pairs live in Z₂³ (8 masks from 3 generators). Bridges use 23 distinct masks from 31 possible — more variety, but still far fewer than the 63 non-identity elements of Z₂⁶. What subspace do they span? Is there a minimal generating set? What's the rank of the bridge mask matrix over GF(2)?

**Method:**
- Stack all 31 bridge XOR masks as rows of a 31×6 binary matrix
- Compute rank over GF(2) — this tells us the dimension of the subspace bridges can reach
- Find a minimal basis (row-reduce)
- Check: do the 23 unique masks form a subgroup, coset, or linear code?
- Compare to the standard generator subspace {O, M, I}

**Expected output:** The dimension and basis of bridge mask space, and whether it has algebraic closure properties.

---

## Thread 2: Bridge-to-Orbit Projection

**Question:** Can we predict the orbit transition from the bridge mask?

Each bridge mask is a 6-bit XOR. Each orbit transition is a 3-bit signature change. The projection from 6-bit mask to 3-bit signature change should be computable — but is it a function? (Same mask → same orbit change?) Or does it depend on the starting hexagram?

**Method:**
- For each bridge, compute both the 6-bit mask and the 3-bit signature change
- Group by mask: do identical masks always produce the same orbit change?
- If yes: find the projection formula (likely involves the signature's own structure)
- If no: characterize when the same mask produces different orbit changes — what determines it?

**Expected output:** Whether bridge mask determines orbit transition, and the projection rule if it exists.

---

## Thread 3: Pair+Bridge Compound Units

**Question:** What happens when we treat (standard pair, bridge, next standard pair) as a compound transition?

The sequence alternates: pair mask (algebraic), bridge mask (free), pair mask (algebraic), ... The compound unit is the pair+bridge composition. What's the algebra of these compound moves?

**Method:**
- For each position k, compute: pair_k mask, bridge_k mask, pair_{k+1} mask
- Compute the compound: pair_k ⊕ bridge_k (XOR composition in Z₂⁶)
- Also compute the full 3-step: pair_k ⊕ bridge_k ⊕ pair_{k+1}
- Check: does the compound have generator structure? Simpler than bridges alone?
- Look at the 4-hexagram path: hex_{2k} → hex_{2k+1} → hex_{2k+2} → hex_{2k+3}

**Expected output:** Whether compound transitions recover algebraic structure that bridges alone lack.

---

## Thread 4: Why These Specific Masks?

**Question:** The King Wen sequence has freedom in choosing bridge masks (they're not generator-determined). What constrains the choices it actually makes?

29/31 bridges are non-standard, but they're not random either (23 unique from 63 possible). Something selects these specific masks. Candidate constraints:
- Hamming distance minimization (bridges are gentler than pairs)
- Orbit transition requirements (the orbit graph is sparse — maybe few masks achieve the needed transitions)
- Line-level patterns (which specific lines change at bridges?)
- Trigram-level constraints (do bridges preserve or break trigram structure?)

**Method:**
- For each orbit transition that occurs, enumerate ALL masks that could achieve it from the specific starting hexagram
- Compare actual mask to the set of possible masks — is it minimal Hamming? Random? Structured?
- Analyze which lines (1-6) are flipped at each bridge — is there a positional bias?
- Check trigram (upper/lower) preservation: how often does a bridge change 0, 1, 2, 3 lines per trigram?

**Expected output:** The constraint(s) that explain why these specific masks were chosen from the available options.

---

## Thread 5: Directed Graph Cycles

**Question:** The orbit transition graph has 20 directed edges across 8 nodes with near-uniform degree. What is its cycle structure?

**Method:**
- Build the weighted directed graph explicitly
- Find all simple cycles (the graph is small enough for exhaustive enumeration)
- Check for Eulerian path/circuit (does one exist given the degree sequence?)
- Compute strongly connected components
- Check: does the actual King Wen bridge sequence trace a specific path through this graph? Is it Hamiltonian? Does it visit edges in a systematic order?
- Analyze the 31-step walk: which edges are used once vs multiple times?

**Expected output:** The cycle structure, whether an Eulerian/Hamiltonian path exists, and how the actual sequence relates to the graph's topology.

---

## Thread 6: Single-Bit Bridges

**Question:** Two bridges have Hamming distance 1 (single line change). These are the minimal possible transitions. What makes them special?

Only 2 of 31 bridges change a single bit. In a 6-dimensional space, single-bit moves are the edges of the hypercube — the most local possible change. These are structurally privileged.

**Method:**
- Identify the two single-bit bridges: which hexagrams, which line, which orbit transition
- What's special about these positions in the sequence? Are they near structural boundaries?
- The single bit that changes — is it a "tension" line (part of the signature) or a "harmony" line?
- Compare to the 13 Hamming-3 bridges (the mode): is there a continuum from minimal to maximal bridge change?

**Expected output:** The identity and structural role of the two minimal bridges, and the full Hamming-distance spectrum's relationship to sequence position.

---

## Thread 7: Synthesis

Synthesize research up to this point, ask and explore questions on unresolved points. Determine whether more threads are appropriate for further exploration. If so, create a new research document plan and repeat. 


## Execution Order

Threads 1-2 are foundational (algebraic structure). Thread 3 builds on 1-2. Thread 4 is independent but benefits from 1-2. Threads 5-6 are independent.

**Round 1 (parallel):** Threads 1+2 (algebraic) and Threads 5+6 (graph + special cases)
**Round 2 (parallel):** Threads 3+4 (compound structure + constraint analysis), informed by Round 1
**Synthesis:** Captain + sage discuss cross-thread implications
