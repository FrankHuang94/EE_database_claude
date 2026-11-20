# Solutions 11-03 · Convolution

Problems: [11-03 problems](../problems/11-03-problems.md) · Chapter: [11-03](../chapters/11-03-convolution.md). Every number below is recomputed by [verify_11_03.py](../verify/verify_11_03.py), which convolves by explicit loops, matrix products and numerical integration.

---

## Solutions

### Solution 11-03.1

Rows are the scaled, shifted copies $x[k]h[n - k]$:

| $n$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $x[0]h[n]$ | 2 | 6 | | |
| $x[1]h[n-1]$ | | −1 | −3 | |
| $x[2]h[n-2]$ | | | 1 | 3 |
| $y[n]$ | **2** | **5** | **−2** | **3** |

Length $3 + 2 - 1$ = 4. Sum: $2 + 5 - 2 + 3$ = **8** $= (\sum x)(\sum h) = 2 \times 4$.

### Solution 11-03.2

(a) Supports add: $[-2 + 3, 1 + 4] = [1, 5]$, from **1** to **5**.

(b) $y[n] = x[n - 3] - x[n - 4]$, so $y = 1, 0, 0, 0, -1$ at $n = 1, \dots, 5$: $y[1]$ = **1** and $y[5]$ = **−1**, zero in between.

(c) This $h$ is a first difference delayed by three samples: $y[n] = x[n - 3] - x[n - 4]$. A first difference responds only where the input changes, so a boxcar produces a +1 at its rising edge and a −1 at its falling edge, three samples late.

### Solution 11-03.3

(a) Convolving with $\delta[n - 3]$ delays by 3: $x[n - 3]$. Convolving with $\delta[n + 2]$ advances by 2: $u[n + 2]$, which starts at $n = -2$.

(b) $h[n] = 2\delta[n - 1] - \delta[n - 3]$: the values 2 at $n = 1$ and −1 at $n = 3$. DC gain $\sum h = 2 - 1$ = **1**.

(c) $h = \delta[n]$, since $x * \delta = x$.

### Solution 11-03.4

(a) $y[0] = 1 \cdot 3 = 3$; $y[1] = 1 \cdot (-1) + 2 \cdot 3 = 5$; $y[2] = 1 \cdot 1 + 2 \cdot (-1) = -1$; $y[3] = 2 \cdot 1 = 2$. So $y$ = **3**, **5**, **−1**, **2**. The polynomial product $(1 + 2z)(3 - z + z^2) = 3 - z + z^2 + 6z - 2z^2 + 2z^3 = 3 + 5z - z^2 + 2z^3$ has the same coefficients.

(b) $[1, 2] * [3, 1, 1] = [3, 7, 3, 2]$. Reading index 0 as the most significant digit, the sequences are 12 and 311, and the product is **3732**. No column exceeded 9, so no carries arose.

### Solution 11-03.5

(a) For $n \ge 0$, $y[n] = \sum_{k=0}^{n}0.5^k\,0.5^{n-k} = (n + 1)\,0.5^n$, the $a = b$ case of §3.2. So $y$ = **1**, **1**, **0.75**, **0.5** at $n = 0, 1, 2, 3$.

(b) $y[n] = \sum_{k=0}^{\min(n,3)}0.5^{n-k}$. $y[2] = 0.25 + 0.5 + 1$ = **1.75**; $y[3] = 0.125 + 0.25 + 0.5 + 1$ = **1.875**. For $n \ge 3$ all four input samples have arrived: $y[n] = 0.5^n(1 + 2 + 4 + 8) = 15 \times 0.5^n$, so $y[4]$ = **0.9375**: once the boxcar has passed, the output decays at the system's own rate.

### Solution 11-03.6

$y(t) = \int_0^t e^{-2\tau}\,d\tau = \tfrac12(1 - e^{-2t})$ for $t \ge 0$. At 0.5 s, $\tfrac12(1 - e^{-1})$ = **0.3161**. The final value is **0.5** $= \int_0^\infty e^{-2t}\,dt$, the area of $h$: the DC gain.

### Solution 11-03.7

(a) Breakpoints 0, 1, 2. For $0 \le t < 1$ the overlap is $[0, t]$, so $y = t$; for $1 \le t < 2$ it is $[t - 1, 1]$, so $y = 2 - t$. A triangle: $y(0.5)$ = **0.5**, $y(1)$ = **1**, $y(1.5)$ = **0.5**.

(b) Flip the pulse $x$: with $x(t - \tau) = 1$ for $t - 1 < \tau \le t$, $y(t) = \int h(\tau)\,d\tau$ over the overlap of $[t - 1, t]$ with $[0, 2)$. Breakpoints $0 + 0$, $1 + 0$, $0 + 2$, $1 + 2$: 0, 1, 2, 3.

