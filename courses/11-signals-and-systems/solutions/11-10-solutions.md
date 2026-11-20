# Solutions 11-10 · Sampling, Aliasing and Reconstruction

Problems: [11-10 problems](../problems/11-10-problems.md) · Chapter: [11-10](../chapters/11-10-sampling-aliasing-reconstruction.md). Every number below is recomputed by [verify_11_10.py](../verify/verify_11_10.py), which samples tones and locates their FFT peaks, simulates noise and jitter, and searches filter orders numerically.

---

## Solutions

### Solution 11-10.1

(a) The Nyquist rate is $2f_M$ = **8** kHz. (b) At 10 kHz the Nyquist frequency is **5** kHz. The first copy of the spectrum starts at $f_s - f_M = 10 - 4$ = 6 kHz, so the gap above the 4 kHz band edge is **2** kHz: that is the transition band available to the anti-aliasing filter.

### Solution 11-10.2

600 Hz: $\lvert 600 - 1000\rvert$ = **400** Hz. 1100 Hz: **100** Hz. 1900 Hz: $\lvert 1900 - 2000\rvert$ = **100** Hz. 2450 Hz: $\lvert 2450 - 2000\rvert$ = **450** Hz. Two different inputs (1100 and 1900 Hz) land on the same 100 Hz, one upright and one reversed.

### Solution 11-10.3

$700 - 1000 = -300$ Hz, negative, so the phase flips: the samples are $\cos(2\pi \cdot 300\,nT - 30°)$, a **300** Hz cosine with phase **−30**°. Check at $n = 1$: $\cos(2\pi \cdot 0.7 + 30°) = \cos(282°) = 0.2079$ and $\cos(2\pi \cdot 0.3 - 30°) = \cos(78°) = 0.2079$.

### Solution 11-10.4

$\operatorname{sinc}(0.25) = \sin(\pi/4)/(\pi/4)$ = **0.9003**, or **−0.91** dB; $\operatorname{sinc}(0.5) = 2/\pi$ = **0.6366**, or **−3.92** dB.

### Solution 11-10.5

(a) At 8 kHz (Nyquist 4 kHz): 3 kHz stays at **3** kHz and 7 kHz folds to **1** kHz. (b) At 12 kHz (Nyquist 6 kHz): 3 kHz stays and 7 kHz folds to $12 - 7$ = **5** kHz. In both cases two distinct lines appear, so nothing looks wrong, but the 7 kHz tone is misreported each time. (c) Both are correct only for $f_s > 2 \times 7$ = **14** kHz. Aliasing is dangerous precisely because it produces plausible, wrong answers.

### Solution 11-10.6

At 500 SPS the first alias frequency is $500 - 150 = 350$ Hz. From §3.4, $n \ge \ln(10^4 - 1)/(2\ln(350/150)) = 9.210/1.695$ = **5.44**, so order **6**. At 4 kSPS the first alias frequency is 3850 Hz, and $n \ge 9.210/(2\ln 25.67)$ = **1.42**, so order **2**. Sampling eight times faster and decimating digitally replaces a sixth-order analog filter with a second-order one; the ADS1292R takes this to the extreme with a 128 kHz modulator and a simple RC (Example 11-10.7).

### Solution 11-10.7

Without a filter, every sample carries all the noise up to 1 MHz: $20\,\text{nV}\sqrt{10^6\,\text{Hz}}$ = **20** µV RMS. With an ideal 50 kHz filter: $20\,\text{nV}\sqrt{5 \times 10^4}$ = **4.47** µV. The difference is $20\log_{10}(20/4.47) = 10\log_{10}(1\,\text{MHz}/50\,\text{kHz})$ = **13.0** dB of avoidable noise.

### Solution 11-10.8

Droop at 20 kHz: $\operatorname{sinc}(20/44.1)$ = **0.6944**, **−3.17** dB. The first image is at $44.1 - 20$ = **24.1** kHz with weight $\operatorname{sinc}(24.1/44.1)$ = **0.5763**, **−4.79** dB relative to DC and only **1.62** dB below the tone. With a 44.1 kHz rate, the reconstruction filter has only 4.1 kHz between 20 kHz and the image: the reason practical CD-rate DACs interpolate to a higher rate before the hold.

### Solution 11-10.9

(a) $\lvert H(e^{j\omega})\rvert = \lvert\sin(3\omega/2)/(3\sin(\omega/2))\rvert$ with $\omega = 2\pi \times 100/1000 = 0.2\pi$: **0.8727**. (b) 900 Hz aliases to **100** Hz and comes out with the same gain, 0.8727: no DT filter can tell it from a real 100 Hz input. (c) The null at $\omega = 2\pi/3$, that is $1000/3$ = **333.3** Hz.

### Solution 11-10.10

$x_r(t) = \operatorname{sinc}(t/T)$. At 0.5 ms: $\operatorname{sinc}(0.5) = 2/\pi$ = **0.6366**. At 1.5 ms: $\operatorname{sinc}(1.5) = \sin(1.5\pi)/(1.5\pi) = -1/(1.5\pi)$ = **−0.2122**. Between samples the reconstruction rings; at every other sample instant it is exactly zero.

### Solution 11-10.11

$B$ = 0.2 MHz, $f_H/B = 54$. From $2f_H/n \le f_s \le 2f_L/(n - 1)$:

- $n$ = 54: $21.6/54 = 0.4$ MHz to $21.2/53 = 0.4$ MHz: a single rate, **0.4** MHz, with zero width.
- $n$ = 50: **0.432** to **0.43265** MHz, a window **0.653** kHz wide.
- $n$ = 40: **0.54** to **0.54359** MHz, a window **3.59** kHz wide.

