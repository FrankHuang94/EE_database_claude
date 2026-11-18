# Course 03 · Final Exam (Probability, Statistics and Random Variables for EE)

**Time limit:** 180 minutes. **Allowed:** a scientific calculator, the [Course 03 equation sheet](../../../reference/equation-sheets/03-probability-statistics-and-random-variables.md) printed without its chapter links, and the table of distribution values at the end of this paper (every Q-function and t value you need is there). No notes, no Python.
**Instructions:** answer all 15 questions and show every step. Each [A] is worth 5 points, each [B] 8 and each [C] 12 (123 points in total; 86 or more, about 70%, is a strong pass). Within a question, the lettered parts carry equal weight unless the solutions' rubric says otherwise. Give numerical answers to 4 significant figures unless told otherwise, with units. Question 14 is a short-answer diligence question graded against the rubric in the solutions. Solutions are in a separate file, [solutions.md](solutions.md). Open it only after you finish.

Constants: $k = 1.380649\times10^{-23}$ J/K $= 8.617333\times10^{-5}$ eV/K, $q = 1.602177\times10^{-19}$ C; kelvin = °C + 273.15; a year is 8766 hours. Noise densities are one-sided.

---

**1 [A] · Yield and the union bound.** A die passes final test only if three blocks pass, and they fail independently with probabilities 0.02 (CPU), 0.05 (SerDes) and 0.01 (SRAM).
(a) Find the probability that a die passes.
(b) Find the probability that exactly one block fails.
(c) Find the probability that at least one block fails, exactly and by the union bound. By what percentage does the bound overstate it?

**2 [B] · Escapes, overkill and retest.** 2% of incoming dies are defective. The test rejects a defective die with probability 0.97 and wrongly rejects a good die with probability 0.03.
(a) What fraction of dies is rejected?
(b) What is the defect level of the shipped (passing) dies, in DPPM?
(c) What fraction of rejected dies is actually good?
(d) To recover yield, the rejected dies are retested once, independently, with the same test, and those that pass are shipped. Find the defect level of this recovered population in DPPM, and comment.

**3 [A] · Errors in a frame.** Frames of 10,000 bits cross a link with independent bit errors at BER $2\times10^{-5}$.
(a) Find the mean number of errors per frame and the probability of an error-free frame, with the Poisson approximation and exactly.
(b) A code corrects one error per frame. Find the frame failure probability.
(c) Failed frames are retransmitted until they succeed. Find the mean number of transmissions per frame.

**4 [B] · Did the firmware fix work?** A chip's standby current has mean 12.0 mA and standard deviation 0.8 mA across parts, known from long production history. After a power-management firmware fix, 25 parts average 11.6 mA. Assume the standard deviation is unchanged.
(a) Test $H_0$: μ = 12.0 mA against $H_1$: μ < 12.0 mA at α = 0.05. Find the test statistic and the p-value.
(b) If the fix really lowers the mean to 11.7 mA, what is the probability that a 25-part test detects it?
(c) How many parts would give 90% power against a true mean of 11.7 mA?
(d) A colleague proposes deciding between a one-sided and a two-sided test after seeing the data. What does that do to the true false-alarm rate?

**5 [B] · Decisions in Gaussian noise.** A receiver slices levels of ±90 mV in Gaussian noise of σ = 12 mV, with equal priors.
(a) Find the bit error rate.
(b) What noise σ would give a BER of exactly $10^{-12}$?
(c) The slicer has a +4 mV threshold offset. Find the new BER and the factor by which it has risen.
(d) Explain in one or two sentences why a small offset matters so much here.

**6 [B] · A 25 GT/s jitter budget.** A link runs at 25 GT/s with dual-Dirac deterministic jitter $DJ(\delta\delta) = 12$ ps. Its random jitter comes from two independent sources of 1.2 ps and 0.9 ps rms.
(a) Find the unit interval and the total random jitter.
(b) Find the total jitter and the eye opening (ps and UI) at $10^{-12}$, and the total jitter at $10^{-15}$.
(c) The receiver needs 8 ps of eye at $10^{-12}$. Find the largest allowable random jitter, and the largest allowable value of the 1.2 ps source if only that source can be improved.

**7 [B] · Power of a noisy signal.** A voltage is $v(t) = 0.5\text{ V} + 0.2\cos(2\pi\cdot1\text{ kHz}\cdot t)\text{ V} + n(t)$, where $n(t)$ is independent zero-mean Gaussian noise of 30 mV rms.
(a) Find the mean, the mean square, the RMS value and the AC RMS value of $v$.
(b) Find the average power $v$ delivers to 50 Ω, in mW and dBm.
(c) Find the signal-to-noise ratio of the sinusoid against the noise, in dB.
(d) Within what band around its mean does the noise stay 99.73% of the time?

**8 [C] · Log-normal leakage.** A transistor's off-current is $I = I_0\exp\big(-\Delta V_{TH}/(nV_T)\big)$ with $\Delta V_{TH} \sim \mathcal{N}(0, (18\text{ mV})^2)$, $n = 1.3$ and $V_T = kT/q$ at 300 K. The median device leaks $I_0 = 0.2$ nA.
(a) Find $V_T$, the standard deviation $\sigma_\ell$ of $\ln(I/I_0)$, and the ratio of mean to median leakage.
(b) Find the fraction of devices leaking more than three times the median, and the 99th-percentile leakage as a multiple of the median.
(c) A block has $2\times10^7$ such transistors. Estimate its total leakage, and the percentage by which a power model built on the median device underestimates it.
(d) Name the inequality behind (c), and say which way the error would go for any convex dependence.

