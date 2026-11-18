# Solutions 03-04 · Joint Distributions, Correlation and the CLT

Problems: [03-04 problems](../problems/03-04-problems.md) · Chapter: [03-04](../chapters/03-04-joint-distributions-and-clt.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_03_04.py](../verify/verify_03_04.py).

---

## Solutions

### Solution 03-04.1

(a) Row sums give $P(X = 0) = $ **0.6** and $P(X = 1) = $ **0.4**; column sums give $P(Y = 0, 1, 2) = $ **0.4**, **0.35**, **0.25**. Independence fails: $p_{XY}(0, 0) = 0.30$ but $P(X = 0)P(Y = 0) = 0.24$.

(b) $P(Y = 2 \mid X = 1) = 0.15/0.4 = $ **0.375**, against $P(Y = 2) = 0.25$ overall: bad dies are flagged more often.

(c) $\mathbb{E}[X] = $ **0.4**; $\mathbb{E}[Y] = 0.35 + 2(0.25) = $ **0.85**; $\mathbb{E}[XY] = 1(0.15) + 2(0.15) = 0.45$, so $\operatorname{Cov}(X, Y) = 0.45 - 0.4\times0.85 = $ **0.11**. With $\operatorname{Var}(X) = 0.24$ and $\operatorname{Var}(Y) = 0.35 + 4(0.25) - 0.85^2 = 0.6275$, $\rho = 0.11/\sqrt{0.24\times0.6275} = $ **0.2835**. The scan is informative but weakly so.

### Solution 03-04.2

(a) $\int_0^1\int_0^1(x + y)\,dx\,dy = 1/2 + 1/2 = 1$, so $c = $ **1**. $f_X(x) = \int_0^1(x + y)\,dy = x + 1/2$.

(b) $P(X + Y < 1) = \int_0^1\int_0^{1-x}(x + y)\,dy\,dx = \int_0^1\big[x(1 - x) + (1 - x)^2/2\big]dx = 1/6 + 1/6 = $ **0.3333**.

(c) $\mathbb{E}[X] = \int_0^1x(x + 1/2)\,dx = 1/3 + 1/4 = $ **0.5833** (and $\mathbb{E}[Y]$ the same by symmetry). $\mathbb{E}[XY] = \int\int xy(x + y) = 1/6 + 1/6 = $ **0.3333**. $\operatorname{Cov} = 1/3 - 49/144 = -1/144 = $ **−0.006944**. $\operatorname{Var}(X) = 5/12 - 49/144 = 11/144$, so $\rho = -1/11 = $ **−0.09091**. Not independent: $f_{XY} = x + y$ is not $(x + 1/2)(y + 1/2)$.

### Solution 03-04.3

$\mathbb{E}[X] = 0$ and $\mathbb{E}[XY] = \mathbb{E}[X^3] = (-1 + 0 + 1)/3 = 0$, so $\operatorname{Cov}(X, Y) = 0 - 0\cdot\mathbb{E}[Y] = 0$: uncorrelated. But $P(Y = 1 \mid X = 0) = 0$ while $P(Y = 1) = 2/3$: dependent. A power detector ($Y = X^2$) has exactly this structure: its output is uncorrelated with a symmetric input yet completely determined by it. Correlation detects only linear dependence.

### Solution 03-04.4

(a) Worst case: all ten at +10 Ω, a deviation of **100 Ω**. Each deviation has σ = $20/\sqrt{12} = 5.774$ Ω, so the total has σ = $\sqrt{10}\times5.774 = $ **18.26 Ω**.

(b) 50 Ω is $50/18.26 = 2.739$σ, so the CLT gives $2Q(2.739) = $ **0.006170**.

(c) The CLT overestimates by 25%. Each term is bounded, so the sum can never exceed 100 Ω, and its tails fall faster than a Gaussian's (Figure 1). The CLT is accurate near the center; at 2.7σ with only ten terms, the bounded shape still shows. For tolerance analysis this error is on the safe side.

### Solution 03-04.5

(a) $\sqrt{3^2 + 4^2 + 12^2} = \sqrt{169} = $ **13.00 µV**.

(b) $\sqrt{9 + 16 + 36} = $ **7.810 µV**. Halving the dominant source helps far more than eliminating both small ones (which would leave 12 µV): in an RSS budget, attack the largest term.

