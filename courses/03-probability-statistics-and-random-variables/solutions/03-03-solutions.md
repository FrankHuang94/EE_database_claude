# Solutions 03-03 · Expectation, Variance and Functions of Random Variables

Problems: [03-03 problems](../problems/03-03-problems.md) · Chapter: [03-03](../chapters/03-03-expectation-and-functions-of-rvs.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_03_03.py](../verify/verify_03_03.py).

---

## Solutions

### Solution 03-03.1

$\mathbb{E}[X] = 0(0.5) + 1(0.3) + 2(0.15) + 3(0.05) = $ **0.75**.
$\mathbb{E}[X^2] = 0.3 + 4(0.15) + 9(0.05) = $ **1.35**.
$\operatorname{Var}(X) = 1.35 - 0.75^2 = $ **0.7875**, so $\sigma_X = $ **0.8874** retransmissions.

### Solution 03-03.2

(a) $\mathbb{E}[X] = \int_0^2x\cdot\tfrac38x^2dx = \tfrac38\cdot\tfrac{16}{4} = $ **1.5**. $\mathbb{E}[X^2] = \tfrac38\cdot\tfrac{32}{5} = $ **2.4**. $\operatorname{Var}(X) = 2.4 - 2.25 = $ **0.15**, $\sigma_X = $ **0.3873**.

(b) By linearity, $\mathbb{E}[Y] = 3(1.5) - 2 = $ **2.5**; by the scaling rule, $\operatorname{Var}(Y) = 9(0.15) = $ **1.35**; and $\mathbb{E}[Y^2] = \operatorname{Var}(Y) + (\mathbb{E}[Y])^2 = 1.35 + 6.25 = $ **7.6**.

### Solution 03-03.3

(a) The median $m$ solves $e^{-m/1000} = 1/2$: $m = 1000\ln2 = $ **693.1 h**. The density $e^{-t/1000}/1000$ is largest at $t = 0$, so the mode is **0**.

(b) Maximize $f_Y(y) \propto \exp[-(\ln y)^2/(2s^2)]/y$. Its logarithm is $-(\ln y)^2/(2s^2) - \ln y$; the derivative with respect to $\ln y$ is $-\ln y/s^2 - 1 = 0$, so $\ln y = -s^2$ and the mode is $e^{-s^2} = e^{-0.4771} = $ **0.6206**.

(c) Both distributions are skewed right, so mode < median < mean: 0 < 693.1 h < 1000 h, and 0.6206 < 1 < 1.269. A "typical" value should be the median (half the parts are better, half worse) and should say so; the mean is the right number for totals over many parts (fleet failures, array leakage).

### Solution 03-03.4

(a) Let $I_{ij}$ indicate that devices $i$ and $j$ collide. $P(I_{ij} = 1) = 1/N$ (whatever $i$ drew, $j$ matches it with probability $1/N$). The number of colliding pairs is $\sum_{i<j}I_{ij}$, so its expectation is $\binom k2/N$, even though the indicators are dependent.

(b) 302 devices, 16-bit IDs: $45{,}451/65{,}536 = $ **0.6935**. 10,000 devices, 32-bit IDs: $49{,}995{,}000/2^{32} = $ **0.01164**.

(c) With $N$ the number of colliding pairs, Markov gives $P(N \ge 1) \le \mathbb{E}[N]$: at most 0.6935 and 0.01164. The exact values, 0.5007 and 0.01157, respect both bounds. The bound is tight when collisions are rare (the second case) and loose when several are likely.

### Solution 03-03.5

(a) The number of attempts is geometric with $q = 0.98$. $\mathbb{E}[K] = 1/0.98 = $ **1.0204**, $\operatorname{Var}(K) = 0.02/0.98^2 = $ **0.02082**, $\sigma_K = $ **0.1443**.

(b) $1/q \le 1.5$ requires $q \ge 2/3$, so the failure probability must be at most **0.3333**.

### Solution 03-03.6

(a) $\sigma = \sqrt{100} = $ **10**.

(b) A deviation of 20 is $k = 2$ standard deviations, so Chebyshev gives $P \le 1/4 = $ **0.25**.

