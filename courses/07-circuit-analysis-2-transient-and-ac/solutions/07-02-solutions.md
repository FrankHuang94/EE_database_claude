# Solutions 07-02 · First-Order RC and RL Transients

Problems: [07-02 problems](../problems/07-02-problems.md) · Chapter: [07-02](../chapters/07-02-first-order-rc-rl-transients.md)

Every numerical answer below appears in the answer key at the end. Each one is recomputed by [verify_07_02.py](../verify/verify_07_02.py), and those marked † are also confirmed by an ngspice netlist in [labs/07-02-lab](../labs/07-02-lab/README.md).

---

## Solutions

### Solution 07-02.1

(a) $\tau = RC = (2.2\times10^{3})(47\times10^{-6}) = 0.1034$ s $= 103.4$ ms.
(b) $\tau = L/R = 5\times10^{-3}/50 = 1.00\times10^{-4}$ s $= 100$ µs.
(c) $\tau = RC = (10\times10^{3})(10\times10^{-12}) = 1.00\times10^{-7}$ s $= 100$ ns.
(d) In an RC circuit the resistor limits the current that changes the capacitor's charge, so a larger R slows the transient. In an RL circuit the resistor is what dissipates the inductor's stored energy (at rate $i^2R$), so a larger R drains it faster.

### Solution 07-02.2

(a) The remaining fraction is $e^{-3} = 0.0498$, i.e. **4.98%**.
(b) Need $e^{-t/\tau} = 0.001$, so $t/\tau = \ln 1000 = 6.908$.
(c) Need $e^{-t/\tau} = 0.5$, so $t/\tau = \ln 2 = 0.6931$.

### Solution 07-02.3

**Initial values.** The capacitor is uncharged, so $v_C(0^+) = v_C(0^-) = 0$. In the $0^+$ circuit the capacitor acts as a 0 V source, a short to ground. The 4 kΩ resistor then has 0 V across it and carries no current, and all the current from the source flows into the capacitor: $i_C(0^+) = 10\text{ V}/1\text{ kΩ} = 10.0$ mA.

**Final values.** The capacitor is an open circuit, so the two resistors form a divider: $v_C(\infty) = 10\cdot\frac{4}{1 + 4} = 8.00$ V, and $i_C(\infty) = 0$.

**Time constant.** With the 10 V source shorted, the capacitor sees 1 kΩ ∥ 4 kΩ: $R_{Th} = \frac{1\cdot 4}{1 + 4}$ kΩ $= 800\ \Omega$. So $\tau = 800 \times 1\times10^{-6} = 0.800$ ms.

**Answer.** $v_C(t) = 8\big(1 - e^{-t/0.8\text{ ms}}\big)$ V.

*Check:* $i_C(0^+) = C\,\frac{dv_C}{dt}\big|_{0^+} = (1\,\mu\text{F})\frac{8\text{ V}}{0.8\text{ ms}} = 10$ mA ✓.

### Solution 07-02.4

In DC steady state the inductor is a short, so $v_L = 0$ and $i_L = 9/3 = 3.00$ A. The stored energy is $w = \tfrac{1}{2}Li^2 = \tfrac{1}{2}(2\times10^{-3})(3^2) = 9.00\times10^{-3}$ J $= 9.00$ mJ.

### Solution 07-02.5

The capacitor discharges through $R$: $v(t) = 3.3\,e^{-t/(RC)}$. The requirement is $v(50\text{ ms}) \ge 3.0$ V:

$$
3.3\,e^{-0.05/(RC)} \ge 3.0 \iff \frac{0.05}{RC} \le \ln\frac{3.3}{3.0} = 0.09531 \iff RC \ge \frac{0.05}{0.09531} = 0.5246\ \text{s}.
$$

With $C = 10$ µF: $R \ge 0.5246/10^{-5} = 52.46$ kΩ. The load must draw *less* current than $3.3\text{ V}/52.46\text{ kΩ} \approx 63$ µA, or a larger capacitor is needed.

### Solution 07-02.6

$\tau = RC = (10^4)(10^{-6}) = 10$ ms.

