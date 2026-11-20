# Equation Sheet · 16 Digital Signal Processing

The relations to know cold from Course 16, each with its conditions and the chapter that derives it.

Conventions:

- $\omega$ is in rad/sample, $\omega = 2\pi f/f_s$; Nyquist is $\omega = \pi$; $W_N = e^{-j2\pi/N}$;
- filter order $M$ (length $M + 1$ for an FIR filter); $\delta_p$, $\delta_s$ are the passband and stopband ripples, $A_s = -20\log_{10}\delta_s$, and peak-to-peak passband ripple is $20\log_{10}((1 + \delta_p)/(1 - \delta_p))$;
- an $N$-bit quantizer covers ±1 with step $\Delta = 2^{1-N}$ ("LSB");
- symbol reuse, as in the chapters: $N$ is the DFT length, a filter's analog order, a bit count or the number of CIC stages, as each row says; $D$ is the discrimination in 16-07 and a window's transition constant in 16-06; $M$ is also a decimation factor and $L$ an interpolation factor or loading factor; $K$ is the CORDIC gain.

## Discrete-time signals and systems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Aliasing: $f$ and $f + mf_s$ give the same samples; a real tone appears at $\lvert f - mf_s\rvert$ folded into $[0, f_s/2]$ | Ideal sampling, no anti-alias filter | [16-01](../../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md) |
| $N$-point moving average: $\lvert H\rvert = \lvert\sin(N\omega/2)/(N\sin(\omega/2))\rvert$; nulls at $mf_s/N$; delay $(N - 1)/2$; noise variance gain $1/N$ | White input noise | [16-01](../../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md) |
| EMA $y[n] = (1 - \alpha)y[n - 1] + \alpha x[n]$: time constant $\approx 1/\alpha - 1/2$ samples; noise gain $\alpha/(2 - \alpha)$ | $0 < \alpha \le 1$ | [16-01](../../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md) |
| Stability (BIBO) $\Leftrightarrow \sum\lvert h[n]\rvert < \infty$ $\Leftrightarrow$ all poles inside the unit circle (causal) | Rational $H(z)$ | [16-01](../../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md) |
| Sum of $N$ terms needs $\lceil\log_2N\rceil$ extra accumulator bits | Worst case | [16-01](../../courses/16-digital-signal-processing/chapters/16-01-discrete-time-systems-review.md) |

## DTFT, z-transform and pole–zero design

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $X(e^{j\omega}) = \sum x[n]e^{-j\omega n}$, periodic in $2\pi$; $X(z) = \sum x[n]z^{-n}$ with ROC; DTFT = $X(z)$ on $\lvert z\rvert = 1$ | ROC must contain the unit circle | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |
| $\lvert H(e^{j\omega})\rvert = \lvert g\rvert\prod\lvert e^{j\omega} - z_i\rvert/\prod\lvert e^{j\omega} - p_i\rvert$ (vector picture) |  | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |
| Pole at radius $r$: $\Delta\omega_{3\,\text{dB}} \approx 2(1 - r)$, $\Delta f \approx (1 - r)f_s/\pi$; $\tau_s = -1/\ln r \approx 1/(1 - r)$ samples; width × time constant ≈ 2 | $r$ near 1 | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |
| Notch: zeros $e^{\pm j\omega_0}$, poles $re^{\pm j\omega_0}$: $(1 - 2\cos\omega_0z^{-1} + z^{-2})/(1 - 2r\cos\omega_0z^{-1} + r^2z^{-2})$; scale by $1/H(1)$ |  | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |
| Group delay $\tau_g = -d\phi/d\omega$; a pole at its own angle adds $\rho/(1 - \rho)$ samples; symmetric FIR of length $N$: $(N - 1)/2$ |  | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |
| All-pass $(z^{-1} - a)/(1 - az^{-1})$: $\lvert H\rvert = 1$; delay $(1 + a)/(1 - a)$ at DC | $\lvert a\rvert < 1$ | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |
| Reflecting a zero to $1/z_i^*$ keeps $\lvert H\rvert$ (up to a constant): minimum phase has all zeros inside |  | [16-02](../../courses/16-digital-signal-processing/chapters/16-02-dtft-and-z-transform-for-dsp.md) |

