# Solutions 16-07 · IIR Filter Design

Problems: [16-07 problems](../problems/16-07-problems.md) · Chapter: [16-07](../chapters/16-07-iir-filter-design.md). Every number below is recomputed by [verify_16_07.py](../verify/verify_16_07.py): designs against SciPy's `butter`, `cheby1`, `ellip` and `bilinear_zpk`, prototypes against `buttap` and `cheb1ap`, orders against `buttord`, `cheb1ord` and `ellipord`, and group delays against `scipy.signal.group_delay`.

---

## Solutions

### Solution 16-07.1

(a) $f_a = (8000/\pi)\tan(\pi f_d/8000)$ with $8000/\pi = 2546.5$ Hz:

- 1 kHz: $\tan(\pi/8) = 0.41421$, so **1054.8** Hz;
- 2 kHz: $\tan(\pi/4) = 1$, so **2546.5** Hz;
- 3 kHz: $\tan(3\pi/8) = 2.4142$, so **6147.7** Hz.

(b) The analog filter's −3 dB point (10 kHz) is carried to $f_d = (48{,}000/\pi)\arctan(\pi \times 10{,}000/48{,}000) = 15{,}279 \times \arctan(0.65450)$ = **8855** Hz, **11.5**% low. The filter's order does not matter: every point of the response moves by the same warping.

### Solution 16-07.2

(a) With $c = 2f_s = 16{,}000$ s⁻¹: $z = (c + s)/(c - s) = (15{,}000 + j5000)/(17{,}000 - j5000)$. Multiplying by the conjugate of the denominator, $z = (15{,}000 + j5000)(17{,}000 + j5000)/(17{,}000^2 + 5000^2) = (2.30 \times 10^8 + j1.60 \times 10^8)/3.14 \times 10^8$ = **0.7325 + j0.5096**, radius **0.8923**: inside the circle, as a stable pole should be.

(b) With $s = \sigma + j\Omega$, $\lvert c + s\rvert^2 - \lvert c - s\rvert^2 = (c + \sigma)^2 - (c - \sigma)^2 = 4c\sigma$ (the $\Omega^2$ terms cancel). Since $c > 0$, $\lvert z\rvert = \lvert c + s\rvert/\lvert c - s\rvert < 1$ exactly when $\sigma < 0$.

### Solution 16-07.3

$D = (10^4 - 1)/(10^{0.1} - 1) = 9999/0.25893$ = **38,617**; $\sqrt D = 196.5$.

- Butterworth: $\log_{10}D/(2\log_{10}2) = 4.5868/0.60206$ = **7.62**, so **8**.
- Chebyshev: $\operatorname{arccosh}196.5/\operatorname{arccosh}2 = 5.9738/1.3170$ = **4.54**, so **5**.
- Elliptic: the elliptic-integral formula gives **3.32**, so **4**.

The elliptic filter needs half the Butterworth's order.

### Solution 16-07.4

Prewarp: $K = \tan(\pi \times 100/48{,}000)$ = **0.006545**. With $s/\Omega_c = \frac1K\frac{1 - z^{-1}}{1 + z^{-1}}$:

$$
H(z) = \frac{s/\Omega_c}{s/\Omega_c + 1} = \frac{1 - z^{-1}}{(1 - z^{-1}) + K(1 + z^{-1})} = \frac{1}{1 + K}\,\frac{1 - z^{-1}}{1 - \frac{1 - K}{1 + K}z^{-1}} .
$$

Gain constant $1/(1 + K)$ = **0.99350**; pole $(1 - K)/(1 + K)$ = **0.98699**; zero at $z = 1$ (DC is blocked). At Nyquist, $H(-1) = \frac{1}{1 + K}\cdot\frac{2}{1 + p} = 1$ exactly. Time constant $-1/\ln p$ = **76.4** samples = **1.59** ms (the approximation $1/(1 - p)$ gives 76.9), matching the analog $1/\Omega_c$ = 1.59 ms. This is the DC blocker of 16-02, $(1 - z^{-1})/(1 - az^{-1})$, with $a = 0.98699$ and a gain of 0.99350 that makes the high-frequency gain exactly 1; its corner $1 - a = 0.0130$ rad/sample matches $2\pi \times 100/48{,}000 = 0.0131$.

### Solution 16-07.5

(a) $s_k = e^{j\pi(2k + 2)/6}$ for $k = 1, 2, 3$: angles 120°, 180°, 240°, so $s = -\tfrac12 \pm j\tfrac{\sqrt3}{2}$ and $s = -1$. Then $(s + \tfrac12)^2 + \tfrac34 = s^2 + s + 1$ and

$$
H(s) = \frac{1}{(s + 1)(s^2 + s + 1)} .
$$

