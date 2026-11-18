# Equation Sheet · 03 Probability, Statistics and Random Variables

The relations to know cold from Course 03, each with its conditions and where it is derived. The FE Reference Handbook lists many of these, but knowing their conditions is what keeps you out of the tails where they fail.

## Probability rules

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $P(A \cup B) = P(A) + P(B) - P(A \cap B)$; union bound $P(\cup A_i) \le \sum P(A_i)$ | Bound is tight when events are rare | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| $1 - (1 - p)^n \approx np$ if $np \ll 1$; compute as $-\operatorname{expm1}(n\operatorname{log1p}(-p))$ | Rare-event rule; avoid cancellation | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| $P(A \mid B) = P(A \cap B)/P(B)$; total probability $P(A) = \sum_i P(A \mid B_i)P(B_i)$ | Partition $B_i$ | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| Bayes: $P(B \mid A) = P(A \mid B)P(B)/P(A)$; posterior odds = prior odds × likelihood ratio | Base rates dominate rare conditions | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| Independent: $P(A \cap B) = P(A)P(B)$ | Not the same as mutually exclusive | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| Series reliability $\prod R_i$; parallel $1 - \prod(1 - R_i)$; TMR $3R^2 - 2R^3$ | Independent failures; common-mode failures break these | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| Defect level $DL = 1 - Y^{1 - T}$ | Williams–Brown; yield $Y$, fault coverage $T$ | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |
| Zero failures in $n$: confidence $1 - (1 - p)^n$; $n \approx -\ln(1 - C)/p$ (3/p at 95%) | Zero-error BER tests | [03-01](../../courses/03-probability-statistics-and-random-variables/chapters/03-01-probability-in-ee-language.md) |

## Distributions

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Binomial $\binom nk p^k(1 - p)^{n-k}$: mean $np$, variance $np(1 - p)$ | $n$ independent trials | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Geometric $(1 - q)^{k-1}q$: mean $1/q$, variance $(1 - q)/q^2$ | Trials to first success | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Poisson $\lambda^ke^{-\lambda}/k!$: mean = variance = λ | Binomial limit, $\lambda = np$; rare independent events | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Exponential $P(T > t) = e^{-rt}$: mean $1/r$, σ = $1/r$; memoryless | Constant failure rate; Poisson-process gaps | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| 1 FIT = 1 failure per $10^9$ device-hours; rates in series add | 1000 FIT ≈ 0.9% per year | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Uniform on $[a, b]$: mean $(a + b)/2$, variance $(b - a)^2/12$ | Quantization error: $\Delta^2/12$ | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Gaussian: $P(X > a) = Q((a - \mu)/\sigma)$; $Q(x) = \tfrac12\operatorname{erfc}(x/\sqrt2)$ | 68.27 / 95.45 / 99.73% within 1, 2, 3σ | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| $\frac{x}{1 + x^2}\phi(x) < Q(x) < \phi(x)/x$; $Q(x) \le \tfrac12e^{-x^2/2}$ | $\phi(x) = e^{-x^2/2}/\sqrt{2\pi}$ | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| $Q(3) = 1.350\times10^{-3}$, $Q(4.5) = 3.398\times10^{-6}$, $Q(6) = 9.866\times10^{-10}$; $Q^{-1}(10^{-12}) = 7.034$ | Landmarks | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Binary BER in Gaussian noise: $Q(A/\sigma)$; $10^{-12}$ needs 16.94 dB | Threshold midway, equal priors | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |
| Dual-Dirac: $TJ = DJ(\delta\delta) + 2Q_{\text{BER}}\sigma_{RJ}$; $2Q = 14.069$ at $10^{-12}$ | Transition density 1/2; eye = 1 UI − TJ | [03-02](../../courses/03-probability-statistics-and-random-variables/chapters/03-02-random-variables-and-distributions.md) |

