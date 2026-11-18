# Problems 03-02 · Random Variables and Distributions

Chapter: [03-02](../chapters/03-02-random-variables-and-distributions.md) · Worked solutions: [03-02 solutions](../solutions/03-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** events are independent unless the problem says otherwise; a year is 8766 hours. Use a Q-function table, `scipy.stats.norm.sf` or $Q(x) = \tfrac12\operatorname{erfc}(x/\sqrt2)$. Answers to 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 03-02.1 [A]

The number $X$ of retransmissions needed by a packet has PMF $p_X(0) = 0.5$, $p_X(1) = 0.3$, $p_X(2) = 0.15$, $p_X(3) = 0.05$. (a) Tabulate the CDF and sketch it. (b) Find $P(1 \le X \le 2)$ and $P(X > 1)$ from the CDF.

### Problem 03-02.2 [A]

A random variable has density $f_X(x) = cx^2$ for $0 \le x \le 2$ and 0 elsewhere. (a) Find $c$. (b) Find the CDF and $F_X(1.5)$. (c) Find $P(X > 1)$.

### Problem 03-02.3 [A]

A reticle holds 20 dies, each defective with probability 0.05. Find the probability that (a) none is defective, (b) at most one is, (c) three or more are.

### Problem 03-02.4 [B]

**Poisson yield with repair.** Killer defects land at $D_0 = 0.1$ per cm² on a 2 cm² die. (a) Find the yield (no defect). (b) Find the probability of exactly one defect. (c) Spare rows can repair any single defect (but not two). What is the yield with repair?

### Problem 03-02.5 [B]

Compare the binomial with $n = 50$, $p = 0.04$ and the Poisson with λ = 2 at $k = 0$ and $k = 2$. Why does the approximation work less well here than in Example 03-02.3?

### Problem 03-02.6 [A]

A link retries a packet until it gets through; each attempt fails with probability 0.02. Find the probability that the first success is on the third attempt, and that more than two attempts are needed.

### Problem 03-02.7 [B]

**Soft errors in an AI accelerator.** An accelerator holds 256 MB (2048 Mb) of on-chip SRAM at 15 FIT/Mb (neutron-induced). (a) Find the chip's soft-error rate in FIT and its expected upsets per year. (b) What is the probability a chip goes a year with no upset? (c) How many upsets per day does a cluster of 10,000 chips see?

### Problem 03-02.8 [A]

A drive is specified with an MTTF of $10^6$ hours under a constant failure rate. Find (a) its rate in FIT, (b) the probability it fails within one year, and (c) the probability it survives 10 years.

### Problem 03-02.9 [B]

**A series system of exponential parts.** A board has three parts with constant failure rates of 200, 300 and 500 FIT; the board fails when any part fails. (a) Show that the board's lifetime is exponential with the sum of the rates. (b) Find the probability the board survives 5 years.

### Problem 03-02.10 [B]

An ideal quantizer with step Δ = 1 mV rounds a busy input that varies over many steps, so the error $e$ is well modeled as uniform on $[-0.5, 0.5]$ mV. (a) Write the PDF and CDF of $e$. (b) Find $P(|e| > 0.4\text{ mV})$ and $F_e(0.3\text{ mV})$.

### Problem 03-02.11 [B]

**A supply rail.** The rail voltage is Gaussian with mean 1.0 V and σ = 15 mV; the specification is 0.95–1.05 V. (a) What fraction of the time is it out of specification? (b) What σ would make the out-of-spec fraction 1 ppm (both sides together)?

### Problem 03-02.12 [B]

A link runs exactly at BER $10^{-12}$, so $A/\sigma = Q^{-1}(10^{-12}) = 7.0345$; carry this value at full precision. (a) Find the BER if the signal drops by 1 dB. (b) Find the BER if it rises by 1 dB. (c) By what factors does the BER change?

### Problem 03-02.13 [B]

**Comparator offset.** Levels ±A with $A/\sigma = 6$ are sliced by a comparator whose threshold sits 0.5σ above zero instead of at zero. Equal priors. (a) Find the BER. (b) Compare it with the ideal threshold, and explain the asymmetry between the two error types.

### Problem 03-02.14 [B]

**A 64 GT/s jitter budget.** The link has $DJ(\delta\delta) = 4$ ps and random jitter of 0.4 ps rms.

(a) Find the unit interval, the total jitter at $10^{-12}$, and the eye opening in ps and UI.
(b) The random jitter is the sum of two independent sources, 0.3 and 0.25 ps rms. Confirm the total, and say which one to attack first.
(c) Why are random-jitter specifications for clocks at these rates quoted in femtoseconds?

### Problem 03-02.15 [C]

**Six Sigma arithmetic.** A specification sits ±6σ from the target of a Gaussian process.

(a) With the process centered, what fraction is out of specification?
(b) With the mean shifted by 1.5σ, as the Six Sigma convention assumes, what fraction is out?
(c) A "three sigma" process (limits at ±3σ) with the same 1.5σ shift: what fraction is out, in ppm?
(d) Comment on what the 1.5σ convention assumes about a process.

### Problem 03-02.16 [A]

Name the distribution that best models each quantity, and the assumption behind it: (a) the number of alpha-particle upsets in a memory per day; (b) the time between them; (c) the number of failing dies among 100 on a wafer; (d) the number of attempts until a link trains; (e) the thermal-noise voltage across a resistor at an instant; (f) the phase of a free-running oscillator observed at a random time.

### Problem 03-02.17 [B]

**Memorylessness, both ways.** Let $K$ be the number of trials until the first success, with success probability $q$ per trial.
(a) Show that $P(K > m + n \mid K > m) = P(K > n)$.
(b) Conversely, suppose $K$ takes values $1, 2, \dots$ and is memoryless. Let $s = P(K > 1)$. Show that $P(K > n) = s^n$, so $K$ must be geometric. (This is why the geometric is the only memoryless distribution on the positive integers, as the exponential is on the positive reals.)
(c) A link retrains until it locks, each attempt succeeding with probability 0.7. After three failed attempts, what is the probability that more than two further attempts are needed?

### Problem 03-02.18 [B]

**Deriving the MAP threshold.** A receiver sees $Y = \pm A + N$ with $A = 100$ mV, Gaussian noise σ = 20 mV, and priors $P_1 = 0.1$ (for $+A$) and $P_0 = 0.9$.
(a) Starting from "decide 1 when $P_1f(y \mid +A) > P_0f(y \mid -A)$", derive the threshold $y_{\text{th}} = (\sigma^2/2A)\ln(P_0/P_1)$ and evaluate it.
(b) Find the error probability with this threshold and with the midway threshold 0, and their ratio.
(c) Which way did the threshold move, and why does that lower the error probability?

### Problem 03-02.19 [B]

**Bounds and erfc.** (a) Evaluate the lower bound $x\phi(x)/(1 + x^2)$ and the upper bound $\phi(x)/x$ at $x = 5$, and check that the exact $Q(5)$ lies between them. (b) Evaluate $\tfrac12e^{-x^2/2}$ at $x = 5$; is it a useful estimate there? (c) A data sheet quotes an error probability of $\tfrac12\operatorname{erfc}(3)$. Convert it to Q-function form and evaluate it.

### Problem 03-02.20 [C]

**An optical receiver with unequal noise.** In an optical link, the photocurrent for a 0 is 1 µA and for a 1 is 21 µA. Shot noise grows with the light, so the noise is σ₀ = 1 µA on a 0 and σ₁ = 3 µA on a 1 (Gaussian). Bits are equally likely.
(a) Find the BER with the threshold midway, at 11 µA.
(b) Find the threshold that puts it the same number of standard deviations from both levels, and the resulting BER. Show that this BER equals $Q\big((I_1 - I_0)/(\sigma_0 + \sigma_1)\big)$, the optical "Q-factor" formula.
(c) Find the exact BER-minimizing threshold numerically, and its BER.
(d) As the receiver designer, which threshold would you implement, and why do optical receivers often adjust their threshold adaptively?

---

## Objective coverage

| Learning objective (chapter 03-02) | Problems |
|---|---|
| 1. PMF, PDF and CDF; interval probabilities | 1, 2, 10 |
| 2. Bernoulli, binomial, geometric, Poisson; Poisson limit | 3, 4, 5, 6, 16, 17 |
| 3. Uniform and exponential; memorylessness; FIT | 7, 8, 9, 10, 16 |
| 4. Gaussian and the Q-function | 11, 12, 13, 15, 19 |
| 5. BER in Gaussian noise; dual-Dirac jitter | 12, 13, 14, 18, 20 |
| 6. When models fail | 5, 15, 16 |