(c) Fully correlated sources add as amplitudes: $3 + 4 = 7$ µV, then RSS with the independent 12 µV: $\sqrt{49 + 144} = $ **13.89 µV**.

### Solution 03-04.6

(a) $\sigma_d = 20\sqrt{2(1 - 0.95)} = $ **6.325 mV**.

(b) $20\sqrt{2(1 - \rho)} \le 2$ requires $1 - \rho \le 0.005$: ρ ≥ **0.995**. The two wires must see almost identical interference, which demands tight physical symmetry: matched routing, equal coupling to aggressors, twisted or closely coupled pairs. A small asymmetry converts common-mode interference into differential noise.

### Solution 03-04.7

The total is Poisson with mean $0.27 + 0.05 = 0.32$ per year (§3.4). (a) $e^{-0.32} = $ **0.7261**. (b) $0.32^2e^{-0.32}/2 = $ **0.03718**.

### Solution 03-04.8

(a) For $t \ge 0$, $f_T(t) = \int_0^tre^{-rs}\cdot re^{-r(t-s)}\,ds = r^2e^{-rt}\int_0^tds = r^2t\,e^{-rt}$ (an Erlang distribution). Its mean is $1/r + 1/r = 2/r = $ **200,000 h**, and $R(t) = \int_t^\infty r^2se^{-rs}ds = (1 + rt)e^{-rt}$.

(b) At $rt = 0.1$: cold spare $1.1e^{-0.1} = $ **0.9953**; hot spare $2e^{-0.1} - e^{-0.2} = $ **0.9909**. The cold spare wins because it does not age while waiting, and its MTTF is double a single part's against 1.5 times for the hot pair. The price is a switch-over that must work when needed, and a spare that starts cold.

### Solution 03-04.9

$1.96\times5/\sqrt n \le 0.5$ gives $n \ge (1.96\times10)^2 = 384.1$ (with $z = 1.95996$), so **385** samples.

### Solution 03-04.10

(a) Mean $600\times0.1 = $ **60**, σ = $\sqrt{600\times0.1\times0.9} = $ **7.348**.

(b) $P(N > 75) = P(N \ge 76) \approx Q\big((75.5 - 60)/7.348\big) = Q(2.109) = $ **0.01746**.

(c) The exact value is 0.02000, so the CLT is 13% low. The binomial with small $p$ is skewed right (like the Poisson), so its upper tail is heavier than the symmetric Gaussian's. In the opposite case of Problem 03-04.4 (bounded, light tails) the CLT erred the other way; in both, the error grows the further out you go.

### Solution 03-04.11

(a) $\operatorname{Var}\big(\tfrac1n\sum X_i\big) = \tfrac{1}{n^2}\big[n\sigma^2 + n(n - 1)\rho\sigma^2\big] = \sigma^2\Big[\frac1n + \rho\frac{n - 1}{n}\Big] = \sigma^2\Big[\rho + \frac{1 - \rho}{n}\Big]$.

(b) $\sqrt{0.01 + 0.99/100} = $ **0.1411**, against 0.1 for independent samples; as $n \to \infty$ it falls only to $\sqrt{0.01} = $ **0.1**.

(c) A correlation of just 1% sets a floor: no amount of averaging gets below $\sqrt\rho\,\sigma$. Slow drift, 1/f noise and shared interference are exactly such correlated components, which is why long averages stop improving and why measurement systems chop, auto-zero or calibrate instead (03-06, [20](../../20-analog-and-mixed-signal-ic-design/README.md)).

### Solution 03-04.12

(a) $\mathbb{E}[B \mid A = 0.73] = 0.75 + 0.9(0.73 - 0.75) = $ **0.732 V**; $\sigma_{B\mid A} = 10\sqrt{1 - 0.81} = $ **4.359 mV**.

(b) $P(B < 0.72 \mid A) = \Phi\big((0.72 - 0.732)/0.004359\big) = \Phi(-2.753) = $ **0.002953**, against $Q(3) = $ **0.001350** unconditionally: the low reading at A roughly doubles the risk at B, and the tighter conditional spread is what keeps it from being worse.

### Solution 03-04.13

