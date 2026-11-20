# Solutions 11-06 · The Continuous-Time Fourier Transform

Problems: [11-06 problems](../problems/11-06-problems.md) · Chapter: [11-06](../chapters/11-06-continuous-time-fourier-transform.md). Every number below is recomputed by [verify_11_06.py](../verify/verify_11_06.py), which evaluates the transform integrals numerically.

---

## Solutions

### Solution 11-06.1

(a) Write $e^{-3t}u(t - 2) = e^{-6}\,e^{-3(t - 2)}u(t - 2)$: a delayed exponential times a constant. By the time-shift property, $X = e^{-6}e^{-j2\omega}/(3 + j\omega)$, so $\lvert X(0)\rvert = e^{-6}/3$ = **8.26 × 10⁻⁴**.

(b) $e^{-2\lvert t\rvert} = e^{-2t}u(t) + e^{2t}u(-t)$, whose transforms are $1/(2 + j\omega)$ and (by time reversal) $1/(2 - j\omega)$. The sum is $4/(4 + \omega^2)$, real and even as the signal is, with $X(0)$ = **1**, its area.

(c) The 10 ms pulse has transform $0.01\operatorname{sinc}(0.01f)$; multiplying by the cosine places half-height copies at ±1 kHz: $X(f) = 0.005\operatorname{sinc}(0.01(f - 1000)) + 0.005\operatorname{sinc}(0.01(f + 1000))$. The peak is **0.005** (V·s) at ±1 kHz; the other copy's sinc is zero there (its argument is 20).

### Solution 11-06.2

(a) $1/(2 + j\omega) \leftrightarrow e^{-2t}u(t)$, and by frequency differentiation $t\,e^{-2t}u(t) \leftrightarrow 1/(2 + j\omega)^2$ (equivalently, the convolution of $e^{-2t}u(t)$ with itself). Its peak is at $t$ = **0.5** s, where it equals $0.5e^{-1}$ = **0.1839**.

(b) $2\cos3t$, by the pair for the cosine.

(c) $x(t) = \sin(Wt)/(\pi t)$, the ideal low-pass impulse response.

### Solution 11-06.3

$E = \frac{1}{2\pi}\int\lvert X\rvert^2d\omega = \frac{1}{2\pi}\cdot2W = W/\pi$. For $W = 2\pi \times 1000$: **2000** (s⁻¹, for a signal in s⁻¹; a voltage $V_0\sin(Wt)/(\pi t)$ would have $V_0^2$ times this in V²·s with $V_0$ in V·s). The time integral $\int\sin^2(Wt)/(\pi t)^2dt$ is not elementary; the frequency domain makes it trivial.

### Solution 11-06.4

First nulls at $1/T$: **100** MHz and **1** GHz. Energies $V^2T$: **10** V²·ns and **1** V²·ns. Spectral magnitude at DC equals the area $VT$: 10 and 1 V·ns, a ratio of **10**. The shorter pulse spreads ten times less energy over ten times more bandwidth.

### Solution 11-06.5

(a) Each pulse has transform $T\operatorname{sinc}(fT)$, so the triangle has $T^2\operatorname{sinc}^2(fT)$.

