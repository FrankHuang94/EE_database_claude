# Solutions 20-07 · Nyquist ADCs: Flash, SAR and Pipeline

Problems: [20-07 problem set](../problems/20-07-problems.md) · Chapter: [20-07](../chapters/20-07-nyquist-adcs.md). Every number below is recomputed by [verify_20_07.py](../verify/verify_20_07.py).

---

## Solutions

### Solution 20-07.1

$2^N - 1$: **31**, **127** and **511**. The count grows by a factor of about **2** per bit.

### Solution 20-07.2

Four comparators fired, so the ones-counting encoder outputs **4**. The first 1→0 transition is after comparator 3, so the first-transition encoder outputs **3**. The true input is near code 3 or 4; the ones count is off by at most one code, while a first-transition encoder can be off by many codes when the bubble sits higher up.

### Solution 20-07.3

$v_x = -0.73 + \text{code}/32$:

| Trial | $v_x$ (V) | Decision |
|---|---|---|
| 10000 | **−0.23** | keep |
| 11000 | **+0.02** | clear |
| 10100 | **−0.105** | keep |
| 10110 | **−0.0425** | keep |
| 10111 | **−0.01125** | keep |

The code is 10111 = **23**: 23/32 = 0.71875 ≤ 0.73 < 0.75.

### Solution 20-07.4

| Bits | Conventional | Monotonic | Saving |
|---|---|---|---|
| 8 | **339.3** | **63.5** | **81.3**% |
| 12 | **5459.3** | **1023.5** | **81.3**% |

Both grow about fourfold per bit, so the saving is almost independent of resolution.

### Solution 20-07.5

7 ns/12 = **0.583** ns per decision. Settling to half an LSB needs $\ln 2^{13}$ = 9.01 time constants, so $\tau_{DAC} \le$ **64.7** ps. Redundancy relaxes this for the early, large steps (Example 20-07.4).

### Solution 20-07.6

$m_k = \sum_{j>k}w_j - w_k + 1$: **64**, **32**, **32**, **32**, **32**, then 0, 0, 0, 0, 0, 0 for the last six decisions (16, 8, 4, 2, 1 and the second 32). The last decisions have small DAC steps that settle quickly; margin is needed where the transients are large, at the start.

### Solution 20-07.7

| Stage | Input | $D$ | Residue |
|---|---|---|---|
| 1 | 0.62 | **+1** | **0.24** |
| 2 | 0.24 | **0** | **0.48** |
| 3 | 0.48 | **+1** | **−0.04** |

The digital output adds the decisions with weights 2:1 per stage, plus whatever the later stages make of −0.04 V.

### Solution 20-07.8

$A > 2^{13}/0.4$ = **20480**, that is **86.2** dB. Such gains are hard at low supply voltages, which is why high-resolution pipelines rely on calibration, gain-boosted or ring amplifiers.

### Solution 20-07.9

The 1.5-bit stage tolerates $\pm V_{REF}/4$ = **±125** mV. The 1-bit stage tolerates **0**: with one comparator at zero, any offset makes some residues exceed $\pm V_{REF}$, outside the next stage's range, and no later decision can correct them. The second comparator buys the redundancy.

### Solution 20-07.10

- Scaled (1, 0.5, 0.25 pF): $kT/C_1(1 + \tfrac12 + \tfrac14)$ = 1.75 $kT/C_1$ → **85.1** µV.
- Equal (1 pF each): $1 + \tfrac14 + \tfrac1{16}$ = 1.3125 $kT/C_1$ → **73.7** µV.
- First stage alone: **64.4** µV.

### Solution 20-07.11

$10\log_{10}[\Delta o^2/(2A^2)] = 10\log_{10}[(2\text{ mV})^2/(2 \times 0.25)]$ = **−51.0** dBc, at $f_s/2$ whatever the input frequency.

### Solution 20-07.12

Gain: $\alpha = 2 \times 10^{-50/20}$ = **0.63**%. Skew: $\Delta t = 1/(\pi \times 5\text{ GHz} \times 10^{50/20})$ = **0.20** ps, or 200 fs.

### Solution 20-07.13

From $\text{FoM}_S = \text{SNDR} + 10\log_{10}(BW/P)$: $P = BW/10^{(\text{FoM}_S - \text{SNDR})/10}$.

(a) $P$ = 50 MHz/10^{10} = **5.0** mW. A pipelined-SAR or a pipeline is the natural choice at 100 MS/s and 14 bits; such figures are at or below today's frontier there (§9).

(b) $P$ = 10 GHz/10^{10.5} = **316** mW. At 20 GS/s and 8 bits, an interleaved array of SARs or pipelines is the norm.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-07.1a | comparators, 5 bits | 31 | — |
| 20-07.1b | comparators, 7 bits | 127 | — |
| 20-07.1c | comparators, 9 bits | 511 | — |
| 20-07.1d | growth per bit | 2 | — |
| 20-07.2a | ones count | 4 | — |
| 20-07.2b | first transition | 3 | — |
| 20-07.3a | v_x trial 1 | −0.23 | V |
| 20-07.3b | v_x trial 2 | 0.02 | V |
| 20-07.3c | v_x trial 3 | −0.105 | V |
| 20-07.3d | v_x trial 4 | −0.0425 | V |
| 20-07.3e | v_x trial 5 | −0.01125 | V |
| 20-07.3f | code | 23 | — |
| 20-07.4a | conventional, 8 bits | 339.3 | C_u V² |
| 20-07.4b | monotonic, 8 bits | 63.5 | C_u V² |
| 20-07.4c | saving, 8 bits | 81.3 | % |
| 20-07.4d | conventional, 12 bits | 5459.3 | C_u V² |
| 20-07.4e | monotonic, 12 bits | 1023.5 | C_u V² |
| 20-07.4f | saving, 12 bits | 81.3 | % |
| 20-07.5a | time per decision | 0.583 | ns |
| 20-07.5b | largest DAC tau | 64.7 | ps |
| 20-07.6a | margin 1 | 64 | LSB |
| 20-07.6b | margin 2 | 32 | LSB |
| 20-07.6c | margin 3 | 32 | LSB |
| 20-07.6d | margin 4 | 32 | LSB |
| 20-07.6e | margin 5 | 32 | LSB |
| 20-07.7a | D stage 1 | 1 | — |
| 20-07.7b | residue stage 1 | 0.24 | V |
| 20-07.7c | D stage 2 | 0 | — |
| 20-07.7d | residue stage 2 | 0.48 | V |
| 20-07.7e | D stage 3 | 1 | — |
| 20-07.7f | residue stage 3 | −0.04 | V |
| 20-07.8a | gain | 20480 | — |
| 20-07.8b | gain in dB | 86.2 | dB |
| 20-07.9a | 1.5-bit tolerance | 125 | mV |
| 20-07.9b | 1-bit tolerance | 0 | mV |
| 20-07.10a | scaled noise | 85.1 | µV |
| 20-07.10b | equal noise | 73.7 | µV |
| 20-07.10c | first stage alone | 64.4 | µV |
| 20-07.11a | offset spur | −51.0 | dBc |
| 20-07.12a | gain mismatch | 0.63 | % |
| 20-07.12b | skew | 0.20 | ps |
| 20-07.13a | power, 14-bit 100 MS/s | 5.0 | mW |
| 20-07.13b | power, 8-bit 20 GS/s | 316 | mW |
