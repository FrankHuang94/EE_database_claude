# Solutions 07-03 · Second-Order RLC Transients

Problems: [07-03 problems](../problems/07-03-problems.md) · Chapter: [07-03](../chapters/07-03-second-order-rlc-transients.md). Every number below is recomputed by [verify_07_03.py](../verify/verify_07_03.py), mostly by integrating the circuit's state equations numerically; values marked † are also confirmed by an ngspice netlist in [labs/07-03-lab](../labs/07-03-lab/README.md).

---

## Solutions

### Solution 07-03.1

$\omega_0 = 1/\sqrt{2\times10^{-3}\times50\times10^{-9}} = 1/\sqrt{10^{-10}} = $ **100.0 krad/s**, $f_0 = $ **15.92 kHz**. $Z_0 = \sqrt{2\times10^{-3}/50\times10^{-9}} = \sqrt{4\times10^4} = $ **200.0 Ω**. α = $R/(2L) = 150/(4\times10^{-3}) = $ **37.50 × 10³ s⁻¹**, ζ = $R/(2Z_0) = 150/400 = $ **0.3750**, underdamped, $Q = 1/(2\zeta) = $ **1.333**, and $\omega_d = \sqrt{10^{10} - 1.406\times10^9} = $ **92.70 krad/s**. Critical damping needs $R = 2Z_0 = $ **400.0 Ω**.

### Solution 07-03.2

(a) $Z_0 = \sqrt{50\times10^{-6}/200\times10^{-9}} = \sqrt{250} = $ **15.81 Ω**. A parallel tank is critically damped when $Z_0/(2R) = 1$: $R = Z_0/2 = $ **7.906 Ω**.

(b) ζ = $Z_0/(2R) = 15.81/100 = $ **0.1581**, $Q = R/Z_0 = $ **3.162**, α = $1/(2RC) = 1/(2\times50\times200\times10^{-9}) = $ **50.00 × 10³ s⁻¹** and $\omega_0 = 1/\sqrt{10^{-11}} = $ **316.2 krad/s**.

(c) **Smaller.** A parallel resistor damps by draining the tank, so lowering it toward 7.9 Ω increases ζ. Raising it reduces the damping.

### Solution 07-03.3

Continuity gives $i(0^+) = i(0^-) = $ **0** and $v_C(0^+) = $ **4 V**. In the $0^+$ circuit no current flows, so $v_R(0^+) = $ **0**, and KVL around the loop puts the rest of the source voltage across the inductor: $v_L(0^+) = 10 - 0 - 4 = $ **6 V**. The slopes: $di/dt(0^+) = v_L(0^+)/L = 6/(5\times10^{-3}) = $ **1200 A/s**; $dv_C/dt(0^+) = i(0^+)/C = $ **0**; $v_R = Ri$, so $dv_R/dt(0^+) = R\,di/dt(0^+) = 20\times1200 = $ **24 000 V/s**. Final values: the capacitor blocks DC, so $i(\infty) = $ **0** and $v_C(\infty) = $ **10 V**.

### Solution 07-03.4

(a) $\omega_0 = 1/\sqrt{10^{-3}\times10^{-5}} = 10^4$ rad/s; α = $R/(2L) = 2/(2\times10^{-3}) = $ **1000 s⁻¹**; ζ = **0.1000**; $\omega_d = \sqrt{10^8 - 10^6} = $ **9950 rad/s**; $Z_0 = \sqrt{10^{-3}/10^{-5}} = $ **10.00 Ω**.

(b) Take $i$ flowing out of the capacitor's + terminal around the loop. At $0^+$, $i = 0$ and the full 100 V appears across the inductor, so $di/dt(0^+) = 100/10^{-3} = 10^5$ A/s, and the final current is 0. By the underdamped master formula with $D = 0$:

$$
i(t) = \frac{V_0}{\omega_dL}e^{-\alpha t}\sin\omega_dt = 10.05\,e^{-1000t}\sin(9950t)\ \text{A}.
$$

(c) As in chapter §3.7, the peak is at $\omega_dt = \arccos\zeta$: $t = 1.4706/9950 = $ **147.8 µs**, with $i_{pk} = (V_0/Z_0)\exp\big(-\zeta\arccos\zeta/\sqrt{1 - \zeta^2}\big) = 10\,e^{-0.1478} = $ **8.626 A**.

(d) The current returns to zero at $t = \pi/\omega_d = $ **315.7 µs**. Then $v_C = -V_0e^{-\alpha\pi/\omega_d} = -100\,e^{-0.3157} = $ **−72.92 V**: the capacitor has been charged the other way. The energy still stored is $(72.92/100)^2 = $ **53.18%** of the original.