(a) **0 to 5 ms** (charging toward 5 V from 0): $v_C(5\text{ ms}) = 5\big(1 - e^{-0.5}\big) = 5(0.3935) = 1.967$ V.
**After 5 ms** (discharging toward 0 from 1.967 V): $v_C(t) = 1.967\,e^{-(t - 5\text{ ms})/10\text{ ms}}$, so $v_C(15\text{ ms}) = 1.967\,e^{-1} = 0.7237$ V.

(b) At $0^+$: $i = (5 - 0)/10\text{ kΩ} = 0.500$ mA. Just after 5 ms the input is 0 and $v_C = 1.967$ V, so $i = (0 - 1.967)/10\text{ kΩ} = -0.1967$ mA. The current reverses as the capacitor discharges back into the source.

(c) The sketch rises along an exponential to 1.97 V at 5 ms, with initial slope 0.5 V/ms, then decays exponentially through 0.72 V at 15 ms and 0.27 V at 25 ms. The pulse is much shorter than τ, so the capacitor charges only about 39% of the way.

### Solution 07-02.7

(a) Seen from the inductor, with the current source opened, $R_1$ and $R_2$ are in series: $R_{Th} = 10 + 15 = 25\ \Omega$. So $\tau = L/R_{Th} = 0.050/25 = 2.00$ ms. At $t \to \infty$ the inductor is a short, and the 2 A splits between $R_1$ and the branch $R_2$ + short by the current-divider rule: $i_L(\infty) = 2\cdot\frac{R_1}{R_1 + R_2} = 2\cdot\frac{10}{25} = 0.800$ A.

(b) At $0^+$, $i_L = 0$ (continuity). All 2 A flows through $R_1$, so the voltage across the parallel combination is $2 \times 10 = 20$ V. $R_2$ carries no current, so it drops nothing, and the full 20 V appears across the inductor: $v_L(0^+) = 20.0$ V.

(c) $i_L(t) = 0.8\big(1 - e^{-t/2\text{ ms}}\big)$ A, so $i_L(3\text{ ms}) = 0.8(1 - e^{-1.5}) = 0.8(0.7769) = 0.6215$ A.

*Check:* $v_L(0^+) = L\,\frac{di}{dt}\big|_{0^+} = 0.05 \times \frac{0.8}{0.002} = 20$ V ✓.

### Solution 07-02.8

(a) Before $t = 0$, the capacitor is an open circuit and there is no current, so no voltage drops across $R_1$: $v_C(0^-) = 12$ V. Afterwards, $R_1$ and $R_2$ form a divider: $v_C(\infty) = 12\cdot\frac{2}{2 + 2} = 6.00$ V.

(b) The capacitor sees $R_1 \parallel R_2 = 1$ kΩ, so $\tau = (10^3)(5\times10^{-6}) = 5.00$ ms.

(c) $i_{R2}(0^-) = 0$ (the switch is open). At $0^+$, $v_C = 12$ V by continuity, so $i_{R2}(0^+) = 12/2\text{ kΩ} = 6.00$ mA. $R_1$ has 12 V on both ends, so $i_{R1}(0^+) = 0$, and KCL at A gives $i_C(0^+) = i_{R1} - i_{R2} = -6.00$ mA: the capacitor discharges into $R_2$. Finally $i_{R2}(\infty) = 6\text{ V}/2\text{ kΩ} = 3.00$ mA.
**What jumps:** $i_{R2}$ (0 → 6 mA) and $i_C$ (0 → −6 mA). $v_C$ does not.

(d) $v_C(t) = 6 + (12 - 6)e^{-t/5\text{ ms}} = 6 + 6e^{-t/5\text{ ms}}$ V, and $i_{R2}(t) = v_C/2\text{ kΩ} = 3 + 3e^{-t/5\text{ ms}}$ mA.

### Solution 07-02.9

(a) $f_{3dB} \approx 0.35/t_r = 0.35/(3.5\times10^{-9}) = 100$ MHz. The exact single-pole relation $f_{3dB} = \ln 9/(2\pi t_r)$ gives 99.9 MHz, so the 0.35 rule is accurate to 0.1% for one pole.

