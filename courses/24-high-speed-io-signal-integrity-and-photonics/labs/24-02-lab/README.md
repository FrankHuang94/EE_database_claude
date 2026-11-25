# Lab 24-02 · Cursors, Statistical Eyes, Jitter Fits and CDR Tracking

**Objective.** Confirm a two-pole channel's cursors in ngspice, compare a statistical eye with the peak-distortion bound, see why a dual-Dirac fit to sinusoidal jitter gives a DJ(δδ) smaller than the peak-to-peak value, and check the first-order CDR's tracking error against $\lvert1 - H(f)\rvert$.

**Chapter:** [24-02 · Eye Diagrams, Jitter and BER](../../chapters/24-02-eye-diagrams-jitter-ber.md)

## Background

§3.1 defined the cursors of a pulse response and the peak-distortion eye $h_0/(M - 1) - \sum\lvert h_k\rvert$. §3.2 replaced the single worst pattern with the full ISI distribution, the statistical eye. §3.5 fitted jitter tails with the dual-Dirac model, and §3.7 showed that a first-order CDR leaves a tracking error $\lvert1 - H(f)\rvert = (f/f_c)/\sqrt{1 + (f/f_c)^2}$ of the input jitter.

## Files

- `eye.py`: Q and its inverse; the two-pole channel's pulse response and cursors; peak-distortion eyes; the ISI distribution and statistical BER; dual-Dirac total jitter, bathtubs and Q-scale fits; the tail of sinusoidal plus random jitter; first-order CDR tolerance and a time-domain loop simulation; test length, phase-noise jitter and COM.
- `pulse.cir`: a 1 V, 31.25 ps pulse through two buffered RC sections with τ = 12.5 ps (Example 24-02.2).
- `24-02-eye-lab.ipynb`: the notebook for all four parts.

## Procedure

**Part 1 · Cursors** (ngspice and notebook). *Predict* $h_{-1}$, $h_0$, $h_1$ and $h_2$ from Example 24-02.2, then run `ngspice -b pulse.cir` and compare with `eye.cursors(0.4)`.

**Part 2 · Statistical against peak-distortion eye** (notebook). For NRZ at 32 GBd with a 400 mV swing and 8 mV rms noise, *predict* whether the 10⁻¹² eye height of the statistical eye is much larger or only slightly larger than the worst-case eye less $2 \times 7.03\sigma$. Compute both, and the statistical BER at the eye centre against the worst-case bound of Example 24-02.3.

**Part 3 · Fitting sinusoidal jitter** (notebook). Combine 3 ps peak-to-peak sinusoidal PJ with 0.4 ps rms RJ. *Predict* whether a dual-Dirac fit gives DJ(δδ) above or below 3 ps. Compute the exact tail and fit Q-scale lines through its 10⁻⁹ and 10⁻¹² points, and through its 10⁻⁶ and 10⁻⁹ points.

**Part 4 · CDR tracking** (notebook). Simulate a first-order loop with $f_c$ = 4 MHz tracking unit sinusoidal jitter at 100 kHz, 4 MHz and 40 MHz. *Predict* each tracking-error ratio from §3.7, then compare.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-02.a | main cursor | 0.7340 | |
| Lab 24-02.b | first post-cursor | 0.2109 | |
| Lab 24-02.c | statistical eye height at 1e-12 | 80.6 | mV |
| Lab 24-02.d | worst-case eye less noise at 1e-12 | 74.7 | mV |
| Lab 24-02.e | statistical BER at the eye centre | 4.0e-33 | |
| Lab 24-02.f | fitted DJ, 1e-9 and 1e-12 points | 2.44 | ps |
| Lab 24-02.g | fitted sigma, 1e-9 and 1e-12 points | 0.419 | ps |
| Lab 24-02.h | fitted DJ, 1e-6 and 1e-9 points | 2.35 | ps |
| Lab 24-02.i | tracking error at 100 kHz | 0.0250 | |
| Lab 24-02.j | tracking error at 4 MHz | 0.707 | |
| Lab 24-02.k | tracking error at 40 MHz | 0.995 | |
| Lab 24-02.l | statistical eye over worst case | 8 | % |
| Lab 24-02.m | worst-case bound over statistical BER | 16 | |
| Lab 24-02.n | share of the ISI in the first post-cursor | 79 | % |

- Part 1: ngspice gives $h_{-1}$ = 0.0216, $h_0$ = 0.7340, $h_1$ = 0.2109 and $h_2$ = 0.0297, matching the analytic pulse to better than 0.01%.
- Part 2: the statistical eye at 10⁻¹² is 80.6 mV tall against 74.7 mV for the worst case less noise, only 8% more. This channel has one large post-cursor, and a preceding opposite bit, which puts it against the current one, occurs in half of all symbols, so the bound is nearly reached. The statistical BER at the centre, 4.0 × 10⁻³³, is 16 times below the bound of 6.3 × 10⁻³².
- Part 3: the fit gives DJ(δδ) = 2.44 ps and σ = 0.419 ps from the 10⁻⁹ and 10⁻¹² points, and 2.35 ps from the 10⁻⁶ and 10⁻⁹ points. A sinusoid spends most of its time near its extremes but its tail is still rounded by the Gaussian, so the fit trades some DJ for a slightly larger σ. The fitted DJ(δδ) depends on where the fit is made, which is why instruments state their fit region.
- Part 4: the simulated ratios are 0.0250, 0.707 and 0.995, matching $\lvert1 - H\rvert$ to four digits.

## Discussion

1. Why does the peak-distortion bound come so close to the statistical eye in Part 2, when Problem 24-02.12 found a 37% difference?

   <details><summary>Answer</summary>

   Here a single cursor, $h_1$ = 0.211, carries 79% of the ISI, and the patterns that put it against the bit are common. In Problem 24-02.12(c) the ISI is spread over 20 small cursors, and the pattern that aligns them all occurs once in 2²⁰ symbols, so the realistic tail is much shorter than the bound.

   </details>

2. Would a dual-Dirac fit to pure duty-cycle distortion (two equally likely edge positions) plus RJ give the true DJ?

   <details><summary>Answer</summary>

   Yes, essentially: that distribution is two Diracs, so the model is exact except for the weighting of each Dirac, which shifts the fitted intercept slightly. The dual-Dirac model is exact for DCD and approximate for everything else.

   </details>

3. Why is the tracking error at $f_c$ only 0.707, not 0.5?

   <details><summary>Answer</summary>

   At the corner $H = 1/(1 + j)$, so the clock lags the data by 45° with magnitude 0.707. The error $1 - H = j/(1 + j)$ also has magnitude 0.707: the two phasors are at right angles, not in line, so their magnitudes do not add to 1.

   </details>

## Optional hardware

A bit-error-rate tester with a jitter-injection option, or a fast real-time oscilloscope with jitter-decomposition software, will show a bathtub, an RJ/DJ split and a jitter-tolerance curve on any 10 Gb/s-class transceiver evaluation board. Compare the instrument's DJ(δδ) at two BER fit regions with Part 3.
