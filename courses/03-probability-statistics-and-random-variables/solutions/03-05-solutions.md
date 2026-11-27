# Solutions 03-05 · Estimation and Hypothesis Testing for Engineers

Problems: [03-05 problems](../problems/03-05-problems.md) · Chapter: [03-05](../chapters/03-05-estimation-and-hypothesis-testing.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_03_05.py](../verify/verify_03_05.py).

---

## Solutions

### Solution 03-05.1

\$\bar x = 25/5 = \$ **5 mV**. Deviations −2, 0, −1, 1, 2 have squares summing to 10, so \$s^2 = 10/4 = \$ **2.5 mV²**, \$s = \$ **1.581 mV** and the standard error is \$s/\sqrt5 = \$ **0.7071 mV**. Dividing by $n$ gives **2.0 mV²**. That estimator averages $(n - 1)\sigma^2/n$, 20% low here, because the deviations are measured from $\bar x$, which is fitted to these same five numbers and so sits closer to them than the true mean does.

### Solution 03-05.2

The standard error is $2/\sqrt{16} = 0.5$ nA, so the interval is $10.3 \pm 1.960\times0.5 = 10.3 \pm 0.9800$: **[9.320, 11.28] nA**. "95%" describes the procedure: if the experiment were repeated many times, 95% of the intervals so constructed would contain the true current. This particular interval either does or does not.

### Solution 03-05.3

With ν = 4, $t_{0.025,4} = 2.776$ and the half-width is \$2.776\times0.7071 = \$ **1.963 mV**: **[3.037, 6.963] mV**. Using 1.960 would give a half-width of **1.386 mV**, so the t-interval is **41.66%** wider. With five samples, $s$ itself is very uncertain, and the t distribution pays for it.

### Solution 03-05.4

(a) $n \ge (1.960\times3/0.5)^2 = 138.3$, so **139** measurements.

(b) $n \ge 1.960^2\times0.9\times0.1/0.01^2 = 3457.3$, so **3458** dies.

(c) $p(1 - p)$ is largest at $p = 0.5$: $n \ge 1.960^2\times0.25/0.01^2 = 9603.6$, so **9604**. Prior knowledge that the yield is high cuts the sample by almost two-thirds.

### Solution 03-05.5

(a) \$\hat p = 46/500 = \$ **0.092**, standard error \$\sqrt{0.092\times0.908/500} = \$ **0.01293**, and the interval is $0.092 \pm 0.02533$: **[0.06667, 0.1173]**.

(b) \$1 - 0.05^{1/1000} = \$ **0.002991**, against $3/1000 = 0.003$ from the rule of three.

### Solution 03-05.6

(a) With ν = 99, the chi-square quantiles are $\chi^2_{0.025} = 73.36$ and $\chi^2_{0.975} = 128.4$, so

$$
0.40\sqrt{99/128.4} \le \sigma \le 0.40\sqrt{99/73.36}: \quad [0.3512, 0.4647]\ \text{ps} .
$$

So **0.3512** to **0.4647 ps**.

(b) At the estimate, $14.069\times0.40 = $ **5.628 ps**; at the upper limit, $14.069\times0.4647 = $ **6.537 ps**. A conservative budget must carry about 0.9 ps for the uncertainty of the jitter measurement itself.

### Solution 03-05.7

Point estimate: $2/(5\times10^8)$ per hour \$= \$ **4 FIT**. With $c = 2$, $\lambda_U = 5.322$ at 90%, so $r_U = 5.322/(5\times10^8)$, or **10.64 FIT**. With no failures, $\lambda_U = 2.303$: **4.605 FIT**.

### Solution 03-05.8

(a) $z = (93 - 100)/(20/\sqrt{25}) = $ **−1.75**; one-sided p-value $\Phi(-1.75) = $ **0.04006**.

(b) $0.040 < 0.05$: reject $H_0$; the evidence favors lower leakage.

