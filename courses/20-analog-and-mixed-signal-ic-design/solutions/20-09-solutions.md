# Solutions 20-09 · DACs

Problems: [20-09 problem set](../problems/20-09-problems.md) · Chapter: [20-09](../chapters/20-09-dacs.md). Every number below is recomputed by [verify_20_09.py](../verify/verify_20_09.py).

---

## Solutions

### Solution 20-09.1

LSB = 2.5 V/4096 = **0.610** mV; code 3000 gives $3000 \times 2.5/4096$ = **1.831** V; the string has $2^{12}$ = **4096** resistors.

### Solution 20-09.2

Code 1011 has $b_3 = 1$, $b_2 = 0$, $b_1 = 1$, $b_0 = 1$. Node by node, $V_k = (b_kV_{REF} + V_{k-1})/2$ with $V_{-1} = 0$: $V_0 = 0.5$, $V_1 = (1 + 0.5)/2 = 0.75$, $V_2 = 0.375$, $V_3 = (1 + 0.375)/2$ = **0.6875** $V_{REF}$ = 11/16. The output resistance is **R** (in units of R: **1**).

### Solution 20-09.3

$2^5 - 1$ = **31** unary cells of $2^{11}$ = **2048** LSB each, and **11** binary cells.

### Solution 20-09.4

- Binary: $\sigma_{DNL} = 0.001\sqrt{2^{16} - 1}$ = **0.256** LSB.
- Segmented 4 + 12: the worst step switches one 4096-unit cell against 4095 binary units: $0.001\sqrt{2^{13} - 1}$ = **0.0905** LSB.

### Solution 20-09.5

$N_t \approx 2^{14}$, $\sqrt{N_t}$ = 128. Mid-scale: $\sigma_u = 1/(3 \times 128)$ = **0.260**%. Exact: $0.5/(1.818 \times 128)$ = **0.215**%.

### Solution 20-09.6

$WL = (\sqrt2 \times 3.5 \times 10^{-3}/(0.5 \times 0.00215))^2$ = **21.2** µm² per unit; × 16,383 = **0.348** mm². Two more bits than Example 20-09.3 cost **10.2** times the area (fourfold per bit, partly offset by the larger overdrive).

### Solution 20-09.7

$Z > R_LN_t^2/2 = 50 \times 1023^2/2$ = **26.2** MΩ. With that $Z$, $xN_t = 50 \times 1023/26.2\text{ MΩ}$ and HD2 ≈ $xN_t/4$ → **−66.2** dBc. A 10-bit-accurate static characteristic does not guarantee 10-bit spectral purity.

### Solution 20-09.8

Estimates: HD2 ≈ 0.01/4 → **−52.0** dBc; HD3 ≈ $0.01^2/16$ → **−104.1** dBc. Exact (harmonic analysis of $n/(1 + nx)$): single-ended HD2 **−52.1** dBc; differential HD2 cancels and HD3 is **−104.2** dBc. The estimates are excellent when $xN_t \ll 1$.

### Solution 20-09.9

Droop at 0.4 $f_s$: **−2.42** dB; image at 0.6 $f_s$: **−5.94** dB, only **3.52** dB below the signal. The reconstruction filter must go from passband to stopband between 400 and 600 MHz.

### Solution 20-09.10

NRZ: from 0 to −3.92 dB, a variation of **3.92** dB. RZ: from $\tfrac12$ at DC to $\tfrac12\,\text{sinc}(0.25)$ at $f_s/2$, a variation of **0.91** dB (at 6 dB less absolute level).

### Solution 20-09.11

Mixed mode: $\text{sinc}(0.35)\sin(0.35\pi)$ → **−2.83** dB. NRZ: $\text{sinc}(0.7)$ → **−8.69** dB. Mixed mode delivers **5.86** dB more in the second zone.

### Solution 20-09.12

- Binary: for 100 ps the output is 511 LSB too high: $511/1024 \times 1\text{ V} \times 100$ ps = **49.9** pV·s.
- Segmented 4 + 6: the new unary cell (64 LSB) overlaps the 63 LSB of binary cells: $63/1024 \times 100$ ps = **6.15** pV·s.

### Solution 20-09.13

$\ln 2^{19}$ = 13.17 time constants: τ ≤ 2 µs/13.17 = **0.152** µs; bandwidth ≥ **1.05** MHz.

### Solution 20-09.14

| Sample | Code | Elements used | Pointer after |
|---|---|---|---|
| 1 | 3 | 0, 1, 2 | **3** |
| 2 | 5 | 3, 4, 5, 6, 7 | **0** |
| 3 | 2 | 0, 1 | **2** |

After samples 1 and 2 (codes summing to 8), every element has been used exactly once. Writing each element as $1 + \varepsilon_i$ with $\sum\varepsilon_i = 0$ (errors measured from the mean element), the total error over those two samples is $\sum\varepsilon_i = 0$. Over any run whose codes sum to a multiple of 8 the error cancels, so the error sequence is the first difference of a bounded sequence: first-order noise shaping. After sample 3, elements 0 and 1 have been used twice (**2** elements ahead of the rest).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-09.1a | LSB | 0.610 | mV |
| 20-09.1b | output, code 3000 | 1.831 | V |
| 20-09.1c | resistors | 4096 | — |
| 20-09.2a | output, code 1011 | 0.6875 | V_REF |
| 20-09.2b | output resistance | 1 | R |
| 20-09.3a | unary cells | 31 | — |
| 20-09.3b | LSB per unary cell | 2048 | — |
| 20-09.3c | binary cells | 11 | — |
| 20-09.4a | binary σ(DNL) | 0.256 | LSB |
| 20-09.4b | segmented σ(DNL) | 0.0905 | LSB |
| 20-09.5a | σ_u, mid-scale | 0.260 | % |
| 20-09.5b | σ_u, exact | 0.215 | % |
| 20-09.6a | unit area | 21.2 | µm² |
| 20-09.6b | total area | 0.348 | mm² |
| 20-09.6c | area ratio to Example 3 | 10.2 | — |
| 20-09.7a | unit impedance | 26.2 | MΩ |
| 20-09.7b | HD2 | −66.2 | dBc |
| 20-09.8a | HD2 estimate | −52.0 | dBc |
| 20-09.8b | HD3 estimate | −104.1 | dBc |
| 20-09.8c | HD2 exact | −52.1 | dBc |
| 20-09.8d | HD3 exact | −104.2 | dBc |
| 20-09.9a | droop | −2.42 | dB |
| 20-09.9b | image | −5.94 | dB |
| 20-09.9c | image below signal | 3.52 | dB |
| 20-09.10a | NRZ variation | 3.92 | dB |
| 20-09.10b | RZ variation | 0.91 | dB |
| 20-09.11a | mixed mode at 0.7 fs | −2.83 | dB |
| 20-09.11b | NRZ at 0.7 fs | −8.69 | dB |
| 20-09.11c | advantage | 5.86 | dB |
| 20-09.12a | binary glitch | 49.9 | pV·s |
| 20-09.12b | segmented glitch | 6.15 | pV·s |
| 20-09.13a | time constant | 0.152 | µs |
| 20-09.13b | bandwidth | 1.05 | MHz |
| 20-09.14a | pointer after sample 1 | 3 | — |
| 20-09.14b | pointer after sample 2 | 0 | — |
| 20-09.14c | pointer after sample 3 | 2 | — |
| 20-09.14d | elements used twice | 2 | — |
