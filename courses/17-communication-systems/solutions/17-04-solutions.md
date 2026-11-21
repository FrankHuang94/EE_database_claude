# Solutions 17-04 · Baseband Digital Transmission

Problems: [17-04 problems](../problems/17-04-problems.md) · Chapter: [17-04](../chapters/17-04-baseband-digital-transmission.md). Every number below is recomputed by [verify_17_04.py](../verify/verify_17_04.py): spectra by numerical folding and integration, pulse samples by direct evaluation, eyes and error rates by enumerating symbol patterns, and the DFE and spectra by simulation.

---

## Solutions

### Solution 17-04.1

(a) Each lane carries $400/4$ = **100** Gb/s. PAM4 sends 2 bits per symbol: **50** GBd, Nyquist frequency **25** GHz.

(b) 64 Gb/s at 2 bits per symbol is **32** GBd, with Nyquist frequency **16** GHz: the same as 32 Gb/s NRZ.

(c) 3 bits per 2 symbols is **1.5** bits per symbol. A three-level symbol can carry at most $\log_23 = 1.585$ bits, so the code achieves $1.5/1.585$ = **0.946** of the maximum; the 9 combinations of two symbols carry 8 bit patterns, and the ninth is spare.

### Solution 17-04.2

- (a) $10.3125 \times 64/66$ = **10.0** Gb/s.
- (b) $2.5 \times 8/10$ = **2.0** Gb/s.
- (c) $8 \times 128/130$ = **7.877** Gb/s per lane. Sixteen lanes carry $16 \times 7.877 = 126.0$ Gb/s, which is $126.0/8$ = **15.75** GB/s in each direction.

The long block codes cost about 1.5–3% of the line rate against 8b/10b's 25%, which is why links abandoned 8b/10b as rates rose.

### Solution 17-04.3

$\mathbb{E}[a^2] = (M^2 - 1)/3$: **1**, **5** and **21** for M = 2, 4, 8.

(a) Equal peak amplitude: the outer level is $M - 1$, so with the peak fixed the spacing scales as $1/(M - 1)$: 4-PAM **−9.54** dB, 8-PAM $20\log_{10}(1/7)$ = **−16.90** dB.

(b) Equal average power: the spacing scales as $1/\sqrt{\mathbb{E}[a^2]}$, relative to 2-PAM $\sqrt{3/(M^2 - 1)}$: 4-PAM $20\log_{10}(1/\sqrt5)$ = **−6.99** dB, 8-PAM $20\log_{10}\sqrt{3/63}$ = **−13.22** dB.

Each doubling of the number of levels costs about 6 dB at equal average power (the classic rule for large M), more at equal peak.

### Solution 17-04.4

The pulse is a positive half-width rectangle followed by a negative one. A rectangle of width $T/2$ starting at 0 has transform $(T/2)\operatorname{sinc}(fT/2)e^{-j\pi fT/2}$; the negative one is the same delayed by $T/2$. So

$$
P(f) = \frac T2\operatorname{sinc}\Big(\frac{fT}2\Big)e^{-j\pi fT/2}\big(1 - e^{-j\pi fT}\big) = jT\operatorname{sinc}\Big(\frac{fT}2\Big)\sin\Big(\frac{\pi fT}2\Big)e^{-j\pi fT} ,
$$

using $1 - e^{-j\theta} = 2je^{-j\theta/2}\sin(\theta/2)$. For independent equiprobable ±A symbols, $S_a = A^2$ and $S_X = \lvert P\rvert^2A^2/T = A^2T\operatorname{sinc}^2(fT/2)\sin^2(\pi fT/2)$. At $f = 1/T$: $\operatorname{sinc}^2(1/2)\sin^2(\pi/2) = (2/\pi)^2$ = **0.405** $A^2T$. Where NRZ has a null, Manchester has much of its power.

### Solution 17-04.5

Fold each spectrum with period $1/T$ and test for a constant $T$ (it suffices to check $0 \le f \le 1/(2T)$ by symmetry).

- (a) For $0 < f < 1/T$ the copies at $0$ and $1/T$ overlap: $T(1 - fT) + T(1 - (1/T - f)T) = T$. **Zero ISI.** The pulse is $\operatorname{sinc}^2(t/T)$, zero at every nonzero multiple of $T$.
- (b) Between $0.4/T$ and $0.6/T$ two copies overlap, each $T$: the sum is $2T$ there. **Fails.** The pulse is $1.2\operatorname{sinc}(1.2t/T)$, so $h(T)/h(0) = \operatorname{sinc}(1.2)$ = **−0.156**.
- (c) The ideal rectangle: copies just touch, sum $T$. **Zero ISI** (the sinc).
- (d) The linear roll-off from $0.3/T$ to $0.7/T$ is odd-symmetric about $0.5/T$ (where it equals $T/2$), so the overlapping copies add to $T$. **Zero ISI.**

