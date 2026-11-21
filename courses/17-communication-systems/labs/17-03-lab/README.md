# Lab 17-03 · Analog Modulation and Its Noise

Chapter: [17-03 · Analog Modulation (Brief)](../../chapters/17-03-analog-modulation.md)

## Objective

Build each analog modulator and detector in discrete time and check the chapter's results:

- the phasing method's single sideband, and what imperfect quadrature does to it;
- Bessel-function spectra of tone FM;
- the output SNR of DSB-SC, SSB and AM receivers against the baseband reference;
- FM's $\tfrac32\beta^2$ gain above threshold and its collapse below;
- FM's parabolic output noise and what de-emphasis removes.

## Background

All schemes are compared at the same received power $S_R$ and noise density $N_0$ through $\gamma = S_R/(N_0W)$ (§3.1). Bandpass signals are simulated either directly at a carrier (DSB, SSB, AM) or in complex baseband (FM), with noise scaled from $N_0$: a real passband sample has noise variance $N_0f_s/2$, and each of the I and Q components of complex-baseband noise has variance $N_0f_s$ (17-01 §3.9). Output SNR is measured by projecting the receiver output onto the known message; everything not explained by the message counts as noise.

## Files

- `analogmod.py`: `hilbert`, `ssb`, `dsb_sc`, `am`, `envelope`, `coherent_demod`, `lowpass`, `fm_baseband`, `pm_baseband`, `fm_discriminator`, `preemphasis`, `deemphasis`, `bessel_lines`, `power_fraction`, `carson`, `snr_theory_db`, `measured_snr_db`, `simulate_linear_snr`, `simulate_fm_snr`.
- `17-03-analog-modulation-lab.ipynb`: the guided notebook.

## Procedure

1. **SSB by phasing.** Generate upper-sideband SSB of a two-tone message and plot its spectrum. Predict the unwanted sideband's level with a 1° quadrature error, then measure it.
2. **Bessel lines.** For β = 1, 2.405 and 5, predict the carrier and first few sidebands, then compare an FFT of simulated tone FM with $\lvert J_n(\beta)\rvert$.
3. **Four receivers.** Predict DSB, SSB and AM output SNR at γ = 30 dB (AM with $k_a$ = 0.9 and the lab's three-tone message), then run `simulate_linear_snr`.
4. **FM threshold.** Predict the FM output SNR for γ from 12 to 40 dB with β-equivalent deviation ratio 5, sweep `simulate_fm_snr`, and mark where the curve leaves the formula. Repeat with `if_factor=1.5`.
5. **De-emphasis.** Estimate the discriminator's output noise spectrum with no modulation, confirm the $f^2$ shape, and measure the noise reduction from 75 µs de-emphasis over 15 kHz.

## Expected results

- Part 1: the unwanted sideband about 41 dB down with a 1° error, and below the numerical floor with none.
- Part 2: FFT line magnitudes equal $\lvert J_n(\beta)\rvert$; the carrier vanishes at β = 2.405.
- Part 3: DSB and SSB at 30 dB; AM at $10\log_{10}[k_a^2P_m/(1 + k_a^2P_m)] + 30$ dB, about 20.8 dB for the lab's message.
- Part 4: about 45.7 dB at γ = 30 dB; the simulation follows the formula down to γ ≈ 21 dB (10 dB CNR in Carson's band) and then collapses; with the IF filter at exactly Carson's bandwidth the output SNR approaches a distortion floor near 57 dB at high γ (about 53 dB at γ = 40 dB).
- Part 5: a parabola, and a reduction of about 13.2 dB.

### Lab answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 17-03.a | predicted FM output SNR at γ = 30 dB, D = 5, tone | 45.74 | dB |
| Lab 17-03.b | predicted DSB and SSB output SNR at γ = 30 dB | 30 | dB |
| Lab 17-03.c | γ at the FM threshold (10 dB CNR in 12W) | 20.79 | dB |

## Discussion

1. Why does the phasing modulator need a Hilbert transformer that works over the whole message band, and why is that hard for voice down to 300 Hz in analog hardware?
2. In Part 4, why does the IF filter's width not affect the output SNR above threshold, but does affect the threshold and the high-SNR distortion floor?
3. Why is the AM receiver's SNR in Part 3 so much lower than DSB's, when both use the same bandwidth?

### Answers

1. Every message frequency must be shifted by exactly 90°; an analog all-pass network approximates this only over a limited ratio of frequencies, and errors there leave the unwanted sideband partly unsuppressed (Problem 17-03.13). A digital FIR Hilbert transformer does it accurately except near DC and Nyquist.
2. Above threshold, the output noise is set by the noise inside the final low-pass filter's band $W$, which the IF filter does not change. The IF filter does change the total noise the limiter and discriminator see, which sets where clicks begin, and a filter as narrow as Carson's bandwidth also clips the signal's own spectral tails, adding distortion that limits the SNR at high γ.
3. Most of AM's power is carrier, which carries no message; only the sideband fraction $k_a^2P_m/(1 + k_a^2P_m)$ (about 12% here) contributes signal, while the noise in the $2W$ band is the same as DSB's.

## Optional hardware

A low-cost software-defined-radio dongle tuned to a local FM station gives complex baseband samples at a few hundred kilosamples per second. Apply `fm_discriminator`, then 75 µs or 50 µs de-emphasis, and listen; plot the discriminator output spectrum to see the mono audio, the 19 kHz pilot and the 23–53 kHz L − R band of a stereo station.
