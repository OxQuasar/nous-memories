# Phase 3: Trigram and Nuclear Trigram Decomposition of KW Pairs

## 1. Full Trigram Decomposition (32 pairs)

Encoding: L1=bit0 (bottom) … L6=bit5 (top). Trigrams shown as 3-bit binary.

| # | a | b | Type | lower(a) | upper(a) | lower(b) | upper(b) | lower rel | upper rel | cross(la↔ub) | cross(ua↔lb) |
|---|---|---|------|----------|----------|----------|----------|-----------|-----------|-------------|-------------|
| 1 | 000000 | 111111 | pal | 000 | 000 | 111 | 111 | complement | complement | complement | complement |
| 2 | 000001 | 100000 | rev | 001 | 000 | 000 | 100 | other | other | reversal | identity |
| 3 | 000010 | 010000 | rev | 010 | 000 | 000 | 010 | other | other | identity | identity |
| 4 | 000011 | 110000 | rev | 011 | 000 | 000 | 110 | other | other | reversal | identity |
| 5 | 000100 | 001000 | rev | 100 | 000 | 000 | 001 | other | other | reversal | identity |
| 6 | 000101 | 101000 | rev | 101 | 000 | 000 | 101 | other | other | identity | identity |
| 7 | 000110 | 011000 | rev | 110 | 000 | 000 | 011 | other | other | reversal | identity |
| 8 | 000111 | 111000 | rev | 111 | 000 | 000 | 111 | complement | complement | identity | identity |
| 9 | 001001 | 100100 | rev | 001 | 001 | 100 | 100 | reversal | reversal | reversal | reversal |
| 10 | 001010 | 010100 | rev | 010 | 001 | 100 | 010 | other | other | identity | reversal |
| 11 | 001011 | 110100 | rev | 011 | 001 | 100 | 110 | complement | complement | reversal | reversal |
| 12 | 001100 | 110011 | pal | 100 | 001 | 011 | 110 | complement | complement | comp∘rev | comp∘rev |
| 13 | 001101 | 101100 | rev | 101 | 001 | 100 | 101 | other | other | identity | reversal |
| 14 | 001110 | 011100 | rev | 110 | 001 | 100 | 011 | comp∘rev | comp∘rev | reversal | reversal |
| 15 | 001111 | 111100 | rev | 111 | 001 | 100 | 111 | other | other | identity | reversal |
| 16 | 010001 | 100010 | rev | 001 | 010 | 010 | 100 | other | other | reversal | identity |
| 17 | 010010 | 101101 | pal | 010 | 010 | 101 | 101 | complement | complement | complement | complement |
| 18 | 010011 | 110010 | rev | 011 | 010 | 010 | 110 | other | other | reversal | identity |
| 19 | 010101 | 101010 | rev | 101 | 010 | 010 | 101 | complement | complement | identity | identity |
| 20 | 010110 | 011010 | rev | 110 | 010 | 010 | 011 | other | other | reversal | identity |
| 21 | 010111 | 111010 | rev | 111 | 010 | 010 | 111 | other | other | identity | identity |
| 22 | 011001 | 100110 | rev | 001 | 011 | 110 | 100 | complement | complement | reversal | reversal |
| 23 | 011011 | 110110 | rev | 011 | 011 | 110 | 110 | reversal | reversal | reversal | reversal |
| 24 | 011101 | 101110 | rev | 101 | 011 | 110 | 101 | other | other | identity | reversal |
| 25 | 011110 | 100001 | pal | 110 | 011 | 001 | 100 | complement | complement | comp∘rev | comp∘rev |
| 26 | 011111 | 111110 | rev | 111 | 011 | 110 | 111 | other | other | identity | reversal |
| 27 | 100011 | 110001 | rev | 011 | 100 | 001 | 110 | comp∘rev | comp∘rev | reversal | reversal |
| 28 | 100101 | 101001 | rev | 101 | 100 | 001 | 101 | other | other | identity | reversal |
| 29 | 100111 | 111001 | rev | 111 | 100 | 001 | 111 | other | other | identity | reversal |
| 30 | 101011 | 110101 | rev | 011 | 101 | 101 | 110 | other | other | reversal | identity |
| 31 | 101111 | 111101 | rev | 111 | 101 | 101 | 111 | other | other | identity | identity |
| 32 | 110111 | 111011 | rev | 111 | 110 | 011 | 111 | other | other | identity | reversal |