**9 [B] · Combining correlated measurements.** Two sensors measure the same voltage with zero-mean errors $X$ and $Y$: $\sigma_X = 3$ mV, $\sigma_Y = 4$ mV, correlation ρ = 0.6.
(a) Find the standard deviations of $X - Y$ and of the plain average $(X + Y)/2$.
(b) Find the weight $w$ that minimizes the variance of $wX + (1 - w)Y$, and the resulting standard deviation.
(c) Repeat (b) for ρ = 0, and explain why correlation limits the benefit of combining sensors.

**10 [C] · A block code, the CLT and bursts.** Blocks of 2000 bits are protected by a code that corrects up to 4 bit errors. Bit errors are independent with BER $5\times10^{-4}$.
(a) Find the block failure probability exactly and with the Poisson approximation.
(b) Find the Gaussian (CLT) approximation with a continuity correction, and the factor by which it is wrong.
(c) Suppose instead that errors arrive in pairs of adjacent bits, at the same average BER, with the number of pairs per block Poisson. Find the block failure probability, and the factor by which pairing worsens it relative to the Poisson value of (a).
(d) Over $10^6$ blocks with independent errors, find the mean and standard deviation of the number of failed blocks.

**11 [B] · Estimation and capability.** Eight measurements of a bandgap reference (mV) are 1199.2, 1201.5, 1200.8, 1198.9, 1200.3, 1201.9, 1199.6 and 1200.6. The specification is 1200 ± 6 mV.
(a) Find the sample mean, the sample standard deviation and a 95% confidence interval for the mean.
(b) Estimate Cp and Cpk.
(c) Using $\text{SE}(\hat C_{pk}) \approx \sqrt{1/(9n) + \hat C_{pk}^2/(2(n - 1))}$, find a one-sided 95% lower bound on Cpk (to 3 significant figures). Does the study demonstrate Cpk ≥ 1.33?
(d) If further parts gave the same $\hat C_{pk}$, about how many parts in total would make the lower bound reach 1.33?

**12 [C] · From an HTOL test to a field claim.** A qualification runs 300 units for 1000 h at a junction temperature of 125 °C, and one unit fails. Assume Arrhenius acceleration with $E_a = 0.6$ eV and use at 70 °C.
(a) Find the acceleration factor and the equivalent device-hours at use.
(b) Find the point estimate of the field failure rate, and its 60% and 90% upper confidence bounds, in FIT.
(c) A separate test shows that a second failure mechanism wears out, with a Weibull shape of 3 and a characteristic life of 25,000 h at 125 °C. Find its $B_1$ life at stress, and at use (in years) assuming the same acceleration factor.
(d) How many of the 300 HTOL units would this wear-out mechanism be expected to fail in 1000 h? In two or three sentences, say what (c) means for the FIT number of (b).

**13 [B] · A receiver noise budget.** A 200 Ω source at 290 K drives an amplifier with input voltage noise 1.5 nV/√Hz and input current noise 1 pA/√Hz.
(a) Find the source's noise density and the total input-referred noise density.
(b) Find the noise factor $F$ (the total input-referred noise power divided by the source's own thermal noise power at 290 K) and the noise figure $10\log_{10}F$.
(c) Find the input-referred rms noise in a 20 MHz bandwidth, and the receiver's noise floor in dBm using $-174\text{ dBm/Hz} + 10\log_{10}B + \text{NF}$ (with $kT_0$ computed exactly).
(d) The amplifier's output is sampled onto a 2 pF capacitor at 300 K. Find the kT/C noise.

**14 [A] · Reading a datasheet skeptically.** A startup's product brief claims: (i) "PAPR 7 dB" for its OFDM transmitter; (ii) "FIT < 1, proven in qualification"; (iii) "Cpk = 2.0 on all critical parameters"; (iv) "0.9 nV/√Hz input noise". For each claim, name the missing piece of information that determines whether it means anything, and the question you would ask.

**15 [B] · Averaging real noise.** (a) A sensor's noise has σ = 1 mV and an exponential autocorrelation with correlation time 2 ms. Using $\operatorname{Var}(\langle x\rangle_T) \approx 2\sigma^2\tau_c/T$, find the standard deviation of a 1 s time average and the effective number of independent samples.
(b) The 1 s record is sampled every 10 µs. How many samples is that, and why does the answer to (a) not improve?
(c) An amplifier has white noise 5 nV/√Hz and a 1/f corner of 20 Hz. Find its rms noise in the 0.1–10 Hz band.
(d) Find the rms noise in 0.01–10 Hz, and explain why measuring for longer (reaching lower frequencies) adds noise instead of averaging it away.

---

## Table of distribution values

Use these values; you need no others. $Q(x) = P(Z > x)$ for a standard normal $Z$; $Q^{-1}$ is its inverse.

| Value | | Value | |
|---|---|---|---|
| $Q(2.0512)$ | 0.02012 | $Q(7.1667)$ | $3.842\times10^{-13}$ |
| $Q(3.5009)$ | $2.319\times10^{-4}$ | $Q(7.5)$ | $3.191\times10^{-14}$ |
| $Q(2.5)$ | $6.210\times10^{-3}$ | $Q(7.8333)$ | $2.376\times10^{-15}$ |
| $Q(0.23)$ | 0.4090 | $Q^{-1}(0.1) = z_{0.1}$ | 1.2816 |
| $Q^{-1}(0.05) = z_{0.05}$ | 1.645 | $Q^{-1}(10^{-12})$ | 7.034 |
| $Q^{-1}(0.01)$ | 2.326 | $2Q^{-1}(10^{-12})$, $2Q^{-1}(10^{-15})$ | 14.069, 15.883 |
| $t_{0.025,7}$ (95%, 7 degrees of freedom) | 2.365 | Poisson upper bound $\lambda_U(1)$ | 2.022 (60%), 3.890 (90%) |
