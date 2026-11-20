# Solutions 11-08 · The Laplace Transform and System Functions

Problems: [11-08 problems](../problems/11-08-problems.md) · Chapter: [11-08](../chapters/11-08-laplace-transform-and-system-functions.md). Every number below is recomputed by [verify_11_08.py](../verify/verify_11_08.py), which integrates the transform definitions numerically, finds poles with `numpy.roots`, and simulates the step responses.

---

## Solutions

### Solution 11-08.1

$X_1(s) = 1/(s + 4)$ with ROC σ > **−4** (right of the pole), and $X_2(s) = 1/(s + 4)$ with ROC σ < −4 (§3.2): the same formula, opposite ROCs. $X_1(1) = 1/5$ = **0.2**. $X_2(-5) = 1/(-1)$ = **−1**. At $s = 1$ the integral defining $X_2$ diverges: $-\int_{-\infty}^0e^{-5t}dt$ grows without bound as $t \to -\infty$. The formula $1/(s + 4)$ gives a number there, but it is not the transform of $x_2$.

### Solution 11-08.2

$X(s) = \int_0^2e^{-st}dt = (1 - e^{-2s})/s$, with the whole plane as ROC because the pulse has finite duration (§3.3, property 3). Near $s = 0$, $e^{-2s} \approx 1 - 2s$, so $X(s) \to 2$: the singularity is removable, and **$X(0)$ = 2** s, the pulse's area. $X(1) = 1 - e^{-2}$ = **0.8647** s. On the axis, $X(j\omega) = (1 - e^{-j2\omega})/(j\omega) = e^{-j\omega}\cdot2\sin\omega/\omega$, which first vanishes at ω = π = **3.142** rad/s: a pulse of length 2 s has spectral nulls at multiples of $1/(2\ \text{s})$ = 0.5 Hz (11-06).

### Solution 11-08.3

Zero: **−1**. Poles: $s^2 + 6s + 25 = 0$ gives $s = -3 \pm j4$. Their radius is $\omega_0 = \sqrt{9 + 16}$ = **5** rad/s, $\zeta = 3/5$ = **0.6**, and $Q = 1/(2\zeta)$ = **0.8333**. DC gain $H(0) = 1/25$ = **0.04**. Causal with both poles in the left half-plane, so stable.

### Solution 11-08.4

- (i) Right of the only pole, which is in the left half-plane: **causal and stable**.
- (ii) Right of a pole at +1: causal, but the ROC excludes the axis: **causal, unstable** ($h = e^tu(t)$ grows).
- (iii) Left of the pole: $h = -e^{t}u(-t)$, which decays as $t \to -\infty$. The ROC contains the axis: **anticausal, stable**.
- (iv) A strip containing the axis: **stable**, and two-sided, so **noncausal**. By §3.4, $h = -\tfrac14e^{-t}u(t) - \tfrac14e^{3t}u(-t)$.
- (v) $e^{s}$ is a time *advance* of 1 s, so $h(t) = e^{-(t + 1)}u(t + 1)$, which starts at $t = -1$: **noncausal**, although the ROC is a right half-plane, and **stable** (the ROC contains the axis). $h(-0.5) = e^{-0.5}$ = **0.6065**. This is the exception noted in §3.6: a right half-plane ROC proves causality only for rational system functions.

### Solution 11-08.5

Residues: at −1, $(s + 5)/(s + 3) = 4/2$ = **2**; at −3, $(s + 5)/(s + 1) = 2/(-2)$ = **−1**. So $X = 2/(s + 1) - 1/(s + 3)$. The strip −3 < σ < −1 lies right of the pole at −3 (a right-sided term) and left of the pole at −1 (a left-sided term):

$$
x(t) = -e^{-3t}u(t) - 2e^{-t}u(-t) .
$$

$x(1) = -e^{-3}$ = **−0.04979** and $x(-1) = -2e^{1}$ = **−5.437**. The strip does not contain the imaginary axis, so there is no Fourier transform: the left-sided part $-2e^{-t}$ grows as $t \to -\infty$.

### Solution 11-08.6