## The DFT

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $X[k] = \sum_{n=0}^{N-1}x[n]W_N^{kn}$, $x[n] = \frac1N\sum X[k]W_N^{-kn}$; samples of the DTFT at $\omega_k = 2\pi k/N$ |  | [16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md) |
| Bin spacing $f_s/N$; on-bin tone of amplitude $A$: $\lvert X[k_0]\rvert = AN/2$; real input: $X[N - k] = X[k]^*$ |  | [16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md) |
| Circular shift ↔ $W_N^{km}$; circular convolution ↔ product; Parseval $\sum\lvert x\rvert^2 = \frac1N\sum\lvert X\rvert^2$ |  | [16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md) |
| Linear = circular convolution when $N \ge L + M - 1$; overlap-save keeps $N - M + 1$ outputs per block | $M$-tap filter | [16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md) |
| FFT convolution cost $4[N\log_2N + N]/(N - M + 1)$ real multiplies per output; crossover near 44 taps | Simple cost model | [16-03](../../courses/16-digital-signal-processing/chapters/16-03-the-dft.md) |

## The FFT

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Radix-2 DIT: $X[k] = G[k] + W_N^kH[k]$, $X[k + N/2] = G[k] - W_N^kH[k]$ ($G$, $H$ = DFTs of even and odd samples) | $N$ a power of 2 | [16-04](../../courses/16-digital-signal-processing/chapters/16-04-the-fft.md) |
| $\log_2N$ stages, $\frac N2\log_2N$ butterflies (complex multiplies), $N\log_2N$ complex adds; saving $2N/\log_2N$ over $N^2$ |  | [16-04](../../courses/16-digital-signal-processing/chapters/16-04-the-fft.md) |
| Non-trivial twiddle multiplications: $\frac N2\log_2N - \frac{3N}2 + 2$; radix-4: $\frac{3N}8\log_2N$ | Excluding $W^0$, $-j$ | [16-04](../../courses/16-digital-signal-processing/chapters/16-04-the-fft.md) |
| R2SDF pipeline: $\log_2N$ butterflies, $\log_2N - 2$ general multipliers, $N - 1$ delay words, one sample per clock | Streaming | [16-04](../../courses/16-digital-signal-processing/chapters/16-04-the-fft.md) |
| Word growth up to $\log_2N$ bits ($1 + \sqrt2$ per stage in one component); scaling by 1/2 per stage gives $X/N$ | Fixed point | [16-04](../../courses/16-digital-signal-processing/chapters/16-04-the-fft.md) |

## Spectral analysis and ADC testing

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\text{CG} = \frac1N\sum w$; $\text{ENBW} = N\sum w^2/(\sum w)^2$ bins; scalloping $\lvert W(e^{j\pi/N})\rvert/\lvert W(1)\rvert$ | Window $w[n]$ | [16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) |
| Rectangular: ENBW 1, −13.3 dB sidelobes, −3.92 dB scalloping; Hann: CG 0.5, ENBW 1.5, −31.5 dB, −1.42 dB; 4-term Blackman–Harris: ENBW 2.0, −92 dB |  | [16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) |
| Floor below tone $= \text{SNR} + 10\log_{10}(N/(2\,\text{ENBW}))$; processing gain $10\log_{10}(N/2)$ | White noise | [16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) |
| Coherent test: $f_{in} = k f_s/N$ with $\gcd(k, N) = 1$ (odd $k$ for $N = 2^m$) | No window needed | [16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) |
| Ideal SNR $6.02N + 1.76$ dB ($N$ bits); $\text{ENOB} = (\text{SINAD} - 1.76)/6.02$; at $-x$ dBFS add $x$ dB to SINAD to refer it to full scale | Full-scale sine | [16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) |
| Periodogram bin: standard deviation = mean; averaging $K$ segments divides it by $\sqrt K$ | Welch | [16-05](../../courses/16-digital-signal-processing/chapters/16-05-spectral-analysis-and-windowing.md) |

