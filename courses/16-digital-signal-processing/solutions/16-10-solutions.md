# Solutions 16-10 · Quantization and Fixed-Point Effects

Problems: [16-10 problems](../problems/16-10-problems.md) · Chapter: [16-10](../chapters/16-10-quantization-and-fixed-point.md). Every number below is recomputed by [verify_16_10.py](../verify/verify_16_10.py): formats and bounds from their definitions, SQNR and dither penalties by simulation, noise gains and norms from impulse responses, and floating-point rounding with NumPy's float16 and an independent bit-level encoder.

---

## Solutions

### Solution 16-10.1

(a) Q4.12: range $[-8, 8 - 2^{-12}]$, step $2^{-12}$ = **2.441** × 10⁻⁴. Q1.31: step $2^{-31}$ = **4.657** × 10⁻¹⁰.

(b) Range ±20 needs $2^{I-1} > 20$, so $I$ = **6** (±32). Resolution $2^{-F} \le 0.001$ needs $F$ = **10** ($2^{-10} = 0.000977$). Total **16** bits: Q6.10.

### Solution 16-10.2

10 bits: $10\log_{10}(1.5 \times 4^{10})$ = **61.97** dB; 14 bits: **86.05** dB. (The rounded rule $6.02N + 1.76$ gives 61.96 and 86.04, off in the last digit.) For 100 dB: $N \ge (100 - 1.76)/6.02$ = **16.32**, so **17** bits.

### Solution 16-10.3

Each truncation error has mean $-\Delta/2$; 1000 of them add to $-1000 \times 2^{-15}/2$ = **−0.01526**, about 500 LSB, while the rounding errors' random part grows only as $\sqrt{1000}$. Biased errors accumulate linearly.

### Solution 16-10.4

One product: Q2.30 (32 bits; two sign bits, because $(-1)\times(-1) = +1$ needs the extra integer bit). Sum of 64 products: 6 guard bits, **Q8.30** (38 bits). Rounding the sum once to Q1.15 adds variance $\Delta^2/12$ with $\Delta = 2^{-15}$: $2^{-30}/12$ = **7.76** × 10⁻¹¹ (full-scale units squared).

### Solution 16-10.5

Granular only: $10\log_{10}(3 \times 2^{32}/16)$ = **89.06** dB. Including clipping: the clipping noise is the same fraction of the signal power as at 12 bits ($2[(1 + 16)Q(4) - 4\phi(4)]$ = **6.18 × 10⁻⁶** of $\sigma^2$), so the SQNR is **52.1** dB, barely better than the 51.9 dB at 12 bits. Once clipping dominates, extra bits are wasted: back off instead (the 16-bit optimum is $L \approx 5.9$, 85.4 dB).

### Solution 16-10.6

$g[n] = a^n$, so $\sum_{n\ge0}a^{2n} = 1/(1 - a^2)$. For $a = 0.9$: $1/0.19$ = **5.26**, **7.2** dB. For $a = 0.99$: $1/0.0199$ = **50.25**, **17.0** dB. Extra bits: $\tfrac12\log_2 50.25$ = **2.83**, so **3** bits.

### Solution 16-10.7

64 independent rounding errors add 64 times the variance of one: $10\log_{10}64$ = **18.06** dB more noise. Full-precision accumulation (16-08 §3.6) avoids it.

### Solution 16-10.8

rms: $\sqrt{101} \times 2^{-12}/\sqrt{12}$ = **7.08 × 10⁻⁴**, **−63.0** dB. Worst case: $101 \times 2^{-13}$ = **0.0123**, **−38.2** dB. The truth for the peak error usually lies a few dB above the rms estimate and far below the bound.

### Solution 16-10.9

$1/(2(1 - a))$: **10** LSB for $a = 0.95$, **50** LSB for $a = 0.99$. Starting from 200 LSB, the simulation decays and sticks at exactly 10 and 50 LSB. Poles close to the circle give large dead bands: a filter with $a = 0.99$ can idle at 50 LSB indefinitely.

### Solution 16-10.10

From the impulse response: $L_1$ = **13.67**, $L_\infty$ = **11.84** (16-08 Problem 16-08.5), $L_2$ = **2.680**. Scaling bits ($\lceil\log_2\rceil$): $L_1$: **4**, $L_\infty$: **4**, $L_2$: **2**. A speech codec (random-like signals, occasional clipping tolerable with saturation) would use $L_2$ scaling and keep two bits of SNR; a safety-critical controller should use $L_1$ scaling, which makes overflow impossible for any bounded input.