(e) In an underdamped discharge the current overshoots and recharges the capacitor in reverse, here to 73% of the original voltage. Many capacitors (electrolytics in particular, but also film and ceramic types in pulse service) are damaged or aged by reverse voltage, so pulse capacitors state how much reversal they tolerate, and pulse circuits add damping or a reverse diode.

### Solution 07-03.5

(a) $R = 2\sqrt{L/C} = 2\sqrt{10} = $ **6.325 Ω**.

(b) The critically damped step response from rest is $v_C = 1 - (1 + \omega_0t)e^{-\omega_0t}$ (02-03). Solving $(1 + x)e^{-x} = 0.1$ numerically gives $x = 3.890$, so with $\omega_0 = 1/\sqrt{10^{-11}} = 316.2$ krad/s, $t_{90} = 3.890/316\,228 = $ **12.30 µs**.

(c) With ζ = 2, α = $2\omega_0$ and the roots are $s_{1,2} = \omega_0(-2 \pm \sqrt3)$, so $s_1 = -0.2679\,\omega_0$ and $s_2 = -3.732\,\omega_0$. The overdamped step response $v_C = 1 + (s_2e^{s_1t} - s_1e^{s_2t})/(s_1 - s_2)$ reaches 0.9 at **28.05 µs**, **2.281** times slower. Heavy damping costs speed: the slow root moves toward zero as ζ grows, and the response creeps at its pace.

### Solution 07-03.6

(a) $\omega_0 = 1/\sqrt{10^{-2}\times10^{-8}} = $ **100.0 krad/s**, $Z_0 = \sqrt{10^{-2}/10^{-8}} = $ **1000 Ω**, ζ = $Z_0/(2R) = 1000/4000 = $ **0.2500**, α = $1/(2RC) = $ **25.00 × 10³ s⁻¹**.

(b) KCL at the top node with $v = L\,di_L/dt$: $I = v/R + i_L + C\dot v = (L/R)\dot i_L + i_L + LC\ddot i_L$, so

$$
\ddot i_L + 2\alpha\dot i_L + \omega_0^2i_L = \omega_0^2I ,
$$

the standard all-pole step equation with final value $I$, starting from rest ($i_L(0^+) = 0$; $\dot i_L(0^+) = v(0^+)/L = 0$). So OS = $e^{-\pi(0.25)/0.9682} = 44.43\%$ and the peak is $2\times1.4443 = $ **2.889 mA**† at $t_p = \pi/\omega_d = $ **32.45 µs**.

(c) $v = L\,di_L/dt = L\,I\dfrac{\omega_0^2}{\omega_d}e^{-\alpha t}\sin\omega_dt = IZ_0\dfrac{\omega_0}{\omega_d}e^{-\alpha t}\sin\omega_dt$. Its peak is at $\omega_dt = \arccos\zeta$, $t = $ **13.61 µs**, with value $IZ_0\exp\big(-\zeta\arccos\zeta/\sqrt{1 - \zeta^2}\big) = 2\text{ V}\times e^{-0.3404} = $ **1.423 V**†.

(d) Duality: in a series RLC hit by a voltage step, the *current* peaks near $V/Z_0$; in a parallel RLC hit by a current step, the *voltage* peaks near $IZ_0$. The all-pole variable is the capacitor voltage in series and the inductor current in parallel.

### Solution 07-03.7

(a) In DC steady state the inductor is a short and the capacitor open, so the source sees $R_1 + R_2 = 6$ Ω: $i_L(0^-) = $ **2.000 A** and $v_C(0^-) = 2\times4 = $ **8.000 V**.

(b) With $R_2$ gone, the source, $R_1$, $L$ and $C$ form a **series RLC** driven by 12 V. α = $R_1/(2L) = 2/(10^{-3}) = $ **2000 s⁻¹**, $\omega_0 = 1/\sqrt{0.5\times10^{-3}\times50\times10^{-6}} = $ **6325 rad/s**, ζ = **0.3162**, $\omega_d = \sqrt{4\times10^7 - 4\times10^6} = $ **6000 rad/s**.

(c) By continuity $v_C(0^+) = 8$ V, and the capacitor current at $0^+$ is the inductor current (series loop now): $dv_C/dt(0^+) = 2/(50\times10^{-6}) = $ **40 000 V/s**. Finally the capacitor blocks DC, so $v_C(\infty) = $ **12 V**.

(d) $D = 8 - 12 = -4$ V and $(\dot v_C(0^+) + \alpha D)/\omega_d = (40\,000 - 8000)/6000 = 5.333$ V:

$$
v_C(t) = 12 + e^{-2000t}\big(-4\cos6000t + 5.333\sin6000t\big)\ \text{V},
$$

so $v_C(0.5\text{ ms}) = $ **13.73 V**.

(e) The extremes satisfy $\tan\omega_dt = \omega_d\dot v_C(0^+)/(\alpha\dot v_C(0^+) + \omega_0^2D) = 6000\times40\,000/(8\times10^7 - 1.6\times10^8) = -3$. The ratio is negative, so $\omega_dt = \pi - \arctan3 = 1.8925$ and $t = $ **315.4 µs**, where $v_C = $ **15.37 V**†. The capacitor started *below* its final value but already charging fast (2 A), so it overshoots by 28% of the 12 V final value.

### Solution 07-03.8

(a) Replace $C$ by a source $v$ and $L$ by a source $i_L$. KCL at node a and KVL around the inductor branch:

$$
C\dot v = \frac{V - v}{R_1} - i_L, \qquad L\dot i_L = v - R_2i_L, \qquad
\mathbf{A} = \begin{pmatrix}-1/(R_1C) & -1/C\\ 1/L & -R_2/L\end{pmatrix} = \begin{pmatrix}-10^4 & -10^6\\ 100 & -1000\end{pmatrix}.
$$

(b) $\operatorname{tr}\mathbf{A} = -11\,000$ s⁻¹, so α = **5500 s⁻¹**; $\det\mathbf{A} = 10^7 + 10^8 = 1.1\times10^8$ s⁻², so $\omega_0 = $ **10.49 krad/s**; ζ = **0.5244**; $\omega_d = $ **8930 rad/s**.

(c) At DC, $v(\infty) = 11\times10/110 = $ **1.000 V** and $i_L(\infty) = 11/110 = $ **0.1000 A**. At $0^+$, $v = 0$ and $i_L = 0$, so the whole input current $11/100$ A charges $C$: $\dot v(0^+) = 0.11/10^{-6} = $ **1.100 × 10⁵ V/s**.

(d) $D = -1$ V and $(\dot v(0^+) + \alpha D)/\omega_d = (110\,000 - 5500)/8930 = 11.70$ V, so $v(t) = 1 + e^{-5500t}\big(-\cos8930t + 11.70\sin8930t\big)$ V. The first extreme is where $\tan\omega_dt = 8930\times1.1\times10^5/(5500\times1.1\times10^5 - 1.1\times10^8) = 1.984$, at $t = $ **123.6 µs**, with $v = $ **6.066 V**†.

(e) The 02-03 formula would give a peak of $1\times(1 + e^{-\pi\zeta/\sqrt{1 - \zeta^2}}) = 1.144$ V. The real peak is five times higher. The formula assumes an all-pole response starting from rest with zero slope; here $v$ starts with a large slope, because the capacitor is charged directly through $R_1$ long before the inductor's current builds up. In transfer-function language (07-04), $v$'s response has a zero from the $R_2$–$L$ branch. The circuit's ζ is the same for every variable; the waveform's overshoot is not.

### Solution 07-03.9

(a) As in Example 07-03.6, with $a = -(1/R_1 + 1/R_2)/C_1 = -(10^{-3} + 5\times10^{-4})/(2\times10^{-6}) = -750$, $b = 1/(R_2C_1) = 250$, $c = 1/(R_2C_2) = 1000$, $d = -1000$ (all in s⁻¹):

$$
\mathbf{A} = \begin{pmatrix}-750 & 250\\ 1000 & -1000\end{pmatrix}\ \text{s}^{-1}, \qquad \operatorname{tr}\mathbf{A} = -1750, \quad \det\mathbf{A} = 750\,000 - 250\,000 = 500\,000 .
$$

So α = 875 s⁻¹, $\omega_0 = 707.1$ s⁻¹, ζ = **1.237**, and $s_{1,2} = -875 \pm \sqrt{765\,625 - 500\,000} = -875 \pm 515.4$: **−359.6 s⁻¹** and **−1390 s⁻¹**.

(b) $-1/s_1 - 1/s_2 = -\operatorname{tr}\mathbf{A}/\det\mathbf{A} = 1750/500\,000 = $ **3.500 ms**, and $R_1(C_1 + C_2) + R_2C_2 = 10^3\times2.5\times10^{-6} + 2\times10^3\times0.5\times10^{-6} = 3.5$ ms ✓.

