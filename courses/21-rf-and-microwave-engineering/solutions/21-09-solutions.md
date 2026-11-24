# Solutions 21-09 · The RF Front End: Filters, Switches and Modules

Problems: [21-09 problem set](../problems/21-09-problems.md) · Chapter: [21-09](../chapters/21-09-rf-front-end.md). Every number below is recomputed by [verify_21_09.py](../verify/verify_21_09.py).

---

## Solutions

### Solution 21-09.1

(a) $f_p = f_s\sqrt{1 + 1/15}$ = 1.8 × 1.03280 = **1.8590** GHz.

(b) $C_m = C_0/15$ = **100.0** fF.

(c) $L_m = 1/[(2\pi f_s)^2C_m] = 1/[(1.131 \times 10^{10})^2 \times 10^{-13}]$ = **78.18** nH.

(d) $R_m = 2\pi f_sL_m/Q = (1.131 \times 10^{10} \times 78.18 \times 10^{-9})/1500$ = **0.589** Ω.

Units: s²/F = H; rad/s × H = Ω.

### Solution 21-09.2

With $x = (\pi/2)(3.50/3.60)$ = 1.5272 rad:

(a) $k^2_{eff} = x\cot x$ = **6.67** %.

(b) $(\pi^2/4)(0.10/3.60)$ = **6.85** %.

(c) $r = 1/[(f_p/f_s)^2 - 1] = 1/(1.05796 - 1)$ = **17.25**.

The two coupling figures differ by 3% here; at higher coupling the gap widens (§8).

### Solution 21-09.3

(a) Solving $k^2_{eff}$ = 0.075 for $f_p/f_s$ gives a spacing of **3.24** %.

(b) The notches sit about one spacing below and above the centre (§3.2), so the pass band is at most $2 \times 0.03237 \times 2593$ = **167.9** MHz wide.

(c) **No**: the band needs 194 MHz.

(d) The spacing must reach $194/(2 \times 2593)$ = 3.74%, which needs $k^2_{eff}$ = **8.59** %.

In practice designers widen ladders with added inductors, accepting some loss and rejection, or move to higher-coupling films (§9).

### Solution 21-09.4

(a) $f_{s,sh} = f_p/\sqrt{1 + 1/20}$ = 2.45/1.02470 = **2.3910** GHz.

(b–d) Cascade the four ABCD matrices (series, shunt, series, shunt) at each frequency and take $S_{21} = 2/(A + B/Z_0 + CZ_0 + D)$ (lab `frontend.py`):

- (b) insertion loss at 2.45 GHz **0.334** dB;
- (c) rejection at 2.30 GHz **18.71** dB;
- (d) rejection at 2.60 GHz **19.46** dB.

Two sections give only about 19 dB of rejection 150 MHz from the band; the chapter's three-section ladder gives about 32 dB at 120 MHz. Each added section buys rejection at the cost of loss.

### Solution 21-09.5

(a) $\Delta f = 1.9 \times 10^9 \times (-15 \times 10^{-6}) \times 115$ = **−3.28** MHz.

(b) 3.28/20 = **16.4** %.

(c) $0.25 \times 20 \times 10^6/(1.9 \times 10^9 \times 115)$ = **22.9** ppm/°C.

### Solution 21-09.6

(a) 26 + 2.5 = **28.5** dBm.

(b) 28.5 − 52 = **−23.5** dBm.

(c) −20 − (−23.5) = **3.5** dB: little headroom, so the LNA's linearity (and the receive filter's rejection of the transmit band ahead of it) must be designed for this leakage.

(d) $-138 - L \le -174 + 2.5 - 6$ gives $L \ge$ **39.5** dB.

### Solution 21-09.7

(a, b) **26** and **25** dBm: 398.1 and 316.2 mW.

(c, d) 398.1/0.35 = **1137.4** mW and 316.2/0.35 = **903.5** mW.

(e) **233.9** mW.

(f) 0.3 × 233.9 = **70.2** mW.

(g) 70.2 mW/3.85 V = **18.2** mA.

One decibel of filter loss costs about 18 mA of average battery current at this duty cycle, plus the heat in the PA and the filter.

### Solution 21-09.8

(a) 1.5 Ω × 80 fF = **120** fs.

