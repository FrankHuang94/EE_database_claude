# Lab 17-04 · Pulses, Eyes and Equalizers

Chapter: [17-04 · Baseband Digital Transmission](../../chapters/17-04-baseband-digital-transmission.md)

## Objective

Build baseband PAM links in simulation and check the chapter's results:

- the folded-spectrum test for zero ISI and the raised-cosine family;
- eye diagrams of NRZ through a one-pole channel, and their worst-case openings;
- the timing sensitivity of sinc and raised-cosine pulses;
- zero-forcing and decision-feedback equalization, with their error rates;
- NRZ against PAM4 through a lossy channel.

Confirm the one-pole channel's cursors with ngspice.

## Background

A link's sampled pulse response (cursors $h_k$) determines everything: the worst-case eye is $h_0 - \sum_{k\ne0}\lvert h_k\rvert$, the exact binary error rate with Gaussian noise is the average of $Q(v/\sigma)$ over all interfering patterns, and an equalizer works by reshaping the cursors (§3.3, §3.6, §3.7). Zero ISI requires the spectrum folded at the symbol rate to be flat (§3.4).

## Files

- `baseband.py`: `pam_levels`, `gray_map`, `mean_energy`, `raised_cosine`, `raised_cosine_spectrum`, `root_raised_cosine`, `manchester_psd`, `folded_spectrum`, `waveform`, `rc_channel`, `rc_cursors`, `worst_case_eye`, `pattern_samples`, `statistical_ber`, `fold_eye`, `zf_equalizer`, `apply_ffe`, `simulate_binary`.
- `17-04-baseband-lab.ipynb`: the guided notebook.
- `rc_channel.cir`: ngspice transient of a single 40 ps bit through a 5 GHz one-pole RC network, sampled at the bit ends.

## Procedure

1. **Nyquist's criterion.** For the four spectra of Problem 17-04.5, predict which give zero ISI; then fold each numerically and sample its pulse.
2. **Eyes on an RC channel.** For a 5 GHz pole, predict the worst-case eye at 10, 25 and 45 Gb/s; then simulate random NRZ through `rc_channel`, fold the eyes and measure the openings.
3. **Timing sensitivity.** Predict how the eye of sinc and raised-cosine (α = 0.22, 0.5) pulses shrinks as the sampling instant moves from 0 to 0.3T; then sweep it.
4. **Equalization.** For the channel of Example 17-04.5 at σ = 0.25, predict the bit-error rate with no equalizer, the three-tap ZF FFE and a two-tap DFE; then simulate.
5. **PAM4 against NRZ.** At the same bit rate through a one-pole channel, predict which has the larger worst-case eye relative to its level spacing; then compare the eyes.
6. **ngspice.** Run `python tools/run_spice.py 17-04` and compare $h_0$ and $h_1$ with $1 - r$ and $(1 - r)r$.

## Expected results

- Part 1: (a), (c) and (d) pass; (b) fails with $h(T)/h(0) = -0.156$.
- Part 2: worst-case eyes of 0.914, 0.431 and 0.005 of the ideal at 10, 25 and 45 Gb/s (the last just short of closing at 45.3 Gb/s); the simulated eyes match.
- Part 3: the sinc eye closes within about 0.1T; the raised-cosine eyes degrade gradually, more slowly for larger α.
- Part 4: the DFE's error rate is close to the statistical eye with only the precursor left, $8.2 \times 10^{-5}$, a little higher because of error propagation; both equalizers beat no equalization.
- Part 5: NRZ keeps the larger worst-case eye at every rate. On a one-pole channel PAM4 never wins: with $x = e^{-T_{\text{NRZ}}/\tau}$, NRZ's eye is $1 - 2x$ and PAM4's (relative to its peak) is $(1 - 4x^2)/3 = (1 - 2x)(1 + 2x)/3$, a factor $(1 + 2x)/3 < 1$ smaller, and both close at the same bit rate.
- Part 6: 0.715 and 0.204.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-04.a | worst-case eye, 5 GHz pole, 10 Gb/s | 0.914 | — |
| Lab 17-04.b | worst-case eye, 5 GHz pole, 45 Gb/s | 0.005 | — |
| Lab 17-04.c | BER after a two-tap DFE with correct decisions, σ = 0.25 | 8.2e-5 | — |

## Discussion

1. Why does the worst-case eye of the one-pole channel depend only on $r = e^{-T/\tau}$?
2. In Part 4, why does the DFE's simulated error rate match a statistical eye containing only the precursor?
3. Why can an eye diagram look open while the measured error rate is poor?

### Answers

1. The pulse response is self-similar: every cursor is $(1 - r)r^k$, so their sum and the main cursor depend only on how much the output decays in one bit, which is $r$.
2. With correct decisions the DFE subtracts the postcursors exactly, so only $h_{-1}$ remains as ISI. Errors are rare at σ = 0.25, so error propagation adds only a modest fraction (each error makes the next decision likelier to fail, which is why the simulated rate sits somewhat above the statistical eye).
3. The eye drawn from a short record may never include the rare worst-case patterns, and noise enhancement or jitter can be hidden by averaging or by the display; the BER counts every pattern.

## Optional hardware

With an oscilloscope and a pattern generator (or a microcontroller toggling a pin through an RC low-pass filter), display the eye of a pseudo-random bit stream at several rates and compare its opening with $1 - 2e^{-T/\tau}$.
