# Course 17 · Final Exam Solutions (Communication Systems)

Exam: [README.md](README.md). Every number below is recomputed by [verify_17_exam.py](../verify/verify_17_exam.py):

- noise bandwidths and correlations by numerical integration of $\lvert H\rvert^2$ and of the PSD, and the random-phase sinusoid's autocorrelation by averaging over Θ;
- cascades and sensitivities from their definitions; Bessel spectra with `scipy.special.jv`, checked by an FFT of the tone-FM waveform;
- ISI from the sampled pulse response of a simulated RC channel; matched-filter and RC-filter SNRs by integration; error probabilities with `scipy.stats.norm`, and the MAP threshold by root finding on the weighted likelihoods;
- entropy and a Huffman code built by a heap; the Hamming code by enumerating all error patterns; Erlang B from its closed form;
- path loss from an exact two-ray field sum; fading error rates by numerical integration over the exponential SNR density; ICI from the exact Dirichlet kernel; MIMO capacity from `numpy.linalg.svd`;
- networking results with the standard-library `ipaddress` module and from the definitions.

---

## Solutions

### Solution 1

(a) The mean is $E[A\cos(2\pi f_0t + \Theta)] = \frac{A}{2\pi}\int_0^{2\pi}\cos(2\pi f_0t + \theta)\,d\theta = 0$ for every $t$. The autocorrelation is

$$
R_X(t + \tau, t) = A^2E[\cos(2\pi f_0(t + \tau) + \Theta)\cos(2\pi f_0t + \Theta)] = \frac{A^2}{2}\cos(2\pi f_0\tau) + \frac{A^2}{2}E[\cos(2\pi f_0(2t + \tau) + 2\Theta)] .
$$

The last expectation is zero, so $R_X(\tau) = (A^2/2)\cos(2\pi f_0\tau)$ = **2** cos(2π · 1000 τ) V². The mean is constant and $R_X$ depends only on τ, so the process is **wide-sense stationary**.

(b) The power is $R_X(0)$ = **2** V² (2 W into 1 Ω), as for any sinusoid of 2 V peak. By Wiener–Khinchin, $S_X(f) = \tfrac{A^2}{4}\big[\delta(f - f_0) + \delta(f + f_0)\big]$: two lines of weight **1** V² at ±1 kHz.

(c) For $H(f) = 1/(1 + jf/f_c)$,

$$
B_N = \int_0^\infty\frac{df}{1 + (f/f_c)^2} = \frac\pi2f_c = \textbf{15.71}\ \text{kHz} .
$$

The output variance is $\int_{-\infty}^{\infty}(N_0/2)\lvert H\rvert^2df = N_0B_N = 2 \times 10^{-8} \times 15\,708$ = **3.142 × 10⁻⁴** V², an rms value of **17.72** mV.

(d) The output autocorrelation of a one-pole filter driven by white noise is proportional to $e^{-\lvert\tau\rvert/RC}$ (17-01), so the correlation coefficient is $\rho(\tau) = e^{-\lvert\tau\rvert/RC}$ with $RC = 1/(2\pi f_c)$ = 15.92 µs. At 20 µs, $\rho = e^{-1.257}$ = **0.285**. It falls below 0.1 for $\tau > RC\ln10$ = **36.65** µs.

### Solution 2

(a) In linear terms: $F_1 = 10^{0.15} = 1.4125$, $G_1 = 31.62$; the mixer's $F_2 = 10^{0.8} = 6.310$, $G_2 = 10^{-0.8} = 0.1585$; $F_3 = 10^{0.4} = 2.512$. Friis:

$$
F = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1G_2} = 1.4125 + 0.1679 + 0.3017 = \textbf{1.882},
$$

