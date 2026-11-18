# Solutions 03-02 · Random Variables and Distributions

Problems: [03-02 problems](../problems/03-02-problems.md) · Chapter: [03-02](../chapters/03-02-random-variables-and-distributions.md)

Every numerical answer below is listed in the answer key at the end and is recomputed by [verify_03_02.py](../verify/verify_03_02.py).

---

## Solutions

### Solution 03-02.1

(a) The CDF jumps at each value: $F_X(x) = 0$ for $x < 0$, **0.5** on $[0, 1)$, **0.8** on $[1, 2)$, **0.95** on $[2, 3)$ and **1** from 3 on: a staircase.

(b) $P(1 \le X \le 2) = F_X(2) - F_X(0) = 0.95 - 0.5 = $ **0.45** (the CDF at 0, not at 1, because $X = 1$ is included). $P(X > 1) = 1 - F_X(1) = $ **0.2**.

### Solution 03-02.2

(a) $\int_0^2cx^2dx = 8c/3 = 1$, so $c = 3/8 = $ **0.375** (units of 1/(units of $x$)³).

(b) $F_X(x) = \int_0^x\tfrac38u^2du = x^3/8$ for $0 \le x \le 2$ (0 below, 1 above). $F_X(1.5) = 3.375/8 = $ **0.4219**.

(c) $P(X > 1) = 1 - F_X(1) = 1 - 1/8 = $ **0.875**. Most of the probability sits near 2, where the density is largest.

### Solution 03-02.3

Binomial with $n = 20$, $p = 0.05$. (a) $0.95^{20} = $ **0.3585**. (b) $0.95^{20} + 20\times0.05\times0.95^{19} = 0.3585 + $ **0.3774** $= $ **0.7358**. (c) $P(2) = \binom{20}{2}0.05^2\,0.95^{18} = $ **0.1887**, so $P(X \ge 3) = 1 - P(X \le 2) = 1 - (0.7358 + 0.1887) = $ **0.07548**.

### Solution 03-02.4

The defect count is Poisson with λ = $AD_0 = 0.2$.

(a) $Y = e^{-0.2} = $ **0.8187**.

(b) $P(1) = 0.2e^{-0.2} = $ **0.1637**.

(c) Repair saves the one-defect dies: $P(0) + P(1) = e^{-0.2}(1 + 0.2) = $ **0.9825**. Redundancy turns an **18.13%** loss into **1.752%**, which is why memories always carry spare rows and columns.

### Solution 03-02.5

| $k$ | Binomial ($n = 50$, $p = 0.04$) | Poisson (λ = 2) |
|---|---|---|
| 0 | $0.96^{50} = $ **0.1299** | $e^{-2} = $ **0.1353** |
| 2 | $\binom{50}{2}0.04^2\,0.96^{48} = $ **0.2762** | $2e^{-2} = $ **0.2707** |

The Poisson is **4.2%** high at $k = 0$ and **2.0%** low at $k = 2$. Here $p = 0.04$ is not tiny and $n = 50$ is not huge: the factor $(1 - p)^{n}$ is $e^{n\ln(1 - p)}$ with $\ln0.96 = -0.0408$, not $-0.04$, and the binomial cannot exceed 50 events. In Example 03-02.3 ($p = 10^{-4}$, $n = 12{,}000$) these effects are negligible.

### Solution 03-02.6

Geometric with success probability 0.98. (a) Fail, fail, succeed: $0.02^2\times0.98 = $ **3.92×10⁻⁴**. (b) More than two attempts means the first two fail: $0.02^2 = $ **4×10⁻⁴**.

### Solution 03-02.7

(a) $15\times2048 = $ **30,720 FIT**. Per year, $30{,}720\times10^{-9}\times8766 = $ **0.2693** upsets.

(b) Poisson: $P(0) = e^{-0.2693} = $ **0.7639**. About one chip in four sees an upset each year.