(c) Two-sided, \$p = \$ **0.08012**, not significant at 5%. The one-sided test is appropriate only if the direction was specified before seeing the data (the change was designed to lower leakage and an increase would be treated the same as no improvement). Choosing the sidedness after looking at the data halves the reported p-value, and so doubles the true significance level: you would reject whenever $|z| > 1.645$, which under $H_0$ happens 10% of the time, so a nominal 5% test is really a 10% test.

### Solution 03-05.9

(a) Reject when $\bar x \le 100 - 1.645\times4 = $ **93.42 nA**.

(b) If μ = 90 nA, $P(\bar X \le 93.42) = \Phi\big((93.42 - 90)/4\big) = \Phi(0.8551) = $ **0.8038**.

(c) $n = \big((1.645 + 1.282)\times20/10\big)^2 = 34.26$, so **35** parts.

### Solution 03-05.10

(a) $1 - 0.95^{20} = $ **0.6415**: more likely than not, some parameter "fails".

(b) Bonferroni tests each at $0.05/20 = $ **0.0025**, giving an overall false-alarm probability of $1 - 0.9975^{20} = $ **0.04883**, just under 5%. The price is lower power for each individual test.

### Solution 03-05.11

(a) $C_p = 100/72 = $ **1.389**; $C_{pu} = (50 - 10)/36 = $ **1.111**; $C_{pl} = (10 + 50)/36 = $ **1.667**; $C_{pk} = $ **1.111**.

(b) $Q(40/12) + Q(60/12) = Q(3.333) + Q(5) = $ **429.3 ppm**, almost all above the upper limit.

(c) Centering makes $C_{pk} = C_p = 1.389$ and the rate \$2Q(50/12) = \$ **30.91 ppm**. Keeping the +10 ppm offset, $C_{pk} = 40/(3\sigma) = 4/3$ needs σ = **10.00 ppm**, a 17% cut in spread. Centering (trimming the crystal load or calibrating) is usually far cheaper.

### Solution 03-05.12

(a) $\text{SE} = \sqrt{1/270 + 2.25/58} = $ **0.2061**, and the bound is $1.5 - 1.645\times0.2061 = $ **1.161**.

(b) Solve $1.5 - 1.645\sqrt{1/(9n) + 2.25/(2(n - 1))} = 1.33$ numerically: $n = 116.6$, so **117** parts. Demonstrating capability takes far more data than estimating it.

### Solution 03-05.13

(a) Robust sigma \$= (2.37 - 2.10)/1.35 = \$ **0.2 µA**, so the static limits are $2.23 \pm 6\times0.2$: **[1.03, 3.43] µA**.

(b) $2.30 \pm 6\times0.35$: **[0.20, 4.40] µA**.

(c) The 3.6 µA part passes the datasheet and the ordinary limits, but the robust PAT limit (3.43 µA) rejects it. The defective parts inflated the ordinary standard deviation and so widened the very limits meant to catch them; the median and quartiles barely move when a few outliers are added.

### Solution 03-05.14

(a) $R(10) = e^{-(10/20)^3} = $ **0.8825**.

(b) $h(10) = (3/20)(10/20)^2 = $ **0.0375** per year.

(c) $B_{10} = 20(-\ln0.9)^{1/3} = $ **9.446 years**.

(d) MTTF $= 20\,\Gamma(4/3) = $ **17.86 years**; median $= 20(\ln2)^{1/3} = $ **17.70 years**. With γ = 3 the hazard rises with age: wear-out, the right-hand wall of the bathtub. One unit in ten has failed by 9.4 years, though the MTTF is almost 18.

### Solution 03-05.15

(a) The life ratio equals the acceleration factor: $4000/1200 = \exp[(E_a/k)(1/423.15 - 1/448.15)]$, so

$$
E_a = \frac{k\ln(4000/1200)}{1/423.15 - 1/448.15} = 0.7870\ \text{eV} .
$$

So $E_a = $ **0.7870 eV**.

(b) From 150 °C to 105 °C, $AF = \exp[(0.7870/k)(1/378.15 - 1/423.15)] = $ **13.04**, so the median life is $4000\times13.04 = $ **52,175 h**, or **5.952 years**.

