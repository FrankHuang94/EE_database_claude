# Equation Sheet · 11 Signals and Systems

The relations to know cold from Course 11, each with its conditions and the chapter that derives it.

Conventions:

- CT frequency in hertz $f$ (or rad/s ω where marked); DT frequency ω in rad/sample, with $\omega = 2\pi f/f_s$ for sampled signals;
- $X(f) = \int x(t)e^{-j2\pi ft}dt$, $X(j\omega) = \int x(t)e^{-j\omega t}dt$, $X(e^{j\omega}) = \sum x[n]e^{-j\omega n}$, $X(s)$ and $X(z)$ bilateral with their ROCs;
- $\operatorname{sinc}(u) = \sin(\pi u)/(\pi u)$; systems are at rest unless stated.

## Signals and systems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Energy $E = \int\lvert x\rvert^2dt$; power $P = \lim\frac{1}{2T}\int_{-T}^{T}\lvert x\rvert^2dt$; sinusoid $A^2/2$ | Powers of different frequencies add | [11-01](../../courses/11-signals-and-systems/chapters/11-01-signals-classification-and-operations.md) |
| DT $e^{j\omega n}$ periodic iff $\omega/2\pi$ rational; $\omega$ and $\omega + 2\pi$ identical | Frequency modulo 2π | [11-01](../../courses/11-signals-and-systems/chapters/11-01-signals-classification-and-operations.md) |
| $\delta(at) = \delta(t)/\lvert a\rvert$; $x(t)\delta(t - t_0) = x(t_0)\delta(t - t_0)$ | Sifting | [11-01](../../courses/11-signals-and-systems/chapters/11-01-signals-classification-and-operations.md) |
| Linear = additive + homogeneous; TI: shift in gives the same shift out | Test with the substitution rule | [11-02](../../courses/11-signals-and-systems/chapters/11-02-system-properties.md) |
| First-order recursion $y = ay[n-1] + x$: $\lvert y\rvert \le B/(1 - \lvert a\rvert)$ | $\lvert a\rvert < 1$ | [11-02](../../courses/11-signals-and-systems/chapters/11-02-system-properties.md) |

## Convolution and LTI systems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $y = x * h$: $\sum_kx[k]h[n - k]$, $\int x(\tau)h(t - \tau)d\tau$ | LTI; $h$ the impulse response | [11-03](../../courses/11-signals-and-systems/chapters/11-03-convolution.md) |
| Lengths add ($L_x + L_h - 1$); areas multiply; step response $=$ running sum of $h$ | Support and area rules | [11-03](../../courses/11-signals-and-systems/chapters/11-03-convolution.md) |
| BIBO stable $\iff \sum\lvert h\rvert < \infty$ ($\int\lvert h\rvert < \infty$) | Worst-case gain is $\sum\lvert h\rvert$ | [11-03](../../courses/11-signals-and-systems/chapters/11-03-convolution.md) |
| Difference equation roots $r_k$: $h[n] = \sum A_kr_k^n$; stable iff $\lvert r_k\rvert < 1$ | Causal, at rest | [11-04](../../courses/11-signals-and-systems/chapters/11-04-lti-systems-and-differential-equations.md) |
| Resonator poles $re^{\pm j\theta}$: $h[n] = r^n\sin((n + 1)\theta)/\sin\theta$ | $a_1 = -2r\cos\theta$, $a_2 = r^2$ | [11-04](../../courses/11-signals-and-systems/chapters/11-04-lti-systems-and-differential-equations.md) |
| Eigenfunctions: $e^{st} \to H(s)e^{st}$, $z^n \to H(z)z^n$ | $s$, $z$ in the ROC | [11-04](../../courses/11-signals-and-systems/chapters/11-04-lti-systems-and-differential-equations.md) |

## Fourier series and transforms

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $c_k = \frac1T\int_Tx(t)e^{-jk\omega_0t}dt$, $x = \sum c_ke^{jk\omega_0t}$ | Periodic, period $T$ | [11-05](../../courses/11-signals-and-systems/chapters/11-05-fourier-series.md) |
| Square wave ±1: odd harmonics $4/(\pi k)$; Gibbs overshoot 8.95% of the jump (peak 1.179) | Does not shrink with more terms | [11-05](../../courses/11-signals-and-systems/chapters/11-05-fourier-series.md) |
| Parseval: $P = \sum\lvert c_k\rvert^2$; THD $= \sqrt{\sum_{k\ge2}\lvert c_k\rvert^2}/\lvert c_1\rvert$ | RMS adds in quadrature | [11-05](../../courses/11-signals-and-systems/chapters/11-05-fourier-series.md) |
| $e^{-at}u(t) \leftrightarrow 1/(a + j\omega)$; rect of width $\tau$ $\leftrightarrow \tau\operatorname{sinc}(f\tau)$; Gaussian ↔ Gaussian | $a > 0$ | [11-06](../../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md) |
| Shift $e^{-j2\pi ft_0}$; modulation $x\cos(2\pi f_ct) \leftrightarrow \frac12[X(f - f_c) + X(f + f_c)]$; convolution ↔ product | Property table | [11-06](../../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md) |
| Energy $\int\lvert x\rvert^2dt = \int\lvert X(f)\rvert^2df$; group delay $-d\angle H/d\omega$ | Parseval | [11-06](../../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md) |
| Rise time ≈ 0.35/bandwidth (10–90%, −3 dB); cascades add in quadrature (approx.) | Single pole: $\ln 9/2\pi \approx 0.350$ | [11-06](../../courses/11-signals-and-systems/chapters/11-06-continuous-time-fourier-transform.md) |
| DTFT periodic in 2π; $a^nu[n] \leftrightarrow 1/(1 - ae^{-j\omega})$; $L$-boxcar → Dirichlet kernel, nulls at $2\pi k/L$ | $\lvert a\rvert < 1$ | [11-07](../../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md) |
| Symmetric FIR of $N$ taps: linear phase, delay $(N - 1)/2$ samples | Constant group delay | [11-07](../../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md) |
| Resolution $\Delta f \approx 1/T_{obs}$ (rectangular), ≈ 2× with Hamming; zero-padding does not help | Spectral analysis | [11-07](../../courses/11-signals-and-systems/chapters/11-07-discrete-time-fourier-transform.md) |

