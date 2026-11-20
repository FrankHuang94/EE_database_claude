# Solutions 17-06 · Bandpass Digital Modulation and BER

Problems: [17-06 problems](../problems/17-06-problems.md) · Chapter: [17-06](../chapters/17-06-bandpass-digital-modulation.md). Every number below is recomputed by [verify_17_06.py](../verify/verify_17_06.py): constellation statistics by enumeration, error rates in closed form, by Craig's integral and by Monte Carlo, and EVM by simulating impaired transmitters.

---

## Solutions

### Solution 17-06.1

Matching $s = I\cos\omega_ct - Q\sin\omega_ct$ term by term: $I$ = **3** and $-Q = 4$, so $Q$ = **−4**. The complex envelope is $3 - 4j$, the amplitude $\sqrt{9 + 16}$ = **5**, and the phase $\arctan(-4/3)$ = **−53.13°**. The sign convention matters: a "+sin" term is a negative Q.

### Solution 17-06.2

With $E_s = 2$ the points are $(\pm1, \pm1)$. Gray labels: (+1, +1) → 00, (−1, +1) → 10, (−1, −1) → 11, (+1, −1) → 01 (first bit sets the sign of I, second the sign of Q). Adjacent points are 2 apart, so $d_{min}$ = **2**; they differ in one bit. Diagonal points (distance $2\sqrt2$) differ in **both** bits, but diagonal errors are rare at useful SNRs.

### Solution 17-06.3

$\eta = \log_2M/(1 + \alpha)$: 1024-QAM, $10/1.05$ = **9.52** b/s/Hz; 16-QAM, $4/1.35$ = **2.96** b/s/Hz.

### Solution 17-06.4

$E_s/N_0 = 63.1$. Nearest neighbours: $2Q(\sqrt{126.2}\sin(\pi/8)) = 2Q(4.30)$ = **1.72 × 10⁻⁵**; Craig's integral gives the same to three digits, because at this SNR only the two nearest neighbours matter. Per bit, $E_b/N_0 = 18 - 10\log_{10}3$ = **13.23** dB.

### Solution 17-06.5

In each dimension the levels ±1, ±3, ±5, ±7 have mean square $(1 + 9 + 25 + 49)/4 = 21$, so $E_s = 2 \times 21$ = **42**, matching $2(M - 1)/3$. The corner (7, 7) has energy 98, so the peak-to-average ratio is $98/42$, **3.68** dB. At $E_s/N_0$ = 25 dB (316.2), $p = 2(1 - 1/8)Q(\sqrt{3 \times 316.2/63}) = 1.75\,Q(3.880)$ and $P_s = 1 - (1 - p)^2$ = **1.82 × 10⁻⁴**.

### Solution 17-06.6

At high SNR each symbol error goes to a neighbour, each boundary equally often. With natural labels, the boundaries −3|−1, −1|1 and 1|3 separate 00|01 (1 bit), 01|10 (2 bits) and 10|11 (1 bit): an average of 4/3 bits per error. Gray labels change exactly 1 bit at every boundary. The natural-label BER is therefore higher by a factor of **1.33**.

### Solution 17-06.7

$10^{-25/20}$ = **5.62**%. 8% EVM is $-20\log_{10}0.08$ = **21.94** dB. Combined: the noise powers add, $0.03^2 + 10^{-3} = 1.9 \times 10^{-3}$, so the SNR is $1/(1.9 \times 10^{-3})$, **27.21** dB, almost 3 dB below the receiver's own 30 dB because the transmitter's 3% (30.5 dB) is comparable.

### Solution 17-06.8

A phase error φ moves a point of radius $r$ by $r\lvert e^{j\phi} - 1\rvert$, with $\lvert e^{j\phi} - 1\rvert^2 = 2 - 2\cos\phi$. For Gaussian φ with rms σ, $\mathbb{E}[\cos\phi] = e^{-\sigma^2/2}$, so $\text{EVM}^2 = 2 - 2e^{-\sigma^2/2} \approx \sigma^2$. With σ = 2° = 0.0349 rad, EVM = **3.49**%, an equivalent SNR of **29.14** dB, only just inside NR's 3.5% limit for 256-QAM on its own and far outside the 2.5% for 1024-QAM. For QAM the outer points move more than the inner ones; the rms over the constellation is the same, $\sigma$ times the rms radius, to first order.

### Solution 17-06.9

$\tfrac12e^{-E_b/N_0} = 10^{-6}$ gives $E_b/N_0 = \ln(5 \times 10^5) = 13.12$, **11.18** dB. BPSK needs 10.53 dB: DPSK costs **0.65** dB here, less than the 0.75 dB at $10^{-5}$; the penalty shrinks as the SNR rises.

### Solution 17-06.10

$\Delta f = h/T = 0.5 \times 1$ MHz = **500** kHz, so the two tones sit at ±**250** kHz from the carrier. Bluetooth LE's 1 Mb/s PHY uses GFSK with an index near 0.5, the MSK spacing; its test specification checks an average deviation between 225 and 275 kHz for a pattern of alternating bits ([R-278], secondary), consistent with ±250 kHz.