(c) $10^4\times30{,}720\times10^{-9}\times24 = $ **7.373** upsets per day. At cluster scale, soft errors are a daily event, so the SRAM must be protected by ECC and the system must log and handle corrected errors.

### Solution 03-02.8

(a) Rate $= 1/\text{MTTF} = 10^{-6}$ per hour $= $ **1000 FIT**.

(b) $1 - e^{-10^{-6}\times8766} = $ **0.8728%**. This annualized failure rate is the useful number; the MTTF of **114** years is not a lifetime.

(c) $e^{-10^{-6}\times87{,}660} = $ **0.9161**.

### Solution 03-02.9

(a) The board survives to $t$ only if every part does. With independent parts, $P(T > t) = e^{-r_1t}e^{-r_2t}e^{-r_3t} = e^{-(r_1 + r_2 + r_3)t}$: exponential with the summed rate, here 1000 FIT. This is why FIT rates of parts in series simply add.

(b) $e^{-10^{-6}\times43{,}830} = $ **0.9571**.

### Solution 03-02.10

(a) $f_e(x) = 1$ mV⁻¹ on $[-0.5, 0.5]$ mV, zero elsewhere. $F_e(x) = 0$ below −0.5, $(x + 0.5)/1$ (with $x$ in mV) on the interval, and 1 above.

(b) $|e| > 0.4$ covers two strips of width 0.1 mV: probability **0.2**. $F_e(0.3) = 0.3 + 0.5 = $ **0.8**.

### Solution 03-02.11

(a) Each limit is $50/15 = 3.333$σ away, so the out-of-spec fraction is $2Q(3.333) = $ **8.581×10⁻⁴**, or **858.1** ppm.

(b) Need $2Q(k) = 10^{-6}$, so $Q(k) = 5\times10^{-7}$ and $k = Q^{-1}(5\times10^{-7}) = $ **4.892**. Then $\sigma = 50/4.892 = $ **10.22 mV**. A **32%** cut in σ buys an **858**-fold cut in violations: Gaussian tails reward tighter control very steeply.

### Solution 03-02.12

(a) 1 dB less signal divides $A/\sigma$ by $10^{1/20} = $ **1.122**: $7.0345/1.122 = $ **6.269**, and $Q(6.269) = $ **1.811×10⁻¹⁰**.

(b) 1 dB more: $7.0345\times1.122 = $ **7.893**, and $Q(7.893) = $ **1.477×10⁻¹⁵**.

(c) The BER rises **181**-fold for the lost decibel and falls **677**-fold for the gained one. The asymmetry is the $e^{-x^2/2}$ tail: each step further out buys more.

*Sensitivity check.* Starting from the rounded 7.034 instead gives $Q(6.2691) = $ **1.816×10⁻¹⁰**, 0.3% higher. Near $10^{-12}$, $d\ln Q/dx \approx -x$, so an error of $\delta$ in $A/\sigma$ shifts the BER by about $7\delta$ in relative terms: keep four decimals when working this deep in the tail.

### Solution 03-02.13

(a) With the threshold at $+0.5\sigma$, a sent 1 ($+A$) is misread when the noise is below $-(A - 0.5\sigma)$, probability $Q(5.5)$; a sent 0 when the noise exceeds $A + 0.5\sigma$, probability $Q(6.5)$. With equal priors, $\text{BER} = \tfrac12\big(Q(5.5) + Q(6.5)\big) = \tfrac12(1.899\times10^{-8} + 4.016\times10^{-11}) = $ **9.515×10⁻⁹**.

(b) The ideal threshold gives $Q(6) = $ **9.866×10⁻¹⁰**, so the offset costs a factor of **9.644**. Moving the threshold toward $+A$ helps the far level ($-A$) and hurts the near one ($+A$), but not equally in absolute terms. The far level's error probability can fall by at most $Q(6)$, from $9.866\times10^{-10}$ to $Q(6.5) = $ **4.016×10⁻¹¹**, while the near level's rises from $Q(6)$ to $Q(5.5) = $ **1.899×10⁻⁸**, an increase of **1.800×10⁻⁸**. The tail is so steep that the larger term dominates the average. Comparator offsets must be small compared with σ, or calibrated out.