(b) $1/(2\pi \times 1.2 \times 10^{-13})$ = **1.33** THz.

(c) $20\log_{10}(1 + 1.5/100)$ = **0.129** dB.

(d) $x = 2Z_0\omega C_{off}$ = 100 × 2π × 3.5 × 10⁹ × 80 × 10⁻¹⁵ = 0.1759, so the isolation is $10\log_{10}(1 + 1/x^2)$ = **15.23** dB.

### Solution 21-09.9

(a) $P$ = 398.1 mW, so $V = \sqrt{2 \times 50 \times 0.3981}$ = **6.31** V.

(b) $\lvert\Gamma\rvert$ = 3/5 = 0.6, so the worst case is 6.31 × 1.6 = **10.10** V.

(c) 10.10/2.4 = 4.21, so **5** transistors.

(d) N transistors, each N times wider: area grows by $N^2$ = **25**.

### Solution 21-09.10

(a) $R_{on} = 2Z_0(10^{0.2/20} - 1)$ = **2.33** Ω.

(b) $C_{off} = 150\ \text{fs}/2.33\ \Omega$ = **64.4** fF.

(c) $x = 100 \times 2\pi \times 2.7 \times 10^9 \times 64.4 \times 10^{-15}$ = 0.1093, isolation **19.28** dB.

(d) $C_{off}$ = 42.9 fF, $x$ = 0.0728, isolation **22.78** dB: a 1.5× better figure of merit buys 3.5 dB of isolation at the same loss, $20\log_{10}1.5$ = 3.5 dB, because isolation is set by $x \propto C_{off}$ when $x \ll 1$.

### Solution 21-09.11

(a) $\lvert\Gamma\rvert$ = 0.6: $-10\log_{10}(0.64)$ = **1.94** dB.

(b) $\lvert\Gamma\rvert$ = 1/3: **0.51** dB.

(c) $1 - \lvert\Gamma\rvert^2 = 10^{-0.1}$ gives $\lvert\Gamma\rvert$ = **0.4535**.

(d) VSWR = 1.4535/0.5465 = **2.66**.

### Solution 21-09.12

(a) $\lvert\Gamma\rvert$ = 2/3: **2.55** dB. (b) **0.51** dB.

(c) Tuning pays while its loss is below 2.55 − 0.51 = **2.04** dB.

(d) 2.04 − 0.6 = **1.44** dB.

### Solution 21-09.13

(a) $2f_1 - f_2$ = 3490 − 1950 = **1540** MHz. (b) $2f_2 - f_1$ = 3900 − 1745 = **2155** MHz: inside the receive channel.

(c) For equal tones, $P_{IM3} = 3P - 2\,\text{IIP3}$ (21-03): 60 − 130 = **−70** dBm.

(d) $-174 + 10\log_{10}(10^7) + 4$ = **−100** dBm.

(e) $3 \times 20 - 2\,\text{IIP3} \le -106$ gives IIP3 ≥ **83** dBm.

A switch IIP3 above 80 dBm is a demanding specification; it is one reason uplink carrier-aggregation combinations are scheduled, filtered or routed to separate antennas rather than solved by linearity alone.

### Solution 21-09.14

(a) 0.67 × 4,086.9 = **2,738** $M. (b) 0.61 × 3,959.6 = **2,415** $M.

(c) **−323** $M; (d) **−11.8** %.

(e) 4,086.9 − 2,738.2 = **1,349** $M; (f) 3,959.6 − 2,415.4 = **1,544** $M; (g) **+14.5** %.

(h, i) A whole-percent share is uncertain by ±0.5 percentage point: ±**20.4** $M in fiscal 2025 and ±**19.8** $M in fiscal 2026. The Apple decline is far larger than the rounding; the non-Apple growth is real but less precisely known than the headline suggests.

### Solution 21-09.15

(a) $\lambda/2 = 11{,}000/(2 \times 3.5 \times 10^9)$ = **1.57** µm.

(b) $\lambda/4 = c/(4f\sqrt{\varepsilon_{eff}}) = 3 \times 10^8/(4 \times 3.5 \times 10^9 \times 2.449)$ = **8.75** mm.