With $b = 2$ in §3.2: $X(s) = 4/(4 - s^2)$ with ROC −2 < σ < 2. The strip contains the axis, so the Fourier transform is $X(j\omega) = 4/(4 + \omega^2)$: **1** at ω = 0 (the area, $2 \times \tfrac12$) and **0.5** at ω = 2 rad/s. $X(1) = 4/3$ = **1.333**, which checks against $\int e^{-2\lvert t\rvert}e^{-t}dt = \tfrac13 + 1$.

### Solution 11-08.7

$H(s) = 13/(s^2 + 4s + 13)$ (initial rest makes it causal). Poles: $-2 \pm j3$. $\omega_0 = \sqrt{13}$ = **3.606** rad/s, $\zeta = 2/\sqrt{13}$ = **0.5547**, $Q$ = **0.9014**. The magnitude peaks where $\lvert D(j\omega)\rvert^2 = (13 - \omega^2)^2 + 16\omega^2$ is smallest; its derivative with respect to ω² is $2(\omega^2 - 13) + 16 = 0$, at $\omega^2 = 5$: ω = **2.236** rad/s (= $\omega_0\sqrt{1 - 2\zeta^2}$). There $\lvert D\rvert^2 = 64 + 80 = 144$, so the peak is $13/12$ = **1.083**, a mild 0.70 dB rise because ζ is only a little below 0.7071.

### Solution 11-08.8

$H = G/(1 + \beta G) = A_0/(1 + s/\omega_a + \beta A_0)$. Dividing by $1 + \beta A_0$:

$$
H(s) = \frac{A_0/(1 + \beta A_0)}{1 + s/[\omega_a(1 + \beta A_0)]} .
$$

The closed-loop DC gain is $10^5/10\,001$ = **9.999** (almost exactly $1/\beta$), and the pole moved from 10 Hz to $10 \times 10\,001$ Hz = **100.0** kHz. Gain times bandwidth: open loop $10^5 \times 10$ Hz = 1 MHz; closed loop $9.999 \times 100.01$ kHz = **1** MHz. Feedback moves the pole out along the real axis by the factor $1 + \beta A_0$ and divides the gain by the same factor: the gain–bandwidth product of 10-09 is a statement about where the closed-loop pole lands.

### Solution 11-08.9

Poles at −10 and −100; DC gain $1000/1000 = 1$. At ω = 10: the vectors have lengths $\sqrt{10^2 + 10^2}$ = **14.14** and $\sqrt{100^2 + 10^2}$ = **100.5**, at angles 45° and $\arctan(0.1)$ = **5.71**°. So $\lvert H\rvert = 1000/(14.14 \times 100.5)$ = **0.7036** and $\angle H$ = **−50.71**°. At ω = 100: lengths 100.5 and $\sqrt{2} \times 100$ = **141.4**, angles $\arctan 10$ = **84.29**° and 45°, so $\lvert H\rvert$ = **0.07036** and $\angle H$ = **−129.29**°. Each pole costs about 3 dB and 45° at its own frequency, and the other pole adds a little.

### Solution 11-08.10

(a) $\lvert 2 - j\omega\rvert = \sqrt{4 + \omega^2} = \lvert 2 + j\omega\rvert$, so $\lvert H\rvert = 1$. The phase is $-2\arctan(\omega/2)$: **−90**° at ω = 2.

(b) $\tau = 2a/(a^2 + \omega^2)$ with $a = 2$: **1** s at DC and $4/8$ = **0.5** s at ω = 2.

(c) $Y = (2 - s)/[s(s + 2)] = 1/s - 2/(s + 2)$, so $y = 1 - 2e^{-2t}$ for $t > 0$. At $t = 0^+$, $y$ = **−1**: as $s \to \infty$, $H \to -1$, so the step's edge passes straight through inverted. It crosses zero when $e^{-2t} = \tfrac12$, at $t = \ln2/2$ = **0.3466** s, and settles at 1. A flat magnitude does not mean a harmless system: the phase distorts the waveform badly.

### Solution 11-08.11

