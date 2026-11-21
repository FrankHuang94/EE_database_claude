# Solutions 17-05 · Matched Filters and Optimal Detection

Problems: [17-05 problems](../problems/17-05-problems.md) · Chapter: [17-05](../chapters/17-05-matched-filters-and-detection.md). Every number below is recomputed by [verify_17_05.py](../verify/verify_17_05.py): integrals numerically, error probabilities in closed form and by Monte Carlo detection, Gram–Schmidt on sampled waveforms, and pulse compression on a simulated chirp.

---

## Solutions

### Solution 17-05.1

The matched filter is $h(t) = s(T - t) = A(1 - t/T)$ for $0 \le t < T$: a falling ramp. The energy is

$$
E = \int_0^T\frac{A^2t^2}{T^2}\,dt = \frac{A^2T}{3} = \frac{4 \times 3 \times 10^{-6}}{3} = \textbf{4.0} \times 10^{-6}\ \text{V}^2\text{s} ,
$$

and the peak SNR is $2E/N_0 = 8 \times 10^{-6}/10^{-7}$ = **80**, **19.03** dB. A rectangular pulse of the same peak would carry three times the energy; the ramp wastes amplitude in its low early part.

### Solution 17-05.2

$P_b = Q(\sqrt{2E_b/N_0})$:

- 0 dB: $Q(\sqrt2) = Q(1.414)$ = **0.0786**.
- 4 dB: $Q(\sqrt{5.024}) = Q(2.241)$ = **0.0125**.
- 7 dB: $Q(\sqrt{10.02}) = Q(3.165)$ = **7.7 × 10⁻⁴**.
- 9.6 dB: $Q(\sqrt{18.24}) = Q(4.271)$ = **9.7 × 10⁻⁶**.

Each 3 dB at the high end buys far more than at the low end: the "waterfall".

### Solution 17-05.3

$E_b/N_0 = [Q^{-1}(P_b)]^2/2$:

- $10^{-3}$: $Q^{-1} = 3.090$, so $E_b/N_0$ = 4.774, **6.79** dB.
- $10^{-9}$: $Q^{-1} = 5.998$, **12.55** dB.
- $10^{-12}$: $Q^{-1} = 7.034$, **13.93** dB.

From $10^{-9}$ to $10^{-12}$, a thousandfold improvement, costs only 1.4 dB.

### Solution 17-05.4

With the window shifted by $T/4$, the integrator collects only $3T/4$ of the wanted pulse: the signal falls to 0.75 of its peak while the noise (integrated over a full window) is unchanged, so the SNR falls by $0.75^2$, **−2.50** dB. The remaining quarter of the window now holds the next symbol, contributing $\pm0.25$; when it has the opposite sign, the sample is $0.75 - 0.25$ = **0.5** of the ideal: the worst-case eye halves (−6.02 dB).

### Solution 17-05.5

$\phi_1 = s_1$ (energy 1). $s_2 - \langle s_2, \phi_1\rangle\phi_1 = s_2 - 0.5s_1$ is $+0.5$ on the first half and $-0.5$ on the second, energy 0.25, so $\phi_2 = 2(s_2 - 0.5s_1)$, the ±1 split pulse. $s_3 = s_1 - s_2$ and $s_4 = s_2 - s_3$ lie in the span already found, so the space has **2** dimensions. Vectors: $\mathbf s_1 = (1, 0)$, $\mathbf s_2 = (0.5, 0.5)$, $\mathbf s_3 = (0.5, -0.5)$, $\mathbf s_4 = (0, 1)$. Distances: $d_{23} = \lvert(0, 1)\rvert$ = **1.0**, $d_{14} = \lvert(1, -1)\rvert = \sqrt2$ = **1.414**.

### Solution 17-05.6

Each coordinate is ±a with independent noise of variance $N_0/2$, so a coordinate is wrong with probability $q = Q(a/\sqrt{N_0/2}) = Q(\sqrt{E_s/N_0}) = Q(\sqrt{10})$ = 7.83 × 10⁻⁴. The symbol is right only if both coordinates are: $P_s = 1 - (1 - q)^2 = 2q - q^2$ = **1.565 × 10⁻³**. The union bound counts two neighbours at $d = 2a$ and one diagonal point at $2\sqrt2a$: $2Q(\sqrt{10}) + Q(\sqrt{20})$ = **1.569 × 10⁻³**. The nearest-neighbour approximation $2q$ = **1.565 × 10⁻³** differs from the exact value only in the $q^2$ term.

### Solution 17-05.7

