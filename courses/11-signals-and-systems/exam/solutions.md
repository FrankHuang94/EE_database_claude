# Course 11 · Final Exam Solutions (Signals and Systems)

Exam: [README.md](README.md). Every number below is recomputed by [verify_11_exam.py](../verify/verify_11_exam.py) by an independent route where one exists (numerical integration and convolution, iteration of the difference equations, root finding, simulation of the sampled and modulated signals).

**Grading.** Each [B] question is 8 points; give full credit to a correct method with arithmetic slips under 1%, and half credit for a correct setup with one conceptual slip (a wrong ROC side, a missing factor ½). Question 13 is graded on the derivation steps (4 points per part); Question 14 against its rubric.

---

## 1 · Periodicity and power

(a) The components have periods 10 ms and 6.667 ms (frequencies 100 and 150 Hz); the fundamental is their greatest common divisor, 50 Hz, so the period is **20** ms.
(b) Sinusoids at different frequencies are orthogonal (11-01), so powers add: $3^2/2 + 2^2/2$ = **6.5** V².

## 2 · System properties

(a) (i) Linear; **time-varying** (a delayed input gives $t\,x(t - t_0)$, not $(t - t_0)x(t - t_0)$); causal and memoryless; **unstable** (a bounded input $x = 1$ gives the unbounded $y = t$).
(ii) Linear; **time-varying** (a decimator: shifting the input by one sample does not shift the output); **noncausal** ($y[1]$ needs $x[2]$); stable.
(iii) Linear and time-invariant at rest; causal; stable, since its impulse response $0.5^nu[n]$ is absolutely summable.
(b) $\lvert y\rvert \le B\sum_n0.5^n = 2B$: the bound is **2** times $B$, approached by $x = B$ applied for a long time (the output $2B(1 - 0.5^{n+1})$ tends to $2B$).

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

## 6 · Transforms by properties

(a) Write $y(t) = x(2(t - 1))$ with $x(t) = e^{-t}u(t)$. Scaling by 2: $x(2t) \leftrightarrow \tfrac12X(j\omega/2) = \tfrac12\cdot\frac{1}{1 + j\omega/2} = \frac{1}{2 + j\omega}$. Delaying by 1 s multiplies by $e^{-j\omega}$: $Y(j\omega) = e^{-j\omega}/(2 + j\omega)$. The delay changes only the phase, so $\lvert Y(j2)\rvert = 1/\lvert2 + j2\rvert = 1/\sqrt8$ = **0.3536**.
(b) Frequency differentiation, $t\,x(t) \leftrightarrow j\,dX/d\omega$: $j\frac{d}{d\omega}(1 + j\omega)^{-1} = j \cdot (-j)(1 + j\omega)^{-2} = 1/(1 + j\omega)^2$.
(c) In time: $\int_0^\infty t^2e^{-2t}dt = 2!/2^3$ = **0.25** (V²·s if $z$ is in volts). By Parseval: $\frac{1}{2\pi}\int_{-\infty}^{\infty}\frac{d\omega}{(1 + \omega^2)^2}$, and the integral is **1.571** ($\pi/2$, by $\omega = \tan\theta$: $\int\cos^2\theta\,d\theta$ over $(-\pi/2, \pi/2)$), giving $(\pi/2)/(2\pi)$ = **0.25**. The two agree.

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

## 10 · One formula, three sequences

