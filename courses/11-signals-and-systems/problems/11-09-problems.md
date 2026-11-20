# Problems 11-09 · The z-Transform

Chapter: [11-09](../chapters/11-09-z-transform.md) · Worked solutions: [11-09 solutions](../solutions/11-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $X(z) = \sum x[n]z^{-n}$ (bilateral unless stated); system functions in powers of $z^{-1}$ with $A(z) = 1 + a_1z^{-1} + a_2z^{-2} + \cdots$; difference equations describe causal systems unless stated; give every transform with its ROC.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-09.1 [A]

**Outside and inside.** Find the z-transforms and ROCs of $x_1[n] = 0.8^nu[n]$ and $x_2[n] = -0.8^nu[-n - 1]$. Evaluate $X_1(2)$ and $X_2(0.5)$. Why can you not evaluate $X_2$ at $z = 2$?

### Problem 11-09.2 [A]

**A short sequence.** $x[0] = 1$, $x[1] = 2$, $x[2] = 3$, zero elsewhere. Find $X(z)$ and its ROC, evaluate $X(1)$ and $X(-1)$, and find its zeros and their distance from the origin.

### Problem 11-09.3 [A]

**Reading a pole–zero plot.** $H(z) = (1 + z^{-1})/(1 - 0.9z^{-1})$ is causal. Give its pole and zero, decide whether it is stable, and find its gain at DC, at ω = π/2 and at ω = π. What kind of filter is it?

### Problem 11-09.4 [A]

**Three ROCs.** For $H(z) = 1/[(1 - 0.5z^{-1})(1 - 1.5z^{-1})]$, list the possible ROCs and classify each system as causal or not and stable or not. For the stable one, find $h[0]$ and $h[-1]$.

### Problem 11-09.5 [B]

**Partial fractions.** Find $x[n]$ for $X(z) = (1 - 0.2z^{-1})/[(1 - 0.8z^{-1})(1 + 0.4z^{-1})]$ with ROC $\lvert z\rvert > 0.8$, and check $x[0]$, $x[1]$ and $x[2]$ by long division.

### Problem 11-09.6 [B]

**Long division.** For the causal $X(z) = 1/(1 - z^{-1} + 0.5z^{-2})$, find $x[0]$ to $x[4]$ by long division. Then find the poles (radius and angle) and confirm $x[4]$ from the resonator formula $r^n\sin((n + 1)\theta)/\sin\theta$.

### Problem 11-09.7 [B]

**An initial condition.** Solve $y[n] = 0.8y[n - 1] + x[n]$ with $x[n] = u[n]$ and $y[-1] = -5$ using the unilateral z-transform. Give $y[0]$, $y[1]$ and the final value, and the first $n$ at which $y$ is within 1% of its final value.

### Problem 11-09.8 [B]

**A comb filter.** $y[n] = x[n] - x[n - 4]$ at $f_s$ = 8 kHz. Find $H(z)$, its zeros and poles, the frequencies (in hertz, from 0 to 4 kHz) that it removes, and its largest gain and where it occurs.

### Problem 11-09.9 [B]

**Designing a resonator.** Place a pole pair to make a resonator at 1 kHz with a −3 dB bandwidth of about 50 Hz at $f_s$ = 16 kHz. Give θ, $r$, $a_1$ and $a_2$. Then find (numerically) the exact peak frequency, peak gain and −3 dB bandwidth of $H(z) = 1/A(z)$.

### Problem 11-09.10 [B]

**Stable or not?** Use the stability triangle to classify these biquad denominators $1 + a_1z^{-1} + a_2z^{-2}$: (i) $a_1 = -1.9$, $a_2 = 0.95$; (ii) $a_1 = 0.5$, $a_2 = -1.2$; (iii) $a_1 = -1.6$, $a_2 = 0.55$; (iv) $a_1 = 1.0$, $a_2 = 0.3$. For (iii), find $P(1)$ and the offending root; for (iv), find the pole radius.

### Problem 11-09.11 [B]

**Two ways to digitize a pole.** $H(s) = 1/(s + 1000)$ is to be implemented at $f_s$ = 10 kHz. (a) By impulse invariance, $h[n] = Th(nT)$: find the digital pole and the DC gain, and compare with the analog DC gain. (b) By the bilinear transform: find the digital pole, the DC gain, and the digital frequency to which the analog corner (1000 rad/s) is mapped.

### Problem 11-09.12 [C]

**A 1 Hz notch.** Redesign Example 11-09.4's notch for a −3 dB width of 1 Hz. Find $r$ from the estimate $2(1 - r)$, the exact width, the transient's time constant in samples and seconds, and the time for a hum transient to decay to 1%. What is the cost of a narrow notch?

### Problem 11-09.13 [C]

**Coarse coefficients.** A biquad's coefficients are stored with 8 fractional bits. Taking the largest radius below 1, find $r$, the largest realizable $\lvert a_1\rvert$ below $2r$, and the smallest nonzero pole angle. What frequency is that at 48 kHz and at 8 kHz?

### Problem 11-09.14 [C]

**A boxcar built from a pole and zeros.** $H(z) = \frac{1}{8}(1 - z^{-8})/(1 - z^{-1})$. (a) Locate its zeros and explain what happens to the pole at $z = 1$. (b) Find its DC gain, its first null, and its gain at ω = π/8 (in dB). (c) Find the gain of three such sections in cascade (a sinc³ filter) at π/8. (d) Implemented as an integrator $1/(1 - z^{-1})$ followed by a comb $1 - z^{-8}$, the integrator alone is not BIBO-stable. Why can the cascade still work in hardware?

---

## Objective coverage

| Learning objective (chapter 11-09) | Problems |
|---|---|
| 1. Definition and ROC | 1, 2, 4 |
| 2. ROC properties; DTFT on the unit circle | 1, 2, 4 |
| 3. Inversion and the unilateral transform | 5, 6, 7 |
| 4. System functions, causality, stability, the triangle | 3, 4, 8, 10, 13, 14 |
| 5. Geometric evaluation, resonators and notches, s to z | 3, 8, 9, 11, 12, 14 |