- $0 \le t < 1$: $\int_0^t\tau\,d\tau = t^2/2$.
- $1 \le t < 2$: $\int_{t-1}^{t}\tau\,d\tau = t - \tfrac12$.
- $2 \le t < 3$: $\int_{t-1}^{2}\tau\,d\tau = 2 - (t - 1)^2/2$.

So $y(0.5)$ = **0.125**, $y(1.5)$ = **1** and $y(2.5) = 2 - 1.125$ = **0.875**. Continuity: at 1, $\tfrac12 = \tfrac12$; at 2, $1.5 = 1.5$; at 3, 0. The area is $1 \times 2$ = **2**.

### Solution 11-03.8

(a) With $\tau$ = 1 ms and $\tau_2$ = 2 ms:

$$
y(t) = \int_0^t 5e^{-\lambda/\tau_2}\,\frac{1}{\tau}e^{-(t - \lambda)/\tau}\,d\lambda = \frac{5}{\tau}e^{-t/\tau}\int_0^t e^{\lambda(1/\tau - 1/\tau_2)}\,d\lambda = \frac{5\tau_2}{\tau_2 - \tau}\left(e^{-t/\tau_2} - e^{-t/\tau}\right) ,
$$

which is $10\left(e^{-t/2\,\text{ms}} - e^{-t/1\,\text{ms}}\right)$ V.

(b) Setting $dy/dt = 0$: $\tfrac12e^{-t/2} = e^{-t}$ (t in ms), so $e^{-t/2} = \tfrac12$ and $t = 2\ln2$ = **1.386** ms. Then $y = 10(0.5 - 0.25)$ = **2.5** V.

(c) $\int_0^\infty y\,dt = 10(2 - 1)$ = **10** V·ms, and the area rule gives $(5\ \text{V} \times 2\ \text{ms}) \times 1$ = 10 V·ms.

**Units check.** $\frac{5}{\tau}$ (V/ms) times an integral in ms gives volts.

### Solution 11-03.9

(a) $h[0] = s[0] = 1 - 0.5$ = **0.5**, and for $n \ge 1$, $h[n] = s[n] - s[n - 1] = 0.5^n - 0.5^{n+1} = 0.5^{n+1}$. So $h[n] = 0.5^{n+1}u[n]$, with DC gain $\sum h = 0.5/(1 - 0.5)$ = **1**, the step's final value.

(b) $h = ds/dt = \frac{1}{\tau}e^{-t/\tau} - \frac{1}{\tau}e^{-t/\tau} + \frac{t}{\tau^2}e^{-t/\tau} = \frac{t}{\tau^2}e^{-t/\tau}$ for $t \ge 0$: two identical, buffered RC stages in cascade (Example 11-03.5).

### Solution 11-03.10

(a) Cascade: $h_1 * h_2 = [1 \cdot 1, 1 \cdot (-1) + 1 \cdot 1, 1 \cdot (-1)] = 1, 0, -1$. Parallel: $h_1 + h_2 = 2, 0$, that is, $2\delta[n]$.

(b) The step response is the running sum of $h$: $s[0] = 1$, $s[1] = 1$, $s[n] = 0$ for $n \ge 2$. The cascade computes $x[n] - x[n - 2]$, the change over two samples, which is 1 while the step is "new" and 0 once the input has been constant for two samples.

(c) $h_2 * h_1 = [1, 1 - 1, -1] = 1, 0, -1$, the same: convolution is commutative.

### Solution 11-03.11

(a) $\lvert h[n]\rvert \le 0.9^n$, so $\sum\lvert h\rvert \le 1/(1 - 0.9)$ = **10**: stable.

(b) An FIR boxcar: $\sum\lvert h\rvert$ = **100**: stable.

(c) $\int_0^\infty 1\,dt$ diverges: unstable (the integrator).

(d) $\sum n\,0.5^n = 0.5/(1 - 0.5)^2$ = **2**: stable. The factor $n$ grows, but the exponential wins.

(e) $\int_0^T dt/(1 + t) = \ln(1 + T)$ diverges: unstable, although $h \to 0$.

### Solution 11-03.12

(a) DC gain $0.25 - 0.5 + 1 - 0.5 + 0.25$ = **0.5**. Worst-case gain $0.25 + 0.5 + 1 + 0.5 + 0.25$ = **2.5**.

(b) The worst input has the signs of $h$ reversed in time against the output instant: $+, -, +, -, +$, an alternating sequence. For $x[n] = (-1)^n$, $y[n] = \sum_k h[k]\,(-1)^{n-k} = (-1)^n\sum_k h[k]\,(-1)^k$, and $h[k]\,(-1)^k = 0.25, 0.5, 1, 0.5, 0.25$, so $\lvert y\rvert$ = **2.5**: the alternating input is the worst case at every sample. The filter passes the highest DT frequency with five times its DC gain: it is a high-pass filter.