### Solution 03-02.14

(a) $1\text{ UI} = 1/(64\times10^9) = $ **15.625 ps**. $TJ = 4 + 14.069\times0.4 = $ **9.628 ps**. Eye opening $15.625 - 9.628 = $ **5.997 ps**, or **0.3838 UI**.

(b) $\sqrt{0.3^2 + 0.25^2} = $ **0.3905 ps** rms, consistent with 0.4 ps after rounding. Attack the 0.3 ps source first: halving it gives $\sqrt{0.15^2 + 0.25^2} = $ **0.2915** ps, while halving the other gives only $\sqrt{0.3^2 + 0.125^2} = $ **0.325** ps. In quadrature, the largest term dominates.

(c) At 64 GT/s, each 0.1 ps rms of random jitter costs $14.069\times0.1 = $ **1.407** ps of eye at $10^{-12}$, or **9.0%** of the 15.625 ps unit interval. Reference clocks and PLLs must therefore be specified at the 100 fs level and below.

### Solution 03-02.15

(a) Centered: $2Q(6) = 1.973\times10^{-9}$: **1.973 ppb** (parts per billion).

(b) Shifted 1.5σ: the near limit is 4.5σ away and the far one 7.5σ: $Q(4.5) + Q(7.5) = $ **3.398×10⁻⁶**, the famous 3.4 ppm. The far tail adds only $Q(7.5) = $ **3.191×10⁻¹⁴**.

(c) Limits 3σ from target with a 1.5σ shift: $Q(1.5) + Q(4.5) = $ **0.06681** $+ 3.4\times10^{-6} = $ **66,811 ppm**, about 6.7%.