(a) $X(z) = \frac{A}{1 - 0.8z^{-1}} + \frac{B}{1 + 1.25z^{-1}}$ with $A = \frac{1}{1 + 1.25/0.8} = \frac{1}{2.5625}$ = **0.3902** (exactly 16/41) and $B = \frac{1}{1 - 0.8/(-1.25)} = \frac{1}{1.64}$ = **0.6098** (25/41). Check: $A + B = 1 = X(\infty)$.
(b) Poles at radii 0.8 and 1.25 give three ROCs. $\lvert z\rvert > 1.25$: causal, growing as $1.25^n$, not summable. $0.8 < \lvert z\rvert < 1.25$: two-sided, and the only one whose ROC contains the unit circle, so the only absolutely summable one. $\lvert z\rvert < 0.8$: anticausal, growing as $0.8^n$ for $n \to -\infty$, not summable.
(c) In the ring, the pole at 0.8 is inside the ROC's inner circle (right-sided term) and the pole at −1.25 outside its outer circle (left-sided term): $x[n] = A(0.8)^nu[n] - B(-1.25)^nu[-n - 1]$. So $x[0] = A$ = **0.3902**, $x[2] = 0.3902 \times 0.64$ = **0.2498**, and $x[-1] = -B(-1.25)^{-1} = 0.6098 \times 0.8$ = **0.4878**.

## 11 · A sampled-data chain

(a) $\omega = 2\pi \times 1/8 = \pi/4$, and $H(e^{j\omega}) = \tfrac12(1 + e^{-j\omega}) = e^{-j\omega/2}\cos(\omega/2)$, so the gain is $\cos(\pi/8)$ = **0.9239**.
(b) The droop is $\operatorname{sinc}(f/f_s) = \operatorname{sinc}(1/8) = \sin(\pi/8)/(\pi/8)$ = **0.9745**. The 1 kHz output amplitude is $0.9239 \times 0.9745$ = **0.9003** V.
(c) The hold output contains copies of the DT spectrum at $kf_s \pm 1$ kHz; the first image is at $8 - 1$ = **7** kHz, carrying the same DT amplitude, weighted by $\operatorname{sinc}(7/8)$. Relative to the tone: $\operatorname{sinc}(7/8)/\operatorname{sinc}(1/8) = \frac{\sin(7\pi/8)/(7\pi/8)}{\sin(\pi/8)/(\pi/8)} = \frac17$, since $\sin(7\pi/8) = \sin(\pi/8)$: **−16.90** dB. A smoothing filter is needed.
(d) $9 - 8$ = **1** kHz: a 9 kHz input produces exactly the same samples as the 1 kHz tone, so it comes out at 1 kHz with the same gain, and no DT filter can separate the two. Only an analog filter before the sampler can.

## 12 · An AM link

(a) $\eta = (0.36/2)/(1 + 0.36/2)$ = **15.25**%.
(b) $RC \le \sqrt{1 - 0.36}/(0.6 \times 2\pi \times 3000)$ = **70.74** µs.
(c) $100 + 2 \times 10.7$ = **121.4** MHz.

## 13 · Derivations (rubric)

(a) *4 points.* The impulse train is periodic with period $T$; its Fourier coefficients are $\frac1T\int_{-T/2}^{T/2}\delta(t)e^{-j2\pi kf_st}dt = f_s$ (1 point), so $\sum_n\delta(t - nT) = f_s\sum_ke^{j2\pi kf_st}$ (1 point). Multiplying $x(t)$ by $e^{j2\pi kf_st}$ shifts its spectrum to $X(f - kf_s)$ (1 point); summing gives the result (1 point).
(b) *4 points.* BIBO stability ⇔ $\int\lvert h\rvert dt < \infty$ ⇔ σ = 0 lies in the ROC (1 point, the ROC as the region of absolute convergence). Causal ⇒ $h$ right-sided ⇒ ROC is a right half-plane, which for rational $H$ starts at the rightmost pole (1 point). That half-plane contains σ = 0 exactly when the rightmost pole has negative real part (1 point). Conversely, for a *proper* $H$, partial fractions give $h(t) = D\delta(t) + \sum_kA_kt^{m}e^{p_kt}u(t)$, with a constant $D$ (zero for strictly proper $H$) and powers $t^m$ for repeated poles; with every Re $p_k < 0$ each term is absolutely integrable, since $t^me^{-\alpha t}$ is integrable for α > 0 (1 point). "Proper" is needed because an improper $H$ contains derivatives: $H(s) = s$ has no poles at all, yet the bounded input $\sin(t^2)$ produces the unbounded output $2t\cos(t^2)$.
(c) *4 points.* Complex pair: $\lvert p\rvert^2 = a_2$, so inside ⇔ $a_2 < 1$, and $P(\pm1) > 0$ automatically (1 point). Real pair: $P(1) = (1 - p_1)(1 - p_2)$, $P(-1) = (1 + p_1)(1 + p_2)$ (1 point); both inside ⇒ both positive and $\lvert p_1p_2\rvert < 1$; conversely a root at or beyond ±1 with $P(\pm1) > 0$ forces the other beyond too, contradicting $\lvert a_2\rvert < 1$ (1 point). $P(\pm1) > 0$ is $1 \pm a_1 + a_2 > 0$, i.e. $\lvert a_1\rvert < 1 + a_2$ (1 point).

