# Solutions 07-04 · Laplace-Domain Circuit Analysis

Problems: [07-04 problems](../problems/07-04-problems.md) · Chapter: [07-04](../chapters/07-04-laplace-domain-circuit-analysis.md). Every number below is recomputed by [verify_07_04.py](../verify/verify_07_04.py), by symbolic s-domain algebra and independently by time-domain simulation; values marked † are also confirmed by an ngspice netlist in [labs/07-04-lab](../labs/07-04-lab/README.md).

---

## Solutions

### Solution 07-04.1

(a) Inductor: series form $sL = 0.02s$ Ω with a source $L\,i(0^-) = 0.02\times0.5 = $ **10.00 mV·s** pushing current in the direction of $i$; parallel form $1/(sL)$ with a current source $i(0^-)/s = 0.5/s$ A·s. Capacitor: parallel form $sC$ with a current source $C\,v(0^-) = 4.7\times10^{-6}\times5 = $ **23.50 µC** (A·s) pushing current out of the + terminal; series form $1/(sC)$ with a source $v(0^-)/s = 5/s$ V·s, + at the + terminal.

(b) Shorted inductor ($V = 0$): $I = L\,i(0^-)/(sL) = i(0^-)/s = 0.5/s$, so $i(t) = 0.5$ A for all $t > 0$: the current is trapped. Open capacitor ($I = 0$): $sCV = Cv(0^-)$, so $V = v(0^-)/s = 5/s$ and $v(t) = 5$ V: the charge stays. Both match the ideal elements' behavior.

### Solution 07-04.2

The parallel LC has $Z_{LC} = \dfrac{sL\cdot\frac{1}{sC}}{sL + \frac{1}{sC}} = \dfrac{sL}{1 + s^2LC}$, so

$$
Z(s) = R + \frac{sL}{1 + s^2LC} = \frac{RLCs^2 + Ls + R}{LCs^2 + 1} = 100\,\frac{s^2 + 10^4s + 10^8}{s^2 + 10^8}\ \Omega .
$$

Poles at $s = \pm j$ **10.00 krad/s**; zeros at $s = -5000 \pm j8660$ s⁻¹ (the roots of $s^2 + 10^4s + 10^8$). $Z(0) = $ **100 Ω** (the inductor shorts the tank at DC) and $Z(\infty) = 100$ Ω (the capacitor shorts it at high frequency). The poles sit on the imaginary axis because at $\omega_0 = 1/\sqrt{LC}$ the lossless tank's impedance is infinite: a current source driving the network at that frequency would see an open circuit. A lossless parallel LC is exactly the case §3.8 allows on the axis.

### Solution 07-04.3

(a) Initial value: $\lim_{s\to\infty}sV = \lim\dfrac{10(s + 200)}{(s + 100)(s + 400)} = $ **0 V**. The poles of $sV$ are −100 and −400, both in the left half-plane, so the final-value theorem applies: $v(\infty) = \dfrac{10\times200}{100\times400} = $ **0.05000 V** (50 mV).

(b) $\lim_{s\to0}sV = 10/10^6 = $ **10.00 µV**, but $sV = 10/(s^2 + 10^6)$ has poles at $\pm j1000$, on the imaginary axis, so the theorem does not apply. Partial fractions give $V = 10^{-5}\big(\tfrac1s - \tfrac{s}{s^2 + 10^6}\big)$ and $v(t) = 10^{-5}(1 - \cos1000t)$ V: it oscillates forever between 0 and **20.00 µV**, with an average of **10.00 µV**. The "final value" the theorem returns is only the average of a signal that never settles.

### Solution 07-04.4

(a) Use parallel models: the inductor is $1/(sL)$ with a source $i(0^-)/s = 0.01/s$ in the direction of its current (down, out of the node); the capacitor is $sC$ with a source $Cv(0^-) = 10^{-5}$ A·s pushing current into the node. KCL at the top node, currents leaving:

$$
\frac{V}{R} + \frac{V}{sL} + \frac{0.01}{s} + sCV - 10^{-5} - \frac{0.02}{s} = 0 .
$$

Multiplying by $s/C$ and collecting: $V\big(s^2 + \tfrac{s}{RC} + \tfrac{1}{LC}\big) = 5s + \dfrac{0.02 - 0.01}{C}$, so

