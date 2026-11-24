# Solutions 21-11 · Link Budgets

Problems: [21-11 problem set](../problems/21-11-problems.md) · Chapter: [21-11](../chapters/21-11-link-budgets.md). Every number below is recomputed by [verify_21_11.py](../verify/verify_21_11.py).

---

## Solutions

### Solution 21-11.1

(a) 20 − 2 + 3 = **21** dBm.

(b) 21 − 110 − 8 + 0 − 1 = **−98** dBm.

(c) −98 − (−95) = **−3** dB: the link does not close even with zero margin.

(d) It is **9** dB short of the design. Each line has an owner: 3 dB from a better antenna, 2 dB from a lower-loss switch, and so on, or a lower data rate.

### Solution 21-11.2

Each dB multiplies the range by $10^{1/(10n)}$:

- (a) **12.2** %, (b) **8.0** %, (c) **5.9** %.
- (d) $10^{6/20}$ = **2.00**, (e) $10^{6/30}$ = **1.58**, (f) $10^{6/40}$ = **1.41**.

The 6 dB that doubles free-space range buys only 41% more range at $n$ = 4.

### Solution 21-11.3

(a) $-174 + 60 + 12 + 7$ = **−95.0** dBm. (b) $-174 + 50.97 + 12 + 7$ = **−104.03** dBm.

(c) $(2^{0.1} - 1)/0.1$ = 0.718: **−1.44** dB. (d) $(2^4 - 1)/4$ = 3.75: **5.74** dB.

### Solution 21-11.4

(a) $234 \times 6 \times \tfrac56/13.6\ \mu\text{s}$ = **86.0** Mb/s.

(b) **18** dB. (c) $10\log_{10}(86.03/8.603)$ = **10.00** dB; the other 8 dB is the higher $E_b/N_0$ that 64-QAM needs.

### Solution 21-11.5

(a) $6 \times Q^{-1}(0.05) = 6 \times 1.6449$ = **9.87** dB. (b) $-10\log_{10}(-\ln 0.95)$ = **12.90** dB.

(c) Numerically, **16.55** dB. (d) **22.77** dB.

### Solution 21-11.6

$b = 39.08\log_{10}e/(6\sqrt2)$ = 2.000. Jakes's formula gives (a) **97.4** % and (b) **98.8** %.

### Solution 21-11.7

$-10\log_{10}(1 - \eta)$: (a) **1.55** dB, (b) **3.98** dB, (c) **10** dB. Loading a cell beyond about 75% costs disproportionately in uplink coverage.

### Solution 21-11.8

(a) $2 + 0.7$ = **2.7** dB. (b) $5 + 14$ = **19.0** dB. (c) $25.4 + 0.385$ = **25.79** dB.

(d) $5 - 10\log_{10}(0.3 \times 10^{-0.27} + 0.7 \times 10^{-1.9})$ = **12.70** dB.

(e) $5 - 10\log_{10}(0.7 \times 10^{-2.579} + 0.3 \times 10^{-1.9})$ = **27.50** dB. (f) **14.80** dB.

Energy-efficient coated windows cost a 3.5 GHz indoor user about 15 dB, the difference between good and no indoor coverage.

### Solution 21-11.9

(a) $10^{3/39.08}$ = **1.19**. (b) $1.193^2$ = **1.42**. (c) $1 - 1/1.424$ = **29.8** %.

### Solution 21-11.10

(a) $-174 + 10\log_{10}3750 + 5$ = **−133.26** dBm.

(b) −141 − (−133.26) = **−7.74** dB.

(c) $10^{(1 + 7.74)/10}$ = 7.5, so **8** repetitions: the narrower subcarrier saves 6 dB of noise and a factor of 4 in repetitions.

### Solution 21-11.11

(a) $12 \times 10\,400/4096 \times 0.8$ = **24.4** b/s. (b) $12 \times 125\,000/4096 \times 0.8$ = **293** b/s.

(c) 22 + 148 = **170** dB. (d) 22 + 137 = **159** dB. (e) $10^{11/35}$ = **2.06**.

The headline budget buys twice the range at one-twelfth of the rate.

### Solution 21-11.12

(a) −7 − 190.6 − 5.3 + 19 + 228.6 = **44.7** dBHz. (b) 44.7 − 55.56 = **−10.9** dB: no useful uplink from a handheld to a geostationary satellite without a much larger satellite antenna or a much narrower channel.

### Solution 21-11.13

(a) $\lambda$ = 0.1578 m; $10\log_{10}(\lambda^2/4\pi)$ = **−27.03** dB(m²).

(b) −120 − 27.03 + 30 = **−117.03** dBm/MHz. (c) **−107.63** dBm/MHz.

(d) **−9.03** dB. (e) **0.37** dB. (f) **−2.63** dB.

At the limit the interference raises the noise floor by about 0.5 dB; at the waiver, with no polarization loss, it doubles it. Each side's conclusion follows from which antenna gain, polarization and noise figure it assumes.