(c) Exactly, $P(N \le 80) + P(N \ge 120) = 0.02265 + 0.02823 = $ **0.05088**. The Gaussian approximation $2Q(2) = $ **0.04550** is close; Chebyshev, which must hold for every distribution, is five times too pessimistic. The Poisson's right tail is a little heavier than its left (it is skewed right), so the two exact tails differ.

### Solution 03-03.7

(a) The rate is $10^{-6}$ per hour, so the mean is $10^6$ h $= $ **114.1 years**, and for an exponential the standard deviation equals the mean: **114.1 years**.

(b) Median $= \ln2\times114.1 = $ **79.07 years**.

(c) $P(T > \text{MTTF}) = e^{-1} = $ **0.3679**: almost two-thirds of parts fail before the MTTF.

### Solution 03-03.8

(a) $\int_0^\infty e^{-rt}dt = 1/r = $ **100,000 h**.

(b) $\int_0^\infty(2e^{-rt} - e^{-2rt})dt = 2/r - 1/(2r) = $ **150,000 h**.

(c) $\int_0^\infty(3e^{-2rt} - 2e^{-3rt})dt = 3/(2r) - 2/(3r) = 5/(6r) = $ **83,333 h**, less than a single part.

(d) At $t = 10{,}000$ h ($rt = 0.1$): single part $e^{-0.1} = $ **0.9048**; TMR $3e^{-0.2} - 2e^{-0.3} = $ **0.9746**. TMR is far better over short missions, where it masks any single failure, but once one part has failed the system needs both survivors, which is worse than needing one. The curves cross where $R = 1/2$, at $rt = \ln2$, or **69,315 h**. MTTF averages over the whole life and hides this: choose redundancy by the mission time and repair interval, not by MTTF.

### Solution 03-03.9

$I = 10B$ A, where $B$ is Bernoulli with $p = 0.25$.

(a) $\mathbb{E}[I] = 10\times0.25 = $ **2.5 A**.

(b) $\mathbb{E}[I^2] = 100\times0.25 = 25$ A², so $I_{\text{rms}} = $ **5 A**, twice the average.

(c) The AC part has variance $25 - 2.5^2 = 18.75$ A², so the ripple RMS is **4.330 A**. Pulsed loads stress input capacitors with ripple currents far above the average current.

### Solution 03-03.10

The sinusoid's mean square is $(10\text{ mV})^2/2 = 5\times10^{-5}$ V² and the noise's is $10^{-6}$ V². Independent and zero-mean, so the powers add.

(a) $\sqrt{5.1\times10^{-5}} = $ **7.141 mV** rms.

(b) $5.1\times10^{-5}/50 = 1.02\times10^{-6}$ W, which is **−29.91 dBm**.

(c) $5\times10^{-5}/10^{-6} = 50$, or **16.99 dB**.

### Solution 03-03.11

(a) For uniform noise on $[-a, a]$: $\mathbb{E}[|V|] = a/2$ and the RMS is $a/\sqrt3$, so the meter reads $1.1107\times(a/2)/(a/\sqrt3) - 1 = $ **−3.809%**. A triangle wave sampled at a random time is exactly this uniform variable, which is why the 01-07 triangle result is the same. For Gaussian noise, $1.1107\times0.7979 - 1 = $ **−11.38%** (−1.049 dB, Example 03-03.4).

(b) Clipping occurs when $|X| > 3\sigma$, a fraction $2Q(3) = $ **0.2700%** of the time. The clipped power is $2[(1 + 9)Q(3) - 3\phi(3)]\sigma^2 = $ **4.069×10⁻⁴**σ², so the reading falls by $\sqrt{1 - 4.069\times10^{-4}}$, a bias of **−0.02035%**. A crest-factor rating of 3 is ample for Gaussian noise; signals with rarer, higher peaks (OFDM measured over long captures, pulsed loads) need more.

### Solution 03-03.12

(a) For $t \ge 0$, $P(T > t) = P(-\ln U > rt) = P(U < e^{-rt}) = e^{-rt}$: the exponential survival function.