## Expectation and functions of random variables

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $\mathbb{E}[g(X)] = \sum g(k)p(k)$ or $\int g(x)f(x)\,dx$ | No need for the distribution of $g(X)$ | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| $\mathbb{E}[aX + bY + c] = a\mathbb{E}[X] + b\mathbb{E}[Y] + c$ | Always, even for dependent variables | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| $\operatorname{Var}(X) = \mathbb{E}[X^2] - \mu^2$; $\operatorname{Var}(aX + b) = a^2\operatorname{Var}(X)$ |  | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| MTTF $= \int_0^\infty R(t)\,dt$: parallel pair $1.5/r$, TMR $5/(6r)$ |  | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| $\mathbb{E}[V^2] = (\mathbb{E}[V])^2 + \operatorname{Var}(V)$ | Total power = DC + AC; AC RMS = σ | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| $f_Y(y) = \sum_i f_X(x_i)/\lvert g'(x_i)\rvert$, $g(x_i) = y$ | Change of variables | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| Log-normal $e^X$, $X \sim \mathcal{N}(\mu, s^2)$: median $e^\mu$, mean $e^{\mu + s^2/2}$ | Subthreshold leakage | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| Markov $P(X \ge a) \le \mathbb{E}[X]/a$; Chebyshev $P(\lvert X - \mu\rvert \ge k\sigma) \le 1/k^2$ | Any distribution | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| Jensen: convex $g$ ⇒ $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$ | Leakage, Arrhenius, RMS ≥ mean | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| PAPR of complex Gaussian (OFDM) at probability $p$: $10\log_{10}\ln(1/p)$ dB | 9.643 dB at $10^{-4}$; sine 3.010 dB | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| Exponential power: $\mathbb{E}[(P - c)^+] = \bar Pe^{-c/\bar P}$ | Clipped power fraction = clipping probability | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |
| ADC, Gaussian input, loading $k = V_{FS}/\sigma$: granular SNR $6.02N + 4.77 - 20\log_{10}k$ dB; clipping $2[(1 + k^2)Q(k) - k\phi(k)]$ | Optimum $k$ ≈ 3.9 (8 bits), 5.0 (12 bits) | [03-03](../../courses/03-probability-statistics-and-random-variables/chapters/03-03-expectation-and-functions-of-rvs.md) |

## Joint distributions, sums and limit theorems

| Relation | Conditions / notes | Chapter |
|---|---|---|
| Marginal $f_X = \int f_{XY}\,dy$; conditional $f_{Y\mid X} = f_{XY}/f_X$; independent ⇔ $f_{XY} = f_Xf_Y$ |  | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| $\operatorname{Cov}(X, Y) = \mathbb{E}[XY] - \mu_X\mu_Y$; $\rho = \operatorname{Cov}/(\sigma_X\sigma_Y) \in [-1, 1]$ | Uncorrelated ≠ independent (except jointly Gaussian) | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| $\operatorname{Var}(X \pm Y) = \sigma_X^2 + \sigma_Y^2 \pm 2\operatorname{Cov}(X, Y)$ | RSS when uncorrelated; differential noise $\sigma\sqrt{2(1 - \rho)}$ | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| $f_{X+Y} = f_X * f_Y$; Poisson + Poisson = Poisson; Gaussian + Gaussian = Gaussian | Independent terms | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| $\operatorname{Var}(\bar X_n) = \sigma^2/n$; averaging $n$ gains $10\log_{10}n$ dB | Independent samples only | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| CLT: $(\sum X_i - n\mu)/(\sigma\sqrt n) \to \mathcal{N}(0, 1)$ | Center only; fails in far tails, with dependence or heavy tails | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| Jointly Gaussian: $\mathbb{E}[Y \mid x] = \mu_Y + \rho(\sigma_Y/\sigma_X)(x - \mu_X)$, $\operatorname{Var}(Y \mid x) = \sigma_Y^2(1 - \rho^2)$ | Regression line | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| I, Q independent $\mathcal{N}(0, \sigma^2)$: envelope Rayleigh, phase uniform, power exponential (mean $2\sigma^2$) | Polar Jacobian $r$ | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |
| RS($n$, $k$): $p_s = 1 - (1 - p)^m$; $\text{UCR} = P(N > t)$, $N \sim$ binomial($n$, $p_s$) | $t = (n - k)/2$; RS(544,514): $t = 15$ | [03-04](../../courses/03-probability-statistics-and-random-variables/chapters/03-04-joint-distributions-and-clt.md) |

## Estimation, testing and reliability

