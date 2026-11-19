# Solutions 11-01 · Signals: Classification and Operations

Problems: [11-01 problems](../problems/11-01-problems.md) · Chapter: [11-01](../chapters/11-01-signals-classification-and-operations.md). Every number below is recomputed by [verify_11_01.py](../verify/verify_11_01.py).

---

## Solutions

### Solution 11-01.1

(a) A sinusoid of amplitude 2: a power signal, $P = 2^2/2$ = **2**.

(b) Finite and decaying on both sides: an energy signal, $E = 2\int_0^\infty e^{-6t}\,dt = 2/6$ = **0.3333** (units of $x^2$ times seconds).

(c) $\sum_{n=-N}^{N}u[n]^2 = N + 1$, so $P = \lim(N + 1)/(2N + 1)$ = **0.5**: a power signal. Its energy is infinite.

(d) $\int_0^T t^2\,dt = T^3/3$ grows without bound, and so does $T^3/3$ divided by $2T$: neither energy nor power.

(e) $E = \sum_{n\ge0}0.25^n = 1/(1 - 0.25)$ = **1.333**: an energy signal. The alternating sign does not matter, since only $x^2$ enters.

(f) $\frac{1}{2T}\int_{-T}^{T}u(t)^2\,dt = T/2T$, so $P$ = **0.5**: a power signal.

### Solution 11-01.2

(a) $T_1 = 2\pi/10\pi = 0.2$ s and $T_2 = 2\pi/4\pi = 0.5$ s; the ratio $2/5$ is rational, and $T_0 = 5T_1 = 2T_2$ = **1** s.

(b) Simplify first: $\cos^2(3t) = \tfrac12 + \tfrac12\cos(6t)$, so $T_0 = 2\pi/6 = \pi/3$ = **1.047** s, half the period of $\cos 3t$.

(c) $T_1 = 2\pi/5$ and $T_2 = 2\pi/7$, ratio $7/5$; $T_0 = 5T_1 = 7T_2 = 2\pi$ = **6.283** s. Equivalently, the frequencies 5 and 7 rad/s are the 5th and 7th harmonics of 1 rad/s.

(d) $2\pi/5 \div 2\pi = 1/5$, so $N_1 = 5$; $(3\pi/4)/2\pi = 3/8$, so $N_2 = 8$. $N_0 = \operatorname{lcm}(5, 8)$ = **40**.

(e) $\omega/2\pi = 1/(12\pi)$ is irrational: not periodic.

(f) $1.2\pi/2\pi = 0.6 = 3/5$, so $N_0$ = **5** samples (three cosine cycles). Note $\cos(1.2\pi n) = \cos(0.8\pi n)$ (§3.7), which has the same period.

### Solution 11-01.3

(a) $e^{-3}$ = **0.04979**.

(b) $\delta(4t - 2) = \delta\big(4(t - 0.5)\big) = \tfrac14\delta(t - 0.5)$, so the integral is $\tfrac14\sin(\pi/2)$ = **0.25**.

(c) The impulse is at $t = -2$, outside [0, 5]: **0**.

(d) Only $n = 3$ survives: $3^2 + 1$ = **10**.

(e) Only $n = -2$ survives, where $u[-2] = 0$: **0**.

### Solution 11-01.4

$E_x = \int_{-1}^{1}(t + 1)^2\,dt = \big[(t + 1)^3/3\big]_{-1}^{1} = 8/3$ = **2.667**. For each transformation, a feature of $x$ at $\tau$ appears where the argument equals $\tau$.

(a) $2t + 1 = \tau$ gives $t = (\tau - 1)/2$: the support $\tau \in [-1, 1]$ maps to $t \in$ [**−1**, **0**] s. $y_1(-0.25) = x(0.5)$ = **1.5**. Compression by 2: $E = E_x/2$ = **1.333**. The ramp still rises left to right, over half the time.

(b) $1 - t/2 = \tau$ gives $t = 2(1 - \tau)$: $\tau = 1$ maps to $t = 0$ and $\tau = -1$ to $t = 4$, so the support is [**0**, **4**] s and the ramp now *falls*, from 2 at $t = 0$ to 0 at $t = 4$. $y_2(3) = x(-0.5)$ = **0.5**. Stretching by 2 doubles the energy: $E = 2E_x$ = **5.333**.