(b) $g(u) = u^2$ is increasing on $[0, 1]$ with inverse $u = \sqrt y$ and $g'(u) = 2\sqrt y$, so $f_Y(y) = 1/(2\sqrt y)$ on $(0, 1]$. From the density, $\mathbb{E}[Y] = \int_0^1y/(2\sqrt y)\,dy = \int_0^1\tfrac12\sqrt y\,dy = 1/3$; directly, $\mathbb{E}[U^2] = \int_0^1u^2du = 1/3$. Both give **0.3333**, as the expectation rule promises.

(c) $P = -\bar P\ln U$ is exponential with mean $\bar P$ by (a), so $R = \sqrt{-\bar P\ln U}$ is Rayleigh (Problem 03-03.13).

### Solution 03-03.13

(a) $R = \sqrt P$ is increasing, $P = R^2$, $dP/dR = 2R$: $f_R(r) = f_P(r^2)\cdot2r = (2r/\bar P)e^{-r^2/\bar P}$ for $r \ge 0$.

(b) $\mathbb{E}[R] = \int_0^\infty r\cdot(2r/\bar P)e^{-r^2/\bar P}dr$. With $r = \sqrt{\bar P}\,u/\sqrt2$, this becomes $\sqrt{\bar P/2}\int_0^\infty u^2e^{-u^2/2}du = \sqrt{\bar P/2}\cdot\sqrt{2\pi}/2 = \sqrt{\pi\bar P}/2$, using $\int_0^\infty u^2e^{-u^2/2}du = \tfrac12\sqrt{2\pi}$ (half of the Gaussian second moment). So $\mathbb{E}[R] = $ **0.8862**$\sqrt{\bar P}$. The median solves $e^{-m^2/\bar P} = 1/2$: $m = \sqrt{\bar P\ln2} = $ **0.8326**$\sqrt{\bar P}$.

(c) $P(R > 2\mathbb{E}[R]) = \exp(-4\cdot\pi\bar P/4/\bar P) = e^{-\pi} = $ **0.04321**.

(d) $(\mathbb{E}[R])^2/\bar P = \pi/4$, which is **−1.049 dB**: the same factor as the average-responding meter on Gaussian noise, by a different route.

### Solution 03-03.14

(a) With $T$ in kelvin and $E_a/k = 0.7/8.617333\times10^{-5} = $ **8123** K:

$$
\frac{r(358.15)}{r(338.15)} = \exp\Big[8123\Big(\frac{1}{338.15} - \frac{1}{358.15}\Big)\Big] = 3.825, \qquad \frac{r(318.15)}{r(338.15)} = 0.2209 .
$$

So the hot half runs at **3.825** times and the cold half at **0.2209** times the 65 °C rate.

(b) The average is $(3.825 + 0.2209)/2 = $ **2.023** times the 65 °C rate: Jensen's inequality, with a factor of 2 at stake.

(c) The hot half contributes $3.825/(3.825 + 0.2209) = $ **0.9454** of failures, about 95%. Reliability is governed by the hottest periods, so thermal budgets must use time-at-temperature profiles, not averages.

### Solution 03-03.15

(a) Take σ = 1. The error on the upper tail is $Z - k$ for $Z > k$. Expand $(z - k)^2 = z^2 - 2kz + k^2$ and integrate against φ from $k$ to ∞:

- $\int_k^\infty\phi\,dz = Q(k)$;
- $\int_k^\infty z\phi\,dz = \phi(k)$, because $\phi'(z) = -z\phi(z)$;
- $\int_k^\infty z^2\phi\,dz$: by parts with $u = z$, $dv = z\phi\,dz$, $v = -\phi$: $[-z\phi]_k^\infty + \int_k^\infty\phi\,dz = k\phi(k) + Q(k)$.

So the upper tail gives $k\phi + Q - 2k\phi + k^2Q = (1 + k^2)Q(k) - k\phi(k)$, and the lower tail the same by symmetry: $D_{\text{clip}} = 2[(1 + k^2)Q(k) - k\phi(k)]\sigma^2$.