(a) The complex pair is at $\omega_c e^{\pm j120°} = \omega_c(-\tfrac12 \pm j\tfrac{\sqrt3}{2})$: real part **−0.5** ω_c. Its angle from the negative real axis is 60°, so ζ = cos 60° = **0.5**.

(b) $\lvert H\rvert = 1/\sqrt{1 + 2^6} = 1/\sqrt{65}$: **−18.13** dB.

(c) We need $10\log_{10}(1 + 4^n) \ge 40$, so $4^n \ge 9999$ and $n \ge \log 9999/\log 4 = 6.64$. Order **7** gives 42.1 dB (order 6 gives only 36.1 dB).

### Solution 11-08.12

(a) $H(0) = -3/6$ = **−0.5**.

(b) No. The inverse $1/H = (s + 1)(s + 6)/(s - 3)$ has a pole at +3. With a causal ROC (σ > 3) it is unstable; with a stable ROC (σ < 3) it is anticausal.

(c) Reflect the zero to −3: $H_{min}(s) = -(s + 3)/[(s + 1)(s + 6)]$ and $H_{ap}(s) = (3 - s)/(3 + s)$. Check: $H_{min}H_{ap} = -(3 - s)/[(s + 1)(s + 6)] = (s - 3)/[(s + 1)(s + 6)]$. The minus sign in $H_{min}$ keeps the DC gains equal. The all-pass group delay at DC is $2/3$ = **0.6667** s.

(d) The cascade $H \cdot (1/H_{min}) = H_{ap}$: the magnitude is perfectly equalized, but the all-pass phase remains, $-2\arctan(\omega/3)$, which is **−90**° at ω = 3. An equalizer can flatten the magnitude of a non-minimum-phase channel but cannot remove its excess phase without becoming unstable or noncausal; in practice, a delay is accepted and the residual phase distortion is budgeted.

### Solution 11-08.13

(a) $G = 10^{-6/20} = 0.5012$, so the zero is at $0.5012 \times 21.25$ = **10.65** GHz. At Nyquist, $\lvert H\rvert = \lvert 0.5012 + j1.25\rvert/(1.6008 \times 1.1180)$, or **−2.47** dB, and the boost is $-2.47 + 6$ = **3.53** dB.

(b) Stepping through the settings, −12 dB gives 9.05 dB of boost and **−13** dB gives **10.02** dB: −13 dB is the smallest attenuation that meets 10 dB.

(c) At the deep settings the zero is far below Nyquist, so $G$ is negligible beside $f/f_z$ = 1.25 in the numerator. The Nyquist gain tends to $1.25/(1.6008 \times 1.1180)$, or **−3.12** dB, independent of $g_{DC}$, so the boost tends to $\lvert g_{DC}\rvert - 3.12$ dB. The high-frequency gain is set by the poles; the $g_{DC}$ knob only lowers the low-frequency gain.

### Solution 11-08.14