(c) $-t - 1 = \tau$ gives $t = -\tau - 1$: the support maps to [**−2**, **0**] s, reversed (falling from 2 at $t = -2$ to 0 at $t = 0$). $y_3(-0.5) = x(-0.5)$ = **0.5**. Reversal and shift preserve energy: **2.667**.

### Solution 11-01.5

(a) The slope of the rise is 3 V per 1 ms = **3000** V/s. Adding a ramp at each change of slope (+3000 V/s at 0, −3000 at 1 ms, −3000 at 4 ms, +3000 at 5 ms):

$$
x(t) = 3000\big[r(t) - r(t - 1\ \text{ms}) - r(t - 4\ \text{ms}) + r(t - 5\ \text{ms})\big]\ \text{V}.
$$

(b) Since $r' = u$: $x'(t) = 3000\big[u(t) - u(t - 1\ \text{ms}) - u(t - 4\ \text{ms}) + u(t - 5\ \text{ms})\big]$ V/s: +3000 V/s during the rise, 0 on the flat top, −3000 V/s during the fall. There are no impulses, because $x$ has no jumps.

(c) In milliseconds, the rise contributes $\int_0^1(3\tau)^2\,d\tau = 3$ V²·ms, the top $9 \times 3 = 27$ V²·ms and the fall another 3, for $E$ = **33** V²·ms = 0.033 V²·s. Into 50 Ω: $0.033/50$ J = **0.66** mJ.

(d) The area is $3 \times (0.5 + 3 + 0.5) = 12$ V·ms, so the average over 5 ms is **2.4** V. The RMS value is $\sqrt{33/5}$ = **2.569** V, above the average as it must be.

### Solution 11-01.6

(a) $x(-t)$ is 1 on $(-2, 0)$. So $x_e = \tfrac12$ on $(-2, 2)$, and $x_o = \tfrac12\operatorname{sgn}(t)$ on $(-2, 2)$, both zero outside. $E_x$ = **2**; $E_e = \tfrac14 \times 4$ = **1**; $E_o$ = **1** (in seconds, for dimensionless $x$). They are equal because $x$ is causal (§3.4).

(b) $\cos t$ is even; $\sin t$ is odd; $\sin t\cos t$ is odd × even = odd. So $x_e = \cos t$ and $x_o = \sin t + \sin t\cos t$.

(c) $x[2] = 0.25$ and $x[-2] = 0$, so $x_e[-2] = (0 + 0.25)/2$ = **0.125** and $x_o[-2] = (0 - 0.25)/2$ = **−0.125**. $E_x = \sum 0.25^n$ = **1.333**. With $x[0] = 1$, $E_e = (E_x + 1)/2$ = **1.167** and $E_o = (E_x - 1)/2$ = **0.1667**. They sum to $E_x$.

### Solution 11-01.7

(a) Group conjugate pairs: $3e^{j\theta} + 3e^{-j\theta} = 6\cos\theta$ and $je^{j\phi} - je^{-j\phi} = j(2j\sin\phi) = -2\sin\phi$. So $x(t) = 2 + 6\cos(100\pi t) - 2\sin(300\pi t)$, which is real.

(b) The components are at 0, 50 Hz and 150 Hz; their greatest common divisor is 50 Hz, so $T_0$ = **20** ms. Power, from the exponential form ($\lvert C\rvert^2$ each, all frequencies distinct): $4 + 9 + 9 + 1 + 1$ = **24**. From the real form: $2^2 + 6^2/2 + 2^2/2 = 4 + 18 + 2 = 24$, the same. RMS $\sqrt{24}$ = **4.899**.

(c) $5\cos(10t)\cos(30t) = 2.5\cos(20t) + 2.5\cos(40t)$. The fundamental is 20 rad/s, so $T_0 = 2\pi/20$ = **0.3142** s. $P = 2.5^2/2 + 2.5^2/2$ = **6.25**, RMS **2.5**.

### Solution 11-01.8

$x[n] = \{1, 2, 3, 4\}$ for $n = 0, \dots, 3$, $E_x = 1 + 4 + 9 + 16$ = **30**.

(a) $x[4 - 2] = x[2]$ = **3**.

(b) $1 - n \in [0, 3]$ gives $n \in$ [**−2**, **1**]. At $n = -2$: $x[3]$ = **4**. The sequence is reversed: 4, 3, 2, 1 at $n = -2, \dots, 1$.

