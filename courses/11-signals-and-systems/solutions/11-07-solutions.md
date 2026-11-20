# Solutions 11-07 · The Discrete-Time Fourier Transform

Problems: [11-07 problems](../problems/11-07-problems.md) · Chapter: [11-07](../chapters/11-07-discrete-time-fourier-transform.md). Every number below is recomputed by [verify_11_07.py](../verify/verify_11_07.py), which sums the DTFT definition on fine frequency grids.

---

## Solutions

### Solution 11-07.1

$X = 1 + 2e^{-j\omega} + e^{-j2\omega} = e^{-j\omega}(e^{j\omega} + 2 + e^{-j\omega}) = e^{-j\omega}(2 + 2\cos\omega)$: a one-sample delay times a real, nonnegative function. Magnitudes: **4** at DC, **2** at π/2, **0** at π. A symmetric sequence, so linear phase with a delay of 1 sample.

### Solution 11-07.2

(a) $2\pi \times 1/48$ = **0.04167**π rad/sample.

(b) $f_s/2$ = **24** kHz.

(c) $\omega = 2\pi \times 30/48 = 1.25\pi$, which is the same as $1.25\pi - 2\pi = -0.75\pi$ on the circle, and for a real cosine the same as $+0.75\pi$: it appears at $0.75\pi$, which is **18** kHz $= 48 - 30$ kHz. The samples cannot distinguish 30 kHz from 18 kHz: aliasing (11-10).

### Solution 11-07.3

At −0.3π: the conjugate, magnitude **2** and phase **+40**°. At 1.7π = −0.3π + 2π: the same as at −0.3π (2, +40°). At 2.3π = 0.3π + 2π: the same as at 0.3π (2, −40°).

### Solution 11-07.4

$X = 1/(1 + 0.5e^{-j\omega})$. At DC: $1/1.5$ = **0.6667**. At π: $1/(1 - 0.5)$ = **2**. The sequence alternates in sign, so most of its energy is at the fastest frequency: high-pass, the alternation property applied to $0.5^n$.

### Solution 11-07.5

$\sum_n0.5^{\lvert n\rvert}e^{-j\omega n} = 1 + \sum_{n\ge1}0.5^n(e^{-j\omega n} + e^{j\omega n})$. Using $\sum_{n\ge1}(ae^{\pm j\omega})^n = ae^{\pm j\omega}/(1 - ae^{\pm j\omega})$ and combining over the common denominator $1 - 2a\cos\omega + a^2$ gives $(1 - a^2)/(1 - 2a\cos\omega + a^2) = 0.75/(1.25 - \cos\omega)$ for $a = 0.5$. At DC: **3**; at π: **0.3333**. It is real because the sequence is real and even: every $e^{-j\omega n}$ pairs with $e^{j\omega n}$ into a cosine.

### Solution 11-07.6

