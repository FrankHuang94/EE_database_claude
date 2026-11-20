# Lab 17-01 · Measuring Random Processes

Chapter: [17-01 · Random Processes and Power Spectral Density](../../chapters/17-01-random-processes-and-psd.md)

## Objective

Estimate autocorrelations and power spectral densities from simulated data and check them against the chapter's theory:

- ensemble against time averages;
- noise through filters and noise bandwidth;
- the spectra of digital (PAM) signals;
- noise folding when wideband noise is sampled;
- the in-phase and quadrature components of bandpass noise.

Confirm the resonant-circuit noise of Example 17-01.3 with an ngspice noise analysis.

## Background

The Wiener–Khinchin theorem (§3.4) says the PSD is the transform of the autocorrelation, and §3.5 says a filter multiplies it by $\lvert H\rvert^2$. Measured spectra are averaged periodograms (Welch's method, 16-05), which estimate the PSD with a scatter that falls as one over the square root of the number of averaged segments. All densities in this lab are in V²/Hz into 1 Ω; `psd_welch` returns one-sided densities unless asked for two-sided ones.

## Files

- `randproc.py`: estimators (`autocorr_time`, `autocorr_ensemble`, `psd_welch`), models (`white_noise`, `ou_samples` for exactly sampled RC-filtered noise, `ar1_psd`, `lorentzian_two_sided`, `aliased_density`), PAM (`pam_waveform`, `nrz_psd`, `nrz_power_fraction`, `pam_line_power`), bandpass noise (`bandpass_noise`, `iq_components`), circuits (`rlc_vc_density`) and a numerical Bochner test (`is_valid_autocorrelation`).
- `17-01-random-processes-lab.ipynb`: the guided notebook.
- `rlc_noise.cir`: ngspice noise analysis of a resistor driving a series L–C, measured across C, for $R$ = 5 Ω and 50 Ω.

## Procedure

1. **Ensemble against time.** Generate 2000 short AR(1) records ($a$ = 0.9, $\sigma_w^2$ = 1) and one long record. Predict $R[0]$ and $R[1]$, then compare the ensemble estimate at a fixed time with the time-average estimate of the long record.
2. **Noise through a filter.** Simulate Example 17-01.2's white noise and one-pole filter as exactly sampled RC noise; predict the rms from the noise bandwidth, then measure it and the correlation at 100 ns.
3. **Data spectra.** Estimate the PSDs of polar and unipolar NRZ and of half-sine PAM at 16 samples per symbol. Before plotting, predict the nulls, the DC line and the half-sine's first null.
4. **Noise folding.** Sample exponentially correlated noise with $\tau_c$ = 0.1 µs and 1 µs at 1 MS/s; predict the in-band density ratio, then compare the AR(1) closed form, the alias sum and a Welch estimate.
5. **I/Q noise.** Down-convert simulated bandpass noise centred on the oscillator, then offset by 5 MHz. Predict the powers of $n_I$, $n_Q$ and their correlation at lag 0 and at other lags.
6. **ngspice.** Run `ngspice -b rlc_noise.cir` (or `python tools/run_spice.py 17-01`) and compare the two rms values with $\sqrt{kT/C}$.

## Expected results

- Part 1: both estimates approach $R[0] = 1/(1 - 0.81)$ = 5.26 and $R[1]$ = 4.74, within a few percent, because the AR(1) process is ergodic.
- Part 2: 12.5 µV rms and a correlation of 0.53 at 100 ns (Example 17-01.2).
- Part 3: nulls at multiples of the bit rate; a DC line holding half the unipolar signal's power; the half-sine's first null at $1.5/T$ and much lower sidelobes.
- Part 4: density ratios of 5.00 and 1.08 (Example 17-01.5); the three methods agree.
- Part 5: $n_I$ and $n_Q$ each carry the bandpass power; zero-lag correlation near 0 in both cases; with the offset band, large correlations at nonzero lags.
- Part 6: ngspice gives 2.035 µV for both resistors.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-01.a | rms capacitor voltage, R = 50 Ω (ngspice) | 2.035 | µV |
| Lab 17-01.b | AR(1) R[1], a = 0.9 | 4.74 | — |

## Discussion

1. In Part 1, why does the ensemble estimate at one instant agree with a time average over one record? Name a process for which it would not (03-06).
2. In Part 3, why does the half-sine pulse have a wider main lobe but less power outside $\lvert f\rvert < 1/T$?
3. In Part 4, why does the total power of the samples not depend on the sample rate, while the in-band density does?
4. In Part 5, why must the zero-lag correlation of $n_I$ and $n_Q$ vanish even for the offset band?

### Answers

1. The AR(1) process is ergodic: its covariance decays, so time averages converge to ensemble averages. A population of amplifiers with random fixed offsets is not: one unit's time average converges to its own offset.
2. The half-sine has no jumps, so its spectrum falls as $1/f^2$ in amplitude ($1/f^4$ in power) against $1/f$ for NRZ's sharp edges; the price is a main lobe 1.5 times wider.
3. Sampling preserves $R(0)$, the total power, but folds every frequency into $\lvert f\rvert < f_s/2$; the same power in a narrower band is a higher density.
4. $R_{n_In_Q}(\tau)$ is odd for any WSS bandpass noise (§3.9), so it is zero at τ = 0; only the lagged correlations depend on symmetry.

## Optional hardware

With a sound card (or any ADC with a known sample rate) and a resistor, record the input with nothing connected and with a large resistor across it, estimate both PSDs with Welch's method, and compare the difference with $4kTR$ (expect the sound card's own noise to dominate unless the resistor is above about 100 kΩ). A low-cost software-defined radio receiving with its antenna replaced by a 50 Ω load shows its own I/Q noise: check that the two channels have equal power and nearly zero zero-lag correlation.