## Laplace and z-transforms

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $e^{-at}u(t) \leftrightarrow 1/(s + a)$, σ > −Re a; $-e^{-at}u(-t)$ same formula, σ < −Re a | The ROC is part of the answer | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| ROC: vertical strip, no poles inside; right-sided → right half-plane; FT exists iff $j\omega$ axis in ROC | Rational $X$: bounded by poles | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| Causal and stable rational $H$ $\iff$ all poles with Re < 0 | Proper $H$ | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| Feedback $H = G/(1 + GK)$; poles at $1 + GK = 0$ | Negative feedback | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| Second order: radius ω₀, ζ = cos θ, $Q = 1/(2\zeta)$; −3 dB bandwidth $2\alpha = \omega_0/Q$; gain $Q$ at ω₀ | Poles $-\alpha \pm j\omega_d$ | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| Second-order all-pole step response: overshoot $e^{-\pi\zeta/\sqrt{1 - \zeta^2}}$ | $0 < \zeta < 1$ | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| $\lvert H(j\omega)\rvert = \lvert K\rvert\prod\lvert j\omega - z_i\rvert/\prod\lvert j\omega - p_k\rvert$ | Geometric evaluation | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| All-pass $(a - s)/(a + s)$: delay $2a/(a^2 + \omega^2)$; RHP zero → no stable causal inverse | Minimum phase | [11-08](../../courses/11-signals-and-systems/chapters/11-08-laplace-transform-and-system-functions.md) |
| $a^nu[n] \leftrightarrow 1/(1 - az^{-1})$, $\lvert z\rvert > \lvert a\rvert$; left-sided twin inside | ROC is a ring | [11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md) |
| Causal and stable $\iff$ poles inside the unit circle; biquad: $\lvert a_2\rvert < 1$, $\lvert a_1\rvert < 1 + a_2$ | $1 + a_1z^{-1} + a_2z^{-2}$ | [11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md) |
| Pole at radius $r$ near 1: bandwidth ≈ $2(1 - r)$ rad/sample, time constant ≈ $1/(1 - r)$ samples | Resonators and notches | [11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md) |
| $z = e^{sT}$ (sampling, impulse invariance); bilinear $s = \frac2T\frac{1 - z^{-1}}{1 + z^{-1}}$, $\Omega = \frac2T\tan\frac\omega2$ | Warping; prewarp one frequency | [11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md) |
| Unilateral shift: $x[n - 1] \leftrightarrow z^{-1}X + x[-1]$ | Initial conditions | [11-09](../../courses/11-signals-and-systems/chapters/11-09-z-transform.md) |

## Sampling and modulation

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $X_s(f) = f_s\sum_kX(f - kf_s)$; recover if $f_s > 2f_M$ | Sampling theorem | [11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| Alias of $f_0$: $\lvert f_0 - kf_s\rvert \le f_s/2$ | Phase flips from reversed zones | [11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| Anti-aliasing: attenuation at $f_s - f_B$; Butterworth $n \ge \ln(10^{A/10} - 1)/(2\ln[(f_s - f_B)/f_c])$ | Oversampling relaxes it | [11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| Sinc interpolation $x(t) = \sum x[n]\operatorname{sinc}((t - nT)/T)$; ZOH $\operatorname{sinc}(f/f_s)$, −3.92 dB at $f_s/2$, delay $T/2$ | Reconstruction | [11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| Ideal ADC SNR $6.02N + 1.76$ dB; oversampling +$10\log_{10}\text{OSR}$; jitter SNR $-20\log_{10}(2\pi f_0\sigma_t)$ | Full-scale sine | [11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| Band-pass sampling $2f_H/n \le f_s \le 2f_L/(n - 1)$, $1 \le n \le \lfloor f_H/B\rfloor$ | Odd $n$ upright | [11-10](../../courses/11-signals-and-systems/chapters/11-10-sampling-aliasing-reconstruction.md) |
| DSB-SC bandwidth $2W$; coherent output ∝ cos φ; AM efficiency $m^2P_x/(1 + m^2P_x)$ | Modulation | [11-11](../../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md) |
| Envelope detector $1/f_c \ll RC \le \sqrt{1 - m^2}/(m\omega_m)$; image $f_{RF} + 2f_{IF}$ (high-side LO) | Receivers | [11-11](../../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md) |
| Shannon capacity $C = B\log_2(1 + \text{SNR})$ | AWGN channel | [11-11](../../courses/11-signals-and-systems/chapters/11-11-modulation-and-filtering-applications.md) |
