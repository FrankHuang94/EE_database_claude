# Solutions 17-10 · OFDM

Problems: [17-10 problems](../problems/17-10-problems.md) · Chapter: [17-10](../chapters/17-10-ofdm.md). Every number below is recomputed by [verify_17_10.py](../verify/verify_17_10.py), with simulation cross-checks where a formula is approximate.

---

## Solutions

### Solution 17-10.1

$\int_0^{0.9T}e^{j2\pi t/T}dt = \frac{T}{j2\pi}(e^{j1.8\pi} - 1)$, of magnitude $\frac{T}{2\pi}|e^{j1.8\pi} - 1| = \frac{T}{2\pi} \times 2\sin(0.9\pi) = 0.0984T$. Normalized by $0.9T$: **0.109**, or **−19.2** dB of leakage between neighbours. Over the full symbol the integrand completes one cycle and the result is **0**. A window error of 10% turns orthogonal subcarriers into strongly coupled ones, which is why the prefix must also absorb timing error.

### Solution 17-10.2

$\Delta f = 20\,\text{MHz}/64$ = **312.5** kHz, $T = 1/\Delta f$ = **3.2** μs, guard fraction $0.8/(3.2 + 0.8)$ = **20** %.

### Solution 17-10.3

$T_{CP} = (144/2048)T$ with $T = 1/(15 \times 2^\mu\,\text{kHz})$. μ = 2: $T$ = 16.67 μs, $T_{CP}$ = **1.17** μs. μ = 3: $T_{CP}$ = 0.586 μs, covering $c \times 0.586\,\mu\text{s}$ = **176** m of excess path.

### Solution 17-10.4

The receiver discards the prefix's energy, so $E_b/N_0$ falls by $10\log_{10}(1 + T_{CP}/T)$. NR: $10\log_{10}(2192/2048)$ = **0.30** dB. 20% guard ($T_{CP}/T$ = 0.25): $10\log_{10}1.25$ = **0.97** dB.

### Solution 17-10.5

$(\pi\varepsilon)^2/3 \le 10^{-3.5}$ gives $\varepsilon \le \sqrt{3 \times 10^{-3.5}}/\pi$ = **0.0098**, so the residual error must be below $0.0098 \times 30$ kHz = **294** Hz, or **0.084** ppm at 3.5 GHz: far tighter than any free-running crystal, so the receiver must track frequency.

### Solution 17-10.6

$(\pi f_D/\Delta f)^2/6 \le 10^{-3}$: $f_D \le \sqrt{6 \times 10^{-3}} \times 120\,\text{kHz}/\pi$ = **2959** Hz. At 28 GHz, $v = f_Dc/f_c$ = 31.7 m/s = **114** km/h.

### Solution 17-10.7

$\gamma = -\ln\big(1 - (1 - p)^{1/256}\big)$: $p = 10^{-4}$ gives **11.69** dB; $p = 10^{-2}$ gives **10.06** dB. A factor of 100 in probability moves the PAPR by only 1.6 dB, because the exponential tail is steep.

### Solution 17-10.8

$(4096/2) \times 12$ = **24 576** complex multiplications per symbol; at 28 000 symbols/s, **6.88e8** per second per antenna, before the receiver's channel estimation and decoding.

### Solution 17-10.9

Subcarrier SNR $= |H_k|^2 \times 100 = 1$, **0** dB, after ZF as before it. QPSK at $E_s/N_0$ = 1: $1 - (1 - Q(1))^2$ = **0.292**. MMSE multiplies by $H_k^*/(|H_k|^2 + 0.01)$, a positive real multiple of $1/H_k$ (here 0.5), so the decision regions of QPSK (which depend only on signs) give **identical** decisions; for 16-QAM the scaling must be undone first. The remedy for a notched subcarrier is coding across subcarriers or not loading it, not a different one-tap equalizer.

### Solution 17-10.10

$106 \times 12$ = 1272 subcarriers × 14 symbols per 1 ms slot = $17.81 \times 10^6$ resource elements/s. Rate: $17.81 \times 10^6 \times 6 \times 0.75 \times 0.86$ = **68.9** Mb/s, **3.45** b/s/Hz.

### Solution 17-10.11

