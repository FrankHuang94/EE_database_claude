# Solutions 04-09 · Waves and Optics Basics

Problems: [04-09 problems](../problems/04-09-problems.md) · Chapter: [04-09](../chapters/04-09-waves-and-optics.md). Every number below is recomputed by [verify_04_09.py](../verify/verify_04_09.py).

---

## Solutions

### Solution 04-09.1

$\lambda = c/f = $ **12.49 cm**; $T = 1/f = $ **0.4167 ns**; $k = 2\pi/\lambda = $ **50.30 rad/m**.

### Solution 04-09.2

(a) $v = \sqrt{T/\mu} = \sqrt{100/0.002} = $ **223.6 m/s**; $f_1 = v/(2L) = $ **223.6 Hz**.

(b) $f_1 = \sqrt{T/\mu}/(2L)$, so $T = \mu(2Lf_1)^2 = 0.002\times(440)^2 = $ **387.2 N**. Frequency goes as the square root of tension: doubling the pitch needs four times the tension.

### Solution 04-09.3

A tone at the average frequency, 441.5 Hz, whose loudness rises and falls at the beat frequency $|443 - 440| = $ **3 Hz**.

### Solution 04-09.4

$\Delta y = \lambda L/d = 532\times10^{-9}\times2/0.5\times10^{-3} = $ **2.128 mm**.

### Solution 04-09.5

(a) $\sin\theta = 0.5 - 1/0.75 = -0.8333$, so θ = **−56.44°**: a second beam on the other side of broadside, wasting power and picking up interference.

(b) The grating lobe at $\sin\theta_0 - \lambda/d$ stays outside the visible range ($|\sin\theta| > 1$) only if $\lambda/d > 1 + \sin\theta_0$, i.e. $d/\lambda < 1/(1 + 0.5) = $ **0.6667**. Arrays that steer widely use about λ/2.

### Solution 04-09.6

$\sin\theta = \lambda/a = 0.0633$, so θ = **3.629°**. The central band runs between the first minima on either side: width $2L\tan\theta = $ **126.9 mm** on a screen 1 m away. A slit only 16 wavelengths wide spreads light substantially.

### Solution 04-09.7

$\theta = 1.22\lambda/D = 1.22\times550\times10^{-9}/5\times10^{-3} = $ **1.342×10⁻⁴ rad**; at 100 m, **13.42 mm**. A phone camera cannot resolve finer than about a centimeter at that distance, whatever its pixel count.

### Solution 04-09.8

(a) $n_c = \sqrt{3.48} = $ **1.865**.

(b) Thickness $\lambda/(4n_c) = 1550/(4\times1.9) = $ **203.9 nm**. $R = \big(\frac{3.48 - 1.9^2}{3.48 + 1.9^2}\big)^2 = \big(\frac{-0.13}{7.09}\big)^2 = $ **0.03362%**, down from 30.6%, because silicon nitride's index is close to ideal.

### Solution 04-09.9

(a) $\sin\theta_2 = \sin30°/1.5 = 0.3333$, so θ₂ = **19.47°**.

(b) $\arcsin(1/1.5) = $ **41.81°**.

(c) $\arcsin(1.444/3.48) = $ **24.52°**. Light in a silicon waveguide clad by oxide is totally reflected for any angle beyond 24.5° from the normal; the large index contrast confines the guided mode to a few hundred nanometers, allowing tight bends and dense photonic circuits ([24-08](../../24-high-speed-io-signal-integrity-and-photonics/chapters/24-08-silicon-photonics.md)).

### Solution 04-09.10

$\text{NA} = \sqrt{1.48^2 - 1.46^2} = $ **0.2425**; acceptance half-angle $\arcsin0.2425 = $ **14.03°**: twice the single-mode example's, easing alignment.

### Solution 04-09.11

