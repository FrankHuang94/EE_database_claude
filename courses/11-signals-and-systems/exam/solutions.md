# Course 11 · Final Exam Solutions (Signals and Systems)

Exam: [README.md](README.md). Every number below is recomputed by [verify_11_exam.py](../verify/verify_11_exam.py) by an independent route where one exists (numerical integration and convolution, iteration of the difference equations, root finding, simulation of the sampled and modulated signals).

**Grading.** Each [B] question is 8 points; give full credit to a correct method with arithmetic slips under 1%, and half credit for a correct setup with one conceptual slip (a wrong ROC side, a missing factor ½). Question 13 is graded on the derivation steps (4 points per part); Question 14 against its rubric.

---

## 1 · Periodicity and power

(a) The components have periods 10 ms and 6.667 ms (frequencies 100 and 150 Hz); the fundamental is their greatest common divisor, 50 Hz, so the period is **20** ms.
(b) Sinusoids at different frequencies are orthogonal (11-01), so powers add: $3^2/2 + 2^2/2$ = **6.5** V².

## 2 · System properties

(i) Linear; **time-varying** (a delayed input gives $t\,x(t - t_0)$, not $(t - t_0)x(t - t_0)$); causal and memoryless; **unstable** (a bounded input $x = 1$ gives the unbounded $y = t$).
(ii) Linear; **time-varying** (a decimator: shifting the input by one sample does not shift the output); **noncausal** ($y[1]$ needs $x[2]$); stable.
(iii) Linear and time-invariant at rest; causal; stable, since its impulse response $0.5^nu[n]$ is absolutely summable.
(d) $\lvert y\rvert \le B\sum_n0.5^n = 2B$: the bound is **2** times $B$, reached by $x = B$ for all time.

## 3 · Convolution

(a) For $0 \le t \le 2$, $y(t) = \int_0^te^{-(t-\tau)}d\tau = 1 - e^{-t}$, so $y(1)$ = **0.6321**. For $t > 2$, $y(t) = \int_0^2e^{-(t-\tau)}d\tau = e^{-(t-2)} - e^{-t}$, so $y(3)$ = **0.3181**.
(b) $\{1, 2, 3\} * \{1, -1\} = \{1, 2 - 1, 3 - 2, -3\}$ = **{1, 1, 1, −3}**: a first difference of the sequence padded with zeros.

## 4 · A difference equation

(a) $r^2 - 1.2r + 0.36 = (r - 0.6)^2$: a double root at **0.6**. The impulse response is $h[n] = (n + 1)0.6^nu[n]$ (check: $h[0] = 1$, $h[1] = 1.2$).
(b) $h[3] = 4 \times 0.216$ = **0.864**; $h[4] = 5 \times 0.1296$ = **0.648**.
(c) DC gain $1/(1 - 1.2 + 0.36)$ = **6.25**. Both roots are inside the unit circle: stable.

## 5 · A square wave's harmonics

(a) The ±1 square wave's odd harmonics have amplitudes $4/(\pi k)$: the third is **0.4244** V.
(b) Its power is 1 V²; the fundamental's is $(4/\pi)^2/2 = 8/\pi^2$ = **0.8106** of it.
(c) THD $= \sqrt{(1 - 8/\pi^2)/(8/\pi^2)} = \sqrt{\pi^2/8 - 1}$ = **48.34**%.

## 6 · A decaying exponential's spectrum

(a) $X(f) = 1/(1000 + j2\pi f)$, so $\lvert X\rvert^2$ halves at $2\pi f = 1000$: **159.2** Hz.
(b) $\int_0^\infty e^{-2000t}dt = 1/2000$ V²·s, which across 1 Ω is **0.5** mJ.
(c) By Parseval, the fraction below $f_c$ is $\frac{2}{\pi}\arctan(1)$ = **0.5**: exactly half the energy lies below the −3 dB frequency of a single pole.

## 7 · A four-point average

(a) $\lvert H\rvert = \lvert\sin(2\omega)/(4\sin(\omega/2))\rvert$; at π/4: $1/(4\sin(\pi/8))$ = **0.6533**.
(b) Zeros of $\sin(2\omega)$: ω = **0.5**π and **π**.
(c) Symmetric taps of length 4: **1.5** samples.

