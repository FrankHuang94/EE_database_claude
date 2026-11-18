# Course 03 · Final Exam — Solutions

Exam: [README.md](README.md). All numbers are recomputed by [verify_03_exam.py](../verify/verify_03_exam.py). Each solution names the chapter to revisit if you lost points.

**1.** *(03-01)* (a) Independent blocks: $P(\text{pass}) = 0.98\times0.95\times0.99 = $ **0.9217**.

(b) Exactly one fails: $0.02(0.95)(0.99) + 0.98(0.05)(0.99) + 0.98(0.95)(0.01) = 0.01881 + 0.04851 + 0.00931 = $ **0.07663**.

(c) Exactly, $1 - 0.92169 = $ **0.07831**. The union bound is $0.02 + 0.05 + 0.01 = $ **0.08**, **2.158%** high, because it double-counts dies with two or more failing blocks. With small probabilities the bound is a good quick estimate.

**2.** *(03-01)* (a) $P(\text{reject}) = 0.02(0.97) + 0.98(0.03) = 0.0194 + 0.0294 = $ **0.0488**.

(b) Bayes: $P(\text{defective} \mid \text{pass}) = \dfrac{0.02\times0.03}{0.02\times0.03 + 0.98\times0.97} = \dfrac{0.0006}{0.9512} = 6.308\times10^{-4}$, or **630.8 DPPM**.

(c) $P(\text{good} \mid \text{reject}) = 0.0294/0.0488 = $ **0.6025**: three in five rejects are good dies (overkill).

(d) Among rejects the defective fraction is $0.0194/0.0488 = 0.3975$. After an independent retest, a reject that passes is defective with probability

$$
\frac{0.3975\times0.03}{0.3975\times0.03 + 0.6025\times0.97} = 0.0200 ,
$$

that is, **20,000 DPPM**, exactly the incoming defect rate and **31.71** times worse than the first-pass shipments. Because the miss rate equals the false-reject rate (0.03), the retest's evidence exactly cancels the first test's: the recovered population is no better than untested dies. (Real retests also differ because defects are often repeatable rather than independent between tests.)

**3.** *(03-02)* (a) λ = $10^4\times2\times10^{-5} = $ **0.2**. Poisson: $e^{-0.2} = $ **0.8187**. Exactly: $(1 - 2\times10^{-5})^{10^4} = $ **0.8187** (they agree to four digits).

(b) Failure needs two or more errors: $1 - e^{-0.2}(1 + 0.2) = $ **0.01752**.

(c) Transmissions are geometric with success probability $1 - 0.01752$: mean $1/0.98248 = $ **1.018**.

**4.** *(03-02, 03-04)* (a) $8\times50 + 400 + 1200 = $ **2000 FIT**, a rate of $2\times10^{-6}$ per hour. Per year, $2\times10^{-6}\times8766 = 0.01753$, so $P(\text{fail within a year}) = 1 - e^{-0.01753} = $ **0.01738**. MTTF $= 1/(2\times10^{-6})$ h $= $ **57.04 years**.

(b) $e^{-7\times0.01753} = $ **0.8845**.

(c) **0.01738**, the same as for a new board: constant-rate (exponential) lifetimes are memoryless. This holds only in the flat part of the bathtub curve.

(d) The number of failed boards is binomial(50,000, 0.01738): mean **869.0**, standard deviation $\sqrt{50{,}000\times0.01738\times0.98262} = $ **29.22**. Then $P(N > 1000) \approx Q\big((1000.5 - 869.0)/29.22\big) = Q(4.5016) \approx$ **3.37×10⁻⁶**. (The exact binomial value is **5.37×10⁻⁶**: 4.5σ out, the normal approximation already underestimates the tail, as 03-04 warned.)

**5.** *(03-02)* (a) $A/\sigma = 90/12 = $ **7.5**, so BER $= Q(7.5) = $ **3.191×10⁻¹⁴**.

(b) $\sigma = 90/Q^{-1}(10^{-12}) = 90/7.034 = $ **12.79 mV**.

(c) The near level's errors need noise beyond $(90 - 4)/12 = 7.1667$σ and the far level's beyond 7.8333σ: BER $= \tfrac12\big(3.842\times10^{-13} + 2.376\times10^{-15}\big) = $ **1.933×10⁻¹³**, **6.058** times worse.

(d) Deep in a Gaussian tail, each fraction of a σ is worth a large factor in probability: losing 0.33σ on one side costs far more than gaining it on the other side returns (03-02 Problem 13).

**6.** *(03-02, 03-04)* (a) $1/25\text{ GHz} = $ **40 ps**; random jitters add in quadrature: $\sqrt{1.2^2 + 0.9^2} = $ **1.5 ps**.