(b) For $T = 1$: $X(0)$ = **1** (the triangle's area, base 2, height 1); $X(0.5) = \operatorname{sinc}^2(0.5) = (2/\pi)^2$ = **0.4053**.

(c) As $1/f^2$: the triangle is continuous with corners (no jumps), so by the smoothness rule its spectrum falls one power faster than a pulse's. The convolution theorem says the same: two $1/f$ factors multiply.

### Solution 11-06.6

Time domain: $\int_0^\infty\frac{1}{\tau^2}e^{-2t/\tau}dt = \frac{1}{2\tau}$ = **500** s⁻¹. Parseval: $\frac{1}{2\pi}\int\frac{d\omega}{1 + \omega^2\tau^2} = \frac{1}{2\pi}\cdot\frac{\pi}{\tau} = \frac{1}{2\tau}$, the same. This quantity, $\int\lvert H(f)\rvert^2df$, is the filter's **noise bandwidth** (for a DC gain of 1): $1/(4\tau)$ in one-sided hertz, $\pi/2$ times its −3 dB bandwidth, the factor of 01-06 and 03-06.

### Solution 11-06.7

(a) Numerator and denominator are complex conjugates, so their magnitudes are equal: $\lvert H\rvert = 1$ at every frequency.

(b) $\angle H = -\arctan(\omega\tau) - \arctan(\omega\tau) = -2\arctan(\omega\tau)$. Group delay: $\tau_g = -\frac{d\angle H}{d\omega} = \frac{2\tau}{1 + \omega^2\tau^2}$.

(c) At $\omega = 0$: $2\tau$ = **2** µs. At $\omega = 1/\tau$: τ = **1** µs.

(d) Yes. No frequency is attenuated, but low frequencies are delayed twice as long as those near $1/\tau$, so a pulse containing both spreads out: phase distortion. All-pass sections are used deliberately to *correct* such distortion elsewhere (group-delay equalizers).

### Solution 11-06.8

(a) $h(t) = \sin(Wt)/(\pi t)$ with $W = 2\pi \times 1000$ rad/s. Its peak, at $t = 0$, is $W/\pi$ = **2000** s⁻¹; its first zero is at $Wt = \pi$, $t$ = **0.5** ms.

(b) The step response $\tfrac12 + \frac1\pi\operatorname{Si}(Wt)$ peaks where its derivative $h$ first returns to zero, at $t$ = 0.5 ms, with value **1.0895**: the Gibbs overshoot.

### Solution 11-06.9

The energy fraction within $\lvert f\rvert < W$ is $\int_{-WT}^{WT}\operatorname{sinc}^2u\,du$. Setting it to 0.9 gives $WT$ = **0.8485**, so 90% lies within 0.849 MHz, inside the first null at 1 MHz (which holds 90.28%). Setting it to 0.99 gives $WT$ = **10.29**: 99% needs 10.3 MHz, ten times the first-null bandwidth. The last 9% of a sharp-edged pulse's energy is spread over a very wide band.

### Solution 11-06.10

(a) $0.35/2\ \text{GHz}$ = **175** ps.

(b) $\sqrt{175^2 + 300^2}$ = **347.3** ps, about **16**% slow: a 2 GHz scope is not fast enough to measure a 300 ps edge accurately; the "five times faster" guideline calls for about 60 ps.

### Solution 11-06.11

(a) $\lvert x\rvert^2 = e^{-2a\lvert t\rvert}$, so $\sigma_t^2 = \int t^2e^{-2a\lvert t\rvert}dt/\int e^{-2a\lvert t\rvert}dt = 1/(2a^2)$. With $X = 2a/(a^2 + \omega^2)$, $\sigma_\omega^2 = \int\omega^2\lvert X\rvert^2d\omega/\int\lvert X\rvert^2d\omega = a^2$. The product is $\sigma_t\sigma_\omega = 1/\sqrt2$ = **0.7071**, above the Gaussian's minimum of 0.5, as the uncertainty principle requires.

(b) For a pulse, $\lvert X\rvert^2$ falls as $1/\omega^2$, so $\omega^2\lvert X\rvert^2$ tends to a constant (on average) and $\int\omega^2\lvert X\rvert^2d\omega$ diverges. The same holds for $e^{-at}u(t)$, whose spectrum also falls as $1/\omega$. Any signal with a jump has infinite RMS bandwidth, which is one reason RMS widths are used mainly for smooth pulses.

### Solution 11-06.12

(a) Multiplying by $\cos(2\pi f_ct)$ shifts half-height copies of the message spectrum to ±1 MHz. The positive-frequency copy occupies **995** to **1005** kHz.

(b) **10** kHz: the message's spectrum extends from −5 to +5 kHz (a real signal's spectrum is symmetric), and modulation moves the whole two-sided spectrum, both halves, up to the carrier. Single-sideband techniques (11-11) remove one half.