### Solution 17-04.6

A passband raised-cosine signal occupies $(1 + \alpha)R_s$. With 6 MHz and α = 0.25: $R_s = 6/1.25$ = **4.8** Msymbol/s and 64-QAM carries $6 \times 4.8$ = **28.8** Mb/s. With α = 0.1: $R_s$ = **5.455** Msymbol/s and **32.73** Mb/s, 14% more, paid for with longer filters and less timing margin.

### Solution 17-04.7

A sample whose noiseless value is $v$ is decided wrongly with probability $Q(v/\sigma)$. The worst pattern gives the upper bound $Q(0.6/0.12) = Q(5)$ = **2.87 × 10⁻⁷**; the ISI-free cursor gives the lower bound $Q(1/0.12) = Q(8.33)$ = **3.9 × 10⁻¹⁷**. Ten orders of magnitude separate them, so the actual error rate depends almost entirely on how often the worst patterns occur (Problem 17-04.14).

### Solution 17-04.8

τ = $1/(2\pi \times 10\ \text{GHz})$ = 15.92 ps. A 50% eye needs $r = 1/4$, so $T = \tau\ln4$ and the rate is $1/(\tau\ln4)$ = **45.3** Gb/s. At 56 Gb/s, $T$ = 17.86 ps, $T/\tau$ = 1.122, $r$ = 0.326, and the worst-case eye is $1 - 2r$ = **0.349**.

### Solution 17-04.9

At ε = 0.25T, summing over ±200 symbols:

- Raised cosine, α = 0.35: main cursor **0.894**, worst-case ISI **0.640**, eye **0.254**.
- Sinc: main cursor **0.900**, worst-case ISI **2.68**, eye **−1.78**: closed, and the sum keeps growing with more terms.

A quarter-symbol timing error costs the α = 0.35 pulse most of its eye; it is still open, while the sinc's is not.

### Solution 17-04.10

With correct past decisions, a DFE removes the postcursors it covers exactly.

- One tap (removes $h_1$): the remaining ISI is $h_{-1} + h_2 = 0.25$, so the worst-case eye is $1 - 0.25$ = **0.75**.
- Two taps (removes $h_1$ and $h_2$): only the precursor remains, and the eye is $1 - 0.1$ = **0.9**.
- The three-tap ZF equalizer gave 0.922 but multiplied the noise variance by 1.364.

The DFE cannot touch precursors (the future symbols are not yet decided) and adds no noise, but a wrong decision subtracts the wrong ISI. The ZF FFE handles precursors at the cost of noise. Practical receivers use a short FFE for precursors and a DFE for postcursors.

### Solution 17-04.11

Let $h_s(t) = h(t)\sum_k\delta(t - kT) = \sum_kh(kT)\delta(t - kT)$. Multiplying by an impulse train convolves spectra with $\frac1T\sum_m\delta(f - m/T)$ (11-10), so $H_s(f) = \frac1T\sum_mH(f - m/T)$. Zero ISI means $h(kT) = \delta_k$, so $h_s(t) = \delta(t)$ and $H_s(f) = 1$. Hence $\sum_mH(f - m/T) = T$.

Now let $H$ be zero beyond $1/T$, equal to $T$ below $(1 - \alpha)/(2T)$, and satisfy $H(1/(2T) + x) = T - H(1/(2T) - x)$ in the roll-off (odd symmetry about the point $(1/(2T), T/2)$). For $0 \le f \le 1/(2T)$, only the copies $m = 0$ and $m = 1$ can be nonzero, and with $f = 1/(2T) - x$: $H(f) + H(f - 1/T) = H(1/(2T) - x) + H(1/(2T) + x) = T$ (using evenness, $H(f - 1/T) = H(1/T - f)$). By symmetry the same holds for negative $f$.

For the raised cosine with α = 0.5 at $f = 0.4/T$: the roll-off runs from $0.25/T$ to $0.75/T$, so $H(0.4/T)/T = \tfrac12[1 + \cos(2\pi \times 0.15)]$ = **0.794** and $H(-0.6/T)/T = \tfrac12[1 + \cos(2\pi \times 0.35)]$ = **0.206**; they sum to 1.

### Solution 17-04.12

$\operatorname{sinc}(t/T)$ has spectrum $T$ on $\lvert f\rvert < 1/(2T)$; the delayed copy multiplies it by $e^{-j2\pi fT}$. So

