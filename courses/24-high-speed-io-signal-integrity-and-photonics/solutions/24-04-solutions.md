# Solutions 24-04 · DSP-Based SerDes and FEC

Problems: [24-04 problems](../problems/24-04-problems.md) · Chapter: [24-04](../chapters/24-04-dsp-serdes-and-fec.md)

Every number is recomputed by [verify_24_04.py](../verify/verify_24_04.py).

---

## Solutions

### Solution 24-04.1

(a) $\Delta = 2.5/2^7$ = **0.0195**.

(b) $\sigma_q = 0.0195/\sqrt{12}$ = **0.00564**.

(c) $20\log_{10}(0.7454/0.00564)$ = **42.4** dB.

(d) $(1/3)/0.00564$ = **59.1**.

One more bit and a full scale 17% smaller (headroom above the outer level halved, from 50% to 25%) gain 7.6 dB over the 6-bit design of Example 24-04.1, but the smaller headroom risks clipping when ISI is large.

### Solution 24-04.2

(a) $\sigma_t = 10^{-30/20}/(2\pi \times 53.125 \times 10^9)$ = **94.7** fs.

(b) $10^{-38/20}/(2\pi \times 26.5625 \times 10^9)$ = **75.4** fs.

### Solution 24-04.3

(a) The noise powers relative to the signal are $10^{-3.0}$, $10^{-3.48}$ and $10^{-3.56}$; their sum gives $-10\log_{10}(\ldots)$ = **27.9** dB.

(b) Without thermal noise and crosstalk: **32.2** dB. Without quantization: **28.9** dB. Without jitter: **28.8** dB.

The 30 dB term dominates, so improving it pays most. A better ADC or clock gains about a decibel at most, because the total can never exceed the worst single term.

### Solution 24-04.4

(a) $106.25/128$ = **0.830** GS/s.

(b) At multiples of $f_s/M$ = **0.830** GHz.

(c) $10^{-32/20}/(2\pi \times 26.5625 \times 10^9)$ = **151** fs.

### Solution 24-04.5

(a) $40 \times 106.25 \times 10^9 \times 30 \times 10^{-15}$ = **127.5** mW.

(b) $16 \times 106.25 \times 10^9 \times 10 \times 10^{-15}$ = **17.0** mW.

(c) $(127.5 + 17.0)\ \text{mW}/212.5\ \text{Gb/s}$ = **0.68** pJ/b, of which the FFE is 0.60 and the MLSD 0.08.

The FFE dominates because it runs 40 operations per symbol; trimming taps saves more than simplifying the detector.

### Solution 24-04.6

(a) A single error gives $4(1 + 0.75^2)$ = **6.25**. An exhaustive search over error events up to 7 symbols long finds nothing closer, so the gain is $10\log_{10}(6.25/4)$ = **1.94** dB.

(b) A single error gives $4(1 + 0.25 + 0.0625)$ = **5.25**. The double error (2, −2) gives $(2, -1, -0.5, -0.5)$, with $d^2$ = 5.5, larger; the search again finds the single error closest. The gain is **1.18** dB.

### Solution 24-04.7

(a) $4^3$ = **64** states and $4^4$ = **256** branches per symbol.

(b) $2^3$ = **8** states and $2^4$ = **16** branches.

(c) $16 \times 106.25 \times 10^9$ = **1.7** × 10¹² updates per second.

### Solution 24-04.8

(a) $4 \times 25.6$ = **102.4** ns.

(b) $102.4 + 100$ = **202** ns.

(c) $202.4 + 56$ = **258** ns.

### Solution 24-04.9

$Q^{-1}(10^{-3})$ = 3.090 and $Q^{-1}(10^{-15})$ = 7.941, so NCG = $20\log_{10}(7.941/3.090) + 10\log_{10}0.9$ = **7.74** dB, about 0.9 dB more than KP4 for nearly twice the overhead.

### Solution 24-04.10

(a) $200 \times (257/256) \times (544/514)$ = **212.5** Gb/s, or **106.25** GBd in PAM4.

(b) $2 \times 113.4375/200 - 1$ = **13.4** %.

(c) $212.5/200 - 1$ = **6.25** %.

### Solution 24-04.11

(a) $16 \times 64 \times 10^9/2048$ = **5.0** × 10⁸ flits per second.

(b) $5 \times 10^8 \times 5 \times 10^{-6}$ = **2,500** retries per second.

