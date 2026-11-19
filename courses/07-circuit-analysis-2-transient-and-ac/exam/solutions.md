# Course 07 · Final Exam — Solutions

Exam: [README.md](README.md).

All numbers are recomputed by [verify_07_exam.py](../verify/verify_07_exam.py). Every circuit answer (Questions 2 to 6 and 9 to 14) is confirmed in ngspice by three netlists:

- [exam_transient.cir](exam_transient.cir) for the millisecond transients (Questions 2, 3 and 5);
- [exam_ringing.cir](exam_ringing.cir) for the microsecond ringing (Questions 4 and 13c);
- [exam_ac.cir](exam_ac.cir) for the AC answers.

Each solution names the chapter to revisit if you lost points.

**1.** *(07-01)*

(a) $i = C\,dv/dt = 10\ \mu\text{F}\times(5\ \text{V}/2\ \text{ms}) = $ **25 mA**, constant while the ramp lasts.

(b) $v = L\,di/dt = 100\ \mu\text{H}\times(3\ \text{A}/10\ \mu\text{s}) = $ **30 V**. The stored energy is $w = \tfrac12Li^2 = \tfrac12\times100\ \mu\text{H}\times9\ \text{A}^2 = $ **450 µJ**.

(c) Series capacitors combine reciprocally: $C = (1/4.7 + 1/2.2)^{-1}$ µF = **1.499 µF**.

- Both carry the same current, so both acquire the same charge, $Q = CV = 1.499\ \mu\text{F}\times12\ \text{V} = 17.98$ µC.
- The voltages are therefore inversely proportional to the capacitances:
  - the 4.7 µF capacitor gets $12\times2.2/6.9 = $ **3.826 V**;
  - the 2.2 µF capacitor gets $12\times4.7/6.9 = $ **8.174 V**.
- The smaller capacitor takes the larger voltage, so check each part's voltage rating separately.

(d) The capacitor supplies $\Delta I$ for $\Delta t$, losing charge $\Delta I\,\Delta t$, so $\Delta V = \Delta I\,\Delta t/C$. Then $C \ge \Delta I\,\Delta t/\Delta V = 2\ \text{A}\times1\ \mu\text{s}/50\ \text{mV} = $ **40 µF**.

Real capacitors also drop $\Delta I\times\text{ESR}$ and $L\,di/dt$ across their ESL the instant the step arrives. A 2 A step into 10 mΩ of ESR would use 20 mV of the 50 mV budget, so the real design needs more capacitance and low-ESR parts (07-01 §3.6).

**2.** *(07-02)*

(a) $\tau = RC = 10\ \text{k}\Omega\times100\ \text{nF} = $ **1 ms**. Then $v_C(2\ \text{ms}) = 3.3(1 - e^{-2}) = $ **2.853 V**, 86.5% of the way.

(b) The 10% and 90% points are at $\tau\ln(1/0.9)$ and $\tau\ln(1/0.1)$, so $t_r = \tau\ln9 = $ **2.197 ms**.

- The bandwidth is $f_{3dB} = 1/(2\pi\tau) = $ **159.2 Hz**.
- Their product is $\ln9/(2\pi) = $ **0.3497**: the "$t_rf_{3dB}$ ≈ 0.35" rule, exact for a single pole.

(c) The error after time $t$ is $3.3e^{-t/\tau}$ V. Half an LSB of a 12-bit converter is $3.3/2^{13}$ V. Setting them equal gives $t = 13\tau\ln2 = $ **9.011 ms**, that is, $(N + 1)\ln2$ time constants.

(d) The source delivers $QV = CV^2$. Half is stored, so the other half is dissipated in the resistor: $\tfrac12CV^2 = \tfrac12\times100\ \text{nF}\times3.3^2 = $ **544.5 nJ**. The value of $R$ does not matter.

**3.** *(07-02)*

(a) Before $t = 0$ the capacitor is an open circuit, and R1 and R2 form a divider: $v_C(0^-) = 12\times12/16 = $ **9 V**.

(b) With S closed, R2 ∥ R3 = 4 kΩ. Seen from the capacitor:

- Thévenin voltage: $V_{Th} = 12\times4/(4 + 4) = $ **6 V**, the final value.
- Thévenin resistance: $R_{Th} = 4\parallel12\parallel6$ kΩ $= 1/(0.25 + 0.0833 + 0.1667)$ kΩ = 2 kΩ.
- Time constant: $\tau_1 = R_{Th}C = $ **20 ms**.

Hence $v_C(t) = 6 + (9 - 6)e^{-t/20\ \text{ms}} = 6 + 3e^{-t/20\ \text{ms}}$ V.

(c) At $0^+$ the capacitor still holds 9 V, so $i_{R3} = 9/6\ \text{k}\Omega = $ **1.5 mA**. KCL at node a, with currents into the capacitor:

- R1 brings in $(12 - 9)/4\ \text{k}\Omega = 0.75$ mA;
- R2 takes $9/12\ \text{k}\Omega = 0.75$ mA;
- R3 takes 1.5 mA.

So $i_C(0^+) = 0.75 - 0.75 - 1.5 = $ **−1.5 mA**: the capacitor discharges.

Check: $C\,dv_C/dt(0^+) = 10\ \mu\text{F}\times(-3/20\ \text{ms}) = -1.5$ mA. The capacitor current jumped from 0 to −1.5 mA at the switching instant, while its voltage did not jump.

(d) $6 + 3e^{-t/\tau_1} = 7$ gives $t = \tau_1\ln3 = $ **21.97 ms**.

(e) $v_C(40\ \text{ms}) = 6 + 3e^{-2} = $ **6.406 V**. This is the initial value for the second interval.

- With S open, the final value is again 9 V.
- $R_{Th} = 4\parallel12 = 3$ kΩ, so $\tau_2 = $ **30 ms**. The time constant changes because the circuit changed (07-02, Common mistake 4).
- So $v_C(100\ \text{ms}) = 9 - (9 - 6.406)e^{-60/30} = $ **8.649 V**.

**4.** *(07-03)*

(a) The rates:

- $\omega_0 = 1/\sqrt{LC} = 1/\sqrt{10^{-3}\times10^{-6}} = $ **31,623 rad/s**, so $f_0 = \omega_0/2\pi = $ **5033 Hz**.
- $\alpha = R/(2L) = 20/0.002 = $ **10,000 s⁻¹**.
- $\zeta = \alpha/\omega_0 = $ **0.3162**, so $Q = 1/(2\zeta) = $ **1.581**, which equals $\sqrt{L/C}/R = 31.62/20$.

The circuit is underdamped.

(b) $\omega_d = \sqrt{\omega_0^2 - \alpha^2} = \sqrt{10^9 - 10^8} = $ **30,000 rad/s**, so $f_d = $ **4775 Hz**.

(c) The step response from rest is

$$
v_C = V\Big[1 - e^{-\alpha t}\Big(\cos\omega_dt + \frac{\alpha}{\omega_d}\sin\omega_dt\Big)\Big] ,
$$

whose derivative is $V(\omega_0^2/\omega_d)e^{-\alpha t}\sin\omega_dt$. The derivative is first zero at $t_p = \pi/\omega_d = $ **104.7 µs**. There $\cos\omega_dt = -1$, so $v_C = V(1 + e^{-\alpha\pi/\omega_d})$.

- The overshoot is $e^{-\pi/3}$ = **35.09%** (the same as $e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$).
- The peak voltage is $10\times1.3509 = $ **13.51 V**.

(d) Critical damping needs $\zeta = 1$, that is, $R = 2\sqrt{L/C} = $ **63.25 Ω**.

For 5% overshoot, solve $e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = 0.05$:

$$
\zeta = \frac{\ln(1/0.05)}{\sqrt{\pi^2 + \ln^2(1/0.05)}} = \frac{2.996}{4.341} = 0.6901 ,
$$

so $R = 2\zeta\sqrt{L/C} = $ **43.65 Ω**.

**5.** *(07-04)*

(a) After a long time at 2 V, no current flows: the capacitors are open circuits and the resistors drop nothing. So $v_{C1}(0^-) = v_{C2}(0^-) = $ **2 V**.

(b) In the s-domain, each capacitor becomes an admittance $sC$ in parallel with a current source $Cv(0^-)$ that drives current into its node. With $G = 1/R$, $V_{in}(s) = 5/s$ and $\tau = RC$ = 1 ms, KCL gives these equations at node 2 and node 3:

$$
\begin{aligned}
G(V_2 - V_{in}) + sCV_2 + G(V_2 - V_3) &= 2C ,\\
G(V_3 - V_2) + sCV_3 &= 2C .
\end{aligned}
$$

Divide by $G$:

- The node-3 equation gives $V_2 = (1 + s\tau)V_3 - 2\tau$.
- Substituting into the node-2 equation, $(2 + s\tau)V_2 - V_3 = 5/s + 2\tau$, gives

$$
V_3\big[(1 + s\tau)(2 + s\tau) - 1\big] = \frac{5}{s} + 2\tau + 2\tau(2 + s\tau)
\quad\Longrightarrow\quad
V_3(s) = \frac{5/s + 6\tau + 2\tau^2s}{\tau^2s^2 + 3\tau s + 1} .
$$

(c) With zero initial conditions, the same algebra gives

$$
H(s) = \frac{V_3}{V_{in}} = \frac{1}{\tau^2s^2 + 3\tau s + 1} .
$$

Expanding $2/s + 3H/s = (2\tau^2s^2 + 6\tau s + 2 + 3)/[s(\tau^2s^2 + 3\tau s + 1)]$ reproduces (b). The physical reading: the circuit starts in the steady state for a 2 V input, so the response is 2 V plus the zero-state response to a 3 V step.

- The denominator is $\tau^2s^2 + 3\tau s + 1$. Comparing with $s^2 + 2\zeta\omega_0s + \omega_0^2$ gives $\omega_0 = 1/\tau$ and $2\zeta = 3$, so **ζ = 1.5**: overdamped. An RC ladder cannot ring (07-03 §3.9).
- The poles are $s = (-3 \pm \sqrt5)/(2\tau)$: **−382.0 s⁻¹** and **−2618 s⁻¹**.

(d) Write $x = s\tau$, so the poles are $x_1 = -0.3820$ and $x_2 = -2.618$. Then

$$
\frac{H}{s} = \frac{\tau}{x(x - x_1)(x - x_2)}
$$

has residues 1 at $x = 0$, $1/[x_1(x_1 - x_2)] = -(5 + 3\sqrt5)/10 = -1.1708$, and $1/[x_2(x_2 - x_1)] = (3\sqrt5 - 5)/10 = 0.1708$. Multiplying by 3 and adding the 2 V gives

$$
v_3(t) = 5 - 3.512\,e^{-382.0t} + 0.5125\,e^{-2618t}\ \text{V}\quad(t \text{ in s}) .
$$

The coefficients are **−3.512** and **0.5125**.

(e) The values:

- $v_3(1\ \text{ms}) = 5 - 3.5125e^{-0.382} + 0.5125e^{-2.618} = $ **2.640 V**.
- $v_3(2\ \text{ms}) = $ **3.367 V**.

The theorem checks:

- **Initial value.** $\lim_{s\to\infty}sV_3 = 2\tau^2s^2/(\tau^2s^2) \to$ **2 V**, matching the continuity of the capacitor voltages. The time function gives $5 - 3.5125 + 0.5125 = 2$ as well.
- **Initial slope.** $sV_3 - v_3(0^+) = \big[(5 + 6\tau s + 2\tau^2s^2) - 2(\tau^2s^2 + 3\tau s + 1)\big]/(\tau^2s^2 + 3\tau s + 1) = 3/(\tau^2s^2 + 3\tau s + 1)$, so $\lim_{s\to\infty}s[sV_3 - v_3(0^+)] = \lim 3s/(\tau^2s^2 + \ldots) \to$ **0**. Physically, C2 can only change through R2, and at $0^+$ both ends of R2 sit at 2 V.
- **Final value.** $\lim_{s\to0}sV_3 = 5/1 = $ **5 V**.

The zero initial slope is why the curve starts flat: two cascaded lags.

**6.** *(07-05, 07-06)*

(a) At $\omega = 10^4$ rad/s:

- $Z_L = j\omega L = $ **j100 Ω**;
- $Z_C = 1/(j\omega C) = $ **−j10 Ω**.

The C–R2 branch is $10 - j10$ Ω. In parallel with $j100$:

$$
Z_p = \frac{j100(10 - j10)}{10 + j90} = \frac{(1000 + j1000)(10 - j90)}{8200} = 12.195 - j9.756\ \Omega .
$$

So the source sees $Z_{in} = 20 + Z_p = $ **32.20 − j9.756 Ω**.

(b) Use the divider: $\mathbf{V}_2 = 10\,Z_p/Z_{in}$.

- $\lvert Z_p\rvert = 15.62$ Ω at −38.66°.
- $\lvert Z_{in}\rvert = 33.64$ Ω at −16.86°.
- So $\mathbf{V}_2 = $ **4.642 V at −21.80°**, that is, $v_2(t) = 4.642\cos(10^4t - 21.80°)$ V.

Then $\mathbf{I}_{R2} = \mathbf{V}_2/(10 - j10) = 4.642\angle{-21.80°}/14.14\angle{-45°} = $ **0.3283 A at +23.20°**. The current leads $v_2$ because the branch is capacitive.

(c) $P_{R2} = \tfrac12\lvert\mathbf{I}_{R2}\rvert^2R_2 = \tfrac12\times0.3283^2\times10 = $ **0.5388 W**.

The source current is $\mathbf{I}_s = 10/Z_{in} = 0.2973$ A at +16.86°, so

$$
P_s = \tfrac12\operatorname{Re}(\mathbf{V}_s\mathbf{I}_s^*) = \tfrac12\times10\times0.2973\cos16.86° = \textbf{1.422 W} .
$$

Check: $P_{R1} = \tfrac12\times0.2973^2\times20 = 0.8836$ W, and $0.8836 + 0.5388 = 1.422$ W. L and C absorb no average power.

(d) With R2 removed, C carries no current, so node 3 sits at node 2's open-circuit voltage:

$$
\mathbf{V}_{Th} = 10\,\frac{j100}{20 + j100} = \textbf{9.806 V at 11.31°} .
$$

Turning the source off:

$$
Z_{Th} = -j10 + \frac{20\cdot j100}{20 + j100} = -j10 + (19.23 + j3.846) = \textbf{19.23 − j6.154 Ω} .
$$

(e) The conjugate match is $Z_L = Z_{Th}^* = $ **19.23 + j6.154 Ω**. With the reactances cancelled,

$$
P_{max} = \frac{\lvert\mathbf{V}_{Th}\rvert^2}{8R_{Th}} = \frac{96.15}{8\times19.23} = \textbf{0.6250 W}
$$

(peak phasors, hence 8 rather than 4).

This equals $10^2/(8\times20)$, the power available from the source and R1 alone, because L and C are lossless. A lossless network can only transform impedances; it neither creates nor absorbs power. Conjugate matching through it therefore recovers all of the source's available power.

**7.** *(07-06)*

(a) The power triangle:

- $\lvert S\rvert = P/\text{PF} = 10/0.75 = $ **13.33 kVA**.
- $Q = \lvert S\rvert\sin\theta = 13.33\sqrt{1 - 0.75^2} = $ **8.819 kvar**.
- $I = \lvert S\rvert/V = 13{,}333/230 = $ **57.97 A**.

(b) At PF 0.95 the reactive power must fall to $Q_{new} = P\tan(\arccos0.95) = 10\times0.3287 = 3.287$ kvar. The capacitor supplies $Q_C = 8.819 - 3.287 = 5.532$ kvar. With $Q_C = \omega CV^2$:

$$
C = \frac{5532}{2\pi\cdot50\cdot230^2} = \textbf{332.9 µF} .
$$

(c) $I_{new} = 10{,}000/(230\times0.95) = $ **45.77 A**. The $I^2R$ loss scales as $(0.75/0.95)^2 = 0.6233$, a reduction of **37.67%** for the same useful power.

(d) Different frequencies add in quadrature:

- $I_{rms} = \sqrt{10^2 + 3^2 + 1.5^2} = $ **10.55 A**.
- $\text{THD} = \sqrt{3^2 + 1.5^2}/10 = $ **33.54%**.
- Only the fundamental carries real power (the voltage is a pure sinusoid), so $\text{PF} = \cos0\times I_1/I_{rms} = 1/\sqrt{1 + \text{THD}^2} = $ **0.9481**.

**No capacitor can fix this.** The power factor is lost to distortion, not displacement. A capacitor would add a leading displacement, and it could resonate with the line inductance at a harmonic. The cure is to shape the current: active power-factor correction, or a harmonic filter.

**8.** *(07-07)*

(a) The asymptotes:

- **Magnitude:** 0 dB up to the zero at $10^3$ rad/s, then +20 dB/decade up to the pole at $10^4$, then flat at 20 dB.
- **Phase:** 0° below $10^2$, rising at +45°/decade to the zero's +90° asymptote. The pole subtracts from $10^3$ upward, so the straight-line phase is a trapezoid that returns to 0° above $10^5$. Its maximum occurs between the two corners.

(b) The exact gains:

- At $10^3$: $\lvert H\rvert = \lvert1 + j\rvert/\lvert1 + j0.1\rvert = 1.4142/1.0050$, which is **2.967 dB**, versus 0 dB on the asymptote.
- At $10^4$: $\lvert1 + j10\rvert/\lvert1 + j\rvert = 7.106$, which is **17.03 dB**, versus 20 dB on the asymptote.

The errors are about ±3 dB at each corner, slightly less than 3.01 dB because the other corner is one decade away.

(c) By symmetry on the log axis, the maximum lead is at the geometric mean: $\omega_m = \sqrt{10^3\times10^4} = $ **3162 rad/s**. There:

- the lead is $\arctan\sqrt{10} - \arctan(1/\sqrt{10}) = 72.45° - 17.55° = $ **54.90°** (equivalently $\arcsin[(10 - 1)/(10 + 1)]$);
- the gain is $\sqrt{10}$, that is, **10.00 dB**, halfway up in dB.

(d) The gain–bandwidth product is $A_0f_1 = 10^5\times10$ Hz = **1 MHz**. For $f \gg 10$ Hz,

