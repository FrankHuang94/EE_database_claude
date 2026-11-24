# Lab 20-10 · PLL Loop Dynamics, Noise, Jitter and Fractional-N Spurs

Chapter: [20-10 · PLLs and Jitter](../../chapters/20-10-plls-and-jitter.md)

## Objective

- Confirm a third-order charge-pump loop's crossover and phase margin in ngspice.
- See how the pole/zero spread b trades phase margin, peaking and settling.
- Split the output phase noise into reference and VCO contributions and find a good loop bandwidth.
- Integrate phase noise to jitter and see how the integration band changes the answer.
- Watch a MASH fractional-N divider produce shaped noise for a "busy" fraction and spurs for a simple one.

## Background

`pll.py` contains the phase-domain model (`loop_filter_z`, `open_loop`, `closed_loop`), `design_third_order`, `crossover_and_pm`, `step_settle`, `integrate_jitter`, `mash_sequence` (integer accumulators, as in hardware), `divider_phase_psd`, and the figures of merit `fom_jitter`, `fom_oscillator` and `tdc_floor`. `loop.cir` is the open loop of Example 20-10.2 built from controlled sources: voltages represent phases.

## Procedure

1. **Open loop.** Run `ngspice -b loop.cir`; compare with `crossover_and_pm` (Part 1).
2. **Spread.** Redesign the loop for b = 4, 10 and 20 at the same crossover; plot the closed-loop phase-step responses and the closed-loop gain (Part 2).
3. **Noise.** With −150 dBc/Hz reference noise and a VCO at −120 dBc/Hz at 1 MHz (falling 20 dB per decade), compute the output phase noise for crossovers of 0.1, 0.3, 1, 2 and 5 MHz and integrate each to jitter (Part 3).
4. **Jitter bands.** Integrate the profile of Example 20-10.5 from 12 kHz to 20 MHz and from 10 kHz to 100 MHz (Part 4).
5. **Fractional-N.** Generate the MASH 1-1-1 sequence for 123/500 and for a busy fraction ($2^{23} + 12345$ out of $2^{25}$); compute the phase-error spectra and compare the busy one with `divider_phase_psd` (Part 5).

## Expected results

- **Part 1.** ngspice and the Python model agree: 2.00 MHz crossover and 54.9° of phase margin.
- **Part 2.** b = 4, 10 and 20 give 36.9°, 54.9° and 64.8° of margin; the lowest margin rings longest and peaks most.
- **Part 3.** The reference path dominates in band and the VCO outside. Integrated from 1 kHz to 1 GHz the jitter is about 226, 172, 226, 309 and 483 fs: the minimum, about 172 fs, sits near 0.3 MHz, where $N^2$ times the reference noise (−110 dBc/Hz) meets the VCO's −120 dBc/Hz·(1 MHz/f)² line (§3.4). Wider loops let in more multiplied reference noise; narrower ones leave the VCO uncorrected.
- **Part 4.** **876** fs for 12 kHz–20 MHz and **895** fs for 10 kHz–100 MHz: for this profile most of the jitter lies within a few times the loop bandwidth, so the band changes little. A noisier tail beyond 20 MHz would change it a lot.
- **Part 5.** The 123/500 sequence repeats every 1000 reference cycles and its spectrum is a comb of spurs 50 kHz apart; the busy fraction follows the formula to within the spectral estimate's scatter (a decibel or two for the notebook's record length; longer records converge on it).

## Discussion

1. **Why does ngspice need no knowledge of "phase"?** The phase-domain model is linear: a current proportional to a voltage, an impedance, an integrator and a gain. Any linear circuit simulator can evaluate it if voltages stand for phases.
2. **Why does a simple rational fraction make spurs?** The accumulators return to the same state after a fixed number of cycles, so the divide pattern, and the phase error it creates, is periodic: its spectrum is a set of lines, not noise.
3. **Where would you set the loop bandwidth of a fractional-N PLL with a noisy VCO?** Wide enough to suppress the VCO, narrow enough to filter the ΔΣ noise that rises at 40 dB per decade; the lab's Part 3 and Part 5 together show the compromise.

## Optional hardware

Evaluation boards for integer and fractional-N synthesizers come with loop-filter calculators and phase-noise plots. Changing the charge-pump current setting and measuring the phase-noise plot's in-band level and bandwidth reproduces Part 3.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-10.a | jitter, 12 kHz to 20 MHz | 876 | fs |
| Lab 20-10.b | jitter, 10 kHz to 100 MHz | 895 | fs |
| Lab 20-10.c | Part 3 jitter at 0.1 MHz | 226 | fs |
| Lab 20-10.d | Part 3 jitter at 0.3 MHz (minimum) | 172 | fs |
| Lab 20-10.e | Part 3 jitter at 1 MHz | 226 | fs |
| Lab 20-10.f | Part 3 jitter at 2 MHz | 309 | fs |
| Lab 20-10.g | Part 3 jitter at 5 MHz | 483 | fs |
| Lab 20-10.h | reference-VCO crossing | 0.316 | MHz |
| Lab 20-10.i | multiplied reference noise | −110 | dBc/Hz |