$$
V(s) = \frac{5s + 5000}{s^2 + 2000s + 10^7} = \frac{5(s + 1000)}{(s + 1000)^2 + 3000^2} .
$$

(b) α = **1000 s⁻¹**, $\omega_d = $ **3000 rad/s**, and the numerator is exactly 5 times $(s + 1000)$, so $v(t) = 5e^{-1000t}\cos3000t$ V. At 1 ms: $5e^{-1}\cos3 = $ **−1.821 V**.

(c) The zero-state part keeps only the 20 mA source: $V_{zs} = \dfrac{0.02/C}{s^2 + 2000s + 10^7} = \dfrac{10^4}{(s + 1000)^2 + 3000^2}$, so $v_{zs} = \dfrac{10^4}{3000}e^{-1000t}\sin3000t$, amplitude **3.333 V**. The zero-input part is the rest, $V_{zi} = \dfrac{5(s - 1000)}{(s + 1000)^2 + 3000^2}$, that is $e^{-1000t}(5\cos3000t - 3.333\sin3000t)$. Their sine terms cancel in the total. Both share the same poles.

### Solution 07-04.5

(a) The source is $V_{Th} = 10/s$ (the capacitor's initial-condition source) behind $Z_{Th} = 1000 + 1/(sC) = 1000 + 5\times10^5/s$. With the inductor ($sL = 0.5s$, no initial current):

$$
I(s) = \frac{10/s}{1000 + 5\times10^5/s + 0.5s} = \frac{20}{s^2 + 2000s + 10^6} = \frac{20}{(s + 1000)^2} .
$$

(b) A repeated pole at −1000 s⁻¹: **critically damped** (α = $\omega_0$ = 1000 s⁻¹, ζ = **1.000**). From $1/(s + a)^2 \leftrightarrow te^{-at}$, $i(t) = 20\,t\,e^{-1000t}$ A.

(c) $di/dt = 20e^{-1000t}(1 - 1000t) = 0$ at $t = $ **1.000 ms**, where $i = 20\times10^{-3}e^{-1} = $ **7.358 mA**.

(d) $V_L = sL\,I = 10s/(s + 1000)^2$, and $\lim_{s\to\infty}sV_L = $ **10 V**: at $0^+$ no current flows, so the full capacitor voltage appears across the inductor ✓.

### Solution 07-04.6

(a) With mesh currents $I_1$ (source, $R_1$, $C$) and $I_2$ ($C$, $L$, $R_2$), both clockwise:

$$
\Big(R_1 + \frac{1}{sC}\Big)I_1 - \frac{1}{sC}I_2 = \frac{10}{s}, \qquad -\frac{1}{sC}I_1 + \Big(\frac{1}{sC} + sL + R_2\Big)I_2 = 0 .
$$

Solving (Cramer's rule): $I_2(s) = \dfrac{10^8}{s\,(s^2 + 20\,000s + 2\times10^8)}$ A·s.

(b) Poles: $s = 0$ (the step) and $s = -10\,000 \pm j10\,000$ s⁻¹. With $\omega_0 = \sqrt{2}\times10^4$ and α = $10^4$, ζ = **0.7071**.

(c) Final value $\lim_{s\to0}sI_2 = 10^8/(2\times10^8) = $ **0.5000 A** (the DC path is $R_1 + R_2$ = 20 Ω). $I_2$ has no zeros and starts from rest, so the all-pole formulas apply: overshoot $e^{-\pi} = 4.32\%$, peak **0.5216 A**† at $t = \pi/\omega_d = $ **314.2 µs**. The full waveform is $i_2 = 0.5\big[1 - e^{-10^4t}(\cos10^4t + \sin10^4t)\big]$, so $i_2(0.5\text{ ms}) = $ **0.5023 A**.

### Solution 07-04.7

Nodal analysis with $\tau = RC$ = 1 ms: at node 1, $(V_1 - V_{in})/R + sCV_1 + (V_1 - V_2)/R = 0$; at node 2, $(V_2 - V_1)/R + sCV_2 = 0$, so $V_1 = (1 + s\tau)V_2$. Substituting:

$$
H(s) = \frac{V_2}{V_{in}} = \frac{1}{(s\tau)^2 + 3s\tau + 1} .
$$

Poles: $s\tau = (-3 \pm\sqrt5)/2$, so $s = $ **−382.0 s⁻¹** and **−2618 s⁻¹**, exactly the eigenvalues of 07-03 Example 07-03.6. DC gain $H(0) = $ **1**. There are no finite zeros because no series branch can become infinite (the series elements are resistors) and no shunt branch can become zero at a finite $s$ (a capacitor's impedance $1/(sC)$ vanishes only as $s \to \infty$).

### Solution 07-04.8

(a) The shunt branch is $Z_{sh} = sL + 1/(sC)$, and the divider gives

$$
H(s) = \frac{Z_{sh}}{R + Z_{sh}} = \frac{s^2LC + 1}{s^2LC + sRC + 1} = \frac{s^2 + 10^{15}}{s^2 + 5\times10^7s + 10^{15}} .
$$

(b) Zeros at $s = \pm j/\sqrt{LC} = \pm j31.62$ Mrad/s: the series LC shorts the node at **5.033 MHz**, removing that frequency completely.

(c) Poles: $s = -2.5\times10^7 \pm j\sqrt{10^{15} - 6.25\times10^{14}}$, that is **−25.00** ± j**19.36** Mrad/s, with ζ = $(R/2)\sqrt{C/L} = $ **0.7906**.

(d) $H(0) = 1$ (the capacitor blocks DC in the trap) and $H(\infty) = 1$ (the inductor blocks high frequencies): the trap only bites near 5 MHz.

### Solution 07-04.9

(a) $Y(s) = \dfrac{1}{R + sL + 1/(sC)} = \dfrac{sC}{s^2LC + sRC + 1} = \dfrac{1}{L}\,\dfrac{s}{s^2 + (R/L)s + 1/(LC)}$, with α = 5000 s⁻¹ and $\omega_d = 31.22$ krad/s (Problem 07-03.14).

(b) Write $s = (s + \alpha) - \alpha$: $i_\delta(t) = \dfrac{1}{L}e^{-\alpha t}\Big(\cos\omega_dt - \dfrac{\alpha}{\omega_d}\sin\omega_dt\Big)$. At $0^+$: $1/L = $ **1000 A per V·s**. (A unit voltage impulse puts 1 V·s across the inductor at once, giving it $1/L$ amperes.)

(c) Zero where $\tan\omega_dt = \omega_d/\alpha$: $t = \arctan(\omega_d/\alpha)/\omega_d = $ **45.22 µs**. The step response is the integral of the impulse response, so the step response's current has its peak exactly where the impulse response crosses zero: 45.22 µs, as Problem 07-03.14 found.

### Solution 07-04.10

(a) Flux linkage is conserved through the switching instant (the s-domain shows an impulse of voltage, of finite area, so no flux can change discontinuously in total): $L_1\cdot1 + L_2\cdot0 = (L_1 + L_2)\,i$, so $i = 10/40 = $ **0.2500 A**.

(b) Before: $\tfrac12(0.01)(1^2) = $ **5.000 mJ**. After: $\tfrac12(0.04)(0.25^2) = $ **1.250 mJ**.

(c) The 30 mH inductor gains $L_2\Delta i = 0.03\times0.25 = $ **7.500 mV·s** of flux linkage, and the 10 mH inductor loses the same. In the s-domain the switch voltage contains an impulse of that area: an ideal switch would see an infinite voltage for zero time. A real one arcs or breaks down, and that is where the missing 3.75 mJ goes (07-01's inductive kick).

(d) It is Example 07-04.4's dual: there, charge was conserved and capacitor voltages jumped with a current impulse; here flux is conserved and inductor currents jump with a voltage impulse. In both, the ideal model loses energy it cannot place.

### Solution 07-04.11

(a) KCL at the drain, currents leaving: $g_mV_{in} + (V_{out} - V_{in})sC_{gd} + V_{out}/R_D + sC_LV_{out} = 0$, so

$$
H(s) = \frac{sC_{gd} - g_m}{1/R_D + s(C_{gd} + C_L)} = -g_mR_D\,\frac{1 - sC_{gd}/g_m}{1 + sR_D(C_{gd} + C_L)} .
$$

(b) Zero at $s = +g_m/C_{gd} = 2\times10^{10}$ rad/s (**3.183 GHz**), in the right half-plane; pole at $s = -1/\big(R_D(C_{gd} + C_L)\big) = -8\times10^7$ rad/s (**12.73 MHz**); DC gain $-g_mR_D = $ **−50**.

(c) $v_{out}(0^+) = \lim_{s\to\infty}H(s)\times10\text{ mV} = \dfrac{C_{gd}}{C_{gd} + C_L}\times10\text{ mV} = $ **2.000 mV** (positive!), and $v_{out}(\infty) = -50\times10\text{ mV} = $ **−0.5000 V**.

(d) Partial fractions: $v_{out}(t) = -0.5 + 0.502e^{-8\times10^7t}$ V. It crosses zero when $e^{-8\times10^7t} = 0.5/0.502$, at $t = \ln(1.004)/(8\times10^7) = $ **49.9 ps**.

(e) At the first instant the transistor's current cannot yet change the drain voltage much, but the gate step is coupled straight through $C_{gd}$ to the drain, a capacitive divider with $C_L$: the output jumps up by 2 mV. Only then does the inverting transconductance pull it down toward −0.5 V. Two paths with opposite signs, the hallmark of a right-half-plane zero. In a feedback amplifier that zero costs phase margin, which is why op-amp designers fight it (Course 12).

### Solution 07-04.12

(a) With $V_b = V_o/K$, KCL at node a: $(V_a - V_{in})/R + (V_a - V_b)/R + sC(V_a - V_o) = 0$; at node b: $(V_b - V_a)/R + sCV_b = 0$. Eliminating $V_a$:

$$
H(s) = \frac{K}{(sRC)^2 + (3 - K)\,sRC + 1} .
$$

(b) $\omega_0 = 1/RC = 10^4$ rad/s, $f_0 = $ **1.592 kHz**, and comparing with $s^2 + (\omega_0/Q)s + \omega_0^2$ gives $Q = 1/(3 - K)$. For $Q = 1/\sqrt2$: $K = 3 - \sqrt2 = $ **1.586**.

(c) The damping term vanishes at $K = $ **3**: the poles reach the imaginary axis and the circuit oscillates at 1.592 kHz; above 3 they move into the right half-plane and the oscillation grows until the amplifier saturates. The same characteristic equation as the Wien bridge of Example 07-04.6: both circuits use positive feedback through an RC network.

### Solution 07-04.13

(a) Writing $x = sRC$ and solving the three node equations (each node: current in through the left resistor, out through the right resistor and the capacitor) gives $V_3/V_{in} = 1/(x^3 + 5x^2 + 6x + 1)$; the cross terms come from each section loading the previous one.

(b) The loop $V_{in} = -KV_3$ has a nonzero solution when $1 + K/(x^3 + 5x^2 + 6x + 1) = 0$:

$$
x^3 + 5x^2 + 6x + (1 + K) = 0 .
$$

All coefficients are positive, so the cubic condition requires $5\times6 > 1 + K$: stable for $K < $ **29**, oscillating at $K = 29$.

(c) At $K = 29$: $x^3 + 5x^2 + 6x + 30 = (x^2 + 6)(x + 5)$. The imaginary roots $x = \pm j\sqrt6$ give $\omega = \sqrt6/RC$, so $f = \sqrt6/(2\pi\times10^{-4}) = $ **3.898 kHz**, and the third root $x = -5$ is $s = -5/RC = $ **−50.00 × 10³ s⁻¹**, a decaying mode.

### Solution 07-04.14

(a) $f_z = 1/(2\pi R_{ESR}C)$ with $C$ = 2.2 µF: **723.4 kHz** at 0.1 Ω and **3.617 kHz** at 20 Ω. The window allows the zero anywhere between about 3.6 kHz and 720 kHz.

(b) With 5 mΩ: $f_z = $ **14.47 MHz**, twenty times above the window's top. The zero is now far beyond the loop's crossover and can no longer add the phase lead the regulator was designed around, so it may oscillate.

(c) With 0.205 Ω in total: $f_z = $ **352.9 kHz**, back inside the window. The cost: a load step $\Delta I$ produces an immediate output step $\Delta I\times R$ across that resistance before the loop responds, here $0.05\times0.205 = $ **10.25 mV**, and the resistor adds output noise and ripple.

(d) No: $1/(2\pi\times0.1\times2.2\times10^{-6}) = 723.4$ kHz, ten times the printed 72.3 kHz. The note's physics is right; its arithmetic slipped a decimal place (§9).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-04.1a | inductor initial-condition source | 10.00 | mV·s |
| 07-04.1b | capacitor initial-condition source | 23.50 | µC |
| 07-04.2a | pole magnitude | 10.00 | krad/s |
| 07-04.2b | zero real part | −5000 | s⁻¹ |
| 07-04.2c | zero imaginary part | 8660 | s⁻¹ |
| 07-04.2d | $Z(0)$ | 100 | Ω |
| 07-04.3a | $v(0^+)$ | 0 | V |
| 07-04.3b | $v(\infty)$ | 0.05000 | V |
| 07-04.3c | naive final value | 10.00 | µV |
| 07-04.3d | average of the oscillation | 10.00 | µV |
| 07-04.3e | maximum of the oscillation | 20.00 | µV |
| 07-04.4a | α | 1000 | s⁻¹ |
| 07-04.4b | $\omega_d$ | 3000 | rad/s |
| 07-04.4c | $v(1\text{ ms})$ | −1.821 | V |
| 07-04.4d | zero-state amplitude | 3.333 | V |
| 07-04.5a | ζ | 1.000 | — |
| 07-04.5b | time of the peak | 1.000 | ms |
| 07-04.5c | peak current | 7.358 | mA |
| 07-04.5d | $v_L(0^+)$ | 10 | V |
| 07-04.6a | pole real part | −10 000 | s⁻¹ |
| 07-04.6b | pole imaginary part | 10 000 | s⁻¹ |
| 07-04.6c | ζ | 0.7071 | — |
| 07-04.6d | final current | 0.5000 | A |
| 07-04.6e | peak current | 0.5216 | A |
| 07-04.6f | time of the peak | 314.2 | µs |
| 07-04.6g | $i_2(0.5\text{ ms})$ | 0.5023 | A |
| 07-04.7a | slow pole | −382.0 | s⁻¹ |
| 07-04.7b | fast pole | −2618 | s⁻¹ |
| 07-04.7c | DC gain | 1 | — |
| 07-04.8a | notch frequency | 5.033 | MHz |
| 07-04.8b | pole real part | −25.00 | Mrad/s |
| 07-04.8c | pole imaginary part | 19.36 | Mrad/s |
| 07-04.8d | ζ | 0.7906 | — |
| 07-04.9a | $i_\delta(0^+)$ | 1000 | A/(V·s) |
| 07-04.9b | first zero crossing | 45.22 | µs |
| 07-04.10a | common current | 0.2500 | A |
| 07-04.10b | energy before | 5.000 | mJ |
| 07-04.10c | energy after | 1.250 | mJ |
| 07-04.10d | flux linkage transferred | 7.500 | mV·s |
| 07-04.11a | zero | 3.183 | GHz |
| 07-04.11b | pole | 12.73 | MHz |
| 07-04.11c | DC gain | −50 | — |
| 07-04.11d | $v_{out}(0^+)$ | 2.000 | mV |
| 07-04.11e | $v_{out}(\infty)$ | −0.5000 | V |
| 07-04.11f | zero-crossing time | 49.9 | ps |
| 07-04.12a | $f_0$ | 1.592 | kHz |
| 07-04.12b | gain for Q = 1/√2 | 1.586 | — |
| 07-04.12c | gain at the stability limit | 3 | — |
| 07-04.13a | gain at the onset of oscillation | 29 | — |
| 07-04.13b | oscillation frequency | 3.898 | kHz |
| 07-04.13c | third root | −50.00 | 10³ s⁻¹ |
| 07-04.14a | ESR zero at 0.1 Ω | 723.4 | kHz |
| 07-04.14b | ESR zero at 20 Ω | 3.617 | kHz |
| 07-04.14c | ESR zero of the ceramic | 14.47 | MHz |
| 07-04.14d | zero with 0.2 Ω added | 352.9 | kHz |
| 07-04.14e | step across 0.205 Ω at 50 mA | 10.25 | mV |