## FIR filter design

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Linear phase: $h[n] = \pm h[M - n]$, $H = e^{-j\omega M/2}A(\omega)$ (times $j$ if antisymmetric); delay $M/2$ samples | Types I–IV | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Type II (symmetric, $M$ odd): $A(\pi) = 0$; type III: zeros at 0 and $\pi$; type IV: zero at 0 | Forced zeros | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Ideal low-pass $h_d[n] = \sin(\omega_c(n - M/2))/(\pi(n - M/2))$; Gibbs overshoot 8.95% at any length; gain 0.5 at $\omega_c$ | Truncation | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Window method: $\delta_p = \delta_s$; errors rectangular −21, Hann −44, Hamming ≈ −53, Blackman −75 dB; transition $\approx 2\pi D/M$, $D$ ≈ 0.9, 3.1, 3.3, 5.6 |  | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Kaiser: $\beta = 0.1102(A - 8.7)$ for $A > 50$; $0.5842(A - 21)^{0.4} + 0.07886(A - 21)$ for $21 \le A \le 50$; $M = (A - 8)/(2.285\Delta\omega)$ | $A = -20\log_{10}\min(\delta_p, \delta_s)$ | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Equiripple order $M \approx (-10\log_{10}(\delta_p\delta_s) - 13)/(2.324\Delta\omega)$; weight $W = \delta_p/\delta_s$ in the stopband | Parks–McClellan | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Alternation: the optimum type I filter's weighted error has at least $L + 2$ alternating extrema, $L = M/2$ | Chebyshev minimax | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |
| Multipliers with folding: $\lceil(M + 1)/2\rceil$ per output | Symmetric taps | [16-06](../../courses/16-digital-signal-processing/chapters/16-06-fir-filter-design.md) |

## IIR filter design

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Discrimination $D = (10^{A_s/10} - 1)/(10^{A_p/10} - 1)$ | Edges in dB | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |
| Butterworth: $N \ge \log_{10}D/(2\log_{10}(\Omega_s/\Omega_p))$; −3.01 dB at $\Omega_c$; poles equally spaced on $\lvert s\rvert = \Omega_c$; $20N$ dB/decade | Maximally flat | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |
| Chebyshev I: $N \ge \operatorname{arccosh}\sqrt D/\operatorname{arccosh}(\Omega_s/\Omega_p)$; poles $\Omega_p(-\sinh a\sin u_k + j\cosh a\cos u_k)$, $u_k = (2k - 1)\pi/(2N)$, $a = \frac1N\operatorname{arcsinh}(1/\varepsilon)$ | Equiripple passband | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |
| Elliptic: $N \ge K(k)K'(k_1)/(K(k_1)K'(k))$, $k = \Omega_p/\Omega_s$, $k_1 = 1/\sqrt D$; round up | Equiripple both bands | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |
| Bilinear: $s = 2f_s(1 - z^{-1})/(1 + z^{-1})$; $\Omega = 2f_s\tan(\omega/2)$; prewarp every band edge | No aliasing, warped axis | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |
| Impulse invariance $h[n] = Th_a(nT)$: pole $s_k \to e^{s_kT}$; $1/(s + a) \to T/(1 - e^{-aT}z^{-1})$ | Aliases; low-pass only | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |
| Biquad cost: 5 multiplications; 3 with zeros on the circle and $b_0 = b_2 = 1$ | Cascade of SOS | [16-07](../../courses/16-digital-signal-processing/chapters/16-07-iir-filter-design.md) |

## Filter structures

| Relation | Conditions / notes | Chapter |
|---|---|---|
| DF I: $2N$ delays; DF II: $N$ delays (internal state $x/A$); both $2N + 1$ multipliers for order $N$ |  | [16-08](../../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md) |
| Transposed FIR: critical path one multiplier + one adder at any length; direct form: one multiplier + (taps − 1) adders as a chain, or $\lceil\log_2(\text{taps})\rceil$ adder levels as a tree |  | [16-08](../../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md) |
| Pole sensitivity $\partial p_i/\partial a_k = -p_i^{N-k}/\prod_{j\ne i}(p_i - p_j)$; biquad angle sensitivity $1/(2\rho\sin\theta)$ | Clustered poles are fragile | [16-08](../../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md) |
| Lattice step-down: $k_N = a_N$, $a^{(N-1)}_i = (a_i - k_Na_{N-i})/(1 - k_N^2)$; biquad: $k_2 = a_2$, $k_1 = a_1/(1 + a_2)$; stable iff all $\lvert k_m\rvert < 1$ |  | [16-08](../../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md) |
| Order the sections: pair each pole with its nearest zeros; scale with $L_\infty$ or $L_2$ norms at every internal node | Cascade design | [16-08](../../courses/16-digital-signal-processing/chapters/16-08-filter-structures.md) |