(c) Two points always fit a line; they cannot show whether a single mechanism with constant $E_a$ holds from 105 to 175 °C, and an error in $E_a$ is amplified exponentially in the extrapolation. Use at least three stress temperatures (to check linearity on an Arrhenius plot), enough units per cell to estimate the medians well, failure analysis to confirm the same mechanism at every temperature, and stress conditions as close to use as test time allows.

### Solution 03-05.16

(a) At 60% confidence with zero failures, $\lambda_U = 0.9163$, so the equivalent device-hours must be at least \$0.9163\times10^9/20 = \$ **4.581×10⁷ h**. With $AF = 77.65$, each unit contributes $77{,}650$ h, so $N \ge 4.581\times10^7/77{,}650 = 590.0$: **591** units.

(b) At 0.5 eV, $AF = \exp[(0.5/k)(1/328.15 - 1/398.15)] = $ **22.39**, so 591 units demonstrate only $0.9163\times10^9/(591\times1000\times22.39) = $ **69.24 FIT**.

(c) The same test "demonstrates" 20 FIT or 69 FIT depending on an assumed activation energy that the test itself does not measure. FIT claims are only as good as the acceleration model; ask which $E_a$ was assumed, for which mechanisms, and what supports it.

### Solution 03-05.17

(a) The differences are 0.08, 0.05, 0.09, 0.05, 0.05, 0.11, 0.02 and 0.09 mV: mean $\bar d = $ **0.0675 mV**, standard deviation $s_d = $ **0.02964 mV**. Then

$$
t = \frac{\bar d}{s_d/\sqrt8} = \frac{0.0675}{0.010480} = 6.441 ,
$$

so $t = $ **6.441** with 7 degrees of freedom, and the one-sided p-value is **1.766×10⁻⁴**: the update clearly lowers offset.

(b) The before and after samples have standard deviations **0.2622** and **0.2347 mV**, so $\text{SE} = \sqrt{0.2622^2/8 + 0.2347^2/8} = $ **0.1244 mV** and $t = 0.0675/0.1244 = $ **0.5425**. The Welch formula gives $\nu = $ **13.83**, and the one-sided p-value is **0.2981**: nothing detected.