(b) $\tau = RC = 10^3 \times 10^{-8} = 10$ µs.

- $f_{3dB} = 1/(2\pi\tau) = 1/(2\pi\times10^{-5}) = 15.92$ kHz.
- $t_r = \tau\ln 9 = 21.97$ µs.
- $t_{50} = \tau\ln 2 = 6.931$ µs.

### Solution 07-02.10

(a) From chapter §3.10 with $x(0) = 0$: $x(t) = k(t - \tau) + k\tau\,e^{-t/\tau}$. With $k = 2$ V/ms and $\tau = 1$ ms, $x(t) = 2(t - 1) + 2e^{-t}$ V, with $t$ in ms.

(b) $x(5) = 2(4) + 2e^{-5} = 8 + 0.0135 = 8.013$ V. The input at that moment is 10 V.

(c) Once $e^{-t/\tau} \approx 0$, $x = k(t - \tau)$. That is the input delayed by $\tau = 1$ ms, or equivalently below the input by a constant $k\tau = 2.00$ V.

### Solution 07-02.11

(a) Virtual ground at the inverting input: the input current $v_{in}/R = -1/10^4 = -0.1$ mA flows into the capacitor from the virtual-ground side, so $v_{out}(t) = -\frac{1}{RC}\int_0^t v_{in}\,d\lambda = -\frac{1}{10^{-3}}(-1)t = t/(1\text{ ms})$ V. At $t = 5$ ms, $v_{out} = 5.000$ V.†

(b) The output ramps at 1 V/ms and reaches the +12 V rail at $t = 12.0$ ms. After that, the op-amp can no longer hold a virtual ground and the ideal-integrator model stops applying.

(c) Leaky integrator: $\tau = R_fC = (10^5)(10^{-7}) = 10.0$ ms. The DC gain is $-R_f/R = -10$, so the final value is $(-10)(-1) = 10.0$ V. The output is
$v_{out}(t) = 10\big(1 - e^{-t/10\text{ ms}}\big)$ V, so $v_{out}(10\text{ ms}) = 10(1 - e^{-1}) = 6.321$ V.†
The ideal integrator would read 10 V at 10 ms. The leaky version tracks it initially, since $10(1 - e^{-t/\tau}) \approx t/(1\text{ ms})$ for $t \ll \tau$, then levels off at 10 V instead of hitting the rail.

### Solution 07-02.12

Use $V_{max} = \frac{V}{1 + k}$, $V_{min} = \frac{Vk}{1 + k}$ and ripple $= V\frac{1 - k}{1 + k}$, with $k = e^{-T/(2\tau)}$, $V = 1$ V and $T = 1$ ms.

(a) $\tau = 0.5$ ms: $k = e^{-1} = 0.3679$. So $V_{max} = 1/1.3679 = 0.7311$ V,† $V_{min} = 0.2689$ V,† ripple $= 0.4621$ V.

(b) $\tau = 5$ ms: $k = e^{-0.1} = 0.9048$. So $V_{max} = 1/1.9048 = 0.5250$ V,† $V_{min} = 0.4750$ V,† ripple $= 0.04996$ V. The approximation gives $VT/(4\tau) = 1/20 = 0.0500$ V, which agrees to 0.1%.

(c) The larger τ, because it gives a nearly constant output (here 0.5 V ± 2.5%) equal to the duty cycle × V. The cost is response time: when the PWM duty cycle changes, the output takes about 5τ (25 ms here) to settle to the new level. Ripple and response speed trade off directly. A second-order filter improves the trade ([07-08](../chapters/07-08-filters-and-resonance.md)).

### Solution 07-02.13

(a) The source delivers charge $Q = CV$ at constant voltage $V$, so it supplies energy $W_S = VQ = CV^2$. The capacitor ends with $\tfrac{1}{2}CV^2$. By energy conservation, the resistor dissipates $CV^2 - \tfrac{1}{2}CV^2 = \tfrac{1}{2}CV^2$, for any R. (Directly: $\int_0^\infty (V^2/R)e^{-2t/RC}dt = \tfrac{1}{2}CV^2$.)