The deeper the undersampling, the narrower the window: the clock must be accurate to a fraction of a percent, and the analog band-pass filter must reject every other Nyquist zone, all of which are only 200–270 kHz wide.

### Solution 11-10.12

Setting $-20\log_{10}(2\pi f_0\sigma_t) = 70$: $\sigma_t = 10^{-3.5}/(2\pi f_0)$. At 100 MHz: **503** fs RMS. At 1 GHz: **50.3** fs RMS. Every decade of input frequency tightens the jitter budget tenfold.

### Solution 11-10.13

Before: $10\log_{10}(1.5 \times 2^{24})$ = **74.01** dB (the rule of thumb $6.02 \times 12 + 1.76$ rounds this to 74.0). Oversampling by 64 keeps $1/64$ of the quantization noise in band: $+10\log_{10}64$ = **18.06** dB, giving **92.07** dB (adding the rounded constants would give 92.06). The equivalent resolution is $(92.07 - 1.76)/6.02$ = **15.0** bits: 3 bits gained by a 64-fold rate increase, half a bit per doubling. Noise shaping (20-08) does much better.

### Solution 11-10.14

A single pole gives $10\log_{10}[1 + (f/f_c)^2] \ge 40$ dB at $f$ = 127.95 kHz when $f_c \le 127.95\,\text{kHz}/\sqrt{9999}$ = **1.280** kHz. With 4 kΩ effective, $C = 1/(2\pi \times 4\,\text{k}\Omega \times 1.280\,\text{kHz})$ = **31.1** nF. The data sheet warns that a larger capacitor degrades THD [R-190], so the gain in alias rejection is paid for in distortion; a second-order filter or shielding against the 128 kHz interferer may be better choices.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-10.1a | Nyquist rate | 8 | kHz |
| 11-10.1b | Nyquist frequency | 5 | kHz |
| 11-10.1c | transition gap | 2 | kHz |
| 11-10.2a | alias of 600 Hz | 400 | Hz |
| 11-10.2b | alias of 1100 Hz | 100 | Hz |
| 11-10.2c | alias of 1900 Hz | 100 | Hz |
| 11-10.2d | alias of 2450 Hz | 450 | Hz |
| 11-10.3a | apparent frequency | 300 | Hz |
| 11-10.3b | apparent phase | −30 | ° |
| 11-10.3c | sample at n = 1 | 0.2079 | — |
| 11-10.4a | gain at f_s/4 | 0.9003 | — |
| 11-10.4b | gain at f_s/4 | −0.91 | dB |
| 11-10.4c | gain at f_s/2 | 0.6366 | — |
| 11-10.4d | gain at f_s/2 | −3.92 | dB |
| 11-10.5a | alias of 7 kHz at 8 kHz | 1 | kHz |
| 11-10.5b | alias of 7 kHz at 12 kHz | 5 | kHz |
| 11-10.5c | rate for both correct | 14 | kHz |
| 11-10.5d | 3 kHz tone at both rates | 3 | kHz |
| 11-10.6a | order bound at 500 SPS | 5.44 | — |
| 11-10.6b | order at 500 SPS | 6 | — |
| 11-10.6c | order bound at 4 kSPS | 1.42 | — |
| 11-10.6d | order at 4 kSPS | 2 | — |
| 11-10.6e | ln(10⁴ − 1) | 9.210 | — |
| 11-10.6f | 2 ln(350/150) | 1.695 | — |
| 11-10.6g | ratio at 4 kSPS | 25.67 | — |
| 11-10.7a | unfiltered RMS noise | 20 | µV |
| 11-10.7b | filtered RMS noise | 4.47 | µV |
| 11-10.7c | difference | 13.0 | dB |
| 11-10.8a | droop at 20 kHz | 0.6944 | — |
| 11-10.8b | droop at 20 kHz | −3.17 | dB |
| 11-10.8c | first image frequency | 24.1 | kHz |
| 11-10.8d | image weight | 0.5763 | — |
| 11-10.8e | image level | −4.79 | dB |
| 11-10.8f | image below the tone | 1.62 | dB |
| 11-10.9a | gain at 100 Hz | 0.8727 | — |
| 11-10.9b | alias of 900 Hz | 100 | Hz |
| 11-10.9c | null frequency | 333.3 | Hz |
| 11-10.10a | x_r(0.5 ms) | 0.6366 | — |
| 11-10.10b | x_r(1.5 ms) | −0.2122 | — |
| 11-10.11a | n = 54 rate | 0.4 | MHz |
| 11-10.11b | n = 50 window low | 0.432 | MHz |
| 11-10.11c | n = 50 window high | 0.43265 | MHz |
| 11-10.11d | n = 50 window width | 0.653 | kHz |
| 11-10.11e | n = 40 window low | 0.54 | MHz |
| 11-10.11f | n = 40 window high | 0.54359 | MHz |
| 11-10.11g | n = 40 window width | 3.59 | kHz |
| 11-10.12a | jitter at 100 MHz | 503 | fs |
| 11-10.12b | jitter at 1 GHz | 50.3 | fs |
| 11-10.13a | SNR, 12 bits | 74.01 | dB |
| 11-10.13b | oversampling gain | 18.06 | dB |
| 11-10.13c | SNR after | 92.07 | dB |
| 11-10.13d | equivalent bits | 15.0 | — |
| 11-10.14a | corner frequency | 1.280 | kHz |
| 11-10.14b | capacitor | 31.1 | nF |
