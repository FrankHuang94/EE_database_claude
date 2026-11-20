# Solutions 12-08 · Op-Amp Internals

Problems: [12-08 problems](../problems/12-08-problems.md) · Chapter: [12-08](../chapters/12-08-op-amp-internals.md). Every number below is recomputed by [verify_12_08.py](../verify/verify_12_08.py), which solves the amplifiers by complex nodal analysis and finds output resistances by test-current injection rather than reusing these formulas.

---

## Solutions

### Solution 12-08.1

$A_1 = 0.2\ \text{mA/V} \times 400\ \text{k}\Omega$ = **80**; $A_2 = 2\ \text{mA/V} \times 40\ \text{k}\Omega$ = **80**; total **6400**, or **76.12** dB.

### Solution 12-08.2

SR $= 50\ \mu\text{A}/2\ \text{pF}$ = **25** V/µs, so 2 V takes **80** ns.

### Solution 12-08.3

$f_{FP} = 10\ \text{V/µs}/(2\pi \times 2\ \text{V})$ = **795.8** kHz.

### Solution 12-08.4

$\text{SR} = \omega_uV_{ov1} = 2\pi \times 20\ \text{MHz} \times 0.15\ \text{V}$ = **18.85** V/µs for the MOS pair; $2\pi \times 20\ \text{MHz} \times 2V_T$ = **6.497** V/µs for the bipolar pair.

### Solution 12-08.5

$\text{SR}/\omega_u = 2V_T(1 + g_mR_E)$, so quadrupling needs $g_mR_E$ = 3. With $g_m = 50\ \mu\text{A}/25.852\ \text{mV}$ = **1.934** mA/V, $R_E$ = **1551** Ω. The cost: the pair's effective transconductance falls by 4, so the GBW falls by 4 unless $C_c$ is cut by 4 (which keeps the GBW and raises the slew rate fourfold); the resistors also add thermal noise and some offset.

### Solution 12-08.6

Internal: $50\ \mu\text{A}/2\ \text{pF}$ = **25** V/µs. Output stage: $200\ \mu\text{A}/12\ \text{pF}$ = **16.67** V/µs. Rising edges are output-limited (16.67 V/µs); falling edges are input-limited (25 V/µs). Balancing needs $I_7 = 25\ \text{V/µs} \times 12\ \text{pF}$ = **300** µA.

### Solution 12-08.7

$R_{up} = 100\ \text{k} + 50\ \text{k} + 1\ \text{mA/V} \times 100\ \text{k}\Omega \times 50\ \text{k}\Omega$ = **5.15** MΩ; $R_{dn} = 200\ \text{k} + 1\ \text{mA/V} \times (100\ \text{k}\Omega)^2$ = **10.2** MΩ; $R_{out}$ = **3.422** MΩ, and the estimated gain is $g_{m1}R_{out}$ = **3422** (**70.69** dB).

### Solution 12-08.8

GBW $= 1\ \text{mA/V}/(2\pi \times 3\ \text{pF})$ = **53.05** MHz. The folding node's pole is at $1\ \text{mA/V}/(2\pi \times 0.4\ \text{pF})$ = **397.9** MHz, so PM ≈ $90^\circ - \arctan(53.05/397.9)$ = **82.41**°.

### Solution 12-08.9

$\Delta I = 0.5\%$ of 100 µA = 0.5 µA, so $\Delta V_{CM} = 0.5\ \mu\text{A} \times 3.422\ \text{M}\Omega$ = **1.711** V: the outputs hit a rail. With CMFB the loop gain is $0.2\ \text{mA/V} \times 3.422\ \text{M}\Omega$ = **684.4**, and the error falls to $1.711\ \text{V}/685.4$ = **2.496** mV.

### Solution 12-08.10

The NMOS pair needs $V_{CM} \ge 0.6 + 0.2 + 0.2$ = **1.0** V; the PMOS pair needs $V_{CM} \le 3.3 - 1.0$ = **2.3** V. Both conduct from 1.0 to 2.3 V, where $g_m$ is **2** times its value near either rail; a constant-$g_m$ circuit would quarter each pair's current there.

### Solution 12-08.11

