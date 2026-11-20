# Solutions 16-04 · The FFT Algorithm

Problems: [16-04 problems](../problems/16-04-problems.md) · Chapter: [16-04](../chapters/16-04-the-fft.md). Every number below is recomputed by [verify_16_04.py](../verify/verify_16_04.py): FFTs against `numpy.fft`, operation counts by instrumenting the lab's in-place FFT, and bit-reversed orders and hardware counts by enumeration.

---

## Solutions

### Solution 16-04.1

$\log_2256$ = **8** stages of 128 butterflies: **1,024** butterflies and at most 1,024 complex multiplications. Non-trivial: $\frac{256}2 \times 8 - \frac{3 \times 256}2 + 2 = 1024 - 384 + 2$ = **642**. Direct DFT: $256^2$ = 65,536, a ratio of **64**.

### Solution 16-04.2

Four-bit reversal: $3 = 0011 \to 1100$ = **12**; $6 = 0110 \to 0110$ = **6**; $11 = 1011 \to 1101$ = **13**. An index stays put exactly when its 4-bit pattern is a palindrome: 0000, 0110, 1001 and 1111, that is **4** indices (0, 6, 9 and 15).

### Solution 16-04.3

Stage $s$ combines DFTs of length $2^{s-1}$ into length $2^s$, so its butterflies join samples $2^{s-1}$ apart: spans 1, 2, 4, 8, 16 and **32** in stages 1 to 6. Stage $s$ uses the twiddles $W_{2^s}^j$ for $j = 0, \dots, 2^{s-1} - 1$: 1, 2, 4, 8, 16 and 32 distinct twiddles.

### Solution 16-04.4

Even samples $(0, 0)$: $G = (0, 0)$. Odd samples $(1, -1)$: $H = (1 + (-1), 1 - (-1)) = (0, 2)$. Butterflies with $W_4^0 = 1$ and $W_4^1 = -j$:

- $X[0] = G[0] + H[0] = 0$, $X[2] = G[0] - H[0] = 0$;
- $X[1] = G[1] + (-j)H[1]$ = **−2j**, $X[3] = G[1] - (-j)H[1]$ = **2j**.

Check: $x = (0, 1, 0, -1) = \sin(\pi n/2)$, a quarter-rate sine of amplitude 1, whose DFT is $\mp jN/2 = \mp 2j$ at bins 1 and 3.

### Solution 16-04.5

Even bins take $x[n] + x[n + 4] = (1, 1, 1, 1)$; their 4-point DFT gives $X[0]$ = **4** and $X[2] = X[4] = X[6]$ = **0**. Odd bins take $(x[n] - x[n + 4])W_8^n = (1, W_8, W_8^2, W_8^3)$; its 4-point DFT at index 0 gives $X[1] = 1 + W_8 + W_8^2 + W_8^3 = 1 + (0.7071 - 0.7071j) + (-j) + (-0.7071 - 0.7071j)$ = **1 − j2.4142**, and at index 1 gives $X[3] = 1 + W_8W_4^{1} + W_8^2W_4^2 + W_8^3W_4^3 = 1 + W_8^3 + W_8^6 + W_8^9$ = **1 − j0.4142**.

### Solution 16-04.6

642 non-trivial complex multiplications (Solution 16-04.1): with four real multiplications each, **2,568**; with three, **1,926**.

### Solution 16-04.7

Radix-2: $\frac N2\log_2N$; radix-4: $\frac{3N}8\log_2N$.

| $N$ | Radix-2 | Radix-4 |
|---|---|---|
| 1024 | 5,120 | **3,840** |
| 4096 | 24,576 | **18,432** |

Radix-4 needs **75**% of the radix-2 count at every size.

### Solution 16-04.8

$\frac{512}2\log_2512 + 512 = 256 \times 9 + 512$ = **2,816** complex multiplications, **55.0**% of the 5,120 for a 1024-point complex FFT.