$$
H(f) = T(1 + e^{-j2\pi fT}) = 2T\cos(\pi fT)e^{-j\pi fT},\qquad \lvert f\rvert < \frac{1}{2T} ,
$$

with bandwidth exactly $1/(2T)$, Nyquist's minimum, but a spectrum that falls smoothly to zero at the band edge instead of the sinc's brick wall. Its samples are $h(0) = h(T) = 1$ and zero elsewhere: controlled ISI from exactly one neighbour. With ±1 symbols the sampler sees $a_n + a_{n-1} \in \{-2, 0, +2\}$ with probabilities **0.25**, **0.5** and 0.25: **3** levels. With the same peak amplitude (2), the level spacing is 2 against binary's 4: the eye is half as tall, **−6.02** dB.

The controlled ISI lets the pulse use the minimum bandwidth with a spectrum that is still strictly band-limited, so only approximately realizable, but far easier to approximate than the sinc's because it falls to zero at the band edge instead of jumping. Its problem is that decoding $a_n = y_n - a_{n-1}$ propagates errors. **Precoding** at the transmitter ($b_n = d_n \oplus b_{n-1}$, sending $a_n = 2b_n - 1$) makes each received level depend on one data bit alone (0 means the bit is 1, ±2 means it is 0), so errors no longer propagate.

### Solution 17-04.13

At 112 Gb/s the Nyquist frequencies are 56 GHz (NRZ) and 28 GHz (PAM4); PAM4 wins when $L(56) - L(28) > 20\log_{10}3 = 9.54$ dB.

- (a) $a(56 - 28) > 9.54$ gives $a >$ **0.341** dB/GHz, a loss of 9.54 dB at 28 GHz and 19.1 dB at 56 GHz.
- (b) $b(\sqrt{56} - \sqrt{28}) > 9.54$ gives $b >$ **4.354** dB/√GHz, which is **23.04** dB at 28 GHz.

The square-root channel must be much lossier overall before PAM4 pays, because its loss grows slowly between the two Nyquist frequencies.

### Solution 17-04.14

The interference is $0.1a_{1} + 0.3a_{-1}$ in the indexing of cursors ($h_{-1}$ multiplies the next symbol, $h_1$ the previous), taking the four values ±0.4 and ±0.2. With $a_0 = +1$, the noiseless samples are **0.6**, **0.8**, **1.2** and **1.4**, each with probability 1/4. The BER is

$$
\tfrac14\big[Q(6) + Q(8) + Q(12) + Q(14)\big] = \textbf{2.47} \times 10^{-10} ,
$$

almost entirely from the worst pattern: $Q(6)/4$. The worst-case bound is $Q(6)$ = **9.87 × 10⁻¹⁰**, only four times higher, and the ISI-free value is $Q(10)$ = **7.6 × 10⁻²⁴**. The statistical eye's lesson: at low error rates, the worst patterns set the BER, and their probability, not the average ISI, is what matters.

### Solution 17-04.15

(a) With $q_k = \sum_jc_jh_{k-j}$, the three conditions are

$$
\begin{aligned}
q_{-1} &= c_{-1}h_0 + c_0h_{-1} + c_1h_{-2} = c_{-1} + 0.15c_0 = 0 ,\\
q_0 &= c_{-1}h_1 + c_0h_0 + c_1h_{-1} = 0.5c_{-1} + c_0 + 0.15c_1 = 1 ,\\
q_1 &= c_{-1}h_2 + c_0h_1 + c_1h_0 = 0.2c_{-1} + 0.5c_0 + c_1 = 0 .
\end{aligned}
$$

From the first, $c_{-1} = -0.15c_0$; the third gives $c_1 = -0.5c_0 + 0.03c_0 = -0.47c_0$; the second then gives $c_0(1 - 0.075 - 0.0705) = 1$, so $c_0$ = **1.1703**, $c_{-1}$ = **−0.1755** and $c_1$ = **−0.5500**.

(b) $q_{-2} = c_{-1}h_{-1} = -0.0263$; $q_{-1} = 0$, $q_0 = 1$, $q_1 = 0$ by design; $q_2 = c_0h_2 + c_1h_1 = 0.2341 - 0.2750 = -0.0410$; $q_3 = c_1h_2 = -0.1100$. Residual ISI $0.0263 + 0.0410 + 0.1100$ = **0.1773**: the equalizer zeroes the taps it controls and pushes smaller ISI outside its span.

(c) Before: $h_0 - (0.15 + 0.5 + 0.2)$ = **0.15**, a nearly closed eye. After: $1 - 0.1773$ = **0.823**.