$C_c = 0.22 \times 4$ = **0.88** pF. $g_{m1} = 2\pi \times 20\ \text{MHz} \times 0.88\ \text{pF}$ = **110.6** µA/V, so $g_{m6}$ = **1.106** mA/V. At 0.2 V overdrive, $I_{SS} = g_{m1}V_{ov}$ = **22.12** µA (each input device carries half) and $I_6 = g_{m6}V_{ov}/2$ = **110.6** µA. Slew limits: $I_{SS}/C_c$ = **25.13** V/µs internal and $I_6/(C_L + C_c)$ = **22.66** V/µs at the output.

### Solution 12-08.12

$R_1 = 1/(0.1 \times 11.06\ \mu\text{A})/2$ = **452.1** kΩ and $R_2 = 1/(0.1 \times 110.6\ \mu\text{A})/2$ = **45.21** kΩ, so the gain is $(110.6\ \mu\text{A/V} \times 452.1\ \text{k}\Omega)(1.106\ \text{mA/V} \times 45.21\ \text{k}\Omega) = 50 \times 50$ = **2500**. The crossover sits below $g_{m1}/(2\pi C_c)$ because the non-dominant pole, only 2.2 times above it, already lowers the magnitude there: the same effect as in Example 12-06.1. To reach 20 MHz of actual crossover, raise $g_{m1}$ and $g_{m6}$ together by about **13**% (found by solving the circuit again at scaled transconductances).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 12-08.1a | first-stage gain | 80 | — |
| 12-08.1b | second-stage gain | 80 | — |
| 12-08.1c | total gain | 6400 | — |
| 12-08.1d | total gain | 76.12 | dB |
| 12-08.2a | slew rate | 25 | V/µs |
| 12-08.2b | time for 2 V | 80 | ns |
| 12-08.3a | full-power bandwidth | 795.8 | kHz |
| 12-08.4a | MOS slew rate | 18.85 | V/µs |
| 12-08.4b | bipolar slew rate | 6.497 | V/µs |
| 12-08.5a | g_m | 1.934 | mA/V |
| 12-08.5b | emitter resistor | 1551 | Ω |
| 12-08.6a | internal limit | 25 | V/µs |
| 12-08.6b | output-stage limit | 16.67 | V/µs |
| 12-08.6c | balancing I_7 | 300 | µA |
| 12-08.7a | R_up | 5.15 | MΩ |
| 12-08.7b | R_dn | 10.2 | MΩ |
| 12-08.7c | R_out | 3.422 | MΩ |
| 12-08.7d | estimated gain | 3422 | — |
| 12-08.7e | estimated gain | 70.69 | dB |
| 12-08.8a | GBW | 53.05 | MHz |
| 12-08.8b | folding-node pole | 397.9 | MHz |
| 12-08.8c | estimated phase margin | 82.41 | ° |
| 12-08.9a | common-mode shift | 1.711 | V |
| 12-08.9b | CMFB loop gain | 684.4 | — |
| 12-08.9c | residual error | 2.496 | mV |
| 12-08.10a | NMOS pair lower limit | 1.0 | V |
| 12-08.10b | PMOS pair upper limit | 2.3 | V |
| 12-08.10c | g_m ratio | 2 | — |
| 12-08.11a | C_c | 0.88 | pF |
| 12-08.11b | g_m1 | 110.6 | µA/V |
| 12-08.11c | g_m6 | 1.106 | mA/V |
| 12-08.11d | I_SS | 22.12 | µA |
| 12-08.11e | I_6 | 110.6 | µA |
| 12-08.11f | internal slew limit | 25.13 | V/µs |
| 12-08.11g | output slew limit | 22.66 | V/µs |
| 12-08.12a | R_1 | 452.1 | kΩ |
| 12-08.12b | R_2 | 45.21 | kΩ |
| 12-08.12c | DC gain | 2500 | — |
| 12-08.12d | exact phase margin | 59.97 | ° |
| 12-08.12e | exact crossover | 17.59 | MHz |
| 12-08.12f | g_m increase for a 20 MHz crossover | 13 | % |
| 12-08.12g | current per input device | 11.06 | µA |
