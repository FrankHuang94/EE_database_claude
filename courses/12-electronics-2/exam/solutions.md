# Course 12 · Final Exam Solutions (Electronics II)

Exam: [README.md](README.md). Every number below is recomputed by [verify_12_exam.py](../verify/verify_12_exam.py), which solves the circuits by nodal analysis, root finding and numerical integration rather than reusing these formulas.

---

## Solutions

### Solution 1

(a) Each device carries 100 µA, so $g_m = \sqrt{2 \times 2\ \text{mA/V}^2 \times 100\ \mu\text{A}}$ = **0.6325** mA/V, and the differential-output gain is $g_mR_D$ = **6.325**.

(b) Single-ended differential gain $g_mR_D/2$ = **3.162**; common-mode gain $g_mR_D/(1 + 2g_mR_{SS})$ = **0.04961** (inverting; the shortcut $R_D/(2R_{SS})$ gives **0.05**); CMRR = **63.75**, or **36.09** dB.

(c) The pair fully switches at $\lvert v_{id}\rvert = \sqrt{2I_{SS}/k}$ = **0.4472** V.

### Solution 2

(a) $g_m(r_{o2} \parallel r_{o4}) = 1\ \text{mA/V} \times 50\ \text{k}\Omega$ = **50**.

(b) Each cascode side: $2r_o + g_mr_o^2$ = **10.2** MΩ; the two sides in parallel give **5.1** MΩ, and the gain is $g_mR_{out}$ = **5100**.

### Solution 3

(a) Gain $g_mR_L$ = **10**. $C_{in} = C_{gs} + C_{gd}(1 + 10)$ = **320** fF, so the input pole is near $1/(2\pi \times 10\ \text{k}\Omega \times 320\ \text{fF})$ = **49.74** MHz.

(b) $C_{out} = C_L + C_{gd}(1 + 1/10)$ = **122** fF, so the output pole is near $1/(2\pi \times 5\ \text{k}\Omega \times 122\ \text{fF})$ = **260.9** MHz. The zero is at $g_m/(2\pi C_{gd})$ = **15.92** GHz.

(c) The exact 44.01 MHz is below the Miller input estimate: the Miller approximation assumes the full midband gain across $C_{gd}$ at the input pole, and ignores the output node's contribution; with poles only five times apart, the second pole also lowers the −3 dB point.

### Solution 4

$R_{gd} = R_S + R_L + g_mR_SR_L$ = **115** kΩ. $b_1 = 10\ \text{k}\Omega \times 100\ \text{fF} + 115\ \text{k}\Omega \times 20\ \text{fF} + 5\ \text{k}\Omega \times 100\ \text{fF}$ = **3.8** ns, so $1/(2\pi b_1)$ = **41.88** MHz, within 5% of the exact 44.01 MHz and conservative. $C_{gd}$ contributes **61**% of $b_1$.

### Solution 5

(a) $T = 2000 \times 0.05$ = **100**; $A_f = 2000/101$ = **19.80**.

(b) Series mixing: $R_{in} \approx 10\ \text{k}\Omega \times 101$ = **1.01** MΩ. Shunt sampling: $R_{out} \approx 1\ \text{k}\Omega/101$ = **9.901** Ω. Bandwidth $50\ \text{kHz} \times 101$ = **5.05** MHz.

### Solution 6

(a) $f_u$ = **5** MHz, $r$ = **1.6**. Solving $\lvert T\rvert = 1$ gives a crossover of **4.385** MHz, where the phase is $-\arctan(438.5) - \arctan(0.5481)$, so PM = **61.40**°.

(b) $Q = 1/\sqrt r$ = **0.7906**, so $\zeta$ = 0.6325 and the overshoot is **7.69**%.

### Solution 7

(a) $C_c = 0.22 \times 3\ \text{pF}$ = **0.66** pF; GBW $= 0.4\ \text{mA/V}/(2\pi \times 0.66\ \text{pF})$ = **96.46** MHz; $p_2 \approx 4\ \text{mA/V}/(2\pi \times 3\ \text{pF})$ = **212.2** MHz; zero at $4\ \text{mA/V}/(2\pi \times 0.66\ \text{pF})$ = **964.6** MHz.