### Reversal pair structure verification

For reversal pairs: upper(b) = rev₃(lower(a)) and lower(b) = rev₃(upper(a)).

**All 28 reversal pairs pass: True** (28/28)

## 2. Nuclear Trigram Decomposition

Nuclear trigrams: lower_nuc = (L2,L3,L4) = bits 1,2,3; upper_nuc = (L3,L4,L5) = bits 2,3,4.

| # | a | b | Type | lnuc(a) | unuc(a) | lnuc(b) | unuc(b) | lnuc XOR | unuc XOR | lnuc H | unuc H |
|---|---|---|------|---------|---------|---------|---------|----------|----------|--------|--------|
| 1 | 000000 | 111111 | pal | 000 | 000 | 111 | 111 | 111 | 111 | 3 | 3 |
| 2 | 000001 | 100000 | rev | 000 | 000 | 000 | 000 | 000 | 000 | 0 | 0 |
| 3 | 000010 | 010000 | rev | 001 | 000 | 000 | 100 | 001 | 100 | 1 | 1 |
| 4 | 000011 | 110000 | rev | 001 | 000 | 000 | 100 | 001 | 100 | 1 | 1 |
| 5 | 000100 | 001000 | rev | 010 | 001 | 100 | 010 | 110 | 011 | 2 | 2 |
| 6 | 000101 | 101000 | rev | 010 | 001 | 100 | 010 | 110 | 011 | 2 | 2 |
| 7 | 000110 | 011000 | rev | 011 | 001 | 100 | 110 | 111 | 111 | 3 | 3 |
| 8 | 000111 | 111000 | rev | 011 | 001 | 100 | 110 | 111 | 111 | 3 | 3 |
| 9 | 001001 | 100100 | rev | 100 | 010 | 010 | 001 | 110 | 011 | 2 | 2 |
| 10 | 001010 | 010100 | rev | 101 | 010 | 010 | 101 | 111 | 111 | 3 | 3 |
| 11 | 001011 | 110100 | rev | 101 | 010 | 010 | 101 | 111 | 111 | 3 | 3 |
| 12 | 001100 | 110011 | pal | 110 | 011 | 001 | 100 | 111 | 111 | 3 | 3 |
| 13 | 001101 | 101100 | rev | 110 | 011 | 110 | 011 | 000 | 000 | 0 | 0 |
| 14 | 001110 | 011100 | rev | 111 | 011 | 110 | 111 | 001 | 100 | 1 | 1 |
| 15 | 001111 | 111100 | rev | 111 | 011 | 110 | 111 | 001 | 100 | 1 | 1 |
| 16 | 010001 | 100010 | rev | 000 | 100 | 001 | 000 | 001 | 100 | 1 | 1 |
| 17 | 010010 | 101101 | pal | 001 | 100 | 110 | 011 | 111 | 111 | 3 | 3 |
| 18 | 010011 | 110010 | rev | 001 | 100 | 001 | 100 | 000 | 000 | 0 | 0 |
| 19 | 010101 | 101010 | rev | 010 | 101 | 101 | 010 | 111 | 111 | 3 | 3 |
| 20 | 010110 | 011010 | rev | 011 | 101 | 101 | 110 | 110 | 011 | 2 | 2 |
| 21 | 010111 | 111010 | rev | 011 | 101 | 101 | 110 | 110 | 011 | 2 | 2 |
| 22 | 011001 | 100110 | rev | 100 | 110 | 011 | 001 | 111 | 111 | 3 | 3 |
| 23 | 011011 | 110110 | rev | 101 | 110 | 011 | 101 | 110 | 011 | 2 | 2 |
| 24 | 011101 | 101110 | rev | 110 | 111 | 111 | 011 | 001 | 100 | 1 | 1 |
| 25 | 011110 | 100001 | pal | 111 | 111 | 000 | 000 | 111 | 111 | 3 | 3 |
| 26 | 011111 | 111110 | rev | 111 | 111 | 111 | 111 | 000 | 000 | 0 | 0 |
| 27 | 100011 | 110001 | rev | 001 | 000 | 000 | 100 | 001 | 100 | 1 | 1 |
| 28 | 100101 | 101001 | rev | 010 | 001 | 100 | 010 | 110 | 011 | 2 | 2 |
| 29 | 100111 | 111001 | rev | 011 | 001 | 100 | 110 | 111 | 111 | 3 | 3 |
| 30 | 101011 | 110101 | rev | 101 | 010 | 010 | 101 | 111 | 111 | 3 | 3 |
| 31 | 101111 | 111101 | rev | 111 | 011 | 110 | 111 | 001 | 100 | 1 | 1 |
| 32 | 110111 | 111011 | rev | 011 | 101 | 101 | 110 | 110 | 011 | 2 | 2 |

