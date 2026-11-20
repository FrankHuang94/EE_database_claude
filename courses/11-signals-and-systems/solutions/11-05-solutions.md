# Solutions 11-05 · Fourier Series

Problems: [11-05 problems](../problems/11-05-problems.md) · Chapter: [11-05](../chapters/11-05-fourier-series.md). Every number below is recomputed by [verify_11_05.py](../verify/verify_11_05.py), which integrates the analysis formula numerically and simulates the circuits.

---

## Solutions

### Solution 11-05.1

(a) Rewrite each term with Euler's formula. $3$ gives $c_0$ = **3**. $2\cos\omega_0t = e^{j\omega_0t} + e^{-j\omega_0t}$ gives $c_{\pm1}$ = **1**. $\sin(3\omega_0t - \pi/4) = \frac{1}{2j}\left(e^{j(3\omega_0t - \pi/4)} - e^{-j(3\omega_0t - \pi/4)}\right)$, so $c_3 = \frac{1}{2j}e^{-j\pi/4} = \tfrac12e^{-j3\pi/4}$: magnitude **0.5**, angle **−135**°, and $c_{-3} = c_3^*$.

(b) $\cos^2\omega_0t = \tfrac12 + \tfrac14e^{j2\omega_0t} + \tfrac14e^{-j2\omega_0t}$: $c_0$ = **0.5** and $c_{\pm2}$ = **0.25**, all others zero. (Measured against its own period $T_0/2$, these are the DC term and the first harmonic.)

### Solution 11-05.2

(a) Even, so all $b_k = 0$ (coefficients real); half-wave symmetric, so all even harmonics vanish, including $c_0$. Only odd cosine terms remain.

(b) Odd: all $a_k = 0$ including $a_0$; every harmonic is present (no half-wave symmetry).

(c) Even (only cosines), and its period is half the sine's, so measured against the sine's period every odd harmonic is zero.

(d) No symmetry is required, but the sinc envelope has zeros at $k = 4, 8, 12, \dots$ (§3.4).

### Solution 11-05.3

$c_0 = AD = 5/3$ = **1.667** V. $\lvert c_1\rvert = AD\,\operatorname{sinc}(1/3)$ = **1.378** V, so $A_1$ = **2.757** V. The first zero of $\operatorname{sinc}(k/3)$ is at $k$ = **3**.

### Solution 11-05.4

(a) $x$ is odd, so $a_k = 0$. With $T_0 = 2\pi$ and $\omega_0 = 1$,

$$
b_k = \frac{2}{2\pi}\int_{-\pi}^{\pi}t\sin kt\,dt = \frac{2}{\pi}\int_0^{\pi}t\sin kt\,dt .
$$

By parts, with $u = t$ and $dv = \sin kt\,dt$: $\int_0^\pi t\sin kt\,dt = \left[-\frac{t\cos kt}{k}\right]_0^\pi + \frac1k\int_0^\pi\cos kt\,dt = -\frac{\pi\cos k\pi}{k} + 0$, so $b_k = -\frac{2\cos k\pi}{k} = \frac{2(-1)^{k+1}}{k}$.

(b) $b_1$ = **2**, $b_2$ = **−1**, $b_3$ = **0.6667**.

(c) Every term $\sin k\pi$ is zero, so the series gives **0** at $t = \pi$: the midpoint of the jump from $+\pi$ to $-\pi$ (§3.5).

### Solution 11-05.5

$\max(\sin\omega t, 0) = \tfrac12\sin\omega t + \tfrac12\lvert\sin\omega t\rvert$, since the two halves add on the positive half-cycle and cancel on the negative one. The full-wave series contributes only DC and even harmonics, the sine only the fundamental:

- DC: $\tfrac12 \cdot \tfrac{2}{\pi} = 1/\pi$ = **0.3183**.
- At $\omega$: $\tfrac12$ = **0.5**.
- At $2\omega$: $\tfrac12 \cdot \frac{4}{3\pi} = \frac{2}{3\pi}$ = **0.2122**.
- At $4\omega$: $\tfrac12 \cdot \frac{4}{15\pi}$ = **0.04244**.

The half-wave rectifier has a fundamental ripple at the line frequency itself, harder to filter than the full-wave rectifier's $2\omega$.

### Solution 11-05.6

(a) The 0-to-1 wave is $\tfrac12 + \tfrac12s(t)$, where $s$ is the ±1 square wave. So $c_0 = \tfrac12$ and $c_k = \tfrac12 \cdot \frac{2}{jk\pi} = \frac{1}{jk\pi}$ for odd $k$, 0 for even $k \ne 0$.

(b) The new wave is the old one advanced by $T_0/4$: $x_{new}(t) = x(t + T_0/4)$, so $c_k^{new} = c_ke^{jk\omega_0T_0/4} = c_ke^{jk\pi/2}$. For odd $k$, $\frac{1}{jk\pi}e^{jk\pi/2} = \frac{j^{k-1}}{k\pi}$, which is real ($j^{k-1} = \pm1$ for odd $k$). The coefficients are real because the shifted wave is even.