(d) It assumes the process stays Gaussian 4.5σ into its tail and that its mean wanders by no more than 1.5σ over the long run, without the drift being detected and corrected. Neither is guaranteed, which is why the convention is debated (Ramberg 2000, [R-065](../../../reference/research-log.md#r-065--six-sigma-34-ppm-and-the-15σ-shift)); measured defect rates are the real test.

### Solution 03-02.16

(a) **Poisson**: many atoms, each very unlikely to emit toward the array in a given day, independently. (b) **Exponential**: the waiting time between events of a constant-rate Poisson process. (c) **Binomial** with $n = 100$, if dies fail independently with the same probability; clustering breaks this, and real yield models add a clustering parameter. (d) **Geometric**, if each attempt succeeds independently with the same probability. (e) **Gaussian**: the sum of a vast number of independent electron motions (03-04). (f) **Uniform** on $[0, 2\pi)$, because the observation time is unrelated to the oscillator's phase.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 03-02.1a | F(0) | 0.5 | — |
| 03-02.1b | F(1) | 0.8 | — |
| 03-02.1c | F(2) | 0.95 | — |
| 03-02.1d | P(1 ≤ X ≤ 2) | 0.45 | — |
| 03-02.1e | P(X > 1) | 0.2 | — |
| 03-02.2a | c | 0.375 | — |
| 03-02.2b | F(1.5) | 0.4219 | — |
| 03-02.2c | P(X > 1) | 0.875 | — |
| 03-02.3a | P(none defective) | 0.3585 | — |
| 03-02.3b | P(at most one) | 0.7358 | — |
| 03-02.3c | P(three or more) | 0.07548 | — |
| 03-02.3d | P(exactly one) | 0.3774 | — |
| 03-02.3e | P(exactly two) | 0.1887 | — |
| 03-02.4a | Poisson yield | 0.8187 | — |
| 03-02.4b | P(exactly one defect) | 0.1637 | — |
| 03-02.4c | yield with repair | 0.9825 | — |
| 03-02.4d | loss without repair | 18.13 | % |
| 03-02.4e | loss with repair | 1.752 | % |
| 03-02.5a | binomial P(0) | 0.1299 | — |
| 03-02.5b | Poisson P(0) | 0.1353 | — |
| 03-02.5c | binomial P(2) | 0.2762 | — |
| 03-02.5d | Poisson P(2) | 0.2707 | — |
| 03-02.5e | Poisson excess at k = 0 | 4.2 | % |
| 03-02.5f | Poisson shortfall at k = 2 | 2.0 | % |
| 03-02.6a | first success on third attempt | 3.92×10^-4 | — |
| 03-02.6b | more than two attempts | 4×10^-4 | — |
| 03-02.7a | chip soft-error rate | 30720 | FIT |
| 03-02.7b | upsets per chip-year | 0.2693 | — |
| 03-02.7c | P(no upset in a year) | 0.7639 | — |
| 03-02.7d | cluster upsets per day | 7.373 | — |
| 03-02.8a | failure rate | 1000 | FIT |
| 03-02.8b | P(fail within a year) | 0.8728 | % |
| 03-02.8c | P(survive 10 years) | 0.9161 | — |
| 03-02.8d | MTTF | 114 | years |
| 03-02.9a | P(board survives 5 years) | 0.9571 | — |
| 03-02.10a | P(error magnitude > 0.4 mV) | 0.2 | — |
| 03-02.10b | F(0.3 mV) | 0.8 | — |
| 03-02.11a | out-of-spec fraction | 8.581×10^-4 | — |
| 03-02.11b | σ for 1 ppm | 10.22 | mV |
| 03-02.11c | out-of-spec fraction | 858.1 | ppm |
| 03-02.11d | k for 1 ppm two-sided | 4.892 | — |
| 03-02.11e | cut in σ | 32 | % |
| 03-02.11f | reduction in violations | 858 | — |
| 03-02.12a | BER after losing 1 dB | 1.811×10^-10 | — |
| 03-02.12b | A/σ after gaining 1 dB | 7.893 | — |
| 03-02.12c | BER after gaining 1 dB | 1.477×10^-15 | — |
| 03-02.12d | penalty factor | 181 | — |
| 03-02.12e | improvement factor | 677 | — |
| 03-02.12f | 1 dB amplitude ratio | 1.122 | — |
| 03-02.12g | A/σ after losing 1 dB | 6.269 | — |
| 03-02.12h | BER from rounded 7.034 | 1.816×10^-10 | — |
| 03-02.13a | BER with offset threshold | 9.515×10^-9 | — |
| 03-02.13b | BER with ideal threshold | 9.866×10^-10 | — |
| 03-02.13c | offset penalty factor | 9.644 | — |
| 03-02.13d | Q(6.5) | 4.016×10^-11 | — |
| 03-02.13e | Q(5.5) | 1.899×10^-8 | — |
| 03-02.13f | rise in near-level errors | 1.800×10^-8 | — |
| 03-02.14a | unit interval | 15.625 | ps |
| 03-02.14b | total jitter at 1e-12 | 9.628 | ps |
| 03-02.14c | eye opening | 5.997 | ps |
| 03-02.14d | eye opening | 0.3838 | UI |
| 03-02.14e | combined random jitter | 0.3905 | ps |
| 03-02.14f | RJ after halving 0.3 ps source | 0.2915 | ps |
| 03-02.14g | RJ after halving 0.25 ps source | 0.325 | ps |
| 03-02.14h | eye cost of 0.1 ps RJ | 1.407 | ps |
| 03-02.14i | eye cost as share of UI | 9.0 | % |
| 03-02.15a | centered ±6σ out-of-spec | 1.973 | ppb |
| 03-02.15b | shifted ±6σ out-of-spec | 3.398×10^-6 | — |
| 03-02.15d | Q(7.5) | 3.191×10^-14 | — |
| 03-02.15e | Q(1.5) | 0.06681 | — |
| 03-02.15c | shifted ±3σ out-of-spec | 66811 | ppm |
