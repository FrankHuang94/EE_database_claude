# Problems 16-01 · Discrete-Time Signals and Systems Review

Chapter: [16-01](../chapters/16-01-discrete-time-systems-review.md) · Worked solutions: [16-01 solutions](../solutions/16-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Digital frequency $\omega = 2\pi f/f_s$ in rad/sample; sequences start at $n = 0$ unless stated; systems start from rest. "MAC" is one multiply-accumulate.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 16-01.1 [A]

**Digital frequency.** A CD-audio system samples at 44.1 kHz. (a) Find the digital frequencies of tones at 441 Hz and 11.025 kHz. (b) Find the period, in samples, of each sampled tone. (c) Express the 11.025 kHz tone in cycles per sample.

### Problem 16-01.2 [A]

**Where do the tones land?** A data logger samples at 1 kHz with no anti-aliasing filter. Find the apparent frequency of input tones at 300 Hz, 700 Hz, 1.3 kHz, 1.7 kHz and 2.2 kHz. Which of them produce exactly the same samples as the 300 Hz tone (with the same phase)?

### Problem 16-01.3 [A]

**Periodic or not?** Decide whether each sequence is periodic and, if so, give its fundamental period: (a) $\cos(\pi n/6)$; (b) $\cos(n/6)$; (c) $\sin(0.7\pi n)$; (d) $\cos(0.8\pi n) + \cos(0.5\pi n)$; (e) $e^{j5\pi n/3}$.

### Problem 16-01.4 [A]

**Classify the systems.** For each system, state whether it is linear, time-invariant, causal, BIBO stable and memoryless, with a one-line reason for each "no": (a) $y[n] = 3x[n] + 2$; (b) $y[n] = n\,x[n]$; (c) $y[n] = x[n+1] - x[n]$; (d) $y[n] = x[2n]$; (e) $y[n]$ = the median of $x[n]$, $x[n-1]$ and $x[n-2]$.

### Problem 16-01.5 [B]

**Convolution by hand.** Convolve $x = (1, 2, 3)$ with $h = (2, -1, 1)$, both starting at $n = 0$. Count the multiply-accumulates the direct sum performs, and check your answer with the identity $\sum_n y[n] = \bigl(\sum_n x[n]\bigr)\bigl(\sum_n h[n]\bigr)$.

### Problem 16-01.6 [B]

**A first-order recursion with a zero.** For $y[n] = 0.5\,y[n-1] + x[n] + x[n-1]$: (a) find $h[0]$ to $h[3]$ by recursion and $h[n]$ in closed form; (b) find the step response $s[n]$ in closed form and evaluate $s[0]$, $s[3]$ and $s[\infty]$; (c) check $s[\infty]$ against $\sum_n h[n]$.

### Problem 16-01.7 [B]

**Stable or not?** Decide BIBO stability, and give $\sum\lvert h[n]\rvert$ where it is finite: (a) $h[n] = 0.9^n u[n]$; (b) $h[n] = (-1.1)^n u[n]$; (c) $h[n] = u[n]/(n + 1)$; (d) $h[n] = u[n]/(n + 1)^2$; (e) $y[n] = 1.6\,y[n-1] - 0.64\,y[n-2] + x[n]$; (f) $y[n] = y[n-2] + x[n]$.

### Problem 16-01.8 [B]

**Designing an exponential averager.** A temperature sensor is sampled at 1 kHz. Firmware will smooth it with an EMA whose $\alpha$ is a power of 2, so the multiply is a shift. Choose the largest such $\alpha$ that gives a time constant of at least 50 ms. Then give the exact time constant, the length of moving average with the same white-noise reduction, and the first sample at which the step response is within 1% of its final value.

### Problem 16-01.9 [B]

**A 60 Hz hum filter.** A biosignal front end samples at 960 Hz. (a) Which moving-average length $N$ places nulls at 60 Hz and all its harmonics, with the first null at 60 Hz? (b) Find its gain at 10 Hz (ratio and dB) and at 50 Hz. (c) Find its delay in samples and milliseconds.

### Problem 16-01.10 [B]

**Block diagrams and poles.** For $y[n] = 0.9\,y[n-1] - 0.5\,y[n-2] + x[n] + 0.5\,x[n-1]$: (a) count the delays of a direct-form-I and a direct-form-II realization, and the non-trivial multipliers and two-input adders; (b) find the poles in polar form and decide stability; (c) find $h[0]$ to $h[3]$.

### Problem 16-01.11 [B]

**Sinusoids through a three-tap filter.** The FIR filter $h = (0.25, 0.5, 0.25)$ is driven by (a) the constant 2, (b) $\cos(\pi n/2)$, (c) $\cos(\pi n/3)$ and (d) $(-1)^n$. Find its frequency response in the form $e^{-j\omega}A(\omega)$ with $A$ real, and the steady-state output for each input.

### Problem 16-01.12 [C]

**Accumulator width and wraparound.** (a) A 64-tap FIR filter takes 12-bit signed samples and 16-bit signed coefficients. How many bits must its accumulator have so that no sum can overflow? How many guard bits does a 48-bit accumulator leave? (b) A recursive moving sum of 64 such 12-bit samples uses wraparound arithmetic. What accumulator width does it need? (c) Trace a 2-sample recursive moving sum on a 4-bit signed accumulator (range −8 to 7) for the input 3, 4, 2, forming $s[n-1] + x[n]$ first. Show the wrapped intermediate and confirm the final $s[2]$.

### Problem 16-01.13 [C]

**An earbud's real-time budget.** An earbud runs, on each of two microphones at 16 kHz, a 128-tap linear-phase FIR beamforming filter and 4 biquads of 5 MACs each. Its MCU runs at 48 MHz and averages 1.5 cycles per MAC (loads included). (a) Find the MAC rate and the processor load. (b) The product needs end-to-end processing latency below 10 ms. Find the latency of the FIR filter and of double-buffered 32-sample blocks, and decide whether the design meets the target. (c) Would 64-sample blocks meet it?

### Problem 16-01.14 [C]

**A filter that is secretly unstable.** Consider $y[n] = 2\,y[n-1] - y[n-2] + x[n] - 2\,x[n-1] + x[n-2]$. (a) Find its impulse response by recursion. Is it BIBO stable? (b) A single computational error adds $\varepsilon$ to the stored $y[n_0]$ and nothing else goes wrong. Find the error in $y[n]$ for $n \ge n_0$, and its size 1000 samples later. (c) What has gone wrong, and how should the filter be implemented?

---

## Objective coverage

| Learning objective (chapter 16-01) | Problems |
|---|---|
| 1. DSP chain, digital frequency and aliasing | 1, 2 |
| 2. Periodicity of discrete-time sinusoids | 1, 3 |
| 3. Impulse and step responses, convolution | 5, 6, 10, 14 |
| 4. BIBO and internal stability | 4, 7, 10, 14 |
| 5. Steady-state sinusoidal response | 9, 11 |
| 6. MACs, memory, latency and real-time budgets | 5, 8, 12, 13 |
