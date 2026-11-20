# Problems 11-08 · The Laplace Transform and System Functions

Chapter: [11-08](../chapters/11-08-laplace-transform-and-system-functions.md) · Worked solutions: [11-08 solutions](../solutions/11-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $X(s) = \int x(t)e^{-st}dt$ (bilateral) with $s = \sigma + j\omega$; systems described by differential equations are causal unless stated; give every transform with its ROC.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-08.1 [A]

**Right and left.** Find the Laplace transforms and ROCs of $x_1(t) = e^{-4t}u(t)$ and $x_2(t) = -e^{-4t}u(-t)$. Evaluate $X_1(1)$ and $X_2(-5)$. Why can you not evaluate $X_2$ at $s = 1$?

### Problem 11-08.2 [A]

**A pulse.** For $x(t) = u(t) - u(t - 2)$, find $X(s)$ and its ROC, and explain why $s = 0$ is not a pole. Evaluate $X(0)$ and $X(1)$, and find the lowest positive ω at which $X(j\omega) = 0$.

### Problem 11-08.3 [A]

**Reading a pole–zero plot.** $H(s) = (s + 1)/(s^2 + 6s + 25)$ is causal. Find its zero and poles, ω₀, ζ, Q and DC gain. Is it stable?

### Problem 11-08.4 [A]

**Causal? Stable?** Classify each system as causal or not and stable or not: (i) $1/(s + 2)$, σ > −2; (ii) $1/(s - 1)$, σ > 1; (iii) $1/(s - 1)$, σ < 1; (iv) $1/[(s + 1)(s - 3)]$, −1 < σ < 3; (v) $e^{s}/(s + 1)$, σ > −1. For (v), find $h(-0.5)$.

### Problem 11-08.5 [B]

**Inverting with a strip.** Find $x(t)$ for $X(s) = (s + 5)/[(s + 1)(s + 3)]$ with ROC −3 < σ < −1. Evaluate $x(1)$ and $x(-1)$. Does $x$ have a Fourier transform?

### Problem 11-08.6 [B]

**A two-sided exponential.** Find the Laplace transform and ROC of $e^{-2\lvert t\rvert}$. From it, find the Fourier transform and its values at ω = 0 and ω = 2 rad/s, and evaluate $X(1)$.

### Problem 11-08.7 [B]

**From an equation to a resonance.** $\ddot y + 4\dot y + 13y = 13x$. Find $H(s)$, its poles, ω₀, ζ and Q, and the frequency and height of its magnitude peak.

### Problem 11-08.8 [B]

**Feedback trades gain for bandwidth.** An op-amp's open-loop gain is $G(s) = A_0/(1 + s/\omega_a)$ with $A_0 = 10^5$ and $\omega_a = 2\pi \times 10$ Hz. A resistive divider feeds back $\beta$ = 0.1. Find the closed-loop system function, its DC gain, the frequency of its pole in hertz, and the product of DC gain and bandwidth, open and closed loop.

### Problem 11-08.9 [B]

**Geometric evaluation.** $H(s) = 1000/[(s + 10)(s + 100)]$. Using pole vectors, find $\lvert H\rvert$ and $\angle H$ at ω = 10 and ω = 100 rad/s.

### Problem 11-08.10 [B]

**An all-pass step.** For $H(s) = (2 - s)/(2 + s)$: (a) show $\lvert H(j\omega)\rvert = 1$ and find the phase at ω = 2 rad/s; (b) find the group delay at DC and at ω = 2 rad/s; (c) find the step response, its value at $t = 0^+$, and when it crosses zero.

### Problem 11-08.11 [B]

**Third-order Butterworth.** The poles of a third-order Butterworth low-pass with cutoff ω_c are at radius ω_c and angles 120°, 180° and 240°. (a) Give the complex pair's real part (as a multiple of ω_c) and its damping ratio. (b) With $f_c$ = 10 kHz, find the gain at 20 kHz. (c) What is the lowest Butterworth order with at least 40 dB of attenuation at $2f_c$?

### Problem 11-08.12 [C]

**A channel with a right-half-plane zero.** $H(s) = (s - 3)/[(s + 1)(s + 6)]$ is causal. (a) Find its DC gain. (b) Can it have a causal, stable inverse? (c) Write $H = H_{min}H_{ap}$ with $H_{min}$ minimum-phase and $H_{ap}$ all-pass, and find the all-pass factor's group delay at DC. (d) An equalizer $1/H_{min}$ (made proper by adding fast poles) is placed after the channel. What remains, and what is its phase at ω = 3 rad/s?

### Problem 11-08.13 [C]

**Choosing a CTLE setting.** For the reference CTLE of Example 11-08.6: (a) at $g_{DC}$ = −6 dB find the zero frequency, the gain at Nyquist and the boost; (b) find the smallest attenuation setting (an integer in dB) that gives at least 10 dB of boost at Nyquist, and the boost it gives; (c) explain why the boost is always about 3 dB less than $\lvert g_{DC}\rvert$ at the deeper settings.

### Problem 11-08.14 [C]

**Q from a measurement.** A resonator's band-pass response peaks at 100 MHz with a −3 dB bandwidth of 4 MHz. Find Q, the real part of its poles, the time constant of the ringing envelope, and the number of ring cycles in which the envelope falls by a factor of $e$.

---

## Objective coverage

| Learning objective (chapter 11-08) | Problems |
|---|---|
| 1. Bilateral transform and ROC | 1, 2, 6 |
| 2. ROC properties; Fourier transform on the axis | 1, 2, 4, 5, 6 |
| 3. Inversion with the ROC | 5, 10, 12 |
| 4. Causality, stability, system functions and feedback | 4, 7, 8, 12 |
| 5. Geometric evaluation, Q, all-pass and minimum phase | 3, 9, 10, 11, 13, 14 |