(a) The envelope is Rayleigh with $\sigma = 1$ mV; $\mathbb{E}[R] = \int_0^\infty r\cdot(r/\sigma^2)e^{-r^2/(2\sigma^2)}dr = \sigma\sqrt{\pi/2} = $ **1.253 mV**.

(b) $P(R > 3) = e^{-9/2} = $ **0.01111**.

(c) $\mathbb{E}[R^2] = 2\sigma^2 = $ **2 mV²**. The phase is uniform on $[0, 2\pi)$ and independent of the envelope.

### Solution 03-04.14

(a) $\operatorname{Var}(X_1 - 2X_2) = 4 + 4(1) - 2\cdot2\cdot\operatorname{Cov} = 8 - 4(0.6\times2\times1) = $ **3.2**.

(b) $\operatorname{Var}(X_1 - aX_2) = 4 - 2a(1.2) + a^2$, minimized at $a = 1.2$ (setting the derivative $-2.4 + 2a$ to zero), with minimum $4 - 2.88 + 1.44 = $ **2.56**.

(c) $a = \operatorname{Cov}/\sigma_2^2 = \rho\sigma_1/\sigma_2$ is the regression slope of §3.7, and the minimum $\sigma_1^2(1 - \rho^2)$ is the conditional variance: subtracting the best linear prediction of $X_1$ from $X_2$ removes exactly the correlated part. In finance this is the minimum-variance hedge ratio. In electronics it is how a reference sensor, a replica circuit or an adaptive canceler removes correlated noise; the residual $\sqrt{1 - \rho^2}$ shows why cancellation needs very high correlation.

### Solution 03-04.15

(a) At $p = 10^{-4}$, $p_s = 1 - (1 - 10^{-4})^{10}$ and $np_s = 0.5438$. The exact binomial tail $P(N \ge 16)$ is **1.360×10⁻¹⁸**; the Poisson approximation gives **1.674×10⁻¹⁸**.

(b) Solving $\text{UCR}(p) = 10^{-10}$ by bisection on $\log\text{UCR}$ gives $p = $ **3.338×10⁻⁴**.

(c) With $t = 7$ and $n = 528$: mean 1.266 wrong symbols, and $P(N \ge 8) = $ **5.154×10⁻⁵**, about $6\times10^7$ times worse than RS(544,514)'s $8.152\times10^{-13}$. Doubling the correction capability moves the failure point from 8 to 16 errors, deep into a tail that falls roughly like $\lambda^k/k!$. Stronger codes cost parity overhead and decoder power and latency, which is the tradeoff standards bodies weigh.

### Solution 03-04.16

(a) Random errors: $P(\text{Poisson}(1.304) \ge 16) = $ **9.839×10⁻¹³**. Paired errors: $P(\text{Poisson}(0.652) \ge 8) = $ **4.552×10⁻⁷**, about $4.6\times10^5$ times worse with the same average number of wrong symbols. Pairing halves the number of independent events needed to fail.

(b) Solve $P(\text{Poisson}(\lambda_b) \ge 8) = 9.839\times10^{-13}$: $\lambda_b = $ **0.1204** bursts, or **0.2408** wrong symbols per codeword. Since $p_s \approx mp$ at these rates, the pre-FEC BER must fall in the same ratio, to about $2.4\times10^{-4}\times0.2408/1.304 = $ **4.431×10⁻⁵**: 5.4 times lower.