### Solution 16-04.9

Conjugate: $X^* = (10, -2 - 2j, -2, -2 + 2j)$. Forward 4-point FFT (with $W_4 = -j$): $\sum X^*[k] = 4$; $X^*[0] - jX^*[1] - X^*[2] + jX^*[3] = 10 - j(-2 - 2j) + 2 + j(-2 + 2j) = 10 + 2j - 2 + 2 - 2j - 2 = 8$; similarly 12 and 16. Conjugate and divide by 4: $x$ = **(1, 2, 3, 4)**, recovering Example 16-04.2's input.

### Solution 16-04.10

Butterflies per transform: $\frac{4096}2 \times 12$ = **24,576**. A new block arrives every $4096/250 \times 10^6$ = **16.384** µs, which is 16,384 cycles at 1 GHz. Required: $24{,}576/16{,}384$ = **1.5** butterflies per cycle, so **2** units (with 25% margin), plus a ping-pong buffer.

### Solution 16-04.11

$\log_21024$ = **10** butterfly units, $10 - 2$ = **8** general complex multipliers, and $1024 - 1$ = **1,023** delay words. At 32 bits (16 + 16) per word: 32,736 bits = **4,092** bytes. Each butterfly is busy **50**% of the time.

### Solution 16-04.12

(a) The magnitude can grow by at most $N = 2^{12}$ (a full-scale DC input at bin 0), so $12 + 12$ = **24** bits.

(b) An on-bin cosine of amplitude $A$ gives $\lvert X\rvert = AN/2$; with 1/2 per stage the output is $X/N$, so $A/2$ = **1023.5** (1023 or 1024 after rounding), which needs 10 magnitude bits plus the sign: **11** of the 12 bits. The scaling costs one bit of headroom for this signal and adds rounding noise at every stage (16-10).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 16-04.1a | stages | 8 | — |
| 16-04.1b | butterflies | 1024 | — |
| 16-04.1c | non-trivial multiplications | 642 | — |
| 16-04.1d | direct to FFT ratio | 64 | — |
| 16-04.2a | position of 3 | 12 | — |
| 16-04.2b | position of 6 | 6 | — |
| 16-04.2c | position of 11 | 13 | — |
| 16-04.2d | indices that stay in place | 4 | — |
| 16-04.3a | span in stage 6 | 32 | — |
| 16-04.4a | X[1] | −j2 | — |
| 16-04.4b | X[3] | j2 | — |
| 16-04.5a | X[0] | 4 | — |
| 16-04.5b | X[2] | 0 | — |
| 16-04.5c | X[1] | 1−j2.4142 | — |
| 16-04.5d | X[3] | 1−j0.4142 | — |
| 16-04.6a | real multiplications, 4 per complex | 2568 | — |
| 16-04.6b | real multiplications, 3 per complex | 1926 | — |
| 16-04.7a | radix-4, N = 1024 | 3840 | — |
| 16-04.7b | radix-4, N = 4096 | 18432 | — |
| 16-04.7c | radix-4 relative to radix-2 | 75 | % |
| 16-04.8a | real-FFT complex multiplications | 2816 | — |
| 16-04.8b | fraction of the complex FFT | 55.0 | % |
| 16-04.10a | butterflies per transform | 24576 | — |
| 16-04.10b | time per transform | 16.384 | µs |
| 16-04.10c | butterflies per cycle needed | 1.5 | — |
| 16-04.10d | butterfly units | 2 | — |
| 16-04.11a | butterfly units | 10 | — |
| 16-04.11b | general multipliers | 8 | — |
| 16-04.11c | delay words | 1023 | — |
| 16-04.11d | delay memory | 4092 | bytes |
| 16-04.11e | butterfly utilization | 50 | % |
| 16-04.12a | word length without scaling | 24 | bits |
| 16-04.12b | scaled on-bin output | 1023.5 | — |
| 16-04.12c | bits used | 11 | bits |
