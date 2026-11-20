# Course 12 · Final Exam Solutions (Electronics II)

Exam: [README.md](README.md). Every number below is recomputed by [verify_12_exam.py](../verify/verify_12_exam.py), which solves the circuits by nodal analysis, root finding and numerical integration rather than reusing these formulas.

---

## Solutions

### Solution 1

(a) Each device carries 100 µA, so $g_m = \sqrt{2 \times 2\ \text{mA/V}^2 \times 100\ \mu\text{A}}$ = **0.6325** mA/V, and the differential-output gain is $g_mR_D$ = **6.325**.

(b) Single-ended differential gain $g_mR_D/2$ = **3.162**; common-mode gain $g_mR_D/(1 + 2g_mR_{SS})$ = **0.04961** (inverting; the shortcut $R_D/(2R_{SS})$ gives **0.05**); CMRR = **63.75**, or **36.09** dB.

(c) The pair fully switches at $\lvert v_{id}\rvert = \sqrt{2I_{SS}/k}$ = **0.4472** V.

(d) With zero input, a resistor mismatch $\Delta R_D$ produces $I_D\Delta R_D$ of differential output; referred to the input through $g_mR_D$ it is $V_{OS} = (I_D/g_m)(\Delta R_D/R_D) = (V_{ov}/2)(\Delta R_D/R_D)$. Here $V_{ov} = \sqrt{2I_D/k}$ = 0.3162 V and, relative to the mean resistance, $\Delta R_D/R_D$ = 0.02/1.01, so $V_{OS}$ = **3.131** mV (taking 2% of either resistor instead changes the answer by 1%, well within such an estimate).

### Solution 2

