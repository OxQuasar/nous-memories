# I Ching Research Summary

## What was found

The I Ching's algebraic structure is the unique instantiation of the (3,5) complement-respecting surjection. PG(2,F₂) decorated with one compass. 52 results proven or verified across 5 workflows (atlas, mh-atlas, deep, unification, semantic-map). Zero contradictions. 0.5 bits genuine freedom.

The texts and the algebra are independent systems sharing a narrow interface: two distributional bridges (凶×basin, 吉×生体), both surviving position control, operating through different algebraic projections. 89% of textual content is orthogonal to algebra. The commentary tradition sees primes 2 and 3 but not 5.

---

## Established results (52 items — full list in deep/open-questions.md)

### The structure (atlas + deep + unification)

- **Zero residual:** 13 五行 coordinates jointly identify every hexagram uniquely. H(hexagram | full profile) = 0.0 bits.
- **Zero free parameters:** The 0.50-bit cosmological choice is forced by conjunction of textual bridge + cycle attractor semantics (R32). The full selection chain: 240 surjections → 2 (R47).
- **{2,2,2,1,1} is the sole organizing principle.** Three doubleton elements, two singletons (Water/Fire). The partition is forced by pigeonhole at (3,5).
- **The torus is the frame, the Z₅ quotient is the picture.** Z₅×Z₅ is lossy (variable resolution), 互 not well-defined on it (17/25 multi-valued). Valence lives on the Z₅ diagonal — relation type, not position (R21).
- **Two bridges connect text to algebra:** 凶×basin (core projection, OR=4.25, p=0.00002) and 吉×生体 (shell projection, OR=2.19, p=0.004). Both encode process not state. Bridge orthogonality proven at perturbation level (R16).
- **Only two reading methods exist:** Shell (3+3 trigram split = 梅花) and core (1+4+1 nuclear overlap = 火珠林). Proven as the only two primitive projections on Z₂⁶ (R5).

### The geometry (unification)

- **PG(2,F₂):** Three lines through complement (H, P, Q) carry the three coprime pairings. P+Q+H = 8 theorem.
- **互 is a shear:** One term (ī leaks into i) creates all dynamical richness. Rank 6→4→2. P→H parity rotation → 克 amplification 1.538×.
- **KW pairing = orbit class** (theorem). 先天 = Fano triangle walk, unique via b₀ constancy (predictive test — not input).
- **Eigenstructure:** Spectral gap 0.71, stationary π(同+克+被克) = 89%. Zero flow from stride-2 to stride-1. P-coset alignment exact: F(同)=1, F(克)=1/13.
- **先天→後天** = H↔Q redistribution with P as pivot. Preserves only Q-axis {坎,離}. Not a dihedral element.

### The 梅花 atlas (384 states)

- **8 arc types** with perfect symmetry (rescued/betrayed 56/56, improving/deteriorating 52/52).
- **先天 parity wall:** 192/384 reachable, biased toward favorable arcs (OR=5.23).
- **体互 adversarial:** 63% 克-dominant. Informationally calibrated — favorable signals at 体互 are rare, therefore high-information.
- **Two independent channels:** Text (爻辭, present state) vs arc (體/用 trajectory). 先天 drops text channel. 後天 uses both.
- **18 domains, one engine:** All use identical 生克 evaluation. Domain selects semantic binding + imagery overlay.

### The texts (semantic map)

- **89% residual thickness.** Texts have rich independent structure organized by position, not algebra.
- **Positional dominance:** k=3 clusters separate by line position (χ²=37.2, p=0.0001), not by hexagram.
- **小象 encodes 3-layer hierarchy:** χ²=125, p=5×10⁻²⁶. Three vocabulary groups match the three algebraic layers.
- **Commentary is non-algebraic:** 大象 imagistic (zero 五行 vocabulary). 彖傳 binary-structural (Z₂ register). 小象 positional only.
- **彖傳 does anomaly detection:** Comments on the unusual (Kun basin has highest 剛/柔 ratio), not the dominant.

---

## Open questions

### About the I Ching specifically

**Q1: 火珠林 operational atlas.** The second of two reading methods. Unmapped. Uses 六親 × 日辰 activation — a time-dependent overlay with floating daily reference, vs 梅花's fixed 體 reference. Would complete the operational pair. Whether the 4/5 ceiling (via 日辰) produces a structurally different arc space than 梅花's 2/5 ceiling is the key structural question.