(d) $\sum c_j^2 = 0.0308 + 1.3695 + 0.3025$ = **1.703**, **2.31** dB of noise enhancement. Worth it: the worst-case eye grows 5.5 times (14.8 dB) for 2.3 dB more noise. A DFE could remove $q_2$ and $q_3$ without enhancing noise, and more FFE taps would shrink the residual further.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-04.1a | lane bit rate | 100 | Gb/s |
| 17-04.1b | lane symbol rate | 50 | GBd |
| 17-04.1c | lane Nyquist frequency | 25 | GHz |
| 17-04.1d | 64 GT/s PAM4 symbol rate | 32 | GBd |
| 17-04.1e | its Nyquist frequency | 16 | GHz |
| 17-04.1f | PAM3 code bits per symbol | 1.5 | — |
| 17-04.1g | fraction of log2 3 | 0.946 | — |
| 17-04.2a | 64b/66b payload | 10.0 | Gb/s |
| 17-04.2b | 8b/10b payload | 2.0 | Gb/s |
| 17-04.2c | 128b/130b payload per lane | 7.877 | Gb/s |
| 17-04.2d | x16 payload per direction | 15.75 | GB/s |
| 17-04.3a | E[a²], M = 2 | 1 | — |
| 17-04.3b | E[a²], M = 4 | 5 | — |
| 17-04.3c | E[a²], M = 8 | 21 | — |
| 17-04.3d | 4-PAM spacing, equal peak | −9.54 | dB |
| 17-04.3e | 8-PAM spacing, equal peak | −16.90 | dB |
| 17-04.3f | 4-PAM spacing, equal power | −6.99 | dB |
| 17-04.3g | 8-PAM spacing, equal power | −13.22 | dB |
| 17-04.4a | Manchester PSD at 1/T | 0.405 | A²T |
| 17-04.5a | first ISI sample of spectrum (b) | −0.156 | — |
| 17-04.6a | symbol rate, α = 0.25 | 4.8 | Msymbol/s |
| 17-04.6b | bit rate, α = 0.25 | 28.8 | Mb/s |
| 17-04.6c | symbol rate, α = 0.1 | 5.455 | Msymbol/s |
| 17-04.6d | bit rate, α = 0.1 | 32.73 | Mb/s |
| 17-04.7a | BER upper bound | 2.87e-7 | — |
| 17-04.7b | BER lower bound | 3.9e-17 | — |
| 17-04.8a | rate for a 50% eye | 45.3 | Gb/s |
| 17-04.8b | eye at 56 Gb/s | 0.349 | — |
| 17-04.9a | RC main cursor at 0.25T | 0.894 | — |
| 17-04.9b | RC worst ISI at 0.25T | 0.640 | — |
| 17-04.9c | RC eye at 0.25T | 0.254 | — |
| 17-04.9d | sinc main cursor at 0.25T | 0.900 | — |
| 17-04.9e | sinc worst ISI at 0.25T | 2.68 | — |
| 17-04.9f | sinc eye at 0.25T | −1.78 | — |
| 17-04.10a | eye with one DFE tap | 0.75 | — |
| 17-04.10b | eye with two DFE taps | 0.9 | — |
| 17-04.11a | H(0.4/T)/T, α = 0.5 | 0.794 | — |
| 17-04.11b | H(−0.6/T)/T, α = 0.5 | 0.206 | — |
| 17-04.12a | duobinary levels | 3 | — |
| 17-04.12b | probability of the zero level | 0.5 | — |
| 17-04.12c | probability of each outer level | 0.25 | — |
| 17-04.12d | eye relative to NRZ, same peak | −6.02 | dB |
| 17-04.13a | linear loss slope threshold | 0.341 | dB/GHz |
| 17-04.13b | square-root loss coefficient threshold | 4.354 | dB/√GHz |
| 17-04.13c | corresponding loss at 28 GHz | 23.04 | dB |
| 17-04.14a | worst sample value | 0.6 | — |
| 17-04.14b | exact BER | 2.47e-10 | — |
| 17-04.14c | worst-case bound | 9.87e-10 | — |
| 17-04.14d | ISI-free BER | 7.6e-24 | — |
| 17-04.15a | c0 | 1.1703 | — |
| 17-04.15b | c−1 | -0.1755 | — |
| 17-04.15c | c1 | -0.5500 | — |
| 17-04.15d | residual ISI | 0.1773 | — |
| 17-04.15e | eye before | 0.15 | — |
| 17-04.15f | eye after | 0.823 | — |
| 17-04.15g | noise enhancement | 1.703 | — |
| 17-04.15h | noise enhancement | 2.31 | dB |