(c) $1 - (1 - 10^{-6})^{2048}$ = **2.0** × 10⁻³.

The FEC corrects almost all of the 2 errored flits in a thousand. The remaining 5 in a million are retried, about 2,500 a second, each costing about 100 ns.

### Solution 24-04.12

(a) A burst of $b$ bits touches at most $\lceil(b - 1)/10\rceil + 1$ symbols. Fifteen symbols are always corrected when $(b - 1)/10 \le 14$, so $b$ = **141** bits.

(b) Round-robin interleaving gives each codeword at most a quarter of the symbols touched, rounded up, so up to 60 symbols are corrected: $b = 59 \times 10 + 1$ = **591** bits.

### Solution 24-04.13

(a) $4 \times 151$ = **604** ns.

(b) $4 \times 2.0$ = **8** ns.

Six hundred nanoseconds is more than a DRAM access, which is why a memory-semantic fabric cannot use Ethernet's standard FEC unchanged.

### Solution 24-04.14

(a) The error is $e_n = c_0x_n + c_1x_{n-1} - a_n$. Setting $\partial E[e_n^2]/\partial c_i = 0$ gives $\mathbf R\mathbf c = \mathbf p$ with $R_{ij} = E[x_{n-i}x_{n-j}]$ and $p_i = E[x_{n-i}a_n]$. Here $E[x_n^2] = 1 + 0.25 + 0.01$ = **1.26**, $E[x_nx_{n-1}] = E[(a_n + 0.5a_{n-1})(a_{n-1} + 0.5a_{n-2})]$ = **0.5**, and $\mathbf p = (1, 0)$. So

$$
\begin{pmatrix}1.26 & 0.5\\ 0.5 & 1.26\end{pmatrix}\begin{pmatrix}c_0\\ c_1\end{pmatrix} = \begin{pmatrix}1\\ 0\end{pmatrix},
$$

with determinant **1.3376**: $c_0 = 1.26/1.3376$ = **0.942** and $c_1 = -0.5/1.3376$ = **−0.374**.

(b) At the optimum, $E[e_n^2] = 1 - \mathbf p^T\mathbf c = 1 - c_0$ = **0.0580**.

(c) With (1, −0.5) the combined response is $(1, 0, -0.25)$: residual ISI of variance $0.25^2$ = **0.0625** plus noise $(1 + 0.25) \times 0.01$ = 0.0125, a total of **0.075**. MMSE accepts a little ISI (it does not fully cancel the post-cursor) to amplify the noise less, and its total error is lower.

### Solution 24-04.15

(a) Each state is the current symbol; a branch from $a_{n-1}$ to $a_n$ costs $(y_n - a_n - 0.5a_{n-1})^2$, and each state keeps the cheaper of its two incoming paths. Starting from state +1 (metric 0):

| $n$ | $y_n$ | metric of state +1 (from) | metric of state −1 (from) |
|---|---|---|---|
| 0 | 1.6 | **0.01** (+1) | **4.41** (+1) |
| 1 | 0.4 | **1.22** (+1) | **0.82** (+1) |
| 2 | −1.3 | **4.06** (−1) | **0.86** (−1) |
| 3 | −0.7 | **2.30** (−1) | **1.50** (−1) |

(b) State −1 ends cheapest (**1.50**). Tracing back: −1 ← −1 ← −1 ← +1, so the sequence is (+1, −1, −1, −1).

(c) A slicer decides on the sign of $y_n$: (+1, +1, −1, −1), wrong at $n$ = 1 because the post-cursor of the first +1 lifted $y_1$. The DFE subtracts $0.5\hat a_{n-1}$ and gets (+1, −1, −1, −1), the same as Viterbi here; the two differ only when noise makes a DFE decision wrong and the error propagates.

### Solution 24-04.16

(a) $p_s = 1 - (1 - 2.4 \times 10^{-4})^{10}$ = **2.40 × 10⁻³**.

(b) $544 \times p_s$ = **1.30** symbol errors per codeword.