The prefix must exceed about $3\tau_{rms}$, so it covers links with $\tau_{rms} < T_{CP}/3$. At 30 kHz: $\log_{10}(2.344\,\mu\text{s}/3) = -6.107$; $z = (-6.107 + 6.57)/0.39 = 1.19$, so **88.4** % of links (using the unrounded mean $-6.4700 - 0.134\log_{10}6 = -6.5743$). At 15 kHz ($T_{CP}$ = 4.69 μs): **97.6** %. 99th percentile: $10^{-6.5743 + 2.326 \times 0.39}$ = **2.15** μs. The tail of the delay-spread distribution, not its median of 0.27 μs, sets the prefix, which is why wide-area deployments favour 15 or 30 kHz.

### Solution 17-10.12

$T_{CP}$ = 144/2048 of the FFT length: $4096 \times 144/2048$ = **288** samples at 122.88 MHz. The phase $2\pi\varepsilon$ is unambiguous for $|2\pi\varepsilon| < \pi$, so $|\varepsilon| <$ **0.5**, half a subcarrier spacing; larger offsets need a coarse integer-offset search (for example on synchronization signals).

### Solution 17-10.13

$\sin(\pi\varepsilon)/(N\sin(\pi\varepsilon/N)) \approx \sin(\pi\varepsilon)/(\pi\varepsilon) = \text{sinc}\,\varepsilon$ for large $N$, and $\text{sinc}^2\varepsilon = \big(1 - (\pi\varepsilon)^2/6 + \dots\big)^2 = 1 - (\pi\varepsilon)^2/3 + O(\varepsilon^4)$. So $P_{ICI} = 1 - \text{sinc}^2\varepsilon \approx (\pi\varepsilon)^2/3$. For $N$ = 64, ε = 0.2: exact **0.1248** (−9.04 dB), approximation **0.1316** (−8.81 dB): the approximation overstates ICI by 0.23 dB at this large offset.

### Solution 17-10.14

With DFT size $M = N$, the transmitter computes $x = \text{IFFT}_N(\text{FFT}_N(s)) = s$ (with consistent normalization): the samples are exactly the original QAM symbols, a single-carrier waveform. For QPSK all samples have the same magnitude, so the Nyquist-sampled PAPR is **0** dB. With $M < N$ (a contiguous allocation of a fraction of the band) the IFFT interpolates between the symbols with a sinc-like kernel, which creates modest peaks between samples: the several-decibel advantage over OFDM in §3.6 rather than a perfect 0 dB.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-10.1a | correlation over 0.9 T | 0.109 | — |
| 17-10.1b | leakage in dB | −19.2 | dB |
| 17-10.1c | correlation over T | 0 | — |
| 17-10.2a | subcarrier spacing | 312.5 | kHz |
| 17-10.2b | useful symbol | 3.2 | μs |
| 17-10.2c | guard fraction | 20 | % |
| 17-10.3a | prefix at μ = 2 | 1.17 | μs |
| 17-10.3b | excess path at μ = 3 | 176 | m |
| 17-10.4a | NR prefix penalty | 0.30 | dB |
| 17-10.4b | 20% guard penalty | 0.97 | dB |
| 17-10.5a | largest ε | 0.0098 | — |
| 17-10.5b | largest frequency error | 294 | Hz |
| 17-10.5c | largest error in ppm | 0.084 | ppm |
| 17-10.6a | largest Doppler | 2959 | Hz |
| 17-10.6b | speed at 28 GHz | 114 | km/h |
| 17-10.7a | PAPR at 1e-4 | 11.69 | dB |
| 17-10.7b | PAPR at 1e-2 | 10.06 | dB |
| 17-10.8a | multiplications per symbol | 24576 | — |
| 17-10.8b | multiplications per second | 6.88e8 | 1/s |
| 17-10.9a | subcarrier SNR | 0 | dB |
| 17-10.9b | QPSK symbol-error rate | 0.292 | — |
| 17-10.10a | information rate | 68.9 | Mb/s |
| 17-10.10b | spectral efficiency | 3.45 | b/s/Hz |
| 17-10.11a | links covered at 30 kHz | 88.4 | % |
| 17-10.11b | links covered at 15 kHz | 97.6 | % |
| 17-10.11c | 99th-percentile delay spread | 2.15 | μs |
| 17-10.12a | prefix length | 288 | samples |
| 17-10.12b | unambiguous offset | 0.5 | — |
| 17-10.13a | exact ICI | 0.1248 | — |
| 17-10.13b | approximate ICI | 0.1316 | — |
| 17-10.14a | Nyquist-sampled PAPR | 0 | dB |