### Nuclear trigram relationships

| # | a | b | Type | lnuc rel | unuc rel |
|---|---|---|------|----------|----------|
| 1 | 000000 | 111111 | pal | complement | complement |
| 2 | 000001 | 100000 | rev | identity | identity |
| 3 | 000010 | 010000 | rev | other | other |
| 4 | 000011 | 110000 | rev | other | other |
| 5 | 000100 | 001000 | rev | other | other |
| 6 | 000101 | 101000 | rev | other | other |
| 7 | 000110 | 011000 | rev | complement | complement |
| 8 | 000111 | 111000 | rev | complement | complement |
| 9 | 001001 | 100100 | rev | other | other |
| 10 | 001010 | 010100 | rev | complement | complement |
| 11 | 001011 | 110100 | rev | complement | complement |
| 12 | 001100 | 110011 | pal | complement | complement |
| 13 | 001101 | 101100 | rev | identity | identity |
| 14 | 001110 | 011100 | rev | other | other |
| 15 | 001111 | 111100 | rev | other | other |
| 16 | 010001 | 100010 | rev | other | other |
| 17 | 010010 | 101101 | pal | complement | complement |
| 18 | 010011 | 110010 | rev | identity | identity |
| 19 | 010101 | 101010 | rev | complement | complement |
| 20 | 010110 | 011010 | rev | other | other |
| 21 | 010111 | 111010 | rev | other | other |
| 22 | 011001 | 100110 | rev | complement | complement |
| 23 | 011011 | 110110 | rev | other | other |
| 24 | 011101 | 101110 | rev | other | other |
| 25 | 011110 | 100001 | pal | complement | complement |
| 26 | 011111 | 111110 | rev | identity | identity |
| 27 | 100011 | 110001 | rev | other | other |
| 28 | 100101 | 101001 | rev | other | other |
| 29 | 100111 | 111001 | rev | complement | complement |
| 30 | 101011 | 110101 | rev | complement | complement |
| 31 | 101111 | 111101 | rev | other | other |
| 32 | 110111 | 111011 | rev | other | other |

## 3. Sub-hexagram Weight Analysis

w = yang-count (popcount). Δw = |w(a_part) − w(b_part)|.