(c) $x[2n]$ keeps $x[0] = 1$ (at $n = 0$) and $x[2] = 3$ (at $n = 1$); its value at $n = 1$ is **3**, and its energy is $1 + 9$ = **10**, a third of $E_x$, not a half.

(d) $y[n] = 1, 0, 2, 0, 3, 0, 4$ for $n = 0, \dots, 6$. $y[6] = x[3]$ = **4**. Energy **30**, unchanged: zero insertion loses nothing.

(e) $x[2n + 1]$ keeps $x[1] = 2$ and $x[3] = 4$: energy $4 + 16$ = **20**. Decimation's effect on energy depends on which samples it keeps, because it discards information; CT time scaling, which discards nothing, always divides the energy by exactly $\lvert a\rvert$.

### Solution 11-01.9

(a) $x(t) = 2e^{-t}e^{j2\pi t}$, so $\operatorname{Re}\{x\} = 2e^{-t}\cos(2\pi t)$, a 1 Hz cosine in a decaying envelope. The envelope falls to 10% when $e^{-t} = 0.1$, at $t = \ln10$ = **2.303** s, during which the 1 Hz cosine completes **2.303** cycles.

(b) $x[n] = 0.9^ne^{j\pi n/4}$: the oscillation has $\omega = \pi/4$, so it repeats every $2\pi/(\pi/4)$ = **8** samples; the envelope $0.9^n$ reaches 0.1 at $n = \ln0.1/\ln0.9$ = **21.85**, so the first integer sample below 0.1 is $n$ = **22**.

(c) $z = -0.9 = 0.9e^{j\pi}$: a decaying envelope at the highest DT frequency, $\omega = \pi$, so the sign alternates every sample.

### Solution 11-01.10

(a) $3.5\pi - 2\pi = 1.5\pi$, which is equivalent to $1.5\pi - 2\pi = -0.5\pi$; a cosine is even, so the frequency in $[0, \pi]$ is $0.5\pi$ = **1.571** rad/sample.

(b) $7 - 2\pi$ = **0.7168** rad/sample, already in $[0, \pi]$.

(c) $26/10 = 2.6$ cycles per sample, equivalent to 0.6, i.e. $\omega = 1.2\pi$, which for a cosine is the same as $0.8\pi$. That corresponds to $0.4f_s$ = **4** kHz.

(d) $2\pi(1/10) = 0.2\pi$; $2\pi(9/10) = 1.8\pi \equiv -0.2\pi$, the same cosine; $2\pi(11/10) = 2.2\pi \equiv 0.2\pi$. All give $0.2\pi$ = **0.6283** rad/sample.

### Solution 11-01.11

(a) Duty cycle $100\ \mu\text{s} \times 100\ \text{Hz}$ = **1**%. Average current $0.01 \times 50$ mA = **0.5** mA; RMS current $\sqrt{0.01} \times 50$ mA = **5** mA (01-07: $X_{rms} = \sqrt{D}X_p$).

(b) The LED drops a nearly constant 3 V whenever it conducts, so its instantaneous power is $3i$, whose average is $3I_{avg}$ = **1.5** mW. The resistor's instantaneous power is $i^2R$, whose average is $I_{rms}^2R = (5\ \text{mA})^2 \times 2\ \Omega$ = **50** µW. Power in a constant-voltage element follows the average current; power in a resistance follows the mean square.

(c) $200\ \text{mAh}/0.5\ \text{mA}$ = **400** h. The LED's peak power is $3\ \text{V} \times 50\ \text{mA}$ = **150** mW, and the current's crest factor is $50/5$ = **10**: the supply must deliver **100** times the average current for 1% of the time.

### Solution 11-01.12

(a) At $t = 0$ only the first step is on: $x(0)$ = **2**. At $t = 1.5$ both steps are on: $x(1.5) = 2 - 3$ = **−1**. For $t > 2$ the ramp adds $t - 2$: $x(3) = -1 + 1$ = **0**, $x(5) = -1 + 3$ = **2**. So $x$ is 0, jumps to 2 at $t = -1$, drops to −1 at $t = 1$, and climbs with slope 1 from $t = 2$.

(b) $x'(t) = 2\delta(t + 1) - 3\delta(t - 1) + u(t - 2)$.

