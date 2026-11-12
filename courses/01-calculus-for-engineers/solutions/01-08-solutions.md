# Solutions 01-08 · Sequences, Series and Taylor Expansions

Problems: [01-08 problems](../problems/01-08-problems.md) · Chapter: [01-08](../chapters/01-08-sequences-series-and-taylor.md)

Every numerical answer below is listed in the answer key at the end and is recomputed independently by [verify_01_08.py](../verify/verify_01_08.py).

---

## Solutions

### Solution 01-08.1

(a) Divide by $n$: $\dfrac{2 + 1/n}{3 - 2/n} \to $ **0.6667** (2/3).

(b) Take logs: $n\ln(1 + 2/n) \to 2$ (01-02), so the limit is $e^2 = $ **7.389**.

(c) Geometric, $a = 1$, $r = \tfrac{1}{3}$: $1/(1 - \tfrac{1}{3}) = $ **1.5**.

(d) First term $a = 0.9$, $r = 0.9$: $0.9/0.1 = $ **9**.

(e) Finite geometric: $(2^{10} - 1)/(2 - 1) = $ **1023**: the largest 10-bit unsigned integer.

### Solution 01-08.2

(a) A p-series with $p = 2 > 1$: **converges**, to $\pi^2/6 = $ **1.645**.
(b) The harmonic series: **diverges** ($p = 1$).
(c) Ratio test: $\dfrac{(k + 1)/2^{k+1}}{k/2^k} = \dfrac{k + 1}{2k} \to \tfrac{1}{2} < 1$, so it **converges**, to **2**.
(d) Alternating, with $1/k$ decreasing to 0: **converges** (conditionally), to $\ln2 = $ **0.6931**.
(e) Ratio test: $\dfrac{(k + 1)!/10^{k+1}}{k!/10^k} = \dfrac{k + 1}{10} \to \infty$: **diverges**. The terms shrink for $k < 9$, then grow without bound: factorials beat exponentials eventually.

### Solution 01-08.3

(a) Each series follows from the table in §3.5, with substitutions:

- $e^{-x} = 1 - x + \dfrac{x^2}{2} - \dfrac{x^3}{6} + \cdots$
- $\cos2x = 1 - 2x^2 + \dfrac{2}{3}x^4 - \dfrac{4}{45}x^6 + \cdots$ (substitute $2x$)
- $\dfrac{1}{1 + x} = 1 - x + x^2 - x^3 + \cdots$
- $\ln(1 + x) = x - \dfrac{x^2}{2} + \dfrac{x^3}{3} - \dfrac{x^4}{4} + \cdots$
- $\sqrt{1 + x} = 1 + \dfrac{x}{2} - \dfrac{x^2}{8} + \dfrac{x^3}{16} - \cdots$ (binomial, $\alpha = \tfrac{1}{2}$)

(b) $1 - 0.1 + 0.005 - 0.000167 = $ **0.904833**, against $e^{-0.1} = $ **0.904837**: an error of $-4.1\times10^{-6}$. That is within the alternating bound $0.1^4/24 = 4.2\times10^{-6}$ ✓.

### Solution 01-08.4

(a) The ratio is $\dfrac{k}{k + 1}\lvert x\rvert \to \lvert x\rvert$, so **R = 1**.
(b) The ratio is $\dfrac{\lvert x\rvert}{k + 1} \to 0$ for every $x$, so **R = ∞**.
(c) The ratio is $(k + 1)\lvert x\rvert \to \infty$ unless $x = 0$, so **R = 0**.
(d) The ratio is $\lvert x - 2\rvert/3$, so **R = 3**, centered at 2: it converges for $-1 < x < 5$.

### Solution 01-08.5

(a) With $x[n] = 1$ at $n = 0$ and 0 otherwise: $y[0] = 1$, $y[1] = 0.8$, $y[2] = 0.8^2$, …, so $h[n] = 0.8^n$.

(b) $\sum_{n\ge0}0.8^n = 1/(1 - 0.8) = $ **5**. A unit step input settles at 5.