| # | a | b | Type | w(lo_a) | w(up_a) | w(lo_b) | w(up_b) | Δw lo | Δw up | w(ln_a) | w(un_a) | w(ln_b) | w(un_b) | Δw ln | Δw un |
|---|---|---|------|---------|---------|---------|---------|-------|-------|---------|---------|---------|---------|-------|-------|
| 1 | 000000 | 111111 | pal | 0 | 0 | 3 | 3 | 3 | 3 | 0 | 0 | 3 | 3 | 3 | 3 |
| 2 | 000001 | 100000 | rev | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 000010 | 010000 | rev | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 |
| 4 | 000011 | 110000 | rev | 2 | 0 | 0 | 2 | 2 | 2 | 1 | 0 | 0 | 1 | 1 | 1 |
| 5 | 000100 | 001000 | rev | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 6 | 000101 | 101000 | rev | 2 | 0 | 0 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 0 | 0 |
| 7 | 000110 | 011000 | rev | 2 | 0 | 0 | 2 | 2 | 2 | 2 | 1 | 1 | 2 | 1 | 1 |
| 8 | 000111 | 111000 | rev | 3 | 0 | 0 | 3 | 3 | 3 | 2 | 1 | 1 | 2 | 1 | 1 |
| 9 | 001001 | 100100 | rev | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 |
| 10 | 001010 | 010100 | rev | 1 | 1 | 1 | 1 | 0 | 0 | 2 | 1 | 1 | 2 | 1 | 1 |
| 11 | 001011 | 110100 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 1 | 1 |
| 12 | 001100 | 110011 | pal | 1 | 1 | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 |
| 13 | 001101 | 101100 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 0 | 0 |
| 14 | 001110 | 011100 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 3 | 2 | 2 | 3 | 1 | 1 |
| 15 | 001111 | 111100 | rev | 3 | 1 | 1 | 3 | 2 | 2 | 3 | 2 | 2 | 3 | 1 | 1 |
| 16 | 010001 | 100010 | rev | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 1 |
| 17 | 010010 | 101101 | pal | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 |
| 18 | 010011 | 110010 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 19 | 010101 | 101010 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 1 |
| 20 | 010110 | 011010 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 0 | 0 |
| 21 | 010111 | 111010 | rev | 3 | 1 | 1 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 0 | 0 |
| 22 | 011001 | 100110 | rev | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 1 |
| 23 | 011011 | 110110 | rev | 2 | 2 | 2 | 2 | 0 | 0 | 2 | 2 | 2 | 2 | 0 | 0 |
| 24 | 011101 | 101110 | rev | 2 | 2 | 2 | 2 | 0 | 0 | 2 | 3 | 3 | 2 | 1 | 1 |
| 25 | 011110 | 100001 | pal | 2 | 2 | 1 | 1 | 1 | 1 | 3 | 3 | 0 | 0 | 3 | 3 |
| 26 | 011111 | 111110 | rev | 3 | 2 | 2 | 3 | 1 | 1 | 3 | 3 | 3 | 3 | 0 | 0 |
| 27 | 100011 | 110001 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 |
| 28 | 100101 | 101001 | rev | 2 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| 29 | 100111 | 111001 | rev | 3 | 1 | 1 | 3 | 2 | 2 | 2 | 1 | 1 | 2 | 1 | 1 |
| 30 | 101011 | 110101 | rev | 2 | 2 | 2 | 2 | 0 | 0 | 2 | 1 | 1 | 2 | 1 | 1 |
| 31 | 101111 | 111101 | rev | 3 | 2 | 2 | 3 | 1 | 1 | 3 | 2 | 2 | 3 | 1 | 1 |
| 32 | 110111 | 111011 | rev | 3 | 2 | 2 | 3 | 1 | 1 | 2 | 2 | 2 | 2 | 0 | 0 |

## 4. Summary Statistics

### Trigram relationship distributions

#### All pairs (n=32)

| Relationship | lower(a)↔lower(b) | upper(a)↔upper(b) | lower(a)↔upper(b) | upper(a)↔lower(b) |
|-------------|-------------------|-------------------|-------------------|-------------------|
| complement | 8 | 8 | 2 | 2 |
| comp∘rev | 2 | 2 | 2 | 2 |
| identity | 0 | 0 | 14 | 14 |
| other | 20 | 20 | 0 | 0 |
| reversal | 2 | 2 | 14 | 14 |

#### Reversal pairs (n=28)

| Relationship | lower(a)↔lower(b) | upper(a)↔upper(b) | lower(a)↔upper(b) | upper(a)↔lower(b) |
|-------------|-------------------|-------------------|-------------------|-------------------|
| complement | 4 | 4 | 0 | 0 |
| comp∘rev | 2 | 2 | 0 | 0 |
| identity | 0 | 0 | 14 | 14 |
| other | 20 | 20 | 0 | 0 |
| reversal | 2 | 2 | 14 | 14 |

#### Palindromic pairs (n=4)

| Relationship | lower(a)↔lower(b) | upper(a)↔upper(b) | lower(a)↔upper(b) | upper(a)↔lower(b) |
|-------------|-------------------|-------------------|-------------------|-------------------|
| complement | 4 | 4 | 2 | 2 |
| comp∘rev | 0 | 0 | 2 | 2 |

