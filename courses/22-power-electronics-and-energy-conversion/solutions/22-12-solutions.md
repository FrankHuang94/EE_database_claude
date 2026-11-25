# Solutions 22-12 · Power Systems Fundamentals

Problems: [22-12 problem set](../problems/22-12-problems.md) · Chapter: [22-12](../chapters/22-12-power-systems-fundamentals.md). Every number below is recomputed by [verify_22_12.py](../verify/verify_22_12.py).

---

## Solutions

### Solution 22-12.1

(a) $500^2/500$ = **500** Ω; (b) $500\ \text{MVA}/(\sqrt3 \times 500\ \text{kV})$ = **577** A; (c) $25/500$ = **0.050** pu.

### Solution 22-12.2

$0.15 \times (100/200) \times (20/22)^2$ = **0.0620** pu.

### Solution 22-12.3

$10 \times (138/13.8)^2$ = **1000** Ω: an impedance scales with the square of the turns ratio.

### Solution 22-12.4

(a) $500^2/250$ = **1000** MW; (b) 150 km is a medium line: $1.75 \times 1000$ = **1750** MW.

### Solution 22-12.5

(a) $\sin\delta = 2.0 \times 0.25/(1.02 \times 1.00)$ = 0.490, $\delta$ = **29.4**°.

(b) $(1.02\cos29.4° - 1.00)/0.25$ = **−0.444** pu: bus 2 must *supply* 0.444 pu of reactive power into the line.

(c) $(1.02^2 - 1.02\cos29.4°)/0.25$ = **0.605** pu.

The line absorbs 0.605 + 0.444 = **1.05** pu of reactive power ($I^2X$) to carry 2 pu of real power, which is why heavily loaded lines need reactive support at both ends.

### Solution 22-12.6

(a) $(2 \times 30 + 8 \times 10) \times 10^6/69\,000$ = **2029** V; (b) **2.94** %.

### Solution 22-12.7

(a) $100/5000$ = **0.020** pu; (b) $100/(0.020 + 0.10)$ = **833** MVA; (c) $833\ \text{MVA}/(\sqrt3 \times 13.8\ \text{kV})$ = **34.9** kA. The transformer limits the fault far more than the strong 138 kV source.

### Solution 22-12.8

(a) $1/0.12$ = **8.33** pu; (b) $3/(0.12 + 0.12 + 0.06)$ = **10.0** pu; (c) **1.20**.

### Solution 22-12.9

(a) $3 \times 60/(2 \times 5 \times 100)$ = **0.18** Hz/s; (b) **0.30** Hz/s.

### Solution 22-12.10

$\beta_1 = 300/(0.04 \times 60)$ = 125 MW/Hz and $\beta_2 = 500/(0.05 \times 60)$ = 166.7 MW/Hz. (a) $\Delta f = -80/291.7$ = **−0.274** Hz; (b) $125 \times 0.274$ = **34.3** MW; (c) **45.7** MW. Each unit takes a share proportional to $S/R$, not to $S$ alone.

### Solution 22-12.11

(a) $1500 \times 60/(2 \times 400\,000)$ = **0.1125** Hz/s, upward; (b) $1500/25\,000$ = **0.060** Hz. The frequency rises because load, not generation, was lost.

### Solution 22-12.12

(a) $192/0.047$ = **4085** TWh; (b) $649/0.118$ = **5500** TWh. The projection assumes total US consumption grows by about a third in six years, with datacenters a large part of that growth.

### Solution 22-12.13

$\beta = 2\pi \times 60/(0.979c)$ = 1.284 × 10⁻³ rad/km, so $V_R/V_S = 1/\cos(0.385)$ = **1.079**: an 8% rise at the open end, which is why long lines are switched with shunt reactors.

### Solution 22-12.14

(a) $r' = e^{-1/4} \times 14$ mm = **10.90** mm. (b) $L = (\mu_0/2\pi)\ln(D/r') = 2 \times 10^{-7}\ln(7.0/0.01090)$ = 1.293 µH/m = **1.293** mH/km; (c) $X = 2\pi \times 60 \times 1.293$ mH = **0.487** Ω/km. (d) $C = 2\pi\varepsilon_0/\ln(D/r) = 55.63\ \text{pF/m}/\ln 500$ = 8.95 pF/m = **8.95** nF/km. (e) $Z_c = \sqrt{L/C}$ = **380** Ω; (f) SIL $= (230\ \text{kV})^2/380\ \Omega$ = **139** MW. These match the typical 230 kV values in §7: a single conductor of this size is what such a line uses.

