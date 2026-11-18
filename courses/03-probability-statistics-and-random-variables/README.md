<!-- BEGIN GENERATED (tools/build_curriculum.py) — edit tools/data/curriculum.yml, not this block -->

# 03 · Probability, Statistics and Random Variables for EE

An accelerated course for a learner who already knows probability and statistics from finance: the same mathematics restated in EE language (bit errors, yield, noise, measurement) and extended to the Gaussian Q-function and random-process ideas that noise and communications courses need.

| | |
|---|---|
| **Term** | 1 |
| **Study hours** | ≈ 43 |
| **University equivalents** | Probability and Random Processes for EE (junior); MIT 6.041 / 6.431 |
| **Textbook alignment** | Leon-Garcia, *Probability, Statistics, and Random Processes for Electrical Engineering*; Bertsekas & Tsitsiklis, *Introduction to Probability* |
| **Free courses** | MIT OCW 6.041SC Probabilistic Systems Analysis and Applied Probability |
| **Prerequisites** | [01 · Calculus for Engineers](../01-calculus-for-engineers/README.md) |
| **FE areas** | Probability and Statistics |

## Learning objectives

1. Model engineering events (bit errors, defects, failures) with the appropriate discrete or continuous distribution.
2. Compute expectations, variances, covariances and correlation coefficients, including for sums and functions of random variables.
3. Use the Gaussian distribution and the Q-function to compute error and yield probabilities.
4. Apply estimation, confidence intervals and hypothesis tests to measurement and yield data.
5. Explain autocorrelation, stationarity and white noise as the bridge to noise analysis and communications.

## Chapter map

| Chapter | Hours | Status | Materials |
|---|---|---|---|
| [03-01 · Probability in EE Language](chapters/03-01-probability-in-ee-language.md) | 6 | ✅ verified | [problems](problems/03-01-problems.md) · [solutions](solutions/03-01-solutions.md) · [lab](labs/03-01-lab/README.md) · [verify](verify/verify_03_01.py) |
| [03-02 · Random Variables and Distributions](chapters/03-02-random-variables-and-distributions.md) | 8 | ✅ verified | [problems](problems/03-02-problems.md) · [solutions](solutions/03-02-solutions.md) · [lab](labs/03-02-lab/README.md) · [verify](verify/verify_03_02.py) |
| [03-03 · Expectation, Variance and Functions of Random Variables](chapters/03-03-expectation-and-functions-of-rvs.md) | 6 | ✅ verified | [problems](problems/03-03-problems.md) · [solutions](solutions/03-03-solutions.md) · [lab](labs/03-03-lab/README.md) · [verify](verify/verify_03_03.py) |
| [03-04 · Joint Distributions, Correlation and the CLT](chapters/03-04-joint-distributions-and-clt.md) | 8 | ✅ verified | [problems](problems/03-04-problems.md) · [solutions](solutions/03-04-solutions.md) · [lab](labs/03-04-lab/README.md) · [verify](verify/verify_03_04.py) |
| [03-05 · Estimation and Hypothesis Testing for Engineers](chapters/03-05-estimation-and-hypothesis-testing.md) | 6 | ✅ verified | [problems](problems/03-05-problems.md) · [solutions](solutions/03-05-solutions.md) · [lab](labs/03-05-lab/README.md) · [verify](verify/verify_03_05.py) |
| [03-06 · Random Processes Preview: Noise](chapters/03-06-random-processes-preview.md) | 6 | ✅ verified | [problems](problems/03-06-problems.md) · [solutions](solutions/03-06-solutions.md) · [lab](labs/03-06-lab/README.md) · [verify](verify/verify_03_06.py) |

**Course resources:** [Course final exam](exam/README.md) · [Flashcards (Anki CSV)](../../flashcards/03-probability-statistics-and-random-variables.csv) · [Equation sheet](../../reference/equation-sheets/03-probability-statistics-and-random-variables.md)

