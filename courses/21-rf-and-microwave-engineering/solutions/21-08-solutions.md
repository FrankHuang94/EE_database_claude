# Solutions 21-08 · Transceiver Architectures

Problems: [21-08 problem set](../problems/21-08-problems.md) · Chapter: [21-08](../chapters/21-08-transceiver-architectures.md). Every number below is recomputed by [verify_21_08.py](../verify/verify_21_08.py).

---

## Solutions

### Solution 21-08.1

(a) Low side: $f_{LO} = f_{RF} - f_{IF}$ = **1.7** GHz. (b) The image is the other input that lands on the IF: $f_{LO} - f_{IF}$ = **1.5** GHz, $2f_{IF}$ below the wanted signal.

### Solution 21-08.2

$x = (1.9/0.06)(1.5/1.9 - 1.9/1.5)$ = −15.11, so each order adds about $20\log_{10}15.11$ = 23.6 dB: (a) **23.60** dB, (b) **47.17** dB, (c) **70.76** dB, and (d) order **3** meets 50 dB.

### Solution 21-08.3

(a) LO1 = 5.8 + 1.2 = **7.0** GHz; (b) image1 = 5.8 + 2.4 = **8.2** GHz.

(c) LO2 = 1.2 − 0.01 = **1.19** GHz; (d) image2 = 1.19 − 0.01 = **1.18** GHz, just 20 MHz from the first IF.

(e) $x = (1.2/0.02)(1.18/1.2 - 1.2/1.18)$ = −2.017, so a second-order filter gives $10\log_{10}(1 + 2.017^4)$ = **12.44** dB. (f) About 6 dB per order: order **10**. The second image must instead be handled by a narrower first-IF filter, a higher second IF, or an image-reject (quadrature) second mixer.

### Solution 21-08.4

(a, b) $\lvert 3f_{LO} - f_{RF}\rvert = f_{IF}$ gives $f_{RF}$ = 5.1 ∓ 0.2 = **4.9** and **5.3** GHz; the preselector removes them easily.

(c, d) With a low-side LO, $2f_{RF} - 2f_{LO} = \pm f_{IF}$ gives $f_{RF} = f_{LO} \pm f_{IF}/2$ = **1.8** and **1.6** GHz.

(e) At 1.8 GHz the third-order preselector gives only **32.09** dB; (f) at 1.6 GHz, **62.34** dB. The spur 100 MHz from the wanted signal relies on the mixer's balance.

### Solution 21-08.5

(a) EVM = $10^{-35/20}$ = **1.78** %. (b) Errors add in power: $(1.78/2.5)^2$ = **50.6** % of the budget, half of it gone before noise, phase noise and the PA.

### Solution 21-08.6

Integrate $S(f)$ from $f_1$ = 10 kHz to the channel edge $B$: the noise is $S_0[(B - f_1) + f_c\ln(B/f_1)]$, so flicker raises it by

$$
10\log_{10}\left(1 + \frac{f_c\ln(B/f_1)}{B - f_1}\right) .
$$

(a) For $B$ = 1 MHz: **2.86** dB. (b) For 100 MHz: **0.08** dB. Flicker noise hurts narrow channels (Bluetooth, IoT) and barely touches wide ones (Wi-Fi, 5G), which is part of why low-IF suits the former and zero-IF the latter.

### Solution 21-08.7

$P_{IM2} = 2P - \text{IIP2} \le -106$ dBm gives IIP2 ≥ 2(−30) + 106 = **46** dBm.

### Solution 21-08.8

(a) 25 + 12 = **37** dB.

(b, c) $\varepsilon = \theta = \sqrt{2 \times 10^{-3.7}}$: ε = **2.00** %, θ = **1.14**°.

(d) $2f_{IF}/f_p$ = 4: $10\log_{10}(1 + 4^8)$ = **48.16** dB.

### Solution 21-08.9

$f_s/2$ = 1.5 GHz.

- 2.45 GHz is in zone (a) **2** (1.5–3.0 GHz), an even zone, so it appears mirrored at 3.0 − 2.45 = (b) **0.55** GHz.
- 5.8 GHz is in zone (c) **4** (4.5–6.0 GHz), also mirrored: 6.0 − 5.8 = (d) **0.2** GHz.

Both bands must be filtered so that nothing else folds onto 0.55 or 0.2 GHz.

### Solution 21-08.10

(a) $\sigma_t = 10^{-60/20}/(2\pi \times 6 \times 10^9)$ = **26.5** fs.