### Solution 22-12.15

The base current at 230 kV is 251.0 A.

(a) $I_f = 1/0.30$ = **3.33** pu = **837** A. (b) $3/(0.30 + 0.30 + 0.15)$ = **4.00** pu = **1004** A. (c) $I_1 = 1/(Z_1 + Z_2) = -j1.667$ pu, and $I_b = (a^2 - a)I_1 = -j\sqrt3I_1$, so $\lvert I_b\rvert = \sqrt3/0.60$ = **2.89** pu = **725** A, 0.866 of the three-phase value. (d) $Z_2Z_0/(Z_2 + Z_0)$ = j0.10, so $I_1 = 1/(\text{j}0.30 + \text{j}0.10) = -\text{j}2.50$; the current divides as $I_2 = -I_1Z_0/(Z_2 + Z_0) = +\text{j}0.833$ and $I_0 = -I_1Z_2/(Z_2 + Z_0) = +\text{j}1.667$. Then $I_b = I_0 + a^2I_1 + aI_2$, whose magnitude is **3.82** pu = **959** A. (e) The ground carries $3I_0$: **5.00** pu = **1255** A. With $Z_0 < Z_1$ both ground faults exceed the three-phase fault, and the double-line-to-ground fault puts the largest current into the ground.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-12.1a | impedance base | 500 | Ω |
| 22-12.1b | current base | 577 | A |
| 22-12.1c | line impedance | 0.050 | pu |
| 22-12.2 | new per-unit reactance | 0.0620 | pu |
| 22-12.3 | referred impedance | 1000 | Ω |
| 22-12.4a | SIL | 1000 | MW |
| 22-12.4b | loadability | 1750 | MW |
| 22-12.5a | angle | 29.4 | ° |
| 22-12.5b | reactive power arriving at bus 2 | −0.444 | pu |
| 22-12.5c | reactive power leaving bus 1 | 0.605 | pu |
| 22-12.5d | reactive power absorbed by the line | 1.05 | pu |
| 22-12.6a | voltage drop | 2029 | V |
| 22-12.6b | voltage drop | 2.94 | % |
| 22-12.7a | source impedance | 0.020 | pu |
| 22-12.7b | fault MVA | 833 | MVA |
| 22-12.7c | fault current | 34.9 | kA |
| 22-12.8a | three-phase fault | 8.33 | pu |
| 22-12.8b | ground fault | 10.0 | pu |
| 22-12.8c | ratio | 1.20 | |
| 22-12.9a | RoCoF, H = 5 s | 0.18 | Hz/s |
| 22-12.9b | RoCoF, H = 3 s | 0.30 | Hz/s |
| 22-12.10a | frequency change | −0.274 | Hz |
| 22-12.10b | 300 MW unit's pickup | 34.3 | MW |
| 22-12.10c | 500 MW unit's pickup | 45.7 | MW |
| 22-12.11a | RoCoF | 0.1125 | Hz/s |
| 22-12.11b | steady frequency rise | 0.060 | Hz |
| 22-12.12a | implied 2024 total | 4085 | TWh |
| 22-12.12b | implied 2030 total | 5500 | TWh |
| 22-12.13 | Ferranti ratio | 1.079 | |
| 22-12.14a | geometric mean radius | 10.90 | mm |
| 22-12.14b | inductance | 1.293 | mH/km |
| 22-12.14c | reactance | 0.487 | Ω/km |
| 22-12.14d | capacitance | 8.95 | nF/km |
| 22-12.14e | characteristic impedance | 380 | Ω |
| 22-12.14f | surge-impedance loading | 139 | MW |
| 22-12.15a | three-phase fault | 3.33 | pu |
| 22-12.15b | three-phase fault | 837 | A |
| 22-12.15c | SLG fault | 4.00 | pu |
| 22-12.15d | SLG fault | 1004 | A |
| 22-12.15e | LL fault | 2.89 | pu |
| 22-12.15f | LL fault | 725 | A |
| 22-12.15g | DLG fault, faulted phase | 3.82 | pu |
| 22-12.15h | DLG fault, faulted phase | 959 | A |
| 22-12.15i | DLG ground current | 5.00 | pu |
| 22-12.15j | DLG ground current | 1255 | A |