### Solution 21-11.14

(a) −128.5 + 174 − 3 = **42.5** dBHz. (b) 42.5 − 63.01 = **−20.51** dB.

(c) $10\log_{10}1023$ = **30.10** dB.

(d) A 20 ms coherent integration has a 50 Hz bandwidth: 42.5 − 16.99 = **25.51** dB.

### Solution 21-11.15

(a) $1 - 0.999^{368}$ = **30.8** %. (b) $1 - (1 - 0.00017)^{2112}$ = **30.2** %. (c) **2112** bits.

The specification lowers the BER for longer packets so that the packet-error rate at sensitivity stays near 30%.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-11.1a | EIRP | 21 | dBm |
| 21-11.1b | received power | −98 | dBm |
| 21-11.1c | margin over sensitivity | −3 | dB |
| 21-11.1d | shortfall | 9 | dB |
| 21-11.2a | range gain per dB, n = 2 | 12.2 | % |
| 21-11.2b | range gain per dB, n = 3 | 8.0 | % |
| 21-11.2c | range gain per dB, n = 4 | 5.9 | % |
| 21-11.2d | range factor of 6 dB, n = 2 | 2.00 | |
| 21-11.2e | range factor of 6 dB, n = 3 | 1.58 | |
| 21-11.2f | range factor of 6 dB, n = 4 | 1.41 | |
| 21-11.3a | sensitivity, 1 Mb/s | −95.0 | dBm |
| 21-11.3b | sensitivity, 125 kb/s | −104.03 | dBm |
| 21-11.3c | Shannon Eb/N0, 0.1 b/s/Hz | −1.44 | dB |
| 21-11.3d | Shannon Eb/N0, 4 b/s/Hz | 5.74 | dB |
| 21-11.4a | MCS7 rate | 86.0 | Mb/s |
| 21-11.4b | sensitivity difference | 18 | dB |
| 21-11.4c | rate ratio | 10.00 | dB |
| 21-11.5a | shadowing margin, 5 % | 9.87 | dB |
| 21-11.5b | Rayleigh margin, 5 % | 12.90 | dB |
| 21-11.5c | combined margin, 5 % | 16.55 | dB |
| 21-11.5d | naive sum | 22.77 | dB |
| 21-11.6a | area coverage, 90 % edge | 97.4 | % |
| 21-11.6b | area coverage, 95 % edge | 98.8 | % |
| 21-11.7a | noise rise, 30 % | 1.55 | dB |
| 21-11.7b | noise rise, 60 % | 3.98 | dB |
| 21-11.7c | noise rise, 90 % | 10 | dB |
| 21-11.8a | standard glass | 2.7 | dB |
| 21-11.8b | concrete | 19.0 | dB |
| 21-11.8c | IRR glass | 25.79 | dB |
| 21-11.8d | low-loss building | 12.70 | dB |
| 21-11.8e | high-loss building | 27.50 | dB |
| 21-11.8f | difference | 14.80 | dB |
| 21-11.9a | radius factor | 1.19 | |
| 21-11.9b | area factor | 1.42 | |
| 21-11.9c | sites saved | 29.8 | % |
| 21-11.10a | noise in 3.75 kHz | −133.26 | dBm |
| 21-11.10b | required SNR | −7.74 | dB |
| 21-11.10c | repetitions | 8 | |
| 21-11.11a | SF12 rate, 10.4 kHz | 24.4 | b/s |
| 21-11.11b | SF12 rate, 125 kHz | 293 | b/s |
| 21-11.11c | budget, 10.4 kHz | 170 | dB |
| 21-11.11d | budget, 125 kHz | 159 | dB |
| 21-11.11e | range ratio | 2.06 | |
| 21-11.12a | GEO uplink C/N0 | 44.7 | dBHz |
| 21-11.12b | GEO uplink CNR | −10.9 | dB |
| 21-11.13a | isotropic aperture | −27.03 | dB(m²) |
| 21-11.13b | received power at the limit | −117.03 | dBm/MHz |
| 21-11.13c | received power at the waiver | −107.63 | dBm/MHz |
| 21-11.13d | I/N at the limit | −9.03 | dB |
| 21-11.13e | I/N at the waiver | 0.37 | dB |
| 21-11.13f | I/N at the waiver with polarization loss | −2.63 | dB |
| 21-11.14a | C/N0 | 42.5 | dBHz |
| 21-11.14b | SNR in 2 MHz | −20.51 | dB |
| 21-11.14c | processing gain of 1023 chips | 30.10 | dB |
| 21-11.14d | SNR after 20 ms | 25.51 | dB |
| 21-11.15a | PER, 37-byte payload | 30.8 | % |
| 21-11.15b | PER, 255-byte payload | 30.2 | % |
| 21-11.15c | counted bits, 255-byte payload | 2112 | |