## 8 · An inverse Laplace transform

(a) Residues: at −1, $(-1 + 3)/(-1 + 2)$ = **2**; at −2, $(-2 + 3)/(-2 + 1)$ = **−1**. With σ > −1 both terms are right-sided: $x(t) = (2e^{-t} - e^{-2t})u(t)$.
(b) $x(1) = 2e^{-1} - e^{-2}$ = **0.6004**.
(c) Also −2 < σ < −1 (two-sided: $-2e^{-t}u(-t) - e^{-2t}u(t)$) and σ < −2 (left-sided). Only the given ROC, σ > −1, contains the $j\omega$ axis, so only the causal signal has a Fourier transform.

## 9 · Feedback and pole positions

(a) $H = K/(s^2 + 4s + K)$; with $K$ = 13 the poles are $-2 \pm j3$; ω₀ = $\sqrt{13}$ = **3.606** rad/s and ζ = $2/\sqrt{13}$ = **0.5547**.
(b) $e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$ = **12.31**%.
(c) $\zeta = 2/\sqrt K = 0.7071$ gives $K$ = **8**.

## 10 · A digital notch

(a) $\omega_0 = \pi/3$ is $f_s/6$ = **166.7** Hz. $a_1 = -2(0.95)\cos(\pi/3)$ = **−0.95** and $a_2 = 0.95^2$ = **0.9025**.
(b) The numerator $1 - z^{-1} + z^{-2}$ is 1 at DC and the denominator is $1 - 0.95 + 0.9025 = 0.9525$, so $K$ = **0.9525**.
(c) Width ≈ $2(1 - r)$ = 0.1 rad/sample, or $0.1 \times 1000/(2\pi)$ = **15.92** Hz. Margin $1 + 0.9025 - 0.95$ = **0.9525** > 0 and $\lvert a_2\rvert < 1$: stable.

## 11 · Sampling audio

(a) $\lvert 30 - 44.1\rvert$ = **14.1** kHz, inside the audio band.
(b) First alias frequency $44.1 - 20 = 24.1$ kHz, a ratio of 1.205. $n \ge \ln(10^6 - 1)/(2\ln1.205)$ = **37.04**, so **38**th order: impractical, which is why audio converters oversample.
(c) $-20\log_{10}(2\pi \times 20\,\text{kHz} \times 1\,\text{ns})$ = **78.0** dB.

## 12 · An AM link

(a) $\eta = (0.36/2)/(1 + 0.36/2)$ = **15.25**%.
(b) $RC \le \sqrt{1 - 0.36}/(0.6 \times 2\pi \times 3000)$ = **70.74** µs.
(c) $100 + 2 \times 10.7$ = **121.4** MHz.

## 13 · Derivations (rubric)

(a) *4 points.* The impulse train is periodic with period $T$; its Fourier coefficients are $\frac1T\int_{-T/2}^{T/2}\delta(t)e^{-j2\pi kf_st}dt = f_s$ (1 point), so $\sum_n\delta(t - nT) = f_s\sum_ke^{j2\pi kf_st}$ (1 point). Multiplying $x(t)$ by $e^{j2\pi kf_st}$ shifts its spectrum to $X(f - kf_s)$ (1 point); summing gives the result (1 point).
(b) *4 points.* BIBO stability ⇔ $\int\lvert h\rvert dt < \infty$ ⇔ σ = 0 lies in the ROC (1 point, the definition of the ROC as the region of absolute convergence). Causal ⇒ $h$ right-sided ⇒ ROC is a right half-plane, which for rational $H$ starts at the rightmost pole (1 point). That half-plane contains σ = 0 exactly when the rightmost pole has negative real part (1 point); conversely, if all poles are in the open left half-plane, every term $A_ke^{p_kt}u(t)$ is absolutely integrable (1 point).
(c) *4 points.* Complex pair: $\lvert p\rvert^2 = a_2$, so inside ⇔ $a_2 < 1$, and $P(\pm1) > 0$ automatically (1 point). Real pair: $P(1) = (1 - p_1)(1 - p_2)$, $P(-1) = (1 + p_1)(1 + p_2)$ (1 point); both inside ⇒ both positive and $\lvert p_1p_2\rvert < 1$; conversely a root at or beyond ±1 with $P(\pm1) > 0$ forces the other beyond too, contradicting $\lvert a_2\rvert < 1$ (1 point). $P(\pm1) > 0$ is $1 \pm a_1 + a_2 > 0$, i.e. $\lvert a_1\rvert < 1 + a_2$ (1 point).

