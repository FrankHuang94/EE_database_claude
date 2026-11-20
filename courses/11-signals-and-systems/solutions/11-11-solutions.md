# Solutions 11-11 · Modulation and Filtering Applications

Problems: [11-11 problems](../problems/11-11-problems.md) · Chapter: [11-11](../chapters/11-11-modulation-and-filtering-applications.md). Every number below is recomputed by [verify_11_11.py](../verify/verify_11_11.py).

---

## Solutions

### Solution 11-11.1

The sidebands span $1\,\text{MHz} \pm 10$ kHz: **0.99** to **1.01** MHz, a width of **20** kHz.

### Solution 11-11.2

The output scales by $\cos 60°$ = **0.5**, or **−6.02** dB.

### Solution 11-11.3

The envelope is $A(1 + m\cos\omega_mt)$, so its maximum is $A(1 + m)$ = 1.5 V and its minimum $A(1 - m)$ = 0.5 V. Adding and subtracting: $A$ = **1** V and $m = (1.5 - 0.5)/(1.5 + 0.5)$ = **0.5**.

### Solution 11-11.4

$f_{LO} = 98.1 + 10.7$ = **108.8** MHz; $f_{image} = 98.1 + 2 \times 10.7$ = **119.5** MHz, 21.4 MHz above the station: a front-end filter must attenuate signals that far up, which is far easier than separating stations 21.4 MHz apart only after mixing.

### Solution 11-11.5

The carrier power is $A^2/2$ = 10 W; the sidebands add $m^2/2$ times that for a tone: $10 \times 0.32$ = **3.2** W. Total: **13.2** W. Efficiency: $3.2/13.2$ = **24.2**%.

### Solution 11-11.6

$RC \le \sqrt{1 - 0.64}/(0.8 \times 2\pi \times 10^4)$ = **11.94** µs. The IF period is $1/455\,\text{kHz}$ = **2.198** µs, only **5.43** times smaller: an RC that follows a 10 kHz envelope at this depth cannot also smooth the IF ripple well. A higher IF, a lower modulation depth or a lower audio bandwidth relaxes the conflict.

### Solution 11-11.7

The output is the message multiplied by $\cos(2\pi \cdot 0.5\,t)$: it fades to zero and returns with inverted sign, with nulls every **1** s (at 0.5 s, 1.5 s, …).

### Solution 11-11.8

Outputs at $\lvert 900 - 1000\rvert$ = **100** MHz and $900 + 1000$ = **1900** MHz. A receiver keeps 100 MHz as the IF. The image is at $f_{LO} + f_{IF}$ = **1100** MHz.

### Solution 11-11.9

Spacing $3.1 + 0.9$ = **4** kHz; twelve channels need **48** kHz. The guard band is set by the selection filters' transition width: sharper (higher-order, elliptic) filters allow narrower guards and more channels in the same spectrum.

### Solution 11-11.10

Butterworth **11**, Chebyshev type I **7**, elliptic **5**. The transition ratio of 2 is gentler than Example 11-11.4's 1.5, so the Butterworth penalty is smaller, but the ranking is the same.

### Solution 11-11.11

$1\,\text{Gb/s}/80\,\text{MHz} = 12.5$ bit/s/Hz, so $\text{SNR} \ge 2^{12.5} - 1$ = **5792**, or **37.6** dB. Real links need several decibels more for coding gaps and implementation losses.

### Solution 11-11.12

The image is at $f_0 + 2f_{IF}$. Solving $10\log_{10}[1 + Q^2(f/f_0 - f_0/f)^2] = 40$ dB for $f > f_0$ gives the image frequency $f$ = **2166** kHz, so $f_{IF} = (2166 - 600)/2$ = **783** kHz. A 455 kHz IF would give less rejection with this front end: either a sharper (two-stage) front end or a higher IF is needed.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-11.1a | lower edge | 0.99 | MHz |
| 11-11.1b | upper edge | 1.01 | MHz |
| 11-11.1c | width | 20 | kHz |
| 11-11.2a | factor | 0.5 | — |
| 11-11.2b | loss | −6.02 | dB |
| 11-11.3a | carrier amplitude | 1 | V |
| 11-11.3b | modulation index | 0.5 | — |
| 11-11.4a | LO frequency | 108.8 | MHz |
| 11-11.4b | image frequency | 119.5 | MHz |
| 11-11.4c | image offset from the station | 21.4 | MHz |
| 11-11.5a | sideband power | 3.2 | W |
| 11-11.5b | total power | 13.2 | W |
| 11-11.5c | efficiency | 24.2 | % |
| 11-11.6a | maximum RC | 11.94 | µs |
| 11-11.6b | IF period | 2.198 | µs |
| 11-11.6c | ratio | 5.43 | — |
| 11-11.7a | time between nulls | 1 | s |
| 11-11.8a | difference frequency | 100 | MHz |
| 11-11.8b | sum frequency | 1900 | MHz |
| 11-11.8c | image | 1100 | MHz |
| 11-11.9a | channel spacing | 4 | kHz |
| 11-11.9b | total bandwidth | 48 | kHz |
| 11-11.10a | Butterworth order | 11 | — |
| 11-11.10b | Chebyshev I order | 7 | — |
| 11-11.10c | elliptic order | 5 | — |
| 11-11.11a | required SNR | 5792 | — |
| 11-11.11b | required SNR | 37.6 | dB |
| 11-11.12a | image frequency | 2166 | kHz |
| 11-11.12b | IF | 783 | kHz |