(a) $g_m(r_{o2} \parallel r_{o4}) = 1\ \text{mA/V} \times 50\ \text{k}\Omega$ ≈ **50**. (A full nodal solution of the OTA, with every $r_o$ including the diode-connected mirror device's, gives **49.75**.)

(b) Each cascode side: $2r_o + g_mr_o^2$ = **10.2** MΩ; the two sides in parallel give **5.1** MΩ. With the output shorted, the input device's signal current divides between its cascode, which offers about $1/g_m$, and its own $r_o$, so the short-circuit transconductance is $g_m \cdot (g_m + 1/r_o)/(g_m + 2/r_o)$ = **0.9902** mA/V, and the gain is $G_mR_{out}$ = **5050** (the approximation $g_mR_{out}$ = 5100 is 1% high).

### Solution 3

(a) The midband gain is $-g_mR_L$, of magnitude **10** (inverting). $C_{in} = C_{gs} + C_{gd}(1 + 10)$ = **320** fF, so the input pole is near $1/(2\pi \times 10\ \text{k}\Omega \times 320\ \text{fF})$ = **49.74** MHz.

(b) $C_{out} = C_L + C_{gd}(1 + 1/10)$ = **122** fF, so the output pole is near $1/(2\pi \times 5\ \text{k}\Omega \times 122\ \text{fF})$ = **260.9** MHz. The zero is at $g_m/(2\pi C_{gd})$ = **15.92** GHz.

(c) The poles are 18.6 times apart, so the input pole is dominant and the −3 dB frequency (44.01 MHz) sits just below it (44.14 MHz). The Miller estimate of that pole is **13.0**% high because it leaves out the output node's time constant: the dominant pole is about $1/b_1$, and $b_1$ contains the output node's $R_L(C_L + C_{gd})$ = **0.6** ns out of **3.8** ns (Question 4), which the input-side Miller capacitance does not capture. OCTC, which keeps it, lands **4.8**% low.

### Solution 4

(a) $R_{gd} = R_S + R_L + g_mR_SR_L$ = **115** kΩ. $b_1 = 10\ \text{k}\Omega \times 100\ \text{fF} + 115\ \text{k}\Omega \times 20\ \text{fF} + 5\ \text{k}\Omega \times 100\ \text{fF}$ = **3.8** ns, so $1/(2\pi b_1)$ = **41.88** MHz, within 5% of the exact 44.01 MHz and conservative (the poles are real), closer than the Miller estimate. $C_{gd}$ contributes **60.5**% of $b_1$.

(b) The cascode device's source presents $R_x = 1/g_{m2}$ = 500 Ω. Now $C_{gd}$ sees $R_S + R_x + g_mR_SR_x$ = **20.5** kΩ; the time constants are 1 ns ($C_{gs}$), 0.41 ns ($C_{gd}$), 0.06 ns ($C_x$) and $5\ \text{k}\Omega \times 120\ \text{fF}$ = 0.6 ns at the output, so $b_1$ = **2.07** ns and the estimate is **76.89** MHz: the cascode removed most of the Miller term, and the input node now dominates.

### Solution 5

(a) $T = 2000 \times 0.05$ = **100**; $A_f = 2000/101$ = **19.80**.

(b) Series mixing: $R_{in} \approx 10\ \text{k}\Omega \times 101$ = **1.01** MΩ. Shunt sampling: $R_{out} \approx 1\ \text{k}\Omega/101$ = **9.901** Ω. Bandwidth $50\ \text{kHz} \times 101$ = **5.05** MHz.

(c) Replace the amplifier's internal source by an independent one behind $R_o$, with the input zeroed. The inverting node sees $R_1 \parallel R_{in}$ = 909.1 Ω, and the loaded divider returns $(R_1 \parallel R_{in})/(R_o + R_2 + R_1 \parallel R_{in})$ of the source voltage, so $T = 2000 \times 909.1/20\,909$ = **86.96**, 13% below the unloaded $A\beta$ = 100. Solving the full circuit, the closed-loop gain is **19.77**, the input resistance **0.9633** MΩ and the output resistance **10.83** Ω: the loading costs some loop gain, and the simple estimates of (b) are 5% and 9% optimistic.

### Solution 6

(a) $f_u$ = **5** MHz, $r$ = **1.6**. Solving $\lvert T\rvert = 1$ gives a crossover of **4.385** MHz, where the phase is $-\arctan(438.5) - \arctan(0.5481)$, so PM = **61.40**°.

(b) $Q = 1/\sqrt r$ = **0.7906**, so $\zeta$ = 0.6325 and the overshoot is **7.69**%.

### Solution 7

(a) $C_c = 0.22 \times 3\ \text{pF}$ = **0.66** pF; GBW $= 0.4\ \text{mA/V}/(2\pi \times 0.66\ \text{pF})$ = **96.46** MHz; $p_2 \approx 4\ \text{mA/V}/(2\pi \times 3\ \text{pF})$ = **212.2** MHz; zero at $4\ \text{mA/V}/(2\pi \times 0.66\ \text{pF})$ = **964.6** MHz.

(b) $1/g_{m2}$ = **250** Ω removes the zero; $(1 + C_L/C_c)/g_{m2}$ = **1386** Ω cancels $p_2$.

(c) The DC gain is $g_{m1}R_1 \cdot g_{m2}R_2 = 160 \times 400$ = 64 000. Solving the two-node circuit at unity gain gives a crossover of **86.72** MHz and a phase margin of **59.17**°; the exact non-dominant pole is **180.2** MHz, below the 212.2 MHz estimate because $C_1$ adds to node 2's effective capacitance in the split. The rules of 12-06 landed within a degree of 60°.

### Solution 8

(a) $P_L = 12^2/16$ = **9** W; $P_S = 2 \times 144/(8\pi)$ = **11.46** W; η = **78.54**%.

(b) $V_{op} = 24/\pi$ = **7.639** V; $P_{D,max} = 2 \times 144/(8\pi^2)$ = **3.648** W total, **1.824** W per transistor. $\theta_{SA} \le (125 - 50)/1.824 - 3$ = **38.12** °C/W for each transistor on its own heat sink. On one shared sink, the sink carries 3.648 W and each junction sits $1.824 \times 3$ °C above it: $50 + 3.648\,\theta_{SA} + 5.472 \le 125$, so $\theta_{SA} \le$ **19.06** °C/W.

### Solution 9

(a) $g_{m1} = I_{SS}/V_{ov}$ = **200** µA/V; GBW $= g_{m1}/(2\pi C_c)$ = **15.92** MHz.

(b) Internal $I_{SS}/C_c$ = **20** V/µs. On the falling edge the PMOS M6 cuts off, and the sink $I_7$ discharges $C_L$ while the first stage still pushes $I_{SS}$ through $C_c$ into the output: $(I_7 - I_{SS})/C_L$ = **13.75** V/µs. (If node 1 clamped at its rail, the bound would be $I_7/(C_L + C_c)$ = **15** V/µs.) Rising edges are input-limited (20 V/µs), falling edges output-limited (13.75 V/µs). Full-power bandwidth at 2 V peak, set by the slower edge: $13.75\ \text{V/µs}/(2\pi \times 2\ \text{V})$ = **1.094** MHz.

### Solution 10

(a) $C_1C_2/(C_1 + C_2)$ = 0.8 nF, so $f_0 = 1/(2\pi\sqrt{4.7\ \mu\text{H} \times 0.8\ \text{nF}})$ = **2.596** MHz; $g_m \ge (C_2/C_1)/R$ = **2.667** mA/V.

(b) $f = 1/(2 \times 9 \times 25\ \text{ps})$ = **2.222** GHz.

(c) The crystal runs at $f_s\sqrt{1 + C_m/(C_0 + C_L)}$: **454.4** ppm above $f_s$ with 8 pF and **384.5** ppm with 10 pF, so the 2 pF change pulls it by **69.90** ppm (about 1.4 kHz at 20 MHz).

### Solution 11

(a) $R_{eq} = \gamma/g_m + 1/(g_m^2R_D) = 66.67 + 10$ = **76.67** Ω; $e_n = \sqrt{4kTR_{eq}}$ = **1.127** nV/√Hz; over 1 MHz, **1.127** µV RMS.

(b) $\sqrt{kT/2\ \text{pF}}$ = **45.51** µV.

### Solution 12

(a) With the source at the standard $T_0$ = 290 K, $4kT_0R_s$ = 1.602 × 10⁻¹⁷, $e_n^2$ = 9 × 10⁻¹⁸ and $(i_nR_s)^2$ = 2.5 × 10⁻¹⁹ V²/Hz, so $F$ = **1.578** and NF = **1.980** dB.

(b) $R_{opt} = e_n/i_n$ = **6** kΩ, where $F_{min} = 1 + e_ni_n/(2kT_0)$ = **1.187**, NF = **0.7457** dB.

### Solution 13

(a) Close the loop, $s_c = Px$: then $x = cu + dPx$, so $x = cu/(1 - dP)$ and $y = au + bPcu/(1 - dP)$. Define the return ratio $T = -dP$ (the loop gain at the source), the direct transmission $A_{\mathrm{dir}} = a$ (gain with $P = 0$), and the asymptotic gain $A_\infty = a - bc/d$ (gain as $P \to \infty$, forcing $x \to 0$). Then $A_\infty T + A_{\mathrm{dir}} = (a - bc/d)(-dP) + a = a(1 - dP) + bcP$, and dividing by $1 + T = 1 - dP$ gives $a + bcP/(1 - dP)$, the closed-loop gain. ∎

(b) Each transistor carries a half-sine of peak $V_{op}/R_L$, whose average over a cycle is $V_{op}/(\pi R_L)$, so $P_S = 2V_{CC}V_{op}/(\pi R_L)$ and $\eta = P_L/P_S = (\pi/4)(V_{op}/V_{CC})$, at most π/4 at $V_{op} = V_{CC}$. The dissipation $P_D = 2V_{CC}V_{op}/(\pi R_L) - V_{op}^2/(2R_L)$ is maximized where $dP_D/dV_{op} = 0$: $V_{op} = 2V_{CC}/\pi$.

(c) KCL at node 1 and node 2, with the input's current source omitted (it does not affect the denominator):

$$
\Big(\frac{1}{R_1} + s(C_1 + C_c)\Big)V_1 - sC_cV_2 = 0, \qquad (g_{m2} - sC_c)V_1 + \Big(\frac{1}{R_2} + s(C_2 + C_c)\Big)V_2 = 0 .
$$

The determinant, multiplied by $R_1R_2$, is $1 + s\big[R_1(C_1 + C_c) + R_2(C_2 + C_c) + g_{m2}R_1R_2C_c\big] + s^2R_1R_2\big[(C_1 + C_c)(C_2 + C_c) - C_c^2\big]$, so

$$
b_1 = R_1\big[C_1 + C_c(1 + g_{m2}R_2)\big] + R_2(C_c + C_2), \qquad b_2 = R_1R_2\big[C_1C_2 + C_c(C_1 + C_2)\big] .
$$

For well-separated real poles, $p_1 \approx 1/b_1$ and $p_2 \approx b_1/b_2$. When the Miller term $g_{m2}R_1R_2C_c$ dominates $b_1$, $p_1 \approx 1/(g_{m2}R_1R_2C_c)$ and $p_2 \approx g_{m2}R_1R_2C_c/b_2 = g_{m2}C_c/[C_1C_2 + C_c(C_1 + C_2)]$: a larger $C_c$ pushes $p_1$ down and $p_2$ up (toward $g_{m2}/(C_1 + C_2)$), which is pole splitting. ∎

### Solution 14

(a) $g_m = 1\ \mu\text{A}/25.852\ \text{mV}$ = **38.68** µA/V, so $e_n = \sqrt{2kT/g_m}$ = **14.63** nV/√Hz for one ideal transistor. The claim is **857** times lower in power, and a single transistor would need about 857 × 1 µA = **0.857** mA to reach 0.5 nV/√Hz. A rail-to-rail input is at least a differential pair: sharing 1 µA, each device runs at 0.5 µA ($g_m$ = **19.34** µA/V, **20.70** nV/√Hz each), and the pair's input-referred noise is √2 times one device's, **29.27** nV/√Hz, **3426** times the claim in power. For a transistor input stage at 300 K with no passive voltage gain (such as a transformer) ahead of it, the claim is physically impossible.

(b) Rubric (any two, 2 points each, each with its exposing question):

- The noise was measured in a separate high-current mode, and 1 µA is a different (low-power) mode: "What is the supply current at the operating point where 0.5 nV/√Hz was measured?"
- "1 µA" is an average over a duty cycle, with the amplifier on only part of the time: "What is the current while it is actually amplifying, and what is the duty cycle?"
- The figure is referred to an input that sits behind passive voltage gain (a transformer or a sensor's own gain), or the gain used to refer it is overstated: "Referred to which node, and through what gain, measured how?"
- It is a simulated or typical value, or a unit slip (nV for µV, a density quoted as if integrated): "Is it measured, on how many parts, and what is the integrated noise from 0.1 Hz to 1 MHz?"

(c) Rubric (4 points for three of): the integrated noise over the stated bandwidth, including 1/f; the current noise $i_n$ with the sensor's source impedance; the supply current at the noise operating point; the measurement conditions (temperature, gain, source resistance); and, for a rail-to-rail input, the noise across the common-mode range, where the two pairs hand over (12-08).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X12.1a | g_m | 0.6325 | mA/V |
| X12.1b | differential-output gain | 6.325 | — |
| X12.1c | single-ended differential gain | 3.162 | — |
| X12.1d | common-mode gain magnitude | 0.04961 | — |
| X12.1e | CMRR | 36.09 | dB |
| X12.1g | shortcut common-mode gain | 0.05 | — |
| X12.1h | CMRR ratio | 63.75 | — |
| X12.1f | full-switching input | 0.4472 | V |
| X12.1i | offset from 2% R_D mismatch | 3.131 | mV |
| X12.2a | five-transistor OTA gain | 50 | — |
| X12.2b | cascode side resistance | 10.2 | MΩ |
| X12.2c | total output resistance | 5.1 | MΩ |
| X12.2d | telescopic gain | 5050 | — |
| X12.2e | OTA gain, full nodal solution | 49.75 | — |
| X12.2f | cascoded input transconductance | 0.9902 | mA/V |
| X12.2g | approximate telescopic gain | 5100 | — |
| X12.3a | midband gain | 10 | — |
| X12.3b | Miller input capacitance | 320 | fF |
| X12.3c | input-pole estimate | 49.74 | MHz |
| X12.3d | output capacitance | 122 | fF |
| X12.3e | output-pole estimate | 260.9 | MHz |
| X12.3f | zero | 15.92 | GHz |
| X12.3g | exact −3 dB | 44.01 | MHz |
| X12.4a | resistance seen by C_gd | 115 | kΩ |
| X12.4b | b_1 | 3.8 | ns |
| X12.4c | bandwidth estimate | 41.88 | MHz |
| X12.4d | C_gd's share | 60.5 | % |
| X12.4e | R_gd with the cascode | 20.5 | kΩ |
| X12.4f | b_1 with the cascode | 2.07 | ns |
| X12.4g | estimate with the cascode | 76.89 | MHz |
| X12.3h | Miller estimate's excess | 13.0 | % |
| X12.3i | output-node time constant | 0.6 | ns |
| X12.3j | OCTC shortfall | 4.8 | % |
| X12.3k | exact input pole | 44.14 | MHz |
| X12.3l | exact output pole | 819.8 | MHz |
| X12.3m | pole ratio | 18.6 | — |
| X12.5a | loop gain | 100 | — |
| X12.5b | closed-loop gain | 19.80 | — |
| X12.5c | input resistance | 1.01 | MΩ |
| X12.5d | output resistance | 9.901 | Ω |
| X12.5e | bandwidth | 5.05 | MHz |
| X12.5f | exact return ratio | 86.96 | — |
| X12.5g | exact closed-loop gain | 19.77 | — |
| X12.5h | exact input resistance | 0.9633 | MΩ |
| X12.5i | exact output resistance | 10.83 | Ω |
| X12.6a | f_u | 5 | MHz |
| X12.6b | r | 1.6 | — |
| X12.6c | crossover | 4.385 | MHz |
| X12.6d | phase margin | 61.40 | ° |
| X12.6e | Q | 0.7906 | — |
| X12.6f | damping ratio | 0.6325 | — |
| X12.6g | overshoot | 7.69 | % |
| X12.7a | C_c | 0.66 | pF |
| X12.7b | GBW | 96.46 | MHz |
| X12.7c | p_2 | 212.2 | MHz |
| X12.7d | zero | 964.6 | MHz |
| X12.7e | R_z removing the zero | 250 | Ω |
| X12.7f | R_z cancelling p_2 | 1386 | Ω |
| X12.7g | exact crossover | 86.72 | MHz |
| X12.7h | exact phase margin | 59.17 | ° |
| X12.7i | exact p_2 | 180.2 | MHz |
| X12.8a | maximum output power | 9 | W |
| X12.8b | supply power | 11.46 | W |
| X12.8c | efficiency | 78.54 | % |
| X12.8d | worst-case amplitude | 7.639 | V |
| X12.8e | total worst dissipation | 3.648 | W |
| X12.8f | per-transistor dissipation | 1.824 | W |
| X12.8g | largest θ_SA | 38.12 | °C/W |
| X12.8h | largest θ_SA, shared sink | 19.06 | °C/W |
| X12.9a | g_m1 | 200 | µA/V |
| X12.9b | GBW | 15.92 | MHz |
| X12.9c | internal slew limit | 20 | V/µs |
| X12.9d | output slew limit | 13.75 | V/µs |
| X12.9e | full-power bandwidth | 1.094 | MHz |
| X12.9f | output bound with node 1 clamped | 15 | V/µs |
| X12.10a | Colpitts frequency | 2.596 | MHz |
| X12.10b | minimum g_m | 2.667 | mA/V |
| X12.10d | offset with 8 pF | 454.4 | ppm |
| X12.10e | offset with 10 pF | 384.5 | ppm |
| X12.10f | pulling | 69.90 | ppm |
| X12.10c | ring frequency | 2.222 | GHz |
| X12.11a | equivalent noise resistance | 76.67 | Ω |
| X12.11b | input noise density | 1.127 | nV/√Hz |
| X12.11c | RMS over 1 MHz | 1.127 | µV |
| X12.11d | kT/C at 2 pF | 45.51 | µV |
| X12.12a | noise factor | 1.578 | — |
| X12.12b | noise figure | 1.980 | dB |
| X12.12c | optimum source resistance | 6 | kΩ |
| X12.12d | minimum noise factor | 1.187 | — |
| X12.12e | minimum noise figure | 0.7457 | dB |
| X12.14a | g_m at 1 µA | 38.68 | µA/V |
| X12.14b | minimum noise density | 14.63 | nV/√Hz |
| X12.14c | power ratio to the claim | 857 | — |
| X12.14d | current for 0.5 nV/√Hz | 0.857 | mA |
| X12.14e | g_m per pair device | 19.34 | µA/V |
| X12.14f | noise per pair device | 20.70 | nV/√Hz |
| X12.14g | pair noise | 29.27 | nV/√Hz |
| X12.14h | pair's power ratio to the claim | 3426 | — |