(b) $TJ = 12 + 14.069\times1.5 = $ **33.10 ps**; the eye is $40 - 33.10 = $ **6.897 ps**, or **0.1724 UI**. At $10^{-15}$: $12 + 15.883\times1.5 = $ **35.82 ps**.

(c) $TJ \le 40 - 8 = 32$ ps requires $\sigma_{RJ} \le (32 - 12)/14.069 = $ **1.422 ps**. With the 0.9 ps source fixed, the other must satisfy $\sqrt{1.422^2 - 0.9^2}$: at most **1.100 ps**, an 8% cut.

**7.** *(03-03)* (a) Mean **0.5 V**. The three parts are uncorrelated, so their powers add: $0.5^2 + 0.2^2/2 + 0.03^2 = 0.25 + 0.02 + 0.0009 = $ **0.2709 V²**. RMS **0.5205 V**; AC RMS $\sqrt{0.0209} = $ **0.1446 V**.

(b) $0.2709/50 = $ **5.418 mW**, or **7.338 dBm**.

(c) $0.02/0.0009 = 22.22$, or **13.47 dB**.

(d) ±3σ: **±90 mV**.

**8.** *(03-03)* (a) $V_T = kT/q = $ **25.85 mV**; $s = 18/(1.3\times25.85) = $ **0.5356**; mean over median $e^{s^2/2} = $ **1.154**.

(b) $P(I > 3I_0) = Q(\ln3/s) = Q(2.0512) = $ **0.02012**; the 99th percentile is $e^{2.326s} = $ **3.476** times the median.

(c) The sum of $2\times10^7$ independent leakages is close to $2\times10^7$ times the mean: $2\times10^7\times0.2\text{ nA}\times1.154 = $ **4.617 mA**. A median-device model predicts 4 mA, low by **13.36%** of the true value.

(d) Jensen's inequality: for convex $g$, $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$. Evaluating any convex dependence at the typical input underestimates the average.

**9.** *(03-04)* (a) $\operatorname{Cov} = 0.6\times3\times4 = 7.2$ mV². $\operatorname{Var}(X - Y) = 9 + 16 - 14.4 = 10.6$, so σ = **3.256 mV**; $\operatorname{Var}\big((X + Y)/2\big) = (9 + 16 + 14.4)/4 = 9.85$, so σ = **3.138 mV**, barely better than the better sensor alone.

(b) $\operatorname{Var} = w^2\sigma_X^2 + (1 - w)^2\sigma_Y^2 + 2w(1 - w)c$; setting its derivative to zero gives $w = (\sigma_Y^2 - c)/(\sigma_X^2 + \sigma_Y^2 - 2c) = 8.8/10.6 = $ **0.8302**, and σ = **2.949 mV**.

(c) With ρ = 0, $w = 16/25 = $ **0.64** and σ = $\sqrt{9\times16/25} = $ **2.4 mV**. Shared error (here 60% correlation) cannot be averaged away; combining helps only with the independent part (03-04 §3.3).

**10.** *(03-04)* (a) λ = $2000\times5\times10^{-4} = 1$. Failure needs 5 or more errors: exactly (binomial) **3.648×10⁻³**; Poisson $1 - e^{-1}(1 + 1 + \tfrac12 + \tfrac16 + \tfrac1{24}) = $ **3.660×10⁻³**.

(b) σ = $\sqrt{2000\times5\times10^{-4}\times(1 - 5\times10^{-4})} = $ **0.9997**; $z = (4.5 - 1)/0.9997 = $ **3.501**; $Q(3.5009) = $ **2.319×10⁻⁴**, about **15.73** times too small.

(c) Pairs are Poisson with mean 0.5; 4 bit errors (2 pairs) are corrected but 6 (3 pairs) are not, so failure needs 3 or more pairs: $1 - e^{-0.5}(1 + 0.5 + 0.125) = $ **0.01439**, **3.931** times worse than random errors at the same average BER.

(d) Mean $10^6\times3.648\times10^{-3} = $ **3648**, standard deviation $\sqrt{3648\times(1 - 0.003648)} = $ **60.29**.

**11.** *(03-05)* (a) $\bar x = $ **1200.35 mV**, $s = $ **1.068 mV**, standard error $1.068/\sqrt8 = 0.3775$ mV, and the 95% interval is $1200.35 \pm 2.365\times0.3775$: **[1199.46, 1201.24] mV**.

(b) $\hat C_p = 12/(6\times1.068) = $ **1.873**; $\hat C_{pk} = (1206 - 1200.35)/(3\times1.068) = $ **1.764** (the upper limit is nearer).

