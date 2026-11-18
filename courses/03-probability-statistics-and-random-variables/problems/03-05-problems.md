# Problems 03-05 · Estimation and Hypothesis Testing for Engineers

Chapter: [03-05](../chapters/03-05-estimation-and-hypothesis-testing.md) · Worked solutions: [03-05 solutions](../solutions/03-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** measurements are independent and, where intervals use t or chi-square, Gaussian. Use `scipy.stats` (norm, t, chi2, poisson) or tables. $k = 8.617333\times10^{-5}$ eV/K; kelvin = °C + 273.15. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 03-05.1 [A]

Five measurements of a reference voltage error are 3, 5, 4, 6 and 7 mV. Find the sample mean, the sample variance with $n - 1$, the sample standard deviation and the standard error. What would dividing by $n$ give for the variance, and why is it biased?

### Problem 03-05.2 [A]

Sixteen measurements of a bias current average 10.3 nA. The instrument's noise is known to be σ = 2 nA per reading. Find the 95% confidence interval for the true current, and state carefully what "95%" means.

### Problem 03-05.3 [B]

Using the five measurements of Problem 03-05.1 with σ unknown, find the 95% t-interval for the mean. How much wider is it than a z-interval computed with $s$ in place of σ?

### Problem 03-05.4 [B]

**Planning sample sizes.** (a) Random jitter has σ ≈ 3 ps per measurement. How many measurements give a 95% interval of ±0.5 ps for the mean? (b) How many dies must be tested to estimate a yield near 90% to within ±1% at 95% confidence? (c) What if nothing is known about the yield in advance?

### Problem 03-05.5 [B]

(a) In a reliability screen, 46 of 500 units fail. Find the failure fraction, its standard error and a 95% confidence interval. (b) A different screen of 1000 units has no failures. Find the exact 95% upper bound and compare with the rule of three.

### Problem 03-05.6 [B]

**How well is random jitter known?** One hundred jitter samples (mean estimated from the same data) have a sample standard deviation of 0.40 ps. (a) Find a 95% confidence interval for the true rms jitter. (b) Using the dual-Dirac multiplier 14.069 at $10^{-12}$ (03-02), how much total-jitter budget does the upper confidence limit consume, compared with the point estimate?

### Problem 03-05.7 [A]

A field population accumulates $5\times10^8$ device-hours with 2 failures. Find the point estimate of the failure rate in FIT and the 90% upper bound. What would the 90% bound be with no failures?

### Problem 03-05.8 [B]

A process change is meant to lower mean leakage from 100 nA. Part-to-part σ is 20 nA (assume known). Twenty-five parts from the new process average 93 nA. (a) Compute the z statistic and the one-sided p-value. (b) Decide at α = 0.05. (c) What would a two-sided test conclude, and which is appropriate here?

### Problem 03-05.9 [B]

**Power and sample size.** For the test of Problem 03-05.8 (one-sided, α = 0.05, n = 25, σ = 20 nA): (a) find the critical sample mean; (b) find the power if the true mean is 90 nA; (c) find the sample size that gives 90% power against 90 nA.

### Problem 03-05.10 [A]

A characterization plan tests 20 independent parameters, each at α = 0.05, on a process that has not changed. (a) What is the probability of at least one false alarm? (b) What per-test level does the Bonferroni correction use, and what is the resulting overall false-alarm probability?

### Problem 03-05.11 [B]

A 100 MHz oscillator's frequency error is specified at ±50 ppm. The process mean error is +10 ppm and σ = 12 ppm. (a) Find Cp, Cpu, Cpl and Cpk. (b) Find the expected out-of-specification rate. (c) Compare two fixes: centering the mean (find the new rate) or reducing σ with the mean unchanged (find the σ that gives Cpk = 4/3).

### Problem 03-05.12 [B]

A capability study reports $\hat C_{pk} = 1.5$. Using the approximate standard error of §3.5 and a one-sided 95% bound: (a) what lower bound does a 30-part study support? (b) How many parts are needed for the lower bound to reach 1.33?

### Problem 03-05.13 [B]

**Part Average Testing.** A reference population of standby currents has median 2.23 µA, first quartile 2.10 µA and third quartile 2.37 µA. A few defective parts drag the ordinary statistics to mean 2.30 µA and standard deviation 0.35 µA. (a) Find the robust sigma and the static PAT limits. (b) Find the mean ± 6σ limits. (c) A part reads 3.6 µA, inside its 5 µA datasheet limit. Which screen catches it, and why are robust statistics preferred?

### Problem 03-05.14 [B]

A capacitor population wears out with Weibull parameters α = 20 years and γ = 3. Find (a) the reliability at 10 years, (b) the hazard rate at 10 years, (c) the $B_{10}$ life, (d) the MTTF and the median life. Which regime of the bathtub curve is this?

### Problem 03-05.15 [C]

**Estimating an activation energy.** Median lives on a high-temperature stress are 1200 h at 175 °C and 4000 h at 150 °C. (a) Assuming Arrhenius acceleration, estimate $E_a$. (b) Extrapolate the median life to a 105 °C use condition, in hours and years. (c) Why is this extrapolation risky, and how would you reduce the risk?

### Problem 03-05.16 [C]

**Planning an HTOL test.** A product must demonstrate ≤ 20 FIT at 60% confidence at 55 °C, from a 1000 h test at 125 °C with zero failures. (a) Assuming $E_a = 0.7$ eV, find the equivalent device-hours and the number of units required. (b) If the true activation energy is 0.5 eV, what does the same test actually demonstrate? (c) What does this say about FIT claims?

---

## Objective coverage

| Learning objective (chapter 03-05) | Problems |
|---|---|
| 1. Estimators, bias, sample variance, standard error | 1, 3, 4 |
| 2. Confidence intervals: mean, proportion, variance, failure rate | 2, 3, 4, 5, 6, 7 |
| 3. Hypothesis tests, p-values, power, multiple testing | 8, 9, 10 |
| 4. Process capability, its uncertainty, outlier screening | 11, 12, 13 |
| 5. Weibull lifetimes and Arrhenius acceleration | 14, 15, 16 |
