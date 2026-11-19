# Problems 11-01 · Signals: Classification and Operations

Chapter: [11-01](../chapters/11-01-signals-classification-and-operations.md) · Worked solutions: [11-01 solutions](../solutions/11-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** $t$ in seconds unless stated; energies and powers are normalized (to 1 Ω) unless a resistor is given; the DT power uses the symmetric window $1/(2N + 1)\sum_{-N}^{N}$; DT frequencies are in rad/sample.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 11-01.1 [A]

**Energy or power?** Classify each signal as an energy signal, a power signal or neither, and find its energy or power: (a) $2\cos(5t)$; (b) $e^{-3\lvert t\rvert}$; (c) $u[n]$; (d) $t\,u(t)$; (e) $(-0.5)^nu[n]$; (f) $u(t)$.

### Problem 11-01.2 [A]

**Fundamental periods.** Find the fundamental period, or show that the signal is not periodic: (a) $\cos(10\pi t) + \sin(4\pi t)$; (b) $\cos^2(3t)$; (c) $e^{j5t} + e^{j7t}$; (d) $e^{j2\pi n/5} + e^{j3\pi n/4}$; (e) $\cos(n/6)$; (f) $\cos(1.2\pi n)$.

### Problem 11-01.3 [A]

**Sifting.** Evaluate (a) $\int_{-\infty}^{\infty}e^{-3t}\,\delta(t - 1)\,dt$; (b) $\int_{-\infty}^{\infty}\sin(\pi t)\,\delta(4t - 2)\,dt$; (c) $\int_{0}^{5}t^3\,\delta(t + 2)\,dt$; (d) $\sum_{n}(n^2 + 1)\,\delta[n - 3]$; (e) $\sum_{n}2^nu[n]\,\delta[n + 2]$.

### Problem 11-01.4 [B]

**Three transformations.** Let $x(t) = t + 1$ for $-1 \le t \le 1$ and 0 otherwise. Find $E_x$. Then, for each of (a) $y_1(t) = x(2t + 1)$, (b) $y_2(t) = x(1 - t/2)$ and (c) $y_3(t) = x(-t - 1)$, find the support, the value at the stated time ($y_1(-0.25)$, $y_2(3)$, $y_3(-0.5)$) and the energy. Sketch each.

### Problem 11-01.5 [B]

**A trapezoidal pulse.** A voltage rises linearly from 0 at $t = 0$ to 3 V at $t$ = 1 ms, holds until 4 ms, and falls linearly to 0 at 5 ms. (a) Write it as a sum of ramps, and give the slope in V/s. (b) Write its derivative with steps. (c) Find its energy in V²·ms and the energy it delivers to 50 Ω. (d) Find its average and RMS values over the 5 ms pulse.

### Problem 11-01.6 [B]

**Even and odd parts.** (a) Find the even and odd parts of the pulse $x(t) = u(t) - u(t - 2)$ and their energies. (b) Split $x(t) = \cos t + \sin t + \sin t\cos t$ into even and odd parts by inspection. (c) For $x[n] = (0.5)^nu[n]$, find $x_e[-2]$, $x_o[-2]$ and the energies $E_x$, $E_e$ and $E_o$.

### Problem 11-01.7 [B]

**Power from exponentials.** (a) Show that $x(t) = 2 + 3e^{j100\pi t} + 3e^{-j100\pi t} + je^{j300\pi t} - je^{-j300\pi t}$ is real, and write it with cosines and sines. (b) Find its fundamental period, its power and its RMS value. (c) Find the fundamental period, power and RMS value of $y(t) = 5\cos(10t)\cos(30t)$.

### Problem 11-01.8 [B]

**Discrete-time operations.** Let $x[n] = n + 1$ for $0 \le n \le 3$ and 0 otherwise. (a) Find $x[n - 2]$ at $n = 4$. (b) Find the support of $x[1 - n]$ and its value at $n = -2$. (c) Find $x[2n]$, its value at $n = 1$ and its energy, and compare with $E_x$. (d) Find the zero-insertion interpolation $y[n] = x[n/2]$ ($n$ even, else 0), its value at $n = 6$ and its energy. (e) Find the energy of $x[2n + 1]$, and explain why it differs from (c).

### Problem 11-01.9 [B]

**Damped exponentials.** (a) For $x(t) = 2e^{(-1 + j2\pi)t}$, write $\operatorname{Re}\{x\}$, find the time for the envelope to fall to 10% of its initial value, and how many cycles occur in that time. (b) For $x[n] = (0.9e^{j\pi/4})^n$, find the period of the oscillation in samples, the value of $n$ at which the envelope reaches 0.1, and the first integer $n$ at which it is below 0.1. (c) Describe $x[n] = (-0.9)^n$ in the language of §3.7.

### Problem 11-01.10 [B]

**Which frequency is it?** (a) Find the frequency in $[0, \pi]$ that gives the same real cosine as $\omega = 3.5\pi$. (b) Do the same for $\omega$ = 7 rad/sample. (c) A 26 kHz cosine is sampled at 10 kHz; at what frequency in $[0, f_s/2]$ does it appear? (d) Show that 1 kHz, 9 kHz and 11 kHz cosines sampled at 10 kHz all give the DT frequency 0.2π, and evaluate it.

### Problem 11-01.11 [B]

**A pulsed LED.** A wearable's optical heart-rate sensor drives its LED with 50 mA pulses lasting 100 µs, repeated at 100 Hz. The LED drops 3 V while on, and the drive path has 2 Ω of series resistance. (a) Find the duty cycle and the average and RMS currents (01-07). (b) Find the average power in the LED and in the resistor, and explain why one uses the average current and the other the RMS current. (c) Find the hours a 200 mAh battery could supply this load alone, the LED's peak power, and the current's crest factor (peak/RMS).

### Problem 11-01.12 [C]

**Jumps and their derivative.** Let $x(t) = 2u(t + 1) - 3u(t - 1) + r(t - 2)$. (a) Find $x(0)$, $x(1.5)$, $x(3)$ and $x(5)$, and sketch $x$. (b) Find $x'(t)$. (c) Evaluate $\int_{-\infty}^{\infty}x'(t)e^{-t}\,dt$, and check the result by integrating by parts.

### Problem 11-01.13 [C]

**An impulse of a function.** Using the scaling property near each root, show that $\delta\big(g(t)\big) = \sum_i\delta(t - t_i)/\lvert g'(t_i)\rvert$ for a function $g$ with simple roots $t_i$. Then evaluate (a) $\int_{-\infty}^{\infty}e^{t}\,\delta(t^2 - 4)\,dt$ and (b) $\int_{0}^{\infty}\cos(t)\,\delta(t^2 - \pi^2)\,dt$.

### Problem 11-01.14 [C]

**Cancelling mains hum by averaging.** An ECG front end samples at 500 SPS. (a) Find the DT period $N_0$ of 50 Hz and of 60 Hz interference. (b) Averaging each block of $N$ consecutive samples removes any sinusoid that completes a whole number of its DT periods in the block, because a sinusoid sums to zero over a period. Find the smallest $N$ that removes both 50 Hz and 60 Hz, and the block's duration. (c) Show that the same block removes the third harmonics at 150 Hz and 180 Hz. (d) Find the lowest nonzero frequency that the block also removes, and say why that matters for an ECG.

---

## Objective coverage

| Learning objective (chapter 11-01) | Problems |
|---|---|
| 1. Classify signals | 1, 2, 6 |
| 2. Energy, power and RMS | 1, 5, 7, 11 |
| 3. Fundamental periods, CT and DT | 2, 7, 14 |
| 4. Time-axis operations, CT and DT | 4, 8 |
| 5. Steps, ramps and impulses | 3, 5, 12, 13 |
| 6. Complex exponentials and DT frequency | 9, 10, 14 |
