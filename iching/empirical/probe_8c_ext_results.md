# Probe 8c-ext: Arc Symmetry Under Three 体克用 Modes

Tests whether the arc symmetries from atlas-mh hold when 体克用 is revalued.

## 1. Valence Templates

| Relation | Competition | Manifestation | Nurture | Nurture-full |
|----------|-------------|---------------|---------|-------------|
| 生体 | +2 | +2 | +2 | +2 |
| 体克用 | +1 | +0 | -1 | -1 |
| 比和 | +0 | +0 | +0 | +0 |
| 体生用 | -1 | -1 | -1 | +1 |
| 克体 | -2 | -2 | -2 | -2 |

**Competition:** Standard atlas-mh (14/17 domains)
**Manifestation:** 体克用 = delayed/ambiguous (5 domains: 婚姻, 求謀, 求名, 行人, 失物)
**Nurture:** 体克用 = unfavorable (2 domains: 飲食, 生產)
**Nurture-full:** Additionally 体生用 inverted (1 domain: 生產)

## 2. Arc Type Distributions

| Arc type | Competition | Manifestation | Nurture | Nurture-full |
|----------|-------------|---------------|---------|-------------|
| stable_neutral |    6 |   25 |    6 |    6 |
| rescued |   56 |   30 |   48 |   64 |
| betrayed |   56 |   30 |   48 |   64 |
| improving |   52 |   30 |   12 |   40 |
| deteriorating |   52 |   78 |   86 |   56 |
| stable_favorable |   47 |   39 |    0 |    2 |
| stable_unfavorable |   48 |  117 |  129 |   61 |
| mixed |   67 |   35 |   55 |   91 |
| **total** |  384 |  384 |  384 |  384 |

## 3. Symmetry Checks

| Template | rescued | betrayed | R=B? | improving | deteriorating | I=D? |
|----------|---------|----------|------|-----------|---------------|------|
| competition | 56 | 56 | ✓ | 52 | 52 | ✓ |
| manifestation | 30 | 30 | ✓ | 30 | 78 | ✗ |
| nurture | 48 | 48 | ✓ | 12 | 86 | ✗ |
| nurture_full | 64 | 64 | ✓ | 40 | 56 | ✗ |

### Symmetry breaking in manifestation

| Arc type | Competition | manifestation | Delta |
|----------|-------------|---------|-------|
| stable_neutral | 6 | 25 | +19 |
| rescued | 56 | 30 | -26 |
| betrayed | 56 | 30 | -26 |
| improving | 52 | 30 | -22 |
| deteriorating | 52 | 78 | +26 |
| stable_favorable | 47 | 39 | -8 |
| stable_unfavorable | 48 | 117 | +69 |
| mixed | 67 | 35 | -32 |

### Symmetry breaking in nurture

| Arc type | Competition | nurture | Delta |
|----------|-------------|---------|-------|
| rescued | 56 | 48 | -8 |
| betrayed | 56 | 48 | -8 |
| improving | 52 | 12 | -40 |
| deteriorating | 52 | 86 | +34 |
| stable_favorable | 47 | 0 | -47 |
| stable_unfavorable | 48 | 129 | +81 |
| mixed | 67 | 55 | -12 |

### Symmetry breaking in nurture_full

| Arc type | Competition | nurture_full | Delta |
|----------|-------------|---------|-------|
| rescued | 56 | 64 | +8 |
| betrayed | 56 | 64 | +8 |
| improving | 52 | 40 | -12 |
| deteriorating | 52 | 56 | +4 |
| stable_favorable | 47 | 2 | -45 |
| stable_unfavorable | 48 | 61 | +13 |
| mixed | 67 | 91 | +24 |

## 4. Stable Neutral Invariance

| Template | 6 stable_neutral states survive? |
|----------|---------------------------------|
| competition | ✓ all 6 |
| manifestation | ✓ all 6 |
| nurture | ✓ all 6 |
| nurture_full | ✓ all 6 |

## 5. Favorable ↔ Unfavorable Flips