(c) $P(N > 15) = \sum_{k=16}^{544}\binom{544}{k}p_s^k(1 - p_s)^{544 - k}$ = **8.2 × 10⁻¹³**. Uncorrectable codewords are rare at this input, but bursts (several bit errors in one symbol or neighbouring symbols) raise the rate, which is why burst behaviour matters for FEC design.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 24-04.1a | step | 0.0195 | |
| 24-04.1b | quantization noise | 0.00564 | |
| 24-04.1c | SQNR | 42.4 | dB |
| 24-04.1d | half-eye ratio | 59.1 | |
| 24-04.1e | gain over the 6-bit design | 7.6 | dB |
| 24-04.1e1 | headroom reduction | 17 | % |
| 24-04.2a | jitter for 30 dB at 53.125 GHz | 94.7 | fs |
| 24-04.2b | jitter for 38 dB at 26.5625 GHz | 75.4 | fs |
| 24-04.3a | total SNR | 27.9 | dB |
| 24-04.3b | without thermal noise | 32.2 | dB |
| 24-04.3b1 | without quantization | 28.9 | dB |
| 24-04.3b2 | without jitter | 28.8 | dB |
| 24-04.4a | slice rate | 0.830 | GS/s |
| 24-04.4b | offset spur spacing | 0.830 | GHz |
| 24-04.4c | skew for 32 dB | 151 | fs |
| 24-04.5a | FFE power | 127.5 | mW |
| 24-04.5b | MLSD power | 17.0 | mW |
| 24-04.5c | energy per bit | 0.68 | pJ/b |
| 24-04.5c1 | FFE energy per bit | 0.60 | pJ/b |
| 24-04.5c2 | MLSD energy per bit | 0.08 | pJ/b |
| 24-04.6a | distance, (1, 0.75) | 6.25 | |
| 24-04.6a1 | gain, (1, 0.75) | 1.94 | dB |
| 24-04.6b | distance, (1, 0.5, 0.25) | 5.25 | |
| 24-04.6b1 | double-error distance | 5.5 | |
| 24-04.6b2 | gain, (1, 0.5, 0.25) | 1.18 | dB |
| 24-04.7a | PAM4 states | 64 | |
| 24-04.7a1 | PAM4 branches | 256 | |
| 24-04.7b | NRZ states | 8 | |
| 24-04.7b1 | NRZ branches | 16 | |
| 24-04.7c | updates per second | 1.7e12 | |
| 24-04.8a | accumulation | 102.4 | ns |
| 24-04.8b | total without inner code | 202 | ns |
| 24-04.8c | total with inner code | 258 | ns |
| 24-04.9a0 | inverse Q at 1e-3 | 3.090 | |
| 24-04.9a | NCG | 7.74 | dB |
| 24-04.9b | advantage over KP4 | 0.9 | dB |
| 24-04.10a | bit rate | 212.5 | Gb/s |
| 24-04.10a1 | symbol rate | 106.25 | GBd |
| 24-04.10b | total overhead | 13.4 | % |
| 24-04.10c | overhead without inner code | 6.25 | % |
| 24-04.11a | flits per second | 5.0e8 | |
| 24-04.11b | retries per second | 2500 | |
| 24-04.11c | errored-flit probability | 2.0e-3 | |
| 24-04.12a | burst, one codeword | 141 | bits |
| 24-04.12b | burst, 4-way interleave | 591 | bits |
| 24-04.12b1 | symbols corrected across 4 codewords | 60 | |
| 24-04.13a | Ethernet round trip | 604 | ns |
| 24-04.13b | flit-FEC round trip | 8 | ns |
| 24-04.14a0 | R00 | 1.26 | |
| 24-04.14a1 | R01 | 0.5 | |
| 24-04.14a2 | determinant | 1.3376 | |
| 24-04.14a | c0 | 0.942 | |
| 24-04.14a3 | c1 | -0.374 | |
| 24-04.14b | minimum MSE | 0.0580 | |
| 24-04.14c0 | ZF residual ISI | 0.0625 | |
| 24-04.14c | ZF MSE | 0.075 | |
| 24-04.15a | metric +1 at n=0 | 0.01 | |
| 24-04.15a1 | metric -1 at n=0 | 4.41 | |
| 24-04.15a2 | metric +1 at n=1 | 1.22 | |
| 24-04.15a3 | metric -1 at n=1 | 0.82 | |
| 24-04.15a4 | metric +1 at n=2 | 4.06 | |
| 24-04.15a5 | metric -1 at n=2 | 0.86 | |
| 24-04.15a6 | metric +1 at n=3 | 2.30 | |
| 24-04.15b | final metric | 1.50 | |
| 24-04.16a | symbol error probability | 2.40e-3 | |
| 24-04.16b | mean symbol errors | 1.30 | |
| 24-04.16c | uncorrectable probability | 8.2e-13 | |
