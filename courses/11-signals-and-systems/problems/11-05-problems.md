# Problems 11-05 · Fourier Series

Chapter: [11-05](../chapters/11-05-fourier-series.md) · Worked solutions: [11-05 solutions](../solutions/11-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $T_0$ is the fundamental period and $\omega_0 = 2\pi/T_0$; $\operatorname{sinc}(u) = \sin(\pi u)/(\pi u)$; amplitudes $A_k = 2\lvert c_k\rvert$ for real signals; "RMS" values of harmonics are $A_k/\sqrt2$.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-05.1 [A]

**Coefficients by inspection.** Without integrating, find the nonzero $c_k$: (a) $x(t) = 3 + 2\cos\omega_0t + \sin(3\omega_0t - \pi/4)$, giving $c_3$ in magnitude and angle; (b) $x(t) = \cos^2(\omega_0t)$.

### Problem 11-05.2 [A]

**Symmetry.** For each signal, say which coefficients must vanish: (a) a ±1 square wave that is +1 for $\lvert t\rvert < T_0/4$ (even, half-wave symmetric); (b) a sawtooth $x = 2At/T_0$ on $(-T_0/2, T_0/2)$; (c) a full-wave rectified sine; (d) a 0-to-1 pulse train with 25% duty.

### Problem 11-05.3 [A]

**A pulse train.** A 5 V pulse train has a duty cycle of 1/3. Find $c_0$, $\lvert c_1\rvert$ and the 1st harmonic's amplitude, and the lowest harmonic that is missing.

### Problem 11-05.4 [B]

**A sawtooth by integration by parts.** Let $x(t) = t$ for $-\pi < t < \pi$, repeated with period $2\pi$. (a) Show that $b_k = 2(-1)^{k+1}/k$ and $a_k = 0$. (b) Give $b_1$, $b_2$ and $b_3$. (c) What does the series give at $t = \pi$, and why?

### Problem 11-05.5 [B]

**A half-wave rectifier.** Write the half-wave rectified sine $\max(\sin\omega t, 0)$ as half of $\sin\omega t$ plus half of $\lvert\sin\omega t\rvert$, and use the full-wave series of §3.4 to find its DC value and the amplitudes at $\omega$, $2\omega$ and $4\omega$.

### Problem 11-05.6 [B]

**Shift and offset.** (a) Starting from the ±1 square wave, find the coefficients of the 0-to-1 square wave with 50% duty that is high on $(0, T_0/2)$. (b) Shift it so that it is high on $(-T_0/4, T_0/4)$. What happens to the coefficients, and why are they now real? (c) Give $\lvert c_1\rvert$.

### Problem 11-05.7 [B]

**Parseval for the triangle.** (a) Show that a triangle wave of amplitude 1 has power 1/3. (b) Use Parseval and $A_k = 8/(\pi^2k^2)$ to evaluate $\sum_{k\text{ odd}}1/k^4$. (c) Find the fraction of the power in the fundamental and the triangle's THD.

### Problem 11-05.8 [B]

**Harmonic currents.** A rectifier load draws a current whose RMS harmonic components are 10 A (fundamental), 6 A (3rd), 3 A (5th) and 1.5 A (7th). (a) Find the current THD. (b) Find the total RMS current. (c) With a sinusoidal supply voltage in phase with the fundamental current, find the power factor.

### Problem 11-05.9 [B]

**Filtering a square wave.** A ±1 V, 1 kHz square wave drives an RC low-pass with a 1 kHz corner. (a) Find the output's fundamental amplitude and phase. (b) Find the 3rd harmonic's amplitude and phase. (c) The output's THD, summing all harmonics, is 16.35%. Compare with the input's.

### Problem 11-05.10 [B]

**A harmonic selector.** A 10 MHz clock swinging ±1.65 V (a square wave) drives a band-pass filter centered at 30 MHz to make a 30 MHz sinusoid. (a) Find the 30 MHz component's amplitude at the input. (b) If the filter attenuates 10 MHz by 40 dB and 50 MHz by 30 dB, find the residual 10 MHz and 50 MHz amplitudes at its output, assuming unity gain at 30 MHz.

### Problem 11-05.11 [C]

**Taming Gibbs.** The Fejér sum replaces the partial sum's coefficients by tapered ones: harmonic $k$ is weighted by $1 - k/(N + 1)$. (a) For the ±1 square wave with $N = 99$, the Fejér sum's maximum is 0.9868. Compare with the ordinary partial sum's. (b) Explain why tapering removes the overshoot, and what it costs.

### Problem 11-05.12 [C]

**A 12-bit PWM DAC.** A microcontroller's 64 MHz timer generates 12-bit PWM (4096 counts per period) from a 3.3 V pin, filtered by one RC section. (a) Find the PWM frequency and the size of one LSB. (b) The worst-case peak-to-peak ripple, at 50% duty, is about $AT_0/(4RC)$. Find the $RC$ that keeps it below half an LSB, and the filter's corner frequency. (c) How long does the filter take to settle to within half an LSB after a full-scale step? (d) What does this suggest about single-RC PWM DACs at 12 bits?

### Problem 11-05.13 [C]

**Another AM station.** Repeat Example 11-05.8 for a station at 1300 kHz with switching frequencies of 400, 500 and 600 kHz. Which works, and how does that compare with the data sheet's recommendation for 1125–1375 kHz?

### Problem 11-05.14 [C]

**Where a PWM signal's power goes.** A 3.3 V pulse train has duty cycle $D$. (a) Show that its total power is $A^2D$, its DC power $A^2D^2$, and the power in all harmonics together $A^2D(1 - D)$. Evaluate them for $D = 0.25$. (b) Use Parseval and §3.4 to show that $\sum_{k\ge1}\operatorname{sinc}^2(kD) = (1 - D)/(2D)$, and check it for $D = 0.25$. (c) At which duty cycle is the harmonic power largest?

---

## Objective coverage

| Learning objective (chapter 11-05) | Problems |
|---|---|
| 1. Coefficients of standard signals in all forms | 1, 3, 4, 5 |
| 2. Symmetry and properties | 2, 5, 6 |
| 3. Convergence, Gibbs, decay rates | 4, 11 |
| 4. Parseval, RMS, THD | 7, 8, 14 |
| 5. LTI response to periodic inputs | 9, 10, 12 |
| 6. Placing switching harmonics | 13 |