(b) With granular noise $k^2/(3\cdot4^{10})$ and $\text{SNR} = 1/(\text{granular} + D_{\text{clip}})$:

| $k$ | Granular-only SNR | Clipping-only SNR | Total SNR | Dominant |
|---|---|---|---|---|
| 3 | 55.43 dB | 33.91 dB | **33.88 dB** | clipping |
| 4 | 52.94 dB | 52.09 dB | **49.48 dB** | both, about equally |
| 5 | 51.00 dB | 74.12 dB | **50.98 dB** | granular |

(c) Maximizing numerically gives $k = $ **4.494** and SNR **51.56 dB**, against **51.92 dB** from granular noise alone at that $k$. At the optimum, clipping costs only about 0.4 dB, and the remaining loss relative to a full-scale sine (**61.97 dB**) is the price of headroom for a peaky signal.

### Solution 03-03.16

(a) $\mathbb{E}[(P - c)^+] = \int_c^\infty(p - c)\tfrac{1}{\bar P}e^{-p/\bar P}dp$. Substitute $u = p - c$: $e^{-c/\bar P}\int_0^\infty u\tfrac{1}{\bar P}e^{-u/\bar P}du = \bar P\,e^{-c/\bar P}$, since the last integral is the mean of an exponential.

(b) and (c), with $x = 10^{\text{back-off}/10}$ and $\bar\eta = (\pi/4)/(\sqrt x\cdot\sqrt\pi/2)$:

| Back-off | Clipping probability $e^{-x}$ | Clipped power | Class-B efficiency |
|---|---|---|---|
| 6 dB | **0.01867** | **−17.29 dB** | **44.42%** |
| 8 dB | **1.819×10⁻³** | **−27.40 dB** | **35.28%** |
| 10 dB | **4.540×10⁻⁵** | **−43.43 dB** | **28.02%** |

