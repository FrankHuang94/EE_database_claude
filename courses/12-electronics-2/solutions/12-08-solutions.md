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

Internal: $50\ \mu\text{A}/2\ \text{pF}$ = **25** V/µs. Output stage, on the edge where M6 cuts off (falling, for the chapter's NMOS pair and PMOS M6): $(200 - 50)\ \mu\text{A}/10\ \text{pF}$ = **15.00** V/µs. Rising edges are input-limited (25 V/µs); falling edges are output-limited (15.00 V/µs). Balancing needs $(I_7 - 50\ \mu\text{A})/10\ \text{pF} = 25$ V/µs, so $I_7$ = **300** µA.

### Solution 12-08.7

$R_{up} = 100\ \text{k} + 50\ \text{k} + 1\ \text{mA/V} \times 100\ \text{k}\Omega \times 50\ \text{k}\Omega$ = **5.15** MΩ; $R_{dn} = 200\ \text{k} + 1\ \text{mA/V} \times (100\ \text{k}\Omega)^2$ = **10.2** MΩ; $R_{out}$ = **3.422** MΩ, and the estimated gain is $g_{m1}R_{out}$ = **3422** (**70.69** dB).

### Solution 12-08.8

GBW $= 1\ \text{mA/V}/(2\pi \times 3\ \text{pF})$ = **53.05** MHz. The folding node's pole is at $1\ \text{mA/V}/(2\pi \times 0.4\ \text{pF})$ = **397.9** MHz, so PM ≈ $90^\circ - \arctan(53.05/397.9)$ = **82.41**°.

### Solution 12-08.9

$\Delta I = 0.5\%$ of 100 µA = 0.5 µA, so $\Delta V_{CM} = 0.5\ \mu\text{A} \times 3.422\ \text{M}\Omega$ = **1.711** V: the outputs hit a rail. With CMFB the loop gain is $0.2\ \text{mA/V} \times 3.422\ \text{M}\Omega$ = **684.4**, and the error falls to $1.711\ \text{V}/685.4$ = **2.496** mV.

### Solution 12-08.10

The NMOS pair needs $V_{CM} \ge 0.6 + 0.2 + 0.2$ = **1.0** V; the PMOS pair needs $V_{CM} \le 3.3 - 1.0$ = **2.3** V. Both conduct from 1.0 to 2.3 V, where $g_m$ is **2** times its value near either rail; a constant-$g_m$ circuit would quarter each pair's current there.

### Solution 12-08.11

$C_c = 0.22 \times 4$ = **0.88** pF. $g_{m1} = 2\pi \times 20\ \text{MHz} \times 0.88\ \text{pF}$ = **110.6** µA/V, so $g_{m6}$ = **1.106** mA/V. At 0.2 V overdrive, $I_{SS} = g_{m1}V_{ov}$ = **22.12** µA (each input device carries half) and $I_7 = g_{m6}V_{ov}/2$ = **110.6** µA. Slew limits: $I_{SS}/C_c$ = **25.13** V/µs internal (rising) and $(I_7 - I_{SS})/C_L$ = **22.12** V/µs at the output (falling).

### Solution 12-08.12

$R_1 = 1/(0.1 \times 11.06\ \mu\text{A})/2$ = **452.1** kΩ and $R_2 = 1/(0.1 \times 110.6\ \mu\text{A})/2$ = **45.21** kΩ, so the gain is $(110.6\ \mu\text{A/V} \times 452.1\ \text{k}\Omega)(1.106\ \text{mA/V} \times 45.21\ \text{k}\Omega) = 50 \times 50$ = **2500**. The crossover sits below $g_{m1}/(2\pi C_c)$ because the non-dominant pole, only 2.2 times above it, already lowers the magnitude there: the same effect as in Example 12-06.1. To reach 20 MHz of actual crossover, raise $g_{m1}$ and $g_{m6}$ together by about **13**% (found by solving the circuit again at scaled transconductances).

### Solution 12-08.13

KCL at node 1 and at the output, with the capacitor currents written in terms of the two node voltages' rates:

$$
(C_1 + C_c)\dot v_1 - C_c\dot v_o = I_{SS}, \qquad -C_c\dot v_1 + (C_L + C_c)\dot v_o = -I_7 .
$$

The determinant is $\Delta = C_1C_L + C_1C_c + C_cC_L$ = 0.2 × 5 + 0.2 × 1.1 + 1.1 × 5 = **6.72** pF². By Cramer's rule,

$$
\dot v_o = -\frac{(C_1 + C_c)I_7 - C_cI_{SS}}{\Delta} = -\frac{1.3 \times 100 - 1.1 \times 20}{6.72}\ \frac{\mu\text{A}}{\text{pF}} = \mathbf{-16.07}\ \text{V/µs},
\qquad
\dot v_1 = \frac{(C_L + C_c)I_{SS} - C_cI_7}{\Delta} = \mathbf{1.786}\ \text{V/µs} .
$$

(µA/pF is V/µs.) Node 1 drifts up slowly while the output falls. As $C_1 \to 0$, $\dot v_o \to -(C_cI_7 - C_cI_{SS})/(C_cC_L) = -(I_7 - I_{SS})/C_L$ = −16.00 V/µs; as $C_1 \to \infty$, node 1 is pinned and $\dot v_o \to -I_7/(C_L + C_c)$ = −16.39 V/µs. The 0.2 pF case sits between, close to the free-node bound because $C_1 \ll C_c$.

### Solution 12-08.14

(a) Every $V_{GS}$ is $V_{TH} + V_{ov}$ = 0.7 V. The tail source needs its drain at least $V_{ov}$ = 0.2 V above ground, so $V_{CM} \ge V_{GS1} + 0.2$ = **0.9** V. M1's drain sits at the mirror's gate–drain node, $V_{DD} - V_{SG3}$ = 1.1 V, and M1 stays saturated while its gate is no more than $V_{TN}$ above its drain: $V_{CM} \le 1.1 + 0.5$ = **1.6** V. The range is 0.7 V wide, inside a 1.8 V supply.

(b) M7 needs $v_{out} \ge V_{ov7}$ = **0.2** V and M6 needs $v_{out} \le V_{DD} - V_{ov6}$ = **1.6** V.

(c) The improved non-dominant pole is $g_{m6}C_c/[2\pi(C_1C_L + C_c(C_1 + C_L))]$ = **26.05** MHz, the zero is at 144.7 MHz and $g_{m1}/(2\pi C_c)$ = 14.47 MHz, so PM ≈ $90^\circ - \arctan(14.47/26.05) - \arctan(14.47/144.7)$ = **55.24**°. At the exact crossover, 12.70 MHz, the same formula gives **59.0**°, within a degree of the exact 59.78°: most of the hand estimate's error comes from taking the crossover at $g_{m1}/C_c$, which the non-dominant pole pulls down (12-06 Example 1).

### Solution 12-08.15

(a) $\Delta V_{CM} = 0.005 \times 50\ \mu\text{A} \times 5.175\ \text{M}\Omega$ = **1.294** V: more than the output can swing, so without CMFB the outputs would simply rail. Holding 1 mV needs $1 + T \ge 1294$, so $T \ge$ **1293** and $g_{m,cm} \ge 1293/5.175\ \text{M}\Omega$ = **0.2499** mA/V.

(b) For differential signals the centre node is an AC ground, so each 1 MΩ resistor appears directly in parallel with that output's 5.175 MΩ: $R_{out}$ falls to **0.838** MΩ, and the differential gain to **16.20**% of its value (**−15.81** dB). Resistive sensing works only if the resistors are much larger than $R_{out}$, which is impractical at megohms, or if the outputs are first buffered by source followers, which costs headroom. In sampled-data circuits, switched-capacitor sensing draws no DC current and is the usual answer; in continuous-time circuits, a separate differential pair per output that compares each output with $V_{CM}$ avoids loading the outputs at all.

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
| 12-08.6b | output-stage limit | 15.00 | V/µs |
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
| 12-08.11e | I_7 | 110.6 | µA |
| 12-08.11f | internal slew limit | 25.13 | V/µs |
| 12-08.11g | output slew limit | 22.12 | V/µs |
| 12-08.13a | capacitance determinant | 6.72 | pF² |
| 12-08.13b | output slew rate | −16.07 | V/µs |
| 12-08.13c | node-1 rate | 1.786 | V/µs |
| 12-08.14a | lowest input common mode | 0.9 | V |
| 12-08.14b | highest input common mode | 1.6 | V |
| 12-08.14c | lowest output | 0.2 | V |
| 12-08.14d | highest output | 1.6 | V |
| 12-08.14e | improved p_2 | 26.05 | MHz |
| 12-08.14f | hand phase-margin estimate | 55.24 | ° |
| 12-08.14g | estimate at the exact crossover | 59.0 | ° |
| 12-08.15a | common-mode shift | 1.294 | V |
| 12-08.15b | loop gain needed | 1293 | — |
| 12-08.15c | CMFB transconductance | 0.2499 | mA/V |
| 12-08.15d | loaded output resistance | 0.838 | MΩ |
| 12-08.15e | remaining differential gain | 16.20 | % |
| 12-08.15f | gain loss | −15.81 | dB |
| 12-08.12a | R_1 | 452.1 | kΩ |
| 12-08.12b | R_2 | 45.21 | kΩ |
| 12-08.12c | DC gain | 2500 | — |
| 12-08.12d | exact phase margin | 59.97 | ° |
| 12-08.12e | exact crossover | 17.59 | MHz |
| 12-08.12f | g_m increase for a 20 MHz crossover | 13 | % |
| 12-08.12g | current per input device | 11.06 | µA |
