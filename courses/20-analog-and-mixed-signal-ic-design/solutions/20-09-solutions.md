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

### Solution 20-09.15

(a) Looking left from node $k$, the source resistance $R_{k-1}$ of the ladder to the left plus the series R is in parallel with node $k$'s leg $2R + r$:

$$
R_k = \frac{(R_{k-1} + R)(2R + r)}{R_{k-1} + 3R + r} .
$$

At the fixed point $R_k = R_{k-1} = R^*$: $R^*(R^* + 3R + r) = (R^* + R)(2R + r)$, which simplifies to $R^{*2} + RR^* - (2R^2 + rR) = 0$, so

$$
R^* = \frac{R}{2}\left(-1 + \sqrt{9 + 4\varepsilon}\right) \approx \frac{R}{2}\left(-1 + 3 + \frac{2\varepsilon}{3}\right) = R\left(1 + \frac{\varepsilon}{3}\right) ,
$$

using $\sqrt{9 + 4\varepsilon} \approx 3 + 2\varepsilon/3$. For ε = 0.01, $R^*$ = **1.00333** R. (The recursion converges quickly from any starting value, so a few nodes from the termination the ladder already looks like this.)

(b) Node $k$ joins two Thévenin sources: the left ladder ($V_{k-1}$ behind $R^* + R$) and its own leg ($b_kV_{REF}$ behind $2R + r$). By superposition,

$$
V_k = \underbrace{\frac{2R + r}{R^* + 3R + r}}_{a}V_{k-1} + \underbrace{\frac{R^* + R}{R^* + 3R + r}}_{c}b_kV_{REF} .
$$

To first order, $a \approx (2 + \varepsilon)/(4 + 4\varepsilon/3) \approx \tfrac12(1 + \varepsilon/2)(1 - \varepsilon/3) \approx \tfrac12(1 + \varepsilon/6)$ and $c \approx (2 + \varepsilon/3)/(4 + 4\varepsilon/3) \approx \tfrac12(1 - \varepsilon/6)$. Exactly, for ε = 0.01: $a$ = **0.500831**, $c$ = **0.499169**.

(c) Bit $k$ reaches the output (node $N - 1$) with weight $w_k = c\,a^{N-1-k}$. The MSB has $w_{N-1} = c$; the lower bits sum to $c(a + a^2 + \cdots) \approx c\,a/(1 - a) \approx c(1 + \varepsilon/3)$ for many bits, using $a/(1 - a) \approx (1 + \varepsilon/6)/(1 - \varepsilon/6) \approx 1 + \varepsilon/3$. Ideally the lower bits sum to one LSB less than the MSB; here they exceed the ideal by about $(\varepsilon/3)w_{N-1}$, and $w_{N-1} \approx 2^{N-1}$ LSB. The major-carry step is therefore short by that amount:

$$
\text{DNL}_{carry} \approx -\frac{\varepsilon}{3}\,2^{N-1}\ \text{LSB}.
$$

N = 10: **−1.71** LSB, against the nodal **−1.68** LSB of Example 20-09.1 (the estimate ignores the termination and the finite ladder). N = 8: **−0.43** LSB (nodal **−0.41**). The error doubles per bit, which is why switch resistance matters most in high-resolution ladders.

(d) Make each leg $2R - r$, so that leg plus switch is exactly 2R and the 2:1 ratio holds at every node; $a = c = \tfrac12$ exactly.

### Solution 20-09.16

(a) $N_t = 2^{14} - 1$ = 16383: $\sigma_u \le 0.5/(1.818\sqrt{16383})$ = **0.215**%.

(b) The worst step has $\sigma_{DNL} = \sigma_u\sqrt{2^{B+1} - 1}$ with $B = 14 - M$. For ≤ 0.1 LSB: $2^{B+1} - 1 \le (0.1/0.002149)^2$ = 2166, so $B + 1 \le 11$ and $B \le 10$: $M \ge$ **4** (M = 4 gives 0.0972 LSB; M = 3 gives 0.138 LSB). The decoder allows $2^M - 1 \le 63$, so $M \le$ **6**. Any of M = 4, 5, 6 meets both; more unary bits lower the glitch energy and the DNL further at the cost of a larger decoder, so high-speed designs usually take the upper end.

(c) $WL = [\sqrt2A_{VT}/(V_{ov}\sigma_u)]^2 = [\sqrt2 \times 3\ \text{mV·µm}/(0.4\ \text{V} \times 0.002149)]^2$ = **24.4** µm² per unit. Segmentation does not change the number of units, 16383, so the sources occupy **0.399** mm²: a large analog block, which is why high-resolution designs turn to calibration or DEM instead of relying on area alone (the calibration row of the chapter's §6).

(d) The differential HD3 estimate $(xN_t)^2/16 \le 10^{-70/20}$ gives $xN_t \le 4 \times 10^{-70/40}$ = **0.0711**, a per-unit $x = R_L/\lvert Z_u\rvert$ = 4.34 × 10⁻⁶ and $\lvert Z_u\rvert \ge$ **5.76** MΩ at 500 MHz, which is the impedance of **55.3** aF. But the code-dependent capacitance belongs to cells, not units: with $m$ unary cells on, the output is $m\,2^BI_uR_L/(1 + mR_L/Z_{cell})$, which is the unit model with $x = (R_L/Z_{cell})/2^B$. A cell of $2^B = 256$ units may therefore have $C_{cell} \le 256 \times 55.3$ aF = **14.2** fF, an achievable value for a cascoded switch pair. A fully unary or binary design spreading the same capacitance over units would need each unit far below a femtofarad. (A check with the capacitive $x = j\omega CR_L$ and the full harmonic analysis gives −70.0 dBc at this capacitance, within 0.1 dB of the estimate.)

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
| 20-09.15a | fixed-point resistance | 1.00333 | R |
| 20-09.15b | fraction passed, a | 0.500831 | — |
| 20-09.15c | own-bit weight, c | 0.499169 | — |
| 20-09.15d | carry DNL estimate, 10 bits | −1.71 | LSB |
| 20-09.15e | carry DNL, 10 bits, nodal | −1.68 | LSB |
| 20-09.15f | carry DNL estimate, 8 bits | −0.43 | LSB |
| 20-09.15g | carry DNL, 8 bits, nodal | −0.41 | LSB |
| 20-09.16a | unit sigma | 0.215 | % |
| 20-09.16b | minimum unary bits | 4 | — |
| 20-09.16c | maximum unary bits | 6 | — |
| 20-09.16d | unit area | 24.4 | µm² |
| 20-09.16e | total source area | 0.399 | mm² |
| 20-09.16f | xN_t bound | 0.0711 | — |
| 20-09.16g | unit impedance | 5.76 | MΩ |
| 20-09.16h | unit capacitance | 55.3 | aF |
| 20-09.16i | cell capacitance | 14.2 | fF |
