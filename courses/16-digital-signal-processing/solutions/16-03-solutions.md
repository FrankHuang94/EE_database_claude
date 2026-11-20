# Solutions 16-03 · The DFT and Its Properties

Problems: [16-03 problems](../problems/16-03-problems.md) · Chapter: [16-03](../chapters/16-03-the-dft.md). Every number below is recomputed by [verify_16_03.py](../verify/verify_16_03.py): DFTs from the definition (the lab's matrix) against `numpy.fft`, circular convolutions computed directly and by DFT products, block convolutions against `numpy.convolve`, and the cost model searched over FFT sizes.

---

## Solutions

### Solution 16-03.1

Only $x[0] = 1$ and $x[2] = -1$ are nonzero, so $X[k] = 1 - W_4^{2k} = 1 - (-1)^k$: $X = (0, 2, 0, 2)$, that is $X[1]$ = **2** and $X[3]$ = **2**. The sequence is $\cos(\pi n/2)$, a quarter of the sample rate: **0.25** $f_s$. Its energy sits in bin 1 and its mirror, bin 3, each $AN/2 = 1 \times 4/2 = 2$.

### Solution 16-03.2

Bin spacing $f_s/N = 10^6/4096$ = **244.14** Hz. The 100 kHz tone sits at $100{,}000/244.14$ = **409.6**: between bins 409 and 410. Bin 4000 is above $N/2$, so it is $(4000 - 4096) \times 244.14$ = **−23.44** kHz.

### Solution 16-03.3

From Example 16-03.1, $X = (10, -2 + 2j, -2, -2 - 2j)$.

(a) $(4, 1, 2, 3) = x[((n - 1))_4]$, a circular shift by 1, so its DFT is $W_4^kX[k] = (-j)^kX[k]$: $(10,\ (-j)(-2 + 2j),\ (-1)(-2),\ (j)(-2 - 2j)) = (10, 2 + 2j, 2, 2 - 2j)$. Magnitudes are unchanged; only phases rotate.

(b) $(-1)^n = W_4^{-2n}$, a modulation by $l = 2$, so the DFT is $X[((k - 2))_4] = (X[2], X[3], X[0], X[1]) = (-2, -2 - 2j, 10, -2 + 2j)$: the spectrum shifted by half the sample rate.

### Solution 16-03.4

$y[n] = \sum_m h[m]x[((n - m))_4] = x[n] - x[((n - 1))_4]$:

- $y[0] = x[0] - x[3] = 1 - 1$ = **0**
- $y[1] = x[1] - x[0] = 2 - 1$ = **1**
- $y[2] = x[2] - x[1] = 0 - 2$ = **−2**
- $y[3] = x[3] - x[2] = 1 - 0$ = **1**

Check: $X = (4, 1 - j, -2, 1 + j)$ and $H = (0, 1 + j, 2, 1 - j)$; the products are $(0, 2, -4, 2)$, whose inverse DFT is $(0, 1, -2, 1)$.

### Solution 16-03.5

The linear convolution has $200 + 57 - 1$ = **256** samples, so $N \ge 256$; the smallest power of 2 is also **256**. (A 255-point DFT would wrap the last output onto the first.)

### Solution 16-03.6

By §3.3, $\tilde h[0] = \sum_{r\ge0}0.9^{rN} = 1/(1 - 0.9^N)$, so the relative error is $0.9^N/(1 - 0.9^N)$. It falls below 0.01 when $0.9^N < 0.01/1.01$, that is $N > \ln(0.0099)/\ln 0.9 = 43.8$: $N$ = **44** (error **0.98**%; $N$ = 43 gives 1.09%).

### Solution 16-03.7

On-bin, $\lvert X[100]\rvert = \lvert X[2048 - 100]\rvert = AN/2 = 2 \times 1024$ = **2048** (in volts times samples). The mean-square value of a 2 V cosine is $A^2/2$ = **2** V². Parseval: $\sum x^2 = N \times 2 = 4096$ V², and $\frac1N(2048^2 + 2048^2) = 4096$ V².

### Solution 16-03.8

At 50 Hz the tone completes exactly 50 cycles: the largest bin is $N/2$, ratio **1** (0 dB). At 50.5 Hz the tone falls halfway between bins 50 and 51; the largest bin is **0.6397** of $N/2$, or **−3.88** dB. The long-record limit for a complex exponential is $\lvert\sin(\pi/2)\rvert/(N\sin(\pi/2N)) \to 2/\pi$ = 0.6366 (−3.92 dB); the real cosine's mirror-image tone adds a little.

### Solution 16-03.9

Block length $L = N - M + 1 = 128 - 33 + 1$ = **96**. Blocks: $\lceil 10{,}000/96\rceil$ = **105** (the last one partly filled). Each block output is $L + M - 1 = 128$ samples, overlapping the next by $M - 1$ = **32**. Full output length $10{,}000 + 33 - 1$ = **10,032**.

### Solution 16-03.10

$C(N, 255) = 4[N\log_2N + N]/(N - 254)$:

| $N$ | Cost per output |
|---|---|
| 512 | 79.4 |
| 1024 | 58.5 |
| 2048 | **54.8** |
| 4096 | 55.4 |

The best is $N$ = **2048**, with block length $L = 2048 - 254$ = **1794** and **54.8** multiplies per output, against 255 for direct convolution: **4.65** times fewer. Longer filters gain more, because the FFT's cost per output grows only logarithmically while direct cost grows linearly.

### Solution 16-03.11

$\cos(2\pi \cdot 3n/16)$ has bins 3 and 13, each $AN/2 = 16/2$ = **8**. $0.5\sin(\theta) = 0.5(e^{j\theta} - e^{-j\theta})/(2j)$, so bin 5 holds $0.5 \times 16/(2j) = -4j$ and bin 11 holds $+4j$: magnitude **4** each. All other bins are zero, because both tones complete whole numbers of cycles in 16 samples.

### Solution 16-03.12

(a) A 17-sample channel needs a prefix of at least $M - 1$ = **16** samples, a delay spread of $16/(20\text{ MHz})$ = **0.8** µs. The overhead is $16/(64 + 16)$ = **20**% of airtime.

These are exactly the numbers of 802.11a/g Wi-Fi: a 64-point FFT at 20 MHz with a 0.8 µs, 16-sample guard interval (R-236).

(b) A 9-tap channel needs 8 samples: overhead $8/72$ = **11.1**% with 64 subcarriers and $8/264$ = **3.03**% with 256. More subcarriers amortize the prefix, at the cost of longer symbols, which are more sensitive to frequency offset and to channels that change during the symbol.

### Solution 16-03.13

(a) Both tones are on bins: $\lvert X[4]\rvert = \lvert X[5]\rvert = AN/2$ = **8**, and every other bin is zero. The 16-point DFT shows two clean lines, but it says nothing about what lies between them.

(b) Padding to 64 points puts **3** spectral samples between the tones (at 4.25, 4.5 and 4.75 cycles); padding to 256 puts **15**. Both show the same dip, a minimum of **2.01** at 4.5 cycles, which is **−12.0** dB below the peaks: exactly the DTFT's value there. Zero padding only samples the 16-sample record's DTFT more finely (§3.6); it cannot change it.

(c) No. Two tones 0.5 cycle per record apart are closer than the record's resolution (about one bin, $f_s/N$): the 16-sample record's DTFT has a single merged lobe, peaking at about **4.25** cycles, and finer sampling of that lobe never splits it. Only a longer record narrows the main lobes.

### Solution 16-03.14

(a) $N$ = 4 and $M$ = 2, so each block keeps $L = N - M + 1$ = **3** outputs and the hop is 3. The first block is $(0, 1, 2, 3)$: one leading zero ($M - 1$) for the input before $n = 0$.

(b) Block 1, $(0, 1, 2, 3) \circledast (1, 1, 0, 0)$: the circular convolution is $(0 + 3, 1 + 0, 2 + 1, 3 + 2) = (3, 1, 3, 5)$. The first sample, 3, is the wrapped one ($x[3] + x[0]$); discard it and keep **(1, 3, 5)**. Block 2 starts 3 samples later, $(3, 4, 5, 6)$: circular convolution $(3 + 6, 4 + 3, 5 + 4, 6 + 5) = (9, 7, 9, 11)$; keep **(7, 9, 11)**. A third block $(6, 0, 0, 0)$ gives $(6, 6, 0, 0)$ and keeps $(6, 0, 0)$, the tail.

(c) Direct convolution: $(1, 1 + 2, 2 + 3, 3 + 4, 4 + 5, 5 + 6, 6) = (1, 3, 5, 7, 9, 11, 6)$, the same.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-03.1a | X[1] | 2 | — |
| 16-03.1b | X[3] | 2 | — |
| 16-03.1c | frequency as a fraction of fs | 0.25 | — |
| 16-03.2a | bin spacing | 244.14 | Hz |
| 16-03.2b | bin of 100 kHz | 409.6 | — |
| 16-03.2c | frequency of bin 4000 | −23.44 | kHz |
| 16-03.3a | shifted X[1] | 2+j2 | — |
| 16-03.3b | shifted X[2] | 2 | — |
| 16-03.3c | shifted X[3] | 2−j2 | — |
| 16-03.3d | modulated X[1] | −2−j2 | — |
| 16-03.3e | modulated X[2] | 10 | — |
| 16-03.4a | y[0] | 0 | — |
| 16-03.4b | y[1] | 1 | — |
| 16-03.4c | y[2] | −2 | — |
| 16-03.4d | y[3] | 1 | — |
| 16-03.5a | smallest N | 256 | — |
| 16-03.5b | smallest power of 2 | 256 | — |
| 16-03.6a | smallest N for 1% | 44 | — |
| 16-03.6b | error at that N | 0.98 | % |
| 16-03.7a | on-bin magnitude | 2048 | — |
| 16-03.7b | mean-square value | 2 | V² |
| 16-03.8a | largest bin ratio, 50 Hz | 1 | — |
| 16-03.8b | largest bin ratio, 50.5 Hz | 0.6397 | — |
| 16-03.8c | the same in dB | −3.88 | dB |
| 16-03.9a | block length | 96 | — |
| 16-03.9b | number of blocks | 105 | — |
| 16-03.9c | overlap | 32 | — |
| 16-03.9d | output length | 10032 | — |
| 16-03.10a | cost, N = 512 | 79.4 | per output |
| 16-03.10b | cost, N = 1024 | 58.5 | per output |
| 16-03.10c | best cost | 54.8 | per output |
| 16-03.10d | cost, N = 4096 | 55.4 | per output |
| 16-03.10e | best N | 2048 | — |
| 16-03.10f | block length | 1794 | — |
| 16-03.10g | saving | 4.65 | — |
| 16-03.11a | bins 3 and 13 | 8 | — |
| 16-03.11b | bin 5 | −j4 | — |
| 16-03.11c | magnitude of bins 5 and 11 | 4 | — |
| 16-03.12a | shortest prefix | 16 | samples |
| 16-03.12b | delay spread | 0.8 | µs |
| 16-03.12c | overhead, 64 points | 20 | % |
| 16-03.12d | overhead, 9 taps, 64 points | 11.1 | % |
| 16-03.12e | overhead, 9 taps, 256 points | 3.03 | % |
| 16-03.13a | on-bin magnitude | 8 | — |
| 16-03.13b | samples between tones, 64 points | 3 | — |
| 16-03.13c | samples between tones, 256 points | 15 | — |
| 16-03.13d | dip minimum | 2.01 | — |
| 16-03.13e | dip below the peaks | −12.0 | dB |
| 16-03.13f | merged-lobe peak, 4 and 4.5 cycles | 4.25 | cycles |
| 16-03.14a | outputs kept per block | 3 | — |
