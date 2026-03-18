# I Ching Architecture Applied to Markets

## Source

This draws on the I Ching structural research program (180 results across 16 workflows). Key references:

- `iching/usage.md` — the system as judgment instrument
- `iching/reversal/findings.md` — the residual, axioms, judgment boundary (R94–R180)
- `iching/unification/synthesis-3.md` — the uniqueness theorem (15 theorems)
- `iching/directory.md` — full research directory

## Core Insight

The I Ching is not a prediction system. It is a judgment instrument with a specific architecture:

```
Continuous reality → Discretization → Assessment vocabulary → Relational evaluation → Judgment
```

The research proved this architecture has a precise 11/89 split — 11% algorithmic, 89% judgment — and the gap is *by design*. The system explicitly formalizes its own specification gap. What transfers to trading is the architecture, not the content.

---

## The Architecture in Trading

```
Price/volume/macro data → Indicators/signals → Condition classification → Relational evaluation → Trade decision
```

### 1. Design the Gap

Most trading systems try to eliminate discretion. The I Ching's finding: the gap between algorithm and judgment is structural, not a failure to be optimized away. The tradition explicitly states: 「推數又須明理」 — calculation must be supplemented by reasoning (R143).

**Application:** Build systems that explicitly separate what the algorithm handles from what judgment handles. Formalize the boundary. Don't pretend the algorithm covers everything; don't pretend judgment is arbitrary.

The algorithm handles:
- Signal identification
- Regime classification
- Position sizing rules
- Risk limits

Judgment handles:
- Is this signal real? (真 vs 形色)
- Does the context support the signal?
- How do multiple signals relate to each other?
- When to override

### 2. The 真/形色 Question

The 梅花 tradition formalizes: 「真火能克金，形色則不能克」 — real fire can destroy metal; the mere appearance of fire cannot (R142).

**Translation:** A real breakout destroys a range. A false breakout merely looks like one. The algorithm says "breakout signal." The judgment says "is this 真 (real) or 形色 (apparent)?" This magnitude assessment is the central practitioner operation — not an afterthought, but the primary judgment call.

The research proved this gap is irreducible: no algebraic feature predicts opposition strength (R131). No decomposable formalism captures it (R149). The magnitude question can only be answered by compositional assessment of the full situation.

### 3. Grid and Terrain

The I Ching uses 象 (symbolic categories) as a discrete coordinate grid: "this is hexagram X, trigram Y." The thematic manifold is the continuous terrain those coordinates index. Correlation between grid and terrain is exactly zero (R145, Mantel r = −0.003).

**Translation:** The setup type (breakout, mean-reversion, trend continuation) is the grid. The specific feel of *this particular* instance is the terrain. Knowing you're in a "breakout setup" tells you nothing about the terrain of this specific breakout. Two setups can be identical on the grid and completely different on the terrain.

Every experienced trader knows this. The transferable insight: grid and terrain are *provably* independent, not just "sometimes different." Systems that classify setups without navigating terrain are incomplete by structural necessity.

---

## Relational Assessment: The 五行 Parallel

The five phases (五行) are not categories. They're *positions in a relational cycle*. Wood doesn't describe a thing. Wood-generates-Fire describes how two things relate. The I Ching uses two independent relational cycles:

- **生 (generation):** This condition nourishes that one
- **克 (destruction):** This condition undermines that one

The research proved Z₅ is the minimum prime supporting two independent Hamiltonian cycles (R102). Whether trading needs exactly five relational positions is an empirical question. But the dual-cycle architecture — two independent evaluations of how conditions relate — is the transferable structure.

### Relational Evaluation of Market Conditions

Don't label a market condition with an element. Assess the *relation* between two conditions (2 directed relational cycles on Z₅):

**生 relations (generative):**
- Volatility expansion → generates breakout opportunities
- Trend persistence → generates momentum confirmation
- Liquidity influx → generates price discovery
- Compression → generates energy for directional move
- Confirmation across timeframes → generates conviction

**克 relations (destructive):**
- Range compression → destroys trend signals
- Divergence → destroys breakout confidence
- News shock → destroys technical setups
- Liquidity withdrawal → destroys orderly price action
- Conflicting timeframes → destroys conviction

**The dual-cycle tension:** The same condition can be simultaneously generative in one dimension and destructive in another. Rising volume might generate breakout opportunity (生) while destroying position sizing confidence (克) through increased slippage risk. The two cycles give you the tension — and that tension is where judgment lives.

### The Interface Asymmetry

The {4,2,2,2,2} cascade (see `iching/atlas-hzl/findings.md`): Earth occupies 4 of 12 temporal positions, Fire/Metal only 2 each. The interface is calibrated so that the default background is transition/consolidation. Deviations carry disproportionate signal.

**Trading parallel:** Most of the time, markets are in transition — consolidating, chopping, digesting. Sharp directional conditions (trend, breakout, crash) are rare but carry disproportionate signal. A system calibrated to treat transition as the default, with heightened sensitivity during rare directional periods, mirrors the 納甲 interface:

- **Common background (Earth-equivalent):** Range, consolidation, low-information. Default position sizing. Standard rules apply.
- **Rare signal (Fire/Metal-equivalent):** Strong trend, volatility event, regime change. Heightened attention. This is where the 真/形色 question matters most — is this the real thing or just the shape of one?

The scarcity of directional periods *is itself* information. A system that expects chop and responds to genuine direction has a structural edge over one that treats every signal equally.

