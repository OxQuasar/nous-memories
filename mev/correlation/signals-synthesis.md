# Correlation-Cascade Investigation — Signals Synthesis

> 4 iterations, 2026-03-20

---

## Core Finding

**The reflexive LST depeg cascade through Aave's $5.6B phantom wall is structurally blocked.** All Aave CAPO adapters use `cap(protocol_rate) × ETH/USD` — no market-price feeds. DEX depegs do not propagate to Aave's liquidation engine. Bytecode-verified with 0.0000% price reconstruction error for all three tokens (wstETH, weETH, osETH).

**The system traded distributed market risk for concentrated operational risk.** The same architecture that blocks market cascades creates a centralized configuration surface (CAPO snapshot parameters) where a single operational error produces the exact liquidation cascade the architecture was designed to prevent.

---

## Signal Assessment: What Showed Lead Time

### Tier 1 — Demonstrated, actionable

**1. CAPO Snapshot Staleness** — STRONGEST SIGNAL
- *What it is:* Age and drift of the CAPO `snapshotRatio` parameter vs actual protocol rate
- *Why it matters:* March 10, 2026 demonstrated that ratio/timestamp misalignment produces instant mass liquidation (49 events, 84 seconds, $28.7M). The failure is operational, not market-driven.
- *Current state:* weETH snapshot from March 2024 (5.4% drift from actual rate). osETH from April 2024. Both exceed the 2.85% incident magnitude.
- *Lead time:* Continuously monitorable on-chain. The drift is visible weeks/months before any incident.
- *Actionability:* High. Monitor `snapshotRatio` on each CAPO adapter. Alert when drift exceeds 2%.

**2. Phantom Position HF Distribution Shifts** — STRONG SIGNAL
- *What it is:* Health factor distribution of large phantom positions (>$100M)
- *Why it matters:* The $1.42B whale survived March 10 by 0.98%. If it had added leverage (lowering HF from 1.040 to 1.028), it would have been liquidated. Position changes are visible before any trigger event.
- *Lead time:* Days to weeks. Large position changes are on-chain events.
- *Actionability:* Moderate. Monitor Aave deposit/borrow events for mega-whales.

### Tier 2 — Relevant for cross-protocol risk, not Aave-direct

