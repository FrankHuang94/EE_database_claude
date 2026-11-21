# Solutions 17-01 · Random Processes and Power Spectral Density

Problems: [17-01 problems](../problems/17-01-problems.md) · Chapter: [17-01](../chapters/17-01-random-processes-and-psd.md). Every number below is recomputed by [verify_17_01.py](../verify/verify_17_01.py): transforms and noise bandwidths by numerical integration, correlations by simulation, the PAM spectra by Welch estimates of simulated symbol streams, and the I/Q cross-correlation by down-converting simulated noise.

---

## Solutions

### Solution 17-01.1

The tone and the noise are independent and the tone has zero mean, so the cross terms vanish:

$$
R_X(\tau) = \tfrac12\cos(2\pi f_0\tau) + 0.01e^{-\lvert\tau\rvert/10\,\mu\text{s}}\ \text{V}^2 .
$$

Total power $R_X(0) = 0.5 + 0.01$ = **0.51** V², of which the tone is $0.5/0.51$ = **0.980**. $S_X(f)$ has two lines of 0.25 V² at ±1 kHz plus the Lorentzian $2 \times 0.01 \times 10^{-5}/(1 + (2\pi f \times 10^{-5})^2)$ V²/Hz, flat to its corner at $1/(2\pi \times 10\ \mu\text{s})$ = **15.9** kHz.

### Solution 17-01.2

One-sided: $G = (4 \times 10^{-9})^2$ = **1.6 × 10⁻¹⁷** V²/Hz; two-sided: $S = G/2$ = **8 × 10⁻¹⁸** V²/Hz. In 10 kHz to 1 MHz: $\sqrt{1.6 \times 10^{-17} \times 0.99 \times 10^6}$ = **3.98** µV rms (the same from the two-sided density over both the positive and negative bands).

### Solution 17-01.3

(a) $\mathbb{E}[X] = \mathbb{E}[A]\cos(2\pi f_0t) = 0$, but $R_X(t_1, t_2) = \sigma^2\cos(2\pi f_0t_1)\cos(2\pi f_0t_2)$ depends on the times themselves: the power $\sigma^2\cos^2(2\pi f_0t)$ varies with $t$. **Not WSS.**

(b) Mean 0. With $\mathbb{E}[AB] = 0$,

$$
R_X(t + \tau, t) = \sigma^2[\cos\omega(t + \tau)\cos\omega t + \sin\omega(t + \tau)\sin\omega t] = \sigma^2\cos(\omega\tau) ,
$$

which depends only on τ. **WSS.** The quadrature term fills in exactly the power the cosine lacks at each instant.

(c) Using $\cos a\cos b = \tfrac12[\cos(a - b) + \cos(a + b)]$ with $\omega = 2\pi f_0$,

$$
R_X(t + \tau, t) = \frac{\sigma^2}{2}\left[\cos\omega\tau + \cos(2\omega t + \omega\tau)\right] .
$$

The mean (zero) is trivially periodic, and the autocorrelation is periodic in $t$ with period $\pi/\omega = 1/(2f_0)$ = **0.5** ms, the period of $\cos(2\omega t)$: shifting both times by half a carrier cycle flips the sign of both cosines and leaves their product unchanged. So $X$ is **cyclostationary**, with period half the carrier period (the power $\sigma^2\cos^2\omega t$ peaks twice per cycle). Averaging over one period removes the $2\omega t$ term:

$$
\bar R_X(\tau) = \frac{\sigma^2}{2}\cos\omega\tau = \cos(2\pi \cdot 1000\,\tau)\ \text{V}^2 ,
$$

so the average power is $\bar R_X(0) = \sigma^2/2$ = **1** V², half of the 2 V² of the WSS process in (b), which has a second, quadrature component of equal power. Its spectrum is the transform of $\bar R_X$: $\tfrac{\sigma^2}{4}[\delta(f - f_0) + \delta(f + f_0)]$, the same line shape as (b) at half the height.

