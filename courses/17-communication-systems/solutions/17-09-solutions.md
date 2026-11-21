# Solutions 17-09 · Wireless Channels: Fading and Multipath

Problems: [17-09 problems](../problems/17-09-problems.md) · Chapter: [17-09](../chapters/17-09-wireless-channels.md). Every number below is recomputed by [verify_17_09.py](../verify/verify_17_09.py), several by independent routes (exact field sums, numerical integration, Monte Carlo).

---

## Solutions

### Solution 17-09.1

$20\log_{10}(4\pi d f/c)$: at 5.8 GHz and 1 km, **107.72** dB; at 60 GHz and 100 m, **108.01** dB. Ten times the frequency at a tenth of the distance gives almost the same loss, because $fd$ is nearly the same.

### Solution 17-09.2

Free-space loss at 28 GHz and 200 m: 107.41 dB. $P_r = 23 + 25 + 15 - 107.41$ = **−44.41** dBm, a strong signal: array gain more than pays for the frequency.

### Solution 17-09.3

With fixed effective areas, $P_r = P_tA_tA_r/(\lambda^2d^2)$, so $P_r \propto f^2$: ten times the frequency gives **+20.0** dB. Gain $G = 4\pi A/\lambda^2$: at 30 GHz ($\lambda$ = 9.99 mm), $4\pi \times 0.1/(9.993 \times 10^{-3})^2 = 12\,584$, **41.0** dBi (21.0 dBi at 3 GHz). The isotropic $20\log f$ loss is more than cancelled by the two antenna gains.

### Solution 17-09.4

$d_{BP} = 4h_th_r/\lambda = 4 \times 30 \times 1.5/0.3331$ = **540** m. At 5 km: $40\log_{10}5000 - 20\log_{10}30 - 20\log_{10}1.5 = 147.96 - 29.54 - 3.52$ = **114.9** dB (an exact two-ray field sum gives 114.94 dB). Free space: **105.5** dB. Beyond the breakpoint the ground reflection costs 9.4 dB at 5 km, and the gap widens by 20 dB per decade.

### Solution 17-09.5

At 1 km: $80 + 35\log_{10}10$ = **115** dB. Budget 125 dB: $d = 100 \times 10^{(125 - 80)/35}$ = **1931** m. Margin $8 \times 1.2816$ = 10.25 dB leaves 114.75 dB: $d = 100 \times 10^{34.75/35}$ = **984** m. A 10 dB margin halves the range at $n$ = 3.5.

### Solution 17-09.6

$d'_{BP} = 4 \times 9 \times 0.5 \times 28 \times 10^9/(3 \times 10^8)$ = **1680** m, so LOS uses PL1. $d_{3D} = \sqrt{50^2 + 8.5^2}$ = 50.72 m. LOS: $32.4 + 21\log_{10}50.72 + 20\log_{10}28$ = **97.15** dB. NLOS: $35.3\log_{10}50.72 + 22.4 + 21.3\log_{10}28$ = **113.42** dB (larger than LOS, so it is the NLOS value).

### Solution 17-09.7

Mean delay 0.5 μs, $\overline{\tau^2}$ = 0.5 μs², so $\tau_{rms} = \sqrt{0.5 - 0.25}$ = **0.5** μs. $H(f) = 1 + e^{-j2\pi f\tau}$, $|H| = 2|\cos(\pi f\tau)|$: nulls every $1/\tau$ = **1** MHz. Frequency correlation $|R_H(\Delta f)| = |\cos(\pi\Delta f\tau)|$ = 0.5 at $\Delta f = 1/(3\tau)$ = **333** kHz.

### Solution 17-09.8

$\Delta f = \sqrt{1/\rho^2 - 1}/(2\pi\tau_{rms})$. At ρ = 0.5: $\sqrt3/(2\pi \times 50\,\text{ns})$ = **5.51** MHz. At ρ = 0.9: $\sqrt{0.2346}/(2\pi \times 50\,\text{ns})$ = **1.54** MHz. A 20 MHz Wi-Fi channel is therefore frequency-selective indoors.

### Solution 17-09.9

Pedestrian: $v$ = 1.389 m/s, $f_D = 1.389 \times 5.8 \times 10^9/c$ = **26.9** Hz, $T_c = 0.242/f_D$ = **9.01** ms. Train: 83.3 m/s, $f_D$ = **723** Hz, $T_c$ = **0.335** ms.

### Solution 17-09.10