$$
\lvert A\rvert \approx \frac{10^6/f}{\sqrt{1 + (f/f_2)^2}} .
$$

Setting $\lvert A\beta\rvert = 1$ with β = 1 gives $f^2 + f^4/f_2^2 = 10^{12}$. As a quadratic in $u = f^2$:

$$
u = \frac{f_2^2}{2}\Big(\sqrt{1 + 4\times10^{12}/f_2^2} - 1\Big) = 2\times10^{12}(\sqrt2 - 1) ,
$$

so $f_c = $ **910.2 kHz**. The phase margin is

$$
\text{PM} = 180° - \arctan(f_c/10) - \arctan(f_c/f_2) = 180° - 89.999° - 24.47° = \textbf{65.53°} .
$$

(e) With β = 0.1, $\lvert A\beta\rvert = 1$ gives $u = 2\times10^{12}(\sqrt{1.01} - 1)$, so $f_c = $ **99.88 kHz**. Then $\text{PM} = 180° - 89.994° - \arctan(0.04994) = $ **87.15°**.

The **unity-gain follower is harder to stabilize.** The most feedback (β = 1) pushes the crossover highest, closest to the second pole, where that pole's phase lag erodes the margin. This is why datasheets quote phase margin at unity gain, and why some fast op-amps are only "stable for gains ≥ 5".

**9.** *(07-08)*

(a) The resonance:

- $\omega_0 = 1/\sqrt{LC} = 10^7$ rad/s, so $f_0 = $ **1.592 MHz**.
- $Q = \omega_0L/R = 100/5 = $ **20**.
- $\text{BW} = f_0/Q = $ **79.58 kHz**.
- At resonance the reactances cancel, so the current is $1/5$ A and $\lvert\mathbf{V}_C\rvert = I/(\omega_0C) = 0.2\times100 = $ **20 V**, which is $Q$ times the drive. Parts must be rated for this.

(b) The output is $H = R/[R + j(\omega L - 1/\omega C)]$:

- At 1.5 MHz, $X = 94.25 - 106.10 = -11.86$ Ω, so $\lvert H\rvert = 5/\sqrt{25 + 140.5} = 0.3886$, that is, **−8.210 dB**, at a phase of $-\arctan(X/R) = $ **+67.13°** (the circuit looks capacitive below resonance).
- At 1.7 MHz, $X = +13.19$ Ω, giving **−9.011 dB** at **−69.24°**.

The response is not symmetric in hertz. It is symmetric in the logarithm of frequency, and 1.5 MHz is slightly closer to $f_0$ on that scale than 1.7 MHz.

(c) For the unity-gain Sallen–Key with equal resistors:

- $\omega_0 = 1/(R\sqrt{C_1C_2})$ and $Q = \tfrac12\sqrt{C_1/C_2}$.
- A Butterworth section needs $Q = 1/\sqrt2$, so $C_1 = 2C_2$, and then $\omega_0 = 1/(\sqrt2RC_2)$.
- So $C_2 = 1/(\sqrt2\times10^4\times2\pi\times10^3) = $ **11.25 nF** and $C_1 = $ **22.51 nF**.

Check: the gain at 1 kHz is **−3.010 dB**.

(d) A Butterworth filter of order $n$ has $\lvert H\rvert^2 = 1/[1 + (f/f_c)^{2n}]$:

- For $n = 2$ at 3 kHz: $10\lg(1 + 3^4) = $ **19.14 dB**.
- For 40 dB: $3^{2n} \ge 10^4 - 1$, so $n \ge 4.192$. The lowest order is **5**, which gives $10\lg(1 + 3^{10}) = $ **47.71 dB**.

Each added order buys about 6 dB per octave (20 dB per decade) further out.

**10.** *(07-09)*

(a) The coupling coefficient is $k = M/\sqrt{L_1L_2} = 1.8/2 = $ **0.9**. In series:

- aiding: $L_1 + L_2 + 2M = $ **8.6 mH**;
- opposing: $L_1 + L_2 - 2M = $ **1.4 mH**.

(b) Take both mesh currents entering the dotted terminals, with the load in the secondary loop:

$$
\begin{aligned}
\mathbf{V}_1 &= j\omega L_1\mathbf{I}_1 + j\omega M\mathbf{I}_2 ,\\
0 &= j\omega M\mathbf{I}_1 + (j\omega L_2 + Z_L)\mathbf{I}_2 .
\end{aligned}
$$

The second equation gives $\mathbf{I}_2 = -j\omega M\mathbf{I}_1/(Z_L + j\omega L_2)$, and so

$$
Z_{in} = j\omega L_1 + \frac{(\omega M)^2}{Z_L + j\omega L_2} .
$$

At 10 kHz:

- $\omega L_1 = 251.3$ Ω, $\omega L_2 = 62.83$ Ω and $\omega M = 113.1$ Ω.
- The reflected impedance is $12{,}791/(50 + j62.83) = $ **99.19 − j124.6 Ω**. It is capacitive: an inductive secondary reflects as a capacitive term.
- So $Z_{in} = $ **99.19 + j126.7 Ω**.
- The current ratio is $\lvert\mathbf{I}_2/\mathbf{I}_1\rvert = \omega M/\lvert Z_L + j\omega L_2\rvert = 113.1/80.30 = $ **1.408**.

(c) An ideal transformer scales impedance by $n^2$: $n = \sqrt{800/8} = $ **10**, that is, 10:1 turns, with the amplifier on the 10-turn side.

(d) At full load and PF 0.8 the output is 8000 W and the losses are $80 + 200 = 280$ W, so $\eta = 8000/8280 = $ **96.62%**.

- Copper loss scales as the square of the load fraction $x$; core loss is constant.
- Efficiency peaks where they are equal: $x = \sqrt{80/200} = $ **0.6325**.
- There $\eta = 0.6325\times8000/(0.6325\times8000 + 160) = $ **96.93%**.

**11.** *(07-10)*

(a) Open-circuit tests:

- With port 2 open, a current into port 1 flows through $Z_a$ and $Z_c$: $z_{11} = 10 + 100 = $ **110 Ω**, and $z_{21} = \mathbf{V}_2/\mathbf{I}_1 = $ **100 Ω** (only $Z_c$ is shared).
- Likewise $z_{22} = 20 + 100 = $ **120 Ω** and $z_{12} = $ **100 Ω**.