### Solution 17-01.4

(a) The transform of $e^{-a\lvert\tau\rvert}$ is $2a/(a^2 + 4\pi^2f^2)$; multiplying by the cosine shifts half of it to $\pm f_0$:

$$
S(f) = \frac{a}{a^2 + 4\pi^2(f - f_0)^2} + \frac{a}{a^2 + 4\pi^2(f + f_0)^2} > 0 .
$$

It is positive everywhere, so the function is a valid autocorrelation (narrowband noise centred on $f_0$, with bandwidth set by $a$).

(b) $S(f) = 2\int_0^1(1 - \tau^2)\cos(\omega\tau)\,d\tau = 4(\sin\omega - \omega\cos\omega)/\omega^3$ with $\omega = 2\pi f$. The numerator changes sign where $\tan\omega = \omega$, first at $\omega$ = 4.4934, so $S < 0$ for $f$ just above **0.715** Hz (until 1.230 Hz). The minimum is **−0.115** V²/Hz at 0.917 Hz. **Not valid**, although the function is even, peaks at zero and is smooth inside its support.

### Solution 17-01.5

$\tau_c = RC$ = **1.0** µs; $B_N = 1/(4RC)$ = **250** kHz; output rms $\sqrt{10^{-14} \times 2.5 \times 10^5}$ = **50.0** µV. Correlation $e^{-T_s/\tau_c} < 0.01$ needs $T_s > \tau_c\ln100$ = **4.61** µs.

### Solution 17-01.6

$B_N = \int_0^\infty df/(1 + (f/f_c)^4) = f_c\int_0^\infty dx/(1 + x^4) = f_c\pi/(2\sqrt2)$ = **1.111** $f_c$. A one-pole filter has $(\pi/2)f_c$ = **1.571** $f_c$. The steeper skirt admits **29.3**% less noise for the same −3 dB bandwidth.

### Solution 17-01.7

The sensor noise $V$ adds to the output, $Y = h * X + V$, and is independent of $X$, so $R_{VX} = 0$ and $S_{YX} = HS_X$, unchanged. At 1 kHz, $H = 1/(1 + j)$: $\lvert S_{YX}\rvert = 10^{-6}/\sqrt2$ = **7.07 × 10⁻⁷** V²/Hz, at a phase of **−45**°. The sensor noise only increases the variance of the cross-spectrum estimate, which averaging reduces.

### Solution 17-01.8

$R_X[0] = 1/(1 - 0.64)$ = **2.778**; $R_X[1] = aR_X[0]$ = **−2.222**. $S_X(e^{j0}) = 1/(1 + 0.8)^2$ = **0.309**; $S_X(e^{j\pi}) = 1/(1 - 0.8)^2$ = **25**. The negative coefficient makes successive samples alternate in sign on average: the power is concentrated near $\omega = \pi$, the highest frequencies.

### Solution 17-01.9

