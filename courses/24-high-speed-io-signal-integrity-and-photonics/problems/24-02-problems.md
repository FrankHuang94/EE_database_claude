# Problems 24-02 · Eye Diagrams, Jitter and BER

Chapter: [24-02](../chapters/24-02-eye-diagrams-jitter-ber.md) · Worked solutions: [24-02 solutions](../solutions/24-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- $Q(x)$ is the Gaussian tail probability and $Q^{-1}$ its inverse.
- The dual-Dirac multiplier is $2Q^{-1}(\text{BER})$, as in §3.5 (14.07 at 10⁻¹²).
- Eyes are fractions of the full swing unless stated otherwise.
- For NRZ, BER = $Q(V_{eye}/2\sigma_n)$. For Gray-coded PAM4, SER = $1.5\,Q(V_{eye}/2\sigma_n)$ and BER = SER/2.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-02-lab/eye.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-02.1 [A]

**Multipliers.** Find $Q^{-1}$ and the dual-Dirac multiplier $2Q^{-1}$ at BERs of (a) 10⁻⁴, (b) 10⁻¹⁰ and (c) 10⁻¹⁴.

### Problem 24-02.2 [A]

**Classifying jitter.** Classify each source as random jitter (RJ), data-dependent jitter (DDJ), periodic jitter (PJ) or bounded uncorrelated jitter (BUJ), and say whether it adds in quadrature or linearly in a budget:

- (a) thermal noise in the transmitter's clock buffer;
- (b) a 1 MHz ripple on the transmitter's supply;
- (c) the long tail of a lossy channel's pulse response;
- (d) a clock whose rising-to-falling time is not exactly half a period;
- (e) crosstalk from a neighbouring lane running unrelated data.

### Problem 24-02.3 [B]

**A first-order channel.** *(lab)* A channel is a single pole with τ = 0.5 UI. A one-UI pulse rises as $1 - e^{-t/\tau}$ and then decays.

- (a) Show that the pulse peaks at $t$ = 1 UI and that its cursors are $h_0 = 1 - e^{-2}$ and $h_k = h_0e^{-2k}$ for $k \ge 1$, with no pre-cursors.
- (b) Evaluate $h_0$, $h_1$ and $h_2$.
- (c) Sum the ISI exactly.
- (d) Find the NRZ and PAM4 peak-distortion eyes.

### Problem 24-02.4 [B]

**What one DFE tap buys.** A sampled pulse response has $h_{-1}$ = 0.05, $h_0$ = 0.60, $h_1$ = 0.25 and $h_2$ = 0.05 (assumed).

- (a) Find the NRZ and PAM4 peak-distortion eyes.
- (b) A one-tap decision-feedback equalizer (24-03) cancels $h_1$ exactly. Find both eyes again.

### Problem 24-02.5 [B]

**Eye height to BER.** An NRZ receiver sees a 60 mV worst-case eye.

- (a) Find the BER with 4 mV rms of noise.
- (b) What noise keeps the BER at 10⁻¹²?
- (c) What noise keeps it at 10⁻¹⁵?

### Problem 24-02.6 [B]

**The PAM4 noise penalty.** A PAM4 receiver has three 40 mV eyes stacked in a 120 mV swing, with 3 mV rms of noise.

- (a) Find the SER and BER.
- (b) An NRZ signal with the same 120 mV swing and the same ISI-free channel has one 120 mV eye. Find its BER.
- (c) By how many decibels must the PAM4 signal be larger to give the same eye-to-noise ratio as the NRZ one?

### Problem 24-02.7 [B]

**Total jitter at 53 GBd.** A 106.25 Gb/s PAM4 lane (53.125 GBd) has RJ = 0.25 ps rms and DJ(δδ) = 2.0 ps. Find the UI, then TJ, the horizontal eye opening in ps and the opening in UI at (a) 10⁻¹² and (b) 10⁻¹⁵.

### Problem 24-02.8 [B]

**Bathtub extrapolation.** *(lab)* At 53.125 GBd a tester finds the left wall of the bathtub 2.10 ps from the crossing at BER 10⁻⁵ and 2.55 ps at 10⁻⁸.

- (a) Find σ and DJ(δδ) assuming dual-Dirac tails.
- (b) Find the wall's position at 10⁻¹².
- (c) Find the eye opening at 10⁻¹², in ps and in UI, if the right wall is symmetric.

### Problem 24-02.9 [B]

**Allocating random jitter.** A 53.125 GBd link must keep TJ(10⁻¹²) at or below 0.40 UI. Its deterministic jitter (assumed) is 0.8 ps of duty-cycle distortion, 2.0 ps of residual ISI and 0.7 ps of crosstalk jitter. The transmitter PLL contributes 0.15 ps rms and the receiver 0.12 ps rms.

- (a) Find the allowed TJ in ps and the total DJ.
- (b) Find the largest total RJ.
- (c) How much rms jitter may the reference clock contribute?

### Problem 24-02.10 [B]

**How long is a BER test?** A 106.25 Gb/s lane must be shown to have BER ≤ 10⁻¹².

- (a) How many error-free bits, and how many seconds, give 95% confidence?
- (b) How many give 99% confidence?
- (c) If one error is allowed in the test, how many bits give 95% confidence? (With Poisson errors of mean λ, the probability of at most one error is $e^{-\lambda}(1 + \lambda)$.)

### Problem 24-02.11 [C]

**Jitter tolerance at 53 GBd.** A receiver's CDR is first-order with its corner at the baud rate divided by 26,562.5. Its eye absorbs 0.25 UI peak-to-peak of tracking error (assumed). The lane runs at 53.125 GBd.

- (a) Find $f_c$.
- (b) Find the tolerable sinusoidal jitter at 100 kHz.
- (c) Find the frequency below which the receiver tolerates more than 1 UI.
- (d) Find the fraction of the input jitter that appears as tracking error at 200 kHz and at $f_c$.

### Problem 24-02.12 [C]

**Statistical against worst-case eyes.** *(lab)* NRZ, $h_0$ = 0.7 and Gaussian noise σ = 0.05, all in units of half the swing.

- (a) The only ISI is $h_1$ = 0.2 and $h_2$ = 0.1. For random data, find the exact BER at the eye centre by averaging over the four ISI patterns, and the worst-case bound $Q((h_0 - \sum\lvert h_k\rvert)/\sigma)$.
- (b) For each method in (a), find the largest σ that keeps the BER at 10⁻¹².
- (c) Now the ISI is 20 equal cursors of 0.015 each: the same 0.3 total, so the same worst case. Find the exact BER at σ = 0.05 and the largest σ for 10⁻¹². What does this say about long channels?

### Problem 24-02.13 [B]

**A reference clock from its phase-noise plot.** A 100 MHz reference clock has a flat phase noise of −140 dBc/Hz from 12 kHz to 20 MHz (assumed; integrate both sidebands, as in 20-10).

- (a) Find its rms jitter.
- (b) Compare it with PCIe 5.0's 0.15 ps limit, ignoring the weighting filters.
- (c) What flat phase-noise level would meet 0.15 ps?

### Problem 24-02.14 [C]

**What FEC buys a PAM4 link.** For Gray-coded PAM4 with BER = 0.75 $Q(V_{eye}/2\sigma_n)$:

- (a) Find the required $V_{eye}/2\sigma_n$ for a raw BER of 10⁻¹².
- (b) Find it for an FBER of 10⁻⁶.
- (c) Find the difference in dB.
- (d) How many error-free bits, and how long at 128 Gb/s, demonstrate 10⁻⁶ with 95% confidence?

### Problem 24-02.15 [A]

**Reading a COM result.** A channel's COM analysis reports a signal amplitude of 30 mV and noise-plus-interference of 20 mV at the target DER.

- (a) Find COM.
- (b) Does the channel pass the 3 dB threshold?
- (c) How large could the noise-plus-interference grow before it fails?

### Problem 24-02.16 [C]

**Deriving total jitter.** In the dual-Dirac model each crossing is a Gaussian of rms $RJ$ centred at $\pm DJ(\delta\delta)/2$. (a) Show that, if each edge's tail beyond the sampling point is set equal to the BER, the eye closes by $DJ/2 + Q^{-1}(\text{BER})\,RJ$ from each side, so $TJ = 2Q^{-1}(\text{BER})\,RJ + DJ(\delta\delta)$. (b) Explain why the factor ½ (half the transitions in each Dirac) does not appear, and what convention absorbs it. (c) Evaluate TJ for $RJ$ = 0.2 ps and $DJ(\delta\delta)$ = 1.5 ps at 10⁻¹² and 10⁻¹⁵, and the eye width at 10⁻¹² for 53.125 GBd.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Pulse response, cursors and peak-distortion and statistical eyes | 3, 4, 12 |
| 2. Vertical eye to BER, NRZ and PAM4 | 5, 6, 14 |
| 3. Jitter decomposition and dual-Dirac total jitter | 1, 2, 7, 16 |
| 4. Bathtubs and jitter budgets | 8, 9 |
| 5. CDR jitter tolerance and reference clocks | 11, 13 |
| 6. BER targets, FEC and test time | 10, 14, 15 |
