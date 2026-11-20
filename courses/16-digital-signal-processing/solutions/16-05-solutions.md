# Solutions 16-05 · Spectral Analysis and Windowing

Problems: [16-05 problems](../problems/16-05-problems.md) · Chapter: [16-05](../chapters/16-05-spectral-analysis-and-windowing.md). Every number below is recomputed by [verify_16_05.py](../verify/verify_16_05.py): window figures of merit from their definitions, floor depths and SNRs by simulating quantized sines, and leakage by evaluating the windows' DTFTs.

---

## Solutions

### Solution 16-05.1

(a) **Flat-top**: scalloping below 0.01 dB, so an off-bin tone reads correctly. (b) **Blackman–Harris**: sidelobes below −92 dB; for a tone halfway between bins, Hann's leakage 15 bins away is **−79.9** dB, as large as the spur. (c) **Rectangular**: in a coherent test there is no leakage to suppress, and its main lobe is the narrowest. (d) **Hann**: a good compromise between resolution, leakage and noise.

Blackman with $N$ = 2048 at 48 kHz: bin spacing $48{,}000/2048$ = **23.44** Hz, noise bandwidth $1.7268 \times 23.4375$ = **40.47** Hz.

### Solution 16-05.2

$A = \lvert X\rvert/(N\cdot\text{CG}/2) = 367.4/(4096 \times 0.35875/2)$ = **0.500**.

### Solution 16-05.3

$\text{SNR} = 6.02 \times 14 + 1.76$ = **86.04** dB. Floor depth: $86.04 + 10\log_{10}(16{,}384/2)$ = **125.2** dB below the tone.

### Solution 16-05.4

$\sum_n 0.5 = N/2$, and $\sum_n\cos(2\pi n/N) = 0$ (a sum of a complex exponential over a full period, 16-03 §3.1), so $\sum w = N/2$. Squaring, $w^2 = 0.25 - 0.5\cos\theta + 0.25\cos^2\theta$ with $\cos^2\theta = (1 + \cos2\theta)/2$; the cosine sums vanish again, leaving $\sum w^2 = N(0.25 + 0.125) = 3N/8$. Then ENBW $= N(3N/8)/(N/2)^2$ = **1.5** bins, for every $N \ge 3$.

### Solution 16-05.5

SNR = floor depth − processing gain = $120 - 10\log_{10}(32{,}768) = 120 - 45.15$ = **74.85** dB. ENOB = $(74.85 - 1.76)/6.02$ = **12.14** bits (assuming no distortion; with distortion, SINAD and ENOB are lower).

### Solution 16-05.6

Rectangular: separation must exceed 1.21 bins, so $f_s/N \le 150/1.21$, $N \ge 1.207 \times 48{,}000/150$ = **386.1** (with the exact 1.2067-bin width), so 387 samples (8.1 ms); the smallest power of 2 is **512**. Hann: $N \ge 2.00 \times 48{,}000/150$ = **640** samples (13.3 ms); power of 2: **1024**.

### Solution 16-05.7

Each periodogram bin has standard deviation equal to its mean; averaging $K$ independent segments divides it by $\sqrt K$. $1/\sqrt K \le 0.1$ needs $K$ = **100** segments: $100 \times 1024$ = **102,400** samples, **2.13** s at 48 kHz.

### Solution 16-05.8

$70\text{ MHz} \times 32{,}768/250\text{ MHz} = 9175.04$; the nearest odd integer is $M$ = **9175**, relatively prime to $2^{15}$. $f_{in} = 9175 \times 250\text{ MHz}/32{,}768$ = **69.99969** MHz. The 2nd harmonic is at bin 18,350, above $N/2 = 16{,}384$, so it aliases to $32{,}768 - 18{,}350$ = **14,418**. The 3rd is at 27,525, aliasing to **5,243**.

### Solution 16-05.9

As measured: $(70.0 - 1.76)/6.02$ = **11.34** bits. Referred to full scale (add the 1 dB the test level gave up): $(71.0 - 1.76)/6.02$ = **11.50** bits.

### Solution 16-05.10

THD: $10\log_{10}(10^{-8.5} + 10^{-7.8} + 10^{-9.5} + 10^{-9.0})$ = **−76.92** dB, dominated by HD3. SINAD combines noise and distortion powers: $-10\log_{10}(10^{-7.2} + 10^{-7.692})$ = **70.79** dB. SFDR is set by the largest spur, HD3: **78** dB.