The network is **reciprocal** ($z_{12} = z_{21}$; it contains only R, L and C) but **not symmetric** ($z_{11} \ne z_{22}$).

(b) The ABCD parameters, with $\Delta_z = 110\times120 - 100^2 = 3200$ Ω²:

- $A = z_{11}/z_{21} = $ **1.1**;
- $B = \Delta_z/z_{21} = $ **32 Ω**;
- $C = 1/z_{21} = $ **0.01 S**;
- $D = z_{22}/z_{21} = $ **1.2**.

$AD - BC = 1.32 - 0.32 = $ **1**, as reciprocity requires.

(c) $Z_{in} = (AZ_L + B)/(CZ_L + D) = (55 + 32)/(0.5 + 1.2) = $ **51.18 Ω**, and $\mathbf{V}_2/\mathbf{V}_1 = Z_L/(AZ_L + B) = 50/87 = $ **0.5747**.

(d) With $Z_0$ = 50 Ω, the common denominator is $A + B/Z_0 + CZ_0 + D = 1.1 + 0.64 + 0.5 + 1.2 = 3.44$. So:

- $S_{11} = (A + B/Z_0 - CZ_0 - D)/3.44 = 0.04/3.44 = $ **0.01163**. Check: $(Z_{in} - 50)/(Z_{in} + 50) = 1.176/101.2$.
- $S_{21} = 2/3.44 = $ **0.5814**, which equals $S_{12}$.
- $S_{22} = (-A + B/Z_0 - CZ_0 + D)/3.44 = $ **0.06977**.

The losses:

- insertion loss $-20\lg0.5814 = $ **4.711 dB**;
- return loss $-20\lg0.01163 = $ **38.69 dB**.

$S_{11} \ne S_{22}$ because the network is not symmetric. From port 1 the 10 Ω arm plus the rest looks like 51.2 Ω, close to 50 Ω. From port 2 the 20 Ω arm makes it look like $(DZ_0 + B)/(CZ_0 + A) = 92/1.6 = 57.5$ Ω.

**12.** *(07-11)*

(a) In Δ, each phase sees the line voltage:

- $I_p = 400/\lvert30 + j40\rvert = 400/50 = $ **8 A**;
- $I_L = \sqrt3I_p = $ **13.86 A**.

The power:

- $P = 3I_p^2R = 3\times64\times30 = $ **5760 W**;
- $Q = 3\times64\times40 = $ **7680 var**;
- $\text{PF} = \cos53.13° = $ **0.6 lagging**.

(b) For a balanced load with impedance angle θ:

- $W_1 = V_LI_L\cos(30° + \theta) = 400\times13.86\cos83.13° = $ **663.0 W**;
- $W_2 = V_LI_L\cos(30° - \theta) = 5543\cos(-23.13°) = $ **5097 W**.

Recovering the totals: $W_1 + W_2 = $ **5760 W** $= P$, and $\sqrt3(W_2 - W_1) = $ **7680 var** $= Q$.

(c) Unity PF needs 7680 var of capacitive compensation, 2560 var per phase.

- In Y, each capacitor sees $400/\sqrt3 = 230.9$ V, so $C_Y = 2560/(2\pi\cdot50\cdot230.9^2) = $ **152.8 µF**.
- The new line current is $5760/(\sqrt3\times400) = $ **8.314 A**, down from 13.86 A.
- In Δ, each capacitor sees 400 V, so $C_\Delta = 2560/(2\pi\cdot50\cdot400^2) = $ **50.93 µF**. That is a third of $C_Y$, but each capacitor must be rated for the line voltage.

**13.** *(07-03, 07-07, 07-08)*

(a) The filter:

- $\omega_0 = 1/\sqrt{LC} = 1/\sqrt{2.2\ \mu\text{H}\times47\ \mu\text{F}} = 98{,}342$ rad/s, so $f_0 = $ **15.65 kHz**.
- $Z_0 = \sqrt{L/C} = $ **0.2164 Ω**.

The transfer function from the switch node is

$$
H(s) = \frac{1}{s^2LC + sL/R + 1} ,
$$

a second-order low-pass. Comparing $s/(\omega_0Q)$ with $sL/R$ gives $Q = R/(\omega_0L) = R/Z_0 = $ **4.622**. At $f_0$ the gain is exactly $Q$: **13.30 dB** of peaking.

(b) The DC output is the average of the switch node, $DV_{in} = 0.25\times12 = $ **3 V** (L is a short and C an open at DC).

A pulse train of height $V$ and duty $D$ has an $n$th-harmonic amplitude of $(2V/n\pi)\sin(n\pi D)$. The fundamental is therefore $(24/\pi)\sin45° = $ **5.402 V** peak.

At 500 kHz:

- $j\omega L = j6.912$ Ω.
- The capacitor branch is $Z_C = 0.010 - j0.006773$ Ω.
- In parallel with 1 Ω: $Z_p = Z_C/(1 + Z_C) = 0.009946 - j0.006639$ Ω.
- So $\lvert H\rvert = \lvert Z_p\rvert/\lvert j\omega L + Z_p\rvert = 0.01196/6.905 = 0.001732$, and the output fundamental is $5.402\times0.001732 = $ **9.355 mV**.
- Without the ESR, $\lvert H\rvert \approx 1/[(f/f_0)^2 - 1] = 0.000981$, giving **5.298 mV**.

**The ESR sets the ripple.** Its zero is at $1/(2\pi\cdot\text{ESR}\cdot C) = 338.6$ kHz, below the switching frequency. At 500 kHz the 10 mΩ of ESR exceeds the 6.77 mΩ capacitive reactance. This is why converter designs specify low-ESR ceramics or polymer capacitors, or put several in parallel.

(c) With the switch node held at a constant voltage, L returns to AC ground. The step is a current $\Delta I\,u(t)$ drawn from the output node, which sees $sL \parallel R \parallel 1/(sC)$:

$$
V(s) = -\frac{\Delta I}{s}\cdot\frac{sL}{s^2LC + sL/R + 1} = -\frac{\Delta I/C}{s^2 + s/(RC) + 1/(LC)} .
$$