(c) About **5,570** times.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-09.1a | anti-resonance | 1.8590 | GHz |
| 21-09.1b | motional capacitance | 100.0 | fF |
| 21-09.1c | motional inductance | 78.18 | nH |
| 21-09.1d | motional resistance | 0.589 | Ω |
| 21-09.2a | exact k²_eff | 6.67 | % |
| 21-09.2b | approximate k² | 6.85 | % |
| 21-09.2c | capacitance ratio | 17.25 | |
| 21-09.3a | resonance spacing | 3.24 | % |
| 21-09.3b | pass-band upper bound | 167.9 | MHz |
| 21-09.3d | k²_eff needed | 8.59 | % |
| 21-09.4a | shunt series resonance | 2.3910 | GHz |
| 21-09.4b | insertion loss | 0.334 | dB |
| 21-09.4c | rejection at 2.30 GHz | 18.71 | dB |
| 21-09.4d | rejection at 2.60 GHz | 19.46 | dB |
| 21-09.5a | drift | −3.28 | MHz |
| 21-09.5b | share of the gap | 16.4 | % |
| 21-09.5c | TCF for 25 % | 22.9 | ppm/°C |
| 21-09.6a | PA output | 28.5 | dBm |
| 21-09.6b | leakage at the LNA | −23.5 | dBm |
| 21-09.6c | compression margin | 3.5 | dB |
| 21-09.6d | receive-band isolation | 39.5 | dB |
| 21-09.7a | PA output, 3 dB filter | 26 | dBm |
| 21-09.7b | PA output, 2 dB filter | 25 | dBm |
| 21-09.7c | DC power, 3 dB filter | 1137.4 | mW |
| 21-09.7d | DC power, 2 dB filter | 903.5 | mW |
| 21-09.7e | extra DC power | 233.9 | mW |
| 21-09.7f | extra average power | 70.2 | mW |
| 21-09.7g | extra average current | 18.2 | mA |
| 21-09.8a | figure of merit | 120 | fs |
| 21-09.8b | cut-off frequency | 1.33 | THz |
| 21-09.8c | on-state loss | 0.129 | dB |
| 21-09.8d | isolation at 3.5 GHz | 15.23 | dB |
| 21-09.9a | matched peak voltage | 6.31 | V |
| 21-09.9b | worst-case peak voltage | 10.10 | V |
| 21-09.9c | transistors | 5 | |
| 21-09.9d | area factor | 25 | |
| 21-09.10a | R_on | 2.33 | Ω |
| 21-09.10b | C_off | 64.4 | fF |
| 21-09.10c | isolation, 150 fs | 19.28 | dB |
| 21-09.10d | isolation, 100 fs | 22.78 | dB |
| 21-09.11a | mismatch loss, VSWR 4 | 1.94 | dB |
| 21-09.11b | mismatch loss, VSWR 2 | 0.51 | dB |
| 21-09.11c | reflection magnitude for 1 dB | 0.4535 | |
| 21-09.11d | VSWR for 1 dB | 2.66 | |
| 21-09.12a | mismatch loss, VSWR 5 | 2.55 | dB |
| 21-09.12b | mismatch loss, VSWR 2 | 0.51 | dB |
| 21-09.12c | break-even tuner loss | 2.04 | dB |
| 21-09.12d | net gain | 1.44 | dB |
| 21-09.13a | 2f1 − f2 | 1540 | MHz |
| 21-09.13b | 2f2 − f1 | 2155 | MHz |
| 21-09.13c | IM3 level | −70 | dBm |
| 21-09.13d | noise floor | −100 | dBm |
| 21-09.13e | IIP3 needed | 83 | dBm |
| 21-09.14a | Apple revenue FY2025 | 2738 | $M |
| 21-09.14b | Apple revenue FY2026 | 2415 | $M |
| 21-09.14c | change | −323 | $M |
| 21-09.14d | change | −11.8 | % |
| 21-09.14e | non-Apple FY2025 | 1349 | $M |
| 21-09.14f | non-Apple FY2026 | 1544 | $M |
| 21-09.14g | non-Apple change | 14.5 | % |
| 21-09.14h | rounding uncertainty FY2025 | 20.4 | $M |
| 21-09.14i | rounding uncertainty FY2026 | 19.8 | $M |
| 21-09.15a | AlN thickness | 1.57 | µm |
| 21-09.15b | quarter-wave line | 8.75 | mm |
| 21-09.15c | ratio | 5570 | |
