# Problems 03-03 · Expectation, Variance and Functions of Random Variables

Chapter: [03-03](../chapters/03-03-expectation-and-functions-of-rvs.md) · Worked solutions: [03-03 solutions](../solutions/03-03-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** a year is 8766 hours; $k = 8.617333\times10^{-5}$ eV/K; temperatures in kelvin are °C + 273.15. Use `scipy.stats` or tables for Q and Poisson values. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 03-03.1 [A]

The number of retransmissions $X$ has PMF $p_X(0) = 0.5$, $p_X(1) = 0.3$, $p_X(2) = 0.15$, $p_X(3) = 0.05$ (Problem 03-02.1). Find $\mathbb{E}[X]$, $\mathbb{E}[X^2]$, $\operatorname{Var}(X)$ and $\sigma_X$.

### Problem 03-03.2 [A]

$X$ has density $f_X(x) = 3x^2/8$ on $[0, 2]$ (Problem 03-02.2). (a) Find $\mathbb{E}[X]$, $\mathbb{E}[X^2]$, $\operatorname{Var}(X)$ and $\sigma_X$. (b) For $Y = 3X - 2$, find $\mathbb{E}[Y]$, $\operatorname{Var}(Y)$ and $\mathbb{E}[Y^2]$ without computing the distribution of $Y$.

### Problem 03-03.3 [A]

Mean, median and mode. (a) For an exponential lifetime with mean 1000 h, find the median and the mode. (b) For the log-normal leakage of Example 03-03.6 ($\sigma_\ell = 0.6907$, median 1), find the mode, using $f_Y$ from §3.6. (c) Order the three for each distribution, and say which one a "typical" specification should quote.

### Problem 03-03.4 [B]

**Expected collisions.** $k$ devices draw IDs independently and uniformly from $N$ values. (a) Using indicators, show that the expected number of colliding pairs is $\binom k2/N$. (b) Evaluate it for 302 devices with 16-bit IDs and for 10,000 devices with 32-bit IDs. (c) Use Markov's inequality to bound the probability of any collision, and compare with the exact values 0.5007 and 0.01157 from 03-01.

### Problem 03-03.5 [B]

A link resends a packet until it succeeds; each attempt fails with probability 0.02. (a) Find the mean, variance and standard deviation of the number of attempts. (b) What is the largest per-attempt failure probability for which the mean number of attempts stays at or below 1.5?

### Problem 03-03.6 [B]

**Chebyshev versus Poisson.** A fleet's yearly soft-error count is Poisson with mean 100. (a) Find its standard deviation. (b) Bound $P(|N - 100| \ge 20)$ with Chebyshev's inequality. (c) Compute the exact probability, and compare it with a Gaussian approximation $2Q(2)$.

### Problem 03-03.7 [A]

A part fails at a constant 1000 FIT. Find (a) the mean and standard deviation of its lifetime in years, (b) its median lifetime in years, and (c) the probability that it outlives its MTTF.

### Problem 03-03.8 [B]

**Redundancy and MTTF.** Parts fail independently at $r = 10^{-5}$ per hour. Using $\text{MTTF} = \int_0^\infty R(t)\,dt$, find the MTTF of (a) one part, (b) two parts in parallel, and (c) triple modular redundancy (the system works while at least two of three parts work, so $R = 3e^{-2rt} - 2e^{-3rt}$). (d) Compare the single part and TMR over a 10,000 h mission. Reconcile (c) and (d).

### Problem 03-03.9 [B]

**A pulsed current.** A switch carries 10 A for 25% of each period and 0 A otherwise. Sampling at a random instant makes the current a scaled Bernoulli variable. Find (a) the average current, (b) the RMS current, and (c) the AC (ripple) RMS current that an input capacitor must handle.

### Problem 03-03.10 [B]

A 50 Ω receiver input sees a 10 mV-amplitude sinusoid plus independent zero-mean Gaussian noise of 1 mV rms. Find (a) the total RMS voltage, (b) the total power in dBm, and (c) the signal-to-noise ratio in dB.

### Problem 03-03.11 [B]

**Meters and crest factor.** An average-responding meter reads $1.1107\,\mathbb{E}[|V|]$. (a) Find its relative error on uniform noise (and hence on any triangle wave) and on Gaussian noise. (b) A true-RMS meter clips inputs beyond 3 times the RMS value (a crest-factor rating of 3). For Gaussian noise, find the fraction of time it clips, the mean square it loses, $\mathbb{E}[X^2] - \mathbb{E}[\text{clip}(X)^2]$, as a fraction of σ², and the resulting bias of the reading. Why is the loss not the clipping-noise power $D_{\text{clip}}$ of §3.9? Repeat the bias for a crest-factor rating of 4.

### Problem 03-03.12 [B]

**Inverse transform and change of variables.** $U$ is uniform on $[0, 1]$. (a) Show that $T = -\ln(U)/r$ is exponential with rate $r$. (b) Find the density of $Y = U^2$, and compute $\mathbb{E}[Y]$ both from that density and directly as $\mathbb{E}[U^2]$. (c) How would you generate a Rayleigh envelope with mean power $\bar P$ from $U$?

### Problem 03-03.13 [B]

**The Rayleigh envelope.** The instantaneous power $P$ of a complex Gaussian signal is exponential with mean $\bar P$, and the envelope is $R = \sqrt P$. (a) Derive $f_R$. (b) Find $\mathbb{E}[R]$ in units of $\sqrt{\bar P}$, and the median. (c) Find $P(R > 2\,\mathbb{E}[R])$. (d) An instrument averages the envelope and reports $(\mathbb{E}[R])^2$ as the power. By how many dB does it underread?

### Problem 03-03.14 [B]

**Jensen and temperature cycling.** A failure mechanism has rate proportional to $e^{-E_a/(kT)}$ with $E_a = 0.7$ eV. A part spends half its time at 45 °C and half at 85 °C. (a) Find the rates at 45 °C and 85 °C relative to the rate at the average temperature, 65 °C. (b) How much higher is the time-averaged rate than the rate at 65 °C? (c) What fraction of failures happen during the hot half?

### Problem 03-03.15 [C]

**ADC loading with clipping.** A 10-bit ADC digitizes a zero-mean Gaussian signal with full scale $\pm k\sigma$.

(a) Derive the clipping-noise power $D_{\text{clip}} = 2[(1 + k^2)Q(k) - k\phi(k)]\sigma^2$.
(b) Find the total SNR for $k$ = 3, 4 and 5, and say which noise dominates in each case.
(c) Find the optimum $k$ and SNR numerically, and compare with the granular-only SNR at that $k$.

### Problem 03-03.16 [C]

**OFDM back-off.** The power of an OFDM signal is exponential with mean $\bar P$.

(a) Show that $\mathbb{E}[(P - c)^+] = \bar P\,e^{-c/\bar P}$.
(b) For back-offs of 6, 8 and 10 dB (saturation at $x\bar P$ with $10\log_{10}x$ equal to the back-off), find the clipping probability and the lost (clipped-off) power fraction in dB.
(c) Find the ideal class-B average efficiency (Example 03-03.7) at each back-off, ignoring the clipped samples.
(d) Find the back-off that keeps the lost power below −30 dB. Error-vector and spectrum limits, however, constrain the power of the error signal, $\mathbb{E}[(R - \sqrt{x})^2;\ R > \sqrt{x}]$ with $\bar P = 1$ (§3.8). Compute it numerically at 8 dB, and find the back-off at which it reaches −30 dB and the efficiency there. Which criterion would you design to, and what tools could recover some efficiency?

### Problem 03-03.17 [B]

**A detector with a DC offset.** The input to a square-law detector is $X \sim \mathcal{N}(0.5, 1)$ (volts), and the output is $Y = X^2$. (a) Derive $f_Y$ using both branches of the inverse. (b) Evaluate $f_Y(1)$. (c) Find $\mathbb{E}[Y]$ without integrating. (d) Find $P(Y > 4)$.

---

## Objective coverage

| Learning objective (chapter 03-03) | Problems |
|---|---|
| 1. Expectation, functions of a random variable, linearity and indicators | 1, 2, 4, 8 |
| 2. Variance, moments, means and variances of standard distributions | 1, 2, 3, 5, 6, 7 |
| 3. DC, AC and total power; RMS | 9, 10, 11 |
| 4. Distributions of functions of a random variable | 3, 12, 13, 17 |
| 5. Markov, Chebyshev and Jensen inequalities | 4, 6, 14 |
| 6. Crest factor, PAPR, headroom and clipping | 11, 15, 16 |
