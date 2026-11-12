# Course 01 · Final Exam (Calculus for Engineers)

**Time limit:** 180 minutes. **Allowed:** a scientific calculator, and the [Course 01 equation sheet](../../../reference/equation-sheets/01-calculus-for-engineers.md) printed without its chapter links. No notes, no Python.
**Instructions:** answer all 15 questions and show every step. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (127 points in total; 89 or more, about 70%, is a strong pass). Give numerical answers to 4 significant figures unless told otherwise, with units. Question 11(d) is a short-answer diligence question graded against the rubric in the solutions. Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

Unless stated otherwise: $\varepsilon_0 = 8.854\times10^{-12}$ F/m, $\mu_0 = 4\pi\times10^{-7}$ H/m.

---

**1 [A] · Logs, decibels and exponentials.** A receiver chain has a 20 dB amplifier, then a cable with 6 dB of loss, then a 14 dB amplifier.
(a) What is the total gain in dB, as a voltage ratio and as a power ratio?
(b) A signal decays as $e^{-t/\tau}$ with $\tau = 2$ ms. How long does it take to fall to 1% of its starting value?

**2 [A] · Limits and continuity.**
(a) Find $\lim_{x\to0} \sin(3x)/x$.
(b) An RC low-pass filter has gain magnitude $H(f) = 1/\sqrt{1 + (f/f_c)^2}$ with $f_c = 1$ kHz. Find $\lim_{f\to\infty} f\,H(f)$, and say what it tells you about the gain at high frequency.
(c) A capacitor voltage is $v(t) = 2t$ V for $t < 1$ s and $v(t) = a - t$ V for $t \ge 1$ s ($t$ in seconds). Find the $a$ that makes $v$ continuous. Is its derivative continuous too, and what would that mean for the capacitor current?

**3 [B] · Derivatives.**
(a) A 10 nF capacitor has $v(t) = 5e^{-t/\tau}\sin(\omega t)$ V, with $\tau = 1$ µs and $\omega = 2\pi\times1$ MHz. Find the current $i = C\,dv/dt$ at $t = 0$.
(b) Find $\dfrac{d}{dx}\ln(1 + x^2)$ at $x = 2$.
(c) A diode obeys $I = I_S\left(e^{V/V_T} - 1\right)$. Use implicit differentiation to find $dV/dI$, and evaluate it at $I = 1$ mA with $V_T = 25.85$ mV.

**4 [B] · Optimization.** A 10 V source with internal resistance $R_s = 50\ \Omega$ drives a load $R_L$.
(a) Use calculus to find the $R_L$ that maximizes the load power, and that maximum power.
(b) Find the load power for $R_L = 100\ \Omega$, as a value and as a percentage of the maximum.
(c) Find the load power for $R_L = 25\ \Omega$. Explain, using the shape of the power curve near its peak, why a factor-of-2 mismatch either way costs only about 11%.

**5 [C] · Newton's method and linearization.** A 5 V supply drives a 1 kΩ resistor in series with a diode ($I_S = 1.0\times10^{-14}$ A, $V_T = 25.85$ mV).
(a) Write an equation $g(V) = 0$ for the diode voltage $V$. Apply two Newton iterations starting from $V_0 = 0.7$ V.
(b) Give the converged $V$ and the current $I$.
(c) Find the diode's small-signal resistance $r_d = dV/dI$ at this operating point.
(d) Use linearization to estimate how much $V$ rises if the supply rises by 0.1 V. The exact re-solved rise is 0.590 mV. Explain why the linear estimate is slightly high.

**6 [A] · Accumulating charge.** A sensor draws $i(t) = 3e^{-t/(2\text{ ms})}$ mA for $t \ge 0$.
(a) What total charge does it draw from $t = 0$ to $\infty$?
(b) What charge does it draw in the first 2 ms, and what fraction of the total is that?

**7 [B] · Techniques of integration.**
(a) Evaluate $\int_0^1 x e^x\,dx$.
(b) Evaluate $\int_0^1 \dfrac{dx}{(x + 1)(x + 2)}$.
(c) A 1 µF capacitor charged to 10 V discharges through a resistor $R$, so $v(t) = 10e^{-t/RC}$ V. Show by integrating the resistor power from 0 to $\infty$ that the resistor dissipates $\tfrac12 CV_0^2$ whatever $R$ is, and evaluate it.

**8 [B] · Average and RMS.** A half-wave rectified sine is $v(t) = 10\sin(\omega t)$ V for the first half of each period and 0 for the second half.
(a) Find its average value.
(b) Find its RMS value.
(c) Find the average power it delivers to a 50 Ω resistor.
(d) A colleague computes the power as $V_{avg}^2/R$. What does that give, and why is it wrong?