(c) In general $a = -(1/R_1 + 1/R_2)/C_1$, $b = 1/(R_2C_1)$, $c = 1/(R_2C_2)$ and $d = -1/(R_2C_2)$. The discriminant of $s^2 - (a + d)s + (ad - bc) = 0$ is $(a + d)^2 - 4(ad - bc) = (a - d)^2 + 4bc$. Since $bc = 1/(R_2^2C_1C_2) > 0$, the discriminant is strictly positive: two distinct real roots. Both are negative because $\operatorname{tr}\mathbf{A} < 0$ and $\det\mathbf{A} = 1/(R_1R_2C_1C_2) > 0$. The circuit is overdamped for all positive values.

### Solution 07-03.10

(a) $(f_1/f_2)^2 = 4$, so $C = 470/(4 - 1) = $ **156.7 pF**. Then $L = 1/\big((2\pi\times120\times10^6)^2\times156.7\times10^{-12}\big) = $ **11.23 nH**, and $Z_0 = \sqrt{11.23\times10^{-9}/156.7\times10^{-12}} = $ **8.466 Ω**.

(b) $R_d$ = **8.2 Ω** (the nearest E12 value) and $C_d \approx 4\times156.7 = 627$ pF, so **680 pF**. This is the procedure of Todd's Unitrode paper and TI's SLVA255 ([R-113](../../../reference/research-log.md#r-113--rc-snubbers-and-gate-drive-damping)).

(c) $P = C_dV^2f_{sw} = 680\times10^{-12}\times400^2\times10^5 = $ **10.88 W**.

(d) Ten watts in one resistor is a lot of heat in a small part, and it is efficiency lost on every cycle (a 500 W converter loses about 2% to this alone). At high voltage the $V^2$ makes RC snubbers expensive. Designers then reduce the cause rather than absorb it: a tighter layout or better package to cut $L$ (raising $f_0$ and lowering $Z_0$, so less energy rings), a smaller snubber accepting more overshoot, a clamp that only absorbs the overshoot energy (an RCD clamp, Course 22), or soft-switching topologies that avoid hard edges altogether.

### Solution 07-03.11

(a) The electrolytic's capacitance is an ideal capacitor in series with its ESR, connected across the ceramic: exactly the RC damper of chapter §3.10, with $C_d$ = 47 µF (4.7 times the ceramic) and $R_d = R_b$. The rule is $R_b \approx Z_0 = \sqrt{L/C} = $ **0.3162 Ω** of the original tank, with $C_d$ several times $C$.

(b) KVL along the cable, KCL at the input node and at the electrolytic's internal node:

$$
L\dot i_L = V - Ri_L - v_C, \qquad C\dot v_C = i_L - \frac{v_C - v_b}{R_b}, \qquad C_b\dot v_b = \frac{v_C - v_b}{R_b}.
$$

(c) Simulating from rest with a 12 V step: peak **15.07 V**† with 0.1 Ω, **13.70 V**† with 0.3 Ω and **17.17 V**† with 1.0 Ω. With 0.3 Ω the input stays within ±2% of 12 V after **23.3 µs**, against about 150 µs without the electrolytic. The price is a larger inrush: the cable current now peaks at **41.23 A**† (against 33.71 A), because it charges 57 µF instead of 10 µF.

(d) 0.3 Ω, essentially $Z_0$, is the best of the three (a finer search puts the optimum near 0.25 Ω), confirming the rule. Too little ESR and the electrolytic simply joins the ceramic as a larger, still lightly damped capacitance (a new tank with $L$, ringing more slowly); too much ESR and the damper is disconnected at the ringing frequency, so the ceramic rings almost as before.

(e) A series resistor raises the loop resistance to 0.35 Ω, so ζ = $0.35/(2\times0.3162) = 0.5534$ and OS = $e^{-\pi(0.5534)/0.8329} = 12.40\%$: a peak of **13.49 V**, slightly lower than the damper's 13.70 V. But at 2 A it drops **0.60 V** and dissipates **1.20 W** continuously. The electrolytic damper costs nothing in steady state, so it is the better fix; a series resistor also worsens the regulation of the supply under load.

### Solution 07-03.12

(a) $Z_0 = \sqrt{8\times10^{-9}/2\times10^{-9}} = $ **2.000 Ω**; ζ = $R/(2Z_0) = 1/4 = $ **0.2500**. The gate voltage is the capacitor voltage of a series RLC, so OS = 44.43% and the gate peaks at $12\times1.4443 = $ **17.33 V**.

(b) $R = 2Z_0 = $ **4.000 Ω**. TI's gate-drive guide gives the same rule as its optimum external gate resistor, $2\sqrt{L_S/C_{ISS}}$ minus the driver and internal gate resistances, with $L_S$ the inductance that resonates with $C_{ISS}$ in the gate-drive loop ([R-113](../../../reference/research-log.md#r-113--rc-snubbers-and-gate-drive-damping)): here, the whole 8 nH loop.

(c) With $\omega_0 = 1/\sqrt{1.6\times10^{-17}} = 2.5\times10^8$ rad/s, the critically damped response $1 - (1 + x)e^{-x}$ reaches 10% at $x = 0.5318$ and 90% at $x = 3.890$, so $t_r = 3.358/\omega_0 = $ **13.43 ns**.

(d) 17.3 V is inside ±20 V, but only by 2.7 V, and real loops add more: the inductance estimate is rough, and the driver's supply itself may overshoot. Raising the external gate resistance to bring the total to 2–4 Ω (ζ = 0.5–1) removes most of the overshoot at the cost of a slower edge and more switching loss; shrinking the gate loop (driver close to the transistor, a Kelvin source connection) lowers $L$ and therefore $Z_0$, which helps both.

### Solution 07-03.13

(a) With no resistance, the capacitor voltage follows $V(1 - \cos\omega_0t)$ and the current $(V/Z_0)\sin\omega_0t$, with $Z_0 = \sqrt{10^{-2}/10^{-6}} = 100$ Ω. The current returns to zero at $t = \pi\sqrt{LC} = $ **314.2 µs**, when the capacitor reaches $2V = $ **800 V**; the diode then blocks, and the capacitor holds 800 V. The peak current is $V/Z_0 = $ **4.000 A**.

(b) The capacitor now starts 600 V below the supply, so the swing is 600 V about the 400 V center: it ends at $400 + 600 = $ **1000 V**, at the same time, with peak current $600/100 = $ **6.000 A**.

(c) From the supply. In (a) the supply delivers $Q = C\Delta v = 800$ µC at 400 V, which is 0.32 J, and the capacitor holds $\tfrac12(10^{-6})(800^2) = 0.32$ J: with no resistance there is no loss. (In (b) the supply delivers 0.48 J, raising the capacitor's energy from 0.02 J to 0.50 J.) The inductor stores energy on the way up and hands it on, so the capacitor ends above the supply. Resonant charging reaches twice the supply voltage with almost no loss (compare the ½CV² loss of charging through a resistor, 07-02 §3.8), which is why radar modulators and pulsed lasers use it to charge their pulse-forming networks.

### Solution 07-03.14

(a) $Z_0 = \sqrt{10^{-3}/10^{-6}} = $ **31.62 Ω**, ζ = $10/63.25 = $ **0.1581**, α = $10/(2\times10^{-3}) = $ **5000 s⁻¹**, $\omega_d = \sqrt{10^9 - 2.5\times10^7} = $ **31.22 krad/s**.

(b) At $0^+$ no current flows and $v_C = 0$, so the whole step is across the inductor.

| Variable | Value at $0^+$ | Slope at $0^+$ |
|---|---|---|
| $v_C$ | 0 | $i/C = 0$ |
| $i$ | 0 | $v_L/L = 5000$ A/s |
| $v_L$ | 5 V | $-RV/L = -50\,000$ V/s |
| $v_R$ | 0 | $R\,di/dt = 50\,000$ V/s |

The slope of $v_L$ follows from $v_L = V - v_R - v_C$: its derivative is $-\dot v_R - \dot v_C = -50\,000$ V/s.

(c) $i_{pk} = (V/Z_0)\exp\big(-\zeta\arccos\zeta/\sqrt{1 - \zeta^2}\big) = 0.1581\times0.7976 = $ **126.1 mA**†, at $t = \arccos\zeta/\omega_d = $ **45.22 µs**.

(d) $v_L$ has $D = 5$ V (final value 0) and slope $-50\,000$ V/s, so its extremes satisfy $\tan\omega_dt = 31\,225\times(-50\,000)/\big(5000\times(-50\,000) + 10^9\times5\big) = -0.3287$. The ratio is negative, so $\omega_dt = \pi - 0.3175 = 2.824$: $t = $ **90.44 µs**, where $v_L = $ **−3.181 V**†.

(e) $v_L = L\,di/dt$, so $v_L$ turns negative exactly when the current starts to fall: at the current peak, $\omega_dt = \arccos\zeta$, that is $t$ = 45.22 µs from (c). By KVL, that is the instant when $v_R + v_C$ reaches $V$, well before the capacitor voltage itself passes $V$ (at $\omega_dt = \pi - \arccos\zeta$, $t = $ **55.39 µs**). From then on the inductor slows the current down, returning its stored energy to the circuit. This happens for every damping, even an overdamped circuit that never overshoots, because the current must return to its final value of zero: a negative inductor voltage simply means the current is falling.

### Solution 07-03.15

(a) $f_0 = 1/(2\pi\sqrt{10^{-15}}) = $ **5.033 MHz**.

(b) The tank sees a net parallel conductance $1/R - g$, so α = $(1/R - g)/(2C) = (10^{-4} - 2\times10^{-4})/(2\times10^{-9}) = $ **−50.00 × 10³ s⁻¹**. A negative α means the envelope $e^{-\alpha t}$ *grows*: the amplifier supplies more energy per cycle than the resistor removes, and the roots sit in the right half-plane (02-03 §3.9).

(c) Growth time constant $1/\lvert\alpha\rvert = $ **20.00 µs**; from 1 mV to 1 V takes $20\ \mu\text{s}\times\ln1000 = $ **138.2 µs**, about **695** cycles at 5.033 MHz.

(d) $g = 1/R = $ **0.1000 mS** makes α = 0, an undamped sinusoid. In a real oscillator the amplifier's gain falls as the amplitude grows (it saturates or is regulated), so the effective $g$ settles exactly at $1/R$ at some amplitude; 12-09 analyzes this amplitude limiting.

### Solution 07-03.16

(a) $f_0 = 1/(2\pi\sqrt{150\times10^{-9}\times10.8\times10^{-12}}) = $ **125.0 MHz**; $Z_0 = \sqrt{150\times10^{-9}/10.8\times10^{-12}} = $ **117.9 Ω**; ζ = $R/(2Z_0) = 50/235.7 = $ **0.2121**.

(b) The probe's capacitor voltage is what the scope sees, and it is the all-pole variable of a series RLC, so a fast step overshoots by $e^{-\pi(0.2121)/0.9772} = $ **50.6%**, ringing at about 125 MHz. None of that is in the circuit.

(c) With 15 nH: $f_0 = $ **395.4 MHz**, $Z_0 = $ **37.27 Ω**, ζ = $50/74.54 = $ **0.6708**, and the overshoot falls to **5.83%**. Shortening the ground both raises the ring frequency (often above the scope's bandwidth) and lowers $Z_0$, so the same source resistance damps it much more.

(d) A 100 MHz scope attenuates a 125 MHz ring substantially, so much of it may not be seen at all (Tektronix makes this point for its 11 pF, 6-inch example); a 500 MHz scope shows it in full. The danger is the faster scope: it shows ringing that is not in the circuit.

(e) Change the ground-lead length (or switch to a spring) and watch the ringing frequency. If the frequency moves, the ringing belongs to the probe; if it does not, it comes from the circuit (the test Tektronix recommends, [R-114](../../../reference/research-log.md#r-114--oscilloscope-probe-ground-lead-ringing)).

### Solution 07-03.17

(a) Each integrator's inverting input is a virtual ground, so the input currents flow into the feedback network (06-10).

- A1: $(v_{in} + v_3)/R = -C\,\dot v_1 - v_1/R_Q$.
- A2: $v_1/R = -C\,\dot v_2$, so $v_1 = -RC\,\dot v_2$.
- A3: $v_3 = -v_2$.

Substitute $v_1$ and $v_3$ into A1's equation:

$$
\frac{v_{in} - v_2}{R} = RC^2\,\ddot v_2 + \frac{RC}{R_Q}\,\dot v_2
\quad\Longrightarrow\quad
\ddot v_2 + \frac{1}{R_QC}\,\dot v_2 + \frac{1}{(RC)^2}\,v_2 = \frac{v_{in}}{(RC)^2} .
$$

(b) Compare with $\ddot x + 2\alpha\dot x + \omega_0^2x$:

- $\omega_0 = 1/(RC) = $ **10 000 rad/s** ($f_0$ = 1.592 kHz);
- $\alpha = 1/(2R_QC)$, so $\zeta = \alpha/\omega_0 = R/(2R_Q) = $ **0.1**;
- $Q = R_Q/R = $ **5**.

$R$ and $C$ set the frequency; $R_Q$ alone sets the damping.

(c) The DC gain is 1, so $v_2 \to$ **1 V**. With no zeros and the circuit at rest, the standard formulas apply:

- the overshoot is $e^{-\pi\zeta/\sqrt{1 - \zeta^2}} = e^{-0.3157} = $ **72.92%**;
- the peak is **1.729 V**;
- it occurs at $t_p = \pi/\omega_d = \pi/(10^4\sqrt{0.99}) = $ **315.7 µs**.

(d) $R_Q = QR = R/\sqrt2 = $ **7.071 kΩ** (equivalently $R/(2\zeta)$ with $\zeta = 1/\sqrt2$). The overshoot falls to $e^{-\pi} = $ **4.321%**.

(e) The op-amps are active elements. They supply energy, and, more to the point, the loop is not a reciprocal resistor network. The current into A1 depends on $v_3$, but nothing about $v_1$ drives back into A3 the same way, so the symmetry that §3.9's proof needed ($G_{12}$ appearing equally in both equations) is broken. Two integrators in a loop with an inversion behave like an inductor and a capacitor exchanging energy. This **two-integrator loop** is the basis of state-variable and Tow–Thomas active filters, which realize any $\omega_0$ and $Q$ with resistors, capacitors and op-amps alone.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-03.1a | $\omega_0$ | 100.0 | krad/s |
| 07-03.1b | $f_0$ | 15.92 | kHz |
| 07-03.1c | $Z_0$ | 200.0 | Ω |
| 07-03.1d | α | 37.50 | 10³ s⁻¹ |
| 07-03.1e | ζ | 0.3750 | — |
| 07-03.1f | $Q$ | 1.333 | — |
| 07-03.1g | $\omega_d$ | 92.70 | krad/s |
| 07-03.1h | R for critical damping | 400.0 | Ω |
| 07-03.2a | $Z_0$ | 15.81 | Ω |
| 07-03.2b | R for critical damping | 7.906 | Ω |
| 07-03.2c | ζ with 50 Ω | 0.1581 | — |
| 07-03.2d | $Q$ with 50 Ω | 3.162 | — |
| 07-03.2e | α with 50 Ω | 50.00 | 10³ s⁻¹ |
| 07-03.2f | $\omega_0$ | 316.2 | krad/s |
| 07-03.3a | $v_C(0^+)$ | 4 | V |
| 07-03.3b | $v_L(0^+)$ | 6 | V |
| 07-03.3c | $di/dt(0^+)$ | 1200 | A/s |
| 07-03.3d | $dv_R/dt(0^+)$ | 24 000 | V/s |
| 07-03.3e | $v_C(\infty)$ | 10 | V |
| 07-03.4a | α | 1000 | s⁻¹ |
| 07-03.4b | ζ | 0.1000 | — |
| 07-03.4c | $\omega_d$ | 9950 | rad/s |
| 07-03.4d | $Z_0$ | 10.00 | Ω |
| 07-03.4e | time of peak current | 147.8 | µs |
| 07-03.4f | peak current | 8.626 | A |
| 07-03.4g | time of first current zero | 315.7 | µs |
| 07-03.4h | capacitor voltage then | −72.92 | V |
| 07-03.4i | energy still stored | 53.18 | % |
| 07-03.5a | R for critical damping | 6.325 | Ω |
| 07-03.5b | 90 % time, critical | 12.30 | µs |
| 07-03.5c | 90 % time, ζ = 2 | 28.05 | µs |
| 07-03.5d | ratio of the 90 % times | 2.281 | — |
| 07-03.6a | $\omega_0$ | 100.0 | krad/s |
| 07-03.6b | $Z_0$ | 1000 | Ω |
| 07-03.6c | ζ | 0.2500 | — |
| 07-03.6d | α | 25.00 | 10³ s⁻¹ |
| 07-03.6e | peak inductor current | 2.889 | mA |
| 07-03.6f | time of the current peak | 32.45 | µs |
| 07-03.6g | time of the voltage peak | 13.61 | µs |
| 07-03.6h | peak tank voltage | 1.423 | V |
| 07-03.7a | $i_L(0^-)$ | 2.000 | A |
| 07-03.7b | $v_C(0^-)$ | 8.000 | V |
| 07-03.7c | α | 2000 | s⁻¹ |
| 07-03.7d | $\omega_0$ | 6325 | rad/s |
| 07-03.7e | ζ | 0.3162 | — |
| 07-03.7f | $\omega_d$ | 6000 | rad/s |
| 07-03.7g | $dv_C/dt(0^+)$ | 40 000 | V/s |
| 07-03.7h | $v_C(\infty)$ | 12 | V |
| 07-03.7i | $v_C(0.5\text{ ms})$ | 13.73 | V |
| 07-03.7j | time of the peak | 315.4 | µs |
| 07-03.7k | peak $v_C$ | 15.37 | V |
| 07-03.8a | α | 5500 | s⁻¹ |
| 07-03.8b | $\omega_0$ | 10.49 | krad/s |
| 07-03.8c | ζ | 0.5244 | — |
| 07-03.8d | $\omega_d$ | 8930 | rad/s |
| 07-03.8e | $v(\infty)$ | 1.000 | V |
| 07-03.8f | $i_L(\infty)$ | 0.1000 | A |
| 07-03.8g | $dv/dt(0^+)$ | 1.100 | 10⁵ V/s |
| 07-03.8h | time of the peak | 123.6 | µs |
| 07-03.8i | peak $v$ | 6.066 | V |
| 07-03.8j | peak predicted by the all-pole formula | 1.144 | V |
| 07-03.9a | ζ | 1.237 | — |
| 07-03.9b | $s_1$ | −359.6 | s⁻¹ |
| 07-03.9c | $s_2$ | −1390 | s⁻¹ |
| 07-03.9d | sum of time constants | 3.500 | ms |
| 07-03.10a | parasitic capacitance | 156.7 | pF |
| 07-03.10b | loop inductance | 11.23 | nH |
| 07-03.10c | $Z_0$ | 8.466 | Ω |
| 07-03.10d | snubber power | 10.88 | W |
| 07-03.11a | $Z_0$ of the original tank | 0.3162 | Ω |
| 07-03.11b | peak, $R_b$ = 0.1 Ω | 15.07 | V |
| 07-03.11c | peak, $R_b$ = 0.3 Ω | 13.70 | V |
| 07-03.11d | peak, $R_b$ = 1.0 Ω | 17.17 | V |
| 07-03.11e | settling to ±2 %, $R_b$ = 0.3 Ω | 23.3 | µs |
| 07-03.11f | peak with a 0.3 Ω series resistor | 13.49 | V |
| 07-03.11g | series-resistor drop at 2 A | 0.60 | V |
| 07-03.11h | series-resistor power at 2 A | 1.20 | W |
| 07-03.11i | peak cable current, $R_b$ = 0.3 Ω | 41.23 | A |
| 07-03.12a | $Z_0$ | 2.000 | Ω |
| 07-03.12b | ζ | 0.2500 | — |
| 07-03.12c | peak gate voltage | 17.33 | V |
| 07-03.12d | R for critical damping | 4.000 | Ω |
| 07-03.12e | 10–90 % rise time, critical | 13.43 | ns |
| 07-03.13a | time to full charge | 314.2 | µs |
| 07-03.13b | final voltage from 0 V | 800 | V |
| 07-03.13c | peak current from 0 V | 4.000 | A |
| 07-03.13d | final voltage from −200 V | 1000 | V |
| 07-03.13e | peak current from −200 V | 6.000 | A |
| 07-03.14a | $Z_0$ | 31.62 | Ω |
| 07-03.14b | ζ | 0.1581 | — |
| 07-03.14c | α | 5000 | s⁻¹ |
| 07-03.14d | $\omega_d$ | 31.22 | krad/s |
| 07-03.14e | slope of $v_L$ at $0^+$ | −50 000 | V/s |
| 07-03.14f | peak current | 126.1 | mA |
| 07-03.14g | time of the $v_L$ minimum | 90.44 | µs |
| 07-03.14h | minimum $v_L$ | −3.181 | V |
| 07-03.14i | time of the current peak | 45.22 | µs |
| 07-03.14j | time $v_C$ first reaches $V$ | 55.39 | µs |
| 07-03.15a | $f_0$ | 5.033 | MHz |
| 07-03.15b | α | −50.00 | 10³ s⁻¹ |
| 07-03.15c | growth time constant | 20.00 | µs |
| 07-03.15d | time to grow 1000× | 138.2 | µs |
| 07-03.15e | cycles during the growth | 695 | — |
| 07-03.15f | g that just sustains oscillation | 0.1000 | mS |
| 07-03.16a | $f_0$ with the 6-inch lead | 125.0 | MHz |
| 07-03.16b | $Z_0$ with the 6-inch lead | 117.9 | Ω |
| 07-03.16c | ζ with the 6-inch lead | 0.2121 | — |
| 07-03.16d | overshoot with the 6-inch lead | 50.6 | % |
| 07-03.16e | $f_0$ with the spring | 395.4 | MHz |
| 07-03.16f | $Z_0$ with the spring | 37.27 | Ω |
| 07-03.16g | ζ with the spring | 0.6708 | — |
| 07-03.16h | overshoot with the spring | 5.83 | % |
| 07-03.17a | $\omega_0$ | 10000 | rad/s |
| 07-03.17b | ζ | 0.1 | — |
| 07-03.17c | $Q$ | 5 | — |
| 07-03.17d | final value | 1 | V |
| 07-03.17e | overshoot | 72.92 | % |
| 07-03.17f | peak | 1.729 | V |
| 07-03.17g | peak time | 315.7 | µs |
| 07-03.17h | $R_Q$ for a Butterworth response | 7.071 | kΩ |
| 07-03.17i | Butterworth overshoot | 4.321 | % |
