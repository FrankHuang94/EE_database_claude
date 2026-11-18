# Problems 03-04 · Joint Distributions, Correlation and the CLT

Chapter: [03-04](../chapters/03-04-joint-distributions-and-clt.md) · Worked solutions: [03-04 solutions](../solutions/03-04-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** variables are independent unless the problem says otherwise. Use `scipy.stats` for binomial, Poisson and Q values. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 03-04.1 [A]

A die's final status $X$ (0 good, 1 bad) and the number of defects $Y$ an optical scan flags on it have the joint PMF below.

| | $Y = 0$ | $Y = 1$ | $Y = 2$ |
|---|---|---|---|
| $X = 0$ | 0.30 | 0.20 | 0.10 |
| $X = 1$ | 0.10 | 0.15 | 0.15 |

(a) Find both marginals, and decide whether $X$ and $Y$ are independent. (b) Find $P(Y = 2 \mid X = 1)$. (c) Find $\mathbb{E}[X]$, $\mathbb{E}[Y]$, $\operatorname{Cov}(X, Y)$ and the correlation coefficient.

### Problem 03-04.2 [A]

$(X, Y)$ has joint density $f(x, y) = c(x + y)$ on the unit square $0 \le x, y \le 1$. (a) Find $c$ and the marginal $f_X$. (b) Find $P(X + Y < 1)$. (c) Find $\mathbb{E}[X]$, $\mathbb{E}[XY]$, $\operatorname{Cov}(X, Y)$ and ρ. Are $X$ and $Y$ independent?

### Problem 03-04.3 [A]

$X$ is equally likely to be −1, 0 or 1, and $Y = X^2$. Show that $X$ and $Y$ are uncorrelated but not independent. Give an engineering situation with the same structure.

### Problem 03-04.4 [B]

**A tolerance stack.** Ten 1 kΩ resistors in series each deviate from nominal by an independent amount uniform on ±10 Ω. (a) Find the worst-case deviation of the total and its standard deviation. (b) Use the CLT to estimate the probability that the total deviates by more than 50 Ω. (c) The exact probability is 0.004938. Why does the CLT overestimate it?

### Problem 03-04.5 [B]

**A noise budget.** Three independent noise sources referred to an amplifier input are 3, 4 and 12 µV rms. (a) Find the total. (b) Find the total if the 12 µV source is halved instead of the other two being eliminated. (c) Find the total if the 3 and 4 µV sources are fully correlated (same waveform, same sign).

### Problem 03-04.6 [B]

**Matching a differential pair.** Each wire of a pair picks up 20 mV rms of common interference, with correlation ρ between the wires. (a) Find the differential noise for ρ = 0.95. (b) What correlation is needed to keep the differential noise at or below 2 mV rms? What does that say about layout symmetry?

### Problem 03-04.7 [B]

An accelerator's SRAM sees soft errors at 0.27 per year and its flip-flops at 0.05 per year, both Poisson and independent. Find the probability of (a) no upset in a year and (b) exactly two upsets in a year.

### Problem 03-04.8 [B]

**Cold spare versus hot spare.** Parts fail at a constant $r = 10^{-5}$ per hour. (a) A cold spare (unpowered until the first part fails, perfect switch-over) gives a system lifetime $T = T_1 + T_2$. Find its density by convolution, its MTTF and its reliability $R(t)$. (b) Compare $R(10{,}000\text{ h})$ with a hot spare (both powered, parallel).

### Problem 03-04.9 [B]

A noise measurement has σ = 5 mV per sample. How many independent samples are needed for the sample mean to be within ±0.5 mV of the truth with 95% probability (by the CLT)?

### Problem 03-04.10 [B]

A wafer has 600 dies, each defective with probability 0.1, independently. (a) Find the mean and standard deviation of the number of defective dies. (b) Estimate $P(N > 75)$ with the CLT and a continuity correction. (c) The exact binomial value is 0.02000. Why does the CLT underestimate it?

### Problem 03-04.11 [B]

**Averaging with correlated noise.** $n$ samples have variance σ² each and correlation ρ between every pair. (a) Show that the variance of their mean is $\sigma^2[\rho + (1 - \rho)/n]$. (b) With σ = 1 and ρ = 0.01, find the standard error for $n = 100$ and its limit as $n \to \infty$. (c) What does this mean for averaging in the presence of slow drift?

### Problem 03-04.12 [B]

Two on-die voltage sensors read the supply at nearby points. Their readings are jointly Gaussian, each with mean 0.75 V and σ = 10 mV, with correlation 0.9. Sensor A reads 0.73 V. (a) Find the conditional mean and standard deviation of sensor B. (b) Find the probability that B is below 0.72 V, and compare with the unconditional probability.

### Problem 03-04.13 [A]

The in-phase and quadrature noise of a receiver are independent $\mathcal{N}(0, (1\text{ mV})^2)$. Find (a) the mean envelope, (b) the probability the envelope exceeds 3 mV, and (c) the mean power in mV². What is the distribution of the phase?

### Problem 03-04.14 [C]

**Optimal cancellation.** $X_1$ and $X_2$ have standard deviations 2 and 1 and correlation 0.6 (for example, a noisy measurement and a reference sensor that sees part of the same noise). (a) Find $\operatorname{Var}(X_1 - 2X_2)$. (b) Find the coefficient $a$ that minimizes $\operatorname{Var}(X_1 - aX_2)$ and the minimum variance. (c) Interpret the result in terms of §3.8, and as a finance hedge ratio.

### Problem 03-04.15 [C]

**FEC design.** For RS(544,514) ($n = 544$, $t = 15$, $m = 10$) with independent bit errors:

(a) Find the uncorrectable codeword ratio at a pre-FEC BER of $10^{-4}$, exactly and with the Poisson approximation.
(b) Find, numerically, the pre-FEC BER at which the uncorrectable codeword ratio is $10^{-10}$.
(c) The weaker RS(528,514) "KR4" code of 25 Gb/s-per-lane Ethernet ($n = 528$, $t = 7$, also 10-bit symbols) sees the same pre-FEC BER of $2.4\times10^{-4}$. Find its uncorrectable codeword ratio, and compare with Example 03-04.7.

### Problem 03-04.16 [C]

**Bursts break the binomial.** At a pre-FEC BER of $2.4\times10^{-4}$, RS(544,514) sees on average λ = 1.304 wrong symbols per codeword. Model two cases with Poisson counts:

- random errors: wrong symbols are Poisson with mean λ, and the codeword fails with 16 or more;
- paired errors: errors arrive as bursts that each corrupt two adjacent symbols, bursts are Poisson with mean λ/2, and the codeword fails with 8 or more bursts.

(a) Find the uncorrectable codeword ratio in each case. (b) To what mean number of wrong symbols, and what pre-FEC BER (inverting $p_s = 1 - (1 - p)^{10}$), must the paired-error link be improved to match the random-error failure rate? (c) Relate the result to the IEEE practice described in §9.

### Problem 03-04.17 [B]

**Multi-bit upsets: a random sum.** Particle strikes on a memory arrive as a Poisson count $N$ with mean 4 per day. Each strike independently upsets $K$ adjacent bits, with $P(K = 1) = 0.6$, $P(K = 2) = 0.3$ and $P(K = 3) = 0.1$. Let $S$ be the total number of upset bits in a day.

(a) Find $\mathbb{E}[K]$ and $\operatorname{Var}(K)$.
(b) Condition on $N$ and use iterated expectations and total variance to find $\mathbb{E}[S]$, $\operatorname{Var}(S)$ and $\sigma_S$.
(c) Compare $\operatorname{Var}(S)$ with the variance of a Poisson count of the same mean. What does the difference mean for an error-correcting code that fixes one bit per word?

### Problem 03-04.18 [B]

**Series and parallel lifetimes.** Two independent parts have exponential lifetimes $T_1$ and $T_2$ with rates $r_1 = 2\times10^{-5}$ and $r_2 = 1\times10^{-5}$ per hour.

(a) A system that needs both parts (series) fails at $\min(T_1, T_2)$. Show that this lifetime is exponential and find its MTTF.
(b) Find the probability that part 1 fails first.
(c) A redundant system that works while either part works (parallel) fails at $\max(T_1, T_2)$. Find its MTTF from the survival function.
(d) By what percentage does the redundant pair beat the better part alone? Why does pairing unequal parts gain so little?

---

## Objective coverage

| Learning objective (chapter 03-04) | Problems |
|---|---|
| 1. Joint, marginal and conditional distributions; independence; conditioning (iterated expectations, total variance) | 1, 2, 3, 17, 18 |
| 2. Covariance, correlation, variance of sums | 1, 2, 4, 5, 6, 11, 14 |
| 3. Sums of independent variables by convolution | 7, 8 |
| 4. Law of large numbers and the CLT, and their limits | 4, 9, 10, 11 |
| 5. Jointly Gaussian variables; Rayleigh and exponential | 12, 13, 14 |
| 6. Block errors, FEC, dependence and tails | 15, 16 |