$Q = f_0/B = 100/4$ = **25**. For a band-pass resonance the −3 dB bandwidth in rad/s is exactly $2\alpha$ (§3.7), so $\alpha = \pi B = \pi \times 4$ MHz, and the poles' real part is **−12.57** × 10⁶ s⁻¹. The ringing envelope $e^{-\alpha t}$ has time constant $1/\alpha$ = **79.58** ns, during which the resonator completes about $f_0/\alpha = Q/\pi$ = **7.958** cycles. (Strictly it rings at the damped frequency $f_d = f_0\sqrt{1 - 1/(4Q^2)}$, so the count is $f_d/\alpha$ = **7.956**; at $Q$ = 25 the difference is negligible.) A high-Q resonator rings for about $Q/\pi$ cycles per $e$-fold decay.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-08.1a | ROC boundary | −4 | s⁻¹ |
| 11-08.1b | X₁(1) | 0.2 | s |
| 11-08.1c | X₂(−5) | −1 | s |
| 11-08.2a | X(0) | 2 | s |
| 11-08.2b | X(1) | 0.8647 | s |
| 11-08.2c | first spectral null | 3.142 | rad/s |
| 11-08.2d | null spacing | 0.5 | Hz |
| 11-08.3a | zero | −1 | s⁻¹ |
| 11-08.3b | ω₀ | 5 | rad/s |
| 11-08.3c | ζ | 0.6 | — |
| 11-08.3d | Q | 0.8333 | — |
| 11-08.3e | DC gain | 0.04 | — |
| 11-08.4a | h(−0.5) for (v) | 0.6065 | — |
| 11-08.5a | residue at −1 | 2 | — |
| 11-08.5b | residue at −3 | −1 | — |
| 11-08.5c | x(1) | −0.04979 | — |
| 11-08.5d | x(−1) | −5.437 | — |
| 11-08.6a | X(j0) | 1 | s |
| 11-08.6b | X(j2) | 0.5 | s |
| 11-08.6c | X(1) | 1.333 | s |
| 11-08.7a | ω₀ | 3.606 | rad/s |
| 11-08.7b | ζ | 0.5547 | — |
| 11-08.7c | Q | 0.9014 | — |
| 11-08.7d | peak frequency | 2.236 | rad/s |
| 11-08.7e | peak magnitude | 1.083 | — |
| 11-08.7f | peak in decibels | 0.70 | dB |
| 11-08.8a | closed-loop DC gain | 9.999 | — |
| 11-08.8b | closed-loop pole | 100.0 | kHz |
| 11-08.8c | gain–bandwidth product | 1 | MHz |
| 11-08.8d | closed-loop pole, unrounded | 100.01 | kHz |
| 11-08.9a | vector length to −10 at ω = 10 | 14.14 | rad/s |
| 11-08.9b | vector length to −100 at ω = 10 | 100.5 | rad/s |
| 11-08.9c | angle of the −100 vector at ω = 10 | 5.71 | ° |
| 11-08.9d | magnitude at ω = 10 | 0.7036 | — |
| 11-08.9e | phase at ω = 10 | −50.71 | ° |
| 11-08.9f | vector length to −100 at ω = 100 | 141.4 | rad/s |
| 11-08.9g | angle of the −10 vector at ω = 100 | 84.29 | ° |
| 11-08.9h | magnitude at ω = 100 | 0.07036 | — |
| 11-08.9i | phase at ω = 100 | −129.29 | ° |
| 11-08.10a | phase at ω = 2 | −90 | ° |
| 11-08.10b | group delay at DC | 1 | s |
| 11-08.10c | group delay at ω = 2 | 0.5 | s |
| 11-08.10d | step response at 0⁺ | −1 | — |
| 11-08.10e | zero-crossing time | 0.3466 | s |
| 11-08.11a | complex pair real part | −0.5 | ω_c |
| 11-08.11b | complex pair ζ | 0.5 | — |
| 11-08.11c | gain at 2f_c | −18.13 | dB |
| 11-08.11d | order for 40 dB at 2f_c | 7 | — |
| 11-08.11e | order 7 attenuation at 2f_c | 42.1 | dB |
| 11-08.11f | order 6 attenuation at 2f_c | 36.1 | dB |
| 11-08.11g | lower bound on the order | 6.64 | — |
| 11-08.12a | DC gain | −0.5 | — |
| 11-08.12b | all-pass group delay at DC | 0.6667 | s |
| 11-08.12c | residual phase at ω = 3 | −90 | ° |
| 11-08.13a | zero at −6 dB | 10.65 | GHz |
| 11-08.13b | Nyquist gain at −6 dB | −2.47 | dB |
| 11-08.13c | boost at −6 dB | 3.53 | dB |
| 11-08.13d | smallest setting for 10 dB | −13 | dB |
| 11-08.13e | boost at −13 dB | 10.02 | dB |
| 11-08.13f | limiting Nyquist gain | −3.12 | dB |
| 11-08.13g | G at −6 dB | 0.5012 | — |
| 11-08.14a | Q | 25 | — |
| 11-08.14b | pole real part | −12.57 | 10⁶ s⁻¹ |
| 11-08.14c | envelope time constant | 79.58 | ns |
| 11-08.14d | cycles per e-fold decay | 7.958 | — |
| 11-08.14e | cycles at the damped frequency | 7.956 | — |