### manifestation
- Favorable → Unfavorable: **33** states
- Unfavorable → Favorable: **0** states

  Sample favorable→unfavorable transitions:
  - hex= 0 line=2: improving → stable_unfavorable (rv=['比和', '比和', '克体', '体克用'], vals=[0, 0, -2, 0])
  - hex= 3 line=1: rescued → stable_unfavorable (rv=['体生用', '比和', '克体', '体克用'], vals=[-1, 0, -2, 0])
  - hex= 4 line=5: improving → stable_unfavorable (rv=['比和', '体克用', '克体', '体克用'], vals=[0, 0, -2, 0])
  - hex= 6 line=3: rescued → stable_unfavorable (rv=['克体', '克体', '体生用', '体克用'], vals=[-2, -2, -1, 0])
  - hex=10 line=6: rescued → stable_unfavorable (rv=['体生用', '体克用', '比和', '体克用'], vals=[-1, 0, 0, 0])

### nurture
- Favorable → Unfavorable: **69** states
- Unfavorable → Favorable: **0** states

  Sample favorable→unfavorable transitions:
  - hex= 0 line=2: improving → deteriorating (rv=['比和', '比和', '克体', '体克用'], vals=[0, 0, -2, -1])
  - hex= 0 line=5: improving → deteriorating (rv=['比和', '比和', '比和', '体克用'], vals=[0, 0, 0, -1])
  - hex= 1 line=4: stable_favorable → stable_unfavorable (rv=['体克用', '体克用', '体克用', '比和'], vals=[-1, -1, -1, 0])
  - hex= 1 line=6: stable_favorable → stable_unfavorable (rv=['体克用', '体克用', '体克用', '体克用'], vals=[-1, -1, -1, -1])
  - hex= 3 line=1: rescued → stable_unfavorable (rv=['体生用', '比和', '克体', '体克用'], vals=[-1, 0, -2, -1])

### nurture_full
- Favorable → Unfavorable: **68** states
- Unfavorable → Favorable: **40** states

  Sample favorable→unfavorable transitions:
  - hex= 0 line=2: improving → deteriorating (rv=['比和', '比和', '克体', '体克用'], vals=[0, 0, -2, -1])
  - hex= 0 line=5: improving → deteriorating (rv=['比和', '比和', '比和', '体克用'], vals=[0, 0, 0, -1])
  - hex= 1 line=4: stable_favorable → stable_unfavorable (rv=['体克用', '体克用', '体克用', '比和'], vals=[-1, -1, -1, 0])
  - hex= 1 line=6: stable_favorable → stable_unfavorable (rv=['体克用', '体克用', '体克用', '体克用'], vals=[-1, -1, -1, -1])
  - hex= 3 line=1: rescued → betrayed (rv=['体生用', '比和', '克体', '体克用'], vals=[1, 0, -2, -1])

  Sample unfavorable→favorable transitions:
  - hex= 1 line=2: stable_unfavorable → rescued (rv=['克体', '比和', '比和', '体生用'], vals=[-2, 0, 0, 1])
  - hex= 2 line=1: betrayed → rescued (rv=['体克用', '比和', '克体', '体生用'], vals=[-1, 0, -2, 1])
  - hex= 2 line=4: stable_unfavorable → rescued (rv=['克体', '体生用', '克体', '体生用'], vals=[-2, 1, -2, 1])
  - hex= 6 line=1: stable_unfavorable → rescued (rv=['克体', '克体', '体生用', '体生用'], vals=[-2, -2, 1, 1])
  - hex= 9 line=3: deteriorating → improving (rv=['比和', '生体', '体克用', '体生用'], vals=[0, 2, -1, 1])

## 6. Arc Type Transition Matrices

Shows how arc types change from competition (standard) to each alternative template.

### Competition → manifestation

**122 states changed** arc type, 262 unchanged.