(b) $1/g_{m2}$ = **250** Ω removes the zero; $(1 + C_L/C_c)/g_{m2}$ = **1386** Ω cancels $p_2$.

### Solution 8

(a) $P_L = 12^2/16$ = **9** W; $P_S = 2 \times 144/(8\pi)$ = **11.46** W; η = **78.54**%.

(b) $V_{op} = 24/\pi$ = **7.639** V; $P_{D,max} = 2 \times 144/(8\pi^2)$ = **3.648** W total, **1.824** W per transistor. $\theta_{SA} \le (125 - 50)/1.824 - 3$ = **38.12** °C/W.

### Solution 9

(a) $g_{m1} = I_{SS}/V_{ov}$ = **200** µA/V; GBW $= g_{m1}/(2\pi C_c)$ = **15.92** MHz.

(b) Internal $I_{SS}/C_c$ = **20** V/µs. On the falling edge the PMOS M6 cuts off, and the sink $I_7$ discharges $C_L$ while the first stage still pushes $I_{SS}$ through $C_c$ into the output: $(I_7 - I_{SS})/C_L$ = **13.75** V/µs. (If node 1 clamped at its rail, the bound would be $I_7/(C_L + C_c)$ = **15** V/µs.) Rising edges are input-limited (20 V/µs), falling edges output-limited (13.75 V/µs). Full-power bandwidth at 2 V peak, set by the slower edge: $13.75\ \text{V/µs}/(2\pi \times 2\ \text{V})$ = **1.094** MHz.

### Solution 10

(a) $C_1C_2/(C_1 + C_2)$ = 0.8 nF, so $f_0 = 1/(2\pi\sqrt{4.7\ \mu\text{H} \times 0.8\ \text{nF}})$ = **2.596** MHz; $g_m \ge (C_2/C_1)/R$ = **2.667** mA/V.

(b) $f = 1/(2 \times 9 \times 25\ \text{ps})$ = **2.222** GHz.

### Solution 11

(a) $R_{eq} = \gamma/g_m + 1/(g_m^2R_D) = 66.67 + 10$ = **76.67** Ω; $e_n = \sqrt{4kTR_{eq}}$ = **1.127** nV/√Hz; over 1 MHz, **1.127** µV RMS.

(b) $\sqrt{kT/2\ \text{pF}}$ = **45.51** µV.

### Solution 12

(a) $4kTR_s$ = 1.657 × 10⁻¹⁷, $e_n^2$ = 9 × 10⁻¹⁸ and $(i_nR_s)^2$ = 2.5 × 10⁻¹⁹ V²/Hz, so $F$ = **1.558** and NF = **1.927** dB.

(b) $R_{opt} = e_n/i_n$ = **6** kΩ, where $F_{min} = 1 + e_ni_n/(2kT)$ = **1.181**, NF = **0.7228** dB.

### Solution 13

(a) Close the loop, $s_c = Px$: then $x = cu + dPx$, so $x = cu/(1 - dP)$ and $y = au + bPcu/(1 - dP)$. Define the return ratio $T = -dP$ (the loop gain at the source), the direct transmission $A_{\mathrm{dir}} = a$ (gain with $P = 0$), and the asymptotic gain $A_\infty = a - bc/d$ (gain as $P \to \infty$, forcing $x \to 0$). Then $A_\infty T + A_{\mathrm{dir}} = (a - bc/d)(-dP) + a = a(1 - dP) + bcP$, and dividing by $1 + T = 1 - dP$ gives $a + bcP/(1 - dP)$, the closed-loop gain. ∎

(b) Each transistor carries a half-sine of peak $V_{op}/R_L$, whose average over a cycle is $V_{op}/(\pi R_L)$, so $P_S = 2V_{CC}V_{op}/(\pi R_L)$ and $\eta = P_L/P_S = (\pi/4)(V_{op}/V_{CC})$, at most π/4 at $V_{op} = V_{CC}$. The dissipation $P_D = 2V_{CC}V_{op}/(\pi R_L) - V_{op}^2/(2R_L)$ is maximized where $dP_D/dV_{op} = 0$: $V_{op} = 2V_{CC}/\pi$.