### Solution 17-06.11

In one dimension the $L = \sqrt M$ levels have mean square $(L^2 - 1)/3$ (17-04 §3.1); two independent dimensions double it: $E_s = 2(L^2 - 1)/3 = 2(M - 1)/3$. The minimum distance is the level spacing, 2. With $E_b = E_s/\log_2M$,

$$
\frac{d_{min}^2}{4E_b} = \frac{4}{4 \cdot 2(M - 1)/(3\log_2M)} = \frac{3\log_2M}{2(M - 1)} .
$$

For $M = 4$: $3 \times 2/(2 \times 3)$ = **1**: 4-QAM is QPSK, whose bits ride on antipodal BPSK in each dimension.

### Solution 17-06.12

With $E_s = 1$ the distances to the other points are $d_k = 2\sin(k\pi/8)$ for $k$ = 1, 2, 3 (two points each) and 4 (one point). The full union bound is

$$
\sum_{k=1}^{3}2Q\Big(\frac{d_k}{\sqrt{2N_0}}\Big) + Q\Big(\frac{d_4}{\sqrt{2N_0}}\Big) = \textbf{2.3395} \times 10^{-3}
$$

at $E_s/N_0$ = 15 dB, against the nearest-neighbour **2.3395 × 10⁻³** and Craig's exact **2.3395 × 10⁻³**: the farther points add only about $2 \times 10^{-8}$ (the second neighbours, $2Q(5.62)$), in the sixth significant figure; the exact value differs from the nearest-neighbour term by far less still.

### Solution 17-06.13

From Problem 17-03.13, the image (unwanted sideband) power relative to the wanted signal is $(1 - 2g\cos\varepsilon + g^2)/(1 + 2g\cos\varepsilon + g^2)$ with $g$ = 1.01 and ε = 1°: **−39.96** dB. For random data the image term behaves like an independent error of that relative power, so the EVM is its square root, **1.00**%, an equivalent SNR of 39.96 dB: harmless for 256-QAM but a visible share of a 1024-QAM budget. Real transceivers calibrate I/Q imbalance to keep this term well below the oscillator's phase-noise contribution.

### Solution 17-06.14

Solving $P_s = 10^{-3}$ numerically:

- QPSK ($2q - q^2$): **10.35** dB;
- 16-QAM: **17.63** dB;
- 64-QAM: **23.97** dB;
- 256-QAM: **30.08** dB.

At 18 dB the modem picks **16-QAM**. The symbol rate is $20/1.25 = 16$ Msymbol/s, so the bit rate is $4 \times 16$ = **64** Mb/s before coding. (Real modems use coded thresholds, several dB lower, and a finer grid of code rates.)

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 17-06.1a | I | 3 | — |
| 17-06.1b | Q | −4 | — |
| 17-06.1c | amplitude | 5 | — |
| 17-06.1d | phase | −53.13 | ° |
| 17-06.2a | QPSK minimum distance, Es = 2 | 2 | — |
| 17-06.3a | 1024-QAM, α = 0.05 | 9.52 | b/s/Hz |
| 17-06.3b | 16-QAM, α = 0.35 | 2.96 | b/s/Hz |
| 17-06.4a | 8-PSK SER at 18 dB | 1.72e-5 | — |
| 17-06.4b | Eb/N0 | 13.23 | dB |
| 17-06.5a | 64-QAM Es | 42 | — |
| 17-06.5b | 64-QAM peak-to-average | 3.68 | dB |
| 17-06.5c | 64-QAM SER at 25 dB | 1.82e-4 | — |
| 17-06.6a | natural/Gray BER ratio | 1.33 | — |
| 17-06.7a | EVM for −25 dB | 5.62 | % |
| 17-06.7b | SNR for 8% EVM | 21.94 | dB |
| 17-06.7c | combined SNR | 27.21 | dB |
| 17-06.8a | EVM from 2° phase noise | 3.49 | % |
| 17-06.8b | equivalent SNR | 29.14 | dB |
| 17-06.9a | DPSK Eb/N0 for 1e-6 | 11.18 | dB |
| 17-06.9b | penalty over BPSK | 0.65 | dB |
| 17-06.10a | tone spacing | 500 | kHz |
| 17-06.10b | peak deviation | 250 | kHz |
| 17-06.11a | figure of merit for M = 4 | 1 | — |
| 17-06.12a | full union bound | 2.3395e-3 | — |
| 17-06.12b | nearest-neighbour approximation | 2.3395e-3 | — |
| 17-06.12c | Craig exact | 2.3395e-3 | — |
| 17-06.13a | image ratio | −39.96 | dB |
| 17-06.13b | EVM | 1.00 | % |
| 17-06.14a | QPSK threshold | 10.35 | dB |
| 17-06.14b | 16-QAM threshold | 17.63 | dB |
| 17-06.14c | 64-QAM threshold | 23.97 | dB |
| 17-06.14d | 256-QAM threshold | 30.08 | dB |
| 17-06.14e | bit rate at 18 dB | 64 | Mb/s |