---

## The Five Judgment Operations in Trading

The I Ching research characterized exactly five practitioner operations at the algorithm-judgment boundary (R140), invariant across two different divination traditions. These map directly:

| Operation | I Ching (freq) | Trading equivalent |
|-----------|---------------|-------------------|
| **Analogy** | 40% | Pattern recognition: "this looks like X setup." Contextual activation of prior experience. Not mechanical pattern matching — contextual, situational. |
| **Integration** | 19% | Confluence assessment: do independent channels (price action, volume, macro, positioning) converge on the same conclusion? Two independent information streams that must agree. |
| **External** | 19% | Regime/context awareness: calendar effects, news cycle, liquidity conditions, broader market state. Information from outside the immediate signal. |
| **Weighting** | 17.5% | Magnitude assessment: how strong is this signal? Is it 真 (real) or 形色 (apparent)? This is partly algorithmic (counting confirming/disconfirming factors) and partly judgment (assessing whether the confirming factors are genuine). |
| **Exception** | 5% | Override: "something's wrong." Kill the trade despite the signal. The rarest operation but the most important for risk management. |

**Three-phase sequence:** Read (analogy + integration) → Assess (weighting) → Anchor (external context). Exceptions interrupt when the standard reading would be wrong.

This is a trainable repertoire. Not "use your gut" — five specific operations in a specific sequence. A trading journal could be structured around these five: for each trade, which operations did you perform, in what order, and what did each contribute?

---

## Composability

The deepest axiom: situations are built from independent binary aspects (the group axiom on F₂ⁿ). This is the creative insight that makes the I Ching the I Ching — the one contingent step in the forcing chain (R174).

Market situations decompose similarly:

| Binary polarity | States |
|----------------|--------|
| Direction | Trending / Ranging |
| Volatility | Expanding / Contracting |
| Risk appetite | Risk-on / Risk-off |
| Level | Above / Below key reference |
| Liquidity | Ample / Thin |
| Confirmation | Confirming / Diverging |

Each is an independent binary assessment. The market situation is their composition. The I Ching's uniqueness theorem says: if you take composability seriously, add polarity (each state has an opposite) and dual evaluation (生/克), you get one rigid structure.

Whether the trading version has the same rigidity is an open question. The number of independent binary polarities might differ (6 market dimensions vs 6 hexagram lines — coincidental). The evaluation might need more or fewer than 5 relational positions. But the architectural principle — that a situation is a composition of independent binary assessments, evaluated relationally — transfers directly.

---

## What Doesn't Transfer

- **Element assignments.** "This market is Wood" is category error. The elements are relational positions, not labels.
- **Divination.** Casting coins to determine trades. The research showed the system is a judgment instrument, not a prediction engine.
- **The specific number 5.** Z₅ is forced by the I Ching's axioms. Trading may have a different relational structure requiring a different prime (or no prime at all).

## What Transfers

- **The 11/89 architecture.** Formalize the algorithm-judgment boundary. Don't try to eliminate it.
- **The 真/形色 question.** The primary judgment operation is magnitude assessment: is this real?
- **Grid ⊥ terrain.** Setup type and situation feel are provably independent.
- **Five judgment operations.** A trainable, finite repertoire for navigating the gap.
- **Dual relational evaluation.** Assess how conditions relate to each other, not what category they belong to.
- **Interface asymmetry.** Calibrate to the common background; treat deviation as signal.
- **Composability.** Decompose situations into independent binary aspects; evaluate the composition.

---

## Crossing the Gap: A Reward Model for 真/形色

The 11/89 split implies most of the value lives in judgment. The hardest judgment call — is this signal real (真) or merely the shape of one (形色)? — is a scoring problem. A local model trained to score signal genuineness could cross the gap.

### The idea

Train a reward model that scores algo-generated signals on a 真/形色 scale. The algo generates candidates. The model scores each. You set the threshold. The model doesn't trade — it filters.

### What it would need

**Structured input (the grid):** The composability layer — each market moment decomposed into its binary polarities (trending/ranging, vol expanding/contracting, risk-on/off, above/below level, confirming/diverging, liquidity ample/thin). Plus: the signal itself, its source channel, current regime classification, calendar/event context.

**Training signal:** Historical signals with outcomes. Each labeled: was this 真 (signal led to profitable resolution) or 形色 (signal failed despite looking right)? The richer the annotation — what context mattered, what distinguished real from apparent — the better.

**Chain-of-thought structure:** The five judgment operations as a reasoning template. For each signal, the model walks through:
1. **Analogy** — what historical situations does this resemble?
2. **Integration** — do independent channels confirm?
3. **Weighting** — how strong is the evidence, and is it genuine?
4. **External** — what regime/context factors apply?
5. **Exception** — any disqualifying conditions?

Then scores.

### Open questions

- How much annotated history is needed before the model has enough terrain to navigate?
- Does the binary polarity decomposition (composability) provide a better state representation than raw features?
- Can the model learn the 真/形色 distinction from outcomes alone, or does it need human-annotated reasoning about *why* signals were real or apparent?
- Does the interface asymmetry principle (most time is background, rare periods carry signal) help with class imbalance in training?
- What's the right base model size for this narrow task?

note: 18 was the start of the last run - **Hexagram content.** The 384 line texts describe human situations in ancient Chinese agricultural society. They don't describe markets.