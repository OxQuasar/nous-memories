# I Ching Research — Captain's Log

## Key Files

- Research directory: `memories/iching/directory.md`
- Core texts: `memories/texts/iching/` (yaoci.json, guaci.json, tuan.json, xiangzhuan.json, xugua.json)
- Atlas: `memories/iching/atlas/atlas.json` — hex profiles, `kw_number`, `complement`, `reverse`, `lower_trigram`, `upper_trigram`, `basin`, `palace`, `surface_cell`
- Embeddings: `memories/iching/synthesis/embeddings.npz` (keys: guaci, yaoci, daxiang, tuan; yaoci = 384×1024 BGE-M3)
- Reversal investigation: `memories/iching/reversal/` — main research program
  - `findings.md` — canonical results document (R94–R180)
  - `questions.md` —  program summary
  - `exploration-log.md` — iteration-by-iteration log (19 iterations)
  - `resonance-tests.md` — T1/T2/T3 framework (all complete)
  - `Q1/` — computation scripts and cached embeddings (phases 1–8)
  - `Q2/` — axiom investigations including Q2 Proper
  - `Q2T2/`, `Q3/`, `T3/` — investigation phases
- East/West investigation: `memories/iching/eastwest/` — cyclotomic, KW sequence, torus coherence, dynamics, perturbation, cross-architecture replication
  - `findings.md` — canonical results document (R181–R214)
  - `exploration-log.md` — iteration-by-iteration log (12 iterations, R181–R214)
  - `questions.md` 
  - Scripts: `cyclotomic_probe.py`, `kw_sequence_probe.py`, `torus_coherence.py`, `differentiation_principle.py`, `hu_cell_validation.py`, `dynamics_probe.py`, `edge_type_decomposition.py`, `perturbation_directions.py`, `sikuroberta_replication.py`, `pair_concordance.py`
- Fibonacci / opposition manifold investigation: `memories/iching/fibo/` — Fibonacci alignment, opposition space probes, cross-layer geometry, independence tests
  - `findings.md` — canonical results document (R215–R237)
  - `questions.md` — Fibonacci open questions 
  - `exploration-log.md` — iteration log (8 iterations: Fibonacci + semantic probes + cross-layer + position-resolved + Hamming-length + unification + d=2/reversal + trigram decomposition)
  - `fibo_probe.py`, `semantic_probes.py`, `artifact_check.py`, `cross_layer_opposition.py`, `position_resolved.py`, `hamming_length.py`, `unification_test.py`, `reversal_and_d2_retest.py`, `trigram_d2_decomposition.py`, `rank_bimodality.py` — computation scripts