## 14 · Diligence (rubric)

(a) *4 points.* 0.1 Hz at 250 SPS is $2\pi \times 0.1/250 = 0.002513$ rad/sample, so $1 - r = 0.001257$ and $r$ = **0.99874** (2 points). The transient decays as $r^n$, time constant $-1/\ln r$ = **795** samples, **3.18** s (2 points): every change in the hum's amplitude or phase (a cable moving, a person walking past equipment) leaves a 60 Hz residue for several seconds.
(b) *4 points.* 180 Hz appears at $\lvert 180 - 250\rvert$ = **70** Hz and 300 Hz at $300 - 250$ = **50** Hz (2 points). Neither is at 60 Hz, so the notch leaves both, now inside the ECG band, where no digital filter can separate them from the signal (2 points). The claim "removes all mains interference" fails without an analog anti-aliasing filter. Even with one, the 120 Hz second harmonic (below the 125 Hz Nyquist frequency) passes straight through a 60 Hz notch: "all mains interference" needs notches at the harmonics too.
(c) *4 points.* Away from 60 Hz the notch's group delay is close to zero, so "zero latency" is nearly true for most of the band; the claim hides two real costs (2 points). Near 60 Hz the group delay spikes, to the order of the transient time constant of (a), about 795 samples, so ECG components close to 60 Hz (the sharp QRS complex has some) are delayed and phase-shifted relative to the rest. And after any change in the hum, the notch needs several seconds, set by $1/(1 - r)$, to settle, during which mains interference leaks through. Questions: what analog filtering precedes the ADC and what is its attenuation at $f_s - f_B$; what is the notch's settling time after a hum transient and how was it validated; what group delay and phase distortion does the signal chain add, against the relevant ECG standards (2 points for good questions).

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
| X11.6a | magnitude of Y at 2 rad/s | 0.3536 | — |
| X11.6b | energy of z, in time | 0.25 | — |
| X11.6c | integral of 1/(1 + ω²)² | 1.571 | — |
| X11.6d | energy of z, by Parseval | 0.25 | — |
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
| X11.10a | residue A | 0.3902 | — |
| X11.10b | residue B | 0.6098 | — |
| X11.10c | x[0] | 0.3902 | — |
| X11.10d | x[2] | 0.2498 | — |
| X11.10e | x[−1] | 0.4878 | — |
| X11.11a | DT filter gain | 0.9239 | — |
| X11.11b | hold droop at 1 kHz | 0.9745 | — |
| X11.11c | 1 kHz output amplitude | 0.9003 | V |
| X11.11d | first image frequency | 7 | kHz |
| X11.11e | image relative to the tone | −16.90 | dB |
| X11.11f | output frequency of a 9 kHz input | 1 | kHz |
| X11.12a | sideband power fraction | 15.25 | % |
| X11.12b | maximum RC | 70.74 | µs |
| X11.12c | image frequency | 121.4 | MHz |
| X11.14a | pole radius | 0.99874 | — |
| X11.14b | time constant | 795 | samples |
| X11.14c | time constant | 3.18 | s |
| X11.14d | alias of 180 Hz | 70 | Hz |
| X11.14e | alias of 300 Hz | 50 | Hz |
