# Probe 5: Multiple 動爻 in Kernel Language

## 1. Change Pattern Distribution

P(flip) = 1/4 per line, independently. E[k] = 1.50, σ = 1.06.

| k (moving lines) | P(k) | Masks |
|-------------------|------|-------|
| 0 | 0.177979 | 1 |
| 1 | 0.355957 | 6 |
| 2 | 0.296631 | 15 |
| 3 | 0.131836 | 20 |
| 4 | 0.032959 | 15 |
| 5 | 0.004395 | 6 |
| 6 | 0.000244 | 1 |

P(no change) = 0.1780. P(exactly 1 change, as in 梅花) = 0.3560.

The **modal outcome is no change** (17.8%), followed by exactly 1 change (35.6%).
But P(≥2 changes) = 46.6% — **nearly half the time, multiple lines move**.

## 2. Onion Component Analysis

| Components touched | P |
|-------------------|------|
| none | 0.177979 |
| O | 0.138428 |
| M | 0.138428 |
| I | 0.138428 |
| O+M | 0.107666 |
| O+I | 0.107666 |
| M+I | 0.107666 |
| O+M+I | 0.083740 |

### Interface (basin-determining) component

- P(no interface change): 0.562500 → basin preserved
- P(one interface bit flips): 0.375000 → **basin crosses**
- P(both interface bits flip): 0.062500 → basin preserved (parity same)
- P(basin change) = 0.375000 = 3/8

## 3. Basin-Crossing Probability

| Mechanism | P(basin change) | P(basin change \| ≥1 flip) |
|-----------|-----------------|---------------------------|
| 梅花 (1 flip) | 0.333333 (= 2/6) | 0.333333 |
| 火珠林 (coin) | 0.375000 (= 3/8) | 0.456192 |

火珠林 is **112.5% as likely** to cross basins as 梅花.
The coin mechanism's ability to flip multiple lines increases basin-crossing
probability because both interface bits can be independently engaged.

## 4. Depth Change Distribution

| Δd | P (unconditional) |
|----|-------------------|
| -2 | 0.038086 |
| -1 | 0.126709 |
| +0 | 0.670410 |
| +1 | 0.126709 |
| +2 | 0.038086 |

P(depth preserved) = 0.6704
P(depth increases) = 0.1648
P(depth decreases) = 0.1648

Depth changes are approximately **symmetric** — no net drift toward or away
from attractors.

## 5. 六親 Word Change

Average line-type changes per transformation:
- Under 變卦's own palace: 4.38 / 6 lines
- Under 本卦's palace (inherited): 3.40 / 6 lines

The palace switch adds substantial 六親 disruption beyond the trigram change.
Switching palaces adds ~0.98 extra type changes on average.

## 6. Expected Information Change

E[Hamming distance] = 1.50 (vs 梅花's fixed 1)

| Outcome | P | Structural meaning |
|---------|---|--------------------|
| No change (d=0) | 0.1780 | 靜卦 — no transformation |
| Exactly 1 flip (d=1) | 0.3560 | Same regime as 梅花 |
| Multiple flips (d≥2) | 0.4661 | Multi-layer engagement |

Nearly half the time (47%), the coin mechanism produces multiple simultaneous
changes — engaging more than one onion layer at once. This is structurally
impossible in 梅花 and gives 火珠林 access to cross-layer dynamics.

## 7. 梅花 vs 火珠林 Summary

| Property | 梅花 | 火珠林 |
|----------|------|--------|
| Flip mechanism | Deterministic (1 line) | Probabilistic (0–6 lines) |
| E[Hamming distance] | 1.00 | 1.50 |
| P(no change) | 0 | 0.1780 |
| P(basin cross) | 0.3333 | 0.3750 |
| P(multi-layer) | 0 | 0.4661 |
| 六親 disruption (own pal.) | — | ~4.4 types |
| 六親 disruption (inherit) | — | ~3.4 types |

## 8. Key Findings

### Finding 1: The coin mechanism is a multi-scale perturbation

Unlike 梅花's single-bit flip (which touches exactly one onion layer),
火珠林's coin mechanism has P=0.466 of engaging multiple layers
simultaneously. This makes 火珠林 structurally capable of capturing
cross-layer dynamics that 梅花 cannot access in a single transformation.

### Finding 2: Basin crossing is more likely under coins

P(basin cross) = 3/8 = 0.3750 for coins vs 2/6 = 0.3333 for
single flip. The ~12% increase comes from the coin's ability to flip interface
bits independently of other layers.

### Finding 3: Depth change is symmetric

The coin mechanism shows no net drift toward or away from attractors.
This is algebraically expected: the uniform flip probability treats all
directions equally, and the depth function is symmetric under complement.

### Finding 4: Palace switch dominates 六親 disruption

The palace switch (from 本卦's to 變卦's own palace) changes ~4.4
out of 6 六親 types, while inheriting the palace changes ~3.4.
The difference measures how much structural disruption the palace system
adds beyond the raw trigram change.

### Finding 5: 靜卦 (no moving lines) is the modal outcome

P(no change) = 0.1780 — the single most probable outcome is no
transformation at all. The 火珠林 mechanism includes 'stillness' as a
structural possibility, unlike 梅花 where transformation is guaranteed.