an NF of **2.75** dB. After the LNA, the **IF amplifier** contributes most (0.302 against the mixer's 0.168), because the mixer's loss divides the gain in front of it by 6.3.

(b) $T_e = T_0(F - 1) = 290 \times 0.882$ = **255.8** K.

(c) A passive loss $L$ at $T_0$ has $F = L$, and it divides the following gain by $L$, so the new factor is $L \cdot F$: $2 + 2.75$ = **4.75** dB. Loss in front of the LNA adds decibel for decibel.

(d) $P_{sens} = -174 + 10\log_{10}(20 \times 10^6) + 2.75 + 10 = -174 + 73.01 + 2.75 + 10$ = **−88.2** dBm. Because $\text{SNR} = (E_b/N_0)(R_b/B)$, $E_b/N_0 = 10 - 10\log_{10}(40/20)$ = **6.99** dB.

### Solution 3

(a) The deviation ratio is $D = \Delta f/W = 40/10$ = **4**. Carson's rule gives $B_T = 2(\Delta f + W) = 2(40 + 10)$ = **100** kHz.

(b) The carrier holds $J_0^2(4)$ = **0.158** of the power. Lines lie at $f_c \pm n \times 10$ kHz, so the ±50 kHz Carson band contains $n = 0$ to 5:

$$
J_0^2 + 2\sum_{n=1}^{5}J_n^2 = 0.1577 + 2(0.0044 + 0.1326 + 0.1851 + 0.0790 + 0.0175) = \textbf{0.995}.
$$

Carson's rule captures 99.5% of the power here, which is why it is a good engineering bandwidth.

(c) For a tone, $\text{SNR}_{\text{FM}} = \tfrac32\beta^2\gamma$ with $\gamma = S_R/(N_0W)$, against $\text{SNR}_{\text{DSB}} = \gamma$. The advantage is $\tfrac32 \times 16$ = **24**, **13.80** dB. FM uses **100** kHz; DSB uses $2W$ = **20** kHz. FM spends five times the bandwidth to buy 13.8 dB.

(d) With $k_a^2P_m = 0.5^2/2 = 0.125$, $\eta = 0.125/1.125$ = **0.111** (11.1%), so the output SNR is $\eta\gamma$, **−9.54** dB against DSB. Eight-ninths of the power is carrier.

### Solution 4

(a) NRZ carries one bit per symbol: **56** GBd, Nyquist frequency **28** GHz. PAM4 carries two: **28** GBd, Nyquist **14** GHz.

(b) $(1 + \alpha)R_s/2 = 1.3 \times 28/2$ = **18.2** GHz.

(c) $\tau = 1/(2\pi \times 12\ \text{GHz})$ = **13.26** ps. The one-pole pulse response has main cursor $h_0 = 1 - r$ and postcursors summing to $r$ (17-04).

- NRZ: $T$ = 17.86 ps, $r = e^{-1.346}$ = **0.260**. Worst-case ISI subtracts $r$ from each side of the ±1 decision, so the eye is $2(1 - r) - 2r$, or $1 - 2r$ = **0.480** of the ideal eye of 2.
- PAM4 (levels ±1, ±1/3): $T$ = 35.71 ps, $r = e^{-2.693}$ = **0.0677**. Adjacent levels are $\tfrac23(1 - r)$ apart at the sampler, and the worst-case ISI is $r$ times the largest level, on each side. The eye is $\tfrac23(1 - r) - 2r$, a fraction $(1 - 4r)/3$ = **0.243** of NRZ's ideal eye.

**NRZ** is better, by $20\log_{10}(0.480/0.243)$ = **5.90** dB. A one-pole channel loses only 6 dB per octave, less than PAM4's 9.54 dB penalty.

(d) PAM4 fits three eyes into the same peak-to-peak swing, so each is a third as tall: $20\log_{10}3$ = **9.54** dB of SNR at equal peak amplitude and equal noise.

### Solution 5

(a) $E = A^2T = (2 \times 10^{-3})^2 \times 0.5 \times 10^{-6}$ = **2 × 10⁻¹²** V²·s, and $N_0 = 2 \times 10^{-14}$ V²/Hz, so $2E/N_0$ = **200**, **23.01** dB.

(b) With $x = T/\tau = 0.5$:

$$
\text{SNR}_{RC} = \frac{A^2(1 - e^{-x})^2}{N_0/(4\tau)}, \qquad \frac{\text{SNR}_{RC}}{2E/N_0} = \frac{4\tau(1 - e^{-x})^2}{2T} = \frac{2(1 - e^{-x})^2}{x} = 4(1 - e^{-0.5})^2 = \textbf{0.619},
$$

so $\text{SNR}_{RC}$ = **123.9**, **20.93** dB, a loss of **2.08** dB. This filter is too slow: its output has not risen far by $t = T$, so it loses signal. The best τ (17-05) loses 0.89 dB.

(c) $E_b/N_0 = 10^{0.9} = 7.943$. Antipodal: $Q(\sqrt{2 \times 7.943}) = Q(3.986)$ = **3.36 × 10⁻⁵**. Orthogonal: $Q(\sqrt{7.943}) = Q(2.818)$ = **2.41 × 10⁻³**, 3 dB worse in SNR and 72 times worse in error rate here.

(d) The noise has σ = $\sqrt{N_0/2}$ = 0.632. Choosing +1 when $0.7f(r \mid +1) > 0.3f(r \mid -1)$ gives

$$
r > t = \frac{N_0}{4}\ln\frac{0.3}{0.7} = 0.2 \times (-0.847) = \textbf{−0.169} .
$$

+1 is misread when $n < t - 1$: $Q(1.169/0.632) = Q(1.849)$ = **0.0322**. −1 is misread when $n > t + 1$: $Q(0.831/0.632) = Q(1.313)$ = **0.0946**. Then $P_e = 0.7 \times 0.0322 + 0.3 \times 0.0946$ = **0.0509**. ML (threshold 0): $Q(1/0.632) = Q(1.581)$ = **0.0569**. MAP moves the threshold toward the less likely symbol and cuts the error rate by about a tenth.

### Solution 6

(a) Bit rate $2 \times 25$ = **50** Mb/s; bandwidth $(1 + 0.2) \times 25$ = **30** MHz; η = **1.667** b/s/Hz. With Gray coding, QPSK has BPSK's bit-error rate: $Q(\sqrt{2 \times 5.012}) = Q(3.166)$ = **7.73 × 10⁻⁴**.

(b) $E_s/N_0 = 4 \times 10^{1.4} = 100.5$. Per dimension, $p = 2(1 - 1/4)Q(\sqrt{3E_s/(15N_0)}) = 1.5\,Q(4.483) = 1.5 \times 3.68 \times 10^{-6} = 5.53 \times 10^{-6}$. Then $P_s = 1 - (1 - p)^2$ = **1.11 × 10⁻⁵**. With Gray coding almost every symbol error flips one of four bits, so $P_b \approx P_s/4$ = **2.76 × 10⁻⁶**.

(c) $\text{SNR}_{\text{EVM}} = 1/\text{EVM}^2$: 4.5% gives **26.94** dB and 8% gives **21.94** dB.

(d) Noise-like impairments add in power, so $1/\text{SNR} = 1/316.2 + 0.05^2 = 0.003162 + 0.0025$, giving SNR = **176.6**, **22.47** dB. The transmitter's 26 dB of EVM-equivalent SNR costs the link 2.5 dB.

### Solution 7

(a) $H = -\sum p\log_2p = 0.35(1.515) + 0.25(2) + 0.20(2.322) + 0.12(3.059) + 0.08(3.644)$ = **2.153** bits. Huffman merges 0.08 + 0.12 = 0.20, then 0.20 + 0.20 = 0.40, then 0.25 + 0.35 = 0.60, then 0.40 + 0.60. Reading off the tree gives lengths (2, 2, 2, 3, 3) for (0.35, 0.25, 0.20, 0.12, 0.08), for example codewords 00, 01, 10, 110, 111. The average is $0.35 \cdot 2 + 0.25 \cdot 2 + 0.20 \cdot 2 + 0.12 \cdot 3 + 0.08 \cdot 3$ = **2.2** bits, an efficiency of 2.153/2.2 = **0.979**. A fixed-length code needs 3 bits.

(b) $H_b(0.05) = -0.05\log_20.05 - 0.95\log_20.95 = 0.2864$, so $C = 1 - 0.2864$ = **0.714** bits per channel use.

(c) $C = B\log_2(1 + \text{SNR}) = 10^7\log_2(1 + 31.62)$ = **50.28** Mb/s.

(d) At capacity, $\text{SNR} = \eta E_b/N_0$, so $\eta = \log_2(1 + \eta E_b/N_0)$ and $E_b/N_0 \ge (2^\eta - 1)/\eta$. At η = 3 this is 7/3 = 2.333, **3.68** dB. As η → 0 it tends to $\ln 2$, **−1.59** dB (Solution 13b).

### Solution 8

(a) Rate 4/7 = **0.571**; $d_{min}$ = **3**; $t$ = **1**. A block fails when two or more of its seven bits are in error:

$$
P_{block} = 1 - (1 - p)^7 - 7p(1 - p)^6 = \textbf{2.03 × 10⁻³},
$$

against $1 - 0.99^4$ = **0.0394** for four uncoded bits, 19 times better. This compares at equal channel bit-error rate; at equal $E_b/N_0$ each coded bit has only 4/7 of the energy, and the gain shrinks to the 0.58 dB of 17-08.

(b) A CRC of degree 16 detects **all bursts of 16 bits or fewer** (and every odd number of errors if its generator has the factor $x + 1$). Longer random patterns escape with probability about $2^{-16}$ = **1.53 × 10⁻⁵**.

(c) Soft: $10\log_{10}(Rd_{free}) = 10\log_{10}6$ = **7.78** dB. Hard decisions: $t = \lfloor(12 - 1)/2\rfloor = 5$, so $10\log_{10}(R(t + 1)) = 10\log_{10}3$ ≈ **4.77** dB, about 3 dB less.

(d) $t = (n - k)/2 = 32/2$ = **16** symbols. Overhead $255/223 - 1$ = **14.35**%. A burst of $b$ bits can touch $\lceil(b - 1)/8\rceil + 1$ symbols, so every burst up to $8(t - 1) + 1$ = **121** bits is corrected.

### Solution 9

(a) $L_{fs} = 20\log_{10}(4\pi d/\lambda)$ with λ = 0.3277 m: $20\log_{10}(4\pi \times 300/0.3277)$ = **81.22** dB. The received power is $20 - 81.22$ = **−61.22** dBm.

(b) $d_{BP} = 4h_th_r/\lambda = 4 \times 10 \times 1.5/0.1249$ = **480.3** m. Beyond it, $P_r/P_t = h_t^2h_r^2/d^4$, so $L = 40\log_{10}2000 - 20\log_{10}15 = 132.04 - 23.52$ = **108.5** dB. (The exact two-ray sum gives **108.7** dB: at only four times the breakpoint, $\sin x \approx x$ is still 0.2 dB optimistic.)

(c) $f_D = vf_c/c = 25 \times 2.6 \times 10^9/2.998 \times 10^8$ = **216.8** Hz, and $T_c = 1.521/(2\pi f_D) \approx 0.242/f_D$ = **1.117** ms. A 0.5 ms slot is shorter than $T_c$. The correlation across it is $J_0(2\pi f_D \times 0.5\ \text{ms})$ = **0.887**, so the fading is **slow** over the slot, but channel estimates must be refreshed every millisecond or so.

(d) With $\bar\gamma = 10^{2.5}$ = 316.2 and μ = $\sqrt{\bar\gamma/(1 + \bar\gamma)}$ = 0.998422, one antenna gives $\tfrac12(1 - \mu)$ = **7.89 × 10⁻⁴**, close to $1/(4\bar\gamma)$ = **7.91 × 10⁻⁴**. The sheet's $L$-branch formula with $L$ = 2 is $\big(\tfrac{1 - \mu}{2}\big)^2\big[1 + 2\cdot\tfrac{1 + \mu}{2}\big] = \big(\tfrac{1 - \mu}{2}\big)^2(2 + \mu)$ = **1.865 × 10⁻⁶**, against the approximation $\binom32(1/(4\bar\gamma))^2$ = **1.875 × 10⁻⁶**. Diversity gains a factor of **423** at 25 dB.

### Solution 10

(a) $T = 1/\Delta f$ = **66.67** µs; $T_{CP} = (144/2048)T$ = **4.69** µs. Overhead $T_{CP}/(T + T_{CP})$ = **6.57**%. Excess path $cT_{CP}$ = **1.41** km.

(b) $0.2 \times 10^{-6} \times 2.6 \times 10^9$ = **520** Hz, so ε = 520/30 000 = **0.0173**. ICI ≈ $(\pi\varepsilon)^2/3$ = 9.88 × 10⁻⁴, **−30.1** dB, a ceiling on the per-subcarrier SNR unless the offset is corrected.

(c) $\mathbf H$ is symmetric, with eigenvalues 1 ± 0.5, so its singular values are 1.5 and 0.5 and $\sigma^2$ = **2.25** and **0.25**. With power $\rho/2$ per antenna:

$$
C = \log_2(1 + 50 \times 2.25) + \log_2(1 + 50 \times 0.25) = 6.827 + 3.755 = \textbf{10.58}\ \text{b/s/Hz} .
$$

SISO with unit gain gives $\log_2 101$ = **6.66** b/s/Hz: the two layers raise capacity by 59%, even though the second eigenmode is weak.

(d) MRC: $(1.2 + 0.6) \times 10$ = 18, **12.55** dB. Alamouti: $(1.2 + 0.6) \times 10/2$ = 9, **9.54** dB. Both have diversity order 2. Alamouti is 3 dB behind because the transmitter splits its power without knowing the channel.

### Solution 11

(a) Slotted: $S = Ge^{-G} = 0.75e^{-0.75}$ = **0.354**. Pure: $S = Ge^{-2G} = 0.75e^{-1.5}$ = **0.167**, already past pure ALOHA's optimum at $G$ = 0.5, while slotted ALOHA is still climbing toward its optimum at $G$ = 1.

(b) Erlang B with $A$ = 3 and $c$ = 8, by the recursion $B(k) = AB(k - 1)/(k + AB(k - 1))$, gives **0.813**%. For 10 Erlangs: $B(17)$ = 1.29% and $B(18)$ = 0.714%, so **18** channels.

(c) $\text{SIR} = (\sqrt{3N})^n/6$. $N$ = 3 gives $3^{3.5}/6$ = 7.79, **8.92** dB, too low. $N$ = 4 gives $12^{1.75}/6$ = 12.9, **11.10** dB. The smallest valid cluster is **N = 4**.

(d) A block uses a second attempt with probability 0.2 and a third with probability $0.2^2$, so the mean number of transmissions is $1 + 0.2 + 0.04$ = **1.24**. It is delivered with probability $1 - 0.2^3 = 0.992$, so the throughput is $0.992/1.24$ = **0.8** of one attempt per block, which is $1 - p$ for any attempt limit (17-12). The residual failure is $0.2^3$ = **0.008**.

### Solution 12

(a) The L3 packet is 200 + 8 + 20 = 228 bytes, above the 46-byte minimum. On the wire: $8 + 14 + 228 + 4 + 12$ = **266** bytes, so the efficiency is 200/266 = **75.2**%.

(b) $2^{7} - 2 = 126 \ge 100$, but $2^6 - 2 = 62$ is too few, so the prefix is **/25** with **126** hosts, and the /20 holds $2^{25 - 20}$ = **32** of them.

(c) The limit is $8 \times 65\,535/0.08$ = **6.55** Mb/s. The BDP is $2.5 \times 10^9 \times 0.08/8$ = **25.0** MB. The shift must satisfy $65\,535 \times 2^s \ge 25 \times 10^6$: $2^8$ gives 16.8 MB and $2^9$ gives 33.6 MB, so the shift is **9**.

(d) Dijkstra from P, settling the closest unsettled router each time:

| Step | Settled | Tentative distances (Q, R, S, T) |
|---|---|---|
| 0 | P (0) | Q 3, R 1, S ∞, T ∞ |
| 1 | R (1) | Q min(3, 1 + 1) = 2, S 1 + 6 = 7, T 1 + 5 = 6 |
| 2 | Q (2) | S min(7, 2 + 2) = 4, T 6 |
| 3 | S (4) | T min(6, 4 + 1) = 5 |
| 4 | T (5) | — |

Distances: Q **2**, R **1**, S **4**, T **5**. The path to T is P–R–Q–S–T, so P forwards T-bound packets to **R**, its first hop, even though the direct-looking route P–R–T costs 6.

### Solution 13

(a) Let $s(t)$ have energy $E$ on $[0, T]$ and pass through $h(t)$. At $t = T$ the signal is $y_s(T) = \int h(\lambda)s(T - \lambda)\,d\lambda$. White noise of PSD $N_0/2$ gives output variance $(N_0/2)\int h^2(\lambda)\,d\lambda$ (17-01). So

$$
\text{SNR} = \frac{\big(\int h(\lambda)s(T - \lambda)\,d\lambda\big)^2}{(N_0/2)\int h^2(\lambda)\,d\lambda} \le \frac{\int h^2\,d\lambda\int s^2(T - \lambda)\,d\lambda}{(N_0/2)\int h^2\,d\lambda} = \frac{2E}{N_0},
$$

by the Cauchy–Schwarz inequality $(\int fg)^2 \le \int f^2\int g^2$. Equality holds if and only if $h(\lambda) = ks(T - \lambda)$ for a constant $k$: the filter is the time-reversed, delayed pulse. Its maximum SNR depends only on the pulse's energy, not its shape. ∎

(b) With signal power $P = E_bR_b$ and noise power $N_0B$, $\text{SNR} = (E_b/N_0)(R_b/B) = \eta E_b/N_0$. Reliable communication requires $R_b \le C$, i.e. $\eta \le \log_2(1 + \eta E_b/N_0)$, so

$$
\frac{E_b}{N_0} \ge \frac{2^\eta - 1}{\eta} = \frac{e^{\eta\ln2} - 1}{\eta} .
$$

The right side increases with η (its derivative has the sign of $e^x(x - 1) + 1 > 0$ for $x = \eta\ln 2 > 0$), so the smallest bound is its limit at η → 0. Expanding $e^{\eta\ln2} = 1 + \eta\ln2 + O(\eta^2)$ gives $(2^\eta - 1)/\eta \to \ln2$ = 0.693, or **−1.59** dB. No code at any bandwidth works below it. ∎

(c) Let the channel be $h[0..L - 1]$ and the block $x[0..N - 1]$, with the prefix $x[N - G..N - 1]$ sent first, $G \ge L - 1$. Index the transmitted stream so that $\tilde x[n] = x[n \bmod N]$ for $-G \le n \le N - 1$. The received sample at $0 \le n \le N - 1$ (after discarding the $G$ prefix samples) is

$$
y[n] = \sum_{l=0}^{L-1}h[l]\tilde x[n - l] = \sum_{l=0}^{L-1}h[l]x[(n - l) \bmod N],
$$

because $n - l \ge -(L - 1) \ge -G$ always lands inside the prefix or the block, where $\tilde x$ equals the periodic extension. No sample of the previous block enters, so there is no inter-block interference. This is the circular convolution $y = h \circledast x$. By the DFT's circular-convolution theorem (16-03), $Y[k] = H[k]X[k]$ with $H[k] = \sum_lh[l]e^{-j2\pi kl/N}$. Each subcarrier sees one complex gain, removed by a one-tap equalizer. ∎

### Solution 14

(a) The noise density is $-174 + 6$ = −168 dBm/Hz. At 1 Mb/s, $E_b/N_0 = P_r - N_0 - 10\log_{10}R_b = -137 + 168 - 60$ = **−29.0** dB. That is **27.4** dB below the Shannon limit of −1.59 dB, which no modulation or code can cross. The claim is physically impossible as stated.

(b) $C/N_0 = -137 + 168$ = 31 dB-Hz = **1259** Hz. At the Shannon limit, $R_b \le (C/N_0)/\ln2$ = **1816** b/s. At 5 dB, $1259/3.162$ = **398** b/s. A −137 dBm sensitivity is a few-hundred-bit-per-second number.

(c)

- Free space: $d = (\lambda/4\pi)10^{151/20}$ with λ = 0.3454 m, **975** km, far beyond the horizon; meaningless on the ground.
- Two-ray with 15 m and 1 m antennas: breakpoint 174 m, and $40\log_{10}d = 151 + 20\log_{10}15$ gives **23.1** km. With a 10 dB fade margin, **13.0** km.
- At 1 Mb/s and 5 dB, the sensitivity is $-174 + 60 + 6 + 5$ = **−103** dBm. The budget is 117 dB and the two-ray range **3.26** km (1.83 km with the margin).

So 20 km is plausible at hundreds of bits per second, and 1 Mb/s is plausible over a few kilometres, but not both at once.

(d) Rubric (3 points: 1 point for each well-chosen question paired with the condition that would make the claims consistent, up to 3; a strong answer usually offers four or more):

| Question to the founders | What would make the claims consistent |
|---|---|
| At what data rate, bandwidth and packet error rate was −137 dBm measured? | −137 dBm is the lowest-rate mode (hundreds of b/s), and 1 Mb/s is a different mode with its own, much higher sensitivity |
| What noise figure, modulation and code, and what $E_b/N_0$ does the demodulator need? | Numbers whose sum reproduces the sensitivity: $-174 + \text{NF} + 10\log_{10}R_b + E_b/N_0$ |
| Was the 20 km range measured, with what antenna heights, terrain and fade margin, and at what rate? | Line of sight from an elevated gateway at the lowest rate, with the margin stated |
| Is there antenna gain, diversity or a repetition/spreading gain hidden in "sensitivity"? | Processing gain counted explicitly and traded against rate |
| What do range and rate do to battery life (time on air per packet)? | A duty-cycle and energy-per-packet calculation at the long-range rate |
| What regulatory duty-cycle and power limits apply in the 868 MHz band? | A link budget that fits the transmit-power and duty-cycle limits of the target region |

A strong answer computes the Shannon-limit violation first, then shows that each claim is reachable separately (rate at short range, range at low rate) and asks which mode each number came from.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| X17.1a | autocorrelation amplitude A²/2 | 2 | V² |
| X17.1b | PSD line weight at ±1 kHz | 1 | V² |
| X17.1c | noise bandwidth | 15.71 | kHz |
| X17.1d | output noise variance | 3.142e-4 | V² |
| X17.1e | output noise rms | 17.72 | mV |
| X17.1f | correlation at 20 µs | 0.285 | — |
| X17.1g | spacing for correlation 0.1 | 36.65 | µs |
| X17.2a | cascade noise factor | 1.882 | — |
| X17.2b | cascade noise figure | 2.75 | dB |
| X17.2c | mixer term | 0.168 | — |
| X17.2d | IF-amplifier term | 0.302 | — |
| X17.2e | equivalent noise temperature | 255.8 | K |
| X17.2f | NF with filter in front | 4.75 | dB |
| X17.2g | sensitivity | -88.2 | dBm |
| X17.2h | Eb/N0 at 40 Mb/s | 6.99 | dB |
| X17.3a | deviation ratio | 4 | — |
| X17.3b | Carson bandwidth | 100 | kHz |
| X17.3c | carrier power fraction | 0.158 | — |
| X17.3d | power fraction inside Carson band | 0.995 | — |
| X17.3e | FM advantage over DSB (ratio) | 24 | — |
| X17.3f | FM advantage over DSB | 13.80 | dB |
| X17.3g | AM power efficiency | 0.111 | — |
| X17.3h | AM output SNR relative to DSB | -9.54 | dB |
| X17.4a | RC bandwidth of PAM4 | 18.2 | GHz |
| X17.4b | channel time constant | 13.26 | ps |
| X17.4c | r for NRZ | 0.260 | — |
| X17.4d | NRZ worst-case eye | 0.480 | — |
| X17.4e | r for PAM4 | 0.0677 | — |
| X17.4f | PAM4 worst-case eye (NRZ ideal = 1) | 0.243 | — |
| X17.4g | NRZ advantage | 5.90 | dB |
| X17.4h | PAM4 eye penalty | 9.54 | dB |
| X17.5a | pulse energy | 2e-12 | V²·s |
| X17.5b | matched-filter SNR | 200 | — |
| X17.5c | matched-filter SNR | 23.01 | dB |
| X17.5d | RC/matched SNR ratio | 0.619 | — |
| X17.5e | RC filter SNR | 123.9 | — |
| X17.5f | RC filter SNR | 20.93 | dB |
| X17.5g | RC filter loss | 2.08 | dB |
| X17.5h | antipodal BER at 9 dB | 3.36e-5 | — |
| X17.5i | orthogonal BER at 9 dB | 2.41e-3 | — |
| X17.5j | MAP threshold | -0.169 | — |
| X17.5k | P(error given +1) | 0.0322 | — |
| X17.5l | P(error given −1) | 0.0946 | — |
| X17.5m | MAP error probability | 0.0509 | — |
| X17.5n | ML error probability | 0.0569 | — |
| X17.6a | QPSK spectral efficiency | 1.667 | b/s/Hz |
| X17.6b | QPSK BER at 7 dB | 7.73e-4 | — |
| X17.6c | 16-QAM symbol-error probability | 1.11e-5 | — |
| X17.6d | 16-QAM BER | 2.76e-6 | — |
| X17.6e | SNR for 4.5% EVM | 26.94 | dB |
| X17.6f | SNR for 8% EVM | 21.94 | dB |
| X17.6g | effective SNR (ratio) | 176.6 | — |
| X17.6h | effective SNR | 22.47 | dB |
| X17.7a | entropy | 2.153 | bits |
| X17.7b | Huffman average length | 2.2 | bits |
| X17.7c | code efficiency | 0.979 | — |
| X17.7d | BSC capacity | 0.714 | bits/use |
| X17.7e | AWGN capacity | 50.28 | Mb/s |
| X17.7f | minimum Eb/N0 at 3 b/s/Hz | 3.68 | dB |
| X17.7g | Shannon limit | -1.59 | dB |
| X17.8a | Hamming rate | 0.571 | — |
| X17.8b | Hamming block-error probability | 2.03e-3 | — |
| X17.8c | four uncoded bits in error | 0.0394 | — |
| X17.8d | CRC-16 escape probability | 1.53e-5 | — |
| X17.8e | soft coding gain | 7.78 | dB |
| X17.8f | hard coding gain (approx.) | 4.77 | dB |
| X17.8g | RS correctable symbols | 16 | — |
| X17.8h | RS overhead | 14.35 | % |
| X17.8i | longest burst corrected | 121 | bits |
| X17.9a | free-space path loss | 81.22 | dB |
| X17.9b | received power | -61.22 | dBm |
| X17.9c | two-ray breakpoint | 480.3 | m |
| X17.9d | two-ray loss at 2 km (d⁴ law) | 108.5 | dB |
| X17.9d2 | two-ray loss at 2 km (exact sum) | 108.7 | dB |
| X17.9e | Doppler shift | 216.8 | Hz |
| X17.9f | coherence time | 1.117 | ms |
| X17.9g | correlation over 0.5 ms | 0.887 | — |
| X17.9h | Rayleigh BPSK BER | 7.89e-4 | — |
| X17.9i | 1/(4γ̄) | 7.91e-4 | — |
| X17.9j | two-branch MRC BER | 1.865e-6 | — |
| X17.9k | two-branch approximation | 1.875e-6 | — |
| X17.9l | diversity factor at 25 dB | 423 | — |
| X17.10a | useful symbol | 66.67 | µs |
| X17.10b | cyclic prefix | 4.69 | µs |
| X17.10c | CP overhead | 6.57 | % |
| X17.10d | excess path absorbed | 1.41 | km |
| X17.10e | frequency offset | 520 | Hz |
| X17.10f | normalized offset | 0.0173 | — |
| X17.10g | ICI power | -30.1 | dB |
| X17.10h | 2×2 capacity | 10.58 | b/s/Hz |
| X17.10i | SISO capacity | 6.66 | b/s/Hz |
| X17.10j | MRC SNR | 12.55 | dB |
| X17.10k | Alamouti SNR | 9.54 | dB |
| X17.11a | slotted ALOHA throughput | 0.354 | — |
| X17.11b | pure ALOHA throughput | 0.167 | — |
| X17.11c | Erlang B, 8 channels, 3 E | 0.813 | % |
| X17.11d | channels for 10 E at 1% | 18 | — |
| X17.11e | SIR, N = 3 | 8.92 | dB |
| X17.11f | SIR, N = 4 | 11.10 | dB |
| X17.11g | mean HARQ transmissions | 1.24 | — |
| X17.11g2 | HARQ throughput | 0.8 | — |
| X17.11h | residual failure after three | 0.008 | — |
| X17.12a | wire bytes | 266 | bytes |
| X17.12b | UDP efficiency | 75.2 | % |
| X17.12c | prefix length | 25 | — |
| X17.12d | subnets in the /20 | 32 | — |
| X17.12e | window-limited throughput | 6.55 | Mb/s |
| X17.12f | bandwidth-delay product | 25.0 | MB |
| X17.12g | window shift count | 9 | — |
| X17.12h | distance to Q | 2 | — |
| X17.12i | distance to R | 1 | — |
| X17.12j | distance to S | 4 | — |
| X17.12k | distance to T | 5 | — |
| X17.14a | implied Eb/N0 | -29.0 | dB |
| X17.14b | gap to the Shannon limit | 27.4 | dB |
| X17.14c | C/N0 | 1259 | Hz |
| X17.14d | rate at the Shannon limit | 1816 | b/s |
| X17.14e | rate at 5 dB | 398 | b/s |
| X17.14f | free-space range | 975 | km |
| X17.14g | two-ray range | 23.1 | km |
| X17.14h | two-ray range with margin | 13.0 | km |
| X17.14i | sensitivity at 1 Mb/s | -103 | dBm |
| X17.14j | two-ray range at 1 Mb/s | 3.26 | km |
| X17.3i | FM bandwidth | 100 | kHz |
| X17.3j | DSB bandwidth | 20 | kHz |
| X17.4i | NRZ symbol rate | 56 | GBd |
| X17.4j | NRZ Nyquist frequency | 28 | GHz |
| X17.4k | PAM4 symbol rate | 28 | GBd |
| X17.4l | PAM4 Nyquist frequency | 14 | GHz |
| X17.5o | orthogonal-to-antipodal BER ratio at 9 dB | 72 | — |
| X17.6i | QPSK bit rate | 50 | Mb/s |
| X17.6j | QPSK occupied bandwidth | 30 | MHz |
| X17.8j | Hamming improvement factor | 19 | — |
| X17.10l | 2×2 gain over SISO | 59 | % |
| X17.12l | usable hosts per subnet | 126 | — |
| X17.14k | two-ray breakpoint, 868 MHz | 174 | m |
| X17.14l | link budget at 1 Mb/s | 117 | dB |
| X17.14m | two-ray range at 1 Mb/s with margin | 1.83 | km |
