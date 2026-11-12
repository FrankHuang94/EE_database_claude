# Problems 01-03 · Derivatives: Rates of Change in Circuits

Chapter: [01-03](../chapters/01-03-derivatives.md) · Worked solutions: [01-03 solutions](../solutions/01-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** angles in radians; $\ln$ is the natural log; passive sign convention; answers to 4 significant figures unless stated. Use a calculator or Python freely, but show the method. Where a symbolic derivative is asked for, give the general formula before evaluating it.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 01-03.1 [A]

Using only the limit definition of the derivative, find:

(a) $f'(1)$ for $f(x) = 3x^2 - x$;
(b) $g'(2)$ for $g(x) = 1/x$.

### Problem 01-03.2 [A]

Differentiate, then evaluate.

(a) $\dfrac{d}{dx}\big(4x^3 - 2x + 7\big)$ at $x = 2$  (b) $\dfrac{d}{dx}x^{-2}$ at $x = 1$  (c) $\dfrac{d}{dx}\sqrt{x}$ at $x = 9$  (d) $\dfrac{d}{dx}\dfrac{5}{x^3}$ at $x = 1$

### Problem 01-03.3 [A]

Differentiate, then evaluate.

(a) $\dfrac{d}{dt}e^{-3t}$ at $t = 0$  (b) $\dfrac{d}{dx}\ln(5x)$ at $x = 2$  (c) $\dfrac{d}{dt}\sin(377t)$ at $t = 0$  (d) $\dfrac{d}{dx}2^x$ at $x = 3$  (e) $\dfrac{d}{dx}\tan x$ at $x = \pi/4$

### Problem 01-03.4 [A]

Use the product or quotient rule.

(a) $\dfrac{d}{dx}\big(x^2e^x\big)$ at $x = 1$  (b) $\dfrac{d}{dx}\dfrac{\sin x}{x}$ at $x = \pi/2$  (c) $\dfrac{d}{dx}\dfrac{x + 1}{x - 1}$ at $x = 3$

### Problem 01-03.5 [A]

Use the chain rule.

(a) $\dfrac{d}{dx}(3x + 1)^5$ at $x = 0$  (b) $\dfrac{d}{dx}\sqrt{1 + x^2}$ at $x = 1$  (c) $\dfrac{d}{dt}e^{-t^2}$ at $t = 1$  (d) $\dfrac{d}{dt}V_m\cos(\omega t + \phi)$ in general

### Problem 01-03.6 [A]

State the units of each derivative, and what it means physically.

(a) $dq/dt$ for charge in coulombs and time in seconds  (b) $dI/dV$ for a device's current against its voltage  (c) $dv/dt$ for an op-amp output in volts and time in microseconds  (d) $d\theta/dt$ for a phase angle in radians  (e) $dR/dT$ for a resistor's resistance against temperature in kelvin

### Problem 01-03.7 [B]

A 10 µF capacitor has this voltage across it: a linear ramp from 0 to 10 V over 0–2 ms, a hold at 10 V from 2 to 5 ms, and a linear ramp back to 0 V over 5–6 ms.

(a) Sketch $v(t)$ and find the current in each interval.
(b) What is the stored energy at the peak?
(c) Find the power delivered to the capacitor at $t = 1$ ms and just before $t = 2$ ms.
(d) Explain why the current can jump at $t = 2$ ms although the voltage cannot.

### Problem 01-03.8 [B]

An op-amp's slew rate (the maximum $\lvert dv/dt\rvert$ its output can produce) is 1 V/µs.

(a) The output is to be $V_p\sin\omega t$. Show that the maximum slope is $\omega V_p$, and derive the **full-power bandwidth** $f_{max} = SR/(2\pi V_p)$.
(b) Find $f_{max}$ for $V_p = 10$ V and for $V_p = 1$ V.
(c) Repeat (b), the 10 V case, for the LM358's 0.3 V/µs.

### Problem 01-03.9 [B]

(a) A 100 µH inductor carries $i(t) = 0.5\sin(2\pi\cdot50\,000\,t)$ A. Find the amplitude of its voltage and the ratio of voltage amplitude to current amplitude (the **reactance** $\omega L$).
(b) In a buck converter, the inductor ($L = 4.7$ µH) sees $v_L = 12 - 3.3 = 8.7$ V while the switch is on. Find $di/dt$ in A/µs, and the current rise (ripple) during an on-time of 0.3 µs.

### Problem 01-03.10 [B]

A 2 µF capacitor carries the ringing voltage $v(t) = 5e^{-200t}\sin(1000t)$ V for $t \ge 0$.

(a) Find $dv/dt$ and the current at $t = 0$.
(b) Find the first time $t_1 > 0$ at which $v$ reaches a local maximum, by setting $dv/dt = 0$.
(c) Evaluate $v(t_1)$. Why is it less than 5 V?

### Problem 01-03.11 [B]

Elasticity (relative sensitivity) $S^{y}_{x} = \dfrac{x}{y}\dfrac{dy}{dx}$.

(a) Show that for $y = kx^n$, $S = n$, and that for $y = f(x)g(x)$, $S^{y}_{x} = S^{f}_{x} + S^{g}_{x}$.
(b) For $P = \alpha CV^2f$, find $S^{P}_{V}$ at fixed $f$, and under DVFS with $f \propto V$.
(c) Battery runtime is $T = E/P$. Under DVFS, estimate the runtime gain from a 1% voltage reduction using the elasticity. Then compute the exact gain.
(d) An RC filter has corner $f_c = 1/(2\pi RC)$. Find $S^{f_c}_{R}$. Estimate the corner's change for a +5% resistor error, then compute it exactly for +5% and −5%.

### Problem 01-03.12 [B]

Implicit differentiation and inverse functions.

(a) Find the slope of the circle $x^2 + y^2 = 25$ at the point $(3, 4)$.
(b) Evaluate $\dfrac{d}{dx}\arctan x$ at $x = 1$.
(c) A diode's voltage is $V = V_T\ln(I/I_s)$. Find $dV/dI$, and evaluate the small-signal resistance at $I = 1$ mA and 10 mA, with $V_T = 25.85$ mV. Show that it agrees with $1/g_d$ from the chapter.

### Problem 01-03.13 [B]

Numerical derivatives of $\sin x$ at $x = 1$ (exact value $\cos 1$).

(a) Compute the central differences with $h = 0.1$ and $h = 0.01$, and the forward difference with $h = 0.1$, to 6 significant figures. Find each error.
(b) The central-difference error is predicted to be about $-\tfrac{h^2}{6}\cos 1$. Check this at $h = 0.1$.
(c) The total error of the central difference is about $\tfrac{h^2}{6}\lvert f'''\rvert + \tfrac{\epsilon_{\text{mach}}}{h}$. Taking $\lvert f'''\rvert \approx 1$ and $\epsilon_{\text{mach}} = 2.22\times10^{-16}$, find the best step size. Its minimum lies where the derivative of the total error is zero: $h^3 = 3\epsilon_{\text{mach}}$.

### Problem 01-03.14 [C]

**Corners and their smooth substitutes.** The rectifier and the ReLU activation function in neural networks are both $\mathrm{ReLU}(x) = \max(0, x)$.

(a) Find the derivative of ReLU for $x < 0$ and $x > 0$. Explain why it is not differentiable at 0.
(b) The **softplus** $s(x) = \ln(1 + e^x)$ is a smooth version. Show that $s'(x) = 1/(1 + e^{-x})$, the **logistic sigmoid**.
(c) Evaluate $s(0)$, $s'(0)$, $s(5)$ and $s'(5)$. How far is softplus from ReLU at $x = 0$ and at $x = 5$?
(d) Neural-network training adjusts weights by following derivatives. What practical problem arises where ReLU's derivative is exactly zero, and how does a smooth or "leaky" variant help?
(e) A real diode's I–V curve is a smooth version of an ideal diode's corner. Which feature of the exponential law plays the role of softplus's smoothing?

### Problem 01-03.15 [C]

**Power flow in a capacitor.** A 1 µF capacitor is connected across the 60 Hz mains, $v(t) = 170\sin(377t)$ V.

(a) Find $i(t)$ and $p(t) = v(t)i(t)$. Use $\sin a\cos a = \tfrac{1}{2}\sin 2a$ to show that $p(t)$ oscillates at twice the line frequency with zero average.
(b) Find the peak instantaneous power.
(c) Verify that $p = dw/dt$ with $w = \tfrac{1}{2}Cv^2$.
(d) The **reactive power** of a capacitor is $Q = V_{rms}^2\,\omega C$, in volt-amperes reactive (var). Show that it equals the peak of $p(t)$, and evaluate it. What does it mean that the capacitor draws current but consumes no average power? ([07-06](../../07-circuit-analysis-2-transient-and-ac/chapters/07-06-ac-power-and-power-factor.md) develops this.)

### Problem 01-03.16 [C]

**The marginal value of a decibel.** Shannon capacity is $C = B\log_2(1 + \text{SNR})$, with SNR in linear units ([00-01](../../00-orientation/chapters/00-01-map-of-electrical-engineering.md)). Engineers usually think in $\text{SNR}_{\text{dB}} = 10\log_{10}\text{SNR}$.

(a) Using the chain rule, show that

$$
\frac{dC}{d\,\text{SNR}_{\text{dB}}} = B\,\frac{\ln 10}{10\ln 2}\,\frac{\text{SNR}}{1 + \text{SNR}}.
$$

(b) For $B = 20$ MHz, evaluate this marginal capacity per dB at SNR = 30 dB and at 0 dB.
(c) At 30 dB, compare the derivative's prediction for +1 dB with the exact gain, $C(31\text{ dB}) - C(30\text{ dB})$.
(d) Interpret: at high SNR each extra dB is worth about $B/3$ bits per second. What does that imply about spending transmit power versus acquiring bandwidth?

---

## Objective coverage

| Learning objective (chapter 01-03) | Problems |
|---|---|
| 1. Derivative from the definition; slopes and rates with units | 1, 6, 8 |
| 2. Power, product, quotient and chain rules | 2, 4, 5, 10, 16 |
| 3. Exponential, log, trig, inverse derivatives; implicit differentiation; sinusoids | 3, 5(d), 9, 12, 14, 15 |
| 4. Capacitor and inductor laws, power and energy; small-signal conductance | 7, 9, 10, 12(c), 15 |
| 5. Elasticity and sensitivity; numerical differentiation | 11, 13, 16 |