$t = (N_0/4)\ln(P_2/P_1) = 0.25\ln(0.4/0.6)$ = **−0.1014**. With σ = $\sqrt{N_0/2}$ = 0.7071: $P(e\mid+1) = Q((1 - t)/\sigma) = Q(1.558)$ and $P(e\mid-1) = Q((1 + t)/\sigma) = Q(1.271)$, so $P_e = 0.6\,Q(1.558) + 0.4\,Q(1.271)$ = **0.0766**. ML: $Q(1/0.7071) = Q(1.414)$ = **0.0786**. With priors this close to equal, MAP gains only 2.7%.

### Solution 17-05.8

Solve $\frac{2(M - 1)}{M}Q\big(\sqrt{6E_s/((M^2 - 1)N_0)}\big) = 10^{-5}$ numerically:

- 2-PAM: **9.59** dB.
- 4-PAM: **16.76** dB.
- 8-PAM: **23.06** dB.

Each doubling of M costs about 6–7 dB of $E_s/N_0$ (and, per bit, about 4–5 dB of $E_b/N_0$).

### Solution 17-05.9

With $x = T/\tau = 2$, the ratio is $2(1 - e^{-2})^2/2 = (1 - e^{-2})^2$ = **0.748**, **−1.26** dB: worse than the optimum (0.815 at $x$ = 1.256) because the wider filter ($f_{3\text{dB}} = 1/(2\pi\tau) = 1/(\pi T) \approx 0.32/T$, against the optimum's $0.20/T$) passes more noise while gaining little extra signal.

### Solution 17-05.10

Write $x = fT$. The pulse spectrum satisfies $\lvert S(f)\rvert^2 = A^2T^2\operatorname{sinc}^2(x)$ and $\int\lvert S\rvert^2df = E$. Let $g(x) = 1 + 9/(1 + x^2)$ so that $S_n = (N_0/2)g$.

(a) The white-noise matched filter $H = S^*$ has signal output $E$ and noise variance $\int\lvert S\rvert^2S_n\,df = (N_0/2)E\int\operatorname{sinc}^2(x)g(x)\,dx$. Relative to $2E/N_0$ the SNR is $1/\int\operatorname{sinc}^2g\,dx$ = **0.1167**, **−9.33** dB.

(b) The optimal filter gives $\int\lvert S\rvert^2/S_n\,df$, relative to $2E/N_0$: $\int\operatorname{sinc}^2(x)/g(x)\,dx$ = **0.1453**, **−8.38** dB. (Numerically, write $1/g = 1 - 9/(10 + x^2)$ and use $\int\operatorname{sinc}^2 = 1$: the remaining integrand decays fast, whereas a truncated integral of $\operatorname{sinc}^2/g$ converges slowly.)

Accounting for the colour gains **0.95** dB: the optimal filter de-emphasizes the low frequencies where the noise is ten times stronger, at the cost of discarding some signal energy there.

### Solution 17-05.11

With transmit spectrum $P = \sqrt{H_{RC}}$ (unit-energy normalization aside) and receive filter $H$, the sampled SNR relative to the matched filter is, by the Cauchy–Schwarz form of §3.2, $\lvert\int PH\,df\rvert^2/\big(\int\lvert P\rvert^2df\int\lvert H\rvert^2df\big)$. For the brick-wall $H = 1$ on $\lvert f\rvert \le (1 + \alpha)/(2T)$, $\int\lvert H\rvert^2 = (1 + \alpha)/T$, giving the stated formula. Numerically, with $T = 1$ and α = 0.35, the ratio is **0.889**, **−0.51** dB. The brick-wall filter collects the noise in the roll-off bands at full weight although the signal there is weak. (It also does not give zero ISI with the RRC pulse.)

### Solution 17-05.12

$E_s/N_0 = \log_2M \times 3.981$:

- M = 2: $Q(\sqrt{3.98})$ = **0.0230**, bandwidth ×2 (two dimensions per bit, against one for antipodal binary).
- M = 16: $15\,Q(\sqrt{15.92})$ = **4.9 × 10⁻⁴**, bandwidth ×4.
- M = 64: $63\,Q(\sqrt{23.89})$ = **3.2 × 10⁻⁵**, bandwidth ×10.7.

At fixed $E_b/N_0$ the error probability falls as M grows, while the bandwidth grows as $M/\log_2M$. Letting M → ∞ (with a tighter bound than the union bound), the error probability goes to zero for any $E_b/N_0 > \ln 2$, −1.59 dB: Shannon's limit (17-07), reached here by spending unlimited bandwidth.

### Solution 17-05.13

$TB = 20\ \mu\text{s} \times 50\ \text{MHz}$ = **1000**, **30** dB. Resolution $c/(2B) = 3 \times 10^8/10^8$ = **3.0** m. An unmodulated pulse resolves $c\tau/2$, so the same 3 m needs τ = $1/B$ = **20** ns, a thousand times shorter than the chirp. For the same energy it needs a thousand times (30 dB) more peak power. Pulse compression lets a solid-state transmitter with modest peak power match a high-power magnetron's detection and resolution.

### Solution 17-05.14

$E/N_0 = C/N_0 \times T$ = 46.87 dB-Hz − 30 dB = 16.87 dB, so the peak SNR is $2E/N_0$ = **19.88** dB (97.3, an amplitude ratio of 9.86 between the expected peak and the noise standard deviation). A threshold at half the peak sits 4.93σ from both the peak and zero:

- miss probability $Q(4.93)$ = **4.1 × 10⁻⁷**;
- false-alarm probability per wrong cell, the same **4.1 × 10⁻⁷**.

A full search covers $1023 \times 2 \times 20$ = **40 920** cells, so about **0.017** false alarms are expected per search. Real receivers correlate non-coherently (the magnitude of I and Q) because the carrier phase is unknown during acquisition; that costs some sensitivity and changes the statistics from Gaussian to Rician and Rayleigh, but the picture is the same.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-05.1a | ramp energy | 4.0e-6 | V²s |
| 17-05.1b | peak SNR | 80 | — |
| 17-05.1c | peak SNR in dB | 19.03 | dB |
| 17-05.2a | BPSK BER at 0 dB | 0.0786 | — |
| 17-05.2b | BPSK BER at 4 dB | 0.0125 | — |
| 17-05.2c | BPSK BER at 7 dB | 7.7e-4 | — |
| 17-05.2d | BPSK BER at 9.6 dB | 9.7e-6 | — |
| 17-05.3a | Eb/N0 for 1e-3 | 6.79 | dB |
| 17-05.3b | Eb/N0 for 1e-9 | 12.55 | dB |
| 17-05.3c | Eb/N0 for 1e-12 | 13.93 | dB |
| 17-05.4a | SNR loss, quarter-symbol shift | −2.50 | dB |
| 17-05.4b | worst-case eye | 0.5 | — |
| 17-05.5a | dimensions | 2 | — |
| 17-05.5b | d23 | 1.0 | — |
| 17-05.5c | d14 | 1.414 | — |
| 17-05.6a | exact symbol-error probability | 1.565e-3 | — |
| 17-05.6b | union bound | 1.569e-3 | — |
| 17-05.6c | nearest-neighbour approximation | 1.565e-3 | — |
| 17-05.7a | MAP threshold | −0.1014 | — |
| 17-05.7b | MAP error probability | 0.0766 | — |
| 17-05.7c | ML error probability | 0.0786 | — |
| 17-05.8a | 2-PAM Es/N0 for 1e-5 | 9.59 | dB |
| 17-05.8b | 4-PAM Es/N0 for 1e-5 | 16.76 | dB |
| 17-05.8c | 8-PAM Es/N0 for 1e-5 | 23.06 | dB |
| 17-05.9a | ratio at τ = T/2 | 0.748 | — |
| 17-05.9b | in dB | −1.26 | dB |
| 17-05.10a | white matched filter in coloured noise | 0.1167 | — |
| 17-05.10b | in dB | −9.33 | dB |
| 17-05.10c | optimal filter | 0.1453 | — |
| 17-05.10d | in dB | −8.38 | dB |
| 17-05.10e | gain from whitening | 0.95 | dB |
| 17-05.11a | brick-wall ratio | 0.889 | — |
| 17-05.11b | in dB | −0.51 | dB |
| 17-05.12a | M = 2 bound | 0.0230 | — |
| 17-05.12b | M = 16 bound | 4.9e-4 | — |
| 17-05.12c | M = 64 bound | 3.2e-5 | — |
| 17-05.12d | M = 64 bandwidth expansion | 10.7 | — |
| 17-05.13a | time-bandwidth product | 1000 | — |
| 17-05.13b | in dB | 30 | dB |
| 17-05.13c | range resolution | 3.0 | m |
| 17-05.13d | equivalent short pulse | 20 | ns |
| 17-05.14a | peak SNR | 19.88 | dB |
| 17-05.14b | miss probability | 4.1e-7 | — |
| 17-05.14c | false-alarm probability per cell | 4.1e-7 | — |
| 17-05.14d | cells per search | 40920 | — |
| 17-05.14e | expected false alarms per search | 0.017 | — |