### Solution 16-10.11

(a) Rectangular dither (variance $\Delta^2/12$) plus rounding error ($\Delta^2/12$): $\Delta^2/6$, **3.01** dB more than undithered. (b) Triangular dither ($\Delta^2/6$) plus rounding: $\Delta^2/4$, **4.77** dB more. Rectangular dither removes the error's correlation with the signal in the mean but leaves its power varying with the signal (noise modulation, audible on quiet passages); triangular dither makes both the mean and the power of the error independent of the signal, so audio engineers pay the extra 1.76 dB for a constant, benign floor.

### Solution 16-10.12

$0.3 = 1.2 \times 2^{-2}$.

| Format | Significand bits $p$ | 0.3 rounds to | Relative error | 1000 rounds to |
|---|---|---|---|---|
| E4M3 | 4 | 0.3125 | **4.17**% | **448** (saturated) |
| E5M2 | 3 | 0.3125 | 4.17% | **1024** |
| bfloat16 | 8 | 0.30078125 | **0.26**% | 1000 |
| binary16 | 11 | 0.300049 | **0.016**% | 1000 |

The errors sit within each format's bound $2^{-p}$ (6.25%, 12.5%, 0.39%, 0.049%). E4M3 cannot represent 1000 at all (its maximum is 448), which is why FP8 tensors are always paired with scale factors; E5M2 trades precision for range and reaches 1000 with a coarse 2.4% error.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-10.1a | Q4.12 step | 2.441e-4 | — |
| 16-10.1b | Q1.31 step | 4.657e-10 | — |
| 16-10.1c | integer bits | 6 | bits |
| 16-10.1d | fractional bits | 10 | bits |
| 16-10.1e | total bits | 16 | bits |
| 16-10.2a | 10-bit SQNR | 61.97 | dB |
| 16-10.2b | 14-bit SQNR | 86.05 | dB |
| 16-10.2c | bits for 100 dB, real | 16.32 | — |
| 16-10.2d | bits for 100 dB | 17 | bits |
| 16-10.3a | accumulated truncation error | −0.01526 | — |
| 16-10.4a | rounding variance | 7.76e-11 | — |
| 16-10.5a | granular SQNR at 16 bits | 89.06 | dB |
| 16-10.5b | SQNR with clipping at 16 bits | 52.1 | dB |
| 16-10.5c | clipping-noise fraction at L = 4 | 6.18e-6 | — |
| 16-10.6a | noise gain, a = 0.9 | 5.26 | — |
| 16-10.6b | noise gain, a = 0.9 | 7.2 | dB |
| 16-10.6c | noise gain, a = 0.99 | 50.25 | — |
| 16-10.6d | noise gain, a = 0.99 | 17.0 | dB |
| 16-10.6e | extra bits, real | 2.83 | — |
| 16-10.6f | extra bits | 3 | bits |
| 16-10.7a | noise increase | 18.06 | dB |
| 16-10.8a | rms estimate | −63.0 | dB |
| 16-10.8b | worst-case bound | −38.2 | dB |
| 16-10.8c | rms estimate | 7.08e-4 | — |
| 16-10.8d | worst-case bound | 0.0123 | — |
| 16-10.9a | dead band, a = 0.95 | 10 | LSB |
| 16-10.9b | dead band, a = 0.99 | 50 | LSB |
| 16-10.10a | L1 norm | 13.67 | — |
| 16-10.10b | L∞ norm | 11.84 | — |
| 16-10.10c | L2 norm | 2.680 | — |
| 16-10.10d | L1 scaling bits | 4 | bits |
| 16-10.10e | L2 scaling bits | 2 | bits |
| 16-10.10f | L∞ scaling bits | 4 | bits |
| 16-10.11a | rectangular dither penalty | 3.01 | dB |
| 16-10.11b | triangular dither penalty | 4.77 | dB |
| 16-10.12a | E4M3 relative error for 0.3 | 4.17 | % |
| 16-10.12b | bfloat16 relative error | 0.26 | % |
| 16-10.12c | binary16 relative error | 0.016 | % |
| 16-10.12d | E4M3 for 1000 | 448 | — |
| 16-10.12e | E5M2 for 1000 | 1024 | — |
| 16-10.12f | E4M3 and E5M2 value for 0.3 | 0.3125 | — |
| 16-10.12g | bfloat16 value for 0.3 | 0.30078125 | — |
| 16-10.12h | binary16 value for 0.3 | 0.300049 | — |
| 16-10.12i | E5M2 relative error for 1000 | 2.4 | % |