(b) Step $n$ raises the source from $(n-1)V/N$ to $nV/N$ while the capacitor starts at $(n-1)V/N$. That is identical to part (a) with a step size of $V/N$, so the loss per step is $\tfrac{1}{2}C(V/N)^2$. Over $N$ steps: $N\cdot\tfrac{1}{2}C\frac{V^2}{N^2} = \frac{CV^2}{2N}$. ∎

(c) $CV_{DD}^2 = (2\times10^{-15})(0.75^2) = 1.125\times10^{-15}$ J $= 1.125$ fJ per 0 → 1 transition. Half is dissipated during charging; the other half is stored and dissipated when the node discharges.

(d) $P = \alpha CV_{DD}^2f = 0.15 \times 1.125\times10^{-15} \times 3\times10^{9} = 5.063\times10^{-7}$ W $= 0.506$ µW.

(e) $50/(5.063\times10^{-7}) = 9.88\times10^{7}$, about **98.8 million** such nodes. A large SoC has billions of transistors, so average activity factors must be far lower than 0.15. In practice they are, thanks to clock gating and idle blocks.

(f) Power scales as $V_{DD}^2$: $(0.65/0.75)^2 = 0.7511$, a **24.9%** reduction. The maximum frequency would also fall, because lower $V_{DD}$ means less gate overdrive, higher effective transistor resistance, a longer RC delay and a lower $f_{max}$. That is the essence of dynamic voltage and frequency scaling (DVFS): lower V and lower f together cut power roughly cubically.

### Solution 07-02.14

(a) $I_0 = 12/200 = 60.0$ mA.