## Multirate DSP

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\downarrow M$: $Y(e^{j\omega}) = \frac1M\sum_{k=0}^{M-1}X(e^{j(\omega - 2\pi k)/M})$; $\uparrow L$: $X(e^{j\omega L})$, images need a filter with gain $L$ |  | [16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md) |
| Noble identities: $H(z^M)$ then $\downarrow M$ = $\downarrow M$ then $H(z)$; $\uparrow L$ then $H(z^L)$ = $H(z)$ then $\uparrow L$ |  | [16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md) |
| Polyphase $H(z) = \sum_{p=0}^{M-1}z^{-p}E_p(z^M)$, $e_p[n] = h[nM + p]$; saves a factor $M$ (or $L$) |  | [16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md) |
| Rational $L/M$: one filter with cutoff $\min(\pi/L, \pi/M)$; 44.1 → 48 kHz is 160/147 |  | [16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md) |
| Half-band: middle tap 1/2, every other tap 0; $4K + 3$ taps with $K + 1$ folded multipliers | Decimate or interpolate by 2 | [16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md) |
| CIC $H(z) = \bigl((1 - z^{-R})/(1 - z^{-1})\bigr)^N$: $\lvert H\rvert = \lvert\sin(\pi fR/f_s)/\sin(\pi f/f_s)\rvert^N$; DC gain $R^N$; register growth $N\log_2R$ bits; wrap-around arithmetic | $N$ stages, decimation by $R$ | [16-09](../../courses/16-digital-signal-processing/chapters/16-09-multirate-dsp.md) |

## Quantization and fixed point

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Rounding error uniform on $[-\Delta/2, \Delta/2]$, white: power $\Delta^2/12$ | Busy signal | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |
| SQNR (full-scale sine) $= 6.02N + 1.76$ dB; Gaussian at loading $L$ = full scale/$\sigma$: $6.02N + 4.77 - 20\log_{10}L$ before clipping |  | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |
| Q$I$.$F$ ($I$ integer bits including the sign): step $2^{-F}$, range $[-2^{I-1}, 2^{I-1} - \Delta]$; Q1.15 step $3.05 \times 10^{-5}$ | Two's complement | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |
| Noise gain from a rounding point: $\sum g[n]^2$; first-order $1/(1 - a^2)$ | White rounding noise | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |
| TPDF dither ±1 LSB: total error power $\Delta^2/4$ (+4.8 dB); the error's first two moments become independent of the signal |  | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |
| Dead band of $y = Q(ay[n - 1])$: $\lvert k\rvert \le 1/(2(1 - \lvert a\rvert))$ LSB | Rounding | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |
| Recursive filters must saturate (wrap-around sustains overflow limit cycles); FIR and CIC integrators may wrap |  | [16-10](../../courses/16-digital-signal-processing/chapters/16-10-quantization-and-fixed-point.md) |

## DSP hardware

| Relation | Conditions / notes | Chapter |
|---|---|---|
| MAC: product $b_x + b_c$ bits; accumulator + $\lceil\log_2N\rceil$ guard bits | $N$-term sum | [16-11](../../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md) |
| Units $= \lceil(\text{mults per output} \times f_s)/f_{\text{clk}}\rceil$; folding trades clock for units |  | [16-11](../../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md) |
| Iteration bound $T_\infty = \max_\ell T_\ell/D_\ell$ (loop time over loop registers); look-ahead by $M$: $y[n] = a^My[n - M] + \sum_{i<M}a^ix[n - i]$ divides it by $M$ | Recursive loops | [16-11](../../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md) |
| CSD: no two adjacent non-zero digits; adders = non-zero digits − 1 | Constant multipliers | [16-11](../../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md) |
| Energy at 45 nm: 8-bit mult 0.2 pJ, 32-bit mult 3.1 pJ, 32-bit add 0.1 pJ, 64-bit read of an 8 KB cache 10 pJ, instruction ≈ 70 pJ, DRAM 1.3–2.6 nJ | R-208 | [16-11](../../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md) |
| CORDIC: $x_{i+1} = x_i - d_iy_i2^{-i}$, $y_{i+1} = y_i + d_ix_i2^{-i}$, $z_{i+1} = z_i - d_i\arctan2^{-i}$; gain $K = \prod\sqrt{1 + 2^{-2i}} \to 1.64676$; range ±99.88°; residual after $n$ iterations $\lvert z_n\rvert \le \arctan2^{-(n-1)} < 2^{1-n}$ | Rotation $d_i = \operatorname{sign}z_i$, $(x_0, y_0) = (1/K, 0)$ → $(\cos\theta, \sin\theta)$; vectoring $d_i = -\operatorname{sign}y_i$, $z_0 = 0$, $x_0 > 0$ → $x_n = K\sqrt{x_0^2 + y_0^2}$, $z_n = \arctan(y_0/x_0)$ | [16-11](../../courses/16-digital-signal-processing/chapters/16-11-dsp-hardware-architectures.md) |