(b) $s_k = e^{j\pi(2k + 3)/8}$: angles **112.5°**, **157.5°**, **202.5°** and **247.5°**. A pair at angle $180° \pm \alpha$ from the positive real axis has $\zeta = \cos\alpha$: the pair at ±157.5° has $\zeta = \cos 22.5°$ = **0.924**, the pair at ±112.5° has $\zeta = \cos 67.5°$ = **0.383**.

### Solution 16-07.6

$\varepsilon = \sqrt{10^{0.1} - 1}$ = **0.5088**; $a = \frac13\operatorname{arcsinh}(1/0.5088) = \frac13\operatorname{arcsinh}(1.9652)$ = **0.4760**; $\sinh a$ = **0.4942**, $\cosh a$ = **1.1154**. With $u_k$ = 30°, 90°, 150°:

$$
s_{1,3} = -0.4942 \times 0.5 \pm j1.1154 \times 0.8660 = -0.2471 \pm j0.9660, \qquad s_2 = -0.4942 .
$$

The order is odd, so the DC gain is **1** (0 dB): the response starts at the top of the ripple and the 1 dB dips occur inside the passband.

### Solution 16-07.7

$\Omega_cT = 2\pi \times 2000/8000 = \pi/2$; $H(z) = 1.5708/(1 - e^{-\pi/2}z^{-1})$ with pole $e^{-\pi/2} = 0.2079$. DC gain $1.5708/0.7921$ = **1.983**; Nyquist gain $1.5708/1.2079$ = **1.300**; ratio **0.656**. The analog filter at 4 kHz, relative to DC, has $1/\sqrt{1 + 2^2}$ = **0.447**. Two effects of 16-07 §3.3 combine. The impulse response jumps at $t = 0$, so the constant $\Omega_cT/2 = \pi/4$ = **0.785** is added at every frequency. The aliased sum alone gives a DC gain of $(\pi/4)\coth(\pi/4)$ = **1.198** and a Nyquist gain of $(\pi/4)\tanh(\pi/4)$ = **0.515**, a ratio of **0.430**, close to the analog 0.447. So the endpoint term causes both the nearly doubled DC gain and most of the raised ratio (0.656). Impulse invariance is a poor choice when the cutoff is a quarter of the sampling rate, and halving $h[0]$ is the first repair.

### Solution 16-07.8

For a pole $\rho e^{j\theta}$, the delay contribution is $-(\rho^2 - \rho\cos(\omega - \theta))/(1 - 2\rho\cos(\omega - \theta) + \rho^2)$.

- Near pole ($\omega - \theta = 0$): $-(\rho^2 - \rho)/(1 - \rho)^2 = \rho/(1 - \rho)$ = **19**.
- Far pole ($\omega - \theta = \pi/2$): $-\rho^2/(1 + \rho^2) = -0.9025/1.9025 = -0.474$.

Total **18.53** samples. The single-pole approximation (19) is within 3%: near its own angle, a pole close to the circle dominates.

### Solution 16-07.9

(a) Prewarped edges at $f_s$ = 1 kHz: $(1000/\pi)\tan(0.04\pi)$ = **40.21** Hz and $(1000/\pi)\tan(0.05\pi)$ = **50.42** Hz. The elliptic bound is **6.76**, so order **7**, which the lab checks: exactly 0.5 dB of passband ripple and **60.0** dB of attenuation from 50 Hz.

(b) $\delta_p = (10^{0.025} - 1)/(10^{0.025} + 1) = 0.02877$, $\delta_s = 0.001$, $\Delta\omega = 2\pi \times 10/1000 = 0.06283$: $M \approx (-10\log_{10}(2.877 \times 10^{-5}) - 13)/(2.324 \times 0.06283)$ = **222.0**, so about 223 taps and **112** multiplications after folding.

(c) The order-7 elliptic filter as sections needs **12** multiplications per output: about **9.3** times fewer. A 10 Hz transition at a 1 kHz rate is very sharp in normalized terms, which is where IIR filters shine.

### Solution 16-07.10

With $K = 1$, $v = (1 - z^{-1})/(1 + z^{-1})$ replaces $s/\Omega_c$ in $1/\big((v + 1)(v^2 + v + 1)\big)$. Over the common denominator $(1 + z^{-1})$:

- $v + 1 = \dfrac{2}{1 + z^{-1}}$;
- $v^2 + v + 1 = \dfrac{(1 - z^{-1})^2 + (1 - z^{-1})(1 + z^{-1}) + (1 + z^{-1})^2}{(1 + z^{-1})^2} = \dfrac{3 + z^{-2}}{(1 + z^{-1})^2}$, since the $z^{-1}$ terms cancel ($-2 + 0 + 2$) and the $z^{-2}$ terms give $1 - 1 + 1$.

So

