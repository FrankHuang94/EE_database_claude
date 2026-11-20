# Problems 16-02 · DTFT and z-Transform for DSP

Chapter: [16-02](../chapters/16-02-dtft-and-z-transform-for-dsp.md) · Worked solutions: [16-02 solutions](../solutions/16-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Coefficients are in powers of $z^{-1}$; systems are causal unless stated; $\omega$ is in rad/sample; group delay $\tau_g = -d\phi/d\omega$ in samples. "−3 dB width" of a notch or resonator means the distance between the two half-power points.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-02.1 [A]

**A DC blocker by inspection.** For $y[n] = 0.8\,y[n-1] + x[n] - x[n-1]$, give $H(z)$, its pole and zero, the ROC, and whether it is stable. Find $\lvert H\rvert$ at DC and at $\omega = \pi$ from the geometry.

### Problem 16-02.2 [A]

**Geometric evaluation.** $H(z) = (1 - z^{-2})/(1 + 0.81z^{-2})$. Locate the poles and zeros, and find $\lvert H\rvert$ at $\omega = 0$, $\pi/2$ and $\pi$ using distances only.

### Problem 16-02.3 [A]

**Three ROCs, one stable system.** $H(z) = 1/[(1 - 0.5z^{-1})(1 - 2z^{-1})]$. List the three possible ROCs and say which is causal and which is stable. For the stable one, find $h[n]$ by partial fractions and give $h[0]$ and $h[-1]$.

### Problem 16-02.4 [B]

**Designing a DC blocker.** An audio chain at $f_s$ = 48 kHz needs $H(z) = (1 - z^{-1})/(1 - az^{-1})$ with its −3 dB point (relative to the gain at $\omega = \pi$) at 20 Hz. Estimate $a$ from $1 - a \approx \omega_c$, then find the exact $a$ and the −3 dB frequency that the estimate actually gives.

### Problem 16-02.5 [B]

**A narrow 60 Hz notch.** Design the notch of §3.3 for 60 Hz at $f_s$ = 1 kHz with a −3 dB width of about 2 Hz. Give $r$, the coefficients scaled to unit DC gain, the exact width, and the time constant in samples. Comment on whether such a narrow notch is wise.

### Problem 16-02.6 [B]

**A resonator at π/3.** For $H_{res}$ with $r$ = 0.95 and $\omega_0 = \pi/3$, estimate the peak gain and $Q$ from §3.3, then find the exact peak, the −3 dB bandwidth and $Q$.

### Problem 16-02.7 [B]

**Group delay of one pole.** Find the group delay of $H(z) = 1/(1 - 0.9z^{-1})$ at $\omega = 0$ and $\omega = \pi$, and explain the sign at $\pi$.

### Problem 16-02.8 [B]

**A short linear-phase filter.** $h = (1, -2.5, 1)$. Show that it has linear phase and give its group delay. Find its zeros and check they form a reciprocal pair. What is its gain at DC and at $\pi$?

### Problem 16-02.9 [B]

**Three filters with one magnitude.** Starting from $h = (1, -2.5, 1)$ of Problem 16-02.8, find the minimum-phase and maximum-phase FIR filters of length 3 with the same magnitude response. For all three, give the fraction of total energy in the first sample, and the group delay at DC.

### Problem 16-02.10 [C]

**A half-sample delay.** Design the first-order all-pass $(z^{-1} - a)/(1 - az^{-1})$ with a group delay of 0.5 samples at DC. Give $a$, the group delay at $\pi$, and the phase error against an ideal half-sample delay at $\omega = \pi/4$.

### Problem 16-02.11 [C]

**Equalizer length.** A link's sampled pulse response is $(0.6, 1)$. (a) Is the channel minimum phase? (b) For the delayed FIR inverse of §3.7, how many taps keep the residual ISI below 1%, and what latency results? (c) For the mirror channel $(1, 0.6)$, how many taps of a truncated causal inverse give the same residual, with what latency?

### Problem 16-02.12 [C]

**Decomposing a system.** Write $H(z) = (1 - 3z^{-1})/(1 - 0.5z^{-1})$ as $H_{min}(z)\,H_{ap}(z)$. Give the group delay of $H$, $H_{min}$ and $H_{ap}$ at DC and at $\pi$, and confirm that they add.

---

## Objective coverage

| Learning objective (chapter 16-02) | Problems |
|---|---|
| 1. Frequency response from poles and zeros | 1, 2, 3 |
| 2. Notches, resonators and DC blockers | 1, 4, 5, 6 |
| 3. Group delay and linear phase | 7, 8, 9 |
| 4. Minimum phase and the min/all-pass decomposition | 9, 12 |
| 5. First-order all-pass design | 10, 12 |
| 6. Inverse systems and equalizers | 3, 11 |