### Solution 11-06.13

(a) $10^{-32/20}$ = **0.0251** of the amplitude.

(b) $15.5\ \text{dB}/(1\ \text{dB/in})$ ≈ **15.5** inches.

(c) Twice the frequency at twice the loss per inch: about **7.75** inches for the same allocation. Real board loss grows somewhat faster than proportionally at high frequency (dielectric loss is proportional to frequency, conductor loss grows as its square root, and roughness adds), so this estimate is optimistic for some materials and pessimistic for others. The point stands: doubling the Nyquist frequency roughly halves the reach, which is why PCIe 6.0 chose PAM4.

### Solution 11-06.14

(a) $0.2619 \times 2000$ = **523.9** Hz.

(b) $u = 60/2000 = 0.03$: $20\log_{10}\operatorname{sinc}^3(0.03)$ = **−0.039** dB, essentially no attenuation; the faster rate passes mains hum untouched.

(c) The notches fall at every multiple of $f_{DR}$. Both 50 and 60 Hz, and all their harmonics, are multiples of **10** Hz, so a 10 SPS sinc filter notches them all. Precision weigh-scale and temperature ADCs use exactly such slow, mains-rejecting rates; the ADS1292R, built for ECG bandwidths, does not offer it (its lowest rate is 125 SPS).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-06.1a | magnitude at DC, (a) | 8.26e-4 | — |
| 11-06.1b | X(0), (b) | 1 | — |
| 11-06.1c | peak, (c) | 0.005 | — |
| 11-06.2a | time of the peak | 0.5 | s |
| 11-06.2b | peak value | 0.1839 | — |
| 11-06.3a | energy for W = 2π·1000 | 2000 | — |
| 11-06.4a | first null, 10 ns | 100 | MHz |
| 11-06.4b | first null, 1 ns | 1 | GHz |
| 11-06.4c | energy, 10 ns | 10 | V²·ns |
| 11-06.4d | energy, 1 ns | 1 | V²·ns |
| 11-06.4e | DC ratio | 10 | — |
| 11-06.5a | triangle X(0) | 1 | — |
| 11-06.5b | triangle X(0.5) | 0.4053 | — |
| 11-06.6a | energy of h | 500 | s⁻¹ |
| 11-06.7a | group delay at DC | 2 | µs |
| 11-06.7b | group delay at 1/τ | 1 | µs |
| 11-06.8a | impulse-response peak | 2000 | s⁻¹ |
| 11-06.8b | first zero / time of step peak | 0.5 | ms |
| 11-06.8c | step-response peak | 1.0895 | — |
| 11-06.9a | 90% energy bandwidth × T | 0.8485 | — |
| 11-06.9b | 99% energy bandwidth × T | 10.29 | — |
| 11-06.10a | scope rise time | 175 | ps |
| 11-06.10b | displayed rise time | 347.3 | ps |
| 11-06.10c | error | 16 | % |
| 11-06.11a | product for the two-sided exponential | 0.7071 | — |
| 11-06.12a | lower edge | 995 | kHz |
| 11-06.12b | upper edge | 1005 | kHz |
| 11-06.12c | bandwidth | 10 | kHz |
| 11-06.13a | amplitude at 32 dB | 0.0251 | — |
| 11-06.13b | trace length, 16 GHz | 15.5 | in |
| 11-06.13c | trace length, 32 GHz | 7.75 | in |
| 11-06.14a | −3 dB at 2 kSPS | 523.9 | Hz |
| 11-06.14b | gain at 60 Hz | −0.039 | dB |
| 11-06.14c | notching output rate | 10 | SPS |