| from \ to | stable_n |  rescued | betrayed | improvin | deterior | stable_f | stable_u |    mixed | total |
|---|---|---|---|---|---|---|---|---|---|
| stable_neutr | **   6** |          |          |          |          |          |          |          |     6 |
| rescued      |          | **  30** |          |          |          |          |      22  |       4  |    56 |
| betrayed     |          |          | **  30** |          |      26  |          |          |          |    56 |
| improving    |       7  |          |          | **  30** |          |       4  |      11  |          |    52 |
| deterioratin |          |          |          |          | **  52** |          |          |          |    52 |
| stable_favor |      12  |          |          |          |          | **  35** |          |          |    47 |
| stable_unfav |          |          |          |          |          |          | **  48** |          |    48 |
| mixed        |          |          |          |          |          |          |      36  | **  31** |    67 |

### Competition → nurture

**180 states changed** arc type, 204 unchanged.

| from \ to | stable_n |  rescued | betrayed | improvin | deterior | stable_f | stable_u |    mixed | total |
|---|---|---|---|---|---|---|---|---|---|
| stable_neutr | **   6** |          |          |          |          |          |          |          |     6 |
| rescued      |          | **  30** |          |          |          |          |      22  |       4  |    56 |
| betrayed     |          |          | **  30** |          |      12  |          |      11  |       3  |    56 |
| improving    |          |      18  |          | **  12** |      22  |          |          |          |    52 |
| deterioratin |          |          |          |          | **  52** |          |          |          |    52 |
| stable_favor |          |          |      13  |          |          |          |      12  |      22  |    47 |
| stable_unfav |          |          |          |          |          |          | **  48** |          |    48 |
| mixed        |          |          |       5  |          |          |          |      36  | **  26** |    67 |

### Competition → nurture_full

**278 states changed** arc type, 106 unchanged.

| from \ to | stable_n |  rescued | betrayed | improvin | deterior | stable_f | stable_u |    mixed | total |
|---|---|---|---|---|---|---|---|---|---|
| stable_neutr | **   6** |          |          |          |          |          |          |          |     6 |
| rescued      |          | **  14** |      14  |      16  |          |          |       7  |       5  |    56 |
| betrayed     |          |      14  | **  14** |          |      12  |          |          |      16  |    56 |
| improving    |          |      18  |          | **  12** |      22  |          |          |          |    52 |
| deterioratin |          |          |      18  |      12  | **  22** |          |          |          |    52 |
| stable_favor |          |          |      13  |          |          |          |      12  |      22  |    47 |
| stable_unfav |          |      14  |          |          |          |          | **  12** |      22  |    48 |
| mixed        |          |       4  |       5  |          |          |       2  |      30  | **  26** |    67 |

## 7. 体克用 Position Analysis

Which vector positions contain 体克用, and how reclassification redistributes them.

- Position 0 (ben): **78** states contain 体克用
- Position 1 (ti_hu): **121** states contain 体克用
- Position 2 (yong_hu): **87** states contain 体克用
- Position 3 (bian): **78** states contain 体克用

- 体克用 at ben (start): 78 states
- 体克用 at bian (end): 78 states
- 体克用 at both endpoints: 12 states

These are the states most affected by revaluation, since the arc classifier primarily uses ben (start) and bian (end) valences.

### Arc types for states with 体克用 at ben position

| Arc type | Competition | Manifestation | Nurture | Nurture-full |
|----------|-------------|---------------|---------|-------------|
| stable_neutral |    0 |   12 |    0 |    0 |
| rescued |    0 |    0 |   18 |   32 |
| betrayed |   26 |    0 |    0 |    0 |
| improving |   18 |   18 |    0 |    0 |
| deteriorating |    0 |   26 |   12 |   12 |
| stable_favorable |   21 |    9 |    0 |    0 |
| stable_unfavorable |    0 |   11 |   34 |   22 |
| mixed |   13 |    2 |   14 |   12 |

## 8. Summary

**Symmetry is broken under some templates.**

- competition: R=B ✓, I=D ✓
- manifestation: R=B ✓, I=D ✗ BROKEN
- nurture: R=B ✓, I=D ✗ BROKEN
- nurture_full: R=B ✓, I=D ✗ BROKEN

**All 6 stable_neutral states survive under every template** — they have all-比和 vectors, which map to all-zero valence regardless of 体克用 mode.