(c) $0.8^n < 0.01$ when $n > \ln0.01/\ln0.8 = 20.64$, so at **n = 21**.

(d) The geometric series diverges for $\lvert r\rvert \ge 1$: the impulse response $1.1^n$ grows without bound. The filter is **unstable**. The condition $\lvert a\rvert < 1$ is the stability criterion, the discrete-time cousin of "poles in the left half-plane" ([11-09](../../11-signals-and-systems/chapters/11-09-z-transform.md)).

### Solution 01-08.6

(a) $\sum_{k=1}^{30}1.05^{-k} = \dfrac{1 - 1.05^{-30}}{0.05} = $ **15.37**.

(b) $1/0.05 = $ **20**: the infinite geometric series.

(c) $\dfrac{1 - 1.08^{-10}}{0.08} = 6.710$, so **\$6.710 M**. This is the number to set against the upgrade's capital cost.

(d) At 0% the ratio is $r = 1$, so the series is $1 + 1 + 1 + \cdots$, which diverges. A finite value needs $\lvert r\rvert < 1$, i.e. a positive discount rate.

### Solution 01-08.7

(a) $1 - 0.125 + 0.0026042 = $ **0.8776042**, against $\cos0.5 = $ **0.8775826**: an error of **2.160×10^−5**. The alternating-series bound (the first omitted term) is $0.5^6/720 = $ **2.170×10^−5** ✓.

(b) The bounds at $x = \pi/2$:

| Last term kept | Number of terms | Bound |
|---|---|---|
| $x^7$ | 4 | $1.6\times10^{-4}$ |
| $x^9$ | 5 | $3.6\times10^{-6}$ |
| $x^{11}$ | 6 | $5.7\times10^{-8}$ |

So **6 terms** (through $x^{11}$) are needed. Reducing the argument to $\lvert x\rvert \le \pi/4$ first would save two terms, which is why math libraries reduce arguments before evaluating series.

### Solution 01-08.8

(a) $\sqrt{1.05} \approx 1 + 0.025 = $ **1.025**. The next term is $-x^2/8 = $ **−3.125×10^−4**. Exact: **1.024695**, an actual error of $-3.05\times10^{-4}$ ✓.

(b) $1/(1 - 0.02) \approx 1.02$. The next term is $+x^2 = $ **4×10^−4**. Exact: **1.020408** ✓.

(c) $1.03^5 \approx 1 + 5(0.03) = $ **1.15**. The next term is $\binom{5}{2}x^2 = $ **0.009**. Exact: **1.159274**, an actual error of 0.00927 ✓. Compounding adds visibly to the linear estimate even at 3%.

### Solution 01-08.9

(a) $G = \dfrac{2\times10^5}{1 + 2\times10^5/11} = $ **10.99940**. The relative error is $1 - G\beta = $ **55.00 ppm**, and $1/(A\beta) = 11/2\times10^5 = $ **55.00 ppm**: identical to four digits.

(b) With $A = 1000$: $G = $ **10.88032**, an error of **1.088%**. The first-order estimate gives **1.1%**. It is still adequate as a rough figure, but the second-order term (0.012%) is now visible.

(c) $1/(A\beta) = 10^{-4}$ gives $A\beta = 10^4$, so $A = 1.1\times10^5$ (101 dB) for this gain of 11.

### Solution 01-08.10

(a) $j^2 = -1$, $j^3 = -j$, $j^4 = 1$. So the even-power terms of $e^{j\theta}$ are real, with alternating signs, giving the cosine series. The odd-power terms are $j$ times real numbers with alternating signs, giving $j$ times the sine series. The series converges absolutely, so the regrouping is valid.

(b) The partial sum through $(j\pi/3)^6/6!$ is $0.49996 + j0.86630$. The exact value is $0.5 + j0.86603$, and the magnitude of the error is **2.72×10^−4**.

### Solution 01-08.11

(a) $f(x \pm h) = f \pm hf' + \tfrac{h^2}{2}f'' \pm \tfrac{h^3}{6}f''' + O(h^4)$. Then:

- $\dfrac{f(x + h) - f(x)}{h} = f' + \tfrac{h}{2}f'' + O(h^2)$;
- $\dfrac{f(x + h) - f(x - h)}{2h} = f' + \tfrac{h^2}{6}f''' + O(h^4)$. The even terms cancel in the subtraction, and the next surviving term is of order $h^4$.

(b) For $f = e^x$ at 0, all derivatives are 1. Forward error: **0.05171** (predicted $h/2 = 0.05$). Central error: **0.0016675** (predicted $h^2/6 = 0.0016667$) ✓.

(c) $D_R$ has error **−2.08×10^−7**: the $h^2$ terms cancel, leaving an $h^4$ error. This "extrapolation to zero step" is the principle behind Romberg integration and adaptive ODE solvers.

### Solution 01-08.12

(a) With $a_1 = 1$ and $a_3 = -0.05$: fundamental $a_1A + \tfrac{3}{4}a_3A^3 = 1 - 0.0375 = $ **0.9625 V**. Third harmonic $\tfrac{1}{4}\lvert a_3\rvert A^3 = 0.0125$ V, so HD3 $= 0.0125/0.9625 = $ **1.299%**.

(b) The fundamental's gain is $1 - \tfrac{3}{4}(0.05)A^2$. Set it to $10^{-1/20} = 0.8913$: $0.0375A^2 = 0.1087$, so $A_{1dB} = $ **1.703 V**.

(c) $A_{IP3} = \sqrt{\tfrac{4}{3}\cdot\tfrac{1}{0.05}} = $ **5.164 V**. The ratio is $20\log_{10}(5.164/1.703) = $ **9.636 dB**. Both amplitudes scale as $\sqrt{a_1/\lvert a_3\rvert}$, so $a_3$ cancels from their ratio: $A_{IP3}^2/A_{1dB}^2 = \dfrac{4/3}{\tfrac{4}{3}(1 - 10^{-1/20})} = 9.19$, i.e. 9.6 dB. This is the textbook "IP3 is about 10 dB above P1dB" rule.

### Solution 01-08.13

| $A$ (mV) | Taylor $A/(4V_T)$ | Exact $I_2/I_1$ |
|---|---|---|
| 1 | **0.9671%** | **0.9671%** |
| 5 | 4.836% | 4.828% |
| 10 | 9.671% | 9.611% |
| 25.85 | 25.00% | 24.02% |

The Taylor estimate overstates HD2 slightly, and its relative error grows roughly as $A^2$. It reaches 1% of its own value at about **12.8 mV**, half of $V_T$. Below that the simple formula is excellent.

### Solution 01-08.14

(a) Alternating, decreasing terms: after $N$ terms the error in π is below $4/(2N + 1)$. Requiring $4/(2N + 1) \le 10^{-6}$ gives $N \ge 1\,999\,999.5$, so **2 000 000 terms**.

(b) With 5 terms each: $16\arctan\tfrac{1}{5} - 4\arctan\tfrac{1}{239} = $ **3.14159268**, an error of **2.9×10^−8**, already better than (a) needs.

(c) The arctan series has radius 1. At $x = 1$ we sit *on* the boundary, where convergence is slowest: the terms shrink only like $1/(2k + 1)$. At $x = 1/5$ the terms shrink by a factor of 25 per step, and at $1/239$ by 57,000. Convergence is fast deep inside the radius and slow near its edge. Good numerical algorithms transform a problem so that the series is evaluated near its center.

### Solution 01-08.15

(a) Launched wave $1\times50/75 = $ **0.6667 V**; $\Gamma_s = (25 - 50)/75 = $ **−0.3333**; $\Gamma_L = (100 - 50)/150 = $ **0.3333**.

(b) The far-end voltage after $n$ arrivals is $V_l(1 + \Gamma_L)\sum_{k=0}^{n-1}(\Gamma_s\Gamma_L)^k$, with ratio $-1/9$. The limit is $\dfrac{0.6667\times1.3333}{1 + 1/9} = $ **0.8 V**, equal to the DC divider $100/125 = 0.8$ ✓.

