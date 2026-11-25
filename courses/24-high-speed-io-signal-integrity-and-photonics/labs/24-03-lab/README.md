# Lab 24-03 · CTLE, FFE, DFE and CDR

**Objective.** Confirm the source-degenerated CTLE's response in ngspice; design a zero-forcing transmitter FFE and compare it with a DFE; measure DFE error propagation; watch sign-sign LMS adapt DFE taps; and see why a bang-bang CDR needs an integral path to track a frequency offset.

**Chapter:** [24-03 · SerDes Architecture and Equalization](../../chapters/24-03-serdes-architecture.md)

## Background

§3.3 designed a three-tap FFE by zero forcing under $\sum\lvert c_j\rvert = 1$. §3.4 derived the CTLE's zero $1/R_SC_S$, first pole $(1 + g_mR_S/2)/R_SC_S$ and output pole $1/R_DC_L$. §3.5 gave the probability that a DFE error is followed by another, and §3.6 the sign-sign LMS update. §3.7 linearized the bang-bang detector to a gain of $\sqrt{2/\pi}/\sigma$ and showed that a proportional-only loop can slew at most $\rho\delta$ UI per UI.

## Files

- `serdes.py`: cursor convolution and zero-forcing FFE design; peak-distortion eyes with and without DFE; the CTLE response; analytic and simulated DFE error propagation; sign-sign LMS adaptation of DFE taps and data level; bang-bang detector gain and a bang-bang CDR with proportional and integral paths; driver power; the PAM4 break-even loss.
- `ctle.cir`: the CTLE of Example 24-03.4 as a small-signal differential half-circuit.
- `24-03-serdes-lab.ipynb`: the notebook for all five parts.

## Procedure

**Part 1 · CTLE** (ngspice and notebook). *Predict* the DC gain, the peak gain and its frequency, and the gain at 16 GHz, then run `ngspice -b ctle.cir`. In the notebook, remove the output pole and see how much peaking returns.

**Part 2 · FFE against DFE** (notebook). *Predict* the three zero-forcing taps for 24-02's channel and the equalized NRZ and PAM4 eyes, then compute them and compare with a two-tap DFE.

**Part 3 · DFE error propagation** (notebook). Simulate 4 × 10⁵ NRZ symbols through $h_0$ = 1, $h_1$ = 0.5 with a one-tap DFE and noise set for a 10⁻³ error rate without propagation. *Predict* the fraction of errors that follow another error.

**Part 4 · LMS adaptation** (notebook). Start a two-tap DFE at zero on 24-02's channel with 0.02 rms noise and a step of $2^{-9}$, and adapt taps and data level by sign-sign LMS. *Predict* where they settle.

**Part 5 · Bang-bang CDR** (notebook). With a step of $2^{-14}$ UI, 0.02 UI rms jitter and a 100 ppm offset, run a proportional-only loop and one with an integral step of $2^{-20}$. *Predict* which keeps lock, and what the integrator settles to.

## Expected results

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 24-03.a | CTLE DC gain | 0.80 | |
| Lab 24-03.b | CTLE peak gain | 2.69 | |
| Lab 24-03.c | CTLE peak frequency | 13.8 | GHz |
| Lab 24-03.d | CTLE gain at 16 GHz | 2.664 | |
| Lab 24-03.e | CTLE peaking without the output pole | 13.98 | dB |
| Lab 24-03.f | NRZ eye with FFE | 0.520 | |
| Lab 24-03.g | NRZ eye with two-tap DFE | 0.709 | |
| Lab 24-03.h | noise for a 1e-3 error rate | 0.324 | |
| Lab 24-03.i | error continuation probability | 0.25 | |
| Lab 24-03.j | adapted first tap | 0.211 | |
| Lab 24-03.k | adapted second tap | 0.030 | |
| Lab 24-03.l | adapted data level | 0.734 | |
| Lab 24-03.m | proportional-only slew limit | 30.5 | ppm |
| Lab 24-03.n | integrator's settled value | 1.0e-4 | UI/UI |

- Part 1: ngspice gives 0.80 at DC, a peak of 2.69 at 13.8 GHz and 2.664 at 16 GHz, matching the closed form. Without the output pole the gain rises monotonically to 4.0, a full 13.98 dB of peaking.
- Part 2: the FFE's taps are −0.0223, 0.7602 and −0.2175, giving an NRZ eye of 0.520; the two-tap DFE gives 0.709 by keeping the main cursor.
- Part 3: σ = 0.324 for a 10⁻³ error rate. About a quarter of errors follow another error, as the formula predicts for $h_1 = h_0/2$, and the error rate rises by about a third above 10⁻³.
- Part 4: the taps settle within a few LMS steps of 0.211 and 0.030 and the data level near 0.734, then dither.
- Part 5: the proportional-only loop, able to slew only 30.5 ppm, slips cycles: its phase error grows without bound. With the integral path the error stays within about 0.01 UI and the integrator settles at 1.0 × 10⁻⁴ UI per UI, the 100 ppm offset itself.

## Discussion

1. Why does the LMS-adapted DFE tap equal $h_1$ rather than some other value?

   <details><summary>Answer</summary>

   The update's average is proportional to the correlation between the error and the previous decision. That correlation is zero only when no ISI from the previous symbol remains in the sample, which is when the tap equals $h_1$. Noise and other cursors are uncorrelated with the previous decision, so they do not bias the result, though they make it dither.

   </details>

2. The proportional-only loop has a linearized bandwidth of 10.3 MHz. Why does that not save it?

   <details><summary>Answer</summary>

   The linear model holds only while the phase error stays within a few σ of zero. A 100 ppm offset needs the phase to move $10^{-4}$ UI per UI, but a vote moves it by at most $2^{-14}$ UI and arrives only half the time, so the loop's maximum slew rate is $3.05 \times 10^{-5}$ UI per UI. The error grows until the detector saturates and the loop slips cycles.

   </details>

3. How would you make the CTLE's peaking less sensitive to $C_L$?

   <details><summary>Answer</summary>

   Push the output pole up: shunt-peaking inductors in series with $R_D$, a lower $R_D$ with a higher $g_m$ (more current), or splitting the boost across two cascaded stages, each with modest peaking and a higher output pole.

   </details>

## Optional hardware

FPGA development boards with multi-gigabit transceivers expose their TX FFE, CTLE and DFE settings and an eye scan. Sweeping the TX de-emphasis and CTLE settings over a cable or backplane shows the trade between equalization and noise directly.