(c) $\text{SE} = \sqrt{1/72 + 1.764^2/14} = $ **0.4859**, and the bound is $1.764 - 1.645\times0.4859 = $ **0.9646**. No: eight parts cannot demonstrate 1.33.

(d) Solving $1.764 - 1.645\sqrt{1/(9n) + 1.764^2/(2(n - 1))} = 1.33$ gives $n \approx 24.9$: about **25** parts.

**12.** *(03-05)* (a) $AF = \exp\big[(0.6/8.617333\times10^{-5})(1/343.15 - 1/398.15)\big] = $ **16.49**; device-hours $300\times1000\times16.49 = $ **4.948×10⁶ h**.

(b) Point estimate $1/(4.948\times10^6)$ per hour $= $ **202.1 FIT**. Upper bounds: $2.022/D = $ **408.7 FIT** (60%) and $3.890/D = $ **786.2 FIT** (90%).

(c) $B_1 = 2500(-\ln0.99)^{1/3} = $ **539.5 h** at stress; at use $\times16.49$: **8898 h**, or **1.015 years**.

(d) A FIT rate assumes a constant failure rate; a wear-out mechanism with a $B_1$ life near one year means about 1% of parts fail in the first year of use and the rate then rises, so (b)'s FIT number is the wrong summary. The mechanism must be fixed or the product derated before any reliability claim makes sense.

**13.** *(03-06)* (a) $\sqrt{4kT_0R} = \sqrt{4\times1.380649\times10^{-23}\times290\times200} = $ **1.790 nV/√Hz**. The current noise in the source becomes $1\text{ pA}\times200\ \Omega = 0.2$ nV/√Hz. Total: $\sqrt{1.790^2 + 1.5^2 + 0.2^2} = $ **2.344 nV/√Hz**.

(b) $F = 2.344^2/1.790^2 = $ **1.715**, so NF = **2.342 dB**.

(c) $2.344\text{ nV}\times\sqrt{2\times10^7} = $ **10.48 µV** rms. Floor: $-173.98 + 73.01 + 2.34 = $ **−98.62 dBm**.

(d) $\sqrt{kT/C} = \sqrt{4.142\times10^{-21}/2\times10^{-12}} = $ **45.51 µV** rms.

**14.** *(03-02, 03-03, 03-05, 03-06)* Rubric: about 1 point per claim (4), plus 1 for at least two well-formed questions. Strong answers:

- (i) PAPR is meaningless without the CCDF probability (and capture length, and whether crest-factor reduction is on): "PAPR at what probability, measured how?" (03-03).
- (ii) A FIT bound needs device-hours, failures, confidence level and activation energy, and assumes no wear-out: "How many equivalent device-hours, at what confidence and $E_a$, and what are the wear-out mechanisms' B-lives?" A standard qualification demonstrates tens to hundreds of FIT, not < 1 (03-05).
- (iii) Cpk needs the sample size, the number of lots and evidence that the process is stable: "From how many parts and lots, what is the lower confidence bound, and what is Ppk?" (03-05).
- (iv) A noise density needs its frequency and the 1/f corner: "At what frequency, and what is the 0.1–10 Hz noise (or the full density curve)?" (03-06).