(c) The partial sums are 0.8889, 0.7901, 0.8011, …, with errors of 11.1%, 1.23% and 0.137%. The first arrival within 1% is **the 3rd**. A ratio of $-1/9$ settles fast; the open line of chapter Example 01-08.1 (ratio $-2/3$) rings much longer.

---

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 01-08.1a | (a) | 0.6667 | — |
| 01-08.1b | (b) | 7.389 | — |
| 01-08.1c | (c) | 1.5 | — |
| 01-08.1d | (d) | 9 | — |
| 01-08.1e | (e) | 1023 | — |
| 01-08.2a | sum of 1/k² | 1.645 | — |
| 01-08.2b | sum of k/2^k | 2 | — |
| 01-08.2c | alternating harmonic sum | 0.6931 | — |
| 01-08.3a | four-term e^(−0.1) | 0.904833 | — |
| 01-08.3b | e^(−0.1) | 0.904837 | — |
| 01-08.4a | radius for (d) | 3 | — |
| 01-08.5a | DC gain | 5 | — |
| 01-08.5b | samples to fall below 1 % | 21 | — |
| 01-08.6a | 30-year annuity factor | 15.37 | — |
| 01-08.6b | perpetuity factor | 20 | — |
| 01-08.6c | PV of savings | 6.710 | $M |
| 01-08.7a | three-term cos 0.5 | 0.8776042 | — |
| 01-08.7b | cos 0.5 | 0.8775826 | — |
| 01-08.7c | actual error | 2.160×10^-5 | — |
| 01-08.7d | alternating bound | 2.170×10^-5 | — |
| 01-08.7e | sine terms for 1e−6 | 6 | — |
| 01-08.8a | √1.05 estimate | 1.025 | — |
| 01-08.8b | next-term estimate | −3.125×10^-4 | — |
| 01-08.8c | √1.05 exact | 1.024695 | — |
| 01-08.8d | 1/0.98 exact | 1.020408 | — |
| 01-08.8e | next term for 1/0.98 | 4×10^-4 | — |
| 01-08.8f | 1.03^5 exact | 1.159274 | — |
| 01-08.8g | next term for 1.03^5 | 0.009 | — |
| 01-08.9a | gain with A = 2e5 | 10.99940 | — |
| 01-08.9b | error with A = 2e5 | 55.00 | ppm |
| 01-08.9c | gain with A = 1000 | 10.88032 | — |
| 01-08.9d | error with A = 1000 | 1.088 | % |
| 01-08.10a | error magnitude of partial sum | 2.72×10^-4 | — |
| 01-08.11a | forward error | 0.05171 | — |
| 01-08.11b | central error | 0.0016675 | — |
| 01-08.11c | Richardson error | −2.08×10^-7 | — |
| 01-08.12a | fundamental at 1 V | 0.9625 | V |
| 01-08.12b | HD3 at 1 V | 1.299 | % |
| 01-08.12c | 1 dB compression amplitude | 1.703 | V |
| 01-08.12d | IP3 amplitude | 5.164 | V |
| 01-08.12e | IP3 / P1dB | 9.636 | dB |
| 01-08.13a | Taylor HD2 at 1 mV | 0.9671 | % |
| 01-08.13b | exact HD2 at 1 mV | 0.9671 | % |
| 01-08.13c | exact HD2 at 25.85 mV | 24.02 | % |
| 01-08.13d | amplitude where Taylor errs by 1 % | 12.8 | mV |
| 01-08.14a | Leibniz terms | 2000000 | — |
| 01-08.14b | Machin, 5 terms each | 3.14159268 | — |
| 01-08.14c | Machin error | 2.9×10^-8 | — |
| 01-08.15a | launched wave | 0.6667 | V |
| 01-08.15b | Γ_s | −0.3333 | — |
| 01-08.15c | Γ_L | 0.3333 | — |
| 01-08.15d | final far-end voltage | 0.8 | V |
| 01-08.15e | arrivals to within 1 % | 3 | — |