(c) Sifting the impulses and integrating the step:

$$
\int x'(t)e^{-t}\,dt = 2e^{1} - 3e^{-1} + \int_2^\infty e^{-t}\,dt = 2e - 3e^{-1} + e^{-2} = \textbf{4.468}.
$$

By parts, $\int x'e^{-t}\,dt = \big[xe^{-t}\big]_{-\infty}^{\infty} + \int xe^{-t}\,dt$. The boundary term vanishes ($x = 0$ at $-\infty$, and $xe^{-t} \to 0$ at $+\infty$ since $x$ grows only linearly), so the result is $\int_{-1}^{\infty}x(t)e^{-t}\,dt = \int_{-1}^{1}2e^{-t}\,dt + \int_{1}^{\infty}\big(-1 + (t - 2)u(t - 2)\big)e^{-t}\,dt = 2(e - e^{-1}) - e^{-1} + e^{-2}$, the same 4.468.

### Solution 11-01.13

*Derivation.* Near a simple root $t_i$, $g(t) \approx g'(t_i)(t - t_i)$, and $g$ has no other zero nearby. Since δ is zero away from its argument's zeros, only these neighborhoods contribute, and in each the scaling property gives $\delta\big(g'(t_i)(t - t_i)\big) = \delta(t - t_i)/\lvert g'(t_i)\rvert$. Summing over roots gives the formula.

(a) $g = t^2 - 4$ has roots $\pm2$ with $\lvert g'\rvert = \lvert2t\rvert = 4$ at both. So the integral is $(e^{2} + e^{-2})/4$ = **1.881**.

(b) $t^2 - \pi^2$ has roots $\pm\pi$; only $t = \pi$ lies in $[0, \infty)$, with $\lvert g'\rvert = 2\pi$. So the integral is $\cos(\pi)/(2\pi)$ = **−0.1592**.

### Solution 11-01.14

(a) 50 Hz: $\omega/2\pi = 50/500 = 1/10$, so $N_0$ = **10**. 60 Hz: $60/500 = 3/25$, so $N_0$ = **25**.

(b) The block must hold whole periods of both: $N = \operatorname{lcm}(10, 25)$ = **50** samples, lasting $50/500$ s = **100** ms.

(c) 150 Hz: $150/500 = 3/10$, so $N_0$ = **10**; 180 Hz: $180/500 = 9/25$, so $N_0$ = **25**. Both divide 50, so the same block removes them.

(d) A cosine at $f$ sums to zero over 50 samples when it completes a whole, nonzero number of cycles in them (and is not at a multiple of $f_s$, where every sample is equal): $50f/500 = f/10$ must be a positive integer. The lowest such $f$ is **10** Hz. The block average therefore also removes 10, 20, 30 Hz… of the ECG itself, whose band extends below and through these frequencies. Averaging is a crude filter with nulls at every multiple of 10 Hz; Course 16 designs filters that notch mains without removing the signal's own components.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-01.1a | power of 2cos 5t | 2 | — |
| 11-01.1b | energy of e^(−3abs t) | 0.3333 | — |
| 11-01.1c | power of u[n] | 0.5 | — |
| 11-01.1d | energy of (−0.5)^n u[n] | 1.333 | — |
| 11-01.1e | power of u(t) | 0.5 | — |
| 11-01.2a | T_0 (a) | 1 | s |
| 11-01.2b | T_0 (b) | 1.047 | s |
| 11-01.2c | T_0 (c) | 6.283 | s |
| 11-01.2d | N_0 (d) | 40 | — |
| 11-01.2e | N_0 (f) | 5 | — |
| 11-01.3a | integral (a) | 0.04979 | — |
| 11-01.3b | integral (b) | 0.25 | — |
| 11-01.3c | integral (c) | 0 | — |
| 11-01.3d | sum (d) | 10 | — |
| 11-01.3e | sum (e) | 0 | — |
| 11-01.4a | E_x | 2.667 | — |
| 11-01.4b | y_1 support start | −1 | s |
| 11-01.4c | y_1 support end | 0 | s |
| 11-01.4d | y_1(−0.25) | 1.5 | — |
| 11-01.4e | E of y_1 | 1.333 | — |
| 11-01.4f | y_2 support start | 0 | s |
| 11-01.4g | y_2 support end | 4 | s |
| 11-01.4h | y_2(3) | 0.5 | — |
| 11-01.4i | E of y_2 | 5.333 | — |
| 11-01.4j | y_3 support start | −2 | s |
| 11-01.4k | y_3 support end | 0 | s |
| 11-01.4l | y_3(−0.5) | 0.5 | — |
| 11-01.4m | E of y_3 | 2.667 | — |
| 11-01.5a | slope | 3000 | V/s |
| 11-01.5b | energy | 33 | V²·ms |
| 11-01.5c | energy into 50 Ω | 0.66 | mJ |
| 11-01.5d | average over pulse | 2.4 | V |
| 11-01.5e | RMS over pulse | 2.569 | V |
| 11-01.6a | E_x (a) | 2 | s |
| 11-01.6b | E_e (a) | 1 | s |
| 11-01.6c | E_o (a) | 1 | s |
| 11-01.6d | x_e[−2] (c) | 0.125 | — |
| 11-01.6e | x_o[−2] (c) | −0.125 | — |
| 11-01.6f | E_x (c) | 1.333 | — |
| 11-01.6g | E_e (c) | 1.167 | — |
| 11-01.6h | E_o (c) | 0.1667 | — |
| 11-01.7a | T_0 of x | 20 | ms |
| 11-01.7b | power of x | 24 | — |
| 11-01.7c | RMS of x | 4.899 | — |
| 11-01.7d | T_0 of y | 0.3142 | s |
| 11-01.7e | power of y | 6.25 | — |
| 11-01.7f | RMS of y | 2.5 | — |
| 11-01.8a | E_x | 30 | — |
| 11-01.8b | x[n − 2] at n = 4 | 3 | — |
| 11-01.8c | support start of x[1 − n] | −2 | — |
| 11-01.8d | support end of x[1 − n] | 1 | — |
| 11-01.8e | x[1 − n] at n = −2 | 4 | — |
| 11-01.8f | x[2n] at n = 1 | 3 | — |
| 11-01.8g | energy of x[2n] | 10 | — |
| 11-01.8h | interpolated y[6] | 4 | — |
| 11-01.8i | energy of interpolated | 30 | — |
| 11-01.8j | energy of x[2n + 1] | 20 | — |
| 11-01.9a | envelope to 10% | 2.303 | s |
| 11-01.9b | cycles in that time | 2.303 | — |
| 11-01.9c | DT oscillation period | 8 | — |
| 11-01.9d | n at envelope 0.1 | 21.85 | — |
| 11-01.9e | first integer n below 0.1 | 22 | — |
| 11-01.10a | equivalent of 3.5π | 1.571 | rad/sample |
| 11-01.10b | equivalent of 7 | 0.7168 | rad/sample |
| 11-01.10c | apparent frequency of 26 kHz | 4 | kHz |
| 11-01.10d | DT frequency of 1, 9, 11 kHz | 0.6283 | rad/sample |
| 11-01.11a | duty cycle | 1 | % |
| 11-01.11b | average current | 0.5 | mA |
| 11-01.11c | RMS current | 5 | mA |
| 11-01.11d | LED average power | 1.5 | mW |
| 11-01.11e | resistor average power | 50 | µW |
| 11-01.11f | battery life | 400 | h |
| 11-01.11g | LED peak power | 150 | mW |
| 11-01.11h | crest factor | 10 | — |
| 11-01.11i | peak / average current | 100 | — |
| 11-01.12a | x(0) | 2 | — |
| 11-01.12b | x(1.5) | −1 | — |
| 11-01.12c | x(3) | 0 | — |
| 11-01.12d | x(5) | 2 | — |
| 11-01.12e | integral | 4.468 | — |
| 11-01.13a | integral (a) | 1.881 | — |
| 11-01.13b | integral (b) | −0.1592 | — |
| 11-01.14a | N_0 of 50 Hz | 10 | — |
| 11-01.14b | N_0 of 60 Hz | 25 | — |
| 11-01.14c | block length | 50 | — |
| 11-01.14d | block duration | 100 | ms |
| 11-01.14e | N_0 of 150 Hz | 10 | — |
| 11-01.14f | N_0 of 180 Hz | 25 | — |
| 11-01.14g | lowest other frequency removed | 10 | Hz |