$$
H(z) = \frac{(1 + z^{-1})^3}{2(3 + z^{-2})} = \frac{\tfrac16(1 + 3z^{-1} + 3z^{-2} + z^{-3})}{1 + \tfrac13z^{-2}} .
$$

Poles: $z = 0$ and $z^2 = -1/3$, so $z = \pm j0.5774$ (radius **0.5774**); three zeros at $z = -1$. DC: $H(1) = 8/(2 \times 4)$ = **1**. At 2 kHz ($\omega = \pi/2$, $z^{-1} = -j$): $(1 - j)^3 = -2 - 2j$, $\lvert\cdot\rvert = 2\sqrt2$; $3 + z^{-2} = 3 - 1 = 2$; $\lvert H\rvert = 2\sqrt2/4 = 1/\sqrt2$, **−3.01** dB, as a Butterworth filter must give at its cutoff.

### Solution 16-07.11

(a) An all-pass filter can only *add* delay (its group delay is positive everywhere), so the flattest result has a constant delay at least equal to the peak, **69.51** samples (at the 4 kHz edge). At DC the equalizer must add at least $69.51 - 7.99$ = **61.52** samples.

(b) $69.51/48{,}000$ = **1.448** ms, against $68/48{,}000$ = **1.417** ms for the equiripple FIR filter: the equalized IIR filter is *slower*.

(c) Once linear phase is required, the IIR filter's low-delay advantage disappears and its multiplication advantage shrinks (the equalizer needs several more sections and still only approximates a flat delay). That is why linear-phase applications use FIR filters.

### Solution 16-07.12

(a) The expanded denominator is $1 - 6.543z^{-1} + 19.31z^{-2} - 33.47z^{-3} + 37.19z^{-4} - \cdots$; the largest coefficient is **37.19**, which needs **6** integer bits plus a sign ($2^5 = 32 < 37.19 < 64$).

(b) Largest pole radius after rounding the single polynomial:

| Fractional bits | 16 | 14 | 12 | 10 |
|---|---|---|---|---|
| Largest pole radius | **0.98451** | **0.97989** | **1.03017** | **1.10277** |

At 12 bits a pole is outside the unit circle: the filter is **unstable**. (Even at 16 bits the largest radius has moved from 0.98499 to 0.98451, changing the response near the band edge.)

(c) Rounding each biquad's $a_1, a_2$ separately, the largest radius stays between 0.984 and 0.986 all the way down to 8 fractional bits (**0.98425** at 8 bits): always stable.

(d) The roots of a high-degree polynomial with clustered roots are hypersensitive to its coefficients: a perturbation $\Delta a_k$ moves a root by roughly $\Delta a_k\,p^{N-k}/\prod_{j\ne i}(p_i - p_j)$, and the product of small distances between clustered poles in the denominator is tiny. A biquad's two poles depend only on its own two coefficients, with no clustered partners to amplify the error. This is why SciPy recommends `output='sos'` and why every product implements IIR filters as cascades of sections (16-08).

### Solution 16-07.13

(a) With $\Omega = 2f_s\tan(\pi f/f_s)$: passband edges **6292** and **12,639** rad/s; stopband edges **3143** and **25,723** rad/s. (Warping moves the 4 kHz edge by 2.3%, the 2 kHz edge by 0.6% and the others by less than 0.2%.)

(b) $\Omega_0 = \sqrt{6292 \times 12{,}639}$ = **8918** rad/s and $B = 12{,}639 - 6292$ = **6346** rad/s. The centre maps back to $f = (f_s/\pi)\arctan(\Omega_0/2f_s)$ = **1415** Hz: the geometric mean of 1 and 2 kHz (1414 Hz), not the arithmetic mean.

(c) A stopband edge maps to $\lvert\Omega_s^2 - \Omega_0^2\rvert/(B\Omega_s)$: **3.492** for 500 Hz and **3.566** for 4 kHz. The smaller ratio, 3.492 at the lower edge, is the harder requirement and governs.

