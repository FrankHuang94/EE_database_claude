# Problems 11-04 · LTI Systems and Differential/Difference Equations

Chapter: [11-04](../chapters/11-04-lti-systems-and-differential-equations.md) · Worked solutions: [11-04 solutions](../solutions/11-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** systems are LTI and start at rest; difference equations are written with $y[n]$ on the left with coefficient 1; $t$ in seconds unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-04.1 [A]

**Properties from $h$.** For each impulse response, decide memory, causality and stability (give $\sum\lvert h\rvert$ or $\int\lvert h\rvert$ when finite), and give an inverse if one is simple: (a) $h[n] = \delta[n] - \delta[n - 2]$; (b) $h(t) = e^{-t}u(t + 1)$; (c) $h[n] = 2^nu[-n]$; (d) $h(t) = \delta(t - 2)$.

### Problem 11-04.2 [A]

**An exponential moving average.** $y[n] = 0.8y[n - 1] + 0.2x[n]$. (a) Find $h[0]$, $h[1]$ and $h[2]$ by iteration. (b) Find the DC gain. (c) Find the step response after 10 samples, $s[9]$.

### Problem 11-04.3 [A]

**Roots and stability.** Find the characteristic roots and decide stability: (a) $y[n] - 0.9y[n - 1] - 0.1y[n - 2] = x[n]$; (b) $y[n] + 0.25y[n - 2] = x[n]$ (also give the ringing period); (c) $y[n] - 2.5y[n - 1] + y[n - 2] = x[n]$.

### Problem 11-04.4 [B]

**Closed form.** For $y[n] - 1.2y[n - 1] + 0.32y[n - 2] = x[n]$: (a) find the roots; (b) write $h[n]$ in closed form and check $h[0]$ to $h[3]$ by iteration; (c) find the DC gain.

### Problem 11-04.5 [B]

**Designing a resonator.** A sensor hub samples at 8 kHz and needs a resonator that rings at 1 kHz and whose envelope falls to 1% in 10 ms. Find θ, $r$ and the two feedback coefficients.

### Problem 11-04.6 [B]

**Direct feedthrough.** A CT system obeys $\dot y + 2y = \dot x + 3x$. (a) Find $H(s)$ by the eigenfunction method. (b) Write $H(s)$ as a constant plus a strictly proper fraction, and find $h(t)$. Why does $h$ contain an impulse? (c) Find the DC gain two ways.

### Problem 11-04.7 [B]

**An overdamped RLC circuit.** The series RLC circuit of Example 11-04.5 has its resistor raised to 100 Ω. (a) Find the characteristic roots. (b) Find $h(t)$ for the capacitor voltage, using $h(0^+) = 0$ and $\dot h(0^+) = \omega_0^2$. (c) Find the time of its peak.

### Problem 11-04.8 [B]

**Jump conditions.** For $2\ddot y + 3\dot y + y = x$: (a) state $h(0^+)$ and $\dot h(0^+)$; (b) find $h(t)$; (c) find its peak time and value; (d) check its area against the DC gain.

### Problem 11-04.9 [B]

**Two realizations.** For $y[n] = 0.5x[n] + 0.5x[n - 1] + 0.9y[n - 1]$: (a) draw direct forms I and II and count delays, multipliers and additions for each; (b) find the DC gain.

### Problem 11-04.10 [B]

**Frequency response.** For the filter of Problem 11-04.9, find $H(e^{j\omega})$ and evaluate its magnitude at $\omega = 0$ and $\omega = \pi$, and its magnitude and phase at $\omega = \pi/2$. What kind of filter is it?

### Problem 11-04.11 [C]

**Rounding a resonator.** The resonator of Example 11-04.4 has coefficients 1.2728 and 0.81. A low-cost implementation stores coefficients with 4 fractional bits (steps of 1/16). (a) Find the stored coefficients. (b) Find the new pole radius, angle and ringing period. (c) What does this suggest about coefficient word length for narrow resonances?

### Problem 11-04.12 [C]

**Smoothing in a wearable.** A wearable smooths a heart-rate estimate updated at 50 samples per second. (a) Choose α in $y[n] = (1 - \alpha)y[n - 1] + \alpha x[n]$ so that its step response reaches 63% (one time constant) after 50 samples (1 s). (b) How long until it settles within 1% of a step? (c) Compare its memory and arithmetic per sample with a 5 s moving average. (d) What does the exponential average give up?

### Problem 11-04.13 [B]

**Zero input plus zero state.** $y[n] = 0.5y[n - 1] + x[n]$ starts with $y[-1] = 6$ (not at rest) and is driven by $x[n] = u[n]$. (a) Find the zero-input response (initial condition, no input) and the zero-state response (input, zero initial condition). (b) Add them, and check $y[0]$ and $y[1]$ by iterating the equation directly. (c) Evaluate both parts and the total at $n = 3$, and the final value.

---

## Objective coverage

| Learning objective (chapter 11-04) | Problems |
|---|---|
| 1. Properties and inverses from $h$ | 1 |
| 2. Difference equations: iteration, roots, stability | 2, 3, 4, 5, 11, 13 |
| 3. Differential equations: impulse responses and jump conditions | 6, 7, 8 |
| 4. Block-diagram realizations and their cost | 9, 11, 12 |
| 5. Eigenfunctions and frequency response | 6, 10 |