$T$ = 40 ps, so the first null is at **25** GHz. One-sided density near DC: $2A^2T = 2 \times 0.09 \times 4 \times 10^{-11}$ = **7.2 × 10⁻¹²** V²/Hz. Power below 12.5 GHz: $0.774 \times 0.09$ = **0.0696** V². Unipolar 0/0.6 V has $\mu_a$ = 0.3 V and $\sigma_a^2$ = 0.09 V². The only line is at DC (the others fall on the sinc's zeros) and carries $\mu_a^2/(\mu_a^2 + \sigma_a^2)$ = **0.5** of the power.

### Solution 17-01.10

$R(\tau) = N_0B\operatorname{sinc}(2B\tau)$ with $N_0/2 = 2 \times 10^{-17}$ and $B$ = 5 MHz: samples every $1/(2B)$ = **100** ns are uncorrelated, hence independent (Gaussian). Variance $N_0B = 4 \times 10^{-17} \times 5 \times 10^6$ = **2 × 10⁻¹⁰** V² (σ = 14.1 µV). $P(\lvert X\rvert > 3\sigma) = 2Q(3)$ = **0.00270**.

### Solution 17-01.11

The amplifier's one-sided density is $(5\ \text{nV})^2$ = $2.5 \times 10^{-17}$ V²/Hz, and its noise bandwidth is $(\pi/2) \times 50$ MHz = 78.5 MHz.

- **Unfiltered.** All $2.5 \times 10^{-17} \times 78.5 \times 10^6 = 1.96 \times 10^{-9}$ V² folds into the 5 MHz Nyquist band: **44.3** µV rms. Near DC the folded density is $T/(2\tau_c)$ times the original, with $\tau_c = 1/(2\pi \times 50\ \text{MHz})$ and $T$ = 100 ns ($a = e^{-T/\tau_c} \approx 2 \times 10^{-14}$ is negligible): **15.7** times, **11.96** dB.
- **With an ideal 5 MHz filter.** $2.5 \times 10^{-17}\int_0^{5\,\text{MHz}}df/(1 + (f/50\,\text{MHz})^2) = 2.5 \times 10^{-17} \times 50\ \text{MHz} \times \arctan0.1 = 1.25 \times 10^{-10}$ V²: **11.2** µV rms.

The anti-alias filter cuts the sampled noise by a factor of four in rms. The ADC's own resolution would be wasted without it.

### Solution 17-01.12

$P(f) = \int_0^T\sin(\pi t/T)e^{-j2\pi ft}dt$, which evaluates to

$$
\lvert P(f)\rvert = \frac{2T}{\pi}\left\lvert\frac{\cos(\pi fT)}{1 - 4f^2T^2}\right\rvert .
$$

At $fT = 1/2$ numerator and denominator vanish together (the limit is $T/2$), so the first null is at $fT$ = **1.5**, against 1 for NRZ: a wider main lobe. But the sidelobes fall as $1/f^4$ in power, because the pulse has no jumps. The fraction of power below $1/T$ is **0.970**, against **0.903** for NRZ. Both have symbol energy $T/2$ here (NRZ of amplitude $1/\sqrt2$). The half-sine's DC density, $\lvert P(0)\rvert^2/T = (2/\pi)^2T$ = **0.405** $T$, is lower than NRZ's 0.5 $T$, since its energy is spread wider.

### Solution 17-01.13

With the noise only above the carrier, $S_n(f + f_c)$ is $N_0/2$ on $0 < f < B$ and $S_n(f - f_c)$ is $N_0/2$ on $-B < f < 0$. So $S_{n_I}(f) = N_0/2$ for $\lvert f\rvert < B$: twice the bandwidth at half the density of the symmetric case, with power $N_0B$ = the bandpass power. The cross-spectrum is $j(N_0/2)$ on $(0, B)$ and $-j(N_0/2)$ on $(-B, 0)$, and transforming,

$$
R_{n_In_Q}(\tau) = -\frac{N_0}{2}\cdot\frac{1 - \cos(2\pi B\tau)}{\pi\tau} = -N_0B\,\frac{1 - \cos x}{x},\qquad x = 2\pi B\tau .
$$

It is zero at τ = 0, as it must be, and odd. The correlation coefficient $-(1 - \cos x)/x$ reaches its largest magnitude, **0.725**, at $x$ = 2.331, that is at $\tau = \pm$**0.371**$/B$. It is **negative** for $\tau > 0$: a tone above the carrier, $\cos(2\pi(f_c + \delta)t)$, gives $n_I = \cos2\pi\delta t$ and $n_Q = \sin2\pi\delta t$, so $n_Q$ lags $n_I$ by 90° ($n_Q(t) = n_I(t - 1/(4\delta))$). Then $\mathbb E[n_I(t + \tau)n_Q(t)] = -\tfrac12\sin(2\pi\delta\tau) < 0$ for small τ > 0. The simulation in the verify script confirms the sign.

### Solution 17-01.14

$R_a[0] = \mathbb{E}[a^2] = P(\text{bit} = 1)$ = **0.5**. Adjacent symbols are both nonzero with probability 1/4, and then they have opposite signs: $R_a[\pm1]$ = **−0.25**. For $\lvert m\rvert \ge 2$ the sign depends on the random number of marks between them and averages to zero. So $S_a(e^{j\theta}) = 0.5 - 0.5\cos\theta = \sin^2(\theta/2)$ and

$$
S_X(f) = \frac{\lvert P(f)\rvert^2}{T}\sin^2(\pi fT) = T\operatorname{sinc}^2(fT)\sin^2(\pi fT) .
$$

At DC it is **0**: AMI is DC-free, which is why it was used on transformer-coupled telephone lines (T1 carrier). The peak satisfies $\tan(\pi fT) = 2\pi fT$, at $fT$ = **0.371**, where $S_X$ = **0.525** $T$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-01.1a | total power | 0.51 | V² |
| 17-01.1b | tone fraction | 0.980 | — |
| 17-01.1c | noise corner | 15.9 | kHz |
| 17-01.2a | one-sided density | 1.6e-17 | V²/Hz |
| 17-01.2b | two-sided density | 8e-18 | V²/Hz |
| 17-01.2c | rms noise, 10 kHz–1 MHz | 3.98 | µV |
| 17-01.3a | shortest period of the cyclostationary process | 0.5 | ms |
| 17-01.3b | its average power | 1 | V² |
| 17-01.4a | first frequency with S < 0 | 0.715 | Hz |
| 17-01.4b | end of the negative region | 1.230 | Hz |
| 17-01.4c | minimum of S | −0.115 | V²/Hz |
| 17-01.5a | correlation time | 1.0 | µs |
| 17-01.5b | noise bandwidth | 250 | kHz |
| 17-01.5c | output rms | 50.0 | µV |
| 17-01.5d | minimum sampling interval | 4.61 | µs |
| 17-01.6a | two-pole noise bandwidth | 1.111 | × fc |
| 17-01.6b | one-pole noise bandwidth | 1.571 | × fc |
| 17-01.6c | noise reduction | 29.3 | % |
| 17-01.7a | cross-spectrum magnitude | 7.07e-7 | V²/Hz |
| 17-01.7b | cross-spectrum phase | −45 | ° |
| 17-01.8a | R[0] | 2.778 | — |
| 17-01.8b | R[1] | −2.222 | — |
| 17-01.8c | PSD at 0 | 0.309 | — |
| 17-01.8d | PSD at π | 25 | — |
| 17-01.9a | first null | 25 | GHz |
| 17-01.9b | one-sided density near DC | 7.2e-12 | V²/Hz |
| 17-01.9c | power below 12.5 GHz | 0.0696 | V² |
| 17-01.9d | line fraction, unipolar | 0.5 | — |
| 17-01.10a | independent-sample spacing | 100 | ns |
| 17-01.10b | sample variance | 2e-10 | V² |
| 17-01.10c | P(abs > 3σ) | 0.00270 | — |
| 17-01.11a | folded rms | 44.3 | µV |
| 17-01.11b | density ratio | 15.7 | — |
| 17-01.11c | density ratio | 11.96 | dB |
| 17-01.11d | filtered rms | 11.2 | µV |
| 17-01.12a | first null | 1.5 | × 1/T |
| 17-01.12b | half-sine power below 1/T | 0.970 | — |
| 17-01.12c | NRZ power below 1/T | 0.903 | — |
| 17-01.12d | half-sine DC density | 0.405 | × T |
| 17-01.13a | largest correlation magnitude | 0.725 | — |
| 17-01.13b | lag of the extremum | 0.371 | × 1/B |
| 17-01.14a | R_a[0] | 0.5 | — |
| 17-01.14b | R_a[1] | −0.25 | — |
| 17-01.14c | AMI peak frequency | 0.371 | × 1/T |
| 17-01.14d | AMI peak PSD | 0.525 | × T |
