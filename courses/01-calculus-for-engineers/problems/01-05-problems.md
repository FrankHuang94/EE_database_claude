# Problems 01-05 · Integrals: Accumulating Charge and Energy

Chapter: [01-05](../chapters/01-05-integrals.md) · Worked solutions: [01-05 solutions](../solutions/01-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles in radians; $\ln$ is the natural log; passive sign convention; answers to 4 significant figures unless stated. Use a calculator or Python freely, but show the method, and state units for every physical integral.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-05.1 [A]

Approximate $\int_0^1 e^x\,dx$ with $n = 4$ subintervals using the left, right, midpoint and trapezoid rules. Compare each with the exact value $e - 1$, and explain the sign of each error.

### Problem 01-05.2 [A]

Evaluate with the fundamental theorem of calculus.

(a) $\displaystyle\int_1^4\sqrt{x}\,dx$  (b) $\displaystyle\int_0^\pi\sin x\,dx$  (c) $\displaystyle\int_1^e\frac{1}{x}\,dx$  (d) $\displaystyle\int_0^2\big(3x^2 - 2x + 1\big)\,dx$  (e) $\displaystyle\int_0^{\ln 2}e^{2x}\,dx$  (f) $\displaystyle\int_0^{\pi/4}\sec^2x\,dx$

### Problem 01-05.3 [A]

Use part 1 of the fundamental theorem (with the chain rule where needed).

(a) $\dfrac{d}{dx}\displaystyle\int_0^x\cos(t^2)\,dt$
(b) $\dfrac{d}{dx}\displaystyle\int_1^{x^2}\ln t\,dt$, evaluated at $x = 2$
(c) $\dfrac{d}{dx}\displaystyle\int_x^5 e^{-t}\,dt$

### Problem 01-05.4 [A]

(a) Explain without computing why $\displaystyle\int_{-1}^{1}x^3\cos x\,dx = 0$.
(b) Evaluate $\displaystyle\int_{-2}^{2}x^2\,dx$ using symmetry.
(c) Without integrating, bound $\displaystyle\int_0^1 e^{-x^2}\,dx$ from below and above using the minimum and maximum of the integrand. (The true value is 0.7468.)

### Problem 01-05.5 [B]

A 2 µF capacitor starts at $v(0) = 1$ V. It receives a current of +10 mA for $0 < t < 1$ ms, then −5 mA for $1 < t < 3$ ms, then zero.

(a) Find $v$ at 1 ms and at 3 ms.
(b) What is the net charge delivered over the 3 ms? Explain why the final voltage equals the initial voltage.
(c) Sketch $v(t)$.

### Problem 01-05.6 [B]

A 10 µH inductor in a switching converter starts with $i(0) = 0.5$ A. It sees +5 V for 2 µs, then −5 V for the next 2 µs, repeating.

(a) Find $i$ at 2 µs and at 4 µs.
(b) Find the average inductor current over one period.
(c) Find the peak stored energy.

### Problem 01-05.7 [B]

A 12 V source charges an uncharged 10 µF capacitor through a resistor $R$.

(a) Find the stored energy at the end, and the energy delivered by the source.
(b) Show by integration that the energy dissipated in $R$ is $\tfrac{1}{2}CV^2$ for every $R$.
(c) Suggest one way to charge a capacitor that wastes less than half the energy.

### Problem 01-05.8 [B]

Find the average value over one period of:

(a) $\sin^2(\omega t)$  (b) a sawtooth that ramps linearly from 0 to 3 V and resets  (c) a 3.3 V PWM signal with 30% duty cycle  (d) a half-wave rectified sine of 10 V peak

### Problem 01-05.9 [B]

A smartwatch draws 15 mA for 3 minutes every hour (a GPS fix) and 1.2 mA for the remaining 57 minutes. Its battery holds 300 mAh.

(a) Find the average current and the battery life in hours and days.
(b) A gauge's current sensor has a +50 µA offset. How much false charge does it count per day, as a percentage of capacity?
(c) Which reduction extends life more: halving the GPS current, or cutting the idle current by 20%?

### Problem 01-05.10 [B]

Numerical integration of $\int_0^\pi\sin x\,dx = 2$.

(a) Apply the trapezoid rule with $n = 4$ and $n = 8$. Find each error and the error ratio. What order of convergence does it show?
(b) Apply the midpoint rule with $n = 4$. Compare its error with the trapezoid error at $n = 4$.
(c) Combine them as $(2M + T)/3$ (Simpson's rule) and find the error.

### Problem 01-05.11 [B]

An op-amp integrator has $v_{out}(t) = -\dfrac{1}{RC}\displaystyle\int_0^t v_{in}\,d\lambda$ with $R = 10$ kΩ and $C = 100$ nF, starting from $v_{out}(0) = 0$.

(a) A 0.5 V step is applied at $t = 0$. Find $v_{out}$ at 2 ms and the slope of the output ramp.
(b) The op-amp's output saturates at −12 V. When does that happen?
(c) A ±1 V square wave at 1 kHz is applied instead (starting with +1 V). Find the peak-to-peak amplitude of the resulting triangle wave. (In practice a resistor across $C$ stops the output from drifting to the rail.)

### Problem 01-05.12 [B]

**A dual-slope ADC.** The converter integrates an unknown voltage $V_x$ for a fixed time $T_1 = 20$ ms, then integrates a reference of opposite sign, $-V_{ref} = -1$ V, until the integrator returns to zero, taking time $T_2$.

(a) Show that $V_x = V_{ref}T_2/T_1$, independent of $R$ and $C$.
(b) For $V_x = 0.35$ V, find $T_2$, and the count of a 1 MHz clock during $T_2$.
(c) A 50 Hz interference $A\sin(2\pi\cdot50t + \phi)$ adds to $V_x$. Show that it contributes nothing to the integral over $T_1$, for any $A$ and $\phi$. What would happen in a 60 Hz country?

### Problem 01-05.13 [B]

Let $A(x) = \displaystyle\int_0^x\big(t^2 - 4\big)\,dt$ (Figure 2 of the chapter).

(a) Without integrating, find where $A$ is increasing and decreasing, and locate its minimum for $x \ge 0$.
(b) Find $A(x)$ explicitly, the minimum value, and the positive $x$ where $A$ returns to zero.
(c) Interpret the zero crossing in terms of areas.

### Problem 01-05.14 [C]

**A capacitor whose capacitance depends on voltage.** Ceramic capacitors made with high-permittivity dielectrics (X5R, X7R) lose capacitance as DC bias rises. As an illustrative model, let $C(v) = C_0(1 + av)$ with $C_0 = 1$ µF and $a = -0.1$ V⁻¹, charged from 0 to 5 V.

(a) Charge is $q = \int_0^{V}C(v)\,dv$. Find the stored charge, and compare with the nominal $C_0V$.
(b) Energy is $w = \int v\,dq = \int_0^V v\,C(v)\,dv$. Find it and compare with $\tfrac{1}{2}C_0V^2$.
(c) What is the "effective" capacitance $q/V$ at 5 V? Why does this matter when choosing decoupling or energy-storage capacitors from a datasheet's nominal value?

### Problem 01-05.15 [C]

**Energy metering by sampling.** A 50 Hz system has $v = 325\sin(\omega t)$ V and $i = 10\sin(\omega t - 30^\circ)$ A.

(a) Find the exact average power by integration.
(b) A meter samples $v$ and $i$ at $N$ equally spaced instants per cycle and averages the products: $P_N = \dfrac{1}{N}\sum_{k=0}^{N-1}v_ki_k$. Compute $P_N$ for $N = 80$ and $N = 3$, starting at $t = 0$.
(c) Compute $P_2$ starting at $t = 1$ ms. Explain why $N = 2$ fails while $N = 3$ is exact. (Hint: what frequencies does the product $v\cdot i$ contain?)
(d) How much energy does this load use in one hour, in kWh?

---

## Objective coverage

| Learning objective (chapter 01-05) | Problems |
|---|---|
| 1. Riemann sums; definite integral as limit and signed area | 1, 4, 10, 15 |
| 2. Fundamental theorem of calculus | 2, 3, 13 |
| 3. Antiderivatives and linear substitution | 2, 7, 8 |
| 4. Charge, capacitor voltage, inductor current, energy | 5, 6, 7, 14 |
| 5. Average values; integrators and measurement | 8, 9, 11, 12, 15 |