(c) $\lvert c_1\rvert = 1/\pi$ = **0.3183**: shifting changes phases, never magnitudes.

### Solution 11-05.7

(a) Over a quarter period the triangle rises linearly from 0 to 1, and $\frac{1}{L}\int_0^Lu^2\,du$ for $u$ rising from 0 to 1 is $\tfrac13$; by symmetry every quarter has the same mean square, so $P$ = **0.3333**.

(b) Parseval: $\frac13 = \sum_{k\text{ odd}}\frac12\left(\frac{8}{\pi^2k^2}\right)^2 = \frac{32}{\pi^4}\sum_{k\text{ odd}}\frac{1}{k^4}$, so $\sum_{k\text{ odd}}1/k^4 = \pi^4/96$ = **1.0147**.

(c) The fundamental's power is $\frac12(8/\pi^2)^2 = 32/\pi^4$, a fraction $96/\pi^4$ = **98.55**% of 1/3. THD $= \sqrt{1/0.98553 - 1}$ = **12.12**%. A triangle is a much better approximation of a sine than a square wave is.

### Solution 11-05.8

(a) $\text{THD} = \sqrt{6^2 + 3^2 + 1.5^2}/10$ = **68.74**%.

(b) $I_{rms} = \sqrt{10^2 + 6^2 + 3^2 + 1.5^2}$ = **12.13** A (Parseval: RMS values add in quadrature).

(c) Only the fundamental current carries real power with a sinusoidal voltage, so $\text{PF} = I_1/I_{rms} = 10/12.13$ = **0.8241**, even though the fundamental is in phase. This **distortion power factor** is why rectifier loads need power-factor correction (07-06, Course 22).

### Solution 11-05.9

(a) $A_1 = 4/\pi$ = 1.273 V and $H(j\omega_0) = 1/(1 + j)$: amplitude $1.273/\sqrt2$ = **0.9003** V, phase **−45**°.

(b) $A_3 = 0.4244$ V and $H(j3\omega_0) = 1/(1 + 3j)$: amplitude $0.4244/\sqrt{10}$ = **0.1342** V, phase $-\arctan3$ = **−71.57**°.

(c) Each harmonic is attenuated by $1/\sqrt{1 + k^2}$, roughly $1/k$, so the output's coefficients fall as $1/k^2$, like a triangle's. The THD drops from **48.34**% to **16.35**%. (The output is a series of exponential charging curves, visibly closer to a triangle than to a square.)

### Solution 11-05.10

(a) $A_3 = \frac{4 \times 1.65}{3\pi}$ = **0.7003** V.

(b) $A_1 = 4 \times 1.65/\pi = 2.101$ V, attenuated by 40 dB (×0.01): **21.01** mV. $A_5 = 4 \times 1.65/(5\pi) = 0.4202$ V, attenuated by 30 dB (×0.0316): **13.29** mV. Both spurs are small but not negligible next to 700 mV; a sharper or higher-order filter, or a waveform with less 1st and 5th harmonic, would improve the spectral purity.

### Solution 11-05.11

(a) The ordinary partial sum peaks at **1.179**; the Fejér sum at **0.9868**: no overshoot at all.

(b) The Fejér sum equals the average of the partial sums $S_0, \dots, S_N$, which is the square wave convolved with the Fejér kernel, a positive pulse of unit area. Averaging a signal that lies between −1 and +1 with positive weights cannot leave that range, so no overshoot is possible. The cost is a slower transition: the edge is smeared over a wider interval than the partial sum's, because the highest harmonics are weighted down. This is the first example of **windowing**, the central trade between ringing and resolution in spectral analysis and filter design (Course 16).

### Solution 11-05.12

(a) $f_{PWM} = 64\ \text{MHz}/4096$ = **15625** Hz, so $T_0$ = 64 µs. One LSB is $3.3/4096$ = **0.8057** mV, and half an LSB **0.4028** mV.

(b) $RC \ge AT_0/(4 \times 0.4028\ \text{mV}) = 3.3 \times 64\ \mu\text{s}/(1.611\ \text{mV})$ = **0.1311** s, a corner of $1/(2\pi RC)$ = **1.214** Hz.

(c) Settling from a full-scale step to within half an LSB requires $e^{-t/RC} \le 1/8192$, so $t = RC\ln8192$ = **1.181** s.

(d) A single RC section makes a 12-bit PWM DAC accurate but extremely slow: over a second to settle. Practical designs raise the PWM frequency (fewer bits per period, or dithering), use a second- or third-order filter, or split the value across two PWM channels, each reducing the required $RC$.

### Solution 11-05.13