### Solution 16-05.11

Evaluating the windows' DTFTs at 20.5 bins from the tone, relative to their value at 0.5 bin (the peak bin): rectangular **−32.3** dB, Blackman–Harris **−137.9** dB (far below its −92 dB first sidelobe, because its sidelobes fall with distance).

### Solution 16-05.12

Floor depth = SNR + $10\log_{10}(N/(2\,\text{ENBW}))$: rectangular $80 + 36.1$ = **116.1** dB, Blackman–Harris $80 + 33.1$ = **113.1** dB. With the rectangular window, though, the carrier's leakage at 20 bins (−32 dB) dwarfs both the floor and the −100 dBc spur: invisible. With Blackman–Harris the leakage (−138 dB) is far below the floor, and the spur stands **13.1** dB above the floor: visible.

### Solution 16-05.13

Write $\cos(2\pi n/N) = \frac12(e^{j2\pi n/N} + e^{-j2\pi n/N})$, so $w[n] = \frac12 - \frac14e^{j2\pi n/N} - \frac14e^{-j2\pi n/N}$ for $n = 0, \dots, N - 1$. Multiplying by $e^{\pm j2\pi n/N}$ shifts a DTFT by $\pm2\pi/N$ (the modulation property, 11-07), and the DTFT of the constant 1 over $N$ samples is $W_R(\omega)$. Therefore

$$
W(e^{j\omega}) = \tfrac12W_R(\omega) - \tfrac14W_R(\omega - 2\pi/N) - \tfrac14W_R(\omega + 2\pi/N) .
$$

At the bins, $\omega = 2\pi k/N$, $W_R$ equals $N$ at $k = 0$ and 0 at every other bin. So an on-bin tone reaches only its own bin (weight $\frac12N$) and the two adjacent bins (weight $\frac14N$ each, with the opposite sign): **3** bins in all, the adjacent ones at $20\log_{10}(1/4)/(1/2)$ = **−6.02** dB relative to the peak. The three shifted kernels also cancel each other's sidelobes far from the tone, which is why Hann's sidelobes fall at 18 dB per octave instead of the rectangular window's 6.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-05.1a | Blackman bin spacing | 23.44 | Hz |
| 16-05.1b | Blackman noise bandwidth | 40.47 | Hz |
| 16-05.1c | Hann leakage 15 bins from a half-bin tone | −79.9 | dB |
| 16-05.2a | amplitude | 0.500 | — |
| 16-05.3a | ideal 14-bit SNR | 86.04 | dB |
| 16-05.3b | floor depth | 125.2 | dB |
| 16-05.4a | Hann ENBW | 1.5 | bins |
| 16-05.5a | SNR | 74.85 | dB |
| 16-05.5b | ENOB | 12.14 | bits |
| 16-05.6a | rectangular minimum N | 386.1 | samples |
| 16-05.6b | rectangular FFT size | 512 | — |
| 16-05.6c | Hann minimum N | 640 | samples |
| 16-05.6d | Hann FFT size | 1024 | — |
| 16-05.7a | segments | 100 | — |
| 16-05.7b | samples | 102400 | — |
| 16-05.7c | duration | 2.13 | s |
| 16-05.8a | coherent bin | 9175 | — |
| 16-05.8b | input frequency | 69.99969 | MHz |
| 16-05.8c | 2nd-harmonic bin | 14418 | — |
| 16-05.8d | 3rd-harmonic bin | 5243 | — |
| 16-05.9a | ENOB as measured | 11.34 | bits |
| 16-05.9b | ENOB referred to full scale | 11.50 | bits |
| 16-05.10a | THD | −76.92 | dB |
| 16-05.10b | SINAD | 70.79 | dB |
| 16-05.10c | SFDR | 78 | dB |
| 16-05.11a | rectangular leakage at 20 bins | −32.3 | dB |
| 16-05.11b | Blackman–Harris leakage at 20 bins | −137.9 | dB |
| 16-05.12a | rectangular floor depth | 116.1 | dB |
| 16-05.12b | Blackman–Harris floor depth | 113.1 | dB |
| 16-05.12c | spur above the Blackman–Harris floor | 13.1 | dB |
| 16-05.13a | bins reached by an on-bin tone | 3 | — |
| 16-05.13b | adjacent-bin level | −6.02 | dB |