$\rho$ = 0.1 (−20 dB): $P(r < 0.1r_{rms}) = 1 - e^{-0.01}$ = **0.995** %. Crossing rate $\sqrt{2\pi} \times 50 \times 0.1 \times e^{-0.01}$ = **12.4** per second; average fade duration $(e^{0.01} - 1)/(\sqrt{2\pi} \times 50 \times 0.1)$ = **0.802** ms. Check: $12.4 \times 0.802 \times 10^{-3} = 0.00995$, the fraction of time below the level.

### Solution 17-09.11

$\mathbb E[r] = \int_0^\infty\frac{r^2}{\sigma^2}e^{-r^2/2\sigma^2}dr = \sigma\sqrt{\pi/2}$ (a half-Gaussian second moment), and $\mathbb E[r^2] = 2\sigma^2$, so $r_{rms} = \sigma\sqrt2$. Ratio $\sqrt{\pi/4}$ = **0.886**. The power is exponential with mean $\Omega$; its median solves $1 - e^{-x/\Omega} = 0.5$: $x = \Omega\ln2$, **−1.59** dB below the mean.

### Solution 17-09.12

$\bar P_b = \int_0^\infty\tfrac12e^{-\gamma}\frac{1}{\bar\gamma}e^{-\gamma/\bar\gamma}d\gamma = \frac{1}{2\bar\gamma}\cdot\frac{1}{1 + 1/\bar\gamma} = \frac{1}{2(1 + \bar\gamma)}$. At 30 dB ($\bar\gamma$ = 1000): DPSK **5.00e-4**; BPSK $\tfrac12(1 - \sqrt{1000/1001})$ = **2.50e-4**. In fading the 3 dB gap between them is the whole story: both fall as $1/\bar\gamma$. In AWGN at a BER of $10^{-5}$ the gap is only **0.75** dB (BPSK needs 9.59 dB; DPSK, from $\tfrac12e^{-\gamma} = 10^{-5}$, needs $10\log_{10}\ln(5 \times 10^4)$ = 10.34 dB).

### Solution 17-09.13

Threshold $x$ = 0.1 of the mean. One branch: $1 - e^{-0.1}$ = **0.0952**. Selection: both branches must be below, $(1 - e^{-0.1})^2$ = **0.00906**. MRC: $1 - e^{-0.1}(1.1)$ = **0.00468**, about half of selection's, and both fall as $x^2$ (diversity order 2).

### Solution 17-09.14

$v$ = 138.9 m/s: $f_D = 138.9 \times 3.5 \times 10^9/c$ = **1621** Hz. Nyquist sampling of a process bandlimited to $\pm f_D$ needs a spacing below $1/(2f_D)$ = **0.308** ms. A symbol lasts $0.5/14$ = 35.7 μs, so pilots at most every **8** symbols ($0.308/0.0357$ = 8.6). Practical designs add margin for noise and channel-estimation error, so pilots are placed more densely than this bound.

### Solution 17-09.15

(a) Rayleigh: $P(|h|^2 < 0.1) = 1 - e^{-0.1}$ = **9.52** %.

(b) $K = 10^{0.6}$ = 3.981. With $a = \sqrt{2K}$ = 2.822 and $b = \sqrt{2(K + 1)x} = \sqrt{2 \times 4.981 \times 0.1}$ = 0.998, the outage is $1 - Q_1(2.822, 0.998)$ = **1.65** %: the line-of-sight path cuts the outage by a factor of about 6.

(c) $(K + 1)e^{-K}x = 4.981 \times 0.01867 \times 0.1$ = **0.93** %, 44% low. The approximation replaces the density of $|h|^2$ on $[0, x]$ by its value at zero, but for a Rician channel that density rises steeply away from zero (it peaks near the line-of-sight power), so it is valid only for $x \ll 1/(K + 1)$, that is for deeper fades.

(d) At $x = 10^{-3}$: Rayleigh $1 - e^{-0.001}$ ≈ 0.1 %; Rician $1 - Q_1(2.822, 0.0998)$ = **0.0094** %, which now matches $(K + 1)e^{-K}x$ = 0.0093 % closely. Both curves fall one decade per 10 dB at deep fades: the Rician advantage is a constant factor, $e^{K}/(K + 1)$ ≈ 10.7, not a steeper slope.

### Solution 17-09.16

(a) Independence gives $f_{XY}(x, y) = \frac{1}{2\pi\sigma^2}e^{-(x^2 + y^2)/(2\sigma^2)}$. With $x = r\cos\theta$, $y = r\sin\theta$, the Jacobian is