| Relation | Conditions / notes | Chapter |
|---|---|---|
| $S^2 = \sum(X_i - \bar X)^2/(n - 1)$ | Unbiased | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Mean: $\bar X \pm z_{\alpha/2}\sigma/\sqrt n$ or $\bar X \pm t_{\alpha/2,n-1}S/\sqrt n$ | $z_{0.025} = 1.960$; $t_{0.025,9} = 2.262$ | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Proportion $\hat p \pm z\sqrt{\hat p(1 - \hat p)/n}$; zero failures: upper bound ≈ $3/n$ at 95% | Rule of three | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Variance: $\nu S^2/\chi^2_{1-\alpha/2,\nu} \le \sigma^2 \le \nu S^2/\chi^2_{\alpha/2,\nu}$ | Gaussian data | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Failure rate from $c$ failures in $D$ device-hours: $r_U = \tfrac12\chi^2_{\text{conf},2c+2}/D$ | $c = 0$: 0.916 (60%), 2.303 (90%) | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Sample size to detect shift δ: $n = ((z_\alpha + z_\beta)\sigma/\delta)^2$ | One-sided test | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| $C_p = (\text{USL} - \text{LSL})/(6\sigma)$; $C_{pk} = \min(\text{USL} - \mu, \mu - \text{LSL})/(3\sigma)$ | 1.33 ↔ 63 ppm centered; AIAG: ≥ 1.33 ongoing, ≥ 1.67 initial | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| $\text{SE}(\hat C_{pk}) \approx \sqrt{1/(9n) + \hat C_{pk}^2/(2(n - 1))}$ | About 0.2 at $n = 30$ | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Hazard $h = f/R$; Weibull $R = e^{-(t/\alpha)^\gamma}$, $h = (\gamma/\alpha)(t/\alpha)^{\gamma - 1}$; $B_p = \alpha(-\ln(1 - p))^{1/\gamma}$ | γ < 1, = 1, > 1: infant, random, wear-out | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |
| Arrhenius $AF = \exp[(E_a/k)(1/T_{use} - 1/T_{stress})]$ | 0.7 eV, 125 → 55 °C: 77.65 | [03-05](../../courses/03-probability-statistics-and-random-variables/chapters/03-05-estimation-and-hypothesis-testing.md) |

## Random processes and noise

| Relation | Conditions / notes | Chapter |
|---|---|---|
| WSS: constant mean, $R_X(t, t + \tau) = R_X(\tau)$; $R_X(0)$ = power |  | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| Var of a time average ≈ $2\sigma^2\tau_c/T$; $N_{\text{eff}} = T/(2\tau_c)$ | Exponential autocorrelation, $T \gg \tau_c$ | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| $S_X(f) = \int R_X(\tau)e^{-j2\pi f\tau}d\tau$; power $= \int S_X\,df$; one-sided $G = 2S$ | Wiener–Khinchin | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| $\sigma^2e^{-\lvert\tau\rvert/\tau_c}$ ↔ $G(f) = 4\sigma^2\tau_c/(1 + (2\pi f\tau_c)^2)$ | Corner $1/(2\pi\tau_c)$ | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| $S_Y = \lvert H\rvert^2S_X$; one RC pole: $B_N = (\pi/2)f_{3\text{dB}} = 1/(4RC)$ |  | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| Thermal: $4kTR$ V²/Hz, $4kT/R$ A²/Hz; $\overline{v^2} = kT/C$ | 4.07 nV/√Hz for 1 kΩ at 300 K | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| $kT_0 = -174$ dBm/Hz; floor $= -174 + 10\log_{10}B + \text{NF}$ dBm | $T_0 = 290$ K | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| Shot noise $2qI$ A²/Hz | 17.9 pA/√Hz at 1 mA | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| 1/f: $e_w^2(1 + f_c/f)$; power in $[f_1, f_2]$ = $e_w^2[f_c\ln(f_2/f_1) + (f_2 - f_1)]$ | Equal power per decade | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
| Random walk: $\operatorname{Var}(W(t)) = (N_0/2)t$ | Spread grows as $\sqrt t$ | [03-06](../../courses/03-probability-statistics-and-random-variables/chapters/03-06-random-processes-preview.md) |