(b) NSD = $-\text{SNR} - 10\log_{10}(f_s/2)$ = −60 − 91.76 = **−151.76** dBFS/Hz.

### Solution 21-08.11

(a) $F = F_1 + (F_{ADC} - 1)/G$ with $F_1 = 10^{0.1}$, $F_{ADC} = 10^{2.5}$, $F = 10^{0.25}$: $G = (316.2 - 1)/(1.778 - 1.259)$ = 607, **27.83** dB.

(b) The ADC tolerates +2 − 6 = −4 dBm, so the LNA input may see −4 − 27.83 = **−31.83** dBm.

(c) A passive filter's loss adds to the noise figure in dB: 1.5 + 2.5 = **4.0** dB. Filtering buys blocker tolerance at 1.5 dB of sensitivity; the alternative is less gain and a worse ADC contribution.

### Solution 21-08.12

(a) $4/(\varepsilon^2 + \theta^2) = 10^4$ with θ = 0.5° = 8.73 mrad: $\varepsilon = \sqrt{4 \times 10^{-4} - 7.6 \times 10^{-5}}$ = **1.80** %.

(b) The exact formula gives **40.06** dB.

### Solution 21-08.13

(a) $N_{TX} - 45 \le -174 + 4 - 6$ gives $N_{TX} \le$ **−131** dBm/Hz; (b) **−157** dBc/Hz relative to 26 dBm.

(c) $-135 - L \le -176$ gives $L \ge$ **41** dB.

### Solution 21-08.14

4 × 4 = 16 cellular chains plus 1 GNSS: **17** receive chains (and, with carriers in different bands, up to four receive LOs).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-08.1a | LO | 1.7 | GHz |
| 21-08.1b | image | 1.5 | GHz |
| 21-08.2a | order 1 | 23.60 | dB |
| 21-08.2b | order 2 | 47.17 | dB |
| 21-08.2c | order 3 | 70.76 | dB |
| 21-08.2d | order needed | 3 | |
| 21-08.3a | LO1 | 7.0 | GHz |
| 21-08.3b | first image | 8.2 | GHz |
| 21-08.3c | LO2 | 1.19 | GHz |
| 21-08.3d | second image | 1.18 | GHz |
| 21-08.3e | IF1 filter at the second image | 12.44 | dB |
| 21-08.3f | order for 60 dB | 10 | |
| 21-08.4a | LO third-harmonic response | 4.9 | GHz |
| 21-08.4b | LO third-harmonic response | 5.3 | GHz |
| 21-08.4c | half-IF spur | 1.8 | GHz |
| 21-08.4d | half-IF spur | 1.6 | GHz |
| 21-08.4e | preselector at 1.8 GHz | 32.09 | dB |
| 21-08.4f | preselector at 1.6 GHz | 62.34 | dB |
| 21-08.5a | EVM floor | 1.78 | % |
| 21-08.5b | share of a 2.5 % budget | 50.6 | % |
| 21-08.6a | flicker penalty, 1 MHz | 2.86 | dB |
| 21-08.6b | flicker penalty, 100 MHz | 0.08 | dB |
| 21-08.7 | IIP2 | 46 | dBm |
| 21-08.8a | IRR | 37 | dB |
| 21-08.8b | gain error | 2.00 | % |
| 21-08.8c | phase error | 1.14 | deg |
| 21-08.8d | complex-filter selectivity | 48.16 | dB |
| 21-08.9a | zone, 2.45 GHz | 2 | |
| 21-08.9b | alias, 2.45 GHz | 0.55 | GHz |
| 21-08.9c | zone, 5.8 GHz | 4 | |
| 21-08.9d | alias, 5.8 GHz | 0.2 | GHz |
| 21-08.10a | jitter for 60 dB at 6 GHz | 26.5 | fs |
| 21-08.10b | NSD | −151.76 | dBFS/Hz |
| 21-08.11a | LNA gain | 27.83 | dB |
| 21-08.11b | largest blocker at the LNA input | −31.83 | dBm |
| 21-08.11c | NF with the filter | 4.0 | dB |
| 21-08.12a | gain error | 1.80 | % |
| 21-08.12b | exact sideband suppression | 40.06 | dB |
| 21-08.13a | allowed TX noise | −131 | dBm/Hz |
| 21-08.13b | allowed TX noise | −157 | dBc/Hz |
| 21-08.13c | isolation needed | 41 | dB |
| 21-08.14 | receive chains | 17 | |