$h[n] = \frac{1}{2\pi}\left[\int_{-\pi/2}^{-\pi/4} + \int_{\pi/4}^{\pi/2}\right]e^{j\omega n}d\omega = \frac{\sin(\pi n/2) - \sin(\pi n/4)}{\pi n}$, the difference of two ideal low-pass filters. $h[0] = (\pi/2 - \pi/4)/\pi$ = **0.25** (the passband's share of the circle); $h[1] = (1 - \sin(\pi/4))/\pi$ = **0.09323**.

### Solution 11-07.7

(a) $\tfrac18(1 + 3e^{-j\omega} + 3e^{-j2\omega} + e^{-j3\omega}) = \tfrac18(1 + e^{-j\omega})^3 = \left[e^{-j\omega/2}\cos(\omega/2)\right]^3$, using $1 + e^{-j\omega} = 2e^{-j\omega/2}\cos(\omega/2)$.

(b) Group delay **1.5** samples (symmetric, 4 taps). Gains: **1** at DC, $\cos^3(\pi/4)$ = **0.3536** at π/2, **0** at π. Binomial filters are cascades of two-point averages: three of them here.

### Solution 11-07.8

(a) $\omega_0 = 2\pi \times 60/500 = 0.24\pi$. Zeros at $e^{\pm j\omega_0}$ give $(1 - e^{j\omega_0}z^{-1})(1 - e^{-j\omega_0}z^{-1}) = 1 - 2\cos\omega_0z^{-1} + z^{-2}$, with $\cos\omega_0$ = **0.7290**.

(b) The DC gain is $2 - 2\cos\omega_0$ = **0.5421**; dividing the taps by it normalizes the filter.

(c) The response is $e^{-j\omega}(2\cos\omega - 2\cos\omega_0)/0.5421$. At 50 Hz ($\omega = 0.2\pi$): **0.2953**, deep attenuation of a frequency it should pass. At 120 Hz: **2.458**, amplification. A three-tap FIR notch is far too wide: zeros alone cannot make a narrow notch. A practical notch puts poles just inside the circle next to the zeros (an IIR notch), so the response recovers to 1 quickly away from 60 Hz (11-09).

### Solution 11-07.9

(a) The output is $\sum_kh[k]x[n - k]$, a sum of independent terms, so its variance is $\sigma^2\sum h[k]^2 = \sigma^2 \times 5 \times (1/5)^2$, a factor of **0.2**: averaging $L$ samples divides white-noise variance by $L$.

(b) White noise has a flat spectrum, so the output variance is $\sigma^2\frac{1}{2\pi}\int_{-\pi}^{\pi}\lvert H\rvert^2d\omega$, which by Parseval equals $\sigma^2\sum h^2$: the same 0.2.

### Solution 11-07.10

(a) Spacing 10 Hz, so about $1/10$ Hz = **0.1** s.

(b) About twice as long, **0.2** s: the price of the Hamming window's lower sidelobes is a wider main lobe.

### Solution 11-07.11

Searching odd lengths: **75** taps is the first with a 10–90% transition of at most 0.05π (it achieves **0.0493**π). Its stopband, for $\omega \ge 0.3\pi$, is at most **−55.8** dB. The transition width of a windowed design shrinks in proportion to $1/N$, so halving it would need about 150 taps.

### Solution 11-07.12

(a) $y[n] = \cos(0.6\pi \cdot 2n) = \cos(1.2\pi n)$, and $1.2\pi - 2\pi = -0.8\pi$, so $y = \cos(0.8\pi n)$: frequency **0.8**π.

(b) Downsampling by 2 stretches the spectrum by 2, so content above $\pi/2$ moves beyond π and wraps around the circle: aliasing. Before downsampling by $M$, a designer must low-pass filter to $\pi/M$ (a decimation filter, like the ADS1292R's sinc³); 11-10 and Course 16 develop this.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-07.1a | magnitude at DC | 4 | — |
| 11-07.1b | magnitude at π/2 | 2 | — |
| 11-07.1c | magnitude at π | 0 | — |
| 11-07.2a | ω for 1 kHz | 0.04167 | π rad/sample |
| 11-07.2b | frequency at π | 24 | kHz |
| 11-07.2c | apparent frequency of 30 kHz | 18 | kHz |
| 11-07.3a | magnitude at −0.3π | 2 | — |
| 11-07.3b | phase at −0.3π | 40 | ° |
| 11-07.4a | magnitude at DC | 0.6667 | — |
| 11-07.4b | magnitude at π | 2 | — |
| 11-07.5a | value at DC | 3 | — |
| 11-07.5b | value at π | 0.3333 | — |
| 11-07.6a | h[0] | 0.25 | — |
| 11-07.6b | h[1] | 0.09323 | — |
| 11-07.7a | group delay | 1.5 | samples |
| 11-07.7b | gain at DC | 1 | — |
| 11-07.7c | gain at π/2 | 0.3536 | — |
| 11-07.7d | gain at π | 0 | — |
| 11-07.8a | cos ω_0 | 0.7290 | — |
| 11-07.8b | unnormalized DC gain | 0.5421 | — |
| 11-07.8c | gain at 50 Hz | 0.2953 | — |
| 11-07.8d | gain at 120 Hz | 2.458 | — |
| 11-07.9a | variance factor | 0.2 | — |
| 11-07.10a | record length, rectangular | 0.1 | s |
| 11-07.10b | record length, Hamming | 0.2 | s |
| 11-07.11a | taps | 75 | — |
| 11-07.11b | transition achieved | 0.0493 | π rad/sample |
| 11-07.11c | stopband depth | −55.8 | dB |
| 11-07.12a | frequency after downsampling | 0.8 | π rad/sample |
