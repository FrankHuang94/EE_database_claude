# Lab 20-08 · Delta-Sigma Modulators: Traces, Noise Shaping, Stability, MASH and Jitter

Chapter: [20-08 · Oversampling and Sigma-Delta Converters](../../chapters/20-08-sigma-delta-converters.md)

## Objective

- Confirm the first-order loop's arithmetic in a circuit simulator, with and without excess loop delay.
- See idle tones appear for small DC inputs.
- Measure noise shaping: SQNR against OSR and order, and the output spectrum's slope.
- See a high-order 1-bit loop go unstable, and stabilize it with Lee's rule.
- Measure a MASH's sensitivity to op-amp gain and a continuous-time loop's sensitivity to clock jitter.

## Background

`dsm.py` contains `mod1` (first order), `mod2` (second order, any number of quantizer levels), `ef_mod` (any NTF in error-feedback form), `lee_ntf` (Butterworth-pole NTFs with a chosen peak gain), `mash11` (1-1 MASH with a leaky first integrator), `ct1` (the sampled continuous-time first-order loop with excess loop delay) and the helpers `inband_sqnr`, `sqnr_formula`, `cic_gain` and `jitter_noise`. Levels span [−1, 1]; 0 dBFS is a sine of amplitude 1; spectra use 65,536 samples, a Hann window and a sine at about a third of the band edge. `ct_dsm.cir` builds two continuous-time first-order loops (1 µs clock, integrator time constant equal to the clock period, a tanh comparator and a switch-and-capacitor master-slave latch); the second has a third latch stage that delays its DAC by half a period.

## Procedure

1. **Traces.** Run `ngspice -b ct_dsm.cir` and compare the integrator voltages at the clock edges with Examples 20-08.2 and 20-08.7. Simulate `mod1` with DC inputs of 0.002 and 0.01 and look at the low-frequency spectrum (Part 1).
2. **Noise shaping.** Simulate `mod1` and `mod2` at −6 dBFS for OSR = 32, 64 and 128 and compare with `sqnr_formula`; plot the spectra on a log-frequency axis; repeat `mod2` with 16 levels (Part 2).
3. **Stability.** Run `ef_mod` with $(1 - z^{-1})^3$ and $(1 - z^{-1})^4$ NTFs, then with `lee_ntf(3)` and `lee_ntf(4)`; record the largest quantizer input and the SQNR averaged over eight input phases (Part 3).
4. **MASH and jitter.** Run `mash11` with ε = 0, 10⁻³ and 10⁻²; compute `jitter_noise` for the 1-bit and 16-level second-order streams (Part 4).

## Expected results

- **Part 1.** ngspice's integrator voltages match the hand traces to a few microvolts, and both loops' outputs average exactly 0.2 V over 40 periods. For $x$ = 0.002 the spectrum shows lines at multiples of $xf_s$ with amplitude $2x$ (−48.0 dBFS); a larger DC input moves the lines up in frequency and makes them stronger.
- **Part 2.** 47.7 dB (first order) and 70.3 dB (second order) at OSR = 64, against the model's 44.8 and 73.2 dB; 54.3 and 84.2 dB for the second order at OSR = 32 and 128; 97.0 dB with 16 levels. The spectra rise at 20 and 40 dB per decade.
- **Part 3.** The pure third- and fourth-order loops diverge (the quantizer input grows without bound). The Lee-rule loops keep the quantizer input bounded and reach **80** and **90** dB at OSR = 64.
- **Part 4.** MASH: **73.2** dB ideal, **72.8** dB with ε = 10⁻³ (A = 1000) and **59.7** dB with ε = 10⁻² (A = 100). Jitter: E[(Δy)²] = 2.36 (1-bit) and 0.0298 (16 levels).

## Discussion

1. **Why do the Lee-rule results vary by about a decibel with the input phase?** A high-order 1-bit loop is a nonlinear system with chaotic sensitivity: a change in the last bit of one sample changes every later decision. Only averages over many runs are reproducible, which is why the expected results quote phase averages.
2. **Why does the MASH simulation beat the white-noise model at A = 100?** The first stage's quantization error is not white: much of its power lies at high frequency, so less of the leaked error falls in band.
3. **What would a return-to-zero DAC do to the jitter result?** It makes every period contain two edges whatever the data, so the jitter error no longer depends on $\Delta y$ but on $y$ itself: more edges, but the charge error per edge no longer depends on the data pattern.

## Optional hardware

A first-order modulator can be built from an op-amp integrator, a comparator and a D flip-flop clocked at a few hundred kilohertz, with the flip-flop output fed back through a resistor. Average its output with an RC filter and compare with the DC input; then feed a slow sine and look at the bitstream's density on an oscilloscope.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-08.a | MASH SQNR, ideal | 73.2 | dB |
| Lab 20-08.b | MASH SQNR, A = 1000 | 72.8 | dB |
| Lab 20-08.c | MASH SQNR, A = 100 | 59.7 | dB |
| Lab 20-08.d | Lee-rule SQNR, L = 3 | 80 | dB |
| Lab 20-08.e | Lee-rule SQNR, L = 4 | 90 | dB |