(c) This is the effect the IEEE analyses capture with their burst parameter $a$ (§9): correlated errors demand a lower pre-FEC BER, and interleaving codewords, which separates the symbols of a burst into different codewords, recovers much of the loss.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 03-04.1a | P(X = 0) | 0.6 | — |
| 03-04.1b | P(X = 1) | 0.4 | — |
| 03-04.1c | P(Y = 0) | 0.4 | — |
| 03-04.1d | P(Y = 1) | 0.35 | — |
| 03-04.1e | P(Y = 2) | 0.25 | — |
| 03-04.1f | P(Y = 2 given X = 1) | 0.375 | — |
| 03-04.1g | E[X] | 0.4 | — |
| 03-04.1h | E[Y] | 0.85 | — |
| 03-04.1i | covariance | 0.11 | — |
| 03-04.1j | correlation coefficient | 0.2835 | — |
| 03-04.1k | Var(Y) | 0.6275 | — |
| 03-04.2a | c | 1 | — |
| 03-04.2b | P(X + Y < 1) | 0.3333 | — |
| 03-04.2c | E[X] | 0.5833 | — |
| 03-04.2d | E[XY] | 0.3333 | — |
| 03-04.2e | covariance | −0.006944 | — |
| 03-04.2f | correlation coefficient | −0.09091 | — |
| 03-04.4a | worst-case deviation | 100 | Ω |
| 03-04.4b | standard deviation of the total | 18.26 | Ω |
| 03-04.4c | CLT estimate of P(deviation > 50 Ω) | 0.006170 | — |
| 03-04.4d | 50 Ω in standard deviations | 2.739 | — |
| 03-04.4e | exact P(deviation > 50 Ω) | 0.004938 | — |
| 03-04.4f | CLT overestimate | 25 | % |
| 03-04.5a | total noise | 13.00 | µV |
| 03-04.5b | total with the largest source halved | 7.810 | µV |
| 03-04.5c | total with two sources correlated | 13.89 | µV |
| 03-04.6a | differential noise at ρ = 0.95 | 6.325 | mV |
| 03-04.6b | correlation needed for 2 mV | 0.995 | — |
| 03-04.7a | P(no upset) | 0.7261 | — |
| 03-04.7b | P(two upsets) | 0.03718 | — |
| 03-04.8a | cold-spare MTTF | 200000 | h |
| 03-04.8b | cold-spare reliability at 10,000 h | 0.9953 | — |
| 03-04.8c | hot-spare reliability at 10,000 h | 0.9909 | — |
| 03-04.9a | samples required | 385 | — |
| 03-04.9b | unrounded sample count | 384.1 | — |
| 03-04.10a | mean defective dies | 60 | — |
| 03-04.10b | standard deviation | 7.348 | — |
| 03-04.10c | CLT estimate of P(N > 75) | 0.01746 | — |
| 03-04.10d | standardized distance | 2.109 | — |
| 03-04.10e | exact P(N > 75) | 0.02000 | — |
| 03-04.10f | CLT shortfall | 13 | % |
| 03-04.11a | standard error at n = 100 | 0.1411 | — |
| 03-04.11b | standard-error floor | 0.1 | — |
| 03-04.12a | conditional mean of B | 0.732 | V |
| 03-04.12b | conditional standard deviation of B | 4.359 | mV |
| 03-04.12c | P(B < 0.72 V given A) | 0.002953 | — |
| 03-04.12d | P(B < 0.72 V) unconditionally | 0.001350 | — |
| 03-04.13a | mean envelope | 1.253 | mV |
| 03-04.13b | P(envelope > 3 mV) | 0.01111 | — |
| 03-04.13c | mean power | 2 | mV² |
| 03-04.14a | Var(X1 − 2X2) | 3.2 | — |
| 03-04.14b | optimal coefficient | 1.2 | — |
| 03-04.14c | minimum variance | 2.56 | — |
| 03-04.15a | UCR at 1e-4, exact | 1.360×10^-18 | — |
| 03-04.15b | UCR at 1e-4, Poisson | 1.674×10^-18 | — |
| 03-04.15c | pre-FEC BER for UCR 1e-10 | 3.338×10^-4 | — |
| 03-04.15d | UCR of the t = 7 code | 5.154×10^-5 | — |
| 03-04.15e | mean wrong symbols at 1e-4 | 0.5438 | — |
| 03-04.15f | mean wrong symbols, t = 7 code | 1.266 | — |
| 03-04.15g | failure ratio of the weaker code | 6×10^7 | — |
| 03-04.16a | UCR, random errors | 9.839×10^-13 | — |
| 03-04.16b | UCR, paired errors | 4.552×10^-7 | — |
| 03-04.16c | required mean bursts | 0.1204 | — |
| 03-04.16d | required mean wrong symbols | 0.2408 | — |
| 03-04.16e | required pre-FEC BER | 4.431×10^-5 | — |
| 03-04.16f | paired over random failure ratio | 4.6×10^5 | — |
| 03-04.16g | required BER reduction factor | 5.4 | — |
