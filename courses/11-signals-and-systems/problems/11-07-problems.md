# Problems 11-07 · The Discrete-Time Fourier Transform

Chapter: [11-07](../chapters/11-07-discrete-time-fourier-transform.md) · Worked solutions: [11-07 solutions](../solutions/11-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $X(e^{j\omega}) = \sum x[n]e^{-j\omega n}$, ω in rad/sample; for sampled signals $\omega = 2\pi f/f_s$; sequences are listed from $n = 0$ unless stated.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-07.1 [A]

**A three-sample sequence.** For $x = 1, 2, 1$, find $X(e^{j\omega})$ in the form (linear phase) × (real function), and its magnitude at ω = 0, π/2 and π.

### Problem 11-07.2 [A]

**Converting frequencies.** At $f_s$ = 48 kHz: (a) what is ω for 1 kHz? (b) Which frequency is at ω = π? (c) A 30 kHz tone is sampled. At what frequency between 0 and 24 kHz does it appear, and why?

### Problem 11-07.3 [A]

**Symmetry on the circle.** A real sequence has $\lvert X(e^{j\omega})\rvert$ = 2 at ω = 0.3π and phase −40° there. Give $X$ at ω = −0.3π, 1.7π and 2.3π.

### Problem 11-07.4 [A]

**A high-pass exponential.** For $x = (-0.5)^nu[n]$, find $\lvert X\rvert$ at DC and at π, and say why it is high-pass.

### Problem 11-07.5 [B]

**A two-sided exponential.** Show that $0.5^{\lvert n\rvert} \leftrightarrow 0.75/(1.25 - \cos\omega)$, and evaluate it at ω = 0 and π. Why is it real?

### Problem 11-07.6 [B]

**An ideal band-pass filter.** Find $h[n]$ for the ideal filter passing $\pi/4 < \lvert\omega\rvert < \pi/2$, and give $h[0]$ and $h[1]$.

### Problem 11-07.7 [B]

**A binomial filter.** $h = \tfrac18(1, 3, 3, 1)$. (a) Show $H = e^{-j1.5\omega}\cos^3(\omega/2)$. (b) Find its group delay and its gains at 0, π/2 and π.

### Problem 11-07.8 [B]

**An FIR notch.** An ECG sampled at 500 SPS must reject 60 Hz. (a) Place zeros on the unit circle at $\pm\omega_0$ and write the three-tap filter $1, -2\cos\omega_0, 1$. (b) Normalize it to unity DC gain. (c) Find its gain at 50 Hz and at 120 Hz. What goes wrong?

### Problem 11-07.9 [B]

**Averaging noise.** A five-point average filters white noise, whose samples are independent with variance $\sigma^2$. (a) Show that the output variance is $\sigma^2\sum h^2$ and evaluate the factor. (b) Check it with Parseval.

### Problem 11-07.10 [B]

**Seeing two hum lines.** A spectrum must separate 50 Hz and 60 Hz mains components. (a) Estimate the record length with a rectangular window. (b) Roughly how long with a Hamming window, whose main lobe is twice as wide?

### Problem 11-07.11 [C]

**How many taps?** A low-pass filter with cutoff π/4 is designed by Hamming-windowed truncation. Find (numerically) the smallest odd length whose 10–90% transition is at most 0.05π, and its stopband depth for $\omega \ge \pi/4 + 0.05\pi$.

### Problem 11-07.12 [C]

**Keeping every other sample.** $x[n] = \cos(0.6\pi n)$ is downsampled by 2, $y[n] = x[2n]$. (a) Find $y$'s frequency in $[0, \pi]$. (b) Explain why the result is not $1.2\pi$, and what a designer must do before downsampling a signal with content above $\pi/2$.

### Problem 11-07.13 [B]

**A discrete-time Fourier series.** A sequence of period 6 has one period $x[0..5] = 3, 2, 1, 0, 1, 2$. (a) Find its DTFS coefficients $a_0, \dots, a_5$. (b) Check Parseval's relation. (c) Write its DTFT on $-\pi < \omega \le \pi$.

### Problem 11-07.14 [B]

**What zero-padding shows.** $x[n] = 1$ for $n = 0, 1, 2, 3$. (a) Find its 4-point DFT. (b) Zero-pad to 8 points and find $\lvert X[1]\rvert$, $\lvert X[2]\rvert$ and $\lvert X[3]\rvert$. (c) Explain the difference between (a) and (b) using the DTFT, and say whether zero-padding improved the resolution.

---

## Objective coverage

| Learning objective (chapter 11-07) | Problems |
|---|---|
| 1. Definition, inverse, periodicity | 1, 3, 5, 6, 13 |
| 2. Standard pairs and properties | 1, 4, 5, 6 |
| 3. Frequency response, group delay, nulls, linear phase | 7, 8 |
| 4. Truncation, windows, resolution | 10, 11 |
| 5. DT and CT frequency; the DFT; the DTFS | 2, 9, 12, 13, 14 |