(c) $\log_2 2.5$ = **1.32**, so **2** guard bits.

### Solution 11-03.13

(a) The pattern reversed: $h = -1, 1, 1$ (at $n = 0, 1, 2$).

(b) $p * h = [1, 1, -1] * [-1, 1, 1] = -1, 0, 3, 0, -1$. The peak, **3**, equals the pattern's energy $\sum p^2$ and occurs when the pattern is fully aligned; the largest sidelobe has magnitude **1**.

(c) The receiver decides that a packet has started when the output crosses a threshold between the sidelobe level and the peak. A large ratio of peak to sidelobe leaves room for noise on either side of the threshold, so detections are reliable and well timed. This three-chip pattern is a Barker code, one of a family designed for sidelobes of magnitude at most 1.

### Solution 11-03.14

(a) $28 \times 28 \times 128 \times 128 \times 9$ = **115.6** million MACs (the same count as Example 11-03.8, by coincidence of the dimensions).

(b) $115.6 \times 10^6/(4096 \times 10^9)$ = **28.22** µs.

(c) $28.22/25$ = **113**% utilization: more than the hardware can do with direct convolution. Either the claim is wrong, or the device is not computing all 115.6 million MACs.

(d) Two legitimate possibilities. **Sparsity:** if many weights or activations are zero and the hardware skips them, fewer MACs are executed; the result is exact only if the zeros are really there. **A fast algorithm:** Winograd-type transforms compute a 3 × 3 convolution with fewer multiplications than the direct method by spending extra additions. The distinguishing question is: "How many MACs does your hardware actually execute for this layer, on dense weights, and what is the latency on a dense benchmark?" A sparsity-based number collapses on dense weights; a fast-algorithm number does not, but may lose some numerical accuracy at low precision.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 11-03.1a | y[0] | 2 | — |
| 11-03.1b | y[1] | 5 | — |
| 11-03.1c | y[2] | −2 | — |
| 11-03.1d | y[3] | 3 | — |
| 11-03.1e | sum of y | 8 | — |
| 11-03.2a | start of support | 1 | — |
| 11-03.2b | end of support | 5 | — |
| 11-03.2c | y[1] | 1 | — |
| 11-03.2d | y[5] | −1 | — |
| 11-03.3a | DC gain | 1 | — |
| 11-03.4a | y[0] | 3 | — |
| 11-03.4b | y[1] | 5 | — |
| 11-03.4c | y[2] | −1 | — |
| 11-03.4d | y[3] | 2 | — |
| 11-03.4e | 12 × 311 | 3732 | — |
| 11-03.5a | y[0] | 1 | — |
| 11-03.5b | y[1] | 1 | — |
| 11-03.5c | y[2] | 0.75 | — |
| 11-03.5d | y[3] | 0.5 | — |
| 11-03.5e | boxcar response y[2] | 1.75 | — |
| 11-03.5f | boxcar response y[3] | 1.875 | — |
| 11-03.5g | boxcar response y[4] | 0.9375 | — |
| 11-03.6a | step response at 0.5 s | 0.3161 | — |
| 11-03.6b | final value | 0.5 | — |
| 11-03.7a | triangle at 0.5 | 0.5 | — |
| 11-03.7b | triangle at 1 | 1 | — |
| 11-03.7c | triangle at 1.5 | 0.5 | — |
| 11-03.7d | y(0.5) | 0.125 | — |
| 11-03.7e | y(1.5) | 1 | — |
| 11-03.7f | y(2.5) | 0.875 | — |
| 11-03.7g | area | 2 | — |
| 11-03.8a | time of peak | 1.386 | ms |
| 11-03.8b | peak | 2.5 | V |
| 11-03.8c | area | 10 | V·ms |
| 11-03.9a | h[0] | 0.5 | — |
| 11-03.9b | DC gain | 1 | — |
| 11-03.11a | bound for (a) | 10 | — |
| 11-03.11b | sum for (b) | 100 | — |
| 11-03.11c | sum for (d) | 2 | — |
| 11-03.12a | DC gain | 0.5 | — |
| 11-03.12b | worst-case gain | 2.5 | — |
| 11-03.12c | output magnitude for (−1)ⁿ | 2.5 | — |
| 11-03.12d | log₂ 2.5 | 1.32 | bit |
| 11-03.12e | guard bits | 2 | bit |
| 11-03.13a | matched-filter peak | 3 | — |
| 11-03.13b | largest sidelobe magnitude | 1 | — |
| 11-03.14a | MACs | 115.6 | M |
| 11-03.14b | minimum time | 28.22 | µs |
| 11-03.14c | implied utilization | 113 | % |