### Nuclear XOR mask distributions

#### All pairs

| XOR mask | lower nuclear | upper nuclear |
|----------|--------------|--------------|
| 000 | 4 | 4 |
| 001 | 8 | 0 |
| 011 | 0 | 8 |
| 100 | 0 | 8 |
| 110 | 8 | 0 |
| 111 | 12 | 12 |

#### Reversal pairs

| XOR mask | lower nuclear | upper nuclear |
|----------|--------------|--------------|
| 000 | 4 | 4 |
| 001 | 8 | 0 |
| 011 | 0 | 8 |
| 100 | 0 | 8 |
| 110 | 8 | 0 |
| 111 | 8 | 8 |

#### Palindromic pairs

| XOR mask | lower nuclear | upper nuclear |
|----------|--------------|--------------|
| 111 | 4 | 4 |

### Weight correlations within KW pairs

| Level | Pearson r |
|-------|----------|
| Full hexagram (w(a) vs w(b)) | 0.5158 |
| Lower trigram | -0.0769 |
| Upper trigram | 0.1250 |
| Lower nuclear | 0.2766 |
| Upper nuclear | 0.2766 |

### Mean |Δw| by sub-hexagram level

| Level | All pairs | Reversal only |
|-------|-----------|---------------|
| Lower trigram | 1.1250 | 1.0714 |
| Upper trigram | 1.1250 | 1.0714 |
| Lower nuclear | 0.7500 | 0.5714 |
| Upper nuclear | 0.7500 | 0.5714 |

## 5. Cross-Decomposition Analysis

### Line position membership

| Line | Mirror pair | Trigram | Nuclear |
|------|-------------|---------|---------|
| L1 (bit 0) | O (outer) | lower | none |
| L2 (bit 1) | M (middle) | lower | lower_nuc |
| L3 (bit 2) | I (inner) | lower | lower_nuc, upper_nuc |
| L4 (bit 3) | I (inner) | upper | lower_nuc, upper_nuc |
| L5 (bit 4) | M (middle) | upper | upper_nuc |
| L6 (bit 5) | O (outer) | upper | none |

### Mirror-pair × Trigram overlap matrix

Each cell shows which line positions fall in both categories.

| Mirror pair | lower | upper |
|-------------|-------|-------|
| O (outer) | L1 | L6 |
| M (middle) | L2 | L5 |
| I (inner) | L3 | L4 |

### Mirror-pair × Nuclear trigram overlap matrix

| Mirror pair | lower_nuc (L2,L3,L4) | upper_nuc (L3,L4,L5) |
|-------------|----------------------|----------------------|
| O (outer) | — | — |
| M (middle) | L2 | L5 |
| I (inner) | L3, L4 | L3, L4 |

### Key structural observations


The **inner pair I = {L3, L4}** is the unique mirror pair split across trigrams:
- L3 belongs to lower trigram; L4 belongs to upper trigram.
- Both L3 and L4 belong to BOTH nuclear trigrams.
- The outer pair O = {L1, L6} is fully split (L1 in lower only, L6 in upper only) with no nuclear overlap.
- The middle pair M = {L2, L5} is fully split across trigrams but each member belongs to exactly one nuclear trigram.

Nuclear trigrams bridge the trigram boundary: lower_nuc = {L2, L3, **L4**} reaches into upper; upper_nuc = {**L3**, L4, L5} reaches into lower.
The L3|L4 membrane is the site where mirror-pair geometry and trigram geometry are maximally non-aligned,
and the nuclear trigrams are the structural elements that span this membrane.

## 6. Analytical Observations

### 6.1 Trigram-level structure of reversal pairs

For all 28 reversal pairs, the hexagram-level reversal (rev₆) decomposes as:
- **Swap** the upper and lower trigrams
- **Reverse** each trigram internally (rev₃)

