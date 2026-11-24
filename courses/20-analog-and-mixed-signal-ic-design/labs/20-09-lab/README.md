# Lab 20-09 · DACs: Ladders, Segmentation, Yield, Output Impedance, Spectra and Element Matching

Chapter: [20-09 · DACs](../../chapters/20-09-dacs.md)

## Objective

- Solve an R-2R ladder by nodal analysis and see where switch resistance hurts; confirm it in ngspice.
- Compare binary, unary and segmented current-steering DACs under random mismatch.
- Check the INL-yield rules of §3.4 by Monte Carlo.
- See output-impedance compression in ngspice and its harmonics, single-ended and differential.
- Plot NRZ, RZ and mixed-mode responses, and watch data-weighted averaging shape a DAC's mismatch.

## Background

`dac.py` contains `r2r_output` (a voltage-mode ladder with optional mismatch and switch resistance), `string_dac`, `cs_levels` (segmented current-steering levels with random unit errors), `inl_dnl`, `zout_levels` (single-ended and differential compression), `harmonics`, `zoh_gain` (NRZ, RZ and mixed-mode pulses) and `dwa_select`. `r2r.cir` is a 10-bit ladder (R = 1 kΩ, $V_{REF}$ = 1.2 V) in four copies; `zout.cir` is a 15-cell DAC (1 mA cells with 50 kΩ output resistance into 50 Ω).

## Procedure

1. **Ladders.** Compute code 683 and the DNL and INL of a ladder with a 1% switch resistance; run `ngspice -b r2r.cir` (Part 1).
2. **Segmentation.** Generate 2000 random 14-bit DACs (σ_u = 0.5%) in binary, unary and 6 + 8 segmented form; compare the spread of DNL at the worst transition (Part 2).
3. **Yield.** Simulate 4000 unary 12-bit DACs at σ_u = 0.521% and 0.430% and count those with max |INL| ≤ ½ LSB (Part 3).
4. **Output impedance.** Run `ngspice -b zout.cir`; then compute the harmonics of the single-ended and differential outputs of a 12-bit DAC with $xN_t$ = 0.0643 (Part 4).
5. **Spectra and DWA.** Plot the NRZ, RZ and mixed-mode responses to $2f_s$. Then drive a 16-element DAC whose elements have a ±1% linear gradient with a 41-cycle sine (4096 samples, codes 0 to 16) using fixed (thermometer) selection and DWA, and compare the in-band error at OSR = 16 (Part 5).

## Expected results

- **Part 1.** 0.8004 V; with 1% switch resistance, worst DNL −1.68 LSB at the 511 → 512 transition (the output falls 0.80 mV: non-monotonic) and worst INL 0.84 LSB. ngspice agrees. With every leg made 2R − r_sw the DNL vanishes; padding only the termination leaves it at −1.69 LSB.
- **Part 2.** The DNL spreads at the worst step follow §3.3: about 0.64, 0.005 and 0.11 LSB.
- **Part 3.** About 98% of designs pass at 0.521%, and about 99.7% at 0.430%; the exact rule is the one that meets the target.
- **Part 4.** ngspice: 0.7389 V at full scale and 0.0556 LSB of INL. Harmonics: single-ended HD2 −36.1 dBc; differential HD2 cancelled, HD3 −72.3 dBc.
- **Part 5.** The responses match Example 20-09.5. The in-band mismatch error, relative to the signal, is **−52.5** dB with fixed selection and **−85.5** dB with DWA: the same elements, used in rotation, push the error out of band.

## Discussion

1. **Why does the switch resistance give a DNL error twice its INL error?** Every leg is a little too resistive, so the MSB's weight ends up low by about ε relative to the sum of the lower bits; INL peaks at about ε/2 on either side of mid-scale with opposite signs, and the DNL at the MSB step is the full (negative) jump between them.
2. **Why is the mid-scale yield estimate optimistic?** It checks one code. The INL is a random walk pinned at both ends, and its maximum over all codes is larger than its mid-scale value.
3. **Why does DWA's error look like first-order shaped noise?** Each element's usage count never differs from any other's by more than one, so the accumulated error is bounded and the error itself is its first difference.

## Optional hardware

Build a 4-bit R-2R ladder from 1% resistors and an MCU's GPIO pins, measure every code with a multimeter, and compute the DNL. Then swap in 5% resistors for the MSB leg and watch the mid-scale step.

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 20-09.a | in-band error, fixed selection | −52.5 | dB |
| Lab 20-09.b | in-band error, DWA | −85.5 | dB |