Status legend: ⬜ planned · ✏️ draft · ✅ verified (all checks pass) · 🏁 reviewed (independent audit done)

<!-- END GENERATED -->

## Course notes

**How to approach this course.** Course 03 takes about 43 hours. It assumes you already know probability and statistics from finance, and restates them in the language of chips and links: bit errors, yield, defects, noise, jitter and reliability. The six chapters run in order. 03-01 (events, Bayes, independence, reliability) and 03-02 (distributions, the Q-function, BER and jitter) are the foundation. 03-03 and 03-04 extend them to expectations, functions of random variables, several variables at once and the limit theorems, and 03-05 turns them around into estimation, tests, process capability and reliability statistics. 03-06 is a preview of random processes and the physics of noise, which Courses 11, 16, 17 and 20 develop. Work at least the [A] and [B] problems of every chapter. Every lab is a seeded simulation notebook that checks a formula by repeating the experiment thousands of times; 03-06 also has an ngspice noise netlist.

**What to master cold.** The union bound and the $e^{-np}$ rule, Bayes with base rates, and series/parallel reliability (03-01); the binomial, Poisson and exponential laws, FIT arithmetic, the Q-function and its landmarks, BER = $Q(A/\sigma)$ and dual-Dirac total jitter (03-02); linearity of expectation, the DC-plus-AC power split, change of variables, Jensen's inequality and PAPR at a stated probability (03-03); covariance and the variance of sums, the $1/\sqrt n$ law of averaging, the CLT and where it fails, and the binomial tail of a codeword (03-04); t, chi-square and Poisson confidence bounds, test power, Cp and Cpk, Weibull lifetimes and Arrhenius acceleration (03-05); autocorrelation, the PSD, $4kTR$, kT/C, $-174$ dBm/Hz and $2qI$ (03-06). The [equation sheet](../../reference/equation-sheets/03-probability-statistics-and-random-variables.md) collects them.

**Assessment.** The [course final exam](exam/README.md) has 14 questions, takes 180 minutes, and allows a calculator, the equation sheet and the table of distribution values printed with it, but not Python. Aim for at least 70%. Question 14 is a short-answer diligence question about four datasheet claims. The [flashcards](../../flashcards/03-probability-statistics-and-random-variables.csv) (128 cards) are for spaced review alongside the chapters.

**Why this course matters for diligence.** Almost every quality, reliability and performance claim you will meet is a statistic: a BER at a target, a FIT bound, a Cpk, a PAPR, a noise density. Each means something only with its conditions: the probability level, the confidence level and sample size, the activation energy, the bandwidth or frequency. The chapters' Marketing vs Reality sections and exam Question 14 practice asking for exactly those.

**Perishable content.** The mathematics is timeless. The dated facts are in the practitioner sections, logged as [R-059](../../reference/research-log.md#r-059--serial-link-bit-error-rate-targets-pcie-and-ethernet) to [R-071](../../reference/research-log.md#r-071--op-amp-noise-specifications-1f-and-zero-drift) in the research log. The ones most likely to move are the standards and their revisions (link BER targets and FEC in [R-059](../../reference/research-log.md#r-059--serial-link-bit-error-rate-targets-pcie-and-ethernet) and [R-067](../../reference/research-log.md#r-067--rs544514-kp4-fec-and-pre-fec-ber); JEDEC and AEC qualification in [R-061](../../reference/research-log.md#r-061--qualification-sample-sizes-aec-q100-and-jedec-jesd47) and [R-068](../../reference/research-log.md#r-068--process-capability-and-outlier-screening)), vendor-measured soft-error rates ([R-064](../../reference/research-log.md#r-064--soft-error-rates-and-fit)), and the datasheets quoted for op-amp noise ([R-071](../../reference/research-log.md#r-071--op-amp-noise-specifications-1f-and-zero-drift)). Check those entries once a year.