(d) $D = (10^4 - 1)/(10^{0.1} - 1)$ = 38,617, so $N \ge \log_{10}D/(2\log_{10}3.492)$ = **4.22**: a prototype of order **5**. Each pole becomes a pair, so the band-pass filter has order **10**, built as **5** biquads. SciPy's `buttord` returns the same prototype order, and the resulting filter has 48.4 dB of attenuation at 500 Hz and 49.4 dB at 4 kHz, with exactly 1 dB at both passband edges.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-07.1a | prewarped 1 kHz | 1054.8 | Hz |
| 16-07.1b | prewarped 2 kHz | 2546.5 | Hz |
| 16-07.1c | prewarped 3 kHz | 6147.7 | Hz |
| 16-07.1d | unprewarped −3 dB point | 8855 | Hz |
| 16-07.1e | error | 11.5 | % |
| 16-07.2a | real part of z | 0.7325 | — |
| 16-07.2b | imaginary part of z | 0.5096 | — |
| 16-07.2c | radius | 0.8923 | — |
| 16-07.3a | discrimination | 38617 | — |
| 16-07.3b | Butterworth bound | 7.62 | — |
| 16-07.3c | Chebyshev bound | 4.54 | — |
| 16-07.3d | elliptic bound | 3.32 | — |
| 16-07.4a | K | 0.006545 | — |
| 16-07.4b | gain constant | 0.99350 | — |
| 16-07.4c | pole | 0.98699 | — |
| 16-07.4d | time constant | 76.4 | samples |
| 16-07.4e | time constant | 1.59 | ms |
| 16-07.5a | fourth-order pole angle 1 | 112.5 | ° |
| 16-07.5b | fourth-order pole angle 2 | 157.5 | ° |
| 16-07.5c | damping of the pair nearer the real axis | 0.924 | — |
| 16-07.5d | damping of the pair nearer the jΩ axis | 0.383 | — |
| 16-07.6a | ε | 0.5088 | — |
| 16-07.6b | a | 0.4760 | — |
| 16-07.6c | sinh a | 0.4942 | — |
| 16-07.6d | cosh a | 1.1154 | — |
| 16-07.6e | complex pole real part | −0.2471 | — |
| 16-07.6f | complex pole imaginary part | 0.9660 | — |
| 16-07.6g | DC gain | 1 | — |
| 16-07.7a | DC gain | 1.983 | — |
| 16-07.7b | Nyquist gain | 1.300 | — |
| 16-07.7c | Nyquist over DC | 0.656 | — |
| 16-07.7d | analog gain at 4 kHz over DC | 0.447 | — |
| 16-07.7e | endpoint term | 0.785 | — |
| 16-07.7f | aliased-sum DC gain | 1.198 | — |
| 16-07.7g | aliased-sum Nyquist gain | 0.515 | — |
| 16-07.7h | aliased-sum ratio | 0.430 | — |
| 16-07.8a | near-pole delay | 19 | samples |
| 16-07.8b | total group delay | 18.53 | samples |
| 16-07.9a | elliptic bound | 6.76 | — |
| 16-07.9f | prewarped 40 Hz | 40.21 | Hz |
| 16-07.9g | prewarped 50 Hz | 50.42 | Hz |
| 16-07.9h | order-7 attenuation from 50 Hz | 60.0 | dB |
| 16-07.9b | FIR order estimate | 222.0 | — |
| 16-07.9c | FIR folded multiplications | 112 | — |
| 16-07.9d | elliptic SOS multiplications | 12 | — |
| 16-07.9e | ratio | 9.3 | — |
| 16-07.10a | pole radius | 0.5774 | — |
| 16-07.10b | DC gain | 1 | — |
| 16-07.10c | gain at 2 kHz | −3.01 | dB |
| 16-07.11a | equalized delay at least | 69.51 | samples |
| 16-07.11b | delay to add at DC | 61.52 | samples |
| 16-07.11c | equalized delay | 1.448 | ms |
| 16-07.11d | FIR delay | 1.417 | ms |
| 16-07.12a | largest direct-form coefficient | 37.19 | — |
| 16-07.12b | integer bits | 6 | bits |
| 16-07.12c | pole radius, 16 bits | 0.98451 | — |
| 16-07.12d | pole radius, 14 bits | 0.97989 | — |
| 16-07.12e | pole radius, 12 bits | 1.03017 | — |
| 16-07.12f | pole radius, 10 bits | 1.10277 | — |
| 16-07.12g | biquad pole radius, 8 bits | 0.98425 | — |
| 16-07.13a | prewarped lower passband edge | 6292 | rad/s |
| 16-07.13b | prewarped upper passband edge | 12639 | rad/s |
| 16-07.13c | prewarped lower stopband edge | 3143 | rad/s |
| 16-07.13d | prewarped upper stopband edge | 25723 | rad/s |
| 16-07.13e | centre Ω0 | 8918 | rad/s |
| 16-07.13f | bandwidth B | 6346 | rad/s |
| 16-07.13g | digital centre frequency | 1415 | Hz |
| 16-07.13h | prototype stopband, lower edge | 3.492 | — |
| 16-07.13i | prototype stopband, upper edge | 3.566 | — |
| 16-07.13j | Butterworth order bound | 4.22 | — |
| 16-07.13k | prototype order | 5 | — |
| 16-07.13l | band-pass order | 10 | — |
| 16-07.13m | biquads | 5 | — |
| 16-07.13n | attenuation at 500 Hz | 48.4 | dB |
| 16-07.13o | attenuation at 4 kHz | 49.4 | dB |