(d) −30 dBc requires $e^{-x} \le 10^{-3}$, so $x \ge \ln1000 = 6.908$, a back-off of at least **8.393 dB** with efficiency **33.72%**. Choose a little more, say 8.5 dB, for margin. Crest-factor reduction (clipping and filtering in the digital domain under control), digital predistortion (linearizing the amplifier so it can run nearer saturation), and envelope tracking or Doherty architectures (raising efficiency at back-off) recover part of the loss. The clipped-power figure here is a simple proxy; real standards specify error-vector magnitude and adjacent-channel leakage, which [17](../../17-communication-systems/README.md) and [21](../../21-rf-and-microwave-engineering/README.md) treat.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 03-03.1a | E[X] | 0.75 | — |
| 03-03.1b | E[X²] | 1.35 | — |
| 03-03.1c | Var(X) | 0.7875 | — |
| 03-03.1d | σ_X | 0.8874 | — |
| 03-03.2a | E[X] | 1.5 | — |
| 03-03.2b | E[X²] | 2.4 | — |
| 03-03.2c | Var(X) | 0.15 | — |
| 03-03.2d | σ_X | 0.3873 | — |
| 03-03.2e | E[Y] | 2.5 | — |
| 03-03.2f | Var(Y) | 1.35 | — |
| 03-03.2g | E[Y²] | 7.6 | — |
| 03-03.3a | exponential median | 693.1 | h |
| 03-03.3b | exponential mode | 0 | h |
| 03-03.3c | log-normal mode | 0.6206 | — |
| 03-03.4a | expected colliding pairs, 16-bit | 0.6935 | — |
| 03-03.4b | expected colliding pairs, 32-bit | 0.01164 | — |
| 03-03.5a | mean attempts | 1.0204 | — |
| 03-03.5b | variance of attempts | 0.02082 | — |
| 03-03.5c | standard deviation of attempts | 0.1443 | — |
| 03-03.5d | largest failure probability | 0.3333 | — |
| 03-03.6a | standard deviation | 10 | — |
| 03-03.6b | Chebyshev bound | 0.25 | — |
| 03-03.6c | P(N ≤ 80) | 0.02265 | — |
| 03-03.6d | P(N ≥ 120) | 0.02823 | — |
| 03-03.6e | exact two-sided probability | 0.05088 | — |
| 03-03.6f | Gaussian approximation | 0.04550 | — |
| 03-03.7a | mean lifetime | 114.1 | years |
| 03-03.7b | standard deviation of lifetime | 114.1 | years |
| 03-03.7c | median lifetime | 79.07 | years |
| 03-03.7d | P(outlive MTTF) | 0.3679 | — |
| 03-03.8a | MTTF, one part | 100000 | h |
| 03-03.8b | MTTF, parallel pair | 150000 | h |
| 03-03.8c | MTTF, TMR | 83333 | h |
| 03-03.8d | single-part reliability at 10,000 h | 0.9048 | — |
| 03-03.8e | TMR reliability at 10,000 h | 0.9746 | — |
| 03-03.8f | TMR crossover time | 69315 | h |
| 03-03.9a | average current | 2.5 | A |
| 03-03.9b | RMS current | 5 | A |
| 03-03.9c | ripple RMS current | 4.330 | A |
| 03-03.10a | total RMS voltage | 7.141 | mV |
| 03-03.10b | total power | −29.91 | dBm |
| 03-03.10c | SNR | 16.99 | dB |
| 03-03.11a | average-meter error, uniform noise | −3.809 | % |
| 03-03.11b | average-meter error, Gaussian noise | −11.38 | % |
| 03-03.11c | fraction of time clipped | 0.2700 | % |
| 03-03.11d | clipped power over σ² | 4.069×10^-4 | — |
| 03-03.11e | reading bias from clipping | −0.02035 | % |
| 03-03.12a | E[U²] | 0.3333 | — |
| 03-03.13a | mean envelope over √P̄ | 0.8862 | — |
| 03-03.13b | median envelope over √P̄ | 0.8326 | — |
| 03-03.13c | P(R > 2 E[R]) | 0.04321 | — |
| 03-03.13d | envelope-average underread | −1.049 | dB |
| 03-03.14a | hot-half rate ratio | 3.825 | — |
| 03-03.14b | cold-half rate ratio | 0.2209 | — |
| 03-03.14c | average over rate at 65 °C | 2.023 | — |
| 03-03.14d | fraction of failures when hot | 0.9454 | — |
| 03-03.14e | activation temperature E_a/k | 8123 | K |
| 03-03.15a | granular SNR, k = 3 | 55.43 | dB |
| 03-03.15b | clipping SNR, k = 3 | 33.91 | dB |
| 03-03.15c | total SNR, k = 3 | 33.88 | dB |
| 03-03.15d | granular SNR, k = 4 | 52.94 | dB |
| 03-03.15e | clipping SNR, k = 4 | 52.09 | dB |
| 03-03.15f | total SNR, k = 4 | 49.48 | dB |
| 03-03.15g | granular SNR, k = 5 | 51.00 | dB |
| 03-03.15h | clipping SNR, k = 5 | 74.12 | dB |
| 03-03.15i | total SNR, k = 5 | 50.98 | dB |
| 03-03.15j | optimum loading | 4.494 | — |
| 03-03.15k | optimum SNR | 51.56 | dB |
| 03-03.15l | granular SNR at optimum | 51.92 | dB |
| 03-03.15m | full-scale sine SNR, 10 bits | 61.97 | dB |
| 03-03.16a | clipping probability, 6 dB | 0.01867 | — |
| 03-03.16b | clipped power, 6 dB | −17.29 | dB |
| 03-03.16c | efficiency, 6 dB | 44.42 | % |
| 03-03.16d | clipping probability, 8 dB | 1.819×10^-3 | — |
| 03-03.16e | clipped power, 8 dB | −27.40 | dB |
| 03-03.16f | efficiency, 8 dB | 35.28 | % |
| 03-03.16g | clipping probability, 10 dB | 4.540×10^-5 | — |
| 03-03.16h | clipped power, 10 dB | −43.43 | dB |
| 03-03.16i | efficiency, 10 dB | 28.02 | % |
| 03-03.16j | minimum back-off for −30 dBc | 8.393 | dB |
| 03-03.16k | efficiency at that back-off | 33.72 | % |