400 kHz: harmonics 400, 800, 1200, 1600 kHz; 1200 kHz is **100** kHz from the station. 500 kHz: 500, 1000, 1500 kHz; the nearest, 1500 kHz, is **200** kHz away, and the station lies between the 2nd and 3rd harmonics. 600 kHz: 600, 1200, 1800 kHz; 1200 kHz is **100** kHz away. So 500 kHz is best, which matches the data sheet's choice of 500 kHz for 1125–1375 kHz: its 2nd and 3rd harmonics (1000 and 1500 kHz) straddle that whole band, while 1200 kHz (from 400 or 600 kHz switching) falls inside it.

### Solution 11-05.14

(a) The signal is $A$ for a fraction $D$ of the time and 0 otherwise, so its mean square is $A^2D$. The DC component is $AD$, with power $A^2D^2$. The rest, $A^2D - A^2D^2 = A^2D(1 - D)$, is in the harmonics. For $A$ = 3.3 V and $D$ = 0.25: total **2.7225** V², DC **0.6806** V², harmonics **2.042** V².

(b) Parseval: $\sum_{k\ne0}\lvert c_k\rvert^2 = 2A^2D^2\sum_{k\ge1}\operatorname{sinc}^2(kD)$ must equal $A^2D(1 - D)$, so $\sum_{k\ge1}\operatorname{sinc}^2(kD) = (1 - D)/(2D)$, which is **1.5** for $D = 0.25$. Summing 200,000 terms numerically gives 1.49999…, approaching 1.5.

(c) $D(1 - D)$ is largest at $D$ = **0.5**: a 50% square wave puts the most power into harmonics, which is why PWM ripple is worst at mid-scale (Problem 11-05.12).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-05.1a | c_0 | 3 | — |
| 11-05.1b | c_1 | 1 | — |
| 11-05.1c | magnitude of c_3 | 0.5 | — |
| 11-05.1d | angle of c_3 | −135 | ° |
| 11-05.1e | c_0 of cos² | 0.5 | — |
| 11-05.1f | c_2 of cos² | 0.25 | — |
| 11-05.3a | c_0 | 1.667 | V |
| 11-05.3b | magnitude of c_1 | 1.378 | V |
| 11-05.3c | A_1 | 2.757 | V |
| 11-05.3d | lowest missing harmonic | 3 | — |
| 11-05.4a | b_1 | 2 | — |
| 11-05.4b | b_2 | −1 | — |
| 11-05.4c | b_3 | 0.6667 | — |
| 11-05.4d | series at t = π | 0 | — |
| 11-05.5a | DC | 0.3183 | — |
| 11-05.5b | amplitude at ω | 0.5 | — |
| 11-05.5c | amplitude at 2ω | 0.2122 | — |
| 11-05.5d | amplitude at 4ω | 0.04244 | — |
| 11-05.6a | magnitude of c_1 | 0.3183 | — |
| 11-05.7a | triangle power | 0.3333 | — |
| 11-05.7b | sum of 1/k⁴ over odd k | 1.0147 | — |
| 11-05.7c | fundamental's share | 98.55 | % |
| 11-05.7d | triangle THD | 12.12 | % |
| 11-05.8a | current THD | 68.74 | % |
| 11-05.8b | total RMS current | 12.13 | A |
| 11-05.8c | power factor | 0.8241 | — |
| 11-05.9a | output fundamental | 0.9003 | V |
| 11-05.9b | its phase | −45 | ° |
| 11-05.9c | output 3rd harmonic | 0.1342 | V |
| 11-05.9d | its phase | −71.57 | ° |
| 11-05.9e | input THD | 48.34 | % |
| 11-05.9f | output THD | 16.35 | % |
| 11-05.10a | 30 MHz amplitude | 0.7003 | V |
| 11-05.10b | residual 10 MHz | 21.01 | mV |
| 11-05.10c | residual 50 MHz | 13.29 | mV |
| 11-05.11a | partial-sum peak | 1.179 | — |
| 11-05.11b | Fejér-sum peak | 0.9868 | — |
| 11-05.12a | PWM frequency | 15625 | Hz |
| 11-05.12b | one LSB | 0.8057 | mV |
| 11-05.12c | half an LSB | 0.4028 | mV |
| 11-05.12d | RC | 0.1311 | s |
| 11-05.12e | corner frequency | 1.214 | Hz |
| 11-05.12f | settling time | 1.181 | s |
| 11-05.13a | 400 kHz: distance to the nearest harmonic | 100 | kHz |
| 11-05.13b | 500 kHz: distance to the nearest harmonic | 200 | kHz |
| 11-05.13c | 600 kHz: distance to the nearest harmonic | 100 | kHz |
| 11-05.14a | total power | 2.7225 | V² |
| 11-05.14b | DC power | 0.6806 | V² |
| 11-05.14c | harmonic power | 2.042 | V² |
| 11-05.14d | sum of sinc² for D = 0.25 | 1.5 | — |
| 11-05.14e | duty with most harmonic power | 0.5 | — |