(a) A ray enters the end face from air at angle θ to the axis and refracts to $\theta_1$: $\sin\theta = n_1\sin\theta_1$. Inside, it meets the core boundary at $90° - \theta_1$ from that boundary's normal; to be trapped, $n_1\sin(90° - \theta_1) \ge n_2$, i.e. $\cos\theta_1 \ge n_2/n_1$. At the limit, $\sin\theta_1 = \sqrt{1 - n_2^2/n_1^2}$, so $\sin\theta_{\max} = n_1\sin\theta_1 = \sqrt{n_1^2 - n_2^2}$.

(b) Fiber $2\times0.5 = 1.0$ dB plus connectors $2\times0.4 = 0.8$ dB: **1.8 dB**. Received power **−1.8 dBm**. Short-reach links have generous loss budgets; their limits are cost and power.

### Solution 04-09.12

(a) $\Delta t = DL\Delta\lambda = 17\times40\times0.08 = $ **54.4 ps**.

(b) $T_b \ge 2\Delta t = 108.8$ ps, so the bit rate is at most $1/108.8$ ps = **9.191 Gb/s**. Faster links over this distance need narrower sources, operation near 1310 nm, or electronic dispersion compensation.

### Solution 04-09.13

After the first: ½. After the second (30° to the first): $\tfrac12\cos^230° = $ **0.375**. After the third (60° to the second): $0.375\times\cos^260° = $ **0.09375**.

### Solution 04-09.14

(a) At the quarter-wave condition $2\delta = \pi$, so $\cos2\delta = -1$ and $R = \frac{(r_1 - r_2)^2}{(1 - r_1r_2)^2}$. Substituting $r_1$ and $r_2$ and clearing denominators, $\frac{r_1 - r_2}{1 - r_1r_2} = \frac{n_0n_s - n_c^2}{n_0n_s + n_c^2}$ (multiply numerator and denominator by $(n_0 + n_c)(n_c + n_s)$), the formula of Example 04-09.3.

(b) With $r_1 = -0.1597$, $r_2 = -0.04167$ and $d$ = 99.64 nm: at 450 nm $R$ = **1.721%**; at 650 nm **1.563%** (against 1.411% at the design wavelength). A single layer works over a broad but not unlimited band.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-09.1a | wavelength at 2.4 GHz | 12.49 | cm |
| 04-09.1b | period | 0.4167 | ns |
| 04-09.1c | wavenumber | 50.30 | rad/m |
| 04-09.2a | wave speed | 223.6 | m/s |
| 04-09.2b | fundamental | 223.6 | Hz |
| 04-09.2c | tension for 440 Hz | 387.2 | N |
| 04-09.3a | beat frequency | 3 | Hz |
| 04-09.4a | fringe spacing | 2.128 | mm |
| 04-09.5a | grating-lobe direction | −56.44 | ° |
| 04-09.5b | largest spacing without grating lobes | 0.6667 | λ |
| 04-09.6a | first-minimum angle | 3.629 | ° |
| 04-09.6b | central band width at 1 m | 126.9 | mm |
| 04-09.7a | angular resolution | 1.342×10^-4 | rad |
| 04-09.7b | resolvable separation at 100 m | 13.42 | mm |
| 04-09.8a | ideal coating index for silicon | 1.865 | — |
| 04-09.8b | silicon-nitride quarter-wave thickness | 203.9 | nm |
| 04-09.8c | residual reflectance | 0.03362 | % |
| 04-09.9a | refraction angle | 19.47 | ° |
| 04-09.9b | critical angle, glass to air | 41.81 | ° |
| 04-09.9c | critical angle, silicon to oxide | 24.52 | ° |
| 04-09.10a | multimode NA | 0.2425 | — |
| 04-09.10b | acceptance half-angle | 14.03 | ° |
| 04-09.11a | total link loss | 1.8 | dB |
| 04-09.11b | received power | −1.8 | dBm |
| 04-09.12a | pulse spreading | 54.4 | ps |
| 04-09.12b | highest bit rate | 9.191 | Gb/s |
| 04-09.13a | after the second polarizer | 0.375 | — |
| 04-09.13b | after the third polarizer | 0.09375 | — |
| 04-09.14a | reflectance at 450 nm | 1.721 | % |
| 04-09.14b | reflectance at 650 nm | 1.563 | % |