(c) The unit-to-unit spread of offsets (about 0.25 mV) is about eight times the spread of the changes (0.03 mV). Pairing subtracts each unit from itself and removes the shared part, exactly the differential trick of 03-04: $\operatorname{Var}(B - A) = \sigma_B^2 + \sigma_A^2 - 2\operatorname{Cov}$, small when before and after are strongly correlated. The unpaired test throws that correlation away. Pair whenever the same units can be measured under both conditions (before/after, two test sockets, two temperatures); when they cannot, as in a split lot, a matched design (pairing wafers or lots) recovers some of the benefit.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 03-05.1a | sample mean | 5 | mV |
| 03-05.1b | sample variance | 2.5 | mV² |
| 03-05.1c | sample standard deviation | 1.581 | mV |
| 03-05.1d | standard error | 0.7071 | mV |
| 03-05.1e | variance dividing by n | 2.0 | mV² |
| 03-05.2a | half-width | 0.9800 | nA |
| 03-05.2b | lower limit | 9.320 | nA |
| 03-05.2c | upper limit | 11.28 | nA |
| 03-05.3a | t half-width | 1.963 | mV |
| 03-05.3b | lower limit | 3.037 | mV |
| 03-05.3c | upper limit | 6.963 | mV |
| 03-05.3d | z half-width | 1.386 | mV |
| 03-05.3e | extra width of the t-interval | 41.66 | % |
| 03-05.4a | jitter measurements | 139 | — |
| 03-05.4b | dies for ±1% at 90% yield | 3458 | — |
| 03-05.4c | dies with no prior knowledge | 9604 | — |
| 03-05.5a | failure fraction | 0.092 | — |
| 03-05.5b | standard error | 0.01293 | — |
| 03-05.5c | lower limit | 0.06667 | — |
| 03-05.5d | upper limit | 0.1173 | — |
| 03-05.5e | exact zero-failure bound | 0.002991 | — |
| 03-05.6a | lower limit of rms jitter | 0.3512 | ps |
| 03-05.6b | upper limit of rms jitter | 0.4647 | ps |
| 03-05.6c | chi-square 2.5% quantile, 99 df | 73.36 | — |
| 03-05.6d | chi-square 97.5% quantile, 99 df | 128.4 | — |
| 03-05.6e | random-jitter budget at the estimate | 5.628 | ps |
| 03-05.6f | random-jitter budget at the upper limit | 6.537 | ps |
| 03-05.7a | point estimate | 4 | FIT |
| 03-05.7b | 90% upper bound, two failures | 10.64 | FIT |
| 03-05.7c | 90% upper bound, no failures | 4.605 | FIT |
| 03-05.8a | z statistic | −1.75 | — |
| 03-05.8b | one-sided p-value | 0.04006 | — |
| 03-05.8c | two-sided p-value | 0.08012 | — |
| 03-05.9a | critical sample mean | 93.42 | nA |
| 03-05.9b | power at 90 nA | 0.8038 | — |
| 03-05.9c | sample size for 90% power | 35 | — |
| 03-05.9d | unrounded sample size | 34.26 | — |
| 03-05.10a | false-alarm probability | 0.6415 | — |
| 03-05.10b | Bonferroni per-test level | 0.0025 | — |
| 03-05.10c | overall false-alarm probability, Bonferroni | 0.04883 | — |
| 03-05.11a | Cp | 1.389 | — |
| 03-05.11b | Cpu | 1.111 | — |
| 03-05.11c | Cpl | 1.667 | — |
| 03-05.11d | out-of-specification rate | 429.3 | ppm |
| 03-05.11e | rate after centering | 30.91 | ppm |
| 03-05.11f | σ for Cpk 4/3 | 10.00 | ppm |
| 03-05.12a | standard error at n = 30 | 0.2061 | — |
| 03-05.12b | lower bound at n = 30 | 1.161 | — |
| 03-05.12c | parts needed | 117 | — |
| 03-05.13a | robust sigma | 0.2 | µA |
| 03-05.13b | lower PAT limit | 1.03 | µA |
| 03-05.13c | upper PAT limit | 3.43 | µA |
| 03-05.13d | lower mean ± 6σ limit | 0.20 | µA |
| 03-05.13e | upper mean ± 6σ limit | 4.40 | µA |
| 03-05.14a | reliability at 10 years | 0.8825 | — |
| 03-05.14b | hazard at 10 years | 0.0375 | 1/year |
| 03-05.14c | B10 life | 9.446 | years |
| 03-05.14d | MTTF | 17.86 | years |
| 03-05.14e | median life | 17.70 | years |
| 03-05.15a | activation energy | 0.7870 | eV |
| 03-05.15b | acceleration factor 150 °C to 105 °C | 13.04 | — |
| 03-05.15c | median life at 105 °C | 52175 | h |
| 03-05.15d | median life at 105 °C | 5.952 | years |
| 03-05.16a | device-hours required | 4.581×10^7 | h |
| 03-05.16b | units required | 591 | — |
| 03-05.16c | acceleration factor at 0.5 eV | 22.39 | — |
| 03-05.16d | demonstrated FIT at 0.5 eV | 69.24 | FIT |
| 03-05.17a | mean difference | 0.0675 | mV |
| 03-05.17b | standard deviation of differences | 0.02964 | mV |
| 03-05.17c | paired t statistic | 6.441 | — |
| 03-05.17d | paired one-sided p-value | 1.766×10^-4 | — |
| 03-05.17e | standard deviation before | 0.2622 | mV |
| 03-05.17f | standard deviation after | 0.2347 | mV |
| 03-05.17g | unpaired standard error | 0.1244 | mV |
| 03-05.17h | Welch t statistic | 0.5425 | — |
| 03-05.17i | Welch degrees of freedom | 13.83 | — |
| 03-05.17j | Welch one-sided p-value | 0.2981 | — |
| 03-05.17k | standard error of the mean difference | 0.010480 | mV |