Weak answers accept a number without its conditions, or dismiss the claims without saying what would make them testable.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| X03.1a | P(die passes) | 0.9217 | — |
| X03.1b | P(exactly one fails) | 0.07663 | — |
| X03.1c | P(at least one fails) | 0.07831 | — |
| X03.1d | union bound | 0.08 | — |
| X03.1e | overstatement of the bound | 2.158 | % |
| X03.2a | fraction rejected | 0.0488 | — |
| X03.2b | shipped defect level | 630.8 | DPPM |
| X03.2c | good fraction of rejects | 0.6025 | — |
| X03.2d | defective fraction of rejects | 0.3975 | — |
| X03.2e | recovered-population defect level | 20000 | DPPM |
| X03.2f | ratio to first-pass defect level | 31.71 | — |
| X03.3a | mean errors per frame | 0.2 | — |
| X03.3b | P(no error), Poisson | 0.8187 | — |
| X03.3c | P(no error), exact | 0.8187 | — |
| X03.3d | frame failure probability | 0.01752 | — |
| X03.3e | mean transmissions | 1.018 | — |
| X03.4a | board failure rate | 2000 | FIT |
| X03.4b | P(fail within a year) | 0.01738 | — |
| X03.4c | MTTF | 57.04 | years |
| X03.4d | P(survive 7 years) | 0.8845 | — |
| X03.4e | conditional failure probability | 0.01738 | — |
| X03.4f | mean failed boards | 869.0 | — |
| X03.4g | standard deviation | 29.22 | — |
| X03.4h | normal approximation of P(N > 1000) | 3.37×10^-6 | — |
| X03.4i | exact binomial P(N > 1000) | 5.37×10^-6 | — |
| X03.4j | expected failures per board-year | 0.01753 | — |
| X03.5a | A/σ | 7.5 | — |
| X03.5b | BER | 3.191×10^-14 | — |
| X03.5c | σ for BER 1e-12 | 12.79 | mV |
| X03.5d | BER with offset | 1.933×10^-13 | — |
| X03.5e | BER increase factor | 6.058 | — |
| X03.6a | unit interval | 40 | ps |
| X03.6b | total random jitter | 1.5 | ps |
| X03.6c | total jitter at 1e-12 | 33.10 | ps |
| X03.6d | eye opening | 6.897 | ps |
| X03.6e | eye opening | 0.1724 | UI |
| X03.6f | total jitter at 1e-15 | 35.82 | ps |
| X03.6g | allowable random jitter | 1.422 | ps |
| X03.6h | allowable 1.2 ps source | 1.100 | ps |
| X03.7a | mean | 0.5 | V |
| X03.7b | mean square | 0.2709 | V² |
| X03.7c | RMS | 0.5205 | V |
| X03.7d | AC RMS | 0.1446 | V |
| X03.7e | power into 50 Ω | 5.418 | mW |
| X03.7f | power into 50 Ω | 7.338 | dBm |
| X03.7g | SNR | 13.47 | dB |
| X03.7h | 3σ noise band | 90 | mV |
| X03.8a | thermal voltage | 25.85 | mV |
| X03.8b | s | 0.5356 | — |
| X03.8c | mean over median | 1.154 | — |
| X03.8d | fraction above three times the median | 0.02012 | — |
| X03.8e | 99th percentile over median | 3.476 | — |
| X03.8f | block leakage | 4.617 | mA |
| X03.8g | underestimate of a median model | 13.36 | % |
| X03.9a | σ of X − Y | 3.256 | mV |
| X03.9b | σ of the plain average | 3.138 | mV |
| X03.9c | optimal weight | 0.8302 | — |
| X03.9d | optimal σ | 2.949 | mV |
| X03.9e | optimal weight, uncorrelated | 0.64 | — |
| X03.9f | optimal σ, uncorrelated | 2.4 | mV |
| X03.10a | block failure, exact | 3.648×10^-3 | — |
| X03.10b | block failure, Poisson | 3.660×10^-3 | — |
| X03.10c | σ of the error count | 0.9997 | — |
| X03.10d | z with continuity correction | 3.501 | — |
| X03.10e | Gaussian approximation | 2.319×10^-4 | — |
| X03.10f | Gaussian error factor | 15.73 | — |
| X03.10g | block failure with pairs | 0.01439 | — |
| X03.10h | pairing penalty | 3.931 | — |
| X03.10i | mean failed blocks in 1e6 | 3648 | — |
| X03.10j | standard deviation | 60.29 | — |
| X03.11a | sample mean | 1200.35 | mV |
| X03.11b | sample standard deviation | 1.068 | mV |
| X03.11c | lower 95% limit | 1199.46 | mV |
| X03.11d | upper 95% limit | 1201.24 | mV |
| X03.11e | Cp | 1.873 | — |
| X03.11f | Cpk | 1.764 | — |
| X03.11g | standard error of Cpk | 0.4859 | — |
| X03.11h | 95% lower bound on Cpk | 0.9646 | — |
| X03.11i | parts needed | 25 | — |
| X03.11j | standard error of the mean | 0.3775 | mV |
| X03.12a | acceleration factor | 16.49 | — |
| X03.12b | equivalent device-hours | 4.948×10^6 | h |
| X03.12c | point estimate | 202.1 | FIT |
| X03.12d | 60% upper bound | 408.7 | FIT |
| X03.12e | 90% upper bound | 786.2 | FIT |
| X03.12f | B1 life at stress | 539.5 | h |
| X03.12g | B1 life at use | 8898 | h |
| X03.12h | B1 life at use | 1.015 | years |
| X03.13a | source noise density | 1.790 | nV/√Hz |
| X03.13b | total input noise density | 2.344 | nV/√Hz |
| X03.13c | noise factor | 1.715 | — |
| X03.13d | noise figure | 2.342 | dB |
| X03.13e | rms noise in 20 MHz | 10.48 | µV |
| X03.13f | noise floor | −98.62 | dBm |
| X03.13g | kT/C noise at 2 pF | 45.51 | µV |