$$
\left|\frac{\partial(x, y)}{\partial(r, \theta)}\right| = \left|\begin{matrix}\cos\theta & -r\sin\theta\\ \sin\theta & r\cos\theta\end{matrix}\right| = r ,
$$

so $f_{R\Theta}(r, \theta) = \frac{r}{2\pi\sigma^2}e^{-r^2/(2\sigma^2)}$ for $r \ge 0$, $0 \le \theta < 2\pi$. This is $\big[\frac{r}{\sigma^2}e^{-r^2/(2\sigma^2)}\big] \times \frac{1}{2\pi}$, a product of a function of $r$ alone and a constant in θ: θ is uniform on $[0, 2\pi)$ and independent of $r$.

(b) Integrating out θ gives $f_r(r) = \frac{r}{\sigma^2}e^{-r^2/(2\sigma^2)}$. For $s = r^2$, $f_s(s) = f_r(\sqrt s)\,\frac{1}{2\sqrt s} = \frac{1}{2\sigma^2}e^{-s/(2\sigma^2)}$: exponential with mean $2\sigma^2 = \Omega$.

(c) Mean: $\int_0^\infty r\,f_r\,dr = \sigma\sqrt{\pi/2}$ = **1.253**σ (a Gaussian integral). Median: $P(r < m) = 1 - e^{-m^2/(2\sigma^2)} = \tfrac12$ gives $m = \sigma\sqrt{2\ln2}$ = **1.177**σ. The mean exceeds the median because the density has a long upper tail.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-09.1a | loss at 5.8 GHz, 1 km | 107.72 | dB |
| 17-09.1b | loss at 60 GHz, 100 m | 108.01 | dB |
| 17-09.2a | received power | −44.41 | dBm |
| 17-09.3a | change from 3 to 30 GHz | 20.0 | dB |
| 17-09.3b | dish gain at 30 GHz | 41.0 | dBi |
| 17-09.4a | two-ray breakpoint | 540 | m |
| 17-09.4b | two-ray loss at 5 km | 114.9 | dB |
| 17-09.4c | free-space loss at 5 km | 105.5 | dB |
| 17-09.5a | loss at 1 km | 115 | dB |
| 17-09.5b | range for 125 dB | 1931 | m |
| 17-09.5c | range with 90% shadowing margin | 984 | m |
| 17-09.6a | breakpoint at 28 GHz | 1680 | m |
| 17-09.6b | LOS loss | 97.15 | dB |
| 17-09.6c | NLOS loss | 113.42 | dB |
| 17-09.7a | rms delay spread | 0.5 | μs |
| 17-09.7b | null spacing | 1 | MHz |
| 17-09.7c | 50% coherence bandwidth | 333 | kHz |
| 17-09.8a | coherence bandwidth at 0.5 | 5.51 | MHz |
| 17-09.8b | coherence bandwidth at 0.9 | 1.54 | MHz |
| 17-09.9a | pedestrian Doppler | 26.9 | Hz |
| 17-09.9b | pedestrian coherence time | 9.01 | ms |
| 17-09.9c | train Doppler | 723 | Hz |
| 17-09.9d | train coherence time | 0.335 | ms |
| 17-09.10a | probability below −20 dB | 0.995 | % |
| 17-09.10b | fades per second | 12.4 | 1/s |
| 17-09.10c | average fade duration | 0.802 | ms |
| 17-09.11a | mean/rms envelope | 0.886 | — |
| 17-09.11b | median power relative to mean | −1.59 | dB |
| 17-09.12a | DPSK at 30 dB | 5.00e-4 | — |
| 17-09.12b | BPSK at 30 dB | 2.50e-4 | — |
| 17-09.13a | single-branch outage | 0.0952 | — |
| 17-09.13b | selection-combining outage | 0.00906 | — |
| 17-09.13c | MRC outage | 0.00468 | — |
| 17-09.14a | Doppler at 500 km/h | 1621 | Hz |
| 17-09.14b | Nyquist pilot spacing | 0.308 | ms |
| 17-09.14c | symbols between pilots | 8 | — |
| 17-09.12c | BPSK-DPSK gap in AWGN at 1e-5 | 0.75 | dB |
| 17-09.15a | Rayleigh outage, 10 dB margin | 9.52 | % |
| 17-09.15b | Rician outage, K = 6 dB, 10 dB margin | 1.65 | % |
| 17-09.15c | small-x approximation at 10 dB | 0.93 | % |
| 17-09.15d | Rician outage at 30 dB | 0.0094 | % |
| 17-09.16a | mean envelope | 1.253 | σ |
| 17-09.16b | median envelope | 1.177 | σ |