**9 [C] · Probability densities: quantization noise.** A 12-bit ADC spans 0 to 1 V, so its step is $\Delta = 1\text{ V}/2^{12}$. Model the quantization error as uniformly distributed on $[-\Delta/2, \Delta/2]$.
(a) Show by integration that the RMS error is $\Delta/\sqrt{12}$.
(b) Evaluate $\Delta$ and the RMS error.
(c) A full-scale sine (1 V peak-to-peak) is applied. Find the signal-to-quantization-noise ratio (SNR) in dB.
(d) Show that each extra bit adds a fixed number of dB, find it, and reconcile your answer to (c) with the rule of thumb SNR ≈ 6.02$N$ + 1.76 dB.

**10 [B] · Taylor series and error bounds.**
(a) Estimate $e^{0.1}$ with the third-order Maclaurin polynomial. Bound the error with the Lagrange remainder, then compare with the actual error.
(b) Estimate $\ln 1.2$ with the first three terms of the series for $\ln(1 + x)$. Find the actual error and the alternating-series bound.
(c) A diode current is proportional to $e^{v/V_T}$, with $v = 0.1\,V_T\cos\omega t$. Use the Taylor series to estimate the second-harmonic distortion: the second-harmonic amplitude divided by the fundamental, in %.

**11 [B] · Dies per wafer and a cost claim.** A startup's CEO says: "Our next chip doubles the die from 300 mm² to 600 mm², so its cost per die roughly doubles." Assume a 300 mm wafer costs \$17,000, a defect density $D_0 = 0.07$ per cm², and Poisson yield $Y = e^{-AD_0}$ (all illustrative).
(a) Use the dies-per-wafer formula to find the gross dies for each size.
(b) Find the yield and the good dies per wafer for each.
(c) Find the cost per good die for each, and the ratio.
(d) In two or three sentences, explain why the CEO's statement is wrong and name two questions you would ask next.

**12 [B] · Partial derivatives and tolerance.** An LC oscillator runs at $f_0 = 1/(2\pi\sqrt{LC})$ with $L = 10$ µH ± 2% and $C = 100$ pF ± 5%.
(a) Find $f_0$.
(b) Use partial derivatives (or the log differential) to find the relative sensitivities $\dfrac{L}{f_0}\dfrac{\partial f_0}{\partial L}$ and $\dfrac{C}{f_0}\dfrac{\partial f_0}{\partial C}$.
(c) Find the worst-case relative frequency error.
(d) Treating the tolerances as independent standard deviations, find the root-sum-square (RSS) error. Which part would you tighten first?

**13 [C] · Lagrange multipliers.** Two paralleled power converters share a total current $I = 100$ A. Their losses are $R_1I_1^2 + R_2I_2^2$, with $R_1 = 10$ mΩ and $R_2 = 15$ mΩ.
(a) Use a Lagrange multiplier to find the current split that minimizes the total loss, and that loss.
(b) Find $\lambda$, and explain its meaning in watts per ampere.
(c) Compare with an equal 50/50 split. Explain why the optimum looks like current division between parallel resistors.
(d) Show that your critical point is a minimum.

**14 [C] · Gauss's law and a coaxial cable.** A coaxial cable has an inner conductor of radius $a = 0.45$ mm, an outer conductor of inner radius $b = 3.5a$, and polyethylene insulation with $\varepsilon_r = 2.25$. The inner conductor carries charge $\lambda$ per meter.
(a) Use Gauss's law on a coaxial cylinder of radius $r$ ($a < r < b$) to find $E(r)$.
(b) Integrate $E$ from $a$ to $b$ to find the voltage between the conductors.
(c) Find the capacitance per meter.
(d) At 100 V between the conductors, find the charge per meter and the largest field in the insulation, and say where it occurs.

**15 [B] · Current, circulation and potential.**
(a) In a round wire of radius $a = 0.5$ mm, the current density is $J(r) = J_0(r/a)^2$ with $J_0 = 10$ A/mm². Find the total current with a double integral in polar coordinates.
(b) Use Ampère's law, $\oint \mathbf{B}\cdot d\mathbf{l} = \mu_0 I_{enc}$, to find $B$ at the wire's surface.
(c) Show that $\mathbf{F} = (2xy + 1,\ x^2)$ is conservative, find a potential, and find the work $\int \mathbf{F}\cdot d\mathbf{r}$ from (0, 0) to (1, 2).