**3. DEX Liquidity Cliff Proximity** — RELEVANT BUT INDIRECT
- *What it is:* Current sell volume needed to exhaust DEX liquidity for each LST
- *Why it matters:* Not for Aave (oracle doesn't watch DEX), but for other protocols (Morpho, Euler, Spark) that may use market-price feeds. Also determines liquidator execution quality when Aave DOES liquidate.
- *Current state:* wstETH cliff at ~$5.7M, weETH at ~$13.9M, osETH at ~$976K. All show phase-transition (cliff, not curve) behavior.
- *Lead time:* Liquidity changes over days/weeks. Pool TVL is monitorable.
- *Actionability:* Low for Aave cascade. High for cross-protocol cascade hypothesis.

**4. Chainlink stETH/ETH Feed Behavior** — RELEVANT FOR OTHER PROTOCOLS ONLY
- *What it is:* 24h heartbeat, no deviation-triggered updates observed. Rate: 0.999.
- *Why it matters:* NOT used by Aave CAPO. But any protocol using this feed has up to 24h oracle lag during a genuine stETH depeg.
- *Lead time:* N/A — it's a structural parameter, not a signal.

### Tier 3 — Background monitoring

**5. Validator Slashing Events** — LOW FREQUENCY, HIGH SEVERITY
- *What it is:* Correlated validator failures that reduce protocol exchange rates
- *Why it matters:* A 3.83% drop in `getPooledEthByShares` would liquidate the $1.42B wstETH whale. Propagates instantly through protocol rate → CAPO → Aave.
- *Lead time:* Minutes to hours (slashing is on-chain but rate impact propagates through protocol mechanics).
- *Actionability:* Low — rare, hard to anticipate. Monitor Beaconchain for correlated slashing.

**6. ETHx/osETH as Canary Tokens** — WEAK FOR AAVE, USEFUL FOR ECOSYSTEM
- *What it is:* Tier 3 LSTs with thinnest liquidity ($21K ETHx, $976K osETH) crack first in any LST selling event.
- *Why it matters:* Not directly for Aave (protocol-rate oracle), but depeg in these tokens is early warning for broader LST stress that could affect protocols with market-price oracles.
- *Lead time:* Simultaneous with or slightly before larger LST stress.

---

## What Was Noise — Do Not Revisit

**1. DEX cascade ratios (20x–4,681x) as Aave vulnerability metric.** These ratios compare DEX depth to phantom exposure, but the Aave oracle doesn't watch DEX prices. The ratios remain meaningful for protocols using market-price feeds, but are not an Aave cascade trigger. The initial thesis that these ratios quantify Aave cascade risk was refuted.

**2. Chainlink stETH/ETH update timing as Aave cascade bottleneck.** The 24h heartbeat analysis was extensive but ultimately irrelevant — the feed is not embedded in any CAPO adapter. It matters for other protocols, not Aave.

**3. stETH/ETH and eETH/ETH DEX depth as "oracle-facing layer."** Measured in iteration 3 on the assumption that Aave's oracle watched these markets. It doesn't. The shared-pool finding (stETH routes through wstETH pools) is interesting market microstructure but not cascade-relevant for Aave.

**4. Historical depeg magnitudes (Step 2, never executed).** Was designed to answer "how often do depegs reach cascade-triggering levels?" Since DEX depegs don't trigger Aave liquidations, the question became moot for the primary investigation. Still relevant if the cross-protocol hypothesis is pursued.

---

## Composite Signal Construction

Based on the investigation, a practical monitoring composite would combine:

### CAPO Operational Risk Monitor (Primary)
```
For each LST in {wstETH, weETH, osETH}:
  drift = (current_protocol_rate - snapshotRatio) / snapshotRatio
  days_since_snapshot = now - snapshotTimestamp
  
  ALERT if drift > 2%  (March 10 was 2.85%)
  WARN  if drift > 1.5%
  WATCH if days_since_snapshot > 30
  
  On any snapshotRatio update tx:
    new_drift = abs(new_ratio - current_protocol_rate) / current_protocol_rate
    ALERT if new_drift > 1%  (misconfiguration indicator)
```

### Position Topology Monitor (Secondary)
```
For each mega-whale (>$100M phantom position):
  depeg_margin = (HF - 1.0) / HF
  
  ALERT if depeg_margin < 2%  (within March 10 incident range)
  WARN  if depeg_margin < 3%
  
  On any deposit/borrow event for whale addresses:
    recompute HF
    ALERT if HF decreased
```

### Ecosystem Stress Monitor (Background)
```
  stETH/ETH DEX price deviation from 1.0
  ALERT if > 0.5% sustained for > 1 hour
  
  Validator slashing event count (Beaconchain)
  ALERT if > 50 validators slashed in single epoch
```

---

## Next Steps

The investigation has reached the boundary of what technical probing can determine for the Aave-specific cascade. Three threads remain open:

### 1. Cross-Protocol Oracle Survey (Highest leverage)
Do Morpho, Euler, Spark use market-price Chainlink feeds for LSTs? If yes, the reflexive cascade model disproved for Aave may apply to those protocols. The DEX depth data, cascade ratios, and Chainlink timing analysis become directly relevant. A cascade originating in other protocols could propagate to Aave through sustained market stress → protocol rate erosion.

### 2. CAPO Monitoring Pipeline (Most actionable)
Build the composite monitor described above. The CAPO snapshot staleness is monitorable today with simple on-chain queries. weETH drift at 5.4% already exceeds the incident threshold.

### 3. Protocol Rate Disruption Magnitude (Background)
How much correlated validator slashing would change `getPooledEthByShares` or `getRate()` by 3-5%? Requires understanding Lido/EtherFi validator set size and the Ethereum PoS penalty structure. Low probability but determines the protocol-event trigger threshold.

### Not recommended to pursue
- Historical depeg magnitudes (Step 2) — moot for Aave cascade
- Transaction-level cascade replay (Step 5) — the March 10 incident IS the replay
- Cross-LST contagion through DEX pools (Step 6) — mechanism blocked at Aave oracle