This is a parallel RLC with $\alpha = 1/(2RC) = 10{,}638$ s⁻¹ and $\omega_d = \sqrt{\omega_0^2 - \alpha^2} = 97{,}765$ rad/s. Inverting,

$$
v(t) = -\frac{\Delta I}{\omega_dC}e^{-\alpha t}\sin\omega_dt .
$$

The peak is where $\tan\omega_dt = \omega_d/\alpha$, at $t = $ **14.96 µs**. Its value is

$$
\frac{2}{97{,}765\times47\ \mu\text{F}}\,e^{-0.1591}\sin(1.462) = 0.4353\times0.8529\times0.9941 = \textbf{0.3690 V}
$$

of droop. The undamped estimate $\Delta I\cdot Z_0 = $ **0.4327 V** is 17% pessimistic: the load resistor damps the ring ($\zeta = 1/2Q = 0.108$). In a real converter the loop responds within a few microseconds and the ESR adds an instant step of $\Delta I\times\text{ESR}$ = 20 mV.

(d) At 10 Ω, $Q = 10/0.2164 = $ **46.22**, and the gain at $f_0$ is **33.30 dB**.

- The output filter then rings for many cycles ($\alpha = 1/(2RC) = $ **1064 s⁻¹**, so the envelope's time constant is **0.940 ms**, about 15 periods of **63.9 µs**).
- A load step's peak approaches $\Delta I\cdot Z_0$.
- The peaking also makes the control loop much harder to compensate.

Designers damp it in several ways:

- an RC damper across the output capacitor, with $R \approx Z_0$ and a capacitor several times $C$ (07-03 §3.10);
- capacitors with deliberate ESR (polymer or electrolytic) in parallel with the ceramics;
- a closed loop with enough phase margin;
- specifying a minimum load.

**14.** *(07-10, 07-08)*

(a) Unmatched:

- $\Gamma = (12.5 - 50)/(12.5 + 50) = $ **−0.6**;
- the return loss is $-20\lg0.6 = $ **4.437 dB**;
- the mismatch loss is $-10\lg(1 - 0.36) = $ **1.938 dB**: 36% of the power is reflected.

(b) Seen from the 50 Ω side, the shunt capacitor's admittance $jB$ is in parallel with $R_L + jX$:

$$
Y_{in} = jB + \frac{R_L - jX}{R_L^2 + X^2} .
$$

Setting $Y_{in} = 1/50$:

- The real part requires $R_L/(R_L^2 + X^2) = 1/50$, so $X^2 = R_L(50 - R_L)$ and $X = R_L\sqrt{50/R_L - 1} = QR_L$, with $Q = \sqrt{R_{high}/R_{low} - 1}$.
- The imaginary part requires $B = X/(R_L^2 + X^2) = X/(50R_L) = Q/50$, so the shunt reactance is $50/Q$.

Here $Q = \sqrt{50/12.5 - 1} = \sqrt3 = 1.732$. So:

- $X_L = 21.65$ Ω, giving $L = 21.65/(2\pi\times2.4\ \text{GHz}) = $ **1.436 nH**;
- $X_C = 28.87$ Ω, giving $C = 1/(2\pi\times2.4\ \text{GHz}\times28.87) = $ **2.297 pF**.

(c) From port 1 (the 50 Ω side), the network is the shunt capacitor followed by the series inductor:

$$
\begin{bmatrix}1 & 0\\ j/28.87 & 1\end{bmatrix}\begin{bmatrix}1 & j21.65\\ 0 & 1\end{bmatrix} = \begin{bmatrix}1 & j21.65\\ j0.03464 & 0.25\end{bmatrix} .
$$

The 0.25 is $1 - 21.65/28.87 = 1 - Q^2/4$. Then

$$
Z_{in} = \frac{AZ_L + B}{CZ_L + D} = \frac{12.5 + j21.65}{0.25 + j0.4330} = \textbf{50 Ω} ,
$$

because the numerator is exactly 50 times the denominator.

(d) Repeat the ABCD calculation at the new frequencies:

- At 2.2 GHz: $Z_{in} = 42.47 + j8.078$ Ω, so $\lvert\Gamma\rvert = $ **0.1189** and the return loss is **18.49 dB**.
- At 2.6 GHz: $Z_{in} = 53.33 - j13.03$ Ω, so $\lvert\Gamma\rvert = $ **0.1291** and the return loss is **17.78 dB**.

**Yes**, both band edges beat 10 dB comfortably. A $Q$ of 1.73 is low, so the match is broadband. A larger impedance ratio would raise $Q$ and narrow it, and two L-sections through an intermediate impedance lower each section's $Q$.

**15.** *(07-01, 07-07, 07-08, 07-11)* **Rubric:** 2 points per claim, 1 for identifying the flaw and 1 for a question that would expose it. Each part lists the minimum acceptable flaw first; any one of the other points earns the flaw point too. A question earns its point if the answer to it would confirm or refute the claim with data.

(a) **Minimum flaw:** capacitance alone does not set the impedance at 1 GHz; inductance does. Other acceptable points:

- Every capacitor has ESL and becomes an inductor above its self-resonant frequency, which for board capacitors lies far below 1 GHz (Example 07-01.5: 2.251 MHz for a 10 µF ceramic with 0.5 nH).
- Board capacitors cannot reach the die through the package and via inductance at 1 GHz; that job falls to package and on-die capacitance.
- Class II ceramics lose much of their capacitance under DC bias, so the nominal 2,000 µF overstates what the rail has.

*Ask:* "What is the measured or simulated impedance profile of the power-delivery network from DC to 1 GHz, against your target impedance?"

(b) **Minimum flaw:** $\sqrt3V_LI_L = \sqrt3\times415\times30 = $ **21.56 kVA** is the apparent power at 100% of the breaker rating; it equals 21.56 kW only at unity power factor. Other acceptable points:

- Continuous loads are commonly limited to 80% of the rating, which gives **17.25 kVA** (07-11 §9).
- Real power is lower than the apparent power by the power factor.
- Power-supply efficiency and redundancy (A/B feeds, each sized to carry the whole rack) cut the usable IT load further.

*Ask:* "What continuous derating, power factor and redundancy scheme does the 21.6 kW figure assume?"

(c) **Minimum flaw:** at the −3 dB frequency a single 1 MHz tone is already reduced to 70.7% of its amplitude (**29.3%** lost) and phase-shifted. A pure tone keeps its shape, so accept "attenuated and phase-shifted" as the flaw. The phase shift is 45° for a first-order filter and 90° for a second-order Butterworth. Other acceptable points:

- A real signal has bandwidth around 1 MHz, and its components near the corner are attenuated and delayed by different amounts, which does distort it (group-delay variation).
- A signal that must pass unchanged needs the passband edge well above it, with a flatness specification.

*Ask:* "What are the passband flatness and group-delay variation over the signal's actual band?"

(d) **Minimum flaw:** at unity gain the loop's crossover sits closest to the op-amp's higher poles, so the phase margin is smallest there (Question 8). The buffer may peak, overshoot or oscillate, especially with a capacitive load. Other acceptable points:

- The GBW predicts the bandwidth only for a single-pole amplifier.
- Large signals are limited by the slew rate, not by the GBW.

*Ask:* "What are the phase margin and step response at unity gain with our actual load capacitance, and what are the slew rate and full-power bandwidth?"

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X07.1a | capacitor current | 25 | mA |
| X07.1b | inductor voltage | 30 | V |
| X07.1c | inductor energy at 3 A | 450 | µJ |
| X07.1d | series capacitance | 1.499 | µF |
| X07.1e | voltage on 4.7 µF | 3.826 | V |
| X07.1f | voltage on 2.2 µF | 8.174 | V |
| X07.1g | minimum bulk capacitance | 40 | µF |
| X07.2a | time constant | 1 | ms |
| X07.2b | capacitor voltage at 2 ms | 2.853 | V |
| X07.2c | 10–90% rise time | 2.197 | ms |
| X07.2d | −3 dB bandwidth | 159.2 | Hz |
| X07.2e | rise time × bandwidth | 0.3497 | — |
| X07.2f | 12-bit settling time | 9.011 | ms |
| X07.2g | energy dissipated in R | 544.5 | nJ |
| X07.3a | v_C(0−) | 9 | V |
| X07.3b | final value, S closed | 6 | V |
| X07.3c | time constant, S closed | 20 | ms |
| X07.3d | current in R3 at 0+ | 1.5 | mA |
| X07.3e | capacitor current at 0+ | −1.5 | mA |
| X07.3f | time to reach 7 V | 21.97 | ms |
| X07.3g | v_C at 40 ms | 6.406 | V |
| X07.3h | time constant, S open | 30 | ms |
| X07.3i | v_C at 100 ms | 8.649 | V |
| X07.4a | ω0 | 31623 | rad/s |
| X07.4b | f0 | 5033 | Hz |
| X07.4c | α | 10000 | 1/s |
| X07.4d | ζ | 0.3162 | — |
| X07.4e | Q | 1.581 | — |
| X07.4f | ω_d | 30000 | rad/s |
| X07.4g | f_d | 4775 | Hz |
| X07.4h | overshoot | 35.09 | % |
| X07.4i | peak capacitor voltage | 13.51 | V |
| X07.4j | time of voltage peak | 104.7 | µs |
| X07.4m | resistance for critical damping | 63.25 | Ω |
| X07.4n | ζ for 5% overshoot | 0.6901 | — |
| X07.4o | resistance for 5% overshoot | 43.65 | Ω |
| X07.5a | capacitor voltages at 0− | 2 | V |
| X07.5b | damping ratio | 1.5 | — |
| X07.5c | slow pole | −382.0 | 1/s |
| X07.5d | fast pole | −2618 | 1/s |
| X07.5e | slow-pole coefficient | −3.512 | V |
| X07.5f | fast-pole coefficient | 0.5125 | V |
| X07.5g | v_3 at 1 ms | 2.640 | V |
| X07.5h | v_3 at 2 ms | 3.367 | V |
| X07.5i | v_3(0+) | 2 | V |
| X07.5j | dv_3/dt(0+) | 0 | V/s |
| X07.5k | v_3(∞) | 5 | V |
| X07.6a | Z_L | 100 | Ω |
| X07.6b | Z_C (reactance) | −10 | Ω |
| X07.6c | Re Z_in | 32.20 | Ω |
| X07.6d | Im Z_in | −9.756 | Ω |
| X07.6e | amplitude of v_2 | 4.642 | V |
| X07.6f | phase of v_2 | −21.80 | ° |
| X07.6g | amplitude of i_R2 | 0.3283 | A |
| X07.6h | phase of i_R2 | 23.20 | ° |
| X07.6i | power in R2 | 0.5388 | W |
| X07.6j | power delivered by the source | 1.422 | W |
| X07.6k | Thévenin amplitude | 9.806 | V |
| X07.6l | Thévenin phase | 11.31 | ° |
| X07.6m | R_Th | 19.23 | Ω |
| X07.6n | X_Th | −6.154 | Ω |
| X07.6o | maximum power | 0.6250 | W |
| X07.6p | Re Z_p | 12.195 | Ω |
| X07.6q | Im Z_p | −9.756 | Ω |
| X07.6r | source current amplitude | 0.2973 | A |
| X07.6s | source current phase | 16.86 | ° |
| X07.6t | power in R1 | 0.8836 | W |
| X07.7a | apparent power | 13.33 | kVA |
| X07.7b | reactive power | 8.819 | kvar |
| X07.7c | line current | 57.97 | A |
| X07.7d | reactive power at PF 0.95 | 3.287 | kvar |
| X07.7e | capacitor reactive power | 5.532 | kvar |
| X07.7f | correction capacitance | 332.9 | µF |
| X07.7g | new line current | 45.77 | A |
| X07.7h | loss reduction | 37.67 | % |
| X07.7i | RMS current with harmonics | 10.55 | A |
| X07.7j | THD | 33.54 | % |
| X07.7k | power factor with harmonics | 0.9481 | — |
| X07.7l | loss ratio after correction | 0.6233 | — |
| X07.8a | exact gain at 10³ rad/s | 2.967 | dB |
| X07.8b | exact gain at 10⁴ rad/s | 17.03 | dB |
| X07.8c | frequency of maximum lead | 3162 | rad/s |
| X07.8d | maximum phase lead | 54.90 | ° |
| X07.8e | gain at maximum lead | 10.00 | dB |
| X07.8f | gain–bandwidth product | 1 | MHz |
| X07.8g | crossover, unity gain | 910.2 | kHz |
| X07.8h | phase margin, unity gain | 65.53 | ° |
| X07.8i | crossover, gain 10 | 99.88 | kHz |
| X07.8j | phase margin, gain 10 | 87.15 | ° |
| X07.9a | f0 | 1.592 | MHz |
| X07.9b | Q | 20 | — |
| X07.9c | bandwidth | 79.58 | kHz |
| X07.9d | capacitor voltage at resonance | 20 | V |
| X07.9e | gain at 1.5 MHz | −8.210 | dB |
| X07.9f | phase at 1.5 MHz | 67.13 | ° |
| X07.9g | gain at 1.7 MHz | −9.011 | dB |
| X07.9h | phase at 1.7 MHz | −69.24 | ° |
| X07.9i | C_2 | 11.25 | nF |
| X07.9j | C_1 | 22.51 | nF |
| X07.9k | Sallen–Key gain at 1 kHz | −3.010 | dB |
| X07.9l | second-order attenuation at 3 kHz | 19.14 | dB |
| X07.9m | minimum order (continuous) | 4.192 | — |
| X07.9n | lowest Butterworth order | 5 | — |
| X07.9o | fifth-order attenuation at 3 kHz | 47.71 | dB |
| X07.10a | coupling coefficient | 0.9 | — |
| X07.10b | series aiding | 8.6 | mH |
| X07.10c | series opposing | 1.4 | mH |
| X07.10d | Re reflected impedance | 99.19 | Ω |
| X07.10e | Im reflected impedance | −124.6 | Ω |
| X07.10f | Im Z_in | 126.7 | Ω |
| X07.10g | current ratio | 1.408 | — |
| X07.10h | turns ratio | 10 | — |
| X07.10i | full-load efficiency | 96.62 | % |
| X07.10j | load fraction for maximum efficiency | 0.6325 | — |
| X07.10k | maximum efficiency | 96.93 | % |
| X07.11a | z11 | 110 | Ω |
| X07.11b | z21 | 100 | Ω |
| X07.11c | z22 | 120 | Ω |
| X07.11d | A | 1.1 | — |
| X07.11e | B | 32 | Ω |
| X07.11f | C | 0.01 | S |
| X07.11g | D | 1.2 | — |
| X07.11h | AD − BC | 1 | — |
| X07.11i | input impedance | 51.18 | Ω |
| X07.11j | voltage gain | 0.5747 | — |
| X07.11k | S11 | 0.01163 | — |
| X07.11l | S21 | 0.5814 | — |
| X07.11m | S22 | 0.06977 | — |
| X07.11n | insertion loss | 4.711 | dB |
| X07.11o | return loss | 38.69 | dB |
| X07.11q | port-2 impedance | 57.5 | Ω |
| X07.12a | phase current | 8 | A |
| X07.12b | line current | 13.86 | A |
| X07.12c | real power | 5760 | W |
| X07.12d | reactive power | 7680 | var |
| X07.12e | power factor | 0.6 | — |
| X07.12f | W1 | 663.0 | W |
| X07.12g | W2 | 5097 | W |
| X07.12h | C per phase, Y | 152.8 | µF |
| X07.12i | new line current | 8.314 | A |
| X07.12j | C per phase, Δ | 50.93 | µF |
| X07.13a | f0 | 15.65 | kHz |
| X07.13b | Z0 | 0.2164 | Ω |
| X07.13c | Q at 1 Ω | 4.622 | — |
| X07.13d | gain at f0, 1 Ω | 13.30 | dB |
| X07.13e | DC output | 3 | V |
| X07.13f | switch-node fundamental | 5.402 | V |
| X07.13g | output ripple with ESR | 9.355 | mV |
| X07.13h | output ripple without ESR | 5.298 | mV |
| X07.13i | ESR zero | 338.6 | kHz |
| X07.13j | time of peak droop | 14.96 | µs |
| X07.13k | peak droop | 0.3690 | V |
| X07.13l | ΔI·Z0 estimate | 0.4327 | V |
| X07.13m | Q at 10 Ω | 46.22 | — |
| X07.13n | gain at f0, 10 Ω | 33.30 | dB |
| X07.13o | α at 10 Ω | 1064 | 1/s |
| X07.13p | envelope time constant at 10 Ω | 0.940 | ms |
| X07.13q | ringing period at 10 Ω | 63.9 | µs |
| X07.13r | α at 1 Ω | 10638 | 1/s |
| X07.13s | ω_d at 1 Ω | 97765 | rad/s |
| X07.13t | ζ at 1 Ω | 0.108 | — |
| X07.14a | Γ unmatched | −0.6 | — |
| X07.14b | return loss unmatched | 4.437 | dB |
| X07.14c | mismatch loss unmatched | 1.938 | dB |
| X07.14d | Q of the L-section | 1.732 | — |
| X07.14e | L | 1.436 | nH |
| X07.14f | C | 2.297 | pF |
| X07.14g | Z_in at 2.4 GHz | 50 | Ω |
| X07.14h | magnitude of Γ at 2.2 GHz | 0.1189 | — |
| X07.14i | return loss at 2.2 GHz | 18.49 | dB |
| X07.14j | magnitude of Γ at 2.6 GHz | 0.1291 | — |
| X07.14k | return loss at 2.6 GHz | 17.78 | dB |
| X07.14n | Re Z_in at 2.2 GHz | 42.47 | Ω |
| X07.14o | Im Z_in at 2.2 GHz | 8.078 | Ω |
| X07.14p | Re Z_in at 2.6 GHz | 53.33 | Ω |
| X07.14q | Im Z_in at 2.6 GHz | −13.03 | Ω |
| X07.15a | apparent power of a 30 A, 415 V feed | 21.56 | kVA |
| X07.15b | 80% continuous rating | 17.25 | kVA |
| X07.15c | amplitude lost at the −3 dB frequency | 29.3 | % |