## 14 · Diligence (rubric)

(a) *4 points.* 0.1 Hz at 250 SPS is $2\pi \times 0.1/250 = 0.002513$ rad/sample, so $1 - r = 0.001257$ and $r$ = **0.99874** (2 points). The transient decays as $r^n$, time constant $-1/\ln r$ = **795** samples, **3.18** s (2 points): every change in the hum's amplitude or phase (a cable moving, a person walking past equipment) leaves a 60 Hz residue for several seconds.
(b) *4 points.* 180 Hz appears at $\lvert 180 - 250\rvert$ = **70** Hz and 300 Hz at $300 - 250$ = **50** Hz (2 points). Neither is at 60 Hz, so the notch leaves both, now inside the ECG band, where no digital filter can separate them from the signal (2 points): the claim "removes all mains interference" fails without an analog anti-aliasing filter (and the 300 Hz alias at 50 Hz would also defeat a 50 Hz notch elsewhere).
(c) *4 points.* A causal IIR notch has nonzero group delay that rises sharply near the notch; "zero latency" is impossible, and the narrow notch also distorts low-frequency ECG content near 60 Hz through its phase (2 points). Questions: what analog filtering precedes the ADC and what is its attenuation at $f_s - f_B$; what is the notch's settling time after a hum transient and how was it validated; what group delay and phase distortion does the signal chain add, against the relevant ECG standards (2 points for good questions).

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X11.1a | fundamental period | 20 | ms |
| X11.1b | average power | 6.5 | V² |
| X11.2a | stability bound factor for (iii) | 2 | — |
| X11.3a | y(1) | 0.6321 | — |
| X11.3b | y(3) | 0.3181 | — |
| X11.3c | fourth sample of the DT convolution | −3 | — |
| X11.4a | repeated root | 0.6 | — |
| X11.4b | h[3] | 0.864 | — |
| X11.4c | h[4] | 0.648 | — |
| X11.4d | DC gain | 6.25 | — |
| X11.5a | third-harmonic amplitude | 0.4244 | V |
| X11.5b | fundamental's power fraction | 0.8106 | — |
| X11.5c | THD | 48.34 | % |
| X11.6a | half-power frequency | 159.2 | Hz |
| X11.6b | energy across 1 Ω | 0.5 | mJ |
| X11.6c | energy fraction below it | 0.5 | — |
| X11.7a | gain at π/4 | 0.6533 | — |
| X11.7b | first null | 0.5 | π rad/sample |
| X11.7c | group delay | 1.5 | samples |
| X11.8a | residue at −1 | 2 | — |
| X11.8b | residue at −2 | −1 | — |
| X11.8c | x(1) | 0.6004 | — |
| X11.9a | ω₀ | 3.606 | rad/s |
| X11.9b | ζ | 0.5547 | — |
| X11.9c | overshoot | 12.31 | % |
| X11.9d | K for ζ = 0.7071 | 8 | — |
| X11.10a | notch frequency | 166.7 | Hz |
| X11.10b | a₁ | −0.95 | — |
| X11.10c | a₂ | 0.9025 | — |
| X11.10d | normalizing gain | 0.9525 | — |
| X11.10e | notch width estimate | 15.92 | Hz |
| X11.10f | stability margin | 0.9525 | — |
| X11.11a | alias of 30 kHz | 14.1 | kHz |
| X11.11b | order bound | 37.04 | — |
| X11.11c | order | 38 | — |
| X11.11d | jitter-limited SNR | 78.0 | dB |
| X11.12a | sideband power fraction | 15.25 | % |
| X11.12b | maximum RC | 70.74 | µs |
| X11.12c | image frequency | 121.4 | MHz |
| X11.14a | pole radius | 0.99874 | — |
| X11.14b | time constant | 795 | samples |
| X11.14c | time constant | 3.18 | s |
| X11.14d | alias of 180 Hz | 70 | Hz |
| X11.14e | alias of 300 Hz | 50 | Hz |