This means the cross-relationships (lower(a)↔upper(b), upper(a)↔lower(b)) are always either
**identity** (when the trigram is a palindrome under rev₃) or **reversal** (when it's not).
The direct relationships (lower(a)↔lower(b), upper(a)↔upper(b)) are generically unrelated
('other') because they compare trigrams that have been both swapped and reversed.

### 6.2 The 'other' category

20 of 28 reversal pairs show 'other' for direct trigram relationships. This is expected:
lower(b) = rev₃(upper(a)), which equals lower(a) only when upper(a) = rev₃(lower(a)) —
i.e., when the hexagram has the form T|rev₃(T). The 4 'complement' pairs among reversal pairs
are those where T and rev₃(T) happen to be complements (e.g., 000↔111). The 2 'reversal' pairs
are where the hexagram has the form T|T (both trigrams identical and self-palindromic under rev₃).
The 2 'comp∘rev' pairs arise when T|rev₃(T) yields comp∘rev₃ as the direct relationship.

### 6.3 Nuclear XOR mask structure

The nuclear XOR masks show a striking pattern:

- **Lower nuclear** uses masks: {000, 001, 110, 111}
- **Upper nuclear** uses masks: {000, 011, 100, 111}
- Only mask **111** and **000** are shared between lower and upper nuclear

This is structurally determined. Nuclear trigrams are extracted by bit-shifting:
lower_nuc = bits[1:4], upper_nuc = bits[2:5]. Their XOR masks inherit structure from
the hexagram-level XOR mask. For reversal pairs, the hexagram mask is palindromic
(determined by mirror-pair signature). The nuclear XOR is a contiguous 3-bit window
of this 6-bit palindromic mask.

### 6.4 Nuclear XOR as window of hexagram mask

For each pair, the hexagram-level XOR mask m = a⊕b has 6 bits. The nuclear XOR masks are:

- lower_nuc XOR = m[1:4] (bits 1,2,3 of m)
- upper_nuc XOR = m[2:5] (bits 2,3,4 of m)

Since reversal pairs have palindromic masks (mᵢ = m₅₋ᵢ), the 7 possible masks
(from the signature group) map to specific nuclear XOR patterns:

| Hex mask (6-bit) | Signature | lower_nuc XOR | upper_nuc XOR |
|-----------------|-----------|---------------|---------------|
| 001100 | (0,0,1) | 110 | 011 |
| 010010 | (0,1,0) | 001 | 100 |
| 011110 | (0,1,1) | 111 | 111 |
| 100001 | (1,0,0) | 000 | 000 |
| 101101 | (1,0,1) | 110 | 011 |
| 110011 | (1,1,0) | 001 | 100 |
| 111111 | (1,1,1) | 111 | 111 |

The nuclear XOR vocabulary is fully determined by the hexagram-level signature vocabulary.
Both nuclear layers use exactly 4 masks. The overlap is {000, 111} — exactly the masks
where the inner pair (I) contributes the same way to both nuclear windows.

### 6.5 Weight preservation at sub-hexagram levels

Hexagram-level weight is perfectly preserved for reversal pairs (Δw = 0), but this does NOT
propagate to sub-hexagram levels:

- **Trigram level:** mean |Δw| = 1.07 for reversal pairs. The swap+reverse operation
  redistributes weight between lower and upper trigrams. Weight is preserved globally
  but NOT locally.
- **Nuclear level:** mean |Δw| = 0.57 for reversal pairs — better than trigrams (0.57 < 1.07).
  The nuclear trigrams, which span the L3|L4 boundary, experience less weight disruption
  than the standard trigrams.
- **Implication:** Nuclear trigrams are more weight-stable under reversal than standard trigrams.
  This is because nuclear trigrams overlap at {L3, L4} — the inner pair — which contributes
  the same bits to both nuclear trigrams. The shared core dampens weight fluctuations.

### 6.6 Weight correlation hierarchy

The weight correlation between KW partners varies dramatically by decomposition level:

- Full hexagram: r = +0.52 (strong positive, driven by 28/32 reversal pairs with Δw=0)
- Lower nuclear: r = +0.28; Upper nuclear: r = +0.28 (moderate positive)
- Upper trigram: r = +0.13 (weak positive)
- Lower trigram: r = −0.08 (near zero / weak negative)

The nuclear level preserves more of the hexagram-level correlation than the trigram level.
This is consistent with nuclear trigrams spanning the inner pair boundary —
they see more of the global structure than either trigram alone.
