# Lab 21-05 · Mixers: Conversion, Images, Harmonics, Noise Folding and N-Path Filters

Chapter: [21-05 · Mixers](../../chapters/21-05-mixers.md)

## Objective

- See frequency translation, the image and the LO-harmonic responses in a simulated spectrum.
- Confirm the commutating mixer's conversion gain and harmonic response in ngspice.
- Measure noise folding by multiplying random noise by a square wave.
- Map image rejection against gain and phase error, and harmonic rejection against LO mismatch.
- Simulate a 4-path filter and measure its bandwidth and centre loss.

## Background

`mixer.py` holds `conversion_gain_square`, `irr_db` (exact) and `irr_small_db`, `hr_weights` and `composite_lo_harmonics` (FFT of a weighted sum of phase-shifted square waves) and `ssb_nf_from_dsb`. `mixer.cir` contains four ideal-switch circuits: a double-balanced passive mixer at its fundamental and at the LO's 3rd harmonic, a Gilbert-type commutated transconductor, and a 4-path filter driven by four 25 % clock phases; each output amplitude is measured by correlating a uniformly resampled waveform with sine and cosine.

## Procedure

1. **Spectrum.** Multiply a 2.45 GHz tone and a 7.25 GHz tone by a 2.40 GHz square wave and plot the output spectrum near the 50 MHz IF (Part 1).
2. **ngspice.** *Predict* the four measured gains, then run `ngspice -b mixer.cir` (Part 2).
3. **Noise folding.** Multiply white noise by a square wave and measure the IF noise against the share that comes from the signal band; repeat with the image removed (Part 3).
4. **Image and harmonic rejection.** Map the IRR over gain errors of 0–5 % and phase errors of 0–5°; then compute the harmonic-reject LO's 3rd and 5th responses against weight and phase error (Part 4).
5. **N-path filter.** Simulate the 4-path filter of Example 21-05.8 at its centre and at ±BW/2 (Part 5).

## Expected results

- **Part 1.** Both tones land at 50 MHz, the 7.25 GHz one 9.5 dB weaker.
- **Part 2.** −3.92 dB, −13.46 dB, +16.08 dB and −1.82 dB, matching $2/\pi$, $2/(3\pi)$, $(2/\pi)g_mR_L$ and the N-path centre loss.
- **Part 3.** The unfiltered noise factor comes out near $\pi^2/4$: **3.8** dB in the seeded simulation (a few tenths of a decibel of scatter between seeds); removing the image brings it to about 1.7 dB.
- **Part 4.** 40 dB near 1 % and 1°; the harmonic-reject LO's 3rd response rises from zero to −55.6 dB for 1 % weight error and about −44 dB for 1° phase error.
- **Part 5.** −1.82 dB at 1 GHz, and **−2.96** dB and **−3.06** dB (relative to the centre) at +3.98 MHz and −3.98 MHz: the averaging model's 3 dB points, with a small asymmetry from the sampled nature of the circuit.

## Discussion

1. **Why does white noise stay white after multiplication by a square wave?** Because $s^2(t) = 1$: the product's autocorrelation equals the noise's. The signal, by contrast, is converted with gain $2/\pi$, which is why folding costs SNR.
2. **Why is phase error more damaging than weight error in the harmonic-reject LO?** A weight error on the middle phase disturbs one term of each cancelling sum; a phase error on an outer phase rotates a term whose partner then no longer cancels it, and it affects the 3rd and 5th harmonics equally.
3. **Why does the N-path filter need $NR_sC \gg 1/f_{LO}$?** The capacitors must average over many LO cycles for each to see a nearly constant input phase; otherwise the staircase approximation and the averaging bandwidth formula both fail.

## Optional hardware

A passive diode-ring mixer module, two signal generators and a spectrum analyzer show conversion loss directly: set the LO to the data sheet's drive level, apply an RF tone, and measure the IF. Then move the RF to near three times the LO frequency and measure the 3rd-harmonic response, and reduce the LO drive by a few decibels and watch the conversion loss and the IM3 of two RF tones rise.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 21-05.a | seeded Monte Carlo unfiltered SSB NF | 3.8 | dB |
| Lab 21-05.b | N-path response at +BW/2 relative to the centre | −2.96 | dB |
| Lab 21-05.c | N-path response at −BW/2 relative to the centre | −3.06 | dB |