(c) The resistor's noise $4kTR$ (V²/Hz) reaches the capacitor through $1/(1 + j2\pi fRC)$, so $\overline{v^2} = \int_0^\infty 4kTR\,df/(1 + (2\pi fRC)^2) = 4kTR \cdot 1/(4RC) = kT/C$, using $\int_0^\infty dx/(1 + x^2) = \pi/2$. A larger $R$ raises the density in proportion to $R$ but narrows the noise bandwidth $1/(4RC)$ in proportion to $1/R$; they cancel. Equivalently, the capacitor's average energy is $kT/2$ by equipartition.

### Solution 14

(a) $g_m = 1\ \mu\text{A}/25.852\ \text{mV}$ = **38.68** µA/V, so $e_n = \sqrt{2kT/g_m}$ = **14.63** nV/√Hz for one ideal transistor (a differential pair, with two, is √2 worse). The claim is **857** times lower in power. A single transistor would need about 857 × 1 µA = **0.857** mA to reach 0.5 nV/√Hz, nearly a thousand times the claimed total current. As stated, the claim is physically impossible.

(b) Rubric (any two, 3 points each, with the exposing question):

- The noise is quoted at one frequency (e.g. 1 kHz) where an external low-noise component dominates, or only the *voltage* noise of a separate high-current front end is meant: "What is the total supply current at the operating point where 0.5 nV/√Hz is measured?"
- The figure is per √Hz *at a high frequency* of a chopped amplifier, or after averaging/decimation in a narrow band: "What is the integrated noise from 0.1 Hz to 1 MHz?"
- The number is input-referred to a large gain setting with a different bias: "At what gain and bias was it measured?"
- "1 µA" is a sleep or average duty-cycled current: "What is the current while it is actually amplifying?"

(c) Rubric (3 points for three): the integrated noise over the stated bandwidth including 1/f; the current noise $i_n$ (with the sensor's source impedance); the supply current at the noise operating point; and the measurement conditions (temperature, gain, source resistance).

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
| X12.2a | five-transistor OTA gain | 50 | — |
| X12.2b | cascode side resistance | 10.2 | MΩ |
| X12.2c | total output resistance | 5.1 | MΩ |
| X12.2d | telescopic gain | 5100 | — |
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
| X12.4d | C_gd's share | 61 | % |
| X12.5a | loop gain | 100 | — |
| X12.5b | closed-loop gain | 19.80 | — |
| X12.5c | input resistance | 1.01 | MΩ |
| X12.5d | output resistance | 9.901 | Ω |
| X12.5e | bandwidth | 5.05 | MHz |
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
| X12.8a | maximum output power | 9 | W |
| X12.8b | supply power | 11.46 | W |
| X12.8c | efficiency | 78.54 | % |
| X12.8d | worst-case amplitude | 7.639 | V |
| X12.8e | total worst dissipation | 3.648 | W |
| X12.8f | per-transistor dissipation | 1.824 | W |
| X12.8g | largest θ_SA | 38.12 | °C/W |
| X12.9a | g_m1 | 200 | µA/V |
| X12.9b | GBW | 15.92 | MHz |
| X12.9c | internal slew limit | 20 | V/µs |
| X12.9d | output slew limit | 13.75 | V/µs |
| X12.9e | full-power bandwidth | 1.094 | MHz |
| X12.9f | output bound with node 1 clamped | 15 | V/µs |
| X12.10a | Colpitts frequency | 2.596 | MHz |
| X12.10b | minimum g_m | 2.667 | mA/V |
| X12.10c | ring frequency | 2.222 | GHz |
| X12.11a | equivalent noise resistance | 76.67 | Ω |
| X12.11b | input noise density | 1.127 | nV/√Hz |
| X12.11c | RMS over 1 MHz | 1.127 | µV |
| X12.11d | kT/C at 2 pF | 45.51 | µV |
| X12.12a | noise factor | 1.558 | — |
| X12.12b | noise figure | 1.927 | dB |
| X12.12c | optimum source resistance | 6 | kΩ |
| X12.12d | minimum noise factor | 1.181 | — |
| X12.12e | minimum noise figure | 0.7228 | dB |
| X12.14a | g_m at 1 µA | 38.68 | µA/V |
| X12.14b | minimum noise density | 14.63 | nV/√Hz |
| X12.14c | power ratio to the claim | 857 | — |
| X12.14d | current for 0.5 nV/√Hz | 0.857 | mA |