**Q2: KW sequence ordering.** The pairing is explained (orbit class, R38). The linear order 1–64 is not. Confirmed outside PG(2,F₂) (Z < 1.5σ). Basin clustering is the sole sequential signal (60% same-basin vs 37% expected, p<0.001). 上經/下經 = palindromic/non-palindromic partition. What is the organizing principle?

**Q3: The 0.5-bit.** Algebraically irreducible (V₄ kernel, R52). P→H coherence favors traditional assignment but doesn't force it. The selection chain reduces 240→2: two candidates survive all known constraints with identical counts. Is there a principle beyond coherence, or is this genuinely where mathematics ends and convention begins?

**Q4: 納甲 modification history.** When did the 京氏易傳 → 火珠林 rule change occur? Requires surveying 唐–宋 intermediate texts. Historical-philological, not computational.

### About the texts

**Q5: Temporal × semantic interaction.** Does the 凶×basin bridge strength modulate by season? If the signal is purely structural (position in Z₂⁶), season shouldn't matter. If it modulates, the bridge has a temporal component. Computable from atlas/temporal.json × valence data. Lower priority.

**Q6: Why exactly two bridges?** 凶×basin and 吉×生体 are the entire text-algebra interface. Both distributional, both narrow, operating through core and shell projections respectively. Is it coincidence that there are exactly two, matching the two primitive projections (R5)? Or does the structure predict exactly two contact points?

**Q7: 彖傳 as systematic anomaly detector.** The observation that 彖傳 comments preferentially on structurally unusual lines (Kun basin has highest 剛/柔 ratio) is measured for one variable. Is this systematic across the 彖傳? Fine-grained analysis needed.

**Q8: Three-register temporal architecture.** Three historical layers see three different primes: 爻辭 (~9th c. BC) → positions; 小象/彖傳 (~5th c. BC) → Z₂ binary structure; 五行 (~1st c. BC) → Z₅ dynamics. Does the temporal sequence follow the prime ordering by coincidence or by necessity? Pattern observation, not measured.

**Q9: 說卦傳 sequence.** The 說卦傳 lists trigram attributes (family members, body parts, animals, directions). These are partly algebraic (direction = compass, verified), partly conventional (animals). Untested whether the non-compass attributes carry algebraic signal.

### Interpretive (not computational)

**Q10: Incommensurability as mechanism.** The system's practical function (divination) may depend on the incommensurability between Z₂ and Z₅ — you enter through binary (casting), exit through pentadic (interpretation). The 2/5 visibility ceiling (only 2 of 5 elements visible at once) creates structural partiality. Is partiality a bug (lossy projection) or a feature (forced specificity)?

*Note: "What is the coordinate-free object?" is the central question of `unification/unification.md` Phase 3 — it's a question about the mathematics, not the I Ching.*

---

## Document map

| Folder | Contents |
|--------|----------|
| `atlas/` | Static 五行 atlas: 64 hexagram profiles, torus, transformations, constraints, temporal overlay. Terminal structural computation. |
| `mh-atlas/` | 梅花 operational atlas: 384 states, arcs, torus flow, channels, timing, 18 domains. |
| `deep/` | Deep exploration: 9 iterations proving (3,5) uniqueness, derivation tree, 42 resolved items in open-questions.md. |
| `unification/` | Unification program: PG(2,F₂) framework (synthesis-1/2.md), (n,p) landscape, selection chain, eigenstructure. 12 iterations across 2 phases. |
| `semantic-map/` | Text-algebra interface: 89% residual, two bridges, three commentary registers. 9 scripts, 13 data files. |
| `unification/unification.md` | Phase 3: the search for the object. Central question + 6 supporting questions. |
| `synthesis/` | Early cross-workflow synthesis (bridges, orthogonality wall). Superseded by later findings docs but data files still referenced. |
| `huozhulin/` | 火珠林 preliminary: 納甲 map, palace kernel, 六親 algebra. Partial — full atlas unmapped (Q1). |
| `opposition-theory/` | Early algebraic exploration (cycle algebra, phase structure). Absorbed into deep/ and unification/. |
| `texts/` | Source texts: yaoci.json, guaci.json, xiangzhuan.json, tuanzhuan, etc. |

## Source cross-references

- Primary document: `unification/unification.md`
- Definitive account: `unification/synthesis-2.md`
- Full result inventory: `deep/open-questions.md` (R1–R52)
- Semantic map: `semantic-map/findings.md`
- Number theory questions: `numbers/questions.md`