(b) At turn-off, the coil current (60 mA) continues through $R_f$. The coil's top is at +12 V. Current flows down through the coil and back up through $R_f$, so the coil's bottom (the transistor's terminal) rises to $12 + I_0R_f$. Requiring $12 + 0.06R_f \le 30$ gives $R_f \le 300\ \Omega$.

(c) The decay loop contains $L$, $R_{coil}$ and $R_f$ in series: $\tau = L/(R_{coil} + R_f) = 0.1/500 = 0.200$ ms.

(d) $i(t) = I_0e^{-t/\tau}$ reaches $0.1I_0$ at $t = \tau\ln 10 = 0.200 \times 2.303 = 0.4605$ ms.†

(e) The diode clamps the coil's bottom at $12 + 0.7 = 12.7$ V. The decay loop now contains $L$, $R_{coil}$ and a constant 0.7 V drop: $\tau = L/R_{coil} = 0.1/200 = 0.500$ ms.

(f) KVL around the loop: $L\frac{di}{dt} + R_{coil}i + 0.7 = 0$, so $i$ approaches $-0.7/200 = -3.5$ mA with time constant 0.5 ms:
$i(t) = (60 + 3.5)e^{-t/0.5\text{ ms}} - 3.5$ mA. (The diode stops conducting when $i$ reaches 0, so the negative asymptote is never actually reached.)
Setting $i = 6$ mA: $e^{-t/\tau} = 9.5/63.5$, so $t = 0.5\ln(63.5/9.5) = 0.5 \times 1.900 = 0.9499$ ms.†
The diode version is about **2.1× slower** to release, the price of the much lower voltage stress.

(g) The total energy dissipated is $\tfrac{1}{2}LI_0^2 = \tfrac{1}{2}(0.1)(0.06^2) = 1.80\times10^{-4}$ J $= 0.180$ mJ in either case. The flyback method changes only where it is dissipated and how fast.

### Solution 07-02.15

(a) $N_\tau = (12 + 1)\ln 2 = 9.011$.

(b) $\tau_{max} = 100\text{ ns}/9.011 = 11.10$ ns, so $R_{max} = 11.10\text{ ns}/10\text{ pF} = 1.110$ kΩ.

(c) $v_n = \sqrt{kT/C} = \sqrt{4.142\times10^{-21}/10^{-11}} = 20.35$ µV rms. The 12-bit LSB is $3.3/4096 = 805.7$ µV, so the noise is 0.0253 LSB: negligible.

(d) The 16-bit LSB is $3.3/65536 = 50.35$ µV, so the noise is $20.35/50.35 = 0.404$ LSB rms. That is significant: it costs more than a third of a bit of effective resolution and makes the low-order bits noisy.

(e) Require $\sqrt{kT/C} \le 0.1 \times 50.35$ µV $= 5.035$ µV, so $C \ge kT/(5.035\times10^{-6})^2 = 4.142\times10^{-21}/2.535\times10^{-11} = 163.4$ pF.
With 16-bit settling ($N_\tau = 17\ln 2 = 11.78$) in 100 ns: $\tau_{max} = 8.486$ ns, so $R_{max} = 8.486\text{ ns}/163.4\text{ pF} = 51.95\ \Omega$.
**The tradeoff:** going from 12 to 16 bits made the capacitor about 16× larger, for noise, while the settling requirement also tightened. The allowable resistance fell from 1.11 kΩ to about 52 Ω, more than 20× lower. The driver must deliver large currents into a large capacitor very quickly. This is why precision ADCs need powerful, carefully chosen drivers, and why "16-bit performance" claims must be read together with the recommended driver.

### Solution 07-02.16

(a) The total charge is $Q = CV_0 = (10^{-6})(10) = 10$ µC, and it is conserved because no charge leaves the two-capacitor circuit. In the final state both capacitors are at the same voltage $V_f$, so $2CV_f = Q$ and $V_f = 5.00$ V.

(b) The resistor sees the two capacitors in series around the loop: $C_{eq} = \frac{C\cdot C}{C + C} = C/2 = 0.5$ µF. So $\tau = RC_{eq} = (10^3)(0.5\times10^{-6}) = 0.500$ ms.

(c) Before: $\tfrac{1}{2}(10^{-6})(10^2) = 50.0$ µJ. After: $2 \times \tfrac{1}{2}(10^{-6})(5^2) = 25.0$ µJ. Dissipated: 25.0 µJ, half of the original, **independent of R**, by the same argument as Problem 13(a).

(d) With $R = 0$ exactly, the circuit equations have no consistent solution: an instantaneous voltage change would need infinite current. Physically, real wires always have some resistance and inductance. With very small R, the energy is radiated as electromagnetic waves or dissipated in a spark, or the circuit rings through its parasitic inductance until resistance damps it. The 25 µJ is lost one way or another; the idealized model has simply hidden where.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-02.1a | τ (2.2 kΩ, 47 µF) | 103.4 | ms |
| 07-02.1b | τ (5 mH, 50 Ω) | 100 | µs |
| 07-02.1c | τ (10 kΩ, 10 pF) | 100 | ns |
| 07-02.2a | remaining after 3τ | 4.98 | % |
| 07-02.2b | time constants to 99.9 % | 6.908 | — |
| 07-02.2c | time constants to 50 % | 0.6931 | — |
| 07-02.3a | $i_C(0^+)$ | 10.0 | mA |
| 07-02.3b | $v_C(\infty)$ | 8.00 | V |
| 07-02.3c | $R_{Th}$ | 800 | Ω |
| 07-02.3d | τ | 0.800 | ms |
| 07-02.4a | inductor current | 3.00 | A |
| 07-02.4b | stored energy | 9.00 | mJ |
| 07-02.5a | minimum RC | 0.5246 | s |
| 07-02.5b | minimum R | 52.46 | kΩ |
| 07-02.6a | $v_C(5\text{ ms})$ | 1.967 | V |
| 07-02.6b | $v_C(15\text{ ms})$ | 0.7237 | V |
| 07-02.6c | current at $0^+$ | 0.500 | mA |
| 07-02.6d | current just after 5 ms | −0.1967 | mA |
| 07-02.6e | $v_C(25\text{ ms})$ | 0.27 | V |
| 07-02.7a | $R_{Th}$ | 25 | Ω |
| 07-02.7b | τ | 2.00 | ms |
| 07-02.7c | $i_L(\infty)$ | 0.800 | A |
| 07-02.7d | $v_L(0^+)$ | 20.0 | V |
| 07-02.7e | $i_L(3\text{ ms})$ | 0.6215 | A |
| 07-02.8a | $v_C(0^-)$ | 12 | V |
| 07-02.8b | $v_C(\infty)$ | 6.00 | V |
| 07-02.8c | τ | 5.00 | ms |
| 07-02.8d | $i_{R2}(0^+)$ | 6.00 | mA |
| 07-02.8e | $i_C(0^+)$ | −6.00 | mA |
| 07-02.8f | $i_{R2}(\infty)$ | 3.00 | mA |
| 07-02.9a | scope bandwidth (0.35 rule) | 100 | MHz |
| 07-02.9b | scope bandwidth (exact single pole) | 99.9 | MHz |
| 07-02.9c | $f_{3dB}$ of 1 kΩ, 10 nF | 15.92 | kHz |
| 07-02.9d | 10–90 % rise time | 21.97 | µs |
| 07-02.9e | 50 % delay | 6.931 | µs |
| 07-02.10a | $x(5\text{ ms})$ | 8.013 | V |
| 07-02.10b | steady lag | 1.00 | ms |
| 07-02.10c | steady error | 2.00 | V |
| 07-02.11a | ideal integrator at 5 ms | 5.000 | V |
| 07-02.11b | time to reach +12 V rail | 12.0 | ms |
| 07-02.11c | leaky integrator at 10 ms | 6.321 | V |
| 07-02.11d | leaky integrator final value | 10.0 | V |
| 07-02.11e | leaky integrator τ | 10.0 | ms |
| 07-02.12a | $V_{max}$, τ = 0.5 ms | 0.7311 | V |
| 07-02.12b | $V_{min}$, τ = 0.5 ms | 0.2689 | V |
| 07-02.12c | ripple, τ = 0.5 ms | 0.4621 | V |
| 07-02.12d | $V_{max}$, τ = 5 ms | 0.5250 | V |
| 07-02.12e | $V_{min}$, τ = 5 ms | 0.4750 | V |
| 07-02.12f | ripple, τ = 5 ms | 0.04996 | V |
| 07-02.12g | ripple approximation $VT/(4\tau)$ | 0.0500 | V |
| 07-02.13a | energy per 0→1 transition | 1.125 | fJ |
| 07-02.13b | average dynamic power per node | 0.506 | µW |
| 07-02.13c | nodes for 50 W | 98.8 | million |
| 07-02.13d | power reduction 0.75 → 0.65 V | 24.9 | % |
| 07-02.14a | $I_0$ | 60.0 | mA |
| 07-02.14b | maximum $R_f$ | 300 | Ω |
| 07-02.14c | τ with resistor flyback | 0.200 | ms |
| 07-02.14d | time to 10 % (resistor) | 0.4605 | ms |
| 07-02.14e | τ with diode flyback | 0.500 | ms |
| 07-02.14f | time to 10 % (diode) | 0.9499 | ms |
| 07-02.14g | transistor voltage with diode | 12.7 | V |
| 07-02.14h | energy dissipated during release | 0.180 | mJ |
| 07-02.15a | time constants, 12-bit | 9.011 | — |
| 07-02.15b | $\tau_{max}$ | 11.10 | ns |
| 07-02.15c | $R_{max}$ | 1.110 | kΩ |
| 07-02.15d | kT/C noise, 10 pF | 20.35 | µV |
| 07-02.15e | noise in 12-bit LSB | 0.0253 | — |
| 07-02.15f | noise in 16-bit LSB | 0.404 | — |
| 07-02.15g | capacitor for 0.1 LSB at 16 bits | 163.4 | pF |
| 07-02.15h | $R_{max}$ with that capacitor | 51.95 | Ω |
| 07-02.16a | final voltage | 5.00 | V |
| 07-02.16b | τ | 0.500 | ms |
| 07-02.16c | energy before | 50.0 | µJ |
| 07-02.16d | energy after | 25.0 | µJ |
| 07-02.16e | energy dissipated | 25.0 | µJ |
